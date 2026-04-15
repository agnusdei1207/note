+++
title = "트랜스포머 아키텍처 (Transformer Architecture)"
weight = 123
date = "2024-03-21"
[extra]
categories = ["AI", "DeepLearning", "NLP"]
+++

## 핵심 인사이트 (3줄 요약)
- **Attention Is All You Need**: RNN이나 CNN 없이 오직 셀프 어텐션(Self-Attention) 메커니즘만으로 시퀀스 데이터를 처리하여 병렬 연산 효율을 극대화한 아키텍처임.
- **장기 의존성 문제 해결**: 거리와 관계없이 모든 토큰 간의 상관관계를 직접 계산함으로써, 기존 시퀀셜 모델의 정보 소실 문제를 근본적으로 극복함.
- **현대 LLM의 근간**: BERT, GPT 등 현재 모든 초거대 언어 모델의 표준 뼈대로 자리 잡으며 자연어 처리를 넘어 비전, 음성 분야까지 확장됨.

### Ⅰ. 개요 (Context & Background)
- **배경**: 이전의 RNN/LSTM은 순차적 처리 특성상 학습 속도가 느리고, 문장이 길어질수록 초기 정보가 소실되는 한계가 있었음.
- **정의**: 2017년 구글이 제안한 인코더-디코더 구조의 모델로, 단어 간의 연관성을 수치화하는 '어텐션'을 핵심 동력으로 사용함.
- **영향**: 시퀀스 모델링의 패러다임을 '순차 처리'에서 '병렬 행렬 연산'으로 전환시켜 대규모 데이터 학습의 문을 열었음.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ Transformer Architecture: Key Components ]

      Input Tokens                     Output Tokens
           |                                |
   [Positional Encoding]            [Positional Encoding]
           |                                |
    +--------------+                 +--------------+
    | Multi-Head   |                 | Masked Multi |
    | Self-Attention|                | Head Attention|
    +--------------+                 +--------------+
           |                                |
    +--------------+                 +--------------+
    | Feed Forward |<----Attention----| Multi-Head   |
    | Network      |      Connect     | Cross-Attn   |
    +--------------+                 +--------------+
       (Encoder)                        (Decoder)

[ Scaled Dot-Product Attention ]
Attention(Q, K, V) = softmax( (QK^T) / sqrt(dk) ) * V
- Q (Query): 찾고자 하는 정보
- K (Key): 정보의 인덱스/라벨
- V (Value): 실제 정보 값
```
- **Self-Attention**: 문장 내의 단어들이 서로 어떤 관계를 갖는지 스스로 학습함 (예: 'it'이 무엇을 지칭하는지 파악).
- **Multi-Head Attention**: 여러 개의 어텐션을 병렬로 수행하여 문법, 의미, 문맥 등 다양한 관점에서 정보를 추출함.
- **Positional Encoding**: 단어의 순서 정보를 알려주기 위해 사인/코사인 함수를 이용한 위치 값을 임베딩에 더해줌.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | RNN / LSTM | Transformer |
| :--- | :--- | :--- |
| **연산 방식** | 순차적 (Sequential) | 병렬적 (Parallel) |
| **학습 속도** | 느림 (GPU 활용 한계) | 매우 빠름 (행렬 연산 최적화) |
| **장기 의존성** | 거리가 멀면 정보 유실 | 모든 거리에서 동일한 관계 계산 |
| **모델 구조** | 재귀적 루프 | 셀프 어텐션 스택 |
| **주요 활용** | 초기 챗봇, 번역기 | GPT, BERT, Llama 등 최신 AI |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **확장성(Scalability)**: 모델의 크기(파라미터 수)와 데이터 양을 늘릴수록 성능이 비약적으로 향상되는 Scaling Law가 적용되는 최적의 구조임.
- **전이 학습(Transfer Learning)**: 거대 코퍼스로 사전 학습(Pre-training)된 트랜스포머 모델을 하위 태스크에 미세 조정(Fine-tuning)하여 고성능 달성이 가능함.
- **기술사적 판단**: 트랜스포머는 단순한 알고리즘을 넘어 '범용 아키텍처'로 진화하고 있으며, 비전 트랜스포머(ViT) 등을 통해 도메인 간 경계가 무너지는 융합의 핵심임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **AGI로의 진화**: 인간의 사고 방식과 유사하게 문맥을 통합적으로 이해하는 능력을 갖추어 범용 인공지능(AGI) 구현의 핵심 기술로 평가받음.
- **효율화 과제**: 연산 복잡도가 시퀀스 길이의 제곱($O(n^2)$)에 비례하는 문제를 해결하기 위해 FlashAttention 등 최적화 기술이 지속 연구됨.
- **결론**: 트랜스포머는 딥러닝 역사에서 가장 중요한 변곡점 중 하나이며, 이를 깊이 이해하는 것은 현대 AI 엔지니어링의 필수 소양임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **Self-Attention**: 핵심 메커니즘
- **Multi-Head Attention**: 표현력 강화
- **BERT / GPT**: 대표적 파생 모델
- **Scaling Law**: 모델 확장성 이론

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날에는 책을 읽을 때 한 글자씩 차례대로 읽느라 앞 내용을 잊어버리곤 했어요.
2. 트랜스포머는 한 페이지를 한눈에 훑어보며 중요한 단어들끼리 선으로 연결해서 읽는 천재 독서가 같아요.
3. 덕분에 아주 긴 이야기도 한순간에 이해하고 멋진 대답을 해줄 수 있답니다!
