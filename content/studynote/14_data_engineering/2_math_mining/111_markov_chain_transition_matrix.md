+++
weight = 111
title = "마르코프 체인 (Markov Chain) 및 전이 행렬"
date = "2024-03-24"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
- **미래는 현재에만 의존:** 과거의 이력과 무관하게 '현재 상태'가 주어지면 미래 상태의 확률 분포가 결정되는 마르코프 성질(Markov Property)을 가짐.
- **전이 확률 행렬(Transition Matrix):** 상태 간 이동 확률을 행렬로 정식화하여 시스템의 장기적인 안정 상태(Stationary Distribution)를 수학적으로 예측 가능.
- **활용성:** 검색 엔진의 페이지랭크(PageRank), 자연어 처리(Next Word Prediction), 대기행렬 이론 및 금융 시계열 모델링의 근간이 됨.

### Ⅰ. 개요 (Context & Background)
마르코프 체인은 시간이 지남에 따라 상태가 확률적으로 변하는 이산 시간 확률 과정(Discrete-time Stochastic Process)의 대표적 모델입니다. 1906년 안드레이 마르코프에 의해 제안되었으며, "과거의 경로가 아닌 현재의 위치가 미래를 결정한다"는 비기억성(Memorylessness)을 핵심으로 합니다. 빅데이터 환경에서는 사용자 행동 로그 패턴 분석이나 대규모 그래프 데이터에서의 가중치 계산 등에 필수적인 수학적 도구입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
마르코프 체인은 상태 집합($S$), 전이 확률 행렬($P$), 그리고 초기 상태 분포($\pi_0$)로 구성됩니다.

```text
[ Markov Chain State Transition Diagram ]

      ( 0.7 )               ( 0.4 )
      +-----+               +-----+
      |     |               |     |
      v     |     0.3       |     v
   +-----------+ ------> +-----------+
   |  State A  |         |  State B  |
   | (Sunny)   | <------ | (Rainy)   |
   +-----------+  0.6    +-----------+

[ Transition Probability Matrix (P) ]
         To A   To B
From A [ 0.7    0.3 ]
From B [ 0.6    0.4 ]

* P_ij = P(X_{t+1} = j | X_t = i)
* Sum of each row must be 1.0 (Stochastic Matrix)
```

**핵심 원리:**
1. **마르코프 성질 (Markov Property):** $P(X_{n+1} | X_n, X_{n-1}, ..., X_0) = P(X_{n+1} | X_n)$. 연쇄의 계산 복잡도를 획기적으로 낮춤.
2. **Chapman-Kolmogorov 방정식:** $n$단계 전이 확률은 전이 행렬 $P$를 $n$번 거듭제곱($P^n$)하여 도출 가능.
3. **정상 분포 (Stationary Distribution):** 연쇄가 충분히 반복되었을 때 변하지 않는 확률 분포($\pi P = \pi$). 시스템의 최종적인 균형 상태를 의미.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 마르코프 체인 (Markov Chain) | 은닉 마르코프 모델 (HMM) |
| :--- | :--- | :--- |
| **상태 가시성** | 상태가 직접 관찰됨 (Observable) | 상태는 숨겨져 있고 출력값(Emission)만 관찰됨 |
| **주요 목적** | 상태 변화 예측 및 안정 상태 분석 | 관측 데이터로부터 숨겨진 상태 시퀀스 추론 |
| **대표 사례** | 페이지랭크, 대기행렬 분석 | 음성 인식, 단어 품사 태깅 (POS Tagging) |
| **핵심 변수** | 전이 확률 행렬 (Transition Matrix) | 전이 확률 + 방출 확률 (Emission Probability) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **데이터 엔지니어링 관점:** 웹 로그 데이터로부터 이탈률(Churn)을 계산할 때, 사용자가 특정 페이지에서 다음 페이지로 넘어갈 확률을 마르코프 체인으로 모델링하여 병목 지점 및 최적 경로를 산출할 수 있습니다.
- **기술사적 판단:** 단순 통계보다 동적인 변화를 반영할 수 있는 강력한 프레임워크입니다. 특히 대규모 분산 환경에서는 전이 행렬의 거듭제곱을 병렬 처리(Matrix Multiplication)함으로써 복잡한 그래프 시스템의 영향력을 고속으로 계산하는 것이 핵심 역량입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
마르코프 체인은 AI 시대에 들어 MCMC(Markov Chain Monte Carlo)와 같은 복잡한 확률 분포 샘플링 기법으로 진화하여 베이지안 추론의 핵심이 되었습니다. 강화학습의 MDP(Markov Decision Process) 역시 이 모델의 확장판입니다. 결론적으로, 불확실성이 높은 데이터 스트림 환경에서 시스템의 장기적 거동을 예측하기 위한 가장 견고한 수학적 표준입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Stochastic Process, Probability Theory
- **하위 개념:** Absorbing Markov Chain, Ergodicity, Stationary Distribution
- **연관 기술:** PageRank Algorithm, HMM, Reinforcement Learning (MDP), MCMC

### 👶 어린이를 위한 3줄 비유 설명
1. 개구리가 연못의 연잎 사이를 점프해서 돌아다니는 것과 같아요.
2. 개구리가 다음에 어디로 뛸지는 '지금 밟고 있는 연잎'에서만 결정되고, 예전에 어디에 있었는지는 상관없어요.
3. 오랫동안 개구리가 뛰어놀다 보면, 어떤 연잎에 개구리가 제일 많이 머물게 될지 수학적으로 미리 알 수 있답니다.
