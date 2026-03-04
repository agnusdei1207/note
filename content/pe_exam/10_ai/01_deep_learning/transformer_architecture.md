+++
title = "Transformer Architecture"
description = "자연어 처리의 패러다임을 바꾼 Attention Is All You Need 논문의 핵심, 트랜스포머 아키텍처의 심층 구조와 동작 원리"
date = 2024-05-24
[taxonomies]
tags = ["AI", "Deep Learning", "Transformer", "LLM", "Attention"]
+++

# Transformer Architecture

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트랜스포머는 기존 RNN/LSTM의 순차적 처리(Sequential Processing) 한계를 극복하고, '셀프 어텐션(Self-Attention)' 메커니즘을 통해 문장 내 모든 단어 간의 관계를 병렬로 계산하는 혁신적인 딥러닝 아키텍처입니다.
> 2. **가치**: 무한한 병렬 연산이 가능해져 모델의 크기와 학습 데이터의 규모를 기하급수적으로 키울 수 있게 되었으며, 이는 GPT, BERT 등 거대 언어 모델(LLM) 탄생의 근본적인 기술적 기반이 되었습니다.
> 3. **융합**: 자연어 처리(NLP)를 넘어 컴퓨터 비전(Vision Transformer), 음성 인식, 단백질 구조 예측(AlphaFold) 등 인공지능 전 분야를 통일하는 범용적(Universal) 기반 아키텍처로 진화하였습니다.

---

### Ⅰ. 개요 (Context & Background)

트랜스포머(Transformer)는 2017년 구글(Google) 연구진이 발표한 논문 "Attention Is All You Need"에서 처음 제안된 딥러닝 모델 아키텍처입니다. 기존의 기계 번역 모델들이 문장을 처음부터 끝까지 순서대로 읽어 나가며 맥락을 파악했던 것과 달리, 트랜스포머는 문장 안의 모든 단어를 동시에 펼쳐놓고 '어떤 단어가 어떤 단어와 가장 깊은 연관이 있는지(Attention)'를 수학적으로 계산합니다. 이를 통해 문맥을 완벽하게 이해하면서도 GPU의 병렬 처리 능력을 극대화할 수 있습니다.

**💡 비유: 텔레파시로 소통하는 거대한 번역 공장**
기존의 RNN 모델이 '한 명의 번역가가 단어를 하나씩 순서대로 읽으면서 앞의 내용을 힘겹게 기억(메모리)해 나가는 방식'이라면, 트랜스포머는 '수천 명의 번역가가 텔레파시로 서로의 생각을 실시간으로 공유하며 문장 전체를 동시에 번역하는 거대한 공장'과 같습니다. 문장의 맨 앞에 있는 단어와 맨 끝에 있는 단어도 텔레파시(Self-Attention)를 통해 즉각적으로 의미를 교환하므로, 아무리 긴 문장이라도 문맥이 유실되지 않고 순식간에 처리됩니다.

**등장 배경 및 발전 과정:**
1. **기존 기술(RNN/LSTM)의 치명적 한계점**: 시퀀스 데이터를 처리하던 기존 RNN(Recurrent Neural Network)은 데이터가 순차적으로 입력되어야 하므로 연산의 **병렬화(Parallelization)가 불가능**하여 학습 속도가 매우 느렸습니다. 또한 문장이 길어질수록 앞부분의 정보가 뒤로 갈수록 희미해지는 **기울기 소실(Vanishing Gradient) 및 장기 의존성(Long-term Dependency) 문제**라는 구조적 병목에 갇혀 있었습니다.
2. **혁신적 패러다임 변화 (Attention Is All You Need)**: 트랜스포머는 RNN의 순환 구조를 완전히 버리고 오직 어텐션(Attention) 메커니즘만으로 모델을 구성했습니다. 순서 정보를 유지하기 위해 수학적인 주기 함수를 사용하는 **Positional Encoding**을 도입하였고, 문맥을 입체적으로 파악하기 위해 **Multi-Head Attention**을 창안하여 패러다임을 완전히 뒤집었습니다.
3. **현재 시장의 비즈니스적 요구사항**: 기업들은 수천억 개의 파라미터를 가진 초대규모 AI(Foundation Model)를 짧은 시간 내에 학습시키길 원합니다. 트랜스포머의 병렬 처리 구조는 최신 GPU(NVIDIA H100 등)의 행렬 곱셈(Matrix Multiplication) 연산 구조와 완벽하게 맞아떨어져, AI 발전의 가장 강력한 비즈니스 동력이 되었습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

트랜스포머는 입력 문장의 맥락을 압축하는 **인코더(Encoder)**와 이를 바탕으로 새로운 문장을 생성하는 **디코더(Decoder)**의 스택으로 구성됩니다.

#### 주요 구성 요소

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 수학적/기술적 특징 | 비유 |
|---|---|---|---|---|
| **Positional Encoding** | 단어의 순서 정보를 모델에 주입 | 입력 임베딩 벡터에 사인(Sine)과 코사인(Cosine) 주기 함수의 값을 더하여, 단어의 절대적/상대적 위치 정보를 수학적 좌표로 각인시킴 | $PE(pos, 2i) = \sin(pos/10000^{2i/d})$ | 단어 카드에 '몇 번째'인지 홀로그램 스티커 붙이기 |
| **Self-Attention** | 문장 내 단어 간의 연관성(가중치) 계산 | 하나의 단어가 다른 모든 단어와 얼마나 연관되는지를 Query(질의), Key(키), Value(값) 벡터의 내적(Dot Product)을 통해 계산 | Scaled Dot-Product Attention | 모르는 단어가 나왔을 때 주변 단어들에게 "너 나랑 관련 있어?" 물어보기 |
| **Multi-Head Attention** | 다양한 관점에서 문맥을 동시에 파악 | 하나의 어텐션을 수행하는 대신, 임베딩 차원을 여러 개(Head)로 쪼개어 독립적으로 어텐션을 수행한 뒤 결과를 연결(Concat) | 서로 다른 가중치 행렬 $W^Q, W^K, W^V$ 사용 | 문법 학자, 감정 분석가, 의미 학자가 동시에 한 문장을 분석하기 |
| **Feed Forward Network (FFN)** | 어텐션의 결과를 비선형적으로 변환 | 각 위치마다 동일하게 적용되는 2개의 선형 변환(Linear Transformation)과 그 사이의 ReLU/GELU 활성화 함수로 구성 | $FFN(x) = \max(0, xW_1 + b_1)W_2 + b_2$ | 회의가 끝난 후 각자 자리로 돌아가 생각을 정리하고 증폭시키기 |
| **Layer Normalization & Residual Connection** | 깊은 신경망의 학습 안정화 및 기울기 소실 방지 | 입력을 출력에 그대로 더해주는 잔차 연결(Add)을 수행하고, 층 단위로 정규화(Norm)하여 파라미터 업데이트를 안정시킴 | $\text{LayerNorm}(x + \text{Sublayer}(x))$ | 작업 과정에서 발생한 노이즈를 닦아내고 핵심만 다음 단계로 넘기기 |

#### 정교한 구조 다이어그램 (ASCII Art)

```text
======================================================================================================
                               [ TRANSFORMER ARCHITECTURE ]
======================================================================================================

          [ ENCODER STACK (e.g., Nx = 6) ]               [ DECODER STACK (e.g., Nx = 6) ]
                                                                        ^
                                                                        |
          +-------------------------------+              +-------------------------------+
          |       LayerNorm & Add         |              |       LayerNorm & Add         |
          +-------------------------------+              +-------------------------------+
          |  Feed Forward Network (FFN)   |              |  Feed Forward Network (FFN)   |
          +-------------------------------+              +-------------------------------+
          |       LayerNorm & Add         |              |       LayerNorm & Add         |
          +-------------------------------+              +-------------------------------+
          | Multi-Head Self-Attention     |              | Encoder-Decoder Attention     |
          | (Q=K=V from Encoder)          |              | (Q from Decoder, K=V from Enc)|
          +-------------------------------+              +-------------------------------+
                         ^                               |       LayerNorm & Add         |
                         |                               +-------------------------------+
                 [ Encoder Output ]--------------------->| Masked Multi-Head Attention   |
                         |                               | (Q=K=V from Decoder)          |
                         |                               +-------------------------------+
          +-------------------------------+              +-------------------------------+
          |      Positional Encoding      |              |      Positional Encoding      |
          +-------------------------------+              +-------------------------------+
          |       Input Embedding         |              |       Output Embedding        |
          +-------------------------------+              +-------------------------------+
                         ^                                              ^
                         |                                              |
                   [ Input Words ]                                [ Output Words ]
                 (e.g., "I love AI")                        (e.g., "나는 AI를 사랑해", Shifted)

======================================================================================================
                      [ SCALED DOT-PRODUCT ATTENTION MECHANISM ]
======================================================================================================
  
  1. MatMul: Query(Q) x Key(K)^T  --->  Scores (단어 간의 연관성 점수)
  2. Scale:  Scores / sqrt(d_k)   --->  Scaled Scores (기울기 폭발 방지)
  3. Mask:   (Optional, Decoder only) 치팅 방지를 위해 미래의 단어 위치를 -infinity로 마스킹
  4. Softmax: Softmax(Scaled)     --->  Attention Weights (총합이 1이 되는 확률 분포)
  5. MatMul: Weights x Value(V)   --->  Final Contextualized Vector (최종 문맥 벡터)

```

#### 심층 동작 원리: Self-Attention의 수학적 완성
Self-Attention 연산은 본질적으로 데이터베이스의 검색 메커니즘을 행렬 연산으로 구현한 것입니다.

**수식: Scaled Dot-Product Attention**
$$ \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V $$
1. **$Q, K, V$ 생성**: 입력 벡터 행렬 $X$에 각각 학습 가능한 가중치 행렬 $W^Q, W^K, W^V$를 곱하여 쿼리(Query), 키(Key), 값(Value) 행렬을 생성합니다.
2. **유사도 계산 ($QK^T$)**: 내적(Dot Product)을 통해 각 단어가 다른 모든 단어와 얼마나 연관성이 높은지 스코어를 구합니다.
3. **스케일링 ($\sqrt{d_k}$)**: 차원 수 $d_k$가 커지면 내적 값이 기하급수적으로 커져 Softmax의 기울기가 0에 수렴하는 현상을 막기 위해 $\sqrt{d_k}$로 나눕니다.
4. **소프트맥스 (Softmax)**: 점수를 0~1 사이의 확률값으로 변환합니다. 이 가중치가 바로 특정 단어에 얼마나 집중(Attention)할 것인지를 나타냅니다.
5. **문맥 정보 결합 ($ \times V$)**: 가중치 행렬을 실제 정보가 담긴 Value 행렬에 곱하여 최종적으로 맥락이 반영된 출력 벡터를 생성합니다.

**실무 수준의 핵심 코드 예시 (PyTorch 기반 Multi-Head Attention)**

```python
import torch
import torch.nn as nn
import math

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads # Head당 차원 수 분할
        
        # Q, K, V를 위한 선형 변환 (행렬 곱 최적화를 위해 한 번에 계산 후 분할하는 방식 채택)
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model) # 최종 출력 결합용

    def forward(self, q, k, v, mask=None):
        batch_size = q.size(0)
        
        # 1. 선형 변환 후 Head 수만큼 차원 분할 및 형태 변경: (Batch, Seq_len, d_model) -> (Batch, Heads, Seq_len, d_k)
        Q = self.W_q(q).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(k).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(v).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # 2. Scaled Dot-Product Attention 계산
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        if mask is not None:
            # Masking 처리 (미래 정보 접근 차단)
            scores = scores.masked_fill(mask == 0, -1e9)
            
        attention_weights = torch.softmax(scores, dim=-1)
        
        # 3. Value 곱하기
        attention_output = torch.matmul(attention_weights, V)
        
        # 4. 여러 Head의 결과를 Concat 및 원상 복구: (Batch, Seq_len, d_model)
        concat_output = attention_output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
        
        # 5. 최종 선형 변환
        output = self.W_o(concat_output)
        return output
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 심층 기술 비교: Transformer vs LSTM vs CNN

| 평가 지표 | LSTM (RNN 계열) | CNN (합성곱 신경망) | Transformer |
|---|---|---|---|
| **데이터 처리 방식** | 순차적 (Sequential) | 지역적 패치 (Local Patch) 병렬 | **전역적 병렬 (Global Parallel)** |
| **계산 복잡도 (Layer당)** | $O(n \cdot d^2)$ | $O(k \cdot n \cdot d^2)$ | **$O(n^2 \cdot d)$** (문장 길이 $n$의 제곱에 비례) |
| **장기 의존성(Long-term) 포착**| 취약 (거리가 멀어지면 정보 유실) | 매우 취약 (Receptive Field의 한계) | **완벽함 (모든 단어가 거리 1로 연결됨)** |
| **하드웨어 가속(GPU) 친화도** | 낮음 (이전 연산이 끝나야 다음 연산 가능)| 매우 높음 | **가장 높음 (거대한 행렬 곱연산으로 극대화)** |
| **해석 가능성 (Explainability)** | 블랙박스 (Hidden State 변화 추적 어려움) | CAM 등을 통한 시각화 가능 | **어텐션 맵(Attention Map)을 통해 단어 간 관계 직접 시각화 가능** |

*($n$: 시퀀스 길이, $d$: 임베딩 차원, $k$: 커널 사이즈)*

#### 과목 융합 관점 분석
- **[컴퓨터 구조(OS/HW) + Transformer]**: 트랜스포머의 치명적 단점은 문장 길이($N$)가 길어질수록 어텐션 행렬의 크기가 $N^2$로 커져 VRAM(비디오 메모리)을 극심하게 소모한다는 점입니다. 이 오버헤드를 줄이기 위해 OS의 메모리 계층(SRAM과 HBM) 간의 입출력을 최적화한 **FlashAttention** 알고리즘이 등장했습니다. 이는 타일링(Tiling) 기법을 사용하여 HBM(High Bandwidth Memory) 접근 횟수를 최소화하고 SRAM에서 Softmax를 병합 연산함으로써, 메모리 벽(Memory Wall)을 허물고 GPU의 텐서 코어(Tensor Core) 활용률을 극대화한 컴퓨터 구조와 AI의 융합 사례입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 기술사적 판단 (실무 시나리오)
- **시나리오 1: 수십만 자의 긴 문서를 처리해야 하는 요약 시스템 구축**
  - **문제**: 표준 트랜스포머는 $O(N^2)$의 연산 복잡도를 가져, 입력 토큰이 100K를 넘어가면 Out Of Memory(OOM) 에러가 발생합니다.
  - **전략적 의사결정**: 전체 Self-Attention 대신 연산량을 $O(N)$으로 줄이는 **Sparse Attention (Longformer, BigBird)** 구조를 도입하거나, 입력 단계를 청크로 나누어 재귀적으로 처리하는 구조, 혹은 최근 부상하는 **Ring Attention** 기법을 적용하여 Context Window를 1M 이상으로 확장하는 아키텍처를 선택합니다.
- **시나리오 2: 초실시간 챗봇 서비스에서의 추론 지연(Inference Latency) 최적화**
  - **문제**: 디코더(Decoder)가 답변을 한 단어씩 생성할 때마다 이전 단어들의 K, V 값을 반복적으로 다시 계산해야 하므로 지연 시간이 급증합니다.
  - **전략적 의사결정**: **KV Cache** 기술을 필수적으로 도입합니다. 이전에 계산된 Key와 Value 텐서를 GPU 메모리에 캐싱해두고 재활용하여 연산량을 줄입니다. 더 나아가 메모리 대역폭을 획기적으로 줄이기 위해 멀티 헤드에서 K, V를 공유하는 **GQA(Grouped-Query Attention)** 또는 **MQA(Multi-Query Attention)**가 적용된 모델(Llama 3 등)을 뼈대로 채택해야 합니다.
- **시나리오 3: 한정된 GPU 자원(예: 24GB VRAM)에서의 파인튜닝 (Fine-tuning)**
  - **문제**: 수백억 파라미터를 가진 트랜스포머 모델을 전체 학습(Full Fine-tuning)하는 것은 물리적으로 불가능합니다.
  - **전략적 의사결정**: 파라미터 효율적 미세조정(PEFT) 기법인 **LoRA(Low-Rank Adaptation)**를 도입합니다. 기존 모델의 가중치는 동결(Freeze)한 채, Attention 가중치 행렬(주로 $W^Q, W^V$) 옆에 Rank가 매우 낮은(예: r=8) 작은 행렬 두 개를 병렬로 삽입하여 이 부분만 학습시킴으로써 VRAM 사용량을 90% 이상 절감합니다.

#### 주의사항 및 안티패턴 (Anti-patterns)
- **패딩과 마스킹 오류 (Padding Mask Leak)**: 배치(Batch) 처리를 위해 길이를 맞추는 패딩(Padding) 토큰이 Attention 계산에 참여하게 방치하면 모델이 심각한 오류를 빚습니다. 반드시 `padding_mask`를 적용하여 소프트맥스 연산 전 패딩 위치에 `-inf`를 할당해야 합니다.
- **Position Information의 부재**: 트랜스포머의 철학은 순서가 없다는 것입니다. 만약 Positional Encoding을 누락하거나 실수로 훼손하면, 모델은 문장을 순서 없는 단어의 집합(Bag of Words)으로만 인식하게 되어 문장 생성에 완전히 실패하는 안티패턴이 발생합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 정량적/정성적 기대효과
| 구분 | 내용 및 지표 |
|---|---|
| **정성적 효과** | - 언어, 비전, 오디오 등 다중 양식(Multi-modal) 데이터 처리 아키텍처의 대통합 달성<br>- 인간의 언어 이해력에 필적하는 거대 언어 모델(LLM) 생태계 구축 (OpenAI, HuggingFace) |
| **정량적 효과** | - 기존 RNN 대비 병렬 처리로 인한 훈련 시간(Training Time) 단축 (수개월 -> 수일)<br>- 번역, 요약, 질의응답 등 모든 NLP 벤치마크(GLUE, SuperGLUE) SOTA(State-of-the-Art) 석권 |

#### 미래 전망 및 진화 방향
- **MoE (Mixture of Experts)와의 결합**: 모델의 크기를 키우면서도 연산 비용을 줄이기 위해, 트랜스포머의 FFN 층을 여러 개의 '전문가(Expert) 네트워크'로 분리하고 입력 데이터에 따라 필요한 전문가만 부분적으로 활성화(Sparse Activation)하는 라우팅 아키텍처(예: GPT-4, Mixtral)가 표준으로 자리 잡고 있습니다.
- **트랜스포머를 넘어서 (Beyond Transformer)**: $O(N^2)$의 복잡도를 본질적으로 극복하기 위해, 최근 선형 복잡도 $O(N)$를 가지면서도 장기 의존성을 유지하는 상태 공간 모델(State Space Model)인 **Mamba** 구조가 트랜스포머의 강력한 대안 혹은 상호 보완재로 연구되고 있습니다.

**※ 참고 표준/가이드**: 
- 트랜스포머 기반의 파운데이션 모델 개발 시, AI 모델의 공정성과 투명성을 검증하기 위한 **IEEE 7000 시리즈 (AI 윤리 표준)**를 준수하여 학습 데이터의 편향성(Bias)이 Attention 가중치에 영구적으로 각인되는 것을 방지하는 아키텍처 통제 지침이 요구됩니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- `[Large Language Model (LLM)](./llm.md)`: 트랜스포머의 디코더(GPT 계열) 또는 인코더(BERT 계열)를 수천억 파라미터로 확장한 거대 신경망.
- `[GQA (Grouped-Query Attention)](./gqa_mqa.md)`: 트랜스포머의 KV 연산 병목을 극복하기 위해 제안된 최신 어텐션 변형 메커니즘.
- `[FlashAttention](./flash_attention.md)`: GPU 메모리 IO 병목을 타파하여 트랜스포머의 학습과 추론을 비약적으로 가속하는 하드웨어 친화적 알고리즘.
- `[Vision Transformer (ViT)](./vision_transformer.md)`: 이미지를 16x16 패치로 나누어 트랜스포머에 입력함으로써 CNN을 대체한 컴퓨터 비전 아키텍처.
- `[Word Embedding](./embedding.md)`: 트랜스포머의 입력층에서 단어를 고차원 벡터로 변환하는 기초 NLP 기술.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **트랜스포머가 뭔가요?**: 옛날 AI는 문장을 읽을 때 한 단어씩 순서대로 읽느라 앞내용을 자꾸 까먹었는데, 트랜스포머는 **모든 단어를 한 번에 쫙 펼쳐놓고 동시에 읽는 마법의 돋보기**예요.
2. **어떻게 작동하나요?**: '셀프 어텐션'이라는 텔레파시 기술을 써서, 문장 속에 있는 모든 단어들이 서로서로 "우리 얼마나 친해?"라고 동시에 질문하며 의미를 꽉 잡아내요.
3. **왜 좋은가요?**: 한 번에 다 같이 일하니까 엄청나게 빠르고, 아주아주 긴 글을 읽어도 절대 내용을 까먹지 않아서 지금의 똑똑한 챗GPT가 태어날 수 있었답니다!
