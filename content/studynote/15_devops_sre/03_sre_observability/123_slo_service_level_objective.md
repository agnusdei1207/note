+++
weight = 123
title = "서비스 수준 목표 (SLO, Service Level Objective)"
date = "2025-05-22"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
- **SLO (Service Level Objective)**: SLI(지표)가 도달해야 하는 구체적인 목표 범위(Target range)로, "우리의 서비스는 얼마나 안정적이어야 하는가?"에 대한 답.
- **가용성 보증**: 100% 가용성은 불가능함을 인정하고, 적절한 목표(예: 99.9%)를 설정하여 시스템 안정성과 배포 속도 간의 균형을 맞춤.
- **의사결정 도구**: SLO는 단순한 목표가 아니라, 에러 예산(Error Budget) 산출의 근거가 되어 팀의 개발 우선순위를 결정하는 핵심 기준임.

### Ⅰ. 개요 (Context & Background)
엔지니어링 팀은 항상 '새로운 기능의 빠른 출시'와 '시스템의 완벽한 안정성' 사이에서 충돌합니다. SLO는 이 갈등을 해결하기 위한 정량적 타협점입니다. 비즈니스 가치와 사용자 기대치를 바탕으로 목표치를 설정함으로써, 감정이 아닌 데이터에 기반한 의사결정 체계를 구축할 수 있습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
SLO를 설정하고 관리하는 계층 구조와 에러 예산의 연계 아키텍처입니다.

```text
[ SLO Management & Error Budget Architecture ]

     "Business Requirements" --> [ SLO Target (e.g., 99.9%) ]
                                        |
     "Measured SLIs" (Actuals) ----+    | (Target - Actual = Budget)
                                   |    v
                   [ Error Budget Calculation Engine ]
                   (Remaining Budget: 0.1% - Actual Failures)
                                   |
           +-----------------------+-----------------------+
           |                                               |
  [ Budget Left > 0 ]                            [ Budget Spent <= 0 ]
  -> Safe to Deploy New Features                 -> Freeze Deployments!
  -> Risk-taking possible                        -> Focus on Reliability
```

**핵심 원리:**
1. **목표 범위 (Target Range)**: 보통 '9'의 개수로 표현됨. 99.9%(Three Nines)는 한 달에 약 43분의 장애가 허용됨을 의미.
2. **측정 윈도우 (Windowing)**: 보통 28일 또는 30일 이동 평균(Rolling Window)을 사용하여 현재 상태를 평가.
3. **사용자 기대치 반영**: 너무 높은 SLO는 비용 낭비를 초래하고, 너무 낮은 SLO는 사용자 이탈을 유발함. "사용자가 불만을 느끼기 직전"이 가장 적절한 목표치.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | SLI (Indicator) | SLO (Objective) | SLA (Agreement) |
| :--- | :--- | :--- | :--- |
| **정의** | 측정하는 값 (Value) | 목표하는 값 (Target) | 법적/금전적 약속 (Contract) |
| **질문** | "무엇을 재는가?" | "얼마나 잘해야 하는가?" | "약속을 못 지키면 어떻게 할 것인가?" |
| **대상** | 엔지니어링 텔레메트리 | 개발/운영 팀 공동 목표 | 외부 고객 / 비즈니스 파트너 |
| **엄격함** | 가장 상세함 | 중간 (SLA보다 높게 설정) | 가장 낮음 (위약금 방어용) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **적용 전략 (Implementation Strategy)**:
  * **SLO 초과 달성 방지**: SLO보다 시스템이 너무 안정적이면 사용자가 그 고가용성에 중독되므로, 일부러 정기 점검을 수행하여 에러 예산을 소모함으로써 사용자의 기대치를 관리할 필요가 있음.
  * **점진적 수립**: 처음부터 완벽한 SLO를 잡으려 하지 말고, 과거 데이터를 바탕으로 '현재 가능한 수준'에서 시작하여 점진적으로 강화.
* **기술사적 판단 (Architectural Judgment)**:
  * SLO는 "실패를 허용하는 용기"를 주는 도구임. 에러 예산이 남아 있다면 카오스 엔지니어링이나 대규모 인프라 변경을 과감하게 시도할 수 있는 근거가 됨. 또한, 특정 마이크로서비스의 SLO는 상위 서비스의 SLO에 종속되므로 계층적인 SLO 설계가 필수적임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
SLO는 데이터 기반의 협업 문화를 완성합니다. 향후에는 비즈니스 지표(매출, 리텐션)와 시스템 SLO를 실시간으로 연동하여, 수익을 극대화할 수 있는 최적의 안정성 목표치를 AI가 동적으로 조정하는 'Dynamic SLO' 기술이 표준화될 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **SRE 핵심**: SLI/SLO/SLA, Error Budget, Blameless Post-mortem
* **운영 지표**: Availability (99.x%), Latency Thresholds, MTTR
* **비즈니스 연계**: Customer Satisfaction, Retention Rate, TCO

### 👶 어린이를 위한 3줄 비유 설명
1. "이번 학기 수학 점수를 90점 이상 받겠다"라고 스스로 세운 목표가 바로 SLO예요.
2. 만약 100점을 목표로 하면 너무 힘들어서 놀지도 못하니까(비용 증가), 친구들과 놀 시간도 챙기면서 공부도 잘할 수 있는 적당한 목표(90점)를 잡는 거예요.
3. 이 목표를 지키면 칭찬을 받고, 못 지키면 게임 시간을 줄이고 공부에 더 집중하기로 약속하는 것과 같답니다.
