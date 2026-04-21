import os

OUT = "/Users/pf/workspace/brainscience/content/studynote/09_security/05_web_app_security/"

def write_file(filename, weight, title, content):
    path = os.path.join(OUT, filename)
    if os.path.exists(path):
        print(f"SKIP: {filename}")
        return
    with open(path, "w") as f:
        f.write(f'+++\nweight = {weight}\ntitle = "{title}"\ndate = "2026-04-21"\n[extra]\ncategories = "studynote-security"\n+++\n\n')
        f.write(content.strip() + "\n")
    print(f"CREATED: {filename}")

write_file("420_directory_traversal.md", 420, "420. Directory Traversal — 경로 역추적", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Directory Traversal (경로 역추적, Path Traversal)은 `../` 시퀀스를 이용해 웹 애플리케이션의 루트 디렉터리 밖의 파일 시스템에 무단 접근하는 공격이다.
> 2. **가치**: 설정 파일(`/etc/passwd`, `web.xml`), 소스 코드, 자격 증명 파일을 직접 읽어낼 수 있어 정보 유출과 추가 공격의 발판이 된다.
> 3. **판단 포인트**: 사용자 입력을 파일 경로에 직접 포함할 때 반드시 정규화(Canonicalization) 후 허용 경로 내 포함 여부를 검증해야 하며, 절대 경로 참조 방식으로 전환하는 것이 근본 해결책이다.

---

## Ⅰ. 개요 및 필요성

Directory Traversal은 웹 서버가 사용자가 요청한 파일 이름을 그대로 파일 시스템 경로에 연결할 때 발생한다. 공격자는 `../../etc/passwd` 같은 입력을 통해 의도된 디렉터리를 벗어나 서버의 민감한 파일에 접근한다. Windows 환경에서는 `..\\..\\windows\\system32\\config\\SAM` 처럼 백슬래시를 사용하기도 한다.

이 공격이 지속적으로 위험한 이유는 구현이 단순하고 탐지가 어렵기 때문이다. WAF (Web Application Firewall)가 `../` 패턴을 막더라도, URL 인코딩(`%2e%2e%2f`), 이중 인코딩(`%252e%252e%252f`), 유니코드 인코딩(`%c0%ae%c0%ae`) 등 다양한 우회 기법이 존재한다.

취약 코드 예시 (Java):
```java
String filename = request.getParameter("file");
File f = new File("/var/app/files/" + filename);
```
공격 입력: `../../../etc/passwd`

📢 **섹션 요약 비유**: Directory Traversal은 건물 지하 창고에 가는 척 엘리베이터에 탔다가, 최상층 사장실까지 버튼을 눌러 들어가는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 인코딩 기법 | 예시 | 설명 |
|:---|:---|:---|
| 기본 traversal | `../../../etc/passwd` | 직접 경로 역추적 |
| URL 인코딩 | `%2e%2e%2f` | `.` = %2e, `/` = %2f |
| 이중 URL 인코딩 | `%252e%252e%252f` | 서버 측 디코딩 두 번 |
| 유니코드 | `..%c0%af` | 슬래시 유니코드 표현 |
| 경로 정규화 우회 | `/app/./../../etc` | `.` 삽입으로 필터 우회 |

```
┌──────────────────────────────────────────────────────────┐
│           Directory Traversal 공격 흐름                  │
├──────────────────────────────────────────────────────────┤
│  [공격자] GET /download?file=../../../etc/passwd         │
│       │                                                  │
│       ▼                                                  │
│  [웹 서버] 경로 결합: /var/app/files/../../../etc/passwd │
│       │                                                  │
│       ▼                                                  │
│  실제 접근: /etc/passwd → 시스템 사용자 목록 반환        │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: `../`은 "한 단계 위로"라는 의미다. 공격자는 이 단계를 무한히 올라가다 보면 결국 서버의 가장 중요한 파일들이 있는 곳에 닿는다.

---

## Ⅲ. 비교 및 연결

Directory Traversal은 LFI (Local File Inclusion)와 구분된다.

| 구분 | Directory Traversal | LFI (Local File Inclusion) |
|:---|:---|:---|
| 목적 | 파일 내용 읽기 | 파일 포함·실행 |
| 위험도 | 정보 유출 | 코드 실행 가능 |
| 발생 위치 | 파일 다운로드 기능 | include/require 구문 |
| 예시 | `/download?file=../etc/passwd` | `/?page=../shell.php` |

📢 **섹션 요약 비유**: Traversal은 남의 일기를 읽는 것이고, LFI는 그 일기를 프로그램으로 실행시키는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**대응 전략**:
1. **경로 정규화 검증**: `File.getCanonicalPath()`로 정규화 후 허용 기본 경로로 시작하는지 확인
2. **화이트리스트 파일명**: 허용된 파일명 목록만 허용, 경로 문자 자체를 입력에서 거부
3. **chroot jail**: 프로세스가 특정 디렉터리 외부에 접근 불가하도록 OS 수준 제한
4. **간접 참조(Indirect Reference)**: 파일 경로 대신 ID 값으로 매핑 후 서버에서 경로 결정
5. **최소 권한 원칙**: 웹 서버 프로세스 계정에 최소 파일 시스템 권한만 부여

📢 **섹션 요약 비유**: 가장 안전한 방법은 사용자가 파일 이름을 직접 지정하지 않고, "1번 파일 주세요"라는 번호만 받아 서버가 알아서 매핑하는 것이다.

---

## Ⅴ. 기대효과 및 결론

경로 정규화와 화이트리스트 검증을 결합하면 Directory Traversal 공격을 효과적으로 차단할 수 있다. 특히 Java의 `getCanonicalPath()`, Python의 `os.path.realpath()` 등 언어별 정규화 API를 활용하면 인코딩 우회 기법도 함께 방어된다.

기술사 관점에서 파일 접근 기능 설계 시 사용자 입력을 경로에 직접 연결하는 패턴 자체를 금지하는 아키텍처 원칙이 필요하다.

📢 **섹션 요약 비유**: 사용자에게 파일 경로를 직접 지정하게 하는 것은 손님에게 창고 열쇠를 주는 것이다. 대신 "A 상품 주세요" 형태로만 요청받고 창고 위치는 직원만 알게 해야 한다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| LFI | 확장 공격 | 파일 실행으로 발전 |
| RFI (Remote File Inclusion) | 원격 파일 버전 | 외부 URL 파일 포함 |
| Canonicalization | 핵심 대응 | 경로 정규화 |
| chroot | OS 방어 | 프로세스 디렉터리 격리 |
| OWASP A01 | 연관 취약점 | 접근 제어 실패 범주 |

### 👶 어린이를 위한 3줄 비유 설명
- Directory Traversal은 미로에서 "뒤로 뒤로 계속 가면" 출구가 아닌 다른 방에 들어갈 수 있는 것처럼, `../`를 반복해서 서버의 비밀 파일에 접근하는 방법이야.
- 착한 웹사이트는 사용자가 "특정 파일 이름"을 직접 입력하지 못하게 해야 해.
- 마치 도서관 사서가 손님이 요청한 책 번호를 받아 직접 가져오듯, 서버도 파일 경로를 직접 노출하지 않아야 안전해!
""")

write_file("423_access_control_bypass.md", 423, "423. 접근 제어 회피 CORS Misconfiguration", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CORS (Cross-Origin Resource Sharing) Misconfiguration은 웹 서버가 교차 출처 요청의 `Origin` 헤더를 무분별하게 신뢰해, 악의적인 외부 도메인이 인증된 사용자의 자격으로 민감한 API에 접근할 수 있게 하는 취약점이다.
> 2. **가치**: CORS 오설정은 사용자가 악성 사이트를 방문하는 것만으로도 자신의 인증 토큰·쿠키를 통한 API 호출이 공격자에게 가능하게 하므로, 데이터 유출·계정 탈취로 직결된다.
> 3. **판단 포인트**: `Access-Control-Allow-Origin: *`과 `withCredentials: true`의 조합은 브라우저가 차단하지만, Origin을 동적으로 반사하거나 `null` Origin을 허용하는 설정이 실제 공격 벡터가 된다.

---

## Ⅰ. 개요 및 필요성

브라우저의 SOP (Same-Origin Policy) 는 다른 출처(Origin)의 리소스 접근을 기본적으로 차단한다. CORS는 서버가 특정 출처를 명시적으로 허용해 이 제한을 완화하는 메커니즘이다. 하지만 CORS 설정이 잘못되면 원래 막아야 할 교차 출처 접근을 오히려 허용하게 된다.

가장 흔한 오설정 패턴:
1. **Origin 동적 반사**: 모든 요청의 Origin 헤더를 그대로 `Access-Control-Allow-Origin`에 반영
2. **null Origin 허용**: `Access-Control-Allow-Origin: null` — file:// 프로토콜이나 샌드박스 iframe에서 악용 가능
3. **와일드카드 + 자격증명**: `Allow-Origin: *` + `Allow-Credentials: true` — 브라우저 차단이지만 잘못 이해한 개발자가 우회 시도
4. **부분 매칭**: `attacker.victim.com` 형태의 서브도메인 허용

📢 **섹션 요약 비유**: CORS 오설정은 클럽 입구에서 "아무 손님이나 VIP라고 하면 들여보내는" 규칙과 같다. 원래 VIP만 들어가야 하는데 아무나 VIP 흉내를 낼 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CORS Misconfiguration 공격 흐름:

| 단계 | 설명 |
|:---|:---|
| 1 | 피해자가 `https://victim-bank.com`에 로그인 (세션 쿠키 보유) |
| 2 | 피해자가 공격자의 `https://evil.com` 방문 |
| 3 | evil.com 페이지가 victim-bank.com API 호출 (XHR/Fetch) |
| 4 | victim-bank.com이 evil.com Origin을 허용 (오설정) |
| 5 | 브라우저가 피해자 쿠키와 함께 요청 전송 |
| 6 | 계좌 정보·거래 내역 탈취 |

```
┌──────────────────────────────────────────────────────────────┐
│            CORS Misconfiguration 공격 흐름                   │
├──────────────────────────────────────────────────────────────┤
│  [evil.com]                                                  │
│     │ fetch("https://api.bank.com/balance", {credentials:    │
│     │        "include"})                                     │
│     ▼                                                        │
│  [api.bank.com] ← Origin: https://evil.com 확인             │
│     │  잘못된 설정: ACAO: https://evil.com + ACAC: true     │
│     ▼                                                        │
│  [브라우저] 피해자 쿠키 포함 응답 → evil.com에 전달           │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 은행 창구가 "내가 해당 계좌 주인이에요"라는 메모만 보여주면 잔액을 알려주는 것과 같다. 실제로 누가 메모를 쓰든 상관없이.

---

## Ⅲ. 비교 및 연결

CORS Misconfiguration과 CSRF (Cross-Site Request Forgery)의 차이를 명확히 해야 한다.

| 구분 | CORS Misconfiguration | CSRF |
|:---|:---|:---|
| 피해 방식 | 응답 데이터 읽기 가능 | 피해자 권한으로 액션 수행 |
| SameSite 쿠키로 방어 | 부분적 | 효과적 |
| 공격자 요구 | Origin 허용된 도메인 통제 | 피해자가 링크/페이지 방문 |
| 위험 | 데이터 읽기·탈취 | 의도치 않은 상태 변경 |

📢 **섹션 요약 비유**: CORS 오설정은 남의 은행 잔액을 몰래 볼 수 있는 것이고, CSRF는 남의 계좌에서 돈을 이체하게 만드는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**안전한 CORS 설정 원칙**:
1. **엄격한 화이트리스트**: 허용 Origin을 정적 목록으로 관리, 요청 Origin과 비교
2. **null Origin 비허용**: `ACAO: null` 사용 금지
3. **불필요한 ACAC 제거**: `Access-Control-Allow-Credentials: true` 최소화
4. **Vary: Origin 헤더**: 캐시가 Origin별로 다른 응답을 구분하도록 설정
5. **Preflight 검증**: OPTIONS 요청의 Method·Headers도 엄격히 검증
6. **SameSite 쿠키**: `SameSite=Strict` 또는 `SameSite=Lax`로 CSRF 동시 방어

```nginx
# 올바른 예시 (Nginx)
if ($http_origin ~* "^https://(trusted-app.com|api.trusted.com)$") {
    add_header 'Access-Control-Allow-Origin' "$http_origin";
}
```

�� **섹션 요약 비유**: 초대 손님 목록을 미리 작성해두고, 그 목록에 있는 이름만 입장시키는 것이 올바른 CORS 설정이다.

---

## Ⅴ. 기대효과 및 결론

엄격한 CORS 정책과 SameSite 쿠키를 조합하면 교차 출처 데이터 탈취와 CSRF를 동시에 방어할 수 있다. 특히 API Gateway 수준에서 통합 CORS 정책을 관리하면 개별 서비스별 오설정 위험을 줄일 수 있다.

기술사 관점에서 CORS 오설정은 A01 Broken Access Control의 한 형태다. 클라이언트 측 SOP 메커니즘에 의존하는 것이 아니라, 서버 측에서 명시적으로 신뢰 도메인을 정의하고 관리하는 아키텍처가 필요하다.

📢 **섹션 요약 비유**: CORS 보안은 문을 잠그는 것만큼 중요하다. "누구나 들어올 수 있지만 아무것도 가져갈 수 없다"는 착각이 가장 위험한 오설정이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SOP (Same-Origin Policy) | 기반 정책 | 기본 교차 출처 차단 |
| CSRF | 연관 공격 | 교차 출처 상태 변경 |
| SameSite 쿠키 | 보완 방어 | 쿠키 교차 사이트 전송 제한 |
| Preflight | CORS 메커니즘 | 본 요청 전 권한 확인 |
| Access-Control-Allow-Credentials | 핵심 설정 | 자격증명 포함 여부 |

### 👶 어린이를 위한 3줄 비유 설명
- CORS는 웹사이트가 "이 손님은 우리 친구야"라고 인정하는 규칙인데, 잘못 설정하면 나쁜 사람도 "친구예요"라고 속일 수 있어.
- 그러면 나쁜 웹사이트가 내 은행 계좌 정보를 몰래 볼 수 있게 돼.
- 그래서 초대받은 사이트 목록을 미리 정확하게 정해 놓는 게 중요해!
""")

write_file("424_cryptographic_failures.md", 424, "424. A02 암호화 실패", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Cryptographic Failures (암호화 실패, A02)는 민감 데이터를 전송·저장할 때 암호화가 없거나 취약한 알고리즘을 사용해 공격자가 데이터를 평문으로 획득할 수 있게 되는 취약점이다.
> 2. **가치**: 2021년 OWASP에서 "민감 데이터 노출" 에서 명칭이 변경되어 근본 원인(암호화 실패)을 강조하며 2위를 차지할 만큼 광범위하고 치명적이다.
> 3. **판단 포인트**: TLS (Transport Layer Security) 1.2+ 강제, AES (Advanced Encryption Standard) -256 저장 암호화, 비밀번호에 bcrypt·Argon2 사용, 하드코딩된 키 제거가 핵심 대응이다.

---

## Ⅰ. 개요 및 필요성

암호화 실패는 단순히 "암호화를 안 했다"는 것 이상을 포함한다. 암호화를 적용했더라도 취약한 알고리즘(MD5, SHA-1, DES, RC4), 짧은 키 길이, 안전하지 않은 키 관리, 불완전한 구현 등이 모두 암호화 실패에 해당한다.

민감 데이터 분류:
- **최고 민감**: 비밀번호, 암호화 키, API (Application Programming Interface) 키
- **고 민감**: 신용카드 번호, 주민등록번호, 의료 기록
- **중 민감**: 이름, 이메일, 주소, 전화번호
- **저 민감**: 공개 데이터

각 분류에 따라 저장·전송 암호화 요구 수준이 달라진다. GDPR (General Data Protection Regulation), PCI DSS (Payment Card Industry Data Security Standard), HIPAA (Health Insurance Portability and Accountability Act) 등 규정은 민감 데이터의 암호화를 법적으로 의무화한다.

📢 **섹션 요약 비유**: 아무리 금고(서버)가 튼튼해도, 금고 안의 문서가 읽기 쉬운 글씨로 쓰여 있으면 금고를 부수는 순간 전부 탈취된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

암호화 실패 유형과 현대적 대응:

| 취약 방식 | 문제점 | 현대적 대응 |
|:---|:---|:---|
| HTTP (평문) 전송 | 네트워크 스니핑 | TLS 1.3, HTTPS 전면 적용 |
| MD5/SHA-1 비밀번호 해시 | 레인보우 테이블 공격 | bcrypt, Argon2, scrypt |
| DES/3DES 암호화 | 키 길이 부족 | AES-256-GCM |
| ECB 운용 모드 | 패턴 노출 | CBC, GCM 사용 |
| 하드코딩 키 | 소스 코드 노출 | KMS (Key Management Service) 사용 |
| 취약한 난수 | 예측 가능 | CSPRNG (Cryptographically Secure PRNG) 사용 |

```
┌──────────────────────────────────────────────────────────┐
│           암호화 계층별 보안 요구사항                     │
├──────────────────────────────────────────────────────────┤
│  전송 계층: TLS 1.3 → 완전 순방향 비밀성(PFS) 보장      │
│  저장 계층: AES-256-GCM → 인증된 암호화 + 무결성         │
│  인증 계층: bcrypt(cost=12) → 느린 해시로 무차별 방어     │
│  키 관리: AWS KMS / HashiCorp Vault → 키 순환·감사      │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 전송 암호화는 우편물을 봉투에 넣는 것, 저장 암호화는 파일 캐비닛에 자물쇠를 거는 것, 비밀번호 해싱은 원본을 아예 알아볼 수 없게 분쇄하는 것이다.

---

## Ⅲ. 비교 및 연결

암호화와 해싱의 목적 차이를 명확히 구분해야 한다.

| 구분 | 암호화 (Encryption) | 해싱 (Hashing) |
|:---|:---|:---|
| 목적 | 복호화 가능한 기밀성 | 단방향 무결성 검증 |
| 비밀번호 저장 | 부적합 (키 탈취 시 전체 노출) | 적합 (bcrypt, Argon2) |
| 데이터 전송 | 적합 (TLS) | 부적합 |
| 키 필요 | 예 | 아니오 (솔트(Salt) 사용) |

📢 **섹션 요약 비유**: 암호화는 자물쇠 채우기(열 수 있음), 해싱은 분쇄기에 넣기(복원 불가)다. 비밀번호는 분쇄기가 맞다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**TLS 설정 체크리스트**:
- TLS 1.2 이상 강제, TLS 1.0/1.1 비활성화
- HSTS (HTTP Strict Transport Security) 헤더 설정 (`max-age=31536000; includeSubDomains`)
- 강력한 암호화 스위트(Cipher Suite) 우선: ECDHE-RSA-AES256-GCM-SHA384
- 인증서 유효성 및 만료 일정 모니터링

**비밀번호 저장 설정**:
- bcrypt: `cost=12` (서버 성능에 따라 10~14 조정)
- Argon2id: `memory=65536, iterations=3, parallelism=4` (NIST SP 800-63B 권장)
- 솔트(Salt): 각 비밀번호별 128비트 무작위 솔트 적용

📢 **섹션 요약 비유**: 보안 설정을 기본값으로 두면 대부분 취약하다. 직접 TLS 버전, 암호화 알고리즘, 해시 비용을 명시적으로 설정하는 것이 전문가의 책임이다.

---

## Ⅴ. 기대효과 및 결론

전송·저장·인증 세 계층에 걸쳐 현대적 암호화를 적용하면 A02 취약점을 구조적으로 해결할 수 있다. 특히 키 관리를 KMS (Key Management Service)로 중앙화하면 하드코딩 키 문제와 키 순환 이슈를 동시에 해결한다.

기술사 관점에서 암호화 실패는 **데이터 생명주기(Data Lifecycle) 보안** 관점에서 접근해야 한다. 데이터 생성부터 폐기까지 각 단계에서 필요한 암호화 수준을 정의하고, SDL (Secure Development Lifecycle)에 통합하는 것이 중요하다.

📢 **섹션 요약 비유**: 암호화는 자동차 안전벨트처럼, 사고가 나기 전에 항상 채워야 효과가 있다. 사고 난 후에 벨트를 매는 것은 의미가 없다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| TLS 1.3 | 전송 암호화 | 최신 전송 계층 보안 |
| AES-256-GCM | 저장 암호화 | 인증된 대칭 암호화 |
| bcrypt/Argon2 | 비밀번호 해싱 | 의도적 느린 해시 |
| KMS | 키 관리 | 중앙화된 키 생명주기 관리 |
| PFS (Perfect Forward Secrecy) | TLS 속성 | 세션 키 노출 최소화 |

### 👶 어린이를 위한 3줄 비유 설명
- 암호화 실패는 비밀 편지를 봉투도 없이 그냥 우체통에 넣는 것과 같아. 누구나 읽을 수 있어.
- 비밀번호를 MD5로 저장하는 건 비밀을 그냥 메모지에 적어서 누구나 볼 수 있는 곳에 두는 것과 같아.
- 안전한 암호화는 편지를 자물쇠 달린 상자에 넣고, 열쇠도 따로 안전하게 보관하는 거야!
""")

write_file("425_hardcoded_credentials.md", 425, "425. 하드코딩 자격증명", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 하드코딩된 자격증명 (Hardcoded Credentials)은 비밀번호, API (Application Programming Interface) 키, 토큰, DB (Database) 연결 문자열 등을 소스 코드에 직접 기록해 버전 관리 시스템(VCS, Version Control System)이나 바이너리를 통해 누구에게나 노출되는 취약점이다.
> 2. **가치**: GitHub에서 분당 수십 개의 민감 정보가 노출된다는 연구 결과가 있으며, 한 번 공개된 키는 즉시 자동화 도구로 수집되어 악용된다.
> 3. **판단 포인트**: 환경 변수(Environment Variable), 비밀 관리 서비스(Secrets Manager), Vault를 통한 런타임 주입이 표준 대응이며, 커밋 전 자동 스캔(pre-commit hook)으로 사전 차단해야 한다.

---

## Ⅰ. 개요 및 필요성

개발 편의성을 위해 코드에 자격증명을 직접 작성하는 습관은 심각한 보안 위협이다. 특히 오픈소스 프로젝트에서 민감 정보가 포함된 커밋이 GitHub에 푸시되면, 즉시 봇이 이를 스캔해 AWS (Amazon Web Services) 자격증명, Stripe API 키, Slack 웹훅 등을 수집한다.

더 위험한 것은 **히스토리 문제**다. 코드에서 자격증명을 삭제해 새 커밋을 만들어도, git 히스토리에 이전 커밋이 남아 있어 `git log -p`로 언제든 복원 가능하다. 완전한 제거를 위해서는 `git filter-branch`나 `BFG Repo-Cleaner`로 히스토리를 재작성해야 한다.

흔한 하드코딩 패턴:
```python
DB_PASSWORD = "admin1234"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
STRIPE_SECRET = "sk_live_AbCdEfGhIjKlMnOp"
```

📢 **섹션 요약 비유**: 하드코딩 자격증명은 집 열쇠를 현관문에 붙여놓는 것과 같다. 깔끔하고 편리하지만, 지나가는 모든 사람이 볼 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

하드코딩 자격증명의 위험 경로:

| 노출 경로 | 위험도 | 설명 |
|:---|:---|:---|
| 공개 GitHub 저장소 | 최상 | 즉시 자동화 스캔 대상 |
| 컨테이너 이미지 | 상 | `docker inspect`, layer 분석으로 추출 |
| APK/IPA 바이너리 | 중상 | 역공학(Reverse Engineering) 도구로 추출 |
| 로그 파일 | 중 | 스택 트레이스에 연결 문자열 포함 |
| 환경 변수 미관리 | 중 | `.env` 파일이 git에 포함되는 경우 |

```
┌──────────────────────────────────────────────────────────┐
│         하드코딩 자격증명 탐지 및 관리 흐름              │
├──────────────────────────────────────────────────────────┤
│  개발자 코드 작성                                        │
│       │                                                  │
│       ▼                                                  │
│  pre-commit hook (GitLeaks, TruffleHog) — 사전 차단      │
│       │ 탐지 시 커밋 차단                                │
│       ▼                                                  │
│  CI/CD 파이프라인 비밀 스캔 (2차 방어)                   │
│       │                                                  │
│       ▼                                                  │
│  런타임: Vault/Secrets Manager에서 동적 주입             │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: pre-commit 훅은 편지를 보내기 전에 "비밀 내용이 들어있나요?" 하고 자동 검사하는 비서다.

---

## Ⅲ. 비교 및 연결

자격증명 관리의 성숙도 모델:

| 단계 | 방식 | 보안 수준 |
|:---|:---|:---|
| 0단계 | 소스 코드 하드코딩 | 최악 |
| 1단계 | `.env` 파일 (git 제외) | 낮음 |
| 2단계 | 환경 변수 주입 | 보통 |
| 3단계 | AWS Secrets Manager, Vault | 높음 |
| 4단계 | 단기 자격증명 + 자동 순환 | 최상 |

📢 **섹션 요약 비유**: 자격증명 관리는 자물쇠 수준을 높여가는 과정이다. 하드코딩은 잠금 없음, Vault는 지문+비밀번호+시간 제한 금고다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**대응 전략**:
1. **pre-commit 훅**: GitLeaks, detect-secrets를 모든 개발자 환경에 설치 의무화
2. **GitHub Advanced Security**: 저장소 수준에서 Secret Scanning 활성화
3. **비밀 관리 서비스**: AWS Secrets Manager, HashiCorp Vault, Azure Key Vault 도입
4. **단기 자격증명**: AWS IAM (Identity and Access Management) Roles for EC2, IRSA (IAM Roles for Service Accounts) 사용으로 장기 자격증명 배제
5. **유출 대응 프로세스**: 유출 확인 즉시 해당 자격증명 폐기(Revoke) 및 재발급

📢 **섹션 요약 비유**: 좋은 비밀 관리는 호텔처럼 운영하는 것이다. 체크인 시 임시 카드키를 발급하고, 체크아웃 시 자동 무효화. 마스터키를 직원이 주머니에 넣고 다니지 않는다.

---

## Ⅴ. 기대효과 및 결론

비밀 관리 서비스 + pre-commit 훅 + Secret Scanning 조합은 하드코딩 자격증명 위험을 구조적으로 제거한다. 특히 IRSA나 Workload Identity 같은 단기 자격증명 메커니즘은 긴 수명의 자격증명 자체를 없애 노출 위험을 최소화한다.

기술사 관점에서 자격증명 관리는 **Identity & Access Management (IAM) 거버넌스**의 핵심이다. 개발-운영 환경 분리, 자격증명 수명주기 관리, 감사 로그 통합이 종합 솔루션이다.

📢 **섹션 요약 비유**: 비밀번호를 포스트잇에 적어 모니터에 붙이는 직원과 매월 자동 교체되는 임시 카드키를 쓰는 직원 중 어느 쪽이 더 안전한지는 자명하다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| GitLeaks | 탐지 도구 | 소스 코드 자격증명 스캔 |
| HashiCorp Vault | 비밀 관리 | 중앙화된 비밀 저장·배포 |
| IRSA | 단기 자격증명 | K8s SA와 IAM Role 연결 |
| Secret Scanning | CI/CD 통합 | 자동 비밀 탐지 |
| Rotation | 키 관리 | 주기적 자격증명 갱신 |

### 👶 어린이를 위한 3줄 비유 설명
- 코드에 비밀번호를 넣는 건 일기에 집 비밀번호를 쓰고 공개 게시판에 붙이는 것과 같아.
- 해커들은 자동 프로그램으로 GitHub에서 매일 비밀번호와 API 키를 훔쳐가고 있어.
- 그래서 비밀번호는 코드 밖에서 관리하고, 사용할 때만 잠깐 빌려오는 방식이 가장 안전해!
""")

write_file("426_weak_tls_version.md", 426, "426. 약한 TLS 버전", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 약한 TLS (Transport Layer Security) 버전이나 암호화 스위트(Cipher Suite) 사용은 POODLE, BEAST, DROWN 같은 프로토콜 수준 공격에 취약하게 하고, 공격자가 전송 데이터를 복호화하거나 변조할 수 있게 한다.
> 2. **가치**: TLS 1.0/1.1은 2021년 RFC 8996으로 공식 폐기되었고, PCI DSS 3.2+는 TLS 1.2 이상 의무화, TLS 1.3은 현재 표준으로 모든 신규 서비스에 적용되어야 한다.
> 3. **판단 포인트**: TLS 버전뿐 아니라 암호화 스위트(RC4, NULL 암호화, 수출용 암호화), 인증서 강도(키 길이), HSTS (HTTP Strict Transport Security) 적용 여부를 종합 점검해야 한다.

---

## Ⅰ. 개요 및 필요성

TLS는 인터넷 통신의 기밀성·무결성·인증을 제공하는 핵심 프로토콜이다. 하지만 오래된 버전과 취약한 암호화 스위트는 20년간 발견된 수많은 공격에 노출되어 있다.

주요 TLS 취약점 공격:
- **POODLE (Padding Oracle On Downgraded Legacy Encryption)**: SSL 3.0 패딩 오라클 공격
- **BEAST (Browser Exploit Against SSL/TLS)**: TLS 1.0 CBC 블록 암호 공격
- **DROWN (Decrypting RSA with Obsolete and Weakened eNcryption)**: SSLv2 약점으로 TLS 세션 복호화
- **FREAK (Factoring RSA Export Keys)**: 수출용 512비트 RSA 강제 협상
- **Logjam**: 512비트 DH (Diffie-Hellman) 파라미터 다운그레이드

이런 공격들은 오래된 TLS 버전이 "지원만 하고 있어도" 공격자가 핸드셰이크 과정에서 다운그레이드를 강제할 수 있어 위험하다.

📢 **섹션 요약 비유**: 집에 새 잠금장치를 달면서 옛날 마스터키 구멍을 막지 않으면, 공격자는 옛날 구멍으로 들어온다.

---

## Ⅱ. 아키텍처 및 핵심 원리

TLS 버전별 현황과 권장 수준:

| TLS 버전 | 상태 | 출시 | 권고 |
|:---:|:---|:---:|:---|
| SSL 3.0 | 완전 폐기 | 1996 | 즉시 비활성화 |
| TLS 1.0 | 공식 폐기 (RFC 8996) | 1999 | 즉시 비활성화 |
| TLS 1.1 | 공식 폐기 (RFC 8996) | 2006 | 즉시 비활성화 |
| TLS 1.2 | 허용 (설정 주의 필요) | 2008 | 강력한 스위트만 허용 |
| TLS 1.3 | 권장 현재 표준 | 2018 | 모든 신규 서비스 적용 |

```
┌──────────────────────────────────────────────────────────┐
│           TLS 1.3 개선 포인트                            │
├──────────────────────────────────────────────────────────┤
│  1-RTT 핸드셰이크 (TLS 1.2 대비 레이턴시 감소)          │
│  0-RTT 재연결 (이전 세션 재개)                           │
│  취약 암호화 스위트 전면 제거 (RC4, DES, NULL 등)        │
│  PFS (Perfect Forward Secrecy) 기본 강제               │
│  RSA 키 교환 제거 → ECDHE/DHE만 허용                    │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: TLS 1.3는 낡은 자물쇠 구멍을 모두 용접해버리고, 최신 생체 인식만 남긴 것과 같다.

---

## Ⅲ. 비교 및 연결

| 구분 | TLS 1.2 | TLS 1.3 |
|:---|:---|:---|
| 핸드셰이크 | 2-RTT | 1-RTT (0-RTT 재연결) |
| PFS | 선택적 | 기본 강제 |
| 취약 암호 제거 | 불완전 | RC4, DES, 수출암호 전면 제거 |
| 속도 | 느림 | 빠름 |
| 브라우저 지원 | 전체 | 최신 브라우저 (99%+) |

📢 **섹션 요약 비유**: TLS 1.2는 구형 자동차(안전벨트 있음), TLS 1.3은 에어백·충돌방지·자동제동까지 갖춘 최신 자동차다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**Nginx TLS 설정 예시**:
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-CHACHA20-POLY1305;
ssl_prefer_server_ciphers on;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";
```

**정기 점검 도구**:
- **SSL Labs Server Test**: ssllabs.com/ssltest — A+ 등급 목표
- **testssl.sh**: 명령줄 TLS 취약점 스캔 도구
- **Qualys SSL Pulse**: 대규모 TLS 설정 모니터링

📢 **섹션 요약 비유**: SSL Labs A+ 등급은 자동차 충돌 안전 테스트 최고 등급과 같다. 설정 후 반드시 외부 검증을 받아야 한다.

---

## Ⅴ. 기대효과 및 결론

TLS 1.3 전용 설정과 HSTS preload 등록을 완료하면 전송 계층 보안을 현재 최고 수준으로 높일 수 있다. HSTS preload는 브라우저 출하 시점부터 HTTPS를 강제해 SSLStrip 공격도 방어한다.

기술사 관점에서 TLS 설정은 인프라 수준의 보안 요소로, IaC (Infrastructure as Code) 템플릿에 강제 설정을 포함시키고 CSPM (Cloud Security Posture Management) 도구로 준수 여부를 지속 모니터링해야 한다.

📢 **섹션 요약 비유**: TLS 버전 관리는 소프트웨어 패치처럼 지속적 유지보수가 필요하다. 한 번 설정하고 잊으면 새로운 공격에 무방비 상태가 된다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| POODLE | 공격 예시 | SSL 3.0 패딩 오라클 |
| PFS | 보안 속성 | 세션 키 노출 최소화 |
| HSTS | 보완 통제 | HTTP→HTTPS 강제 전환 |
| Certificate Pinning | 추가 방어 | 인증서 위변조 방지 |
| Cipher Suite | 설정 요소 | 암호화 알고리즘 조합 |

### 👶 어린이를 위한 3줄 비유 설명
- TLS는 인터넷에서 편지를 안전하게 보내는 봉투인데, 낡은 봉투는 쉽게 뜯을 수 있어.
- TLS 1.3은 봉투 위에 특수 잠금장치까지 달린 가장 최신 봉투야.
- 낡은 봉투(SSL 3.0, TLS 1.0)는 쓰지 말고, 항상 최신 봉투를 써야 안전해!
""")

print("Batch 2 done (420, 423-426).")
