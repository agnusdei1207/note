+++
title = "트랜스포머와 거대 언어 모델 아키텍처 (Transformer & LLM Architecture)"
weight = 1
+++

## 핵심 인사이트 (3줄 요약)
1. **Self-Attention 메커니즘**: 문장 내 모든 단어 간의 연관성을 동시에 계산하여 문맥(Context)을 완벽하게 파악, 순차 처리(RNN)의 병목을 해결함.
2. **병렬 처리 및 확장성(Scalability)**: 데이터의 병렬 처리가 가능해져 대규모 데이터셋과 거대 파라미터(Scaling Law)를 활용한 초거대 AI(LLM)의 기반을 마련함.
3. **Foundation Model 패러다임**: 방대한 데이터로 사전학습(Pre-training)된 거대 모델을 다양한 하위 작업(Downstream Task)에 파인튜닝(Fine-tuning) 또는 프롬프팅으로 재활용하는 혁신.

### Ⅰ. 개요 (Context & Background)
- **정의**: 'Attention Is All You Need(2017)'에서 소개된, 어텐션 메커니즘만을 사용하여 시퀀스-투-시퀀스(Seq2Seq) 작업을 수행하는 신경망 아키텍처.
- **등장 배경**: 기존 RNN/LSTM 모델은 장기 의존성 문제(Long-term Dependency)와 순차 연산으로 인한 학습 속도의 한계를 지니고 있었음.
- **적용 분야**: ChatGPT 등 대화형 AI, 번역, 문서 요약뿐만 아니라 Vision Transformer(ViT)를 통한 이미지 처리, 단백질 구조 예측(AlphaFold)까지 확장.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
트랜스포머의 핵심은 Query, Key, Value 벡터를 활용한 Multi-Head Attention 연산입니다.

```text
+-------------------------------------------------------------+
|            트랜스포머 아키텍처 (Transformer Architecture)          |
+-------------------------------------------------------------+
|                                                             |
|   [Inputs] -> (Word Embedding) + (Positional Encoding)      |
|                       |                                     |
|    +-----------------------------------------------+        |
|    | Encoder Block (N layers)                      |        |
|    |  +-----------------------------------------+  |        |
|    |  |       Multi-Head Self-Attention         |  |        |
|    |  |  (Q, K, V 벡터로 단어 간 상관관계 가중치 계산) |  |        |
|    |  +-----------------------------------------+  |        |
|    |       | (Add & Norm)                          |        |
|    |  +-----------------------------------------+  |        |
|    |  |       Feed Forward Neural Network       |  |        |
|    |  +-----------------------------------------+  |        |
|    |       | (Add & Norm)                          |        |
|    +-------|---------------------------------------+        |
|            | (Context Vectors)                              |
|            v                                                |
|    +-----------------------------------------------+        |
|    | Decoder Block (N layers)  [Autoregressive]    |        |
|    |  +-----------------------------------------+  |        |
|    |  | Masked Multi-Head Self-Attention        |  |        |
|    |  +-----------------------------------------+  |        |
|    |  | Encoder-Decoder Cross-Attention         |  |        |
|    |  +-----------------------------------------+  |        |
|    |  | Feed Forward Neural Network             |  |        |
|    +-----------------------------------------------+        |
|                       |                                     |
|   [Output Probabilities (Softmax)] -> [Next Token Prediction]|
+-------------------------------------------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | RNN / LSTM | Transformer (LLM 기반) |
|---|---|---|
| **데이터 처리 방식** | 순차적 처리 (Sequential) | 병렬 처리 (Parallel) |
| **장기 문맥 (Long Context)** | 정보 소실 발생 (Vanishing Gradient) | 위치에 무관하게 직접 참조 (Global Context) |
| **확장성 (Scalability)** | 하드웨어 가속 한계, 스케일업 어려움 | GPU 클러스터 기반 무한 스케일업 가능 |
| **대표 모델** | Google NMT, 초기 Siri | GPT-4, LLaMA, BERT, Claude |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **RAG (Retrieval-Augmented Generation) 도입**: LLM의 할루시네이션(환각) 현상을 완화하고 기업 내부 데이터를 안전하게 연동하기 위한 검색 증강 생성 아키텍처 필수 적용.
- **파라미터 효율적 튜닝 (PEFT/LoRA)**: 거대 모델 전체를 재학습하는 비용을 절감하기 위해 모델의 가중치는 고정하고 소수의 파라미터만 학습하는 경제적 전략 채택.
- **비용 최적화 (FinOps for AI)**: 토큰(Token) 단위의 과금 체계를 고려한 프롬프트 엔지니어링 최적화 및 경량화 오픈소스 모델(sLLM) 앙상블 운영 고려.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **생산성의 퀀텀 점프**: 코딩 보조(Copilot), 초안 작성, 복잡한 데이터 분석 등 지식 노동의 폭발적인 효율성 증대.
- **초거대 AI 생태계**: 파운데이션 모델(Foundation Model) 위에서 동작하는 수많은 AI 에이전트(Agentic Workflow) 시대로의 진화.
- **표준화 방안**: 오픈 모델의 가중치 공유, 추론 최적화 프레임워크(vLLM, TensorRT-LLM) 표준화 및 AI 프롬프트 보안 가이드라인 수립.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 딥러닝(Deep Learning), 자연어처리(NLP)
- **하위 개념**: Self-Attention, 인코더-디코더(Encoder-Decoder), 사전학습(Pre-training)
- **연관 기술**: 프롬프트 엔지니어링(Prompt Engineering), RAG, 벡터 데이터베이스(Vector DB), LangChain

### 👶 어린이를 위한 3줄 비유 설명
1. **트랜스포머는 '책을 한 번에 전체로 보는 마법의 눈'을 가졌어요.** 예전 컴퓨터는 글씨를 한 글자씩 읽어야 해서 뒤로 가면 앞의 내용을 까먹었거든요.
2. **Self-Attention은 교실 안의 친구들이 누가 누구와 짝꿍인지 한눈에 파악하는 기술**이에요. 그래서 문맥을 정확하게 이해하죠.
3. **거대 언어 모델(LLM)은 세상의 모든 도서관 책을 다 읽어본 아주 똑똑한 앵무새**예요. 질문을 하면 가장 어울리는 다음 단어를 척척 만들어냅니다.