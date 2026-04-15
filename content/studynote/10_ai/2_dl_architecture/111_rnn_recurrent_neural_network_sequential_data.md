+++
title = "111. 순환 신경망 (RNN, Recurrent Neural Network)"
weight = 112
date = "2024-11-20"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
1. **순환 신경망(RNN)**은 음성, 텍스트, 주식 가격과 같이 시간에 따라 순차적으로 발생하는 시계열(Sequential) 데이터 처리에 특화된 딥러닝 아키텍처입니다.
2. 내부에 루프(Loop) 구조를 가져 이전 단계의 출력(Hidden State)을 현재 단계의 입력으로 재활용함으로써 과거의 문맥(Context)을 기억합니다.
3. 정보가 길어질수록 과거의 기억이 희미해지는 장기 의존성(Long-term Dependency) 문제와 기울기 소실(Vanishing Gradient) 한계를 지니고 있어 LSTM과 GRU로 발전하게 되었습니다.

### Ⅰ. 개요 (Context & Background)
기존의 인공 신경망(FNN, CNN)은 모든 입력과 출력이 서로 독립적이라고 가정합니다. 하지만 우리가 일상에서 접하는 문장이나 날씨 데이터는 앞뒤 문맥과 순서가 매우 중요합니다. **RNN(Recurrent Neural Network)**은 정보가 네트워크 내부에서 순환하는 경로를 도입하여, 시간의 흐름(Time Step)에 따른 순차적인 데이터를 모델링하고 앞의 정보가 뒤의 정보에 영향을 미치도록 설계된 혁신적인 신경망 모델입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
RNN의 가장 큰 특징은 **은닉 상태(Hidden State)**를 관리하는 순환 구조입니다. 시간 $t$에서의 은닉 상태 $h_t$는 현재의 입력 $x_t$와 이전 시간 단계의 은닉 상태 $h_{t-1}$을 모두 고려하여 업데이트됩니다. 이로 인해 RNN은 입력 시퀀스에 대한 일종의 '기억(Memory)'을 유지하게 됩니다.

수식으로는 다음과 같이 표현됩니다:
$$ h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_h) $$
$$ y_t = W_{hy} h_t + b_y $$

```text
[RNN Unfolded Architecture]

           y_(t-1)         y_t           y_(t+1)
             ^              ^               ^
             |              |               |
             W_hy           W_hy            W_hy
             |              |               |
 ... -> [Hidden h_(t-1)] -> [Hidden h_t] -> [Hidden h_(t+1)] -> ...
             ^              ^               ^
             |              |               |
             W_xh           W_xh            W_xh
             |              |               |
          x_(t-1)          x_t           x_(t+1)

* x_t: Input at time t
* h_t: Hidden State (Memory) at time t
* y_t: Output at time t
* W_hh: Hidden-to-Hidden Weight Matrix (Shared across time)
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구분 (Category) | CNN (Convolutional Neural Network) | RNN (Recurrent Neural Network) |
| :--- | :--- | :--- |
| **주요 처리 데이터** | 이미지, 공간적 구조 데이터 (Grid) | 텍스트, 음성, 시계열 데이터 (Sequence) |
| **핵심 연산 원리** | 공간적인 필터(Kernel) 이동 및 합성곱 연산 | 시간 축(Time Step)을 따른 은닉 상태 순환 및 유지 |
| **입출력 길이** | 고정된 크기의 입출력 처리 | 가변적인 길이의 시퀀스 입출력 가능 |
| **치명적 단점** | 픽셀 간 멀리 떨어진 공간 관계 파악의 한계 | 문장이 길어질 경우 장기 의존성(기울기 소실) 문제 발생 |
| **주요 발전 모델** | ResNet, VGG, YOLO | LSTM, GRU, Seq2Seq |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **적용 도메인 선정:** RNN 기반 모델은 기계 번역(Machine Translation), 음성 인식(Speech Recognition), 텍스트 생성, 주가 예측 등 순서가 의미를 갖는 동적 시스템에서 탁월한 성과를 보입니다.
- **성능 한계와 아키텍처 전환:** 기본 RNN(Vanilla RNN)은 'BPTT(Backpropagation Through Time)' 수행 시 활성화 함수(tanh)의 누적 곱셈으로 인해 기울기 소실 현상이 급격히 발생합니다. 실무에서는 이러한 한계를 극복하기 위해 기본 RNN 대신 **LSTM**이나 **GRU**를 기본으로 채택하며, 최근 초거대 언어 처리에서는 완전히 어텐션 기반의 **Transformer** 아키텍처로 넘어가고 있습니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
RNN은 시계열 데이터 분석과 자연어 처리(NLP) 분야에 획기적인 전환점을 가져온 근간 아키텍처입니다. 비록 어텐션 메커니즘과 트랜스포머의 등장으로 그 위상이 다소 축소되었으나, 시계열 데이터를 순차적으로 처리하는 본질적 효율성과 가벼운 연산 특성으로 인해 여전히 소규모 임베디드 시스템, 센서 시계열 분석, 음성 스트리밍 디코딩 등 특정 분야에서는 강력한 표준 기술로 활용되고 있습니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 인공 신경망(ANN), 딥러닝(Deep Learning)
- **하위 개념:** BPTT, 기울기 소실(Vanishing Gradient), 은닉 상태(Hidden State)
- **관련 기술:** LSTM, GRU, 자연어 처리(NLP), 트랜스포머(Transformer)

### 👶 어린이를 위한 3줄 비유 설명
1. **RNN:** 친구가 한 글자씩 불러주는 비밀번호를 외울 때, 머릿속에 방금 들은 글자와 예전에 들은 글자를 계속 합쳐서 기억하는 방법이에요.
2. 책을 읽을 때 앞 페이지 내용을 기억해야 지금 페이지의 내용이 이해가 가는 것과 똑같아요.
3. 하지만 글이 너무 길어지면 앞부분을 까먹어버리는 '기억상실증' 단점이 있어서, 메모장을 쓰는 새로운 방법(LSTM)이 나오게 되었답니다.
