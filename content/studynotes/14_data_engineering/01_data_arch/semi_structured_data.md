+++
title = "반정형 데이터 (Semi-structured Data)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 반정형 데이터 (Semi-structured Data)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 반정형 데이터는 고정된 스키마 없이 데이터 자체에 구조 정보(태그, 마커)를 포함하고 있는 형태로, JSON, XML, YAML, Parquet 등이 대표적이며 웹 API, 로그, IoT 센서 데이터에서 주로 생성됩니다.
> 2. **가치**: 정형 데이터의 엄격함과 비정형 데이터의 자유로움 사이에서 유연성을 제공하며, 스키마 온 리드(Schema-on-Read) 방식으로 데이터 레이크와 데이터 레이크하우스의 핵심 저장 형식입니다.
> 3. **융합**: NoSQL 도큐먼트 저장소(MongoDB), 분산 메시지 큐(Kafka), 컬럼형 스토리지(Parquet) 등 현대 데이터 스택의 대부분이 반정형 데이터를 기반으로 하며, AI/ML 파이프라인의 입력 데이터로 가장 널리 활용됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**반정형 데이터(Semi-structured Data)**는 관계형 데이터베이스의 엄격한 테이블 스키마를 따르지 않으면서도, 데이터 내부에 구조를 설명하는 메타데이터(태그, 마커, 헤더)를 포함하는 데이터 형식입니다. 각 레코드가 서로 다른 필드를 가질 수 있고, 필드의 데이터 타입이 동적으로 변할 수 있는 유연성을 제공합니다.

**반정형 데이터의 핵심 특성**:
- **자기 기술성 (Self-describing)**: 데이터와 구조 정보가 함께 존재
- **유연한 스키마 (Flexible Schema)**: 필드 추가/삭제가 자유로움
- **계층적 구조 (Hierarchical)**: 중첩된 객체와 배열 표현 가능
- **이기종 데이터 (Heterogeneous)**: 동일 컬렉션 내 다른 구조의 레코드 공존

**대표적 반정형 데이터 형식**:
- **JSON (JavaScript Object Notation)**: 웹 API, 설정 파일, NoSQL 저장소
- **XML (eXtensible Markup Language)**: 엔터프라이즈 데이터 교환, SOAP
- **YAML (YAML Ain't Markup Language)**: 설정 파일, DevOps 매니페스트
- **Parquet/ORC**: 컬럼형 반정형 스토리지 (빅데이터 분석)
- **Avro/Protocol Buffers**: 직렬화 포맷 (데이터 직렬화, RPC)

#### 2. 💡 비유를 통한 이해
반정형 데이터를 **'장바구니 영수증'**이나 **'명함'**에 비유할 수 있습니다.
- **정형 데이터**: 모든 명함이 똑같은 템플릿(이름, 회사, 전화번호, 이메일)에 딱 맞아야 합니다. 팩스 번호가 없는 사람도 빈 칸으로 남겨야 합니다.
- **반정형 데이터**: 각 명함이 자유로운 형식을 가집니다. 어떤 명함은 SNS 계정이 있고, 어떤 명함은 없습니다. 어떤 명함은 QR코드가 있고, 어떤 명함은 회사 로고가 있습니다. 명함마다 필요한 정보만 담을 수 있습니다.
- **JSON 예시**:
```json
{
  "이름": "홍길동",
  "회사": "ABC 주식회사",
  "연락처": ["010-1234-5678", "02-9876-5432"],
  "소셜미디어": {
    "링크드인": "linkedin.com/in/hong",
    "깃허브": "github.com/hong"
  }
}
```
이 명함에는 '소셜미디어' 정보가 있지만, 다른 사람의 명함에는 없을 수도 있습니다.

#### 3. 등장 배경 및 발전 과정
1. **웹 2.0과 API 경제 (2000s)**: 웹 서비스 간 데이터 교환이 폭증하면서 XML이 표준으로 자리 잡았습니다. SOAP(Simple Object Access Protocol)가 엔터프라이즈 통합에 사용되었습니다.
2. **JSON의 부상 (2001~)**: 더글라스 크록포드가 JavaScript 객체 표기법을 기반으로 JSON을 표준화했습니다. XML보다 가볍고 JavaScript와 호환성이 높아 RESTful API의 사실상 표준이 되었습니다.
3. **NoSQL의 등장 (2009~)**: MongoDB, CouchDB 등 도큐먼트 데이터베이스가 반정형 데이터를 네이티브로 저장하고 쿼리하는 기능을 제공했습니다.
4. **빅데이터와 스트리밍 (2010s~)**: Kafka가 JSON/Avro 메시지를 스트리밍하고, Spark가 Parquet 파일을 분석하는 현대 데이터 스택의 핵심이 되었습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 반정형 데이터 포맷별 구조 비교 (표)

| 포맷 | 구조 특징 | 직렬화 방식 | 압축 지원 | 스키마 진화 | 주요 활용 |
|:---|:---|:---|:---|:---|:---|
| **JSON** | 키-값 쌍, 중첩 객체/배열 | 텍스트 (UTF-8) | Gzip 등 외부 | 동적 (스키마 없음) | Web API, 설정 |
| **XML** | 태그 기반 트리 구조 | 텍스트 | Gzip 등 외부 | XSD/DTD 선택 | 엔터프라이즈, SOAP |
| **YAML** | 들여쓰기 기반 계층 | 텍스트 | 없음 | 동적 | 설정, CI/CD |
| **Parquet** | 컬럼형, 로우 그룹 | 바이너리 | Snappy, Zstd | 스키마 메타데이터 | 빅데이터 분석 |
| **Avro** | 스키마 기반 바이너리 | 바이너리 | Deflate, Snappy | 전방/후방 호환 | Kafka, Hadoop |
| **Protobuf** | .proto 스키마 정의 | 바이너리 | Varint 내장 | 번호 기반 호환 | gRPC, 직렬화 |

#### 2. JSON 데이터 모델링 아키텍처 (ASCII 다이어그램)

```text
<<< JSON Semi-structured Data Model >>>

┌─────────────────────────────────────────────────────────────────────────┐
│  JSON Document Example (e-commerce Order)                               │
├─────────────────────────────────────────────────────────────────────────┤
│  {                                                                      │
│    "order_id": "ORD-2024-001",          ← String (Primitive)           │
│    "customer": {                         ← Nested Object                │
│      "id": 5001,                                                        │
│      "name": "홍길동",                                                  │
│      "tier": "GOLD"                                                     │
│    },                                                                   │
│    "items": [                            ← Array of Objects             │
│      {                                                                  │
│        "product_id": "P001",                                            │
│        "name": "무선 키보드",                                           │
│        "quantity": 2,                                                   │
│        "price": 59000,                                                  │
│        "options": { "color": "black", "layout": "ansi" }                │
│      },                                                                 │
│      {                                                                  │
│        "product_id": "P002",                                            │
│        "name": "마우스 패드",                                           │
│        "quantity": 1,                                                   │
│        "price": 15000,                                                  │
│        "options": null                   ← Null Value (Flexible)        │
│      }                                                                  │
│    ],                                                                   │
│    "metadata": {                         ← Dynamic Schema               │
│      "source": "mobile_app",                                            │
│      "campaign": "spring_sale_2024",     ← Optional Field               │
│      "ab_test_group": "B"                ← New Field Added Later        │
│    },                                                                   │
│    "created_at": "2024-03-04T10:30:00Z"                                 │
│  }                                                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
┌─────────────────────────────────────────────────────────────────────────┐
│                    Schema-on-Read Processing                             │
│                                                                         │
│  1. Storage: Raw JSON stored as-is (Schemaless Write)                   │
│  2. Query Time: Schema inferred or applied dynamically                  │
│  3. Parser: JSON → Tree Structure → DataFrame/Relation                  │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Spark DataFrame Schema Inference:                               │   │
│  │  root                                                            │   │
│  │   |-- order_id: string (nullable = true)                         │   │
│  │   |-- customer: struct (nullable = true)                         │   │
│  │   |    |-- id: long (nullable = true)                            │   │
│  │   |    |-- name: string (nullable = true)                        │   │
│  │   |    |-- tier: string (nullable = true)                        │   │
│  │   |-- items: array (nullable = true)                             │   │
│  │   |    |-- element: struct                                       │   │
│  │   |    |    |-- product_id: string                               │   │
│  │   |    |    |-- quantity: long                                   │   │
│  │   |    |    |-- price: long                                      │   │
│  │   |    |    |-- options: struct                                  │   │
│  │   |-- metadata: map<string, string> (nullable = true)            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 3. 심층 동작 원리: JSON 파싱과 쿼리 처리

**JSON 파싱 과정**:
```python
"""
JSON 파싱 및 쿼리 처리 메커니즘 (Python 예시)
"""
import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

# 1. 토크나이저 (Tokenizer): JSON 문자열 → 토큰 스트림
@dataclass
class Token:
    type: str      # STRING, NUMBER, BOOLEAN, NULL, LBRACE, RBRACE, LBRACKET, COLON, COMMA
    value: Any

def tokenize(json_str: str) -> List[Token]:
    """JSON 문자열을 토큰으로 분해"""
    tokens = []
    i = 0
    while i < len(json_str):
        ch = json_str[i]
        if ch.isspace():
            i += 1
        elif ch == '{':
            tokens.append(Token('LBRACE', '{'))
            i += 1
        elif ch == '}':
            tokens.append(Token('RBRACE', '}'))
            i += 1
        elif ch == '[':
            tokens.append(Token('LBRACKET', '['))
            i += 1
        elif ch == ']':
            tokens.append(Token('RBRACKET', ']'))
            i += 1
        elif ch == '"':
            # 문자열 파싱
            j = i + 1
            while json_str[j] != '"':
                if json_str[j] == '\\':
                    j += 2
                else:
                    j += 1
            tokens.append(Token('STRING', json_str[i+1:j]))
            i = j + 1
        elif ch.isdigit() or ch == '-':
            # 숫자 파싱
            j = i
            while j < len(json_str) and json_str[j] in '0123456789.-eE+':
                j += 1
            value = float(json_str[i:j]) if '.' in json_str[i:j] else int(json_str[i:j])
            tokens.append(Token('NUMBER', value))
            i = j
        # ... 기타 토큰 처리
    return tokens

# 2. 파서 (Parser): 토큰 스트림 → AST (Abstract Syntax Tree) / Python Dict
def parse_json(json_str: str) -> Dict[str, Any]:
    """재귀 하강 파싱 (Recursive Descent Parsing)"""
    data = json.loads(json_str)
    return data

# 3. 쿼리 엔진: JSONPath / SQL-on-JSON 처리
def jsonpath_query(data: Dict, path: str) -> Any:
    """
    JSONPath 쿼리 예시
    $ = 루트
    .field = 필드 접근
    [n] = 배열 인덱스
    [*] = 와일드카드
    """
    import jsonpath_ng
    from jsonpath_ng import parse

    jsonpath_expr = parse(path)
    matches = [match.value for match in jsonpath_expr.find(data)]
    return matches[0] if len(matches) == 1 else matches

# 사용 예시
order_json = '''
{
  "order_id": "ORD-2024-001",
  "items": [
    {"product_id": "P001", "price": 59000},
    {"product_id": "P002", "price": 15000}
  ]
}
'''

order = parse_json(order_json)

# JSONPath로 모든 상품 가격 합계 계산
prices = jsonpath_query(order, '$.items[*].price')
total = sum(prices)  # 74000
```

**Spark에서의 JSON 처리 (Schema-on-Read)**:
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, get_json_object

spark = SparkSession.builder.appName("SemiStructuredDemo").getOrCreate()

# 1. 스키마 추론 없이 로드 (모든 컬럼이 string)
df_raw = spark.read.json("s3://data-lake/orders/", primitiveAsString=True)

# 2. 명시적 스키마 적용 (Schema-on-Read)
from pyspark.sql.types import StructType, StructField, StringType, LongType, ArrayType

schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("customer", StructType([
        StructField("id", LongType(), True),
        StructField("name", StringType(), True)
    ]), True),
    StructField("items", ArrayType(StructType([
        StructField("product_id", StringType(), True),
        StructField("quantity", LongType(), True),
        StructField("price", LongType(), True)
    ])), True)
])

df = spark.read.schema(schema).json("s3://data-lake/orders/")

# 3. 중첩 구조 Flatten (반정형 → 정형 변환)
df_flat = df.select(
    col("order_id"),
    col("customer.id").alias("customer_id"),
    col("customer.name").alias("customer_name"),
    explode("items").alias("item")
).select(
    col("order_id"),
    col("customer_id"),
    col("item.product_id"),
    col("item.quantity"),
    col("item.price")
)

# 4. SQL 쿼리
df_flat.createOrReplaceTempView("orders")
spark.sql("""
    SELECT customer_id, SUM(quantity * price) as total_amount
    FROM orders
    GROUP BY customer_id
    ORDER BY total_amount DESC
""").show()
```

#### 4. Parquet 컬럼형 반정형 스토리지 구조

```text
<<< Parquet File Internal Structure >>>

┌─────────────────────────────────────────────────────────────────────────┐
│  Parquet File: orders.parquet (Row Group: 128MB)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Row Group 1 (128MB, ~1M rows)                                    │   │
│  │                                                                   │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │   │
│  │  │ Column Chunk │  │ Column Chunk │  │ Column Chunk │           │   │
│  │  │ order_id     │  │ customer.id  │  │ items.price  │           │   │
│  │  │ (STRING)     │  │ (INT64)      │  │ (LIST<INT>)  │           │   │
│  │  │              │  │              │  │              │           │   │
│  │  │ Repetition   │  │ Definition   │  │ Repetition   │           │   │
│  │  │ Levels: 0    │  │ Levels: 0-2  │  │ Levels: 0-2  │           │   │
│  │  │ Definition   │  │ Min: 1001    │  │ Max: 99000   │           │   │
│  │  │ Levels: 0-1  │  │ Max: 9999    │  │ Null Count:0 │           │   │
│  │  │ Compression: │  │ Compression: │  │ Compression: │           │   │
│  │  │   SNAPPY     │  │   ZSTD       │  │   SNAPPY     │           │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘           │   │
│  │                                                                   │   │
│  │  ┌──────────────────────────────────────────────────────────┐    │   │
│  │  │ Page (8KB, 압축 단위)                                     │    │   │
│  │  │  - 데이터 페이지: 실제 값 (RLE, Dictionary 인코딩)         │    │   │
│  │  │  - 딕셔너리 페이지: 고유값 사전                            │    │   │
│  │  │  - 오프셋 인덱스: 페이지 내 레코드 위치                    │    │   │
│  │  └──────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Footer (메타데이터)                                              │   │
│  │  - Schema: 중첩 구조 정의                                         │   │
│  │  - Row Group 정보: 오프셋, 크기, 통계                             │   │
│  │  - Column Chunk 메타데이터: Min/Max/Null Count (스킵 활용)        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  [핵심 최적화 기법]                                                      │
│  1. Column Pruning: 필요한 컬럼만 읽기                                   │
│  2. Predicate Pushdown: Min/Max 통계로 페이지 스킵                       │
│  3. Dictionary Encoding: LOW CARDINALITY → 정수 매핑                    │
│  4. RLE (Run-Length Encoding): 연속된 동일값 압축                       │
│  5. Repetition/Definition Levels: 중첩/선택적 필드 표현                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 반정형 데이터 처리 방식 비교표

| 비교 항목 | RDBMS JSON 컬럼 | MongoDB (도큐먼트 DB) | Spark/Data Lake | Elasticsearch |
|:---|:---|:---|:---|:---|
| **스키마** | 스키마 온 라이트 | 스키마 온 리드 | 스키마 온 리드 | 동적 매핑 |
| **쿼리 언어** | SQL + JSON 함수 | MongoDB Query Language | Spark SQL / DataFrame | Query DSL |
| **인덱싱** | GIN / JSON 인덱스 | BTree, Text, Geospatial | Parquet 통계, Partition | Inverted Index |
| **중첩 쿼리** | jsonb_path_query | 중첩 필드 직접 접근 | explode + flatten | nested 쿼리 |
| **성능** | OLTP 최적화 | 읽기/쓰기 균형 | 대용량 분석 | 전문 검색 특화 |
| **확장성** | 수직 확장 | 수평 샤딩 | 무한 수평 확장 | 샤딩 + 복제 |

#### 2. 과목 융합 관점 분석

**프로그래밍 언어 관점 - 직렬화/역직렬화**:
- **JSON 직렬화**: Python의 `json.dumps()`, JavaScript의 `JSON.stringify()` 등 객체를 문자열로 변환
- **성능 최적화**: ujson, orjson 등 C 기반 고속 JSON 파서는 기본 파서보다 5~10배 빠름
- **스트리밍 파싱**: ijson, Jackson Streaming API 등 대용량 JSON을 메모리에 올리지 않고 스트리밍 파싱

**데이터베이스 관점 - JSON 컬럼 타입**:
```sql
-- PostgreSQL JSONB (바이너리 JSON, 인덱싱 지원)
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50),
    payload JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- GIN 인덱스 생성 (Generalized Inverted Index)
CREATE INDEX idx_payload_gin ON events USING GIN (payload);

-- JSONPath 쿼리 (PostgreSQL 12+)
SELECT * FROM events
WHERE payload @? '$.items[*] ? (@.price > 50000)';

-- JSONB 연산자
SELECT payload->>'order_id' as order_id,
       payload->'customer'->>'name' as customer_name,
       jsonb_array_length(payload->'items') as item_count
FROM events
WHERE event_type = 'order';
```

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 마이크로서비스 API 응답 캐싱**
- **상황**: 여러 마이크로서비스의 API 응답을 캐싱하여 프론트엔드에 빠르게 제공
- **선택**: Redis에 JSON 문자열로 저장, 필요 시 부분 업데이트
- **이유**: Redis의 Hash 타입보다 JSON이 유연하며, 클라이언트에서 바로 사용 가능
```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

# API 응답 캐싱
def cache_user_profile(user_id: int, profile: dict, ttl: int = 3600):
    key = f"user:profile:{user_id}"
    r.setex(key, ttl, json.dumps(profile))

# 캐시 조회
def get_cached_profile(user_id: int) -> dict:
    key = f"user:profile:{user_id}"
    cached = r.get(key)
    return json.loads(cached) if cached else None
```

**시나리오 2: Kafka 메시지 포맷 선정 (JSON vs Avro)**
- **JSON 선택 기준**: 스키마가 자주 변함, 디버깅 용이성 중요, 소규모 팀
- **Avro 선택 기준**: 스키마 진화 관리 필요, 고성능 직렬화, 대규모 데이터 파이프라인

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **스키마 관리 전략**: Schema Registry 사용 여부, 스키마 진화 호환성 정책
- [ ] **압축 및 인코딩**: JSON은 Gzip 압축 필수, Parquet은 Snappy/Zstd 선택
- [ ] **파싱 성능**: 고부하 시스템에서는 바이너리 포맷(Avro, Protobuf) 고려
- [ ] **쿼리 패턴**: 중첩 필드 자주 쿼리 → flatten 여부, 인덱싱 전략

#### 3. 안티패턴 (Anti-patterns)

- **JSON Bomb**: 매우 깊게 중첩된 JSON으로 파서 스택 오버플로우 유발 → 깊이 제한 설정
- **과도한 중첩**: 5단계 이상 중첩은 쿼리 복잡도 급증 → 적절히 flatten
- **무분별한 필드 추가**: 하위 호환성 깨지는 변경 방지

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 구분 | 정형 데이터 | 반정형 데이터 | 개선 효과 |
|:---|:---|:---|:---|
| **개발 속도** | 스키마 변경 시 마이그레이션 | 즉시 필드 추가 가능 | 10배 단축 |
| **데이터 다양성** | 고정 구조만 | 유연한 구조 | 새로운 데이터 수용 |
| **분석 민첩성** | ETL 대기 | 바로 분석 가능 | Time-to-Insight 단축 |

#### 2. 미래 전망
반정형 데이터는 **AI/ML 시대**에 더욱 중요해질 것입니다. LLM의 입력/출력이 JSON 포맷이며, RAG(Retrieval-Augmented Generation) 파이프라인에서 문서 청크가 JSON으로 표현됩니다. 또한 **Schema Evolution** 관리를 위한 Schema Registry(Confluent, AWS Glue)가 표준화되고 있습니다.

#### 3. 참고 표준
- **RFC 8259**: The JSON Data Interchange Format (IETF, 2017)
- **W3C XML 1.0**: Extensible Markup Language
- **Apache Parquet Format**: Columnar storage format specification

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[정형 데이터 (Structured Data)](@/studynotes/14_data_engineering/01_data_arch/structured_data.md)**: 고정 스키마를 가진 전통적 데이터 형식
- **[비정형 데이터 (Unstructured Data)](@/studynotes/14_data_engineering/01_data_arch/unstructured_data.md)**: 스키마가 없는 텍스트, 이미지 등
- **[NoSQL 데이터베이스](@/studynotes/14_data_engineering/01_data_arch/nosql_databases.md)**: 반정형 데이터 저장에 특화된 DB
- **[스키마 온 리드 (Schema-on-Read)](@/studynotes/14_data_engineering/01_data_arch/schema_on_read.md)**: 읽기 시 스키마 적용 방식
- **[아파치 카프카 (Apache Kafka)](@/studynotes/14_data_engineering/03_pipelines/apache_kafka.md)**: 반정형 메시지 스트리밍 플랫폼

---

### 👶 어린이를 위한 3줄 비유 설명
1. **자유로운 일기장**: 반정형 데이터는 일기장에 비유할 수 있어요. 어떤 날은 날씨를 적고, 어떤 날은 기분만 적어도 돼요. 정해진 양식이 없거든요.
2. **꼬리표가 달린 물건**: 각 물건에 '이건 장난감이야', '이건 5000원이야' 같은 꼬리표(태그)가 달려 있어서, 꼬리표만 보면 무엇인지 알 수 있어요.
3. **필요한 것만 적기**: 친구들 명함을 모을 때, 어떤 친구는 전화번호만, 어떤 친구는 인스타그램 아이디만 적어도 돼요. 모두 똑같을 필요가 없답니다!
