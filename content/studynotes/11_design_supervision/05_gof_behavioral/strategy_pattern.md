+++
title = "전략 패턴 (Strategy Pattern)"
categories = ["studynotes-11_design_supervision"]
+++

# 전략 패턴 (Strategy Pattern)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전략 패턴은 동일 계열의 **알고리즘들을 캡슐화**하고 인터페이스화하여, 런타임에 클라이언트 코드 변경 없이 **알고리즘(전략)을 쉽게 교체**할 수 있게 하는 행위 패턴입니다.
> 2. **가치**: 복잡한 조건문(if-else/switch)을 다형성으로 대체하여 OCP를 실현하고, 각 알고리즘을 독립적으로 테스트할 수 있어 유지보수성이 크게 향상됩니다.
> 3. **융합**: 결제 수단 선택, 정렬 알고리즘, 압축 방식, 라우팅 알고리즘 등 다양한 영역에서 활용되며, 스프링의 @Qualifier, 함수형 프로그래밍의 고차함수와 연관됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 전략 패턴의 정의
전략(Strategy) 패턴은 **"알고리즘군을 정의하고, 각각을 캡슐화하여 교체해서 사용할 수 있게 만드는 패턴"**입니다. 클라이언트는 사용하는 알고리즘에 독립적으로, 알고리즘의 변경이나 확장이 클라이언트에 영향을 주지 않습니다.

### 💡 비유: 내비게이션의 경로 탐색
내비게이션에서 목적지까지 가는 방법은 여러 가지입니다. **최단 거리, 고속도로 우선, 유료 도로 회피** 등. 사용자는 상황에 따라 다른 전략을 선택할 수 있고, 내비게이션은 선택된 전략에 따라 다른 경로를 안내합니다.

### 2. 등장 배경
- **조건문 복잡성**: if-else/switch가 많아지면 유지보수 어려움
- **알고리즘 변화**: 알고리즘이 자주 변경되거나 확장되는 경우
- **코드 중복**: 여러 클래스에서 동일한 알고리즘 선택 로직 중복

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 전략 패턴 구조 다이어그램

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        전략 패턴 구조                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                           Context                                    │   │
│   ├─────────────────────────────────────────────────────────────────────┤   │
│   │  - strategy: Strategy                                                │   │
│   │  + setStrategy(strategy: Strategy)                                   │   │
│   │  + executeStrategy()                                                 │   │
│   └──────────────────────────────┬──────────────────────────────────────┘   │
│                                  │ uses                                      │
│                                  ▼                                           │
│                  ┌───────────────────────────────┐                          │
│                  │     <<interface>>             │                          │
│                  │        Strategy               │                          │
│                  ├───────────────────────────────┤                          │
│                  │ + execute(): void             │                          │
│                  └───────────────┬───────────────┘                          │
│                                  │ implements                               │
│          ┌───────────────────────┼───────────────────────┐                  │
│          │                       │                       │                  │
│          ▼                       ▼                       ▼                  │
│   ┌────────────────┐     ┌────────────────┐     ┌────────────────┐          │
│   │ ConcreteStrategy│     │ConcreteStrategy│     │ConcreteStrategy│          │
│   │       A        │     │       B        │     │       C        │          │
│   ├────────────────┤     ├────────────────┤     ├────────────────┤          │
│   │ + execute()    │     │ + execute()    │     │ + execute()    │          │
│   │ // 알고리즘 A  │     │ // 알고리즘 B  │     │ // 알고리즘 C  │          │
│   └────────────────┘     └────────────────┘     └────────────────┘          │
│                                                                             │
│   [클라이언트 사용]                                                          │
│   context.setStrategy(ConcreteStrategyA())                                  │
│   context.executeStrategy()  // 알고리즘 A 실행                              │
│   context.setStrategy(ConcreteStrategyB())                                  │
│   context.executeStrategy()  // 알고리즘 B 실행                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 구현 예시: 결제 수단 선택

```kotlin
// Strategy 인터페이스
interface PaymentStrategy {
    fun pay(amount: Double): PaymentResult
}

// Concrete Strategies
class CreditCardStrategy(
    private val cardNumber: String,
    private val cvv: String
) : PaymentStrategy {
    override fun pay(amount: Double): PaymentResult {
        println("신용카드로 $$amount 결제")
        return PaymentResult(success = true, transactionId = "CC-${System.currentTimeMillis()}")
    }
}

class KakaoPayStrategy(
    private val accountId: String
) : PaymentStrategy {
    override fun pay(amount: Double): PaymentResult {
        println("카카오페이로 $$amount 결제")
        return PaymentResult(success = true, transactionId = "KP-${System.currentTimeMillis()}")
    }
}

class TossPayStrategy(
    private val phoneNumber: String
) : PaymentStrategy {
    override fun pay(amount: Double): PaymentResult {
        println("토스로 $$amount 결제")
        return PaymentResult(success = true, transactionId = "TP-${System.currentTimeMillis()}")
    }
}

// Context
class PaymentProcessor {
    private var strategy: PaymentStrategy? = null

    fun setStrategy(strategy: PaymentStrategy) {
        this.strategy = strategy
    }

    fun processPayment(amount: Double): PaymentResult {
        return strategy?.pay(amount)
            ?: throw IllegalStateException("결제 수단이 선택되지 않았습니다")
    }
}

// 클라이언트
fun main() {
    val processor = PaymentProcessor()

    // 신용카드 결제
    processor.setStrategy(CreditCardStrategy("1234-5678-9012-3456", "123"))
    processor.processPayment(100.0)

    // 카카오페이 결제
    processor.setStrategy(KakaoPayStrategy("user@kakao.com"))
    processor.processPayment(50.0)

    // 토스 결제
    processor.setStrategy(TossPayStrategy("010-1234-5678"))
    processor.processPayment(75.0)
}
```

### 3. if-else vs 전략 패턴 비교

```text
[if-else 사용 (Bad)]

fun processPayment(type: String, amount: Double) {
    if (type == "CARD") {
        // 신용카드 결제 로직
    } else if (type == "KAKAO") {
        // 카카오페이 결제 로직
    } else if (type == "TOSS") {
        // 토스 결제 로직
    } else if (type == "NAVER") {  // 새 결제수단 추가 시 수정 필요!
        // 네이버페이 결제 로직
    }
    // OCP 위반: 새로운 타입 추가 시 기존 코드 수정

[전략 패턴 사용 (Good)]

fun processPayment(strategy: PaymentStrategy, amount: Double) {
    strategy.pay(amount)
}
// 새 결제수단 추가 시 기존 코드 수정 없음
// NaverPayStrategy만 새로 구현하면 됨
// OCP 준수
```

### 4. 함수형 프로그래밍과의 연계

```kotlin
// Kotlin에서 함수 타입으로 전략 표현
typealias PaymentStrategy = (Double) -> PaymentResult

val creditCardStrategy: PaymentStrategy = { amount ->
    println("신용카드로 $$amount 결제")
    PaymentResult(success = true, transactionId = "CC-$amount")
}

val kakaoPayStrategy: PaymentStrategy = { amount ->
    println("카카오페이로 $$amount 결제")
    PaymentResult(success = true, transactionId = "KP-$amount")
}

fun processPayment(strategy: PaymentStrategy, amount: Double) {
    strategy(amount)
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (비교표 2개+)

### 1. 상태 패턴 vs 전략 패턴

| 구분 | 전략 패턴 | 상태 패턴 |
|:---:|:---|:---|
| **목적** | 알고리즘 교체 | 상태별 행위 변경 |
| **변경 주체** | 클라이언트가 직접 교체 | 객체 내부에서 자동 전이 |
| **의도** | "어떻게"를 변경 | "무엇을"을 변경 |
| **예시** | 정렬 알고리즘, 결제 수단 | 자판기 상태, 게임 캐릭터 |

### 2. 활용 사례

| 분야 | Context | Strategy |
|:---:|:---|:---|
| **정렬** | Collections.sort() | Comparator |
| **압축** | 압축 유틸리티 | ZIP, RAR, 7Z |
| **인증** | AuthManager | OAuth, JWT, Session |
| **라우팅** | Router | 최단경로, 최소시간 |

### 3. 장단점

| 장점 | 단점 |
|:---|:---|
| 조건문 제거 | 클래스 수 증가 |
| OCP 준수 | 클라이언트가 전략 선택 |
| 알고리즘 독립적 테스트 | 전략 선택 로직 노출 |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (800자+)

### 기술사적 판단

#### 시나리오: 배송비 계산
- **상황**: 무료 배송, 유료 배송, 새벽 배송, 해외 배송 등 다양한 배송비 정책
- **전략**: DeliveryFeeStrategy로 각 정책 구현
- **기술사적 판단**: 새로운 배송 정책(예: 드론 배송) 추가 시 기존 코드 수정 없음

### 도입 체크리스트
- [ ] 알고리즘이 런타임에 교체되어야 하는가?
- [ ] 알고리즘 변형이 자주 발생하는가?
- [ ] 복잡한 조건문을 제거해야 하는가?
- [ ] 알고리즘이 클라이언트로부터 숨겨져야 하는가?

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 구분 | 효과 |
|:---:|:---|
| **유지보수성** | 알고리즘 독립적 수정 |
| **확장성** | 새 전략 추가 용이 |
| **테스트** | 전략별 단위 테스트 |

### 참고 표준
- **GoF Design Patterns**: 전략 패턴 정의
- **Clean Code**: 조건문 대체 가이드

---

## 📌 관련 개념 맵
- [상태 패턴](./state_pattern.md): 상태 전이
- [팩토리 메서드](../03_gof_creational/factory_method_pattern.md): 전략 생성
- [OCP 원칙](../02_principles/solid_principles.md): 개방-폐쇄 원칙

---

## 👶 어린이를 위한 3줄 비유
1. 전략 패턴은 **게임에서 캐릭터의 무기를 바꾸는 것**과 같아요. 검, 활, 마법봉 중에서 상황에 따라 골라 쓸 수 있죠.
2. 캐릭터는 **어떤 무기든 똑같이 휘두르기만 하면 돼요.** 무기가 바뀌어도 캐릭터는 바뀌지 않아요.
3. 나중에 새로운 무기가 생겨도 **캐릭터를 고칠 필요 없이** 무기만 추가하면 돼요!
