+++
title = "[OS] 169. 디스패치 지연 (Dispatch Latency)"
date = "2026-03-04"
[extra]
categories = "studynote-operating-system"
tags = ["Dispatch Latency", "Scheduling", "Context Switch", "Real-time"]
+++

# 디스패치 지연 (Dispatch Latency)

## 1. 디스패치 지연 (Dispatch Latency)의 정의
- 스케줄러가 한 프로세스를 중단시키고 다른 프로세스를 실행하기 시작할 때까지 걸리는 시간
- 실시간 시스템(Real-time System)의 응답 성능을 결정하는 핵심 지표

## 2. 디스패치 지연의 구성 요소

### 2.1 주요 발생 원인
1. **Context Switch:** 현재 실행 중인 프로세스의 상태 저장 및 새 프로세스의 상태 복원
2. **Scheduling Time:** 다음에 실행할 최적의 프로세스를 결정하는 알고리즘 수행 시간
3. **Interrupt Handling:** 실행 중인 인터럽트 서비스 루틴(ISR)의 완료 대기 시간
4. **Preemption Latency:** 커널 모드에서 실행 중인 작업을 중단시키기 위한 커널 선점 가능 여부 확인 및 처리

### 2.2 디스패치 지연 과정 (ASCII)
```text
[ Process A Running ]
          |
 (Interrupt/Event) -> Context Save (Process A)
          |
 [ Dispatch Latency Start ]
          |
   1. Scheduling Algorithm execution
   2. Context Restore (Process B)
          |
 [ Dispatch Latency End ]
          |
[ Process B Running ]
```

## 3. 디스패치 지연 감소 기법

### 3.1 운영체제 설계 측면
- **Preemptive Kernel:** 커널 모드에서도 안전하게 선점을 허용하여 지연을 최소화함
- **Optimized Scheduling:** O(1) 또는 O(log N) 스케줄링 알고리즘 적용
- **Deferred Interrupt Handling:** 긴 ISR을 후반부 처리(Bottom Half)로 분리

### 3.2 하드웨어 측면
- **Register Windows:** 하드웨어 레지스터 세트를 여러 개 두어 문맥 교환 속도 향상 (SPARC 등)

## 4. 기술사적 견해: 디스패치 지연의 중요성
- 임베디드 및 자율주행 시스템과 같은 경성 실시간(Hard Real-time) 환경에서는 평균 지연시간보다 '최악의 경우 지연시간(WCET)'의 보장이 더 중요함
- 따라서 커널 내부의 임계 구역(Critical Section) 길이를 최소화하고 스핀락 점유 시간을 관리하는 것이 시스템 안정성의 핵심임
