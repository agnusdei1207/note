+++
title = "팩토리 메서드 패턴 (Factory Method Pattern)"
categories = ["studynotes-11_design_supervision"]
+++

# 팩토리 메서드 패턴 (Factory Method Pattern)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 팩토리 메서드 패턴은 객체를 생성하는 인터페이스는 상위 클래스가 정의하되, **실제 생성할 객체의 클래스는 하위 클래스가 결정**하도록 위임하는 생성 패턴입니다.
> 2. **가치**: 클라이언트 코드를 구체 클래스에 의존하지 않게 하여 OCP(개방-폐쇄 원칙)를 실현하고, 확장에는 열려 있으면서도 수정에는 닫혀 있는 유연한 구조를 제공합니다.
> 3. **융합**: 스프링 프레임워크의 BeanFactory, JPA의 EntityManagerFactory, 그리고 마이크로서비스의 서비스 디스커버리 패턴과 연관됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 팩토리 메서드 패턴의 정의
팩토리 메서드(Factory Method) 패턴은 **"객체 생성을 서브클래스에게 위임"**하는 패턴입니다. 상위 클래스에서는 인스턴스를 만드는 방법(인터페이스)만 결정하고, 실제 어떤 구체적인 클래스의 인스턴스를 생성할지는 하위 클래스가 결정합니다. 이를 통해 클라이언트는 구체적인 클래스를 알 필요 없이 객체를 생성할 수 있습니다.

### 💡 비유: 피자 가게의 주문 시스템
피자 가게에서 손님이 "피자 주문해요!"라고 하면, 점원은 어떤 피자를 만들지 결정합니다. 뉴욕 스타일 가게면 뉴욕 피자를, 시카고 스타일 가게면 시카고 피자를 만들죠. 손님은 **어떻게 만드는지 알 필요 없이** 주문만 하면 됩니다. 팩토리 메서드는 이처럼 객체 생성의 세부 사항을 캡슐화합니다.

### 2. 등장 배경
- **new 연산자의 문제**: 구체 클래스에 직접 의존하면 유연성 저하
- **OCP 위반**: 새로운 타입 추가 시 클라이언트 코드 수정 필요
- **복잡한 생성 로직**: 객체 생성에 조건 분기가 많아지면 유지보수 어려움

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 팩토리 메서드 구조 다이어그램

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                     팩토리 메서드 패턴 구조                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────┐           ┌─────────────────────┐                │
│   │     <<interface>>    │           │      Creator        │                │
│   │       Product        │           │  (Factory)          │                │
│   ├─────────────────────┤           ├─────────────────────┤                │
│   │ + operation()       │           │ + factoryMethod()   │ ← abstract    │
│   └──────────┬──────────┘           │ + someOperation()   │                │
│              │                       └──────────┬──────────┘                │
│              │ implements                       │ extends                   │
│     ┌────────┴────────┐               ┌────────┴────────┐                  │
│     │                 │               │                 │                  │
│  ┌──▼───────┐    ┌────▼───┐       ┌──▼───────┐    ┌────▼───┐              │
│  │ConcreteP1│    │ConcreteP2│      │ConcreteC1│    │ConcreteC2│             │
│  ├──────────┤    ├────────┤       ├──────────┤    ├────────┤              │
│  │+operation│    │+operation│      │+factoryM │    │+factoryM │             │
│  └──────────┘    └────────┘       │  ()      │    │  ()      │             │
│                                    │  return  │    │  return  │             │
│                                    │  P1      │    │  P2      │             │
│                                    └──────────┘    └────────┘              │
│                                                                             │
│   [클라이언트 사용]                                                          │
│   Creator creator = new ConcreteCreator1();                                 │
│   Product product = creator.factoryMethod(); // ConcreteProduct1 반환       │
│   product.operation();                                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 핵심 구성 요소

| 구성 요소 | 역할 | 설명 |
|:---:|:---|:---|
| **Product** | 인터페이스/추상클래스 | 팩토리가 생성할 객체의 인터페이스 |
| **ConcreteProduct** | 구체 클래스 | 실제 생성되는 객체 |
| **Creator** | 추상 클래스 | 팩토리 메서드 선언 |
| **ConcreteCreator** | 구체 클래스 | 실제 Product 인스턴스 생성 |

### 3. 구현 예시

```kotlin
// Product 인터페이스
interface Transport {
    fun deliver(): String
}

// Concrete Products
class Truck : Transport {
    override fun deliver() = "트럭으로 육로 배송"
}

class Ship : Transport {
    override fun deliver() = "배로 해로 배송"
}

// Creator (Factory)
abstract class Logistics {
    // 팩토리 메서드
    abstract fun createTransport(): Transport

    // 비즈니스 로직
    fun planDelivery(): String {
        val transport = createTransport()
        return "배송 계획: ${transport.deliver()}"
    }
}

// Concrete Creators
class RoadLogistics : Logistics() {
    override fun createTransport() = Truck()
}

class SeaLogistics : Logistics() {
    override fun createTransport() = Ship()
}

// 클라이언트 사용
fun main() {
    val logistics: Logistics = RoadLogistics()
    println(logistics.planDelivery()) // "배송 계획: 트럭으로 육로 배송"
}
```

### 4. 팩토리 메서드 vs 단순 팩토리

```text
[단순 팩토리 (Simple Factory) - 패턴 아님]

class SimpleFactory {
    fun create(type: String): Product {
        return when (type) {  // OCP 위반: 새 타입 추가 시 수정 필요
            "A" -> ConcreteProductA()
            "B" -> ConcreteProductB()
            else -> throw IllegalArgumentException()
        }
    }
}

[팩토리 메서드 - GoF 패턴]

abstract class Factory {
    abstract fun create(): Product  // 하위 클래스에서 구현
    // 새 타입 추가 시 새로운 하위 클래스만 추가하면 됨 (OCP 준수)
}
```

### 5. 매개변수화 팩토리 메서드

```text
┌─────────────────────────────────────────────────────────────────┐
│             매개변수화 팩토리 메서드 (Parameterized Factory)       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   abstract class Dialog {                                       │
│       fun render() {                                            │
│           val button = createButton("확인")  // 매개변수 전달     │
│           button.onClick { /* ... */ }                          │
│           button.render()                                       │
│       }                                                         │
│                                                                 │
│       abstract fun createButton(caption: String): Button        │
│   }                                                             │
│                                                                 │
│   class WindowsDialog : Dialog() {                              │
│       override fun createButton(caption: String) =              │
│           WindowsButton(caption)                                │
│   }                                                             │
│                                                                 │
│   class WebDialog : Dialog() {                                  │
│       override fun createButton(caption: String) =              │
│           HTMLButton(caption)                                   │
│   }                                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (비교표 2개+)

### 1. 생성 패턴 비교

| 패턴 | 목적 | 생성 시점 결정 | 생성 책임 | 복잡도 |
|:---:|:---|:---|:---|:---:|
| **팩토리 메서드** | 하위 클래스에 생성 위임 | 컴파일 타임 | 하위 클래스 | 중간 |
| **추상 팩토리** | 연관 객체 군 생성 | 런타임 | 구체 팩토리 | 높음 |
| **빌더** | 복잡한 객체 단계적 생성 | 런타임 | 클라이언트 | 높음 |
| **프로토타입** | 복제를 통한 생성 | 런타임 | 프로토타입 | 낮음 |
| **싱글톤** | 유일 인스턴스 보장 | 최초 접근 시 | 클래스 자신 | 낮음 |

### 2. 팩토리 메서드 활용 사례

| 프레임워크 | 활용 예시 | 설명 |
|:---:|:---|:---|
| **Java Collections** | `Collections.singleton()` | 불변 컬렉션 생성 |
| **Spring** | `FactoryBean` | Bean 생성 로직 캡슐화 |
| **JPA** | `EntityManagerFactory` | EntityManager 생성 |
| **Android** | `onCreateViewHolder` | RecyclerView ViewHolder 생성 |
| **JUnit** | `Parameterized` | 테스트 케이스 생성 |

### 3. OCP 관점 분석

```text
[OCP 준수 여부 비교]

                     새로운 Product 추가 시
                           │
          ┌────────────────┴────────────────┐
          │                                  │
          ▼                                  ▼
   ┌──────────────┐                  ┌──────────────┐
   │ 팩토리 메서드 │                  │   직접 생성   │
   │    적용      │                  │  (new 연산자) │
   └──────┬───────┘                  └──────┬───────┘
          │                                  │
          ▼                                  ▼
   기존 코드 수정 X                   기존 코드 수정 O
   새로운 Creator만 추가              모든 생성 코드 수정
   (OCP 준수)                         (OCP 위반)
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (800자+)

### 기술사적 판단 (실무 시나리오)

#### 시나리오 1: 멀티 플랫폼 UI 컴포넌트
- **상황**: Windows, macOS, Linux 각각 다른 버튼/다이얼로그 구현 필요
- **전략**: 팩토리 메서드로 플랫폼별 구체 팩토리 구현
- **기술사적 판단**: 플랫폼별 코드 분리로 유지보수성 향상

#### 시나리오 2: 데이터베이스 독립적 DAO
- **상황**: Oracle, MySQL, PostgreSQL 지원 필요
- **전략**: DAO 팩토리 메서드로 DB별 DAO 생성
- **기술사적 판단**: 추후 새로운 DB 추가 시 기존 코드 수정 없이 확장 가능

### 도입 시 고려사항 체크리스트

**[팩토리 메서드 도입 체크리스트]**
- [ ] 객체 생성 로직이 복잡한가?
- [ ] 다양한 타입의 객체를 생성해야 하는가?
- [ ] 생성될 객체 타입이 런타임에 결정되는가?
- [ ] OCP를 준수해야 하는가?
- [ ] 하위 클래스 확장이 예상되는가?

### 안티패턴 주의사항

| 안티패턴 | 설명 | 대응 방안 |
|:---:|:---|:---|
| **과도한 서브클래싱** | 제품마다 Creator 서브클래스 생성 | 매개변수화 팩토리 또는 추상 팩토리 고려 |
| **불필요한 추상화** | 제품이 하나뿐인데 패턴 적용 | 단순 팩토리로 충분 |
| **팩토리의 비대화** | 팩토리에 비즈니스 로직 혼재 | 팩토리는 생성 책임만 담당 |

---

## Ⅴ. 기대효과 및 결론 (400자+)

### 정량적/정성적 기대효과

| 구분 | 효과 | 기대 수치 |
|:---:|:---|:---|
| **확장성** | 새로운 타입 추가 용이 | 코드 수정 0% |
| **유지보수성** | 생성 로직 중앙화 | 변경 영향 최소화 |
| **테스트 용이성** | Mock 객체 생성 용이 | 테스트 커버리지 향상 |
| **결합도** | 구체 클래스 의존 제거 | 의존성 역전 원칙 준수 |

### 미래 전망
1. **DI 컨테이너 통합**: 스프링 등에서 팩토리 빈으로 활용
2. **함수형 팩토리**: 람다/함수 참조로 팩토리 구현
3. **빌더와 결합**: 복잡한 객체 생성 시 빌더와 조합

### 참고 표준/가이드
- **GoF Design Patterns**: 팩토리 메서드 패턴 원본 정의
- **Effective Java**: 정적 팩토리 메서드 권장
- **Clean Code**: 팩토리 활용 가이드

---

## 📌 관련 개념 맵 (5개+)
- [추상 팩토리 패턴](./abstract_factory_pattern.md): 연관 객체 군 생성
- [빌더 패턴](./builder_pattern.md): 복잡한 객체 단계적 생성
- [템플릿 메서드 패턴](../05_gof_behavioral/template_method_pattern.md): 팩토리 메서드의 기반
- [OCP 원칙](../02_principles/solid_principles.md): 개방-폐쇄 원칙 실현
- [DI 컨테이너](../02_principles/dependency_injection.md): 팩토리의 현대적 구현

---

## 👶 어린이를 위한 3줄 비유
1. 팩토리 메서드는 **장난감 가게에서 주문을 받는 방식**과 같아요. 손님이 "로봇 장난감 주세요"라고 하면, 점원은 어떤 로봇을 줄지 결정해요.
2. 서울 가게는 서울 로봇을, 부산 가게는 부산 로봇을 주죠. 손님은 **어느 가게인지만 알면 되고**, 로봇을 직접 만들 필요는 없어요.
3. 이렇게 하면 새로운 지역에 가게가 생겨도, 기존 가게들은 전혀 바꿀 필요가 없어요!
