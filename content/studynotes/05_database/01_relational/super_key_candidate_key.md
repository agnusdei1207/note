+++
title = "슈퍼 키와 후보 키 (Super Key, Candidate Key)"
date = "2026-03-04"
[extra]
categories = "studynotes-database"
+++

# 슈퍼 키와 후보 키 (Super Key, Candidate Key)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 슈퍼 키는 유일성(Uniqueness)을 만족하는 속성 집합이고, 후보 키는 유일성과 최소성(Minimality)을 모두 만족하는 슈퍼 키의 부분집합입니다.
> 2. **가치**: 후보 키 중 하나를 기본 키(PK)로 선택하고, 나머지는 대체 키(Alternate Key)가 되며, 키 설계는 정규화와 성능의 핵심 요소입니다.
> 3. **융합**: 키 이론은 인덱스 설계, 조인 최적화, 분산 DB의 샤딩 키 선정에 직접적으로 영향을 미칩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**슈퍼 키 (Super Key)**
- 정의: 릴레이션에서 튜플을 유일하게 식별할 수 있는 속성(들)의 집합
- 특성: **유일성(Uniqueness)** 만족
- 예: {학번}, {학번, 이름}, {학번, 이름, 학과}, {주민번호} ...

**후보 키 (Candidate Key)**
- 정의: 슈퍼 키 중 최소성을 만족하는 것
- 특성: **유일성 + 최소성(Minimality)** 모두 만족
- 예: {학번}, {주민번호}

**키의 계층 구조**:
```
모든 속성 조합
       ↓ [유일성 만족]
    슈퍼 키
       ↓ [최소성 만족]
    후보 키
       ↓ [설계자 선택]
    기본 키 (PK)
       ↓ [나머지]
    대체 키 (AK)
```

#### 2. 💡 비유를 통한 이해
**사람 식별**로 비유할 수 있습니다:

```
[슈퍼 키] - 사람을 구별할 수 있는 모든 조합
- {주민번호}                    ✓ 유일함
- {주민번호, 이름}              ✓ 유일함 (하지만 이름은 필요 없음)
- {주민번호, 이름, 주소}        ✓ 유일함 (이름, 주소 필요 없음)
- {여권번호}                    ✓ 유일함 (여권 있는 사람만)
- {이름, 생년월일, 주소}        ✗ 유일하지 않을 수 있음

[후보 키] - 꼭 필요한 것만 포함
- {주민번호}    ✓ 더 줄일 수 없음
- {여권번호}    ✓ 더 줄일 수 없음

[기본 키 선택]
- 주민번호를 기본 키로 선택

[대체 키]
- 여권번호는 대체 키가 됨
```

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계**: 파일 시스템에서는 레코드 식별을 위해 물리적 위치(주소)를 사용했으나, 데이터 이동 시 식별이 불가능해졌습니다.
2. **혁신적 패러다임의 도입**: E.F. Codd가 관계형 모델에서 논리적 식별자인 키의 개념을 도입했습니다. 슈퍼 키와 후보 키는 정규화 이론의 핵심이 되었습니다.
3. **비즈니스적 요구사항**: 모든 비즈니스 엔티티는 유일하게 식별되어야 하며, 이를 위한 키 설계가 필수적입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 키의 종류와 특성 (표)

| 키 종류 | 유일성 | 최소성 | 예시 | 비고 |
|:---|:---|:---|:---|:---|
| **슈퍼 키** | ✓ | ✗ | {학번, 이름} | 유일하기만 하면 됨 |
| **후보 키** | ✓ | ✓ | {학번} | 더 줄일 수 없음 |
| **기본 키** | ✓ | ✓ | {학번} | 후보 키 중 선택 |
| **대체 키** | ✓ | ✓ | {주민번호} | 기본 키 아닌 후보 키 |
| **외래 키** | ✗ | ✗ | {학과코드} | 다른 테이블 참조 |

#### 2. 슈퍼 키와 후보 키 관계 다이어그램

```text
+====================================================================+
|                [ 슈퍼 키와 후보 키의 관계 ]                          |
+====================================================================+

학생(학번, 주민번호, 이름, 학과, 학년)

[모든 슈퍼 키]
┌─────────────────────────────────────────────────────────────────┐
│  {학번}                        ← 후보 키 (최소)                  │
│  {주민번호}                    ← 후보 키 (최소)                  │
│  {학번, 이름}                  ← 슈퍼 키 (이름 불필요)            │
│  {학번, 학과}                  ← 슈퍼 키 (학과 불필요)            │
│  {주민번호, 이름}              ← 슈퍼 키 (이름 불필요)            │
│  {학번, 주민번호}              ← 슈퍼 키 (주민번호 불필요)        │
│  {학번, 이름, 학과}            ← 슈퍼 키                          │
│  ...                                                            │
│  {학번, 주민번호, 이름, 학과, 학년} ← 슈퍼 키 (전체)              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ 최소성 만족
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    [ 후보 키 ]                                    │
│  ┌───────────────┐         ┌───────────────┐                   │
│  │   {학번}      │         │ {주민번호}    │                   │
│  │   CK1         │         │   CK2         │                   │
│  └───────┬───────┘         └───────┬───────┘                   │
│          │                         │                            │
│          │ 설계자 선택              │                            │
│          ▼                         ▼                            │
│  ┌───────────────┐         ┌───────────────┐                   │
│  │  기본 키 (PK) │         │  대체 키 (AK) │                   │
│  │   {학번}      │         │ {주민번호}    │                   │
│  └───────────────┘         └───────────────┘                   │
└─────────────────────────────────────────────────────────────────┘

[최소성 검증 예시]
{학번, 이름}이 후보 키인가?
- {학번}만으로도 유일성을 보장할 수 있는가? → YES
- 따라서 {학번, 이름}은 후보 키가 아님 (이름이 불필요)

{이름, 학과}가 후보 키인가?
- {이름}만으로 유일성을 보장하는가? → NO (동명이인)
- {학과}만으로 유일성을 보장하는가? → NO
- 따라서 {이름, 학과}는 슈퍼 키도 아님
```

#### 3. 심층 동작 원리: 최소성 판별

**1단계: 슈퍼 키 판별**

```text
[유일성 검증]
릴레이션 R에서 속성 집합 K가 슈퍼 키인지 확인:

∀ t1, t2 ∈ R: (t1 ≠ t2) ⇒ (t1[K] ≠ t2[K])

예시: 학생 릴레이션에서 K = {학번}
- 학번이 같은 두 튜플은 존재할 수 없음
- 따라서 {학번}은 슈퍼 키
```

**2단계: 후보 키 판별 (최소성)**

```text
[최소성 검증]
슈퍼 키 K가 후보 키인지 확인:
K의 어떤 진부분집합 K'도 슈퍼 키가 아니어야 함

∀ K' ⊂ K: K'는 슈퍼 키가 아님

예시 1: K = {학번, 이름}
- K' = {학번} → 슈퍼 키임 → {학번, 이름}은 후보 키 아님

예시 2: K = {학번}
- K' = {} → 슈퍼 키 아님
- {학번}은 더 이상 줄일 수 없음 → 후보 키
```

**3단계: 함수적 종속성과 후보 키**

```sql
-- 함수적 종속성으로 후보 키 판별

-- 학생 릴레이션
-- FD1: 학번 → 이름, 학과, 학년  (학번이 모든 속성 결정)
-- FD2: 주민번호 → 이름, 학과, 학년

-- 후보 키: 학번, 주민번호
-- (각각이 모든 속성을 함수적으로 결정)

CREATE TABLE students (
    student_id VARCHAR(10) PRIMARY KEY,  -- 기본 키로 선택
    ssn VARCHAR(14) UNIQUE,              -- 대체 키 (UNIQUE)
    name VARCHAR(50) NOT NULL,
    dept_id VARCHAR(5),
    year INT
);

-- 복합 후보 키 예시 (수강 릴레이션)
-- FD: (학번, 과목코드) → 성적
-- 후보 키: {학번, 과목코드}

CREATE TABLE enrollments (
    student_id VARCHAR(10),
    course_id VARCHAR(10),
    grade CHAR(2),
    PRIMARY KEY (student_id, course_id)  -- 복합 기본 키
);
```

#### 4. 실무 수준의 키 분석 구현

```python
"""
슈퍼 키와 후보 키 분석 시스템
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Set, Tuple, FrozenSet
from itertools import combinations

@dataclass
class Relation:
    """릴레이션 정의"""
    name: str
    attributes: List[str]
    tuples: List[Dict[str, Any]] = field(default_factory=list)

class KeyAnalyzer:
    """키 분석기"""

    def __init__(self, relation: Relation):
        self.relation = relation
        self.all_super_keys: Set[FrozenSet[str]] = set()
        self.candidate_keys: Set[FrozenSet[str]] = set()

    def analyze(self) -> Dict[str, Any]:
        """전체 키 분석"""
        print(f"\n=== {self.relation.name} 릴레이션 키 분석 ===")
        print(f"속성: {self.relation.attributes}")
        print(f"튜플 수: {len(self.relation.tuples)}")

        # 1. 모든 슈퍼 키 찾기
        self._find_all_super_keys()

        # 2. 후보 키 찾기 (최소성 만족)
        self._find_candidate_keys()

        return {
            'super_keys': [set(sk) for sk in self.all_super_keys],
            'candidate_keys': [set(ck) for ck in self.candidate_keys],
            'super_key_count': len(self.all_super_keys),
            'candidate_key_count': len(self.candidate_keys)
        }

    def _find_all_super_keys(self) -> None:
        """모든 슈퍼 키 찾기"""
        attrs = self.relation.attributes

        # 1개 속성부터 전체까지 조합 검사
        for r in range(1, len(attrs) + 1):
            for combo in combinations(attrs, r):
                key = frozenset(combo)
                if self._is_super_key(key):
                    self.all_super_keys.add(key)

        print(f"\n[슈퍼 키] 총 {len(self.all_super_keys)}개")
        for sk in sorted(self.all_super_keys, key=len):
            print(f"  {set(sk)}")

    def _is_super_key(self, key: FrozenSet[str]) -> bool:
        """슈퍼 키 여부 확인 (유일성)"""
        seen = set()
        for t in self.relation.tuples:
            # 키 속성 값들의 조합
            key_value = tuple(t.get(attr) for attr in key)
            if key_value in seen:
                return False  # 중복 발견
            seen.add(key_value)
        return True

    def _find_candidate_keys(self) -> None:
        """후보 키 찾기 (최소성)"""
        # 길이 순으로 정렬 (짧은 것부터)
        sorted_super_keys = sorted(self.all_super_keys, key=len)

        for sk in sorted_super_keys:
            # 이미 후보 키의 부분집합이면 스킵
            is_minimal = True
            for ck in self.candidate_keys:
                if ck < sk:  # ck가 sk의 진부분집합
                    is_minimal = False
                    break

            if is_minimal:
                self.candidate_keys.add(sk)

        print(f"\n[후보 키] 총 {len(self.candidate_keys)}개")
        for ck in sorted(self.candidate_keys, key=len):
            print(f"  {set(ck)}")

    def select_primary_key(self, ck_index: int = 0) -> FrozenSet[str]:
        """기본 키 선택"""
        sorted_ck = sorted(self.candidate_keys, key=len)
        if 0 <= ck_index < len(sorted_ck):
            pk = sorted_ck[ck_index]
            print(f"\n[기본 키 선택] {set(pk)}")
            return pk
        raise ValueError("잘못된 후보 키 인덱스")

    def get_alternate_keys(self, primary_key: FrozenSet[str]) -> Set[FrozenSet[str]]:
        """대체 키 목록"""
        alternate = self.candidate_keys - {primary_key}
        print(f"\n[대체 키] {len(alternate)}개")
        for ak in alternate:
            print(f"  {set(ak)}")
        return alternate

    def suggest_index(self) -> List[str]:
        """인덱스 생성 제안"""
        suggestions = []

        # 기본 키는 자동 인덱스
        for ck in self.candidate_keys:
            if len(ck) == 1:
                suggestions.append(f"CREATE INDEX idx_{list(ck)[0]} ON {self.relation.name}({list(ck)[0]});")
            else:
                cols = '_'.join(sorted(ck))
                col_list = ', '.join(sorted(ck))
                suggestions.append(f"CREATE INDEX idx_{cols} ON {self.relation.name}({col_list});")

        print("\n[인덱스 제안]")
        for s in suggestions:
            print(f"  {s}")
        return suggestions

# ==================== 사용 예시 ====================
if __name__ == "__main__":
    # 릴레이션 생성
    students = Relation(
        name="students",
        attributes=["student_id", "ssn", "name", "dept_id", "email"],
        tuples=[
            {"student_id": "001", "ssn": "900101-1234567", "name": "홍길동", "dept_id": "D01", "email": "hong@test.com"},
            {"student_id": "002", "ssn": "910202-2345678", "name": "김철수", "dept_id": "D01", "email": "kim@test.com"},
            {"student_id": "003", "ssn": "920303-3456789", "name": "이영희", "dept_id": "D02", "email": "lee@test.com"},
            {"student_id": "004", "ssn": "930404-4567890", "name": "박영수", "dept_id": "D01", "email": "park@test.com"},
        ]
    )

    # 키 분석
    analyzer = KeyAnalyzer(students)
    result = analyzer.analyze()

    # 기본 키 선택
    pk = analyzer.select_primary_key(0)  # 첫 번째 후보 키 선택

    # 대체 키 조회
    alternate = analyzer.get_alternate_keys(pk)

    # 인덱스 제안
    analyzer.suggest_index()

    # 결과 요약
    print("\n=== 분석 결과 요약 ===")
    print(f"슈퍼 키 수: {result['super_key_count']}")
    print(f"후보 키 수: {result['candidate_key_count']}")
    print(f"후보 키 목록: {[set(ck) for ck in result['candidate_keys']]}")

    # 동명이인 있는 경우 테스트
    print("\n\n=== 동명이인 케이스 ===")
    students2 = Relation(
        name="students_same_name",
        attributes=["student_id", "name", "dept_id"],
        tuples=[
            {"student_id": "001", "name": "홍길동", "dept_id": "D01"},
            {"student_id": "002", "name": "홍길동", "dept_id": "D02"},  # 동명이인
        ]
    )
    analyzer2 = KeyAnalyzer(students2)
    analyzer2.analyze()
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 슈퍼 키 vs 후보 키 비교

| 비교 항목 | 슈퍼 키 | 후보 키 |
|:---|:---|:---|
| **유일성** | 만족 | 만족 |
| **최소성** | 불필요 | 필수 |
| **수** | 많음 | 적음 |
| **용도** | 이론적 분석 | 실제 사용 |

#### 2. 키 선택 기준

| 기준 | 설명 | 우선순위 |
|:---|:---|:---|
| **불변성** | 값이 변하지 않음 | 높음 |
| **간결성** | 속성 수가 적음 | 높음 |
| **의미성** | 비즈니스 의미 있음 | 중간 |
| **보안성** | 민감 정보 없음 | 높음 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 복합 키 vs 대리 키**
- 상황: (주문일자, 순번) vs 주문ID
- 판단: 복합 키는 조인 복잡, 대리 키는 의미 없음
- 전략: 대리 키(Auto Increment) + Unique 제약조건

**시나리오 2: 자연 키 vs 대리 키**
- 상황: 주민번호 vs 회원ID
- 판단: 자연 키는 변경 가능성, 개인정보
- 전략: 대리 키 사용, 주민번호는 Unique

#### 2. 안티패턴 (Anti-patterns)
- **과도한 복합 키**: 조인 성능 저하
- **변경 가능한 키**: PK 변경은 위험
- **민감 정보 키**: 개인정보 노출 위험

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과
- 정확한 식별자 설계
- 정규화 이론의 기반
- 인덱스 설계 가이드

#### 2. 참고 표준
- **E.F. Codd**: 관계형 모델 키 이론
- **함수적 종속성**: 정규화 기반

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[기본 키](@/studynotes/05_database/01_relational/primary_key.md)**: 선택된 후보 키
- **[정규화](@/studynotes/05_database/01_relational/normalization.md)**: 후보 키 기반 분석
- **[인덱스](@/studynotes/05_database/01_relational/b_tree_index.md)**: 키 기반 성능 최적화
- **[무결성](@/studynotes/05_database/01_relational/integrity_constraints.md)**: 키로 보장

---

### 👶 어린이를 위한 3줄 비유 설명
1. **학생 식별**: 반에서 친구를 찾을 때 이름만 쓰면 동명이인이 있을 수 있어요. 학번을 쓰면 확실히 찾을 수 있죠! 학번이 후보 키예요!
2. **최소한의 정보**: 친구를 부를 때 "001번 홍길동 군"이라고 안 하고 "001번"이라고만 해도 돼요. 학번만으로도 충분하니까요!
3. **여러 가지 방법**: 친구를 식별하는 방법이 학번만 있는 게 아니에요. 주민번호, 여권번호도 다 달라요. 이게 다 후보 키예요!
