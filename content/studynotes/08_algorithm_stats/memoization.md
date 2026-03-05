+++
title = "메모이제이션 (Memoization): Top-Down DP의 캐싱 전략"
date = "2026-03-04"
[extra]
categories = "studynotes-algorithm-stats"
+++

# 메모이제이션 (Memoization): Top-Down DP의 캐싱 전략

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 메모이제이션은 함수의 반환값을 캐시에 저장하여 **동일 입력에 대한 재호출 시 저장된 값을 즉시 반환**하는 최적화 기법으로, 동적 프로그래밍의 Top-Down 접근법 핵심입니다.
> 2. **가치**: 피보나치 수열 $O(2^n) \rightarrow O(n)$, 그래프 탐색 $O(2^n) \rightarrow O(n^2)$ 등 지수 시간 복잡도를 선형/다항 시간으로 획기적으로 단축합니다.
> 3. **융합**: 함수형 프로그래밍의 순수 함수, 웹 API 캐싱, React의 useMemo/useCallback, Redis/Memcached 등 광범위하게 활용됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 메모이제이션의 정의와 작동 원리

메모이제이션(Memoization)은 1968년 Donald Michie가 처음 제안한 기법으로, **"memo" (메모, 기억)**에서 유래한 단어입니다. (Memorization과 구별)

**핵심 원리**:
```
f(x) 호출 → 캐시에 x 존재?
    Yes → 캐시값 반환 (O(1))
    No  → f(x) 계산 → 결과를 캐시에 저장 → 반환
```

**적용 조건**:
1. **순수 함수 (Pure Function)**: 동일 입력 → 동일 출력
2. **부작용 없음 (No Side Effects)**: 외부 상태 변경 없음
3. **참조 투명성 (Referential Transparency)**: f(x)는 값으로 대체 가능

#### 💡 비유: 수학 공식책에 답 적어두기
복잡한 미적분 문제를 풀 때, 한 번 푼 문제의 답을 공식책 여백에 적어둡니다. 나중에 똑같은 문제가 나오면 다시 풀지 않고 적어둔 답을 바로 찾아 씁니다. 이것이 메모이제이션입니다. 문제를 푸는 시간은 10분이지만, 답을 찾는 시간은 1초입니다.

#### 2. 등장 배경 및 발전 과정
1. **Michie의 창안**: 1968년 AI 연구에서 "memo functions" 개념 제안.
2. **Lisp/함수형 언어**: 자연스러운 순수 함수 환경에서 널리 사용.
3. **현대적 확장**: Python의 `@lru_cache`, JavaScript의 메모이제이션 라이브러리, React Hooks 등.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 메모이제이션 구현 방식 비교

| 방식 | 구현 | 장점 | 단점 | 적합 상황 |
|:---:|:---|:---|:---|:---|
| **딕셔너리 캐시** | `memo = {}` | 유연한 키 | 직접 관리 | 일반적 사용 |
| **@lru_cache** | 데코레이터 | 간편, 자동 관리 | Python 한정 | Python 개발 |
| **클로저** | 함수 팩토리 | 캡슐화 | 복잡성 | 라이브러리 |
| **클래스** | 인스턴스 변수 | 상태 관리 | 보일러플레이트 | 복잡한 로직 |

#### 2. 메모이제이션 구조 다이어그램 (ASCII)

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    MEMOIZATION ARCHITECTURE                             │
  └─────────────────────────────────────────────────────────────────────────┘

                          ┌───────────────────┐
                          │  Function Call    │
                          │   f(args)         │
                          └─────────┬─────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
            ┌───────────────┐               ┌───────────────┐
            │  Cache Lookup │               │  Cache Miss   │
            │   (Hash)      │               │  (First Call) │
            └───────┬───────┘               └───────┬───────┘
                    │                               │
            ┌───────┴───────┐                      │
            │               │                      │
        Hit ▼           Miss ▼                      ▼
    ┌─────────────┐ ┌─────────────┐        ┌─────────────────┐
    │ Return      │ │ Compute     │        │ 1. Execute f()  │
    │ Cached      │ │ Function    │        │ 2. Store result │
    │ Value O(1)  │ │             │        │    in cache     │
    └─────────────┘ └──────┬──────┘        │ 3. Return       │
                          │               └────────┬────────┘
                          └─────────────────────────┘
                                            │
                                            ▼
                                    ┌───────────────┐
                                    │ Future Calls  │
                                    │   Hit Cache   │
                                    └───────────────┘

  ═══════════════════════════════════════════════════════════════════════════
  FIBONACCI MEMOIZATION TRACE
  ═══════════════════════════════════════════════════════════════════════════

  Cache State After Each Call:

  fib(5) 호출
  ├── fib(4) 호출
  │   ├── fib(3) 호출
  │   │   ├── fib(2) 호출
  │   │   │   ├── fib(1) 호출 → return 1, cache={1:1}
  │   │   │   ├── fib(0) 호출 → return 0, cache={0:0, 1:1}
  │   │   │   └── return 1, cache={0:0, 1:1, 2:1}
  │   │   ├── fib(1) 호출 → CACHE HIT! return 1
  │   │   └── return 2, cache={0:0, 1:1, 2:1, 3:2}
  │   ├── fib(2) 호출 → CACHE HIT! return 1
  │   └── return 3, cache={0:0, 1:1, 2:1, 3:2, 4:3}
  ├── fib(3) 호출 → CACHE HIT! return 2
  └── return 5, cache={0:0, 1:1, 2:1, 3:2, 4:3, 5:5}

  총 호출: 9회 (순진한 재귀: 15회, O(2^n))
  캐시 히트: 3회
  실제 계산: 6회 (O(n))
```

#### 3. 시간 복잡도 분석

| 함수 | 순진한 재귀 | 메모이제이션 | 개선율 |
|:---|:---:|:---:|:---:|
| fib(n) | $O(2^n)$ | $O(n)$ | $O(2^n) / n$ |
| binomial(n,k) | $O(2^n)$ | $O(nk)$ | 지수 → 다항 |
| lcs(m,n) | $O(2^{m+n})$ | $O(mn)$ | 지수 → 다항 |
| coin_change(n) | $O(k^n)$ | $O(n \cdot k)$ | 지수 → 다항 |

#### 4. 실무 코드 예시: 다양한 메모이제이션 패턴

```python
"""
메모이제이션 구현 패턴 모음
"""
from functools import lru_cache, wraps
from typing import Callable, Any, Dict, Tuple
import hashlib
import json
import time

# ============================================
# 1. 기본 딕셔너리 메모이제이션
# ============================================

def memoize_dict(func: Callable) -> Callable:
    """
    기본 딕셔너리 기반 메모이제이션 데코레이터
    """
    cache: Dict[Tuple, Any] = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        # 키 생성 (args + kwargs)
        key = (args, frozenset(kwargs.items()))

        if key not in cache:
            cache[key] = func(*args, **kwargs)

        return cache[key]

    # 캐시 접근을 위한 속성
    wrapper.cache = cache
    wrapper.cache_clear = lambda: cache.clear()

    return wrapper

# ============================================
# 2. LRU (Least Recently Used) 캐시
# ============================================

def memoize_lru(maxsize: int = 128) -> Callable:
    """
    LRU 캐시 기반 메모이제이션 (직접 구현)
    """
    def decorator(func: Callable) -> Callable:
        cache: Dict[Tuple, Any] = {}
        access_order = []  # 접근 순서 추적

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))

            if key in cache:
                # LRU 업데이트
                access_order.remove(key)
                access_order.append(key)
                return cache[key]

            # 캐시 미스 - 계산
            result = func(*args, **kwargs)

            # 캐시 크기 관리
            if maxsize > 0 and len(cache) >= maxsize:
                # 가장 오래된 항목 제거
                oldest = access_order.pop(0)
                del cache[oldest]

            cache[key] = result
            access_order.append(key)
            return result

        wrapper.cache = cache
        return wrapper

    return decorator

# Python 내장 lru_cache 사용
@lru_cache(maxsize=128)
def fibonacci_lru(n: int) -> int:
    """Python 내장 LRU 캐시 활용"""
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# ============================================
# 3. TTL (Time-To-Live) 메모이제이션
# ============================================

def memoize_ttl(ttl_seconds: float = 60.0) -> Callable:
    """
    만료 시간이 있는 메모이제이션
    """
    def decorator(func: Callable) -> Callable:
        cache: Dict[Tuple, Tuple[float, Any]] = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            current_time = time.time()

            # 만료된 항목 확인
            if key in cache:
                timestamp, value = cache[key]
                if current_time - timestamp < ttl_seconds:
                    return value
                else:
                    del cache[key]  # 만료됨

            # 계산 및 저장
            result = func(*args, **kwargs)
            cache[key] = (current_time, result)
            return result

        wrapper.cache = cache
        return wrapper

    return decorator

# ============================================
# 4. 재귀 함수용 클래스 기반 메모이제이션
# ============================================

class MemoizedRecursive:
    """
    재귀 함수에서 self-call도 메모이제이션되도록
    """
    def __init__(self, func: Callable):
        self.func = func
        self.cache: Dict[Tuple, Any] = {}
        wraps(func)(self)

    def __call__(self, *args, **kwargs):
        key = (args, frozenset(kwargs.items()))

        if key not in self.cache:
            # 재귀 호출 시 self.__call__을 통해 캐시 활용
            self.cache[key] = self.func(*args, **kwargs)

        return self.cache[key]

    def clear_cache(self):
        self.cache.clear()

# ============================================
# 5. 적용 예시들
# ============================================

@memoize_dict
def fibonacci_basic(n: int) -> int:
    """기본 메모이제이션"""
    if n <= 1:
        return n
    return fibonacci_basic(n - 1) + fibonacci_basic(n - 2)

@MemoizedRecursive
def fibonacci_class(n: int) -> int:
    """클래스 기반 - 재귀 내부 호출도 캐시"""
    if n <= 1:
        return n
    return fibonacci_class(n - 1) + fibonacci_class(n - 2)

@lru_cache(maxsize=None)
def binomial_coefficient(n: int, k: int) -> int:
    """이항 계수 - 파스칼 삼각형"""
    if k == 0 or k == n:
        return 1
    return binomial_coefficient(n - 1, k - 1) + binomial_coefficient(n - 1, k)

@lru_cache(maxsize=None)
def coin_change_ways(amount: int, coins: Tuple[int, ...], index: int = 0) -> int:
    """동전 교환 방법 수"""
    if amount == 0:
        return 1
    if amount < 0 or index >= len(coins):
        return 0

    # 현재 동전을 사용하는 경우 + 사용하지 않는 경우
    return (coin_change_ways(amount - coins[index], coins, index) +
            coin_change_ways(amount, coins, index + 1))

@memoize_ttl(ttl_seconds=5.0)
def expensive_computation(n: int) -> int:
    """TTL이 있는 계산 (5초 후 만료)"""
    time.sleep(0.1)  # 비용이 큰 계산 시뮬레이션
    return n ** 2

# ============================================
# 테스트 및 성능 비교
# ============================================

if __name__ == "__main__":
    print("=== 피보나치 성능 비교 ===")

    # 순진한 재귀 (느림)
    def fib_naive(n):
        if n <= 1:
            return n
        return fib_naive(n-1) + fib_naive(n-2)

    n = 35
    start = time.time()
    result_naive = fib_naive(n)
    print(f"순진한 재귀 fib({n}): {result_naive} ({time.time()-start:.4f}s)")

    start = time.time()
    result_memo = fibonacci_lru(n)
    print(f"메모이제이션 fib({n}): {result_memo} ({time.time()-start:.4f}s)")

    print("\n=== 캐시 정보 ===")
    print(f"fibonacci_lru 캐시 정보: {fibonacci_lru.cache_info()}")

    print("\n=== 이항 계수 ===")
    n, k = 30, 15
    print(f"C({n}, {k}) = {binomial_coefficient(n, k)}")
    print(f"캐시 정보: {binomial_coefficient.cache_info()}")

    print("\n=== 동전 교환 ===")
    coins = (1, 5, 10, 25)
    amount = 100
    print(f"{amount}원을 만드는 방법: {coin_change_ways(amount, coins)}가지")

    print("\n=== TTL 메모이제이션 ===")
    print("첫 호출 (계산):", expensive_computation(10))
    print("두 번째 호출 (캐시):", expensive_computation(10))
    print("5초 대기...")
    time.sleep(5.1)
    print("만료 후 호출 (재계산):", expensive_computation(10))
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 메모이제이션 vs 타뷸레이션 비교

| 특성 | 메모이제이션 (Top-Down) | 타뷸레이션 (Bottom-Up) |
|:---:|:---|:---|
| **방향** | 큰 문제 → 작은 문제 | 작은 문제 → 큰 문제 |
| **계산** | 필요한 것만 | 모든 부분문제 |
| **재귀** | 사용 | 사용 안 함 |
| **스택** | O(n) 깊이 | 없음 |
| **구현 난이도** | 직관적 | 체계적 |
| **적합 문제** | 불규칙 의존성 | 규칙적 의존성 |

#### 2. 캐시 전략 비교

| 전략 | 설명 | 장점 | 단점 |
|:---:|:---|:---|:---|
| **Unbounded** | 무제한 캐시 | 모든 결과 보존 | 메모리 폭발 |
| **LRU** | 최근 사용 순 | 자주 쓰는 것 보존 | 구현 복잡 |
| **LFU** | 빈도 순 | 핫 아이템 보존 | 빈도 계산 비용 |
| **TTL** | 시간 기반 만료 | 자동 갱신 | 만료 전 메모리 낭비 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오

**시나리오 A: API 응답 캐싱**
- **문제**: 동일 요청에 대한 반복 DB 조회
- **전략**: `@memoize_ttl(ttl_seconds=300)`로 5분 캐싱

**시나리오 B: 복잡한 계산 최적화**
- **문제**: 재귀적 수학 계산 (조합, 확률)
- **전략**: `@lru_cache(maxsize=None)`로 결과 저장

#### 2. 메모이제이션 적용 체크리스트
- [ ] 순수 함수인가? (부작용 없음)
- [ ] 입력이 해시 가능한가?
- [ ] 메모리 사용량이 감당 가능한가?
- [ ] 캐시 무효화 전략이 있는가?

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 구분 | 효과 |
|:---:|:---|
| **정량적** | 지수 시간 → 선형/다항 시간 |
| **정성적** | 코드 단순화 (재귀 그대로 사용) |

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [동적 프로그래밍 (Dynamic Programming)](./dynamic_programming.md): 메모이제이션의 이론적 기반.
- [타뷸레이션 (Tabulation)](./tabulation.md): Bottom-Up 대안.
- [해시 테이블 (Hash Table)](./03_datastructure/hash_table.md): 캐시 구현의 핵심.
- [재귀 (Recursion)](./recursion.md): 메모이제이션의 적용 대상.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 메모이제이션은 **"한 번 푼 숙제 답을 노트에 적어두는 것"**이에요.
2. 다음에 똑같은 문제가 나오면 **다시 풀지 않고 노트에서 찾아서** 시간을 아껴요.
3. 컴퓨터도 마찬가지로 **계산 결과를 저장해두고 다시 써서** 아주 빨라져요!
