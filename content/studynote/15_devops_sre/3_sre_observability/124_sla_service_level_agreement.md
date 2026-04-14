+++
weight = 124
title = "서비스 수준 합의 (SLA, Service Level Agreement)"
date = "2025-05-22"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
- **SLA (Service Level Agreement)**: 서비스 제공자와 이용자 간의 성능 및 품질 수준에 대한 공식적인 법적/비즈니스적 계약으로, 미달성 시 보상 방안을 포함함.
- **비즈니스 약속**: 기술적인 목표인 SLO와 달리, SLA는 가용성(Uptime) 및 응답 속도 등의 핵심 지표를 기준으로 비즈니스 신뢰를 보증하는 장치임.
- **기술사적 관점**: 엔지니어링 조직은 SLA 위반 시의 재무적 리스크를 방어하기 위해 내부 SLO를 SLA보다 훨씬 엄격하게 설정(Buffering)해야 함.

### Ⅰ. 개요 (Context & Background)
SLA는 IT 서비스를 하나의 상품으로 거래할 때 품질을 보증하는 핵심 문서입니다. 특히 클라우드 컴퓨팅(SaaS, PaaS, IaaS) 환경에서 SLA는 고객사와의 계약 관계에서 법적 책임의 근거가 되며, 서비스의 공신력을 평가하는 척도가 됩니다. SRE 관점에서 SLA는 시스템이 무너졌을 때 비즈니스에 미치는 타격의 한계선입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
SLA를 포함하는 전체 품질 관리 체계와 가용성 보상 체계의 아키텍처입니다.

```text
[ Business Trust & SLA Compensation Structure ]

      Contract Layer (SLA) <--- External Commitment (Customer)
               |
      Management Layer (SLO) <--- Internal Target (Dev/Ops)
               |
      Measurement Layer (SLI) <--- Real-time Metric (Telemetry)

[ Availability Calculation & Service Credit ]

   Uptime (%) = (Scheduled - Downtime) / Scheduled * 100

   SLA Tier (Example):
   - 99.9%+: No Credit (Ideal)
   - 99.0% - 99.9%: 10% Service Credit Refund
   - Under 99.0%: 30% Service Credit Refund
```

**핵심 원리 및 구성 요소:**
1. **가동률 (Uptime)**: 특정 기간 동안 서비스가 정상적으로 작동한 시간 비율. (연간 99.9%는 총 장애 시간 8.76시간 이하)
2. **보상 규정 (Service Credit)**: 약속된 수준을 지키지 못했을 때 이용료 할인이나 환불을 명시.
3. **제외 항목 (Exclusions)**: 정기 점검, 천재지변, 외부 공격(DDoS), 고객사의 귀책 사유 등은 장애 시간에서 제외.
4. **측정 기준 및 빈도**: 한 달 또는 분기 단위로 평가하며, 측정 도구(Tool)와 보고 방식(Report)을 합의.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | 내부 관리용 (Internal SLO) | 대외 계약용 (External SLA) |
| :--- | :--- | :--- |
| **목적** | 엔지니어링 팀의 채찍과 당근 | 고객 신뢰 확보 및 법적 방어 |
| **목표 수치** | 공격적 (Aggressive, 예: 99.95%) | 보수적 (Conservative, 예: 99.9%) |
| **위반 시 여파** | 배포 동결 (Error Budget 소진) | 환불, 위약금 지급, 평판 하락 |
| **지표의 복잡성** | 복잡하고 상세함 (수천 개 지표) | 단순하고 명확함 (가용성 위주) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **적용 전략 (Implementation Strategy)**:
  * **보호막(Buffer) 설계**: 내부 SLO를 SLA보다 한 단계 높게 설정하여(예: SLA 99% → SLO 99.9%), SLO를 위반하더라도 SLA를 지킬 수 있는 시간적 여유를 확보해야 함.
  * **책임 공유 모델 (Shared Responsibility)**: 인프라 제공자(AWS 등)가 보증하는 SLA와 내가 만든 앱의 SLA를 명확히 구분하여 엔드투엔드 가용성을 산출.
* **기술사적 판단 (Architectural Judgment)**:
  * SLA는 단순한 '장애 방지'가 아닌 '비즈니스 협상 도구'임. 지나치게 높은 SLA 보증은 인프라 비용(Redundancy)을 기하급수적으로 증가시키므로, 고객의 비즈니스 가치에 맞는 경제적 SLA(Economic SLA)를 제안하는 것이 전문가의 역량임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
SLA는 고객과의 신뢰 관계를 유지하는 최후의 보루입니다. 향후에는 스마트 계약(Smart Contract) 기술과 연동되어 장애 발생 시 수동 청구 없이 자동으로 보상금이 지급되는 투명한 SLA 체계가 클라우드 시장의 표준이 될 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **비즈니스 통제**: Contract Law, Service Credit, KPI
* **SRE 체계**: SLI/SLO/SLA Integration
* **가용성**: High Availability (HA), Disaster Recovery (DR), 9s

### 👶 어린이를 위한 3줄 비유 설명
1. "내일 아침 9시까지 숙제를 꼭 다 할게!"라고 엄마랑 약속하고, 못 하면 간식을 안 먹겠다고 서명까지 한 종이가 바로 SLA예요.
2. 사실 속으로는 '8시 반까지 끝내야지(SLO)'라고 마음먹어서 혹시 늦어도 9시는 안 넘기려고 노력하는 거죠.
3. 약속을 지키면 엄마가 칭찬해주고, 못 지키면 약속대로 벌칙(보상)을 받는 시스템이랍니다.
