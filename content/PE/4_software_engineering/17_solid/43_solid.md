+++
title = "43. SOLID 원칙 (SOLID Principles)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["SOLID", "OOP", "Design-Principles", "Clean-Architecture", "Dependency-Inversion"]
draft = false
+++

# SOLID 원칙 (SOLID Principles)

## 핵심 인사이트 (3줄 요약)
> 1. **S**RP (Single Responsibility): **"클래스**는 **하나의 **책임**만 **가져야 **한다**"는 **원칙**으로, **여러 **이유**로 **변경**되지 **않도록 **분리**하고 **테스트**와 **유지보수**를 **용이**하게 **만든다.
> 2. **O**CP (Open/Closed): **"개방 **폐쇄", **수정 **폐쇄**"**로 **확장**을 **위해 **열리고 **수정**에는 **닫혀**있어야 **하며**추상화**(Abstraction)와 **다형성**(Polymorphism)**으로 **새로운 **기능**을 **추가**한다.
> 3. **L**SP (Liskov Substitution): **"자식 **클래스**는 **부모 **클래스**로 **대체**가능**해야 **한다**"**는 **원칙**으로, **상속**관계에서 **IS-A** 관계를 **유지**하고 **계약**(Contract)을 **준수**하며 **리스코프**를 **위배**하지 **않는다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 이커머스 플랫폼 리팩토링
**상황**: 단일 클래스 5000줄
**판단**: SOLID 원칙 적용

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                         Refactoring to SOLID Principles                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Before (God Class):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  class ECommerceService:                                                                     │  │
    │      def __init__(self):                                                                  │  │
    │          self.db = DatabaseConnection()                                                    │  │
    │          self.smtp = EmailServer()                                                         │  │
    │          self.logger = Logger()                                                            │  │
    │          self.cache = RedisCache()                                                        │  │
    │                                                                                             │  │
    │      def create_order(self, user_id, items):                                                   │  │
    │          # Validate user                                                                      │  │
    │          # Check inventory                                                                  │  │
    │          # Calculate pricing                                                                │  │
    │          # Save order                                                                       │  │
    │          # Send email                                                                       │  │
    │          # Update cache                                                                     │  │
    │          # Log transaction                                                                  │  │
    │          # ... 5000 lines                                                                 │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    After (SRP + OCP + DIP + ISP + LSP):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # SRP: Separate concerns                                                                     │  │
    │  class OrderService:                                                                      │  │
    │      def __init__(self, db: Database, repository: OrderRepository,                     │  │
    │                   notifier: Notifier):                                                   │  │
    │          self.db = db                                                                      │  │
    │          self.repository = repository                                                    │  │
    │          self.notifier = notifier                                                          │  │
    │                                                                                             │  │
    │      def create_order(self, user_id: str, items: List[OrderItem]) -> Order:             │  │
    │          order = self.repository.create(user_id, items)                                 │  │
    │          self.notifier.send_order_confirmation(order)                                     │  │  │
    │          return order                                                                        │  │
    │                                                                                             │  │
    │  # OCP: Abstraction for payment methods                                                     │  │
    │  class PaymentProcessor(ABC):                                                             │  │
    │      @abstractmethod                                                                     │  │
    │      def process(self, amount: Decimal) -> bool:                                          │  │
    │                                                                                             │  │
    │  class CreditCardProcessor(PaymentProcessor):                                            │  │
    │      def process(self, amount: Decimal) -> bool:                                          │  │
    │          # Credit card logic                                                                │  │
    │                                                                                             │  │
    │  class PayPalProcessor(PaymentProcessor):                                                │  │
    │      def process(self, amount: Decimal) -> bool:                                            │  │
    │          # PayPal logic                                                                    │  │
    │                                                                                             │  │
    │  # DIP: Depend on abstractions, not concretions                                       │  │
    │  def checkout(payment_processor: PaymentProcessor):                                   │  │
    │      if payment_processor.process(order.total):                                           │  │
    │          order.status = "paid"                                                          │  │
    │                                                                                             │  │
    │  # ISP: Many small interfaces                                                           │  │
    │  class OrderRepository:                                                                  │  │
    │      def create(self, user_id: str, items: List[OrderItem]) -> Order:                      │  │
    │      def find_by_id(self, order_id: str) -> Optional[Order]:                               │  │
    │      def update_status(self, order_id: str, status: str):                               │  │
    │                                                                                             │  │
    │  # LSP: Square -> Rectangle is valid                                                │  │
    │  class Square(Rectangle):                                                                 │  │
    │      def area(self) -> float: return self.width * self.height                                 │  │
    │                                                                                             │  │
    │  # DIP: High-level modules depend on low-level modules                                       │  │
    │  OrderService → OrderRepository → Database                                             │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### SOLID 적용 효과

| 원칙 | 적용 전 | 적용 후 |
|------|--------|--------|
| **유지보수** | 어려움 | 쉬움 |
| **확장성** | 깨짐 | 쉬움 |
| **테스트** | 어려움 | 쉬움 |
| **이해도** | 낮음 | 높음 |

### 모범 사례

1. **SRP**: 1 클래스 = 1 책임
2. **OCP**: 인터페이스 의존
3. **LSP**: 리스코프 방지
4. **DIP**: DI 사용
5. **ISP**: 작은 인터페이스

### 미래 전망

1. **SOLID+**: Functional SOLID
2. **Clean Arch**: 헥사걸탈
3. **DDD**: 도메인 주도 설계
4. **Microservices**: SOLID 적용

### ※ 참고 표준/가이드
- **Uncle Bob**: Clean Code
- **Martin**: Clean Architecture
- **Martin**: Agile Principles

---

## 📌 관련 개념 맵

- [디자인 패턴](./14_design_patterns/40_design_patterns.md) - 구체화
- [리팩토링](./16_refactoring/42_refactoring.md) - 개선
- [아키텍처](./4_architecture/15_enterprise_architecture.md) - 적용
