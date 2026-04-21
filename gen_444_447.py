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

w("444_security_misconfiguration_deep.md", 444, "444. A05 보안 설정 오류 심화", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: A05 Security Misconfiguration (보안 설정 오류) 심화는 기본 오류를 넘어 클라우드 IAM (Identity and Access Management) 과다 권한, HTTP 보안 헤더 누락, XML 외부 엔티티(XXE, XML External Entity) 처리 오설정 등 복잡한 설정 오류 유형을 다룬다.
> 2. **가치**: 2021 OWASP에서 A05로 5위를 유지했으며, 클라우드 전환으로 오설정 공격 표면이 폭발적으로 증가했다. CSPM (Cloud Security Posture Management) 도구의 필요성이 급증한 배경이다.
> 3. **판단 포인트**: HTTP 보안 헤더(CSP, HSTS, X-Frame-Options), XML 파서 보안 설정, 클라우드 IAM 최소 권한이 심화 대응의 3대 축이다.

---

## Ⅰ. 개요 및 필요성

Security Misconfiguration 심화는 단순 기본 비밀번호 미변경을 넘어, 더 복잡하고 탐지하기 어려운 설정 오류들을 다룬다.

**심화 오설정 유형**:
1. **XXE (XML External Entity) 처리**: XML 파서가 외부 엔티티를 처리해 파일 시스템 접근·SSRF (Server-Side Request Forgery) 가능
2. **HTTP 보안 헤더 누락**: CSP (Content Security Policy), HSTS (HTTP Strict Transport Security), X-Frame-Options, X-Content-Type-Options 미설정
3. **CORS 와일드카드**: `Access-Control-Allow-Origin: *` 과다 허용
4. **클라우드 IAM 과다 권한**: EC2 인스턴스에 AdministratorAccess 역할 부여
5. **시크릿 환경 변수 로그 출력**: 설정값이 로그에 평문으로 기록

📢 **섹션 요약 비유**: 심화 오설정은 수면 아래에 있는 빙산 부분이다. 쉽게 보이는 기본 비밀번호 미변경은 빙산 위쪽이고, XXE·IAM 과다 권한은 훨씬 더 크고 위험한 아래 부분이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

**HTTP 보안 헤더 효과**:

| 헤더 | 방어 대상 | 예시 값 |
|:---|:---|:---|
| Content-Security-Policy (CSP) | XSS (Cross-Site Scripting) | `default-src 'self'` |
| Strict-Transport-Security (HSTS) | SSL Stripping | `max-age=31536000; includeSubDomains` |
| X-Frame-Options | 클릭재킹 | `DENY` 또는 `SAMEORIGIN` |
| X-Content-Type-Options | MIME 스니핑 | `nosniff` |
| Referrer-Policy | 정보 유출 | `strict-origin-when-cross-origin` |
| Permissions-Policy | 브라우저 기능 제한 | `camera=(), microphone=()` |

```
┌──────────────────────────────────────────────────────────┐
│           XXE 공격 흐름 (보안 설정 오류 심화)            │
├──────────────────────────────────────────────────────────┤
│  공격자가 악성 XML 전송:                                 │
│  <?xml version="1.0"?>                                   │
│  <!DOCTYPE test [<!ENTITY xxe SYSTEM "file:///etc/passwd"│
│  ]><test>&xxe;</test>                                    │
│       │                                                  │
│       ▼                                                  │
│  XML 파서가 외부 엔티티 처리 → /etc/passwd 반환          │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: HTTP 보안 헤더는 집 안의 각 방에 개별 잠금장치를 다는 것이다. 현관문(HTTPS)만으로는 집 안 방들까지 보호하지 못한다.

---

## Ⅲ. 비교 및 연결

| 심화 오설정 | 위험 | 방어 |
|:---|:---|:---|
| XXE | 파일 읽기, SSRF, DoS | XML 파서 외부 엔티티 비활성화 |
| HTTP 헤더 누락 | XSS, 클릭재킹, 다운그레이드 | securityHeaders 미들웨어 |
| IAM 과다 권한 | 클라우드 전체 침해 | 최소 권한 + IAM Access Analyzer |
| CORS 와일드카드 | 데이터 탈취 | 엄격한 Origin 화이트리스트 |

📢 **섹션 요약 비유**: 각 심화 오설정은 서로 다른 창문이 열려있는 것이다. 하나씩 닫지 않으면 어느 창문으로든 침입이 가능하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**XXE 방어 (Java SAXParserFactory)**:
```java
SAXParserFactory factory = SAXParserFactory.newInstance();
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
```

**클라우드 IAM 최소 권한 원칙**:
1. **IAM Access Analyzer**: 실제 사용한 권한 분석, 미사용 권한 제거 권고
2. **SCP (Service Control Policy)**: AWS Organizations 수준 권한 상한 설정
3. **Permission Boundary**: IAM 역할/사용자의 최대 권한 경계 설정

📢 **섹션 요약 비유**: IAM Access Analyzer는 직원이 실제로 사용하는 열쇠만 남기고, 한 번도 쓰지 않은 열쇠는 반납시키는 보안 감사다.

---

## Ⅴ. 기대효과 및 결론

HTTP 보안 헤더 자동 적용, XXE 방어 설정, IAM 최소 권한 자동화를 파이프라인에 통합하면 심화 오설정 취약점을 사전에 차단할 수 있다. securityheaders.com을 통한 정기적인 헤더 점수 확인, Prowler/ScoutSuite를 통한 클라우드 설정 감사가 현대적 운영 방법이다.

📢 **섹션 요약 비유**: 심화 보안 설정 관리는 집안 구석구석을 정기적으로 점검하는 것이다. 눈에 보이는 문뿐 아니라 환기구, 창문, 바닥까지 빠짐없이.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| XXE | 심화 취약점 | XML 외부 엔티티 처리 |
| CSP (Content Security Policy) | 보안 헤더 | XSS 방어 정책 |
| IAM Access Analyzer | 클라우드 도구 | 미사용 권한 탐지 |
| CSPM | 통합 도구 | 클라우드 보안 설정 관리 |
| SCP | 클라우드 통제 | 서비스 제어 정책 |

### 👶 어린이를 위한 3줄 비유 설명
- 보안 설정 오류 심화는 겉보기엔 괜찮아 보이지만 깊숙이 숨어있는 위험이야.
- XML 파일 처리할 때 설정 하나 잘못하면 서버 전체 파일을 읽을 수 있는 구멍이 생겨.
- 그래서 모든 레이어(XML 파서, HTTP 헤더, 클라우드 권한)를 꼼꼼히 설정해야 해!
""")

w("445_vulnerable_outdated_components.md", 445, "445. A06 취약한 구성 요소", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Vulnerable and Outdated Components (취약하고 구식인 구성 요소, A06)는 알려진 CVE (Common Vulnerabilities and Exposures) 취약점을 가진 라이브러리·프레임워크·런타임을 계속 사용해 공격자가 공개된 익스플로잇을 실행할 수 있게 되는 취약점이다.
> 2. **가치**: 2021 Log4Shell (CVE-2021-44228, CVSS 10.0), 2017 Equifax 침해(Apache Struts CVE-2017-5638)처럼 단일 라이브러리 취약점이 수천만 명의 데이터 침해로 이어진 역사적 사례가 존재한다.
> 3. **판단 포인트**: SBOM (Software Bill of Materials) 관리, SCA (Software Composition Analysis) CI/CD 통합, 자동 의존성 업데이트(Dependabot, Renovate)가 현대적 대응의 3대 축이다.

---

## Ⅰ. 개요 및 필요성

현대 소프트웨어의 80% 이상이 오픈소스 라이브러리로 구성된다. 이 라이브러리들은 지속적으로 새로운 취약점이 발견되며, 패치 없이 사용하면 공격자가 공개된 PoC (Proof of Concept) 코드로 즉시 공격할 수 있다.

**역사적 대형 사고**:
| 취약점 | 연도 | 영향 라이브러리 | 피해 |
|:---|:---:|:---|:---|
| Heartbleed | 2014 | OpenSSL | 전 세계 서버 66% 영향 |
| Apache Struts RCE | 2017 | Struts 2 | Equifax 1억 4,300만 명 데이터 유출 |
| Log4Shell | 2021 | Log4j | 수만 개 조직 동시 영향 |
| Spring4Shell | 2022 | Spring Framework | Spring 생태계 전반 |

📢 **섹션 요약 비유**: 취약한 구성 요소는 완벽한 자동차에 리콜 대상인 브레이크 패드를 그대로 쓰는 것이다. 내 잘못이 아니어도 사고가 난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SCA (Software Composition Analysis) 도구 생태계:

| 도구 | 특징 | 통합 방법 |
|:---|:---|:---|
| OWASP Dependency-Check | 오픈소스, NVD 연동 | Maven/Gradle 플러그인 |
| Snyk | 상용, 실시간 DB | GitHub Actions, CI/CD |
| Dependabot | GitHub 내장 | 자동 PR 생성 |
| Renovate | 오픈소스 | 유연한 규칙 설정 |
| Trivy | 컨테이너 특화 | Docker 스캔 |

```
┌──────────────────────────────────────────────────────────┐
│           SCA + SBOM 통합 파이프라인                     │
├──────────────────────────────────────────────────────────┤
│  코드 커밋 → [Dependabot/Renovate] 의존성 자동 감지      │
│       │                                                  │
│       ▼                                                  │
│  빌드 → [SCA 스캔] CVE 탐지 → CVSS 임계값 이상 시 빌드  │
│           차단                                           │
│       │                                                  │
│       ▼                                                  │
│  배포 → [Trivy] 컨테이너 이미지 스캔                     │
│       │                                                  │
│       ▼                                                  │
│  운영 → [SBOM] 구성 요소 목록 관리 → CVE 신규 알림      │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: SCA는 식품 성분 라벨을 읽어주는 도우미다. 배달 온 재료(라이브러리)가 리콜 대상인지 자동으로 확인해준다.

---

## Ⅲ. 비교 및 연결

| 구분 | A06 Vulnerable Components | A08 Integrity Failures |
|:---|:---|:---|
| 핵심 위험 | 알려진 취약점을 가진 버전 사용 | 변조된 컴포넌트 배포 |
| 탐지 방법 | SCA 스캔 | 코드 서명, 해시 검증 |
| 공격자 행동 | 공개 CVE 익스플로잇 실행 | 공급망 침해 |
| 예방 | 최신 패치 버전 사용 | 무결성 검증 |

📢 **섹션 요약 비유**: A06는 낡은 자물쇠를 사용하는 것이고, A08은 자물쇠 제조사가 마스터키를 심은 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**의존성 관리 전략**:
1. **버전 고정(Version Pinning)**: `package-lock.json`, `requirements.txt`에 정확한 버전과 해시 고정
2. **SBOM 생성**: `syft`, `cdxgen`으로 CycloneDX 형식 SBOM 자동 생성
3. **CVE 임계값 정책**: CVSS 7.0 이상 취약점은 빌드 차단, 4.0 이상은 경고
4. **의존성 감사 주기**: 주간 자동 스캔, Critical CVE는 즉시 대응
5. **EOL (End of Life) 추적**: endoflife.date 서비스로 라이브러리 지원 종료 추적

📢 **섹션 요약 비유**: CVE 임계값 정책은 식품 유통기한 관리와 같다. 만료된(취약한) 재료는 자동으로 거부하고, 임박한(위험 임박) 재료는 경고를 받는다.

---

## Ⅴ. 기대효과 및 결론

SCA + SBOM + 자동 패치 봇 조합은 취약한 구성 요소 위험을 구조적으로 관리할 수 있는 현대적 체계다. 미국 정부의 SBOM 의무화 정책과 EU CRA (Cyber Resilience Act)는 이를 규제 수준으로 강제하고 있으며, 이에 대비한 선제적 도입이 필요하다.

📢 **섹션 요약 비유**: SBOM은 소프트웨어의 성분표다. 식품 성분표처럼, 모든 소프트웨어가 무엇으로 만들어졌는지 투명하게 공개하는 것이 미래의 표준이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| CVE | 기준 | 공개 취약점 식별자 |
| SCA | 탐지 도구 | 의존성 취약점 자동 분석 |
| SBOM | 관리 문서 | 소프트웨어 구성 요소 목록 |
| Log4Shell | 실제 사례 | Log4j JNDI 인젝션 취약점 |
| Dependabot | 자동화 도구 | GitHub 의존성 자동 업데이트 |

### 👶 어린이를 위한 3줄 비유 설명
- 취약한 구성 요소는 케이크를 만들 때 썩은 밀가루를 쓰는 것처럼, 나쁜 부품이 있는 라이브러리를 쓰는 거야.
- Log4Shell 같은 사고는 그 나쁜 부품 하나 때문에 수만 개 회사가 동시에 피해를 입은 거야.
- 그래서 SCA 도구로 쓰는 모든 부품이 안전한지 자동으로 확인해야 해!
""")

w("446_cve_dependency.md", 446, "446. CVE 취약점 의존성", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CVE (Common Vulnerabilities and Exposures) 취약점 의존성은 소프트웨어가 사용하는 라이브러리·컴포넌트에 알려진 CVE 취약점이 있을 때, 해당 취약점이 애플리케이션에도 상속되는 보안 위험이다.
> 2. **가치**: CVSS (Common Vulnerability Scoring System) 점수와 의존성 깊이(직접·전이적 의존성)를 교차 분석해 우선순위를 정하고, 패치 가능 여부와 완화 방법을 조합해 대응해야 한다.
> 3. **판단 포인트**: 직접 의존성(direct dependency)보다 전이적 의존성(transitive dependency)에 의한 CVE가 탐지하기 어렵고 더 많으므로, SBOM 기반 전체 의존성 트리 관리가 핵심이다.

---

## Ⅰ. 개요 및 필요성

현대 소프트웨어의 의존성 구조는 복잡한 트리를 이룬다. 직접 사용하는 라이브러리(1단계)뿐 아니라, 그 라이브러리가 사용하는 라이브러리(2단계), 그리고 그 이상의 전이적 의존성까지 포함하면 수백 개의 컴포넌트가 된다. 이 중 어느 하나에라도 CVE가 있으면 애플리케이션이 취약해진다.

**의존성 트리 구조**:
```
my-app
├── spring-boot 3.1.0
│   ├── spring-core 6.0.0
│   │   └── commons-logging 1.2 ← CVE-2014-0119 존재
│   └── jackson-databind 2.15.0
│       └── jackson-core 2.15.0 ← CVE-XXXX 존재 시 전이
└── log4j 2.17.1 (패치 버전)
```

직접 의존성(spring-boot, jackson-databind)을 최신으로 유지해도, 그 내부에서 사용하는 라이브러리에 취약점이 있으면 위험이 남는다.

📢 **섹션 요약 비유**: CVE 의존성은 안전한 재료를 사서도 그 재료를 만든 공장의 원재료가 오염된 경우와 같다. 내가 직접 산 재료가 아니라 2~3단계 공급망까지 확인해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| CVE 속성 | 설명 | 대응 |
|:---|:---|:---|
| CVSS Score | 취약점 심각도 (0-10) | 7.0+: 즉시 패치, 4.0-6.9: 계획적 패치 |
| Attack Vector | 네트워크/로컬 등 공격 경로 | Network: 높은 우선순위 |
| Exploitability | 익스플로잇 가용성 | PoC 공개 시 즉시 대응 |
| 영향 범위 | 기밀성/무결성/가용성 | CIA Triad 평가 |

```
┌──────────────────────────────────────────────────────────┐
│           CVE 의존성 관리 우선순위 결정                  │
├──────────────────────────────────────────────────────────┤
│  CVSS 9.0+ + PoC 공개 + 직접 의존성 → 즉시 패치         │
│  CVSS 7.0+ + 네트워크 접근 가능     → 48시간 내 패치     │
│  CVSS 4.0-6.9 + 간접 의존성        → 스프린트 내 계획   │
│  CVSS 4.0 미만                     → 다음 정기 업데이트  │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: CVE 대응은 긴급도에 따라 분류하는 응급실 트리아지다. CVSS 10점은 응급실 1번, 4점 미만은 일반 진료 대기다.

---

## Ⅲ. 비교 및 연결

| 구분 | 직접 의존성 CVE | 전이적 의존성 CVE |
|:---|:---|:---|
| 탐지 용이성 | 비교적 쉬움 | 어려움 (깊은 트리) |
| 패치 방법 | 버전 직접 업그레이드 | 상위 의존성 업그레이드 또는 exclusion |
| 빈도 | 낮음 | 높음 |
| 도구 | `npm audit`, `pip-audit` | SBOM 기반 전체 스캔 |

📢 **섹션 요약 비유**: 직접 의존성 취약점은 직접 산 자동차 부품 결함이고, 전이적 의존성 취약점은 그 부품을 만든 공장의 원자재 결함이다. 둘 다 사고의 원인이 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**의존성 취약점 관리 도구**:
1. **npm audit fix**: Node.js 패키지 자동 취약점 수정
2. **pip-audit**: Python 패키지 취약점 스캔
3. **OWASP Dependency-Check**: Java/Python/Ruby 멀티 언어 지원
4. **Trivy**: 컨테이너 이미지 포함 SBOM + CVE 매핑
5. **VEX (Vulnerability Exploitability eXchange)**: 취약점이 실제로 익스플로잇 가능한지 문서화

**VEX 활용**: CVE가 탐지되더라도 실제 코드 경로에서 해당 기능이 사용되지 않으면 "Not Affected"로 표시해 불필요한 패닉을 줄일 수 있다.

📢 **섹션 요약 비유**: VEX는 "우리 창고에 결함 있는 부품이 있긴 하지만, 이 제품에는 그 부품이 안 쓰여서 괜찮습니다"라는 공식 선언이다.

---

## Ⅴ. 기대효과 및 결론

CVE 의존성 관리를 체계화하면 운영 중 취약점 노출 시간(Window of Exposure)을 최소화할 수 있다. SBOM + SCA + VEX의 조합은 현재 가장 진보한 의존성 보안 관리 체계이며, 미국 CISA (Cybersecurity and Infrastructure Security Agency)가 권장하는 공급망 보안 표준이다.

📢 **섹션 요약 비유**: CVE 의존성 관리는 복잡한 공급망의 안전을 보장하는 품질 관리 시스템이다. 완성품뿐 아니라 원자재 단계까지 추적하는 것이 목표다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| CVSS | 평가 기준 | 취약점 심각도 점수 |
| NVD (National Vulnerability Database) | CVE 저장소 | 미국 NIST 운영 CVE DB |
| Transitive Dependency | 위험 경로 | 간접 의존성 취약점 |
| VEX | 익스플로잇 문서 | 취약점 실제 영향 명시 |
| SBOM | 관리 기반 | 전체 의존성 목록 |

### 👶 어린이를 위한 3줄 비유 설명
- CVE는 프로그램 부품의 결함 번호야. 처럼 리콜 번호처럼 공식으로 등록된 버그야.
- 내가 직접 쓰는 라이브러리뿐 아니라, 그 라이브러리가 쓰는 라이브러리까지 체크해야 해.
- 그래서 SCA 도구로 모든 부품의 결함을 자동으로 찾아내는 게 중요해!
""")

w("447_sca.md", 447, "447. SCA (Software Composition Analysis)", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SCA (Software Composition Analysis, 소프트웨어 구성 요소 분석)는 애플리케이션이 사용하는 오픈소스 라이브러리와 서드파티 컴포넌트의 CVE (Common Vulnerabilities and Exposures) 취약점, 라이선스 이슈, 버전 정보를 자동으로 탐지·분석하는 보안 도구이다.
> 2. **가치**: SCA는 CI/CD (Continuous Integration/Continuous Delivery) 파이프라인에 통합해 "취약한 라이브러리가 포함된 빌드는 배포하지 않는다"는 게이팅 정책을 자동으로 시행할 수 있다.
> 3. **판단 포인트**: SAST (Static Application Security Testing)가 자체 코드의 취약점을 분석한다면, SCA는 의존성 코드의 취약점을 분석한다. 둘을 함께 사용해야 전체 코드베이스를 커버할 수 있다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 개발팀이 직접 작성하는 코드는 전체 코드베이스의 20~30%에 불과하다. 나머지 70~80%는 오픈소스 라이브러리와 프레임워크다. SAST가 직접 작성 코드를 분석하지만, 의존성 코드는 SAST로 분석하기 어렵다. SCA가 이 간극을 메운다.

SCA가 제공하는 분석 결과:
- **취약점 분석**: 의존성 라이브러리의 CVE 목록과 CVSS 점수
- **라이선스 분석**: GPL, LGPL, MIT, Apache 등 라이선스 호환성 검토
- **버전 분석**: 최신 버전과의 차이, 업그레이드 권고
- **SBOM 생성**: 전체 구성 요소 목록 자동 생성

📢 **섹션 요약 비유**: SCA는 식품의 성분 분석 기계다. 요리사(개발자)가 직접 만든 음식이 아니라, 외부에서 사온 재료(라이브러리)에 문제가 없는지 검사한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SCA 동작 원리 및 CI/CD 통합:

| 단계 | SCA 활동 | 결과 |
|:---|:---|:---|
| 의존성 수집 | package.json, pom.xml 파싱 | 전체 의존성 트리 |
| CVE 매핑 | NVD, OSV, GitHub Advisory DB와 비교 | CVE 목록 + CVSS 점수 |
| 정책 적용 | CVSS 임계값, 라이선스 화이트리스트 | 허용/거부 결정 |
| 보고서 생성 | SBOM (CycloneDX/SPDX) 출력 | 감사·컴플라이언스 |

```
┌──────────────────────────────────────────────────────────┐
│           SCA CI/CD 통합 흐름                            │
├──────────────────────────────────────────────────────────┤
│  코드 커밋                                               │
│       │                                                  │
│       ▼                                                  │
│  CI 파이프라인 시작                                      │
│  ├── SAST (자체 코드 분석)                               │
│  ├── SCA (의존성 취약점 분석)  ← 여기                    │
│  │       CVSS ≥ 7.0: 빌드 차단                          │
│  │       CVSS 4.0-6.9: 경고                             │
│  └── DAST (런타임 취약점 분석)                           │
│       │                                                  │
│       ▼                                                  │
│  통과 시: 배포 진행                                      │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: SCA 게이팅은 공항 수하물 검색대와 같다. 취약한 라이브러리를 가진 코드가 배포 비행기에 탑승하지 못하게 막는다.

---

## Ⅲ. 비교 및 연결

| 구분 | SAST | SCA | DAST |
|:---|:---|:---|:---|
| 분석 대상 | 자체 작성 코드 | 의존성·오픈소스 | 실행 중인 애플리케이션 |
| 시점 | 빌드 전 | 빌드 시 | 배포 후 |
| 오탐(False Positive) | 높음 | 낮음 | 낮음 |
| 대표 도구 | SonarQube, Checkmarx | Snyk, Dependabot | OWASP ZAP, Burp Suite |

📢 **섹션 요약 비유**: SAST는 내가 쓴 글의 맞춤법을 검사하고, SCA는 참고 문헌의 신뢰성을 검증하고, DAST는 실제 발표 현장에서 청중 반응을 테스트하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**주요 SCA 도구 비교**:
| 도구 | 무료/유료 | 강점 | CI/CD 통합 |
|:---|:---:|:---|:---:|
| OWASP Dependency-Check | 무료 | 다양한 언어 지원 | Maven, Gradle |
| Snyk | 유료(무료 플랜) | 실시간 취약점 DB | GitHub, GitLab |
| Dependabot | 무료(GitHub) | 자동 PR 생성 | GitHub Actions |
| Trivy | 무료 | 컨테이너 이미지 포함 | 모든 CI/CD |
| Black Duck | 유료 | 엔터프라이즈 컴플라이언스 | 대기업 환경 |

**라이선스 관리**:
- GPL 라이선스 라이브러리: 소스 공개 의무 발생 → 상용 제품에 부적합
- MIT/Apache 2.0: 상용 사용 자유, 출처 표기 필요
- LGPL: 동적 링크 시 허용, 정적 링크 시 소스 공개 의무

📢 **섹션 요약 비유**: SCA 라이선스 분석은 요리 레시피의 저작권을 확인하는 것이다. 상업용 식당에서 저작권이 있는 레시피를 무단으로 쓰면 법적 문제가 생긴다.

---

## Ⅴ. 기대효과 및 결론

SCA를 CI/CD 파이프라인에 통합하면 취약한 의존성이 포함된 소프트웨어가 운영 환경에 배포되는 것을 자동으로 방지할 수 있다. SBOM 자동 생성을 결합하면 컴플라이언스 증빙 자료도 함께 확보된다.

기술사 관점에서 SCA는 DevSecOps (Development, Security, Operations) 파이프라인의 필수 구성 요소로, Shift Left Security(보안을 개발 초기로 당기기)의 핵심 도구다.

📢 **섹션 요약 비유**: SCA 없이 개발하는 것은 재료 검사 없이 음식을 파는 것이다. 맛은 있을지 몰라도 안전은 보장할 수 없다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SBOM | 산출물 | SCA 결과로 생성되는 구성 요소 목록 |
| NVD | CVE 데이터 소스 | SCA가 비교하는 취약점 DB |
| SAST | 보완 도구 | 자체 코드 정적 분석 |
| Snyk | 대표 도구 | 실시간 CVE DB 연동 SCA |
| DevSecOps | 통합 프레임워크 | 개발·보안·운영 통합 |

### 👶 어린이를 위한 3줄 비유 설명
- SCA는 내가 만든 음식에 들어간 모든 재료가 안전한지 확인하는 검사기야.
- 내가 직접 만든 부분(코드)만 아니라, 다른 곳에서 가져온 부분(라이브러리)도 다 검사해.
- CI/CD 파이프라인에 연결하면 문제 있는 라이브러리가 있으면 자동으로 배포를 막아줘!
""")

print("Batch 444-447 done.")
