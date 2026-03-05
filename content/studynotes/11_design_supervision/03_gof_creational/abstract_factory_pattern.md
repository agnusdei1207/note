+++
title = "추상 팩토리 패턴 (Abstract Factory Pattern)"
categories = ["studynotes-11_design_supervision"]
+++

# 추상 팩토리 패턴 (Abstract Factory Pattern)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 추상 팩토리 패턴은 서로 연관되거나 의존적인 **여러 객체 군(Family)**을 구체적인 클래스를 지정하지 않고 하나의 팩토리 인터페이스를 통해 일괄 생성하는 생성 패턴입니다.
> 2. **가치**: 클라이언트는 구체 팩토리만 교체하면 전체 제품군을 일관되게 변경할 수 있어, UI 테마 전환, DB 벤더 교체, 플랫폼 간 이식 등에 강력한 유연성을 제공합니다.
> 3. **융합**: 크로스 플랫폼 GUI 프레임워크, 데이터베이스 독립적 DAO, 그리고 마이크로서비스의 환경별 설정 관리에 활용됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 추상 팩토리 패턴의 정의
추상 팩토리(Abstract Factory) 패턴은 **"연관된 객체들의 집합을 생성하기 위한 인터페이스를 제공"**하는 패턴입니다. 클라이언트는 구체적인 클래스를 지정하지 않고도 일관된 스타일이나 테마를 가진 관련 객체들을 생성할 수 있습니다. 이는 팩토리 메서드 패턴을 **여러 제품 유형으로 확장**한 것으로 볼 수 있습니다.

### 💡 비유: 가구 세트 구매
이케아에 가서 '북유럽 스타일' 가구 세트를 주문하면 의자, 테이블, 소파가 모두 북유럽 스타일로 옵니다. '모던 스타일'로 바꾸면 모든 가구가 모던 스타일로 바뀌죠. 추상 팩토리는 이처럼 **일관된 스타일의 제품군**을 생성합니다.

### 2. 등장 배경
- **일관성 보장**: 관련 객체들이 서로 어울리도록 보장
- **플랫폼 독립성**: 운영체제별로 다른 UI 컴포넌트 일관되게 생성
- **제품군 교체**: 전체 제품군을 쉽게 교체 가능

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 추상 팩토리 구조 다이어그램

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                      추상 팩토리 패턴 구조                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────┐         ┌─────────────────────┐                  │
│   │  AbstractFactory    │         │   AbstractProductA  │                  │
│   │  <<interface>>      │         │   <<interface>>     │                  │
│   ├─────────────────────┤         ├─────────────────────┤                  │
│   │ + createProductA()  │────────►│ + operationA()      │                  │
│   │ + createProductB()  │         └──────────┬──────────┘                  │
│   └──────────┬──────────┘                    │                              │
│              │              ┌────────────────┴────────────────┐             │
│              │              │                                 │             │
│   ┌──────────┴─────────┐ ┌──▼────────────┐         ┌────────▼────┐        │
│   │ ConcreteFactory1   │ │ProductA1      │         │ProductA2    │        │
│   ├────────────────────┤ │(Style 1)      │         │(Style 2)    │        │
│   │+ createProductA()  │ ├───────────────┤         ├─────────────┤        │
│   │  return ProductA1()│ │+operationA()  │         │+operationA()│        │
│   │+ createProductB()  │ └───────────────┘         └─────────────┘        │
│   │  return ProductB1()│                                                    │
│   └────────────────────┘         ┌─────────────────────┐                  │
│                                  │   AbstractProductB  │                  │
│   ┌────────────────────┐         │   <<interface>>     │                  │
│   │ ConcreteFactory2   │────────►├─────────────────────┤                  │
│   ├────────────────────┤         │ + operationB()      │                  │
│   │+ createProductA()  │         └──────────┬──────────┘                  │
│   │  return ProductA2()│                    │                              │
│   │+ createProductB()  │         ┌──────────┴──────────┐                  │
│   │  return ProductB2()│         │                     │                  │
│   └────────────────────┘    ┌────▼────┐         ┌──────▼────┐             │
│                              │ProductB1│         │ProductB2  │             │
│                              │(Style 1)│         │(Style 2)  │             │
│                              └─────────┘         └───────────┘             │
│                                                                             │
│   [클라이언트 사용]                                                          │
│   val factory: AbstractFactory = ConcreteFactory1()                        │
│   val productA = factory.createProductA()  // ProductA1 반환               │
│   val productB = factory.createProductB()  // ProductB1 반환               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 핵심 구성 요소

| 구성 요소 | 역할 | 설명 |
|:---:|:---|:---|
| **AbstractFactory** | 인터페이스 | 제품 군 생성을 위한 추상 인터페이스 |
| **ConcreteFactory** | 구체 클래스 | 특정 제품 군의 실제 생성 구현 |
| **AbstractProduct** | 인터페이스 | 제품의 공통 인터페이스 |
| **ConcreteProduct** | 구체 클래스 | 구체 팩토리가 생성하는 실제 제품 |
| **Client** | 클라이언트 | 추상 팩토리와 추상 제품만 사용 |

### 3. 구현 예시: 크로스 플랫폼 UI

```kotlin
// Abstract Products
interface Button {
    fun paint(): String
}

interface Checkbox {
    fun paint(): String
}

// Abstract Factory
interface GUIFactory {
    fun createButton(): Button
    fun createCheckbox(): Checkbox
}

// Concrete Products - Windows Style
class WindowsButton : Button {
    override fun paint() = "Windows 스타일 버튼"
}

class WindowsCheckbox : Checkbox {
    override fun paint() = "Windows 스타일 체크박스"
}

// Concrete Products - Mac Style
class MacButton : Button {
    override fun paint() = "Mac 스타일 버튼"
}

class MacCheckbox : Checkbox {
    override fun paint() = "Mac 스타일 체크박스"
}

// Concrete Factories
class WindowsFactory : GUIFactory {
    override fun createButton() = WindowsButton()
    override fun createCheckbox() = WindowsCheckbox()
}

class MacFactory : GUIFactory {
    override fun createButton() = MacButton()
    override fun createCheckbox() = MacCheckbox()
}

// Client
class Application(private val factory: GUIFactory) {
    fun render() {
        val button = factory.createButton()
        val checkbox = factory.createCheckbox()
        println("${button.paint()}, ${checkbox.paint()}")
    }
}
```

### 4. 팩토리 메서드 vs 추상 팩토리

```text
[비교 구조]

팩토리 메서드:
  Creator ─────► Product (1종류)
     │
     └─► factoryMethod()

추상 팩토리:
  AbstractFactory ─────► ProductA, ProductB, ProductC... (여러 종류)
     │
     ├─► createProductA()
     ├─► createProductB()
     └─► createProductC()

[관계]
추상 팩토리의 각 create 메서드는 사실상 팩토리 메서드
→ 추상 팩토리 = 여러 팩토리 메서드의 집합
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (비교표 2개+)

### 1. 생성 패턴 비교

| 패턴 | 생성 대상 | 일관성 보장 | 확장성 | 복잡도 |
|:---:|:---|:---:|:---:|:---:|
| **팩토리 메서드** | 단일 제품 | X | 제품 추가 용이 | 중간 |
| **추상 팩토리** | 제품 군 | **O** | 제품군 추가 용이 | 높음 |
| **빌더** | 복잡한 단일 객체 | X | 구성 변경 용이 | 높음 |
| **프로토타입** | 복제 가능 객체 | X | 프로토타입 추가 | 낮음 |

### 2. 활용 사례

| 분야 | 예시 | 제품군 |
|:---:|:---|:---|
| **GUI** | Swing, JavaFX | Button, Checkbox, ScrollBar |
| **DB** | JDBC DAO | Connection, Statement, ResultSet |
| **게임** | 캐릭터 종족 | Weapon, Armor, Skill |
| **테마** | 다크/라이트 모드 | Color, Font, Icon |

### 3. 장단점 분석

| 장점 | 단점 |
|:---|:---|
| 제품군 일관성 보장 | 새로운 제품 추가 어려움 |
| 구체 클래스 분리 | 클래스 수 증가 |
| 팩토리 교체 용이 | 복잡도 증가 |
| OCP 준수 | - |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (800자+)

### 기술사적 판단 (실무 시나리오)

#### 시나리오 1: 데이터베이스 벤더 교체
- **상황**: Oracle → PostgreSQL 마이그레이션
- **전략**: DAO 추상 팩토리로 DB별 구현체 제공
- **기술사적 판단**: 팩토리만 교체하면 전체 DAO 교체 가능

#### 시나리오 2: 다크/라이트 테마 전환
- **상황**: 사용자 테마 설정에 따른 UI 컴포넌트 교체
- **전략**: ThemeFactory로 Color, Font, Icon 일괄 생성
- **기술사적 판단**: 테마 전환 시 모든 컴포넌트 일관성 보장

### 도입 체크리스트
- [ ] 연관된 객체 군을 생성해야 하는가?
- [ ] 제품군 전체를 교체할 가능성이 있는가?
- [ ] 일관성 보장이 중요한가?
- [ ] 새로운 제품 추가보다 제품군 추가가 더 빈번한가?

---

## Ⅴ. 기대효과 및 결론 (400자+)

### 기대효과

| 구분 | 효과 |
|:---:|:---|
| **일관성** | 제품군 내 모든 제품의 스타일/동작 일관 |
| **교체 용이성** | 팩토리 교체만으로 전체 제품군 변경 |
| **결합도 저감** | 클라이언트가 구체 클래스에 의존하지 않음 |

### 참고 표준
- **GoF Design Patterns**: 추상 팩토리 패턴 정의
- **Java AWT/Swing**: Peer 아키텍처

---

## 📌 관련 개념 맵
- [팩토리 메서드](./factory_method_pattern.md): 단일 객체 생성
- [빌더 패턴](./builder_pattern.md): 복잡한 객체 조립
- [브리지 패턴](../04_gof_structural/bridge_pattern.md): 구현 계층 분리
- [전략 패턴](../05_gof_behavioral/strategy_pattern.md): 알고리즘 교체

---

## 👶 어린이를 위한 3줄 비유
1. 추상 팩토리는 **세트로 된 장난감**을 사는 것과 같아요. 경찰차 세트를 사면 경찰차, 경찰인형, 신호등이 다 같이 와요.
2. 소방차 세트로 바꾸면 소방차, 소방관 인형, 소화전이 와요. 섞여서 오지 않죠!
3. 이렇게 하면 어떤 세트를 고르든 **모든 장난감이 어울리게** 같이 놀 수 있어요!
