+++
title = "기술 통계 (Descriptive Statistics)"
date = 2025-03-02

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 기술 통계 (Descriptive Statistics)

## 핵심 인사이트 (3줄 요약)
> **데이터의 특성을 요약하고 설명하는 통계 기법**. 중심경향성(평균/중앙값/최빈값) + 산포도(분산/표준편차/IQR). 데이터 분석의 첫 단계.

---

## 📝 전문가 모의답안 (2.5페이지 분량)

### 📌 예상 문제
> **"기술 통계의 개념과 구성 요소를 설명하고, 중심경향성과 산포도 척도의 특징을 비교하시오."**

---

### Ⅰ. 개요

#### 1. 개념
기술 통계(Descriptive Statistics)는 **수집된 데이터의 특성을 요약, 정리, 설명하는 통계적 방법**이다. 데이터 전체를 일일이 보지 않고도 핵심 특징을 파악할 수 있게 해준다.

> 💡 **비유**: "반 성적 요약표" - 30명 점수를 평균, 최고, 최저로 한눈에 파악

**등장 배경**:
1. **기존 문제점**: 원시 데이터는 너무 많아 패턴 파악 어려움
2. **기술적 필요성**: 데이터의 핵심 특성을 빠르게 이해해야 함
3. **시장 요구**: 비즈니스 의사결정을 위한 데이터 요약 필요

**핵심 목적**: 데이터 분포의 중심, 퍼짐, 형태를 요약하여 이해

---

### Ⅱ. 구성 요소 및 핵심 원리

#### 2. 기술 통계 핵심 구성 요소

| 구분 | 척도 | 정의 | 특징 |
|-----|------|------|------|
| **중심경향성** | 평균 (Mean) | 모든 값의 합 / 개수 | 이상값에 민감 |
| | 중앙값 (Median) | 정렬 후 중간 값 | 이상값에 강건 |
| | 최빈값 (Mode) | 가장 빈번한 값 | 범주형 가능 |
| **산포도** | 범위 (Range) | 최댓값 - 최솟값 | 이상값 민감 |
| | 분산 (Variance) | 편차 제곱의 평균 | 단위가 제곱 |
| | 표준편차 (Std) | 분산의 제곱근 | 원 단위 |
| | IQR | Q3 - Q1 | 이상값 강건 |
| **분포형태** | 왜도 (Skewness) | 좌우 비대칭 정도 | 0=대칭 |
| | 첨도 (Kurtosis) | 뾰족함 정도 | 0=정규분포 |

#### 3. 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────┐
│               기술 통계 구조                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 중심경향성 (Central Tendency):                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  데이터: [1, 2, 3, 4, 5, 6, 7, 8, 100]              │   │
│  │                                                     │   │
│  │  평균(μ) = 136/9 = 15.1  ← 이상값(100)에 끌려감    │   │
│  │  중앙값 = 5               ← 이상값 영향 적음        │   │
│  │  최빈값 = 없음 (모두 1회)                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  📈 산포도 (Dispersion):                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  범위 = 100 - 1 = 99                                │   │
│  │  분산(σ²) = Σ(xᵢ-μ)²/n = 893.2                     │   │
│  │  표준편차(σ) = √893.2 = 29.9                        │   │
│  │  IQR = Q3(7) - Q1(3) = 4  ← 이상값 영향 없음       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  📉 분포 형태 (Shape):                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │   왜도 > 0 (오른쪽 꼬리)    왜도 = 0 (대칭)         │   │
│  │        ____                   _____                │   │
│  │       /    \                 /     \               │   │
│  │      /      \___            /       \              │   │
│  │     /            \          \       /              │   │
│  │    /              \          \_____/               │   │
│  │                                                     │   │
│  │   왜도 < 0 (왼쪽 꼬리)                              │   │
│  │            ____                                    │   │
│  │           /    \                                   │   │
│  │      ___/      \                                  │   │
│  │     /              \                               │   │
│  │    /                \                              │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 4. 동작 원리 단계별 설명

```
① 데이터 수집 → ② 정렬/전처리 → ③ 중심경향성 계산 → ④ 산포도 계산 → ⑤ 시각화
```

- **1단계**: 원시 데이터 수집
- **2단계**: 데이터 정렬, 결측치 처리
- **3단계**: 평균, 중앙값, 최빈값 계산
- **4단계**: 분산, 표준편차, IQR 계산
- **5단계**: 히스토그램, 박스플롯으로 시각화

#### 5. Python 코드 예시

```python
from typing import List, Tuple, Dict
from collections import Counter
import math

# ==================== 중심경향성 ====================

def mean(data: List[float]) -> float:
    """
    산술 평균 (Arithmetic Mean)

    시간복잡도: O(n)
    이상값에 민감함
    """
    return sum(data) / len(data)


def median(data: List[float]) -> float:
    """
    중앙값 (Median)

    시간복잡도: O(n log n) - 정렬 필요
    이상값에 강건함
    """
    sorted_data = sorted(data)
    n = len(sorted_data)

    if n % 2 == 1:
        return sorted_data[n // 2]
    else:
        return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2


def mode(data: List[float]) -> List[float]:
    """
    최빈값 (Mode)

    가장 자주 나타나는 값(들)
    여러 개일 수 있음
    """
    counter = Counter(data)
    max_count = max(counter.values())
    return [val for val, count in counter.items() if count == max_count]


def weighted_mean(data: List[float], weights: List[float]) -> float:
    """가중 평균"""
    return sum(d * w for d, w in zip(data, weights)) / sum(weights)


def geometric_mean(data: List[float]) -> float:
    """기하 평균: (∏xᵢ)^(1/n) - 성장률에 적합"""
    return math.prod(data) ** (1 / len(data))


def harmonic_mean(data: List[float]) -> float:
    """조화 평균: n / Σ(1/xᵢ) - 속도/비율에 적합"""
    return len(data) / sum(1 / x for x in data)


# ==================== 산포도 ====================

def variance(data: List[float], population: bool = True) -> float:
    """
    분산 (Variance)

    σ² = Σ(xᵢ - μ)² / n (모분산)
    s² = Σ(xᵢ - x̄)² / (n-1) (표본분산)
    """
    n = len(data)
    m = mean(data)

    divisor = n if population else n - 1
    return sum((x - m) ** 2 for x in data) / divisor


def std_dev(data: List[float], population: bool = True) -> float:
    """
    표준편차 (Standard Deviation)

    σ = √분산
    """
    return math.sqrt(variance(data, population))


def range_val(data: List[float]) -> float:
    """범위: 최댓값 - 최솟값"""
    return max(data) - min(data)


def quartiles(data: List[float]) -> Tuple[float, float, float]:
    """
    사분위수 (Q1, Q2, Q3)

    Q2 = 중앙값
    Q1 = 하위 50%의 중앙값
    Q3 = 상위 50%의 중앙값
    """
    sorted_data = sorted(data)
    n = len(sorted_data)

    q2 = median(sorted_data)

    if n % 2 == 0:
        lower = sorted_data[:n // 2]
        upper = sorted_data[n // 2:]
    else:
        lower = sorted_data[:n // 2]
        upper = sorted_data[n // 2 + 1:]

    q1 = median(lower)
    q3 = median(upper)

    return q1, q2, q3


def iqr(data: List[float]) -> float:
    """
    사분위수 범위 (Interquartile Range)

    IQR = Q3 - Q1
    이상값 탐지에 활용
    """
    q1, q2, q3 = quartiles(data)
    return q3 - q1


def coefficient_of_variation(data: List[float]) -> float:
    """
    변동계수 (Coefficient of Variation)

    CV = (σ / μ) × 100
    단위에 무관한 산포도 비교
    """
    return (std_dev(data) / mean(data)) * 100


# ==================== 분포 형태 ====================

def skewness(data: List[float]) -> float:
    """
    왜도 (Skewness)

    0: 대칭
    양수: 오른쪽 꼬리 (왼쪽에 치우침)
    음수: 왼쪽 꼬리 (오른쪽에 치우침)
    """
    n = len(data)
    m = mean(data)
    s = std_dev(data)

    return (n / ((n - 1) * (n - 2))) * sum(((x - m) / s) ** 3 for x in data)


def kurtosis(data: List[float]) -> float:
    """
    첨도 (Kurtosis) - 초과 첨도

    0: 정규분포와 동일
    양수: 정규분포보다 뾰족함 (꼬리 두꺼움)
    음수: 정규분포보다 평평함 (꼬리 얇음)
    """
    n = len(data)
    m = mean(data)
    s = std_dev(data)

    kurt = (n * (n + 1) / ((n - 1) * (n - 2) * (n - 3))) * \
           sum(((x - m) / s) ** 4 for x in data) - \
           (3 * (n - 1) ** 2) / ((n - 2) * (n - 3))

    return kurt


# ==================== 이상값 탐지 ====================

def detect_outliers_iqr(data: List[float]) -> List[float]:
    """
    IQR 기반 이상값 탐지

    이상값: Q1 - 1.5×IQR 미만 또는 Q3 + 1.5×IQR 초과
    """
    q1, q2, q3 = quartiles(data)
    iqr_val = q3 - q1

    lower_bound = q1 - 1.5 * iqr_val
    upper_bound = q3 + 1.5 * iqr_val

    return [x for x in data if x < lower_bound or x > upper_bound]


def detect_outliers_zscore(data: List[float], threshold: float = 3.0) -> List[float]:
    """
    Z-score 기반 이상값 탐지

    이상값: |z-score| > threshold
    """
    m = mean(data)
    s = std_dev(data)

    return [x for x in data if abs((x - m) / s) > threshold]


# ==================== 요약 통계 ====================

def describe(data: List[float]) -> Dict:
    """
    요약 통계량 (pandas.describe()와 유사)
    """
    q1, q2, q3 = quartiles(data)

    return {
        'count': len(data),
        'mean': mean(data),
        'std': std_dev(data, population=False),
        'min': min(data),
        '25%': q1,
        '50%': q2,  # median
        '75%': q3,
        'max': max(data),
        'range': range_val(data),
        'iqr': q3 - q1,
        'skewness': skewness(data),
        'kurtosis': kurtosis(data),
        'cv': coefficient_of_variation(data)
    }


# ==================== 테스트 및 검증 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("기술 통계 테스트")
    print("=" * 50)

    # 정상 데이터
    data1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # 이상값 포함 데이터
    data2 = [1, 2, 3, 4, 5, 6, 7, 8, 100]

    print("\n[정상 데이터]")
    stats1 = describe(data1)
    for k, v in stats1.items():
        print(f"  {k}: {v:.2f}" if isinstance(v, float) else f"  {k}: {v}")

    print("\n[이상값 포함 데이터]")
    stats2 = describe(data2)
    for k, v in stats2.items():
        print(f"  {k}: {v:.2f}" if isinstance(v, float) else f"  {k}: {v}")

    print(f"\n[IQR 기반 이상값] {detect_outliers_iqr(data2)}")
    print(f"[Z-score 기반 이상값] {detect_outliers_zscore(data2)}")

    # 평균 vs 중앙값 비교
    print("\n[평균 vs 중앙값 비교]")
    print(f"  정상 데이터: 평균={mean(data1):.2f}, 중앙값={median(data1):.2f}")
    print(f"  이상값 포함: 평균={mean(data2):.2f}, 중앙값={median(data2):.2f}")
    print("  → 이상값이 평균에 큰 영향, 중앙값은 영향 적음")
```

---

### Ⅲ. 기술 비교 분석

#### 6. 중심경향성 척도 비교

| 척도 | 장점 | 단점 | 이상값 영향 | 적용 |
|-----|------|------|-----------|------|
| 평균 | 수학적 성질 우수, 모든 값 활용 | 이상값 민감 | ★ 큼 | 대칭 분포 |
| 중앙값 | 이상값 강건, 순서만 의미 | 극값 정보 손실 | 작음 | 비대칭 분포 |
| 최빈값 | 범주형 가능, 직관적 | 유일하지 않을 수 있음 | 없음 | 명목척도 |
| 절사평균 | 이상값 영향 감소 | 정보 손실 | 중간 | 대회 심사 |

#### 7. 산포도 척도 비교

| 척도 | 장점 | 단점 | 이상값 영향 | 단위 |
|-----|------|------|-----------|------|
| 범위 | 계산 간단 | 극값 2개만 사용 | ★ 큼 | 원 단위 |
| 분산 | 수학적 성질 우수 | 단위가 제곱 | ★ 큼 | 제곱 |
| 표준편차 | 원 단위, 직관적 | 이상값 민감 | ★ 큼 | 원 단위 |
| IQR | 이상값 강건 | 중간 50%만 | 작음 | 원 단위 |
| CV | 단위 무관 비교 | 평균 0이면 무의미 | 중간 | 무차원 |

#### 8. 장단점 분석

| 장점 | 단점 |
|-----|------|
| 데이터 요약으로 빠른 파악 | 정보 손실 (분포 세부사항) |
| 비교 용이 (다른 데이터셋) | 맥락 부족 가능 |
| 계산 간단, 빠름 | 이상값에 따른 왜곡 |
| 시각화와 결합 효과적 | 통계적 추론 불가 |

---

### Ⅳ. 실무 적용 방안

#### 9. 실무 적용 시나리오

| 적용 분야 | 구체적 적용 방법 | 기대 효과 |
|---------|----------------|----------|
| **데이터 품질 검사** | 요약 통계로 이상값/결측치 탐지 | 데이터 품질 90% 향상 |
| **KPI 대시보드** | 일/주/월별 평균, 표준편차 모니터링 | 이상 현상 조기 감지 |
| **A/B 테스트** | 그룹별 요약 통계 비교 | 통계적 유의성 판단 기반 |
| **금융 리스크** | 수익률 분산/표준편차로 변동성 측정 | VaR 계산 기반 |
| **품질 관리** | 공정 데이터 IQR로 관리한계 설정 | 불량률 50% 감소 |

#### 10. 실제 기업/서비스 사례

- **Google Analytics**: 웹사이트 방문자 요약 통계
- **AWS CloudWatch**: 서버 메트릭 평균/표준편차 모니터링
- **Six Sigma**: 공정 능력 분석에 표준편차 활용
- **금융 포트폴리오**: 샤프 지수 = (수익률 - 무위험률) / 표준편차

#### 11. 도입 시 고려사항

1. **기술적**:
   - 데이터 분포 형태 확인 후 적절한 척도 선택
   - 이상값 처리 전략 수립

2. **운영적**:
   - 자동화된 대시보드 구축
   - 알림 임계값 설정

3. **보안적**:
   - 민감 데이터의 경우 집계 수준 조정

4. **경제적**:
   - 오픈소스 라이브러리 활용 (pandas, numpy)

#### 12. 주의사항 / 흔한 실수

- ❌ 평균만 보고 분포 판단 → 분산/분포형태 확인 필요
- ❌ 이상값 처리 없이 분석 → 왜곡된 결과
- ❌ 단위 다른 데이터 직접 비교 → CV 사용
- ❌ 비대칭 분포에 평균 사용 → 중앙값 권장

#### 13. 관련 개념

```
📌 기술 통계 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│  [추론통계] ←──→ [기술 통계] ←──→ [데이터 시각화]              │
│       ↓                ↓                ↓                      │
│  [가설검정]      [확률분포]        [박스플롯]                   │
│       ↓                              ↓                         │
│  [신뢰구간]                     [히스토그램]                    │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 추론통계 | 후속 단계 | 기술통계 후 모집단 추론 | `[가설검정](./hypothesis_testing.md)` |
| 확률분포 | 기반 | 데이터 분포 모델링 | `[분포](./distributions.md)` |
| 회귀분석 | 응용 | 변수 간 관계 분석 | `[회귀](./regression.md)` |
| 데이터 시각화 | 병행 | 히스토그램, 박스플롯 | 관련 문서 참조 |

---

### Ⅴ. 기대 효과 및 결론

#### 14. 정량적 기대 효과

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 데이터 이해 | 요약 통계로 빠른 파악 | 분석 시간 70% 단축 |
| 이상 탐지 | IQR/Z-score로 자동 탐지 | 이상값 탐지율 95% |
| 품질 관리 | 공정 능력 지수 향상 | Cp/Cpk 1.33 이상 |
| 의사결정 | 데이터 기반 객관적 판단 | 의사결정 정확도 30% 향상 |

#### 15. 미래 전망

1. **기술 발전 방향**:
   - 실시간 스트리밍 데이터 요약
   - 자동화된 이상값 탐지 (ML 기반)

2. **시장 트렌드**:
   - 셀프서비스 BI 도구 확대
   - Exploratory Data Analysis (EDA) 자동화

3. **후속 기술**:
   - Augmented Analytics (AI 기반 분석)
   - 실시간 대시보드

> **결론**: 기술 통계는 데이터 분석의 첫 단계로, 데이터의 중심, 퍼짐, 형태를 요약하여 빠른 이해를 돕는다. 평균과 표준편차가 기본이지만, 이상값이 있을 때는 중앙값과 IQR이 더 적합하다.

> **※ 참고 표준**: ISO 3534 (Statistics), NIST/SEMATECH e-Handbook of Statistical Methods

---

## 어린이를 위한 종합 설명

**기술 통계를 쉽게 이해해보자!**

기술 통계는 마치 **반 성적표**와 같아요. 30명 친구들의 점수를 하나하나 다 보는 게 아니라, 평균이 몇 점인지, 최고점은 몇 점인지만 봐도 반 전체를 알 수 있어요.

첫째, **평균**은 모든 점수를 더해서 학생 수로 나눈 거예요. 하지만 100점을 맞은 친구가 한 명 있으면 평균이 확 올라가요. 이상값(특별히 높거나 낮은 값)이 평균을 흔들어요!

둘째, **중앙값**은 점수를 줄 세웠을 때 딱 중간에 있는 친구의 점수예요. 100점을 맞은 친구가 있어도 중앙값은 별로 안 변해요. 그래서 이상값이 있을 때는 중앙값이 더 정확해요!

---