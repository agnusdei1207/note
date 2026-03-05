+++
title = "망형 데이터 모델 (Network Model)"
date = "2026-03-04"
[extra]
categories = "studynotes-database"
+++

# 망형 데이터 모델 (Network Model)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 망형 데이터 모델은 데이터를 그래프 구조로 표현하는 데이터베이스 모델로, M:N 관계를 허용하며, CODASYL DBTG가 1969년 표준화하여 계층형 모델의 한계를 극복했습니다.
> 2. **가치**: 복잡한 다대다 관계를 자연스럽게 표현할 수 있어, 항공 예약, 재고 관리 등 복잡한 비즈니스 데이터 모델링에서 활용되며, 조회 성능은 계층형 대비 2-3배 향상됩니다.
> 3. **융합**: 망형 모델은 그래프 데이터베이스(Neo4j)와 객체지향 DB의 선조이며, 현대 ERD의 다대다 관계 표현의 이론적 기반이 됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**망형 데이터 모델(Network Model)**은 데이터를 레코드 타입과 링크로 구성된 그래프 구조로 표현하는 데이터베이스 모델입니다. 1969년 CODASYL(Conference on Data Systems Languages) DBTG(Data Base Task Group)가 표준화했습니다.

**핵심 특징**:
- **그래프 구조**: 레코드 간의 다대다(M:N) 관계 허용
- **SET 타입**: 두 레코드 타입 간의 1:N 관계 정의
- **소유자-멤버**: SET에서 부모를 소유자(Owner), 자식을 멤버(Member)라 함
- **다중 부모**: 한 레코드가 여러 SET의 멤버가 될 수 있음
- **네비게이션**: 프로그래머가 경로를 명시하여 데이터 접근

**계층형과의 차이점**:
```
계층형: 하나의 부모만 가능 (1:N, 트리)
망형:  여러 부모 가능 (M:N, 그래프)
```

#### 2. 💡 비유를 통한 이해
**대학 수강 시스템**으로 비유할 수 있습니다:

```
[계층형으로는 표현 어려움]
학생 --(수강)--> 과목
      ↑
      └-- 한 학생이 여러 과목, 한 과목에 여러 학생 = M:N

[망형으로 표현]
         [학생1] ─────┐
            │        │
         [학생2] ───┼──→ [수강] ──→ [과목1]
            │        │        │
         [학생3] ───┼────────┘    [과목2]
                       │
                       └────────→ [과목3]

SET 1: 학생-수강 (1:N)
SET 2: 과목-수강 (1:N)
```

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계**: 계층형 모델은 M:N 관계를 표현하지 못해, 학생-과목, 공급자-부품 같은 복잡한 관계를 데이터 중복으로 해결해야 했습니다.
2. **혁신적 패러다임의 도입**: 1969년 CODASYL DBTG가 망형 모델을 표준화했고, IDMS, Raima Database Manager 등 상용 시스템이 등장했습니다. Charles Bachman이 망형 모델의 선구자로 1973년 튜링상을 수상했습니다.
3. **비즈니스적 요구사항**: 항공 예약 시스템, 도서관 관리, 재고 관리 등 복잡한 관계를 가진 시스템에서 활용되었으나, 현재는 관계형 DB와 그래프 DB로 대체되었습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 망형 모델 구성 요소 (표)

| 구성 요소 | 정의 | 특성 | 예시 | 비고 |
|:---|:---|:---|:---|:---|
| **레코드 타입(Record Type)** | 데이터 저장 단위 | 필드들의 집합 | 학생, 과목 | 테이블과 유사 |
| **필드(Field)** | 데이터 항목 | 원자값 | 학번, 과목코드 | 칼럼과 유사 |
| **SET 타입** | 레코드 간 관계 | 1:N 명명된 관계 | 학생-수강, 과목-수강 | 관계와 유사 |
| **소유자(Owner)** | SET의 부모 측 | 1:N의 1 | 학생, 과목 | 부모와 유사 |
| **멤버(Member)** | SET의 자식 측 | 1:N의 N | 수강 | 자식과 유사 |
| **링크(Link/Pointer)** | 물리적 연결 | 레코드 간 포인터 | NEXT, PRIOR | |

#### 2. 망형 데이터 모델 구조 다이어그램

```text
+=====================================================================+
|                    [ 망형 데이터 모델 구조 ]                         |
+=====================================================================+

[예시: 학생-과목 수강 시스템 (M:N 관계)]

    [학생 레코드 타입]                    [과목 레코드 타입]
    +---------------+                    +---------------+
    | 학번 (PK)     |                    | 과목코드 (PK) |
    | 이름          |                    | 과목명        |
    | 학과          |                    | 학점          |
    +---------------+                    +---------------+
           │                                    │
           │ SET: 학생-수강                     │ SET: 과목-수강
           │ (Owner: 학생, Member: 수강)       │ (Owner: 과목, Member: 수강)
           │                                    │
           └──────────┐            ┌───────────┘
                      │            │
                      ▼            ▼
              [수강 레코드 타입] ←────── 연결 레코드 (Junction)
              +-------------------+
              | 학번 (FK)         | ← 학생 SET의 멤버
              | 과목코드 (FK)     | ← 과목 SET의 멤버
              | 성적              |
              | NEXT_STUDENT ptr  | → 다음 수강 (같은 학생)
              | NEXT_COURSE ptr   | → 다음 수강 (같은 과목)
              +-------------------+

[데이터 구조 예시]

학생 S001 ─────┐
               │
               ├──── 수강1 (S001, C101, A) ─────┐
               │         │                      │
               │         └── NEXT_COURSE ───────┼──→ 과목 C101
               │                                │
               └──── 수강2 (S001, C102, B+) ────┘
                         │
                         └── NEXT_COURSE ───────────→ 과목 C102

학생 S002 ─────┐
               │
               └──── 수강3 (S002, C101, B) ──────→ 과목 C101 (위와 공유)

[SET 순회 방식]
1. 학생 S001에서 시작
2. 학생-수강 SET을 통해 수강1 이동
3. NEXT_STUDENT로 수강2 이동 (같은 학생의 다음 수강)
4. 과목-수강 SET을 통해 과목 C101 이동
```

#### 3. 심층 동작 원리: CODASYL DDL/DML

**1단계: 스키마 정의 (DDL)**

```cobol
* CODASYL Schema Definition Example
SCHEMA NAME IS UNIVERSITY.

* 학생 레코드 타입
RECORD NAME IS STUDENT;
    STUDENT_ID; TYPE IS CHARACTER 8;
    STUDENT_NAME; TYPE IS CHARACTER 20;
    DEPARTMENT; TYPE IS CHARACTER 30.
KEY STUDENT_KEY IS STUDENT_ID;
    DUPLICATES ARE NOT ALLOWED.

* 과목 레코드 타입
RECORD NAME IS COURSE;
    COURSE_ID; TYPE IS CHARACTER 6;
    COURSE_NAME; TYPE IS CHARACTER 40;
    CREDITS; TYPE IS INTEGER.
KEY COURSE_KEY IS COURSE_ID;
    DUPLICATES ARE NOT ALLOWED.

* 수강 레코드 타입 (연결 엔티티)
RECORD NAME IS ENROLLMENT;
    GRADE; TYPE IS CHARACTER 2.

* SET 정의: 학생-수강
SET NAME IS STUDENT-ENROLL;
    OWNER IS STUDENT;
    MEMBER IS ENROLLMENT;
    ORDER IS SORTED BY DEFINED KEYS;
    KEY IS ASCENDING STUDENT_ID;
    SET MODE IS CHAIN;
    LINK IS PRIOR TO NEXT;

* SET 정의: 과목-수강
SET NAME IS COURSE-ENROLL;
    OWNER IS COURSE;
    MEMBER IS ENROLLMENT;
    ORDER IS LAST;
    SET MODE IS CHAIN;
    LINK IS NEXT.
```

**2단계: 데이터 조작 (DML)**

```cobol
* CODASYL DML Operations

* 1. 레코드 저장 (STORE)
MOVE 'S001' TO STUDENT_ID.
MOVE '홍길동' TO STUDENT_NAME.
MOVE '컴퓨터공학' TO DEPARTMENT.
STORE STUDENT.

* 2. SET 연결 (CONNECT)
* 수강 레코드를 학생-수강 SET에 연결
MOVE 'A' TO GRADE.
STORE ENROLLMENT.
CONNECT ENROLLMENT TO STUDENT-ENROLL.
CONNECT ENROLLMENT TO COURSE-ENROLL.

* 3. SET 순회 (FIND)
* 학생 S001의 첫 번째 수강 찾기
MOVE 'S001' TO STUDENT_ID.
FIND ANY STUDENT USING STUDENT_ID.
FIND FIRST ENROLLMENT WITHIN STUDENT-ENROLLMENT.

* 4. 다음 레코드 찾기
FIND NEXT ENROLLMENT WITHIN STUDENT-ENROLLMENT.

* 5. 소유자 찾기 (逆방향)
FIND OWNER WITHIN COURSE-ENROLLMENT.

* 6. SET 연결 해제 (DISCONNECT)
DISCONNECT ENROLLMENT FROM STUDENT-ENROLLMENT.

* 7. 레코드 삭제 (ERASE)
ERASE ENROLLMENT.
```

**3단계: 현대적 구현 (SQL로의 변환)**

```sql
-- 망형 모델의 SET을 관계형으로 변환

-- 레코드 타입 → 테이블
CREATE TABLE students (
    student_id VARCHAR(8) PRIMARY KEY,
    student_name VARCHAR(20),
    department VARCHAR(30)
);

CREATE TABLE courses (
    course_id VARCHAR(6) PRIMARY KEY,
    course_name VARCHAR(40),
    credits INT
);

-- SET 관계 → 교차 테이블 (연결 엔티티)
CREATE TABLE enrollments (
    student_id VARCHAR(8),
    course_id VARCHAR(6),
    grade VARCHAR(2),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- SET 순회 → JOIN 쿼리
-- 학생-수강 SET 순회
SELECT e.*
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
WHERE s.student_id = 'S001';

-- 과목-수강 SET 순회
SELECT e.*
FROM courses c
JOIN enrollments e ON c.course_id = e.course_id
WHERE c.course_id = 'C101';

-- 양방향 탐색 (망형의 이점)
SELECT s.student_name, c.course_name, e.grade
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id;
```

#### 4. 실무 수준의 망형 모델 구현

```python
"""
망형 데이터 모델 구현 (현대적 Python 버전)
CODASYL DBTG 스타일의 SET 기반 관계 관리
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set as TypingSet
from enum import Enum

class SetOrder(Enum):
    """SET 순서 정의"""
    FIRST = "FIRST"      # 새 멤버를 첫 번째에
    LAST = "LAST"        # 새 멤버를 마지막에
    NEXT = "NEXT"        # 현재 위치 다음에
    PRIOR = "PRIOR"      # 현재 위치 이전에
    SORTED = "SORTED"    # 정렬된 순서

@dataclass
class Record:
    """망형 모델의 레코드"""
    record_type: str
    fields: Dict[str, Any] = field(default_factory=dict)
    # SET 멤버십: {set_name: (owner_record, next_member, prior_member)}
    set_memberships: Dict[str, Dict] = field(default_factory=dict)

    @property
    def db_key(self) -> str:
        """레코드 식별 키"""
        return f"{self.record_type}:{id(self)}"

@dataclass
class SetType:
    """SET 타입 정의"""
    name: str
    owner_type: str
    member_type: str
    order: SetOrder = SetOrder.LAST

@dataclass
class SetOccurrence:
    """SET 발생 (실제 관계 인스턴스)"""
    set_type: SetType
    owner: Record
    members: List[Record] = field(default_factory=list)

    def add_member(self, member: Record) -> None:
        """멤버 추가"""
        if self.set_type.order == SetOrder.FIRST:
            self.members.insert(0, member)
        else:  # LAST
            self.members.append(member)

        # 멤버의 SET 멤버십 업데이트
        member.set_memberships[self.set_type.name] = {
            'owner': self.owner,
            'position': len(self.members) - 1
        }

    def remove_member(self, member: Record) -> None:
        """멤버 제거"""
        if member in self.members:
            self.members.remove(member)
            if self.set_type.name in member.set_memberships:
                del member.set_memberships[self.set_type.name]

    def get_first(self) -> Optional[Record]:
        """첫 번째 멤버 반환"""
        return self.members[0] if self.members else None

    def get_next(self, current: Record) -> Optional[Record]:
        """다음 멤버 반환"""
        try:
            idx = self.members.index(current)
            return self.members[idx + 1] if idx + 1 < len(self.members) else None
        except ValueError:
            return None

class NetworkDatabase:
    """망형 데이터베이스 구현"""

    def __init__(self, name: str):
        self.name = name
        self.record_types: Dict[str, List[Record]] = {}
        self.set_types: Dict[str, SetType] = {}
        self.set_occurrences: Dict[str, List[SetOccurrence]] = {}

    # ==================== 스키마 정의 (DDL) ====================

    def define_record_type(self, type_name: str) -> None:
        """레코드 타입 정의"""
        self.record_types[type_name] = []
        print(f"[Schema] 레코드 타입 정의: {type_name}")

    def define_set_type(self, name: str, owner_type: str,
                       member_type: str, order: SetOrder = SetOrder.LAST) -> None:
        """SET 타입 정의"""
        set_type = SetType(name, owner_type, member_type, order)
        self.set_types[name] = set_type
        self.set_occurrences[name] = []
        print(f"[Schema] SET 타입 정의: {name} ({owner_type} → {member_type})")

    # ==================== 데이터 조작 (DML) ====================

    def create_record(self, record_type: str, fields: Dict[str, Any]) -> Record:
        """레코드 생성 (STORE)"""
        if record_type not in self.record_types:
            raise ValueError(f"알 수 없는 레코드 타입: {record_type}")

        record = Record(record_type=record_type, fields=fields)
        self.record_types[record_type].append(record)
        print(f"[DML] 레코드 생성: {record_type} - {fields}")
        return record

    def connect_to_set(self, set_name: str,
                      owner: Record, member: Record) -> None:
        """SET에 멤버 연결 (CONNECT)"""
        if set_name not in self.set_types:
            raise ValueError(f"알 수 없는 SET 타입: {set_name}")

        set_type = self.set_types[set_name]

        # 해당 owner의 SET occurrence 찾기 또는 생성
        occurrence = self._find_or_create_occurrence(set_type, owner)
        occurrence.add_member(member)
        print(f"[DML] SET 연결: {set_name} ({owner.fields} → {member.fields})")

    def disconnect_from_set(self, set_name: str, member: Record) -> None:
        """SET에서 멤버 연결 해제 (DISCONNECT)"""
        if set_name not in member.set_memberships:
            return

        owner = member.set_memberships[set_name]['owner']
        occurrence = self._find_occurrence(set_name, owner)
        if occurrence:
            occurrence.remove_member(member)
        print(f"[DML] SET 연결 해제: {set_name}")

    # ==================== 네비게이션 (FIND) ====================

    def find_record(self, record_type: str,
                   key_field: str, key_value: Any) -> Optional[Record]:
        """레코드 찾기 (FIND ANY)"""
        for record in self.record_types.get(record_type, []):
            if record.fields.get(key_field) == key_value:
                return record
        return None

    def find_first_in_set(self, set_name: str, owner: Record) -> Optional[Record]:
        """SET의 첫 번째 멤버 찾기 (FIND FIRST WITHIN)"""
        occurrence = self._find_occurrence(set_name, owner)
        return occurrence.get_first() if occurrence else None

    def find_next_in_set(self, set_name: str,
                        current: Record) -> Optional[Record]:
        """SET의 다음 멤버 찾기 (FIND NEXT WITHIN)"""
        if set_name not in current.set_memberships:
            return None

        owner = current.set_memberships[set_name]['owner']
        occurrence = self._find_occurrence(set_name, owner)
        return occurrence.get_next(current) if occurrence else None

    def find_owner(self, set_name: str, member: Record) -> Optional[Record]:
        """SET의 소유자 찾기 (FIND OWNER WITHIN)"""
        if set_name in member.set_memberships:
            return member.set_memberships[set_name]['owner']
        return None

    # ==================== 내부 메서드 ====================

    def _find_occurrence(self, set_name: str,
                        owner: Record) -> Optional[SetOccurrence]:
        """SET occurrence 찾기"""
        for occ in self.set_occurrences.get(set_name, []):
            if occ.owner == owner:
                return occ
        return None

    def _find_or_create_occurrence(self, set_type: SetType,
                                   owner: Record) -> SetOccurrence:
        """SET occurrence 찾기 또는 생성"""
        occurrence = self._find_occurrence(set_type.name, owner)
        if not occurrence:
            occurrence = SetOccurrence(set_type, owner)
            self.set_occurrences[set_type.name].append(occurrence)
        return occurrence

    # ==================== 분석 메서드 ====================

    def get_set_statistics(self) -> Dict[str, Any]:
        """SET 통계"""
        stats = {}
        for set_name, occurrences in self.set_occurrences.items():
            total_members = sum(len(occ.members) for occ in occurrences)
            stats[set_name] = {
                'occurrences': len(occurrences),
                'total_members': total_members,
                'avg_members': total_members / len(occurrences) if occurrences else 0
            }
        return stats

# ==================== 사용 예시 ====================
if __name__ == "__main__":
    # 망형 데이터베이스 생성
    db = NetworkDatabase("UniversityDB")

    # 1. 스키마 정의 (DDL)
    db.define_record_type("STUDENT")
    db.define_record_type("COURSE")
    db.define_record_type("ENROLLMENT")

    db.define_set_type("STUDENT-ENROLL", "STUDENT", "ENROLLMENT")
    db.define_set_type("COURSE-ENROLL", "COURSE", "ENROLLMENT")

    # 2. 레코드 생성 (STORE)
    student1 = db.create_record("STUDENT",
        {"student_id": "S001", "name": "홍길동", "dept": "컴공"})
    student2 = db.create_record("STUDENT",
        {"student_id": "S002", "name": "김철수", "dept": "경영"})

    course1 = db.create_record("COURSE",
        {"course_id": "C101", "name": "데이터베이스", "credits": 3})
    course2 = db.create_record("COURSE",
        {"course_id": "C102", "name": "알고리즘", "credits": 3})

    # 3. 수강(연결 레코드) 생성 및 SET 연결 (CONNECT)
    # S001 → C101
    enroll1 = db.create_record("ENROLLMENT", {"grade": "A"})
    db.connect_to_set("STUDENT-ENROLL", student1, enroll1)
    db.connect_to_set("COURSE-ENROLL", course1, enroll1)

    # S001 → C102
    enroll2 = db.create_record("ENROLLMENT", {"grade": "B+"})
    db.connect_to_set("STUDENT-ENROLL", student1, enroll2)
    db.connect_to_set("COURSE-ENROLL", course2, enroll2)

    # S002 → C101
    enroll3 = db.create_record("ENROLLMENT", {"grade": "B"})
    db.connect_to_set("STUDENT-ENROLL", student2, enroll3)
    db.connect_to_set("COURSE-ENROLL", course1, enroll3)

    # 4. 네비게이션 (FIND)
    print("\n=== 네비게이션 테스트 ===")

    # 학생 S001의 첫 번째 수강 찾기
    first_enroll = db.find_first_in_set("STUDENT-ENROLL", student1)
    print(f"S001의 첫 번째 수강: {first_enroll.fields if first_enroll else 'None'}")

    # 다음 수강 찾기
    next_enroll = db.find_next_in_set("STUDENT-ENROLL", first_enroll)
    print(f"S001의 다음 수강: {next_enroll.fields if next_enroll else 'None'}")

    # 수강의 과목(소유자) 찾기
    course = db.find_owner("COURSE-ENROLL", first_enroll)
    print(f"첫 번째 수강의 과목: {course.fields if course else 'None'}")

    # 5. SET 통계
    print("\n=== SET 통계 ===")
    print(db.get_set_statistics())
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 계층형 vs 망형 vs 관계형 모델 비교

| 비교 항목 | 계층형 | 망형 | 관계형 |
|:---|:---|:---|:---|
| **구조** | 트리 | 그래프 | 테이블 |
| **관계** | 1:N만 | 1:N (여러 SET로 M:N) | M:N 자유로움 |
| **다중 부모** | 불가능 | 가능 | 가능 (FK) |
| **데이터 접근** | 네비게이션 | 네비게이션 | SQL (선언적) |
| **복잡도** | 낮음 | 높음 | 중간 |
| **유연성** | 낮음 | 중간 | 높음 |
| **표준화** | IBM IMS | CODASYL DBTG | ANSI SQL |

#### 2. 망형 모델의 장단점

| 장점 | 단점 |
|:---|:---|
| M:N 관계 표현 가능 | 높은 프로그래밍 복잡도 |
| 데이터 중복 감소 | 네비게이션 경로 명시 필요 |
| 빠른 조회 (포인터) | 구조 변경 어려움 |
| 명확한 관계 정의 | 학습 곡선 가파름 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 망형에서 관계형 마이그레이션**
- 상황: IDMS 레거시 → Oracle 마이그레이션
- 판단: SET을 외래키로 변환
- 전략:
  1. 레코드 타입 → 테이블
  2. SET → 외래키 관계
  3. 연결 레코드 → 교차 테이블

**시나리오 2: 그래프 데이터베이스 도입**
- 상황: 복잡한 네트워크 관계 분석 필요
- 판단: 망형 모델의 현대적 계승인 그래프 DB 적합
- 전략: Neo4j 등 그래프 DB로 이동

#### 2. 안티패턴 (Anti-patterns)
- **과도한 SET**: 너무 많은 SET → 복잡도 폭증
- **잦은 구조 변경**: SET 정의 변경 → 전체 재구성

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과
- M:N 관계 자연스러운 표현
- 포인터 기반 빠른 조회
- 데이터 중복 최소화

#### 2. 미래 전망
- **그래프 데이터베이스**: 망형의 현대적 계승
- **지식 그래프**: 복잡한 관계 표현에 활용

#### 3. 참고 표준
- **CODASYL DBTG 1969**: 망형 모델 표준
- **Charles Bachman**: 튜링상 1973 (망형 모델 공헌)

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[계층형 모델](@/studynotes/05_database/01_relational/hierarchical_model.md)**: 망형의 전신
- **[관계형 모델](@/studynotes/05_database/01_relational/relational_model.md)**: 망형의 후계자
- **[그래프 DB](@/studynotes/05_database/01_relational/nosql.md)**: 망형의 현대적 계승
- **[M:N 관계](@/studynotes/05_database/01_relational/er_model.md)**: 망형의 핵심 이점

---

### 👶 어린이를 위한 3줄 비유 설명
1. **친구 관계**: 나는 여러 명의 친구가 있고, 각 친구도 다른 친구들이 있어요. 한 명이 여러 명과 연결될 수 있는 거예요. 이게 망형이에요!
2. **지하철 노선도**: 한 역에서 여러 노선을 탈 수 있고, 한 노선도 여러 역을 지나가죠? 모든 것이 서로 연결된 그물처럼 되어 있어요!
3. **여행 경로**: 서울에서 부산 갈 때, 대전을 거치거나 대구를 거칠 수 있어요. 여러 가지 경로가 있고, 어떤 도시는 여러 경로에서 공통으로 지나가기도 하죠!
