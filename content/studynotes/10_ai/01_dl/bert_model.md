+++
title = "BERT (Bidirectional Encoder Representations from Transformers)"
date = "2026-03-04"
[extra]
categories = ["studynotes-10_ai"]
+++

# BERT (Bidirectional Encoder Representations from Transformers)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트랜스포머의 인코더만을 사용하여 양방향(Bidirectional) 문맥을 동시에 학습하는 사전 학습 언어 모델로, MLM(Masked Language Model)과 NSP(Next Sentence Prediction)로 대규모 텍스트에서 언어 이해 능력을 획득합니다.
> 2. **가치**: 11개 NLP 태스크에서 SOTA 달성, 파인튜닝만으로 다양한下游 작업 수행, GLUE 벤치마크에서 인간 능가, NLP 분야의 ImageNet 같은 역할을 수행했습니다.
> 3. **융합**: 질의응답, 감성 분석, 개체명 인식, 문장 분류 등 모든 NLP下游 태스크의 기반 모델로, RoBERTa, ALBERT, DeBERTa 등 다양한 변형 모델의 출발점입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**BERT(Bidirectional Encoder Representations from Transformers)**는 2018년 Google AI 연구팀이 발표한 사전 학습 언어 모델입니다. 핵심 특징은 **(1) 양방향 문맥 학습, (2) 마스크드 언어 모델링(MLM), (3) 전이 학습을 위한 표현 학습**입니다.

**사전 학습 태스크**:
1. **Masked Language Model (MLM)**: 입력 토큰의 15%를 [MASK]로 대체 후 예측
2. **Next Sentence Prediction (NSP)**: 두 문장이 연속인지 분류

**모델 규모**:
- BERT-Base: 12층, 768 hidden, 12 heads, 110M 파라미터
- BERT-Large: 24층, 1024 hidden, 16 heads, 340M 파라미터

#### 2. 💡 비유를 통한 이해
BERT는 **'독해 만점자'**에 비유할 수 있습니다:

- **양방향 학습**: 문장의 앞과 뒤를 동시에 읽으면서 "이 단어는 이런 의미구나" 파악. GPT는 앞에서 뒤로만 읽음.
- **MLM (빈칸 채우기)**: "나는 [MASK]를 먹었다"에서 빈칸에 "밥", "사과" 등을 예측.
- **NSP (문장 연결)**: "안녕하세요?" 다음에 "반갑습니다"가 오는지 "오늘 날씨가 춥네요"가 오는지 판단.

#### 3. 등장 배경 및 발전 과정

1.  **기존 기술의 한계**:
    - **단방향 모델**: ELMo, GPT는 왼쪽→오른쪽으로만 문맥 활용. "은행"의 의미가 뒤에 나오는 단어에 따라 달라지는 것을 완전히 파악 못함.
    - **태스크별 모델**: 각 NLP 태스크마다 별도 모델 설계 필요.

2.  **혁신적 패러다임**:
    - **BERT (2018)**: 양방향 학습으로 문맥 이해력 획기적 향상
    - **RoBERTa (2019)**: 더 많은 데이터, 더 긴 학습, NSP 제거
    - **ALBERT (2019)**: 파라미터 공유로 경량화
    - **DeBERTa (2020)**: Disentangled Attention으로 성능 향상
    - **SpanBERT, DistilBERT, TinyBERT** 등 다양한 변형

3.  **영향력**: NLP 분야의 판도를 바꾸어, "Pre-training + Fine-tuning" 패러다임 확립.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. BERT 구성 요소

| 요소 | 역할 | 설명 |
|:---|:---|:---|
| **Token Embedding** | 단어 표현 | WordPiece 토크나이저 (30,000 vocab) |
| **Position Embedding** | 위치 정보 | 학습 가능한 위치 임베딩 (최대 512) |
| **Segment Embedding** | 문장 구분 | 문장 A/B 구분 (0/1) |
| **Transformer Encoder** | 문맥 학습 | 12층 (Base) / 24층 (Large) |
| **[CLS] Token** | 문장 표현 | 첫 토큰, 분류 태스크용 |
| **[SEP] Token** | 문장 구분 | 두 문장 사이 구분자 |
| **[MASK] Token** | MLM용 | 학습 시 15% 토큰 대체 |

#### 2. BERT 입력 표현

```
입력: [CLS] 나는 사과를 좋아한다 [SEP] 사과는 맛있다 [SEP]

Token Emb:    [CLS]  나는  사과를  좋아한다  [SEP]  사과는  맛있다  [SEP]
Segment Emb:    0     0      0        0        0      1      1       1
Position Emb:   0     1      2        3        4      5      6       7

최종 입력 = Token Emb + Segment Emb + Position Emb
```

#### 3. 사전 학습 태스크

**MLM (Masked Language Model)**:
- 입력의 15% 토큰 선택
- 80% → [MASK], 10% → 랜덤 토큰, 10% → 원래 토큰
- 주변 문맥으로 마스크된 토큰 예측

**NSP (Next Sentence Prediction)**:
- 입력: [CLS] 문장A [SEP] 문장B [SEP]
- 50% 실제 다음 문장, 50% 랜덤 문장
- [CLS] 토큰의 출력으로 이진 분류

#### 4. PyTorch BERT 구현 예시

```python
import torch
import torch.nn as nn
from transformers import BertModel, BertTokenizer

class BERTClassifier(nn.Module):
    def __init__(self, model_name='bert-base-uncased', num_classes=2):
        super().__init__()
        self.bert = BertModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_classes)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        cls_output = outputs.last_hidden_state[:, 0, :]  # [CLS] token
        return self.classifier(self.dropout(cls_output))
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### BERT vs GPT 비교

| 항목 | BERT | GPT |
|:---|:---|:---|
| **구조** | Encoder only | Decoder only |
| **방향** | 양방향 | 단방향 (left-to-right) |
| **사전학습** | MLM, NSP | Next Token Prediction |
| **강점** | 이해, 분류, 질의응답 | 생성, 작문 |
| **용도** | 분류, NER, QA | 텍스트 생성 |

#### BERT 변형 모델

| 모델 | 특징 | 개선점 |
|:---|:---|:---|
| **RoBERTa** | 동적 마스킹, 더 많은 데이터 | 성능 향상 |
| **ALBERT** | 파라미터 공유, 인자 분해 | 경량화 |
| **DeBERTa** | 분리된 어텐션 | 성능 향상 |
| **DistilBERT** | 지식 증류 | 40% 축소, 60% 빠름 |

---

### Ⅳ. 실무 적용

#### 파인튜닝 시나리오

1. **텍스트 분류**: [CLS] 토큰 + Linear layer
2. **개체명 인식(NER)**: 각 토큰 분류
3. **질의응답**: Start/End position 예측
4. **유사도 계산**: 두 문장 임베딩 코사인 유사도

#### 한국어 BERT

- KoBERT (SKT), K-BERT, KoELECTRA 등
- 한국어 WordPiece/Morpheme 토크나이저 적용

---

### Ⅴ. 결론

BERT는 NLP 분야에서 양방향 문맥 학습의 중요성을 입증하며, 사전 학습된 언어 모델의 시대를 열었습니다. 현재도 다양한下游 태스크의 기반 모델로 활용됩니다.

---

### 📌 관련 개념 맵
- [트랜스포머](@/studynotes/10_ai/01_dl/transformer_architecture.md)
- [GPT](@/studynotes/10_ai/01_dl/gpt_model.md)
- [전이 학습](@/studynotes/10_ai/02_ml/transfer_learning.md)
- [NLP 기초](@/studynotes/10_ai/02_ml/nlp_fundamentals.md)
- [파인튜닝](@/studynotes/10_ai/01_dl/fine_tuning.md)

---

### 👶 어린이를 위한 3줄 비유
1. **양방향 독서**: BERT는 책을 앞에서 뒤로, 뒤에서 앞으로 동시에 읽으면서 이해해요.
2. **빈칸 채우기**: "나는 [MASK]를 먹었다"에서 빈칸이 뭔지 맞추면서 단어의 의미를 배워요.
3. **만능 독해왕**: 한번 많이 공부해두면, 시험 문제 풀기, 요약하기, 질문 대답하기 다 잘할 수 있어요!
