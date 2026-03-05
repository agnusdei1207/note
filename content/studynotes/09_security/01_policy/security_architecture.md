+++
title = "보안 아키텍처 (Security Architecture)"
date = "2026-03-04"
[extra]
categories = "studynotes-09_security"
+++

# 보안 아키텍처 (Security Architecture)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 조직의 비즈니스 목표와 위험 식욕에 부합하는 보안 통제를 체계적으로 설계하고 구현하는 구조적 프레임워크입니다.
> 2. **가치**: 보안 투자의 최적화, 위험 관리의 일관성, 컴플라이언스 충족, 비즈니스-IT 정렬을 실현합니다.
> 3. **융합**: SABSA, TOGAF, Zachman, Zero Trust 등 다양한 프레임워크가 결합된 엔터프라이즈 보안 설계 체계입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**보안 아키텍처(Security Architecture)**는 조직의 정보보안 요구사항을 충족하기 위한 보안 통제, 메커니즘, 프로세스의 구조적 설계입니다. 이는 비즈니스 아키텍처, 데이터 아키텍처, 애플리케이션 아키텍처, 기술 아키텍처와 통합되어야 합니다.

**Open Group 정의**:
> "조직의 보안 요구사항을 충족하기 위해 보안 서비스, 통제, 메커니즘을 설계하고 조정하는 구조"

**보안 아키텍처의 구성 요소**:
- **보안 정책 (Policy)**: 원칙과 규칙
- **보안 서비스 (Services)**: 인증, 인가, 암호화 등
- **보안 통제 (Controls)**: 기술적, 관리적, 물리적
- **보안 메커니즘 (Mechanisms)**: 구현 방식

#### 2. 💡 비유를 통한 이해
보안 아키텍처는 **'건축 설계도'**에 비유할 수 있습니다.
- **설계 철학**: 현대식 vs 클래식 - 보안 원칙
- **구조도**: 기둥, 벽, 창문 배치 - 아키텍처 다이어그램
- **재료 명세서**: 콘크리트 강도, 철근 규격 - 보안 통제 스펙
- **시공 지침서**: 순서, 검수 기준 - 구현 가이드
- **유지보수 계획**: 정기 점검, 보수 - 운영 프로세스

#### 3. 등장 배경 및 발전 과정
1. **초기 보안**: 개별 시스템별 보안 (1970~80년대)
2. **표준화 등장**: ISO 7498-2 보안 아키텍처 (1988)
3. **프레임워크**: Zachman, TOGAF 보안 확장 (1990년대)
4. **SABSA**: 비즈니스 기반 보안 아키텍처 (1995)
5. **엔터프라이즈**: EAP (Enterprise Security Architecture) (2000년대)
6. **Zero Trust**: 새로운 패러다임 (2010년대~)

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 주요 보안 아키텍처 프레임워크 비교 (표)

| 프레임워크 | 특징 | 구조 | 장점 | 용도 |
|:---|:---|:---|:---|:---|
| **SABSA** | 비즈니스 중심 | 6계층 × 6열 매트릭스 | 비즈니스 정렬 | 엔터프라이즈 |
| **TOGAF** | EA 통합 | ADM + 보안 확장 | IT 전체 통합 | 대기업 EA |
| **Zachman** | ontologie 기반 | 6행 × 6열 | 분류 체계 | 분석/설계 |
| **NIST CSF** | 위험 기반 | 5/6 기능 | 실무적 가이드 | 미 연방/일반 |
| **Zero Trust** | 불신 기반 | 7가지 원칙 | 현대적 위협 대응 | 클라우드/DX |

#### 2. SABSA 아키텍처 매트릭스

```text
<<< SABSA (Sherwood Applied Business Security Architecture) Matrix >>>

    +------------------------------------------------------------------+
    |                 SABSA 6×6 매트릭스                                |
    +------------------------------------------------------------------+
    |                | WHAT    | WHY    | HOW     | WHO    | WHERE   | WHEN    |
    |                | 자산    | 동기   | 과정    | 사람    | 위치    | 시간    |
    +------------------------------------------------------------------+
    | Contextual     | 비즈니스| 비즈니스| 비즈니스| 비즈니스| 비즈니스| 비즈니스|
    | (운영 맥락)    | 자산    | 위험    | 프로세스| 주체    | 환경    | 일정    |
    +------------------------------------------------------------------+
    | Conceptual     | 보안    | 보안    | 보안    | 보안    | 보안    | 보안    |
    | (개념적)       | 도메인  | 정책    | 서비스  | 엔티티  | 위치    | 시간    |
    +------------------------------------------------------------------+
    | Logical        | 보안    | 보안    | 보안    | 보안    | 보안    | 보안    |
    | (논리적)       | 정보    | 규칙    | 메커니즘| 역할    | 네트워크| 일정    |
    +------------------------------------------------------------------+
    | Physical       | 보안    | 보안    | 보안    | 보안    | 보안    | 보안    |
    | (물리적)       | 데이터  | 표준    | 도구    | 계정    | 하드웨어| 타임라인|
    +------------------------------------------------------------------+
    | Component      | 보안    | 보안    | 보안    | 보안    | 보안    | 보안    |
    | (구성요소)     | 제품    | 지침    | 기술    | ID 시스템| 플랫폼  | 스케줄  |
    +------------------------------------------------------------------+
    | Operational    | 보안    | 보안    | 보안    | 보안    | 보안    | 보안    |
    | (운영)         | 운영    | 모니터링| 운영    | 관리    | 배포    | 운영    |
    +------------------------------------------------------------------+

<<< 엔터프라이즈 보안 아키텍처 구조 >>>

    +------------------------------------------------------------------+
    |                    비즈니스 아키텍처 (Business)                  |
    |  ┌──────────────────────────────────────────────────────────┐  |
    |  │  전략적 목표 | 비즈니스 프로세스 | 조직 구조 | 규제 요건  │  |
    |  └──────────────────────────────────────────────────────────┘  |
    +------------------------------------------------------------------+
                                    │
                                    │ 정렬
                                    v
    +------------------------------------------------------------------+
    |                    보안 아키텍처 (Security)                     |
    |  ┌──────────────────────────────────────────────────────────┐  |
    |  │                    보안 거버넌스                          │  |
    |  │  ┌────────────────────────────────────────────────────┐  │  |
    |  │  │ 보안 정책 | 표준 | 지침 | 절차 | 역할/책임         │  │  |
    |  │  └────────────────────────────────────────────────────┘  │  |
    |  └──────────────────────────────────────────────────────────┘  |
    |  ┌──────────────────────────────────────────────────────────┐  |
    |  │                    보안 도메인                            │  |
    |  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌──────────┐ │  |
    |  │  │ 신원/접근 │ │ 네트워크  │ │ 데이터    │ │ 애플리케이션│ │  |
    |  │  │ 관리      │ │ 보안      │ │ 보안      │ │ 보안       │ │  |
    |  │  │ (IAM)     │ │ (NetSec)  │ │ (DataSec) │ │ (AppSec)   │ │  |
    |  │  └───────────┘ └───────────┘ └───────────┘ └──────────┘ │  |
    |  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌──────────┐ │  |
    |  │  │ 엔드포인트│ │ 클라우드  │ │ 운영      │ │ 물리      │ │  |
    |  │  │ 보안      │ │ 보안      │ │ 보안      │ │ 보안      │ │  |
    |  │  │ (EPS)     │ │ (CloudSec)│ │ (OpSec)   │ │ (PhySec)  │ │  |
    |  │  └───────────┘ └───────────┘ └───────────┘ └──────────┘ │  |
    |  └──────────────────────────────────────────────────────────┘  |
    |  ┌──────────────────────────────────────────────────────────┐  |
    |  │                    보안 서비스                             │  |
    |  │  인증 | 인가 | 암호화 | 무결성 | 부인방지 | 감사          │  |
    |  └──────────────────────────────────────────────────────────┘  |
    +------------------------------------------------------------------+
                                    │
                                    │ 구현
                                    v
    +------------------------------------------------------------------+
    |                    기술 아키텍처 (Technology)                   |
    |  ┌──────────────────────────────────────────────────────────┐  |
    |  │  인프라 | 플랫폼 | 미들웨어 | 애플리케이션 | 데이터       │  |
    |  └──────────────────────────────────────────────────────────┘  |
    +------------------------------------------------------------------+
```

#### 3. 심층 동작 원리: 보안 아키텍처 설계 방법론

```python
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple
from enum import Enum
from datetime import datetime

class ArchitectureLayer(Enum):
    BUSINESS = "business"          # 비즈니스
    DATA = "data"                  # 데이터
    APPLICATION = "application"    # 애플리케이션
    TECHNOLOGY = "technology"      # 기술
    SECURITY = "security"          # 보안

class SecurityDomain(Enum):
    IAM = "identity_access"
    NETWORK = "network"
    ENDPOINT = "endpoint"
    APPLICATION = "application"
    DATA = "data"
    CLOUD = "cloud"
    OPERATIONS = "operations"
    PHYSICAL = "physical"

class ControlType(Enum):
    PREVENTIVE = "preventive"
    DETECTIVE = "detective"
    CORRECTIVE = "corrective"
    RECOVERY = "recovery"
    DETERRENT = "deterrent"

class ControlLayer(Enum):
    ADMINISTRATIVE = "administrative"  # 관리적
    TECHNICAL = "technical"            # 기술적
    PHYSICAL = "physical"              # 물리적

@dataclass
class SecurityControl:
    """보안 통제"""
    id: str
    name: str
    domain: SecurityDomain
    control_type: ControlType
    control_layer: ControlLayer
    description: str
    implementation_status: str = "planned"  # planned, implementing, deployed
    effectiveness: float = 0.0  # 0.0 ~ 1.0
    cost: float = 0.0

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain.value,
            'type': self.control_type.value,
            'layer': self.control_layer.value,
            'status': self.implementation_status,
            'effectiveness': self.effectiveness
        }

@dataclass
class SecurityRequirement:
    """보안 요구사항"""
    id: str
    name: str
    description: str
    source: str  # regulation, policy, risk, business
    priority: int  # 1-5
    related_controls: List[str] = field(default_factory=list)

@dataclass
class SecurityCapability:
    """보안 역량"""
    name: str
    domain: SecurityDomain
    maturity_level: int  # 0-5
    target_level: int
    gaps: List[str] = field(default_factory=list)
    controls: List[SecurityControl] = field(default_factory=list)

class SecurityArchitectureFramework:
    """
    보안 아키텍처 프레임워크
    - 요구사항 관리
    - 통제 매핑
    - 역량 평가
    - 로드맵 수립
    """

    def __init__(self, organization_name: str):
        self.organization_name = organization_name
        self.requirements: Dict[str, SecurityRequirement] = {}
        self.controls: Dict[str, SecurityControl] = {}
        self.capabilities: Dict[str, SecurityCapability] = {}
        self.architecture_views: Dict[str, Dict] = {}

    def add_requirement(self, requirement: SecurityRequirement):
        """보안 요구사항 추가"""
        self.requirements[requirement.id] = requirement

    def add_control(self, control: SecurityControl):
        """보안 통제 추가"""
        self.controls[control.id] = control

    def map_control_to_requirement(self, control_id: str, requirement_id: str):
        """통제-요구사항 매핑"""
        if requirement_id in self.requirements:
            if control_id not in self.requirements[requirement_id].related_controls:
                self.requirements[requirement_id].related_controls.append(control_id)

    def assess_capability(self, domain: SecurityDomain) -> SecurityCapability:
        """역량 평가"""
        domain_controls = [
            c for c in self.controls.values() if c.domain == domain
        ]

        # 배포된 통제만 고려
        deployed = [c for c in domain_controls if c.implementation_status == "deployed"]

        # 평균 효과성으로 성숙도 계산
        if deployed:
            avg_effectiveness = sum(c.effectiveness for c in deployed) / len(deployed)
            maturity = int(avg_effectiveness * 5)
        else:
            maturity = 0

        capability = SecurityCapability(
            name=domain.value,
            domain=domain,
            maturity_level=maturity,
            target_level=3,  # 기본 목표
            gaps=self._identify_gaps(domain, domain_controls)
        )

        self.capabilities[domain.value] = capability
        return capability

    def _identify_gaps(self, domain: SecurityDomain, controls: List[SecurityControl]) -> List[str]:
        """갭 식별"""
        gaps = []

        # 계획된 통제
        planned = [c for c in controls if c.implementation_status == "planned"]
        if planned:
            gaps.append(f"{len(planned)} controls not yet implemented")

        # 저효과 통제
        low_effectiveness = [c for c in controls if c.effectiveness < 0.5]
        if low_effectiveness:
            gaps.append(f"{len(low_effectiveness)} controls with low effectiveness")

        # 통제 유형별 커버리지
        covered_types = set(c.control_type for c in controls)
        missing_types = set(ControlType) - covered_types
        if missing_types:
            gaps.append(f"Missing control types: {[t.value for t in missing_types]}")

        return gaps

    def generate_architecture_view(self, view_type: str) -> Dict:
        """아키텍처 뷰 생성"""
        if view_type == "capability":
            return self._generate_capability_view()
        elif view_type == "control":
            return self._generate_control_view()
        elif view_type == "requirement":
            return self._generate_requirement_view()
        elif view_type == "roadmap":
            return self._generate_roadmap_view()
        else:
            return {}

    def _generate_capability_view(self) -> Dict:
        """역량 뷰"""
        view = {
            'organization': self.organization_name,
            'generated_at': datetime.utcnow().isoformat(),
            'domains': {}
        }

        for domain in SecurityDomain:
            capability = self.capabilities.get(domain.value)
            if capability:
                view['domains'][domain.value] = {
                    'maturity_level': capability.maturity_level,
                    'target_level': capability.target_level,
                    'gap_count': len(capability.gaps),
                    'gaps': capability.gaps
                }
            else:
                view['domains'][domain.value] = {
                    'maturity_level': 0,
                    'target_level': 3,
                    'gap_count': 0,
                    'gaps': ['Not assessed']
                }

        return view

    def _generate_control_view(self) -> Dict:
        """통제 뷰"""
        view = {
            'organization': self.organization_name,
            'generated_at': datetime.utcnow().isoformat(),
            'summary': {
                'total': len(self.controls),
                'deployed': len([c for c in self.controls.values() if c.implementation_status == "deployed"]),
                'implementing': len([c for c in self.controls.values() if c.implementation_status == "implementing"]),
                'planned': len([c for c in self.controls.values() if c.implementation_status == "planned"])
            },
            'by_domain': {},
            'by_type': {}
        }

        # 도메인별 분류
        for domain in SecurityDomain:
            domain_controls = [c for c in self.controls.values() if c.domain == domain]
            view['by_domain'][domain.value] = len(domain_controls)

        # 유형별 분류
        for ctrl_type in ControlType:
            type_controls = [c for c in self.controls.values() if c.control_type == ctrl_type]
            view['by_type'][ctrl_type.value] = len(type_controls)

        return view

    def _generate_requirement_view(self) -> Dict:
        """요구사항 뷰"""
        view = {
            'organization': self.organization_name,
            'generated_at': datetime.utcnow().isoformat(),
            'requirements': [],
            'coverage_analysis': {}
        }

        for req in self.requirements.values():
            coverage = len(req.related_controls)
            view['requirements'].append({
                'id': req.id,
                'name': req.name,
                'source': req.source,
                'priority': req.priority,
                'control_coverage': coverage,
                'covered': coverage > 0
            })

        # 커버리지 분석
        covered = len([r for r in view['requirements'] if r['covered']])
        total = len(view['requirements'])
        view['coverage_analysis'] = {
            'total_requirements': total,
            'covered_requirements': covered,
            'uncovered_requirements': total - covered,
            'coverage_percentage': (covered / total * 100) if total > 0 else 0
        }

        return view

    def _generate_roadmap_view(self) -> Dict:
        """로드맵 뷰"""
        planned_controls = [
            c for c in self.controls.values()
            if c.implementation_status in ["planned", "implementing"]
        ]

        # 우선순위별 정렬 (비용/효과 기반)
        sorted_controls = sorted(
            planned_controls,
            key=lambda c: (c.cost / max(c.effectiveness, 0.1))
        )

        view = {
            'organization': self.organization_name,
            'generated_at': datetime.utcnow().isoformat(),
            'phases': [
                {
                    'phase': 'Phase 1 - Quick Wins',
                    'timeline': '0-3 months',
                    'controls': [c.to_dict() for c in sorted_controls[:5] if c.cost < 100000]
                },
                {
                    'phase': 'Phase 2 - Core Security',
                    'timeline': '3-6 months',
                    'controls': [c.to_dict() for c in sorted_controls[5:15]]
                },
                {
                    'phase': 'Phase 3 - Advanced Security',
                    'timeline': '6-12 months',
                    'controls': [c.to_dict() for c in sorted_controls[15:]]
                }
            ],
            'total_investment': sum(c.cost for c in planned_controls),
            'estimated_risk_reduction': sum(c.effectiveness * 0.2 for c in planned_controls if c.implementation_status == "deployed")
        }

        return view

    def assess_compliance(self, framework: str) -> Dict:
        """컴플라이언스 평가"""
        compliance_matrix = {
            'iso27001': {
                'domains': [SecurityDomain.IAM, SecurityDomain.NETWORK, SecurityDomain.DATA],
                'required_controls': 50
            },
            'pci-dss': {
                'domains': [SecurityDomain.NETWORK, SecurityDomain.DATA, SecurityDomain.APPLICATION],
                'required_controls': 40
            },
            'nist-csf': {
                'domains': list(SecurityDomain),
                'required_controls': 100
            }
        }

        if framework not in compliance_matrix:
            return {'error': f'Unknown framework: {framework}'}

        config = compliance_matrix[framework]

        # 관련 도메인 통제 분석
        relevant_controls = [
            c for c in self.controls.values()
            if c.domain in config['domains']
        ]

        deployed = len([c for c in relevant_controls if c.implementation_status == "deployed"])
        total_needed = config['required_controls']

        return {
            'framework': framework,
            'compliance_score': min(deployed / total_needed * 100, 100),
            'controls_deployed': deployed,
            'controls_required': total_needed,
            'gap': max(0, total_needed - deployed),
            'domains_covered': [d.value for d in config['domains']]
        }

# 사용 예시
if __name__ == "__main__":
    # 프레임워크 초기화
    framework = SecurityArchitectureFramework("Acme Corporation")

    # 요구사항 정의
    req1 = SecurityRequirement(
        id="REQ-001",
        name="데이터 암호화",
        description="모든 민감 데이터는 저장 및 전송 중 암호화되어야 함",
        source="regulation",
        priority=5
    )
    framework.add_requirement(req1)

    req2 = SecurityRequirement(
        id="REQ-002",
        name="다중 인증",
        description="모든 관리자 접근은 MFA를 통해야 함",
        source="policy",
        priority=5
    )
    framework.add_requirement(req2)

    # 통제 정의
    ctrl1 = SecurityControl(
        id="CTRL-001",
        name="TLS 1.3 암호화",
        domain=SecurityDomain.NETWORK,
        control_type=ControlType.PREVENTIVE,
        control_layer=ControlLayer.TECHNICAL,
        description="모든 통신에 TLS 1.3 적용",
        implementation_status="deployed",
        effectiveness=0.95,
        cost=50000
    )
    framework.add_control(ctrl1)
    framework.map_control_to_requirement("CTRL-001", "REQ-001")

    ctrl2 = SecurityControl(
        id="CTRL-002",
        name="AES-256 저장 암호화",
        domain=SecurityDomain.DATA,
        control_type=ControlType.PREVENTIVE,
        control_layer=ControlLayer.TECHNICAL,
        description="데이터베이스 컬럼 암호화",
        implementation_status="deployed",
        effectiveness=0.90,
        cost=100000
    )
    framework.add_control(ctrl2)
    framework.map_control_to_requirement("CTRL-002", "REQ-001")

    ctrl3 = SecurityControl(
        id="CTRL-003",
        name="FIDO2 인증",
        domain=SecurityDomain.IAM,
        control_type=ControlType.PREVENTIVE,
        control_layer=ControlLayer.TECHNICAL,
        description="하드웨어 키 기반 MFA",
        implementation_status="implementing",
        effectiveness=0.85,
        cost=200000
    )
    framework.add_control(ctrl3)
    framework.map_control_to_requirement("CTRL-003", "REQ-002")

    ctrl4 = SecurityControl(
        id="CTRL-004",
        name="WAF",
        domain=SecurityDomain.APPLICATION,
        control_type=ControlType.PREVENTIVE,
        control_layer=ControlLayer.TECHNICAL,
        description="웹 애플리케이션 방화벽",
        implementation_status="planned",
        effectiveness=0.80,
        cost=150000
    )
    framework.add_control(ctrl4)

    # 역량 평가
    print("=== Security Capability Assessment ===")
    for domain in [SecurityDomain.NETWORK, SecurityDomain.DATA, SecurityDomain.IAM]:
        capability = framework.assess_capability(domain)
        print(f"{domain.value}: Maturity {capability.maturity_level}/5")

    # 아키텍처 뷰
    print("\n=== Control View ===")
    control_view = framework.generate_architecture_view("control")
    print(f"Total Controls: {control_view['summary']['total']}")
    print(f"Deployed: {control_view['summary']['deployed']}")

    print("\n=== Requirement View ===")
    req_view = framework.generate_architecture_view("requirement")
    print(f"Requirements Coverage: {req_view['coverage_analysis']['coverage_percentage']:.1f}%")

    print("\n=== Compliance Assessment ===")
    compliance = framework.assess_compliance("iso27001")
    print(f"ISO 27001 Score: {compliance['compliance_score']:.1f}%")
