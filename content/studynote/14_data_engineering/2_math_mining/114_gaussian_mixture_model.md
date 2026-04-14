+++
weight = 114
title = "가우시안 혼합 모델 (Gaussian Mixture Model, GMM)"
date = "2024-03-24"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
- **확률 기반 군집화:** 데이터가 여러 개의 가우시안(정규) 분포가 결합된 형태라고 가정하고, 각 데이터가 특정 군집에 속할 확률(Soft Clustering)을 계산.
- **EM 알고리즘:** Expectation(기댓값 계산)과 Maximization(매개변수 최적화) 과정을 반복하여 숨겨진 분포의 평균과 분산을 추정.
- **유연한 경계:** K-Means처럼 원형의 고정된 경계가 아닌, 타원형의 유연한 군집 경계를 형성하여 복잡한 데이터 구조를 효과적으로 모델링.

### Ⅰ. 개요 (Context & Background)
대부분의 군집화 알고리즘은 데이터를 특정 그룹에 확정적으로 할당하지만(Hard Clustering), 현실의 데이터는 여러 특성이 섞여 있는 경우가 많습니다. 가우시안 혼합 모델(GMM)은 데이터가 $K$개의 정규 분포로부터 생성되었다고 보고, 통계적 추론을 통해 각 분포의 파라미터를 찾아내는 생성 모델(Generative Model)입니다. 이는 음성 인식, 이상 탐지, 복잡한 밀도 추정 분야에서 핵심적인 역할을 합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
GMM은 관측되지 않은 '잠재 변수(Latent Variable)'를 포함하는 확률 모델입니다.

```text
[ GMM Architecture: Probabilistic Mixture ]

      Density (P)
         ^          Cluster 1 (Normal)      Cluster 2 (Normal)
         |            ________                ________
         |           /        \              /        \
         |          /    **    \            /    **    \
         |_________/____*__*____\__________/____*__*____\_________> Data (X)
                        [mu1, sigma1]          [mu2, sigma2]

[ EM Algorithm Workflow ]
1. Initialization: 초기 평균(mu), 분산(sigma), 혼합 계수(pi)를 설정.
2. E-Step (Expectation): 현재 파라미터를 기반으로 각 데이터가 군집에 속할 확률(Responsibility) 계산.
3. M-Step (Maximization): 계산된 확률을 가중치로 삼아 mu, sigma, pi를 재학습(Update).
4. Convergence: 파라미터 변화가 미미할 때까지 반복.
```

**핵심 원리:**
1. **정규 분포의 선형 결합:** 전체 데이터 분포 $p(x)$를 $K$개 가우시안 분포의 가중치 합으로 표현.
2. **공분산 행렬(Covariance Matrix):** 군집의 방향성과 신장도를 결정하여 다양한 형태의 타원형 클러스터를 지원.
3. **최대 가능도 추정(MLE)의 확장:** 로그 가능도 함수를 최대화하기 위해 EM 알고리즘을 사용.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | K-Means Clustering | Gaussian Mixture Model (GMM) |
| :--- | :--- | :--- |
| **할당 방식** | Hard (0 또는 1) | Soft (0 ~ 1 사이의 확률) |
| **군집 형태** | 원형 (Spherical) | 타원형 (Elliptical / Flexible) |
| **최적화 기법** | 거리 기반 최적화 | EM 알고리즘 (확률 기반) |
| **장점** | 계산 속도가 매우 빠름 | 데이터의 통계적 구조 반영 우수 |
| **단점** | 군집 크기가 다르면 성능 저하 | 초기값에 민감, 계산 복잡도 높음 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **실무 적용:** 센서 데이터 분석에서 정상 범주를 GMM으로 모델링한 후, 새로운 데이터가 발생할 확률이 매우 낮을 경우(Low Likelihood) 이를 이상치(Anomaly)로 판정하는 '이상 탐지' 시스템에 널리 쓰입니다.
- **기술사적 판단:** GMM은 데이터의 '불확실성'을 모델링할 수 있다는 점에서 강력하지만, 차원이 높아질수록 공분산 행렬 계산 비용이 기하급수적으로 증가합니다. 기술사는 실무에서 `covariance_type` 옵션(spherical, diag, full)을 데이터 특성에 맞춰 조정하여 성능과 정확도의 균형을 맞추는 전략을 제시해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
GMM은 딥러닝 시대에도 변하지 않는 통계적 기초를 제공하며, 최근에는 VAE(Variational Autoencoder)와 같은 생성 모델의 잠재 공간(Latent Space) 분포를 모델링하는 데 응용되고 있습니다. 데이터 엔지니어링 관점에서 확률적 군집화는 단순 분류를 넘어 데이터의 생성 원리를 이해하는 표준적인 방법론으로 자리 잡고 있습니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Unsupervised Learning, Probabilistic Modeling
- **하위 개념:** EM Algorithm, Normal Distribution, Latent Variable
- **연관 기술:** K-Means, DBSCAN, VAE, Anomaly Detection

### 👶 어린이를 위한 3줄 비유 설명
1. 아이스크림 가게에 '초코맛'과 '딸기맛'이 섞여 있는 통이 있다고 생각해 보세요.
2. 어떤 부분은 초코맛이 더 강하고, 어떤 부분은 딸기맛이 더 강한데, 이걸 확률로 계산하는 거예요.
3. "이 한 숟가락은 초코일 확률이 80%네!"라고 말해주는 것이 바로 가우시안 모델이에요.
