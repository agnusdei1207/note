+++
weight = 61
title = "오일러 경로 및 회로 (Eulerian Path & Circuit)"
date = "2024-05-22"
[extra]
categories = "studynote-algorithm"
+++

## 핵심 인사이트 (3줄 요약)
- **한 붓 그리기:** 모든 간선(Edge)을 정확히 한 번씩만 통과하는 경로입니다.
- **차수(Degree) 조건:** 무방향 그래프에서 오일러 회로는 모든 정점의 차수가 짝수여야 합니다.
- **연결성 전제:** 간선이 있는 모든 정점들이 하나의 컴포넌트로 연결되어 있어야 합니다.

### Ⅰ. 개요 (Context & Background)
- **유래:** 쾨니히스베르크의 다리 문제(Seven Bridges of Königsberg)를 해결하기 위해 레온하르트 오일러가 제안한 개념입니다.
- **의미:** 그래프 이론의 시작점으로 평가받으며, 효율적인 순회 및 경로 탐색의 기초가 됩니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **오일러 회로 (Eulerian Circuit):** 시작점과 도착점이 같은 오일러 경로. 모든 정점의 차수가 짝수여야 합니다.
- **오일러 경로 (Eulerian Path):** 시작점과 도착점이 다른 오일러 경로. 홀수 차수를 가진 정점이 정확히 2개여야 합니다.

```text
[Eulerian Graph Conditions]
+-------------------+------------------------------------------+
| Graph Type        | Conditions for Eulerian Circuit          |
+-------------------+------------------------------------------+
| Undirected (무방향)| All vertices have even degree (모두 짝수)   |
+-------------------+------------------------------------------+
| Directed (유방향)  | In-degree = Out-degree for all vertices  |
+-------------------+------------------------------------------+

[Bilingual Flow]
1. 정점 차수 확인 (Check Degrees)
2. 시작 정점 선택 (Select Start Node)
3. Hierholzer 알고리즘 또는 DFS로 경로 구성 (Path Reconstruction)
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Comparison) | 오일러 경로 (Eulerian Path) | 해밀턴 경로 (Hamiltonian Path) |
|:---:|:---|:---|
| **방문 대상** | 모든 간선 (Every Edge) | 모든 정점 (Every Vertex) |
| **방문 횟수** | 정확히 1번 | 정확히 1번 |
| **복잡도** | P 문제 (O(V+E)) | NP-완전 문제 (NP-Complete) |
| **핵심 조건** | 정점의 차수 (Degree) | 특정 조건 없음 (복잡함) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **네트워크 라우팅:** 모든 링크를 점검해야 하는 네트워크 모니터링이나 제설차/청소차의 최단 경로 설계에 활용됩니다.
- **게놈 시퀀싱:** DNA 서열을 재구성할 때 k-mer 그래프를 오일러 경로 문제로 변환하여 해결하는 'De Bruijn Graph' 방식이 대표적입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **효율적 순회:** 복잡한 네트워크에서 모든 자원(간선)을 낭비 없이 순회할 수 있는 이론적 토대를 제공합니다.
- **결론:** 간선 중심의 경로 탐색에서 최적의 해를 보장하는 선형 시간 알고리즘의 정점입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 그래프 순회 (Graph Traversal)
- **유사 개념:** 해밀턴 경로 (Hamiltonian Path)
- **관련 알고리즘:** Hierholzer 알고리즘, Fleury 알고리즘

### 👶 어린이를 위한 3줄 비유 설명
- "종이에서 펜을 떼지 않고 모든 선을 다 그리는 '한 붓 그리기' 게임이에요."
- "집집마다 신문을 배달할 때, 갔던 길을 또 가지 않고 모든 골목을 다 도는 똑똑한 배달부 같아요."
- "동그라미나 네모를 그릴 때 어디서 시작해서 어디로 끝날지 미리 아는 방법이에요."
