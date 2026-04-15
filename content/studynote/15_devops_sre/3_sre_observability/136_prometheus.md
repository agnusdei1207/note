+++
weight = 136
title = "프로메테우스 (Prometheus)"
date = "2026-03-04"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
- 프로메테우스는 클라우드 네이티브 환경의 사실상 표준(De Facto Standard) 메트릭 수집 및 경고 시스템으로, 시계열 데이터베이스(TSDB)를 내장하고 있다.
- 에이전트가 데이터를 밀어넣는 방식(Push)이 아닌, 서버가 주기적으로 엔드포인트에서 데이터를 당겨오는 **Pull 방식**의 아키텍처를 채택하여 수집 대상의 부하를 줄인다.
- 강력한 쿼리 언어인 PromQL을 통해 실시간 지표 분석과 유연한 알람 설정을 지원하며, 그라파나(Grafana)와 결합하여 최상의 시각화를 제공한다.

### Ⅰ. 개요 (Context & Background)
SoundCloud에서 개발하여 CNCF에 기부된 프로메테우스는 MSA와 쿠버네티스 환경에 최적화되어 있다. 동적인 서비스 디스커버리(Service Discovery) 기능을 통해 수시로 생성되고 사라지는 컨테이너들을 자동으로 감지하고 모니터링 대상으로 등록할 수 있어, 현대 인프라 운영의 핵심 도구로 자리 잡았다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
프로메테우스는 **HTTP Pull 모델**과 **다차원 데이터 모델(Label)**을 기반으로 동작한다.

```text
[ Prometheus Architecture / 프로메테우스 아키텍처 ]

  [ Targets ] <---- (Pull Metrics) ---- [ Prometheus Server ] ----> [ Alertmanager ]
  - Apps (Exporter)                      - Retrieval                 - Alert Push
  - K8s Nodes                            - TSDB Storage
  - Pushgateway (Short-lived jobs)       - PromQL Engine

             ^                                  |
             | (Service Discovery)              v
       [ K8s API / EC2 ]                [ Visualization (Grafana) ]

1. Retrieval: Pull metrics from HTTP /metrics endpoints.
2. Storage: Save as time-series data with Labels (key=value).
3. PromQL: Query engine for analysis (e.g., rate(http_requests_total[5m])).
```

- **Exporter:** 하둡, MySQL, OS 지표 등을 프로메테우스 포맷으로 변환하여 노출하는 에이전트.
- **Pushgateway:** 배치 작업 등 Pull이 불가능한 짧은 수명(Short-lived) 작업을 위한 버퍼.
- **Service Discovery:** 쿠버네티스 API 등을 통해 모니터링 대상을 자동으로 식별.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 프로메테우스 (Prometheus) | ELK 스택 (Elasticsearch) |
| :--- | :--- | :--- |
| **데이터 유형** | 메트릭 (수치형 시계열) | 로그 (텍스트 기반 이벤트) |
| **수집 방식** | Pull 기반 (주기적 수집) | Push 기반 (로그 발생 시 전송) |
| **주 목적** | 인프라 상태 감시 및 알람 | 문제 발생 시 상세 원인 분석(디버깅) |
| **저장 용량** | 상대적으로 적음 (수치 데이터) | 매우 큼 (전문 텍스트 저장) |
| **시너지 효과** | 프로메테우스로 장애 감지 후, ELK 로그로 상세 원인 파악 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **신뢰성 최우선:** 프로메테우스는 "시스템이 죽었을 때 알람을 보낼 수 있어야 한다"는 원칙에 충실하다. 따라서 다른 인프라에 의존하지 않는 단일 바이너리 독립 실행이 가능하도록 설계되었다.
- **고가용성(HA) 전략:** 기본적으로 단일 서버 아키텍처이므로, 대규모 환경에서는 Thanos나 Cortex 같은 솔루션을 결합하여 멀티 클러스터 통합 및 장기 데이터 보관을 실현해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
프로메테우스는 OpenTelemetry와 같은 표준과의 호환성을 강화하며 옵저버빌리티 생태계의 중심축을 지키고 있다. 쿠버네티스 운영자에게 프로메테우스는 선택이 아닌 필수이며, 이를 통해 인프라의 가시성을 확보하고 장애 복구 시간(MTTR)을 단축하는 핵심 자산이 된다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** SRE (Site Reliability Engineering), 옵저버빌리티
- **핵심 요소:** PromQL, Exporter, Alertmanager
- **연관 기술:** 쿠버네티스, 그라파나, Thanos, OpenTelemetry

### 👶 어린이를 위한 3줄 비유 설명
- 학교 선생님(서버)이 학생들(앱)의 가방을 돌아가면서 열어보고 숙제(메트릭)를 잘했는지 확인하는 방식이에요.
- 숙제를 안 한 학생이 있으면 즉시 교무실(알람)에 알려줘요.
- 학생이 전학 오거나 가도 선생님이 바로 알아채서 체크 리스트를 업데이트한답니다!
