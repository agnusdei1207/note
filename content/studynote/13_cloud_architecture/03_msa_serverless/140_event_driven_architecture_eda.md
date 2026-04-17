+++
weight = 140
title = "이벤트 기반 아키텍처 (EDA, Event-Driven Architecture)"
date = "2024-03-20"
[extra]
categories = "studynote-cloud"
+++

## 핵심 인사이트 (3줄 요약)
1. EDA는 시스템의 상태 변화(Event)를 감지하고, 이를 비동기적으로 발행/구독(Pub/Sub)하여 동작하는 소프트웨어 설계 패러다임이다.
2. 서비스 간 직접 호출 대신 메시지 브로커를 거치므로 결합도(Coupling)를 극도로 낮추고, 개별 서비스의 독립적 확장과 장애 격리를 실현한다.
3. 데이터의 최종 일관성(Eventual Consistency)을 수용하며, 실시간 데이터 처리와 복잡한 비즈니스 워크플로우를 유연하게 구현하는 클라우드 네이티브의 핵심 구조다.

### Ⅰ. 개요 (Context & Background)
전통적인 요청-응답(Request-Response) 방식은 호출자가 수신자의 응답을 기다려야 하는 동기(Blocking) 구조로, 수신 서비스 장애 시 호출자까지 마비되는 '연쇄 장애' 위험이 크다. 마이크로서비스(MSA)가 수백 개로 늘어나는 현대적 환경에서는 이러한 강결합을 끊기 위해 '이벤트'를 매개로 소통하는 아키텍처가 필수적이다. 이는 "주문이 완료되었습니다"라는 외침(Event)만 던지고, 필요한 팀(배송, 알림, 재고)들이 알아서 각자의 일을 하는 방식이다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
EDA는 이벤트 생산자, 이벤트 채널, 이벤트 소비자라는 세 가지 핵심 요소로 구성된다.

```text
[EDA Core Components & Flow]
+-----------------+      +-----------------+      +-----------------+
| Event Producer  |      |  Event Channel  |      | Event Consumer  |
| (State Change)  |      | (Message Broker)|      | (Action/Logic)  |
+-------+---------+      +-------+---------+      +-------+---------+
        |                        |                        |
  [Publish Event] =======> [ Topic/Queue ] =======> [Subscribe/Push]
        |                        |                        |
+-------V---------+      +-------V---------+      +-------V---------+
| Order Service   |      | Apache Kafka    |      | Shipping Service|
| (Order Created) |      | RabbitMQ / SQS  |      | (Start Delivery)|
+-----------------+      +-----------------+      +-----------------+
  * Characteristics: Asynchronous, Decoupled, Distributed
```

1. **이벤트 (Event)**: 상태의 변화를 나타내는 불변의 기록(예: OrderPlaced, PaymentFailed).
2. **이벤트 채널 (Message Broker)**: 생산자와 소비자를 중계하는 인프라. 메시지를 영속적으로 보관하고 분산 전송을 보장한다. (Kafka, RabbitMQ, SNS/SQS)
3. **작동 방식**:
   - **발행/구독 (Pub/Sub)**: 1:N 통신 가능. 하나의 이벤트에 여러 소비자 반응.
   - **이벤트 스트리밍**: 실시간으로 발생하는 대량의 이벤트를 순차적으로 처리.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 요청-응답 (Request-Response) | 이벤트 기반 (EDA) |
| :--- | :--- | :--- |
| **통신 방식** | 동기 (Synchronous / Blocking) | 비동기 (Asynchronous / Non-blocking) |
| **결합도** | 강결합 (상대방 주소/상태 알아야 함) | 느슨한 결합 (이벤트 내용만 알면 됨) |
| **장애 영향** | 수신자 장애 시 송신자 대기/실패 | 브로커에 메시지 저장 후 나중에 처리 가능 |
| **데이터 일관성** | 즉각적 일관성 (ACID) | 최종 일관성 (Eventual Consistency) |
| **적합성** | 단순 조회, 실시간 확답 필수 업무 | 복잡한 연쇄 처리, 실시간 분석, MSA |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **아키텍트의 판단**: EDA 도입 시 가장 큰 도전은 '추적성(Traceability)'과 '디버깅'이다. 메시지가 어디서 막혔는지 파악하기 어렵기 때문에 **분산 추적(Distributed Tracing)**과 **상관관계 ID(Correlation ID)** 도입이 필수적이다.
- **전략적 제언**: 메시지 유실이나 중복 처리를 방지하기 위해 **멱등성(Idempotency) 설계**와 **Transactional Outbox 패턴**을 적용하여 데이터 정합성을 보장해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
EDA는 시스템을 유연하고 탄력적으로 만든다. 미래의 EDA는 단순한 비동기 통신을 넘어, **이벤트 소싱(Event Sourcing)** 및 **서버리스(FaaS)**와 결합하여 인프라 비용을 최적화하고 초거대 분산 시스템을 지능적으로 제어하는 신경망 역할을 수행할 것이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 마이크로서비스 아키텍처 (MSA), 클라우드 네이티브
- **하위 개념**: Pub/Sub, 메시지 브로커, 비동기 통신
- **연관 개념**: 사가 패턴 (Saga), 이벤트 소싱, CQRS, 최종 일관성

### 👶 어린이를 위한 3줄 비유 설명
1. EDA는 방송국에서 "내일 비가 옵니다!"라고 뉴스(이벤트)를 전하는 것과 같아요.
2. 방송국은 누가 듣는지 몰라도 그냥 방송만 하고, 우산 장수나 농부 아저씨는 그 방송을 듣고(구독) 각자 할 일을 준비하죠.
3. 서로 전화를 걸어 일일이 알려주지 않아도 방송 한 번으로 모든 사람이 동시에 움직일 수 있는 편리한 방법이랍니다.
