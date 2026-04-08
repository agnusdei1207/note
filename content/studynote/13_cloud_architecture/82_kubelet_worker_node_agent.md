+++
title = "82. Kubelet (큐블렛) - 마스터 노드의 명령을 받아 파드(Pod)를 생성/관리하고 헬스체크 결과를 보고하는 노드별 에이전트"
date = "2026-04-07"
[extra]
categories = "studynote-cloud"
+++

# Kubelet (큐블렛): 쿠버네티스 워커 노드 에이전트

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Kubelet (큐블렛)은 쿠버네티스 (Kubernetes) 클러스터의 각 워커 노드 (Worker Node) 위에서 실행되는 에이전트 프로세스로, 마스터 노드의 API Server가 할당한 Pod (포드) 명세(Spec)를 받아 컨테이너 런타임 (Container Runtime) 을 통해 실제 컨테이너를 기동·유지·감시하는 "노드의 관리자"다.
> 2. **가치**: 클러스터에 수천 개의 노드가 있어도 각 노드의 Kubelet이 독립적으로 로컬 Pod 상태를 지속 감시하며 API Server에 헬스리포트를 제출함으로써, 중앙 제어 평면이 모든 Pod 상태를 실시간으로 파악하고 장애 자동 복구(Self-Healing)를 수행할 수 있게 한다.
> 3. **융합**: Kubelet은 CRI (Container Runtime Interface)를 통해 containerd·CRI-O 등 다양한 컨테이너 런타임과 추상화된 방식으로 통신하고, CNI (Container Network Interface)와 CSI (Container Storage Interface) 플러그인을 통해 네트워크와 스토리지 프로비저닝을 조율한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: Kubelet은 각 워커 노드에 데몬(Daemon)으로 상시 실행되며 세 가지 핵심 역할을 수행한다. ① API Server로부터 해당 노드에 배치된 Pod Spec(PodSpec YAML)을 수신, ② 명세에 따라 컨테이너를 생성·기동·정지, ③ 컨테이너의 Liveness/Readiness Probe를 주기적으로 수행하여 상태를 API Server에 보고.
- **필요성**: 수천 개의 컨테이너가 분산 배포된 환경에서 중앙 서버가 모든 컨테이너를 직접 제어하고 감시하는 것은 불가능하다. Kubelet이 각 노드의 "현장 담당자"로서 로컬에서 자율 관리하기 때문에 쿠버네티스가 수천 노드로 확장 (Scale-Out) 가능하다.
- **💡 비유**: Kubelet은 본사(API Server)가 지시한 인력 배치표(PodSpec)를 받아, 현장 공장(Worker Node)에서 실제로 직원(Container)을 채용하고 근무 상태를 감시·보고하는 공장 라인 관리자다.
- **등장 배경**: 구글 Borg 시스템의 "borglet" 에이전트에서 영감을 받아 쿠버네티스 초기에 설계됨. CRI 추상화 계층이 도입되면서 도커(Docker) 외에 containerd, CRI-O 등 다양한 런타임 지원이 가능해졌다.

```text
┌────────────────────────────────────────────────────────┐
│       쿠버네티스 노드 아키텍처에서 Kubelet 위치              │
├────────────────────────────────────────────────────────┤
│                                                        │
│  [마스터 노드 (Control Plane)]                           │
│   ├─ API Server ◀──────── kubectl                      │
│   ├─ Scheduler (Pod 노드 배치 결정)                      │
│   ├─ Controller Manager (상태 조정)                     │
│   └─ etcd (클러스터 상태 저장소)                          │
│          │                                             │
│          │ PodSpec 할당 / 상태 Watch                    │
│          ▼                                             │
│  [워커 노드 (Worker Node)]                              │
│   ├─ Kubelet ◀──── API Server에서 PodSpec 수신          │
│   │    ├─ CRI를 통해 컨테이너 런타임에 Pod 기동 요청       │
│   │    ├─ Liveness · Readiness Probe 실행              │
│   │    └─ 노드 상태·Pod 상태를 API Server에 주기 보고     │
│   ├─ Kube-Proxy (네트워크 규칙 관리)                     │
│   └─ 컨테이너 런타임 (containerd / CRI-O)               │
└────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 구조도는 Kubelet이 제어 평면(Control Plane)과 실제 컨테이너 런타임 사이에서 "번역기 겸 감시자" 역할을 담당함을 보여준다. API Server로부터 PodSpec을 Watch(구독)하고, 변경 사항이 생기면 즉시 CRI(containerd 등)를 호출하여 컨테이너를 생성·삭제·재시작한다. 동시에 주기적으로 Probe(헬스 체크)를 실행하고 API Server에 상태를 보고함으로써 Scheduler와 Controller Manager가 정확한 클러스터 상태 정보를 바탕으로 의사결정(예: 죽은 Pod 재스케줄링)을 내릴 수 있게 한다.

- **📢 섹션 요약 비유**: 본사 인사팀(API Server)이 "A동 2층에 직원 3명 배치"를 지시하면, 현장 관리자(Kubelet)가 직접 채용하고 출근 상태를 매일 인사팀에 보고하는 구조입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Kubelet 주요 컴포넌트와 동작

| 컴포넌트 | 역할 | 관련 기술 |
|:---|:---|:---|
| **PodSpec 동기화** | API Server로부터 해당 노드의 PodSpec을 Watch/Pull로 수신 | etcd Watch, HTTP Long-Polling |
| **CRI (Container Runtime Interface)** | containerd·CRI-O 등 런타임과 표준 gRPC 인터페이스로 통신 | gRPC, Protobuf |
| **Liveness Probe** | 컨테이너가 살아 있는지 주기 HTTP/TCP/Exec 체크, 실패 시 재시작 | `livenessProbe` spec |
| **Readiness Probe** | 트래픽 수신 준비 여부 체크, 실패 시 Service 엔드포인트에서 제외 | `readinessProbe` spec |
| **Startup Probe** | 느린 기동 앱을 위해 초기화 완료 전까지 Liveness 체크 유예 | `startupProbe` spec |
| **cAdvisor** | 컨테이너별 CPU·메모리·네트워크 메트릭 수집, Prometheus 연동 | `/metrics` HTTP endpoint |

---

### Kubelet Probe 동작 흐름

헬스 프로브(Probe)는 Kubelet의 자가 치유(Self-Healing) 기능의 핵심 엔진이다. Liveness Probe 실패는 컨테이너 재시작을, Readiness Probe 실패는 Service 엔드포인트에서의 제외를 트리거한다.

```text
┌───────────────────────────────────────────────────────────┐
│         Kubelet Probe 동작 상태 전이도                       │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  [컨테이너 시작]                                             │
│       │                                                   │
│       ▼                                                   │
│  Startup Probe 설정 시 → 성공할 때까지 Liveness 유예         │
│       │                                                   │
│       ▼                                                   │
│  ┌─ Liveness Probe (주기적 실행) ─┐                         │
│  │  성공 → 정상 운영 계속           │                        │
│  │  실패 (consecutiveFailures 초과)│                        │
│  │    └─▶ 컨테이너 Kill → 재시작   │                        │
│  └────────────────────────────────┘                       │
│                                                           │
│  ┌─ Readiness Probe (주기적 실행) ─┐                        │
│  │  성공 → Service 엔드포인트 등록  │                        │
│  │  실패 → Service 엔드포인트 제거  │                        │
│  │  (컨테이너 Kill 안 함, 운영 계속) │                        │
│  └─────────────────────────────────┘                      │
│                                                           │
│  Probe 방식: HTTP GET / TCP Socket / EXEC 명령             │
└───────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Liveness와 Readiness Probe는 목적이 다르다. Liveness는 "컨테이너가 살아서 제 기능을 하는가"를 확인하며 실패 시 재시작(kill & restart)을 트리거한다. Readiness는 "서비스 트래픽을 받을 준비가 됐는가"를 확인하며 실패 시 Service 엔드포인트에서만 제거하고 컨테이너는 살려둔다(재시작 없음). 이 구분이 중요한 이유는 초기화 중인 앱이나 일시적으로 과부하 상태인 앱에서 Liveness 실패로 재시작이 무한 반복(CrashLoopBackOff)되는 것을 Readiness 전략으로 방지할 수 있기 때문이다.

- **📢 섹션 요약 비유**: Liveness는 "직원이 살아있나?" 체크(사망 시 대체 채용=재시작), Readiness는 "직원이 지금 손님 응대 가능한 상태인가?" 체크(준비 안 된 직원은 손님 배정에서 빼지만 해고는 안 함)입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### CrashLoopBackOff 원인 및 Probe 설정 트레이드오프

| 상황 | Probe 미설정 시 문제 | 적절한 Probe 설정 효과 |
|:---|:---|:---|
| 앱 기동에 60초 소요 | Liveness 실패→재시작→다시 60초→무한 반복 | Startup Probe로 60초 유예→정상 기동 후 Liveness 시작 |
| DB 연결 순간 일시 불가 | Liveness 실패→불필요한 재시작→연결 끊김 더 악화 | Readiness 실패→엔드포인트 제거→재연결 후 자동 복귀 |
| OOM 크래시 반복 | 재시작마다 메모리 증가→노드 전체 불안정 | Liveness + 메모리 Limit 조합→임계치 초과 시 재시작·재스케줄링 |

```text
┌───────────────────────────────────────────────────────────┐
│     Kubelet이 관리하는 CRI·CNI·CSI 인터페이스 연동 구조      │
├───────────────────────────────────────────────────────────┤
│                                                           │
│           Kubelet                                         │
│           │                                               │
│     ┌─────┼─────────────────┐                            │
│     │     │                 │                            │
│     ▼     ▼                 ▼                            │
│   CRI    CNI              CSI                            │
│ (컨테이너) (네트워크)     (스토리지)                         │
│     │     │                 │                            │
│     ▼     ▼                 ▼                            │
│ containerd  Calico/Flannel  EBS/NFS CSI Driver            │
│ CRI-O       Cilium          Ceph RBD                      │
│                                                           │
│  CRI: grpc로 Pod 생성·삭제·상태 조회 표준화                   │
│  CNI: Pod IP 할당 및 네트워크 플러그인 연동                   │
│  CSI: PersistentVolume 프로비저닝 및 마운트                  │
└───────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Kubelet은 gRPC 기반의 세 가지 표준 인터페이스를 통해 컨테이너 런타임(CRI), 네트워크(CNI), 스토리지(CSI)와 통신한다. 이 추상화 계층 덕분에 쿠버네티스는 특정 벤더 종속(Lock-in) 없이 containerd, CRI-O 등 다양한 런타임과 Calico, Flannel, Cilium 등 다양한 네트워크 솔루션을 플러그인 방식으로 교체 가능하다.

- **📢 섹션 요약 비유**: Kubelet은 범용 리모컨(표준 인터페이스)으로 TV(CRI), 에어컨(CNI), 조명(CSI) 등 어느 브랜드 제품이든 제어하는 스마트홈 허브와 같습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오
1. **시나리오 — CrashLoopBackOff로 Pod 계속 죽음**: 앱 초기화에 90초가 걸리는 신규 서비스를 배포했는데 Liveness Probe가 30초 후 실패해 재시작 루프.
   - **판단**: `startupProbe`를 설정하여 `failureThreshold * periodSeconds = 120초` 동안 Liveness 유예. 초기화 완료 신호(HTTP /health 200 반환) 후 Liveness 체크 시작.
2. **시나리오 — 노드 NotReady 상태로 Pod 전부 Terminating**: 네트워크 순단으로 kubelet → API Server 연결 5분 이상 끊기자 node.kubernetes.io/not-ready Taint 자동 적용, 해당 노드 Pod 전체 재스케줄링.
   - **판단**: `--node-status-update-frequency`와 `node-monitor-grace-period` 파라미터를 네트워크 환경에 맞게 튜닝하고, 중요 Pod는 PodDisruptionBudget(PDB)으로 재스케줄링 중 최소 가용 수를 보장해야 한다.

### 도입 체크리스트
- **기술적**: 모든 프로덕션 Pod에 Liveness와 Readiness Probe가 적절히 설정되어 있는가? 설정 없이 배포하면 앱 크래시 시 Kubelet이 상태를 알 수 없어 트래픽이 죽은 Pod로 계속 전달된다.
- **운영적**: Kubelet 버전과 API Server 버전 사이에 최대 2개 마이너 버전 차이(Skew Policy)를 유지하고 있는가?

### 안티패턴
- **Probe 미설정 배포**: Readiness Probe 없으면 컨테이너 기동 직후(앱 초기화 전) 트래픽이 유입되어 500 에러 폭발. "배포 성공"했는데 고객은 에러를 경험하는 최악의 상황.

- **📢 섹션 요약 비유**: 신규 직원(컨테이너)이 업무 교육(초기화)을 마치기도 전에 고객 전화를 연결하는 것(Readiness Probe 미설정)과 같습니다. 교육 완료 신호를 받은 후에 고객을 연결해야 합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | Probe 미설정 | Kubelet Probe 적절 설정 시 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 앱 크래시 감지 수 분 소요, 수동 재시작 | 30초 이내 자동 감지·재시작 | 장애 복구 시간 **95% 단축** |
| **정성** | 노드 이상 시 수동 워크로드 이전 | Kubelet 보고→Controller 자동 재스케줄링 | 야간 장애 무인 자동 복구 가능 |

### 미래 전망
- **eBPF 기반 Kubelet 강화**: Cilium + eBPF로 Kubelet 네트워크 정책과 모니터링이 커널 수준에서 처리되어 오버헤드가 줄고 관찰 가능성(Observability)이 극대화되는 방향으로 진화 중이다.

### 참고 표준
- **Kubernetes CRI 스펙 (kubernetes/cri-api)**: gRPC 기반 컨테이너 런타임 인터페이스 공개 스펙.

- **📢 섹션 요약 비유**: Kubelet의 Probe 시스템은 공장의 자동 품질 검사 라인처럼, 불량품(비정상 컨테이너)을 사람 개입 없이 자동으로 걸러내고 정상 제품(정상 컨테이너)만 포장(트래픽 수신) 단계로 넘기는 자동화 품질 게이트입니다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

- **API Server** | Kubelet이 PodSpec을 구독하고 상태를 보고하는 쿠버네티스 제어 평면의 중앙 허브.
- **Pod (포드)** | Kubelet이 실제로 생성·관리하는 쿠버네티스 최소 배포 단위.
- **CRI (Container Runtime Interface)** | Kubelet과 containerd·CRI-O를 연결하는 gRPC 표준 인터페이스.
- **Self-Healing** | Probe 실패 시 컨테이너 자동 재시작·재스케줄링 메커니즘. Kubelet이 핵심 구현체.
- **PodDisruptionBudget (PDB)** | Kubelet이 유발하는 재스케줄링 과정에서 최소 가용 Pod 수를 보장하는 정책.

---

## 👶 어린이를 위한 3줄 비유 설명
1. 쿠버네티스는 수천 개의 공장(서버)을 지휘하는 거대한 공장 회사인데, 각 공장마다 **공장 관리자(Kubelet)**가 있어요.
2. 본사(API Server)가 "A공장에 로봇 3대 설치해"라고 보내면, Kubelet이 직접 로봇(컨테이너)을 설치하고 매시간 "잘 작동하고 있습니다"라고 보고해요.
3. 로봇이 갑자기 고장나면 Kubelet이 즉시 알아채고 새 로봇으로 자동 교체해주니까, 사람이 밤새 공장을 지키지 않아도 된답니다.
