+++
title = "확률 기초 (Probability Basics)"
date = 2025-03-02

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 확률 기초 (Probability Basics)

## 핵심 인사이트 (3줄 요약)
> **불확실성을 0~1 사이 수치로 정량화**. 조건부 확률, 독립/종속, 베이즈 정리가 핵심. 모든 통계/머신러닝의 기초.

---

### Ⅰ. 개요

**개념**: 확률(Probability)은 **어떤 사건이 발생할 가능성을 0과 1 사이의 수치로 나타내는 수학적 체계**다. 0은 불가능, 1은 필수 발생을 의미한다.

> 💡 **비유**: "날씨 예보" - 기상청이 "내일 비 올 확률 70%"라고 하면, 100번 중 70번은 비가 온다는 뜻이에요. 우리는 이 정보로 우산을 챙길지 결정하죠.

**등장 배경** (3가지 이상 기술):

1. **기존 문제점**: 불확실한 상황에서 직관이나 감에만 의존하면 잘못된 의사결정을 하기 쉬움. 도박, 보험, 투자 등에서 체계적 오류 발생
2. **기술적 필요성**: 게임 이론, 통계적 추론, 머신러닝 등에서 불확실성을 수학적으로 다루기 위한 엄밀한 정의 필요
3. **산업적 요구**: 보험료 계산, 리스크 관리, 품질 관리, A/B 테스트 등 다양한 분야에서 확률 기반 의사결정이 필수

**핵심 목적**: 불확실성을 정량화하여 합리적이고 최적의 의사결정을 지원하는 것.

---

### Ⅱ. 구성 요소 및 핵심 원리

**구성 요소** (4개 이상):

| 구성 요소 | 영어 | 역할/기능 | 비유 |
|----------|------|----------|------|
| 표본공간 S | Sample Space | 모든 가능한 결과의 집합 | 주사위 {1,2,3,4,5,6} |
| 사건 E | Event | 표본공간의 부분집합 | 짝수 {2,4,6} |
| 확률 P | Probability | 사건 발생 가능성 (0~1) | P(짝수) = 0.5 |
| 확률변수 X | Random Variable | 결과를 수치로 매핑 | X = 주사위 눈 |

**확률 공리 (Kolmogorov Axioms)**:

```
┌─────────────────────────────────────────────────────────────────┐
│                콜모고로프 확률 공리                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣ 비음수성 (Non-negativity):                                │
│     P(A) ≥ 0  for all A ∈ F                                    │
│     → 모든 사건의 확률은 0 이상                                 │
│                                                                 │
│  2️⃣ 정규화 (Normalization):                                   │
│     P(S) = 1                                                   │
│     → 전체 표본공간의 확률은 1                                  │
│                                                                 │
│  3️⃣ 가산성 (Additivity):                                      │
│     P(A∪B) = P(A) + P(B)  if A∩B = ∅                          │
│     → 서로 배반인 사건들의 합집합 확률은 각각의 합              │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  따름 정리:                                                │ │
│  │  • P(Aᶜ) = 1 - P(A)  (여사건)                             │ │
│  │  • P(A∪B) = P(A) + P(B) - P(A∩B)  (포함-배제 원리)        │ │
│  │  • P(A) ≤ P(B) if A ⊆ B  (단조성)                         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**확률 종류와 계산법**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    확률의 세 가지 정의                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📊 고전적 확률 (Classical):                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  P(E) = 유리한 경우의 수 / 전체 경우의 수                  │ │
│  │  전제: 모든 결과가 동등하게 가능                          │ │
│  │  예: P(주사위 3) = 1/6                                    │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  📈 경험적 확률 (Empirical/Frequentist):                        │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  P(E) = 사건 발생 횟수 / 전체 시행 횟수                    │ │
│  │  전제: 충분히 많은 반복                                   │ │
│  │  예: 1000번 던져 160번 3 → P(3) ≈ 0.16                    │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  🎯 주관적 확률 (Subjective/Bayesian):                          │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  P(E) = 개인의 믿음 정도                                  │ │
│  │  전제: 정보와 경험에 기반                                 │ │
│  │  예: "내일 비 올 확률 70%" (기상학자 판단)                 │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**조건부 확률과 독립**:

| 개념 | 공식 | 의미 |
|-----|------|------|
| 조건부 확률 | P(A\|B) = P(A∩B) / P(B) | B가 주어졌을 때 A의 확률 |
| 독립 사건 | P(A∩B) = P(A) × P(B) | 한 사건이 다른 사건에 영향 없음 |
| 종속 사건 | P(A∩B) ≠ P(A) × P(B) | 사건들이 서로 영향 |
| 곱셈 법칙 | P(A∩B) = P(A) × P(B\|A) | 교집합 확률 계산 |
| 전확률 정리 | P(B) = Σ P(B\|Aᵢ)P(Aᵢ) | 전체 확률 분해 |

**베이즈 정리와 확장**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    베이즈 정리                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│              P(B|A) × P(A)                                      │
│   P(A|B) = ─────────────                                        │
│                 P(B)                                            │
│                                                                 │
│  확장 형태:                                                     │
│              P(B|A) × P(A)                                      │
│   P(A|B) = ──────────────────────                               │
│            Σ P(B|Aᵢ) × P(Aᵢ)                                    │
│                                                                 │
│  응용:                                                          │
│  • 질병 진단: 증상 → 질병 확률                                  │
│  • 스팸 필터: 단어 → 스팸 확률                                  │
│  • 기계 학습: 데이터 → 모델 확률                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**동작 원리** (단계별 상세 설명):

```
① 표본공간정의 → ② 사건정의 → ③ 확률계산 → ④ 조건부/독립판단 → ⑤ 의사결정
```

- **1단계**: 문제 상황에서 가능한 모든 결과(표본공간)를 정의
- **2단계**: 관심 있는 사건(조건)을 명확히 정의
- **3단계**: 고전적/경험적/주관적 방법으로 확률 계산
- **4단계**: 사건 간 독립/종속 관계 파악, 조건부 확률 활용
- **5단계**: 계산된 확률을 바탕으로 최적 의사결정

**코드 예시** (Python):

```python
from typing import List, Set, Dict, Tuple
from fractions import Fraction
import random

class Probability:
    """확률 기초 개념 구현"""

    @staticmethod
    def classical_probability(favorable: int, total: int) -> Fraction:
        """고전적 확률 계산"""
        return Fraction(favorable, total)

    @staticmethod
    def empirical_probability(event_count: int, total_trials: int) -> float:
        """경험적 확률 계산"""
        return event_count / total_trials

    @staticmethod
    def conditional_probability(joint: float, condition: float) -> float:
        """조건부 확률: P(A|B) = P(A∩B) / P(B)"""
        if condition == 0:
            raise ValueError("조건 사건의 확률이 0이면 조건부 확률을 정의할 수 없습니다")
        return joint / condition

    @staticmethod
    def bayes_theorem(prior: float, likelihood: float, evidence: float) -> float:
        """베이즈 정리: P(A|B) = P(B|A) × P(A) / P(B)"""
        if evidence == 0:
            raise ValueError("증거 확률이 0이면 베이즈 정리를 적용할 수 없습니다")
        return (likelihood * prior) / evidence

    @staticmethod
    def independence_test(p_a: float, p_b: float, p_ab: float, tolerance: float = 1e-6) -> bool:
        """독립성 검정: P(A∩B) = P(A) × P(B)이면 독립"""
        return abs(p_ab - p_a * p_b) < tolerance


class DiceExperiment:
    """주사위 실험 - 확률 개념 시뮬레이션"""

    def __init__(self, sides: int = 6):
        self.sides = sides
        self.sample_space = list(range(1, sides + 1))

    def probability(self, event: Set[int]) -> Fraction:
        """사건의 확률 계산"""
        favorable = len([x for x in self.sample_space if x in event])
        return Fraction(favorable, self.sides)

    def simulate(self, trials: int, event: Set[int]) -> float:
        """몬테카를로 시뮬레이션"""
        hits = sum(1 for _ in range(trials) if random.randint(1, self.sides) in event)
        return hits / trials


class ProbabilityCalculator:
    """복합 확률 계산기"""

    @staticmethod
    def union_probability(p_a: float, p_b: float, p_ab: float) -> float:
        """합집합 확률: P(A∪B) = P(A) + P(B) - P(A∩B)"""
        return p_a + p_b - p_ab

    @staticmethod
    def complement_probability(p_a: float) -> float:
        """여사건 확률: P(Aᶜ) = 1 - P(A)"""
        return 1 - p_a

    @staticmethod
    def multiplication_rule(p_a: float, p_b_given_a: float) -> float:
        """곱셈 법칙: P(A∩B) = P(A) × P(B|A)"""
        return p_a * p_b_given_a

    @staticmethod
    def total_probability(conditional_probs: List[Tuple[float, float]]) -> float:
        """
        전확률 정리: P(B) = Σ P(B|Aᵢ) × P(Aᵢ)
        conditional_probs: [(P(B|A₁), P(A₁)), (P(B|A₂), P(A₂)), ...]
        """
        return sum(p_b_given_a * p_a for p_b_given_a, p_a in conditional_probs)


class BinomialExperiment:
    """이항 분포 실험 (n번 시도 중 k번 성공)"""

    @staticmethod
    def factorial(n: int) -> int:
        """팩토리얼 계산"""
        if n <= 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def combination(n: int, k: int) -> int:
        """조합 C(n,k) = n! / (k! × (n-k)!)"""
        if k > n or k < 0:
            return 0
        return BinomialExperiment.factorial(n) // (
            BinomialExperiment.factorial(k) * BinomialExperiment.factorial(n - k)
        )

    @staticmethod
    def probability(n: int, k: int, p: float) -> float:
        """
        이항 확률: P(X=k) = C(n,k) × p^k × (1-p)^(n-k)
        n: 시도 횟수
        k: 성공 횟수
        p: 성공 확률
        """
        c = BinomialExperiment.combination(n, k)
        return c * (p ** k) * ((1 - p) ** (n - k))

    @staticmethod
    def expected_value(n: int, p: float) -> float:
        """기댓값: E[X] = np"""
        return n * p

    @staticmethod
    def variance(n: int, p: float) -> float:
        """분산: Var(X) = np(1-p)"""
        return n * p * (1 - p)


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("확률 기초 예시")
    print("=" * 60)

    # 1. 고전적 확률
    print("\n1. 고전적 확률 - 주사위")
    dice = DiceExperiment(sides=6)
    even_event = {2, 4, 6}
    print(f"P(짝수) = {dice.probability(even_event)}")
    print(f"P(3 이상) = {dice.probability({3, 4, 5, 6})}")

    # 2. 경험적 확률 (시뮬레이션)
    print("\n2. 경험적 확률 - 10000번 시뮬레이션")
    empirical = dice.simulate(10000, even_event)
    print(f"시뮬레이션 P(짝수) ≈ {empirical:.4f} (이론값: 0.5)")

    # 3. 조건부 확률
    print("\n3. 조건부 확률")
    # 예: 카드 뽑기에서 하트를 뽑을 확률
    # P(하트) = 13/52 = 0.25
    # P(그림카드) = 12/52 = 0.231
    # P(하트∩그림카드) = 3/52 = 0.058
    # P(그림카드|하트) = 3/13 ≈ 0.231
    p_heart = 13/52
    p_face = 12/52
    p_heart_and_face = 3/52
    p_face_given_heart = Probability.conditional_probability(p_heart_and_face, p_heart)
    print(f"P(그림카드|하트) = {p_face_given_heat:.4f}")

    # 4. 독립성 검정
    print("\n4. 독립성 검정")
    # 주사위 두 번 던지기: 두 결과는 독립
    p_first_6 = 1/6
    p_second_6 = 1/6
    p_both_6 = 1/36
    is_independent = Probability.independence_test(p_first_6, p_second_6, p_both_6)
    print(f"주사위 두 번: P(첫6)={p_first_6:.4f}, P(둘6)={p_second_6:.4f}, P(둘다6)={p_both_6:.4f}")
    print(f"독립인가? {is_independent}")

    # 5. 베이즈 정리
    print("\n5. 베이즈 정리 - 질병 진단")
    p_disease = 0.01  # 유병률 1%
    p_positive_given_disease = 0.95  # 민감도
    p_positive_given_healthy = 0.05  # 위양성률

    # 전확률 정리로 P(양성) 계산
    p_positive = ProbabilityCalculator.total_probability([
        (p_positive_given_disease, p_disease),
        (p_positive_given_healthy, 1 - p_disease)
    ])
    print(f"P(양성) = {p_positive:.4f}")

    # 베이즈 정리로 P(질병|양성) 계산
    p_disease_given_positive = Probability.bayes_theorem(
        p_disease, p_positive_given_disease, p_positive
    )
    print(f"P(질병|양성) = {p_disease_given_positive:.4f} ({p_disease_given_positive:.1%})")

    # 6. 이항 분포
    print("\n6. 이항 분포 - 동전 10번 던지기")
    n, p = 10, 0.5
    print(f"동전 10번 던져 정확히 5번 앞면: P = {BinomialExperiment.probability(n, 5, p):.4f}")
    print(f"기댓값: E[X] = {BinomialExperiment.expected_value(n, p)}")
    print(f"분산: Var(X) = {BinomialExperiment.variance(n, p):.2f}")
