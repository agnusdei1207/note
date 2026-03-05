+++
title = "ALE / ARO / SLE (연간 손실 예상액 계산)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# ALE / ARO / SLE (연간 손실 예상액 계산)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 정량적 위험 분석의 핵심 공식으로, ALE = ARO × SLE를 통해 연간 예상 손실액을 산출하여 보안 투자의 경제적 정당성을 확보합니다.
> 2. **가치**: 보안 통제 도입 비용과 기대 손실 감소액을 비교하여 ROI 기반 의사결정을 가능하게 합니다.
> 3. **융합**: 보험료 산출, 예산 배분, 비즈니스 연속성 계획(BCP), 보안 투자 우선순위 결정에 활용됩니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**ALE/ARO/SLE**는 정량적 위험 분석(Quantitative Risk Analysis)의 핵심 지표로, 위험을 금전적 가치로 환산하여 보안 투자의 경제적 근거를 제시합니다.

**핵심 용어 정의**:

| 용어 | 영문 명칭 | 정의 | 단위 |
|:---|:---|:---|:---|
| **SLE** | Single Loss Expectancy | 단일 사고 발생 시 예상 손실액 | 원(\) |
| **ARO** | Annualized Rate of Occurrence | 연간 사고 발생 확률 (빈도) | 회/년 |
| **ALE** | Annualized Loss Expectancy | 연간 총 예상 손실액 | 원/년 |

**핵심 공식**:
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│    ALE (연간 예상 손실액) = ARO × SLE                        │
│                                                             │
│    = (연간 발생 횟수) × (단일 사고 손실액)                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

    여기서:
    SLE = Asset Value × Exposure Factor (EF)

    - Asset Value (자산 가치): 정보 자산의 금전적 가치
    - Exposure Factor (노출 계수): 사고 발생 시 손실 비율 (0~1)
```

#### 2. 비유를 통한 이해
ALE/ARO/SLE는 **'자동차 보험료 계산'**에 비유할 수 있습니다.
- **SLE (단일 사고 손실액)**: 사고 한 번 낼 때 수리비 (예: 500만원)
- **ARO (연간 사고 빈도)**: 1년에 사고 날 확률 (예: 0.1회/년 = 10년에 1번)
- **ALE (연간 예상 손실액)**: 500만원 × 0.1 = 50만원/년 → 연간 보험료 결정 근거

#### 3. 등장 배경 및 발전 과정
1. **1960년대**: 보험 수학(Actuarial Science)에서 위험 정량화 시작
2. **1970년대**: 미국 국방부(DOD)에서 정보시스템 위험 분석에 도입
3. **1990년대**: NIST SP 800-30 등 표준화된 방법론 정립
4. **2000년대**: 기업 위험 관리(ERM) 프레임워크와 통합
5. **현재**: FAIR(Factor Analysis of Information Risk) 등 발전된 모델 등장

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. SLE 산출 공식 상세 분석

```text
<<< SLE (Single Loss Expectancy) 산출 구조 >>>

    ┌─────────────────────────────────────────────────────────────────┐
    │                    SLE = Asset Value × EF                       │
    └─────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
    ┌───────────────────────────┐   ┌───────────────────────────────┐
    │     Asset Value (자산가치) │   │  Exposure Factor (노출계수)   │
    ├───────────────────────────┤   ├───────────────────────────────┤
    │ - 하드웨어 교체 비용       │   │ - 사고 시 손실 비율 (0~1)     │
    │ - 소프트웨어 라이선스      │   │ - 완전 손실: EF = 1.0 (100%)  │
    │ - 데이터 복구 비용         │   │ - 부분 손실: EF = 0.5 (50%)   │
    │ - 업무 중단 손실           │   │ - 경미 손실: EF = 0.1 (10%)   │
    │ - 평판 손실                │   │                               │
    │ - 법적 비용/벌금           │   │                               │
    └───────────────────────────┘   └───────────────────────────────┘

    <<< 자산 가치 산정 방법 >>>

    1. 원가법 (Cost Approach)
       자산가치 = 취득원가 - 감가상각누계액

    2. 시장법 (Market Approach)
       자산가치 = 유사 자산 시장 거래가격

    3. 수익법 (Income Approach)
       자산가치 = Σ (미래 예상 현금흐름 / (1+할인율)^n)

    4. 비용법 (Cost to Recreate)
       자산가치 = 자산 재생성/복구에 소요되는 총비용
```

#### 2. ARO 산정 방법

| 산정 방법 | 설명 | 적용 예시 | 정확도 |
|:---|:---|:---|:---|
| **과거 데이터 분석** | 유사 사고 이력 기반 | "지난 5년간 DDoS 3회" → ARO=0.6 | 높음 |
| **업계 평균** | 동종 업계 통계 활용 | "금융권 평균 피싱 사고 0.2회/년" | 중간 |
| **전문가 판단** | 보안 전문가 추정 | "전문가 5명 평균 0.3회/년" | 중간 |
| **시뮬레이션** | 몬테카를로 시뮬레이션 | 10,000회 시뮬레이션 결과 | 높음 |
| **위협 인텔리전스** | CTI 데이터 기반 | "APT 그룹 TTP 분석" | 높음 |

#### 3. 정량적 위험 분석 종합 다이어그램

```text
<<< 정량적 위험 분석 프로세스 >>>

  ┌──────────────────────────────────────────────────────────────────────┐
  │                    Step 1: 자산 식별 및 가치 산정                     │
  │  ┌────────────────────────────────────────────────────────────────┐ │
  │  │  Asset ID    │ 자산명           │ 카테고리    │ 가치(원)      │ │
  │  │  AS-001      │ 고객 DB 서버     │ 데이터     │ 500,000,000   │ │
  │  │  AS-002      │ ERP 시스템       │ 애플리케이션│ 300,000,000   │ │
  │  │  AS-003      │ 웹 서버 군       │ 인프라     │ 100,000,000   │ │
  │  └────────────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │                    Step 2: 위협 및 취약점 식별                        │
  │  ┌────────────────────────────────────────────────────────────────┐ │
  │  │  위협 ID     │ 위협 유형        │ 대상 자산   │ 취약점        │ │
  │  │  TH-001      │ 랜섬웨어 감염    │ AS-001     │ 패치 미적용   │ │
  │  │  TH-002      │ DDoS 공격        │ AS-003     │ 트래픽 과부하 │ │
  │  │  TH-003      │ 내부자 데이터 유출│ AS-001    │ 접근 통제 미흡│ │
  │  └────────────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │                    Step 3: SLE (단일 손실 예상액) 산출                │
  │  ┌────────────────────────────────────────────────────────────────┐ │
  │  │  위협 ID     │ 자산가치(AV)     │ EF    │ SLE (=AV×EF)       │ │
  │  │  TH-001      │ 500,000,000원    │ 0.8   │ 400,000,000원      │ │
  │  │  TH-002      │ 100,000,000원    │ 0.3   │ 30,000,000원       │ │
  │  │  TH-003      │ 500,000,000원    │ 1.0   │ 500,000,000원      │ │
  │  └────────────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │                    Step 4: ARO (연간 발생 빈도) 산정                  │
  │  ┌────────────────────────────────────────────────────────────────┐ │
  │  │  위협 ID     │ 위협 유형        │ 과거 데이터  │ ARO (회/년)  │ │
  │  │  TH-001      │ 랜섬웨어         │ 5년간 1회   │ 0.2          │ │
  │  │  TH-002      │ DDoS             │ 연 2회      │ 2.0          │ │
  │  │  TH-003      │ 내부자 유출      │ 3년간 1회   │ 0.33         │ │
  │  └────────────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │                    Step 5: ALE (연간 손실 예상액) 산출                │
  │  ┌────────────────────────────────────────────────────────────────┐ │
  │  │  위협 ID     │ SLE            │ ARO     │ ALE (=SLE×ARO)    │ │
  │  │  TH-001      │ 400,000,000원  │ 0.2     │ 80,000,000원      │ │
  │  │  TH-002      │ 30,000,000원   │ 2.0     │ 60,000,000원      │ │
  │  │  TH-003      │ 500,000,000원  │ 0.33    │ 165,000,000원     │ │
  │  │              │                │ 총 ALE: │ 305,000,000원/년  │ │
  │  └────────────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │                    Step 6: 비용-효익 분석 (Cost-Benefit)             │
  │  ┌────────────────────────────────────────────────────────────────┐ │
  │  │  통제 도입 비용          │ ALE 감소 효과       │ ROI            │ │
  │  │  EDR 솔루션: 30백만원/년 │ 랜섬웨어 ALE: -60%  │ 160%           │ │
  │  │  DDoS 방어: 20백만원/년  │ DDoS ALE: -80%      │ 140%           │ │
  │  │  DLP 도입: 40백만원/년   │ 유출 ALE: -50%      │ 106%           │ │
  │  │  총 투자: 90백만원/년    │ 총 ALE 감소: 167백만│ ROI: 85%       │ │
  │  └────────────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────────────┘
```

#### 4. Python 구현: ALE 계산기

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import statistics

class AssetCategory(Enum):
    HARDWARE = "하드웨어"
    SOFTWARE = "소프트웨어"
    DATA = "데이터"
    PERSONNEL = "인력"
    REPUTATION = "평판"

class ThreatType(Enum):
    MALWARE = "악성코드"
    RANSOMWARE = "랜섬웨어"
    DDOS = "DDoS"
    INSIDER = "내부자 위협"
    PHISHING = "피싱"
    APT = "APT"

@dataclass
class Asset:
    """정보 자산"""
    asset_id: str
    name: str
    category: AssetCategory
    value: float  # 자산 가치 (원)
    description: str = ""

@dataclass
class Threat:
    """위협"""
    threat_id: str
    name: str
    threat_type: ThreatType
    target_asset_id: str
    exposure_factor: float  # 0.0 ~ 1.0
    annual_rate: float  # 연간 발생 빈도
    description: str = ""

@dataclass
class RiskCalculation:
    """위험 계산 결과"""
    threat_id: str
    asset_id: str
    asset_value: float
    exposure_factor: float
    sle: float  # Single Loss Expectancy
    aro: float  # Annualized Rate of Occurrence
    ale: float  # Annualized Loss Expectancy

class QuantitativeRiskAnalyzer:
    """정량적 위험 분석기"""

    def __init__(self):
        self.assets: Dict[str, Asset] = {}
        self.threats: Dict[str, Threat] = {}
        self.calculations: List[RiskCalculation] = []

    def add_asset(self, asset: Asset):
        """자산 등록"""
        self.assets[asset.asset_id] = asset

    def add_threat(self, threat: Threat):
        """위협 등록"""
        self.threats[threat.threat_id] = threat

    def calculate_sle(self, asset_value: float, exposure_factor: float) -> float:
        """SLE (Single Loss Expectancy) 계산"""
        return asset_value * exposure_factor

    def calculate_ale(self, sle: float, aro: float) -> float:
        """ALE (Annualized Loss Expectancy) 계산"""
        return sle * aro

    def perform_analysis(self) -> List[RiskCalculation]:
        """전체 위험 분석 수행"""
        self.calculations = []

        for threat in self.threats.values():
            asset = self.assets.get(threat.target_asset_id)
            if asset is None:
                continue

            sle = self.calculate_sle(asset.value, threat.exposure_factor)
            ale = self.calculate_ale(sle, threat.annual_rate)

            calculation = RiskCalculation(
                threat_id=threat.threat_id,
                asset_id=asset.asset_id,
                asset_value=asset.value,
                exposure_factor=threat.exposure_factor,
                sle=sle,
                aro=threat.annual_rate,
                ale=ale
            )
            self.calculations.append(calculation)

        return self.calculations

    def get_total_ale(self) -> float:
        """총 연간 예상 손실액"""
        return sum(calc.ale for calc in self.calculations)

    def get_risk_by_asset(self) -> Dict[str, float]:
        """자산별 총 ALE"""
        risk_by_asset = {}
        for calc in self.calculations:
            if calc.asset_id not in risk_by_asset:
                risk_by_asset[calc.asset_id] = 0
            risk_by_asset[calc.asset_id] += calc.ale
        return risk_by_asset

    def get_risk_by_threat_type(self) -> Dict[ThreatType, float]:
        """위협 유형별 총 ALE"""
        risk_by_type = {}
        for calc in self.calculations:
            threat = self.threats.get(calc.threat_id)
            if threat:
                if threat.threat_type not in risk_by_type:
                    risk_by_type[threat.threat_type] = 0
                risk_by_type[threat.threat_type] += calc.ale
        return risk_by_type

    def prioritize_risks(self) -> List[RiskCalculation]:
        """위험 우선순위 정렬 (ALE 기준)"""
        return sorted(self.calculations, key=lambda x: x.ale, reverse=True)


@dataclass
class SecurityControl:
    """보안 통제"""
    control_id: str
    name: str
    annual_cost: float
    target_threat_ids: List[str]
    effectiveness: float  # 0.0 ~ 1.0 (위험 감소율)

    def calculate_reduced_ale(self, original_ale: float) -> float:
        """통제 적용 후 ALE 계산"""
        return original_ale * (1 - self.effectiveness)


class CostBenefitAnalyzer:
    """비용-효익 분석기"""

    def __init__(self, risk_analyzer: QuantitativeRiskAnalyzer):
        self.risk_analyzer = risk_analyzer
        self.controls: Dict[str, SecurityControl] = {}

    def add_control(self, control: SecurityControl):
        """보안 통제 등록"""
        self.controls[control.control_id] = control

    def analyze_control_roi(self, control_id: str) -> Dict:
        """개별 통제의 ROI 분석"""
        control = self.controls.get(control_id)
        if not control:
            return {}

        # 해당 통제가 영향을 미치는 위협들의 ALE 합계
        relevant_ale = 0
        for calc in self.risk_analyzer.calculations:
            if calc.threat_id in control.target_threat_ids:
                relevant_ale += calc.ale

        # 위험 감소액
        risk_reduction = relevant_ale * control.effectiveness

        # 순 혜택
        net_benefit = risk_reduction - control.annual_cost

        # ROI (%)
        roi = (net_benefit / control.annual_cost * 100) if control.annual_cost > 0 else 0

        return {
            'control_id': control_id,
            'control_name': control.name,
            'annual_cost': control.annual_cost,
            'relevant_ale': relevant_ale,
            'risk_reduction': risk_reduction,
            'net_benefit': net_benefit,
            'roi': roi,
            'cost_effective': net_benefit > 0
        }

    def analyze_all_controls(self) -> List[Dict]:
        """모든 통제의 ROI 분석"""
        results = []
        for control_id in self.controls:
            results.append(self.analyze_control_roi(control_id))
        return sorted(results, key=lambda x: x['roi'], reverse=True)

    def recommend_optimal_controls(self, budget: float) -> List[Dict]:
        """예산 내 최적 통제 조합 추천 (그리디 알고리즘)"""
        all_analysis = self.analyze_all_controls()

        # 비용 효율적인 통제만 필터링
        cost_effective = [a for a in all_analysis if a['cost_effective']]

        # ROI 순 정렬
        cost_effective.sort(key=lambda x: x['roi'], reverse=True)

        # 예산 내에서 선택
        selected = []
        remaining_budget = budget

        for analysis in cost_effective:
            if analysis['annual_cost'] <= remaining_budget:
                selected.append(analysis)
                remaining_budget -= analysis['annual_cost']

        return selected


# 사용 예시
if __name__ == "__main__":
    # 위험 분석기 생성
    analyzer = QuantitativeRiskAnalyzer()

    # 자산 등록
    analyzer.add_asset(Asset(
        asset_id="AS-001",
        name="고객 데이터베이스",
        category=AssetCategory.DATA,
        value=500_000_000,  # 5억원
        description="고객 개인정보 및 거래 데이터"
    ))

    analyzer.add_asset(Asset(
        asset_id="AS-002",
        name="ERP 시스템",
        category=AssetCategory.SOFTWARE,
        value=300_000_000,  # 3억원
        description="전사 자원 관리 시스템"
    ))

    analyzer.add_asset(Asset(
        asset_id="AS-003",
        name="웹 서버",
        category=AssetCategory.HARDWARE,
        value=100_000_000,  # 1억원
        description="외부 서비스 웹 서버"
    ))

    # 위협 등록
    analyzer.add_threat(Threat(
        threat_id="TH-001",
        name="랜섬웨어 감염",
        threat_type=ThreatType.RANSOMWARE,
        target_asset_id="AS-001",
        exposure_factor=0.8,  # 80% 손실
        annual_rate=0.2,  # 5년에 1회
        description="랜섬웨어로 인한 데이터 암호화"
    ))

    analyzer.add_threat(Threat(
        threat_id="TH-002",
        name="DDoS 공격",
        threat_type=ThreatType.DDOS,
        target_asset_id="AS-003",
        exposure_factor=0.3,  # 30% 손실 (업무 중단)
        annual_rate=2.0,  # 연 2회
        description="DDoS로 인한 서비스 중단"
    ))

    analyzer.add_threat(Threat(
        threat_id="TH-003",
        name="내부자 데이터 유출",
        threat_type=ThreatType.INSIDER,
        target_asset_id="AS-001",
        exposure_factor=1.0,  # 100% 손실 (완전 유출)
        annual_rate=0.33,  # 3년에 1회
        description="내부자에 의한 데이터 유출"
    ))

    # 위험 분석 수행
    calculations = analyzer.perform_analysis()

    print("=" * 60)
    print("정량적 위험 분석 결과")
    print("=" * 60)

    for calc in calculations:
        threat = analyzer.threats[calc.threat_id]
        asset = analyzer.assets[calc.asset_id]
        print(f"\n위협: {threat.name}")
        print(f"  대상 자산: {asset.name}")
        print(f"  자산 가치: {calc.asset_value:,.0f}원")
        print(f"  노출 계수(EF): {calc.exposure_factor:.0%}")
        print(f"  SLE (단일 손실): {calc.sle:,.0f}원")
        print(f"  ARO (연간 빈도): {calc.aro:.2f}회/년")
        print(f"  ALE (연간 손실): {calc.ale:,.0f}원")

    print("\n" + "=" * 60)
    print(f"총 연간 예상 손실액: {analyzer.get_total_ale():,.0f}원")
    print("=" * 60)

    # 비용-효익 분석
    cba = CostBenefitAnalyzer(analyzer)

    cba.add_control(SecurityControl(
        control_id="CTL-001",
        name="EDR 솔루션",
        annual_cost=30_000_000,  # 3천만원/년
        target_threat_ids=["TH-001"],
        effectiveness=0.7  # 70% 위험 감소
    ))

    cba.add_control(SecurityControl(
        control_id="CTL-002",
        name="DDoS 방어 서비스",
        annual_cost=20_000_000,  # 2천만원/년
        target_threat_ids=["TH-002"],
        effectiveness=0.8  # 80% 위험 감소
    ))

    cba.add_control(SecurityControl(
        control_id="CTL-003",
        name="DLP 솔루션",
        annual_cost=40_000_000,  # 4천만원/년
        target_threat_ids=["TH-003"],
        effectiveness=0.6  # 60% 위험 감소
    ))

    print("\n" + "=" * 60)
    print("보안 통제 ROI 분석")
    print("=" * 60)

    roi_results = cba.analyze_all_controls()
    for result in roi_results:
        print(f"\n통제: {result['control_name']}")
        print(f"  연간 비용: {result['annual_cost']:,.0f}원")
        print(f"  위험 감소액: {result['risk_reduction']:,.0f}원")
        print(f"  순 혜택: {result['net_benefit']:,.0f}원")
        print(f"  ROI: {result['roi']:.0f}%")
        print(f"  비용 효율적: {'예' if result['cost_effective'] else '아니오'}")

    # 예산 내 최적 조합 추천
    print("\n" + "=" * 60)
    print("예산 8천만원 내 최적 통제 조합")
    print("=" * 60)

    optimal = cba.recommend_optimal_controls(budget=80_000_000)
    total_cost = 0
    total_benefit = 0
    for rec in optimal:
        print(f"- {rec['control_name']}: 비용 {rec['annual_cost']:,.0f}원, ROI {rec['roi']:.0f}%")
        total_cost += rec['annual_cost']
        total_benefit += rec['net_benefit']

    print(f"\n총 비용: {total_cost:,.0f}원")
    print(f"총 순 혜택: {total_benefit:,.0f}원")
```

#### 5. 위험 분석 결과 해석 가이드

| ALE 대비 통제 비용 | 판단 | 권장 조치 |
|:---|:---|:---|
| 비용 < ALE × 0.5 | 강력 도입 권장 | 즉시 도입 검토 |
| 비용 = ALE × 0.5~1.0 | 도입 고려 | 상세 비용-효익 분석 |
| 비용 > ALE × 1.0~2.0 | 신중 검토 | 대안 통제 탐색 |
| 비용 > ALE × 2.0 | 비권장 | 위험 수용 또는 다른 대책 |

---

### III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 정량적 vs 정성적 위험 분석 비교

| 구분 | 정량적 (ALE/ARO/SLE) | 정성적 (Risk Matrix) |
|:---|:---|:---|
| **접근 방식** | 수치화, 금전적 가치 | 등급화, 상대적 평가 |
| **장점** | 객관적, ROI 계산 가능 | 단순, 빠른 적용 |
| **단점** | 데이터 수집 어려움 | 주관적, 비교 곤란 |
| **적용 분야** | 보안 예산 산정, 보험 | 초기 위험 스캔, 컴플라이언스 |
| **도구** | Excel, FAIR, RIMS RM | Risk Matrix, FMEA |
| **정확도** | ±30% 오차 범위 | 등급 간 격차 큼 |

#### 2. 산업별 ALE 사례 비교

| 산업 | 주요 위협 | 전형적 ALE | 통제 투자 비율 |
|:---|:---|:---|:---|
| **금융** | 내부자 유출, APT | 매출 0.5~1% | 50~70% |
| **제조** | 랜섬웨어, 스파이웨어 | 매출 0.2~0.5% | 30~50% |
| **의료** | 랜섬웨어, 데이터 유출 | 매출 0.3~0.8% | 40~60% |
| **유통** | DDoS, 결제 데이터 | 매출 0.1~0.3% | 20~40% |
| **공공** | APT, 데이터 유출 | 예산 0.5~1% | 40~60% |

#### 3. 과목 융합 관점 분석
- **보안 관리**: 위험 기반 보안 통제 우선순위 결정
- **비즈니스 연속성**: BIA(Business Impact Analysis)와 연계
- **컴플라이언스**: GDPR, CCPA 위반 벌금을 SLE에 반영
- **보험**: 사이버 보험료 산정의 기초 데이터
- **IT 예산**: 보안 투자 ROI 정당화

---

### IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 랜섬웨어 대응 투자 결정**
- 상황: 중견 제조기업, 랜섬웨어 ALE 8천만원 산출
- 통제 옵션: 백업 시스템(3천만원/년) vs EDR(5천만원/년)
- 판단: 백업 시스템 80% 효과 → ALE 1,600만원, ROI 167% → 백업 우선

**시나리오 2: 클라우드 보안 투자**
- 상황: 클라우드 마이그레이션, 데이터 유출 ALE 5억원
- 통제 옵션: CASB(1억원/년) vs DLP(8천만원/년)
- 판단: CASB 60%, DLP 40% 효과 → CASB 선택 (순혜택 2억)

**시나리오 3: 내부자 위협 대응**
- 상황: 핀테크, 내부자 유출 ALE 3억원
- 통제 옵션: UEBA(1.5억원/년) + PAM(8천만원/년)
- 판단: 복합 통제 85% 효과 → 순혜택 2.45억원 → 도입

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] 자산 가치 산정 방법론 표준화
- [ ] 과거 사고 데이터 수집 및 분석
- [ ] EF, ARO 추정의 근거 문서화
- [ ] 정기적 ALE 재산정 (연 1회 이상)
- [ ] 경영진 보고용 대시보드 구축
- [ ] 통제 효과성 측정 프로세스

#### 3. 안티패턴 (Anti-patterns)
- **과신(Optimism Bias)**: ARO를 너무 낮게 추정
- **최근성 효과(Recency Bias)**: 최근 사고에 과도한 가중치
- **분석 마비(Analysis Paralysis)**: 완벽한 데이터만 고집
- **숫자 맹신**: 정성적 요소(평판, 법적 리스크) 무시

---

### V. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | 내용 | 측정 방법 |
|:---|:---|:---|
| 보안 예산 최적화 | ALE 대비 20~30% 비용 절감 | 예산 대비 실제 손실 비교 |
| 투자 의사결정 객관화 | ROI 기반 통제 선택 | 프로젝트 승인율 향상 |
| 이해관계자 커뮤니케이션 | 경영진 이해 용이 | 보고서 이해도 조사 |
| 보험료 협상 | 데이터 기반 보험료 할인 | 보험료 인하율 |

#### 2. 미래 전망 및 진화 방향
- **AI/ML 기반 ARO 예측**: 과거 데이터 패턴 학습으로 정확도 향상
- **실시간 위험 계산**: 동적 자산 가치, 위협 인텔리전스 연동
- **FAIR 모델 확산**: Open FAIR 표준으로 상호 운용성 확보
- **사이버 보험 연동**: ALE 기반 보험료 산정 자동화

#### 3. 참고 표준/가이드
- **NIST SP 800-30**: 위험 분석 가이드
- **ISO/IEC 27005**: 정보보안 위험 관리
- **FAIR (Factor Analysis of Information Risk)**: 정량적 위험 모델
- **RIMS Risk Maturity Model**: 위험 관리 성숙도

---

### 관련 개념 맵 (Knowledge Graph)
- [위험 관리](@/studynotes/09_security/01_policy/risk_management.md) : ALE/ARO/SLE의 상위 개념
- [CIA 3요소](@/studynotes/09_security/01_policy/cia_triad.md) : 위험 분석의 보안 목표
- [심층 방어](@/studynotes/09_security/01_policy/defense_in_depth.md) : 다층 통제의 비용-효익
- [업무연속성 계획](@/studynotes/09_security/01_policy/dr_bcp.md) : BIA와 ALE 연계
- [보안 정책](@/studynotes/09_security/01_policy/security_policy.md) : 위험 기반 정책 수립

---

### 어린이를 위한 3줄 비유 설명
1. **사고 날 확률 계산**: "1년에 비가 10번 오고, 우산이 없으면 5천원짜리 옷이 젖는다" → 1년에 5만원 손해!
2. **돈으로 환산하기**: "가게에서 물건이 도난당할 확률과 손해액을 계산하면, 경비원을 고용할지 결정할 수 있어요."
3. **현명한 투자**: "1년에 5만원 손실 예상인데 1만원짜리 우산을 사면, 4만원을 아낄 수 있어요!"
