+++
weight = 65
title = "회귀 (Regression)"
date = "2026-03-04"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **핵심 정의**: 하나 이상의 독립 변수($x$)와 종속 변수($y$) 사이의 상관관계를 수치적인 함수로 모델링하여 연속적인 값을 예측하는 기법이다.
> 2. **방법론**: 선형 회귀(Linear Regression)를 기본으로 하며, 손실 함수(MSE 등)를 최소화하도록 가중치($W$)와 편향($b$)을 최적화하는 과정을 거친다.
> 3. **활용 가치**: 매출 예측, 주가 전망, 수요 예측 등 수치 데이터의 흐름과 경향성을 파악해야 하는 비즈니스 핵심 의사결정에 광범위하게 사용된다.

---

### Ⅰ. 개요 (Context & Background)
회귀(Regression)라는 용어는 통계학자 Francis Galton이 "부모의 키가 커도 자녀의 키는 결국 전체 평균으로 회귀하려 한다"는 현상을 발견한 것에서 유래했다. 현대 머신러닝에서 회귀는 데이터를 가장 잘 설명하는 **'최적의 선(Best Fit Line)'** 혹은 곡선을 찾는 과정을 의미한다. 분류(Classification)가 '어떤 그룹인가'를 묻는다면, 회귀는 '얼마나 많은가' 또는 '값이 무엇인가'를 다룬다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
  [Data Points & Regression Line]       [Core Formula]
                                         y = Wx + b + ε
    Y |        .  * (Error/Residual)
      |     . /                          - y: Dependent Var (Target)
      |    . /                           - x: Independent Var (Feature)
      |   / .                            - W: Weight (Slope)
      |  /  .                            - b: Bias (Intercept)
      | / .                              - ε: Error Term
      └────────────────── X

  [Optimization Process]
  1. Prediction  : Compute y_hat = Wx + b
  2. Loss Calc   : MSE = (1/n) * Σ(y - y_hat)^2
  3. Optimizer   : Gradient Descent to Update W, b
```

**핵심 알고리즘:**
1. **단순 선형 회귀 (Simple Linear Regression):** 한 개의 독립 변수와 한 개의 종속 변수의 관계.
2. **다중 선형 회귀 (Multiple Linear Regression):** 여러 개의 독립 변수를 사용하여 복합적인 원인을 분석.
3. **로지스틱 회귀 (Logistic Regression):** 이름은 회귀이지만, S자 곡선(Sigmoid)을 활용하여 이진 분류에 사용되는 특수한 경우.
4. **릿지/라쏘 회귀 (Ridge/Lasso):** 과적합을 방지하기 위해 규제(Penalty) 항을 추가한 형태.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구분 | 회귀 (Regression) | 분류 (Classification) |
|:---|:---|:---|
| **출력값 형태** | **연속형 (Continuous)** | **범주형 (Discrete/Labels)** |
| **대표 평가지표** | **MSE, RMSE, R-squared, MAE** | Accuracy, Precision, Recall, F1 |
| **주요 사례** | 온도 예측, 주식 가격, 배달 시간 | 스팸 판별, 질병 진단, 이미지 인식 |
| **손실 함수** | Mean Squared Error (평균 제곱 오차) | Cross Entropy (크로스 엔트로피) |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
회귀 분석 실무에서 가장 경계해야 할 것은 **'상관관계와 인과관계를 혼동하는 것'**이다. 통계적으로 상관관계가 높다고 해서 반드시 인과관계가 성립하는 것은 아니기 때문이다. 기술사적 관점에서는 모델의 예측력($R^2$)뿐만 아니라 잔차(Residual) 분석을 통해 오차가 무작위성을 띠는지 확인해야 한다. 또한 피처들 간의 다중공선성이 높으면 회귀 계수(Weight)가 불안정해지므로 VIF 지수를 점검하거나 규제 모델(Ridge, Lasso)을 적용하는 것이 필수적이다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
회귀는 고전 통계학에서 딥러닝(신경망의 선형 결합)에 이르기까지 모든 AI 알고리즘의 근간이 된다. 특히 최근에는 설명 가능한 AI(XAI)의 중요성이 커지면서, 복잡한 딥러닝 모델 대신 해석이 용이한 회귀 기반의 대리 모델(Surrogate Model)을 활용하는 사례가 늘고 있다. 데이터의 연속성을 이해하고 예측하는 회귀 기술은 자율주행의 경로 예측, 스마트 팩토리의 수명 예측 등 정밀 제어 분야에서 계속해서 진화할 것이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **최적화 기법**: 최소제곱법 (Ordinary Least Squares), 경사 하강법
- **평가 지표**: 결정 계수 (R-squared), MAE, RMSE
- **심화 모델**: Polynomial Regression, Generalized Linear Model (GLM)

---

### 👶 어린이를 위한 3줄 비유 설명
1. 회귀는 흩어져 있는 점들을 보고 **'가장 잘 어울리는 줄'**을 긋는 놀이예요.
2. 어제와 오늘 공부한 시간을 보고 내일 시험 점수가 몇 점일지 **수치로 맞히는 것**이죠.
3. 점들이 선에 딱 달라붙어 있을수록, 우리가 그은 선이 정답에 가깝다는 뜻이랍니다!
