+++
title = "BSC (Balanced Scorecard, 균형 성과 기록표)"
date = "2026-03-04"
[extra]
categories = "studynotes-enterprise"
+++

# BSC (Balanced Scorecard, 균형 성과 기록표)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 로버트 캐플란(Robert Kaplan)과 데이비드 노턴(David Norton)이 개발한 경영 성과 관리 도구로, **재무, 고객, 내부 프로세스, 학습과 성장의 4가지 관점에서 조직의 성과를 균형 있게 평가**합니다.
> 2. **가치**: 단기 재무 성과에만 치우친 경영의 편중을 해소하고, 비재무적 지표를 통해 미래 성장 동력과 전략 실행을 체계적으로 관리할 수 있게 합니다.
> 3. **융합**: KPI(Key Performance Indicator), 전략 체계도(Strategy Map), OKR과 결합되며, IT 관점에서는 IT BSC, 디지털 BSC로 확장 적용됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. BSC의 개념 및 철학적 근간
균형 성과 기록표(BSC, Balanced Scorecard)는 1992년 하버드 비즈니스 리뷰에 발표된 이래 전 세계 기업과 공공기관에서 가장 널리 활용되는 전략 실행 및 성과 관리 프레임워크입니다. BSC의 핵심 철학은 **"측정할 수 없는 것은 관리할 수 없다(What gets measured gets managed)"**는 것과, **"균형(Balance)"**의 중요성입니다. 기존의 재무 중심 성과 평가는 과거를 보여줄 뿐 미래를 예측하지 못합니다. BSC는 **재무적 지표와 비재무적 지표, 단기적 목표와 장기적 목표, 선행 지표와 후행 지표 사이의 균형**을 통해 조직의 지속가능한 성공을 보장합니다.

#### 2. 💡 비유를 통한 이해: 종합 건강 검진 vs 체중계
체중계(재무 지표)만 보고 건강을 판단하는 것은 위험합니다. 체중은 정상인데 혈압이 높을 수도, 근력이 약할 수도 있습니다. **BSC는 '종합 건강 검진'입니다.** 체중(재무)뿐만 아니라 혈압(고객 만족도), 심폐 지구력(내부 프로세스 효율), 근력(직원 역량)을 모두 측정합니다. 하나가 나빠도 다른 것을 챙기며, 전체적인 건강(조직 성과)을 유지합니다.

#### 3. 등장 배경 및 발전 과정
- **1987년**: Analog Devices사에서 최초로 'Scorecard' 개념 도입
- **1992년**: Kaplan & Norton, HBR에 "The Balanced Scorecard" 논문 게재
- **1996년**: "The Balanced Scorecard: Translating Strategy into Action" 저서 출간
- **2000년**: "The Strategy-Focused Organization" - 전략 실행 도구로 발전
- **2004년**: "Strategy Maps" - 4대 관점 간 인과관계 시각화
- **2008년**: "The Execution Premium" - 전략 실행 시스템으로 확장
- **현재**: 디지털 대시보드, AI 기반 성과 예측, OKR과의 융합

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. BSC의 4대 관점 (Four Perspectives)

| 관점 | 영문 | 핵심 질문 | 대상 | 예시 KPI |
| :--- | :--- | :--- | :--- | :--- |
| **재무** | Financial | "주주에게 어떻게 보여질 것인가?" | 주주, 투자자 | ROE, EPS, 매출 성장률, EBITDA |
| **고객** | Customer | "고객에게 어떻게 보여질 것인가?" | 고객 | 고객 만족도, NPS, 시장 점유율, 신규 고객 수 |
| **내부 프로세스** | Internal Process | "어떤 프로세스에 탁월해야 하는가?" | 운영 프로세스 | 주문 처리 시간, 품질 불량률, 혁신 비율 |
| **학습과 성장** | Learning & Growth | "지속적 개선과 가치 창출을 어떻게 할 것인가?" | 조직, 인력, 시스템 | 직원 만족도, 교육 시간, 시스템 가용성 |

#### 2. BSC 전략 체계도 (Strategy Map) 다이어그램

```text
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           [ BSC 전략 체계도 (Strategy Map) ]                        │
│                                                                                     │
│  ┌───────────────────────────────────────────────────────────────────────────────┐ │
│  │                         [ 재무 관점 (Financial) ]                              │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                          │ │
│  │  │ 매출 성장   │  │ 수익성 향상 │  │ 자산 효율화 │                          │ │
│  │  │  20% 증대   │  │ ROE 15%    │  │ 자산회전율  │                          │ │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                          │ │
│  └─────────┼────────────────┼────────────────┼──────────────────────────────────┘ │
│            │                │                │                                      │
│            ▼                ▼                ▼   "어떤 재무 성과를 낼 것인가?"     │
│  ┌───────────────────────────────────────────────────────────────────────────────┐ │
│  │                         [ 고객 관점 (Customer) ]                               │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                          │ │
│  │  │고객 만족도  │  │ 시장 점유율 │  │ 브랜드 이미지│                          │ │
│  │  │   90점     │  │   25%      │  │   상위 3위  │                          │ │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                          │ │
│  └─────────┼────────────────┼────────────────┼──────────────────────────────────┘ │
│            │                │                │                                      │
│            ▼                ▼                ▼   "고객에게 무엇을 제공할 것인가?"   │
│  ┌───────────────────────────────────────────────────────────────────────────────┐ │
│  │                    [ 내부 프로세스 관점 (Internal Process) ]                   │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │ │
│  │  │혁신 프로세스│  │ 운영 프로세스│  │서비스 프로세스│  │규제/사회책임 │         │ │
│  │  │신제품 출시  │  │리드타임 단축│  │A/S 만족도   │  │환경/윤리    │         │ │
│  │  │  6개월 내   │  │  3일 → 1일 │  │   95점     │  │  준수       │         │ │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │ │
│  └─────────┼────────────────┼────────────────┼────────────────┼──────────────────┘ │
│            │                │                │                │                    │
│            ▼                ▼                ▼                ▼                    │
│                                          "어떤 프로세스에 탁월해야 하는가?"        │
│  ┌───────────────────────────────────────────────────────────────────────────────┐ │
│  │                    [ 학습과 성장 관점 (Learning & Growth) ]                    │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                          │ │
│  │  │ 인적 자본   │  │ 정보 자본   │  │ 조직 자본   │                          │ │
│  │  │직원 역량    │  │시스템/기술  │  │문화/리더십  │                          │ │
│  │  │  교육 40h  │  │ERP/CRM 구축│  │성과 보상    │                          │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                          │ │
│  └───────────────────────────────────────────────────────────────────────────────┘ │
│                                          "어떤 역량과 문화가 필요한가?"            │
│                                                                                     │
│  ═══════════════════════════════════════════════════════════════════════════════   │
│  ※ 인과관계: 학습/성장 → 내부 프로세스 → 고객 → 재무 (하향식 달성)                │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

#### 3. 선행 지표 vs 후행 지표

| 구분 | 정의 | 특징 | 예시 |
| :--- | :--- | :--- | :--- |
| **후행 지표 (Lagging)** | 결과를 측정하는 지표 | 과거 지향, 측정 용이 | 매출, 수익, 시장 점유율 |
| **선행 지표 (Leading)** | 미래 결과를 예측하는 지표 | 미래 지향, 측정 어려움 | 직원 만족도, 파이프라인, R&D 투자 |

**BSC의 균형**: 재무는 후행, 학습/성장은 선행, 이들이 균형을 이루어야 함

#### 4. IT BSC (IT 관점 BSC) 및 Python 구현

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class BSCPerspective(Enum):
    FINANCIAL = "재무"
    CUSTOMER = "고객"
    INTERNAL_PROCESS = "내부 프로세스"
    LEARNING_GROWTH = "학습과 성장"

@dataclass
class KPI:
    """KPI 정의"""
    name: str
    perspective: BSCPerspective
    target: float
    actual: float
    unit: str
    weight: float  # 가중치 (0~1)
    is_leading: bool  # 선행 지표 여부

    @property
    def achievement_rate(self) -> float:
        """달성률 계산"""
        if self.target == 0:
            return 0
        return (self.actual / self.target) * 100

    @property
    def weighted_score(self) -> float:
        """가중 점수 계산"""
        return min(self.achievement_rate, 150) * self.weight  # 최대 150%

class BSCScorecard:
    """BSC 성과 기록표"""

    def __init__(self, organization: str, period: str):
        self.organization = organization
        self.period = period
        self.kpis: List[KPI] = []

    def add_kpi(self, kpi: KPI):
        """KPI 추가"""
        self.kpis.append(kpi)

    def calculate_perspective_score(self, perspective: BSCPerspective) -> Dict:
        """관점별 점수 계산"""
        perspective_kpis = [kpi for kpi in self.kpis if kpi.perspective == perspective]

        if not perspective_kpis:
            return {"score": 0, "kpis": []}

        total_weight = sum(kpi.weight for kpi in perspective_kpis)
        weighted_sum = sum(kpi.weighted_score for kpi in perspective_kpis)
        normalized_score = weighted_sum / total_weight if total_weight > 0 else 0

        return {
            "score": normalized_score,
            "kpis": [{"name": kpi.name, "actual": kpi.actual, "target": kpi.target,
                      "achievement": kpi.achievement_rate}
                     for kpi in perspective_kpis]
        }

    def generate_report(self) -> str:
        """BSC 성과 보고서 생성"""
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    BSC 성과 기록표 - {self.organization}                       ║
║                         기간: {self.period}                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
"""

        total_score = 0
        for perspective in BSCPerspective:
            result = self.calculate_perspective_score(perspective)
            score = result["score"]
            total_score += score

            status = "●" if score >= 100 else "○" if score >= 80 else "▽"
            report += f"║ 【{perspective.value}】 {status} {score:.1f}점\n"

            for kpi_data in result["kpis"]:
                ach = kpi_data["achievement"]
                ach_status = "✓" if ach >= 100 else "△" if ach >= 80 else "✗"
                report += f"║   {ach_status} {kpi_data['name']}: {kpi_data['actual']} / {kpi_data['target']} ({ach:.1f}%)\n"

            report += "║\n"

        avg_score = total_score / 4
        overall_status = "우수" if avg_score >= 100 else "양호" if avg_score >= 80 else "미달"

        report += f"""╠══════════════════════════════════════════════════════════════════════════════╣
║ 【종합 평가】 {avg_score:.1f}점 ({overall_status})                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        return report

# 실행 예시: IT 부서 BSC
if __name__ == "__main__":
    # IT BSC 생성
    it_bsc = BSCScorecard(organization="IT 부서", period="2024 Q1")

    # 재무 관점 KPI
    it_bsc.add_kpi(KPI("IT 예산 절감률", BSCPerspective.FINANCIAL, 10, 12, "%", 0.5, False))
    it_bsc.add_kpi(KPI("IT 투자 ROI", BSCPerspective.FINANCIAL, 150, 165, "%", 0.5, False))

    # 고객 관점 KPI
    it_bsc.add_kpi(KPI("내부 고객 만족도", BSCPerspective.CUSTOMER, 85, 88, "점", 0.4, True))
    it_bsc.add_kpi(KPI("SLA 준수율", BSCPerspective.CUSTOMER, 99, 98.5, "%", 0.3, False))
    it_bsc.add_kpi(KPI("서비스 요청 처리 시간", BSCPerspective.CUSTOMER, 4, 3.5, "시간", 0.3, False))

    # 내부 프로세스 관점 KPI
    it_bsc.add_kpi(KPI("시스템 가용성", BSCPerspective.INTERNAL_PROCESS, 99.9, 99.95, "%", 0.4, False))
    it_bsc.add_kpi(KPI("장애 복구 시간(MTTR)", BSCPerspective.INTERNAL_PROCESS, 2, 1.5, "시간", 0.3, False))
    it_bsc.add_kpi(KPI("프로젝트 납기 준수율", BSCPerspective.INTERNAL_PROCESS, 90, 95, "%", 0.3, False))

    # 학습과 성장 관점 KPI
    it_bsc.add_kpi(KPI("직원 교육 시간", BSCPerspective.LEARNING_GROWTH, 40, 45, "시간", 0.3, True))
    it_bsc.add_kpi(KPI("기술 자격증 취득률", BSCPerspective.LEARNING_GROWTH, 50, 60, "%", 0.3, True))
    it_bsc.add_kpi(KPI("직원 만족도", BSCPerspective.LEARNING_GROWTH, 80, 82, "점", 0.4, True))

    # 보고서 출력
    print(it_bsc.generate_report())
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 성과 관리 프레임워크 비교

| 특성 | BSC | KPI | OKR | MBO |
| :--- | :--- | :--- | :--- | :--- |
| **개발자** | Kaplan & Norton | - | Intel/Google | Peter Drucker |
| **구조** | 4대 관점 | 단일 지표 | 목표 + 핵심 결과 | 목표 + 기한 |
| **시간 범위** | 장기 (1~3년) | 월/분기 | 분기 | 연간 |
| **측정 방식** | 균형 점수 | 정량 지표 | 달성/미달 | 달성률 |
| **적합 조직** | 대기업, 공공기관 | 모든 조직 | 스타트업, IT | 전통적 조직 |
| **강점** | 균형, 전략 연계 | 단순, 측정 용이 | 민첩, 도전적 | 명확한 책임 |

#### 2. 과목 융합 관점 분석
- **IT 거버넌스 (IT BSC)**: IT 부서의 성과를 4대 관점(비즈니스 기여, 사용자 만족, 운영 효율, 혁신 역량)으로 평가합니다.
- **ITSM (SLA 관점)**: 고객 관점 KPI로 SLA 준수율, 서비스 요청 처리 시간 등을 활용합니다.
- **전략 경영 (Strategy Map)**: BSC의 4대 관점 간 인과관계를 시각화하여 전략 실행 로직을 명확히 합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단: BSC 도입 시나리오
**[상황]** K기업은 단기 실적 위주 경영으로 장기 성장 동력이 약화되고 있습니다. BSC 도입을 검토합니다.

**[전략적 접근]**
1. **Top-down vs Bottom-up**: CEO 주도 Top-down으로 전사 BSC 수립 후, 부서별로 Cascade-down
2. **KPI 선정 원칙**:
   - 각 관점당 4~6개 KPI (전체 15~25개)
   - SMART 원칙 (Specific, Measurable, Achievable, Relevant, Time-bound)
   - 선행/후행 지표의 균형
3. **연계 보상**: BSC 성과를 인센티브, 승진에 연계하여 동기 부여

#### 2. 도입 시 고려사항 (Checklist)
- **전략 명확화**: BSC 이전에 명확한 전략(Vision, Mission, Strategy)이 선행되어야 합니다.
- **데이터 가용성**: KPI 측정에 필요한 데이터가 수집 가능한지 확인
- **주기적 리뷰**: 분기별 BSC 리뷰 미팅, 연간 전략 수정

#### 3. 안티패턴 (Anti-patterns)
- **"지표만 늘리기"**: 의미 없는 지표를 너무 많이 설정하여 관리 부담 증가
- **"재무 관점 편중"**: 결국 재무 지표만 중요하게 취급
- **"전략 연계 없음"**: BSC가 전략과 무관한 단순 측정 도구로 전락

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 개선 항목 | BSC 도입 시 기대효과 |
| :--- | :--- | :--- |
| **전략 실행** | 전략 달성률 | 30~50% 향상 |
| **의사소통** | 전략 이해도 | 60% → 90% 향상 |
| **성과 투명성** | 성과 가시성 | 전 조직 실시간 파악 |
| **균형 성장** | 비재무 지표 개선 | 고객 만족, 직원 만족 동시 향상 |

#### 2. 미래 전망: 디지털 BSC & AI 기반 성과 관리
- **Real-time Dashboard**: BI 도구와 연동한 실시간 BSC 대시보드
- **AI 예측**: 선행 지표 기반 재무 성과 예측
- **OKR 융합**: BSC의 균형성 + OKR의 민첩성 결합

#### 3. 참고 문헌
- **Robert Kaplan & David Norton, "The Balanced Scorecard" (1996)**
- **Robert Kaplan & David Norton, "Strategy Maps" (2004)**
- **Balanced Scorecard Institute**

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [KPI (Key Performance Indicator)](@/studynotes/07_enterprise_systems/01_strategy/kpi.md): BSC의 구성 요소
- [OKR (Objectives and Key Results)](@/studynotes/07_enterprise_systems/01_strategy/okr.md): BSC의 Agile 버전
- [CSF (Critical Success Factor)](@/studynotes/07_enterprise_systems/01_strategy/csf.md): BSC KPI 도출의 전제
- [IT 거버넌스 (IT Governance)](@/studynotes/07_enterprise_systems/01_strategy/it_governance.md): IT BSC의 상위 체계
- [COBIT](@/studynotes/07_enterprise_systems/01_strategy/cobit.md): IT 거버넌스와 BSC의 융합

---

### 👶 어린이를 위한 3줄 비유 설명
1. BSC는 학교에서 공부, 운동, 친구관계, 예절을 골고루 잘하라고 적어둔 '목표표'와 같아요.
2. 시험 점수(재무)만 잘 받는 게 아니라, 친구들과 사이좋게 지내고(고객), 청소도 잘 하고(프로세스), 매일 독서도 하는 것(학습/성장)을 모두 챙겨요.
3. 이렇게 하면 공부만 잘하는 친구보다 훨씬 더 훌륭한 사람이 될 수 있답니다!
