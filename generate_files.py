import os

files = {
    "content/studynote/11_design_supervision/9_design_principles/101_solid_object_oriented_design_principles.md": """+++
weight = 101
title = "객체 지향 설계 원칙 (SOLID)"
date = "2026-03-04"
[extra]
categories = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)
1. **SOLID**는 로버트 C. 마틴이 제안한 객체 지향 프로그래밍 및 설계의 5가지 기본 원칙으로, 유지보수성과 확장성을 극대화합니다.
2. 각 원칙(SRP, OCP, LSP, ISP, DIP)은 소프트웨어 모듈의 응집도를 높이고 결합도를 낮추는 아키텍처적 기반을 제공합니다.
3. 변화에 강한 유연한 시스템 구조를 만들기 위해 애자일(Agile) 개발 및 리팩토링의 핵심 지침으로 활용됩니다.

### Ⅰ. 개요 (Context & Background)
객체 지향 설계 원칙(SOLID)은 소프트웨어 설계에서 흔히 발생하는 코드 냄새(Code Smell)와 스파게티 코드를 방지하기 위해 로버트 C. 마틴(Uncle Bob)이 정립한 5대 원칙입니다. 현대 소프트웨어 공학에서 디자인 패턴과 클린 아키텍처를 구현하기 위한 필수적인 뼈대로 작용하며, 시스템의 생명주기를 연장하고 유지보수 비용(TCO)을 최소화하는 데 기여합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
SOLID 원칙은 결합도(Coupling) 최소화와 응집도(Cohesion) 최대화를 목표로 합니다.

```text
+-------------------------------------------------------------+
|                SOLID Design Principles                      |
|                                                             |
|  [S] SRP : Single Responsibility (단일 책임)                |
|      -> Class should have one reason to change              |
|                                                             |
|  [O] OCP : Open-Closed (개방-폐쇄)                          |
|      -> Open for extension, Closed for modification         |
|                                                             |
|  [L] LSP : Liskov Substitution (리스코프 치환)              |
|      -> Subtypes must be substitutable for base types       |
|                                                             |
|  [I] ISP : Interface Segregation (인터페이스 분리)          |
|      -> Clients should not be forced to depend on unused    |
|                                                             |
|  [D] DIP : Dependency Inversion (의존성 역전)               |
|      -> Depend on abstractions, not concretions             |
+-------------------------------------------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 원칙 | 주요 목적 | 안티 패턴 (위반 시) | 해결 패턴 |
|---|---|---|---|
| **SRP** | 클래스의 역할 단순화 | 갓 클래스 (God Class) | Facade, Proxy |
| **OCP** | 기존 코드 변경 없이 확장 | 하드 코딩, 조건문 남발 | Strategy, Decorator |
| **LSP** | 상속의 신뢰성 보장 | 예외 던지기, 타입 체크 | Template Method |
| **ISP** | 인터페이스의 비대화 방지 | 뚱뚱한 인터페이스 | Adapter |
| **DIP** | 모듈 간의 결합도 분리 | 스파게티 코드, 강결합 | Dependency Injection |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **초기 설계 vs 과도한 엔지니어링**: 모든 원칙을 초기에 완벽하게 적용하려 하면 YAGNI(You Aren't Gonna Need It) 원칙에 위배될 수 있습니다. 리팩토링 단계에서 점진적으로 적용하는 전략이 필요합니다.
* **아키텍처 영향**: 마이크로서비스 아키텍처(MSA)에서 각 서비스의 바운디드 컨텍스트(Bounded Context)를 정의할 때 SRP와 DIP가 핵심 분리 기준이 됩니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
SOLID 원칙을 준수하면 코드의 가독성이 향상되고, 테스트 주도 개발(TDD) 환경에서 단위 테스트 작성이 매우 용이해집니다. 궁극적으로 기술 부채(Technical Debt)를 예방하고 시스템의 지속 가능한 진화를 보장하는 객체 지향 철학의 완성이라 할 수 있습니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **상위 개념**: 소프트웨어 아키텍처, 객체 지향 프로그래밍(OOP)
* **하위 개념**: SRP, OCP, LSP, ISP, DIP
* **연관 개념**: GoF 디자인 패턴, 클린 아키텍처, TDD, 응집도와 결합도

### 👶 어린이를 위한 3줄 비유 설명
1. 레고 블록을 조립할 때, 각 블록은 하나의 역할만 해야 쉽게 바꿀 수 있어요.
2. 새로운 로봇 팔을 끼울 때 기존 몸통을 부수지 않아도 돼야 좋은 장난감이에요.
3. 작은 블록은 큰 블록이 있던 자리에 쏙 들어가서 완벽하게 호환되어야 해요!
""",

    "content/studynote/11_design_supervision/9_design_principles/102_srp_single_responsibility_principle.md": """+++
weight = 102
title = "SRP (Single Responsibility Principle, 단일 책임 원칙)"
date = "2026-03-04"
[extra]
categories = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)
1. **SRP(단일 책임 원칙)**은 클래스나 모듈이 단 하나의 변경 이유(책임)만을 가져야 한다는 객체 지향 설계의 첫 번째 원칙입니다.
2. 응집도를 극대화하여 사이드 이펙트(Side Effect)를 방지하고 유지보수성을 크게 향상시킵니다.
3. 데이터 접근, 비즈니스 로직, UI 출력이 한 클래스에 섞이는 '갓 클래스(God Class)' 안티 패턴을 타파하는 근본적인 해결책입니다.

### Ⅰ. 개요 (Context & Background)
SRP는 소프트웨어 개발에서 가장 지키기 어렵지만 가장 중요한 원칙 중 하나입니다. 기능 추가나 요구사항 변경 시 수정해야 할 대상이 여러 곳에 분산되거나 한 곳에 집중되어 발생하는 결함의 파급(Ripple Effect)을 막기 위해, 책임을 세밀하게 분리하는 것이 핵심입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
클래스는 한 가지의 책임만 지며, 그 책임을 완전히 캡슐화해야 합니다.

```text
+-------------------------------------------------------------+
|                SRP Architecture Principle                   |
|                                                             |
|  [Bad Design - God Class]                                   |
|  +--------------------+                                     |
|  |    UserAccount     | -> Handles Auth, DB, and UI         |
|  +--------------------+                                     |
|                                                             |
|  [Good Design - SRP]                                        |
|  +----------------+   +----------------+   +-------------+  |
|  | Authenticator  |   | UserRepository |   | UserView    |  |
|  +----------------+   +----------------+   +-------------+  |
|   (Auth Logic)          (DB Operations)     (UI Display)    |
+-------------------------------------------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 특성 | 단일 책임 원칙 준수 (SRP) | 단일 책임 원칙 위반 (God Class) |
|---|---|---|
| **응집도 (Cohesion)** | 높음 (High) | 낮음 (Low) |
| **결합도 (Coupling)** | 낮음 (Low) | 높음 (High) |
| **테스트 용이성** | 모킹(Mocking) 및 단위 테스트가 매우 쉬움 | 의존성이 복잡하여 단위 테스트 어려움 |
| **재사용성** | 모듈화가 잘 되어 재사용성 극대화 | 불필요한 기능까지 묶여 재사용 불가 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **책임의 범위 설정**: '책임'이라는 단어는 비즈니스 도메인에 따라 유연하게 해석되어야 합니다. 과도한 분리는 클래스의 파편화(Shotgun Surgery)를 유발할 수 있으므로, 적절한 추상화 수준을 유지해야 합니다.
* **아키텍처 적용**: 마이크로서비스(MSA) 설계 시 단일 책임 원칙은 서비스의 바운디드 컨텍스트(Bounded Context)를 쪼개는 가장 근본적인 척도로 작용합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
SRP를 충실히 따르면 시스템의 복잡성이 분산되어 코드의 가독성이 높아지고, 여러 명의 개발자가 동시에 협업하더라도 머지(Merge) 충돌을 최소화할 수 있습니다. 이는 클린 코드(Clean Code)를 향한 첫걸음입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **상위 개념**: SOLID 원칙
* **하위 개념**: 응집도(Cohesion), 결합도(Coupling)
* **연관 개념**: 갓 클래스(God Class), 마이크로서비스(MSA), 파사드 패턴(Facade)

### 👶 어린이를 위한 3줄 비유 설명
1. 요리사는 요리만, 웨이터는 서빙만, 계산원은 계산만 해야 식당이 잘 돌아가요.
2. 한 사람이 모든 일을 다 하려고 하면 실수하기 쉽고 엄청 피곤해져요.
3. 코드도 각자 자기 역할만 딱 하나씩 맡아서 하도록 나눠주는 것이 SRP랍니다!
""",

    "content/studynote/11_design_supervision/9_design_principles/103_ocp_open_closed_principle.md": """+++
weight = 103
title = "OCP (Open-Closed Principle, 개방-폐쇄 원칙)"
date = "2026-03-04"
[extra]
categories = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)
1. **OCP(개방-폐쇄 원칙)**은 소프트웨어 개체는 확장에 대해서는 열려 있어야 하고, 수정에 대해서는 닫혀 있어야 한다는 원칙입니다.
2. 다형성(Polymorphism)과 인터페이스 추상화를 통해 기존 코드를 건드리지 않고 새로운 기능을 추가할 수 있는 유연성을 제공합니다.
3. 조건문(if-else, switch)의 남발을 방지하고 디자인 패턴(전략 패턴 등)을 적용하는 가장 핵심적인 배경 원리입니다.

### Ⅰ. 개요 (Context & Background)
버그 수정이나 신규 기능 추가 시 기존 코드를 직접 수정하게 되면 파급 효과(Ripple Effect)로 인해 예상치 못한 장애가 발생할 수 있습니다. OCP는 기존의 테스트된 핵심 코드는 그대로 유지(Closed)하면서 기능은 쉽게 추가(Open)할 수 있는 구조적 안전망을 요구합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
인터페이스나 추상 클래스를 상속받아 새로운 구현체를 추가하는 방식이 OCP의 근간입니다.

```text
+-------------------------------------------------------------+
|                OCP Architecture Principle                   |
|                                                             |
|  [Before OCP - Hardcoded]                                   |
|  PaymentProcessor -> if (type==Credit) payCredit()          |
|                   -> else if (type==Paypal) payPaypal()     |
|                                                             |
|  [After OCP - Polymorphism]                                 |
|  PaymentProcessor -> uses -> [PaymentStrategy Interface]    |
|                                     ^                       |
|                                     |-- CreditPayment       |
|                                     |-- PaypalPayment       |
|                                     |-- CryptoPayment (New) |
+-------------------------------------------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 항목 | OCP 위배 구조 (Procedural) | OCP 준수 구조 (Object-Oriented) |
|---|---|---|
| **기능 확장 방법** | 기존 함수의 내부 로직(if/switch) 수정 | 인터페이스를 상속받은 새 클래스 추가 |
| **장애 위험성** | 기존 기능에 버그가 발생할 확률 매우 높음 | 기존 코드는 안전 (변경되지 않음) |
| **테스트 범위** | 수정된 함수 전체 재테스트 (Regression) | 새로 추가된 클래스만 테스트 |
| **관련 패턴** | 없음 (절차지향적 하드코딩) | Strategy, Decorator, Factory Method |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **인터페이스 설계의 중요성**: OCP를 지키기 위해서는 도메인에서 변경될 가능성이 높은 부분을 예측하여 적절한 인터페이스(추상화 계층)를 미리 배치해야 합니다.
* **스프링 프레임워크와의 시너지**: DI(의존성 주입) 프레임워크를 활용하면 런타임 시점에 클라이언트 코드 변경 없이 인터페이스의 구현체를 자유롭게 교체(OCP 달성)할 수 있습니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
OCP는 시스템의 유지보수 비용을 급격히 낮추며, 오픈소스나 프레임워크를 개발할 때 코어 엔진을 보호하면서 플러그인(Plugin) 형태로 사용자 확장을 지원하는 핵심 아키텍처 원칙입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **상위 개념**: SOLID 원칙
* **하위 개념**: 추상화(Abstraction), 다형성(Polymorphism)
* **연관 개념**: 전략 패턴(Strategy Pattern), 의존성 주입(DI), 템플릿 메서드 패턴

### 👶 어린이를 위한 3줄 비유 설명
1. 게임기에 새로운 게임을 하고 싶을 때 게임기 본체를 뜯어서 고치지 않죠?
2. 그냥 새로운 게임 팩(카트리지)을 꽂기만 하면 새로운 게임이 실행되잖아요.
3. 기계는 가만히 두고(수정에 닫힘) 팩만 갈아끼우는 것(확장에 열림)이 OCP예요!
""",

    "content/studynote/12_it_management/4_sdlc_testing/134_cmmi_level_1_initial.md": """+++
weight = 134
title = "CMMI 레벨 1 (Initial, 초기)"
date = "2026-03-04"
[extra]
categories = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)
1. **CMMI 레벨 1(Initial)**은 조직 내에 공식적으로 정의되거나 문서화된 표준 개발 프로세스가 존재하지 않는 가장 원시적인 상태입니다.
2. 프로젝트의 성공이 프로세스의 우수성이 아닌, 뛰어난 소수 개발자(영웅)의 개인 역량에 전적으로 의존합니다.
3. 일정이 지연되거나 예산을 초과하는 리스크가 매우 크며, 성공 경험을 다른 프로젝트로 반복하거나 재현하기 불가능합니다.

### Ⅰ. 개요 (Context & Background)
CMMI(Capability Maturity Model Integration)는 조직의 소프트웨어 개발 및 시스템 구축 능력의 성숙도를 5단계로 평가하는 국제 표준 모델입니다. 레벨 1은 평가의 가장 밑바닥 단계로, 대부분의 초기 스타트업이나 프로세스가 정립되지 않은 개발 조직이 여기에 속합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
레벨 1 조직의 프로세스는 'Ad-hoc(임시 방편적)'이고 '혼돈(Chaotic)' 상태입니다.

```text
+-------------------------------------------------------------+
|                CMMI Level 1 Characteristics                 |
|                                                             |
|  [Input] -> (Black Box / Ad-hoc Process) -> [Output/Result] |
|                                                             |
|  * No standardized procedures                               |
|  * Over-reliance on "Heroes"                                |
|  * Reactive management (Fire-fighting)                      |
|  * Unpredictable cost, schedule, and quality                |
+-------------------------------------------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 평가 요소 | CMMI 레벨 1 (초기) | CMMI 레벨 2 (관리됨) |
|---|---|---|
| **프로세스 유무** | 없음 (개인의 기억과 습관에 의존) | 프로젝트 단위의 기초적 프로세스 존재 |
| **성공의 재현성** | 불가능 (영웅이 퇴사하면 프로젝트 실패) | 유사한 프로젝트에서 반복 성공 가능 |
| **위기 대응 방식** | 사후약방문 (소방수 역할, Fire-fighting) | 요구사항 및 형상 관리 기반 통제 |
| **조직의 상태** | 혼돈(Chaotic), 일관성 없음 | 기율(Disciplined), 프로젝트 관리 통제 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **레벨 2로의 도약 전략**: 레벨 1에서 벗어나기 위해서는 기본 프로젝트 관리 프로세스(요구사항 관리, 프로젝트 계획, 형상 관리, 품질 보증 등)를 수립해야 합니다.
* **리스크 식별**: 품질 관리자(QA)나 감리인이 조직을 심사할 때, 문서화된 산출물이 없고 코드로만 소통하려 한다면 전형적인 레벨 1의 징후로 판단합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
CMMI 레벨 1 상태를 방치하면 기술 부채가 기하급수적으로 쌓이고 조직 확장이 불가능해집니다. 최소한의 베이스라인과 형상 관리를 도입하여 개인의 역량을 조직의 자산(프로세스)으로 내재화하는 첫걸음이 시급합니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **상위 개념**: CMMI, 소프트웨어 공학, SDLC
* **하위 개념**: Ad-hoc 프로세스, 영웅주의(Heroism)
* **연관 개념**: 기술 부채, 애자일 안티 패턴, 스파게티 코드

### 👶 어린이를 위한 3줄 비유 설명
1. 설명서(레시피) 없이 감으로만 요리하는 식당이에요.
2. 주방장 기분이 좋은 날은 맛있지만, 주방장이 아파서 쉬면 음식 맛이 엉망진창이 되죠.
3. 요리법을 기록해두지 않아서 맛을 똑같이 다시 만들어낼 수 없는 상태랍니다.
""",

    "content/studynote/12_it_management/4_sdlc_testing/135_cmmi_level_2_managed.md": """+++
weight = 135
title = "CMMI 레벨 2 (Managed, 관리됨)"
date = "2026-03-04"
[extra]
categories = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)
1. **CMMI 레벨 2(Managed)**는 '프로젝트 단위'의 기본 관리 프로세스(요구사항, 일정, 비용)가 수립된 성숙도 단계입니다.
2. 이전에 성공했던 유사한 프로젝트의 경험과 규칙을 기반으로, 새로운 프로젝트에서도 성공을 '반복(Repeatable)'할 수 있습니다.
3. 개인 영웅주의에서 벗어나 관리 통제(Discipline)를 확보한 최초의 안정화 단계입니다.

### Ⅰ. 개요 (Context & Background)
CMMI 레벨 1의 혼돈 상태를 극복하고, 조직이 최소한 프로젝트를 계획하고 실행 상황을 추적(Tracking)할 수 있게 된 상태입니다. 형상 관리와 요구사항 관리가 핵심적인 프로세스 영역(Process Area, PA)으로 자리 잡으며, 외주 계약이나 감리 시 최소 요구 기준으로 자주 등장합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
프로젝트 레벨의 기율(Discipline)이 확립되어, 입력(Input)과 산출물(Output)의 추적이 가능합니다.

```text
+-------------------------------------------------------------+
|                CMMI Level 2 Characteristics                 |
|                                                             |
|  [Project A] -> (Requirements -> Plan -> Track) -> Success  |
|  [Project B] -> (Repeat Process from Proj A)    -> Success  |
|                                                             |
|  * Basic Project Management Established                     |
|  * Repeatable Success on similar projects                   |
|  * Configuration Management (SCM) Active                    |
+-------------------------------------------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 핵심 프로세스 영역 (PA) | 설명 | 핵심 산출물 |
|---|---|---|
| **요구사항 관리 (REQM)** | 요구사항 변경을 식별, 통제하고 베이스라인 유지 | 요구사항 추적 매트릭스(RTM) |
| **프로젝트 계획 (PP)** | WBS 작성, 일정 및 예산, 인력 할당 계획 | 프로젝트 관리 계획서 |
| **프로젝트 통제 (PMC)** | 계획 대비 실제 진행 현황을 측정(EVM 등) 및 교정 | 주간 보고서, 진척률(%) 현황 |
| **형상 관리 (CM)** | 소스코드 및 문서의 버전 통제, 무결성 유지 | 베이스라인, 형상 관리 대장 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **조직적 한계**: 레벨 2는 '프로젝트 A' 팀과 '프로젝트 B' 팀의 관리 기준이 다를 수 있습니다. 전사적으로 통일된 표준은 없으며 부서별, PM별로 각자의 템플릿을 사용하는 국지적 한계가 존재합니다.
* **감리 관점**: CMMI 레벨 2가 제대로 정착되었는지 평가하려면, 요구사항의 변경 내역이 설계서와 코드에 양방향으로 추적되고 있는지(Traceability)를 최우선으로 검증해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
CMMI 레벨 2 달성을 통해 조직은 프로젝트 일정 지연과 비용 초과 리스크를 획기적으로 낮출 수 있습니다. 이후 전사적 차원의 표준 프로세스를 수립하기 위한 레벨 3(Defined)로 진입할 수 있는 튼튼한 토대가 됩니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **상위 개념**: CMMI, 소프트웨어 공학 품질 관리
* **하위 개념**: 요구사항 관리, 형상 관리, WBS
* **연관 개념**: EVM(획득가치관리), 베이스라인(Baseline)

### 👶 어린이를 위한 3줄 비유 설명
1. 이제 요리사가 자신만의 비밀 '레시피 노트'를 공책에 적어두기 시작했어요.
2. 예전에 맛있게 만들었던 김치찌개를 다음번에도 똑같이 맛있게 만들 수 있죠! (반복 가능)
3. 하지만 아직 다른 식당 주방장과 레시피를 공유하거나 통일하지는 않은 상태랍니다.
""",

    "content/studynote/12_it_management/4_sdlc_testing/136_cmmi_level_3_defined.md": """+++
weight = 136
title = "CMMI 레벨 3 (Defined, 정의됨)"
date = "2026-03-04"
[extra]
categories = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)
1. **CMMI 레벨 3(Defined)**는 개별 프로젝트를 넘어 **전사(조직 전체)의 표준 프로세스**가 문서화되고 확립된 성숙도 단계입니다.
2. 각 프로젝트는 조직 표준 프로세스를 자신들의 환경에 맞게 조정(Tailoring)하여 사용합니다.
3. 체계적인 검토(Peer Review, Inspection)와 위험 관리(Risk Management)가 조직 문화로 내재화되어 소프트웨어 품질이 균일해집니다.

### Ⅰ. 개요 (Context & Background)
CMMI 레벨 2가 'PM(프로젝트 매니저)의 역량에 의한 프로젝트 단위의 관리'였다면, 레벨 3은 '회사의 시스템에 의한 전사적 관리'를 의미합니다. 조직 내 표준 자산(OPD, Organizational Process Definition)이 구축되며, 공공/금융 대형 SI 사업 입찰 시 요구되는 최소 품질 자격 기준이기도 합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
조직 표준 프로세스와 테일러링(Tailoring)의 구조적 관계가 핵심입니다.

```text
+-------------------------------------------------------------+
|                CMMI Level 3 Characteristics                 |
|                                                             |
|   [Organization Standard Process (OPD)]                     |
|           |                 |                 |             |
|       Tailoring         Tailoring         Tailoring         |
|           v                 v                 v             |
|   [Project A Proc]  [Project B Proc]  [Project C Proc]      |
|                                                             |
|  * Proactive Risk Management                                |
|  * Peer Reviews & Inspections                               |
|  * Organizational Training & Process Focus                  |
+-------------------------------------------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 속성 | CMMI 레벨 2 (Managed) | CMMI 레벨 3 (Defined) |
|---|---|---|
| **프로세스의 범위** | 프로젝트/부서 단위 국지적 프로세스 | 전사(회사 전체) 표준 프로세스 |
| **프로세스의 성격** | 사후 대응적 (Reactive) | 사전 예방적 (Proactive) |
| **위험 관리** | 이슈가 터지면 해결에 급급 | 사전에 위험(Risk)을 식별하고 완화 계획 수립 |
| **테일러링(Tailoring)** | 없음 (표준이 없으므로 재단할 것도 없음) | 조직 표준을 기반으로 프로젝트 특성 맞춤 가공 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **테일러링 가이드라인**: 조직 표준을 그대로 100% 적용하면 프로젝트가 경직될 수 있습니다. 프로젝트의 규모(대/중/소)나 방법론(애자일/폭포수)에 따라 불필요한 산출물을 생략할 수 있는 합리적인 테일러링 지침이 필수입니다.
* **품질 활동의 고도화**: 레벨 3부터는 동료 검토(Peer Review)와 인스펙션(Inspection)이 의무화되어, 테스트 단계 이전(설계/코딩 단계)에 결함을 조기 발견(Shift-Left)하는 문화가 정착됩니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
CMMI 레벨 3을 달성하면 개발자의 이직이나 PM의 교체에도 불구하고 프로젝트 품질의 흔들림이 사라집니다. 축적된 전사적 지식 기반은 차후 레벨 4(정량적 관리)를 위한 통계적 베이스라인 데이터베이스(Process Asset Library)로 진화하게 됩니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **상위 개념**: CMMI, 프로세스 혁신
* **하위 개념**: 조직 표준 프로세스, 테일러링(Tailoring), 인스펙션
* **연관 개념**: 예방적 위험 관리(Risk Management), 지식 관리(KMS)

### 👶 어린이를 위한 3줄 비유 설명
1. 이제 식당 본사에서 '전국 체인점 표준 요리 매뉴얼'을 만들어서 책자로 배포했어요.
2. 서울 지점이든 부산 지점이든 똑같은 매뉴얼을 써서 언제나 같은 맛이 보장돼요.
3. 물론 매운맛을 좋아하는 동네(프로젝트)에서는 표준 레시피에서 고춧가루만 살짝 더 추가(테일러링)할 수 있답니다!
""",

    "content/studynote/13_cloud_architecture/2_container_k8s/115_terraform_infrastructure_provisioning.md": """+++
weight = 115
title = "테라폼 (Terraform) 인프라 프로비저닝"
date = "2026-03-04"
[extra]
categories = ["studynote-cloud"]
+++

## 핵심 인사이트 (3줄 요약)
1. **테라폼(Terraform)**은 하시코프(HashiCorp)가 개발한 대표적인 인프라스트럭처 애즈 코드(IaC) 도구로, HCL(선언적 언어)을 사용해 인프라를 코드로 관리합니다.
2. AWS, Azure, GCP 등 수백 개의 이기종 멀티 클라우드 프로바이더(Provider) 자원을 단일 템플릿 언어로 통합 제어할 수 있는 압도적 장점이 있습니다.
3. 인프라의 현재 상태를 저장하는 **상태 파일(tfstate)**을 기반으로 멱등성(Idempotency)을 보장하며, 변경 전 실행 계획(Plan)을 미리 보여주어 안전한 배포가 가능합니다.

### Ⅰ. 개요 (Context & Background)
과거 클라우드 엔지니어들은 웹 브라우저 UI(콘솔) 마우스 클릭이나 절차적 쉘 스크립트로 인프라를 구축했습니다. 이는 휴먼 에러를 유발하고 인프라 버전을 추적할 수 없는 한계가 있었습니다. 테라폼은 클라우드 아키텍처를 소스 코드로 형상 관리(Git 연동)하고, 코드 리뷰를 통해 배포하는 GitOps 패러다임을 열어준 핵심 기술입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
테라폼은 선언형(Declarative) 방식을 사용하여 최종 목표 상태만 지정하면 내부 엔진이 알아서 생성/수정/삭제 순서를 최적화하여 실행합니다.

```text
+-------------------------------------------------------------+
|                Terraform Workflow Architecture              |
|                                                             |
|  [HCL Code (.tf)] ---> `terraform init` (Downloads Provider)|
|         |                                                   |
|         v                                                   |
|  `terraform plan` ---> Compares HCL with [.tfstate] & Cloud |
|         |              (Shows + Create, - Destroy, ~ Update)|
|         v                                                   |
|  `terraform apply` --> Calls Cloud API (AWS/GCP) to match   |
|                        Desired State and Updates [.tfstate] |
+-------------------------------------------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | Terraform (HashiCorp) | AWS CloudFormation | Ansible |
|---|---|---|---|
| **지원 환경** | 멀티/하이브리드 클라우드 | AWS 전용 종속(Lock-in) | 멀티 서버(OS 레벨) |
| **목적** | **인프라 프로비저닝** (VPC, VM 생성) | 인프라 프로비저닝 | **구성 관리** (OS 세팅, 패키지 설치) |
| **관리 방식** | 상태 파일(State) 기반 선언형 | Stack 단위 선언형 | 절차형 + 멱등성 지향 |
| **언어** | HCL (HashiCorp Configuration) | JSON / YAML | YAML |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **상태 파일(tfstate) 관리 보안**: `.tfstate` 파일에는 DB 패스워드 등 민감한 클라우드 메타데이터가 평문으로 저장됩니다. 따라서 절대 로컬 Git에 커밋하면 안 되며, AWS S3나 Terraform Cloud와 같은 원격 백엔드에 저장하고 락(DynamoDB State Lock)을 걸어 동시성 충돌을 막아야 합니다.
* **모듈화(Module)**: 반복되는 인프라 아키텍처(예: EKS 클러스터 구축 템플릿)를 모듈로 추상화하여 사내 개발팀에 벤딩 머신처럼 제공하는 플랫폼 엔지니어링 전략이 요구됩니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
테라폼 도입은 클라우드 재해 복구(DR) 시 몇 분 만에 완벽히 동일한 인프라를 타 리전에 재생성하는 엄청난 복원력을 제공합니다. 최근 클라우드 네이티브 생태계에서는 쿠버네티스의 크로스플레인(Crossplane) 등과 융합되어 더욱 고도화된 IaC 표준으로 진화하고 있습니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **상위 개념**: 인프라 애즈 코드(IaC), 데브옵스(DevOps)
* **하위 개념**: HCL, tfstate, Provider, Module
* **연관 개념**: GitOps, Ansible, AWS CloudFormation, 멀티 클라우드

### 👶 어린이를 위한 3줄 비유 설명
1. 마인크래프트에서 집을 지을 때 블록을 하나씩 손으로 직접 쌓는 건 너무 귀찮고 힘들죠.
2. 테라폼은 "방 3개짜리 멋진 성을 지어줘"라고 설계도(코드)를 써서 주면, 마법 지팡이가 1초 만에 성을 뚝딱 만들어주는 도구예요.
3. 설계도만 잘 보관해두면 언제 어디서든 똑같은 성을 백 번이고 다시 만들 수 있답니다!
""",

    "content/studynote/13_cloud_architecture/2_container_k8s/116_kubernetes_container_image_security_scanning.md": """+++
weight = 116
title = "쿠버네티스 컨테이너 이미지 보안 스캐닝 자동화"
date = "2026-03-04"
[extra]
categories = ["studynote-cloud"]
+++

## 핵심 인사이트 (3줄 요약)
1. **컨테이너 이미지 보안 스캐닝**은 도커(Docker)나 OCI 이미지 내부에 포함된 OS 패키지, 라이브러리(Log4j 등)의 알려진 취약점(CVE)과 하드코딩된 시크릿을 배포 전 식별하는 방어 체계입니다.
2. Trivy, Clair, Anchore 등의 도구를 CI/CD 파이프라인에 통합(Shift-Left)하여, 취약한 이미지가 쿠버네티스 클러스터로 업로드/배포되는 것을 원천 차단합니다.
3. 데브섹옵스(DevSecOps)의 가장 핵심적인 실천 방안이며, 제로 트러스트(Zero Trust) 및 소프트웨어 공급망 보안(SBOM)을 달성하기 위한 필수 조건입니다.

### Ⅰ. 개요 (Context & Background)
컨테이너는 베이스 이미지(Ubuntu, Alpine)를 상속받아 빌드되므로, 개발자가 알지 못하는 수많은 오픈소스 종속성 취약점이 내포될 수 있습니다. 악성 코드가 포함된 이미지가 K8s에 배포되면 하이퍼바이저 샌드박스 우회나 크립토마이닝(코인 채굴) 등 심각한 침해 사고로 직결되므로, 런타임 이전 단계의 철저한 정적 분석(SCA)이 요구됩니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
스캐너는 이미지의 레이어(Layer)를 파싱하여 설치된 패키지 목록을 추출한 뒤, 중앙 취약점 데이터베이스(NVD, MITRE)와 대조합니다.

```text
+-------------------------------------------------------------+
|               Container Security Scanning Pipeline          |
|                                                             |
|  [Dockerfile] -> `docker build` -> [Image Artifact]         |
|                                         |                   |
|  [CI/CD Runner] -> Runs `trivy image <img_name>`            |
|       |                                                     |
|       +--> Parses Base OS & App dependencies (npm, pip)     |
|       +--> Checks against CVE Database                      |
|                                                             |
|  [Result]                                                   |
|   -> CRITICAL/HIGH found? -> Block CI Pipeline (Fail)       |
|   -> Clean? -> Push to Container Registry -> Deploy to K8s  |
+-------------------------------------------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 스캐닝 도구 | 특징 및 생태계 | 스캔 속도 | 활용 단계 |
|---|---|---|---|
| **Trivy (Aqua Sec)** | 빠르고 설정이 쉬움, OS + 언어 종속성 + IaC 파일까지 모두 스캔 | 매우 빠름 (Standalone) | CI 파이프라인, 로컬 개발 |
| **Clair (CoreOS)** | 컨테이너 레지스트리(Quay, Harbor) 통합에 강력 | DB 세팅 필요 (보통) | Registry 업로드 시 자동 훅 |
| **Anchore Engine** | 세밀한 정책(Policy) 제어 엔진 제공, 컴플라이언스 룰셋 적용 | 다소 무거움 | 엔터프라이즈 DevSecOps 중앙 통제 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **어드미션 컨트롤러(Admission Controller) 연계**: CI 단계를 우회하고 수동으로 올라온 이미지에 대비하여, K8s 클러스터 내부에 OPA Gatekeeper나 Kyverno를 구성해 "취약점 스캔 통과 서명(Signature)이 없는 이미지는 배포 거부"하는 강제(Enforcement) 룰을 적용해야 합니다.
* **오탐(False Positive)과 경고 피로**: 모든 'Low/Medium' 취약점까지 빌드를 실패시키면 개발 속도가 저해됩니다. 'Critical/High'와 픽스(Fix)가 존재하는 취약점만 파이프라인을 멈추도록 정책을 테일러링(Tailoring)해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
컨테이너 스캐닝을 파이프라인에 이식하면 런타임 보안 사고율을 90% 이상 예방할 수 있습니다. 최근 보안 트렌드인 소프트웨어 자재 명세서(SBOM, Software Bill of Materials) 자동 생성 기능과 결합하여 전사적인 취약점 거버넌스를 확립하는 방향으로 발전하고 있습니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **상위 개념**: 데브섹옵스(DevSecOps), 클라우드 네이티브 보안
* **하위 개념**: CVE(Common Vulnerabilities and Exposures), OCI 이미지, Trivy
* **연관 개념**: OPA Gatekeeper, SBOM, 공급망 보안(Supply Chain Security)

### 👶 어린이를 위한 3줄 비유 설명
1. 여러분이 공항에서 비행기를 탈 때 보안 검색대에서 엑스레이로 가방을 꼼꼼히 검사하죠?
2. 컨테이너 이미지 스캐닝은 프로그램이 쿠버네티스(비행기)에 타기 전에 혹시 나쁜 폭탄(버그, 바이러스)이 숨어있지 않은지 엑스레이로 미리 검사하는 거예요.
3. 위험한 물건이 발견되면 경고음이 울리고 절대로 비행기에 탈 수 없게 막아준답니다!
""",

    "content/studynote/13_cloud_architecture/2_container_k8s/117_kubernetes_network_policy_micro_segmentation.md": """+++
weight = 117
title = "쿠버네티스 네트워크 폴리시 (마이크로 세그멘테이션)"
date = "2026-03-04"
[extra]
categories = ["studynote-cloud"]
+++

## 핵심 인사이트 (3줄 요약)
1. **네트워크 폴리시(Network Policy)**는 쿠버네티스 내부 파드(Pod) 간의 통신 트래픽(Inbound/Outbound)을 L3/L4 계층에서 IP와 Port 기반으로 통제하는 소프트웨어 정의 방화벽(SDN 방화벽)입니다.
2. 해커가 웹 서버 파드를 탈취하더라도, 내부 DB 파드로 횡적 이동(Lateral Movement)을 하지 못하게 차단하는 **마이크로 세그멘테이션(Micro-segmentation)**을 실현합니다.
3. 이를 구동하려면 Calico나 Cilium과 같은 네트워크 정책 기능을 지원하는 전용 CNI(Container Network Interface) 플러그인이 클러스터에 설치되어 있어야 합니다.

### Ⅰ. 개요 (Context & Background)
기본적으로 쿠버네티스 클러스터 내부의 모든 파드는 아무런 제한 없이 서로 자유롭게 통신(Default Allow All)할 수 있습니다. 이는 클라우드 네이티브 환경에서 심각한 보안 홀(Hole)을 의미합니다. 침해 사고 확산을 막고 제로 트러스트(Zero Trust) 철학을 구현하기 위해 파드 단위의 정밀한 망분리 규정이 필수적으로 요구되며, 이를 명세형(YAML) 코드로 제어하는 기술이 바로 Network Policy입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
네트워크 폴리시는 라벨 셀렉터(Label Selector)를 사용하여 타겟 파드를 식별하고, Ingress(수신)와 Egress(발신) 트래픽 규칙을 화이트리스트(Default Deny, Allow Specific) 방식으로 적용합니다.

```text
+-------------------------------------------------------------+
|               Network Policy Micro-segmentation             |
|                                                             |
|   [Attacker] -> compromises -> [Frontend Pod]               |
|                                   |  (Lateral Move Blocked) |
|                                   X                         |
|   Network Policy:                 |                         |
|   Only [Backend Pod] can access [Database Pod] on port 3306 |
|                                                             |
|  [Frontend Pod] --(Allowed)--> [Backend Pod]                |
|                                      |                      |
|                                  (Allowed)                  |
|                                      v                      |
|                                 [Database Pod]              |
+-------------------------------------------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 접근 통제 방식 | 인프라 방화벽 (AWS Security Group) | K8s Network Policy | 서비스 메시 (Istio Authorization) |
|---|---|---|---|
| **통제 수준** | L3/L4 (Node, VM 단위) | L3/L4 (Pod, IP/Port 단위) | L7 (HTTP Header, URL Path 단위) |
| **식별자** | IP 주소, CIDR | **K8s 라벨(Label), Namespace** | 서비스 서비스 어카운트(mTLS 인증서) |
| **동적 확장성** | Pod 재생성 시 IP 변경 대응 어려움 | 라벨 기반이므로 자동 적용 매핑 | 인증서 기반이므로 가장 강력함 |
| **운영 주체** | 클라우드 인프라 팀 | K8s/플랫폼 보안 팀 | 서비스 개발/데브옵스 팀 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **Default Deny All 정책 적용**: 네임스페이스를 생성할 때 가장 먼저 '모든 트래픽을 차단(Default Deny Ingress/Egress)'하는 정책을 깐 뒤, 통신이 필요한 서비스(예: Frontend -> API)만 명시적으로 허용(Whitelist)하는 방식으로 설계해야 강력한 보안이 유지됩니다.
* **CNI 선택**: Flannel 같은 기본 CNI는 통신망만 뚫어줄 뿐 Network Policy를 적용하지 못합니다. 상용 엔터프라이즈 환경에서는 정책 집행 성능이 우수한 Calico 기반 iptables나, 최근 eBPF 기술을 통해 커널 단에서 초고속 통제를 수행하는 Cilium을 채택하는 것이 기술사적 권장 아키텍처입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
네트워크 폴리시를 통한 마이크로 세그멘테이션은 ISMS-P 및 클라우드 보안 인증(CSAP) 심사 시 내부망 격리 요건을 충족하는 핵심 기술입니다. 향후 L7 영역의 애플리케이션 보안까지 커버하기 위해 Istio와 같은 서비스 메시와 결합한 다층적(Defense-in-Depth) 보안 구조로 진화하고 있습니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **상위 개념**: 클라우드 네이티브 보안, 쿠버네티스
* **하위 개념**: Ingress/Egress, 라벨 셀렉터, CNI
* **연관 개념**: 제로 트러스트, 횡적 이동(Lateral Movement), Calico, Cilium, eBPF

### 👶 어린이를 위한 3줄 비유 설명
1. 학교에 수백 개의 교실(파드)이 있는데, 처음에는 모든 교실 문이 열려 있어서 아무나 마음대로 뛰어다닐 수 있었어요.
2. 하지만 네트워크 폴리시라는 '스마트 교문 지킴이'가 생기면, "1반 학생은 화장실만 갈 수 있고 2반에는 절대 못 들어가!"라고 규칙을 정할 수 있어요.
3. 만약 한 교실에 무서운 악당(해커)이 몰래 들어와도 다른 교실로는 넘어갈 수 없게 꽁꽁 가둬버리는 멋진 방패랍니다!
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

