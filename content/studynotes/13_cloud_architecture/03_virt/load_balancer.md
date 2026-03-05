+++
title = "로드 밸런서 (Load Balancer)"
date = 2024-05-14
description = "트래픽을 여러 서버에 분산시켜 가용성과 성능을 향상시키는 네트워크 장비 또는 소프트웨어의 동작 원리와 알고리즘"
weight = 80
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Load Balancer", "L4", "L7", "ALB", "NLB", "HAProxy", "Nginx", "Reverse Proxy"]
+++

# 로드 밸런서 (Load Balancer) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 들어오는 네트워크 트래픽을 여러 백엔드 서버에 균등하게 분산시켜 단일 서버의 과부하를 방지하고, 서버 장애 시 자동으로 건강한 서버로 라우팅하여 **고가용성(High Availability)**과 **확장성(Scalability)**을 동시에 달성하는 네트워크 인프라 컴포넌트입니다.
> 2. **가치**: 단일 서버 대비 **가용성 99%→99.99% 향상**, **트래픽 처리량 10배 이상 증가**, **무중단 배포 가능**, **SSL 종료로 서버 부하 감소** 등의 이점을 제공하며, 수평적 확장(Scale-out)의 핵심 인프라입니다.
> 3. **융합**: L4(TCP/UDP)와 L7(HTTP) 계층 로드 밸런싱, 오토 스케일링, 헬스 체크, 세션 유지, 서비스 디스커버리와 결합하여 클라우드 네이티브 아키텍처의 필수 구성요소입니다.

---

## Ⅰ. 개요 (Context & Background)

로드 밸런서(Load Balancer)는 클라이언트와 서버 그룹 사이에 위치하여 들어오는 요청을 여러 서버에 분배하는 장치입니다. OSI 7계층 중 어느 계층에서 동작하느냐에 따라 L4(전송 계층)와 L7(애플리케이션 계층) 로드 밸런서로 구분됩니다.

**💡 비유**: 로드 밸런서는 **'은행의 번호표 기계'**와 같습니다. 은행에 손님(요청)이 많이 오면 번호표 기계(로드 밸런서)가 각 창구(서버)로 손님을 고르게 분배합니다. 어떤 창구가 휴식(서버 장애) 중이면 다른 창구로 안내합니다. 덕분에 한 창구에만 줄이 생기지 않고, 모든 창구가 효율적으로 일할 수 있습니다.

**등장 배경 및 발전 과정**:
1. **단일 서버의 한계**: 초기 웹 서버는 단일 머신으로 운영되어 트래픽 증가 시 쉽게 다운되었습니다.
2. **DNS Round Robin (1990년대)**: DNS가 여러 IP를 순환 반환하는 가장 원시적인 로드 밸런싱이었습니다.
3. **하드웨어 로드 밸런서 (1990년대~)**: F5, Citrix NetScaler 등 전용 하드웨어가 등장했습니다.
4. **소프트웨어 로드 밸런서 (2000년대~)**: HAProxy, Nginx, Apache 등 소프트웨어 기반이 대중화되었습니다.
5. **클라우드 로드 밸런서 (2010년대~)**: AWS ALB/NLB, Azure Load Balancer, GCP Cloud Load Balancing이 서비스로 제공됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: 로드 밸런서 핵심 기능

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | OSI 계층 | 비유 |
|---|---|---|---|---|
| **리스너(Listener)** | 클라이언트 요청 수신 | 포트/프로토콜 바인딩 | L4/L7 | 접수대 |
| **타겟 그룹(Target Group)** | 백엔드 서버 그룹 | 인스턴스/IP 등록 | - | 창구들 |
| **헬스 체크(Health Check)** | 서버 상태 모니터링 | HTTP/TCP 프로브 | L4/L7 | 건강 검진 |
| **스케줄러(Scheduler)** | 분산 알고리즘 | RR, WRR, LC, Hash | L4 | 배정 알고리즘 |
| **세션 지속성(Session Persistence)** | 세션 유지 | Source IP Hash, Cookie | L7 | 단골 손님 기억 |
| **SSL 종료(Termination)** | 암호화 해제 | 인증서 관리 | L6/L7 | 보안 게이트 |

### 정교한 구조 다이어그램: L4 vs L7 로드 밸런서

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Load Balancer Architecture ]                            │
│                    (L4 vs L7 Comparison)                                    │
└─────────────────────────────────────────────────────────────────────────────┘

                    [ Clients ]
           ┌─────────────┬─────────────┬─────────────┐
           │   Client 1  │   Client 2  │   Client 3  │
           └──────┬──────┴──────┬──────┴──────┬──────┘
                  │             │             │
                  └─────────────┼─────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          L4 Load Balancer (Transport Layer)                  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                       Decision Based On:                              │  │
│  │                                                                       │  │
│  │    - Source IP:Port ───────────────────────────────────────────┐     │  │
│  │    - Destination IP:Port ──────────────────────────────────────┤     │  │
│  │    - Protocol (TCP/UDP) ───────────────────────────────────────┘     │  │
│  │                                                                       │  │
│  │    장점: 빠름 (패킷 페이로드 검사 안 함)                              │  │
│  │    단점: 콘텐츠 기반 라우팅 불가능                                    │  │
│  │                                                                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│         [ TCP Packet ]                                                      │
│         ┌───────────────────────────────────────┐                          │
│         │ IP Header │ TCP Header │ Payload     │                          │
│         │ Src:Port  │ Dst:Port   │ (암호화됨)  │  ◄── L4는 여기까지만     │
│         └───────────────────────────────────────┘      확인               │
│                                │                                           │
│                                ▼                                           │
│         ┌─────────────────────────────────────────────────────────┐       │
│         │                   Load Balancing Algorithms             │       │
│         │                                                         │       │
│         │  Round Robin: Server1 → Server2 → Server3 → Server1... │       │
│         │  Least Connections: 가장 적은 연결을 가진 서버 선택      │       │
│         │  Source IP Hash: 클라이언트 IP → 특정 서버 매핑         │       │
│         └─────────────────────────────────────────────────────────┘       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          L7 Load Balancer (Application Layer)                │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                       Decision Based On:                              │  │
│  │                                                                       │  │
│  │    - HTTP Method (GET, POST, PUT, DELETE)                            │  │
│  │    - URL Path (/api/v1/users, /products, /checkout)                  │  │
│  │    - HTTP Headers (Host, User-Agent, Cookie)                         │  │
│  │    - Query Parameters (?category=electronics)                        │  │
│  │    - Request Body (JSON payload)                                      │  │
│  │                                                                       │  │
│  │    장점: 콘텐츠 기반 스마트 라우팅 가능                                │  │
│  │    단점: 패킷 검사로 인한 오버헤드                                     │  │
│  │                                                                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│         [ HTTP Request ]                                                    │
│         ┌─────────────────────────────────────────────────────────┐       │
│         │ POST /api/v1/checkout HTTP/1.1                         │       │
│         │ Host: api.example.com                                   │       │
│         │ Content-Type: application/json                          │       │
│         │ Cookie: session_id=abc123                               │       │
│         │                                                         │       │
│         │ {"items": [...], "payment_method": "credit_card"}       │  ◄──  │
│         └─────────────────────────────────────────────────────────┘  L7는│
│                                │                                     전체 │
│                                ▼                                     확인 │
│         ┌─────────────────────────────────────────────────────────┐       │
│  Path │ /api/v1/users/*    │→│ User Service (Port 8080)           │       │
│  Based│ /api/v1/products/* │→│ Product Service (Port 8081)        │       │
│  Rou- │ /api/v1/checkout   │→│ Order Service (Port 8082)          │       │
│  ting │ /static/*          │→│ CDN / Static Server (Port 80)      │       │
│       └─────────────────────────────────────────────────────────┘       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
         ┌───────────┐   ┌───────────┐   ┌───────────┐
         │  Server 1 │   │  Server 2 │   │  Server 3 │
         │  (Web)    │   │  (Web)    │   │  (Web)    │
         │  Health: ✓│   │  Health: ✓│   │  Health: ✓│
         └───────────┘   └───────────┘   └───────────┘


[ Load Balancing Algorithms ]

┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  1. Round Robin (라운드 로빈)                                                │
│     ┌────┐   ┌────┐   ┌────┐                                               │
│     │ S1 │ → │ S2 │ → │ S3 │ → (반복)                                       │
│     └────┘   └────┘   └────┘                                               │
│     모든 서버에 동일하게 분배                                                │
│                                                                              │
│  2. Weighted Round Robin (가중 라운드 로빈)                                  │
│     ┌────┐   ┌────┐   ┌────┐                                               │
│     │ S1 │ → │ S2 │ → │ S3 │                                               │
│     │ W=5│   │ W=3│   │ W=2│                                               │
│     └────┘   └────┘   └────┘                                               │
│     S1: 50%, S2: 30%, S3: 20% 분배 (서버 성능 고려)                          │
│                                                                              │
│  3. Least Connections (최소 연결)                                           │
│     ┌────┐   ┌────┐   ┌────┐                                               │
│     │ S1 │   │ S2 │   │ S3 │                                               │
│     │ C=5│   │ C=2│   │ C=8│  → 새 요청은 S2로 (가장 적은 연결)            │
│     └────┘   └────┘   └────┘                                               │
│     현재 연결 수가 가장 적은 서버 선택                                        │
│                                                                              │
│  4. IP Hash (IP 해시)                                                       │
│     Client IP → Hash Function → Server Selection                            │
│     192.168.1.10 → Hash("192.168.1.10") % 3 → Server 1                     │
│     동일 클라이언트는 항상 동일 서버로 (세션 유지)                            │
│                                                                              │
│  5. URL Hash (URL 해시)                                                     │
│     URL Path → Hash Function → Server Selection                             │
│     /api/users → Hash("/api/users") % 3 → Server 2                         │
│     캐싱 최적화에 유용                                                        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: 헬스 체크와 장애 조치

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    Health Check & Failover Mechanism                        │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ Health Check Configuration ]                                            │
│                                                                            │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  Protocol: HTTP                                                     │   │
│  │  Path: /health                                                      │   │
│  │  Interval: 30s (30초마다 검사)                                      │   │
│  │  Timeout: 5s (5초 내 응답 없으면 실패)                              │   │
│  │  Healthy Threshold: 2 (2회 연속 성공 시 정상)                       │   │
│  │  Unhealthy Threshold: 3 (3회 연속 실패 시 비정상)                   │   │
│  │  Expected Response: 200 OK                                          │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  [ Health Check Timeline ]                                                 │
│                                                                            │
│  Time │ S1 Status │ S2 Status │ S3 Status │ Action                        │
│  ─────┼───────────┼───────────┼───────────┼────────────────────────       │
│   0s  │    ✓      │    ✓      │    ✓      │ Normal operation             │
│  30s  │    ✓      │    ✓      │    ✓      │ Normal                       │
│  60s  │    ✓      │    ✗      │    ✓      │ S2: 1st failure              │
│  90s  │    ✓      │    ✗      │    ✓      │ S2: 2nd failure              │
│  120s │    ✓      │    ✗      │    ✓      │ S2: 3rd failure → REMOVE     │
│       │           │           │           │ Traffic → S1, S3 only        │
│  150s │    ✓      │    ✗      │    ✓      │ S2 still unhealthy           │
│  180s │    ✓      │    ✓      │    ✓      │ S2 recovered! 1st success    │
│  210s │    ✓      │    ✓      │    ✓      │ S2: 2nd success → RESTORE    │
│       │           │           │           │ Traffic → S1, S2, S3 again   │
│                                                                            │
│  [ Traffic Routing After Failover ]                                        │
│                                                                            │
│  Before Failover:                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  Traffic: 33.3% → S1, 33.3% → S2, 33.3% → S3                       │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  After S2 Removal:                                                         │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  Traffic: 50% → S1, 50% → S3                                       │   │
│  │  (S2 is marked UNHEALTHY and removed from rotation)               │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  After S2 Recovery:                                                        │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  Traffic: 33.3% → S1, 33.3% → S2, 33.3% → S3                       │   │
│  │  (S2 is marked HEALTHY and added back to rotation)                │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: Nginx 로드 밸런서 구성

```nginx
# Nginx Load Balancer Configuration

# 1. 업스트림 서버 그룹 정의 (백엔드 서버)
upstream backend_servers {
    # 로드 밸런싱 알고리즘 (기본: Round Robin)
    # least_conn;          # 최소 연결 알고리즘
    # ip_hash;             # IP 해시 (세션 유지)
    # hash $request_uri;   # URL 해시

    # 가중 라운드 로빈 (서버 성능 차이 고려)
    server 10.0.1.10:8080 weight=5;
    server 10.0.1.11:8080 weight=3;
    server 10.0.1.12:8080 weight=2;

    # 백업 서버 (모든 기본 서버 다운 시 사용)
    server 10.0.1.13:8080 backup;

    # 헬스 체크 (Nginx Plus 기능, 오픈소스는 passive check)
    # health_check interval=30s fails=3 passes=2;

    # 연결 유지 (Keep-Alive)
    keepalive 32;

    # 최대 실패 횟수와 타임아웃
    server 10.0.1.14:8080 max_fails=3 fail_timeout=30s;
}

# 2. API 서버 그룹 (경로 기반 라우팅용)
upstream api_servers {
    least_conn;
    server 10.0.2.10:8080;
    server 10.0.2.11:8080;
    server 10.0.2.12:8080;

    keepalive 16;
}

# 3. 메인 서버 블록
server {
    listen 80;
    listen 443 ssl http2;
    server_name api.example.com;

    # SSL 설정
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    # 보안 헤더
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # 액세스 로그
    access_log /var/log/nginx/access.log combined;
    error_log /var/log/nginx/error.log warn;

    # 4. 경로 기반 라우팅 (L7 로드 밸런싱)
    location / {
        proxy_pass http://backend_servers;

        # 프록시 헤더 설정
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 타임아웃 설정
        proxy_connect_timeout 10s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # 연결 유지
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        # 버퍼링
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }

    # API 경로는 별도 서버 그룹으로
    location /api/ {
        proxy_pass http://api_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # 속도 제한
        limit_req zone=api_limit burst=20 nodelay;
    }

    # 정적 파일은 캐시
    location /static/ {
        proxy_pass http://backend_servers;
        proxy_cache static_cache;
        proxy_cache_valid 200 1d;
        proxy_cache_key $uri;
        add_header X-Cache-Status $upstream_cache_status;
    }

    # 헬스 체크 엔드포인트
    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }

    # 에러 페이지
    error_page 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}

# 4. 속도 제한 설정
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

# 5. 캐시 설정
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=static_cache:10m
                 max_size=1g inactive=1d use_temp_path=off;
```

### AWS Application Load Balancer (Terraform)

```hcl
# AWS Application Load Balancer 구성

# 1. ALB 생성
resource "aws_lb" "main" {
  name               = "production-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = true
  enable_http2               = true

  # 액세스 로그
  access_logs {
    bucket  = aws_s3_bucket.logs.id
    prefix  = "alb-logs"
    enabled = true
  }

  tags = {
    Name = "production-alb"
  }
}

# 2. 타겟 그룹 (웹 서버)
resource "aws_lb_target_group" "web" {
  name        = "web-target-group"
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "instance"

  # 헬스 체크 설정
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 3
  }

  # 세션 유지 (Sticky Sessions)
  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400  # 24시간
    enabled         = false
  }

  tags = {
    Name = "web-tg"
  }
}

# 3. HTTP 리스너 (HTTPS로 리다이렉트)
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

# 4. HTTPS 리스너
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = aws_acm_certificate.main.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}

# 5. 경로 기반 라우팅 규칙
resource "aws_lb_listener_rule" "api" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }

  condition {
    path_pattern {
      values = ["/api/*"]
    }
  }
}

resource "aws_lb_listener_rule" "static" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 200

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.static.arn
  }

  condition {
    path_pattern {
      values = ["/static/*"]
    }
  }
}

# 6. WAF 연동 (보안)
resource "aws_wafv2_web_acl_association" "main" {
  resource_arn = aws_lb.main.arn
  web_acl_arn  = aws_wafv2_web_acl.main.arn
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 로드 밸런서 유형

| 비교 관점 | L4 (NLB) | L7 (ALB) | 하드웨어 (F5) | 소프트웨어 (HAProxy) |
|---|---|---|---|---|
| **OSI 계층** | Layer 4 | Layer 7 | L4~L7 | L4~L7 |
| **성능** | 초고성능 (Mpps) | 고성능 | 최고성능 | 높음 |
| **지연 시간** | <1ms | 1~5ms | <1ms | 1~3ms |
| **라우팅 유연성** | 낮음 | 높음 | 높음 | 높음 |
| **SSL 종료** | 지원 | 지원 | 지원 | 지원 |
| **비용** | 중간 | 중간 | 높음 | 낮음 |
| **관리 복잡성** | 낮음 | 낮음 | 높음 | 중간 |
| **적합한 용도** | DB, TCP 서비스 | HTTP API, 웹 | 엔터프라이즈 | 범용 |

### 과목 융합 관점 분석

**네트워크와의 융합**:
- **TCP/UDP 처리**: 3-way handshake, 타임아웃, 재전송
- **NAT (Network Address Translation)**: VIP → DIP 변환
- **DSR (Direct Server Return)**: 응답이 LB를 거치지 않고 직접 클라이언트로

**보안과의 융합**:
- **DDoS 방어**: 속도 제한, IP 차단
- **WAF (Web Application Firewall)**: SQL Injection, XSS 방지
- **SSL/TLS 종료**: 인증서 관리, 암호화 해제

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 고트래픽 웹 서비스 로드 밸런싱

**문제 상황**: 이커머스 기업 G사의 웹 서버가 피크 시간에 다운됩니다. 현재 단일 서버로 운영 중입니다.

**기술사의 전략적 의사결정**:

1. **현재 상황 분석**:
   - 일일 방문자: 100만 명
   - 피크 시간 RPS: 10,000
   - 단일 서버 최대 처리: 2,000 RPS
   - 가용성: 95% (월 36시간 다운타임)

2. **로드 밸런싱 아키텍처 설계**:

   ```
   Internet → CloudFront(CDN) → WAF → ALB → [Web Servers x 5]
                                              ↓
                                        [App Servers x 10]
                                              ↓
                                        [DB Cluster]
   ```

3. **기대 효과**:

   | 지표 | 도입 전 | 도입 후 | 개선 |
   |---|---|---|---|
   | 처리 용량 | 2,000 RPS | 20,000 RPS | 10배 |
   | 가용성 | 95% | 99.99% | 5%→0.01% |
   | 장애 복구 | 30분 | 30초 | 98% 단축 |

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - Single Point of Failure**: 로드 밸런서 자체가 단일 실패점이 되지 않도록 다중화 필수.

- **안티패턴 - Sticky Session Overuse**: 세션 유지를 과도하게 사용하면 로드 밸런싱 효과가 감소합니다.

- **체크리스트**:
  - [ ] 헬스 체크 엔드포인트 구현
  - [ ] 로드 밸런서 다중화 (Active-Active 또는 Active-Passive)
  - [ ] SSL 인증서 갱신 자동화
  - [ ] 모니터링 및 알림 설정
  - [ ] 장애 시나리오 테스트

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 단일 서버 | 로드 밸런서 적용 | 개선율 |
|---|---|---|---|
| **처리량** | 2,000 RPS | 20,000+ RPS | 10배 향상 |
| **가용성** | 95% | 99.99% | 5배 향상 |
| **복구 시간** | 30분 | 30초 | 98% 단축 |
| **무중단 배포** | 불가능 | 가능 | 100% |

### 미래 전망 및 진화 방향

- **Global Load Balancing**: 전 세계 리전 간 트래픽 분산
- **AI 기반 트래픽 예측**: 트래픽 패턴 학습 후 선제적 스케일링
- **Service Mesh 통합**: Envoy 기반 L7 로드 밸런싱

### ※ 참고 표준/가이드
- **RFC 7230-7235**: HTTP/1.1 표준
- **AWS Well-Architected Framework**: 로드 밸런싱 모범 사례
- **Nginx Documentation**: 오픈소스 로드 밸런서 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [오토 스케일링](@/studynotes/13_cloud_architecture/03_virt/auto_scaling.md) : 로드 밸런서와 필수 연동
- [고가용성](@/studynotes/10_network/_index.md) : 로드 밸런서의 핵심 목표
- [CDN](@/studynotes/10_network/03_protocols/cdn.md) : 정적 콘텐츠 캐싱
- [VPC](@/studynotes/13_cloud_architecture/03_virt/vpc.md) : 클라우드 네트워크 격리
- [서비스 디스커버리](@/studynotes/13_cloud_architecture/01_native/service_discovery.md) : 동적 서비스 등록

---

### 👶 어린이를 위한 3줄 비유 설명
1. 로드 밸런서는 **'은행의 번호표 기계'**와 같아요. 손님(요청)을 여러 창구(서버)로 고르게 분배해줘요.
2. 어떤 창구가 쉬는 시간이면(서버 장애), **'다른 창구로 안내'**해줘요. 덕분에 은행은 계속 영업해요.
3. 한 창구에만 줄이 생기지 않아서 **'모든 창구가 바쁘게 일해요'**. 손님도 빨리 업무를 볼 수 있어요!
