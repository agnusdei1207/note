+++
weight = 15
title = "타뷸레이션 (Tabulation)"
date = "2024-05-22"
[extra]
categories = "studynote-algorithm"
+++

## 핵심 인사이트 (3줄 요약)
- **Bottom-Up 방식의 DP:** 최소 단위 문제부터 시작하여 상향식으로 테이블을 채워나가는 동적 프로그래밍 기법입니다.
- **반복문 기반 구현:** 재귀 호출 없이 반복문을 사용하므로 스택 오버플로우 위험이 없으며 오버헤드가 적습니다.
- **전체 하위 문제 해결:** 메모이제이션과 달리 모든 하위 문제를 순차적으로 해결하며 테이블 전체를 완성합니다.

### Ⅰ. 개요 (Context & Background)
- **동적 프로그래밍(DP)의 구현체:** 중복되는 부분 문제(Overlapping Subproblems)와 최적 부분 구조(Optimal Substructure)를 가진 문제를 해결하는 핵심 방법론 중 하나입니다.
- **명칭의 유래:** 결과를 'Table'에 기록하며 채워나간다는 의미에서 'Tabulation'이라 불립니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **상향식 접근 (Bottom-Up Approach):** 작은 문제의 해를 먼저 구하고, 이를 이용해 점진적으로 더 큰 문제의 해를 구합니다.
- **점화식(State Transition Equation):** 문제 간의 관계를 수식으로 정의하여 테이블을 갱신하는 논리적 기반이 됩니다.

```text
[Tabulation Process: Fibonacci Example]
+-----------+-----------+-----------+-----------+-----------+
| F(0) = 0  | F(1) = 1  | F(2) = 1  | F(3) = 2  | F(4) = 3  |  <-- Table (Array)
+-----------+-----------+-----------+-----------+-----------+
      |           |           |           |           |
    Step 1      Step 2      Step 3      Step 4      Step 5
  (Base Case) (Base Case)  (F1 + F0)   (F2 + F1)   (F3 + F2)

[Bilingual Flow]
작은 문제 (Small Problem)  --->  중간 문제 (Mid Problem)  --->  전체 문제 (Target Problem)
하향식 의존성 없음 (No recursive overhead) | 루프 기반 (Loop-based)
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Comparison) | 타뷸레이션 (Tabulation) | 메모이제이션 (Memoization) |
|:---:|:---|:---|
| **접근 방식** | 상향식 (Bottom-Up) | 하향식 (Top-Down) |
| **구현 방식** | 반복문 (Iterative Loop) | 재귀 함수 (Recursive Function) |
| **스택 부하** | 없음 (No Stack Overhead) | 있음 (Stack Overflow Risk) |
| **해결 범위** | 모든 하위 문제 해결 | 필요한 하위 문제만 해결 |
| **적용 시기** | 점화식이 명확하고 전체를 채울 때 | 하위 문제의 일부만 필요할 때 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **성능 최적화:** 재귀의 함수 호출 오버헤드를 제거해야 하는 고성능 시스템(임베디드, 실시간 처리)에서 선호됩니다.
- **공간 복잡도 개선:** 이전 단계의 결과만 필요할 경우 Sliding Window 기법을 적용하여 공간 복잡도를 O(1)로 줄일 수 있습니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **예측 가능성:** 실행 흐름이 순차적이므로 디버깅이 용이하고 메모리 사용량이 정적입니다.
- **결론:** 복잡한 알고리즘을 정형화된 반복문으로 치환함으로써 시스템 안정성을 높이는 최적의 DP 구현 기술입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 동적 프로그래밍 (Dynamic Programming)
- **유사 개념:** 메모이제이션 (Memoization), 분할 정복 (Divide and Conquer)
- **하위 개념:** 점화식 (Recurrence Relation), 슬라이딩 윈도우 (Sliding Window)

### 👶 어린이를 위한 3줄 비유 설명
- "계단 오르기랑 비슷해요. 1층부터 차근차근 밟고 올라가서 꼭대기에 도착하는 방법이에요."
- "숙제를 할 때 1번 문제부터 10번 문제까지 순서대로 다 푸는 것과 같아요."
- "미리 작은 답들을 공책(표)에 적어두고, 그걸 보고 큰 답을 계산하는 똑똑한 방법이에요."
