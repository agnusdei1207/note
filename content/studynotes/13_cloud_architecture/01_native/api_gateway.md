+++
title = "API 게이트웨이 (API Gateway)"
date = 2024-05-14
description = "마이크로서비스 아키텍처에서 클라이언트와 백엔드 서비스들 사이에 위치하는 단일 진입점으로, 라우팅, 인증, 스로틀링, 로드밸런싱 등 횡단 관심사를 통합 처리하는 프록시 계층"
weight = 100
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["API Gateway", "Kong", "AWS API Gateway", "Nginx", "Reverse Proxy", "Microservices"]
+++

# API 게이트웨이 (API Gateway) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 수많은 마이크로서비스 앞단에 위치하여 클라이언트의 요청을 적절한 서비스로 라우팅하고, 인증/인가, 속도 제한, 로그 수집, 프로토콜 변환 등 **횡단 관심사(Cross-cutting Concerns)**를 중앙 집중화하는 **'통합 프록시'**입니다.
> 2. **가치**: 클라이언트 복잡도 감소(단일 엔드포인트), 보안 정책 중앙화, 트래픽 관리, 서비스 추상화로 **마이크로서비스 운영 효율성을 50% 이상 향상**시킵니다.
> 3. **융합**: Kubernetes Ingress Controller, Service Mesh(Istio Gateway), GraphQL Gateway, Event-Driven Gateway 등 다양한 형태로 진화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

API 게이트웨이는 마이크로서비스 아키텍처에서 클라이언트(웹, 모바일, IoT)와 백엔드 서비스 사이의 단일 진입점 역할을 합니다. 내부적으로 수십, 수백 개의 마이크로서비스가 존재하더라도, 클라이언트는 게이트웨이 하나만 바라봅니다. 게이트웨이는 요청을 받아 적절한 서비스로 전달하고, 응답을 가공하여 클라이언트에게 반환합니다.

**💡 비유**: API 게이트웨이는 **'호텔 프론트 데스크'**와 같습니다. 손님(클라이언트)은 프론트 데스크(게이트웨이)에만 요청하면 됩니다. "룸서비스 주문", "청소 요청", "관광 안내" 등 다양한 요청이 프론트 데스크를 통해 각 부서(서비스)로 전달됩니다. 손님은 어느 부서가 담당하는지 알 필요가 없습니다.

**등장 배경 및 발전 과정**:
1. **클라이언트 복잡도 폭증**: 마이크로서비스가 늘어나면서, 클라이언트가 수십 개의 서비스 엔드포인트를 직접 호출해야 하는 문제가 발생했습니다.
2. **횡단 관심사 중복**: 각 서비스마다 인증, 로깅, 속도 제한을 구현하는 것은 비효율적이었습니다.
3. **Netflix Zuul (2013)**: Netflix가 자사의 스트리밍 서비스를 위해 개발한 API 게이트웨이가 오픈소스화되었습니다.
4. **클라우드 서비스로 정착**: AWS API Gateway, Azure API Management, Google Cloud Endpoints 등 관리형 서비스가 등장했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### API 게이트웨이 핵심 기능

| 기능 | 상세 설명 | 구현 기술 | 비유 |
|---|---|---|---|
| **라우팅 (Routing)** | URL Path 기반 서비스 매핑 | Path Rewrite, Regex | 안내 데스크 |
| **인증/인가 (Auth)** | JWT 검증, OAuth, API Key | IAM, OAuth Server | 신분증 확인 |
| **속도 제한 (Rate Limiting)** | 초당 요청 수 제한 | Token Bucket, Leaky Bucket | 입장 인원 제한 |
| **로드 밸런싱** | 백엔드 서비스 부하 분산 | Round Robin, Weighted | 줄 세우기 |
| **프로토콜 변환** | REST ↔ gRPC, SOAP ↔ REST | Protocol Adapter | 통역사 |
| **응답 캐싱** | 자주 요청되는 응답 캐시 | Redis, In-memory | 빠른 재답변 |
| **서킷 브레이커** | 장애 서비스 격리 | Hystrix, Resilience4j | 비상 차단기 |
| **로그/모니터링** | 요청/응답 로그 수집 | ELK, Prometheus | CCTV |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                      [ API Gateway Architecture ]                           │
└─────────────────────────────────────────────────────────────────────────────┘

     ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
     │   Web    │  │  Mobile  │  │   IoT    │  │  Partner │
     │  Client  │  │   App    │  │ Device   │  │   API    │
     └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
          │             │             │             │
          └─────────────┴──────┬──────┴─────────────┘
                               │ HTTPS
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          [ API Gateway ]                                    │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         Request Pipeline                               │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │ │
│  │  │  SSL    │  │  Auth   │  │  Rate   │  │  Logging│  │ Routing │    │ │
│  │  │Termination│ │ (JWT)  │  │  Limit  │  │         │  │         │    │ │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘    │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                     Backend Service Registry                           │ │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │ │
│  │  │ /api/users/*     │  │ /api/orders/*    │  │ /api/products/*  │   │ │
│  │  │ → user-service   │  │ → order-service  │  │ → product-service│   │ │
│  │  │   :8001          │  │   :8002          │  │   :8003          │   │ │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘   │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                        Cross-Cutting Concerns                          │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │ │
│  │  │Circuit  │  │ Request │  │Response │  │  API    │  │ Service │    │ │
│  │  │Breaker  │  │ Timeout │  │ Transform│ │ Version │  │  Mesh   │    │ │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘    │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         │                            │                            │
         ▼                            ▼                            ▼
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  User Service   │         │ Order Service   │         │ Product Service │
│  (Pod 1..N)     │         │ (Pod 1..N)      │         │ (Pod 1..N)      │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

### 심층 동작 원리: Rate Limiting 알고리즘

```
┌────────────────────────────────────────────────────────────────────────────┐
│                     Rate Limiting Algorithms                               │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ 1. Token Bucket ]                                                       │
│                                                                            │
│     ┌──────────────────────────────────────────────┐                      │
│     │              Bucket (Capacity: 10)           │                      │
│     │  ○ ○ ○ ○ ○ ○ ○ ○ ○ ○                         │                      │
│     │  ▲                              ▲            │                      │
│     │  │ Refill: 2 tokens/sec        │            │                      │
│     │  └──────────────────────────────┘            │                      │
│     └──────────────────────────────────────────────┘                      │
│     Request arrives → Token exists? → Yes: Consume token, proceed         │
│                                → No: Reject (429 Too Many Requests)       │
│                                                                            │
│     장점: 버스트 허용, 효율적                                               │
│     단점: 메모리 필요                                                       │
│                                                                            │
│  [ 2. Leaky Bucket ]                                                       │
│                                                                            │
│     Requests ──► ┌────────────────┐ ──► ┌──────────────┐ ──► Process     │
│                   │  Queue (FIFO)  │     │  Fixed Rate  │                  │
│                   │  [ ][ ][ ][ ]  │     │  (10 req/s)  │                  │
│                   └────────────────┘     └──────────────┘                  │
│                          ↑                                                │
│                    Queue Full? → Reject                                   │
│                                                                            │
│     장점: 일정한 처리 속도                                                   │
│     단점: 버스트 대응 불가                                                   │
│                                                                            │
│  [ 3. Sliding Window Log ]                                                │
│                                                                            │
│     Window: 1 second                                                       │
│     ┌─────────────────────────────────────────────────────────────────┐   │
│     │  Timestamp: [t1, t2, t3, t4, t5]                                │   │
│     │  Current:  t=10                                                │   │
│     │  Window:   t-1 to t (9 to 10)                                  │   │
│     │  Count in window: if < limit → allow, else → reject            │   │
│     └─────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│     장점: 정확한 제어                                                        │
│     단점: 메모리 사용 많음                                                   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: Kong API Gateway 설정

```yaml
# Kong declarative configuration (kong.yml)
_format_version: "3.0"

services:
  - name: user-service
    url: http://user-service.default.svc.cluster.local:8001
    routes:
      - name: user-route
        paths:
          - /api/users
        methods:
          - GET
          - POST
          - PUT
          - DELETE
        strip_path: false
    plugins:
      - name: jwt
        config:
          secret_is_base64: false
      - name: rate-limiting
        config:
          minute: 100
          policy: local
      - name: request-transformer
        config:
          add:
            headers:
              - X-Request-ID:$(uuid)

  - name: order-service
    url: http://order-service.default.svc.cluster.local:8002
    routes:
      - name: order-route
        paths:
          - /api/orders
    plugins:
      - name: jwt
      - name: rate-limiting
        config:
          minute: 50
      - name: correlation-id
        config:
          header_name: X-Correlation-ID
          generator: uuid

  - name: product-service
    url: http://product-service.default.svc.cluster.local:8003
    routes:
      - name: product-route
        paths:
          - /api/products
    plugins:
      - name: key-auth
      - name: rate-limiting
        config:
          minute: 200
      - name: response-cache
        config:
          strategy: memory
          content_type:
            - application/json
          cache_ttl: 60

plugins:
  - name: prometheus
    config:
      per_consumer: true
  - name: file-log
    config:
      path: /var/log/kong/access.log
```

```nginx
# Nginx API Gateway Configuration
upstream user_service {
    least_conn;
    server user-service-1:8001 weight=3;
    server user-service-2:8001 weight=2;
    server user-service-3:8001 backup;
    keepalive 32;
}

upstream order_service {
    least_conn;
    server order-service-1:8002;
    server order-service-2:8002;
    keepalive 32;
}

# Rate limiting zone
limit_req_zone $binary_remote_addr zone=user_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=order_limit:10m rate=5r/s;

server {
    listen 80;
    listen 443 ssl http2;

    # SSL configuration
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # User Service
    location /api/users {
        limit_req zone=user_limit burst=20 nodelay;

        # JWT validation (using auth_request module)
        auth_request /auth/validate;
        auth_request_set $user_id $upstream_http_x_user_id;

        proxy_pass http://user_service;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-User-ID $user_id;
        proxy_set_header Connection "";

        # Timeout settings
        proxy_connect_timeout 5s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;

        # Circuit breaker using upstream checks
        proxy_next_upstream error timeout http_500 http_502 http_503;
        proxy_next_upstream_tries 3;
    }

    # Order Service
    location /api/orders {
        limit_req zone=order_limit burst=10 nodelay;

        auth_request /auth/validate;

        proxy_pass http://order_service;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header Connection "";
    }

    # Health check endpoint
    location /health {
        return 200 "OK";
        add_header Content-Type text/plain;
    }
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: API 게이트웨이 솔루션

| 비교 관점 | Kong | AWS API Gateway | Nginx | Istio Gateway |
|---|---|---|---|---|
| **유형** | 오픈소스/상용 | 관리형 서비스 | 오픈소스 | Service Mesh |
| **운영 복잡도** | 중간 | 낮음 | 높음 | 높음 |
| **기능 완성도** | 높음 | 높음 | 중간 | 높음 |
| **비용** | 오픈소스 무료 | 사용량 기반 | 무료 | 무료 |
| **확장성** | 수동 | 자동 | 수동 | 자동 (K8s) |
| **적합 대상** | 중견~대기업 | 스타트업~대기업 | 소규모 | Kubernetes 환경 |

### 과목 융합 관점 분석

**보안(Security)과의 융합**:
- **OAuth 2.0 / JWT**: 게이트웨이에서 토큰 검증 후 서비스로 전달
- **API Key Management**: 파트너 API용 키 발급/관리
- **WAF (Web Application Firewall)**: SQL Injection, XSS 방어

**네트워크와의 융합**:
- **CDN 통합**: 정적 콘텐츠 캐싱 (CloudFront + API Gateway)
- **DDoS 방어**: 속도 제한, IP 차단

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: API 게이트웨이 도입 의사결정

**문제 상황**: 50개 마이크로서비스를 운영 중이며, 각 서비스마다 인증 로직이 중복 구현되어 있습니다.

**기술사의 전략적 의사결정**:
1. **중앙 집중식 인증**: 게이트웨이에서 JWT 검증, User ID를 헤더로 서비스에 전달
2. **Rate Limiting**: 서비스별로 다른 속도 제한 설정
3. **BFF(Backend for Frontend)**: 모바일, 웹용 별도 게이트웨이 경로

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - Gateway as Monolith**: 게이트웨이에 너무 많은 비즈니스 로직을 담으면 또 다른 모놀리식이 됩니다. 라우팅, 인증, 제한만 담당해야 합니다.
- **체크리스트**:
  - [ ] 인증/인가 방식 결정 (JWT, OAuth, API Key)
  - [ ] Rate Limiting 정책 정의
  - [ ] 장애 격리 전략 (Circuit Breaker)
  - [ ] 로깅/모니터링 통합
  - [ ] Blue-Green 배포 지원 여부

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 게이트웨이 없음 | 게이트웨이 도입 | 개선율 |
|---|---|---|---|
| **인증 코드 중복** | 50개 서비스 | 1개 위치 | 98% 감소 |
| **클라이언트 복잡도** | 50개 엔드포인트 | 1개 엔드포인트 | 98% 감소 |
| **보안 패치 시간** | 50개 서비스 | 1개 위치 | 98% 단축 |

### 미래 전망 및 진화 방향

- **GraphQL Gateway**: 단일 GraphQL 스키마로 여러 REST API 통합
- **Event-Driven Gateway**: WebSocket, SSE, Kafka 통합
- **AI-Powered Gateway**: 이상 트래픽 자동 탐지, 동적 라우팅

### ※ 참고 표준/가이드
- **OpenAPI Specification**: API 계약 표준
- **OAuth 2.0 / OIDC**: 인증 표준
- **Envoy Proxy**: CNCF 표준 프록시

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [마이크로서비스 아키텍처 (MSA)](@/studynotes/13_cloud_architecture/01_native/msa.md) : API 게이트웨이의 상위 아키텍처
- [서비스 메시 (Service Mesh)](@/studynotes/13_cloud_architecture/01_native/service_mesh.md) : 게이트웨이의 진화형
- [BFF (Backend for Frontend)](@/studynotes/13_cloud_architecture/01_native/bff.md) : 클라이언트별 게이트웨이
- [로드 밸런서](@/studynotes/13_cloud_architecture/03_virt/load_balancer.md) : 트래픽 분산 기술
- [OAuth 2.0 / JWT](@/studynotes/13_cloud_architecture/01_native/oauth_jwt.md) : 인증 기술

---

### 👶 어린이를 위한 3줄 비유 설명
1. API 게이트웨이는 **'호텔 프론트 데스크'**예요. 손님은 프론트에만 말하면 돼요.
2. "룸서비스요!", "청소해주세요!" 하면 **'프론트가 알아서 담당 부서로 연결'**해줘요.
3. 그리고 **'너무 많은 손님이 몰리면 줄을 세워요'**. 한꺼번에 다 들어가면 호텔이 버티지 못하니까요!
