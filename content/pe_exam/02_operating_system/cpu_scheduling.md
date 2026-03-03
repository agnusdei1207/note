+++
title = "CPU 스케줄링 (CPU Scheduling)"
date = 2026-03-02

[extra]
categories = "pe_exam-operating_system"
+++

# CPU 스케줄링 (CPU Scheduling)

## 핵심 인사이트 (3줄 요약)
> 준비(Ready) 상태의 프로세스 중 **어떤 프로세스에 CPU를 얼마나 할당할지 결정**하는 운영체제의 핵심 기능. 선점형(Preemptive)과 비선점형(Non-preemptive)으로 구분하며, FCFS, SJF, Round Robin, MLFQ 등의 알고리즘이 있다. 응답시간·처리량·공정성·CPU 활용률을 균형있게 최적화하는 것이 목표다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: CPU 스케줄링은 **다중 프로그래밍 환경에서 준비 상태(Ready)의 프로세스들 중 어떤 프로세스에 CPU를 할당할지, 얼마나 오래 할당할지 결정**하는 운영체제의 핵심 메커니즘이다. 스케줄러(Scheduler)가 스케줄링 알고리즘에 따라 결정을 내린다.

> 💡 **비유**: CPU 스케줄링은 **"병원 접수 대기열 관리"**와 같다. 환자(프로세스)들이 진료(CPU)를 기다리는데, 누구를 먼저 볼지 결정해야 한다. 응급 환자는 우선순위가 높고, 예약 환자는 순서대로, 오래 기다린 환자는 에이징으로 배려한다.

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 단일 프로그램 실행의 비효율**: 초기 컴퓨터는 한 번에 하나의 프로그램만 실행했다. I/O 대기 시간 동안 CPU가 유휴 상태가 되어 비효율적이었다.
2. **기술적 필요성**: 다중 프로그래밍으로 **여러 프로세스가 CPU를 공유**하게 되면서, 공정하고 효율적인 CPU 할당 방법이 필요했다. CPU는 한 번에 하나의 프로세스만 실행할 수 있다.
3. **시장/산업 요구**: 대화형 시스템(응답 시간 중요), 일괄 처리 시스템(처리량 중요), 실시간 시스템(마감 시간 준수) 등 **다양한 워크로드에 맞는 스케줄링**이 요구되었다.

**핵심 목적**: CPU 활용률을 높이고, 사용자 응답 시간을 최소화하며, 시스템 처리량을 최대화하고, 모든 프로세스에 공정하게 CPU를 할당하는 것이다.

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **장기 스케줄러** | 프로세스 생성/메모리 적재 결정 | 시스템 부하 조절, 멀티프로그래밍 정도 제어 | 병원 입원 결정 |
| **중기 스케줄러** | 스와핑(Swapping) 관리 | 메모리 부족 시 프로세스 보류/재개 | 병원 대기실 관리 |
| **단기 스케줄러** | CPU 할당 결정 | 밀리초 단위로 매우 빈번 실행 | 진료 순서 결정 |
| **디스패처(Dispatcher)** | 실제 CPU 제어권 이양 | 문맥 교환(Context Switch) 수행 | 진료실로 안내 |
| **준비 큐(Ready Queue)** | 실행 대기 프로세스 목록 | 다양한 자료구조 (큐, 우선순위 큐) | 대기 환자 목록 |
| **PCB(Process Control Block)** | 프로세스 상태 저장 | 우선순위, CPU burst, 대기시간 포함 | 환자 차트 |

**구조 다이어그램** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CPU 스케줄링 시스템 구조                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │                     프로세스 상태 전이도                            │    │
│   │                                                                   │    │
│   │   ┌─────────┐                    ┌─────────┐                     │    │
│   │   │  생성   │ ──장기스케줄러──→ │  준비   │                      │    │
│   │   │ (New)   │                    │ (Ready) │                     │    │
│   │   └─────────┘                    └────┬────┘                     │    │
│   │                                       │                          │    │
│   │                     ┌───단기스케줄러──┴──디스패처──┐             │    │
│   │                     ↓                             ↓             │    │
│   │              ┌─────────┐  I/O 요청         ┌─────────┐          │    │
│   │   ←──인터럽트──│  실행   │────────────────→│  대기   │          │    │
│   │   │           │(Running)│                  │ (Wait)  │          │    │
│   │   │           └─────────┘                  └────┬────┘          │    │
│   │   │                │                             │               │    │
│   │   │            종료 │         I/O 완료            │               │    │
│   │   │                ↓                             │               │    │
│   │   │           ┌─────────┐←───────────────────────┘               │    │
│   │   │           │  종료   │                                        │    │
│   │   │           │(Exit)   │                                        │    │
│   │   │           └─────────┘                                        │    │
│   │   │                                                              │    │
│   │   └──시간 만료(Time Quantum)──→ 준비 상태로 복귀                  │    │
│   │                                                                  │    │
│   └───────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │                    스케줄러 계층 구조                               │    │
│   │                                                                   │    │
│   │   ┌─────────────────┐                                            │    │
│   │   │   장기 스케줄러  │ ← 새 프로세스 생성 빈도 조절               │    │
│   │   │  (Job Scheduler) │   (분~시간 단위)                          │    │
│   │   └────────┬────────┘                                            │    │
│   │            ↓                                                     │    │
│   │   ┌─────────────────┐                                            │    │
│   │   │   중기 스케줄러  │ ← 메모리 부족 시 스왑 인/아웃              │    │
│   │   │ (Swap Scheduler) │   (초 단위)                               │    │
│   │   └────────┬────────┘                                            │    │
│   │            ↓                                                     │    │
│   │   ┌─────────────────┐     ┌─────────────────┐                    │    │
│   │   │   단기 스케줄러  │ ──→ │    디스패처     │                    │    │
│   │   │  (CPU Scheduler) │     │   (Dispatcher)  │                    │    │
│   │   │  (ms 단위)       │     │  문맥 교환 수행  │                    │    │
│   │   └─────────────────┘     └─────────────────┘                    │    │
│   │            ↓                        ↓                            │    │
│   │   ┌─────────────────────────────────────────┐                    │    │
│   │   │              준비 큐 (Ready Queue)        │                    │    │
│   │   │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐        │                    │    │
│   │   │  │ P1  │→│ P2  │→│ P3  │→│ P4  │        │                    │    │
│   │   │  │ Pri │ │ Pri │ │ Pri │ │ Pri │        │                    │    │
│   │   │  │high │ │ med │ │ low │ │ med │        │                    │    │
│   │   │  └─────┘ └─────┘ └─────┘ └─────┘        │                    │    │
│   │   └─────────────────────────────────────────┘                    │    │
│   │                         ↓                                        │    │
│   │                  ┌───────────┐                                   │    │
│   │                  │    CPU    │                                   │    │
│   │                  └───────────┘                                   │    │
│   └───────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):
```
① 프로세스 생성 → ② 준비 큐 진입 → ③ 단기 스케줄러 선택 → ④ 디스패처 이양 → ⑤ 실행 → ⑥ 종료/대기/선점
```

- **1단계 - 프로세스 생성 및 준비 큐 진입**:
  - 장기 스케줄러가 새 프로세스 승인
  - PCB 생성, 메모리 할당
  - 준비 큐(Ready Queue)의 끝에 추가

- **2단계 - 단기 스케줄러 선택**:
  - 스케줄링 알고리즘에 따라 다음 실행할 프로세스 선택
  - 우선순위, CPU burst, 대기 시간 등 고려
  - 타이머 인터럽트, I/O 완료, 프로세스 종료 시 호출

- **3단계 - 디스패처(Dispatcher) 실행**:
  - 현재 실행 프로세스의 상태를 PCB에 저장
  - 선택된 프로세스의 PCB에서 상태 복원
  - CPU 레지스터, PC, SP 등 복원
  - 사용자 모드로 전환, 프로세스 실행 시작

- **4단계 - 프로세스 실행**:
  - CPU burst 실행 (연산)
  - I/O 요청 시 대기 상태로 전이
  - 타임 퀀텀 만료 시 선점 (선점형 스케줄링)

- **5단계 - 전이 (Transition)**:
  - **실행 → 종료**: 프로세스 완료
  - **실행 → 대기**: I/O 요청, 이벤트 대기
  - **실행 → 준비**: 타임 퀀텀 만료, 더 높은 우선순위 도착
  - **대기 → 준비**: I/O 완료, 이벤트 발생

**핵심 알고리즘/공식** (해당 시 필수):
```
스케줄링 성능 지표:
┌─────────────────────────────────────────────────────────────────┐
│  1. CPU 이용률 (CPU Utilization)                                │
│     CPU Utilization = (총 CPU 시간 - 유휴 시간) / 총 CPU 시간    │
│     목표: 40% (저부하) ~ 90% (고부하)                           │
│                                                                 │
│  2. 처리량 (Throughput)                                         │
│     Throughput = 완료된 프로세스 수 / 단위 시간                  │
│     목표: 시스템별 상이 (실시간 < 일괄)                         │
│                                                                 │
│  3. 총처리시간 (Turnaround Time)                                │
│     TAT = 완료 시각 - 도착 시각                                  │
│     = 대기 시간 + CPU 버스트 + I/O 시간                         │
│     목표: 최소화                                                 │
│                                                                 │
│  4. 대기 시간 (Waiting Time)                                    │
│     Waiting Time = 준비 큐에서 대기한 총 시간                    │
│     목표: 최소화, 공정성 보장                                    │
│                                                                 │
│  5. 응답 시간 (Response Time)                                   │
│     Response Time = 첫 응답 시각 - 요청 시각                     │
│     목표: 대화형 시스템에서 100ms 이하                           │
└─────────────────────────────────────────────────────────────────┘

알고리즘별 성능 분석:
┌─────────────────────────────────────────────────────────────────┐
│  FCFS (First Come First Served):                                │
│  - 평균 대기시간: 변동 큼 (Convoy Effect)                        │
│  - 공정성: ★ 좋음 (도착 순서 준수)                              │
│  - 구현: 매우 간단                                               │
│                                                                 │
│  SJF (Shortest Job First):                                      │
│  - 평균 대기시간: ★ 최소 (이론적 최적)                           │
│  - 문제: CPU burst 예측 어려움, 기아(Starvation) 발생            │
│                                                                 │
│  Round Robin:                                                   │
│  - 평균 대기시간: 중간                                           │
│  - 응답시간: ★ 균등 (Time Quantum에 의존)                        │
│  - 공정성: ★ 좋음                                                │
│  - 최적 Time Quantum: 평균 CPU burst의 80%                      │
│                                                                 │
│  MLFQ (Multi-Level Feedback Queue):                             │
│  - 적응형: ★ CPU burst 특성 자동 파악                           │
│  - I/O bound: 높은 우선순위 유지                                 │
│  - CPU bound: 낮은 우선순위로 강등                               │
└─────────────────────────────────────────────────────────────────┘

에이징(Aging) 공식:
Priority_new = Priority_old + (Wait_Time / Aging_Factor)
예: 15분마다 우선순위 +1
```

**코드 예시** (필수: Python 또는 의사코드):
```python
# CPU 스케줄링 알고리즘 시뮬레이터
from dataclasses import dataclass
from typing import List, Optional
from collections import deque

@dataclass
class Process:
    pid: int
    arrival_time: int
    burst_time: int
    priority: int = 0
    remaining_time: int = 0
    start_time: int = -1
    completion_time: int = 0
    waiting_time: int = 0
    turnaround_time: int = 0

    def __post_init__(self):
        self.remaining_time = self.burst_time


class CPUScheduler:
    def __init__(self, processes: List[Process]):
        self.processes = processes
        self.timeline = []  # (pid, start, end)

    def fcfs(self) -> dict:
        """FCFS (First Come First Served) - 비선점"""
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        current_time = 0

        for p in processes:
            if current_time < p.arrival_time:
                current_time = p.arrival_time

            p.start_time = current_time
            p.waiting_time = current_time - p.arrival_time
            current_time += p.burst_time
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time

            self.timeline.append((p.pid, p.start_time, p.completion_time))

        return self._calculate_stats()

    def sjf(self) -> dict:
        """SJF (Shortest Job First) - 비선점"""
        processes = sorted(self.processes, key=lambda p: (p.arrival_time, p.burst_time))
        ready_queue = []
        current_time = 0
        completed = 0
        n = len(processes)
        idx = 0

        while completed < n:
            # 도착한 프로세스들을 준비 큐에 추가
            while idx < n and processes[idx].arrival_time <= current_time:
                ready_queue.append(processes[idx])
                idx += 1

            if not ready_queue:
                current_time = processes[idx].arrival_time
                continue

            # 가장 짧은 버스트 타임 선택
            ready_queue.sort(key=lambda p: p.burst_time)
            p = ready_queue.pop(0)

            p.start_time = current_time
            p.waiting_time = current_time - p.arrival_time
            current_time += p.burst_time
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time

            self.timeline.append((p.pid, p.start_time, p.completion_time))
            completed += 1

        return self._calculate_stats()

    def round_robin(self, time_quantum: int = 2) -> dict:
        """Round Robin - 선점형"""
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        ready_queue = deque()
        current_time = 0
        idx = 0
        n = len(processes)

        # 첫 번째 프로세스 추가
        ready_queue.append(processes[0])
        idx = 1

        while ready_queue or idx < n:
            # 도착한 프로세스 추가
            while idx < n and processes[idx].arrival_time <= current_time:
                ready_queue.append(processes[idx])
                idx += 1

            if not ready_queue:
                current_time = processes[idx].arrival_time
                continue

            p = ready_queue.popleft()

            if p.start_time == -1:
                p.start_time = current_time

            exec_time = min(time_quantum, p.remaining_time)
            self.timeline.append((p.pid, current_time, current_time + exec_time))

            current_time += exec_time
            p.remaining_time -= exec_time

            # 도착한 새 프로세스 추가
            while idx < n and processes[idx].arrival_time <= current_time:
                ready_queue.append(processes[idx])
                idx += 1

            if p.remaining_time > 0:
                ready_queue.append(p)
            else:
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time

        return self._calculate_stats()

    def priority_scheduling(self) -> dict:
        """우선순위 스케줄링 - 비선점, 에이징 적용"""
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        ready_queue = []
        current_time = 0
        completed = 0
        n = len(processes)
        idx = 0
        aging_interval = 5  # 5단위시간마다 에이징

        while completed < n:
            # 도착한 프로세스 추가 + 에이징
            while idx < n and processes[idx].arrival_time <= current_time:
                # 에이징: 대기 시간에 따른 우선순위 조정
                wait_time = current_time - processes[idx].arrival_time
                processes[idx].priority -= wait_time // aging_interval
                ready_queue.append(processes[idx])
                idx += 1

            if not ready_queue:
                current_time = processes[idx].arrival_time
                continue

            # 가장 높은 우선순위 (숫자가 작을수록 높음)
            ready_queue.sort(key=lambda p: p.priority)
            p = ready_queue.pop(0)

            p.start_time = current_time
            p.waiting_time = current_time - p.arrival_time
            current_time += p.burst_time
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time

            self.timeline.append((p.pid, p.start_time, p.completion_time))
            completed += 1

        return self._calculate_stats()

    def mlfq(self, queues: int = 3, time_quanta: List[int] = None) -> dict:
        """MLFQ (Multi-Level Feedback Queue)"""
        if time_quanta is None:
            time_quanta = [2, 4, 8]  # 각 큐의 타임 퀀텀

        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        # 각 레벨의 큐
        queues = [deque() for _ in range(queues)]
        current_time = 0
        idx = 0
        n = len(processes)

        # 첫 프로세스를 최상위 큐에 추가
        queues[0].append(processes[0])
        idx = 1

        while any(queues) or idx < n:
            # 도착한 프로세스를 최상위 큐에 추가
            while idx < n and processes[idx].arrival_time <= current_time:
                queues[0].append(processes[idx])
                idx += 1

            # 가장 높은 우선순위의 비어있지 않은 큐 찾기
            current_queue = -1
            for i, q in enumerate(queues):
                if q:
                    current_queue = i
                    break

            if current_queue == -1:
                if idx < n:
                    current_time = processes[idx].arrival_time
                    queues[0].append(processes[idx])
                    idx += 1
                continue

            p = queues[current_queue].popleft()
            quantum = time_quanta[current_queue]

            if p.start_time == -1:
                p.start_time = current_time

            exec_time = min(quantum, p.remaining_time)
            self.timeline.append((p.pid, current_time, current_time + exec_time))

            current_time += exec_time
            p.remaining_time -= exec_time

            # 도착한 새 프로세스 추가
            while idx < n and processes[idx].arrival_time <= current_time:
                queues[0].append(processes[idx])
                idx += 1

            if p.remaining_time > 0:
                # 하위 큐로 강등 (최하위면 유지)
                next_queue = min(current_queue + 1, len(queues) - 1)
                queues[next_queue].append(p)
            else:
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time

        return self._calculate_stats()

    def _calculate_stats(self) -> dict:
        """통계 계산"""
        n = len(self.processes)
        avg_waiting = sum(p.waiting_time for p in self.processes) / n
        avg_turnaround = sum(p.turnaround_time for p in self.processes) / n

        # 프로세스별 상세 정보
        details = []
        for p in self.processes:
            details.append({
                'PID': p.pid,
                'Arrival': p.arrival_time,
                'Burst': p.burst_time,
                'Start': p.start_time,
                'Completion': p.completion_time,
                'Waiting': p.waiting_time,
                'Turnaround': p.turnaround_time
            })

        return {
            'avg_waiting_time': avg_waiting,
            'avg_turnaround_time': avg_turnaround,
            'timeline': self.timeline,
            'details': details
        }


# 성능 비교 테스트
def compare_algorithms():
    print("=== CPU 스케줄링 알고리즘 비교 ===\n")

    # 테스트 프로세스
    processes = [
        Process(pid=1, arrival_time=0, burst_time=10, priority=2),
        Process(pid=2, arrival_time=1, burst_time=5, priority=1),
        Process(pid=3, arrival_time=2, burst_time=2, priority=3),
        Process(pid=4, arrival_time=3, burst_time=8, priority=2),
    ]

    algorithms = [
        ("FCFS", lambda s: s.fcfs()),
        ("SJF", lambda s: s.sjf()),
        ("Round Robin (Q=2)", lambda s: s.round_robin(2)),
        ("Priority + Aging", lambda s: s.priority_scheduling()),
        ("MLFQ", lambda s: s.mlfq()),
    ]

    results = []
    for name, algo in algorithms:
        scheduler = CPUScheduler(processes.copy())
        stats = algo(scheduler)
        results.append((name, stats))

        print(f"\n[{name}]")
        print(f"  평균 대기시간: {stats['avg_waiting_time']:.2f}")
        print(f"  평균 총처리시간: {stats['avg_turnaround_time']:.2f}")
        print(f"  타임라인: {stats['timeline']}")

    # 최적 알고리즘 찾기
    best_waiting = min(results, key=lambda x: x[1]['avg_waiting_time'])
    best_turnaround = min(results, key=lambda x: x[1]['avg_turnaround_time'])

    print(f"\n[최적 알고리즘]")
    print(f"  대기시간 최소: {best_waiting[0]} ({best_waiting[1]['avg_waiting_time']:.2f})")
    print(f"  총처리시간 최소: {best_turnaround[0]} ({best_turnaround[1]['avg_turnaround_time']:.2f})")


if __name__ == "__main__":
    compare_algorithms()
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):
| 장점 | 단점 |
|-----|------|
| **FCFS 장점**: 공정성, 구현 간단 | **FCFS 단점**: Convoy Effect, 평균 대기시간 높음 |
| **SJF 장점**: 평균 대기시간 최소 | **SJF 단점**: 기아 현상, 버스트 예측 어려움 |
| **RR 장점**: 응답시간 균등, 기아 없음 | **RR 단점**: 문맥교환 오버헤드, 퀀텀 튜닝 필요 |
| **MLFQ 장점**: 적응형, 자동 최적화 | **MLFQ 단점**: 구현 복잡, 파라미터 튜닝 어려움 |

**스케줄링 알고리즘 종합 비교** (필수: 최소 2개 대안):
| 알고리즘 | 선점 | 기아 | 응답시간 | 대기시간 | 구현 | 용도 |
|---------|------|------|----------|----------|------|------|
| **FCFS** | X | X | 나쁨 | 나쁨 | ★간단 | 교육용 |
| **SJF** | X | ★O | 좋음 | ★최소 | 중간 | 일괄 |
| **SRTF** | O | ★O | 좋음 | ★최소 | 중간 | 일괄 |
| **Priority** | 양쪽 | O | 중간 | 중간 | 중간 | 실시간 |
| **Round Robin** | O | X | ★균등 | 중간 | 간단 | ★시분할 |
| **MLQ** | O | O | 좋음 | 중간 | 복잡 | 특수 |
| **MLFQ** | O | X | ★좋음 | 중간 | ★복잡 | ★범용OS |

> **★ 선택 기준**:
> - **대화형 시스템**: Round Robin (응답시간 균등)
> - **일괄 처리**: SJF/SRTF (처리량 최대)
> - **실시간**: Priority + EDF/RMS
> - **범용 OS**: MLFQ (적응형)

**선점형 vs 비선점형 비교**:
| 특성 | 선점형 (Preemptive) | 비선점형 (Non-preemptive) |
|------|-------------------|-------------------------|
| **CPU 반납** | 강제 가능 | 자발적만 |
| **응답시간** | ★ 짧음 | 김 |
| **오버헤드** | 높음 (문맥교환) | ★ 낮음 |
| **구현** | 복잡 | ★ 간단 |
| **실시간** | ★ 적합 | 부적합 |
| **예측성** | 낮음 | ★ 높음 |

---

### Ⅳ. 실무 적용 방안 (필수: 기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **리눅스 서버** | CFS(Completely Fair Scheduler) 적용, cgroup으로 CPU 할당 제한 | 멀티테넌트 환경에서 공정성 95% 이상 |
| **실시간 시스템** | EDF(Earliest Deadline First) + Priority Inheritance Protocol | 마감시간 준수율 99.99% |
| **클라우드/컨테이너** | Kubernetes CPU Request/Limit, Completely Fair Scheduler | 리소스 격리, QoS 보장 |
| **게임 서버** | 우선순위 기반 + Real-time 스레드 분리 | 지연 10ms 이하 |

**실제 도입 사례** (필수: 구체적 기업/서비스):
- **사례 1: 리눅스 CFS** - 완전 공정 스케줄러. Red-Black Tree로 태스크 관리, 가상 런타임(vruntime) 기반 공정성. 1000+ 프로세스에서도 균등한 CPU 할당.
- **사례 2: 안드로이드** - cgroup 기반 포그라운드/백그라운드 분리. 포그라운드 앱에 95% CPU, 백그라운드에 5%. 배터리 30% 절감.
- **사례 3: Google Borg/Kubernetes** - 각 컨테이너에 CPU Request/Limit 설정. QoS Class(Guaranteed/Burstable/BestEffort)로 우선순위 관리.

**도입 시 고려사항** (필수: 4가지 관점):
1. **기술적**:
   - 워크로드 특성 분석 (CPU bound vs I/O bound)
   - 응답시간 요구사항
   - 멀티코어 스케줄링 (NUMA 고려)
   - 실시간성 요구사항

2. **운영적**:
   - 모니터링 (CPU 사용률, 대기시간)
   - 튜닝 (타임 퀀텀, 우선순위)
   - 디버깅 (스케줄링 지연 추적)
   - 로드 밸런싱

3. **보안적**:
   - DoS 공격 (CPU 독점)
   - 우선순위 조작 방지
   - cgroup 격리
   - 실시간 스레드 제한

4. **경제적**:
   - 하드웨어 비용 vs 성능
   - 멀티코어 확장성
   - 전력 소비
   - 라이선스 (실시간 OS)

**주의사항 / 흔한 실수** (필수: 최소 3개):
- ❌ **타임 퀀텀 너무 작게 설정**: 문맥교환 오버헤드 > 실제 작업 → 성능 급감
- ❌ **에이징 없는 우선순위 스케줄링**: 기아(Starvation) 발생 → 저우선순위 프로세스 무한 대기
- ❌ **실시간 스케줄링 무시**: 일반 OS 스케줄러는 마감시간 보장 안 함 → RTOS 필요

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):
```
📌 CPU 스케줄링 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│                      CPU 스케줄링                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  프로세스 ←──→ CPU스케줄링 ←──→ 문맥교환                         │
│     ↓              ↓              ↓                             │
│  PCB          인터럽트       레지스터                             │
│     ↓              ↓              ↓                             │
│  스레드        타이머        커널모드                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 프로세스 | 스케줄링 대상 | 실행 단위 | `[프로세스](./process.md)` |
| 문맥 교환 | 실행 메커니즘 | CPU 제어권 이양 | `[문맥 교환](./context_switch.md)` |
| 인터럽트 | 스케줄링 트리거 | 타이머, I/O 완료 | `[인터럽트](../01_computer_architecture/interrupt.md)` |
| 교착상태 | 부정적 결과 | 리소스 경쟁 | `[교착상태](./deadlock.md)` |
| 동기화 | 병렬 실행 제어 | 뮤텍스, 세마포어 | `[동기화](./synchronization.md)` |
| 스레드 | 경량 프로세스 | 스레드 스케줄링 | `[스레드](./thread.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| CPU 활용률 | 유휴 시간 최소화 | 85~95% 이상 |
| 응답 시간 | 대화형 시스템 | 100ms 이하 |
| 처리량 | 일괄 처리 시스템 | 프로세스/초 최대화 |
| 공정성 | 모든 프로세스 | 기아 0회 |

**미래 전망** (필수: 3가지 관점):
1. **기술 발전 방향**:
   - **에너지 인식 스케줄링**: 전력 소비 최소화 (ARM big.LITTLE)
   - **AI 기반 스케줄링**: 워크로드 예측, 적응형 튜닝
   - **실시간 리눅스 (PREEMPT_RT)**: 더 낮은 지연, 결정적 응답

2. **시장 트렌드**:
   - 클라우드/컨테이너에서의 리소스 격리 강화
   - 실시간 게임/스트리밍의 저지연 요구
   - 엣지 컴퓨팅의 전력 제약 스케줄링

3. **후속 기술**:
   - **Heterogeneous Scheduling**: CPU+GPU+NPU 통합 스케줄링
   - **Quantum Scheduling**: 양자 컴퓨팅 작업 스케줄링
   - **eBPF 스케줄링**: 커널 확장 가능한 스케줄러

> **결론**: CPU 스케줄링은 운영체제의 **가장 핵심적인 메커니즘**으로, 시스템 성능과 사용자 경험을 직접 결정한다. 알고리즘별 장단점을 이해하고, 워크로드 특성에 맞는 최적의 스케줄링 전략을 선택하는 것이 기술사의 핵심 역량이다.

> **※ 참고 표준**: POSIX.1 (sched_setscheduler), Linux CFS Documentation, Real-Time Linux Wiki, ARM big.LITTLE MP Scheduling

---

## 어린이를 위한 종합 설명 (필수)

**CPU 스케줄링은 "병원 진료 순서 정하기"야!**

병원에 환자들이 많이 왔어요. 누구부터 진료할까요?

**병원 대기열:**
```
환자1: 감기 (진료 10분)
환자2: 배탈 (진료 5분)
환자3: 콧물 (진료 2분)
환자4: 두통 (진료 8분)
```

**여러 가지 방법이 있어요:**

1. **FCFS (먼저 온 순서)**
   - 온 순서대로 진료해요
   - 환자1 → 환자2 → 환자3 → 환자4
   - 공정하지만, 감기 환자가 10분이나 걸려서 콧물 환자가 오래 기다려요 😢

2. **SJF (짧은 것부터)**
   - 진료가 짧은 사람부터!
   - 환자3(2분) → 환자2(5분) → 환자4(8분) → 환자1(10분)
   - 빠르지만, 오래 걸리는 환자는 영원히 못 볼 수도 있어요! 😰

3. **Round Robin (돌아가면서)**
   - 2분씩만 진료하고 다음 사람!
   - 환자1(2분) → 환자2(2분) → 환자3(완료!) → 환자4(2분) → ...
   - 모두가 조금씩 빨리 진료받아요! 😊

4. **우선순위 (긴급한 것부터)**
   - 응급 환자 먼저!
   - 일반 환자는 오래 기다려요... 😢
   - 그래서 **에이징**으로 오래 기다린 사람 우선순위 올려줘요!

**어떤 걸 쓸까요?**

- 🎮 **게임**: Round Robin (모두 빠르게!)
- 📊 **계산**: SJF (빨리 끝내!)
- 🏥 **병원**: 우선순위 (응급 먼저!)

CPU도 똑같아요! 여러 프로그램이 CPU를 쓰고 싶어 해요. 운영체제가 **공정하게** 나눠줘요! 🖥️

---
