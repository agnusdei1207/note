+++
title = "계층형 데이터 모델 (Hierarchical Model)"
date = "2026-03-04"
[extra]
categories = "studynotes-database"
+++

# 계층형 데이터 모델 (Hierarchical Model)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 계층형 데이터 모델은 데이터를 트리(Tree) 구조로 표현하는 데이터베이스 모델로, 부모-자식 관계가 1:N으로 구성되며, 1960년대 IBM IMS가 대표적인 구현체입니다.
> 2. **가치**: 단순한 구조로 인해 빠른 조회 성능(평균 2-3배)을 제공하며, 조직도, 제품 BOM, 파일 시스템 등 계층적 데이터에 최적화되어 있습니다.
> 3. **융합**: 계층형 모델은 XML, JSON, LDAP 등 현대 기술의 기반이 되었으며, RDBMS의 셀프 조인, CTE 재귀 쿼리로도 계층 구조를 구현할 수 있습니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**계층형 데이터 모델(Hierarchical Model)**은 데이터를 부모-자식 관계의 트리 구조로 표현하는 데이터베이스 모델입니다. 주요 특징은 다음과 같습니다:

- **트리 구조**: 하나의 루트(Root) 노드에서 시작하여 계층적으로 확장
- **1:N 관계**: 하나의 부모는 여러 자식을 가질 수 있으나, 자식은 하나의 부모만 가짐
- **네비게이션 방식**: 데이터 접근 시 부모에서 자식으로 순차적 이동
- **물리적 순서**: 데이터가 저장된 순서가 접근 순서를 결정

**핵심 용어**:
- 세그먼트(Segment): 계층형 모델에서의 레코드 단위
- 트리(Tree): 전체 데이터 구조
- 루트(Root): 최상위 세그먼트
- 부모(Parent)/자식(Child): 상하위 관계

#### 2. 💡 비유를 통한 이해
**가계도(족보)**로 비유할 수 있습니다:
```
                    [시조 할아버지]
                         |
            +------------+------------+
            |                         |
      [큰아버지]                 [할아버지]
            |                         |
      +-----+-----+             +-----+-----+
      |           |             |           |
   [사촌1]    [사촌2]       [아버지]    [작은아버지]
                                |
                          +-----+-----+
                          |           |
                       [나]       [동생]
```

가계도에서:
- 한 사람은 한 부모만 가짐 (1:N 관계)
- 위에서 아래로만 탐색 가능 (네비게이션)
- 시조 할아버지가 루트 노드

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계**: 1960년대 초, Apollo 우주 계획을 위한 대용량 데이터 관리가 필요했습니다. 파일 시스템으로는 복잡한 부품 계층 구조(BOM)를 효율적으로 관리할 수 없었습니다.
2. **혁신적 패러다임의 도입**: 1966년 IBM이 IMS(Information Management System)를 개발하여 계층형 모델을 처음 구현했습니다. 이는 최초의 상용 DBMS로 평가받습니다.
3. **비즈니스적 요구사항**: 제조업의 BOM(Bill of Materials), 금융의 계정과목, 정부의 조직도 등 계층적 데이터 관리가 필요한 분야에서 여전히 활용됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 계층형 모델 구성 요소 (표)

| 구성 요소 | 정의 | 특성 | 예시 | 비고 |
|:---|:---|:---|:---|:---|
| **세그먼트(Segment)** | 데이터 저장 단위 | 필드들의 집합 | 부서, 사원 | 테이블과 유사 |
| **필드(Field)** | 최소 데이터 단위 | 원자값 | 부서명, 사원명 | 칼럼과 유사 |
| **트리(Tree)** | 전체 데이터 구조 | 계층적 | 조직도 | 하나의 DB |
| **루트(Root)** | 최상위 세그먼트 | 부모 없음 | 본사 | 진입점 |
| **부모(Parent)** | 상위 세그먼트 | 1:N 관계 | 부서 → 사원 | |
| **자식(Child)** | 하위 세그먼트 | 1부모만 | 사원 ← 부서 | |

#### 2. 계층형 데이터 모델 구조 다이어그램

```text
+=====================================================================+
|                    [ 계층형 데이터 모델 구조 ]                       |
+=====================================================================+

[예시: 회사 조직도 + 프로젝트]

                           [회사] ← 루트 세그먼트
                             |
                +------------+------------+
                |                         |
            [부서:개발팀]            [부서:영업팀]    ← 부모 세그먼트
                |                         |
        +-------+-------+         +-------+-------+
        |       |       |         |       |       |
     [사원]  [사원]  [사원]    [사원]  [사원]  [사원]  ← 자식 세그먼트
        |       |
     [프로젝트] [프로젝트]                           ← 손자 세그먼트

[물리적 저장 구조 - 선주문 순회(Pre-order Traversal)]

저장 순서: 회사 → 개발팀 → 사원1 → 프로젝트A → 프로젝트B →
          사원2 → 사원3 → 영업팀 → 사원4 → 사원5 → 사원6

+----+----+----+----+----+----+----+----+----+----+----+----+
|회사|개발|사원1|P-A |P-B |사원2|사원3|영업|사원4|사원5|사원6|...
+----+----+----+----+----+----+----+----+----+----+----+----+
  ↑              ↑
  루트         리프(Leaf) - 자식 없음

[데이터 접근 예시]
질의: "개발팀 사원1의 프로젝트 찾기"
1. 루트(회사)에서 시작
2. 개발팀 세그먼트로 이동 (GET NEXT)
3. 사원1 세그먼트로 이동 (GET NEXT)
4. 프로젝트A 세그먼트 조회 (GET NEXT)
5. 프로젝트B 세그먼트 조회 (GET NEXT)
```

#### 3. 심층 동작 원리: IMS 데이터 조작

**1단계: 데이터 정의 (DBD - Database Definition)**

```assembly
* IMS DBD Definition Example
DBD     NAME=ORGDB,ACCESS=HISAM
DATASET DD1=ORGDATA,DEVICE=3380,SIZE=1000
SEGM    NAME=COMPANY,BYTES=50,PARENT=0
FIELD   NAME=(COMP_ID,SEQ),BYTES=4,START=1,TYPE=C
FIELD   NAME=COMP_NAME,BYTES=30,START=5,TYPE=C
SEGM    NAME=DEPT,BYTES=80,PARENT=COMPANY
FIELD   NAME=(DEPT_ID,SEQ),BYTES=4,START=1,TYPE=C
FIELD   NAME=DEPT_NAME,BYTES=30,START=5,TYPE=C
SEGM    NAME=EMP,BYTES=100,PARENT=DEPT
FIELD   NAME=(EMP_ID,SEQ),BYTES=4,START=1,TYPE=C
FIELD   NAME=EMP_NAME,BYTES=30,START=5,TYPE=C
FIELD   NAME=SALARY,BYTES=10,START=35,TYPE=P
DBDGEN
FINISH
END
```

**2단계: 데이터 조작 (DL/I 호출)**

```cobol
* IMS DL/I Data Manipulation
* GET UNIQUE: 특정 세그먼트 직접 검색
CALL 'CBLTDLI' USING GU
                     PCB-ADDRESS
                     IO-AREA
                     COMPANY-KEY
                     DEPT-KEY
                     EMP-KEY

* GET NEXT: 순차적 다음 세그먼트 검색
CALL 'CBLTDLI' USING GN
                     PCB-ADDRESS
                     IO-AREA

* INSERT: 새 세그먼트 추가
CALL 'CBLTDLI' USING ISRT
                     PCB-ADDRESS
                     IO-AREA
                     COMPANY-KEY
                     DEPT-KEY
                     EMP-KEY

* REPLACE: 세그먼트 수정
CALL 'CBLTDLI' USING REPL
                     PCB-AREA
                     IO-AREA

* DELETE: 세그먼트 삭제
CALL 'CBLTDLI' USING DLET
                     PCB-ADDRESS
                     IO-AREA
```

**3단계: 현대적 구현 (SQL로의 변환)**

```sql
-- 계층 구조 테이블
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100),
    parent_dept_id INT,
    FOREIGN KEY (parent_dept_id) REFERENCES departments(dept_id)
);

-- 재귀 CTE로 계층 조회 (MySQL 8.0+, PostgreSQL, Oracle)
WITH RECURSIVE dept_hierarchy AS (
    -- 기본 케이스: 루트 노드
    SELECT dept_id, dept_name, parent_dept_id, 1 AS level,
           CAST(dept_name AS VARCHAR(1000)) AS path
    FROM departments
    WHERE parent_dept_id IS NULL

    UNION ALL

    -- 재귀 케이스: 자식 노드
    SELECT d.dept_id, d.dept_name, d.parent_dept_id,
           dh.level + 1,
           CONCAT(dh.path, ' > ', d.dept_name)
    FROM departments d
    INNER JOIN dept_hierarchy dh ON d.parent_dept_id = dh.dept_id
)
SELECT * FROM dept_hierarchy ORDER BY path;

-- Oracle 계층 쿼리 (CONNECT BY)
SELECT dept_id, dept_name, level,
       SYS_CONNECT_BY_PATH(dept_name, ' > ') AS path
FROM departments
START WITH parent_dept_id IS NULL
CONNECT BY PRIOR dept_id = parent_dept_id
ORDER SIBLINGS BY dept_name;
```

#### 4. 실무 수준의 계층형 모델 구현

```python
"""
계층형 데이터 모델 구현 (현대적 Python 버전)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from collections import deque

@dataclass
class Segment:
    """계층형 모델의 세그먼트(노드)"""
    name: str
    segment_type: str
    fields: Dict[str, Any] = field(default_factory=dict)
    children: List['Segment'] = field(default_factory=list)
    parent: Optional['Segment'] = None

    def add_child(self, child: 'Segment') -> None:
        child.parent = self
        self.children.append(child)

    def get_path(self) -> List[str]:
        """루트부터 현재 노드까지의 경로"""
        path = []
        current = self
        while current:
            path.append(current.name)
            current = current.parent
        return list(reversed(path))

class HierarchicalDatabase:
    """계층형 데이터베이스 구현"""

    def __init__(self, name: str):
        self.name = name
        self.root: Optional[Segment] = None
        self.segments: Dict[str, Segment] = {}

    def set_root(self, segment: Segment) -> None:
        """루트 세그먼트 설정"""
        self.root = segment
        self.segments[segment.name] = segment
        print(f"[Hierarchy] 루트 설정: {segment.name}")

    def add_segment(self, parent_name: str, child: Segment) -> None:
        """세그먼트 추가 (부모-자식 관계)"""
        if parent_name not in self.segments:
            raise ValueError(f"부모 세그먼트 '{parent_name}' 없음")

        parent = self.segments[parent_name]
        parent.add_child(child)
        self.segments[child.name] = child
        print(f"[Hierarchy] 세그먼트 추가: {parent_name} → {child.name}")

    # ==================== 네비게이션 연산 ====================

    def get_unique(self, path: List[str]) -> Optional[Segment]:
        """
        GET UNIQUE: 경로로 직접 접근
        예: ['Company', 'Development', 'Employee001']
        """
        current = self.root
        for name in path[1:]:  # 루트 제외
            found = False
            for child in current.children:
                if child.name == name:
                    current = child
                    found = True
                    break
            if not found:
                return None
        return current

    def get_next(self, current: Segment) -> Optional[Segment]:
        """
        GET NEXT: 선주문 순회로 다음 세그먼트 반환
        Pre-order: Root → Left → Right
        """
        # 자식이 있으면 첫 번째 자식 반환
        if current.children:
            return current.children[0]

        # 자식이 없으면 형제(sibling) 찾기
        temp = current
        while temp.parent:
            siblings = temp.parent.children
            idx = siblings.index(temp)
            if idx + 1 < len(siblings):
                return siblings[idx + 1]
            temp = temp.parent

        return None  # 더 이상 없음

    def get_next_within_parent(self, current: Segment) -> Optional[Segment]:
        """
        GET NEXT IN PARENT: 같은 부모 내에서 다음 형제
        """
        if not current.parent:
            return None

        siblings = current.parent.children
        idx = siblings.index(current)
        if idx + 1 < len(siblings):
            return siblings[idx + 1]
        return None

    def get_parent(self, current: Segment) -> Optional[Segment]:
        """GET PARENT: 부모 세그먼트 반환"""
        return current.parent

    # ==================== 트리 순회 ====================

    def traverse_preorder(self, visitor: Callable[[Segment], None]) -> None:
        """선주문 순회 (Pre-order Traversal)"""
        if not self.root:
            return

        stack = [self.root]
        while stack:
            node = stack.pop()
            visitor(node)
            # 역순으로 스택에 추가 (왼쪽 자식 먼저 방문)
            for child in reversed(node.children):
                stack.append(child)

    def traverse_levelorder(self, visitor: Callable[[Segment], None]) -> None:
        """레벨 순서 순회 (BFS)"""
        if not self.root:
            return

        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            visitor(node)
            queue.extend(node.children)

    # ==================== 검색 연산 ====================

    def find_by_field(self, field_name: str,
                      value: Any) -> List[Segment]:
        """필드 값으로 세그먼트 검색"""
        results = []

        def search(node: Segment):
            if node.fields.get(field_name) == value:
                results.append(node)

        self.traverse_preorder(search)
        return results

    def get_subtree(self, segment_name: str) -> List[Segment]:
        """특정 세그먼트의 서브트리 반환"""
        if segment_name not in self.segments:
            return []

        subtree = []
        root_segment = self.segments[segment_name]

        def collect(node: Segment):
            subtree.append(node)

        # BFS로 서브트리 수집
        queue = deque([root_segment])
        while queue:
            node = queue.popleft()
            subtree.append(node)
            queue.extend(node.children)

        return subtree

# ==================== 사용 예시 ====================
if __name__ == "__main__":
    # 계층형 데이터베이스 생성
    db = HierarchicalDatabase("CompanyDB")

    # 루트 세그먼트
    company = Segment("SAMSUNG", "Company",
                     {"comp_id": "C001", "comp_name": "삼성전자"})
    db.set_root(company)

    # 부서 세그먼트 (1레벨)
    dev_dept = Segment("DEV_TEAM", "Department",
                       {"dept_id": "D001", "dept_name": "개발팀"})
    sales_dept = Segment("SALES_TEAM", "Department",
                         {"dept_id": "D002", "dept_name": "영업팀"})

    db.add_segment("SAMSUNG", dev_dept)
    db.add_segment("SAMSUNG", sales_dept)

    # 사원 세그먼트 (2레벨)
    emp1 = Segment("EMP001", "Employee",
                   {"emp_id": "E001", "emp_name": "홍길동", "salary": 50000000})
    emp2 = Segment("EMP002", "Employee",
                   {"emp_id": "E002", "emp_name": "김철수", "salary": 45000000})
    emp3 = Segment("EMP003", "Employee",
                   {"emp_id": "E003", "emp_name": "이영희", "salary": 40000000})

    db.add_segment("DEV_TEAM", emp1)
    db.add_segment("DEV_TEAM", emp2)
    db.add_segment("SALES_TEAM", emp3)

    # 네비게이션 테스트
    print("\n=== GET UNIQUE ===")
    segment = db.get_unique(["SAMSUNG", "DEV_TEAM", "EMP001"])
    print(f"조회 결과: {segment.name if segment else 'Not Found'}")
    print(f"필드: {segment.fields if segment else 'N/A'}")

    print("\n=== GET NEXT (선주문 순회) ===")
    current = db.root
    while current:
        print(f"  → {current.name} ({current.segment_type})")
        current = db.get_next(current)

    print("\n=== 필드 검색 ===")
    results = db.find_by_field("salary", 50000000)
    for r in results:
        print(f"  검색 결과: {r.name} - {r.fields}")

    print("\n=== 서브트리 조회 ===")
    subtree = db.get_subtree("DEV_TEAM")
    print(f"  개발팀 서브트리: {[s.name for s in subtree]}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 계층형 vs 망형 vs 관계형 모델 비교

| 비교 항목 | 계층형 모델 | 망형 모델 | 관계형 모델 |
|:---|:---|:---|:---|
| **구조** | 트리 (1:N) | 그래프 (N:M) | 테이블 |
| **관계** | 부모-자식 | 소유자-멤버 | 외래키 |
| **데이터 접근** | 네비게이션 | 네비게이션 | 선언적(SQL) |
| **유연성** | 낮음 | 중간 | 높음 |
| **복잡도** | 낮음 | 높음 | 중간 |
| **M:N 관계** | 불가능 | 가능 | 가능 |
| **대표 시스템** | IBM IMS | IDMS, Raima | Oracle, MySQL |

#### 2. 계층형 모델의 장단점

| 장점 | 단점 |
|:---|:---|
| 빠른 조회 성능 (경로 기반) | M:N 관계 표현 불가 |
| 단순한 구조 (이해 용이) | 데이터 중복 발생 가능 |
| 효율적인 물리적 저장 | 구조 변경 어려움 |
| 명확한 부모-자식 관계 | 프로그래밍 복잡度高 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 레거시 시스템 현대화**
- 상황: IMS 기반 레거시 시스템을 RDBMS로 마이그레이션
- 판단: 계층 구조를 관계형으로 변환 전략 수립
- 전략:
  1. 세그먼트 → 테이블 매핑
  2. 부모-자식 관계 → 외래키로 변환
  3. 네비게이션 로직 → SQL 쿼리로 변환

**시나리오 2: 계층적 데이터 설계**
- 상황: 조직도, 카테고리, 메뉴 구조 설계
- 판단: 관계형 DB에서 계층 구조 구현 방법 선택
- 전략:
  - Adjacency List: parent_id 컬럼 사용 (간단, 재귀 필요)
  - Nested Set: left/right 값 사용 (조회 빠름, 수정 느림)
  - Path Enumeration: 경로 문자열 저장 (조회 쉬움)
  - Closure Table: 별도 관계 테이블 (유연함)

**시나리오 3: XML/JSON 데이터 처리**
- 상황: 계층적 반정형 데이터 저장
- 판단: 계층형 모델의 현대적 변형 활용
- 전략: Native XML DB 또는 JSON 컬럼 타입 활용

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] **데이터 특성**: 계층적 구조인가? M:N 관계가 많은가?
- [ ] **질의 패턴**: 부모→자식 순차 조회가 주된 패턴인가?
- [ ] **변경 빈도**: 구조 변경이 빈번한가?
- [ ] **성능 요구**: 조회 성능이 중요한가, 수정 성능이 중요한가?

#### 3. 안티패턴 (Anti-patterns)
- **강제 계층화**: M:N 관계를 억지로 계층형으로 표현 → 중복 폭증
- **과도한 깊이**: 깊은 계층 구조 → 네비게이션 성능 저하
- **루트 없는 구조**: 여러 진입점 → 접근 복잡도 증가

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 구분 | 파일 시스템 | 계층형 DB | 관계형 DB |
|:---|:---|:---|:---|
| 계층 데이터 표현 | 수동 구현 | 자연스러움 | 변환 필요 |
| 조회 성능 | 느림 | 빠름 (경로 기반) | 중간 |
| 유연성 | 높음 | 낮음 | 높음 |
| 유지보수 | 어려움 | 중간 | 쉬움 |

#### 2. 미래 전망
- **XML/JSON 데이터베이스**: 계층형 모델의 현대적 계승
- **그래프 데이터베이스**: 계층형 + 네트워크 확장
- **멀티모델 DB**: 계층, 관계, 그래프 통합 지원

#### 3. 참고 표준
- **IBM IMS**: 최초의 계층형 DBMS
- **XML DOM**: 계층형 문서 모델 표준

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[망형 데이터 모델](@/studynotes/05_database/01_relational/network_model.md)**: 계층형의 확장 (N:M 가능)
- **[관계형 모델](@/studynotes/05_database/01_relational/relational_model.md)**: 현대적 대안
- **[트리 구조](@/studynotes/05_database/01_relational/hierarchical_query.md)**: SQL로 계층 구조 구현
- **[XML 데이터베이스](@/studynotes/05_database/04_dw_olap/xml_database.md)**: 계층형 모델의 현대적 구현

---

### 👶 어린이를 위한 3줄 비유 설명
1. **가계도**: 할아버지 → 아빠 → 나 → 내 동생으로 이어지는 가계도를 생각해 보세요. 한 사람은 한 명의 부모만 있죠. 이렇게 위에서 아래로만 이어지는 구조예요!
2. **폴더와 파일**: 컴퓨터의 폴더 안에 또 폴더가 있고, 그 안에 파일이 있죠? 이것도 계층형이에요. '내 문서' 폴더가 할아버지, '학교' 폴더가 아빠, '숙제.txt' 파일이 나 같은 거예요!
3. **회사 조직도**: 사장님 아래에 부장님이 있고, 부장님 아래에 과장님이 있죠? 위에서 아래로만 명령이 떨어지는 것처럼, 데이터도 위에서 아래로만 찾아갈 수 있어요!
