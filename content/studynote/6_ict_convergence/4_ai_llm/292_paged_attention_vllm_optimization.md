+++
title = "292. 페이즈드 어텐션 (PagedAttention / vLLM) - LLM 추론 가속화를 위한 가상 메모리 관리 혁신"
weight = 292
date = "2026-03-04"
[extra]
categories = "studynote-ict-convergence"
+++

## 핵심 인사이트 (3줄 요약)
- **메모리 파편화 해결:** OS의 가상 메모리 페이징 기법을 차용하여, LLM 추론 시 발생하는 KV 캐시(Key-Value Cache)의 메모리 파편화 문제를 획기적으로 해결한 기술.
- **처리량(Throughput) 극대화:** 낭비되는 GPU 메모리를 최소화하여 기존 서빙 프레임워크 대비 최대 24배 이상의 높은 처리량을 달성하며 LLM 운영 비용(TCO) 절감에 기여.
- **동적 할당 아키텍처:** 고정된 크기의 연속 메모리 할당 대신 필요 시마다 '페이지' 단위로 동적 할당하여 가변적인 텍스트 생성 길이에 유연하게 대응 가능.

### Ⅰ. 개요 (Context & Background)
LLM(초거대 언어 모델) 서비스 운영에서 가장 큰 비용 병목은 GPU 메모리입니다. 특히 텍스트 생성 과정에서 과거 토큰 정보를 저장하는 **KV 캐시**는 메모리 점유율이 매우 높으며, 생성될 텍스트 길이를 미리 알 수 없어 메모리를 과도하게 예약(Over-provisioning)하거나 파편화(Fragmentation)가 발생하는 문제가 있었습니다. UC 버클리 연구진이 제안한 **PagedAttention**은 운영체제의 페이징(Paging) 개념을 도입하여 GPU 메모리를 효율적으로 관리함으로써 이러한 한계를 돌파한 vLLM 프레임워크의 핵심 기술입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
PagedAttention은 연속적인 논리 메모리 주소를 비연속적인 물리 메모리 블록에 매핑하는 방식입니다.

```text
[PagedAttention Concept Map]
 Logical KV Cache (Sequence)        Physical GPU Memory Blocks
 +-----------------------+          +-----------------------+
 | Block 0 (Token 0~3)   | ----\    | [Block 2] [Block 0]   | (Scattered)
 +-----------------------+      \   +-----------------------+
 | Block 1 (Token 4~7)   | ------\  | [Free ] [Block 1]     | (Efficiency)
 +-----------------------+        \ +-----------------------+
 | Block 2 (Token 8~11)  | --------> Block Table (Mapping)
 +-----------------------+

 [Key Mechanism]
 - Divide KV cache into fixed-size "blocks" (Pages).
 - Map logical sequences to physical blocks via a "Block Table".
 - Eliminate internal/external fragmentation in GPU VRAM.
```

1. **블록화 (Blocking):** KV 캐시를 고정된 크기(예: 16개 토큰)의 블록으로 분할.
2. **블록 테이블 (Block Table):** 논리적 시퀀스 순서와 물리적 GPU 메모리 블록 주소를 연결하는 매핑 정보 관리.
3. **동적 할당 (On-demand Allocation):** 토큰이 생성됨에 따라 새로운 블록이 필요할 때만 물리 메모리를 할당하여 낭비 차단.
4. **공유 메커니즘 (Copy-on-Write):** 동일한 프롬프트를 공유하는 여러 요청(Parallel Sampling) 시 메모리 복사 없이 동일 블록 참조 가능.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Comparison) | 기존 서빙 (FasterTransformer 등) | 페이즈드 어텐션 (vLLM) |
|---|---|---|
| **메모리 할당 방식** | 연속적(Continuous) 할당 | 비연속적(Paging) 할당 |
| **메모리 효율** | 파편화 및 오버프로비저닝 발생 (60~80% 낭비) | 96% 이상의 메모리 활용률 달성 |
| **처리량 (Throughput)** | 낮음 (Batch Size 제한) | 매우 높음 (대규모 Batch 가능) |
| **복잡성** | 낮음 | 높음 (블록 테이블 관리 오버헤드) |
| **주요 특징** | 정적 메모리 예약 | 동적 메모리 공유 및 할당 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
**[실무 적용 전략]**
- **비용 최적화:** 동일한 하드웨어에서 더 많은 동시 접속자를 수용할 수 있어 API 서비스 단가를 낮추는 데 결정적 역할을 합니다.
- **멀티 서비스 운영:** 빔 서치(Beam Search)나 다중 출력 샘플링 시 메모리 공유 기능을 극대화하여 추론 자원을 절약할 수 있습니다.

**[기술사적 판단]**
PagedAttention은 하드웨어 성능을 소프트웨어 아키텍처(OS 이론의 전이)로 극복한 대표적 사례입니다. 단순히 알고리즘 개선을 넘어 'LLM 서빙 인프라의 표준'으로 자리 잡았으며, 향후 모델 사이즈가 커질수록 이러한 효율적 자원 관리 기술의 가치는 더욱 증대될 것입니다. 특히 온디바이스(On-device) AI처럼 자원이 극도로 제한된 환경에서도 페이징 기법의 변용이 필수적일 것으로 판단됩니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
PagedAttention의 도입으로 초거대 모델 서빙의 대중화가 가속화되었습니다. 현재 vLLM뿐만 아니라 TGI(Text Generation Inference), TensorRT-LLM 등 주요 프레임워크가 유사한 기법을 채택하고 있습니다. 향후에는 메모리 관리를 넘어 계산 자체를 최적화하는 플래시 어텐션(FlashAttention)과 결합하여 '입출력(IO)과 메모리' 모두를 정복하는 통합 추론 엔진으로 진화할 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **기반 기술:** Virtual Memory, Paging, KV Cache
- **프레임워크:** vLLM, TensorRT-LLM, HuggingFace TGI
- **연관 기술:** FlashAttention, Continuous Batching, Quantization (AWQ/GPTQ)

### 👶 어린이를 위한 3줄 비유 설명
1. **기존 방식**은 기차표를 끊을 때 몇 명이 탈지 몰라 기차 칸 전체를 미리 비워두는 바람에 자리가 텅텅 남는 것과 같아요.
2. **페이즈드 어텐션**은 손님이 한 명 올 때마다 빈 의자를 하나씩 가져다주고, 의자가 부족하면 다른 방에서 가져와서 빈틈없이 앉히는 방법이에요.
3. 덕분에 똑같은 크기의 기차에 훨씬 더 많은 손님이 탈 수 있게 되었답니다!
