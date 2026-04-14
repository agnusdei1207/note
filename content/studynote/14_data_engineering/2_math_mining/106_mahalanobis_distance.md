+++
title = "마할라노비스 거리 (Mahalanobis Distance)"
weight = 106
date = "2026-03-04"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
1. **마할라노비스 거리**는 데이터의 상관관계(공분산)를 고려하여 데이터군 중심으로부터의 거리를 측정하는 통계적 거리 척도이다.
2. 유클리드 거리와 달리 데이터의 분포 형태를 반영하므로, 변수 간 상관성이 높은 다변량 데이터에서 훨씬 정확한 거리 계산이 가능하다.
3. 머신러닝에서 이상치 탐지(Outlier Detection), 다변량 통계 분석, 그리고 분류 알고리즘의 핵심 기반 기술로 사용된다.

### Ⅰ. 개요 (Context & Background)
- **배경**: 변수 간 단위가 다르거나 서로 강하게 결합(상관성)되어 있을 때, 단순 직선 거리인 유클리드 거리(Euclidean Distance)는 데이터의 실제 거리를 왜곡할 위험이 있다.
- **필요성**: 데이터가 특정 방향으로 길게 늘어진 타원형 분포를 가질 때, 분포의 중심으로부터 멀어진 정도를 통계적으로 유의미하게 평가해야 한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **수리적 정의**: $D_M(x) = \sqrt{(x - \mu)^T S^{-1} (x - \mu)}$
  - $x$: 데이터 포인트 벡터
  - $\mu$: 평균 벡터 (데이터군의 중심)
  - $S^{-1}$: 공분산 행렬의 역행렬 (변수 간 상관관계와 분산을 반영)

```text
[Mahalanobis vs Euclidean Distance Concept]

     ^ (Variable Y)
     |
     |         * (Point A)  <-- Closer in Euclidean, but Outlier in Mahalanobis!
     |       /
     |     /   (Distribution Ellipse)
     |   /        +-------+
     | /       /           \
     |       /      (Center) \
     +----------------------------> (Variable X)

1. Normalization: Scale each variable by its standard deviation.
2. Rotation: Account for the correlation (Covariance) between X and Y.
3. Distance: Measure distance in this decorrelated space.
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 유클리드 거리 (Euclidean) | 마할라노비스 거리 (Mahalanobis) |
| :--- | :--- | :--- |
| **상관관계 고려** | 무시 (독립 변수 가정) | 필수 고려 (공분산 행렬 활용) |
| **분포 형태** | 원형 (Spherical) | 타원형 (Elliptical, 데이터 형태 반영) |
| **단위 의존성** | 매우 민감함 (스케일링 필수) | 상대적으로 강건함 (자동 보정 효과) |
| **주요 용도** | 일반적 군집화 (K-Means) | 이상치 탐지, 다변량 가설 검정 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **실무 적용**: 금융 사기 탐지(FDS), 제조 공정의 불량 품질 모니터링, 생체 인식(얼굴/홍채) 모델에서 변수 간 복잡한 관계를 분석할 때 핵심적으로 활용된다.
- **기술사적 판단**: 변수 간 공선성(Multicollinearity)이 높은 경우 단순 거리는 신뢰할 수 없다. 마할라노비스 거리는 공분산의 역행렬을 이용해 데이터를 '화이트닝(Whitening)' 처리하는 효과가 있어, 신뢰도 높은 이상치 식별이 가능하다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 데이터의 고유한 구조를 무너뜨리지 않고 거리를 측정함으로써, 인공지능 모델의 오탐지(False Positive)를 획기적으로 낮출 수 있다.
- **결론**: 다변량 분석의 정수이며, 데이터가 복잡해질수록 단순 거리 척도보다 마할라노비스와 같은 통계적 거리 개념이 분석의 품질을 결정짓는 핵심 요소가 된다.

### 📌 관련 개념 맵 (Knowledge Graph)
1. **Covariance Matrix**: 변수 간의 변동이 얼마나 함께 일어나는지 나타내는 행렬
2. **Standardization (Z-score)**: 평균 0, 분산 1로 변환하는 기법
3. **Chi-square Distribution**: 마할라노비스 거리의 제곱은 자유도가 변수 개수인 카이제곱 분포를 따름

### 👶 어린이를 위한 3줄 비유 설명
1. **유클리드 거리**: 지도 위에서 집과 학교 사이의 직선 길이를 그냥 자로 재는 거예요.
2. **마할라노비스 거리**: 길이뿐만 아니라, 길이 울퉁불퉁한지 아니면 길이 한쪽으로 치우쳐 있는지까지 생각해서 '실제로 얼마나 가기 힘든 거리인가'를 재는 거예요.
3. **결론**: 겉모양뿐만 아니라 데이터들이 모여 있는 성질까지 고려해서 똑똑하게 거리를 재는 방법이에요.
