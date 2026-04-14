+++
weight = 10066
title = "분류 (Classification)"
date = "2026-03-04"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **핵심 정의**: 주어진 데이터를 미리 정의된 여러 개의 클래스(범주) 중 하나로 나누는 지도 학습의 대표적인 기법이다.
> 2. **방법론**: 데이터의 특징(Features)을 분석하여 최적의 결정 경계(Decision Boundary)를 찾고, 이를 기준으로 새로운 데이터의 라벨을 예측한다.
> 3. **활용 가치**: 스팸 메일 판별, 질병 유무 진단, 이미지 내 사물 인식 등 일상생활과 산업 현장에서 가장 빈번하게 발생하는 '결정 문제'를 자동화한다.

---

### Ⅰ. 개요 (Context & Background)
분류(Classification)는 인간이 지능을 발휘하는 가장 기본적인 방식 중 하나인 '범주화'를 컴퓨터가 수행하도록 만든 것이다. 머신러닝의 분류 모델은 수많은 정답 데이터를 학습하여, 보지 못한 새로운 데이터가 들어왔을 때 그것이 A그룹인지 B그룹인지 확률적으로 판단한다. 결과값이 연속적인 수치인 회귀와 달리, 분류는 **'이산적인 라벨'**을 출력한다는 점이 가장 큰 차이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
  [Input Data Points]          [Decision Boundary]         [Final Labels]
                                (Separation Logic)          (A or B Class)
    Y |    Class A                Y |     \ Class A            Group: Red (A)
      |   (o o o)                   |   o o\  o                Group: Blue (B)
      |     (o)                     |   o o \ o
      |       (x x)                 |  ------\------- (Boundary)
      |      (x x x)                |     x x \x
      |      Class B                |    x x x \ Class B
      └─────────────── X            └─────────────── X

  [Binary vs Multi-class Classification]
  1. Binary (이진)      : Yes / No, Spam / Ham (2 Classes)
  2. Multi-class (다중) : Dog / Cat / Bird (N Classes)
```

**핵심 알고리즘:**
1. **로지스틱 회귀 (Logistic Regression):** 시그모이드 함수를 사용하여 0~1 사이의 확률값으로 분류.
2. **의사결정 나무 (Decision Tree):** 스무고개 방식으로 데이터를 분할하여 분류.
3. **서포트 벡터 머신 (SVM):** 클래스 간의 간격(Margin)을 최대화하는 최적의 경계를 탐색.
4. **나이브 베이즈 (Naive Bayes):** 베이즈 정리를 이용한 확률 기반 분류.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구분 | 분류 (Classification) | 군집화 (Clustering) |
|:---|:---|:---|
| **학습 방식** | **지도 학습 (Supervised)** | **비지도 학습 (Unsupervised)** |
| **정답 (Label)** | **필요함 (Pre-defined)** | 필요 없음 (Discover patterns) |
| **목표** | 미리 정해진 그룹에 배정 | 데이터 간 유사성으로 그룹 찾기 |
| **성능 측정** | Accuracy, Confusion Matrix | Silhouette Score, Elbow Method |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
분류 모델을 실무에 적용할 때 가장 중요한 기술사적 판단 기준은 **'데이터 불균형(Imbalanced Data)'** 처리다. 암 진단이나 사기 탐지(FDS)와 같이 특정 클래스가 매우 적은 경우, 정확도(Accuracy)만으로는 모델의 성능을 제대로 평가할 수 없다. 이때는 정밀도(Precision)와 재현율(Recall)의 조화 평균인 **F1-Score**를 핵심 지표로 삼아야 한다. 또한 결정 경계가 너무 복잡해져 발생하는 과적합(Overfitting)을 방지하기 위해 앙상블(Random Forest, XGBoost) 기법을 적극적으로 활용하는 것이 실무적 표준이다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
분류 기술은 단순한 스팸 필터를 넘어, 자율주행차의 보행자 인식, 의료 AI의 암세포 전이 판별 등 고난도 판단 영역으로 진화하고 있다. 최근에는 딥러닝 기반의 합성곱 신경망(CNN)이나 트랜스포머(Transformer) 아키텍처가 결합되면서 정밀도가 비약적으로 향상되었다. 앞으로는 단순한 분류를 넘어 '왜 그렇게 분류했는지'에 대한 근거를 제시하는 설명 가능성(Explainability)이 분류 모델의 핵심적인 경쟁력이 될 것이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **평가 도구**: 혼동 행렬 (Confusion Matrix), ROC 커브
- **알고리즘 확장**: 랜덤 포레스트 (Random Forest), 부스팅 (Boosting)
- **응용 분야**: 자연어 처리 (Sentiment Analysis), 컴퓨터 비전 (Image Tagging)

---

### 👶 어린이를 위한 3줄 비유 설명
1. 분류는 시장에 있는 과일들을 보고 **'사과인지 포도인지 맞히는 상자'**와 같아요.
2. 상자 속에 과일 사진을 많이 넣어주면, 나중에는 새로운 과일만 봐도 "이건 사과야!"라고 알려주죠.
3. 바구니에 사과와 포도를 따로따로 예쁘게 나눠 담는 도우미라고 생각하면 된답니다!
