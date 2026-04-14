+++
weight = 119
title = "앙상블 조합 보팅 (Ensemble Voting Methods)"
date = "2024-03-23"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
- 앙상블 보팅은 여러 개의 독립적인 모델(분류기)의 예측 결과를 결합하여 개별 모델보다 더 높은 정확도와 안정성을 얻는 기법이다.
- 예측 결과의 단순 빈도수를 계산하는 하드 보팅(Hard Voting)과 모델의 예측 확률 평균을 사용하는 소프트 보팅(Soft Voting)으로 구분된다.
- 모델 간의 낮은 상관관계(Diversity)가 앙상블 효과 극대화의 핵심이며, 이는 모델의 분산(Variance)을 줄여 과적합(Overfitting)을 방지한다.

### Ⅰ. 개요 (Context & Background)
머신러닝에서 하나의 '만능 모델'을 찾는 것은 매우 어렵다. 하지만 여러 개의 '어느 정도 똑똑한 모델'들을 모아 집단 지성을 활용하면 개별 모델의 편향이나 오류를 서로 보완할 수 있다. **앙상블 보팅(Ensemble Voting)**은 이러한 '다수결 원칙'을 알고리즘화한 것으로, 배깅(Bagging)이나 부스팅(Boosting)과 같은 특정 방식에 얽매이지 않고 서로 다른 유형의 알고리즘(예: KNN + SVM + Random Forest)을 결합할 수 있는 유연한 프레임워크다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
보팅은 크게 두 가지 메커니즘으로 나뉜다. 하드 보팅은 '투표수'에 집중하고, 소프트 보팅은 '확신의 정도(확률)'에 가중치를 둔다.

```text
[ Ensemble Voting Architecture: Hard vs Soft ]
(앙상블 보팅 아키텍처: 하드 vs 소프트 방식)

      +-------------+     +-------------+     +-------------+
      | Classifier A|     | Classifier B|     | Classifier C|
      +------+------+     +------+------+     +------+------+
             |                   |                   |
    [Output: Class 1]   [Output: Class 2]   [Output: Class 1]
             |                   |                   |
             +---------+---------+---------+---------+
                       |
        +--------------v--------------+
        |        Voting Layer         |
        +--------------+--------------+
                       |
   [Hard Voting]       |      [Soft Voting]
   Count Labels:       |      Avg Probabilities:
   Class 1: 2 votes    |      Class 1: (0.9+0.4+0.8)/3 = 0.7
   Class 2: 1 vote     |      Class 2: (0.1+0.6+0.2)/3 = 0.3
   Winner: Class 1     |      Winner: Class 1 (0.7)
```

1. **하드 보팅 (Majority Voting):** 각 분류기가 예측한 클래스 중 가장 많이 선택된 클래스를 최종 예측값으로 결정한다.
2. **소프트 보팅 (Probability Voting):** 각 분류기가 예측한 클래스별 확률을 합산하여 평균을 내고, 가장 높은 평균 확률을 가진 클래스를 선택한다. 일반적으로 하드 보팅보다 성능이 뛰어나 권장된다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 하드 보팅 (Hard Voting) | 소프트 보팅 (Soft Voting) | 가중치 보팅 (Weighted Voting) |
| :--- | :--- | :--- | :--- |
| **결합 기준** | 최종 라벨 (Label) | 예측 확률 (Probability) | 모델 성능별 가중치 |
| **적용 시점** | 확률 출력이 불가능할 때 | 대부분의 분류 문제 (권장) | 특정 모델 신뢰도가 높을 때 |
| **특징** | 다수결 기반, 안정적 | 모델의 확신도를 반영함 | 고성능 모델의 목소리를 키움 |
| **수학적 관점** | Mode (최빈값) | Mean (산술 평균) | Weighted Average |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
**실무적 판단 (Technical Insight):**
앙상블의 성능을 높이려면 개별 모델들이 서로 다른 오류를 범해야 한다. 즉, 상관관계가 낮은 모델들을 섞는 것이 유리하다.
- **Diversity Strategy:** 선형 모델(Logistic Regression), 비선형 모델(SVM), 트리 모델(XGBoost)을 섞어 각 알고리즘이 보지 못하는 데이터의 측면을 보완하게 한다.
- **Kaggle & Competition:** 소수점 차이의 정밀도를 다투는 경진대회에서 최종 모델은 거의 항상 다수의 상위 모델을 소프트 보팅으로 묶은 형태를 띤다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
앙상블 보팅은 개별 알고리즘의 한계를 집단 지성으로 극복하는 가장 직관적이고 강력한 방법이다. 모델의 복잡도를 무작정 높이는 것보다, 검증된 여러 모델의 조화로운 결합이 실무에서 더 높은 신뢰성을 보장한다. 인공지능이 복잡해질수록 단일 거대 모델보다는 각 분야에 특화된 소규모 모델들의 보팅이나 라우팅(Routing)을 통한 의사결정 체계가 더욱 주목받을 것이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념:** Ensemble Learning
- **유사 개념:** Bagging (Parallel), Boosting (Sequential), Stacking (Meta-model)
- **하위 개념:** Wisdom of the Crowd, Probability Calibration

### 👶 어린이를 위한 3줄 비유 설명
- 친구 3명에게 "저 간판에 쓰인 글자가 뭐야?"라고 물어보는 것과 같아요.
- 2명이 "사과"라고 하고 1명이 "포도"라고 하면 "사과"라고 믿는 게 하드 보팅이에요.
- 친구들이 "난 90% 사과 같아"라고 확신까지 말해주면 그걸 다 합쳐서 결정하는 게 소프트 보팅이에요!
