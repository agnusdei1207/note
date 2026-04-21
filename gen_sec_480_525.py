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

FILES["485_owasp_zap.md"] = """\
+++
weight = 485
title = "485. OWASP ZAP (Zed Attack Proxy)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OWASP ZAP (Zed Attack Proxy)는 OWASP (Open Web Application Security Project)에서 개발한 무료 오픈소스 웹 취약점 스캐너로, 수동·자동 취약점 탐지를 모두 지원하는 통합 웹 보안 테스트 도구이다.
> 2. **가치**: CI/CD (Continuous Integration/Continuous Delivery) 파이프라인에 통합하여 DAST (Dynamic Application Security Testing) 자동화가 가능하며, API 보안 테스트에도 활용된다.
> 3. **판단 포인트**: Active Scan은 실제 공격 페이로드를 전송하므로 운영 환경이 아닌 스테이징 환경에서만 사용해야 한다.

---

## Ⅰ. 개요 및 필요성

ZAP은 2010년 오픈소스로 공개되어 현재 가장 널리 사용되는 웹 보안 테스트 도구 중 하나이다. 인터셉팅 프록시로 동작하며, 브라우저와 웹 서버 사이에서 HTTP (Hypertext Transfer Protocol) 트래픽을 캡처·수정·재전송할 수 있다.

주요 기능: Spider(자동 URL 수집), Active Scan(취약점 자동 탐지), Passive Scan(트래픽 분석), Fuzzer, 인증 관리, API 스캔.

📢 **섹션 요약 비유**: 건물 보안 점검관(ZAP)이 문·창문·배관(HTTP 트래픽)을 직접 흔들어보며 취약점을 찾는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 스캔 유형 | 동작 | 위험 수준 |
|:---|:---|:---|
| Passive Scan | 트래픽 관찰만 | 무해 |
| Spider | URL 자동 크롤링 | 낮음 |
| Ajax Spider | SPA JavaScript 렌더링 | 낮음 |
| Active Scan | 취약점 페이로드 전송 | 높음(운영 금지) |
| Fuzzer | 커스텀 페이로드 | 높음 |

```
[ZAP 동작 아키텍처]

브라우저
  │ HTTP 요청
  ▼
ZAP 프록시 (8080포트)
  ├─ Passive Scan: 트래픽 분석
  ├─ Spider: 링크 자동 수집
  ├─ Active Scan: 취약점 페이로드 주입
  │    ├─ SQLi 테스트
  │    ├─ XSS 테스트
  │    └─ Path Traversal 테스트
  ▼
대상 웹 서버
  │ 응답
  ▼
ZAP 결과 보고서
  Alert: High/Medium/Low/Informational
```

📢 **섹션 요약 비유**: 건물 점검관이 실제로 문을 두드리고(Active) 유리창을 들여다보며(Passive) 취약점을 기록하는 것이다.

---

## Ⅲ. 비교 및 연결

| 도구 | 특징 | 유형 |
|:---|:---|:---|
| OWASP ZAP | 무료, CI/CD 통합 | DAST |
| Burp Suite | 강력한 수동 테스트 | DAST(유료 Pro) |
| Nikto | 빠른 서버 취약점 스캔 | DAST |
| Nessus | 네트워크+웹 통합 | 취약점 스캐너 |

📢 **섹션 요약 비유**: ZAP은 무료 건물 안전 검사관, Burp Suite는 전문 보안 엔지니어—용도에 따라 선택한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**CI/CD ZAP 통합 예시 (GitHub Actions)**:
```yaml
- name: ZAP Baseline Scan
  uses: zaproxy/action-baseline@v0.10.0
  with:
    target: 'https://staging.example.com'
```

**Baseline Scan**: Passive 스캔만 수행하여 CI/CD에서 안전하게 실행 가능. Full Scan은 Active 포함하여 스테이징 전용.

📢 **섹션 요약 비유**: 배포 전 검사관(ZAP)이 자동으로 건물을 점검하고 이상 있으면 배포를 막는 것이다.

---

## Ⅴ. 기대효과 및 결론

ZAP을 CI/CD에 통합하면 웹 취약점을 배포 전에 자동으로 탐지하여 Shift-Left 보안을 실현할 수 있다. Baseline Scan은 Passive 모드이므로 운영 환경에도 적용 가능하다.

📢 **섹션 요약 비유**: 건물을 짓는 과정(CI/CD)에서 매번 검사관이 확인하면 완공 후 수리비(보안 사고 비용)가 줄어든다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| DAST | 분류 | 동적 애플리케이션 보안 테스트 |
| CI/CD | 통합 환경 | 자동화 파이프라인 보안 테스트 |
| Active Scan | 기능 | 취약점 페이로드 자동 전송 |
| Burp Suite | 비교 도구 | 전문 수동 테스트 도구 |

### 👶 어린이를 위한 3줄 비유 설명
ZAP은 웹사이트(건물)의 약한 곳을 찾아주는 무료 보안 점검관이에요.
문을 두드려보고(Active Scan) 눈으로 살펴보며(Passive Scan) 취약점을 기록해요.
건물을 지을 때마다(배포마다) 자동으로 점검하면 나중에 큰 수리를 안 해도 돼요.
"""

FILES["486_burp_suite.md"] = """\
+++
weight = 486
title = "486. Burp Suite (웹 취약점 진단 도구)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Burp Suite는 PortSwigger사의 웹 애플리케이션 보안 테스트 통합 플랫폼으로, 인터셉팅 프록시를 중심으로 스캐너·인트루더·리피터 등 다양한 모듈을 제공한다.
> 2. **가치**: 수동 침투 테스트에서 가장 강력한 도구이며, 전문 모의해킹(Penetration Testing) 시장에서 사실상 표준 도구로 사용된다.
> 3. **판단 포인트**: Community Edition은 무료지만 자동 스캐너가 없고, Professional Edition($449/년)에서 Active Scanner, Burp Collaborator가 제공된다.

---

## Ⅰ. 개요 및 필요성

Burp Suite는 2003년 처음 출시되어 현재 버전 2.x까지 발전했다. 인터셉팅 프록시를 통해 HTTP/HTTPS (Hypertext Transfer Protocol Secure) 트래픽을 실시간으로 캡처하고 수정할 수 있어, 웹 애플리케이션의 모든 요청·응답을 완전히 제어할 수 있다.

주요 모듈: Proxy(인터셉팅), Scanner(자동 취약점 탐지), Intruder(자동화 공격), Repeater(요청 수동 반복), Decoder(인코딩 변환), Comparer(응답 비교), Collaborator(Out-of-Band 공격), DOM Invader(DOM XSS 탐지).

📢 **섹션 요약 비유**: 웹 보안 스위스 아미 나이프—하나의 도구에 모든 기능이 담긴 전문 해킹 도구 세트이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 모듈 | 기능 | 용도 |
|:---|:---|:---|
| Proxy | HTTP 인터셉팅 | 트래픽 분석 |
| Scanner | 자동 취약점 탐지 | DAST 자동화 |
| Intruder | 자동화 페이로드 주입 | Brute Force, Fuzzing |
| Repeater | 단일 요청 반복 수정 | 수동 취약점 검증 |
| Collaborator | Out-of-Band 서버 | Blind XXE/SSRF 탐지 |

```
[Burp Suite 프록시 구조]

브라우저
  (Proxy 설정: 127.0.0.1:8080)
  │
  ▼
Burp Proxy
  ├─ Intercept: 요청 일시 정지·수정
  ├─ HTTP History: 모든 요청 로그
  └─ WebSockets: WS 트래픽 캡처
  │
  ▼
대상 웹 서버

[Intruder 공격 유형]
  Sniper: 단일 파라미터 퍼징
  Battering Ram: 모든 파라미터 동일 페이로드
  Pitchfork: 파라미터별 다른 페이로드 리스트
  Cluster Bomb: 모든 조합
```

📢 **섹션 요약 비유**: 탐정(침투 테스터)의 도구 가방—현미경(Proxy), 자물쇠 따개(Intruder), 기록장(Repeater)이 모두 들어있다.

---

## Ⅲ. 비교 및 연결

| 항목 | Burp Community | Burp Professional |
|:---|:---|:---|
| 가격 | 무료 | $449/년 |
| 자동 스캐너 | 없음 | 있음 |
| Intruder 속도 | 제한적 | 무제한 |
| Collaborator | 없음 | 있음 |

📢 **섹션 요약 비유**: 커뮤니티(무료)는 기본 도구, 프로(유료)는 완전한 해킹 실험실이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**SQL 인젝션 테스트 워크플로우**:
1. Proxy로 로그인 요청 캡처
2. Repeater로 전송, 파라미터에 `'` 입력 후 오류 확인
3. Intruder로 Union-based SQLi 페이로드 자동화

**Burp Collaborator 활용**: DNS·HTTP Out-of-Band 서버로 Blind SSRF (Server-Side Request Forgery), Blind XXE (XML External Entity) 탐지에 필수적이다.

📢 **섹션 요약 비유**: Collaborator는 범죄 현장에 마련한 비밀 수신함—직접 보이지 않는 공격도 증거를 남긴다.

---

## Ⅴ. 기대효과 및 결론

Burp Suite를 활용한 수동 침투 테스트는 자동화 스캐너가 놓치는 복잡한 비즈니스 로직 취약점을 발견하는 데 탁월하다. 기술사 시험에서 모의해킹 도구 관련 논술 시 ZAP(무료, CI/CD)과 Burp(전문, 수동)의 용도 차이를 명확히 설명하는 것이 중요하다.

📢 **섹션 요약 비유**: 자동화 로봇(ZAP)은 빠르지만 섬세한 범죄는 전문 형사(Burp)가 찾아낸다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| DAST | 분류 | 동적 보안 테스트 유형 |
| Intruder | 핵심 모듈 | 자동화 페이로드 공격 |
| Collaborator | 고급 기능 | Out-of-Band 공격 탐지 |
| OWASP ZAP | 비교 도구 | 무료 DAST 대안 |

### 👶 어린이를 위한 3줄 비유 설명
Burp Suite는 웹사이트(건물)의 모든 구석을 탐색할 수 있는 탐정 도구 세트예요.
모든 대화(HTTP 요청)를 엿듣고(Proxy), 반복해보고(Repeater), 자동으로 시험해볼(Intruder) 수 있어요.
전문 탐정(침투 테스터)이 사용하는 도구라서 올바른 목적으로만 써야 해요.
"""

FILES["487_sqlmap.md"] = """\
+++
weight = 487
title = "487. SQLMap (SQL 인젝션 자동화 도구)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SQLMap은 SQL (Structured Query Language) 인젝션 취약점을 자동으로 탐지하고 익스플로잇하는 오픈소스 도구로, Error-based·Boolean-based·Time-based·Union-based 등 다양한 기법을 지원한다.
> 2. **가치**: 수동으로 수 시간이 걸리는 SQL 인젝션 분석을 자동화하여 DB (Database) 스키마·데이터 덤프, OS 명령 실행까지 가능하다.
> 3. **판단 포인트**: SQLMap은 취약점 탐지 후 자동으로 악용(exploitation)까지 진행하므로, 반드시 서면 허가를 받은 대상에만 사용해야 한다.

---

## Ⅰ. 개요 및 필요성

SQLMap은 2006년 처음 공개된 이후 SQL 인젝션 자동화 도구의 사실상 표준이 되었다. Python으로 작성되어 모든 OS에서 동작하며, MySQL·PostgreSQL·Oracle·MSSQL·SQLite 등 주요 DBMS (Database Management System)를 지원한다.

자동 탐지 기법: Error-based, Union-based, Boolean-based Blind, Time-based Blind, Stacked Queries, Out-of-Band.

📢 **섹션 요약 비유**: 금고(DB) 열기 도구—취약한 자물쇠(SQL 인젝션)를 자동으로 찾아내고 여는 스위스 아미 나이프이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 기법 | 동작 원리 | 속도 |
|:---|:---|:---|
| Error-based | DB 오류 메시지 분석 | 빠름 |
| Union-based | UNION SELECT로 데이터 추출 | 빠름 |
| Boolean Blind | 참/거짓 응답 차이 분석 | 중간 |
| Time-based Blind | 응답 지연 시간 측정 | 느림 |
| Out-of-Band | DNS/HTTP 외부 채널 | 느림 |

```
[SQLMap 동작 흐름]

sqlmap -u "http://target.com/page?id=1"
  │
  ▼
파라미터 자동 식별
  id=1 → 취약 파라미터 탐지
  │
  ▼
인젝션 기법 순서 시도
  Error-based → Union → Boolean → Time
  │
  ▼
DB 정보 추출
  DB 버전, DB 명, 테이블, 컬럼, 데이터
  │
  ▼
(옵션) OS Shell / File Read/Write
```

📢 **섹션 요약 비유**: 자물쇠 따개(SQLMap)가 여러 종류의 도구(기법)를 순서대로 사용해 문을 열어본다.

---

## Ⅲ. 비교 및 연결

| 옵션 | 기능 |
|:---|:---|
| `--dbs` | DB 목록 열거 |
| `--tables -D dbname` | 테이블 목록 |
| `--dump -T table` | 테이블 데이터 덤프 |
| `--os-shell` | OS 명령어 실행 |
| `--level=5 --risk=3` | 공격 강도 최대 |
| `--batch` | 비대화식 자동 실행 |

📢 **섹션 요약 비유**: 옵션들은 도구 가방 안의 각기 다른 도구—필요한 것만 꺼내 쓰면 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**방어 관점 활용**: WAF (Web Application Firewall) 규칙 효과 검증, 입력 검증 우회 가능 여부 확인, 파라미터화 쿼리(Parameterized Query) 적용 여부 테스트에 활용한다.

**탐지 우회 옵션**:
```
sqlmap --tamper=space2comment,between  # WAF 우회 tamper 스크립트
sqlmap --delay=2 --timeout=30          # 타이밍 조절
```

**법적 주의**: 권한 없는 대상에 SQLMap 사용은 불법이다. 버그바운티·CTF·화이트박스 테스트에만 사용한다.

📢 **섹션 요약 비유**: 자물쇠 따개는 내 집 잠긴 문을 열 때만 합법—남의 집에 쓰면 범죄이다.

---

## Ⅴ. 기대효과 및 결론

방어자 관점에서 SQLMap은 자신의 시스템에 SQL 인젝션 취약점이 있는지 빠르게 검증하는 데 매우 유용하다. 파라미터화 쿼리와 ORM (Object-Relational Mapping)을 적용했을 때 SQLMap이 데이터를 추출하지 못하면 방어가 성공적으로 이루어진 것이다.

📢 **섹션 요약 비유**: 방어 효과를 검증하려면 직접 자물쇠(내 시스템)를 따개(SQLMap)로 시험해봐야 한다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Parameterized Query | 방어 | SQL 인젝션 근본 차단 |
| WAF | 탐지 | SQLMap 요청 시그니처 탐지 |
| Blind SQLi | 기법 | 응답 차이로 데이터 추출 |
| tamper script | 우회 | WAF 탐지 회피 기법 |

### 👶 어린이를 위한 3줄 비유 설명
SQLMap은 웹사이트의 잠긴 금고(DB)를 자동으로 열어보는 도구예요.
금고 자물쇠(SQL 쿼리)에 문제가 있으면 자동으로 찾아내고 내용물(데이터)을 꺼낼 수 있어요.
허가받은 집(내 시스템)에서만 사용해야 하고, 남의 집에 쓰면 범죄예요.
"""

FILES["488_nikto.md"] = """\
+++
weight = 488
title = "488. Nikto (웹 서버 취약점 스캐너)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Nikto는 웹 서버의 알려진 취약점·위험한 파일·구성 오류를 빠르게 스캔하는 오픈소스 CLI (Command Line Interface) 도구로, 6,700개 이상의 잠재적 위험 항목을 데이터베이스로 관리한다.
> 2. **가치**: 초기 정보 수집(Reconnaissance) 단계에서 빠른 공격 표면(Attack Surface) 파악에 유용하며, 서버 헤더·쿠키 설정·디렉토리 노출 등을 자동으로 점검한다.
> 3. **판단 포인트**: Nikto는 스텔스 기능이 없어 IDS (Intrusion Detection System)/WAF에 즉시 탐지되므로, 은밀한 테스트보다는 빠른 기본 점검에 적합하다.

---

## Ⅰ. 개요 및 필요성

Nikto는 2001년 CIRT.net에서 개발한 웹 서버 취약점 스캐너이다. Apache·Nginx·IIS (Internet Information Services) 등 모든 웹 서버를 대상으로 취약한 파일·디렉토리(예: `/admin`, `/.git`, `/phpinfo.php`), 서버 헤더 정보 노출, 구형 소프트웨어 버전 등을 탐지한다.

Kali Linux에 기본 탑재되어 있으며, Perl로 작성되어 크로스 플랫폼 동작이 가능하다.

📢 **섹션 요약 비유**: 건물 외관을 빠르게 돌아다니며 열린 문·깨진 창문·경고 표지판을 체크하는 빠른 사전 점검이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 스캔 항목 | 예시 | 위험 |
|:---|:---|:---|
| 위험한 파일 | `/phpinfo.php`, `/.git` | 정보 노출 |
| 구형 소프트웨어 | Apache 2.2.x | CVE (Common Vulnerabilities Exposures) 취약점 |
| 보안 헤더 누락 | X-Frame-Options, CSP 없음 | Clickjacking, XSS |
| 기본 자격증명 | `admin:admin` 기본값 | 무단 접근 |
| 취약한 CGI | 오래된 CGI (Common Gateway Interface) 스크립트 | RCE (Remote Code Execution) |

```
[Nikto 스캔 흐름]

nikto -h https://target.com -o report.html
  │
  ▼
대상 서버 연결
  │
  ▼
6,700+ 항목 점검
  ├─ 서버 버전 확인
  ├─ 위험 파일 경로 확인
  ├─ 보안 헤더 확인
  ├─ 쿠키 속성 확인
  └─ 디렉토리 리스팅 확인
  │
  ▼
결과 보고서 (HTML/CSV/XML)
```

📢 **섹션 요약 비유**: 점검관이 체크리스트(6,700항목)를 들고 건물 외관을 빠르게 순회하는 것이다.

---

## Ⅲ. 비교 및 연결

| 도구 | 특징 | 탐지 난이도 |
|:---|:---|:---|
| Nikto | 빠른 기본 스캔, 노이즈 많음 | IDS에 즉시 탐지 |
| OWASP ZAP | 심층 스캔, CI/CD 통합 | 중간 |
| Burp Suite | 수동 심층 분석 | 설정에 따라 다름 |
| Nmap | 포트·서비스 스캔 | 낮음 |

📢 **섹션 요약 비유**: Nikto는 빠르지만 시끄러운 점검, Burp는 느리지만 조용한 정밀 분석이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**기본 사용법**:
```
nikto -h https://target.com          # 기본 스캔
nikto -h https://target.com -Tuning 1  # SQL 인젝션 집중
nikto -h https://target.com -ssl      # HTTPS 강제
nikto -h https://target.com -useragent "Custom"  # UA 변경
```

방어자 관점: Nikto가 발견하는 항목들을 사전에 수정하면 공격자의 초기 정보 수집을 무력화할 수 있다. 특히 `X-Powered-By`, `Server` 헤더 제거와 보안 헤더 추가가 핵심이다.

📢 **섹션 요약 비유**: 점검관이 발견하는 문제들을 미리 고쳐두면 공격자가 찾을 것이 없어진다.

---

## Ⅴ. 기대효과 및 결론

Nikto를 통한 기초 보안 점검으로 서버 구성 오류·정보 노출·레거시 취약점을 빠르게 파악할 수 있다. 정기적인 Nikto 스캔 결과를 기반으로 서버 하드닝(Hardening) 작업을 수행하면 공격 표면을 효과적으로 줄일 수 있다.

📢 **섹션 요약 비유**: 빠른 점검(Nikto)으로 쉬운 취약점을 먼저 제거하면 고급 공격자도 시작점을 잃는다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| CVE | 탐지 기반 | 알려진 취약점 데이터베이스 |
| 정보 수집 | 단계 | Nikto의 주요 활용 단계 |
| 서버 하드닝 | 방어 | Nikto 결과 기반 보안 강화 |
| IDS | 탐지됨 | Nikto 트래픽 즉시 탐지 |

### 👶 어린이를 위한 3줄 비유 설명
Nikto는 건물(웹 서버)을 빠르게 돌아다니며 열린 문·깨진 창문을 찾는 점검관이에요.
체크리스트(6,700항목)에 있는 문제들을 자동으로 확인해줘요.
점검관이 발견한 문제를 미리 고치면 나쁜 사람이 들어올 구멍이 없어져요.
"""

# Commit batch 485-488
for fname, content in FILES.items():
    w(fname, content)
commit("feat: Security #485-488 ZAP/Burp/SQLMap/Nikto")
FILES.clear()
print("Batch 485-488 done")
