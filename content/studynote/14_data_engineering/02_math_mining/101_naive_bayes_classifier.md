+++
weight = 101
title = "나이브 베이즈 분류와 라플라스 스무딩 (Naive Bayes Classifier & Laplace Smoothing)"
date = "2025-05-22"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
- **나이브 베이즈 (Naive Bayes)**: 베이즈 정리를 기반으로 모든 특성(Feature)이 서로 독립적이라는 가정(Naive) 하에 데이터의 클래스를 예측하는 확률적 분류기.
- **라플라스 스무딩 (Laplace Smoothing)**: 학습 데이터에 나타나지 않은 값이 등장했을 때 확률이 0이 되어 전체 결과가 0이 되는 'Zero Probability' 문제를 방지하는 기법.
- **실무 강점**: 계산 속도가 매우 빠르고 적은 데이터로도 효율적이며, 텍스트 분류(스팸 필터링) 및 다중 클래스 분류에서 강력한 성능을 발휘함.

### Ⅰ. 개요 (Context & Background)
텍스트 데이터처럼 차원이 매우 높은 환경에서 복잡한 모델은 연산 비용이 크고 과적합되기 쉽습니다. 나이브 베이즈는 특성 간의 상호작용을 무시하는 '순진한(Naive)' 가정을 통해 계산을 단순화하면서도, 실무에서 놀라운 정확도를 보여주는 고전적이고 강력한 알고리즘입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
베이즈 정리 기반의 분류 로직과 라플라스 스무딩의 수리적 아키텍처입니다.

```text
[ Naive Bayes Probability Flow ]

1. Prior Probability (사전 확률): P(Class) - 각 클래스가 나타날 기본 확률
2. Likelihood (우도): P(Feature | Class) - 특정 클래스에서 이 특성이 나타날 확률
3. Posterior Probability (사후 확률): P(Class | Feature) ∝ P(Class) * Π P(Feature_i | Class)

[ Laplace Smoothing Architecture (Additive Smoothing) ]

     Traditional Likelihood:   P(w|C) = count(w, C) / count(C)
                                       |
                                       v
     Smoothed Likelihood:      P(w|C) = (count(w, C) + α) / (count(C) + α*V)

     * α (Alpha): 보통 1 (Laplace) 또는 소수값 (Lidstone) 사용
     * V (Vocabulary Size): 특성(단어)의 전체 가짓수
```

**핵심 원리:**
1. **조건부 독립 가정**: "스팸 메일에서 'Free'라는 단어가 나올 확률은 'Money'라는 단어가 나올 확률과 상관이 없다"고 가정하여 연쇄 곱셈 연산을 가능하게 함.
2. **최대 사후 확률 (MAP)**: 계산된 여러 클래스의 사후 확률 중 가장 높은 확률을 가진 클래스를 최종 정답으로 선택.
3. **Log-sum Trick**: 확률(0~1 사이)을 계속 곱하면 숫자가 너무 작아져서 컴퓨터가 계산 못 하는(Underflow) 문제를 막기 위해, 확률에 로그(log)를 취해 덧셈 연산으로 변환.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | 가우시안 나이브 베이즈 | 다항 분포 나이브 베이즈 (Multinomial) | 베르누이 나이브 베이즈 |
| :--- | :--- | :--- | :--- |
| **데이터 형태** | 연속형 변수 (키, 몸무게 등) | 이산형/횟수 변수 (단어 빈도) | 이진(Binary) 변수 (단어 존재 유무) |
| **확률 분포** | 정규 분포 (Gaussian) | 다항 분포 (Multinomial) | 베르누이 분포 |
| **주요 용도** | 일반적인 수치 데이터 분류 | 일반적인 텍스트 분류 (TF) | 짧은 문서/스팸 분류 (Presence) |
| **특징** | 평균과 표준편차 활용 | 출현 빈도 가중치 부여 | 단어의 유/무만 판단 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **적용 전략 (Implementation Strategy)**:
  * **텍스트 전처리**: 불용어(Stopwords) 제거 및 어간 추출(Stemming)을 통해 전체 단어 수(V)를 적절히 통제해야 라플라스 스무딩의 왜곡을 최소화할 수 있음.
  * **온라인 학습**: 나이브 베이즈는 새로운 데이터가 들어오면 기존 빈도에 더하기만 하면 되므로, 실시간으로 변화하는 데이터 흐름(Data Stream)에 적응하기 매우 좋음.
* **기술사적 판단 (Architectural Judgment)**:
  * "나이브한 가정" 때문에 특성 간의 강한 상관관계가 있는 데이터(예: 주가 지수들)에서는 성능이 떨어질 수 있음. 이 경우 LDA나 Random Forest와 성능을 비교해야 함. 그러나 텍스트 분류와 같이 독립성 가정이 어느 정도 들어맞는 영역에서는 여전히 비용 대비 최고의 성능(Efficiency)을 보여줌.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
나이브 베이즈는 딥러닝 시대에도 스팸 필터링, 감성 분석의 베이스라인(Baseline) 모델로서 확고한 위치를 차지합니다. 향후에는 단순한 빈도 기반을 넘어 LLM 임베딩 벡터의 분포를 나이브 베이즈의 사전 확률로 결합하는 하이브리드 추론 방식으로 발전할 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **확률론**: Bayes' Theorem, Prior/Posterior, Likelihood
* **분류 알고리즘**: Logistic Regression, SVM, Decision Tree
* **텍스트 처리**: TF-IDF, Bag of Words, Zero Frequency Problem

### 👶 어린이를 위한 3줄 비유 설명
1. 편지를 읽고 "당첨, 무료, 선물" 같은 단어가 얼마나 자주 나오는지 세어서 스팸인지 아닌지 맞히는 게임이에요.
2. 한 번도 못 본 단어가 나왔다고 해서 전체를 빵점(0) 처리하지 않도록, 모든 단어에 1점을 미리 보너스로 주는 게 '스무딩'이에요.
3. 단어들이 서로 도우며 나오든 말든 상관없이 각자 따로따로 계산하니까 아주 빠르고 간편한 방법이랍니다.
