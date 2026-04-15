+++
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
