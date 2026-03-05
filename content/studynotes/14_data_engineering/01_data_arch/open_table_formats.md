+++
title = "오픈 테이블 포맷 (Open Table Formats)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 오픈 테이블 포맷 (Open Table Formats)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 오픈 테이블 포맷(Apache Iceberg, Delta Lake, Apache Hudi)은 데이터 레이크 위에 ACID 트랜잭션, 타임 트래블, 스키마 에볼루션을 제공하는 메타데이터 계층입니다.
> 2. **가치**: 객체 스토리지(S3)의 파일 덩어리를 RDBMS 수준의 테이블로 관리하여, 데이터 레이크하우스를 완성합니다.
> 3. **융합**: Spark, Flink, Trino 등 다양한 엔진에서 동일한 테이블을 공유할 수 있어 벤더 락인(Lock-in)을 방지합니다.

---

### Ⅰ. 개요

#### 1. 3대 오픈 테이블 포맷

| 포맷 | 개발사 | 특징 |
|:---|:---|:---|
| **Apache Iceberg** | Netflix | 표준화, 멀티엔진 지원 |
| **Delta Lake** | Databricks | Spark 통합, 성능 최적화 |
| **Apache Hudi** | Uber | CDC, Upsert 특화 |

---

### Ⅱ. 핵심 기능

1. **ACID 트랜잭션**: 원자성, 일관성 보장
2. **타임 트래블**: 과거 스냅샷 조회
3. **스키마 에볼루션**: 컬럼 추가/변경
4. **파티션 에볼루션**: 파티션 변경
5. **데이터 스킵**: Min/Max 통계로 성능 최적화

---

### Ⅲ. 아키텍처

```text
+------------------+
| Compute Engine   |
| (Spark/Flink)    |
+--------+---------+
         |
         v
+--------+---------+
| Table Format     |
| (Iceberg/Delta)  |
| - Metadata       |
| - Manifest       |
| - Snapshot       |
+--------+---------+
         |
         v
+--------+---------+
| Object Storage   |
| (S3/GCS/ADLS)    |
| - Parquet Files  |
+------------------+
```

---

### Ⅳ. Iceberg 예시

```sql
-- 테이블 생성
CREATE TABLE sales (
    id BIGINT,
    product STRING,
    amount DOUBLE
) USING iceberg
PARTITIONED BY (days(timestamp));

-- 타임 트래블
SELECT * FROM sales TIMESTAMP AS OF '2024-03-01';

-- 스냅샷 관리
CALL system.expire_snapshots('sales', '2024-03-01');
```

---

### Ⅴ. 결론

오픈 테이블 포맷은 데이터 레이크하우스의 핵심 기술이며, 현대 데이터 아키텍처의 표준으로 자리 잡았습니다.

---

### 관련 개념 맵
- **[데이터 레이크하우스](@/studynotes/14_data_engineering/01_data_arch/data_lakehouse.md)**
- **[Parquet](@/studynotes/14_data_engineering/01_data_arch/parquet.md)**

---

### 어린이를 위한 3줄 비유
1. **책갈피**: 오픈 테이블 포맷은 책갈피예요. 어디까지 읽었는지 표시해줘요.
2. **독서 기록**: 언제 읽었는지, 무엇을 읽었는지 기록해줘요.
3. **시간 여행**: 지난달에 읽은 내용을 다시 보고 싶으면 기록에서 찾아봐요!
