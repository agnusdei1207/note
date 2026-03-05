+++
title = "CMMI (Capability Maturity Model Integration)"
date = 2024-05-24
description = "소프트웨어 개발 조직의 성숙도 수준을 평가하고 프로세스 개선을 유도하는 국제 표준 모델"
weight = 30
+++

# CMMI (Capability Maturity Model Integration)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CMMI는 소프트웨어 개발 조직의 **프로세스 성숙도를 5단계(초기→관리→정의→정량적관리→최적화)**로 평가하고, 체계적인 프로세스 개선을 통해 **예측 가능한 고품질 소프트웨어**를 개발할 수 있도록 돕는 국제 표준 모델입니다.
> 2. **가치**: 프로세스 성숙도가 1단계에서 3단계로 향상될 경우 **일정 준수율 30% 향상, 결함 밀도 40% 감소** 등 정량적 품질 개선 효과가 입증되어 있으며, 특히 공공/국방 SI 프로젝트의 **입찰 자격 요건**으로 활용됩니다.
> 3. **융합**: 기존의 단계형(Staged) 표현과 연속형(Continuous) 표현을 모두 지원하며, 애자일/DevOps와 대립되는 것이 아니라 **애자일 조직의 프로세스 표준화**를 위한 프레임워크로 진화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의
CMMI(Capability Maturity Model Integration)는 미국 카네기 멜런 대학교의 **SEI(Software Engineering Institute)**에서 개발한 프로세스 성숙도 평가 모델입니다. 1991년 CMM(Capability Maturity Model)로 시작하여, 2002년 CMMI로 통합되었고, 현재 **CMMI V2.0(2018)**이 최신 버전입니다.

**CMMI의 3대 핵심 구성**:
1. **프로세스 영역(Process Areas)**: 개선해야 할 핵심 활동 영역
2. **목표(Goals)**: 각 프로세스 영역에서 달성해야 하는 목표
3. **실천사항(Practices)**: 목표 달성을 위한 구체적 활동

### 💡 일상생활 비유: 요리 학교의 등급 시스템
CMMI는 요리 학교의 등급 시스템과 유사합니다.

```
[Level 1: 초기형] - "집에서 혼자 요리하는 사람"
- 레시피 없이 감으로 요리
- 맛이 들쑥날쑥
- 재료가 부족하면 그냥 안 만듦
- "운"에 따라 성패 결정

[Level 2: 관리형] - "패밀리 레스토랑 주방"
- 기본 레시피 존재
- 비슷한 맛 유지
- 재료 발주 계획 있음
- 하지만 요리사마다 차이 존재

[Level 3: 정의형] - "프랜차이즈 레스토랑"
- 표준화된 레시피 매뉴얼
- 누가 만들어도 같은 맛
- 교육 프로그램 체계화
- 품질 검사 프로세스 존재

[Level 4: 정량적 관리형] - "미슐랭 레스토랑"
- 모든 요리 과정을 수치화
- 온도, 시간, 재료 양 정밀 측정
- 통계적 품질 관리
- 목표 대비 실적 실시간 추적

[Level 5: 최적화형] - "세계 최고의 요리 연구소"
- 지속적인 레시피 개선
- 신기술/신재료 적극 도입
- 혁신적인 조리법 연구
- 업계 벤치마킹 대상
```

### 2. 등장 배경 및 발전 과정

#### 1) 1980년대 소프트웨어 위기와 미 국방부의 요구
미 국방부는 소프트웨어 프로젝트의 **60% 이상이 예산 초과, 일정 지연, 품질 미달**로 실패하는 것을 문제로 인식했습니다. 이를 해결하기 위해 소프트웨어 개발업체의 **객관적 능력 평가 기준**이 필요했습니다.

#### 2) 1991년 CMM의 탄생
웨스 험프리(Watts Humphrey)가 이끄는 SEI 팀이 **CMM(Capability Maturity Model for Software)**을 발표했습니다. 이는 소프트웨어 개발 조직의 성숙도를 5단계로 평가하는 최초의 모델이었습니다.

#### 3) 2002년 CMMI로 통합
CMM이 소프트웨어(SW-CMM), 시스템 공학(SE-CMM), 인적 자원(P-CMM) 등으로 분산되면서 혼란이 발생했습니다. 이를 **CMMI로 통합**하여 일관된 프레임워크를 제공하게 되었습니다.

#### 4) CMMI V2.0 (2018)의 진화
- 애자일/DevOps와의 통합 가이드 추가
- 서비스(CMMI-SVC), 획득(CMMI-ACQ) 영역 통합
- 실천사항의 유연성 증대

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. CMMI 5단계 성숙도 모델

| 레벨 | 명칭 | 특징 | 프로세스 특성 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **1** | 초기형 (Initial) | 혼돈, 예측 불가 | 프로세스 없음, 개인 역량 의존 | 야생의 요리사 |
| **2** | 관리형 (Managed) | 프로젝트 단위 관리 | 기본 프로젝트 관리, 요구사항 관리 | 가정식 레스토랑 |
| **3** | 정의형 (Defined) | 조직 표준 프로세스 | 표준 프로세스, 조직 차원 교육 | 프랜차이즈 |
| **4** | 정량적 관리형 (Quantitatively Managed) | 통계적 관리 | 정량적 목표, 통계적 프로세스 관리 | 미슐랭 레스토랑 |
| **5** | 최적화형 (Optimizing) | 지속적 개선 | 프로세스 혁신, 기술 도입 | 요리 연구소 |

### 2. 정교한 구조 다이어그램: CMMI 5단계 레벨

```text
================================================================================
|                     CMMI MATURITY LEVELS ARCHITECTURE                         |
================================================================================

    Level 5: OPTIMIZING (최적화형)
    ========================================
    | Focus: Continuous Process Improvement |
    | - Process Innovation                  |
    | - Causal Analysis & Resolution (CAR)  |
    | - Organizational Performance Mgmt     |
    ========================================
                        ^
                        | Innovation & Optimization
                        v
    Level 4: QUANTITATIVELY MANAGED (정량적 관리형)
    ========================================
    | Focus: Statistical Process Control    |
    | - Organizational Process Performance  |
    | - Quantitative Project Management     |
    | - Statistical Predictions             |
    ========================================
                        ^
                        | Quantitative Management
                        v
    Level 3: DEFINED (정의형)
    ========================================
    | Focus: Standardization                |
    | - Requirements Development            |
    | - Technical Solution                  |
    | - Product Integration                 |
    | - Verification & Validation           |
    | - Organizational Process Definition   |
    ========================================
                        ^
                        | Standard Processes
                        v
    Level 2: MANAGED (관리형)
    ========================================
    | Focus: Project Management             |
    | - Requirements Management             |
    | - Project Planning                    |
    | - Project Monitoring & Control        |
    | - Supplier Agreement Management       |
    | - Measurement & Analysis              |
    | - Process & Product Quality Assurance |
    | - Configuration Management            |
    ========================================
                        ^
                        | Basic Management
                        v
    Level 1: INITIAL (초기형)
    ========================================
    | Focus: Individual Heroics             |
    | - Ad-hoc processes                    |
    | - Success depends on individuals      |
    | - Unpredictable outcomes              |
    ========================================

    KEY INSIGHT:
    ===========
    - Each level builds on the previous level
    - Skipping levels is NOT recommended
    - Level 3 is the "Tipping Point" for consistent quality

================================================================================
```

### 3. 심층 동작 원리: 레벨별 핵심 프로세스 영역

#### Level 2: 관리형 (Managed) 핵심 PA

| 프로세스 영역 | 목적 | 핵심 실천사항 |
| :--- | :--- | :--- |
| **요구사항 관리 (REQM)** | 요구사항 변경 통제 | 요구사항 추적성, 변경 심의 |
| **프로젝트 계획 (PP)** | 현실적 계획 수립 | WBS, 일정/자원 산정, 이해관계자 참여 |
| **프로젝트 모니터링 (PMC)** | 진척 관리 및 시정 | 이슈 추적, 마일스톤 검토, 시정 조치 |
| **공급자 계약 관리 (SAM)** | 외부 공급자 관리 | 공급자 선정, 계약, 성과 모니터링 |
| **측정 및 분석 (MA)** | 데이터 기반 의사결정 | 측정 목표 정의, 데이터 수집/분석 |
| **품질 보증 (PPQA)** | 프로세스 준수 검증 | 감사, 비준수 보고, 시정 조치 |
| **형상 관리 (CM)** | 작업 산출물 관리 | 형상 식별, 기준선 관리, 변경 통제 |

#### Level 3: 정의형 (Defined) 핵심 PA

| 프로세스 영역 | 목적 | 핵심 실천사항 |
| :--- | :--- | :--- |
| **요구사항 개발 (RD)** | 요구사항 도출 및 분석 | 이해관계자 니즈, 기능/비기능 요구사항 |
| **기술 솔루션 (TS)** | 설계 및 구현 | 아키텍처, 컴포넌트 설계, 구현 |
| **제품 통합 (PI)** | 컴포넌트 통합 | 통합 순서, 인터페이스 검증 |
| **검증 (VER)** | 올바르게 만들었는가 | 동료 검토, 테스트 수행 |
| **확인 (VAL)** | 올바른 것을 만들었는가 | 인수 테스트, 사용자 검증 |
| **조직 프로세스 정의 (OPD)** | 표준 프로세스 수립 | 조직 표준 프로세스, 테일러링 가이드 |
| **조직 프로세스 집중 (OPF)** | 프로세스 개선 | 프로세스 개선 제안, 배포 |

### 4. 실무 예시: Level 2 달성을 위한 체크리스트

```python
"""
CMMI Level 2 달성 체크리스트 (간소화 버전)
실제 평가에서는 증거(Evidence) 문서가 필요
"""

class CMMILevel2Assessment:
    """CMMI Level 2 달성 여부 자가 진단"""

    def __init__(self, organization_name: str):
        self.org = organization_name
        self.results = {}

    def assess_requirements_management(self) -> dict:
        """요구사항 관리 (REQM) 평가"""
        checklist = {
            "SG1: 요구사항 관리":
                [
                    ("요구사항이 이해관계자와 합의되었는가?", False),
                    ("요구사항 변경이 공식 프로세스를 통해 이루어지는가?", False),
                    ("요구사항 추적 매트릭스(RTM)가 유지되는가?", False),
                    ("요구사항과 작업 산출물 간 일관성이 유지되는가?", False),
                ]
        }
        return self._evaluate(checklist)

    def assess_project_planning(self) -> dict:
        """프로젝트 계획 (PP) 평가"""
        checklist = {
            "SG1: 추정":
                [
                    ("프로젝트 범위가 정의되었는가?", False),
                    ("작업 분할 구조(WBS)가 작성되었는가?", False),
                    ("일정 및 비용이 현실적으로 추정되었는가?", False),
                ],
            "SG2: 계획 수립":
                [
                    ("프로젝트 계획서가 문서화되었는가?", False),
                    ("이해관계자가 계획을 검토했는가?", False),
                    ("리스크가 식별되고 완화 계획이 있는가?", False),
                ]
        }
        return self._evaluate(checklist)

    def assess_configuration_management(self) -> dict:
        """형상 관리 (CM) 평가"""
        checklist = {
            "SG1: 기준선 확립":
                [
                    ("형상 항목이 식별되었는가?", False),
                    ("형상 관리 시스템이 구축되었는가?", False),
                    ("기준선(Baseline)이 생성되고 공표되었는가?", False),
                ],
            "SG2: 변경 추적 및 통제":
                [
                    ("변경 요청이 공식적으로 관리되는가?", False),
                    ("변경의 영향도가 분석되는가?", False),
                    ("형상 감사가 수행되는가?", False),
                ]
        }
        return self._evaluate(checklist)

    def _evaluate(self, checklist: dict) -> dict:
        """체크리스트 평가 (실제로는 사용자 입력 필요)"""
        total = 0
        checked = 0
        for category, items in checklist.items():
            for question, status in items:
                total += 1
                if status:
                    checked += 1
        return {
            "score": f"{checked}/{total}",
            "percentage": (checked / total) * 100 if total > 0 else 0,
            "satisfied": checked == total
        }

    def get_overall_assessment(self) -> str:
        """종합 평가 결과"""
        assessments = {
            "REQM": self.assess_requirements_management(),
            "PP": self.assess_project_planning(),
            "CM": self.assess_configuration_management(),
        }

        all_satisfied = all(a["satisfied"] for a in assessments.values())

        if all_satisfied:
            return f"✅ {self.org}은(는) CMMI Level 2 달성 준비가 되었습니다."
        else:
            return f"⚠️ {self.org}은(는) 일부 PA에서 미달성 항목이 있습니다."
```

### 5. CMMI 평가 방법 (SCAMPI)

| 평가 유형 | 목적 | 소요 시간 | 산출물 |
| :--- | :--- | :--- | :--- |
| **SCAMPI A** | 공식 평가 (인증용) | 1~2주 | 공식 등급 부여 |
| **SCAMPI B** | 준비 상태 진단 | 3~5일 | 개선 권고사항 |
| **SCAMPI C** | 간편 진단 | 1~3일 | 빠른 피드백 |

**SCAMPI A 평가 프로세스**:
1. 계획 수립 (Plan) - 평가 범위, 일정, 참여자
2. 준비 (Prepare) - 설문, 문서 검토
3. 평가 수행 (Conduct) - 인터뷰, 문서 검증
4. 결과 보고 (Report) - 강점/약점, 등급 부여

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: CMMI vs ISO 9001 vs SPICE

| 비교 항목 | CMMI | ISO 9001 | SPICE (ISO 15504) |
| :--- | :--- | :--- | :--- |
| **대상** | 소프트웨어/시스템 개발 | 모든 산업 | 소프트웨어 프로세스 |
| **구조** | 5단계 성숙도 | 인증(Pass/Fail) | 6단계 역량 수준 |
| **초점** | 프로세스 개선 | 품질 경영 시스템 | 프로세스 역량 평가 |
| **유연성** | 중간 (테일러링 가능) | 높음 (해석 여지) | 높음 (연속형) |
| **업데이트** | CMMI V2.0 (2018) | ISO 9001:2015 | ISO 15504:2012 |
| **주요 적용** | 미 국방부, 공공 SI | 제조, 서비스 전반 | 유럽, 자동차 |

### 2. 과목 융합 관점 분석

#### CMMI + 애자일

```text
[전통적 인식 - 대립]
CMMI: "문서화, 표준 프로세스, 통제"
애자일: "동작하는 코드, 개인과 상호작용, 변화 수용"
→ 서로 상충한다?

[현대적 인식 - 통합]
CMMI: "무엇을(What) 달성해야 하는가"
애자일: "어떻게(How) 달성할 것인가"

[애자일 조직의 CMMI 적용 예시]
Level 2 요구사항 관리:
  - CMMI: "요구사항을 관리하라"
  - 애자일: 제품 백로그, 스프린트 백로그로 관리

Level 3 검증/확인:
  - CMMI: "검증과 확인을 수행하라"
  - 애자일: TDD, 지속적 통합, 스프린트 리뷰

Level 5 지속적 개선:
  - CMMI: "프로세스를 최적화하라"
  - 애자일: 스프린트 회고, Kaizen
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 및 기술사적 의사결정

**[시나리오 1] 공공 SI 기업의 CMMI Level 3 인증 획득**
*   **상황**: 정부 발주 대형 SI 사업 입찰에 CMMI Level 3 이상이 필수 조건으로 추가됨
*   **기술사적 판단**: 18개월 로드맵 수립
    *   **Phase 1 (6개월)**: 현황 진단, 갭 분석, 개선 계획 수립
    *   **Phase 2 (6개월)**: 표준 프로세스 정의, 파일럿 프로젝트 적용
    *   **Phase 3 (6개월)**: 전사 확산, SCAMPI B 진단, SCAMPI A 평가

**[시나리오 2] 스타트업의 선택적 CMMI 실천**
*   **상황**: 빠른 성장, 품질 문제 증가, 하지만 공식 인증은 과도한 비용
*   **기술사적 판단**: Level 2 핵심 실천만 선별 도입
    *   형상 관리(CM): Git/GitHub 도입
    *   요구사항 관리(REQM): Jira 백로그 관리
    *   측정 및 분석(MA): DORA 메트릭 측정
    *   공식 인증은 추후 비즈니스 필요 시 검토

### 2. 도입 시 고려사항 (체크리스트)

**비즈니스 필요성**:
- [ ] 입찰 요구사항: 고객/시장에서 CMMI 인증을 요구하는가?
- [ ] 품질 문제: 현재 프로세스로 품질 문제가 빈발하는가?
- [ ] 조직 규모: 평가 비용 대비 효용이 있는가?

**조직 준비도**:
- [ ] 경영진 의지: 최고 경영진이 개선을 지원하는가?
- [ ] 프로세스 문화: 문서화와 프로세스 준수 문화가 있는가?
- [ ] 전담 조직: EPG(Engineering Process Group) 구성 가능한가?

### 3. 주의사항 및 안티패턴

*   **페이퍼웍 헬(Paperwork Hell)**: 문서만 작성하고 실제 프로세스는 따르지 않는 경우
    → CMMI는 **"문서가 아니라 실천"**이 핵심입니다. 평가에서도 실제 수행 여부를 검증합니다.

*   **레벨 순서 건너뛰기**: Level 1에서 바로 Level 3로 가려는 시도
    → 각 레벨은 **전제 조건(Pre-requisite)**입니다. 기초 없이 고급 단계는 지속 불가능합니다.

*   **개선 중단**: 인증 획득 후 개선 활동 중단
    → CMMI Level 5의 핵심은 **지속적 개선**입니다. 인증은 시작점이지 종착점이 아닙니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 지표 | Level 1 → Level 3 개선 효과 | 출처 |
| :--- | :--- | :--- | :--- |
| **일정 준수** | 프로젝트 일정 준수율 | 30% 향상 | SEI 보고서 |
| **비용 통제** | 예산 초과율 | 25% 감소 | SEI 보고서 |
| **품질** | 결함 밀도 (Defects/KLOC) | 40% 감소 | SEI 보고서 |
| **생산성** | LOC/인월 | 15% 향상 | SEI 보고서 |
| **고객 만족** | 고객 만족도 | 20% 향상 | 산업별 차이 |

### 2. 미래 전망 및 진화 방향

1.  **CMMI V3.0 (예정)**: AI/ML 기반 개발, 보안(Security) 영역 강화
2.  **애자일-CMMI 통합**: CMMI가 애자일 방법론을 공식적으로 인정하는 가이드 지속 강화
3.  **자동화된 평가**: 도구 기반 증거 수집으로 평가 효율화

### ※ 참고 표준/가이드
*   **CMMI Institute (ISACA)**: 공식 CMMI 기관 (cmmiinstitute.com)
*   **CMMI for Development (CMMI-DEV)**: 개발 조직용 CMMI
*   **CMMI for Services (CMMI-SVC)**: 서비스 조직용 CMMI
*   **ISO/IEC 15504 (SPICE)**: 유럽 중심의 프로세스 평가 표준

---

## 📌 관련 개념 맵 (Knowledge Graph)
*   [소프트웨어 품질 관리](@/studynotes/04_software_engineering/02_quality/software_quality_standards.md) : CMMI의 품질 목표
*   [형상 관리](@/studynotes/04_software_engineering/01_sdlc/_index.md) : Level 2 핵심 프로세스 영역
*   [프로젝트 관리](@/studynotes/04_software_engineering/03_project/project_management_evm.md) : CMMI Level 2의 핵심
*   [애자일 방법론](@/studynotes/04_software_engineering/01_sdlc/agile_methodology.md) : CMMI와 통합 가능한 방법론
*   [ISO 9001](@/studynotes/04_software_engineering/02_quality/_index.md) : 유사한 품질 경영 표준

---

## 👶 어린이를 위한 3줄 비유 설명
1. **문제**: 요리 대회에 나갔는데, 어떤 사람은 레시피 없이 감으로 요리하고, 어떤 사람은 매번 다른 방법으로 요리해요. 누가 잘하는지 모르겠어요!
2. **해결(CMMI)**: 요리 학교에 5단계 등급을 만들었어요. 1단계는 아무렇게나 요리, 2단계는 레시피대로만 요리, 3단계는 표준 레시피 매뉴얼을 만들어서 누구나 같은 맛, ... 5단계는 계속 연구해서 더 맛있게!
3. **효과**: 이제 어떤 요리사가 믿을 만한지 등급을 보면 알 수 있어요. 등급이 높을수록 맛있는 요리를 기대할 수 있죠!
