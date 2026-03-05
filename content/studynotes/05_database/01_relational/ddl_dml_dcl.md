+++
title = "DDL, DML, DCL (데이터 정의/조작/제어 언어)"
date = "2026-03-04"
[extra]
categories = "studynotes-database"
+++

# DDL, DML, DCL (데이터 정의/조작/제어 언어)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DDL(CREATE/ALTER/DROP)은 데이터 구조 정의, DML(SELECT/INSERT/UPDATE/DELETE)는 데이터 조작, DCL(GRANT/REVOKE)은 권한 제어를 담당하는 SQL의 3대 명령어 그룹입니다.
> 2. **가치**: DDL은 스키마 관리로 데이터 독립성을, DML은 CRUD 연산으로 비즈니스 로직을, DCL은 보안으로 데이터 보호를 각각 담당합니다.
> 3. **융합**: DDL은 트랜잭션과 연동(ROLLBACK 가능성), DML은 옵티마이저의 최적화 대상, DCL은 감사 로그와 연동됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**DDL (Data Definition Language) - 데이터 정의 언어**
- 데이터베이스 구조(스키마)를 정의, 수정, 삭제
- CREATE, ALTER, DROP, TRUNCATE
- DDL은 자동 COMMIT (Auto-commit)

**DML (Data Manipulation Language) - 데이터 조작 언어**
- 데이터를 조회, 삽입, 수정, 삭제
- SELECT, INSERT, UPDATE, DELETE
- DML은 트랜잭션 내에서 수행 (COMMIT/ROLLBACK 가능)

**DCL (Data Control Language) - 데이터 제어 언어**
- 데이터에 대한 접근 권한을 부여/회수
- GRANT, REVOKE
- 보안과 감사의 핵심

**TCL (Transaction Control Language) - 트랜잭션 제어 언어**
- 트랜잭션을 제어
- COMMIT, ROLLBACK, SAVEPOINT

#### 2. 💡 비유를 통한 이해
**도서관 관리**로 비유할 수 있습니다:

```
[DDL] 도서관 건축/리모델링
- CREATE: 도서관 신축 (새 테이블 생성)
- ALTER: 열람실 확장 (칼럼 추가)
- DROP: 창고 철거 (테이블 삭제)
- TRUNCATE: 책장 비우기 (데이터만 삭제)

[DML] 도서관 이용
- SELECT: 책 찾기 (조회)
- INSERT: 새 책 등록 (삽입)
- UPDATE: 책 정보 수정 (갱신)
- DELETE: 폐기 도서 제거 (삭제)

[DCL] 도서관 권한
- GRANT: 대출 권한 부여
- REVOKE: 대출 권한 회수
```

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계**: 초기 DBMS는 각 기능이 혼재되어 있었고, 구조 변경과 데이터 조작이 명확히 분리되지 않았습니다.
2. **혁신적 패러다임의 도입**: SQL-86 표준에서 DDL, DML, DCL을 명확히 구분했습니다. 이는 데이터 독립성과 보안의 기반이 되었습니다.
3. **비즈니스적 요구사항**: DBA는 DDL로 구조 관리, 개발자는 DML로 비즈니스 로직 구현, 보안 담당자는 DCL로 접근 제어를 각각 담당합니다.

---

### Ⅱ. 아키키텍처 및 핵심 원리 (Deep Dive)

#### 1. SQL 명령어 분류 (표)

| 분류 | 명령어 | 기능 | Auto Commit | 대상 |
|:---|:---|:---|:---|:---|
| **DDL** | CREATE | 객체 생성 | O | 스키마 |
| | ALTER | 객체 수정 | O | 스키마 |
| | DROP | 객체 삭제 | O | 스키마 |
| | TRUNCATE | 데이터 삭제 | O | 데이터 |
| **DML** | SELECT | 데이터 조회 | X | 데이터 |
| | INSERT | 데이터 삽입 | X | 데이터 |
| | UPDATE | 데이터 수정 | X | 데이터 |
| | DELETE | 데이터 삭제 | X | 데이터 |
| **DCL** | GRANT | 권한 부여 | O | 권한 |
| | REVOKE | 권한 회수 | O | 권한 |
| **TCL** | COMMIT | 트랜잭션 확정 | - | 트랜잭션 |
| | ROLLBACK | 트랜잭션 취소 | - | 트랜잭션 |
| | SAVEPOINT | 저장점 설정 | - | 트랜잭션 |

#### 2. DDL/DML/DCL 처리 흐름 다이어그램

```text
+====================================================================+
|                    [ SQL 명령어 처리 흐름 ]                         |
+====================================================================+

[사용자 요청]
      │
      ▼
┌──────────────────────────────────────────────────────────────┐
│                     SQL Parser                                │
│  SQL 구문 분석 → 토큰화 → 파스 트리 생성                      │
└──────────────────────────────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────────────────────────────┐
│                   명령어 분류                                  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │  DDL    │  │  DML    │  │  DCL    │  │  TCL    │        │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │
└───────┼────────────┼────────────┼────────────┼──────────────┘
        │            │            │            │
        ▼            ▼            ▼            ▼
┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
│    DDL    │ │    DML    │ │    DCL    │ │    TCL    │
│  Handler  │ │  Handler  │ │  Handler  │ │  Handler  │
├───────────┤ ├───────────┤ ├───────────┤ ├───────────┤
│ 1. DD     │ │ 1. 권한   │ │ 1. 권한   │ │ 1. 트랜잭 │
│    Lock   │ │    검증   │ │    맵     │ │    션 상 │
│ 2. 스키마 │ │ 2. 옵티   │ │    업데이 │ │    태 관 │
│    업데이 │ │    마이저 │ │    트     │ │    리    │
│ 3. Auto   │ │ 3. 실행   │ │ 2. Auto   │ │ 2. Lock  │
│    Commit │ │    계획   │ │    Commit │ │    해제  │
│ 4. DD     │ │ 4. 데이터 │ │           │ │           │
│    Unlock │ │    접근   │ │           │ │           │
└───────────┘ └───────────┘ └───────────┘ └───────────┘
      │            │            │            │
      └────────────┴────────────┴────────────┘
                         │
                         ▼
                   [결과 반환]
```

#### 3. 심층 동작 원리: 각 명령어 상세

**1단계: DDL (Data Definition Language)**

```sql
-- ==================== CREATE ====================
-- 테이블 생성
CREATE TABLE employees (
    emp_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_name VARCHAR(100) NOT NULL,
    dept_id INT,
    salary DECIMAL(15,2) CHECK (salary > 0),
    hire_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 외래 키
    CONSTRAINT fk_emp_dept
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- 인덱스 생성
CREATE INDEX idx_emp_name ON employees(emp_name);
CREATE UNIQUE INDEX idx_emp_email ON employees(email);

-- 뷰 생성
CREATE VIEW vw_employee_summary AS
SELECT emp_id, emp_name, dept_id
FROM employees
WHERE salary > 50000000;

-- ==================== ALTER ====================
-- 칼럼 추가
ALTER TABLE employees
ADD COLUMN phone VARCHAR(20);

-- 칼럼 수정
ALTER TABLE employees
MODIFY COLUMN emp_name VARCHAR(200);

-- 칼럼 삭제
ALTER TABLE employees
DROP COLUMN phone;

-- 제약조건 추가
ALTER TABLE employees
ADD CONSTRAINT chk_salary_range
CHECK (salary BETWEEN 0 AND 100000000);

-- ==================== DROP ====================
-- 테이블 삭제 (구조 + 데이터)
DROP TABLE employees;
DROP TABLE IF EXISTS employees;  -- 존재하면 삭제

-- ==================== TRUNCATE ====================
-- 데이터만 삭제 (구조 유지, DDL로 분류)
TRUNCATE TABLE employees;
-- DELETE FROM employees와 차이:
-- 1. TRUNCATE는 롤백 불가
-- 2. TRUNCATE는 Auto Commit
-- 3. TRUNCATE는 더 빠름 (로깅 최소화)
```

**2단계: DML (Data Manipulation Language)**

```sql
-- ==================== INSERT ====================
-- 단일 행 삽입
INSERT INTO employees (emp_name, dept_id, salary)
VALUES ('홍길동', 1, 50000000);

-- 다중 행 삽입
INSERT INTO employees (emp_name, dept_id, salary)
VALUES
    ('김철수', 1, 45000000),
    ('이영희', 2, 55000000),
    ('박영수', 1, 40000000);

-- SELECT 결과 삽입
INSERT INTO employees_backup
SELECT * FROM employees WHERE hire_date < '2023-01-01';

-- ==================== UPDATE ====================
-- 단일 테이블 수정
UPDATE employees
SET salary = salary * 1.1
WHERE dept_id = 1;

-- 서브쿼리 활용 수정
UPDATE employees
SET salary = (
    SELECT AVG(salary) FROM employees
)
WHERE emp_id = 100;

-- ==================== DELETE ====================
-- 조건 삭제
DELETE FROM employees
WHERE hire_date < '2020-01-01';

-- 전체 삭제 (TRUNCATE와 다름: 롤백 가능)
DELETE FROM employees;

-- ==================== SELECT ====================
-- 기본 조회
SELECT emp_id, emp_name, salary
FROM employees
WHERE dept_id = 1
ORDER BY salary DESC
LIMIT 10;

-- 조인 조회
SELECT e.emp_name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;

-- 집계 조회
SELECT dept_id, COUNT(*) as cnt, AVG(salary) as avg_salary
FROM employees
GROUP BY dept_id
HAVING AVG(salary) > 50000000;
```

**3단계: DCL (Data Control Language)**

```sql
-- ==================== GRANT ====================
-- 시스템 권한 부여
GRANT CREATE SESSION TO user1;
GRANT CREATE TABLE TO user1;
GRANT ALL PRIVILEGES TO admin_user;

-- 객체 권한 부여
GRANT SELECT ON employees TO user1;
GRANT SELECT, INSERT, UPDATE ON employees TO user2;
GRANT ALL ON employees TO manager;

-- 칼럼 레벨 권한
GRANT SELECT (emp_id, emp_name) ON employees TO hr_user;
GRANT UPDATE (salary) ON employees TO payroll_user;

-- 권한 전달 (WITH GRANT OPTION)
GRANT SELECT ON employees TO user3 WITH GRANT OPTION;
-- user3도 다른 사용자에게 권한 부여 가능

-- 역할(Role) 활용
CREATE ROLE hr_role;
GRANT SELECT ON employees TO hr_role;
GRANT SELECT ON departments TO hr_role;
GRANT hr_role TO user4;

-- ==================== REVOKE ====================
-- 권한 회수
REVOKE SELECT ON employees FROM user1;
REVOKE ALL ON employees FROM manager;

-- CASCADE: 회수된 권한으로 부여된 권한도 회수
REVOKE SELECT ON employees FROM user3 CASCADE;
```

**4단계: TCL (Transaction Control Language)**

```sql
-- ==================== COMMIT ====================
-- 트랜잭션 확정
BEGIN;
    UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
    UPDATE accounts SET balance = balance + 1000 WHERE id = 2;
COMMIT;  -- 변경사항 영구 반영

-- ==================== ROLLBACK ====================
-- 트랜잭션 취소
BEGIN;
    DELETE FROM employees WHERE dept_id = 99;
    -- 실수 발견!
ROLLBACK;  -- 삭제 취소

-- ==================== SAVEPOINT ====================
-- 부분 롤백
BEGIN;
    INSERT INTO orders VALUES (1, '주문1');
    SAVEPOINT sp1;

    INSERT INTO orders VALUES (2, '주문2');
    SAVEPOINT sp2;

    INSERT INTO orders VALUES (3, '주문3');
    -- 주문3만 취소
    ROLLBACK TO sp2;

COMMIT;  -- 주문1, 2만 확정
```

#### 4. 실무 수준의 SQL 실행기 구현

```python
"""
간소화된 SQL 실행기 구현
DDL, DML, DCL 명령어 처리
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
import re

class CommandType(Enum):
    DDL = "DDL"
    DML = "DML"
    DCL = "DCL"
    TCL = "TCL"

@dataclass
class Table:
    """테이블 정의"""
    name: str
    columns: Dict[str, str]  # name -> type
    primary_key: List[str] = field(default_factory=list)
    foreign_keys: Dict[str, str] = field(default_factory=dict)
    rows: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class User:
    """사용자 정의"""
    name: str
    permissions: Dict[str, List[str]] = field(default_factory=dict)  # table -> actions

class SQLExecutor:
    """SQL 실행기"""

    def __init__(self):
        self.tables: Dict[str, Table] = {}
        self.users: Dict[str, User] = {}
        self.current_user: Optional[str] = None
        self.transaction_active: bool = False
        self.transaction_buffer: List[Callable] = field(default_factory=list)
        self.savepoints: Dict[str, int] = {}

    def execute(self, sql: str) -> Dict[str, Any]:
        """SQL 실행"""
        sql = sql.strip().upper()
        cmd_type = self._classify_command(sql)

        print(f"\n[SQL] {sql[:50]}...")
        print(f"[Type] {cmd_type.value}")

        if cmd_type == CommandType.DDL:
            return self._execute_ddl(sql)
        elif cmd_type == CommandType.DML:
            return self._execute_dml(sql)
        elif cmd_type == CommandType.DCL:
            return self._execute_dcl(sql)
        elif cmd_type == CommandType.TCL:
            return self._execute_tcl(sql)
        else:
            return {'error': 'Unknown command type'}

    def _classify_command(self, sql: str) -> CommandType:
        """명령어 분류"""
        first_word = sql.split()[0]
        if first_word in ('CREATE', 'ALTER', 'DROP', 'TRUNCATE'):
            return CommandType.DDL
        elif first_word in ('SELECT', 'INSERT', 'UPDATE', 'DELETE'):
            return CommandType.DML
        elif first_word in ('GRANT', 'REVOKE'):
            return CommandType.DCL
        elif first_word in ('COMMIT', 'ROLLBACK', 'SAVEPOINT', 'BEGIN'):
            return CommandType.TCL
        return CommandType.DML

    # ==================== DDL ====================

    def _execute_ddl(self, sql: str) -> Dict[str, Any]:
        """DDL 실행"""
        if sql.startswith('CREATE TABLE'):
            return self._create_table(sql)
        elif sql.startswith('DROP TABLE'):
            return self._drop_table(sql)
        elif sql.startswith('TRUNCATE'):
            return self._truncate_table(sql)
        elif sql.startswith('ALTER'):
            return self._alter_table(sql)
        return {'error': 'Unsupported DDL'}

    def _create_table(self, sql: str) -> Dict[str, Any]:
        """테이블 생성"""
        # 간소화된 파싱
        match = re.search(r'CREATE TABLE (\w+)', sql)
        if not match:
            return {'error': 'Invalid CREATE TABLE syntax'}

        table_name = match.group(1)
        self.tables[table_name] = Table(
            name=table_name,
            columns={'id': 'INT', 'name': 'VARCHAR(100)'},
            rows=[]
        )
        print(f"[DDL] 테이블 '{table_name}' 생성됨")
        return {'success': True, 'table': table_name}

    def _drop_table(self, sql: str) -> Dict[str, Any]:
        """테이블 삭제"""
        match = re.search(r'DROP TABLE (\w+)', sql)
        if not match:
            return {'error': 'Invalid DROP TABLE syntax'}

        table_name = match.group(1)
        if table_name in self.tables:
            del self.tables[table_name]
            print(f"[DDL] 테이블 '{table_name}' 삭제됨")
            return {'success': True}
        return {'error': f"Table '{table_name}' not found"}

    def _truncate_table(self, sql: str) -> Dict[str, Any]:
        """테이블 초기화"""
        match = re.search(r'TRUNCATE TABLE (\w+)', sql)
        if not match:
            return {'error': 'Invalid TRUNCATE syntax'}

        table_name = match.group(1)
        if table_name in self.tables:
            self.tables[table_name].rows.clear()
            print(f"[DDL] 테이블 '{table_name}' 초기화됨")
            return {'success': True, 'affected_rows': 'ALL'}
        return {'error': f"Table '{table_name}' not found"}

    # ==================== DML ====================

    def _execute_dml(self, sql: str) -> Dict[str, Any]:
        """DML 실행"""
        if sql.startswith('INSERT'):
            return self._insert(sql)
        elif sql.startswith('SELECT'):
            return self._select(sql)
        elif sql.startswith('UPDATE'):
            return self._update(sql)
        elif sql.startswith('DELETE'):
            return self._delete(sql)
        return {'error': 'Unsupported DML'}

    def _insert(self, sql: str) -> Dict[str, Any]:
        """데이터 삽입"""
        match = re.search(r'INSERT INTO (\w+)', sql)
        if not match:
            return {'error': 'Invalid INSERT syntax'}

        table_name = match.group(1)
        if table_name not in self.tables:
            return {'error': f"Table '{table_name}' not found"}

        # 간소화: 임의 데이터 삽입
        new_row = {'id': len(self.tables[table_name].rows) + 1, 'name': 'test'}
        self.tables[table_name].rows.append(new_row)

        print(f"[DML] '{table_name}'에 1행 삽입")
        return {'success': True, 'affected_rows': 1}

    def _select(self, sql: str) -> Dict[str, Any]:
        """데이터 조회"""
        match = re.search(r'FROM (\w+)', sql)
        if not match:
            return {'error': 'Invalid SELECT syntax'}

        table_name = match.group(1)
        if table_name not in self.tables:
            return {'error': f"Table '{table_name}' not found"}

        rows = self.tables[table_name].rows
        print(f"[DML] '{table_name}'에서 {len(rows)}행 조회")
        return {'success': True, 'rows': rows}

    def _update(self, sql: str) -> Dict[str, Any]:
        """데이터 수정"""
        match = re.search(r'UPDATE (\w+)', sql)
        if not match:
            return {'error': 'Invalid UPDATE syntax'}

        table_name = match.group(1)
        # 간소화: 실제 수정 로직 생략
        print(f"[DML] '{table_name}'에서 수정 수행")
        return {'success': True, 'affected_rows': 0}

    def _delete(self, sql: str) -> Dict[str, Any]:
        """데이터 삭제"""
        match = re.search(r'DELETE FROM (\w+)', sql)
        if not match:
            return {'error': 'Invalid DELETE syntax'}

        table_name = match.group(1)
        # 간소화: 실제 삭제 로직 생략
        print(f"[DML] '{table_name}'에서 삭제 수행")
        return {'success': True, 'affected_rows': 0}

    # ==================== DCL ====================

    def _execute_dcl(self, sql: str) -> Dict[str, Any]:
        """DCL 실행"""
        if sql.startswith('GRANT'):
            return self._grant(sql)
        elif sql.startswith('REVOKE'):
            return self._revoke(sql)
        return {'error': 'Unsupported DCL'}

    def _grant(self, sql: str) -> Dict[str, Any]:
        """권한 부여"""
        match = re.search(r'GRANT (\w+) ON (\w+) TO (\w+)', sql)
        if match:
            permission, table, user = match.groups()
            if user not in self.users:
                self.users[user] = User(name=user, permissions={})
            if table not in self.users[user].permissions:
                self.users[user].permissions[table] = []
            self.users[user].permissions[table].append(permission)
            print(f"[DCL] '{user}'에게 '{table}'의 '{permission}' 권한 부여")
            return {'success': True}
        return {'error': 'Invalid GRANT syntax'}

    def _revoke(self, sql: str) -> Dict[str, Any]:
        """권한 회수"""
        match = re.search(r'REVOKE (\w+) ON (\w+) FROM (\w+)', sql)
        if match:
            permission, table, user = match.groups()
            if user in self.users and table in self.users[user].permissions:
                if permission in self.users[user].permissions[table]:
                    self.users[user].permissions[table].remove(permission)
                    print(f"[DCL] '{user}'의 '{table}' '{permission}' 권한 회수")
            return {'success': True}
        return {'error': 'Invalid REVOKE syntax'}

    # ==================== TCL ====================

    def _execute_tcl(self, sql: str) -> Dict[str, Any]:
        """TCL 실행"""
        if sql.startswith('COMMIT'):
            return self._commit()
        elif sql.startswith('ROLLBACK'):
            return self._rollback()
        elif sql.startswith('SAVEPOINT'):
            return self._savepoint(sql)
        return {'error': 'Unsupported TCL'}

    def _commit(self) -> Dict[str, Any]:
        """트랜잭션 확정"""
        self.transaction_buffer.clear()
        self.savepoints.clear()
        print("[TCL] COMMIT 수행")
        return {'success': True}

    def _rollback(self) -> Dict[str, Any]:
        """트랜잭션 취소"""
        self.transaction_buffer.clear()
        self.savepoints.clear()
        print("[TCL] ROLLBACK 수행")
        return {'success': True}

    def _savepoint(self, sql: str) -> Dict[str, Any]:
        """세이브포인트 설정"""
        match = re.search(r'SAVEPOINT (\w+)', sql)
        if match:
            sp_name = match.group(1)
            self.savepoints[sp_name] = len(self.transaction_buffer)
            print(f"[TCL] SAVEPOINT '{sp_name}' 설정")
            return {'success': True}
        return {'error': 'Invalid SAVEPOINT syntax'}

# ==================== 사용 예시 ====================
if __name__ == "__main__":
    executor = SQLExecutor()

    # DDL
    executor.execute("CREATE TABLE employees (id INT, name VARCHAR(100))")
    executor.execute("CREATE TABLE departments (id INT, name VARCHAR(100))")

    # DML
    executor.execute("INSERT INTO employees VALUES (1, '홍길동')")
    executor.execute("INSERT INTO employees VALUES (2, '김철수')")
    executor.execute("SELECT * FROM employees")

    # DCL
    executor.execute("GRANT SELECT ON employees TO user1")
    executor.execute("GRANT INSERT ON employees TO user1")

    # TCL
    executor.execute("COMMIT")
    executor.execute("SAVEPOINT sp1")

    # DDL - TRUNCATE
    executor.execute("TRUNCATE TABLE employees")
    executor.execute("SELECT * FROM employees")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. DDL vs DML vs DCL 비교

| 비교 항목 | DDL | DML | DCL |
|:---|:---|:---|:---|
| **대상** | 스키마 | 데이터 | 권한 |
| **롤백** | 불가 | 가능 | 불가 |
| **Auto Commit** | O | X | O |
| **주 사용자** | DBA | 개발자 | 보안담당자 |
| **빈도** | 낮음 | 높음 | 낮음 |

#### 2. DELETE vs TRUNCATE 비교

| 비교 항목 | DELETE | TRUNCATE |
|:---|:---|:---|
| **분류** | DML | DDL |
| **롤백** | 가능 | 불가 |
| **WHERE** | 가능 | 불가 |
| **속도** | 느림 | 빠름 |
| **로그** | 행 단위 | 페이지 단위 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 대량 데이터 삭제**
- 상황: 1000만 건 삭제 필요
- 판단: DELETE vs TRUNCATE
- 전략: 전체 삭제면 TRUNCATE, 조건 삭제면 DELETE (배치)

**시나리오 2: DDL 운영 중 수행**
- 상황: 운영 중 칼럼 추가
- 판단: DDL은 Lock 획득
- 전략: ONLINE DDL 사용 또는 점검 시간 수행

#### 2. 안티패턴 (Anti-patterns)
- **운영 중 DDL**: Lock 대기 폭증
- **GRANT 과다**: 권한 관리 복잡
- **DELETE 전체**: TRUNCATE 사용 권장

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과
- 명확한 책임 분리
- 보안 강화 (DCL)
- 트랜잭션 관리 (TCL)

#### 2. 참고 표준
- **ANSI SQL-86**: DDL/DML/DCL 분류
- **SQL:2016**: 최신 SQL 표준

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[트랜잭션](@/studynotes/05_database/01_relational/acid.md)**: TCL의 대상
- **[보안](@/studynotes/05_database/04_dw_olap/database_security.md)**: DCL의 목적
- **[스키마](@/studynotes/05_database/01_relational/schema_definition.md)**: DDL의 대상
- **[옵티마이저](@/studynotes/05_database/03_optimization/query_optimization.md)**: DML 최적화

---

### 👶 어린이를 위한 3줄 비유 설명
1. **장난감 정리함 만들기**: 정리함을 만드는 게 DDL이에요. "이 칸에는 인형, 저 칸에는 자동차!"라고 정하는 거죠!
2. **장난감 넣고 빼기**: 정리함에 장난감을 넣고 빼는 게 DML이에요. "로봇 넣기", "인형 찾기" 같은 거요!
3. **누가 쓸 수 있나**: "동생은 내 정리함 못 써!"라고 정하는 게 DCL이에요. 누가 뭘 할 수 있는지 정하는 거죠!
