import os
OUT = "/Users/pf/workspace/brainscience/content/studynote/09_security/05_web_app_security/"

def w(fn, weight, title, content):
    path = os.path.join(OUT, fn)
    if os.path.exists(path):
        print(f"SKIP: {fn}")
        return
    with open(path, "w") as f:
        f.write(f'+++\nweight = {weight}\ntitle = "{title}"\ndate = "2026-04-21"\n[extra]\ncategories = "studynote-security"\n+++\n\n')
        f.write(content.strip() + "\n")
    print(f"CREATED: {fn}")

w("436_ldap_injection_web.md", 436, "436. LDAP Injection (웹 관점)", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: LDAP (Lightweight Directory Access Protocol) Injection은 사용자 입력이 LDAP 쿼리 필터에 직접 포함될 때 공격자가 LDAP 특수 문자를 삽입해 인증을 우회하거나 디렉토리 정보를 탈취하는 취약점이다.
> 2. **가치**: Active Directory (AD) 인증을 사용하는 기업 내부 시스템, SSO (Single Sign-On) 포털에서 LDAP 인젝션으로 관리자 권한을 우회할 수 있어 기업 보안의 핵심 취약점이다.
> 3. **판단 포인트**: LDAP 특수 문자(`*`, `(`, `)`, `\`, `NUL`) 이스케이프 처리와 화이트리스트 검증이 핵심 방어이며, 입력값을 LDAP DN (Distinguished Name) 이나 필터에 직접 연결하는 패턴 자체를 제거해야 한다.

---

## Ⅰ. 개요 및 필요성

LDAP는 기업 환경에서 사용자 인증, 그룹 관리, 디렉토리 서비스에 광범위하게 사용된다. 웹 애플리케이션이 LDAP 서버와 연동해 로그인을 처리할 때, 사용자 입력을 검증 없이 LDAP 필터에 포함하면 공격자가 필터 구조를 변경할 수 있다.

**취약 코드 예시 (Java)**:
```java
String ldapFilter = "(&(uid=" + username + ")(password=" + password + "))";
// 공격 입력 username: admin)(&(uid=admin)
// 실행 필터: (&(uid=admin)(&(uid=admin))(password=anything))
// → 비밀번호 없이 admin으로 로그인 가능
```

LDAP 주요 특수 문자:
- `*` : 와일드카드 — 모든 값 매칭
- `(`, `)` : 필터 그룹 경계
- `\` : 이스케이프 문자
- `NUL` (0x00) : 문자열 종료

📢 **섹션 요약 비유**: LDAP 인젝션은 회사 직원 명부를 조회할 때 "홍길동*"을 검색해 이름이 홍길동으로 시작하는 모든 직원을 가져오는 것처럼, 특수 문자로 검색 범위를 마음대로 조작하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

LDAP 인증 우회 공격 패턴:

| 공격 유형 | 입력 예시 | 효과 |
|:---|:---|:---|
| 비밀번호 우회 | `*)(uid=admin))(|(uid=*` | 비밀번호 조건 무력화 |
| 와일드카드 | `*` (비밀번호 필드) | 모든 비밀번호 매칭 |
| 정보 열거 | `a*` (uid 검색) | 'a'로 시작하는 모든 사용자 |
| Blind 탐색 | `)(uid=admin)(` | 조건 분리로 구조 파악 |

```
┌──────────────────────────────────────────────────────────┐
│           LDAP 인젝션 공격 흐름                          │
├──────────────────────────────────────────────────────────┤
│  원래 필터: (&(uid=user)(password=pass))                 │
│                                                          │
│  공격 입력 (uid): admin)(|(uid=*                         │
│  변조 필터: (&(uid=admin)(|(uid=*)(password=pass))       │
│                                                          │
│  결과: uid=admin OR 모든 uid 조건 → 인증 우회            │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: LDAP 필터에 괄호를 삽입하는 것은 수식에 괄호를 추가해 계산 순서를 바꾸는 것과 같다. `1+2*3`과 `(1+2)*3`의 결과가 다르듯, 필터 구조가 바뀌면 결과도 달라진다.

---

## Ⅲ. 비교 및 연결

| 구분 | SQL 인젝션 | LDAP 인젝션 |
|:---|:---|:---|
| 대상 | 관계형 DB | 디렉토리 서비스 (AD, OpenLDAP) |
| 특수 문자 | `'`, `;`, `--` | `*`, `(`, `)`, `\`, `NUL` |
| 주요 피해 | 데이터 탈취 | 인증 우회, 계정 열거 |
| 방어 | Prepared Statement | LDAP 특수 문자 이스케이프 |

📢 **섹션 요약 비유**: SQL과 LDAP는 다른 언어를 쓰지만 공격 원리는 같다. 사용자 입력이 쿼리/필터 구조를 변경할 수 있을 때 인젝션이 발생한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**LDAP 특수 문자 이스케이프 (RFC 4515)**:
| 문자 | 이스케이프 | 문자 | 이스케이프 |
|:---:|:---:|:---:|:---:|
| `*` | `\2a` | `(` | `\28` |
| `)` | `\29` | `\` | `\5c` |
| NUL | `\00` | `/` | `\2f` |

**대응 전략**:
1. **입력 이스케이프**: LDAP 특수 문자를 RFC 4515 기준으로 이스케이프
2. **화이트리스트**: 사용자명은 `[a-zA-Z0-9._-]+` 패턴만 허용
3. **LDAP 라이브러리 API**: 직접 필터 문자열 구성 대신 라이브러리의 파라미터화 API 사용
4. **최소 권한**: LDAP 바인드 계정에 필요한 최소 읽기 권한만 부여

📢 **섹션 요약 비유**: 특수 문자를 이스케이프하는 것은 메뉴판에 있는 음식만 주문할 수 있도록 하는 것이다. 특수 주문(공격)은 메뉴에 없으므로 무시된다.

---

## Ⅴ. 기대효과 및 결론

LDAP 특수 문자 이스케이프와 화이트리스트 검증을 조합하면 LDAP 인젝션을 효과적으로 방어할 수 있다. 특히 Active Directory와 연동된 시스템에서 LDAP 인젝션 방어는 전사적 계정 탈취를 막는 핵심 통제다.

기술사 관점에서 LDAP 인젝션은 디렉토리 서비스 연동 아키텍처 설계 시 반드시 고려해야 할 보안 요소로, AAA (Authentication, Authorization, Accounting) 프레임워크의 첫 번째 요소인 인증의 무결성을 위협한다.

📢 **섹션 요약 비유**: LDAP 인젝션 방어는 회사 출입 명부를 조작하는 것을 막는 것이다. 명부가 조작되면 권한 없는 사람이 언제든 들어올 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Active Directory | 공격 대상 | 기업 디렉토리 서비스 |
| RFC 4515 | 이스케이프 기준 | LDAP 필터 문자열 표준 |
| SSO | 연관 취약점 | 인증 연동 경로 |
| SQL Injection | 유사 공격 | 동일 원리, 다른 인터프리터 |
| Whitelist Validation | 방어 방법 | 허용 문자 패턴 강제 |

### 👶 어린이를 위한 3줄 비유 설명
- LDAP 인젝션은 회사 직원 목록을 검색할 때 특수 기호로 "모든 사람 보여줘"라고 속이는 방법이야.
- 기업에서 로그인을 LDAP으로 하는 경우가 많아서, 이 공격으로 비밀번호 없이 관리자로 로그인할 수 있어.
- 특수 기호를 '안전한 코드'로 바꾸는 이스케이프 처리가 핵심 방어야!
""")

w("437_xpath_injection.md", 437, "437. XPath Injection", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: XPath Injection (XPath 인젝션)은 XML (eXtensible Markup Language) 데이터를 쿼리하는 XPath 표현식에 사용자 입력이 직접 포함될 때, 공격자가 쿼리 논리를 변경해 인증을 우회하거나 XML 문서의 전체 내용을 추출하는 취약점이다.
> 2. **가치**: XPath 인젝션은 SQL 인젝션과 유사하지만 XML 데이터를 대상으로 하며, 권한 분리나 데이터 필터링 없이 전체 XML 트리에 접근할 수 있다는 특성이 있다.
> 3. **판단 포인트**: 파라미터화된 XPath (XPath Variables/Parameterized XPath)를 지원하는 언어에서는 반드시 사용하고, 그렇지 않으면 입력 이스케이프와 화이트리스트 검증을 적용해야 한다.

---

## Ⅰ. 개요 및 필요성

XML 데이터 저장소와 XSLT (eXtensible Stylesheet Language Transformations) 처리, SOA (Service-Oriented Architecture) 환경에서 XPath를 사용한 데이터 검색이 광범위하게 이루어진다. 이때 XPath 쿼리에 사용자 입력을 직접 포함하면 인젝션 취약점이 생긴다.

**취약 코드 예시 (Java)**:
```java
String xpath = "//users/user[name/text()='" + username + "' AND "
             + "password/text()='" + password + "']";
// 공격 입력: username = admin' or '1'='1
// 결과 XPath: //users/user[name/text()='admin' or '1'='1' AND ...]
// → password 조건 무시, admin 계정 인증 우회
```

XPath에는 SQL의 `--` 같은 주석이 없지만, `or '1'='1'`로 조건을 무력화할 수 있다.

📢 **섹션 요약 비유**: XPath 인젝션은 XML 파일로 만든 전화번호부에서 특정 사람을 찾을 때, 검색 조건에 "아니면 모든 사람"을 덧붙여 전체 목록을 가져오는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

XPath 인젝션 공격 패턴과 효과:

| 공격 유형 | 입력 예시 | 효과 |
|:---|:---|:---|
| 인증 우회 | `admin' or '1'='1` | 비밀번호 조건 무력화 |
| Blind 탐색 | `'] and count(/) > 0 and ('a'='a` | XML 구조 탐색 |
| 데이터 추출 | `admin' or name()='root` | 루트 요소 접근 |

```
┌──────────────────────────────────────────────────────────┐
│           XPath 인젝션 공격 흐름                         │
├──────────────────────────────────────────────────────────┤
│  정상 XPath: //user[name='admin' and pw='secret']        │
│                                                          │
│  공격 입력 (name): admin' or '1'='1                      │
│  변조 XPath: //user[name='admin' or '1'='1' and pw='x'] │
│                                                          │
│  결과: name='admin' 조건 OR '1'='1'(항상 참) → 인증 우회 │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: XPath 인젝션도 SQL 인젝션과 동일하게 조건에 "또는 항상 참인 조건"을 덧붙여 필터를 무력화한다.

---

## Ⅲ. 비교 및 연결

| 구분 | SQL 인젝션 | XPath 인젝션 |
|:---|:---|:---|
| 대상 | 관계형 DB | XML 데이터 |
| 주석 | `--`, `#` | 없음 (다른 우회 기법 사용) |
| 전체 데이터 접근 | information_schema 활용 | 루트(`/`) 노드에서 전체 접근 |
| 권한 구분 | DB 권한 체계 | XPath는 권한 분리 없음 |

📢 **섹션 요약 비유**: XPath는 SQL처럼 권한 테이블이 없다. 한 번 접근하면 XML 문서 전체를 볼 수 있는 마스터키가 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**대응 전략**:
1. **파라미터화 XPath**: Java Saxon 라이브러리의 XPathVariable, .NET의 XPathExpression 파라미터 사용
2. **입력 이스케이프**: 아포스트로피(`'`), 따옴표(`"`), `<`, `>`, `&` 이스케이프
3. **화이트리스트 검증**: 사용자 입력은 영숫자만 허용 (`[a-zA-Z0-9]+`)
4. **XML 스키마 검증**: XSD (XML Schema Definition)로 입력 XML 구조 검증
5. **최소 노출**: XML 파일에 민감 데이터(비밀번호 해시) 저장 자체를 최소화

📢 **섹션 요약 비유**: 파라미터화 XPath는 SQL의 Prepared Statement와 같다. 데이터와 쿼리 구조를 분리해 구조 변경을 원천 차단한다.

---

## Ⅴ. 기대효과 및 결론

파라미터화 XPath와 입력 화이트리스트를 적용하면 XPath 인젝션을 방어할 수 있다. XML 기반 설정 파일이나 데이터 저장소를 사용하는 레거시 시스템에서 특히 주의가 필요하며, 현대 시스템에서는 JSON 기반 REST API와 적절한 DB 사용으로 XPath 노출 자체를 줄이는 것이 최선이다.

📢 **섹션 요약 비유**: XPath 인젝션을 막는 것은 SQL 인젝션과 같은 원리다. 사용자가 제공한 문자열이 쿼리 구조의 일부가 되지 않도록 해야 한다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| XPath | 쿼리 언어 | XML 데이터 탐색 언어 |
| XML | 데이터 형식 | XPath의 대상 |
| SQL Injection | 유사 공격 | 동일 원리, 다른 인터프리터 |
| XPathVariable | 방어 방법 | 파라미터화 XPath |
| XSD | 검증 도구 | XML 스키마 검증 |

### 👶 어린이를 위한 3줄 비유 설명
- XPath 인젝션은 XML이라는 파일에서 정보를 찾을 때, "이 사람 찾아줘"라는 요청에 "아니면 모든 사람 보여줘"를 몰래 추가하는 방법이야.
- SQL 인젝션이랑 원리가 똑같아. 검색 조건을 속이는 거야.
- 그래서 검색어를 코드와 분리하는 파라미터화 방법을 항상 써야 해!
""")

w("438_el_injection.md", 438, "438. Expression Language Injection", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: EL (Expression Language) Injection (표현식 언어 인젝션)은 Java EE (Enterprise Edition) 의 JSP (JavaServer Pages) EL, Spring SpEL (Spring Expression Language), JSF (JavaServer Faces) EL 등 표현식 언어 엔진에 사용자 입력이 직접 평가될 때 임의 코드를 실행하는 취약점이다.
> 2. **가치**: EL 인젝션은 단순 데이터 조작을 넘어 서버 측 Java 코드를 직접 실행할 수 있어 원격 코드 실행(RCE, Remote Code Execution)으로 이어질 수 있다.
> 3. **판단 포인트**: 사용자 입력을 EL 표현식 컨텍스트에 직접 포함하지 않고, 입력값을 EL 처리 전에 이스케이프하거나, SpEL의 경우 SimpleEvaluationContext를 사용해 평가 컨텍스트를 제한해야 한다.

---

## Ⅰ. 개요 및 필요성

Java 웹 프레임워크(Spring, JSF, Thymeleaf 등)는 표현식 언어를 통해 서버 사이드 데이터를 HTML 템플릿에 동적으로 바인딩한다. 그러나 사용자 입력이 표현식으로 평가되는 맥락에 포함되면, 공격자가 임의 Java 코드를 서버에서 실행할 수 있다.

**Spring SpEL 인젝션 예시**:
```java
// 취약한 코드: 사용자 입력을 SpEL 표현식으로 평가
ExpressionParser parser = new SpelExpressionParser();
Expression expr = parser.parseExpression(userInput);
Object result = expr.getValue();

// 공격 입력: T(java.lang.Runtime).getRuntime().exec("id")
// → 서버에서 OS 명령 실행!
```

JSP EL의 경우 `${userInput}` 형태로 출력할 때, 입력이 다시 EL로 평가되는 이중 평가(Double Evaluation) 취약점이 대표적이다.

📢 **섹션 요약 비유**: EL 인젝션은 "계산기에 '2+3'을 입력하면 5가 나오듯, 공격자가 '서버에서 이 명령을 실행해'라는 표현식을 입력하면 그대로 실행되는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

EL 인젝션 공격 경로:

| 프레임워크 | 취약 패턴 | 공격 예시 |
|:---|:---|:---|
| Spring SpEL | `parser.parseExpression(input)` | `T(java.lang.Runtime).getRuntime().exec("id")` |
| JSP EL | `${param.input}` 이중 평가 | `${applicationScope}` (설정 탈취) |
| Spring Boot | `@Value("${input}")` (동적) | `#{T(java.lang.System).exit(0)}` |

```
┌──────────────────────────────────────────────────────────┐
│           SpEL 인젝션 → RCE 공격 흐름                    │
├──────────────────────────────────────────────────────────┤
│  공격자 입력: T(java.lang.Runtime).getRuntime()           │
│                .exec(new String[]{"sh","-c","id"})        │
│       │                                                   │
│       ▼                                                   │
│  SpEL 파서가 Java 코드로 평가                             │
│       │                                                   │
│       ▼                                                   │
│  서버에서 "id" 명령 실행 → uid=www-data 등 반환          │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: SpEL 인젝션은 수식 계산기에 `execute(os_command)`라는 함수를 입력해 서버 명령을 실행하는 것이다.

---

## Ⅲ. 비교 및 연결

| 구분 | EL Injection | SSTI (Server-Side Template Injection) |
|:---|:---|:---|
| 대상 | Java EL 엔진 | Jinja2, Freemarker, Thymeleaf 등 |
| 위험도 | RCE 가능 | RCE 가능 |
| 발생 환경 | Java 웹 프레임워크 | Python/Java/Ruby 템플릿 |
| 방어 | SimpleEvaluationContext | 템플릿 샌드박스, 이스케이프 |

📢 **섹션 요약 비유**: EL Injection과 SSTI는 같은 공격의 다른 방언이다. 둘 다 "표현식 엔진이 사용자 입력을 코드로 실행한다"는 공통점이 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**Spring SpEL 안전 사용**:
1. **SimpleEvaluationContext 사용**: `StandardEvaluationContext` 대신 제한된 컨텍스트 사용
2. **사용자 입력을 SpEL 표현식으로 사용 금지**: 고정 표현식 + 파라미터 바인딩으로 대체
3. **JSP EL 이중 평가 방지**: `JSTL c:out`으로 출력, `isELIgnored` 설정 검토
4. **Spring MVC 설정**: 사용자 입력이 뷰 이름으로 사용되지 않도록 엄격한 뷰 이름 검증

📢 **섹션 요약 비유**: SimpleEvaluationContext는 계산기에서 수학 연산만 허용하고, OS 명령 실행 함수는 아예 없애버리는 것이다.

---

## Ⅴ. 기대효과 및 결론

EL 인젝션은 적절한 컨텍스트 제한과 사용자 입력을 표현식으로 처리하지 않는 아키텍처 원칙으로 방어할 수 있다. 특히 Spring 기반 애플리케이션에서 SpEL이 필요한 경우 SimpleEvaluationContext를 기본값으로 사용하는 팀 코딩 표준이 중요하다.

기술사 관점에서 EL 인젝션은 "표현식 언어 엔진의 강력함이 취약점이 된다"는 교훈을 담고 있다. 강력한 기능일수록 입력 처리에 더욱 엄격한 원칙이 필요하다.

📢 **섹션 요약 비유**: 강력한 계산기를 사용자에게 직접 쥐어주는 것은 위험하다. 버튼을 제한해 수식만 입력할 수 있게 하는 것이 안전한 설계다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SpEL | 공격 대상 | Spring 표현식 언어 |
| SimpleEvaluationContext | 방어 방법 | 제한된 SpEL 평가 컨텍스트 |
| SSTI | 유사 공격 | 서버 측 템플릿 인젝션 |
| RCE | 최종 피해 | 원격 코드 실행 |
| Double Evaluation | 취약 패턴 | 이중 EL 평가 |

### 👶 어린이를 위한 3줄 비유 설명
- EL 인젝션은 수식 계산기에 "2+3" 대신 "이 명령어를 실행해"라고 입력해 컴퓨터가 그대로 따르는 공격이야.
- Java 웹 프로그램에서 특히 많이 쓰이는 표현식 언어(SpEL)가 공격 대상이 돼.
- 그래서 사용자가 넣은 값은 절대 표현식으로 평가하면 안 되고, 제한된 기능만 쓸 수 있게 해야 해!
""")

w("439_ssti.md", 439, "439. Template Injection (SSTI)", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SSTI (Server-Side Template Injection)는 사용자 입력이 서버 측 템플릿 엔진(Jinja2, Freemarker, Twig, Pebble 등)에 의해 직접 평가될 때, 템플릿 구문을 이용해 임의 코드를 실행하는 취약점이다.
> 2. **가치**: `{{7*7}}`이 출력에서 `49`로 나타나면 SSTI가 존재한다는 신호이며, 이는 SSRF (Server-Side Request Forgery), RCE (Remote Code Execution), 파일 시스템 접근으로 확장될 수 있다.
> 3. **판단 포인트**: 사용자 입력을 템플릿 문자열로 렌더링하지 않고 데이터로만 전달하는 것이 근본 해결책이며, 템플릿 엔진의 샌드박스 모드 활성화가 보조 방어다.

---

## Ⅰ. 개요 및 필요성

웹 프레임워크는 HTML 템플릿에 서버 사이드 데이터를 바인딩하기 위해 템플릿 엔진을 사용한다. 그런데 사용자 입력 자체가 템플릿으로 렌더링되면, 공격자가 템플릿 구문(`{{...}}`, `${...}`, `#{}` 등)을 삽입해 서버에서 코드를 실행할 수 있다.

**Python Jinja2 SSTI 예시**:
```python
# 취약한 코드: 사용자 입력을 직접 렌더링
from flask import Flask, render_template_string, request
app = Flask(__name__)

@app.route("/")
def index():
    name = request.args.get("name", "")
    return render_template_string(f"<h1>Hello {name}</h1>")

# 공격 입력: {{7*7}} → Hello 49 (SSTI 확인)
# 고급 공격: {{config.items()}} → 설정 정보 유출
# RCE: {{''.__class__.mro()[1].__subclasses__()[...].popen("id").read()}}
```

SSTI 탐지 페이로드(엔진 식별용):
- `{{7*7}}` → 49 : Jinja2, Twig
- `${7*7}` → 49 : Freemarker, Thymeleaf
- `#{7*7}` → 49 : Ruby ERB
- `<%= 7*7 %>` → 49 : Ruby ERB

📢 **섹션 요약 비유**: SSTI는 마치 Word에서 {사용자이름}을 치환하는 기능을 악용해, "{사용자이름}이 아닌 {os.execute('명령')}"을 삽입하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SSTI 공격 단계와 페이로드:

| 단계 | 목표 | Jinja2 페이로드 예시 |
|:---|:---|:---|
| 1. 탐지 | SSTI 존재 여부 확인 | `{{7*7}}` → 49 |
| 2. 엔진 식별 | 템플릿 엔진 파악 | `{{7*'7'}}` → 7777777 (Jinja2 특성) |
| 3. 정보 수집 | 객체·설정 탐색 | `{{config.items()}}` |
| 4. RCE | 코드 실행 | `{{''.__class__...popen("id")}}` |

```
┌──────────────────────────────────────────────────────────┐
│           SSTI 탐지에서 RCE까지                          │
├──────────────────────────────────────────────────────────┤
│  입력: {{7*7}}                                           │
│  출력: 49 → SSTI 확인!                                  │
│                                                          │
│  입력: {{config.SECRET_KEY}}                             │
│  출력: 'my-secret-key' → 설정 정보 유출                 │
│                                                          │
│  입력: {{....__subclasses__()...popen("id")}}            │
│  출력: uid=1000 → RCE 성공!                             │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: SSTI 탐지는 "계산기에 2+2를 넣어서 4가 나오면 작동한다"고 확인하는 것이다. 그 다음 훨씬 위험한 계산(명령 실행)을 넣는다.

---

## Ⅲ. 비교 및 연결

| 구분 | SSTI | EL Injection |
|:---|:---|:---|
| 대상 | 템플릿 엔진 (Jinja2, Freemarker) | Java EL (SpEL, JSP EL) |
| 언어 | Python, Java, Ruby, PHP | Java |
| 구문 | `{{...}}`, `${...}` | `${...}`, `#{...}` |
| 최종 피해 | RCE, 정보 유출 | RCE |

📢 **섹션 요약 비유**: SSTI와 EL Injection은 같은 원리의 공격이다. "엔진이 입력을 코드로 실행한다"는 점이 공통점이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**핵심 방어 전략**:
1. **사용자 입력을 템플릿 문자열로 사용 금지**: `render_template_string(input)` 패턴 완전 제거
2. **데이터 바인딩만 허용**: `render_template("template.html", name=user_input)` 방식
3. **Jinja2 샌드박스**: `SandboxedEnvironment` 사용 — 위험한 객체 접근 차단
4. **SAST 탐지**: `render_template_string`, `Template(input)` 패턴 탐지 룰 설정
5. **최소 권한**: 웹 서버 프로세스 권한 최소화

```python
# 취약한 패턴
return render_template_string(f"Hello {name}")  # 금지

# 안전한 패턴
return render_template("hello.html", name=name)  # 권장
```

📢 **섹션 요약 비유**: 안전한 템플릿 사용은 사용자에게 빈칸을 채우는 권한만 주고, 편집 권한은 주지 않는 것이다.

---

## Ⅴ. 기대효과 및 결론

사용자 입력을 데이터 컨텍스트에서만 처리하고 절대 템플릿 문자열로 사용하지 않는 원칙을 팀 전체가 준수하면 SSTI를 완전히 방어할 수 있다. SAST 도구로 위험 패턴을 빌드 시점에 탐지하면 실수를 사전에 차단할 수 있다.

기술사 관점에서 SSTI는 오픈소스 웹 프레임워크를 사용하는 현대 웹 개발에서 가장 과소평가된 고위험 취약점 중 하나다. 특히 Flask, Django, Spring Boot 개발자가 반드시 숙지해야 할 취약점이다.

📢 **섹션 요약 비유**: SSTI 방어는 요리사에게 레시피(템플릿)를 주되, 손님이 재료(입력)를 직접 레시피에 써넣지 못하게 하는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Jinja2 | 공격 대상 | Python 템플릿 엔진 |
| SandboxedEnvironment | 방어 도구 | Jinja2 안전 실행 환경 |
| render_template_string | 취약 패턴 | 입력을 직접 템플릿으로 렌더링 |
| EL Injection | 유사 공격 | Java 표현식 언어 인젝션 |
| RCE | 최종 피해 | 원격 코드 실행 |

### 👶 어린이를 위한 3줄 비유 설명
- SSTI는 "안녕, {이름}!"이라는 편지 양식에, 이름 자리에 "명령어"를 넣어 서버가 그 명령어를 실행하게 만드는 방법이야.
- {{7*7}}을 입력해서 "49"가 보이면 그 서버는 SSTI에 취약한 거야.
- 그래서 사용자 입력은 무조건 "채울 내용"으로만 쓰고, 절대 양식 자체를 수정하게 두면 안 돼!
""")

print("Batch 436-439 done.")
