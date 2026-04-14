+++
weight = 127
title = "온콜 (On-call) 관리"
date = "2024-03-23"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
- 온콜은 장애 발생 시 즉각 대응하기 위해 대기하는 업무로, SRE 팀의 가용성과 시스템 신뢰성을 보장하는 핵심 프로세스다.
- 과도한 경보(Alert Fatigue)와 불합리한 교대 근무는 엔지니어의 건강과 시스템 품질을 저해하므로 정교한 관리 전략이 필수적이다.
- '의미 있는 경보'에만 반응하도록 SLI/SLO 기반의 경보 시스템을 구축하고, 장애 대응 후에는 반드시 포스트모템을 거쳐야 한다.

### Ⅰ. 개요 (Context & Background)
- **정의**: 특정 기간 동안 시스템의 가용성과 안정성을 책임지고 대기하며, 긴급 상황 발생 시 응급 조치를 수행하는 업무 형태다.
- **배경**: 24/7 중단 없는 서비스가 보편화되면서 야간이나 휴일에도 장애를 해결할 엔지니어가 상시 대기해야 할 필요성이 커졌다. 하지만 무분별한 온콜은 팀의 생산성을 떨어뜨리는 주범이 된다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
[ On-call Management Workflow ]

 (System) ---[Threshold Check]---> (Monitoring Tools)
                                       |
 [ High Priority Alert ] <-------------+-------------> [ Low Priority Alert ]
          |                                                   |
 (Pager/Notification)                                   (Log/Dashboard)
          |                                                   |
    (On-call Engineer)                                  (Non-Oncall Time)
          |
  [ Incident Response ] ----> [ Blameless Post-mortem ] ----> [ Automation ]
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 전통적 장애 대기 (Ops) | SRE 방식의 온콜 (On-call) |
| :--- | :--- | :--- |
| **목표** | 단순히 시스템을 다시 띄우는 것 | 장애 원인 파악 및 재발 방지 자동화 |
| **경보 기준** | CPU 80% 등 단순 임계치 | SLO 위반 가능성 등 비즈니스 관점 |
| **팀 구성** | 운영팀 전담 | Dev와 Ops가 공유하거나 SRE 팀 내 순환 |
| **사후 관리** | 장애 보고서 (징계 성격) | 비난 없는 포스트모템 (학습 성격) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **경보 피로(Alert Fatigue) 방어**: 자가 치유가 가능한 경보는 온콜에게 알리지 않는다. 사람이 직접 개입해야 하는 긴급 상황만 '페이저(Pager)'를 울리게 설정한다.
- **교대 근무 최적화**: 한 사람이 연속으로 너무 오래 대기하지 않도록 2차 대기자(Secondary)를 지정하고, 지역적으로 분산된 팀(Follow-the-sun 모델)을 활용해 야간 근무를 최소화한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- 온콜은 단순한 고통이 아니라 시스템의 약점을 파악하는 가장 생생한 기회다. 성공적인 온콜 관리는 엔지니어의 심리적 안전감을 높이고, 장애 복구 시간(MTTR)을 단축하며, 궁극적으로 자동화된 복구 시스템으로 나아가는 징검다리 역할을 한다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: SRE (Site Reliability Engineering)
- **자식 개념**: 경보(Alerting), 장애 대응(Incident Response)
- **연관 개념**: MTTR, 경보 피로(Alert Fatigue), 포스트모템(Post-mortem)

### 👶 어린이를 위한 3줄 비유 설명
- 온콜은 밤이나 주말에도 소방서에서 대기하는 소방관 아저씨와 비슷해요.
- 불(장애)이 나면 즉시 달려가서 끄지만, 아주 작은 연기에는 사이렌을 울리지 않게 조절해야 소방관 아저씨가 힘들지 않아요.
- 불을 끄고 나면 "왜 불이 났을까?"를 연구해서 다음에는 불이 안 나게 도와주는 역할도 한답니다.
