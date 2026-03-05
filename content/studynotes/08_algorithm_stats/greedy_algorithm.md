+++
title = "탐욕 알고리즘 (Greedy Algorithm): 지역 최적의 누적과 전역 최적의 기회"
date = "2026-03-04"
[extra]
categories = "studynotes-algorithm-stats"
+++

# 탐욕 알고리즘 (Greedy Algorithm): 지역 최적의 누적과 전역 최적의 기회

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 탐욕 알고리즘은 각 단계에서 **현재 상태 기준으로 최선의 선택(Local Optimum)**을 반복하여, 결과적으로 전체 문제의 최적해(Global Optimum)에 도달하는 알고리즘 설계 패러다임입니다.
> 2. **가치**: 백트래킹이나 동적 프로그래밍 대비 **구현의 단순성과 실행 효율성**이 뛰어나며, 최적 부분구조와 탐욕 선택 속성을 만족하는 문제에서 선형 또는 선형 로그 시간 복잡도를 달성합니다.
> 3. **융합**: 최소 신장 트리(Kruskal, Prim), 최단 경로(Dijkstra), 허프만 코딩, 스케줄링 등 핵심 CS 문제들의 기반이 되며, AI/ML의 의사결정 휴리스틱으로도 확장됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 탐욕 알고리즘의 정의와 작동 조건

탐욕 알고리즘은 "매 순간 가장 좋아 보이는 선택을 하라"는 전략입니다. 하지만 모든 문제에 적용할 수 있는 것은 아니며, 두 가지 핵심 조건이 필요합니다.

**① 탐욕 선택 속성 (Greedy Choice Property)**
- 지역적 최적 선택이 전역적 최적해의 일부가 되는 성질
- 이전 선택이 이후 선택에 영향을 주지 않음
- "한 번의 탐욕적 선택이 최적해를 해치지 않는다"

**② 최적 부분구조 (Optimal Substructure)**
- 문제의 최적해가 부분 문제들의 최적해로 구성됨
- "큰 문제의 최적해 안에 작은 문제의 최적해가 포함된다"

**탐욕 알고리즘 vs 동적 프로그래밍 비교**:
- **DP**: 모든 부분문제의 해를 저장하고, 이후 선택에서 활용
- **Greedy**: 이전 선택을 되돌아보지 않고, 현재만 바라봄

#### 💡 비유: 자판기에서 거스름돈 주기
1,500원짜리 음료를 5,000원에 샀을 때 3,500원 거스름돈을 준다고 가정합시다. 탐욕적 방법은 "가장 큰 동전부터"입니다: 1,000원 × 3 + 500원 × 1 = 3,500원. 이것이 최소 동전 개수입니다. 이것이 가능한 이유는 한국 동전 체계(1, 5, 10, 50, 100, 500)가 탐욕 조건을 만족하기 때문입니다. 반면 4원, 3원, 1원 동전 체계에서 6원을 만들 때, 탐욕법은 4+1+1=3개이지만, 실제 최적은 3+3=2개입니다.

#### 2. 등장 배경 및 발전 과정
1. **초기 형태**: 1950년대 활동 선택 문제(Activity Selection)에서 최초 체계적 분석.
2. **최소 신장 트리**: Kruskal(1956), Prim(1957) 알고리즘이 탐욕법의 대표 성공 사례.
3. **정보 이론**: 허프만 코딩(1952)이 데이터 압축의 기초 확립.
4. **현대적 확장**: 근사 알고리즘, 휴리스틱 탐색, 게임 AI로 확장.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 탐욕 알고리즘 분류표

| 알고리즘 | 문제 유형 | 탐욕 선택 기준 | 시간 복잡도 | 정확성 보장 |
|:---:|:---|:---|:---:|:---:|
| **거스름돈** | 동전 교환 | 최대 액면가 | $O(n)$ | 조건부 |
| **활동 선택** | 구간 스케줄링 | 최소 종료 시간 | $O(n \log n)$ | Yes |
| **크루스칼** | MST | 최소 가중치 간선 | $O(E \log E)$ | Yes |
| **프림** | MST | 최소 가중치 연결 | $O(E \log V)$ | Yes |
| **다익스트라** | 최단 경로 | 최소 거리 정점 | $O((V+E) \log V)$ | Yes (비음수) |
| **허프만** | 무손실 압축 | 최소 빈도 결합 | $O(n \log n)$ | Yes |
| **배낭 문제(분할)** | 최적화 | 최대 단위 가치 | $O(n \log n)$ | Yes |
| **배낭 문제(0/1)** | 최적화 | 최대 가치 | - | No (근사만) |

#### 2. 탐욕 알고리즘 구조 다이어그램 (ASCII)

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    GREEDY ALGORITHM EXECUTION FLOW                      │
  └─────────────────────────────────────────────────────────────────────────┘

                          ┌───────────────────┐
                          │    Problem(n)     │
                          │   Candidates: C   │
                          └─────────┬─────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
            ┌───────────────────────────────────────────┐
            │           SELECTION PHASE                  │
            │   ┌─────────────────────────────────────┐ │
            │   │  1. Evaluate all candidates         │ │
            │   │  2. Select locally optimal choice   │ │
            │   │  3. criterion = max/min value       │ │
            │   └─────────────────────────────────────┘ │
            └───────────────────┬───────────────────────┘
                                │
                    ┌───────────┼───────────┐
                    │  FEASIBILITY CHECK    │
                    │  Is selection valid?  │
                    └───────────┬───────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                Yes ▼                   No ▼
            ┌─────────────┐         ┌─────────────┐
            │   ADD to    │         │   DISCARD   │
            │  Solution   │         │  candidate  │
            └──────┬──────┘         └──────┬──────┘
                   │                       │
                   └───────────┬───────────┘
                               │
                    ┌──────────┴──────────┐
                    │  More candidates?   │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                Yes ▼                  No ▼
            ┌─────────────┐        ┌─────────────┐
            │  Continue   │        │   OUTPUT    │
            │   Loop      │        │  Solution   │
            └─────────────┘        └─────────────┘

  ═══════════════════════════════════════════════════════════════════════════
  KRUSKAL MST EXAMPLE
  ═══════════════════════════════════════════════════════════════════════════

  Graph:                    Sorted Edges (Greedy Order):
       A -----4----- B       1. (D,E) weight=2  ✓
       |\           /|       2. (B,D) weight=3  ✓
       | \         / |       3. (A,B) weight=4  ✓
       8  2       1  6       4. (C,E) weight=5  ✓ [MST 완성]
       |   \     /   |       5. (B,C) weight=6  ✗ [사이클 발생]
       |    \   /    |       6. (A,D) weight=8  ✗ [사이클 발생]
       C-----5---E    D

  MST Result: A-B-C-E-D with total weight = 4+6+5+2 = 17
  (Actually: A-B(4) + B-D(3) + D-E(2) + C-E(5) = 14)

  Greedy Choice: 항상 가중치가 가장 작은 간선 선택
  Feasibility: Union-Find로 사이클 검사
```

#### 3. 탐욕 알고리즘 정당성 증명 기법

**① 탐욕 선택 속성 증명 (Exchange Argument)**
- 임의의 최적해 $O$가 존재한다고 가정
- $O$의 첫 번째 선택을 탐욕적 선택 $g$로 교환
- 교환 후에도 여전히 최적해임을 증명

**② 최적 부분구조 증명 (Cut-and-Paste)**
- 최적해가 부분 문제의 최적해를 포함함을 증명
- 부분 문제의 비최적해를 가정하여 모순 유도

**③ 매트로이드 이론 (Matroid Theory)**
- 문제가 매트로이드 구조를 가지면 탐욕법이 항상 최적
- 예: 최소 신장 트리, 작업 스케줄링

#### 4. 실무 코드 예시: 대표적 탐욕 알고리즘 구현

```python
"""
탐욕 알고리즘 대표 구현 모음
"""
from typing import List, Tuple, Optional
from dataclasses import dataclass
import heapq

# ============================================
# 1. 활동 선택 문제 (Activity Selection)
# ============================================

@dataclass
class Activity:
    name: str
    start: int
    finish: int

def activity_selection(activities: List[Activity]) -> List[Activity]:
    """
    활동 선택 문제 - O(n log n)
    탐욕 선택: 가장 먼저 끝나는 활동 선택

    증명 (Exchange Argument):
    - 최적해 OPT의 첫 번째 활동이 a1, 탐욕적 선택이 g1
    - finish(g1) ≤ finish(a1) (탐욕적 선택 정의)
    - a1을 g1으로 교환해도 여전히 최적해
    """
    # 종료 시간 기준 정렬
    sorted_activities = sorted(activities, key=lambda a: a.finish)

    selected = [sorted_activities[0]]
    last_finish = sorted_activities[0].finish

    for activity in sorted_activities[1:]:
        if activity.start >= last_finish:
            selected.append(activity)
            last_finish = activity.finish

    return selected

# ============================================
# 2. 크루스칼 MST 알고리즘
# ============================================

class UnionFind:
    """Union-Find (Disjoint Set Union) - Kruskal에 필수"""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 경로 압축
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """두 집합을 합침. 사이클이면 False 반환"""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # 이미 같은 집합 (사이클)

        # 랭크 기반 합치기
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

@dataclass
class Edge:
    u: int
    v: int
    weight: int

def kruskal_mst(n: int, edges: List[Edge]) -> Tuple[List[Edge], int]:
    """
    Kruskal MST - O(E log E)
    탐욕 선택: 가중치가 가장 작은 간선 선택

    정당성: MST 문제는 매트로이드 구조를 가짐
    """
    # 간선을 가중치 기준 정렬
    sorted_edges = sorted(edges, key=lambda e: e.weight)

    uf = UnionFind(n)
    mst_edges = []
    total_weight = 0

    for edge in sorted_edges:
        if uf.union(edge.u, edge.v):
            mst_edges.append(edge)
            total_weight += edge.weight

            if len(mst_edges) == n - 1:
                break  # MST 완성

    return mst_edges, total_weight

# ============================================
# 3. 다익스트라 최단 경로
# ============================================

def dijkstra(n: int, graph: List[List[Tuple[int, int]]], start: int) -> List[int]:
    """
    다익스트라 최단 경로 - O((V + E) log V)
    탐욕 선택: 현재 최소 거리의 정점 선택

    정당성:
    - 음수 간선이 없을 때만 보장
    - 선택된 정점의 거리는 확정 (더 이상 갱신되지 않음)
    """
    INF = float('inf')
    dist = [INF] * n
    dist[start] = 0

    # (거리, 정점) 힙
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)

        # 이미 처리된 정점 스킵
        if d > dist[u]:
            continue

        for v, weight in graph[u]:
            new_dist = dist[u] + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    return dist

# ============================================
# 4. 허프만 코딩
# ============================================

@dataclass
class HuffmanNode:
    char: Optional[str]
    freq: int
    left: Optional['HuffmanNode'] = None
    right: Optional['HuffmanNode'] = None

    def __lt__(self, other):
        return self.freq < other.freq

def huffman_coding(char_freq: dict) -> Tuple[HuffmanNode, dict]:
    """
    허프만 코딩 - O(n log n)
    탐욕 선택: 최소 빈도의 두 노드 결합

    정당성: 최적 접두사 코드를 생성하는 것이 증명됨
    """
    # 리프 노드 생성
    heap = [HuffmanNode(char=c, freq=f) for c, f in char_freq.items()]
    heapq.heapify(heap)

    # 트리 구성
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = HuffmanNode(
            char=None,
            freq=left.freq + right.freq,
            left=left,
            right=right
        )
        heapq.heappush(heap, merged)

    root = heap[0]

    # 코드 생성
    codes = {}
    def generate_codes(node: HuffmanNode, code: str):
        if node.char is not None:
            codes[node.char] = code
            return
        if node.left:
            generate_codes(node.left, code + '0')
        if node.right:
            generate_codes(node.right, code + '1')

    generate_codes(root, '')

    return root, codes

# ============================================
# 5. 분할 가능 배낭 문제 (Fractional Knapsack)
# ============================================

@dataclass
class Item:
    name: str
    value: int
    weight: int

    @property
    def value_per_weight(self) -> float:
        return self.value / self.weight

def fractional_knapsack(capacity: int, items: List[Item]) -> Tuple[List[Tuple[str, float]], int]:
    """
    분할 가능 배낭 문제 - O(n log n)
    탐욕 선택: 단위 무게당 가치가 가장 높은 물건 선택

    0/1 배낭 문제에서는 탐욕법이 최적해를 보장하지 않음!
    """
    # 단위 가치 기준 정렬
    sorted_items = sorted(items, key=lambda i: i.value_per_weight, reverse=True)

    total_value = 0
    remaining = capacity
    selected = []

    for item in sorted_items:
        if remaining <= 0:
            break

        take = min(item.weight, remaining)
        selected.append((item.name, take))
        total_value += take * item.value_per_weight
        remaining -= take

    return selected, int(total_value)

# ============================================
# 6. 0/1 배낭 문제 - 탐욕 근사
# ============================================

def knapsack_greedy_approx(capacity: int, items: List[Item]) -> Tuple[List[str], int]:
    """
    0/1 배낭 문제에 대한 탐욕 근사 알고리즘
    주의: 최적해를 보장하지 않음!

    근사 비율: 최악의 경우 임의로 나쁠 수 있음
    """
    sorted_items = sorted(items, key=lambda i: i.value_per_weight, reverse=True)

    total_value = 0
    remaining = capacity
    selected = []

    for item in sorted_items:
        if item.weight <= remaining:
            selected.append(item.name)
            total_value += item.value
            remaining -= item.weight

    return selected, total_value

# ============================================
# 테스트
# ============================================

if __name__ == "__main__":
    print("=== 1. 활동 선택 문제 ===")
    activities = [
        Activity("A1", 1, 4),
        Activity("A2", 3, 5),
        Activity("A3", 0, 6),
        Activity("A4", 5, 7),
        Activity("A5", 3, 9),
        Activity("A6", 5, 9),
        Activity("A7", 6, 10),
        Activity("A8", 8, 11),
        Activity("A9", 8, 12),
        Activity("A10", 2, 14),
        Activity("A11", 12, 16),
    ]
    selected = activity_selection(activities)
    print(f"선택된 활동: {[a.name for a in selected]}")
    print(f"활동 수: {len(selected)}")

    print("\n=== 2. Kruskal MST ===")
    edges = [
        Edge(0, 1, 4), Edge(0, 2, 3), Edge(1, 2, 1),
        Edge(1, 3, 2), Edge(2, 3, 4), Edge(3, 4, 2),
        Edge(4, 5, 6)
    ]
    mst, weight = kruskal_mst(6, edges)
    print(f"MST 간선: {[(e.u, e.v, e.weight) for e in mst]}")
    print(f"총 가중치: {weight}")

    print("\n=== 3. 허프만 코딩 ===")
    char_freq = {'a': 45, 'b': 13, 'c': 12, 'd': 16, 'e': 9, 'f': 5}
    root, codes = huffman_coding(char_freq)
    print(f"허프만 코드: {codes}")

    print("\n=== 4. 분할 가능 배낭 ===")
    items = [
        Item("Gold", 60, 10),
        Item("Silver", 100, 20),
        Item("Bronze", 120, 30)
    ]
    selected, value = fractional_knapsack(50, items)
    print(f"선택: {selected}")
    print(f"총 가치: {value}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 탐욕 알고리즘 적용 가능성 판단표

| 문제 | 탐욕 선택 속성 | 최적 부분구조 | 탐욕법 적용 | 비고 |
|:---|:---:|:---:|:---:|:---|
| 활동 선택 | Yes | Yes | **최적** | 종료 시간 정렬 |
| MST (Kruskal) | Yes | Yes | **최적** | 매트로이드 |
| 최단 경로 (Dijkstra) | Yes | Yes | **최적** | 비음수 가중치 |
| 허프만 코딩 | Yes | Yes | **최적** | 최적 접두사 코드 |
| 분할 배낭 | Yes | Yes | **최적** | 분할 가능 |
| 0/1 배낭 | No | Yes | **근사만** | DP 필요 |
| 동전 교환 (일반) | No | Yes | **근사만** | 동전 체계 의존 |
| TSP | No | Yes | **근사만** | NP-hard |

#### 2. 과목 융합 관점

- **네트워크**: 라우팅 프로토콜(RIP, OSPF)의 경로 선택에 다익스트라 활용
- **운영체제**: CPU 스케줄링(Shortest Job First), 메모리 할당(First Fit, Best Fit)
- **정보 이론**: 허프만 코딩, LZ 계열 압축

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오

**시나리오 A: 클러스터 서버 작업 스케줄링**
- **문제**: 100개 작업의 최적 순서 결정
- **전략**: 처리 시간이 짧은 작업 우선(SJF) - 대기 시간 최소화

**시나리오 B: 네트워크 백본 설계**
- **문제**: 최소 비용으로 모든 노드 연결
- **전략**: Kruskal MST로 최소 비용 연결망 구축

#### 2. 탐욕 알고리즘 적용 체크리스트
- [ ] 탐욕 선택 속성 증명 가능한가?
- [ ] 최적 부분구조가 존재하는가?
- [ ] 역선택(Cut) 예시가 있는가?
- [ ] 근사해로 충분한가?

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 구분 | 효과 |
|:---:|:---|
| **정량적** | O(2^n) → O(n log n) 가능 |
| **정성적** | 구현 단순, 이해 용이 |

#### 2. 참고 문헌
- **Cormen et al., CLRS**, Chapter 16: Greedy Algorithms

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [동적 프로그래밍](./dynamic_programming.md): 중복 부분문제 처리.
- [최소 신장 트리 (MST)](./02_graph/mst.md): 탐욕법의 대표 응용.
- [다익스트라 알고리즘](./02_graph/dijkstra.md): 최단 경로 탐욕 해법.
- [백트래킹](./backtracking.md): 탐욕 실패 시 대안.
- [근사 알고리즘](./approximation_algorithm.md): 탐욕 기반 최적화.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 탐욕 알고리즘은 **"지금 당장 가장 좋아 보이는 것부터 고르는 방법"**이에요.
2. 마치 사탕 바구니에서 **가장 큰 사탕부터 집어서** 주머니를 채우는 것과 같아요.
3. 어떤 때는 욕심내서 고른 게 **나중에 보면 최고의 선택**이 되기도 하지만, 아닐 때도 있어요!
