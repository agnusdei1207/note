+++
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
