+++
title = "데이터 레이크 (Data Lake)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 데이터 레이크 (Data Lake)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 레이크(Data Lake)는 정형, 반정형, 비정형 데이터를 원시(Raw) 형태 그대로 저장하는 대용량 중앙 저장소로, 스키마 온 리드(Schema-on-Read) 방식을 통해 데이터 수집 시 변환 작업을 지연시킵니다.
> 2. **가치**: "Store First, Process Later" 철학으로 데이터 수집 속도를 극대화하고, 향후 분석 요구사항에 유연하게 대응할 수 있으며, 저렴한 객체 스토리지(S3, ADLS, GCS)를 활용하여 비용 효율적입니다.
> 3. **융합**: 하둡 HDFS에서 시작하여 클라우드 객체 스토리지로 진화하였으며, 현재는 데이터 레이크하우스 아키텍처의 기반이 되어 ACID 트랜잭션과 고성능 분석을 지원합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**데이터 레이크(Data Lake)**는 기업의 모든 데이터를 원본 형태로 중앙 집중 저장하는 시스템입니다. 2010년 James Dixon(Pentaho CTO)이 처음 제안한 개념으로, "정제된 물(데이터 웨어하우스)"이 아닌 "자연 상태의 물(원시 데이터)"을 저장하는 호수(Lake)에 비유되었습니다.

**데이터 레이크의 핵심 특성**:
- **원시 데이터 저장 (Raw Data Storage)**: 변환 없이 원본 그대로 저장
- **스키마 온 리드 (Schema-on-Read)**: 읽기 시점에 스키마 적용
- **다양한 데이터 유형**: 정형, 반정형, 비정형 모두 수용
- **저비용 스토리지**: 객체 스토리지(S3, ADLS, GCS) 활용
- **탄력적 확장**: 무제한에 가까운 스토리지 확장

**데이터 레이크 vs 데이터 웨어하우스**:
| 비교 항목 | Data Lake | Data Warehouse |
|:---|:---|:---|
| **데이터 형태** | Raw (원시) | Processed (가공) |
| **스키마** | Schema-on-Read | Schema-on-Write |
| **데이터 유형** | 모든 유형 | 주로 정형 |
| **저장 비용** | 낮음 | 높음 |
| **주요 사용자** | Data Scientist | Business Analyst |
| **처리 엔진** | Spark, Presto | SQL Engine |

#### 2. 비유를 통한 이해
데이터 레이크를 **'자연 호수'**나 **'창고'**에 비유할 수 있습니다.
- **데이터 웨어하우스**: 정수장에서 정화된 물을 저장하는 '정수조'입니다. 깨끗하고 바로 마실 수 있지만, 정수 과정이 필요해서 시간이 걸립니다.
- **데이터 레이크**: 빗물, 강물, 지하수 등 모든 물을 그대로 받아두는 '자연 호수'입니다. 바로 마실 수는 없지만, 필요할 때만 정수해서 쓰면 됩니다. 물을 버리지 않고 다 모아두는 것입니다.

**데이터 늪(Data Swamp) 경고**: 호수를 관리하지 않으면 쓰레기장이 되듯, 데이터 레이크에 메타데이터 관리, 카탈로그, 거버넌스가 없으면 활용 불가능한 '데이터 늪'이 됩니다.

#### 3. 등장 배경 및 발전 과정
1. **하둡 HDFS 시대 (2006~2015)**: 구글 GFS 논문을 기반으로 한 HDFS가 분산 파일 시스템으로 데이터 레이크 역할을 수행했습니다. 페타바이트급 데이터를 저렴하게 저장할 수 있었습니다.
2. **클라우드 객체 스토리지 등장 (2010s)**: AWS S3(2006), Azure Blob Storage, Google Cloud Storage가 사실상의 데이터 레이크 스토리지가 되었습니다. 무한 확장, 99.999999999% 내구성, 저렴한 비용이 특징입니다.
3. **데이터 레이크의 한계 인식 (2015~)**: 스키마 부재로 인한 데이터 품질 문제, ACID 미지원, 작은 파일 문제(Small File Problem) 등이 지적되었습니다.
4. **데이터 레이크하우스로 진화 (2020~)**: Apache Iceberg, Delta Lake, Apache Hudi 등의 오픈 테이블 포맷이 레이크 위에 트랜잭션 계층을 추가하여 레이크하우스 아키텍처가 등장했습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 데이터 레이크 아키텍처 구성 요소 (표)

| 계층 | 구성 요소 | 핵심 기능 | 기술 스택 |
|:---|:---|:---|:---|
| **Ingestion** | 데이터 수집 | Batch, Streaming, CDC | Kafka, Kinesis, Sqoop |
| **Storage** | 객체 스토리지 | 원시 데이터 저장 | S3, ADLS, GCS, MinIO |
| **Catalog** | 메타데이터 관리 | 스키마, 파티션 정보 | AWS Glue, Hive Metastore |
| **Processing** | 데이터 처리 | ETL, 분석, ML | Spark, Presto, Flink |
| **Governance** | 거버넌스 | 보안, 품질, 리니지 | Apache Ranger, Apache Atlas |
| **Serving** | 데이터 서빙 | 쿼리, API | Athena, Redshift Spectrum |

#### 2. 데이터 레이크 Zones 아키텍처 (ASCII 다이어그램)

```text
<<< Data Lake Zone Architecture (Medallion Architecture) >>>

+--------------------------------------------------------------------------+
|                        Data Lake Zones (S3 Bucket)                        |
+--------------------------------------------------------------------------+

[RAW / Bronze Zone] - 원천 데이터 그대로 저장
+--------------------------------------------------------------------------+
|  s3://data-lake/raw/                                                     |
|  ├── /sales/                                                             |
|  │   ├── /year=2024/month=03/day=04/                                     |
|  │   │   ├── sales_20240304_001.json                                     |
|  │   │   ├── sales_20240304_002.json                                     |
|  │   │   └── ...                                                         |
|  ├── /logs/                                                              |
|  │   ├── /web/                                                           |
|  │   │   └── web_logs_20240304.parquet                                   |
|  └── /external/                                                          |
|      └── market_data_202403.csv                                          |
|                                                                          |
|  특성: 원본 보존, 불변(Immutable), 전체 히스토리 유지                     |
+--------------------------------------------------------------------------+
                                    |
                                    | ETL/ELT Processing
                                    v
[CLEANSED / Silver Zone] - 정제된 데이터
+--------------------------------------------------------------------------+
|  s3://data-lake/cleansed/                                                |
|  ├── /sales/                                                             |
|  │   └── /year=2024/month=03/                                            |
|  │       └── sales_cleaned.parquet                                       |
|  ├── /customers/                                                         |
|  │   └── customers_master.parquet                                        |
|                                                                          |
|  특성: 중복 제거, 타입 변환, 파티셔닝, 기본 정제                           |
+--------------------------------------------------------------------------+
                                    |
                                    | Aggregation, Join
                                    v
[CURATED / Gold Zone] - 분석용 모델
+--------------------------------------------------------------------------+
|  s3://data-lake/curated/                                                 |
|  ├── /analytics/                                                         |
|  │   ├── monthly_sales_summary.parquet                                   |
|  │   └── customer_segmentation.parquet                                   |
|  ├── /ml_features/                                                       |
|  │   └── recommendation_features.parquet                                 |
|  └── /reports/                                                           |
|      └── executive_dashboard_data.parquet                                |
|                                                                          |
|  특성: 비즈니스 준비 완료, Star Schema, 집계 테이블                        |
+--------------------------------------------------------------------------+

[Metadata & Catalog Layer]
+--------------------------------------------------------------------------+
|  AWS Glue Data Catalog / Hive Metastore                                  |
|  - 테이블 정의 (Schema)                                                   |
|  - 파티션 위치 정보                                                       |
|  - 데이터 통계 (RowCount, Size)                                          |
+--------------------------------------------------------------------------+
```

#### 3. 심층 동작 원리: Schema-on-Read 처리

**Schema-on-Read vs Schema-on-Write 비교**:
```python
"""
Schema-on-Read: 데이터 레이크의 핵심 원리
데이터 저장 시 스키마 없이 저장하고, 읽기 시점에 스키마 적용
"""

# 1. Schema-on-Write (전통적 DW 방식)
# 저장 전에 스키마 검증 필요
sql_create = """
CREATE TABLE sales (
    sales_id    BIGINT PRIMARY KEY,
    product_id  VARCHAR(20) NOT NULL,
    quantity    INT CHECK (quantity > 0),
    amount      DECIMAL(10,2),
    sale_date   DATE
);
"""
# 데이터 적재 시 스키마 위반 → 에러 발생

# 2. Schema-on-Read (데이터 레이크 방식)
# 저장은 원본 그대로, 읽기 시 스키마 적용
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType

spark = SparkSession.builder.appName("DataLakeDemo").getOrCreate()

# 원본 JSON 파일 읽기 (스키마 추론)
df_raw = spark.read.json("s3://data-lake/raw/sales/")

# 읽기 시점에 명시적 스키마 적용
schema = StructType([
    StructField("sales_id", LongType(), True),
    StructField("product_id", StringType(), True),
    StructField("quantity", LongType(), True),
    StructField("amount", DoubleType(), True),
    StructField("sale_date", StringType(), True)
])

df_typed = spark.read.schema(schema).json("s3://data-lake/raw/sales/")

# 스키마 검증 및 변환
from pyspark.sql.functions import col, to_date

df_clean = df_typed \
    .filter(col("quantity") > 0) \
    .withColumn("sale_date", to_date(col("sale_date"), "yyyy-MM-dd"))

# Parquet으로 저장 (Silver Zone)
df_clean.write.mode("overwrite") \
    .partitionBy("sale_date") \
    .parquet("s3://data-lake/cleansed/sales/")

# 3. 장단점
"""
Schema-on-Read 장점:
- 데이터 수집 속도 향상 (변환 대기 없음)
- 원본 데이터 보존 (나중에 다시 처리 가능)
- 유연한 스키마 진화 (새 필드 추가 용이)

Schema-on-Read 단점:
- 읽기 시 스키마 적용 오버헤드
- 데이터 품질 문제를 나중에 발견
- 쿼리 성능 저하 가능성
"""
```

#### 4. 파티셔닝과 데이터 스킵 (Data Skipping)

```python
"""
데이터 레이크 성능 최적화: 파티셔닝과 파일 포맷
"""

# 1. 파티셔닝 전략
# 데이터를 디렉터리 구조로 분할하여 불필요한 파일 읽기 방지

# Hive 스타일 파티셔닝
# s3://data-lake/sales/year=2024/month=03/day=04/sales.parquet

df_sales = spark.read.parquet("s3://data-lake/sales/")

# 파티션 프루닝 (Partition Pruning)
# WHERE 절의 파티션 컬럼 조건으로 불필요한 파티션 스킵
df_march = df_sales.filter("year = 2024 AND month = 03")
# → year=2024/month=03/ 디렉터리만 읽음

# 2. Parquet 파일 포맷의 데이터 스킵
# Parquet은 컬럼별 Min/Max 통계를 저장
# 쿼리 조건과 비교하여 불필요한 Row Group 스킵

# 3. Z-Ordering (Databricks Delta Lake)
# 여러 컬럼에 대해 공간 채우기 곡선(Space-filling Curve) 정렬
# WHERE customer_id = 123 AND product_id = 456 같은 복합 조건 효율적 처리

# 4. Compaction (파일 병합)
# 작은 파일이 많으면 메타데이터 오버헤드 증가
# 주기적으로 작은 파일을 큰 파일(128MB~1GB)로 병합

spark.read.parquet("s3://data-lake/sales/year=2024/month=03/") \
    .repartition(10) \
    .write.mode("overwrite") \
    .parquet("s3://data-lake/sales/year=2024/month=03_compacted/")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 데이터 저장소 진화 비교표

| 시대 | 1세대 (DW) | 2세대 (Data Lake) | 3세대 (Lakehouse) |
|:---|:---|:---|:---|
| **스토리지** | 전용 어플라이언스 | HDFS / Object Storage | Object Storage + Table Format |
| **스키마** | Schema-on-Write | Schema-on-Read | Hybrid |
| **ACID** | 지원 | 미지원 | 지원 (Iceberg/Delta) |
| **비용** | 높음 | 낮음 | 낮음 |
| **파이프라인** | ETL | ELT | ELT + Incremental |
| **사용자** | BI 분석가 | 데이터 사이언티스트 | 모든 사용자 |

#### 2. 과목 융합 관점 분석

**운영체제 관점 - 파일 시스템**:
- **HDFS**: 블록 기반 분산 파일 시스템, 128MB 블록, 3-way 복제
- **객체 스토리지(S3)**: 키-값 기반, eventual consistency(일부), 무제한 확장

**데이터베이스 관점 - 카탈로그**:
- **Hive Metastore**: 데이터 레이크의 테이블 메타데이터 관리
- **AWS Glue**: 서버리스 카탈로그 서비스

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 로그 분석 데이터 레이크 구축**
- **요구사항**: 웹/앱 로그 일 10TB, 1년 보관, 실시간 분석
- **아키텍처**:
  - 수집: Kafka → S3 (Firehose)
  - 저장: S3 Raw Zone (JSON)
  - 처리: Glue ETL → Parquet (Silver Zone)
  - 쿼리: Athena (Serverless SQL)

**시나리오 2: 데이터 레이크에서 레이크하우스로 마이그레이션**
- **문제**: ACID 미지원으로 중복 데이터, 잘못된 업데이트 발생
- **해결**: Delta Lake/Iceberg 도입, 기존 Parquet에 메타데이터 계층 추가

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **스토리지 선정**: S3 Standard vs Glacier (아카이브)
- [ ] **파티셔닝 전략**: 날짜, 지역, 서비스 등 기준
- [ ] **파일 포맷**: JSON(원본) vs Parquet(분석용)
- [ ] **카탈로그**: Glue vs Hive Metastore vs Unity Catalog
- [ ] **거버넌스**: 암호화, 접근 제어, 감사 로그

#### 3. 안티패턴 (Anti-patterns)

- **데이터 늪 (Data Swamp)**: 메타데이터/카탈로그 없이 데이터만 쌓기
- **무분별한 JSON 저장**: Parquet 변환 없이 JSON만 저장 → 쿼리 성능 저하
- **파티셔닝 과소/과다**: 너무 적으면 스캔 많음, 너무 많으면 작은 파일 문제

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 구분 | DW 방식 | Data Lake 방식 | 개선 효과 |
|:---|:---|:---|:---|
| **수집 속도** | 변환 대기 | 즉시 저장 | 10배 향상 |
| **저장 비용** | $23/GB/년 | $0.023/GB/월 | 90% 절감 |
| **데이터 유형** | 정형만 | 모든 유형 | 유연성 확보 |
| **분석 민첩성** | 스키마 변경 필요 | 바로 분석 | Time-to-Insight 단축 |

#### 2. 미래 전망
데이터 레이크는 단독으로 사용되기보다 **데이터 레이크하우스**의 스토리지 계층으로 통합되고 있습니다. Apache Iceberg, Delta Lake, Apache Hudi 같은 오픈 테이블 포맷이 표준화되면서, 데이터 레이크 위에 ACID 트랜잭션, 타임 트래블, 스키마 에볼루션 기능이 추가되고 있습니다.

#### 3. 참고 표준
- **Apache Parquet Format**: Columnar Storage Format
- **Apache Iceberg Specification**: Table Format for Large Datasets
- **AWS S3 Best Practices**: Data Lake Architecture Guidelines

---

### 관련 개념 맵 (Knowledge Graph)
- **[데이터 웨어하우스 (Data Warehouse)](@/studynotes/14_data_engineering/01_data_arch/data_warehouse.md)**: 정형 데이터 분석 저장소
- **[데이터 레이크하우스 (Data Lakehouse)](@/studynotes/14_data_engineering/01_data_arch/data_lakehouse.md)**: 레이크 + DW 융합
- **[스키마 온 리드 (Schema-on-Read)](@/studynotes/14_data_engineering/01_data_arch/schema_on_read.md)**: 읽기 시점 스키마 적용
- **[Apache Iceberg](@/studynotes/14_data_engineering/01_data_arch/apache_iceberg.md)**: 오픈 테이블 포맷
- **[S3 객체 스토리지](@/studynotes/13_cloud_architecture/object_storage.md)**: 클라우드 스토리지

---

### 어린이를 위한 3줄 비유 설명
1. **커다란 호수**: 데이터 레이크는 자연 호수 같아요. 빗물, 강물, 시냇물 등 모든 물을 그대로 받아들이죠.
2. **필요할 때만 정수**: 호수의 물은 바로 마실 수는 없지만, 필요할 때만 정수해서 마시면 돼요. 미리 정수할 필요가 없죠.
3. **아무거나 다 넣어요**: 장난감, 돌멩이, 꽃잎 등 뭐든지 넣을 수 있어요. 나중에 필요한 것만 골라서 쓰면 됩니다!
