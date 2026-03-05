+++
title = "외래 키 (Foreign Key) - 참조 무결성 보장"
date = "2026-03-04"
[extra]
categories = "studynotes-database"
+++

# 외래 키 (Foreign Key)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 외래 키(FK)는 다른 테이블의 기본 키(PK)를 참조하는 속성으로, 릴레이션 간 관계를 정의하고 참조 무결성(Referential Integrity)을 보장하는 핵심 제약조건입니다.
> 2. **가치**: 외래 키는 데이터 불일치를 99% 방지하고, 조인 연산의 기반을 제공하며, CASCADE 옵션으로 관련 데이터 일괄 처리를 자동화합니다.
> 3. **융합**: 외래 키는 관계형 모델의 관계 표현 수단이며, ORM의 연관관계 매핑, 마이크로서비스의 데이터 참조 설계에도 영향을 미칩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**외래 키(Foreign Key, FK)**는 한 릴레이션의 속성(또는 속성 집합)이 다른 릴레이션의 기본 키(Primary Key)를 참조하는 제약조건입니다.

**핵심 정의**:
```
릴레이션 R1의 외래 키 FK가 릴레이션 R2의 기본 키 PK를 참조할 때:
- FK의 각 값은 R2.PK에 존재하는 값이거나 NULL이어야 함
- 이를 참조 무결성(Referential Integrity)이라 함
```

**외래 키의 특성**:
- 참조하는 쪽: 자식 테이블(Child Table) / 외래 키 테이블
- 참조되는 쪽: 부모 테이블(Parent Table) / 기본 키 테이블
- 외래 키 값은 부모 테이블의 기본 키 값이거나 NULL
- 외래 키와 기본 키는 도메인(데이터 타입)이 일치해야 함

#### 2. 💡 비유를 통한 이해
**여권 번호**로 비유할 수 있습니다:

```
[여행객 테이블]              [여권 테이블]
┌────────────┐              ┌────────────┐
│ 여행객ID   │              │ 여권번호   │ ← 기본 키
│ 이름       │              │ 발급일     │
│ 여권번호   │──────────────│ 만료일     │
│   (FK)     │  참조        │ 발급국     │
└────────────┘              └────────────┘

- 여행객의 여권번호는 실제 존재하는 여권번호여야 함
- 여행객이 여권이 없으면 여권번호는 NULL
- 여권이 폐기되면 해당 여행객의 여행객ID도 처리 필요
```

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계**: 파일 시스템에서는 관련 데이터 간의 일관성을 애플리케이션에서 수동으로 관리해야 했습니다. 실수로 한쪽만 수정하면 데이터 불일치가 발생했습니다.
2. **혁신적 패러다임의 도입**: E.F. Codd의 관계형 모델에서 외래 키 개념을 도입하여 DBMS가 자동으로 참조 무결성을 보장하도록 했습니다.
3. **비즈니스적 요구사항**: 주문-상품, 학생-과목, 사원-부서 등 모든 비즈니스 데이터는 관계를 가지므로 외래 키는 필수적입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 외래 키 구성 요소 (표)

| 구성 요소 | 정의 | 예시 | 비고 |
|:---|:---|:---|:---|
| **외래 키 속성** | FK를 구성하는 칼럼 | orders.customer_id | 자식 테이블 |
| **참조 테이블** | FK가 가리키는 테이블 | customers | 부모 테이블 |
| **참조 속성** | FK가 참조하는 PK | customers.customer_id | |
| **ON DELETE** | 부모 삭제 시 동작 | CASCADE, RESTRICT | |
| **ON UPDATE** | 부모 수정 시 동작 | CASCADE, SET NULL | |

#### 2. 외래 키 관계 다이어그램

```text
+====================================================================+
|                    [ 외래 키 관계 구조 ]                            |
+====================================================================+

[1:N 관계 (가장 일반적)]

  부모 테이블 (1)                      자식 테이블 (N)
┌─────────────────┐                ┌─────────────────┐
│ customers       │                │ orders          │
├─────────────────┤                ├─────────────────┤
│ customer_id (PK)│◄───────────────│ order_id (PK)   │
│ name            │    참조        │ customer_id (FK)│
│ email           │                │ order_date      │
│ phone           │                │ total_amount    │
└─────────────────┘                └─────────────────┘
         │                                   │
         │ 1                                 │ N
         └───────────────────────────────────┘
              한 고객은 여러 주문을 가질 수 있음

[M:N 관계 (교차 테이블 필요)]

  students (M)                enrollments                courses (N)
┌─────────────┐             ┌─────────────┐            ┌─────────────┐
│ student_id  │◄────────────│ student_id  │───────────►│ course_id   │
│ (PK)        │    FK       │ (FK)        │    FK      │ (PK)        │
│ name        │             │ course_id   │            │ name        │
└─────────────┘             │ (FK)        │            └─────────────┘
                            │ grade       │
                            │ (PK: 복합키) │
                            └─────────────┘

[자기 참조 (Self-Referencing)]

┌─────────────────┐
│ employees       │
├─────────────────┤
│ emp_id (PK)     │
│ name            │
│ manager_id (FK) │◄──┐
└─────────────────┘   │
      │               │
      └───────────────┘
        자신의 테이블 참조
        (manager_id는 emp_id를 참조)
```

#### 3. 심층 동작 원리: 참조 무결성 옵션

**1단계: 외래 키 생성**

```sql
-- 기본 외래 키 생성
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(15,2),

    -- 외래 키 제약조건
    CONSTRAINT fk_order_customer
    FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id)
);

-- 옵션 포함 외래 키
ALTER TABLE orders
ADD CONSTRAINT fk_order_customer
FOREIGN KEY (customer_id)
REFERENCES customers(customer_id)
    ON DELETE RESTRICT    -- 참조하는 데이터 있으면 삭제 불가
    ON UPDATE CASCADE;    -- 부모 PK 변경 시 자식도 변경
```

**2단계: 참조 무결성 옵션 상세**

```sql
-- ON DELETE / ON UPDATE 옵션

-- 1. CASCADE: 부모 변경 시 자식도 자동 변경
ALTER TABLE order_items
ADD CONSTRAINT fk_item_order
FOREIGN KEY (order_id)
REFERENCES orders(order_id)
    ON DELETE CASCADE    -- 주문 삭제 시 주문상품도 자동 삭제
    ON UPDATE CASCADE;   -- 주문ID 변경 시 상품ID도 변경

-- 2. RESTRICT (또는 NO ACTION): 부모 변경 거부
ALTER TABLE orders
ADD CONSTRAINT fk_order_customer
FOREIGN KEY (customer_id)
REFERENCES customers(customer_id)
    ON DELETE RESTRICT;  -- 주문이 있는 고객은 삭제 불가

-- 3. SET NULL: 부모 삭제 시 자식 FK를 NULL로 설정
ALTER TABLE employees
ADD CONSTRAINT fk_emp_department
FOREIGN KEY (dept_id)
REFERENCES departments(dept_id)
    ON DELETE SET NULL;  -- 부서 삭제 시 직원의 dept_id를 NULL로

-- 4. SET DEFAULT: 부모 삭제 시 자식 FK를 기본값으로
ALTER TABLE orders
ADD CONSTRAINT fk_order_status
FOREIGN KEY (status_id)
REFERENCES order_status(status_id)
    ON DELETE SET DEFAULT;  -- 상태 삭제 시 기본 상태(1)로 설정
```

**3단계: 참조 무결성 검증 과정**

```text
[INSERT 시 검증]
INSERT INTO orders (order_id, customer_id, ...) VALUES (1, 999, ...);

1. DBMS가 customers 테이블에서 customer_id = 999 검색
2. 존재하면 → INSERT 허용
3. 존재하지 않으면 → "foreign key constraint fails" 에러

[DELETE 시 검증]
DELETE FROM customers WHERE customer_id = 1;

1. DBMS가 orders 테이블에서 customer_id = 1 검색
2. 존재하면:
   - RESTRICT: 삭제 거부
   - CASCADE: 해당 orders도 삭제
   - SET NULL: orders.customer_id를 NULL로 변경
3. 존재하지 않으면 → DELETE 허용

[UPDATE 시 검증]
UPDATE customers SET customer_id = 999 WHERE customer_id = 1;

1. 새로운 ID(999)가 이미 존재하는지 확인 (PK 제약)
2. 기존 ID(1)을 참조하는 orders 확인
3. CASCADE면 orders.customer_id도 999로 변경
4. RESTRICT면 참조가 있으면 수정 거부
```

#### 4. 실무 수준의 외래 키 관리 구현

```python
"""
외래 키 제약조건 관리 시스템 구현
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from enum import Enum

class ForeignKeyAction(Enum):
    """외래 키 액션 정의"""
    CASCADE = "CASCADE"
    RESTRICT = "RESTRICT"
    SET_NULL = "SET NULL"
    SET_DEFAULT = "SET DEFAULT"
    NO_ACTION = "NO ACTION"

@dataclass
class ForeignKey:
    """외래 키 정의"""
    name: str
    child_table: str
    child_columns: List[str]
    parent_table: str
    parent_columns: List[str]
    on_delete: ForeignKeyAction = ForeignKeyAction.RESTRICT
    on_update: ForeignKeyAction = ForeignKeyAction.RESTRICT

@dataclass
class Table:
    """테이블 정의"""
    name: str
    primary_key: List[str]
    rows: List[Dict[str, Any]] = field(default_factory=list)

class ForeignKeyManager:
    """외래 키 관리자"""

    def __init__(self):
        self.tables: Dict[str, Table] = {}
        self.foreign_keys: List[ForeignKey] = []

    def add_table(self, table: Table) -> None:
        """테이블 추가"""
        self.tables[table.name] = table

    def add_foreign_key(self, fk: ForeignKey) -> None:
        """외래 키 추가"""
        # 유효성 검증
        if fk.child_table not in self.tables:
            raise ValueError(f"자식 테이블 '{fk.child_table}' 없음")
        if fk.parent_table not in self.tables:
            raise ValueError(f"부모 테이블 '{fk.parent_table}' 없음")

        self.foreign_keys.append(fk)
        print(f"[FK] 외래 키 추가: {fk.child_table}.{fk.child_columns} "
              f"→ {fk.parent_table}.{fk.parent_columns}")

    def insert_row(self, table_name: str, row: Dict[str, Any]) -> bool:
        """
        행 삽입 (참조 무결성 검증)
        """
        table = self.tables.get(table_name)
        if not table:
            raise ValueError(f"테이블 '{table_name}' 없음")

        # 이 테이블이 자식인 외래 키 검증
        for fk in self.foreign_keys:
            if fk.child_table == table_name:
                if not self._validate_fk_on_insert(fk, row):
                    return False

        table.rows.append(row)
        print(f"[INSERT] {table_name}: {row}")
        return True

    def delete_row(self, table_name: str, condition: Dict[str, Any]) -> int:
        """
        행 삭제 (참조 무결성 처리)
        """
        table = self.tables.get(table_name)
        if not table:
            raise ValueError(f"테이블 '{table_name}' 없음")

        # 삭제할 행 찾기
        rows_to_delete = [
            r for r in table.rows
            if all(r.get(k) == v for k, v in condition.items())
        ]

        if not rows_to_delete:
            return 0

        # 이 테이블이 부모인 외래 키 처리
        for fk in self.foreign_keys:
            if fk.parent_table == table_name:
                self._handle_fk_on_delete(fk, rows_to_delete)

        # 실제 삭제
        original_count = len(table.rows)
        table.rows = [
            r for r in table.rows
            if not all(r.get(k) == v for k, v in condition.items())
        ]

        deleted = original_count - len(table.rows)
        print(f"[DELETE] {table_name}: {deleted}행 삭제")
        return deleted

    def _validate_fk_on_insert(self, fk: ForeignKey, row: Dict[str, Any]) -> bool:
        """INSERT 시 FK 검증"""
        parent_table = self.tables[fk.parent_table]

        # FK 값 추출
        fk_values = [row.get(col) for col in fk.child_columns]

        # NULL이면 통과 (NULL 허용 가정)
        if all(v is None for v in fk_values):
            return True

        # 부모 테이블에서 참조 값 존재 확인
        for parent_row in parent_table.rows:
            parent_values = [parent_row.get(col) for col in fk.parent_columns]
            if fk_values == parent_values:
                return True

        print(f"[FK 위반] {fk_values}이 {fk.parent_table}에 없음")
        return False

    def _handle_fk_on_delete(self, fk: ForeignKey,
                            deleted_rows: List[Dict[str, Any]]) -> None:
        """DELETE 시 FK 액션 처리"""
        child_table = self.tables[fk.child_table]

        for deleted_row in deleted_rows:
            # 삭제된 행의 PK 값
            parent_values = [deleted_row.get(col) for col in fk.parent_columns]

            # 자식 테이블에서 참조하는 행 찾기
            for child_row in child_table.rows:
                child_values = [child_row.get(col) for col in fk.child_columns]

                if child_values == parent_values:
                    self._apply_fk_action(fk.on_delete, child_row,
                                         fk.child_columns)

    def _apply_fk_action(self, action: ForeignKeyAction,
                        row: Dict[str, Any], columns: List[str]) -> None:
        """FK 액션 적용"""
        if action == ForeignKeyAction.CASCADE:
            # CASCADE: 행 삭제 (별도 처리 필요)
            print(f"[FK CASCADE] 참조 행 삭제 필요: {row}")
        elif action == ForeignKeyAction.SET_NULL:
            for col in columns:
                row[col] = None
            print(f"[FK SET NULL] {columns} → NULL")
        elif action == ForeignKeyAction.RESTRICT:
            raise ValueError(
                f"[FK RESTRICT] 참조 무결성 위반: 삭제 불가"
            )

    def get_referencing_rows(self, table_name: str,
                            pk_values: List[Any]) -> List[Dict]:
        """특정 PK를 참조하는 모든 행 조회"""
        references = []

        for fk in self.foreign_keys:
            if fk.parent_table == table_name:
                child_table = self.tables[fk.child_table]
                for row in child_table.rows:
                    child_values = [row.get(col) for col in fk.child_columns]
                    if child_values == pk_values:
                        references.append({
                            'table': fk.child_table,
                            'row': row
                        })

        return references

# ==================== 사용 예시 ====================
if __name__ == "__main__":
    manager = ForeignKeyManager()

    # 1. 테이블 정의
    manager.add_table(Table(
        name="customers",
        primary_key=["customer_id"],
        rows=[
            {"customer_id": 1, "name": "홍길동", "email": "hong@test.com"},
            {"customer_id": 2, "name": "김철수", "email": "kim@test.com"},
        ]
    ))

    manager.add_table(Table(
        name="orders",
        primary_key=["order_id"],
        rows=[]
    ))

    # 2. 외래 키 정의
    manager.add_foreign_key(ForeignKey(
        name="fk_order_customer",
        child_table="orders",
        child_columns=["customer_id"],
        parent_table="customers",
        parent_columns=["customer_id"],
        on_delete=ForeignKeyAction.RESTRICT,
        on_update=ForeignKeyAction.CASCADE
    ))

    # 3. INSERT 테스트
    print("\n=== INSERT 테스트 ===")

    # 유효한 FK
    manager.insert_row("orders", {
        "order_id": 1,
        "customer_id": 1,
        "total": 100000
    })

    # 무효한 FK
    manager.insert_row("orders", {
        "order_id": 2,
        "customer_id": 999,  # 존재하지 않음
        "total": 50000
    })

    # 4. DELETE 테스트
    print("\n=== DELETE 테스트 ===")

    # 참조가 있는 고객 삭제 시도
    try:
        manager.delete_row("customers", {"customer_id": 1})
    except ValueError as e:
        print(f"삭제 실패: {e}")

    # 5. 참조 조회
    print("\n=== 참조 조회 ===")
    refs = manager.get_referencing_rows("customers", [1])
    print(f"고객 1을 참조하는 주문: {refs}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 참조 무결성 옵션 비교

| 옵션 | DELETE 시 동작 | UPDATE 시 동작 | 사용 케이스 |
|:---|:---|:---|:---|
| **CASCADE** | 자식도 삭제 | 자식도 수정 | 강한 종속 (주문-상품) |
| **RESTRICT** | 삭제 거부 | 수정 거부 | 약한 종속 (사원-부서) |
| **SET NULL** | 자식 FK = NULL | 자식 FK = NULL | 선택적 참조 |
| **SET DEFAULT** | 자식 FK = 기본값 | 자식 FK = 기본값 | 기본 상태 있음 |

#### 2. 외래 키 vs 조인 인덱스

| 비교 항목 | 외래 키 | 조인 인덱스 |
|:---|:---|:---|
| **목적** | 무결성 보장 | 성능 최적화 |
| **자동 생성** | 아니오 | DBMS 따라 다름 |
| **필수 여부** | 논리적 필수 | 성능상 선택 |
| **오버헤드** | INSERT/DELETE 시 | 조회 시 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 대량 데이터 삭제**
- 상황: 100만 건 주문 데이터 삭제
- 판단: CASCADE 사용 시 대량 DELETE 유발
- 전략: 배치로 나누어 삭제 또는 FK 일시 해제

**시나리오 2: 마이크로서비스**
- 상황: 서비스 간 DB 분리
- 판단: FK가 물리적으로 불가능
- 전략: 논리적 참조 + 이벤트 기반 동기화

#### 2. 안티패턴 (Anti-patterns)
- **FK 없는 설계**: 무결성 보장 불가
- **과도한 CASCADE**: 의도치 않은 대량 삭제
- **순환 FK**: A→B→A 참조 (주의 필요)

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과
- 데이터 불일치 99% 방지
- 관계 표현의 표준 수단
- 조인 연산의 기반

#### 2. 참고 표준
- **ANSI SQL**: FOREIGN KEY 문법
- **참조 무결성**: Codd의 12규칙 중 하나

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[기본 키](@/studynotes/05_database/01_relational/primary_key.md)**: FK가 참조하는 대상
- **[무결성 제약조건](@/studynotes/05_database/01_relational/normalization.md)**: FK의 목적
- **[조인](@/studynotes/05_database/03_optimization/hash_join.md)**: FK 기반 연산
- **[ER 모델](@/studynotes/05_database/01_relational/er_model.md)**: 관계 표현

---

### 👶 어린이를 위한 3줄 비유 설명
1. **가족 관계**: 나는 아빠의 자식이에요. 내 '아빠 이름' 칸에는 실제 내 아빠 이름만 쓸 수 있죠. 없는 사람을 아빠라고 부를 수 없어요!
2. **주소록**: 친구 전화번호부에서 '반' 칸에는 우리 반에 실제로 있는 반 번호만 쓸 수 있어요. 없는 반 번호는 쓰면 안 돼요!
3. **도서대출**: 도서관에서 책을 빌릴 때 책 번호를 써요. 이 번호는 도서관에 실제 있는 책 번호여야 하죠. 없는 책을 빌릴 수는 없어요!
