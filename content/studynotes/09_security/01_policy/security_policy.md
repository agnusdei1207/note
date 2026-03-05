+++
title = "보안 정책 (Security Policy)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# 보안 정책 (Security Policy)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 조직의 정보 자산을 보호하기 위해 경영진이 승인한 공식 문서로, 보안 목표, 범위, 역할/책임, 준수 요건을 체계적으로 정의하는 거버넌스의 핵심입니다.
> 2. **가치**: 보안 정책은 법적 컴플라이언스 충족, 보안 사고 예방, 직원 보안 의식 제고, 내부 통제 체계 확립의 기준점이 됩니다.
> 3. **융합**: ISO 27001, NIST CSF, GDPR 등 국제 표준과 연동하며, 클라우드 보안 정책, Zero Trust 정책 등 신기술 환경으로 지속 진화합니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**보안 정책(Security Policy)**은 조직이 정보 자산을 보호하기 위해 수립한 규칙, 지침, 표준, 절차의 총체적인 체계입니다. 이는 단순한 문서가 아니라 조직의 보안 문화와 행동 양식을 규정하는 '헌법'과 같은 역할을 수행합니다.

**정책 계층 구조 (Policy Hierarchy)**:
```
┌─────────────────────────────────────────────────────────────────┐
│  Level 1: Policies (정책)                                       │
│  - 경영진 승인, 높은 수준의 원칙                                 │
│  - "무엇을 보호할 것인가?", "왜 필요한가?"                        │
│  - 예: 정보보안 정책, 개인정보보호 정책, 접근통제 정책            │
├─────────────────────────────────────────────────────────────────┤
│  Level 2: Standards (표준)                                      │
│  - 정책을 구현하기 위한 기술적/운영적 요구사항                    │
│  - "어떻게 구현할 것인가?"                                       │
│  - 예: 암호화 표준, 비밀번호 표준, 네트워크 표준                  │
├─────────────────────────────────────────────────────────────────┤
│  Level 3: Guidelines (지침)                                     │
│  - 권장 사항, 모범 사례                                          │
│  - "무엇을 권장하는가?"                                          │
│  - 예: 모바일 기기 사용 지침, 원격근무 지침                       │
├─────────────────────────────────────────────────────────────────┤
│  Level 4: Procedures (절차)                                     │
│  - 단계별 수행 지침                                              │
│  - "구체적으로 어떤 단계를 거치는가?"                            │
│  - 예: 사용자 계정 생성 절차, 보안사고 대응 절차                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 2. 핵심 구성 요소

| 구성 요소 | 정의 | 예시 | 필수성 |
|:---|:---|:---|:---|
| **목적 (Purpose)** | 정책 존재 이유 | "정보 자산을 무단 접근으로부터 보호" | 필수 |
| **범위 (Scope)** | 적용 대상 | "전 임직원, 협력업체, 모든 IT 시스템" | 필수 |
| **역할/책임 (Roles)** | 담당자 정의 | CISO, 보안팀, IT팀, 전 직원 | 필수 |
| **준수 요건 (Compliance)** | 법적/규제 요건 | 개인정보보호법, ISO 27001 | 필수 |
| **시행일/개정이력** | 효력 발생 시점 | 2026.01.01 시행 | 필수 |
| **예외 처리** | 예외 승인 절차 | 예외 승인 위원회 심의 | 권장 |
| **위반 시 조치** | 제재 내용 | 징계, 형사 고발 | 권장 |

#### 3. 비유를 통한 이해
보안 정책은 **'국가의 헌법과 법률 체계'**에 비유할 수 있습니다.
- **정책(Policy)** = 헌법: 국가의 기본 원칙과 방향성
- **표준(Standard)** = 법률: 구체적인 규정과 의무
- **지침(Guideline)** = 행정지침: 권장 사항과 해석
- **절차(Procedure)** = 시행령/시행규칙: 구체적 수행 단계

#### 4. 등장 배경 및 발전 과정
1. **초기 (1970~80년대)**: 컴퓨터 보안 정책 - 물리적 접근 통제 중심
2. **성장기 (1990년대)**: 인터넷 확산 → 네트워크 보안 정책 대두
3. **표준화 (2000년대)**: ISO 17799(현 27001) 등 국제 표준 등장
4. **규제 강화 (2010년대)**: GDPR, 개인정보보호법 등 법적 의무 강화
5. **현재 (2020년대)**: Zero Trust, 클라우드 보안 정책, AI 윤리 규정

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 보안 정책 프레임워크 비교

| 프레임워크 | 주요 특징 | 적용 대상 | 핵심 문서 |
|:---|:---|:---|:---|
| **ISO 27001** | ISMS 인증 기반, PDCA 사이클 | 모든 조직 | ISMS 정책서 |
| **NIST CSF** | 5대 기능(식별/보호/탐지/대응/복구) | 미국 기관, 글로벌 기업 | 정보보안 프로그램 |
| **COBIT** | IT 거버넌스 중심 | IT 조직 | IT 정책 프레임워크 |
| **SABSA** | 비즈니스 연계 보안 아키텍처 | 엔터프라이즈 | 엔터프라이즈 보안 정책 |
| **PCI DSS** | 카드 결제 데이터 보호 | 결제 처리 기업 | 카드 데이터 보안 정책 |

#### 2. 보안 정책 수립 프로세스 다이어그램

```text
<<< 보안 정책 수립 및 관리 수명주기 >>>

  ┌──────────────────────────────────────────────────────────────────────┐
  │                    Phase 1: 계획 (Plan)                              │
  │  ┌────────────────────────────────────────────────────────────────┐ │
  │  │  1.1 경영진 승인 획득 (Executive Sponsorship)                   │ │
  │  │  1.2 정책 수립 팀 구성 (Policy Team Formation)                  │ │
  │  │  1.3 법적/규제 요구사항 분석 (Legal/Regulatory Analysis)        │ │
  │  │  1.4 현황 분석 (Gap Analysis)                                   │ │
  │  │  1.5 위험 평가 연계 (Risk Assessment Alignment)                 │ │
  │  └────────────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │                    Phase 2: 개발 (Develop)                           │
  │  ┌────────────────────────────────────────────────────────────────┐ │
  │  │  2.1 정책 초안 작성 (Policy Drafting)                           │ │
  │  │      - 목적, 범위, 역할/책임, 준수 요건 정의                    │ │
  │  │  2.2 이해관계자 검토 (Stakeholder Review)                        │ │
  │  │      - 법무, IT, HR, 사업부서 협의                               │ │
  │  │  2.3 법적 검토 (Legal Review)                                   │ │
  │  │  2.4 수정 및 보완 (Revision)                                    │ │
  │  └────────────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │                    Phase 3: 승인 (Approve)                           │
  │  ┌────────────────────────────────────────────────────────────────┐ │
  │  │  3.1 경영진 승인 (Executive Approval)                           │ │
  │  │  3.2 이사회 보고 (Board Reporting) - 중요 정책                   │ │
  │  │  3.3 공식 발효 (Official Enforcement)                           │ │
  │  │  3.4 버전 관리 (Version Control)                                │ │
  │  └────────────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │                    Phase 4: 구현 (Implement)                         │
  │  ┌────────────────────────────────────────────────────────────────┐ │
  │  │  4.1 교육 및 인지 (Awareness Training)                          │ │
  │  │  4.2 기술적 통제 구현 (Technical Controls)                       │ │
  │  │  4.3 절차 문서 배포 (Procedure Distribution)                    │ │
  │  │  4.4 모니터링 체계 구축 (Monitoring Setup)                       │ │
  │  └────────────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │                    Phase 5: 운영 및 개선 (Operate & Improve)         │
  │  ┌────────────────────────────────────────────────────────────────┐ │
  │  │  5.1 정기 검토 (Annual Review)                                  │ │
  │  │  5.2 준수 모니터링 (Compliance Monitoring)                       │ │
  │  │  5.3 위반 대응 (Violation Response)                             │ │
  │  │  5.4 지속 개선 (Continuous Improvement)                         │ │
  │  └────────────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────────────┘
```

#### 3. 핵심 보안 정책 유형 및 내용

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime, timedelta

class PolicyType(Enum):
    """보안 정책 유형"""
    INFORMATION_SECURITY = "정보보안 정책"      # 최상위 정책
    ACCEPTABLE_USE = "승인된 사용 정책"         # IT 자원 사용
    ACCESS_CONTROL = "접근통제 정책"            # 시스템 접근
    DATA_CLASSIFICATION = "데이터 분류 정책"     # 데이터 보호
    INCIDENT_RESPONSE = "보안사고 대응 정책"     # 사고 처리
    BUSINESS_CONTINUITY = "업무연속성 정책"      # 재해 복구
    VENDOR_MANAGEMENT = "공급업체 관리 정책"     # 제3자 관리
    PRIVACY = "개인정보보호 정책"               # 개인정보
    CRYPTOGRAPHY = "암호화 정책"                # 암호화 표준
    REMOTE_WORK = "원격근무 정책"               # 재택근무

class PolicyStatus(Enum):
    """정책 상태"""
    DRAFT = "초안"
    REVIEW = "검토중"
    APPROVED = "승인됨"
    ACTIVE = "시행중"
    DEPRECATED = "폐기예정"
    ARCHIVED = "보관됨"

@dataclass
class PolicyVersion:
    """정책 버전 정보"""
    version: str
    effective_date: datetime
    expiry_date: Optional[datetime] = None
    changes: str = ""
    approver: str = ""

@dataclass
class SecurityPolicy:
    """보안 정책 클래스"""
    policy_id: str
    title: str
    policy_type: PolicyType
    status: PolicyStatus
    purpose: str
    scope: str
    roles_responsibilities: Dict[str, str]
    compliance_requirements: List[str]
    versions: List[PolicyVersion] = field(default_factory=list)
    exceptions: List[Dict] = field(default_factory=list)
    violations: List[Dict] = field(default_factory=list)

    def add_version(self, version: PolicyVersion):
        """새 버전 추가"""
        # 이전 버전 만료
        if self.versions:
            self.versions[-1].expiry_date = version.effective_date
        self.versions.append(version)

    def request_exception(self, requester: str, reason: str,
                          duration: timedelta) -> Dict:
        """예외 요청"""
        exception = {
            'id': f"EXC-{len(self.exceptions)+1:04d}",
            'requester': requester,
            'reason': reason,
            'start_date': datetime.now(),
            'end_date': datetime.now() + duration,
            'status': 'pending',
            'approver': None
        }
        self.exceptions.append(exception)
        return exception

    def approve_exception(self, exception_id: str, approver: str):
        """예외 승인"""
        for exc in self.exceptions:
            if exc['id'] == exception_id:
                exc['status'] = 'approved'
                exc['approver'] = approver
                return True
        return False

    def record_violation(self, violator: str, description: str,
                         severity: str) -> Dict:
        """위반 기록"""
        violation = {
            'id': f"VIO-{len(self.violations)+1:04d}",
            'violator': violator,
            'description': description,
            'severity': severity,
            'date': datetime.now(),
            'action_taken': None,
            'status': 'open'
        }
        self.violations.append(violation)
        return violation

    def get_compliance_score(self) -> float:
        """준수 점수 계산 (0-100)"""
        if not self.violations:
            return 100.0

        # 심각도별 가중치
        severity_weights = {
            'critical': 30,
            'high': 20,
            'medium': 10,
            'low': 5
        }

        # 미해결 위반 건수 기준
        open_violations = [v for v in self.violations if v['status'] == 'open']
        penalty = sum(severity_weights.get(v['severity'], 5) for v in open_violations)

        return max(0, 100 - penalty)

    def is_due_for_review(self) -> bool:
        """정기 검토 필요 여부"""
        if not self.versions:
            return True

        last_version = self.versions[-1]
        review_period = timedelta(days=365)  # 1년

        return datetime.now() - last_version.effective_date > review_period


class PolicyManager:
    """보안 정책 관리자"""

    def __init__(self):
        self.policies: Dict[str, SecurityPolicy] = {}

    def create_policy(self, policy: SecurityPolicy):
        """정책 생성"""
        self.policies[policy.policy_id] = policy

    def get_policy(self, policy_id: str) -> Optional[SecurityPolicy]:
        """정책 조회"""
        return self.policies.get(policy_id)

    def get_all_policies(self) -> List[SecurityPolicy]:
        """모든 정책 조회"""
        return list(self.policies.values())

    def get_policies_by_type(self, policy_type: PolicyType) -> List[SecurityPolicy]:
        """유형별 정책 조회"""
        return [p for p in self.policies.values() if p.policy_type == policy_type]

    def get_policies_for_review(self) -> List[SecurityPolicy]:
        """검토 필요 정책 목록"""
        return [p for p in self.policies.values() if p.is_due_for_review()]

    def generate_compliance_report(self) -> Dict:
        """준수 현황 보고서 생성"""
        report = {
            'generated_at': datetime.now(),
            'total_policies': len(self.policies),
            'by_type': {},
            'by_status': {},
            'avg_compliance_score': 0,
            'policies_for_review': 0,
            'open_violations': 0,
            'active_exceptions': 0
        }

        total_score = 0
        for policy in self.policies.values():
            # 유형별 집계
            type_name = policy.policy_type.value
            report['by_type'][type_name] = report['by_type'].get(type_name, 0) + 1

            # 상태별 집계
            status_name = policy.status.value
            report['by_status'][status_name] = report['by_status'].get(status_name, 0) + 1

            # 준수 점수
            total_score += policy.get_compliance_score()

            # 검토 필요
            if policy.is_due_for_review():
                report['policies_for_review'] += 1

            # 미해결 위반
            report['open_violations'] += len([v for v in policy.violations if v['status'] == 'open'])

            # 활성 예외
            now = datetime.now()
            report['active_exceptions'] += len([
                e for e in policy.exceptions
                if e['status'] == 'approved' and e['end_date'] > now
            ])

        report['avg_compliance_score'] = total_score / len(self.policies) if self.policies else 0

        return report


# 사용 예시
if __name__ == "__main__":
    # 정책 관리자 생성
    manager = PolicyManager()

    # 정보보안 정책 생성
    infosec_policy = SecurityPolicy(
        policy_id="POL-IS-001",
        title="정보보안 기본 정책",
        policy_type=PolicyType.INFORMATION_SECURITY,
        status=PolicyStatus.ACTIVE,
        purpose="조직의 정보 자산을 보호하고 법적/규제 요건을 준수하기 위함",
        scope="전 임직원, 협력업체, 모든 정보 시스템 및 데이터",
        roles_responsibilities={
            "CISO": "정보보안 정책 수립 및 총괄",
            "보안팀": "정책 구현 및 모니터링",
            "IT팀": "기술적 통제 구현",
            "전 직원": "정책 준수 및 위반 신고"
        },
        compliance_requirements=[
            "개인정보보호법",
            "정보통신망법",
            "ISO 27001",
            "ISMS-P"
        ]
    )

    # 버전 추가
    infosec_policy.add_version(PolicyVersion(
        version="2.0",
        effective_date=datetime(2026, 1, 1),
        changes="Zero Trust 원칙 추가, 클라우드 보안 요건 강화",
        approver="CEO"
    ))

    # 정책 등록
    manager.create_policy(infosec_policy)

    # 예외 요청
    exception = infosec_policy.request_exception(
        requester="영업팀 김대리",
        reason="고객 미팅을 위한 출장 중 개인 기기 사용",
        duration=timedelta(days=7)
    )
    print(f"예외 요청: {exception['id']}")

    # 예외 승인
    infosec_policy.approve_exception(exception['id'], "CISO")
    print(f"예외 승인 완료")

    # 위반 기록
    violation = infosec_policy.record_violation(
        violator="개발팀 박사원",
        description="무단으로 소스코드를 외부 저장소에 업로드",
        severity="high"
    )
    print(f"위반 기록: {violation['id']}")

    # 준수 현황 보고서
    report = manager.generate_compliance_report()
    print(f"\n=== 보안 정책 준수 현황 ===")
    print(f"총 정책 수: {report['total_policies']}")
    print(f"평균 준수 점수: {report['avg_compliance_score']:.1f}")
    print(f"검토 필요 정책: {report['policies_for_review']}")
    print(f"미해결 위반: {report['open_violations']}")
    print(f"활성 예외: {report['active_exceptions']}")
```

#### 4. 핵심 보안 정책 매트릭스

| 정책명 | 목적 | 주요 대상 | 핵심 요건 | 검토 주기 |
|:---|:---|:---|:---|:---|
| 정보보안 정책 | 최상위 보안 원칙 | 전 조직 | CIA 보장, 법적 준수 | 연 1회 |
| 접근통제 정책 | 무단 접근 방지 | IT 시스템 | 최소권한, 직무분리 | 연 1회 |
| 데이터 분류 정책 | 데이터 보호 수준 결정 | 모든 데이터 | 4단계 분류, 라벨링 | 연 1회 |
| 암호화 정책 | 기밀성 보장 | 민감 데이터 | AES-256, TLS 1.3 | 반기 1회 |
| 인시던트 대응 정책 | 사고 대응 체계 | 보안팀 | 4시간 내 보고, 24시간 내 대응 | 연 2회 |
| 공급업체 관리 정책 | 제3자 위험 관리 | 협력업체 | 보안 평가, 계약 내 보안 조항 | 연 1회 |
| 원격근무 정책 | 재택근무 보안 | 원격 근무자 | VPN, MFA, 업무용 기기 | 반기 1회 |

---

### III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 국내외 보안 정책 프레임워크 비교

| 프레임워크 | 국가/기관 | 핵심 특징 | 적용 분야 | 인증 여부 |
|:---|:---|:---|:---|:---|
| **ISO 27001** | 국제(ISO) | ISMS, PDCA | 전 산업 | 인증 |
| **NIST CSF** | 미국 | 5대 기능, Tiers | 연방기관, 민간 | 자체 인증 |
| **ISMS-P** | 한국 | 개인정보+정보보안 통합 | 주요 정보통신서비스 | 인증 |
| **PCI DSS** | 글로벌 | 카드 데이터 보호 | 결제 처리 | 인증 |
| **SOC 2** | 미국(AICPA) | 5대 신뢰원칙 | 서비스 조직 | 인증 |
| **FedRAMP** | 미국 | 클라우드 보안 | 연방 클라우드 | 인증 |

#### 2. 정책 수립 방법론 비교

| 방법론 | 접근 방식 | 장점 | 단점 | 적합한 조직 |
|:---|:---|:---|:---|:---|
| **Top-Down** | 경영진 주도 | 조직적 합의, 강제력 | 현장 저항 가능 | 대기업 |
| **Bottom-Up** | 현장 중심 | 실용적, 수용성 높음 | 전사 일관성 부족 | 중소기업 |
| **Risk-Based** | 위험 기반 | 우선순위 명확 | 위험 평가 복잡 | 금융, 공공 |
| **Compliance-Driven** | 규제 중심 | 법적 준수 보장 | 최소 요건만 충족 | 규제 산업 |
| **Maturity-Based** | 성숙도 기반 | 단계적 발전 | 시간 소요 | 성장 기업 |

#### 3. 과목 융합 관점 분석
- **네트워크 보안**: 네트워크 접근 정책, 방화벽 규칙, VPN 사용 정책
- **시스템 보안**: 시스템 접근 정책, 패치 관리 정책, 로그 관리 정책
- **애플리케이션 보안**: SDLC 보안 정책, 코드 리뷰 정책, 취약점 관리 정책
- **데이터베이스**: 데이터 분류 정책, 접근 통제 정책, 백업 정책
- **클라우드**: 클라우드 사용 정책, 책임 분담 모델, 데이터 주권 정책

---

### IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 스타트업 보안 정책 구축**
- 상황: 50인 규모 스타트업, 보안 정책 전무
- 판단: Risk-Based 접근으로 핵심 정책 우선 수립
- 핵심 정책: 정보보안 정책, 접근통제 정책, 데이터 분류 정책
- 구현: Notion 기반 정책 문서, Google Workspace 보안 설정

**시나리오 2: 금융사 GDPR 대응 정책 수립**
- 상황: 유럽 고객 보유, GDPR 준수 필요
- 판단: Compliance-Driven 접근으로 개인정보보호 정책 강화
- 핵심 정책: 개인정보보호 정책, 데이터 주권 정책, 동의 관리 정책
- 구현: DPO 지정, DPIA 프로세스, 데이터 주체 권리 보장

**시나리오 3: 제조업 IoT 보안 정책 수립**
- 상황: 스마트팩토리 구축, OT/IT 융합 보안 필요
- 판단: IEC 62443 기반 OT 보안 정책 수립
- 핵심 정책: OT 보안 정책, 펌웨어 관리 정책, 네트워크 분리 정책
- 구현: Purdue 모델 적용, NAC 도입, 보안 모니터링

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] 경영진 후원(Executive Sponsorship) 확보
- [ ] 법무팀, HR, IT, 사업부서 이해관계자 협의
- [ ] 기존 정책과의 충돌 여부 검토
- [ ] 적용 가능한 법적/규제 요구사항 식별
- [ ] 정책 교육 계획 수립
- [ ] 예외 처리 프로세스 정의
- [ ] 위반 시 제재 수준 합의
- [ ] 정기 검토 및 개선 프로세스 정의

#### 3. 안티패턴 (Anti-patterns)
- **"복사붙여넣기" 정책**: 타사 정책 무비판적 도입 → 실제 적용 불가
- **"서랍 속 정책"**: 문서만 있고 실제 적용 안 됨 → 준수 모니터링 필수
- **"과도한 정책"**: 모든 것을 규제 → 업무 마비, 직원 저항
- **"업데이트 안 되는 정책"**: 5년 전 정책 그대로 → 현실과 괴리

---

### V. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | 도입 전 | 도입 후 | 개선율 |
|:---|:---|:---|:---|
| 보안 사고 건수 | 연 20건 | 연 5건 | 75% 감소 |
| 정책 준수율 | 40% | 95% | 137% 증가 |
| 감사 지적사항 | 15건 | 2건 | 87% 감소 |
| 직원 보안 인식 | 50점 | 85점 | 70% 향상 |
| 컴플라이언스 비용 | 5억원 | 2억원 | 60% 절감 |

#### 2. 미래 전망 및 진화 방향
- **AI 기반 정책 관리**: 자동 준수 모니터링, 위반 예측
- **실시간 적응형 정책**: 상황에 따른 동적 정책 조정
- **Zero Trust 정책**: "절대 신뢰 없음" 원칙의 정책화
- **개인정보 중심 설계**: Privacy by Design 정책 통합
- **공급망 보안 정책**: SBOM, 공급업체 보안 평가 의무화

#### 3. 참고 표준/가이드
- **ISO/IEC 27001**: 정보보안 관리 체계 - 정책 요구사항
- **ISO/IEC 27002**: 보안 통제 - 정책 구현 지침
- **NIST SP 800-53**: 보안 통제 - 정책 관련 통제
- **개인정보보호법**: 개인정보 처리 방침 의무
- **정보통신망법**: 정보통신망 보안 조치 의무

---

### 관련 개념 맵 (Knowledge Graph)
- [CIA 3요소](@/studynotes/09_security/01_policy/cia_triad.md) : 보안 정책의 핵심 목표 정의
- [위험 관리](@/studynotes/09_security/01_policy/risk_management.md) : 위험 기반 정책 수립
- [심층 방어](@/studynotes/09_security/01_policy/defense_in_depth.md) : 다층 보안 통제 정책
- [ISO 27001](@/studynotes/09_security/01_policy/isms_p.md) : 국제 보안 관리 체계 표준
- [보안 아키텍처](@/studynotes/09_security/01_policy/security_architecture.md) : 정책의 기술적 구현

---

### 어린이를 위한 3줄 비유 설명
1. **규칙의 책**: 학교에 규칙이 있듯이, 회사에도 지켜야 할 규칙이 있어요. "남의 물건에 손대지 않기"처럼 정보도 지키는 규칙이에요.
2. **약속의 문서**: 가족끼리 약속을 정해놓면 지키기 쉽죠? 회사도 모두가 지킬 수 있게 문서로 정해두는 거예요.
3. **지킴이의 도구**: 경찰관이 법을 지키듯, 보안 정책은 회사의 모든 사람이 정보를 지키도록 도와주는 도구예요.
