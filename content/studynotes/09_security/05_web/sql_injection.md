+++
title = "SQL Injection"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# SQL Injection

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 사용자 입력이 SQL 쿼리에 직접 삽입되어 공격자가 임의의 SQL 명령을 실행할 수 있는 취약점으로, 데이터 유출, 변조, 삭제, 인증 우회, 서버 장악까지 이어지는 치명적 공격입니다.
> 2. **가치**: OWASP Top 10 A03의 핵심이며, 파라미터화 쿼리(Prepared Statement), ORM, 입력 검증으로 100% 방어 가능한 "예방 가능한 취약점"입니다.
> 3. **융합**: Blind SQLi, Second-Order SQLi, Stored Procedure SQLi 등 다양한 변형이 있으며, WAF 탐지 규칙, 정적 분석, 침투 테스트의 주요 대상입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**SQL Injection**은 사용자 입력값이 SQL 쿼리 문자열에 검증 없이 결합될 때 발생하는 취약점입니다. 공격자는 쿼리 구조를 변경하여 데이터베이스에 접근, 수정, 삭제할 수 있습니다.

```
SQL Injection 분류:
1. In-Band SQLi (Classic)
   - Error-based: 에러 메시지로 정보 수집
   - Union-based: UNION으로 데이터 추출

2. Blind SQLi (Inferential)
   - Boolean-based: 참/거짓 응답으로 추측
   - Time-based: 응답 지연으로 추측

3. Out-of-Band SQLi
   - DNS/HTTP 채널로 데이터 유출

4. Second-Order SQLi
   - 저장된 입력이 나중에 실행됨
```

#### 2. 비유를 통한 이해
SQL Injection은 **'폼 양식 조작'**에 비유할 수 있습니다.

- **정상**: "이름: 홍길동" → "홍길동님 환영합니다"
- **SQL Injection**: "이름: 홍길동 OR 1=1--" → "모든 회원님 환영합니다"

폼의 의도를 벗어나 시스템 전체에 영향을 미치는 것입니다.

#### 3. 등장 배경 및 발전 과정
1. **1998년**: RDS (Rain Forest Puppy)가 SQL Injection 개념 최초 공개
2. **2000년대**: 웹 앱 보편화 → SQL Injection 급증
3. **2003년**: OWASP Top 10 최초 발표 (Injection 포함)
4. **2011년**: Sony PlayStation Network 유출 (SQL Injection)
5. **2019년**: SQLMap 등 자동화 도구 고도화
6. **현재**: NoSQL Injection, GraphQL Injection으로 확장

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. SQL Injection 공격 유형별 분석

```
=== 1. Error-based SQL Injection ===

정상 요청:
GET /user?id=1

백엔드 쿼리:
SELECT * FROM users WHERE id = 1

공격 요청:
GET /user?id=1'

에러 응답:
You have an error in your SQL syntax near ''' at line 1
→ 에러 메시지로 DB 정보 노출!

정보 수집:
GET /user?id=1 AND 1=CONVERT(int, @@version)--
→ Microsoft SQL Server 2019... 버전 노출


=== 2. Union-based SQL Injection ===

정상 쿼리:
SELECT title, content FROM posts WHERE id = 1

공격:
GET /post?id=1 UNION SELECT username, password FROM users--

최종 쿼리:
SELECT title, content FROM posts WHERE id = 1
UNION SELECT username, password FROM users--

→ posts 결과 + users 테이블 노출!


=== 3. Blind Boolean-based SQL Injection ===

참/거짓으로 1비트씩 추출

공격:
GET /user?id=1 AND SUBSTRING(password,1,1)='a'--

참이면: 정상 응답
거짓이면: 빈 응답 또는 에러

자동화: 1문자당 최대 256번 시도
→ 비효율적이지만 자동화 도구로 가능


=== 4. Blind Time-based SQL Injection ===

응답 지연으로 참/거짓 판단

공격:
GET /user?id=1; IF (SUBSTRING(password,1,1)='a')
              WAITFOR DELAY '0:0:5'--

참이면: 5초 지연
거짓이면: 즉시 응답

→ 에러 메시지 없어도 데이터 추출 가능!


=== 5. Second-Order SQL Injection ===

저장된 입력이 나중에 실행

1단계: 공격자가 악성 입력 저장
POST /register
username: admin'--

2단계: 관리자가 사용자 목록 조회
SELECT * FROM users WHERE username = 'admin'--'

→ 쿼리 변형!


=== 6. NoSQL Injection ===

MongoDB 예시:

정상:
db.users.find({username: username})

공격:
username = {$ne: ""}  # "빈 문자열이 아닌"
db.users.find({username: {$ne: ""}})
→ 모든 사용자 반환!
```

#### 2. 심층 방어 기법

```
=== 1. Prepared Statement (파라미터화 쿼리) ===

취약한 코드 (절대 금지!):
String query = "SELECT * FROM users WHERE username = '" +
               username + "' AND password = '" + password + "'";

안전한 코드 (Java JDBC):
String query = "SELECT * FROM users WHERE username = ? AND password = ?";
PreparedStatement stmt = conn.prepareStatement(query);
stmt.setString(1, username);
stmt.setString(2, password);

원리:
- 쿼리 구조와 데이터가 분리됨
- 사용자 입력은 항상 "데이터"로 처리
- SQL 구문으로 해석되지 않음


=== 2. ORM 사용 ===

Python SQLAlchemy (안전):
from sqlalchemy.orm import Session
from models import User

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
    # 자동으로 파라미터화


=== 3. 입력 검증 (방어적 프로그래밍) ===

화이트리스트 방식:
import re

def validate_id(user_input):
    # 숫자만 허용
    if not re.match(r'^\d+$', user_input):
        raise ValueError("Invalid ID")
    return int(user_input)


=== 4. 최소 권한 원칙 ===

애플리케이션 DB 계정:
- DROP, TRUNCATE 권한 없음
- 특정 테이블만 SELECT/INSERT/UPDATE
- 스키마 변경 권한 없음


=== 5. 에러 메시지 은닉 ===

프로덕션 설정:
- 상세 에러 대신 일반 메시지
- 스택 트레이스 노출 금지
- 에러는 로그에만 기록
```

#### 3. 방어 아키텍처

```
=== SQL Injection 방어 다층 구조 ===

┌──────────────────────────────────────────────────────────────┐
│                      Layer 1: 입력 검증                       │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  입력 유형 검증: 숫자, 이메일, URL 등                   │ │
│  │  길이 제한: 최대 입력 길이                              │ │
│  │  화이트리스트: 허용된 문자만                            │ │
│  └────────────────────────────────────────────────────────┘ │
│                              │                               │
│                              ▼                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                   Layer 2: WAF                          │ │
│  │                                                        │ │
│  │  SQL Injection 시그니처 탐지                           │ │
│  │  - UNION, SELECT, INSERT, DROP 등                      │ │
│  │  - --, /*, ; 등 SQL 메타문자                           │ │
│  │  - 기본 패턴 + 머신러닝                                 │ │
│  └────────────────────────────────────────────────────────┘ │
│                              │                               │
│                              ▼                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │             Layer 3: 파라미터화 쿼리                    │ │
│  │                                                        │ │
│  │  PreparedStatement/ORM 사용                            │ │
│  │  쿼리 구조와 데이터 분리                                │ │
│  └────────────────────────────────────────────────────────┘ │
│                              │                               │
│                              ▼                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │             Layer 4: 최소 권한 DB 계정                  │ │
│  │                                                        │ │
│  │  앱 계정: SELECT, INSERT, UPDATE만                     │ │
│  │  DROP, TRUNCATE 권한 없음                              │ │
│  └────────────────────────────────────────────────────────┘ │
│                              │                               │
│                              ▼                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │               Layer 5: 모니터링                         │ │
│  │                                                        │ │
│  │  이상 쿼리 탐지                                         │ │
│  │  대량 데이터 추출 알림                                  │ │
│  │  감사 로그                                              │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. SQL Injection 탐지 난이도

| 유형 | 탐지 난이도 | 자동화 가능 | WAF 탐지 |
|:---|:---:|:---:|:---:|
| Error-based | 쉬움 | O | O |
| Union-based | 중간 | O | O |
| Boolean Blind | 어려움 | O | △ |
| Time Blind | 매우 어려움 | O | X |
| Second-Order | 매우 어려움 | X | X |

#### 2. 과목 융합 관점

**데이터베이스와 융합**
- 저장 프로시저: sp_executesql (동적 SQL 금지)
- 뷰(View): 직접 테이블 접근 방지
- 감사(Audit): 민감 테이블 접근 로그

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 레거시 시스템 SQL Injection 대응**
- 상황: 소스 수정 불가, 3rd party 솔루션
- 판단: WAF 가상 패치
- 전략:
  1. WAF에서 SQL Injection 패턴 차단
  2. DB Proxy에서 쿼리 필터링
  3. 장기적으로 솔루션 교체

**시나리오 2: Blind SQL Injection 탐지**
- 상황: 이상 트래픽 감지, 에러 없음
- 판단: Time-based Blind 의심
- 전략:
  1. 요청 빈도 제한 (Rate Limiting)
  2. 동일 파라미터 패턴 탐지
  3. 응답 시간 이상 탐지

#### 2. 안티패턴 (Anti-patterns)

```
취약한 구현 (금지!)

1. 문자열 결합
   query = "SELECT * FROM users WHERE id = " + id;

2. 필터링만 의존
   input = input.replace("'", "''");
   → 인코딩 우회 가능

3. ORM raw 쿼리
   db.execute(f"SELECT * FROM users WHERE id = {id}");
   → ORM 사용의미 없음

올바른 구현:

1. 파라미터화 쿼리
   cursor.execute("SELECT * FROM users WHERE id = ?", (id,));

2. ORM 사용
   User.query.filter_by(id=id).first();

3. 화이트리스트 검증
   if not id.isdigit(): raise ValueError()
```

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 | 항목 | 수치/내용 |
|:---|:---|:---|
| **방어율** | 파라미터화 쿼리 | 100% |
| **데이터 유출 방지** | 전체 테이블 | 0건 |
| **규정 준수** | PCI DSS | 6.5.1 |

#### 2. 참고 표준/가이드

| 표준 | 내용 |
|:---|:---|
| **OWASP ASVS** | V5.3.1 - 파라미터화 쿼리 |
| **CWE-89** | SQL Injection |
| **PCI DSS 6.5.1** | Injection 방어 |

---

### 관련 개념 맵 (Knowledge Graph)
- [OWASP Top 10](@/studynotes/09_security/05_web/owasp_top10.md) : A03 Injection
- [WAF](@/studynotes/09_security/03_network/waf.md) : SQL Injection 탐지
- [XSS](@/studynotes/09_security/05_web/xss.md) : 다른 인젝션 유형
- [NoSQL Injection](@/studynotes/09_security/05_web/nosql_injection.md) : NoSQL 변형
- [ORM](@/studynotes/09_security/05_web/orm_security.md) : 안전한 DB 접근

---

### 어린이를 위한 3줄 비유 설명
1. **비밀 친구 목록**: SQL Injection은 선생님이 부르는 출석부를 몰래 바꾸는 것과 같아요. "홍길동 있어?"라고 물었는데 "다 있어!"라고 바꿔버리는 거예요.
2. **약속된 질문만**: 선생님이 미리 정해놓은 질문 방식만 쓰면 안전해요. "1번 학생 있어?"만 물어보는 거죠.
3. **숨기기**: 에러 메시지도 "틀렸어요"만 보여주고 자세한 내용은 안 알려줘요. 그래야 나쁜 사람이 정보를 못 얻어요!
