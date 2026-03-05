+++
title = "NoSQL 데이터베이스 (NoSQL Databases)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# NoSQL 데이터베이스 (NoSQL Databases)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NoSQL(Not Only SQL)은 관계형 모델을 따르지 않는 데이터베이스로, 키-값, 도큐먼트, 컬럼 패밀리, 그래프 등 4가지 유형이 있으며, 수평 확장과 유연한 스키마에 특화되어 있습니다.
> 2. **가치**: 대용량 데이터 처리, 높은 쓰기 처리량, 유연한 스키마, 수평 확장이 가능하여 빅데이터와 실시간 웹 애플리케이션에 최적화되어 있습니다.
> 3. **융합**: CAP 정리에 따라 일관성(Consistency), 가용성(Availability), 파티션 감내(Partition Tolerance) 중 2가지를 선택하는 트레이드오프가 존재합니다.

---

### Ⅰ. 개요

#### 1. NoSQL 4가지 유형

| 유형 | 설명 | 대표 제품 | 활용 사례 |
|:---|:---|:---|:---|
| **키-값 (Key-Value)** | 단순 키-값 쌍 저장 | Redis, Memcached | 캐시, 세션 |
| **도큐먼트 (Document)** | JSON/BSON 문서 저장 | MongoDB, CouchDB | 콘텐츠 관리, 카탈로그 |
| **컬럼 패밀리 (Wide-Column)** | 컬럼 단위 저장 | Cassandra, HBase | 시계열, 로그 |
| **그래프 (Graph)** | 노드-엣지 관계 저장 | Neo4j, Neptune | 소셜 네트워크, 추천 |

#### 2. RDBMS vs NoSQL

| 비교 | RDBMS | NoSQL |
|:---|:---|:---|
| **스키마** | 고정 | 유연 |
| **확장** | 수직 | 수평 |
| **트랜잭션** | ACID | BASE |
| **쿼리** | SQL | API/전용 쿼리 |

---

### Ⅱ. 아키텍처

```text
<<< NoSQL Data Models >>>

[Key-Value Store]
+-------+------------------+
| Key   | Value            |
+-------+------------------+
| user:1| {"name":"홍길동"} |
| user:2| {"name":"김철수"} |
+-------+------------------+

[Document Store]
{
  "_id": "user_001",
  "name": "홍길동",
  "orders": [
    {"product": "laptop", "price": 1500000},
    {"product": "mouse", "price": 50000}
  ]
}

[Wide-Column Store]
Row Key: user_001
+----------------+----------------+----------------+
| Column Family: Profile          | Column Family: Orders        |
+----------------+----------------+----------------+
| name: 홍길동   | age: 30        | order_1: {...} |
+----------------+----------------+----------------+

[Graph Database]
(User) ---[FRIEND]---> (User)
  |                       |
[PURCHASED]          [PURCHASED]
  |                       |
(Product) <---------- (Product)
```

---

### Ⅲ. CAP 정리와 BASE

#### 1. CAP 정리
```text
분산 시스템은 세 가지 중 두 가지만 만족 가능:

C (Consistency): 모든 노드가 동시에 같은 데이터 반환
A (Availability): 모든 요청이 응답을 받음 (실패/성공)
P (Partition Tolerance): 네트워크 분할 시에도 시스템 동작

[선택 예시]
- CP: MongoDB (일관성 우선)
- AP: Cassandra (가용성 우선)
- CA: 단일 노드 RDBMS (분산 불가)
```

#### 2. BASE 특성
- **Basically Available**: 기본적으로 가용
- **Soft State**: 상태가 시간에 따라 변할 수 있음
- **Eventually Consistent**: 일정 시간 후 일관성 달성

---

### Ⅳ. 실무 적용

```python
# MongoDB 예시
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce']
products = db['products']

# 도큐먼트 삽입
products.insert_one({
    "name": "무선 키보드",
    "price": 59000,
    "category": "전자기기",
    "specs": {"connectivity": "Bluetooth", "battery": "AA"}
})

# 쿼리
result = products.find({"category": "전자기기", "price": {"$lt": 100000}})
```

---

### Ⅴ. 결론

NoSQL은 대용량, 유연한 스키마, 수평 확장이 필요한 현대 애플리케이션의 핵심 데이터베이스입니다.

---

### 관련 개념 맵
- **[CAP 정리](@/studynotes/14_data_engineering/01_data_arch/cap_theorem.md)**
- **[MongoDB](@/studynotes/14_data_engineering/01_data_arch/mongodb.md)**
- **[Redis](@/studynotes/14_data_engineering/01_data_arch/redis.md)**

---

### 어린이를 위한 3줄 비유
1. **여러 가지 서랍**: NoSQL은 여러 종류의 서랍이 있어요. 편지 넣는 서랍, 사진 넣는 서랍, 물건 넣는 서랍!
2. **마음대로 넣기**: 서랍마다 규칙이 달라요. 어떤 건 그냥 넣고, 어떤 건 이름표를 붙여요.
3. **친구와 나눠요**: 서랍이 부족하면 친구 집에도 나눠서 보관해요. 한 집이 불 나도 괜찮아요!
