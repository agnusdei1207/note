import os
BASE = "/Users/pf/workspace/brainscience/content/studynote/09_security/05_web_app_security"

files = {
"464_prototype_pollution.md": (464, "464. Prototype Pollution (JavaScript Prototype Pollution)", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Prototype Pollution은 JavaScript의 프로토타입 체인 메커니즘을 악용해 `Object.prototype`을 오염시킴으로써, 애플리케이션 전체 객체에 악성 속성을 주입하는 취약점이다.
> 2. **가치**: 서버 측(Node.js)에서는 Prototype Pollution이 RCE로 이어질 수 있고, 클라이언트 측에서는 XSS (Cross-Site Scripting) 방어 우회로 활용된다.
> 3. **판단 포인트**: `__proto__`, `constructor`, `prototype` 키를 사용자 입력에서 필터링하거나, `Object.create(null)`로 프로토타입 없는 객체를 생성하는 것이 핵심 방어다.

---

## Ⅰ. 개요 및 필요성

JavaScript에서 모든 객체는 `prototype`을 통해 상위 객체의 속성을 상속받는다. 이 메커니즘 덕분에 `{}.toString()`처럼 모든 객체에서 공통 메서드를 사용할 수 있다.

Prototype Pollution은 이 메커니즘을 역이용한다. 공격자가 `obj.__proto__.adminRole = true`처럼 `__proto__`를 통해 `Object.prototype`에 속성을 추가하면, 이후 생성된 모든 객체가 `adminRole = true`를 가지게 된다. 이는 인증 우회, 권한 상승, 더 나아가 템플릿 엔진이나 eval을 사용하는 코드에서 RCE로 이어진다.

```text
┌──────────────────────────────────────────────────────────────┐
│           Prototype Pollution 개념도                          │
├──────────────────────────────────────────────────────────────┤
│  정상:                                                        │
│  user = {}                                                   │
│  user.__proto__ === Object.prototype  (공통 조상)             │
│                                                              │
│  오염 공격:                                                   │
│  payload = {"__proto__": {"isAdmin": true}}                  │
│  merge(target, payload)  ← 재귀 병합 함수가 취약한 경우      │
│                                                              │
│  결과:                                                        │
│  Object.prototype.isAdmin === true                           │
│  let victim = {}                                             │
│  victim.isAdmin === true  ← 새로 만든 모든 객체가 오염됨     │
└──────────────────────────────────────────────────────────────┘
```

2019년 lodash의 `_.merge()`, `_.set()` 함수에서 Prototype Pollution이 발견됐고(CVE-2019-10744), 이는 수백만 개의 Node.js 프로젝트에 영향을 미쳤다.

📢 **섹션 요약 비유**: Prototype Pollution은 마을 공용 우물(Object.prototype)에 독을 타는 것이다. 이후 우물을 쓰는 모든 사람(객체)이 오염된 물을 마신다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 취약한 코드 패턴

| 취약 패턴 | 코드 예시 | 위험 |
|:---|:---|:---|
| 재귀 merge | lodash _.merge() | Object.prototype 오염 |
| 경로 설정 | lodash _.set(obj, "a.__proto__.x", v) | 오염 가능 |
| JSON 파싱 후 병합 | Object.assign()으로 사용자 JSON 병합 | 제한적 위험 |
| 깊은 클론 | deepClone(userInput) | 재귀 처리 시 위험 |

```text
┌──────────────────────────────────────────────────────────────┐
│              Node.js RCE 경로 (템플릿 엔진)                   │
├──────────────────────────────────────────────────────────────┤
│  1. Object.prototype.outputFunctionName = "x;process.mainModule│
│     .require('child_process').execSync('id')//";             │
│                                                              │
│  2. EJS (Embedded JavaScript) 템플릿 렌더링 시:              │
│     template options에서 outputFunctionName 참조             │
│     → eval(오염된 속성 값) 실행 → RCE!                       │
│                                                              │
│  영향받는 템플릿 엔진: EJS, Handlebars, Pug (구버전)         │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: Node.js RCE는 우물에 탄 독이 요리사의 냄비(템플릿 엔진)를 통해 모든 음식(코드 실행)에 스며드는 것이다.

---

## Ⅲ. 비교 및 연결

| 공격 컨텍스트 | 영향 | 방어 |
|:---|:---|:---|
| 클라이언트 측 | XSS 방어 우회, UI 조작 | 입력 필터링 |
| 서버 측 (Node.js) | 인증 우회, RCE | Object.create(null) |
| 패키지 의존성 | 광범위한 영향 | 라이브러리 업데이트 |

Python의 경우에도 `__class__`, `__base__`, `__subclasses__` 를 통한 유사한 공격(Python SSTI에서 MRO 탐색)이 존재한다.

📢 **섹션 요약 비유**: 클라이언트와 서버 측 Prototype Pollution은 같은 독이 집 안 수돗물(클라이언트)과 마을 공용 식당(서버) 모두에 퍼지는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**방어 코드 패턴**:
```javascript
// 방어 1: 위험한 키 필터링
function safeMerge(target, source) {
    const dangerous = ['__proto__', 'constructor', 'prototype'];
    for (const key of Object.keys(source)) {
        if (dangerous.includes(key)) continue;  // 필터링
        if (typeof source[key] === 'object') {
            safeMerge(target[key] ??= {}, source[key]);
        } else {
            target[key] = source[key];
        }
    }
}

// 방어 2: 프로토타입 없는 객체 생성
const safe = Object.create(null);  // __proto__ 없음

// 방어 3: Object.freeze()로 Object.prototype 고정
Object.freeze(Object.prototype);  // 오염 시도 시 에러 또는 무시
```

📢 **섹션 요약 비유**: Object.freeze()는 공용 우물 위에 투명한 덮개를 씌우는 것이다. 누가 독을 넣으려 해도 덮개 때문에 들어가지 않는다.

---

## Ⅴ. 기대효과 및 결론

Prototype Pollution 방어를 통해 인증 우회, 권한 상승, Node.js RCE, XSS 방어 우회 등 광범위한 공격 체인을 차단할 수 있다. lodash 4.17.21+, jQuery 3.4+, 최신 Node.js 라이브러리들은 이미 패치됐으므로, 의존성 최신화가 가장 빠른 완화 방법이다.

📢 **섹션 요약 비유**: Prototype Pollution 방어 완성은 공용 우물(Object.prototype)을 잠그고, 각 집마다 개별 정수기(Object.create(null))를 설치하는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| __proto__ | 공격 진입점 | 프로토타입 체인 접근 |
| lodash _.merge() | 취약 함수 | CVE-2019-10744 |
| Object.freeze() | 방어 기술 | 프로토타입 동결 |
| EJS (Embedded JavaScript) | RCE 경로 | 오염된 속성 eval 실행 |
| Object.create(null) | 방어 기술 | 프로토타입 없는 객체 |

### 👶 어린이를 위한 3줄 비유 설명
- Prototype Pollution은 마을 공용 식수대(Object.prototype)에 색소를 타는 것이에요.
- 이 식수대에서 물을 받는 모든 집(객체)의 물이 오염돼요.
- 식수대에 자물쇠(Object.freeze)를 달거나, 집마다 개별 정수기(Object.create(null))를 쓰면 안전해요!
"""),

"465_redos.md": (465, "465. ReDoS (Regular Expression Denial of Service)", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ReDoS (Regular Expression Denial of Service, 정규표현식 서비스 거부)는 취약한 정규표현식 패턴에 악의적으로 설계된 입력을 주어, 정규식 엔진의 백트래킹 (Backtracking)이 지수적으로 증가해 서버가 마비되는 공격이다.
> 2. **가치**: 단 하나의 HTTP 요청으로 싱글 스레드 서버(Node.js 이벤트 루프 등)를 수십 초~수 분간 마비시킬 수 있어, 파급력 대비 공격 비용이 매우 낮다.
> 3. **판단 포인트**: 취약한 패턴 특징은 중첩 수량자 `(a+)+`, 교대 중복 `(a|aa)+` 등이며, 재작성(Linear Regex) 또는 타임아웃 설정으로 방어한다.

---

## Ⅰ. 개요 및 필요성

정규표현식 엔진은 매칭 실패 시 백트래킹으로 이전 상태로 돌아가며 다시 시도한다. 대부분의 경우 이 과정은 빠르게 끝나지만, 특정 패턴과 특정 입력이 만나면 백트래킹 횟수가 입력 길이의 지수 함수로 증가한다.

2016년 Stack Overflow는 ReDoS로 34분간 다운됐다(개시). 원인은 `/ +/` 를 처리하는 Markdown 파서의 정규식 취약점이었다. Node.js와 싱글 스레드 이벤트 루프 환경에서 ReDoS는 단일 CPU를 100% 점유해 서버 전체를 마비시킨다.

```text
┌──────────────────────────────────────────────────────────────┐
│              ReDoS 취약 패턴과 악성 입력                      │
├──────────────────────────────────────────────────────────────┤
│  취약 패턴: ^(a+)+$                                           │
│  정상 입력: "aaa" → 빠른 매칭                                 │
│  악성 입력: "aaaaaaaaaaaaaaaaaaaX"                            │
│                                                              │
│  백트래킹 폭발:                                               │
│  - (a+)+ 에서 외부 + 가 내부 a+ 의 결과를 나눠 갖는 방법이   │
│    2^n 가지 존재 (n = 'a' 글자 수)                           │
│  - n=20: ~1,000,000번 백트래킹 → CPU 장시간 점유              │
│                                                              │
│  처리 시간: O(2^n) → n=30이면 ~1초, n=35이면 ~30초            │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: ReDoS는 미로(정규식 엔진)에서 탈출하지 못하고 계속 되돌아가다 지쳐 쓰러지게 만드는 공격이다. 나쁜 설계의 미로는 출구를 찾을수록 더 깊어진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 취약한 패턴 분류 (Evil Regex)

| 패턴 유형 | 예시 | 위험 이유 |
|:---|:---|:---|
| 중첩 수량자 | `(a+)+` | 외부·내부 수량자 조합 지수 증가 |
| 중복 교대 | `(a|a)+` | 동일 문자 교대 조합 |
| 교대 중첩 | `(a|aa)+` | 부분 일치 재조합 |
| 충분히 긴 패턴 | `([a-zA-Z]+)*` | 문자 클래스 중첩 |

```text
┌──────────────────────────────────────────────────────────────┐
│              안전한 정규식 설계 원칙                          │
├──────────────────────────────────────────────────────────────┤
│  원칙 1: 중첩 수량자 제거                                    │
│  취약: (a+)+$   →  안전: a+$                                 │
│                                                              │
│  원칙 2: 원자 그룹 (Atomic Group) 사용 (지원 엔진)           │
│  취약: (a+)+$   →  안전: (?>a+)+$  (백트래킹 없음)           │
│                                                              │
│  원칙 3: 소유형 수량자 (Possessive Quantifier) 사용           │
│  취약: a++$     →  안전: a++$  (일부 엔진 지원)              │
│                                                              │
│  원칙 4: 정규식 타임아웃 설정                                 │
│  Node.js: /pattern/u with timeout option (ES2022+)          │
│  Java: Pattern.compile with custom timeout                  │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 안전한 정규식은 일방통행 도로처럼 한 방향으로만 가고 돌아오지 않는 경로를 만드는 것이다.

---

## Ⅲ. 비교 및 연결

| 항목 | ReDoS | Billion Laughs (XXE DoS) | HTTP 플러드 |
|:---|:---|:---|:---|
| 공격 요청 수 | 1건 | 1건 | 수백만 건 |
| CPU 영향 | 100% 점유 | 메모리 고갈 | 네트워크/CPU |
| 탐지 난이도 | 높음 | 중간 | 낮음 |
| 방어 핵심 | 정규식 재작성 | 외부 엔티티 비활성화 | Rate Limiting |

ReDoS는 단일 요청으로 발생하므로 Rate Limiting만으로는 방어할 수 없다. 정규식 자체를 선형 시간 복잡도로 재작성하거나, RE2 엔진(Google, 선형 보장)으로 교체하는 것이 근본 해결책이다.

📢 **섹션 요약 비유**: ReDoS는 단 한 번의 질문으로 상대방을 무한 고민에 빠트리는 철학적 역설과 같다. 아무리 많은 번거로운 질문(HTTP 플러드)보다 한 번의 치명적 질문이 더 위험할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**자동화 탐지 도구**:
- **safe-regex**: Node.js용 ReDoS 취약 패턴 탐지 (`npm install safe-regex`)
- **rexploits**: Python용 ReDoS 분석
- **vuln-regex-detector**: OWASP ReDoS 취약점 검사 도구

```javascript
// Node.js에서 RE2 엔진 사용
const RE2 = require('re2');
const re = new RE2('^(a+)+$');  // 선형 시간 보장, ReDoS 안전
```

**정규식 코드 리뷰 체크포인트**:
1. 중첩 수량자 `(X+)+`, `(X*)*` 패턴 탐색
2. 동일 문자 클래스 교대 `(a|a)` 패턴
3. 사용자 입력을 처리하는 모든 정규식 목록 작성 후 safe-regex 스캔

📢 **섹션 요약 비유**: ReDoS 점검은 미로 게임 설계자가 "이 미로에 갇히면 빠져나올 수 있는가?"를 미리 테스트하는 것이다.

---

## Ⅴ. 기대효과 및 결론

ReDoS 방어를 통해 단일 HTTP 요청으로 인한 서비스 마비를 예방할 수 있다. 특히 사용자 입력을 처리하는 모든 정규식을 안전성 분석 도구로 자동 검사하는 것을 CI/CD 파이프라인에 포함시키면, 새로운 취약 정규식 도입을 사전에 차단할 수 있다.

RE2 엔진은 선형 시간(O(n)) 복잡도를 보장하므로, 보안이 중요한 환경에서는 RE2 또는 이에 기반한 엔진(Rust의 regex 크레이트 등)으로 전환하는 것이 근본 해결책이다.

📢 **섹션 요약 비유**: ReDoS 완전 방어는 미로를 직선 도로(RE2 선형 엔진)로 교체하는 것이다. 직선 도로는 아무리 길어도 끝이 있어 갇히지 않는다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| 백트래킹 | 취약 메커니즘 | 지수적 증가의 원인 |
| RE2 엔진 | 근본 해결책 | 선형 시간 보장 정규식 |
| safe-regex | 탐지 도구 | Node.js ReDoS 패턴 검사 |
| 원자 그룹 | 완화 기법 | 백트래킹 제거 구문 |
| Stack Overflow 사고 | 실제 사례 | 2016년 34분 다운 |

### 👶 어린이를 위한 3줄 비유 설명
- ReDoS는 컴퓨터에게 "이 수수께끼 풀어봐"라고 했는데 답이 없어서 컴퓨터가 계속 생각만 하다가 지쳐버리는 공격이에요.
- 수수께끼를 풀수록 경우의 수가 2배씩 늘어나서 절대 못 풀어요.
- 쉽게 풀 수 있는 수수께끼만 내거나(안전한 정규식), 시간 제한(타임아웃)을 두면 막을 수 있어요!
"""),

"466_open_redirect.md": (466, "466. Open Redirect (오픈 리다이렉트)", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 오픈 리다이렉트 (Open Redirect)는 웹 애플리케이션이 사용자 제공 URL로 검증 없이 리다이렉트할 때, 공격자가 신뢰받은 도메인을 경유해 피해자를 악성 사이트로 유도하는 취약점이다.
> 2. **가치**: 오픈 리다이렉트는 단독으로는 낮은 위험으로 분류되지만, 피싱·OAuth 토큰 탈취·SSRF 체인 공격의 중간 단계로 결합될 때 심각한 피해를 야기한다.
> 3. **판단 포인트**: 허용 목록(Allow List) 기반 리다이렉트 검증이 핵심이며, 외부 URL 리다이렉트는 설계 수준에서 배제하고 내부 경로만 허용해야 한다.

---

## Ⅰ. 개요 및 필요성

오픈 리다이렉트는 애플리케이션이 `?next=`, `?redirect=`, `?url=` 같은 파라미터를 검증 없이 리다이렉트 목적지로 사용할 때 발생한다. 피해자에게는 신뢰받는 도메인(예: `bank.com/redirect?url=attacker.com`)의 URL이 보이므로 의심 없이 클릭한다.

특히 OAuth 2.0 인증 흐름에서 `redirect_uri` 파라미터가 느슨하게 검증될 때 오픈 리다이렉트는 인증 코드·액세스 토큰 탈취로 이어질 수 있어 OAuth Redirect 취약점이라고도 불린다.

```text
┌──────────────────────────────────────────────────────────────┐
│               오픈 리다이렉트 공격 흐름                       │
├──────────────────────────────────────────────────────────────┤
│  1. 공격자가 링크 생성:                                       │
│     https://trusted.com/login?next=https://attacker.com/phish│
│                                                              │
│  2. 피해자: trusted.com 도메인이라 신뢰하고 클릭              │
│                                                              │
│  3. 서버: HTTP 302 Location: https://attacker.com/phish       │
│                                                              │
│  4. 피해자: attacker.com의 가짜 로그인 페이지로 이동          │
│     → 자격증명 탈취                                           │
│                                                              │
│  OAuth 변형:                                                  │
│  redirect_uri=https://trusted.com/..?url=https://attacker.com│
│  → 인가 코드가 attacker.com에 노출                            │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 오픈 리다이렉트는 회사 안내데스크가 방문자에게 "저쪽으로 가세요"라고 안내하는데, 가리킨 방향이 사실은 회사 밖의 위험한 장소인 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 리다이렉트 우회 기법

| 우회 기법 | 예시 | 설명 |
|:---|:---|:---|
| 도메인 앞 슬래시 | `//attacker.com` | 프로토콜 상대 URL |
| @를 이용한 우회 | `https://trusted.com@attacker.com` | @ 이전은 사용자 정보 |
| 서브도메인 위장 | `trusted.com.attacker.com` | 피해자 도메인처럼 보임 |
| 이중 인코딩 | `%2Fattacker.com` | URL 디코딩 전 검증 우회 |
| 자바스크립트 스킴 | `javascript:alert(1)` | XSS 결합 가능 |

```text
┌──────────────────────────────────────────────────────────────┐
│               안전한 리다이렉트 구현                          │
├──────────────────────────────────────────────────────────────┤
│  방어 1: 상대 경로만 허용                                    │
│  - 허용: /dashboard, /home                                   │
│  - 차단: http://, https://, //, javascript:                  │
│  if (!redirect.startsWith('/') || redirect.startsWith('//')) │
│      redirect = '/home';                                     │
│                                                              │
│  방어 2: 허용 목록 도메인만 허용                              │
│  ALLOWED = ['trusted.com', 'auth.trusted.com']               │
│  parsed = urlparse(redirect)                                 │
│  if parsed.netloc not in ALLOWED: redirect = '/'             │
│                                                              │
│  방어 3: 간접 리다이렉트 (토큰 기반)                          │
│  /redirect?token=abc123 → 서버에서 토큰으로 URL 조회          │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 안전한 리다이렉트는 택시 기사가 미리 정해진 목적지 목록(허용 목록)에서만 손님을 데려다주는 것이다. 목록에 없는 곳은 거절한다.

---

## Ⅲ. 비교 및 연결

| 공격 체인 | 오픈 리다이렉트 역할 | 피해 수준 |
|:---|:---|:---|
| 피싱 | 신뢰 도메인 위장 | 자격증명 탈취 |
| OAuth 토큰 탈취 | redirect_uri 오용 | 계정 탈취 |
| SSRF 우회 | URL 필터 우회 | 내부 서비스 접근 |
| 오픈 리다이렉트 단독 | 낮은 위험 | 사이트 신뢰도 손상 |

OAuth 2.0 RFC 6749는 `redirect_uri`를 사전 등록된 URI와 정확히 일치시키도록 요구한다. 느슨한 패턴 매칭(`trusted.com/*`)은 우회 가능하므로 정확한 문자열 비교가 필요하다.

📢 **섹션 요약 비유**: 오픈 리다이렉트가 혼자서는 작은 문제지만, OAuth 토큰이나 피싱과 결합하면 대형 금고의 마스터 키가 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**체크리스트**:
1. `next=`, `redirect=`, `url=`, `return_url=` 파라미터 검색
2. 302/301 응답에서 Location 헤더 값 외부 URL 여부 점검
3. OAuth `redirect_uri` 정확한 등록 URI와 일치 여부 검증
4. CSP `default-src` + `form-action` 지시어로 의도치 않은 전송 차단

📢 **섹션 요약 비유**: 오픈 리다이렉트 점검은 회사 안내데스크 매뉴얼을 검토하면서 "이 경우에 어디로 안내해야 하나?"를 모든 케이스에 대해 확인하는 것이다.

---

## Ⅴ. 기대효과 및 결론

오픈 리다이렉트를 제거하면 피싱 공격의 신뢰성 소재 제거, OAuth 인증 코드 탈취 방지, SSRF 체인 우회 차단의 효과를 얻는다. 작은 취약점처럼 보이지만 공격 체인의 핵심 링크로 작동하므로, 모든 리다이렉트 파라미터를 체계적으로 관리해야 한다.

📢 **섹션 요약 비유**: 오픈 리다이렉트 방어 완성은 회사 안내데스크에 미리 승인된 목적지 목록을 붙여두고, 그 외 장소로 안내하는 것을 엄격히 금지하는 규정을 만드는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| OAuth redirect_uri | 연관 취약점 | 토큰 탈취로 이어짐 |
| 피싱 | 공격 목적 | 신뢰 도메인 위장 |
| SSRF | 체인 공격 | URL 필터 우회 수단 |
| Allow List | 핵심 방어 | 허용 도메인·경로 목록 |
| RFC 6749 | 관련 표준 | OAuth redirect_uri 보안 |

### 👶 어린이를 위한 3줄 비유 설명
- 오픈 리다이렉트는 학교 안내판(신뢰받는 웹사이트)이 이상한 곳(사기 사이트)으로 방향을 가리키는 거예요.
- 학교 안내판이니까 아무 의심 없이 따라가다가 위험한 곳에 도착해요.
- 안내판에 허락된 장소 목록(허용 목록)을 붙여두고 그 외 장소는 안내하지 않으면 안전해요!
"""),

"467_host_header_injection.md": (467, "467. Host Header Injection (호스트 헤더 인젝션)", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Host Header Injection은 HTTP 요청의 `Host` 헤더를 조작해 웹 서버가 잘못된 호스트 정보를 신뢰하게 만들어 패스워드 재설정 링크 탈취, 캐시 포이즈닝, SSRF 등을 유발하는 취약점이다.
> 2. **가치**: 서버가 `Host` 헤더를 신뢰해 동적으로 URL을 생성하는 패턴(패스워드 재설정 이메일, 절대 URL 생성 등)에서 직접적인 피해로 이어진다.
> 3. **판단 포인트**: 서버에서 절대 URL을 생성할 때 `Host` 헤더 대신 설정 파일에서 도메인을 읽거나, 허용된 호스트 목록과 일치 여부를 검증해야 한다.

---

## Ⅰ. 개요 및 필요성

HTTP/1.1에서 `Host` 헤더는 가상 호스팅을 지원하기 위해 필수 헤더로 도입됐다. 서버가 여러 도메인을 호스팅할 때 `Host` 헤더로 어떤 사이트에 대한 요청인지 구분한다.

문제는 서버 애플리케이션이 `Host` 헤더 값을 신뢰하고 이메일의 링크, 절대 URL, 리다이렉트 목적지 등에 그대로 사용할 때 발생한다. 공격자가 `Host: attacker.com`으로 요청을 보내면, 서버가 패스워드 재설정 링크를 `attacker.com` 도메인으로 생성해 피해자에게 이메일로 보내는 상황이 만들어진다.

```text
┌──────────────────────────────────────────────────────────────┐
│           패스워드 재설정 링크 탈취 공격                      │
├──────────────────────────────────────────────────────────────┤
│  공격자 요청:                                                 │
│  POST /reset-password                                        │
│  Host: attacker.com                                          │
│  email: victim@example.com                                   │
│                                                              │
│  서버 동작 (취약):                                            │
│  reset_url = "http://" + request.host + "/reset?token=" + t  │
│  → "http://attacker.com/reset?token=ABCD1234"                │
│                                                              │
│  피해자에게 이메일 발송:                                      │
│  "패스워드 재설정: http://attacker.com/reset?token=ABCD1234" │
│                                                              │
│  피해자 클릭 → attacker.com에서 토큰 탈취 → 계정 탈취        │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: Host Header Injection은 편지를 받는 주소(Host 헤더)를 조작해서, 회신 편지(패스워드 재설정 이메일)가 내 집이 아닌 공격자 집으로 가게 만드는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Host Header Injection 공격 유형

| 공격 유형 | 조작 방법 | 영향 |
|:---|:---|:---|
| 패스워드 재설정 탈취 | Host: attacker.com | 리셋 토큰 탈취 |
| 웹 캐시 포이즈닝 | Host: evil.com | 캐시에 악성 응답 저장 |
| SSRF 우회 | Host: internal.server | 내부 서비스 접근 |
| 가상 호스트 우회 | Host: admin.internal | 관리 인터페이스 접근 |
| X-Forwarded-Host 인젝션 | X-Forwarded-Host: attacker.com | 프록시 경유 시 우회 |

```text
┌──────────────────────────────────────────────────────────────┐
│               방어 아키텍처                                   │
├──────────────────────────────────────────────────────────────┤
│  방어 1: 설정 파일에서 도메인 읽기                           │
│  BASE_URL = config.get('BASE_URL')  # "https://mysite.com"   │
│  reset_url = BASE_URL + "/reset?token=" + token              │
│  (Host 헤더 사용하지 않음)                                    │
│                                                              │
│  방어 2: Host 헤더 검증                                      │
│  ALLOWED_HOSTS = ['mysite.com', 'www.mysite.com']            │
│  if request.host not in ALLOWED_HOSTS:                       │
│      return 400 Bad Request                                  │
│                                                              │
│  방어 3: 웹 서버 레벨 차단 (Nginx)                           │
│  server {                                                    │
│    if ($host !~* ^(mysite\.com|www\.mysite\.com)$) {         │
│      return 400;                                             │
│    }                                                         │
│  }                                                           │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 방어는 회사에서 "회신 주소는 항상 우리 회사 주소를 사용하고, 고객이 알려준 주소를 사용하지 않는다"는 규정을 두는 것이다.

---

## Ⅲ. 비교 및 연결

| 항목 | Host Header Injection | Open Redirect | SSRF |
|:---|:---|:---|:---|
| 조작 대상 | Host 헤더 | URL 파라미터 | URL 파라미터 |
| 주요 피해 | 패스워드 탈취, 캐시 포이즈닝 | 피싱 | 내부 서비스 접근 |
| 방어 핵심 | 허용 호스트 목록 | 허용 URL 목록 | 허용 URL 목록 |

Django 프레임워크는 `ALLOWED_HOSTS` 설정으로 Host 헤더 검증을 내장 지원한다. Rails, Spring, Laravel도 유사한 호스트 검증 메커니즘을 제공한다.

📢 **섹션 요약 비유**: Host Header Injection은 열쇠를 복사하는 것과 달리, 열쇠 공장(서버)에 "이 주소로 열쇠를 보내줘"라고 거짓 주소를 알려주는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**Django 설정 예**:
```python
# settings.py
ALLOWED_HOSTS = ['mysite.com', 'www.mysite.com']
# Host 헤더가 목록에 없으면 400 에러
```

**Spring Boot 설정**:
```yaml
server:
  forward-headers-strategy: framework  # 프록시 헤더 검증
```

**테스트 방법**:
- Burp Suite에서 Host 헤더 변경 후 응답의 URL에 조작된 호스트 포함 여부 확인
- 패스워드 재설정 요청에 `Host: burpcollaborator.net` 삽입 후 이메일 수신 확인

📢 **섹션 요약 비유**: Host Header Injection 테스트는 "이 편지를 공격자 주소로 보내줘"라고 서버에 요청해보고, 서버가 정말 그 주소로 보내는지 확인하는 것이다.

---

## Ⅴ. 기대효과 및 결론

Host Header Injection 방어를 통해 패스워드 재설정 토큰 탈취, 웹 캐시 포이즈닝, 가상 호스트 우회 등 다양한 공격을 차단할 수 있다. 방어 구현이 단순(허용 호스트 목록)한 것에 비해 방치 시 피해가 크므로, 기본 보안 설정으로 항상 포함해야 한다.

📢 **섹션 요약 비유**: Host Header Injection 방어는 우체국에 "이 회사에서 보내는 편지는 항상 이 주소로만 보낼 수 있다"는 규정을 등록해두는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| 패스워드 재설정 | 주요 공격 대상 | 리셋 토큰 탈취 |
| 웹 캐시 포이즈닝 | 결합 공격 | 오염된 응답 캐시 저장 |
| X-Forwarded-Host | 우회 수단 | 프록시 경유 시 악용 |
| ALLOWED_HOSTS | 핵심 방어 | 허용 호스트 목록 |
| Django ALLOWED_HOSTS | 구현 예시 | 프레임워크 내장 방어 |

### 👶 어린이를 위한 3줄 비유 설명
- Host Header Injection은 편지에 "답장은 이 주소로 보내줘"라고 가짜 주소를 적는 거예요.
- 우체부(서버)가 그 주소를 믿으면 비밀 편지(패스워드 재설정 링크)가 나쁜 사람에게 가요.
- "답장 주소는 항상 회사 주소(설정 파일)"를 쓰도록 규정하면 막을 수 있어요!
"""),

"468_http_response_splitting.md": (468, "468. HTTP Response Splitting (HTTP 응답 분할)", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: HTTP Response Splitting (HTTP 응답 분할)은 HTTP 응답 헤더에 개행 문자(`\r\n`, `\n`)를 삽입해 응답을 임의로 분리하고, 완전히 새로운 HTTP 응답을 주입하는 헤더 인젝션 공격이다.
> 2. **가치**: 공격에 성공하면 XSS, 웹 캐시 포이즈닝, 쿠키 인젝션, 피싱 등 다양한 2차 공격이 가능하며, 특히 캐시 서버가 있는 환경에서 캐시 포이즈닝 피해가 크다.
> 3. **판단 포인트**: 헤더 값에 사용자 입력을 포함할 때 개행 문자(`CR`, `LF`)를 반드시 제거하거나 인코딩해야 하며, 현대 웹 프레임워크는 대부분 이를 자동 처리한다.

---

## Ⅰ. 개요 및 필요성

HTTP/1.1 헤더는 `\r\n`(CRLF, Carriage Return Line Feed)으로 구분된다. 서버가 사용자 입력을 헤더 값에 그대로 포함할 때, 공격자가 `\r\n` 문자를 입력에 삽입하면 헤더가 중간에 끊기고 새로운 헤더나 완전히 새로운 HTTP 응답이 시작된다.

이를 CRLF Injection 또는 HTTP Header Injection이라고도 부른다. 단순한 헤더 주입부터 전체 응답 분할까지 다양한 변형이 존재한다.

```text
┌──────────────────────────────────────────────────────────────┐
│              HTTP Response Splitting 공격                    │
├──────────────────────────────────────────────────────────────┤
│  취약한 코드:                                                 │
│  response.setHeader("Location", request.getParam("url"))     │
│                                                              │
│  악성 입력:                                                   │
│  url = "/safe\r\nContent-Length: 0\r\n\r\nHTTP/1.1 200 OK\r\n│
│  Content-Type: text/html\r\n\r\n<script>attack()</script>"   │
│                                                              │
│  생성된 응답:                                                 │
│  HTTP/1.1 302 Found                                          │
│  Location: /safe                                             │
│  Content-Length: 0                                           │
│                                                              │
│  HTTP/1.1 200 OK                  ← 두 번째 응답 주입!       │
│  Content-Type: text/html                                     │
│                                                              │
│  <script>attack()</script>                                   │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: HTTP Response Splitting은 편지 중간에 "편지 끝" 도장을 위조해서 다음 내용을 완전히 다른 편지로 만들어 끼워 넣는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 공격 시나리오와 방어

| 공격 변형 | 삽입 대상 | 피해 |
|:---|:---|:---|
| CRLF 인젝션 | 모든 응답 헤더 | 임의 헤더 추가 |
| 쿠키 인젝션 | Set-Cookie 헤더 | 세션 쿠키 조작 |
| 캐시 포이즈닝 | Location 헤더 | 악성 응답 캐시 |
| 응답 분할 XSS | 응답 본문 주입 | 스크립트 실행 |

```text
┌──────────────────────────────────────────────────────────────┐
│               방어 구현 (Python 예시)                         │
├──────────────────────────────────────────────────────────────┤
│  # 취약한 코드                                               │
│  redirect_url = request.args.get('url')                      │
│  response.headers['Location'] = redirect_url  # 위험!        │
│                                                              │
│  # 안전한 코드: CR, LF 문자 제거                             │
│  def sanitize_header(value):                                 │
│      return value.replace('\r', '').replace('\n', '')        │
│  safe_url = sanitize_header(redirect_url)                    │
│                                                              │
│  # 현대 프레임워크: 자동 처리                                │
│  # Flask, Django, Spring: 헤더에 CRLF 자동 거부              │
└──────────────────────────────────────────────────────────────┘
```

현대 웹 프레임워크(Flask, Django, Spring, Express.js)는 응답 헤더 설정 시 CRLF 문자를 자동으로 거부하거나 인코딩한다. 그러나 저수준 HTTP 라이브러리를 직접 사용하거나 레거시 시스템에서는 여전히 취약점이 존재할 수 있다.

📢 **섹션 요약 비유**: CRLF 제거는 편지에 "편지 끝" 도장 위조를 막기 위해 편지 내용에서 인장 문자를 모두 지우는 검열이다.

---

## Ⅲ. 비교 및 연결

| 항목 | HTTP Response Splitting | HTTP Request Smuggling |
|:---|:---|:---|
| 조작 대상 | 서버 응답 헤더 | 서버 요청 처리 |
| 공격 위치 | 응답 헤더 파라미터 | Content-Length vs Transfer-Encoding |
| 주요 피해 | 캐시 포이즈닝, XSS | 요청 처리 혼란, 보안 통제 우회 |
| 방어 핵심 | CRLF 필터링 | 헤더 일관성 검증 |

HTTP Request Smuggling은 유사하지만 다른 공격으로, 프론트엔드와 백엔드 서버 간의 HTTP 요청 경계 해석 차이를 이용한다.

📢 **섹션 요약 비유**: HTTP Response Splitting과 HTTP Request Smuggling은 같은 우체국(HTTP)에서 다른 방법으로 편지를 위조하는 두 가지 공격이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**취약한 패턴 탐지**:
1. `response.setHeader()`, `header()` 함수에 사용자 입력 직접 전달 여부 확인
2. URL 파라미터 값이 `Location`, `Set-Cookie` 헤더에 포함되는지 확인
3. `%0d%0a` (CRLF URL 인코딩)를 파라미터로 주입해 응답 헤더 확인

**보안 테스트**:
- 도구: Burp Suite Intruder에 CRLF 페이로드 삽입
- 페이로드: `%0d%0a%0d%0a<script>alert(1)</script>`

📢 **섹션 요약 비유**: HTTP Response Splitting 테스트는 편지봉투에 숨겨진 위조 도장을 찾기 위해 UV 램프로 조사하는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

HTTP Response Splitting 방어를 통해 웹 캐시 포이즈닝, XSS, 쿠키 인젝션 등 연쇄 공격을 차단할 수 있다. 현대 프레임워크는 자동으로 방어하지만, 레거시 코드와 저수준 HTTP 처리 코드에 대한 정기 감사가 필요하다.

최신 HTTP/2, HTTP/3 환경에서는 헤더 구분 방식이 변경되어 전통적인 CRLF 인젝션의 적용 범위가 줄었지만, HTTP/1.1을 지원하는 레거시 시스템과 프록시에서는 여전히 유효한 공격이다.

📢 **섹션 요약 비유**: HTTP Response Splitting 완전 방어는 편지 배달 시스템 자체를 현대화해서 도장 위조가 물리적으로 불가능한 디지털 서명 체계(HTTP/2 헤더)로 바꾸는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| CRLF Injection | 동의어 | HTTP Response Splitting의 다른 이름 |
| 웹 캐시 포이즈닝 | 결합 공격 | 오염된 응답이 캐시에 저장 |
| HTTP Request Smuggling | 유사 공격 | 요청 경계 해석 차이 악용 |
| Set-Cookie 인젝션 | 변형 공격 | 쿠키 값 조작 |
| HTTP/2 | 완화 요소 | CRLF 헤더 분리 미사용 |

### 👶 어린이를 위한 3줄 비유 설명
- HTTP Response Splitting은 편지 중간에 "여기서 끝"이라고 써서 그 뒤에 다른 편지를 끼워 넣는 거예요.
- 받는 사람(브라우저)은 두 번째 편지도 진짜 편지라고 생각해요.
- 편지에 "여기서 끝" 표시를 쓸 수 없도록 규칙을 만들면(CRLF 필터링) 막을 수 있어요!
"""),
}

for filename, (weight, title, content) in files.items():
    filepath = os.path.join(BASE, filename)
    if os.path.exists(filepath):
        print(f"SKIP (exists): {filename}")
        continue
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f'+++\nweight = {weight}\ntitle = "{title}"\ndate = "2026-04-21"\n[extra]\ncategories = "studynote-security"\n+++\n')
        f.write(content)
    print(f"CREATED: {filename}")

print("Done with batch 464-468")
