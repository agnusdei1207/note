+++
weight = 63
title = "ITIL V3 서비스 수명주기 (Service Lifecycle)"
date = "2024-03-20"
[extra]
categories = "studynote-it-management"
+++

## 핵심 인사이트 (3줄 요약)
- **ITIL V3**는 IT 서비스를 전략 수립부터 설계, 이행, 운영, 개선까지 이어지는 5단계의 **수명주기(Lifecycle)** 모델로 정의함.
- 각 단계는 긴밀하게 연결되어 있으며, 지속적 서비스 개선(CSI)을 통해 순환 구조를 이루어 비즈니스 가치를 극대화함.
- 개별 기술 중심이 아닌 **'서비스(Service)'** 중심의 프로세스 관리를 통해 IT와 비즈니스의 전략적 일치를 추구함.

### Ⅰ. 개요 (Context & Background)
- IT Infrastructure Library (ITIL) V3는 기존의 단편적인 프로세스 나열에서 벗어나, 서비스의 탄생부터 소멸까지를 관리하는 통합 프레임워크를 제안함.
- 전 세계적으로 가장 널리 쓰이는 IT 서비스 관리(ITSM)의 사실상 표준(De facto Standard)으로 자리 잡음.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ ITIL V3 Service Lifecycle Wheel ]

             /------------------------------\
             | Continual Service Improvement |  <--- CSI (항상 순환)
             |  /------------------------\   |
             |  |   Service Transition    |   |  <--- 운영 이관
             |  |  /------------------\  |   |
             |  |  | Service Design    |  |   |  <--- 상세 설계
             |  |  |  /--------------\ |  |   |
             |  |  |  |   Service    | |  |   |  <--- 핵심 전략
             |  |  |  |   Strategy   | |  |   |
             |  |  |  \--------------/ |  |   |
             |  |  \------------------/  |   |
             |  |   Service Operation     |   |  <--- 실 서비스 제공
             |  \------------------------/   |
             \------------------------------/

* 중심(Core): Service Strategy -> Design -> Transition -> Operation (CSI Surrounds)
```
- **Service Strategy**: 비즈니스 목표에 부합하는 서비스 포트폴리오 정의 및 재무, 수요 관리.
- **Service Design**: 가용성, 용량, 보안, 연속성, 서비스 수준(SLA) 등 신규/변경된 서비스의 상세 명세 설계.
- **Service Transition**: 설계된 서비스를 실제 운영 환경으로 안전하게 릴리스(변경, 구성, 배포 관리).
- **Service Operation**: 일상적인 인시던트 처리, 문제 해결, 요청 충족을 통해 고객에게 합의된 가치 제공.
- **Continual Service Improvement (CSI)**: 서비스 성과를 측정하고 비즈니스 변화에 맞춰 지속적으로 개선함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 수명주기 단계 | 주요 프로세스 (Key Processes) | 핵심 목적 (Objective) |
| :--- | :--- | :--- |
| **Strategy** | 포트폴리오 관리, 수요 관리, 재무 관리 | 비즈니스 가치 창출 방향 설정 |
| **Design** | SLM (SLA), 용량, 가용성, 보안 관리 | 서비스 요구사항의 상세화/표준화 |
| **Transition** | 변경 관리, 자산/구성 관리, 릴리스 관리 | 신속하고 안전한 운영 환경 이관 |
| **Operation** | 인시던트, 문제, 이벤트 관리 | 서비스 중단 최소화 및 운영 효율 |
| **CSI** | 서비스 성과 측정, 7단계 개선 모델 | 품질 향상 및 비즈니스 정렬 유지 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **판단 지표**: 서비스 운영이 비체계적이고, 잦은 장애와 복구 지연이 발생하며, IT 조직과 비즈니스 부서 간의 소통 부재 시 도입함.
- **적용 전략**: 모든 프로세스를 한꺼번에 도입하기보다는 비즈니스 시급성이 높은 '인시던트' 및 '변경 관리'부터 단계적으로 구축(Tailoring)해야 함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- IT 운영의 **가시성(Visibility)**을 확보하고, 서비스 품질의 상향 표준화를 통해 고객 만족도를 제고함.
- 최신 버전인 ITIL 4는 이 모델을 계승하되, 애자일(Agile), 데브옵스(DevOps) 환경에 맞춘 '서비스 가치 시스템(SVS)'으로 진화하며 거버넌스를 더욱 강화함.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: IT 서비스 관리 (ITSM), ISO/IEC 20000
- **동급 프레임워크**: COBIT, CMMI (SVC)
- **하위 프로세스**: 인시던트 관리, 문제 관리, 변경 관리 (ITIL 26개 프로세스)

### 👶 어린이를 위한 3줄 비유 설명
- 맛있는 '장난감 가게'를 운영하는 5가지 순서와 같아요.
- 어떤 장난감을 팔지 계획하고(Strategy), 멋지게 만들고(Design), 가게에 진열하고(Transition), 손님에게 팔고(Operation), 더 좋은 가게로 만드는 것(CSI)이에요.
- 이 순서를 잘 지키면 손님도 행복하고 주인님도 부자가 되는 멋진 방법이랍니다.
