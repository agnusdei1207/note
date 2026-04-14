+++
weight = 122
title = "비지도 학습 (Unsupervised Learning)"
date = "2024-05-22"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
1. **정답(Label)이 없는 데이터**로부터 데이터 내부의 숨겨진 구조, 패턴, 상관관계를 스스로 찾아내는 기계학습 방법론이다.
2. 데이터를 유사한 특징끼리 묶는 **군집화(Clustering)**와 복잡한 데이터의 핵심 정보만 남기는 **차원 축소(Dimensionality Reduction)**가 핵심 기법이다.
3. 사전 라벨링 비용이 들지 않아 대규모 비정형 데이터(Unstructured Data) 탐색 및 전처리에 매우 효율적이다.

---

### Ⅰ. 개요 (Context & Background)
현실 세계의 데이터는 대부분 정답이 달려 있지 않다. 비지도 학습은 이러한 가공되지 않은 원시 데이터에서 '무엇이 비슷한지' 또는 '무엇이 특이한지'를 발견하는 기술이다. 데이터 분석의 초기 단계에서 데이터의 분포를 이해하거나, 복잡한 데이터를 단순화하여 후속 학습(지도 학습 등)의 효율을 높이는 데 필수적이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
비지도 학습은 데이터 포인트 간의 거리(Distance)나 밀도(Density)를 계산하여 유사성을 판단한다.

```text
[ Unsupervised Learning Core Concepts / 비지도 학습 핵심 구조 ]

     Input (X)                    Hidden Pattern Discovery             Result
    +-----------+              +----------------------------+       +-------------+
    | *  .  *   |              |  Distance/Similarity Calc  |       |  Clusters   |
    |  . *  .   |  --------->  |  (Euclidean, Cosine...)    | ----> |   [A] [B]   |
    | *  .  *   |              +-------------+--------------+       +-------------+
    +-----------+                            |                      +-------------+
                                             v                      | Reduced Dim |
                               +-------------+--------------+       |   (X1, X2)  |
                               | Projection / Decomposition | ----> +-------------+
                               | (PCA, t-SNE, SVD...)       |
                               +----------------------------+
```

1. **군집화 (Clustering)**: 유사한 특징을 가진 데이터들을 그룹(Cluster)으로 묶는다. (예: K-Means, DBSCAN)
2. **차원 축소 (Dimensionality Reduction)**: 데이터의 변수(Column)는 많지만 실제 정보량은 소수인 경우, 정보를 보존하며 축을 줄인다. (예: PCA)
3. **연관 규칙 (Association Rule)**: 항목 간의 동시 발생 패턴을 발견한다. (예: 장바구니 분석 - Apriori)

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 지도 학습 (Supervised) | 비지도 학습 (Unsupervised) |
| :--- | :--- | :--- |
| **데이터 정답** | 정답(Label) 있음 | 정답(Label) 없음 |
| **주요 목적** | 정답 예측 및 분류 | 데이터 구조 및 패턴 발견 |
| **성능 평가** | 명확함 (정답과 비교) | 주관적 (해석의 영역) |
| **대표 기술** | Regression, CNN, RNN | Clustering, PCA, Autoencoder |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
1. **데이터 전처리(Pre-processing)**: 지도 학습 수행 전, 차원 축소를 통해 모델 연산량을 줄이거나 결측치/이상치 탐지에 비지도 학습을 활용하면 시스템 효율이 극대화된다.
2. **고객 세그멘테이션(Segmentation)**: 마케팅 분야에서 정해진 기준이 아닌, 데이터 스스로가 말해주는 고객 군집을 통해 정교한 타겟팅이 가능하다.
3. **PE 관점의 판단**: 비지도 학습의 결과는 '왜 이렇게 묶였는가'에 대한 비즈니스적 해석(Interpretation)이 뒷받침되어야 한다. 기술적으로는 알고리즘 선정 시 데이터의 노이즈 처리 능력(DBSCAN 등)을 고려해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
생성형 AI의 기반이 되는 자기지도 학습(Self-supervised Learning) 또한 비지도 학습의 확장된 형태이다. 향후 데이터 레이크(Data Lake)에 쌓인 방대한 다크 데이터(Dark Data)를 자산화하기 위해 비지도 학습의 중요성은 더욱 커질 것이며, 이는 데이터 가치 창출의 마중물 역할을 할 것이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: Machine Learning (기계학습)
- **하위 개념**: K-Means, PCA, SVD, Apriori, Anomaly Detection
- **연관 개념**: Dimensionality Reduction, Distance Metrics, Self-supervised Learning

---

### 👶 어린이를 위한 3줄 비유 설명
1. 이름표가 없는 장난감들을 바닥에 쏟아놓고 정리하는 것과 같아요.
2. "얘네는 빨간색이네?", "얘네는 바퀴가 있네?"라며 스스로 비슷한 것끼리 모으는 거예요.
3. 누가 알려주지 않아도 숨겨진 짝꿍을 찾아내는 똑똑한 정리법이에요.
