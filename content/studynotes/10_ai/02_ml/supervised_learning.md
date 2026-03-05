+++
title = "지도 학습 (Supervised Learning)"
date = "2026-03-04"
[extra]
categories = ["studynotes-10_ai"]
+++

# 지도 학습 (Supervised Learning)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 입력 특성(Feature X)과 정답 라벨(Label Y)의 쌍으로 구성된 데이터를 사용하여, 새로운 입력에 대한 정확한 출력을 예측하는 함수 f: X → Y를 학습하는 가장 기본적인 머신러닝 패러다임입니다.
> 2. **가치**: 스팸 필터링(99%+ 정확도), 이미지 분류(97%+), 질병 진단(95%+), 주가 예측 등 산업 전반에서 가장 널리 활용되며, 명확한 성과 측정이 가능해 기업 도입 장벽이 가장 낮습니다.
> 3. **융합**: 딥러닝의 기반으로, 전이 학습(Transfer Learning), 반지도 학습(Semi-supervised Learning), 자기 지도 학습(Self-supervised Learning)으로 확장됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**지도 학습(Supervised Learning)**은 기계학습의 가장 기본적인 형태로, **(1) 라벨링된 훈련 데이터, (2) 손실 함수(Loss Function), (3) 최적화 알고리즘**의 세 요소로 구성됩니다.

수학적으로, 데이터셋 $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^{N}$이 주어졌을 때, 최적의 함수 $f^*$를 찾는 것입니다:

$$f^* = \arg\min_f \frac{1}{N} \sum_{i=1}^{N} L(f(x_i), y_i) + \lambda \Omega(f)$$

여기서:
- $L$: 손실 함수 (MSE, Cross-Entropy 등)
- $\Omega$: 정규화 항 (Regularization)
- $\lambda$: 정규화 강도

**주요 유형**:
1. **분류 (Classification)**: 이산형 출력 (스팸/정상, 질병 유무)
2. **회귀 (Regression)**: 연속형 출력 (주가, 온도, 매출)

#### 2. 💡 비유를 통한 이해
지도 학습은 **'정답이 있는 문제집 풀기'**에 비유할 수 있습니다:

- **훈련 데이터**: 문제(x)와 정답(y)이 함께 있는 문제집
- **학습**: 정답을 보면서 푸는 법을 익힘
- **테스트**: 정답이 없는 새로운 문제 풀기
- **손실 함수**: 틀린 만큼 벌점
- **과적합**: 문제집 답만 외워서 새로운 문제를 못 풂
- **일반화**: 문제의 원리를 이해해서 어떤 문제든 풀 수 있음

#### 3. 등장 배경 및 발전 과정

1.  **기존 기술의 치명적 한계점**:
    - **규칙 기반 시스템**: 모든 규칙을 인간이 작성해야 함. 예외 처리 불가능.
    - **통계적 방법**: 선형 관계만 모델링 가능. 복잡한 패턴 인식 불가.

2.  **혁신적 패러다임의 변화**:
    - **선형 회귀 (1805)**: 최소제곱법으로 시작
    - **로지스틱 회귀 (1958)**: 분류 문제로 확장
    - **결정 트리 (1984)**: 비선형 분할 가능
    - **SVM (1995)**: 마진 최대화로 일반화 향상
    - **앙상블 (2000~)**: 배깅, 부스팅으로 성능 급상승
    - **딥러닝 (2012~)**: 이미지/음성/자연어에서 인간 능가

3.  **비즈니스적 요구사항**:
    - 고객 이탈 예측, 신용평가, 사기 탐지
    - 의료 진단, 제조 품질 검사
    - 마케팅 타겟팅, 개인화 추천

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 지도 학습 파이프라인 구성 요소 (표)

| 단계 | 상세 역할 | 내부 동작 메커니즘 | 도구/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **데이터 수집** | 원시 데이터 확보 | DB, API, 크롤링 | SQL, Kafka | 문제집 구입 |
| **라벨링** | 정답 부착 | 인간 어노테이션, 약한 지도 | Labelbox, Prodigy | 정답 작성 |
| **전처리** | 데이터 정제 | 결측치, 이상치 처리 | Pandas, NumPy | 문제 정리 |
| **특성 공학** | 유의미 특성 추출 | 변환, 선택, 생성 | Scikit-learn | 핵심 요약 |
| **모델 학습** | 패턴 학습 | 최적화 알고리즘 | TensorFlow, PyTorch | 공부 |
| **평가** | 성능 측정 | 교차 검증, 지표 계산 | Scikit-learn | 모의고사 |
| **배포** | 실제 적용 | API, 배치 추론 | FastAPI, ONNX | 실전 투입 |

#### 2. 지도 학습 워크플로우 다이어그램

```text
<<< Supervised Learning Pipeline >>=>

    [Raw Data]
         │
         ▼
    ┌─────────────┐
    │  수집/저장   │ ← DB, API, Files
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │  라벨링     │ ← Human Annotation, Weak Supervision
    │  (x, y) 쌍  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │  전처리     │ ← Cleaning, Normalization, Encoding
    │  결측치/이상치│
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Feature Eng.│ ← Selection, Extraction, Generation
    │  X_train    │
    └──────┬──────┘
           │
           ├──────────────────────┐
           │                      │
           ▼                      ▼
    ┌─────────────┐        ┌─────────────┐
    │  Train Set  │        │   Test Set  │
    │   (70%)     │        │    (30%)    │
    └──────┬──────┘        └──────┬──────┘
           │                      │
           ▼                      │
    ┌─────────────┐               │
    │ 모델 학습   │               │
    │ f(X) → Ŷ   │               │
    └──────┬──────┘               │
           │                      │
           ▼                      ▼
    ┌─────────────────────────────────┐
    │           평가 (Evaluation)      │
    │   Loss = L(Y, Ŷ)                │
    │   Metrics: Acc, F1, RMSE, ...   │
    └─────────────────────────────────┘


<<< Classification vs Regression >>=>

    [Classification]                    [Regression]
    Y ∈ {0, 1, 2, ..., K}              Y ∈ ℝ (연속값)

    ┌───────────────┐                  ┌───────────────┐
    │ Input Image   │                  │ House Features│
    │ (고양이 사진) │                  │ (면적, 방개수)│
    └───────┬───────┘                  └───────┬───────┘
            │                                  │
            ▼                                  ▼
    ┌───────────────┐                  ┌───────────────┐
    │    Model f    │                  │   Model f     │
    │  (Softmax)    │                  │  (Linear/NN)  │
    └───────┬───────┘                  └───────┬───────┘
            │                                  │
            ▼                                  ▼
    ┌───────────────┐                  ┌───────────────┐
    │   [0.1,       │                  │   Ŷ = 5.2억   │
    │    0.8, ← Cat │                  │   (예측 가격) │
    │    0.1]       │                  └───────────────┘
    └───────────────┘

    Loss: CrossEntropy                  Loss: MSE
    Metric: Accuracy, F1                Metric: RMSE, R²
```

#### 3. 핵심 평가 지표

**분류 문제 평가 지표**:
| 지표 | 수식 | 의미 |
|:---|:---|:---|
| **Accuracy** | (TP+TN)/(TP+TN+FP+FN) | 전체 정답률 |
| **Precision** | TP/(TP+FP) | 양성 예측 중 실제 양성 |
| **Recall (TPR)** | TP/(TP+FN) | 실제 양성 중 맞춘 비율 |
| **F1-Score** | 2×P×R/(P+R) | Precision과 Recall 조화 평균 |
| **ROC-AUC** | 곡선 아래 면적 | 임계값 무관 성능 |

**회귀 문제 평가 지표**:
| 지표 | 수식 | 의미 |
|:---|:---|:---|
| **MSE** | (1/n)Σ(y-ŷ)² | 평균 제곱 오차 |
| **RMSE** | √MSE | MSE 제곱근 (단위 동일) |
| **MAE** | (1/n)Σ\|y-ŷ\| | 평균 절대 오차 |
| **R²** | 1 - SS_res/SS_tot | 설명 분산 비율 |

#### 4. 실무 수준의 Scikit-Learn 분류 파이프라인

```python
"""
Production-Ready Supervised Learning Pipeline
- 분류 문제 기준
- 전처리, 모델 선택, 하이퍼파라미터 튜닝, 평가 포함
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score
)
import matplotlib.pyplot as plt
import seaborn as sns

class SupervisedLearningPipeline:
    """
    엔터프라이즈급 지도 학습 파이프라인
    """

    def __init__(
        self,
        target_column: str,
        problem_type: str = 'classification',  # 'classification' or 'regression'
        random_state: int = 42
    ):
        self.target_column = target_column
        self.problem_type = problem_type
        self.random_state = random_state
        self.model = None
        self.preprocessor = None

    def prepare_data(
        self,
        df: pd.DataFrame,
        test_size: float = 0.2
    ) -> tuple:
        """
        데이터 준비 및 분할
        """
        # 특성과 타겟 분리
        X = df.drop(columns=[self.target_column])
        y = df[self.target_column]

        # 범주형/수치형 컬럼 식별
        self.numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        self.categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

        # 전처리 파이프라인 구축
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])

        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, self.numeric_cols),
                ('cat', categorical_transformer, self.categorical_cols)
            ]
        )

        # 레이블 인코딩 (분류용)
        if self.problem_type == 'classification':
            self.label_encoder = LabelEncoder()
            y = self.label_encoder.fit_transform(y)

        # 학습/테스트 분할
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state,
            stratify=y if self.problem_type == 'classification' else None
        )

        return X_train, X_test, y_train, y_test

    def train(
        self,
        X_train: pd.DataFrame,
        y_train: np.ndarray,
        model_type: str = 'random_forest',
        hyperparameter_tuning: bool = False
    ):
        """
        모델 학습
        """
        # 모델 선택
        if model_type == 'random_forest':
            model = RandomForestClassifier(random_state=self.random_state)
            param_grid = {
                'classifier__n_estimators': [100, 200],
                'classifier__max_depth': [10, 20, None],
                'classifier__min_samples_split': [2, 5]
            }
        elif model_type == 'gradient_boosting':
            model = GradientBoostingClassifier(random_state=self.random_state)
            param_grid = {
                'classifier__n_estimators': [100, 200],
                'classifier__learning_rate': [0.01, 0.1],
                'classifier__max_depth': [3, 5]
            }
        elif model_type == 'logistic_regression':
            model = LogisticRegression(random_state=self.random_state, max_iter=1000)
            param_grid = {
                'classifier__C': [0.1, 1.0, 10.0]
            }
        else:
            raise ValueError(f"Unknown model type: {model_type}")

        # 파이프라인 구축
        pipeline = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('classifier', model)
        ])

        # 하이퍼파라미터 튜닝
        if hyperparameter_tuning:
            grid_search = GridSearchCV(
                pipeline, param_grid, cv=5, scoring='f1_weighted', n_jobs=-1
            )
            grid_search.fit(X_train, y_train)
            self.model = grid_search.best_estimator_
            print(f"Best parameters: {grid_search.best_params_}")
        else:
            self.model = pipeline
            self.model.fit(X_train, y_train)

        return self.model

    def evaluate(
        self,
        X_test: pd.DataFrame,
        y_test: np.ndarray
    ) -> dict:
        """
        모델 평가
        """
        y_pred = self.model.predict(X_test)

        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision_weighted': precision_score(y_test, y_pred, average='weighted'),
            'recall_weighted': recall_score(y_test, y_pred, average='weighted'),
            'f1_weighted': f1_score(y_test, y_pred, average='weighted')
        }

        # ROC-AUC (이진 분류)
        if len(np.unique(y_test)) == 2:
            y_proba = self.model.predict_proba(X_test)[:, 1]
            metrics['roc_auc'] = roc_auc_score(y_test, y_proba)

        print("\n=== Classification Report ===")
        print(classification_report(y_test, y_pred))

        print("\n=== Confusion Matrix ===")
        print(confusion_matrix(y_test, y_pred))

        return metrics

    def cross_validate(
        self,
        X: pd.DataFrame,
        y: np.ndarray,
        cv: int = 5
    ) -> dict:
        """
        교차 검증
        """
        pipeline = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('classifier', self.model.named_steps['classifier'])
        ])

        scores = cross_val_score(
            pipeline, X, y, cv=cv, scoring='f1_weighted'
        )

        return {
            'mean_f1': scores.mean(),
            'std_f1': scores.std(),
            'all_scores': scores
        }

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        새로운 데이터 예측
        """
        return self.model.predict(X)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        예측 확률
        """
        return self.model.predict_proba(X)


# 사용 예시
if __name__ == "__main__":
    from sklearn.datasets import load_breast_cancer

    # 데이터 로드
    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target

    # 파이프라인 생성
    pipeline = SupervisedLearningPipeline(
        target_column='target',
        problem_type='classification'
    )

    # 데이터 준비
    X_train, X_test, y_train, y_test = pipeline.prepare_data(df)

    # 모델 학습 (하이퍼파라미터 튜닝 포함)
    pipeline.train(X_train, y_train, model_type='random_forest', hyperparameter_tuning=True)

    # 평가
    metrics = pipeline.evaluate(X_test, y_test)
    print(f"\nMetrics: {metrics}")

    # 교차 검증
    cv_results = pipeline.cross_validate(df.drop(columns=['target']), df['target'])
    print(f"\nCross-Validation F1: {cv_results['mean_f1']:.4f} (+/- {cv_results['std_f1']:.4f})")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 분류 알고리즘 심층 비교

| 알고리즘 | 복잡도 | 해석성 | 과적합 위험 | 스케일링 필요 | 용도 |
|:---|:---|:---|:---|:---|:---|
| **로지스틱 회귀** | O(n×d) | 높음 | 낮음 | 필요 | 베이스라인 |
| **결정 트리** | O(n×d×log n) | 높음 | 높음 | 불필요 | 규칙 추출 |
| **Random Forest** | O(n×d×k) | 중간 | 낮음 | 불필요 | 일반적 |
| **XGBoost** | O(n×d×k×log n) | 낮음 | 중간 | 불필요 | 경진대회 |
| **SVM** | O(n²~n³) | 낮음 | 중간 | 필수 | 소규모 |
| **신경망** | O(n×d×h×l) | 낮음 | 높음 | 필수 | 복잡한 패턴 |

#### 2. 학습 패러다임 비교

| 패러다임 | 데이터 요구 | 라벨 필요 | 장점 | 단점 |
|:---|:---|:---|:---|:---|
| **지도 학습** | 중간~높음 | **필수** | 명확한 목표, 평가 용이 | 라벨링 비용 |
| **비지도 학습** | 높음 | 불필요 | 패턴 발견, 라벨 불필요 | 평가 어려움 |
| **반지도 학습** | 중간 | 일부 | 라벨 비용 절감 | 노이즈 민감 |
| **자기 지도 학습** | 높음 | 자동 생성 | 대규모 사전학습 | pretext task 설계 |
| **강화 학습** | 환경 | 보상 신호 | 순차적 의사결정 | 보상 설계 어려움 |

#### 3. 과목 융합 관점 분석

*   **[지도 학습 + 데이터베이스]**:
    피처 스토어(Feature Store)에서 전처리된 특성을 조회하여 모델 학습. 실시간 추론을 위한 특성 서빙.

*   **[지도 학습 + MLOps]**:
    모델 버전 관리, 자동 재학습(Data Drift 감지), A/B 테스트 배포. 지속적 모니터링.

*   **[지도 학습 + 클라우드]**:
    AutoML 서비스(Google Vertex AI, AWS SageMaker)로 하이퍼파라미터 자동 튜닝, 분산 학습.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단: 실무 시나리오

**시나리오 A: 신용카드 사기 탐지**
*   **상황**: 일일 100만 건 거래, 사기 0.1%, 실시간 탐지 필요
*   **기술사 판단**:
    1.  **문제 정의**: 이진 분류 (정상/사기)
    2.  **불균형 처리**: SMOTE 오버샘플링, 가중치 조정
    3.  **모델 선택**: XGBoost (정밀도+속도 균형)
    4.  **평가 지표**: Precision@k, Recall 중심 (사기 놓치면 치명적)
    5.  **임계값**: False Positive < 1% 조건에서 Recall 최대화

**시나리오 B: 고객 이탈 예측**
*   **상황**: 통신사 100만 고객, 이탈률 5%, 이탈 고객 예측
*   **기술사 판단**:
    1.  **특성**: 통화량, 데이터 사용량, 요금, CS 접촉 이력
    2.  **모델**: Random Forest + SHAP (설명 가능성)
    3.  **평가**: ROC-AUC, 이익 곡선(Lift Curve)
    4.  **액션**: 상위 10% 위험 고객에게 리텐션 캠페인

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **라벨 품질**: 라벨링 오류는 모델 성능의 상한 결정
- [ ] **불균형 처리**: 소수 클래스 전략 (오버/언더샘플링, 가중치)
- [ ] **과적합 방지**: 교차 검증, 정규화, Early Stopping
- [ ] **특성 중요도**: 어떤 특성이 예측에 기여하는지 파악
- [ ] **지속적 모니터링**: Data Drift, Concept Drift 감지

#### 3. 안티패턴 (Anti-patterns)

*   **안티패턴 1: Data Leakage**: 테스트 데이터 정보가 학습에 노출. 시간 기반 분할 필수.
*   **안티패턴 2: 불균형 무시**: 정확도만 보고 99%라며 좋아함 → 소수 클래스 완전 무시.
*   **안티패턴 3: 과도한 특성**: 특성 1000개인데 샘플 1000개. 차원의 저주.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 기존 방식 (Rule-based) | 지도 학습 | 향상 지표 |
|:---|:---|:---|:---|
| **사기 탐지** | 60% Recall | 95% Recall | +35% |
| **이탈 예측** | 정확도 70% | 정확도 90% | +20% |
| **품질 검사** | 인간 92% | AI 99% | +7% |
| **처리 속도** | 100건/시간 | 10,000건/초 | 36,000배 |

#### 2. 미래 전망 및 진화 방향

**단기 (2024~2026)**:
- **AutoML 대중화**: 코딩 없이 모델 개발 가능
- **Few-shot Learning**: 적은 라벨로도 높은 성능

**중기 (2027~2030)**:
- **Foundation Models**: 사전 학습된 대형 모델 파인튜닝
- **멀티모달 지도 학습**: 이미지+텍스트+오디오 결합

**장기 (2030~)**:
- **자동 데이터 라벨링**: AI가 스스로 라벨 생성 및 검증
- **실시간 적응형 학습**: 데이터 변화에 즉시 적응

#### 3. 참고 표준 및 가이드라인

*   **CRISP-DM**: 데이터 마이닝 프로세스 표준
*   **Scikit-learn API**: Python ML 라이브러리 표준
*   **MLflow**: 모델 관리 및 추적 표준

---

### 📌 관련 개념 맵 (Knowledge Graph)

*   **[비지도 학습](@/studynotes/10_ai/02_ml/unsupervised_learning.md)**: 라벨 없이 패턴 학습
*   **[분류 알고리즘](@/studynotes/10_ai/02_ml/classification_algorithms.md)**: 로지스틱, SVM, 트리 기반
*   **[회귀 알고리즘](@/studynotes/10_ai/02_ml/regression_algorithms.md)**: 선형 회귀, Ridge, Lasso
*   **[앙상블 학습](@/studynotes/10_ai/02_ml/ensemble_learning.md)**: 배깅, 부스팅, 스태킹
*   **[모델 평가](@/studynotes/10_ai/02_ml/model_evaluation.md)**: 교차 검증, 평가 지표

---

### 👶 어린이를 위한 3줄 비유 설명

1.  **정답이 있는 문제집**: 지도 학습은 정답이 적혀 있는 문제집으로 공부하는 것과 같아요. 문제와 정답을 보면서 푸는 법을 배워요.
2.  **선생님이 옆에**: 선생님이 "이건 이렇게 푸는 거야" 하고 가르쳐주는 것처럼, 컴퓨터도 정답을 보면서 배워요.
3.  **시험은 정답 없이**: 공부를 다 하면 정답이 없는 새로운 문제도 풀 수 있게 돼요. 이게 바로 AI가 스팸 메일을 찾아내는 방법이에요!
