+++
weight = 121
title = "지도 학습 (Supervised Learning)"
date = "2024-05-22"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
1. **정답(Label)이 포함된 학습 데이터**를 통해 입력(X)과 출력(Y) 간의 매핑 함수(Mapping Function)를 도출하는 기계학습 방법론이다.
2. 결과값의 특성에 따라 연속적인 수치를 예측하는 **회귀(Regression)**와 불연속적인 범주를 구분하는 **분류(Classification)**로 나뉜다.
3. 데이터 엔지니어링 관점에서 고품질의 **라벨링된 데이터셋(Labeled Dataset)** 확보와 피처 엔지니어링(Feature Engineering)이 모델 성능의 핵심이다.

---

### Ⅰ. 개요 (Context & Background)
기계학습(Machine Learning)의 가장 대표적인 유형으로, 입력 데이터와 그에 대응하는 명확한 정답(Ground Truth)을 쌍으로 제공하여 모델을 훈련시킨다. 이는 마치 학생이 문제와 해답지가 있는 문제집으로 공부하는 것과 유사하며, 명확한 목표값이 존재하므로 예측 성능 평가(Accuracy, MSE 등)가 직관적이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
지도 학습은 훈련 단계(Training Phase)에서 오차(Loss)를 최소화하는 방향으로 가중치(Weights)를 업데이트하고, 추론 단계(Inference Phase)에서 미지의 데이터에 대해 결과를 예측한다.

```text
[ Supervised Learning Workflow / 지도 학습 워크플로우 ]

    +-------------------+       +-----------------------+
    |  Labeled Dataset  |       |  Training Algorithm   |
    | (Features, Label) | ----> | (Gradient Descent...) |
    +---------+---------+       +-----------+-----------+
              |                             |
              v                             v
    +---------+---------+       +-----------+-----------+
    |   Input (X)       | ----> |  Model Function (f)   | ----> Prediction (Y')
    +-------------------+       +-----------+-----------+
                                            |
                                            v
                                +-----------+-----------+
                                |  Loss Function (L)    | <--- Compare (Y, Y')
                                +-----------------------+
```

1. **학습 알고리즘**: 경사 하강법(Gradient Descent)을 통해 손실 함수를 최소화하는 최적의 파라미터를 탐색한다.
2. **범주**:
   - **분류(Classification)**: Binary(이진), Multi-class(다중), Multi-label 분류. (예: 스팸 여부, 숫자 인식)
   - **회귀(Regression)**: 선형 회귀, 다항 회귀 등. (예: 주택 가격 예측, 매출 전망)

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 분류 (Classification) | 회귀 (Regression) |
| :--- | :--- | :--- |
| **출력값 형태** | 이산적 (Discrete) / 범주형 | 연속적 (Continuous) / 수치형 |
| **핵심 목표** | 데이터가 속한 클래스 결정 | 입력 변수 간의 상관관계 및 수치 도출 |
| **평가 지표** | Accuracy, Precision, Recall, F1-Score | MSE, RMSE, MAE, R-Squared |
| **대표 알고리즘** | SVM, Random Forest, Logistic Regression | Linear Regression, Lasso, Ridge |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
1. **데이터 품질(Data Quality)**: "Garbage In, Garbage Out". 라벨링 오류(Mislabeled)는 모델 성능을 직접적으로 저하시키므로 데이터 클렌징과 QA 공정이 필수적이다.
2. **과적합(Overfitting) 관리**: 훈련 데이터에만 과도하게 최적화되어 일반화 성능이 떨어지는 것을 막기 위해 규제(Regularization)와 교차 검정(Cross Validation)을 적용해야 한다.
3. **PE 관점의 판단**: 실무에서는 라벨링 비용이 매우 높으므로, 초기에는 적은 양의 데이터로 지도 학습을 수행하고 이후 능동 학습(Active Learning)이나 준지도 학습(Semi-supervised Learning)으로 확장하는 전략이 효율적이다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
지도 학습은 이미 이미지 인식, 음성 번역, 질병 진단 등 다양한 분야에서 인간 수준의 성능을 입증했다. 향후에는 초거대 모델(Foundation Model)을 활용한 미세 조정(Fine-tuning) 전략이 주류가 될 것이며, 데이터 엔지니어는 대규모 데이터 파이프라인 자동화와 라벨링 효율화를 통해 AI의 경제성을 확보해야 한다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: Machine Learning (기계학습)
- **하위 개념**: Linear Regression, Support Vector Machine, Decision Tree, Neural Networks
- **연관 개념**: Loss Function, Overfitting, Labeling, Feature Engineering

---

### 👶 어린이를 위한 3줄 비유 설명
1. 사과 사진 밑에 '사과'라고 적힌 카드로 공부하는 것과 같아요.
2. 나중에 글자가 없는 사과 사진만 봐도 "이건 사과야!"라고 맞힐 수 있게 돼요.
3. 선생님(정답)이 옆에서 틀린 걸 바로바로 고쳐주는 공부법이에요.
