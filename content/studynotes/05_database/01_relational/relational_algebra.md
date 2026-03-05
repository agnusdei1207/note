+++
title = "관계 대수 (Relational Algebra) - 절차적 언어"
date = "2026-03-04"
[extra]
categories = "studynotes-database"
+++

# 관계 대수 (Relational Algebra)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 관계 대수는 관계형 데이터베이스에서 데이터를 조작하기 위한 절차적 언어로, '어떻게' 결과를 얻을지 명시하는 수학적 연산 체계입니다.
> 2. **가치**: 관계 대수는 SQL 옵티마이저의 실행 계획 기반이며, 8개의 기본 연산자로 모든 질의를 표현할 수 있어 쿼리 최적화의 이론적 토대입니다.
> 3. **융합**: 관계 대수는 관계 해석(비절차적)과 동등한 표현력을 가지며, 현대 SQL의 SELECT, JOIN, WHERE 절이 이에 대응됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**관계 대수(Relational Algebra)**는 E.F. Codd가 1970년 관계형 모델과 함께 제안한 데이터 조작 언어로, 릴레이션(Relation)을 입력으로 받아 새로운 릴레이션을 출력하는 연산자들의 집합입니다.

**핵심 특성**:
- **절차적(Procedural)**: 결과를 얻기 위한 연산 순서를 명시
- **폐쇄성(Closure)**: 연산 결과도 릴레이션
- **수학적 기반**: 집합론과 술어 논리에 기반
- **완전성**: 8개 기본 연산자로 모든 질의 표현 가능

**관계 대수 연산자 분류**:
1. **일반 집합 연산자**: 합집합(∪), 교집합(∩), 차집합(-), 카티션 프로덕트(×)
2. **순수 관계 연산자**: 셀렉트(σ), 프로젝트(π), 조인(⋈), 디비전(÷)

#### 2. 💡 비유를 통한 이해
**요리 레시피**로 비유할 수 있습니다:

```
[절차적 - 관계 대수]
요리 과정을 단계별로 명시:
1. 냉장고에서 달걀을 꺼내고 (SELECT)
2. 달걀의 노른자만 분리하고 (PROJECT)
3. 밀가루와 섞어서 (JOIN)
4. 반죽을 오븐에 넣어 구우세요 (결과)

[비절차적 - 관계 해석/SQL]
무엇을 원하는지만 말함:
"케이크가 먹고 싶어요!"
(어떻게 만드는지는 몰라도 됨)
```

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계**: 계층형/망형 모델은 네비게이션 기반이라 질의 방법이 DB 구조에 종속되었습니다. 데이터 독립성이 없었습니다.
2. **혁신적 패러다임의 도입**: 1970년 E.F. Codd가 관계형 모델과 함께 관계 대수/관계 해석을 제안했습니다. 이는 데이터 조작의 수학적 기반을 제공했습니다.
3. **비즈니스적 요구사항**: SQL 옵티마이저는 관계 대수를 기반으로 쿼리를 변환하고 최적화합니다. 개발자는 비절차적 SQL을 쓰지만, DBMS는 내부적으로 관계 대수로 변환합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 관계 대수 연산자 상세 (표)

| 연산자 | 기호 | 정의 | 입력 | 출력 | SQL 대응 |
|:---|:---|:---|:---|:---|:---|
| **셀렉트** | σ | 조건 만족 튜플 선택 | 1개 릴레이션 | 릴레이션 | WHERE |
| **프로젝트** | π | 지정 속성만 추출 | 1개 릴레이션 | 릴레이션 | SELECT col |
| **합집합** | ∪ | 중복 제거 합침 | 2개 릴레이션 | 릴레이션 | UNION |
| **차집합** | - | R에만 있는 튜플 | 2개 릴레이션 | 릴레이션 | MINUS/EXCEPT |
| **교집합** | ∩ | 양쪽 모두 있는 튜플 | 2개 릴레이션 | 릴레이션 | INTERSECT |
| **카티션** | × | 모든 조합 | 2개 릴레이션 | 릴레이션 | CROSS JOIN |
| **조인** | ⋈ | 공통 속성으로 결합 | 2개 릴레이션 | 릴레이션 | JOIN |
| **디비전** | ÷ | 모든 값 포함 튜플 | 2개 릴레이션 | 릴레이션 | NOT EXISTS |

#### 2. 관계 대수 연산자 다이어그램

```text
+====================================================================+
|                    [ 관계 대수 연산자 체계 ]                        |
+====================================================================+

[일반 집합 연산자] - 2개 릴레이션 필요, 호환성 조건
+------------------------+
|   R ∪ S   (합집합)     |  R의 모든 튜플 + S의 모든 튜플 (중복 제거)
+------------------------+
|   R ∩ S   (교집합)     |  R과 S에 모두 있는 튜플
+------------------------+
|   R - S   (차집합)     |  R에만 있는 튜플
+------------------------+
|   R × S   (카티션)     |  R의 각 튜플 × S의 각 튜플
+------------------------+

[순수 관계 연산자] - 관계형 모델 고유
+------------------------+
|  σ_조건(R) (셀렉트)    |  조건을 만족하는 튜플만 (수평)
+------------------------+
|  π_속성(R) (프로젝트)  |  지정 속성만 (수직)
+------------------------+
|  R ⋈ S   (조인)        |  공통 속성 기준 결합
+------------------------+
|  R ÷ S   (디비전)      |  S의 모든 속성 값과 매칭되는 R의 튜플
+------------------------+

[연산 예시]

R (학생)                    S (과목)
+------+--------+          +------+--------+
| 학번 | 이름   |          | 과목 | 학점   |
+------+--------+          +------+--------+
| 001  | 홍길동 |          | DB   | 3      |
| 002  | 김철수 |          | 알고 | 3      |
+------+--------+          +------+--------+

        ↓ σ_학번='001'(R)  [셀렉트]

+------+--------+
| 학번 | 이름   |
+------+--------+
| 001  | 홍길동 |
+------+--------+

        ↓ π_이름(R)  [프로젝트]

+--------+
| 이름   |
+--------+
| 홍길동 |
| 김철수 |
+--------+

        ↓ R × S  [카티션 프로덕트]

+------+--------+------+--------+
| 학번 | 이름   | 과목 | 학점   |
+------+--------+------+--------+
| 001  | 홍길동 | DB   | 3      |
| 001  | 홍길동 | 알고 | 3      |
| 002  | 김철수 | DB   | 3      |
| 002  | 김철수 | 알고 | 3      |
+------+--------+------+--------+
```

#### 3. 심층 동작 원리: 각 연산자 상세

**1단계: 셀렉트(Selection) - σ (Sigma)**

```text
정의: σ_조건(R) = 릴레이션 R에서 조건을 만족하는 튜플 선택
특성: 수평적 부분집합 (행 필터링), 카디널리티 감소, 차수 불변

[예시]
학생 릴레이션
+------+--------+------+
| 학번 | 이름   | 학년 |
+------+--------+------+
| 001  | 홍길동 | 3    |
| 002  | 김철수 | 2    |
| 003  | 이영희 | 3    |
+------+--------+------+

σ_학년=3(학생)
+------+--------+------+
| 학번 | 이름   | 학년 |
+------+--------+------+
| 001  | 홍길동 | 3    |
| 003  | 이영희 | 3    |
+------+--------+------+

[SQL]
SELECT * FROM 학생 WHERE 학년 = 3;

[복합 조건]
σ_학년=3 ∧ 학과='컴공'(학생)  -- AND
σ_학년=3 ∨ 학년=4(학생)       -- OR
```

**2단계: 프로젝트(Projection) - π (Pi)**

```text
정의: π_속성리스트(R) = 릴레이션 R에서 지정된 속성만 추출
특성: 수직적 부분집합 (열 필터링), 차수 감소, 중복 제거

[예시]
학생 릴레이션
+------+--------+------+
| 학번 | 이름   | 학년 |
+------+--------+------+
| 001  | 홍길동 | 3    |
| 002  | 김철수 | 3    |
| 003  | 이영희 | 2    |
+------+--------+------+

π_이름,학년(학생)
+--------+------+
| 이름   | 학년 |
+--------+------+
| 홍길동 | 3    |
| 김철수 | 3    |
| 이영희 | 2    |
+--------+------+

[SQL]
SELECT DISTINCT 이름, 학년 FROM 학생;

[중복 제거 예시]
π_학년(학생)  -- {3, 2} (중복 제거됨)
```

**3단계: 조인(Join) - ⋈**

```text
정의: R ⋈_조건 S = 카티션 프로덕트 후 조건 필터링
종류:
- 자연 조인(Natural Join): 공통 속성으로 동등 조인, 중복 속성 제거
- 세타 조인(Theta Join): 일반 비교 연산자 사용
- 외부 조인(Outer Join): 매칭 안 되는 튜플도 포함

[자연 조인 예시]
학생                          수강
+------+--------+            +------+--------+
| 학번 | 이름   |            | 학번 | 과목   |
+------+--------+            +------+--------+
| 001  | 홍길동 |            | 001  | DB     |
| 002  | 김철수 |            | 001  | 알고   |
+------+--------+            | 002  | DB     |
                             +------+--------+

학생 ⋈ 수강 (자연 조인 - 학번 기준)
+------+--------+--------+
| 학번 | 이름   | 과목   |
+------+--------+--------+
| 001  | 홍길동 | DB     |
| 001  | 홍길동 | 알고   |
| 002  | 김철수 | DB     |
+------+--------+--------+

[SQL]
SELECT 학생.학번, 학생.이름, 수강.과목
FROM 학생 NATURAL JOIN 수강;
-- 또는
SELECT 학생.학번, 학생.이름, 수강.과목
FROM 학생 JOIN 수강 ON 학생.학번 = 수강.학번;
```

**4단계: 디비전(Division) - ÷**

```text
정의: R ÷ S = R의 속성 중 S의 속성과 매칭되는 모든 값을 가진 튜플
용도: "모든 ~을/를 가진" 질의에 사용

[예시]
수강(R) - 학번, 과목
+------+--------+
| 학번 | 과목   |
+------+--------+
| 001  | DB     |
| 001  | 알고   |
| 001  | 네트   |
| 002  | DB     |
| 002  | 알고   |
| 003  | DB     |
+------+--------+

필수과목(S) - 과목
+--------+
| 과목   |
+--------+
| DB     |
| 알고   |
+--------+

수강 ÷ 필수과목
+------+
| 학번 |
+------+
| 001  |  ← DB, 알고 모두 수강
| 002  |  ← DB, 알고 모두 수강
+------+
(003은 알고를 안 해서 제외)

[SQL - NOT EXISTS 이중 부정]
SELECT DISTINCT 학번
FROM 수강 R1
WHERE NOT EXISTS (
    SELECT * FROM 필수과목 S
    WHERE NOT EXISTS (
        SELECT * FROM 수강 R2
        WHERE R2.학번 = R1.학번
        AND R2.과목 = S.과목
    )
);
```

#### 4. 실무 수준의 관계 대수 구현

```python
"""
관계 대수(Relational Algebra) Python 구현
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Set, Callable, Optional
from functools import reduce

@dataclass
class Relation:
    """릴레이션(테이블) 표현"""
    name: str
    attributes: List[str]
    tuples: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        # 각 튜플이 모든 속성을 가지도록 보장
        for t in self.tuples:
            for attr in self.attributes:
                if attr not in t:
                    t[attr] = None

    @property
    def degree(self) -> int:
        """차수 (속성 개수)"""
        return len(self.attributes)

    @property
    def cardinality(self) -> int:
        """카디널리티 (튜플 개수)"""
        return len(self.tuples)

class RelationalAlgebra:
    """관계 대수 연산 구현"""

    # ==================== 순수 관계 연산자 ====================

    @staticmethod
    def select(relation: Relation, predicate: Callable[[Dict], bool]) -> Relation:
        """
        셀렉트(Selection): σ_조건(R)
        조건을 만족하는 튜플만 선택 (수평 필터링)
        """
        result_tuples = [t for t in relation.tuples if predicate(t)]
        return Relation(
            name=f"σ_{relation.name}",
            attributes=relation.attributes.copy(),
            tuples=result_tuples
        )

    @staticmethod
    def project(relation: Relation, attributes: List[str]) -> Relation:
        """
        프로젝트(Projection): π_속성(R)
        지정된 속성만 추출 (수직 필터링), 중복 제거
        """
        # 속성 검증
        for attr in attributes:
            if attr not in relation.attributes:
                raise ValueError(f"속성 '{attr}'이 릴레이션에 없음")

        # 속성 추출 및 중복 제거
        seen: Set[tuple] = set()
        result_tuples = []
        for t in relation.tuples:
            projected = {k: v for k, v in t.items() if k in attributes}
            key = tuple(sorted(projected.items()))
            if key not in seen:
                seen.add(key)
                result_tuples.append(projected)

        return Relation(
            name=f"π_{relation.name}",
            attributes=attributes,
            tuples=result_tuples
        )

    @staticmethod
    def cartesian_product(r1: Relation, r2: Relation) -> Relation:
        """
        카티션 프로덕트: R × S
        모든 튜플 조합
        """
        # 속성 이름 충돌 방지
        new_attributes = []
        r1_prefix = f"{r1.name}." if set(r1.attributes) & set(r2.attributes) else ""
        r2_prefix = f"{r2.name}." if set(r1.attributes) & set(r2.attributes) else ""

        for attr in r1.attributes:
            new_attributes.append(f"{r1_prefix}{attr}")
        for attr in r2.attributes:
            new_attributes.append(f"{r2_prefix}{attr}")

        result_tuples = []
        for t1 in r1.tuples:
            for t2 in r2.tuples:
                combined = {}
                for attr in r1.attributes:
                    combined[f"{r1_prefix}{attr}"] = t1[attr]
                for attr in r2.attributes:
                    combined[f"{r2_prefix}{attr}"] = t2[attr]
                result_tuples.append(combined)

        return Relation(
            name=f"{r1.name}×{r2.name}",
            attributes=new_attributes,
            tuples=result_tuples
        )

    @staticmethod
    def theta_join(r1: Relation, r2: Relation,
                   condition: Callable[[Dict, Dict], bool]) -> Relation:
        """
        세타 조인: R ⋈_조건 S
        조건을 만족하는 튜플만 조인
        """
        result_tuples = []

        for t1 in r1.tuples:
            for t2 in r2.tuples:
                if condition(t1, t2):
                    # 속성 이름 충돌 처리
                    combined = {}
                    for attr in r1.attributes:
                        combined[f"{r1.name}.{attr}"] = t1[attr]
                    for attr in r2.attributes:
                        if attr in r1.attributes:
                            combined[f"{r2.name}.{attr}"] = t2[attr]
                        else:
                            combined[attr] = t2[attr]
                    result_tuples.append(combined)

        # 속성 리스트 구성
        new_attributes = [f"{r1.name}.{a}" for a in r1.attributes]
        for a in r2.attributes:
            if a in r1.attributes:
                new_attributes.append(f"{r2.name}.{a}")
            else:
                new_attributes.append(a)

        return Relation(
            name=f"{r1.name}⋈{r2.name}",
            attributes=new_attributes,
            tuples=result_tuples
        )

    @staticmethod
    def natural_join(r1: Relation, r2: Relation) -> Relation:
        """
        자연 조인: R ⋈ S
        공통 속성으로 동등 조인, 중복 속성 제거
        """
        # 공통 속성 찾기
        common_attrs = list(set(r1.attributes) & set(r2.attributes))
        r1_only = [a for a in r1.attributes if a not in common_attrs]
        r2_only = [a for a in r2.attributes if a not in common_attrs]

        result_tuples = []
        for t1 in r1.tuples:
            for t2 in r2.tuples:
                # 공통 속성 값이 같은지 확인
                match = all(t1[a] == t2[a] for a in common_attrs)
                if match:
                    combined = {}
                    for a in r1_only:
                        combined[a] = t1[a]
                    for a in common_attrs:
                        combined[a] = t1[a]
                    for a in r2_only:
                        combined[a] = t2[a]
                    result_tuples.append(combined)

        return Relation(
            name=f"{r1.name}⋈{r2.name}",
            attributes=r1_only + common_attrs + r2_only,
            tuples=result_tuples
        )

    # ==================== 일반 집합 연산자 ====================

    @staticmethod
    def union(r1: Relation, r2: Relation) -> Relation:
        """
        합집합: R ∪ S
        중복 제거하여 합침 (호환성 필요: 같은 속성)
        """
        if r1.attributes != r2.attributes:
            raise ValueError("합집합: 속성이 호환되지 않음")

        seen: Set[tuple] = set()
        result_tuples = []

        for t in r1.tuples + r2.tuples:
            key = tuple(sorted(t.items()))
            if key not in seen:
                seen.add(key)
                result_tuples.append(t.copy())

        return Relation(
            name=f"{r1.name}∪{r2.name}",
            attributes=r1.attributes.copy(),
            tuples=result_tuples
        )

    @staticmethod
    def intersection(r1: Relation, r2: Relation) -> Relation:
        """
        교집합: R ∩ S
        양쪽 모두에 있는 튜플만
        """
        if r1.attributes != r2.attributes:
            raise ValueError("교집합: 속성이 호환되지 않음")

        r2_keys = {tuple(sorted(t.items())) for t in r2.tuples}
        result_tuples = [
            t.copy() for t in r1.tuples
            if tuple(sorted(t.items())) in r2_keys
        ]

        return Relation(
            name=f"{r1.name}∩{r2.name}",
            attributes=r1.attributes.copy(),
            tuples=result_tuples
        )

    @staticmethod
    def difference(r1: Relation, r2: Relation) -> Relation:
        """
        차집합: R - S
        R에만 있는 튜플
        """
        if r1.attributes != r2.attributes:
            raise ValueError("차집합: 속성이 호환되지 않음")

        r2_keys = {tuple(sorted(t.items())) for t in r2.tuples}
        result_tuples = [
            t.copy() for t in r1.tuples
            if tuple(sorted(t.items())) not in r2_keys
        ]

        return Relation(
            name=f"{r1.name}-{r2.name}",
            attributes=r1.attributes.copy(),
            tuples=result_tuples
        )

    @staticmethod
    def division(r1: Relation, r2: Relation) -> Relation:
        """
        디비전: R ÷ S
        R의 속성 중 S의 모든 값과 매칭되는 튜플
        """
        # R의 속성 중 S에 없는 속성 = 결과 속성
        result_attrs = [a for a in r1.attributes if a not in r2.attributes]
        divisor_attrs = [a for a in r2.attributes if a in r1.attributes]

        if not divisor_attrs:
            raise ValueError("디비전: 공통 속성이 없음")

        # 각 후보 튜플에 대해 S의 모든 값을 가지는지 확인
        result_tuples = []
        candidates = {}

        # 후보 그룹화
        for t1 in r1.tuples:
            key = tuple(t1[a] for a in result_attrs)
            if key not in candidates:
                candidates[key] = set()
            val = tuple(t1[a] for a in divisor_attrs)
            candidates[key].add(val)

        # S의 모든 조합
        s_values = set()
        for t2 in r2.tuples:
            val = tuple(t2[a] for a in divisor_attrs)
            s_values.add(val)

        # S의 모든 값을 가지는 후보만 선택
        for key, vals in candidates.items():
            if s_values <= vals:  # S의 모든 값이 후보에 있음
                result_tuples.append(dict(zip(result_attrs, key)))

        return Relation(
            name=f"{r1.name}÷{r2.name}",
            attributes=result_attrs,
            tuples=result_tuples
        )

# ==================== 사용 예시 ====================
if __name__ == "__main__":
    ra = RelationalAlgebra()

    # 학생 릴레이션
    students = Relation(
        name="students",
        attributes=["student_id", "name", "dept_id", "year"],
        tuples=[
            {"student_id": "001", "name": "홍길동", "dept_id": "D01", "year": 3},
            {"student_id": "002", "name": "김철수", "dept_id": "D01", "year": 2},
            {"student_id": "003", "name": "이영희", "dept_id": "D02", "year": 3},
        ]
    )

    # 과목 릴레이션
    courses = Relation(
        name="courses",
        attributes=["course_id", "course_name", "credits"],
        tuples=[
            {"course_id": "C01", "course_name": "DB", "credits": 3},
            {"course_id": "C02", "course_name": "알고리즘", "credits": 3},
        ]
    )

    # 수강 릴레이션
    enrollments = Relation(
        name="enrollments",
        attributes=["student_id", "course_id", "grade"],
        tuples=[
            {"student_id": "001", "course_id": "C01", "grade": "A"},
            {"student_id": "001", "course_id": "C02", "grade": "B+"},
            {"student_id": "002", "course_id": "C01", "grade": "A-"},
            {"student_id": "003", "course_id": "C01", "grade": "B"},
        ]
    )

    print("=== 원본 릴레이션 ===")
    print(f"학생: {[t['name'] for t in students.tuples]}")
    print(f"과목: {[t['course_name'] for t in courses.tuples]}")

    # 1. 셀렉트: 학년이 3인 학생
    print("\n=== σ_연도=3(학생) ===")
    result = ra.select(students, lambda t: t["year"] == 3)
    print(f"결과: {[t['name'] for t in result.tuples]}")

    # 2. 프로젝트: 학생 이름만
    print("\n=== π_이름(학생) ===")
    result = ra.project(students, ["name"])
    print(f"결과: {[t['name'] for t in result.tuples]}")

    # 3. 자연 조인: 학생 ⋈ 수강
    print("\n=== 학생 ⋈ 수강 (자연 조인) ===")
    result = ra.natural_join(students, enrollments)
    for t in result.tuples:
        print(f"  {t['name']}: {t['course_id']} ({t['grade']})")

    # 4. 복합 연산: 학년 3 학생의 이름과 학과
    print("\n=== π_이름,학과(σ_연도=3(학생)) ===")
    temp = ra.select(students, lambda t: t["year"] == 3)
    result = ra.project(temp, ["name", "dept_id"])
    for t in result.tuples:
        print(f"  {t}")

    # 5. 디비전: 모든 과목을 수강한 학생
    print("\n=== 수강 ÷ 과목 (모든 과목 수강자) ===")
    # 수강에서 학번, 과목코드만 프로젝트
    enroll_proj = ra.project(enrollments, ["student_id", "course_id"])
    course_proj = ra.project(courses, ["course_id"])
    result = ra.division(enroll_proj, course_proj)
    print(f"모든 과목 수강자: {[t['student_id'] for t in result.tuples]}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 관계 대수 vs 관계 해석 비교

| 비교 항목 | 관계 대수 | 관계 해석 |
|:---|:---|:---|
| **특성** | 절차적 | 비절차적 |
| **질문** | "어떻게 구할 것인가?" | "무엇을 구할 것인가?" |
| **표현** | 연산자 조합 | 논리식/술어 |
| **SQL 매핑** | 실행 계획 | WHERE 절 |
| **표현력** | 동등함 | 동등함 |

#### 2. 관계 대수 연산자와 SQL 매핑

| 관계 대수 | SQL | 예시 |
|:---|:---|:---|
| σ_조건(R) | SELECT * FROM R WHERE 조건 | WHERE |
| π_속성(R) | SELECT 속성 FROM R | SELECT |
| R ∪ S | R UNION S | UNION |
| R ∩ S | R INTERSECT S | INTERSECT |
| R - S | R EXCEPT S (MINUS) | EXCEPT |
| R × S | R CROSS JOIN S | CROSS JOIN |
| R ⋈ S | R JOIN S ON | JOIN |
| R ÷ S | NOT EXISTS (이중 부정) | NOT EXISTS |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 쿼리 최적화 이해**
- 상황: SQL 실행 계획 해석 필요
- 판단: 실행 계획은 관계 대수로 표현됨
- 전략: 관계 대수 이해로 옵티마이저 동작 파악

**시나리오 2: 복잡한 질의 설계**
- 상황: 복잡한 비즈니스 질의 구현
- 판단: 관계 대수로 먼저 논리적 설계
- 전략: σ → π → ⋈ 순서로 최적화

#### 2. 안티패턴 (Anti-patterns)
- **불필요한 카티션**: 조인 조건 누락 → 성능 저하
- **과도한 중첩**: 복잡한 관계 대수 → 가독성 저하

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과
- SQL 최적화 이론적 기반
- 쿼리 변환/최적화 표준
- 데이터베이스 이론의 핵심

#### 2. 참고 표준
- **E.F. Codd (1970)**: 관계 대수 제안
- **C.J. Date**: 관계 대수 교과서

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[관계 해석](@/studynotes/05_database/01_relational/relational_calculus.md)**: 비절차적 대응
- **[SQL](@/studynotes/05_database/03_optimization/query_optimization.md)**: 관계 대수의 실제 구현
- **[옵티마이저](@/studynotes/05_database/03_optimization/query_optimization.md)**: 관계 대수 기반 실행 계획
- **[조인](@/studynotes/05_database/03_optimization/hash_join.md)**: 관계 대수 조인 연산

---

### 👶 어린이를 위한 3줄 비유 설명
1. **장난감 고르기**: 장난감 가게에서 "빨간색"인 것만 고르는 게 셀렉트예요. 색깔 조건으로 걸러내는 거죠!
2. **장난감 이름만 말하기**: 장난감을 설명할 때 "이름"만 말하는 게 프로젝트예요. 크기나 가격은 빼고 이름만!
3. **장난감 묶음**: 내 장난감과 친구 장난감을 합치는 게 합집합, 둘 다 가진 것만 찾는 게 교집합이에요!
