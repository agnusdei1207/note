+++
weight = 128
title = "인공 신경망 (ANN) 및 다층 퍼셉트론 (MLP)"
date = "2026-03-04"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
- 인공 신경망(ANN)은 인간 뇌의 뉴런 구조를 모방하여 비선형적인 복잡한 데이터 패턴을 학습하는 딥러닝의 기본 모델이다.
- 다층 퍼셉트론(MLP)은 입력층, 하나 이상의 은닉층, 출력층으로 구성되며 역전파(Backpropagation) 알고리즘을 통해 가중치를 최적화한다.
- 심층 신경망(DNN)의 토대가 되어 이미지, 음성, 자연어 처리 등 현대 AI 기술의 폭발적인 발전을 이끈 핵심 기술이다.

### Ⅰ. 개요 (Context & Background)
인공 신경망은 1950년대 퍼셉트론(Perceptron)에서 시작되었으나 선형 분리 불가능 문제(XOR 문제)로 정체기를 겪었다. 이후 다층 구조와 역전파 알고리즘의 도입으로 비선형 문제를 해결하며 화려하게 부활했다. 현대의 모든 딥러닝 아키텍처(CNN, RNN, Transformer 등)는 이 기본적인 ANN/MLP의 가중치 학습 원리를 공유한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
ANN의 핵심은 **가중치(Weight) 합산**과 **활성화 함수(Activation Function)**를 통한 정보의 비선형 변환이다.

```text
[ MLP Architecture / 다층 퍼셉트론 구조 ]

 Input Layer     Hidden Layer(s)    Output Layer
 (입력층)          (은닉층)           (출력층)
    ○ -------------- ○ -------------- ○
    ○ --(Weights)--- ○ --(Weights)--- ○
    ○ -------------- ○ -------------- ○
    
[ Basic Neuron Unit / 기본 뉴런 연산 ]
x1 --- w1 ---\
x2 --- w2 ---> [ Sum: Σ(xi*wi + b) ] -> [ Activation: f(z) ] -> Output (y)
xn --- wn ---/
```

1.  **순전파 (Forward Propagation):** 입력 데이터가 각 층의 가중치와 곱해지고 활성화 함수를 거쳐 출력층까지 전달된다.
2.  **손실 함수 (Loss Function):** 예측값과 실제 정답 사이의 오차를 계산한다 (MSE, Cross Entropy 등).
3.  **역전파 (Backpropagation):** 연쇄 법칙(Chain Rule)을 이용하여 출력층의 오차를 입력층 방향으로 거슬러 올라가며 각 가중치의 기울기(Gradient)를 계산한다.
4.  **가중치 업데이트:** 경사 하강법(Gradient Descent)을 통해 오차를 줄이는 방향으로 가중치를 미세하게 조정한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구분 | 단층 퍼셉트론 (SLP) | 다층 퍼셉트론 (MLP) |
| :--- | :--- | :--- |
| **층 구조** | 입력층 - 출력층 | 입력층 - 은닉층(1개 이상) - 출력층 |
| **해결 가능 문제** | 선형 분리 가능 (OR, AND) | 비선형 분리 가능 (XOR 등 복잡한 패턴) |
| **핵심 알고리즘** | Delta Rule | 역전파 (Backpropagation) |
| **활성화 함수** | 계단 함수 (Step Function) | Sigmoid, ReLU, Tanh 등 |
| **한계점** | 표현 능력의 극심한 제한 | 과적합 위험, 기울기 소실(Vanishing Gradient) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **범용 근사 정리 (Universal Approximation Theorem):** 충분히 많은 뉴런과 은닉층이 있다면 어떤 복잡한 함수도 근사할 수 있다는 이론적 근거를 제공한다.
- **깊이의 함정:** 층을 무조건 깊게 쌓는다고 성능이 올라가지는 않는다. 기울기 소실 문제나 계산 복잡도 증가를 고려해야 하며, 이를 해결하기 위해 ReLU 활성화 함수나 Batch Normalization 같은 기법이 실무에서 필수적으로 사용된다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
ANN과 MLP는 '설명 가능성(XAI)' 측면에서는 블랙박스라는 비판을 받지만, 데이터가 충분할 때 보여주는 성능은 압도적이다. 최근에는 물리 법칙을 신경망에 주입하는 PINN(Physics-Informed Neural Networks)이나 경량화된 온디바이스 AI 등으로 진화하며 전 산업 영역의 표준 아키텍처로 자리 잡았다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 딥러닝 (Deep Learning), 머신러닝 (Machine Learning)
- **하위 개념:** 뉴런 (Perceptron), 은닉층 (Hidden Layer), 역전파 (Backpropagation)
- **연관 기술:** 활성화 함수, 손실 함수, 옵티마이저 (SGD, Adam)

### 👶 어린이를 위한 3줄 비유 설명
- 우리 머릿속에 있는 뇌 세포들이 서로 신호를 주고받으며 공부하는 방식을 컴퓨터로 만든 거예요.
- 처음에는 틀린 답을 내놓기도 하지만, 틀릴 때마다 조금씩 수정을 하면서 정답을 맞히는 법을 배워요.
- 마치 수천 개의 퀴즈 문제를 풀면서 똑똑해지는 마법 상자와 같답니다!
