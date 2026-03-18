+++
title = "CQRS (Command Query Responsibility Segregation) 패턴"
description = "시스템의 상태를 변경하는 명령(Command) 모델과 상태를 반환하는 조회(Query) 모델을 물리/논리적으로 분리하여 확장성과 성능을 극대화하는 아키텍처 패턴"
weight = 197
+++

# CQRS (Command Query Responsibility Segregation) 패턴

> **약어 (Abbreviation)**: CQRS (Command Query Responsibility Segregation)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CQRS (Command Query Responsibility Segregation) 패턴은 하나의 시스템에서 데이터의 **상태를 변경하는 쓰기 작업(Command)**과 **데이터를 읽는 조회 작업(Query)**의 책임과 모델을 완벽하게 분리하는 소프트웨어 아키텍처 패턴이다.
> 2. **가치**: 쓰기보다 읽기 요청이 압도적으로 많은 환경에서 조회 전용 데이터베이스를 별도로 구축(Materialized View)하여 **조회 성능(Read Performance)을 극대화**하고, 복잡한 조인(Join) 없이 빠른 응답을 제공한다.
> 3. **융합**: 비동기 데이터 동기화를 위해 **메시지 브로커 (Kafka)** 및 **이벤트 소싱 (Event Sourcing)** 패턴과 융합되어 최신 마이크로서비스(MSA)의 대규모 트래픽 처리 표준으로 활용된다.

---

## Ⅰ. 개요 (Context & Background)

- **개념**: CQRS (Command Query Responsibility Segregation)는 CQS (Command Query Separation) 원칙을 아키텍처 레벨로 확장한 것으로, "명령(C)은 상태를 바꾸되 반환값이 없고, 조회(Q)는 반환값이 있되 상태를 바꾸지 않는다"는 원칙에 따라 데이터베이스와 모델을 아예 두 갈래로 나누는 방식이다.
- **💡 비유**: 식당에서 '주문을 받는 직원(Command)'과 '음식을 내어주는 직원(Query)'을 나누고, 심지어 '주문서(Write DB)'와 '완성된 음식 진열대(Read DB)'를 따로 두어 손님들이 줄 서지 않게 하는 것과 같습니다.
- **등장 배경**:
  - **기존 한계**: 전통적인 CRUD 기반 단일 DB 아키텍처는 쓰기와 읽기를 같은 테이블에서 수행했다. 트래픽이 몰리면 쓰기 락(Lock)이 읽기를 방해하고, 복잡한 화면 구성을 위한 무거운 조인(Join) 쿼리가 전체 시스템 성능을 저하시켰다.
  - **혁신적 패러다임**: "대부분의 비즈니스는 읽기(Read)와 쓰기(Write)의 비율이 100:1에서 1000:1에 달한다."는 사실에 착안하여, 쓰기와 읽기의 성능 확장(Scale-out)을 완전히 독립적으로 수행할 수 있는 비대칭 모델이 고안되었다.
  - **현재의 비즈니스 요구**: MSA 환경에서는 여러 서비스의 데이터를 모아서(Aggregation) 보여줘야 하는 화면이 많다. API Composition의 지연을 피하기 위해 조회 전용 데이터베이스를 미리 만들어 두는 CQRS가 필수가 되었다.

> 다음은 전통적인 단일 CRUD 모델의 병목 현상과 CQRS 모델의 구조적 차이를 보여주는 비교 도식이다.

```text
┌─────────────────────────────────────────────────────────────┐
│ [Traditional CRUD vs CQRS Architecture]                     │
├──────────────────────────────┬──────────────────────────────┤
│ 1. Traditional CRUD          │ 2. CQRS Pattern              │
│                              │                              │
│   [Client]                   │        [Client]              │
│    |    ^                    │         |    ^               │
│  Write Read                  │     Command  Query           │
│    v    |                    │         v    |               │
│  [  App  ] (병목/락 경합)    │     [App C] [App Q]          │
│      |                       │        |      |              │
│      v                       │      (DB W) (DB R)           │
│ [Single DB]                  │        |      ^              │
│ (Order, User, Product Join)  │        +--Sync+              │
└──────────────────────────────┴──────────────────────────────┘
```
- **해설**: 기존 모델은 하나의 DB가 무거운 쓰기와 복잡한 읽기를 동시에 견뎌야 했다. 반면 CQRS는 쓰기(App C / DB W)와 읽기(App Q / DB R)가 철저히 분리된다. DB W에 데이터가 쓰이면, 백그라운드 동기화(Sync)를 통해 DB R이 화면(View)에 최적화된 형태로 미리 조인된 데이터를 저장해둔다.

> **📢 섹션 요약 비유**: 도서관에서 책을 새로 입고하고 분류하는 복잡한 창고(Write DB)와, 학생들이 가장 많이 찾는 베스트셀러만 모아둔 별도의 열람실(Read DB)을 나누어 운영하는 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소

| 요소명 | 역할 | 내부 동작 | 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Command Model** | 상태 변경(CUD) 담당 | 도메인 로직을 검증하고 Write DB의 상태를 변경함 | JPA, RDBMS | 창고 관리자 |
| **Write DB** | 정규화된 데이터 저장 | 3정규화(3NF)된 형태로 일관성(ACID)을 엄격히 지키며 데이터 적재 | PostgreSQL, MySQL | 물류 창고 |
| **Event Synchronizer** | 모델 간 데이터 동기화 | Write DB의 변경 사실을 Read DB로 전달 (Message Broker 활용) | Kafka, Debezium (CDC) | 지게차 운반수 |
| **Query Model** | 데이터 조회(R) 담당 | 비즈니스 로직 없이 Read DB에서 데이터를 즉시 퍼서 반환 | DTO, MyBatis | 진열대 직원 |
| **Read DB (View DB)** | 비정규화(Denormalization) 데이터 저장 | 조인이 필요 없도록 화면 출력 형태(JSON) 그대로 저장 | Elasticsearch, MongoDB | 쇼룸 진열대 |

### 2. 정상 동작 흐름 (Happy Path)

> 아래 다이어그램은 사용자가 주문을 생성(Command)한 뒤, 이벤트 브로커를 거쳐 조회 전용 DB에 어떻게 반영(Query)되는지 보여주는 흐름도이다.

```text
[CQRS Full Synchronization Flow]

(Client)
  │
  ├── 1. POST /orders (Command)
  v
[Command Service]
  │
  ├── 2. Validate Business Logic
  ├── 3. Save to [Write DB (PostgreSQL)]  (정규화 테이블)
  │
  └── 4. Publish Event "OrderCreated"
           │
           v
    [[ Message Broker (Kafka) ]]
           │
           ├── 5. Subscribe "OrderCreated"
           v
[Query Service / Projector]
  │
  ├── 6. Fetch necessary data (User info, Product info)
  └── 7. Save to [Read DB (MongoDB)]      (비정규화된 단일 문서)
           │
           v
(Client) <── 8. GET /orders/summary (Query) -> 즉시 0.01초 내 반환
```
- **해설**: 쓰기 모델은 트랜잭션의 정합성을 위해 RDBMS를 쓴다. 쓰기가 완료되면 '주문 생성됨' 이벤트가 Kafka로 날아간다. Query Service(Projector)는 이 이벤트를 잡아서 사용자 정보와 상품 정보를 미리 다 조인(Join)하여, NoSQL(MongoDB 등)에 하나의 뚱뚱한 문서(Document) 형태로 저장한다. 이후 클라이언트가 조회를 요청하면, Query Service는 조인 없이 Document를 통째로 던져주므로 극단적인 성능 최적화가 달성된다.

### 3. Materialized View (구체화된 뷰) 메커니즘
CQRS에서 Read DB의 본질은 **Materialized View(구체화된 뷰)**다. 이는 매번 쿼리할 때마다 Join 연산을 수행하는 Logical View와 달리, 쿼리 결과를 아예 디스크에 '물리적인 테이블이나 문서'로 구워놓는(Materialized) 기법이다. 이벤트가 발생할 때만 백그라운드에서 이 뷰를 갱신하므로, 사용자의 읽기 요청은 CPU 연산 없이 단순 디스크/메모리 I/O만으로 끝난다.

> **📢 섹션 요약 비유**: 매번 손님이 올 때마다 밀가루 반죽부터 시작해 피자를 굽는 것(단일 DB Join)이 아니라, 새벽에 미리 여러 종류의 조각 피자를 구워 진열장(Read DB)에 놔두고 손님이 고르면 즉시 내어주는 방식입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 단일 DB 구조 vs 물리적 CQRS 비교

| 비교 항목 | 전통적 CRUD (단일 모델) | CQRS (물리적 DB 분리) | 설계 시 판단 기준 |
|:---|:---|:---|:---|
| **응답 속도 (Latency)** | 쓰기/읽기 경합, 복잡한 조인으로 느림 | 읽기는 단순 매핑, 쓰기는 독립적으로 매우 빠름 | 읽기 성능 최적화 필요성 |
| **일관성 수준 (Consistency)** | 강한 일관성 (Strong Consistency) 보장 | **결과적 일관성 (Eventual Consistency)** 수용 | 화면 반영 지연(수 초)의 비즈니스 허용 여부 |
| **확장성 (Scalability)** | DB 스케일업(Scale-up) 위주 한계 | 쓰기와 읽기 서버/DB를 독립적으로 스케일아웃 | 트래픽의 Read/Write 비율 편차 |
| **시스템 복잡도 (Complexity)**| 매우 낮음 (하나의 트랜잭션) | 매우 높음 (브로커, DB 2개, 동기화 로직 관리) | 개발 및 운영 인프라 역량 |

### 2. 논리적 CQRS와 물리적 CQRS의 단계 (Maturity)
CQRS는 한 번에 도입하기엔 러닝 커브가 크다. 따라서 실무에서는 단계적으로 접근한다.

```text
[CQRS Maturity Levels]

Level 1. Logical CQRS (동일 DB, 다른 코드)
  [App W] --(JPA)--> [Single DB]
  [App R] --(MyBatis)--> [Single DB]
  - 이점: 코드 레벨의 분리로 유지보수성 향상.
  - 한계: DB 자체가 병목일 경우 해결 불가.

Level 2. Physical CQRS with Replica (마스터-슬레이브 분리)
  [App W] ----> [DB Master]
                  | (Replication)
  [App R] ----> [DB Read Replica]
  - 이점: DB 부하 분산.
  - 한계: 여전히 스키마가 같아 복잡한 조인은 피할 수 없음.

Level 3. Physical CQRS with Heterogeneous DB (이기종 DB 분리)
  [App W] ----> [RDBMS (PostgreSQL)]
                  | (Kafka / CDC)
  [App R] ----> [NoSQL (Elasticsearch / MongoDB)]
  - 이점: 읽기 성능 극한의 최적화 (검색, 집계 특화).
  - 한계: 동기화(Sync) 로직이 깨질 경우 치명적 불일치 발생.
```

> **📢 섹션 요약 비유**: 처음에는 한 냉장고에서 칸만 나누어 쓰고(논리적 분리), 다음엔 김치냉장고를 추가로 사서 나누며(Replication), 최종적으로는 냉동창고와 전시용 쇼케이스를 완전히 분리(이기종 DB)하는 확장 과정과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오와 의사결정
- **상황**: 대형 이커머스의 메인 상품 전시 페이지. 하루 수천만 건의 조회가 발생하지만, 상품의 가격이나 재고 변경(쓰기)은 하루에 몇 번 발생하지 않음. 사용자는 다양한 필터(카테고리, 리뷰 수, 평점)로 상품을 검색함.
- **판단**: 읽기와 쓰기의 비율이 10,000:1 이상이다. RDBMS(Write DB)에서 상품, 옵션, 리뷰 테이블을 매번 조인하는 것은 불가능하다. **Level 3 물리적 CQRS**를 도입하여, 상품 정보가 변경될 때마다 Kafka 이벤트를 쏘고 **Elasticsearch(Read DB)**에 역정규화된 검색용 문서를 저장한다. 메인 페이지는 Elasticsearch만 바라보게 하여 검색 속도를 밀리초 단위로 단축한다.

### 2. 도입 시 핵심 체크리스트 (Technical & Operational)
1. **결과적 일관성(Eventual Consistency) 허용 여부**: Write DB에 쓰기가 완료되고 Read DB에 동기화되기까지 0.1초~2초의 지연(Replication Lag)이 발생한다. 사용자가 "결제했는데 왜 바로 내역 화면에 안 나오지?"라고 클레임을 걸 수 있는가? 이를 화면 단에서 어떻게 무마할 것인가? (예: "반영 중입니다" 메시지 또는 Optimistic UI 업데이트).
2. **이벤트 순서(Ordering) 보장**: 주문 상태가 '결제됨' -> '취소됨' 순서로 브로커를 탔는데, Read DB 쪽 Projector가 네트워크 이슈로 순서를 뒤바꿔 수신하면 DB 상태가 꼬인다. Kafka의 파티션 키(Partition Key)를 주문 ID로 설정하여 순서를 강제했는가?
3. **이벤트 재생(Replay) 능력**: Read DB(예: Elasticsearch)의 인덱스가 깨지거나 새로운 검색 화면 요구사항이 생겨 스키마를 엎어야 할 때, 과거의 이벤트를 처음부터 다시 재생(Replay)하여 Read DB를 통째로 다시 빌드할 수 있는 인프라가 있는가? (이벤트 소싱과의 결합 필요).

### 3. 치명적 안티패턴 (Anti-Pattern)
- **단순 CRUD 게시판에 CQRS 도입 (Over-engineering)**: 읽기와 쓰기 비율이 1:1에 가깝고, 복잡한 조인이 없는 단순 백오피스 어드민 화면에 굳이 CQRS를 도입하는 것.

> 아래는 단순 시스템에 CQRS를 도입했을 때 발생하는 비용 곡선을 나타낸 그래프이다.

```text
개발 및 운영 비용 (Cost)
   ^
   |                     / CQRS (단순한 시스템에서는 과도한 비용)
   |                    /
   |                   /
   |                  /
   |   CRUD          /
   |   ----         /
   |       \       /
   |        \-----/ (일정 복잡도를 넘어가면 CQRS가 이득)
   |
   +-------------------------------------> 도메인/쿼리 복잡도 (Complexity)
```
- **해설**: CQRS는 "공짜 점심이 아니다". 데이터 동기화 지연 해결, 브로커 인프라 운영, 데이터 보정(Reconciliation) 배치 등 엄청난 개발/운영 비용을 동반한다. 시스템의 쿼리가 RDBMS의 인덱싱만으로 충분히 커버된다면 절대 도입해서는 안 되는 패턴이다.

> **📢 섹션 요약 비유**: 동네 구멍가게에서 물건을 팔기 위해 대형 마트의 바코드 스캐너와 물류 자동화 시스템을 수천만 원 들여 설치하는 격(오버엔지니어링)입니다. 내 비즈니스의 트래픽과 조인 복잡도를 먼저 진단해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량/정성적 기대효과

| 기대효과 구분 | 도입 전 (RDBMS Join) | 도입 후 (CQRS + NoSQL) | ROI 및 변화 지표 |
|:---|:---|:---|:---|
| **조회 성능 (Read Latency)**| 조인 및 인덱스 스캔으로 수 초 지연 | 단일 문서(Document) 단순 Get | 메인 페이지 응답 속도 90% 이상 단축 |
| **시스템 격리 (Fault Tolerance)**| 뷰어(View) 트래픽이 쓰기(결제) DB 마비 | 메인 페이지 폭주해도 결제 DB 안전 | 장애 전파(Cascading Failure) 완전 차단 |
| **다형성 (Polyglot Persistence)**| 모든 데이터를 관계형으로 억지 매핑 | 검색은 ES, 캐시는 Redis 등 최적 도구 사용| 비즈니스 요구사항(전문 검색 등) 수용력 극대화 |

### 2. 미래 전망 및 아키텍처 진화
- **이벤트 소싱 (Event Sourcing)과의 결합 표준화**: CQRS는 상태 동기화의 불안정성을 극복하기 위해, 상태 대신 "이벤트 발생 내역 자체"를 원본으로 저장하는 이벤트 소싱과 영혼의 단짝으로 결합되어 진화하고 있다 (ES/CQRS 아키텍처).
- **클라우드 벤더의 관리형 서비스 지원**: 개발자가 직접 CDC 파이프라인을 구축하던 과거와 달리, 최근에는 AWS DynamoDB Streams -> Lambda -> OpenSearch 로 이어지는 관리형 파이프라인이 CQRS 구현의 사실상 표준(De-facto)으로 자리 잡고 있다.

> **📢 섹션 요약 비유**: CQRS는 짐을 싣는 마차(Write)와 승객을 태우는 스포츠카(Read)의 엔진을 분리하는 작업입니다. 초기 설계는 고통스럽지만, 완벽히 분리된 엔진은 트래픽이라는 무한한 고속도로에서 절대 서로의 발목을 잡지 않습니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- 이벤트 소싱 (Event Sourcing) | CQRS와 가장 자주 결합되는 패턴으로, 데이터의 현재 상태가 아닌 상태 변경 이벤트의 연속(Log)을 저장하는 기법
- Materialized View (구체화된 뷰) | CQRS의 Read DB가 취하는 형태로, 복잡한 조인 결과를 미리 디스크에 계산해 두어 조회 속도를 극대화한 테이블
- 트랜잭셔널 아웃박스 (Transactional Outbox) | Write DB의 커밋과 메시지 브로커 이벤트 발행 간의 원자성을 보장하기 위해 CQRS 동기화 파이프라인 앞단에 배치되는 패턴
- 결과적 일관성 (Eventual Consistency) | 데이터가 즉각 동기화되지 않지만, 시간이 지나면 결국 Read DB가 Write DB의 상태를 반영하게 된다는 비동기 분산 시스템의 특징
- CDC (Change Data Capture) | Write DB(예: MySQL)의 binlog를 감지하여 Read DB(예: Elasticsearch)로 이벤트를 쏴주는 데이터 파이프라인 기술 (Debezium 등)

### 👶 어린이를 위한 3줄 비유 설명
1. **개념**: 장난감 가게에서 창고에 장난감을 채워 넣는 아저씨(쓰기)와, 손님에게 예쁘게 진열된 장난감을 보여주는 아저씨(읽기)의 일을 완전히 나눈 거예요.
2. **원리**: 창고 아저씨가 새 장난감을 받으면, 비서(메시지 브로커)에게 "새로 들어왔어!"라고 알려줘요. 그럼 진열장 아저씨는 비서의 말을 듣고 즉시 손님이 보기 편하게 세트로 묶어서 예쁜 진열장(Read DB)에 올려둬요.
3. **효과**: 손님이 천 명이 몰려와도 진열장만 보고 장난감을 사 가면 되니까, 창고에서 무거운 짐을 정리하는 일과 부딪히지 않고 엄청나게 빠르게 구경할 수 있어요!
