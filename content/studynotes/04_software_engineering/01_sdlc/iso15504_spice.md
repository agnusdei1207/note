+++
title = "ISO/IEC 15504 (SPICE) 소프트웨어 프로세스 평가 표준"
date = "2026-03-04"
description = "소프트웨어 프로세스 역량 및 성숙도 평가를 위한 국제 표준 프레임워크"
weight = 26
+++

# ISO/IEC 15504 (SPICE) 소프트웨어 프로세스 평가 표준

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SPICE(Software Process Improvement and Capability dEtermination)는 소프트웨어 조직의 **프로세스 역량을 0~5단계로 평가**하고, 객관적이고 정량적인 방식으로 **프로세스 개선 방향을 도출**하는 국제 표준입니다.
> 2. **가치**: CMMI가 단계형(Staged) 중심인 반면, SPICE는 **연속형(Continuous) 표현**을 기본으로 하여 조직이 **선택적 프로세스 개선**을 할 수 있게 하며, 특히 **유럽 자동차 산업(Automotive SPICE)**에서 필수 평가 기준으로 활용됩니다.
> 3. **융합**: ISO 15504는 CMMI, ISO 12207과 상호 보완적이며, **프로세스 평가 모델(PAM)**과 **프로세스 개선 모델(PRM)**의 이중 구조를 통해 평가와 개선을 통합 지원합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

ISO/IEC 15504, 일명 **SPICE(Software Process Improvement and Capability dEtermination)**는 소프트웨어 프로세스의 역량 수준을 평가하기 위한 국제 표준입니다.

**SPICE의 2가지 목적**:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                        SPICE의 2가지 목적                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  🎯 목적 1: 프로세스 개선 (Process Improvement)                         │
│                                                                         │
│     조직 내부 목적:                                                     │
│     - 현재 프로세스 역량 파악                                           │
│     - 개선 우선순위 도출                                                │
│     - 개선 활동의 효과 측정                                             │
│                                                                         │
│     질문: "우리 조직은 어디가 부족하고, 무엇을 개선해야 하는가?"        │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  🏆 목적 2: 역량 결정 (Capability Determination)                        │
│                                                                         │
│     조직 외부 목적:                                                     │
│     - 공급자 선정 평가                                                  │
│     - 입찰 자격 요건                                                    │
│     - 계약상 요구사항 충족 확인                                         │
│                                                                         │
│     질문: "이 공급자가 우리 프로젝트를 수행할 역량이 있는가?"           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 💡 일상생활 비유: 학교 성적 시스템 vs 스포츠 랭킹

```
[ CMMI (단계형) - 학년제 시스템 ]

1학년 → 2학년 → 3학년 → ...
       ↑
    모든 과목을 통과해야 다음 학년으로

장점: 명확한 진행 경로
단점: 특정 과목에 재능 있어도 전체가 올라야 함

[ SPICE (연속형) - 스포츠 랭킹 시스템 ]

수영: 금메달 (Level 5)
달리기: 은메달 (Level 4)
체조: 동메달 (Level 3)
├─ 각 종목별로 독립적 평가
└─ 강점/약점이 명확히 드러남

장점: 선택적 개선 가능
      "수영은 이미 금메달이니 달리기 연습에 집중하자!"
```

### 2. 등장 배경 및 발전 과정

#### 1) 1990년대 프로세스 평가 표준화 요구

```
[ 당시의 상황 ]

미국 ─── CMM (1991) → CMMI (2002)
│        SEI 주도, 미 국방부 중심
│
유럽 ─── SPICE 프로젝트 시작 (1993)
│        ISO 주도, 다국적 참여
│        - 영국, 독일, 프랑스, 이탈리아 등
│        - 다양한 산업 분야 반영
│
문제 ─── 두 표준의 차이로 인한 혼란
        - 어느 표준을 따라야 하는가?
        - 평가 결과 비교 어려움
```

#### 2) SPICE/ISO 15504의 발전

```
[ 역사적 발전 ]

1993 ─── SPICE 프로젝트 시작 (ISO/JTC1/SC7)
    │
1998 ─── ISO/TR 15504 (기술 보고서)
    │   - 9개 파트로 구성
    │   - 시범 적용 및 피드백 수집
    │
2003~6── ISO/IEC 15504 (국제 표준)
    │   - Part 1~7 공식 발행
    │   - 평가 모델 구체화
    │
2008 ─── Automotive SPICE 확산
    │   - BMW, Volkswagen 등 유럽 완성차업체
    │   - 공급자 필수 평가 기준으로 채택
    │
2012 ─── ISO/IEC 15504 개정
    │   - ISO 12207과의 정렬 강화
    │
현재 ─── ISO/IEC 330xx 시리즈로 분화
        - ISO 33001: 개념 및 용어
        - ISO 33003: 평가 방법 요구사항
        - ISO 33004: 평가 모델 요구사항
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. SPICE 6단계 역량 수준 (Capability Levels)

CMMI가 5단계인 반면, SPICE는 **0단계(불완전)**를 포함한 6단계입니다.

| 레벨 | 명칭 | 특징 | 프로세스 속성 |
|:---:|:---|:---|:---|
| **0** | 불완전 (Incomplete) | 프로세스가 구현되지 않거나 목적 달성 실패 | - |
| **1** | 수행 (Performed) | 프로세스가 수행되어 목적 달성 | PA 1.1: 수행 |
| **2** | 관리 (Managed) | 계획되고, 모니터링되고, 조정됨 | PA 2.1: 관리, PA 2.2: 작업 산출물 관리 |
| **3** | 확립 (Established) | 표준 프로세스에 따라 수행됨 | PA 3.1: 프로세스 정의, PA 3.2: 프로세스 배포 |
| **4** | 예측 가능 (Predictable) | 정량적 목표 달성, 통계적 관리 | PA 4.1: 정량적 분석, PA 4.2: 정량적 관리 |
| **5** | 최적화 (Optimizing) | 지속적 개선, 비즈니스 목표 달성 | PA 5.1: 프로세스 혁신, PA 5.2: 프로세스 최적화 |

### 2. 정교한 구조 다이어그램: SPICE 역량 수준

```text
================================================================================
|                    SPICE CAPABILITY LEVELS ARCHITECTURE                      |
================================================================================

    Level 5: OPTIMIZING (최적화)
    ========================================
    | PA 5.1: Process Innovation            |
    | PA 5.2: Process Optimization          |
    | Focus: Continuous Improvement         |
    ========================================
                        ▲
                        │ Innovation & Optimization
                        │
    Level 4: PREDICTABLE (예측 가능)
    ========================================
    | PA 4.1: Quantitative Analysis         |
    | PA 4.2: Quantitative Management       |
    | Focus: Statistical Process Control    |
    ========================================
                        ▲
                        │ Quantitative Management
                        │
    Level 3: ESTABLISHED (확립)
    ========================================
    | PA 3.1: Process Definition            |
    | PA 3.2: Process Deployment            |
    | Focus: Standardization                |
    ========================================
                        ▲
                        │ Standard Processes
                        │
    Level 2: MANAGED (관리)
    ========================================
    | PA 2.1: Performance Management        |
    | PA 2.2: Work Product Management       |
    | Focus: Planning & Monitoring          |
    ========================================
                        ▲
                        │ Basic Management
                        │
    Level 1: PERFORMED (수행)
    ========================================
    | PA 1.1: Process Performance           |
    | Focus: Getting the job done           |
    ========================================
                        ▲
                        │ Basic Execution
                        │
    Level 0: INCOMPLETE (불완전)
    ========================================
    | No process attributes                 |
    | Focus: N/A (Chaos)                    |
    ========================================

================================================================================
|  KEY INSIGHT: 각 레벨은 이전 레벨의 모든 속성을 충족해야 달성 가능          |
================================================================================

[ 프로세스 속성 달성 등급 ]

N (Not Achieved):   0% ~ 15% 달성
P (Partially Achieved): 15% ~ 50% 달성
L (Largely Achieved):   50% ~ 85% 달성
F (Fully Achieved):     85% ~ 100% 달성

[ 레벨 달성 기준 ]
Level N 달성을 위해:
- Level N의 모든 PA가 'L' (Largely) 이상
- 또는 Level N의 PA가 'F' (Fully)
```

### 3. SPICE 프로세스 참조 모델 (PRM)

```text
[ ISO 15504 프로세스 그룹 ]

┌─────────────────────────────────────────────────────────────────────────┐
│                        PRM (Process Reference Model)                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  📌 CUS: 고객-공급자 프로세스 그룹                                      │
│     ├─ CUS.1: 소프트웨어 획득                                           │
│     ├─ CUS.2: 공급                                                      │
│     ├─ CUS.3: 요구사항 도출                                             │
│     └─ CUS.4: 운영                                                      │
│                                                                         │
│  🛠️ ENG: 공학 프로세스 그룹                                             │
│     ├─ ENG.1: 요구사항 분석                                             │
│     ├─ ENG.2: 소프트웨어 설계                                           │
│     ├─ ENG.3: 소프트웨어 구현                                           │
│     ├─ ENG.4: 소프트웨어 테스트                                         │
│     └─ ENG.5: 소프트웨어 유지보수                                       │
│                                                                         │
│  📊 MAN: 관리 프로세스 그룹                                              │
│     ├─ MAN.1: 프로젝트 관리                                             │
│     ├─ MAN.2: 품질 관리                                                 │
│     └─ MAN.3: 위험 관리                                                 │
│                                                                         │
│  🏢 ORG: 조직 프로세스 그룹                                              │
│     ├─ ORG.1: 조직 정렬                                                 │
│     ├─ ORG.2: 인력 관리                                                 │
│     └─ ORG.3: 인프라                                                    │
│                                                                         │
│  🔧 SUP: 지원 프로세스 그룹                                              │
│     ├─ SUP.1: 문서화                                                    │
│     ├─ SUP.2: 형상 관리                                                 │
│     ├─ SUP.3: 품질 보증                                                 │
│     ├─ SUP.4: 검증                                                      │
│     ├─ SUP.5: 확인                                                      │
│     └─ SUP.6: 리뷰                                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4. Automotive SPICE (ASPICE) 상세

Automotive SPICE는 자동차 산업에서 필수적인 SPICE 변형입니다.

```text
[ Automotive SPICE 프로세스 ]

┌─────────────────────────────────────────────────────────────────────────┐
│                     Automotive SPICE (ASPICE)                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  🚗 시스템 공학 프로세스 (SYS)                                          │
│     SYS.1: 요구사항 도출                                                │
│     SYS.2: 시스템 요구사항 분석                                         │
│     SYS.3: 시스템 아키텍처 설계                                         │
│     SYS.4: 시스템 통합 및 검증                                          │
│     SYS.5: 시스템 적격성 테스트                                         │
│                                                                         │
│  💻 소프트웨어 공학 프로세스 (SWE)                                      │
│     SWE.1: 소프트웨어 요구사항 분석                                     │
│     SWE.2: 소프트웨어 아키텍처 설계                                     │
│     SWE.3: 소프트웨어 상세 설계 및 단위 구현                            │
│     SWE.4: 소프트웨어 단위 검증                                         │
│     SWE.5: 소프트웨어 통합 및 검증                                      │
│     SWE.6: 소프트웨어 적격성 테스트                                     │
│                                                                         │
│  📋 획득 및 공급 프로세스 (ACQ/SUP)                                     │
│     ACQ.4: 공급자 모니터링                                              │
│     SPL.1: 공급자 공급                                                  │
│                                                                         │
│  ⚙️ 지원 프로세스 (SUP)                                                 │
│     SUP.1: 품질 보증                                                    │
│     SUP.2: 형상 관리                                                    │
│     SUP.8: 문제 해결                                                    │
│     SUP.9: 변경 요청 관리                                               │
│     SUP.10: 기술 변경 관리                                              │
│                                                                         │
│  🏢 관리 프로세스 (MAN)                                                 │
│     MAN.3: 프로젝트 관리                                                │
│     MAN.5: 위험 관리                                                    │
│                                                                         │
│  🏛️ 재사용 프로세스 (REU)                                               │
│     REU.2: 재사용 프로그램 관리                                         │
│                                                                         │
│  🔄 프로세스 개선 (PIM)                                                 │
│     PIM.1: 프로세스 개선                                                │
│                                                                         │
│  ☁️ 툴 및 기술 (TWO)                                                    │
│     TWO.1: 도구 관리                                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

[ ASPICE 평가 등급 요구사항 ]

자동차 OEM(현대, 토요타, BMW 등)의 일반적 요구사항:
- 신규 공급자: Level 2 이상
- 핵심 ECU 소프트웨어: Level 3 이상
- 안전 중요 컴포넌트 (ISO 26262 연계): Level 3+ 최우선
```

### 5. 실무 예시: SPICE 평가 결과 보고서

```python
"""
SPICE 평가 결과 분석 및 보고서 생성
"""

from dataclasses import dataclass
from typing import Dict, List
from enum import Enum

class AchievementLevel(Enum):
    """속성 달성 등급"""
    N = "Not Achieved (0-15%)"
    P = "Partially Achieved (15-50%)"
    L = "Largely Achieved (50-85%)"
    F = "Fully Achieved (85-100%)"

class CapabilityLevel(Enum):
    """역량 수준"""
    LEVEL_0 = 0
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4
    LEVEL_5 = 5

@dataclass
class ProcessAssessment:
    """프로세스 평가 결과"""
    process_id: str
    process_name: str
    pa_1_1: AchievementLevel  # Process Performance
    pa_2_1: AchievementLevel  # Performance Management
    pa_2_2: AchievementLevel  # Work Product Management
    pa_3_1: AchievementLevel  # Process Definition
    pa_3_2: AchievementLevel  # Process Deployment
    strengths: List[str]
    weaknesses: List[str]

    def calculate_capability_level(self) -> CapabilityLevel:
        """역량 수준 계산"""
        # Level 1: PA 1.1이 L 이상
        if self.pa_1_1 in [AchievementLevel.L, AchievementLevel.F]:
            # Level 2: PA 2.1, PA 2.2가 모두 L 이상
            if all([
                self.pa_2_1 in [AchievementLevel.L, AchievementLevel.F],
                self.pa_2_2 in [AchievementLevel.L, AchievementLevel.F]
            ]):
                # Level 3: PA 3.1, PA 3.2가 모두 L 이상
                if all([
                    self.pa_3_1 in [AchievementLevel.L, AchievementLevel.F],
                    self.pa_3_2 in [AchievementLevel.L, AchievementLevel.F]
                ]):
                    return CapabilityLevel.LEVEL_3
                return CapabilityLevel.LEVEL_2
            return CapabilityLevel.LEVEL_1
        return CapabilityLevel.LEVEL_0

class SPICEAssessmentReport:
    """SPICE 평가 보고서"""

    def __init__(self, organization_name: str):
        self.organization_name = organization_name
        self.assessments: Dict[str, ProcessAssessment] = {}

    def add_assessment(self, assessment: ProcessAssessment):
        self.assessments[assessment.process_id] = assessment

    def generate_report(self) -> str:
        """평가 보고서 생성"""
        report = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    SPICE 프로세스 평가 보고서                               ║
╠═══════════════════════════════════════════════════════════════════════════╣
║ 조직명: {self.organization_name:<60} ║
╠═══════════════════════════════════════════════════════════════════════════╣
║ 프로세스별 역량 수준                                                       ║
╠═══════════════════════════════════════════════════════════════════════════╣
"""

        # 프로세스별 결과
        for process_id, assessment in self.assessments.items():
            level = assessment.calculate_capability_level()
            level_str = f"Level {level.value}"
            report += f"║ {process_id}: {assessment.process_name:<20} → {level_str:<10}          ║\n"

        # 요약 통계
        level_counts = {}
        for assessment in self.assessments.values():
            level = assessment.calculate_capability_level()
            level_counts[level] = level_counts.get(level, 0) + 1

        report += "╠═══════════════════════════════════════════════════════════════════════════╣\n"
        report += "║ 수준별 분포                                                               ║\n"
        for level in CapabilityLevel:
            count = level_counts.get(level, 0)
            bar = "█" * count
            report += f"║   Level {level.value}: {bar:<30} ({count}개)         ║\n"

        # 강점/약점 요약
        report += "╠═══════════════════════════════════════════════════════════════════════════╣\n"
        report += "║ 주요 강점                                                                 ║\n"
        all_strengths = []
        for assessment in self.assessments.values():
            all_strengths.extend(assessment.strengths)
        for strength in all_strengths[:5]:
            report += f"║   ✅ {strength:<65} ║\n"

        report += "║                                                                           ║\n"
        report += "║ 개선 필요 영역                                                            ║\n"
        all_weaknesses = []
        for assessment in self.assessments.values():
            all_weaknesses.extend(assessment.weaknesses)
        for weakness in all_weaknesses[:5]:
            report += f"║   ⚠️ {weakness:<65} ║\n"

        report += "╚═══════════════════════════════════════════════════════════════════════════╝"
        return report

# 사용 예시
if __name__ == "__main__":
    report = SPICEAssessmentReport("XYZ 자동차 부품 (주)")

    # 샘플 평가 결과
    assessments = [
        ProcessAssessment(
            process_id="SWE.1",
            process_name="요구사항 분석",
            pa_1_1=AchievementLevel.F,
            pa_2_1=AchievementLevel.L,
            pa_2_2=AchievementLevel.L,
            pa_3_1=AchievementLevel.P,
            pa_3_2=AchievementLevel.P,
            strengths=["명확한 요구사항 문서화", "이해관계자 참여"],
            weaknesses=["추적성 관리 미흡", "표준 프로세스 미정의"]
        ),
        ProcessAssessment(
            process_id="SWE.2",
            process_name="아키텍처 설계",
            pa_1_1=AchievementLevel.F,
            pa_2_1=AchievementLevel.F,
            pa_2_2=AchievementLevel.L,
            pa_3_1=AchievementLevel.L,
            pa_3_2=AchievementLevel.L,
            strengths=["체계적 설계 리뷰", "명확한 인터페이스 정의"],
            weaknesses=["설계 대안 분석 부족"]
        ),
        ProcessAssessment(
            process_id="SWE.3",
            process_name="상세 설계 및 구현",
            pa_1_1=AchievementLevel.L,
            pa_2_1=AchievementLevel.P,
            pa_2_2=AchievementLevel.P,
            pa_3_1=AchievementLevel.N,
            pa_3_2=AchievementLevel.N,
            strengths=["코딩 표준 준수"],
            weaknesses=["코드 리뷰 프로세스 미흡", "단위 테스트 커버리지 낮음"]
        ),
    ]

    for assessment in assessments:
        report.add_assessment(assessment)

    print(report.generate_report())
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: SPICE vs CMMI

| 비교 항목 | SPICE (ISO 15504) | CMMI |
|:---:|:---|:---|
| **기원** | 유럽/ISO | 미국/SEI |
| **표현 방식** | 연속형(Continuous) 기본 | 단계형(Staged) + 연속형 |
| **레벨 수** | 6단계 (0~5) | 5단계 (1~5) |
| **평가 방식** | 프로세스별 독립 평가 | 전체 성숙도 등급 |
| **유연성** | 높음 (선택적 개선) | 중간 |
| **주요 적용** | 유럽 자동차(ASPICE) | 미 국방, 공공 SI |
| **ISO 표준** | O | X (ISACA 관리) |

### 2. SPICE vs CMMI 레벨 매핑

```text
[ 레벨 매핑 ]

SPICE                CMMI
───────────────────────────────
Level 5: 최적화  ←→  Level 5: 최적화
Level 4: 예측    ←→  Level 4: 정량적관리
Level 3: 확립    ←→  Level 3: 정의
Level 2: 관리    ←→  Level 2: 관리
Level 1: 수행    ←→  Level 1: 초기
Level 0: 불완전  ←→  (해당 없음)

[ 핵심 차이점 ]

CMMI (단계형):
┌─────────────────────────────────────────────┐
│  Level 3                                    │
│  ┌─────────────────────────────────────────┐│
│  │  모든 프로세스가 Level 3 수준           ││
│  └─────────────────────────────────────────┘│
└─────────────────────────────────────────────┘

SPICE (연속형):
┌─────────────────────────────────────────────┐
│  요구분석: Level 3  ████████               │
│  설계:     Level 4  ████████████           │
│  구현:     Level 2  █████                  │
│  테스트:   Level 3  ████████               │
└─────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오

**[시나리오] 자동차 부품업체 ASPICE 평가 대응**

```
상황:
- 유럽 OEM(BMW) 공급자 등록 필요
- ASPICE Level 2 이상 요구
- 현재 역량 불확실

기술사적 판단:

1️⃣ 현황 진단 (Diagnostic Assessment)
   - 주요 프로세스 16개 평가
   - 현재 수준 파악: 평균 Level 1.5

2️⃣ Gap 분석
   - 목표 vs 현황 격차 식별
   - 우선 개선 프로세스 선정:
     * MAN.3 프로젝트 관리
     * SUP.2 형상 관리
     * SWE.1 요구사항 분석

3️⃣ 개선 계획 수립
   - 18개월 로드맵
   - Phase 1 (6개월): Level 2 달성
   - Phase 2 (6개월): Level 2 안정화
   - Phase 3 (6개월): 정식 평가

4️⃣ 평가 대응
   - 증거(Evidence) 체계적 관리
   - 인터뷰 준비
   - 시연 준비

결과:
- 목표: Level 2
- 달성: Level 2 (일부 Level 3)
- BMW 공급자 등록 성공
```

### 2. 도입 시 고려사항

```text
[ SPICE/ASPICE 도입 체크리스트 ]

✅ 비즈니스 필요성
□ 고객(OEM)의 ASPICE 요구사항인가?
□ 유럽 시장 진출 목표인가?
□ 프로세스 개선의 객관적 척도가 필요한가?

✅ 조직 준비도
□ 평가 담당자 교육 이수했는가?
□ 프로세스 문서화가 어느 정도 되어 있는가?
□ 증거 자료(Evidence) 관리 체계가 있는가?

✅ 리소스
□ 18~24개월 개선 기간 확보 가능한가?
□ 전담 인력 배치 가능한가?
□ 외부 컨설팅 필요한가?
```

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 효과 |
|:---:|:---|
| **정량적** | 결함률 30~50% 감소 |
| **정량적** | 프로젝트 성공률 25% 향상 |
| **정성적** | 유럽 OEM 공급자 등록 |
| **정성적** | 프로세스 약점 식별 및 개선 |

### 2. 미래 전망

```
SPICE의 미래:

1. ISO 330xx 시리즈로 진화
   - 더 명확한 평가 방법론
   - 다양한 도메인 적용

2. Automotive SPICE 4.0
   - 자율주행, 커넥티드카 대응
   - AI/ML 개발 프로세스 포함

3. Agile SPICE
   - 애자일 방법론과의 융합
   - 유연한 평가 기준
```

### ※ 참고 표준/가이드

- **ISO/IEC 15504**: SPICE 공식 표준
- **Automotive SPICE PAM**: 자동차 산업용 평가 모델
- **intacs**: SPICE 평가자 인증 기관
- **VDA QMC**: Automotive SPICE 공식 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [CMMI](@/studynotes/04_software_engineering/01_sdlc/cmmi.md) : 유사한 성숙도 모델
- [ISO 12207](./) : 프로세스 정의 표준
- [프로젝트 관리](@/studynotes/04_software_engineering/03_project/project_management_evm.md) : MAN 프로세스 그룹
- [형상 관리](@/studynotes/04_software_engineering/01_sdlc/configuration_management.md) : SUP 프로세스

---

## 👶 어린이를 위한 3줄 비유 설명

1. **문제**: 피아노를 배우는데 "연습 좀 더 해"라고만 하니까 뭘 어떻게 해야 할지 모르겠어요.

2. **해결(SPICE)**: 선생님이 "음계는 3단계, 건반은 2단계, 리듬은 1단계야"라고 알려줬어요. 이제 "리듬 연습에 집중하자"라고 정확히 알 수 있죠.

3. **효과**: 약점이 뭔지 정확히 알아서 연습하니까 실력이 쑥쑥 늘어요. 그리고 나중에 오디션 볼 때도 "리듬은 이미 3단계예요"라고 자랑할 수 있죠!
