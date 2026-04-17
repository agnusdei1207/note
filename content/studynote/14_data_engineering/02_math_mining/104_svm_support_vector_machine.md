+++
weight = 104
title = "서포트 벡터 머신 (SVM, Support Vector Machine)"
date = "2024-05-22"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
- **마진 극대화(Margin Maximization):** 두 클래스 사이의 거리를 최대한 벌려주는 결정 경계(Hyperplane)를 찾아 일반화 성능을 극대화함.
- **커널 트릭(Kernel Trick):** 저차원에서 해결 불가능한 비선형 문제를 고차원으로 투영(Mapping)하여 선형적으로 분리해내는 수학적 마법임.
- **서포트 벡터 활용:** 경계 근처의 핵심 데이터(Support Vector)들만 사용하여 모델을 구축하므로, 데이터가 적고 고차원인 경우에도 매우 강력함.

### Ⅰ. 개요 (Context & Background)
1. **강력한 결정론적 분류:** 로지스틱 회귀가 확률에 기반한다면, SVM은 기하학적인 경계를 찾아내는 결정론적(Deterministic) 방식임.
2. **이상치에 강함:** 결정 경계에서 멀리 떨어진 데이터는 모델 학습에 영향을 주지 않으므로, 데이터 노이즈에 비교적 강건(Robust)함.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **SVM Core Concept & Structural Design**
```text
[ Feature Space (2D) ]             [ Kernel Mapping (3D) ]
      o   o  |  x   x                    |   (Non-linear to Linear)
    o   o    |    x   x                  |  _----_
 o      (Margin)      x                / / x  x \ \
 o <----- d ------> x                 | |  o  o  | |
    o   o    |    x   x                  \ \_----_/ /
      o   o  |  x   x                    |
[ Support Vectors & Hyperplane ]

1. Hyperplane (결정 초평면): f(x) = w·x + b = 0
2. Margin (마진): 초평면에서 가장 가까운 데이터(서포트 벡터)까지의 거리. 2/||w||
3. Support Vectors: 결정 경계를 정의하는 가장 외곽의 데이터 포인트들.
```

1. **소프트 마진(Soft Margin)과 하드 마진(Hard Margin):**
   - **Hard Margin:** 완벽한 분리를 추구함(과적합 위험).
   - **Soft Margin:** 약간의 오분류(Slack Variable)를 허용하여 마진을 더 크게 가져감. 파라미터 C를 통해 규제 강도를 조절함.
2. **커널 트릭 (Kernel Trick):**
   - 직선으로 나눌 수 없는(Non-linear) 데이터를 고차원(Infinite dimension)으로 보내어 선형 분리가 가능하도록 함.
   - 실제로 모든 데이터를 고차원으로 변환하면 계산량이 폭증하지만, 커널 함수(RBF, Polynomial)를 사용해 변환 없이 내적(Dot Product) 값만 계산함으로써 연산 효율 확보.
3. **최적화 문제:** 라그랑주 승수법(Lagrange Multipliers)을 통해 목적 함수를 최소화하는 Quadratic Programming 문제로 치환하여 해를 구함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | SVM (Linear/RBF) | Random Forest (Ensemble) | Neural Network (Deep Learning) |
| :--- | :--- | :--- | :--- |
| **작동 원리** | 기하학적 마진 극대화 | 의사결정 나무의 다수결 | 가중치 연쇄 업데이트 |
| **데이터 크기** | 소규모/중규모에 강함 | 대규모 정형 데이터 유리 | 대규모 비정형 데이터(이미지/음성) |
| **파라미터** | C (규제), Gamma (커널 곡률) | 나무 개수, 깊이 | 레이어 수, 학습률 등 |
| **비선형 처리** | 커널 트릭 (수학적 전개) | 계층적 분기 (조건문) | 비선형 활성화 함수 (ReLU 등) |
| **해석 가능성** | 낮음 (블랙박스 성격) | 보통 (Feature Importance) | 매우 낮음 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
1. **데이터 스케일링 필수:** SVM은 데이터 간의 거리(Distance)를 계산하므로, 특정 변수의 단위가 크면 모델이 왜곡됨. 반드시 정규화/표준화 전처리가 선행되어야 함.
2. **기술사적 판단:** SVM은 고차원 텍스트 데이터(예: 스팸 분류, 문서 카테고리화)에서 매우 높은 효율을 보임. 딥러닝이 부담스러운 중소규모 데이터셋에서는 성능과 속도의 최적 지점을 제공하므로, 상시 Baseline 모델군에 포함시켜야 함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
1. **기대효과:** 마진 극대화를 통해 알려지지 않은 미래 데이터(Unseen Data)에 대한 뛰어난 예측 안정성(Generalization Power)을 보장함.
2. **결론:** SVM은 통계학적 엄밀함과 기하학적 통찰이 융합된 알고리즘이며, 커널 트릭이라는 혁신적인 개념을 통해 비선형 세계를 선형적으로 해석할 수 있게 해준 데이터 분석의 필수 고전임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 지도 학습 (Supervised Learning), 분류 (Classification)
- **하위 개념:** 결정 초평면 (Hyperplane), 커널 트릭 (RBF Kernel)
- **연관 개념:** 라그랑주 승수법, 소프트 마진 (Soft Margin)

### 👶 어린이를 위한 3줄 비유 설명
- **하드 마진:** 우리 팀과 상대 팀 사이에 절대로 넘어오지 못하게 아주 튼튼한 울타리를 치는 거예요.
- **커널 트릭:** 평면에서는 섞여 있는 구슬들을 공중으로 휙 던져서(3D), 위아래로 나누는 마법 종이를 끼워 넣는 것과 같아요.
- **결론:** 양쪽 팀에서 가장 힘센 선수(서포트 벡터)들이 서로 멀리 떨어지도록 가운데에 선을 긋는 시합이랍니다.
