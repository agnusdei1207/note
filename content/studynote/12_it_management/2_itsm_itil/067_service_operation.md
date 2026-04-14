+++
weight = 67
title = "서비스 운영 (Service Operation)"
date = "2024-03-20"
[extra]
categories = "studynote-it-management"
+++

## 핵심 인사이트 (3줄 요약)
1. 서비스 운영은 ITIL 프레임워크에서 비즈니스 가치가 실제로 실현되는 유일한 단계로, 약속된 서비스 수준(SLA)을 유지하는 활동이다.
2. 인시던트 관리, 문제 관리, 이벤트 관리 등의 프로세스를 통해 서비스 중단을 최소화하고 업무 연속성을 확보하는 것이 핵심이다.
3. 최근에는 AI옵스(AIOps)를 활용한 선제적 장애 탐지와 자동 복구 체계를 결합하여 '무중단 운영'을 지향하는 추세다.

### Ⅰ. 개요 (Context & Background)
ITIL V3의 서비스 수명주기 중 '서비스 운영(Service Operation)'은 구축된 IT 시스템이 실제 사용자에게 전달되는 시점의 모든 활동을 포괄한다. 설계와 전환이 아무리 훌륭해도 운영이 불안정하면 비즈니스 가치는 훼손된다. 따라서 서비스 운영의 목표는 효율성과 안정성 사이의 균형을 유지하며, 발생한 장애를 신속히 복구하고 재발을 방지하는 데 있다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
서비스 운영은 5가지 핵심 프로세스와 4가지 기능 조직으로 구성되어 유기적으로 동작한다.

```text
[Service Operation Process & Function]
+-----------------------------------------------------------+
| Functions (People/Org)                                    |
| [Service Desk] [Tech Mgmt] [App Mgmt] [IT Ops Mgmt]       |
+--------------------------+--------------------------------+
                           |
+--------------------------V--------------------------------+
| Key Processes (Workflows)                                 |
| 1. Incident Mgmt: Quick Restore (SLA focus)               |
| 2. Problem Mgmt: Root Cause Analysis (KEDB)               |
| 3. Event Mgmt: Monitoring & Alerting                      |
| 4. Request Fulfillment: Standard Requests                 |
| 5. Access Mgmt: Rights & Permissions                      |
+-----------------------------------------------------------+
  * Goal: Stability, Efficiency, Value Realization
```

1. **인시던트 관리 (Incident Mgmt)**: 서비스 중단 시 원인 파악보다 '빠른 복구(Workaround)'에 집중하여 비즈니스 영향을 최소화한다.
2. **문제 관리 (Problem Mgmt)**: 반복되는 인시던트의 '근본 원인(Root Cause)'을 분석하여 영구적으로 제거하며, KEDB(Known Error DB)를 구축한다.
3. **이벤트 관리 (Event Mgmt)**: 모니터링 도구를 통해 상태 변화를 감지하고, 유의미한 이벤트를 식별하여 대응을 트리거한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 인시던트 관리 (Incident) | 문제 관리 (Problem) |
| :--- | :--- | :--- |
| **목적** | 빠른 서비스 복구 (SLA 준수) | 근본 원인 제거 및 재발 방지 |
| **시간 관점** | 단기적, 긴급함 | 중장기적, 분석적 |
| **주요 활동** | 우회 조치(Workaround) 적용 | RCA(Root Cause Analysis) 수행 |
| **성공 지표** | MTTR (평균 복구 시간) 단축 | 인시던트 발생 건수 감소 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **운영자의 판단**: 인시던트 발생 시 원인 분석에 매몰되어 복구 시간을 놓치는 '분석의 함정'을 경계해야 한다. 일단 서비스를 살린 후(Reboot, Switch-over 등), 문제 관리 프로세스에서 깊이 있게 분석하는 '역할 분담'이 체계화되어야 한다.
- **전략적 제언**: 클라우드 MSA 환경에서는 장애 전파가 빠르므로, 서비스 메시(Istio)와 연계된 서킷 브레이커를 서비스 운영의 자동화된 통제 수단으로 활용해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
서비스 운영은 단순한 유지보수를 넘어 비즈니스 가치 창출의 전초기지다. 향후 ITIL 4의 SVS와 결합하여 고도화된 가치 흐름(Value Stream)을 형성할 것이며, 사람이 개입하지 않는 '셀프 힐링(Self-healing)' 아키텍처가 운영의 표준이 될 것이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: ITSM, ITIL
- **하위 개념**: 인시던트, 문제, KEDB, 서비스 데스크
- **연관 개념**: SLA, OLA, BCP, AIOps, DevOps

### 👶 어린이를 위한 3줄 비유 설명
1. 서비스 운영은 장난감 가게를 매일 아침 열고 손님을 맞이하는 것과 같아요.
2. 장난감이 고장 나면 일단 새 걸로 바꿔주고(인시던트), 나중에 왜 고장 났는지 공장에 물어보는(문제) 일을 해요.
3. 손님들이 언제든 즐겁게 장난감을 가지고 놀 수 있도록 가게를 깨끗하고 안전하게 지키는 역할이랍니다.
