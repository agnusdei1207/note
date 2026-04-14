+++
weight = 124
title = "셀프 어텐션 (Self-Attention)"
date = "2025-05-15"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
- 입력 시퀀스 내의 모든 단어가 **서로를 참조**하여 문맥적 의미를 파악하는 내부 응집 기법이다.
- "The animal didn't cross the street because **it** was too tired"에서 'it'이 'animal'임을 수학적으로 찾아내는 핵심 기술이다.
- 거리에 상관없이 단어 간의 직접적인 연결을 형성하여 RNN의 고질적인 **장기 의존성(Long-term Dependency)** 문제를 해결한다.

### Ⅰ. 개요 (Context & Background)
전통적인 RNN은 단어를 순차적으로 처리하며 정보를 압축하기 때문에, 문장이 길어지면 앞쪽의 정보를 잃어버리는 한계가 있었다. 셀프 어텐션은 문장 전체를 한꺼번에 입력받아, 모든 단어 쌍(Pairwise)에 대해 유사도를 계산한다. 이를 통해 각 단어는 자신을 둘러싼 주변 맥락(Context)을 완벽하게 반영한 새로운 벡터 표현을 얻게 된다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
셀프 어텐션은 동일한 시퀀스에서 유래한 Q, K, V를 사용하여 연산을 수행한다.

```text
[Self-Attention Mechanism: Intra-sequence Relationship]

Input Sequence: "I love learning AI"
                 X1  X2     X3    X4

Step 1: Each Xi generates Qi, Ki, Vi via weight matrices.

Step 2: Score Calculation (Similarity check within same sentence)
   Score(X1, X1), Score(X1, X2), Score(X1, X3), Score(X1, X4)
   - "I" relates to "I", "love", "learning", "AI"

Step 3: Softmax Normalization
   Weights = Softmax(Scores)

Step 4: Weighted Sum of Values
   Contextual_X1 = Σ (Weights * Vi)

[Architecture Diagram]
     [I]    [love]   [learning]   [AI]
      |       |          |         |
   +--v-------v----------v---------v--+
   |        Self-Attention Layer      |  <-- Every word looks at 
   |      (All-to-All Interaction)    |      every other word.
   +--|-------|----------|---------|--+
      v       v          v         v
    [C1]    [C2]       [C3]      [C4]    <-- Context-aware vectors
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Criteria) | 셀프 어텐션 (Self-Attention) | RNN (Recurrent) | CNN (Convolutional) |
| :--- | :--- | :--- | :--- |
| **문맥 참조 범위** | **전체 시퀀스 (Global)** | 이전 상태 (Sequential) | 윈도우 크기 내 (Local) |
| **병렬 처리** | **완전 가능 (Highly Parallel)** | 불가능 (Step-by-step) | 가능 (Filter-based) |
| **장거리 의존성** | **상수 시간 O(1) 연결** | 선형 시간 O(n) 소실 | 로그 시간 O(log n) |
| **연산 복잡도** | O(n² · d) (시퀀스 길이 제곱) | O(n · d²) | O(k · n · d²) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **(문맥적 중의성 해결)** "Bank"라는 단어가 "River bank"인지 "Investment bank"인지 주변 단어와의 셀프 어텐션 강도를 통해 즉각적으로 판별한다.
- **(연산 비용 이슈)** 시퀀스 길이(n)의 제곱에 비례하는 연산 복잡도 때문에, 아주 긴 문서(Long Context) 처리 시 메모리 부족 문제가 발생한다. 이를 위해 **Linear Attention**이나 **Flash Attention** 같은 최적화 기법이 실무적으로 중요하다.
- **(기술사적 가치)** 셀프 어텐션은 '정적인 단어장'을 '살아있는 문맥'으로 변환하는 **다이나믹 그래프** 생성 기술이며, 이는 인공지능이 인간의 언어 이해 방식과 유사한 추론을 수행하게 하는 결정적 계기가 되었다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
셀프 어텐션은 트랜스포머의 핵심 엔진으로서 NLP를 넘어 비전(Vision Transformer), 단백질 구조 예측(AlphaFold 2) 등 다양한 도메인으로 확장되고 있다. 데이터 내의 숨겨진 모든 관계를 스스로 찾아내는 이 메커니즘은 '범용 인공지능(AGI)'으로 가는 가장 중요한 수학적 도구로 평가받는다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: 어텐션 메커니즘(Attention Mechanism)
- **자식/확장 개념**: 멀티 헤드 어텐션(Multi-Head Attention), 마스크드 셀프 어텐션(Masked Self-Attention)
- **유사 개념**: 그래프 신경망(GNN - 노드 간 관계 처리), 완전 연결망(Fully Connected)

### 👶 어린이를 위한 3줄 비유 설명
1. 교실에 있는 모든 친구들이 서로를 쳐다보면서 "누가 나랑 제일 친한가?" 생각해요.
2. "나(it)"라는 단어는 "강아지(animal)"라는 친구를 가장 빤히 쳐다보며 그 뜻을 이해해요.
3. 이렇게 서로를 꼼꼼히 살펴보면 문장 속의 숨은 뜻을 완벽하게 알 수 있답니다!
