+++
title = "MVC 패턴 (Model-View-Controller)"
categories = ["studynotes-11_design_supervision"]
+++

# MVC 패턴 (Model-View-Controller)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MVC는 애플리케이션을 **Model(데이터/비즈니스 로직), View(사용자 인터페이스), Controller(입력 처리/흐름 제어)**로 분리하여 관심사를 분리(SoC)하는 아키텍처 패턴입니다.
> 2. **가치**: 각 컴포넌트의 독립적인 개발, 테스트, 수정이 가능하며, 옵저버, 전략, 컴포지트 패턴의 복합체로 GoF 패턴의 실제 응용 사례입니다.
> 3. **융합**: Spring MVC, ASP.NET MVC 등 웹 프레임워크의 표준 아키텍처이며, MVP, MVVM 등 다양한 변형의 기반이 됩니다.

---

## Ⅰ. 개요

### 1. MVC 구성요소

| 구성요소 | 역할 | 책임 |
|:---:|:---|:---|
| **Model** | 데이터, 비즈니스 로직 | 상태 관리, 데이터 처리 |
| **View** | 사용자 인터페이스 | 화면 렌더링 |
| **Controller** | 입력 처리, 흐름 제어 | Model/View 중재 |

### 💡 비유: 레스토랑 운영
- **Model**: 주방(재료, 요리법)
- **View**: 메뉴판, 테이블 세팅
- **Controller**: 웨이터(주문 받아서 주방에 전달)

---

## Ⅱ. 구조

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MVC 패턴 구조                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                         ┌──────────────┐                                    │
│                         │    View      │                                    │
│                         │   (사용자    │                                    │
│                         │    인터페이스)│                                    │
│                         └──────┬───────┘                                    │
│                                │ 사용자 입력                                 │
│                                ▼                                             │
│                         ┌──────────────┐                                    │
│                         │  Controller  │                                    │
│                         │  (흐름 제어)  │                                    │
│                         └──────┬───────┘                                    │
│                                │                                            │
│              ┌─────────────────┼─────────────────┐                          │
│              │                 │                 │                          │
│              ▼                 │                 ▼                          │
│       ┌──────────────┐         │         ┌──────────────┐                   │
│       │    Model     │◄────────┘         │    View      │                   │
│       │  (데이터)    │                   │   (갱신)     │                   │
│       └──────────────┘                   └──────────────┘                   │
│              │                                                              │
│              └─────── 상태 변경 알림 (Observer) ──────►                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1. 동작 흐름

```
1. 사용자 입력 → Controller
2. Controller → Model 조작
3. Model → 상태 변경
4. Model → View에 알림 (Observer)
5. View → 화면 갱신
```

---

## Ⅲ. 변형 패턴

### 1. MVC vs MVP vs MVVM

| 구분 | MVC | MVP | MVVM |
|:---:|:---|:---|:---|
| **연결** | View-Model 직접 | Presenter 중개 | ViewModel 바인딩 |
| **테스트** | 어려움 | 용이 | 매우 용이 |
| **사례** | Spring MVC | Android | WPF, Vue |

---

## Ⅳ. Spring MVC 예시

```kotlin
// Controller
@Controller
class UserController(private val userService: UserService) {
    @GetMapping("/users/{id}")
    fun getUser(@PathVariable id: Long, model: Model): String {
        model.addAttribute("user", userService.findById(id))
        return "userDetail"  // View 이름
    }
}

// Model (Service + Entity)
@Service
class UserService(private val userRepository: UserRepository) {
    fun findById(id: Long) = userRepository.findById(id)
}

// View (Thymeleaf 템플릿)
// userDetail.html
// <div th:text="${user.name}"></div>
```

---

## Ⅴ. 기대효과

| 효과 | 설명 |
|:---:|:---|
| **관심사 분리** | 독립적 개발/테스트 |
| **재사용성** | View/Model 재사용 |
| **유지보수** | 수정 영향 최소화 |

---

## 📌 관련 개념
- [옵저버 패턴](../05_gof_behavioral/observer_pattern.md): Model-View 연결
- [전략 패턴](../05_gof_behavioral/strategy_pattern.md): Controller 전략
- [MVVM](./mvvm_pattern.md): 데이터 바인딩

---

## 👶 어린이를 위한 비유
MVC는 **피자 가게**와 같아요! 주방(Model)에서 피자를 만들고, 메뉴판(View)에서 보여주고, 웨이터(Controller)가 주문을 받아요. 각자 자기 일만 하면 돼요!
