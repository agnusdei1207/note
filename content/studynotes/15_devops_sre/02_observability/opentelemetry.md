+++
title = "OpenTelemetry (오픈텔레메트리)"
categories = ["studynotes-15_devops_sre"]
+++

# OpenTelemetry (오픈텔레메트리)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 메트릭, 로그, 트레이스 3대 옵저버빌리티 데이터의 수집, 처리, 전송을 위한 벤더 중립적(vendor-neutral) 글로벌 표준 프레임워크로, CNCF 졸업 프로젝트입니다.
> 2. **가치**: 한 번의 계측(Instrumentation)으로 Prometheus, Jaeger, Datadog 등 어떤 백엔드에도 데이터를 전송할 수 있어, 벤더 락인(vendor lock-in)을 완전히 제거합니다.
> 2. **융합**: 다양한 언어 SDK, 자동 계측(Auto-Instrumentation), 그리고 Collector를 통해 클라우드 네이티브 관측성의 사실상 표준으로 자리잡았습니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)

**OpenTelemetry(OTel)**는 분산 시스템의 관측성(Observability)을 위한 **통합 계측 프레임워크**로, 다음 세 가지 핵심 구성요소를 제공합니다:

1. **API**: 계측을 위한 언어 독립적 인터페이스
2. **SDK**: API의 구현체, 처리 파이프라인 포함
3. **Collector**: 데이터 수집, 처리, 라우팅을 위한 프록시

목표: **"계측은 한 번, 백엔드는 자유롭게"**

### 2. 구체적인 일상생활 비유

**통합 충전 케이블**로 비유해 봅시다.

과거에는 삼성폰은 삼성 충전기, 애플폰은 애플 충전기, 소니는 소니 충전기가 필요했습니다. 이것은 각 모니터링 벤더(Prometheus, Jaeger, Datadog)가 자체 에이전트를 요구하는 것과 같습니다.

OpenTelemetry는 **USB-C**와 같습니다. 한 번 USB-C를 지원하도록 만들면, 어떤 브랜드의 충전기(백엔드)에도 연결할 수 있습니다.

### 3. 등장 배경 및 발전 과정

**1단계: 기존 기술의 치명적 한계점 (파편화)**
- OpenTracing (CNCF): 분산 추적 표준 API
- OpenCensus (Google): 메트릭 + 추적 통합
- Prometheus: 메트릭 표준
- Jaeger/Zipkin: 추적 백엔드
- 각각 다른 SDK, 다른 데이터 포맷, 다른 설정 방식

**2단계: 혁신적 패러다임 변화**
- 2019년: OpenTracing + OpenCensus 통합 → OpenTelemetry 탄생
- 2021년: CNCF Incubating 프로젝트
- 2023년: CNCF Graduated (졸업) 프로젝트
- 현재: 산업계 사실상 표준

**3단계: 현재 시장/산업의 비즈니스적 요구사항**
- 멀티 클라우드 환경에서 벤더 락인 방지
- 통합 옵저버빌리티 스택 요구
- 애플리케이션 코드 변경 없는 백엔드 교체

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. OpenTelemetry 핵심 구성 요소

| 구성요소 | 상세 역할 | 내부 동작 메커니즘 | 지원 언어/환경 | 비고 |
|:---|:---|:---|:---|:---|
| **API** | 계측 인터페이스 | Tracer, Meter, Logger 인터페이스 제공 | 모든 언어 | 구현 없음 |
| **SDK** | API 구현체 | SpanProcessor, Exporter, Sampler | Java, Python, Go, JS, .NET, Rust | 실제 동작 |
| **Auto-Instrumentation** | 자동 계측 | 바이트코드 조작, 에이전트 | Java, Python, Node.js, .NET | 코드 수정 불필요 |
| **Collector** | 데이터 파이프라인 | Receivers → Processors → Exporters | 독립 바이너리 | 중앙 집중 처리 |
| **OTLP** | 전송 프로토콜 | gRPC/HTTP 바이너리 프로토콜 | Protocol Buffers | 표준 포맷 |

### 2. 정교한 구조 다이어그램: OpenTelemetry 전체 아키텍처

```text
================================================================================
                   [ OpenTelemetry Complete Architecture ]
================================================================================

    [ Application Layer ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   ┌──────────────────────────────────────────────────────────────────┐  │
    │   │                    Application Code                               │  │
    │   │                                                                    │  │
    │   │   // 수동 계측 (Manual Instrumentation)                           │  │
    │   │   Span span = tracer.spanBuilder("operation")                    │  │
    │   │       .setAttribute("key", "value")                              │  │
    │   │       .startSpan();                                              │  │
    │   │   // ... 비즈니스 로직 ...                                        │  │
    │   │   span.end();                                                     │  │
    │   │                                                                    │  │
    │   └──────────────────────────────────────────────────────────────────┘  │
    │                                    │                                    │
    │                                    ▼                                    │
    │   ┌──────────────────────────────────────────────────────────────────┐  │
    │   │              OpenTelemetry API (Interface Layer)                  │  │
    │   │                                                                    │  │
    │   │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │  │
    │   │   │ Tracer API  │  │ Meter API   │  │ Logger API  │              │  │
    │   │   │ (Traces)    │  │ (Metrics)   │  │ (Logs)      │              │  │
    │   │   └─────────────┘  └─────────────┘  └─────────────┘              │  │
    │   │                                                                    │  │
    │   └──────────────────────────────────────────────────────────────────┘  │
    │                                    │                                    │
    │                                    ▼                                    │
    │   ┌──────────────────────────────────────────────────────────────────┐  │
    │   │              OpenTelemetry SDK (Implementation)                   │  │
    │   │                                                                    │  │
    │   │   ┌─────────────────────────────────────────────────────────────┐ │  │
    │   │   │ Span Processor (Batch vs Simple)                           │ │  │
    │   │   │ - Batch: 여러 Span을 모아서 전송 (효율적)                   │ │  │
    │   │   │ - Simple: 즉시 전송 (디버깅용)                             │ │  │
    │   │   └─────────────────────────────────────────────────────────────┘ │  │
    │   │                              │                                     │  │
    │   │                              ▼                                     │  │
    │   │   ┌─────────────────────────────────────────────────────────────┐ │  │
    │   │   │ Sampler (샘플링 결정)                                      │ │  │
    │   │   │ - AlwaysOn: 100% 수집                                      │ │  │
    │   │   │ - TraceIdRatio: N% 확률 수집                               │ │  │
    │   │   │ - ParentBased: 부모 Span 샘플링 따라감                     │ │  │
    │   │   └─────────────────────────────────────────────────────────────┘ │  │
    │   │                              │                                     │  │
    │   │                              ▼                                     │  │
    │   │   ┌─────────────────────────────────────────────────────────────┐ │  │
    │   │   │ Exporter (내보내기)                                        │ │  │
    │   │   │ - OTLP Exporter → Collector                                │ │  │
    │   │   │ - Jaeger Exporter → Jaeger 직접                            │ │  │
    │   │   │ - Prometheus Exporter → Prometheus                         │ │  │
    │   │   └─────────────────────────────────────────────────────────────┘ │  │
    │   │                                                                    │  │
    │   └──────────────────────────────────────────────────────────────────┘  │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
                                       │
                                       │ OTLP (gRPC/HTTP)
                                       ▼
    [ Collector Layer ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   ┌──────────────────────────────────────────────────────────────────┐  │
    │   │                  OpenTelemetry Collector                         │  │
    │   │                                                                  │  │
    │   │   ┌─────────────────────────────────────────────────────────────┐│  │
    │   │   │ RECEIVERS (수신)                                            ││  │
    │   │   │ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐   ││  │
    │   │   │ │ OTLP      │ │ Jaeger    │ │ Zipkin    │ │ Prometheus│   ││  │
    │   │   │ │ (gRPC/HTTP)│ │ (Thrift)  │ │ (JSON)    │ │ (Remote)  │   ││  │
    │   │   │ └───────────┘ └───────────┘ └───────────┘ └───────────┘   ││  │
    │   │   └─────────────────────────────────────────────────────────────┘│  │
    │   │                              │                                    │  │
    │   │                              ▼                                    │  │
    │   │   ┌─────────────────────────────────────────────────────────────┐│  │
    │   │   │ PROCESSORS (처리)                                           ││  │
    │   │   │ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐      ││  │
    │   │   │ │ Batch         │ │ Memory        │ │ Filtering     │      ││  │
    │   │   │ │ (배치 처리)   │ │ Limiter       │ │ (필터링)      │      ││  │
    │   │   │ │               │ │ (메모리 제한) │ │               │      ││  │
    │   │   │ └───────────────┘ └───────────────┘ └───────────────┘      ││  │
    │   │   │ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐      ││  │
    │   │   │ │ Attributes    │ │ Tail Sampling │ │ Transform     │      ││  │
    │   │   │ │ (속성 추가)   │ │ (꼬리 샘플링) │ │ (변환)        │      ││  │
    │   │   │ └───────────────┘ └───────────────┘ └───────────────┘      ││  │
    │   │   └─────────────────────────────────────────────────────────────┘│  │
    │   │                              │                                    │  │
    │   │                              ▼                                    │  │
    │   │   ┌─────────────────────────────────────────────────────────────┐│  │
    │   │   │ EXPORTERS (내보내기)                                        ││  │
    │   │   │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            ││  │
    │   │   │ │ OTLP        │ │ Jaeger      │ │ Prometheus  │            ││  │
    │   │   │ │ (Backend)   │ │ (Backend)   │ │ (RemoteWrite)│           ││  │
    │   │   │ └─────────────┘ └─────────────┘ └─────────────┘            ││  │
    │   │   │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            ││  │
    │   │   │ │ Datadog     │ │ New Relic   │ │ Google Cloud│            ││  │
    │   │   │ │ (SaaS)      │ │ (SaaS)      │ │ (GCP)       │            ││  │
    │   │   │ └─────────────┘ └─────────────┘ └─────────────┘            ││  │
    │   │   └─────────────────────────────────────────────────────────────┘│  │
    │   │                                                                  │  │
    │   └──────────────────────────────────────────────────────────────────┘  │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
    [ Backend Layer - Vendor Neutral ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   ┌────────────────────────────────────────────────────────────────┐    │
    │   │                  Observability Backends                         │    │
    │   │                                                                  │    │
    │   │   [ 오픈소스 ]              [ 상용 SaaS ]           [ 클라우드 ]  │    │
    │   │   ┌───────────┐            ┌───────────┐          ┌───────────┐│    │
    │   │   │ Jaeger    │            │ Datadog   │          │ AWS X-Ray ││    │
    │   │   │ Zipkin    │            │ New Relic │          │ GCP Trace ││    │
    │   │   │ Prometheus│            │ Splunk    │          │ Azure App ││    │
    │   │   │ Tempo     │            │ Dynatrace │          │ Insights  ││    │
    │   │   │ Loki      │            │ Honeycomb │          │           ││    │
    │   │   └───────────┘            └───────────┘          └───────────┘│    │
    │   │                                                                  │    │
    │   │   ⭐ 동일한 OpenTelemetry 계측으로 모든 백엔드 사용 가능        │    │
    │   │                                                                  │    │
    │   └────────────────────────────────────────────────────────────────┘    │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
```

### 3. 심층 동작 원리: Collector 구성

```yaml
# otel-collector-config.yaml - OpenTelemetry Collector 설정 예시
receivers:
  # OTLP 수신 (기본 포트)
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

  # Jaeger 호환 수신
  jaeger:
    protocols:
      grpc:
        endpoint: 0.0.0.0:14250
      thrift_http:
        endpoint: 0.0.0.0:14268

  # Prometheus 수신
  prometheus:
    config:
      scrape_configs:
        - job_name: 'otel-collector'
          scrape_interval: 10s
          static_configs:
            - targets: ['localhost:8888']

processors:
  # 배치 처리 (메모리 효율)
  batch:
    timeout: 1s
    send_batch_size: 1024
    send_batch_max_size: 2048

  # 메모리 제한
  memory_limiter:
    check_interval: 1s
    limit_mib: 512
    spike_limit_mib: 128

  # 속성 추가 (예: 환경 정보)
  resource:
    attributes:
      - key: deployment.environment
        value: production
        action: upsert
      - key: service.namespace
        value: my-service
        action: upsert

  # 필터링 (민감 정보 제거)
  filter:
    traces:
      span:
        # 특정 속성 제거
        - 'attributes["password"] != nil'
        - 'attributes["credit_card"] != nil'

  # Tail Sampling (에러/지연만 100% 샘플링)
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: errors
        type: status_code
        status_code:
          status_codes: [ERROR]
      - name: slow-traces
        type: latency
        latency:
          threshold_ms: 1000
      - name: random sampling
        type: probabilistic
        probabilistic:
          sampling_percentage: 10

exporters:
  # Jaeger로 내보내기
  jaeger:
    endpoint: jaeger-collector:14250
    tls:
      insecure: true

  # Prometheus Remote Write
  prometheusremotewrite:
    endpoint: http://prometheus:9090/api/v1/write

  # OTLP로 다른 Collector로 전달
  otlp:
    endpoint: another-collector:4317

  # 디버깅용 로그
  logging:
    loglevel: debug

  # 파일로 저장 (백업용)
  file:
    path: /var/log/otel/traces.json

service:
  pipelines:
    # 트레이스 파이프라인
    traces:
      receivers: [otlp, jaeger]
      processors: [memory_limiter, batch, tail_sampling]
      exporters: [jaeger, logging]

    # 메트릭 파이프라인
    metrics:
      receivers: [otlp, prometheus]
      processors: [memory_limiter, batch]
      exporters: [prometheusremotewrite]

    # 로그 파이프라인
    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [logging]
```

### 4. 실무 코드: Python 애플리케이션 계측

```python
#!/usr/bin/env python3
"""
OpenTelemetry Python 계측 예시
Flask 애플리케이션에 메트릭, 로그, 트레이스 통합
"""

from flask import Flask, request
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource

# 1. 리소스 정의 (서비스 정보)
resource = Resource.create({
    "service.name": "payment-service",
    "service.version": "1.0.0",
    "deployment.environment": "production"
})

# 2. 트레이싱 설정
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# OTLP Exporter 설정
otlp_trace_exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4317",
    insecure=True
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_trace_exporter)
)

# 3. 메트릭 설정
metric_reader = PeriodicExportingMetricReader(
    exporter=OTLPMetricExporter(
        endpoint="http://otel-collector:4317",
        insecure=True
    ),
    export_interval_millis=10000  # 10초마다 전송
)
metrics.set_meter_provider(MeterProvider(
    resource=resource,
    metric_readers=[metric_reader]
))
meter = metrics.get_meter(__name__)

# 4. 커스텀 메트릭 정의
request_counter = meter.create_counter(
    name="payment_requests_total",
    description="Total number of payment requests",
    unit="1"
)

request_duration = meter.create_histogram(
    name="payment_request_duration_ms",
    description="Payment request duration in milliseconds",
    unit="ms"
)

# 5. Flask 앱 생성 및 자동 계측
app = Flask(__name__)

# Flask 자동 계측
FlaskInstrumentor().instrument_app(app)

# Requests 라이브러리 자동 계측
RequestsInstrumentor().instrument()

# 6. 비즈니스 로직
import requests
import time

@app.route("/api/payments", methods=["POST"])
def process_payment():
    start_time = time.time()

    # 수동 Span 생성
    with tracer.start_as_current_span("process_payment") as span:
        # Span 속성 추가
        span.set_attribute("payment.amount", request.json.get("amount"))
        span.set_attribute("payment.currency", request.json.get("currency", "KRW"))
        span.set_attribute("user.id", request.json.get("user_id"))

        try:
            # 외부 API 호출 (자동으로 Span 생성됨)
            response = requests.post(
                "http://pg-gateway/api/charge",
                json=request.json
            )

            # 메트릭 기록
            request_counter.add(1, {
                "status": "success",
                "currency": request.json.get("currency", "KRW")
            })

            duration_ms = (time.time() - start_time) * 1000
            request_duration.record(duration_ms, {
                "endpoint": "/api/payments"
            })

            return {"status": "success", "transaction_id": response.json()["id"]}

        except Exception as e:
            # 에러 Span 기록
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))

            request_counter.add(1, {"status": "error"})
            return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 옵저버빌리티 표준 비교

| 특성 | OpenTelemetry | Prometheus Native | Datadog SDK | Jaeger SDK |
|:---|:---|:---|:---|:---|
| **데이터 타입** | Metrics + Logs + Traces | Metrics만 | Metrics + Logs + Traces | Traces만 |
| **벤더 독립성** | 완전 독립 | Prometheus 종속 | Datadog 종속 | Jaeger 종속 |
| **자동 계측** | 다양한 언어 지원 | 없음 | 에이전트 기반 | 제한적 |
| **Collector** | 통합 Collector | 없음 | Agent | 없음 |
| **표준화** | CNCF 표준 | De facto 표준 | 사설 | CNCF |

### 2. 과목 융합 관점 분석

**OpenTelemetry + 서비스 메시 (Istio)**:
- 사이드카 프록시가 자동으로 OTel Span 생성
- Envoy가 OTLP로 트레이스 전송
- 애플리케이션 코드 수정 불필요

**OpenTelemetry + Kubernetes**:
- OTel Operator가 자동으로 사이드카 주입
- Instrumentation CRD로 언어별 설정
- Pod 주입으로 자동 계측

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

**시나리오 A: 벤더 교체 필요 (Datadog → Prometheus + Tempo)**
- **상황**: 비용 절감을 위해 상용 APM에서 오픈소스로 전환
- **기술사의 전략적 의사결정**:
  1. **OpenTelemetry 도입**: 애플리케이션은 이미 OTel 사용 중
  2. **Collector 설정 변경**: Exporter만 Datadog → Prometheus + Tempo로 변경
  3. **애플리케이션 코드 변경**: **없음** (핵심 장점)

**시나리오 B: 멀티 백엔드 운영**
- **상황**: 개발팀은 Datadog, SRE팀은 Prometheus 사용
- **기술사의 전략적 의사결정**:
  1. **Collector에서 멀티 Export**: 동일 데이터를 두 백엔드로 전송
  2. **비용 최적화**: 샘플링으로 데이터 양 조절

### 2. 도입 시 고려사항 (체크리스트)

**SDK 도입 체크리스트**:
- [ ] 지원 언어 확인 (주요 언어 모두 지원)
- [ ] Auto-Instrumentation vs 수동 계측 결정
- [ ] Sampler 설정 (프로덕션: 10-20%)
- [ ] Resource Attributes 설정 (서비스명, 버전)

**Collector 배포 체크리스트**:
- [ ] 배포 방식 결정 (DaemonSet vs Deployment)
- [ ] Processor 구성 (Batch, Memory Limiter)
- [ ] Exporter 구성 (대상 백엔드)
- [ ] TLS/인증 설정

### 3. 주의사항 및 안티패턴

**안티패턴 1: SDK 없이 Collector만 사용**
- 문제: 애플리케이션 레벨 컨텍스트 손실
- 해결: SDK로 계측 후 Collector로 집계

**안티패턴 2: 과도한 샘플링**
- 문제: 중요 장애 데이터 손실
- 해결: Tail Sampling으로 에러/지연 100% 보장

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **벤더 교체 비용** | 수개월 리팩토링 | 설정만 변경 | 95% 절감 |
| **계측 일관성** | 벤더별 상이 | 통합 API | 유지보수 용이 |
| **데이터 품질** | 파편화 | 통합 컨텍스트 | 상관관계 분석 |

### 2. 미래 전망 및 진화 방향

**완전한 통합**:
- Metrics, Logs, Traces 완전 통합
- Profiling 추가 (지속적 프로파일링)
- 단일 데이터 모델

**AI/ML 통합**:
- 자동 이상 탐지
- 예측적 알림
- 자동 루트 코즈 분석

### 3. 참고 표준/가이드

- **OpenTelemetry.io**: 공식 문서
- **CNCF OTel Specification**: 기술 명세
- **OTEP (OTel Enhancement Proposals)**: 기능 제안 프로세스

---

## 관련 개념 맵 (Knowledge Graph)

- [옵저버빌리티 기본](@/studynotes/15_devops_sre/02_observability/observability_fundamentals.md) : OpenTelemetry의 상위 개념
- [분산 추적](@/studynotes/15_devops_sre/02_observability/distributed_tracing.md) : 트레이싱 데이터 수집
- [Prometheus 모니터링](@/studynotes/15_devops_sre/02_observability/prometheus_monitoring.md) : 메트릭 백엔드
- [Jaeger](@/studynotes/15_devops_sre/02_observability/jaeger.md) : 트레이싱 백엔드
- [서비스 메시](@/studynotes/15_devops_sre/03_automation/service_mesh.md) : 자동 계측 인프라

---

## 어린이를 위한 3줄 비유 설명

1. OpenTelemetry는 **통합 충전 케이블(USB-C)**과 같아요. 어떤 브랜드 충전기든 연결할 수 있죠.
2. 과거에는 삼성폰은 삼성 충전기, 애플폰은 애플 충전기가 필요했어요. 이제는 **하나의 케이블로 모두 충전**해요.
3. 프로그램도 마찬가지! **한 번만 계측하면** 어떤 모니터링 도구(Datadog, Prometheus 등)에도 연결돼요!
