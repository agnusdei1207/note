+++
title = "분기 한정 (Branch and Bound): 최적화 문제의 지능적 탐색"
date = "2026-03-04"
[extra]
categories = "studynotes-algorithm-stats"
+++

# 분기 한정 (Branch and Bound): 최적화 문제의 지능적 탐색

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분기 한정은 상태 공간 트리를 탐색하며 **하한(Lower Bound)과 상한(Upper Bound)**을 계산하여, 현재 최적해보다 나쁠 수 없는 노드만 탐색하는 **최적화 문제 해결 기법**입니다.
> 2. **가치**: TSP, 정수 프로그래밍, 배낭 문제 등 NP-hard 최적화 문제에서 완전 탐색 대비 수천 배 빠른 수행 시간을 달성하며, **최적해를 보장**합니다.
> 3. **융합**: 운영 연구(OR), 공급망 최적화, 스케줄링, 자원 배분 등 실제 산업 최적화 문제의 핵심 해법입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 분기 한정의 정의와 작동 원리

분기 한정(Branch and Bound, B&B)은 1960년대 A.H. Land와 A.G. Doig가 개발한 알고리즘으로, **분기(Branch)**와 **한정(Bound)**의 두 가지 연산으로 구성됩니다.

**핵심 연산**:
1. **분기 (Branching)**: 문제를 더 작은 부분 문제로 분할
2. **한정 (Bounding)**: 각 부분 문제의 해에 대한 하한/상한 계산
3. **가지치기 (Pruning)**: 한정값이 현재 최적해보다 나쁜 노드 제외

**백트래킹 vs 분기 한정**:
- **백트래킹**: 제약 조건 위반 시 가지치기 (feasibility)
- **분기 한정**: 비용 기반 가지치기 (optimality)

#### 💡 비유: 가격 제한 있는 쇼핑
100만 원 예산으로 최고의 노트북을 찾는다고 가정해 봅시다. 모든 매장을 다 돌지 않고, 온라인으로 최저가를 먼저 확인합니다. 어떤 매장이 "최저가가 120만 원 이상"이라면 그 매장은 아예 방문하지 않습니다(한정). 이렇게 **가격 상한을 미리 파악해서 불필요한 방문을 줄이는 것**이 분기 한정입니다.

#### 2. 등장 배경 및 발전 과정
1. **Land & Doig (1960)**: 정수 선형 계획법을 위한 최초의 B&B 알고리즘.
2. **Little et al. (1963)**: TSP에 B&B 적용.
3. **현대적 발전**: CPLEX, Gurobi 등 상용 최적화 소프트웨어의 핵심 엔진.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 분기 한정 구조

| 구성 요소 | 설명 | 예시 (TSP) |
|:---:|:---|:---|
| **분기 규칙** | 부분 문제 분할 방법 | 특정 간선 포함/제외 |
| **한정 함수** | 하한/상한 계산 | MST 비용, 최소 간선 합 |
| **선택 규칙** | 다음 탐색 노드 선택 | BFS, DFS, Best-First |
| **가지치기** | 탐색 중단 조건 | bound > best_known |

#### 2. 분기 한정 실행 다이어그램 (ASCII)

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                BRANCH AND BOUND EXECUTION FLOW                          │
  └─────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────┐
                    │         Priority Queue          │
                    │   (노드들을 bound 기준 정렬)    │
                    └────────────────┬────────────────┘
                                     │
                                     ▼
                    ┌─────────────────────────────────┐
                    │     1. 노드 선택 (Pop)          │
                    │    Best-First: 최소 bound 선택  │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
            ┌───────────────┐                 ┌───────────────┐
            │ 2. 한정 계산   │                 │  해 완성?     │
            │   Bound(node) │                 │               │
            └───────┬───────┘                 └───────┬───────┘
                    │                                 │
                    ▼                                 │
            ┌───────────────┐                        │
            │ Bound >= best?│                        │
            │               │                        │
            └───────┬───────┘                        │
                    │                                │
            ┌───────┴───────┐                Yes    │
            │               │                  ▼     │
        Yes ▼           No  ▼          ┌──────────┐ │
    ┌─────────────┐ ┌─────────────┐    │해 갱신   │ │
    │  PRUNE      │ │ 3. 분기     │    │best=cost│ │
    │  (가지치기)  │ │ (자식 생성) │    └──────────┘ │
    └─────────────┘ └──────┬──────┘                 │
                           │                        │
                           ▼                        │
                    ┌───────────────┐               │
                    │ 자식들을      │               │
                    │ 큐에 추가     │◄──────────────┘
                    └───────────────┘

  ═══════════════════════════════════════════════════════════════════════════
  TSP BRANCH AND BOUND EXAMPLE
  ═══════════════════════════════════════════════════════════════════════════

  그래프: 4개 도시 (0,1,2,3)

         0 ───10── 1
         │╲      ╱ │
        15╲ ╲  ╱  ╱25
         │  ╲╳╱   │
        30  ╱╲   35
         │╱    ╲ │
         3───20──2

  간선 비용:
  0-1:10, 0-3:15, 0-2:30
  1-2:35, 1-3:25
  2-3:20

  분기: 간선 (0,1)을 포함하거나 제외

  ┌──────────────────────────────────────────────────────────────────┐
  │                        Root Node                                 │
  │  Bound = MST 비용 + 최소 진입/진출 간선들의 조정                  │
  │  Bound ≈ 10+15+20+25 = 70 (lower bound)                         │
  └───────────────────────────┬──────────────────────────────────────┘
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
  ┌────────────────────────┐    ┌────────────────────────┐
  │  Include edge (0,1)    │    │  Exclude edge (0,1)    │
  │  Bound: 75             │    │  Bound: 80             │
  │  (유망함, 계속 탐색)    │    │  (유망함, 계속 탐색)    │
  └───────────┬────────────┘    └────────────────────────┘
              │
    ┌─────────┴─────────┐
    ▼                   ▼
  ┌─────────────────┐  ┌─────────────────┐
  │ Include (1,2)   │  │ Exclude (1,2)   │
  │ Bound: 85       │  │ Bound: 78       │
  │ (best=80보다 큼)│  │ (유망함)        │
  │ ✗ PRUNED        │  │ ...             │
  └─────────────────┘  └─────────────────┘

  최종 최적해: 0-1-3-2-0 = 10+25+20+30 = 85
  (실제로는 더 정교한 한정 함수 사용)
```

#### 3. 한정 함수 (Bounding Function) 설계

| 문제 유형 | 하한 계산법 | 설명 |
|:---|:---|:---|
| **TSP** | MST 기반 | 미방문 도시들의 MST 비용 + 연결 간선 |
| **배낭 (0/1)** | 선형 완화 | 분할 배낭 문제의 해를 하한으로 |
| **정수 계획** | LP 완화 | 연속 변수 허용한 LP 해 |
| **Job Scheduling** | 최소 완료 시간 | 남은 작업들의 최소 처리 시간 |

#### 4. 실무 코드 예시: 분기 한정 구현

```python
"""
분기 한정 (Branch and Bound) 구현 모음
"""
from typing import List, Tuple, Optional
from dataclasses import dataclass, field
import heapq
import copy

# ============================================
# 1. 0/1 배낭 문제 (Branch and Bound)
# ============================================

@dataclass
class KnapsackNode:
    """배낭 문제의 탐색 노드"""
    level: int          # 현재 아이템 인덱스
    value: int          # 현재 가치
    weight: int         # 현재 무게
    bound: float        # 상한 (linear relaxation)
    items: List[int] = field(default_factory=list)

    def __lt__(self, other):
        # 최대 힙을 위해 음수 비교
        return self.bound > other.bound

def knapsack_branch_bound(values: List[int], weights: List[int], capacity: int) -> Tuple[int, List[int]]:
    """
    0/1 배낭 문제 - Branch and Bound

    Returns: (최대 가치, 선택된 아이템 인덱스)
    """
    n = len(values)
    items = [(v, w, i) for i, (v, w) in enumerate(zip(values, weights))]
    items.sort(key=lambda x: x[0]/x[1] if x[1] > 0 else 0, reverse=True)

    def calculate_bound(node: KnapsackNode) -> float:
        """상한 계산: Linear Relaxation"""
        if node.weight >= capacity:
            return 0

        bound = node.value
        weight = node.weight
        level = node.level

        # 남은 아이템들을 단위 가치 순으로 추가
        while level < n and weight + items[level][1] <= capacity:
            weight += items[level][1]
            bound += items[level][0]
            level += 1

        # 분할 가능한 마지막 아이템
        if level < n:
            bound += (capacity - weight) * items[level][0] / items[level][1]

        return bound

    # Best-First Search (우선순위 큐)
    pq = []
    root = KnapsackNode(level=0, value=0, weight=0, bound=calculate_bound(KnapsackNode(0, 0, 0, 0)))
    heapq.heappush(pq, root)

    max_value = 0
    best_items = []

    while pq:
        node = heapq.heappop(pq)

        # 가지치기: 상한이 현재 최적해보다 작거나 같음
        if node.bound <= max_value:
            continue

        if node.level >= n:
            continue

        v, w, idx = items[node.level]

        # 선택하는 경우
        left = KnapsackNode(
            level=node.level + 1,
            value=node.value + v,
            weight=node.weight + w,
            bound=0,
            items=node.items + [idx]
        )
        left.bound = calculate_bound(left)

        if left.weight <= capacity:
            if left.value > max_value:
                max_value = left.value
                best_items = left.items
            if left.bound > max_value:
                heapq.heappush(pq, left)

        # 선택하지 않는 경우
        right = KnapsackNode(
            level=node.level + 1,
            value=node.value,
            weight=node.weight,
            bound=0,
            items=node.items[:]
        )
        right.bound = calculate_bound(right)

        if right.bound > max_value:
            heapq.heappush(pq, right)

    return max_value, sorted(best_items)

# ============================================
# 2. TSP (Traveling Salesman Problem)
# ============================================

@dataclass
class TSPNode:
    """TSP 탐색 노드"""
    path: List[int]         # 현재까지의 경로
    cost: int               # 현재 비용
    bound: float            # 하한

    def __lt__(self, other):
        return self.bound < other.bound

def tsp_branch_bound(dist: List[List[int]]) -> Tuple[int, List[int]]:
    """
    TSP - Branch and Bound

    Args:
        dist: 거리 행렬 (dist[i][j] = i→j 비용)
    Returns:
        (최소 비용, 최적 경로)
    """
    n = len(dist)

    def calculate_bound(node: TSPNode) -> float:
        """하한 계산: 각 도시의 최소 진입/진출 간선 합"""
        bound = node.cost

        # 미방문 도시들의 최소 간선 비용
        visited = set(node.path)

        for i in range(n):
            if i in visited and i != node.path[-1]:
                continue

            min_out = float('inf')
            for j in range(n):
                if j not in visited or j == node.path[0]:
                    if i != j:
                        min_out = min(min_out, dist[i][j])

            if min_out != float('inf'):
                bound += min_out

        return bound

    pq = []
    start = 0
    root = TSPNode(path=[start], cost=0, bound=calculate_bound(TSPNode([start], 0, 0)))
    heapq.heappush(pq, root)

    min_cost = float('inf')
    best_path = []

    while pq:
        node = heapq.heappop(pq)

        # 가지치기
        if node.bound >= min_cost:
            continue

        # 모든 도시 방문 완료
        if len(node.path) == n:
            # 시작점으로 복귀
            total = node.cost + dist[node.path[-1]][start]
            if total < min_cost:
                min_cost = total
                best_path = node.path + [start]
            continue

        # 분기: 다음 도시 선택
        current = node.path[-1]
        for next_city in range(n):
            if next_city not in node.path:
                new_cost = node.cost + dist[current][next_city]
                new_path = node.path + [next_city]
                child = TSPNode(path=new_path, cost=new_cost, bound=0)
                child.bound = calculate_bound(child)

                if child.bound < min_cost:
                    heapq.heappush(pq, child)

    return min_cost, best_path

# ============================================
# 3. Job Scheduling (최소 완료 시간)
# ============================================

@dataclass
class ScheduleNode:
    """스케줄링 노드"""
    schedule: List[int]     # 작업 순서
    completion_time: int    # 완료 시간
    bound: float            # 하한

    def __lt__(self, other):
        return self.bound < other.bound

def job_scheduling_branch_bound(
    processing_times: List[int],
    num_machines: int = 1
) -> Tuple[int, List[int]]:
    """
    단일 기계 스케줄링 - 총 완료 시간 최소화

    Returns: (최소 완료 시간, 작업 순서)
    """
    n = len(processing_times)

    def calculate_bound(node: ScheduleNode) -> float:
        """하한: 현재 완료 시간 + 남은 작업들"""
        remaining = [processing_times[i] for i in range(n) if i not in node.schedule]
        return node.completion_time + sum(remaining)

    pq = []
    root = ScheduleNode(schedule=[], completion_time=0, bound=calculate_bound(ScheduleNode([], 0, 0)))
    heapq.heappush(pq, root)

    min_time = float('inf')
    best_schedule = []

    while pq:
        node = heapq.heappop(pq)

        if node.bound >= min_time:
            continue

        if len(node.schedule) == n:
            if node.completion_time < min_time:
                min_time = node.completion_time
                best_schedule = node.schedule
            continue

        for job in range(n):
            if job not in node.schedule:
                new_completion = node.completion_time + processing_times[job] * (len(node.schedule) + 1)
                child = ScheduleNode(
                    schedule=node.schedule + [job],
                    completion_time=node.completion_time + processing_times[job],
                    bound=0
                )
                child.bound = calculate_bound(child)

                if child.bound < min_time:
                    heapq.heappush(pq, child)

    return min_time, best_schedule

# ============================================
# 4. 정수 분할 (Integer Partition)
# ============================================

def integer_knapsack(values: List[int], weights: List[int], capacity: int) -> int:
    """
    정수 배낭 (각 아이템 무제한 선택 가능) - Branch and Bound
    """
    n = len(values)
    best_value = [0]

    def calculate_bound(level: int, current_value: int, current_weight: int) -> float:
        if current_weight >= capacity:
            return 0

        bound = current_value
        weight = current_weight

        for i in range(level, n):
            if weights[i] == 0:
                continue
            max_count = (capacity - weight) // weights[i]
            bound += max_count * values[i]
            weight += max_count * weights[i]

            if weight >= capacity:
                break

        return bound

    def branch_and_bound(level: int, current_value: int, current_weight: int):
        if current_weight > capacity:
            return

        if current_value > best_value[0]:
            best_value[0] = current_value

        if level >= n:
            return

        # 가지치기
        bound = calculate_bound(level, current_value, current_weight)
        if bound <= best_value[0]:
            return

        # 현재 아이템 선택 (0개부터 최대 가능 개수까지)
        max_count = (capacity - current_weight) // weights[level] if weights[level] > 0 else 0

        for count in range(max_count, -1, -1):  # 큰 값부터 (best-first)
            new_weight = current_weight + count * weights[level]
            new_value = current_value + count * values[level]
            branch_and_bound(level + 1, new_value, new_weight)

    branch_and_bound(0, 0, 0)
    return best_value[0]

# ============================================
# 테스트
# ============================================

if __name__ == "__main__":
    print("=== 0/1 배낭 (Branch and Bound) ===")
    values = [60, 100, 120]
    weights = [10, 20, 30]
    capacity = 50
    result, items = knapsack_branch_bound(values, weights, capacity)
    print(f"최대 가치: {result}, 선택 아이템: {items}")

    print("\n=== TSP (Branch and Bound) ===")
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    cost, path = tsp_branch_bound(dist)
    print(f"최소 비용: {cost}, 경로: {path}")

    print("\n=== Job Scheduling ===")
    times = [3, 1, 4, 2]
    min_time, schedule = job_scheduling_branch_bound(times)
    print(f"최소 완료 시간: {min_time}, 순서: {schedule}")

    print("\n=== 정수 배낭 ===")
    result = integer_knapsack(values, weights, capacity)
    print(f"정수 배낭 최대 가치: {result}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 탐색 전략 비교

| 전략 | 설명 | 장점 | 단점 |
|:---:|:---|:---|:---|
| **DFS** | 깊이 우선 | 메모리 효율 | 최적해 늦게 발견 가능 |
| **BFS** | 너비 우선 | 최단 경로 보장 | 메모리 많이 사용 |
| **Best-First** | bound 기반 | 빠른 최적해 발견 | 우선순위 큐 오버헤드 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 분기 한정 적용 체크리스트
- [ ] 최적화 문제인가? (max/min)
- [ ] 효과적인 한정 함수를 설계할 수 있는가?
- [ ] 탐색 공간이 적절한가?
- [ ] 근사 알고리즘으로 충분하지 않은가?

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 구분 | 효과 |
|:---:|:---|
| **정량적** | 완전 탐색 대비 수천 배 빠른 수행 |
| **정성적** | 최적해 보장 |

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [백트래킹 (Backtracking)](./backtracking.md): 제약 기반 탐색.
- [근사 알고리즘](./approximation_algorithm.md): 빠른 근사해 필요 시.
- [정수 프로그래밍](./09_optimization/integer_programming.md): OR의 핵심.
- [TSP](./02_graph/tsp.md): 대표적 NP-hard 문제.
- [힙 (Heap)](./03_datastructure/heap.md): 우선순위 큐 구현.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 분기 한정은 **"예산을 정해놓고 쇼핑하는 방법"**이에요.
2. "이 매장은 물건이 다 너무 비싸서 예산을 넘어!"라고 **미리 알면 안 가도 돼요**.
3. 이렇게 **안 가도 되는 곳을 미리 차단**해서 빠르고 똑똑하게 쇼핑해요!
