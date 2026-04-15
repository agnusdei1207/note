+++
weight = 102
title = "회귀 라쏘 (Lasso) 및 릿지 (Ridge) 규제 (Regularization)"
date = "2024-05-22"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
- **과적합 방지(Anti-Overfitting):** 모델의 가중치(Coefficient) 크기에 패널티를 부여하여 복잡도를 제어하고 일반화 성능을 극대화함.
- **L1 Lasso vs L2 Ridge:** Lasso는 불필요한 변수를 0으로 만들어 변수 선택 효과를 제공하며, Ridge는 가중치를 작게 유지하여 다중공선성을 완화함.
- **편향-분산 트레이드오프:** 약간의 편향(Bias)을 허용하는 대신 분산(Variance)을 획기적으로 낮추어 실무 데이터의 노이즈에 강건한 모델을 구축함.

### Ⅰ. 개요 (Context & Background)
1. **정규화의 필요성:** 단순 선형 회귀(OLS)는 모든 독립변수를 활용하며 훈련 데이터에 완벽히 맞추려다 보니, 데이터의 노이즈까지 학습하여 실제 서비스 시 성능이 급락하는 과적합(Overfitting) 문제가 빈번함.
2. **비용 함수의 변형:** 오차 제곱합(RSS)만을 최소화하는 기존 방식에 가중치 절대값(L1) 또는 제곱(L2) 항을 추가하여 모델이 "너무 큰 가중치"를 갖지 못하도록 제약 조건을 부여함.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **Regularization Concept & Geometric Interpretation**
```text
[ Cost Function Structure ]
Loss = RSS(Residual Sum of Squares) + λ * Penalty(Weight)

1. Lasso (L1): Penalty = Σ|βj|  --> Diamond Shape Constraint Area
2. Ridge (L2): Penalty = Σβj²   --> Circular Shape Constraint Area

[ Geometric Intuition (기하학적 해석) ]
  Lasso Constraint (L1)          Ridge Constraint (L2)
       |   /                         |   /
     --+--+-- β1                   --+--+-- β1
       | /                           | /
  (Diamond hits axis)          (Circle hits smoothly)
  Variable Selection Effect     Weights Shrinkage (No Zero)
```

1. **Lasso (Least Absolute Shrinkage and Selection Operator):**
   - 패널티 항으로 가중치의 절대값 합을 사용함.
   - 제약 조건 영역이 다이아몬드 형태의 각진 구조를 가져, 최적점이 축(Axis) 위에서 형성될 확률이 높음. 이 과정에서 일부 변수의 회귀 계수가 정확히 0이 되어 **자동 변수 선택(Feature Selection)** 기능 수행.
2. **Ridge (Tikhonov Regularization):**
   - 패널티 항으로 가중치의 제곱 합을 사용함.
   - 제약 조건 영역이 원형이며, 회귀 계수를 0에 가깝게 수축(Shrinkage)시키지만 완전히 0으로 만들지는 않음. **다중공선성(Multicollinearity)**이 있는 변수들 사이에서 가중치를 분산시켜 모델의 안정성 확보.
3. **Hyperparameter λ (Lambda):**
   - λ가 0이면 일반 선형 회귀와 동일하며, λ가 커질수록 규제가 강해져 모델이 단순해짐(Underfitting 위험).

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | Lasso Regression (L1) | Ridge Regression (L2) | Elastic Net (융합) |
| :--- | :--- | :--- | :--- |
| **패널티 항** | L1 Norm (절대값 합) | L2 Norm (제곱 합) | L1 + L2 혼합 |
| **변수 선택** | 가능 (계수를 0으로 만듦) | 불가능 (계수를 축소만 함) | 가능 (상관관계 변수 그룹화) |
| **해결 문제** | 불필요한 변수 제거 | 다중공선성(변수 간 상관) 완화 | Lasso+Ridge 단점 보완 |
| **미분 가능성** | 0에서 미분 불가 (좌표 하강법) | 모든 구간 미분 가능 | 혼합 형태 |
| **데이터 특성** | 중요한 변수가 소수일 때 유리 | 변수가 많고 서로 상관될 때 유리 | 변수가 매우 많은 고차원 데이터 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
1. **모델 선택 전략 (Decision Strategy):**
   - 분석 결과의 **설명력(Interpretability)**이 중요하다면 Lasso를 사용하여 핵심 변수만 추려내는 것이 유리함.
   - 데이터에 독립변수가 많고 서로 밀접하게 연관되어 있어 **예측 안정성**이 최우선이라면 Ridge를 권장함.
2. **기술사적 판단:** 현대 데이터 엔지니어링에서 규제 모델은 선택이 아닌 필수임. 특히 파라미터가 수만 개인 딥러닝에서도 Weight Decay라는 이름의 Ridge 규제가 기본 탑재됨. 실무에서는 교차 검증(Cross Validation)을 통해 최적의 λ와 α(Elastic Net 비율)를 찾는 파이프라인 자동화가 핵심임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
1. **기대효과:** 복잡한 현실 데이터에서 일반화 성능(Generalization)을 확보하여 프로덕션 배포 시 예측 성능의 변동성을 최소화함.
2. **결론:** Lasso와 Ridge는 선형 모델의 한계를 극복하는 수학적 도구이며, 이를 통해 데이터 엔지니어는 고차원 데이터(High Dimensional Data) 환경에서도 신뢰할 수 있는 예측 모델을 설계할 수 있는 근간을 마련함.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 선형 회귀(Linear Regression), 과적합(Overfitting)
- **하위 개념:** 좌표 하강법(Coordinate Descent), 다중공선성(Multicollinearity)
- **연관 개념:** 엘라스틱 넷(Elastic Net), 편향-분산 트레이드오프(Bias-Variance Tradeoff)

### 👶 어린이를 위한 3줄 비유 설명
- **Lasso:** 너무 많은 가방을 들고 가기 힘들어서, 정말 중요한 물건만 남기고 나머지 가방은 아예 버려버리는 똑똑한 정리왕이에요.
- **Ridge:** 모든 가방을 다 들고 가되, 가방 안의 짐을 골고루 조금씩 덜어내서 전체 무게를 가볍게 만드는 균형 잡기 선수예요.
- **결론:** 둘 다 모델이 너무 욕심부려서(과적합) 무거워지는 걸 막아주는 다이어트 선생님이랍니다.
