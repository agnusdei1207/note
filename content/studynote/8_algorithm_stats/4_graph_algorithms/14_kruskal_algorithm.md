+++
weight = 14
title = "크루스칼 알고리즘 (Kruskal's Algorithm)"
date = "2026-03-25"
[extra]
categories = "studynote-algorithm"
+++

## 핵심 인사이트 (3줄 요약)
- 간선(Edge) 중심의 최소 신장 트리(MST) 알고리즘으로, 가중치가 낮은 간선부터 선택하며 사이클을 방지함
- Union-Find 자료구조를 활용하여 사이클 발생 여부를 효율적으로 판단함
- 간선 리스트가 희소한(Sparse) 그래프에서 프림(Prim) 알고리즘보다 성능 우위를 점함

### Ⅰ. 개요 (Context & Background)
크루스칼 알고리즘은 그리디(Greedy) 기법을 활용하여 그래프 내의 모든 정점을 최소 비용으로 연결하는 최소 신장 트리(MST)를 구축한다. 통신망 설계, 도로 구축, 배관 연결 등 연결 비용을 최소화해야 하는 네트워크 인프라 설계의 핵심이다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[Kruskal's Algorithm Flow - Greedy + Union-Find]

1. Sort all Edges by weight (Ascending)
   Edge(A,B,2) < Edge(C,D,4) < Edge(B,C,7) ...

2. For each edge:
   If Find(U) != Find(V):  <-- No Cycle?
      Union(U, V)          <-- Add to MST
   Else:
      Discard (Avoid Cycle)

[Data Structure: Union-Find]
- Find: 노드의 루트 노드를 찾아 소속 집합 확인 (Path Compression)
- Union: 두 집합을 하나의 트리로 병합 (Union by Rank)
```
- **그리디 전략:** 전체를 보지 않고 당장 가장 저렴한 간선을 선택해도 최적해(MST)가 보장됨

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | 크루스칼 (Kruskal) | 프림 (Prim) |
| :--- | :--- | :--- |
| 중심 요소 | 간선 (Edge) | 정점 (Vertex) |
| 시간 복잡도 | O(E log E) 또는 O(E log V) | O(E log V) 또는 O(E + V log V) |
| 적합한 그래프 | 희소 그래프 (Sparse Graph) | 밀집 그래프 (Dense Graph) |
| 주요 메커니즘 | 간선 정렬 + Union-Find | 우선순위 큐 + 인접 노드 확장 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **실무 적용:** 대규모 네트워크 설계 시 간선 리스트만으로 동작하므로 구현이 직관적이며, 분산 환경에서도 Union-Find의 효율성을 극대화하여 적용 가능함
- **기술사적 판단:** 간선을 정렬하는 오버헤드가 크므로, 간선의 개수가 정점의 제곱에 비례하는 밀집 그래프에서는 프림 알고리즘을 선택하는 것이 성능상 유리함

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과:** 네트워크 구축 비용의 수학적 최저치를 보장하며, 복잡한 인프라 구조를 최소한의 자원으로 연결하는 최적화 도구로 활용됨
- **결론:** 크루스칼은 자료구조(Union-Find)와 알고리즘(Greedy)의 이상적인 결합 사례로, 전산학의 기초이자 강력한 최적화 표준임

### 📌 관련 개념 맵 (Knowledge Graph)
- 탐욕 알고리즘 → MST → 크루스칼 / 프림
- 크루스칼 → 사이클 판별 → Union-Find (Disjoint Set)
- MST → 응용 → Steiner Tree (NP-Hard)

### 👶 어린이를 위한 3줄 비유 설명
- 크루스칼 알고리즘은 **가장 싼 도로부터 먼저 까는 시공사**와 같아요.
- 이미 이어진 도시들 사이에 또 길을 놓아 빙빙 도는 건 피하고, 새로 연결되는 길만 골라요.
- 이렇게 하면 모든 도시를 가장 적은 비용으로 한 번에 이어 줄 수 있어요!
