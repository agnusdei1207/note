#!/usr/bin/env python3
"""Generate security study notes 480-525"""
import os, subprocess, sys

BASE = "/Users/pf/workspace/brainscience/content/studynote/09_security/05_web_app_security"
REPO = "/Users/pf/workspace/brainscience"

def w(fname, content):
    path = os.path.join(BASE, fname)
    if os.path.exists(path):
        print(f"SKIP: {fname}")
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"CREATED: {fname}")
    return True

def commit(msg):
    subprocess.run(["git", "add", "-A"], cwd=REPO, check=True)
    subprocess.run(["git", "commit", "-m", msg,
        "--trailer", "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"],
        cwd=REPO, check=True)
    print(f"COMMITTED: {msg}")

FILES = {}

FILES["480_clickjacking.md"] = """\
+++
weight = 480
title = "480. Clickjacking (클릭재킹)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Clickjacking(UI Redressing)은 공격자가 투명한 iframe으로 합법적 페이지를 덮어 피해자가 보이지 않는 버튼을 클릭하게 만드는 시각적 기만 공격이다.
> 2. **가치**: JavaScript 취약점 없이도 피해자의 클릭 행위를 가로채 의도치 않은 작업(계좌 이체, 권한 부여 등)을 실행시킬 수 있다.
> 3. **판단 포인트**: X-Frame-Options 또는 CSP frame-ancestors 헤더로 해당 사이트가 iframe 안에 삽입될 수 없도록 차단하는 것이 핵심 방어이다.

---

## Ⅰ. 개요 및 필요성

Clickjacking은 UI Redressing 또는 Iframe Overlay Attack으로도 불린다. 공격자는 `opacity:0`으로 투명하게 처리한 대상 사이트의 iframe을 자신의 페이지 위에 올려놓는다. 피해자는 매력적인 버튼을 클릭한다고 생각하지만 실제로는 투명 iframe의 버튼(예: 구매, 이체, 친구 추가)을 클릭하게 된다.

2008년 Adobe Flash 권한 허용 버튼을 가로채는 공격이 최초 발견 사례이며, Facebook 좋아요 버튼 클릭재킹(Likejacking)이 대규모 피해를 일으키기도 했다.

📢 **섹션 요약 비유**: 투명 유리판 위에 예쁜 그림을 그려서 유리판 아래 버튼을 누르게 유도하는 마술 트릭이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 구성 요소 | 역할 | 공격자 코드 예시 |
|:---|:---|:---|
| 외부 페이지 | 클릭 유도 UI | `<div>클릭하면 경품!` |
| 투명 iframe | 실제 피해 대상 | `opacity:0; position:absolute` |
| 위치 조정 | 버튼 정렬 | `top:100px; left:200px` |

```
공격자 페이지 (피해자 화면)
┌──────────────────────────────┐
│  "여기 클릭하면 경품!"        │  ← 보이는 레이어
│                              │
│     [클릭하세요!]             │  ← 버튼처럼 보임
└──────────────────────────────┘
          │ 실제로는 위에
┌──────────────────────────────┐
│  bank.com (투명 iframe)      │  ← 안 보이는 레이어
│                              │
│     [이체 확인]               │  ← 실제 클릭 대상
└──────────────────────────────┘
```

�� **섹션 요약 비유**: 유리판(투명 iframe) 위에 달콤한 사탕 그림을 그려서 유리 아래의 버튼을 누르게 하는 것이다.

---

## Ⅲ. 비교 및 연결

| 방어 헤더 | 효과 | 지원 브라우저 |
|:---|:---|:---|
| X-Frame-Options: DENY | 모든 iframe 차단 | 구형 포함 전체 |
| X-Frame-Options: SAMEORIGIN | 동일 출처만 허용 | 구형 포함 전체 |
| CSP frame-ancestors 'none' | 모든 iframe 차단 | 현대 브라우저 |
| CSP frame-ancestors 'self' | 동일 출처만 허용 | 현대 브라우저 |

CSP `frame-ancestors`가 X-Frame-Options보다 더 세밀한 제어(특정 도메인 허용)가 가능해 현대 권장 방법이다.

📢 **섹션 요약 비유**: X-Frame-Options는 구형 자물쇠, CSP frame-ancestors는 스마트 잠금 장치다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**서버 설정 예시 (Nginx)**:
```
add_header X-Frame-Options "DENY";
add_header Content-Security-Policy "frame-ancestors 'none'";
```

**Frame Busting JavaScript** (레거시 방어, CSP에 의해 우회 가능):
```js
if (top !== self) { top.location = self.location; }
```

Frame Busting은 `sandbox` 속성 iframe으로 우회 가능하므로 헤더 기반 방어가 필수이다.

📢 **섹션 요약 비유**: 유리판을 애초에 못 쓰게 하는 법(헤더)이 유리판 위 그림을 지우는 것(JS)보다 확실하다.

---

## Ⅴ. 기대효과 및 결론

X-Frame-Options와 CSP frame-ancestors를 함께 적용하면 모든 브라우저에서 클릭재킹 공격이 차단된다. 중요한 결제·권한 페이지에는 반드시 이 헤더를 설정해야 한다.

📢 **섹션 요약 비유**: 투명 유리판 자체를 만들지 못하게 하면 클릭재킹 마술 트릭이 애초에 불가능해진다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| X-Frame-Options | 방어 | iframe 삽입 차단 헤더 |
| CSP frame-ancestors | 방어 | 세밀한 frame 삽입 제어 |
| Likejacking | 사례 | Facebook 좋아요 클릭재킹 |
| Frame Busting | 레거시 방어 | JS 기반 iframe 탈출 |

### 👶 어린이를 위한 3줄 비유 설명
클릭재킹은 유리판 위에 그림을 그려서 유리 아래 버튼을 누르게 하는 속임수예요.
피해자는 예쁜 그림을 클릭했지만 사실은 송금 버튼을 누른 거예요.
서버가 "내 페이지는 유리판 안에 넣지 마세요"(X-Frame-Options)라고 규칙을 세우면 막을 수 있어요.
"""

FILES["481_x_frame_options.md"] = """\
+++
weight = 481
title = "481. X-Frame-Options 헤더"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: X-Frame-Options는 브라우저에게 해당 페이지를 `<frame>`, `<iframe>`, `<object>` 태그 안에 삽입하는 것을 허용할지 제어하는 HTTP (Hypertext Transfer Protocol) 응답 헤더이다.
> 2. **가치**: Clickjacking 공격을 서버 설정만으로 간단하게 방어할 수 있는 가장 직관적인 수단이며, 구형 브라우저(IE 8+)도 지원한다.
> 3. **판단 포인트**: ALLOW-FROM 지시어는 현대 브라우저에서 지원이 중단되었으므로, 특정 도메인 허용이 필요하면 CSP frame-ancestors를 사용해야 한다.

---

## Ⅰ. 개요 및 필요성

X-Frame-Options는 2009년 Microsoft와 Mozilla가 공동으로 제안한 비표준 헤더로, RFC 7034로 표준화되었다. 세 가지 값을 지원한다.
- `DENY`: 어떠한 frame 안에도 삽입 불가
- `SAMEORIGIN`: 동일 출처(same origin) frame 안에만 허용
- `ALLOW-FROM uri`: 특정 URI만 허용(현대 브라우저 미지원)

📢 **섹션 요약 비유**: "내 초상화를 다른 집 액자(iframe)에 걸지 마세요"라고 알리는 저작권 표시이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 값 | 동작 | 현대 브라우저 지원 |
|:---|:---|:---|
| DENY | 모든 frame 차단 | 전체 |
| SAMEORIGIN | 동일 오리진만 허용 | 전체 |
| ALLOW-FROM | 특정 URL만 허용 | 미지원(deprecated) |

```
[X-Frame-Options 동작]

서버 응답
  HTTP/1.1 200 OK
  X-Frame-Options: DENY
        │
        ▼
  브라우저 판단
        │
  ┌─────┴───────┐
  │ iframe 시도? │
  └─────┬───────┘
        │ YES
        ▼
  로드 차단 + 콘솔 오류
  "Refused to display ... in a frame
   because it set 'X-Frame-Options' to 'deny'"
```

📢 **섹션 요약 비유**: 집 문에 "손님은 현관으로만, 창문으로는 출입 불가"라고 붙여두는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 항목 | X-Frame-Options | CSP frame-ancestors |
|:---|:---|:---|
| 표준 여부 | RFC 7034(비공식) | W3C CSP Level 2 |
| 세밀한 제어 | 제한적 | 다중 출처 허용 가능 |
| 구형 브라우저 | 지원(IE 8+) | 미지원 |
| 권장 | 호환성용 | 현대 기본 권장 |

두 헤더를 모두 설정하면 구형·현대 브라우저 모두 커버된다.

📢 **섹션 요약 비유**: 구형 자물쇠(X-Frame-Options)와 스마트 잠금(CSP)을 함께 쓰면 모든 문이 잠긴다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**설정 예시**:
```
# Nginx
add_header X-Frame-Options "SAMEORIGIN" always;

# Apache
Header always append X-Frame-Options SAMEORIGIN

# Spring Security
http.headers().frameOptions().sameOrigin();
```

어드민·결제·인증 페이지는 `DENY`, 대시보드 위젯처럼 자체 iframe 허용이 필요한 경우 `SAMEORIGIN`을 사용한다.

📢 **섹션 요약 비유**: 중요 방(결제 페이지)은 완전히 잠그고, 내부 공유 방(대시보드)은 가족(동일 오리진)만 열수 있게 하는 것이다.

---

## Ⅴ. 기대효과 및 결론

X-Frame-Options를 적용하면 Clickjacking 공격의 가장 기본적인 기법이 차단된다. CSP frame-ancestors와 함께 설정하면 모든 브라우저 환경에서 완전한 Clickjacking 방어가 구현된다.

📢 **섹션 요약 비유**: 오래된 자물쇠(X-Frame-Options)와 최신 잠금 장치(CSP)를 함께 달면 어떤 도둑도 못 들어온다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Clickjacking | 방어 대상 | iframe 기반 UI 기만 공격 |
| CSP frame-ancestors | 대체·보완 | 현대 브라우저 권장 |
| RFC 7034 | 표준 | X-Frame-Options 명세 |
| SAMEORIGIN | 설정값 | 동일 출처 frame 허용 |

### 👶 어린이를 위한 3줄 비유 설명
X-Frame-Options는 내 사진을 다른 집 액자에 걸지 못하게 하는 저작권 딱지예요.
"DENY"는 아무도 못 쓰게, "SAMEORIGIN"은 우리 집(동일 사이트)만 쓸 수 있게 해요.
이 딱지가 없으면 나쁜 사람이 내 사진 위에 유리판을 덮어 사기를 칠 수 있어요.
"""

FILES["482_frame_ancestors.md"] = """\
+++
weight = 482
title = "482. frame-ancestors (CSP frame-ancestors 지시어)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CSP (Content Security Policy) `frame-ancestors` 지시어는 X-Frame-Options의 현대적 대체제로, 페이지를 frame·iframe·object 안에 삽입할 수 있는 허용 출처를 정밀하게 제어한다.
> 2. **가치**: 다수의 신뢰 도메인(다른 서비스, 파트너사)을 화이트리스트로 설정할 수 있어 X-Frame-Options의 단일 ALLOW-FROM 한계를 극복한다.
> 3. **판단 포인트**: `frame-ancestors 'none'`은 DENY와 동일하며, CSP와 X-Frame-Options가 충돌 시 현대 브라우저는 CSP를 우선 적용한다.

---

## Ⅰ. 개요 및 필요성

CSP Level 2에서 도입된 `frame-ancestors` 지시어는 브라우저가 해당 응답을 frame 안에 로드하기 전에 부모 frame의 출처를 검증하도록 강제한다. X-Frame-Options와 달리 다수의 출처를 공백으로 구분해 나열할 수 있다.

`frame-ancestors`는 Clickjacking 방어에 특화된 지시어로, `default-src`의 fallback이 적용되지 않아 명시적으로 선언해야 한다.

📢 **섹션 요약 비유**: 특정 건물(허용 도메인)에서 온 사람만 내 전시관(페이지)에 frame 형태로 전시할 수 있게 허용 목록을 만드는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 설정값 | 의미 | X-Frame-Options 대응 |
|:---|:---|:---|
| `'none'` | 모든 frame 차단 | DENY |
| `'self'` | 동일 출처만 허용 | SAMEORIGIN |
| `https://trusted.com` | 특정 도메인 허용 | ALLOW-FROM (deprecated) |
| `https://a.com https://b.com` | 다중 도메인 허용 | 불가능 |

```
[frame-ancestors 설정 예시]

Content-Security-Policy: frame-ancestors 'self' https://dashboard.corp.com

          브라우저 체크
               │
    ┌──────────┴──────────┐
    │ 부모 frame 출처?     │
    └──────────┬──────────┘
        ┌──────┴───────────┐
        ▼                   ▼
  self / corp.com          기타 출처
      → 허용                → 차단
```

📢 **섹션 요약 비유**: 전시관 입구에 "우리 건물(self)과 파트너 건물(trusted.com)에만 출품 허용" 안내문을 붙이는 것이다.

---

## Ⅲ. 비교 및 연결

| 항목 | X-Frame-Options | CSP frame-ancestors |
|:---|:---|:---|
| 다중 출처 허용 | 불가 | 가능 |
| 브라우저 우선순위 | 낮음 | 높음 |
| 구형 브라우저 | 지원 | 미지원 |
| 메타 태그 사용 | 불가 | 불가(헤더만) |

두 헤더를 모두 설정하는 것이 최선이며, `frame-ancestors`가 없는 경우 X-Frame-Options로 폴백(fallback)된다.

📢 **섹션 요약 비유**: CSP는 최신 스마트 도어락, X-Frame-Options는 구형 열쇠—둘 다 달아야 모든 문이 안전하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**설정 예시**:
```
# 완전 차단
Content-Security-Policy: frame-ancestors 'none';

# 동일 출처 + 파트너 허용
Content-Security-Policy: frame-ancestors 'self' https://partner.example.com;
```

임베디드 위젯(분석 대시보드, 지도 등)이 필요한 서비스는 `frame-ancestors 'self' https://app.corp.com`으로 파트너 도메인만 허용하고 나머지는 차단한다.

📢 **섹션 요약 비유**: 허가증(화이트리스트)을 가진 파트너만 전시관 액자(iframe)에 넣을 수 있게 한다.

---

## Ⅴ. 기대효과 및 결론

`frame-ancestors`를 통해 Clickjacking 방어와 정상 임베딩 허용을 동시에 달성할 수 있다. X-Frame-Options와 병행 설정 시 모든 브라우저 환경에서 완전한 Clickjacking 방어가 가능하다.

📢 **섹션 요약 비유**: 최신 스마트 도어락과 구형 자물쇠를 모두 달면 어떤 침입자도 막을 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| X-Frame-Options | 레거시 대응 | 구형 브라우저 Clickjacking 방어 |
| CSP Level 2 | 표준 | frame-ancestors 도입 버전 |
| Clickjacking | 방어 대상 | iframe 기반 UI 기만 |
| DENY | 설정값 | none과 동일 효과 |

### 👶 어린이를 위한 3줄 비유 설명
frame-ancestors는 내 전시물(페이지)을 어떤 건물(도메인)의 액자(iframe)에 걸 수 있는지 목록을 만드는 규칙이에요.
목록에 없는 건물에서 전시하려 하면 경보(차단)가 울려요.
옛날 자물쇠(X-Frame-Options)도 함께 달면 구식 건물에서도 안전해요.
"""

FILES["483_cors_preflight.md"] = """\
+++
weight = 483
title = "483. CORS Preflight (교차 출처 리소스 공유 사전 요청)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CORS (Cross-Origin Resource Sharing) Preflight는 브라우저가 실제 요청 전에 `OPTIONS` 메서드로 서버에 허용 여부를 사전 확인하는 메커니즘으로, SOP (Same-Origin Policy) 완화를 안전하게 수행하기 위한 장치이다.
> 2. **가치**: 서버가 명시적으로 허용한 출처·메서드·헤더만 크로스 오리진 요청이 가능하므로, 무분별한 크로스 오리진 요청으로 인한 CSRF (Cross-Site Request Forgery) 유사 공격을 방지한다.
> 3. **판단 포인트**: `Access-Control-Allow-Origin: *`와 `Access-Control-Allow-Credentials: true`를 동시에 설정하면 보안 취약점이 발생하며 브라우저도 이를 거부한다.

---

## Ⅰ. 개요 및 필요성

SOP는 기본적으로 다른 출처로의 요청을 차단하지만, 현대 웹(API 서버, CDN, 마이크로서비스)은 크로스 오리진 요청이 필수적이다. CORS는 W3C (World Wide Web Consortium) 표준으로 이를 안전하게 허용한다.

Preflight 요청은 다음 조건 중 하나가 해당될 때 발생한다.
- HTTP 메서드가 GET·POST·HEAD가 아닌 경우(PUT, DELETE, PATCH 등)
- Content-Type이 `text/plain`, `multipart/form-data`, `application/x-www-form-urlencoded` 이외인 경우
- 커스텀 요청 헤더가 포함된 경우

📢 **섹션 요약 비유**: 파티장(서버)에 들어가기 전에 문지기(Preflight)에게 먼저 초대받았는지 물어보는 절차이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 응답 헤더 | 역할 | 예시 |
|:---|:---|:---|
| Access-Control-Allow-Origin | 허용 출처 | `https://app.example.com` |
| Access-Control-Allow-Methods | 허용 메서드 | `GET, POST, PUT` |
| Access-Control-Allow-Headers | 허용 헤더 | `Content-Type, Authorization` |
| Access-Control-Max-Age | Preflight 캐시 | `3600` (초) |
| Access-Control-Allow-Credentials | 쿠키 포함 허용 | `true` |

```
브라우저 (origin: app.example.com)
  │
  │ OPTIONS /api/data HTTP/1.1
  │ Origin: https://app.example.com
  │ Access-Control-Request-Method: PUT
  ▼
API 서버
  │ HTTP/1.1 204 No Content
  │ Access-Control-Allow-Origin: https://app.example.com
  │ Access-Control-Allow-Methods: GET, PUT
  ▼
브라우저 판단: 허용됨
  │
  │ PUT /api/data HTTP/1.1  ← 실제 요청
  ▼
API 서버 처리
```

📢 **섹션 요약 비유**: 식당(API)에 예약 전화(Preflight)를 먼저 하고 실제 방문(본 요청)하는 것이다.

---

## Ⅲ. 비교 및 연결

| 요청 유형 | Preflight 발생 여부 | 이유 |
|:---|:---|:---|
| GET + 단순 헤더 | 없음 | Simple Request |
| POST + JSON body | 있음 | Content-Type 비표준 |
| DELETE | 있음 | 비표준 메서드 |
| Authorization 헤더 | 있음 | 커스텀 헤더 |

Simple Request(단순 요청)는 Preflight 없이 바로 전송되므로 CSRF와 유사한 위험이 있다. 이 때문에 서버 사이드 CSRF 방어는 여전히 필요하다.

📢 **섹션 요약 비유**: 간단한 심부름(Simple Request)은 예약 없이 바로 가지만, 복잡한 업무(비표준 메서드)는 반드시 사전 예약이 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**잘못된 설정(취약)**:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true  ← 브라우저 오류 발생
```

**올바른 설정**:
```
Access-Control-Allow-Origin: https://trusted.app.com  # 특정 출처만
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT
```

**기술사 논점**: "CORS 설정 오류(와일드카드 + Credentials)는 세션 하이재킹 경로를 열어주므로, 허용 출처는 반드시 명시적으로 지정해야 한다."

📢 **섹션 요약 비유**: 파티에 아무나 초대(wildcard)하면서 와인(쿠키)도 마음대로 마시게 하는 것은 파티 난장판의 시작이다.

---

## Ⅴ. 기대효과 및 결론

Preflight 메커니즘과 명시적 CORS 설정을 통해 신뢰된 출처만 API에 접근하도록 제한하면 크로스 오리진 공격 표면이 최소화된다. `Access-Control-Max-Age` 설정으로 Preflight 캐시를 활용하면 성능과 보안을 동시에 달성한다.

📢 **섹션 요약 비유**: 사전 예약 시스템(Preflight)이 있으면 불청객 없이 초대받은 손님만 파티장에 입장할 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SOP | 기반 | 크로스 오리진 기본 차단 정책 |
| Simple Request | 관련 | Preflight 없이 전송되는 요청 |
| OPTIONS 메서드 | 메커니즘 | Preflight HTTP 메서드 |
| Credentials | 위험 요소 | wildcard와 동시 사용 금지 |

### 👶 어린이를 위한 3줄 비유 설명
CORS Preflight는 낯선 집에 방문하기 전에 전화로 "방문해도 되나요?"라고 먼저 묻는 예의예요.
집 주인(서버)이 "네, 오세요"(허용 헤더)라고 해야만 방문할 수 있어요.
아무 집이나 들어가도 된다고 하면(wildcard + credentials) 도둑이 들 수 있어요.
"""

FILES["484_cors_flow.md"] = """\
+++
weight = 484
title = "484. CORS 요청 흐름 (Cross-Origin Resource Sharing Flow)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CORS (Cross-Origin Resource Sharing) 요청 흐름은 브라우저가 다른 출처(origin)의 리소스를 요청할 때 SOP (Same-Origin Policy)를 안전하게 완화하기 위해 거치는 헤더 교환 과정이다.
> 2. **가치**: CORS 흐름을 정확히 이해해야 API 접근 오류를 빠르게 진단하고, 보안 설정(허용 출처, 메서드, 헤더)이 올바른지 검증할 수 있다.
> 3. **판단 포인트**: 응답의 `Access-Control-Allow-Origin`이 요청의 `Origin` 헤더와 일치해야 하며, 와일드카드(`*`)는 Credentials 요청에서 사용 불가이다.

---

## Ⅰ. 개요 및 필요성

브라우저는 크로스 오리진 요청 시 자동으로 `Origin` 헤더를 추가한다. 서버 응답에 `Access-Control-Allow-Origin`이 없거나 `Origin` 값과 불일치하면 브라우저는 응답을 차단하고 JavaScript에서 오류를 발생시킨다.

중요: CORS는 **서버가 응답을 보내지 않는 것이 아니라**, 브라우저가 응답을 JavaScript에 노출하지 않는 것이다. 따라서 CORS는 클라이언트 사이드 보호 메커니즘이다.

📢 **섹션 요약 비유**: 편지(요청)는 배달되지만, 우체부(브라우저)가 발신자(서버) 허가 없이 수신자(JS)에게 내용물을 보여주지 않는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 단계 | 요청/응답 | 주요 헤더 |
|:---|:---|:---|
| 1. Simple 요청 | GET/POST + 단순 헤더 | `Origin: https://app.com` |
| 2. 서버 응답 | CORS 허용 시 | `Access-Control-Allow-Origin: https://app.com` |
| 3. Preflight | 비단순 요청 전 | `OPTIONS + ACRM + ACRH` |
| 4. 서버 Preflight 응답 | 허용 여부 | `Access-Control-Allow-Methods` |
| 5. 실제 요청 | Preflight 통과 후 | 본 요청 전송 |

```
[CORS Simple Request 흐름]

브라우저
  origin: https://app.com
  │ GET /api/data
  │ Origin: https://app.com
  ▼
서버 (api.backend.com)
  │ 200 OK
  │ Access-Control-Allow-Origin: https://app.com
  ▼
브라우저 검증
  ├─ ACAO == Origin? → YES → JS에 응답 노출
  └─ ACAO 없음/불일치? → CORS 오류, 응답 차단

[CORS 오류 메시지]
"Access to fetch at 'https://api.backend.com/data'
 from origin 'https://app.com' has been blocked by
 CORS policy: No 'Access-Control-Allow-Origin' header"
```

📢 **섹션 요약 비유**: 도서관(서버)이 책(응답)을 주긴 하지만, 사서(브라우저)가 대출증(ACAO 헤더) 없으면 책을 독자(JS)에게 넘기지 않는다.

---

## Ⅲ. 비교 및 연결

| 흐름 유형 | 조건 | Preflight |
|:---|:---|:---|
| Simple Request | GET/POST + 단순 헤더 | 없음 |
| Preflighted Request | PUT/DELETE/커스텀 헤더 | 있음 |
| Credentialed Request | withCredentials=true | 있음 + ACAC 필요 |

CORS 오류는 서버 문제가 아닌 브라우저 정책이므로, `curl`로 직접 요청하면 CORS 오류 없이 응답이 온다. 이 점이 보안 테스트 시 혼동을 야기한다.

📢 **섹션 요약 비유**: 사서(브라우저) 규칙은 일반인(JS)에게만 적용되고, 직원(curl)은 그냥 책을 가져갈 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**CORS 설정 보안 체크리스트**:
1. `Access-Control-Allow-Origin`을 특정 출처로 제한
2. `Access-Control-Allow-Origin: *` + Credentials 동시 사용 금지
3. `Access-Control-Allow-Methods`에 최소 필요 메서드만 나열
4. `Access-Control-Max-Age` 설정으로 Preflight 캐시 활용(성능)

**Spring CORS 설정 예시**:
```java
@CrossOrigin(origins = "https://app.example.com",
             methods = {RequestMethod.GET, RequestMethod.POST})
```

📢 **섹션 요약 비유**: 허용 목록(ACAO)이 정확할수록 올바른 독자만 책을 받아볼 수 있다.

---

## Ⅴ. 기대효과 및 결론

정확한 CORS 흐름 이해를 바탕으로 올바른 설정을 적용하면, 크로스 오리진 API 접근을 안전하게 허용하면서도 무단 접근을 차단할 수 있다. 특히 Credentials 요청에서 명시적 출처 지정은 세션 탈취 방어의 핵심이다.

📢 **섹션 요약 비유**: 사서 규칙(CORS)이 정확하면 진짜 독자에게는 책을, 불청객에게는 책을 숨긴다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SOP | 기반 | 크로스 오리진 기본 차단 |
| Preflight | 메커니즘 | 비단순 요청 사전 허가 |
| ACAO | 핵심 헤더 | 허용 출처 선언 |
| Credentials | 위험 설정 | wildcard 동시 사용 금지 |

### 👶 어린이를 위한 3줄 비유 설명
CORS는 도서관(서버)이 책(응답)을 낯선 동네(다른 출처) 독자에게 줄 수 있는지 사서(브라우저)가 확인하는 규칙이에요.
도서관이 "이 동네(출처) 독자는 괜찮아요"라고 말해야(ACAO 헤더) 사서가 책을 전달해요.
아무한테나 다 준다고 하면(wildcard + credentials) 사서가 거부해요.
"""

# Commit batch 480-484
for fname, content in FILES.items():
    w(fname, content)

commit("feat: Security #480-484 Clickjacking/CORS/Preflight")
FILES.clear()

print("Batch 480-484 done")
