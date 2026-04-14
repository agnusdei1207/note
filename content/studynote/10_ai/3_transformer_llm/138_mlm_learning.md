+++
title = "MLM 학습 (Masked Language Modeling)"
date = "2025-05-15"
weight = 138
[extra]
categories = ["ai", "transformer-llm"]
+++

## 핵심 인사이트 (3줄 요약)
- **문맥 이해의 핵심**: 문장 내 일부 단어를 빈칸(`[MASK]`)으로 가리고 주변 단어를 통해 빈칸을 맞추는 자기 지도 학습 기법임.
- **양방향(Bidirectional) 학습**: 앞 단어만 보고 다음 단어를 예측하는 방식과 달리, 단어의 좌우 문맥을 동시에 파악하여 깊이 있는 의미를 추출함.
- **BERT의 기반 기술**: 구글의 BERT 모델을 성공시킨 핵심 학습 목표로, 텍스트 분류 및 개체명 인식 성능을 비약적으로 향상시킴.

### Ⅰ. 개요 (Context & Background)
MLM(Masked Language Modeling)은 자연어 처리(NLP)에서 라벨링되지 않은 방대한 텍스트 데이터를 스스로 학습하기 위해 고안된 'Pre-training' 기법이다. 기존의 통계적 언어 모델들이 왼쪽에서 오른쪽으로만 읽는 한계를 극복하기 위해, 문장 중간에 구멍을 뚫고 이를 메우는 '빈칸 채우기 문제'를 통해 언어의 구조와 의미를 학습한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
입력 데이터의 약 15% 정도를 무작위로 선정하여 마스킹을 수행한다.

```text
[ MLM Learning Process - MLM 학습 프로세스 ]

   Input Sentence: "The cat sat on the mat."
          |
   Masking (15%):
          |-- 80%: Replace with [MASK] -> "The cat [MASK] on the mat."
          |-- 10%: Replace with Random -> "The cat [apple] on the mat."
          |-- 10%: Keep unchanged     -> "The cat sat on the mat."
          |
   +------------------------------------+
   |   Transformer Encoder (Bidirectional) |
   +------------------------------------+
          |
   Prediction: [MASK] is likely "sat"
          |
   Loss: Cross-Entropy (Predicted vs Original)
```

**학습 디테일:**
1. **양방향 어텐션**: 인코더의 모든 층에서 양방향 정보를 활용하여 각 토큰의 표현력을 극대화함.
2. **다양한 변형**: RoBERTa 등 이후 모델에서는 마스킹 패턴을 고정하지 않고 매 에폭마다 바꾸는 **Dynamic Masking**을 사용하여 성능을 더욱 높임.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | MLM (Masked LM) | CLM (Causal LM / Next Token Prediction) |
| :--- | :--- | :--- |
| **학습 방향** | 양방향 (Bidirectional) | 단방향 (Auto-regressive) |
| **대표 모델** | BERT, RoBERTa, ALBERT | GPT series, Llama |
| **주요 강점** | 문맥 이해, 텍스트 분석, 문장 분류 | 텍스트 생성, 대화, 창의적 글쓰기 |
| **학습 데이터** | 문장 내부 관계 중심 | 시퀀스 흐름 중심 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **도메인 특화 학습**: 법률, 의료 등 특정 도메인의 비라벨 데이터를 MLM으로 사전 학습시킨 후 태스크를 수행하면 비약적인 성능 향상을 얻을 수 있다.
- **기술사적 판단**: 생성형 AI가 대세인 현재에도, 검색 엔진의 랭킹 모델이나 스팸 탐지, 감성 분석 등 '이해'가 중요한 영역에서는 MLM 기반의 인코더 모델이 훨씬 경제적이고 정확한 솔루션이다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
MLM은 언어 모델이 단순히 단어의 빈도를 외우는 것이 아니라, 문맥적 의미(Contextual Meaning)를 포착하게 만든 혁신적인 기법이다. 최근에는 텍스트뿐만 아니라 이미지(Masked Image Modeling), 음성 데이터의 사전 학습에도 이 원리가 적용되며 멀티모달 AI의 표준 학습법으로 확장되고 있다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위**: 자기 지도 학습 (Self-Supervised Learning), NLP
- **하위**: Whole Word Masking (WWM), Dynamic Masking
- **연관**: BERT, NSP, Transformer Encoder, SpanBERT

### 👶 어린이를 위한 3줄 비유 설명
1. 문장 속에서 몇 단어를 손가락으로 가리고, "여기에 들어갈 단어는 뭘까?"라고 퀴즈를 내는 거예요.
2. 앞뒤 단어들을 잘 살펴보면 가려진 단어가 무엇인지 짐작할 수 있게 되죠.
3. 이 퀴즈를 수천만 번 풀다 보면, 어떤 문장이든 찰떡같이 이해하는 언어 박사가 된답니다.
