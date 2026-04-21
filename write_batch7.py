import os
BASE = "/Users/pf/workspace/brainscience/content/studynote/07_enterprise_systems/05_data_bi"
def w(fn, txt):
    path = os.path.join(BASE, fn)
    if os.path.exists(path): print(f"SKIP: {fn}"); return
    with open(path, 'w', encoding='utf-8') as f: f.write(txt)
    print(f"OK: {fn}")

w("317_tde_vs_application_encryption.md", """\
+++
weight = 317
title = "317. 데이터베이스 암호화 TDE vs 애플리케이션 레벨 암호화 (TDE vs Application Encryption)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TDE (Transparent Data Encryption)는 DB 엔진이 디스크 I/O 시점에 자동 암·복호화하는 투명한 암호화이고, 애플리케이션 레벨 암호화는 앱이 필드 단위로 제어하는 세밀한 암호화다.
> 2. **가치**: TDE는 성능 오버헤드 <5%로 전체 데이터 보호가 가능하지만, DB 관리자(DBA)가 평문으로 접근 가능하다는 한계가 있다. 필드 레벨 암호화는 DBA 접근도 차단한다.
> 3. **판단 포인트**: GDPR, PCI-DSS 규정은 저장 데이터 암호화를 요구하지만, 누가 암호화 키를 관리하는지가 내부 위협 대응의 핵심이다.

## Ⅰ. 개요 및 필요성

데이터베이스에 저장된 민감 데이터가 해킹, 내부자 유출, 물리적 디스크 탈취로 노출되는 사고가 지속 발생한다.
특히 PCI-DSS (Payment Card Industry Data Security Standard)는 카드 번호 암호화를 의무화하고, GDPR은 개인정보 암호화를 권고한다.

데이터베이스 암호화의 두 주요 방식:
- **TDE (Transparent Data Encryption)**: DB 엔진 레벨에서 파일/페이지 단위 암호화
- **애플리케이션 레벨 암호화**: 앱이 저장 전 암호화, 조회 후 복호화 (필드 단위)

암호화 계층:
```
앱 → [앱 레벨 암호화] → DB 엔진 → [TDE] → 디스크 파일
```

📢 **섹션 요약 비유**: TDE는 금고 자체를 잠그는 것(건물 안 사람은 금고 내용 볼 수 있음), 앱 레벨 암호화는 금고 안 물건도 개별 봉투에 넣는 것(열쇠 없으면 내용 불가)이다.

## Ⅱ. 아키텍처 및 핵심 원리

### TDE 작동 메커니즘

TDE는 DEK (Data Encryption Key) + KEK (Key Encryption Key) 2계층 키 구조를 사용한다:

```
평문 데이터 → AES-256으로 암호화 (DEK 사용) → 암호문 저장
DEK 자체도 KEK(마스터 키)로 암호화하여 키 파일에 저장
KEK는 HSM (Hardware Security Module) 또는 KMS에 보관
```

TDE 적용 범위:
- Data at Rest: 데이터 파일(.mdf), 트랜잭션 로그, 백업 파일
- 메모리 상의 데이터(버퍼 풀)는 평문 → DBA 접근 가능

### 필드 레벨 암호화 (Field-Level Encryption)

```python
# 애플리케이션에서 저장 전 암호화
from cryptography.fernet import Fernet

def store_sensitive_field(ssn: str) -> bytes:
    key = kms.get_key("ssn-encryption-key")
    f = Fernet(key)
    return f.encrypt(ssn.encode())  # 암호문 저장

# 조회 시 복호화
def retrieve_sensitive_field(encrypted: bytes) -> str:
    key = kms.get_key("ssn-encryption-key")
    f = Fernet(key)
    return f.decrypt(encrypted).decode()
```

FPE (Format-Preserving Encryption): 암호문이 원본과 같은 형식 유지
- 카드번호 4532-XXXX-XXXX-1234 → 9871-XXXX-XXXX-5634 (형식 유지)
- 레거시 시스템 호환성 확보에 유용

### ASCII 다이어그램: 암호화 레이어 비교

```
  ┌──────────────────────────────────────────────────────────────┐
  │                  암호화 계층 비교                             │
  │                                                              │
  │  애플리케이션 레벨 암호화                                     │
  │  ┌────────────────────────────────────────────────────────┐  │
  │  │  App → 필드 암호화 → DB 저장                           │  │
  │  │  - DBA가 조회해도 암호문만 보임 ✅                      │  │
  │  │  - 쿼리 시 복호화 후 비교 (인덱스 제한) ⚠             │  │
  │  └────────────────────────────────────────────────────────┘  │
  │                          ↓                                   │
  │  TDE (Transparent Data Encryption)                           │
  │  ┌────────────────────────────────────────────────────────┐  │
  │  │  DB 엔진 → AES-256 → 디스크 파일                      │  │
  │  │  - DB 버퍼(메모리)는 평문 → DBA 접근 가능 ⚠           │  │
  │  │  - 성능 오버헤드 <5% ✅                                │  │
  │  │  - 백업 파일도 자동 암호화 ✅                          │  │
  │  └────────────────────────────────────────────────────────┘  │
  │                          ↓                                   │
  │  디스크 파일 암호화 (OS/스토리지 레벨)                        │
  │  ┌────────────────────────────────────────────────────────┐  │
  │  │  BitLocker, dm-crypt, 스토리지 어레이 암호화           │  │
  │  └────────────────────────────────────────────────────────┘  │
  └──────────────────────────────────────────────────────────────┘
```

### TDE vs 애플리케이션 암호화 비교

| 항목 | TDE | 애플리케이션 레벨 암호화 |
|:---|:---|:---|
| 적용 범위 | 전체 DB 파일 | 선택 필드 |
| DBA 접근 | 평문 조회 가능 | 암호문만 보임 |
| 성능 오버헤드 | <5% | 5~20% (복호화 연산) |
| 인덱스 지원 | 정상 | 제한 (암호문 정렬 불가) |
| 구현 복잡도 | 낮음 (DB 설정) | 높음 (앱 코드 수정) |
| 키 관리 | DB 엔진 + HSM | 앱 + KMS |

📢 **섹션 요약 비유**: TDE는 건물 입구 보안 게이트, 앱 레벨 암호화는 각 방 자물쇠다. 게이트는 외부 침입을 막고, 자물쇠는 내부 직원도 막는다.

## Ⅲ. 비교 및 연결

### 규정별 암호화 요건

| 규정 | 요건 | 권장 방식 |
|:---|:---|:---|
| PCI-DSS | 카드번호 저장 시 AES-256 암호화 | FPE 또는 토큰화 |
| GDPR | 개인정보 처리 시 적절한 기술적 보호조치 | TDE + 필드 레벨 |
| HIPAA | PHI (의료정보) 암호화 | TDE + 앱 레벨 |
| 개인정보보호법 | 비밀번호 단방향 해시, 주민번호 암호화 | 앱 레벨 필수 |

📢 **섹션 요약 비유**: 규정은 최소 자물쇠 기준이다. 현관문은 잠가야 하고(TDE), 귀중품 서랍도 따로 잠가야 한다(앱 레벨).

## Ⅳ. 실무 적용 및 기술사 판단

### 암호화 설계 체크리스트

- [ ] 규정 확인: PCI-DSS, GDPR, 개인정보보호법 적용 범위
- [ ] 민감 데이터 분류: PII, 카드번호, 주민번호, 의료정보 목록화
- [ ] TDE + 필드 레벨 조합 결정: DBA 내부 위협 고려 여부
- [ ] 키 관리: HSM 또는 클라우드 KMS (AWS KMS, Azure Key Vault) 사용
- [ ] 암호화 키 로테이션: 1년 주기 권장, 자동화 필수

### 안티패턴

| 안티패턴 | 문제 | 해결 방법 |
|:---|:---|:---|
| 동일 키로 전체 암호화 | 키 유출 시 전체 데이터 노출 | 컬럼별·목적별 키 분리 |
| 암호화 키를 소스 코드에 하드코딩 | 버전 관리 노출 위험 | KMS/Vault로 외부화 |
| 백업 암호화 미적용 | 백업 유출 시 평문 노출 | TDE 사용 시 자동 포함 |

📢 **섹션 요약 비유**: 암호화 키를 소스 코드에 넣는 건 집 열쇠를 현관문에 붙여두는 것이다.

## Ⅴ. 기대효과 및 결론

| 항목 | 암호화 미적용 | TDE+앱 레벨 암호화 |
|:---|:---|:---|
| 디스크 탈취 피해 | 전체 데이터 평문 노출 | 암호문만 노출 (키 없이 해독 불가) |
| DBA 내부 유출 | 직접 조회 가능 | 앱 레벨 암호화로 차단 |
| 규정 감사 | 위반 과징금 위험 | 컴플라이언스 충족 |
| 성능 영향 | 없음 | TDE <5%, 앱 5~20% |

📢 **섹션 요약 비유**: 암호화는 보험이다. 평소엔 비용만 나가지만, 사고가 나면 가치가 증명된다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| TDE | 암호화 방식 | DB 엔진 레벨 투명 암호화 |
| DEK/KEK | 키 구조 | 데이터 키 + 마스터 키 2계층 |
| AES-256 | 알고리즘 | 현재 표준 대칭 암호화 |
| FPE | 특수 암호화 | 형식 보존 암호화 |
| HSM | 키 보관 | 하드웨어 보안 모듈 |
| KMS | 키 관리 | 클라우드 키 관리 서비스 |

### �� 어린이를 위한 3줄 비유 설명

1. TDE는 집 전체를 금고로 만드는 것이에요. 도둑이 집을 통째로 가져가도 열 수 없어요.
2. 앱 레벨 암호화는 서랍마다 자물쇠를 다는 것이에요. 집 안에 들어온 사람도 열쇠가 없으면 못 열어요.
3. KMS는 열쇠 보관함이에요. 열쇠를 소스 코드에 두지 않고 전용 보관함에서 꺼내 써요.
""")

w("318_sql_injection_defense.md", """\
+++
weight = 318
title = "318. SQL 인젝션 동적 바인딩 파서 방화벽 설계 (SQL Injection Defense)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SQL Injection (SQL 인젝션)은 사용자 입력이 SQL 구문으로 해석될 때 발생하며, PreparedStatement (파라미터 바인딩)가 가장 효과적인 근본 방어다.
> 2. **가치**: Parameterized Query는 입력값을 절대 SQL 코드로 해석하지 않아 공격을 원천 차단하고, WAF (Web Application Firewall)는 알려진 패턴의 2차 방어선을 형성한다.
> 3. **판단 포인트**: 방어 심층 구조(Defense in Depth)는 앱 레벨(바인딩), WAF(웹 방화벽), DB 방화벽(화이트리스트), 최소 권한 원칙(Least Privilege) 4계층을 모두 갖춰야 한다.

## Ⅰ. 개요 및 필요성

SQL Injection은 OWASP (Open Web Application Security Project) Top 10 목록에서 2021년 기준 3위를 기록한 가장 오래되고 치명적인 웹 취약점이다.

기본 공격 예시:
```sql
-- 정상 쿼리
SELECT * FROM users WHERE username = 'alice' AND password = 'secret';

-- 공격 입력: username = "admin'--"
SELECT * FROM users WHERE username = 'admin'--' AND password = '...';
-- → 주석(--) 이후 무시, admin으로 인증 우회
```

공격 유형:
- Classic (고전): WHERE 1=1로 전체 데이터 추출
- Blind (블라인드): 참/거짓으로 데이터 비트 추론
- Time-based: SLEEP(5)로 조건 참/거짓 판별
- Out-of-band: DNS 쿼리로 데이터 외부 전송

피해 범위: 전체 DB 탈취, 인증 우회, 관리자 권한 획득, 데이터 삭제

📢 **섹션 요약 비유**: SQL Injection은 주문서에 "모든 음식 무료 제공"이라고 적어 넣는 것이다. 주방이 주문서를 검증 없이 그대로 처리하면 피해가 발생한다.

## Ⅱ. 아키텍처 및 핵심 원리

### PreparedStatement (파라미터 바인딩) 원리

```java
// 취약한 코드 (동적 쿼리 - SQL Injection 가능)
String query = "SELECT * FROM users WHERE id = " + userId; // 위험!

// 안전한 코드 (PreparedStatement - SQL Injection 불가)
PreparedStatement stmt = conn.prepareStatement(
    "SELECT * FROM users WHERE id = ?"
);
stmt.setString(1, userId); // userId가 SQL 코드가 아닌 데이터로만 처리
```

바인딩 메커니즘:
1. SQL 구문을 먼저 DB 서버에서 파싱·컴파일
2. 파라미터는 데이터로만 전달 (코드 실행 불가)
3. `admin'--` 입력 시 그냥 문자열 `admin'--` 로만 취급

### ORM 파라미터화

```python
# Django ORM - 자동 파라미터화
User.objects.filter(username=request.GET['username'])

# SQLAlchemy (Raw SQL도 안전하게)
session.execute(
    text("SELECT * FROM users WHERE id = :user_id"),
    {"user_id": user_id}
)
```

### ASCII 다이어그램: Defense-in-Depth 계층

```
  사용자 요청
       │
       ▼
  ┌────────────────────────────────────────────────────────┐
  │  Layer 1: 입력 유효성 검사 (Input Validation)           │
  │  - 허용 문자 화이트리스트 (영숫자, 특수문자 제한)          │
  │  - 길이 제한, 타입 검사                                 │
  └────────────────────────────┬───────────────────────────┘
                               ▼
  ┌────────────────────────────────────────────────────────┐
  │  Layer 2: WAF (Web Application Firewall)               │
  │  - SQL 키워드 패턴 탐지 (UNION, SELECT, DROP 등)        │
  │  - 알려진 공격 시그니처 차단                            │
  │  - Mod_Security, AWS WAF, Cloudflare                   │
  └────────────────────────────┬───────────────────────────┘
                               ▼
  ┌────────────────────────────────────────────────────────┐
  │  Layer 3: 앱 레벨 (PreparedStatement / ORM)            │
  │  - 파라미터 바인딩으로 SQL 인젝션 원천 차단 ✅ (핵심)   │
  │  - 동적 쿼리 금지, 저장 프로시저 활용                  │
  └────────────────────────────┬───────────────────────────┘
                               ▼
  ┌────────────────────────────────────────────────────────┐
  │  Layer 4: DB 방화벽 + 최소 권한                        │
  │  - DB 방화벽: 쿼리 화이트리스트 (Imperva, McAfee DAM)  │
  │  - App 계정: SELECT/INSERT/UPDATE 권한만, DROP 불가     │
  │  - 민감 테이블 조회 시도 알람                          │
  └────────────────────────────────────────────────────────┘
```

### 공격 유형별 방어 매핑

| 공격 유형 | 방어 방법 |
|:---|:---|
| Classic Injection | PreparedStatement (바인딩) |
| Blind Injection | 에러 메시지 숨김, 응답 시간 표준화 |
| Time-based | DB 쿼리 타임아웃 설정 (<5초) |
| Second-order | 저장 시에도 바인딩, 조회 시 재이스케이프 |
| Stored Procedure | SP 내부에서도 동적 SQL 금지 |

📢 **섹션 요약 비유**: PreparedStatement는 주문서 양식을 미리 인쇄해두는 것이다. 손님이 어떤 내용을 적어도 미리 정해진 칸에만 들어가고, 주방 지시문을 수정할 수 없다.

## Ⅲ. 비교 및 연결

### WAF vs DB 방화벽

| 항목 | WAF | DB 방화벽 |
|:---|:---|:---|
| 위치 | 웹 서버 앞 | DB 서버 앞 |
| 분석 대상 | HTTP 요청 페이로드 | SQL 쿼리 |
| 탐지 방법 | 패턴 매칭 시그니처 | 쿼리 화이트리스트 |
| 우회 가능성 | 인코딩 우회 가능 | 쿼리 레벨 정밀 |
| 대표 제품 | AWS WAF, Cloudflare, ModSecurity | Imperva SecureSphere, McAfee DAM |

📢 **섹션 요약 비유**: WAF는 건물 입구 보안 요원, DB 방화벽은 금고실 앞 전담 경비원이다. 입구를 통과했더라도 금고실은 따로 검사한다.

## Ⅳ. 실무 적용 및 기술사 판단

### SQL Injection 방어 체크리스트

- [ ] 모든 DB 쿼리에 PreparedStatement / ORM 파라미터화 적용
- [ ] 에러 메시지에 DB 정보 미포함 (테이블명, 스키마 노출 금지)
- [ ] App DB 계정: 최소 권한 원칙 (DROP, TRUNCATE 권한 제거)
- [ ] WAF 규칙 설정 및 주기적 업데이트
- [ ] 정기 침투 테스트 (분기 1회, sqlmap 등 자동화 도구 활용)

### 안티패턴

| 안티패턴 | 문제 | 해결 방법 |
|:---|:---|:---|
| 동적 쿼리 문자열 연결 | SQL Injection 직접 노출 | PreparedStatement 필수 |
| WAF만 믿고 바인딩 미적용 | 인코딩 우회 시 방어 없음 | 다중 계층 방어 |
| SA/root 권한으로 앱 실행 | 공격 성공 시 전체 DB 삭제 가능 | 최소 권한 계정 사용 |

📢 **섹션 요약 비유**: WAF만 믿는 건 현관 잠금장치만 믿고 창문은 열어두는 것이다. 다중 방어선이 필수다.

## Ⅴ. 기대효과 및 결론

| 항목 | 미방어 | 방어 후 |
|:---|:---|:---|
| SQL Injection 성공률 | 취약 코드 100% 공격 가능 | PreparedStatement = 0% |
| 데이터 유출 피해 | 전체 DB 탈취 가능 | 암호화 + 최소 권한으로 피해 최소화 |
| 규정 준수 | OWASP 위반 | OWASP Top 10 A03 충족 |

📢 **섹션 요약 비유**: SQL Injection 방어는 자동차 안전벨트다. 하지 않아도 평소엔 멀쩡하지만, 사고 시 결과가 치명적으로 달라진다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| PreparedStatement | 핵심 방어 | 파라미터 바인딩으로 코드 분리 |
| WAF | 2차 방어 | HTTP 패턴 기반 공격 탐지 |
| DB 방화벽 | 3차 방어 | 쿼리 화이트리스트 |
| 최소 권한 | 피해 최소화 | DROP/TRUNCATE 권한 제거 |
| OWASP Top 10 | 기준 | 웹 보안 상위 10대 취약점 |

### 👶 어린이를 위한 3줄 비유 설명

1. SQL Injection은 주문서에 몰래 "전부 공짜로 해줘"라고 써넣는 것이에요.
2. PreparedStatement는 주문서 양식이 이미 인쇄돼 있어서 손님이 내용을 추가할 수 없는 것이에요.
3. 방어 심층 구조는 문 잠금, 보안 카메라, 금고를 모두 갖춘 은행처럼 여러 층의 보호가 있는 것이에요.
""")

print("317~318 완료")
