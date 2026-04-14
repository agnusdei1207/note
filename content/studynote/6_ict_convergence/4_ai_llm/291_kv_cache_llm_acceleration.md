+++
title = "291. KV 캐시 (Key-Value Cache) - LLM 텍스트 추론 가속화"
date = "2026-04-11"
weight = 291
[extra]
categories = "studynote-ict-convergence"
+++

# 291. KV 캐시 (Key-Value Cache)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: KV 캐시는 대규모 언어 모델(LLM)이 문장을 생성할 때, 이전에 처리한 토큰들의 Key(키)와 Value(값) 행렬을 메모리에 저장해 두어 중복 연산을 피하는 최적화 기법이다.
> 2. **필요성**: 오토레그레시브 생성 특성상 매 단계마다 전체 문맥을 다시 계산(Self-Attention)해야 하는데, 이를 방지하여 추론 속도(Throughput)를 획기적으로 높여준다.
> 3. **문제점**: 긴 문장을 생성할수록 KV 캐시가 차지하는 VRAM(GPU 메모리) 용량이 기하급수적으로 늘어나며, 메모리 파편화(Fragmentation) 이슈가 발생한다.

---

### Ⅰ. 개요 (Context & Background)
LLM 서비스의 비용은 대부분 GPU 메모리 점유율에서 발생한다. 특히 사용자의 질문이 길어질수록 어텐션 연산량은 제곱으로 늘어난다. KV 캐시는 이미 계산된 정보를 재활용함으로써 연산 자원을 절약하지만, 반대로 GPU 메모리를 많이 소모하는 트레이드오프(Trade-off) 관계에 있다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
[ Without KV Cache: Full Re-computation ]
Step N: Input [T1, T2, T3, T4] -> Compute Attention(T1~T4) -> Predict T5

[ With KV Cache: Incremental Update ]
Step N-1: [T1, T2, T3] processed. Store {K1~K3, V1~V3} in GPU Memory.
Step N:   [T4] arrives. Only compute {K4, V4}.
          Combined with Cached {K1~K3, V1~V3} -> Predict T5

* Bilingual Legend:
- Key-Value Cache: KV matrix storage (Key/Value 행렬 저장소)
- Self-Attention: Relation calculation (자가 어텐션 연산)
- Inference Throughput: Generation speed (추론 처리량)
- Memory Fragmentation: Unused space gaps (메모리 파편화)
```

1. **상태 보존 (State Retention)**: 트랜스포머 모델의 각 레이어에서 생성된 이전 토큰들의 Key와 Value 벡터를 캐시 슬롯에 담아둔다.
2. **연산량 감소**: 매 단계에서 '새로운 토큰 하나'에 대한 K, V 값만 계산하면 되므로, 전체 문맥을 다시 훑는 O(N^2) 연산을 O(N) 수준으로 체감상 낮출 수 있다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | KV 캐시 미사용 (None) | KV 캐시 사용 (KV Caching) |
| :--- | :--- | :--- |
| **연산량 (Flops)** | 토큰이 늘어날수록 급증 (Heavy) | 새로운 토큰만 연산 (Efficient) |
| **메모리 점유 (VRAM)** | 모델 가중치 중심 (Static) | 문맥 길이에 따라 증가 (Dynamic) |
| **추론 지연 (Latency)** | 매우 느림 (Long context 시) | 매우 빠름 (연산 오버헤드 제거) |
| **최대 문맥 길이** | 하드웨어 한계까지 가능 | 캐시 메모리 용량에 의해 제한됨 |
| **핵심 이슈** | 연산 병목 (Compute Bound) | 메모리 대역폭 병목 (Memory Bound) |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
1. **메모리 파편화 해결**: KV 캐시는 메모리를 정적으로 미리 할당하여 낭비되는 공간이 많다. 이를 해결하기 위해 **PagedAttention (vLLM)** 같은 기술을 사용하여 메모리를 페이징 단위로 관리하는 것이 필수적이다.
2. **모델 아키텍처 개선**: 모든 헤드의 KV를 공유하는 **MQA (Multi-Query Attention)**나 그룹별로 공유하는 **GQA (Grouped-Query Attention)**를 적용하여 캐시 용량을 8배 이상 줄일 수 있다.
3. **양자화 (Quantization)**: KV 캐시 자체를 FP16에서 INT8/INT4로 양자화하여 더 적은 메모리로 더 긴 문맥(Long Context)을 처리할 수 있게 설계해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
KV 캐시는 LLM의 상용화(Inference Optimization)를 가능하게 한 1등 공신이다. 향후에는 수백만 토큰의 문맥을 처리하는 'Infinite Context' 시대를 위해, 중요하지 않은 캐시를 삭제하는 'Cache Eviction' 기법이나, 보조 기억 장치를 활용하는 'Offloading' 기술이 더욱 발전할 것이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 트랜스포머 추론 최적화(Inference Optimization)
- **동등 개념**: vLLM (PagedAttention), MQA/GQA
- **하위 개념**: VRAM 파편화, 정적 할당, 양자화(Quantization)

---

### 👶 어린이를 위한 3줄 비유 설명
1. **중간 저장**: 수학 문제를 풀 때, 앞에서 계산한 중간 정답을 종이 구석에 적어놓는 것과 같아요.
2. **시간 절약**: 다음에 똑같은 계산이 나오면 다시 풀지 않고, 적어놓은 정답을 바로 보고 다음 단계로 넘어갈 수 있어요.
3. **공간 필요**: 하지만 적어놓을 종이가 부족해지면 더 이상 문제를 풀 수 없으니, 종이를 아껴 쓰는 지혜가 필요하답니다.
