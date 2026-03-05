+++
title = "재귀 (Recursion): 자기 자신을 호출하는 우아한 문제 해결법"
date = "2026-03-04"
[extra]
categories = "studynotes-algorithm-stats"
+++

# 재귀 (Recursion): 자기 자신을 호출하는 우아한 문제 해결법

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 재귀는 함수가 **자기 자신을 호출(Self-Reference)**하여 문제를 더 작은 부분 문제로 분해해 해결하는 알고리즘 설계 패러다임으로, 분할 정복과 동적 프로그래밍의 이론적 기반이다.
> 2. **가치**: 복잡한 문제를 **수학적 귀납법**처럼 간결하게 표현할 수 있어, 트리 순회, 그래프 탐색, 수학적 계산 등에서 코드 가독성과 설계 단순성을 극대화한다.
> 3. **융합**: 운영체제의 함수 호출 스택, 파일 시스템의 디렉터리 탐색, 컴파일러의 파싱 알고리즘 등 시스템 소프트웨어 전반에 걸쳐 필수적으로 활용된다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 재귀의 정의와 설계 철학
재귀(Recursion)는 어떤 문제를 해결하기 위해 **동일한 구조의 더 작은 문제**로 쪼개고, 그 작은 문제를 다시 자신의 함수로 해결하는 방식입니다. 모든 재귀 함수는 두 가지 핵심 요소를 반드시 포함해야 합니다:

1. **기본 사례 (Base Case)**: 재귀 호출을 멈추는 종료 조건
2. **재귀 사례 (Recursive Case)**: 문제를 더 작은 크기로 분해하여 자신을 호출

#### 💡 비유: 거울 속의 거울
화장실에서 큰 거울 앞에 작은 거울을 대면, 거울 속에 거울이 무한히 비칩니다. 하지만 어느 순간 거울이 너무 작아져서 더 이상 비칠 수 없게 되죠. 재귀도 이와 같습니다. 함수가 자기 자신을 계속 호출하지만, **기본 사례(Base Case)**라는 "더 이상 쪼갤 수 없는 단계"에 도달하면 멈춥니다.

#### 2. 등장 배경 및 발전 과정
1. **수학적 기원**: 19세기 수학자들은 피보나치 수열, 팩토리얼 등을 점화식으로 정의했습니다. 이것이 재귀의 이론적 뿌리입니다.
2. **프로그래밍 언어의 발전**: 1958년 LISP이 최초로 재귀를 일급 시민으로 채택했습니다.
3. **구조적 프로그래밍**: 1960년대, 재귀는 복잡한 문제를 우아하게 표현하는 도구로 인정받았습니다.
4. **현대적 활용**: 함수형 프로그래밍(Haskell, Scala)에서 재귀는 루프를 대체하는 주요 제어 구조입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 재귀의 실행 메커니즘: 호출 스택 (Call Stack)

```
┌─────────────────────────────────────────────────────────────────┐
│                    재귀 호출 스택 동작 예시                        │
│                    factorial(4) 계산 과정                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [1] 초기 호출: factorial(4)                                    │
│      ┌──────────────────┐                                       │
│      │ factorial(4)     │ ← 4 * factorial(3) 대기               │
│      │ return 4 * ?     │                                       │
│      └──────────────────┘                                       │
│                                                                 │
│  [2] 첫 번째 재귀: factorial(3)                                  │
│      ┌──────────────────┐                                       │
│      │ factorial(3)     │ ← 3 * factorial(2) 대기               │
│      │ return 3 * ?     │                                       │
│      ├──────────────────┤                                       │
│      │ factorial(4)     │ (대기 중)                              │
│      └──────────────────┘                                       │
│                                                                 │
│  [3] 두 번째 재귀: factorial(2)                                  │
│      ┌──────────────────┐                                       │
│      │ factorial(2)     │ ← 2 * factorial(1) 대기               │
│      ├──────────────────┤                                       │
│      │ factorial(3)     │ (대기 중)                              │
│      ├──────────────────┤                                       │
│      │ factorial(4)     │ (대기 중)                              │
│      └──────────────────┘                                       │
│                                                                 │
│  [4] 기본 사례 도달: factorial(1) = 1 반환                        │
│      ┌──────────────────┐                                       │
│      │ factorial(1)     │ → return 1 (Base Case!)               │
│      └──────────────────┘                                       │
│                                                                 │
│  [5~7] 스택 해제 (Unwinding):                                    │
│      factorial(2) = 2 * 1 = 2                                   │
│      factorial(3) = 3 * 2 = 6                                   │
│      factorial(4) = 4 * 6 = 24 ✓                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 2. 재귀 vs 반복 (Recursion vs Iteration)

```python
# 재귀적 팩토리얼
def factorial_recursive(n):
    """
    재귀 방식 팩토리얼

    시간 복잡도: O(n)
    공간 복잡도: O(n) - 호출 스택
    """
    # 기본 사례 (Base Case)
    if n <= 1:
        return 1
    # 재귀 사례 (Recursive Case)
    return n * factorial_recursive(n - 1)


# 반복적 팩토리얼
def factorial_iterative(n):
    """
    반복문 방식 팩토리얼

    시간 복잡도: O(n)
    공간 복잡도: O(1) - 상수 공간
    """
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# 꼬리 재귀 팩토리얼 (Tail Recursion)
def factorial_tail(n, accumulator=1):
    """
    꼬리 재귀 방식 팩토리얼

    특징: 재귀 호출이 함수의 마지막 연산
    최적화: TCO 지원 시 O(1) 공간
    Python은 TCO 미지원이지만, 개념적 이해용
    """
    if n <= 1:
        return accumulator
    return factorial_tail(n - 1, n * accumulator)
```

#### 3. 대표적 재귀 알고리즘 구현

**A. 피보나치 수열 (비효율적 vs 효율적)**

```python
import time
from functools import lru_cache

# 순진한 재귀 (지수 시간 - 매우 비효율적)
def fib_naive(n):
    """
    시간 복잡도: O(2^n) - 중복 계산 폭발
    공간 복잡도: O(n)

    문제: fib(5)를 구할 때 fib(3)이 2번, fib(2)가 3번 계산됨
    """
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


# 메모이제이션 적용 (선형 시간)
@lru_cache(maxsize=None)
def fib_memo(n):
    """
    시간 복잡도: O(n) - 각 n에 대해 1번만 계산
    공간 복잡도: O(n)

    LRU Cache가 이전 결과를 저장하여 중복 계산 방지
    """
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


# 반복적 DP (최적)
def fib_dp(n):
    """
    시간 복잡도: O(n)
    공간 복잡도: O(1) - 변수 2개만 사용
    """
    if n <= 1:
        return n

    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr


# 성능 비교
def benchmark_fib():
    n = 35

    start = time.time()
    result_naive = fib_naive(n)
    time_naive = time.time() - start

    start = time.time()
    result_memo = fib_memo(n)
    time_memo = time.time() - start

    start = time.time()
    result_dp = fib_dp(n)
    time_dp = time.time() - start

    print(f"n={n}")
    print(f"Naive: {time_naive:.4f}s")
    print(f"Memo:  {time_memo:.6f}s")
    print(f"DP:    {time_dp:.6f}s")
```

**B. 하노이 탑 (Tower of Hanoi)**

```python
def hanoi(n, source, auxiliary, target, moves=None):
    """
    하노이 탑 재귀 알고리즘

    시간 복잡도: O(2^n) - 이동 횟수
    공간 복잡도: O(n) - 재귀 깊이

    Parameters:
    - n: 원반 개수
    - source: 출발 기둥
    - auxiliary: 보조 기둥
    - target: 목표 기둥
    """
    if moves is None:
        moves = []

    if n == 1:
        moves.append(f"{source} → {target}")
        return moves

    # n-1개를 보조 기둥으로 이동
    hanoi(n - 1, source, target, auxiliary, moves)

    # 가장 큰 원반을 목표 기둥으로 이동
    moves.append(f"{source} → {target}")

    # n-1개를 보조 기둥에서 목표 기둥으로 이동
    hanoi(n - 1, auxiliary, source, target, moves)

    return moves

# 실행 예시
# moves = hanoi(3, 'A', 'B', 'C')
# print(f"총 {len(moves)}회 이동:")
# for move in moves:
#     print(move)
```

**C. 이진 트리 순회 (Binary Tree Traversal)**

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def preorder(root, result=None):
    """전위 순회: Root → Left → Right"""
    if result is None:
        result = []
    if root:
        result.append(root.val)     # 1. 루트 방문
        preorder(root.left, result)  # 2. 왼쪽 서브트리
        preorder(root.right, result) # 3. 오른쪽 서브트리
    return result


def inorder(root, result=None):
    """중위 순회: Left → Root → Right (BST에서 정렬 순서)"""
    if result is None:
        result = []
    if root:
        inorder(root.left, result)   # 1. 왼쪽 서브트리
        result.append(root.val)      # 2. 루트 방문
        inorder(root.right, result)  # 3. 오른쪽 서브트리
    return result


def postorder(root, result=None):
    """후위 순회: Left → Right → Root (트리 삭제 시 사용)"""
    if result is None:
        result = []
    if root:
        postorder(root.left, result)  # 1. 왼쪽 서브트리
        postorder(root.right, result) # 2. 오른쪽 서브트리
        result.append(root.val)       # 3. 루트 방문
    return result


# 트리 높이 계산 (재귀 활용)
def tree_height(root):
    """트리의 높이 계산"""
    if not root:
        return 0
    return 1 + max(tree_height(root.left), tree_height(root.right))
```

#### 4. 재귀 복잡도 분석: 마스터 정리 (Master Theorem)

$$T(n) = aT\left(\frac{n}{b}\right) + f(n)$$

| 케이스 | 조건 | 시간 복잡도 |
|:---:|:---|:---:|
| 1 | $f(n) = O(n^{\log_b a - \epsilon})$ | $\Theta(n^{\log_b a})$ |
| 2 | $f(n) = \Theta(n^{\log_b a} \log^k n)$ | $\Theta(n^{\log_b a} \log^{k+1} n)$ |
| 3 | $f(n) = \Omega(n^{\log_b a + \epsilon})$ | $\Theta(f(n))$ |

**적용 예시:**
- 이진 탐색: $T(n) = T(n/2) + O(1)$ → $\Theta(\log n)$
- 합병 정렬: $T(n) = 2T(n/2) + O(n)$ → $\Theta(n \log n)$
- 피보나치 (비효율): $T(n) = T(n-1) + T(n-2) + O(1)$ → $\Theta(\phi^n)$

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 재귀 vs 반복 심층 비교

| 비교 항목 | 재귀 (Recursion) | 반복 (Iteration) |
|:---|:---|:---|
| **가독성** | 수학적 정의와 일치, 직관적 | 상태 관리가 명시적, 복잡할 수 있음 |
| **메모리** | O(n) 스택 공간 필요 | O(1) 상수 공간 가능 |
| **오버헤드** | 함수 호출 비용 존재 | 직접 점프, 효율적 |
| **스택 오버플로우** | 깊은 재귀 시 위험 | 없음 |
| **디버깅** | 호출 스택 추적 용이 | 변수 상태 추적 필요 |
| **함수형 언어** | 자연스러운 표현 | 부자연스러움 |
| **적합 문제** | 트리, 그래프, 분할 정복 | 단순 반복, 순차 처리 |

#### 2. 과목 융합 관점 분석

**A. 운영체제 융합: 프로세스 스택**
- 재귀 함수 호출 시마다 **스택 프레임(Stack Frame)** 생성
- 지역 변수, 반환 주소, 이전 프레임 포인터 저장
- 스택 크기 제한 (Linux 기본 8MB) → 깊은 재귀 시 오버플로우

**B. 컴파일러 융합: 파싱과 AST**
- **재귀 하강 파서(Recursive Descent Parser)**: 문법 규칙을 재귀 함수로 변환
- **추상 구문 트리(AST)**: 트리 구조를 재귀로 순회하여 코드 생성

**C. 파일 시스템 융합: 디렉터리 탐색**
```python
import os

def list_files_recursive(directory, depth=0):
    """재귀적 디렉터리 순회"""
    indent = "  " * depth
    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        if os.path.isdir(path):
            print(f"{indent}📁 {entry}/")
            list_files_recursive(path, depth + 1)
        else:
            print(f"{indent}📄 {entry}")
```

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 A: JSON 데이터 중첩 처리**
- **문제**: 깊이가 불확정한 중첩 JSON 구조 파싱
- **기술사적 결단**:
  - 재귀적 파싱 함수 작성 (자연스러운 표현)
  - 최대 깊이 제한 설정 (무한 재귀 방지)
  - 깊이 > 100 시 예외 처리

**시나리오 B: 대규모 그래프 DFS 탐색**
- **문제**: 100만 노드 그래프에서 연결 요소 탐색
- **기술사적 결단**:
  - 재귀 DFS 대신 **명시적 스택** 사용
  - 이유: 파이썬 기본 재귀 제한 ~1000, 스택 오버플로우 위험
  - `sys.setrecursionlimit()`으로 제한을 늘릴 수 있으나 근본 해결 아님

#### 2. 도입 시 고려사항 (체크리스트)

**기술적 고려사항**:
- [ ] 재귀 깊이 예상 (시스템 제한과 비교)
- [ ] 기본 사례(Base Case)가 모든 경로에서 도달 가능한지 검증
- [ ] 꼬리 재귀 최적화(TCO) 가능성 확인 (언어 의존)

**운영적 고려사항**:
- [ ] 프로덕션 환경에서 재귀 깊이 모니터링
- [ ] 스택 오버플로우 예외 처리
- [ ] 성능 크리티컬 섹션에서 반복문 고려

#### 3. 주의사항 및 안티패턴

**안티패턴 1: 무한 재귀 (Infinite Recursion)**
```python
# 잘못된 예: 기본 사례 누락
def bad_recursion(n):
    return n * bad_recursion(n - 1)  # 종료 조건 없음!

# 올바른 예
def good_recursion(n):
    if n <= 1:  # 기본 사례
        return 1
    return n * good_recursion(n - 1)
```

**안티패턴 2: 지수 시간 재귀 (중복 계산)**
```python
# 비효율: O(2^n)
def fib_bad(n):
    if n <= 1:
        return n
    return fib_bad(n-1) + fib_bad(n-2)  # 중복 계산

# 효율: O(n) with memoization
from functools import lru_cache
@lru_cache
def fib_good(n):
    if n <= 1:
        return n
    return fib_good(n-1) + fib_good(n-2)
```

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 효과 내용 | 기대 수치 |
|:---:|:---|:---|
| **정량적** | 코드 라인 수 감소 | 반복 대비 30~50% 감소 |
| **정량적** | 버그 발생률 감소 | 수학적 정의와 일치하여 논리 오류 감소 |
| **정성적** | 유지보수성 향상 | 문제 구조와 코드 구조의 일치 |
| **정성적** | 알고리즘 설계 용이성 | 분할 정복, 동적 프로그래밍의 자연스러운 표현 |

#### 2. 미래 전망 및 진화 방향
1. **꼬리 재귀 최적화 확대**: Python 제외 주요 언어에서 TCO 지원 확대
2. **함수형 프로그래밍 부상**: 순수 함수와 불변성에서 재귀의 중요성 증대
3. **하이브리드 접근**: 재귀로 설계, 반복으로 최적화하는 패턴 보편화

#### ※ 참고 표준/가이드
- **SICP (Structure and Interpretation of Computer Programs)**: 재귀 사고 교과서
- **Python PEP 8**: 재귀 함수 명명 규칙 및 가이드라인
- **IEEE 754**: 재귀적 수치 알고리즘의 정밀도 가이드

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [분할 정복 (Divide and Conquer)](./divide_and_conquer.md): 재귀를 핵심 메커니즘으로 활용
- [동적 프로그래밍 (Dynamic Programming)](./dynamic_programming.md): 재귀 + 메모이제이션
- [트리 자료구조 (Tree)](./03_datastructure/binary_tree.md): 재귀 순회의 대표적 응용
- [깊이 우선 탐색 (DFS)](./02_graph/graph_algorithms.md): 그래프 재귀 탐색
- [호출 스택 (Call Stack)](../01_software_engineering/_index.md): 재귀의 실행 메커니즘

---

### 👶 어린이를 위한 3줄 비유 설명
1. 재귀는 **"러시아 인형"**과 같아요. 큰 인형을 열면 작은 인형이 나오고, 또 열면 더 작은 인형이 나오는 식이에요. 가장 작은 인형(Base Case)이 나올 때까지 계속 열어요.
2. 또는 **"이야기 속의 이야기"**라고 생각할 수 있어요. 영화 속 캐릭터가 또 다른 영화를 보고, 그 영화 속 캐릭터가 또 다른 영화를 보는 식이에요.
3. 컴퓨터는 이 "자기 자신을 부르는 마법"을 통해, 아주 복잡한 문제도 **"가장 작은 문제가 될 때까지 쪼개서"** 해결할 수 있답니다!
