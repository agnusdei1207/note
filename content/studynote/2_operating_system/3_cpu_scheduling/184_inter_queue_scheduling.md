+++
title = "[OS] 184. 큐 간 스케줄링 (Inter-queue Scheduling)"
date = "2026-03-04"
[extra]
categories = "studynote-operating-system"
tags = ["Multi-level Queue", "Inter-queue Scheduling", "Fixed Priority", "Time Slice"]
+++

# 큐 간 스케줄링 (Inter-queue Scheduling)

## 1. 큐 간 스케줄링 (Inter-queue Scheduling)의 정의
- 여러 개의 준비 큐(Ready Queue)가 존재하는 다단계 큐(Multi-level Queue) 시스템에서, 어느 큐에 CPU를 할당할지 결정하는 방식
- 큐 자체의 우선순위 또는 자원 배분 비율을 정의함

## 2. 큐 간 스케줄링의 주요 방식

### 2.1 고정 우선순위 스케줄링 (Fixed Priority Scheduling)
- 높은 우선순위 큐가 비어있지 않으면 낮은 우선순위 큐는 CPU를 할당받지 못함
- **특징:** 기아(Starvation) 현상이 발생할 가능성이 큼

### 2.2 시간 할당 스케줄링 (Time Slice Scheduling)
- 각 큐에 CPU 시간의 일정 비율(예: 80%는 시스템 큐, 20%는 사용자 큐)을 할당하는 방식
- **특징:** 모든 큐에 최소한의 CPU 시간을 보장하여 기아 현상을 완화함

### 2.3 큐 구조 및 배분 예시 (ASCII)
```text
[ Queue A: System Processes ] --- (80% CPU Time) ---+
                                                    |
[ Queue B: Interactive Tasks ] --- (15% CPU Time) ---|---> [ CPU ]
                                                    |
[ Queue C: Batch Processes ]   --- ( 5% CPU Time) ---+
```

## 3. 기술사적 견해: 정적 큐 vs 동적 큐의 조화
- 현대 OS는 단순 큐 간 스케줄링을 넘어, MLFQ와 같이 큐 사이를 프로세스가 이동할 수 있게 하여 처리 효율을 높임
- 시스템 응답성과 처리량의 균형을 위해 각 큐의 특성에 맞는 워크로드 배분이 중요함
