+++
weight = 153
title = "브리지 패턴 (Bridge Pattern)"
date = "2026-03-04"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
1. **관심사 분리**: 추상화(Abstraction) 계층과 구현(Implementation) 계층을 완전히 분리하여 각각 독립적으로 확장 가능하게 하는 구조 패턴입니다.
2. **상속의 폭발 방지**: 기능과 플랫폼이 기하급수적으로 늘어날 때 발생하는 '상속의 조합 폭발' 문제를 합성(Composition)을 통해 해결합니다.
3. **런타임 유연성**: 컴파일 타임이 아닌 런타임에 구현체를 동적으로 교체할 수 있어 시스템의 결합도를 낮추고 유지보수성을 극대화합니다.

### Ⅰ. 개요 (Context & Background)
브리지 패턴은 "구현(Implementation)에서 추상화(Abstraction)를 분리하여 두 계층이 독립적으로 변할 수 있도록 한다"는 원칙을 따릅니다. 주로 그래픽 윈도우 시스템이나 드라이버 설계와 같이, 하나의 기능이 여러 종류의 운영체제나 하드웨어 플랫폼에서 동작해야 할 때 사용됩니다. 상속(Inheritance)은 클래스 간의 강한 결합을 유발하지만, 브리지는 합성(Composition)을 통해 수평적 확장을 지원합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
브리지 패턴은 추상부(Abstraction), 정교화된 추상부(Refined Abstraction), 구현자(Implementor), 구체적인 구현자(Concrete Implementor)의 4가지 구성요소로 이루어집니다.

```text
  [ Abstraction ] (추상부) ------------> [ Implementor ] (구현자 인터페이스)
         ^                                      ^
         |                                      |
[ Refined Abstraction ]              [ Concrete Implementor ] (구체적 구현)
   (기능 확장 계층)                       (플랫폼별 실제 로직)

  <Bilingual Flow Diagram>
  1. Client calls Abstraction.operation() -> 클라이언트가 추상부 호출
  2. Abstraction delegates to Implementor -> 추상부가 구현자에게 위임
  3. Implementor.devSpecificLogic() -> 실제 플랫폼별 로직 수행
```

- **Abstraction**: 기능 계층의 최상위 클래스로, 구현자 객체에 대한 참조를 유지합니다.
- **Implementor**: 구현 계층의 인터페이스로, 실제 작업을 수행하는 기본 연산들을 정의합니다.
- **Bridge**: Abstraction이 Implementor를 멤버 변수로 가지고 있는 관계 자체가 '다리(Bridge)' 역할을 수행합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
브리지 패턴은 다른 구조 패턴과 혼동되기 쉬우나 목적이 명확히 다릅니다.

| 구분 | 브리지 패턴 (Bridge) | 어댑터 패턴 (Adapter) | 전략 패턴 (Strategy) |
| :--- | :--- | :--- | :--- |
| **핵심 목적** | 설계 단계에서 기능과 구현 분리 | 이미 존재하는 두 인터페이스의 호환 | 알고리즘의 동적 교체 |
| **사용 시점** | 시스템 설계(Design) 초기 | 개발 중(After-fact) 연동 시 | 행위(Behavior) 선택 시 |
| **관계 구조** | Abstraction - Implementor (1:1) | Client - Adaptee (1:1) | Context - Strategy (1:N) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **적용 케이스**: 
    - OS별 GUI 컴포넌트 처리 (WindowsButton, MacButton 등)
    - 데이터베이스 드라이버 (JDBC: Java의 표준 인터페이스와 각 벤더별 드라이버 구현 분리)
    - 로그 라이브러리 (추상 로그 API와 실제 저장 매체-File, DB, Console 분리)
- **기술사적 판단**: 브리지 패턴은 **OCP(Open-Closed Principle)**와 **DIP(Dependency Inversion Principle)**를 가장 충실히 구현하는 패턴입니다. 클래스 계층 구조가 너무 복잡해져서 관리가 불가능할 때, 계층을 두 개(기능 계층, 구현 계층)로 쪼개는 'Surgical Divide' 전략으로 활용해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
브리지 패턴을 적용하면 구현 세부 사항이 클라이언트로부터 완전히 숨겨지므로, 구현 코드를 변경하거나 새로운 플랫폼을 추가해도 클라이언트 코드를 수정할 필요가 없습니다. 이는 대규모 엔터프라이즈 시스템의 **유지보수 비용(TCO) 절감**과 **이식성(Portability) 확보**에 결정적인 역할을 합니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: 구조 패턴 (Structural Patterns), 합성 (Composition)
- **유사 개념**: 어댑터 패턴 (Adapter), 전략 패턴 (Strategy)
- **하위 기술**: 인터페이스 분리, 다형성 (Polymorphism)

### 👶 어린이를 위한 3줄 비유 설명
1. **만능 리모컨(추상부)**과 **여러 대의 TV(구현부)**를 생각해보세요.
2. 리모컨의 '채널 변경' 버튼을 누르면, 이 리모컨이 삼성 TV에 연결됐든 LG TV에 연결됐든 상관없이 TV가 채널을 바꿔요.
3. 리모컨 모양을 바꾸거나 새로운 TV를 사와도, 리모컨 버튼을 누르는 방법은 변하지 않는 것과 같아요.
