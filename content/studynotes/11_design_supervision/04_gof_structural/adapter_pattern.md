+++
title = "어댑터 패턴 (Adapter Pattern)"
categories = ["studynotes-11_design_supervision"]
+++

# 어댑터 패턴 (Adapter Pattern)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 어댑터 패턴은 **호환되지 않는 인터페이스**를 가진 두 클래스를 연결하기 위해, 클라이언트가 요구하는 인터페이스로 **래핑(Wrapping)**하여 함께 동작할 수 있도록 변환하는 구조 패턴입니다.
> 2. **가치**: 기존 코드를 수정하지 않고(수정 폐쇄) 새로운 인터페이스에 맞게 재사용(확장 개방)할 수 있어, 레거시 시스템 통합, 외부 라이브러리 활용, API 버전 관리에 필수적입니다.
> 3. **융합**: 스프링 MVC의 HandlerAdapter, JPA의 Dialect, 그리고 MSA의 API 게이트웨이에서 광범위하게 활용됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 어댑터 패턴의 정의
어댑터(Adapter) 패턴은 **"클래스의 인터페이스를 클라이언트가 기대하는 다른 인터페이스로 변환"**하는 패턴입니다. 호환되지 않는 인터페이스 때문에 함께 작동할 수 없는 클래스들이 함께 작동할 수 있게 합니다. 별명으로 **래퍼(Wrapper) 패턴**이라고도 불립니다.

### 💡 비유: 해외 여행용 플러그 어댑터
한국에서 만든 전자기기를 유럽에서 사용하려면 플러그 모양이 달라서 직접 꽂을 수 없습니다. 이때 **플러그 어댑터**를 사용하면 한국 플러그를 유럽 소켓에 맞게 변환해줍니다. 어댑터 패턴도 이처럼 서로 다른 인터페이스를 연결해줍니다.

### 2. 등장 배경
- **레거시 통합**: 기존 시스템을 새로운 시스템에 통합
- **외부 라이브러리**: 제3자 라이브러리를 내부 인터페이스에 맞춤
- **인터페이스 불일치**: 클라이언트가 요구하는 인터페이스와 실제 구현이 다른 경우

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 어댑터 패턴 구조 다이어그램

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        어댑터 패턴 구조                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [객체 어댑터 (Object Adapter) - 합성 사용]                                  │
│                                                                             │
│   ┌────────────────┐          ┌────────────────┐                           │
│   │    Client      │          │    Target      │                           │
│   │                │          │  <<interface>> │                           │
│   ├────────────────┤          ├────────────────┤                           │
│   │                │ uses     │ + request()    │                           │
│   │                │─────────►│                │                           │
│   └────────────────┘          └───────┬────────┘                           │
│                                       │ implements                          │
│                                       ▼                                     │
│   ┌────────────────┐          ┌────────────────┐                           │
│   │    Adaptee     │          │    Adapter     │                           │
│   │  (기존 클래스)  │          │                │                           │
│   ├────────────────┤          ├────────────────┤                           │
│   │+ specificRequest()│◄──────│- adaptee: Adaptee│                          │
│   │                │  위임     │+ request()     │                           │
│   └────────────────┘          └────────────────┘                           │
│                                                                             │
│   [호출 흐름]                                                                │
│   Client ──► Target.request() ──► Adapter.request()                        │
│                                     │                                       │
│                                     └──► adaptee.specificRequest()          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 객체 어댑터 vs 클래스 어댑터

| 구분 | 객체 어댑터 | 클래스 어댑터 |
|:---:|:---|:---|
| **구현 방식** | 합성(Composition) | 상속(Inheritance) |
| **유연성** | 높음 (런타임 교체 가능) | 낮음 (컴파일 타임 고정) |
| **다중 상속** | 필요 없음 | 필요 (다중 상속 지원 언어만) |
| **적용 범위** | Adaptee 서브클래스도 적용 가능 | Adaptee 서브클래스 적용 어려움 |
| **추천도** | **높음** | 낮음 (다중 상속 지원 시만) |

### 3. 구현 예시: 결제 게이트웨이 어댑터

```kotlin
// Target: 클라이언트가 기대하는 인터페이스
interface PaymentProcessor {
    fun pay(amount: Double): PaymentResult
}

// Adaptee: 외부 결제 라이브러리 (수정 불가)
class TossPaymentClient {
    fun executePayment(price: Int, currency: String): TossResponse {
        // 실제 토스 결제 로직
        return TossResponse(success = true, transactionId = "TOSS-123")
    }
}

class KakaoPayClient {
    fun sendMoney(krw: Long): KakaoResult {
        // 실제 카카오페이 로직
        return KakaoResult(status = "SUCCESS", orderId = "KAKAO-456")
    }
}

// Adapter: Toss용 어댑터
class TossPaymentAdapter(private val tossClient: TossPaymentClient) : PaymentProcessor {
    override fun pay(amount: Double): PaymentResult {
        val response = tossClient.executePayment(amount.toInt(), "KRW")
        return PaymentResult(
            success = response.success,
            transactionId = response.transactionId
        )
    }
}

// Adapter: Kakao용 어댑터
class KakaoPayAdapter(private val kakaoClient: KakaoPayClient) : PaymentProcessor {
    override fun pay(amount: Double): PaymentResult {
        val result = kakaoClient.sendMoney(amount.toLong())
        return PaymentResult(
            success = result.status == "SUCCESS",
            transactionId = result.orderId
        )
    }
}

// 클라이언트
class PaymentService(private val processor: PaymentProcessor) {
    fun processOrder(amount: Double) {
        val result = processor.pay(amount)
        if (result.success) {
            println("결제 성공: ${result.transactionId}")
        }
    }
}
```

### 4. 양방향 어댑터 (Two-Way Adapter)

```text
┌─────────────────────────────────────────────────────────────────┐
│                    양방향 어댑터 구조                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌────────────┐         ┌────────────┐                        │
│   │  TargetA   │         │  TargetB   │                        │
│   │ +operationA│         │ +operationB│                        │
│   └─────┬──────┘         └─────┬──────┘                        │
│         │                      │                                │
│         └──────────┬───────────┘                                │
│                    │                                            │
│                    ▼                                            │
│         ┌─────────────────────┐                                │
│         │  TwoWayAdapter      │                                │
│         ├─────────────────────┤                                │
│         │ +operationA()       │ ◄── TargetA 인터페이스 구현     │
│         │ +operationB()       │ ◄── TargetB 인터페이스 구현     │
│         └─────────────────────┘                                │
│                                                                 │
│   양쪽 인터페이스 모두 지원하여 어느 쪽에서든 사용 가능              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (비교표 2개+)

### 1. 어댑터 vs 퍼사드 vs 데코레이터

| 패턴 | 목적 | 인터페이스 변경 | 구조 |
|:---:|:---|:---:|:---|
| **어댑터** | 인터페이스 호환 | O (변환) | 합성/상속 |
| **퍼사드** | 복잡성 단순화 | O (단순화) | 합성 |
| **데코레이터** | 기능 추가 | X (동일) | 합성 |
| **프록시** | 접근 제어 | X (동일) | 합성 |

### 2. 활용 사례

| 분야 | 예시 | Target | Adaptee |
|:---:|:---|:---|:---|
| **Spring MVC** | HandlerAdapter | ModelAndView handle() | Controller |
| **JPA** | Dialect | JPA 표준 인터페이스 | Oracle, MySQL 드라이버 |
| **Collections** | Arrays.asList() | List 인터페이스 | 배열 |
| **I/O** | InputStreamReader | Reader | InputStream |

### 3. 장단점

| 장점 | 단점 |
|:---|:---|
| 기존 코드 수정 없이 재사용 | 복잡도 증가 |
| 단일 책임 원칙 준수 | 다수의 클래스 생성 |
| 개방-폐쇄 원칙 준수 | - |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (800자+)

### 기술사적 판단 (실무 시나리오)

#### 시나리오 1: 레거시 시스템 통합
- **상황**: 기존 ERP 시스템과 새로운 웹 서비스 연동
- **전략**: ERP API를 내부 인터페이스에 맞는 어댑터 구현
- **기술사적 판단**: 레거시 수정 없이 통합, 향후 ERP 교체 시 어댑터만 교체

#### 시나리오 2: 외부 API 버전 관리
- **상황**: 결제 API v1에서 v2로 마이그레이션
- **전략**: v2 어댑터 구현 후 점진적 교체
- **기술사적 판단**: 클라이언트 코드 수정 없이 백엔드만 교체

### 도입 체크리스트
- [ ] 기존 인터페이스를 수정할 수 없는가?
- [ ] 새로운 인터페이스가 필요한가?
- [ ] 런타임에 구현체를 교체해야 하는가?
- [ ] 다중 상속이 필요하지 않은가? (객체 어댑터 권장)

---

## Ⅴ. 기대효과 및 결론 (400자+)

### 기대효과

| 구분 | 효과 |
|:---:|:---|
| **재사용성** | 기존 코드 수정 없이 새 환경에서 활용 |
| **유연성** | 런타임에 구현체 교체 가능 |
| **결합도** | 클라이언트와 구현체 분리 |

### 참고 표준
- **GoF Design Patterns**: 어댑터 패턴 정의
- **Java I/O Streams**: 어댑터 패턴 활용 예

---

## 📌 관련 개념 맵
- [퍼사드 패턴](./facade_pattern.md): 복잡성 단순화
- [데코레이터 패턴](./decorator_pattern.md): 기능 추가
- [브리지 패턴](./bridge_pattern.md): 구현 분리
- [프록시 패턴](./proxy_pattern.md): 접근 제어

---

## 👶 어린이를 위한 3줄 비유
1. 어댑터 패턴은 **여행 가서 쓰는 플러그 변환기**와 같아요. 한국 충전기를 유럽에서 쓰려면 모양을 바꿔주는 게 필요하죠.
2. 충전기를 뜯어서 고치는 게 아니라, **중간에 변환기를 끼워서** 맞추는 거예요. 이렇게 하면 충전기는 그대로고 변환기만 바꾸면 돼요.
3. 프로그램에서도 이렇게 **서로 다른 것들을 연결**해줄 때 어댑터를 써요!
