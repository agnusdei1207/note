+++
title = "공간 복잡도 (Space Complexity): 메모리 자원의 효율적 관리"
date = "2026-03-04"
[extra]
categories = "studynotes-algorithm-stats"
+++

# 공간 복잡도 (Space Complexity): 메모리 자원의 효율적 관리

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 공간 복잡도는 알고리즘 수행에 필요한 **메모리 공간의 양**을 입력 크기 $n$의 함수로 표현한 것으로, **고정 공간(Auxiliary Space)**과 **입력 공간(Input Space)**의 합으로 구성됩니다.
> 2. **가치**: 메모리 제약 환경(임베디드, 모바일, 빅데이터)에서 알고리즘 선택의 결정적 기준을 제공하며, 시간-공간 트레이드오프(Space-Time Tradeoff) 분석의 근거가 됩니다.
> 3. **융합**: 가상 메모리, 캐시 계층, 분산 스토리지와 연계하여 실제 시스템 메모리 요구량 예측의 정확도를 높입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 공간 복잡도의 정의와 구성 요소
공간 복잡도 $S(n)$은 알고리즘이 입력 크기 $n$을 처리하기 위해 필요한 **총 메모리 공간**을 의미합니다. 이는 두 가지 구성 요소로 나뉩니다:

$$S(n) = \text{Fixed Space} + \text{Variable Space}$$

1. **고정 공간 (Fixed Space / Static Space)**
   - 명령어 공간 (코드 영역)
   - 단순 변수, 상수
   - 고정 크기 구조체
   - 입력 크기와 무관하게 일정함

2. **가변 공간 (Variable Space / Dynamic Space / Auxiliary Space)**
   - 동적 할당 메모리 (Heap)
   - 재귀 호출 스택
   - 입력 크기에 비례하여 증가
   - **보통 "공간 복잡도"라 하면 이 부분을 의미**

#### 💡 비유: 요리를 위한 주방 공간
요리(알고리즘)를 하려면 주방(메모리)이 필요합니다. **고정 공간**은 기본적으로 필요한 조리도구, 싱크대, 가스레인지입니다. **가변 공간**은 요리 메뉴(입력)에 따라 달라지는 재료 보관 공간과 조리 중 사용하는 접시들입니다. 10인분 요리보다 100인분 요리에 더 많은 임시 접시가 필요한 것처럼, 입력이 클수록 더 많은 메모리가 필요합니다.

#### 2. 등장 배경 및 발전 과정
1. **초기 컴퓨팅**: 1960~70년대 메모리가 귀한 시절, 공간 효율성은 생존 문제였습니다.
2. **시간-공간 트레이드오프 인식**: 더 많은 메모리를 사용하여 실행 속도를 높이는 기법(메모이제이션, 캐싱)이 보편화되었습니다.
3. **현대적 도전**: 빅데이터와 AI 시대에 메모리 부족(OOM)은 여전히 치명적 장애입니다. 공간 복잡도는 임베디드, IoT, 엣지 컴퓨팅에서 핵심 설계 기준입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 메모리 영역별 공간 복잡도

| 메모리 영역 | 용도 | 크기 결정 요인 | 해제 시점 | 예시 |
|:---:|:---|:---|:---|:---|
| **Code Segment** | 프로그램 코드 | 알고리즘 길이 | 프로그램 종료 | 컴파일된 명령어 |
| **Data Segment** | 전역/정적 변수 | 전역 변수 개수 | 프로그램 종료 | `static int count` |
| **Stack** | 지역 변수, 재귀 호출 | 재귀 깊이, 지역변수 | 함수 반환 | 재귀 호출 프레임 |
| **Heap** | 동적 할당 | `malloc`, `new` 호출 | 명시적/GC | 리스트, 트리 노드 |

#### 2. 공간 복잡도 분석 다이어그램 (ASCII)

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    MEMORY SPACE ANALYSIS                           │
  └─────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────┐
                    │      INPUT SPACE (n units)      │
                    │   [Original Input Data]         │
                    │   e.g., Array of n integers     │
                    └─────────────────────────────────┘
                                    │
                                    ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │                     AUXILIARY SPACE                                │
  │                                                                     │
  │   ┌──────────────────────────────────────────────────────────────┐ │
  │   │                    O(1) - Constant Space                     │ │
  │   │  ┌───┬───┬───┬───┐                                          │ │
  │   │  │ i │ j │tmp│len│  ← Loop variables, temporaries           │ │
  │   │  └───┴───┴───┴───┘                                          │ │
  │   │  Examples: In-place Sort, Swap algorithms                    │ │
  │   └──────────────────────────────────────────────────────────────┘ │
  │                                                                     │
  │   ┌──────────────────────────────────────────────────────────────┐ │
  │   │                   O(log n) - Stack Space                     │ │
  │   │  ┌─────────────────────────────┐                             │ │
  │   │  │   Recursion Frame (log n)   │                             │ │
  │   │  │  ┌─────┐┌─────┐┌─────┐    │                             │ │
  │   │  │  │f(n) ││f(n/2)││f(n/4)│   │                             │ │
  │   │  │  └─────┘└─────┘└─────┘    │                             │ │
  │   │  └─────────────────────────────┘                             │ │
  │   │  Examples: Binary Search, Balanced Tree recursion            │ │
  │   └──────────────────────────────────────────────────────────────┘ │
  │                                                                     │
  │   ┌──────────────────────────────────────────────────────────────┐ │
  │   │                     O(n) - Linear Space                      │ │
  │   │  ┌───┬───┬───┬───┬───┬───────┬───┐                          │ │
  │   │  │ 0 │ 1 │ 2 │ 3 │ 4 │  ...  │n-1│  ← Auxiliary array       │ │
  │   │  └───┴───┴───┴───┴───┴───────┴───┘                          │ │
  │   │  Examples: Merge Sort temp array, Hash Table, DP Table       │ │
  │   └──────────────────────────────────────────────────────────────┘ │
  │                                                                     │
  │   ┌──────────────────────────────────────────────────────────────┐ │
  │   │                    O(n²) - Quadratic Space                   │ │
  │   │  ┌───┬───┬───┬───┐                                          │ │
  │   │  │   │   │   │   │                                          │ │
  │   │  ├───┼───┼───┼───┤   n x n Matrix                           │ │
  │   │  │   │   │   │   │                                          │ │
  │   │  ├───┼───┼───┼───┤   Examples: Floyd-Warshall,              │ │
  │   │  │   │   │   │   │            Edit Distance DP              │ │
  │   │  └───┴───┴───┴───┘                                          │ │
  │   └──────────────────────────────────────────────────────────────┘ │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘

  [Space-Time Tradeoff Examples]

  +-------------------+---------------+---------------+
  | Algorithm         | Time          | Space         |
  +-------------------+---------------+---------------+
  | Merge Sort        | O(n log n)    | O(n)          | ← Uses extra array
  | Quick Sort        | O(n log n)    | O(log n)      | ← In-place, recursion
  | Heap Sort         | O(n log n)    | O(1)          | ← True in-place
  | Hash Table Lookup | O(1) avg      | O(n)          | ← Space for speed
  +-------------------+---------------+---------------+
```

#### 3. 심층 동작 원리: 공간 복잡도 분석 5단계

**① 입력 공간 계산**
- 입력 데이터 자체가 차지하는 공간을 파악합니다.
- 예: $n$개의 정수 배열 → $4n$ bytes (32-bit)

**② 보조 공간 식별**
- 알고리즘이 추가로 사용하는 메모리를 식별합니다.
- 임시 배열, 해시 테이블, DP 테이블 등

**③ 재귀 스택 공간**
- 재귀 호출 시 각 프레임이 차지하는 공간 × 최대 깊이
- 예: 이진 탐색 → $O(\log n)$ 스택

**④ 동적 할당 추적**
- 런타임에 `malloc`, `new` 등으로 할당되는 메모리
- 연결 리스트, 트리 노드 등

**⑤ 총 공간 복잡도 도출**
- 모든 구성 요소의 합을 점근 표기법으로 표현

#### 4. 실무 코드 예시: 공간 복잡도 비교

```python
import sys
from typing import List, Optional
from dataclasses import dataclass
import tracemalloc

# ============================================
# O(1) Space: 제자리 정렬 (In-place Sort)
# ============================================
def selection_sort_inplace(arr: List[int]) -> None:
    """
    선택 정렬 - O(1) 보조 공간
    입력 배열 내에서 직접 교환만 수행
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # 교환 (추가 메모리 불필요)
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

# ============================================
# O(n) Space: 합병 정렬 (Merge Sort)
# ============================================
def merge_sort(arr: List[int]) -> List[int]:
    """
    합병 정렬 - O(n) 보조 공간
    병합 단계에서 임시 배열 필요
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])   # 새 리스트 생성
    right = merge_sort(arr[mid:])  # 새 리스트 생성

    return _merge(left, right)

def _merge(left: List[int], right: List[int]) -> List[int]:
    """두 정렬된 리스트 병합 - O(n) 공간"""
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
# O(log n) Space: 퀵 정렬 (Quick Sort)
# ============================================
def quick_sort(arr: List[int], low: int = 0, high: Optional[int] = None) -> None:
    """
    퀵 정렬 - O(log n) 스택 공간 (평균)
    재귀 깊이만큼 스택 사용
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = _partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)

def _partition(arr: List[int], low: int, high: int) -> int:
    """Lomuto 파티션 - O(1) 공간"""
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# ============================================
# O(n²) Space: 동적 프로그래밍 (Edit Distance)
# ============================================
def edit_distance_dp(str1: str, str2: str) -> int:
    """
    편집 거리 (Levenshtein Distance) - O(mn) 공간
    2차원 DP 테이블 사용
    """
    m, n = len(str1), len(str2)

    # m x n 2차원 테이블 생성
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 초기화
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # DP 채우기
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # 삭제
                    dp[i][j-1],    # 삽입
                    dp[i-1][j-1]   # 교체
                )

    return dp[m][n]

# ============================================
# 공간 최적화: O(n) → O(1) 예시
# ============================================
def edit_distance_optimized(str1: str, str2: str) -> int:
    """
    편집 거리 - O(min(m,n)) 공간으로 최적화
    이전 행과 현재 행만 유지
    """
    m, n = len(str1), len(str2)

    # 더 짧은 문자열을 열로 사용
    if m < n:
        str1, str2 = str2, str1
        m, n = n, m

    # 두 행만 유지
    prev = list(range(n + 1))
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                curr[j] = prev[j-1]
            else:
                curr[j] = 1 + min(prev[j], curr[j-1], prev[j-1])
        prev, curr = curr, prev

    return prev[n]

# ============================================
# 메모리 사용량 측정 유틸리티
# ============================================
def measure_memory_usage(func, *args) -> tuple:
    """함수 실행 시 메모리 사용량 측정"""
    tracemalloc.start()

    result = func(*args)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return result, peak / 1024  # KB 단위

# 테스트
if __name__ == "__main__":
    import random

    # 테스트 데이터
    n = 10000
    test_arr = [random.randint(1, 100000) for _ in range(n)]

    print(f"=== 공간 복잡도 비교 (n={n}) ===\n")

    # O(1) 공간
    arr1 = test_arr.copy()
    _, mem = measure_memory_usage(selection_sort_inplace, arr1)
    print(f"선택 정렬 (O(1)): {mem:.2f} KB")

    # O(n) 공간
    _, mem = measure_memory_usage(merge_sort, test_arr.copy())
    print(f"합병 정렬 (O(n)): {mem:.2f} KB")

    # O(log n) 공간
    arr3 = test_arr.copy()
    _, mem = measure_memory_usage(quick_sort, arr3, 0, n-1)
    print(f"퀵 정렬 (O(log n)): {mem:.2f} KB")

    print("\n=== 편집 거리 공간 최적화 ===")
    s1, s2 = "algorithm", "logarithm"

    _, mem_dp = measure_memory_usage(edit_distance_dp, s1, s2)
    _, mem_opt = measure_memory_usage(edit_distance_optimized, s1, s2)

    print(f"기본 DP (O(mn)): {mem_dp:.2f} KB")
    print(f"최적화 (O(min(m,n))): {mem_opt:.2f} KB")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 정렬 알고리즘 공간 복잡도 비교

| 알고리즘 | 시간 복잡도 | 공간 복잡도 | 제자리 여부 | 안정성 | 적합 상황 |
|:---:|:---:|:---:|:---:|:---:|:---|
| 버블 정렬 | $O(n^2)$ | $O(1)$ | Yes | Yes | 교육용, 소규모 |
| 선택 정렬 | $O(n^2)$ | $O(1)$ | Yes | No | 메모리 극도 제약 |
| 삽입 정렬 | $O(n^2)$ | $O(1)$ | Yes | Yes | 거의 정렬된 데이터 |
| 합병 정렬 | $O(n \log n)$ | $O(n)$ | No | Yes | 안정성 필요 |
| 퀵 정렬 | $O(n \log n)$ | $O(\log n)$ | Yes | No | 범용 고속 정렬 |
| 힙 정렬 | $O(n \log n)$ | $O(1)$ | Yes | No | 메모리 + 속도 |

#### 2. 시간-공간 트레이드오프 분석

| 기법 | 시간 개선 | 공간 비용 | 예시 |
|:---|:---:|:---:|:---|
| 메모이제이션 | 중복 계산 제거 | 결과 캐싱 | 피보나치 DP |
| 해시 테이블 | $O(n) \rightarrow O(1)$ | $O(n)$ | 빠른 조회 |
| 인덱싱 | $O(n) \rightarrow O(\log n)$ | 인덱스 저장 | DB 인덱스 |
| 비트마스크 | 집합 연산 고속화 | 정수형 저장 | DP 상태 압축 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오

**시나리오 A: 임베디드 시스템 메모리 제약**
- **환경**: 64KB RAM, 1MB 플래시
- **문제**: 5000개 센서 데이터 정렬 필요
- **전략**: $O(1)$ 공간의 **힙 정렬** 사용, 재귀 대신 반복문으로 스택 오버플로우 방지

**시나리오 B: 빅데이터 처리의 메모리 부족**
- **환경**: 100GB 데이터, 16GB RAM
- **문제**: 메모리에 한 번에 로드 불가
- **전략**: **외부 정렬(External Sort)** - 데이터를 청크로 분할, 각각 메모리 내에서 정렬 후 디스크 기반 병합

#### 2. 공간 최적화 체크리스트
- [ ] 불필요한 복사 제거 (참조 활용)
- [ ] 재귀 → 반복문 변환 고려
- [ ] DP 테이블 공간 최적화 (2행만 유지)
- [ ] 적절한 자료구조 선택 (배열 vs 연결리스트)

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 구분 | 효과 | 비고 |
|:---:|:---|:---|
| **정량적** | 메모리 사용량 50% 절감 | 공간 최적화 알고리즘 적용 시 |
| **정량적** | OOM 장애 90% 감소 | 정확한 공간 요구량 예측 |
| **정성적** | 시스템 안정성 향상 | 메모리 여유 확보 |

#### 2. 미래 전망
- **메모리 계층 인식 알고리즘**: L1/L2/L3 캐시, RAM, SSD의 계층을 고려한 알고리즘 설계가 중요해집니다.

#### ※ 참고 표준
- **MISRA C**: 임베디드 시스템의 동적 메모리 할당 제한 가이드라인

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [시간 복잡도 (Time Complexity)](./time_complexity.md): 시간-공간 트레이드오프의 대상.
- [동적 프로그래밍 (Dynamic Programming)](./dynamic_programming.md): 공간-시간 교환의 대표 사례.
- [재귀 (Recursion)](./recursion.md): 스택 공간 복잡도의 주원인.
- [힙 정렬 (Heap Sort)](./01_sorting/heap_sort.md): O(1) 공간 정렬의 예시.
- [해시 테이블 (Hash Table)](./03_datastructure/hash_table.md): O(n) 공간으로 O(1) 시간 달성.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 공간 복잡도는 **"방을 얼마나 넓게 써야 하는지"**를 나타내는 거예요.
2. 어떤 알고리즘은 책상만 있으면 되지만(O(1)), 어떤 건 큰 창고가 필요해요(O(n)).
3. 좋은 알고리즘은 **작은 방에서도 효율적으로 일해서** 공간을 아껴줘요!
