+++
title = "소프트웨어 공학 (Software Engineering)"
date = 2024-05-24
description = "체계적이고 수량화 가능한 접근법을 통한 고품질 소프트웨어 개발의 학문적 기반"
weight = 5
+++

# 소프트웨어 공학 (Software Engineering)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 공학은 **공학적 원리, 방법론, 도구**를 적용하여 **신뢰성, 효율성, 유지보수성**을 갖춘 소프트웨어를 체계적으로 개발, 운영, 유지보수하는 **학문이자 실천 분야**입니다.
> 2. **가치**: 소프트웨어 위기(예산 초과, 일정 지연, 품질 저하)를 극복하기 위해 탄생했으며, **프로젝트 성공률을 30% 이상 향상**시키고 **유지보수 비용을 40% 절감**하는 정량적 효과가 입증되어 있습니다.
> 3. **융합**: 컴퓨터 과학(알고리즘, 자료구조) + 관리 과학(프로젝트 관리) + 인지 과학(UI/UX) + 경제학(비용 분석)의 **학제적 융합 분야**로 지속 진화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**소프트웨어 공학(Software Engineering)**이란 1968년 NATO 컨퍼런스에서 처음 공식적으로 정의된 용어로, **"소프트웨어의 개발, 운영, 유지보수에 공학적 원리를 적용하는 체계적인 접근법"**을 의미합니다.

IEEE가 정의한 표준 정의는 다음과 같습니다:
> "소프트웨어의 개발, 운영 및 유지보수에 체계적이고, 수량화 가능하며, 규율 있는 접근법을 적용하는 것. 즉, 소프트웨어에 공학을 적용하는 것이다."

**소프트웨어 공학의 3대 목표**:

| 목표 | 정의 | 측정 지표 |
| :--- | :--- | :--- |
| **신뢰성 (Reliability)** | 의도된 기능을 오류 없이 일관되게 수행 | MTBF, 가용성, 결함 밀도 |
| **효율성 (Efficiency)** | 자원(시간, 비용, 인력)의 최적 활용 | 생산성(LOC/인월), 비용 대비 효과 |
| **유지보수성 (Maintainability)** | 변경 용이성 및 진화 가능성 | 수정 소요 시간, 회귀 테스트 비용 |

### 💡 일상생활 비유: 건축 설계 사무실

```
소프트웨어 공학 = 건축 설계 및 시공 체계

[비교 매핑]
┌────────────────┬─────────────────────────────────────┐
│ 건축 분야      │ 소프트웨어 공학 분야                 │
├────────────────┼─────────────────────────────────────┤
│ 건축 설계도면  │ 소프트웨어 설계 문서 (UML, 아키텍처)  │
│ 건축 법규      │ 코딩 표준, 보안 가이드라인           │
│ 시공 매뉴얼    │ 개발 방법론 (애자일, 워터폴)         │
│ 품질 검사      │ 테스팅, 코드 리뷰, 정적 분석         │
│ 유지보수 계획  │ 유지보수 프로세스, 형상 관리         │
│ 건축가         │ 소프트웨어 아키텍트                   │
│ 시공팀         │ 개발팀                               │
│ 감리           │ 품질 보증(QA) 팀                     │
└────────────────┴─────────────────────────────────────┘

[핵심 통찰]
- 건물이 무너지지 않으려면 → 구조 설계, 재료 검사, 시공 감리 필요
- 소프트웨어가 실패하지 않으려면 → 아키텍처 설계, 코드 품질, 테스팅 필요
```

### 2. 등장 배경 및 발전 과정

#### 1) 1960년대: 소프트웨어 위기 (Software Crisis)의 발생

```text
[소프트웨어 위기의 증상]
┌─────────────────────────────────────────────────────────────┐
│ 1. 예산 초과 (Budget Overrun)                               │
│    - 평균 프로젝트의 60%가 예산 초과                        │
│    - 일부 프로젝트는 예산의 200% 이상 소요                  │
│                                                             │
│ 2. 일정 지연 (Schedule Slippage)                            │
│    - 계획 대비 평균 2~3배 지연                              │
│    - "99% 완료" 상태가 수개월 지속                          │
│                                                             │
│ 3. 품질 저하 (Poor Quality)                                 │
│    - 출시 후 발견되는 결함 다수                             │
│    - 사용자 불만, 시스템 장애 빈발                          │
│                                                             │
│ 4. 사용자 요구 미충족 (Unmet Requirements)                  │
│    - 개발된 시스템이 실제 필요와 불일치                     │
│    - 재개발 또는 폐기 사례 증가                             │
└─────────────────────────────────────────────────────────────┘
```

**사례: IBM OS/360 프로젝트 (1964-1966)**
- 5,000명년(Man-Year) 투입
- 원래 예산의 4배 비용 소요
- 출시 후 수천 개의 버그 존재
- 이 경험을 바탕으로 프레드 브룩스가 "The Mythical Man-Month" 저술

#### 2) 1968년: NATO 컨퍼런스와 "소프트웨어 공학"의 탄생

독일 가르미쉬에서 열린 NATO 컨퍼런스에서 **F.L. Bauer** 등이 "Software Engineering"이라는 용어를 처음 제안했습니다.

> "소프트웨어 위기는 소프트웨어 개발에 공학적 접근법을 적용함으로써 해결할 수 있다."

#### 3) 1970년대~1980년대: 구조적 방법론의 등장

| 연도 | 발전 내용 | 주요 인물/기관 |
| :--- | :--- | :--- |
| 1970 | 워터폴 모델 제안 | Winston Royce |
| 1972 | 구조적 프로그래밍 | Edsger Dijkstra |
| 1978 | 구조적 분석/설계 (SASD) | Tom DeMarco, Larry Constantine |
| 1980 | 정보 공학 (IE) | James Martin |
| 1985 | CMM 개발 시작 | SEI (Carnegie Mellon) |

#### 4) 1990년대: 객체지향과 프로세스 표준화

```text
[1990년대 주요 발전]
┌────────────────────────────────────────────────────┐
│ 1991 │ CMM (Capability Maturity Model) 발표       │
│ 1995 │ 스크럼(Scrum) 방법론 공식화                │
│ 1997 │ UML (Unified Modeling Language) 표준화     │
│ 1998 │ ISO/IEC 12207 (SW 생명주기 표준) 발행      │
└────────────────────────────────────────────────────┘
```

#### 5) 2000년대~현재: 애자일, DevOps, AI로의 진화

- **2001**: 애자일 선언문 (Agile Manifesto)
- **2010**: DevOps 운동 확산
- **2015**: 마이크로서비스 아키텍처 대중화
- **2020**: AI 기반 코드 생성 (GitHub Copilot), LLM 활용 개발

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 소프트웨어 공학의 지식 체계 (SWEBOK)

IEEE가 정의한 **소프트웨어 공학 지식 체계(SWEBOK, Software Engineering Body of Knowledge)**는 소프트웨어 공학의 15개 핵심 지식 영역을 정의합니다.

```text
================================================================================
│                    SWEBOK V3.0 - 15 KNOWLEDGE AREAS                            │
================================================================================

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                    SOFTWARE ENGINEERING BODY OF KNOWLEDGE                │
    └─────────────────────────────────────────────────────────────────────────┘
                                       │
           ┌───────────────────────────┼───────────────────────────┐
           │                           │                           │
           v                           v                           v
    ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
    │ REQUIREMENTS│            │   DESIGN    │            │ CONSTRUCTION│
    │ ENGINEERING │            │ ENGINEERING │            │ ENGINEERING │
    │             │            │             │            │             │
    │ - 도출      │            │ - 아키텍처  │            │ - 코딩      │
    │ - 분석      │            │ - 상세 설계 │            │ - 빌드      │
    │ - 명세      │            │ - 패턴      │            │ - 통합      │
    │ - 검증      │            │ - 평가      │            │ - 디버깅    │
    └─────────────┘            └─────────────┘            └─────────────┘
           │                           │                           │
           v                           v                           v
    ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
    │   TESTING   │            │MAINTENANCE  │            │CONFIGURATION│
    │ ENGINEERING │            │ ENGINEERING │            │ MANAGEMENT  │
    │             │            │             │            │             │
    │ - 단위      │            │ - 수정      │            │ - 식별      │
    │ - 통합      │            │ - 적응      │            │ - 통제      │
    │ - 시스템    │            │ - 완전화    │            │ - 감사      │
    │ - 인수      │            │ - 예방      │            │ - 기록      │
    └─────────────┘            └─────────────┘            └─────────────┘
           │                           │                           │
           v                           v                           v
    ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
    │ ENGINEERING │            │   QUALITY   │            │  PROJECT    │
    │ MANAGEMENT  │            │ ENGINEERING │            │ MANAGEMENT  │
    │             │            │             │            │             │
    │ - 계획      │            │ - SQA       │            │ - 범위      │
    │ - 수행      │            │ - V&V       │            │ - 일정      │
    │ - 모니터링  │            │ - 개선      │            │ - 비용      │
    │ - 종료      │            │ - 측정      │            │ - 위험      │
    └─────────────┘            └─────────────┘            └─────────────┘

    +-------------------------------------------------------------------+
    │ RELATED DISCIPLINES (관련 분야)                                    │
    │ - Computer Science (컴퓨터 과학)                                  │
    │ - Mathematics (수학)                                              │
    │ - Management Science (관리 과학)                                  │
    │ - Human-Computer Interaction (인간-컴퓨터 상호작용)               │
    │ - Systems Engineering (시스템 공학)                               │
    +-------------------------------------------------------------------+

================================================================================
```

### 2. 소프트웨어 공학의 7대 원칙

| 원칙 | 설명 | 실천 예시 |
| :--- | :--- | :--- |
| **1. 계층화 (Abstraction)** | 복잡성을 관리하기 위해 추상화 레벨 활용 | 아키텍처 → 설계 → 코드 |
| **2. 정보 은닉 (Information Hiding)** | 모듈 내부 구현 상세를 외부에 숨김 | 인터페이스 기반 설계, 캡슐화 |
| **3. 모듈화 (Modularity)** | 시스템을 독립적 모듈로 분할 | 마이크로서비스, 컴포넌트 |
| **4. 일관성 (Consistency)** | 전체 시스템에 걸쳐 일관된 설계 | 코딩 컨벤션, 아키텍처 스타일 |
| **5. 완전성 (Completeness)** | 모든 요구사항을 충족 | 요구사항 추적성 매트릭스 |
| **6. 검증 가능성 (Verifiability)** | 요구사항 및 설계의 테스트 가능성 | 인수 기준, DoD (Definition of Done) |
| **7. 추적성 (Traceability)** | 요구사항-설계-코드-테스트 간 연결 | RTM (Requirements Traceability Matrix) |

### 3. 소프트웨어 개발 패러다임의 진화

```text
[소프트웨어 개발 패러다임 진화]

Phase 1: 1960s-1970s - "Code & Fix"
┌─────────────────────────────────────────────────────────┐
│  [문제] → [코딩] → [실행] → [에러 수정] → [반복]        │
│                                                         │
│  문제: 체계적 프로세스 부재, 품질 불안정                 │
└─────────────────────────────────────────────────────────┘
                         ↓
Phase 2: 1970s-1990s - "Structured Methods"
┌─────────────────────────────────────────────────────────┐
│  [요구사항] → [분석] → [설계] → [구현] → [테스트]       │
│                                                         │
│  특징: 워터폴, V-모델, 구조적 분석/설계                  │
└─────────────────────────────────────────────────────────┘
                         ↓
Phase 3: 1990s-2010s - "Object-Oriented & Process"
┌─────────────────────────────────────────────────────────┐
│  [OOA] → [OOD] → [OOP] + [프로세스 관리]                │
│                                                         │
│  특징: UML, CMM/CMMI, RUP, 객체지향 방법론              │
└─────────────────────────────────────────────────────────┘
                         ↓
Phase 4: 2000s-Present - "Agile & DevOps"
┌─────────────────────────────────────────────────────────┐
│  [계획] ←→ [개발] ←→ [배포] ←→ [운영] (순환)           │
│                                                         │
│  특징: 스크럼, 칸반, CI/CD, MSA, 클라우드 네이티브       │
└─────────────────────────────────────────────────────────┘
                         ↓
Phase 5: 2020s-Future - "AI-Augmented Engineering"
┌─────────────────────────────────────────────────────────┐
│  [AI 어시스턴트] + [개발자] → [생성/검증/운영]          │
│                                                         │
│  특징: Copilot, LLM 기반 코드 생성, 자동화된 테스팅     │
└─────────────────────────────────────────────────────────┘
```

### 4. 핵심 메트릭: 소프트웨어 공학 성숙도 측정

```python
"""
소프트웨어 공학 성숙도 측정 프레임워크
조직의 소프트웨어 공학 실천 수준을 정량화
"""

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class EngineeringMetric:
    """소프트웨어 공학 메트릭 정의"""
    name: str
    description: str
    target_value: float
    unit: str
    weight: float

class SoftwareEngineeringMaturity:
    """소프트웨어 공학 성숙도 평가"""

    def __init__(self, organization: str):
        self.org = organization
        self.metrics = self._initialize_metrics()
        self.scores: Dict[str, float] = {}

    def _initialize_metrics(self) -> List[EngineeringMetric]:
        """핵심 메트릭 초기화"""
        return [
            EngineeringMetric(
                name="requirements_traceability",
                description="요구사항 추적성 확보율",
                target_value=90.0,
                unit="%",
                weight=0.15
            ),
            EngineeringMetric(
                name="code_review_coverage",
                description="코드 리뷰 적용률",
                target_value=100.0,
                unit="%",
                weight=0.12
            ),
            EngineeringMetric(
                name="test_automation_rate",
                description="테스트 자동화율",
                target_value=80.0,
                unit="%",
                weight=0.15
            ),
            EngineeringMetric(
                name="ci_cd_adoption",
                description="CI/CD 파이프라인 적용률",
                target_value=95.0,
                unit="%",
                weight=0.13
            ),
            EngineeringMetric(
                name="defect_density",
                description="결함 밀도 (목표 미만)",
                target_value=0.5,
                unit="defects/KLOC",
                weight=0.15
            ),
            EngineeringMetric(
                name="technical_debt_ratio",
                description="기술 부채 비율",
                target_value=5.0,
                unit="%",
                weight=0.10
            ),
            EngineeringMetric(
                name="documentation_completeness",
                description="문서화 완성도",
                target_value=85.0,
                unit="%",
                weight=0.10
            ),
            EngineeringMetric(
                name="security_scan_coverage",
                description="보안 스캔 적용률",
                target_value=100.0,
                unit="%",
                weight=0.10
            ),
        ]

    def assess(self, actual_values: Dict[str, float]) -> Dict:
        """성숙도 평가 수행"""
        total_score = 0.0
        details = []

        for metric in self.metrics:
            actual = actual_values.get(metric.name, 0)
            target = metric.target_value

            # 달성률 계산 (100% 초과 방지)
            if metric.name in ["defect_density", "technical_debt_ratio"]:
                # 낮을수록 좋은 메트릭
                achievement = min(100, (target / max(actual, 0.001)) * 100)
            else:
                # 높을수록 좋은 메트릭
                achievement = min(100, (actual / target) * 100)

            weighted_score = achievement * metric.weight
            total_score += weighted_score

            details.append({
                "metric": metric.name,
                "actual": actual,
                "target": target,
                "unit": metric.unit,
                "achievement": round(achievement, 1),
                "weighted_score": round(weighted_score, 2)
            })

        return {
            "organization": self.org,
            "total_score": round(total_score, 1),
            "max_score": 100.0,
            "maturity_level": self._get_maturity_level(total_score),
            "details": details
        }

    def _get_maturity_level(self, score: float) -> str:
        """점수 기반 성숙도 레벨 산정"""
        if score >= 90:
            return "Level 5: Optimizing (최적화형)"
        elif score >= 75:
            return "Level 4: Quantitatively Managed (정량적 관리형)"
        elif score >= 60:
            return "Level 3: Defined (정의형)"
        elif score >= 40:
            return "Level 2: Managed (관리형)"
        else:
            return "Level 1: Initial (초기형)"


# 사용 예시
if __name__ == "__main__":
    assessment = SoftwareEngineeringMaturity("TechCorp")

    sample_data = {
        "requirements_traceability": 85.0,
        "code_review_coverage": 95.0,
        "test_automation_rate": 70.0,
        "ci_cd_adoption": 90.0,
        "defect_density": 0.8,
        "technical_debt_ratio": 8.0,
        "documentation_completeness": 75.0,
        "security_scan_coverage": 100.0,
    }

    result = assessment.assess(sample_data)
    print(f"조직: {result['organization']}")
    print(f"총점: {result['total_score']}/100")
    print(f"성숙도: {result['maturity_level']}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 소프트웨어 공학 vs 타 공학 분야

| 비교 항목 | 소프트웨어 공학 | 기계 공학 | 건축 공학 |
| :--- | :--- | :--- | :--- |
| **대상 물질** | 무형 (코드, 데이터) | 유형 (금속, 플라스틱) | 유형 (콘크리트, 강철) |
| **변경 용이성** | 매우 높음 (복사-붙여넣기) | 낮음 (재가공 비용) | 매우 낮음 (철거 후 재시공) |
| **복제 비용** | 거의 0 | 높음 (재료비) | 매우 높음 |
| **일정 예측** | 어려움 (불확실성 높음) | 비교적 정확 | 비교적 정확 |
| **품질 측정** | 정성적, 간접적 | 물리적 특성 측정 | 구조적 안전성 검증 |
| **노후화** | 기술 부채, 호환성 문제 | 마모, 부식 | 노후화, 내진 문제 |

### 2. 과목 융합 관점 분석

#### 소프트웨어 공학 + 데이터베이스

```text
[융합 포인트]
1. 요구사항 분석 → 개념적 데이터 모델링 (ERD)
2. 설계 → 논리/물리 스키마 설계, 인덱스 전략
3. 테스팅 → 데이터 무결성 검증, 성능 테스트
4. 유지보수 → 스키마 마이그레이션, 데이터 이관

[심층 분석]
소프트웨어 공학에서 "정보 은닉" 원칙은
데이터베이스의 "뷰(View)", "저장 프로시저"와 연결됨
→ 내부 스키마 변경이 애플리케이션에 영향 최소화
```

#### 소프트웨어 공학 + 네트워크

```text
[융합 포인트]
1. 분산 시스템 아키텍처 설계
2. 네트워크 지연/대역폭을 고려한 성능 요구사항
3. 보안 설계 (전송 계층 암호화, 인증)
4. 장애 허용 설계 (타임아웃, 재시도, 서킷 브레이커)

[심층 분석]
마이크로서비스 아키텍처에서 네트워크 지연(Latency)은
핵심 품질 속성이 됨 → 서비스 분할 시 네트워크 경계 고려
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 및 기술사적 의사결정

**[시나리오 1] 대형 금융 SI 프로젝트의 방법론 선택**

*   **상황**: 100인 규모, 2년 프로젝트, 레거시 시스템과의 연동, 높은 보안 요구사항
*   **기술사적 판단**: **하이브리드 방법론 (Water-Scrum-Fall)** 채택
    *   **실행 전략**:
        1. 분석/설계 단계는 워터폴 (문서화 중시, 이해관계자 합의)
        2. 개발 단계는 스크럼 (2주 스프린트, 지속적 통합)
        3. 테스트/배포 단계는 통제적 (형상 관리, 인수 테스트)

**[시나리오 2] 스타트업의 애자일 도입**

*   **상황**: 5인 개발팀, 3개월 MVP, 요구사항 불확실성 높음
*   **기술사적 판단**: **XP(Extreme Programming) + 스크럼** 혼합
    *   **실행 전략**:
        1. 1주 스프린트로 빠른 피드백
        2. TDD, 짝 프로그래밍으로 품질 확보
        3. 지속적 배포로 매일 출시 가능 상태 유지

### 2. 도입 시 고려사항 (체크리스트)

**프로젝트 특성 분석**:
- [ ] 요구사항 안정성: 요구사항이 얼마나 자주 변화하는가?
- [ ] 규모 복잡도: 팀 크기, 코드 규모, 기술 스택 복잡도
- [ ] 품질 요구사항: 안전 중요(Safety-Critical) 시스템인가?
- [ ] 이해관계자: 고객의 참여 가능성, 승인 프로세스

**조직 준비도 평가**:
- [ ] 방법론 교육: 팀의 애자일/폴프식 방법론 이해도
- [ ] 도구 인프라: CI/CD, 협업 도구, 테스트 자동화
- [ ] 문화: 실패를 수용하는 문화, 자율성 보장

### 3. 주의사항 및 안티패턴

*   **"공학 없는 코딩" (Code Without Engineering)**:
    "동작만 하면 되지"라는 태도로 설계, 테스트, 문서화를 무시
    → 단기적 속도는 빠르나 장기적 기술 부채 급증

*   **"문서를 위한 문서" (Documentation for Documentation's Sake)**:
    가치 없는 문서를 양산하여 실제 개발 시간 침해
    → "동작하는 코드가 최고의 문서" 원칙과 균형 필요

*   **"도구 숭배" (Tool Worship)**:
    도구(JIRA, Jenkins 등)를 도입하는 것이 곧 공학적 실천이라 착각
    → 도구는 프로세스를 지원할 뿐, 프로세스 자체가 아님

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 지표 | 미적용 vs 적용 | 개선 효과 | 출처 |
| :--- | :--- | :--- | :--- | :--- |
| **프로젝트 성공률** | 일정/예산 준수 | 30% → 60% | 100% 향상 | Standish Group |
| **품질** | 결함 밀도 | 5.0 → 1.5 defects/KLOC | 70% 감소 | NASA |
| **생산성** | 기능점수/인월 | 15 → 25 FP/인월 | 67% 향상 | ISBSG |
| **유지보수** | 변경 소요 시간 | 10일 → 3일 | 70% 감소 | 내부 데이터 |

### 2. 미래 전망 및 진화 방향

1.  **AI-Augmented Software Engineering**: LLM 기반 코드 생성, 자동화된 테스트 작성, 지능형 코드 리뷰
2.  **Quantum Software Engineering**: 양자 알고리즘 기반 소프트웨어의 새로운 개발 패러다임
3.  **Green Software Engineering**: 탄소 배출 저감을 고려한 지속 가능한 소프트웨어 개발
4.  **Cyber-Physical Systems Engineering**: IoT, 자율주행 등 물리-사이버 융합 시스템의 공학

### ※ 참고 표준/가이드
*   **ISO/IEC/IEEE 12207**: 소프트웨어 생명주기 프로세스
*   **ISO/IEC/IEEE 15288**: 시스템 생명주기 프로세스
*   **SWEBOK Guide (IEEE)**: 소프트웨어 공학 지식 체계
*   **CMMI V2.0**: 역량 성숙도 모델 통합
*   **PMBOK Guide (PMI)**: 프로젝트 관리 지식 체계

---

## 📌 관련 개념 맵 (Knowledge Graph)
*   [소프트웨어 위기](@/studynotes/04_software_engineering/01_sdlc/_index.md) : 소프트웨어 공학의 탄생 배경
*   [소프트웨어 생명주기 (SDLC)](@/studynotes/04_software_engineering/01_sdlc/sdlc_waterfall_model.md) : 공학적 프로세스의 구체화
*   [애자일 방법론](@/studynotes/04_software_engineering/01_sdlc/agile_methodology.md) : 현대적 소프트웨어 공학의 핵심
*   [소프트웨어 품질](@/studynotes/04_software_engineering/02_quality/software_quality_standards.md) : 공학의 목표
*   [CMMI](@/studynotes/04_software_engineering/01_sdlc/cmmi.md) : 프로세스 성숙도 평가

---

## 👶 어린이를 위한 3줄 비유 설명
1. **문제**: 친구들이 모래성을 만드는데, 어떤 친구는 계획 없이 막 쌓다가 무너뜨리고, 어떤 친구는 설계도를 그리고 차근차근 만들어요. 누가 더 튼튼한 모래성을 만들까요?
2. **해결(소프트웨어 공학)**: 소프트웨어 공학은 "어떻게 하면 무너지지 않는 튼튼한 소프트웨어를 만들까?"를 연구하는 학문이에요. 설계도(설계), 건축법(방법론), 안전 검사(테스팅)를 체계적으로 적용해요.
3. **효과**: 소프트웨어 공학을 적용하면 우리가 매일 쓰는 스마트폰 앱이 갑자기 꺼지지 않고, 은행 앱이 돈을 잃어버리지 않고, 게임이 중간에 멈추지 않아요!
