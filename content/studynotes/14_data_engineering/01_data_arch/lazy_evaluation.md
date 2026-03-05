+++
title = "지연 평가 (Lazy Evaluation)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 지연 평가 (Lazy Evaluation)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 지연 평가는 연산 요청을 즉시 실행하지 않고, 실행 계획(DAG)만 구축해 두었다가 실제 결과가 필요한 시점(Action)에 한 번에 최적화하여 실행하는 전략입니다.
> 2. **가치**: 불필요한 연산을 건너뛰고(Skipping), 여러 연산을 통합 최적화(Fusion)하여 성능을 극대화합니다.
> 3. **융합**: 스파크 RDD/DataFrame의 핵심 최적화 기법이며, 함수형 프로그래밍(Haskell)과 데이터베이스 쿼리 옵티마이저에도 적용됩니다.

---

### Ⅰ. 개요

#### 1. 개념
**지연 평가(Lazy Evaluation)**는 연산을 실제로 수행하지 않고, 무엇을 할지만 기록해 두었다가 결과가 정말 필요할 때 수행하는 평가 전략입니다.

#### 2. 스파크에서의 적용
- **Transformation**: 지연 평가 (map, filter, join)
- **Action**: 즉시 실행 (count, collect, save)

---

### Ⅱ. 동작 원리

```text
<<< Lazy Evaluation in Spark >>>

[Transformation 단계 - 실행 계획만 구축]
df1 = spark.read.parquet("data/")      # 실행 계획 추가
df2 = df1.filter(col("age") > 20)      # 실행 계획 추가
df3 = df2.select("name", "age")        # 실행 계획 추가
df4 = df3.groupBy("name").count()      # 실행 계획 추가

# 아직 실제 실행 안됨!

[Action 단계 - 실제 실행]
result = df4.collect()  # 여기서 모든 변환이 한 번에 실행됨

[최적화 효과]
- Catalyst 옵티마이저가 전체 DAG 분석
- 불필요한 컬럼 제거 (Column Pruning)
- 필터 조건 푸시다운 (Predicate Pushdown)
- 연산 융합 (Operation Fusion)
```

---

### Ⅲ. 장단점

**장점**:
- 불필요한 연산 생략
- 통합 최적화 가능
- 메모리 효율성

**단점**:
- 디버깅 어려움
- 실행 시점 예측 불가

---

### Ⅳ. 실무 적용

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("LazyDemo").getOrCreate()

# Transformation (지연)
df = spark.read.parquet("s3://data/users/")
active = df.filter(col("status") == "active")
names = active.select("name", "email")

# 실행 계획 확인
names.explain()

# Action (실제 실행)
result = names.collect()
```

---

### Ⅴ. 결론

지연 평가는 스파크의 핵심 최적화 기법으로, 대용량 데이터 처리 성능을 극대화합니다.

---

### 관련 개념 맵
- **[Apache Spark](@/studynotes/14_data_engineering/01_data_arch/apache_spark.md)**
- **[RDD](@/studynotes/14_data_engineering/01_data_arch/rdd.md)**
- **[DataFrame](@/studynotes/14_data_engineering/01_data_arch/dataframe.md)**

---

### 어린이를 위한 3줄 비유
1. **숙제 미루기**: 숙제를 하라고 하면 바로 안 하고, "나중에 할 리스트"에만 적어둬요.
2. **선생님이 확인할 때**: 선생님이 숙제 검사하라고 하면 그때 한 번에 다 해요.
3. **필요 없는 건 안 해**: 검사 안 보는 숙제는 리스트에서 지워서 안 해도 돼요!
