+++
title = "Web 1.0과 Web 2.0 (Web 1.0 & Web 2.0)"
description = "웹의 진화 과정에서 Web 1.0(읽기 전용)과 Web 2.0(읽기-쓰기, 플랫폼 중심)의 특징과 한계점을 분석하는 심층 기술 백서"
date = 2024-05-15
[taxonomies]
tags = ["Web 1.0", "Web 2.0", "Platform Economy", "ICT Convergence", "Internet Evolution"]
+++

# Web 1.0과 Web 2.0 (Web 1.0 & Web 2.0)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Web 1.0은 정적 HTML 페이지 중심의 '읽기 전용(Read-Only)' 인터넷 시대로, 사용자는 콘텐츠 소비자로만 역할이 제한되었으며, Web 2.0은 AJAX, 소셜 미디어, 클라우드 기반 플랫폼의 등장으로 사용자가 콘텐츠 생성과 상호작용에 참여하는 '읽기-쓰기(Read-Write)' 패러다임으로 전환된 웹 환경입니다.
> 2. **가치**: Web 2.0은 플랫폼 비즈니스 모델(플랫폼 경제)을 창출하여 페이스북, 유튜브, 우버 등 수조 원 규모의 디지털 경제 생태계를 구축했으나, 동시에 데이터 독점, 프라이버시 침해, 알고리즘 편향 등 중앙화된 플랫폼 권력의 부작용을 야기했습니다.
> 3. **융합**: Web 2.0의 한계를 극복하기 위해 블록체인 기반 탈중앙화, 사용자 데이터 주권 보장, 토큰 이코노미를 결합한 Web 3.0으로 진화하고 있으며, AI 생성 콘텐츠(AIGC)와 메타버스가 웹 경험을 3차원으로 확장하는 미래 방향으로 전개됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**Web 1.0**은 1990년대 초반부터 2000년대 초반까지 지속된 인터넷의 첫 번째 세대로, 팀 버너스리(Tim Berners-Lee)가 제안한 하이퍼텍스트 전송 프로토콜(HTTP)과 HTML(HyperText Markup Language)을 기반으로, 주로 기관과 기업이 단방향으로 정보를 제공하는 정적(Static) 웹페이지들로 구성되었습니다. 사용자는 브라우저를 통해 콘텐츠를 '읽기만' 할 수 있었으며, 콘텐츠 생성은 극소수의 기술적 지식을 갖춘 웹마스터에게 제한되었습니다.

**Web 2.0**은 2004년경 달 코니(Tim O'Reilly)가 정의한 개념으로, 사용자가 콘텐츠를 직접 생성·수정·공유할 수 있는 '참여형 플랫폼'으로서의 웹을 의미합니다. AJAX(Asynchronous JavaScript and XML), RSS, 위키(Wiki), 블로그, 소셜 네트워크 서비스(SNS) 등의 기술이 등장하면서, 웹은 단순한 문서 열람 공간을 넘어 소프트웨어 애플리케이션 플랫폼으로 진화했습니다.

### 2. 구체적인 일상생활 비유
**Web 1.0**은 마치 **도서관의 백과사전**과 같습니다. 도서관에 가면 이미 인쇄되어 있는 책들을 읽을 수만 있고, 일반 방문객은 책의 내용을 수정하거나 새로운 글을 추가할 수 없습니다. 모든 지식은 소수의 저자와 출판사가 독점적으로 생산합니다.

**Web 2.0**은 **열린 광장의 커뮤니티 게시판**과 같습니다. 누구나 게시판에 글을 쓰고, 댓글을 달며, 좋아요를 누르고, 다른 사람의 글을 공유할 수 있습니다. 광장 관리자(플랫폼 기업)는 이 공간을 제공하고 운영하는 대신, 사용자들이 만들어낸 모든 활동 데이터를 수집하여 맞춤형 광고를 보여주고 수익을 창출합니다.

### 3. 등장 배경 및 발전 과정
1. **Web 1.0의 한계와 Web 2.0 등장 배경**:
   - **정적 콘텐츠의 제약**: Web 1.0의 HTML 페이지는 서버에 저장된 파일을 그대로 전송하는 방식으로, 사용자 맞춤형 콘텐츠 제공이 불가능했습니다. 모든 방문자에게 동일한 페이지가 노출되며, 개인화나 상호작용이 전무했습니다.
   - **콘텐츠 생산의 독점**: 홈페이지 제작에는 HTML, CSS, FTP 업로드 등 기술적 지식이 필요하여, 일반 사용자는 정보 소비자로만 국한되었습니다. 이는 인터넷의 민주화와 참여라는 월드와이드웹의 원래 철학과 배치되었습니다.
   - **기술적 기반의 성숙**: 2000년대 초반 브로드밴드 인터넷 보급, 브라우저의 JavaScript 엔진 고도화, XMLHttpRequest 객체를 통한 비동기 통신(AJAX) 기술이 성숙하면서, 페이지 새로고침 없이 서버와 데이터를 주고받는 동적 웹 애플리케이션이 가능해졌습니다.

2. **플랫폼 경제의 부상과 중앙화 문제**:
   - 페이스북(2004), 유튜브(2005), 트위터(2006), 아이폰(2007) 등의 등장으로 사용자 생성 콘텐츠(UGC, User Generated Content)가 폭발적으로 증가했습니다.
   - 그러나 이러한 플랫폼들은 '무료 서비스'를 제공하는 대가로 사용자의 개인정보, 행동 데이터, 소셜 관계망을 수집하고 독점하는 '데이터 팩토리' 모델로 진화했습니다. 캠브리지 애널리티카 스캔들(2018) 등은 이러한 중앙화된 데이터 독점의 위험성을 극명히 보여주었습니다.

3. **Web 2.0에서 Web 3.0으로의 전환 압력**:
   - 플랫폼 기업의 독점적 지위로 인한 경제적 불평등(크리에이터 vs 플랫폼 수익 배분), 검열과 계정 정지 위험, 알고리즘에 의한 여론 조작 우려 등이 사회적 문제로 대두되었습니다.
   - 이를 해결하기 위해 블록체인 기반의 탈중앙화 프로토콜, 사용자 데이터 주권(DID, MyData), 토큰 이코노미를 결합한 Web 3.0 비전이 제시되고 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Component) | Web 1.0 특성 | Web 2.0 특성 | 내부 동작 메커니즘 | 비유 |
|:---|:---|:---|:---|:---|
| **콘텐츠 생산 주체** | 웹마스터, 기관 (일방향) | 모든 사용자 (쌍방향) | CMS(WordPress), SNS 플랫폼이 에디터 UI 제공, 사용자 입력을 DB에 저장 | 도서관 저자 → 위키피디아 참여자 |
| **페이지 렌더링** | 정적 HTML (서버 사이드) | 동적 AJAX/SPA (클라이언트 사이드) | JavaScript가 DOM을 조작하고, REST API로 서버와 비동기 통신 | 인쇄된 책 → 실시간 업데이트 뉴스피드 |
| **데이터 저장** | 파일 시스템 (정적 파일) | 관계형/NoSQL 데이터베이스 | MySQL, PostgreSQL, MongoDB 등이 사용자 데이터를 구조화하여 저장 | 물리 문서 보관소 → 클라우드 DB |
| **사용자 식별** | 익명/IP 기반 | 계정 기반 (OAuth, SSO) | 중앙 인증 서버가 ID/PW를 관리하고 세션/토큰(JWT) 발급 | 방문증 없이 열람 → 회원카드 발급 |
| **수익 모델** | 배너 광고, 유료 구독 | 타겟 광고, 데이터 판매, 플랫폼 수수료 | 행동 추적(Cookie, Pixel), 빅데이터 분석, 실시간 입찰(RTB) 광고 | 신문 광고 → 맞춤형 추천 광고 |
| **프로토콜/기술** | HTTP, HTML, CGI | HTTP/HTTPS, AJAX, REST API, JSON | XMLHTTPRequest, Fetch API, WebSocket을 통한 실시간 양방향 통신 | 우편 → 인스턴트 메신저 |

### 2. 정교한 구조 다이어그램: Web 1.0 vs Web 2.0 아키텍처 비교

```text
================================================================================
                    [ Web 1.0 Architecture (Static Web) ]
================================================================================
        +----------------+         +------------------+
        |   Web Browser  |  HTTP   |   Web Server     |
        |  (Netscape/IE) | <-----> |  (Apache/IIS)    |
        +----------------+  HTML   +------------------+
                                        |      |
                                        v      v
                                +----------+ +----------+
                                | Static   | | CGI/Perl |
                                | HTML/CSS | | Scripts  |
                                | Files    | | (Limited)|
                                +----------+ +----------+

=> 특징: 요청 시마다 페이지 전체 새로고침, 서버가 완성된 HTML 전송
=> 한계: 상호작용 부재, 개인화 불가, 콘텐츠 업데이트 어려움


================================================================================
                    [ Web 2.0 Architecture (Dynamic/Platform Web) ]
================================================================================

+-------------------+     AJAX/REST API      +------------------------+
|   Modern Browser  | <------------------->  |    Web Application     |
|  (Chrome/Safari)  |     JSON/WebSocket     |       Server           |
|                   |                        +------------------------+
| +---------------+ |                              |            |
| | SPA Framework | |                              v            v |
| | (React/Vue)   | |   +-----------+      +-------------+        |
| | Client-Side   | |   | API       |      | Database    |        |
| | Rendering     | |   | Gateway   |<---->| (MySQL/     |        |
| +---------------+ |   | (REST/    |      |  MongoDB)   |        |
| | User Data     | |   |  GraphQL) |      +-------------+        |
| | (Cookies/     | |   +-----------+             |               |
| |  LocalStore)  | |        |                    v               |
| +---------------+ |        |          +------------------+       |
| | Social Login  | |        +--------->| User Profile     |       |
| | (OAuth 2.0)   | |                   | & Behavioral    |       |
| +---------------+ |                   | Data Storage    |       |
+-------------------+                   +------------------+       |
                                               |                  |
                                               v                  v
                                        +-------------+    +-------------+
                                        | Ad Network  |    | Analytics   |
                                        | (Targeting) |    | (Big Data)  |
                                        +-------------+    +-------------+

=> 특징: 비동기 통신으로 페이지 부분 업데이트, 사용자 행동 데이터 실시간 수집
=> 플랫폼: 사용자 생성 콘텐츠(UGC), 소셜 그래프, 추천 알고리즘 결합
```

### 3. 심층 동작 원리: AJAX와 동적 웹의 구현
Web 2.0의 핵심 기술인 AJAX(Asynchronous JavaScript and XML)의 동작 메커니즘입니다.

1. **사용자 이벤트 발생**: 사용자가 '더 보기' 버튼을 클릭하거나 무한 스크롤이 하단에 도달합니다.
2. **JavaScript 이벤트 핸들러 실행**: 브라우저의 JavaScript 엔진이 이벤트를 감지하고, `XMLHttpRequest` 또는 `fetch()` API를 호출합니다.
3. **비동기 HTTP 요청 전송**: 페이지 새로고침 없이 백그라운드에서 서버에 REST API 요청(GET /api/posts?page=2)을 보냅니다. 요청 헤더에는 사용자 인증 토큰(JWT)과 세션 쿠키가 포함됩니다.
4. **서버 측 데이터 처리**: API 서버가 데이터베이스에서 추가 콘텐츠를 조회하고, JSON 형식으로 직렬화하여 응답합니다. 동시에 사용자의 행동 로그(어떤 콘텐츠를 조회했는지)를 분석 DB에 기록합니다.
5. **클라이언트 측 DOM 업데이트**: 브라우저가 JSON 응답을 수신하면, JavaScript가 DOM(Document Object Model)을 동적으로 조작하여 새 콘텐츠를 페이지 하단에 추가 렌더링합니다. 이 과정에서 페이지 깜빡임이 전혀 발생하지 않습니다.

### 4. 핵심 알고리즘 및 실무 코드 예시: OAuth 2.0 소셜 로그인 플로우

Web 2.0 플랫폼의 핵심인 소셜 로그인(OAuth 2.0) 인증 플로우를 구현한 코드 예시입니다.

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
import httpx
import secrets
from typing import Dict

app = FastAPI()

# OAuth 2.0 설정 (Google 예시)
GOOGLE_CLIENT_ID = "your-client-id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your-client-secret"
GOOGLE_REDIRECT_URI = "https://yourapp.com/auth/callback"

# 임시 상태 저장소 (실제는 Redis 등 분산 캐시 사용)
state_store: Dict[str, str] = {}

@app.get("/auth/login/google")
async def google_login():
    """
    OAuth 2.0 인증 요청 시작
    사용자를 Google 로그인 페이지로 리다이렉트
    """
    # CSRF 방지용 랜덤 state 토큰 생성
    state_token = secrets.token_urlsafe(32)
    state_store[state_token] = "pending"

    # OAuth 2.0 Authorization Code Grant 플로우 시작
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile"  # 요청할 사용자 정보 범위
        f"&state={state_token}"          # CSRF 방지
        f"&access_type=offline"          # 리프레시 토큰 요청
    )
    return RedirectResponse(url=auth_url)

@app.get("/auth/callback")
async def google_callback(request: Request):
    """
    Google 인증 완료 후 콜백 처리
    Authorization Code를 Access Token으로 교환
    """
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    # 1. State 토큰 검증 (CSRF 방어)
    if state not in state_store:
        raise HTTPException(status_code=400, detail="Invalid state token")

    # 2. Authorization Code → Access Token 교환
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        # 3. Access Token으로 사용자 정보 조회
        userinfo_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_info = userinfo_response.json()

    # 4. 사용자 DB 저장 및 세션 생성 (Web 2.0의 핵심: 사용자 식별)
    user_email = user_info.get("email")
    user_name = user_info.get("name")

    # 실제 서비스에서는 여기서 DB 조회/생성 및 JWT 발급
    return {
        "message": "Web 2.0 로그인 성공",
        "user_email": user_email,
        "user_name": user_name,
        "note": "플랫폼이 사용자를 식별하고 행동 데이터를 추적합니다"
    }

# Web 2.0 플랫폼의 핵심: 사용자 행동 추적 (Behavioral Tracking)
@app.post("/api/track/event")
async def track_user_behavior(event: dict):
    """
    사용자의 모든 클릭, 스크롤, 체류 시간을 추적
    → 이 데이터가 맞춤형 광고와 추천 알고리즘의 원료가 됨
    """
    user_id = event.get("user_id")
    event_type = event.get("event_type")  # click, scroll, purchase, etc.
    content_id = event.get("content_id")
    timestamp = event.get("timestamp")

    # 실제로는 Kafka 스트림 → BigQuery/Data Lake로 적재
    print(f"[TRACKING] User {user_id}: {event_type} on {content_id} at {timestamp}")

    return {"status": "tracked", "privacy_note": "Web 2.0은 사용자 데이터를 수집합니다"}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: Web 1.0 vs Web 2.0 vs Web 3.0

| 평가 지표 | Web 1.0 (Read-Only) | Web 2.0 (Read-Write) | Web 3.0 (Read-Write-Own) |
|:---|:---|:---|:---|
| **데이터 소유권** | 콘텐츠 제작자 소유 | 플랫폼 기업 독점 | 사용자 소유 (탈중앙화) |
| **상호작용 수준** | 없음 (단방향) | 높음 (댓글, 공유, 협업) | 높음 + 스마트 컨트랙트 자동화 |
| **신원 관리** | 익명/IP 기반 | 중앙 계정 (OAuth, 이메일) | 탈중앙 신원 (DID, 지갑) |
| **수익 모델** | 광고, 구독 | 데이터 판매, 광고, 수수료 | 토큰 이코노미, 크리에이터 직접 수익 |
| **신뢰 모델** | 콘텐츠 제작자 신뢰 | 플랫폼 신뢰 (Faustian Bargain) | 코드/알고리즘 신뢰 (Trustless) |
| **프로토콜** | HTTP, HTML | HTTP/HTTPS, REST, WebSocket | HTTP, IPFS, 블록체인 |
| **대표 서비스** | 야후 디렉토리, 개인 홈피 | 페이스북, 유튜브, 우버 | 유니스왑, 오픈씨, 렌싱 프로토콜 |

### 2. 과목 융합 관점 분석 (Web 2.0 + 타 기술 시너지)
- **Web 2.0 + 데이터베이스 (DB)**: Web 2.0 플랫폼의 핵심은 사용자 데이터의 구조화된 저장과 실시간 조회입니다. 페이스북의 TaO, 구글의 Spanner와 같은 분산 데이터베이스는 수십억 명의 사용자 데이터를 밀리초 단위에 조회하기 위한 Read 복제본, 샤딩, 파티셔닝 기술을 극한으로 발전시켰습니다.
- **Web 2.0 + AI/ML**: 플랫폼이 수집한 사용자 행동 데이터는 머신러닝 추천 알고리즘(협업 필터링, 딥러닝 기반 CTR 예측)의 학습 데이터가 됩니다. 이것이 '당신이 좋아할 만한 콘텐츠'와 '맞춤형 광고'를 가능하게 합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략
- **[상황 A] 레거시 기업의 디지털 전환 (Web 1.0 → Web 2.0)**
  - **문제점**: 정적 웹사이트만 운영 중인 제조기업이 고객 참여형 커뮤니티와 개인화 서비스를 구축해야 함.
  - **기술사 판단**: CMS(WordPress, Contentful) 도입으로 비개발자도 콘텐츠를 수정할 수 있게 하고, 고객 데이터 수집을 위한 CRM(Salesforce) 연동. 단, GDPR, CCPA 등 개인정보보호 법규 준수를 위한 동의 관리(Consent Management) 플랫폼 필수 도입.

- **[상황 B] 플랫폼 기업의 데이터 독점 리스크 관리**
  - **문제점**: Web 2.0 플랫폼 모델로 성장한 기업이 규제 당국의 '데이터 독점' 조사와 '알고리즘 투명성' 요구에 직면.
  - **기술사 판단**: 데이터 이동성(Data Portability) API를 개방하고, 사용자에게 자신의 데이터를 다운로드/삭제할 수 있는 권한을 부여. 장기적으로는 Web 3.0의 탈중앙화 신원(DID) 기술과 호환되는 아키텍처로 마이그레이션 준비.

### 2. 도입 시 고려사항 (기술적/법적 체크리스트)
- **개인정보보호 법규 준수**: GDPR(유럽), CCPA(캘리포니아), 개인정보보호법(한국)에 따른 데이터 수집 목적 고지, 동의 획득, 삭제권(잊혀질 권리) 보장 메커니즘 구현.
- **플랫폼 종속성(Lock-in) 완화**: 특정 클라우드 공급자나 SaaS 플랫폼에 데이터가 완전히 종속되지 않도록, 데이터 내보내기 기능과 오픈 표준 포맷(JSON, CSV) 지원.

### 3. 주의사항 및 안티패턴 (Anti-patterns)
- **데이터 과잉 수집(Over-collection)**: "나중에 쓸지도 모르니 일단 다 저장하자"는 안티패턴. GDPR의 '데이터 최소화 원칙' 위반이며, 보안 사고 시 유출 범위가 커집니다. 필요한 데이터만 수집하고, 보존 기간을 명시해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | Web 1.0 (AS-IS) | Web 2.0 (TO-BE) | 개선 지표 |
|:---|:---|:---|:---|
| **사용자 참여율** | 0% (읽기 전용) | 30~70% (UGC 비중) | **참여형 커뮤니티 형성** |
| **콘텐츠 업데이트 주기** | 주/월 단위 수동 갱신 | 실시간 (사용자 생성) | **정보 최신성 확보** |
| **개인화 수준** | 없음 (동일 페이지) | 행동 기반 추천 | **사용자 경험(UX) 향상** |
| **수익 모델 다양성** | 광고/구독 제한적 | 광고, 데이터, 마켓플레이스 | **비즈니스 모델 확장** |

### 2. 미래 전망 및 진화 방향
- **Web 3.0으로의 과도기**: Web 2.0 플랫폼들이 점진적으로 블록체인 기술을 도입하고 있습니다(트위터의 NFT 프로필, 유튜브의 NFT 크리에이터 도구 등). 향후 5~10년 내 사용자 데이터 주권을 보장하는 하이브리드 모델이 등장할 것입니다.
- **AI 생성 콘텐츠(AIGC)의 폭발**: ChatGPT, Stable Diffusion 등 AI가 텍스트, 이미지, 영상을 생성하는 시대에, Web 2.0 플랫폼은 'AI 콘텐츠 식별'과 '저작권 보호'라는 새로운 난제에 직면합니다.
- **메타버스와 3D 웹**: Web 2.0의 2D 화면 기반 인터페이스를 넘어, VR/AR 기기와 공간 컴퓨팅 기술이 결합된 입체적 웹 경험이 차세대 표준으로 부상합니다.

### 3. 참고 표준/가이드
- **W3C 웹 표준**: HTML5, CSS3, ECMAScript 등 웹 기술의 공식 사양.
- **OAuth 2.0 / OpenID Connect**: Web 2.0 소셜 로그인의 사실상 표준 인증 프로토콜 (RFC 6749).
- **GDPR (General Data Protection Regulation)**: 유럽연합 개인정보보호 규정, Web 2.0 플랫폼의 데이터 처리에 강력한 제약.

---

## 관련 개념 맵 (Knowledge Graph)
- **[Web 3.0](@/studynotes/06_ict_convergence/02_blockchain/web3.md)**: Web 2.0의 데이터 독점 문제를 블록체인 기반 탈중앙화로 해결하는 차세대 웹.
- **[블록체인](@/studynotes/06_ict_convergence/02_blockchain/blockchain.md)**: Web 3.0의 신뢰 계층을 담당하는 분산 원장 기술.
- **[DID (탈중앙화 신원)](@/studynotes/06_ict_convergence/02_blockchain/did.md)**: Web 2.0의 중앙 계정 시스템을 대체하는 사용자 주권형 신원 증명.
- **[REST API](@/studynotes/06_ict_convergence/01_cloud/rest_api.md)**: Web 2.0 애플리케이션의 표준 통신 인터페이스.
- **[마이데이터 (MyData)](@/studynotes/06_ict_convergence/06_core_topics/mydata.md)**: Web 2.0 플랫폼에서 사용자에게 데이터 제어권을 반환하는 프레임워크.

---

## 어린이를 위한 3줄 비유 설명
1. **Web 1.0**은 마치 **백화점 쇼윈도**예요. 유리창 너머로 예쁜 옷들을 구경만 할 수 있고, 직접 입어보거나 의견을 말할 수는 없어요.
2. **Web 2.0**은 **놀이공원** 같아요! 직접 놀이기구를 타고, 친구들과 사진도 찍고, 게시판에 내 이야기도 쓸 수 있어요. 하지만 놀이공원 주인이 여러분의 모든 행동을 지켜보고 기록한다는 게 조금 무섭죠?
3. 그래서 등장한 **Web 3.0**은 여러분이 직접 **놀이공원의 주인**이 되는 거예요! 내가 만든 놀이기구, 내가 찍은 사진이 모두 나의 소유가 되고, 다른 사람들과 공정하게 나눌 수 있어요.
