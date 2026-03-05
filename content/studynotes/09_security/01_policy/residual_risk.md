+++
title = "잔여 위험 (Residual Risk)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# 잔여 위험 (Residual Risk)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 보안 통제 적용 후에도 여전히 존재하는 위험으로, 고유 위험(Inherent Risk)에서 통제 효과를 차감한 후의 순위험입니다.
> 2. **가치**: 잔여 위험은 조직의 위험 식욕(Risk Appetite)과 비교하여 수용 가능 여부를 판단하는 의사결정의 핵심 기준입니다.
> 3. **융합**: ISO 27005, NIST RMF 등 모든 위험 관리 프레임워크에서 필수 개념으로, 보안 투자 ROI 측정의 기준점이 됩니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**잔여 위험(Residual Risk)**은 보안 통제(예방, 탐지, 교정)를 모두 적용한 후에도 잔존하는 위험 수준을 의미합니다. 이는 "완벽한 보안은 존재하지 않는다"는 전제에 기반합니다.

**위험의 종류 및 관계**:
```
┌─────────────────────────────────────────────────────────────────────┐
│                    위험(Risk)의 계층 구조                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │      고유 위험 (Inherent Risk / Gross Risk)                  │   │
│  │      ─────────────────────────────────────────               │   │
│  │      통제가 없을 때의 원초적 위험 수준                        │   │
│  │      공식: IR = 위협 × 취약점 × 자산가치                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                         │                                          │
│                         │ - 보안 통제 효과                          │
│                         ▼                                          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │      잔여 위험 (Residual Risk / Net Risk)                    │   │
│  │      ────────────────────────────────────────                │   │
│  │      통제 적용 후 남은 위험                                  │   │
│  │      공식: RR = IR × (1 - 통제효과성)                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                         │                                          │
│                         │ - 위험 수용                               │
│                         ▼                                          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │      목표 위험 (Target Risk)                                 │   │
│  │      ──────────────────────────                              │   │
│  │      조직이 수용하려는 위험 수준                              │   │
│  │      = 위험 식욕 (Risk Appetite)                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**핵심 공식**:
```
잔여 위험 (RR) = 고유 위험 (IR) × (1 - 통제 효과성)

또는 더 상세하게:

RR = IR - (IR × CE) + 제어 우회 위험 + 새로운 위험

여기서:
- IR = Inherent Risk (고유 위험)
- CE = Control Effectiveness (통제 효과성, 0~1)
- 제어 우회 위험 = 통제를 회피하는 새로운 공격 기법
- 새로운 위험 = 통제 도입으로 인해 발생하는 부차적 위험
```

#### 2. 비유를 통한 이해
잔여 위험은 **'자동차 안전벨트와 에어백'**에 비유할 수 있습니다.
- **고유 위험**: 안전 장치 없이 운전할 때 사망 위험 (높음)
- **보안 통제**: 안전벨트, 에어백, 차체 강화 (위험 감소)
- **잔여 위험**: 모든 안전 장치 후에도 남은 사망 위험 (0이 아님)
- **교훈**: 100% 안전은 불가능하지만, 위험을 수용 가능한 수준으로 낮출 수 있다

#### 3. 등장 배경 및 발전 과정
1. **1970년대**: 미국 국방부에서 위험 기반 접근 시작
2. **1990년대**: COSO ERM 프레임워크에서 정식 개념화
3. **2000년대**: ISO 27005, NIST SP 800-30에서 표준화
4. **2010년대**: APT, 제로데이 공격으로 잔여 위험 관리 중요성 대두
5. **현재**: Zero Trust, 지속적 위험 평가로 실시간 잔여 위험 모니터링

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 잔여 위험 계산 모델

```text
<<< 잔여 위험 산정 다이어그램 >>>

    ┌───────────────────────────────────────────────────────────────────────┐
    │                     고유 위험 (Inherent Risk)                         │
    │  ┌─────────────────────────────────────────────────────────────────┐ │
    │  │  위협 (Threat)          취약점 (Vulnerability)     자산 (Asset)  │ │
    │  │  ─────────────          ─────────────────────      ───────────  │ │
    │  │  - 랜섬웨어 공격자      - 패치 미적용              - 고객 DB    │ │
    │  │  - 내부자 위협          - 약한 비밀번호            - ERP 시스템 │ │
    │  │  - APT 그룹             - 권한 과다 부여           - 영업비밀   │ │
    │  │                                                                 │ │
    │  │  고유 위험 점수 = 위협확률 × 취약점정도 × 자산영향도             │ │
    │  │  예: 0.8 × 0.7 × 0.9 = 0.504 (50.4%)                            │ │
    │  └─────────────────────────────────────────────────────────────────┘ │
    └───────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
    ┌───────────────────────────────────────────────────────────────────────┐
    │                     보안 통제 적용 (Security Controls)                │
    │  ┌─────────────────────────────────────────────────────────────────┐ │
    │  │  예방 통제 (Preventive)      탐지 통제 (Detective)              │ │
    │  │  ────────────────────        ────────────────────               │ │
    │  │  - 방화벽, IPS               - SIEM, EDR                        │ │
    │  │  - 접근 통제                 - 로그 모니터링                    │ │
    │  │  - 암호화                    - IDS                              │ │
    │  │                                                                 │ │
    │  │  교정 통제 (Corrective)      복구 통제 (Recovery)               │ │
    │  │  ────────────────────        ────────────────────               │ │
    │  │  - 인시던트 대응             - 백업 복구                        │ │
    │  │  - 격리 조치                 - DRP                              │ │
    │  │  - 패치 적용                 - 보험                            │ │
    │  └─────────────────────────────────────────────────────────────────┘ │
    │                                                                       │
    │  통제 효과성 평가:                                                    │
    │  ┌─────────────────────────────────────────────────────────────────┐ │
    │  │  통제 유형        │ 적용 전 위험 │ 통제 효과성 │ 적용 후 위험   │ │
    │  │  ─────────────────────────────────────────────────────────────  │ │
    │  │  방화벽           │    50%       │    40%      │    30%         │ │
    │  │  EDR              │    30%       │    60%      │    12%         │ │
    │  │  백업             │    12%       │    50%      │     6%         │ │
    │  │  ─────────────────────────────────────────────────────────────  │ │
    │  │  잔여 위험        │              │             │     6%         │ │
    │  └─────────────────────────────────────────────────────────────────┘ │
    └───────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
    ┌───────────────────────────────────────────────────────────────────────┐
    │                     잔여 위험 평가 (Residual Risk Assessment)         │
    │  ┌─────────────────────────────────────────────────────────────────┐ │
    │  │                                                                 │ │
    │  │         잔여 위험 (6%)                                          │ │
    │  │            │                                                    │ │
    │  │            ▼                                                    │ │
    │  │  ┌─────────────────────────────────────────────────────────┐   │ │
    │  │  │  위험 식욕 (Risk Appetite) = 5%                          │   │ │
    │  │  └─────────────────────────────────────────────────────────┘   │ │
    │  │            │                                                    │ │
    │  │            ▼                                                    │ │
    │  │  ┌─────────────────────────────────────────────────────────┐   │ │
    │  │  │  잔여 위험(6%) > 위험 식욕(5%)                           │   │ │
    │  │  │  → 추가 통제 필요 OR 위험 수용 승인                      │   │ │
    │  │  └─────────────────────────────────────────────────────────┘   │ │
    │  │                                                                 │ │
    │  └─────────────────────────────────────────────────────────────────┘ │
    └───────────────────────────────────────────────────────────────────────┘
```

#### 2. 위험 식욭(Risk Appetite)과 잔여 위험 비교

| 위험 식욭 수준 | 정의 | 잔여 위험 기준 | 적용 조직 |
|:---|:---|:---|:---|
| **보수적 (Conservative)** | 위험 최소화 우선 | 잔여 위험 < 5% | 금융, 의료, 원자력 |
| **중간 (Moderate)** | 균형적 접근 | 잔여 위험 5~15% | 일반 기업, 공공기관 |
| **진취적 (Aggressive)** | 혁신 우선 | 잔여 위험 15~30% | 스타트업, 벤처 |
| **매우 진취적** | 높은 위험 감수 | 잔여 위험 > 30% | 일부 투자사, 도박업 |

#### 3. Python 구현: 잔여 위험 분석기

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import statistics

class RiskLevel(Enum):
    """위험 등급"""
    CRITICAL = "심각"
    HIGH = "높음"
    MEDIUM = "중간"
    LOW = "낮음"
    NEGLIGIBLE = "무시가능"

class ControlType(Enum):
    """통제 유형"""
    PREVENTIVE = "예방"
    DETECTIVE = "탐지"
    CORRECTIVE = "교정"
    RECOVERY = "복구"
    DETERRENT = "억제"

@dataclass
class Control:
    """보안 통제"""
    control_id: str
    name: str
    control_type: ControlType
    effectiveness: float  # 0.0 ~ 1.0
    annual_cost: float
    description: str = ""

@dataclass
class Risk:
    """위험 항목"""
    risk_id: str
    name: str
    threat: str
    vulnerability: str
    asset: str
    inherent_likelihood: float  # 0.0 ~ 1.0
    inherent_impact: float  # 0.0 ~ 1.0
    applied_controls: List[Control] = field(default_factory=list)

    @property
    def inherent_risk(self) -> float:
        """고유 위험 점수"""
        return self.inherent_likelihood * self.inherent_impact

    def calculate_residual_risk(self) -> Tuple[float, List[Control]]:
        """잔여 위험 계산"""
        if not self.applied_controls:
            return self.inherent_risk, []

        # 각 통제의 누적 효과 계산
        total_reduction = 0
        applied = []

        # 예방 통제 먼저 적용
        preventive = [c for c in self.applied_controls if c.control_type == ControlType.PREVENTIVE]
        for control in preventive:
            reduction = self.inherent_risk * control.effectiveness * (1 - total_reduction)
            total_reduction += reduction / self.inherent_risk if self.inherent_risk > 0 else 0
            applied.append(control)

        # 탐지 통제
        detective = [c for c in self.applied_controls if c.control_type == ControlType.DETECTIVE]
        for control in detective:
            reduction = self.inherent_risk * control.effectiveness * (1 - total_reduction)
            total_reduction += reduction / self.inherent_risk if self.inherent_risk > 0 else 0
            applied.append(control)

        # 교정 통제
        corrective = [c for c in self.applied_controls if c.control_type == ControlType.CORRECTIVE]
        for control in corrective:
            reduction = self.inherent_risk * control.effectiveness * (1 - total_reduction)
            total_reduction += reduction / self.inherent_risk if self.inherent_risk > 0 else 0
            applied.append(control)

        # 복구 통제
        recovery = [c for c in self.applied_controls if c.control_type == ControlType.RECOVERY]
        for control in recovery:
            reduction = self.inherent_risk * control.effectiveness * (1 - total_reduction)
            total_reduction += reduction / self.inherent_risk if self.inherent_risk > 0 else 0
            applied.append(control)

        residual = self.inherent_risk * max(0, 1 - total_reduction)
        return residual, applied

    def get_risk_level(self, risk_score: float) -> RiskLevel:
        """위험 등급 판정"""
        if risk_score >= 0.7:
            return RiskLevel.CRITICAL
        elif risk_score >= 0.5:
            return RiskLevel.HIGH
        elif risk_score >= 0.3:
            return RiskLevel.MEDIUM
        elif risk_score >= 0.1:
            return RiskLevel.LOW
        else:
            return RiskLevel.NEGLIGIBLE

@dataclass
class RiskAppetite:
    """위험 식욭 정의"""
    category: str
    max_acceptable_risk: float  # 0.0 ~ 1.0
    description: str

    def is_acceptable(self, residual_risk: float) -> bool:
        """잔여 위험 수용 가능 여부"""
        return residual_risk <= self.max_acceptable_risk


class ResidualRiskAnalyzer:
    """잔여 위험 분석기"""

    def __init__(self):
        self.risks: Dict[str, Risk] = {}
        self.risk_appetites: Dict[str, RiskAppetite] = {}
        self.available_controls: Dict[str, Control] = {}

    def add_risk(self, risk: Risk):
        """위험 등록"""
        self.risks[risk.risk_id] = risk

    def add_control(self, control: Control):
        """통제 등록"""
        self.available_controls[control.control_id] = control

    def set_risk_appetite(self, appetite: RiskAppetite):
        """위험 식욭 설정"""
        self.risk_appetites[appetite.category] = appetite

    def apply_control_to_risk(self, risk_id: str, control_id: str):
        """위험에 통제 적용"""
        risk = self.risks.get(risk_id)
        control = self.available_controls.get(control_id)
        if risk and control:
            risk.applied_controls.append(control)

    def analyze_all_risks(self) -> List[Dict]:
        """전체 위험 분석"""
        results = []
        for risk in self.risks.values():
            residual, controls = risk.calculate_residual_risk()
            results.append({
                'risk_id': risk.risk_id,
                'name': risk.name,
                'inherent_risk': risk.inherent_risk,
                'inherent_level': risk.get_risk_level(risk.inherent_risk).value,
                'residual_risk': residual,
                'residual_level': risk.get_risk_level(residual).value,
                'risk_reduction': risk.inherent_risk - residual,
                'reduction_percent': (risk.inherent_risk - residual) / risk.inherent_risk * 100 if risk.inherent_risk > 0 else 0,
                'applied_controls': [c.name for c in controls]
            })
        return results

    def check_risk_acceptance(self, category: str = "default") -> List[Dict]:
        """위험 수용 여부 검사"""
        appetite = self.risk_appetites.get(category, RiskAppetite("default", 0.2, "기본 위험 식욭"))
        results = []

        for risk in self.risks.values():
            residual, _ = risk.calculate_residual_risk()
            is_acceptable = appetite.is_acceptable(residual)

            results.append({
                'risk_id': risk.risk_id,
                'name': risk.name,
                'residual_risk': residual,
                'risk_appetite': appetite.max_acceptable_risk,
                'is_acceptable': is_acceptable,
                'action_required': "수용 가능" if is_acceptable else "추가 통제 필요"
            })

        return results

    def calculate_total_residual_risk(self) -> float:
        """전체 잔여 위험 계산"""
        total = 0
        for risk in self.risks.values():
            residual, _ = risk.calculate_residual_risk()
            total += residual
        return total / len(self.risks) if self.risks else 0

    def recommend_additional_controls(self, max_budget: float) -> List[Dict]:
        """추가 통제 추천"""
        # 수용 불가능한 위험 식별
        unacceptable = []
        for risk in self.risks.values():
            residual, _ = risk.calculate_residual_risk()
            if residual > 0.2:  # 기준 초과
                unacceptable.append(risk)

        # 비용 효율적인 통제 추천
        recommendations = []
        for risk in unacceptable:
            for control in self.available_controls.values():
                if control not in risk.applied_controls:
                    if control.annual_cost <= max_budget:
                        # 잠재적 위험 감소량
                        potential_reduction = residual * control.effectiveness
                        cost_effectiveness = potential_reduction / control.annual_cost

                        recommendations.append({
                            'risk_id': risk.risk_id,
                            'risk_name': risk.name,
                            'control_id': control.control_id,
                            'control_name': control.name,
                            'cost': control.annual_cost,
                            'potential_reduction': potential_reduction,
                            'cost_effectiveness': cost_effectiveness
                        })

        # 비용 효율성 순 정렬
        recommendations.sort(key=lambda x: x['cost_effectiveness'], reverse=True)
        return recommendations


# 사용 예시
if __name__ == "__main__":
    # 분석기 생성
    analyzer = ResidualRiskAnalyzer()

    # 위험 식욭 설정
    analyzer.set_risk_appetite(RiskAppetite(
        category="default",
        max_acceptable_risk=0.2,
        description="일반적인 위험 식욭 - 20% 이하만 수용"
    ))

    # 위험 등록
    analyzer.add_risk(Risk(
        risk_id="R-001",
        name="랜섬웨어 감염",
        threat="랜섬웨어 공격자",
        vulnerability="패치 미적용",
        asset="고객 데이터베이스",
        inherent_likelihood=0.7,
        inherent_impact=0.9
    ))

    analyzer.add_risk(Risk(
        risk_id="R-002",
        name="DDoS 공격",
        threat="해커 그룹",
        vulnerability="트래픽 증폭 취약점",
        asset="웹 서비스",
        inherent_likelihood=0.8,
        inherent_impact=0.5
    ))

    analyzer.add_risk(Risk(
        risk_id="R-003",
        name="내부자 데이터 유출",
        threat="악의적 내부자",
        vulnerability="과도한 권한",
        asset="영업비밀",
        inherent_likelihood=0.3,
        inherent_impact=0.95
    ))

    # 통제 등록
    analyzer.add_control(Control(
        control_id="C-001",
        name="차세대 방화벽(NGFW)",
        control_type=ControlType.PREVENTIVE,
        effectiveness=0.4,
        annual_cost=50_000_000
    ))

    analyzer.add_control(Control(
        control_id="C-002",
        name="EDR 솔루션",
        control_type=ControlType.DETECTIVE,
        effectiveness=0.6,
        annual_cost=30_000_000
    ))

    analyzer.add_control(Control(
        control_id="C-003",
        name="DDoS 방어 서비스",
        control_type=ControlType.PREVENTIVE,
        effectiveness=0.7,
        annual_cost=20_000_000
    ))

    analyzer.add_control(Control(
        control_id="C-004",
        name="백업 시스템",
        control_type=ControlType.RECOVERY,
        effectiveness=0.8,
        annual_cost=15_000_000
    ))

    analyzer.add_control(Control(
        control_id="C-005",
        name="DLP 솔루션",
        control_type=ControlType.PREVENTIVE,
        effectiveness=0.5,
        annual_cost=40_000_000
    ))

    # 통제 적용
    analyzer.apply_control_to_risk("R-001", "C-001")  # 랜섬웨어에 방화벽
    analyzer.apply_control_to_risk("R-001", "C-002")  # 랜섬웨어에 EDR
    analyzer.apply_control_to_risk("R-001", "C-004")  # 랜섬웨어에 백업
    analyzer.apply_control_to_risk("R-002", "C-003")  # DDoS에 DDoS 방어
    analyzer.apply_control_to_risk("R-003", "C-005")  # 내부자에 DLP

    # 분석 수행
    print("=" * 70)
    print("잔여 위험 분석 결과")
    print("=" * 70)

    results = analyzer.analyze_all_risks()
    for r in results:
        print(f"\n위험: {r['name']}")
        print(f"  고유 위험: {r['inherent_risk']:.2%} ({r['inherent_level']})")
        print(f"  잔여 위험: {r['residual_risk']:.2%} ({r['residual_level']})")
        print(f"  위험 감소: {r['reduction_percent']:.1f}%")
        print(f"  적용 통제: {', '.join(r['applied_controls'])}")

    # 위험 수용 검사
    print("\n" + "=" * 70)
    print("위험 수용 여부 검사")
    print("=" * 70)

    acceptance = analyzer.check_risk_acceptance()
    for a in acceptance:
        status = "✓ 수용 가능" if a['is_acceptable'] else "✗ 추가 통제 필요"
        print(f"{a['name']}: 잔여위험 {a['residual_risk']:.2%} vs 식욭 {a['risk_appetite']:.2%} → {status}")

    # 추가 통제 추천
    print("\n" + "=" * 70)
    print("추가 통제 추천 (예산 5천만원)")
    print("=" * 70)

    recommendations = analyzer.recommend_additional_controls(max_budget=50_000_000)
    for rec in recommendations[:5]:  # 상위 5개
        print(f"\n{rec['risk_name']} → {rec['control_name']}")
        print(f"  비용: {rec['cost']:,}원/년")
        print(f"  예상 위험 감소: {rec['potential_reduction']:.2%}")
        print(f"  비용 효율성: {rec['cost_effectiveness']:.4f}")
```

#### 4. 통제 효과성 평가 기준

| 통제 유형 | 효과성 범위 | 측정 방법 | 예시 |
|:---|:---|:---|:---|
| **예방 통제** | 30~70% | 사고 예방률 | 방화벽: 40%, 암호화: 60% |
| **탐지 통제** | 40~80% | 탐지율(Recall) | SIEM: 60%, EDR: 75% |
| **교정 통제** | 50~90% | 복구 성공률 | IR 프로세스: 70% |
| **복구 통제** | 60~95% | RTO/RPO 달성률 | 백업: 80%, DRP: 90% |

---

### III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 위험 관리 프레임워크별 잔여 위험 처리

| 프레임워크 | 잔여 위험 정의 | 처리 방식 | 승인 권한 |
|:---|:---|:---|:---|
| **ISO 27005** | 통제 후 남은 위험 | 수용/전가/추가통제 | 경영진 |
| **NIST RMF** | 허용 위험 대비 과잉/부족 | Authorize/Deny | Authorizing Official |
| **COBIT** | IT 위험의 잔존분 | Risk Profile 관리 | 이사회 |
| **FAIR** | Loss Exposure의 순값 | 최적화 분석 | CRO |

#### 2. 산업별 잔여 위험 수용 기준

| 산업 | 일반적 위험 식욭 | 주요 규제 | 잔여 위험 관리 |
|:---|:---|:---|:---|
| **금융** | 보수적 (~5%) | Basel III, DLP | 사이버 보험, 자본 적립 |
| **의료** | 중간 (~10%) | HIPAA, GDPR | 환자 안전 최우선 |
| **제조** | 중간 (~15%) | IEC 62443 | 생산 중단 최소화 |
| **공공** | 보수적 (~5%) | FISMA, FedRAMP | 국가 안보 고려 |
| **유통** | 진취적 (~20%) | PCI DSS | 비용 효율성 중시 |

#### 3. 과목 융합 관점 분석
- **위험 관리**: 잔여 위험은 위험 관리 프로세스의 핵심 산출물
- **컴플라이언스**: 규제 요건 충족 여부 판단의 기준
- **보안 예산**: 잔여 위험 감소 대비 투자 효율성 분석
- **보험**: 사이버 보험 가입 시 잔여 위험 평가 필요
- **감사**: 잔여 위험 수용 승인 프로세스 감사

---

### IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 클라우드 마이그레이션 잔여 위험**
- 상황: 온프레미스 → 클라우드 전환, 고유 위험 60%
- 통제: CSPM, CWPP, IAM 강화 → 통제 효과성 70%
- 잔여 위험: 60% × 30% = 18%
- 판단: 위험 식욕 20% 대비 수용 가능, 단 모니터링 강화

**시나리오 2: APT 대응 잔여 위험**
- 상황: APT 공격 위험 40%, Zero-Day 취약점 존재
- 통제: EDR, 위협 헌팅, 네트워크 분리 → 효과성 80%
- 잔여 위험: 40% × 20% = 8%
- 판단: Zero-Day는 예방 불가 → 탐지/대응 중심으로 전환

**시나리오 3: 공급망 공격 잔여 위험**
- 상황: SW 공급망 공격 위험 35%, SBOM 미확보
- 통제: 공급업체 보안 평가, 코드 서명 검증 → 효과성 50%
- 잔여 위험: 35% × 50% = 17.5%
- 판단: 위험 식욕 초과 → SBOM 도입, SCA 도구 추가 필요

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] 조직의 위험 식욭(Risk Appetite) 명확화
- [ ] 고유 위험 정확한 산정
- [ ] 통제 효과성 객관적 평가
- [ ] 잔여 위험 수용 승인 프로세스 정립
- [ ] 정기적 잔여 위험 재평가 (분기별)
- [ ] 상위 위험 잔여 위험 보고 체계

#### 3. 안티패턴 (Anti-patterns)
- **잔여 위험 무시**: "통제 다 했으니 안전하다" → False Security
- **과도한 통제**: 잔여 위험 0% 추구 → 비용 낭비
- **일회성 평가**: 최초 1회만 평가 → 환경 변화 미반영
- **주관적 판단**: 데이터 없이 "괜찮을 것" → 근거 부족

---

### V. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | 내용 | 측정 지표 |
|:---|:---|:---|
| 보안 투자 최적화 | 필요 이상 통제 방지 | 비용 대비 위험 감소율 |
| 의사결정 객관화 | 데이터 기반 위험 수용 | 승인 프로세스 일관성 |
| 규제 준수 | 위험 기반 통제 입증 | 감사 지적 감소 |
| 이해관계자 신뢰 | 투명한 위험 관리 | 경영진 신뢰도 |

#### 2. 미래 전망 및 진화 방향
- **실시간 잔여 위험**: 지속적 위험 평가(CRP)로 실시간 모니터링
- **AI 기반 예측**: ML로 잔여 위험 변화 예측
- **동적 위험 식욭**: 비즈니스 상황에 따른 위험 식욭 자동 조정
- **통합 위험 플랫폼**: GRC(Governance, Risk, Compliance) 통합 관리

#### 3. 참고 표준/가이드
- **ISO/IEC 27005**: 정보보안 위험 관리 - 잔여 위험 처리
- **NIST SP 800-37**: RMF - 위험 허용 결정
- **ISO 31000**: 위험 관리 - 위험 평가 프로세스
- **COSO ERM**: 전사적 위험 관리 - 위험 식욭 프레임워크

---

### 관련 개념 맵 (Knowledge Graph)
- [위험 관리](@/studynotes/09_security/01_policy/risk_management.md) : 잔여 위험의 상위 개념
- [ALE/ARO/SLE](@/studynotes/09_security/01_policy/ale_aro_sle.md) : 정량적 위험 분석 도구
- [심층 방어](@/studynotes/09_security/01_policy/defense_in_depth.md) : 다층 통제로 잔여 위험 최소화
- [보안 정책](@/studynotes/09_security/01_policy/security_policy.md) : 위험 식욭 정의
- [인시던트 대응](@/studynotes/09_security/01_policy/dr_bcp.md) : 잔여 위험 발현 시 대응

---

### 어린이를 위한 3줄 비유 설명
1. **남은 위험**: 비가 올 때 우산을 써도 신발은 젖을 수 있어요. 우산(통제)을 썼는데도 남는 젖을 확률이 잔여 위험이에요.
2. **완벽은 없다**: 모든 문에 자물쇠를 달아도 창문을 통해 들어올 수 있죠? 100% 안전은 불가능해요.
3. **수용하기**: "신발이 좀 젖을 수는 있지만 괜찮아"라고 생각하는 것처럼, 남은 위험을 받아들이는 거예요.
