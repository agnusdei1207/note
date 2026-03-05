+++
title = "빌더 패턴 (Builder Pattern)"
categories = ["studynotes-11_design_supervision"]
+++

# 빌더 패턴 (Builder Pattern)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 빌더 패턴은 **복잡한 객체의 생성 과정(초기화)과 표현 방법을 분리**하여, 동일한 생성 프로세스로 다양한 구성의 객체를 단계별로 유연하게 생성하는 패턴입니다.
> 2. **가치**: 파라미터가 많은 생성자(Telescoping Constructor) 문제를 해결하고, 메서드 체이닝(Method Chaining)을 통해 가독성 높은 객체 생성 코드를 작성할 수 있습니다.
> 3. **융합**: Lombok의 @Builder, StringBuilder, ImmutableList.builder(), 그리고 JPA의 CriteriaBuilder 등 Java/Kotlin 생태계 전반에서 광범위하게 활용됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 빌더 패턴의 정의
빌더(Builder) 패턴은 **"복잡한 객체의 생성과 표현을 분리하여, 동일한 생성 과정으로 서로 다른 표현을 생성"**하는 패턴입니다. 클라이언트는 복잡한 내부 구조를 알 필요 없이 단계적으로 객체를 조립할 수 있습니다.

### 💡 비유: 햄버거 세트 주문
패스트푸드점에서 햄버거 세트를 주문할 때, "버거는 어떤 걸로요? 음료는요? 사이드는요?"라고 하나씩 물어봅니다. 손님은 **원하는 것만 선택**하면 되고, 점원은 선택한 것들을 조립해서 세트를 완성합니다. 빌더 패턴도 이처럼 단계별로 객체를 조립합니다.

### 2. 등장 배경
- **복잡한 생성자**: 파라미터가 많아져서 가독성 저하
- **선택적 파라미터**: 일부만 필요한 경우 처리 어려움
- **불변 객체**: 생성 후 수정 불가능한 객체 생성

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 빌더 패턴 구조 다이어그램

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        빌더 패턴 구조                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────┐         ┌─────────────────────┐                  │
│   │     <<interface>>    │         │       Product       │                  │
│   │       Builder        │         │   (복잡한 객체)      │                  │
│   ├─────────────────────┤         ├─────────────────────┤                  │
│   │ + buildPartA()      │────────►│ - partA             │                  │
│   │ + buildPartB()      │         │ - partB             │                  │
│   │ + buildPartC()      │         │ - partC             │                  │
│   │ + getResult():Product│         │ + operation()       │                  │
│   └──────────┬──────────┘         └─────────────────────┘                  │
│              │ implements                                                    │
│     ┌────────┴────────┐                                                     │
│     │                 │                                                     │
│  ┌──▼────────────┐ ┌──▼────────────┐                                       │
│  │ConcreteBuilder│ │ConcreteBuilder│                                       │
│  │       1       │ │       2       │                                       │
│  ├───────────────┤ ├───────────────┤                                       │
│  │- product:Prod │ │- product:Prod │                                       │
│  │+buildPartA()  │ │+buildPartA()  │                                       │
│  │+buildPartB()  │ │+buildPartB()  │                                       │
│  │+getResult()   │ │+getResult()   │                                       │
│  └───────────────┘ └───────────────┘                                       │
│                                                                             │
│   ┌─────────────────────┐                                                  │
│   │      Director       │ (Optional)                                       │
│   ├─────────────────────┤                                                  │
│   │ - builder: Builder  │                                                  │
│   │ + construct()       │                                                  │
│   └─────────────────────┘                                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 문제 상황: Telescoping Constructor

```kotlin
// Bad: 파라미터가 많은 생성자
class User(
    val name: String,
    val age: Int,
    val email: String?,
    val phone: String?,
    val address: String?,
    val company: String?,
    val jobTitle: String?
)

// 사용 시 가독성 저하
val user = User(
    "홍길동",
    30,
    "hong@example.com",
    null,  // phone은 필요 없음
    "서울시 강남구",
    null,  // company는 필요 없음
    "개발자"
)
```

### 3. 빌더 패턴 적용

```kotlin
// Good: 빌더 패턴
class User private constructor(
    val name: String,
    val age: Int,
    val email: String?,
    val phone: String?,
    val address: String?,
    val company: String?,
    val jobTitle: String?
) {
    class Builder {
        private var name: String = ""
        private var age: Int = 0
        private var email: String? = null
        private var phone: String? = null
        private var address: String? = null
        private var company: String? = null
        private var jobTitle: String? = null

        fun name(name: String) = apply { this.name = name }
        fun age(age: Int) = apply { this.age = age }
        fun email(email: String?) = apply { this.email = email }
        fun phone(phone: String?) = apply { this.phone = phone }
        fun address(address: String?) = apply { this.address = address }
        fun company(company: String?) = apply { this.company = company }
        fun jobTitle(jobTitle: String?) = apply { this.jobTitle = jobTitle }

        fun build() = User(name, age, email, phone, address, company, jobTitle)
    }

    companion object {
        fun builder() = Builder()
    }
}

// 사용 (Method Chaining)
val user = User.builder()
    .name("홍길동")
    .age(30)
    .email("hong@example.com")
    .address("서울시 강남구")
    .jobTitle("개발자")
    .build()  // phone, company는 생략 가능
```

### 4. Kotlin 데이터 클래스 활용

```kotlin
// Kotlin에서는 data class와 기본값으로 더 간단히
data class User(
    val name: String,
    val age: Int = 0,
    val email: String? = null,
    val phone: String? = null,
    val address: String? = null,
    val company: String? = null,
    val jobTitle: String? = null
)

// 사용
val user = User(
    name = "홍길동",
    age = 30,
    email = "hong@example.com",
    address = "서울시 강남구",
    jobTitle = "개발자"
)
```

### 5. Lombok @Builder (Java)

```java
@Builder
public class User {
    private String name;
    private int age;
    private String email;
    private String phone;
    private String address;
    private String company;
    private String jobTitle;
}

// 사용
User user = User.builder()
    .name("홍길동")
    .age(30)
    .email("hong@example.com")
    .build();
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (비교표 2개+)

### 1. 생성 패턴 비교

| 패턴 | 용도 | 생성 방식 | 복잡도 |
|:---:|:---|:---|:---:|
| **빌더** | 복잡한 객체 단계적 생성 | 조립 | 높음 |
| **팩토리 메서드** | 단일 객체 생성 | 서브클래스 | 중간 |
| **추상 팩토리** | 연관 객체군 생성 | 팩토리 조합 | 높음 |
| **프로토타입** | 복제를 통한 생성 | clone | 낮음 |

### 2. 활용 사례

| 라이브러리 | 클래스 | 용도 |
|:---:|:---|:---|
| **Java** | StringBuilder | 문자열 조립 |
| **Guava** | ImmutableList.builder() | 불변 리스트 생성 |
| **Lombok** | @Builder | 객체 생성 자동화 |
| **JPA** | CriteriaBuilder | 쿼리 조립 |
| **OkHttp** | Request.Builder | HTTP 요청 생성 |

### 3. 장단점

| 장점 | 단점 |
|:---|:---|
| 가독성 향상 | 클래스 수 증가 |
| 선택적 파라미터 | 코드량 증가 |
| 불변 객체 생성 | - |
| 단계적 검증 | - |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (800자+)

### 기술사적 판단

#### 시나리오: HTTP 요청 객체 생성
- **상황**: 복잡한 API 요청 객체 (필수/선택 필드 혼재)
- **전략**: 빌더 패턴으로 필수 필드 검증 및 선택 필드 유연 처리
- **기술사적 판단**: 필수 필드는 Builder 생성자에서, 선택 필드는 메서드로

### 도입 체크리스트
- [ ] 생성자 파라미터가 4개 이상인가?
- [ ] 선택적 파라미터가 많은가?
- [ ] 불변 객체가 필요한가?
- [ ] 생성 로직이 복잡한가?

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 구분 | 효과 |
|:---:|:---|
| **가독성** | 명확한 필드명으로 생성 |
| **유연성** | 선택적 필드 자유로운 생략 |
| **불변성** | 생성 후 수정 불가 |

### 참고 표준
- **GoF Design Patterns**: 빌더 패턴
- **Effective Java**: 빌더 패턴 권장

---

## 📌 관련 개념 맵
- [팩토리 메서드](./factory_method_pattern.md): 단일 객체 생성
- [불변 객체](../05_gof_behavioral/immutable_object.md): Immutable Object
- [메서드 체이닝](../02_principles/method_chaining.md): Fluent Interface

---

## 👶 어린이를 위한 3줄 비유
1. 빌더 패턴은 **레고를 조립하는 것**과 같아요. 한 번에 다 만드는 게 아니라, 하나씩 차곡차곡 쌓아서 완성해요.
2. "이걸 붙이고, 저걸 붙이고, 이제 다 됐어!"라고 **단계별로 만들 수 있어요.** 원하는 것만 붙일 수도 있죠.
3. 이렇게 하면 **복잡한 것도 쉽게 만들 수 있어서** 훨씬 편해요!
