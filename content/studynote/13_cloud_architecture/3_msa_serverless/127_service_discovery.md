+++
weight = 127
title = "서비스 디스커버리 (Service Discovery)"
date = "2024-03-24"
[extra]
categories = "studynote-cloud"
+++

## 핵심 인사이트 (3줄 요약)
- **서비스 디스커버리**는 클라우드 환경에서 오토스케일링 등으로 인해 동적으로 변하는 마이크로서비스들의 IP 주소와 포트 위치를 자동으로 찾아주는 매커니즘임.
- 각 서비스의 상태를 저장하는 **서비스 레지스트리(Service Registry)**와 이를 조회하는 탐색 로직으로 구성됨.
- 클라이언트 사이드와 서버 사이드 탐색 방식이 있으며, MSA 환경의 네트워킹 핵심 기반 기술임.

### Ⅰ. 개요 (Context & Background)
- 고정된 IP를 가진 전통적인 서버 환경과 달리, 클라우드/컨테이너 환경에서는 파드(Pod)나 인스턴스가 수시로 생성되고 소멸함.
- 수백 개의 서비스가 서로 통신할 때 수동으로 IP를 관리하는 것은 불가능하므로, 동적으로 위치 정보를 등록하고 조회하는 자동화 체계가 필수적임.
- 넷플릭스 유레카(Eureka), 쿠버네티스 서비스(DNS/Kube-proxy), 주키퍼(ZooKeeper) 등이 대표적인 솔루션임.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- 서비스 디스커버리는 '등록(Registration)', '해지(Deregistration)', '탐색(Lookup)'의 생명주기를 가짐.

```text
[ Service Discovery Workflow ]
+---------------------+       +---------------------+
|  Service Registry   | <---  |  New Service Node   |
| (Database of IPs)   | [REG] | [Self-Registration] |
+---------------------+       +---------------------+
          ^
          | [LOOKUP]
+---------|-----------+       +---------------------+
|   Service Consumer  | ----> |   Service Provider  |
| (Client/Gateway)    | [CALL]| (Found via IP/Port) |
+---------------------+       +---------------------+

[ BILINGUAL PATTERN: Client vs Server Side ]
1. Client-Side: Client calls Registry -> Gets IP -> Calls Service Direct. (e.g., Netflix Eureka)
2. Server-Side: Client calls Load Balancer -> LB calls Registry -> LB routes to Service. (e.g., AWS ELB, K8s Service)

+-------------------+       +-------------------+       +-------------------+
|     Client        | ----> |   Load Balancer   | ----> |   Service Node    |
| [Request Service] |       | [Query Registry]  |       | [Receive Request] |
+-------------------+       +-------------------+       +-------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 방식 | 클라이언트 사이드 (Client-Side) | 서버 사이드 (Server-Side) |
| :--- | :--- | :--- |
| **특징** | 클라이언트가 레지스트리를 직접 조회 | 로드밸런서가 레지스트리 조회 대행 |
| **장점** | 서비스별 부하 분산 알고리즘 직접 구현 | 클라이언트 로직 단순화 (투명성) |
| **단점** | 서비스 언어별 디스커버리 라이브러리 필요 | 로드밸런서 자체가 가용성 병목(SPOF) 가능 |
| **솔루션** | Netflix Eureka, Consul | Kubernetes Service, AWS ELB/ALB |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **헬스 체크(Health Check)**: 레지스트리는 서비스 노드의 생존 여부를 주기적으로 확인하여, 장애가 발생한 노드의 IP를 자동으로 목록에서 제거해야 함.
- **쿠버네티스 기반 표준**: 최근에는 인프라 레벨에서 DNS를 통해 서비스 디스커버리를 제공하는 쿠버네티스 표준 방식이 선호됨.
- **가용성 설계**: 서비스 레지스트리 자체가 죽으면 전체 통신이 불가능해지므로, 레지스트리는 반드시 클러스터링(etcd 등)을 통해 고가용성을 확보해야 함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- 서비스 디스커버리는 유연한 확장(Scaling)과 자가 치유(Self-healing) 아키텍처를 실현하는 클라우드 네이티브의 근간임.
- 향후 서비스 메시(Service Mesh)에서는 사이드카 프록시가 이 역할을 대행하며 개발자의 비즈니스 로직과 더욱 격리될 것임.
- 결론적으로 서비스 디스커버리는 **복잡한 분산 시스템의 '내비게이션'** 역할을 수행하여 통신 복잡도를 획기적으로 낮춤.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 마이크로서비스 아키텍처 (MSA), 오케스트레이션
- **하위 개념**: 서비스 레지스트리, 헬스 체크, 유레카, DNS
- **연관 개념**: 로드 밸런서, API 게이트웨이, 쿠버네티스, etcd

### 👶 어린이를 위한 3줄 비유 설명
- 학교 축제 때 떡볶이 가게 위치가 자꾸 바뀔 때, 게시판에 가서 "오늘 떡볶이 어디서 팔아요?"라고 물어보는 것과 같아요.
- 게시판(레지스트리)은 가게가 어디로 이사 갔는지 실시간으로 알려줘요.
- 덕분에 손님들은 가게 주소를 외우지 않아도 맛있는 떡볶이를 찾으러 갈 수 있답니다.
