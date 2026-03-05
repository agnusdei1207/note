+++
title = "소프트웨어 비용 산정 (Software Cost Estimation)"
date = 2024-05-24
description = "COCOMO, 기능점수(FP), LOC 기반 소프트웨어 개발 비용 예측 및 일정 계획 기법"
weight = 10
+++

# 소프트웨어 비용 산정 (Software Cost Estimation)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 비용 산정은 프로젝트의 **범위(Scope)를 정량화**하고, 이를 기반으로 **필요 인력(PM), 기간(Duration), 비용(Cost)**을 예측하는 활동으로, 하향식(전문가 판단)과 상향식(LOC, FP, COCOMO) 기법으로 대별됩니다.
> 2. **가치**: 초기 단계에서 현실적인 예산과 일정을 수립함으로써 **프로젝트 실패(예산 초과 177%, 일정 지연 221%)를 예방**하고, 이해관계자의 기대를 관리합니다.
> 3. **융합**: 애자일에서는 스토리 포인트, 플래닝 포커로 대체되나, 대형 SI/공공 프로젝트에서는 여전히 **COCOMO II, 기능점수(FP)가 입찰 및 계약의 필수 도구**입니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의
소프트웨어 비용 산정은 소프트웨어 개발에 필요한 **자원(Resource)**을 예측하는 활동입니다. 여기서 '비용'은 단순히 금전적 비용뿐만 아니라 **인력(Man-Month), 기간(Duration), 하드웨어/소프트웨어 자원**을 모두 포함합니다.

**비용 산정의 3요소 (Iron Triangle)**:
1. **규모(Size)**: 소프트웨어의 크기 (LOC, FP, Story Point)
2. **노력(Effort)**: 필요한 인력 (Person-Month, PM)
3. **일정(Schedule)**: 소요 기간 (Month, Week)

### 💡 일상생활 비유: 집 짓는 비용 예측
소프트웨어 비용 산정은 집을 짓기 전 견적을 내는 것과 유사합니다.

```
[집 짓기 견적]
1. 집 크기 측정 (평수) = 소프트웨어 규모 (LOC, FP)
2. 필요한 자재 계산 = 개발 도구, 라이브러리
3. 필요한 인력 계산 (인부 수 × 기간) = 노력 (PM)
4. 총 비용 계산 = 소프트웨어 비용

[하향식] "비슷한 집 지을 때 5억 들었으니, 이번도 5억"
[상향식] "방이 5개니까 방마다 1억, 주방 5천만 원... 총 6억"
```

### 2. 등장 배경 및 발전 과정

#### 1) 소프트웨어 위기와 비용 산정의 필요성
1968년 NATO 컨퍼런스에서 '소프트웨어 위기'가 논의된 이후, **예산 초과, 일정 지연, 품질 저하**가 프로젝트 실패의 3대 원인으로 지목되었습니다. Standish Group의 CHAOS 보고서에 따르면:
- 평균 예산 초과율: **177%**
- 평균 일정 지연율: **221%**
- 전체 기능의 45%만이 실제 사용됨

#### 2) 1981년 COCOMO의 탄생
배리 봄(Barry Boehm)이 **COCOMO(Constructive COst MOdel)**를 발표했습니다. 63개 프로젝트의 실적 데이터를 기반으로 한 최초의 체계적 비용 산정 모델입니다.

#### 3) 2000년 COCOMO II로 진화
인터넷, 객체지향, 컴포넌트 기반 개발에 대응하여 **COCOMO II**가 발표되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 비용 산정 기법 분류

| 분류 | 기법 | 원리 | 장점 | 단점 |
| :--- | :--- | :--- | :--- | :--- |
| **하향식** | 전문가 판단 | 유사 프로젝트 경험 기반 | 빠름 | 주관적 |
| | 델파이 기법 | 다수 전문가 합의 | 객관성 향상 | 시간 소요 |
| **상향식** | LOC (Lines of Code) | 코드 라인 수 기반 | 객관적 | 언어별 차이 |
| | FP (Function Point) | 기능 개수 기반 | 언어 독립적 | 복잡한 계산 |
| | COCOMO | 수학적 모델 | 공식화됨 | 보정 계수 의존 |
| **애자일** | 스토리 포인트 | 상대적 규모 | 팀별 최적화 | 절대적 비용 변환 어려움 |

### 2. 정교한 구조 다이어그램: 비용 산정 프로세스

```text
================================================================================
|                  SOFTWARE COST ESTIMATION PROCESS                             |
================================================================================

    [1. SCOPE DEFINITION]
    =====================
    | - Requirements Gathering
    | - WBS (Work Breakdown Structure)
    | - Feature List
    =====================
              |
              v
    [2. SIZE ESTIMATION]
    =====================
    | Method Selection:
    | +-- LOC (Lines of Code)
    | +-- FP (Function Points)
    | +-- Story Points (Agile)
    | +-- Use Case Points
    =====================
              |
              v
    [3. EFFORT ESTIMATION]
    =====================
    | Convert Size to Effort (Person-Month)
    |
    | COCOMO Formula:
    | Effort = A × (Size)^B × EAF
    |   - A, B: Mode constants
    |   - EAF: Effort Adjustment Factor
    =====================
              |
              v
    [4. SCHEDULE ESTIMATION]
    =====================
    | Calculate Duration
    |
    | COCOMO Formula:
    | Duration = C × (Effort)^D
    | Staffing = Effort / Duration
    =====================
              |
              v
    [5. COST CALCULATION]
    =====================
    | Total Cost = Effort × Unit Cost
    |
    | Components:
    | +-- Labor Cost
    | +-- Hardware/Software
    | +-- Training
    | +-- Contingency (10-20%)
    =====================
              |
              v
    [6. VALIDATION & ADJUSTMENT]
    ============================
    | - Expert Review
    | - Historical Data Comparison
    | - Risk Adjustment
    | - Stakeholder Approval
    ============================

================================================================================
```

### 3. 심층 동작 원리: COCOMO 모델

#### 기본 COCOMO (Basic COCOMO)

```text
[BASIC COCOMO 공식]

Effort (PM) = A × (KLOC)^B
Duration (Month) = C × (Effort)^D
Staff = Effort / Duration

[프로젝트 유형별 계수]

+----------------+-------+-------+-------+-------+
| Mode           |   A   |   B   |   C   |   D   |
+----------------+-------+-------+-------+-------+
| Organic        |  2.4  | 1.05  | 2.5   | 0.38  |
| (유기적형)     |       |       |       |       |
| - Small team   |       |       |       |       |
| - Familiar env |       |       |       |       |
+----------------+-------+-------+-------+-------+
| Semi-Detached  |  3.0  | 1.12  | 2.5   | 0.35  |
| (준분리형)     |       |       |       |       |
| - Medium team  |       |       |       |       |
| - Mixed exp    |       |       |       |       |
+----------------+-------+-------+-------+-------+
| Embedded       |  3.6  | 1.20  | 2.5   | 0.32  |
| (내장형)       |       |       |       |       |
| - Tight const  |       |       |       |       |
| - High risk    |       |       |       |       |
+----------------+-------+-------+-------+-------+

[예시 계산]
프로젝트: 50 KLOC, Semi-Detached

Effort = 3.0 × (50)^1.12
       = 3.0 × 69.8
       = 209.4 Person-Month

Duration = 2.5 × (209.4)^0.35
         = 2.5 × 7.0
         = 17.5 Months

Staff = 209.4 / 17.5 = 12 people
```

#### 중간 COCOMO (Intermediate COCOMO)

```text
[INTERMEDIATE COCOMO 공식]

Effort = A × (KLOC)^B × EAF

EAF (Effort Adjustment Factor) = ∏(Cost Driver Rating)

[15개 비용 드라이버 (Cost Drivers)]

PRODUCT ATTRIBUTES (제품 속성)
1. RELY   - Required Software Reliability
2. DATA   - Database Size
3. CPLX   - Product Complexity

PLATFORM ATTRIBUTES (플랫폼 속성)
4. TIME   - Execution Time Constraints
5. STOR   - Main Storage Constraints
6. VIRT   - Virtual Machine Volatility
7. TURN   - Computer Turnaround Time

PERSONNEL ATTRIBUTES (인력 속성)
8. ACAP   - Analyst Capability
9. AEXP   - Applications Experience
10. PCAP  - Programmer Capability
11. VEXP  - Virtual Machine Experience
12. LEXP  - Language Experience

PROJECT ATTRIBUTES (프로젝트 속성)
13. MODP  - Modern Programming Practices
14. TOOL  - Use of Software Tools
15. SCED  - Required Development Schedule

[각 드라이버 등급]
Very Low: 0.70 ~ Nominal: 1.00 ~ Very High: 1.40

[예시]
- RELY: High (1.15) - 금융 시스템
- CPLX: Very High (1.30) - 복잡한 알고리즘
- ACAP: High (0.86) - 우수한 분석가
- TOOL: High (0.86) - 최신 도구 사용

EAF = 1.15 × 1.30 × 0.86 × 0.86 = 1.11

Effort = Basic Effort × EAF = 209.4 × 1.11 = 232.4 PM
```

### 4. 기능점수 (Function Point) 산정

```text
[FUNCTION POINT 계산 과정]

STEP 1: 기능 유형별 식별 및 복잡도 평가

데이터 기능 (Data Functions)
+----------------+---------------------------+
| Type           | Description               |
+----------------+---------------------------+
| ILF            | Internal Logical File     |
| (내부 논리 파일)| 시스템 내부에서 관리      |
| EIF            | External Interface File    |
| (외부 인터페이스)| 외부 시스템 참조          |
+----------------+---------------------------+

트랜잭션 기능 (Transaction Functions)
+----------------+---------------------------+
| Type           | Description               |
+----------------+---------------------------+
| EI             | External Input            |
| (외부 입력)     | 데이터 입력, 화면         |
| EO             | External Output           |
| (외부 출력)     | 보고서, 계산 포함 출력    |
| EQ             | External Inquiry          |
| (외부 조회)     | 단순 조회                 |
+----------------+---------------------------+

STEP 2: 복잡도 결정 (DET, RET, FTR)

DET (Data Element Type): 데이터 필드 수
RET (Record Element Type): 레코드 유형 수
FTR (File Type Referenced): 참조 파일 수

예: 주문 등록 화면 (EI)
- DET: 주문번호, 고객ID, 상품코드, 수량, 금액 = 5
- FTR: 주문파일, 고객파일 = 2
- 복잡도: Low

STEP 3: 가중치 적용

+--------+-------+-------+-------+
| Type   | Low   | Avg   | High  |
+--------+-------+-------+-------+
| ILF    |   7   |  10   |  15   |
| EIF    |   5   |   7   |  10   |
| EI     |   3   |   4   |   6   |
| EO     |   4   |   5   |   7   |
| EQ     |   3   |   4   |   6   |
+--------+-------+-------+-------+

UFP (Unadjusted Function Point) = Σ(개수 × 가중치)

STEP 4: 조정계수 적용 (VAF)

14개 일반 시스템 특성 (GSC)
1. 데이터 통신
2. 분산 데이터 처리
3. 성능
4. 운용성
5. 이중화
...

VAF = 0.65 + (0.01 × Σ(GSC Score))
    = 0.65 ~ 1.35 범위

AFP (Adjusted Function Point) = UFP × VAF

[예시]
UFP = 320
VAF = 0.65 + (0.01 × 42) = 1.07
AFP = 320 × 1.07 = 342.4 FP

LOC 변환 (Java 기준):
LOC = AFP × 46 = 342.4 × 46 = 15,750 LOC
```

### 5. 실무 코드 예시: COCOMO 계산기

```python
"""
COCOMO II 비용 산정 계산기
"""

import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict

class ProjectMode(Enum):
    """프로젝트 유형"""
    ORGANIC = "organic"          # 유기적형
    SEMI_DETACHED = "semi"       # 준분리형
    EMBEDDED = "embedded"        # 내장형

# COCOMO 계수
COCOMO_PARAMS = {
    ProjectMode.ORGANIC: {"A": 2.4, "B": 1.05, "C": 2.5, "D": 0.38},
    ProjectMode.SEMI_DETACHED: {"A": 3.0, "B": 1.12, "C": 2.5, "D": 0.35},
    ProjectMode.EMBEDDED: {"A": 3.6, "B": 1.20, "C": 2.5, "D": 0.32},
}

@dataclass
class CostEstimate:
    """비용 산정 결과"""
    size_kloc: float
    effort_pm: float           # Person-Month
    duration_months: float    # 개월
    staff_count: float        # 인원 수
    cost_usd: float           # 비용 (USD)

class COCOMOCalculator:
    """COCOMO 비용 산정 계산기"""

    def __init__(self, mode: ProjectMode, cost_per_pm: float = 15000):
        """
        Args:
            mode: 프로젝트 유형
            cost_per_pm: 인월당 비용 (USD)
        """
        self.mode = mode
        self.params = COCOMO_PARAMS[mode]
        self.cost_per_pm = cost_per_pm
        self.eaf = 1.0  # Effort Adjustment Factor

    def set_effort_adjustment_factor(self, cost_drivers: Dict[str, float]):
        """
        비용 드라이버를 기반으로 EAF 설정

        Args:
            cost_drivers: {드라이버명: 등급} 딕셔너리
                          예: {"RELY": 1.15, "CPLX": 1.30}
        """
        self.eaf = 1.0
        for driver, rating in cost_drivers.items():
            self.eaf *= rating

    def calculate(self, size_kloc: float) -> CostEstimate:
        """
        COCOMO 공식을 이용한 비용 산정

        Args:
            size_kloc: 소프트웨어 규모 (KLOC)

        Returns:
            CostEstimate: 산정 결과
        """
        A = self.params["A"]
        B = self.params["B"]
        C = self.params["C"]
        D = self.params["D"]

        # 노력 산정 (Person-Month)
        effort_pm = A * (size_kloc ** B) * self.eaf

        # 일정 산정 (Months)
        duration_months = C * (effort_pm ** D)

        # 인원 수
        staff_count = effort_pm / duration_months

        # 총 비용
        cost_usd = effort_pm * self.cost_per_pm

        return CostEstimate(
            size_kloc=size_kloc,
            effort_pm=round(effort_pm, 1),
            duration_months=round(duration_months, 1),
            staff_count=round(staff_count, 1),
            cost_usd=round(cost_usd, 0)
        )

    def estimate_from_function_points(
        self, fp: float, loc_per_fp: int = 46
    ) -> CostEstimate:
        """
        기능점수로부터 비용 산정

        Args:
            fp: 기능점수
            loc_per_fp: FP당 LOC (언어별 상이)
                       Java: 46, C: 128, Python: 22
        """
        kloc = (fp * loc_per_fp) / 1000
        return self.calculate(kloc)


# 사용 예시
if __name__ == "__main__":
    # 1. 기본 COCOMO
    calc = COCOMOCalculator(ProjectMode.SEMI_DETACHED, cost_per_pm=20000000)
    result = calc.calculate(50)  # 50 KLOC

    print("=== COCOMO 비용 산정 결과 ===")
    print(f"규모: {result.size_kloc} KLOC")
    print(f"노력: {result.effort_pm} PM (인월)")
    print(f"기간: {result.duration_months} 개월")
    print(f"인원: {result.staff_count} 명")
    print(f"비용: {result.cost_usd:,} 원")

    # 2. 중간 COCOMO (비용 드라이버 적용)
    calc.set_effort_adjustment_factor({
        "RELY": 1.15,   # 높은 신뢰성 요구
        "CPLX": 1.30,   # 높은 복잡도
        "ACAP": 0.86,   # 우수한 분석가
        "PCAP": 0.86,   # 우수한 프로그래머
        "TOOL": 0.86,   # 최신 도구
    })

    result_adjusted = calc.calculate(50)
    print("\n=== 조정된 COCOMO 결과 ===")
    print(f"EAF: {calc.eaf:.2f}")
    print(f"노력: {result_adjusted.effort_pm} PM")
    print(f"비용: {result_adjusted.cost_usd:,} 원")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 산정 기법별 정확도

| 기법 | 적용 시점 | 오차 범위 | 노력 | 적합 상황 |
| :--- | :--- | :--- | :--- | :--- |
| **전문가 판단** | 초기 | ±50~100% | 낮음 | 유사 프로젝트 경험 있을 때 |
| **LOC** | 설계 후 | ±30~50% | 중간 | 기술 스택 확정 후 |
| **FP** | 요구사항 후 | ±20~40% | 높음 | 언어 독립적 산정 필요 시 |
| **COCOMO II** | 설계 후 | ±20~30% | 중간 | 대형 프로젝트, 계약용 |
| **스토리 포인트** | 스프린트 계획 | ±20% | 낮음 | 애자일, 상대적 비교 |

### 2. 과목 융합 관점 분석

#### 비용 산정 + 위험 관리

```text
[불확실성 원뿔 (Cone of Uncertainty)]

정확도
  ^
  |                        *****
  |                    ***     ***
  |                ***             ***
  |            ***                     ***
  |        ***                             ***
  |    ***                                     ***
  |****                                             ***
  +----------------------------------------------------> 시간
   착수   요구   설계   구현   테스트   완료

   초기: ±4배 (0.25x ~ 4x)
   요구사항 완료: ±1.6배
   설계 완료: ±1.25배
   완료 직전: ±1.0배

[리스크 조정]
Basic Estimate × Risk Contingency = Final Estimate

Low Risk: × 1.1 (10% 추가)
Medium Risk: × 1.3 (30% 추가)
High Risk: × 1.5 (50% 추가)
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오

**[시나리오] 공공 SI 입찰용 비용 산정**
*   **상황**: RFP에 300개 기능 명세, 계약용 산정 필요
*   **전략**:
    1. 기능점수법으로 객관적 규모 산정 (ISO/IEC 20926)
    2. COCOMO II로 노력/일정 산정
    3. 위험 프리미엄 15% 추가
    4. 감사용 산정 근거 문서화

### 2. 주의사항

*   **브룩스의 법칙**: "지체된 프로젝트에 인력을 추가하면 더 늦어진다"
    → 일정 단축을 위해 인력 추가는 한계가 있음

*   **낙관적 편향**: 실제보다 낮게 산정하는 경향
    → PERT 3점 추정 (낙관/기대/비관)으로 보정

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### ※ 참고 표준/가이드
*   **ISO/IEC 20926**: 기능점수(FP) 산정 방법 표준
*   **ISO/IEC 19761**: COSMIC 기능점수
*   **COCOMO II**: USC(Center for Systems and Software Engineering)

---

## 📌 관련 개념 맵 (Knowledge Graph)
*   [프로젝트 관리](@/studynotes/04_software_engineering/03_project/project_management_evm.md) : 비용 산정 기반 프로젝트 통제
*   [WBS (Work Breakdown Structure)](@/studynotes/04_software_engineering/03_project/_index.md) : 범위 정의 도구
*   [요구사항 공학](@/studynotes/04_software_engineering/04_requirements/requirements_engineering.md) : 규모 산정의 입력
*   [위험 관리](@/studynotes/04_software_engineering/03_project/_index.md) : 불확실성 완화

---

## 👶 어린이를 위한 3줄 비유 설명
1. **문제**: 레고로 성을 만들기 전에 "레고 블록이 몇 개 필요할까?"를 모르겠어요.
2. **해결(비용 산정)**: 성의 크기를 먼저 정하고, 비슷한 성을 만든 경험을 참고해서 블록 수를 계산해요. "탑이 5개니까 탑마다 100개, 벽이 20개..." 이렇게요.
3. **효과**: 엄마에게 "블록 1,000개만 사줘"라고 정확히 말할 수 있어서, 다 사놓고 안 쓰거나 중간에 부족한 일이 없어요!
