+++
title = "269. MCS 락"
weight = 269
+++

# 269. MCS 락 (MCS Lock)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 자신의 노드에서 스핀하는 NUMA 친화적 큐 락
> 2. **가치**: 높은 경합, NUMA 시스템에 최적
> 3. **융합**: CLH 락, 스핀락, 캐시 효율과 연관

---

## Ⅰ. 개요

### 개념 정의

MCS 락(Mellor-Crummey and Scott Lock)은 **각 스레드가 자신의 지역 노드에서 스핀하는 NUMA 친화적 큐 기반 스핀락**이다. CLH와 달리 지역 노드에서 스핀하므로 NUMA 시스템에 효율적이다.

### 💡 비유: 자리표
MCS 락은 **자리표**와 같다. 내 자리표만 확인한다. 내 자리에 앉을 수 있을 때까지 내 자리에서 기다린다. 남의 자리를 보지 않는다.

### MCS 락 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                MCS 락 구조                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【기본 구조】                                                         │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  struct mcs_node {                                                 │ │
│  │      mcs_node* next;       // 다음 노드                             │ │
│  │      bool locked;          // true: 대기, false: 진입              │ │
│  │  };                                                              │ │
│  │                                                             │ │
│  │  struct mcs_lock {                                                 │ │
│  │      atomic<mcs_node*> tail;  // 큐 끝                              │ │
│  │  };                                                              │ │
│  │                                                             │ │
│  │  각 스레드:                                                         │ │
│  │  • my_node: 자신의 노드 (여기서 스핀)                                  │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【동작 원리】                                                          │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  lock():                                                           │ │
│  │  1. my_node->next = nullptr                                       │ │
│  │  2. my_node->locked = true                                        │ │
│  │  3. prev = tail.exchange(my_node)                                 │ │
│  │  4. if (prev != nullptr) {                                        │ │
│  │         prev->next = my_node  // 이전 노드에 연결                   │ │
│  │         while (my_node->locked) spin();  // 내 노드에서 스핀         │ │
│  │     }                                                             │ │
│  │     // prev == null이면 바로 진입                                    │ │
│  │                                                             │ │
│  │  unlock():                                                         │ │
│  │  1. if (my_node->next == nullptr) {                               │ │
│  │         if (tail.compare_exchange(my_node, nullptr))               │ │
│  │             return;  // 대기자 없음                                  │ │
│  │         while (my_node->next == nullptr) spin();  // 대기자 대기     │ │
│  │     }                                                             │ │
│  │  2. my_node->next->locked = false  // 다음 스레드 깨움             │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【큐 상태 변화】                                                       │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  초기: tail = null                                                  │ │
│  │                                                             │ │
│  │  T1 lock (prev = null):                                            │ │
│  │  tail → [node1(locked=true)]                                       │ │
│  │  → 바로 진입!                                                        │ │
│  │                                                             │ │
│  │  T2 lock (prev = node1):                                           │ │
│  │  tail → [node2(locked=true)]                                       │ │
│  │           ↑                                                         │ │
│  │      node1(locked=true, next=node2)                                │ │
│  │                                                             │ │
│  │  T2는 node2에서 스핀 (자신의 지역 메모리!)                               │ │
│  │                                                             │ │
│  │  T1 unlock:                                                        │ │
│  │  node1.next = node2                                                │ │
│  │  node2.locked = false  → T2 깨어남!                                 │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【NUMA 장점】                                                          │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  CLH: 이전 노드에서 스핀 (다른 NUMA 노드 가능)                          │ │
│  │  MCS: 자신의 노드에서 스핀 (지역 NUMA 노드)                             │ │
│  │                                                             │ │
│  │  → NUMA 시스템에서 MCS가 더 효율적                                    │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석

### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                MCS 락 상세                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【CLH vs MCS 비교】                                                   │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  특성           CLH                    MCS                       │ │
│  │  ────           ────                    ────                      │ │
│  │  스핀 위치       pred_node->locked      my_node->locked            │ │
│  │  링크 방향       이전 노드 ←             이전 노드 → 다음 노드         │ │
│  │  unlock         my_node->locked=false   next->locked=false        │ │
│  │  NUMA           비효율 (원격 스핀)        효율적 (지역 스핀)           │ │
│  │  복잡도          단순                    약간 복잡                    │ │
│  │  대기자 확인     불필요                   CAS 필요                    │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【장단점】                                                             │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  장점:                                                              │ │
│  │  • NUMA 친화적 (지역 노드에서 스핀)                                    │ │
│  │  • 캐시 효율적 (캐시 라인 바운싱 최소화)                               │ │
│  │  • FIFO 공정성                                                      │ │
│  │  • 기아 상태 없음                                                    │ │
│  │  • 높은 경합에서 우수                                                  │ │
│  │                                                             │ │
│  │  단점:                                                               │ │
│  │  • 구현 복잡 (unlock에서 대기자 확인 필요)                             │ │
│  │  • 일반 락보다 오버헤드                                                │ │
│  │  • 낮은 경합에서는 이점 없음                                           │ │
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
│  【C++ MCS 락 구현】                                                   │
│  ──────────────────                                                  │
│  #include <atomic>                                                   │
│                                                                     │
│  class MCSLock {                                                     │
│      struct Node {                                                   │
│          std::atomic<Node*> next{nullptr};                           │
│          std::atomic<bool> locked{true};                             │
│      };                                                              │
│                                                                     │
│      std::atomic<Node*> tail{nullptr};                              │
│      static thread_local Node my_node;                              │
│                                                                     │
│  public:                                                            │
│      void lock() {                                                  │
│          Node* node = &my_node;                                      │
│          node->next.store(nullptr, std::memory_order_relaxed);       │
│          node->locked.store(true, std::memory_order_relaxed);        │
│                                                                     │
│          Node* prev = tail.exchange(node, std::memory_order_acq_rel);│
│                                                                     │
│          if (prev != nullptr) {                                      │
│              prev->next.store(node, std::memory_order_release);      │
│              while (node->locked.load(std::memory_order_acquire)) {  │
│                  // 스핀 (자신의 지역 변수!)                             │
│              }                                                       │
│          }                                                          │
│      }                                                              │
│                                                                     │
│      void unlock() {                                                │
│          Node* node = &my_node;                                      │
│                                                                     │
│          // 대기자가 있는지 확인                                        │
│          if (node->next.load(std::memory_order_acquire) == nullptr) {│
│              Node* expected = node;                                  │
│              if (tail.compare_exchange_strong(expected, nullptr,    │
│                      std::memory_order_release)) {                   │
│                  return;  // 대기자 없음                               │
│              }                                                       │
│              // 대기자가 올 때까지 대기                                  │
│              while (node->next.load(std::memory_order_acquire) == nullptr) {│
│                  // 스핀                                               │
│              }                                                       │
│          }                                                          │
│                                                                     │
│          // 다음 스레드 깨우기                                          │
│          node->next.load(std::memory_order_acquire)                  │
│               ->locked.store(false, std::memory_order_release);      │
│      }                                                              │
│  };                                                                 │
│                                                                     │
│  thread_local MCSLock::Node MCSLock::my_node;                        │
│                                                                     │
│  【Java MCS 락】                                                       │
│  ──────────────────                                                  │
│  import java.util.concurrent.atomic.*;                              │
│                                                                     │
│  class MCSLock {                                                     │
│      static class Node {                                             │
│          volatile Node next;                                         │
│          volatile boolean locked = true;                             │
│      }                                                              │
│                                                                     │
│      private final AtomicReference<Node> tail =                     │
│          new AtomicReference<>(null);                                │
│      private final ThreadLocal<Node> myNode =                       │
│          ThreadLocal.withInitial(Node::new);                        │
│                                                                     │
│      public void lock() {                                            │
│          Node node = myNode.get();                                  │
│          node.next = null;                                           │
│          node.locked = true;                                         │
│          Node prev = tail.getAndSet(node);                           │
│          if (prev != null) {                                         │
│              prev.next = node;                                       │
│              while (node.locked) {                                   │
│                  Thread.onSpinWait();                                │
│              }                                                       │
│          }                                                          │
│      }                                                              │
│                                                                     │
│      public void unlock() {                                          │
│          Node node = myNode.get();                                  │
│          if (node.next == null) {                                    │
│              if (tail.compareAndSet(node, null)) return;            │
│              while (node.next == null) Thread.onSpinWait();         │
│          }                                                          │
│          node.next.locked = false;                                  │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  【Linux 커널 qspinlock】                                              │
│  ──────────────────                                                  │
│  // MCS 변형, 4바이트 큐 기반 스핀락                                    │
│  // 최신 Linux의 기본 스핀락 구현                                        │
│                                                                     │
│  // 3개 스레드 이하: 인라인 빠른 경로                                    │
│  // 그 이상: MCS 큐 모드                                               │
│                                                                     │
│  // kernel/locking/qspinlock.c                                       │
│                                                                     │
│  【성능 비교 (64 코어 NUMA)】                                           │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  락 타입              처리량 (ops)    원격 메모리 접근                 │ │
│  │  ────────              ─────────        ──────────────               │ │
│  │  스핀락 (CAS)           20,000         90%                          │ │
│  │  티켓 락                50,000         70%                          │ │
│  │  CLH 락                100,000        50%                          │ │
│  │  MCS 락                150,000        10%                          │ │
│  │                                                             │ │
│  │  NUMA 시스템에서 MCS가 가장 효율적                                      │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【언제 사용할까?】                                                      │
│  ──────────────────                                                  │
│  적합:                                                                 │
│  • 높은 경합                                                          │
│  • NUMA 시스템                                                        │
│  • 다중 소켓 서버                                                      │
│  • 공정성 필요                                                        │
│                                                                     │
│  부적합:                                                               │
│  • 낮은 경합 (일반 락 충분)                                              │
│  • 단일 코어/소켓                                                       │
│  • 짧은 임계 영역                                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론

### 핵심 요약

```
• 개념: 자신의 노드에서 스핀하는 큐 락
• 특징: NUMA 친화적, 지역 스핀
• 장점: NUMA 효율, 캐시 효율, 공정성
• 단점: 구현 복잡, unlock 오버헤드
• CLH vs MCS: 스핀 위치, NUMA 효율
• 활용: Linux qspinlock
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [CLH 락](./268_clh_lock.md) → 유사 락
- [티켓 락](./267_ticket_lock.md) → 간단한 대안
- [락 스래싱](./264_lock_thrashing.md) → 완화
- [NUMA](../3_cpu_scheduling/219_numa_scheduling.md) → 최적화 대상

### 👶 어린이를 위한 3줄 비유 설명

**개념**: MCS 락은 "자리표" 같아요!

**원리**: 내 자리표만 확인해요!

**효과**: 내 자리에서 기다려요!
