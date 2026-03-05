+++
title = "GPT (Generative Pre-trained Transformer)"
date = "2026-03-04"
[extra]
categories = ["studynotes-10_ai"]
+++

# GPT (Generative Pre-trained Transformer)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트랜스포머의 디코더만을 사용하여 이전 토큰들로부터 다음 토큰을 예측하는 자기 회귀(Auto-regressive) 언어 모델로, 대규모 텍스트 코퍼스에서 생성 능력을 학습합니다.
> 2. **가치**: GPT-3 (175B), GPT-4 (1.7T 추정) 등으로 확장하며 Few-shot, Zero-shot 능력을 발현, ChatGPT로 전 세계에 생성형 AI 열풍을 일으켰습니다.
> 3. **융합**: 프롬프트 엔지니어링, RAG, RLHF와 결합하여 대화형 AI, 코딩 어시스턴트, 창작 도구로 진화하며 범용 인공지능(AGI)의 가능성을 보여줍니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**GPT(Generative Pre-trained Transformer)**는 OpenAI가 개발한 생성형 사전 학습 언어 모델입니다. 핵심 특징은 **(1) 디코더 전용 구조, (2) 자기 회귀 생성, (3) 대규모 사전 학습 + 파인튜닝**입니다.

**모델 진화**:
- GPT-1 (2018): 117M 파라미터, 사전학습+파인튜닝 패러다임
- GPT-2 (2019): 1.5B, Zero-shot 태스크 수행
- GPT-3 (2020): 175B, Few-shot, In-context Learning
- GPT-3.5 (2022): RLHF 적용, ChatGPT
- GPT-4 (2023): 멀티모달, 1.7T 추정, GPT-4o
- GPT-4o (2024): 실시간 멀티모달, 오디오/비디오 통합

#### 2. 💡 비유를 통한 이해
GPT는 **'이야기를 이어가는 이야기꾼'**에 비유할 수 있습니다:

- **자기 회귀**: "옛날 옛적에 호랑이가 한 마리 살았는데..." 다음에 "그 호랑이는"으로 자연스럽게 이어감.
- **단방향**: 지금까지 말한 내용만 보고 다음 말을 예측. 미래의 내용은 못 봄.
- **Few-shot**: "이런 식으로 이야기해 줘" 예시를 몇 개 보여주면 패턴을 금방 익힘.

#### 3. GPT의 확장 법칙 (Scaling Laws)

모델 크기, 데이터 양, 연산량을 늘리면 성능이 예측 가능하게 향상:

$$L(N) = \frac{C}{N^\alpha}$$

- $N$: 파라미터 수
- $L$: 손실 (낮을수록 좋음)
- $\alpha \approx 0.076$ (Kaplan et al.)

**Emergent Abilities**: 특정 규모를 넘으면 갑자기 새로운 능력 발현 (수학, 논리, 코딩).

---

### Ⅱ. 아키텍처 및 핵심 원리

#### GPT 구조

| 요소 | 역할 | 설명 |
|:---|:---|:---|
| **Token Embedding** | 단어 표현 | BPE 토크나이저 (50,257 vocab) |
| **Position Embedding** | 위치 정보 | 학습 가능한 위치 임베딩 |
| **Masked Self-Attention** | 인과적 어텐션 | 미래 토큰 마스킹 |
| **Feed Forward** | 비선형 변환 | MLP (4× hidden) |
| **Layer Norm** | 정규화 | Pre-LN 구조 |

#### GPT vs BERT 구조 비교

```text
GPT (Decoder-only):           BERT (Encoder-only):
     x → Masked Attn →        x → Bidirectional Attn →
         ↓                          ↓
      FFN → ... →              FFN → ... →
         ↓                          ↓
    Next Token                [CLS] for Classification

마스킹:
GPT: 미래 토큰 마스킹 (▼▼▼)
BERT: 무작위 토큰 마스킹 (↑↓↑)
```

#### PyTorch GPT 구현

```python
import torch
import torch.nn as nn
import math

class GPTBlock(nn.Module):
    def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = nn.MultiheadAttention(d_model, n_heads, dropout)
        self.ln2 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout)
        )

    def forward(self, x, mask=None):
        # Pre-LN + Self-Attention
        x = x + self.attn(self.ln1(x), self.ln1(x), self.ln1(x),
                         attn_mask=mask, need_weights=False)[0]
        # Pre-LN + FFN
        x = x + self.ff(self.ln2(x))
        return x
```

---

### Ⅲ. GPT의 핵심 능력

#### 1. In-Context Learning
- **Zero-shot**: 예시 없이 바로 수행
- **Few-shot**: 몇 개 예시로 패턴 학습
- **Chain-of-Thought**: 단계별 추론 유도

#### 2. RLHF (Reinforcement Learning from Human Feedback)
1. **SFT**: 지도 학습으로 초기 모델 학습
2. **Reward Model**: 인간 선호도 학습
3. **PPO**: 보상 최적화로 정책 학습

#### 3. 프롬프트 엔지니어링

```text
시스템 프롬프트: "당신은 도움이 되는 AI 어시스턴트입니다."
사용자: "파이썬으로 피보나치 수열을 작성해 줘."

CoT 프롬프트: "단계별로 생각해 봅시다."
1. 피보나치 수열의 정의는...
2. 기저 조건은...
3. 점화식은...
```

---

### Ⅳ. GPT 모델 비교

| 모델 | 파라미터 | 컨텍스트 | 특징 |
|:---|:---|:---|:---|
| GPT-2 | 1.5B | 1,024 | Zero-shot |
| GPT-3 | 175B | 2,048 | Few-shot |
| GPT-3.5 | 175B | 4,096 | RLHF, ChatGPT |
| GPT-4 | ~1.7T | 8,192~128K | 멀티모달 |
| GPT-4o | ? | 128K | 실시간 오디오/비디오 |

---

### Ⅴ. 실무 적용

#### 활용 분야
- **코딩 어시스턴트**: GitHub Copilot, Cursor
- **문서 작성**: Notion AI, Jasper
- **고객 서비스**: 챗봇, FAQ 자동화
- **교육**: 튜터링, 과제 도움

#### API 사용 예시

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "당신은 한국어 AI 어시스턴트입니다."},
        {"role": "user", "content": "머신러닝을 3줄로 설명해 줘."}
    ],
    temperature=0.7,
    max_tokens=200
)
```

---

### 📌 관련 개념 맵
- [BERT](@/studynotes/10_ai/01_dl/bert_model.md)
- [트랜스포머](@/studynotes/10_ai/01_dl/transformer_architecture.md)
- [RLHF](@/studynotes/10_ai/01_dl/rlhf_llm_alignment.md)
- [프롬프트 엔지니어링](@/studynotes/10_ai/01_dl/prompt_engineering.md)
- [LLM 최적화](@/studynotes/10_ai/01_dl/llm_optimization.md)

---

### 👶 어린이를 위한 3줄 비유
1. **이야기 이어가기**: GPT는 "옛날에..." 하고 시작하면 그 다음을 계속 이어서 말하는 이야기꾼이에요.
2. **예시만 보여주면**: "이렇게 써!" 하고 예시를 몇 개만 보여주면 금방 그 스타일로 글을 쓸 수 있어요.
3. **만능 작가**: 시, 소설, 코딩, 번역 뭐든 할 수 있는 똑똑한 작가 친구예요!
