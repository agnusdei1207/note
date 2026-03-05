+++
title = "데이터 레이크하우스 (Data Lakehouse)"
categories = ["studynotes-16_bigdata"]
+++

# 데이터 레이크하우스 (Data Lakehouse)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Data Lakehouse는 **Data Lake의 유연성과 저비용** + **Data Warehouse의 ACID 트랜잭션과 고성능**을 결합한 차세대 데이터 아키텍처로, Delta Lake, Apache Iceberg, Apache Hudi 등의 **오픈 테이블 포맷** 위에 구축됩니다.
> 2. **가치**: 기존 Lambda 아키텍처(배치+실시간 분리)의 복잡성을 제거하고, **단일 플랫폼**에서 BI, ML, 스트리밍을 모두 지원하여 TCO 50% 절감, 데이터 엔지니어링 생산성 3배 향상을 실현합니다.
> 3. **융합**: Databricks(Delta Lake), Snowflake(Iceberg 지원), AWS(Apache Iceberg on S3), Microsoft Fabric(OneLake) 등 주요 클라우드 플랫폼에서 레이크하우스가 **데이터 분석의 표준 아키텍처**로 자리잡았습니다.

---

## Ⅰ. 개요 (Context & Background)

Data Lakehouse는 2020년 Databricks가 처음 제안한 개념으로, **Data Lake의 스토리지 비용 효율성**과 **Data Warehouse의 분석 성능/신뢰성**을 단일 플랫폼에서 제공합니다. 핵심 기술은 **오픈 테이블 포맷(Open Table Format)**으로, 객체 스토리지(S3, GCS, ADLS) 위에 ACID 트랜잭션, 스키마 강제, 타임 트래블 등을 구현합니다.

**💡 비유: 대형 마트 + 프리미엄 백화점의 결합**
Data Lake는 **거대한 창고형 마트**입니다. 물건이 많고 저렴하지만, 물건이 어디 있는지 찾기 어렵고 품질이 보장되지 않습니다. Data Warehouse는 **프리미엄 백화점**입니다. 물건이 정돈되어 있고 품질이 보장되지만, 비싸고 다양한 물건을 담기 어렵습니다. Data Lakehouse는 **이 두 가지의 장점을 합친 미래형 쇼핑몰**입니다. 창고처럼 저렴하게 물건을 많이 보관하면서도, 백화점처럼 정돈되어 있고 품질이 보장됩니다.

**등장 배경 및 발전 과정:**
1. **기존 기술의 치명적 한계점**:
   - **Data Lake**: Schema-on-Read로 인한 "Data Swamp", 데이터 품질 저하, ACID 미지원
   - **Data Warehouse**: 고비용, 비정형 데이터 미지원, 스키마 경직성
   - **Lambda 아키텍처**: 배치+실시간 이중화로 인한 복잡성, 데이터 중복
2. **혁신적 패러다임 변화**: **Delta Lake(2019)**, **Apache Iceberg(2018)**, **Apache Hudi(2016)** 등 오픈 테이블 포맷이 등장하여 객체 스토리지 위에 **ACID 트랜잭션 레이어**를 추가했습니다.
3. **비즈니스적 요구사항**: AI/ML 워크로드 증가, 실시간 분석 요구, 클라우드 네이티브 전환, 데이터 거버넌스 강화 등 복합적 요구가 Lakehouse 도입을 가속화했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Lakehouse 핵심 구성 요소

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|---|---|---|---|---|
| **Object Storage** | 저비용 데이터 저장 | S3/GCS/ADLS, Parquet/ORC 파일 | AWS S3, Azure ADLS | 창고 건물 |
| **Open Table Format** | ACID/메타데이터 관리 | Delta Log, Iceberg Manifest, Hudi Timeline | Delta Lake, Iceberg, Hudi | 정리 시스템 |
| **Compute Engine** | 쿼리 처리 및 분석 | Spark SQL, Presto/Trino, Flink | Databricks, Snowflake | 쇼핑 카트 |
| **Catalog** | 테이블 메타데이터 중앙 관리 | Unity Catalog, Glue Catalog, Hive Metastore | Unity Catalog, Polar | 상품 목록 |
| **Governance** | 보안, 계보, 품질 관리 | RBAC, Data Lineage, Data Quality Rules | Unity Catalog, Atlas | 품질 관리팀 |

### 정교한 구조 다이어그램 (ASCII Art)

```text
========================================================================================================
                              [ DATA LAKEHOUSE ARCHITECTURE ]
========================================================================================================

  [ DATA SOURCES ]              [ LAKEHOUSE ARCHITECTURE ]           [ CONSUMERS ]

  +-------------+              +-----------------------------------+ +-------------+
  | RDBMS       |              |        UNITY CATALOG              | | BI Tools    |
  | (CDC)       |----------+   |  +-------+ +-------+ +-------+   | | (Tableau)   |
  +-------------+          |   |  |Schema | |Policy | |Lineage|   | +-------------+
                           |   |  +-------+ +-------+ +-------+   |
  +-------------+          |   +-----------------------------------+ | +-------------+
  | Kafka       |          |              |                         | | ML Platform |
  | (Streaming) |----------+------------►|◄-----------------------►| | (MLflow)    |
  +-------------+          |              |                         | +-------------+
                           |   +-----------------------------------+
  +-------------+          |   |       COMPUTE LAYER               | | +-------------+
  | API Logs    |----------+   |  +----------+  +----------+       | | | Data API    |
  +-------------+          |   |  | Spark    |  | Presto/  |       | | | (REST)      |
                           |   |  | Engine   |  | Trino    |       | | +-------------+
  +-------------+          |   |  +----------+  +----------+       | |
  | Files       |----------+   +-----------------------------------+ |
  | (S3/ADLS)   |              |                                   |
  +-------------+              |        OPEN TABLE FORMAT          |
                               |  +--------------------------------+|
                               |  | Delta Lake | Iceberg | Hudi    ||
                               |  +--------------------------------+|
                               |  | - ACID Transactions            ||
                               |  | - Schema Enforcement           ||
                               |  | - Time Travel                  ||
                               |  | - Partition Pruning            ||
                               |  +--------------------------------+|
                               +-----------------------------------+
                                              |
                               +-----------------------------------+
                               |      OBJECT STORAGE (Cheap)       |
                               |  +-------------------------------+|
                               |  | Bronze Layer (Raw)            ||
                               |  | - Landing zone for all data   ||
                               |  +-------------------------------+|
                               |  | Silver Layer (Cleansed)       ||
                               |  | - Validated, deduped data     ||
                               |  +-------------------------------+|
                               |  | Gold Layer (Business-Ready)   ||
                               |  | - Aggregated, ML-ready data   ||
                               |  +-------------------------------+|
                               +-----------------------------------+

========================================================================================================
                              [ MEDALLION ARCHITECTURE ]
========================================================================================================

  [ BRONZE LAYER ]                 [ SILVER LAYER ]              [ GOLD LAYER ]

  ┌─────────────────┐            ┌─────────────────┐         ┌─────────────────┐
  │ Raw Data        │            │ Cleansed Data   │         │ Business-Ready  │
  │                 │            │                 │         │                 │
  │ - All columns   │──────────► │ - Validated     │───────► │ - Aggregated    │
  │ - All rows      │ Transform  │ - Deduplicated  │ Enrich  │ - Denormalized  │
  │ - No filtering  │            │ - Standardized  │         │ - Optimized     │
  │                 │            │                 │         │                 │
  │ Parquet/JSON    │            │ Delta/Iceberg   │         │ Delta/Iceberg   │
  │ Append-only     │            │ Upserts enabled │         │ Star Schema     │
  └─────────────────┘            └─────────────────┘         └─────────────────┘

  Characteristics:
  - Immutable raw data           - Data quality rules         - Business metrics
  - Full history preserved       - Schema enforcement         - ML feature store
  - Minimal transformation       - Join reference data        - Self-service BI

========================================================================================================
                              [ DELTA LAKE ACID TRANSACTION ]
========================================================================================================

  Transaction Log (_delta_log/)

  00000000000000000000.json  ← Initial commit
  ├── {"commitInfo": {"timestamp": 1234567890, "operation": "CREATE TABLE"}}
  └── {"metaData": {"id": "xxx", "schemaString": "{...}"}}

  00000000000000000001.json  ← Insert operation
  ├── {"add": {"path": "part-00000.parquet", "size": 1024, "modificationTime": ...}}
  └── {"add": {"path": "part-00001.parquet", "size": 2048, "modificationTime": ...}}

  00000000000000000002.json  ← Update operation (Delete old + Add new)
  ├── {"remove": {"path": "part-00000.parquet", "deletionTimestamp": ...}}
  └── {"add": {"path": "part-00002.parquet", "size": 3072, "modificationTime": ...}}

  ACID Properties:
  - Atomicity: Transaction log entries are atomic
  - Consistency: Schema validation before commit
  - Isolation: Snapshot isolation via log versioning
  - Durability: Write-ahead log on object storage

========================================================================================================
```

### 심층 동작 원리: Delta Lake ACID 구현

**1. Delta Lake 트랜잭션 로그**
```python
# PySpark로 Delta Lake 테이블 생성 및 관리
from pyspark.sql import SparkSession
from delta.tables import DeltaTable

spark = SparkSession.builder \
    .appName("LakehouseExample") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Bronze Layer: 원시 데이터 적재 (Append)
raw_events = spark.read.json("s3://raw/events/2024/01/")
raw_events.write.format("delta").mode("append").save("s3://lakehouse/bronze/events/")

# Silver Layer: 정제 및 검증
bronze_df = spark.read.format("delta").load("s3://lakehouse/bronze/events/")

# 데이터 품질 규칙 적용
silver_df = bronze_df \
    .filter("user_id IS NOT NULL") \
    .filter("event_time <= current_timestamp()") \
    .dropDuplicates(["event_id"]) \
    .withColumn("event_date", F.to_date("event_time"))

silver_df.write.format("delta").mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save("s3://lakehouse/silver/events/")

# Gold Layer: 비즈니스 집계
silver_df = spark.read.format("delta").load("s3://lakehouse/silver/events/")

gold_df = silver_df \
    .groupBy("event_date", "event_type") \
    .agg(
        F.count("*").alias("event_count"),
        F.countDistinct("user_id").alias("unique_users"),
        F.sum("revenue").alias("total_revenue")
    )

gold_df.write.format("delta").mode("overwrite") \
    .partitionBy("event_date") \
    .save("s3://lakehouse/gold/daily_metrics/")

# Time Travel: 특정 버전 조회
version_5_df = spark.read.format("delta") \
    .option("versionAsOf", 5) \
    .load("s3://lakehouse/silver/events/")

# MERGE INTO (Upsert)
delta_table = DeltaTable.forPath(spark, "s3://lakehouse/silver/users/")

updates_df = spark.read.format("delta").load("s3://lakehouse/bronze/user_updates/")

delta_table.alias("target").merge(
    updates_df.alias("source"),
    "target.user_id = source.user_id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
```

**2. Delta Lake vs Iceberg vs Hudi 비교**
```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    OPEN TABLE FORMAT COMPARISON                                 │
├─────────────────┬───────────────────┬───────────────────┬───────────────────────┤
│ Feature         │ Delta Lake        │ Apache Iceberg    │ Apache Hudi           │
├─────────────────┼───────────────────┼───────────────────┼───────────────────────┤
│ 개발사          │ Databricks        │ Netflix → Apache  │ Uber → Apache         │
├─────────────────┼───────────────────┼───────────────────┼───────────────────────┤
│ Primary Engine  │ Spark             │ Flink, Spark, Trino│ Spark, Flink         │
├─────────────────┼───────────────────┼───────────────────┼───────────────────────┤
│ ACID 구현       │ Transaction Log   │ Manifest Files    │ Timeline + Metadata   │
├─────────────────┼───────────────────┼───────────────────┼───────────────────────┤
│ Time Travel     │ O (Version-based) │ O (Snapshot-based)│ O (Timeline-based)    │
├─────────────────┼───────────────────┼───────────────────┼───────────────────────┤
│ Partition       │ Static            │ Hidden Partition  │ Static/Dynamic        │
│ Evolution       │                   │ (자동 파티션)     │                       │
├─────────────────┼───────────────────┼───────────────────┼───────────────────────┤
│ Upsert          │ MERGE INTO        │ MERGE INTO        │ Native Upsert         │
│ Performance     │ (Optimized)       │ (Iceberg v2)      │ (Copy-on-Write/       │
│                 │                   │                   │  Merge-on-Read)       │
├─────────────────┼───────────────────┼───────────────────┼───────────────────────┤
│ Schema Evolution│ Limited           │ Full Support      │ Full Support          │
├─────────────────┼───────────────────┼───────────────────┼───────────────────────┤
│ 적합 Use Case   │ BI/ML 통합        │ 다양한 엔진 지원  │ CDC/Incremental       │
│                 │ (Databricks)      │ (Trino/Flink)     │ Processing            │
└─────────────────┴───────────────────┴───────────────────┴───────────────────────┘
```

**3. Unity Catalog 통합 거버넌스**
```sql
-- Unity Catalog로 중앙 집중식 권한 관리

-- 1. 카탈로그 생성
CREATE CATALOG IF NOT EXISTS production;
CREATE CATALOG IF NOT EXISTS staging;

-- 2. 스키마 생성
CREATE SCHEMA IF NOT EXISTS production.sales;
CREATE SCHEMA IF NOT EXISTS production.marketing;

-- 3. 테이블 생성 (Managed Table)
CREATE TABLE production.sales.orders (
    order_id LONG,
    customer_id STRING,
    order_date DATE,
    amount DOUBLE
) USING DELTA
PARTITIONED BY (order_date);

-- 4. 권한 부여 (Fine-grained)
GRANT SELECT ON SCHEMA production.sales TO `data_analysts`;
GRANT SELECT, MODIFY ON TABLE production.sales.orders TO `sales_team`;

-- 5. 행 수준 보안 (Row-level Security)
CREATE FUNCTION production.sales.is_own_region(region STRING)
RETURNS BOOLEAN
RETURN CURRENT_USER() IN (SELECT user_id FROM region_managers WHERE region = region);

CREATE VIEW production.sales.orders_by_region AS
SELECT * FROM production.sales.orders
WHERE is_own_region(region);

GRANT SELECT ON VIEW production.sales.orders_by_region TO `regional_managers`;
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Data Lake vs Data Warehouse vs Data Lakehouse

| 비교 지표 | Data Lake | Data Warehouse | Data Lakehouse |
|---|---|---|---|
| **데이터 유형** | 모든 유형 (Raw) | 정형 데이터만 | 모든 유형 + 구조화 |
| **스키마** | Schema-on-Read | Schema-on-Write | Schema-on-Read + Enforcement |
| **ACID** | X | O | O |
| **비용** | 매우 낮음 | 높음 | 낮음 |
| **성능** | 낮음 (파일 스캔) | 높음 (인덱싱) | 높음 (통계/인덱싱) |
| **BI 지원** | 제한적 | 완벽 | 완벽 |
| **ML 지원** | 완벽 | 제한적 | 완벽 |
| **실시간** | 제한적 | X | O |
| **복잡성** | 낮음 | 중간 | 중간 |

### 과목 융합 관점 분석

- **[데이터베이스 + Lakehouse]**: Lakehouse는 RDBMS의 **ACID 트랜잭션**을 분산 파일 시스템에 구현합니다. MVCC(Multi-Version Concurrency Control), Write-Ahead Log, Snapshot Isolation 등의 기법이 Parquet 파일 위에서 동작합니다.

- **[운영체제 + Lakehouse]**: Lakehouse의 성능은 **객체 스토리지 최적화**에 크게 의존합니다. S3의 List API 병목을 피하기 위한 파티션 프루닝, 파일 크기 최적화, 캐싱 전략이 핵심입니다.

- **[보안 + Lakehouse]**: Unity Catalog는 **RBAC(Row-Level Security + Column Masking)**를 제공합니다. 데이터 이동 없이 단일 메타스토어에서 모든 데이터 자산의 권한을 관리합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 레거시 Data Warehouse 마이그레이션**
- **문제**: 기존 Teradata 시스템의 높은 라이선스 비용과 확장성 한계
- **전략적 의사결정**:
  1. **Lakehouse로 통합**: Snowflake 또는 Databricks로 이관
  2. **Medallion Architecture 도입**: Bronze → Silver → Gold 계층화
  3. **Incremental Migration**: 우선순위 테이블부터 순차적 이관
  4. **Cost Analysis**: TCO 60% 절감 목표

**시나리오 2: 실시간 + 배치 통합 플랫폼**
- **문제**: Lambda 아키텍처(Speed Layer + Batch Layer)의 중복 및 복잡성
- **전략적 의사결정**:
  1. **Kappa-like 단순화**: Kafka → Delta Lake로 직접 스트리밍
  2. **Structured Streaming**: Spark Structured Streaming으로 Bronze Layer 적재
  3. **Incremental Processing**: Silver/Gold는 Micro-batch로 갱신
  4. **Unified API**: 동일 Spark 코드로 배치/스트리밍 처리

**시나리오 3: ML Feature Store 구축**
- **문제**: ML 모델 학습용 Feature의 중복 개발 및 불일치
- **전략적 의사결정**:
  1. **Feature Store로 Lakehouse 활용**: Delta Table로 Feature 저장
  2. **Point-in-Time Correctness**: Time Travel로 과거 Feature 재현
  3. **Feature Serving**: Online Store(Redis) + Offline Store(Delta)
  4. **Feature Lineage**: Unity Catalog로 Feature 계보 추적

### 주의사항 및 안티패턴 (Anti-patterns)

- **안티패턴 - Small File Problem**: 너무 많은 작은 파일은 메타데이터 오버헤드와 쿼리 성능 저하를 유발. **OPTIMIZE**와 **Z-ORDER**로 파일 병합 필요

- **안티패턴 - Bronze Layer 과도한 정제**: Bronze Layer는 원시 데이터 그대로 보존해야. 정제는 Silver Layer에서 수행

- **안티패턴 - Governance 부재**: Lakehouse도 거버넌스 없으면 Data Swamp가 됨. **Unity Catalog** 또는 **DataHub** 필수 도입

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | 내용 및 지표 |
|---|---|
| **정성적 효과** | - 단일 플랫폼으로 BI/ML/Streaming 통합<br>- 데이터 중복 제거로 일관성 향상<br>- 셀프서비스 분석 환경 구축 |
| **정량적 효과** | - TCO **50~70% 절감** (DW 대비)<br>- 데이터 엔지니어링 생산성 **3배 향상**<br>- 쿼리 성능 **2~5배 개선** (Z-Ordering) |

### 미래 전망 및 진화 방향

- **Universal Format**: Delta UniForm으로 Delta/Iceberg/Hudi 상호 운용성 확보
- **AI-native Lakehouse**: LLM 기반 자연어 쿼리, Auto-optimization
- **Data Mesh Integration**: Lakehouse를 Data Product의 물리적 저장소로 활용

**※ 참고 표준/가이드**:
- **Databricks Lakehouse Platform**: 상용 Lakehouse 구현
- **Apache Iceberg Specification**: 오픈 테이블 포맷 표준
- **Delta Lake Protocol**: Delta Lake 트랜잭션 프로토콜

---

## 📌 관련 개념 맵 (Knowledge Graph)

- `[Delta Lake](@/studynotes/16_bigdata/06_data_lake/delta_lake.md)`: Databricks의 오픈 테이블 포맷
- `[Apache Iceberg](@/studynotes/16_bigdata/06_data_lake/apache_iceberg.md)`: Netflix의 오픈 테이블 포맷
- `[Medallion Architecture](@/studynotes/16_bigdata/06_data_lake/medallion_architecture.md)`: Bronze/Silver/Gold 계층 구조
- `[Data Mesh](@/studynotes/16_bigdata/06_data_lake/data_mesh.md)`: 분산형 데이터 아키텍처
- `[Unity Catalog](@/studynotes/16_bigdata/06_data_lake/unity_catalog.md)`: Databricks 통합 거버넌스

---

## 👶 어린이를 위한 3줄 비유 설명

1. **레이크하우스가 뭔가요?**: 큰 창고(Data Lake)와 예쁜 상점(Data Warehouse)을 **합친 곳**이에요. 창고처럼 많은 물건을 싸게 보관하면서도, 상점처럼 깔끔하게 정리되어 있어요.
2. **왜 좋은가요?**: 예전에는 창고에서 물건을 찾아서 상점으로 옮겨야 했어요. 이제는 그냥 바로 창고에서 찾아서 살 수 있어서 **시간과 돈을 아낄 수 있어요**.
3. **어디에 쓰나요?**: 넷플릭스에서 뭘 볼지 추천해 주거나, 은행에서 이상한 거래를 찾아낼 때 **엄청나게 많은 데이터**를 빠르고 정확하게 분석하는 데 써요!
