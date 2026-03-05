+++
title = "파인튜닝 및 전이 학습 (Fine-tuning & Transfer Learning)"
date = "2026-03-04"
[extra]
categories = ["studynotes-10_ai"]
+++

# 파인튜닝 및 전이 학습 (Fine-tuning & Transfer Learning)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 대규모 데이터로 사전 학습된 모델(Pre-trained Model)의 가중치를 가져와, 특정 태스크의 소규모 데이터로 추가 학습(Fine-tuning)하여 도메인 특화 성능을 달성하는 기술입니다.
> 2. **가치**: 학습 데이터 90% 절감, 학습 시간 95% 단축, 제한된 자원으로도 SOTA 성능 달성 가능. BERT, GPT, ResNet 등의 파운데이션 모델 활용의 핵심.
> 3. **융합**: PEFT(LoRA, QLoRA), 프롬프트 튜닝, 어댑터와 결합하여 파라미터 효율적 파인튜닝으로 진화.

---

### Ⅰ. 개요

#### 전이 학습 (Transfer Learning)
**정의**: 한 도메인에서 학습한 지식을 다른 도메인으로 전이하는 기법

**유형**:
1. **Feature Extraction**: 사전 학습 모델을 특성 추출기로만 사용 (동결)
2. **Fine-tuning**: 전체 또는 일부 가중치를 새 데이터로 재학습
3. **Domain Adaptation**: 소스 도메인 → 타겟 도메인 적응

#### 파인튜닝 (Fine-tuning)
**정의**: 사전 학습된 모델의 가중치를 타겟 태스크 데이터로 미세 조정

**전략**:
1. **Full Fine-tuning**: 모든 파라미터 업데이트
2. **Layer-wise**: 층별로 다른 학습률 적용
3. **Gradual Unfreezing**: 층을 점진적으로 동결 해제

---

### Ⅱ. PEFT (Parameter-Efficient Fine-Tuning)

#### PEFT 기법 비교

| 기법 | 파라미터 | 원리 | 장점 |
|:---|:---|:---|:---|
| **LoRA** | 0.1~1% | 저차원 분해 행렬 추가 | 메모리 효율, 병합 가능 |
| **QLoRA** | 0.1% | 4비트 양자화 + LoRA | 16GB GPU에서 65B 학습 |
| **AdaLoRA** | 가변 | 중요도 기반 랭크 조절 | 효율적 자원 할당 |
| **Prefix Tuning** | 0.1% | 입력에 학습 가능한 프리픽스 추가 | 원본 모델 보존 |
| **Prompt Tuning** | 0.01% | 입력 임베딩에 소프트 프롬프트 | 매우 적은 파라미터 |
| **Adapters** | 1~5% | 층 사이에 작은 병목 모듈 삽입 | 모듈화 |

#### LoRA (Low-Rank Adaptation)

$$W' = W + \Delta W = W + BA$$

- $B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times k}$
- $r \ll \min(d, k)$ (보통 4~64)
- A는 랜덤 초기화, B는 0 초기화

#### PyTorch LoRA 구현

```python
import torch
import torch.nn as nn

class LoRALinear(nn.Module):
    def __init__(self, in_features, out_features, rank=8, alpha=16):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)
        self.lora_A = nn.Parameter(torch.zeros(rank, in_features))
        self.lora_B = nn.Parameter(torch.zeros(out_features, rank))
        self.scaling = alpha / rank

        # A는 정규분포, B는 0으로 초기화
        nn.init.kaiming_normal_(self.lora_A)

    def forward(self, x):
        # 원본 + LoRA
        return self.linear(x) + (x @ self.lora_A.T @ self.lora_B.T) * self.scaling
```

---

### Ⅲ. 전이 학습 vs 처음부터 학습

| 항목 | From Scratch | Transfer Learning |
|:---|:---|:---|
| **데이터 요구** | 많음 (수백만) | 적음 (수천~수만) |
| **학습 시간** | 김 (일~주) | 짧음 (시간~일) |
| **연산 비용** | 높음 | 낮음 |
| **성능 상한** | 데이터 품질 의존 | 사전학습 품질 의존 |
| **과적합 위험** | 낮음 (데이터 많으면) | 높음 (소량 데이터) |

---

### Ⅳ. 실무 적용

#### LLM 파인튜닝 시나리오

1. **법률 도메인**: 법률 문서로 LLaMA 파인튜닝 → 법률 어시스턴트
2. **의료 도메인**: 의료 논문으로 BioBERT 파인튜닝 → 임상 의사결정 지원
3. **고객 서비스**: 회사 FAQ로 GPT 파인튜닝 → 챗봇

#### Hugging Face 파인튜닝

```python
from transformers import AutoModelForCausalLM, Trainer, TrainingArguments

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b")

training_args = TrainingArguments(
    output_dir="./fine-tuned-model",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=2e-5,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

trainer.train()
```

---

### 📌 관련 개념 맵
- [BERT](@/studynotes/10_ai/01_dl/bert_model.md)
- [GPT](@/studynotes/10_ai/01_dl/gpt_model.md)
- [LLM 최적화](@/studynotes/10_ai/01_dl/llm_optimization.md)
- [지도 학습](@/studynotes/10_ai/02_ml/supervised_learning.md)
- [RAG](@/studynotes/10_ai/01_dl/rag.md)

---

### 👶 어린이를 위한 3줄 비유
1. **선수 경험 활용**: 전이 학습은 축구 선수가 축구로 단련한 체력을 농구에서도 활용하는 것과 같아요.
2. **조금만 더 연습**: 이미 잘하는 선수에게 농구 규칙만 가르쳐주면 금방 농구도 잘하게 돼요.
3. **시간 절약**: 처음부터 달리기 연습을 안 해도 되니까 훨씬 빨리 배울 수 있어요!
