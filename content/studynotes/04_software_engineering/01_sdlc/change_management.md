+++
title = "변경 관리 (Change Management)"
date = "2026-03-04"
description = "소프트웨어 변경 사항을 체계적으로 식별, 통제, 추적하는 프로세스"
weight = 42
+++

# 변경 관리 (Change Management)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 변경 관리는 소프트웨어 개발 과정에서 발생하는 **모든 변경 사항을 식별, 분석, 승인, 구현, 검증**하는 체계적인 프로세스로, 무분별한 변경으로 인한 **범위 크리프(Scope Creep)와 품질 저하**를 방지합니다.
> 2. **가치**: 체계적인 변경 관리는 **재작업 비용 30% 감소, 프로젝트 일정 준수율 25% 향상** 효과가 있으며, 특히 요구사항이 자주 변하는 애자일 환경에서도 **변경의 영향도를 투명하게 관리**할 수 있게 합니다.
> 3. **융합**: 변경 관리는 **형상 관리(SCM)**의 핵심 구성요소이며, 현대적으로는 **이슈 추적 시스템(Jira, GitHub Issues)**과 **CI/CD 파이프라인**으로 자동화됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

변경 관리(Change Management)는 소프트웨어 수명주기 동안 발생하는 모든 변경을 통제하는 프로세스입니다.

**변경 관리의 핵심 구성요소**:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                        변경 관리 핵심 구성요소                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  📝 변경 요청 (Change Request, CR)                                     │
│     - 변경의 내용, 이유, 영향도, 우선순위                               │
│                                                                         │
│  🔍 영향 분석 (Impact Analysis)                                         │
│     - 일정, 비용, 품질, 리스크에 미치는 영향                            │
│                                                                         │
│  ✅ 승인 기관 (Change Control Board, CCB)                              │
│     - 변경 승인/반려 결정                                               │
│                                                                         │
│  📊 변경 로그 (Change Log)                                              │
│     - 모든 변경의 이력 추적                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 💡 일상생활 비유: 인테리어 변경 요청

```
[ 인테리어 변경 관리 ]

고객: "주방을 싱크대에서 아일랜드 식탁으로 바꾸고 싶어요"

1. 변경 요청서 작성
   - 현재: 싱크대
   - 변경 후: 아일랜드 식탁
   - 이유: 공간 활용, 가족 모임

2. 영향 분석
   - 추가 비용: +500만원
   - 공사 기간: +3일
   - 구조 변경: 배관 이동 필요
   - 위험: 방수 문제

3. CCB 심의 (설계자, 시공자, 고객)
   - 승인 조건: 추가 비용 고객 부담

4. 변경 구현
   - 도면 수정 → 시공 → 검수

5. 변경 기록
   - "2024-03-04: 주방 식탁 변경 승인 및 완료"
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 변경 관리 프로세스

```text
================================================================================
|                    CHANGE MANAGEMENT PROCESS                                |
================================================================================

    [ 1. 변경 요청 접수 ]
    ┌────────────────────────────────────────────────────────────────────┐
    │                                                                    │
    │   변경 요청자 ──▶ CR 양식 작성 ──▶ 등록                            │
    │                                                                    │
    │   ┌──────────────────────────────────────────────────────────────┐ │
    │   │  변경 요청서 (Change Request Form)                          │ │
    │   │  ────────────────────────────────────────────────────────── │ │
    │   │  CR 번호: CR-2024-0123                                      │ │
    │   │  요청자: 홍길동                                             │ │
    │   │  요청일: 2024-03-04                                         │ │
    │   │  제목: 결제 수단에 간편결제 추가                            │ │
    │   │  유형: 기능 추가 / 변경 / 결함 수정                         │ │
    │   │  우선순위: 높음 / 중간 / 낮음                               │ │
    │   │  상세 설명: 카카오페이, 네이버페이 결제 추가 요청           │ │
    │   │  비즈니스 이유: 고객 편의성 증대, 이탈률 감소               │ │
    │   └──────────────────────────────────────────────────────────────┘ │
    └────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    [ 2. 변경 분석 및 평가 ]
    ┌────────────────────────────────────────────────────────────────────┐
    │                                                                    │
    │   영향 분석 (Impact Analysis)                                      │
    │   ┌──────────────────────────────────────────────────────────────┐ │
    │   │  분야          │  영향도                                    │ │
    │   │  ──────────────┼─────────────────────────────────────────── │ │
    │   │  일정          │  +2주 소요 (PG사 연동, 테스트)             │ │
    │   │  비용          │  +15인일 (개발) + 5인일 (테스트)           │ │
    │   │  기술          │  새로운 PG사 연동 모듈 개발 필요           │ │
    │   │  품질          │  기존 결제 기능 회귀 테스트 필요           │ │
    │   │  문서          │  설계서, 매뉴얼 업데이트 필요              │ │
    │   │  의존성        │  결제 서비스, 프론트엔드 영향             │ │
    │   └──────────────────────────────────────────────────────────────┘ │
    │                                                                    │
    │   위험 평가 (Risk Assessment)                                     │
    │   - 기술적 난이도: 중간                                           │
    │   - 실패 가능성: 낮음                                             │
    │   - 롤백 가능성: 높음                                             │
    └────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    [ 3. CCB 심의 및 결정 ]
    ┌────────────────────────────────────────────────────────────────────┐
    │                                                                    │
    │   CCB (Change Control Board) 구성                                 │
    │   - 프로젝트 관리자 (PM)                                          │
    │   - 기술 리드 (Tech Lead)                                         │
    │   - QA 리더                                                       │
    │   - 제품 책임자 (PO)                                              │
    │                                                                    │
    │   결정 옵션:                                                       │
    │   ✅ 승인 (Approved): 변경 진행                                   │
    │   ❌ 반려 (Rejected): 변경 불필요/위험                            │
    │   ⏸️ 보류 (Deferred): 추후 검토                                   │
    │   🔄 조건부 승인 (Conditionally Approved): 조건 충족 시 진행     │
    │                                                                    │
    └────────────────────────────────────────────────────────────────────┘
                                    │
                            승인된 경우 │
                                    ▼
    [ 4. 변경 구현 ]
    ┌────────────────────────────────────────────────────────────────────┐
    │                                                                    │
    │   구현 계획 수립 ──▶ 개발 ──▶ 테스트 ──▶ 검증                     │
    │                                                                    │
    │   ┌──────────────────────────────────────────────────────────────┐ │
    │   │  구현 체크리스트                                             │ │
    │   │  □ 설계서 업데이트                                          │ │
    │   │  □ 코드 구현                                                │ │
    │   │  □ 단위 테스트                                              │ │
    │   │  □ 통합 테스트                                              │ │
    │   │  □ 회귀 테스트                                              │ │
    │   │  □ 문서 업데이트                                            │ │
    │   │  □ 코드 리뷰                                                │ │
    │   └──────────────────────────────────────────────────────────────┘ │
    │                                                                    │
    └────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    [ 5. 변경 검증 및 종료 ]
    ┌────────────────────────────────────────────────────────────────────┐
    │                                                                    │
    │   검증 항목:                                                       │
    │   - 변경 요구사항 충족 여부                                       │
    │   - 기존 기능 영향 없음 (회귀 테스트 통과)                        │
    │   - 문서 업데이트 완료                                            │
    │                                                                    │
    │   종료: CR 상태를 "완료(Closed)"로 변경                            │
    │                                                                    │
    └────────────────────────────────────────────────────────────────────┘

================================================================================
```

### 2. 실무 예시: Jira를 활용한 변경 관리

```python
"""
변경 관리 시스템 예시
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class ChangeType(Enum):
    FEATURE = "기능 추가"
    MODIFICATION = "기능 변경"
    DEFECT = "결함 수정"
    ENHANCEMENT = "성능 개선"
    DOCUMENTATION = "문서 변경"

class Priority(Enum):
    HIGH = "높음"
    MEDIUM = "중간"
    LOW = "낮음"

class CRStatus(Enum):
    SUBMITTED = "접수"
    ANALYZING = "분석중"
    CCB_REVIEW = "CCB 심의"
    APPROVED = "승인"
    REJECTED = "반려"
    DEFERRED = "보류"
    IMPLEMENTING = "구현중"
    TESTING = "테스트중"
    COMPLETED = "완료"
    CLOSED = "종료"

@dataclass
class ImpactAnalysis:
    """영향 분석 결과"""
    schedule_impact: str  # 일정 영향
    cost_impact: str      # 비용 영향
    technical_impact: str # 기술 영향
    quality_impact: str   # 품질 영향
    affected_components: List[str]  # 영향받는 컴포넌트
    risk_level: str       # 위험 수준

@dataclass
class ChangeRequest:
    """변경 요청"""
    cr_id: str
    title: str
    description: str
    change_type: ChangeType
    priority: Priority
    requester: str
    request_date: datetime
    status: CRStatus = CRStatus.SUBMITTED
    impact_analysis: Optional[ImpactAnalysis] = None
    ccb_decision: Optional[str] = None
    implementation_notes: List[str] = field(default_factory=list)

class ChangeManagementSystem:
    """변경 관리 시스템"""

    def __init__(self):
        self.change_requests: dict[str, ChangeRequest] = {}
        self.cr_counter = 0

    def create_cr(self, title: str, description: str, change_type: ChangeType,
                  priority: Priority, requester: str) -> ChangeRequest:
        """변경 요청 생성"""
        self.cr_counter += 1
        cr_id = f"CR-{datetime.now().year}-{self.cr_counter:04d}"

        cr = ChangeRequest(
            cr_id=cr_id,
            title=title,
            description=description,
            change_type=change_type,
            priority=priority,
            requester=requester,
            request_date=datetime.now()
        )

        self.change_requests[cr_id] = cr
        return cr

    def analyze_impact(self, cr_id: str, analysis: ImpactAnalysis):
        """영향 분석 수행"""
        if cr_id in self.change_requests:
            cr = self.change_requests[cr_id]
            cr.impact_analysis = analysis
            cr.status = CRStatus.CCB_REVIEW

    def ccb_decide(self, cr_id: str, decision: str):
        """CCB 결정"""
        if cr_id in self.change_requests:
            cr = self.change_requests[cr_id]
            cr.ccb_decision = decision

            if decision == "승인":
                cr.status = CRStatus.APPROVED
            elif decision == "반려":
                cr.status = CRStatus.REJECTED
            elif decision == "보류":
                cr.status = CRStatus.DEFERRED

    def generate_report(self) -> str:
        """변경 관리 보고서 생성"""
        report = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    변경 관리 현황 보고서                                   ║
╠═══════════════════════════════════════════════════════════════════════════╣
║ 총 변경 요청: {len(self.change_requests)}개{' ':>50} ║
╠═══════════════════════════════════════════════════════════════════════════╣
"""

        status_counts = {}
        for cr in self.change_requests.values():
            status_counts[cr.status] = status_counts.get(cr.status, 0) + 1

        for status, count in status_counts.items():
            report += f"║ {status.value}: {count}개{' ':>55} ║\n"

        report += "╚═══════════════════════════════════════════════════════════════════════════╝"
        return report

# 사용 예시
if __name__ == "__main__":
    cms = ChangeManagementSystem()

    # 변경 요청 생성
    cr = cms.create_cr(
        title="간편결제 기능 추가",
        description="카카오페이, 네이버페이 간편결제 기능 추가",
        change_type=ChangeType.FEATURE,
        priority=Priority.HIGH,
        requester="김PO"
    )

    # 영향 분석
    impact = ImpactAnalysis(
        schedule_impact="+2주",
        cost_impact="+20인일",
        technical_impact="PG사 연동 모듈 신규 개발",
        quality_impact="회귀 테스트 필요",
        affected_components=["결제서비스", "프론트엔드"],
        risk_level="중간"
    )
    cms.analyze_impact(cr.cr_id, impact)

    # CCB 결정
    cms.ccb_decide(cr.cr_id, "승인")

    print(cms.generate_report())
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 1. 애자일 환경에서의 변경 관리

| 구분 | 전통적 (폭포수) | 애자일 |
|:---:|:---|:---|
| **변경 시점** | 초기에 고정 | 지속적 |
| **승인 기관** | 공식 CCB | PO + 팀 |
| **변경 단위** | 대규모 | 작은 단위 |
| **문서화** | 무거움 | 가벼움 (스토리) |
| **변경 비용** | 높음 | 낮음 |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 1. 변경 관리 안티패턴

```
❌ 안티패턴 1: "변경은 무료다"
- 모든 변경을 수용하다가 프로젝트 붕괴
- 해결: 변경 영향 분석 → 우선순위 → 승인 절차

❌ 안티패턴 2: "CCB가 모든 걸 막는다"
- 관료주의로 인해 유연성 상실
- 해결: 낮은 위험 변경은 간소화된 절차

❌ 안티패턴 3: "구두로 변경 요청"
- 추적 불가능한 변경 → "누가 언제 왜?"
- 해결: 모든 변경은 시스템에 등록
```

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 구분 | 효과 |
|:---:|:---|
| **정량적** | 재작업 비용 30% 감소 |
| **정량적** | 범위 크리프 50% 감소 |
| **정성적** | 변경 투명성 확보 |
| **정성적** | 감사 추적 가능 |

---

## 📌 관련 개념 맵

- [형상 관리(SCM)](@/studynotes/04_software_engineering/01_sdlc/configuration_management.md)
- [기준선(Baseline)](./)
- [범위 관리](./)
- [요구사항 관리](@/studynotes/04_software_engineering/04_requirements/requirements_engineering.md)

---

## 👶 어린이를 위한 3줄 비유 설명

1. **문제**: 팀 프로젝트인데 친구가 맘대로 주제를 바꾸고, 다른 친구는 분량을 늘리고, 또 다른 친구는 제출일을 바꿔요. 아무도 뭘 바꿨는지 모르겠어요!

2. **해결(변경 관리)**: "변경 요청서"를 쓰기로 했어요. "주제를 A에서 B로 바꾸고 싶어요. 이유는... 영향은..."라고 적어서 팀장한테 승인받아야 해요.

3. **효과**: 이제 누가 뭘 바꿨는지 다 알 수 있어요. 그리고 "이건 시간이 너무 많이 걸려서 안 돼"라고 명확히 말할 수도 있죠!
