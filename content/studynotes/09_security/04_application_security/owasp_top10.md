+++
title = "OWASP Top 10 (2021)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# OWASP Top 10 (2021)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OWASP Top 10은 웹 애플리케이션의 가장 치명적인 10대 보안 취약점을 정리한 표준으로, A01~A10으로 분류되며 모든 보안 교육과 SDLC의 필수 참조입니다.
> 2. **가치**: 2021년 개정에서는 취약한 접근 제어(A01), 암호화 실패(A02), 인젝션(A03)이 상위권이며, Insecure Design(A04), SSRF(A10)가 새로 추가되었습니다.
> 3. **융합**: Security by Design, DevSecOps, SAST/DAST 도구, WAF 룰셋과 결합하여 실무에서 적용되며, PCI DSS, ISO 27001 감사의 기준이 됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. OWASP Top 10 (2021) 목록

| 순위 | 코드 | 취약점 | 위험도 |
|:---|:---|:---|:---|
| **A01** | Broken Access Control | 접근 제어 실패 | 높음 |
| **A02** | Cryptographic Failures | 암호화 실패 | 높음 |
| **A03** | Injection | 인젝션 | 높음 |
| **A04** | Insecure Design | 안전하지 않은 설계 | 높음 |
| **A05** | Security Misconfiguration | 보안 설정 오류 | 중간 |
| **A06** | Vulnerable Components | 취약한 컴포넌트 | 높음 |
| **A07** | Auth Failures | 인증 실패 | 높음 |
| **A08** | Software/Data Integrity Failures | 무결성 실패 | 중간 |
| **A09** | Logging Failures | 로깅/모니터링 실패 | 중간 |
| **A10** | SSRF | 서버 사이드 요청 위조 | 중간 |

#### 2. 2017 vs 2021 변화

| 변화 | 내용 |
|:---|:---|
| **A01 승격** | Broken Access Control이 1위로 (2017: 5위) |
| **A02 변경** | Sensitive Data Exposure → Cryptographic Failures |
| **A04 신설** | Insecure Design (새로운 카테고리) |
| **A08 신설** | Software and Data Integrity Failures |
| **A10 신설** | SSRF (Server-Side Request Forgery) |
| **삭제** | A4:2017 XML External Entities (XXE) → A05 통합 |

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. A01: Broken Access Control (접근 제어 실패)

```text
                    [ 접근 제어 실패 유형 ]

1. IDOR (Insecure Direct Object Reference)
   /api/user/123/profile → /api/user/124/profile
   (권한 없이 다른 사용자 데이터 접근)

2. 경로 순회 (Path Traversal)
   /download?file=../../../etc/passwd

3. 권한 상승 (Privilege Escalation)
   일반 사용자가 관리자 기능 실행

4. 메타데이터 조작
   hidden field, JWT claim 변조

5. CORS 오설정
   Access-Control-Allow-Origin: *

[방어]
- RBAC/ABAC 구현
- 소유권 검증 (user_id == resource.owner_id)
- 기본 거부 정책
- 감사 로그
```

#### 2. A02: Cryptographic Failures (암호화 실패)

```text
                    [ 암호화 실패 유형 ]

1. 평문 전송
   HTTP, SMTP, FTP로 민감 데이터 전송

2. 평문 저장
   비밀번호, 신용카드 평문 저장

3. 약한 알고리즘
   MD5, SHA-1, DES, RC4 사용

4. 하드코딩된 키
   소스코드에 암호화 키 포함

5. 불충분한 키 길이
   RSA-1024, AES-128 (환경에 따라)

6. 랜덤 미사용
   예측 가능한 IV, Salt, Nonce

[방어]
- TLS 1.3 필수
- AES-256-GCM, ChaCha20-Poly1305
- Argon2id 패스워드 해싱
- HSM/KMS 사용
```

#### 3. A03: Injection (인젝션)

```text
                    [ 인젝션 유형 ]

1. SQL Injection
   ' OR '1'='1' --
   SELECT * FROM users WHERE id = '' OR '1'='1' --'

2. OS Command Injection
   ; cat /etc/passwd
   ; rm -rf /

3. LDAP Injection
   *)(uid=*))(|(uid=*

4. XPath Injection
   ' or '1'='1

5. NoSQL Injection
   {"$gt": ""}

6. Template Injection (SSTI)
   {{7*7}} → 49

[방어]
- 파라미터화 쿼리 (Prepared Statement)
- ORM 사용
- 입력 검증 (Allowlist)
- 최소 권한 DB 계정
- WAF
```

#### 4. 핵심 코드: 방어 구현

```python
from dataclasses import dataclass
from typing import Optional, List
import hashlib
import secrets
import re
from functools import wraps
from flask import request, jsonify, g

# A01: 접근 제어 구현
class AccessControl:
    """접근 제어 구현"""

    @staticmethod
    def check_ownership(user_id: int, resource_user_id: int) -> bool:
        """리소스 소유권 확인"""
        return user_id == resource_user_id

    @staticmethod
    def check_permission(user_role: str, required_role: str) -> bool:
        """역할 기반 권한 확인"""
        role_hierarchy = {'guest': 0, 'user': 1, 'admin': 2, 'superadmin': 3}
        return role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 0)

def require_ownership(func):
    """소유권 검증 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        resource_id = kwargs.get('resource_id')
        # 실제로는 DB에서 리소스 조회
        # resource = db.get_resource(resource_id)
        # if resource.owner_id != g.current_user.id:
        #     return jsonify({"error": "Forbidden"}), 403
        return func(*args, **kwargs)
    return wrapper


# A02: 암호화 구현
class CryptoSecurity:
    """암호화 보안 구현"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Argon2id 패스워드 해싱 (실제로는 argon2 라이브러리)"""
        # 시뮬레이션
        salt = secrets.token_hex(16)
        # 실제: argon2.PasswordHasher().hash(password)
        return f"$argon2id${salt}${hashlib.sha256((password + salt).encode()).hexdigest()}"

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """패스워드 검증"""
        import hmac
        parts = hashed.split('$')
        if len(parts) != 4:
            return False
        salt = parts[2]
        expected = parts[3]
        computed = hashlib.sha256((password + salt).encode()).hexdigest()
        return hmac.compare_digest(computed, expected)


# A03: 인젝션 방어
class SQLInjectionDefense:
    """SQL 인젝션 방어"""

    # 파라미터화 쿼리 (安全的)
    SAFE_QUERY = """
    SELECT * FROM users
    WHERE id = %s AND status = %s
    """

    # 입력 검증
    @staticmethod
    def validate_id(user_input: str) -> Optional[int]:
        """ID 검증 (숫자만 허용)"""
        if re.match(r'^\d+$', user_input):
            return int(user_input)
        return None

    @staticmethod
    def sanitize_string(user_input: str, max_length: int = 100) -> str:
        """문자열 살균"""
        # 길이 제한
        sanitized = user_input[:max_length]
        # 위험 문자 이스케이프 (실제로는 ORM/파라미터화 사용)
        dangerous_chars = ["'", '"', ';', '--', '/*', '*/']
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized


# A05: 보안 설정
class SecurityHeaders:
    """보안 헤더 설정"""

    @staticmethod
    def get_security_headers() -> dict:
        """필수 보안 헤더"""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=()"
        }


# A07: 인증 보안
class AuthSecurity:
    """인증 보안 구현"""

    def __init__(self):
        self.failed_attempts: dict = {}
        self.max_attempts = 5
        self.lockout_duration = 300  # 5분

    def check_brute_force(self, user_id: str) -> bool:
        """무차별 대입 확인"""
        import time
        now = time.time()

        if user_id in self.failed_attempts:
            attempts, lockout_until = self.failed_attempts[user_id]

            # 잠금 중
            if lockout_until and now < lockout_until:
                return False

            # 만료된 시도 정리
            if now - attempts[0] > 3600:  # 1시간
                self.failed_attempts[user_id] = ([], None)

        return True

    def record_failed_attempt(self, user_id: str):
        """실패 시도 기록"""
        import time
        now = time.time()

        if user_id not in self.failed_attempts:
            self.failed_attempts[user_id] = ([], None)

        attempts, lockout = self.failed_attempts[user_id]
        attempts.append(now)

        # 임계값 초과 시 잠금
        if len(attempts) >= self.max_attempts:
            self.failed_attempts[user_id] = (attempts, now + self.lockout_duration)


# A10: SSRF 방어
class SSRFDefense:
    """SSRF 방어 구현"""

    PRIVATE_IP_RANGES = [
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.0.0/16",
        "127.0.0.0/8",
        "169.254.0.0/16",  # AWS 메타데이터
    ]

    ALLOWED_DOMAINS = [
        "api.example.com",
        "cdn.example.com"
    ]

    @staticmethod
    def is_private_ip(ip: str) -> bool:
        """사설 IP 확인"""
        import ipaddress
        try:
            ip_obj = ipaddress.ip_address(ip)
            for cidr in SSRFDefense.PRIVATE_IP_RANGES:
                if ip_obj in ipaddress.ip_network(cidr):
                    return True
        except:
            pass
        return False

    @staticmethod
    def validate_url(url: str) -> bool:
        """URL 검증"""
        from urllib.parse import urlparse
        import socket

        try:
            parsed = urlparse(url)

            # 스킴 확인
            if parsed.scheme not in ['http', 'https']:
                return False

            # 도메인 화이트리스트
            if parsed.hostname not in SSRFDefense.ALLOWED_DOMAINS:
                return False

            # DNS 리바인딩 방지
            ip = socket.gethostbyname(parsed.hostname)
            if SSRFDefense.is_private_ip(ip):
                return False

            return True
        except:
            return False


# 사용 예시
if __name__ == "__main__":
    print("=== OWASP Top 10 방어 예시 ===")

    # A01: 접근 제어
    print("\n[A01] 접근 제어:")
    print(f"  소유권 확인: {AccessControl.check_ownership(1, 1)}")
    print(f"  권한 확인: {AccessControl.check_permission('admin', 'user')}")

    # A02: 암호화
    print("\n[A02] 암호화:")
    hashed = CryptoSecurity.hash_password("mypassword")
    print(f"  패스워드 해시: {hashed[:50]}...")
    print(f"  검증: {CryptoSecurity.verify_password('mypassword', hashed)}")

    # A03: 인젝션
    print("\n[A03] 인젝션 방어:")
    print(f"  ID 검증: {SQLInjectionDefense.validate_id('123')}")
    print(f"  악성 입력: {SQLInjectionDefense.validate_id(\"1' OR '1'='1\")}")

    # A10: SSRF
    print("\n[A10] SSRF 방어:")
    print(f"  내부 IP: {SSRFDefense.is_private_ip('192.168.1.1')}")
    print(f"  공인 IP: {SSRFDefense.is_private_ip('8.8.8.8')}")
