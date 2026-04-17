+++
weight = 108
title = "지니 불순도 (Gini Impurity)"
date = "2024-03-23"
[extra]
categories = "studynote-dataengineering"
+++

## 핵심 인사이트 (3줄 요약)
- 결정 트리(Decision Tree)에서 노드 분할의 기준이 되는 지표로, 데이터 집합의 통계적 이질성을 측정한다.
- 불순도가 0일 때 가장 순수한 상태(한 클래스만 존재)이며, 각 클래스의 확률 제곱 합을 1에서 빼서 계산한다.
- 엔트로피(Entropy) 대비 계산 복잡도가 낮아 CART(Classification and Regression Trees) 알고리즘의 기본 지표로 널리 활용된다.

### Ⅰ. 개요 (Context & Background)
- **정의**: 데이터 집합 내에서 서로 다른 클래스가 얼마나 섞여 있는지를 나타내는 척도이다.
- **배경**: 결정 트리는 데이터를 가장 잘 분류할 수 있는 '질문'을 찾아가며 성장한다. 이때 '가장 잘 분류한다'는 것은 분할 후 자식 노드들의 불순도가 최소화(정보 이득 최대화)되는 지점을 찾는 것을 의미한다.
- **수식**: $G = 1 - \sum_{i=1}^{c} (p_i)^2$ (여기서 $p_i$는 해당 집단 내 클래스 $i$의 비율)

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **작동 원리**:
  1. 현재 노드의 지니 불순도를 계산한다.
  2. 가능한 모든 분할 조건에 대해 자식 노드들의 가중 평균 지니 불순도를 계산한다.
  3. 분할 전후의 불순도 차이(Gini Gain)가 가장 큰 조건을 선택하여 분리한다.

```text
[ Gini Impurity Decision Process ]

      [Root Node]
    (Gini: 0.5, A:50, B:50)
           |
    < Split Condition? >
    /              \
 [Left Node]     [Right Node]
 (Gini: 0.1)     (Gini: 0.1)
 (A:45, B:5)     (A:5, B:45)
      |               |
   Purest <------- Purest
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 지니 불순도 (Gini Impurity) | 엔트로피 (Entropy / Information Gain) |
| :--- | :--- | :--- |
| **핵심 수식** | $1 - \sum p_i^2$ | $-\sum p_i \log_2(p_i)$ |
| **계산 속도** | 빠름 (단순 제곱 연산) | 상대적으로 느림 (로그 연산 포함) |
| **사용 알고리즘** | CART (Classification and Regression Trees) | ID3, C4.5, C5.0 |
| **분할 경향** | 가장 빈도가 높은 클래스를 격리하는 경향 | 조금 더 균형 잡힌 트리를 만드는 경향 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **성능 최적화**: 지니 불순도는 로그 연산이 없어 대규모 데이터셋에서 결정 트리를 생성할 때 속도 측면에서 유리하다.
- **과적합(Overfitting) 주의**: 불순도만 계속 낮추려다 보면 트리가 너무 깊어져 과적합이 발생할 수 있으므로, `max_depth`나 `min_samples_split` 같은 가지치기(Pruning) 전략과 병행해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- 지니 불순도는 기계 학습의 가장 직관적이고 강력한 분류 기준 중 하나로 자리 잡았다. 현재 랜덤 포레스트(Random Forest)나 XGBoost, LightGBM 같은 앙상블 모델 내부에서도 변수 중요도(Feature Importance)를 산출하는 핵심 근거로 사용되며, 모델의 해석 가능성(Explainability)을 높이는 데 기여하고 있다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: 결정 트리(Decision Tree), 정보 이론(Information Theory)
- **자식 개념**: CART 알고리즘, 변수 중요도(Feature Importance)
- **연관 개념**: 엔트로피(Entropy), 정보 이득(Information Gain), 가지치기(Pruning)

### 👶 어린이를 위한 3줄 비유 설명
- 빨간 사탕과 파란 사탕이 섞인 상자에서 사탕을 하나 꺼낼 때, 무슨 색인지 맞히기 어려운 정도를 말해요.
- 사탕들이 골고루 섞여 있으면 "불순도가 높다"고 하고, 한 가지 색만 있으면 "불순도가 0(순수하다)"이라고 해요.
- 인공지능은 이 상자를 잘 나눠서, 사탕 색깔을 맞히기 쉬운 "순수한 상자"들로 만드는 연습을 한답니다.
