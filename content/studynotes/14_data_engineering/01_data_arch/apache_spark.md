+++
title = "아파치 스파크 (Apache Spark)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 아파치 스파크 (Apache Spark)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 아파치 스파크는 인메모리(In-Memory) 기반의 초고속 범용 분산 처리 엔진으로, 하둡 맵리듀스의 느린 디스크 I/O를 극복하고 배치, 스트리밍, ML, 그래프 처리를 통합 지원합니다.
> 2. **가치**: RDD(Resilient Distributed Dataset)라는 불변 분산 컬렉션 추상화와 지연 평가(Lazy Evaluation)로 100배 빠른 처리 성능을 제공합니다.
> 3. **융합**: SQL(DataFrame), Streaming(Structured Streaming), ML(MLlib), Graph(GraphX)을 단일 엔진에서 지원하는 통합 데이터 처리 플랫폼입니다.

---

### Ⅰ. 개요

#### 1. 개념 및 정의
**아파치 스파크(Apache Spark)**는 2009년 UC Berkeley AMPLab에서 개발된 오픈소스 분산 처리 엔진입니다. 맵리듀스와 달리 중간 결과를 메모리에 유지하여 반복 작업에서 최대 100배 빠른 성능을 발휘합니다.

#### 2. 핵심 구성요소
| 구성요소 | 역할 |
|:---|:---|
| **Spark Core** | RDD, 분산 작업 스케줄링 |
| **Spark SQL** | DataFrame, SQL 쿼리 |
| **Spark Streaming** | 실시간 스트림 처리 |
| **MLlib** | 머신러닝 라이브러리 |
| **GraphX** | 그래프 처리 |

---

### Ⅱ. 아키텍처

```text
<<< Apache Spark Architecture >>>

+--------------------------------------------------------------------------+
|                        Spark Application                                  |
+--------------------------------------------------------------------------+
|  +------------------+                                                    |
|  |   Driver Program |  (main() 실행, SparkContext 생성)                  |
|  +--------+---------+                                                    |
|           |                                                              |
|  +--------v---------+    +-------------+    +-------------+              |
|  |   Cluster Manager|<-->|  Executor 1 |    |  Executor 2 |              |
|  | (Standalone/YARN/|    | - Task 1    |    | - Task 3    |              |
|  |  Mesos/K8s)      |    | - Task 2    |    | - Task 4    |              |
|  +------------------+    | - Cache     |    | - Cache     |              |
|                          +-------------+    +-------------+              |
+--------------------------------------------------------------------------+

[RDD Lineage & Fault Tolerance]
RDD A → map → RDD B → filter → RDD C → reduce → Result
         |
         +-- 장애 발생 시 Lineage(계보)를 따라 재계산하여 복구
```

---

### Ⅲ. 핵심 원리

#### 1. RDD (Resilient Distributed Dataset)
- **Resilient**: 장애 시 자동 복구
- **Distributed**: 클러스터에 분산 저장
- **Dataset**: 불변(Immutable) 레코드 컬렉션

#### 2. 지연 평가 (Lazy Evaluation)
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Demo").getOrCreate()

# Transformation (즉시 실행 안함)
df = spark.read.parquet("s3://data/")  # Action 아님
filtered = df.filter(df.amount > 1000)  # Transformation
grouped = filtered.groupBy("category").count()  # Transformation

# Action (여기서 실제 실행)
result = grouped.collect()  # Action - 여기서 실행됨
```

---

### Ⅳ. 실무 적용

```python
# Spark DataFrame 예시
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg

spark = SparkSession.builder \
    .appName("Sales Analysis") \
    .getOrCreate()

# 데이터 로드
sales = spark.read.parquet("s3://lake/sales/")

# 변환 및 집계
result = sales \
    .filter(col("year") == 2024) \
    .groupBy("category") \
    .agg(
        sum("amount").alias("total_sales"),
        avg("amount").alias("avg_sales"),
        count("*").alias("transaction_count")
    ) \
    .orderBy(col("total_sales").desc())

# 결과 출력
result.show()

# 저장
result.write.parquet("s3://lake/curated/sales_summary/")
```

---

### Ⅴ. 결론

스파크는 현대 데이터 엔지니어링의 핵심 엔진이며, 데이터 레이크하우스 아키텍처에서 배치/스트리밍/ML을 통합 처리합니다.

---

### 관련 개념 맵
- **[RDD](@/studynotes/14_data_engineering/01_data_arch/rdd.md)**
- **[지연 평가](@/studynotes/14_data_engineering/01_data_arch/lazy_evaluation.md)**
- **[Apache Hadoop](@/studynotes/14_data_engineering/01_data_arch/apache_hadoop.md)**

---

### 어린이를 위한 3줄 비유
1. **기억력 좋은 요리사**: 스파크는 중간 과정을 기억해요. 다시 요리할 때 처음부터 안 하고 기억한 걸 써요.
2. **나중에 한 번에**: 재료를 썰고, 끓이고, 담는 걸 미리 계획만 하고, 손님 주문할 때 한 번에 해요.
3. **실수해도 복구**: 요리가 잘못되면 처음부터 다시 하는 게 아니라, 기억한 레시피로 다시 만들어요!
