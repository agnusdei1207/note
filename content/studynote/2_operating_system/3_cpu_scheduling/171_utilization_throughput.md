+++
title = "[OS] 171. CPU 이용률 (Utilization) 및 처리량 (Throughput)"
date = "2026-03-04"
[extra]
categories = "studynote-operating-system"
tags = ["CPU Utilization", "Throughput", "Scheduling Criteria"]
+++

# CPU 이용률 (Utilization) 및 처리량 (Throughput)

## 1. 개요: 스케줄링의 성능 지표
- CPU 스케줄링 알고리즘을 평가하기 위해 사용되는 주요 시스템 중심(System-oriented) 성능 척도

## 2. CPU 이용률 (CPU Utilization)
- 전체 시간 대비 CPU가 실제 작업을 수행한 시간의 비율 (%)
- **목표:** 가능한 CPU가 쉬지 않도록(Busy) 유지하는 것 (보통 40% ~ 90% 유지)

## 3. 처리량 (Throughput)
- 단위 시간당 완료되는 프로세스의 개수
- **목표:** 주어진 시간 내에 최대한 많은 프로세스를 완료시키는 것

### 3.1 상호 관계 및 수식 (ASCII)
```text
  CPU Utilization = (Busy Time / Total Time) * 100
  Throughput = (Total Completed Processes / Total Time)
  
  [ 관계성 ]
  Throughput ↑  ->  System Efficiency ↑
  Utilization ↑ ->  Resource Management Efficiency ↑
```

## 4. 기술사적 견해: 성능 최적화의 균형
- 높은 CPU 이용률이 항상 좋은 것은 아님 (90% 이상은 시스템 병목 유발 가능)
- 따라서 처리량을 최대화하되, 응답 시간과 대기 시간을 적절히 고려한 '시스템 수용력(Capacity)' 설계가 필요함
