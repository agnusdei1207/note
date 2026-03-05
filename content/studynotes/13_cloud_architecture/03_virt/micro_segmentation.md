+++
title = "마이크로 세그멘테이션 (Micro-Segmentation)"
date = 2024-05-18
description = "VM 또는 컨테이너 Pod 단위로 방화벽 룰을 세밀하게 적용하여 동서 트래픽 횡적 이동 차단하는 제로 트러스트 보안 기법"
weight = 60
[taxonomies]
categories = ["studynotes-13_cloud_architecture"]
tags = ["Micro-Segmentation", "Zero Trust", "East-West Traffic", "Network Security", "NSX", "Illumio"]
+++

# 마이크로 세그멘테이션 (Micro-Segmentation)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 마이크로 세그멘테이션은 데이터센터 내부의 동서(East-West) 트래픽을 워크로드(VM, 컨테이너, Pod) 단위까지 세분화하여 격리하고, 최소 권한 원칙(Least Privilege)에 따라 허용된 통신만 허용하는 제로 트러스트 네트워크 보안 아키텍처입니다.
> 2. **가치**: 랜섬웨어, APT 공격 시 횡적 이동(Lateral Movement)을 90% 이상 차단, 공격 표면(Attack Surface) 최소화, 규제 준수(GDPR, PCI-DSS) 용이, 보안 사고 시 피해 범위 국소화를 실현합니다.
> 3. **융합**: SDN(Software Defined Networking), 서비스 메시(Istio), 제로 트러스트(ZTA), 클라우드 네이티브 보안, 컨테이너 보안과 결합하여 현대적 디펜시블 아키텍처(Zero Trust Architecture)를 구현합니다.

---

## Ⅰ. 개요 (Context & Background)

마이크로 세그멘테이션은 기존 경계 기반 보안(Perimeter Security)의 한계를 극복하기 위해 등장했습니다. 전통적인 방화벽은 데이터센터 외부와 내부의 경계(남북 트래픽)만 보호했으나, 내부 침입 후 공격자의 횡적 이동은 막지 못했습니다. 마이크로 세그멘테이션은 모든 워크로드 간 통신을 기본 차단(Deny All)하고, 필요한 통신만 허용(Allow)하여 내부 공격을 원천 차단합니다.

**💡 비유**: 마이크로 세그멘테이션은 **'호텔 객실 보안 시스템'**과 같습니다. 기존 방화벽은 호텔 로비(경계)에서만 출입을 통제했으나, 로비를 통과하면 모든 객실에 자유롭게 출입할 수 있었습니다. 마이크로 세그멘테이션은 각 객실(워크로드)마다 개별 키카드(방화벽 규칙)가 필요합니다. 101호 투숙객은 102호, 201호에 들어갈 수 없습니다. 어떤 투숙객이 문제를 일으켜도 다른 객실에는 영향이 없습니다.

**등장 배경 및 발전 과정**:
1. **경계 보안의 붕괴**: APT, 내부자 위협, 서비스 데스크 피싱으로 내부 침입 증가.
2. **횡적 이동의 위험**: 공격자가 한 서버 침입 후 DB, 관리 서버로 이동하는 공격 빈발.
3. **VMware NSX 출시 (2013)**: 분산 방화벽(Distributed Firewall)으로 VM 단위 격리 실현.
4. **Illumio, Guardicore 등장**: 에이전트 기반 마이크로 세그멘테이션 솔루션.
5. **제로 트러스트 표준화**: NIST SP 800-207 (2020)에서 핵심 요소로 명시.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 마이크로 세그멘테이션 구현 방식 (표)

| 구현 방식 | 상세 설명 | 장점 | 단점 | 대표 제품 |
|---|---|---|---|---|
| **네트워크 기반 (SDN)** | 하이퍼바이저 vSwitch에 규칙 삽입 | 성능 우수, 에이전트 불필요 | 가상화 환경만 지원 | VMware NSX, Cisco ACI |
| **에이전트 기반** | OS에 소프트웨어 에이전트 설치 | 물리/가상/클라우드 모두 지원 | 오버헤드, 관리 복잡 | Illumio, Guardicore |
| **컨테이너/CNI 기반** | Kubernetes Network Policy | 클라우드 네이티브, 동적 | 컨테이너만 지원 | Calico, Cilium |
| **서비스 메시 기반** | 사이드카 프록시에서 L7 필터링 | 트래픽 가시성, mTLS | 복잡성, 오버헤드 | Istio, Linkerd |

### 마이크로 세그멘테이션 정책 요소 (표)

| 정책 요소 | 설명 | 예시 |
|---|---|---|
| **Source (출발지)** | 통신을 시작하는 워크로드 그룹 | Web-Tier VMs |
| **Destination (목적지)** | 통신을 받는 워크로드 그룹 | DB-Tier VMs |
| **Service (서비스)** | 프로토콜/포트 | TCP/3306 (MySQL) |
| **Action (액션)** | 허용/차단/로그 | Allow |
| **Context (컨텍스트)** | 추가 조건 (시간, 인증) | Business Hours Only |

### 정교한 마이크로 세그멘테이션 아키텍처 다이어그램

```ascii
+===========================================================================+
|                    Micro-Segmentation Architecture                        |
|                                                                           |
|  [Traditional Perimeter Security - ONLY North-South Protection]          |
|  +--------------------------------------------------------------------+  |
|  |                      External Firewall                             |  |
|  |                    (North-South Traffic)                          |  |
|  +------------------------------+-------------------------------------+  |
|                                 |                                        |
|  +------------------------------v-------------------------------------+  |
|  |                      Internal Network                              |  |
|  |                                                                    |  |
|  |   +--------+    +--------+    +--------+    +--------+            |  |
|  |   | Web    |    | App    |    | DB     |    | Admin  |            |  |
|  |   | Server |<-->| Server |<-->| Server |<-->| Server |            |  |
|  |   +--------+    +--------+    +--------+    +--------+            |  |
|  |        ^            ^             ^             ^                  |  |
|  |        +------------+-------------+-------------+                  |  |
|  |              ALL Internal Traffic ALLOWED!                        |  |
|  |         (Attacker can move Laterally after breach)                |  |
|  +--------------------------------------------------------------------+  |
|                                                                           |
+===========================================================================+

+===========================================================================+
|              [Micro-Segmentation - East-West Protection]                  |
|                                                                           |
|  +--------+                    +--------+                    +--------+  |
|  | Web    |                    | App    |                    | DB     |  |
|  | Server |                    | Server |                    | Server |  |
|  | +----+ |    Allow:8080      | +----+ |    Allow:3306     | +----+ |  |
|  | | DFW| |<------------------>| | DFW| |<----------------->| | DFW| |  |
|  | +----+ |                    | +----+ |                   | +----+ |  |
|  +---+----+                    +---+----+                   +---+----+  |
|      |                             |                            |       |
|      |  Deny All                   |  Deny All                  |Deny   |
|      |  (Web cannot talk to DB)    |  (App cannot talk to Admin)|All    |
|      v                             v                            v       |
|  +---+----+                    +---+----+                   +---+----+  |
|  | Admin  |                    | Log    |                   | Backup |  |
|  | Server |                    | Server |                   | Server |  |
|  | +----+ |                    | +----+ |                   | +----+ |  |
|  | | DFW| |                    | | DFW| |                   | | DFW| |  |
|  | +----+ |                    | +----+ |                   | +----+ |  |
|  +--------+                    +--------+                   +--------+  |
|                                                                           |
|  [Security Groups / Tags]                                                 |
|  +--------------------------------------------------------------------+  |
|  |  SG-Web: 10.0.1.0/24, Tag: App=Web                                |  |
|  |  SG-App: 10.0.2.0/24, Tag: App=API                                |  |
|  |  SG-DB:  10.0.3.0/24, Tag: App=Database                           |  |
|  +--------------------------------------------------------------------+  |
|                                                                           |
|  [Micro-Segmentation Rules]                                               |
|  +--------------------------------------------------------------------+  |
|  | Rule 1: SG-Web -> SG-App (TCP/8080) = ALLOW                       |  |
|  | Rule 2: SG-App -> SG-DB (TCP/3306) = ALLOW                        |  |
|  | Rule 3: SG-Admin -> SG-All (TCP/22) = ALLOW (with MFA)            |  |
|  | Rule 4: Any -> Any = DENY (Default)                               |  |
|  +--------------------------------------------------------------------+  |
+===========================================================================+

[Attack Scenario Comparison]
+---------------------------------------------------------------------------+
| Traditional:                                                              |
| Attacker compromises Web Server -> Access App Server -> Exfiltrate DB     |
| (No internal barriers)                                                    |
+---------------------------------------------------------------------------+
| Micro-Segmentation:                                                       |
| Attacker compromises Web Server -> Cannot access DB (blocked by DFW)     |
| (Lateral movement blocked)                                                |
+---------------------------------------------------------------------------+
```

### 심층 동작 원리: NSX 분산 방화벽 (Distributed Firewall)

1. **워크로드 태깅 (Workload Tagging)**:
   - VM 생성 시 vCenter/NSX에 의해 자동 태그 할당
   - 태그 예: App=Web, Env=Prod, Owner=TeamA
   - IP 주소가 변경되어도 태그 기반 정책 유지

2. **정책 정의 (Policy Definition)**:
   - 관리자가 보안 그룹 간 통신 규칙 정의
   - 선언형(Declarative) 정책: "Web은 App의 8080만 접근"
   - 정책은 NSX Manager에서 중앙 관리

3. **정책 배포 (Policy Distribution)**:
   - NSX Manager가 모든 ESXi 호스트에 정책 푸시
   - 각 호스트의 vSwitch(DFW 모듈)가 정책 저장
   - 분산 처리: 각 호스트가 로컬에서 필터링

4. **패킷 필터링 (Packet Filtering)**:
   - VM 송신/수신 시 vSwitch에서 규칙 평가
   - 5-tuple (Src IP, Dst IP, Src Port, Dst Port, Protocol) 매칭
   - 매칭되는 규칙 없으면 Default Deny 적용

5. **로그 및 감사 (Logging & Audit)**:
   - 차단/허용된 연결에 대한 로그 생성
   - SIEM(Splunk, QRadar)으로 전송
   - 규정 준수 감사 추적 제공

### 핵심 코드: Kubernetes Network Policy (Calico)

```yaml
# Kubernetes Network Policy: 마이크로 세그멘테이션
# 네임스페이스: production
# 목표: 웹->앱->DB 계층만 통신 허용, 나머지 차단

---
# 1. 웹 계층: 외부 인그레스만 허용, 아웃그레스는 앱 계층만
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-tier-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      tier: web
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # 외부 로드밸런서에서만 접근 허용
    - from:
        - ipBlock:
            cidr: 10.0.0.0/8  # 내부 네트워크
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080
        - protocol: TCP
          port: 8443
  egress:
    # 앱 계층의 8080 포트로만 아웃그레스 허용
    - to:
        - podSelector:
            matchLabels:
              tier: app
      ports:
        - protocol: TCP
          port: 8080
    # DNS 조회 허용
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: UDP
          port: 53

---
# 2. 앱 계층: 웹에서 인그레스, DB로 아웃그레스
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-tier-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      tier: app
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # 웹 계층에서만 접근 허용
    - from:
        - podSelector:
            matchLabels:
              tier: web
      ports:
        - protocol: TCP
          port: 8080
  egress:
    # DB 계층의 MySQL 포트로만 아웃그레스 허용
    - to:
        - podSelector:
            matchLabels:
              tier: database
      ports:
        - protocol: TCP
          port: 3306
        - protocol: TCP
          port: 5432  # PostgreSQL
    # Redis 캐시
    - to:
        - podSelector:
            matchLabels:
              tier: cache
      ports:
        - protocol: TCP
          port: 6379
    # DNS
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: UDP
          port: 53

---
# 3. DB 계층: 앱에서만 인그레스, 아웃그레스는 금지
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: database-tier-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      tier: database
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # 앱 계층에서만 접근 허용
    - from:
        - podSelector:
            matchLabels:
              tier: app
      ports:
        - protocol: TCP
          port: 3306
        - protocol: TCP
          port: 5432
    # 백업 서버 (특정 IP만)
    - from:
        - ipBlock:
            cidr: 10.100.50.100/32
      ports:
        - protocol: TCP
          port: 3306
  egress:
    # DNS만 허용 (업데이트, NTP 등 필요 시 추가)
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: UDP
          port: 53

---
# 4. 기본 거부 정책 (Default Deny All)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}  # 모든 파드에 적용
  policyTypes:
    - Ingress
    - Egress
  # 규칙 없음 = 모든 트래픽 거부
```

### 마이크로 세그멘테이션 성능 메트릭

| 메트릭 | 전통적 방화벽 | 마이크로 세그멘테이션 | 비고 |
|---|---|---|---|
| **규칙 평가 시간** | 중앙 집중 (지연) | 분산 (마이크로초) | DFW는 호스트 로컬 |
| **확장성** | 방화벽 장비 한계 | 무제한 (호스트 증가) | 선형 확장 |
| **규칙 수** | 수천 개 | 수백만 개 | 워크로드별 규칙 |
| **가시성** | IP 기반 | 태그/워크로드 기반 | 동적 환경 대응 |

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 마이크로 세그멘테이션 제품 비교

| 제품 | 벤더 | 구현 방식 | 특징 | 적합 시나리오 |
|---|---|---|---|---|
| **NSX Distributed Firewall** | VMware | SDN/하이퍼바이저 | vSphere 통합, 고성능 | VMware 환경 |
| **Illumio Core** | Illumio | 에이전트 | 멀티 플랫폼, 시각화 우수 | 하이브리드 |
| **Guardicore Centra** | Akamai | 에이전트 | 위협 탐지 통합 | 데이터센터 |
| **Calico** | Tigera | CNI/네트워크 | Kubernetes 네이티브 | 컨테이너 |
| **Cilium** | Isovalent | eBPF | L7 가시성, 고성능 | 클라우드 네이티브 |
| **Cisco ACI** | Cisco | SDN | 하드웨어/소프트웨어 | 대형 데이터센터 |

### 과목 융합 관점 분석

- **네트워크와의 융합**: SDN(Software Defined Networking)이 마이크로 세그멘테이션의 기반입니다. VXLAN 오버레이 위에 분산 방화벽 규칙이 적용됩니다.

- **보안과의 융합**: 제로 트러스트 아키텍처(ZTA)의 핵심 요소입니다. "Never Trust, Always Verify" 원칙을 내부 네트워크에 적용합니다. NIST SP 800-207에서 표준화되었습니다.

- **컨테이너와의 융합**: Kubernetes Network Policy로 컨테이너 Pod 단위 격리를 구현합니다. Calico, Cilium, Weave Net이 대표적입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 금융권 데이터센터 보안 강화**
- **요구사항**: PCI-DSS 준수, 카드 데이터 DB 격리, 감사 추적
- **기술사의 의사결정**:
  1. VMware NSX DFW로 VM 단위 격리
  2. 카드 DB 서버는 앱 서버에서만 접근 허용
  3. 관리자 접근은 Jump Server + MFA 필요
  4. 모든 차단/허용 로그를 SIEM으로 전송
  5. **효과**: PCI-DSS 1.2.1, 1.3 항목 준수

**시나리오 2: 랜섬웨어 방어**
- **요구사항**: 랜섬웨어 확산 방지, 피해 범위 최소화
- **기술사의 의사결정**:
  1. Illumio로 모든 서버에 에이전트 배포
  2. 서비스 간 통신만 허용, 나머지 차단
  3. 의심스러운 통신 패턴 자동 탐지
  4. **효과**: 감염 시 1대만 피해, 확산 차단

### 도입 시 고려사항

- [ ] 애플리케이션 매핑: 현재 통신 패턴 파악 필수
- [ ] 단계적 도입: Monitor 모드 -> Enforce 모드
- [ ] 예외 처리: 레거시, 관리 트래픽 예외 규칙
- [ ] 성능 영향: 에이전트/DFW 오버헤드 측정

### 안티패턴

1. **과도한 세분화**: 모든 VM 간 규칙 생성 시 관리 복잡성 폭증. 그룹 기반 정책 사용.
2. **모니터링 스킵**: 바로 Enforce 모드 적용 시 서비스 중단. 반드시 Monitor 선행.
3. **태그 관리 소홀**: 태그가 잘못되면 정책이 잘못 적용됨. 자동 태깅 권장.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대효과

| 구분 | 기존 (Perimeter Only) | Micro-Segmentation | 개선 |
|---|---|---|---|
| **횡적 이동 차단** | 0% | 95%+ | 95% 향상 |
| **공격 표면** | 전체 내부망 | 개별 워크로드 | 99% 축소 |
| **감사 추적** | IP 기반 | 워크로드 기반 | 정확도 향상 |
| **규제 준수** | 부분 | 완전 | 100% 준수 |

### 미래 전망

1. **AI 기반 정책 생성**: 통신 패턴 학습으로 자동 정책 추천
2. **Decoupled Security**: 워크로드와 보안 정책 완전 분리
3. **SASE 통합**: SD-WAN + CASB + Micro-Segmentation 통합

### ※ 참고 표준
- **NIST SP 800-207**: Zero Trust Architecture
- **PCI-DSS v4.0**: Requirement 1 (Network Security)
- **CIS Kubernetes Benchmark**: Network Policy 권장사항

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [제로 트러스트](@/studynotes/13_cloud_architecture/01_native/zero_trust.md) : 마이크로 세그멘테이션의 보안 철학
- [SDN](@/studynotes/13_cloud_architecture/03_virt/sdn.md) : 구현 기반 기술
- [서비스 메시](@/studynotes/13_cloud_architecture/01_native/service_mesh.md) : L7 마이크로 세그멘테이션
- [Network Policy](@/studynotes/13_cloud_architecture/01_native/network_policy.md) : Kubernetes 구현
- [분산 방화벽](@/studynotes/13_cloud_architecture/03_virt/distributed_firewall.md) : NSX 구현

---

### 👶 어린이를 위한 3줄 비유 설명
1. 마이크로 세그멘테이션은 **'호텔 객실 키카드'**예요. 로비를 지나면 모든 방에 들어갈 수 있는 게 아니에요.
2. 내 키카드로는 **'내 방만'** 열려요. 다른 사람 방은 절대 못 들어가요.
3. 그래서 어떤 방에 **'나쁜 사람이 들어가도'** 다른 방은 안전해요. 문이 잠겨 있거든요!
