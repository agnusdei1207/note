+++
title = "시큐어 SDLC (Secure Software Development Life Cycle)"
date = 2024-05-24
description = "소프트웨어 개발 전 단계에 보안 활동을 통합한 보안 중심 개발 프로세스"
weight = 10
+++

# 시큐어 SDLC (Secure Software Development Life Cycle)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시큐어 SDLC는 소프트웨어 개발의 **요구사항, 설계, 구현, 테스트, 배포 전 단계에 보안 활동을 내장(Shift-Left)**하여, 개발 완료 후 발견되는 보안 취약점을 **조기에 예방하고 탐지**하는 보안 중심 개발 방법론입니다.
> 2. **가치**: 개발 단계에서 취약점을 수정하는 비용은 운영 단계에서 수정하는 비용의 **1/100** 수준이며, **OWASP Top 10, CWE/SANS Top 25** 등의 주요 취약점을 체계적으로 방어합니다.
> 3. **융합**: Microsoft SDL, OWASP SAMM, BSIMM 등의 성숙도 모델과 연계되며, **DevSecOps의 핵심 기반**으로서 CI/CD 파이프라인에 보안 검사를 자동화합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의
시큐어 SDLC(Secure Software Development Life Cycle)는 **"보안은 나중에"**가 아니라 **"처음부터 보안을"**이라는 철학으로, 소프트웨어 개발의 각 단계에서 수행해야 할 보안 활동을 정의한 프레임워크입니다.

**핵심 원칙**:
1. **Secure by Design**: 설계 단계부터 보안 고려
2. **Secure by Default**: 기본 설정이 보안적으로 안전
3. **Secure in Deployment**: 배포 환경의 보안 보장

### 💡 일상생활 비유: 안전한 건축
시큐어 SDLC는 건축에서 안전을 처음부터 고려하는 것과 유사합니다.

```
[전통적 접근 - 비보안 SDLC]
1. 집 설계 (보안 고려 안 함)
2. 시공
3. 완공 후 "문이 없네?" → 문 설치
4. "창문이 위험해!" → 창문 보강
5. "화재 감지기가 없네!" → 추가 비용

[시큐어 SDLC 접근]
1. 요구사항: "도난 방지, 화재 안전 필요"
2. 설계: 방범창, 소방 설비 포함한 설계도
3. 시공: 안전 자재 사용, 표준 시공
4. 검사: 안전 점검 통과 후 입주
→ 처음부터 안전한 집, 추가 비용 없음
```

### 2. 등장 배경 및 발전 과정

#### 1) 전통적 SDLC의 보안 문제
```
[비보안 SDLC의 문제점]

개발 단계           보안 활동          취약점 발견 시점
============        ============       ================
요구사항 분석       없음
설계               없음
구현               없음               → 10% 여기서 발견
테스트             기능 테스트만      → 20% 여기서 발견
배포               없음
운영               모니터링만         → 70% 여기서 발견 (가장 비용 큼)

[비용 비교]
요구사항 단계에서 수정: 1x
설계 단계에서 수정: 10x
구현 단계에서 수정: 100x
운영 단계에서 수정: 1000x
```

#### 2) 2000년대: Microsoft SDL의 탄생
Microsoft는 2002년 Trustworthy Computing 이니셔티브를 시작하고, 2004년 **SDL(Security Development Lifecycle)**을 공식화했습니다. Windows Vista부터 SDL을 적용하여 보안 취약점이 45% 감소했습니다.

#### 3) 2010년대: OWASP, DevSecOps로 확산
OWASP가 **SAMM(Software Assurance Maturity Model)**을 발표하고, DevOps의 등장으로 **DevSecOps**가 탄생했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 시큐어 SDLC 단계별 보안 활동

| SDLC 단계 | 보안 활동 | 상세 내용 | 산출물 |
| :--- | :--- | :--- | :--- |
| **요구사항** | 보안 요구사항 도출 | 데이터 분류, 규정 준수, 위협 식별 | 보안 요구사항 명세서 |
| **설계** | 위협 모델링 | STRIDE, 공격 표면 분석 | 위협 모델링 보고서 |
| **구현** | 시큐어 코딩 | OWASP 가이드, 입력값 검증 | 보안 코드, 정적 분석 보고서 |
| **테스트** | 보안 테스트 | SAST, DAST, 침투 테스트 | 보안 테스트 보고서 |
| **배포** | 보안 배포 | 취약점 스캔, 구성 검토 | 배포 승인서 |
| **운영** | 보안 모니터링 | SIEM, 침해 사고 대응 | 보안 로그, 대응 보고서 |

### 2. 정교한 구조 다이어그램: 시큐어 SDLC 프로세스

```text
================================================================================
|                    SECURE SDLC - SECURITY ACTIVITIES BY PHASE                 |
================================================================================

    [ REQUIREMENTS PHASE ]
    =====================
    | Security Activities:
    | +-- Security Requirements Elicitation
    | +-- Data Classification (Public, Internal, Confidential, Secret)
    | +-- Compliance Requirements (GDPR, PCI-DSS, ISMS)
    | +-- Security Risk Assessment
    | Output: Security Requirements Specification
    =====================
              |
              v
    [ DESIGN PHASE ]
    ================
    | Security Activities:
    | +-- Threat Modeling (STRIDE, DREAD)
    | +-- Attack Surface Analysis
    | +-- Security Architecture Review
    | +-- Cryptographic Design
    | Output: Threat Modeling Report, Secure Design Documents
    ================
              |
              v
    [ IMPLEMENTATION PHASE ]
    =======================
    | Security Activities:
    | +-- Secure Coding Standards (OWASP)
    | +-- Input Validation
    | +-- Output Encoding
    | +-- SAST (Static Application Security Testing)
    | +-- Code Review (Security Focus)
    | Output: Secure Source Code, SAST Report
    =======================
              |
              v
    [ VERIFICATION PHASE ]
    =====================
    | Security Activities:
    | +-- DAST (Dynamic Application Security Testing)
    | +-- Penetration Testing
    | +-- Fuzz Testing
    | +-- Security Code Review
    | +-- SCA (Software Composition Analysis)
    | Output: Security Test Report, Vulnerability List
    =====================
              |
              v
    [ RELEASE PHASE ]
    ================
    | Security Activities:
    | +-- Final Security Review (FSR)
    | +-- Vulnerability Scanning (Container, VM)
    | +-- Configuration Hardening
    | +-- Security Incident Response Plan
    | Output: Release Approval, Security Checklist
    ================
              |
              v
    [ RESPONSE PHASE ]
    =================
    | Security Activities:
    | +-- Security Monitoring (SIEM)
    | +-- Incident Response
    | +-- Vulnerability Management
    | +-- Security Updates/Patching
    | Output: Security Logs, Incident Reports
    =================

    FEEDBACK LOOP: Lessons Learned --> Requirements Phase

================================================================================
```

### 3. 심층 동작 원리: 위협 모델링 (STRIDE)

```text
[STRIDE 위협 모델링]

위협 유형    의미                    예시                    완화 대책
========    =====                   ====                    ========
S - Spoofing  신분 위장              로그인 우회, IP 위조     인증 (Authentication)
T - Tampering 데이터 변조            SQL Injection, 파일 변조 무결성 (Integrity)
R - Repudiation 부인                로그 삭제, 거래 부인     부인 방지 (Non-repudiation)
I - Info       정보 노출              데이터 유출, 로그 노출   기밀성 (Confidentiality)
    Disclosure
D - DoS        서비스 거부            DDoS, 리소스 고갈       가용성 (Availability)
E - Elevation  권한 상승              일반 사용자→관리자      인가 (Authorization)
    of Privilege

[위협 모델링 프로세스]

1. 대상 시스템 분해
   - DFD(Data Flow Diagram) 작성
   - 신뢰 경계(Trust Boundary) 식별

2. 위협 식별
   - 각 데이터 흐름/처리에 STRIDE 적용
   - "여기서 위장(S)이 가능한가?"

3. 위협 평가
   - DREAD 점수 계산
   - Damage + Reproducibility + Exploitability + Affected users + Discoverability

4. 완화 전략 수립
   - 기술적 대책 (암호화, 인증 등)
   - 프로세스 대책 (감사, 교육 등)
```

### 4. 실무 코드 예시: 시큐어 코딩

```python
"""
시큐어 코딩 예시: 사용자 입력 처리
OWASP Top 10 방어: Injection, XSS, Broken Authentication
"""

import bcrypt
import re
from functools import wraps
from flask import request, jsonify
from typing import Optional

# ============== 입력값 검증 (Input Validation) ==============

class InputValidator:
    """보안 입력값 검증 클래스"""

    # 화이트리스트 패턴 (허용된 형식만)
    PATTERNS = {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'username': r'^[a-zA-Z0-9_-]{3,20}$',
        'password': r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
        'phone': r'^01[0-9]-?[0-9]{4}-?[0-9]{4}$',
    }

    @classmethod
    def validate(cls, input_type: str, value: str) -> tuple[bool, str]:
        """입력값 검증 (화이트리스트 방식)"""
        if input_type not in cls.PATTERNS:
            return False, f"알 수 없는 입력 유형: {input_type}"

        pattern = cls.PATTERNS[input_type]
        if re.match(pattern, value):
            return True, "유효한 입력값"

        return False, f"유효하지 않은 {input_type} 형식"

    @classmethod
    def sanitize_html(cls, value: str) -> str:
        """HTML 특수문자 이스케이프 (XSS 방어)"""
        return (value
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#x27;'))


# ============== SQL Injection 방어 ==============

# 잘못된 예 (취약점 있음)
def get_user_unsafe(username: str):
    # SQL Injection 취약!
    query = f"SELECT * FROM users WHERE username = '{username}'"
    # ' OR '1'='1 입력 시 모든 사용자 노출

# 올바른 예 (Parameterized Query)
def get_user_safe(db, username: str) -> Optional[dict]:
    """Parameterized Query를 사용한 SQL Injection 방어"""
    query = "SELECT id, username, email FROM users WHERE username = ?"
    cursor = db.execute(query, (username,))
    return cursor.fetchone()


# ============== 비밀번호 보안 ==============

class PasswordManager:
    """비밀번호 안전 저장 및 검증 (OWASP 권장)"""

    # bcrypt 사용 (PBKDF2, Argon2도 권장)
    ROUNDS = 12  # 연산 복잡도 (2^12)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """비밀번호 해싱 (솔트 포함)"""
        # 입력값 검증
        is_valid, msg = InputValidator.validate('password', password)
        if not is_valid:
            raise ValueError(msg)

        # bcrypt로 해싱 (자동으로 솔트 생성)
        salt = bcrypt.gensalt(rounds=cls.ROUNDS)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @classmethod
    def verify_password(cls, password: str, hashed: str) -> bool:
        """비밀번호 검증"""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                hashed.encode('utf-8')
            )
        except Exception:
            return False


# ============== 인증/인가 보안 ==============

def require_auth(f):
    """인증 데코레이터"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': '인증 토큰이 없습니다'}), 401

        # JWT 검증 (예시)
        try:
            payload = verify_jwt_token(token.replace('Bearer ', ''))
            request.current_user = payload
        except InvalidTokenError:
            return jsonify({'error': '유효하지 않은 토큰'}), 401

        return f(*args, **kwargs)
    return decorated_function


def require_role(role: str):
    """역할 기반 접근 제어 (RBAC)"""
    def decorator(f):
        @wraps(f)
        @require_auth
        def decorated_function(*args, **kwargs):
            user_role = request.current_user.get('role')

            if user_role != role and user_role != 'admin':
                return jsonify({'error': '권한이 없습니다'}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ============== 로깅 및 감사 ==============

import logging
from datetime import datetime

class SecurityLogger:
    """보안 이벤트 로깅"""

    def __init__(self):
        self.logger = logging.getLogger('security')
        self.logger.setLevel(logging.INFO)

    def log_authentication(self, username: str, success: bool, ip: str):
        """인증 시도 로깅"""
        status = "SUCCESS" if success else "FAILURE"
        self.logger.info(
            f"[AUTH] {status} | user={username} | ip={ip} | time={datetime.now()}"
        )

    def log_authorization(self, user: str, resource: str, granted: bool):
        """인가 결정 로깅"""
        status = "GRANTED" if granted else "DENIED"
        self.logger.warning(
            f"[AUTHZ] {status} | user={user} | resource={resource}"
        )

    def log_sensitive_data_access(self, user: str, data_type: str, action: str):
        """민감 데이터 접근 로깅"""
        self.logger.critical(
            f"[DATA] {action} | user={user} | data_type={data_type}"
        )
```

### 5. 보안 테스트 도구 체계

| 테스트 유형 | 도구 | 탐지 대상 | CI/CD 통합 |
| :--- | :--- | :--- | :--- |
| **SAST** | SonarQube, Semgrep, Checkmarx | 소스코드 취약점 | 커밋 시 |
| **DAST** | OWASP ZAP, Burp Suite | 런타임 취약점 | 스테이징 배포 시 |
| **SCA** | Snyk, Dependabot, OWASP Dependency-Check | 라이브러리 취약점 | 빌드 시 |
| **IaC 스캔** | Checkov, tfsec, KICS | 인프라 구성 오류 | PR 시 |
| **컨테이너 스캔** | Trivy, Clair, Anchore | 이미지 취약점 | 빌드 시 |
| **비밀 스캔** | GitLeaks, truffleHog | 하드코딩된 비밀 | 커밋 시 |

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: SDL vs OWASP SAMM vs BSIMM

| 비교 항목 | Microsoft SDL | OWASP SAMM | BSIMM |
| :--- | :--- | :--- | :--- |
| **개발자** | Microsoft | OWASP | Cigital/Synopsys |
| **성격** | 규범적(Prescriptive) | 성숙도 모델 | 실증적(Descriptive) |
| **구조** | 7단계 활동 | 4영역 12실천 | 4영역 112활동 |
| **적용 대상** | Microsoft 제품 | 모든 조직 | 성숙도 비교 |
| **특징** | 구체적 가이드 | 로드맵 제공 | 벤치마킹 |

### 2. 과목 융합 관점 분석

#### 시큐어 SDLC + DevOps (DevSecOps)

```text
[DevSecOps 파이프라인에 보안 내장]

    [CODE]       [BUILD]       [TEST]       [RELEASE]      [DEPLOY]
       |            |             |             |             |
       v            v             v             v             v
   +--------+   +--------+   +----------+   +---------+   +--------+
   | GitLeaks   | SAST    |   | DAST     |   | Container|   | RASP  |
   | 비밀스캔   | 정적분석 |   | 동적분석 |   | Scan     |   | 런타임|
   +--------+   +--------+   +----------+   +---------+   +--------+
       |            |             |             |             |
       v            v             v             v             v
   +--------+   +--------+   +----------+   +---------+   +--------+
   | SCA    |   | SCA    |   | Pen      |   | Config  |   | SIEM  |
   | 의존성 |   | 빌드   |   | Test     |   | Audit   |   | 모니터|
   +--------+   +--------+   +----------+   +---------+   +--------+

   Quality Gate: 보안 이슈 Critical이면 파이프라인 중단

[Shift-Left Security]
- 보안 테스트를 개발 초기(왼쪽)로 이동
- "코드 커밋 = 보안 검사 시작"
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오

**[시나리오] 금융 앱 개발 시 시큐어 SDLC 적용**
*   **규제 요구사항**: 전자금융감독규정, ISMS-P 인증
*   **적용 활동**:
    1. 요구사항: 금융감독원 47개 보안 약점 반영
    2. 설계: STRIDE 위협 모델링, 암호화 설계
    3. 구현: 시큐어 코딩 가이드 준수, 정적 분석
    4. 테스트: 모의 해킹, DAST
    5. 배포: 취약점 스캔 후 배포 승인

### 2. 주의사항

*   **보안 vs 개발 속도**: 보안 활동이 개발을 지연시키지 않도록 자동화 필수
*   **오탐지(False Positive)**: 도구가 너무 민감하면 개발자 무시
    → 오탐지 튜닝, True Positive 우선 해결
*   **보안 교육 부재**: 개발자가 보안 지식 없으면 시큐어 코딩 불가
    → 정기적 보안 교육, CTF 참여 권장

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### ※ 참고 표준/가이드
*   **Microsoft SDL**: Microsoft Security Development Lifecycle
*   **OWASP SAMM**: Software Assurance Maturity Model
*   **BSIMM**: Building Security In Maturity Model
*   **NIST SP 800-64**: Security Considerations in SDLC
*   **행정안전부 가이드**: 소프트웨어 개발보안 가이드 (47개 보안약점)

---

## 📌 관련 개념 맵 (Knowledge Graph)
*   [DevSecOps](@/studynotes/04_software_engineering/01_sdlc/devops.md) : 시큐어 SDLC의 DevOps 확장
*   [OWASP Top 10](@/studynotes/04_software_engineering/07_security/_index.md) : 주요 웹 취약점
*   [소프트웨어 테스팅](@/studynotes/04_software_engineering/02_quality/software_testing.md) : 보안 테스트 기법
*   [CMMI](@/studynotes/04_software_engineering/01_sdlc/cmmi.md) : 프로세스 성숙도

---

## 👶 어린이를 위한 3줄 비유 설명
1. **문제**: 집을 다 지어놓고 나서 "문이 없어서 도둑이 들어와!"라고 발견하면 큰일이에요.
2. **해결(시큐어 SDLC)**: 집을 짓기 전부터 "문은 어디에? 자물쇠는 어떤 거? 창문은 잠기는 거?"를 생각해요. 설계도에 이미 문이 있어요!
3. **효과**: 집이 완성되었을 때 이미 안전해요. 나중에 "문을 뚫어야 해"라고 안 해도 돼요!
