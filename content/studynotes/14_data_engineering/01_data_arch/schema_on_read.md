+++
title = "스키마 온 리드 (Schema-on-Read)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 스키마 온 리드 (Schema-on-Read)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스키마 온 리드(Schema-on-Read)는 데이터를 저장할 때 스키마를 적용하지 않고, 데이터를 읽어서 분석할 때 비로소 스키마를 적용하는 데이터 처리 방식입니다.
> 2. **가치**: 데이터 수집 속도를 극대화하고, 원본 데이터를 보존하며, 향후 다양한 분석 요구사항에 유연하게 대응할 수 있어 데이터 레이크와 데이터 레이크하우스의 핵심 철학입니다.
> 3. **융합**: 스키마 온 라이트(Schema-on-Write)와 대비되며, 현대 데이터 아키텍처에서는 두 방식을 혼합하여 수집 단계에서는 온 리드, 분석 단계에서는 온 라이트 특성을 활용합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**스키마 온 리드(Schema-on-Read)**는 데이터를 저장소에 기록할 때는 별도의 스키마 검증 없이 원본 그대로 저장하고, 이후 데이터를 읽어서 쿼리하거나 분석할 때 그 시점에 스키마를 정의하여 적용하는 방식입니다. 이는 전통적인 RDBMS의 스키마 온 라이트(Schema-on-Write)와 대조되는 개념입니다.

**핵심 특성 비교**:
| 특성 | Schema-on-Write | Schema-on-Read |
|:---|:---|:---|
| **스키마 적용 시점** | 쓰기 시점 (저장 전) | 읽기 시점 (쿼리 시) |
| **데이터 저장 형태** | 정형 (변환됨) | 원본 그대로 |
| **유연성** | 낮음 (스키마 변경 어려움) | 높음 (다양한 스키마 적용 가능) |
| **데이터 품질 검증** | 저장 전 검증 | 읽기 시 검증 |
| **적합한 용도** | 트랜잭션, BI 리포팅 | 탐색적 분석, 데이터 과학 |

#### 2. 비유를 통한 이해
- **Schema-on-Write (도서관 분류)**: 책을 도서관에 들이밀 때 먼저 분류번호를 정하고, 카드목록에 등록한 다음에야 책장에 꽂습니다. 분류가 잘못되면 다시 꺼내서 다시 분류해야 합니다.
- **Schema-on-Read (창고 보관)**: 물건을 창고에 들이밀 때는 그냥 아무 데나 둡니다. 나중에 물건을 찾을 때 "이건 전자제품이고, 저건 의류다"라고 분류해서 찾습니다.

#### 3. 등장 배경
데이터 레이크의 등장과 함께 스키마 온 리드가 주목받았습니다. 다양한 소스에서 생성되는 대용량 데이터를 빠르게 수집하고 저장하기 위해, 저장 전 스키마 정의와 변환 작업을 지연시키는 접근이 필요했기 때문입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 처리 흐름 비교

```text
<<< Schema-on-Write vs Schema-on-Read >>>

[Schema-on-Write Flow]
Source Data → Transform & Validate → Apply Schema → Store → Query
                    (지연 발생)          (제약 있음)

[Schema-on-Read Flow]
Source Data → Store (Raw) → Query → Apply Schema at Read Time
                (즉시)       (지연 없음)    (유연함)
```

#### 2. 실제 구현 예시 (Spark)

```python
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

spark = SparkSession.builder.appName("SchemaOnRead").getOrCreate()

# Schema-on-Read: 원본 JSON 저장 (스키마 없음)
raw_data = {"id": 1, "name": "홍길동", "age": 30, "city": "서울"}

# 읽기 시점에 스키마 적용
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

df = spark.read.schema(schema).json("s3://lake/users/")
```

#### 3. 장단점 분석

**장점**:
- 데이터 수집 속도 향상
- 원본 데이터 보존
- 다양한 분석 스키마 적용 가능
- 스키마 진화 용이

**단점**:
- 읽기 시 스키마 적용 오버헤드
- 데이터 품질 문제를 나중에 발견
- 쿼리 성능 저하 가능

---

### Ⅲ. 융합 비교 및 다각도 분석

| 관점 | Schema-on-Write | Schema-on-Read |
|:---|:---|:---|
| **데이터베이스** | RDBMS, DW | Data Lake, NoSQL |
| **품질 관리** | 사전 검증 | 사후 검증 |
| **성능** | 쓰기 느림, 읽기 빠름 | 쓰기 빠름, 읽기 느림 |
| **유연성** | 낮음 | 높음 |

---

### Ⅳ. 실무 적용 및 기술사적 판단

**도입 시 고려사항**:
- 데이터 수집 속도가 중요한가?
- 데이터 스키마가 자주 변하는가?
- 원본 데이터 보존이 필요한가?

**하이브리드 접근**: Bronze Layer(Schema-on-Read) → Silver/Gold Layer(Schema-on-Write)

---

### Ⅴ. 기대효과 및 결론

| 구분 | 효과 |
|:---|:---|
| **수집 속도** | 변환 대기 없이 즉시 저장 |
| **유연성** | 다양한 분석 요구사항 대응 |
| **비용** | 초기 ETL 비용 절감 |

---

### 관련 개념 맵 (Knowledge Graph)
- **[스키마 온 라이트 (Schema-on-Write)](@/studynotes/14_data_engineering/01_data_arch/schema_on_write.md)**
- **[데이터 레이크 (Data Lake)](@/studynotes/14_data_engineering/01_data_arch/data_lake.md)**
- **[데이터 레이크하우스 (Data Lakehouse)](@/studynotes/14_data_engineering/01_data_arch/data_lakehouse.md)**

---

### 어린이를 위한 3줄 비유 설명
1. **나중에 분류하기**: 장난감을 방에 들일 때 그냥 다 넣어두고, 나중에 놀 때 "이건 로봇, 이건 자동차"라고 정해요.
2. **빠르게 정리**: 하나하나 분류하느라 시간 낭비하지 않고, 일단 다 넣어두니까 정리가 빨라요.
3. **여러 가지로 분류 가능**: 로봇을 "색깔별"로도 분류할 수 있고, "크기별"로도 분류할 수 있어요!
