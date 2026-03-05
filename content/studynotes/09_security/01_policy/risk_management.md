+++
title = "위험 관리 (Risk Management)"
date = "2026-03-04"
[extra]
categories = "studynotes-09_security"
+++

# 위험 관리 (Risk Management)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 조직의 정보자산에 대한 위험을 체계적으로 식별, 분석, 평가, 대응, 모니터링하는 지속적 프로세스로, 비즈니스 목표와 보안 투자의 균형을 도모합니다.
> 2. **가치**: 보안 예산의 효율적 배분, 의사결정 지원, 컴플라이언스 충족, 비즈니스 연속성 보장을 실현합니다.
> 3. **융합**: 정량적/정성적 분석, ALE/ARO/SLE 계산, ISO 27005, NIST RMF 등이 결합된 체계적 접근법입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**위험 관리(Risk Management)**는 조직이 목표를 달성하는 데 있어 불확실성이 미치는 영향을 관리하는 체계적 프로세스입니다. 정보보안 관점에서는 정보자산에 대한 위협, 취약점, 영향을 분석하여 적절한 통제를 적용하는 활동입니다.

**ISO 31000 정의**:
> "조직이 목표를 달성하는 데 있어 불확실성이 미치는 영향을 관리하기 위한 지침"

**위험의 공식**:
```
Risk = Threat × Vulnerability × Impact
위험 = 위협 × 취약점 × 영향도
```

**위험 관리 수명주기**:
1. **식별 (Identification)**: 자산, 위협, 취약점 파악
2. **분석 (Analysis)**: 발생 가능성과 영향 평가
3. **평가 (Evaluation)**: 위험 우선순위 결정
4. **대응 (Treatment)**: 위험 감소, 전가, 회피, 수용
5. **모니터링 (Monitoring)**: 지속적 검토 및 개선

#### 2. 💡 비유를 통한 이해
위험 관리는 **'보험 설계'**에 비유할 수 있습니다.
- **자산 식별**: 보험 대상 파악 (집, 자동차, 건강)
- **위험 분석**: 발생 확률과 손실 규모 계산
- **위험 대응**: 보험 가입(전가), 안전장치 설치(감소)
- **보험료**: 보안 투자 비용
- **자기부담**: 잔여 위험 수용

#### 3. 등장 배경 및 발전 과정
1. **전통적 위험 관리**: 재무, 보험 중심 (1960~70년대)
2. **정보보안 위험 관리**: 컴퓨터 보안 등장 (1980년대)
3. **표준화**: ISO 27001/27005, NIST SP 800-30 (1990~2000년대)
4. **엔터프라이즈 위험 관리 (ERM)**: 전사적 통합 관리 (2000년대)
5. **사이버 위험 관리**: 클라우드, AI 등 신기술 대응 (2010년대~)

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 위험 관리 프로세스 체계 (표)

| 단계 | 활동 | 산출물 | 도구/기법 |
|:---|:---|:---|:---|
| **자산 식별** | 하드웨어, 소프트웨어, 데이터, 인력 | 자산 목록, 자산 가치표 | 자산 관리 도구, CMDB |
| **위협 식별** | 내부/외부 위협원 파악 | 위협 목록, 위협 시나리오 | 위협 모델링, MITRE ATT&CK |
| **취약점 식별** | 기술/관리적 약점 파악 | 취약점 목록, CVSS 점수 | 취약점 스캐너, Pentest |
| **위험 분석** | 가능성×영향 계산 | 위험 점수, 위험 매트릭스 | 정량/정성 분석 |
| **위험 평가** | 우선순위 결정 | 위험 등록부, 위험 프로필 | 위험 기준 비교 |
| **위험 대응** | 통제 적용 | 통제 계획, 예산 | 방어 기술, 보험 |
| **모니터링** | 지속적 검토 | 위험 대시보드, KRI | SIEM, GRC 플랫폼 |

#### 2. 위험 관리 아키텍처 다이어그램

```text
<<< Risk Management Framework Architecture >>>

    +----------------------------------------------------------+
    |                 위험 관리 거버넌스 (Governance)            |
    |  +----------------------------------------------------+  |
    |  |  Board → CISO → Risk Committee → Business Units    |  |
    |  |  위험 정책, 위험 식욕(Risk Appetite), 승인          |  |
    |  +----------------------------------------------------+  |
    +----------------------------------------------------------+
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        v                       v                       v
    +-----------+         +-----------+         +-----------+
    │ 위험 식별 │         │ 위험 분석 │         │ 위험 평가 │
    │           │         │           │         │           │
    │ - 자산    │ ───────► │ - 가능성  │ ───────► │ - 우선순위│
    │ - 위협    │         │ - 영향도  │         │ - 등급화  │
    │ - 취약점  │         │ - 위험도  │         │ - 비교    │
    +-----------+         +-----------+         +-----------+
                                                    │
                                                    v
    +----------------------------------------------------------+
    |                 위험 대응 전략 (Risk Treatment)            |
    |  +----------------------------------------------------+  |
    |  |  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ |  |
    |  |  │  회피    │ │  감소    │ │  전가    │ │  수용  │ |  |
    |  |  │(Avoid)   │ │(Mitigate)│ │(Transfer)│ │(Accept)│ |  |
    |  |  └──────────┘ └──────────┘ └──────────┘ └────────┘ |  |
    |  +----------------------------------------------------+  |
    +----------------------------------------------------------+
                                │
                                v
    +----------------------------------------------------------+
    |                 위험 모니터링 (Monitoring)                 |
    |  +----------------------------------------------------+  |
    |  |  KRI (Key Risk Indicators)                        |  |
    |  |  ┌──────────────────────────────────────────────┐ |  |
    |  |  │ 위험 대시보드                                  │ |  |
    |  |  │ - 위험 추세 그래프                            │ |  |
    |  |  │ - 위험 임계치 알림                            │ |  |
    |  |  │ - 통제 효과성 측정                            │ |  |
    |  |  └──────────────────────────────────────────────┘ |  |
    |  +----------------------------------------------------+  |
    +----------------------------------------------------------+

<<< 위험 매트릭스 (Risk Matrix) >>>

    영향도 (Impact)
    ↑
    │  ┌─────┬─────┬─────┬─────┬─────┐
    │  │ M   │ H   │ H   │ C   │ C   │  C = Critical (위험)
    │  ├─────┼─────┼─────┼─────┼─────┤
    │  │ L   │ M   │ H   │ H   │ C   │  H = High (높음)
    │  ├─────┼─────┼─────┼─────┼─────┤
    │  │ L   │ M   │ M   │ H   │ H   │  M = Medium (중간)
    │  ├─────┼─────┼─────┼─────┼─────┤
    │  │ N   │ L   │ M   │ M   │ H   │  L = Low (낮음)
    │  ├─────┼─────┼─────┼─────┼─────┤
    │  │ N   │ N   │ L   │ L   │ M   │  N = Negligible (무시)
    │  └─────┴─────┴─────┴─────┴─────┘
    └───────────────────────────────────────→ 발생 가능성 (Likelihood)
          매우   낮음   중간   높음   매우
          낮음                       높음
```

#### 3. 심층 동작 원리: 위험 분석 및 계산

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime
import json

class RiskLevel(Enum):
    NEGLIGIBLE = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5

class AssetType(Enum):
    HARDWARE = "hardware"
    SOFTWARE = "software"
    DATA = "data"
    PERSONNEL = "personnel"
    SERVICE = "service"

class ThreatCategory(Enum):
    CYBER_ATTACK = "cyber_attack"
    NATURAL_DISASTER = "natural_disaster"
    HUMAN_ERROR = "human_error"
    INSIDER_THREAT = "insider_threat"
    SUPPLY_CHAIN = "supply_chain"
    SYSTEM_FAILURE = "system_failure"

@dataclass
class Asset:
    """정보 자산"""
    id: str
    name: str
    type: AssetType
    owner: str
    value: float  # 자산 가치 (원)
    criticality: int  # 1-5 (중요도)
    description: str = ""

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type.value,
            'owner': self.owner,
            'value': self.value,
            'criticality': self.criticality
        }

@dataclass
class Threat:
    """위협"""
    id: str
    name: str
    category: ThreatCategory
    description: str
    likelihood_base: float  # 0.0 ~ 1.0 (기본 발생 확률)

@dataclass
class Vulnerability:
    """취약점"""
    id: str
    name: str
    description: str
    cvss_score: float  # 0.0 ~ 10.0
    affected_asset_id: str
    exploitability: float  # 0.0 ~ 1.0

@dataclass
class Risk:
    """위험"""
    id: str
    asset: Asset
    threat: Threat
    vulnerability: Vulnerability

    # 분석 결과
    likelihood: float  # 0.0 ~ 1.0
    impact: float  # 금액 (원)
    risk_score: float  # 위험 점수
    risk_level: RiskLevel

    # 대응
    treatment: str = ""  # avoid, mitigate, transfer, accept
    residual_risk: float = 0.0
    controls: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'asset': self.asset.name,
            'threat': self.threat.name,
            'vulnerability': self.vulnerability.name,
            'likelihood': self.likelihood,
            'impact': self.impact,
            'risk_score': self.risk_score,
            'risk_level': self.risk_level.name,
            'treatment': self.treatment,
            'residual_risk': self.residual_risk
        }

class QuantitativeRiskAnalyzer:
    """
    정량적 위험 분석
    - ALE (Annual Loss Expectancy)
    - ARO (Annual Rate of Occurrence)
    - SLE (Single Loss Expectancy)
    """

    @staticmethod
    def calculate_sle(asset_value: float, exposure_factor: float) -> float:
        """
        단일 손실 기대값 (SLE)
        SLE = 자산 가치 × 노출 계수

        Args:
            asset_value: 자산 가치 (원)
            exposure_factor: 손실 비율 (0.0 ~ 1.0)
        """
        return asset_value * exposure_factor

    @staticmethod
    def calculate_ale(sle: float, aro: float) -> float:
        """
        연간 손실 기대값 (ALE)
        ALE = SLE × ARO

        Args:
            sle: 단일 손실 기대값
            aro: 연간 발생률 (회/년)
        """
        return sle * aro

    @staticmethod
    def calculate_risk_reduction_ale(
        current_ale: float,
        control_cost: float,
        control_effectiveness: float,
        aro: float
    ) -> Tuple[float, float]:
        """
        통제 적용 후 ALE 및 비용 효과 계산

        Returns:
            (새로운 ALE, 비용 절감)
        """
        new_aro = aro * (1 - control_effectiveness)
        new_ale = (current_ale / aro) * new_aro

        # 연간 비용 절감
        annual_savings = current_ale - new_ale - control_cost

        return new_ale, annual_savings

    @staticmethod
    def calculate_roi(
        annual_savings: float,
        control_cost: float
    ) -> float:
        """
        투자 대비 효과 (ROI)
        ROI = (연간 절감액 - 통제 비용) / 통제 비용 × 100
        """
        if control_cost == 0:
            return float('inf')
        return ((annual_savings - control_cost) / control_cost) * 100

class RiskMatrix:
    """
    위험 매트릭스 분석
    - 가능성 × 영향도 매핑
    - 위험 등급 결정
    """

    def __init__(self):
        # 5x5 위험 매트릭스 정의
        self.matrix = {
            # (가능성 등급, 영향도 등급) → 위험 등급
            (1, 1): RiskLevel.NEGLIGIBLE, (1, 2): RiskLevel.NEGLIGIBLE,
            (1, 3): RiskLevel.LOW, (1, 4): RiskLevel.LOW, (1, 5): RiskLevel.MEDIUM,
            (2, 1): RiskLevel.NEGLIGIBLE, (2, 2): RiskLevel.LOW,
            (2, 3): RiskLevel.LOW, (2, 4): RiskLevel.MEDIUM, (2, 5): RiskLevel.MEDIUM,
            (3, 1): RiskLevel.LOW, (3, 2): RiskLevel.LOW,
            (3, 3): RiskLevel.MEDIUM, (3, 4): RiskLevel.MEDIUM, (3, 5): RiskLevel.HIGH,
            (4, 1): RiskLevel.LOW, (4, 2): RiskLevel.MEDIUM,
            (4, 3): RiskLevel.MEDIUM, (4, 4): RiskLevel.HIGH, (4, 5): RiskLevel.HIGH,
            (5, 1): RiskLevel.MEDIUM, (5, 2): RiskLevel.MEDIUM,
            (5, 3): RiskLevel.HIGH, (5, 4): RiskLevel.HIGH, (5, 5): RiskLevel.CRITICAL,
        }

        # 위험 레벨별 임계값
        self.thresholds = {
            RiskLevel.NEGLIGIBLE: 5,
            RiskLevel.LOW: 10,
            RiskLevel.MEDIUM: 20,
            RiskLevel.HIGH: 30,
            RiskLevel.CRITICAL: 50
        }

    def get_risk_level(self, likelihood_grade: int, impact_grade: int) -> RiskLevel:
        """위험 등급 조회"""
        key = (likelihood_grade, impact_grade)
        return self.matrix.get(key, RiskLevel.MEDIUM)

    def likelihood_to_grade(self, likelihood: float) -> int:
        """가능성 (0-1)을 등급 (1-5)으로 변환"""
        if likelihood < 0.1:
            return 1
        elif likelihood < 0.3:
            return 2
        elif likelihood < 0.5:
            return 3
        elif likelihood < 0.7:
            return 4
        else:
            return 5

    def impact_to_grade(self, impact: float, asset_value: float) -> int:
        """영향도 (원)를 등급 (1-5)으로 변환"""
        ratio = impact / asset_value if asset_value > 0 else 0

        if ratio < 0.05:
            return 1
        elif ratio < 0.15:
            return 2
        elif ratio < 0.30:
            return 3
        elif ratio < 0.50:
            return 4
        else:
            return 5

class RiskManagementSystem:
    """
    통합 위험 관리 시스템
    """

    def __init__(self):
        self.assets: Dict[str, Asset] = {}
        self.threats: Dict[str, Threat] = {}
        self.vulnerabilities: Dict[str, Vulnerability] = {}
        self.risks: Dict[str, Risk] = {}
        self.risk_matrix = RiskMatrix()
        self.quantitative_analyzer = QuantitativeRiskAnalyzer()

        # 위험 식욭 (Risk Appetite)
        self.risk_appetite = {
            RiskLevel.NEGLIGIBLE: "수용",
            RiskLevel.LOW: "수용",
            RiskLevel.MEDIUM: "모니터링",
            RiskLevel.HIGH: "대응 필요",
            RiskLevel.CRITICAL: "즉시 대응"
        }

    def register_asset(self, asset: Asset):
        """자산 등록"""
        self.assets[asset.id] = asset

    def register_threat(self, threat: Threat):
        """위협 등록"""
        self.threats[threat.id] = threat

    def register_vulnerability(self, vuln: Vulnerability):
        """취약점 등록"""
        self.vulnerabilities[vuln.id] = vuln

    def identify_risk(self,
                      asset_id: str,
                      threat_id: str,
                      vuln_id: str) -> Risk:
        """위험 식별 및 분석"""
        asset = self.assets[asset_id]
        threat = self.threats[threat_id]
        vuln = self.vulnerabilities[vuln_id]

        # 가능성 계산 (위협 기본 확률 × 취약점 악용 가능성)
        likelihood = threat.likelihood_base * vuln.exploitability
        likelihood = min(likelihood, 1.0)

        # 영향도 계산 (자산 가치 × 노출 계수)
        exposure_factor = vuln.cvss_score / 10.0
        impact = asset.value * exposure_factor

        # 위험 점수 및 등급 계산
        likelihood_grade = self.risk_matrix.likelihood_to_grade(likelihood)
        impact_grade = self.risk_matrix.impact_to_grade(impact, asset.value)
        risk_level = self.risk_matrix.get_risk_level(likelihood_grade, impact_grade)

        risk_score = likelihood_grade * impact_grade

        risk = Risk(
            id=f"RISK-{asset_id[:4]}-{threat_id[:4]}",
            asset=asset,
            threat=threat,
            vulnerability=vuln,
            likelihood=likelihood,
            impact=impact,
            risk_score=risk_score,
            risk_level=risk_level
        )

        self.risks[risk.id] = risk
        return risk

    def analyze_quantitative(self,
                            risk: Risk,
                            aro: float) -> Dict:
        """
        정량적 위험 분석

        Args:
            risk: 위험 객체
            aro: 연간 발생률
        """
        sle = self.quantitative_analyzer.calculate_sle(
            risk.impact,
            1.0  # 전체 손실 가정
        )

        ale = self.quantitative_analyzer.calculate_ale(sle, aro)

        return {
            'sle': sle,
            'aro': aro,
            'ale': ale,
            'annual_cost': ale
        }

    def evaluate_treatment(self,
                          risk: Risk,
                          control_cost: float,
                          control_effectiveness: float,
                          aro: float) -> Dict:
        """
        위험 대응 평가

        Args:
            risk: 위험 객체
            control_cost: 통제 비용 (연간)
            control_effectiveness: 통제 효과성 (0-1)
            aro: 연간 발생률
        """
        current_ale = risk.impact * aro

        new_ale, annual_savings = self.quantitative_analyzer.calculate_risk_reduction_ale(
            current_ale,
            control_cost,
            control_effectiveness,
            aro
        )

        roi = self.quantitative_analyzer.calculate_roi(annual_savings, control_cost)

        # 잔여 위험
        residual_risk = new_ale

        # 비용 효과적 여부
        cost_effective = annual_savings > 0 or roi > 0

        return {
            'current_ale': current_ale,
            'new_ale': new_ale,
            'control_cost': control_cost,
            'annual_savings': annual_savings,
            'roi': roi,
            'residual_risk': residual_risk,
            'cost_effective': cost_effective,
            'recommendation': '구현 권장' if cost_effective else '대안 검토'
        }

    def set_treatment(self,
                     risk_id: str,
                     treatment: str,
                     controls: List[str],
                     residual_risk: float):
        """위험 대응 설정"""
        if risk_id in self.risks:
            risk = self.risks[risk_id]
            risk.treatment = treatment
            risk.controls = controls
            risk.residual_risk = residual_risk

    def get_risk_report(self) -> Dict:
        """위험 보고서 생성"""
        risks_by_level = {
            level: [] for level in RiskLevel
        }

        for risk in self.risks.values():
            risks_by_level[risk.risk_level].append(risk.to_dict())

        return {
            'total_risks': len(self.risks),
            'by_level': {
                level.name: len(risks)
                for level, risks in risks_by_level.items()
            },
            'details': risks_by_level,
            'summary': {
                'critical_immediate': len(risks_by_level[RiskLevel.CRITICAL]),
                'high_action_needed': len(risks_by_level[RiskLevel.HIGH]),
                'medium_monitor': len(risks_by_level[RiskLevel.MEDIUM]),
                'low_acceptable': len(risks_by_level[RiskLevel.LOW]) +
                                  len(risks_by_level[RiskLevel.NEGLIGIBLE])
            }
        }

    def prioritize_risks(self) -> List[Risk]:
        """위험 우선순위 정렬"""
        return sorted(
            self.risks.values(),
            key=lambda r: (r.risk_level.value, -r.risk_score),
            reverse=True
        )

# 사용 예시
if __name__ == "__main__":
    rms = RiskManagementSystem()

    # 1. 자산 등록
    customer_db = Asset(
        id="ASSET-001",
        name="고객 DB",
        type=AssetType.DATA,
        owner="DB팀",
        value=10_000_000_000,  # 100억 원
        criticality=5,
        description="고객 개인정보 및 거래 이력"
    )
    rms.register_asset(customer_db)

    # 2. 위협 등록
    ransomware = Threat(
        id="THREAT-001",
        name="랜섬웨어 공격",
        category=ThreatCategory.CYBER_ATTACK,
        description="암호화 및 금전 갈취",
        likelihood_base=0.3  # 30% 기본 발생 확률
    )
    rms.register_threat(ransomware)

    # 3. 취약점 등록
    unpatched_db = Vulnerability(
        id="VULN-001",
        name="미패치 DB 취약점",
        description="SQL Server 최신 패치 미적용",
        cvss_score=9.8,
        affected_asset_id="ASSET-001",
        exploitability=0.8
    )
    rms.register_vulnerability(unpatched_db)

    # 4. 위험 식별
    risk = rms.identify_risk("ASSET-001", "THREAT-001", "VULN-001")
    print(f"=== 위험 식별 결과 ===")
    print(f"위험 ID: {risk.id}")
    print(f"위험 등급: {risk.risk_level.name}")
    print(f"가능성: {risk.likelihood:.1%}")
    print(f"영향도: {risk.impact:,.0f}원")

    # 5. 정량적 분석
    quant_result = rms.analyze_quantitative(risk, aro=0.1)  # 10년에 1회
    print(f"\n=== 정량적 분석 ===")
    print(f"SLE (단일 손실): {quant_result['sle']:,.0f}원")
    print(f"ARO (연간 발생률): {quant_result['aro']}")
    print(f"ALE (연간 손실 기대값): {quant_result['ale']:,.0f}원")

    # 6. 위험 대응 평가
    treatment_eval = rms.evaluate_treatment(
        risk=risk,
        control_cost=100_000_000,  # 1억 원/년
        control_effectiveness=0.9,  # 90% 감소
        aro=0.1
    )
    print(f"\n=== 위험 대응 평가 ===")
    print(f"현재 ALE: {treatment_eval['current_ale']:,.0f}원")
    print(f"통제 후 ALE: {treatment_eval['new_ale']:,.0f}원")
    print(f"연간 절감액: {treatment_eval['annual_savings']:,.0f}원")
    print(f"ROI: {treatment_eval['roi']:.1f}%")
    print(f"권장사항: {treatment_eval['recommendation']}")

    # 7. 위험 보고서
    report = rms.get_risk_report()
    print(f"\n=== 위험 보고서 ===")
    print(f"총 위험 수: {report['total_risks']}")
    print(f"Critical: {report['summary']['critical_immediate']}")
    print(f"High: {report['summary']['high_action_needed']}")
