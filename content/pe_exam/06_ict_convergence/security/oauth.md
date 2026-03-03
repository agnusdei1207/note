+++
title = "OAuth 2.0 (오픈 인증)"
date = 2025-03-01

[extra]
categories = "pe_exam-ict_convergence"
+++

# OAuth 2.0 (오픈 인증)

## 핵심 인사이트 (3줄 요약)
> **OAuth 2.0은 사용자 비밀번호를 제3자 앱에 노출하지 않고, 제한된 범위의 리소스 접근 권한을 안전하게 위임하는 개방형 인가(Authorization) 프로토콜**이다.
> "구글로 로그인", "페이스북 계정으로 계속하기" 등의 소셜 로그인과 API 접근 권한 부여에 표준으로 사용된다.
> Access Token, Refresh Token, Authorization Code 등의 흐름을 통해 보안성과 사용자 편의성을 동시에 확보하며, OIDC(OpenID Connect)와 결합하여 인증+인가를 통합 지원한다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: OAuth 2.0(Open Authorization 2.0)은 사용자가 자신의 비밀번호를 제3자 애플리케이션에 공유하지 않고도, 특정 리소스(프로필, 이메일, 사진 등)에 대한 제한된 접근 권한을 안전하게 위임할 수 있게 하는 개방형 인가 프로토콜이다. IETF RFC 6749로 표준화되어 있다.

> **비유**: "호텔 체크인 시 발급받는 키카드" — 호텔 전체 마스터 키(비밀번호)를 주는 게 아니라, 특정 객실(특정 리소스)만 열 수 있는 키카드(Access Token)를 발급해 주는 것과 같다. 키카드는 일정 시간 후 만료되고, 필요한 권한만 가진다.

**등장 배경** (필수: 3가지 이상 기술):

1. **기존 문제점**: OAuth 1.0은 암호화 복잡도가 높고 구현이 어려웠으며, 데스크톱/모바일 앱 지원이 부족했다. 또한 비밀번호 공유 방식(Password Anti-pattern)이 만연하여 보안 사고 위험이 컸다.

2. **기술적 필요성**: 모바일 앱, SPA(Single Page Application), IoT 기기 등 다양한 클라이언트 환경을 지원하고, HTTPS 기반으로 단순화된 보안 모델을 제공할 필요가 있었다.

3. **시장/산업 요구**: 소셜 로그인, API 경제(API Economy), SaaS 연동 등 제3자 앱에 안전하게 권한을 위임하는 표준 방식에 대한 글로벌 플랫폼(Google, Facebook, Microsoft)의 합의와 요구가 있었다.

**핵심 목적**: 사용자의 비밀번호 노출 없이 제3자 애플리케이션에 제한된 리소스 접근 권한을 안전하게 위임하고, 사용자 경험(UX)을 개선하면서 보안성을 유지하는 것이다.

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **Resource Owner** | 리소스 소유자 (사용자) | 권한 부여 승인/거부 의사 결정 | 호텔 투숙객 |
| **Client** | 제3자 애플리케이션 | 사용자 대신 리소스 접근 요청 | 여행사 앱 |
| **Authorization Server** | 인가 서버 | 사용자 인증, 토큰 발급 | 호텔 프론트데스크 |
| **Resource Server** | 리소스 서버 | 보호된 리소스 보관, 토큰 검증 | 호텔 객실 |
| **Access Token** | 접근 토큰 | 리소스 접근용 자격증명, 수명 제한 | 키카드 |
| **Refresh Token** | 갱신 토큰 | 새 Access Token 발급용, 수명 김 | 재발급 쿠폰 |

**구조 다이어그램** (필수: ASCII 아트):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OAuth 2.0 Authorization Code Flow                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌────────────────┐                        ┌────────────────────────────┐  │
│  │ Resource Owner │                        │   Authorization Server     │  │
│  │    (사용자)     │                        │    (Google/Facebook)       │  │
│  │                │                        │                            │  │
│  │   👤 사용자    │                        │  ┌──────────────────────┐  │  │
│  │                │                        │  │  /authorize          │  │  │
│  └───────┬────────┘                        │  │  (인증+동의 화면)     │  │  │
│          │                                 │  └──────────┬───────────┘  │  │
│          │                                 │             │              │  │
│          │  (A) 로그인 요청                │             │              │  │
│          │                                 │  ┌──────────┴───────────┐  │  │
│          │                                 │  │  /token              │  │  │
│          │                                 │  │  (토큰 발급)         │  │  │
│          │                                 │  └──────────────────────┘  │  │
│          │                                 └─────────────┬──────────────┘  │
│          │                                               │                │
│          ▼                                               │                │
│  ┌────────────────┐                                      │                │
│  │     Client     │                                      │                │
│  │  (제3자 앱)    │                                      │                │
│  │                │                                      │                │
│  │  ┌──────────┐  │   (B) 인증 요청                      │                │
│  │  │client_id │  │   GET /authorize?                   │                │
│  │  │redirect  │──┼─────────────────────────────────────→│                │
│  │  │scope     │  │   response_type=code                │                │
│  │  │state     │  │   &client_id=xxx                    │                │
│  │  └──────────┘  │   &redirect_uri=xxx                 │                │
│  │                │   &scope=profile email              │                │
│  │                │                                      │                │
│  │                │   (C) 사용자 로그인 + 동의            │                │
│  │                │←────────────────────────────────────→│                │
│  │                │   (브라우저 리다이렉트)               │                │
│  │                │                                      │                │
│  │                │   (D) Authorization Code 반환        │                │
│  │                │←─────────────────────────────────────│                │
│  │                │   redirect_uri?code=xyz&state=abc    │                │
│  │                │                                      │                │
│  │                │   (E) 토큰 요청 (Backend-to-Backend) │                │
│  │                │   POST /token                        │                │
│  │                │   grant_type=authorization_code      │                │
│  │                │──┼────────────────────────────────────→                │
│  │                │   &code=xyz                          │                │
│  │                │   &client_id=xxx                     │                │
│  │                │   &client_secret=SECRET              │                │
│  │                │                                      │                │
│  │                │   (F) Access Token + Refresh Token   │                │
│  │                │←─────────────────────────────────────│                │
│  │                │   {"access_token": "...",           │                │
│  │                │    "refresh_token": "...",          │                │
│  │                │    "expires_in": 3600}              │                │
│  │                │                                      │                │
│  └───────┬────────┘                                      │                │
│          │                                               │                │
│          │ (G) API 요청 + Access Token                   │                │
│          ▼                                               │                │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │                     Resource Server                                 │   │
│  │                     (Google API)                                    │   │
│  │                                                                     │   │
│  │   GET /userinfo                                                     │   │
│  │   Authorization: Bearer <access_token>                             │   │
│  │                                                                     │   │
│  │   ┌──────────────────────────────────────────────────────────────┐ │   │
│  │   │  1. 토큰 검증 (서명, 만료, 권한)                              │ │   │
│  │   │  2. 리소스 반환                                               │ │   │
│  │   │  {"name": "홍길동", "email": "user@example.com"}            │ │   │
│  │   └──────────────────────────────────────────────────────────────┘ │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):

```
① 인증 요청 → ② 사용자 동의 → ③ Auth Code 발급 → ④ 토큰 교환 → ⑤ 리소스 접근 → ⑥ 토큰 갱신
```

- **1단계 (인증 요청)**: Client가 사용자를 Authorization Server의 /authorize 엔드포인트로 리다이렉트. client_id, redirect_uri, scope, state 파라미터 전달
- **2단계 (사용자 동의)**: 사용자가 Authorization Server에서 로그인 후, Client가 요청한 권한 범위(scope)에 대한 동의(Consent) 수행
- **3단계 (Auth Code 발급)**: Authorization Server가 redirect_uri로 Authorization Code(일회용)를 전달. state 파라미터로 CSRF 방지
- **4단계 (토큰 교환)**: Client가 Authorization Code를 /token 엔드포인트로 전송. client_secret 포함하여 서버 간 통신으로 Access Token 획득
- **5단계 (리소스 접근)**: Client가 Access Token을 Authorization 헤더(Bearer Token)에 포함하여 Resource Server API 호출
- **6단계 (토큰 갱신)**: Access Token 만료 시 Refresh Token으로 새 Access Token 발급 (사용자 재인증 불필요)

**핵심 알고리즘/공식** (해당 시 필수):

```
Authorization Code Flow 보안 검증:
┌─────────────────────────────────────────────────────────────────┐
│  1. CSRF 방지: state 파라미터 검증                               │
│     if (received_state != stored_state) → Reject                │
│                                                                  │
│  2. Redirect URI 검증:                                           │
│     if (redirect_uri != registered_redirect_uri) → Reject       │
│                                                                  │
│  3. PKCE (Proof Key for Code Exchange):                         │
│     code_verifier = random(43-128 chars)                        │
│     code_challenge = BASE64URL(SHA256(code_verifier))           │
│     Token Request: code_verifier 검증                            │
└─────────────────────────────────────────────────────────────────┘

Token 구조 (JWT 형태인 경우):
┌─────────────────────────────────────────────────────────────────┐
│  Access Token = Header.Payload.Signature                        │
│                                                                  │
│  Header:  {"alg": "RS256", "typ": "JWT"}                       │
│  Payload: {"sub": "user123", "aud": "client_id",               │
│            "scope": "profile email",                            │
│            "exp": 1516239022, "iat": 1516239022}               │
│  Signature: RSASHA256(                                          │
│    base64UrlEncode(header) + "." +                             │
│    base64UrlEncode(payload),                                   │
│    private_key                                                  │
│  )                                                              │
└─────────────────────────────────────────────────────────────────┘
```

**코드 예시** (필수: Python 또는 의사코드):

```python
"""
OAuth 2.0 Authorization Code Flow 구현 예시
Flask 기반 웹 애플리케이션에서의 소셜 로그인
"""

import secrets
import hashlib
import base64
import requests
from dataclasses import dataclass
from typing import Optional, Dict
from flask import Flask, request, redirect, session, jsonify
import urllib.parse

@dataclass
class OAuthConfig:
    """OAuth 2.0 설정"""
    client_id: str
    client_secret: str
    redirect_uri: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    scope: str

class OAuthClient:
    """OAuth 2.0 클라이언트 구현"""

    def __init__(self, config: OAuthConfig):
        self.config = config
        self.state_store = {}  # 실제로는 Redis 등 사용

    def generate_pkce_verifier(self) -> str:
        """PKCE code_verifier 생성 (43~128자)"""
        return secrets.token_urlsafe(64)

    def generate_pkce_challenge(self, verifier: str) -> str:
        """PKCE code_challenge 생성 (S256 방식)"""
        data = verifier.encode('utf-8')
        digest = hashlib.sha256(data).digest()
        return base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')

    def get_authorization_url(self, state: str, code_challenge: str) -> str:
        """인증 URL 생성"""
        params = {
            'response_type': 'code',
            'client_id': self.config.client_id,
            'redirect_uri': self.config.redirect_uri,
            'scope': self.config.scope,
            'state': state,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        }

        # state 저장 (CSRF 방지)
        self.state_store[state] = {'code_challenge': code_challenge}

        url = f"{self.config.authorization_endpoint}?{urllib.parse.urlencode(params)}"
        return url

    def exchange_code_for_token(
        self,
        code: str,
        state: str,
        code_verifier: str
    ) -> Optional[Dict]:
        """Authorization Code를 Token으로 교환"""
        # state 검증
        if state not in self.state_store:
            raise ValueError("Invalid state parameter")

        stored = self.state_store.pop(state)

        # PKCE 검증
        expected_challenge = self.generate_pkce_challenge(code_verifier)
        if expected_challenge != stored['code_challenge']:
            raise ValueError("PKCE verification failed")

        # Token 요청
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.config.redirect_uri,
            'client_id': self.config.client_id,
            'client_secret': self.config.client_secret,
            'code_verifier': code_verifier
        }

        response = requests.post(
            self.config.token_endpoint,
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        if response.status_code != 200:
            raise Exception(f"Token request failed: {response.text}")

        return response.json()

    def refresh_access_token(self, refresh_token: str) -> Optional[Dict]:
        """Refresh Token으로 새 Access Token 발급"""
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.config.client_id,
            'client_secret': self.config.client_secret
        }

        response = requests.post(
            self.config.token_endpoint,
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        if response.status_code != 200:
            raise Exception(f"Token refresh failed: {response.text}")

        return response.json()

    def get_userinfo(self, access_token: str) -> Dict:
        """Access Token으로 사용자 정보 조회"""
        response = requests.get(
            self.config.userinfo_endpoint,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        if response.status_code != 200:
            raise Exception(f"UserInfo request failed: {response.text}")

        return response.json()


# Flask 애플리케이션 예시
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Google OAuth 2.0 설정 (예시)
google_config = OAuthConfig(
    client_id="your-client-id.apps.googleusercontent.com",
    client_secret="your-client-secret",
    redirect_uri="http://localhost:5000/callback",
    authorization_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
    token_endpoint="https://oauth2.googleapis.com/token",
    userinfo_endpoint="https://www.googleapis.com/oauth2/v2/userinfo",
    scope="openid profile email"
)

oauth_client = OAuthClient(google_config)


@app.route('/')
def index():
    """홈페이지 - 로그인 링크 제공"""
    return '''
    <h1>OAuth 2.0 Demo</h1>
    <a href="/login">Google로 로그인</a>
    '''


@app.route('/login')
def login():
    """로그인 시작 - Authorization Server로 리다이렉트"""
    # PKCE verifier/challenge 생성
    code_verifier = oauth_client.generate_pkce_verifier()
    code_challenge = oauth_client.generate_pkce_challenge(code_verifier)

    # state 생성
    state = secrets.token_urlsafe(16)

    # 세션에 저장
    session['code_verifier'] = code_verifier
    session['state'] = state

    # 인증 URL 생성 및 리다이렉트
    auth_url = oauth_client.get_authorization_url(state, code_challenge)
    return redirect(auth_url)


@app.route('/callback')
def callback():
    """Authorization Server로부터 콜백"""
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')

    if error:
        return f"Error: {error}", 400

    # state 검증
    if state != session.get('state'):
        return "Invalid state", 400

    # code_verifier 가져오기
    code_verifier = session.get('code_verifier')

    try:
        # Token 교환
        tokens = oauth_client.exchange_code_for_token(code, state, code_verifier)

        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')
        expires_in = tokens.get('expires_in')

        # 사용자 정보 조회
        userinfo = oauth_client.get_userinfo(access_token)

        return jsonify({
            'message': 'Login successful!',
            'user': userinfo,
            'token_info': {
                'expires_in': expires_in,
                'has_refresh_token': refresh_token is not None
            }
        })

    except Exception as e:
        return f"Error: {str(e)}", 400


@app.route('/refresh', methods=['POST'])
def refresh():
    """토큰 갱신"""
    refresh_token = session.get('refresh_token')

    if not refresh_token:
        return "No refresh token", 400

    try:
        tokens = oauth_client.refresh_access_token(refresh_token)
        return jsonify(tokens)
    except Exception as e:
        return f"Error: {str(e)}", 400


if __name__ == '__main__':
    print("=== OAuth 2.0 Authorization Code Flow Demo ===")
    print("1. Visit http://localhost:5000")
    print("2. Click 'Google로 로그인'")
    print("3. Authorize the application")
    print("4. View user info")
    app.run(debug=True, port=5000)
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):

| 장점 | 단점 |
|-----|------|
| **비밀번호 노출 방지**: 사용자 비밀번호를 제3자 앱에 절대 공유하지 않음 | **구현 복잡도**: 다양한 Grant Type, 보안 고려사항으로 구현 난이도 높음 |
| **세분화된 권한 제어**: Scope를 통해 필요한 최소 권한만 부여 가능 | **토큰 관리 부담**: Access Token 만료, Refresh Token 저장 등 클라이언트 관리 필요 |
| **SSO/소셜 로그인 지원**: Google, Facebook 등 계정으로 간편 로그인 구현 | **의존성**: Authorization Server 장애 시 서비스 영향 |
| **표준 프로토콜**: RFC 6749 표준, 다양한 라이브러리/플랫폼 지원 | **토큰 탈취 위험**: Access Token 탈취 시 만료 전까지 악용 가능 |
| **다양한 클라이언트 지원**: 웹, 모바일, SPA, 서버 간 통신 등 | **리다이렉트 필요**: Authorization Code Flow는 필수적으로 리다이렉트 발생 |

**대안 기술 비교** (필수: 최소 2개 대안):

| 비교 항목 | OAuth 2.0 | OpenID Connect (OIDC) | SAML 2.0 |
|---------|----------|----------------------|----------|
| **핵심 목적** | ★ 인가 (Authorization) | 인가 + 인증 (Authentication) | 인증 + 인가 (Enterprise) |
| **토큰 형식** | Access Token (불투명/JWT) | ★ ID Token (JWT) + Access Token | SAML Assertion (XML) |
| **프로토콜** | REST/JSON | REST/JSON | SOAP/XML |
| **사용자 정보** | API 호출로 조회 | ★ 토큰에 포함 (claims) | Assertion에 포함 |
| **복잡도** | 중간 | ★ 낮음 (OAuth 기반) | 높음 |
| **적합 환경** | API 접근 권한 | ★ 소셜 로그인, SSO | 엔터프라이즈 SSO |

| 비교 항목 | Authorization Code | Client Credentials | Implicit (Deprecated) |
|---------|-------------------|-------------------|----------------------|
| **사용 시나리오** | ★ 웹/모바일 앱 | 서비스 간 통신 (M2M) | SPA (현재 권장 X) |
| **Client Secret** | 필요 | ★ 필요 | 불필요 |
| **토큰 노출** | 없음 (Backend 교환) | 없음 | ★ 브라우저 노출 |
| **Refresh Token** | 지원 | 미지원 (불필요) | 미지원 |
| **PKCE 권장** | ★ 필수 | 해당 없음 | 해당 없음 |

> **선택 기준**:
> - **웹 애플리케이션**: Authorization Code + PKCE
> - **SPA (React/Vue)**: Authorization Code + PKCE (Implicit 사용 금지)
> - **모바일 앱**: Authorization Code + PKCE
> - **서버 간 통신(M2M)**: Client Credentials
> - **사용자 인증 필요**: OAuth 2.0 + OIDC 조합

**Grant Type 진화 계보**:

```
OAuth 2.0 Grant Types:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────────────────┐                                       │
│  │ Authorization Code  │ ──→ 권장: 모든 웹/모바일 앱            │
│  │ + PKCE              │                                       │
│  └─────────────────────┘                                       │
│           ↑                                                     │
│           │ 진화                                                 │
│  ┌────────┴────────────┐                                       │
│  │ Authorization Code  │ ──→ 레거시 (PKCE 없이)                │
│  │ (Classic)           │                                       │
│  └─────────────────────┘                                       │
│                                                                 │
│  ┌─────────────────────┐                                       │
│  │ Implicit            │ ──→ ★ 폐지됨 (RFC 6819)              │
│  │                     │     Authorization Code + PKCE 사용    │
│  └─────────────────────┘                                       │
│                                                                 │
│  ┌─────────────────────┐                                       │
│  │ Client Credentials  │ ──→ M2M (서비스 계정)                 │
│  │                     │                                       │
│  └─────────────────────┘                                       │
│                                                                 │
│  ┌─────────────────────┐                                       │
│  │ Resource Owner      │ ──→ ★ 권장 안 함 (비밀번호 노출)      │
│  │ Password Credentials│     레거시 시스템만 사용              │
│  └─────────────────────┘                                       │
│                                                                 │
│  ┌─────────────────────┐                                       │
│  │ Refresh Token       │ ──→ 토큰 갱신 전용                    │
│  │                     │                                       │
│  └─────────────────────┘                                       │
│                                                                 │
│  ┌─────────────────────┐                                       │
│  │ Device Code         │ ──→ TV, CLI, IoT 기기                 │
│  │                     │                                       │
│  └─────────────────────┘                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Ⅳ. 실무 적용 방안 (필수: 전문가 판단력 증명)

**전문가적 판단** (필수: 3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **소셜 로그인 서비스** | Google/Facebook/Kakao OAuth + OIDC 연동, Authorization Code + PKCE 구현 | 회원가입 전환율 40% 향상, 비밀번호 관리 비용 80% 절감 |
| **API 플랫폼 (Open API)** | Client Credentials Grant로 파트너사 API 접근 권한 부여, Scope 기반 요금제 차등 | API 남용 95% 차단, 과금 정확도 100% |
| **B2B SaaS 연동** | OAuth 2.0으로 타사 SaaS(Salesforce, Slack)와 안전한 데이터 연동 | 연동 구축 시간 60% 단축, 보안 인증 획득 |

**실제 도입 사례** (필수: 구체적 기업/서비스):

- **사례 1: 토스(Toss)** - OAuth 2.0 + OIDC 기반 소셜 로그인으로 카카오, 네이버, 구글 계정 연동. 회원가입 단계 간소화로 가입 전환율 35% 향상. 비밀번호 재설정 문의 70% 감소.

- **사례 2: Stripe** - OAuth 2.0 기반 Connect 플랫폼으로, 마켓플레이스 판매자들이 Stripe 결제 기능을 연동. 판매자가 직접 Stripe 계정 없이도 결제 처리 가능. Scope 기반으로 결제 조회만 허용 등 세분화된 권한 제어.

- **사례 3: Slack** - OAuth 2.0으로 서드파티 앱 연동. 사용자가 Slack 비밀번호 없이 타 앱(Zoom, Google Drive)에 Slack 권한 부여. 워크스페이스별, 채널별 Scope 제어로 최소 권한 원칙 실현.

**도입 시 고려사항** (필수: 4가지 관점):

1. **기술적**:
   - Grant Type 선택: 클라이언트 유형에 맞는 적절한 흐름 선택
   - PKCE 구현: 모바일/SPA에서 필수 (RFC 7636)
   - Token 저장소: 안전한 Refresh Token 저장 (암호화)
   - HTTPS 필수: 모든 OAuth 통신은 HTTPS 위에서 수행

2. **운영적**:
   - 토큰 만료 정책: Access Token 1시간, Refresh Token 30일 등
   - 토큰 폐기(Revoke): 로그아웃 시 토큰 무효화 처리
   - 로그 및 감사: 인증 이벤트 로깅, 이상 징후 탐지
   - 다중 Provider: Google, Facebook 등 다중 IdP 지원

3. **보안적**:
   - state 파라미터: CSRF 방지 필수
   - Redirect URI 검증: 사전 등록된 URI만 허용
   - Scope 최소화: 필요한 최소 권한만 요청
   - Token 탈취 대응: 짧은 만료, 감사 로그, 이상 탐지

4. **경제적**:
   - IdP 비용: Google/Facebook 무료, Auth0/Okta 유료
   - 개발 비용: OAuth 라이브러리 vs 직접 구현
   - 운영 비용: 토큰 저장소, 로그 저장소
   - 규정 준수: GDPR, CCPA 등 개인정보 처리 기준

**주의사항 / 흔한 실수** (필수: 최소 3개):

- **Implicit Grant 사용**: 브라우저에 토큰이 노출되어 보안 취약. 반드시 Authorization Code + PKCE 사용 권장
- **Refresh Token 부주의 저장**: Refresh Token이 탈취되면 장기간 악용 가능. 반드시 암호화하여 저장, 사용 시마다 검증
- **state 파라미터 누락**: CSRF 공격에 취약. 반드시 state 파라미터를 생성하고 콜백에서 검증

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):

```
📌 OAuth 2.0 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────────────────┐
│                        OAuth 2.0 연관 개념 맵                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│      ┌──────────┐                        ┌──────────┐                      │
│      │   SAML   │←────────────────────→│ OAuth 2.0│←────────────────────→│ JWT      │
│      │(엔터프라이즈)│                        │          │                        │(토큰형식) │
│      └──────────┘                        └────┬─────┘                        └──────────┘
│           ↑                                   │                                   ↑
│           │                                   │                                   │
│           ↓                                   ↓                                   │
│      ┌──────────┐                        ┌──────────┐                        │
│      │OpenID    │←────────────────────→│  PKCE    │                        │
│      │Connect   │                        │(보안강화) │                        │
│      │(인증확장) │                        └──────────┘                        │
│      └──────────┘                        ┌──────────┐                        │
│                                          │  Token   │                        │
│                                          │  관리    │                        │
│                                          └──────────┘                        │
│                                                ↑                              │
│                                                │                              │
│                                          ┌──────────┐                        │
│                                          │   SSO    │←───────────────────────┘
│                                          │(통합로그인)│
│                                          └──────────┘
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| **JWT** | 토큰 형식 | OAuth Access Token의 표준 포맷 | `[jwt](./jwt.md)` |
| **OpenID Connect** | 인증 확장 | OAuth 2.0 위에 인증 계층 추가 | `[oidc](./oidc.md)` |
| **PKCE** | 보안 강화 | 모바일/SPA용 Authorization Code 보안 | OAuth 확장 (RFC 7636) |
| **SSO** | 통합 로그인 | OAuth를 활용한 Single Sign-On | `[sso](./sso.md)` |
| **Token Binding** | 보안 기술 | 토큰과 클라이언트 결합으로 탈취 방지 | OAuth 2.0 Token Binding |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| **보안** | 비밀번호 노출 방지, 세분화된 권한 제어 | 비밀번호 유출 사고 100% 예방 |
| **사용자 경험** | 소셜 로그인으로 간편 가입/로그인 | 가입 전환율 30% 향상 |
| **개발 효율** | 표준 프로토콜로 인증 시스템 구축 시간 단축 | 인증 개발 기간 50% 단축 |
| **호환성** | 다양한 IdP와 연동 가능 | 멀티 IdP 지원 100% |

**미래 전망** (필수: 3가지 관점):

1. **기술 발전 방향**: OAuth 2.1로 통합(Javascript 보안 강화), DPoP(Demonstrating Proof of Possession)로 토큰 바인딩, FIDO/WebAuthn과 결합한 패스워드리스 인증.

2. **시장 트렌드**: CIAM(Customer Identity and Access Management) 플랫폼 성장, Zero Trust 아키텍처 내 토큰 기반 인증 확대, API Economy로 OAuth 활용 확대.

3. **후속 기술**: GNAP(Grant Negotiation and Authorization Protocol)이 차세대 표준으로 연구 중. 기존 OAuth의 복잡성을 줄이고 보안을 강화하는 방향.

> **결론**: OAuth 2.0은 현대 웹/모바일 애플리케이션의 인가 표준으로, 비밀번호 없이 안전하게 권한을 위임하는 핵심 프로토콜이다. OIDC와 결합하여 인증+인가를 통합 지원하며, PKCE, DPoP 등으로 지속 보안 강화되고 있다.

> **참고 표준**: IETF RFC 6749(OAuth 2.0), RFC 6750(Bearer Token), RFC 7636(PKCE), RFC 8252(OAuth 2.0 for Native Apps), OpenID Connect Core 1.0

---

## 어린이를 위한 종합 설명 (필수)

**OAuth 2.0을 쉽게 이해해보자!**

OAuth 2.0은 마치 **호텔 체크인 시 발급받는 키카드** 같아요.

**개념 설명**:
여행을 갔을 때, 호텔에 도착하면 프론트데스크에서 체크인을 해요. 직원은 우리 신분증을 확인하고, "이 분은 505호 손님입니다"라고 확인해 줘요. 그리고 505호 객실만 열 수 있는 키카드를 줘요. 이 키카드는 호텔 전체를 다 열 수 있는 마스터 키가 아니에요. 딱 우리 방만 열 수 있죠. OAuth 2.0도 이런 거예요. 구글이나 페이스북이라는 "호텔"에서 우리가 다른 앱(여행사 앱)에게 딱 필요한 정보만 볼 수 있는 "키카드"를 발급해 주는 거예요.

**동작 원리 설명**:
여행사 앱이 "고객님의 구글 프로필 정보가 필요해요"라고 하면, 우리는 구글 로그인 화면으로 이동해요. 구글이 "여행사 앱이 이름과 이메일을 요청했어요. 허락하시겠습니까?"라고 물어보죠. 우리가 "네"라고 하면, 구글이 여행사 앱에게 임시 키(Access Token)를 줘요. 이 키로 여행사 앱은 구글에서 딱 우리 이름과 이메일만 가져올 수 있어요. 우리 구글 비밀번호는 여행사 앱이 절대 알 수 없어요!

**장점/효과 설명**:
OAuth 덕분에 우리는 모든 앱마다 새로운 비밀번호를 만들 필요가 없어요. 구글이나 페이스북 계정 하나로 수많은 앱에 가입할 수 있죠. 그리고 비밀번호를 여기저기 공유하지 않아도 돼서 훨씬 안전해요. 만약 어떤 앱이 나쁜 마음을 먹어도, 우리 구글 비밀번호를 모르니까 구글 계정을 털어갈 수 없어요!

---
