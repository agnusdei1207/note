+++
title = "CAP 정리 (Consistency, Availability, Partition Tolerance)"
categories = ["studynotes-16_bigdata"]
+++

# CAP 정리 (Consistency, Availability, Partition Tolerance)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CAP 정리는 2000년 Eric Brewer가 제안한 분산 시스템 이론으로, **일관성(Consistency)**, **가용성(Availability)**, **분할 내성(Partition Tolerance)** 중 **최대 2개만 동시에 보장**할 수 있음을 증명합니다.
> 2. **가치**: CAP 정리는 NoSQL 데이터베이스, 분산 시스템 설계 시 **트레이드오프를 명시적으로 인식**하게 하여, 비즈니스 요구사항에 맞는 시스템 아키텍처 선택의 기준을 제공합니다.
> 3. **융합**: 현대 분산 시스템은 CAP를 넘어 **PACELC 이론**, **Tunable Consistency**, **CQRS 패턴** 등으로 진화하며, 동적 일관성 조정과 지역 최적화를 추구합니다.

---

## Ⅰ. 개요 (Context & Background)

CAP 정리는 분산 컴퓨팅의 근본적 한계를 정의한 이론입니다. 네트워크 분할(Partition)은 분산 시스템에서 피할 수 없는 현실이므로, **P(Partition Tolerance)는 필수**이며, 결과적으로 **C(Consistency)와 A(Availability) 사이의 선택**이 핵심입니다.

**💡 비유: 끊어진 전화선과 의사결정**
두 개의 은행 지점이 전화선으로 연결되어 있습니다. 한 지점에 고객이 와서 100만 원을 인출했습니다. 그 순간 전화선이 끊어졌습니다(Partition). 지점장은 선택해야 합니다. (1) 다른 지점의 잔액을 확인할 수 없으니 거래를 거부한다(Consistency 우선). (2) 일단 거래를 승인하고 나중에 동기화한다(Availability 우선).

**등장 배경 및 발전 과정:**
1. **기존 기술의 치명적 한계점**: 1990년대까지 분산 시스템은 ACID 트랜잭션을 완벽히 보장하려 했습니다. 하지만 네트워크 지연, 장애는 불가피하며, 완벽한 일관성은 **시스템 전체의 정지**를 초래했습니다.
2. **혁신적 패러다임 변화**: Brewer는 "네트워크 분할은 피할 수 없다"는 전제하에, **일관성과 가용성의 트레이드오프**를 명시적으로 인정하는 것이 더 나은 설계라고 주장했습니다.
3. **비즈니스적 요구사항**: 웹 스케일 서비스는 99.99% 가용성을 요구하며, 일시적 데이터 불일치를 감수하는 **결과적 일관성(Eventual Consistency)** 모델이 수용되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### CAP 3요소 상세 분석

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|---|---|---|---|---|
| **Consistency** | 모든 노드가 동일한 데이터 반환 | 동기 복제, Quorum Read/Write, 2PC | RDBMS, MongoDB, HBase | 모든 지점이 동일한 잔액 |
| **Availability** | 모든 요청에 응답 보장 (성공/실패) | 비동기 복제, Failover, Read Repair | Cassandra, DynamoDB, Riak | 지점이 문을 닫지 않음 |
| **Partition Tolerance** | 네트워크 분할 시에도 동작 유지 | Consistent Hashing, Vector Clock, Gossip | 모든 분산 시스템 | 전화선이 끊겨도 업무 지속 |

### 정교한 구조 다이어그램 (ASCII Art)

```text
========================================================================================================
                              [ CAP THEOREM TRIANGLE ]
========================================================================================================

                              Consistency (C)
                                  ▲
                                 /│\
                                / │ \
                               /  │  \
                              /   │   \
                             /    │    \
                   [ CA ]   /     │     \   [ CP ]
                           /      │      \
                          /       │       \
                         /        │        \
                        /         │         \
                       /          │          \
                      ├───────────┼───────────┤
                       \          │          /
                        \         │         /
                         \        │        /
                          \       │       /
                           \      │      /
                   [ AP ]   \     │     /
                             \    │    /
                              \   │   /
                               \  │  /
                                \ │ /
                                 \│/
                                  ▼
                          Availability (A)

        Note: In distributed systems, Partition Tolerance (P) is mandatory.
        Therefore, the real choice is between CP and AP.

========================================================================================================
                              [ CP vs AP SYSTEM BEHAVIOR ]
========================================================================================================

  [ CP SYSTEM (Consistency + Partition Tolerance) ]

  Normal Operation:                Partition Scenario:
  ┌───────┐    ┌───────┐          ┌───────┐ XX ┌───────┐
  │ Node1 │◄──►│ Node2 │          │ Node1 │ XX │ Node2 │
  │ v=10  │    │ v=10  │          │ v=10  │ XX │ v=10  │
  └───────┘    └───────┘          └───────┘ XX └───────┘
      │            │                   ▲        XX
      │ Sync Write │                   │        XX
      ▼            ▼                ┌──┴──┐     XX
  ┌─────────────────┐              │Write│     XX
  │ Client Write    │              │Fail!│     XX
  │ v=20            │              └─────┘     XX
  └─────────────────┘                          XX
                                     Returns Error to Client

  Examples: MongoDB (Primary down = write fail), HBase, Redis Cluster
  Trade-off: Strong consistency but reduced availability during partitions


  [ AP SYSTEM (Availability + Partition Tolerance) ]

  Normal Operation:                Partition Scenario:
  ┌───────┐    ┌───────┐          ┌───────┐ XX ┌───────┐
  │ Node1 │◄──►│ Node2 │          │ Node1 │ XX │ Node2 │
  │ v=10  │    │ v=10  │          │ v=20  │ XX │ v=10  │
  └───────┘    └───────┘          └───────┘ XX └───────┘
      │            │                   ▲        XX
      │ Async Write│                   │        XX
      ▼            ▼                ┌──┴──┐     XX
  ┌─────────────────┐              │Write│     XX
  │ Client Write    │              │ OK! │     XX
  │ v=20            │              └─────┘     XX
  └─────────────────┘                          XX
                                     Returns Success (Inconsistent State)

  Examples: Cassandra, DynamoDB, CouchDB
  Trade-off: Always available but temporary inconsistency (Eventual Consistency)

========================================================================================================
                              [ QUORUM AND CONSISTENCY LEVELS ]
========================================================================================================

  Replication Factor (RF) = 3
  Write Quorum (W) = 2, Read Quorum (R) = 2
  W + R > RF ensures strong consistency

  ┌─────────────────────────────────────────────────────────────────────┐
  │                      READ/WRITE QUORUM                              │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │   Node 1        Node 2        Node 3                               │
  │   ┌─────┐       ┌─────┐       ┌─────┐                              │
  │   │ v=5 │       │ v=5 │       │ v=3 │  (Stale)                     │
  │   └──┬──┘       └──┬──┘       └──┬──┘                              │
  │      │             │             │                                 │
  │      ▼             ▼             ▼                                 │
  │   ┌─────────────────────────────────┐                              │
  │   │  Read Quorum (R=2): Read from   │                              │
  │   │  2 nodes, return latest value   │                              │
  │   │  → Returns v=5 (from Node 1,2)  │                              │
  │   └─────────────────────────────────┘                              │
  │                                                                     │
  │   ┌─────────────────────────────────┐                              │
  │   │  Write Quorum (W=2): Write to   │                              │
  │   │  2 nodes before acknowledging   │                              │
  │   │  → Node 3 updated asynchronously│                              │
  │   └─────────────────────────────────┘                              │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘

  Consistency Level Options:
  - ONE: Fastest, weakest consistency
  - QUORUM: Balanced (W + R > RF)
  - ALL: Strongest, slowest

========================================================================================================
```

### 심층 동작 원리: Quorum 기반 일관성 제어

**1. Quorum 공식과 일관성 보장**
```text
Quorum 일관성 조건:
W + R > RF (Replication Factor)

예시: RF = 3
- W=2, R=2: Strong Consistency (2+2=4 > 3)
- W=1, R=1: Weak Consistency (1+1=2 ≤ 3) - Stale read 가능
- W=3, R=1: Strong Consistency (3+1=4 > 3)
- W=1, R=3: Strong Consistency (1+3=4 > 3)

지연 시간 vs 일관성 트레이드오프:
- 높은 W: 쓰기 지연 증가, 일관성 향상
- 높은 R: 읽기 지연 증가, 일관성 향상
```

**2. DynamoDB 일관성 모델**
```python
# DynamoDB 읽기 일관성 옵션
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

# Eventually Consistent Read (기본, 저비용)
response = table.get_item(
    Key={'user_id': '123'}
)
# 비용: 1 RCU per 4KB

# Strongly Consistent Read
response = table.get_item(
    Key={'user_id': '123'},
    ConsistentRead=True
)
# 비용: 2 RCU per 4KB (2배)
# 항상 최신 데이터 보장

# Transactional Read (ACID)
response = dynamodb.meta.client.transact_get_items(
    TransactItems=[
        {
            'Get': {
                'TableName': 'Users',
                'Key': {'user_id': {'S': '123'}}
            }
        },
        {
            'Get': {
                'TableName': 'Orders',
                'Key': {'order_id': {'S': '456'}}
            }
        }
    ]
)
# 비용: 2x Strongly Consistent Read
# 여러 아이템의 원자적 읽기
```

**3. Cassandra Tunable Consistency**
```java
// Cassandra 일관성 수준 튜닝 (Java Driver)
import com.datastax.driver.core.ConsistencyLevel;
import com.datastax.driver.core.querybuilder.QueryBuilder;

// 쓰기 일관성: QUORUM
Statement writeStmt = QueryBuilder.insertInto("users")
    .value("user_id", "123")
    .value("name", "John")
    .setConsistencyLevel(ConsistencyLevel.QUORUM);

// 읽기 일관성: LOCAL_QUORUM (로컬 DC만)
Statement readStmt = QueryBuilder.select()
    .from("users")
    .where(QueryBuilder.eq("user_id", "123"))
    .setConsistencyLevel(ConsistencyLevel.LOCAL_QUORUM);

// 일관성 수준별 특성
// ONE: 1개 노드만 응답 (빠름, 약한 일관성)
// QUORUM: 과반수 응답 (균형)
// ALL: 모든 노드 응답 (강한 일관성, 느림)
// LOCAL_QUORUM: 로컬 DC 내 과반수 (글로벌 배포)
// EACH_QUORUM: 각 DC별 과반수 (강한 글로벌 일관성)
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: CP vs AP 시스템

| 비교 지표 | CP (Consistency + Partition Tolerance) | AP (Availability + Partition Tolerance) |
|---|---|---|
| **대표 DB** | MongoDB, HBase, Redis Cluster | Cassandra, DynamoDB, CouchDB |
| **장애 대응** | 쓰기 거부 (일관성 유지) | 쓰기 허용 (일시적 불일치) |
| **지연 시간** | 높음 (동기 복제) | 낮음 (비동기 복제) |
| **복잡성** | 낮음 (Strong Consistency) | 높음 (Conflict Resolution) |
| **Use Case** | 금융, 주문, 재고 | SNS, IoT, 로그, 캐시 |
| **Trade-off** | 가용성 희생 | 일관성 희생 |

### PACELC 이론 (CAP의 확장)

```text
PACELC (2012, Daniel Abadi):

If Partition (P):    Choose Availability (A) or Consistency (C)
Else (E):            Choose Latency (L) or Consistency (C)

┌─────────────────────────────────────────────────────────────────────┐
│                     PACELC DECISION TREE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                        Is there a Partition?                        │
│                             /       \                               │
│                          Yes         No                             │
│                           /           \                             │
│                  ┌───────▼───────┐   ┌▼───────────────┐             │
│                  │ Choose A or C │   │ Choose L or C  │             │
│                  │               │   │                │             │
│                  │ A: Available  │   │ L: Low Latency │             │
│                  │ C: Consistent │   │ C: Consistent  │             │
│                  └───────────────┘   └────────────────┘             │
│                                                                     │
│  Examples:                                                          │
│  - PC/EC: MongoDB, HBase (Consistency always)                       │
│  - PA/EL: Cassandra, DynamoDB (Availability & Low Latency)          │
│  - PA/EC: MySQL + Replication (Async replication)                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 과목 융합 관점 분석

- **[네트워크 + CAP]**: CAP의 P(Partition)는 네트워크 레이어에서 발생합니다. **네트워크 지연**, **패킷 손실**, **라우터 장애** 등이 Partition을 유발하며, 이를 감지하고 대응하는 메커니즘(Gossip, Heartbeat)이 분산 시스템에 내장됩니다.

- **[운영체제 + CAP]**: 분산 시스템의 **타이머**, **동기화**, **메모리 모델**은 CAP 구현에 영향을 미칩니다. Vector Clock, Lamport Timestamp 등 **논리적 시계**는 물리적 시계의 불일치 문제를 해결합니다.

- **[데이터베이스 + CAP]**: CAP는 RDBMS의 ACID와 상충합니다. NoSQL은 ACID를 포기하고 **BASE(Basically Available, Soft state, Eventually consistent)** 모델을 채택합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 금융 거래 시스템 - CP 선택**
- **문제**: 계좌 이체 시 잔액 부족을 정확히 감지해야 함
- **전략적 의사결정**:
  1. **CP 시스템 선택**: MongoDB 또는 RDBMS with distributed transactions
  2. **Strong Consistency**: 모든 거래는 동기 복제 후 승인
  3. **Partition 대응**: 장애 시 거래 거부 (일관성 우선)
  4. **HA 구성**: 다중 리전으로 가용성 보완

**시나리오 2: 소셜 미디어 피드 - AP 선택**
- **문제**: 전 세계 사용자의 실시간 피드, 99.99% 가용성 요구
- **전략적 의사결정**:
  1. **AP 시스템 선택**: Cassandra 또는 DynamoDB
  2. **Eventual Consistency**: 피드 업데이트는 몇 초 지연 허용
  3. **Multi-Region**: 각 리전에 로컬 복제본, 지연 최소화
  4. **Conflict Resolution**: Last-Write-Wins 또는 Application-level merge

**시나리오 3: 쇼핑몰 재고 관리 - Hybrid 접근**
- **문제**: 재고 초과 판매 방지(Consistency) + 높은 트래픽(Availability)
- **전략적 의사결정**:
  1. **CQRS 패턴**: 읽기(AP) + 쓰기(CP) 분리
  2. **Redis Cache**: 조회는 캐시에서 빠르게 (AP)
  3. **RDBMS Lock**: 재고 차감은 트랜잭션으로 (CP)
  4. **Saga Pattern**: 분산 트랜잭션 보상 로직

### 주의사항 및 안티패턴 (Anti-patterns)

- **안티패턴 - CAP 오해**: CAP는 "3개 중 2개 선택"이 아니라, **P는 필수이고 C와 A 중 선택**입니다. 네트워크는 언제나 분할될 수 있습니다.

- **안티패턴 - 잘못된 일관성 수준**: 모든 쿼리에 Strong Consistency를 사용하면 성능 저하. **Use Case별로 적절한 수준** 선택 필요

- **안티패턴 - Conflict Resolution 미흡**: AP 시스템에서 충돌 해결 전략(LWW, CRDT, Application merge)이 없으면 데이터 손실 가능

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | 내용 및 지표 |
|---|---|
| **정성적 효과** | - 분산 시스템 설계 시 트레이드오프 명시적 인식<br>- 비즈니스 요구사항에 맞는 DB 선택 기준 제공<br>- 장애 상황 대응 전략 수립 가능 |
| **정량적 효과** | - 시스템 가용성 **99.99%** 달성 (AP)<br>- 데이터 일관성 **99.999%** 보장 (CP)<br>- 적절한 일관성 수준으로 지연 시간 **50~90% 감소** |

### 미래 전망 및 진화 방향

- **Tunable Consistency**: 쿼리 단위로 일관성 수준 동적 조정
- **CRDT (Conflict-free Replicated Data Types)**: 충돌 없는 자동 병합
- **NewSQL**: CAP를 극복하는 새로운 접근 (Spanner, CockroachDB)

**※ 참고 표준/가이드**:
- **Brewer's Conjecture (2000)**: CAP 정리 원론
- **PACELC (2012)**: CAP 확장 이론
- **Dynamo Paper (2007)**: AP 시스템 실제 구현

---

## 📌 관련 개념 맵 (Knowledge Graph)

- `[BASE 속성](@/studynotes/16_bigdata/05_nosql/base_properties.md)`: NoSQL의 완화된 일관성 모델
- `[Eventual Consistency](@/studynotes/16_bigdata/05_nosql/eventual_consistency.md)`: 결과적 일관성 원리
- `[Quorum](@/studynotes/16_bigdata/02_distributed/quorum.md)`: 일관성 보장을 위한 투표 메커니즘
- `[Cassandra](@/studynotes/16_bigdata/05_nosql/cassandra.md)`: AP 시스템 대표 DB
- `[MongoDB](@/studynotes/16_bigdata/05_nosql/mongodb.md)`: CP 시스템 대표 DB

---

## 👶 어린이를 위한 3줄 비유 설명

1. **CAP가 뭔가요?**: 친구 두 명이 다른 교실에 있을 때, **세 가지 중 두 가지만** 가질 수 있다는 법칙이에요. (1) 두 친구가 같은 정보를 알고, (2) 항상 연락이 되고, (3) 통신이 끊겨도 연락하는 건 불가능해요!
2. **왜 중요한가요?**: 인터넷 쇼핑할 때, 물건이 다 팔렸는데도 산다고 나오면 안 되잖아요? 그래서 **정확한 정보**와 **빠른 연결** 사이에서 선택해야 해요.
3. **어떻게 써요?**: 은행은 돈을 정확하게 세는 게 중요해서(C), 게임은 끊기지 않는 게 중요해서(A) 다르게 만들어요!
