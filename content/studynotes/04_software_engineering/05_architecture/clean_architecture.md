+++
title = "클린 아키텍처 (Clean Architecture)"
date = 2024-05-24
description = "Robert C. Martin의 의존성 규칙 기반 계층형 아키텍처, 비즈니스 로직의 프레임워크 독립성 보장"
weight = 10
+++

# 클린 아키텍처 (Clean Architecture)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 클린 아키텍처는 Robert C. Martin(Uncle Bob)이 제안한 아키텍처로, **의존성 규칙(Dependency Rule)**에 따라 모든 의존성이 **바깥쪽(외부)에서 안쪽(내부)으로만** 향해야 하며, 비즈니스 로직이 프레임워크, DB, UI 등 **외부 요소로부터 완전히 독립**되도록 설계하는 것입니다.
> 2. **가치**: 프레임워크 교체, DB 변경, UI 수정이 **비즈니스 로직에 영향을 주지 않으며**, 테스트 용이성(Testability)이 극대화되고, **변화에 유연하게 대응**할 수 있습니다.
> 3. **융합**: 헥사고날 아키텍처, 어니언 아키텍처와 동일한 철학을 공유하며, **DDD(도메인 주도 설계)의 전술적 설계와 완벽하게 결합**됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의
클린 아키텍처는 2017년 Robert C. Martin이 저서 "Clean Architecture: A Craftsman's Guide to Software Structure and Design"에서 정립한 아키텍처 패턴입니다.

**핵심 원칙 - 의존성 규칙 (Dependency Rule)**:
> "소스코드 의존성은 오직 안쪽(내부)으로만 향해야 한다. 내부의 원은 외부의 원에 대해 아무것도 알지 못한다."

### 💡 일상생활 비유: 양파와 같은 구조
클린 아키텍처는 양파와 유사하게 여러 겹의 층으로 구성됩니다.

```
[양파 구조]

     최외각: 껍질 (UI, DB, 프레임워크)
         |
         v
     중간: 과육 (유스케이스, 인터페이스 어댑터)
         |
         v
     핵심: 심 (엔티티, 비즈니스 규칙)

[핵심 원칙]
- 심은 껍질을 모른다
- 껍질은 심을 안다
- 안쪽이 바깥쪽에 의존하지 않는다
```

### 2. 등장 배경 및 발전 과정

#### 1) 기존 아키텍처의 문제점
- **MVC의 한계**: Controller가 Model과 View에 강결합
- **프레임워크 종속**: Spring/Node.js 등 프레임워크 변경 불가
- **DB 종속**: 비즈니스 로직이 SQL에 직접 의존
- **테스트 어려움**: 외부 의존성 때문에 단위 테스트 불가

#### 2) 선행 아키텍처들의 통합
- **헥사고날 아키텍처 (Alistair Cockburn, 2005)**: Ports and Adapters
- **어니언 아키텍처 (Jeffrey Palermo, 2008)**: 계층형 동심원
- **클린 아키텍처 (2012)**: 위 개념들의 통합 및 정립

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 클린 아키텍처의 4계층

| 계층 | 명칭 | 역할 | 내용물 | 의존 대상 |
| :--- | :--- | :--- | :--- | :--- |
| **Entities** | 엔티티 | 핵심 비즈니스 규칙 | 엔터프라이즈/비즈니스 객체 | 없음 (최내부) |
| **Use Cases** | 유스케이스 | 애플리케이션 특화 규칙 | 인터랙터, 비즈니스 로직 흐름 | Entities |
| **Interface Adapters** | 인터페이스 어댑터 | 데이터 변환 | 컨트롤러, 프레젠터, 게이트웨이 | Use Cases |
| **Frameworks & Drivers** | 프레임워크/드라이버 | 외부 세계 연결 | DB, 웹 프레임워크, UI | Interface Adapters |

### 2. 정교한 구조 다이어그램

```text
================================================================================
|                        CLEAN ARCHITECTURE LAYERS                              |
================================================================================

    +-------------------------------------------------------------------+
    |                    Frameworks & Drivers                            |
    |  +-------------------------------------------------------------+  |
    |  |                 Interface Adapters                          |  |
    |  |  +-----------------------------------------------------+    |  |
    |  |  |                  Use Cases                          |    |  |
    |  |  |  +---------------------------------------------+    |    |  |
    |  |  |  |                Entities                     |    |    |  |
    |  |  |  |                                             |    |    |  |
    |  |  |  |   Enterprise Business Rules                 |    |    |  |
    |  |  |  |   - Core business logic                     |    |    |  |
    |  |  |  |   - Domain entities                         |    |    |  |
    |  |  |  |   - Business rules                          |    |    |  |
    |  |  |  |                                             |    |    |  |
    |  |  |  +---------------------------------------------+    |    |  |
    |  |  |                                                |    |    |  |
    |  |  |   Application Business Rules                   |    |    |  |
    |  |  |   - Use cases / Interactors                    |    |    |  |
    |  |  |   - Input/Output boundaries                    |    |    |  |
    |  |  |                                                |    |    |  |
    |  |  +-----------------------------------------------------+    |  |
    |  |                                                           |  |
    |  |   Interface Adapters                                      |  |
    |  |   - Controllers, Presenters                               |  |
    |  |   - Gateways (Repository implementations)                 |  |
    |  |   - Data Mappers                                          |  |
    |  |                                                           |  |
    |  +-------------------------------------------------------------+  |
    |                                                                   |
    |   Frameworks & Drivers                                            |
    |   - Web Framework (Spring, Express)                               |
    |   - Database (MySQL, PostgreSQL, MongoDB)                         |
    |   - External APIs, UI (React, Vue)                                |
    |                                                                   |
    +-------------------------------------------------------------------+

    DEPENDENCY RULE:
    ================
    --> All dependencies point INWARD -->

    Outer layers depend on inner layers
    Inner layers know NOTHING about outer layers

================================================================================
```

### 3. 심층 동작 원리: 의존성 역전 (DIP) 적용

```text
[의존성 역전 원칙 (Dependency Inversion Principle)]

전통적 구조 (문제):
+----------------+        +----------------+
|    Controller  | -----> |   Use Case     |
+----------------+        |   Interactor   |
                          +----------------+
                                 |
                                 v
                          +----------------+
                          |   Repository   |
                          |  (DB 종속)     |
                          +----------------+

→ Use Case가 DB 구현에 직접 의존
→ DB 변경 시 Use Case 수정 필요

클린 아키텍처 구조 (해결):
+----------------+        +----------------+
|    Controller  | -----> |   Input Port   | (Interface)
+----------------+        +----------------+
                                 ^
                                 | implements
                          +----------------+
                          |   Use Case     |
                          |   Interactor   |
                          +----------------+
                                 |
                                 | depends on
                                 v
                          +----------------+
                          |  Output Port   | (Interface)
                          +----------------+
                                 ^
                                 | implements
                          +----------------+
                          |   Repository   |
                          |   Impl         |
                          +----------------+

→ Use Case는 인터페이스(Port)에만 의존
→ DB 구현이 바뀌어도 Use Case 수정 불필요
```

### 4. 실무 코드 예시: 클린 아키텍처 구현

```python
"""
클린 아키텍처 실무 예시: 사용자 등록 기능
Python으로 각 계층을 명확히 분리
"""

# ============== ENTITIES LAYER ==============
# core/entities/user.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    """사용자 엔티티 - 핵심 비즈니스 규칙"""
    id: Optional[int]
    email: str
    name: str
    created_at: datetime

    def is_valid_email(self) -> bool:
        """이메일 유효성 검사 - 비즈니스 규칙"""
        return "@" in self.email and "." in self.email.split("@")[1]

    def can_register(self) -> tuple[bool, str]:
        """등록 가능 여부 - 비즈니스 규칙"""
        if not self.is_valid_email():
            return False, "유효하지 않은 이메일 형식입니다"
        if len(self.name) < 2:
            return False, "이름은 2자 이상이어야 합니다"
        return True, "등록 가능"


# ============== USE CASES LAYER ==============
# core/usecases/ports.py (Input/Output Ports)
from abc import ABC, abstractmethod

class RegisterUserInputPort(ABC):
    """입력 포트 - Controller가 호출하는 인터페이스"""
    @abstractmethod
    def execute(self, email: str, name: str) -> 'RegisterUserResponse':
        pass

class RegisterUserOutputPort(ABC):
    """출력 포트 - Presenter가 구현하는 인터페이스"""
    @abstractmethod
    def present_success(self, user: User) -> 'RegisterUserResponse':
        pass

    @abstractmethod
    def present_failure(self, error_message: str) -> 'RegisterUserResponse':
        pass

class UserRepository(ABC):
    """저장소 포트 - Repository가 구현하는 인터페이스"""
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass


# core/usecases/register_user.py
@dataclass
class RegisterUserRequest:
    email: str
    name: str

@dataclass
class RegisterUserResponse:
    success: bool
    user_id: Optional[int]
    message: str

class RegisterUserInteractor(RegisterUserInputPort):
    """
    유스케이스 인터랙터
    - 애플리케이션 특화 비즈니스 규칙
    - 엔티티를 조율하고 흐름 제어
    """
    def __init__(
        self,
        user_repository: UserRepository,
        output_port: RegisterUserOutputPort
    ):
        self.user_repository = user_repository
        self.output_port = output_port

    def execute(self, email: str, name: str) -> RegisterUserResponse:
        # 1. 사용자 생성
        user = User(id=None, email=email, name=name, created_at=datetime.now())

        # 2. 비즈니스 규칙 검증 (Entity)
        can_register, message = user.can_register()
        if not can_register:
            return self.output_port.present_failure(message)

        # 3. 중복 이메일 확인 (Use Case 규칙)
        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            return self.output_port.present_failure("이미 등록된 이메일입니다")

        # 4. 저장
        saved_user = self.user_repository.save(user)

        # 5. 결과 반환
        return self.output_port.present_success(saved_user)


# ============== INTERFACE ADAPTERS LAYER ==============
# adapters/controllers/user_controller.py
class RegisterUserController:
    """
    컨트롤러
    - 외부 요청을 유스케이스 입력 포트로 변환
    """
    def __init__(self, use_case: RegisterUserInputPort):
        self.use_case = use_case

    def register(self, request_body: dict) -> dict:
        email = request_body.get('email', '')
        name = request_body.get('name', '')

        response = self.use_case.execute(email, name)

        return {
            'success': response.success,
            'user_id': response.user_id,
            'message': response.message
        }

# adapters/presenters/user_presenter.py
class RegisterUserPresenter(RegisterUserOutputPort):
    """
    프레젠터
    - 유스케이스 출력을 표현 형식으로 변환
    """
    def present_success(self, user: User) -> RegisterUserResponse:
        return RegisterUserResponse(
            success=True,
            user_id=user.id,
            message=f"사용자 {user.name}님이 등록되었습니다"
        )

    def present_failure(self, error_message: str) -> RegisterUserResponse:
        return RegisterUserResponse(
            success=False,
            user_id=None,
            message=error_message
        )

# adapters/gateways/user_repository_impl.py
class UserRepositoryImpl(UserRepository):
    """
    저장소 구현체
    - 실제 DB 연동 (SQLAlchemy, Django ORM, etc.)
    """
    def __init__(self, db_session):
        self.db_session = db_session

    def find_by_email(self, email: str) -> Optional[User]:
        # DB 쿼리 로직
        db_user = self.db_session.query(UserModel).filter_by(email=email).first()
        if db_user:
            return User(id=db_user.id, email=db_user.email, name=db_user.name, created_at=db_user.created_at)
        return None

    def save(self, user: User) -> User:
        # DB 저장 로직
        db_user = UserModel(email=user.email, name=user.name, created_at=user.created_at)
        self.db_session.add(db_user)
        self.db_session.commit()
        return User(id=db_user.id, email=db_user.email, name=db_user.name, created_at=db_user.created_at)


# ============== FRAMEWORKS & DRIVERS LAYER ==============
# frameworks/web/app.py (Flask/FastAPI)
from flask import Flask, request, jsonify

app = Flask(__name__)

# 의존성 주입 설정
def setup_dependencies():
    db_session = create_db_session()  # DB 연결
    user_repository = UserRepositoryImpl(db_session)
    presenter = RegisterUserPresenter()
    use_case = RegisterUserInteractor(user_repository, presenter)
    controller = RegisterUserController(use_case)
    return controller

@app.route('/api/users', methods=['POST'])
def register_user():
    controller = setup_dependencies()
    request_body = request.get_json()
    response = controller.register(request_body)
    return jsonify(response), 201 if response['success'] else 400
```

### 5. 계층별 테스트 전략

| 계층 | 테스트 유형 | 의존성 | 도구 |
| :--- | :--- | :--- | :--- |
| **Entities** | 단위 테스트 | 없음 | pytest, JUnit |
| **Use Cases** | 단위 테스트 | Mock Repository, Mock Presenter | pytest-mock, Mockito |
| **Interface Adapters** | 통합 테스트 | Fake/Mock DB | TestContainers |
| **Frameworks** | E2E 테스트 | 실제 DB, HTTP | Selenium, Postman |

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 아키텍처 패턴

| 아키텍처 | 핵심 개념 | 장점 | 단점 | 적합 상황 |
| :--- | :--- | :--- | :--- | :--- |
| **계층형** | Presentation→Business→Data | 단순함 | 하위 계층 의존 | 소규모 앱 |
| **클린 아키텍처** | 의존성 역전 + 동심원 | 독립성, 테스트 용이 | 복잡도 증가 | 중/대형 엔터프라이즈 |
| **헥사고날** | Ports & Adapters | 외부 교체 용이 | 추상화 과다 | 마이크로서비스 |
| **DDD** | 바운디드 컨텍스트 | 비즈니스 정합성 | 학습 곡선 | 복잡한 도메인 |

### 2. 과목 융합 관점 분석

#### 클린 아키텍처 + DDD

```text
[클린 아키텍처 - DDD 매핑]

Clean Architecture          DDD
=================          ====
Entities Layer       <---> Domain Layer
                      - Entity, Value Object
                      - Aggregate Root
                      - Domain Service

Use Cases Layer      <---> Application Layer
                      - Application Service
                      - Command/Query Handler
                      - Domain Event Handler

Interface Adapters   <---> Infrastructure Layer
                      - Repository Implementation
                      - External Service Adapters

[시너지]
- DDD의 전술적 설계가 Clean Architecture의 Entities/Use Cases 구현 가이드
- Clean Architecture의 의존성 규칙이 DDD의 도메인 보호
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오

**[시나리오] 프레임워크 마이그레이션**
*   **상황**: Django → FastAPI로 전환 필요
*   **클린 아키텍처 적용 시**:
    - Entities/Use Cases는 수정 없음
    - Interface Adapters (Controller/Presenter)만 수정
    - Frameworks Layer (Django → FastAPI) 교체
    - **비즈니스 로직 영향 없음**

### 2. 주의사항

*   **과도한 추상화**: 모든 것을 인터페이스화하면 복잡도만 증가
    → 변경 가능성이 높은 부분만 추상화
*   **보일러플레이트 코드**: 많은 인터페이스와 DTO 필요
    → 코드 생성기 또는 템플릿 활용
*   **소규모 프로젝트 과적용**: 작은 프로젝트에는 과도한 엔지니어링
    → 규모에 맞는 아키텍처 선택

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### ※ 참고 표준/가이드
*   **Clean Architecture (Robert C. Martin)**: 원저
*   **Hexagonal Architecture (Alistair Cockburn)**: 선행 개념
*   **Onion Architecture (Jeffrey Palermo)**: 선행 개념

---

## 📌 관련 개념 맵 (Knowledge Graph)
*   [SOLID 원칙](@/studynotes/04_software_engineering/01_sdlc/design_patterns.md) : 클린 아키텍처의 기반 원칙
*   [DDD (Domain-Driven Design)](@/studynotes/04_software_engineering/01_sdlc/msa.md) : 도메인 계층 심화
*   [마이크로서비스](@/studynotes/04_software_engineering/01_sdlc/msa.md) : 클린 아키텍처 적용 대상
*   [TDD](@/studynotes/04_software_engineering/02_quality/software_testing.md) : 클린 아키텍처의 테스트 용이성 활용

---

## 👶 어린이를 위한 3줄 비유 설명
1. **문제**: 레고 로봇을 만들었는데, 팔이 마음에 들지 않아서 바꾸려고 해요. 근데 팔을 바꾸려면 몸통도 다시 만들어야 해요.
2. **해결(클린 아키텍처)**: 이제는 팔, 다리, 머리가 서로 따로따로 붙어요. 팔을 바꾸고 싶으면 팔만 떼고 새 팔을 붙이면 돼요. 몸통(핵심)은 그대로!
3. **효과**: "팔이 부러졌어" 하고 새 팔만 만들면 되니까 훨씬 편해요. 그리고 어떤 팔이든 붙일 수 있어요!
