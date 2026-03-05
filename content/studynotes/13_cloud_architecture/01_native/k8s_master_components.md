+++
title = "쿠버네티스 마스터 노드 컴포넌트"
date = 2026-03-05
description = "쿠버네티스 컨트롤 플레인의 핵심 구성요소인 API Server, etcd, Scheduler, Controller Manager의 아키텍처, 통신 메커니즘 및 고가용성 구성 심층 분석"
weight = 76
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Kubernetes", "Control-Plane", "API-Server", "etcd", "Scheduler", "Controller-Manager"]
+++

# 쿠버네티스 마스터 노드 컴포넌트 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 쿠버네티스 마스터 노드는 API Server(중앙 게이트웨이), etcd(분산 상태 저장소), Scheduler(파드 배치 결정), Controller Manager(상태 일치 제어)로 구성되며, 이들은 선언적 API를 통해 클러스터의 '원하는 상태'를 '현재 상태'로 수렴시키는 제어 평면(Control Plane)을 형성합니다.
> 2. **가치**: 고가용성(HA) 구성에서 **99.99% 가용성**을 달성하며, 수천 개의 노드와 수만 개의 파드를 **초당 5,000+ API 요청** 처리량으로 관리할 수 있습니다.
> 3. **융합**: Raft 합의 알고리즘(etcd), 워치 메커니즘(Informer), 낙관적 동시성 제어(Resource Version) 등 분산 시스템 이론이 통합되어 있으며, GitOps 및 IaC와 결합하여 현대적 인프라의 뇌(Brain) 역할을 수행합니다.

---

## Ⅰ. 개요 (Context & Background)

쿠버네티스 마스터 노드는 클러스터 전체의 '두뇌' 역할을 수행하는 컨트롤 플레인(Control Plane)의 물리적/논리적 구현체입니다. 사용자가 `kubectl apply -f deployment.yaml` 명령을 내리면, 마스터 노드의 컴포넌트들이 협력하여 YAML에 선언된 상태를 실제 워커 노드에서 구현합니다. 이 과정은 완전히 자동화되어 있으며, '원하는 상태(Desired State)'와 '현재 상태(Current State)'의 차이를 지속적으로 감지하고 수정하는 제어 루프(Control Loop)를 기반으로 합니다.

**💡 비유**: 쿠버네티스 마스터 노드는 **'자율주행 자동차의 중앙 컴퓨터'**와 같습니다. 운전자가 "서울역으로 가줘"라고 목적지(Desired State)만 말하면, 중앙 컴퓨터가 GPS(etcd)로 현재 위치를 확인하고, 내비게이션(Scheduler)이 최적 경로를 계산하며, 엔진/브레이크 컨트롤러(Controller Manager)가 실제 주행을 제어합니다. 운전자는 핸들을 잡을 필요가 없습니다.

**등장 배경 및 발전 과정**:
1. **Borg의 유산**: 구글의 내부 시스템 Borg는 수만 대의 서버를 관리하기 위해 중앙 집중식 마스터 아키텍처를 개발했습니다. 쿠버네티스는 이 경험을 오픈소스로 재구현한 것입니다.
2. **API 중심 설계**: 쿠버네티스는 모든 기능이 RESTful API로 노출되는 'API First' 철학을 따릅니다. 이는 kubectl뿐만 아니라 CI/CD 파이프라인, 모니터링 시스템, 서드파티 도구들이 동일한 API를 통해 클러스터를 제어할 수 있게 합니다.
3. **모듈화와 확장성**: 각 컴포넌트는 독립적으로 배포 및 스케일링될 수 있으며, CRD(Custom Resource Definition)와 Aggregation Layer를 통해 서드파티 컨트롤러를 마스터 노드에 통합할 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 마스터 노드 컴포넌트 상세 분석표

| 컴포넌트 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
|---|---|---|---|---|
| **kube-apiserver** | 모든 통신의 중앙 허브. 인증/인가/승인 제어 수행 | Filter Chain 구조로 요청 처리. Watch 기반 실시간 알림 | REST, gRPC, Webhook | 호텔 프론트 데스크 |
| **etcd** | 클러스터 상태의 유일한 진실 공급원(SoT) | Raft 합의 알고리즘으로 분기 일관성 보장. MVCC 지원 | Raft, gRPC, BoltDB | 중앙 금고 |
| **kube-scheduler** | 신규 파드를 최적 노드에 바인딩 | Predicate(필터링) → Priority(스코어링) 2단계 알고리즘 | Scheduling Framework | 배차 관리자 |
| **controller-manager** | 다양한 컨트롤러를 단일 프로세스로 실행 | Informer 패턴으로 이벤트 구독, Reconcile 루프 수행 | Workqueue, RateLimiting | 감시관 그룹 |
| **cloud-controller-manager** | 클라우드별 컨트롤러 분리 (옵션) | CSI/CNI/CCM 인터페이스로 클라우드 API 추상화 | AWS/Azure/GCP SDK | 클라우드 통역사 |

### 정교한 구조 다이어그램: 컨트롤 플레인 내부 통신

```ascii
================================================================================
                    KUBERNETES CONTROL PLANE (HA 구성)
================================================================================

    +------------------+                    +------------------+
    |   kubectl /     |                    |   CI/CD /       |
    |   kubectl proxy |                    |   GitOps Agent  |
    +--------+---------+                    +--------+--------+
             |                                       |
             | HTTPS (443)                           | HTTPS
             v                                       v
+------------+---------------------------------------+-------------+
|                        Load Balancer                             |
|                     (HAProxy / kube-vip)                        |
+------------+----------------+----------------+-----------------+
             |                |                |
    +--------v------+  +------v-------+ +------v--------+
    | API Server #1 |  | API Server #2| | API Server #3 |  <-- Active-Active
    +-------+-------+  +------+-------+ +-------+-------+
            |                 |                  |
            +-----------------+------------------+
                              |
                     gRPC (2379-2380)
                              |
            +-----------------+------------------+
            |                 |                  |
    +-------v------+  +-------v------+  +-------v-------+
    |  etcd #1     |  |  etcd #2     |  |  etcd #3      |  <-- Raft Quorum
    |  (Leader)    |  | (Follower)   |  | (Follower)    |
    +--------------+  +--------------+  +---------------+

    +----------------+  +----------------+  +----------------+
    |   Scheduler    |  | Controller Mgr |  | Cloud Ctrl Mgr |
    |   (Leader Elect)|  | (Leader Elect) |  | (Leader Elect) |
    +-------+--------+  +-------+--------+  +-------+--------+
            |                   |                   |
            | Watch API (List)  | Reconcile Loop    |
            +-------------------+-------------------+
                                |
                    +-----------v-----------+
                    |    API Server (via    |
                    |    Loopback/Service)  |
                    +-----------------------+

================================================================================
                         COMMUNICATION FLOW
================================================================================
1. Client Request --> LB --> API Server (AuthN/AuthZ/Admission)
2. API Server --> etcd (Persist State)
3. Controller Manager --> Watch API --> Reconcile --> Update API
4. Scheduler --> Watch Pending Pods --> Bind Node --> Update API
5. All reads/writes go through API Server (etcd 직접 접근 금지)
```

### 심층 동작 원리: API Server 요청 처리 파이프라인

API Server는 들어오는 모든 요청을 Filter Chain 구조로 처리합니다. 각 단계는 독립적이며 플러그인으로 확장 가능합니다.

1. **Authentication (인증)**: 요청자의 신원을 확인합니다. X.509 인증서, ServiceAccount Token, OIDC, Webhook 등 다양한 방식을 지원합니다.
   ```
   User: system:anonymous --> Authentication --> User: alice (cert: CN=alice)
   ```

2. **Authorization (인가)**: 인증된 사용자가 요청한 리소스에 접근 권한이 있는지 확인합니다. RBAC, ABAC, Node Authorizer, Webhook 등이 있습니다.
   ```
   User: alice, Verb: create, Resource: pods, Namespace: prod
   --> RBAC: RoleBinding "dev-role" exists? --> ALLOW
   ```

3. **Admission Control (승인 제어)**: 요청의 세부 내용을 검증/변환합니다. mutating(변형)과 validating(검증) 두 단계로 나뉩니다.
   - **Mutating**: Default StorageClass 주입, PodSecurityContext 설정, Image Registry Override
   - **Validating**: ResourceQuota 확인, PodSecurity Standards 검증, Custom Policy(OPA/Gatekeeper)

4. **ETCD Persistence**: 모든 승인을 통과한 요청은 etcd에 원자적으로 기록됩니다. 낙관적 동시성 제어를 위해 ResourceVersion이 사용됩니다.

5. **Watch Notification**: etcd에 기록된 변경 사항은 Watch API를 구독 중인 모든 컴포넌트에게 브로드캐스트됩니다.

### 핵심 코드: Controller Manager의 Reconcile 루프

```go
// K8s Controller Manager의 핵심 Reconcile 패턴 (workqueue 기반)
// 참조: k8s.io/client-go/tools/cache/controller.go

type Controller struct {
    indexer      cache.Indexer      // 로컬 캐시 (Informer)
    queue        workqueue.RateLimitingInterface  // 작업 큐
    informer     cache.Controller   // 이벤트 구독기
}

func (c *Controller) Run(workers int, stopCh <-chan struct{}) {
    // 1. Informer 시작 (Watch API Server)
    go c.informer.Run(stopCh)

    // 2. 캐시 동기화 대기
    if !cache.WaitForCacheSync(stopCh, c.informer.HasSynced) {
        runtime.HandleError(fmt.Errorf("timed out waiting for caches to sync"))
        return
    }

    // 3. 워커 고루틴 기동
    for i := 0; i < workers; i++ {
        go wait.Until(c.runWorker, time.Second, stopCh)
    }
}

func (c *Controller) runWorker() {
    for c.processNextItem() {
    }
}

func (c *Controller) processNextItem() bool {
    // 1. 큐에서 아이템 가져오기
    key, quit := c.queue.Get()
    if quit {
        return false
    }
    defer c.queue.Done(key)

    // 2. 비즈니스 로직 실행 (Reconcile)
    err := c.syncToStdout(key.(string))

    // 3. 에러 처리 및 재시도
    if err != nil {
        c.handleErr(err, key)
        return true
    }

    // 4. 큐에서 아이템 제거
    c.queue.Forget(key)
    return true
}

func (c *Controller) syncToStdout(key string) error {
    // 로컬 캐시에서 객체 조회 (API Server 호출 없음)
    obj, exists, err := c.indexer.GetByKey(key)
    if err != nil {
        return err
    }

    if !exists {
        // 객체가 삭제됨 -> Clean-up 로직
        fmt.Printf("Pod %s has been deleted\n", key)
    } else {
        // 객체가 생성/수정됨 -> Reconcile 로직
        pod := obj.(*v1.Pod)
        fmt.Printf("Sync/Add/Update for Pod %s in namespace %s\n",
                   pod.Name, pod.Namespace)
    }
    return nil
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 고가용성 구성 전략

| 구성 요소 | 단일 마스터 | HA (Stacked etcd) | HA (External etcd) |
|---|---|---|---|
| **API Server** | 1개 | 3개 (Active-Active) | 3개 (Active-Active) |
| **etcd** | 1개 (동일 노드) | 3개 (동일 노드) | 3개 (별도 노드) |
| **Scheduler** | 1개 | 3개 (Leader Election) | 3개 (Leader Election) |
| **Controller Mgr** | 1개 | 3개 (Leader Election) | 3개 (Leader Election) |
| **노드 수** | 1 | 3 | 6 (3 Control + 3 etcd) |
| **장애 허용** | 0대 | 1대 | 2대 (etcd 별도) |
| **복잡도** | 낮음 | 중간 | 높음 |
| **권장 환경** | 개발/테스트 | 프로덕션 | 대규모 엔터프라이즈 |

### etcd Raft 합의 알고리즘 상세 분석

etcd는 Raft 알고리즘을 기반으로 분산 일관성을 보장합니다. 주요 특징은 다음과 같습니다.

1. **Leader Election**: etcd 클러스터는 항상 하나의 Leader만 존재합니다. Leader는 하트비트(Heartbeat)를 Follower에게 전송하며, Leader가 다운되면 남은 노드들이 과반수(Quorum)로 새 Leader를 선출합니다.

2. **Log Replication**: 모든 쓰기 요청은 Leader를 통해서만 처리됩니다. Leader는 요청을 로그에 기록하고, 과반수의 Follower가 확인(ACK)하면 커밋합니다.

3. **Linearizable Read**: 일관성 있는 읽기를 위해 Leader는 읽기 요청 시 Quorum 확인(ReadIndex)을 수행하거나 Lease 기반의 Serializable Read를 제공합니다.

```ascii
       Client Write Request
              |
              v
    +------------------+
    |    Leader        |  1. Append to local log
    |    etcd-0        |  2. Replicate to Followers
    +--------+---------+
             |
    +--------+--------+--------+
    |                 |        |
    v                 v        v
+-------+        +-------+  +-------+
|Follower|       |Follower| |Follower|
|etcd-1  |       |etcd-2  | |etcd-3  |
+---+---+        +---+---+  +---+---+
    |                |          |
    +---- ACK -------+--- ACK --+
             |
             v
    Leader commits & responds to Client
```

### 과목 융합 관점 분석: 데이터베이스 및 네트워크 연계

- **데이터베이스(DB)와의 융합**: etcd는 **MVCC(Multi-Version Concurrency Control)**를 지원하여 스냅샷 격리(Snapshot Isolation)를 제공합니다. 이는 동시 읽기/쓰기가 빈번한 K8s 환경에서 Lock 없이 높은 처리량을 가능하게 합니다. 또한 압축(Compaction)과 디플래그레이션(Defragmentation)을 통해 디스크 공간을 관리합니다.

- **네트워크(Network)와의 융합**: API Server는 **TLS 1.3** 기반의 양방향 인증(mTLS)을 사용하며, Service Mesh와 결합 시 Control Plane 통신도 mTLS로 암호화됩니다. 또한 kubectl proxy와 apiserver proxy는 HTTP/2를 통해 멀티플렉싱된 Watch 연결을 최적화합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 대규모 클러스터의 API Server 병목 해결

**문제 상황**: 1,000개 노드, 30,000개 파드를 운영 중인 클러스터에서 API Server의 CPU 사용률이 95%를 상회하며, `kubectl get pods` 명령이 30초 이상 소요됩니다.

**기술사의 전략적 의사결정**:

1. **API Server 수평 확장**: API Server를 3개에서 5개로 확장하고 Load Balancer를 통해 트래픽을 분산합니다.

2. **Watch 캐시 최적화**: `--watch-cache-sizes` 설정을 조정하여 메모리 내 캐시 크기를 늘립니다.
   ```bash
   kube-apiserver --watch-cache-sizes=deployments.apps#1000,pods#50000
   ```

3. **etcd 튜닝**: etcd의 `--quota-backend-bytes`를 8GB에서 16GB로 증설하고, `--snapshot-count`를 10000에서 50000으로 조정합니다.

4. **Admission Webhook 최적화**: 느린 Webhook(Mutating/Validating)을 비동기화하거나 캐싱합니다.

5. **클라이언트 측 최적화**: `kubectl`의 `--watch` 대신 Informer 캐시를 사용하도록 애플리케이션을 수정합니다.

### 도입 시 고려사항 체크리스트

- **기술적 고려사항**:
  - [ ] etcd 백업 스케줄 설정 (최소 1시간 간격)
  - [ ] API Server 인증서 갱신 자동화 (cert-manager)
  - [ ] 감사 로그(Audit Log) 활성화 및 외부 SIEM 연동
  - [ ] Aggregation Layer 설정 (metrics-server 등)

- **운영/보안적 고려사항**:
  - [ ] RBAC 최소 권한 원칙 적용
  - [ ] Pod Security Standards (PSS) Admission 활성화
  - [ ] Control Plane 노드의 전용 리소스 격리 (Taint/Toleration)
  - [ ] etcd 암호화 (Encryption at Rest)

### 안티패턴 (Anti-patterns)

1. **단일 마스터로 프로덕션 운영**: 컨트롤 플레인 장애 시 전체 클러스터가 마비됩니다. 최소 3노드 HA 구성이 필수입니다.

2. **etcd 직접 접근**: API Server를 우회하여 etcd에 직접 쓰기를 수행하면 데이터 무결성이 깨집니다. 모든 상태 변경은 반드시 API Server를 통해야 합니다.

3. **무제한 Watch**: 전체 네임스페이스의 모든 리소스를 Watch하는 컨트롤러는 API Server에 과부하를 줍니다. Label Selector와 Field Selector로 범위를 제한해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 단일 마스터 | 3노드 HA | 5노드 HA + 튜닝 |
|---|---|---|---|
| **API 응답 시간 (P99)** | 500ms | 100ms | 30ms |
| **처리량 (TPS)** | 500 | 2,000 | 10,000 |
| **가용성 (SLA)** | 99% | 99.9% | 99.99% |
| **장애 복구 시간 (RTO)** | 수동 | 30초 | 10초 |
| **노드 수용력** | 100대 | 500대 | 5,000대 |

### 미래 전망 및 진화 방향

1. **Kubernetes API Server의 Serverless화**: AWS EKS on Fargate와 같이 사용자가 컨트롤 플레인을 전혀 관리하지 않는 Serverless Kubernetes가 확산되고 있습니다.

2. **Multi-Cluster Control Plane**: KCP(Kubernetes Control Plane)와 같은 프로젝트는 단일 컨트롤 플레인으로 여러 클러스터를 관리하는 '메타 컨트롤 플레인' 개념을 도입하고 있습니다.

3. **Declarative API의 표준화**: Kubernetes API 패턴이 Gateway API, Cluster API 등으로 확장되며, 인프라 전체를 선언적으로 관리하는 표준으로 자리잡고 있습니다.

### ※ 참고 표준/가이드

- **CIS Kubernetes Benchmark**: 컨트롤 플레인 보안 설정 표준
- **CNCF Conformance**: Kubernetes 호환성 인증 프로그램
- **NIST SP 800-204**: 컨테이너 오케스트레이션 보안 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [쿠버네티스 (Kubernetes)](@/studynotes/13_cloud_architecture/01_native/kubernetes.md) : 마스터 노드가 제어하는 전체 오케스트레이션 플랫폼
- [etcd 분산 저장소](@/studynotes/13_cloud_architecture/01_native/kubernetes.md) : Raft 기반의 고가용성 키-값 저장소
- [워커 노드 컴포넌트](@/studynotes/13_cloud_architecture/01_native/kubernetes.md) : Kubelet, Kube-proxy, Container Runtime
- [RBAC 권한 통제](@/studynotes/13_cloud_architecture/01_native/kubernetes.md) : API Server 인가 메커니즘
- [GitOps 배포](@/studynotes/13_cloud_architecture/01_native/ci_cd.md) : 선언적 API를 활용한 배포 자동화

---

### 👶 어린이를 위한 3줄 비유 설명
1. 쿠버네티스 마스터 노드는 **'학교의 교무실'**과 같아요. 교장 선생님(Scheduler)이 어떤 반에 학생을 배정할지 결정하고, 담임 선생님(Controller)이 학생들이 제자리에 있는지 확인해요.
2. 성적부(etcd)에는 모든 학생의 정보가 적혀 있고, 선생님들은 이 성적부를 보고 학생들을 관리해요.
3. 교무실(마스터 노드)이 휴일에도 일하면, 학교(클러스터) 전체가 문제없이 돌아가요!
