+++
weight = 139
title = "139. 트랜스포머 (Transformer) 아키텍처 - 셀프 어텐션 병렬 처리"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 순환(Recurrence) 없이 셀프 어텐션(Self-Attention)만으로 시퀀스 전체를 한 번에 병렬 처리하는 혁신적 아키텍처이다.
> 2. **가치**: RNN/LSTM의 순차 처리 병목을 제거해 GPU 병렬 처리로 대규모 언어 모델(LLM) 학습을 가능하게 했다.
> 3. **판단 포인트**: 인코더 스택(BERT 계열)은 양방향 이해에, 디코더 스택(GPT 계열)은 자동회귀 생성에 특화되며, 인코더-디코더 결합은 번역·요약에 사용한다.

## Ⅰ. 개요 및 필요성

2017년 Google의 "Attention is All You Need" 논문에서 Vaswani 등이 제안한 Transformer는 순환 신경망(RNN/LSTM)을 완전히 배제하고, 어텐션 메커니즘만으로 자연어 처리(NLP) 전반을 혁신했다.

핵심 아이디어: 시퀀스의 모든 위치가 서로를 직접 참조(O(1) 경로) → 장거리 의존성 문제 소멸, GPU 병렬 학습 가능.

**RNN vs Transformer 비교**
- RNN: 순차 처리 O(n), 장거리 의존성 취약
- Transformer: 병렬 처리 O(1), 전역 문맥 직접 접근

📢 **섹션 요약 비유**: RNN이 전화 메시지를 한 사람씩 전달하는 것이라면, Transformer는 모든 사람이 동시에 이야기를 나누는 원탁 회의다.

## Ⅱ. 아키텍처 및 핵심 원리

| 모듈 | 구성 | 역할 |
|:---|:---|:---|
| 입력 임베딩 | Token Embedding + Positional Encoding | 토큰을 벡터로 변환, 위치 정보 주입 |
| Multi-Head Self-Attention | h개 병렬 어텐션 헤드 | 다양한 관점에서 문맥 포착 |
| Feed-Forward Network (FFN) | 2층 선형 변환 + ReLU | 위치별 비선형 변환 |
| Layer Normalization | 레이어 정규화 | 학습 안정화 |
| Residual Connection | 잔차 연결 | 기울기 직접 전달 |
| Encoder Stack | N×(Attention + FFN) | 입력 문맥 표현 |
| Decoder Stack | N×(Masked Attention + Cross-Attention + FFN) | 출력 생성 |

```
[Transformer 전체 구조]

     입력 시퀀스                     출력 시퀀스 (시프트)
         │                                  │
  [Input Embedding]               [Output Embedding]
  [Positional Encoding]           [Positional Encoding]
         │                                  │
┌────────▼──────────┐           ┌───────────▼──────────┐
│   ENCODER STACK   │           │    DECODER STACK      │
│  ┌─────────────┐  │           │  ┌──────────────────┐ │
│  │Multi-Head   │  │           │  │Masked Multi-Head │ │
│  │Self-Attention│ │           │  │Self-Attention    │ │
│  └──────┬──────┘  │           │  └────────┬─────────┘ │
│  Add & LayerNorm  │           │  Add & LayerNorm       │
│  ┌──────▼──────┐  │           │  ┌────────▼─────────┐ │
│  │Feed-Forward │  │  ──────▶  │  │Cross-Attention   │ │
│  │  Network    │  │  인코더   │  │(Encoder Output)  │ │
│  └──────┬──────┘  │  출력     │  └────────┬─────────┘ │
│  Add & LayerNorm  │           │  Add & LayerNorm       │
│  (×N층 반복)      │           │  ┌────────▼─────────┐ │
└───────────────────┘           │  │Feed-Forward Net  │ │
                                │  └────────┬─────────┘ │
                                │  (×N층 반복)          │
                                └───────────┬────────────┘
                                            │
                                     Linear + Softmax
                                            │
                                       최종 출력 확률
```

📢 **섹션 요약 비유**: Transformer는 여러 전문가 패널이 동시에 발언하고(Multi-Head), 모든 사람의 의견을 즉시 종합해(Self-Attention) 결론을 내리는 회의 시스템이다.

## Ⅲ. 비교 및 연결

| 아키텍처 | 구성 | 대표 모델 | 특화 |
|:---|:---|:---|:---|
| 인코더 전용 | 인코더 N층 | BERT, RoBERTa | 문장 이해, 분류 |
| 디코더 전용 | 디코더 N층 (Masked) | GPT 시리즈 | 텍스트 생성 |
| 인코더-디코더 | 인코더 + 디코더 | T5, BART | 번역, 요약 |

**Transformer 크기 스케일링**
- GPT-1: 1억 파라미터 (12층, 768 차원)
- GPT-3: 1,750억 파라미터 (96층, 12,288 차원)
- GPT-4: 추정 1조+ 파라미터

📢 **섹션 요약 비유**: 인코더는 원문을 분석하는 독해 전문가, 디코더는 글을 생성하는 작가이며, 인코더-디코더 결합은 번역가 역할이다.

## Ⅳ. 실무 적용 및 기술사 판단

**Transformer 기반 서비스 사례**
- ChatGPT / GPT-4: GPT 디코더 기반 대화 AI
- Google BERT: 검색 엔진 의도 파악
- Google Translate: T5 기반 번역
- GitHub Copilot: Codex (GPT 계열) 코드 생성

**설계 고려 사항**
- 컨텍스트 길이 (Context Window): 어텐션은 O(n²) 메모리 → 긴 시퀀스는 Sliding Window, Sparse Attention 필요
- 포지셔널 인코딩: 절대 위치 (원래 Transformer) vs 상대 위치 (RoPE, ALiBi)

**기술사 출제 포인트**
- "Transformer의 Positional Encoding이 필요한 이유와 구현 방식을 설명하시오"
- "인코더 전용/디코더 전용/인코더-디코더 아키텍처의 차이와 적합한 태스크를 설명하시오"

📢 **섹션 요약 비유**: Transformer는 AI 역사의 '인터넷 발명'과 같다. 이전 모든 아키텍처의 한계를 한 번에 뛰어넘어 새 시대를 열었다.

## Ⅴ. 기대효과 및 결론

Transformer는 NLP를 넘어 컴퓨터 비전(ViT, Vision Transformer), 단백질 구조 예측(AlphaFold), 음악 생성, 코드 생성까지 확장되었다. 2017년 논문 이후 AI 연구의 표준 아키텍처가 되었으며, 대규모 언어 모델(LLM) 시대를 열었다.

📢 **섹션 요약 비유**: Transformer는 AI에게 병렬로 생각하는 능력을 준 발명이다. 한 가지를 순서대로 처리하던 AI가 모든 것을 동시에 바라볼 수 있게 됐다.

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 핵심 논문 | Attention is All You Need (2017) | Google Brain 발표 |
| 핵심 모듈 | Multi-Head Self-Attention | 다각도 병렬 어텐션 |
| 핵심 모듈 | Positional Encoding | 위치 정보 주입 |
| 파생 | BERT | 양방향 인코더 |
| 파생 | GPT | 단방향 디코더 |
| 파생 | T5, BART | 인코더-디코더 |
| 확장 | Vision Transformer (ViT) | 이미지 처리 |

### 👶 어린이를 위한 3줄 비유 설명
1. Transformer는 모든 단어가 다른 모든 단어를 동시에 보면서 의미를 파악하는 마법 독서 방법이에요.
2. 줄 세워서 차례차례 전달하던 것을 "모두 동시에 이야기"로 바꿔서 훨씬 빨라졌어요.
3. ChatGPT, Google 번역 모두 이 아이디어 위에서 만들어졌어요.
