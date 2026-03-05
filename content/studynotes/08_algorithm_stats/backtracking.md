+++
title = "백트래킹 (Backtracking): 유망하지 않은 경로의 조기 차단"
date = "2026-03-04"
[extra]
categories = "studynotes-algorithm-stats"
+++

# 백트래킹 (Backtracking): 유망하지 않은 경로의 조기 차단

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 백트래킹은 **상태 공간 트리(State Space Tree)**를 탐색하며, 제약 조건을 위반하는 **유망하지 않은(Promising하지 않은) 경로를 가지치기(Pruning)**하여 전체 탐색 공간을 획기적으로 축소하는 완전 탐색 기법입니다.
> 2. **가치**: N-Queens $O(n!)$, 스도쿠 $O(9^{n^2})$, 부분집합 $O(2^n)$ 등 지수 시간 문제에서 유망 함수를 통해 실제 실행 시간을 수십~수백 배 단축합니다.
> 3. **융합**: AI의 제약 충족 문제(CSP), 컴파일러의 타입 추론, 게임의 퍼즐 해법, 조합 최적화의 Branch & Bound 기반 기술입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 백트래킹의 정의와 작동 원리

백트래킹은 **"시도 → 검증 → 실패 시 되돌아감(Backtrack)"**의 반복으로 동작합니다. 핵심은 **가지치기(Pruning)**를 통해 불필요한 탐색을 조기에 차단하는 것입니다.

**핵심 구성 요소**:
1. **상태 공간 트리 (State Space Tree)**: 가능한 모든 선택을 트리로 표현
2. **유망 함수 (Promising Function)**: 현재 경로가 해로 이어질 수 있는지 판단
3. **제약 조건 (Constraints)**: 해가 만족해야 할 조건들

**알고리즘 구조**:
```
backtrack(state):
    if is_complete(state):
        return state  # 해 발견

    if not is_promising(state):
        return FAIL   # 가지치기

    for each candidate in get_candidates(state):
        new_state = apply(state, candidate)
        result = backtrack(new_state)
        if result != FAIL:
            return result
        undo(state, candidate)  # 백트래킹!

    return FAIL
```

#### 💡 비유: 미로에서 길 찾기
미로를 탈출할 때, 막다른 곳에 도달하면 되돌아가서(Backtrack) 다른 길을 시도합니다. 이때 "이 길은 벽으로 막혀있어서 더 갈 수 없다"고 판단하면 그 즉시 되돌아가고, 다른 모든 갈래길도 똑같이 시도하지 않습니다. 이것이 가지치기입니다. 모든 갈래길을 끝까지 가보는 것보다 훨씬 빠릅니다.

#### 2. 등장 배경 및 발전 과정
1. **D.H. Lehmer (1950s)**: 디지털 컴퓨터에서 백트래킹 개념 최초 적용.
2. **R.J. Walker (1960)**: "Backtracking" 용어 공식화.
3. **현대적 확장**: 제약 프로그래밍(CP), SAT 해법기, 게임 AI 등으로 발전.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 백트래킹 vs 완전 탐색 vs 분기 한정

| 특성 | 완전 탐색 (Brute Force) | 백트래킹 | 분기 한정 (B&B) |
|:---:|:---|:---|:---|
| **탐색 방식** | 모든 경우 수행 | 유망하지 않으면 중단 | 하한/상한 기반 중단 |
| **가지치기** | 없음 | 제약 기반 | 비용 기반 |
| **적용 문제** | 작은 입력 | 제약 충족 | 최적화 |
| **복잡도** | $O(b^d)$ | $O(b^d)$ but 실제 훨씬 빠름 | 최적해 근사 |

#### 2. 상태 공간 트리와 가지치기 다이어그램 (ASCII)

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                 BACKTRACKING: STATE SPACE TREE                          │
  └─────────────────────────────────────────────────────────────────────────┘

                              ┌─────────┐
                              │   Root  │
                              │  ( )    │
                              └────┬────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
            ┌────┴────┐      ┌────┴────┐      ┌────┴────┐
            │  (1)    │      │  (2)    │      │  (3)    │
            │ Promising│      │Promising│      │✗ Pruned │
            └────┬────┘      └────┬────┘      └─────────┘
                 │                 │
        ┌────────┼────────┐       │
        │        │        │       │
   ┌────┴───┐┌───┴────┐┌──┴────┐  │
   │ (1,2)  ││ (1,3)  ││(1,4)  │  │
   │✗Pruned ││Promising││Pruned│  │
   └────────┘└───┬────┘└───────┘  │
                 │                 │
            ┌────┴────┐       ┌────┴────┐
            │(1,3,2)  │       │(2,3)    │
            │Solution!│       │Promising│
            │✓ FOUND  │       └────┬────┘
            └─────────┘            │
                             ┌─────┴─────┐
                             │           │
                        ┌────┴────┐ ┌────┴────┐
                        │(2,3,1)  │ │(2,3,4)  │
                        │✗Pruned  │ │Solution!│
                        └─────────┘ └─────────┘

  범례:
  ┌─────────┐   ┌─────────┐   ┌─────────┐
  │Promising│   │✗ Pruned │   │✓ FOUND  │
  │계속 탐색 │   │가지치기  │   │해 발견   │
  └─────────┘   └─────────┘   └─────────┘

  ═══════════════════════════════════════════════════════════════════════════
  N-QUEENS EXAMPLE (N=4)
  ═══════════════════════════════════════════════════════════════════════════

  유망 함수: 같은 열, 같은 대각선에 퀸이 없어야 함

  State: [Q1행, Q2행, Q3행, Q4행]

  Level 0: []
  Level 1: [0], [1], [2], [3] - 모두 promising
  Level 2: [0,2], [0,3] - [0,0]✗, [0,1]✗ (같은 대각선)
  Level 3: [0,2,1], [0,2,3] - [0,2,0]✗, [0,2,2]✗
  Level 4: [0,2,1,3] - [0,2,1,0]✗, [0,2,1,2]✗, [0,2,1,3] ✓ SOLUTION!

  [0,2,1,3] = Q1은 0행, Q2는 2행, Q3은 1행, Q4는 3행

      0   1   2   3    ← 열
    ┌───┬───┬───┬───┐
  0 │ Q │   │   │   │
    ├───┼───┼───┼───┤
  1 │   │   │ Q │   │
    ├───┼───┼───┼───┤
  2 │   │ Q │   │   │
    ├───┼───┼───┼───┤
  3 │   │   │   │ Q │
    └───┴───┴───┴───┘
    ↑
  행
```

#### 3. 유망 함수 설계 원칙

| 문제 | 유망 함수 (Promising Function) | 제약 조건 |
|:---|:---|:---|
| **N-Queens** | 같은 열, 대각선에 다른 퀸 없음 | $|row_i - row_j| \neq |col_i - col_j|$ |
| **스도쿠** | 행, 열, 3x3 박스에 중복 없음 | 각 숫자 1회만 등장 |
| **부분집합 합** | 현재 합이 목표를 초과하지 않음 | $\sum \leq target$ |
| **순열 생성** | 중복 선택 없음 | 각 원소 1회만 선택 |
| **그래프 색칠** | 인접 정점 다른 색 | $color[u] \neq color[v]$ for $(u,v) \in E$ |

#### 4. 실무 코드 예시: 대표적 백트래킹 구현

```python
"""
백트래킹 대표 구현 모음
"""
from typing import List, Tuple, Optional, Set

# ============================================
# 1. N-Queens 문제
# ============================================

def n_queens(n: int) -> List[List[int]]:
    """
    N-Queens 문제 - 모든 해 반환

    Returns: 각 해는 [Q1행, Q2행, ..., Qn행] 형태
             Q(i)는 i열에 위치한 퀸의 행 번호
    """
    solutions = []

    def is_promising(queens: List[int], row: int, col: int) -> bool:
        """유망 함수: (row, col)에 퀸 배치 가능한가?"""
        for c in range(col):
            r = queens[c]
            # 같은 행
            if r == row:
                return False
            # 같은 대각선
            if abs(r - row) == abs(c - col):
                return False
        return True

    def backtrack(queens: List[int], col: int):
        """백트래킹: col열에 퀸 배치 시도"""
        if col == n:
            solutions.append(queens[:])  # 해 발견
            return

        for row in range(n):
            if is_promising(queens, row, col):
                queens.append(row)
                backtrack(queens, col + 1)
                queens.pop()  # 백트래킹!

    backtrack([], 0)
    return solutions

def print_chessboard(solution: List[int]) -> str:
    """체스판 시각화"""
    n = len(solution)
    board = []
    for col in range(n):
        row = ['Q' if r == solution[col] else '.' for r in range(n)]
        board.append(' '.join(row))
    return '\n'.join(board)

# ============================================
# 2. 스도쿠 해법기
# ============================================

def solve_sudoku(board: List[List[int]]) -> bool:
    """
    스도쿠 풀기 (in-place 수정)

    Args:
        board: 9x9 격자, 빈 칸은 0
    Returns:
        해 존재 여부
    """
    def is_valid(row: int, col: int, num: int) -> bool:
        """유망 함수: (row, col)에 num 배치 가능?"""
        # 행 검사
        if num in board[row]:
            return False

        # 열 검사
        if num in [board[r][col] for r in range(9)]:
            return False

        # 3x3 박스 검사
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if board[r][c] == num:
                    return False

        return True

    def find_empty() -> Optional[Tuple[int, int]]:
        """빈 칸 찾기"""
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return (r, c)
        return None

    def backtrack() -> bool:
        empty = find_empty()
        if empty is None:
            return True  # 해 완성

        row, col = empty
        for num in range(1, 10):
            if is_valid(row, col, num):
                board[row][col] = num
                if backtrack():
                    return True
                board[row][col] = 0  # 백트래킹!

        return False

    return backtrack()

# ============================================
# 3. 부분집합 합 (Subset Sum)
# ============================================

def subset_sum(nums: List[int], target: int) -> List[List[int]]:
    """
    부분집합 합 문제 - 합이 target인 모든 부분집합
    """
    solutions = []

    def backtrack(start: int, current: List[int], current_sum: int):
        # 가지치기: 현재 합이 목표 초과
        if current_sum > target:
            return

        # 해 발견
        if current_sum == target:
            solutions.append(current[:])
            return

        # 추가 탐색
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current, current_sum + nums[i])
            current.pop()  # 백트래킹!

    backtrack(0, [], 0)
    return solutions

# ============================================
# 4. 순열 생성
# ============================================

def permutations_backtrack(nums: List[int]) -> List[List[int]]:
    """
    모든 순열 생성 (백트래킹)
    """
    result = []

    def backtrack(current: List[int], remaining: List[int]):
        if not remaining:
            result.append(current[:])
            return

        for i in range(len(remaining)):
            current.append(remaining[i])
            backtrack(current, remaining[:i] + remaining[i+1:])
            current.pop()  # 백트래킹!

    backtrack([], nums)
    return result

# ============================================
# 5. 조합 생성
# ============================================

def combinations_backtrack(n: int, k: int) -> List[List[int]]:
    """
    n개에서 k개 선택하는 모든 조합
    """
    result = []

    def backtrack(start: int, current: List[int]):
        if len(current) == k:
            result.append(current[:])
            return

        for i in range(start, n + 1):
            current.append(i)
            backtrack(i + 1, current)
            current.pop()  # 백트래킹!

    backtrack(1, [])
    return result

# ============================================
# 6. 미로 탈출 (격자)
# ============================================

def solve_maze(maze: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    미로 탈출 경로 찾기

    Args:
        maze: 0=통로, 1=벽
        start: 시작 좌표
        end: 도착 좌표
    Returns:
        경로 리스트 또는 None
    """
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 우, 하, 좌, 상

    def is_valid(r: int, c: int, visited: Set) -> bool:
        return (0 <= r < rows and 0 <= c < cols and
                maze[r][c] == 0 and (r, c) not in visited)

    def backtrack(pos: Tuple[int, int], path: List[Tuple[int, int]], visited: Set) -> Optional[List[Tuple[int, int]]]:
        if pos == end:
            return path[:]

        r, c = pos
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc, visited):
                visited.add((nr, nc))
                path.append((nr, nc))

                result = backtrack((nr, nc), path, visited)
                if result:
                    return result

                path.pop()
                visited.remove((nr, nc))  # 백트래킹!

        return None

    visited = {start}
    return backtrack(start, [start], visited)

# ============================================
# 7. 그래프 색칠 (Graph Coloring)
# ============================================

def graph_coloring(graph: List[List[int]], m: int) -> Optional[List[int]]:
    """
    m개의 색으로 그래프 색칠하기

    Args:
        graph: 인접 행렬
        m: 색 개수
    Returns:
        각 정점의 색 (0~m-1) 또는 None
    """
    n = len(graph)
    colors = [-1] * n

    def is_safe(vertex: int, color: int) -> bool:
        """유망 함수: vertex에 color 사용 가능?"""
        for i in range(n):
            if graph[vertex][i] == 1 and colors[i] == color:
                return False
        return True

    def backtrack(vertex: int) -> bool:
        if vertex == n:
            return True  # 모든 정점 색칠 완료

        for color in range(m):
            if is_safe(vertex, color):
                colors[vertex] = color
                if backtrack(vertex + 1):
                    return True
                colors[vertex] = -1  # 백트래킹!

        return False

    if backtrack(0):
        return colors
    return None

# ============================================
# 8. 단어 검색 (Word Search)
# ============================================

def word_search(board: List[List[str]], word: str) -> bool:
    """
    격자에서 단어 찾기 (인접 칸 이동)
    """
    rows, cols = len(board), len(board[0])

    def backtrack(r: int, c: int, index: int, visited: Set) -> bool:
        if index == len(word):
            return True

        if (r < 0 or r >= rows or c < 0 or c >= cols or
            (r, c) in visited or board[r][c] != word[index]):
            return False

        visited.add((r, c))

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if backtrack(r + dr, c + dc, index + 1, visited):
                return True

        visited.remove((r, c))  # 백트래킹!
        return False

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0]:
                if backtrack(r, c, 0, set()):
                    return True

    return False

# ============================================
# 테스트
# ============================================

if __name__ == "__main__":
    print("=== N-Queens (N=4) ===")
    solutions = n_queens(4)
    print(f"해 개수: {len(solutions)}")
    for i, sol in enumerate(solutions[:2]):
        print(f"\n해 {i+1}: {sol}")
        print(print_chessboard(sol))

    print("\n=== 스도쿠 ===")
    sudoku = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    if solve_sudoku(sudoku):
        for row in sudoku:
            print(row)

    print("\n=== 부분집합 합 ===")
    print(f"subset_sum([1,2,3,4,5], 7): {subset_sum([1,2,3,4,5], 7)}")

    print("\n=== 순열 ===")
    print(f"permutations([1,2,3]): {permutations_backtrack([1,2,3])}")

    print("\n=== 그래프 색칠 ===")
    graph = [
        [0, 1, 1, 1],
        [1, 0, 1, 0],
        [1, 1, 0, 1],
        [1, 0, 1, 0]
    ]
    colors = graph_coloring(graph, 3)
    print(f"3색 색칠 결과: {colors}")

    print("\n=== 단어 검색 ===")
    board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']]
    print(f"word_search(board, 'ABCCED'): {word_search(board, 'ABCCED')}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 백트래킹 vs 분기 한정 비교

| 특성 | 백트래킹 | 분기 한정 (Branch & Bound) |
|:---:|:---|:---|
| **목표** | 모든 해 또는 하나의 해 | 최적해 (최대/최소) |
| **가지치기 기준** | 제약 조건 위반 | 상한/하한 기반 |
| **탐색 순서** | DFS (주로) | Best-First (우선순위) |
| **적용 문제** | N-Queens, 스도쿠 | TSP, 배낭(최적화) |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 백트래킹 적용 체크리스트
- [ ] 상태 공간이 트리로 표현 가능한가?
- [ ] 유망 함수를 정의할 수 있는가?
- [ ] 제약 조건이 명확한가?
- [ ] 백트래킹 오버헤드가 무작위 탐색보다 작은가?

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 구분 | 효과 |
|:---:|:---|
| **정량적** | 탐색 공간 수십~수백 배 축소 |
| **정성적** | 조합 문제의 체계적 해결 |

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [분기 한정 (Branch and Bound)](./branch_and_bound.md): 최적화 문제로 확장.
- [재귀 (Recursion)](./recursion.md): 백트래킹의 구현 수단.
- [DFS (깊이 우선 탐색)](./02_graph/dfs.md): 백트래킹의 탐색 방식.
- [동적 프로그래밍](./dynamic_programming.md): 메모이제이션 기반 최적화.
- [NP 완전성](./05_complexity/np_complete.md): 백트래킹이 필요한 문제들.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 백트래킹은 **"미로에서 막다른 길을 만나면 되돌아가서 다른 길을 찾는 것"**이에요.
2. "이 길은 절대 출구로 안 이어져!"라고 **미리 알면 그 길은 아예 안 가도 돼요**.
3. 이렇게 **안 봐도 되는 길을 미리 차단**해서 훨씬 빨리 탈출해요!
