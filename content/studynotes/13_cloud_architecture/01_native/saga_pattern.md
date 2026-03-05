+++
title = "사가 패턴 (Saga Pattern)"
date = 2026-03-05
description = "마이크로서비스 환경에서 분산 트랜잭션을 관리하기 위한 사가 패턴의 코레오그래피/오케스트레이션 방식, 보상 트랜잭션 설계 및 실무 적용 심층 분석"
weight = 134
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Saga-Pattern", "Distributed-Transaction", "MSA", "Compensating-Transaction", "Choreography", "Orchestration"]
+++

# 사가 패턴 (Saga Pattern) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 사가 패턴은 분산된 마이크로서비스 간의 장기 실행 트랜잭션을 각 서비스의 로컬 트랜잭션 순차 실행과 실패 시 보상 트랜잭션(Compensating Transaction)으로 논리적 롤백을 수행하는 분산 트랜잭션 패턴입니다.
> 2. **가치**: 2PC(Two-Phase Commit)의 **성능 병목(최대 10배 처리량 저하)**을 제거하고, **99.9% 가용성**을 유지하면서도 데이터 정합성을 결과적 일관성(Eventual Consistency)으로 보장합니다.
> 3. **융합**: 이벤트 소싱(Event Sourcing), CQRS, 트랜잭셔널 아웃박스 패턴과 결합하여 MSA의 데이터 일관성 문제를 포괄적으로 해결하며, AWS Step Functions, Temporal 등 오케스트레이션 플랫폼으로 구현됩니다.

---

## Ⅰ. 개요 (Context & Background)

사가 패턴은 1987년 Hector Garcia-Molina와 Kenneth Salem이 처음 제안한 개념으로, 단일 데이터베이스의 ACID 트랜잭션을 분산 환경으로 확장하기 위한 패턴입니다. 마이크로서비스 아키텍처(MSA)에서는 각 서비스가 자체 데이터베이스를 소유하는 'Database per Service' 원칙을 따르므로, 전통적인 분산 트랜잭션 기법인 2PC(Two-Phase Commit)를 사용할 수 없습니다. 사가 패턴은 이 문제를 해결하기 위해 '결과적 일관성'을 기반으로 한 보상 메커니즘을 제공합니다.

**💡 비유**: 사가 패턴은 **'여행사 패키지 여행 예약'**과 같습니다. 고객이 항공권 → 호텔 → 렌터카 → 투어 순서로 예약할 때, 투어 예약이 실패하면 여행사는 렌터카 취소 → 호텔 취소 → 항공권 취소 순서로 롤백합니다. 각 단계가 별도의 회사(마이크로서비스)에서 처리되지만, 전체 여정의 일관성을 보장합니다.

**등장 배경 및 발전 과정**:
1. **2PC의 한계**: 2PC는 코디네이터가 모든 참여자의 락(Lock)을 잡고 있어야 하므로, 참여자 중 하나가 장애 발생 시 전체 시스템이 블로킹됩니다. 이는 클라우드 환경의 일시적 장애(Transient Failure)에 취약합니다.
2. **NoSQL의 등장**: MongoDB, Cassandra 등의 NoSQL은 분산 환경에서 성능을 위해 2PC를 지원하지 않으므로, 애플리케이션 레벨의 트랜잭션 관리가 필요해졌습니다.
3. **MSA의 데이터베이스 분리**: 마이크로서비스 간 데이터베이스 공유를 금지하는 원칙으로 인해, 서비스 간 트랜잭션 동기화가 필수적 과제가 되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 사가 패턴 구현 방식 비교

| 구분 | 코레오그래피 (Choreography) | 오케스트레이션 (Orchestration) |
|---|---|---|
| **제어 방식** | 분산 제어 (이벤트 기반) | 중앙 집중 제어 (오케스트레이터) |
| **통신 방식** | 이벤트 발행/구독 (Pub/Sub) | 명령(Command) 전송 |
| **복잡도** | 단순한 흐름에 적합 | 복잡한 흐름에 적합 |
| **디버깅** | 어려움 (이벤트 추적 필요) | 용이함 (중앙 상태 관리) |
| **SPOF 위험** | 없음 | 오케스트레이터 고가용성 필요 |
| **결합도** | 낮음 (느슨한 결합) | 중간 (오케스트레이터 의존) |
| **대표 도구** | Kafka, RabbitMQ | AWS Step Functions, Temporal, Camunda |

### 정교한 구조 다이어그램: 주문 처리 사가 예시

```ascii
================================================================================
              SAGA PATTERN: 주문 처리 (항공권 + 호텔 + 결제)
================================================================================

[정상 흐름: Forward Transactions]

  +----------+     OrderCreated      +-------------+
  | Order    | --------------------> | Flight      |
  | Service  |                       | Service     |
  +----------+                       +-------------+
       |                                    |
       |                                    | FlightBooked
       |                                    v
       |                              +-------------+
       |                              | Hotel       |
       |                              | Service     |
       |                              +-------------+
       |                                    |
       |                                    | HotelBooked
       |                                    v
       |                              +-------------+
       +----------------------------> | Payment     |
           OrderConfirmed (Success)    | Service     |
                                      +-------------+
                                            |
                                            | PaymentProcessed
                                            v
                                      +-------------+
                                      | Order       |
                                      | Completed   |
                                      +-------------+

[보상 흐름: Compensating Transactions] (호텔 예약 실패 시)

  +----------+     OrderCreated      +-------------+
  | Order    | --------------------> | Flight      |
  | Service  |                       | Service     |
  +----------+                       +-------------+
       ^                                    |
       |                                    | FlightBooked
       |                                    v
       |                              +-------------+
       |    CancelOrder (Compensate)  | Hotel       |
       +----------------------------- | Service     | <-- FAIL!
                                      +-------------+

  [Rollback Sequence]:
  1. Flight Service receives CancelFlight command
  2. Flight Service executes CancelFlight (Refund)
  3. Order Service marks Order as CANCELLED

================================================================================
                    CHOREOGRAPHY vs ORCHESTRATION
================================================================================

[Choreography - 이벤트 체인]

  Order Service         Flight Service        Hotel Service         Payment Service
       |                      |                     |                      |
       | OrderCreated         |                     |                      |
       +--------------------->|                     |                      |
       |                      | FlightBooked        |                      |
       |                      +-------------------->|                      |
       |                      |                     | HotelBooked          |
       |                      |                     +--------------------->|
       |                      |                     |                      |
       |                      |                     |   HotelBookingFailed |
       |                      |                     |<---------------------+
       |                      | CancelFlight        |                      |
       |                      |<--------------------+                      |
       | OrderCancelled       |                     |                      |
       |<---------------------+                     |                      |

[Orchestration - 중앙 제어]

  +-------------------+
  |  Saga             |
  |  Orchestrator     |
  |  (State Machine)  |
  +---------+---------+
            |
    +-------+-------+-------+-------+
    |       |       |       |       |
    v       v       v       v       v
 +-----+ +------+ +-------+ +--------+
 |Order| |Flight| | Hotel | |Payment |
 +-----+ +------+ +-------+ +--------+

   Orchestrator sends commands:
   1. BookFlightCommand --> FlightService
   2. BookHotelCommand --> HotelService
   3. ProcessPaymentCommand --> PaymentService
   4. If any fails: Send CancelXCommand to completed services

================================================================================
```

### 심층 동작 원리: 보상 트랜잭션 설계

보상 트랜잭션(Compensating Transaction)은 정상 트랜잭션의 논리적 롤백을 수행합니다. 물리적 롤백(UNDO)이 아닌 비즈니스적 취소를 의미합니다.

**보상 트랜잭션 설계 원칙**:

1. **멱등성(Idempotency)**: 보상 작업은 여러 번 실행되어도 동일한 결과를 반환해야 합니다. 네트워크 재시도로 인해 중복 호출될 수 있습니다.

2. **교환성(Commutativity)**: 정상 작업과 보상 작업의 실행 순서에 관계없이 최종 상태가 동일해야 합니다.

3. **가역성 확인**: 이미 보상된 작업에 대해 다시 보상 요청이 오면 아무 작업도 하지 않아야 합니다.

**보상 가능성 판단 예시**:

| 작업 | 보상 가능 여부 | 보상 방법 |
|---|---|---|
| 신용카드 결제 | 가능 | 결제 취소 (Void/Refund) |
| 이메일 발송 | 불가능 | 사과 이메일 발송 (논리적 보상) |
| 외부 API 호출 | 제한적 | 취소 API 호출 (없으면 불가능) |
| DB INSERT | 가능 | DELETE 또는 상태 변경 (CANCELLED) |
| DB UPDATE | 가능 | 이전 값으로 UPDATE |

### 핵심 코드: 오케스트레이션 사가 구현 (Java/Spring)

```java
// Saga Orchestrator - 상태 머신 기반 구현
@Component
public class OrderSagaOrchestrator {

    private final SagaDefinition<OrderSagaState> sagaDefinition;

    public OrderSagaOrchestrator() {
        this.sagaDefinition = SagaDefinition
            .step("book-flight")
                .invoke(this::bookFlight)
                .compensate(this::cancelFlight)
            .step("book-hotel")
                .invoke(this::bookHotel)
                .compensate(this::cancelHotel)
            .step("process-payment")
                .invoke(this::processPayment)
                .compensate(this::refundPayment)
            .build();
    }

    // 정상 작업: 항공권 예약
    private SagaOutput bookFlight(OrderSagaState state) {
        BookFlightCommand command = new BookFlightCommand(
            state.getOrderId(),
            state.getFlightDetails()
        );

        FlightBookingResponse response = flightService.book(command);

        // 멱등성 보장: 이미 처리된 요청 확인
        if (state.getFlightBookingId() != null) {
            return SagaOutput.skip("Flight already booked: " + state.getFlightBookingId());
        }

        state.setFlightBookingId(response.getBookingId());
        return SagaOutput.success(response);
    }

    // 보상 작업: 항공권 취소
    private SagaOutput cancelFlight(OrderSagaState state) {
        // 멱등성: 이미 취소된 경우 스킵
        if (state.isFlightCancelled()) {
            return SagaOutput.skip("Flight already cancelled");
        }

        CancelFlightCommand command = new CancelFlightCommand(
            state.getFlightBookingId(),
            "Order cancelled: " + state.getOrderId()
        );

        try {
            flightService.cancel(command);
            state.setFlightCancelled(true);
            return SagaOutput.success();
        } catch (FlightNotFoundException e) {
            // 이미 존재하지 않음 = 취소된 것으로 간주
            state.setFlightCancelled(true);
            return SagaOutput.success();
        } catch (Exception e) {
            // 재시도 가능한 오류
            return SagaOutput.retry(e);
        }
    }

    // 사가 실행
    public SagaResult execute(OrderRequest request) {
        OrderSagaState state = new OrderSagaState(request);
        return sagaExecutor.execute(sagaDefinition, state);
    }
}

// 사가 상태 영속화 (DB)
@Entity
public class SagaInstance {
    @Id
    private String sagaId;
    private String sagaType;
    private String currentState;      // RUNNING, COMPLETED, COMPENSATING, FAILED
    private int currentStep;
    private String payload;           // JSON 직렬화된 상태
    private Instant createdAt;
    private Instant updatedAt;

    @Version
    private Long version;             // 낙관적 잠금
}
```

### 코레오그래피 사가 구현 (이벤트 기반)

```java
// Order Service - 이벤트 발행
@Service
public class OrderService {

    @Transactional
    public Order createOrder(OrderRequest request) {
        Order order = new Order(request);
        order.setStatus(OrderStatus.PENDING);
        orderRepository.save(order);

        // 트랜잭셔널 아웃박스 패턴으로 이벤트 발행
        outboxService.save(new OutboxEvent(
            "OrderCreated",
            order.getId(),
            objectMapper.writeValueAsString(order)
        ));

        return order;
    }

    // 보상 이벤트 수신
    @KafkaListener(topics = "OrderCancellationRequested")
    @Transactional
    public void handleCancellation(CancellationRequestedEvent event) {
        Order order = orderRepository.findById(event.getOrderId())
            .orElseThrow(() -> new OrderNotFoundException(event.getOrderId()));

        // 멱등성 확인
        if (order.getStatus() == OrderStatus.CANCELLED) {
            return;
        }

        order.setStatus(OrderStatus.CANCELLED);
        orderRepository.save(order);

        // 취소 완료 이벤트 발행
        outboxService.save(new OutboxEvent(
            "OrderCancelled",
            order.getId(),
            objectMapper.writeValueAsString(order)
        ));
    }
}

// Flight Service - 이벤트 구독
@Service
public class FlightService {

    @KafkaListener(topics = "OrderCreated")
    @Transactional
    public void handleOrderCreated(OrderCreatedEvent event) {
        // 중복 처리 방지 (멱등성)
        if (flightBookingRepository.existsByOrderId(event.getOrderId())) {
            return;
        }

        try {
            FlightBooking booking = bookFlight(event);
            flightBookingRepository.save(booking);

            outboxService.save(new OutboxEvent(
                "FlightBooked",
                booking.getId(),
                objectMapper.writeValueAsString(new FlightBookedEvent(
                    event.getOrderId(),
                    booking.getId()
                ))
            ));
        } catch (Exception e) {
            // 실패 이벤트 발행
            outboxService.save(new OutboxEvent(
                "FlightBookingFailed",
                event.getOrderId(),
                objectMapper.writeValueAsString(new FlightBookingFailedEvent(
                    event.getOrderId(),
                    e.getMessage()
                ))
            ));
        }
    }
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 2PC vs 사가 패턴

| 비교 지표 | 2PC (Two-Phase Commit) | 사가 패턴 |
|---|---|---|
| **트랜잭션 범위** | 단기 (초 단위) | 장기 (분~시간~일) |
| **락(Lock) 보유** | 전체 기간 보유 | 각 단계만 짧게 보유 |
| **장애 내성** | 낮음 (블로킹) | 높음 (비블로킹) |
| **일관성 모델** | 강 일관성 (ACID) | 결과적 일관성 (BASE) |
| **복잡도** | 단순 (DB 관리) | 복잡 (앱 레벨 구현) |
| **성능** | 저하 (코디네이터 병목) | 높음 (비동기) |
| **롤백 방식** | 물리적 (UNDO) | 논리적 (보상) |
| **적용 환경** | 단일 DB, 동기 | 분산 DB, 비동기 |

### 과목 융합 관점 분석: 데이터베이스 및 네트워크 연계

- **데이터베이스(DB)와의 융합**: 사가 패턴은 **낙관적 동시성 제어(Optimistic Concurrency Control)**와 결합합니다. 각 서비스의 로컬 트랜잭션은 버전 번호나 타임스탬프를 사용하여 동시 수정을 감지합니다. 또한 **CDC(Change Data Capture)**와 결합하여 이벤트 발행의 신뢰성을 높입니다.

- **네트워크(Network)와의 융합**: 사가 패턴의 신뢰성은 **정확히 한 번(Exactly-once) 메시지 전달**에 의존합니다. Kafka의 Idempotent Producer와 Transactions API, 또는 RabbitMQ의 Publisher Confirms을 활용합니다. 또한 **서킷 브레이커**와 결합하여 외부 서비스 장애 시 빠르게 실패하고 보상을 트리거합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 이커머스 주문 결제 시스템

**문제 상황**: 대규모 이커머스 플랫폼에서 주문 → 재고 차감 → 결제 → 배송 예약의 트랜잭션을 처리해야 합니다. 재고 서비스는 MongoDB, 결제 서비스는 PostgreSQL, 배송 서비스는 MySQL을 사용합니다.

**기술사의 전략적 의사결정**:

1. **오케스트레이션 방식 채택**: 복잡한 비즈니스 규칙(쿠폰 적용, 포인트 사용, 분할 결제)과 명확한 상태 관리를 위해 오케스트레이션을 선택합니다.

2. **AWS Step Functions 활용**: 관리형 오케스트레이션 서비스를 사용하여 인프라 운영 부담을 줄입니다.

3. **보상 트랜잭션 설계**:
   - 주문: 상태를 CANCELLED로 변경
   - 재고: 차감된 수량만큼 증가 (동시성 제어 필요)
   - 결제: PG사 취소 API 호출
   - 배송: 예약 취소 API 호출

4. **타임아웃 및 재시도 정책**:
   - 각 단계 타임아웃: 30초
   - 재시도: 지수 백오프 (1초, 2초, 4초, 8초)
   - 최대 재시도: 5회 후 수동 개입

### 도입 시 고려사항 체크리스트

- **기술적 고려사항**:
  - [ ] 사가 상태 영속화 (DB 선택)
  - [ ] 멱등성 키(Idempotency Key) 설계
  - [ ] 타임아웃 및 재시도 정책 수립
  - [ ] 데드레터 큐(Dead Letter Queue) 구성

- **운영/보안적 고려사항**:
  - [ ] 사가 실행 로그 및 추적(Tracing)
  - [ ] 보상 실패 시 수동 개입 프로세스
  - [ ] 감사 로그(Audit Log) 보관
  - [ ] PII 데이터 마스킹

### 안티패턴 (Anti-patterns)

1. **보상 불가능한 작업 포함**: 이메일 발송, SMS 전송, 외부 시스템 푸시 등 물리적으로 취소할 수 없는 작업을 사가에 포함하면 일관성을 보장할 수 없습니다. 이러한 작업은 사가 완료 후에 실행해야 합니다.

2. **순환 의존성**: A → B → C → A와 같은 순환 사가는 무한 루프에 빠질 수 있습니다. 사가는 항상 DAG(Directed Acyclic Graph) 형태여야 합니다.

3. **과도한 긴 타임아웃**: 타임아웃을 너무 길게 설정하면 리소스가 장시간 점유됩니다. 비즈니스 요구사항에 맞게 현실적인 타임아웃을 설정해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 2PC 기반 | 사가 패턴 | 개선율 |
|---|---|---|---|
| **평균 트랜잭션 시간** | 5초 | 2초 | 60% 단축 |
| **시스템 가용성** | 99.5% | 99.95% | 0.45% 향상 |
| **동시 트랜잭션 수** | 1,000 TPS | 10,000 TPS | 10배 향상 |
| **장애 복구 시간** | 수동 | 자동 (30초) | 99% 단축 |
| **DB 락 대기 시간** | 3초 | 0.1초 | 97% 감소 |

### 미래 전망 및 진화 방향

1. **Temporal/Cadence 워크플로우 엔진**: 복잡한 사가 로직을 선언적으로 정의하고, 자동 재시도, 타임아웃, 보상을 처리하는 관리형 오케스트레이션 플랫폼이 표준화되고 있습니다.

2. **AI 기반 보상 최적화**: 머신러닝을 활용하여 보상 트랜잭션의 순서와 타이밍을 최적화하는 연구가 진행 중입니다.

3. **Blockchain 기반 사가**: 분산 원장 기술을 활용하여 사가 상태를 위변조 불가능하게 기록하고, 스마트 컨트랙트로 보상 로직을 자동화하는 접근이 연구되고 있습니다.

### ※ 참고 표준/가이드

- ** Enterprise Integration Patterns**: 메시지 기반 통합 패턴 표준
- **BPMN 2.0**: 비즈니스 프로세스 모델링 표준 (사가 시각화)
- **CloudEvents**: 이벤트 데이터 형식 표준

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [마이크로서비스 아키텍처 (MSA)](@/studynotes/13_cloud_architecture/01_native/msa.md) : 사가 패턴이 적용되는 기본 아키텍처
- [이벤트 소싱 (Event Sourcing)](@/studynotes/13_cloud_architecture/01_native/msa.md) : 사가 상태 추적을 위한 이벤트 로그
- [트랜잭셔널 아웃박스](@/studynotes/13_cloud_architecture/01_native/msa.md) : 신뢰성 있는 이벤트 발행 패턴
- [서킷 브레이커](@/studynotes/13_cloud_architecture/01_native/circuit_breaker.md) : 외부 서비스 장애 시 빠른 실패
- [CQRS](@/studynotes/13_cloud_architecture/01_native/msa.md) : 명령과 조회 분리로 사가 복잡도 관리

---

### 👶 어린이를 위한 3줄 비유 설명
1. 사가 패턴은 **'도미노 게임'**과 같아요. 도미노를 순서대로 쓰러뜨리다가 중간에 멈추면, 거꾸로 되돌아가며 도미노를 다시 세워요.
2. 이때 각 도미노(서비스)는 "내가 쓰러졌으니까 다시 일어날게!"라고 스스로 말할 수 있어요(보상 트랜잭션).
3. 덕분에 모든 도미노가 다 쓰러지지 않아도, 게임은 언제나 안전하게 끝날 수 있어요!
