+++
title = "비지도 학습 (Unsupervised Learning)"
date = "2026-03-04"
[extra]
categories = ["studynotes-10_ai"]
+++

# 비지도 학습 (Unsupervised Learning)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 라벨이 없는 데이터에서 숨겨진 구조, 패턴, 군집을 자동으로 발견하는 학습 패러다임으로, 군집화(Clustering), 차원 축소(Dimensionality Reduction), 밀도 추정(Density Estimation)이 핵심 기법입니다.
> 2. **가치**: 고객 세분화, 이상 탐지, 추천 시스템, 데이터 압축 등에서 라벨링 비용 없이 가치를 창출하며, 자기 지도 학습의 사전 학습 단계로 대규모 언어 모델의 기반이 됩니다.
> 3. **융합**: 지도 학습과 결합하여 준지도 학습(Semi-supervised), 자기 지도 학습(Self-supervised)으로 확장되며, 생성형 AI의 사전 학습에 필수적입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**비지도 학습(Unsupervised Learning)**은 라벨 $y$ 없이 입력 데이터 $X$만으로 데이터의 내재된 구조를 학습합니다. 핵심 목표는 **(1) 군집화(Clustering), (2) 차원 축소(Dimensionality Reduction), (3) 생성 모델링(Generative Modeling), (4) 이상 탐지(Anomaly Detection)**입니다.

수학적으로, 데이터셋 $\mathcal{D} = \{x_i\}_{i=1}^{N}$이 주어졌을 때, 데이터 분포 $p(x)$를 모델링하거나, 데이터를 의미 있는 그룹으로 분할하는 것입니다.

**주요 유형**:
1. **군집화 (Clustering)**: K-Means, DBSCAN, 계층적 군집화
2. **차원 축소**: PCA, t-SNE, UMAP, Autoencoder
3. **밀도 추정**: GMM, KDE
4. **연관 규칙**: Apriori, FP-Growth

#### 2. 💡 비유를 통한 이해
비지도 학습은 **'정답 없이 스스로 공부하기'**에 비유할 수 있습니다:

- **군집화**: 도서관에서 책을 장르별로 정리하라는데, 장르 표시가 없음. 책 내용을 보고 비슷한 책끼리 모음.
- **차원 축소**: 3D 물체를 2D 사진으로 찍는 것. 가장 특징적인 각도에서 찍어 정보 손실 최소화.
- **이상 탐지**: 반 전체 사진에서 한 명만 다른 교복을 입은 학생 찾기.
- **연관 규칙**: 슈퍼마켓에서 "맥주를 사는 사람은 땅콩도 산다"는 패턴 발견.

#### 3. 등장 배경 및 발전 과정

1.  **기존 기술의 치명적 한계점**:
    - **라벨링 비용**: 모든 데이터에 라벨을 붙이는 것은 비용과 시간이 많이 듦.
    - **미지의 패턴**: 인간이 미처 발견하지 못한 패턴이 데이터에 있을 수 있음.

2.  **혁신적 패러다임의 변화**:
    - **PCA (1901)**: Pearson이 주성분 분석 제안
    - **K-Means (1967)**: MacQueen이 제안한 가장 대중적 군집화
    - **EM 알고리즘 (1977)**: Dempster 등이 GMM 학습 방법 제안
    - **Autoencoder (1987)**: Rumelhart 등이 제안한 신경망 기반 차원 축소
    - **DBSCAN (1996)**: 밀도 기반 군집화로 임의 형태 처리
    - **t-SNE (2008)**: 고차원 시각화 혁신
    - **BERT (2018)**: 자기 지도 학습으로 비지도 학습의 새 장

3.  **비즈니스적 요구사항**:
    - 고객 세분화 (마케팅 타겟팅)
    - 이상 탐지 (사기, 장애 예측)
    - 추천 시스템 (유사 아이템 군집화)
    - 데이터 시각화 및 탐색

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 비지도 학습 기법 구성 요소 (표)

| 기법 | 상세 역할 | 내부 동작 메커니즘 | 대표 알고리즘 | 비유 |
|:---|:---|:---|:---|:---|
| **K-Means** | K개 군집으로 분할 | 중심점 할당-이동 반복 (EM) | Lloyd's Algorithm | 비슷한 것끼리 모으기 |
| **DBSCAN** | 밀도 기반 군집화 | ε-이웃 확장, 노이즈 식별 | Core Point 연결 | 섬 찾기 |
| **PCA** | 선형 차원 축소 | 공분산 고유값 분해 | SVD | 그림자 만들기 |
| **t-SNE** | 비선형 시각화 | 확률 분포 매칭, KL 발산 최소화 | Gradient Descent | 3D→2D 지도 |
| **Autoencoder** | 신경망 압축 | 인코더-디코더, 병목층 | Adam Optimizer | 압축-압축해제 |
| **GMM** | 확률적 군집화 | 가우시안 혼합, EM 학습 | Expectation-Maximization | 연속적 소속도 |

#### 2. 군집화 알고리즘 다이어그램

```text
<<< K-Means Algorithm >>=>

    [Step 1: Initialize]           [Step 2: Assign]            [Step 3: Update]
    랜덤 K개 중심점                각 점 → 가장 가까운 중심      중심점을 평균으로 이동

         ●  ●                          ●  ●                       ●  ●
       ●    ●                        ● ② ●                     ● ② ●
      ●  X   ●                      ●    ●                     ●    ●
     ●   X    ●         →          ●      ●         →         ●  ○   ●
      ●       ●                     ●    ●                      ●    ●
       ●  ●  ●                        ●  ●                       ●  ●
          ●                              ●

    X = 초기 중심점               ② = 군집 2에 할당            ○ = 새 중심점

    반복: 수렴할 때까지 (중심점 이동 < threshold)


<<< DBSCAN (Density-Based Spatial Clustering) >>=>

    파라미터:
    - ε (epsilon): 이웃 반경
    - minPts: 핵심점 최소 이웃 수

    포인트 분류:
    ┌─────────────────────────────────────────────────────────────┐
    │  ●    ●●●●        ●●●●●●                                    │
    │   ●   ●●●●   ●    ●●●●●●        ○ (Border Point)            │
    │    ●  ●●●●        ●●●●●●                                     │
    │       Cluster 1   ★ (Noise)    Cluster 2                   │
    │                                                                │
    │  핵심점(Core): ε 내에 minPts 이상 존재                        │
    │  경계점(Border): 핵심점의 이웃이지만 자신은 핵심 아님           │
    │  노이즈(Noise): 핵심점도 경계점도 아님                         │
    └─────────────────────────────────────────────────────────────┘

    장점: 임의 형태 군집, 노이즈 식별
    단점: 밀도가 다른 군집 혼재 시 어려움


<<< PCA (Principal Component Analysis) >>=>

    3D 데이터                    2D 투영 (PC1, PC2)
    (분산 최대 보존)

         ●                        ●
       ●   ●                    ●   ●
      ●  ●  ●         →       ●   ●   ●
       ●   ●                    ●   ●
         ●                        ●

    과정:
    1. 데이터 중심화 (평균 0)
    2. 공분산 행렬 계산
    3. 고유값 분해
    4. 상위 k개 고유벡터 선택 (주성분)
    5. 데이터 투영
```

#### 3. 심층 동작 원리: K-Means와 PCA

**K-Means 목적 함수**:
$$J = \sum_{i=1}^{N} \sum_{k=1}^{K} r_{ik} ||x_i - \mu_k||^2$$

여기서 $r_{ik}$는 데이터 $i$가 군집 $k$에 속하면 1, 아니면 0입니다.

**PCA 수학적 원리**:
공분산 행렬 $S = \frac{1}{n}X^TX$의 고유값 분해:
$$Sv_i = \lambda_i v_i$$

- $v_i$: 제 $i$ 주성분 (고유벡터)
- $\lambda_i$: 설명 분산 (고유값)

누적 설명 분산 비율이 95% 이상이 되도록 차원 선택.

#### 4. 실무 수준의 Python 비지도 학습 코드

```python
"""
Production-Ready Unsupervised Learning
- K-Means, DBSCAN, PCA, Autoencoder 구현
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional
import torch
import torch.nn as nn

class KMeansClusterer:
    """
    K-Means 군집화 with 최적 K 탐색
    """
    def __init__(self, max_k: int = 10, random_state: int = 42):
        self.max_k = max_k
        self.random_state = random_state
        self.best_k = None
        self.model = None
        self.scaler = StandardScaler()

    def find_optimal_k(
        self,
        X: np.ndarray,
        method: str = 'silhouette'
    ) -> Tuple[int, dict]:
        """
        최적 K 탐색 (Elbow, Silhouette)
        """
        X_scaled = self.scaler.fit_transform(X)
        scores = {}

        for k in range(2, self.max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            labels = kmeans.fit_predict(X_scaled)

            if method == 'silhouette':
                scores[k] = silhouette_score(X_scaled, labels)
            elif method == 'calinski_harabasz':
                scores[k] = calinski_harabasz_score(X_scaled, labels)
            else:  # elbow (inertia)
                scores[k] = kmeans.inertia_

        # 최적 K 선택
        if method in ['silhouette', 'calinski_harabasz']:
            self.best_k = max(scores, key=scores.get)
        else:
            # Elbow: 기울기 급변 지점 (단순화)
            self.best_k = 3  # 실제로는 기울기 분석 필요

        return self.best_k, scores

    def fit(self, X: np.ndarray, n_clusters: Optional[int] = None):
        """
        군집화 학습
        """
        X_scaled = self.scaler.fit_transform(X)
        k = n_clusters or self.best_k or 3

        self.model = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
        self.labels_ = self.model.fit_predict(X_scaled)
        self.centers_ = self.scaler.inverse_transform(self.model.cluster_centers_)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """새 데이터 군집 예측"""
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)


class DBSCANClusterer:
    """
    DBSCAN 군집화 with 자동 파라미터 추천
    """
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()

    def estimate_epsilon(self, X: np.ndarray, k: int = 4) -> float:
        """
        k-distance 그래프로 ε 추정
        """
        from sklearn.neighbors import NearestNeighbors

        X_scaled = self.scaler.fit_transform(X)
        neighbors = NearestNeighbors(n_neighbors=k)
        neighbors.fit(X_scaled)
        distances, _ = neighbors.kneighbors(X_scaled)

        # k번째 이웃 거리 정렬
        k_distances = np.sort(distances[:, k-1])

        # 엘보우 포인트 찾기 (단순화)
        epsilon = np.median(k_distances) * 1.5

        return epsilon

    def fit(
        self,
        X: np.ndarray,
        eps: Optional[float] = None,
        min_samples: int = 5
    ):
        """
        DBSCAN 학습
        """
        X_scaled = self.scaler.fit_transform(X)

        if eps is None:
            eps = self.estimate_epsilon(X)

        self.model = DBSCAN(eps=eps, min_samples=min_samples)
        self.labels_ = self.model.fit_predict(X_scaled)
        self.n_clusters_ = len(set(self.labels_)) - (1 if -1 in self.labels_ else 0)
        self.n_noise_ = list(self.labels_).count(-1)

        return self


class DimensionalityReducer:
    """
    차원 축소 (PCA)
    """
    def __init__(self, variance_threshold: float = 0.95):
        self.variance_threshold = variance_threshold
        self.pca = None
        self.scaler = StandardScaler()

    def fit(self, X: np.ndarray) -> 'DimensionalityReducer':
        """
        PCA 학습
        """
        X_scaled = self.scaler.fit_transform(X)

        # 먼저 전체 성분으로 학습하여 필요 차원 수 확인
        pca_full = PCA()
        pca_full.fit(X_scaled)

        # 누적 분산이 threshold를 넘는 최소 차원 수
        cumsum = np.cumsum(pca_full.explained_variance_ratio_)
        n_components = np.argmax(cumsum >= self.variance_threshold) + 1

        # 최종 PCA 학습
        self.pca = PCA(n_components=n_components)
        self.transformed_ = self.pca.fit_transform(X_scaled)
        self.explained_variance_ratio_ = self.pca.explained_variance_ratio_

        print(f"Original dimensions: {X.shape[1]}")
        print(f"Reduced dimensions: {n_components}")
        print(f"Explained variance: {cumsum[n_components-1]:.4f}")

        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """새 데이터 변환"""
        X_scaled = self.scaler.transform(X)
        return self.pca.transform(X_scaled)

    def inverse_transform(self, X_transformed: np.ndarray) -> np.ndarray:
        """원본 공간으로 복원"""
        X_scaled = self.pca.inverse_transform(X_transformed)
        return self.scaler.inverse_transform(X_scaled)


class Autoencoder(nn.Module):
    """
    신경망 기반 차원 축소
    """
    def __init__(
        self,
        input_dim: int,
        encoding_dim: int,
        hidden_dims: List[int] = None
    ):
        super().__init__()

        if hidden_dims is None:
            hidden_dims = [(input_dim + encoding_dim) // 2]

        # Encoder
        encoder_layers = []
        prev_dim = input_dim
        for h_dim in hidden_dims + [encoding_dim]:
            encoder_layers.extend([
                nn.Linear(prev_dim, h_dim),
                nn.ReLU()
            ])
            prev_dim = h_dim
        self.encoder = nn.Sequential(*encoder_layers[:-1])  # 마지막 ReLU 제거

        # Decoder
        decoder_layers = []
        prev_dim = encoding_dim
        for h_dim in reversed(hidden_dims):
            decoder_layers.extend([
                nn.Linear(prev_dim, h_dim),
                nn.ReLU()
            ])
            prev_dim = h_dim
        decoder_layers.append(nn.Linear(prev_dim, input_dim))
        self.decoder = nn.Sequential(*decoder_layers)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return encoded, decoded

    def get_encoding(self, x: torch.Tensor) -> torch.Tensor:
        """잠재 표현 추출"""
        return self.encoder(x)


# 사용 예시
if __name__ == "__main__":
    from sklearn.datasets import make_blobs, load_iris

    # 테스트 데이터 생성
    X, y_true = make_blobs(n_samples=300, centers=4, n_features=10, random_state=42)

    # K-Means 군집화
    print("=== K-Means Clustering ===")
    kmeans = KMeansClusterer(max_k=10)
    best_k, scores = kmeans.find_optimal_k(X, method='silhouette')
    print(f"Optimal K: {best_k}")
    print(f"Silhouette scores: {scores}")

    kmeans.fit(X)
    print(f"Cluster labels: {np.unique(kmeans.labels_)}")

    # DBSCAN 군집화
    print("\n=== DBSCAN Clustering ===")
    dbscan = DBSCANClusterer()
    dbscan.fit(X, min_samples=5)
    print(f"Number of clusters: {dbscan.n_clusters_}")
    print(f"Noise points: {dbscan.n_noise_}")

    # PCA 차원 축소
    print("\n=== PCA Dimensionality Reduction ===")
    reducer = DimensionalityReducer(variance_threshold=0.95)
    reducer.fit(X)
    print(f"Transformed shape: {reducer.transformed_.shape}")

    # Autoencoder
    print("\n=== Autoencoder ===")
    ae = Autoencoder(input_dim=10, encoding_dim=3, hidden_dims=[7, 5])
    print(f"Autoencoder architecture:\n{ae}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 군집화 알고리즘 비교

| 알고리즘 | 군집 형태 | K 지정 | 노이즈 처리 | 스케일링 | 복잡도 |
|:---|:---|:---|:---|:---|:---|
| **K-Means** | 구형 | 필수 | 없음 | 필요 | O(nkt) |
| **K-Medoids** | 구형 | 필수 | 없음 | 불필요 | O(n²kt) |
| **DBSCAN** | 임의 형태 | 자동 | 있음 | 필요 | O(n log n) |
| **계층적** | 트리 | 반자동 | 없음 | 필요 | O(n²~n³) |
| **GMM** | 타원 | 필수 | 없음 | 필요 | O(nk²) |
| **Spectral** | 비볼록 | 필수 | 없음 | 필요 | O(n³) |

#### 2. 차원 축소 기법 비교

| 기법 | 선형/비선형 | 지도/비지도 | 용도 | 복잡도 |
|:---|:---|:---|:---|:---|
| **PCA** | 선형 | 비지도 | 노이즈 제거, 시각화 | O(d³) |
| **t-SNE** | 비선형 | 비지도 | 시각화 | O(n²) |
| **UMAP** | 비선형 | 비지도 | 시각화, 축소 | O(n log n) |
| **Autoencoder** | 비선형 | 비지도 | 압축, 특성 학습 | O(n×d×h) |
| **LDA** | 선형 | 지도 | 분류 전처리 | O(d³) |
| **ICA** | 선형 | 비지도 | 신호 분리 | O(n²) |

#### 3. 과목 융합 관점 분석

*   **[비지도 학습 + 추천 시스템]**:
    사용자/아이템 군집화로 Cold Start 문제 해결. Matrix Factorization의 초기화.

*   **[비지도 학습 + 이상 탐지]**:
    Isolation Forest, Autoencoder Reconstruction Error로 이상치 탐지.

*   **[비지도 학습 + NLP]**:
    Word2Vec, BERT의 사전 학습이 비지도 학습의 일종. 대규모 텍스트에서 언어 패턴 학습.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단: 실무 시나리오

**시나리오 A: 고객 세분화 (RFM 분석)**
*   **상황**: 100만 고객을 마케팅 타겟별로 분류
*   **기술사 판단**:
    1.  **특성**: Recency(최근 구매), Frequency(빈도), Monetary(금액)
    2.  **전처리**: Log 변환 + Standard Scaling
    3.  **알고리즘**: K-Means (K=4~6)
    4.  **평가**: Silhouette Score + 비즈니스 해석 가능성
    5.  **결과**: VIP, 충성, 잠재, 이탈 위험군 식별

**시나리오 B: 제조 공정 이상 탐지**
*   **상황**: 100개 센서 데이터에서 공정 이상 조기 감지
*   **기술사 판단**:
    1.  **전처리**: PCA로 100→20차원 축소
    2.  **모델**: Autoencoder (재구성 오차)
    3.  **임계값**: 정상 데이터의 99%tile
    4.  **결과**: 센서 고진 전 2시간 전 이상 감지

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **스케일링**: 거리 기반 알고리즘은 스케일링 필수
- [ ] **K 선택**: Elbow, Silhouette, Gap Statistics 병행
- [ ] **해석 가능성**: 군집 특성 프로파일링 필수
- [ ] **평가 지표**: 라벨 없이 Silhouette, Davies-Bouldin 등 사용
- [ ] **노이즈 처리**: DBSCAN, Isolation Forest로 이상치 식별

#### 3. 안티패턴 (Anti-patterns)

*   **안티패턴 1: 스케일링 무시**: 연봉(억)과 나이(십년)를 같이 쓰면 연봉만 중요해짐.
*   **안티패턴 2: K 임의 설정**: "4개면 되겠지" → 비즈니스 의미 없는 군집.
*   **안티패턴 3: 고차원 직접 군집화**: 차원의 저주로 거리 의미 상실. PCA 후 군집화.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 기존 방식 (직관/룰) | 비지도 학습 | 향상/변화 |
|:---|:---|:---|:---|
| **고객 세분화** | 3~5개 구간 | 6~10개 정교 군집 | 타겟팅 정밀도 2배 |
| **이상 탐지** | 임계값 기반 | 패턴 기반 | 오탐 50% 감소 |
| **데이터 압축** | 100% 저장 | 5~20% 저장 | 저장 비용 80% 절감 |
| **데이터 탐색** | 수동 분석 | 자동 패턴 발견 | 분석 시간 90% 단축 |

#### 2. 미래 전망 및 진화 방향

**단기 (2024~2026)**:
- **자기 지도 학습 확대**: BERT, GPT 방식의 사전 학습 표준화
- **심층 군집화 (Deep Clustering)**: 신경망 기반 end-to-end 군집화

**중기 (2027~2030)**:
- **자동 특성 학습**: AutoML + 비지도 학습 결합
- **실시간 스트리밍 군집화**: 온라인 학습 알고리즘

**장기 (2030~)**:
- **AGI의 기반**: 대규모 비지도 학습이 일반 지능의 기반

#### 3. 참고 표준 및 가이드라인

*   **Scikit-learn Clustering**: 표준 군집화 라이브러리
*   **UMAP Documentation**: 차원 축소 베스트 프랙티스
*   **BERT Pre-training**: 자기 지도 학습 표준

---

### 📌 관련 개념 맵 (Knowledge Graph)

*   **[지도 학습](@/studynotes/10_ai/02_ml/supervised_learning.md)**: 라벨 있는 학습
*   **[K-Means](@/studynotes/10_ai/02_ml/kmeans_clustering.md)**: 대표적 군집화 알고리즘
*   **[PCA](@/studynotes/10_ai/02_ml/pca_dimensionality_reduction.md)**: 대표적 차원 축소
*   **[Autoencoder](@/studynotes/10_ai/01_dl/autoencoder_model.md)**: 신경망 기반 압축
*   **[이상 탐지](@/studynotes/10_ai/02_ml/anomaly_detection.md)**: 비지도 학습 응용

---

### 👶 어린이를 위한 3줄 비유 설명

1.  **스스로 정리하기**: 비지도 학습은 선생님이 없어도 스스로 공부하는 것과 같아요. 책장에 있는 책들을 비슷한 것끼리 모아요.
2.  **패턴 찾기**: "이 책들은 그림이 많네?", "이 책들은 두께가 비슷해!" 하면서 스스로 규칙을 찾아요.
3.  **숨은 비밀 발견**: 사람이 미처 몰랐던 숨겨진 패턴을 AI가 발견할 수 있어요. "어? 이 두 상품을 같이 사는 사람이 많네!"
