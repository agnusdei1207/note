+++
title = "NoSQL 데이터베이스 개요"
categories = ["studynotes-16_bigdata"]
+++

# NoSQL 데이터베이스 개요

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NoSQL(Not Only SQL)은 관계형 데이터베이스의 ACID 트랜잭션과 고정 스키마라는 제약을 벗어나, **수평 확장성(Scale-out)**, **유연한 스키마(Schema-less)**, **다양한 데이터 모델**을 지원하는 비관계형 데이터베이스의 총칭입니다.
> 2. **가치**: 페타바이트급 데이터와 초당 수백만 트랜잭션을 처리해야 하는 웹 스케일 애플리케이션에서, RDBMS 대비 **10~100배 높은 처리량**과 **선형 확장성**을 제공합니다.
> 3. **융합**: CAP 정리, BASE 속성, 결과적 일관성(Eventual Consistency) 이론에 기반하며, 빅데이터, 실시간 분석, IoT, 소셜 미디어 플랫폼의 핵심 데이터 저장소로 활용됩니다.

---

## Ⅰ. 개요 (Context & Background)

NoSQL 데이터베이스는 2000년대 후반 Google Bigtable, Amazon Dynamo 논문에서 시작되어, Facebook(Cassandra), LinkedIn(Voldemort), Netflix 등의 초대형 인터넷 기업들이 직면한 **웹 스케일 데이터 처리 문제**를 해결하기 위해 발전했습니다. NoSQL은 단일 기술이 아니라 **Key-Value, Document, Column-Family, Graph** 등 다양한 데이터 모델을 포괄하는 포괄적 용어입니다.

**💡 비유: 도서관 vs 창고**
RDBMS는 **엄격한 분류 체계를 가진 도서관**입니다. 모든 책은 미리 정해진 카테고리와 규칙에 따라 배치되며, 새로운 형태의 책을 넣으려면 분류 체계를 변경해야 합니다. 반면 NoSQL은 **유연한 창고**입니다. 물건이 들어오는 대로 공간에 맞춰 보관하고, 필요하면 창고를 옆에 추가로 지어(수평 확장) 수용력을 늘릴 수 있습니다.

**등장 배경 및 발전 과정:**
1. **기존 기술의 치명적 한계점**: Web 2.0 시대의 SNS, IoT, 모바일 앱은 폭발적인 데이터 증가와 높은 쓰기 처리량을 요구했습니다. 기존 RDBMS는 **수직 확장(Scale-up)의 한계**, **스키마 경직성**, **JOIN 비용**으로 인해 병목이 발생했습니다.
2. **혁신적 패러다임 변화**: Google Bigtable(2006)과 Amazon Dynamo(2007) 논문은 **분산 해시 테이블**, **일관성 해시(Consistent Hashing)**, **벡터 시계(Vector Clock)** 등 새로운 분산 시스템 기법을 제시했습니다.
3. **비즈니스적 요구사항**: 99.99% 가용성, 글로벌 분산, 낮은 지연 시간, 스키마 유연성 등 **웹 스케일 요구사항**을 충족하기 위해 NoSQL이 도입되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### NoSQL 4대 데이터 모델

| 모델 | 상세 역할 | 내부 동작 메커니즘 | 대표 기술 | 비유 |
|---|---|---|---|---|
| **Key-Value** | 단순 키-값 저장 및 조회 | 해시 테이블 기반 O(1) 조회, 메모리/디스크 계층화 | Redis, DynamoDB, Riak | 사물함 |
| **Document** | 계층적 문서(JSON/BSON) 저장 | 내장 인덱스, 샤딩, BSON 직렬화 | MongoDB, CouchDB, Firestore | 파일 캐비닛 |
| **Column-Family** | 열 지향 대용량 저장 | 로우 키 + 컬럼 패밀리, LSM Tree | Cassandra, HBase, ScyllaDB | 스프레드시트 |
| **Graph** | 노드-엣지 관계 저장 | 인접 리스트, 순회 최적화 인덱스 | Neo4j, Neptune, TigerGraph | 지도 |

### 정교한 구조 다이어그램 (ASCII Art)

```text
========================================================================================================
                              [ NOSQL DATA MODELS COMPARISON ]
========================================================================================================

  [ KEY-VALUE STORE ]                    [ DOCUMENT STORE ]

  +-------------------------+            +-------------------------+
  | Key         | Value     |            | _id: "user123"          |
  |-------------|-----------|            | name: "John"            |
  | "user:123"  | "John"    |            | age: 30                 |
  | "user:456"  | "Jane"    |            | address: {              |
  | "session:1" | "{...}"   |            |   city: "Seoul",        |
  +-------------------------+            |   zip: "12345"          |
                                         | }                       |
  O(1) Lookup, Simple Structure          +-------------------------+
                                         Nested Structure, Flexible Schema

  [ COLUMN-FAMILY STORE ]               [ GRAPH DATABASE ]

  +---------------------------------------------------+       +-------------------+
  | Row Key    | CF: Profile   | CF: Activity        |       |  (User1)          |
  |------------|---------------|---------------------|       |     |             |
  | "user:123" | name: "John"  | last_login: "..."   |       |  FOLLOWS    POSTED|
  |            | age: 30       | posts: 100          |       |     |             |
  |------------|---------------|---------------------|       |     v             v
  | "user:456" | name: "Jane"  | last_login: "..."   |       |  (User2)     (Post1)|
  +---------------------------------------------------+       |     |             ^
                                                             |  LIKES          |
                                                             |     |             |
                                                             |     v             |
                                                             |  (User3)----------+

========================================================================================================
                              [ CAP THEOREM & NOSQL POSITIONING ]
========================================================================================================

                              Consistency (C)
                                  ▲
                                 /│\
                                / │ \
                               /  │  \
                              /   │   \
                             /    │    \
                   [ CA ]   /     │     \   [ CP ]
                   RDBMS   /      │      \   MongoDB
                   (Single ├──────┼──────┤   HBase
                    Node)  \      │      /   Redis
                            \     │     /
                             \    │    /
                              \   │   /
                               \  │  /
                                \ │ /
                                 \│/
                                  ▼
                          Availability (A) ←─── [ AP ]
                                                Cassandra
                                                DynamoDB
                                                CouchDB

                             Partition Tolerance (P) is mandatory in distributed systems

========================================================================================================
                              [ CASSANDRA RING ARCHITECTURE ]
========================================================================================================

                     Node 1 (Token: 0)
                   ┌──────────────────┐
                   │  Range: [0, 50]  │
                   └────────┬─────────┘
                            │
           Node 6           │           Node 2
        ┌──────────┐        │        ┌──────────┐
        │ [250,300]│────────┼────────│ [50,100] │
        └──────────┘        │        └──────────┘
              │             │             │
              │    Consistent Hashing     │
              │             │             │
        ┌──────────┐        │        ┌──────────┐
        │ [200,250]│────────┼────────│ [100,150]│
        └──────────┘        │        └──────────┘
           Node 5           │           Node 3
                            │
                   ┌────────┴─────────┐
                   │  Range: [150,200]│
                   └──────────────────┘
                     Node 4 (Token: 150)

         Replication Factor = 3: Each data stored in 3 consecutive nodes

========================================================================================================
```

### 심층 동작 원리: 일관성 수준과 트레이드오프

**1. CAP 정리와 실제 적용**
```text
CAP 정리 (Eric Brewer, 2000):
분산 시스템에서는 Consistency, Availability, Partition Tolerance 중
최대 2개만 동시에 보장할 수 있다.

┌─────────────────────────────────────────────────────────────────────┐
│ CP (Consistency + Partition Tolerance)                              │
│ - 전략: 파티션 발생 시 일관성 유지를 위해 일부 노드 응답 거부        │
│ - 예시: MongoDB (Primary-Secondary), HBase, Redis Cluster           │
│ - 장애 상황: 쓰기 불가 (Primary 선출 중)                             │
├─────────────────────────────────────────────────────────────────────┤
│ AP (Availability + Partition Tolerance)                             │
│ - 전략: 파티션 발생 시 항상 응답하되, 일시적 불일치 허용             │
│ - 예시: Cassandra, DynamoDB, CouchDB                                │
│ - 장애 상황: 최종 일관성(Eventual Consistency)으로 수렴             │
├─────────────────────────────────────────────────────────────────────┤
│ CA (Consistency + Availability) - 단일 노드만 가능                  │
│ - 전략: 파티션이 없는 단일 노드 RDBMS                                │
│ - 예시: 전통적 RDBMS (MySQL, PostgreSQL 단일 인스턴스)              │
│ - 한계: 수평 확장 불가, 단일 장애점                                  │
└─────────────────────────────────────────────────────────────────────┘
```

**2. Cassandra 일관성 수준 (Tunable Consistency)**
```python
# Cassandra Python Driver: 일관성 수준 설정
from cassandra.cluster import Cluster
from cassandra.consistency import ConsistencyLevel

cluster = Cluster(['cassandra1', 'cassandra2', 'cassandra3'])
session = cluster.connect('my_keyspace')

# 일관성 수준 튜닝
# ONE: 하나의 복제본만 응답하면 완료 (빠름, 약한 일관성)
session.execute(
    "SELECT * FROM users WHERE user_id = %s",
    (user_id,),
    consistency_level=ConsistencyLevel.ONE
)

# QUORUM: 과반수 복제본 응답 필요 (균형)
session.execute(
    "UPDATE users SET last_login = %s WHERE user_id = %s",
    (timestamp, user_id),
    consistency_level=ConsistencyLevel.QUORUM
)

# ALL: 모든 복제본 응답 필요 (강한 일관성, 느림)
session.execute(
    "DELETE FROM users WHERE user_id = %s",
    (user_id,),
    consistency_level=ConsistencyLevel.ALL
)

# LOCAL_QUORUM: 로컬 데이터센터 내 과반수 (글로벌 배포 시)
session.execute(
    "INSERT INTO users (user_id, name) VALUES (%s, %s)",
    (user_id, name),
    consistency_level=ConsistencyLevel.LOCAL_QUORUM
)
```

**3. BASE 속성 vs ACID 속성**
```text
┌─────────────────────────────────────────────────────────────────────┐
│ ACID (RDBMS)                        BASE (NoSQL)                    │
├─────────────────────────────────────────────────────────────────────┤
│ Atomicity (원자성)                  Basically Available             │
│   - All or Nothing                    - 항상 응답 보장               │
│                                     - 일시적 불일치 허용            │
├─────────────────────────────────────────────────────────────────────┤
│ Consistency (일관성)                Soft State                      │
│   - 항상 일관된 상태                  - 상태가 시간에 따라 변화      │
│                                     - 외부 개입 없이도 변화 가능    │
├─────────────────────────────────────────────────────────────────────┤
│ Isolation (격리성)                  Eventually Consistent           │
│   - 트랜잭션 간 간섭 없음            - 시간이 지나면 일관성 달성    │
│                                     - 최종적으로 모든 노드 동기화   │
├─────────────────────────────────────────────────────────────────────┤
│ Durability (지속성)                 ─                               │
│   - 영구 저장                                                         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: NoSQL 모델별 특성

| 비교 지표 | Key-Value | Document | Column-Family | Graph |
|---|---|---|---|---|
| **데이터 구조** | 단순 (Key, Value) | 반정형 (JSON/BSON) | 희소 행렬 | 노드+엣지 |
| **스키마** | 없음 | 유연 (Schema-less) | 컬럼 패밀리 | 그래프 스키마 |
| **조회 방식** | 키 기반 O(1) | 키 + 인덱스 | 키 + 컬럼 | 순회(Traversal) |
| **복잡한 쿼리** | 불가능 | 가능 (Aggregation) | CQL 제한 | Cypher/Gremlin |
| **확장성** | 매우 높음 | 높음 | 매우 높음 | 제한적 |
| **Use Case** | 캐시, 세션 | 콘텐츠 관리 | 시계열, IoT | 소셜, 추천 |
| **대표 DB** | Redis, DynamoDB | MongoDB | Cassandra, HBase | Neo4j |

### 과목 융합 관점 분석

- **[데이터베이스 + NoSQL]**: NoSQL은 RDBMS의 **JOIN, 정규화, ACID**를 포기하는 대신 **수평 확장성**과 **유연성**을 얻었습니다. 이는 **데이터 중복 허용**, **조인 없는 설계(Embedding)**, **결과적 일관성**을 받아들이는 패러다임 전환을 요구합니다.

- **[네트워크 + NoSQL]**: 분산 NoSQL은 **Consistent Hashing**, **Gossip Protocol**, **Anti-Entropy** 등 P2P 네트워크 기법을 사용합니다. Cassandra의 **Gossip Protocol**은 모든 노드가 다른 노드의 상태를 주기적으로 교환하여 장애를 감지합니다.

- **[운영체제 + NoSQL]**: NoSQL의 성능은 **메모리 관리**, **파일 시스템**, **네트워크 스택**에 크게 의존합니다. Redis는 **fork()+copy-on-write**를 사용하여 RDB 스냅샷을 생성하고, Cassandra는 **mmap**을 활용한 인덱스 관리를 수행합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 글로벌 쇼핑몰 장바구니 시스템**
- **문제**: 전 세계 사용자의 장바구니 데이터를 실시간으로 저장하고 조회, 99.99% 가용성 필요
- **전략적 의사결정**:
  1. **Document DB 선택**: MongoDB로 장바구니를 문서(JSON)로 저장 (Embedding)
  2. **글로벌 분산**: 3개 리전(US, EU, APAC)에 샤드 배치, 로컬 읽기 지연 최소화
  3. **Read Preference**: 가장 가까운 리전에서 읽기, 쓰기는 Primary로 라우팅
  4. ** TTL 인덱스**: 30일 미접속 장바구니 자동 삭제

**시나리오 2: IoT 센서 데이터 수집 및 분석**
- **문제**: 100만 대 디바이스에서 초당 100만 개의 센서 데이터를 수집하고 시계열 분석
- **전략적 의사결정**:
  1. **Column-Family DB 선택**: Cassandra로 시계열 데이터 최적화 저장
  2. **파티션 키 설계**: `(device_id, date)`로 파티셔닝하여 핫 파티션 방지
  3. **TTL 설정**: 90일 후 자동 만료로 스토리지 비용 절감
  4. **TimeWindow Compaction**: 시계열 쿼리 성능 최적화

**시나리오 3: 실시간 캐싱 계층 구축**
- **문제**: RDBMS 조회 부하를 줄이기 위한 캐싱 계층, ms 단위 응답 필요
- **전략적 의사결정**:
  1. **In-Memory Key-Value DB 선택**: Redis Cluster
  2. **캐시 전략**: Read-Through + Write-Behind
  3. **데이터 구조**: Hash, Sorted Set 활용
  4. **Cluster Mode**: 6개 노드(3 Master + 3 Replica)로 샤딩 및 HA

### 주의사항 및 안티패턴 (Anti-patterns)

- **안티패턴 - RDBMS 마인드로 NoSQL 설계**: JOIN, 정규화를 고집하면 NoSQL의 장점을 살릴 수 없습니다. **데이터 중복을 허용**하고 **Embedding** 패턴을 활용해야 합니다.

- **안티패턴 - 일관성 수준 과소평가**: AP 시스템에서 Strong Consistency를 요구하면 성능이 급격히 저하됩니다. 비즈니스 요구사항에 맞는 **Tunable Consistency**를 선택해야 합니다.

- **안티패턴 - 파티션 키 설계 실패**: 잘못된 파티션 키는 **Hot Partition**을 유발하여 전체 클러스터 성능 저하. 카디널리티와 액세스 패턴을 고려한 설계가 필수입니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | 내용 및 지표 |
|---|---|
| **정성적 효과** | - 스키마 변경 없이 데이터 모델 진화 가능<br>- 글로벌 분산으로 지역별 지연 시간 최소화<br>- RDBMS 병목 해결로 전체 시스템 안정성 향상 |
| **정량적 효과** | - 쓰기 처리량 **10~100배 향상** (RDBMS 대비)<br>- 수평 확장으로 **선형적 용량 증가**<br>- 스토리지 비용 **50~80% 절감** (Commodity HW) |

### 미래 전망 및 진화 방향

- **Multi-Model DB**: 단일 DB가 여러 모델(Key-Value, Document, Graph) 지원
- **NewSQL**: NoSQL의 확장성 + RDBMS의 ACID 결합 (CockroachDB, TiDB)
- **Cloud-Native NoSQL**: AWS DynamoDB, Azure Cosmos DB와 같은 완전 관리형 서비스

**※ 참고 표준/가이드**:
- **CAP Theorem (Brewer, 2000)**: 분산 시스템의 근본적 한계
- **Dynamo Paper (Amazon, 2007)**: AP 시스템 설계 원칙
- **Bigtable Paper (Google, 2006)**: CP 시스템 설계 원칙

---

## 📌 관련 개념 맵 (Knowledge Graph)

- `[CAP 정리](@/studynotes/16_bigdata/05_nosql/cap_theorem.md)`: NoSQL 설계의 이론적 기반
- `[Redis](@/studynotes/16_bigdata/05_nosql/redis.md)`: 인메모리 Key-Value 데이터베이스
- `[MongoDB](@/studynotes/16_bigdata/05_nosql/mongodb.md)**: Document 기반 NoSQL
- `[Cassandra](@/studynotes/16_bigdata/05_nosql/cassandra.md)`: Column-Family 기반 분산 DB
- `[Neo4j](@/studynotes/16_bigdata/05_nosql/neo4j.md)`: Graph 데이터베이스

---

## 👶 어린이를 위한 3줄 비유 설명

1. **NoSQL이 뭔가요?**: 일반 도서관(RDBMS)은 책을 정해진 칸에만 넣을 수 있지만, NoSQL은 **자유로운 창고** 같아요. 어떤 모양의 물건이든 넣을 수 있고, 창고가 부족하면 옆에 또 지을 수 있어요.
2. **왜 쓰나요?**: 인스타그램이나 페이스북처럼 **엄청나게 많은 사람**이 동시에 사진을 올리고 볼 때, 일반 도서관은 너무 느려서 NoSQL 창고를 써요.
3. **단점은 없나요?**: 창고라서 물건 찾기가 조금 어려울 수 있어요. 도서관처럼 "컴퓨터 책은 3층"처럼 정확하게 정해져 있지 않거든요!
