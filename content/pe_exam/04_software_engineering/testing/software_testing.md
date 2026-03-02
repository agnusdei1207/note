+++
title = "소프트웨어 테스트 (Software Testing)"
date = 2025-03-01

[extra]
categories = "software_engineering-testing"
+++

# 소프트웨어 테스트 (Software Testing)

## 핵심 인사이트 (3줄 요약)
> **소프트웨어 결함을 발견하고 품질을 검증하는 체계적 활동**. 단위→통합→시스템→인수 테스트로 진행. 블랙박스(명세 기반)와 화이트박스(구조 기반)로 분류.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 소프트웨어 테스트(Software Testing)는 **소프트웨어가 요구사항을 만족하는지 확인하고 결함을 발견**하기 위해 계획적으로 수행하는 검증 활동으로, 정적 테스트(실행 없이 분석)와 동적 테스트(실행하며 검증)로 구분된다.

> 💡 **비유**: 소프트웨어 테스트는 **"자동차 안전 검사"** 같아요. 출고 전에 브레이크, 엔진, 에어백 등 모든 부품을 철저히 점검하죠. 하나라도 문제가 있으면 출고할 수 없어요. 마찬가지로 소프트웨어도 배포 전에 모든 기능을 테스트해야 합니다!

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 결함 비용의 기하급수적 증가**: 요구사항 단계에서 발견하면 1배, 개발 단계에서 10배, 운영 단계에서 100배 비용 소요 (Boehm의 연구)
2. **기술적 필요성 - 복잡성 증가**: 현대 소프트웨어는 수백만 라인 코드, 수천 개 API, 다양한 환경 지원 → 수동 검증 불가능
3. **시장/산업 요구 - 품질 경쟁력**: 1개의 치명적 버그가 회사 신뢰도에 치명 (예: 대한항공 사이트 마비, 카카오 서버 장애)

**핵심 목적**: **결함 조기 발견으로 품질 확보, 리스크 완화, 비용 절감**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**테스트 레벨 (V-모델)** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        V-모델 (V-Model)                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│         ┌──────────────┐                           ┌──────────────┐     │
│         │ 요구사항 분석 │                           │  인수 테스트  │     │
│         └──────┬───────┘                           └───────┬──────┘     │
│                │                                           │            │
│         ┌──────▼───────┐                           ┌───────▼──────┐     │
│         │    설계      │                           │ 시스템 테스트 │     │
│         └──────┬───────┘                           └───────┬──────┘     │
│                │                                           │            │
│         ┌──────▼───────┐                           ┌───────▼──────┐     │
│         │  상세 설계   │                           │ 통합 테스트  │     │
│         └──────┬───────┘                           └───────┬──────┘     │
│                │                                           │            │
│         ┌──────▼───────┐                           ┌───────▼──────┐     │
│         │    구현      │ ───────────────────────→  │  단위 테스트  │     │
│         └──────────────┘                           └──────────────┘     │
│                                                                         │
│         ◀─────────────────────────────────────────────────────────▶     │
│                           검증 (Verification)                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                       테스트 레벨 상세                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. 단위 테스트 (Unit Test)                                             │
│     ┌─────────────────────────────────────────────────────────────┐    │
│     │ 대상: 함수, 메서드, 클래스 (최소 단위)                        │    │
│     │ 수행자: 개발자                                               │    │
│     │ 기법: 화이트박스 (구조 기반)                                  │    │
│     │ 도구: JUnit, pytest, Jest                                   │    │
│     │ 목표: 모듈 내부 로직 정확성 검증                              │    │
│     └─────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  2. 통합 테스트 (Integration Test)                                      │
│     ┌─────────────────────────────────────────────────────────────┐    │
│     │ 대상: 모듈 간 인터페이스, API 호출                            │    │
│     │ 수행자: 개발자 / 테스터                                       │    │
│     │ 기법: 화이트박스 + 블랙박스                                   │    │
│     │ 전략: 빅뱅, Top-Down, Bottom-Up, 샌드위치                    │    │
│     │ 목표: 컴포넌트 간 상호작용 검증                               │    │
│     └─────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  3. 시스템 테스트 (System Test)                                         │
│     ┌─────────────────────────────────────────────────────────────┐    │
│     │ 대상: 전체 시스템 (End-to-End)                               │    │
│     │ 수행자: QA 팀 (독립적)                                       │    │
│     │ 기법: 블랙박스 (명세 기반)                                    │    │
│     │ 종류: 기능 테스트, 비기능 테스트 (성능, 보안, 사용성)        │    │
│     │ 목표: 요구사항 충족 여부 검증                                 │    │
│     └─────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  4. 인수 테스트 (Acceptance Test)                                       │
│     ┌─────────────────────────────────────────────────────────────┐    │
│     │ 대상: 비즈니스 요구사항                                      │    │
│     │ 수행자: 고객, 사용자, 현업 담당자                             │    │
│     │ 기법: 블랙박스                                                │    │
│     │ 종류: 알파(개발 환경), 베타(실제 환경), UAT(사용자 인수)     │    │
│     │ 목표: 출시 준비 완료 여부 판단                                │    │
│     └─────────────────────────────────────────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**블랙박스 vs 화이트박스 테스트** (필수: 표):
| 구성 요소 | 블랙박스 테스트 | 화이트박스 테스트 |
|----------|---------------|-----------------|
| **내부 구조** | 모름 (블랙박스) | 앎 (화이트박스) |
| **기반** | 명세, 요구사항 | 코드, 제어 흐름 |
| **관점** | 사용자 관점 | 개발자 관점 |
| **주요 기법** | 동등분할, 경계값, 원인-결과 | 구문, 분기, 조건, 경로 커버리지 |
| **적용 시점** | 시스템, 인수 테스트 | 단위, 통합 테스트 |
| **자동화 용이성** | 중간 (UI 의존) | 높음 (코드 레벨) |
| **장점** | 사용자 시나리오 검증 | 코드 커버리지 측정 |
| **단점** | 내부 결함 탐지 어려움 | 요구사항 누락 가능 |

**블랙박스 테스트 기법 상세**:
```
┌─────────────────────────────────────────────────────────────────────────┐
│                   블랙박스 테스트 기법                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. 동등 분할 (Equivalence Partitioning)                                │
│     입력을 동등한 그룹으로 나누어 대표값만 테스트                        │
│                                                                         │
│     예: 나이 입력 (0-150)                                               │
│     ┌────────────┬────────────┬────────────┐                           │
│     │   무효     │    유효    │   무효     │                           │
│     │   < 0     │   0-150    │   > 150    │                           │
│     └────────────┴────────────┴────────────┘                           │
│          -1           50          200                                   │
│                                                                         │
│     → 3개 테스트 케이스로 충분 (무한 조합 대체)                         │
│                                                                         │
│  2. 경계값 분석 (Boundary Value Analysis)                               │
│     경계값에서 오류 발생 확률이 가장 높음                                │
│                                                                         │
│     예: 1-100 점수 입력                                                 │
│     ┌────┬────┬────┬─────┬─────┬─────┐                                │
│     │ 0  │ 1  │ 2  │ 99  │ 100 │ 101 │                                │
│     └────┴────┴────┴─────┴─────┴─────┘                                │
│       ↑    ↑              ↑     ↑     ↑                                 │
│     최소-1 최소        최대-1 최대  최대+1                              │
│                                                                         │
│     → 5개 테스트 케이스 (경계 ± 1)                                      │
│                                                                         │
│  3. 원인-결과 그래프 (Cause-Effect Graph)                               │
│     입력 조건(원인)과 출력(결과)의 관계 분석                             │
│                                                                         │
│     예: 로그인 검증                                                     │
│     원인: C1=ID 올바름, C2=PW 올바름                                    │
│     결과: E1=로그인 성공, E2=에러 메시지                                 │
│                                                                         │
│           C1 ──┐                                                        │
│                ├── AND ── E1                                            │
│           C2 ──┘                                                        │
│                                                                         │
│           NOT C1 ──┐                                                    │
│                    ├── OR ── E2                                         │
│           NOT C2 ──┘                                                    │
│                                                                         │
│  4. 상태 전이 테스트 (State Transition Testing)                         │
│     상태 변화에 따른 동작 검증                                           │
│                                                                         │
│     예: ATM 상태                                                        │
│     ┌─────────┐  카드삽입  ┌─────────┐                                 │
│     │  대기   │ ─────────→ │  인증   │                                 │
│     └─────────┘            └────┬────┘                                 │
│          ↑                     │ 인증성공                               │
│          │                     ▼                                        │
│     ┌────┴────┐  거래완료  ┌─────────┐                                 │
│     │  종료   │ ←───────── │  거래   │                                 │
│     └─────────┘            └─────────┘                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**화이트박스 테스트 기법 상세**:
```
┌─────────────────────────────────────────────────────────────────────────┐
│                   화이트박스 테스트 검증 기준                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  검증 기준 강도: 구문 < 분기 < 조건 < 분기/조건 < MC/DC < 경로          │
│                                                                         │
│  1. 구문 커버리지 (Statement Coverage, C0)                              │
│     모든 문장이 최소 1회 실행                                            │
│                                                                         │
│     def example(x):                                                     │
│         a = 1        # 문장 1                                          │
│         if x > 0:     # 문장 2 (조건)                                   │
│             a = 2    # 문장 3                                          │
│         return a     # 문장 4                                          │
│                                                                         │
│     → x=5: 문장 1,2,3,4 모두 실행 → 100% 구문 커버리지                  │
│                                                                         │
│  2. 분기 커버리지 (Branch Coverage, C1)                                 │
│     모든 분기(T/F)가 최소 1회 실행                                       │
│                                                                         │
│     위 예시에서:                                                        │
│     → x=5 (T), x=-1 (F) → 100% 분기 커버리지                           │
│                                                                         │
│  3. 조건 커버리지 (Condition Coverage, C2)                              │
│     복합 조건의 각 개별 조건이 T/F 최소 1회 실행                         │
│                                                                         │
│     if A and B:  # A와 B 각각 T/F 조합 필요                             │
│                                                                         │
│  4. MC/DC (Modified Condition/Decision Coverage)                        │
│     각 조건이 독립적으로 결과에 영향을 미치는지 검증                     │
│     (항공우주, 의료기기 등 안전 중요 시스템 필수)                        │
│                                                                         │
│  5. 경로 커버리지 (Path Coverage)                                       │
│     모든 실행 경로 테스트 (사실상 불가능)                                │
│                                                                         │
│  [순환 복잡도 (Cyclomatic Complexity)]                                  │
│                                                                         │
│  V(G) = E - N + 2  (E: 엣지 수, N: 노드 수)                             │
│  V(G) = P + 1      (P: 조건문 수)                                       │
│                                                                         │
│       ┌─────┐                                                          │
│       │ 시작│                                                          │
│       └──┬──┘                                                          │
│          │                                                             │
│       ┌──▼──┐                                                          │
│       │ if  │ ← 분기 1                                                 │
│       └──┬──┘                                                          │
│      ┌───┴───┐                                                         │
│      ▼       ▼                                                         │
│     ┌──┐   ┌──┐                                                        │
│     │T │   │F │                                                        │
│     └──┘   └──┘                                                        │
│      │       │                                                         │
│      └───┬───┘                                                         │
│          │                                                             │
│       ┌──▼──┐                                                          │
│       │ 끝  │                                                          │
│       └─────┘                                                          │
│                                                                         │
│  V(G) = 2 → 최소 2개 테스트 케이스 필요                                 │
│                                                                         │
│  복잡도 기준: 1-10 (단순), 11-20 (보통), 21+ (복잡, 리팩토링 권장)       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**핵심 알고리즘/공식** (해당 시 필수):
```
[커버리지 계산 공식]

구문 커버리지 = (실행된 문장 수 / 전체 문장 수) × 100%

분기 커버리지 = (실행된 분기 수 / 전체 분기 수) × 100%

조건 커버리지 = (실행된 조건 T/F 수 / 전체 조건 T/F 수) × 100%

[결함 밀도 (Defect Density)]

결함 밀도 = 발견된 결함 수 / 모듈 크기 (KLOC)

예: 10,000 LOC에서 50개 결함 발견
→ 결함 밀도 = 50 / 10 = 5 defects/KLOC

[테스트 효율성 (Test Effectiveness)]

테스트 효율성 = (테스트 단계 발견 결함 / 총 결함) × 100%

[테스트 커버리지 목표]

단위 테스트: 70-80% (100%는 비효율)
통합 테스트: API 커버리지 100%
시스템 테스트: 요구사항 커버리지 100%

[리스크 기반 테스트 우선순위]

우선순위 = (발생 확률 × 영향도) / 테스트 비용

고위험 영역 (결함 집중):
- 파레토 법칙: 80% 결함이 20% 모듈에 집중
- 복잡한 로직, 외부 인터페이스, 자주 변경되는 코드
```

**코드 예시** (필수: Python 테스트 프레임워크):
```python
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Callable, Any, Set
from enum import Enum, auto
from collections import defaultdict
import ast
import inspect

# ============================================================
# 1. 테스트 케이스 생성기 (블랙박스)
# ============================================================

@dataclass
class TestCase:
    """테스트 케이스"""
    id: str
    description: str
    inputs: Dict[str, Any]
    expected: Any
    actual: Any = None
    passed: bool = False

    def run(self, func: Callable) -> bool:
        """테스트 실행"""
        try:
            self.actual = func(**self.inputs)
            self.passed = self.actual == self.expected
        except Exception as e:
            self.actual = f"Exception: {e}"
            self.passed = False
        return self.passed


class EquivalencePartitioner:
    """동등 분할 테스트 케이스 생성기"""

    @staticmethod
    def generate_numeric_partitions(
        name: str,
        valid_range: Tuple[int, int],
        include_boundary: bool = True
    ) -> List[Dict]:
        """숫자 입력에 대한 동등 분할 생성"""
        min_val, max_val = valid_range
        partitions = []

        # 무효: 최소 미만
        partitions.append({
            "category": "invalid_below",
            "value": min_val - 1,
            "expected_valid": False
        })

        # 유효: 범위 내
        partitions.append({
            "category": "valid",
            "value": (min_val + max_val) // 2,
            "expected_valid": True
        })

        # 무효: 최대 초과
        partitions.append({
            "category": "invalid_above",
            "value": max_val + 1,
            "expected_valid": False
        })

        return partitions


class BoundaryValueAnalyzer:
    """경계값 분석 테스트 케이스 생성기"""

    @staticmethod
    def generate_boundary_values(
        name: str,
        valid_range: Tuple[int, int]
    ) -> List[Dict]:
        """경계값 테스트 케이스 생성"""
        min_val, max_val = valid_range
        test_values = []

        # 최소 경계
        test_values.append({"case": "min-1", "value": min_val - 1, "valid": False})
        test_values.append({"case": "min", "value": min_val, "valid": True})
        test_values.append({"case": "min+1", "value": min_val + 1, "valid": True})

        # 최대 경계
        test_values.append({"case": "max-1", "value": max_val - 1, "valid": True})
        test_values.append({"case": "max", "value": max_val, "valid": True})
        test_values.append({"case": "max+1", "value": max_val + 1, "valid": False})

        return test_values


# ============================================================
# 2. 화이트박스 커버리지 분석기
# ============================================================

@dataclass
class CoverageReport:
    """커버리지 리포트"""
    statement_count: int = 0
    statements_covered: int = 0
    branch_count: int = 0
    branches_covered: int = 0

    @property
    def statement_coverage(self) -> float:
        if self.statement_count == 0:
            return 0.0
        return self.statements_covered / self.statement_count * 100

    @property
    def branch_coverage(self) -> float:
        if self.branch_count == 0:
            return 0.0
        return self.branches_covered / self.branch_count * 100

    def __str__(self):
        return (f"구문 커버리지: {self.statement_coverage:.1f}% "
                f"({self.statements_covered}/{self.statement_count})\n"
                f"분기 커버리지: {self.branch_coverage:.1f}% "
                f"({self.branches_covered}/{self.branch_count})")


class CodeCoverageAnalyzer:
    """코드 커버리지 분석기"""

    def __init__(self):
        self.executed_lines: Set[int] = set()
        self.branches: Dict[int, Set[bool]] = defaultdict(set)  # line -> {True, False}
        self.source_lines: List[str] = []

    def trace_calls(self, frame, event, arg):
        """실행 추적 핸들러"""
        if event == 'line':
            self.executed_lines.add(frame.f_lineno)
        elif event == 'return':
            # 분기 추적 (단순화)
            pass
        return self.trace_calls

    def analyze_function(self, func: Callable, test_cases: List[Tuple]) -> CoverageReport:
        """함수 커버리지 분석"""
        # 소스 코드 분석
        source = inspect.getsource(func)
        self.source_lines = source.split('\n')

        # AST 분석으로 분기 수 계산
        tree = ast.parse(source)
        branch_count = self._count_branches(tree)
        statement_count = len([l for l in self.source_lines if l.strip() and not l.strip().startswith('#')])

        # 기존 추적 데이터 초기화
        self.executed_lines = set()
        self.branches = defaultdict(set)

        # 테스트 실행
        import sys
        old_trace = sys.gettrace()
        sys.settrace(self.trace_calls)

        try:
            for args in test_cases:
                try:
                    if isinstance(args, tuple):
                        func(*args)
                    else:
                        func(args)
                except:
                    pass
        finally:
            sys.settrace(old_trace)

        # 리포트 생성
        return CoverageReport(
            statement_count=statement_count,
            statements_covered=len(self.executed_lines),
            branch_count=branch_count,
            branches_covered=self._count_covered_branches()
        )

    def _count_branches(self, tree: ast.AST) -> int:
        """AST에서 분기 수 계산"""
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For)):
                count += 2  # True, False
            elif isinstance(node, ast.BoolOp):
                # and, or의 단축 평가
                count += len(node.values) - 1
        return max(count, 1)

    def _count_covered_branches(self) -> int:
        """커버된 분기 수 계산 (단순화)"""
        return len(self.executed_lines) // 2  # 추정치


# ============================================================
# 3. 단위 테스트 프레임워크 (미니 버전)
# ============================================================

class TestResult:
    """테스트 결과"""

    def __init__(self):
        self.tests_run: int = 0
        self.failures: List[Tuple[str, str]] = []
        self.errors: List[Tuple[str, str]] = []
        self.skipped: List[str] = []

    @property
    def passed(self) -> int:
        return self.tests_run - len(self.failures) - len(self.errors) - len(self.skipped)

    @property
    def success_rate(self) -> float:
        if self.tests_run == 0:
            return 0.0
        return self.passed / self.tests_run * 100

    def summary(self) -> str:
        lines = [
            f"\n{'='*60}",
            f"테스트 결과 요약",
            f"{'='*60}",
            f"실행: {self.tests_run}",
            f"성공: {self.passed}",
            f"실패: {len(self.failures)}",
            f"에러: {len(self.errors)}",
            f"건너뜀: {len(self.skipped)}",
            f"성공률: {self.success_rate:.1f}%",
        ]

        if self.failures:
            lines.append("\n실패한 테스트:")
            for name, msg in self.failures:
                lines.append(f"  ✗ {name}: {msg}")

        if self.errors:
            lines.append("\n에러 발생 테스트:")
            for name, msg in self.errors:
                lines.append(f"  ⚠ {name}: {msg}")

        return "\n".join(lines)


class TestCase:
    """테스트 케이스 베이스"""
    pass


class TestRunner:
    """테스트 러너"""

    def __init__(self):
        self.result = TestResult()

    def run(self, test_case: TestCase) -> TestResult:
        """테스트 케이스 실행"""
        methods = [m for m in dir(test_case) if m.startswith('test_')]

        for method_name in methods:
            self.result.tests_run += 1
            test_name = f"{test_case.__class__.__name__}.{method_name}"

            # setUp 실행
            if hasattr(test_case, 'setUp'):
                try:
                    test_case.setUp()
                except Exception as e:
                    self.result.errors.append((test_name, str(e)))
                    continue

            # 테스트 실행
            try:
                method = getattr(test_case, method_name)
                method()
                print(f"✓ {test_name}")
            except AssertionError as e:
                self.result.failures.append((test_name, str(e)))
                print(f"✗ {test_name}: {e}")
            except Exception as e:
                self.result.errors.append((test_name, str(e)))
                print(f"⚠ {test_name}: {e}")

            # tearDown 실행
            if hasattr(test_case, 'tearDown'):
                try:
                    test_case.tearDown()
                except:
                    pass

        return self.result


# ============================================================
# 4. 목(Mock) 객체 생성기
# ============================================================

class Mock:
    """간단한 Mock 객체"""

    def __init__(self, **kwargs):
        self._calls: List[Tuple] = []
        self._return_values: Dict[str, Any] = {}
        self._call_counts: Dict[str, int] = defaultdict(int)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, name):
        def mock_method(*args, **kwargs):
            self._calls.append((name, args, kwargs))
            self._call_counts[name] += 1

            if name in self._return_values:
                return self._return_values[name]
            return None

        return mock_method

    def set_return_value(self, method_name: str, value: Any):
        self._return_values[method_name] = value

    def called_with(self, method_name: str, *args, **kwargs) -> bool:
        """특정 인자로 호출되었는지 확인"""
        for call in self._calls:
            if call[0] == method_name:
                if args and call[1] != args:
                    continue
                if kwargs and call[2] != kwargs:
                    continue
                return True
        return False

    @property
    def call_count(self) -> int:
        return len(self._calls)


# ============================================================
# 5. 테스트 데이터 생성기
# ============================================================

class TestDataGenerator:
    """테스트 데이터 생성기"""

    @staticmethod
    def generate_user(valid: bool = True) -> Dict:
        """사용자 데이터 생성"""
        if valid:
            return {
                "id": 1,
                "email": "user@example.com",
                "name": "홍길동",
                "age": 30,
                "phone": "010-1234-5678"
            }
        else:
            return {
                "id": -1,  # 무효
                "email": "invalid-email",  # 무효
                "name": "",  # 무효
                "age": 200,  # 무효
                "phone": "123"  # 무효
            }

    @staticmethod
    def generate_boundary_integers(valid_range: Tuple[int, int]) -> Dict[str, int]:
        """경계값 정수 생성"""
        min_val, max_val = valid_range
        return {
            "below_min": min_val - 1,
            "at_min": min_val,
            "above_min": min_val + 1,
            "below_max": max_val - 1,
            "at_max": max_val,
            "above_max": max_val + 1
        }

    @staticmethod
    def generate_string_variations(max_length: int) -> Dict[str, str]:
        """문자열 경계값 생성"""
        return {
            "empty": "",
            "single_char": "a",
            "at_max": "a" * max_length,
            "over_max": "a" * (max_length + 1),
            "with_special": "test@#$",
            "with_unicode": "테스트中文🎉"
        }


# ============================================================
# 6. 결함 추적기
# ============================================================

class DefectStatus(Enum):
    NEW = auto()
    ASSIGNED = auto()
    FIXED = auto()
    VERIFIED = auto()
    CLOSED = auto()
    REOPENED = auto()


class DefectSeverity(Enum):
    CRITICAL = 1  # 시스템 중단
    HIGH = 2      # 주요 기능 장애
    MEDIUM = 3    # 기능 저하
    LOW = 4       # 사소한 문제


@dataclass
class Defect:
    """결함"""
    id: str
    title: str
    description: str
    severity: DefectSeverity
    status: DefectStatus = DefectStatus.NEW
    assignee: Optional[str] = None
    created_at: str = ""
    test_case_id: Optional[str] = None

    def assign(self, assignee: str):
        self.assignee = assignee
        self.status = DefectStatus.ASSIGNED

    def fix(self):
        self.status = DefectStatus.FIXED

    def verify(self, passed: bool):
        if passed:
            self.status = DefectStatus.VERIFIED
        else:
            self.status = DefectStatus.REOPENED

    def close(self):
        self.status = DefectStatus.CLOSED


class DefectTracker:
    """결함 추적기"""

    def __init__(self):
        self.defects: Dict[str, Defect] = {}
        self._next_id = 1

    def create_defect(self, title: str, description: str,
                      severity: DefectSeverity,
                      test_case_id: str = None) -> Defect:
        """결함 생성"""
        defect_id = f"DEF-{self._next_id:04d}"
        self._next_id += 1

        defect = Defect(
            id=defect_id,
            title=title,
            description=description,
            severity=severity,
            test_case_id=test_case_id,
            created_at=str(datetime.now())
        )
        self.defects[defect_id] = defect
        print(f"🐛 결함 등록: {defect_id} - {title}")
        return defect

    def get_defects_by_status(self, status: DefectStatus) -> List[Defect]:
        """상태별 결함 조회"""
        return [d for d in self.defects.values() if d.status == status]

    def get_defects_by_severity(self, severity: DefectSeverity) -> List[Defect]:
        """심각도별 결함 조회"""
        return [d for d in self.defects.values() if d.severity == severity]

    def summary(self) -> str:
        """결함 요약 리포트"""
        lines = ["\n=== 결함 추적 요약 ==="]

        by_severity = defaultdict(int)
        by_status = defaultdict(int)

        for defect in self.defects.values():
            by_severity[defect.severity.name] += 1
            by_status[defect.status.name] += 1

        lines.append(f"\n총 결함 수: {len(self.defects)}")
        lines.append("\n심각도별:")
        for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            lines.append(f"  {sev}: {by_severity[sev]}")

        lines.append("\n상태별:")
        for status in DefectStatus:
            lines.append(f"  {status.name}: {by_status[status.name]}")

        return "\n".join(lines)


# ============================================================
# 7. 테스트 자동화 파이프라인 (시뮬레이션)
# ============================================================

class TestPipeline:
    """테스트 자동화 파이프라인"""

    def __init__(self, name: str):
        self.name = name
        self.stages: List[Dict] = []
        self.results: Dict[str, bool] = {}

    def add_stage(self, name: str, test_func: Callable,
                  required: bool = True) -> None:
        """테스트 단계 추가"""
        self.stages.append({
            "name": name,
            "test_func": test_func,
            "required": required
        })

    def run(self) -> bool:
        """파이프라인 실행"""
        print(f"\n{'='*60}")
        print(f"테스트 파이프라인: {self.name}")
        print(f"{'='*60}")

        all_passed = True

        for stage in self.stages:
            print(f"\n▶ {stage['name']} 실행 중...")

            try:
                result = stage['test_func']()
                passed = result if isinstance(result, bool) else True
            except Exception as e:
                passed = False
                print(f"  에러: {e}")

            self.results[stage['name']] = passed

            if passed:
                print(f"  ✓ 통과")
            else:
                print(f"  ✗ 실패")
                if stage['required']:
                    all_passed = False

        print(f"\n{'='*60}")
        if all_passed:
            print("🎉 모든 필수 테스트 통과!")
        else:
            print("❌ 일부 필수 테스트 실패")
        print(f"{'='*60}")

        return all_passed


# ============================================================
# 사용 예시
# ============================================================

from datetime import datetime

if __name__ == "__main__":
    print("=" * 60)
    print("소프트웨어 테스트 데모")
    print("=" * 60)

    # 1. 동등 분할 테스트
    print("\n1. 동등 분할 테스트")
    print("-" * 40)
    partitions = EquivalencePartitioner.generate_numeric_partitions(
        "age", (0, 150)
    )
    for p in partitions:
        print(f"  {p['category']}: {p['value']} (유효: {p['expected_valid']})")

    # 2. 경계값 분석
    print("\n2. 경계값 분석")
    print("-" * 40)
    boundaries = BoundaryValueAnalyzer.generate_boundary_values(
        "score", (1, 100)
    )
    for b in boundaries:
        print(f"  {b['case']}: {b['value']} (유효: {b['valid']})")

    # 3. 커버리지 분석
    print("\n3. 코드 커버리지 분석")
    print("-" * 40)

    def sample_function(x: int) -> int:
        result = 0
        if x > 0:
            result = x * 2
        else:
            result = -x
        return result

    analyzer = CodeCoverageAnalyzer()
    report = analyzer.analyze_function(sample_function, [(5,), (-3,)])
    print(report)

    # 4. 결함 추적
    print("\n4. 결함 추적")
    print("-" * 40)
    tracker = DefectTracker()

    tracker.create_defect(
        "로그인 버튼 응답 없음",
        "로그인 버튼 클릭 시 아무 반응 없음",
        DefectSeverity.CRITICAL
    )

    tracker.create_defect(
        "폰트 크기 불일치",
        "헤더와 본문 폰트 크기가 다름",
        DefectSeverity.LOW
    )

    # 결함 상태 변경
    defect = list(tracker.defects.values())[0]
    defect.assign("박개발")
    defect.fix()
    defect.verify(True)
    defect.close()

    print(tracker.summary())

    # 5. 테스트 파이프라인
    print("\n5. 테스트 파이프라인")
    print("-" * 40)

    def unit_tests():
        print("  단위 테스트 50개 실행...")
        return True

    def integration_tests():
        print("  통합 테스트 20개 실행...")
        return True

    def e2e_tests():
        print("  E2E 테스트 10개 실행...")
        return True

    pipeline = TestPipeline("CI/CD 파이프라인")
    pipeline.add_stage("단위 테스트", unit_tests, required=True)
    pipeline.add_stage("통합 테스트", integration_tests, required=True)
    pipeline.add_stage("E2E 테스트", e2e_tests, required=False)

    pipeline.run()
