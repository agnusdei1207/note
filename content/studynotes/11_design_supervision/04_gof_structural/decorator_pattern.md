+++
title = "데코레이터 패턴 (Decorator Pattern)"
categories = ["studynotes-11_design_supervision"]
+++

# 데코레이터 패턴 (Decorator Pattern)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데코레이터 패턴은 객체에 **동적으로 새로운 기능과 책임을 추가**할 수 있게 하는 구조 패턴으로, 상속 대신 합성을 사용하여 런타임에 유연하게 확장합니다.
> 2. **가치**: 단일 책임 원칙(SRP)과 개방-폐쇄 원칙(OCP)을 실현하며, Java I/O Stream, Python 데코레이터 등 언어 차원에서도 광범위하게 활용됩니다.
> 3. **융합**: 스프링의 빈 후처리기(BeanPostProcessor), HTTP 요청/응답 래핑, 그리고 AOP(Aspect-Oriented Programming)의 기반이 됩니다.

---

## Ⅰ. 개요

### 1. 정의
객체에 동적으로 책임을 추가하여 기능을 확장하는 패턴. 서브클래싱보다 유연한 확장 방법 제공.

### 💡 비유: 커피 주문
아메리카노(기본)에 샷 추가 → 샷 추가된 아메리카노, 여기에 시럽 추가 → 샷+시럽 아메리카노. **감싸서 기능 추가**.

---

## Ⅱ. 구조

```
┌─────────────────────────────────────────────────────────────────┐
│                   Component (인터페이스)                         │
│                       + operation()                             │
└─────────────────────────┬───────────────────────────────────────┘
                          │
           ┌──────────────┴──────────────┐
           │                             │
  ┌────────▼────────┐          ┌─────────▼─────────┐
  │ ConcreteComponent│          │    Decorator      │
  │   (기본 객체)    │          │  - component: Comp │
  │  + operation()  │          │  + operation()    │
  └─────────────────┘          └─────────┬─────────┘
                                         │
                              ┌──────────┴──────────┐
                              │                     │
                    ┌─────────▼─────────┐ ┌───────▼────────┐
                    │ ConcreteDecoratorA│ │ConcreteDecoratorB│
                    │  + operation()    │ │  + operation()  │
                    │  + addedBehavior()│ │  + addedBehavior│
                    └───────────────────┘ └─────────────────┘
```

---

## Ⅲ. 예시

### Java I/O

```java
InputStream is = new FileInputStream("file.txt");
InputStream bis = new BufferedInputStream(is);
InputStream dis = new DataInputStream(bis);
// 데코레이터 체인: FileInputStream → Buffered → Data
```

### 커피 예시

```kotlin
interface Coffee { fun cost(): Double; fun description(): String }

class Americano : Coffee {
    override fun cost() = 3000.0
    override fun description() = "아메리카노"
}

class ShotDecorator(private val coffee: Coffee) : Coffee {
    override fun cost() = coffee.cost() + 500
    override fun description() = "${coffee.description()} + 샷"
}

// 사용
val coffee: Coffee = ShotDecorator(ShotDecorator(Americano()))
// 아메리카노 + 샷 + 샷 = 4000원
```

---

## Ⅳ. 비교

| 구분 | 상속 | 데코레이터 |
|:---:|:---|:---|
| **확장 시점** | 컴파일 | 런타임 |
| **유연성** | 낮음 | 높음 |
| **클래스 수** | 폭증 | 중간 |

---

## 📌 관련 개념
- [프록시 패턴](./proxy_pattern.md): 접근 제어
- [어댑터 패턴](./adapter_pattern.md): 인터페이스 변환
- [합성 vs 상속](../02_principles/composition_over_inheritance.md)

---

## 👶 어린이를 위한 비유
데코레이터는 **선물에 예쁜 포장지를 하나씩 감싸는 것**과 같아요. 상자(기본) → 종이 포장 → 리본 → 카드. **감쌀수록 예뻐져요!**
