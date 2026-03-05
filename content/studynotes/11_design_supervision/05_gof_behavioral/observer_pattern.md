+++
title = "옵저버 패턴 (Observer Pattern)"
categories = ["studynotes-11_design_supervision"]
+++

# 옵저버 패턴 (Observer Pattern)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 옵저버 패턴은 한 객체(Subject)의 상태가 변하면 그 객체에 의존하는 **다수의 옵저버들에게 자동으로 알림(Notify)**이 가도록 일대다(1:N) 의존성을 정의하는 행위 패턴입니다.
> 2. **가치**: 발행-구독(Pub/Sub) 구조를 통해 Subject와 Observer 간의 **느슨한 결합(Loose Coupling)**을 실현하며, 이는 MVC 아키텍처, 이벤트 드리븐 시스템, 리액티브 프로그래밍의 근간이 됩니다.
> 3. **융합**: RxJava/Reactor의 Observable, 스프링의 ApplicationEvent, Vue/React의 상태 관리, 그리고 마이크로서비스의 이벤트 버스에서 핵심적으로 활용됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 옵저버 패턴의 정의
옵저버(Observer) 패턴은 **"한 객체의 상태가 바뀌면 그 객체에 의존하는 다른 객체들에게 알림을 보내 자동으로 내용을 갱신"**하는 패턴입니다. 발행-구독(Publish-Subscribe) 모델이라고도 불리며, 객체 간의 1:N 의존 관계를 정의합니다.

### 💡 비유: 신문 구독 시스템
신문사(Subject)가 있고 구독자(Observer)들이 있습니다. 신문이 새로 나오면 신문사가 각 구독자에게 **직접 배달**하는 게 아니라, 구독자 명단을 보고 일괄 발송합니다. 구독자가 늘어도 신문사는 명단만 관리하면 됩니다.

### 2. 등장 배경
- **일대다 의존성**: 하나의 객체 변경이 여러 객체에 영향
- **실시간 갱신**: 상태 변화를 즉시 반영해야 하는 경우
- **느슨한 결합**: Subject가 Observer의 구체 타입을 알 필요 없음

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 옵저버 패턴 구조 다이어그램

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        옵저버 패턴 구조                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      Subject (Publisher)                            │   │
│   ├─────────────────────────────────────────────────────────────────────┤   │
│   │  - observers: List<Observer>                                        │   │
│   │  + attach(observer: Observer)                                       │   │
│   │  + detach(observer: Observer)                                       │   │
│   │  + notify()                                                         │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                    implements      │      notifies                          │
│                                    ▼                                        │
│   ┌────────────────┐    ┌────────────────┐    ┌────────────────┐           │
│   │ ConcreteSubject│    │   <<interface>> │    │   Observer     │           │
│   ├────────────────┤    │    Subject      │    │  (Subscriber)  │           │
│   │ - state        │    ├────────────────┤    ├────────────────┤           │
│   │ + getState()   │    │ + attach()     │    │ + update()     │           │
│   │ + setState()   │    │ + detach()     │    └───────┬────────┘           │
│   └───────┬────────┘    │ + notify()     │            │ implements         │
│           │             └────────────────┘            │                    │
│           │                                           │                    │
│           │ notifies        ┌─────────────────────────┼────────────┐       │
│           └────────────────►│           │             │            │       │
│                           ┌─▼───────┐ ┌──▼───────┐ ┌──▼───────┐           │
│                           │Observer1│ │Observer2 │ │Observer3 │           │
│                           ├─────────┤ ├──────────┤ ├──────────┤           │
│                           │+update()│ │+update() │ │+update() │           │
│                           └─────────┘ └──────────┘ └──────────┘           │
│                                                                             │
│   [동작 흐름]                                                                │
│   1. Client가 ConcreteSubject.setState() 호출                               │
│   2. ConcreteSubject가 notify() 호출                                        │
│   3. notify()가 등록된 모든 Observer의 update() 호출                          │
│   4. 각 Observer가 새 상태를 반영                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 핵심 구성 요소

| 구성 요소 | 역할 | 설명 |
|:---:|:---|:---|
| **Subject** | 인터페이스 | Observer 등록/제거/알림 메서드 선언 |
| **ConcreteSubject** | 구현체 | 상태 저장, 상태 변경 시 Observer 알림 |
| **Observer** | 인터페이스 | update 메서드 선언 |
| **ConcreteObserver** | 구현체 | Subject의 상태 변화에 반응 |

### 3. 구현 예시: 주식 시세 알림

```kotlin
// Observer 인터페이스
interface StockObserver {
    fun update(stockName: String, price: Double)
}

// Subject 인터페이스
interface StockSubject {
    fun attach(observer: StockObserver)
    fun detach(observer: StockObserver)
    fun notifyObservers()
}

// ConcreteSubject
class StockMarket : StockSubject {
    private val observers = mutableListOf<StockObserver>()
    private val stockPrices = mutableMapOf<String, Double>()

    override fun attach(observer: StockObserver) {
        observers.add(observer)
    }

    override fun detach(observer: StockObserver) {
        observers.remove(observer)
    }

    fun setStockPrice(stockName: String, price: Double) {
        stockPrices[stockName] = price
        notifyObservers()
    }

    override fun notifyObservers() {
        stockPrices.forEach { (stock, price) ->
            observers.forEach { it.update(stock, price) }
        }
    }
}

// ConcreteObservers
class MobileAppObserver(private val userId: String) : StockObserver {
    override fun update(stockName: String, price: Double) {
        println("[Mobile-$userId] $stockName 가격: $price")
    }
}

class TradingBotObserver : StockObserver {
    override fun update(stockName: String, price: Double) {
        if (price > 1000.0) {
            println("[Bot] $stockName 매도 신호!")
        }
    }
}

// 사용
fun main() {
    val market = StockMarket()
    market.attach(MobileAppObserver("user1"))
    market.attach(TradingBotObserver())

    market.setStockPrice("AAPL", 150.0)  // 모든 Observer에게 알림
    market.setStockPrice("TSLA", 1200.0) // Bot이 매도 신호
}
```

### 4. Push vs Pull 모델

```text
[Push 모델]
Subject ──► Observer.update(data)
           상태 데이터를 직접 전달

장점: Observer가 필요한 데이터 즉시 확보
단점: 불필요한 데이터도 전달될 수 있음

[Pull 모델]
Subject ──► Observer.update()
Observer ◄── Subject.getState()
           Observer가 필요할 때 데이터 요청

장점: Observer가 필요한 데이터만 가져옴
단점: Observer가 Subject를 알아야 함 (결합도 증가)
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (비교표 2개+)

### 1. 옵저버 패턴 변형 비교

| 구분 | Classic Observer | Pub/Sub (메시지 브로커) | Rx Reactive |
|:---:|:---|:---|:---|
| **연결** | 직접 | 브로커 경유 | 스트림 |
| **동기/비동기** | 동기 | 비동기 | 모두 지원 |
| **필터링** | 없음 | Topic 기반 | Operator |
| **백프레셔** | 없음 | 큐 | 지원 |
| **복잡도** | 낮음 | 중간 | 높음 |

### 2. 활용 사례

| 분야 | 예시 | Subject | Observer |
|:---:|:---|:---|:---|
| **MVC** | Model 변경 | Model | View |
| **GUI** | 버튼 클릭 | Button | ActionListener |
| **Reactive** | 데이터 스트림 | Observable | Subscriber |
| **Spring** | 이벤트 | ApplicationEventPublisher | @EventListener |

### 3. 장단점

| 장점 | 단점 |
|:---|:---|
| Subject-Observer 느슨한 결합 | 무한 루프 위험 (상호 옵저버) |
| 런타임 Observer 추가/제거 | 순서 보장 어려움 |
| OCP 준수 | 메모리 누수 (해제 안 된 Observer) |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (800자+)

### 기술사적 판단 (실무 시나리오)

#### 시나리오 1: 실시간 주문 알림 시스템
- **상황**: 주문 발생 시 관리자, 창고, 고객에게 각각 다른 알림
- **전략**: 주문 서비스를 Subject로 하고 각 알림 채널을 Observer로 구현
- **기술사적 판단**: 새로운 알림 채널(SMS, 푸시) 추가 시 기존 코드 수정 없음

#### 시나리오 2: MSA 이벤트 드리븐 아키텍처
- **상황**: 서비스 간 느슨한 결합 필요
- **전략**: 메시지 브로커(Kafka)를 통한 Pub/Sub 패턴
- **기술사적 판단**: 서비스 장애 격리, 확장성 확보

### 도입 체크리스트
- [ ] 일대다 의존 관계인가?
- [ ] 상태 변경 알림이 필요한가?
- [ ] Observer가 동적으로 변하는가?
- [ ] Subject와 Observer를 분리해야 하는가?

---

## Ⅴ. 기대효과 및 결론 (400자+)

### 기대효과

| 구분 | 효과 |
|:---:|:---|
| **확장성** | 새로운 Observer 추가 용이 |
| **결합도** | Subject-Observer 분리 |
| **유연성** | 런타임 구독 관리 |

### 미래 전망
1. **Reactive Streams**: 배압(Backpressure) 지원 확장
2. **Server-Sent Events**: 웹 실시간 알림
3. **GraphQL Subscription**: 실시간 데이터 구독

### 참고 표준
- **GoF Design Patterns**: 옵저버 패턴 정의
- **ReactiveX**: Reactive Extensions 표준

---

## 📌 관련 개념 맵
- [발행-구독 패턴](./pub_sub_pattern.md): 메시지 브로커 기반 확장
- [MVC 패턴](../02_principles/mvc_pattern.md): Model-View 연결
- [이벤트 드리븐 아키텍처](../02_principles/eda_architecture.md): 비동기 이벤트 처리
- [중재자 패턴](./mediator_pattern.md): 복잡한 통신 중앙화

---

## 👶 어린이를 위한 3줄 비유
1. 옵저버 패턴은 **유치원 선생님이 반 친구들에게 방송하는 것**과 같아요. "점심 시간이에요!"라고 말하면 모든 친구가 알게 되죠.
2. 선생님은 각 친구에게 따로 말하지 않아도 돼요. **한 번 말하면 모두가 들어요.** 새로운 친구가 와도 목록에만 추가하면 돼요.
3. 프로그램에서도 어떤 일이 생기면 **여러 곳에 한 번에 알려줄 때** 옵저버 패턴을 써요!
