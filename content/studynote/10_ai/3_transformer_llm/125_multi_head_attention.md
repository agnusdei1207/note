+++
weight = 125
title = "멀티 헤드 어텐션 (Multi-Head Attention)"
date = "2025-05-15"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
- 셀프 어텐션을 **병렬로 여러 개** 수행하여, 데이터의 다양한 문맥적 측면(문법, 의미, 구조 등)을 동시에 포착한다.
- 하나의 단어가 여러 가지 의미적 관계를 가질 때, 각 **Head**가 서로 다른 관계에 집중함으로써 모델의 표현력을 극대화한다.
- 어텐션 결과를 통합(Concatenate)하고 선형 변환하여, 단일 어텐션보다 훨씬 풍부한 정보를 산출하는 트랜스포머의 핵심 아키텍처다.

### Ⅰ. 개요 (Context & Background)
단일 헤드 어텐션(Single-Head Attention)은 한 문장에서 한 가지 관계에만 집중할 수 있는 편향(Bias)이 생기기 쉽다. 예를 들어 "사과를 먹었다"에서 '사과'가 '먹다'라는 행위의 대상임을 파악하는 동시에, '사과'가 '빨간색'이라는 특징을 가졌다는 정보도 놓치지 않아야 한다. 멀티 헤드 어텐션은 연산 공간을 여러 개로 쪼개어 각기 다른 "시각"에서 정보를 추출함으로써 이러한 다각도 분석을 가능하게 한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
입력 차원(d_model)을 헤드 수(h)로 나누어 병렬 처리한 후 다시 합치는 과정을 거친다.

```text
[Multi-Head Attention Architecture]

1. Splitting (분할): 
   - Input (d_model=512) splits into 8 heads (d_k = 64 each).
   
2. Parallel Attention (병렬 연산):
   - Head 1: Focuses on Grammar (문법적 관계)
   - Head 2: Focuses on Entity (개체 간 관계)
   - ...
   - Head 8: Focuses on Coreference (지칭 관계)

3. Concatenation (결합):
   - Concatenate(head1, head2, ..., head8)

4. Final Linear (선형 변환):
   - Multiply by Wo matrix to get final output dimension.

[Structure Diagram]
        [Input Vector]
       /      |       \
    [Head1] [Head2] [Head-h]  <-- Scaled Dot-Product Attention
       \      |       /
      [  Concatenate  ]
              |
       [Linear Layer]
              |
       [Output Vector]
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Criteria) | 멀티 헤드 어텐션 | 단일 헤드 어텐션 | CNN 필터 비교 |
| :--- | :--- | :--- | :--- |
| **정보 추출 방식** | **다각도 병렬 추출** | 단일 관점 추출 | 다양한 커널(Filter) 사용과 유사 |
| **표현력 (Capacity)** | **매우 높음** | 제한적임 | 높음 (채널 수 비례) |
| **연산 효율성** | 병렬화에 최적화됨 | 단순함 | 로컬 연산 최적 |
| **주요 장점** | 문맥의 중의성 해결 탁월 | 연산 자원 최소화 | 공간 특징 포착 우수 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **(차원 축소의 마법)** 헤드 수를 늘려도 각 헤드의 차원을 줄여서 처리하기 때문에, 단일 헤드 어텐션(전체 차원 사용)과 **총 연산량은 비슷**하면서도 훨씬 정교한 정보를 얻을 수 있는 효율적인 설계다.
- **(앙상블 효과)** 기술사적 관점에서 멀티 헤드 어텐션은 신경망 내부에서 일어나는 **'자기 참조적 앙상블'** 기술이다. 이는 모델이 스스로 중요한 피처를 다각도로 학습하게 만드는 자동화된 특징 추출기 역할을 한다.
- **(파라미터 튜닝)** 헤드 수(h)는 모델의 복잡도와 직결된다. GPT-3의 경우 96개의 헤드를 사용하여 극도로 세밀한 문맥 파악을 수행하며, 이는 모델 성능 향상의 핵심 지표 중 하나다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
멀티 헤드 어텐션은 트랜스포머가 모든 딥러닝 아키텍처의 왕좌를 차지하게 만든 결정적 공헌자다. 현재는 **Multi-Query Attention(MQA)**이나 **Grouped-Query Attention(GQA)** 등으로 변형되어, 추론 속도를 높이면서도 멀티 헤드의 장점을 유지하는 방향으로 진화하고 있다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: 셀프 어텐션(Self-Attention)
- **자식/확장 개념**: GQA(Grouped-Query Attention), MQA(Multi-Query Attention)
- **유사 개념**: 합성곱 신경망의 멀티 필터(CNN Multi-filters), 앙상블 학습(Ensemble Learning)

### 👶 어린이를 위한 3줄 비유 설명
1. 혼자서 숙제를 하는 게 아니라, 8명의 똑똑한 친구들이 팀을 짜서 같이 숙제를 해요.
2. 1번 친구는 글씨가 예쁜지 보고, 2번 친구는 계산이 맞는지 보고, 3번 친구는 내용이 재미있는지 봐요.
3. 마지막에 친구들이 알아낸 걸 다 합치면, 혼자 했을 때보다 훨씬 완벽한 숙제 결과가 나온답니다!
