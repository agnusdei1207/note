+++
title = "Transformer / Attention Mechanism"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# Transformer / Attention Mechanism

## 핵심 인사이트 (3줄 요약)
> **Transformer**는 "Attention Is All You Need"(2017)에서 제안된 순전히 Attention 기반 신경망으로, RNN 없이도 시퀀스를 병렬 처리한다. **Self-Attention**은 문장 내 모든 토큰 쌍의 관계를 가중합으로 계산해 장거리 의존성을 포착한다. LLM·ViT·Stable Diffusion 등 현대 AI의 99%가 Transformer로 구동된다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: Transformer는 Encoder-Decoder 구조의 딥러닝 아키텍처로, Scaled Dot-Product Attention과 Multi-Head Attention을 핵심으로 한다. 입력 시퀀스의 각 토큰이 다른 모든 토큰과의 관계를 동적으로 계산하여 문맥을 파악한다.

> 💡 **비유**: Transformer는 **"회의실에서 모든 참석자가 서로 동시에 대화"** 같아요. 각자가 중요한 말에 선택적으로 집중하죠. "그것"이라는 단어가 나왔을 때, 문맥을 보고 "고양이"와 연결하는 것처럼요!

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - RNN/LSTM 한계**: 순차 처리로 병렬화 불가능, 장거리 의존성 소실 (Vanishing Gradient)
2. **기술적 필요성 - Attention 메커니즘**: 2015년 Bahdanau가 Encoder-Decoder 간 중요 위치 집중 기법 도입 → 기계 번역 품질 향상
3. **시장/산업 요구 - 대규모 언어 모델**: 2017년 Google이 "Attention Is All You Need" 발표, RNN 완전 대체로 BERT, GPT 탄생

**핵심 목적**: **병렬 처리 가능한 시퀀스 모델링, 장거리 의존성 포착, 범용 사전학습 기반 모델**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**Transformer 전체 구조** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Transformer 아키텍처                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ENCODER (×N=6)                    DECODER (×N=6)                      │
│   ┌───────────────────┐            ┌───────────────────┐               │
│   │ Input Embedding   │            │ Output Embedding  │               │
│   │ + Pos Encoding    │            │ + Pos Encoding    │               │
│   └─────────┬─────────┘            └─────────┬─────────┘               │
│             │                                │                          │
│   ┌─────────▼─────────┐            ┌─────────▼─────────┐               │
│   │ Multi-Head Self   │            │ Masked Multi-Head │               │
│   │ Attention         │            │ Self-Attention    │               │
│   └─────────┬─────────┘            └─────────┬─────────┘               │
│             │                                │                          │
│   ┌─────────▼─────────┐            ┌─────────▼─────────┐               │
│   │ Add & Norm        │            │ Add & Norm        │               │
│   └─────────┬─────────┘            └─────────┬─────────┘               │
│             │                                │                          │
│   ┌─────────▼─────────┐            ┌─────────▼─────────┐               │
│   │ Feed Forward      │            │ Cross-Attention   │◄── Encoder 출력│
│   │ Network           │            │ (Encoder-Decoder) │               │
│   └─────────┬─────────┘            └─────────┬─────────┘               │
│             │                                │                          │
│   ┌─────────▼─────────┐            ┌─────────▼─────────┐               │
│   │ Add & Norm        │            │ Add & Norm        │               │
│   └─────────┬─────────┘            └─────────┬─────────┘               │
│             │                                │                          │
│             │                      ┌─────────▼─────────┐               │
│             │                      │ Feed Forward      │               │
│             │                      │ Network           │               │
│             │                      └─────────┬─────────┘               │
│             │                                │                          │
│             │                      ┌─────────▼─────────┐               │
│             │                      │ Add & Norm        │               │
│             │                      └─────────┬─────────┘               │
│             │                                │                          │
│             ▼                                ▼                          │
│   ┌───────────────────┐            ┌───────────────────┐               │
│   │ Encoder 출력      │──────────► │ Linear + Softmax  │               │
│   └───────────────────┘            │ (단어 확률 분포)   │               │
│                                    └───────────────────┘               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**구성 요소 상세** (필수: 표):
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **Input Embedding** | 토큰을 벡터로 변환 | d_model=512 차원 | 이름표 |
| **Positional Encoding** | 위치 정보 주입 | sin/cos 함수 사용 | 좌석번호 |
| **Multi-Head Attention** | 다중 관점 토큰 관계 학습 | h=8~16 헤드 | 여러 각도 분석 |
| **Add & LayerNorm** | Residual + 정규화 | 그래디언트 흐름 개선 | 원본 보존 |
| **Feed Forward Network** | 위치별 독립 비선형 변환 | 2층 MLP (d_ff=2048) | 심층 분석 |
| **Masked Attention** | 미래 토큰 가림 | 디코더 전용 | 치팅 방지 |

**Self-Attention 핵심 원리** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                   Scaled Dot-Product Attention                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Attention(Q, K, V) = softmax(Q·Kᵀ / √d_k) · V                        │
│                                                                         │
│   Q (Query): "무엇을 찾고 싶은가?"                                      │
│   K (Key):   "나는 이런 정보를 가지고 있어"                             │
│   V (Value): "실제 내용"                                                │
│   √d_k:      온도 조절 (softmax 분산 안정화)                            │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                                                                 │  │
│   │   입력 X ────┬───► Wq ───► Q (Query)                           │  │
│   │             ├───► Wk ───► K (Key)                              │  │
│   │             └───► Wv ───► V (Value)                            │  │
│   │                                                                 │  │
│   │   Q × Kᵀ ───────► Attention Scores                            │  │
│   │       │                                                         │  │
│   │       ▼                                                         │  │
│   │   ÷ √d_k ───────► Scaled Scores                                │  │
│   │       │                                                         │  │
│   │       ▼                                                         │  │
│   │   Softmax ──────► Attention Weights (확률 분포)                 │  │
│   │       │                                                         │  │
│   │       ▼                                                         │  │
│   │   × V ──────────► Weighted Sum (문맥 반영 출력)                 │  │
│   │                                                                 │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│   예시: "The cat sat on the mat"                                        │
│                                                                         │
│   "sat"에 대한 Self-Attention:                                          │
│   ┌────────────────────────────────────────────────────────────┐       │
│   │ 단어      │ Attention Weight │ 설명                        │       │
│   ├────────────────────────────────────────────────────────────┤       │
│   │ "cat"     │ 0.45             │ 주어 - 높은 관련성           │       │
│   │ "mat"     │ 0.30             │ 장소 - 중간 관련성           │       │
│   │ "the"     │ 0.10             │ 관사 - 낮은 관련성           │       │
│   │ "on"      │ 0.10             │ 전치사 - 낮은 관련성         │       │
│   │ "The"     │ 0.05             │ 시작 관사 - 매우 낮음        │       │
│   └────────────────────────────────────────────────────────────┘       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

[Multi-Head Attention]

MultiHead(Q,K,V) = Concat(head₁,...,headₕ) · Wₒ
where headᵢ = Attention(QWᵢQ, KWᵢK, VWᵢV)

각 헤드 = 다른 관점에서의 Attention
h=8 헤드 예시:
  Head 1: 문법적 관계 (주어-동사)
  Head 2: 의미적 관계 (동의어)
  Head 3: 위치 관계 (인접 단어)
  ...
  Head 8: 장거리 의존성

→ Concat 후 Wₒ로 혼합하여 종합 표현 생성
```

**핵심 알고리즘/공식** (해당 시 필수):
```
[Self-Attention 복잡도]

시간 복잡도: O(n² · d)
공간 복잡도: O(n² + n·d)

n = 시퀀스 길이, d = 모델 차원

→ 시퀀스 길이 2배 → 메모리/시간 4배
→ Flash Attention: O(n) 메모리로 최적화

[Positional Encoding]

PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

특성:
- 위치마다 고유한 벡터
- 상대 위치 정보 포함 (sin(A-B) = sinA·cosB - cosA·sinB)
- 학습 없이 일반화 가능

[Layer Normalization]

LayerNorm(x) = γ · (x - μ) / σ + β

μ: 해당 층 평균, σ: 표준편차
γ, β: 학습 가능한 스케일/시프트

[Feed Forward Network]

FFN(x) = max(0, xW₁ + b₁)W₂ + b₂

d_model = 512, d_ff = 2048
→ 확장 후 축소 (bottleneck 구조)
```

**코드 예시** (필수: Python 순수 구현):
```python
from dataclasses import dataclass
from typing import List, Optional, Tuple
import math
import random

# ============================================================
# Transformer 구현 (NumPy-free 순수 Python)
# ============================================================

def softmax(x: List[float]) -> List[float]:
    """Softmax 함수"""
    max_x = max(x)
    exp_x = [math.exp(xi - max_x) for xi in x]
    sum_exp = sum(exp_x)
    return [e / sum_exp for e in exp_x]


def layer_norm(x: List[float], eps: float = 1e-6) -> List[float]:
    """Layer Normalization"""
    mean = sum(x) / len(x)
    variance = sum((xi - mean) ** 2 for xi in x) / len(x)
    std = math.sqrt(variance + eps)
    # γ=1, β=0 가정
    return [(xi - mean) / std for xi in x]


def gelu(x: float) -> float:
    """GELU 활성화 함수"""
    return 0.5 * x * (1 + math.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * x**3)))


@dataclass
class Matrix:
    """간단한 행렬 클래스"""
    data: List[List[float]]
    rows: int
    cols: int

    @classmethod
    def zeros(cls, rows: int, cols: int) -> 'Matrix':
        return cls([[0.0] * cols for _ in range(rows)], rows, cols)

    @classmethod
    def random(cls, rows: int, cols: int, scale: float = 0.02) -> 'Matrix':
        data = [[random.gauss(0, scale) for _ in range(cols)] for _ in range(rows)]
        return cls(data, rows, cols)

    def get(self, i: int, j: int) -> float:
        return self.data[i][j]

    def set(self, i: int, j: int, val: float) -> None:
        self.data[i][j] = val

    def row(self, i: int) -> List[float]:
        return self.data[i]

    def col(self, j: int) -> List[float]:
        return [self.data[i][j] for i in range(self.rows)]


def matmul(A: Matrix, B: Matrix) -> Matrix:
    """행렬 곱셈"""
    if A.cols != B.rows:
        raise ValueError(f"Shape mismatch: {A.rows}x{A.cols} @ {B.rows}x{B.cols}")
    result = Matrix.zeros(A.rows, B.cols)
    for i in range(A.rows):
        for j in range(B.cols):
            val = sum(A.get(i, k) * B.get(k, j) for k in range(A.cols))
            result.set(i, j, val)
    return result


def transpose(M: Matrix) -> Matrix:
    """전치 행렬"""
    result = Matrix.zeros(M.cols, M.rows)
    for i in range(M.rows):
        for j in range(M.cols):
            result.set(j, i, M.get(i, j))
    return result


class ScaledDotProductAttention:
    """Scaled Dot-Product Attention"""

    def __init__(self, d_k: int):
        self.d_k = d_k
        self.scale = math.sqrt(d_k)

    def forward(self, Q: Matrix, K: Matrix, V: Matrix,
                mask: Optional[Matrix] = None) -> Tuple[Matrix, Matrix]:
        """
        Q: (seq_len, d_k)
        K: (seq_len, d_k)
        V: (seq_len, d_v)
        Returns: output (seq_len, d_v), attention_weights (seq_len, seq_len)
        """
        seq_len = Q.rows

        # Attention Scores: Q @ K^T / sqrt(d_k)
        K_T = transpose(K)
        scores = matmul(Q, K_T)

        # 스케일링
        for i in range(scores.rows):
            for j in range(scores.cols):
                scores.set(i, j, scores.get(i, j) / self.scale)

        # 마스크 적용 (Decoder용)
        if mask is not None:
            for i in range(scores.rows):
                for j in range(scores.cols):
                    if mask.get(i, j) == 0:
                        scores.set(i, j, -1e9)

        # Softmax (행별)
        attention_weights = Matrix.zeros(seq_len, seq_len)
        for i in range(seq_len):
            row_scores = [scores.get(i, j) for j in range(seq_len)]
            row_probs = softmax(row_scores)
            for j in range(seq_len):
                attention_weights.set(i, j, row_probs[j])

        # Weighted Sum: Attention @ V
        output = matmul(attention_weights, V)

        return output, attention_weights


class MultiHeadAttention:
    """Multi-Head Attention"""

    def __init__(self, d_model: int = 512, n_heads: int = 8):
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        self.d_v = d_model // n_heads

        # 각 헤드의 Q, K, V 투영 가중치
        self.W_Q = [Matrix.random(d_model, self.d_k) for _ in range(n_heads)]
        self.W_K = [Matrix.random(d_model, self.d_k) for _ in range(n_heads)]
        self.W_V = [Matrix.random(d_model, self.d_v) for _ in range(n_heads)]

        # 출력 투영
        self.W_O = Matrix.random(d_model, d_model)

        self.attention = ScaledDotProductAttention(self.d_k)

    def forward(self, X: Matrix, mask: Optional[Matrix] = None) -> Matrix:
        """
        X: (seq_len, d_model)
        Returns: (seq_len, d_model)
        """
        seq_len = X.rows
        head_outputs = []

        for h in range(self.n_heads):
            # Q, K, V 투영
            Q_h = matmul(X, self.W_Q[h])
            K_h = matmul(X, self.W_K[h])
            V_h = matmul(X, self.W_V[h])

            # Attention
            head_out, _ = self.attention.forward(Q_h, K_h, V_h, mask)
            head_outputs.append(head_out)

        # Concat heads
        concat = Matrix.zeros(seq_len, self.n_heads * self.d_v)
        for h, head_out in enumerate(head_outputs):
            for i in range(seq_len):
                for j in range(self.d_v):
                    concat.set(i, h * self.d_v + j, head_out.get(i, j))

        # 출력 투영
        output = matmul(concat, self.W_O)
        return output


class PositionWiseFeedForward:
    """Position-wise Feed Forward Network"""

    def __init__(self, d_model: int = 512, d_ff: int = 2048):
        self.W1 = Matrix.random(d_model, d_ff)
        self.W2 = Matrix.random(d_ff, d_model)
        self.b1 = [0.0] * d_ff
        self.b2 = [0.0] * d_model

    def forward(self, X: Matrix) -> Matrix:
        """X: (seq_len, d_model) -> (seq_len, d_model)"""
        # 첫 번째 선형 + GELU
        hidden = matmul(X, self.W1)
        for i in range(hidden.rows):
            for j in range(hidden.cols):
                hidden.set(i, j, gelu(hidden.get(i, j) + self.b1[j]))

        # 두 번째 선형
        output = matmul(hidden, self.W2)
        for i in range(output.rows):
            for j in range(output.cols):
                output.set(i, j, output.get(i, j) + self.b2[j])

        return output


class PositionalEncoding:
    """Positional Encoding"""

    def __init__(self, d_model: int = 512, max_len: int = 5000):
        self.d_model = d_model
        # 미리 계산된 위치 인코딩
        self.pe = self._compute_pe(max_len)

    def _compute_pe(self, max_len: int) -> Matrix:
        pe = Matrix.zeros(max_len, self.d_model)
        for pos in range(max_len):
            for i in range(self.d_model):
                if i % 2 == 0:
                    val = math.sin(pos / (10000 ** (i / self.d_model)))
                else:
                    val = math.cos(pos / (10000 ** ((i - 1) / self.d_model)))
                pe.set(pos, i, val)
        return pe

    def forward(self, X: Matrix) -> Matrix:
        """X: (seq_len, d_model) -> X + PE"""
        seq_len = X.rows
        result = Matrix.zeros(seq_len, X.cols)
        for i in range(seq_len):
            for j in range(X.cols):
                result.set(i, j, X.get(i, j) + self.pe.get(i, j))
        return result


class TransformerEncoderLayer:
    """Transformer Encoder Layer"""

    def __init__(self, d_model: int = 512, n_heads: int = 8, d_ff: int = 2048):
        self.self_attn = MultiHeadAttention(d_model, n_heads)
        self.ffn = PositionWiseFeedForward(d_model, d_ff)
        self.norm1 = lambda x: layer_norm(x)
        self.norm2 = lambda x: layer_norm(x)

    def forward(self, X: Matrix, mask: Optional[Matrix] = None) -> Matrix:
        # Self-Attention + Residual + Norm
        attn_out = self.self_attn.forward(X, mask)
        # Add & Norm
        for i in range(X.rows):
            row = [X.get(i, j) + attn_out.get(i, j) for j in range(X.cols)]
            normed = self.norm1(row)
            for j, val in enumerate(normed):
                X.set(i, j, val)

        # FFN + Residual + Norm
        ffn_out = self.ffn.forward(X)
        for i in range(X.rows):
            row = [X.get(i, j) + ffn_out.get(i, j) for j in range(X.cols)]
            normed = self.norm2(row)
            for j, val in enumerate(normed):
                X.set(i, j, val)

        return X


class SimpleTokenizer:
    """간단한 토크나이저"""

    def __init__(self, vocab: List[str]):
        self.vocab = vocab
        self.word2idx = {w: i for i, w in enumerate(vocab)}
        self.idx2word = {i: w for i, w in enumerate(vocab)}

    def encode(self, text: str) -> List[int]:
        words = text.lower().split()
        return [self.word2idx.get(w, 0) for w in words]  # 0 = <UNK>

    def decode(self, indices: List[int]) -> str:
        return ' '.join(self.idx2word.get(i, '<UNK>') for i in indices)


class MiniTransformer:
    """Mini Transformer for demonstration"""

    def __init__(self, vocab_size: int = 1000, d_model: int = 128,
                 n_heads: int = 4, n_layers: int = 2, d_ff: int = 512):
        self.d_model = d_model
        self.vocab_size = vocab_size

        # Token Embedding
        self.embedding = Matrix.random(vocab_size, d_model, scale=0.1)

        # Positional Encoding
        self.pos_encoding = PositionalEncoding(d_model)

        # Encoder Layers
        self.encoder_layers = [
            TransformerEncoderLayer(d_model, n_heads, d_ff)
            for _ in range(n_layers)
        ]

        # Output projection
        self.output_proj = Matrix.random(d_model, vocab_size, scale=0.1)

    def forward(self, token_ids: List[int]) -> Matrix:
        """Forward pass"""
        seq_len = len(token_ids)

        # Embedding lookup
        X = Matrix.zeros(seq_len, self.d_model)
        for i, tid in enumerate(token_ids):
            for j in range(self.d_model):
                X.set(i, j, self.embedding.get(tid, j))

        # Positional encoding
        X = self.pos_encoding.forward(X)

        # Encoder layers
        for layer in self.encoder_layers:
            X = layer.forward(X)

        # Output projection (logits)
        logits = matmul(X, self.output_proj)

        return logits

    def predict(self, token_ids: List[int]) -> List[int]:
        """예측 (argmax)"""
        logits = self.forward(token_ids)
        predictions = []
        for i in range(logits.rows):
            row = [logits.get(i, j) for j in range(logits.cols)]
            pred = row.index(max(row))
            predictions.append(pred)
        return predictions


# ============================================================
# Self-Attention 시각화
# ============================================================

def visualize_attention(tokens: List[str], attention_weights: Matrix) -> str:
    """Attention 가중치 시각화"""
    n = len(tokens)
    lines = ["\nAttention Weights Matrix:"]
    lines.append("      " + "  ".join(f"{t:>6}" for t in tokens))
    lines.append("-" * (7 + n * 8))

    for i, token in enumerate(tokens):
        weights = [attention_weights.get(i, j) for j in range(n)]
        row = f"{token:>5} " + "  ".join(f"{w:>6.3f}" for w in weights)
        lines.append(row)

    return "\n".join(lines)


# ============================================================
# 사용 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("         Transformer 구현 데모")
    print("=" * 60)

    # 1. Self-Attention 데모
    print("\n1. Self-Attention 계산")
    print("-" * 40)

    # 간단한 예시: 3개 토큰, 4차원
    Q = Matrix([
        [1.0, 0.0, 0.5, 0.2],
        [0.1, 1.0, 0.3, 0.4],
        [0.5, 0.2, 1.0, 0.1]
    ], 3, 4)

    K = Matrix([
        [0.9, 0.1, 0.4, 0.3],
        [0.2, 0.8, 0.2, 0.5],
        [0.6, 0.3, 0.9, 0.0]
    ], 3, 4)

    V = Matrix([
        [1.0, 0.0],
        [0.0, 1.0],
        [0.5, 0.5]
    ], 3, 2)

    attention = ScaledDotProductAttention(d_k=4)
    output, weights = attention.forward(Q, K, V)

    tokens = ["The", "cat", "sat"]
    print(visualize_attention(tokens, weights))

    print("\n출력:")
    for i in range(output.rows):
        row = [output.get(i, j) for j in range(output.cols)]
        print(f"  {tokens[i]}: {row}")

    # 2. Mini Transformer 데모
    print("\n\n2. Mini Transformer Forward Pass")
    print("-" * 40)

    # 작은 어휘 사전
    vocab = ["<PAD>", "<UNK>", "the", "cat", "sat", "on", "mat", "dog", "ran"]
    tokenizer = SimpleTokenizer(vocab)

    # 모델 생성
    model = MiniTransformer(
        vocab_size=len(vocab),
        d_model=32,
        n_heads=2,
        n_layers=2,
        d_ff=64
    )

    # 입력 문장
    text = "the cat sat"
    token_ids = tokenizer.encode(text)
    print(f"입력: '{text}'")
    print(f"토큰 ID: {token_ids}")
    print(f"토큰: {[vocab[i] for i in token_ids]}")

    # Forward pass
    logits = model.forward(token_ids)
    print(f"\nLogits shape: {logits.rows} x {logits.cols}")
    print(f"Logits (첫 번째 토큰): {[f'{logits.get(0, j):.3f}' for j in range(min(5, logits.cols))]}...")

    # 예측
    predictions = model.predict(token_ids)
    print(f"\n예측 토큰 ID: {predictions}")
    print(f"예측 토큰: {[vocab[i] for i in predictions]}")

    print("\n" + "=" * 60)
    print("Transformer의 핵심:")
    print("1. Self-Attention: 모든 토큰이 서로 관계 계산")
    print("2. Multi-Head: 여러 관점에서 동시 분석")
    print("3. 병렬 처리: RNN 없이 시퀀스 처리")
    print("=" * 60)
