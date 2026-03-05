+++
title = "분산 추적 (Distributed Tracing)"
description = "MSA 환경에서 요청의 전체 흐름을 추적하는 기술에 대한 심층 기술 백서"
date = 2024-05-15
[taxonomies]
tags = ["Distributed Tracing", "Jaeger", "Zipkin", "OpenTelemetry", "MSA", "Observability"]
+++

# 분산 추적 (Distributed Tracing)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 추적(Distributed Tracing)은 마이크로서비스 아키텍처(MSA)에서 하나의 사용자 요청이 여러 서비스를 거쳐 처리되는 전체 경로를 **Trace ID로 연결하여 시각화**하고, 각 구간(Span)의 지연 시간, 에러 발생 지점을 정밀하게 분석하는 옵저버빌리티 핵심 기술입니다.
> 2. **가치**: 분산 추적은 "어떤 서비스에서 병목이 발생했는가?"를 단번에 파악하게 하여 평균 복구 시간(MTTR)을 획기적으로 단축시키고, 서비스 간 의존관계를 자동으로 매핑하여 아키텍처 이해도를 높입니다.
> 3. **융합**: OpenTelemetry(OTel)가 수집 표준으로 자리잡았으며, Jaeger, Zipkin, AWS X-Ray, Datadog APM이 스토리지/시각화 백엔드로 활용됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**분산 추적(Distributed Tracing)**은 분산 시스템(특히 마이크로서비스 아키텍처)에서 **하나의 요청(Request)이 시스템의 여러 컴포넌트(서비스, 데이터베이스, 메시지 큐)를 거쳐 처리되는 전체 여정을 추적하고 시각화하는 기술**입니다. 구글의 Dapper 논문(2010)에서 시작되었으며, 현재 옵저버빌리티(Observability)의 3대 기둥 중 하나입니다.

핵심 개념:
- **Trace(트레이스)**: 하나의 요청이 시스템을 통과하는 전체 경로. 여러 개의 Span으로 구성됩니다.
- **Span(스팬)**: Trace 내에서 단일 서비스(또는 작업)가 수행한 논리적 작업 단위. 시작/종료 시간, 메타데이터를 포함합니다.
- **Trace ID**: 전체 요청 경로를 식별하는 고유 ID. 모든 Span이 동일한 Trace ID를 공유합니다.
- **Span ID**: 개별 Span을 식별하는 고유 ID.
- **Parent Span ID**: 부모-자식 관계를 정의하여 Span 간의 계층 구조를 형성합니다.
- **Context Propagation(컨텍스트 전파)**: Trace ID와 Span ID를 서비스 간 HTTP 헤더로 전달하여 요청 흐름의 연속성을 유지합니다.

### 💡 2. 구체적인 일상생활 비유
**택배 배송 추적 시스템**을 상상해 보세요:
- **Trace**: "서울에서 부산으로 가는 택배 하나" = 하나의 요청
- **Trace ID**: "송장 번호 1234567890" = 전체 배송 경로를 식별
- **Span**: "각 배송 단계" = 서울 물류센터 → 대전 허브 → 부산 물류센터 → 배송 기사
- **Span ID**: "각 단계의 고유 번호" = 서울센터-001, 대전허브-002, 부산센터-003
- **Parent Span ID**: "이전 단계 번호" = 부산센터의 Parent는 대전허브
- **Context Propagation**: "송장이 택배에 계속 부착됨" = 서비스 간 Trace ID 전달

분산 추적은 "송장 번호로 전체 배송 경로를 한눈에 볼 수 있는 것"과 같습니다. 어느 단계에서 지연되었는지, 어디서 분실되었는지 바로 알 수 있죠.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (모놀리식 로그 분석)**:
   모놀리식 애플리케이션에서는 단일 서버의 로그만 보면 됐습니다. 하지만 MSA에서는:
   - 사용자가 "결제가 안 돼요"라고 불만 제기
   - 개발자가 결제 서비스 로그 확인 → "주문 서비스 응답 없음"
   - 주문 서비스 로그 확인 → "재고 서비스 타임아웃"
   - 재고 서비스 로그 확인 → "DB 커넥션 풀 고갈"
   이렇게 수십 개의 서비스 로그를 수동으로 연결해야 했습니다.

2. **혁신적 패러다임 변화의 시작**:
   - **2010년**: Google Dapper 논문 발표. 대규모 분산 시스템 추적 아키텍처 공개.
   - **2012년**: Twitter Zipkin 오픈소스 공개.
   - **2015년**: Uber Jaeger 개발 시작 (2017년 오픈소스).
   - **2019년**: OpenTelemetry 프로젝트 시작 (OpenTracing + OpenCensus 통합).
   - **현재**: OpenTelemetry가 CNCF 졸업 프로젝트로, 산업 표준.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   MSA 환경에서 하나의 요청이 평균 10~50개의 서비스를 거칩니다. "지연 시간이 2초인데 어디서 느린 거야?"라는 질문에 답하기 위해 분산 추적은 필수입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Tracer** | Span 생성 및 Context 관리 | Trace/Span ID 생성, 샘플링 결정 | OpenTelemetry SDK | 택배 송장 발급 기계 |
| **Instrumentation** | 코드에 추적 코드 삽입 | 자동(에이전트) 또는 수동(SDK) 방식 | Java Agent, Python Decorator | 배송 단계 기록원 |
| **Context Propagation** | 서비스 간 Trace Context 전달 | HTTP Header(W3C Trace Context)에 Trace/Span ID 주입 | traceparent, b3 Headers | 송장 택배에 부착 |
| **Collector** | 추적 데이터 수집 및 처리 | Batch 처리, 샘플링, 필터링 | OpenTelemetry Collector | 물류 허브 |
| **Storage Backend** | 추적 데이터 영구 저장 | 분산 저장소, 인덱싱 | Elasticsearch, Cassandra | 물류 창고 |

### 2. 정교한 구조 다이어그램: 분산 추적 데이터 흐름

```text
=====================================================================================================
                    [ Distributed Tracing Complete Architecture ]
=====================================================================================================

+-------------------------------------------------------------------------------------------+
|                              [ USER REQUEST FLOW ]                                        |
|                                                                                           |
|   사용자 요청: "상품 주문하기" (HTTP POST /api/orders)                                    |
|                                                                                           |
+-------------------------------------------------------------------------------------------+
                                        │
                                        │ Trace ID: abc123 생성
                                        │ Span ID: span-001 (Root Span)
                                        ▼
+-------------------------------------------------------------------------------------------+
|                         [ SERVICE A: API Gateway ]                                        |
|                                                                                           |
|   Span: span-001                                                                          |
|   - Service: api-gateway                                                                  |
|   - Operation: POST /api/orders                                                           |
|   - Duration: 450ms                                                                       |
|   - Tags: {"user_id": "user-123", "region": "ap-northeast-2"}                            |
|   │                                                                                       |
|   │ HTTP 호출: GET /inventory (Service B)                                                |
|   │ Headers: {"traceparent": "00-abc123-span002-01"}                                     |
+-------------------------------------------------------------------------------------------+
                                        │
                                        │ Trace ID: abc123 (유지)
                                        │ Span ID: span-002
                                        │ Parent Span ID: span-001
                                        ▼
+-------------------------------------------------------------------------------------------+
|                         [ SERVICE B: Inventory Service ]                                  |
|                                                                                           |
|   Span: span-002                                                                          |
|   - Service: inventory-service                                                            |
|   - Operation: GET /inventory                                                             |
|   - Duration: 120ms                                                                       |
|   - Tags: {"product_id": "prod-456", "stock": 100}                                        |
|   │                                                                                       |
│   │ DB Query: SELECT * FROM products WHERE id = ?                                        |
│   │ Span ID: span-003 (DB Span)                                                          |
+-------------------------------------------------------------------------------------------+
                                        │
                                        │ Trace ID: abc123 (유지)
                                        │ Span ID: span-004
                                        │ Parent Span ID: span-001
                                        ▼
+-------------------------------------------------------------------------------------------+
|                         [ SERVICE C: Order Service ]                                      |
|                                                                                           |
|   Span: span-004                                                                          |
|   - Service: order-service                                                                |
|   - Operation: POST /orders                                                               |
|   - Duration: 280ms                                                                       |
│   │                                                                                       |
│   │ Kafka Publish: order-created                                                         |
│   │ Span ID: span-005 (Messaging Span)                                                   |
+-------------------------------------------------------------------------------------------+
                                        │
                                        ▼
+-------------------------------------------------------------------------------------------+
|                         [ TRACE VISUALIZATION (Jaeger UI) ]                               |
|                                                                                           |
│   +------------------+────────────────────────────────────────────────────────+            |
│   │ Trace ID: abc123 │ Time: 0ms ───────────────────────────────────────>     │            |
│   +------------------+────────────────────────────────────────────────────────+            |
│   │                                                                                  │            │
│   │ api-gateway          ████████████████████████████████████████████ (450ms)    │            │
│   │ ├─ inventory-service     ████████████ (120ms)                               │            │
│   │ │  └─ mysql                 ████ (30ms)                                     │            │
│   │ └─ order-service              ████████████████████ (280ms)                  │            │
│   │    └─ kafka                      ████ (20ms)                                │            │
│   │                                                                                  │            │
│   │ Total Duration: 450ms                                                            │            │
│   │ Critical Path: api-gateway → order-service                                      │            │
│   +---------------------------------------------------------------------------------+            |
|                                                                                           |
+-------------------------------------------------------------------------------------------+
                                        │
                                        │ 추적 데이터 Export
                                        ▼
+-------------------------------------------------------------------------------------------+
|                         [ OPENTELEMETRY COLLECTOR ]                                       |
|                                                                                           |
|  +-------------------+    +-------------------+    +-------------------+                  |
|  | Receivers         │    │ Processors       │    │ Exporters         │                  |
|  │ - OTLP            │───>│ - Batch          │───>│ - Jaeger          │                  |
|  │ - Jaeger          │    │ - Memory Limiter │    │ - Elasticsearch   │                  |
|  │ - Zipkin          │    │ - Sampling       │    │ - Prometheus      │                  |
|  +-------------------+    +-------------------+    +-------------------+                  |
|                                                                                           |
+-------------------------------------------------------------------------------------------+
                                        │
                                        ▼
+-------------------------------------------------------------------------------------------+
|                         [ STORAGE & VISUALIZATION ]                                       |
|                                                                                           |
|  +-------------------+                    +-------------------+                          |
|  | Jaeger Backend    │                    | Elasticsearch     │                          |
|  │ (Trace Storage)   │                    │ (Log & Trace      │                          |
|  │                   │                    │  Correlation)     │                          |
│  +-------------------+                    +-------------------+                          |
|           │                                       │                                      |
│           ▼                                       ▼                                      |
│  +-------------------+                    +-------------------+                          |
|  │ Jaeger UI         │                    │ Kibana            │                          |
|  │ (Trace 검색 &     │                    │ (통합 뷰)         │                          |
│  │  시각화)          │                    │                   │                          |
│  +-------------------+                    +-------------------+                          |
+-------------------------------------------------------------------------------------------+
```

### 3. 심층 동작 원리 (Context Propagation)

**1단계: Trace Context 생성 (Root Span)**
```
사용자 요청이 API Gateway에 도달하면:
1. Tracer가 새로운 Trace ID 생성: abc123def456...
2. Root Span ID 생성: span001
3. 샘플링 결정: 100% / 10% / 1% 중 하나 (성능 고려)

Trace Context:
{
  "trace_id": "abc123def456",
  "span_id": "span001",
  "parent_span_id": null,  // Root Span은 부모 없음
  "trace_flags": "01"      // 01 = sampled, 00 = not sampled
}
```

**2단계: Context Propagation (HTTP Header 전파)**
```
API Gateway → Inventory Service 호출 시:

HTTP Request Headers:
traceparent: 00-abc123def456-span002-01
├── version: 00
├── trace-id: abc123def456 (32 hex chars)
├── parent-id: span002 (16 hex chars)
└── trace-flags: 01 (sampled)

또는 B3 Header Format (Zipkin 호환):
X-B3-TraceId: abc123def456
X-B3-SpanId: span002
X-B3-ParentSpanId: span001
X-B3-Sampled: 1
```

**3단계: Span 생성 및 종료**
```java
// 각 서비스에서 Span 생성 및 종료
Span span = tracer.spanBuilder("GET /inventory")
    .setParent(parentContext)  // 부모 Context에서 Trace ID 상속
    .startSpan();

try {
    // 비즈니스 로직 수행
    Inventory inventory = inventoryRepository.findById(productId);

    // Span에 메타데이터 추가
    span.setAttribute("product.id", productId);
    span.setAttribute("stock.quantity", inventory.getQuantity());

} catch (Exception e) {
    // 에러 기록
    span.recordException(e);
    span.setStatus(StatusCode.ERROR, e.getMessage());
} finally {
    span.end();  // Span 종료 → 지속 시간 확정
}
```

**4단계: 추적 데이터 Export**
```
Span 종료 시 OpenTelemetry SDK가 Collector로 전송:

OTLP (OpenTelemetry Protocol) 메시지:
{
  "resourceSpans": [{
    "resource": {
      "attributes": [
        {"key": "service.name", "value": {"stringValue": "inventory-service"}},
        {"key": "deployment.environment", "value": {"stringValue": "production"}}
      ]
    },
    "scopeSpans": [{
      "spans": [{
        "traceId": "abc123def456",
        "spanId": "span002",
        "parentSpanId": "span001",
        "name": "GET /inventory",
        "kind": 1,  // SPAN_KIND_SERVER
        "startTimeUnixNano": 1704067200000000000,
        "endTimeUnixNano": 1704067200120000000,
        "attributes": [...]
      }]
    }]
  }]
}
```

### 4. 실무 코드 예시 (Spring Boot + OpenTelemetry)

```java
// 1. 의존성 추가 (pom.xml)
/*
<dependency>
    <groupId>io.opentelemetry.instrumentation</groupId>
    <artifactId>opentelemetry-spring-boot-starter</artifactId>
</dependency>
*/

// 2. 수동 Span 생성 (커스텀 로직 추적)
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Scope;
import org.springframework.stereotype.Service;

@Service
public class OrderService {

    private final Tracer tracer;
    private final PaymentClient paymentClient;
    private final InventoryClient inventoryClient;

    public OrderService(Tracer tracer, PaymentClient paymentClient, InventoryClient inventoryClient) {
        this.tracer = tracer;
        this.paymentClient = paymentClient;
        this.inventoryClient = inventoryClient;
    }

    public OrderResult processOrder(OrderRequest request) {
        // 자동 계측된 HTTP 요청이 이미 상위 Span 생성
        Span parentSpan = Span.current();

        // 재고 확인 Span 생성
        Span inventorySpan = tracer.spanBuilder("check_inventory")
            .setParent(parentSpan.getSpanContext())
            .startSpan();

        try (Scope scope = inventorySpan.makeCurrent()) {
            // 재고 확인 로직
            boolean available = inventoryClient.checkStock(request.getProductId());
            inventorySpan.setAttribute("inventory.available", available);

            if (!available) {
                inventorySpan.setStatus(StatusCode.ERROR, "Out of stock");
                throw new OutOfStockException("Product not available");
            }
        } finally {
            inventorySpan.end();
        }

        // 결제 처리 Span 생성
        Span paymentSpan = tracer.spanBuilder("process_payment")
            .setParent(parentSpan.getSpanContext())
            .startSpan();

        try (Scope scope = paymentSpan.makeCurrent()) {
            PaymentResult payment = paymentClient.charge(request.getPaymentInfo());
            paymentSpan.setAttribute("payment.transaction_id", payment.getTransactionId());
            paymentSpan.setAttribute("payment.amount", request.getAmount());

            return new OrderResult(payment.getTransactionId(), "SUCCESS");
        } catch (PaymentException e) {
            paymentSpan.recordException(e);
            paymentSpan.setStatus(StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            paymentSpan.end();
        }
    }
}

// 3. Kafka 메시지에 Trace Context 전파
import io.opentelemetry.context.propagation.TextMapSetter;
import org.apache.kafka.clients.producer.ProducerRecord;

public class OrderEventPublisher {

    private final KafkaProducer<String, OrderEvent> producer;
    private final Tracer tracer;

    public void publishOrderCreated(OrderEvent event) {
        Span span = tracer.spanBuilder("kafka.publish").startSpan();

        try (Scope scope = span.makeCurrent()) {
            ProducerRecord<String, OrderEvent> record = new ProducerRecord<>(
                "order-created",
                event.getOrderId(),
                event
            );

            // Trace Context를 Kafka Header에 주입
            TextMapSetter<ProducerRecord<String, OrderEvent>> setter =
                (carrier, key, value) -> carrier.headers().add(key, value.getBytes());

            OpenTelemetry.getPropagators()
                .getTextMapPropagator()
                .inject(Context.current(), record, setter);

            producer.send(record);
        } finally {
            span.end();
        }
    }
}
```

```yaml
# application.yml - OpenTelemetry 설정
opentelemetry:
  sdk:
    disabled: false
  exporter:
    otlp:
      endpoint: http://otel-collector:4317
  traces:
    exporter: otlp
  metrics:
    exporter: none  # 메트릭은 Prometheus 사용
  logs:
    exporter: none

management:
  tracing:
    sampling:
      probability: 1.0  # 프로덕션에서는 0.1 (10%) 권장
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 분산 추적 백엔드 비교표

| 평가 지표 | Jaeger | Zipkin | AWS X-Ray | Datadog APM |
| :--- | :--- | :--- | :--- | :--- |
| **라이선스** | 오픈소스 (Apache 2.0) | 오픈소스 (Apache 2.0) | AWS 전용 | 상용 |
| **저장소** | Elasticsearch, Cassandra, Kafka | Elasticsearch, Cassandra | AWS 내부 | Datadog Cloud |
| **UI 품질** | 좋음 | 보통 | 좋음 | 매우 좋음 |
| **서비스 맵** | 지원 | 제한적 | 지원 | 매우 강력 |
| **비용** | 무료 (인프라 비용만) | 무료 (인프라 비용만) | 사용량 기반 | 호스트 기준 |
| **K8s 통합** | Operator 지원 | 수동 배포 | AWS EKS 통합 | Agent 설치 |

### 2. 샘플링 전략 비교

| 샘플링 전략 | 설명 | 장점 | 단점 | 적합한 상황 |
| :--- | :--- | :--- | :--- | :--- |
| **Head-based (Probability)** | 요청 시작 시 확률적 샘플링 | 구현 단순, 오버헤드 낮음 | 중요 요청 누락 가능 | 높은 트래픽 서비스 |
| **Tail-based** | 요청 완료 후 지연/에러 기반 샘플링 | 중요 요청 보장 | 높은 메모리 사용 | 낮은 트래픽, 중요 서비스 |
| **Adaptive** | 트래픽 패턴에 따라 자동 조절 | 균형 잡힌 샘플링 | 구현 복잡 | 대규모 서비스 |

### 3. 과목 융합 관점 분석

**분산 추적 + 로그 (Trace-Log Correlation)**
- 로그에 Trace ID를 포함시켜 로그와 추적을 연결합니다.
- "이 로그는 어느 요청에서 발생했나?"를 즉시 파악합니다.

**분산 추적 + 메트릭 (RED Metrics)**
- Rate(요청 수), Errors(에러 수), Duration(지연 시간)을 추적 데이터에서 자동 생성합니다.
- SLO 계산의 기반이 됩니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 50개 서비스 중 어디서 병목인지 모르는 경우**
- **문제점**: 사용자가 "결제가 느려요"라고 불만. 50개 서비스 중 어디서 느린지 모름.
- **기술사 판단**: **분산 추적 도입 및 서비스 맵 활용**.
  1. Jaeger UI의 "Compare Traces" 기능으로 정상/지연 요청 비교.
  2. Critical Path 분석으로 병목 구간 식별.
  3. 서비스 맵으로 의존관계 시각화.

**[상황 B] 샘플링으로 인해 중요 에러가 누락되는 경우**
- **문제점**: 1% 샘플링 중 에러 발생 요청이 샘플링되지 않아 원인 분석 불가.
- **기술사 판단**: **Tail-based 샘플링 또는 에러 우선 샘플링**.
  1. 에러(Status 5xx)가 발생한 요청은 100% 샘플링.
  2. 정상 요청은 1% 샘플링.
  3. 지연(P99 초과) 요청도 100% 샘플링.

### 2. 분산 추적 도입 체크리스트

**구현 체크리스트**
- [ ] 모든 서비스에 OpenTelemetry SDK/Agent가 적용되었는가?
- [ ] HTTP, gRPC, Kafka 등 모든 통신 채널에 Context Propagation이 적용되었는가?
- [ ] 로그에 Trace ID가 포함되어 있는가?
- [ ] 서비스 이름, 버전, 환경 등 Resource Attributes가 설정되었는가?

**운영 체크리스트**
- [ ] 샘플링 비율이 트래픽과 저장소 용량에 적합한가?
- [ ] Trace 데이터 보존 기간이 규제 요구사항을 충족하는가?
- [ ] 추적 시스템 자체의 고가용성이 확보되었는가?

### 3. 안티패턴 (Anti-patterns)

**안티패턴 1: Context Propagation 누락**
- 일부 서비스에서 Trace Header를 전달하지 않음.
- **문제**: Trace가 끊어져 전체 경로를 볼 수 없음.
- **해결**: 모든 HTTP 클라이언트, 메시지 프로듀서에 Propagation 설정.

**안티패턴 2: 과도한 Span 생성**
- 모든 함수 호출마다 Span 생성.
- **문제**: 저장소 폭발, 오버헤드 증가.
- **해결**: 의미 있는 작업 단위(External API 호출, DB 쿼리)만 Span으로.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 (AS-IS) | 도입 후 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **병목 식별 시간** | 수시간 (로그 수동 연결) | 5분 이내 (Trace 검색) | **95% 단축** |
| **MTTR (평균 복구 시간)** | 4시간 | 30분 | **87% 단축** |
| **서비스 의존 파악** | 문서 기반 (구식) | 실시간 자동 매핑 | **정확도 100%** |
| **신규 팀원 온보딩** | 2주 (아키텍처 학습) | 2일 (서비스 맵 확인) | **85% 단축** |

### 2. 미래 전망 및 진화 방향

**OpenTelemetry 완전 통합**
- OpenTelemetry가 메트릭, 로그, 트레이스 통합 수집 표준으로 완성됩니다.
- 벤더 락인 없이 어떤 백엔드로도 전송 가능합니다.

**AI 기반 이상 탐지**
- AI가 정상 패턴을 학습하고, 이상한 Trace 패턴을 자동 탐지합니다.
- "평소와 다른 경로로 요청이 처리됨"을 자동 알림.

### 3. 참고 표준/가이드
- **Google Dapper 논문 (2010)**: 분산 추적 원조
- **W3C Trace Context**: HTTP Header 전파 표준
- **OpenTelemetry Specification**: 계측 및 수집 표준
- **Jaeger Documentation**: 오픈소스 구현 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **[옵저버빌리티 기초](@/studynotes/15_devops_sre/02_observability/observability_fundamentals.md)**: 분산 추적이 속한 옵저버빌리티 3대 기둥
- **[OpenTelemetry](./opentelemetry.md)**: 분산 추적 수집의 글로벌 표준
- **[Jaeger](./jaeger.md)**: 분산 추적 시각화 백엔드
- **[마이크로서비스 아키텍처](@/studynotes/04_software_engineering/01_sdlc/msa.md)**: 분산 추적이 필요한 아키텍처 패턴

---

## 👶 어린이를 위한 3줄 비유 설명
1. 분산 추적은 **'택배 송장 추적'**과 같아요. 택배가 **'서울 → 대전 → 부산'**으로 이동하는 걸 송장 번호(Trace ID)로 계속 볼 수 있죠.
2. 컴퓨터 프로그램에서는 **'요청'**이 여러 **'서비스'**를 거쳐가는데, 분산 추적이 **'어디서 늦었는지'**를 알려줘요.
3. 그래서 **"결제가 왜 느려?"**라고 물으면 **"재고 서비스에서 5초 걸렸어!"**라고 정확히 대답할 수 있어요!
