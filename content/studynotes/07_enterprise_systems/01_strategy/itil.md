+++
title = "ITIL (IT Infrastructure Library)"
date = "2026-03-04"
[extra]
categories = "studynotes-enterprise"
++-

# ITIL (IT Infrastructure Library)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: IT 서비스를 비즈니스 요구에 맞게 설계, 전달, 운영, 개선하는 **글로벌 IT 서비스 관리(ITSM) 베스트 프랙티스 프레임워크**입니다.
> 2. **가치**: IT 서비스 품질 향상, SLA 달성, 고객 만족도 증대, IT 운영 비용 절감을 통해 IT가 진정한 비즈니스 파트너로 거듭나게 합니다.
> 3. **융합**: ITIL 4는 Agile, DevOps, Lean, 클라우드 네이티브 등 현대적 IT 관리 방법론과 통합되어 디지털 트랜스포메이션을 지원합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. ITIL의 개념 및 철학적 근간
ITIL(Information Technology Infrastructure Library)은 영국 정부의 CCTA(Central Computer and Telecommunications Agency)에서 개발된 IT 서비스 관리(ITSM, IT Service Management)를 위한 프레임워크입니다. ITIL의 핵심 철학은 **"IT를 서비스(Service)의 관점에서 관리하고, 이 서비스가 비즈니스 가치(Value)를 창출하도록 보장하는 것"**입니다. ITIL은 IT를 단순한 기술 인프라가 아닌, 고객(비즈니스)에게 가치를 제공하는 '서비스'로 재정의함으로써 IT 조직의 패러다임을 근본적으로 변화시켰습니다. 최신 버전인 ITIL 4는 서비스 가치 시스템(SVS, Service Value System)을 도입하여 Agile, DevOps, Lean 등 현대적 방법론과의 통합을 실현했습니다.

#### 2. 💡 비유를 통한 이해: 레스토랑의 서비스 체계
IT 서비스를 레스토랑에 비유하면, IT 인프라(서버, 네트워크)는 주방의 조리 도구이고, IT 직원은 요리사와 서빙 직원입니다. 고객은 조리 도구가 아니라 맛있는 요리(서비스)를 주문합니다. **ITIL은 '고객이 만족하는 요리를 일관되게 제공하기 위한 레스토랑 운영 매뉴얼'입니다.** 주문을 받는 방법(서비스 데스크), 요리를 만드는 방법(서비스 설계), 불평을 처리하는 방법(인시던트 관리), 메뉴를 개선하는 방법(지속적 개선)이 모두 체계화되어 있습니다.

#### 3. 등장 배경 및 발전 과정
- **1980년대 후반 ITIL v1**: 영국 정부의 IT 서비스 효율화를 위한 가이드라인으로 시작 (30여 권의 서적)
- **2000~2001년 ITIL v2**: 서비스 지원(Service Support)과 서비스 제공(Service Delivery) 중심으로 체계화
- **2007년 ITIL v3**: 서비스 수명주기(Lifecycle) 개념 도입 (전략-설계-전환-운영-개선)
- **2011년 ITIL 2011**: v3의 개정판, 프로세스 정교화
- **2019년 ITIL 4**: 서비스 가치 시스템(SVS), 4차원 모델, 34개 프랙티스, Agile/DevOps 통합

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. ITIL 4 서비스 가치 시스템 (SVS) 구성요소

| 구성요소 | 정의 및 역할 | 상세 내용 |
| :--- | :--- | :--- |
| **입력 (Input)** | 기회(Oportunity)와 수요(Demand) | 비즈니스 기회, 고객 요구사항 |
| **조직 (Organizations & People)** | 조직 구조, 문화, 역량 | IT 팀 구성, 스킬, 리더십 |
| **정보 및 기술 (Information & Technology)** | 지식, 데이터, 시스템 | CMDB, 서비스 포털, 모니터링 도구 |
| **파트너 및 공급자 (Partners & Suppliers)** | 외부 협력 관계 | 아웃소싱, 클라우드 벤더, 컨설팅 |
| **가치 스트림 및 프로세스 (Value Streams & Processes)** | 가치 창출 활동 체계 | 서비스 가치 스트림, 34개 프랙티스 |
| **결과 (Output)** | 가치(Value) | 비즈니스 목표 달성, 고객 만족 |

#### 2. ITIL 4 서비스 가치 체인 (Service Value Chain) 다이어그램

```text
                          ┌─────────────────────────────────────┐
                          │      [ OPPORTUNITY & DEMAND ]       │
                          │         (기회 및 수요)               │
                          └───────────────┬─────────────────────┘
                                          │
    ┌─────────────────────────────────────▼─────────────────────────────────────┐
    │                     SERVICE VALUE CHAIN (서비스 가치 체인)                  │
    │  ┌─────────────────────────────────────────────────────────────────────┐   │
    │  │                                                                     │   │
    │  │   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    │   │
    │  │   │  PLAN    │───▶│  IMPROVE │───▶│ ENGAGE   │───▶│DESIGN &  │    │   │
    │  │   │  (계획)  │    │  (개선)  │    │ (참여)   │    │TRANSITION│    │   │
    │  │   │          │    │          │    │          │    │(설계/전환)│    │   │
    │  │   └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘    │   │
    │  │        │               │               │               │          │   │
    │  │        │               │               │               ▼          │   │
    │  │        │               │               │        ┌──────────┐      │   │
    │  │        │               │               └───────▶│OBTAIN /  │      │   │
    │  │        │               │                        │ BUILD    │      │   │
    │  │        │               │                        │(획득/구축)│      │   │
    │  │        │               │                        └────┬─────┘      │   │
    │  │        │               │                             │            │   │
    │  │        │               │                             ▼            │   │
    │  │        │               │                       ┌──────────┐       │   │
    │  │        └───────────────┴──────────────────────▶│DELIVER & │       │   │
    │  │                                                  │SUPPORT   │       │   │
    │  │                                                  │(전달/지원)│       │   │
    │  │                                                  └──────────┘       │   │
    │  │                                                                     │   │
    │  └─────────────────────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────┬───────────────────────────────────────┘
                                          │
                          ┌───────────────▼─────────────────────┐
                          │          [ VALUE ]                  │
                          │      (가치 - 제품/서비스)            │
                          └─────────────────────────────────────┘
```

#### 3. ITIL 4의 34개 프랙티스 (Practices) 분류
ITIL 4는 34개의 프랙티스를 세 가지 카테고리로 분류합니다.

**[일반 관리 프랙티스 (General Management Practices) - 14개]**
| 프랙티스 | 핵심 목적 |
| :--- | :--- |
| Architecture Management | 조직의 아키텍처 제어 및 계획 |
| Continual Improvement | 서비스의 지속적 개선 |
| Information Security Management | 정보보호 보장 |
| Knowledge Management | 지식의 수집, 공유, 활용 |
| Measurement & Reporting | 성과 측정 및 보고 |
| Organizational Change Management | 조직 변화 관리 |
| Portfolio Management | 서비스 포트폴리오 관리 |
| Project Management | 프로젝트 계획 및 실행 |
| Relationship Management | 이해관계자 관계 유지 |
| Risk Management | 위험 식별 및 관리 |
| Service Financial Management | IT 재무 관리 |
| Strategy Management | IT 전략 수립 |
| Supplier Management | 공급자 관리 |
| Workforce & Talent Management | 인력 및 재능 관리 |

**[서비스 관리 프랙티스 (Service Management Practices) - 18개]**
| 프랙티스 | 핵심 목적 |
| :--- | :--- |
| Availability Management | 서비스 가용성 보장 |
| Business Analysis | 비즈니스 요구 분석 |
| Capacity & Performance Management | 용량 및 성능 관리 |
| Change Control | 변경 통제 |
| Change Enablement | 변경 활성화 (Agile 환경) |
| Deployment Management | 배포 관리 |
| Design & Transition | 설계 및 전환 |
| Incident Management | 인시던트 신속 복구 |
| IT Asset Management | IT 자산 관리 |
| Monitoring & Event Management | 모니터링 및 이벤트 관리 |
| Problem Management | 근본 원인 해결 |
| Release Management | 릴리스 관리 |
| Service Catalog Management | 서비스 카탈로그 관리 |
| Service Configuration Management | 서비스 구성 관리 |
| Service Continuity Management | 서비스 연속성 관리 |
| Service Design | 서비스 설계 |
| Service Desk | 서비스 데스크 (SPOC) |
| Service Level Management | SLA 관리 |
| Service Request Management | 서비스 요청 처리 |
| Service Validation & Testing | 서비스 검증 및 테스트 |

**[기술 관리 프랙티스 (Technical Management Practices) - 3개]**
| 프랙티스 | 핵심 목적 |
| :--- | :--- |
| Deployment Management | 배포 자동화 |
| Infrastructure & Platform Management | 인프라/플랫폼 관리 |
| Software Development & Management | 소프트웨어 개발 관리 |

#### 4. 인시던트 관리 프로세스 상세 및 Python 시뮬레이션

```python
from enum import Enum
from datetime import datetime, timedelta
from dataclasses import dataclass

class Priority(Enum):
    CRITICAL = 1  # 비즈니스 중단, 즉시 대응
    HIGH = 2      # 주요 기능 저하, 4시간 내 대응
    MEDIUM = 3    # 부분적 영향, 8시간 내 대응
    LOW = 4       # 경미한 영향, 24시간 내 대응

@dataclass
class Incident:
    id: str
    title: str
    description: str
    priority: Priority
    impact: str
    urgency: str
    created_at: datetime
    resolved_at: datetime = None
    assigned_to: str = None
    status: str = "New"

class IncidentManager:
    """ITIL 기반 인시던트 관리 시스템"""

    SLA_TARGETS = {
        Priority.CRITICAL: timedelta(hours=1),
        Priority.HIGH: timedelta(hours=4),
        Priority.MEDIUM: timedelta(hours=8),
        Priority.LOW: timedelta(hours=24)
    }

    def __init__(self):
        self.incidents = []
        self.resolution_patterns = {}

    def create_incident(self, title, description, impact, urgency):
        """인시던트 생성 및 우선순위 산정"""
        # 우선순위 매트릭스 (Impact x Urgency)
        priority_matrix = {
            ("High", "High"): Priority.CRITICAL,
            ("High", "Medium"): Priority.HIGH,
            ("High", "Low"): Priority.MEDIUM,
            ("Medium", "High"): Priority.HIGH,
            ("Medium", "Medium"): Priority.MEDIUM,
            ("Medium", "Low"): Priority.LOW,
            ("Low", "High"): Priority.MEDIUM,
            ("Low", "Medium"): Priority.LOW,
            ("Low", "Low"): Priority.LOW,
        }

        priority = priority_matrix.get((impact, urgency), Priority.MEDIUM)
        incident_id = f"INC-{len(self.incidents)+1:05d}"

        incident = Incident(
            id=incident_id,
            title=title,
            description=description,
            priority=priority,
            impact=impact,
            urgency=urgency,
            created_at=datetime.now()
        )
        self.incidents.append(incident)
        return incident

    def check_sla_breach(self, incident):
        """SLA 위반 여부 확인"""
        if incident.resolved_at:
            resolution_time = incident.resolved_at - incident.created_at
        else:
            resolution_time = datetime.now() - incident.created_at

        target = self.SLA_TARGETS[incident.priority]
        return resolution_time > target

    def generate_sla_report(self):
        """SLA 준수 현황 보고서"""
        total = len(self.incidents)
        breached = sum(1 for inc in self.incidents if self.check_sla_breach(inc))

        return {
            "total_incidents": total,
            "sla_breaches": breached,
            "sla_compliance_rate": (total - breached) / total * 100 if total > 0 else 0,
            "by_priority": {
                p.name: {
                    "count": sum(1 for i in self.incidents if i.priority == p),
                    "breached": sum(1 for i in self.incidents
                                    if i.priority == p and self.check_sla_breach(i))
                }
                for p in Priority
            }
        }

# 실행 예시
manager = IncidentManager()

# 인시던트 생성 예시
inc1 = manager.create_incident(
    title="ERP 시스템 접속 불가",
    description="전사적으로 ERP 접속이 되지 않음",
    impact="High",
    urgency="High"
)
inc1.assigned_to = "IT Support Team A"
inc1.resolved_at = datetime.now() + timedelta(minutes=45)

inc2 = manager.create_incident(
    title="프린터 용지 걸림",
    description="3층 프린터에서 용지가 걸림",
    impact="Low",
    urgency="Low"
)

# SLA 보고서 생성
report = manager.generate_sla_report()
print("=== 인시던트 관리 SLA 보고서 ===")
print(f"총 인시던트: {report['total_incidents']}")
print(f"SLA 준수율: {report['sla_compliance_rate']:.1f}%")
for priority, stats in report['by_priority'].items():
    if stats['count'] > 0:
        print(f"  {priority}: {stats['count']}건 (위반: {stats['breached']}건)")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. ITSM 프레임워크 비교 분석

| 특성 | ITIL 4 | COBIT 2019 | ISO 20000 | DevOps |
| :--- | :--- | :--- | :--- | :--- |
| **주요 초점** | IT 서비스 관리 | IT 거버넌스 | ITSM 인증 | 소프트웨어 전달 |
| **프로세스 수** | 34개 프랙티스 | 40개 프로세스 | 24개 프로세스 | 8가지 원칙 |
| **성격** | 베스트 프랙티스 | 통제 프레임워크 | 국제 표준 | 문화/방법론 |
| **인증** | ITIL 4 Foundation 등 | COBIT 5/2019 | ISO 20000 인증 | DevOps Institute |
| **Agile 지원** | 높음 (ITIL 4) | 중간 | 낮음 | 높음 |

#### 2. 과목 융합 관점 분석
- **소프트웨어 공학 (DevOps & Agile)**: ITIL 4는 DevOps, Agile, Lean과의 통합을 명시적으로 지원합니다. 변경 관리(Change Enablement)는 Agile의 지속적 전달(Continuous Delivery)과 조화됩니다.
- **정보보안 (Security Operations)**: ITIL의 인시던트 관리, 문제 관리, 변경 관리는 보안 운영(SecOps)과 밀접하게 연동됩니다. 보안 이벤트는 특수한 인시던트로 처리됩니다.
- **클라우드 컴퓨팅 (Cloud Service Management)**: SaaS, IaaS 등 클라우드 서비스의 SLA 관리, 공급자 관리(Supplier Management)가 ITIL의 핵심 영역으로 부상했습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단: ITSM 도구 선정 시나리오
**[상황]** D기업은 기존의 엑셀과 이메일 기반 IT 지원 체계에서 ITSM 도구 도입을 검토 중입니다. ITIL 4 기반의 서비스 데스크 구축이 목표입니다.

**[전략적 대응 방안]**
1. **요구사항 정의**: ITIL 4의 핵심 프랙티스(인시던트, 문제, 변경, 자산, 서비스 카탈로그) 지원 여부 검토
2. **도구 평가 매트릭스**:

| 평가 항목 | ServiceNow | Jira Service Management | Freshservice | BMC Helix |
| :--- | :--- | :--- | :--- | :--- |
| ITIL 4 준수 | 완벽 | 양호 | 양호 | 완벽 |
| 클라우드/SaaS | 지원 | 지원 | 지원 | 지원 |
| AI/자동화 | 강력 | 중간 | 기본 | 강력 |
| 가격 | 높음 | 중간 | 낮음 | 높음 |
| 커스터마이징 | 높음 | 높음 | 중간 | 높음 |

3. **Pilot 구축**: 3개월간 한 부서에 파일럿 적용 후 전사 확대

#### 2. 도입 시 고려사항 (Checklist)
- **프로세스 선행**: 도구보다 프로세스 정의가 먼저입니다. "도구가 프로세스를 만든다"는 오류를 피해야 합니다.
- **KPI 설정**: First Call Resolution(FCR), Mean Time to Resolve(MTTR), SLA 준수율 등 측정 가능한 지표 설정
- **통합성**: CMDB, 모니터링 도구, AD/LDAP와의 통합 고려

#### 3. 안티패턴 (Anti-patterns)
- **"ITIL은 관료주의다"**: ITIL을 따르느라 너무 많은 승인 단계를 만들어 Agile을 저해하는 경우
- **도구 중심 도입**: 프로세스 없이 도구만 도입하여 현업의 혼란 가중

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 개선 항목 | ITIL 도입 시 기대효과 |
| :--- | :--- | :--- |
| **서비스 품질** | SLA 준수율 | 85% → 98% 향상 |
| **운영 효율** | 인시던트 해결 시간(MTTR) | 40% 단축 |
| **고객 만족** | IT 서비스 만족도 | 20% 이상 향상 |
| **비용 효율** | IT 운영 비용 | 15~25% 절감 |

#### 2. 미래 전망: AI 기반 ITSM
- **AIOps (AI for IT Operations)**: AI가 인시던트를 자동 분류하고, 루트 코즈를 예측하며, 자동 복구를 수행하는 'Autonomous ITSM'로 진화
- **Chatbot & Virtual Agent**: 서비스 데스크의 1차 응대를 AI 챗봇이 담당, 24/7 서비스 제공
- **Predictive Analytics**: 장애 발생을 예측하여 사전 예방적(Proactive) 서비스 관리

#### 3. 참고 표준 및 가이드라인
- **ITIL 4 Foundation (Axelos)**
- **ISO/IEC 20000-1:2018** - IT Service Management
- **ITIL 4 Practice Guides**

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [COBIT (Control Objectives for Information and related Technology)](@/studynotes/07_enterprise_systems/01_strategy/cobit.md): ITIL의 거버넌스 상위 프레임워크
- [SLA (Service Level Agreement)](@/studynotes/07_enterprise_systems/01_strategy/sla.md): ITIL 서비스 수준 관리의 핵심 산출물
- [서비스 데스크 (Service Desk)](@/studynotes/07_enterprise_systems/01_strategy/service_desk.md): ITIL의 고객 접점 조직
- [인시던트 관리 (Incident Management)](@/studynotes/07_enterprise_systems/01_strategy/incident_management.md): ITIL의 핵심 운영 프로세스
- [DevOps](@/studynotes/06_ict_convergence/02_devops/devops.md): ITIL 4와 통합된 현대적 IT 관리 방법론

---

### 👶 어린이를 위한 3줄 비유 설명
1. ITIL은 학교에서 선생님이 학생들을 도와주는 '도움 요청 센터'를 잘 운영하기 위한 방법책과 같아요.
2. "숙제를 모르겠어요"라고 말하면 선생님이 빨리 도와주고, 자주 생기는 어려움은 미리 알려서 예방하는 것처럼, ITIL은 컴퓨터 문제를 빠르고 친절하게 해결해 준답니다.
3. 이 방법책 덕분에 누구나 언제든 도움을 받을 수 있고, 학교 컴퓨터가 항상 잘 작동하게 할 수 있어요!
