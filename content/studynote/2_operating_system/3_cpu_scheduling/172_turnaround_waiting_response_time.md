+++
title = "[OS] 172. 반환/대기/응답 시간 (Turnaround, Waiting, Response Time)"
date = "2026-03-04"
[extra]
categories = "studynote-operating-system"
tags = ["Turnaround Time", "Waiting Time", "Response Time", "Scheduling Criteria"]
+++

# 반환, 대기, 응답 시간 (Turnaround, Waiting, Response Time)

## 1. 개요: 사용자 중심 성능 지표
- 개별 사용자가 시스템에서 느끼는 서비스 품질을 평가하는 핵심 척도

## 2. 주요 시간의 정의 및 공식

### 2.1 반환 시간 (Turnaround Time)
- 프로세스 제출 시점부터 실행이 완료될 때까지의 총 소요 시간
- **공식:** `Turnaround Time = (Exit Time - Arrival Time)` or `(Waiting Time + Service Time)`

### 2.2 대기 시간 (Waiting Time)
- 프로세스가 준비 큐(Ready Queue)에서 대기하며 소비한 시간의 총합
- **공식:** `Waiting Time = (Turnaround Time - Service Time)`

### 2.3 응답 시간 (Response Time)
- 프로세스가 최초로 CPU를 할당받아 응답을 시작할 때까지의 시간
- **공식:** `Response Time = (First Execution Start Time - Arrival Time)`

## 3. 지표 간의 타임라인 비교 (ASCII)
```text
Arrive    Start           End
  |---------|--------------|
  [ Waiting ] [ Execution  ]
  <------- Turnaround ----->
  <-- Resp ->
```

## 4. 기술사적 견해: 시분할 시스템에서의 응답성 보장
- 현대의 인터랙티브 시스템에서는 반환 시간보다 **응답 시간의 최소화**와 **대기 시간의 공정성**이 더 중시됨
- 따라서 라운드 로빈(RR) 스케줄링의 타임 퀀텀(Time Quantum) 최적화 등을 통해 사용자 경험(UX)을 극대화하는 설계가 요구됨
