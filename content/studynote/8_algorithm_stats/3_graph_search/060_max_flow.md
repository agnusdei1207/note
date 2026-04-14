+++
weight = 60
title = "최대 유량 (Max Flow)"
date = "2024-05-22"
[extra]
categories = "studynote-algorithm"
+++

## 핵심 인사이트 (3줄 요약)
- **네트워크 유량 문제:** 소스(Source)에서 싱크(Sink)까지 보낼 수 있는 최대 흐름량을 구하는 알고리즘입니다.
- **용량 제한 및 보존 법칙:** 각 간선의 용량(Capacity)을 넘지 않아야 하며, 중간 노드에서 유입량과 유출량은 같아야 합니다.
- **증가 경로와 잔여 그래프:** 잔여 용량이 남은 경로(Augmenting Path)를 반복적으로 찾아 흐름을 추가하는 방식으로 해결합니다.

### Ⅰ. 개요 (Context & Background)
- **발생 배경:** 물류 이송, 데이터 전송, 교통 흐름 등 네트워크 자원의 최적 활용을 위해 설계되었습니다.
- **핵심 정리:** 최대 유량은 해당 네트워크의 최소 컷(Min-Cut) 용량과 같다는 Max-Flow Min-Cut 정리가 핵심입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **용량 (Capacity):** 간선(u, v)이 가질 수 있는 최대 흐름량 c(u, v).
- **유량 (Flow):** 실제로 간선을 흐르는 양 f(u, v) (f <= c).
- **잔여 그래프 (Residual Graph):** 현재 유량을 제외하고 더 보낼 수 있는 용량 c - f를 나타내는 가상의 그래프입니다.

```text
[Max Flow Concept Diagram]
(S) : Source, (T) : Sink, (A/B/C) : Nodes
Arrow (x/y) : Flow x out of Capacity y

      (2/5)       (2/3)
 (S) ------> (A) ------> (T)
  |           ^           ^
  | (3/4)     | (1/2)     | (3/6)
  v           |           |
 (B) ------> (C) ---------+
      (3/3)

[Algorithm Logic]
1. Find Path (S -> T) with Residual Capacity > 0 (증가 경로 탐색)
2. Bottleneck (Min Residual Capacity) identifies total flow to add (최대 유량 갱신)
3. Update Residual Graph (Forward/Backward Edges) (잔여 그래프 업데이트)
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Comparison) | 포드-풀커슨 (Ford-Fulkerson) | 에드몬드-카프 (Edmonds-Karp) |
|:---:|:---|:---|
| **기본 아이디어** | 증가 경로 반복 탐색 | BFS 기반 증가 경로 탐색 |
| **시간 복잡도** | O(f * E) (f: 최대 유량) | O(V * E²) |
| **장점** | 구현이 간단함 | 흐름량과 관계없이 성능 보장 |
| **단점** | 용량 크기에 따라 느려질 수 있음 | BFS 사용에 따른 오버헤드 |
| **추가 기법** | - | 디닉(Dinic) 알고리즘 (O(V²E))으로 발전 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **이분 매칭(Bipartite Matching):** 최대 유량의 특수한 케이스로, 용량이 모두 1인 네트워크로 모델링하여 해결 가능합니다.
- **네트워크 설계:** 통신망의 병목(Bottleneck) 구간을 찾아내고 전체 처리량(Throughput)을 극대화하는 데 활용됩니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **최적화 도구:** 자원의 제약이 있는 모든 시스템에서 흐름의 최적화를 달성하는 표준적인 방법론입니다.
- **결론:** 복잡한 자원 배분 문제를 그래프 모델링으로 변환하여 정량적으로 해결할 수 있게 해주는 필수 알고리즘입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 네트워크 유량 (Network Flow)
- **핵심 정리:** Max-Flow Min-Cut Theorem
- **관련 알고리즘:** 이분 매칭 (Bipartite Matching), 디닉 (Dinic) 알고리즘

### 👶 어린이를 위한 3줄 비유 설명
- "수도꼭지(Source)에서 물통(Sink)까지 물을 보내는데, 파이프(Edge)가 가늘어서 물이 조금씩만 갈 수 있어요."
- "어떤 길로 물을 보낼지 잘 골라서, 최대한 많은 물을 물통에 담으려는 게임이에요."
- "꽉 막힌 길은 피하고, 아직 물이 더 들어갈 수 있는 길만 찾아서 물을 콸콸 보내는 거예요."
