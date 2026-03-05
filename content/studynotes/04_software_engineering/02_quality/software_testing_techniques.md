+++
title = "소프트웨어 테스팅 기법 (Software Testing Techniques)"
date = 2024-05-24
description = "블랙박스/화이트박스 테스팅, 테스트 레벨, 커버리지 기반 품질 검증 체계"
weight = 10
+++

# 소프트웨어 테스팅 기법 (Software Testing Techniques)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 테스팅은 결함을 발견하고 품질을 검증하기 위해 **계획된 테스트 케이스를 설계·수행·평가**하는 체계적 활동으로, **블랙박스(명세 기반)**와 **화이트박스(구조 기반)**로 대별되며 단위→통합→시스템→인수의 4단계 레벨로 구성됩니다.
> 2. **가치**: 테스트 커버리지(구문 80%+, 분기 70%+)를 확보하고 Shift-Left 테스팅으로 **결함을 개발 초기에 발견**함으로써 수정 비용을 10~100배 절감합니다.
> 3. **융합**: TDD(테스트 주도 개발), BDD(행동 주도 개발), CI/CD 파이프라인 내 자동화 테스트, AI 기반 테스트 케이스 생성 등 **현대적 개발 방법론과 깊이 결합**되어 있습니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의
소프트웨어 테스팅은 소프트웨어가 **요구사항을 충족하는지 검증(Verification)**하고, **사용자의 기대를 만족시키는지 확인(Validation)**하는 활동입니다. 테스팅의 7가지 원칙(ISTQB)은 다음과 같습니다.

1. 테스팅은 결함의 존재를 밝히는 것이지, 결함이 없음을 증명할 수 없다
2. 완벽한 테스팅은 불가능하다 (Exhaustive Testing is Impossible)
3. 조기 테스팅 (Early Testing)
4. 결함의 군집 (Defect Clustering) - 파레토 법칙 (80:20)
5. 살충제 패러독스 (Pesticide Paradox) - 동일한 테스트는 새로운 버그를 못 찾음
6. 테스팅은 정황에 의존적 (Testing is Context Dependent)
7. 오류 부재의 궤변 (Absence of Errors Fallacy) - 요구사항 미충족 시 결함 없어도 무용지물

### 💡 일상생활 비유: 자동차 안전 검사
소프트웨어 테스팅은 자동차의 안전 검사와 유사합니다.

```
[단위 테스트] = 부품 테스트
  - 엔진이 시동되는가?
  - 브레이크 패드가 마모되지 않았는가?
  - 각 부품이 규격에 맞는가?

[통합 테스트] = 조립 후 테스트
  - 엔진과 변속기가 연동되는가?
  - 브레이크 페달을 밟으면 바퀴가 멈추는가?

[시스템 테스트] = 완성차 테스트
  - 최고 속도가 200km/h인가?
  - 연비가 15km/L인가?
  - 충돌 테스트에서 안전한가?

[인수 테스트] = 시승 테스트
  - 운전자가 운전하기 편한가?
  - 승차감이 좋은가?
  - 실제 도로에서 문제없는가?
```

### 2. 등장 배경 및 발전 과정

#### 1) 1950~60년대: 디버깅 시대
초기 소프트웨어에서 '테스팅'은 프로그래머가 직접 코드를 실행해 보는 **디버깅(Debugging)**과 동일시되었습니다.

#### 2) 1970년대: 검증과 확인의 구분
1979년 글렌포드 마이어스(Glenford Myers)가 **"테스팅은 오류가 없음을 증명하는 것이 아니라, 오류를 찾아내는 과정"**임을 정의했습니다. V-모델에서 검증(Verification)과 확인(Validation)의 개념이 정립되었습니다.

#### 3) 1990년대: 테스트 자동화와 TDD
1997년 Kent Beck이 **TDD(Test-Driven Development)**를 소개했고, JUnit(1997) 등 단위 테스트 프레임워크가 등장했습니다.

#### 4) 2000년대~현재: Agile Testing, DevOps, AI Testing
애자일의 등장으로 테스팅이 개발 전 과정에 통합되었고, CI/CD 파이프라인에서 **자동화된 테스트**가 필수가 되었습니다. 최근에는 AI가 테스트 케이스를 생성하는 **AI Testing**이 부상하고 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 테스트 레벨과 유형 매트릭스

| 레벨 | 정의 | 테스트 기반 | 책임자 | 핵심 기법 | V-모델 대응 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **단위 테스트** | 최소 단위(모듈/함수) 검증 | 코드, 설계 | 개발자 | 화이트박스, Mock | 코딩 |
| **통합 테스트** | 모듈 간 인터페이스 검증 | 설계, 아키텍처 | 개발자/테스터 | 통합 전략, API 테스트 | 상세 설계 |
| **시스템 테스트** | 전체 시스템 기능/비기능 검증 | 요구사항, 비즈니스 | 테스터/QA | 블랙박스, 성능/보안 테스트 | 시스템 설계 |
| **인수 테스트** | 사용자 요구 충족 여부 확인 | 비즈니스 요구 | 사용자/PO | UAT, 베타 테스트 | 요구사항 분석 |

### 2. 정교한 구조 다이어그램: 테스팅 V-모델

```text
================================================================================
|                     SOFTWARE TESTING V-MODEL ARCHITECTURE                     |
================================================================================

    [Requirements Analysis] ---------------------------------> [Acceptance Testing]
             |                           |                              |
             | 1:1                       |                              |
             v                           |                              v
    [System Design] -----------------------------> [System Testing]
             |                           |                     |
             | 1:1                       |                     |
             v                           |                     v
    [Detailed Design] -------------------------> [Integration Testing]
             |                           |                  |
             | 1:1                       |                  |
             v                           |                  v
    [Unit Design/Coding] ----------------------> [Unit Testing]
             |                           |               |
             +-------------+-------------+---------------+
                           |
                           v
                  [Test Levels Detail]

    UNIT TESTING (단위 테스트)
    =========================
    | Focus: Individual components
    | Technique: White-box (Structure-based)
    | Coverage: Statement, Branch, Path
    | Tools: JUnit, pytest, NUnit
    ---------------------------

    INTEGRATION TESTING (통합 테스트)
    ================================
    | Focus: Interfaces between components
    | Strategy: Big-bang, Top-down, Bottom-up, Sandwich
    | Tools: Postman, RestAssured, TestContainers
    ----------------------------------

    SYSTEM TESTING (시스템 테스트)
    ==============================
    | Focus: End-to-end functionality
    | Type: Functional + Non-functional
    | Tools: Selenium, JMeter, OWASP ZAP
    -------------------------------

    ACCEPTANCE TESTING (인수 테스트)
    ================================
    | Focus: Business requirements
    | Type: Alpha, Beta, UAT, OAT
    | Criteria: INVEST, Acceptance Criteria
    ---------------------------------

================================================================================
```

### 3. 심층 동작 원리: 블랙박스 vs 화이트박스 테스팅

#### 블랙박스 테스팅 (Black-box Testing)

```text
[특징]
- 내부 구조/코드를 보지 않음
- 입력(Input)과 출력(Output)만 검증
- 명세서(Specification) 기반

[핵심 기법]

1. 동등 분할 (Equivalence Partitioning)
   입력 영역을 동등한 클래스로 분할하여 대푯값만 테스트

   예: 나이 입력 (0-150)
   - 유효 클래스: 1~149 (대푯값: 50)
   - 무효 클래스: -1, 0, 150, 200

2. 경계값 분석 (Boundary Value Analysis)
   경계 부근에서 결함이 많이 발생한다는 원리

   예: 나이 입력 (1-100)
   - 최소 경계: 0, 1, 2
   - 최대 경계: 99, 100, 101

3. 의사결정 테이블 (Decision Table)
   복잡한 조건 조합을 체계적으로 테스트

   예: 할인율 계산
   +-------+-------+-------+-------+
   | 회원  | VIP   | Y     | Y     |
   | 구매액| 10만+ | 10만- | 10만+ |
   | 할인율| 30%   | 10%   | 20%   |
   +-------+-------+-------+-------+

4. 상태 전이 테스팅 (State Transition)
   객체의 상태 변화를 다이어그램으로 표현하고 테스트

   예: 주문 상태
   [주문접수] --> [결제완료] --> [배송중] --> [배송완료]
        |              |
        v              v
     [취소]        [반품]
```

#### 화이트박스 테스팅 (White-box Testing)

```text
[특징]
- 내부 구조/코드를 분석
- 제어 흐름, 데이터 흐름 검증
- 커버리지 기반

[커버리지 종류]

1. 구문 커버리지 (Statement Coverage, C0)
   모든 문장이 최소 1회 실행되는지

   코드:
   1: if (a > 0) {
   2:     x = x + 1;
   3: }
   4: y = y + 1;

   테스트: a = 1 → 라인 1,2,4 실행 (100%)

2. 결정/분기 커버리지 (Decision/Branch Coverage, C1)
   모든 분기가 참/거짓으로 수행되는지

   코드:
   if (a > 0 && b > 0) { ... }

   테스트:
   - a=1, b=1 → 참
   - a=0, b=1 → 거짓
   → 2개 테스트로 100% 분기 커버리지

3. 조건 커버리지 (Condition Coverage, C2)
   각 개별 조건이 참/거짓을 한 번씩 가지는지

   코드:
   if (a > 0 || b > 0) { ... }

   테스트:
   - a=1, b=0 → a=T, b=F → 전체=T
   - a=0, b=1 → a=F, b=T → 전체=T
   → 조건 커버리지 100%이지만, 전체 거짓 케이스 미테스트!

4. 조건/결정 커버리지 (Condition/Decision Coverage)
   개별 조건과 전체 결정 모두 참/거짓을 가짐

5. 변경 조건/결정 커버리지 (MC/DC)
   각 조건이 독립적으로 전체 결과에 영향을 미침을 증명
   (항공/자동차 안전 표준 DO-178C, ISO 26262 요구)

6. 경로 커버리지 (Path Coverage)
   가능한 모든 실행 경로 테스트
   (현실적으로 불가능한 경우 많음)
```

### 4. 실무 코드 예시: 테스트 케이스 설계

```python
"""
테스팅 기법 적용 예시: 사용자 등록 기능
요구사항: 나이는 1-100세, 이메일은 형식 검증, VIP 회원은 10% 할인
"""

import pytest
from unittest.mock import Mock, patch
from decimal import Decimal

class UserRegistration:
    """사용자 등록 서비스"""

    MIN_AGE = 1
    MAX_AGE = 100

    def register(self, name: str, age: int, email: str, is_vip: bool) -> dict:
        """사용자 등록"""
        # 1. 나이 검증 (경계값 분석)
        if age < self.MIN_AGE or age > self.MAX_AGE:
            raise ValueError(f"나이는 {self.MIN_AGE}-{self.MAX_AGE}세여야 합니다")

        # 2. 이메일 형식 검증
        if not self._validate_email(email):
            raise ValueError("유효하지 않은 이메일 형식입니다")

        # 3. 회원 정보 반환
        return {
            "name": name,
            "age": age,
            "email": email,
            "is_vip": is_vip,
            "discount_rate": Decimal("0.1") if is_vip else Decimal("0")
        }

    def _validate_email(self, email: str) -> bool:
        """이메일 형식 검증 (동등 분할)"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))


# ========== 테스트 클래스 ==========

class TestUserRegistration:
    """사용자 등록 테스트"""

    @pytest.fixture
    def service(self):
        return UserRegistration()

    # --- 동등 분할 (Equivalence Partitioning) ---
    @pytest.mark.parametrize("age,expected_valid", [
        # 유효 클래스 (대푯값)
        (25, True),    # 정상 나이
        (1, True),     # 최소 경계
        (100, True),   # 최대 경계

        # 무효 클래스 (대푯값)
        (0, False),    # 최소 미만
        (-1, False),   # 음수
        (101, False),  # 최대 초과
        (150, False),  # 과도한 값
    ])
    def test_age_validation_equivalence_partitioning(
        self, service, age, expected_valid
    ):
        """동등 분할 기반 나이 검증 테스트"""
        if expected_valid:
            result = service.register("Test", age, "test@example.com", False)
            assert result["age"] == age
        else:
            with pytest.raises(ValueError):
                service.register("Test", age, "test@example.com", False)

    # --- 경계값 분석 (Boundary Value Analysis) ---
    @pytest.mark.parametrize("age", [
        0,    # 최소 - 1 (무효)
        1,    # 최소 (유효)
        2,    # 최소 + 1 (유효)
        99,   # 최대 - 1 (유효)
        100,  # 최대 (유효)
        101,  # 최대 + 1 (무효)
    ])
    def test_age_boundary_values(self, service, age):
        """경계값 분석 기반 나이 테스트"""
        is_valid = 1 <= age <= 100

        if is_valid:
            result = service.register("Test", age, "test@example.com", False)
            assert result["age"] == age
        else:
            with pytest.raises(ValueError):
                service.register("Test", age, "test@example.com", False)

    # --- 의사결정 테이블 (Decision Table) ---
    @pytest.mark.parametrize("is_vip,expected_discount", [
        (True, Decimal("0.1")),   # VIP: 10% 할인
        (False, Decimal("0")),    # 일반: 0% 할인
    ])
    def test_vip_discount_decision_table(
        self, service, is_vip, expected_discount
    ):
        """의사결정 테이블 기반 VIP 할인 테스트"""
        result = service.register("Test", 25, "test@example.com", is_vip)
        assert result["discount_rate"] == expected_discount

    # --- 이메일 형식 테스트 (동등 분할) ---
    @pytest.mark.parametrize("email,expected_valid", [
        # 유효 클래스
        ("user@example.com", True),
        ("user.name@example.co.kr", True),
        ("user+tag@example.org", True),

        # 무효 클래스
        ("invalid-email", False),
        ("@example.com", False),
        ("user@", False),
        ("user @example.com", False),
    ])
    def test_email_format_validation(
        self, service, email, expected_valid
    ):
        """이메일 형식 검증 테스트"""
        if expected_valid:
            result = service.register("Test", 25, email, False)
            assert result["email"] == email
        else:
            with pytest.raises(ValueError):
                service.register("Test", 25, email, False)


# ========== 화이트박스 테스트: 커버리지 측정 ==========

def calculate_discount(amount: float, is_vip: bool, is_first_purchase: bool) -> float:
    """
    할인율 계산 함수 (화이트박스 테스트 대상)

    제어 흐름:
    1. VIP이면 기본 10%
    2. 첫 구매면 추가 5%
    3. 10만원 이상이면 추가 3%
    4. 최대 20%까지만 적용
    """
    discount = 0.0

    # 분기 1: VIP 확인
    if is_vip:
        discount += 0.1

    # 분기 2: 첫 구매 확인
    if is_first_purchase:
        discount += 0.05

    # 분기 3: 금액 확인
    if amount >= 100000:
        discount += 0.03

    # 분기 4: 최대 할인율 제한
    if discount > 0.2:
        discount = 0.2

    return discount


class TestCalculateDiscount:
    """할인율 계산 화이트박스 테스트"""

    # 구문 커버리지 (Statement Coverage)
    def test_statement_coverage(self):
        """모든 문장이 실행되도록"""
        # 모든 분기가 True인 케이스
        result = calculate_discount(150000, True, True)
        assert result == 0.2  # 10% + 5% + 3% = 18% but capped at 20%

    # 분기 커버리지 (Branch Coverage)
    @pytest.mark.parametrize("is_vip, is_first, amount, expected", [
        # 모든 분기 조합 (2^4 = 16, 핵심만 추출)
        (True,  True,  150000, 0.2),   # T T T → 최대
        (True,  False, 50000,  0.1),   # T F F → VIP만
        (False, True,  50000,  0.05),  # F T F → 첫구매만
        (False, False, 150000, 0.03),  # F F T → 금액만
        (False, False, 50000,  0.0),   # F F F → 없음
    ])
    def test_branch_coverage(self, is_vip, is_first, amount, expected):
        """모든 분기가 참/거짓으로 수행되도록"""
        result = calculate_discount(amount, is_vip, is_first)
        assert result == expected

    # MC/DC (Modified Condition/Decision Coverage)
    def test_mcdc_vip_independence(self):
        """VIP 조건이 독립적으로 결과에 영향을 미침을 증명"""
        # VIP=True일 때와 VIP=False일 때, 다른 조건은 동일
        amount = 50000
        is_first = False

        with_vip = calculate_discount(amount, True, is_first)
        without_vip = calculate_discount(amount, False, is_first)

        assert with_vip > without_vip  # VIP가 결과에 영향

    def test_mcdc_first_purchase_independence(self):
        """첫구매 조건이 독립적으로 결과에 영향을 미침을 증명"""
        amount = 50000
        is_vip = False

        with_first = calculate_discount(amount, is_vip, True)
        without_first = calculate_discount(amount, is_vip, False)

        assert with_first > without_first
```

### 5. 통합 테스트 전략 비교

| 전략 | 방식 | 장점 | 단점 | 필요 도구 |
| :--- | :--- | :--- | :--- | :--- |
| **빅뱅** | 한 번에 전체 통합 | 간단 | 오류 추적 어려움 | 없음 |
| **하향식** | 상위→하위, Stub 사용 | 조기 프로토타입 가능 | Stub 작성 부담 | Mock Framework |
| **상향식** | 하위→상위, Driver 사용 | 하위 모듈 완전 테스트 | 전체 동작 늦게 확인 | Test Harness |
| **샌드위치** | 상하향 병행 | 속도와 품질 균형 | 복잡도 증가 | Mock + Driver |

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 테스트 더블 (Test Double)

| 유형 | 목적 | 동작 | 사용 시점 |
| :--- | :--- | :--- | :--- |
| **Dummy** | 파라미터 채우기 | 아무 동작 안 함 | 필수 파라미터만 필요할 때 |
| **Stub** | 미리 준비된 답변 | 고정 응답 반환 | 상태 검증, 하향식 통합 |
| **Spy** | 호출 정보 기록 | 실제 동작 + 기록 | 행위 일부 검증 |
| **Mock** | 행위 검증 | 예상 호출 검증 | 상호작용 검증 |
| **Fake** | 실제 구현 대체 | 실제와 유사 동작 | DB, 외부 서비스 대체 |

### 2. 과목 융합 관점 분석

#### 테스팅 + DevOps (CI/CD)

```yaml
# CI/CD 파이프라인에서의 테스팅 단계

stages:
  - unit-test        # 단위 테스트 (화이트박스)
  - integration-test # 통합 테스트
  - system-test      # 시스템 테스트
  - acceptance-test  # 인수 테스트

unit-test:
  script:
    - pytest --cov=src --cov-fail-under=80  # 커버리지 80% 강제
  coverage: '/TOTAL.*\s+(\d+%)$/'

integration-test:
  script:
    - docker-compose up -d test-db
    - pytest tests/integration/

system-test:
  script:
    - selenium-side-runner tests/e2e/

acceptance-test:
  script:
    - behave tests/acceptance/  # BDD (Gherkin)
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오

**[시나리오] 금융 코어뱅킹 시스템 테스트 전략**
*   **상황**: 무중단 배포 필요, 장애 시 금전적 손실 막대
*   **전략**:
    1. 단위 테스트: MC/DC 100% (핵심 로직)
    2. 통합 테스트: API 계약 테스트 (Pact)
    3. 시스템 테스트: 성능/부하/보안 테스트
    4. 인수 테스트: 비즈니스 시나리오 기반 UAT
    5. 운영 테스트: 카나리 배포 + 모니터링

### 2. 주의사항 및 안티패턴

*   **테스트 없는 리팩토링**: 테스트 없이 코드를 수정하면 회귀 버그 위험
*   **과도한 Mocking**: Mock이 너무 많으면 실제 동작과 달라질 수 있음
*   **느린 테스트**: 단위 테스트가 느리면 개발자가 실행하지 않음

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적 기대효과

| 구분 | 지표 | 효과 |
| :--- | :--- | :--- |
| **결함 조기 발견** | 단계별 수정 비용 | 요구사항:1, 설계:10, 코딩:100, 테스트:1000 |
| **커버리지** | 구문 커버리지 80%+ | 결함 밀도 40% 감소 |
| **회귀 방지** | 자동화된 회귀 테스트 | 수동 테스트 대비 90% 시간 절약 |

### ※ 참고 표준/가이드
*   **ISTQB (International Software Testing Qualifications Board)**: 국제 테스팅 자격
*   **ISO/IEC/IEEE 29119**: 소프트웨어 테스팅 국제 표준
*   **DO-178C**: 항공 소프트웨어 테스팅 표준 (MC/DC 요구)

---

## 📌 관련 개념 맵 (Knowledge Graph)
*   [소프트웨어 품질 표준](@/studynotes/04_software_engineering/02_quality/software_quality_standards.md) : 테스팅의 품질 목표
*   [TDD (Test Driven Development)](@/studynotes/04_software_engineering/01_sdlc/agile_methodology.md) : 테스트 중심 개발 방법론
*   [DevOps CI/CD](@/studynotes/04_software_engineering/01_sdlc/devops.md) : 테스트 자동화 파이프라인
*   [V-모델](@/studynotes/04_software_engineering/01_sdlc/v_model.md) : 개발-테스트 대응 구조

---

## 👶 어린이를 위한 3줄 비유 설명
1. **문제**: 숙제를 다 했는데 선생님이 "이거 틀렸어"라고 하면 슬프죠. 처음부터 확인했으면 좋았을 텐데!
2. **해결(테스팅)**: 숙제를 제출하기 전에 스스로 확인하는 거예요. 문제 하나하나(단위), 연계된 문제들(통합), 전체(시스템), 친구에게 보여주기(인수) 단계로!
3. **효과**: 나중에 선생님이 틀렸다고 하면 창피하고 다시 해야 하지만, 미리 확인하면 100점 받을 수 있어요!
