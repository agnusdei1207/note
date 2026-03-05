+++
title = "MongoDB (문서형 데이터베이스)"
categories = ["studynotes-16_bigdata"]
+++

# MongoDB (문서형 데이터베이스)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MongoDB는 **JSON-like 문서(BSON)**를 저장하는 분산 문서형 데이터베이스로, 유연한 스키마(Schema-less), 수평 확장(Sharding), 고가용성(Replica Set)을 특징으로 합니다.
> 2. **가치**: 개발 생산성을 높이는 **풍부한 쿼리 언어**, 인덱싱, Aggregation Pipeline을 제공하며, RDBMS 대비 **스키마 변경 비용이 거의 없어** agile 개발에 최적화되어 있습니다.
> 3. **융합**: Atlas(Managed Cloud), Compass(GUI), Atlas Search(전문 검색), Atlas Data Lake(분석)로 구성된 **통합 데이터 플랫폼**으로 진화했습니다.

---

## Ⅰ. 개요 (Context & Background)

MongoDB는 2009년 10gen(현 MongoDB Inc.)에서 개발된 NoSQL 데이터베이스로, **"개발자 친화적"**인 설계 철학을 가집니다. 관계형 데이터베이스의 JOIN과 정규화 대신 **문서 내 중첩(Embedding)** 방식으로 데이터를 모델링합니다.

**💡 비유: 서류철 vs 엑셀**
RDBMS는 **엑셀 시트 여러 개를 JOIN으로 연결**하는 방식입니다. 반면 MongoDB는 **두꺼운 서류철**입니다. 한 사람의 모든 정보(이름, 주소, 주문 내역, 즐겨찾기)를 **한 페이지(문서)**에 모두 적어둡니다. 서류철이 꽉 차면 옆에 새 서류철(Shard)을 추가하면 됩니다.

**등장 배경 및 발전 과정:**
1. **기존 기술의 치명적 한계점**: RDBMS는 스키마 변경이 어렵고, 객체-관계 매핑(ORM)이 복잡하며, 수평 확장이 어렵습니다.
2. **혁신적 패러다임 변화**: **Document Model** 도입으로 애플리케이션 객체와 저장 형식을 일치시켰고, **BSON(Binary JSON)**으로 효율적인 직렬화를 구현했습니다.
3. **비즈니스적 요구사항**: Agile 개발, 마이크로서비스, 실시간 데이터 처리 등 **빠른 변화와 확장성**이 요구되는 환경에서 채택되었습니다.

---

## Ⅱ. 아키키처 및 핵심 원리 (Deep Dive)

### MongoDB 핵심 구성 요소

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|---|---|---|---|---|
| **Document** | 데이터 저장 단위 | BSON 직렬화, 최대 16MB | JSON, BSON | 서류 한 장 |
| **Collection** | 문서 그룹화 | 논리적 컨테이너, 인덱스 공유 | Table(유사) | 서류철 |
| **Replica Set** | 고가용성 복제 | Primary-Secondary, Oplog 복제 | Election, Failover | 복사본 |
| **Shard** | 수평 분할 | Config Server, Mongos 라우터 | Hash/Range Sharding | 서류철 분리 |
| **Aggregation** | 데이터 처리 파이프라인 | $match, $group, $lookup 단계 | Map-Reduce(구) | 데이터 가공 |

### 정교한 구조 다이어그램 (ASCII Art)

```text
========================================================================================================
                              [ MONGODB REPLICA SET ARCHITECTURE ]
========================================================================================================

                    [ CLIENT APPLICATION ]
                           |
                    +------▼------+
                    |   Driver    |
                    +------+------+
                           |
                    +------▼------+
                    |   Mongos    |  (Sharded Cluster인 경우)
                    +------+------+
                           |
         +-----------------+-----------------+
         |                 |                 |
    +----▼----+       +----▼----+       +----▼----+
    | Primary |       |Secondary|       |Secondary|
    | (Read/  |------>| (Read   |------>| (Read   |
    |  Write) |  Oplog|  Only)  |  Oplog|  Only)  |
    +----+----+       +---------+       +---------+
         |
         v Heartbeat
    [ Election Trigger if Primary Down ]

    Oplog (Operations Log):
    - Capped Collection (고정 크기)
    - 모든 쓰기 연산 기록
    - Secondary가 복제를 위해 읽음

========================================================================================================
                              [ MONGODB SHARDED CLUSTER ]
========================================================================================================

  [ APPLICATION ]
        |
  +-----▼-----+
  |  Mongos   |  (Query Router)
  +-----+-----+
        |
        v (Route to correct shard based on shard key)
  +-----+-------------------------------------------------------+
  |                    Config Servers                          |
  |  (Metadata: which shard has which data)                   |
  +-----+-------------------------------------------------------+
        |
  +-----+-----+-----+-----+-----+-----+
  |     |     |     |     |     |     |
  ▼     ▼     ▼     ▼     ▼     ▼     ▼
+----++----++----++----++----++----++----+
| S1 || S2 || S3 || S4 || S5 || S6 ||... |  (Shards)
| RS || RS || RS || RS || RS || RS ||    |  (Each is a Replica Set)
+----++----++----++----++----++----++----+

  Shard Key Strategies:
  1. Ranged Sharding: key 1-100 → S1, 101-200 → S2 (Hotspot 위험)
  2. Hashed Sharding: hash(key) % N → Even distribution (권장)
  3. Zone Sharding: Geographic/data-based routing

========================================================================================================
                              [ BSON DOCUMENT STRUCTURE ]
========================================================================================================

  {
    "_id": ObjectId("507f1f77bcf86cd799439011"),   // 12-byte ObjectId
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "address": {                                   // Embedded Document
      "street": "123 Main St",
      "city": "Seoul",
      "zip": "12345"
    },
    "orders": [                                    // Array of Documents
      {
        "order_id": "ORD001",
        "items": ["item1", "item2"],
        "total": 99.99,
        "created_at": ISODate("2024-01-15T10:30:00Z")
      }
    ],
    "tags": ["premium", "vip"],                   // Array
    "metadata": {                                 // Flexible Schema
      "source": "mobile",
      "campaign": "summer2024"
    }
  }

  Key Features:
  - _id: Auto-generated if not provided (12-byte)
  - Nested documents (Embedded)
  - Arrays with indexing support
  - Multiple data types (String, Number, Date, Binary, etc.)

========================================================================================================
```

### 심층 동작 원리: Sharding과 Replica Set

**1. Replica Set 구성 및 장애 복구**
```javascript
// Replica Set 초기화 (MongoDB Shell)
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017", priority: 2 },
    { _id: 1, host: "mongo2:27017", priority: 1 },
    { _id: 2, host: "mongo3:27017", priority: 1, arbiterOnly: true }
  ]
})

// 상태 확인
rs.status()

// 장애 복구 프로세스:
// 1. Primary와의 Heartbeat 실패 (10초 기본)
// 2. Secondary들이 Election 시작
// 3. 과반수 투표로 새 Primary 선출
// 4. Client는 새 Primary로 자동 라우팅
```

**2. Sharding 설정**
```javascript
// Sharded Cluster 설정
// 1. Config Server 시작 (Replica Set)
// 2. Shard 서버 시작 (각각 Replica Set)
// 3. Mongos 라우터 시작

// Mongos에서 샤드 추가
sh.addShard("rs1/mongo1:27017,mongo2:27017,mongo3:27017")
sh.addShard("rs2/mongo4:27017,mongo5:27017,mongo6:27017")

// 데이터베이스에 샤딩 활성화
sh.enableSharding("mydb")

// 컬렉션 샤딩 (Hashed Sharding)
sh.shardCollection("mydb.users", { "user_id": "hashed" })

// Ranged Sharding (순서 중요한 경우)
sh.shardCollection("mydb.logs", { "timestamp": 1 })
```

**3. Aggregation Pipeline**
```javascript
// MongoDB Aggregation Pipeline 예시
// 주문 데이터 분석: 월별 카테고리 매출 집계

db.orders.aggregate([
  // 1단계: 날짜 필터링
  {
    $match: {
      order_date: {
        $gte: ISODate("2024-01-01"),
        $lt: ISODate("2024-12-31")
      }
    }
  },

  // 2단계: 월/카테고리 추출
  {
    $project: {
      month: { $month: "$order_date" },
      category: "$items.category",
      total: "$total_amount",
      customer_id: 1
    }
  },

  // 3단계: 배열 펼치기 (items가 배열인 경우)
  {
    $unwind: "$category"
  },

  // 4단계: 그룹화 및 집계
  {
    $group: {
      _id: {
        month: "$month",
        category: "$category"
      },
      total_sales: { $sum: "$total" },
      order_count: { $sum: 1 },
      unique_customers: { $addToSet: "$customer_id" }
    }
  },

  // 5단계: 정렬
  {
    $sort: { "_id.month": 1, "total_sales": -1 }
  },

  // 6단계: 결과 포맷팅
  {
    $project: {
      _id: 0,
      month: "$_id.month",
      category: "$_id.category",
      total_sales: 1,
      order_count: 1,
      unique_customer_count: { $size: "$unique_customers" }
    }
  }
])

// Lookup (LEFT JOIN 유사)
db.orders.aggregate([
  {
    $lookup: {
      from: "customers",
      localField: "customer_id",
      foreignField: "_id",
      as: "customer_info"
    }
  },
  {
    $unwind: "$customer_info"
  }
])
```

**4. 인덱스 최적화**
```javascript
// 인덱스 생성
// 1. 단일 필드 인덱스
db.users.createIndex({ "email": 1 }, { unique: true })

// 2. 복합 인덱스 (쿼리 패턴에 맞게 설계)
db.orders.createIndex({ "customer_id": 1, "order_date": -1 })

// 3. 멀티키 인덱스 (배열 필드)
db.products.createIndex({ "tags": 1 })

// 4. 텍스트 인덱스 (전문 검색)
db.articles.createIndex({ "content": "text" })

// 5. 지리공간 인덱스
db.stores.createIndex({ "location": "2dsphere" })

// 인덱스 사용 확인
db.orders.find({ "customer_id": "C001" }).explain("executionStats")

// Covered Query (인덱스만으로 조회 완료)
db.users.find(
  { "email": "john@example.com" },
  { "_id": 0, "name": 1, "email": 1 }  // 인덱스에 포함된 필드만
)
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: MongoDB vs PostgreSQL vs DynamoDB

| 비교 지표 | MongoDB | PostgreSQL | DynamoDB |
|---|---|---|---|
| **데이터 모델** | Document | Relational | Key-Value |
| **스키마** | Flexible | Rigid | Flexible |
| **JOIN** | $lookup (제한적) | 완벽 지원 | 미지원 |
| **트랜잭션** | 4.0+ 지원 | 완벽 지원 | 지원 |
| **확장성** | Sharding | Read Replicas | Auto-scaling |
| **일관성** | Tunable | Strong | Tunable |
| **적합 Use Case** | CMS, IoT, 실시간 | ERP, 금융 | 세션, 게임 |

### 과목 융합 관점 분석

- **[데이터베이스 + MongoDB]**: MongoDB의 **Embedded Document** 패턴은 정규화 대신 **중복을 허용**하는 설계입니다. 이는 읽기 성능을 높이지만, 데이터 일관성 관리가 복잡해집니다.

- **[운영체제 + MongoDB]**: MongoDB는 **Memory-Mapped Files**를 사용하여 OS의 페이지 캐시를 활용합니다. WiredTiger 스토리지 엔진은 자체 캐시를 관리하여 더 나은 제어를 제공합니다.

- **[네트워크 + MongoDB]**: Replica Set 간 **Oplog 복제**는 네트워크 대역폭을 소모합니다. Cross-region 복제 시 네트워크 지연이 쓰기 성능에 영향을 미칩니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 콘텐츠 관리 시스템(CMS) 구축**
- **문제**: 다양한 유형의 콘텐츠(블로그, 동영상, 상품)를 하나의 DB에 저장
- **전략적 의사결정**:
  1. **Polymorphic Pattern**: type 필드로 문서 유형 구분
  2. **Bucket Pattern**: 배열 필드로 하위 데이터 저장
  3. **Change Streams**: 실시간 알림 구현

**시나리오 2: 대규모 로그 분석 플랫폼**
- **문제**: 초당 10만 개의 로그 저장 및 실시간 집계
- **전략적 의사결정**:
  1. **Time Series Collection**: MongoDB 5.0+ 최적화
  2. **TTL 인덱스**: 30일 후 자동 삭제
  3. **Sharding**: timestamp 기준 ranged sharding

### 주의사항 및 안티패턴 (Anti-patterns)

- **안티패턴 - 무제한 배열**: 배열이 계속 커지면 16MB 문서 제한 도달. **Bucket Pattern**으로 분할

- **안티패턴 - Shard Key 선택 실패**: 카디널리티가 낮거나 단조 증가하는 키는 **Hot Partition** 유발

- **안티패턴 - 과도한 $lookup**: JOIN에 의존하면 성능 저하. **Embedded 패턴**으로 재설계

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | 내용 및 지표 |
|---|---|
| **정성적 효과** | - 스키마 변경 자유로움<br>- 개발 생산성 향상<br>- JSON 네이티브 지원 |
| **정량적 효과** | - 개발 속도 **30~50% 향상**<br>- 수평 확장으로 **선형 성능 증가**<br>- TCO **40% 절감** (Atlas) |

### 미래 전망 및 진화 방향

- **Atlas Vector Search**: 벡터 임베딩 검색으로 AI/ML 지원
- **Atlas Data API**: Serverless 데이터 액세스
- **MongoDB 7.0+:** 향상된 쿼리 성능, 새로운 연산자

**※ 참고 표준/가이드**:
- **MongoDB Documentation**: 공식 문서
- **MongoDB University**: 무료 교육 자료

---

## 📌 관련 개념 맵 (Knowledge Graph)

- `[NoSQL 개요](@/studynotes/16_bigdata/05_nosql/nosql_overview.md)`: NoSQL 기본 개념
- `[Redis](@/studynotes/16_bigdata/05_nosql/redis.md)`: 인메모리 Key-Value
- `[Cassandra](@/studynotes/16_bigdata/05_nosql/cassandra.md)**: Column-Family DB
- `[Document Database](@/studynotes/16_bigdata/05_nosql/document_db.md)`: 문서형 DB 패턴
- `[Sharding](@/studynotes/16_bigdata/02_distributed/sharding.md)`: 데이터 분할 전략

---

## 👶 어린이를 위한 3줄 비유 설명

1. **MongoDB가 뭔가요?**: **커다란 공책** 같아요. 한 페이지에 한 사람의 모든 정보(이름, 주소, 좋아하는 것 등)를 다 적을 수 있어요.
2. **다른 DB와 뭐가 달라요?**: 엑셀은 여러 시트를 연결해야 하지만, MongoDB는 **한 페이지에 다 적을 수 있어서** 찾기 편해요!
3. **어디에 쓰나요?**: 인스타그램, 이베이 같이 **다양한 정보를 빠르게 저장하고 찾아야 하는 곳**에서 써요!
