+++
title = "87. FP-Growth 알고리즘 - 트리 기반의 고속 빈발 항목 추출"
date = "2026-03-04"
weight = 87
[extra]
categories = ["studynote-data-engineering", "math-mining"]
+++

## 핵심 인사이트 (3줄 요약)
- **Candidate 생성 없음**: 기존 Apriori 알고리즘의 고질적인 문제인 수많은 후보(Candidate) 생성 과정을 생략하여 메모리와 연산 효율을 극대화합니다.
- **FP-Tree 구조**: 데이터셋을 트리(Tree) 형태로 압축하여 저장함으로써, 단 두 번의 데이터베이스 스캔만으로 빈발 항목 세트를 찾아낼 수 있습니다.
- **분할 정복 (Divide & Conquer)**: 트리를 조건부 패턴 기지로 나누어 재귀적으로 탐색함으로써 대규모 데이터셋에서도 빠른 성능을 보장합니다.

### Ⅰ. 개요 (Context & Background)
고전적인 Apriori 알고리즘은 데이터셋을 반복적으로 스캔하고, 지지도 계산을 위해 막대한 양의 후보 조합을 만들어야 하므로 빅데이터 환경에서 성능 병목이 심각합니다. 2000년 Han 등이 제안한 FP-Growth(Frequent Pattern Growth)는 데이터를 트리 구조로 압축하여 저장하고 이를 재귀적으로 탐색하는 방식을 채택하여, 후보 생성 없이도 빈발 항목을 추출할 수 있는 혁신을 가져왔습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
FP-Growth는 1) 빈도순 정렬, 2) FP-Tree 생성, 3) 트리 마이닝의 과정을 거칩니다.

```text
[ FP-Tree Construction & Mining Architecture ]

1. DB Scan 1: Count item frequency and filter infrequent items (Min Support).
2. DB Scan 2: Sort items in each transaction by frequency and build FP-Tree.

[ FP-Tree Structure Diagram ]
       (Root)
       /    \
    {A:8}  {B:5}  <-- Frequent Item Header Table
     /       \
  {C:5}     {D:2} <-- Links to same items (Side-links)
   /
{D:3} (Conditional Pattern Base)

3. Recursive Mining:
   - For each item in Header Table (bottom-up):
     - Extract Conditional Pattern Bases (Path to root).
     - Construct Conditional FP-Tree.
     - Generate Frequent Patterns.
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
Apriori 알고리즘과의 핵심 차이점을 비교합니다.

| 비교 항목 | Apriori 알고리즘 | FP-Growth 알고리즘 |
| :--- | :--- | :--- |
| **기본 원리** | Candidate 생성 및 반복 스캔 | FP-Tree 압축 및 재귀적 마이닝 |
| **DB 스캔 횟수** | 후보 항목 집합의 길이만큼 반복 | **단 2회 (고정)** |
| **메모리 사용** | 후보 조합 폭증 시 기하급수적 증가 | 트리에 데이터를 압축하여 상대적 효율적 |
| **데이터 크기** | 소규모 데이터셋에 적합 | **대규모/복잡한 데이터셋**에 강점 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
1. **실시간 추천 시스템**: 이커머스 로그 분석 시 짧은 시간 내에 연관 상품을 추출해야 하는 서빙 환경에서 주로 사용됩니다.
2. **침입 탐지 시스템 (IDS)**: 네트워크 패킷 로그에서 빈번하게 발생하는 공격 패턴을 실시간으로 탐지하는 보안 분야에 적용됩니다.
3. **기술사적 판단**: FP-Growth는 성능 면에서 압도적이지만, FP-Tree가 메모리에 모두 로드되어야 한다는 전제가 있습니다. 데이터가 너무 거대하여 메모리를 초과할 경우 분산 환경(Apache Spark MLlib의 PFP 등)에서의 처리를 고려해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
FP-Growth는 연관 규칙 마이닝의 표준 알고리즘으로 자리 잡았습니다. 단순한 통계적 빈발 추출을 넘어, 최근에는 시퀀셜 패턴(Sequential Pattern) 마이닝과 결합하여 사용자의 다음 행동을 예측하는 고도화된 분석의 근간이 되고 있습니다. 데이터 압축과 분할 정복이라는 알고리즘적 미학이 빅데이터 실무에 가장 잘 구현된 사례입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 연관 규칙 학습, 빈발 항목 마이닝(Frequent Itemset Mining)
- **비교 개념**: Apriori, Eclat 알고리즘
- **관련 기술**: Apache Spark MLlib (FPGrowth), dbt

### 👶 어린이를 위한 3줄 비유 설명
1. 마트 영수증이 100만 장 있는데, 같이 많이 팔린 물건을 찾으려면 영수증을 계속 뒤져야 해서 힘들어요.
2. FP-Growth는 이 영수증들을 지도처럼 한 장의 그림(트리)으로 꽉 압축해서 그려놓는 마법이에요.
3. 이 지도만 보면 영수증을 다시 안 뒤져도 어떤 물건들이 단짝인지 금방 찾아낼 수 있답니다.
