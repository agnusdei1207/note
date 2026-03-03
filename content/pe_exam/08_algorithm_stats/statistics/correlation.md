+++
title = "상관분석 (Correlation Analysis)"
date = 2025-03-02

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 상관분석 (Correlation Analysis)

## 핵심 인사이트 (3줄 요약)
> **두 변수 간 관계의 강도와 방향을 -1~+1로 측정**. 피어슨(선형), 스피어만(순위). 상관≠인과.

---

### Ⅰ. 개요

**개념**: 상관분석(Correlation Analysis)은 **두 변수 간의 선형적 관계의 강도와 방향을 정량적으로 측정하는 통계 기법**이다.

> 💡 **비유**: "키와 몸무게의 관계" - 키가 큰 사람이 보통 몸무게도 많이 나가요. 이런 "같이 증가하는 경향"이 얼마나 강한지를 -1에서 +1 사이 숫자로 나타내는 게 상관계수예요.

**등장 배경** (3가지 이상 기술):

1. **기존 문제점**: 두 변수 사이의 관계를 눈으로만 보면 오해하기 쉬움. 산점도가 복잡할 때 관계의 강도를 정확히 파악 어려움
2. **기술적 필요성**: 변수 선택, 다중공선성 진단, 회귀분석 전 전처리 등에서 정량적 관계 측정 도구 필요
3. **산업적 요구**: 마케팅 효과 측정, 금융 리스크 분석(포트폴리오 상관관계), 의학 연구(위험요인-질병 관계) 등

**핵심 목적**: 변수 간 연관성을 정량화하여 데이터 이해를 높이고, 적절한 분석 방법 선택을 돕는 것.

---

### Ⅱ. 구성 요소 및 핵심 원리

**구성 요소** (4개 이상):

| 구성 요소 | 영어 | 역할/기능 | 비유 |
|----------|------|----------|------|
| 공분산 | Covariance | 두 변수의 공동 변동 | 관계의 "방향" |
| 상관계수 r | Correlation Coefficient | 관계의 강도 (-1~+1) | 관계의 "크기" |
| 결정계수 R² | R-squared | 설명력 (0~1) | 예측 정확도 |
| 산점도 | Scatter Plot | 시각적 관계 표현 | 눈으로 보는 관계 |

**상관계수 종류 비교**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    상관계수 종류                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📊 피어슨 상관계수 (Pearson r):                                │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  r = Σ(xᵢ-x̄)(yᵢ-ȳ) / √[Σ(xᵢ-x̄)² × Σ(yᵢ-ȳ)²]            │ │
│  │                                                           │ │
│  │  • 연속형 변수, 선형 관계 측정                            │ │
│  │  • 정규성 가정 필요                                       │ │
│  │  • 이상치에 민감                                          │ │
│  │  • 가장 널리 사용                                         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  📈 스피어만 순위상관 (Spearman ρ):                              │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  ρ = 1 - (6 × Σdᵢ²) / (n(n²-1))                          │ │
│  │  (dᵢ = 순위 차이)                                        │ │
│  │                                                           │ │
│  │  • 순위형 데이터                                          │ │
│  │  • 비선형 단조 관계도 측정                                │ │
│  │  • 이상치에 강건 (robust)                                 │ │
│  │  • 정규성 가정 불필요                                     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  📉 켄달의 타우 (Kendall's τ):                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  τ = (C - D) / (n(n-1)/2)                                 │ │
│  │  (C: 일치쌍, D: 불일치쌍)                                 │ │
│  │                                                           │ │
│  │  • 순위 일치/불일치 기반                                  │ │
│  │  • 소표본에 적합                                          │ │
│  │  • 동순위(tie) 처리 우수                                  │ │
│  │  • 해석이 직관적                                          │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  🎯 상관계수 해석 기준:                                         │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  |r| ≥ 0.9: 매우 강한 상관                                │ │
│  │  0.7 ≤ |r| < 0.9: 강한 상관                               │ │
│  │  0.5 ≤ |r| < 0.7: 중간 상관                               │ │
│  │  0.3 ≤ |r| < 0.5: 약한 상관                               │ │
│  │  |r| < 0.3: 거의 무상관                                   │ │
│  │                                                           │ │
│  │  r > 0: 양의 상관 (같이 증가)                             │ │
│  │  r < 0: 음의 상관 (반대 방향)                             │ │
│  │  r = 0: 무상관 (선형 관계 없음)                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**공분산과 상관계수 관계**:

```
┌─────────────────────────────────────────────────────────────────┐
│                공분산 → 상관계수 변환                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   공분산: Cov(X,Y) = E[(X-μₓ)(Y-μᵧ)]                           │
│                                                                 │
│           Σ(xᵢ-x̄)(yᵢ-ȳ)                                       │
│         = ───────────────  (표본 공분산)                       │
│                n-1                                              │
│                                                                 │
│   상관계수: r = Cov(X,Y) / (σₓ × σᵧ)                           │
│                                                                 │
│              Σ(xᵢ-x̄)(yᵢ-ȳ)                                     │
│         = ────────────────────────────                         │
│           √[Σ(xᵢ-x̄)²] × √[Σ(yᵢ-ȳ)²]                          │
│                                                                 │
│   특징:                                                         │
│   • 공분산은 단위에 의존 (크기 무한)                            │
│   • 상관계수는 -1~1로 표준화                                    │
│   • r² = R² (결정계수)                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**동작 원리** (단계별 상세 설명):

```
① 데이터수집 → ② 산점도확인 → ③ 상관계수계산 → ④ 유의성검정 → ⑤ 결과해석
```

- **1단계**: 두 변수의 쌍을 이루는 데이터를 수집. 결측치, 이상치 처리
- **2단계**: 산점도를 그려 선형성, 이상치, 패턴을 시각적으로 확인
- **3단계**: 데이터 특성에 맞는 상관계수 선택 후 계산
- **4단계**: t-검정으로 상관계수의 통계적 유의성 확인
- **5단계**: 상관계수 크기와 방향을 해석. 인과관계 아님 주의

**코드 예시** (Python):

```python
from typing import List, Tuple
import math

class CorrelationAnalysis:
    """상관분석 구현"""

    @staticmethod
    def mean(data: List[float]) -> float:
        """평균 계산"""
        return sum(data) / len(data)

    @staticmethod
    def std(data: List[float]) -> float:
        """표준편차 계산"""
        m = CorrelationAnalysis.mean(data)
        variance = sum((x - m) ** 2 for x in data) / (len(data) - 1)
        return math.sqrt(variance)

    @staticmethod
    def covariance(x: List[float], y: List[float]) -> float:
        """공분산 계산: Cov(X,Y) = Σ(xᵢ-x̄)(yᵢ-ȳ) / (n-1)"""
        if len(x) != len(y):
            raise ValueError("두 리스트 길이가 같아야 합니다")

        n = len(x)
        mean_x = CorrelationAnalysis.mean(x)
        mean_y = CorrelationAnalysis.mean(y)

        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / (n - 1)
        return cov

    @staticmethod
    def pearson_correlation(x: List[float], y: List[float]) -> float:
        """
        피어슨 상관계수 계산
        r = Σ(xᵢ-x̄)(yᵢ-ȳ) / √[Σ(xᵢ-x̄)² × Σ(yᵢ-ȳ)²]
        """
        if len(x) != len(y):
            raise ValueError("두 리스트 길이가 같아야 합니다")

        n = len(x)
        mean_x = CorrelationAnalysis.mean(x)
        mean_y = CorrelationAnalysis.mean(y)

        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(
            sum((xi - mean_x) ** 2 for xi in x) *
            sum((yi - mean_y) ** 2 for yi in y)
        )

        if denominator == 0:
            return 0.0

        return numerator / denominator

    @staticmethod
    def r_squared(x: List[float], y: List[float]) -> float:
        """결정계수 R² = r²"""
        r = CorrelationAnalysis.pearson_correlation(x, y)
        return r ** 2

    @staticmethod
    def correlation_test(r: float, n: int, alpha: float = 0.05) -> dict:
        """
        상관계수 유의성 검정 (t-검정)
        H₀: ρ = 0 (상관없음)
        H₁: ρ ≠ 0 (상관있음)
        """
        if n <= 2:
            return {"reject_null": False, "p_value": 1.0}

        # t-통계량
        t_stat = r * math.sqrt((n - 2) / (1 - r ** 2)) if abs(r) < 1 else float('inf')

        # p-value 근사 (정규분포로 근사)
        # |t| > 1.96 → p < 0.05 (양측)
        p_value = 2 * (1 - CorrelationAnalysis._normal_cdf(abs(t_stat)))

        # 임계값
        t_crit = 1.96 if n > 30 else 2.0  # 근사

        return {
            "t_statistic": t_stat,
            "p_value": p_value,
            "reject_null": abs(t_stat) > t_crit,
            "alpha": alpha
        }

    @staticmethod
    def _normal_cdf(z: float) -> float:
        """표준정규분포 CDF 근사"""
        a1, a2, a3, a4, a5 = 0.319381530, -0.356563782, 1.781477937, -1.821255978, 1.330274429
        k = 1 / (1 + 0.2316419 * abs(z))
        cdf = 1 - (1/math.sqrt(2*math.pi)) * math.exp(-z**2/2) * (a1*k + a2*k**2 + a3*k**3 + a4*k**4 + a5*k**5)
        return cdf if z >= 0 else 1 - cdf


class SpearmanCorrelation:
    """스피어만 순위상관계수"""

    @staticmethod
    def rank(data: List[float]) -> List[float]:
        """순위 부여 (동순위는 평균 순위)"""
        sorted_indices = sorted(range(len(data)), key=lambda i: data[i])
        ranks = [0.0] * len(data)

        i = 0
        while i < len(data):
            j = i
            # 동순위 찾기
            while j < len(data) - 1 and data[sorted_indices[j]] == data[sorted_indices[j + 1]]:
                j += 1
            # 평균 순위 부여
            avg_rank = (i + j) / 2 + 1  # 1부터 시작
            for k in range(i, j + 1):
                ranks[sorted_indices[k]] = avg_rank
            i = j + 1

        return ranks

    @staticmethod
    def spearman_correlation(x: List[float], y: List[float]) -> float:
        """
        스피어만 순위상관계수
        ρ = 1 - (6 × Σdᵢ²) / (n(n²-1))
        """
        if len(x) != len(y):
            raise ValueError("두 리스트 길이가 같아야 합니다")

        n = len(x)
        rank_x = SpearmanCorrelation.rank(x)
        rank_y = SpearmanCorrelation.rank(y)

        # 순위 차이 제곱합
        d_squared = sum((rx - ry) ** 2 for rx, ry in zip(rank_x, rank_y))

        # 스피어만 공식
        rho = 1 - (6 * d_squared) / (n * (n ** 2 - 1))
        return rho


class KendallCorrelation:
    """켄달의 타우"""

    @staticmethod
    def kendall_tau(x: List[float], y: List[float]) -> float:
        """
        켄달의 타우
        τ = (C - D) / (n(n-1)/2)
        C: 일치쌍 (concordant), D: 불일치쌍 (discordant)
        """
        if len(x) != len(y):
            raise ValueError("두 리스트 길이가 같아야 합니다")

        n = len(x)
        concordant = 0
        discordant = 0

        for i in range(n):
            for j in range(i + 1, n):
                x_diff = x[i] - x[j]
                y_diff = y[i] - y[j]

                if x_diff * y_diff > 0:  # 같은 방향
                    concordant += 1
                elif x_diff * y_diff < 0:  # 반대 방향
                    discordant += 1
                # x_diff * y_diff == 0: 동점 (tie), 제외

        total_pairs = n * (n - 1) / 2
        if total_pairs == 0:
            return 0.0

        tau = (concordant - discordant) / total_pairs
        return tau


class CorrelationMatrix:
    """상관행렬 계산"""

    @staticmethod
    def compute(data: List[List[float]]) -> List[List[float]]:
        """
        여러 변수 간 상관행렬 계산
        data: [[x1, x2, ...], [y1, y2, ...], ...]
        return: 상관행렬 (n_variables × n_variables)
        """
        n_vars = len(data)
        matrix = [[0.0] * n_vars for _ in range(n_vars)]

        for i in range(n_vars):
            for j in range(n_vars):
                if i == j:
                    matrix[i][j] = 1.0
                else:
                    matrix[i][j] = CorrelationAnalysis.pearson_correlation(data[i], data[j])

        return matrix

    @staticmethod
    def print_matrix(matrix: List[List[float]], labels: List[str] = None) -> str:
        """상관행렬 출력"""
        n = len(matrix)
        if labels is None:
            labels = [f"Var{i+1}" for i in range(n)]

        # 헤더
        header = "        " + "  ".join(f"{l:>8}" for l in labels)
        lines = [header, "-" * len(header)]

        # 행
        for i, row in enumerate(matrix):
            row_str = f"{labels[i]:>8}" + "  ".join(f"{v:>8.3f}" for v in row)
            lines.append(row_str)

        return "\n".join(lines)


def interpret_correlation(r: float) -> str:
    """상관계수 해석"""
    abs_r = abs(r)
    direction = "양의" if r > 0 else "음의" if r < 0 else ""

    if abs_r >= 0.9:
        strength = "매우 강한"
    elif abs_r >= 0.7:
        strength = "강한"
    elif abs_r >= 0.5:
        strength = "중간"
    elif abs_r >= 0.3:
        strength = "약한"
    else:
        strength = "거의 없는"
        direction = ""

    if r == 0:
        return "무상관 (선형 관계 없음)"
    return f"{direction} {strength} 상관관계"


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("상관분석 예시")
    print("=" * 60)

    # 예제 데이터: 키와 몸무게
    height = [150, 155, 160, 165, 170, 175, 180, 185, 190, 195]
    weight = [45, 50, 55, 60, 68, 72, 78, 85, 90, 95]

    # 1. 공분산과 상관계수
    print("\n1. 기본 통계량")
    print(f"키 평균: {CorrelationAnalysis.mean(height):.1f}cm")
    print(f"몸무게 평균: {CorrelationAnalysis.mean(weight):.1f}kg")
    print(f"공분산: {CorrelationAnalysis.covariance(height, weight):.2f}")

    r = CorrelationAnalysis.pearson_correlation(height, weight)
    print(f"피어슨 상관계수: r = {r:.4f}")
    print(f"해석: {interpret_correlation(r)}")
    print(f"결정계수: R² = {CorrelationAnalysis.r_squared(height, weight):.4f}")

    # 2. 유의성 검정
    print("\n2. 상관계수 유의성 검정")
    test_result = CorrelationAnalysis.correlation_test(r, len(height))
    print(f"t-통계량: {test_result['t_statistic']:.4f}")
    print(f"p-value: {test_result['p_value']:.6f}")
    print(f"결론: {'통계적으로 유의미함' if test_result['reject_null'] else '유의미하지 않음'}")

    # 3. 스피어만 상관계수
    print("\n3. 스피어만 순위상관계수")
    rho = SpearmanCorrelation.spearman_correlation(height, weight)
    print(f"ρ = {rho:.4f}")

    # 4. 켄달 타우
    print("\n4. 켄달의 타우")
    tau = KendallCorrelation.kendall_tau(height, weight)
    print(f"τ = {tau:.4f}")

    # 5. 상관행렬
    print("\n5. 상관행렬 (3변수)")
    study_hours = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    scores = [55, 60, 65, 70, 75, 80, 85, 88, 92, 95]

    matrix = CorrelationMatrix.compute([height, weight, study_hours])
    print(CorrelationMatrix.print_matrix(matrix, ["키", "몸무게", "공부시간"]))

    # 6. 주의사항 예시
    print("\n6. 주의: 상관 ≠ 인과")
    print("아이스크림 판매량과 익사 사고의 상관관계가 높을 수 있어요.")
    print("하지만 아이스크림이 익사를 유발하지 않아요!")
    print("→ 두 변수 모두 '더운 날씨'라는 제3의 변수에 영향 받음")
