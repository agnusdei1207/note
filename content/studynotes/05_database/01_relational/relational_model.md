+++
title = "관계형 데이터 모델 (Relational Model)"
date = "2026-03-04"
[extra]
categories = "studynotes-database"
++-

# 관계형 데이터 모델 (Relational Model)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 관계형 데이터 모델은 E.F. Codd가 1970년 제안한 데이터 모델로, 데이터를 2차원 테이블(릴레이션)로 표현하고 수학적 관계 대수/해석을 기반으로 조작합니다.
> 2. **가치**: 관계형 모델은 데이터 독립성, 무결성 보장, 선언적 질의(SQL)를 제공하여 전 세계 데이터베이스 시장의 90% 이상을 차지하는 표준 모델이 되었습니다.
> 3. **융합**: 관계형 모델은 객체지향, XML, JSON 등 다양한 데이터 모델과 통합 진화하며, 현대 NewSQL, 클라우드 DB의 이론적 기반이 됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**관계형 데이터 모델(Relational Model)**은 데이터를 **릴레이션(Relation)**이라는 2차원 테이블 형태로 표현하고, 이를 수학적 **집합론(Set Theory)**과 **술어 논리(Predicate Logic)**에 기반하여 조작하는 데이터 모델입니다.

**핵심 구성 요소**:
1. **구조(Structure)**: 릴레이션, 튜플, 속성, 도메인, 키
2. **조작(Manipulation)**: 관계 대수, 관계 해석, SQL
3. **제약(Constraint)**: 무결성 제약조건 (개체, 참조, 도메인)

**릴레이션의 수학적 정의**:
```
R ⊆ D1 × D2 × ... × Dn
- R: 릴레이션 (n-튜플의 집합)
- Di: 도메인 (속성이 가질 수 있는 값의 집합)
- n: 차수(Degree) = 속성 개수
- |R|: 카디널리티(Cardinality) = 튜플 개수
```

#### 2. 💡 비유를 통한 이해
**엑셀 스프레드시트**로 비유할 수 있습니다:

```
[학생 테이블] = 릴레이션
┌────────┬────────┬────────┬────────┐
│ 학번   │ 이름   │ 학과   │ 학년   │ ← 속성(Attribute/Column)
├────────┼────────┼────────┼────────┤
│ 001    │ 홍길동 │ 컴공   │ 3      │ ← 튜플(Tuple/Row)
│ 002    │ 김철수 │ 경영   │ 2      │
│ 003    │ 이영희 │ 컴공   │ 3      │
└────────┴────────┴────────┴────────┘
    ↑
  도메인(Domain): 학년의 도메인 = {1, 2, 3, 4}
```

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계**: 계층형(IMS)과 망형(IDMS) 모델은 데이터 접근 방법이 복잡하고, 데이터 독립성이 없었으며, 프로그래머가 네비게이션 경로를 모두 알아야 했습니다.
2. **혁신적 패러다임의 도입**: 1970년 IBM의 Edgar F. Codd가 "A Relational Model of Data for Large Shared Data Banks" 논문에서 관계형 모델을 제안했습니다. 이는 데이터를 수학적으로 표현하고, 선언적 질의를 가능하게 했습니다.
3. **비즈니스적 요구사항**: Oracle(1979), DB2(1983), SQL Server(1989), MySQL(1995) 등 상용 RDBMS가 등장하며, 관계형 모델은 데이터베이스의 사실상 표준이 되었습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 관계형 모델 핵심 용어 (표)

| 용어 | 정의 | 수학적 표현 | SQL 대응 |
|:---|:---|:---|:---|
| **릴레이션(Relation)** | 튜플의 집합 | R ⊆ D1×D2×...×Dn | 테이블(Table) |
| **속성(Attribute)** | 데이터 항목 | Ai | 칼럼(Column) |
| **도메인(Domain)** | 속성 값의 집합 | Di | 데이터 타입 |
| **튜플(Tuple)** | 릴레이션의 행 | (v1, v2, ..., vn) | 행(Row) |
| **차수(Degree)** | 속성 개수 | n | 칼럼 수 |
| **카디널리티** | 튜플 개수 | \|R\| | 행 수 |
| **스키마(Schema)** | 릴레이션 구조 | R(A1, A2, ..., An) | 테이블 정의 |
| **인스턴스(Instance)** | 실제 데이터 | 튜플 집합 | 데이터 |

#### 2. 관계형 모델 구조 다이어그램

```text
+====================================================================+
|                    [ 관계형 데이터 모델 구조 ]                      |
+====================================================================+

[릴레이션 스키마 (Relation Schema)]
학생(학번, 이름, 학과, 학년)  ← 논리적 구조 정의 (정적)

[릴레이션 인스턴스 (Relation Instance)]
┌─────────────────────────────────────────────────────────────┐
│                    릴레이션 R (학생)                         │
├────────┬────────┬────────┬────────┬─────────────────────────┤
│ 학번   │ 이름   │ 학과   │ 학년   │ ← 속성 (Attribute)       │
│ (PK)   │        │ (FK)   │        │   Key: 기본키, 외래키    │
├────────┼────────┼────────┼────────┼─────────────────────────┤
│ 001    │ 홍길동 │ D01    │ 3      │ ← 튜플 1 (Tuple)        │
│ 002    │ 김철수 │ D01    │ 2      │ ← 튜플 2                │
│ 003    │ 이영희 │ D02    │ 3      │ ← 튜플 3                │
└────────┴────────┴────────┴────────┴─────────────────────────┘
    ↑        ↑        ↑        ↑
  도메인   도메인   도메인   도메인
  (문자)  (문자)   (코드)   (정수1-4)

[릴레이션의 특성]
1. 튜플의 순서는 무의미 (집합)
2. 속성의 순서는 무의미 (집합)
3. 튜플의 유일성 (중복 없음)
4. 속성 값의 원자성 (Atomic Value)

[릴레이션 간 관계]
학생                        학과
┌────────────────┐         ┌────────────────┐
│ 학번 (PK)      │         │ 학과코드 (PK)  │
│ 이름           │         │ 학과명         │
│ 학과 (FK) ─────┼────────►│ 위치           │
│ 학년           │         └────────────────┘
└────────────────┘
         참조 무결성: 학생.학과는 반드시 학과.학과코드에 존재
```

#### 3. 심층 동작 원리: 관계형 모델의 수학적 기반

**1단계: 릴레이션의 정의**

```text
[수학적 정의]
릴레이션 R은 도메인 D1, D2, ..., Dn의 카티션 프로덕트의 부분집합

R ⊆ D1 × D2 × ... × Dn

[예시]
D1 = {001, 002, 003}           // 학번 도메인
D2 = {홍길동, 김철수, 이영희}    // 이름 도메인
D3 = {1, 2, 3, 4}               // 학년 도메인

D1 × D2 × D3 = {(001,홍길동,1), (001,홍길동,2), ..., (003,이영희,4)}
                ↑ 총 3 × 3 × 4 = 36개 조합

R(학생) = {(001,홍길동,3), (002,김철수,2), (003,이영희,3)}
          ↑ 실제 존재하는 조합만 선택 (부분집합)
```

**2단계: 키의 종류와 특성**

```sql
-- 슈퍼 키 (Super Key): 유일성만 만족
-- 학생 테이블에서 가능한 슈퍼 키
-- {학번}, {학번, 이름}, {학번, 이름, 학과}, {주민번호} ...

-- 후보 키 (Candidate Key): 유일성 + 최소성
-- {학번}, {주민번호} - 더 이상 줄일 수 없음

-- 기본 키 (Primary Key): 후보 키 중 선택
CREATE TABLE students (
    student_id VARCHAR(10) PRIMARY KEY,  -- 기본 키
    name VARCHAR(50) NOT NULL,
    ssn VARCHAR(14) UNIQUE,              -- 대체 키
    dept_id VARCHAR(5),
    ...
);

-- 외래 키 (Foreign Key): 참조 무결성 보장
ALTER TABLE students
ADD CONSTRAINT fk_dept
FOREIGN KEY (dept_id) REFERENCES departments(dept_id);
```

**3단계: 무결성 제약조건**

```sql
-- 1. 개체 무결성 (Entity Integrity)
-- 기본 키는 NULL이거나 중복될 수 없음
CREATE TABLE students (
    student_id VARCHAR(10) PRIMARY KEY,  -- NOT NULL + UNIQUE
    ...
);

-- 2. 참조 무결성 (Referential Integrity)
-- 외래 키는 참조하는 기본 키 값이거나 NULL
ALTER TABLE enrollments
ADD CONSTRAINT fk_student
FOREIGN KEY (student_id)
    REFERENCES students(student_id)
    ON DELETE RESTRICT   -- 참조하는 데이터 있으면 삭제 불가
    ON UPDATE CASCADE;   -- 기본키 변경 시 외래키도 변경

-- 3. 도메인 무결성 (Domain Integrity)
-- 속성 값은 정의된 도메인에 속해야 함
CREATE TABLE students (
    ...
    year INT CHECK (year BETWEEN 1 AND 4),
    email VARCHAR(100) CHECK (email LIKE '%@%.%'),
    ...
);
```

#### 4. 실무 수준의 관계형 모델 구현

```python
"""
관계형 데이터 모델 Python 구현
릴레이션, 튜플, 제약조건 구현
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Set, Optional, Tuple
from enum import Enum

class ConstraintType(Enum):
    PRIMARY_KEY = "PRIMARY_KEY"
    FOREIGN_KEY = "FOREIGN_KEY"
    UNIQUE = "UNIQUE"
    NOT_NULL = "NOT_NULL"
    CHECK = "CHECK"

@dataclass
class Attribute:
    """속성 정의"""
    name: str
    data_type: str
    nullable: bool = True
    default: Any = None

@dataclass
class Constraint:
    """제약조건 정의"""
    name: str
    constraint_type: ConstraintType
    attributes: List[str]
    reference_table: Optional[str] = None
    reference_attrs: Optional[List[str]] = None
    check_condition: Optional[str] = None

@dataclass
class Relation:
    """릴레이션 정의"""
    name: str
    attributes: List[Attribute]
    constraints: List[Constraint] = field(default_factory=list)
    tuples: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def degree(self) -> int:
        """차수: 속성 개수"""
        return len(self.attributes)

    @property
    def cardinality(self) -> int:
        """카디널리티: 튜플 개수"""
        return len(self.tuples)

    @property
    def attribute_names(self) -> List[str]:
        """속성 이름 리스트"""
        return [attr.name for attr in self.attributes]

    @property
    def primary_key_attrs(self) -> List[str]:
        """기본키 속성"""
        for c in self.constraints:
            if c.constraint_type == ConstraintType.PRIMARY_KEY:
                return c.attributes
        return []

class RelationalDatabase:
    """관계형 데이터베이스 구현"""

    def __init__(self):
        self.relations: Dict[str, Relation] = {}

    # ==================== DDL ====================

    def create_table(self, name: str, attributes: List[Attribute],
                    constraints: List[Constraint] = None) -> None:
        """테이블 생성"""
        if name in self.relations:
            raise ValueError(f"테이블 '{name}' 이미 존재")

        relation = Relation(
            name=name,
            attributes=attributes,
            constraints=constraints or []
        )
        self.relations[name] = relation
        print(f"[DDL] 테이블 '{name}' 생성 (차수: {relation.degree})")

    def add_constraint(self, table_name: str, constraint: Constraint) -> None:
        """제약조건 추가"""
        if table_name not in self.relations:
            raise ValueError(f"테이블 '{table_name}' 없음")
        self.relations[table_name].constraints.append(constraint)
        print(f"[DDL] 제약조건 '{constraint.name}' 추가")

    # ==================== DML ====================

    def insert(self, table_name: str, tuple_data: Dict[str, Any]) -> bool:
        """튜플 삽입"""
        if table_name not in self.relations:
            raise ValueError(f"테이블 '{table_name}' 없음")

        relation = self.relations[table_name]

        # 1. 속성 검증
        for attr in relation.attributes:
            if attr.name not in tuple_data:
                if attr.default is not None:
                    tuple_data[attr.name] = attr.default
                elif not attr.nullable:
                    raise ValueError(f"속성 '{attr.name}'은 NULL 불가")

        # 2. 제약조건 검증
        self._validate_constraints(relation, tuple_data)

        # 3. 튜플 삽입
        relation.tuples.append(tuple_data)
        print(f"[DML] '{table_name}'에 튜플 삽입: {tuple_data}")
        return True

    def select(self, table_name: str,
              conditions: Dict[str, Any] = None,
              columns: List[str] = None) -> List[Dict[str, Any]]:
        """튜플 검색"""
        if table_name not in self.relations:
            raise ValueError(f"테이블 '{table_name}' 없음")

        relation = self.relations[table_name]

        # 조건 필터링
        result = relation.tuples
        if conditions:
            result = [
                t for t in result
                if all(t.get(k) == v for k, v in conditions.items())
            ]

        # 칼럼 프로젝션
        if columns:
            result = [
                {k: v for k, v in t.items() if k in columns}
                for t in result
            ]

        print(f"[DML] '{table_name}'에서 {len(result)}개 튜플 검색")
        return result

    def update(self, table_name: str,
              new_values: Dict[str, Any],
              conditions: Dict[str, Any]) -> int:
        """튜플 수정"""
        if table_name not in self.relations:
            raise ValueError(f"테이블 '{table_name}' 없음")

        relation = self.relations[table_name]
        count = 0

        for t in relation.tuples:
            if all(t.get(k) == v for k, v in conditions.items()):
                t.update(new_values)
                count += 1

        print(f"[DML] '{table_name}'에서 {count}개 튜플 수정")
        return count

    def delete(self, table_name: str, conditions: Dict[str, Any]) -> int:
        """튜플 삭제"""
        if table_name not in self.relations:
            raise ValueError(f"테이블 '{table_name}' 없음")

        relation = self.relations[table_name]
        original_count = len(relation.tuples)

        relation.tuples = [
            t for t in relation.tuples
            if not all(t.get(k) == v for k, v in conditions.items())
        ]

        deleted = original_count - len(relation.tuples)
        print(f"[DML] '{table_name}'에서 {deleted}개 튜플 삭제")
        return deleted

    # ==================== 무결성 검증 ====================

    def _validate_constraints(self, relation: Relation,
                            tuple_data: Dict[str, Any]) -> None:
        """제약조건 검증"""
        for constraint in relation.constraints:
            if constraint.constraint_type == ConstraintType.PRIMARY_KEY:
                self._check_primary_key(relation, tuple_data, constraint)
            elif constraint.constraint_type == ConstraintType.FOREIGN_KEY:
                self._check_foreign_key(tuple_data, constraint)
            elif constraint.constraint_type == ConstraintType.UNIQUE:
                self._check_unique(relation, tuple_data, constraint)
            elif constraint.constraint_type == ConstraintType.NOT_NULL:
                self._check_not_null(tuple_data, constraint)

    def _check_primary_key(self, relation: Relation,
                          tuple_data: Dict[str, Any],
                          constraint: Constraint) -> None:
        """기본키 제약 검증"""
        pk_values = tuple(tuple_data.get(attr) for attr in constraint.attributes)

        # NULL 검사
        if None in pk_values:
            raise ValueError(f"기본키 {constraint.attributes}은 NULL 불가")

        # 중복 검사
        for existing in relation.tuples:
            existing_pk = tuple(existing.get(attr) for attr in constraint.attributes)
            if existing_pk == pk_values:
                raise ValueError(f"기본키 {pk_values} 중복")

    def _check_foreign_key(self, tuple_data: Dict[str, Any],
                          constraint: Constraint) -> None:
        """외래키 제약 검증"""
        fk_values = [tuple_data.get(attr) for attr in constraint.attributes]

        # NULL이면 통과
        if all(v is None for v in fk_values):
            return

        # 참조 테이블 확인
        ref_table = self.relations.get(constraint.reference_table)
        if not ref_table:
            raise ValueError(f"참조 테이블 '{constraint.reference_table}' 없음")

        # 참조 값 존재 확인
        found = False
        for t in ref_table.tuples:
            ref_values = [t.get(attr) for attr in constraint.reference_attrs]
            if fk_values == ref_values:
                found = True
                break

        if not found:
            raise ValueError(
                f"참조 무결성 위반: {fk_values}이 "
                f"'{constraint.reference_table}'에 없음"
            )

    def _check_unique(self, relation: Relation,
                     tuple_data: Dict[str, Any],
                     constraint: Constraint) -> None:
        """유니크 제약 검증"""
        values = tuple(tuple_data.get(attr) for attr in constraint.attributes)

        for existing in relation.tuples:
            existing_values = tuple(existing.get(attr) for attr in constraint.attributes)
            if existing_values == values:
                raise ValueError(f"유니크 제약 위반: {values} 중복")

    def _check_not_null(self, tuple_data: Dict[str, Any],
                       constraint: Constraint) -> None:
        """NOT NULL 제약 검증"""
        for attr in constraint.attributes:
            if tuple_data.get(attr) is None:
                raise ValueError(f"속성 '{attr}'은 NULL 불가")

# ==================== 사용 예시 ====================
if __name__ == "__main__":
    db = RelationalDatabase()

    # 1. 부서 테이블 생성
    db.create_table(
        name="departments",
        attributes=[
            Attribute("dept_id", "VARCHAR(5)", nullable=False),
            Attribute("dept_name", "VARCHAR(50)", nullable=False),
            Attribute("location", "VARCHAR(100)"),
        ],
        constraints=[
            Constraint("pk_dept", ConstraintType.PRIMARY_KEY, ["dept_id"]),
        ]
    )

    # 2. 학생 테이블 생성
    db.create_table(
        name="students",
        attributes=[
            Attribute("student_id", "VARCHAR(10)", nullable=False),
            Attribute("name", "VARCHAR(50)", nullable=False),
            Attribute("dept_id", "VARCHAR(5)"),
            Attribute("year", "INT", default=1),
        ],
        constraints=[
            Constraint("pk_student", ConstraintType.PRIMARY_KEY, ["student_id"]),
            Constraint("fk_student_dept", ConstraintType.FOREIGN_KEY,
                      ["dept_id"], "departments", ["dept_id"]),
        ]
    )

    # 3. 데이터 삽입
    db.insert("departments", {"dept_id": "D01", "dept_name": "컴퓨터공학과"})
    db.insert("departments", {"dept_id": "D02", "dept_name": "경영학과"})

    db.insert("students", {"student_id": "001", "name": "홍길동", "dept_id": "D01", "year": 3})
    db.insert("students", {"student_id": "002", "name": "김철수", "dept_id": "D01", "year": 2})

    # 4. 제약조건 위반 테스트
    try:
        db.insert("students", {"student_id": "001", "name": "중복학생"})  # PK 중복
    except ValueError as e:
        print(f"[제약조건] {e}")

    try:
        db.insert("students", {"student_id": "003", "name": "학과없음", "dept_id": "D99"})  # FK 위반
    except ValueError as e:
        print(f"[제약조건] {e}")

    # 5. 검색
    print("\n=== 컴공 학생 검색 ===")
    results = db.select("students", {"dept_id": "D01"})
    for r in results:
        print(f"  {r}")

    # 6. 통계
    print(f"\n학생 테이블 카디널리티: {db.relations['students'].cardinality}")
    print(f"학생 테이블 차수: {db.relations['students'].degree}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 데이터 모델 비교

| 비교 항목 | 계층형 | 망형 | 관계형 |
|:---|:---|:---|:---|
| **구조** | 트리 | 그래프 | 테이블 |
| **관계** | 1:N | M:N (SET) | M:N (FK) |
| **질의** | 네비게이션 | 네비게이션 | SQL (선언적) |
| **독립성** | 낮음 | 낮음 | 높음 |
| **복잡도** | 낮음 | 높음 | 중간 |
| **표준** | IBM IMS | CODASYL | ANSI SQL |

#### 2. 관계형 모델의 장단점

| 장점 | 단점 |
|:---|:---|
| 데이터 독립성 | 복잡한 객체 표현 어려움 |
| 선언적 질의(SQL) | 성능 튜닝 복잡 |
| 무결성 보장 | 객체-관계 임피던스 불일치 |
| 수학적 기반 | 수평 확장성 제한 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: RDBMS vs NoSQL 선택**
- 상황: 신규 서비스 DB 선택
- 판단: 데이터 특성과 질의 패턴 분석
- 전략:
  - 트랜잭션 중심 → RDBMS
  - 대량 로그/문서 → NoSQL
  - 혼합 → Polyglot Persistence

**시나리오 2: 정규화 vs 반정규화**
- 상황: 성능 이슈 발생
- 판단: 정규화는 무결성, 반정규화는 성능
- 전략: 기본 정규화, 핫스팟만 반정규화

#### 2. 안티패턴 (Anti-patterns)
- **God Table**: 과도한 칼럼 → 성능 저하
- **No Primary Key**: 기본키 없음 → 무결성 위반
- **Over-Join**: 과도한 조인 → 복잡도 증가

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과
- 데이터 무결성 99.9% 보장
- SQL 표준화로 생산성 향상
- 수학적 기반으로 이론적 안정성

#### 2. 미래 전망
- **NewSQL**: 관계형 + 수평 확장성
- **HTAP**: OLTP + OLAP 통합
- **Multi-model**: 관계형 + 문서형 + 그래프

#### 3. 참고 표준
- **E.F. Codd (1970)**: 관계형 모델 제안
- **ANSI SQL**: 관계형 질의어 표준

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[정규화](@/studynotes/05_database/01_relational/normalization.md)**: 관계형 설계 원칙
- **[SQL](@/studynotes/05_database/03_optimization/query_optimization.md)**: 관계형 질의어
- **[ER 모델](@/studynotes/05_database/01_relational/er_model.md)**: 개념적 모델링
- **[무결성](@/studynotes/05_database/01_relational/acid.md)**: 데이터 일관성 보장

---

### 👶 어린이를 위한 3줄 비유 설명
1. **표로 정리하기**: 엑셀처럼 표에 데이터를 정리해요. 행은 사람 하나하나, 열은 이름, 나이 같은 정보예요!
2. **수학으로 표현**: 관계형 모델은 수학자가 만들어서 수학 공식처럼 깔끔해요. 집합, 곱집합 같은 걸로 데이터를 설명해요!
3. **질문만 하면 돼요**: "3학년 학생 이름 알려줘!"라고만 말하면 돼요. 어떻게 찾는지는 몰라도 DB가 알아서 찾아줘요!
