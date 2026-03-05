+++
title = "서비스 메시 (Service Mesh)"
date = 2024-05-19
description = "마이크로서비스 간 통신을 투명하게 관리하는 인프라 계층으로, 사이드카 프록시를 통해 라우팅, 보안(mTLS), 관측성을 제공"
weight = 20
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Service Mesh", "Istio", "Envoy", "Sidecar", "mTLS", "Microservices", "Traffic Management"]
+++

# 서비스 메시 (Service Mesh) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 마이크로서비스 환경에서 서비스 간 통신( East-West Traffic)을 전담하는 전용 인프라 계층으로, 비즈니스 코드와 완전히 분리된 사이드카 프록시(Sidecar Proxy)를 통해 라우팅, 로드 밸런싱, 암호화(mTLS), 인증, 관측성을 투명하게 제공합니다.
> 2. **가치**: 수백 개의 마이크로서비스에서 발생하는 통신 복잡성을 **중앙 집중식 제어 평면(Control Plane)**으로 통합 관리하며, **Zero Trust 보안**(mTLS), **카나리 배포**, **서킷 브레이커**, **속도 제한**을 애플리케이션 수정 없이 구현합니다.
> 3. **융합**: 쿠버네티스와 깊게 통합되어 Istio, Linkerd, Consul Connect 등이 구현체로 활용되며, GitOps, Observability Stack(Prometheus, Jaeger)과 결합하여 클라우드 네이티브 운영의 핵심 인프라가 됩니다.

---

## Ⅰ. 개요 (Context & Background)

서비스 메시(Service Mesh)는 마이크로서비스 아키텍처에서 서비스 간 통신을 처리하기 위한 전용 인프라 계층입니다. 각 서비스 인스턴스 옆에 프록시(Sidecar)를 배치하고, 이 모든 프록시를 중앙 제어 평면(Control Plane)에서 관리합니다.

**💡 비유**: 서비스 메시는 **'호텔 컨시어지 팀'**과 같습니다. 각 객실(서비스)에는 전용 비서(사이드카 프록시)가 배치됩니다. 투숙객(서비스 A)이 다른 객실의 투숙객(서비스 B)에게 메시지를 보내려면, 비서가 대신 전달합니다. 비서는 암호화, 우회 경로, 도착 확인, 속도 조절 등을 알아서 처리합니다. 컨시어지 데스크(제어 평면)는 모든 비서에게 규칙을 전달합니다.

**등장 배경 및 발전 과정**:
1. **마이크로서비스의 통신 지옥**: 서비스가 수백 개로 늘어나면 서비스 간 호출이 복잡해지고, 장애 전파, 보안, 모니터링이 불가능해졌습니다.
2. **라이브러리 접근의 한계**: Netflix Ribbon/Hystrix 등을 각 언어별로 구현해야 했고, 코드 침투적이었습니다.
3. **Envoy와 Istio의 등장 (2016~2017)**: Lyft가 Envoy 프록시를, Google/IBM이 Istio를 오픈소스화하며 서비스 메시 개념을 정립했습니다.
4. **CNCF 생태계 통합**: 서비스 메시가 클라우드 네이티브 아키텍처의 필수 구성 요소로 자리 잡았습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: 서비스 메시 아키텍처

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 대표 구현체 | 비유 |
|---|---|---|---|---|
| **데이터 평면 (Data Plane)** | 실제 트래픽 처리 | 프록시가 모든 IN/OUT 트래픽 가로챔 | Envoy, Linkerd-proxy | 현장 비서 |
| **사이드카 (Sidecar)** | Pod 내 프록시 컨테이너 | iptables로 트래픽 리다이렉트 | Envoy Container | 전용 비서 |
| **제어 평면 (Control Plane)** | 정책 배포 및 관리 | xDS API로 프록시에 설정 전파 | Istiod, Linkerd-control | 컨시어지 데스크 |
| **Pilot** | 서비스 디스커버리 | 서비스 레지스트리 → Envoy EDS | Istiod | 안내 데스크 |
| **Citadel** | 인증서 관리 | mTLS 인증서 발급/순환 | Istiod | 보안실 |
| **Mixer** (deprecated) | 정책 및 원격 측정 | Telemetry 수집 | Istiod 통합 | 감사팀 |
| **Galley** (deprecated) | 설정 검증 | YAML 검증 | Istiod 통합 | 문서 검토 |

### 정교한 구조 다이어그램: Istio 서비스 메시 아키텍처

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Istio Service Mesh Architecture ]                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        [ Control Plane (Istiod) ]                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │   Pilot     │  │  Citadel    │  │  Galley     │  │  Injector   │       │
│  │             │  │  (mTLS CA)  │  │  (Config)   │  │  (Sidecar)  │       │
│  │ - Service   │  │             │  │             │  │             │       │
│  │   Discovery │  │ - Cert      │  │ - Validate  │  │ - Auto      │       │
│  │ - Traffic   │  │   Issuance  │  │   Config    │  │   Inject    │       │
│  │   Mgmt      │  │ - Rotation  │  │             │  │             │       │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │
│         │                │                │                │               │
│         └────────────────┴────────────────┴────────────────┘               │
│                                   │                                         │
│                          xDS API (gRPC)                                     │
│                         (EDS, CDS, LDS, RDS)                                │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
    ┌───────────────────────────────┼───────────────────────────────┐
    │                               │                               │
    ▼                               ▼                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          [ Data Plane (Kubernetes Cluster) ]                 │
│                                                                             │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐  │
│  │         Pod: Service A          │  │         Pod: Service B          │  │
│  │  ┌───────────────────────────┐  │  │  ┌───────────────────────────┐  │  │
│  │  │     Application Container │  │  │  │     Application Container │  │  │
│  │  │        (Port 8080)        │  │  │  │        (Port 8080)        │  │  │
│  │  │                           │  │  │  │                           │  │  │
│  │  │  ┌─────┐    ┌─────┐      │  │  │  │  ┌─────┐    ┌─────┐      │  │  │
│  │  │  │ App │◄──►│App  │      │  │  │  │  │ App │◄──►│App  │      │  │  │
│  │  │  │Code │    │Logic│      │  │  │  │  │Code │    │Logic│      │  │  │
│  │  │  └─────┘    └─────┘      │  │  │  │  └─────┘    └─────┘      │  │  │
│  │  └───────────────────────────┘  │  │  └───────────────────────────┘  │  │
│  │                ▲                │  │                ▲                │  │
│  │                │ (Localhost)    │  │                │ (Localhost)    │  │
│  │                ▼                │  │                ▼                │  │
│  │  ┌───────────────────────────┐  │  │  ┌───────────────────────────┐  │  │
│  │  │   Istio Proxy (Envoy)     │  │  │  │   Istio Proxy (Envoy)     │  │  │
│  │  │      (Sidecar)            │  │  │  │      (Sidecar)            │  │  │
│  │  │                           │  │  │  │                           │  │  │
│  │  │  - Inbound Listener       │  │  │  │  - Inbound Listener       │  │  │
│  │  │  - Outbound Listener      │  │  │  │  - Outbound Listener      │  │  │
│  │  │  - mTLS Termination       │  │  │  │  - mTLS Termination       │  │  │
│  │  │  - Load Balancing         │  │  │  │  - Load Balancing         │  │  │
│  │  │  - Circuit Breaking       │  │  │  │  - Circuit Breaking       │  │  │
│  │  │  - Retries / Timeouts     │  │  │  │  - Retries / Timeouts     │  │  │
│  │  └─────────────┬─────────────┘  │  │  └─────────────▲─────────────┘  │  │
│  └────────────────┼────────────────┘  └────────────────┼────────────────┘  │
│                   │                                    │                    │
│                   │        mTLS Encrypted              │                    │
│                   │        ─────────────────►          │                    │
│                   │        (Service-to-Service)        │                    │
│                   └────────────────────────────────────┘                    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Traffic Flow (In-Mesh)                            │   │
│  │                                                                      │   │
│  │  [Client] ──► [Ingress Gateway] ──► [Service A Envoy] ──►           │   │
│  │                                              │                      │   │
│  │                                              │ mTLS                 │   │
│  │                                              ▼                      │   │
│  │                                      [Service B Envoy] ──► [Service B]│   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: Envoy 프록시 트래픽 처리

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    Envoy Sidecar Proxy Internal Flow                        │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ Outbound Traffic: Service A → Service B ]                               │
│                                                                            │
│  Application in Service A                                                  │
│  ┌────────────────────────────┐                                            │
│  │  HTTP Request:             │                                            │
│  │  GET http://service-b/api  │                                            │
│  └─────────────┬──────────────┘                                            │
│                │                                                            │
│                │ 1. iptables REDIRECT (15001)                              │
│                ▼                                                            │
│  ┌────────────────────────────┐                                            │
│  │     Envoy (Sidecar)        │                                            │
│  │                            │                                            │
│  │  ┌──────────────────────┐  │                                            │
│  │  │ Outbound Listener    │  │  ◄── Port 15001                           │
│  │  │ (Virtual Listener)   │  │                                            │
│  │  └──────────┬───────────┘  │                                            │
│  │             │              │                                            │
│  │  ┌──────────▼───────────┐  │                                            │
│  │  │ Route Configuration  │  │  ◄── VirtualService Rules                  │
│  │  │ - Match: /api/*      │  │                                            │
│  │  │ - Route: service-b   │  │                                            │
│  │  └──────────┬───────────┘  │                                            │
│  │             │              │                                            │
│  │  ┌──────────▼───────────┐  │                                            │
│  │  │ Cluster (Service B)  │  │  ◄── DestinationRule                       │
│  │  │ - Endpoints: 3 pods  │  │      (Subsets, LB Policy)                  │
│  │  │ - LB: ROUND_ROBIN    │  │                                            │
│  │  └──────────┬───────────┘  │                                            │
│  │             │              │                                            │
│  │  ┌──────────▼───────────┐  │                                            │
│  │  │ mTLS Encryption      │  │  ◄── Citadel Certificate                   │
│  │  │ - Client Cert        │  │                                            │
│  │  │ - Server CA Verify   │  │                                            │
│  │  └──────────┬───────────┘  │                                            │
│  │             │              │                                            │
│  └─────────────┼──────────────┘                                            │
│                │                                                            │
│                │ 2. Encrypted HTTP/2 over mTLS                             │
│                ▼                                                            │
│  ┌────────────────────────────┐                                            │
│  │     Envoy (Service B)      │                                            │
│  │                            │                                            │
│  │  ┌──────────────────────┐  │                                            │
│  │  │ Inbound Listener     │  │  ◄── Port 15006                           │
│  │  │ - mTLS Termination   │  │                                            │
│  │  │ - Auth Policy Check  │  │                                            │
│  │  └──────────┬───────────┘  │                                            │
│  │             │              │                                            │
│  │  ┌──────────▼───────────┐  │                                            │
│  │  │ Local Forward        │  │                                            │
│  │  │ → localhost:8080     │  │                                            │
│  │  └──────────┬───────────┘  │                                            │
│  │             │              │                                            │
│  └─────────────┼──────────────┘                                            │
│                │                                                            │
│                ▼                                                            │
│  Application in Service B (Port 8080)                                      │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: Istio Traffic Management 구성

```yaml
# 1. Gateway: 인그레스 트래픽 진입점
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: api-gateway
  namespace: production
spec:
  selector:
    istio: ingressgateway  # Istio 기본 Ingress Gateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: api-tls-secret  # Kubernetes Secret
    hosts:
    - "api.example.com"
  - port:
      number: 80
      name: http
      protocol: HTTP
    tls:
      httpsRedirect: true  # HTTP → HTTPS 리다이렉트
    hosts:
    - "api.example.com"

---
# 2. VirtualService: 라우팅 규칙
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-service
  namespace: production
spec:
  hosts:
  - "api.example.com"
  gateways:
  - api-gateway
  http:
  # 카나리 배포: 90% v1, 10% v2
  - match:
    - uri:
        prefix: "/api/v1/users"
    route:
    - destination:
        host: user-service
        subset: v1
      weight: 90
    - destination:
        host: user-service
        subset: v2
      weight: 10

    # 타임아웃 및 재시도
    timeout: 30s
    retries:
      attempts: 3
      perTryTimeout: 10s
      retryOn: gateway-error,connect-failure,refused-stream

    # 결함 주입 (테스트용)
    # fault:
    #   delay:
    #     percentage:
    #       value: 10
    #     fixedDelay: 5s
    #   abort:
    #     percentage:
    #       value: 5
    #     httpStatus: 500

  # 헤더 기반 라우팅 (A/B 테스트)
  - match:
    - uri:
        prefix: "/api/v1/feature"
      headers:
        x-canary:
          exact: "true"
    route:
    - destination:
        host: feature-service
        subset: canary

---
# 3. DestinationRule: 서브셋 및 로드 밸런싱
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: user-service
  namespace: production
spec:
  host: user-service
  trafficPolicy:
    # 연결 풀 설정
    connectionPool:
      tcp:
        maxConnections: 100
        connectTimeout: 5s
      http:
        h2UpgradePolicy: UPGRADE
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000

    # 아웃라이어 탐지 (서킷 브레이커)
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 25

    # TLS 설정
    tls:
      mode: ISTIO_MUTUAL  # mTLS

  # 서브셋 정의
  subsets:
  - name: v1
    labels:
      version: v1
    trafficPolicy:
      loadBalancer:
        simple: ROUND_ROBIN

  - name: v2
    labels:
      version: v2
    trafficPolicy:
      loadBalancer:
        simple: LEAST_REQUEST

---
# 4. PeerAuthentication: mTLS 강제
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT  # 모든 메시 내 통신에 mTLS 강제

---
# 5. AuthorizationPolicy: 접근 제어
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: user-service-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: user-service
  rules:
  # 프론트엔드 서비스에서만 접근 허용
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/frontend-service"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/v1/users/*"]

  # 관리자 서비스는 모든 작업 허용
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/admin-service"]

  # 그 외 모든 요청 거부 (기본 정책)
  - {}

---
# 6. ServiceEntry: 외부 서비스 등록
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: external-api
spec:
  hosts:
  - "external-api.example.com"
  location: MESH_EXTERNAL
  ports:
  - number: 443
    name: https
    protocol: HTTPS
  resolution: DNS

---
# 7. EnvoyFilter: 커스텀 Envoy 설정 (고급)
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: custom-lua-filter
  namespace: production
spec:
  configPatches:
  - applyTo: HTTP_FILTER
    match:
      context: SIDECAR_INBOUND
    patch:
      operation: INSERT_BEFORE
      value:
        name: envoy.lua
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.http.lua.v3.Lua
          default_source_code:
            inline_string: |
              function envoy_on_request(request_handle)
                request_handle:logInfo("Custom Lua filter executed")
              end
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 서비스 메시 구현체

| 비교 관점 | Istio | Linkerd | Consul Connect | AWS App Mesh |
|---|---|---|---|---|
| **제어 평면** | Istiod (Go) | Linkerd-control (Rust) | Consul (Go) | App Mesh Controller |
| **데이터 평면** | Envoy (C++) | Linkerd-proxy (Rust) | Envoy | Envoy |
| **복잡성** | 높음 (풀 기능) | 낮음 (단순함) | 중간 | 중간 |
| **리소스 사용** | 높음 | 낮음 (~10MB) | 중간 | 중간 |
| **mTLS** | 자동 (SPIFFE) | 자동 | 자동 | ACM 인증서 |
| **관측성** | Kiali, Jaeger | 자체 대시보드 | Consul UI | X-Ray |
| **학습 곡선** | 가파름 | 완만함 | 중간 | 중간 |
| **적합한 규모** | 대규모 엔터프라이즈 | 중소규모 | HashiCorp 스택 | AWS 환경 |

### 과목 융합 관점 분석

**보안(Security)과의 융합**:
- **Zero Trust Network**: 서비스 간 모든 통신이 mTLS로 암호화되며, 서비스 ID(SPIFFE) 기반 인증
- **세분화된 접근 제어**: AuthorizationPolicy로 서비스/메서드/경로 단위 접근 통제
- **인증서 자동 순환**: Citadel이 mTLS 인증서를 자동으로 발급/갱신

**네트워크와의 융합**:
- **L7 로드 밸런싱**: HTTP/HTTP2/gRPC 트래픽의 지능형 분산
- **서비스 디스커버리**: DNS 기반 서비스 검색과 로드 밸런싱 통합
- **트래픽 미러링(Shadowing)**: 프로덕션 트래픽을 테스트 환경으로 복제

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 서비스 메시 도입 결정

**문제 상황**: 핀테크 기업 E사는 50개의 마이크로서비스를 운영 중입니다. 서비스 간 통신 보안, 카나리 배포, 장애 격리가 필요합니다.

**기술사의 전략적 의사결정**:

1. **요구사항 분석**:

   | 요구사항 | 현재 상태 | 목표 |
   |---|---|---|
   | 서비스 간 보안 | 없음 (평문) | mTLS 강제 |
   | 카나리 배포 | 수동 | 자동 트래픽 분할 |
   | 장애 격리 | 없음 | 서킷 브레이커 |
   | 관측성 | 로그만 | 분산 추적 |
   | 운영 복잡성 | 중간 | 최소화 |

2. **옵션 평가**:

   | 옵션 | 장점 | 단점 | 추천 |
   |---|---|---|---|
   | **Istio** | 풀 기능, 강력한 정책 | 복잡성, 리소스 | 대규모 |
   | **Linkerd** | 단순함, 경량 | 기능 제한적 | **중소규모** |
   | **라이브러리** (Hystrix) | 제어 용이 | 언어별 구현 | 비추천 |

3. **추천**: **Linkerd** 채택
   - 이유: 50개 서비스는 중간 규모, 운영 단순성 우선, Rust 기반 경량 프록시

4. **단계적 도입**:
   - Phase 1: 개발 환경에 Linkerd 설치 및 검증 (2주)
   - Phase 2: 비핵심 서비스 5개에 적용 (4주)
   - Phase 3: 전체 서비스로 확장 (8주)

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - Over-Engineering**: 모든 기능을 한 번에 적용하려 하지 말고, 핵심 기능(mTLS, 관측성)부터 시작해야 합니다.

- **안티패턴 - Ignoring Resource Overhead**: 사이드카 프록리가 CPU/메모리를 추가로 소모합니다. 리소스 계획에 반영해야 합니다.

- **체크리스트**:
  - [ ] 서비스 메시 도입 목표 명확화
  - [ ] 리소스 오버헤드 측정 (사이드카당 ~100MB)
  - [ ] 기존 인프라와의 호환성 확인
  - [ ] 롤백 계획 수립
  - [ ] 팀 교육 계획

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 도입 전 | 서비스 메시 도입 후 | 개선율 |
|---|---|---|---|
| **보안 (mTLS)** | 없음 | 모든 통신 암호화 | 100% 향상 |
| **MTTD (평균 탐지 시간)** | 30분 | 5분 | 83% 단축 |
| **배포 안정성** | 90% | 99.5% | 10% 향상 |
| **장애 전파** | 빈번 | 격리됨 | 90% 감소 |

### 미래 전망 및 진화 방향

- **eBPF 기반 서비스 메시**: 커널 레벨에서 트래픽 처리 (Cilium Service Mesh)
- **멀티 클러스터 서비스 메시**: 여러 클러스터 간 통합 관리
- **AI 기반 트래픽 관리**: 이상 탐지 및 자동 대응

### ※ 참고 표준/가이드
- **SPIFFE (Secure Production Identity Framework For Everyone)**: 서비스 ID 표준
- **Envoy xDS API**: 프록시 설정 API 표준
- **CNCF Service Mesh Interface (SMI)**: 서비스 메시 인터페이스 표준

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [마이크로서비스 아키텍처 (MSA)](@/studynotes/13_cloud_architecture/01_native/msa.md) : 서비스 메시가 적용되는 아키텍처
- [쿠버네티스](@/studynotes/13_cloud_architecture/01_native/kubernetes.md) : 서비스 메시의 기반 플랫폼
- [사이드카 패턴](@/studynotes/13_cloud_architecture/01_native/sidecar_pattern.md) : 서비스 메시의 핵심 디자인 패턴
- [mTLS](@/studynotes/12_security/03_authentication/mtls.md) : 서비스 간 상호 TLS 인증
- [분산 추적](@/studynotes/15_devops_sre/02_observability/distributed_tracing.md) : 서비스 메시 관측성

---

### 👶 어린이를 위한 3줄 비유 설명
1. 서비스 메시는 **'호텔 컨시어지 팀'**이에요. 각 객실(서비스)에 비서(프록시)가 있어서, 모든 연락을 대신 처리해줘요.
2. 비서가 **'암호화, 우편 배달 추적, 속도 조절'**을 알아서 해줘요. 투숙객(개발자)은 비즈니스에만 집중하면 돼요.
3. 덕분에 **'안전하고 원활한 소통'**이 가능해요. 누가 누구와 대화하는지, 어디서 문제가 생겼는지 한눈에 볼 수 있어요!
