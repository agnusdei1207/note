+++
title = "확률 분포 (Probability Distributions)"
date = 2025-03-02

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 확률 분포 (Probability Distributions)

## 핵심 인사이트 (3줄 요약)
> **확률변수가 가질 수 있는 값과 그 확률의 대응 관계**. 이산형(PMF) vs 연속형(PDF). 정규분포가 통계의 핵심.

---

### Ⅰ. 개요

**개념**: 확률 분포(Probability Distribution)는 **확률변수가 취할 수 있는 모든 값과 그에 대응하는 확률 간의 관계를 나타내는 함수**다.

> 💡 **비유**: "학생들 키 분포" - 우리 반 학생 30명의 키를 재서 그래프로 그려보면, 160cm~170cm 구간에 가장 많은 학생이 있고, 아주 작거나 큰 학생은 드물어요. 이런 "어떤 값이 얼마나 자주 나오는지"를 보여주는 게 확률 분포예요.

**등장 배경** (3가지 이상 기술):

1. **기존 문제점**: 개별 데이터만으로는 패턴을 파악하기 어려움. "키가 165cm일 확률이 얼마야?" 같은 질문에 답할 수 없음
2. **기술적 필요성**: 데이터의 생성 메커니즘을 이해하고, 미래 관측값을 예측하며, 통계적 추론을 수행하기 위한 수학적 기반 필요
3. **산업적 요구**: 품질 관리(정규분포), 고객 서비스 대기시간(지수분포), 결함 수(포아송분포) 등 다양한 현상 모델링 필요

**핵심 목적**: 데이터의 분포 패턴을 파악하여 확률 계산, 예측, 통계적 추론의 기반을 제공하는 것.

---

### Ⅱ. 구성 요소 및 핵심 원리

**구성 요소** (4개 이상):

| 구성 요소 | 영어 | 역할/기능 | 비유 |
|----------|------|----------|------|
| 확률변수 X | Random Variable | 결과를 수치로 매핑 | 주사위 눈 = {1,2,3,4,5,6} |
| PMF/PDF | Mass/Density | 각 값의 확률/밀도 | P(X=1) = 1/6 |
| CDF | Cumulative | 누적 분포 함수 | P(X ≤ 3) = 0.5 |
| 기댓값 μ | Expectation | 분포의 중심 | 평균과 유사 |
| 분산 σ² | Variance | 퍼짐 정도 | 데이터의 산포 |

**확률 분포 분류**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    확률 분포 분류                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📊 이산형 분포 (Discrete):                                     │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • 확률변수가 셀 수 있는 값 (정수 등)                      │ │
│  │  • 확률질량함수 PMF: P(X = x)                              │ │
│  │  • Σ P(X = xᵢ) = 1                                        │ │
│  │  예: 주사위, 동전, 결함 수                                 │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  📈 연속형 분포 (Continuous):                                   │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • 확률변수가 연속적인 값 (실수 범위)                      │ │
│  │  • 확률밀도함수 PDF: f(x)                                  │ │
│  │  • ∫f(x)dx = 1  (면적이 1)                                │ │
│  │  • P(X = x) = 0 (점 확률은 0)                             │ │
│  │  예: 키, 몸무게, 온도, 시간                                │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  🔑 핵심 특성값:                                                │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • 기댓값 (Mean): E[X] = μ                                │ │
│  │  • 분산 (Variance): Var(X) = E[(X-μ)²] = σ²              │ │
│  │  • 표준편차: σ = √Var(X)                                  │ │
│  │  • 왜도 (Skewness): 분포의 비대칭 정도                    │ │
│  │  • 첨도 (Kurtosis): 분포의 뾰족함                         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**주요 이산 분포**:

| 분포 | 조건/용도 | PMF | 기댓값 | 분산 |
|-----|----------|-----|--------|------|
| 베르누이 | 1회 시행 성공/실패 | P(X=k) = p^k(1-p)^(1-k) | p | p(1-p) |
| 이항 | n회 시행 중 k회 성공 | P(X=k) = C(n,k)p^k(1-p)^(n-k) | np | np(1-p) |
| 포아송 | 단위시간/공간 사건 수 | P(X=k) = λ^k·e^(-λ)/k! | λ | λ |
| 기하 | 첫 성공까지 시행 횟수 | P(X=k) = (1-p)^(k-1)·p | 1/p | (1-p)/p² |
| 초기하 | 비복원 추출 | P(X=k) = C(K,k)C(N-K,n-k)/C(N,n) | nK/N | 복잡함 |

**주요 연속 분포**:

| 분포 | 용도 | PDF | 기댓값 | 분산 |
|-----|------|-----|--------|------|
| 정규(Normal) | 자연현상, 중심극한정리 | (1/σ√2π)e^(-(x-μ)²/2σ²) | μ | σ² |
| 표준정규 | 정규분포 표준화 | (1/√2π)e^(-z²/2) | 0 | 1 |
| 지수(Exponential) | 대기시간, 수명 | λe^(-λx) (x≥0) | 1/λ | 1/λ² |
| 균등(Uniform) | 범위 내 동등 확률 | 1/(b-a) (a≤x≤b) | (a+b)/2 | (b-a)²/12 |
| t-분포 | 소표본 추론 | 복잡함 | 0 (ν>1) | ν/(ν-2) (ν>2) |
| 카이제곱 | 분산 추정, 적합도 | 복잡함 | ν | 2ν |
| F-분포 | 분산비교, ANOVA | 복잡함 | d₂/(d₂-2) | 복잡함 |

**정규 분포 핵심 특성**:

```
┌─────────────────────────────────────────────────────────────────┐
│                  정규 분포 (Normal Distribution)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   f(x) = (1/σ√2π) × e^(-(x-μ)²/2σ²)                            │
│                                                                 │
│   ┌─────────────────────────────────────────────────────┐      │
│   │              종 모양 곡선                           │      │
│   │                    *                                │      │
│   │                 *     *                             │      │
│   │               *         *                           │      │
│   │             *             *                         │      │
│   │           *                 *                       │      │
│   │         *                     *                     │      │
│   │   _____*_______________________*_____               │      │
│   │        -3σ -2σ -1σ μ +1σ +2σ +3σ                   │      │
│   └─────────────────────────────────────────────────────┘      │
│                                                                 │
│   68-95-99.7 규칙 (경험 법칙):                                  │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  μ ± 1σ: 68.27%의 데이터                                │  │
│   │  μ ± 2σ: 95.45%의 데이터                                │  │
│   │  μ ± 3σ: 99.73%의 데이터                                │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   표준화: Z = (X - μ) / σ  →  Z ~ N(0, 1)                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**동작 원리** (단계별 상세 설명):

```
① 데이터분석 → ② 분포가정 → ③ 모수추정 → ④ 적합도검정 → ⑤ 확률계산/예측
```

- **1단계**: 히스토그램, Q-Q plot 등으로 데이터 분포 형태 파악
- **2단계**: 데이터 특성에 맞는 분포 모형 선택 (정규, 포아송, 지수 등)
- **3단계**: 표본 데이터로 모수(μ, σ, λ 등)를 추정 (MLE, 모멘트법)
- **4단계**: 적합도 검정(χ², K-S, Shapiro-Wilk)으로 분포 가정 검증
- **5단계**: 선택된 분포로 확률 계산, 신뢰구간, 예측 수행

**코드 예시** (Python):

```python
from typing import List, Tuple, Optional
import math

class DiscreteDistributions:
    """이산형 확률 분포"""

    @staticmethod
    def factorial(n: int) -> int:
        """팩토리얼"""
        if n <= 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def combination(n: int, k: int) -> int:
        """조합 C(n,k)"""
        if k > n or k < 0:
            return 0
        return DiscreteDistributions.factorial(n) // (
            DiscreteDistributions.factorial(k) * DiscreteDistributions.factorial(n - k)
        )

    @staticmethod
    def bernoulli_pmf(k: int, p: float) -> float:
        """베르누이 분포 PMF: P(X=k) = p^k × (1-p)^(1-k)"""
        if k not in [0, 1]:
            return 0.0
        return (p ** k) * ((1 - p) ** (1 - k))

    @staticmethod
    def binomial_pmf(k: int, n: int, p: float) -> float:
        """이항 분포 PMF: P(X=k) = C(n,k) × p^k × (1-p)^(n-k)"""
        if k < 0 or k > n:
            return 0.0
        c = DiscreteDistributions.combination(n, k)
        return c * (p ** k) * ((1 - p) ** (n - k))

    @staticmethod
    def poisson_pmf(k: int, lambda_: float) -> float:
        """포아송 분포 PMF: P(X=k) = λ^k × e^(-λ) / k!"""
        if k < 0:
            return 0.0
        return (lambda_ ** k) * math.exp(-lambda_) / DiscreteDistributions.factorial(k)

    @staticmethod
    def geometric_pmf(k: int, p: float) -> float:
        """기하 분포 PMF: P(X=k) = (1-p)^(k-1) × p"""
        if k < 1:
            return 0.0
        return ((1 - p) ** (k - 1)) * p


class ContinuousDistributions:
    """연속형 확률 분포"""

    @staticmethod
    def normal_pdf(x: float, mu: float, sigma: float) -> float:
        """정규 분포 PDF: f(x) = (1/σ√2π) × e^(-(x-μ)²/2σ²)"""
        coef = 1 / (sigma * math.sqrt(2 * math.pi))
        exponent = -((x - mu) ** 2) / (2 * sigma ** 2)
        return coef * math.exp(exponent)

    @staticmethod
    def normal_cdf(x: float, mu: float, sigma: float) -> float:
        """정규 분포 CDF (근사)"""
        # 표준화 후 근사
        z = (x - mu) / sigma
        return ContinuousDistributions._standard_normal_cdf(z)

    @staticmethod
    def _standard_normal_cdf(z: float) -> float:
        """표준정규분포 CDF 근사 (Abramowitz & Stegun)"""
        a1, a2, a3, a4, a5 = 0.319381530, -0.356563782, 1.781477937, -1.821255978, 1.330274429
        k = 1 / (1 + 0.2316419 * abs(z))
        cdf = 1 - (1/math.sqrt(2*math.pi)) * math.exp(-z**2/2) * (a1*k + a2*k**2 + a3*k**3 + a4*k**4 + a5*k**5)
        return cdf if z >= 0 else 1 - cdf

    @staticmethod
    def exponential_pdf(x: float, lambda_: float) -> float:
        """지수 분포 PDF: f(x) = λ × e^(-λx) (x≥0)"""
        if x < 0:
            return 0.0
        return lambda_ * math.exp(-lambda_ * x)

    @staticmethod
    def exponential_cdf(x: float, lambda_: float) -> float:
        """지수 분포 CDF: F(x) = 1 - e^(-λx)"""
        if x < 0:
            return 0.0
        return 1 - math.exp(-lambda_ * x)

    @staticmethod
    def uniform_pdf(x: float, a: float, b: float) -> float:
        """균등 분포 PDF: f(x) = 1/(b-a) (a≤x≤b)"""
        if a <= x <= b:
            return 1 / (b - a)
        return 0.0

    @staticmethod
    def uniform_cdf(x: float, a: float, b: float) -> float:
        """균등 분포 CDF"""
        if x < a:
            return 0.0
        elif x > b:
            return 1.0
        else:
            return (x - a) / (b - a)


class DistributionStatistics:
    """분포의 통계량"""

    @staticmethod
    def binomial_stats(n: int, p: float) -> Tuple[float, float]:
        """이항 분포: E[X] = np, Var(X) = np(1-p)"""
        mean = n * p
        variance = n * p * (1 - p)
        return mean, variance

    @staticmethod
    def poisson_stats(lambda_: float) -> Tuple[float, float]:
        """포아송 분포: E[X] = λ, Var(X) = λ"""
        return lambda_, lambda_

    @staticmethod
    def normal_stats(mu: float, sigma: float) -> Tuple[float, float]:
        """정규 분포: E[X] = μ, Var(X) = σ²"""
        return mu, sigma ** 2

    @staticmethod
    def exponential_stats(lambda_: float) -> Tuple[float, float]:
        """지수 분포: E[X] = 1/λ, Var(X) = 1/λ²"""
        mean = 1 / lambda_
        variance = 1 / (lambda_ ** 2)
        return mean, variance


class ProbabilityCalculator:
    """확률 계산 유틸리티"""

    @staticmethod
    def normal_probability_between(a: float, b: float, mu: float, sigma: float) -> float:
        """P(a < X < b) for normal distribution"""
        return (ContinuousDistributions.normal_cdf(b, mu, sigma) -
                ContinuousDistributions.normal_cdf(a, mu, sigma))

    @staticmethod
    def normal_probability_above(x: float, mu: float, sigma: float) -> float:
        """P(X > x) for normal distribution"""
        return 1 - ContinuousDistributions.normal_cdf(x, mu, sigma)

    @staticmethod
    def normal_probability_below(x: float, mu: float, sigma: float) -> float:
        """P(X < x) for normal distribution"""
        return ContinuousDistributions.normal_cdf(x, mu, sigma)

    @staticmethod
    def empirical_rule(mu: float, sigma: float) -> dict:
        """68-95-99.7 규칙"""
        return {
            "68%": (mu - sigma, mu + sigma),
            "95%": (mu - 2*sigma, mu + 2*sigma),
            "99.7%": (mu - 3*sigma, mu + 3*sigma)
        }


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("확률 분포 예시")
    print("=" * 60)

    # 1. 이항 분포
    print("\n1. 이항 분포 - 동전 10번 던지기")
    n, p = 10, 0.5
    print(f"n={n}, p={p}")
    for k in range(11):
        prob = DiscreteDistributions.binomial_pmf(k, n, p)
        print(f"  P(X={k}) = {prob:.4f} {'*' * int(prob * 20)}")
    mean, var = DistributionStatistics.binomial_stats(n, p)
    print(f"  E[X] = {mean}, Var(X) = {var}")

    # 2. 포아송 분포
    print("\n2. 포아송 분포 - 시간당 평균 3건의 사고")
    lambda_ = 3
    print(f"λ = {lambda_}")
    for k in range(8):
        prob = DiscreteDistributions.poisson_pmf(k, lambda_)
        print(f"  P(X={k}) = {prob:.4f}")
    mean, var = DistributionStatistics.poisson_stats(lambda_)
    print(f"  E[X] = {mean}, Var(X) = {var}")

    # 3. 정규 분포
    print("\n3. 정규 분포 - IQ 점수 (μ=100, σ=15)")
    mu, sigma = 100, 15
    print(f"μ = {mu}, σ = {sigma}")

    # PDF 값
    for x in [70, 85, 100, 115, 130]:
        pdf = ContinuousDistributions.normal_pdf(x, mu, sigma)
        print(f"  f({x}) = {pdf:.6f}")

    # 확률 계산
    print("\n  확률 계산:")
    print(f"  P(X < 85) = {ProbabilityCalculator.normal_probability_below(85, mu, sigma):.4f}")
    print(f"  P(X > 115) = {ProbabilityCalculator.normal_probability_above(115, mu, sigma):.4f}")
    print(f"  P(85 < X < 115) = {ProbabilityCalculator.normal_probability_between(85, 115, mu, sigma):.4f}")

    # 경험 법칙
    print("\n  68-95-99.7 규칙:")
    rule = ProbabilityCalculator.empirical_rule(mu, sigma)
    for pct, (low, high) in rule.items():
        print(f"    {pct}의 데이터: [{low:.1f}, {high:.1f}]")

    # 4. 지수 분포
    print("\n4. 지수 분포 - 평균 10분 대기시간")
    lambda_exp = 0.1  # 1/10
    print(f"λ = {lambda_exp} (평균 1/λ = {1/lambda_exp}분)")
    print(f"  P(대기 < 5분) = {ContinuousDistributions.exponential_cdf(5, lambda_exp):.4f}")
    print(f"  P(대기 < 10분) = {ContinuousDistributions.exponential_cdf(10, lambda_exp):.4f}")
    print(f"  P(대기 < 20분) = {ContinuousDistributions.exponential_cdf(20, lambda_exp):.4f}")
    mean, var = DistributionStatistics.exponential_stats(lambda_exp)
    print(f"  E[X] = {mean:.1f}분, Var(X) = {var:.1f}")
