+++
weight = 141
title = "141. BERT (Bidirectional Encoder Representations from Transformers)"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Transformer 인코더를 양방향(Bidirectional)으로 쌓아 문장 전체 문맥을 동시에 이해하는 사전 학습 언어 모델이다.
> 2. **가치**: MLM (Masked Language Model)과 NSP (Next Sentence Prediction)로 방대한 텍스트에서 범용 언어 표현을 학습하고, 소량 데이터로 파인튜닝해 다양한 NLP 태스크에 적용한다.
> 3. **판단 포인트**: BERT는 분류·추출 등 이해(Understanding) 태스크에 최적이고, 생성(Generation) 태스크에는 GPT 계열이 적합하다.

## Ⅰ. 개요 및 필요성

2018년 Google이 발표한 BERT (Bidirectional Encoder Representations from Transformers)는 사전 학습(Pre-training) + 파인튜닝(Fine-tuning) 패러다임을 NLP에 정착시켰다.

기존 GPT(단방향)와 달리 BERT는 왼쪽→오른쪽과 오른쪽→왼쪽 문맥을 동시에 활용한다. "나는 [MASK]에 갔다"에서 MASK 예측 시 "나는"과 "갔다" 양쪽을 모두 참고한다.

**BERT 모델 크기**
- BERT-Base: 12층, 768 차원, 12헤드, 1.1억 파라미터
- BERT-Large: 24층, 1024 차원, 16헤드, 3.4억 파라미터

📢 **섹션 요약 비유**: BERT는 빈칸 채우기 시험을 통해 언어를 배우는 학생인데, 앞뒤 문맥을 모두 보고 답한다.

## Ⅱ. 아키텍처 및 핵심 원리

| 항목 | 설명 |
|:---|:---|
| 아키텍처 | Transformer 인코더 N층 스택 |
| 입력 표현 | Token Embedding + Segment Embedding + Positional Embedding |
| 사전 학습 1 | MLM (Masked Language Model): 15% 토큰 마스킹 후 예측 |
| 사전 학습 2 | NSP (Next Sentence Prediction): 두 문장이 연속인지 판별 |
| 파인튜닝 | [CLS] 토큰 표현을 다운스트림 태스크에 활용 |
| 특수 토큰 | [CLS] (분류), [SEP] (문장 구분), [MASK] (마스킹) |

```
[BERT 입력 구조]

[CLS] 나는  학교에  갔다  [SEP] 오늘도  즐거웠다  [SEP]
  │     │      │      │     │      │        │       │
Token Emb + Segment Emb + Position Emb
  │     │      │      │     │      │        │       │
  └─────────────────────────────────────────────────┘
                          │
              Transformer Encoder ×N층
                          │
  h[CLS]  h[나는]  h[학교에]  ...   h[즐거웠다]
     │
  [CLS] 표현 → 분류 태스크 (감정 분석, 문장 분류 등)
  h[학교에] → 토큰 레벨 태스크 (NER, 질의응답 등)

[MLM 사전 학습]
입력: 나는 [MASK]에 갔다
예측: 학교 (양방향 문맥 활용)
```

**사전 학습 태스크**
- MLM: 무작위 15% 토큰 → 80%는 [MASK]로, 10%는 랜덤 단어로, 10%는 원래 유지
- NSP: 50%는 실제 연속 문장, 50%는 랜덤 문장 쌍 → IsNext/NotNext 분류

📢 **섹션 요약 비유**: BERT의 사전 학습은 수백만 권의 책에서 빈칸 채우기와 문장 순서 맞추기를 끊임없이 연습하는 것이다.

## Ⅲ. 비교 및 연결

| 항목 | BERT | GPT | T5 |
|:---|:---|:---|:---|
| 아키텍처 | 인코더 | 디코더 | 인코더-디코더 |
| 방향성 | 양방향 | 단방향 (좌→우) | 양방향 인코더 |
| 주요 태스크 | 이해, 분류, QA | 생성, 대화 | 번역, 요약, 분류 |
| 사전 학습 | MLM + NSP | LM (다음 토큰 예측) | Span Corruption |
| 대표 파생 | RoBERTa, ALBERT | GPT-3, ChatGPT | mT5, Flan-T5 |

**BERT 기반 한국어 모델**
- KoBERT (SKT): 한국어 위키피디아 기반
- KoELECTRA: ELECTRA 방식 효율화
- KLUE-BERT: 한국어 NLU 벤치마크 최적화

📢 **섹션 요약 비유**: BERT가 독해 전문가라면, GPT는 글쓰기 전문가다. 이해와 생성은 서로 다른 능력이다.

## Ⅳ. 실무 적용 및 기술사 판단

**BERT 파인튜닝 태스크 매핑**
- 문장 분류 (Sentiment Analysis): [CLS] 벡터 → Softmax
- 개체명 인식 (NER): 각 토큰 벡터 → 레이블 분류
- 질의응답 (QA): 시작/끝 토큰 위치 예측
- 자연어 추론 (NLI): 두 문장 관계 분류

**파인튜닝 비용**
- BERT-Base GPU A100에서 소규모 데이터 1~5 에포크로 수 시간 내 가능
- 파라미터 전체 파인튜닝 외 LoRA, Adapter 등 경량 파인튜닝 활용 가능

**기술사 출제 포인트**
- "BERT의 양방향 사전 학습이 단방향 언어 모델 대비 갖는 장점을 설명하시오"
- "MLM 태스크에서 15% 토큰 처리 전략의 이유를 설명하시오"

📢 **섹션 요약 비유**: BERT는 방대한 독서를 통해 언어 감각을 기른 만능 언어 전문가이며, 파인튜닝은 그 전문가에게 특정 업무를 짧게 가르치는 과정이다.

## Ⅴ. 기대효과 및 결론

BERT는 NLP 11개 주요 벤치마크에서 모두 SOTA를 달성하며 "사전 학습 + 파인튜닝" 패러다임을 확립했다. 이후 RoBERTa (더 많은 데이터, NSP 제거), ALBERT (파라미터 공유 경량화), ELECTRA (효율적 사전 학습)로 발전했다.

📢 **섹션 요약 비유**: BERT는 AI 언어 이해의 표준을 세운 모델이다. 파인튜닝만으로 수십 가지 NLP 작업을 해결할 수 있다는 것을 증명했다.

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 기반 | Transformer 인코더 | 양방향 셀프 어텐션 |
| 사전 학습 | MLM (Masked Language Model) | 빈칸 채우기 학습 |
| 사전 학습 | NSP (Next Sentence Prediction) | 문장 연속성 판별 |
| 적용 | Fine-tuning | 다운스트림 태스크 적응 |
| 파생 | RoBERTa | MLM 강화, NSP 제거 |
| 파생 | ALBERT | 파라미터 공유 경량화 |
| 경쟁 | GPT | 생성 특화 단방향 |

### 👶 어린이를 위한 3줄 비유 설명
1. BERT는 수백만 권의 책을 읽고 빈칸 채우기를 무한히 연습한 초독서가예요.
2. 앞뒤 문맥을 모두 보고 빈칸을 채우기 때문에 단방향보다 훨씬 똑똑해요.
3. 이렇게 배운 언어 감각을 바탕으로 감정 분석, 번역, 질문 답하기 등 다양한 일을 할 수 있어요.
