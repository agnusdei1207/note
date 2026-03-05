+++
title = "옵저버빌리티 (Observability / 관측성)"
date = 2024-05-19
description = "분산된 수백 개의 마이크로서비스 내부 상태를 외부 출력(로그, 메트릭, 트레이스)만 보고 추론할 수 있는 능력으로, 모니터링의 진화된 개념"
weight = 215
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Observability", "Metrics", "Logs", "Traces", "OpenTelemetry", "Monitoring", "MELT"]
+++

# 옵저버빌리티 (Observability / 관측성) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 복잡한 분산 시스템(마이크로서비스, 컨테이너, 서버리스)의 **내부 상태를 외부 출력(MELT: Metrics, Events, Logs, Traces)만 보고 추론할 수 있는 능력**으로, 전통적 모니터링이 '알려진 문제'를 감지하는 반면, 옵저버빌리티는 '알려지지 않은 문제'까지 탐구할 수 있습니다.
> 2. **가치**: 평균 장애 탐지 시간(MTTD) 60% 단축, 근본 원인 분석(RCA) 시간 70% 단축, **MTTR(평균 복구 시간)을 수시간에서 수분으로 감소**시킵니다.
> 3. **융합**: OpenTelemetry(CNCF 표준), Prometheus(메트릭), ELK/Loki(로그), Jaeger/Zipkin(분산 추적), Grafana(시각화) 등의 기술 스택과 결합합니다.

---

## Ⅰ. 개요 (Context & Background)

옵저버빌리티(Observability)는 제어 이론(Control Theory)에서 유래한 개념으로, 시스템의 내부 상태를 외부 출력만 보고 얼마나 잘 추론할 수 있는지를 나타냅니다. 소프트웨어 관점에서는 **시스템이 생성하는 신호(로그, 메트릭, 트레이스)를 통해 문제를 이해하고 디버깅하는 능력**을 의미합니다.

**💡 비유**: 옵저버빌리티는 **'자동차 대시보드 + 블랙박스 + GPS 추적'**의 결합입니다. 속도계/연료계(메트릭)는 현재 상태를 보여주고, 블랙박스(로그)는 무슨 일이 있었는지 기록하며, GPS(트레이스)는 어디를 지나왔는지 추적합니다. 이三者를 종합하면 "왜 시동이 꺼졌는지"를 파악할 수 있습니다.

**등장 배경 및 발전 과정**:
1. **모니터링의 한계**: 전통적 모니터닝은 "CPU 90% 알림"처럼 알려진 문제만 감지했습니다.
2. **분산 시스템의 복잡성**: 마이크로서비스 수백 개가 연결된 환경에서 "어디서 느린가?"를 찾기 어려워졌습니다.
3. **3 Pillars of Observability**: 2017년 Cindy Sridharan이 "Observability: 3 Pillars" 글에서 개념을 정립했습니다.
4. **OpenTelemetry 통합 (2019)**: OpenTracing + OpenCensus가 통합되어 CNCF 표준이 되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 옵저버빌리티 3대 요소 (3 Pillars) + Events

| 요소 | 상세 설명 | 예시 | 도구 | 비유 |
|---|---|---|---|---|
| **Metrics** | 시계열 숫자 데이터 | CPU%, 응답시간, 에러율 | Prometheus, Datadog | 속도계 |
| **Logs** | 이벤트 기반 텍스트 기록 | "Error connecting to DB" | ELK, Loki | 블랙박스 |
| **Traces** | 요청의 분산 경로 추적 | A→B→C→D 서비스 경로 | Jaeger, Zipkin | GPS 추적 |
| **Events** | 특정 시점의 상태 스냅샷 | 배포 완료, 설정 변경 | PagerDuty, Event DB | 사진 |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Observability Architecture ]                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         [ Instrumentation Layer ]                           │
│                                                                             │
│   Application Services                                                      │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│   │  Service A  │  │  Service B  │  │  Service C  │  │  Service D  │       │
│   │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │       │
│   │ │  Code    │ │  │ │  Code    │ │  │ │  Code    │ │  │ │  Code    │ │       │
│   │ │Auto-Instr│ │  │ │Auto-Instr│ │  │ │Auto-Instr│ │  │ │Auto-Instr│ │       │
│   │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │       │
│   │      │      │  │      │      │  │      │      │  │      │      │       │
│   │  ┌───▼───┐  │  │  ┌───▼───┐  │  │  ┌───▼───┐  │  │  ┌───▼───┐  │       │
│   │  │ OTel  │  │  │  │ OTel  │  │  │  │ OTel  │  │  │  │ OTel  │  │       │
│   │  │Agent  │  │  │  │Agent  │  │  │  │Agent  │  │  │  │Agent  │  │       │
│   │  └───┬───┘  │  │  └───┬───┘  │  │  └───┬───┘  │  │  └───┬───┘  │       │
│   └──────┼──────┘  └──────┼──────┘  └──────┼──────┘  └──────┼──────┘       │
│          │                │                │                │               │
│          └────────────────┴────────────────┴────────────────┘               │
│                                    │                                        │
│                          OpenTelemetry Protocol (OTLP)                      │
│                                    │                                        │
└────────────────────────────────────┼────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         [ Collection Layer ]                                │
│                                                                             │
│   ┌───────────────────────────────────────────────────────────────────────┐│
│   │                     OpenTelemetry Collector                            ││
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ││
│   │  │   Receivers │  │  Processors │  │   Exporters │  │  Extensions │  ││
│   │  │  (OTLP,     │  │ (Batch,     │  │ (Prometheus,│  │ (Health     │  ││
│   │  │  Prometheus)│  │  Memory,    │  │  Jaeger,    │  │  Check)     │  ││
│   │  │             │  │  Tail Sampl)│  │  Loki)      │  │             │  ││
│   │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  ││
│   └───────────────────────────────────────────────────────────────────────┘│
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          │                          │                          │
          ▼                          ▼                          ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│   [ Metrics ]    │      │    [ Logs ]      │      │   [ Traces ]     │
│                  │      │                  │      │                  │
│  ┌────────────┐  │      │  ┌────────────┐  │      │  ┌────────────┐  │
│  │ Prometheus │  │      │    Loki      │  │      │   Jaeger    │  │
│  │  Victoria  │  │      │    ELK       │  │      │   Zipkin    │  │
│  │  Metrics   │  │      │   Datadog    │  │      │  Tempo      │  │
│  └────────────┘  │      │  └────────────┘  │      │  └────────────┘  │
│        │         │      │        │         │      │        │         │
└────────┼─────────┘      └────────┼─────────┘      └────────┼─────────┘
         │                         │                         │
         └─────────────────────────┼─────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        [ Visualization Layer ]                              │
│                                                                             │
│   ┌───────────────────────────────────────────────────────────────────────┐│
│   │                            Grafana                                     ││
│   │  ┌─────────────────────────────────────────────────────────────────┐ ││
│   │  │  Unified Dashboard: Metrics + Logs + Traces                    │ ││
│   │  │                                                                 │ ││
│   │  │  [CPU Graph] [Error Rate] [Latency P99]                        │ ││
│   │  │  [Log Panel] [Trace View] [Service Map]                        │ ││
│   │  └─────────────────────────────────────────────────────────────────┘ ││
│   └───────────────────────────────────────────────────────────────────────┘│
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: 분산 추적 (Distributed Tracing)

```
┌────────────────────────────────────────────────────────────────────────────┐
│                     Distributed Tracing Flow                               │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ 요청 흐름과 Trace/Span 구조 ]                                            │
│                                                                            │
│  User Request                                                              │
│       │                                                                    │
│       │ Trace ID: abc123 (전체 요청 고유)                                   │
│       ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  Service A (API Gateway)                                            │  │
│  │  Span ID: span1, Parent: none                                       │  │
│  │  Duration: 150ms                                                     │  │
│  │  ├─ Process Request: 5ms                                            │  │
│  │  ├─ Call Service B: ─────────────────────────────┐                  │  │
│  │  └─ Return Response: 2ms                         │                  │  │
│  └─────────────────────────────────────────────────│──────────────────┘  │
│                                                     │                      │
│       Span ID: span2, Parent: span1                │                      │
│       W3C Trace Context propagation                ▼                      │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  Service B (Order)                                                   │  │
│  │  Span ID: span2, Parent: span1                                      │  │
│  │  Duration: 100ms                                                     │  │
│  │  ├─ Validate: 5ms                                                   │  │
│  │  ├─ Call Service C: ─────────────────────────┐                      │  │
│  │  └─ Save DB: 10ms                            │                      │  │
│  └──────────────────────────────────────────────│──────────────────────┘  │
│                                                  │                         │
│       Span ID: span3, Parent: span2             ▼                         │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  Service C (Inventory)                                               │  │
│  │  Span ID: span3, Parent: span2                                      │  │
│  │  Duration: 60ms                                                      │  │
│  │  ├─ Check Stock: 50ms (SLOW! 🔴)                                    │  │
│  │  └─ Reserve: 10ms                                                    │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  [ Waterfall View in Jaeger ]                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  Service A    ████████████████████████████████████░░░░░  150ms      │  │
│  │  Service B      █████████████████████████████████░░  100ms          │  │
│  │  Service C        ██████████████████████████████░░  60ms 🔴         │  │
│  │                  ▲                                                    │  │
│  │                  │                                                    │  │
│  │            병목 지점 발견!                                             │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: OpenTelemetry Python

```python
# OpenTelemetry Python Instrumentation
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# 1. TracerProvider 설정
provider = TracerProvider()
trace.set_tracer_provider(provider)

# 2. OTLP Exporter (Jaeger/Tempo로 전송)
otlp_exporter = OTLPSpanExporter(endpoint="otel-collector:4317")
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# 3. Auto-instrumentation
FlaskInstrumentor().instrument()
RequestsInstrumentor().instrument()

# 4. 커스텀 Span 생성
from flask import Flask, request
import requests

app = Flask(__name__)
tracer = trace.get_tracer(__name__)

@app.route("/api/orders", methods=["POST"])
def create_order():
    # 자동 생성된 Span 하위에 커스텀 Span 추가
    with tracer.start_as_current_span("create_order") as span:
        # Span에 속성 추가
        span.set_attribute("order.user_id", request.json.get("user_id"))
        span.set_attribute("order.items_count", len(request.json.get("items", [])))

        # 하위 작업 추적
        with tracer.start_as_current_span("validate_order"):
            # 검증 로직
            pass

        # 외부 서비스 호출 (자동 추적)
        with tracer.start_as_current_span("call_inventory"):
            response = requests.post(
                "http://inventory-service/check",
                json={"items": request.json.get("items")}
            )

        # 이벤트 추가 (에러 발생 지점 표시)
        if response.status_code != 200:
            span.add_event(
                name="inventory_check_failed",
                attributes={"error": response.text}
            )

        return {"status": "created"}

# 5. Metrics 설정
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader

# Prometheus Exporter
reader = PrometheusMetricReader()
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter(__name__)

# Counter 생성
order_counter = meter.create_counter(
    name="orders_total",
    description="Total orders created",
    unit="1"
)

# Histogram 생성 (Latency 추적)
order_duration = meter.create_histogram(
    name="order_duration_seconds",
    description="Order creation duration",
    unit="s"
)

@app.route("/metrics")
def metrics():
    """Prometheus 스크랩 엔드포인트"""
    from prometheus_client import generate_latest
    return generate_latest()
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 옵저버빌리티 솔루션

| 비교 관점 | Prometheus + Grafana | Datadog | New Relic | Elastic Stack |
|---|---|---|---|---|
| **유형** | 오픈소스 조합 | SaaS | SaaS | 오픈소스/Cloud |
| **통합성** | 낮음 (별도 구성) | 높음 | 높음 | 중간 |
| **비용** | 인프라 비용만 | 사용량 기반 | 사용량 기반 | 인프라 + Cloud |
| **K8s 통합** | 네이티브 | 에이전트 | 에이전트 | 에이전트 |
| **학습 곡선** | 높음 | 낮음 | 낮음 | 중간 |

### 과목 융합 관점 분석

**네트워크와의 융합**:
- **Service Map**: 서비스 간 통신 토폴로지 시각화
- **Network Latency**: 네트워크 계층 지연 시간 추적

**데이터베이스와의 융합**:
- **Query Tracing**: DB 쿼리 실행 시간 추적
- **Connection Pool Metrics**: DB 연결 풀 상태 모니터링

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 옵저버빌리티 구축

**문제 상황**: 마이크로서비스 50개 환경에서 "결제가 느리다"는 장애 보고가 접수됩니다.

**기술사의 전략적 의사결정**:
1. **1단계**: 로그 중앙화 (Loki)
2. **2단계**: 메트릭 수집 (Prometheus)
3. **3단계**: 분산 추적 (Tempo + Grafana)
4. **4단계**: 통합 대시보드 (Grafana)
5. **5단계**: 알림 규칙 (Alertmanager)

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - Data Swamp**: 수집만 하고 활용하지 않으면 비용만 낭비합니다. 명확한 Use Case가 있어야 합니다.
- **체크리스트**:
  - [ ] 핵심 SLI/SLO 정의
  - [ ] Cardinality 관리 (메트릭 라벨)
  - [ ] 로그 레벨 표준화
  - [ ] Trace Sampling 정책
  - [ ] Retention 기간 설정

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 도입 전 | 도입 후 | 개선 |
|---|---|---|---|
| **MTTD** | 30분 | 5분 | 83% 단축 |
| **MTTR** | 4시간 | 30분 | 87% 단축 |
| **RCA 시간** | 2시간 | 20분 | 83% 단축 |
| **장애 예방** | 10% | 60% | 50% 향상 |

### 미래 전망 및 진화 방향

- **AI-Powered Observability**: 이상 탐지 자동화, 근본 원인 예측
- **Continuous Profiling**: CPU/Memory 프로파일링 통합
- **Business Observability**: 비즈니스 메트릭과 기술 메트릭 통합

### ※ 참고 표준/가이드
- **OpenTelemetry**: CNCF 옵저버빌리티 표준
- **W3C Trace Context**: 분산 추적 컨텍스트 전파 표준
- **Google SRE Book**: 모니터링/옵저버빌리티 챕터

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [SRE](@/studynotes/13_cloud_architecture/01_native/sre.md) : 옵저버빌리티를 활용하는 엔지니어링
- [Prometheus](@/studynotes/13_cloud_architecture/01_native/prometheus.md) : 메트릭 수집
- [ELK Stack](@/studynotes/13_cloud_architecture/01_native/elk_stack.md) : 로그 분석
- [Jaeger](@/studynotes/13_cloud_architecture/01_native/jaeger.md) : 분산 추적
- [Grafana](@/studynotes/13_cloud_architecture/01_native/grafana.md) : 시각화

---

### 👶 어린이를 위한 3줄 비유 설명
1. 옵저버빌리티는 **'자동차 대시보드 + 블랙박스 + GPS'**예요. 차 상태를 한눈에 알 수 있어요.
2. 속도계(메트릭)는 지금 얼마나 빠른지, 블랙박스(로그)는 무슨 일이 있었는지 알려줘요.
3. GPS(트레이스)는 **'어디를 지나왔는지'** 보여줘요. 그래서 "왜 늦었는지" 바로 알 수 있어요!
