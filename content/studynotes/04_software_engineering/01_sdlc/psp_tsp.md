+++
title = "PSP/TSP (Personal/Team Software Process)"
date = "2026-03-04"
description = "개인과 팀의 소프트웨어 프로세스 역량 향상을 위한 규율적 개발 방법론"
weight = 28
+++

# PSP/TSP (Personal/Team Software Process)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: PSP(Personal Software Process)는 개인 개발자의 작업 습관을 데이터 기반으로 개선하고, TSP(Team Software Process)는 이를 팀 단위로 확장하여 **예측 가능하고 고품질의 소프트웨어**를 개발하는 규율적 방법론입니다.
> 2. **가치**: PSP를 적용한 개발자는 평균 **결함률 75% 감소, 생산성 20% 향상**을 경험하며, TSP 팀은 **일정 준수율 90% 이상, 결함 밀도 0.06/KLOC** 달성이 보고되었습니다.
> 3. **융합**: CMMI의 창시자 Watts Humphrey가 개발했으며, **CMMI Level 5 달성의 실천적 기반**을 제공하고, 개인/팀 차원의 정량적 관리를 가능하게 합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

PSP(Personal Software Process)와 TSP(Team Software Process)는 **Watts Humphrey**가 개발한 소프트웨어 공학 방법론입니다.

**PSP vs TSP 비교**:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                        PSP vs TSP 비교                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  👤 PSP (Personal Software Process)                                    │
│     대상: 개인 개발자                                                   │
│     목표: 개인 작업 습관 개선, 결함 감소, 추정 정확도 향상              │
│     핵심: 시간 기록, 결함 기록, 크기 측정                               │
│                                                                         │
│  👥 TSP (Team Software Process)                                        │
│     대상: 소프트웨어 개발 팀                                            │
│     목표: 팀 성능 최적화, 예측 가능한 프로젝트 수행                     │
│     핵심: 팀 런칭, 주간 미팅, 역할 분담                                 │
│                                                                         │
│  [ 관계 ]                                                              │
│  PSP ──▶ 개인 역량 강화 ──▶ TSP ──▶ 팀 성과 향상                       │
│        (선수 조건)           (확장)                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 💡 일상생활 비유: 운동선수의 훈련 일지와 팀 전략

```
[ PSP - 개인 선수의 훈련 일지 ]

축구 선수가 매일 기록:
- 오늘 달린 거리: 5km
- 슈팅 연습: 100회 (성공 78회)
- 피로도: 7/10
- 몸무게: 72kg

기록을 분석하다 보니:
"월요일에 무리하면 수요일에 부상 위험"
→ 월요일 훈련 강도 조절

[ TSP - 팀 전략 회의 ]

감독 + 선수들이 함께:
- 이번 시즌 목표: 우승
- 각 선수 역할: 공격수, 수비수, 미드필더
- 주간 전략 점검
- 문제 해결 회의

PSP는 "개인의 훈련 데이터"이고,
TSP는 "팀의 승리 전략"이다.
```

### 2. 등장 배경 및 발전 과정

#### 1) Watts Humphrey의 통찰

```
[ 1990년대의 문제 ]

CMM/CMMI의 성공:
- 조직 차원의 프로세스 성숙도 향상
- 많은 조직이 CMM Level 2, 3 달성

하지만:
┌────────────────────────────────────────────────────────────┐
│  ❓ "조직은 성숙했는데, 왜 프로젝트는 여전히 실패하나?"    │
│                                                            │
│  💡 Humphrey의 깨달음:                                     │
│     "조직의 프로세스가 아무리 좋아도,                      │
│      개인이 그것을 실행하지 않으면 소용없다"               │
│                                                            │
│  → 개인 차원의 규율(Discipline)이 필요!                    │
└────────────────────────────────────────────────────────────┘
```

#### 2) PSP/TSP의 탄생과 발전

```
[ 역사적 발전 ]

1995 ─── PSP 0, PSP 0.1 발표
    │   - 기본 시간/결함 기록
    │
1997 ─── PSP 1, PSP 1.1 (크기 추정)
    │   - PROBE(Proxy Based Estimating) 도입
    │
1999 ─── PSP 2, PSP 2.1 (품질 관리)
    │   - 코드 리뷰, 설계 리뷰
    │
1999 ─── PSP 3 (Cyclic Process)
    │   - 대규모 개발 확장
    │
2000 ─── TSP 발표
    │   - PSP를 팀으로 확장
    │   - 팀 런칭, 롤(Role) 정의
    │
현재 ─── PSP/TSP 교육 프로그램 운영
        - SEI 공식 교육
        - 전 세계 확산
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. PSP 진화 단계

| 단계 | 명칭 | 추가되는 능력 | 핵심 스크립트 |
|:---:|:---|:---|:---|
| **PSP0** | 기본 프로세스 | 시간/결함 기록 | PSP0 스크립트 |
| **PSP0.1** | 크기 측정 | 코딩 표준, 크기 측정 | PSP0.1 스크립트 |
| **PSP1** | 개인 추정 | 크기 추정, PROBE | PSP1 스크립트 |
| **PSP1.1** | 작업 계획 | 태스크 계획, 스케줄 | PSP1.1 스크립트 |
| **PSP2** | 품질 관리 | 코드 리뷰, 설계 리뷰 | PSP2 스크립트 |
| **PSP2.1** | 설계 템플릿 | 설계 검증, 템플릿 | PSP2.1 스크립트 |
| **PSP3** | 순환적 개발 | 단계적 확장 | PSP3 스크립트 |

### 2. 정교한 구조 다이어그램: PSP 프로세스 흐름

```text
================================================================================
|                    PERSONAL SOFTWARE PROCESS (PSP)                          |
================================================================================

    [ 계획 (Planning) ]
    ┌────────────────────────────────────────────────────────────────────┐
    │                                                                    │
    │   요구사항 ──▶ 크기 추정(PROBE) ──▶ 자원 추정 ──▶ 일정 계획       │
    │                                                                    │
    │   입력: 요구사항 명세서                                            │
    │   출력: 프로젝트 계획서, 일정표                                    │
    │                                                                    │
    │   ┌──────────────────────────────────────────────────────────────┐ │
    │   │                    PROBE (Proxy Based Estimating)            │ │
    │   │                                                              │ │
    │   │   과거 데이터:                                               │ │
    │   │   ┌────────────────────────────────────────────────────┐    │ │
    │   │   │ 객체 타입 │ 평균 LOC │ 최소 LOC │ 최대 LOC │ 개수 │    │ │
    │   │   ├──────────┼──────────┼──────────┼──────────┼──────┤    │ │
    │   │   │ 계산     │  12.5    │   5.0    │  25.0    │  10  │    │ │
    │   │   │ 데이터   │   8.3    │   3.0    │  15.0    │  15  │    │ │
    │   │   │ I/O      │  18.2    │   8.0    │  35.0    │   8  │    │ │
    │   │   └──────────┴──────────┴──────────┴──────────┴──────┘    │ │
    │   │                                                              │ │
    │   │   → 추정 LOC = Σ(객체수 × 평균LOC) ± 예측구간              │ │
    │   └──────────────────────────────────────────────────────────────┘ │
    │                                                                    │
    └────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    [ 개발 (Development) ]
    ┌────────────────────────────────────────────────────────────────────┐
    │                                                                    │
    │   설계 ──▶ 설계 리뷰 ──▶ 코딩 ──▶ 코드 리뷰 ──▶ 컴파일 ──▶ 테스트 │
    │                                                                    │
    │   ┌──────────────────────────────────────────────────────────────┐ │
    │   │                    시간/결함 기록                             │ │
    │   │                                                              │ │
    │   │   ┌────────────────────────────────────────────────────┐    │ │
    │   │   │ 단계     │ 시작 │ 종료 │ 중단 │ 투입 │ 결함 │ 비고 │    │ │
    │   │   ├──────────┼──────┼──────┼──────┼──────┼──────┼──────┤    │ │
    │   │   │ 설계     │ 9:00 │10:30 │  0   │  90  │  2   │      │    │ │
    │   │   │ 코딩     │10:30 │13:00 │  30  │ 120  │  5   │      │    │ │
    │   │   │ 테스트   │13:00 │14:30 │  0   │  90  │  3   │      │    │ │
    │   │   └──────────┴──────┴──────┴──────┴──────┴──────┴──────┘    │ │
    │   │                                                              │ │
    │   │   결함 기록 로그:                                            │ │
    │   │   ┌────────────────────────────────────────────────────┐    │ │
    │   │   │ ID │ 발견일 │ 단계 │ 유형 │ 주입단계 │ 수정시간 │    │ │
    │   │   ├────┼────────┼──────┼──────┼──────────┼──────────┤    │ │
    │   │   │ 1  │ 3/4    │ 코딩 │ 구문 │ 코딩     │   2분    │    │ │
    │   │   │ 2  │ 3/4    │ 테스트│ 로직 │ 설계     │  15분    │    │ │
    │   │   └────────────────────────────────────────────────────┘    │ │
    │   └──────────────────────────────────────────────────────────────┘ │
    │                                                                    │
    │   핵심 지표:                                                       │
    │   - 단계별 결함 제거 효율 (Phase Yield)                           │
    │   - 검증 비율 (Verification Ratio)                                │
    │   - A/FR (Appraisal to Failure Ratio)                             │
    │                                                                    │
    └────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    [ 사후 분석 (Postmortem) ]
    ┌────────────────────────────────────────────────────────────────────┐
    │                                                                    │
    │   계획 vs 실적 비교 ──▶ 프로세스 개선점 도출                       │
    │                                                                    │
    │   ┌──────────────────────────────────────────────────────────────┐ │
    │   │                    핵심 질문                                 │ │
    │   │                                                              │ │
    │   │   Q1: 추정이 정확했는가? (추정 오차율)                       │ │
    │   │   Q2: 어느 단계에서 결함이 많이 주입되었는가?                │ │
    │   │   Q3: 코드 리뷰가 효과적이었는가?                            │ │
    │   │   Q4: 다음에 무엇을 개선할 것인가?                           │ │
    │   │                                                              │ │
    │   └──────────────────────────────────────────────────────────────┘ │
    │                                                                    │
    └────────────────────────────────────────────────────────────────────┘

================================================================================
|  KEY INSIGHT: "측정하지 않으면 개선할 수 없다" - PSP의 핵심 철학          |
================================================================================
```

### 3. TSP(Team Software Process) 구조

```text
================================================================================
|                    TEAM SOFTWARE PROCESS (TSP)                              |
================================================================================

[ TSP 팀 롤(Role) 구조 ]

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                        ┌─────────────────┐                             │
│                        │   팀 리더       │                             │
│                        │  (Team Leader)  │                             │
│                        └────────┬────────┘                             │
│                                 │                                       │
│    ┌────────────────────────────┼────────────────────────────┐         │
│    │                            │                            │         │
│    ▼                            ▼                            ▼         │
│ ┌──────────────┐     ┌──────────────────┐     ┌──────────────┐        │
│ │ 개발 관리자  │     │   계획 관리자    │     │ 품질 관리자  │        │
│ │(Development  │     │(Planning Manager)│     │(Quality      │        │
│ │ Manager)     │     │                  │     │ Manager)     │        │
│ └──────────────┘     └──────────────────┘     └──────────────┘        │
│                                                                         │
│ ┌──────────────┐     ┌──────────────────┐     ┌──────────────┐        │
│ │ 지원 관리자  │     │   프로세스 관리자│     │ 소프트웨어   │        │
│ │(Support      │     │(Process Manager) │     │ 엔지니어     │        │
│ │ Manager)     │     │                  │     │(SW Engineer) │        │
│ └──────────────┘     └──────────────────┘     └──────────────┘        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

[ 각 롤의 책임 ]

팀 리더: 팀 운영, 고객 인터페이스
개발 관리자: 기술 방향, 아키텍처
계획 관리자: 일정, 태스크 추적
품질 관리자: 품질 목표, 결함 추적
지원 관리자: 도구, 형상 관리
프로세스 관리자: 프로세스 준수, 개선

[ TSP 런칭(Launch) - 9단계 미팅 ]

Day 1: 제품 목표 및 팀 구성
Day 2: 제품 전략 및 컨셉
Day 3: 워크 브레이크다운 구조(WBS)
Day 4: 태스크 시간 추정
Day 5: 일정 계획 수립
Day 6: 위험 평가
Day 7: 품질 계획
Day 8: 품질 계획 완성
Day 9: 팀 계획 발표 및 승인

[ TSP 주간 미팅(Weekly Meeting) ]

┌────────────────────────────────────────────────────────────────────────┐
│ 1. 품질 관리자: 품질 상태 보고                                         │
│ 2. 계획 관리자: 일정 상태 보고                                         │
│ 3. 각 팀원: 개인 태스크 상태                                           │
│ 4. 위험 검토: 새로운 위험 식별                                         │
│ 5. 조치 항목: Action Items 할당                                        │
│ 6. 팀 리더: 종합 및 다음 주 목표                                       │
└────────────────────────────────────────────────────────────────────────┘
```

### 4. 실무 예시: PSP 시간/결함 기록

```python
"""
PSP 시간 및 결함 기록 시스템
"""

from dataclasses import dataclass, field
from datetime import datetime, time
from typing import List, Dict, Optional
from enum import Enum

class Phase(Enum):
    """개발 단계"""
    PLANNING = "계획"
    DESIGN = "설계"
    DESIGN_REVIEW = "설계 리뷰"
    CODING = "코딩"
    CODE_REVIEW = "코드 리뷰"
    COMPILE = "컴파일"
    TEST = "테스트"
    POSTMORTEM = "사후분석"

class DefectType(Enum):
    """결함 유형 (PSP 표준)"""
    DOC = "문서"
    SYNTAX = "구문"
    BUILD = "빌드"
    ASSIGNMENT = "할당"
    INTERFACE = "인터페이스"
    CHECKING = "검사"
    DATA = "데이터"
    FUNCTION = "기능"
    SYSTEM = "시스템"
    ENVIRONMENT = "환경"

@dataclass
class TimeLog:
    """시간 기록"""
    date: str
    phase: Phase
    start_time: str
    end_time: str
    interruption: int  # 중단 시간 (분)
    delta_time: float  # 실제 투입 시간 (분)

@dataclass
class DefectLog:
    """결함 기록"""
    defect_id: int
    date: str
    phase_injected: Phase  # 주입 단계
    phase_removed: Phase   # 제거 단계
    defect_type: DefectType
    fix_time: float  # 수정 시간 (분)
    description: str

@dataclass
class PSPProject:
    """PSP 프로젝트"""
    project_id: str
    program_size_loc: int  # 코드 라인 수
    time_logs: List[TimeLog] = field(default_factory=list)
    defect_logs: List[DefectLog] = field(default_factory=list)

    def add_time_log(self, log: TimeLog):
        self.time_logs.append(log)

    def add_defect_log(self, log: DefectLog):
        self.defect_logs.append(log)

    def get_total_time(self) -> float:
        """총 투입 시간"""
        return sum(log.delta_time for log in self.time_logs)

    def get_phase_time(self, phase: Phase) -> float:
        """단계별 시간"""
        return sum(log.delta_time for log in self.time_logs if log.phase == phase)

    def get_total_defects(self) -> int:
        """총 결함 수"""
        return len(self.defect_logs)

    def get_defects_by_phase(self, phase: Phase, by: str = "removed") -> int:
        """단계별 결함 수"""
        if by == "removed":
            return sum(1 for d in self.defect_logs if d.phase_removed == phase)
        else:  # injected
            return sum(1 for d in self.defect_logs if d.phase_injected == phase)

    def calculate_phase_yield(self, phase: Phase) -> float:
        """
        단계별 수율(Yield) 계산
        = 해당 단계에서 제거한 결함 수 / (이전 단계까지 누적된 결함 + 해당 단계 주입)
        """
        defects_removed_here = self.get_defects_by_phase(phase, "removed")
        # 간소화된 계산 (실제로는 더 복잡)
        if defects_removed_here == 0:
            return 0.0
        # 누적 결함 대비 제거율
        total_before = sum(self.get_defects_by_phase(p, "removed")
                          for p in Phase if p.value < phase.value)
        return (defects_removed_here / (total_before + defects_removed_here)) * 100

    def calculate_afr(self) -> float:
        """
        A/FR (Appraisal to Failure Ratio)
        = 리뷰 시간 / (컴파일 + 테스트 시간)
        높을수록 좋음 (1.0 이상 권장)
        """
        review_time = self.get_phase_time(Phase.DESIGN_REVIEW) + \
                      self.get_phase_time(Phase.CODE_REVIEW)
        failure_time = self.get_phase_time(Phase.COMPILE) + \
                       self.get_phase_time(Phase.TEST)

        if failure_time == 0:
            return float('inf')
        return review_time / failure_time

    def calculate_productivity(self) -> float:
        """생산성 (LOC/시간)"""
        total_hours = self.get_total_time() / 60
        if total_hours == 0:
            return 0.0
        return self.program_size_loc / total_hours

    def generate_report(self) -> str:
        """PSP 프로젝트 보고서"""
        report = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    PSP 프로젝트 보고서                                     ║
╠═══════════════════════════════════════════════════════════════════════════╣
║ 프로젝트 ID: {self.project_id:<55} ║
║ 프로그램 크기: {self.program_size_loc} LOC{' ':>46} ║
╠═══════════════════════════════════════════════════════════════════════════╣
║ 단계별 시간 분석                                                          ║
╠═══════════════════════════════════════════════════════════════════════════╣
"""
        for phase in Phase:
            phase_time = self.get_phase_time(phase)
            percentage = (phase_time / self.get_total_time() * 100) if self.get_total_time() > 0 else 0
            bar = "█" * int(percentage / 2)
            report += f"║ {phase.value:<10} │ {phase_time:>6.0f}분 ({percentage:>5.1f}%) {bar:<20} ║\n"

        report += f"""╠═══════════════════════════════════════════════════════════════════════════╣
║ 총 투입 시간: {self.get_total_time():>6.0f}분 ({self.get_total_time()/60:>5.1f}시간){' ':>25} ║
╠═══════════════════════════════════════════════════════════════════════════╣
║ 결함 분석                                                                  ║
╠═══════════════════════════════════════════════════════════════════════════╣
║ 총 결함 수: {self.get_total_defects():>5}개{' ':>47} ║
║ 결함 밀도: {self.get_total_defects()/self.program_size_loc*1000 if self.program_size_loc > 0 else 0:>5.2f} 개/KLOC{' ':>41} ║
║ A/FR 비율: {self.calculate_afr():>5.2f} {'(좋음 ✅)' if self.calculate_afr() >= 1.0 else '(개선필요 ⚠️)'}{' ':>30} ║
╠═══════════════════════════════════════════════════════════════════════════╣
║ 생산성                                                                     ║
╠═══════════════════════════════════════════════════════════════════════════╣
║ LOC/시간: {self.calculate_productivity():>6.1f}{' ':>47} ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""
        return report

# 사용 예시
if __name__ == "__main__":
    project = PSPProject(
        project_id="PSP-Exercise-1",
        program_size_loc=150
    )

    # 시간 기록 예시
    time_logs = [
        TimeLog("2024-03-04", Phase.PLANNING, "09:00", "09:30", 0, 30),
        TimeLog("2024-03-04", Phase.DESIGN, "09:30", "11:00", 10, 80),
        TimeLog("2024-03-04", Phase.DESIGN_REVIEW, "11:00", "11:30", 0, 30),
        TimeLog("2024-03-04", Phase.CODING, "13:00", "16:00", 30, 150),
        TimeLog("2024-03-04", Phase.CODE_REVIEW, "16:00", "17:00", 0, 60),
        TimeLog("2024-03-04", Phase.COMPILE, "17:00", "17:15", 0, 15),
        TimeLog("2024-03-04", Phase.TEST, "17:15", "18:00", 0, 45),
        TimeLog("2024-03-04", Phase.POSTMORTEM, "18:00", "18:30", 0, 30),
    ]

    for log in time_logs:
        project.add_time_log(log)

    # 결함 기록 예시
    defect_logs = [
        DefectLog(1, "2024-03-04", Phase.CODING, Phase.CODE_REVIEW,
                  DefectType.SYNTAX, 2, "세미콜론 누락"),
        DefectLog(2, "2024-03-04", Phase.DESIGN, Phase.CODE_REVIEW,
                  DefectType.FUNCTION, 10, "루프 종료 조건 오류"),
        DefectLog(3, "2024-03-04", Phase.CODING, Phase.COMPILE,
                  DefectType.SYNTAX, 1, "변수명 오타"),
        DefectLog(4, "2024-03-04", Phase.CODING, Phase.TEST,
                  DefectType.DATA, 15, "배열 인덱스 오류"),
        DefectLog(5, "2024-03-04", Phase.DESIGN, Phase.TEST,
                  DefectType.FUNCTION, 20, "경계값 처리 누락"),
    ]

    for log in defect_logs:
        project.add_defect_log(log)

    print(project.generate_report())
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: PSP/TSP vs CMMI

| 비교 항목 | PSP/TSP | CMMI |
|:---:|:---|:---|
| **초점** | 개인/팀 수준 | 조직 수준 |
| **전제 조건** | 없음 (누구나 시작 가능) | PSP 지식 권장 |
| **측정 방식** | 시간, 결함, 크기 | 프로세스 영역 준수 |
| **적용 단위** | 개인/팀 | 조직 전체 |
| **교육 요구** | 1~2주 집중 교육 | 장기적 적용 |
| **ROI 증빙** | 개인 데이터 기반 | 조직 데이터 기반 |

### 2. PSP/TSP와 CMMI의 관계

```
[ CMMI 달성을 위한 PSP/TSP ]

CMMI Level 2 (관리)
├─ 요구사항 관리 → PSP 요구사항 분석
├─ 프로젝트 계획 → PSP 계획 스크립트
├─ 측정 및 분석 → PSP 데이터 수집
└─ 형상 관리 → TSP 지원 관리자

CMMI Level 3 (정의)
├─ 조직 프로세스 정의 → PSP 스크립트
├─ 통합 프로젝트 관리 → TSP 팀 구조
└─ 검증/확인 → PSP 리뷰 프로세스

CMMI Level 4 (정량적 관리)
├─ 조직 프로세스 성능 → PSP 과거 데이터
└─ 정량적 프로젝트 관리 → PSP/TSP 메트릭

CMMI Level 5 (최적화)
├─ 조직 성능 관리 → PSP 개인 개선
└─ 원인 분석 및 해결 → PSP 사후분석

→ PSP/TSP는 CMMI 고레벨 달성의 "실천적 기반"
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오

**[시나리오] CMMI Level 5 달성을 위한 PSP/TSP 도입**

```
상황:
- 조직이 CMMI Level 3 달성
- Level 4, 5 목표
- 개인 차원의 정량적 관리 부재

기술사적 판단:

1️⃣ PSP 파일럿 도입 (6개월)
   - 핵심 개발자 10명 선정
   - PSP 교육 이수
   - 10개 프로그램 PSP로 개발

2️⃣ 성과 측정
   - 결함률: 40개/KLOC → 10개/KLOC (75% 감소)
   - 추정 오차: ±50% → ±20%
   - 생산성: 20% 향상

3️⃣ 전사 확산
   - 모든 개발자 PSP 교육
   - TSP 팀 구성

4️⃣ CMMI Level 4, 5 달성
   - PSP/TSP 데이터가 정량적 관리 기반
   - 개인별 프로세스 성능 베이스라인 구축
```

### 2. 도입 시 고려사항

```text
[ PSP/TSP 도입 체크리스트 ]

✅ 개인 준비도
□ 데이터 기록에 동의하는가? (시간, 결함)
□ 과거 데이터를 활용할 의향이 있는가?
□ 정기적인 사후분석을 수행할 수 있는가?

✅ 조직 지원
□ PSP/TSP 교육 예산이 있는가?
□ 데이터 기록을 위한 도구가 있는가?
□ 관리자가 시간 기록을 "업무"로 인정하는가?

✅ 기대치 관리
□ 단기적 생산성 저하 가능성을 이해하는가?
□ (PSP 학습 곡선: 6개월~1년)
□ 개인 데이터의 비밀 보장이 되는가?
```

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 효과 (SEI 보고서 기반) |
|:---:|:---|
| **정량적** | 결함률 75% 감소 |
| **정량적** | 테스트 시간 50% 감소 |
| **정량적** | 추정 정확도 2배 향상 |
| **정성적** | 개인 성취감 향상 |
| **정성적** | 예측 가능한 업무 |

### 2. 미래 전망

```
PSP/TSP의 현대적 재해석:

1. 디지털 PSP
   - 자동 시간 추적 도구
   - IDE 연동 결함 기록

2. TSP + Agile
   - 스크럼과 TSP 롤 융합
   - 스프린트별 품질 메트릭

3. AI 기반 개인 코칭
   - 개인 데이터 분석
   - 개선점 자동 제안
```

### ※ 참고 표준/가이드

- **Watts Humphrey**: "PSP: A Self-Improvement Process for Software Engineers"
- **Watts Humphrey**: "TSP: Leading a Development Team"
- **SEI (Software Engineering Institute)**: PSP/TSP 공식 교육

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [CMMI](@/studynotes/04_software_engineering/01_sdlc/cmmi.md) : PSP/TSP의 상위 프레임워크
- [코드 리뷰](@/studynotes/04_software_engineering/02_quality/software_testing.md) : PSP의 핵심 품질 활동
- [프로젝트 관리](@/studynotes/04_software_engineering/03_project/project_management_evm.md) : TSP의 계획 관리
- [결함 관리](./) : PSP의 핵심 메트릭

---

## 👶 어린이를 위한 3줄 비유 설명

1. **문제**: 매일 공부하는데 성적이 안 올라요. 뭘 얼마나 공부했는지도 모르겠고, 틀린 문제는 왜 틀렸는지도 몰라요.

2. **해결(PSP)**: 공부 일지를 쓰기 시작했어요. "오늘 수학 1시간, 틀린 문제 3개(계산 실수 2개, 개념 오해 1개)"라고 적었죠.

3. **효과**: 일지를 보니까 "계산 실수가 많다"는 걸 알게 됐어요. 이제 계산 연습을 더 하니까 성적이 올랐어요. 똑같은 실수를 안 하니까 좋아요!
