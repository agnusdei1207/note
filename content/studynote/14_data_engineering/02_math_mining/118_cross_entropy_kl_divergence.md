+++
weight = 118
title = "정보 이론 교차 엔트로피 (Cross Entropy / KL Divergence)"
date = "2024-03-23"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
- 교차 엔트로피는 실제 데이터 분포와 모델이 예측한 분포 간의 '정보량 차이'를 측정하며, 분류 문제의 손실 함수(Loss Function)로 널리 쓰인다.
- KL 발산(KL Divergence)은 두 확률 분포 사이의 비대칭적 거리 척도로, 교차 엔트로피에서 실제 데이터의 자기 엔트로피를 뺀 값과 같다.
- 딥러닝에서 로지스틱 회귀와 소프트맥스 층의 오차를 최소화할 때 평균 제곱 오차(MSE)보다 빠른 수렴과 정보 이득(Information Gain) 극대화를 제공한다.

### Ⅰ. 개요 (Context & Background)
정보 이론에서 **엔트로피(Entropy)**는 정보의 불확실성을 의미한다. 머신러닝의 목표는 데이터의 실제 분포($P$)를 가장 잘 모사하는 모델 분포($Q$)를 찾는 것이다. 이때 두 분포가 얼마나 다른지 수치화하는 도구가 **교차 엔트로피(Cross Entropy)**와 **KL 발산(Kullback-Leibler Divergence)**이다. 단순히 값이 맞느냐를 따지는 것이 아니라, '확률 분포'의 관점에서 모델의 정확성을 평가하는 지표이다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
교차 엔트로피는 정보량($-\log Q$)의 기댓값을 계산한다. $P$는 실제 정답 분포(대개 One-hot 벡터), $Q$는 모델의 소프트맥스 출력이다.

```text
[ Information Theory: Relationship between Metrics ]
(정보 이론: 엔트로피, 교차 엔트로피, KL 발산의 관계)

       +---------------------------------------------+
       |   Cross Entropy (H(P, Q))                  |
       |  (교차 엔트로피: P를 Q로 설명할 때 정보량)   |
       |                                             |
       |   H(P, Q) = H(P) + D_KL(P || Q)             |
       +-----------+-------------+-------------------+
                   |             |
         +---------v---------+ +-v-------------------------+
         | Entropy H(P)      | | KL Divergence D_KL(P || Q) |
         | (P의 불확실성)     | | (두 분포 사이의 정보 손실) |
         | *Irreducible      | | *Optimization Target      |
         +-------------------+ +---------------------------+

   Formula:
   1. Entropy: H(P) = -Σ P(x) log P(x)
   2. Cross Entropy: H(P, Q) = -Σ P(x) log Q(x)
   3. KL Divergence: D_KL(P||Q) = Σ P(x) log(P(x)/Q(x))
```

- **H(P) (Entropy):** 데이터셋이 정해지면 고정되는 상수값이다.
- **D_KL (KL 발산):** $P$와 $Q$가 같으면 0이며, 다를수록 커진다. 거리처럼 쓰이지만 대칭성이 없어($D(P||Q) \neq D(Q||P)$) 거리가 아닌 '발산'이라 부른다.
- **H(P, Q) (Cross Entropy):** KL 발산을 최소화하는 것은 결국 교차 엔트로피를 최소화하는 것과 같다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 항목 (Metric) | 평균 제곱 오차 (MSE) | 교차 엔트로피 (Cross Entropy) | KL 발산 (KL Divergence) |
| :--- | :--- | :--- | :--- |
| **주요 용도** | 회귀 (Regression) | 분류 (Classification) | 생성 모델 (VAE), 지식 증류 |
| **수학적 특성** | L2 Distance 기반 | 정보 이론/로그 가능도 기반 | 정보 이득/분포 차이 기반 |
| **장점** | 직관적 에러 측정 | 소프트맥스 결합 시 기울기 소실 방지 | 두 확률 분포의 일치도 정밀 측정 |
| **단점** | 분류 시 학습 속도 저하 | 확률값(0~1)에만 적용 가능 | 비대칭성으로 인한 거리 측정 한계 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
**실무적 판단 (Technical Insight):**
분류 문제에서 MSE 대신 교차 엔트로피를 쓰는 이유는 **Gradient Descent** 효율성 때문이다. 시그모이드/소프트맥스 함수는 양 끝단에서 기울기가 매우 작아지는데, 로그 함수가 포함된 교차 엔트로피는 이 기울기를 상쇄하여 오차가 클 때 더 빠르게 학습하게 돕는다.
- **RAG & Search:** 임베딩 벡터 간의 유사도는 코사인 유사도를 쓰지만, 랭커(Ranker) 모델 학습 시에는 상위 문서 분포 일치를 위해 KL 발산을 활용한다.
- **Knowledge Distillation:** 거대 모델(Teacher)의 확률 분포를 작은 모델(Student)에게 전이할 때 KL 발산은 핵심적인 손실 함수로 작동한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
교차 엔트로피는 현대 딥러닝의 표준 손실 함수로 자리 잡았다. 데이터가 확률적 특성을 가질 때 가장 강력한 성능을 발휘하며, 이는 단순히 '정답 맞히기'가 아니라 '데이터의 맥락(Distribution)'을 이해하는 모델을 만드는 기초가 된다. 미래에는 정교한 변분 추론(Variational Inference)과 결합하여 복잡한 잠재 공간(Latent Space)을 최적화하는 핵심 도구로 더욱 발전할 것이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념:** Information Theory, Loss Function
- **유사 개념:** Maximum Likelihood Estimation (MLE), Logistic Loss
- **하위 개념:** Shannon Entropy, Relative Entropy, Binary Cross Entropy

### 👶 어린이를 위한 3줄 비유 설명
- 친구의 비밀번호를 맞히는 게임을 한다고 해봐요.
- 교차 엔트로피는 '내가 친구의 마음을 얼마나 잘 읽었는지'를 점수로 매기는 거예요.
- 점수가 낮을수록 내가 친구의 생각(분포)과 거의 똑같아졌다는 뜻이랍니다!
