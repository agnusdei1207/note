+++
title = "이벤트 소싱 (Event Sourcing)"
date = 2026-03-05
description = "현재 상태를 덮어쓰는 대신 모든 상태 변경 이벤트를 순차적으로 저장하여 완전한 감사 추적, 시간 여행 쿼리, 이벤트 리플레이를 가능하게 하는 아키텍처 패턴 심층 분석"
weight = 138
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Event-Sourcing", "CQRS", "Event-Store", "Event-Replay", "Audit-Trail", "Temporal-Query"]
+++

# 이벤트 소싱 (Event Sourcing) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 이벤트 소싱은 애플리케이션의 상태를 현재 값이 아닌 **상태 변경 이벤트의 순차적 로그(Append-Only Log)**로 저장하여, 과거 모든 시점의 상태 복원(Time Travel), 이벤트 리플레이, 완전한 감사 추적을 가능하게 하는 데이터 영속화 패턴입니다.
> 2. **가치**: 데이터 무결성 측면에서 **100% 복구 가능**, 동시성 충돌 해결의 **원자적 해결**, 비즈니스 인텔리전스를 위한 **완전한 이력 추적**을 제공하며, CQRS와 결합 시 조회 성능을 극대화합니다.
> 3. **융합**: Apache Kafka의 로그 구조, 데이터베이스의 WAL(Write-Ahead Log), 블록체인의 불변 원장, Git의 커밋 히스토리와 개념적으로 동일하며, 이벤트 기반 마이크로서비스의 근간이 됩니다.

---

## Ⅰ. 개요 (Context & Background)

이벤트 소싱(Event Sourcing)은 Martin Fowler, Greg Young, Udi Dahan 등이 주도적으로 발전시킨 아키텍처 패턴으로, 전통적인 CRUD(Create-Read-Update-Delete) 방식의 근본적 한계를 극복하기 위해 제안되었습니다. CRUD에서는 현재 상태만 저장하므로, "어제 오후 3시에 이 계좌의 잔액은 얼마였나?"라는 질문에 답할 수 없습니다. 이벤트 소싱은 모든 변경 이력을 보존함으로써 이러한 시간적 질의를 가능하게 합니다.

**💡 비유**: 이벤트 소싱은 **'은행의 거래 내역부'**와 같습니다. 은행은 고객의 "현재 잔액"만 저장하지 않습니다. 대신 모든 입금, 출금, 이체 내역을 순서대로 기록합니다. 현재 잔액은 모든 거래 내역을 합산하여 계산할 수 있습니다. 또한 "지난달 15일 내 잔액이 얼마였나?"라는 질문에도 그 시점까지의 거래만 합산하면 답할 수 있습니다.

**등장 배경 및 발전 과정**:
1. **감사 추적의 중요성**: 금융, 의료, 공공 분야에서 모든 데이터 변경에 대한 완전한 추적이 법적 요구사항이 되었습니다. CRUD 방식으로는 이를 만족할 수 없습니다.
2. **분산 시스템의 동시성 문제**: 마이크로서비스 환경에서 낙관적 락(Optimistic Lock)의 한계를 극복하기 위해, 이벤트 소싱의 불변성이 주목받았습니다.
3. **이벤트 기반 아키텍처의 부상**: Kafka, EventStoreDB 등 이벤트 스트림 처리 기술이 성숙하면서, 이벤트를 일급 시민(First-class Citizen)으로 다루는 아키텍처가 대중화되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 이벤트 소싱 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 기술 스택 예시 | 특성 |
|---|---|---|---|
| **Event Store** | 이벤트 영속화 저장소 | EventStoreDB, Kafka, PostgreSQL | Append-Only, 불변 |
| **Aggregate** | 도메인 엔티티, 이벤트 생성/소비 | DDD Aggregate Root | 상태 비저장, 이벤트 기반 |
| **Event** | 상태 변경의 불변 팩트 | OrderCreated, PaymentProcessed | 과거 시제, 불변 |
| **Repository** | 이벤트 스트림 저장/조회 | EventSourcingRepository | 스트림 단위 저장 |
| **Projector** | 이벤트를 읽기 모델로 변환 | Event Handler, Consumer | CQRS와 연동 |
| **Saga/Process Manager** | 이벤트 기반 워크플로우 조정 | Orchestrator, Choreography | 분산 트랜잭션 |

### 정교한 구조 다이어그램: 이벤트 소싱 아키텍처

```ascii
================================================================================
                    EVENT SOURCING ARCHITECTURE
================================================================================

                          +------------------+
                          |     Command      |
                          | (CreateOrder)    |
                          +--------+---------+
                                   |
                                   v
                    +------------------------------+
                    |       Command Handler        |
                    |  1. Load Events from Store   |
                    |  2. Rebuild Aggregate State  |
                    |  3. Execute Business Logic   |
                    |  4. Generate New Events      |
                    +--------------+---------------+
                                   |
                                   v
+--------------------------------------------------------------------------------+
|                            EVENT STORE (Append-Only)                            |
|                                                                                 |
|  Stream: order-12345                                                           |
|  +------------+------------+------------+------------+------------+------------+ |
|  | Version 1  | Version 2  | Version 3  | Version 4  | Version 5  | Version 6  | |
|  | OrderCreated| ItemAdded | ItemAdded | ShippingSet| PaymentMade| OrderShipped| |
|  | timestamp: | timestamp: | timestamp: | timestamp: | timestamp: | timestamp:  | |
|  | T1         | T2         | T3         | T4         | T5         | T6          | |
|  +------------+------------+------------+------------+------------+------------+ |
|                                                                                 |
|  Stream: order-67890                                                           |
|  +------------+------------+------------+                                       |
|  | Version 1  | Version 2  | Version 3  |                                       |
|  | OrderCreated| ItemAdded | OrderCancel|                                       |
|  +------------+------------+------------+                                       |
+--------------------------------------------------------------------------------+
                                   |
                                   | Subscribe (Push/Pull)
                                   v
                    +------------------------------+
                    |       Event Processors       |
                    |  (Projectors / Sagas)        |
                    +--------------+---------------+
                                   |
          +------------------------+------------------------+
          |                        |                        |
          v                        v                        v
+------------------+      +------------------+      +------------------+
|   Read Model     |      |   Read Model     |      |   Process Manager|
|   (PostgreSQL)   |      | (Elasticsearch)  |      |   (Saga)         |
|                  |      |                  |      |                  |
| order_summary    |      | order_search_idx |      | shipping_workflow|
+------------------+      +------------------+      +------------------+

================================================================================
                    AGGREGATE STATE REBUILD (Event Replay)
================================================================================

[Command: AddItem to Order-12345]

1. Load all events for stream "order-12345":
   [OrderCreated, ItemAdded, ItemAdded, ShippingSet, PaymentMade]

2. Apply each event to empty Aggregate:

   +-------------+     OrderCreated      +-------------+
   |   Empty     | ------------------->  | status:     |
   |   Order     |                       | CREATED     |
   +-------------+                       | items: []   |
                                         +-------------+
                                               |
                                    ItemAdded  |
                                               v
                                         +-------------+
                                         | status:     |
                                         | CREATED     |
                                         | items: [A]  |
                                         +-------------+
                                               |
                                    ItemAdded  |
                                               v
                                         +-------------+
                                         | status:     |
                                         | CREATED     |
                                         | items: [A,B]|
                                         +-------------+
                                               |
                                    ShippingSet|
                                               v
                                         +-------------+
                                         | status:     |
                                         | READY       |
                                         | items: [A,B]|
                                         | addr: "Seoul"|
                                         +-------------+
                                               |
                                    PaymentMade|
                                               v
                                         +-------------+
                                         | status:     |
                                         | PAID        |
                                         | items: [A,B]|
                                         | addr: "Seoul"|
                                         | paid: $100  |
                                         +-------------+

3. Execute command on current state:
   - Validate: status == PAID (OK)
   - Generate: ItemAdded (item C)

4. Append new event to stream:
   [OrderCreated, ItemAdded, ItemAdded, ShippingSet, PaymentMade, ItemAdded(v6)]

================================================================================
                    EVENT STRUCTURE (JSON Example)
================================================================================

{
  "eventId": "550e8400-e29b-41d4-a716-446655440000",
  "eventType": "OrderCreated",
  "aggregateType": "Order",
  "aggregateId": "order-12345",
  "version": 1,
  "timestamp": "2026-03-05T10:30:00.123Z",
  "metadata": {
    "correlationId": "corr-999",
    "causationId": "cmd-888",
    "userId": "user-001"
  },
  "payload": {
    "customerId": "cust-456",
    "shippingAddress": {
      "street": "123 Main St",
      "city": "Seoul",
      "zipCode": "04524"
    },
    "currency": "KRW"
  }
}
```

### 심층 동작 원리: Snapshot 최적화

이벤트 스트림이 수천 개로 늘어나면, Aggregate 상태 복원에 시간이 오래 걸립니다. 이를 해결하기 위해 **Snapshot** 기법을 사용합니다.

```
이벤트 스트림: [E1, E2, E3, ..., E1000]

Snapshot 없이:
  1. E1부터 E1000까지 모두 리플레이
  2. 시간 복잡도: O(n)

Snapshot 사용:
  1. E500 시점의 Snapshot 로드 (상태 저장)
  2. E501부터 E1000까지만 리플레이
  3. 시간 복잡도: O(m), m << n

Snapshot 저장 전략:
  - N개 이벤트마다 자동 생성 (예: 100개마다)
  - 특정 이벤트 타입에서 생성 (예: OrderCompleted)
  - 수동 트리거
```

### 핵심 코드: 이벤트 소싱 구현 (Java/Axon Framework)

```java
// 이벤트 정의 (불변)
public class OrderCreatedEvent {
    private final String orderId;
    private final String customerId;
    private final Instant createdAt;
    private final List<OrderItem> initialItems;

    // Constructor, getters (no setters - immutable)
}

public class ItemAddedEvent {
    private final String orderId;
    private final OrderItem item;
    private final Instant addedAt;
}

// Aggregate Root (이벤트 소싱)
@Aggregate
public class Order {

    @AggregateIdentifier
    private String orderId;
    private String customerId;
    private OrderStatus status;
    private List<OrderItem> items;
    private BigDecimal totalAmount;

    // 기본 생성자
    protected Order() {
        this.items = new ArrayList<>();
    }

    // Command Handler - 생성
    @CommandHandler
    public Order(CreateOrderCommand cmd) {
        // 이벤트만 발행 (상태 변경 X)
        apply(new OrderCreatedEvent(
            cmd.getOrderId(),
            cmd.getCustomerId(),
            Instant.now(),
            cmd.getItems()
        ));
    }

    // Command Handler - 아이템 추가
    @CommandHandler
    public void handle(AddItemCommand cmd) {
        // 비즈니스 규칙 검증
        if (this.status == OrderStatus.COMPLETED || this.status == OrderStatus.CANCELLED) {
            throw new IllegalStateException("Cannot add items to " + this.status + " order");
        }

        // 중복 아이템 확인
        if (this.items.stream().anyMatch(i -> i.getProductId().equals(cmd.getItem().getProductId()))) {
            throw new IllegalArgumentException("Product already in order");
        }

        // 이벤트 발행
        apply(new ItemAddedEvent(
            cmd.getOrderId(),
            cmd.getItem(),
            Instant.now()
        ));
    }

    // Event Sourcing Handler - 상태 변경
    @EventSourcingHandler
    public void on(OrderCreatedEvent event) {
        this.orderId = event.getOrderId();
        this.customerId = event.getCustomerId();
        this.status = OrderStatus.CREATED;
        this.items = new ArrayList<>(event.getInitialItems());
        this.totalAmount = calculateTotal(this.items);
    }

    @EventSourcingHandler
    public void on(ItemAddedEvent event) {
        this.items.add(event.getItem());
        this.totalAmount = calculateTotal(this.items);
    }

    // Snapshot Trigger (100개 이벤트마다)
    @EventSourcingHandler
    @TriggerSnapshot(condition = "items.size() % 100 == 0")
    public void triggerSnapshot(Object event) {
        // Axon이 자동으로 Snapshot 생성
    }
}

// Snapshot 구조
@Revision(1)
public class OrderSnapshot {
    private String orderId;
    private String customerId;
    private OrderStatus status;
    private List<OrderItem> items;
    private BigDecimal totalAmount;
    private Instant lastModified;

    // Axon이 복원 시 사용
}
```

### 이벤트 소싱 vs CRUD 비교

| 비교 항목 | CRUD (상태 기반) | Event Sourcing (이벤트 기반) |
|---|---|---|
| **저장 방식** | 덮어쓰기 (Overwrite) | 추가 (Append) |
| **과거 상태 조회** | 불가능 | 가능 (Time Travel) |
| **감사 추적** | 별도 로그 필요 | 자동 보장 |
| **동시성 제어** | 비관적/낙관적 락 | 이벤트 버전 충돌 해결 |
| **스토리지 비용** | 낮음 | 높음 (이벤트 누적) |
| **복잡도** | 낮음 | 높음 |
| **적합한 도메인** | 단순 CRUD | 금융, 주문, 감사 |

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Event Store 구현 기술

| Event Store | 특성 | 장점 | 단점 |
|---|---|---|---|
| **EventStoreDB** | 전용 이벤트 스토어 | Competing Consumers, Projections | 학습 곡선 |
| **Apache Kafka** | 분산 로그 | 고처리량, 내구성 | 순서 보장 복잡 |
| **PostgreSQL** | RDBMS + JSONB | 친숙, 트랜잭션 | 스케일 아웃 제한 |
| **Axon Server** | Axon Framework 통합 | gRPC, Snapshot | 벤더 종속 |
| **DynamoDB** | 관리형 NoSQL | 무제한 확장 | 일관성 모델 |

### 과목 융합 관점 분석: 데이터베이스 및 보안 연계

- **데이터베이스(DB)와의 융합**: 이벤트 소싱은 데이터베이스의 **WAL(Write-Ahead Log)** 및 **Binlog**와 개념적으로 동일합니다. CDC(Change Data Capture)는 데이터베이스의 이벤트 소싱을 외부로 노출하는 기술입니다. 또한 **Materialized View**는 이벤트 소싱의 Projector와 동일한 개념입니다.

- **보안(Security)과의 융합**: 이벤트 소싱은 **감사 로그(Audit Log)**의 완벽한 구현입니다. 각 이벤트에는 `userId`, `correlationId`, `ipAddress` 등 메타데이터를 포함하여, 누가 언제 무엇을 했는지 완벽하게 추적할 수 있습니다. 이는 GDPR, SOX, HIPAA 등 규제 준수에 필수적입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 은행 계좌 관리 시스템

**문제 상황**: 은행에서 계좌 이체 시스템을 구축해야 합니다. 모든 거래 내역을 추적해야 하고, "지난달 말 내 잔액이 얼마였나?"라는 질문에 답해야 하며, 동시 이체 요청에 대한 일관성을 보장해야 합니다.

**기술사의 전략적 의사결정**:

1. **이벤트 소싱 도입**:
   - 이벤트: `AccountOpened`, `MoneyDeposited`, `MoneyWithdrawn`, `MoneyTransferred`
   - 각 이벤트에 타임스탬프, 계좌 버전, 거래 ID 포함

2. **동시성 제어**:
   - 낙관적 동시성 제어: 이벤트 버전 확인
   - 버전 충돌 시 자동 재시도 (최대 3회)

3. **Time Travel Query**:
   - 특정 시점까지의 이벤트만 리플레이하여 과거 잔액 계산
   - 일일 배치로 스냅샷 생성 (성능 최적화)

4. **규제 준수**:
   - 모든 이벤트에 사용자 ID, IP 주소, 디바이스 정보 포함
   - 이벤트 암호화 (PII 보호)

### 도입 시 고려사항 체크리스트

- **기술적 고려사항**:
  - [ ] 이벤트 스키마 버전 관리 (Upcasting)
  - [ ] Snapshot 전략 수립
  - [ ] 이벤트 삭제/보관 정책 (GDPR Right to be Forgotten)
  - [ ] 이벤트 재생(Replay) 시스템

- **운영/보안적 고려사항**:
  - [ ] 이벤트 스토어 백업 및 복구
  - [ ] 이벤트 무결성 검증 (체크섬)
  - [ ] 민감 정보 암호화
  - [ ] 이벤트 접근 통제 (RBAC)

### 안티패턴 (Anti-patterns)

1. **이벤트에 현재 상태 저장**: 이벤트는 "무엇이 변경되었는가"만 저장해야 합니다. 현재 상태 전체를 저장하면 이벤트 소싱의 이점을 잃습니다.

   ```
   잘못된 예: OrderUpdated { orderId, items: [...], totalAmount, status, ... }
   올바른 예: ItemAdded { orderId, item }
   ```

2. **이벤트 수정/삭제**: 이벤트는 불변이어야 합니다. 잘못된 이벤트는 보정 이벤트(Compensating Event)로 처리해야 합니다.

3. **과도한 Snapshot 의존**: Snapshot을 너무 자주 생성하면 스토리지 비용이 급증합니다. 적절한 주기(100~500 이벤트)를 설정해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | CRUD 기반 | Event Sourcing | 개선율/차이 |
|---|---|---|---|
| **감사 추적 커버리지** | 50~80% | 100% | 완전 추적 |
| **과거 상태 복원** | 불가능 | 가능 (Time Travel) | 질적 향상 |
| **동시성 충돌 해결** | 수동 | 자동 (이벤트 버전) | 90% 자동화 |
| **버그 재현** | 어려움 | 이벤트 리플레이 | 디버깅 효율화 |
| **스토리지 비용** | 100% | 150~300% | 비용 증가 |
| **개발 복잡도** | 낮음 | 높음 | 러닝 커브 |

### 미래 전망 및 진화 방향

1. **Serverless Event Sourcing**: AWS EventBridge, Azure Event Grid와 같은 관리형 이벤트 버스가 이벤트 소싱 인프라를 추상화하고 있습니다.

2. **Temporal.io**: 워크플로우 엔진이 이벤트 소싱을 기반으로 장기 실행 프로세스를 관리하는 표준으로 자리잡고 있습니다.

3. **Blockchain Convergence**: 블록체인의 불변 원장과 이벤트 소싱의 이벤트 로그가 융합하여, 분산형 감사 추적 시스템이 등장하고 있습니다.

### ※ 참고 표준/가이드

- **Event Store Documentation**: EventStoreDB 공식 문서
- **Axon Framework Reference**: 이벤트 소싱 구현 가이드
- **Martin Fowler - Event Sourcing**: 패턴 정의 및 설명

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [CQRS](@/studynotes/13_cloud_architecture/01_native/cqrs.md) : 이벤트 소싱과 짝을 이루는 조회 패턴
- [사가 패턴 (Saga Pattern)](@/studynotes/13_cloud_architecture/01_native/saga_pattern.md) : 이벤트 기반 분산 트랜잭션
- [CDC (Change Data Capture)](@/studynotes/13_cloud_architecture/04_data_engineering/cdc.md) : DB 변경 이벤트 캡처
- [Apache Kafka](@/studynotes/13_cloud_architecture/04_data_engineering/apache_kafka.md) : 이벤트 스트림 처리 플랫폼
- [트랜잭셔널 아웃박스](@/studynotes/13_cloud_architecture/01_native/msa.md) : 신뢰성 있는 이벤트 발행

---

### 👶 어린이를 위한 3줄 비유 설명
1. 이벤트 소싱은 **'비디오 게임의 리플레이'**와 같아요. 게임은 마지막 장면만 저장하지 않고, 모든 플레이어의 움직임을 순서대로 기록해요.
2. 그래서 "5분 전에 내가 어디 있었지?"가 궁금하면, 처음부터 5분까지만 다시 보면 돼요 (Time Travel).
3. 덕분에 게임 중에 문제가 생겨도, 녹화된 움직임을 다시 보여주면 똑같은 게임을 다시 만들 수 있어요!
