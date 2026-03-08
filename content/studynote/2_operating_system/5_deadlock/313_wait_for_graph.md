+++
title = "313. 대기 그래프"
weight = 313
+++

# 313. 대기 그래프 (Wait-for Graph)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 프로세스 간 대기 관계의 그래프 표현
> 2. **가치**: 교착상태 탐지의 핵심 도구
> 3. **융합**: 자원 할당 그래프, 사이클 탐지와 연관

---

## Ⅰ. 개요

### 개념 정의

대기 그래프(Wait-for Graph)는 **어떤 프로세스가 어떤 프로세스를 기다리는지를 나타내는 방향 그래프**다. 자원 할당 그래프에서 자원 노드를 제거한 단순화된 형태다.

### 💡 비유: 대기줄 지도
대기 그래프는 **대기줄 지도**와 같다. 누가 누구를 기다리는지 한눈에 보여준다. 순환이 있으면 누구도 움직일 수 없다.

### 대기 그래프 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                대기 그래프 구조                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【자원 할당 그래프 → 대기 그래프 변환】                                │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  자원 할당 그래프:                                                    │ │
│  │  P1 ──요청──► R1 ──할당──► P2                                     │ │
│  │  P2 ──요청──► R2 ──할당──► P3                                     │ │
│  │  P3 ──요청──► R1                                                  │ │
│  │                                                             │ │
│  │  대기 그래프 (자원 노드 제거):                                         │ │
│  │  P1 ────────► P2  (P1이 R1 기다림, R1은 P2가 보유)                   │ │
│  │  P2 ────────► P3  (P2가 R2 기다림, R2은 P3가 보유)                   │ │
│  │  P3 ────────► P2  (P3가 R1 기다림, R1은 P2가 보유)                   │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【그래프 구성】                                                        │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  노드 (Node): 프로세스                                               │ │
│  │  간선 (Edge): P1 → P2 는 "P1이 P2가 보유한 자원을 기다림"             │ │
│  │                                                             │ │
│  │       ┌───┐                                                       │ │
│  │       │ P1│ ────────► ┌───┐                                       │ │
│  │       └───┘           │ P2│                                       │ │
│  │         ▲             └───┘                                       │ │
│  │         │               │                                         │ │
│  │         │               ▼                                         │ │
│  │       ┌───┐           ┌───┐                                       │ │
│  │       │ P4│ ◄──────── │ P3│                                       │ │
│  │       └───┘           └───┘                                       │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【사이클 탐지】                                                        │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  사이클 있음 = 교착상태 (단일 인스턴스 자원)                             │ │
│  │                                                             │ │
│  │  P1 → P2 → P3 → P1  (사이클!)                                     │ │
│  │                                                             │ │
│  │  ┌───┐     ┌───┐     ┌───┐                                       │ │
│  │  │ P1│ ──► │ P2│ ──► │ P3│                                       │ │
│  │  └───┘     └───┘     └───┘                                       │ │
│  │     ▲                     │                                       │ │
│  │     └─────────────────────┘                                       │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석

### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                대기 그래프 상세                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【그래프 구축 알고리즘】                                               │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  1. 자원 할당 그래프에서 자원 노드 제거                               │ │
│  │  2. P1 → R → P2 를 P1 → P2 로 변환                                │ │
│  │  3. 간선 방향: 요청 프로세스 → 할당받은 프로세스                       │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【사이클 탐지 알고리즘】                                               │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  1. DFS (깊이 우선 탐색):                                           │ │
│  │     • 각 노드에서 시작하여 깊이 탐색                                   │ │
│  │     • 방문 중인 노드 재방문 = 사이클                                  │ │
│  │     • 시간 복잡도: O(n²)                                            │ │
│  │                                                             │ │
│  │  2. 위상 정렬:                                                       │ │
│  │     • 진입 차수가 0인 노드부터 제거                                   │ │
│  │     • 제거할 수 없는 노드 = 사이클                                    │ │
│  │     • 시간 복잡도: O(n + e)                                         │ │
│  │                                                             │ │
│  │  3. Union-Find:                                                     │ │
│  │     • 간선 추가 시 두 노드가 같은 집합이면 사이클                       │ │
│  │     • 시간 복잡도: O(e · α(n))                                      │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【대기 그래프 vs 자원 할당 그래프】                                     │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  특성           자원 할당 그래프       대기 그래프                   │ │
│  │  ────────       ────────────────       ────────────             │ │
│  │  노드           프로세스 + 자원         프로세스만                  │ │
│  │  간선           요청 + 할당            대기만                      │ │
│  │  복잡도          높음                   낮음                       │ │
│  │  탐지 속도       느림                   빠름                       │ │
│  │  적용           다중 인스턴스           단일 인스턴스               │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【단일 vs 다중 인스턴스】                                              │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  단일 인스턴스 자원:                                                   │ │
│  │  • 대기 그래프에서 사이클 = 교착상태 확정                              │ │
│  │                                                             │ │
│  │  다중 인스턴스 자원:                                                   │ │
│  │  • 사이클이 있어도 교착상태 아닐 수 있음                               │ │
│  │  • 대기 그래프만으로 판단 불가                                         │ │
│  │  • 은행원 알고리즘 필요                                               │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 실무 적용

### 구현 예시
```
┌─────────────────────────────────────────────────────────────────────┐
│                실무 적용                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【대기 그래프 구현】                                                   │
│  ──────────────────                                                  │
│  class WaitForGraph {                                               │
│      Map<Integer, Set<Integer>> graph = new HashMap<>();            │
│                                                                     │
│      // 대기 관계 추가                                                 │
│      void addEdge(int waiter, int holder) {                          │
│          graph.computeIfAbsent(waiter, k -> new HashSet<>())        │
│               .add(holder);                                          │
│      }                                                              │
│                                                                     │
│      // 대기 관계 제거                                                 │
│      void removeEdge(int waiter, int holder) {                       │
│          Set<Integer> edges = graph.get(waiter);                    │
│          if (edges != null) {                                        │
│              edges.remove(holder);                                   │
│          }                                                          │
│      }                                                              │
│                                                                     │
│      // 사이클 탐지 (DFS)                                              │
│      boolean hasCycle() {                                            │
│          Set<Integer> visited = new HashSet<>();                    │
│          Set<Integer> recursionStack = new HashSet<>();             │
│                                                                     │
│          for (int node : graph.keySet()) {                          │
│              if (dfs(node, visited, recursionStack)) {              │
│                  return true;                                        │
│              }                                                      │
│          }                                                          │
│          return false;                                               │
│      }                                                              │
│                                                                     │
│      boolean dfs(int node, Set<Integer> visited,                     │
│                   Set<Integer> recursionStack) {                     │
│          if (recursionStack.contains(node)) return true;            │
│          if (visited.contains(node)) return false;                  │
│                                                                     │
│          visited.add(node);                                          │
│          recursionStack.add(node);                                   │
│                                                                     │
│          Set<Integer> neighbors = graph.get(node);                  │
│          if (neighbors != null) {                                    │
│              for (int neighbor : neighbors) {                       │
│                  if (dfs(neighbor, visited, recursionStack)) {      │
│                      return true;                                    │
│                  }                                                  │
│              }                                                      │
│          }                                                          │
│                                                                     │
│          recursionStack.remove(node);                               │
│          return false;                                               │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  【락 대기 그래프 추적】                                                 │
│  ──────────────────                                                  │
│  class LockWaitGraph {                                              │
│      Map<Long, Set<Long>> waitGraph = new ConcurrentHashMap<>();    │
│      Map<Long, Long> lockHolders = new ConcurrentHashMap<>();       │
│                                                                     │
│      // 락 요청 시                                                     │
│      void onLockRequest(long threadId, Object lock) {               │
│          Long holder = lockHolders.get(lock);                       │
│          if (holder != null && holder != threadId) {                │
│              waitGraph.computeIfAbsent(threadId, k -> new HashSet<>())│
│                         .add(holder);                                │
│          }                                                          │
│      }                                                              │
│                                                                     │
│      // 락 획득 시                                                     │
│      void onLockAcquired(long threadId, Object lock) {              │
│          lockHolders.put(lock, threadId);                           │
│          waitGraph.remove(threadId);  // 대기 관계 제거               │
│      }                                                              │
│                                                                     │
│      // 락 해제 시                                                     │
│      void onLockReleased(long threadId, Object lock) {              │
│          lockHolders.remove(lock);                                   │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  【데이터베이스 락 대기 그래프】                                          │
│  ──────────────────                                                  │
│  // MySQL: 락 대기 그래프 확인                                          │
│  SELECT * FROM information_schema.INNODB_LOCK_WAITS;                │
│  SELECT * FROM performance_schema.data_locks;                       │
│                                                                     │
│  // PostgreSQL: 락 대기 확인                                           │
│  SELECT blocked_locks.pid AS blocked_pid,                           │
│         blocking_locks.pid AS blocking_pid                          │
│  FROM pg_catalog.pg_locks blocked_locks                             │
│  JOIN pg_catalog.pg_locks blocking_locks                            │
│    ON blocking_locks.locktype = blocked_locks.locktype              │
│   AND blocking_locks.pid != blocked_locks.pid                       │
│  WHERE NOT blocked_locks.granted;                                   │
│                                                                     │
│  【주기적 사이클 탐지】                                                 │
│  ──────────────────                                                  │
│  ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);│
│  WaitForGraph wfg = new WaitForGraph();                            │
│                                                                     │
│  scheduler.scheduleAtFixedRate(() -> {                              │
│      if (wfg.hasCycle()) {                                          │
│          log.warn("Deadlock detected in wait-for graph!");          │
│          // 복구 작업 수행                                            │
│          recoveryHandler.handleDeadlock(wfg.findCycle());           │
│      }                                                              │
│  }, 0, 5, TimeUnit.SECONDS);  // 5초마다 탐지                         │
│                                                                     │
│  【사이클 시각화】                                                       │
│  ──────────────────                                                  │
│  void visualizeCycle(List<Integer> cycle) {                         │
│      StringBuilder sb = new StringBuilder("Deadlock cycle: ");      │
│      for (int i = 0; i < cycle.size(); i++) {                       │
│          sb.append("P").append(cycle.get(i));                       │
│          if (i < cycle.size() - 1) {                                │
│              sb.append(" -> ");                                      │
│          }                                                          │
│      }                                                              │
│      sb.append(" -> P").append(cycle.get(0));                       │
│      log.error(sb.toString());                                      │
│  }                                                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론

### 핵심 요약

```
• 개념: 프로세스 간 대기 관계의 그래프
• 구성: 노드=프로세스, 간선=대기
• 변환: 자원 할당 그래프에서 자원 노드 제거
• 탐지: DFS, 위상 정렬, Union-Find
• 판정: 사이클 있음 = 교착상태 (단일 인스턴스)
• 활용: 데이터베이스, 락 관리
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [자원 할당 그래프](./301_resource_allocation_graph.md) → 원본
- [교착상태 탐지](./295_deadlock_detection.md) → 활용
- [사이클 탐지](./315_victim_selection.md) → 알고리즘
- [교착상태](./291_deadlock.md) → 판정 대상

### 👶 어린이를 위한 3줄 비유 설명

**개념**: 대기 그래프는 "대기줄 지도" 같아요!

**원리**: 누가 누구를 기다리는지 보여요!

**효과**: 동그라미가 있으면 막혔어요!
