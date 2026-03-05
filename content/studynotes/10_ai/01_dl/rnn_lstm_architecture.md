+++
title = "순환 신경망 및 LSTM (RNN/LSTM)"
date = "2026-03-04"
[extra]
categories = ["studynotes-10_ai"]
+++

# 순환 신경망 및 LSTM (RNN/LSTM)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 순차적(Sequential) 데이터를 처리하기 위해 이전 시점의 은닉 상태(Hidden State)를 현재 시점의 입력과 함께 처리하는 순환 구조(Recurrent Connection)를 가진 신경망으로, LSTM은 장기 의존성(Long-term Dependency) 문제를 해결하기 위해 게이트(Gate) 메커니즘을 도입했습니다.
> 2. **가치**: 기계 번역에서 BLEU 점수 30% 향상, 음성 인식에서 단어 오류율(WER) 50% 감소, 시계열 예측에서 정확도 40% 개선 등 순차 데이터 처리의 핵심 기술입니다.
> 3. **융합**: Seq2Seq, Attention 메커니즘의 기반이 되며, Transformer의 등장 이전에 자연어 처리를 지배했고, 현재도 시계열 예측, 음성 처리에서 활발히 사용됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**순환 신경망(Recurrent Neural Network, RNN)**은 1980년대에 제안된 이후, 시퀀스 데이터(텍스트, 음성, 시계열 등)를 처리하기 위해 설계된 신경망입니다. 핵심 아이디어는 **(1) 은닉 상태의 순환(Recurrence), (2) 시간에 따른 가중치 공유, (3) 동적 계산 그래프**입니다.

수학적으로 기본 RNN의 은닉 상태 갱신은 다음과 같습니다:

$$h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_h)$$
$$y_t = W_{hy} h_t + b_y$$

**LSTM(Long Short-Term Memory)**은 1997년 호크라이터(Hochreiter)와 슈미드후버(Schmidhuber)가 제안했으며, 장기 의존성 문제를 해결하기 위해 **셀 상태(Cell State)**와 **3개의 게이트(Forget, Input, Output)**를 도입했습니다.

#### 2. 💡 비유를 통한 이해
RNN/LSTM은 **'이야기를 기억하는 독서가'**에 비유할 수 있습니다:

- **기본 RNN**: 책을 읽을 때 직전 문장만 기억하는 사람. 이야기 초반 내용은 금방 잊어버려서 "그가"가 누구인지 모를 때가 많음.
- **LSTM**: 스마트 노트를 가진 독서가. 중요한 인물, 사건은 '노트(셀 상태)'에 적어두고, 필요없는 내용은 지우고, 중요한 내용은 계속 기억.
- **게이트의 역할**:
  - **Forget Gate**: "이전 내용 중 뭘 잊을까?" (불필요한 정보 삭제)
  - **Input Gate**: "새 문장에서 뭘 노트에 추가할까?" (중요 정보 저장)
  - **Output Gate**: "지금 상황에서 뭘 말해야 할까?" (현재 출력 결정)

#### 3. 등장 배경 및 발전 과정

1.  **기존 기술의 치명적 한계점**:
    - **피드포워드 신경망의 한계**: 입력 길이가 고정되어야 함. "나는 학교에 간다"와 "나는 어제 친구와 함께 학교에 갔다"를 동일한 입력 크기로 처리 불가.
    - **독립성 가정**: 각 입력이 독립적이라 가정. 실제로는 "은행"이 앞뒤 문맥에 따라 '금융기관'인지 '강둑'인지 달라짐.

2.  **혁신적 패러다임의 변화**:
    - **RNN (1986~1990)**: 엘먼(Elman) 네트워크 등 순환 구조 제안. 그러나 기울기 소실/폭발 문제로 긴 시퀀스 학습 불가.
    - **LSTM (1997)**: 게이트 메커니즘으로 장기 기억 문제 해결. 2000년대 후반까지 주목받지 못하다가 딥러닝 붐과 함께 재발견.
    - **GRU (2014)**: LSTM의 간소화 버전. 2개 게이트(Reset, Update)로 연산량 감소.
    - **Bi-LSTM (2005)**: 양방향 RNN으로 과거와 미래 문맥 동시 활용.
    - **Seq2Seq (2014)**: 인코더-디코더 구조로 기계 번역 혁신.

3.  **비즈니스적 요구사항**:
    - 실시간 음성 인식 (스마트 스피커, 회의록 자동 작성)
    - 기계 번역 (구글 번역, 파파고)
    - 시계열 예측 (주가, 수요 예측, 날씨)

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. RNN/LSTM 구성 요소 및 내부 메커니즘 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 수식 | 비유 |
|:---|:---|:---|:---|:---|
| **Hidden State (h_t)** | 단기 기억 | 이전 상태와 현재 입력의 결합 | h_t = tanh(W·[h_{t-1}, x_t]) | 작업 기억 |
| **Cell State (C_t)** | 장기 기억 (LSTM) | 컨베이어 벨트처럼 정보 보존 | C_t = f_t⊙C_{t-1} + i_t⊙C̃_t | 노트 |
| **Forget Gate (f_t)** | 불필요 정보 삭제 | Sigmoid로 0~1 사이 가중치 | f_t = σ(W_f·[h_{t-1}, x_t]) | 지우개 |
| **Input Gate (i_t)** | 새 정보 저장 | Sigmoid로 추가할 정보 선택 | i_t = σ(W_i·[h_{t-1}, x_t]) | 펜 |
| **Output Gate (o_t)** | 출력 결정 | 현재 은닉 상태에서 무엇을 출력 | o_t = σ(W_o·[h_{t-1}, x_t]) | 발언 |
| **Candidate (C̃_t)** | 새 후보 정보 | Tanh로 -1~1 사이 값 생성 | C̃_t = tanh(W_C·[h_{t-1}, x_t]) | 새 메모 |

#### 2. RNN vs LSTM 구조 비교 다이어그램

```text
<<< Basic RNN Cell >>>

    x_t ──────┐
              │
              ▼
         ┌─────────┐
    ──→  │  tanh   │  ──→ h_t (출력)
    h_t-1│  W, b   │
         └─────────┘

    문제: 긴 시퀀스에서 h_t-1 → h_t 전파 시 기울기 소실/폭발


<<< LSTM Cell (Long Short-Term Memory) >>>

                    C_t-1 (Cell State: 장기 기억)
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ Forget  │ │  Input  │ │ Output  │
    │  Gate   │ │  Gate   │ │  Gate   │
    │ (f_t)   │ │ (i_t)   │ │ (o_t)   │
    └────┬────┘ └────┬────┘ └────┬────┘
         │           │           │
         │    ┌──────┴──────┐    │
         │    │  Candidate  │    │
         │    │   (C̃_t)    │    │
         │    └──────┬──────┘    │
         │           │           │
         ▼           ▼           │
        (×) ──────→ (+) ──────→ (×) ──→ h_t (Hidden State)
         │           │           │
         │           ▼           │
         │      C_t (New Cell)   │
         │           │           │
         └───────────┴───────────┘

    게이트 식:
    f_t = σ(W_f·[h_{t-1}, x_t] + b_f)  ... 잊을 비율 (0~1)
    i_t = σ(W_i·[h_{t-1}, x_t] + b_i)  ... 입력할 비율 (0~1)
    o_t = σ(W_o·[h_{t-1}, x_t] + b_o)  ... 출력할 비율 (0~1)
    C̃_t = tanh(W_C·[h_{t-1}, x_t] + b_C)  ... 후보 값 (-1~1)
    C_t = f_t ⊙ C_{t-1} + i_t ⊙ C̃_t  ... 셀 상태 갱신
    h_t = o_t ⊙ tanh(C_t)  ... 은닉 상태 출력

<<< BPTT (Backpropagation Through Time) >>>

    t=1     t=2     t=3     t=4
     │       │       │       │
    ▼       ▼       ▼       ▼
    RNN ──→ RNN ──→ RNN ──→ RNN ──→ Loss
     ▲       ▲       ▲       ▲
     │       │       │       │
     └───────┴───────┴───────┘
           Gradient Flow
           (역전파가 시간을 거슬러 올라감)
```

#### 3. 심층 동작 원리: 기울기 소실 문제와 LSTM의 해결책

**기본 RNN의 기울기 소실 증명**:
$$\frac{\partial h_t}{\partial h_k} = \prod_{i=k+1}^{t} \frac{\partial h_i}{\partial h_{i-1}} = \prod_{i=k+1}^{t} W_{hh}^T \cdot \text{diag}(\tanh'(z_i))$$

tanh의 미분값 최대는 1이고 실제로는 0.25~0.5 정도입니다. 시퀀스 길이가 길어지면(t-k가 크면), 이 값들이 계속 곱해져서 0에 수렴합니다.

**LSTM의 해결책**:
- Cell State는 덧셈 연산(+)으로 갱신됩니다: $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$
- Forget Gate가 1에 가까우면, 기울기가 그대로 전파됩니다: $\frac{\partial C_t}{\partial C_{t-1}} \approx 1$
- 이를 "Constant Error Carousel"이라고 합니다.

#### 4. 실무 수준의 PyTorch LSTM 구현 코드

```python
"""
Production-Ready LSTM for Sequence Classification & Generation
- 양방향(Bidirectional), 멀티 레이어, Attention 지원
- 텍스트 분류, 시계열 예측, 언어 모델링 활용 가능
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple

class AttentionLayer(nn.Module):
    """
    LSTM 출력에 적용하는 Attention 층
    - 각 시점의 중요도를 학습하여 가중 평균 계산
    """
    def __init__(self, hidden_dim: int):
        super().__init__()
        self.attention = nn.Linear(hidden_dim, 1)

    def forward(self, lstm_output: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Args:
            lstm_output: (batch, seq_len, hidden_dim)
            mask: (batch, seq_len) - 패딩 위치 표시
        Returns:
            context: (batch, hidden_dim)
        """
        # Attention Score 계산
        scores = self.attention(lstm_output).squeeze(-1)  # (batch, seq_len)

        # Mask 적용 (패딩 부분은 -inf로)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))

        # Softmax로 가중치 계산
        weights = F.softmax(scores, dim=1)  # (batch, seq_len)

        # 가중 합 (Context Vector)
        context = torch.bmm(weights.unsqueeze(1), lstm_output).squeeze(1)  # (batch, hidden_dim)

        return context


class ProductionLSTM(nn.Module):
    """
    엔터프라이즈급 LSTM 모델
    - Bidirectional, Multi-layer, Dropout, Attention 지원
    - 텍스트 분류, 시계열 예측용
    """
    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int,
        hidden_dim: int,
        output_dim: int,
        num_layers: int = 2,
        bidirectional: bool = True,
        dropout: float = 0.3,
        use_attention: bool = True,
        padding_idx: int = 0
    ):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.bidirectional = bidirectional
        self.use_attention = use_attention
        self.num_directions = 2 if bidirectional else 1

        # Embedding Layer
        self.embedding = nn.Embedding(
            vocab_size, embedding_dim,
            padding_idx=padding_idx
        )

        # LSTM Layer
        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            bidirectional=bidirectional,
            dropout=dropout if num_layers > 1 else 0,
            batch_first=True
        )

        # Attention (옵션)
        if use_attention:
            self.attention = AttentionLayer(hidden_dim * self.num_directions)

        # Dropout
        self.dropout = nn.Dropout(dropout)

        # Fully Connected Layer
        fc_input_dim = hidden_dim * self.num_directions
        self.fc = nn.Linear(fc_input_dim, output_dim)

    def forward(
        self,
        x: torch.Tensor,
        lengths: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Args:
            x: (batch, seq_len) - 토큰 인덱스
            lengths: (batch,) - 실제 시퀀스 길이 (패딩 제외)
        Returns:
            output: (batch, output_dim) - 분류 로짓
        """
        batch_size, seq_len = x.shape

        # Embedding: (batch, seq_len, embedding_dim)
        embedded = self.dropout(self.embedding(x))

        # Pack padded sequence for efficiency
        if lengths is not None:
            packed = nn.utils.rnn.pack_padded_sequence(
                embedded, lengths.cpu(),
                batch_first=True, enforce_sorted=False
            )
            lstm_out, (hidden, cell) = self.lstm(packed)
            lstm_out, _ = nn.utils.rnn.pad_packed_sequence(
                lstm_out, batch_first=True,
                total_length=seq_len
            )
        else:
            lstm_out, (hidden, cell) = self.lstm(embedded)

        # lstm_out: (batch, seq_len, hidden_dim * num_directions)

        if self.use_attention:
            # Attention 적용
            mask = (x != 0).float() if lengths is None else None
            context = self.attention(lstm_out, mask)
        else:
            # 마지막 hidden state 사용
            # Bidirectional인 경우 forward와 backward의 마지막 상태 연결
            if self.bidirectional:
                hidden_last = torch.cat([hidden[-2], hidden[-1]], dim=1)
            else:
                hidden_last = hidden[-1]
            context = hidden_last

        # Classification
        context = self.dropout(context)
        output = self.fc(context)

        return output


class SequenceToSequenceLSTM(nn.Module):
    """
    Seq2Seq LSTM (Encoder-Decoder)
    - 기계 번역, 텍스트 요약용
    - Teacher Forcing 지원
    """
    def __init__(
        self,
        src_vocab_size: int,
        tgt_vocab_size: int,
        embedding_dim: int,
        hidden_dim: int,
        num_layers: int = 2,
        dropout: float = 0.3
    ):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.tgt_vocab_size = tgt_vocab_size

        # Encoder
        self.encoder_embedding = nn.Embedding(src_vocab_size, embedding_dim)
        self.encoder_lstm = nn.LSTM(
            embedding_dim, hidden_dim, num_layers,
            dropout=dropout, batch_first=True
        )

        # Decoder
        self.decoder_embedding = nn.Embedding(tgt_vocab_size, embedding_dim)
        self.decoder_lstm = nn.LSTM(
            embedding_dim, hidden_dim, num_layers,
            dropout=dropout, batch_first=True
        )
        self.fc_out = nn.Linear(hidden_dim, tgt_vocab_size)

        self.dropout = nn.Dropout(dropout)

    def encode(
        self,
        src: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """인코더: 소스 문장을 컨텍스트 벡터로 인코딩"""
        embedded = self.dropout(self.encoder_embedding(src))
        _, (hidden, cell) = self.encoder_lstm(embedded)
        return hidden, cell

    def decode_step(
        self,
        input_token: torch.Tensor,
        hidden: torch.Tensor,
        cell: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """디코더 한 스텝: 다음 토큰 예측"""
        embedded = self.dropout(self.decoder_embedding(input_token))
        output, (hidden, cell) = self.decoder_lstm(embedded, (hidden, cell))
        prediction = self.fc_out(output.squeeze(1))
        return prediction, hidden, cell

    def forward(
        self,
        src: torch.Tensor,
        tgt: torch.Tensor,
        teacher_forcing_ratio: float = 0.5
    ) -> torch.Tensor:
        """
        Args:
            src: (batch, src_len)
            tgt: (batch, tgt_len)
            teacher_forcing_ratio: 정답 토큰을 입력으로 사용할 확률
        """
        batch_size, tgt_len = tgt.shape

        # 인코딩
        hidden, cell = self.encode(src)

        # 디코딩
        outputs = torch.zeros(batch_size, tgt_len, self.tgt_vocab_size).to(src.device)
        input_token = tgt[:, 0].unsqueeze(1)  # <SOS> 토큰

        for t in range(1, tgt_len):
            prediction, hidden, cell = self.decode_step(input_token, hidden, cell)
            outputs[:, t] = prediction

            # Teacher Forcing vs Model Prediction
            use_teacher_forcing = torch.rand(1).item() < teacher_forcing_ratio
            top1 = prediction.argmax(1).unsqueeze(1)
            input_token = tgt[:, t].unsqueeze(1) if use_teacher_forcing else top1

        return outputs


# 사용 예시
if __name__ == "__main__":
    # 텍스트 분류 LSTM (감성 분석)
    model = ProductionLSTM(
        vocab_size=10000,
        embedding_dim=300,
        hidden_dim=256,
        output_dim=2,  # 긍정/부정
        num_layers=2,
        bidirectional=True,
        dropout=0.3,
        use_attention=True
    )

    # 더미 데이터
    batch_size, seq_len = 32, 50
    dummy_input = torch.randint(0, 10000, (batch_size, seq_len))
    output = model(dummy_input)

    print(f"Model Parameters: {sum(p.numel() for p in model.parameters()):,}")
    print(f"Input Shape: {dummy_input.shape}")
    print(f"Output Shape: {output.shape}")  # (32, 2)
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. RNN 변형 모델 심층 비교

| 모델 | 게이트 수 | 파라미터 | 장점 | 단점 | 주요 용도 |
|:---|:---|:---|:---|:---|:---|
| **Vanilla RNN** | 0 | 3×h² | 구조 단순 | 기울기 소실 | 단순 패턴 |
| **LSTM** | 3 | 4×4×h² | 장기 기억, 안정적 | 파라미터 많음 | 번역, 음성 |
| **GRU** | 2 | 3×3×h² | LSTM보다 가벼움 | 장기 기억 약간 부족 | 실시간 처리 |
| **Peephole LSTM** | 3 | 4×4×h²+α | 셀 상태 직접 참조 | 복잡도 증가 | 정밀 제어 |
| **Bi-LSTM** | 3×2 | 2×LSTM | 양방향 문맥 | 미래 정보 필요 | 품사 태깅 |

#### 2. 시퀀스 모델링 기법 비교

| 기법 | 설명 | 장점 | 단점 |
|:---|:---|:---|:---|
| **Teacher Forcing** | 학습 시 정답 토큰 입력 | 빠른 수렴 | 노출 편향(exposure bias) |
| **Scheduled Sampling** | 점진적으로 모델 예측 사용 | 노출 편향 완화 | 하이퍼파라미터 추가 |
| **Beam Search** | 추론 시 상위 N개 후보 유지 | 더 나은 출력 | 연산량 증가 |
| **Attention** | 모든 시점 가중 참조 | 장기 의존성 완벽 해결 | 메모리 O(n²) |

#### 3. 과목 융합 관점 분석

*   **[RNN + 자연어 처리]**:
    품사 태깅, 개체명 인식(NER), 감성 분석 등에서 Bi-LSTM + CRF 조합이 표준이었습니다. 현재는 Transformer가 대세지만, 소규모 데이터셋에서는 여전히 LSTM이 효율적입니다.

*   **[RNN + 음성 처리]**:
    CTC(Connectionist Temporal Classification) 손실 함수와 결합하여 음성 인식(ASR)에 활용됩니다. Whisper, Wav2Vec 등 Transformer 기반 모델로 대체되는 추세입니다.

*   **[RNN + 시계열 분석]**:
    주가 예측, 수요 예측, 이상 탐지에서 여전히 널리 사용됩니다. Transformer 대비 적은 데이터로도 학습 가능하고 해석이 용이합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단: 실무 시나리오

**시나리오 A: 실시간 주가 예측 시스템**
*   **상황**: 분 단위 주가 데이터(하루 390개), 다음 5분 후 가격 예측, 지연 <100ms
*   **기술사 판단**:
    1.  **모델 선택**: Stacked LSTM (2층, 128 유닛)
    2.  **입력 특성**: 시가, 고가, 저가, 종가, 거래량 + 기술적 지표 10개
    3.  **윈도우 크기**: 60분 (60개 타임스텝)
    4.  **출력**: 다음 5분 후 수익률 (회귀)
    5.  **성능**: MAPE 2.5%, 지연 30ms

**시나리오 B: 고객 문의 자동 분류**
*   **상황**: 일일 10,000건 고객 문의, 20개 카테고리 분류, 정확도 90% 이상
*   **기술사 판단**:
    1.  **모델 선택**: Bi-LSTM + Attention
    2.  **임베딩**: FastText 사전 학습된 한국어 임베딩 (300차원)
    3.  **데이터**: 과거 1년치 라벨링된 문의 50만 건
    4.  **성능**: 정확도 92%, 처리 속도 1000건/초

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **시퀀스 길이**: LSTM은 100~200 스텝 이상에서 성능 저하. 더 길면 Transformer 권장.
- [ ] **데이터 양**: 시계열의 경우 최소 1,000~10,000 샘플 필요
- [ ] **양방향 여부**: 미래 정보를 볼 수 있는지 확인 (실시간 예측은 단방향)
- [ ] **Attention 추가**: 긴 시퀀스에서 중요 부분 강조 필요 시
- [ ] **그래디언트 클리핑**: RNN/LSTM 학습 시 필수 (max_norm=1.0~5.0)

#### 3. 안티패턴 (Anti-patterns)

*   **안티패턴 1: 너무 깊은 LSTM**: 4층 이상은 과적합 위험. Dropout과 함께 사용 필요.
*   **안티패턴 2: 패딩 처리 무시**: 가변 길이 시퀀스에서 pack_padded_sequence 미사용 → 패딩까지 학습.
*   **안티패턴 3: 타임스텝 무시**: 1분 데이터와 1일 데이터를 동일하게 취급 → 적절한 윈도우 설계 필요.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 기존 방식 (n-gram, HMM) | RNN/LSTM | 향상 지표 |
|:---|:---|:---|:---|
| **기계 번역** | BLEU 0.25 | BLEU 0.35 (LSTM) | +40% |
| **음성 인식** | WER 15% | WER 8% (LSTM+CTC) | -47% |
| **시계열 예측** | MAPE 5% | MAPE 2% (LSTM) | -60% |
| **학습 데이터** | 수동 규칙 | 자동 학습 | 공수 90% 감소 |

#### 2. 미래 전망 및 진화 방향

**단기 (2024~2026)**:
- **Transformer 대체**: NLP에서 Transformer가 주류. LSTM은 시계열, 소규모 NLP에 국한.
- **경량화**: 양자화, 프루닝으로 엣지 디바이스 배포 증가.

**중기 (2027~2030)**:
- **SNN (Spiking Neural Network)**: RNN의 생물학적 모델로 진화
- **Mamba/SSM**: State Space Model이 순차 데이터 처리의 새로운 대안

**장기 (2030~)**:
- **뉴로모픽 칩**: LSTM을 하드웨어로 구현한 초저전력 칩
- **양자 RNN**: 양자 중첩으로 병렬 시퀀스 처리

#### 3. 참고 표준 및 가이드라인

*   **Hugging Face Transformers**: LSTM 모델 라이브러리
*   **ONNX RNN Support**: LSTM 모델 포맷 표준
*   **TensorFlow Lite**: 모바일 LSTM 추론

---

### 📌 관련 개념 맵 (Knowledge Graph)

*   **[트랜스포머](@/studynotes/10_ai/01_dl/transformer_architecture.md)**: RNN을 대체한 어텐션 기반 구조
*   **[어텐션 메커니즘](@/studynotes/10_ai/01_dl/attention_mechanism.md)**: RNN의 한계를 극복한 집중 메커니즘
*   **[Seq2Seq](@/studynotes/10_ai/01_dl/seq2seq_model.md)**: LSTM 기반의 인코더-디코더 구조
*   **[시계열 분석](@/studynotes/10_ai/02_ml/time_series_analysis.md)**: RNN/LSTM의 주요 응용 분야
*   **[음성 인식](@/studynotes/10_ai/01_dl/speech_recognition.md)**: CTC와 결합한 LSTM 응용

---

### 👶 어린이를 위한 3줄 비유 설명

1.  **이야기 기억하기**: RNN은 책을 읽을 때 앞 내용을 기억하면서 다음 내용을 이해하는 것처럼, 이전에 본 것을 기억하고 있어요.
2.  **스마트 노트**: LSTM은 중요한 내용은 '노트'에 적어두고, 필요없는 건 지우고, 중요한 건 계속 기억하는 똑똑한 독서가예요.
3.  **순서 중요**: "은행"이란 단어가 앞에 "돈"이 있으면 금융기관, "강"이 있으면 강둑이라는 걸 아는 것처럼, 문맥을 이해하는 능력이 있어요!
