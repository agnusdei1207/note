+++
title = "텐서플로우 배열 (TensorFlow Tensors: Scalar, Vector, Matrix, Tensor)"
weight = 107
date = "2026-03-04"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
1. **텐서(Tensor)**는 다차원 배열을 의미하며, 0차원(스칼라)부터 N차원까지 데이터를 일관된 수학적 구조로 표현하는 딥러닝의 기본 단위이다.
2. 텐서플로우는 텐서를 통해 병렬 연산을 가속화하고, 미분 가능(Differentiable)한 계산 그래프(Computation Graph) 상에서 데이터를 전달한다.
3. 텐서의 **Shape(형태)**와 **Rank(차원)**는 신경망 계층 간의 데이터 흐름과 행렬 곱 연산의 적합성을 결정하는 핵심 속성이다.

### Ⅰ. 개요 (Context & Background)
- **배경**: 인공신경망은 수많은 가중치와 입력 데이터의 연산으로 구성되며, 이를 효율적으로 처리하기 위해 고차원 수치 배열 데이터 구조인 '텐서'가 필수적이다.
- **필요성**: GPU/TPU와 같은 가속기에서 대규모 행렬 연산을 병렬로 수행하기 위해서는 모든 데이터를 표준화된 다차원 배열 구조로 관리해야 한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **차원별 구성**:
  - **Rank 0 (Scalar)**: 하나의 값 (예: `s = 7`)
  - **Rank 1 (Vector)**: 1차원 배열 (예: `v = [1.0, 2.0, 3.0]`)
  - **Rank 2 (Matrix)**: 2차원 배열 (예: `m = [[1, 2], [3, 4]]`)
  - **Rank 3+ (Tensor)**: 3차원 이상의 고차원 배열 (예: 이미지 데이터 `[Height, Width, Channels]`)

```text
[TensorFlow Data Structure Hierarchy]

(Rank 0)   (Rank 1)        (Rank 2)             (Rank 3)
 Scalar     Vector         Matrix               Tensor (3D+)
  [5]      [1, 2, 3]    [[1, 2], [3, 4]]   [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
   |           |                |                    |
   +-----------+----------------+--------------------+
               | (All are 'tf.Tensor' objects)       |
               | - dtype (float32, int32, etc.)      |
               | - shape (dimensions)                |
               +-------------------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | NumPy Array (ndarray) | TensorFlow Tensor (tf.Tensor) |
| :--- | :--- | :--- |
| **연산 장치** | CPU 전용 | CPU, GPU, TPU 지원 (가속 가능) |
| **불변성 (Immutability)** | 가변적 (내부 값 수정 가능) | 불변 (수정 시 새로운 텐서 생성) |
| **기울기 추적** | 불가능 (수동 계산) | 자동 미분(Auto-grad) 지원 (학습 필수) |
| **실행 방식** | 즉시 실행 (Imperative) | 그래프 최적화 및 Eager Execution 지원 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **실무 적용**: 배치(Batch) 단위의 데이터 처리 시 4차원 텐서(`[Batch, Height, Width, Channel]`)를 기본으로 사용하며, 자연어 처리에서는 3차원 텐서(`[Batch, SeqLen, Embedding]`)를 주로 사용한다.
- **기술사적 판단**: 텐서 연산 시 `Broadcasting`(크기가 다른 텐서 간 연산) 규칙과 `Reshape`(차원 변형)의 원리를 정확히 이해해야 차원 불일치(Dimension Mismatch) 에러를 방지하고 메모리 효율적인 코드를 작성할 수 있다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 데이터 구조를 추상화함으로써 복잡한 딥러닝 알고리즘을 수학 기호와 유사하게 직관적으로 코딩할 수 있게 한다.
- **결론**: 텐서는 인공지능의 공용어이며, 텐서플로우와 파이토치 등 모든 프레임워크가 이를 중심으로 설계되어 있어 데이터 엔지니어에게 필수적인 소양이다.

### 📌 관련 개념 맵 (Knowledge Graph)
1. **tf.Variable**: 훈련 중에 변경되는 가중치(Weights)를 담는 텐서
2. **Reshape & Transpose**: 텐서의 모양을 바꾸거나 축을 교체하는 연산
3. **Sparse Tensor**: 대부분이 0인 데이터를 효율적으로 저장하는 특수 텐서

### 👶 어린이를 위한 3줄 비유 설명
1. **스칼라/벡터/매트릭스**: 스칼라는 '사과 한 개', 벡터는 '사과 한 줄', 매트릭스는 '사과 상자'라고 생각하면 돼요.
2. **텐서**: 사과 상자들을 트럭에 가득 실은 '거대한 사과 창고'가 바로 텐서예요.
3. **결론**: 아주 작은 숫자부터 아주 큰 덩어리 숫자까지 모두 똑같은 방식으로 다룰 수 있게 해주는 마법의 바구니예요.
