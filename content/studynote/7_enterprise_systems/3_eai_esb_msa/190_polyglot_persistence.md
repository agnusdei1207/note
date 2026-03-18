+++
title = "190. 폴리글랏 퍼시스턴스 (Polyglot Persistence)"
date = "2026-03-18"
[extra]
category = "studynote-enterprise"
keywords = ["Polyglot Persistence", "폴리글랏 퍼시스턴스", "MSA", "Microservices", "Database", "NoSQL", "Multi-model", "Right Tool for Right Job"]
+++

# 폴리글랏 퍼시스턴스 (Polyglot Persistence)

> **Polyglot Persistence**: 각 마이크로서비스의 **데이터 접근 패턴과 특성에 최적화된 데이터베이스를 독립적으로 선택**하여 전체 시스템의 성능과 확장성을 극대화하는 아키텍처 패턴으로, **"하나의 DB(One Size Fits All)"** 사고를 버리고 **"적합한 도구를 적합한 곳에(Right Tool for Right Job)"** 적용하는 전략입니다

## 핵심 인사이트

모놀리식 애플리케이션은 단일 RDBMS에 모든 데이터를 통합하는 **"데이터베이스 중심"** 아키텍처였습니다. 하지만 마이크로서비스는 각 서비스가 **독립적인 도메인과 데이터 모델**을 가지므로, 데이터베이스 선택의 자유가 생겼습니다. **폴리글랏 퍼시스턴스**는 사용자 서비스는 **관계형 DB**로 ACID 트랜잭션이 필요하고, 카탈로그 서비스는 **문서 DB**로 유연한 스키마가 필요하고, 추천 서비스는 **그래프 DB**로 관계 탐색이 필요하다는 인식에서 시작됩니다. 각 서비스는 자신만의 DB를 가지며, 다른 서비스의 DB에 **직접 접근할 수 없습니다(API 통신만 허용)**.

---

## Ⅰ. 개념 정의 및 등장 배경

### 1. 정의

**폴리글랏 퍼시스턴스(Polyglot Persistence)**는 2011년 Martin Fowler와 Pramod Sadalage가 제안한 개념으로, **"다양한 데이터 저장소 기술을 혼합 사용"**하는 전략입니다.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    폴리글랏 퍼시스턴스 기본 개념                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   🔄 패러다임 전환                                                          │
│                                                                             │
│   ❌ 전통적 접근 (One Size Fits All)                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │  │
│  │   ┌──────────────────────────────────────────────────────────────┐  │  │
│  │   │                     단일 RDBMS                             │  │  │
│  │   │                     (Oracle/MySQL)                         │  │  │
│  │   │                                                              │  │
│  │   │   ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌─────────┐ │  │
│  │   │   │ 사용자    │  │ 주문      │  │ 상품      │  │ 로그   │ │  │
│  │   │   │ Table     │  │ Table     │  │ Table     │  │ Table  │ │  │
│  │   │   └───────────┘  └───────────┘  └───────────┘  └─────────┘ │  │
│  │   │                                                              │  │
│  │   │   "모든 데이터는 관계형 테이블에!"                             │  │
│  │   │                                                             │  │
│  │   └──────────────────────────────────────────────────────────────┘  │  │
│  │                                                                      │  │
│  │   문제점:                                                            │  │
│  │   • 사용자 프로필: JOIN 복잡, 스키마 변경 어려움                   │  │
│  │   • 상품 카탈로그: 계층 구조 표현 불편 (JSON 파싱)                   │  │
│  │   • 추천 엔진: 그래프 쿼리 없음, 복잡한 연산                      │  │
│  │   • 로그: 대용량 INSERT/SELECT 부하, 비용 높음                      │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   ✅ 폴리글랏 퍼시스턴스 접근 (Right Tool for Right Job)                    │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │  │
│  │   사용자 서비스          주문 서비스          상품 서비스              │  │
│  │   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐       │  │
│  │   │ PostgreSQL   │     │ PostgreSQL   │     │  MongoDB     │       │  │
│  │   │ (관계형)     │     │ (관계형)     │     │  (문서형)    │       │  │
│  │   └──────────────┘     └──────────────┘     └──────────────┘       │  │
│  │                                                                      │  │
│  │   추천 서비스          세션 서비스          로그 서비스               │  │
│  │   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐       │  │
│  │   │  Neo4j      │     │    Redis    │     │ Elasticsearch│       │  │
│  │   │  (그래프)    │     │  (Key-Value) │     │  (검색엔진)   │       │  │
│  │   └──────────────┘     └──────────────┘     └──────────────┘       │  │
│  │                                                                      │  │
│  │   "각 서비스에 맞는 최적의 DB 선택!"                                 │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 등장 배경

| 요인 | 설명 | 해결책 |
|:-----|:-----|:-------|
| **다양한 데이터 모델** | 관계형, 문서, 그래프, 키-값 등 | 각 모델에 최적화된 DB 선택 |
| **확장성 요구** | 수평적 확장이 필수인 시대 | NoSQL의 자동 샤딩 활용 |
| **성능 요구** | 초단위 응답, 대규모 트래픽 | 인메모리 DB, 분산 캐시 |
| **유연성 요구** | 스키마리스, 빠른 반복 | 문서 DB, 칼럼 family DB |
| **비용 효율** | 상용 DB 라이선스 비용 | 오픈 소스 NoSQL, 클라우드 네이티브 |

### 3. 데이터 모델별 특성

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    데이터 모델별 최적 사용 사례                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1. 관계형 모델 (Relational)                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 대표: MySQL, PostgreSQL, Oracle                                  │  │
│  │   • 특징: ACID 트랜잭션, 구조화된 쿼리, JOIN 지원                     │  │
│  │   • 적합한 경우:                                                      │  │
│  │     - 사용자 계정 (일관성 중요)                                        │  │
│  │     - 주문/결제 (트랜잭션 필수)                                      │  │
│  │     - 재고 관리 (정확성 중요)                                        │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   2. 문서 모델 (Document)                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 대표: MongoDB, Couchbase                                         │  │
│  │   • 특징: 스키마리스, 중첩 구조, JSON 기반                            │  │
│  │   • 적합한 경우:                                                      │  │
│  │     - 상품 카탈로그 (속성 다양함)                                     │  │
│  │     - 컨텐츠 관리 (CMS)                                              │  │
│  │     - 프로필 (구조 유연)                                              │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   3. 키-값 모델 (Key-Value)                                                │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 대표: Redis, DynamoDB, Memcached                                 │  │
│  │   • 특징: 초고속 읽기/쓰기, 단순 구조                                 │  │
│  │   • 적합한 경우:                                                      │  │
│  │     - 세션 저장                                                       │  │
│  │     - 캐시                                                           │  │
│  │     - 카운터/래더보드                                                 │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   4. 그래프 모델 (Graph)                                                   │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 대표: Neo4j, Amazon Neptune                                      │  │
│  │   • 특징: 노드/엣지, 관계 탐색, 패턴 매칭                            │  │
│  │   • 적합한 경우:                                                      │  │
│  │     - 소셜 네트워크 (친구 관계)                                       │  │
│  │     - 추천 시스템 (연관 상품)                                         │  │
│  │     - 사기 탐지 (이상 패턴)                                           │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   5. 칼럼 패밀리 (Column Family)                                           │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 대표: Cassandra, ScyllaDB, HBase                                  │  │
│  │   • 특징: 대규모 쓰기, 범위 쿼리, 무한 확장                           │  │
│  │   • 적합한 경우:                                                      │  │
│  │     - 시계열 데이터 (IoT 센서)                                        │  │
│  │     - 로그 수집                                                       │  │
│  │     - 실시간 분석                                                     │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   6. 검색 엔진 (Search Engine)                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 대표: Elasticsearch, Solr                                         │  │
│  │   • 특징: 전문 텍스트, 복합 쿼리, 집계                               │  │
│  │   • 적합한 경우:                                                      │  │
│  │     - 상품 검색                                                       │  │
│  │     - 로그 분석                                                       │  │
│  │     - 모니터링 대시보드                                               │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 서비스별 데이터베이스 선택

### 1. 사용자 서비스 (RDBMS)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    사용자 서비스: PostgreSQL                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   선택 이유:                                                                │
│   • ACID 트랜잭션 보장 (회원가입, 탈퇴, 정보 수정)                         │
│   • 복잡한 관계 (FK 제약조건 필요)                                         │
│   • 데이터 정합성 (중복 가입 방지, 고유 이메일)                            │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │  │
│  │   CREATE TABLE users (                                              │  │
│  │       id SERIAL PRIMARY KEY,                                        │  │
│  │       email VARCHAR(255) UNIQUE NOT NULL,                            │  │
│  │       password_hash VARCHAR(255) NOT NULL,                           │  │
│  │       name VARCHAR(100) NOT NULL,                                    │  │
│  │       phone VARCHAR(20),                                             │  │
│  │       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,                 │  │
│  │       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,                 │  │
│  │       email_verified BOOLEAN DEFAULT FALSE                           │  │
│  │   );                                                                 │  │
│  │                                                                      │  │
│  │   CREATE TABLE user_addresses (                                     │  │
│  │       id SERIAL PRIMARY KEY,                                        │  │
│  │       user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,        │  │
│  │       address_type VARCHAR(20), -- HOME, WORK, OTHER                │  │
│  │       zip_code VARCHAR(10),                                         │  │
│  │       city VARCHAR(100),                                             │  │
│  │       street VARCHAR(255),                                          │  │
│  │       is_default BOOLEAN DEFAULT FALSE                               │  │
│  │   );                                                                 │  │
│  │                                                                      │  │
│  │   -- FK 제약조건으로 데이터 정합성 자동 보장                           │  │
│  │   -- 유니크 제약조건으로 중복 방지                                    │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 상품 카탈로그 서비스 (MongoDB)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    상품 카탈로그 서비스: MongoDB                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   선택 이유:                                                                │
│   • 상품별로 다른 속성 구조 (의류: 사이즈, 전자기기: 사양)                  │
│   • 스키마 변경 빈번 (새 카테고리, 속성 추가)                              │
│   • 중첩 구조 (리뷰, 태그, 옵션)                                          │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │  │
│  │   // 의류 상품 문서                                                   │  │
│  │   {                                                                  │  │
│  │     "_id": ObjectId("..."),                                          │  │
│  │     "sku": "CLOTH-001",                                             │  │
│  │     "name": "코튼 티셔츠",                                            │  │
│  │     "category": "clothing",                                         │  │
│  │     "price": 25000,                                                 │  │
│  │     "attributes": {                                                  │  │
│  │       "material": "cotton",                                          │  │
│  │       "sizes": ["S", "M", "L", "XL"],                                │  │
│  │       "colors": ["black", "white", "navy"],                          │  │
│  │       "season": "spring-summer"                                      │  │
│  │     },                                                                │  │
│  │     "images": [                                                      │  │
│  │       {"url": "https://...", "type": "thumbnail"},                   │  │
│  │       {"url": "https://...", "type": "detail"}                      │  │
│  │     ],                                                                │  │
│  │     "reviews": [                                                     │  │
│  │       {"userId": "user-123", "rating": 5, "comment": "..."},          │  │
│  │       {"userId": "user-456", "rating": 4, "comment": "..."}           │  │
│  │     ],                                                                │  │
│  │     "tags": ["casual", "basic", "round-neck"],                        │  │
│  │     "inventory": {                                                   │  │
│  │       "S": 50, "M": 30, "L": 20, "XL": 10                            │  │
│  │     }                                                                 │  │
│  │   }                                                                  │  │
│  │                                                                      │  │
│  │   // 전자기기 상품 문서 (완전히 다른 구조!)                           │  │
│  │   {                                                                  │  │
│  │     "_id": ObjectId("..."),                                          │  │
│  │     "sku": "ELEC-001",                                              │  │
│  │     "name": "무선 이어폰",                                             │  │
│  │     "category": "electronics",                                       │  │
│  │     "price": 89000,                                                 │  │
│  │     "attributes": {                                                  │  │
│  │       "brand": "Samsung",                                            │  │
│  │       "model": "Galaxy Buds2",                                       │  │
│  │       "specifications": {                                           │  │
│  │         "battery": "60h",                                             │  │
│  │         "connectivity": "Bluetooth 5.2",                              │  │
│  │         "waterResistance": "IPX2",                                   │  │
│  │         "noiseCancellation": true                                    │  │
│  │       }                                                              │  │
│  │     },                                                                │  │
│  │     "warranty": {                                                    │  │
│  │       "period": "12 months",                                         │  │
│  │       "type": "manufacturer"                                          │  │
│  │     }                                                                 │  │
│  │   }                                                                  │  │
│  │                                                                      │  │
│  │   -- 관계형 DB로는 구현 어려운 유연한 구조!                          │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3. 추천 서비스 (Neo4j)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    추천 서비스: Neo4j (그래프 DB)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   선택 이유:                                                                │
│   • 사용자-상품-구매-카테고리 간 복잡한 관계                               │
│   • 관계 기반 쿼리 ("이 상품을 산 사용자들은 무엇을 샀나?")                  │
│   • 패턴 매칭 ("친구의 친구 추천")                                         │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │  │
│  │   // 그래프 모델                                                      │  │
│  │   (User:alice)-[:BOUGHT]->(Product:p1)                               │  │
│  │   (User:alice)-[:BOUGHT]->(Product:p2)                               │  │
│  │   (User:bob)-[:BOUGHT]->(Product:p2)                                 │  │
│  │   (User:bob)-[:BOUGHT]->(Product:p3)                                 │  │
│  │   (Product:p1)-[:IN_CATEGORY]->(Category:electronics)                 │  │
│  │   (Product:p2)-[:IN_CATEGORY]->(Category:electronics)                 │  │
│  │   (Product:p2)-[:ALSO_VIEWED]->(Product:p1)  ← 함께 본 상품 관계      │  │
│  │                                                                      │  │
│  │   // Cypher 쿼리: "이 상품을 산 사용자들이 산 다른 상품 추천"      │  │
│  │   MATCH (u:User {id: $userId})-[:BOUGHT]->(p:Product {id: $productId})│  │
│  │   MATCH (u)-[:BOUGHT]->(other:Product)                               │  │
│  │   WHERE other.id <> $productId                                       │  │
│  │   RETURN other.id, other.name, COUNT(*) AS score                     │  │
│  │   ORDER BY score DESC LIMIT 10                                        │  │
│  │                                                                      │  │
│  │   // "함께 본 상품" 추천                                              │  │
│  │   MATCH (p1:Product {id: $productId})-[:ALSO_VIEWED]->(p2:Product)  │  │
│  │   RETURN p2.id, p2.name                                              │  │
│  │   ORDER BY p2.view_count DESC LIMIT 10                               │  │
│  │                                                                      │  │
│  │   -- 관계형 DB의 JOIN으로는 성능 저하!                                │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4. 세션 서비스 (Redis)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    세션 서비스: Redis (Key-Value)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   선택 이유:                                                                │
│   • 초고속 읽기/쓰기 (서브밀리 응답)                                       │
│   • 단순한 데이터 구조 (세션 ID ↔ 사용자 정보)                              │
│   • TTL 자동 만료                                                         │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │  │
│  │   # 세션 저장                                                         │  │
│  │   HSET session:abc123                                                │  │
│  │     user_id "user-456"                                               │  │
│  │     email "user@example.com"                                        │  │
│  │     name "홍길동"                                                   │  │
│  │     role "customer"                                                 │  │
│  │     created_at "2026-03-18T10:30:00Z"                                │  │
│  │     last_accessed "2026-03-18T10:35:22Z"                             │  │
│  │   EXPIRE session:abc123 1800  # 30분 TTL                             │  │
│  │                                                                      │  │
│  │   # 장바구니 저장 (리스트)                                            │  │
│  │   RPUSH cart:user-456 "item-123:2"  # 상품 ID:수량                    │  │
│  │   RPUSH cart:user-456 "item-456:1"                                   │  │
│  │   EXPIRE cart:user-456 86400  # 24시간                               │  │
│  │                                                                      │  │
│  │   # 조회                                                             │  │
│  │   HGETALL session:abc123                                             │  │
│  │   LRANGE cart:user-456 0 -1                                         │  │
│  │                                                                      │  │
│  │   -- 인메모리라서 0.1ms 응답!                                        │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5. 로그 서비스 (Elasticsearch)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    로그 서비스: Elasticsearch                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   선택 이유:                                                                │
│   • 대규모 쓰기 (초당 수만 건의 로그)                                     │
│   • 전문 텍스트 검색 (에러 메시지, 스택 트레이스)                          │
│   • 집계 및 시각화 (Kibana)                                               │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │  │
│  │   # 로그 문서                                                         │  │
│  │   PUT /logs-app-2026.03.18/_doc/abc123                               │  │
│  │   {                                                                  │  │
│  │     "@timestamp": "2026-03-18T10:30:45.123Z",                        │  │
│  │     "level": "ERROR",                                                │  │
│  │     "service": "order-service",                                      │  │
│  │     "host": "order-pod-5",                                           │  │
│  │     "message": "Payment gateway timeout",                            │  │
│  │     "stack_trace": "java.net.SocketTimeoutException...",              │  │
│  │     "context": {                                                    │  │
│  │       "user_id": "user-789",                                         │  │
│  │       "order_id": "order-456",                                       │  │
│  │       "payment_gateway": "stripe"                                    │  │
│  │     },                                                               │  │
│  │     "tags": ["payment", "timeout", "stripe"]                         │  │
│  │   }                                                                  │  │
│  │                                                                      │  │
│  │   # 검색 쿼리                                                         │  │
│  │   GET /logs-app-*/_search                                            │  │
│  │   {                                                                  │  │
│  │     "query": {                                                       │  │
│  │       "bool": {                                                      │  │
│  │         "must": [                                                    │  │
│  │           {"term": {"level": "ERROR"}},                              │  │
│  │           {"term": {"service": "order-service"}},                     │  │
│  │           {"range": {                                               │  │
│  │             "@timestamp": {                                          │  │
│  │               "gte": "now-1h"                                         │  │
│  │             }                                                        │  │
│  │           }}                                                         │  │
│  │         ],                                                           │  │
│  │         "should": [                                                  │  │
│  │           {"match": {"message": "timeout"}},                         │  │
│  │           {"match": {"message": "connection"}}                        │  │
│  │         ]                                                           │  │
│  │       }                                                             │  │
│  │     },                                                              │  │
│  │     "aggs": {                                                       │  │
│  │       "by_service": {                                               │  │
│  │         "terms": {"field": "service.keyword"}                         │  │
│  │       },                                                            │  │
│  │       "error_count": {                                              │  │
│  │         "value_count": {"field": "level"}                            │  │
│  │       }                                                             │  │
│  │     }                                                               │  │
│  │   }                                                                  │  │
│  │                                                                      │  │
│  │   -- 텍스트 검색 + 집계를 동시에!                                      │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 데이터베이스 선택 가이드

### 1. 의사결정 트리

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    데이터베이스 선택 가이드                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                              시작                                           │
│                                │                                             │
│                                ▼                                             │
│                    ┌───────────────────────┐                                │
│                    │ ACID 트랜잭션 필요? │                                │
│                    └───────────┬───────────┘                                │
│                                │                                             │
│              ┌─────────────────┴─────────────────┐                          │
│              YES                                   NO                         │
│              │                                     │                         │
│              ▼                                     ▼                         │
│    ┌────────────────────┐              ┌────────────────────┐             │
│    │ 관계형 DB (RDBMS)  │              │ 복잡한 관계?      │             │
│    │ • PostgreSQL       │              └─────────┬───────────┘             │
│    │ • MySQL            │                          │                       │
│    └────────────────────┘         ┌─────────────────┴─────────────────┐    │
│                                  │                                     │    │
│                         YES                                     NO           │    │
│                                  │                                     │    │
│                                  ▼                                     ▼    │
│                    ┌────────────────────┐              ┌────────────────────┐│
│                    │ 그래프 DB          │              │ 단순 키-값?      ││
│                    │ • Neo4j            │              └─────────┬───────────┘│
│                    │ • Amazon Neptune   │                        │         │
│                    └────────────────────┘         ┌─────────────────┴─────┐│
│                                                 YES                       NO │
│                                                  │                          ││
│                                                  ▼                          ▼│
│                                    ┌────────────────────┐    ┌────────────────────┐│
│                                    │ Key-Value Store   │    │ 스키마 유연성?    ││
│                                    │ • Redis           │    │                  ││
│                                    │ • DynamoDB        │    └─────────┬───────────┘│
│                                    └────────────────────┘              │             │
│                                                          ┌─────────────────┴─────┐│
│                                                      YES                       NO │
│                                                       │                          ││
│                                                       ▼                          ▼│
│                                          ┌────────────────────┐    ┌────────────────────┐│
│                                          │ 문서 DB           │    │ 대규모 쓰기?     ││
│                                          │ • MongoDB         │    └─────────┬───────────┘│
│                                          │ • Couchbase       │              │             │
│                                          └────────────────────┘    ┌─────────────────┴─────┐│
│                                                                   YES           │             NO│
│                                                                    │            ││
│                                                                    ▼            ▼│
│                                                      ┌────────────────────┐  ┌────────────────────┐│
│                                                      │ Column Family DB  │  │ Search Engine     ││
│                                                      │ • Cassandra       │  │ • Elasticsearch  ││
│                                                      │ • ScyllaDB        │  │ • Solr           ││
│                                                      └────────────────────┘  └────────────────────┘│
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 선택 매트릭스

| 데이터베이스 | 확장성 | 일관성 | 유연성 | 쿼리 복잡도 | 운영 난이도 | 비용 |
|:-----------|:------:|:------:|:------:|:----------:|:----------:|:----:|
| **PostgreSQL** | 수직 ★★★ | 강함 ACID | 낮음 | 높음 (SQL) | 낮음 | 중간 |
| **MongoDB** | 수평 ★★★★ | 최종적 | 높음 | 중간 | 중간 | 중간 |
| **Redis** | 수평 ★★★★★ | 최종적 | 낮음 | 낮음 | 낮음 | 낮음 |
| **Neo4j** | 수직 ★★ | 강함 ACID | 높음 | 매우 높음 (Cypher) | 높음 | 높음 |
| **Cassandra** | 수평 ★★★★★ | 최종적 (Tunable) | 중간 | 낮음 | 높음 | 중간 |
| **Elasticsearch** | 수평 ★★★★ | 최종적 | 높음 | 높음 (DSL) | 높음 | 높음 |

---

## Ⅳ. 실전 구현 패턴

### 1. 데이터베이스 추상화 계층

```java
// Repository 인터페이스 (DB 기술 독립적)

public interface UserRepository {
    User save(User user);
    Optional<User> findById(String id);
    Optional<User> findByEmail(String email);
    List<User> findAll();
    void deleteById(String id);
}

// PostgreSQL 구현
@Repository
@Profile("postgres")
public class PostgresUserRepository implements UserRepository {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Override
    public User save(User user) {
        String sql = """
            INSERT INTO users (email, password_hash, name, phone)
            VALUES (?, ?, ?, ?)
            RETURNING id, created_at
            """;
        return jdbcTemplate.queryForObject(sql,
            (rs, rowNum) -> mapRowToUser(rs),
            user.getEmail(), user.getPasswordHash(),
            user.getName(), user.getPhone()
        );
    }

    @Override
    public Optional<User> findById(String id) {
        String sql = "SELECT * FROM users WHERE id = ?";
        return jdbcTemplate.query(sql, this::mapRowToUser, id)
            .stream().findFirst();
    }

    // ... 다른 메서드 구현
}

// MongoDB 구현 (폴백/대안)
@Repository
@Profile("mongodb")
public class MongoUserRepository implements UserRepository {

    @Autowired
    private MongoTemplate mongoTemplate;

    @Override
    public User save(User user) {
        return mongoTemplate.save(user, "users");
    }

    @Override
    public Optional<User> findById(String id) {
        return Optional.ofNullable(
            mongoTemplate.findById(id, User.class, "users")
        );
    }

    // ... 다른 메서드 구현
}

// 서비스는 구현에 무관
@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;  // 구현 교체 가능!

    public User createUser(UserCreateRequest request) {
        User user = User.builder()
            .email(request.getEmail())
            .passwordHash(passwordEncoder.encode(request.getPassword()))
            .name(request.getName())
            .build();

        return userRepository.save(user);
    }
}
```

### 2. 다중 데이터베이스 전략

```java
// 여러 DB를 동시에 활용하는 서비스

@Service
public class ProductService {

    // PostgreSQL: 트랜잭션, 재고 관리
    @Autowired
    private ProductInventoryRepository inventoryRepository;

    // MongoDB: 상품 카탈로그 (유연한 스키마)
    @Autowired
    private ProductCatalogRepository catalogRepository;

    // Elasticsearch: 전문 검색
    @Autowired
    private ProductSearchRepository searchRepository;

    // Redis: 캐시
    @Autowired
    private ProductCacheRepository cacheRepository;

    @Transactional
    public Product createProduct(ProductCreateRequest request) {
        // 1. PostgreSQL에 상품 기본 정보 저장
        ProductInventory inventory = ProductInventory.builder()
            .sku(request.getSku())
            .stockQuantity(request.getInitialStock())
            .build();
        inventory = inventoryRepository.save(inventory);

        // 2. MongoDB에 상품 상세 정보 저장
        ProductCatalog catalog = ProductCatalog.builder()
            .sku(request.getSku())
            .name(request.getName())
            .description(request.getDescription())
            .attributes(request.getAttributes())  // 유연한 구조
            .images(request.getImages())
            .build();
        catalogRepository.save(catalog);

        // 3. Elasticsearch에 색인
        searchRepository.index(ProductSearchDocument.builder()
            .sku(request.getSku())
            .name(request.getName())
            .description(request.getDescription())
            .build()
        );

        // 4. Redis 캐시
        cacheRepository.set(request.getSku(), catalog, Duration.ofHours(1));

        return Product.builder()
            .sku(request.getSku())
            .name(request.getName())
            .build();
    }

    @Transactional(readOnly = true)
    public Product getProduct(String sku) {
        // 1. Redis 캐시 확인
        Product cached = cacheRepository.get(sku);
        if (cached != null) {
            return cached;
        }

        // 2. MongoDB에서 상세 정보 조회
        ProductCatalog catalog = catalogRepository.findBySku(sku)
            .orElseThrow(() -> new ProductNotFoundException(sku));

        // 3. PostgreSQL에서 재고 정보 조회
        ProductInventory inventory = inventoryRepository.findBySku(sku)
            .orElseThrow(() -> new ProductNotFoundException(sku));

        // 4. 통합 반환
        Product product = Product.builder()
            .sku(sku)
            .name(catalog.getName())
            .description(catalog.getDescription())
            .attributes(catalog.getAttributes())
            .stockQuantity(inventory.getStockQuantity())
            .build();

        // 캐시 업데이트
        cacheRepository.set(sku, product, Duration.ofMinutes(10));

        return product;
    }

    public List<Product> searchProducts(String query) {
        // Elasticsearch로 전문 검색
        return searchRepository.search(query).stream()
            .map(doc -> Product.builder()
                .sku(doc.getSku())
                .name(doc.getName())
                .build())
            .collect(Collectors.toList());
    }
}
```

### 3. 데이터베이스별 설정 분리

```yaml
# application-postgres.yml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/userdb
    username: ${DB_USER}
    password: ${DB_PASSWORD}
    driver-class-name: org.postgresql.Driver
  jpa:
    database-platform: org.hibernate.dialect.PostgreSQLDialect
    hibernate:
      ddl-auto: validate

# application-mongodb.yml
spring:
  data:
    mongodb:
      uri: mongodb://${MONGO_USER}:${MONGO_PASSWORD}@localhost:27017/catalogdb
      auto-index-creation: true

# application-redis.yml
spring:
  redis:
    host: localhost
    port: 6379
    password: ${REDIS_PASSWORD}
    timeout: 2000ms
    lettuce:
      pool:
        max-active: 20
        max-idle: 10
        min-idle: 5
```

---

## Ⅴ. 폴리글랏 퍼시스턴스 고려사항

### 1. 장점

| 장점 | 설명 | 예시 |
|:-----|:-----|:-----|
| **최적의 성능** | 각 데이터 모델에 최적화된 엔진 | 그래프 DB로 추천 쿼리 최적화 |
| **수평적 확장** | NoSQL의 자동 샤딩으로 무한 확장 | Cassandra로 대규모 로그 수집 |
| **유연성** | 스키마 변경 없는 데이터 모델링 | MongoDB로 상품 속성 자유 추가 |
| **비용 절감** | 상용 DB 라이선스 비용 감소 | 오픈 소스 DB 혼합 사용 |
| **기술적 자유** | 벤더 락인 회피 | PostgreSQL + MongoDB + Redis |

### 2. 단점 및 리스크

| 단점 | 설명 | 완화 방안 |
|:-----|:-----|:---------|
| **운영 복잡도** | 여러 DB를 관리해야 함 | Docker Compose, K8s Operator |
| **데이터 동기화** | 여러 DB 간 일관성 유지 어려움 | 이벤트 소싱, CQRS |
| **스킬 요구** | 각 DB 전문가 필요 | 교육, 외부 전문가 활용 |
| **테스트 복잡** | 통합 테스트 환경 구축 어려움 | Testcontainers, 도커 기반 테스트 |
| **모니터링** | 각 DB별 모니터링 도구 필요 | 통합 모니터링 (Prometheus) |

### 3. 데이터 일관성 전략

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              폴리글랏 환경의 데이터 일관성 전략                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   문제: 사용자 DB(PostgreSQL), 주문 DB(PostgreSQL), 재고 DB(NoSQL) 간    │
│         일관성을 어떻게 보장할까?                                           │
│                                                                             │
│   해결 1: 분산 트랜잭션 (Saga Pattern) - #175 참고                        │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   1. 사용자 서비스: 주문 생성 → Local TX                             │  │
│  │   2. 주문 서비스: 주문 저장 → Local TX                               │  │
│  │   3. 재고 서비스: 재고 차감 → Local TX                               │  │
│  │   4. 실패 시 보상 트랜잭션(Compensating Transaction) 실행             │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   해결 2: 이벤트 소싱 (Event Sourcing) - #180 참고                       │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 모든 상태 변경을 이벤트 스트림에 저장                           │  │
│  │   • 각 서비스가 이벤트를 구독하여 자신의 DB 업데이트                 │  │
│  │   • Kafka의 정확히 한 번 전달 보장                                   │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   해결 3: CQRS (Command Query Responsibility Segregation) - #179 참고    │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 쓰기(명령): DB per Service + Saga                              │  │
│  │   • 읽기(쿼리): 통합 뷰(Read Model) + Event Sourcing               │  │
│  │   • 결과적 일관성(Eventual Consistency) 수용                         │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 개념 맵

```
                    ┌────────────────────────┐
                    │ Polyglot Persistence    │
                    └──────────┬─────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  데이터 모델  │      │ 서비스별     │      │  통합 전략   │
│  분류        │      │  선택        │      │              │
├──────────────┤      ├──────────────┤      ├──────────────┤
│ • 관계형     │      │ 사용자: RDBMS│      │ • Saga 패턴  │
│ • 문서형     │      │ 상품: MongoDB│      │ • Event       │
│ • 키-값     │      │ 추천: Neo4j │      │   Sourcing    │
│ • 그래프     │      │ 세션: Redis  │      │ • CQRS        │
│ • Column Fam │      │ 로그: ES     │      │ • API 통신만  │
└──────────────┘      └──────────────┘      └──────────────┘
```

---

## 🎓 섹션 요약 비유 (어린이 설명)

### 🧰 도구 상자 비유

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   🏠 집을 지을 때, 어떤 도구가 필요할까요?                                   │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│   ❌ 나쁜 방법 (망치 하나로 모든 것 해결?)                                 │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│         도구 상자에 망치 하나만 있어! 🔨                                    │
│                                                                             │
│         목수: "나무 자르러 왔어!" ──▶ 망치로 때려서 자름 😅               │
│         배관공: "파이프 잠그렸어!" ──▶ 망치로 두들겨서 뚫어 😅               │
│         전기공: "전선 연결할게!" ──▶ 망치로 전선을... 위험! 🚨              │
│                                                                             │
│         문제:                                                              │
│         • 일은 되지만 느리고 힘들어                                        │
│         • 제대로 된 것도 없어                                              │
│         • 망치로 못 하는 일이 너무 많아                                    │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│   ✅ 좋은 방법 (각 일에 맞는 도구 사용!)                                    │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│         도구 상자에 다양한 도구를 준비! 🧰                                  │
│                                                                             │
│         ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│         │   톱니       │  │   스패너     │  │   펜치       │              │
│         │   🪚          │  │   🔧          │  │   ⚒️          │              │
│         └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                             │
│         목수: "톱니로 딱 딱!" ✅                                           │
│         배관공: "스파너로 확 풀었어!" ✅                                   │
│         전기공: "펜치로 정확하게!" ✅                                      │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│   이게 바로 폴리글랏 퍼시스턴스예요!                                       │
│                                                                             │
│   • 톱니 = 관계형 DB (정확하게 잘라야 할 때, 트랜잭션)                      │
│   • 스패너 = 문서 DB (유연하게 조립할 때, 스키마 자유)                       │
│   • 펜치 = 그래프 DB (복잡한 관계를 연결할 때)                             │
│   • 드라이버 = Key-Value DB (빨리빨리, 단순한 것)                          │
│   • 검사기 = 검색엔진 (무엇인지 찾을 때)                                    │
│                                                                             │
│   "각 일에 맞는 도구를 쓰면 훨씬 효율적이에요!"                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**핵심**: 폴리글랏 퍼시스턴스는 **"각 일에 맞는 도구를 사용하는 것"**과 같아요! 목수에게는 톱니를, 전기공에게는 펜치를 주듯이, 사용자 데이터에는 관계형 DB를, 상품 카탈로그에는 문서 DB를, 추천에는 그래프 DB를 사용하면, 각각의 특성에 맞게 최적의 성능을 낼 수 있어요!

---

## 관련 키워드

- **마이크로서비스 아키텍처 (MSA)** (#163): 폴리글랏 퍼시스턴스가 가능한 기반
- **Database per Service** (#191): 각 서비스가 독립 DB를 가지는 패턴
- **분산 트랜잭션** (#174): 폴리글랏 환경의 트랜잭션 문제
- **사가 패턴** (#175): 데이터 일관성 해결 전략
- **CQRS** (#179): 다중 DB 조회 최적화 패턴
- **NoSQL 데이터베이스**: 폴리글랏 퍼시스턴스의 핵심 기술
