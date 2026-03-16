+++
title = "[OS] 191. 스레드 스케줄링 (Thread Scheduling)"
date = "2026-03-04"
[extra]
categories = "studynote-operating-system"
tags = ["Thread Scheduling", "PCS", "SCS", "Kernel Level Thread"]
+++

# 스레드 스케줄링 (Thread Scheduling)

## 1. 스레드 스케줄링 (Thread Scheduling)의 정의
- 운영체제가 CPU 실행 단위를 프로세스가 아닌 스레드 수준에서 관리하고 결정하는 과정
- 커널 수준 스레드(KLT)와 사용자 수준 스레드(ULT)에 따라 스케줄링 주체와 방식이 달라짐

## 2. 스레드 스케줄링의 두 가지 범위 (Scope)

### 2.1 프로세스 경쟁 범위 (PCS, Process-Contention Scope)
- 사용자 수준 스레드(ULT)가 동일한 프로세스 내의 다른 스레드들과 CPU(또는 LWP)를 차지하기 위해 경쟁하는 범위
- 보통 스레드 라이브러리(Pthreads 등)가 관리함

### 2.2 시스템 경쟁 범위 (SCS, System-Contention Scope)
- 커널 수준 스레드(KLT)가 시스템 전체의 다른 스레드들과 경쟁하는 범위
- 운영체제 커널 스케줄러가 직접 관리함

### 2.3 스케줄링 계층도 (ASCII)
```text
[ User Space ]    Thread 1  Thread 2  Thread 3
                      \        |       /
                     ( PCS - Library Scheduling )
                           \   |   /
[ Kernel Space ]            [ LWP ]
                               |
                     ( SCS - Kernel Scheduling )
                               |
[ Hardware ]                 [ CPU ]
```

## 3. 기술사적 견해: 현대 운영체제의 선택
- 현대 대부분의 운영체제(Linux, Windows, Solaris 등)는 1:1 스레딩 모델을 채택하여 **시스템 경쟁 범위(SCS)** 방식의 스케줄링을 기본으로 함
- 이는 커널이 모든 실행 흐름을 인지하게 하여 다중 프로세서 환경에서 최적의 병렬성을 확보하기 위함임
