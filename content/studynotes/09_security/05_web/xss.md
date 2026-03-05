+++
title = "XSS (Cross-Site Scripting)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# XSS (Cross-Site Scripting)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 공격자가 웹페이지에 악성 스크립트를 삽입하여 다른 사용자의 브라우저에서 실행시키는 취약점으로, 세션 탈취, 키로깅, 피싱, 웹사이트 변조 등의 공격이 가능합니다.
> 2. **가치**: 반사형(Reflected), 저장형(Stored), DOM 기반 세 종류가 있으며, 입력 이스케이프, CSP(Content Security Policy), HttpOnly 쿠키로 방어합니다.
> 3. **융합**: OWASP Top 10 A03의 하위 카테고리, WAF 탐지 규칙, 브라우저 XSS 필터와 결합한 다층 방어가 필요합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**XSS(Cross-Site Scripting)**는 신뢰할 수 있는 웹사이트에 악성 스크립트를 주입하여, 방문자의 브라우저에서 해당 스크립트를 실행시키는 공격입니다. 동일 출처 정책(SOP)을 우회하여 민감 정보를 탈취할 수 있습니다.

#### 2. XSS 공격 유형

| 유형 | 설명 | 영향 범위 |
|:---|:---|:---|
| **Reflected XSS** | URL 파라미터에 스크립트 포함 | 링크 클릭자 |
| **Stored XSS** | DB에 스크립트 저장 | 모든 방문자 |
| **DOM-based XSS** | 클라이언트 JS 취약 | 방문자 |

#### 3. 비유를 통한 이해
XSS는 **'게시판 스티커'**에 비유할 수 있습니다.

- **정상**: "안녕하세요!" 스티커 붙이기
- **XSS**: "이 글을 읽는 사람의 지갑을 주인에게 주세요"라는 스티커
- **결과**: 모든 방문자가 자신도 모르게 지갑을 넘김

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. XSS 공격 시나리오

**Reflected XSS 공격 과정:**
1. 공격자가 악성 URL 생성 및 피해자에게 전송
2. 피해자가 링크 클릭
3. 서버가 검색어를 응답에 포함
4. 브라우저에서 스크립트 실행
5. 쿠키가 공격자 서버로 전송

**Stored XSS 공격 과정:**
1. 공격자가 게시판에 악성 댓글 작성
2. DB에 저장됨
3. 다른 사용자가 게시글 조회
4. 모든 방문자에서 스크립트 실행

#### 2. 심층 방어 기법

**1) 출력 이스케이프 (Output Encoding)**

| 컨텍스트 | 이스케이프 방식 |
|:---|:---|
| HTML 본문 | &lt; &gt; &amp; &quot; &#x27; |
| HTML 속성 | &quot; &#x27; |
| JavaScript | 역슬래시 이스케이프 |
| URL | %XX 인코딩 |

**2) Content Security Policy (CSP)**

```
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.example.com
```

효과:
- 인라인 스크립트 실행 차단
- 외부 스크립트 출처 제한

**3) HttpOnly 쿠키**

```
Set-Cookie: sessionid=abc123; HttpOnly; Secure; SameSite=Strict
```

효과:
- JavaScript에서 document.cookie 접근 불가
- XSS로 쿠키 탈취 방지

**4) DOMPurify 라이브러리**

모든 HTML 입력은 DOMPurify로 sanitize 권장:
- 안전한 HTML만 허용
- 스크립트 태그, 이벤트 핸들러 제거

#### 3. XSS 방어 아키텍처

```
┌──────────────────────────────────────────────────────────────┐
│                     Layer 1: 입력 검증                        │
│  - 화이트리스트 허용 문자만                                    │
│  - DOMPurify로 sanitize                                       │
│                              │                               │
│                              ▼                               │
│                     Layer 2: WAF                              │
│  XSS 시그니처 탐지                                             │
│                              │                               │
│                              ▼                               │
│                Layer 3: 출력 인코딩                           │
│  - 컨텍스트별 이스케이프                                       │
│                              │                               │
│                              ▼                               │
│                  Layer 4: CSP                                 │
│  Content-Security-Policy 헤더                                  │
│                              │                               │
│                              ▼                               │
│                Layer 5: 브라우저 보호                          │
│  - HttpOnly 쿠키                                              │
│  - 브라우저 내장 XSS 필터                                      │
└──────────────────────────────────────────────────────────────┘
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. XSS vs CSRF 비교

| 특성 | XSS | CSRF |
|:---|:---|:---|
| **공격 대상** | 사용자 브라우저 | 서버 |
| **요청 출처** | 피해자 브라우저 | 공격자 페이지 |
| **인증 필요** | X | O |
| **주요 피해** | 쿠키 탈취, 키로깅 | 상태 변경 |
| **방어** | 이스케이프, CSP | CSRF 토큰 |

#### 2. 과목 융합 관점

**프론트엔드와 융합**
- React: JSX 자동 이스케이프 제공
- Vue: v-html은 위험, sanitize 필수
- Angular: DomSanitizer 제공

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 레거시 게시판 XSS 대응**
- 상황: HTML 허용 게시판, 저장형 XSS 발견
- 판단: 다층 방어 적용
- 전략:
  1. DOMPurify로 입력 sanitize
  2. CSP 헤더 추가
  3. HttpOnly 쿠키 설정

**시나리오 2: SPA 보안**
- 상황: 프론트엔드에서 동적 렌더링
- 판단: 모든 사용자 입력은 sanitize 필수
- 전략:
  1. DOMPurify 사용
  2. CSP 추가
  3. Trusted Types API 활용

#### 2. 안티패턴 (Anti-patterns)

취약한 패턴 (금지!):
1. 사용자 입력을 검증 없이 DOM에 삽입
2. CSP 없이 운영
3. HttpOnly 없는 쿠키

올바른 패턴:
1. textContent 사용 또는 DOMPurify로 sanitize
2. CSP 적용
3. HttpOnly, Secure 쿠키

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 | 항목 | 수치/내용 |
|:---|:---|:---|
| **세션 탈취 방지** | HttpOnly | 100% |
| **스크립트 실행 차단** | CSP | 95%+ |
| **규정 준수** | OWASP | A03 대응 |

#### 2. 참고 표준/가이드

| 표준 | 내용 |
|:---|:---|
| **OWASP ASVS** | V5.3.3 - XSS 방어 |
| **CWE-79** | Cross-site Scripting |
| **CSP Level 3** | W3C 표준 |

---

### 관련 개념 맵 (Knowledge Graph)
- [OWASP Top 10](@/studynotes/09_security/05_web/owasp_top10.md) : A03 Injection
- [SQL Injection](@/studynotes/09_security/05_web/sql_injection.md) : 다른 인젝션
- [CSRF](@/studynotes/09_security/05_web/csrf.md) : 관련 웹 공격
- [WAF](@/studynotes/09_security/03_network/waf.md) : XSS 탐지

---

### 어린이를 위한 3줄 비유 설명
1. **나쁜 쪽지**: XSS는 친구의 책에 몰래 나쁜 쪽지를 끼워넣는 것과 같아요. 다른 친구가 책을 보면 쪽지를 읽게 돼요.
2. **특수 잉크**: 우리는 특수 잉크로만 글을 써요. 그래야 나쁜 쪽지가 보이지 않아요. 이게 바로 '이스케이프'예요.
3. **문지기**: CSP는 문지기예요. 우리 반에서 온 쪽지만 읽을 수 있게 해요. 다른 반에서 온 나쁜 쪽지는 버려요!
