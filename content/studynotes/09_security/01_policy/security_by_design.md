+++
title = "내재적 보안 (Security by Design)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# 내재적 보안 (Security by Design)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Security by Design은 소프트웨어/시스템 개발의 초기 요구사항 단계부터 보안을 내재화시켜, 사후 보안(Bolt-on Security)의 비용과 취약점을 근원적으로 해결하는 보안 엔지니어링 철학입니다.
> 2. **가치**: 보안 취약점의 70%는 설계 단계에서 발생하며, Security by Design은 개발 수명주기 전 단계에서 비용 대비 100배 이상의 효과를 창출합니다 (NIST 연구).
> 3. **융합**: Microsoft SDL, OWASP SAMM, NIST SSDF와 결합하여 DevSecOps의 이론적 기반을 제공하며, Privacy by Design, Safety by Design과 함께 Trustworthy Software의 3대 축을 이룹니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**Security by Design(SbD, 내재적 보안)**은 시스템과 소프트웨어를 설계할 때부터 보안 요구사항을 핵심 설계 원칙으로 통합하는 개발 방법론입니다. 이는 보안을 개발 완료 후 추가하는 "사후 보안(Bolt-on Security)"과 대조되는 접근법입니다.

**핵심 원칙 (7대 원칙)**:
1. **Defense in Depth**: 다층 방어 체계
2. **Fail Secure**: 실패 시 안전한 상태로 전환
3. **Least Privilege**: 최소 권한 원칙
4. **Separation of Duties**: 직무 분리
5. **Defense in Depth**: 심층 방어
6. **Keep It Simple**: 단순성 유지
7. **Zero Trust**: 기본 불신

**비교: Bolt-on Security vs Security by Design**

| 구분 | Bolt-on Security | Security by Design |
|:---|:---|:---|
| **보안 적용 시점** | 개발 후, 배포 전 | 요구사항~설계 단계 |
| **보안 담당** | 보안팀 전담 | 개발팀 + 보안팀 협업 |
| **취약점 수정 비용** | 높음 (10~100배) | 낮음 (설계 단계) |
| **보안 인식** | 귀찮은 장애물 | 핵심 품질 속성 |
| **자동화 수준** | 낮음 (수동 점검) | 높음 (CI/CD 통합) |

#### 2. 비유를 통한 이해
Security by Design은 **'자동차 안전 설계'**에 비유할 수 있습니다:

- **Bolt-on Security**: 차를 다 만든 후 안전벨트, 에어백을 나중에 붙임
  - 문제: 차체 구조가 충돌을 고려하지 않음, 추가 비용 발생

- **Security by Design**: 처음부터 충돌 테스트, 에어백, ABS를 설계에 반영
  - 장점: 차체가 충격을 흡수, 안전 시스템이 유기적으로 작동

#### 3. 등장 배경 및 발전 과정
1. **1960~70년대**: 보안은 물리적 접근 통제 중심
2. **1980년대**: 소프트웨어 보안 개념 대두 (Orange Book, TCSEC)
3. **1990년대**: 웹 애플리케이션 보안 취약점 급증
4. **2002년**: Microsoft SDL(Security Development Lifecycle) 발표
5. **2004년**: OWASP Top 10 최초 발표
6. **2010년**: OWASP SAMM(Software Assurance Maturity Model)
7. **2016년**: NIST SP 800-160 (Systems Security Engineering)
8. **2022년**: NIST SSDF(Secure Software Development Framework)

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. Security by Design 프레임워크 구성

| 단계 | 활동 | 산출물 | 도구 |
|:---|:---|:---|:---|
| **요구사항** | 보안 요구사항 도출, ABUSE Cases | Security Requirements, Misuse Cases | Threat Modeling |
| **설계** | 위협 모델링, 보안 아키텍처 | Threat Model, Security Architecture | STRIDE, DFD |
| **구현** | 보안 코딩, 코드 리뷰 | Secure Code, SAST 결과 | SAST, SonarQube |
| **검증** | 보안 테스트, 침투 테스트 | DAST 결과, PenTest Report | DAST, Burp Suite |
| **배포** | 보안 설정, 컨테이너 보안 | Secure Config, IaC | IaC Scan, Trivy |
| **운영** | 모니터링, 대응 | Security Logs, Alerts | SIEM, EDR |

#### 2. SDL(Security Development Lifecycle) 아키텍처

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                    Security Development Lifecycle (SDL)                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   [교육] ──────────────────────────────────────────────────────►        │
│     │                                            ▲                      │
│     ▼                                            │                      │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐              │
│   │요구사항 │───►│ 설계    │───►│ 구현    │───►│ 검증    │              │
│   │(Training│    │(Design) │    │(Implement│   │(Verifica│              │
│   │        │    │         │    │ation)   │    │tion)   │              │
│   └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘              │
│        │              │              │              │                   │
│        │              │              │              │                   │
│   ┌────▼────┐    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐              │
│   │보안요건 │    │위협모델 │    │SAST/코드 │    │DAST/    │              │
│   │도출     │    │링       │    │리뷰      │    │PenTest  │              │
│   │         │    │         │    │          │    │         │              │
│   │Attack   │    │STRIDE/  │    │보안코딩  │    │Fuzzing  │              │
│   │Surface  │    │LINDDUN  │    │표준      │    │         │              │
│   │분석     │    │         │    │          │    │         │              │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘              │
│                                                                         │
│   ┌──────────────────────────────────────────────────────────┐          │
│   │                     보안 활동 (Continuous)                 │          │
│   ├──────────────────────────────────────────────────────────┤          │
│   │ • 보안 교육 (Core Training)                               │          │
│   │ • 취약점 관리 (Vulnerability Response)                    │          │
│   │ • 보안 인시던트 대응 (Incident Response)                  │          │
│   │ • 보안 메트릭 수집 (Metrics & Feedback)                   │          │
│   └──────────────────────────────────────────────────────────┘          │
│                                                                         │
│                              ▼                                          │
│   ┌──────────────────────────────────────────────────────────┐          │
│   │                     [ 릴리즈 (Release) ]                   │          │
│   │        Final Security Review (FSR) → 보안 승인            │          │
│   └──────────────────────────────────────────────────────────┘          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 3. 심층 동작 원리: 위협 모델링 (STRIDE)

```
① 시스템 모델링 (DFD 작성)
   ┌─ 외부 엔티티 (External Entity): 사용자, 외부 시스템
   ├─ 프로세스 (Process): 기능 단위
   ├─ 데이터 저장소 (Data Store): DB, 파일
   └─ 데이터 흐름 (Data Flow): 화살표

② 위협 식별 (STRIDE 적용)
   ┌─ Spoofing (스푸핑): 신원 위장
   │    예: 세션 탈취, 계정 도용
   ├─ Tampering (변조): 데이터 무단 수정
   │    예: SQL Injection, 파라미터 변조
   ├─ Repudiation (부인): 행위 부인
   │    예: 로그 미기록, 전자서명 없음
   ├─ Information Disclosure (정보 유출)
   │    예: 평문 저장, 약한 암호화
   ├─ Denial of Service (서비스 거부)
   │    예: 리소스 고갈, 입력 검증 없음
   └─ Elevation of Privilege (권한 상승)
        예: Insecure Direct Object Reference

③ 위협 우선순위 결정 (DREAD)
   ┌─ Damage: 피해 규모 (0~10)
   ├─ Reproducibility: 재현 가능성 (0~10)
   ├─ Exploitability: 악용 난이도 (0~10)
   ├─ Affected Users: 영향 사용자 수 (0~10)
   ├─ Discoverability: 발견 가능성 (0~10)
   └─ Score = (D+R+E+A+D) / 5

④ 대응 전략 수립
   ┌─ Eliminate: 위협 원천 제거
   ├─ Mitigate: 위협 완화 (기술적 통제)
   ├─ Transfer: 위험 전가 (보험, 아웃소싱)
   └─ Accept: 위험 수용 (낮은 영향)
```

#### 4. 핵심 알고리즘 & 실무 코드: 위협 모델링 자동화

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum
from datetime import datetime

class ThreatCategory(Enum):
    SPOOFING = "Spoofing"
    TAMPERING = "Tampering"
    REPUDIATION = "Repudiation"
    INFORMATION_DISCLOSURE = "Information Disclosure"
    DENIAL_OF_SERVICE = "Denial of Service"
    ELEVATION_OF_PRIVILEGE = "Elevation of Privilege"

class RiskLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class DFDComponent:
    """데이터 흐름 다이어그램 구성요소"""
    component_id: str
    name: str
    component_type: str  # external_entity, process, data_store, data_flow
    description: str
    trust_boundary: str  # internal, external, dmz

@dataclass
class Threat:
    """식별된 위협"""
    threat_id: str
    category: ThreatCategory
    title: str
    description: str
    affected_component: str
    dread_score: float
    risk_level: RiskLevel
    mitigation: str
    status: str = "open"

@dataclass
class DREADScore:
    """DREAD 위험 점수"""
    damage: int          # 0-10
    reproducibility: int # 0-10
    exploitability: int  # 0-10
    affected_users: int  # 0-10
    discoverability: int # 0-10

    def calculate(self) -> float:
        return (self.damage + self.reproducibility +
                self.exploitability + self.affected_users +
                self.discoverability) / 5

    def get_risk_level(self) -> RiskLevel:
        score = self.calculate()
        if score >= 9:
            return RiskLevel.CRITICAL
        elif score >= 7:
            return RiskLevel.HIGH
        elif score >= 5:
            return RiskLevel.MEDIUM
        elif score >= 3:
            return RiskLevel.LOW
        return RiskLevel.INFO

class ThreatModelingEngine:
    """위협 모델링 엔진"""

    def __init__(self):
        self.components: List[DFDComponent] = []
        self.threats: List[Threat] = []
        self.threat_counter = 0

    def add_component(self, component: DFDComponent):
        """DFD 구성요소 추가"""
        self.components.append(component)

    def analyze_component(self, component: DFDComponent) -> List[Threat]:
        """구성요소별 자동 위협 분석"""
        threats = []

        # 컴포넌트 유형별 기본 위협 템플릿
        threat_templates = self._get_threat_templates(component)

        for category, template in threat_templates.items():
            dread = self._calculate_dread(category, component)
            risk = dread.get_risk_level()

            threat = Threat(
                threat_id=self._generate_threat_id(),
                category=category,
                title=template["title"],
                description=template["description"].format(
                    component=component.name
                ),
                affected_component=component.component_id,
                dread_score=dread.calculate(),
                risk_level=risk,
                mitigation=template["mitigation"]
            )
            threats.append(threat)
            self.threats.append(threat)

        return threats

    def _get_threat_templates(
        self, component: DFDComponent
    ) -> Dict[ThreatCategory, Dict]:
        """컴포넌트 유형별 위협 템플릿"""
        templates = {
            ThreatCategory.SPOOFING: {
                "title": "신원 위장 가능성",
                "description": "{component}에 대한 인증 우회 또는 신원 위장 가능",
                "mitigation": "MFA 도입, 세션 관리 강화, 인증서 기반 인증"
            },
            ThreatCategory.TAMPERING: {
                "title": "데이터 변조 가능성",
                "description": "{component}의 데이터 무단 수정 가능",
                "mitigation": "입력 검증, 무결성 검사, 전자서명"
            },
            ThreatCategory.REPUDIATION: {
                "title": "부인 방지 미흡",
                "description": "{component}에서 사용자 행위 추적 불가",
                "mitigation": "감사 로그, 전자서명, 타임스탬프"
            },
            ThreatCategory.INFORMATION_DISCLOSURE: {
                "title": "정보 유출 가능성",
                "description": "{component}에서 민감 정보 노출 가능",
                "mitigation": "암호화, 접근 통제, 데이터 마스킹"
            },
            ThreatCategory.DENIAL_OF_SERVICE: {
                "title": "서비스 거부 가능성",
                "description": "{component} 가용성 저하 가능",
                "mitigation": "Rate Limiting, 리소스 제한, HA 설계"
            },
            ThreatCategory.ELEVATION_OF_PRIVILEGE: {
                "title": "권한 상승 가능성",
                "description": "{component}에서 권한 상승 공격 가능",
                "mitigation": "최소 권한, RBAC, 입력 검증"
            }
        }

        # 신뢰 경계 기반 위협 조정
        if component.trust_boundary == "external":
            # 외부 컴포넌트는 더 높은 위협
            pass  # DREAD 점수에서 반영

        return templates

    def _calculate_dread(
        self,
        category: ThreatCategory,
        component: DFDComponent
    ) -> DREADScore:
        """위협별 DREAD 점수 계산"""
        base_scores = {
            ThreatCategory.SPOOFING: DREADScore(8, 7, 6, 7, 8),
            ThreatCategory.TAMPERING: DREADScore(9, 6, 5, 6, 7),
            ThreatCategory.REPUDIATION: DREADScore(5, 5, 4, 4, 5),
            ThreatCategory.INFORMATION_DISCLOSURE: DREADScore(8, 7, 6, 8, 8),
            ThreatCategory.DENIAL_OF_SERVICE: DREADScore(6, 8, 7, 7, 9),
            ThreatCategory.ELEVATION_OF_PRIVILEGE: DREADScore(9, 6, 7, 7, 7)
        }

        score = base_scores.get(category, DREADScore(5, 5, 5, 5, 5))

        # 신뢰 경계 조정
        if component.trust_boundary == "external":
            score = DREADScore(
                min(score.damage + 1, 10),
                min(score.reproducibility + 1, 10),
                min(score.exploitability + 1, 10),
                score.affected_users,
                min(score.discoverability + 1, 10)
            )

        return score

    def _generate_threat_id(self) -> str:
        self.threat_counter += 1
        return f"TH-{self.threat_counter:04d}"

    def generate_report(self) -> Dict:
        """위협 모델링 보고서 생성"""
        by_category = {}
        by_risk = {}

        for threat in self.threats:
            # 카테고리별 집계
            cat = threat.category.value
            by_category[cat] = by_category.get(cat, 0) + 1

            # 위험도별 집계
            risk = threat.risk_level.value
            by_risk[risk] = by_risk.get(risk, 0) + 1

        return {
            "summary": {
                "total_components": len(self.components),
                "total_threats": len(self.threats),
                "by_category": by_category,
                "by_risk": by_risk
            },
            "components": [
                {
                    "id": c.component_id,
                    "name": c.name,
                    "type": c.component_type,
                    "boundary": c.trust_boundary
                }
                for c in self.components
            ],
            "threats": [
                {
                    "id": t.threat_id,
                    "category": t.category.value,
                    "title": t.title,
                    "dread_score": t.dread_score,
                    "risk_level": t.risk_level.value,
                    "mitigation": t.mitigation,
                    "status": t.status
                }
                for t in sorted(
                    self.threats,
                    key=lambda x: x.dread_score,
                    reverse=True
                )
            ]
        }

# 사용 예시
engine = ThreatModelingEngine()

# DFD 구성요소 정의
engine.add_component(DFDComponent(
    component_id="COMP-001",
    name="Web Application",
    component_type="process",
    description="메인 웹 애플리케이션",
    trust_boundary="dmz"
))

engine.add_component(DFDComponent(
    component_id="COMP-002",
    name="User Database",
    component_type="data_store",
    description="사용자 정보 저장소",
    trust_boundary="internal"
))

engine.add_component(DFDComponent(
    component_id="COMP-003",
    name="External API",
    component_type="external_entity",
    description="외부 결제 시스템 API",
    trust_boundary="external"
))

# 각 구성요소 위협 분석
for component in engine.components:
    threats = engine.analyze_component(component)
    print(f"\n[{component.name}] 위협 분석:")
    for t in threats:
        print(f"  - {t.category.value}: {t.title} (점수: {t.dread_score:.1f})")

# 보고서 생성
report = engine.generate_report()
print(f"\n=== 위협 모델링 요약 ===")
print(f"총 위협 수: {report['summary']['total_threats']}")
print(f"위험도별: {report['summary']['by_risk']}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. SDL 프레임워크 비교

| 프레임워크 | 개발사 | 특징 | 적용 분야 |
|:---|:---|:---|:---|
| **Microsoft SDL** | Microsoft | 최초의 SDL, 포괄적 | 대형 엔터프라이즈 |
| **OWASP SAMM** | OWASP | 성숙도 모델, 오픈소스 | 모든 규모 |
| **NIST SSDF** | NIST | 미국 정부 표준 | 정부, 공급망 |
| **BSIMM** | Cigital | 벤치마킹 모델 | 성숙도 측정 |
| **ISO 27034** | ISO | 국제 표준 | 인증 필요 시 |

#### 2. 개발 단계별 보안 활동 ROI

| 단계 | 활동 | 비용 | 취약점 예방 효과 |
|:---|:---|:---|:---|
| **요구사항** | 보안 요구사항 도출 | $1 | 100x |
| **설계** | 위협 모델링 | $5 | 50x |
| **구현** | SAST, 보안 코딩 | $10 | 15x |
| **검증** | DAST, PenTest | $20 | 5x |
| **배포 후** | 패치, 대응 | $100 | 1x |

#### 3. 과목 융합 관점 분석

- **소프트웨어 공학**: 요구사항 공학, 아키텍처 설계와 통합
- **QA/테스트**: 보안 테스트 자동화, 퍼징, 침투 테스트
- **DevOps**: CI/CD 파이프라인 보안, IaC 보안
- **클라우드**: 보안 그룹, IAM Policy-as-Code
- **컴플라이언스**: PCI DSS, ISO 27001 요구사항

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 핀테크 스타트업 SDL 도입**
- 상황: 보안 팀 없음, 빠른 개발 필요, 규제 준수
- 판단: 경량화된 OWASP SAMM Level 1 목표
- 핵심 결정:
  - 필수: 위협 모델링, SAST, DAST, PenTest
  - 생략: 정식 FSR, 복잡한 승인 프로세스
  - 자동화: GitHub Actions로 SAST/DAST 통합
- 효과: 6개월 내 SAMM Level 1 달성, 심사 통과

**시나리오 2: 대기업 레거시 시스템 보안 강화**
- 상황: 10년 된 레거시, 보안 부채 심각
- 판단: 신규 개발은 SDL, 레거시는 점진적 개선
- 핵심 결정:
  - 신규: SDL 100% 적용
  - 레거시: 취약점 스캔 → 우선순위별 패치
  - 마이그레이션: 점진적 재작성
- 효과: 연간 취약점 60% 감소

**시나리오 3: 공공기관 보안 개발 프로세스 구축**
- 상황: 행정안전부 가이드라인 준수, ISO 27001 인증 필요
- 판단: NIST SSDF + ISO 27034 기반 SDL
- 핵심 결정:
  - 문서화: 요구사항~검증 산출물 표준화
  - 승인: 보안팀 FSR 의무화
  - 감사: 내부 감사 체계 구축
- 효과: ISO 27001 인증, 감사 지적 80% 감소

#### 2. 도입 시 고려사항 (체크리스트)

**조직 준비도**
- [ ] 경영진 지원 확보
- [ ] 보안 교육 프로그램 수립
- [ ] SDL 담당자/팀 지정
- [ ] 보안 도구 예산 확보

**기술 인프라**
- [ ] SAST 도구 도입 (SonarQube, Checkmarx)
- [ ] DAST 도구 도입 (OWASP ZAP, Burp Suite)
- [ ] SCA 도구 도입 (Snyk, Dependabot)
- [ ] CI/CD 파이프라인 준비

**프로세스**
- [ ] 위협 모델링 템플릿 준비
- [ ] 보안 코딩 가이드라인 수립
- [ ] 취약점 분류/우선순위 기준
- [ ] 취약점 수정 SLA 정의

#### 3. 안티패턴 (Anti-patterns)

| 안티패턴 | 문제점 | 올바른 접근 |
|:---|:---|:---|
| **보안은 보안팀만** | 개발자 책임 회피 | 개발팀 보안 책임 공유 |
| **도구만 도입** | 프로세스 없이 기술만 | 프로세스 → 도구 순서 |
| **100% 자동화 고집** | False Positive 홍수 | 자동화 + 인간 리뷰 하이브리드 |
| **배포 전 보안 테스트만** | 늦은 발견, 수정 비용 | 설계~구현 단계 보안 활동 |

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | 내용 | 측정 지표 |
|:---|:---|:---|
| 정량적 | 취약점 감소 | 프로덕션 취약점 70% 감소 |
| 정량적 | 수정 비용 절감 | 설계 단계 대비 100배 절감 |
| 정량적 | 개발 속도 | 보안 이슈로 인한 지연 50% 감소 |
| 정성적 | 보안 인식 | 개발자 보안 역량 향상 |
| 정성적 | 규정 준수 | 감사, 인증 용이 |

#### 2. 미래 전망 및 진화 방향

- **AI 기반 보안 코딩**: Copilot Security, 자동 취약점 수정
- **Shift-Left 확대**: 요구사항 단계 AI 위협 모델링
- **Policy-as-Code**: OPA, Sentinel로 보안 정책 코드화
- **SBOM 의무화**: 공급망 보안, Software Bill of Materials

#### 3. 참고 표준/가이드

- **NIST SP 800-160**: Systems Security Engineering
- **NIST SP 800-218 (SSDF)**: Secure Software Development Framework
- **ISO/IEC 27034**: Application Security
- **OWASP SAMM**: Software Assurance Maturity Model
- **Microsoft SDL**: Security Development Lifecycle

---

### 관련 개념 맵 (Knowledge Graph)

- [OWASP Top 10](@/studynotes/09_security/04_application_security/owasp_top10.md) : 보안 코딩 대상 취약점
- [위협 모델링](@/studynotes/09_security/04_application_security/threat_modeling.md) : Security by Design 핵심 활동
- [DevSecOps](@/studynotes/09_security/04_application_security/devsecops.md) : SDL의 DevOps 통합
- [Privacy by Design](@/studynotes/09_security/01_policy/privacy_by_design.md) : 개인정보 보호 내재화
- [심층 방어](@/studynotes/09_security/01_policy/defense_in_depth.md) : Security by Design 원칙

---

### 어린이를 위한 3줄 비유 설명

1. **미리 설계하기**: 집을 지을 때 처음부터 방화문, 소화기를 계산에 넣어요. 다 지어놓고 나중에 끼워 맞추지 않죠.
2. **처음부터 튼튼하게**: 자동차를 만들 때 충돌 테스트를 생각해서 설계해요. 다 만들고 "안전해야지" 하는 게 아니에요.
3. **모두가 함께**: 건축가, 목수, 전기기사가 모두 안전을 생각해요. 한 사람만 안전을 걱정하면 안 되죠. 프로그램도 마찬가지예요.
