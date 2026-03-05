+++
title = "RDD (Resilient Distributed Dataset)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# RDD (Resilient Distributed Dataset)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: RDD는 스파크의 핵심 데이터 추상화로, 탄력적(Resilient), 분산(Distributed), 불변(Immutable) 특성을 가진 레코드 컬렉션입니다.
> 2. **가치**: 장애 발생 시 리니지(Lineage, 계보)를 통해 자동 복구되며, 지연 평가와 인메모리 캐싱으로 고성능 처리를 제공합니다.
> 3. **융합**: 현재는 고수준 API인 DataFrame/Dataset이 주로 사용되지만, RDD는 스파크의 근간을 이해하는 데 필수적입니다.

---

### Ⅰ. 개요

#### 1. RDD의 3가지 특성
- **Resilient (탄력적)**: 장애 시 Lineage 기반 자동 복구
- **Distributed (분산)**: 클러스터 노드에 파티션 단위 분산
- **Dataset (데이터셋)**: 불변(Immutable) 레코드 컬렉션

#### 2. 연산 유형
| 유형 | 설명 | 예시 |
|:---|:---|:---|
| **Transformation** | 새로운 RDD 생성 (지연 평가) | map, filter, join |
| **Action** | 결과 반환 (실제 실행) | count, collect, save |

---

### Ⅱ. 핵심 원리

```text
<<< RDD Lineage (계보) >>~

RDD A (원본)
   |
   +-- map --> RDD B
   |              |
   |              +-- filter --> RDD C
   |                              |
   +-- 장애 발생 시 Lineage를 따라 재계산
```

#### RDD 생성 방식
```python
# 1. 외부 데이터에서 생성
rdd = sc.textFile("hdfs://path/to/file")

# 2. 컬렉션에서 생성
rdd = sc.parallelize([1, 2, 3, 4, 5])

# 3. 다른 RDD 변환
rdd2 = rdd.map(lambda x: x * 2)
```

---

### Ⅲ. RDD vs DataFrame

| 비교 | RDD | DataFrame |
|:---|:---|:---|
| **타입** | 비정형 | 정형 (스키마 있음) |
| **최적화** | 제한적 | Catalyst 옵티마이저 |
| **성능** | 느림 | 빠름 |
| **사용성** | 복잡 | SQL과 유사 |

---

### Ⅳ. 실무 적용

```python
from pyspark import SparkContext

sc = SparkContext(appName="RDD Demo")

# RDD 생성 및 변환
rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Transformation (지연 평가)
squared = rdd.map(lambda x: x ** 2)
evens = squared.filter(lambda x: x % 2 == 0)

# Action (실제 실행)
result = evens.collect()  # [4, 16, 36, 64, 100]

# 캐싱 (반복 사용 시)
rdd.cache()
```

---

### Ⅴ. 결론

RDD는 스파크의 근간이며, 내부 동작 원리를 이해하는 데 필수적입니다. 실무에서는 DataFrame/Dataset을 주로 사용합니다.

---

### 관련 개념 맵
- **[Apache Spark](@/studynotes/14_data_engineering/01_data_arch/apache_spark.md)**
- **[지연 평가](@/studynotes/14_data_engineering/01_data_arch/lazy_evaluation.md)**
- **[DataFrame](@/studynotes/14_data_engineering/01_data_arch/dataframe.md)**

---

### 어린이를 위한 3줄 비유
1. **나눠서 보관**: 큰 창고의 물건을 여러 방에 나눠서 보관해요.
2. **족보가 있어요**: 물건이 어디서 왔는지 족보로 알 수 있어서, 잃어버려도 다시 찾을 수 있어요.
3. **절대 안 바뀌어**: 한 번 만든 건 바꿀 수 없어요. 새로 만들어야 해요!
