+++
title = "쿠버네티스 네트워킹 (Kubernetes Networking)"
date = "2026-03-05"
[extra]
categories = "studynotes-cloud"
tags = ["kubernetes", "networking", "cni", "service", "ingress", "container"]
+++

# 쿠버네티스 네트워킹 (Kubernetes Networking)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 쿠버네티스 네트워킹은 모든 파드가 고유 IP를 가지고 NAT 없이 서로 통신하며, 서비스(Service)와 인그레스(Ingress)를 통해 외부 트래픽을 동적으로 라우팅하는 선언적 네트워크 추상화 계층입니다.
> 2. **가치**: 마이크로서비스 간 복잡한 통신을 Service Discovery, 로드밸런싱, 네트워크 정책으로 자동화하여 개발자가 인프라가 아닌 비즈니스 로직에 집중하게 합니다.
> 3. **융합**: CNI 플러그인, eBPF 기반 데이터플레인, 서비스 메시와 결합하여 엔터프라이즈급 네트워크 보안과 옵저버빌리티를 제공합니다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의
쿠버네티스 네트워킹은 컨테이너화된 애플리케이션의 통신 요구사항을 충족하기 위해 설계된 네트워크 모델로, 다음의 핵심 원칙을 따릅니다: (1) 모든 파드는 NAT 없이 다른 모든 파드와 통신 가능, (2) 모든 노드의 에이전트는 모든 파드와 통신 가능, (3) 파드의 IP는 다른 파드가 볼 때 자신이 본 IP와 동일. 이를 위해 CNI(Container Network Interface) 플러그인, Service 추상화, Ingress 컨트롤러, Network Policy 등의 계층적 구성요소가 협력합니다.

### 💡 비유
쿠버네티스 네트워킹은 "스마트 우편 시스템"과 같습니다. 각 집(파드)은 고유 주소(IP)를 가지고, 우편 배달부(Service)는 편지를 올바른 집으로 배달합니다. 동네 게이트웨이(Ingress)는 외부에서 오는 우편을 분류하여 각 구역으로 전달하고, 보안 요원(Network Policy)은 허가된 사람만 특정 집에 들어갈 수 있게 통제합니다.

### 등장 배경 및 발전 과정

#### 1. 기존 네트워킹의 한계
- **포트 매핑 지옥**: Docker 기본 네트워크는 호스트 포트를 컨테이너에 매핑, 충돌 빈발
- **IP 주소 관리**: 동적 컨테이너 생성/삭제 시 IP 추적 불가능
- **로드밸런싱 부재**: 컨테이너 확장 시 트래픽 분산을 수동으로 구성
- **서비스 디스커버리 없음**: 컨테이너 IP 변경 시 다른 서비스가 인지 못함

#### 2. 패러다임 변화
```
2014년: Google Borg에서 Kubernetes 네트워크 모델 원형 도출
2015년: CNI (Container Network Interface) 표준화 - CoreOS 주도
2016년: Calico, Flannel 등 오버레이 네트워크 솔루션 등장
2017년: Cilium eBPF 기반 네트워킹 혁신
2018년: Network Policy API 정식 채택
2020년: Service Mesh(Istio)와 쿠버네티스 네트워킹 통합 가속화
2023년: Gateway API (Ingress 차세대) 베타 출시
```

#### 3. 비즈니스적 요구사항
- 마이크로서비스 간 통신 복잡도 증가 (수천 개 서비스)
- 제로 트러스트 네트워크 보안 요구
- 멀티 클러스터, 하이브리드 클라우드 네트워킹
- 네트워크 레벨 옵저버빌리티 (트래픽 추적)

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|-----------|------|
| **CNI 플러그인** | 파드 네트워크 인터페이스 생성/삭제 | veth pair 생성, 브리지 연결, IP 할당 | Calico, Flannel, Cilium, Weave | 우편 배달 경로 생성 |
| **Pause 컨테이너** | 파드 네트워크 네임스페이스 유지 | 최초 실행되어 netns 생성, 다른 컨테이너가 공유 | infra container | 공용 우편함 설치 |
| **kube-proxy** | 서비스 VIP → 파드 IP 매핑 | iptables/IPVS 규칙 프로그래밍 | iptables mode, IPVS mode | 우편 분류 기계 |
| **Service (ClusterIP)** | 클러스터 내부 통신 진입점 | 가상 IP 할당, Endpoints 컨트롤 | 10.96.0.0/12 (기본) | 내부 우편 코드 |
| **Service (NodePort)** | 노드 포트로 외부 트래픽 수신 | 30000-32767 포트 오픈, 모든 노드에 적용 | NodePort Service | 동네 게시판 |
| **Service (LoadBalancer)** | 클라우드 LB와 연동 | AWS ALB, GCP LB 프로비저닝 | MetalLB (온프레미스) | 우체국 창구 |
| **Ingress** | L7(HTTP/HTTPS) 라우팅 | Host/Path 기반 트래픽 분기 | NGINX, Traefik, HAProxy | 고속도로 IC |
| **NetworkPolicy** | 파드 간 접근 통제 | iptables/match 규칙으로 화이트리스트 | Calico, Cilium | 출입증 검사 |
| **CoreDNS** | 클러스터 내 DNS 서비스 | Service 이름 → ClusterIP 변환 | CoreDNS, kube-dns | 전화번호부 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       쿠버네티스 네트워킹 전체 아키텍처                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────┐      │
│   │                        External World                                │      │
│   │  [Internet Users] ──▶ [DNS: app.example.com]                        │      │
│   └────────────────────────────┬────────────────────────────────────────┘      │
│                                │                                                │
│                                ▼                                                │
│   ┌─────────────────────────────────────────────────────────────────────┐      │
│   │                    Cloud Load Balancer (L4)                          │      │
│   │                    AWS ALB / GCP LB / MetalLB                        │      │
│   │                    External IP: 203.0.113.10                         │      │
│   └────────────────────────────┬────────────────────────────────────────┘      │
│                                │ :443                                          │
│                                ▼                                                │
│   ┌─────────────────────────────────────────────────────────────────────┐      │
│   │                        Ingress Controller                            │      │
│   │  ┌─────────────────────────────────────────────────────────────┐   │      │
│   │  │  NGINX Ingress / Traefik / HAProxy                          │   │      │
│   │  │                                                               │   │      │
│   │  │  Rules:                                                      │   │      │
│   │  │  - host: api.example.com → Service: api-service             │   │      │
│   │  │  - host: web.example.com → Service: web-service             │   │      │
│   │  │  - path: /api/v1/*        → Service: api-v1-service         │   │      │
│   │  │                                                               │   │      │
│   │  │  TLS Termination: Let's Encrypt Cert                         │   │      │
│   │  └─────────────────────────────────────────────────────────────┘   │      │
│   └────────────────────────────┬────────────────────────────────────────┘      │
│                                │                                                │
│          ┌─────────────────────┼─────────────────────┐                         │
│          │                     │                     │                         │
│          ▼                     ▼                     ▼                         │
│   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐                   │
│   │  Service    │      │  Service    │      │  Service    │                   │
│   │ ClusterIP   │      │ ClusterIP   │      │ ClusterIP   │                   │
│   │10.96.10.1   │      │10.96.10.2   │      │10.96.10.3   │                   │
│   │Port: 8080   │      │Port: 80     │      │Port: 5432   │                   │
│   └──────┬──────┘      └──────┬──────┘      └──────┬──────┘                   │
│          │                    │                    │                           │
│          │ kube-proxy         │ kube-proxy         │ kube-proxy               │
│          │ (iptables/IPVS)    │                    │                           │
│          ▼                    ▼                    ▼                           │
│   ┌─────────────────────────────────────────────────────────────────────┐      │
│   │                         Worker Nodes                                 │      │
│   │  ┌───────────────────────────────────────────────────────────────┐  │      │
│   │  │                      Node 1 (10.244.1.0/24)                    │  │      │
│   │  │  ┌────────────────────────────────────────────────────────┐   │  │      │
│   │  │  │              Pod Network Namespace                      │   │  │      │
│   │  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │   │  │      │
│   │  │  │  │   Pod A     │  │   Pod B     │  │   Pod C     │    │   │  │      │
│   │  │  │  │ 10.244.1.5  │  │ 10.244.1.6  │  │ 10.244.1.7  │    │   │  │      │
│   │  │  │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │    │   │  │      │
│   │  │  │  │ │Pause    │ │  │ │Pause    │ │  │ │Pause    │ │    │   │  │      │
│   │  │  │  │ │Container│ │  │ │Container│ │  │ │Container│ │    │   │  │      │
│   │  │  │  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │    │   │  │      │
│   │  │  │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │    │   │  │      │
│   │  │  │  │ │ App     │ │  │ │ App     │ │  │ │ App     │ │    │   │  │      │
│   │  │  │  │ │Container│ │  │ │Container│ │  │ │Container│ │    │   │  │      │
│   │  │  │  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │    │   │  │      │
│   │  │  │  └─────────────┘  └─────────────┘  └─────────────┘    │   │  │      │
│   │  │  └────────────────────────────────────────────────────────┘   │  │      │
│   │  │                                                                │  │      │
│   │  │  ┌─────────────────────────────────────────────────────────┐  │  │      │
│   │  │  │                  CNI Plugin (Calico)                     │  │  │      │
│   │  │  │   [veth0] ─── [cni0 bridge] ─── [vxlan/calico]          │  │  │      │
│   │  │  │                                                      │  │  │      │
│   │  │  │   NetworkPolicy Enforcement: iptables rules           │  │  │      │
│   │  │  │   BGP Routing for Pod IP advertisement                │  │  │      │
│   │  │  └─────────────────────────────────────────────────────────┘  │  │      │
│   │  └───────────────────────────────────────────────────────────────┘  │      │
│   │                                                                      │      │
│   │  ┌───────────────────────────────────────────────────────────────┐  │      │
│   │  │                      Node 2 (10.244.2.0/24)                    │  │      │
│   │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │  │      │
│   │  │  │   Pod D     │  │   Pod E     │  │   Pod F     │           │  │      │
│   │  │  │ 10.244.2.5  │  │ 10.244.2.6  │  │ 10.244.2.7  │           │  │      │
│   │  │  └─────────────┘  └─────────────┘  └─────────────┘           │  │      │
│   │  └───────────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────────┘      │
│                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────┐      │
│   │                      CoreDNS (Cluster DNS)                           │      │
│   │  Service: kube-dns (10.96.0.10)                                      │      │
│   │  ConfigMap: Corefile                                                 │      │
│   │    .:53 {                                                            │      │
│   │      errors                                                          │      │
│   │      health                                                          │      │
│   │      kubernetes cluster.local in-addr.arpa ip6.arpa {               │      │
│   │        pods insecure                                                 │      │
│   │        fallthrough in-addr.arpa ip6.arpa                            │      │
│   │      }                                                               │      │
│   │      forward . /etc/resolv.conf                                     │      │
│   │      cache 30                                                        │      │
│   │    }                                                                 │      │
│   └─────────────────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

#### ① 파드 네트워킹 생성 프로세스 (CNI 호출 흐름)

```
Step 1: Kubelet이 파드 생성 감지
        - API Server에서 파드 Spec 수신
        - 파드가 네트워크 준비 상태가 아님을 확인
                    │
                    ▼
Step 2: CNI 플러그인 호출
        - Kubelet이 /opt/cni/bin/abc 경로의 플러그인 실행
        - 환경 변수로 CNI_COMMAND=ADD 전달
        - Stdin으로 네트워크 구성 JSON 전달
                    │
                    ▼
Step 3: 네트워크 네임스페이스 생성 (Pause 컨테이너)
        - Pause 컨테이너가 먼저 실행되어 netns 생성
        - /proc/<pid>/ns/net → 네트워크 네임스페이스 참조
                    │
                    ▼
Step 4: veth pair 생성
        - 호스트 측: vethxxxxx (호스트 네임스페이스)
        - 컨테이너 측: eth0 (파드 네임스페이스)
        - 양방향 터널 연결
                    │
                    ▼
Step 5: 브리지/라우팅 연결
        - [Flannel] veth를 cni0 브리지에 연결
        - [Calico] 라우팅 테이블에 파드 IP 경로 추가
        - [Cilium] eBPF 프로그램으로 tc 필터 연결
                    │
                    ▼
Step 6: IP 주소 할당
        - IPAM (IP Address Management) 플러그인 호출
        - host-local: 로컬 파일 기반 할당
        - calico-ipam: etcd 기반 중앙 관리
                    │
                    ▼
Step 7: 파드 내 네트워크 구성
        - eth0 인터페이스에 IP 설정
        - 기본 라우팅 (default via gateway)
        - /etc/resolv.conf에 DNS 서버 설정
                    │
                    ▼
Step 8: 결과 반환
        - CNI 플러그인이 JSON 결과 반환
        - Kubelet이 파드 상태를 "Ready"로 변경
```

#### ② Service 타입별 트래픽 흐름 상세

```python
# Service 트래픽 흐름 시뮬레이션

class KubernetesNetworkingSimulator:
    """쿠버네티스 네트워킹 트래픽 흐름 시뮬레이터"""

    def __init__(self):
        self.services = {}
        self.endpoints = {}
        self.iptables_rules = []

    def simulate_clusterip_traffic(self, source_pod_ip: str,
                                    service_cluster_ip: str,
                                    service_port: int) -> dict:
        """
        ClusterIP Service 트래픽 흐름 시뮬레이션
        """
        flow = {
            'steps': [],
            'final_destination': None
        }

        # Step 1: 소스 파드에서 패킷 생성
        flow['steps'].append({
            'step': 1,
            'location': 'Source Pod',
            'action': f'패킷 생성: {source_pod_ip}:random_port → {service_cluster_ip}:{service_port}',
            'detail': '애플리케이션이 Service VIP로 요청'
        })

        # Step 2: 파드 네트워크 네임스페이스에서 나감
        flow['steps'].append({
            'step': 2,
            'location': 'Pod Network Namespace',
            'action': '라우팅 조회',
            'detail': '목적지가 Service CIDR(10.96.0.0/12) 내 → kube-proxy 처리'
        })

        # Step 3: 호스트 네트워크 네임스페이스 진입
        flow['steps'].append({
            'step': 3,
            'location': 'Host Network Namespace',
            'action': 'iptables PREROUTING 체인 진입',
            'detail': 'KUBE-SERVICES 체인으로 점프'
        })

        # Step 4: DNAT (Destination NAT)
        service = self.services.get(service_cluster_ip)
        if service:
            # 라운드로빈으로 백엔드 파드 선택
            backend_pod = self._select_backend_pod(service)
            flow['steps'].append({
                'step': 4,
                'location': 'iptables DNAT',
                'action': f'DNAT 수행: {service_cluster_ip}:{service_port} → {backend_pod["ip"]}:{backend_pod["port"]}',
                'detail': 'KUBE-SVC-xxx 체인에서 실제 파드 IP로 변환'
            })

            # Step 5: 파드로 전달
            flow['steps'].append({
                'step': 5,
                'location': 'Destination Pod',
                'action': f'패킷 도착: {backend_pod["ip"]}:{backend_pod["port"]}',
                'detail': 'CNI 오버레이/라우팅을 통해 목적지 파드 도달'
            })

            flow['final_destination'] = backend_pod

        return flow

    def simulate_nodeport_traffic(self, external_ip: str,
                                   node_port: int) -> dict:
        """
        NodePort Service 트래픽 흐름 시뮬레이션
        """
        flow = {'steps': []}

        flow['steps'].append({
            'step': 1,
            'location': 'External Client',
            'action': f'연결 시도: {external_ip}:{node_port}',
            'detail': '외부 클라이언트가 노드의 NodePort로 접속'
        })

        flow['steps'].append({
            'step': 2,
            'location': 'Node Network Stack',
            'action': 'iptables NodePort 규칙 매칭',
            'detail': f'KUBE-NODEPORTS 체인에서 포트 {node_port} 규칙 검색'
        })

        flow['steps'].append({
            'step': 3,
            'location': 'iptables',
            'action': 'ClusterIP Service로 리다이렉트',
            'detail': 'NodePort → ClusterIP 변환 후 일반 Service 흐름 진입'
        })

        return flow

    def simulate_ingress_traffic(self, host: str, path: str) -> dict:
        """
        Ingress를 통한 L7 라우팅 시뮬레이션
        """
        flow = {'steps': []}

        flow['steps'].append({
            'step': 1,
            'location': 'External Client',
            'action': f'HTTPS 요청: Host={host}, Path={path}',
            'detail': 'SNI 기반 TLS 연결, HTTP 헤더에 Host 포함'
        })

        flow['steps'].append({
            'step': 2,
            'location': 'Load Balancer',
            'action': 'L4 로드밸런싱',
            'detail': '외부 트래픽을 Ingress Controller 파드로 분산'
        })

        flow['steps'].append({
            'step': 3,
            'location': 'Ingress Controller (NGINX)',
            'action': f'Host/Path 기반 라우팅: {host}{path}',
            'detail': 'Ingress Rule 매칭 → 백엔드 Service 결정'
        })

        flow['steps'].append({
            'step': 4,
            'location': 'Ingress Controller → Service',
            'action': 'ClusterIP Service 호출',
            'detail': 'kube-proxy를 통해 실제 파드로 전달'
        })

        return flow

    def _select_backend_pod(self, service: dict) -> dict:
        """라운드로빈 백엔드 선택"""
        import random
        endpoints = self.endpoints.get(service['name'], [])
        return random.choice(endpoints) if endpoints else None


# 실제 iptables 규칙 예시 (kube-proxy 생성)
IPTABLES_EXAMPLE = """
# KUBE-SERVICES 체인 (Service 진입점)
-A KUBE-SERVICES -d 10.96.10.1/32 -p tcp --dport 8080 -j KUBE-SVC-ABC123

# KUBE-SVC-xxx 체인 (서비스별 체인, 확률 기반 로드밸런싱)
-A KUBE-SVC-ABC123 -m statistic --mode random --probability 0.3333 -j KUBE-SEP-1
-A KUBE-SVC-ABC123 -m statistic --mode random --probability 0.5000 -j KUBE-SEP-2
-A KUBE-SVC-ABC123 -j KUBE-SEP-3

# KUBE-SEP-xxx 체인 (개별 엔드포인트)
-A KUBE-SEP-1 -p tcp -j DNAT --to-destination 10.244.1.5:8080
-A KUBE-SEP-2 -p tcp -j DNAT --to-destination 10.244.1.6:8080
-A KUBE-SEP-3 -p tcp -j DNAT --to-destination 10.244.2.5:8080
"""
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: CNI 플러그인

| CNI 플러그인 | 네트워크 모드 | 성능 특성 | 기능 | 적용 시나리오 |
|-------------|-------------|-----------|------|--------------|
| **Flannel** | VXLAN, host-gw | 중간 (VXLAN 오버헤드) | 기본 연결성 | 소규모 클러스터, 간편 설치 |
| **Calico** | BGP, IPIP, VXLAN | 높음 (직접 라우팅) | NetworkPolicy, BGP | 엔터프라이즈, 보안 중요 |
| **Cilium** | eBPF | 매우 높음 | L7 Policy, 옵저버빌리티 | 고성능, 서비스 메시 통합 |
| **Weave Net** | VXLAN | 중간 | 간편 설치, 암호화 | 개발/테스트 환경 |
| **Antrea** | OVS | 높음 | VMware 통합 | vSphere 환경 |

### Service 타입 비교

| Service 타입 | 접근 범위 | 외부 IP | 사용 사례 | 비용 |
|-------------|----------|---------|----------|------|
| **ClusterIP** | 클러스터 내부만 | 없음 (10.96.x.x) | 내부 서비스 간 통신 | 무료 |
| **NodePort** | 외부 가능 (노드 IP) | 노드 IP:30000+ | 개발/테스트, 내부 서비스 노출 | 무료 |
| **LoadBalancer** | 외부 가능 | 클라우드 LB IP | 운영 웹 서비스 | LB 비용 부과 |
| **ExternalName** | 클러스터 내부 → 외부 | 없음 | 외부 서비스 DNS 별칭 | 무료 |
| **Headless** | 클러스터 내부 | 없음 (DNS로만) | StatefulSet, 직접 파드 접근 | 무료 |

### 과목 융합 관점 분석

#### [클라우드 + 네트워크] 오버레이 vs 언더레이
```
쿠버네티스 네트워킹의 두 가지 접근:

1. 오버레이 네트워크 (Overlay)
   - Flannel VXLAN: 원본 패킷을 UDP로 캡슐화
   - 장점: 물리 네트워크 구성 변경 불필요
   - 단점: 캡슐화 오버헤드 (약 50 bytes/packet)

   패킷 구조:
   ┌──────────┬──────────┬──────────┬─────────────────────┐
   │  외부 IP  │  UDP 헤더 │  VXLAN   │  원본 이더넷 프레임  │
   │  Header  │  (8B)    │  (8B)    │  (64-1518B)         │
   └──────────┴──────────┴──────────┴─────────────────────┘

2. 언더레이 네트워크 (Underlay) / 라우팅
   - Calico BGP: 각 노드가 파드 IP 대역을 BGP로 광고
   - 장점: 캡슐화 없음, 네이티브 성능
   - 단점: 물리 스위치 BGP 지원 필요

   라우팅 테이블:
   Node 1: 10.244.1.0/24 via 192.168.1.10
   Node 2: 10.244.2.0/24 via 192.168.1.11
   Node 3: 10.244.3.0/24 via 192.168.1.12

3. eBPF 기반 (Cilium)
   - 커널 레벨 패킷 처리
   - iptables 우회 → 10배 이상 성능 향상
   - L7 인식 (HTTP, gRPC) 정책 가능
```

#### [클라우드 + 보안] NetworkPolicy 심층
```
NetworkPolicy 구조 및 동작:

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api-server
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: frontend
        - podSelector:
            matchLabels:
              role: loadbalancer
      ports:
        - protocol: TCP
          port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: database
      ports:
        - protocol: TCP
          port: 5432

동작 원리 (Calico 기준):
1. iptables match-set 규칙 생성
2. IPSet에 허용된 파드 IP 목록 저장
3. 기본 정책 DROP, 명시적 규칙만 ACCEPT

보안 모범 사례:
- Default Deny: 모든 트래픽 차단 후 필요한 것만 허용
- Namespace 격리: 환경(dev/stage/prod)별 별도 정책
- 최소 권한: 포트, 프로토콜 최소화
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 시나리오

#### 시나리오 1: 대규모 마이크로서비스 네트워크 설계
```
요구사항:
- 500개 마이크로서비스
- 일일 10억 요청 처리
- 서비스 간 mTLS 암호화 필수
- 네트워크 레벨 트래픽 가시성 요구

기술사 판단:
1. CNI 선택: Cilium
   - 이유: eBPF 기반 고성능, Hubble 옵저버빌리티 내장
   - kube-proxy 대체 → iptables 오버헤드 제거
   - L7 정책으로 HTTP 메서드 수준 통제 가능

2. Service Mesh: Istio + Cilium 통합
   - Envoy 사이드카 대신 Cilium eBPF로 mTLS
   - 사이드카 오버헤드 제거 (CPU 10-15% 절감)

3. Ingress: Istio Gateway + Envoy
   - 단일 진입점에서 인증, 레이트 리밋, WAF
   - Canary 배포를 위한 트래픽 스플릿

4. 아키텍처:
   [External] → [Istio Gateway] → [Cilium Network] → [Services]
                     │
                     └─ mTLS, Auth, Rate Limit

5. 성능 기대:
   - P99 지연: < 50ms (기존 150ms 대비 67% 감소)
   - 처리량: 100K RPS → 300K RPS (3배 향상)
```

#### 시나리오 2: 하이브리드 클라우드 네트워킹
```
요구사항:
- 온프레미스 K8s + AWS EKS 연결
- 데이터 그래비티로 DB는 온프레미스
- 앱은 AWS에서 실행

기술사 판단:
1. 연결: AWS Direct Connect (1Gbps)
2. CNI: Calico (BGP 지원)
3. 하이브리드 서비스 디스커버리:
   - CoreDNS에 온프레미스 서비스 Forward 구성
   - external-dns로 Route53 동기화

4. 구성:
   ┌─────────────────┐         ┌─────────────────┐
   │   On-Prem K8s   │◀──DC───▶│    AWS EKS      │
   │                 │         │                 │
   │  DB Service     │         │  App Service    │
   │  10.0.0.0/16    │         │  10.244.0.0/16  │
   └─────────────────┘         └─────────────────┘

5. 보안:
   - WireGuard로 오버레이 암호화
   - NetworkPolicy로 크로스 클러스터 통제
```

### 도입 시 고려사항 체크리스트

#### 기술적 고려사항
- [ ] **CNI 선택**: 클러스터 규모, 성능 요구사항, NetworkPolicy 필요성
- [ ] **IP 대역 계획**: 파드 CIDR, Service CIDR 충돌 방지
- [ ] **MTU 설정**: 오버레이 네트워크 시 MTU 조정 (VXLAN: 1450)
- [ ] **DNS 성능**: CoreDNS 리소스, 캐시 TTL, stub domain
- [ ] **kube-proxy 모드**: iptables vs IPVS (대규모는 IPVS 권장)

#### 운영/보안적 고려사항
- [ ] **NetworkPolicy 기본 전략**: Default Deny 적용 여부
- [ ] **트래픽 암호화**: mTLS, WireGuard 필요성
- [ ] **모니터링**: Hubble, Cilium Endpoint 라우팅 가시성
- [ ] **문제 해결**: tcpdump, nslookup, traceroute 활용 방법

### 주의사항 및 안티패턴

#### 안티패턴 1: NodePort를 운영 서비스에 사용
```
잘못된 접근:
- 외부 트래픽을 NodePort로 직접 노출
- 보안 그룹/방화벽 관리 복잡
- 노드 장애 시 해당 노드 포트 접근 불가

올바른 접근:
- 운영은 Ingress + LoadBalancer
- NodePort는 개발/테스트 용도로 제한
- MetalLB (온프레미스)로 LoadBalancer 구현
```

#### 안티패턴 2: CNI 교체 시 데이터 백업 없이 진행
```
잘못된 접근:
- Calico → Cilium 전환 시 그대로 적용
- 파드 네트워크 단절, 클러스터 통신 마비

올바른 접근:
1. 새 노드 풀에 새 CNI로 클러스터 구성
2. 워크로드 점진적 이전 (Rolling Migration)
3. DNS, Service, Ingress 순차 전환
4. 레거시 노드 풀 폐기
```

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 구분 | 기존 (Docker 네트워크) | 쿠버네티스 네트워킹 | 개선효과 |
|-----------|----------------------|-------------------|---------|
| 서비스 디스커버리 시간 | 수동 구성 1시간 | 자동 0초 | -100% |
| IP 관리 오버헤드 | 수동 추적 | CNI 자동 | 인력 90% 감소 |
| 로드밸런싱 설정 | 수동 구성 | Service 자동 | 설정 시간 95% 단축 |
| 네트워크 정책 적용 | 호스트 방화벽 | NetworkPolicy | 선언형 관리 |
| 트래픽 가시성 | 제한적 | Hubble/Jaeger | 100% 추적 가능 |

### 미래 전망 및 진화 방향

#### 1. Gateway API (Ingress 차세대)
- 더 강력한 L7 라우팅 (HTTPRoute, TCPRoute, GRPCRoute)
- 역할 기반 접근 제어 (RBAC 통합)
- 멀티 테넌시 지원 강화
- 예상: 2025년 정식 release

#### 2. eBPF 기반 네트워킹 확산
- iptables 완전 대체
- XDP (eXpress Data Path)로 초저지연 패킷 처리
- 커널 레벨 서비스 메시
- 예상: 2026년 메인스트림

#### 3. 멀티 클러스터 네트워킹
- Submariner, KubeFed로 클러스터 간 서비스 연결
- 글로벌 서비스 디스커버리
- 예상: 엔터프라이즈 표준

### 참고 표준/가이드
- **Kubernetes Network Model**: k8s.io/docs/concepts/cluster-administration/networking/
- **CNI Specification**: github.com/containernetworking/cni
- **NetworkPolicy API**: k8s.io/docs/concepts/services-networking/network-policies/
- **Gateway API**: gateway-api.sigs.k8s.io

---

## 관련 개념 맵 (Knowledge Graph)

1. [쿠버네티스 (Kubernetes)](./kubernetes.md)
   - 관계: K8s의 핵심 네트워킹 모델 구현

2. [서비스 디스커버리 (Service Discovery)](./service_discovery.md)
   - 관계: Service와 CoreDNS로 동적 서비스 탐색

3. [서비스 메시 (Service Mesh)](./service_mesh.md)
   - 관계: mTLS, 트래픽 관리를 위한 추가 계층

4. [CNI (Container Network Interface)](./cni.md)
   - 관계: 파드 네트워크 구성 표준 인터페이스

5. [옵저버빌리티 (Observability)](./observability.md)
   - 관계: 네트워크 트래픽 추적 및 모니터링

6. [네트워크 폴리시 (Network Policy)](./network_policy.md)
   - 관계: 파드 간 통신 보안 정책

---

## 어린이를 위한 3줄 비유 설명

**비유: 스마트 우편 시스템**

쿠버네티스 네트워킹은 아주 똑똑한 우편 배달 시스템 같아요. 각 집(파드)마다 고유 주소가 있어서 어디서든 편지를 보낼 수 있고, '서비스'라는 특별한 우편함을 통해 여러 집 중 한 곳으로 자동으로 배달돼요.

**원리:**
우편 배달부(kube-proxy)는 편지의 주소를 보고 어느 집으로 갈지 정해요. 집이 늘어나거나 줄어들어도 배달부가 알아서 조정해서 편지가 항상 제대로 전달되죠. 보안 요원(NetworkPolicy)은 허락된 사람만 편지를 주고받게 통제해요.

**효과:**
개발자들은 편지가 어떻게 배달되는지 신경 쓰지 않고, 그냥 주소만 쓰면 돼요. 집이 이사 가거나 새 집이 생겨도 우편 시스템이 알아서 처리하니까요!
