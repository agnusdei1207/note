+++
weight = 140
title = "140. 셀프 어텐션 (Self-Attention) / 멀티 헤드 어텐션 / 포지셔널 인코딩"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 셀프 어텐션은 쿼리(Query), 키(Key), 값(Value) 세 행렬로 시퀀스 내 모든 위치 간 관계를 한 번에 계산한다.
> 2. **가치**: 멀티 헤드 어텐션(Multi-Head Attention)은 복수 어텐션 헤드를 병렬 실행해 다양한 언어적 관계(구문, 의미, 지시 대명사 등)를 동시에 포착한다.
> 3. **판단 포인트**: 포지셔널 인코딩(Positional Encoding)은 순서 정보가 없는 어텐션에 위치 신호를 주입하며, 절대 위치(Sinusoidal)와 상대 위치(RoPE, ALiBi) 방식이 현대 LLM에서 병렬 선택된다.

## Ⅰ. 개요 및 필요성

Transformer의 셀프 어텐션은 "시퀀스 내 토큰들이 서로에게 어떻게 주의를 기울이는가"를 계산한다. 외부 입력 없이 자기 자신의 시퀀스 내에서 어텐션을 수행하는 것이 "셀프(Self)"이다.

기존 어텐션(Bahdanau)이 인코더-디코더 간 관계를 계산했다면, 셀프 어텐션은 동일 시퀀스 내 토큰 간 관계를 계산한다.

**예시**: "The animal didn't cross the street because it was too tired"
→ 셀프 어텐션이 "it"이 "animal"을 가리킨다는 것을 학습

📢 **섹션 요약 비유**: 셀프 어텐션은 회의에서 각 참석자가 다른 모든 참석자의 발언에 얼마나 주의를 기울일지를 스스로 결정하는 메커니즘이다.

## Ⅱ. 아키텍처 및 핵심 원리

### Scaled Dot-Product Attention

| 단계 | 연산 | 설명 |
|:---|:---|:---|
| Q, K, V 생성 | Q=XWQ, K=XWK, V=XWV | 입력 X를 3개 행렬로 선형 변환 |
| 점수 계산 | QKᵀ / √dₖ | 쿼리-키 내적 후 차원 크기로 스케일 |
| Softmax | softmax(QKᵀ/√dₖ) | 어텐션 가중치 정규화 |
| 출력 | Attention(Q,K,V) = softmax(QKᵀ/√dₖ)V | 가중 합산 |

```
[Scaled Dot-Product Attention]

     Q (Query)   K (Key)   V (Value)
         │           │          │
         └─────┐      │          │
               ▼      ▼          │
           MatMul (QKᵀ)          │
               │                 │
           Scale (÷√dₖ)          │
               │                 │
           (Mask Optional)       │
               │                 │
            Softmax              │
               │                 │
               └────MatMul───────┘
                        │
                    Output Z

[Multi-Head Attention (h=8 헤드)]

입력 X
  │
  ├──▶ [Head 1: Q₁K₁V₁] ──▶ Z₁ ┐
  ├──▶ [Head 2: Q₂K₂V₂] ──▶ Z₂ │
  ├──▶ [Head 3: Q₃K₃V₃] ──▶ Z₃ ├──▶ Concat ──▶ WO ──▶ 최종 출력
  │    ...                       │
  └──▶ [Head h: QₕKₕVₕ] ──▶ Zₕ ┘

각 헤드는 독립 가중치 WQᵢ, WKᵢ, WVᵢ로 다른 표현 공간 학습
```

### 포지셔널 인코딩 (Positional Encoding)

어텐션은 위치 무관 → 순서 정보를 명시적으로 주입해야 함

| 방식 | 수식/특징 | 사용 모델 |
|:---|:---|:---|
| Sinusoidal (절대) | PE(pos,2i) = sin(pos/10000^(2i/d)) | 원래 Transformer |
| Learned (학습형) | 임베딩 파라미터로 학습 | BERT, GPT-2 |
| RoPE (회전 위치) | 쿼리-키를 회전 행렬로 인코딩 | LLaMA, GPT-NeoX |
| ALiBi (선형 편향) | 어텐션 점수에 거리 패널티 선형 부가 | MPT, BLOOM |

📢 **섹션 요약 비유**: Q는 "나는 무엇을 찾는가?", K는 "나는 무엇을 갖고 있는가?", V는 "실제로 꺼낼 내용"이다. 이 세 역할의 분리가 셀프 어텐션의 핵심이다.

## Ⅲ. 비교 및 연결

| 항목 | 단일 헤드 어텐션 | 멀티 헤드 어텐션 |
|:---|:---|:---|
| 관계 포착 관점 | 단일 | 복수 (구문적, 의미적, 지시 관계 등) |
| 표현 공간 | 1개 | h개 (서로 다른 서브공간) |
| 계산 비용 | 낮음 | h배 (단, 차원 축소로 실제 유사) |
| 성능 | 열세 | 우세 |

**어텐션 복잡도 문제**
- 시퀀스 길이 n에 대해 O(n²) 메모리 및 연산
- 긴 문서 처리: Sparse Attention (Longformer), Flash Attention으로 해결
- Flash Attention: IO-aware 알고리즘으로 메모리 사용 10배 절감

📢 **섹션 요약 비유**: 단일 헤드가 한 방향만 보는 사진기라면, 멀티 헤드는 여러 방향을 동시에 촬영하는 360도 카메라다.

## Ⅳ. 실무 적용 및 기술사 판단

**설계 선택 기준**
- 헤드 수(h): 보통 8~16, 모델 차원(d_model)과 d_model/h = d_k로 맞춤
- 컨텍스트 길이 확장: RoPE + NTK 스케일링으로 학습 시보다 긴 시퀀스 추론 가능
- Flash Attention 2: A100 GPU에서 기존 대비 3배 속도 향상

**어텐션 마스킹**
- Encoder Self-Attention: 패딩(Padding) 마스크만 적용
- Decoder Masked Self-Attention: 미래 토큰 참조 차단 (Causal Mask)
- Cross-Attention: 소스 패딩 마스크 적용

**기술사 출제 포인트**
- "Scaled Dot-Product Attention에서 √dₖ 스케일링이 필요한 이유를 설명하시오"
- "멀티 헤드 어텐션이 단일 헤드 대비 갖는 장점을 설명하시오"

📢 **섹션 요약 비유**: √dₖ 스케일링 없이는 내적 값이 너무 커져 Softmax가 극단적 값을 출력한다. 점수지 배점을 표준화하는 것과 같다.

## Ⅴ. 기대효과 및 결론

셀프 어텐션, 멀티 헤드 어텐션, 포지셔널 인코딩은 Transformer의 세 핵심 기둥이다. 이 세 가지가 결합되어 시퀀스 내 복잡한 언어 구조를 병렬로 학습하는 강력한 표현력을 만든다. 현대 LLM의 모든 발전이 이 기반 위에 있다.

📢 **섹션 요약 비유**: 셀프 어텐션은 AI의 '문맥 파악 능력', 멀티 헤드는 '다면적 사고', 포지셔널 인코딩은 '순서 감각'이다. 이 세 가지가 합쳐져 Transformer가 언어를 이해하는 것이다.

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 핵심 연산 | Scaled Dot-Product Attention | Q·Kᵀ/√dₖ·V |
| 확장 | Multi-Head Attention | h개 병렬 어텐션 |
| 위치 정보 | Positional Encoding | Sinusoidal, RoPE, ALiBi |
| 마스킹 | Causal Mask | 미래 토큰 차단 (디코더) |
| 최적화 | Flash Attention | IO-aware 고속 구현 |
| 복잡도 | O(n²) | 긴 시퀀스 병목 |

### 👶 어린이를 위한 3줄 비유 설명
1. Q는 "나 이거 알고 싶어", K는 "나 이거 알고 있어", V는 "내가 줄 실제 정보"예요.
2. 여러 개의 어텐션 헤드는 여러 명의 친구에게 동시에 다른 질문을 하는 것과 같아요.
3. 포지셔널 인코딩은 문장에 "이 단어는 첫 번째, 이 단어는 두 번째" 번호표를 붙이는 것이에요.
