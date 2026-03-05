+++
title = "V-모델 (V-Model)"
date = 2024-05-24
description = "검증(Verification)과 확인(Validation)의 대칭 구조를 통한 소프트웨어 품질 보증 체계, 폭포수 모델의 테스트 강화 버전"
weight = 16
+++

# V-모델 (V-Model)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: V-모델은 폭포수 모델의 순차적 개발 단계와 테스트 단계를 **V자 형태의 대칭 구조**로 연결하여, 각 개발 단계에서 대응되는 테스트 단계를 정의함으로써 **초기부터 검증 가능한 품질 보증 체계**를 구축한 것입니다.
> 2. **가치**: 요구사항-인수테스트, 설계-통합테스트, 코딩-단위테스트의 **1:1 매핑을 통한 추적성(Traceability)**을 확보하여, 결함의 근본 원인을 신속히 파악하고 수정 비용을 획기적으로 절감합니다.
> 3. **융합**: 안전 중심 시스템(Safety-Critical System)인 항공우주, 의료기기, 자동차, 원자력 분야의 **IEC 61508, ISO 26262, DO-178C 등 안전 표준의 필수 프로세스**로 채택되어 있습니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의
V-모델(V-Model)은 1980년대 독일에서 처음 개발되어 현재는 전 세계적으로 가장 널리 사용되는 소프트웨어 개발 프로세스 모델 중 하나입니다. 폭포수 모델의 변형으로, **좌측 하강 라인(개발 단계)**과 **우측 상승 라인(테스트 단계)**이 V자 형태로 대칭을 이루는 것이 특징입니다.

핵심 개념은 **검증(Verification)**과 **확인(Validation)**의 구분입니다:
- **검증 (Verification)**: "제품을 올바르게 만들고 있는가?" - 명세서대로 개발했는지 확인 (과정 중심)
- **확인 (Validation)**: "올바른 제품을 만들었는가?" - 사용자 요구를 충족하는지 확인 (결과 중심)

### 💡 일상생활 비유: 건축 검사 프로세스
V-모델은 건물을 짓는 과정에서 각 단계마다 대응되는 검사가 존재하는 것과 유사합니다.

```
[설계도 작성] <--매핑--> [준공 검사: 설계도대로 지어졌는가?]
      |                              ^
      v                              |
[구조 계산] <--매핑--> [구조 안전 검사: 계산대로 지어졌는가?]
      |                              ^
      v                              |
[시공] <--매핑--> [재료 검사: 규격 자재를 썼는가?]
```

건축에서는 설계도를 그릴 때 이미 준공 검사 기준을 정해두고, 설계도가 완성되면 그 기준으로 검사합니다. V-모델도 마찬가지로 **요구사항을 작성할 때 인수 테스트 기준을 미리 정의**합니다.

### 2. 등장 배경 및 발전 과정

#### 1) 폭포수 모델의 테스트 문제점
폭포수 모델에서 테스트는 개발의 마지막 단계에 위치했습니다. 이로 인해 다음과 같은 문제가 발생했습니다.
- **늦은 결함 발견**: 요구사항 단계의 오류가 인수 테스트에서야 발견되어 수정 비용이 100배 이상 증가
- **테스트 준비 부족**: 개발 완료 후에야 테스트 계획을 수립하여 테스트 기간 부족
- **추적성 부재**: 결함이 발견되어도 어느 단계의 산출물에서 비롯되었는지 파악 곤란

#### 2) V-모델의 혁신적 해결책
V-모델은 **각 개발 단계에서 즉시 대응되는 테스트 단계를 정의**함으로써 이 문제를 해결했습니다.
- 요구사항 분석 단계에서 **인수 테스트 계획** 수립
- 시스템 설계 단계에서 **시스템 테스트 계획** 수립
- 상세 설계 단계에서 **통합 테스트 계획** 수립
- 코딩 단계에서 **단위 테스트** 수행

#### 3) 안전 중심 산업의 요구사항
항공우주(DO-178C), 자동차(ISO 26262), 의료기기(IEC 62304), 원자력(IEC 61508) 등 안전이 중요한 산업에서는 **요구사항부터 테스트까지의 완전한 추적성**을 법적 요구사항으로 규정하고 있습니다. V-모델은 이러한 규제 요구사항을 가장 잘 충족하는 모델입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. V-모델의 구성 요소 (7단계 + 대칭 테스트)

| 좌측 (개발 단계) | 우측 (테스트 단계) | 대응 관계 | 핵심 활동 | 산출물 |
| :--- | :--- | :--- | :--- | :--- |
| **요구사항 분석** | **인수 테스트** | 1:1 | 사용자 요구 정의, UAT 시나리오 작성 | SRS, 인수 테스트 계획서 |
| **시스템 설계** | **시스템 테스트** | 1:1 | 시스템 아키텍처, 블랙박스 테스트 설계 | HLD, 시스템 테스트 케이스 |
| **상세 설계** | **통합 테스트** | 1:1 | 모듈 인터페이스, 통합 전략 수립 | LLD, 통합 테스트 시나리오 |
| **단위 설계** | **단위 테스트** | 1:1 | 알고리즘, 화이트박스 테스트 설계 | 소스코드, 단위 테스트 코드 |
| **코딩 (Implementation)** | | | 소스코드 작성, 정적 분석 | 실행 파일 |

### 2. 정교한 구조 다이어그램: V-모델의 전체 아키텍처

```text
================================================================================
|                         V-MODEL ARCHITECTURE DIAGRAM                          |
================================================================================

                         [ Requirements Analysis ]
                                    |
                                    | 1:1 Mapping
                                    v
    [ System Design ]                          [ Acceptance Testing ]
           |                                           ^
           | 1:1 Mapping                               | Verify against
           v                                           | Requirements
    [ Detailed Design ]                         [ System Testing ]
           |                                           ^
           | 1:1 Mapping                               | Verify against
           v                                           | System Design
    [ Unit Design ]                             [ Integration Testing ]
           |                                           ^
           | 1:1 Mapping                               | Verify against
           v                                           | Detailed Design
         [ Coding ] -----------------------> [ Unit Testing ]
                        Direct Test
                      (White-box)

    <-- LEFT SIDE -->              <-- RIGHT SIDE -->
      Development                     Testing
      (Decomposition)                 (Integration)

    RELATIONSHIPS:
    =============
    - Each LEFT phase creates deliverables
    - Each RIGHT phase verifies corresponding LEFT deliverable
    - Horizontal arrows indicate TEST BASIS (what to test against)
    - Vertical flow indicates SEQUENCE (top to bottom, then bottom to top)

================================================================================
```

### 3. 심층 동작 원리: 단계별 상세 메커니즘

#### Level 1: 요구사항 분석 ↔ 인수 테스트

```text
[요구사항 분석 단계]
입력: 고객 요청, RFP, 비즈니스 목표
활동:
  1. 이해관계자 인터뷰 및 워크샵
  2. 기능적/비기능적 요구사항 도출
  3. 요구사항 우선순위 설정 (MoSCoW)
  4. SRS (Software Requirements Spec) 작성
  5. ★ 인수 테스트 기준 정의 ★
출력: SRS 문서, 인수 테스트 계획서

            |
            | 1:1 대응
            v

[인수 테스트 단계]
입력: SRS 문서, 인수 테스트 계획서
활동:
  1. 인수 테스트 시나리오 작성
  2. UAT(User Acceptance Test) 수행
  3. 비즈니스 시나리오 기반 테스트
  4. 고객 서명(Sign-off) 획득
검증 기준: "고객이 요청한 대로 동작하는가?"
```

**핵심 원리**: 요구사항을 작성할 때 **어떻게 인수할 것인가(Definition of Done)**를 미리 정의합니다. 이것이 "요구사항 하나당 인수 테스트 케이스 하나 이상"의 원칙입니다.

#### Level 2: 시스템 설계 ↔ 시스템 테스트

```text
[시스템 설계 단계]
입력: SRS 문서
활동:
  1. 시스템 아키텍처 설계 (HLD)
  2. 하드웨어/소프트웨어 할당
  3. 외부 인터페이스 정의
  4. ★ 시스템 테스트 기준 정의 ★
출력: 시스템 설계서, 시스템 테스트 계획서

            |
            | 1:1 대응
            v

[시스템 테스트 단계]
입력: 시스템 설계서, 테스트 계획서
활동:
  1. 블랙박스 테스트 케이스 설계
  2. 기능 테스트 (기능적 요구사항)
  3. 비기능 테스트 (성능, 보안, 가용성)
  4. 회귀 테스트 (결함 수정 후 재테스트)
검증 기준: "시스템이 명세된 대로 동작하는가?"
```

#### Level 3: 상세 설계 ↔ 통합 테스트

```text
[상세 설계 단계]
입력: 시스템 설계서
활동:
  1. 모듈 상세 설계 (LLD)
  2. API 인터페이스 정의
  3. 데이터베이스 스키마 설계
  4. ★ 통합 테스트 기준 정의 ★
출력: 상세 설계서, API 명세, 통합 테스트 계획서

            |
            | 1:1 대응
            v

[통합 테스트 단계]
입력: 상세 설계서, 통합 테스트 계획서
활동:
  1. 모듈 간 인터페이스 테스트
  2. 통합 방식 선택 (Top-down, Bottom-up, Sandwich)
  3. 스텁(Stub) / 드라이버(Driver) 활용
  4. API 통합 테스트 (Postman, RestAssured)
검증 기준: "모듈 간 인터페이스가 올바른가?"
```

#### Level 4: 단위 설계/코딩 ↔ 단위 테스트

```text
[단위 설계/코딩 단계]
입력: 상세 설계서
활동:
  1. 알고리즘 구현
  2. 코딩 표준 준수
  3. ★ 단위 테스트 코드 작성 (TDD) ★
출력: 소스코드, 단위 테스트 코드

            |
            | 직접 테스트
            v

[단위 테스트 단계]
입력: 소스코드
활동:
  1. 화이트박스 테스트 (구문, 분기, 조건 커버리지)
  2. Mock 객체 활용 (의존성 격리)
  3. 경계값 분석, 동등 분할
  4. 코드 커버리지 측정 (80%+ 목표)
검증 기준: "코드가 로직대로 동작하는가?"
```

### 4. 실무 코드 예시: V-모델 기반 테스트 케이스 작성

```python
"""
V-모델 적용 예시: 결제 시스템 개발

요구사항 ID: REQ-PAY-001
요구사항: "사용자는 신용카드로 결제할 수 있어야 한다"
인수 기준: 결제 성공 시 승인 번호가 반환되고, 실패 시 에러 메시지가 표시된다
"""

# 1. 요구사항 분석 단계에서 작성되는 인수 테스트 (Acceptance Test)
class PaymentAcceptanceTest:
    """
    인수 테스트: 고객/PO가 승인하는 테스트
    작성 시점: 요구사항 분석 단계 (SRS 작성 시)
    """

    def test_payment_success_returns_approval_code(self):
        """[AT-001] 결제 성공 시 승인 번호 반환"""
        # Given: 유효한 카드 정보
        card = CreditCard(number="4111111111111111", expiry="12/25", cvv="123")

        # When: 결제 요청
        result = payment_service.process_payment(card, amount=10000)

        # Then: 승인 번호 반환
        assert result.status == "SUCCESS"
        assert result.approval_code is not None
        assert len(result.approval_code) == 8

    def test_payment_failure_shows_error_message(self):
        """[AT-002] 결제 실패 시 에러 메시지 표시"""
        # Given: 유효하지 않은 카드
        card = CreditCard(number="0000000000000000", expiry="12/25", cvv="123")

        # When: 결제 요청
        result = payment_service.process_payment(card, amount=10000)

        # Then: 에러 메시지 표시
        assert result.status == "FAILURE"
        assert result.error_message in ["INVALID_CARD", "INSUFFICIENT_FUNDS"]


# 2. 상세 설계 단계에서 작성되는 통합 테스트 (Integration Test)
class PaymentGatewayIntegrationTest:
    """
    통합 테스트: PaymentService와 외부 PG사 연동 테스트
    작성 시점: 상세 설계 단계
    """

    def test_pg_api_integration(self):
        """[IT-001] PG사 API 호출 및 응답 파싱"""
        # Mock PG API 서버 설정
        mock_pg_server = MockPGServer()
        mock_pg_server.set_response({"code": "00", "approval": "ABC12345"})

        # When: PaymentService -> PG API 호출
        response = payment_gateway.send_request(
            card_number="4111111111111111",
            amount=10000
        )

        # Then: 응답 파싱 검증
        assert response.is_successful() == True
        assert response.approval_code == "ABC12345"


# 3. 코딩 단계에서 작성되는 단위 테스트 (Unit Test)
class CardValidatorUnitTest:
    """
    단위 테스트: 카드 번호 검증 로직
    작성 시점: 코딩 단계 (TDD: 테스트 먼저 작성)
    """

    def test_luhn_algorithm_valid_card(self):
        """[UT-001] Luhn 알고리즘으로 유효한 카드 검증"""
        validator = CardValidator()

        # 유효한 카드 번호 (Luhn 체크섬 통과)
        assert validator.validate_number("4111111111111111") == True
        assert validator.validate_number("5500000000000004") == True

    def test_luhn_algorithm_invalid_card(self):
        """[UT-002] Luhn 알고리즘으로 유효하지 않은 카드 검증"""
        validator = CardValidator()

        # 유효하지 않은 카드 번호
        assert validator.validate_number("4111111111111112") == False
        assert validator.validate_number("1234567890123456") == False

    def test_card_expiry_validation(self):
        """[UT-003] 카드 만료일 검증"""
        validator = CardValidator()

        # 경계값 테스트
        assert validator.is_expired("01/20") == True   # 과거
        assert validator.is_expired("12/99") == False  # 미래
```

### 5. 요구사항 추적 매트릭스 (RTM) 예시

| 요구사항 ID | 설계 ID | 코드 모듈 | 단위 테스트 | 통합 테스트 | 시스템 테스트 | 인수 테스트 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| REQ-PAY-001 | DES-PAY-001 | PaymentService.py | UT-PAY-001~003 | IT-PAY-001 | ST-PAY-001 | AT-001, AT-002 |
| REQ-PAY-002 | DES-PAY-002 | RefundService.py | UT-REF-001~002 | IT-REF-001 | ST-REF-001 | AT-003 |
| REQ-PAY-003 | DES-PAY-003 | CardValidator.py | UT-VAL-001~005 | IT-VAL-001 | ST-VAL-001 | AT-004 |

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 폭포수 vs V-모델 vs W-모델

| 비교 항목 | 폭포수 모델 | V-모델 | W-모델 |
| :--- | :--- | :--- | :--- |
| **테스트 시점** | 개발 완료 후 | 각 단계별 대응 테스트 | V-모델 + 병렬 테스트 설계 |
| **추적성** | 낮음 | 높음 (1:1 매핑) | 매우 높음 (양방향) |
| **문서화** | 중간 | 높음 (테스트 계획서 추가) | 매우 높음 |
| **결함 조기 발견** | 어려움 | 가능 | 최적화 |
| **복잡도** | 낮음 | 중간 | 높음 |
| **적합 분야** | 일반 SI | 안전 중심 시스템 | 초대형/고안전 시스템 |

### 2. 과목 융합 관점 분석

#### V-모델 + 소프트웨어 테스팅

```
[V-모델 단계] <-- 매핑 --> [테스트 레벨 (ISO 29119)]
      |                           |
요구사항 분석   <---->  인수 테스트 (Acceptance)
시스템 설계     <---->  시스템 테스트 (System)
상세 설계       <---->  통합 테스트 (Integration)
코딩           <---->  단위 테스트 (Unit)
```

V-모델의 각 단계는 ISO/IEC/IEEE 29119 소프트웨어 테스팅 표준의 **테스트 레벨**과 정확히 일치합니다.

#### V-모델 + 안전 표준 (IEC 61508, ISO 26262)

```text
[V-모델] ----> [안전 표준 요구사항]

요구사항 분석  -->  안전 요구사항 명세 (Safety Requirements)
시스템 설계    -->  안전 아키텍처 설계 (Safety Architecture)
상세 설계      -->  안전 메커니즘 구현 (Safety Mechanisms)
모든 테스트    -->  안전 검증 (Safety Validation)

필수 산출물:
- 안전 계획서 (Safety Plan)
- 위험 분석 보고서 (Hazard Analysis)
- 안전성 검증 보고서 (Safety Validation Report)
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 및 기술사적 의사결정

**[시나리오 1] 자동차 ECU(전자제어장치) 소프트웨어 개발**
*   **상황**: 자동차 브레이크 제어 시스템 개발. ISO 26262 (ASIL-D) 인증 필요.
*   **기술사적 판단**: V-모델 + ASPICE 프로세스 채택
    *   **실행 전략**:
        1. 각 요구사항에 고유 ID 부여 (REQ-SRS-001)
        2. 요구사항별 인수 테스트 케이스 1개 이상 작성
        3. 모든 단계의 산출물에 대한 **양방향 추적성** 확보
        4. 정적 분석 (MISRA-C 규칙) + 동적 분석 + 하드웨어-in-the-loop 테스트

**[시나리오 2] 금융 코어뱅킹 시스템 고도화**
*   **상황**: 기존 메인프레임 시스템을 오픈시스템으로 이관. 금융감독원 감사 대응 필요.
*   **기술사적 판단**: V-모델 + 데이터 검증 테스트 병행
    *   **실행 전략**:
        1. 기존 시스템과 신규 시스템의 **병렬 운영 기간** 설정
        2. 데이터 정합성 검증 테스트 (기존 vs 신규 결과 비교)
        3. RTM(요구사항 추적 매트릭스) 100% 구축

### 2. 도입 시 고려사항 (체크리스트)

**기술적 고려사항**:
- [ ] 추적성 도구 확보: DOORS, Jama Connect, Polarion 등 요구사항 관리 도구
- [ ] 테스트 자동화: 단위/통합/시스템 테스트 자동화 프레임워크
- [ ] 커버리지 측정: 코드 커버리지 80%+, 요구사항 커버리지 100%

**조직적 고려사항**:
- [ ] 독립적 QA 조직: 개발팀과 분리된 테스트팀 구성
- [ ] 형상 관리: 단계별 기준선(Baseline) 관리 프로세스
- [ ] 감사 체계: 내부 감사 및 외부 인증 기관 대응 체계

### 3. 주의사항 및 안티패턴

*   **테스트 계획 지연**: "개발이 끝나면 테스트 계획을 세우자"는 안티패턴. V-모델의 핵심은 **개발 단계에서 테스트 계획을 작성**하는 것입니다.
*   **추적성 누락**: RTM이 형식적인 문서로 전락하는 현상. 결함 발견 시 RTM을 통해 근본 원인을 추적하는 프로세스를 실제로 수행해야 합니다.
*   **과도한 문서화**: 문서가 목적이 되는 현상. 문서는 의사소통과 추적을 위한 수단이며, 실제 테스트 수행이 더 중요합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 지표 | V-모델 적용 시 효과 |
| :--- | :--- | :--- |
| **결함 조기 발견** | 요구사항 단계 결함 검출률 | 60%+ 증가 |
| **수정 비용 절감** | 단계별 수정 비용 비율 | 1:10:100:1000 (요구:설계:코딩:테스트) → 1:5:20:50 |
| **규제 인증** | 인증 1회 통과율 | 90%+ (문서화된 증뢰 활용) |
| **유지보수** | 결함 원인 파악 시간 | 70% 단축 (RTM 활용) |

### 2. 미래 전망 및 진화 방향

1.  **모델 기반 테스팅 (MBT)**: UML/SysML 모델에서 자동으로 테스트 케이스를 생성하여 V-모델의 효율성을 높이는 방식이 확산될 것입니다.
2.  **지속적 V-모델 (Continuous V-Model)**: 애자일/DevOps 환경에서 V-모델의 검증 철학을 CI/CD 파이프라인에 통합하는 하이브리드 접근이 일반화될 것입니다.
3.  **AI 기반 추적성 분석**: LLM을 활용하여 요구사항과 테스트 케이스 간의 매핑을 자동으로 검증하고 누락을 탐지하는 기술이 도입될 것입니다.

### ※ 참고 표준/가이드
*   **ISO/IEC/IEEE 12207**: 시스템 및 소프트웨어 공학 - 생명주기 공정
*   **ISO/IEC/IEEE 15289**: 시스템 및 소프트웨어 공학 - 생명주기 정보 산출물
*   **ISO 26262**: 도로 차량 - 기능 안전 (자동차)
*   **IEC 61508**: 전기/전자/가변 프로그래밍 가능 전자 안전 관련 시스템의 기능 안전
*   **DO-178C**: 항공기 시스템 및 장비 인증을 위한 소프트웨어 고려사항
*   **IEC 62304**: 의료 기기 소프트웨어 - 소프트웨어 생명주기 공정

---

## 📌 관련 개념 맵 (Knowledge Graph)
*   [폭포수 모델](@/studynotes/04_software_engineering/01_sdlc/sdlc_waterfall_model.md) : V-모델의 기반이 되는 순차적 개발 모델
*   [소프트웨어 테스팅](@/studynotes/04_software_engineering/02_quality/software_testing.md) : V-모델의 테스트 단계에 적용되는 기법
*   [요구사항 추적 매트릭스 (RTM)](@/studynotes/04_software_engineering/04_requirements/requirements_engineering.md) : V-모델의 핵심 산출물
*   [CMMI](@/studynotes/04_software_engineering/01_sdlc/_index.md) : V-모델 기반 프로세스의 성숙도 평가 모델
*   [형상 관리 (SCM)](@/studynotes/04_software_engineering/01_sdlc/_index.md) : V-모델 단계별 기준선 관리

---

## 👶 어린이를 위한 3줄 비유 설명
1. **문제**: 숙제를 다 했는데 선생님이 "문제 풀이 과정을 보여줘"라고 하셔서, 답만 써놓고 과정을 모르는 상황이에요.
2. **해결(V-모델)**: 이제는 숙제를 할 때 각 단계마다 "이렇게 풀었어, 맞는지 확인해줘"라고 체크리스트를 만들어요. 문제 읽기 → 계획 세우기 → 풀기 → 검사하기가 짝을 이루죠.
3. **효과**: 틀린 곳을 바로 찾을 수 있어서, 나중에 "어디서 틀렸지?" 하고 다시 처음부터 풀지 않아도 돼요!
