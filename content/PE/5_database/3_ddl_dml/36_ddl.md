+++
title = "36. DDL (Data Definition Language) - 데이터 정의 언어"
date = 2026-03-06
categories = ["studynotes-database"]
tags = ["DDL", "Data-Definition", "SQL", "Schema", "Database-Objects"]
draft = false
+++

# DDL (Data Definition Language) - 데이터 정의 언어

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DDL은 **"데이터베이스 **구조를 **정의**하고 **관리**하는 **언어\\\"**로, **CREATE**(생성), **ALTER**(변경), **DROP**(삭제), **TRUNCATE**(잘라내기) **명령어**가 **있고 **데이터**가 **아니라 **구조를 **다룬다**.
> 2. **객체**: **TABLE**(테이블), **INDEX**(인덱스), **VIEW**(뷰), **SEQUENCE**(시퀀스), **TRIGGER**(트리거), **PROCEDURE**(저장 프로시저) 등을 **정의**하며 **제약조건**(Constraint)으로 **무결성성**을 **보장**한다.
> 3. **제약조건**: **PRIMARY KEY**(기본키), **FOREIGN KEY**(외래키), **UNIQUE**(유일), **NOT NULL**(비null), **CHECK**(체크), **DEFAULT**(기본값)이 **있고 **CASCADE** 옵션으로 **참조 **무결성성**을 **유지**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
DDL은 **"데이터베이스 청사진"**을 만드는 도구다.

**SQL 명령어 분류**:
| 분류 | 용도 | 대표 명령어 |
|------|------|-------------|
| **DDL** | 구조 정의 | CREATE, ALTER, DROP |
| **DML** | 데이터 조작 | SELECT, INSERT, UPDATE, DELETE |
| **DCL** | 권한 제어 | GRANT, REVOKE |
| **TCL** | 트랜잭션 제어 | COMMIT, ROLLBACK |

### 💡 비유
DDL은 **건축 설계도**와 같다.
- **CREATE**: 새 건물 건설
- **ALTER**: 증축/개조
- **DROP**: 철거
- **TRUNCATE**: 내부 비움

---

## Ⅱ. 아키텍처 및 핵심 원리

### CREATE 문

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         CREATE Statement Examples                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. Create Table with Constraints:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  CREATE TABLE employees (                                                                 │  │
    │      employee_id INT PRIMARY KEY AUTO_INCREMENT,                                         │  │
    │      first_name VARCHAR(50) NOT NULL,                                                     │  │
    │      last_name VARCHAR(50) NOT NULL,                                                      │  │
    │      email VARCHAR(100) UNIQUE,                                                           │  │
    │      hire_date DATE DEFAULT CURRENT_DATE,                                                 │  │
    │      salary DECIMAL(10, 2) CHECK (salary > 0),                                           │  │
    │      department_id INT,                                                                   │  │
    │      FOREIGN KEY (department_id) REFERENCES departments(id)                                │  │
    │         ON DELETE SET NULL ON UPDATE CASCADE                                              │  │
    │  );                                                                                      │  │
    │                                                                                         │  │
    │  Constraint Types:                                                                       │  │
    │  • PRIMARY KEY: Unique identifier, NOT NULL, one per table                               │  │
    │  • FOREIGN KEY: Referential integrity, can be NULL                                        │  │
    │  • UNIQUE: No duplicates, multiple NULLs allowed                                         │  │
    │  • NOT NULL: Must have value                                                             │  │
    │  • CHECK: Boolean expression must be true                                                │  │
    │  • DEFAULT: Value if not specified                                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. Create Index:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  CREATE INDEX idx_employee_email ON employees(email);                                   │  │
    │  CREATE UNIQUE INDEX idx_employee_ssn ON employees(ssn);                                │  │
    │  CREATE INDEX idx_employee_name ON employees(last_name, first_name);  -- Composite     │  │
    │                                                                                         │  │
    │  Index Types:                                                                           │  │
    │  • B-tree: Default, equality and range queries                                            │  │
    │  • Hash: Equality only (memory engines)                                                   │  │
    │  • FULLTEXT: Text search (MyISAM, InnoDB 5.6+)                                            │  │
    │  • SPATIAL: Geospatial data                                                              │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    3. Create View:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  CREATE VIEW employee_department AS                                                       │  │
    │  SELECT                                                                                 │  │
    │      e.employee_id, e.first_name, e.last_name, d.name AS department                     │  │
    │  FROM employees e                                                                       │  │
    │  JOIN departments d ON e.department_id = d.id;                                          │  │
    │                                                                                         │  │
    │  View Benefits:                                                                          │  │
    │  • Simplify complex queries                                                              │  │
    │  • Hide sensitive columns                                                                │  │
    │  • Provide logical data independence                                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    4. Create Sequence:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  CREATE SEQUENCE seq_order_id START WITH 1 INCREMENT BY 1;                              │  │
    │                                                                                         │  │
    │  Usage:                                                                                 │  │
    │  INSERT INTO orders (id, customer_id) VALUES (seq_order_id.NEXTVAL, 123);               │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### ALTER 문

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         ALTER Statement Examples                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. Add Column:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ALTER TABLE employees ADD COLUMN phone VARCHAR(20);                                   │  │
    │  ALTER TABLE employees ADD COLUMN bonus DECIMAL(10,2) DEFAULT 0;                       │  │
    │                                                                                         │  │
    │  -- Add with constraint                                                                 │  │
    │  ALTER TABLE employees ADD CONSTRAINT fk_manager                                       │  │
    │        FOREIGN KEY (manager_id) REFERENCES employees(employee_id);                         │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. Modify Column:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  -- Change data type (must be compatible)                                               │  │
    │  ALTER TABLE employees MODIFY COLUMN salary DECIMAL(12, 2);                             │  │
    │  ALTER TABLE employees MODIFY COLUMN email VARCHAR(150) NOT NULL;                        │  │
    │                                                                                         │  │
    │  -- Rename column (MySQL, PostgreSQL)                                                    │  │
    │  ALTER TABLE employees RENAME COLUMN phone TO mobile;                                   │  │
    │                                                                                         │  │
    │  -- Change default                                                                      │  │
    │  ALTER TABLE employees ALTER COLUMN bonus SET DEFAULT 1000;                             │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    3. Drop Column:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ALTER TABLE employees DROP COLUMN bonus;                                              │  │
    │                                                                                         │  │
    │  -- Drop constraint                                                                     │  │
    │  ALTER TABLE employees DROP CONSTRAINT fk_manager;                                      │  │
    │  ALTER TABLE employees DROP PRIMARY KEY;                                                │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    4. Add/Drop Index:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ALTER TABLE employees ADD INDEX idx_phone (phone);                                     │  │
    │  ALTER TABLE employees DROP INDEX idx_phone;                                            │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    5. Rename Table:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ALTER TABLE employees RENAME TO staff;                                                │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### DROP vs TRUNCATE vs DELETE

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         DROP vs TRUNCATE vs DELETE Comparison                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Comparison Table:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Operation  │  Object    │  Data  │  Structure  │  Speed  │  Rollback  │  Space  │  │  │
    │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  DROP       │  Table     │  All   │  Removed    │  Fast   │  No        │  Freed  │  │  │
    │  TRUNCATE   │  Table     │  All   │  Kept       │  Fast   │  No        │  Freed  │  │  │
    │  DELETE     │  Table     │  Rows  │  Kept       │  Slow   │  Yes       │  Kept   │  │  │
    │  DROP       │  Index     │  N/A   │  Removed    │  Fast   │  No        │  Freed  │  │  │
    │  DELETE     │  Index     │  N/A   │  N/A        │  N/A    │  N/A       │  N/A    │  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Examples:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  DROP TABLE employees;                              -- Remove table and data               │  │
    │  DROP INDEX idx_employee_email;                  -- Remove index                      │  │
    │                                                                                         │  │
    │  TRUNCATE TABLE employees;                        -- Remove all data, keep table        │  │
    │                                                                                         │  │
    │  DELETE FROM employees;                           -- Remove all data, keep table        │  │
    │  DELETE FROM employees WHERE department_id = 5;  -- Conditional delete              │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Why TRUNCATE is Faster:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  DELETE:                                                                                │  │
    │  • Scans table, logs each row                                                           │  │
    │  • Fires triggers (BEFORE/AFTER)                                                         │  │
    │  • Can be rolled back                                                                   │  │
    │  • Leaves empty pages                                                                   │  │
    │                                                                                         │  │
    │  TRUNCATE:                                                                              │  │
    │  • Deallocates data pages directly                                                       │  │
    │  • No row-level logging                                                                 │  │
    │  • Minimal logging (page deallocation)                                                   │  │
    │  • Cannot be rolled back                                                                │  │
    │  • Resets AUTO_INCREMENT                                                                │  │
    │  • No triggers fired                                                                    │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 제약조건 상세 비교

| 제약조건 | 목적 | 컬럼 수 | NULL 허용 | 인덱스 |
|----------|------|----------|-----------|--------|
| **PRIMARY KEY** | 식별자 | 1개 이상 | ✗ | 자동 |
| **FOREIGN KEY** | 참조무결성 | 1개 이상 | ✓ | 사용 |
| **UNIQUE** | 유일성 | 1개 이상 | ✓ 1개 | 자동 |
| **NOT NULL** | 필수값 | 단일 | - | - |
| **CHECK** | 조건검증 | 단일 | - | - |
| **DEFAULT** | 기본값 | 단일 | - | - |

### 참조 무결성 액션

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Referential Integrity Actions                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ON DELETE Actions:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ON DELETE CASCADE:                                                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Parent deleted → Child rows automatically deleted                                   │  │  │
    │  │  Example: DELETE FROM departments WHERE id = 5                                     │  │  │
    │  │           → All employees in department 5 deleted                                   │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  ON DELETE SET NULL:                                                                    │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Parent deleted → Child foreign key set to NULL                                    │  │  │
    │  │  Example: DELETE FROM departments WHERE id = 5                                     │  │  │
    │  │           → employees.department_id = NULL                                         │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  ON DELETE SET DEFAULT:                                                                 │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Parent deleted → Child foreign key set to DEFAULT value                           │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  ON DELETE RESTRICT (default):                                                           │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Parent deleted → Reject if child rows exist                                      │  │  │
    │  │  Example: DELETE FROM departments WHERE id = 5                                     │  │  │
    │  │           → ERROR: Cannot delete department with employees                         │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  ON DELETE NO ACTION:                                                                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Similar to RESTRICT but checked late (deferred)                                   │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    ON UPDATE Actions:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ON UPDATE CASCADE:                                                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Parent primary key updated → Child foreign keys updated                             │  │  │
    │  │  Example: UPDATE departments SET id = 10 WHERE id = 5                               │  │  │
    │  │           → employees.department_id = 10 WHERE department_id = 5                   │  │  │
    │  │  → Rarely used (PK should be immutable)                                             │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  ON UPDATE SET NULL/SET DEFAULT/RESTRICT/NO ACTION:                                      │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Similar semantics to ON DELETE                                                      │  │  │
    │  │  SET NULL is useful for allowing reassignment without orphaned records             │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 스키마 버전 관리
**상황**: 프로덕션 DB DDL 배포
**판단**: 안전한 스키마 변경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Safe Schema Migration Pattern                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Migration Script Structure:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  -- V1__Create_employees_table.sql                                                     │  │
    │  BEGIN TRANSACTION;                                                                     │  │
    │  CREATE TABLE employees (...);                                                          │  │
    │  COMMIT;                                                                                 │  │
    │                                                                                         │  │
    │  -- V2__Add_phone_column.sql                                                             │  │
    │  BEGIN TRANSACTION;                                                                     │  │
    │  -- Add column (non-blocking)                                                            │  │
    │  ALTER TABLE employees ADD COLUMN phone VARCHAR(20) NULL;                                │  │
    │  -- Backfill data (for existing rows)                                                   │  │
    │  UPDATE employees SET phone = 'N/A' WHERE phone IS NULL;                                 │  │
    │  -- Add NOT NULL constraint (blocking, but short)                                        │  │
    │  ALTER TABLE employees MODIFY COLUMN phone VARCHAR(20) NOT NULL;                         │  │
    │  COMMIT;                                                                                 │  │
    │                                                                                         │  │
    │  -- V3__Rename_email_to_contact_email.sql                                               │  │
    │  BEGIN TRANSACTION;                                                                     │  │
    │  -- Add new column                                                                      │  │
    │  ALTER TABLE employees ADD COLUMN contact_email VARCHAR(100);                            │  │
    │  -- Copy data                                                                           │  │
    │  UPDATE employees SET contact_email = email;                                            │  │
    │  -- Add NOT NULL constraint                                                              │  │
    │  ALTER TABLE employees MODIFY COLUMN contact_email VARCHAR(100) NOT NULL;                │  │
    │  -- Drop old column (blocking, but data already migrated)                                │  │
    │  ALTER TABLE employees DROP COLUMN email;                                              │  │
    │  COMMIT;                                                                                 │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Best Practices:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Use transactions for schema changes (rollback on error)                              │  │
    │  2. Make changes backward compatible when possible                                       │  │
    │  3. Add columns as NULL first, backfill, then make NOT NULL                             │  │
    │  4. Use ALTER TABLE instead of DROP + CREATE (preserves data)                           │  │
    │  5. Test migrations on staging first                                                     │  │
    │  6. Have rollback scripts ready                                                          │  │
    │  7. Use versioned migration scripts                                                     │  │
    │  8. Lock tables during schema changes to prevent concurrent modifications                │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 대용량 테이블 DDL 주의사항

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Large Table DDL Considerations                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Adding Columns to Large Tables:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Problem: ALTER TABLE on billion-row table locks table for hours                         │  │
    │                                                                                         │  │
    │  Approaches:                                                                            │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. Online DDL (MySQL 8.0+, PostgreSQL 12+):                                         │  │  │
    │  │     ALTER TABLE employees ADD COLUMN phone VARCHAR(20), ALGORITHM=INPLACE;           │  │  │
    │  │     → Non-blocking, concurrent DML allowed                                          │  │  │
    │  │                                                                                      │  │  │
    │  │  2. Create new table, copy data, swap:                                               │  │  │
    │  │     CREATE TABLE employees_new LIKE employees;                                       │  │  │
    │  │     ALTER TABLE employees_new ADD COLUMN phone VARCHAR(20);                           │  │  │
    │  │     INSERT INTO employees_new SELECT *, NULL FROM employees;                          │  │  │
    │  │     RENAME TABLE employees TO employees_old, employees_new TO employees;              │  │  │
    │  │     DROP TABLE employees_old;                                                       │  │  │
    │  │     → Downtime only during swap (seconds)                                            │  │  │
    │  │                                                                                      │  │  │
    │  │  3. Tool-assisted: pt-online-schema-change (Percona)                                 │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Creating Indexes on Large Tables:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Problem: Index creation locks table, blocks writes                                     │  │
    │                                                                                         │  │
    │  Solution: Online index creation                                                        │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  MySQL:                                                                                │  │  │
    │  │  ALTER TABLE employees ADD INDEX idx_phone (phone), ALGORITHM=INPLACE, LOCK=NONE; │  │  │
    │  │                                                                                      │  │  │
    │  │  PostgreSQL:                                                                          │  │  │
    │  │  CREATE INDEX CONCURRENTLY idx_phone ON employees(phone);                            │  │  │
    │  │                                                                                      │  │  │
    │  │  Oracle:                                                                              │  │  │
    │  │  CREATE INDEX idx_phone ON employees(phone) ONLINE;                                  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### DDL 최적화 기대 효과

| 작업 | 최적화 방법 | 효과 |
|------|-------------|------|
| **컬럼 추가** | NULL → backfill → NOT NULL | 비차단 |
| **인덱스 생성** | CONCURRENT/INPLACE | 작업 중단 없음 |
| **PK 변경** | 임시 PK 사용 | 빠른 변경 |
| **대량 삭제** | TRUNCATE vs DROP | 빠른 삭제 |

### 모범 사례

1. **트랜잭션**: 롤백 가능
2. **백업**: DDL 전 필수
3. **테스트**: 스테이징 먼저
4. **문서화**: 스키마 버전관리

### 미래 전망

1. **자동화**: 마이그레이션 도구
2. **CI/CD**: 스키마 자동 배포
3. **온라인 DDL**: 기본 기능
4. **선언적**: 버전관리 통합

### ※ 참고 표준/가이드
- **SQL-92**: DDL 표준
- **ANSI**: SQL 규격
- **ISO**: 9075
- **MySQL**: ALTER TABLE

---

## 📌 관련 개념 맵

- [DML](./37_dml.md) - 데이터 조작
- [정규화](./19_normalization.md) - 설계
- [트랜잭션](./22_acid.md) - TCL
- [뷰](./47_view.md) - 가상 테이블
