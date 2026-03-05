+++
title = "서비스 디스커버리 (Service Discovery)"
date = 2024-05-15
description = "클라우드 환경에서 동적으로 변하는 컨테이너/서비스의 위치(IP, Port)를 자동으로 등록하고 조회하는 메커니즘으로, Client-side와 Server-side 두 방식이 존재"
weight = 105
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Service Discovery", "Consul", "Eureka", "CoreDNS", "Kubernetes", "DNS"]
+++

# 서비스 디스커버리 (Service Discovery) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 클라우드/컨테이너 환경에서 서비스 인스턴스가 동적으로 생성/삭제될 때, 호출자가 **'어떤 서비스가 어디에 있는지'**를 자동으로 찾을 수 있게 해주는 분산 시스템의 필수 인프라입니다.
> 2. **가치**: 하드코딩된 IP/Port 의존성을 제거하여, 오토스케일링, 롤링 업데이트, 장애 복구 시 **서비스 간 통신이 투명하게 유지**되도록 합니다.
> 3. **융합**: Kubernetes의 CoreDNS/Service, HashiCorp Consul, Netflix Eureka, Istio Pilot 등 다양한 구현체가 있으며, DNS 기반과 API 기반 두 패러다임으로 나뉩니다.

---

## Ⅰ. 개요 (Context & Background)

서비스 디스커버리(Service Discovery)는 분산 시스템에서 서비스 인스턴스의 네트워크 위치(IP 주소와 포트)를 동적으로 찾는 메커니즘입니다. 전통적인 환경에서는 서비스가 고정된 IP를 가졌지만, 클라우드/컨테이너 환경에서는 인스턴스가 수시로 생성되고 삭제되므로, 이를 자동으로 관리하는 시스템이 필수적입니다.

**💡 비유**: 서비스 디스커버리는 **'전화번호부'**와 같습니다. 과거에는 친구 집 주소를 암기했지만(하드코딩), 친구가 이사하면 연락이 끊깁니다. 전화번호부(서비스 레지스트리)가 있으면 친구가 이사할 때마다 새 주소를 등록하고, 나는 이름만 찾으면 현재 주소를 알 수 있습니다.

**등장 배경 및 발전 과정**:
1. **마이크로서비스의 동적 특성**: 컨테이너는 수시로 생성/삭제되며 IP가 매번 달라집니다.
2. **Netflix Eureka (2012)**: Netflix가 자사 스트리밍 서비스를 위해 개발한 서비스 디스커버리가 오픈소스화되었습니다.
3. **Consul (2014)**: HashiCorp가 서비스 디스커버리 + Health Checking + KV Store를 통합하여 발표했습니다.
4. **Kubernetes CoreDNS**: K8s의 표준 서비스 디스커버리로 자리잡았습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 서비스 디스커버리 패턴

| 패턴 | 상세 설명 | 장점 | 단점 | 대표 구현 |
|---|---|---|---|---|
| **Client-side** | 클라이언트가 레지스트리 직접 조회 | 빠른 장애 감지, 로드밸런싱 제어 | 클라이언트 복잡도 증가 | Eureka, Consul |
| **Server-side** | 로드밸런서가 조회 후 프록시 | 클라이언트 단순 | LB SPOF, 지연 추가 | K8s Service, ALB |
| **DNS 기반** | DNS 쿼리로 서비스 위치 해석 | 범용성, 표준 | TTL 지연, 캐시 문제 | CoreDNS, Consul DNS |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                   [ Service Discovery Architecture ]                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                [ Client-Side Discovery Pattern ]                            │
│                                                                             │
│  ┌─────────────────┐                                                        │
│  │    Service A    │                                                        │
│  │    (Client)     │                                                        │
│  │  ┌───────────┐  │     1. Get Service B locations                        │
│  │  │ Discovery │  │ ─────────────────────────┐                             │
│  │  │  Client   │  │                          │                             │
│  │  └─────┬─────┘  │                          ▼                             │
│  └────────┼────────┘    ┌───────────────────────────────────────┐         │
│           │             │        Service Registry               │         │
│           │             │  ┌─────────────────────────────────┐  │         │
│           │             │  │ Service B:                      │  │         │
│           │             │  │  - 10.0.1.2:8080 (healthy)      │  │         │
│           │             │  │  - 10.0.1.3:8080 (healthy)      │  │         │
│           │             │  │  - 10.0.1.4:8080 (unhealthy)    │  │         │
│           │             │  │ Service C: ...                  │  │         │
│           │             │  └─────────────────────────────────┘  │         │
│           │             └───────────────────────────────────────┘         │
│           │                            ▲                                   │
│           │             3. Heartbeat  │     2. Register                    │
│           │             ┌─────────────┴─────────────────────┐             │
│           │             │                                     │             │
│           │    ┌────────┴────────┐    ┌────────────────┐    │             │
│           │    │  Service B      │    │  Service B     │    │             │
│           │    │  Instance 1     │    │  Instance 2    │    │             │
│           │    │  10.0.1.2:8080  │    │  10.0.1.3:8080 │    │             │
│           │    └─────────────────┘    └────────────────┘    │             │
│           │                                                        │        │
│           │  4. Direct Call (Load Balanced)                      │        │
│           └──────────────────────────────────────────────────────┘        │
│                                                                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                [ Server-Side Discovery Pattern ]                            │
│                                                                             │
│  ┌─────────────────┐                                                        │
│  │    Service A    │                                                        │
│  │    (Client)     │     1. Request to service-b                            │
│  │  ┌───────────┐  │ ────────────────────────►                              │
│  │  │ Simple    │  │                          ┌──────────────────┐         │
│  │  │ HTTP Call │  │                          │  Load Balancer   │         │
│  │  └───────────┘  │                          │  (Router)        │         │
│  └─────────────────┘                          │  ┌────────────┐  │         │
│                                                │  │ Query      │  │         │
│                                                │  │ Registry   │  │         │
│                                                │  └────────────┘  │         │
│                                                └────────┬─────────┘         │
│                                                         │                   │
│                          2. Route to healthy instance   │                   │
│                                                         ▼                   │
│                  ┌────────────────────────────────────────────────┐        │
│                  │  Service B Instances                           │        │
│                  │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │        │
│                  │  │Inst 1    │  │Inst 2    │  │Inst 3    │    │        │
│                  │  │10.0.1.2  │  │10.0.1.3  │  │10.0.1.4  │    │        │
│                  │  └──────────┘  └──────────┘  └──────────┘    │        │
│                  └────────────────────────────────────────────────┘        │
│                                                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: Kubernetes Service 디스커버리

```
┌────────────────────────────────────────────────────────────────────────────┐
│                Kubernetes Service Discovery Flow                           │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ 1. Service 등록 ]                                                       │
│                                                                            │
│  kubectl apply -f service.yaml                                             │
│         │                                                                  │
│         ▼                                                                  │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │                    Kubernetes API Server                         │     │
│  │  - Service 객체 생성                                              │     │
│  │  - ClusterIP (10.96.0.1) 할당                                     │     │
│  │  - Endpoints 객체 생성 (Pod IP 매핑)                              │     │
│  └──────────────────────────────────────────────────────────────────┘     │
│         │                                                                  │
│         ▼                                                                  │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │                         CoreDNS                                  │     │
│  │  - Service DNS 레코드 생성                                        │     │
│  │  - my-service.default.svc.cluster.local → 10.96.0.1              │     │
│  └──────────────────────────────────────────────────────────────────┘     │
│                                                                            │
│  [ 2. 서비스 간 호출 ]                                                      │
│                                                                            │
│  Client Pod ───► DNS Query ───► CoreDNS ───► ClusterIP                   │
│                      │                         │                           │
│                      ▼                         ▼                           │
│              my-service.default         10.96.0.1                         │
│                      │                         │                           │
│                      └──────────┬──────────────┘                           │
│                                 │                                          │
│                                 ▼                                          │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │                      kube-proxy                                  │     │
│  │  - iptables/IPVS 규칙 생성                                        │     │
│  │  - ClusterIP → Pod IP 매핑                                       │     │
│  │  - 로드밸런싱 (Round Robin)                                       │     │
│  └──────────────────────────────────────────────────────────────────┘     │
│                                 │                                          │
│                                 ▼                                          │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │                   Target Pod                                     │     │
│  │  - 10.244.1.5:8080                                               │     │
│  │  - 10.244.1.6:8080                                               │     │
│  │  - 10.244.2.3:8080                                               │     │
│  └──────────────────────────────────────────────────────────────────┘     │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: Consul 서비스 디스커버리

```hcl
# Consul Service Definition (user-service.hcl)

service {
  name = "user-service"
  id   = "user-service-1"
  tags = ["v1", "primary"]
  address = "10.0.1.10"
  port    = 8080

  # 헬스 체크 정의
  check {
    id     = "user-service-health"
    name   = "HTTP Health Check"
    http   = "http://10.0.1.10:8080/health"
    interval = "10s"
    timeout  = "5s"
    deregister_critical_service_after = "1m"
  }

  # 태그 기반 라우팅 (Canary 배포용)
  meta = {
    version = "1.0.0"
    weight  = "90"
  }
}

# Consul Connect (Service Mesh) 설정
service {
  name = "user-service"
  connect {
    sidecar_service {
      proxy {
        upstreams = [
          {
            destination_name = "order-service"
            local_bind_port  = 5000
          }
        ]
      }
    }
  }
}
```

```python
# Python Client with Consul Discovery
import consul
import random
import requests

class ConsulServiceDiscovery:
    """Consul 기반 서비스 디스커버리 클라이언트"""

    def __init__(self, host='localhost', port=8500):
        self.consul = consul.Consul(host=host, port=port)
        self.cache = {}  # 로컬 캐시
        self.cache_ttl = 30  # 초

    def get_service_url(self, service_name: str) -> str:
        """서비스 이름으로 URL 조회"""

        # 1. 캐시 확인
        if service_name in self.cache:
            cached = self.cache[service_name]
            if time.time() - cached['timestamp'] < self.cache_ttl:
                instances = cached['instances']
            else:
                instances = self._fetch_from_consul(service_name)
        else:
            instances = self._fetch_from_consul(service_name)

        # 2. 인스턴스가 없으면 에러
        if not instances:
            raise ServiceNotFoundError(f"Service {service_name} not found")

        # 3. 로드밸런싱 (Round Robin)
        instance = random.choice(instances)
        return f"http://{instance['Address']}:{instance['Port']}"

    def _fetch_from_consul(self, service_name: str):
        """Consul에서 서비스 인스턴스 조회 (헬스 체크 통과만)"""
        _, services = self.consul.health.service(
            service_name,
            passing=True  # 건강한 인스턴스만
        )

        instances = []
        for service in services:
            instances.append({
                'Address': service['Service']['Address'],
                'Port': service['Service']['Port'],
                'Tags': service['Service']['Tags']
            })

        # 캐시 갱신
        self.cache[service_name] = {
            'instances': instances,
            'timestamp': time.time()
        }

        return instances

    def call_service(self, service_name: str, path: str, method='GET', **kwargs):
        """서비스 호출 헬퍼"""
        url = f"{self.get_service_url(service_name)}{path}"
        response = requests.request(method, url, **kwargs)
        return response

# 사용 예시
discovery = ConsulServiceDiscovery()
response = discovery.call_service('order-service', '/api/orders')
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 서비스 디스커버리 솔루션

| 비교 관점 | Consul | Eureka | CoreDNS (K8s) | Zookeeper |
|---|---|---|---|---|
| **CAP** | CP (일관성) | AP (가용성) | CP | CP |
| **헬스 체크** | TCP/HTTP/Script | Heartbeat | K8s Probes | Session |
| **DNS 지원** | 있음 | 없음 | 기본 | 없음 |
| **KV Store** | 있음 | 없음 | ConfigMap | 있음 |
| **복잡도** | 중간 | 낮음 | 낮음 (K8s) | 높음 |
| **언어** | Go | Java | Go | Java |

### 과목 융합 관점 분석

**네트워크와의 융합**:
- **DNS Resolution**: 서비스 이름 → IP 변환
- **Load Balancing**: DNS Round Robin, Client-side LB

**데이터베이스와의 융합**:
- **Raft Consensus**: Consul의 분산 합의 알고리즘
- **Gossip Protocol**: Eureka의 피어 투 피어 복제

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 서비스 디스커버리 선택

**문제 상황**: 100개 마이크로서비스를 Kubernetes 환경에서 운영 중입니다.

**기술사의 전략적 의사결정**:
1. **1순위: Kubernetes Native (CoreDNS + Service)**
   - 추가 인프라 없이 K8s 내장 기능 사용
   - DNS 기반 조회로 언어 독립적
2. **2순위: Consul (복잡한 요구사항 시)**
   - 온프레미스/멀티 클라우드 환경
   - Service Mesh (Consul Connect) 필요 시

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - DNS TTL 캐시**: DNS 기반 디스커버리는 TTL 동안 캐시되어, 장애 인스턴스에 계속 연결될 수 있습니다.
- **체크리스트**:
  - [ ] 헬스 체크 주기 및 타임아웃 설정
  - [ ] 캐싱 전략 (TTL, Client-side cache)
  - [ ] 장애 시 Fallback 메커니즘
  - [ ] 멀티 리전/데이터센터 지원

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 하드코딩 IP | 서비스 디스커버리 | 개선 |
|---|---|---|---|
| **장애 복구 시간** | 수동 (수시간) | 자동 (수초) | 99% 단축 |
| **스케일링 대응** | 수동 설정 | 자동 감지 | 100% 자동화 |
| **운영 복잡도** | 높음 | 낮음 | 향상 |

### 미래 전망 및 진화 방향

- **Multi-Cluster Service Discovery**: Federation, Consul Multi-DC
- **AI-Driven Discovery**: 트래픽 패턴 기반 최적 인스턴스 선택

### ※ 참고 표준/가이드
- **DNS SRV Records**: 서비스 디스커버리 표준 DNS 레코드
- **RFC 2782**: DNS SRV RR 스펙

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [마이크로서비스 아키텍처 (MSA)](@/studynotes/13_cloud_architecture/01_native/msa.md) : 서비스 디스커버리의 상위 아키텍처
- [API 게이트웨이](@/studynotes/13_cloud_architecture/01_native/api_gateway.md) : 디스커버리 활용
- [Kubernetes Service](@/studynotes/13_cloud_architecture/01_native/kubernetes_service.md) : K8s 네이티브 디스커버리
- [로드 밸런서](@/studynotes/13_cloud_architecture/03_virt/load_balancer.md) : 트래픽 분산
- [Consul](@/studynotes/13_cloud_architecture/01_native/consul.md) : 대표적 구현체

---

### 👶 어린이를 위한 3줄 비유 설명
1. 서비스 디스커버리는 **'전화번호부'**예요. 친구 집 주소를 외우지 않아도 돼요.
2. 친구가 이사하면 **'새 주소를 전화번호부에 등록'**해요. 나는 이름만 찾으면 돼요.
3. 그리고 친구가 **'집에 없으면(장애) 다른 친구 집으로 연결'**해줘요. 전화를 안 받으면 다른 번호로!
