+++
title = "머신러닝 기초 및 핵심 개념"
date = "2026-03-04"
[extra]
categories = ["studynotes-10_ai"]
+++

# 머신러닝 기초 및 핵심 개념

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 머신러닝은 데이터로부터 패턴을 학습하여 새로운 데이터에 대해 예측/결정을 내리는 알고리즘 체계로, 지도/비지도/강화 학습의 세 패러다임이 있습니다.
> 2. **가치**: 규칙 기반 시스템이 해결 못하는 복잡한 문제(이미지 인식, 언어 이해)를 데이터 기반으로 해결하며, 모든 AI 응용의 기반이 됩니다.
> 3. **융합**: 통계학, 최적화 이론, 컴퓨터 과학이 융합된 학문으로, 딥러닝, 강화학습, 생성형 AI의 출발점입니다.

---

### Ⅰ. 머신러닝 3대 패러다임

#### 1. 지도 학습 (Supervised Learning)
- **정의**: 입력(X)과 정답(Y) 쌍으로 학습
- **유형**: 분류(Classification), 회귀(Regression)
- **알고리즘**: 선형 회귀, 로지스틱 회귀, SVM, 결정 트리, Random Forest, XGBoost

#### 2. 비지도 학습 (Unsupervised Learning)
- **정의**: 라벨 없이 데이터의 구조 학습
- **유형**: 군집화(Clustering), 차원 축소, 밀도 추정
- **알고리즘**: K-Means, DBSCAN, PCA, Autoencoder

#### 3. 강화 학습 (Reinforcement Learning)
- **정의**: 보상 신호를 통해 최적 행동 정책 학습
- **구성**: 에이전트, 환경, 상태, 행동, 보상
- **알고리즘**: Q-Learning, DQN, PPO, A3C

---

### Ⅱ. 핵심 개념

#### 편향-분산 트레이드오프 (Bias-Variance Trade-off)

$$\text{MSE} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Error}$$

| 현상 | 원인 | 증상 | 해결책 |
|:---|:---|:---|:---|
| **과소적합 (Underfitting)** | 높은 편향 | 학습/테스트 모두 낮음 | 복잡한 모델, 특성 추가 |
| **과대적합 (Overfitting)** | 높은 분산 | 학습 높음, 테스트 낮음 | 정규화, 데이터 증강 |

#### 차원의 저주 (Curse of Dimensionality)
- 특성이 늘어날수록 데이터 희소화
- 필요 샘플 수가 기하급수적 증가
- 해결: PCA, 특성 선택, Manifold Learning

#### 교차 검증 (Cross-Validation)
- K-Fold: 데이터를 K개로 분할하여 K번 검증
- 목적: 일반화 성능 추정, 과적합 방지

---

### Ⅲ. 데이터 전처리

#### 인코딩
| 방식 | 설명 | 용도 |
|:---|:---|:---|
| **One-Hot** | 범주 → 이진 벡터 | 순서 없는 범주 |
| **Label** | 범주 → 정수 | 트리 기반 모델 |
| **Target** | 범주 → 타겟 평균 | 고차원 범주 |

#### 스케일링
| 방식 | 공식 | 범위 |
|:---|:---|:---|
| **Min-Max** | (x - min)/(max - min) | [0, 1] |
| **Standard** | (x - μ)/σ | μ=0, σ=1 |
| **Robust** | (x - median)/IQR | 이상치 강건 |

---

### Ⅳ. 평가 지표

#### 분류 지표
| 지표 | 공식 | 의미 |
|:---|:---|:---|
| **Accuracy** | (TP+TN)/Total | 전체 정확도 |
| **Precision** | TP/(TP+FP) | 예측 양성 중 실제 양성 |
| **Recall** | TP/(TP+FN) | 실제 양성 중 예측 양성 |
| **F1** | 2×P×R/(P+R) | 정밀도와 재현율 조화평균 |

#### 회귀 지표
| 지표 | 공식 | 의미 |
|:---|:---|:---|
| **MSE** | (1/n)Σ(y-ŷ)² | 평균 제곱 오차 |
| **RMSE** | √MSE | MSE 제곱근 |
| **R²** | 1 - SS_res/SS_tot | 설명 분산 비율 |

---

### Ⅴ. 하이퍼파라미터 최적화

| 방식 | 원리 | 장점 | 단점 |
|:---|:---|:---|:---|
| **Grid Search** | 모든 조합 탐색 | 완전 탐색 | 느림 |
| **Random Search** | 무작위 샘플링 | 빠름 | 운 의존 |
| **Bayesian** | 확률 모델 기반 | 효율적 | 구현 복잡 |
| **Hyperband** | 조기 종료 + 탐색 | 자원 효율 | 설정 복잡 |

---

### 📌 관련 개념 맵
- [지도 학습](@/studynotes/10_ai/02_ml/supervised_learning.md)
- [비지도 학습](@/studynotes/10_ai/02_ml/unsupervised_learning.md)
- [강화 학습](@/studynotes/10_ai/01_dl/reinforcement_learning.md)
- [딥러닝 기초](@/studynotes/10_ai/01_dl/neural_network_ann.md)
- [ML 핵심 알고리즘](@/studynotes/10_ai/02_ml/ml_core_algorithms.md)

---

### 👶 어린이를 위한 3줄 비유
1. **경험으로 배우기**: 머신러닝은 많은 경험(데이터)을 통해 스스로 규칙을 찾아내는 것이에요.
2. **연습 문제 풀기**: 지도 학습은 정답이 있는 문제를 많이 풀면서 실력을 늘리는 거예요.
3. **스스로 발견하기**: 비지도 학습은 정답 없이 비슷한 것끼리 모으면서 패턴을 찾아요!
