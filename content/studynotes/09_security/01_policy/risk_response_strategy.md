+++
title = "위험 대응 전략 (Risk Response Strategy)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# 위험 대응 전략 (Risk Response Strategy)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 식별된 위험에 대해 조직이 취할 수 있는 4가지 전략(회피, 전가, 완화, 수용)을 체계적으로 분석하여 최적의 대응 방안을 수립합니다.
> 2. **가치**: 위험 대응 전략은 비용-효익 분석, 위험 식욭, 비즈니스 목표를 종합하여 보안 투자의 최적화를 도모합니다.
> 3. **융합**: 보험, 아웃소싱, 컴플라이언스, 비즈니스 연속성 계획과 연계하여 전사적 위험 관리(ERM)의 핵심 요소입니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**위험 대응 전략(Risk Response Strategy)**은 식별된 위험을 처리하기 위한 조직의 공식적인 접근 방식을 의미합니다. ISO 31000, ISO 27005, NIST SP 800-30 등 국제 표준에서 정의하는 4가지 핵심 전략은 다음과 같습니다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                    위험 대응 전략 4가지 (4T Model)                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  1. 회피 (Avoidance / Termination)                                │ │
│  │      ─────────────────────────────                                │ │
│  │      위험을 유발하는 활동 자체를 중단                              │ │
│  │      "하이리스크 활동을 아예 하지 않는다"                          │ │
│  │      예: 위험한 클라우드 서비스 미사용, 고위험 국가 사업 철수      │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  2. 전가 (Transfer / Sharing)                                     │ │
│  │      ────────────────────────                                     │ │
│  │      위험을 제3자에게 이전                                         │ │
│  │      "위험을 다른 주체와 공유하거나 이전한다"                       │ │
│  │      예: 사이버 보험, MSP 아웃소싱, SLA 계약                       │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  3. 완화 (Mitigation / Reduction)                                 │ │
│  │      ──────────────────────────────                               │ │
│  │      보안 통제로 위험 수준 저감                                    │ │
│  │      "위험을 조직이 감당할 수 있는 수준으로 낮춘다"                 │ │
│  │      예: 방화벽, EDR, 접근통제, 암호화, 교육                       │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  4. 수용 (Acceptance / Retention)                                 │ │
│  │      ──────────────────────────────                               │ │
│  │      위험을 있는 그대로 인정                                       │ │
│  │      "위험을 감수하고 활동을 계속한다"                             │ │
│  │      예: 저위험 위험, 완화 비용 과다, 잔여 위험                    │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 2. 위험 대응 전략 선택 기준

| 전략 | 선택 조건 | 비용 | 효과 | 적용 시나리오 |
|:---|:---|:---|:---|:---|
| **회피** | 위험 > 비즈니스 이익 | 없음/낮음 | 100% 제거 | 고위험/저수익 활동 |
| **전가** | 완화 비용 > 전가 비용 | 중간 | 부분 이전 | 재정적 손실 위험 |
| **완화** | 위험 > 식욭, 완화 가능 | 중간/높음 | 부분 감소 | 대부분의 보안 위험 |
| **수용** | 위험 ≤ 식욭, 완화 비용 과다 | 없음/낮음 | 없음 | 저위험, 잔여 위험 |

#### 3. 비유를 통한 이해
위험 대응 전략은 **'건강 관리'**에 비유할 수 있습니다.
- **회피**: 담배를 아예 피우지 않음 (폐암 위험 0%)
- **전가**: 건강 보험 가입 (치료비 부담 이전)
- **완화**: 금연, 운동, 건강 검진 (위험 감소)
- **수용**: 나이 듦에 따른 자연스러운 노화 위험 인정

#### 4. 등장 배경 및 발전 과정
1. **1980년대**: PMBOK에서 프로젝트 위험 대응 전략으로 정립
2. **1990년대**: COSO ERM에서 기업 위험 관리로 확장
3. **2000년대**: ISO 31000, ISO 27005 등 국제 표준화
4. **2010년대**: 사이버 위험 특화 모델 등장 (FAIR)
5. **현재**: AI 기반 동적 위험 대응, 실시간 전략 전환

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 위험 대응 전략 결정 매트릭스

```text
<<< 위험 대응 전략 선택 다이어그램 >>>

                        위험 수준 (Impact × Likelihood)
                                  │
                    높음          │           낮음
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
    높음 │    ┌──────────────────┐│┌──────────────────┐   │
         │    │    회 피         │││    완 화         │   │
         │    │  (Avoidance)     │││  (Mitigation)    │   │
  통제    │    │                  │││                  │   │
  효과성  │    │  - 활동 중단     │││  - 보안 통제     │   │
         │    │  - 시스템 폐기   │││  - 프로세스 개선 │   │
         │    └──────────────────┘│└──────────────────┘   │
         │                        │                        │
         │    ┌──────────────────┐│┌──────────────────┐   │
    낮음 │    │    전 가         │││    수 용         │   │
         │    │  (Transfer)      │││  (Acceptance)    │   │
         │    │                  │││                  │   │
         │    │  - 보험 가입     │││  - 위험 인정     │   │
         │    │  - 아웃소싱      │││  - 예산 비축     │   │
         │    └──────────────────┘│└──────────────────┘   │
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │

    ※ 정확한 위치는 위험 식욭, 비용-효익 분석 결과에 따라 결정
```

#### 2. 위험 대응 전략별 상세 분석

```text
<<< 1. 회피 (Avoidance) 상세 분석 >>>

    적용 조건:
    ┌─────────────────────────────────────────────────────────────────┐
    │  - 위험의 영향이 조직의 존립을 위협                               │
    │  - 위험 완화 비용이 활동의 이익을 초과                            │
    │  - 대안적 접근 방식이 존재                                        │
    │  - 법적/규제적 금지 사항                                          │
    └─────────────────────────────────────────────────────────────────┘

    구현 방법:
    ┌─────────────────────────────────────────────────────────────────┐
    │  1. 활동 중단: 위험한 비즈니스 활동 완전 중지                     │
    │  2. 시스템 폐기: 레거시 시스템 폐기, 새 시스템으로 교체           │
    │  3. 기술 변경: 취약한 기술 대신 안전한 대체 기술 사용             │
    │  4. 정책 변경: 위험한 관행 금지                                   │
    └─────────────────────────────────────────────────────────────────┘

    사례:
    ┌─────────────────────────────────────────────────────────────────┐
    │  - Windows XP 지원 중단 → 윈도우 10/11로 마이그레이션           │
    │  - 공개 Wi-Fi 사용 금지 → 전용망만 사용                          │
    │  - 특정 국가 데이터 센터 철수 → 데이터 주권 이슈 회피            │
    │  - 소셜 미디어 계정 운영 중단 → 계정 탈취 위험 회피              │
    └─────────────────────────────────────────────────────────────────┘


<<< 2. 전가 (Transfer) 상세 분석 >>>

    적용 조건:
    ┌─────────────────────────────────────────────────────────────────┐
    │  - 위험 완화 비용 > 전가 비용                                    │
    │  - 제3자가 위험을 더 효과적으로 관리 가능                        │
    │  - 재정적 손실이 주요 우려                                       │
    │  - 법적 책임 이전 가능                                           │
    └─────────────────────────────────────────────────────────────────┘

    구현 방법:
    ┌─────────────────────────────────────────────────────────────────┐
    │  1. 보험: 사이버 보험, 재해 보험                                 │
    │  2. 아웃소싱: MSP, SOC-as-a-Service                              │
    │  3. 계약: SLA, 책임 한계 조항, 보상 조항                         │
    │  4. 컨소시엄: 위험 공유 pool 구성                                │
    └─────────────────────────────────────────────────────────────────┘

    사례:
    ┌─────────────────────────────────────────────────────────────────┐
    │  - 사이버 보험 가입 (랜섬웨어, 데이터 유출 보상)                 │
    │  - MSSP에 보안 관제 위탁                                         │
    │  - 클라우드 서비스 SLA (99.99% 가용성 보장)                      │
    │  - 공급업체와의 책임 분담 계약                                   │
    └─────────────────────────────────────────────────────────────────┘


<<< 3. 완화 (Mitigation) 상세 분석 >>>

    적용 조건:
    ┌─────────────────────────────────────────────────────────────────┐
    │  - 위험 > 위험 식욭                                              │
    │  - 완화 통제의 효과성이 입증됨                                   │
    │  - 완화 비용이 수용 가능한 수준                                  │
    │  - 기술적/운영적 해결책 존재                                     │
    └─────────────────────────────────────────────────────────────────┘

    구현 방법:
    ┌─────────────────────────────────────────────────────────────────┐
    │  1. 기술적 통제: 방화벽, IDS/IPS, 암호화, MFA                    │
    │  2. 관리적 통제: 정책, 교육, 감사, 인시던트 대응                 │
    │  3. 물리적 통제: 출입 통제, CCTV, 잠금 장치                      │
    │  4. 복구 통제: 백업, DRP, 보험                                   │
    └─────────────────────────────────────────────────────────────────┘

    사례:
    ┌─────────────────────────────────────────────────────────────────┐
    │  - 다층 방화벽 구축으로 침입 차단                                │
    │  - EDR 도입으로 악성코드 탐지 및 차단                            │
    │  - MFA 적용으로 계정 탈취 방지                                   │
    │  - 정기적 보안 교육으로 내부자 위협 감소                         │
    └─────────────────────────────────────────────────────────────────┘


<<< 4. 수용 (Acceptance) 상세 분석 >>>

    적용 조건:
    ┌─────────────────────────────────────────────────────────────────┐
    │  - 위험 ≤ 위험 식욭                                              │
    │  - 완화 비용 > 위험 비용 (ALE)                                   │
    │  - 완화가 기술적으로 불가능                                      │
    │  - 비즈니스 필수 활동 (수용 불가피)                              │
    └─────────────────────────────────────────────────────────────────┘

    구현 방법:
    ┌─────────────────────────────────────────────────────────────────┐
    │  1. 수동 수용: 별도 조치 없이 위험 인정                          │
    │  2. 능동 수용: 예산 비축(Reserve), 대응 계획 수립                │
    │  3. 잔여 위험 수용: 통제 후 남은 위험 인정                       │
    │  4. 비즈니스 수용: 이익을 위해 위험 감수                         │
    └─────────────────────────────────────────────────────────────────┘

    사례:
    ┌─────────────────────────────────────────────────────────────────┐
    │  - 저위험 취약점 (CVSS 1-3) 패치 연기                            │
    │  - DDoS 공격 위험 일부 수용 (완전 방어 비용 과다)                │
    │  - 신규 서비스 런칭 시 일부 보안 위험 수용                       │
    │  - 사이버 보험 면책액(Deductible)까지의 손실 수용                │
    └─────────────────────────────────────────────────────────────────┘
```

#### 3. Python 구현: 위험 대응 전략 결정 시스템

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from decimal import Decimal

class RiskResponseStrategy(Enum):
    """위험 대응 전략"""
    AVOID = "회피"
    TRANSFER = "전가"
    MITIGATE = "완화"
    ACCEPT = "수용"

class RiskCategory(Enum):
    """위험 카테고리"""
    CYBER = "사이버 보안"
    OPERATIONAL = "운영"
    COMPLIANCE = "규제 준수"
    STRATEGIC = "전략"
    FINANCIAL = "재무"

@dataclass
class Risk:
    """위험 항목"""
    risk_id: str
    name: str
    category: RiskCategory
    likelihood: float  # 0.0 ~ 1.0
    impact: float  # 0.0 ~ 1.0 (정규화된 영향도)
    asset_value: float  # 자산 가치 (원)
    description: str = ""

    @property
    def risk_score(self) -> float:
        """위험 점수"""
        return self.likelihood * self.impact

    @property
    def ale(self) -> float:
        """연간 예상 손실액 (간소화)"""
        # ALE = 자산가치 × 영향도 × 발생확률
        return self.asset_value * self.impact * self.likelihood

@dataclass
class MitigationOption:
    """완화 옵션"""
    name: str
    cost: float  # 연간 비용
    effectiveness: float  # 0.0 ~ 1.0
    description: str = ""

    def calculate_reduced_ale(self, original_ale: float) -> float:
        """완화 후 ALE 계산"""
        return original_ale * (1 - self.effectiveness)

@dataclass
class TransferOption:
    """전가 옵션"""
    name: str
    cost: float  # 연간 비용 (보험료 등)
    coverage: float  # 보장 한도
    deductible: float  # 자기 부담금
    description: str = ""

@dataclass
class RiskAppetite:
    """위험 식욭"""
    category: RiskCategory
    max_likelihood: float
    max_impact: float
    max_ale: float

    def is_within_appetite(self, risk: Risk) -> bool:
        """위험 식욭 내 여부 판단"""
        return (
            risk.likelihood <= self.max_likelihood and
            risk.impact <= self.max_impact and
            risk.ale <= self.max_ale
        )

@dataclass
class RiskResponse:
    """위험 대응 결정"""
    risk_id: str
    strategy: RiskResponseStrategy
    rationale: str
    selected_option: Optional[str] = None
    residual_risk: float = 0.0
    implementation_cost: float = 0.0
    approved_by: str = ""
    approval_date: str = ""


class RiskResponseAnalyzer:
    """위험 대응 분석기"""

    def __init__(self):
        self.risks: Dict[str, Risk] = {}
        self.risk_appetites: Dict[RiskCategory, RiskAppetite] = {}
        self.mitigation_options: Dict[str, List[MitigationOption]] = {}
        self.transfer_options: Dict[str, List[TransferOption]] = {}
        self.responses: Dict[str, RiskResponse] = {}

    def add_risk(self, risk: Risk):
        """위험 등록"""
        self.risks[risk.risk_id] = risk

    def set_risk_appetite(self, appetite: RiskAppetite):
        """위험 식욭 설정"""
        self.risk_appetites[appetite.category] = appetite

    def add_mitigation_option(self, risk_id: str, option: MitigationOption):
        """완화 옵션 추가"""
        if risk_id not in self.mitigation_options:
            self.mitigation_options[risk_id] = []
        self.mitigation_options[risk_id].append(option)

    def add_transfer_option(self, risk_id: str, option: TransferOption):
        """전가 옵션 추가"""
        if risk_id not in self.transfer_options:
            self.transfer_options[risk_id] = []
        self.transfer_options[risk_id].append(option)

    def analyze_strategy(self, risk_id: str) -> Dict:
        """최적 대응 전략 분석"""
        risk = self.risks.get(risk_id)
        if not risk:
            return {}

        appetite = self.risk_appetites.get(risk.category)
        analysis = {
            'risk_id': risk_id,
            'risk_name': risk.name,
            'risk_score': risk.risk_score,
            'ale': risk.ale,
            'is_within_appetite': appetite.is_within_appetite(risk) if appetite else None,
            'strategy_analysis': {}
        }

        # 1. 회피 분석
        avoid_analysis = self._analyze_avoid(risk)
        analysis['strategy_analysis']['avoid'] = avoid_analysis

        # 2. 전가 분석
        transfer_analysis = self._analyze_transfer(risk)
        analysis['strategy_analysis']['transfer'] = transfer_analysis

        # 3. 완화 분석
        mitigate_analysis = self._analyze_mitigate(risk)
        analysis['strategy_analysis']['mitigate'] = mitigate_analysis

        # 4. 수용 분석
        accept_analysis = self._analyze_accept(risk, appetite)
        analysis['strategy_analysis']['accept'] = accept_analysis

        # 최적 전략 추천
        analysis['recommended_strategy'] = self._recommend_strategy(analysis)

        return analysis

    def _analyze_avoid(self, risk: Risk) -> Dict:
        """회피 전략 분석"""
        # 회피는 위험을 100% 제거하지만 기회비용 발생
        return {
            'strategy': RiskResponseStrategy.AVOID.value,
            'risk_reduction': 1.0,  # 100% 제거
            'cost': 0,  # 직접 비용 없음
            'opportunity_cost': risk.asset_value,  # 기회비용
            'feasibility': 'low',  # 실현 가능성
            'recommendation': '고위험, 대안 존재 시 고려'
        }

    def _analyze_transfer(self, risk: Risk) -> Dict:
        """전가 전략 분석"""
        options = self.transfer_options.get(risk.risk_id, [])

        if not options:
            return {
                'strategy': RiskResponseStrategy.TRANSFER.value,
                'feasibility': 'none',
                'recommendation': '전가 옵션 없음'
            }

        best_option = min(options, key=lambda x: x.cost)
        transferred = min(best_option.coverage, risk.ale - best_option.deductible)
        residual = risk.ale - transferred

        return {
            'strategy': RiskResponseStrategy.TRANSFER.value,
            'best_option': best_option.name,
            'cost': best_option.cost,
            'coverage': best_option.coverage,
            'deductible': best_option.deductible,
            'transferred_amount': transferred,
            'residual_ale': residual,
            'risk_reduction': transferred / risk.ale if risk.ale > 0 else 0,
            'feasibility': 'high',
            'recommendation': '재정적 손실 보호에 효과적'
        }

    def _analyze_mitigate(self, risk: Risk) -> Dict:
        """완화 전략 분석"""
        options = self.mitigation_options.get(risk.risk_id, [])

        if not options:
            return {
                'strategy': RiskResponseStrategy.MITIGATE.value,
                'feasibility': 'limited',
                'recommendation': '완화 옵션 정의 필요'
            }

        # ROI 기준 최적 옵션 선택
        for option in options:
            reduced_ale = option.calculate_reduced_ale(risk.ale)
            option_roi = (risk.ale - reduced_ale - option.cost) / option.cost if option.cost > 0 else 0

        best_option = max(options, key=lambda x: x.effectiveness / x.cost if x.cost > 0 else 0)
        reduced_ale = best_option.calculate_reduced_ale(risk.ale)
        net_benefit = risk.ale - reduced_ale - best_option.cost

        return {
            'strategy': RiskResponseStrategy.MITIGATE.value,
            'best_option': best_option.name,
            'cost': best_option.cost,
            'effectiveness': best_option.effectiveness,
            'original_ale': risk.ale,
            'reduced_ale': reduced_ale,
            'risk_reduction': best_option.effectiveness,
            'net_benefit': net_benefit,
            'roi': net_benefit / best_option.cost * 100 if best_option.cost > 0 else 0,
            'feasibility': 'high',
            'recommendation': 'ROI > 0이면 도입 권장'
        }

    def _analyze_accept(self, risk: Risk, appetite: Optional[RiskAppetite]) -> Dict:
        """수용 전략 분석"""
        is_acceptable = appetite.is_within_appetite(risk) if appetite else False

        return {
            'strategy': RiskResponseStrategy.ACCEPT.value,
            'is_within_appetite': is_acceptable,
            'ale': risk.ale,
            'cost': 0,
            'risk_reduction': 0,
            'feasibility': 'high' if is_acceptable else 'low',
            'recommendation': '위험 식욭 내면 수용 가능, 아니면 추가 조치 필요'
        }

    def _recommend_strategy(self, analysis: Dict) -> Dict:
        """최적 전략 추천"""
        strategies = analysis['strategy_analysis']

        # 의사결정 규칙
        # 1. 수용 가능하면 수용
        if strategies.get('accept', {}).get('is_within_appetite'):
            return {
                'strategy': RiskResponseStrategy.ACCEPT.value,
                'rationale': '위험 식욭 내에 있어 수용 가능'
            }

        # 2. 완화 ROI > 0이면 완화
        mitigate = strategies.get('mitigate', {})
        if mitigate.get('roi', 0) > 0:
            return {
                'strategy': RiskResponseStrategy.MITIGATE.value,
                'rationale': f"완화 ROI {mitigate['roi']:.0f}%로 비용 효율적",
                'option': mitigate.get('best_option')
            }

        # 3. 전가 비용 < ALE면 전가
        transfer = strategies.get('transfer', {})
        if transfer.get('feasibility') == 'high' and transfer.get('cost', float('inf')) < analysis['ale']:
            return {
                'strategy': RiskResponseStrategy.TRANSFER.value,
                'rationale': f"전가 비용 {transfer['cost']:,.0f}원이 ALE {analysis['ale']:,.0f}원보다 낮음",
                'option': transfer.get('best_option')
            }

        # 4. 위험 점수 매우 높으면 회피
        if analysis['risk_score'] > 0.7:
            return {
                'strategy': RiskResponseStrategy.AVOID.value,
                'rationale': '위험 점수가 매우 높아 활동 재고 필요'
            }

        # 5. 기본: 수용 (능동적)
        return {
            'strategy': RiskResponseStrategy.ACCEPT.value,
            'rationale': '다른 전략의 비용 효율성이 낮음, 예산 비축 권장'
        }

    def generate_response_plan(self, risk_id: str, strategy: RiskResponseStrategy,
                               option: str = None) -> RiskResponse:
        """대응 계획 생성"""
        risk = self.risks.get(risk_id)
        if not risk:
            return None

        response = RiskResponse(
            risk_id=risk_id,
            strategy=strategy,
            rationale=self._get_rationale(risk_id, strategy, option),
            selected_option=option,
            residual_risk=self._calculate_residual(risk, strategy, option),
            implementation_cost=self._calculate_cost(risk_id, strategy, option)
        )

        self.responses[risk_id] = response
        return response

    def _get_rationale(self, risk_id: str, strategy: RiskResponseStrategy,
                       option: str) -> str:
        """근거 작성"""
        rationales = {
            RiskResponseStrategy.AVOID: "위험의 영향이 비즈니스 이익을 초과하여 활동 중단",
            RiskResponseStrategy.TRANSFER: f"{option}을 통한 위험 이전",
            RiskResponseStrategy.MITIGATE: f"{option}을 통한 위험 저감",
            RiskResponseStrategy.ACCEPT: "위험 식욭 내 또는 완화 비용 과다로 수용"
        }
        return rationales.get(strategy, "")

    def _calculate_residual(self, risk: Risk, strategy: RiskResponseStrategy,
                           option: str) -> float:
        """잔여 위험 계산"""
        if strategy == RiskResponseStrategy.AVOID:
            return 0
        elif strategy == RiskResponseStrategy.ACCEPT:
            return risk.ale
        elif strategy == RiskResponseStrategy.MITIGATE:
            options = self.mitigation_options.get(risk.risk_id, [])
            for opt in options:
                if opt.name == option:
                    return opt.calculate_reduced_ale(risk.ale)
        elif strategy == RiskResponseStrategy.TRANSFER:
            options = self.transfer_options.get(risk.risk_id, [])
            for opt in options:
                if opt.name == option:
                    return opt.deductible
        return risk.ale

    def _calculate_cost(self, risk_id: str, strategy: RiskResponseStrategy,
                        option: str) -> float:
        """비용 계산"""
        risk = self.risks.get(risk_id)
        if not risk:
            return 0

        if strategy == RiskResponseStrategy.AVOID:
            return 0  # 직접 비용 없음
        elif strategy == RiskResponseStrategy.ACCEPT:
            return 0
        elif strategy == RiskResponseStrategy.MITIGATE:
            options = self.mitigation_options.get(risk_id, [])
            for opt in options:
                if opt.name == option:
                    return opt.cost
        elif strategy == RiskResponseStrategy.TRANSFER:
            options = self.transfer_options.get(risk_id, [])
            for opt in options:
                if opt.name == option:
                    return opt.cost
        return 0


# 사용 예시
if __name__ == "__main__":
    # 분석기 생성
    analyzer = RiskResponseAnalyzer()

    # 위험 식욭 설정
    analyzer.set_risk_appetite(RiskAppetite(
        category=RiskCategory.CYBER,
        max_likelihood=0.3,
        max_impact=0.4,
        max_ale=100_000_000  # 1억원
    ))

    # 위험 등록
    analyzer.add_risk(Risk(
        risk_id="R-001",
        name="랜섬웨어 공격",
        category=RiskCategory.CYBER,
        likelihood=0.4,
        impact=0.8,
        asset_value=500_000_000,  # 5억원
        description="랜섬웨어로 인한 데이터 암호화 및 업무 중단"
    ))

    # 완화 옵션 추가
    analyzer.add_mitigation_option("R-001", MitigationOption(
        name="EDR + 백업 시스템",
        cost=50_000_000,  # 5천만원/년
        effectiveness=0.7,
        description="EDR 도입 및 정기 백업"
    ))

    analyzer.add_mitigation_option("R-001", MitigationOption(
        name="격리망 구축",
        cost=100_000_000,  # 1억원/년
        effectiveness=0.9,
        description="네트워크 분리로 침해 확산 방지"
    ))

    # 전가 옵션 추가
    analyzer.add_transfer_option("R-001", TransferOption(
        name="사이버 보험",
        cost=20_000_000,  # 2천만원/년
        coverage=400_000_000,  # 4억원 보장
        deductible=50_000_000,  # 5천만원 자부담
        description="랜섬웨어 및 데이터 유출 보장"
    ))

    # 분석 수행
    print("=" * 70)
    print("위험 대응 전략 분석 결과")
    print("=" * 70)

    analysis = analyzer.analyze_strategy("R-001")

    print(f"\n위험명: {analysis['risk_name']}")
    print(f"위험 점수: {analysis['risk_score']:.2f}")
    print(f"ALE: {analysis['ale']:,.0f}원")
    print(f"위험 식욭 내: {'예' if analysis['is_within_appetite'] else '아니오'}")

    print("\n--- 전략별 분석 ---")
    for strategy, details in analysis['strategy_analysis'].items():
        print(f"\n[{strategy.upper()}]")
        for key, value in details.items():
            if key not in ['strategy']:
                print(f"  {key}: {value}")

    print("\n--- 추천 전략 ---")
    rec = analysis['recommended_strategy']
    print(f"전략: {rec['strategy']}")
    print(f"근거: {rec['rationale']}")
    if 'option' in rec:
        print(f"옵션: {rec['option']}")

    # 대응 계획 생성
    response = analyzer.generate_response_plan(
        "R-001",
        RiskResponseStrategy.MITIGATE,
        "EDR + 백업 시스템"
    )

    print("\n--- 대응 계획 ---")
    print(f"전략: {response.strategy.value}")
    print(f"선택 옵션: {response.selected_option}")
    print(f"잔여 위험(ALE): {response.residual_risk:,.0f}원")
    print(f"구현 비용: {response.implementation_cost:,.0f}원/년")
    print(f"근거: {response.rationale}")
```

---

### III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 전략별 비용-효익 비교

| 전략 | 직접 비용 | 간접 비용 | 위험 감소 | 잔여 위험 | 적용성 |
|:---|:---|:---|:---|:---|:---|
| **회피** | 없음 | 기회비용(큼) | 100% | 0% | 제한적 |
| **전가** | 중간 | 관리 오버헤드 | 70~90% | 10~30% | 재무적 위험 |
| **완화** | 높음 | 운영 복잡도 | 50~80% | 20~50% | 대부분 |
| **수용** | 없음 | 잠재적 손실 | 0% | 100% | 저위험 |

#### 2. 위험 유형별 적합 전략

| 위험 유형 | 1순위 전략 | 2순위 전략 | 이유 |
|:---|:---|:---|:---|
| 랜섬웨어 | 완화 | 전가 | 기술적 대응 + 보험 |
| 내부자 위협 | 완화 | - | 기술/관리적 통제 필요 |
| 공급망 공격 | 전가 | 완화 | SLA + 통제 |
| DDoS | 완화 | 수용 | 방어 + 일부 수용 |
| Zero-Day | 전가 | 수용 | 보험 + 수용 |
| 법적/규제 | 회피 | 완화 | 준수 필수 |

#### 3. 과목 융합 관점 분석
- **위험 관리**: ERM 프레임워크의 핵심 프로세스
- **재무 관리**: 보험, 예산 비축, 재무적 영향 분석
- **법무**: 계약, SLA, 책임 분담, 규제 준수
- **비즈니스 연속성**: BCP/DRP와 연계
- **공급망 관리**: 공급업체 위험 전가

---

### IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 랜섬웨어 대응 전략**
- 상황: ALE 8천만원, 위험 식욭 2천만원
- 분석:
  - 완화(EDR+백업): 비용 4천만원, 효과 70% → 잔여 2,400만원
  - 전가(보험): 비용 1천만원, 보장 6천만원 → 잔여 2천만원
- 판단: 완화+전가 복합 전략 → 잔여 720만원 (식욭 내)

**시나리오 2: 클라우드 이관 위험**
- 상황: 데이터 주권 이슈, 규제 위반 가능성
- 분석:
  - 회피: 특정 리전 미사용 → 비즈니스 제약
  - 완화: 암호화, 데이터 마스킹 → 부분 해결
- 판단: 회피(특정 국가 리전 사용 안 함) + 완화(나머지 리전 보안 강화)

**시나리오 3: 레거시 시스템 보안**
- 상황: Windows Server 2008, 패치 불가
- 분석:
  - 완화: 네트워크 격리 → 비용 높음
  - 회피: 시스템 교체 → 프로젝트 필요
- 판단: 단기 완화(격리) + 중장기 회피(교체)

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] 위험 식욭 명확 정의
- [ ] ALE 정확 산정
- [ ] 각 전략별 비용-효익 분석
- [ ] 복합 전략 가능성 검토
- [ ] 이해관계자 합의
- [ ] 정기 재평가 프로세스

#### 3. 안티패턴 (Anti-patterns)
- **단일 전략 고집**: 복합 전략 필요성 무시
- **수용 남용**: "어차피 일어나지 않아" 식 안일한 수용
- **완화 과신**: 통제 효과성 과대평가
- **비용 무시**: 전략 선택 시 비용 고려 안 함

---

### V. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | 내용 | 측정 방법 |
|:---|:---|:---|
| 보안 투자 최적화 | 적절한 전략 선택으로 비용 절감 | 대응 비용/ALE 비율 |
| 위험 노출 관리 | 잔여 위험을 식욭 내로 유지 | 위험 식욭 초과 건수 |
| 의사결정 일관성 | 표준화된 의사결정 프로세스 | 전략 선택 일관성 |
| 컴플라이언스 | 규제 요건 충족 방식 문서화 | 감사 지적 감소 |

#### 2. 미래 전망 및 진화 방향
- **AI 기반 전략 추천**: ML로 최적 전략 자동 추천
- **실시간 전략 전환**: 위험 변화에 따른 동적 전략 변경
- **통합 위험 플랫폼**: 전사적 위험 통합 관리
- **동적 보험**: 실시간 위험 기반 보험료 산정

#### 3. 참고 표준/가이드
- **ISO 31000**: 위험 관리 - 위험 처리 전략
- **ISO/IEC 27005**: 정보보안 위험 관리
- **NIST SP 800-30**: 위험 평가 - 대응 권고사항
- **COSO ERM**: 전사적 위험 관리 - 위험 대응

---

### 관련 개념 맵 (Knowledge Graph)
- [위험 관리](@/studynotes/09_security/01_policy/risk_management.md) : 위험 대응 전략의 상위 개념
- [잔여 위험](@/studynotes/09_security/01_policy/residual_risk.md) : 대응 후 남은 위험
- [ALE/ARO/SLE](@/studynotes/09_security/01_policy/ale_aro_sle.md) : 정량적 위험 분석
- [심층 방어](@/studynotes/09_security/01_policy/defense_in_depth.md) : 완화 전략의 구현
- [보안 정책](@/studynotes/09_security/01_policy/security_policy.md) : 위험 식욭 정의

---

### 어린이를 위한 3줄 비유 설명
1. **피하기(회피)**: "위험한 놀이터에 안 가면 다치지 않아요!" - 아예 그 활동을 하지 않는 거예요.
2. **도와달라고 하기(전가)**: "형아가 지켜줘!" - 다른 사람에게 책임을 맡기는 거예요.
3. **준비하기(완화)**: "헬멧 쓰고 자전거 탈래!" - 위험을 줄이는 방법을 쓰는 거예요. "조금은 다칠 수 있어(수용)"
