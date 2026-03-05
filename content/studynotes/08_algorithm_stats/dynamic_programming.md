+++
title = "동적 프로그래밍 (Dynamic Programming): 중복 계산의 제거와 최적화의 예술"
date = "2026-03-04"
[extra]
categories = "studynotes-algorithm-stats"
+++

# 동적 프로그래밍 (Dynamic Programming): 중복 계산의 제거와 최적화의 예술

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 동적 프로그래밍은 **최적 부분구조(Optimal Substructure)**와 **중복 부분문제(Overlapping Subproblems)**를 가진 문제에서, 부분문제의 해를 저장하고 재사용함으로써 지수 시간을 다항 시간으로 단축하는 알고리즘 설계 기법입니다.
> 2. **가치**: 피보나치 수열 $O(2^n) \rightarrow O(n)$, 배낭 문제 $O(2^n) \rightarrow O(nW)$, 행렬 사슬 곱셈 $O(n!) \rightarrow O(n^3)$ 등의 극적인 성능 개선을 제공합니다.
> 3. **융합**: AI/ML의 강화학습, 생물정보학의 서열 정렬, 금융의 포트폴리오 최적화, 자연어 처리의 Viterbi 알고리즘 등 광범위하게 활용됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 동적 프로그래밍의 정의와 핵심 조건

동적 프로그래밍(Dynamic Programming, DP)은 1950년대 리처드 벨만(Richard Bellman)이 개발한 최적화 기법으로, 복잡한 문제를 더 간단한 부분 문제로 나누어 해결합니다.

**DP 적용을 위한 두 가지 핵심 조건**:

**① 최적 부분구조 (Optimal Substructure)**
- 문제의 최적해가 부분문제의 최적해로 구성됨
- 예: 최단 경로 A→C의 최적해가 A→B 최적 + B→C 최적

**② 중복 부분문제 (Overlapping Subproblems)**
- 동일한 부분문제가 여러 번 반복해서 등장
- 예: fib(5) = fib(4) + fib(3)에서 fib(3), fib(2) 등이 중복 호출

**DP vs 분할 정복 비교**:
- **분할 정복**: 부분문제가 독립적 (중복 없음)
- **동적 프로그래밍**: 부분문제가 중복됨 (저장 재사용)

#### 💡 비유: 수학 숙제를 노트에 적어두기
피보나치 수열을 계산한다고 가정해 봅시다. 순진한 재귀는 매번 앞의 값을 다시 계산합니다. "fib(100)을 구하려면 fib(99)와 fib(98)이 필요한데..." 매번 처음부터 계산하면 평생 걸립니다. DP는 **"계산한 값을 노트에 적어두고 다음에 바로 찾아쓰는 것"**입니다. fib(1)=1, fib(2)=1, fib(3)=2, ... 순서대로 적어두면 fib(100)도 순식간에 구합니다.

#### 2. 등장 배경 및 발전 과정
1. **벨만의 창안**: 1953년 "동적 프로그래밍" 용어 처음 사용. "Dynamic"은 시간 변화를, "Programming"은 최적화 계획을 의미.
2. **고전적 응용**: 1960~70년대 배낭 문제, 행렬 사슬 곱셈, LCS 등이 정립.
3. **현대적 확장**: 바이오인포매틱스(서열 정렬), NLP(Viterbi), AI(강화학습)로 확장.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. DP 접근법 분류

| 접근법 | 설명 | 구현 방식 | 메모리 | 대표 예시 |
|:---:|:---|:---|:---:|:---|
| **Top-Down (메모이제이션)** | 큰 문제 → 작은 문제, 필요시 재귀 호출 | 재귀 + 캐시 | $O(n)$ | 피보나치, 그래프 DP |
| **Bottom-Up (타뷸레이션)** | 작은 문제 → 큰 문제, 순차적 계산 | 반복문 + 테이블 | $O(n)$ | 배낭, LCS, 거리 |
| **공간 최적화** | 직전 상태만 유지 | 슬라이딩 윈도우 | $O(1)$ | 피보나치, 1차원 DP |

#### 2. DP 문제 해결 프로세스 다이어그램 (ASCII)

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │              DYNAMIC PROGRAMMING PROBLEM-SOLVING PIPELINE               │
  └─────────────────────────────────────────────────────────────────────────┘

                          ┌───────────────────┐
                          │   1. 문제 분석     │
                          │  - 최적 부분구조?  │
                          │  - 중복 부분문제?  │
                          └─────────┬─────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
            ┌───────────────┐               ┌───────────────┐
            │     Yes       │               │      No       │
            │   DP 적용     │               │ 다른 기법 탐색 │
            └───────┬───────┘               └───────────────┘
                    │
                    ▼
            ┌───────────────────────────────────────────────┐
            │           2. 상태 정의 (State Definition)       │
            │   DP[i] = i번째까지의 최적해                   │
            │   DP[i][j] = i~j 구간의 최적해                 │
            │   DP[i][w] = i번째까지 용량 w에서의 최적해     │
            └───────────────────────┬───────────────────────┘
                                    │
                    ▼
            ┌───────────────────────────────────────────────┐
            │          3. 점화식 도출 (Recurrence)           │
            │                                                │
            │   DP[i] = f(DP[i-1], DP[i-2], ...)             │
            │                                                │
            │   - Base Case: DP[0], DP[1] 초기화             │
            │   - Transition: 이전 상태 → 현재 상태          │
            └───────────────────────┬───────────────────────┘
                                    │
                    ▼
            ┌───────────────────────────────────────────────┐
            │          4. 구현 방식 선택                      │
            │                                                │
            │   ┌─────────────┐    ┌─────────────┐          │
            │   │  Top-Down   │ or │ Bottom-Up   │          │
            │   │ (Memoization)│    │(Tabulation) │          │
            │   └──────┬──────┘    └──────┬──────┘          │
            │          │                  │                  │
            │          └────────┬─────────┘                  │
            │                   ▼                            │
            │   ┌─────────────────────────────────┐          │
            │   │     Space Optimization?         │          │
            │   │     (O(n) → O(1))               │          │
            │   └─────────────────────────────────┘          │
            └───────────────────────┬───────────────────────┘
                                    │
                    ▼
            ┌───────────────────────────────────────────────┐
            │          5. 정답 도출                          │
            │   - DP[n] 또는 max(DP[:]) 반환                │
            │   - 경로 추적이 필요한 경우 별도 처리         │
            └───────────────────────────────────────────────┘

  ═══════════════════════════════════════════════════════════════════════════
  FIBONACCI DP EXAMPLE
  ═══════════════════════════════════════════════════════════════════════════

  순진한 재귀 (O(2^n)):           메모이제이션 (O(n)):

         fib(5)                        fib(5) ← 1번만 계산
        /      \                         |
     fib(4)   fib(3)                   fib(4) + fib(3) ← 캐시에서 조회
     /    \    /    \                     |
  fib(3) fib(2) fib(2) fib(1)          fib(3) + fib(2)
   /    \       ↑                       /    \
fib(2) fib(1)  중복!               fib(2) + fib(1) ← 캐시
  /    \
fib(1) fib(0)

  중복 호출: fib(3)×2, fib(2)×3, fib(1)×5    각 fib(i)는 1번만 계산

  Bottom-Up 테이블:
  ┌─────┬─────┬─────┬─────┬─────┬─────┐
  │  0  │  1  │  2  │  3  │  4  │  5  │
  ├─────┼─────┼─────┼─────┼─────┼─────┤
  │  0  │  1  │  1  │  2  │  3  │  5  │
  └─────┴─────┴─────┴─────┴─────┴─────┘
    ↑     ↑     ↑     ↑     ↑     ↑
   기저  기저  f(0)+f(1) f(1)+f(2) ...
```

#### 3. 대표적 DP 문제와 점화식

| 문제 | 상태 정의 | 점화식 | 시간 | 공간 |
|:---|:---|:---|:---:|:---:|
| **피보나치** | $DP[i]$ = $i$번째 피보나치 | $DP[i] = DP[i-1] + DP[i-2]$ | $O(n)$ | $O(1)^*$ |
| **계단 오르기** | $DP[i]$ = $i$번째 계단까지의 방법 수 | $DP[i] = DP[i-1] + DP[i-2]$ | $O(n)$ | $O(1)$ |
| **LCS** | $DP[i][j]$ = $A[0:i]$, $B[0:j]$의 LCS | 매칭 시 $DP[i-1][j-1]+1$ | $O(mn)$ | $O(mn)$ |
| **0/1 배낭** | $DP[i][w]$ = $i$번째까지, 용량 $w$ | $\max(DP[i-1][w], DP[i-1][w-w_i]+v_i)$ | $O(nW)$ | $O(nW)$ |
| **편집 거리** | $DP[i][j]$ = $A[0:i]$, $B[0:j]$ 거리 | $\min(삽입, 삭제, 교체) + 1$ | $O(mn)$ | $O(mn)$ |
| **LIS** | $DP[i]$ = $i$번째로 끝나는 LIS 길이 | $DP[i] = \max(DP[j]+1)$ for $j < i, arr[j] < arr[i]$ | $O(n^2)$ | $O(n)$ |
| **행렬 사슬** | $DP[i][j]$ = $i$~$j$ 행렬 곱 최소 비용 | $\min(DP[i][k] + DP[k+1][j] + cost)$ | $O(n^3)$ | $O(n^2)$ |

#### 4. 실무 코드 예시: 대표적 DP 구현

```python
"""
동적 프로그래밍 대표 구현 모음
"""
from typing import List, Tuple, Optional
from functools import lru_cache
import sys

# ============================================
# 1. 피보나치 - 세 가지 방식 비교
# ============================================

def fib_naive(n: int) -> int:
    """순진한 재귀 - O(2^n)"""
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

def fib_memo(n: int, memo: dict = None) -> int:
    """Top-Down 메모이제이션 - O(n)"""
    if memo is None:
        memo = {0: 0, 1: 1}

    if n in memo:
        return memo[n]

    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

def fib_tab(n: int) -> int:
    """Bottom-Up 타뷸레이션 - O(n)"""
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]

def fib_optimized(n: int) -> int:
    """공간 최적화 - O(n) 시간, O(1) 공간"""
    if n <= 1:
        return n

    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr

    return prev1

# Python 데코레이터를 이용한 메모이제이션
@lru_cache(maxsize=None)
def fib_lru(n: int) -> int:
    """LRU 캐시 데코레이터 활용"""
    if n <= 1:
        return n
    return fib_lru(n - 1) + fib_lru(n - 2)

# ============================================
# 2. 0/1 배낭 문제
# ============================================

def knapsack_01(values: List[int], weights: List[int], capacity: int) -> Tuple[int, List[int]]:
    """
    0/1 배낭 문제 - O(nW)

    Returns: (최대 가치, 선택된 아이템 인덱스)
    """
    n = len(values)

    # DP 테이블: dp[i][w] = i번째 아이템까지 고려, 용량 w일 때 최대 가치
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Bottom-Up 채우기
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # i번째 아이템을 선택하지 않는 경우
            dp[i][w] = dp[i - 1][w]

            # i번째 아이템을 선택하는 경우 (용량 충분 시)
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]
                )

    # 선택된 아이템 역추적
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]

    selected.reverse()
    return dp[n][capacity], selected

def knapsack_01_optimized(values: List[int], weights: List[int], capacity: int) -> int:
    """
    공간 최적화 0/1 배낭 - O(W) 공간
    주의: 역추적 불가능
    """
    n = len(values)
    dp = [0] * (capacity + 1)

    for i in range(n):
        # 역순으로 업데이트 (같은 아이템 중복 선택 방지)
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]

# ============================================
# 3. 최장 공통 부분수열 (LCS)
# ============================================

def lcs(text1: str, text2: str) -> Tuple[int, str]:
    """
    최장 공통 부분수열 - O(mn)

    Returns: (LCS 길이, LCS 문자열)
    """
    m, n = len(text1), len(text2)

    # DP 테이블
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Bottom-Up
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # LCS 문자열 역추적
    lcs_str = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            lcs_str.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return dp[m][n], ''.join(reversed(lcs_str))

# ============================================
# 4. 최장 증가 부분수열 (LIS)
# ============================================

def lis_dp(nums: List[int]) -> int:
    """
    LIS - O(n²) DP
    """
    if not nums:
        return 0

    n = len(nums)
    dp = [1] * n  # dp[i] = nums[i]로 끝나는 LIS 길이

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)

def lis_binary_search(nums: List[int]) -> int:
    """
    LIS - O(n log n) 이진 탐색
    Patience Sorting 기반
    """
    if not nums:
        return 0

    tails = []  # tails[i] = 길이 i+1인 LIS의 최소 마지막 원소

    for num in nums:
        # 이진 탐색으로 num이 들어갈 위치 찾기
        left, right = 0, len(tails)
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid

        if left == len(tails):
            tails.append(num)
        else:
            tails[left] = num

    return len(tails)

# ============================================
# 5. 편집 거리 (Edit Distance / Levenshtein)
# ============================================

def edit_distance(word1: str, word2: str) -> int:
    """
    편집 거리 - O(mn)
    연산: 삽입, 삭제, 교체 (각각 비용 1)
    """
    m, n = len(word1), len(word2)

    # dp[i][j] = word1[0:i]를 word2[0:j]로 변환하는 최소 편집 거리
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 기저: 빈 문자열 변환
    for i in range(m + 1):
        dp[i][0] = i  # 삭제만
    for j in range(n + 1):
        dp[0][j] = j  # 삽입만

    # Bottom-Up
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # 매칭, 비용 0
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],     # 삭제
                    dp[i][j - 1],     # 삽입
                    dp[i - 1][j - 1]  # 교체
                )

    return dp[m][n]

# ============================================
# 6. 행렬 사슬 곱셈 (Matrix Chain Multiplication)
# ============================================

def matrix_chain_order(dimensions: List[int]) -> Tuple[int, List[List[int]]]:
    """
    행렬 사슬 곱셈 최적 순서 - O(n³)

    Args:
        dimensions: 행렬들의 차원 [p0, p1, p2, ..., pn]
                   행렬 i의 크기는 pi × p(i+1)

    Returns: (최소 곱셈 횟수, 분할 위치 테이블)
    """
    n = len(dimensions) - 1  # 행렬 개수

    # dp[i][j] = 행렬 i~j를 곱하는 최소 비용
    dp = [[0] * n for _ in range(n)]
    # split[i][j] = 최적 분할 위치
    split = [[0] * n for _ in range(n)]

    # l: 체인 길이
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            dp[i][j] = float('inf')

            for k in range(i, j):
                cost = (dp[i][k] + dp[k + 1][j] +
                        dimensions[i] * dimensions[k + 1] * dimensions[j + 1])

                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k

    return dp[0][n - 1], split

def print_optimal_parens(split: List[List[int]], i: int, j: int) -> str:
    """최적 괄호 순서 출력"""
    if i == j:
        return f"A{i + 1}"
    else:
        return (f"({print_optimal_parens(split, i, split[i][j])}"
                f" × {print_optimal_parens(split, split[i][j] + 1, j)})")

# ============================================
# 7. 최대 부분 배열 합 (Maximum Subarray Sum)
# ============================================

def max_subarray_sum(nums: List[int]) -> int:
    """
    Kadane's Algorithm - O(n)
    DP[i] = i번째 원소로 끝나는 최대 부분 배열 합
    """
    if not nums:
        return 0

    max_ending_here = max_so_far = nums[0]

    for num in nums[1:]:
        # 이전까지의 합을 이어갈지, 새로 시작할지 선택
        max_ending_here = max(num, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)

    return max_so_far

# ============================================
# 테스트
# ============================================

if __name__ == "__main__":
    print("=== 1. 피보나치 비교 ===")
    n = 35
    import time

    start = time.time()
    result_memo = fib_memo(n)
    print(f"메모이제이션 fib({n}) = {result_memo} ({time.time()-start:.4f}s)")

    start = time.time()
    result_tab = fib_tab(n)
    print(f"타뷸레이션 fib({n}) = {result_tab} ({time.time()-start:.4f}s)")

    start = time.time()
    result_opt = fib_optimized(n)
    print(f"공간최적화 fib({n}) = {result_opt} ({time.time()-start:.4f}s)")

    print("\n=== 2. 0/1 배낭 문제 ===")
    values = [60, 100, 120]
    weights = [10, 20, 30]
    capacity = 50
    max_val, selected = knapsack_01(values, weights, capacity)
    print(f"최대 가치: {max_val}, 선택: {selected}")

    print("\n=== 3. LCS ===")
    text1, text2 = "ABCBDAB", "BDCABA"
    length, lcs_str = lcs(text1, text2)
    print(f"LCS('{text1}', '{text2}') = '{lcs_str}' (길이: {length})")

    print("\n=== 4. LIS ===")
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"LIS {nums}: DP={lis_dp(nums)}, BS={lis_binary_search(nums)}")

    print("\n=== 5. 편집 거리 ===")
    print(f"edit_distance('horse', 'ros') = {edit_distance('horse', 'ros')}")

    print("\n=== 6. 행렬 사슬 곱셈 ===")
    dims = [10, 30, 5, 60]  # 3개 행렬: 10×30, 30×5, 5×60
    min_cost, split_table = matrix_chain_order(dims)
    print(f"최소 곱셈 횟수: {min_cost}")
    print(f"최적 순서: {print_optimal_parens(split_table, 0, len(dims)-2)}")

    print("\n=== 7. 최대 부분 배열 합 ===")
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"max_subarray_sum({nums}) = {max_subarray_sum(nums)}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. DP 적용 문제 분류

| 카테고리 | 문제 예시 | 상태 공간 | 전이 복잡도 |
|:---|:---|:---:|:---:|
| **1차원 선형** | 피보나치, 계단 오르기, LIS | $O(n)$ | $O(1) \sim O(n)$ |
| **2차원 그리드** | LCS, 편집 거리, 배낭 | $O(mn)$ | $O(1)$ |
| **구간 DP** | 행렬 사슬, palindrome | $O(n^2)$ | $O(n)$ |
| **비트마스크 DP** | TSP, 집합覆盖 | $O(n \cdot 2^n)$ | $O(n)$ |
| **트리 DP** | 독립 집합, 지름 | $O(n)$ | $O(degree)$ |

#### 2. Top-Down vs Bottom-Up 비교

| 특성 | Top-Down (메모이제이션) | Bottom-Up (타뷸레이션) |
|:---:|:---|:---|
| **구현** | 재귀 + 캐시 | 반복문 |
| **계산 순서** | 필요한 것만 | 모든 상태 |
| **스택 오버플로우** | 가능 | 없음 |
| **메모리** | 호출 스택 + 캐시 | 테이블만 |
| **적합 상황** | 불규칙한 의존성 | 규칙적 의존성 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오

**시나리오 A: DNA 서열 정렬**
- **문제**: 두 DNA 서열의 유사도 계산
- **전략**: LCS 또는 Needleman-Wunsch (편집 거리 변형)

**시나리오 B: 자원 스케줄링**
- **문제**: 제약 조건 하 작업 배치 최적화
- **전략**: 상태 압축 비트마스크 DP

#### 2. DP 적용 체크리스트
- [ ] 최적 부분구조 확인
- [ ] 중복 부분문제 확인
- [ ] 상태 정의 명확화
- [ ] 점화식 도출
- [ ] 기저 사례 정의
- [ ] 공간 최적화 고려

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 구분 | 효과 |
|:---:|:---|
| **정량적** | 지수 시간 → 다항 시간 단축 |
| **정성적** | 체계적 최적화 프레임워크 제공 |

#### 2. 참고 문헌
- **Bellman, R. (1957)**, "Dynamic Programming"
- **CLRS**, Chapter 15: Dynamic Programming

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [메모이제이션 (Memoization)](./memoization.md): Top-Down DP의 핵심.
- [타뷸레이션 (Tabulation)](./tabulation.md): Bottom-Up DP의 핵심.
- [분할 정복 (Divide and Conquer)](./divide_and_conquer.md): 부분문제 독립성 비교.
- [탐욕 알고리즘](./greedy_algorithm.md): 최적 부분구조 공유.
- [백트래킹 (Backtracking)](./backtracking.md): 완전 탐색 대안.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 동적 프로그래밍은 **"수학 숙제를 할 때 답을 노트에 적어두는 것"**과 같아요.
2. 한 번 푼 문제는 다시 풀지 않고 **노트에서 찾아서 쓰니까 시간이 아주 많이 줄어들어요**.
3. 복잡한 문제를 **작은 문제들로 나누고, 차곡차곡 모아서** 큰 답을 찾아요!
