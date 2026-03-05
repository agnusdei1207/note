+++
title = "OWASP Top 10 (2021)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# OWASP Top 10 (2021)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Open Worldwide Application Security Project가 2021년 발표한 웹 애플리케이션 보안 위협 TOP 10으로, 업계 데이터, 설문조사, 전문가 합의를 통해 3년마다 갱신되는 웹 보안의 핵심 지침서입니다.
> 2. **가치**: 개발/보안/경영진의 공통 언어, 보안 투자 우선순위, 규정 준수(PCI DSS)의 기준점으로, "알면 막을 수 있다"는 실용적 가이드를 제공합니다.
> 3. **융합**: DevSecOps의 품질 게이트, SAST/DAST/WAF 탐지 규칙, 보안 교육 커리큘럼, ASVS 검증 표준의 기반이 됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. OWASP Top 10 (2021) 목록

| 순위 | 코드 | 명칭 | 설명 |
|:---:|:---|:---|:---|
| **A01** | A01:2021 | Broken Access Control | 접근 제어 실패 |
| **A02** | A02:2021 | Cryptographic Failures | 암호화 실패 |
| **A03** | A03:2021 | Injection | 인젝션 |
| **A04** | A04:2021 | Insecure Design | 안전하지 않은 설계 |
| **A05** | A05:2021 | Security Misconfiguration | 보안 설정 오류 |
| **A06** | A06:2021 | Vulnerable Components | 취약한 컴포넌트 |
| **A07** | A07:2021 | Auth Failures | 인증/식별 실패 |
| **A08** | A08:2021 | Software Integrity | 소프트웨어 무결성 실패 |
| **A09** | A09:2021 | Logging Failures | 로깅/모니터링 실패 |
| **A10** | A10:2021 | SSRF | 서버 사이드 요청 위조 |

#### 2. 2017 vs 2021 변화

| 2017 | 2021 | 변화 |
|:---|:---|:---|
| A1 Injection | A03 Injection | 순위 하락 |
| A2 Broken Auth | A07 Auth Failures | 분리/확장 |
| A3 Sensitive Data | A02 Crypto Failures | 명칭 변경 |
| A4 XXE | A05 Misconfiguration (통합) | 하위 카테고리 |
| A5 Broken Access | A01 Broken Access | 1위로 상승! |
| A6 Security Misconfig | A05 Misconfiguration | |
| A7 XSS | A03 Injection (통합) | 하위 카테고리 |
| A8 Insecure Deserialization | A08 Software Integrity | 확장 |
| A9 Known Vulnerabilities | A06 Vulnerable Components | |
| A10 Insufficient Logging | A09 Logging Failures | |

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. A01:2021 - Broken Access Control (접근 제어 실패)

```
=== 접근 제어 실패 유형 ===

1. URL 조작
   /api/users/123 → /api/users/456 (다른 사용자 데이터)
   /admin → 비인가 관리자 페이지 접근

2. IDOR (Insecure Direct Object Reference)
   GET /orders?id=1001 → id=1002로 변경
   → 다른 사용자 주문 조회

3. 권한 상승
   일반 사용자 → 관리자 기능 수행
   POST /api/admin/users (권한 검증 없음)

4. 메타데이터 조작
   JWT role: "user" → role: "admin"
   Cookie isAdmin=false → isAdmin=true

5. CORS 오설정
   Access-Control-Allow-Origin: *
   → 모든 도메인에서 API 호출 가능

===========================================

방어 대책:

1. 서버 측 권한 검증 (절대 클라이언트 신뢰 금지)
   @RequireRole("ADMIN")
   public void deleteUser(String userId) {
       // 권한 검증은 서버에서
   }

2. 기본 거부 (Deny by Default)
   - 명시적으로 허용된 것만 접근 가능
   - 403 Forbidden 반환

3. 소유권 검증
   if (!order.getOwner().equals(currentUser)) {
       throw new AccessDeniedException();
   }

4. 세션 기반 접근 제어
   - 세션에서 사용자 ID 확인
   - 요청 파라미터로 ID 받지 않기
```

#### 2. A02:2021 - Cryptographic Failures (암호화 실패)

```
=== 암호화 실패 유형 ===

1. 전송 중 데이터 암호화 실패
   - HTTP 사용 (HTTPS 아님)
   - TLS 1.0/1.1 사용
   - 자체 서명 인증서

2. 저장 데이터 암호화 실패
   - 비밀번호 평문 저장
   - 신용카드 번호 암호화 없음
   - 개인정보 평문 DB 저장

3. 약한 암호화 알고리즘
   - MD5, SHA-1 사용
   - DES, 3DES 사용
   - ECB 모드 사용

4. 키 관리 실패
   - 하드코딩된 키
   - 기본 키 사용
   - 키 버전 관리 없음

===========================================

방어 대책:

1. 전송 암호화
   - TLS 1.2+ 강제
   - HSTS 헤더

2. 저장 암호화
   - AES-256-GCM
   - 비밀번호: Argon2id/bcrypt

3. 키 관리
   - HSM/KMS 사용
   - 키 로테이션
```

#### 3. A03:2021 - Injection (인젝션)

```
=== 인젝션 공격 유형 및 방어 ===

1. SQL Injection 방어

   취약한 패턴 (금지!):
   query = "SELECT * FROM users WHERE username = '" + username + "'"
   → ' OR '1'='1 입력 시 모든 사용자 조회

   안전한 패턴:
   query = "SELECT * FROM users WHERE username = ?"
   db.execute(query, (username,))  # 파라미터화 쿼리

   ORM 사용:
   User.objects.filter(username=username).first()


2. OS Command Injection 방어

   취약한 패턴 (금지!):
   system("ping -c 4 " + host)
   → ; rm -rf / 입력 시 시스템 삭제

   안전한 패턴:
   1) 입력 검증 (IP 또는 도메인만 허용)
   2) subprocess.run(['ping', '-c', '4', host], shell=False)
      # shell=False 필수!


3. XSS (Cross-Site Scripting) 방어

   취약한 패턴:
   return "<div>" + comment + "</div>"
   → <script>alert('XSS')</script> 입력 시 실행

   안전한 패턴:
   1) HTML 이스케이프
   2) CSP 헤더: Content-Security-Policy: default-src 'self'


4. LDAP Injection 방어

   취약한 패턴:
   filter = "(uid=" + username + ")"
   → *)(uid=*))(|(uid=* 입력 시 모든 사용자

   안전한 패턴:
   safe_username = escape_ldap(username)
   filter = "(uid=" + safe_username + ")"
```

#### 4. A04:2021 - Insecure Design (안전하지 않은 설계)

```
=== 안전하지 않은 설계 vs 보안 설계 ===

1. 인증 설계

   취약한 설계:
   - 비밀번호만으로 인증
   - 무제한 로그인 시도
   - 비밀번호 힌트 제공

   보안 설계:
   - MFA 필수
   - 계정 잠금 정책
   - 비밀번호 복구는 재설정만

2. 세션 설계

   취약한 설계:
   - 세션 ID가 URL에 노출
   - 세션 만료 없음
   - 동시 로그인 허용

   보안 설계:
   - 쿠키에 HttpOnly, Secure, SameSite
   - 30분 비활동 시 만료
   - 동시 로그인 제한

3. 권한 설계

   취약한 설계:
   - 클라이언트에서 권한 결정
   - 관리자/일반 사용자만 구분

   보안 설계:
   - 서버 측 RBAC/ABAC
   - 세분화된 권한 (리소스별)

4. 위협 모델링 필수
   - STRIDE: Spoofing, Tampering, Repudiation,
             Information disclosure, Denial of service, Elevation
   - 각 기능별 위협 식별 → 대응 설계
```

#### 5. A05:2021 - Security Misconfiguration (보안 설정 오류)

```
=== 보안 설정 오류 체크리스트 ===

1. 불필요한 기능 비활성화
   [ ] 미사용 포트 닫기
   [ ] 불필요한 서비스 제거
   [ ] 디버그 모드 비활성화

2. 기본 계정/비밀번호 변경
   [ ] admin/admin 변경
   [ ] 기본 SSH 키 교체
   [ ] 데이터베이스 기본 계정 삭제

3. 에러 메시지 최소화
   - 스택 트레이스 노출 금지
   - 일반적인 에러 메시지
   - 상세 에러는 로그만

4. 보안 헤더 설정
   [ ] X-Frame-Options: DENY
   [ ] X-Content-Type-Options: nosniff
   [ ] Content-Security-Policy
   [ ] Strict-Transport-Security

5. 파일 권한
   [ ] 웹 루트 외 중요 파일
   [ ] 설정 파일 읽기 권한 제한
   [ ] 업로드 디렉토리 실행 권한 제거
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. OWASP Top 10 매핑: 개발 단계 vs 대응

| 항목 | 설계 단계 | 개발 단계 | 테스트 단계 | 운영 단계 |
|:---|:---|:---|:---|:---|
| **A01** | RBAC 설계 | 권한 코드 리뷰 | 권한 테스트 | WAF 규칙 |
| **A02** | 암호화 요구사항 | 암호화 라이브러리 | 암호화 테스트 | 키 로테이션 |
| **A03** | 입력 검증 설계 | 파라미터화 쿼리 | 인젝션 테스트 | WAF |
| **A04** | 위협 모델링 | 보안 패턴 | 아키텍처 리뷰 | 모니터링 |
| **A05** | 보안 설정 표준 | 설정 검증 | 구성 스캔 | CSPM |

#### 2. 과목 융합 관점

**DevSecOps와 융합**
- SAST: 소스 코드 스캔
- DAST: 런타임 테스트
- SCA: 라이브러리 취약점

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오: 스타트업 OWASP Top 10 대응**
1. **1단계 (즉시)**: A06 (취약한 컴포넌트), A05 (설정 오류)
   - SCA 도구 도입 (Snyk, Dependabot)
   - 보안 헤더 설정

2. **2단계 (1개월)**: A01, A03, A07
   - 인젝션 방어 (ORM)
   - 인증 강화 (MFA)
   - 권한 검증

3. **3단계 (3개월)**: A02, A04, A08, A09, A10
   - 암호화 적용
   - 로깅/모니터링
   - 위협 모델링

#### 2. 안티패턴 (Anti-patterns)

```
취약한 접근 (금지!)

1. "내 앱은 중요하지 않아"
   - OWASP 대응 생략
   → 모든 앱이 공격 대상

2. 한 번만 검사
   - 초기 보안 테스트만
   → 지속적 검증 필요

3. 기능 우선
   - "나중에 보안 추가"
   → Security by Design 필수

올바른 접근:

1. 모든 앱 대상
   - 내부/외부 앱 모두 OWASP 대응

2. 지속적 검증
   - CI/CD에서 SAST/DAST 실행

3. Security by Design
   - 위협 모델링 → 설계 → 개발
```

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 | 항목 | 수치/내용 |
|:---|:---|:---|
| **취약점 감소** | OWASP Top 10 | 80%+ 방지 |
| **규정 준수** | PCI DSS | 6.5 요구사항 |
| **비용 절감** | 수정 비용 | 설계 단계 10x 저렴 |

#### 2. 참고 표준/가이드

| 표준 | 내용 |
|:---|:---|
| **OWASP ASVS** | Application Security Verification Standard |
| **OWASP Testing Guide** | 테스트 가이드 |
| **PCI DSS 6.5** | OWASP Top 10 대응 |

---

### 관련 개념 맵 (Knowledge Graph)
- [SQL Injection](@/studynotes/09_security/05_web/sql_injection.md) : A03 대표 예시
- [XSS](@/studynotes/09_security/05_web/xss.md) : A03 하위
- [WAF](@/studynotes/09_security/03_network/waf.md) : OWASP 방어 도구
- [접근 제어](@/studynotes/09_security/07_identity/rbac_abac.md) : A01 대응
- [암호화](@/studynotes/09_security/02_crypto/aes.md) : A02 대응

---

### 어린이를 위한 3줄 비유 설명
1. **10가지 위험**: OWASP Top 10은 인터넷에서 가장 많이 생기는 10가지 사고예요. 자전거를 탈 때 조심해야 할 10가지처럼요.
2. **미리 확인**: 사고가 나기 전에 확인하는 거예요. 자전거 브레이크가 고장 났는지 타기 전에 확인하는 것과 같아요.
3. **모두가 같이**: 전 세계 모든 웹사이트가 이 10가지를 조심해요. 그래서 더 안전한 인터넷이 돼요!
