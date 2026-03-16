+++
title = "[OS] 186. MLFQ 파라미터 (Multi-Level Feedback Queue Parameters)"
date = "2026-03-04"
[extra]
categories = "studynote-operating-system"
tags = ["MLFQ", "Scheduling Parameters", "Priority", "Time Quantum"]
+++

# MLFQ 파라미터 (Multi-Level Feedback Queue Parameters)

## 1. MLFQ (Multi-Level Feedback Queue)의 정의
- 프로세스의 CPU 버스트 행태에 따라 큐 사이를 이동시키는 다단계 피드백 큐 스케줄링 방식
- 가장 복잡하지만, 다양한 워크로드에 대해 유연하게 대응 가능한 범용 스케줄러

## 2. MLFQ를 정의하는 5가지 핵심 파라미터

| 파라미터 | 설명 |
|---|---|
| **큐의 개수** | 시스템이 유지하는 준비 큐의 총수 |
| **각 큐의 스케줄링 알고리즘** | 각 단계별 큐가 사용하는 방식(예: RR, FCFS 등) |
| **강격(Promotion) 조건** | 프로세스를 높은 우선순위 큐로 이동시키는 규칙 (에이징 기법 등) |
| **강등(Demotion) 조건** | 프로세스를 낮은 우선순위 큐로 이동시키는 규칙 (타임 슬라이스 소진 등) |
| **큐 진입 결정 방식** | 프로세스가 처음 시스템에 들어올 때 어느 큐에 배치할지 결정하는 규칙 |

### 2.1 동작 원리 개념도 (ASCII)
```text
(New Process) -> [ Q0: Time Quantum 8ms ] (High Priority)
                    | (Quantum expired)
                    v
                 [ Q1: Time Quantum 16ms ] (Medium Priority)
                    | (Quantum expired)
                    v
                 [ Q2: FCFS / RR 64ms ] (Low Priority)
```

## 3. 기술사적 견해: 파라미터 튜닝의 중요성
- MLFQ의 성능은 위 5가지 파라미터를 어떻게 설정하느냐에 따라 극명하게 달라짐
- 현대 리눅스의 CFS(Completely Fair Scheduler)는 엄밀히 말하면 MLFQ는 아니지만, vruntime과 가중치를 통해 MLFQ가 해결하려던 '공정성'과 '응답성'의 문제를 더 정교하게 해결하고 있음
