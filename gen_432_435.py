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

w("432_time_based_blind_sqli.md", 432, "432. Time-based Blind SQL Injection", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Time-based Blind SQL Injection (시간 기반 블라인드 SQL 인젝션)은 조건이 참일 때 DB (Database)가 의도적으로 응답을 지연(SLEEP)하게 해, 응답 시간의 차이로 데이터를 한 비트씩 추출하는 공격이다.
> 2. **가치**: 에러 메시지도, 응답 내용의 차이도 없는 완전 Blind 환경에서 유일하게 동작하는 인젝션 기법으로, 완벽하게 에러를 숨기고 응답을 균일화한 애플리케이션에서도 취약할 수 있다.
> 3. **판단 포인트**: SLEEP() 함수 직접 차단보다 파라미터화 쿼리가 근본 해결책이며, Rate Limiting과 응답 시간 모니터링으로 공격 탐지를 병행해야 한다.

---

## Ⅰ. 개요 및 필요성

Time-based Blind SQLi는 DB에서 SLEEP() 또는 WAITFOR DELAY 함수를 조건부로 실행시켜 응답 시간을 관찰하는 방식이다. 조건이 참이면 지정된 시간만큼 응답이 늦어지고, 거짓이면 즉시 응답한다. 이 차이로 데이터를 추출한다.

**MySQL 공격 예시**:
```sql
-- 첫 번째 비밀번호 글자가 'A'(ASCII 65)이면 5초 지연
' AND IF(ASCII(SUBSTR((SELECT password FROM admin LIMIT 1),1,1))=65, SLEEP(5), 0)--
```

**MS SQL 예시**:
```sql
'; IF (SELECT COUNT(*) FROM users WHERE username='admin')>0 WAITFOR DELAY '0:0:5'--
```

응답이 5초 이상 걸리면 조건이 참, 즉시 오면 거짓으로 판단해 이진 탐색으로 데이터를 추출한다.

📢 **섹션 요약 비유**: Time-based SQLi는 금고 앞에서 "맞는 번호를 누르면 1초, 아니면 즉시 꺼진다"는 신호로 비밀번호를 맞춰가는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| DB 유형 | 지연 함수 | 예시 |
|:---|:---|:---|
| MySQL | `SLEEP(seconds)` | `IF(cond, SLEEP(5), 0)` |
| MS SQL | `WAITFOR DELAY` | `WAITFOR DELAY '0:0:5'` |
| PostgreSQL | `pg_sleep(seconds)` | `SELECT CASE WHEN cond THEN pg_sleep(5) END` |
| Oracle | `DBMS_PIPE.RECEIVE_MESSAGE` | 파이프 수신 대기 |

```
┌──────────────────────────────────────────────────────────┐
│        Time-based Blind SQLi 응답 시간 분석              │
├──────────────────────────────────────────────────────────┤
│  요청 1: ASCII(pw[1])=65 → 응답 5.2초 → 참 (A=65)       │
│  요청 2: ASCII(pw[2])=100 → 응답 0.1초 → 거짓 (d≠100)  │
│  요청 3: ASCII(pw[2])=109 → 응답 5.1초 → 참 (m=109)     │
│                                                          │
│  최종: 비밀번호 = "Am..."                               │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 모스 부호처럼 "길게 = 1, 짧게 = 0"으로 신호를 보내듯, DB의 응답 속도가 공격자에게 정보를 전달한다.

---

## Ⅲ. 비교 및 연결

| 구분 | Boolean Blind | Time-based Blind |
|:---|:---|:---|
| 구분 방법 | 페이지 내용·크기 차이 | 응답 시간 (e.g., 5초 지연) |
| 완전 Blind 환경 | 불가 (차이 없으면 동작 안 함) | 가능 |
| 속도 | 느림 | 더 느림 (SLEEP 시간만큼 추가) |
| 서버 영향 | 낮음 | DB 스레드 점유, 서버 부하 |
| 탐지 난이도 | 어려움 | 응답 시간 이상 탐지 가능 |

📢 **섹션 요약 비유**: Boolean Blind는 색깔로 구분하는 신호이고, Time-based는 소리 길이로 구분하는 모스 부호다. 색깔이 안 보여도 소리는 들린다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**탐지 전략**:
1. **응답 시간 모니터링**: APM (Application Performance Monitoring) 도구로 비정상적 응답 시간 급증 탐지
2. **DB 쿼리 실행 시간 로깅**: 5초 이상 쿼리 즉시 알림
3. **WAF Time-based 탐지**: SLEEP/WAITFOR 키워드 필터링
4. **Rate Limiting**: 동일 세션의 과도한 요청 차단
5. **파라미터화 쿼리**: SLEEP 함수가 쿼리 구조에 삽입되는 것 자체를 방지

📢 **섹션 요약 비유**: 응답 시간 모니터링은 은행 직원이 "이번 고객 처리가 왜 5분이나 걸렸지?"라고 의문을 가지는 것이다.

---

## Ⅴ. 기대효과 및 결론

Time-based Blind SQLi는 파라미터화 쿼리만이 완벽한 방어책이다. WAF와 SLEEP 함수 제한은 우회 가능하다. 추가로 응답 시간 이상 탐지와 Rate Limiting을 조합하면 공격 탐지 및 완화가 가능하다. DB 수준에서 쿼리 실행 시간 제한(Statement Timeout)을 설정하면 서버 부하 위험도 줄일 수 있다.

📢 **섹션 요약 비유**: 도둑이 아무리 천천히 금고를 열어도, 감시 카메라가 "이 사람이 왜 금고 앞에 5분이나 서있지?"라는 경보를 울려야 한다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SLEEP() | 공격 함수 | MySQL 지연 유발 |
| WAITFOR DELAY | 공격 함수 | MS SQL 지연 유발 |
| APM | 탐지 도구 | 응답 시간 이상 감지 |
| Statement Timeout | 방어 설정 | DB 쿼리 최대 실행 시간 제한 |
| Boolean Blind | 연관 기법 | 응답 내용 차이 이용 |

### 👶 어린이를 위한 3줄 비유 설명
- Time-based SQLi는 컴퓨터가 "맞아!"이면 5초 쉬고, "틀려!"이면 바로 대답하는 것을 이용해 비밀을 알아내는 방법이야.
- 답을 직접 볼 수 없어도, 기다리는 시간을 보고 맞는지 틀린지 알 수 있어.
- 그래서 응답 시간이 갑자기 길어지면 "뭔가 수상해!"라고 경보가 울려야 해!
""")

w("433_orm_injection.md", 433, "433. ORM Injection", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ORM (Object-Relational Mapping) Injection은 ORM 프레임워크를 사용하더라도 동적 쿼리 생성, Raw 쿼리 사용, 안전하지 않은 파라미터 바인딩으로 인해 SQL 인젝션이 발생하는 취약점이다.
> 2. **가치**: "ORM을 쓰면 SQL 인젝션이 없다"는 잘못된 통념을 깨트리며, Hibernate HQL (Hibernate Query Language), JPA JPQL, Django ORM, SQLAlchemy 등 모든 ORM이 잘못 사용되면 취약하다.
> 3. **판단 포인트**: ORM의 파라미터 바인딩 API를 올바르게 사용하고, 불가피한 Raw 쿼리는 반드시 파라미터화해야 하며, HQL/JPQL 인젝션도 SQL 인젝션과 동일한 위험도로 처리해야 한다.

---

## Ⅰ. 개요 및 필요성

ORM은 SQL을 직접 작성하지 않고 객체 지향적 방식으로 DB를 조작해 SQL 인젝션을 방지한다고 알려져 있다. 하지만 이것은 ORM이 올바르게 사용될 때만 성립한다. 개발자가 동적 쿼리 필요성, 성능 최적화, 복잡한 조인 등을 위해 ORM의 Raw 쿼리 기능이나 문자열 연결을 사용하면 취약점이 생긴다.

**Hibernate HQL 인젝션 예시 (Java)**:
```java
// 취약한 코드: 문자열 연결로 HQL 구성
String hql = "FROM User WHERE name = '" + userName + "'";
Query query = session.createQuery(hql);

// 공격 입력: admin' OR '1'='1
// 실행 HQL: FROM User WHERE name = 'admin' OR '1'='1'
// → 전체 사용자 반환
```

**안전한 코드**:
```java
String hql = "FROM User WHERE name = :name";
Query query = session.createQuery(hql);
query.setParameter("name", userName);
```

📢 **섹션 요약 비유**: ORM은 안전한 자동 번역기지만, 번역기를 우회해 원문을 직접 삽입하면 번역기의 보호를 받을 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| ORM 프레임워크 | 취약 패턴 | 안전 패턴 |
|:---|:---|:---|
| Hibernate | `createQuery("FROM U WHERE name='"+name+"'")` | `:name` 파라미터 바인딩 |
| JPA/JPQL | 문자열 연결 | `setParameter()` 사용 |
| Django ORM | `raw(f"SELECT * WHERE name='{name}'")` | `filter(name=name)` |
| SQLAlchemy | `text("WHERE name='" + name + "'")` | `text(":name")` + params |

```
┌──────────────────────────────────────────────────────────┐
│           ORM 인젝션 발생 경로                           │
├──────────────────────────────────────────────────────────┤
│  ORM 안전 경로: User.objects.filter(name=input)          │
│  → 자동 파라미터화 → SQL 인젝션 불가                    │
│                                                          │
│  ORM 취약 경로: User.objects.raw(f"WHERE name={input}")  │
│  → 직접 SQL 삽입 → SQL 인젝션 가능                      │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: ORM의 안전한 API는 마치 공항 출국장의 자동 검색대다. 그런데 검색대를 우회하는 VIP 통로(Raw 쿼리)를 아무나 사용하게 두면 의미가 없다.

---

## Ⅲ. 비교 및 연결

| 구분 | 일반 SQL 인젝션 | ORM 인젝션 |
|:---|:---|:---|
| 발생 조건 | 모든 SQL 직접 사용 환경 | ORM Raw 쿼리/문자열 연결 사용 시 |
| 위험도 | 동일 | 동일 |
| 탐지 | SAST로 탐지 가능 | ORM 전용 룰 필요 |
| 방어 | Prepared Statement | ORM 파라미터 바인딩 API |

📢 **섹션 요약 비유**: ORM을 쓴다고 자동으로 안전한 것이 아니라, ORM의 안전한 함수를 올바르게 쓸 때 안전해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**대응 전략**:
1. **ORM 기본 API 우선 사용**: filter(), get(), annotate() 등 ORM 내장 메서드 활용
2. **Raw 쿼리 사용 시 파라미터화 강제**: 코드 리뷰에서 Raw/execute 사용을 반드시 검토
3. **SAST 룰 추가**: 문자열 연결 HQL/JPQL 패턴 탐지 룰 설정
4. **최소 권한**: ORM이 사용하는 DB 계정에 최소 권한만 부여
5. **Lint 규칙**: ORM 안전 API 사용을 강제하는 커스텀 룰 추가

📢 **섹션 요약 비유**: ORM 코드 리뷰는 자동 검색대를 우회하는 통로가 생기지 않았는지 감시하는 것이다.

---

## Ⅴ. 기대효과 및 결론

ORM의 표준 API를 올바르게 사용하고 Raw 쿼리를 금지 또는 엄격히 통제하면 ORM Injection을 방어할 수 있다. 팀 전체에 "ORM = 자동 안전"이 아니라 "올바른 ORM 사용 = 안전"이라는 인식을 정착시키는 것이 중요하다.

📢 **섹션 요약 비유**: ORM은 안전한 칼을 제공하지만, 칼을 거꾸로 들면 여전히 다친다. 도구가 안전한 것이지 사용법이 안전한 것이 아니다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| HQL/JPQL | 공격 대상 | Hibernate/JPA 쿼리 언어 |
| Parameterized Binding | 방어 방법 | `:name` 바인딩 사용 |
| Raw Query | 취약 패턴 | ORM 우회 SQL 직접 실행 |
| SAST | 탐지 도구 | 취약 패턴 코드 레벨 분석 |
| Django filter() | 안전 API | 자동 이스케이프 제공 |

### 👶 어린이를 위한 3줄 비유 설명
- ORM은 위험한 SQL을 대신 써주는 안전한 번역기야.
- 근데 번역기를 안 쓰고 직접 위험한 SQL을 넣으면 번역기가 도와줄 수 없어.
- 그래서 ORM을 쓸 때도 항상 정해진 안전한 방법만 사용해야 해!
""")

w("434_nosql_injection.md", 434, "434. NoSQL Injection", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NoSQL Injection (NoSQL 인젝션)은 MongoDB, Redis, Elasticsearch 등 비관계형 DB (Database)에서 JSON (JavaScript Object Notation)/BSON 쿼리 구조나 쿼리 연산자를 악용해 인증 우회, 데이터 탈취를 유발하는 공격이다.
> 2. **가치**: "SQL을 안 쓰면 SQL 인젝션이 없다"는 잘못된 인식과 달리, MongoDB의 `$where`, `$regex`, `$gt` 연산자가 새로운 인젝션 공격 벡터가 된다.
> 3. **판단 포인트**: 쿼리 파라미터의 타입 검증(JSON 객체를 문자열로 강제), MongoDB 쿼리 연산자 화이트리스트, 최신 드라이버 사용이 핵심 방어책이다.

---

## Ⅰ. 개요 및 필요성

NoSQL 데이터베이스는 SQL을 사용하지 않지만, 사용자 입력을 쿼리에 직접 포함하면 동일한 인젝션 위험에 노출된다. 특히 MongoDB에서 HTTP 요청 바디의 JSON이 쿼리 객체로 직접 변환될 때 공격자가 쿼리 연산자(`$gt`, `$ne`, `$where`, `$regex`)를 주입할 수 있다.

**MongoDB 인젝션 예시**:
```javascript
// 취약한 로그인 코드 (Node.js)
db.users.find({ username: req.body.username, password: req.body.password })

// 공격 입력 (JSON): {"username": "admin", "password": {"$gt": ""}}
// 실행 쿼리: {username: "admin", password: {$gt: ""}}
// password 값이 빈 문자열보다 크면 → 모든 비밀번호 통과 → 인증 우회
```

이 공격은 비밀번호를 모르고도 `$gt`, `$ne`, `$regex` 등으로 조건을 항상 참으로 만들어 인증을 우회한다.

📢 **섹션 요약 비유**: SQL 인젝션이 레스토랑 주문서에 명령을 쓰는 것이라면, NoSQL 인젝션은 주문 앱의 JSON 필드에 "가격이 0보다 크면"이라는 조건을 몰래 삽입하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

MongoDB 주요 인젝션 연산자:

| 연산자 | 의미 | 공격 예시 |
|:---|:---|:---|
| `$gt` | 초과 | `{"password": {"$gt": ""}}` — 항상 참 |
| `$ne` | 불일치 | `{"username": {"$ne": null}}` — 모든 사용자 |
| `$where` | JS 표현식 | `{"$where": "sleep(5000)"}` — 시간 기반 공격 |
| `$regex` | 정규식 | `{"password": {"$regex": ".*"}}` — 항상 참 |

```
┌──────────────────────────────────────────────────────────┐
│           NoSQL 인젝션 공격 흐름                         │
├──────────────────────────────────────────────────────────┤
│  HTTP 요청:                                              │
│  POST /login                                             │
│  {"username":"admin", "password":{"$gt":""}}             │
│       │                                                  │
│       ▼                                                  │
│  MongoDB 쿼리: find({username:"admin",                   │
│                       password:{$gt:""}})                │
│       │                                                  │
│       ▼                                                  │
│  비밀번호 조건 항상 참 → 인증 우회 성공                  │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: NoSQL 인젝션은 "비밀번호가 뭐든 상관없이, 뭔가 있으면 통과"라는 새 규칙을 쿼리에 몰래 집어넣는 것이다.

---

## Ⅲ. 비교 및 연결

| 구분 | SQL 인젝션 | NoSQL 인젝션 |
|:---|:---|:---|
| 대상 | 관계형 DB | MongoDB, Redis 등 |
| 공격 문자 | `'`, `;`, `--` | `{$gt:`, `$where` 등 |
| 인증 우회 | `' OR 1=1--` | `{"password": {"$gt": ""}}` |
| 방어 | 파라미터화 쿼리 | 타입 검증, 연산자 화이트리스트 |

📢 **섹션 요약 비유**: SQL은 구두 주문을 조작하고, NoSQL은 앱 주문 양식의 필드 타입을 바꿔 시스템을 속인다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**대응 전략**:
1. **타입 강제 검증**: 비밀번호 필드는 반드시 string 타입만 허용, 객체 수신 시 거부
2. **쿼리 연산자 화이트리스트**: 허용되지 않은 MongoDB 연산자 포함 시 요청 거부
3. **`$where` 연산자 비활성화**: 서버에서 JavaScript 실행 기능 비활성화
4. **ODM (Object Document Mapping) 사용**: Mongoose 등으로 스키마 타입 강제
5. **최소 권한**: DB 계정에 애플리케이션에 필요한 최소 읽기/쓰기 권한만 부여

```javascript
// 안전한 코드: 타입 검증 추가
const username = String(req.body.username);
const password = String(req.body.password);
db.users.find({ username: username, password: password });
```

📢 **섹션 요약 비유**: 타입 검증은 "주문서에 음식 이름만 적을 수 있고, 코드나 명령은 적을 수 없다"는 규칙을 적용하는 것이다.

---

## Ⅴ. 기대효과 및 결론

타입 강제 검증과 ODM 스키마를 활용하면 NoSQL 인젝션을 구조적으로 방어할 수 있다. 특히 Express.js 환경에서 `express-validator`와 Mongoose를 조합하면 입력 타입 검증과 쿼리 안전성을 동시에 확보할 수 있다.

기술사 관점에서 NoSQL 인젝션은 데이터 타입 혼용이라는 JavaScript의 동적 타입 특성에서 비롯된다. 이를 인식하고 정적 타입 검사(TypeScript)와 입력 검증 라이브러리를 병행 사용하는 아키텍처가 필요하다.

📢 **섹션 요약 비유**: NoSQL 인젝션 방어는 주문 양식에서 "음식 이름" 칸에는 문자만, "수량" 칸에는 숫자만 입력받도록 강제하는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| $gt/$ne/$where | 공격 연산자 | MongoDB 쿼리 연산자 악용 |
| Mongoose ODM | 방어 도구 | 스키마 타입 강제 |
| Type Coercion | 취약 원인 | JavaScript 동적 타입 |
| Input Sanitization | 방어 방법 | 타입·형식 강제 검증 |
| SQL Injection | 유사 공격 | 관계형 DB 인젝션 |

### 👶 어린이를 위한 3줄 비유 설명
- NoSQL 인젝션은 SQL을 안 써도 비슷한 방식으로 DB를 속이는 공격이야.
- MongoDB 같은 DB는 JSON 형식으로 질문하는데, "비밀번호가 뭐든 상관없어"라는 조건을 몰래 넣을 수 있어.
- 그래서 사용자 입력이 항상 문자(string)인지 확인하고, 다른 타입이 들어오면 거부해야 해!
""")

w("435_os_command_injection.md", 435, "435. OS Command Injection", """
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OS Command Injection (OS 명령 인젝션)은 애플리케이션이 사용자 입력을 운영체제 셸 명령의 일부로 사용할 때, 공격자가 세미콜론(;), 파이프(|), 앰퍼샌드(&) 등으로 추가 명령을 삽입해 서버에서 임의 명령을 실행하는 취약점이다.
> 2. **가치**: SQL 인젝션이 DB 서버에 국한되는 것과 달리, OS Command Injection은 서버 전체를 장악할 수 있는 가장 위험한 인젝션 유형이며, 웹쉘 업로드, 원격 제어, 내부망 침투로 이어진다.
> 3. **판단 포인트**: 사용자 입력을 셸 명령에 직접 포함하는 코드 패턴 자체를 제거하고, 불가피하다면 셸 없는 API 호출(exec without shell), 화이트리스트 검증, 최소 권한을 병행해야 한다.

---

## Ⅰ. 개요 및 필요성

웹 애플리케이션이 ping, nslookup, convert 등의 OS 유틸리티를 호출하거나 파일을 처리하기 위해 셸 명령을 사용하는 경우가 있다. 이때 사용자 입력을 검증 없이 명령에 포함하면 공격자가 원하는 명령을 실행할 수 있다.

**취약 코드 예시 (Python)**:
```python
import os
hostname = request.args.get("host")
output = os.system("ping -c 1 " + hostname)
# 공격 입력: "8.8.8.8; cat /etc/passwd"
# 실행: ping -c 1 8.8.8.8; cat /etc/passwd
# → /etc/passwd 파일 내용 반환
```

셸 메타 문자를 활용한 명령 연결:
- `;` : 앞 명령 결과에 관계없이 뒤 명령 실행
- `|` : 앞 명령의 출력을 뒤 명령의 입력으로 연결
- `&&` : 앞 명령 성공 시 뒤 명령 실행
- `||` : 앞 명령 실패 시 뒤 명령 실행
- `` ` `` (백틱): 명령 치환

📢 **섹션 요약 비유**: OS Command Injection은 로봇에게 "사과 가져와"라고 말했더니, 누군가 "사과 가져와, 그리고 집도 폭파해"라고 바꿔 말하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 셸 메타 문자 | 동작 | 공격 예시 |
|:---|:---|:---|
| `;` | 명령 순차 실행 | `8.8.8.8; ls -la /` |
| `\|` | 파이프 연결 | `test \| cat /etc/passwd` |
| `&&` | 조건 실행 (앞 성공 시) | `ls && whoami` |
| `$()` | 명령 치환 | `$(whoami)` |
| `\`\`` | 명령 치환 (백틱) | `` `id` `` |

```
┌──────────────────────────────────────────────────────────┐
│           OS Command Injection 공격 흐름                 │
├──────────────────────────────────────────────────────────┤
│  정상: ping -c 1 8.8.8.8                                 │
│  공격: ping -c 1 8.8.8.8; id; cat /etc/shadow           │
│                                                          │
│  서버 실행:                                              │
│  1. ping -c 1 8.8.8.8 (정상)                             │
│  2. id (현재 사용자 정보 반환)                           │
│  3. cat /etc/shadow (비밀번호 해시 파일 반환)            │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: `;`는 "그리고"라는 의미다. "택배 가져와; 서재에 있는 서류도 모두 가져와"처럼 추가 명령을 덧붙인다.

---

## Ⅲ. 비교 및 연결

| 구분 | SQL 인젝션 | OS Command 인젝션 |
|:---|:---|:---|
| 영향 범위 | DB 수준 | 서버 OS 전체 |
| 위험도 | 상 | 최상 |
| 대표 피해 | 데이터 탈취 | 서버 장악, 내부망 침투 |
| 방어 | 파라미터화 쿼리 | 셸 없는 API, 화이트리스트 |

📢 **섹션 요약 비유**: SQL 인젝션이 창고 열쇠를 훔치는 것이라면, OS Command Injection은 건물 전체의 마스터키를 얻는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**대응 전략**:
1. **셸 없는 API 사용**: `subprocess.run(["ping", "-c", "1", host], shell=False)` — 셸을 거치지 않아 메타 문자 무효화
2. **화이트리스트 검증**: 호스트명은 `^[a-zA-Z0-9.-]+$` 패턴만 허용
3. **셸 API 사용 금지**: `os.system()`, `exec()`, `eval()`, PHP `shell_exec()` 사용 금지
4. **최소 권한**: 웹 서버 프로세스를 루트가 아닌 제한된 계정으로 실행
5. **컨테이너/샌드박스**: Docker 컨테이너로 실행 환경 격리

📢 **섹션 요약 비유**: `shell=False`로 명령을 분리하면 공격자가 ";", "|" 등을 넣어도 별도 명령이 아닌 그냥 문자로 취급된다.

---

## Ⅴ. 기대효과 및 결론

셸 없는 API 호출로 OS Command Injection을 구조적으로 방지할 수 있다. 불가피하게 셸을 사용해야 한다면 `shlex.quote()`로 이스케이프 처리하고, 입력 화이트리스트를 반드시 적용해야 한다. 컨테이너 격리는 공격 성공 시에도 피해 범위를 최소화하는 추가 보호 계층이다.

기술사 관점에서 OS Command Injection은 Capability Limitation(최소 기능 원칙)과 Privilege Separation(권한 분리) 두 원칙을 가장 강력하게 요구하는 취약점이다.

📢 **섹션 요약 비유**: 사용자가 입력한 명령을 직접 실행하지 않는 것은 손님이 직접 주방에 들어와 칼을 쓰지 못하게 하는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Shell Metacharacter | 공격 수단 | ;, |, &&, $() 등 |
| subprocess (shell=False) | 방어 방법 | 셸 없는 프로세스 실행 |
| Whitelist Validation | 방어 방법 | 허용 문자만 입력 허용 |
| Principle of Least Privilege | 설계 원칙 | 최소 권한 실행 |
| Container Isolation | 심층 방어 | 공격 영향 범위 제한 |

### 👶 어린이를 위한 3줄 비유 설명
- OS Command Injection은 로봇에게 심부름을 시키는데, 누군가 "그리고 금고도 가져와"라는 말을 몰래 추가하는 것이야.
- 서버가 이 명령을 다 실행하면 집 전체를 공격자가 통제할 수 있어.
- 그래서 사용자 입력을 절대 명령어로 실행하면 안 되고, 미리 정해진 안전한 방법만 써야 해!
""")

print("Batch 432-435 done.")
