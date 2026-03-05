+++
title = "인증성 (Authenticity)"
date = "2026-03-04"
[extra]
categories = "studynotes-09_security"
+++

# 인증성 (Authenticity)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터, 시스템, 사용자의 신원이나 출처가 진짜임을 보증하는 정보보안 속성으로, 위조와 사칭을 방지하고 신뢰 관계를 형성합니다.
> 2. **가치**: 전자상거래의 거래 신뢰, 디지털 문서의 법적 효력, 시스템 접근의 정당성 보장을 통해 디지털 경제의 기반을 형성합니다.
> 3. **융합**: PKI, 생체인식, FIDO2, 전자서명, 블록체인 등 다양한 기술이 결합된 다층 인증 체계의 핵심 목표입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**인증성(Authenticity)**은 주장된 신원이나 출처가 실제와 일치함을 보증하는 보안 속성입니다. 이는 단순한 "신원 확인"을 넘어, 데이터의 출처, 시스템의 정품성, 사용자의 실체를 암호학적, 절차적으로 검증하는 포괄적 개념입니다.

**ISO 27000 정의**:
> "실체가 식별된 바와 같다는 특성이 입증됨을 보장하는 속성"

**인증성의 핵심 요소**:
- **신원 인증 (Identification)**: "누구인가?"
- **출처 인증 (Origin Authentication)**: "어디서 왔는가?"
- **데이터 인증 (Data Authentication)**: "내용이 진짜인가?"
- **시스템 인증 (System Authentication)**: "장치가 신뢰 가능한가?"

#### 2. 💡 비유를 통한 이해
인증성은 **'여권과 비자'**에 비유할 수 있습니다.
- **여권**: 신원 증명 - 사용자 인증
- **입국 도장**: 출입 기록 - 타임스탬프
- **홀로그램**: 위조 방지 - 전자서명
- **생체 정보**: 소지자 확인 - 생체 인식

#### 3. 등장 배경 및 발전 과정
1. **고대 봉인**: 왕의 인장, 밀랍 봉인으로 문서 진위 확인
2. **전신 시대**: 모스 부호, 전화 통화에서 상대 확인
3. **디지털 서명**: 1976년 Diffie-Hellman, 1977년 RSA
4. **PKI 구축**: 1990년대 인증기관(CA) 체계 확립
5. **생체 인식**: 지문, 홍채, 안면 인식 기술 발전
6. **FIDO/Passkey**: 2013년 FIDO 얼라이언스, 패스워드 없는 인증

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 인증 기술 체계 (표)

| 인증 요소 | 기술 | 보안 강도 | 편의성 | 비용 | 용도 |
|:---|:---|:---|:---|:---|:---|
| **지식 기반** | 비밀번호, PIN | 낮음~중간 | 중간 | 낮음 | 일반 인증 |
| **소유 기반** | OTP, 스마트카드 | 중간~높음 | 중간 | 중간 | 2FA |
| **특성 기반** | 지문, 홍채, 안면 | 높음 | 높음 | 높음 | 생체 인증 |
| **위치 기반** | GPS, IP 지오로케이션 | 낮음 | 높음 | 낮음 | 보조 인증 |
| **행위 기반** | 행동 패턴, 타이핑 | 중간 | 높음 | 중간 | 지속 인증 |
| **디지털 서명** | RSA, ECDSA | 매우 높음 | 중간 | 중간 | 데이터 인증 |

#### 2. 인증 아키텍처 다이어그램

```text
<<< Multi-Factor Authentication Architecture >>>

    +----------------------------------------------------------+
    |                    인증 요청 (Auth Request)               |
    +----------------------------------------------------------+
                                │
                                v
    +----------------------------------------------------------+
    |                    인증 게이트웨이 (Auth Gateway)          |
    |  +----------------------------------------------------+  |
    |  |                인증 요소 수집 (Factor Collection)    |  |
    |  |                                                    |  |
    |  |  ┌─────────┐  ┌─────────┐  ┌─────────┐            |  |
    |  |  │ 지식    │  │ 소유    │  │ 특성    │            |  |
    |  |  │Password │  │ OTP     │  │Biometric│            |  |
    |  |  │  PIN    │  │ Token   │  │ Fingerprint           |  |
    |  |  └────┬────┘  └────┬────┘  └────┬────┘            |  |
    |  |       │            │            │                  |  |
    |  +-------|------------|------------|------------------+  |
    |          │            │            │                     |
    |          v            v            v                     |
    |  +----------------------------------------------------+  |
    |  |                인증 정책 엔진 (Policy Engine)       |  |
    |  |                                                    |  |
    |  |  Risk Score = f(User, Device, Location, Behavior)  |  |
    |  |                                                    |  |
    |  |  ┌─────────────────────────────────────────────┐   |  |
    |  |  │ Risk < 30: Single Factor OK                  │   |  |
    |  |  │ Risk 30-70: MFA Required                     │   |  |
    |  |  │ Risk > 70: Step-up Auth / Deny               │   |  |
    |  |  └─────────────────────────────────────────────┘   |  |
    |  +----------------------------------------------------+  |
    |                                │                         |
    +--------------------------------|-------------------------+
                                     │
                                     v
    +----------------------------------------------------------+
    |                    신원 공급자 (Identity Provider)         |
    |  +----------------------------------------------------+  |
    |  |                사용자 디렉터리 (User Directory)     |  |
    |  |  - LDAP / Active Directory / Azure AD / Okta       |  |
    |  +----------------------------------------------------+  |
    |  +----------------------------------------------------+  |
    |  |                인증 메커니즘 (Auth Mechanism)       |  |
    |  |  - Password Hash Verification (bcrypt, Argon2)     |  |
    |  |  - TOTP/HOTP Validation (RFC 6238/4226)            |  |
    |  |  - FIDO2/WebAuthn Assertion Verification           |  |
    |  |  - Certificate Validation (X.509, OCSP)            |  |
    |  +----------------------------------------------------+  |
    |                                │                         |
    +--------------------------------|-------------------------+
                                     │
                                     v
    +----------------------------------------------------------+
    |                    토큰 발급 (Token Issuance)             |
    |  +----------------------------------------------------+  |
    |  |  ┌─────────┐  ┌─────────┐  ┌─────────┐            |  |
    |  |  │Session  │  │  JWT    │  │ SAML    │            |  |
    |  |  │ Cookie  │  │ Access  │  │ Assertn │            |  |
    |  |  │         │  │ Token   │  │         │            |  |
    |  |  └─────────┘  └─────────┘  └─────────┘            |  |
    |  +----------------------------------------------------+  |
    +----------------------------------------------------------+

<<< FIDO2/WebAuthn 인증 흐름 >>>

    [Client Device]                    [Server (Relying Party)]
         │                                      │
         │  1. 인증 요청                        │
         │ ─────────────────────────────────────>│
         │                                      │
         │  2. Challenge + Credential Options   │
         │ <─────────────────────────────────────│
         │                                      │
         │  3. 사용자 생체/핀 입력               │
         │  ┌─────────────────────────────┐     │
         │  │ Authenticator (TPM/SE)      │     │
         │  │ - Private Key 사용          │     │
         │  │ - Challenge 서명            │     │
         │  │ - Counter 증가              │     │
         │  └─────────────────────────────┘     │
         │                                      │
         │  4. Assertion (Signature + Counter)  │
         │ ─────────────────────────────────────>│
         │                                      │
         │                    ┌─────────────────┤
         │                    │ 5. 검증         │
         │                    │ - 서명 검증     │
         │                    │ - Counter 확인  │
         │                    │ - Origin 검증   │
         │                    └─────────────────┤
         │                                      │
         │  6. 인증 성공 / 실패                 │
         │ <─────────────────────────────────────│
         │                                      │
```

#### 3. 심층 동작 원리: 다요소 인증 구현

```python
import hashlib
import hmac
import time
import struct
import secrets
from dataclasses import dataclass
from typing import Optional, Tuple, List
from enum import Enum
from abc import ABC, abstractmethod

class AuthFactorType(Enum):
    PASSWORD = "password"
    OTP = "otp"
    BIOMETRIC = "biometric"
    CERTIFICATE = "certificate"
    FIDO2 = "fido2"

@dataclass
class AuthResult:
    success: bool
    factor_type: AuthFactorType
    confidence_score: float  # 0.0 ~ 1.0
    message: str
    session_id: Optional[str] = None

class AuthFactor(ABC):
    """인증 요소 추상 클래스"""
    @abstractmethod
    def authenticate(self, credential: dict) -> AuthResult:
        pass

    @abstractmethod
    def get_factor_type(self) -> AuthFactorType:
        pass

class PasswordAuth(AuthFactor):
    """
    비밀번호 인증
    - bcrypt/Argon2 해시 사용
    - 솔트 적용
    - 브루트포스 방어
    """

    def __init__(self, stored_hash: str, max_attempts: int = 5):
        self.stored_hash = stored_hash
        self.max_attempts = max_attempts
        self.attempts = 0
        self.lockout_until = 0

    def authenticate(self, credential: dict) -> AuthResult:
        if time.time() < self.lockout_until:
            return AuthResult(
                success=False,
                factor_type=AuthFactorType.PASSWORD,
                confidence_score=0.0,
                message=f"Account locked until {self.lockout_until}"
            )

        password = credential.get('password', '')

        # 실제 구현에서는 bcrypt.checkpw() 또는 argon2.verify() 사용
        computed_hash = self._hash_password(password)

        if hmac.compare_digest(computed_hash, self.stored_hash):
            self.attempts = 0  # 성공 시 리셋
            return AuthResult(
                success=True,
                factor_type=AuthFactorType.PASSWORD,
                confidence_score=0.7,  # 비밀번호만으로는 중간 신뢰도
                message="Password verified"
            )
        else:
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                self.lockout_until = time.time() + 300  # 5분 잠금

            return AuthResult(
                success=False,
                factor_type=AuthFactorType.PASSWORD,
                confidence_score=0.0,
                message="Invalid password"
            )

    def _hash_password(self, password: str) -> str:
        """비밀번호 해시 (시뮬레이션)"""
        # 실제로는 bcrypt.hashpw() 사용
        return hashlib.sha256(password.encode()).hexdigest()

    def get_factor_type(self) -> AuthFactorType:
        return AuthFactorType.PASSWORD

class TOTPAuth(AuthFactor):
    """
    TOTP (Time-based One-Time Password) 인증
    - RFC 6238 준수
    - 30초 윈도우
    - 6자리 코드
    """

    def __init__(self, secret: bytes, digits: int = 6, period: int = 30):
        self.secret = secret
        self.digits = digits
        self.period = period
        self.used_codes = set()  # 리플레이 공격 방지

    def authenticate(self, credential: dict) -> AuthResult:
        code = credential.get('code', '')

        # 이미 사용된 코드 확인
        if code in self.used_codes:
            return AuthResult(
                success=False,
                factor_type=AuthFactorType.OTP,
                confidence_score=0.0,
                message="Code already used"
            )

        # 현재, 이전, 다음 윈도우 허용 (시계 오차 대응)
        current_time = int(time.time())
        valid = False

        for offset in [-1, 0, 1]:  # 90초 윈도우
            counter = (current_time // self.period) + offset
            expected_code = self._generate_totp(counter)
            if hmac.compare_digest(code, expected_code):
                valid = True
                break

        if valid:
            self.used_codes.add(code)
            # 오래된 코드 정리
            self._cleanup_used_codes(current_time)

            return AuthResult(
                success=True,
                factor_type=AuthFactorType.OTP,
                confidence_score=0.85,
                message="TOTP verified"
            )
        else:
            return AuthResult(
                success=False,
                factor_type=AuthFactorType.OTP,
                confidence_score=0.0,
                message="Invalid or expired code"
            )

    def _generate_totp(self, counter: int) -> str:
        """TOTP 코드 생성"""
        # HMAC-SHA1 사용
        counter_bytes = struct.pack('>Q', counter)
        hmac_digest = hmac.new(self.secret, counter_bytes, hashlib.sha1).digest()

        # 동적 잘림 (Dynamic Truncation)
        offset = hmac_digest[-1] & 0x0F
        code = struct.unpack('>I', hmac_digest[offset:offset+4])[0]
        code = code & 0x7FFFFFFF  # 최상위 비트 제거
        code = code % (10 ** self.digits)

        return str(code).zfill(self.digits)

    def _cleanup_used_codes(self, current_time: int):
        """오래된 사용된 코드 정리"""
        # 실제로는 타임스탬프와 함께 저장하여 정리
        if len(self.used_codes) > 100:
            self.used_codes = set(list(self.used_codes)[-50:])

    def get_factor_type(self) -> AuthFactorType:
        return AuthFactorType.OTP

    def get_provisioning_uri(self, account: str, issuer: str) -> str:
        """Google Authenticator 등록용 URI 생성"""
        import base64
        secret_b32 = base64.b32encode(self.secret).decode('utf-8').rstrip('=')
        return f"otpauth://totp/{issuer}:{account}?secret={secret_b32}&issuer={issuer}&digits={self.digits}&period={self.period}"

class BiometricAuth(AuthFactor):
    """
    생체 인증 시뮬레이션
    - 지문, 홍채, 안면 인식
    - FAR/FRR 고려
    - 템플릿 보호
    """

    def __init__(self,
                 stored_template: bytes,
                 threshold: float = 0.85,
                 far: float = 0.0001,  # False Acceptance Rate
                 frr: float = 0.01):    # False Rejection Rate
        self.stored_template = stored_template
        self.threshold = threshold
        self.far = far
        self.frr = frr

    def authenticate(self, credential: dict) -> AuthResult:
        captured_template = credential.get('template')

        if captured_template is None:
            return AuthResult(
                success=False,
                factor_type=AuthFactorType.BIOMETRIC,
                confidence_score=0.0,
                message="No biometric data provided"
            )

        # 유사도 계산 (실제로는 전문 매칭 알고리즘 사용)
        similarity = self._calculate_similarity(captured_template)

        if similarity >= self.threshold:
            # 생체 인증은 높은 신뢰도
            confidence = min(0.95, similarity + 0.1)
            return AuthResult(
                success=True,
                factor_type=AuthFactorType.BIOMETRIC,
                confidence_score=confidence,
                message=f"Biometric match: {similarity:.2%}"
            )
        else:
            return AuthResult(
                success=False,
                factor_type=AuthFactorType.BIOMETRIC,
                confidence_score=similarity,
                message=f"Biometric mismatch: {similarity:.2%}"
            )

    def _calculate_similarity(self, template: bytes) -> float:
        """템플릿 유사도 계산 (시뮬레이션)"""
        # 실제로는 특징점 매칭 알고리즘 사용
        if len(template) != len(self.stored_template):
            return 0.0

        matching_bytes = sum(
            1 for a, b in zip(template, self.stored_template) if a == b
        )
        return matching_bytes / len(template)

    def get_factor_type(self) -> AuthFactorType:
        return AuthFactorType.BIOMETRIC

class MultiFactorAuth:
    """
    다요소 인증 오케스트레이션
    - 위험 기반 인증
    - 단계별 인증
    - 적응형 인증
    """

    def __init__(self):
        self.auth_factors: List[AuthFactor] = []
        self.risk_thresholds = {
            'low': {'min_score': 0.8, 'factors_required': 1},
            'medium': {'min_score': 0.9, 'factors_required': 2},
            'high': {'min_score': 0.95, 'factors_required': 3}
        }

    def register_factor(self, factor: AuthFactor):
        """인증 요소 등록"""
        self.auth_factors.append(factor)

    def authenticate(self,
                     credentials: dict,
                     risk_level: str = 'medium',
                     require_different_factors: bool = True) -> AuthResult:
        """
        다요소 인증 수행
        """
        config = self.risk_thresholds.get(risk_level, self.risk_thresholds['medium'])
        min_score = config['min_score']
        factors_required = config['factors_required']

        results = []
        passed_factors = 0
        total_confidence = 0.0
        used_factor_types = set()

        for factor in self.auth_factors:
            factor_type = factor.get_factor_type()

            # 해당 요소의 credential이 있는지 확인
            if factor_type.value in credentials:
                result = factor.authenticate(credentials[factor_type.value])
                results.append(result)

                if result.success:
                    # 다른 유형의 요소만 카운트
                    if require_different_factors:
                        if factor_type not in used_factor_types:
                            passed_factors += 1
                            used_factor_types.add(factor_type)
                            total_confidence += result.confidence_score
                    else:
                        passed_factors += 1
                        total_confidence += result.confidence_score

        # 평균 신뢰도 계산
        avg_confidence = total_confidence / passed_factors if passed_factors > 0 else 0

        # 최종 판정
        if passed_factors >= factors_required and avg_confidence >= min_score:
            return AuthResult(
                success=True,
                factor_type=list(used_factor_types)[0] if used_factor_types else AuthFactorType.PASSWORD,
                confidence_score=avg_confidence,
                message=f"Authenticated with {passed_factors} factors",
                session_id=secrets.token_hex(16)
            )
        else:
            return AuthResult(
                success=False,
                factor_type=AuthFactorType.PASSWORD,
                confidence_score=avg_confidence,
                message=f"Insufficient authentication. Required: {factors_required}, Passed: {passed_factors}"
            )

    def step_up_auth(self,
                     current_session: dict,
                     additional_credentials: dict) -> AuthResult:
        """
        단계적 인증 (Step-up Authentication)
        민감한 작업에 대한 추가 인증
        """
        # 이미 인증된 요소 확인
        authenticated_factors = current_session.get('authenticated_factors', [])

        # 추가 인증 요소에 대한 검증
        for factor in self.auth_factors:
            factor_type = factor.get_factor_type()
            if (factor_type.value in additional_credentials and
                factor_type not in authenticated_factors):
                result = factor.authenticate(additional_credentials[factor_type.value])
                if result.success:
                    return AuthResult(
                        success=True,
                        factor_type=factor_type,
                        confidence_score=result.confidence_score,
                        message="Step-up authentication successful",
                        session_id=current_session.get('session_id')
                    )

        return AuthResult(
            success=False,
            factor_type=AuthFactorType.PASSWORD,
            confidence_score=0.0,
            message="Step-up authentication failed"
        )


class AuthenticityVerifier:
    """
    데이터/시스템 진위성 검증
    - 디지털 서명 검증
    - 인증서 검증
    - 출처 인증
    """

    @staticmethod
    def verify_digital_signature(data: bytes,
                                  signature: bytes,
                                  public_key: bytes,
                                  algorithm: str = 'SHA256withRSA') -> Tuple[bool, str]:
        """
        디지털 서명 검증
        - 데이터 무결성
        - 서명자 인증
        - 부인방지
        """
        # 실제 구현에서는 cryptography 라이브러리 사용
        # 시뮬레이션
        expected_sig = hmac.new(public_key, data, hashlib.sha256).digest()

        if hmac.compare_digest(signature, expected_sig):
            return True, "Signature valid - authenticity confirmed"
        else:
            return False, "Signature invalid - authenticity cannot be verified"

    @staticmethod
    def verify_certificate(cert_pem: str,
                          ca_cert_pem: str,
                          revocation_check: bool = True) -> Tuple[bool, str]:
        """
        X.509 인증서 검증
        - 서명 검증
        - 유효기간 확인
        - 폐지 상태 확인 (CRL/OCSP)
        """
        # 실제 구현에서는 openssl/cryptography 사용
        # 시뮬레이션
        return True, "Certificate valid and trusted"

    @staticmethod
    def verify_message_origin(message: dict,
                              expected_sender: str,
                              hmac_key: bytes) -> Tuple[bool, str]:
        """
        메시지 출처 인증
        - HMAC 기반
        - 메시지 변조 방지
        """
        import json

        if 'hmac' not in message:
            return False, "No HMAC provided"

        received_hmac = message['hmac']
        message_copy = {k: v for k, v in message.items() if k != 'hmac'}
        message_bytes = json.dumps(message_copy, sort_keys=True).encode()

        expected_hmac = hmac.new(hmac_key, message_bytes, hashlib.sha256).hexdigest()

        if hmac.compare_digest(received_hmac, expected_hmac):
            return True, f"Message origin verified: {expected_sender}"
        else:
            return False, "HMAC mismatch - origin cannot be verified"


# 사용 예시
if __name__ == "__main__":
    # 1. 다요소 인증 설정
    mfa = MultiFactorAuth()

    # 비밀번호 요소
    password_auth = PasswordAuth(stored_hash="dummy_hash")
    mfa.register_factor(password_auth)

    # TOTP 요소
    totp_secret = secrets.token_bytes(20)
    totp_auth = TOTPAuth(secret=totp_secret)
    mfa.register_factor(totp_auth)

    # 생체 인증 요소
    biometric_auth = BiometricAuth(stored_template=secrets.token_bytes(64))
    mfa.register_factor(biometric_auth)

    # 2. 저위험 인증 (단일 요소)
    print("=== Low Risk Authentication ===")
    result = mfa.authenticate(
        credentials={'password': {'password': 'test123'}},
        risk_level='low'
    )
    print(f"Result: {result.message}")

    # 3. 고위험 인증 (다중 요소)
    print("\n=== High Risk Authentication ===")
    # TOTP 코드 생성
    current_totp = totp_auth._generate_totp(int(time.time()) // 30)

    result = mfa.authenticate(
        credentials={
            'password': {'password': 'test123'},
            'otp': {'code': current_totp},
            'biometric': {'template': biometric_auth.stored_template}
        },
        risk_level='high'
    )
    print(f"Result: {result.message}")
    print(f"Session ID: {result.session_id}")
