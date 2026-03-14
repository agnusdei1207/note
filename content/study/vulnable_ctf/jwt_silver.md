+++
title = "VulnABLE CTF [LUXORA]: JWT Attacks 🥈 Silver (Weak Secret Cracking)"
description = "LUXORA 플랫폼의 취약한 JWT 비밀키를 오프라인 브루트포싱으로 크랙하여 토큰을 위조하는 시나리오"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "JWT", "Silver", "Brute Force", "Hashcat"]
+++

# VulnABLE CTF [LUXORA]: JWT Attacks 🥈 Silver

Bronze 난이도에서는 `none` 알고리즘을 사용하여 서명 검증을 통과했습니다. 하지만 **Silver 난이도**(`/jwt/silver`)에서는 서버가 똑똑해져서 `alg: none`을 완벽하게 차단하고, 오직 `HS256`만 허용하도록 패치되었습니다.

그렇다면 이제는 꼼수를 부릴 수 없고, 정당한 서명(Signature)을 만들어내야 합니다. 서명을 만들려면 서버가 가진 **'비밀키(Secret Key)'**를 알아야 합니다. 어떻게 알아낼 수 있을까요? 바로 오프라인 브루트포싱(Offline Brute-forcing)입니다.

---

## 🕒 1. 타겟 탐색 및 토큰 획득 (Reconnaissance)

이전과 동일하게 브라우저 개발자 도구를 통해 로그인된 사용자의 JWT를 탈취합니다.

**[획득한 JWT]**
```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJ1c2VybmFtZSI6InVzZXIiLCJyb2xlIjoiZ3Vlc3QifQ.
tG3z_6T_uM7E6m... (서명 부분 생략)
```

**[해커의 사고 과정]**
* 이 토큰의 헤더(`HS256`)와 페이로드, 그리고 최종 서명값을 나는 알고 있다.
* `HS256`은 HMAC-SHA256 알고리즘을 뜻하며, 이는 `비밀키`와 `헤더+페이로드`를 섞어서 해시를 만든 것이다.
* 만약 개발자가 비밀키를 `secret`, `123456`, `luxora` 처럼 아주 쉬운 단어로 설정해두었다면? 
* 내 컴퓨터(로컬)에서 세상의 수많은 단어들을 비밀키로 대입해보면서 토큰의 서명값과 일치하는지 비교(Offline Cracking)해보자!

---

## 🕒 2. 오프라인 크래킹 수행 (Exploitation)

온라인으로 서버에 계속 로그인 시도를 하면(Online Brute-force) 계정이 잠기거나 IP가 차단됩니다. 하지만 이미 탈취한 토큰을 내 컴퓨터에서 해독하는 **오프라인 크래킹**은 방화벽이나 차단 시스템의 영향을 전혀 받지 않으며 1초에 수백만 번의 연산이 가능합니다.

### 💡 사용 도구: Hashcat (또는 John the Ripper)
강력한 패스워드 크래킹 도구인 Hashcat을 사용합니다. 사전 파일(Wordlist)로는 해커들의 바이블인 `rockyou.txt`를 활용합니다.

```bash
# jwt.txt 파일에 탈취한 전체 JWT 문자열을 저장
$ echo "eyJhbGci...생략..." > jwt.txt

# Hashcat을 이용해 JWT 크래킹 (모듈 번호 16500 = JWT)
$ hashcat -m 16500 -a 0 jwt.txt /usr/share/wordlists/rockyou.txt
```

### 🔍 크래킹 결과
잠시 후(보통 몇 초~몇 분 이내), Hashcat이 비밀키를 찾아냅니다!

```text
...
eyJhbGciOiJIUzI1... : supersecret123
...
Status...........: Cracked
```

개발자가 사용한 서버의 비밀키가 `supersecret123` 임을 알아냈습니다!

---

## 🕒 3. 토큰 위조 및 권한 탈취 🚩

비밀키를 알았으니, 이제 내 마음대로 조작된 페이로드를 만들고 진짜 서명을 생성할 수 있습니다. `jwt.io` 사이트에 접속합니다.

1. **Payload 수정**: 
   `"role": "guest"` ➔ `"role": "admin"` 으로 변경
2. **Verify Signature 란에 비밀키 입력**: 
   알아낸 비밀키 `supersecret123` 입력
3. **새로운 토큰 복사**: 하단에 새로 생성된 (완벽하게 서명된) JWT를 복사합니다.

이 조작된 토큰을 쿠키에 덮어쓰고 관리자 페이지(`/jwt/silver/admin`)로 접근합니다.

```http
GET /jwt/silver/admin HTTP/1.1
Cookie: token=[내가 새로 만든 관리자 토큰]
```

### 🔍 공격 결과
서버는 이 토큰의 서명을 `supersecret123`으로 검증해보고 "완벽하게 일치하군!"이라며 우리를 관리자로 인정합니다.

```json
{
  "message": "Welcome Admin! Access Granted.",
  "flag": "FLAG{JWT_🥈_WEAK_SECRET_D8F1A2}"
}
```

**플래그 획득:** `FLAG{JWT_🥈_WEAK_SECRET_D8F1A2}`

---

## 🛡️ 방어 대책 (Mitigation)

1. **강력한 비밀키(Secret Key) 사용**: JWT의 보안은 오직 비밀키의 길이나 복잡도에 달려있습니다. 절대로 사람이 외울 수 있는 사전 단어를 쓰지 말고, 최소 256비트(32바이트) 이상의 고난수 문자열(Random Cryptographic Key)을 생성하여 환경 변수에 저장해야 합니다.
   * `openssl rand -base64 32` 와 같은 명령어로 생성하는 것이 좋습니다.
2. **비대칭 키(RS256) 사용 고려**: HS256(대칭키) 대신 RS256(비대칭키) 알고리즘을 사용하면, 비밀키(Private Key)는 서버 깊숙한 곳에 보관하고 서명 검증은 공개키(Public Key)로만 하므로 키 유출 위험과 크래킹 위험이 대폭 감소합니다.

다음 **Gold 🥇 난이도**에서는 비대칭 키(RS256)를 대칭 키(HS256)로 강제 변환시키는 알고리즘 혼동 공격(Algorithm Confusion Attack)을 살펴보겠습니다!