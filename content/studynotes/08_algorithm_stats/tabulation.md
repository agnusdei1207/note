+++
title = "타뷸레이션 (Tabulation): Bottom-Up DP의 순차적 축적"
date = "2026-03-04"
[extra]
categories = "studynotes-algorithm-stats"
+++

# 타뷸레이션 (Tabulation): Bottom-Up DP의 순차적 축적

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 타뷸레이션은 가장 작은 부분문제부터 시작하여 **순차적으로 테이블을 채워나가는 Bottom-Up 동적 프로그래밍 방식**으로, 모든 부분문제를 한 번씩만 계산하여 스택 오버플로우 위험 없이 안정적으로 수행됩니다.
> 2. **가치**: 재귀 호출 오버헤드가 없고, **공간 최적화(슬라이딩 윈도우)**가 용이하며, 반복문 기반 구현으로 CPU 파이프라인 최적화가 잘 됩니다.
> 3. **융합**: 대규모 데이터 처리, 실시간 스트리밍 알고리즘, 임베디드 시스템에서 메모리/스택 제약 시 선호되는 DP 접근법입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 타뷸레이션의 정의와 특징

타뷸레이션(Tabulation)은 동적 프로그래밍의 **Bottom-Up 접근법**으로, 작은 부분문제의 해를 **테이블(배열/행렬)**에 저장하고, 이를 이용하여 더 큰 문제의 해를 순차적으로 구축합니다.

**핵심 특징**:
1. **순차적 계산**: 기저 사례 → 작은 문제 → 큰 문제 순서
2. **반복문 기반**: 재귀 없이 `for`/`while` 사용
3. **전체 테이블 계산**: 필요하지 않은 부분문제도 계산 가능
4. **공간 최적화 용이**: 직전 상태만 유지하면 메모리 O(1) 가능

**메모이제이션 vs 타뷸레이션**:
```
메모이제이션: f(n) 호출 → f(n-1) 필요 → f(n-2) 필요 → ... → f(0) 도달
타뷸레이션: f(0) 계산 → f(1) 계산 → ... → f(n) 계산
```

#### 💡 비유: 건물을 1층부터 지어올리기
메모이제이션은 "10층을 지으려면 9층이 필요하고, 9층을 지으려면 8층이 필요하고..."라며 위에서 아래로 생각합니다. 타뷸레이션은 **"1츨부터 차근차근 지어올려서 10층 완성"**입니다. 1츨을 지을 때 필요한 자재와 기술이 준비되면, 2층, 3층... 순서대로 쌓아올립니다.

#### 2. 등장 배경 및 발전 과정
1. **초기 DP 구현**: 컴퓨터 초기 재귀 제약으로 Bottom-Up가 표준.
2. **성능 최적화**: 재귀 오버헤드, 스택 제한 회피를 위한 선택.
3. **현대적 활용**: 스트리밍 알고리즘, 온라인 알고리즘에서 필수.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 타뷸레이션 구조

| 단계 | 설명 | 예시 (피보나치) |
|:---:|:---|:---|
| **1. 테이블 정의** | `dp[i]`의 의미 정의 | `dp[i]` = i번째 피보나치 수 |
| **2. 기저 초기화** | 가장 작은 문제들 | `dp[0]=0, dp[1]=1` |
| **3. 순회 순서** | 의존성 고려한 반복 방향 | `for i in range(2, n+1)` |
| **4. 점화식 적용** | 이전 값으로 현재 값 계산 | `dp[i] = dp[i-1] + dp[i-2]` |
| **5. 정답 반환** | 최종 결과 | `return dp[n]` |

#### 2. 타뷸레이션 실행 다이어그램 (ASCII)

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                 TABULATION (BOTTOM-UP DP) FLOW                          │
  └─────────────────────────────────────────────────────────────────────────┘

  Step 1: 테이블 생성
  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐
  │  0  │  1  │  2  │  3  │  4  │  5  │  6  │
  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤
  │  ?  │  ?  │  ?  │  ?  │  ?  │  ?  │  ?  │
  └─────┴─────┴─────┴─────┴─────┴─────┴─────┘

  Step 2: 기저 초기화
  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐
  │  0  │  1  │  2  │  3  │  4  │  5  │  6  │
  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤
  │  0  │  1  │  ?  │  ?  │  ?  │  ?  │  ?  │
  └─────┴─────┴─────┴─────┴─────┴─────┴─────┘
     ↑     ↑
   기저  기저

  Step 3-6: 순차적 계산
  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐
  │  0  │  1  │  2  │  3  │  4  │  5  │  6  │
  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤
  │  0  │  1  │  1  │  2  │  3  │  5  │  8  │
  └─────┴─────┴─────┴─────┴─────┴─────┴─────┘
           └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘
              │       │       │       │       │
           0+1=1   1+1=2   1+2=3   2+3=5   3+5=8

  ═══════════════════════════════════════════════════════════════════════════
  2D TABULATION EXAMPLE: LCS (Longest Common Subsequence)
  ═══════════════════════════════════════════════════════════════════════════

  Text1: "ABC" (m=3), Text2: "AC" (n=2)

  dp[i][j] = LCS(text1[0:i], text2[0:j])

      ""    A     C      ← text2
  ┌─────┬─────┬─────┐
  │  0  │  0  │  0  │  ""  ← 기저: 빈 문자열과의 LCS는 0
  ├─────┼─────┼─────┤
  │  0  │  1  │  1  │  A    ← A와 A 매칭: dp[0][0]+1 = 1
  ├─────┼─────┼─────┤      ← A와 C 불일치: max(1, 0) = 1
  │  0  │  1  │  1  │  B
  ├─────┼─────┼─────┤
  │  0  │  1  │  2  │  C    ← C와 C 매칭: dp[2][1]+1 = 2
  └─────┴─────┴─────┘
    ↑
  text1

  순회 순서: 위에서 아래, 왼쪽에서 오른쪽
```

#### 3. 공간 최적화 기법

| 기법 | 설명 | 적용 조건 | 공간 |
|:---:|:---|:---|:---:|
| **슬라이딩 윈도우** | 직전 k개 상태만 유지 | k-차원 의존성 | $O(k)$ |
| **1차원 압축** | 2D→1D 배열 | 행/열 단독 의존 | $O(n)$ |
| **In-place** | 원본 배열 활용 | 입력 수정 허용 | $O(1)$ |

#### 4. 실무 코드 예시: 타뷸레이션 패턴

```python
"""
타뷸레이션 (Bottom-Up DP) 구현 패턴 모음
"""
from typing import List, Tuple

# ============================================
# 1. 기본 타뷸레이션: 피보나치
# ============================================

def fib_tabulation(n: int) -> int:
    """
    피보나치 타뷸레이션 - O(n) 시간, O(n) 공간
    """
    if n <= 1:
        return n

    # 테이블 생성
    dp = [0] * (n + 1)
    dp[1] = 1

    # 순차적 계산
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]

def fib_optimized(n: int) -> int:
    """
    피보나치 공간 최적화 - O(n) 시간, O(1) 공간
    슬라이딩 윈도우 기법
    """
    if n <= 1:
        return n

    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr

    return prev1

# ============================================
# 2. 계단 오르기 문제
# ============================================

def climb_stairs(n: int) -> int:
    """
    n계단을 1칸 또는 2칸씩 오르는 방법 수
    O(n) 시간, O(1) 공간
    """
    if n <= 2:
        return n

    prev2, prev1 = 1, 2  # dp[1], dp[2]

    for _ in range(3, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr

    return prev1

# ============================================
# 3. 0/1 배낭 문제 (2D → 1D 최적화)
# ============================================

def knapsack_2d(values: List[int], weights: List[int], capacity: int) -> int:
    """
    0/1 배낭 - 2D 타뷸레이션 O(nW) 시간, O(nW) 공간
    """
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # 선택 안 함
            dp[i][w] = dp[i - 1][w]

            # 선택함 (용량 충분 시)
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]
                )

    return dp[n][capacity]

def knapsack_1d(values: List[int], weights: List[int], capacity: int) -> int:
    """
    0/1 배낭 - 1D 최적화 O(nW) 시간, O(W) 공간

    핵심: 역순 순회로 중복 선택 방지
    """
    n = len(values)
    dp = [0] * (capacity + 1)

    for i in range(n):
        # 역순 순회: 큰 용량부터 (중복 선택 방지)
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]

# ============================================
# 4. LCS (Longest Common Subsequence)
# ============================================

def lcs_tabulation(text1: str, text2: str) -> int:
    """
    LCS - O(mn) 시간, O(mn) 공간
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]

def lcs_optimized(text1: str, text2: str) -> int:
    """
    LCS - O(mn) 시간, O(min(m,n)) 공간
    두 행만 유지
    """
    if len(text1) < len(text2):
        text1, text2 = text2, text1  # text2가 더 짧게

    m, n = len(text1), len(text2)
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, prev  # swap

    return prev[n]

# ============================================
# 5. 편집 거리 (Edit Distance)
# ============================================

def edit_distance_tabulation(word1: str, word2: str) -> int:
    """
    편집 거리 - O(mn) 시간, O(mn) 공간
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 기저: 빈 문자열 변환
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # 삭제
                    dp[i][j - 1],      # 삽입
                    dp[i - 1][j - 1]   # 교체
                )

    return dp[m][n]

# ============================================
# 6. 최장 증가 부분수열 (LIS)
# ============================================

def lis_tabulation(nums: List[int]) -> int:
    """
    LIS - O(n²) 타뷸레이션
    dp[i] = nums[i]로 끝나는 LIS 길이
    """
    if not nums:
        return 0

    n = len(nums)
    dp = [1] * n  # 최소 자기 자신

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)

# ============================================
# 7. 동전 교환 (최소 동전 수)
# ============================================

def coin_change_min_coins(coins: List[int], amount: int) -> int:
    """
    동전 교환 (최소 개수) - O(n * amount) 시간

    dp[a] = 금액 a를 만드는 최소 동전 수
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # 0원을 만드는 동전 수: 0

    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1

# ============================================
# 8. 행렬 사슬 곱셈
# ============================================

def matrix_chain_tabulation(dimensions: List[int]) -> int:
    """
    행렬 사슬 곱셈 - O(n³) 시간

    dp[i][j] = i번째~j번째 행렬 곱의 최소 비용
    """
    n = len(dimensions) - 1  # 행렬 개수
    dp = [[0] * n for _ in range(n)]

    # l: 체인 길이
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            dp[i][j] = float('inf')

            for k in range(i, j):
                cost = (dp[i][k] + dp[k + 1][j] +
                        dimensions[i] * dimensions[k + 1] * dimensions[j + 1])
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]

# ============================================
# 9. 구간 DP: Palindrome Partitioning
# ============================================

def min_palindrome_cuts(s: str) -> int:
    """
    최소 팰린드롬 분할 횟수 - O(n²)
    """
    n = len(s)

    # is_pal[i][j] = s[i:j+1]이 팰린드롬인가?
    is_pal = [[False] * n for _ in range(n)]

    # 길이 1
    for i in range(n):
        is_pal[i][i] = True

    # 길이 2
    for i in range(n - 1):
        is_pal[i][i + 1] = (s[i] == s[i + 1])

    # 길이 3 이상
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = (s[i] == s[j]) and is_pal[i + 1][j - 1]

    # dp[i] = s[0:i+1]의 최소 분할 횟수
    dp = [float('inf')] * n

    for j in range(n):
        if is_pal[0][j]:
            dp[j] = 0
        else:
            for i in range(j):
                if is_pal[i + 1][j]:
                    dp[j] = min(dp[j], dp[i] + 1)

    return dp[n - 1]

# ============================================
# 테스트
# ============================================

if __name__ == "__main__":
    print("=== 피보나치 타뷸레이션 ===")
    for n in [10, 20, 50]:
        print(f"fib({n}) = {fib_optimized(n)}")

    print("\n=== 0/1 배낭 (2D vs 1D) ===")
    values = [60, 100, 120]
    weights = [10, 20, 30]
    capacity = 50
    print(f"2D: {knapsack_2d(values, weights, capacity)}")
    print(f"1D: {knapsack_1d(values, weights, capacity)}")

    print("\n=== LCS (공간 최적화) ===")
    text1, text2 = "ABCBDAB", "BDCABA"
    print(f"LCS('{text1}', '{text2}') = {lcs_optimized(text1, text2)}")

    print("\n=== 동전 교환 ===")
    coins = [1, 2, 5]
    amount = 11
    print(f"coins={coins}, amount={amount}: {coin_change_min_coins(coins, amount)}개")

    print("\n=== 행렬 사슬 곱셈 ===")
    dims = [10, 30, 5, 60]
    print(f"dimensions={dims}, 최소 비용: {matrix_chain_tabulation(dims)}")

    print("\n=== 팰린드롬 분할 ===")
    s = "aab"
    print(f"'{s}' 최소 분할: {min_palindrome_cuts(s)}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 메모이제이션 vs 타뷸레이션 상세 비교

| 특성 | 메모이제이션 | 타뷸레이션 |
|:---:|:---|:---|
| **구현** | 재귀 + 캐시 | 반복문 |
| **계산 범위** | 필요한 부분문제만 | 모든 부분문제 |
| **스택 오버플로우** | 가능 (깊은 재귀) | 없음 |
| **지역성** | 낮음 (재귀 점프) | 높음 (순차 접근) |
| **공간 최적화** | 어려움 | 용이 (슬라이딩 윈도우) |
| **적합 문제** | 불규칙 의존성 | 규칙적 의존성 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 선택 기준

**타뷸레이션 선택**:
- 모든 부분문제가 필요한 경우
- 스택 오버플로우 우려
- 공간 최적화가 중요한 경우
- 순차적 접근이 자연스러운 경우

**메모이제이션 선택**:
- 일부 부분문제만 필요한 경우
- 불규칙한 의존성 그래프
- 직관적 재귀 구조

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 구분 | 효과 |
|:---:|:---|
| **정량적** | 재귀 오버헤드 제거, 공간 O(n)→O(1) 가능 |
| **정성적** | 스택 안전, 캐시 친화적 |

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [메모이제이션 (Memoization)](./memoization.md): Top-Down 대안.
- [동적 프로그래밍 (Dynamic Programming)](./dynamic_programming.md): 이론적 기반.
- [공간 복잡도 (Space Complexity)](./space_complexity.md): 최적화 대상.
- [슬라이딩 윈도우](./sliding_window.md): 공간 최적화 기법.
- [배낭 문제](./knapsack_problem.md): 대표적 DP 문제.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 타뷸레이션은 **"1층부터 차근차근 건물을 지어올리는 방법"**이에요.
2. 아래층이 완성되어야 위층을 지을 수 있으니까 **순서대로, 하나씩** 쌓아올려요.
3. 이렇게 하면 **비계(스택) 없이도** 안전하게 높은 건물을 지을 수 있어요!
