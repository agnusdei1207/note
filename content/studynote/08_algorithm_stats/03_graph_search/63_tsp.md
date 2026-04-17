+++
weight = 63
title = "63. 외판원 문제 (TSP, Traveling Salesman Problem) - 최단 순회 경로의 탐색"
date = "2024-10-27"
[extra]
categories = "studynote-algorithm"
+++

## 핵심 인사이트 (3줄 요약)
1. **최단 해밀턴 회로**: 여러 도시를 모두 한 번씩만 방문하고 출발지로 돌아오는 '최단 거리'를 찾는 전형적인 조합 최적화 문제다.
2. **NP-난해 (NP-hard)**: 정점의 개수가 늘어날수록 경우의 수가 기하급수적으로 폭증하여(Factorial), 완벽한 해를 구하기 매우 어려운 복잡도를 가진다.
3. **실무적 해결**: 실무에서는 DP(비트마스크)를 통한 정해(Exact) 도출과 근사 알고리즘(Heuristic)을 통한 효율적 해 도출 사이의 Trade-off를 결정하는 것이 핵심이다.

### Ⅰ. 개요 (Context & Background)
외판원 문제(Traveling Salesman Problem, TSP)는 물류, 배송, 회로 설계, 유전자 서열 분석 등 현대 산업 전반에 걸쳐 가장 널리 인용되는 난제다. 단순히 모든 정점을 지나는 해밀턴 경로를 찾는 것을 넘어, 그중 '비용(Cost)이 최소'가 되는 경로를 확정해야 하므로 계산 복잡도가 매우 높다. 이는 알고리즘 효율성 측정과 계산 복잡도 이론의 상징적인 문제로 다뤄진다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
TSP는 가중치 그래프에서 시작 정점에서 출발하여 모든 정점을 거쳐 다시 시작 정점으로 돌아오는 가장 짧은 사이클을 찾는 과정이다.

```text
[Traveling Salesman Problem Concept / 외판원 문제 개념도]

       (A) <--- Start & End
      / | \
   10/ 15\ 20
    /   |   \
  (B)---(C)---(D)
    \  35|  30/
     \   |   /
      \ (E) /
       -----

<Mechanism: Dynamic Programming with Bitmask>
- State: dp[visited_mask][current_node]
- visited_mask: 방문한 도시 집합 (00101b -> A, C 방문)
- Recursion: dp[mask][curr] = min(dp[mask | (1 << next)][next] + cost[curr][next])
```

**주요 알고리즘 모델:**
- **Exact Algorithm**: 헬드-카프(Held-Karp) 알고리즘. 동적 계획법과 비트마스크를 결합하여 $O(n^2 2^n)$ 시간에 해결한다. (N=20 내외 한계)
- **Approximation Algorithm**: MST(최소 신장 트리) 기반 2-근사 알고리즘, 크리스토피디스(Christofides) 알고리즘(1.5-근사).
- **Meta-heuristics**: 유전 알고리즘(Genetic Algorithm), 담금질 기법(Simulated Annealing), 개미 군집 최적화(ACO) 등.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | TSP (외판원 문제) | MST (최소 신장 트리) |
| :--- | :--- | :--- |
| **목표** | 모든 정점 방문 후 **복귀(Cycle)** | 모든 정점을 잇는 **최소 연결(Tree)** |
| **복잡도** | **NP-hard** | **P Class** (Prim, Kruskal) |
| **구조** | 해밀턴 회로 기반 | 비순환 그래프(DAG) 기반 |
| **결과 형태** | 하나의 닫힌 경로(Loop) | 나무 모양의 연결망(Span) |
| **적용 사례** | 배송 기사 동선, 로봇 청소기 경로 | 네트워크 인프라 구축, 케이블 가설 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
기술사적 관점에서 TSP는 **'정확도와 속도의 균형'**을 설계하는 아키텍처 역량을 시험한다.
1. **정밀도 우선**: 반도체 칩 배선 설계나 고가 가공 기계의 드릴링 경로는 DP 기반 정해(Exact) 도출이 필수적이다.
2. **속도 및 비용 우선**: 음식 배달 플랫폼이나 물류 트럭 배차 시스템은 실시간 응답이 중요하므로, 2-opt, 3-opt Local Search나 Nearest Neighbor 알고리즘을 적용한다.
3. **하이브리드 전략**: 분기 한정(Branch and Bound) 기법을 적용하여 탐색 범위를 획기적으로 줄이면서도 최적해에 근접하는 설계를 권장한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
TSP는 공급망 관리(SCM)의 최적화 수준을 결정하는 척도다. 클라우드 컴퓨팅과 분산 처리 기술의 발달로 과거에는 불가능했던 대규모 TSP 분석이 가능해지고 있다. 최근에는 그래프 신경망(GNN)이나 심층 강화학습(DRL)을 통해 스스로 최적 경로를 학습하는 AI 에이전트 모델로 발전하고 있으며, 이는 미래 도심 항공 교통(UAM)의 경로 관제 시스템의 표준 알고리즘으로 자리 잡을 것이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: Combinatorial Optimization, NP-hard
- **유사 개념**: Hamiltonian Cycle, Vehicle Routing Problem (VRP)
- **하위 기술**: Bitmask DP, 2-opt, Ant Colony Optimization (ACO)

### 👶 어린이를 위한 3줄 비유 설명
1. 택배 아저씨가 여러 집을 다 들르고 회사로 돌아올 때, 기름값을 제일 아끼는 길을 찾는 거예요.
2. 집이 3~4개일 땐 쉽지만, 100개가 넘어가면 전 세계 슈퍼컴퓨터를 다 합쳐도 계산하기 힘들 만큼 복잡해져요.
3. 그래서 완벽한 1등 길보다는 "이 정도면 충분히 빠르네!" 하는 지름길을 찾는 것이 중요하답니다.
