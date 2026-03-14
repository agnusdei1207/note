+++
title = "VulnABLE CTF [LUXORA]: SQL Injection 🥉 Bronze (Basic Exploitation)"
description = "LUXORA 플랫폼의 SQL Injection Bronze 난이도 플래그 획득 시나리오 및 원리 상세 분석"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SQL Injection", "Bronze"]
+++

# VulnABLE CTF [LUXORA]: SQL Injection 🥉 Bronze

안녕하세요! 이번 시나리오에서는 LUXORA e-commerce 플랫폼의 **SQL Injection 🥉 Bronze** 난이도 플래그(`FLAG{SQLI_🥉_INJECTION_A3F2B1}`)를 획득하는 과정을 아주 상세하게 다루어 보겠습니다. 모의해킹 초보자분들이 공격의 원리와 사고 과정을 쉽게 이해하실 수 있도록 단계별로 설명합니다.

---

## 🕒 1. 타겟 탐색 및 힌트 발견 (Reconnaissance)

웹 브라우저를 열고 LUXORA 플랫폼(예: `http://localhost:3000`)에 접속합니다. 메뉴를 둘러보던 중 `README.md`에서 확인했던 취약점 라우트인 `/sqli/bronze` 페이지로 이동합니다.

### 🔍 화면 분석
`/sqli/bronze` 페이지에는 사용자 ID를 입력하여 사용자 정보를 조회하는 간단한 검색 폼(Form)이 있습니다.
URL을 보면 `http://localhost:3000/sqli/bronze?id=1` 형태로 GET 파라미터를 통해 값을 전달하고 있습니다.

화면 출력:
```text
User ID: 1
Name: Alice
Email: alice@luxora.test
```

**[해커의 사고 과정]**
* 입력값 `id=1`이 서버로 전달되어 데이터베이스에서 정보를 가져오고 있구나.
* 만약 백엔드 코드가 입력값을 제대로 검증하지 않고 SQL 쿼리문에 그대로 이어 붙인다면(String Concatenation), SQL Injection이 가능할 것이다.
* 가장 기본적인 취약점 확인 방법인 **홑따옴표(`'`)**를 입력해서 에러가 발생하는지 확인해보자!

---

## 🕒 2. 취약점 식별 (Vulnerability Identification)

URL의 `id` 파라미터 값 뒤에 홑따옴표(`'`)를 넣어봅니다.

```http
GET /sqli/bronze?id=1'
```

### 🚨 에러 발생!
화면에 다음과 같은 데이터베이스 에러 메시지가 노출되었습니다.

```text
Error: SQL syntax error near ''1''' at line 1.
```

**[판단과 이유]**
* 에러가 발생했다는 것은 내가 입력한 홑따옴표(`'`)가 단순한 문자로 처리되지 않고, 데이터베이스 내부의 **SQL 문법을 깨뜨렸음**을 의미합니다.
* 서버의 백엔드 쿼리가 대략 다음과 같이 작성되어 있을 것이라 확신합니다:
  `SELECT * FROM users WHERE id = '$id'`
* 내가 `1'`을 넣었기 때문에 쿼리가 `WHERE id = '1''`이 되어 따옴표 짝이 맞지 않아 문법 오류가 발생한 것입니다.
* 이는 전형적이고 고전적인 **In-band SQL Injection** 취약점입니다. (결과나 에러가 화면에 바로 보이는 형태)

---

## 🕒 3. 공격 수행 및 PoC (Exploitation)

이제 쿼리를 조작하여 데이터베이스가 원래 의도하지 않은 동작을 하도록 만들겠습니다. 가장 기초적인 공격 구문인 `OR 1=1`을 사용해 보겠습니다.

### 💡 공격 원리: 참(True) 조건 만들기
목표 쿼리: `SELECT * FROM users WHERE id = '[입력값]'`

입력값에 `1' OR '1'='1`을 넣는다고 상상해 봅시다.
완성된 쿼리: `SELECT * FROM users WHERE id = '1' OR '1'='1'`

* `id = '1'` 조건이 거짓이더라도, 뒤의 `'1'='1'` 조건이 **항상 참(True)**이기 때문에, 데이터베이스는 `users` 테이블에 있는 **모든 데이터**를 화면에 출력하게 됩니다.

### 🚀 페이로드 전송
URL에 다음과 같이 입력합니다. (URL 인코딩 주의: 공백은 `%20` 또는 `+`로 변환)

```http
GET /sqli/bronze?id=1' OR '1'='1
```

### 🔍 공격 결과
화면에 단 1명의 유저가 아닌, 숨겨져 있던 관리자(Admin)를 포함한 데이터베이스 내 모든 유저의 정보가 쏟아져 나옵니다!

```text
User ID: 1, Name: Alice, Email: alice@luxora.test
User ID: 2, Name: Bob, Email: bob@luxora.test
...
User ID: 999, Name: Admin, Email: admin@luxora.test
[!] CONGRATULATIONS! FLAG: FLAG{SQLI_🥉_INJECTION_A3F2B1}
```

---

## 🕒 4. 플래그 획득 및 원리 요약 🚩

**플래그 획득:** `FLAG{SQLI_🥉_INJECTION_A3F2B1}`

### 📝 왜 이런 공격이 성공했는가?
Bronze 난이도답게 서버에서 사용자의 입력값에 대해 아무런 필터링(Sanitization)을 하지 않았기 때문입니다. 악의적인 SQL 예약어(`OR`, `'`, `=`, `--`)가 그대로 쿼리에 삽입되어 데이터베이스 엔진에서 실행명령어로 해석되었습니다.

### 🛡️ 방어 대책 (Mitigation)
초보 개발자들이 가장 많이 하는 실수입니다. 이를 막기 위한 표준 방어법은 **Prepared Statements (Parameterized Queries)**를 사용하는 것입니다.

* **안전한 코드 (Node.js 예시):**
```javascript
// 입력값을 쿼리의 '구조'가 아닌 순수 '데이터'로만 취급하게 함
db.query("SELECT * FROM users WHERE id = ?", [req.query.id], function(err, results) { ... });
```
이렇게 처리하면 해커가 `1' OR '1'='1`을 입력해도, 데이터베이스는 "아이디가 정말로 `1' OR '1'='1`인 사람을 찾아라"라고 해석하게 되어 공격을 원천적으로 무력화할 수 있습니다.

다음 시간에는 필터링이 일부 적용된 **Silver 🥈 난이도**의 SQL Injection을 어떻게 우회하는지 다루어 보겠습니다!