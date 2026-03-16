+++
weight = 647
title = "647. 성능 모니터링 (Performance Monitoring)"
date = "2026-03-16"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "성능 모니터링", "Performance Monitoring", "메트릭", "프로파일링", "APM"]
+++

# 성능 모니터링 (Performance Monitoring)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 성능 모니터링은 시스템의 **CPU, 메모리, 디스크, 네트워크 사용량을 실시간으로 수집, 분석, 경고**하여 성능 병목을 조기 발견하는 활동이다.
> 2. **가치**: "느려졌는데 왜 그럴까?"라는 질문에 **데이터 기반 답변**을 제공하며, 용량 계획, SLA 준수, 장애 예방을 가능하게 한다.
> 3. **융합**: Prometheus, Grafana, Datadog, New Relic 등 **옵서버빌리티(Observability)** 스택이 Logs + Metrics + Traces를 통합한다.

---

## Ⅰ. 성능 모니터링의 개요

### 1. 정의
- 성능 모니터링은 시스템 자원 사용량과 응답 시간을 측정하여 성능을 최적화하는 활동이다.

### 2. 등장 배경
- "시스템이 느린데 어디서 병목이지?"라는 문제 해결 필요

### 3. 💡 비유: '자동차 계기판'
- 성능 모니터링은 **'자동차의 계기판(속도계, RPM, 연료량)'**과 같다.
- 계기판을 보면 과속(과부하)인지, 연료 부족(리소스 부족)인지 알 수 있다.

---

## Ⅱ. 모니터링 대상 (Deep Dive)

### 1. 4대 리소스
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                    모니터링 대상 리소스                          │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [CPU]                                                          │
    │   - 사용율 (%), Load Average, Context Switch                   │
    │   - 프로세스별 CPU 사용량                                       │
    │                                                                 │
    │  [Memory]                                                       │
    │   - 사용량, 여유량, Swap 사용                                   │
    │   - Cache/Buffer vs Active/Inactive                            │
    │                                                                 │
    │  [Disk I/O]                                                     │
    │   - IOPS, Throughput (MB/s), Latency (ms)                      │
    │   - Queue Depth, Await Time                                    │
    │                                                                 │
    │  [Network]                                                      │
    │   - TX/RX (bps, pps), Errors, Drops                            │
    │   - Connection 수, Retransmit                                  │
    │                                                                 │
    │  [Application]                                                  │
    │   - Response Time, Throughput, Error Rate                      │
    │   - Apdex Score (만족도)                                       │
    └─────────────────────────────────────────────────────────────────┘
```

### 2. Load Average
- **1분, 5분, 15분 평균 실행 대기열 큐기**
- 예: 2.5 = 평균 2.5개 프로세스가 실행 대기 중
- **Core 수와 비교**: 4코어에서 LA=4는 100% 사용

---

## Ⅲ. 모니터링 도구

### 1. Linux 기본 도구
| 도구 | 용도 | 예시 |
|:---|:---|:---|
| **top/htop** | 실시간 CPU/메모리 | `top` |
| **vmstat** | 시스템 통계 | `vmstat 1` |
| **iostat** | I/O 통계 | `iostat -x 1` |
| **netstat/ss** | 네트워크 연결 | `ss -s` |
| **sar** | 역사적 데이터 수집 | `sar -u 1 5` |

### 2. 응용 프로그램 모니터링
```bash
# strace로 시스템 콜 추적
strace -p <PID>

# perf로 프로파일링
perf top

# flamegraph로 시각화
FlameGraph
```

---

## Ⅳ. 모니터링 스택 (Prometheus + Grafana)

### 1. 아키텍처
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │             Prometheus + Grafana 모니터링 스택                   │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [Targets]                                                      │
    │   ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
    │   │ Node     │  │ App      │  │ Database │                   │
    │   │ Exporter │  │ Metrics  │  │ Exporter │                   │
    │   └─────┬────┘  └─────┬────┘  └─────┬────┘                   │
    │         │              │              │                        │
    │         └──────────────┴──────────────┘                        │
    │                        │ /metrics                              │
    │                        ▼                                       │
    │  ┌─────────────────────────────────────────────────────────┐   │
    │  │              Prometheus (TSDB)                          │   │
    │  │   - 수집 (Pull-based)                                   │   │
    │  │   - 저장 (시계열 데이터베이스)                          │   │
    │  │   - PromQL 쿼리                                         │   │
    │  └───────────────────────┬─────────────────────────────────┘   │
    │                          │                                      │
    │                          ▼                                      │
    │  ┌─────────────────────────────────────────────────────────┐   │
    │  │                Grafana (대시보드)                       │   │
    │  │   - 시각화                                              │   │
    │  │   - 알림 (Alertmanager)                                 │   │
    │  └─────────────────────────────────────────────────────────┘   │
    │                                                                 │
    │  * Pushgateway: Push-based 메트릭 수집 (일시적 작업)              │
    └─────────────────────────────────────────────────────────────────┘
```

### 2. PromQL 예시
```promql
# CPU 사용율
rate(process_cpu_seconds_total[5m])

# 메모리 사용량
process_resident_memory_bytes{job="api"}

# Request 레이트
rate(http_requests_total[1m])

# P95 레이턴시
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

---

## Ⅴ. APM (Application Performance Monitoring)

### 1. APM 기능
- **Code Profiling**: 함수별 실행 시간
- **Database Query**: 느린 쿼리 식별
- **External Calls**: HTTP/gRPC 호출 추적
- **Error Tracking**: 예외/에러 수집

### 2. Distributed Tracing
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                 Distributed Tracing 예시                        │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  Client ──▶ API Gateway ──▶ Service A ──▶ Service B           │
    │     │          │               │              │                 │
    │     │          Trace ID        │              │                 │
    │     │          Span 1          │ Span 2       │ Span 3         │
    │     │                          │              │                 │
    │     └──────────────────────────┴──────────────┴─────────       │
    │                           Trace                                │
    │                                                                 │
    │  * 각 요청을 고유 Trace ID로 추적                              │
    │  * OpenTelemetry 표준                                          │
    └─────────────────────────────────────────────────────────────────┘
```

---

## Ⅵ. 실무 적용

### 1. 모범 사례
1. **SLI/SLO 정의**: 측정 가능한 목표 설정
2. **Alerting**: 단순 임계값보다 추세 기반
3. **대시보드**: 한눈에 보는 KPI
4. **Retention**: 비용 대비 데이터 보관 기간

### 2. 안티패턴
- **"지나친 메트릭"**: 너무 많으면 야생에서 못 봄
- **"경보 피로"**: 자주 울리면 무시하게 됨
- **"모니터링 없음"**: "느리다"는 감각만 의존

---

## Ⅶ. 기대효과 및 결론

### 1. 정량/정성 기대효과
- **조기 경고**: 사용자가 느끼기 전에 발견
- **데이터 기반 의사결정**: "추가 서버 필요?"

### 2. 미래 전망
- **AI/ML 기반 이상 탐지**
- **Observability 통합**: Logs + Metrics + Traces

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **[시스템 성능 튜닝](./648_performance_tuning.md)**: 모니터링 후 다음 단계
- **[로그 분석](./580_audit_logging.md)**: 로그 기반 모니터링
- **[프로파일링](./xx_profiling.md)**: 상세 성능 분석

---

## 👶 어린이를 위한 3줄 비유 설명
1. 성능 모니터링은 **"자동차 계기판"** 같아요.
2. 속도계(CPU), 연료계(메모리), 엔진 온도(디스크)를 보면 차가 어떤 상태인지 알 수 있죠.
3. 계기판이 없으면 과속하거나 연료가 떨어져도 모르고 사고가 나겠죠?
