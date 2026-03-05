+++
title = "KPI (핵심 성과 지표, Key Performance Indicator)"
description = "조직의 전략적 목표와 CSF 달성 여부를 정량적으로 측정하는 KPI의 개념, 설계 방법, SMART 원칙 및 IT 조직에서의 실무적 적용"
date = 2024-05-22
[taxonomies]
tags = ["IT Management", "Performance Management", "KPI", "Metrics", "CSF"]
+++

# KPI (핵심 성과 지표, Key Performance Indicator)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: KPI(Key Performance Indicator)는 조직의 전략적 목표와 핵심 성공 요인(CSF) 달성 여부를 측정하기 위해 정량적으로 정의된 핵심 지표로, "우리가 올바른 방향으로 가고 있는가?"를 객관적으로 답하는 측정 도구입니다.
> 2. **가치**: KPI는 추상적인 전략을 측정 가능한 목표로 전환하고, 성과의 가시성을 확보하며, 데이터 기반 의사결정과 지속적 개선(PDCA)을 가능하게 하는 성과 관리의 핵심 인프라입니다.
> 3. **융합**: KPI는 BSC(Balanced Scorecard)의 4관점, OKR의 Key Results, IT 거버넌스의 성과 측정 영역과 결합하여 전사적 성과 관리 체계(EPM)의 근간을 형성합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**KPI(Key Performance Indicator, 핵심 성과 지표)**란 조직이 전략적 목표를 달성하고 있는지를 측정하기 위해 사용하는 정량적 지표입니다. "무엇을 측정하는가?"가 곧 "무엇을 중요하게 여기는가?"를 반영하므로, KPI 선정은 전략적 의사결정의 핵심입니다.

**KPI vs 일반 지표(Metric)**:
| 구분 | KPI | 일반 지표(Metric) |
|:---|:---|:---|
| **성격** | 전략적, 핵심적 | 운영적, 보조적 |
| **수량** | 제한적 (조직당 10~20개) | 다수 가능 |
| **연계성** | CSF/전략과 직접 연계 | KPI 지원 |
| **예시** | 서비스 가용성 99.9% | 일일 로그 발생량 |

**SMART KPI 원칙**:
- **S**pecific (구체적): 명확하게 정의된 측정 대상
- **M**easurable (측정 가능): 수치로 표현 가능
- **A**chievable (달성 가능): 현실적 목표
- **R**elevant (관련성): 전략/CSF와 직접 연계
- **T**ime-bound (시간 제한): 명확한 달성 기한

### 💡 일상생활 비유: 자동차 계기판

자동차를 운전할 때 계기판을 봅니다. 여러 정보 중 **핵심 지표(KPI)**는 다음과 같습니다:
- **속도계**: 현재 속도 (안전 운전의 핵심)
- **연료 게이지**: 남은 기름 (주유 시점 결정)
- **엔진 온도**: 과열 여부 (긴급 정지 필요)

반면, **일반 지표(Metric)**는:
- 라디오 볼륨
- 에어컨 온도
- 조수석 안전벨트 착용 여부

IT 조직도 마찬가지입니다. 수천 개의 데이터 중 **핵심 KPI 10~20개**만 집중 관리해야 합니다. 모든 것을 측정하려다 보면 아무것도 관리하지 못합니다.

### 2. 등장 배경 및 발전 과정

#### 1) 기존 기술의 치명적 한계점

과거 성과 관리의 문제점:
- **주관적 평가**: "열심히 일했다" vs "성과가 없다"의 객관적 판단 불가
- **지표 과다**: 수백 개의 지표를 수집하다 보니 분석 불가
- **전략과 단절**: 측정은 많은데 전략 달성 여부는 알 수 없음
- **후행 지표 편중**: 재무 지표만 보고 미래를 예측 못 함

**문제점**:
- "측정하지 않으면 관리할 수 없다" (Peter Drucker)
- 하지만 "모든 것을 측정하면 아무것도 관리할 수 없다"

#### 2) 혁신적 패러다임 변화

1990년대 BSC(Balanced Scorecard)의 등장으로 KPI 체계가 정립되었습니다:
- **4관점 균형**: 재무, 고객, 프로세스, 학습/성장
- **선행/후행 지표**: 미래 예측 + 과거 성과 측정
- **전략 연계**: KPI가 전략 맵과 직접 연결

이후 OKR, EPM(Enterprise Performance Management) 등으로 발전했습니다.

#### 3) 비즈니스적 요구사항

오늘날 IT 조직은 다음 상황에서 KPI를 활용합니다:
- **IT 거버넌스**: IT 성과의 이사회 보고
- **SLA 관리**: 서비스 품질 계약 준수 여부
- **DevOps/SRE**: 시스템 안정성 및 배포 속도 측정
- **FinOps**: 클라우드 비용 최적화

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. KPI 분류 체계

| 분류 기준 | 유형 | 설명 | IT KPI 예시 |
|:---|:---|:---|:---|
| **시간적 성격** | 선행 지표 (Leading) | 미래 성과 예측 | 코드 커버리지, 배포 빈도 |
| | 후행 지표 (Lagging) | 과거 성과 측정 | 장애 건수, 고객 불만 |
| **BSC 관점** | 재무 | 비용, 수익 관련 | IT 투자 ROI, TCO |
| | 고객 | 고객 만족 관련 | NPS, 서비스 가용성 |
| | 프로세스 | 운영 효율 관련 | 배포 주기, MTTR |
| | 학습/성장 | 역량 관련 | 교육 이수율, 이직률 |
| **계층** | 전사 KPI | 최고 경영진 관심 | IT-비즈니스 정렬도 |
| | 부서 KPI | 부서장 관심 | 서버 가용성, 보안 사고 |
| | 개인 KPI | 개인 관심 | 코드 품질 점수 |
| **측정 대상** | 결과 KPI | 최종 성과 | 서비스 가용성 |
| | 프로세스 KPI | 과정 품질 | 변경 성공률 |

### 2. 정교한 KPI 설계 프레임워크

```text
========================================================================================
[ KPI Design & Management Architecture ]
========================================================================================

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         1단계: KPI 도출 (KPI Derivation)                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                               │   │
│  │     비전/미션                                                                 │   │
│  │         ↓                                                                     │   │
│  │     전략적 목표 (Strategic Goals)                                             │   │
│  │         ↓                                                                     │   │
│  │     핵심 성공 요인 (CSF)                                                      │   │
│  │         ↓                                                                     │   │
│  │     ┌─────────────────────────────────────────────────────────────────────┐ │   │
│  │     │                        KPI 도출 질문                                  │ │   │
│  │     │  • "이 CSF를 달성했는지 어떻게 알 수 있는가?"                          │ │   │
│  │     │  • "무엇을 측정해야 이 CSF의 성공을 증명할 수 있는가?"                  │ │   │
│  │     │  • "누가 이 KPI를 책임지는가?"                                        │ │   │
│  │     │  • "얼마나 자주 측정해야 하는가?"                                      │ │   │
│  │     └─────────────────────────────────────────────────────────────────────┘ │   │
│  │         ↓                                                                     │   │
│  │     KPI (Key Performance Indicators)                                         │   │
│  │                                                                               │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────┬────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                      2단계: KPI 정의서 작성 (KPI Definition)                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                               │   │
│  │     [KPI 정의서 템플릿]                                                        │   │
│  │     ┌───────────────────────────────────────────────────────────────────┐   │   │
│  │     │  항목                    내용                                       │   │   │
│  │     │  ──────────────────────────────────────────────────────────────   │   │   │
│  │     │  KPI명                서비스 가용성 (Service Availability)          │   │   │
│  │     │  정의                  서비스가 정상적으로 제공된 시간 비율            │   │   │
│  │     │  계산식                (총 가동 시간 - 장애 시간) / 총 가동 시간 × 100 │   │   │
│  │     │  측정 단위             백분율 (%)                                    │   │   │
│  │     │  목표값                99.9%                                         │   │   │
│  │     │  경고 임계값           99.5% 미만                                    │   │   │
│  │     │  위기 임계값           99.0% 미만                                    │   │   │
│  │     │  측정 주기             월간                                          │   │   │
│  │     │  데이터 출처           모니터링 시스템 (Prometheus)                   │   │   │
│  │     │  담당자                인프라팀장                                     │   │   │
│  │     │  연계 CSF              서비스 품질 혁신                               │   │   │
│  │     │  BSC 관점              고객 관점                                     │   │   │
│  │     │  지표 성격             후행 지표                                      │   │   │
│  │     └───────────────────────────────────────────────────────────────────┘   │   │
│  │                                                                               │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────┬────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        3단계: KPI 대시보드 구축 (Dashboard)                           │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                               │   │
│  │     ┌───────────────────────────────────────────────────────────────────┐   │   │
│  │     │                    IT KPI Executive Dashboard                       │   │   │
│  │     ├───────────────────────────────────────────────────────────────────┤   │   │
│  │     │  [고객 관점]           [프로세스 관점]        [재무 관점]           │   │   │
│  │     │  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐       │   │   │
│  │     │  │ 서비스 가용성 │     │  배포 빈도    │     │  IT ROI      │       │   │   │
│  │     │  │   99.95%    │     │  주 3.2회    │     │   185%      │       │   │   │
│  │     │  │   [GREEN]   │     │   [GREEN]    │     │   [GREEN]   │       │   │   │
│  │     │  │  목표:99.9% │     │  목표:주2회  │     │  목표:150%  │       │   │   │
│  │     │  └──────────────┘     └──────────────┘     └──────────────┘       │   │   │
│  │     │                                                                       │   │   │
│  │     │  [학습/성장 관점]                                                      │   │   │
│  │     │  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐       │   │   │
│  │     │  │  교육 이수율  │     │ 핵심인재유지율 │     │ 코드 커버리지 │       │   │   │
│  │     │  │    92%      │     │    96%       │     │    78%      │       │   │   │
│  │     │  │   [GREEN]   │     │   [GREEN]    │     │  [YELLOW]   │       │   │   │
│  │     │  │  목표:90%   │     │  목표:95%    │     │  목표:80%   │       │   │   │
│  │     │  └──────────────┘     └──────────────┘     └──────────────┘       │   │   │
│  │     │                                                                       │   │   │
│  │     │  [RAG 상태 요약]  ●GREEN: 8개  ●YELLOW: 3개  ●RED: 1개             │   │   │
│  │     └───────────────────────────────────────────────────────────────────┘   │   │
│  │                                                                               │   │
│  │     [RAG (Red-Amber-Green) 상태 정의]                                        │   │
│  │     ● GREEN: 목표 달성 또는 초과                                              │   │
│  │     ● YELLOW: 목표 대비 80~99% 달성 (주의 필요)                                │   │
│  │     ● RED: 목표 대비 80% 미만 달성 (즉각 조치 필요)                            │   │
│  │                                                                               │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────┬────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        4단계: KPI 관리 사이클 (Management Cycle)                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                               │   │
│  │     ┌────────────────────────────────────────────────────────────────┐      │   │
│  │     │                                                                 │      │   │
│  │     │          ┌──────────┐                                          │      │   │
│  │     │          │   Plan   │                                          │      │   │
│  │     │          │  계획    │                                          │      │   │
│  │     │          └────┬─────┘                                          │      │   │
│  │     │               │                                                │      │   │
│  │     │               ▼                                                │      │   │
│  │     │    ┌──────────┐      ┌──────────┐                             │      │   │
│  │     │    │   Act    │──────│   Do     │                             │      │   │
│  │     │    │  개선    │      │  실행    │                             │      │   │
│  │     │    └──────────┘      └────┬─────┘                             │      │   │
│  │     │                           │                                    │      │   │
│  │     │                           ▼                                    │      │   │
│  │     │                    ┌──────────┐                                │      │   │
│  │     │                    │  Check   │                                │      │   │
│  │     │                    │  측정    │                                │      │   │
│  │     │                    └──────────┘                                │      │   │
│  │     │                                                                 │      │   │
│  │     └────────────────────────────────────────────────────────────────┘      │   │
│  │                                                                               │   │
│  │     [KPI 리뷰 주기]                                                           │   │
│  │     • 일간: 실시간 모니터링 (시스템 가용성, 에러율)                             │   │
│  │     • 주간: 스프린트 리뷰 (배포 빈도, 버그 발견율)                              │   │
│  │     • 월간: 운영 리뷰 (MTTR, SLA 달성률)                                      │   │
│  │     • 분기: 경영진 리뷰 (IT ROI, 고객 만족도)                                  │   │
│  │     • 연간: KPI 재설정 (전략 변화, 환경 변화 반영)                              │   │
│  │                                                                               │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘

========================================================================================
```

### 3. IT 조직 핵심 KPI 라이브러리

```python
"""
IT 조직 KPI 관리 시스템
- BSC 4관점별 KPI 정의
- KPI 대시보드 생성
- RAG 상태 평가
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal
from enum import Enum

class BSCPerspective(Enum):
    FINANCIAL = "재무"
    CUSTOMER = "고객"
    PROCESS = "내부 프로세스"
    LEARNING = "학습 및 성장"

class KPICategory(Enum):
    LEADING = "선행 지표"
    LAGGING = "후행 지표"

@dataclass
class KPI:
    """핵심 성과 지표"""
    name: str
    definition: str
    formula: str
    unit: str
    target: float
    warning_threshold: float
    critical_threshold: float
    measurement_frequency: str
    data_source: str
    owner: str
    bsc_perspective: BSCPerspective
    category: KPICategory
    csf_link: str
    current_value: Optional[float] = None

    def evaluate_status(self) -> Literal["GREEN", "YELLOW", "RED"]:
        """RAG 상태 평가"""
        if self.current_value is None:
            return "RED"

        achievement_rate = self.current_value / self.target

        if achievement_rate >= 1.0:
            return "GREEN"
        elif achievement_rate >= 0.8:
            return "YELLOW"
        else:
            return "RED"

    def get_achievement_rate(self) -> Optional[float]:
        """달성률 계산"""
        if self.current_value is None:
            return None
        return round((self.current_value / self.target) * 100, 1)

class KPIManager:
    """KPI 관리 시스템"""

    def __init__(self, organization: str):
        self.organization = organization
        self.kpis: List[KPI] = []

    def add_kpi(self, kpi: KPI) -> None:
        self.kpis.append(kpi)

    def get_kpis_by_perspective(self, perspective: BSCPerspective) -> List[KPI]:
        """BSC 관점별 KPI 조회"""
        return [kpi for kpi in self.kpis if kpi.bsc_perspective == perspective]

    def generate_dashboard(self) -> Dict:
        """KPI 대시보드 생성"""
        dashboard = {
            "organization": self.organization,
            "total_kpis": len(self.kpis),
            "perspectives": {},
            "rag_summary": {"GREEN": 0, "YELLOW": 0, "RED": 0},
            "alerts": []
        }

        for perspective in BSCPerspective:
            kpis = self.get_kpis_by_perspective(perspective)
            dashboard["perspectives"][perspective.value] = []

            for kpi in kpis:
                status = kpi.evaluate_status()
                dashboard["rag_summary"][status] += 1

                kpi_data = {
                    "name": kpi.name,
                    "current": kpi.current_value,
                    "target": kpi.target,
                    "unit": kpi.unit,
                    "achievement_rate": kpi.get_achievement_rate(),
                    "status": status,
                    "trend": "UP" if kpi.current_value and kpi.current_value >= kpi.target * 0.9 else "DOWN"
                }
                dashboard["perspectives"][perspective.value].append(kpi_data)

                # 알림 생성
                if status == "RED":
                    dashboard["alerts"].append({
                        "kpi": kpi.name,
                        "severity": "CRITICAL",
                        "message": f"{kpi.name}이 목표 대비 {100 - kpi.get_achievement_rate()}% 미달"
                    })
                elif status == "YELLOW":
                    dashboard["alerts"].append({
                        "kpi": kpi.name,
                        "severity": "WARNING",
                        "message": f"{kpi.name}이 목표에 근접하지 않음"
                    })

        return dashboard

    def get_it_kpi_library(self) -> Dict[str, List[KPI]]:
        """IT 조직 표준 KPI 라이브러리"""
        library = {
            "고객 관점": [
                KPI(
                    name="서비스 가용성",
                    definition="서비스가 정상 제공된 시간 비율",
                    formula="(총 가동 시간 - 장애 시간) / 총 가동 시간 × 100",
                    unit="%",
                    target=99.9,
                    warning_threshold=99.5,
                    critical_threshold=99.0,
                    measurement_frequency="월간",
                    data_source="모니터링 시스템",
                    owner="인프라팀",
                    bsc_perspective=BSCPerspective.CUSTOMER,
                    category=KPICategory.LAGGING,
                    csf_link="서비스 품질 혁신"
                ),
                KPI(
                    name="평균 장애 복구 시간 (MTTR)",
                    definition="장애 발생부터 복구까지 평균 소요 시간",
                    formula="총 장애 복구 시간 / 장애 건수",
                    unit="시간",
                    target=1.0,
                    warning_threshold=2.0,
                    critical_threshold=4.0,
                    measurement_frequency="월간",
                    data_source="ITSM 시스템",
                    owner="운영팀",
                    bsc_perspective=BSCPerspective.CUSTOMER,
                    category=KPICategory.LAGGING,
                    csf_link="서비스 품질 혁신"
                ),
                KPI(
                    name="고객 만족도 (NPS)",
                    definition="순추천지수",
                    formula="추천율 - 비추천율",
                    unit="점",
                    target=50.0,
                    warning_threshold=30.0,
                    critical_threshold=10.0,
                    measurement_frequency="분기",
                    data_source="설문조사",
                    owner="서비스팀",
                    bsc_perspective=BSCPerspective.CUSTOMER,
                    category=KPICategory.LAGGING,
                    csf_link="고객 경험 혁신"
                ),
            ],
            "프로세스 관점": [
                KPI(
                    name="배포 빈도",
                    definition="단위 기간(주) 내 배포 횟수",
                    formula="주간 배포 횟수",
                    unit="회/주",
                    target=5.0,
                    warning_threshold=2.0,
                    critical_threshold=1.0,
                    measurement_frequency="주간",
                    data_source="CI/CD 파이프라인",
                    owner="DevOps팀",
                    bsc_perspective=BSCPerspective.PROCESS,
                    category=KPICategory.LEADING,
                    csf_link="민첩한 서비스 제공"
                ),
                KPI(
                    name="변경 실패율",
                    definition="전체 변경 중 실패한 변경 비율",
                    formula="실패한 변경 건수 / 전체 변경 건수 × 100",
                    unit="%",
                    target=5.0,
                    warning_threshold=10.0,
                    critical_threshold=20.0,
                    measurement_frequency="월간",
                    data_source="ITSM 시스템",
                    owner="DevOps팀",
                    bsc_perspective=BSCPerspective.PROCESS,
                    category=KPICategory.LAGGING,
                    csf_link="변경 품질 관리"
                ),
            ],
            "재무 관점": [
                KPI(
                    name="IT 투자 ROI",
                    definition="IT 투자 대비 수익률",
                    formula="(IT 투자 수익 - IT 투자 비용) / IT 투자 비용 × 100",
                    unit="%",
                    target=150.0,
                    warning_threshold=100.0,
                    critical_threshold=50.0,
                    measurement_frequency="연간",
                    data_source="재무 시스템",
                    owner="CIO",
                    bsc_perspective=BSCPerspective.FINANCIAL,
                    category=KPICategory.LAGGING,
                    csf_link="IT 가치 실현"
                ),
                KPI(
                    name="클라우드 비용 최적화율",
                    definition="클라우드 비용 절감 달성률",
                    formula="실제 절감액 / 목표 절감액 × 100",
                    unit="%",
                    target=100.0,
                    warning_threshold=80.0,
                    critical_threshold=60.0,
                    measurement_frequency="월간",
                    data_source="클라우드 비용 대시보드",
                    owner="FinOps팀",
                    bsc_perspective=BSCPerspective.FINANCIAL,
                    category=KPICategory.LAGGING,
                    csf_link="비용 효율성"
                ),
            ],
            "학습/성장 관점": [
                KPI(
                    name="교육 이수율",
                    definition="필수 교육 이수 인원 비율",
                    formula="교육 이수 인원 / 전체 인원 × 100",
                    unit="%",
                    target=95.0,
                    warning_threshold=80.0,
                    critical_threshold=60.0,
                    measurement_frequency="분기",
                    data_source="HR 시스템",
                    owner="HR팀",
                    bsc_perspective=BSCPerspective.LEARNING,
                    category=KPICategory.LEADING,
                    csf_link="인재 역량 강화"
                ),
                KPI(
                    name="핵심 인재 유지율",
                    definition="핵심 인재의 조직 내 잔류율",
                    formula="(기존 핵심 인재 - 이직자) / 기존 핵심 인재 × 100",
                    unit="%",
                    target=95.0,
                    warning_threshold=85.0,
                    critical_threshold=75.0,
                    measurement_frequency="연간",
                    data_source="HR 시스템",
                    owner="HR팀",
                    bsc_perspective=BSCPerspective.LEARNING,
                    category=KPICategory.LAGGING,
                    csf_link="인재 유지"
                ),
            ]
        }
        return library


# 실무 적용 예시
if __name__ == "__main__":
    manager = KPIManager("ABC IT 조직")

    # 표준 KPI 라이브러리에서 가져오기
    library = manager.get_it_kpi_library()

    for perspective, kpis in library.items():
        for kpi in kpis:
            manager.add_kpi(kpi)

    # 현재값 업데이트
    for kpi in manager.kpis:
        if kpi.name == "서비스 가용성":
            kpi.current_value = 99.95
        elif kpi.name == "평균 장애 복구 시간 (MTTR)":
            kpi.current_value = 0.8
        elif kpi.name == "배포 빈도":
            kpi.current_value = 4.2
        elif kpi.name == "IT 투자 ROI":
            kpi.current_value = 185.0
        elif kpi.name == "교육 이수율":
            kpi.current_value = 92.0

    # 대시보드 생성
    dashboard = manager.generate_dashboard()

    print(f"=== {dashboard['organization']} KPI 대시보드 ===\n")
    print(f"총 KPI 수: {dashboard['total_kpis']}개")
    print(f"RAG 상태: GREEN {dashboard['rag_summary']['GREEN']}개, "
          f"YELLOW {dashboard['rag_summary']['YELLOW']}개, "
          f"RED {dashboard['rag_summary']['RED']}개")
    print()

    for perspective, kpis in dashboard["perspectives"].items():
        print(f"[{perspective} 관점]")
        for kpi in kpis:
            print(f"  {kpi['name']}: {kpi['current']} / 목표 {kpi['target']} "
                  f"({kpi['achievement_rate']}%) [{kpi['status']}]")
        print()
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. KPI vs Metric vs OKR

| 비교 항목 | KPI | Metric | OKR Key Result |
|:---|:---|:---|:---|
| **성격** | 전략적 핵심 지표 | 운영적 측정값 | 야심찬 목표의 결과 |
| **수량** | 제한적 (10~20개) | 무제한 | Objective당 2~5개 |
| **목표 성격** | 달성 목표 | 측정값 | 도전적 목표 (70% 달성도 성공) |
| **수정 빈도** | 연간/반기 | 실시간 | 분기 |

### 2. DORA Metrics (DevOps 핵심 KPI)

| DORA Metric | 정의 | Elite 수준 |
|:---|:---|:---|
| **Deployment Frequency** | 배포 빈도 | 일일 다회 |
| **Lead Time for Changes** | 변경 리드타임 | 1일 미만 |
| **MTTR** | 평균 복구 시간 | 1시간 미만 |
| **Change Failure Rate** | 변경 실패율 | 0-15% |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

**시나리오: KPI가 많아 "지표 피로(Indicator Fatigue)" 발생**
- **문제 상황**: IT 조직이 50개 이상의 KPI를 운영. 매월 보고서만 수십 페이지. 경영진은 어떤 KPI가 중요한지 파악 못 함.
- **기술사적 의사결정**:
  1. **KPI 계층화**: 전사 KPI 10개, 부서 KPI 20개로 정리
  2. **핵심 KPI 선정**: CSF와 직접 연결된 KPI만 유지
  3. **대시보드 간소화**: 1페이지 Executive Dashboard 구축
  4. **자동화**: KPI 수집 및 보고 자동화로 운영 부하 감소

### 2. 도입 시 고려사항 (체크리스트)

- [ ] KPI와 CSF의 명확한 연결
- [ ] SMART 원칙 준수
- [ ] 선행/후행 지표의 균형
- [ ] BSC 4관점의 균형
- [ ] KPI 정의서 작성
- [ ] 데이터 수집 자동화

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | KPI 도입 전 | KPI 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **전략 가시성** | 30% | 90% | +60%p |
| **의사결정 속도** | 주간 | 일간 | 7배 향상 |
| **성과 달성률** | 50% | 80% | +30%p |

### 2. 미래 전망

1. **실시간 KPI**: 스트리밍 데이터 기반 실시간 KPI
2. **AI 기반 KPI 예측**: 머신러닝으로 KPI 트렌드 예측
3. **자율 KPI 조정**: 환경 변화에 따른 KPI 자동 조정

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [CSF (핵심 성공 요인)](@/studynotes/12_it_management/01_strategy/csf.md): KPI가 측정하는 대상
- [BSC (균형 성과 기록표)](@/studynotes/12_it_management/01_strategy/bsc.md): KPI의 4관점 분류
- [OKR](@/studynotes/12_it_management/01_strategy/okr.md): KPI와 유사한 목표 관리
- [SLA](@/studynotes/12_it_management/01_itsm/sla.md): KPI 기반 서비스 계약

---

## 👶 어린이를 위한 3줄 비유 설명
1. **성적표 같아요**: 학교에서 시험 점수가 내 성적을 보여주듯, 회사도 KPI로 성과를 측정해요!
2. **목표가 있어요**: "수학 90점 맞기!"처럼 회사도 "서비스 99.9% 가용성 달성!" 같은 목표가 있어요.
3. **빨강/노랑/초록**: 목표를 달성하면 초록, 거의 다 가면 노랑, 많이 부족하면 빨강이에요. 신호등처럼요!
