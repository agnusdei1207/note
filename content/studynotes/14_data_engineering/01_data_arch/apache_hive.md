+++
title = "아파치 하이브 (Apache Hive)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 아파치 하이브 (Apache Hive)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 아파치 하이브는 HDFS에 저장된 데이터를 HiveQL(SQL-like)로 쿼리할 수 있는 데이터 웨어하우스 소프트웨어로, SQL을 MapReduce/Tez/Spark 작업으로 변환합니다.
> 2. **가치**: SQL에 익숙한 분석가가 하둡 데이터를 쿼리할 수 있게 하여, 빅데이터 분석의 진입 장벽을 낮췄습니다.
> 3. **융합**: 현재는 Spark SQL, Presto/Trino, 클라우드 DW로 대체되는 추세입니다.

---

### Ⅰ. 개요

#### 1. 핵심 특성
- **HiveQL**: SQL 유사 쿼리 언어
- **메타스토어**: 스키마와 파티션 메타데이터 관리
- **실행 엔진**: MapReduce, Tez, Spark

---

### Ⅱ. 아키텍처

```text
+------------------+
|   Hive Client    |
+--------+---------+
         |
         v
+--------+---------+
|   Hive Server    |
| - Parser         |
| - Optimizer      |
| - Executor       |
+--------+---------+
         |
         v
+--------+---------+
|   Metastore      |
| (MySQL/PostgreSQL)|
+--------+---------+
         |
         v
+--------+---------+
|      HDFS        |
+------------------+
```

---

### Ⅲ. HiveQL 예시

```sql
CREATE TABLE sales (
    id INT,
    product STRING,
    amount DOUBLE
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET;

SELECT year, month, SUM(amount)
FROM sales
GROUP BY year, month;
```

---

### Ⅳ. 결론

하이브는 하둡 생태계의 SQL 게이트웨이로서 역할을 다했으며, 현재는 더 빠른 엔진으로 대체되고 있습니다.

---

### 관련 개념 맵
- **[Apache Hadoop](@/studynotes/14_data_engineering/01_data_arch/apache_hadoop.md)**
- **[Apache Spark](@/studynotes/14_data_engineering/01_data_arch/apache_spark.md)**

---

### 어린이를 위한 3줄 비유
1. **번역기**: 외국어를 모르는 친구가 하이브 번역기를 써서 말해요.
2. **간단한 말로**: 어려운 하둡 말 대신 쉬운 SQL로 말해요.
3. **알아서 번역**: 하이브가 알아서 하둡이 알아듣는 말로 바꿔줘요!
