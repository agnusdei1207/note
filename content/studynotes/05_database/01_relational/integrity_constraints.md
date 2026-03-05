+++
title = "무결성 제약조건 (Integrity Constraints)"
date = "2026-03-04"
[extra]
categories = "studynotes-database"
+++

# 무결성 제약조건 (Integrity Constraints)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 무결성 제약조건은 데이터베이스의 정확성, 일관성, 신뢰성을 보장하기 위해 DBMS가 강제하는 규칙으로, 개체 무결성, 참조 무결성, 도메인 무결성, 사용자 정의 무결성이 있습니다.
> 2. **가치**: 무결성 제약조건은 데이터 오류를 99% 방지하고, 애플리케이션 검증 로직을 50% 감소시키며, 비즈니스 규칙을 DB 레벨에서 일관되게 적용합니다.
> 3. **융합**: 무결성 제약조건은 트랜잭션 ACID의 일관성(Consistency)을 보장하는 핵심 메커니즘으로, SQL DDL의 CONSTRAINT 문으로 정의됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**무결성 제약조건(Integrity Constraints)**은 데이터베이스에 저장된 데이터가 정확하고 일관되며 신뢰할 수 있도록 보장하는 규칙들입니다. DBMS는 이 규칙들을 위반하는 연산을 거부함으로써 데이터 무결성을 보장합니다.

**무결성의 4가지 종류**:

1. **개체 무결성(Entity Integrity)**
   - 기본 키는 NULL이거나 중복될 수 없음
   - 각 튜플을 유일하게 식별 가능하게 보장

2. **참조 무결성(Referential Integrity)**
   - 외래 키는 참조하는 기본 키 값이거나 NULL이어야 함
   - 관련 테이블 간 일관성 보장

3. **도메인 무결성(Domain Integrity)**
   - 속성 값은 정의된 도메인(데이터 타입, 범위)에 속해야 함
   - NOT NULL, CHECK, DEFAULT 등으로 구현

4. **사용자 정의 무결성(User-defined Integrity)**
   - 비즈니스 규칙에 따른 제약조건
   - Trigger, Stored Procedure로 구현

#### 2. 💡 비유를 통한 이해
**은행 계좌 시스템**으로 비유할 수 있습니다:

```
[개체 무결성] 계좌번호
- 모든 계좌는 고유한 번호를 가져야 함
- 계좌번호가 없는 계좌는 있을 수 없음

[참조 무결성] 고객-계좌 관계
- 계좌는 반드시 존재하는 고객에게만 개설 가능
- 없는 고객의 계좌는 있을 수 없음

[도메인 무결성] 잔액
- 잔액은 숫자여야 함
- 잔액은 0 이상이어야 함 (마이너스 불가)

[사용자 정의] 1일 이체 한도
- 하루에 100만 원 이상 이체 불가
- 비즈니스 규칙에 따른 제약
```

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계**: 파일 시스템에서는 데이터 검증을 애플리케이션에서만 수행했고, 여러 앱에서 같은 데이터를 수정할 때 일관성이 깨지는 문제가 발생했습니다.
2. **혁신적 패러다임의 도입**: E.F. Codd가 관계형 모델에서 무결성 제약조건을 DBMS가 관리하도록 제안했습니다. 이는 데이터 품질을 DBMS가 보장하는 혁신이었습니다.
3. **비즈니스적 요구사항**: 금융, 의료, 항공 등 데이터 정확성이 중요한 분야에서 무결성은 선택이 아닌 필수 요건입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 무결성 제약조건 종류 (표)

| 종류 | 대상 | 제약 내용 | DDL 키워드 | 예시 |
|:---|:---|:---|:---|:---|
| **개체 무결성** | 기본 키 | NOT NULL, UNIQUE | PRIMARY KEY | 학번 |
| **참조 무결성** | 외래 키 | 참조 값 존재 | FOREIGN KEY | 학과코드 |
| **도메인 무결성** | 속성 | 타입, 범위, NULL | NOT NULL, CHECK | 학년(1-4) |
| **키 무결성** | 후보 키 | UNIQUE | UNIQUE | 이메일 |
| **NULL 무결성** | 속성 | NULL 불가 | NOT NULL | 이름 |
| **사용자 정의** | 테이블 | 비즈니스 규칙 | TRIGGER | 1일 한도 |

#### 2. 무결성 제약조건 처리 흐름 다이어그램

```text
+====================================================================+
|                    [ 무결성 제약조건 처리 흐름 ]                    |
+====================================================================+

[INSERT/UPDATE 요청]
        │
        ▼
┌───────────────────┐
│  1. 개체 무결성    │ ← PK가 NULL인가? PK가 중복인가?
│  검증             │
└─────────┬─────────┘
          │ 통과
          ▼
┌───────────────────┐
│  2. 참조 무결성    │ ← FK가 참조하는 PK가 존재하는가?
│  검증             │
└─────────┬─────────┘
          │ 통과
          ▼
┌───────────────────┐
│  3. 도메인 무결성  │ ← 데이터 타입이 맞는가? CHECK 조건 만족?
│  검증             │   NOT NULL 조건 만족?
└─────────┬─────────┘
          │ 통과
          ▼
┌───────────────────┐
│  4. 사용자 정의    │ ← Trigger 실행, 비즈니스 규칙 검증
│  무결성 검증      │
└─────────┬─────────┘
          │ 통과
          ▼
    [연산 수행 완료]

[DELETE 요청]
        │
        ▼
┌───────────────────┐
│  참조 무결성 검증  │ ← 삭제할 데이터를 참조하는 데이터가 있는가?
│  (ON DELETE 옵션) │   RESTRICT: 거부
└─────────┬─────────┘   CASCADE: 연쇄 삭제
          │             SET NULL: NULL로 설정
          ▼
    [연산 수행/거부]
```

#### 3. 심층 동작 원리: 각 제약조건 구현

**1단계: 개체 무결성 (Entity Integrity)**

```sql
-- 기본 키로 개체 무결성 보장
CREATE TABLE students (
    student_id VARCHAR(10) PRIMARY KEY,  -- NOT NULL + UNIQUE 자동 적용
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100)
);

-- 복합 기본 키
CREATE TABLE enrollments (
    student_id VARCHAR(10),
    course_id VARCHAR(10),
    grade CHAR(2),
    PRIMARY KEY (student_id, course_id)  -- 복합 PK
);

-- 제약조건 위반 테스트
INSERT INTO students (student_id, name) VALUES (NULL, '홍길동');
-- ERROR: Column 'student_id' cannot be null

INSERT INTO students (student_id, name) VALUES ('001', '홍길동');
INSERT INTO students (student_id, name) VALUES ('001', '김철수');
-- ERROR: Duplicate entry '001' for key 'PRIMARY'
```

**2단계: 참조 무결성 (Referential Integrity)**

```sql
-- 외래 키로 참조 무결성 보장
CREATE TABLE departments (
    dept_id VARCHAR(5) PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL
);

CREATE TABLE students (
    student_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    dept_id VARCHAR(5),

    CONSTRAINT fk_student_dept
    FOREIGN KEY (dept_id)
    REFERENCES departments(dept_id)
    ON DELETE RESTRICT    -- 참조 시 삭제 불가
    ON UPDATE CASCADE     -- PK 변경 시 FK도 변경
);

-- 제약조건 위반 테스트
INSERT INTO students (student_id, name, dept_id) VALUES ('001', '홍길동', 'D99');
-- ERROR: Cannot add or update a child row: a foreign key constraint fails
-- (dept_id 'D99'가 departments에 없음)

DELETE FROM departments WHERE dept_id = 'D01';
-- ERROR: Cannot delete or update a parent row: a foreign key constraint fails
-- (students에서 참조 중)
```

**3단계: 도메인 무결성 (Domain Integrity)**

```sql
-- 도메인 무결성 구현
CREATE TABLE students (
    student_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,                    -- NULL 불가
    email VARCHAR(100) UNIQUE,                    -- 유일해야 함
    year INT DEFAULT 1 CHECK (year BETWEEN 1 AND 4),  -- 1~4만 허용
    phone VARCHAR(20) CHECK (phone LIKE '010-%'),      -- 010으로 시작
    status ENUM('재학', '휴학', '졸업', '제적') DEFAULT '재학',

    -- 복합 CHECK 제약조건
    CONSTRAINT chk_email_format CHECK (
        email IS NULL OR email LIKE '%@%.%'
    )
);

-- 제약조건 위반 테스트
INSERT INTO students (student_id, name, year) VALUES ('001', NULL, 1);
-- ERROR: Column 'name' cannot be null

INSERT INTO students (student_id, name, year) VALUES ('001', '홍길동', 5);
-- ERROR: Check constraint 'students_chk_1' is violated.

INSERT INTO students (student_id, name, phone) VALUES ('001', '홍길동', '011-1234');
-- ERROR: Check constraint 'students_chk_2' is violated.
```

**4단계: 사용자 정의 무결성 (User-defined Integrity)**

```sql
-- Trigger로 비즈니스 규칙 구현
DELIMITER //

CREATE TRIGGER trg_check_daily_limit
BEFORE INSERT ON transfers
FOR EACH ROW
BEGIN
    DECLARE daily_total DECIMAL(15,2);

    -- 당일 이체 총액 계산
    SELECT IFNULL(SUM(amount), 0) INTO daily_total
    FROM transfers
    WHERE account_id = NEW.account_id
    AND transfer_date = CURDATE();

    -- 1일 한도 100만 원 초과 시 에러
    IF daily_total + NEW.amount > 1000000 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '일일 이체 한도 초과 (100만 원)';
    END IF;
END //

DELIMITER ;

-- Stored Procedure로 비즈니스 규칙 구현
DELIMITER //

CREATE PROCEDURE sp_withdraw(
    IN p_account_id VARCHAR(20),
    IN p_amount DECIMAL(15,2)
)
BEGIN
    DECLARE v_balance DECIMAL(15,2);

    -- 잔액 조회
    SELECT balance INTO v_balance
    FROM accounts
    WHERE account_id = p_account_id;

    -- 잔액 부족 시 에러
    IF v_balance < p_amount THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '잔액 부족';
    END IF;

    -- 출금 처리
    UPDATE accounts
    SET balance = balance - p_amount
    WHERE account_id = p_account_id;

    COMMIT;
END //

DELIMITER ;
```

#### 4. 실무 수준의 무결성 검증 시스템

```python
"""
무결성 제약조건 검증 시스템 구현
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable, Tuple
from enum import Enum

class ConstraintType(Enum):
    PRIMARY_KEY = "PRIMARY_KEY"
    FOREIGN_KEY = "FOREIGN_KEY"
    UNIQUE = "UNIQUE"
    NOT_NULL = "NOT_NULL"
    CHECK = "CHECK"

@dataclass
class Constraint:
    """제약조건 정의"""
    name: str
    constraint_type: ConstraintType
    columns: List[str]
    check_expression: Optional[Callable] = None
    reference_table: Optional[str] = None
    reference_columns: Optional[List[str]] = None
    on_delete: str = "RESTRICT"
    on_update: str = "CASCADE"

@dataclass
class ValidationResult:
    """검증 결과"""
    is_valid: bool
    constraint_name: str
    message: str

class IntegrityConstraintManager:
    """무결성 제약조건 관리자"""

    def __init__(self):
        self.constraints: Dict[str, List[Constraint]] = {}  # table -> constraints
        self.tables: Dict[str, List[Dict]] = {}  # table -> rows
        self.primary_keys: Dict[str, List[str]] = {}  # table -> pk columns

    def add_table(self, table_name: str, pk_columns: List[str]) -> None:
        """테이블 추가"""
        self.tables[table_name] = []
        self.primary_keys[table_name] = pk_columns
        self.constraints[table_name] = []
        print(f"[Table] {table_name} 추가 (PK: {pk_columns})")

    def add_constraint(self, table_name: str, constraint: Constraint) -> None:
        """제약조건 추가"""
        if table_name not in self.constraints:
            raise ValueError(f"테이블 '{table_name}' 없음")
        self.constraints[table_name].append(constraint)
        print(f"[Constraint] {table_name}.{constraint.name} 추가")

    def insert(self, table_name: str, row: Dict[str, Any]) -> ValidationResult:
        """행 삽입 (모든 제약조건 검증)"""
        if table_name not in self.tables:
            return ValidationResult(False, "TABLE", f"테이블 '{table_name}' 없음")

        # 모든 제약조건 검증
        for constraint in self.constraints[table_name]:
            result = self._validate_constraint(table_name, constraint, row, "INSERT")
            if not result.is_valid:
                return result

        # 삽입 실행
        self.tables[table_name].append(row)
        print(f"[INSERT] {table_name}: {row}")
        return ValidationResult(True, "SUCCESS", "삽입 성공")

    def update(self, table_name: str, row: Dict[str, Any],
              condition: Dict[str, Any]) -> Tuple[int, List[ValidationResult]]:
        """행 수정"""
        results = []
        updated = 0

        for existing_row in self.tables[table_name]:
            if all(existing_row.get(k) == v for k, v in condition.items()):
                # 수정 후 데이터로 제약조건 검증
                new_row = {**existing_row, **row}
                for constraint in self.constraints[table_name]:
                    result = self._validate_constraint(
                        table_name, constraint, new_row, "UPDATE", existing_row
                    )
                    if not result.is_valid:
                        results.append(result)
                        return (0, results)

                existing_row.update(row)
                updated += 1

        return (updated, [ValidationResult(True, "SUCCESS", f"{updated}행 수정")])

    def delete(self, table_name: str,
              condition: Dict[str, Any]) -> Tuple[int, List[ValidationResult]]:
        """행 삭제 (참조 무결성 확인)"""
        results = []
        rows_to_delete = [
            r for r in self.tables[table_name]
            if all(r.get(k) == v for k, v in condition.items())
        ]

        if not rows_to_delete:
            return (0, [ValidationResult(True, "SUCCESS", "삭제할 행 없음")])

        # 이 테이블을 참조하는 FK 검사
        for constraint in self._get_referencing_constraints(table_name):
            for row in rows_to_delete:
                pk_values = [row.get(col) for col in self.primary_keys[table_name]]
                ref_result = self._check_reference_on_delete(
                    constraint, pk_values
                )
                if not ref_result.is_valid:
                    results.append(ref_result)
                    return (0, results)

        # 삭제 실행
        self.tables[table_name] = [
            r for r in self.tables[table_name]
            if not all(r.get(k) == v for k, v in condition.items())
        ]

        return (len(rows_to_delete),
               [ValidationResult(True, "SUCCESS", f"{len(rows_to_delete)}행 삭제")])

    def _validate_constraint(self, table_name: str, constraint: Constraint,
                            row: Dict[str, Any], operation: str,
                            old_row: Dict = None) -> ValidationResult:
        """개별 제약조건 검증"""

        if constraint.constraint_type == ConstraintType.PRIMARY_KEY:
            return self._check_primary_key(table_name, constraint, row, operation)

        elif constraint.constraint_type == ConstraintType.FOREIGN_KEY:
            return self._check_foreign_key(constraint, row)

        elif constraint.constraint_type == ConstraintType.UNIQUE:
            return self._check_unique(table_name, constraint, row)

        elif constraint.constraint_type == ConstraintType.NOT_NULL:
            return self._check_not_null(constraint, row)

        elif constraint.constraint_type == ConstraintType.CHECK:
            return self._check_constraint(constraint, row)

        return ValidationResult(True, constraint.name, "검증 통과")

    def _check_primary_key(self, table_name: str, constraint: Constraint,
                          row: Dict[str, Any], operation: str) -> ValidationResult:
        """기본키 제약 검증"""
        pk_values = [row.get(col) for col in constraint.columns]

        # NULL 검사
        if None in pk_values:
            return ValidationResult(
                False, constraint.name,
                f"기본키 {constraint.columns}은 NULL 불가"
            )

        # 중복 검사
        for existing in self.tables[table_name]:
            if operation == "UPDATE" and existing == row:
                continue  # 자신은 제외
            existing_pk = [existing.get(col) for col in constraint.columns]
            if existing_pk == pk_values:
                return ValidationResult(
                    False, constraint.name,
                    f"기본키 {pk_values} 중복"
                )

        return ValidationResult(True, constraint.name, "기본키 검증 통과")

    def _check_foreign_key(self, constraint: Constraint,
                          row: Dict[str, Any]) -> ValidationResult:
        """외래키 제약 검증"""
        fk_values = [row.get(col) for col in constraint.columns]

        # NULL이면 통과
        if all(v is None for v in fk_values):
            return ValidationResult(True, constraint.name, "FK NULL 허용")

        # 참조 테이블 확인
        ref_table = self.tables.get(constraint.reference_table)
        if not ref_table:
            return ValidationResult(
                False, constraint.name,
                f"참조 테이블 '{constraint.reference_table}' 없음"
            )

        # 참조 값 존재 확인
        for ref_row in ref_table:
            ref_values = [ref_row.get(col) for col in constraint.reference_columns]
            if fk_values == ref_values:
                return ValidationResult(True, constraint.name, "FK 검증 통과")

        return ValidationResult(
            False, constraint.name,
            f"참조 무결성 위반: {fk_values}이 '{constraint.reference_table}'에 없음"
        )

    def _check_unique(self, table_name: str, constraint: Constraint,
                     row: Dict[str, Any]) -> ValidationResult:
        """유니크 제약 검증"""
        values = [row.get(col) for col in constraint.columns]

        for existing in self.tables[table_name]:
            existing_values = [existing.get(col) for col in constraint.columns]
            if existing_values == values:
                return ValidationResult(
                    False, constraint.name,
                    f"유니크 제약 위반: {values} 중복"
                )

        return ValidationResult(True, constraint.name, "유니크 검증 통과")

    def _check_not_null(self, constraint: Constraint,
                       row: Dict[str, Any]) -> ValidationResult:
        """NOT NULL 제약 검증"""
        for col in constraint.columns:
            if row.get(col) is None:
                return ValidationResult(
                    False, constraint.name,
                    f"'{col}'은 NULL 불가"
                )
        return ValidationResult(True, constraint.name, "NOT NULL 검증 통과")

    def _check_constraint(self, constraint: Constraint,
                         row: Dict[str, Any]) -> ValidationResult:
        """CHECK 제약 검증"""
        if constraint.check_expression:
            try:
                if not constraint.check_expression(row):
                    return ValidationResult(
                        False, constraint.name,
                        f"CHECK 제약 위반"
                    )
            except Exception as e:
                return ValidationResult(False, constraint.name, str(e))

        return ValidationResult(True, constraint.name, "CHECK 검증 통과")

    def _get_referencing_constraints(self, table_name: str) -> List[Constraint]:
        """이 테이블을 참조하는 FK 목록"""
        referencing = []
        for t_name, constraints in self.constraints.items():
            for c in constraints:
                if (c.constraint_type == ConstraintType.FOREIGN_KEY and
                    c.reference_table == table_name):
                    referencing.append(c)
        return referencing

    def _check_reference_on_delete(self, constraint: Constraint,
                                   pk_values: List[Any]) -> ValidationResult:
        """삭제 시 참조 무결성 확인"""
        child_table = self.tables.get(constraint.reference_table, [])
        if constraint.on_delete == "RESTRICT":
            # 자식 테이블에서 참조 확인
            for row in self.tables.get(constraint.columns[0].split('.')[0], []):
                fk_values = [row.get(col) for col in constraint.columns]
                if fk_values == pk_values:
                    return ValidationResult(
                        False, constraint.name,
                        f"참조 무결성: 삭제 불가 (참조하는 데이터 존재)"
                    )
        return ValidationResult(True, constraint.name, "삭제 가능")

# ==================== 사용 예시 ====================
if __name__ == "__main__":
    manager = IntegrityConstraintManager()

    # 1. 테이블 정의
    manager.add_table("departments", ["dept_id"])
    manager.add_table("students", ["student_id"])

    # 2. 부서 제약조건
    manager.add_constraint("departments", Constraint(
        name="pk_dept",
        constraint_type=ConstraintType.PRIMARY_KEY,
        columns=["dept_id"]
    ))

    # 3. 학생 제약조건
    manager.add_constraint("students", Constraint(
        name="pk_student",
        constraint_type=ConstraintType.PRIMARY_KEY,
        columns=["student_id"]
    ))

    manager.add_constraint("students", Constraint(
        name="fk_student_dept",
        constraint_type=ConstraintType.FOREIGN_KEY,
        columns=["dept_id"],
        reference_table="departments",
        reference_columns=["dept_id"]
    ))

    manager.add_constraint("students", Constraint(
        name="chk_year",
        constraint_type=ConstraintType.CHECK,
        columns=["year"],
        check_expression=lambda r: 1 <= r.get("year", 1) <= 4
    ))

    manager.add_constraint("students", Constraint(
        name="nn_name",
        constraint_type=ConstraintType.NOT_NULL,
        columns=["name"]
    ))

    # 4. 데이터 삽입 테스트
    print("\n=== 정상 데이터 ===")
    manager.insert("departments", {"dept_id": "D01", "dept_name": "컴공"})

    result = manager.insert("students", {
        "student_id": "001",
        "name": "홍길동",
        "dept_id": "D01",
        "year": 3
    })
    print(f"결과: {result.message}")

    print("\n=== FK 위반 ===")
    result = manager.insert("students", {
        "student_id": "002",
        "name": "김철수",
        "dept_id": "D99",  # 없는 부서
        "year": 2
    })
    print(f"결과: {result.message}")

    print("\n=== CHECK 위반 ===")
    result = manager.insert("students", {
        "student_id": "003",
        "name": "이영희",
        "dept_id": "D01",
        "year": 5  # 범위 초과
    })
    print(f"결과: {result.message}")

    print("\n=== NOT NULL 위반 ===")
    result = manager.insert("students", {
        "student_id": "004",
        "name": None,  # NULL
        "dept_id": "D01",
        "year": 1
    })
    print(f"결과: {result.message}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 무결성 제약조건 계층 구조

```
무결성 제약조건
├── 선언적 제약 (DDL)
│   ├── 개체 무결성 (PRIMARY KEY)
│   ├── 참조 무결성 (FOREIGN KEY)
│   ├── 도메인 무결성 (NOT NULL, CHECK, DEFAULT)
│   └── 키 무결성 (UNIQUE)
│
└── 절차적 제약 (프로그래밍)
    ├── Trigger
    └── Stored Procedure
```

#### 2. 제약조건 검증 시점

| 시점 | 검증 내용 | 오버헤드 |
|:---|:---|:---|
| **Statement** | 각 SQL 문장 실행 시 | 낮음 |
| **Row** | 각 행 처리 시 | 중간 |
| **Transaction** | 트랜잭션 커밋 시 | 낮음 (지연 검증) |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 대량 데이터 적재**
- 상황: 100만 건 데이터 일괄 INSERT
- 판단: 제약조건 검증으로 성능 저하
- 전략: 제약조건 일시 비활성화 → 적재 → 재활성화

**시나리오 2: FK 없이 설계**
- 상황: 성능 이유로 FK 제거 요청
- 판단: 무결성은 앱에서 보장? → 위험
- 전략: FK 유지, 인덱스 최적화로 성능 개선

#### 2. 안티패턴 (Anti-patterns)
- **제약조건 없는 설계**: 무결성 보장 불가
- **과도한 Trigger**: 성능 저하, 디버깅 어려움
- **앱에서만 검증**: 일관성 보장 불가

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과
- 데이터 오류 99% 방지
- 앱 검증 로직 50% 감소
- 일관성 자동 보장

#### 2. 참고 표준
- **ANSI SQL**: CONSTRAINT 문법
- **Codd 12규칙**: 무결성 독립성

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[기본 키](@/studynotes/05_database/01_relational/primary_key.md)**: 개체 무결성
- **[외래 키](@/studynotes/05_database/01_relational/foreign_key.md)**: 참조 무결성
- **[트랜잭션 ACID](@/studynotes/05_database/01_relational/acid.md)**: 일관성 보장
- **[트리거](@/studynotes/05_database/03_optimization/trigger.md)**: 사용자 정의 무결성

---

### 👶 어린이를 위한 3줄 비유 설명
1. **학교 규칙**: 학교에는 꼭 지켜야 할 규칙이 있어요. "지각 금지", "복장 규정" 같은 거요. 이게 무결성 제약조건이에요!
2. **전화번호 검사**: 친구 전화번호를 적을 때 010으로 시작하는지, 숫자가 맞는지 확인하는 게 도메인 무결성이에요!
3. **가족 관계**: 가족에게는 아빠, 엄마가 필수예요. "아빠 없는 아이는 없다"가 개체 무결성, "진짜 아빠만 아빠라고 부른다"가 참조 무결성이에요!
