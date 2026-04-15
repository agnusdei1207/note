+++
title = "062. ITIL (IT Infrastructure Library)"
weight = 62
date = "2026-03-04"
[extra]
categories = "studynote-it-management"
+++

## 핵심 인사이트 (3줄 요약)
- **ITSM의 사실상 표준:** IT 서비스 관리를 위한 전 세계적인 '베스트 프랙티스' 모음집으로, 수년간 검증된 운영 노하우를 체계화한 도서관이다.
- **수명주기에서 가치 시스템으로:** ITIL V3의 서비스 수명주기 모델에서 ITIL 4의 '서비스 가치 시스템(SVS)'으로 진화하며 디지털 전환 대응력을 높였다.
- **유연한 맞춤화:** 특정 기술이나 특정 기업에 종속되지 않으며, 조직의 규모와 환경에 따라 프로세스를 선택적으로 수용(Adopt)하고 적용(Adapt)할 수 있다.

### Ⅰ. 개요 (Context & Background)
- **정의:** ITIL은 영국 정부(OGC)가 IT 서비스 관리의 효율성과 효과성을 높이기 위해 전 세계의 모범 사례(Best Practices)를 수집하여 정리한 지침서이다.
- **변천사:** 1980년대 하부 구조 관리 위주(V1)에서 시작하여, 프로세스 중심(V2), 서비스 수명주기(V3), 그리고 애자일과 데브옵스를 포용한 가치 공통 창출(V4)로 발전해왔다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **ITIL 4 서비스 가치 시스템 (Service Value System, SVS)**
```text
+-------------------------------------------------------------+
|               ITIL 4 Service Value System (SVS)             |
+-------------------------------------------------------------+
|        [Guiding Principles] -> [Governance] -> [SVC]        |
|-------------------------------------------------------------|
| [Opportunity / Demand] ---> [Value Co-creation] ---> [Value]|
|-------------------------------------------------------------|
|           [Practices] -> [Continual Improvement]            |
+-------------------------------------------------------------+
SVC (Service Value Chain): Plan, Improve, Engage, Design & Transition, Obtain/Build, Deliver & Support
```
- **핵심 원리 (Guiding Principles):**
  1. **Focus on Value:** 모든 활동은 고객 가치 창출과 연결되어야 함.
  2. **Start Where You Are:** 처음부터 다시 하지 말고 기존 자원 활용.
  3. **Progress Iteratively:** 작게 시작하고 피드백을 통해 점진적 개선.
  4. **Collaborate & Promote Visibility:** 투명한 정보 공유 및 부서 간 장벽 제거.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 버전 | ITIL V3 (2007/2011) | ITIL 4 (2019~) |
| :--- | :--- | :--- |
| **핵심 모델** | 서비스 수명주기 (Lifecycle) | 서비스 가치 시스템 (SVS) |
| **구성 단계** | 5개 단계 (Strategy, Design, Transition, Operation, CSI) | 서비스 가치 사슬 (SVC) 및 34개 프랙티스 |
| **중점 사항** | 프로세스 통제 및 정형화 | 애자일, 데브옵스, 린(Lean)과의 통합 |
| **철학** | "What to do" 중심 | "How to think & collaborate" 중심 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **감리 주안점:** ITIL 기반 프로세스가 실제 업무와 괴리되어 '문서 중심'으로 흐르고 있지 않은지, 실질적인 서비스 개선(CSI) 활동이 이루어지는지 확인해야 한다.
- **기술사적 판단:** ITIL 4의 도입은 단순히 과거 프로세스의 계승이 아니다. 복잡계(Complexity)로 진화하는 현대 IT 환경에서 '공동 가치 창출(Co-creation)'이라는 철학을 이해하고, 협업과 투명성을 높이는 데 주력해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과:** 글로벌 표준과의 일치성 확보, IT 운영 비용의 가시성 증대, 서비스 품질의 안정적 유지.
- **결론:** ITIL은 더 이상 경직된 가이드라인이 아니며, 데브옵스의 민첩성과 ITIL의 거버넌스를 결합한 '모던 ITSM'의 핵심 프레임워크로 지속 진화할 것이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** ITSM, IT 거버넌스
- **하위 개념:** 서비스 가치 사슬(SVC), 7대 원칙, 프랙티스(Practices)
- **연관 개념:** ISO/IEC 20000, DevOps, Lean, Agile

### 👶 어린이를 위한 3줄 비유 설명
- 전 세계에서 가장 장사를 잘하는 가게들의 비법을 모아둔 '요리 백과사전'과 같아요.
- 손님이 주문할 때부터 음식을 다 먹고 나갈 때까지 어떻게 하면 기분 좋게 해줄 수 있는지 적혀 있답니다.
- 이 사전을 보고 우리 가게에 맞는 비법을 골라 쓰면 우리 가게도 맛집이 될 수 있어요!
