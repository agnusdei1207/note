+++
title = "분할 정복 (Divide and Conquer): 재귀적 문제 해결의 마스터 패턴"
date = "2026-03-04"
[extra]
categories = "studynotes-algorithm-stats"
+++

# 분할 정복 (Divide and Conquer): 재귀적 문제 해결의 마스터 패턴

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분할 정복은 문제를 **더 작은 독립적 부분 문제로 분할(Divide)**하고, 각각을 재귀적으로 해결(Conquer)한 후, 결과를 **병합(Combine)**하여 원래 문제의 해를 구하는 알고리즘 설계 패러다임입니다.
> 2. **가치**: $T(n) = aT(n/b) + f(n)$ 형태의 점화식으로 표현되며, 마스터 정리를 통해 $O(n \log n)$ 또는 $O(n^d)$의 체계적 복잡도 분석이 가능합니다.
> 3. **융합**: 병렬 컴퓨팅(MapReduce), 캐시 최적 알고리즘, FFT 신호 처리 등 현대 컴퓨팅의 핵심 기술의 기반이 됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 분할 정복의 정의와 3단계 구조

분할 정복(Divide and Conquer)은 로마 제국의 군사 전략 "Divide et Impera(나누고 정복하라)"에서 유래한 알고리즘 설계 기법입니다.

**3단계 구조**:
1. **분할 (Divide)**: 문제를 동일한 구조의 더 작은 부분 문제들로 나눕니다.
2. **정복 (Conquer)**: 부분 문제들을 재귀적으로 해결합니다. (기저 사례 도달 시 직접 해결)
3. **병합 (Combine)**: 부분 문제의 해를 합쳐 원래 문제의 해를 구성합니다.

**일반적 점화식**:
$$T(n) = \underbrace{a}_{\text{부분문제 개수}} \cdot T\left(\underbrace{\frac{n}{b}}_{\text{부분문제 크기}}\right) + \underbrace{f(n)}_{\text{분할+병합 비용}}$$

#### 💡 비유: 백화점 축소 공사
거대한 백화점을 1층씩으로 나누어(Divide), 각 층을 별도 팀이 재귀적으로 철거합니다(Conquer). 마지막으로 각 층의 철거 결과를 취합하여 전체 철거 완료 보고를 합니다(Combine). 1층(기저 사례)은 바로 철거합니다.

#### 2. 등장 배경 및 발전 과정
1. **고전적 예시**: 유클리드 호제법(기원전 300년), 이진 탐색(1946)이 초기 형태입니다.
2. **현대적 정립**: Cooley-Tukey FFT(1965), 퀵 정렬(Hoare, 1961) 등이 체계적 패턴으로 발전했습니다.
3. **병렬화와 만남**: MapReduce, CUDA 등 분산/병렬 컴퓨팅의 이론적 기반이 되었습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 분할 정복 알고리즘 분류표

| 알고리즘 | 분할 방식 | 부분문제 수(a) | 크기 감소(b) | 병합 비용 | 전체 복잡도 |
|:---:|:---|:---:|:---:|:---:|:---:|
| **이진 탐색** | 반으로 분할 | 1 | 2 | $O(1)$ | $O(\log n)$ |
| **퀵 정렬** | 피벗 기준 분할 | 2 | ~2 | $O(n)$ | $O(n \log n)$ |
| **합병 정렬** | 반으로 분할 | 2 | 2 | $O(n)$ | $O(n \log n)$ |
| **Strassen** | 7개 부분행렬 | 7 | 2 | $O(n^2)$ | $O(n^{2.81})$ |
| **Karatsuba** | 3개 부분곱 | 3 | 2 | $O(n)$ | $O(n^{1.585})$ |
| **FFT** | 짝수/홀수 분리 | 2 | 2 | $O(n)$ | $O(n \log n)$ |

#### 2. 분할 정복 구조 다이어그램 (ASCII)

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                 DIVIDE AND CONQUER EXECUTION FLOW                       │
  └─────────────────────────────────────────────────────────────────────────┘

                          ┌───────────────────┐
                          │   Problem(n)      │
                          │   Input Size: n   │
                          └─────────┬─────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │    DIVIDE     │               │
                    │  (Split into  │               │
                    │   subproblems)│               │
                    ▼               ▼               ▼
            ┌───────────┐   ┌───────────┐   ┌───────────┐
            │ SubProb 1 │   │ SubProb 2 │   │ SubProb a │
            │  Size:n/b │   │  Size:n/b │   │  Size:n/b │
            └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
                  │               │               │
         ┌────────┴───────┬───────┴───────┬───────┴────────┐
         │                │   CONQUER     │                │
         │                │ (Recursive    │                │
         │                │  Solution)    │                │
         ▼                ▼               ▼                ▼
    ┌─────────┐      ┌─────────┐     ┌─────────┐     ┌─────────┐
    │Base Case│      │Base Case│     │  ...    │     │Base Case│
    │  n ≤ c  │      │  n ≤ c  │     │         │     │  n ≤ c  │
    └────┬────┘      └────┬────┘     └────┬────┘     └────┬────┘
         │                │               │                │
         │    ┌───────────┴───────────────┴───────────┐    │
         │    │           COMBINE                      │    │
         │    │   (Merge subproblem solutions)        │    │
         │    └───────────────────┬───────────────────┘    │
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  ▼
                          ┌───────────────┐
                          │ Final Solution│
                          │    O(f(n))    │
                          └───────────────┘

  ═══════════════════════════════════════════════════════════════════════════
  MERGE SORT EXAMPLE (a=2, b=2, f(n)=O(n))
  ═══════════════════════════════════════════════════════════════════════════

                      [38, 27, 43, 3, 9, 82, 10]
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
            [38, 27, 43, 3]             [9, 82, 10]
                    │                           │
            ┌───────┴───────┐           ┌───────┴──────┐
            │               │           │              │
        [38, 27]        [43, 3]      [9, 82]        [10]
            │               │           │              │
         ┌──┴──┐         ┌──┴──┐     ┌──┴──┐          │
         │     │         │     │     │     │          │
       [38]  [27]      [43]  [3]   [9]  [82]        [10]
         │     │         │     │     │     │          │
         └──┬──┘         └──┬──┘     └──┬──┘          │
            │               │           │              │
       [27, 38]          [3, 43]    [9, 82]         [10]
            │               │           │              │
            └───────┬───────┘           └──────┬───────┘
                    │                          │
            [3, 27, 38, 43]           [9, 10, 82]
                    │                          │
                    └──────────┬───────────────┘
                               │
                    [3, 9, 10, 27, 38, 43, 82]
```

#### 3. 마스터 정리 (Master Theorem)

분할 정복 알고리즘의 점화식 $T(n) = aT(n/b) + f(n)$에 대한 해:

$$\text{Let } c_{crit} = \log_b a$$

**Case 1**: $f(n) = O(n^{c_{crit} - \epsilon})$ for some $\epsilon > 0$
$$\Rightarrow T(n) = \Theta(n^{c_{crit}}) = \Theta(n^{\log_b a})$$

**Case 2**: $f(n) = \Theta(n^{c_{crit}} \log^k n)$ for some $k \geq 0$
$$\Rightarrow T(n) = \Theta(n^{c_{crit}} \log^{k+1} n)$$

**Case 3**: $f(n) = \Omega(n^{c_{crit} + \epsilon})$ for some $\epsilon > 0$, and $af(n/b) \leq cf(n)$ for some $c < 1$
$$\Rightarrow T(n) = \Theta(f(n))$$

**적용 예시**:

| 점화식 | $a$ | $b$ | $f(n)$ | $c_{crit}$ | Case | $T(n)$ |
|:---|:---:|:---:|:---|:---:|:---:|:---|
| $T(n) = 2T(n/2) + n$ | 2 | 2 | $\Theta(n)$ | 1 | 2 | $\Theta(n \log n)$ |
| $T(n) = 2T(n/2) + 1$ | 2 | 2 | $O(1)$ | 1 | 1 | $\Theta(n)$ |
| $T(n) = 2T(n/2) + n^2$ | 2 | 2 | $\Theta(n^2)$ | 1 | 3 | $\Theta(n^2)$ |
| $T(n) = T(n/2) + 1$ | 1 | 2 | $\Theta(1)$ | 0 | 2 | $\Theta(\log n)$ |
| $T(n) = 3T(n/2) + n$ | 3 | 2 | $\Theta(n)$ | 1.585 | 1 | $\Theta(n^{1.585})$ |

#### 4. 실무 코드 예시: 분할 정복 템플릿과 적용

```python
"""
분할 정복 알고리즘 템플릿 및 대표 구현
"""
from typing import List, Tuple, Any, Callable
import sys
sys.setrecursionlimit(10000)

# ============================================
# 분할 정복 템플릿
# ============================================

def divide_and_conquer_template(
    problem: Any,
    divide: Callable[[Any], List[Any]],
    conquer: Callable[[Any], Any],  # 기저 사례 처리 포함
    combine: Callable[[List[Any]], Any],
    is_base_case: Callable[[Any], bool]
) -> Any:
    """
    분할 정복의 일반적 템플릿

    Args:
        problem: 해결할 문제
        divide: 문제를 부분 문제들로 분할하는 함수
        conquer: 부분 문제를 해결하는 함수 (기저 사례 포함)
        combine: 부분 해를 병합하는 함수
        is_base_case: 기저 사례 판별 함수
    """
    # 기저 사례 (Base Case)
    if is_base_case(problem):
        return conquer(problem)

    # 분할 (Divide)
    subproblems = divide(problem)

    # 정복 (Conquer) - 재귀 호출
    subsolutions = [
        divide_and_conquer_template(
            sub, divide, conquer, combine, is_base_case
        )
        for sub in subproblems
    ]

    # 병합 (Combine)
    return combine(subsolutions)

# ============================================
# 합병 정렬 (Merge Sort)
# ============================================

def merge_sort(arr: List[int]) -> List[int]:
    """
    합병 정렬 - O(n log n)
    T(n) = 2T(n/2) + O(n)
    """
    # 기저 사례
    if len(arr) <= 1:
        return arr

    # 분할
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    # 정복 (재귀)
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)

    # 병합
    return merge(left_sorted, right_sorted)

def merge(left: List[int], right: List[int]) -> List[int]:
    """두 정렬된 리스트 병합 - O(n)"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# ============================================
# 최대 부분 배열 (Maximum Subarray)
# ============================================

def max_subarray(arr: List[int]) -> Tuple[int, int, int]:
    """
    최대 부분 배열 합 - 분할 정복 O(n log n)
    Kadane's algorithm은 O(n)이지만 분할 정복 예시로 구현

    Returns: (시작 인덱스, 끝 인덱스, 최대 합)
    """
    return _max_subarray_helper(arr, 0, len(arr) - 1)

def _max_subarray_helper(
    arr: List[int], low: int, high: int
) -> Tuple[int, int, int]:
    """분할 정복으로 최대 부분 배열 찾기"""
    # 기저 사례
    if low == high:
        return (low, high, arr[low])

    # 분할
    mid = (low + high) // 2

    # 정복 (재귀)
    left_low, left_high, left_sum = _max_subarray_helper(arr, low, mid)
    right_low, right_high, right_sum = _max_subarray_helper(arr, mid + 1, high)
    cross_low, cross_high, cross_sum = _max_crossing_subarray(arr, low, mid, high)

    # 병합 (최댓값 선택)
    if left_sum >= right_sum and left_sum >= cross_sum:
        return (left_low, left_high, left_sum)
    elif right_sum >= left_sum and right_sum >= cross_sum:
        return (right_low, right_high, right_sum)
    else:
        return (cross_low, cross_high, cross_sum)

def _max_crossing_subarray(
    arr: List[int], low: int, mid: int, high: int
) -> Tuple[int, int, int]:
    """중앙을 가로지르는 최대 부분 배열 - O(n)"""
    # 왼쪽 최대
    left_sum = float('-inf')
    sum_val = 0
    max_left = mid
    for i in range(mid, low - 1, -1):
        sum_val += arr[i]
        if sum_val > left_sum:
            left_sum = sum_val
            max_left = i

    # 오른쪽 최대
    right_sum = float('-inf')
    sum_val = 0
    max_right = mid + 1
    for i in range(mid + 1, high + 1):
        sum_val += arr[i]
        if sum_val > right_sum:
            right_sum = sum_val
            max_right = i

    return (max_left, max_right, left_sum + right_sum)

# ============================================
# Karatsuba 곱셈
# ============================================

def karatsuba(x: int, y: int) -> int:
    """
    Karatsuba 곱셈 - O(n^1.585)
    T(n) = 3T(n/2) + O(n)

    x * y를 3번의 재귀 호출로 계산
    """
    # 기저 사례
    if x < 10 or y < 10:
        return x * y

    # 자릿수 계산
    n = max(x.bit_length(), y.bit_length())
    m = n // 2

    # 분할: x = a * 2^m + b, y = c * 2^m + d
    power = 1 << m
    a, b = x // power, x % power
    c, d = y // power, y % power

    # 3번의 재귀 호출
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    # (a+b)(c+d) - ac - bd = ad + bc
    ad_plus_bc = karatsuba(a + b, c + d) - ac - bd

    # 병합: ac * 2^(2m) + (ad+bc) * 2^m + bd
    return (ac << (2 * m)) + (ad_plus_bc << m) + bd

# ============================================
# Strassen 행렬 곱셈
# ============================================

def strassen_matrix_multiply(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """
    Strassen 행렬 곱셈 - O(n^2.807)
    T(n) = 7T(n/2) + O(n^2)
    """
    n = len(A)

    # 기저 사례
    if n <= 64:  # 임계값에서는 일반 곱셈이 더 빠름
        return naive_matrix_multiply(A, B)

    # 2의 거듭제곱으로 패딩 (단순화를 위해 생략)
    mid = n // 2

    # 분할
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]

    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]

    # 7개의 부분곱 (Strassen의 핵심)
    M1 = strassen_matrix_multiply(
        matrix_add(A11, A22), matrix_add(B11, B22))
    M2 = strassen_matrix_multiply(
        matrix_add(A21, A22), B11)
    M3 = strassen_matrix_multiply(
        A11, matrix_sub(B12, B22))
    M4 = strassen_matrix_multiply(
        A22, matrix_sub(B21, B11))
    M5 = strassen_matrix_multiply(
        matrix_add(A11, A12), B22)
    M6 = strassen_matrix_multiply(
        matrix_sub(A21, A11), matrix_add(B11, B12))
    M7 = strassen_matrix_multiply(
        matrix_sub(A12, A22), matrix_add(B21, B22))

    # 병합
    C11 = matrix_add(matrix_sub(matrix_add(M1, M4), M5), M7)
    C12 = matrix_add(M3, M5)
    C21 = matrix_add(M2, M4)
    C22 = matrix_add(matrix_sub(matrix_add(M1, M3), M2), M6)

    # 결과 합치기
    C = [[0] * n for _ in range(n)]
    for i in range(mid):
        for j in range(mid):
            C[i][j] = C11[i][j]
            C[i][j + mid] = C12[i][j]
            C[i + mid][j] = C21[i][j]
            C[i + mid][j + mid] = C22[i][j]

    return C

def matrix_add(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def matrix_sub(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def naive_matrix_multiply(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """기본 행렬 곱셈 - O(n³)"""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

# ============================================
# 테스트
# ============================================

if __name__ == "__main__":
    print("=== 분할 정복 알고리즘 테스트 ===\n")

    # 합병 정렬
    arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"합병 정렬: {arr} → {merge_sort(arr)}")

    # 최대 부분 배열
    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    low, high, total = max_subarray(arr)
    print(f"최대 부분 배열: arr[{low}:{high+1}] = {arr[low:high+1]}, 합 = {total}")

    # Karatsuba
    x, y = 12345, 67890
    print(f"Karatsuba: {x} × {y} = {karatsuba(x, y)} (검증: {x * y})")

    # Strassen
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    print(f"Strassen: {A} × {B} = {strassen_matrix_multiply(A, B)}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 분할 정복 vs 다른 설계 기법

| 특성 | 분할 정복 | 동적 프로그래밍 | 탐욕 알고리즘 |
|:---:|:---|:---|:---|
| **부분문제 독립성** | 필수 (독립적) | 중복 허용 | 없음 |
| **재귀 구조** | 항상 사용 | 선택적 | 드뭄 |
| **병합 단계** | 필수 | 선택적 | 없음 |
| **최적 부분구조** | 필요 | 필요 | 필요 |
| **대표 예시** | 합병정렬, FFT | 피보나치, LCS | 크루스칼, 다익스트라 |

#### 2. 과목 융합 관점

- **병렬 컴퓨팅**: 분할 정복은 자연스럽게 병렬화됩니다. MapReduce의 Map이 분할, Reduce가 병합에 해당합니다.
- **캐시 최적화**: 캐시 크기에 맞춘 분할로 Cache-Oblivious 알고리즘을 설계할 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오

**시나리오: 대용량 이미지 처리**
- **문제**: 10GB 위성 이미지에서 특정 패턴 검색
- **전략**: 이미지를 타일로 분할, 각 타일을 독립적으로 처리, 결과 병합

#### 2. 분할 정복 적용 체크리스트
- [ ] 부분 문제가 독립적인가?
- [ ] 기저 사례가 명확한가?
- [ ] 병합 비용이 분할 이득을 초과하지 않는가?
- [ ] 재귀 깊이 제한을 고려했는가?

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 구분 | 효과 |
|:---:|:---|
| **정량적** | O(n²) → O(n log n) 개선 |
| **정성적** | 병렬화 용이, 모듈화된 설계 |

#### 2. 미래 전망
- **양자 분할 정복**: Quantum Fourier Transform (QFT) 등 양자 알고리즘의 기본 패턴

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [재귀 (Recursion)](./recursion.md): 분할 정복의 구현 수단.
- [마스터 정리 (Master Theorem)](./master_theorem.md): 복잡도 분석 도구.
- [동적 프로그래밍](./dynamic_programming.md): 중복 부분문제 처리 기법.
- [합병 정렬](./01_sorting/merge_sort.md): 분할 정복의 대표 사례.
- [퀵 정렬](./01_sorting/quick_sort.md): 제자리 분할 정복.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 분할 정복은 **"큰 숙제를 작은 숙제들로 나눠서 하는 방법"**이에요.
2. 작은 숙제들을 각각 끝낸 다음, 결과를 모아서 큰 숙제를 완성해요.
3. 여러 친구가 동시에 작은 숙제를 할 수 있어서 **협동으로 더 빨리 끝낼 수 있어요**!
