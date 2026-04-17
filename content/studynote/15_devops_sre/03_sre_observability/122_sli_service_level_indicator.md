+++
weight = 122
title = "서비스 수준 지표 (SLI, Service Level Indicator)"
date = "2025-05-22"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
- **SLI (Service Level Indicator)**: 서비스가 약속된 수준을 잘 지키고 있는지 판단하기 위해 "무엇을 측정할 것인가"를 정의한 구체적인 정량적 수치.
- **주요 지표 (Golden Signals)**: 응답 지연 시간(Latency), 처리량(Traffic), 오류율(Error Rate), 가용성(Availability) 등이 대표적임.
- **기술사적 관점**: 시스템의 모든 것을 측정하는 것이 아니라, "사용자 경험과 직접적으로 연결된 핵심 지표"를 선별하여 데이터 기반 의사결정의 기초로 활용함.

### Ⅰ. 개요 (Context & Background)
마이크로서비스(MSA)와 같은 분산 시스템에서 수천 개의 메트릭 중 무엇이 서비스의 건강 상태를 대변하는지 파악하는 것은 매우 어렵습니다. SRE(Site Reliability Engineering)는 서비스 수준을 관리하기 위해 먼저 "성공"의 기준이 되는 정량적 지표인 SLI를 명확히 정의하는 것에서 시작합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
사용자 요청부터 시스템 내부 처리까지의 흐름에서 SLI가 추출되는 지점과 유형별 아키텍처입니다.

```text
[ Service Delivery Flow & SLI Extraction Points ]

   (User) --> [ API Gateway ] --> [ Microservice ] --> [ DB / Cache ]
     ^              |                   |                  |
     |              | SLI: Latency      | SLI: Error Rate  | SLI: Saturation
     +--------------+-------------------+------------------+
                            |
                            v
               [ Telemetry & Observability Pipeline ]
               (Prometheus / Grafana / Datadog)
                            |
               [ SLI Calculation: (Success / Total) * 100 ]
```

**핵심 원리 및 유형:**
1. **가용성 (Availability)**: 전체 요청 수 중 성공적으로 응답한 비율. (Error rate의 역산)
2. **지연 시간 (Latency)**: 요청이 처리되어 응답이 돌아오기까지 걸린 시간. (P99, P95 등 백분위수 활용)
3. **처리량 (Throughput/Traffic)**: 단위 시간당 시스템에 가해지는 부하 수준 (QPS, TPS).
4. **포화도 (Saturation)**: 시스템 자원 중 얼마나 쓰이고 있는지 (CPU 90% 사용 등), 즉 시스템의 한계를 측정.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 지표 유형 | 측정 방식 (Measurement) | 사용자 체감 (User Experience) | 비고 (Remarks) |
| :--- | :--- | :--- | :--- |
| **성공률 (Success Rate)** | (성공한 요청 수 / 전체 요청 수) | 서비스의 동작 여부 | 2xx/3xx vs 4xx/5xx |
| **지연 (Latency)** | ms (milliseconds) | 서비스의 쾌적함 | 꼬리 지연(Tail Latency) 주의 |
| **포화도 (Saturation)** | % (Percentage) | 향후 장애 예측 | 큐 대기 시간 증가의 전조 |
| **품질 (Quality)** | 서비스 기능의 완성도 | 콘텐츠의 정확성 | 저하된 모드(Degraded mode) 고려 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **적용 전략 (Implementation Strategy)**:
  * **백분위수(Percentiles) 사용**: 평균값(Average)은 극단적인 장애 상황을 가릴 수 있으므로, 최악의 1% 사용자가 겪는 고통을 측정하기 위해 P99, P99.9 지표를 반드시 사용해야 함.
  * **측정 지점 선정**: 사용자에게 가장 가까운 지점(예: 로드밸런서 로그)에서 측정하는 것이 실제 사용자 경험을 가장 잘 대변함.
* **기술사적 판단 (Architectural Judgment)**:
  * 모든 SLI가 동등한 가치를 갖는 것은 아님. 비즈니스 크리티컬한 경로(로그인, 결제 등)에 대한 SLI를 우선순위화해야 하며, 이를 위해 '사용자 여정(User Journey)' 맵핑이 선행되어야 함. 또한 SLI는 기술적 수치(CPU)보다는 비즈니스적 가치(결제 성공)에 가까워야 함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
정확한 SLI 정의는 SLO(목표) 수립의 필수 전제조건입니다. 향후에는 AI가 시스템의 행동 패턴을 학습하여 이상 징후를 스스로 감지하고, "무엇이 핵심 지표인지"를 역으로 제안하는 자동화된 SLI 발굴 시스템이 표준으로 자리 잡을 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **SRE 프레임워크**: SLI → SLO → SLA, Error Budget
* **측정 방법론**: 4 Golden Signals, USE Method, RED Method
* **도구**: OpenTelemetry, Prometheus, Grafana

### 👶 어린이를 위한 3줄 비유 설명
1. 학교 성적표에서 국어 점수, 수학 점수처럼 내가 공부를 얼마나 잘했는지 보여주는 '점수 숫자' 그 자체가 바로 SLI예요.
2. 운동 선수가 얼마나 빨리 달렸는지 재는 '초 시계의 숫자'라고 생각해도 쉬워요.
3. 이 숫자가 높거나 낮음을 보고 내가 지금 잘하고 있는지, 아니면 더 노력해야 하는지 알 수 있답니다.
