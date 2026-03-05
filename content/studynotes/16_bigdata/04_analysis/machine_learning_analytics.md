+++
title = "빅데이터 분석 기법 (Machine Learning Analytics)"
categories = ["studynotes-16_bigdata"]
+++

# 빅데이터 분석 기법 (Machine Learning Analytics)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 빅데이터 분석 기법은 대규모 데이터로부터 의미 있는 패턴, 상관관계, 예측 모델을 도출하는 통계적/알고리즘적 방법론으로, **기술 통계, 추론 통계, 머신러닝, 딥러닝**이 통합된 다층적 접근을 포함합니다.
> 2. **가치**: 데이터 기반 의사결정의 정확도를 높이고, 미래 예측, 이상 탐지, 개인화 추천 등 **비즈니스 가치를 창출**하며, 자동화된 인사이트 도출로 분석 생산성을 획기적으로 향상합니다.
> 3. **융합**: Spark MLlib, Scikit-learn, TensorFlow, PyTorch 등과 결합하여 **분산 처리 기반 ML 파이프라인**을 구축하고, MLOps로 운영화(Productionization)됩니다.

---

## Ⅰ. 개요 (Context & Background)

빅데이터 분석은 단순한 숫자 요약을 넘어 **데이터로부터 실행 가능한 인사이트(Actionable Insights)**를 도출하는 종합적 학문입니다. 기술 통계(Descriptive)에서 시작하여 진단(Diagnostic), 예측(Predictive), 처방(Prescriptive) 분석으로 진화하며, 현재는 **AI/ML 기반 자동화 분석**이 주류입니다.

**💡 비유: 의사의 진단 과정**
빅데이터 분석은 **의사가 환자를 진단하는 과정**과 같습니다. 첫째, 환자의 증상을 관찰하고 기록합니다(**기술 통계**). 둘째, 왜 아픈지 원인을 찾습니다(**진단 분석**). 셋째, 병이 어떻게 진행될지 예측합니다(**예측 분석**). 넷째, 어떤 치료를 할지 처방합니다(**처방 분석**). 최근에는 AI 의사가 자동으로 진단하고 처방까지 제안합니다(**자동화 분석**).

**등장 배경 및 발전 과정:**
1. **기존 기술의 치명적 한계점**: 전통적 통계 분석은 샘플링에 의존하여 **전체 데이터의 패턴을 놓칠 수 있었고**, 정형 데이터만 처리 가능했습니다.
2. **혁신적 패러다임 변화**: 머신러닝의 부상으로 **패턴을 자동으로 학습**하는 방식으로 전환되었고, 딥러닝으로 비정형 데이터(이미지, 텍스트) 분석이 가능해졌습니다.
3. **비즈니스적 요구사항**: 실시간 개인화, 이상 탐지, 수요 예측 등 **예측 정확도와 처리 속도**에 대한 요구가 급증했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 빅데이터 분석 4단계 모델

| 단계 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|---|---|---|---|---|
| **Descriptive (기술)** | 과거 현황 파악 | 집계, 그룹화, 요약 통계 | SQL, Pandas, Tableau | 증상 관찰 |
| **Diagnostic (진단)** | 원인 분석 | 상관분석, 회귀, 드릴다운 | OLAP, Root Cause Analysis | 원인 찾기 |
| **Predictive (예측)** | 미래 예측 | ML 모델 학습, 시계열 분석 | Scikit-learn, Prophet, ARIMA | 예후 예측 |
| **Prescriptive (처방)** | 최적 행동 제안 | 최적화, 의사결정 모델, 추천 | OR, Recommender Systems | 치료 처방 |

### 정교한 구조 다이어그램 (ASCII Art)

```text
========================================================================================================
                              [ BIG DATA ANALYTICS MATURITY MODEL ]
========================================================================================================

                        Value
                          ▲
                          │
         [ PRESCRIPTIVE ] │     "What should we do?"
         - Optimization   │     - Recommender Systems
         - Simulation     │     - A/B Testing
         - Decision       │     - Auto-ML
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        │   [ PREDICTIVE ]│                 │
        │   "What will    │                 │
        │    happen?"     │                 │
        │   - Forecasting │                 │
        │   - ML Models   │                 │
        │   - Anomaly     │                 │
        │     Detection   │                 │
        │                 │                 │
        │  ┌──────────────┼──────────────┐  │
        │  │  [ DIAGNOSTIC ]             │  │
        │  │  "Why did it happen?"       │  │
        │  │  - Correlation Analysis     │  │
        │  │  - Drill-down               │  │
        │  │  - Root Cause               │  │
        │  │                             │  │
        │  │  ┌────────────────────────┐ │  │
        │  │  │   [ DESCRIPTIVE ]      │ │  │
        │  │  │   "What happened?"     │ │  │
        │  │  │   - Reporting          │ │  │
        │  │  │   - Dashboards         │ │  │
        │  │  │   - Aggregation        │ │  │
        │  │  └────────────────────────┘ │  │
        │  └─────────────────────────────┘  │
        └───────────────────────────────────┘

                          Complexity ──►

========================================================================================================
                              [ ML ANALYTICS PIPELINE ]
========================================================================================================

  [ DATA INGESTION ]      [ FEATURE ENGINEERING ]     [ MODEL TRAINING ]      [ SERVING ]
  +---------------+       +-------------------+       +----------------+      +----------+
  | Raw Data      |       | Feature Store     |       | Experiment     |      | API      |
  | (S3/GCS/HDFS) |------>| - Transformation  |------>| Tracking       |----->| Endpoint |
  +---------------+       | - Aggregation     |       | (MLflow)       |      +----------+
                          | - Embedding       |       |                |           │
  +---------------+       +-------------------+       | [Model Registry]          │
  | Streaming     |                                  +----------------+           v
  | (Kafka)       |----------(Real-time Features)---------->|                  +----------+
  +---------------+                                           |                  | Batch    |
                                                              |                  | Predict  |
  +---------------+           +-------------------+           |                  +----------+
  | CDC Events    |---------->| Feature Pipeline  |---------->|                       ^
  +---------------+           +-------------------+           |                       |
                                                              |                  +----------+
                                                              |                  | Real-time|
                                                              |                  | Predict  |
                                                              |                  +----------+
                                                              │
                                                              ▼
                                                    [ MONITORING & GOVERNANCE ]
                                                    - Data Drift Detection
                                                    - Model Performance
                                                    - Bias & Fairness

========================================================================================================
```

### 심층 동작 원리: 분산 ML 파이프라인

**1. Spark MLlib를 활용한 분산 머신러닝**
```python
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StandardScaler, StringIndexer
from pyspark.ml.classification import RandomForestClassifier, GBTClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

# Spark 세션 초기화
spark = SparkSession.builder \
    .appName("BigDataMLPipeline") \
    .config("spark.executor.memory", "8g") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()

# 대용량 데이터 로드 (Parquet)
df = spark.read.parquet("s3://data-lake/gold/customer_features/")

# Feature Engineering Pipeline
# 1. 범주형 변수 인코딩
categorical_cols = ["gender", "country", "segment"]
indexers = [StringIndexer(inputCol=col, outputCol=f"{col}_idx") for col in categorical_cols]

# 2. 수치형 변수 어셈블리
numeric_cols = ["age", "income", "purchase_count", "days_since_last_purchase"]
assembler = VectorAssembler(
    inputCols=numeric_cols + [f"{col}_idx" for col in categorical_cols],
    outputCol="features_raw"
)

# 3. 표준화
scaler = StandardScaler(
    inputCol="features_raw",
    outputCol="features",
    withStd=True,
    withMean=True
)

# 4. 모델 정의 (Random Forest)
rf = RandomForestClassifier(
    labelCol="churn",
    featuresCol="features",
    numTrees=100,
    maxDepth=10,
    seed=42
)

# Pipeline 구성
pipeline = Pipeline(stages=indexers + [assembler, scaler, rf])

# 하이퍼파라미터 튜닝 (Cross-Validation)
paramGrid = ParamGridBuilder() \
    .addGrid(rf.numTrees, [50, 100, 200]) \
    .addGrid(rf.maxDepth, [5, 10, 15]) \
    .build()

crossval = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=paramGrid,
    evaluator=BinaryClassificationEvaluator(labelCol="churn", metricName="areaUnderROC"),
    numFolds=5,
    parallelism=4  # 병렬 처리
)

# 학습 (분산)
train_data, test_data = df.randomSplit([0.8, 0.2], seed=42)
cv_model = crossval.fit(train_data)

# 예측 및 평가
predictions = cv_model.transform(test_data)
evaluator = BinaryClassificationEvaluator(labelCol="churn", metricName="areaUnderROC")
auc = evaluator.evaluate(predictions)
print(f"AUC: {auc:.4f}")

# 모델 저장
best_model = cv_model.bestModel
best_model.write().overwrite().save("s3://models/churn_prediction/v1/")
```

**2. 시계열 분석 (Prophet + Spark)**
```python
from prophet import Prophet
import pandas as pd
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import StructType, StructField, TimestampType, FloatType, StringType

# Prophet 시계열 예측 (분산 처리)
schema = StructType([
    StructField("ds", TimestampType(), True),
    StructField("yhat", FloatType(), True),
    StructField("yhat_lower", FloatType(), True),
    StructField("yhat_upper", FloatType(), True),
    StructField("store_id", StringType(), True)
])

@pandas_udf(schema)
def forecast_store(pdf: pd.DataFrame) -> pd.DataFrame:
    """각 매장별 Prophet 예측 (병렬 실행)"""
    store_id = pdf['store_id'].iloc[0]

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.05
    )

    # 한국 공휴일 추가
    model.add_country_holidays(country_name='KR')

    # 학습
    model.fit(pdf[['ds', 'y']])

    # 30일 예측
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    forecast['store_id'] = store_id
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'store_id']]

# 전체 매장에 대해 분산 예측
df = spark.read.parquet("s3://data-lake/sales_daily/")
forecasts = df.groupBy("store_id").apply(forecast_store)
forecasts.write.parquet("s3://predictions/store_forecasts/")
```

**3. 이상 탐지 (Isolation Forest)**
```python
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.linalg import Vectors
import numpy as np

# Isolation Forest를 활용한 이상 탐지
def isolation_forest_score(data, n_trees=100, sample_size=256):
    """
    Isolation Forest 구현 (개념적)
    실제로는 spark-iforest 또는 PyOD 라이브러리 사용 권장
    """
    scores = []

    for _ in range(n_trees):
        # 랜덤 샘플링
        sample = data.sample(False, sample_size / data.count())

        # 트리 구축 (재귀적 분할)
        # ...

        # 경로 길이 계산
        # ...

    # 이상 점수: 짧은 경로 = 이상치
    return scores

# 활용: 금융 사기 탐지
transactions = spark.read.parquet("s3://data-lake/transactions/")

# Feature Engineering
assembler = VectorAssembler(
    inputCols=["amount", "hour", "merchant_risk_score", "distance_from_home"],
    outputCol="features"
)
feature_df = assembler.transform(transactions)

# Isolation Forest 학습
# (실제 구현은 spark-iforest 라이브러리 사용)
from spark_iforest import IForest

iforest = IForest(
    numTrees=100,
    maxSamples=256,
    maxFeatures=1.0,
    featuresCol="features",
    predictionCol="is_anomaly",
    anomalyScoreCol="anomaly_score"
)

model = iforest.fit(feature_df)
predictions = model.transform(feature_df)

# 이상 거래 필터링
anomalies = predictions.filter(predictions.is_anomaly == 1)
anomalies.write.parquet("s3://alerts/fraud_detection/")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 분석 기법별 특성

| 분석 기법 | 입력 데이터 | 출력 | 복잡도 | 적용 분야 |
|---|---|---|---|---|
| **회귀 분석** | 수치형 | 연속값 예측 | 낮음 | 매출 예측, 가격 책정 |
| **분류** | 혼합형 | 범주 예측 | 중간 | 이탈 예측, 스팸 탐지 |
| **군집화** | 수치형 | 그룹 할당 | 중간 | 세분화, 패턴 발견 |
| **연관 규칙** | 트랜잭션 | 규칙(지지도/신뢰도) | 낮음 | 장바구니 분석 |
| **시계열** | 시계열 | 미래 값 예측 | 높음 | 수요 예측, 주가 예측 |
| **딥러닝** | 비정형 | 복합적 | 매우 높음 | 이미지, NLP, 음성 |

### 과목 융합 관점 분석

- **[통계학 + ML]**: 머신러닝은 통계학의 확장입니다. 회귀분석, 베이지안 추론, 가설 검정 등 **통계적 기반**이 ML 모델의 이론적 근거가 됩니다.

- **[선형대수 + ML]**: 행렬 연산, 차원 축소(PCA), SVD 등 **선형대수**는 ML 알고리즘의 핵심 연산입니다. Spark MLlib은 분산 행렬 연산을 최적화합니다.

- **[운영체제 + ML]**: 대규모 ML 학습은 **메모리 관리, GPU 스케줄링, 분산 컴퓨팅**에 의존합니다. Kubernetes 기반 ML 플랫폼이 표준화되고 있습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 고객 이탈 예측 시스템**
- **문제**: 구독 서비스의 월간 이탈률 5%를 줄여야 함
- **전략적 의사결정**:
  1. **문제 정의**: 이진 분류 (Churn vs Retain)
  2. **Feature Engineering**: 행동 패턴, 접속 빈도, 결제 이력 등 200개 Feature
  3. **모델 선택**: XGBoost + LightGBM 앙상블
  4. **운영화**: Spark Streaming으로 실시간 점수 산정

**시나리오 2: 실시간 추천 시스템**
- **문제**: 이커머스 클릭률(CTR) 2% → 4% 목표
- **전략적 의사결정**:
  1. **협업 필터링**: Matrix Factorization (ALS)
  2. **콘텐츠 기반**: 상품 임베딩 (Word2Vec)
  3. **하이브리드**: 두 모델의 가중 결합
  4. **실시간 갱신**: Kafka + Flink로 실시간 피드백

### 주의사항 및 안티패턴 (Anti-patterns)

- **안티패턴 - Data Leakage**: 학습 데이터에 미래 정보가 포함되어 과적합. **시간 기반 분할** 필수

- **안티패턴 - Feature Store 부재**: Feature 재사용 불가로 일관성 저하. **중앙화된 Feature Store** 구축

- **안티패턴 - 모델 모니터링 부재**: Data Drift로 성능 저하. **지속적 모니터링** 시스템 구축

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | 내용 및 지표 |
|---|---|
| **정성적 효과** | - 데이터 기반 의사결정 문화 정착<br>- 자동화된 인사이트 도출<br>- 비즈니스 민첩성 향상 |
| **정량적 효과** | - 예측 정확도 **85~95%** 달성<br>- 분석 생산성 **5~10배 향상**<br>- ROI **300% 이상** |

### 미래 전망 및 진화 방향

- **AutoML**: 자동 Feature Engineering, 모델 선택, 하이퍼파라미터 튜닝
- **LLM 기반 분석**: 자연어로 쿼리 및 분석 요청
- **Causal AI**: 상관관계를 넘어 인과관계 추론

**※ 참고 표준/가이드**:
- **CRISP-DM**: 데이터 마이닝 표준 프로세스
- **MLflow**: ML 라이프사이클 관리 표준

---

## 📌 관련 개념 맵 (Knowledge Graph)

- `[MLOps](@/studynotes/16_bigdata/08_platform/mlops.md)`: ML 모델 운영화
- `[Feature Store](@/studynotes/16_bigdata/08_platform/feature_store.md)`: Feature 관리 플랫폼
- `[Spark MLlib](@/studynotes/16_bigdata/01_processing/apache_spark.md)`: 분산 ML 라이브러리
- `[추천 시스템](@/studynotes/16_bigdata/04_analysis/recommender_system.md)`: 개인화 추천 기법
- `[시계열 분석](@/studynotes/16_bigdata/04_analysis/time_series_analysis.md)`: 시간 기반 예측

---

## 👶 어린이를 위한 3줄 비유 설명

1. **분석 기법이 뭔가요?**: 많은 데이터에서 **숨겨진 패턴을 찾는 방법**이에요. 마치 탐정이 단서를 모아서 범인을 찾는 것과 같아요.
2. **머신러닝은요?**: 컴퓨터가 **스스로 배우는 것**이에요. 많은 예시를 보여주면 컴퓨터가 "아, 이런 패턴이구나!" 하고 스스로 규칙을 찾아요.
3. **어디에 쓰나요?**: 넷플릭스가 뭘 좋아할지 예측하거나, 은행이 이상한 거래를 찾거나, 날씨를 예측하는 데 써요!
