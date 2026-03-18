+++
title = "트랜잭셔널 아웃박스 (Transactional Outbox) 패턴"
description = "로컬 DB 상태 변경과 메시지 브로커로의 이벤트 발행 간의 완벽한 원자성(Atomicity)을 보장하기 위한 분산 아키텍처 내결함성 패턴"
weight = 196
+++

# 트랜잭셔널 아웃박스 (Transactional Outbox) 패턴

> **약어 (Abbreviation)**: Transactional Outbox (Pattern for reliable messaging and state synchronization)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트랜잭셔널 아웃박스 (Transactional Outbox) 패턴은 비즈니스 데이터(예: 주문)와 이벤트 메시지(예: 주문 생성됨)를 **동일한 로컬 데이터베이스 트랜잭션** 내에서 아웃박스(Outbox) 테이블에 함께 저장하여 두 작업의 **원자성(Atomicity)**을 100% 보장하는 기법이다.
> 2. **가치**: 마이크로서비스 간 비동기 통신 시 흔히 발생하는 "DB 커밋은 성공했으나 이벤트 발행 중 네트워크 오류로 메시지가 유실되는(Message Loss)" 치명적인 데이터 불일치 문제를 근본적으로 해결한다.
> 3. **융합**: 저장된 아웃박스 이벤트를 읽어 브로커로 전달하기 위해 **Message Relay** 기술이 필수적이며, 주로 **CDC (Change Data Capture, 예: Debezium)** 기반의 로그 후행 처리기(Log Tailing)와 강력한 시너지를 낸다.

---

## Ⅰ. 개요 (Context & Background)

- **개념**: 서비스가 상태를 변경하고 그 사실을 외부로 알릴 때, "상태 변경"과 "메시지 발송"이라는 이기종 간의 분산 트랜잭션을 회피하기 위해 "보낼 메시지를 일단 내 DB(Outbox)에 안전하게 적어두고 나중에 전송하는" 설계 방식이다.
- **💡 비유**: 편지를 우체통(Outbox)에 안전하게 넣는 것까지만 내 책임(트랜잭션)으로 하고, 나중에 우체부(Message Relay)가 우체통에서 편지를 수거해 알아서 배달하게 만드는 것과 같습니다.
- **등장 배경**:
  - **기존 한계 (Dual Write Problem)**: 과거에는 RDBMS 커밋 코드 바로 다음 줄에 Kafka 전송 코드를 적었다(이중 쓰기). 그러나 DB 커밋 직후 서버가 죽거나 브로커와 네트워크 단절이 생기면 데이터는 저장됐는데 메시지는 발행되지 않는 "이벤트 유실"이 발생했다.
  - **혁신적 패러다임**: 2PC(Two-Phase Commit)의 무거운 락(Lock) 없이 원자성을 보장하기 위해, 이기종 간 트랜잭션을 포기하고 단일 RDBMS의 ACID 트랜잭션 능력에 메시지 발행 책임을 의탁하는 발상의 전환이 일어났다.
  - **현재의 비즈니스 요구**: Event-Driven Architecture (EDA) 기반의 MSA에서 이벤트 전파의 무결성이 전체 시스템의 정합성을 좌우하므로, 결제·주문 등 금융권과 이커머스의 코어 시스템에서 필수 표준으로 자리 잡았다.

> 다음은 기존의 이중 쓰기(Dual Write) 문제와 이를 해결하는 Outbox 패턴의 개념적 차이를 보여주는 비교 도식이다.

```text
┌─────────────────────────────────────────────────────────────┐
│ [Dual Write Problem vs Transactional Outbox]                │
├────────────────────────────┬────────────────────────────────┤
│ 1. Dual Write (위험)       │ 2. Outbox Pattern (안전)       │
│                            │                                │
│ [App]                      │ [App]                          │
│  │ 1. DB Commit            │  │ 1. Transaction Start        │
│  ├──> [DB] (성공)          │  ├──> [Order Table] Write      │
│  │                         │  ├──> [Outbox Table] Write     │
│  │ 2. Publish (Network Err)│  │ 2. Transaction Commit       │
│  └──x [Kafka] (실패/유실)  │  └──> (DB와 Outbox 동시 성공)  │
│                            │                                │
│ 결과: DB엔 주문있고 Kafka엔│ 결과: 유실률 0%, 이후 Relay가  │
│       없음 (데이터 불일치) │ Outbox를 읽어 브로커로 전송    │
└────────────────────────────┴────────────────────────────────┘
```
- **해설**: 이중 쓰기 구조에서는 네트워크 지연으로 인해 1번과 2번 사이에서 원자성이 깨질 확률이 항상 존재한다. 반면 Outbox 패턴은 RDBMS의 단일 트랜잭션을 활용하므로 "주문은 저장됐는데 아웃박스 기록은 실패하는" 부분 성공(Partial Success) 상황이 기술적으로 원천 차단된다.

> **📢 섹션 요약 비유**: 이메일 앱에서 전송 버튼을 누를 때 네트워크가 끊겨도, 앱이 내부 '보낼 편지함(Outbox)' 폴더에 이메일을 저장해두었다가 인터넷이 연결되면 자동으로 발송하는 원리와 동일합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소

| 요소명 | 역할 | 내부 동작 | 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Business Table** | 도메인 상태 저장 | 주문, 결제 등 실제 비즈니스 데이터를 Insert/Update | RDBMS / NoSQL | 물건 보관 창고 |
| **Outbox Table** | 발송 대기 메시지 저장 | 이벤트의 페이로드, 토픽명, 발행 상태를 Business Table과 같은 트랜잭션으로 Insert | RDBMS / NoSQL | 발송 대기 우체통 |
| **Message Relay** | 아웃박스 수거 및 발행 | Outbox 테이블을 주기적으로 읽어 브로커로 메시지를 전송하고 처리 완료 마킹 | Polling, CDC | 우체부 |
| **Message Broker** | 이벤트 라우팅 | Relay로부터 수신한 메시지를 구독자에게 비동기 전달 | Kafka, RabbitMQ | 우체국 물류 센터 |
| **Local Transaction** | 원자성 보장 매커니즘 | Business와 Outbox 테이블의 쓰기 작업을 1개의 Connection 단위로 묶음 | JDBC, R2DBC | 자물쇠 |

### 2. 메시지 릴레이(Message Relay)의 두 가지 구현 방식

아웃박스에 쌓인 데이터를 브로커로 퍼나르는 방식에는 크게 두 가지가 존재한다.

> 아래는 Polling Publisher 방식과 CDC (Change Data Capture) 기반 Transaction Log Tailing 방식의 동작 흐름을 보여주는 아키텍처 다이어그램이다.

```text
[Message Relay Strategies]

[A] Polling Publisher 방식 (단순, 부하 있음)
   ┌──────────────────────┐
   │ [Local DB]           │
   │ 1. Order Table       │<--- (Tx) --- [Application]
   │ 2. Outbox Table      │
   └──────────┬───────────┘
              │ (SELECT * FROM Outbox WHERE status='READY')
              v
       [Polling Batch] (1초마다 주기적 조회)
              │
              v
       [[ Message Broker ]]


[B] CDC 기반 Log Tailing 방식 (고성능, 복잡함)
   ┌──────────────────────┐
   │ [Local DB]           │
   │ - Order Table        │<--- (Tx) --- [Application]
   │ - Outbox Table       │
   │ ▷ Transaction Log(Binlog/WAL) ◁
   └──────────┬───────────┘
              │ (Event Stream: row 변경분 감지)
              v
       [Debezium / Kafka Connect] (CDC 엔진)
              │
              v
       [[ Message Broker ]]
```
- **해설**:
  - **Polling 방식**: 애플리케이션 내의 스케줄러가 짧은 주기로 Outbox 테이블을 `SELECT`하여 메시지를 브로커에 쏘고 `UPDATE`로 상태를 완료 처리한다. 구현이 쉽지만, 트래픽이 많을 경우 DB에 잦은 조회 쿼리로 부하(Overhead)를 준다.
  - **CDC 방식 (Log Tailing)**: MySQL의 `binlog`나 PostgreSQL의 `WAL` 같은 트랜잭션 로그를 Debezium 같은 CDC 도구가 훔쳐보며 브로커로 즉시 전송한다. DB에 조회 쿼리 부하를 주지 않아 성능이 압도적이며, 딜레이가 ms 단위로 짧다.

### 3. 심층 동작 원리 (CDC 기반 처리)

1. **Transaction Begin**: 애플리케이션이 RDBMS 트랜잭션을 연다.
2. **Business Update**: `Order` 테이블에 신규 주문 행을 생성한다.
3. **Outbox Insert**: 동일한 트랜잭션 컨텍스트 안에서, `Outbox` 테이블에 `{"topic":"order-events", "payload":"{...}"}` 형태로 행을 삽입한다.
4. **Transaction Commit**: 두 작업이 하나의 원자성으로 커밋된다.
5. **Log Generation**: DB 엔진은 내부적으로 커밋된 내역을 `binlog` 파일에 순차 기록한다.
6. **CDC Tailing**: 백그라운드에 떠 있는 Debezium 커넥터가 `binlog`의 변경을 즉시 감지하여 Kafka의 지정된 토픽으로 이벤트를 스트리밍(Publish)한다.

> **📢 섹션 요약 비유**: 폴링(Polling) 방식이 우체부가 매분마다 우체통을 열어보며 새 편지가 있나 확인하는 것이라면, CDC 방식은 우체통에 편지가 떨어지는 순간 센서가 작동해 우체부에게 알림을 쏴주는 스마트 우체통과 같습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 분산 트랜잭션 해법 비교 (2PC vs Outbox)

| 비교 항목 | Two-Phase Commit (2PC) | Transactional Outbox + CDC | 설계 시 판단 기준 |
|:---|:---|:---|:---|
| **일관성 수준** | 강한 일관성 (Strong Consistency) | 결과적 일관성 (Eventual Consistency) | 실시간 동기화 필요 여부 |
| **블로킹/성능** | 매우 큼 (양쪽 완료 전까지 자원 락) | 없음 (로컬 커밋 후 즉시 반환, 비동기) | 시스템 전체의 처리량(Throughput) 요구치 |
| **장애 전파** | 타 시스템 장애 시 내 시스템도 대기(SPOF) | 브로커가 다운되어도 내 DB 트랜잭션은 성공 | 마이크로서비스 격리(Isolation) 수준 |
| **구현 복잡도** | 레거시 미들웨어 의존, NoSQL 지원 불가 | CDC 인프라(Debezium 등) 구축 비용 높음 | 인프라 운영 역량 |

### 2. At-Least-Once (최소 한 번) 전달과 멱등성(Idempotency)의 시너지
아웃박스 패턴은 구조적으로 "최소 한 번(At-Least-Once)" 메시지 전달을 보장한다. 만약 Message Relay가 Kafka로 메시지를 전송하고 응답(ACK)을 받기 직전에 죽는다면, 재시작 시 동일한 메시지를 다시 전송하게 되어 중복(Duplicate) 메시지가 발생한다. 
따라서 이 패턴을 적용할 때는 **수신자(Subscriber) 측의 멱등성 보장 로직**이 반드시 세트로 묶여야만 완벽한 아키텍처가 완성된다.

> 다음은 아웃박스에서 발생할 수 있는 중복 전달 문제와 수신자 측의 멱등성 검증 구조를 보여주는 상태 전이도이다.

```text
[At-Least-Once & Idempotency Synergy]

[Outbox Relay] ──(Msg: ID=123)──> [[ Broker ]] ──> [Subscriber]
    |                                                |
  (Network 끊김, ACK 수신 실패)                      | 1. DB 조회 (ID=123 존재함?)
    |                                                | 2. 존재 안 함 -> 로직 처리 후 DB 저장
  (재시도)                                           |
[Outbox Relay] ──(Msg: ID=123)──> [[ Broker ]] ──> [Subscriber]
                                                     |
                                                     | 1. DB 조회 (ID=123 존재함?)
                                                     | 2. 이미 존재함! -> (무시/스킵)
```
- **해설**: 아웃박스는 메시지 유실을 막는 창이고, 멱등성은 메시지 중복을 막는 방패다. 이 두 가지가 결합되어야만 Eventual Consistency(결과적 일관성)를 완벽하게 달성할 수 있다.

> **📢 섹션 요약 비유**: 우체부가 편지 배달 여부가 헷갈려 같은 내용의 편지를 두 번 넣을 수 있지만(At-Least-Once), 편지를 받는 사람은 내용이 같으면 하나는 쿨하게 버리는(멱등성) 지혜가 필요합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오와 의사결정
- **상황**: MSA 기반 핀테크 서비스에서 송금 승인 트랜잭션을 처리해야 함. 송금 상태를 '완료'로 바꾸는 즉시 '푸시 알림 서버'로 이벤트를 보내야 하는데, 알림 서버 장애로 인해 송금 트랜잭션 자체가 실패해서는 안 됨.
- **판단**: 완벽한 격리와 데이터 무결성이 필요하다. **Transactional Outbox 패턴**을 도입하여 송금 테이블과 Outbox 테이블에 트랜잭션을 묶어 기록한다. 발송은 별도의 CDC(Debezium)가 백그라운드에서 담당하게 하여 알림 서버의 지연/장애가 핵심 금융 트랜잭션에 영향을 주지 않도록(Decoupling) 아키텍처를 설계한다.

### 2. 도입 시 핵심 체크리스트 (Technical & Operational)
1. **아웃박스 테이블 정리 (Housekeeping)**: 처리 완료된 Outbox 데이터가 무한히 쌓이면 DB 스토리지 부하가 발생한다. 일정 기간(예: 7일)이 지난 완료 데이터를 삭제하는 주기적인 배치/스케줄러가 존재하는가?
2. **이벤트 순서 보장 (Ordering)**: 하나의 주문에 대해 "생성 -> 수정 -> 취소" 이벤트가 순차적으로 Outbox에 적혔을 때, 브로커로 전송되는 순서가 보장되는가? (CDC 방식은 Binlog 순서를 지키므로 이점이 크다)
3. **폴링 테이블 인덱싱**: Polling 방식을 사용할 경우 `status='READY'` 조건으로 잦은 조회가 발생하므로, 해당 컬럼에 적절한 인덱스 처리가 되어 DB 풀스캔(Full Scan)을 방지하고 있는가?

### 3. 치명적 안티패턴 (Anti-Pattern)
- **외부 API 직접 호출 포함 (Distributed Transaction Leak)**: Outbox에 넣는 트랜잭션 안에서 엉뚱하게 외부 서비스의 REST API를 호출하는 경우.

> 아래는 Outbox의 원자성을 파괴하는 안티패턴을 시각화한 구조도이다.

```text
[Anti-Pattern: The Leaky Transaction]

[App]
 | 1. Tx Begin
 | 2. Insert Order
 | 3. Insert Outbox
 | 4. HTTP POST /external/api  <== (치명적 오류: 네트워크 지연 발생!)
 | 5. Tx Commit
```
- **해설**: RDBMS 트랜잭션은 가능한 짧게 유지되어야 한다. 트랜잭션 블록 안에서 외부 API를 호출하면, 외부 서버가 느려질 때 내 DB의 커넥션 풀(Connection Pool)이 모두 고갈되어 전체 서비스가 마비(Cascading Failure)된다. DB 작업 외의 I/O는 트랜잭션 밖으로 빼야 한다.

> **📢 섹션 요약 비유**: 우체통에 편지를 넣고 자물쇠를 잠그기 전에, 굳이 옆 동네 친구에게 전화해서 확인하려다 우체통 문을 연 채로 한 시간 동안 멈춰서 있는 꼴입니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량/정성적 기대효과

| 기대효과 구분 | 도입 전 (이중 쓰기) | 도입 후 (Transactional Outbox) | ROI 및 변화 지표 |
|:---|:---|:---|:---|
| **데이터 무결성** | 연 0.5% 수준의 메시지 유실 발생 | 로컬 트랜잭션 보장으로 유실률 0% 달성 | CS 접수 및 데이터 보정 공수 95% 절감 |
| **장애 격리 (Isolation)** | Kafka 점검 시 전체 주문/결제 마비 | Kafka가 죽어도 DB에는 정상 적재됨 | 시스템 코어 서비스의 가용성(RTO) 대폭 향상 |
| **응답 지연 (Latency)** | 메시지 전송 시간만큼 사용자 응답 지연 | DB 로컬 커밋만으로 사용자 즉시 응답 | 클라이언트 체감 API 레이턴시 40% 단축 |

### 2. 미래 전망 및 아키텍처 진화
- **CDC 인프라의 표준화**: 초기에는 Polling 방식이 많이 쓰였으나, 실시간성과 DB 부하 최소화 요구로 인해 **Kafka Connect와 Debezium을 결합한 CDC 방식**이 엔터프라이즈 MSA 메시징 릴레이의 표준(De-facto Standard)으로 완전히 자리 잡았다.
- **클라우드 네이티브 지원**: AWS DynamoDB Streams, Azure DynamoDB TTL 등 클라우드 관리형 데이터베이스들이 데이터 변경 이벤트를 자체적으로 브로커(Kinesis, EventBridge)로 쏘아주는 기능을 기본 제공하면서, 별도의 아웃박스 테이블 관리 없이도 동일한 효과를 내는 아키텍처로 진화하고 있다.

> **📢 섹션 요약 비유**: 트랜잭셔널 아웃박스 패턴은 불안정한 네트워크 바다를 건너기 전, 메시지들에게 구명조끼(로컬 DB)를 입히는 필수 안전 규정입니다. 속도와 독립성을 추구하는 MSA에서 데이터의 생명을 지키는 최후의 보루 역할을 합니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- 코레오그래피 사가 (Choreography Saga) | 이벤트를 발행할 때 메시지 유실을 방지하기 위해 아웃박스 패턴을 필수적으로 동반해야 하는 비동기 트랜잭션 패턴
- CDC (Change Data Capture) | 데이터베이스의 트랜잭션 로그를 추적하여 아웃박스 테이블의 변경분을 브로커로 효율적으로 전달하는 핵심 기술 (예: Debezium)
- 멱등성 (Idempotency) | 아웃박스 패턴이 발생시키는 '최소 한 번(At-Least-Once)' 전송 구조에서 중복 처리를 막아주는 수신자 측 필수 속성
- 이중 쓰기 (Dual Write Problem) | 데이터베이스 커밋과 메시지 큐 전송을 동시에 시도할 때 발생하는 분산 환경의 원자성 파괴 문제
- 이벤트 소싱 (Event Sourcing) | 상태 자체를 저장하지 않고 이벤트 로그만 저장하여, 별도의 Outbox 테이블 없이 자연스럽게 이벤트를 스트리밍하는 상위 호환 아키텍처

### 👶 어린이를 위한 3줄 비유 설명
1. **개념**: 일기를 쓰고(상태 변경) 친구에게 그 내용을 편지(이벤트)로 보내야 하는데, 편지를 부치러 가다가 잃어버리면 안 되잖아요.
2. **원리**: 그래서 아예 내 방에 '보낼 편지함(Outbox)'을 만들어 두고, 일기를 쓸 때마다 그 함에 편지도 같이 넣어둬요. 방 안에서 하는 일이라 절대 잃어버릴 일이 없죠.
3. **효과**: 나중에 우체부 아저씨(CDC)가 우리 집에 와서 그 함에 있는 편지를 다 가져가서 배달해 주기 때문에, 나는 안심하고 내 할 일만 빠르게 할 수 있어요!
