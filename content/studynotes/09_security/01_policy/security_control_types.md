+++
title = "보안 통제 유형 (Security Control Types)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# 보안 통제 유형 (Security Control Types)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 보안 통제는 위협 발생 시점 기준으로 예방(Preventive), 탐지(Detective), 교정(Corrective), 복구(Recovery), 억제(Deterrent)의 5가지 유형으로 분류되며, 이들의 조합이 심층 방어(Defense in Depth)를 구성합니다.
> 2. **가치**: 각 유형별 통제의 적절한 배치는 보안 사고의 예방부터 복구까지 전 생애주기를 커버하여 잔여 위험(Residual Risk)을 최소화합니다.
> 3. **융합**: ISO 27001, NIST CSF, PCI DSS 등 모든 보안 프레임워크가 통제 유형 분류를 기반으로 요구사항을 체계화하며, 자동화된 SOAR 플랫폼에서 유형별 대응 플레이북으로 구현됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**보안 통제(Security Control)**는 정보자산을 보호하기 위해 적용하는 기술적, 관리적, 물리적 수단을 의미합니다. 통제는 위협이 실제 보안 사고로 발전하는 과정에서 어느 시점에 개입하는가에 따라 **5가지 유형**으로 분류됩니다:

1. **예방 통제 (Preventive)**: 위협이 발생하기 전에 차단
2. **탐지 통제 (Detective)**: 위협이나 위반 발생을 식별 및 경고
3. **교정 통제 (Corrective)**: 위반 발생 후 영향을 수정하거나 중단
4. **복구 통제 (Recovery)**: 사고 후 정상 상태로 복원
5. **억제 통제 (Deterrent)**: 잠재적 공격자의 의지를 약화시킴

이 분류는 **NIST SP 800-53**과 **ISO/IEC 27001**에서 채택한 표준 분류 체계입니다.

#### 2. 비유를 통한 이해
보안 통제 유형은 **'건물 보안 시스템'**에 비유할 수 있습니다:

- **예방**: 건물 출입구의 키카드 시스템, 보안 요원
- **탐지**: CCTV, 침입 감지 센서, 화재 경보기
- **교정**: 스프링클러 (화재 시 자동 진화), 자동 차단 벨브
- **복구**: 소화기, 피난 계획, 보험, 복구 팀
- **억제**: "CCTV 운영 중", "무단 침입 시 처벌" 경고문

#### 3. 등장 배경 및 발전 과정
1. **초기 보안**: 예방 중심 (성벽, 잠금장치)
2. **1960~70년대**: 컴퓨터 보안 접근 통제 모델 (Bell-LaPadula, Biba)
3. **1990년대**: 위험 기반 접근, 탐지/복구 중요성 대두
4. **2000년대**: NIST SP 800-53 등 표준화된 통제 분류 체계 정립
5. **2010년대~**: 지능형 위협(APT) 대응을 위한 교정/복구 통제 강화
6. **현재**: 자동화된 탐지-대응(EDR, SOAR)으로 유형 간 경계 모호해짐

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 보안 통제 유형 상세 분석

| 통제 유형 | 정의 | 작동 시점 | 핵심 목표 | 대표 기술 | 비유 |
|:---|:---|:---|:---|:---|:---|
| **예방 (Preventive)** | 위협 발생 전 차단 | 사건 이전 | 위험 원천 봉쇄 | 방화벽, 암호화, 접근통제, MFA | 예방접종 |
| **탐지 (Detective)** | 위반/침입 식별 | 사건 발생 시/직후 | 인지 및 경고 | IDS, SIEM, 로그 분석, CCTV | 건강검진 |
| **교정 (Corrective)** | 위반 영향 수정 | 사건 진행 중/직후 | 피해 확산 방지 | EDR 격리, 자동 패치, 세션 종료 | 응급처치 |
| **복구 (Recovery)** | 정상 상태 복원 | 사건 종료 후 | 업무 연속성 | 백업 복원, DRP, 이미지 복원 | 재활치료 |
| **억제 (Deterrent)** | 공격 의지 약화 | 사건 이전 | 심리적 방어 | 경고문, 감사 정책, 처벌 규정 | 경비 표지판 |

#### 2. 보안 통제 유형 간 상호작용 다이어그램

```text
                    [ 보안 사고 타임라인 ]
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
    ▼                      ▼                      ▼
 [사전 단계]          [사건 발생]           [사후 단계]
    │                      │                      │
    │                      │                      │
┌───▼──────────────────────▼──────────────────────▼───┐
│                                                      │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐       │
│   │ 예방     │   │ 탐지     │   │ 교정     │       │
│   │Preventive│   │Detective │   │Corrective│       │
│   └────┬─────┘   └────┬─────┘   └────┬─────┘       │
│        │              │              │              │
│        ▼              ▼              ▼              │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐       │
│   │ 방화벽   │   │  IDS/IPS │   │  EDR     │       │
│   │ 암호화   │   │  SIEM    │   │  자동격리│       │
│   │ 접근통제 │   │  로깅    │   │  패치    │       │
│   │ MFA      │   │  CCTV    │   │  차단    │       │
│   └──────────┘   └──────────┘   └──────────┘       │
│                                                      │
│   ┌──────────┐                    ┌──────────┐      │
│   │ 억제     │                    │ 복구     │      │
│   │Deterrent │                    │ Recovery │      │
│   └────┬─────┘                    └────┬─────┘      │
│        │                               │            │
│        ▼                               ▼            │
│   ┌──────────┐                    ┌──────────┐      │
│   │ 경고문   │                    │ 백업복원 │      │
│   │ 감사정책 │                    │ DRP      │      │
│   │ 처벌규정 │                    │ 복구계획 │      │
│   │ 허니팟   │                    │ 이미지복원│     │
│   └──────────┘                    └──────────┘      │
│                                                      │
└──────────────────────────────────────────────────────┘

<<< 심층 방어를 위한 통제 조합 >>>

    Layer 1: 예방 + 억제
    ├── 기술적: 방화벽 + 경고 배너
    └── 물리적: 출입문 + "No Entry" 표지판

    Layer 2: 탐지 + 교정
    ├── 기술적: IDS 탐지 → 자동 차단
    └── 관리적: 감사 발견 → 즉시 시정

    Layer 3: 복구 + 피드백
    ├── 기술적: 백업 복원 → 예방 통제 개선
    └── 관리적: 사후 분석 → 정책 업데이트
```

#### 3. 심층 동작 원리: 5단계 통제 연계 프로세스

```
① 예방 통제 작동 (사전)
   ┌─ 사용자 인증 (MFA)
   ├─ 접근 권한 확인 (RBAC)
   ├─ 입력 검증 (WAF)
   └─ 암호화 적용 (TLS 1.3)
          │
          ▼ [ 우회 성공 시 ]

② 탐지 통제 작동 (발생 시)
   ┌─ 이상 행동 탐지 (UEBA)
   ├─ 서명 매칭 (IDS)
   ├─ 로그 상관 분석 (SIEM)
   └─ 알림 발송 (PagerDuty)
          │
          ▼ [ 위반 확인 시 ]

③ 교정 통제 작동 (진행 중)
   ┌─ 자동 세션 종료
   ├─ 계정 잠금
   ├─ 엔드포인트 격리 (EDR)
   └─ 악성코드 제거
          │
          ▼ [ 피해 발생 시 ]

④ 복구 통제 작동 (사후)
   ┌─ 백업에서 데이터 복원
   ├─ 시스템 이미지 복원
   ├─ 서비스 재개 (DRP)
   └─ 취약점 패치
          │
          ▼ [ 사고 종료 후 ]

⑤ 억제 통제 (지속적)
   ┌─ 사고 공개 (필요 시)
   ├─ 처벌 및 제재
   ├─ 보안 정책 강화 공지
   └─ 교육 및 인식 제고
```

#### 4. 핵심 알고리즘 & 실무 코드: 통제 효과성 측정

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime, timedelta
import random

class ControlType(Enum):
    PREVENTIVE = "preventive"
    DETECTIVE = "detective"
    CORRECTIVE = "corrective"
    RECOVERY = "recovery"
    DETERRENT = "deterrent"

class ControlLayer(Enum):
    ADMINISTRATIVE = "administrative"
    TECHNICAL = "technical"
    PHYSICAL = "physical"

@dataclass
class SecurityControl:
    """보안 통제 정의"""
    control_id: str
    name: str
    control_type: ControlType
    layer: ControlLayer
    effectiveness: float  # 0.0 ~ 1.0
    cost: float  # 연간 운영 비용
    coverage: float  # 커버리지 (0.0 ~ 1.0)

@dataclass
class ThreatScenario:
    """위협 시나리오"""
    scenario_id: str
    name: str
    likelihood: float  # 연간 발생 확률
    impact: float  # 영향도 (금액)
    affected_assets: List[str]

class ControlEffectivenessAnalyzer:
    """통제 효과성 분석기"""

    def __init__(self):
        self.controls: List[SecurityControl] = []

    def add_control(self, control: SecurityControl):
        self.controls.append(control)

    def calculate_residual_risk(
        self,
        scenario: ThreatScenario,
        applied_controls: List[SecurityControl]
    ) -> dict:
        """
        잔여 위험 계산

        통제가 없을 때의 기본 위험 = 발생 확률 × 영향도
        통제 적용 후 잔여 위험 = 기본 위험 × (1 - 통제 효과성)
        """
        inherent_risk = scenario.likelihood * scenario.impact

        # 유형별 통제 효과성 누적 (중복 효과 고려)
        type_effectiveness = {}
        for ct in ControlType:
            controls_of_type = [
                c for c in applied_controls
                if c.control_type == ct
            ]
            if controls_of_type:
                # 다중 통제의 결합 효과: 1 - (1-e1)(1-e2)...
                combined = 1.0
                for c in controls_of_type:
                    combined *= (1 - c.effectiveness * c.coverage)
                type_effectiveness[ct.value] = 1 - combined
            else:
                type_effectiveness[ct.value] = 0.0

        # 전체 통제 효과성 (각 유형의 상승 효과)
        total_effectiveness = 1.0
        for eff in type_effectiveness.values():
            total_effectiveness *= (1 - eff)
        total_effectiveness = 1 - total_effectiveness

        residual_risk = inherent_risk * (1 - total_effectiveness)

        return {
            "scenario": scenario.name,
            "inherent_risk": inherent_risk,
            "residual_risk": residual_risk,
            "risk_reduction": inherent_risk - residual_risk,
            "risk_reduction_pct": (1 - residual_risk / inherent_risk) * 100,
            "type_breakdown": type_effectiveness,
            "total_control_effectiveness": total_effectiveness
        }

    def optimize_control_investment(
        self,
        scenarios: List[ThreatScenario],
        budget: float
    ) -> Dict[str, List[SecurityControl]]:
        """
        예산 제약 하 최적 통제 조합 도출
        (ROI 기반 우선순위)
        """
        control_roi = []

        for control in self.controls:
            total_risk_reduction = 0
            for scenario in scenarios:
                # 단일 통제 추가 시 위험 감소분
                result = self.calculate_residual_risk(
                    scenario,
                    [control]
                )
                total_risk_reduction += result["risk_reduction"]

            roi = total_risk_reduction / control.cost if control.cost > 0 else 0
            control_roi.append((control, roi))

        # ROI 내림차순 정렬
        control_roi.sort(key=lambda x: x[1], reverse=True)

        # 예산 내 최적 조합 선택
        selected_controls = []
        remaining_budget = budget
        total_cost = 0

        for control, roi in control_roi:
            if control.cost <= remaining_budget:
                selected_controls.append(control)
                remaining_budget -= control.cost
                total_cost += control.cost

        return {
            "selected_controls": selected_controls,
            "total_cost": total_cost,
            "remaining_budget": remaining_budget,
            "roi_ranking": [(c.name, r) for c, r in control_roi[:10]]
        }

    def generate_control_matrix(self) -> Dict[str, Dict[str, List[str]]]:
        """유형×계층 매트릭스 생성"""
        matrix = {}
        for ct in ControlType:
            matrix[ct.value] = {}
            for cl in ControlLayer:
                controls = [
                    c.name for c in self.controls
                    if c.control_type == ct and c.layer == cl
                ]
                matrix[ct.value][cl.value] = controls
        return matrix

# 사용 예시
analyzer = ControlEffectivenessAnalyzer()

# 통제 정의
analyzer.add_control(SecurityControl(
    control_id="C001",
    name="엔드포인트 보안 (EDR)",
    control_type=ControlType.PREVENTIVE,
    layer=ControlLayer.TECHNICAL,
    effectiveness=0.85,
    cost=50000,
    coverage=0.95
))

analyzer.add_control(SecurityControl(
    control_id="C002",
    name="침입 탐지 시스템 (IDS)",
    control_type=ControlType.DETECTIVE,
    layer=ControlLayer.TECHNICAL,
    effectiveness=0.80,
    cost=30000,
    coverage=1.0
))

analyzer.add_control(SecurityControl(
    control_id="C003",
    name="자동 격리 플레이북",
    control_type=ControlType.CORRECTIVE,
    layer=ControlLayer.TECHNICAL,
    effectiveness=0.90,
    cost=20000,
    coverage=0.80
))

analyzer.add_control(SecurityControl(
    control_id="C004",
    name="일일 백업",
    control_type=ControlType.RECOVERY,
    layer=ControlLayer.TECHNICAL,
    effectiveness=0.95,
    cost=15000,
    coverage=1.0
))

# 위협 시나리오
ransomware = ThreatScenario(
    scenario_id="T001",
    name="랜섬웨어 공격",
    likelihood=0.15,  # 연간 15%
    impact=2000000,   # 20억 원
    affected_assets=["file_server", "db_server", "workstations"]
)

# 잔여 위험 계산
all_controls = [
    c for c in analyzer.controls
    if c.control_id in ["C001", "C002", "C003", "C004"]
]

result = analyzer.calculate_residual_risk(ransomware, all_controls)

print(f"시나리오: {result['scenario']}")
print(f"기본 위험: ₩{result['inherent_risk']:,.0f}")
print(f"잔여 위험: ₩{result['residual_risk']:,.0f}")
print(f"위험 감소: {result['risk_reduction_pct']:.1f}%")
print(f"유형별 효과성: {result['type_breakdown']}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 통제 유형별 기술 비교

| 통제 유형 | 장점 | 단점 | 대표 솔루션 | 적용 우선순위 |
|:---|:---|:---|:---|:---|
| **예방** | 사전 차단으로 비용 최소화 | 100% 차단 불가능, 우회 가능 | Firewall, DLP, 암호화 | 1순위 |
| **탐지** | 실제 침입 식별, 포렌식 지원 | 사후 인지, 이미 피해 발생 가능 | SIEM, IDS, UEBA | 2순위 |
| **교정** | 신속 대응으로 피해 확산 방지 | 자동화 실패 시 수동 개입 필요 | EDR, SOAR | 2순위 |
| **복구** | 업무 연속성 보장 | 복구 시간 동안 서비스 중단 | Veeam, Commvault | 3순위 |
| **억제** | 비용 효율적, 심리적 방어 | 결심한 공격자에게 무력 | 경고문, 감사 정책 | 보조 |

#### 2. 산업별 통제 유형 중요도

| 산업 | 1순위 | 2순위 | 3순위 | 이유 |
|:---|:---|:---|:---|:---|
| **금융** | 예방 > 탐지 | 교정 | 복구 | 데이터 무결성 최우선 |
| **의료** | 복구 > 예방 | 탐지 | 교정 | 서비스 가용성이 생명 |
| **국방** | 예방 > 억제 | 탐지 | 교정 | 기밀성 절대 우선 |
| **제조** | 교정 > 복구 | 예방 | 탐지 | OT 환경 가용성 중시 |
| **SaaS** | 탐지 > 교정 | 예방 | 복구 | 고객 신뢰, SLA 준수 |

#### 3. 과목 융합 관점 분석

- **네트워크 보안**: 방화벽(예방), IDS(탐지), IPS(교정)의 계층적 배치
- **시스템 보안**: ASLR/DEP(예방), 로깅(탐지), 백업(복구)의 OS 수준 구현
- **애플리케이션 보안**: 입력 검증(예방), 로깅(탐지), 예외 처리(교정)의 코드 레벨
- **클라우드 보안**: IAM(예방), CloudTrail(탐지), Auto Remediation(교정)의 서비스형 통제
- **컴플라이언스**: ISO 27001 Annex A가 모든 유형의 통제 요구

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 랜섬웨어 대응 통제 설계**
- 상황: 랜섬웨어 공격 증가, 피해 시 3일 이상 서비스 중단 우려
- 판단: 예방-탐지-교정-복구 전 유형 통제 배치
- 핵심 결정:
  - 예방: EDR 100% 배포, 이메일 보안 게이트웨이
  - 탐지: 랜섬웨어 행위 탐지 룰, 파일 변경 모니터링
  - 교정: 자동 네트워크 격리 플레이북
  - 복구: Immutable 백업, 3-2-1 전략, 4시간 RTO
- 효과: 공격 성공 시에도 4시간 내 복구, 데이터 손실 0

**시나리오 2: 내부자 위협 통제 설계**
- 상황: 퇴사자 데이터 유출 사고 발생, 재발 방지 필요
- 판단: 억제-예방-탐지-교정 체계 구축
- 핵심 결정:
  - 억제: 기밀유지서명, 처벌 사례 공유, 퇴사자 인터뷰
  - 예방: 최소 권한 원칙, DLP, 접근 로그 실명제
  - 탐지: UEBA, 대량 다운로드 탐지, USB 사용 모니터링
  - 교정: 계정 즉시 잠금, 포렌식 조사
- 효과: 내부자 위협 탐지율 90% 향상

**시나리오 3: 클라우드 마이그레이션 통제 설계**
- 상황: 온프레미스에서 AWS로 이관, 통제 체계 재설계 필요
- 판단: 클라우드 네이티브 통제 + 기존 통제 하이브리드
- 핵심 결정:
  - 예방: AWS IAM, Security Group, KMS
  - 탐지: CloudTrail, GuardDuty, Security Hub
  - 교정: Lambda 자동 조치, Systems Manager
  - 복구: AMI 백업, Cross-Region Replication
- 효과: 클라우드 보안 가시성 100%, 자동화된 대응

#### 2. 도입 시 고려사항 (체크리스트)

**기술적 체크리스트**
- [ ] 각 위협 시나리오별 필요 통제 유형 식별
- [ ] 기존 통제와 신규 통제 간 중복/누락 검토
- [ ] 자동화 가능 영역(탐지→교정) 파악
- [ ] 통제 간 연동성 테스트 (예: IDS 탐지 → 방화벽 차단)

**운영적 체크리스트**
- [ ] 통제 유형별 담당자 R&R 정의
- [ ] 통제 효과성 측정 지표(KPI) 설정
- [ ] 정기적 통제 효과성 평가 프로세스
- [ ] 통제 실패 시 대안(Fallback) 마련

#### 3. 안티패턴 (Anti-patterns)

| 안티패턴 | 문제점 | 올바른 접근 |
|:---|:---|:---|
| **예방만 강조** | 우회 성공 시 무방비 상태 | 탐지-교정-복구 통제 병행 |
| **탐지 후 수동만 대응** | 대응 지연으로 피해 확대 | SOAR로 자동화된 교정 |
| **복구 통제 간소화** | 복구 실패 시 서비스 중단 장기화 | 정기적 복구 훈련, 검증 |
| **억제 통제 무시** | 내부자 위협, 실수 증가 | 교육, 인식 제고 병행 |

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | 내용 | 측정 지표 |
|:---|:---|:---|
| 정량적 | 위험 감소 | 통제 적용 후 잔여 위험 70% 감소 |
| 정량적 | 대응 시간 | MTTR 50% 단축 |
| 정량적 | 사고 건수 | 예방 통제로 연간 사고 40% 감소 |
| 정성적 | 규정 준수 | ISO 27001 인증 획득 |
| 정성적 | 보안 인식 | 전사 보안 문화 정착 |

#### 2. 미래 전망 및 진화 방향

- **AI 기반 자동화**: 탐지→교정의 자동 연계, 예측적 예방 통제
- **지속적 적응 보안**: 위협 레벨에 따른 통제 강도 자동 조절
- **DevSecOps 통합**: 코드 레벨 예방 통제, 자동화된 교정
- **클라우드 네이티브**: CSPM, CWPP 등 서비스형 통제 확대

#### 3. 참고 표준/가이드

- **NIST SP 800-53**: 통제 유형 분류 체계 (Appendix F)
- **ISO/IEC 27001 Annex A**: 93개 통제 항목
- **NIST Cybersecurity Framework**: 5기능(Identify/Protect/Detect/Respond/Recover)과 매핑
- **CIS Controls v8**: 18개 통제의 유형 분류

---

### 관련 개념 맵 (Knowledge Graph)

- [심층 방어](@/studynotes/09_security/01_policy/defense_in_depth.md) : 다층 보안을 위한 통제 조합
- [위험 관리](@/studynotes/09_security/01_policy/risk_management.md) : 통제 효과성 기반 위험 완화
- [보안 정책](@/studynotes/09_security/01_policy/security_policy.md) : 관리적 통제의 근거
- [ISO 27001](@/studynotes/09_security/01_policy/isms_p.md) : 통제 요구사항 표준
- [SIEM](@/studynotes/09_security/06_compliance/siem.md) : 탐지 통제의 핵심 플랫폼

---

### 어린이를 위한 3줄 비유 설명

1. **미리 막기 (예방)**: 나쁜 사람이 들어오지 못하게 문을 잠가요. 열쇠가 있는 사람만 들어올 수 있죠. 이게 예방이에요.
2. **빨리 알기 (탐지)**: 혹시 누군가 몰래 들어왔는지 알 수 있게 CCTV를 설치해요. 이상한 일이 생기면 바로 알 수 있죠.
3. **다시 고치기 (복구)**: 만약 문이 부서졌으면 새 문으로 바꿔요. 잃어버린 장난감도 다시 사주고요. 원래대로 만드는 게 복구예요.
