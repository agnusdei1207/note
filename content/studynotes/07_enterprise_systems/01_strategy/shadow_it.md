+++
title = "섀도우 IT (Shadow IT)"
date = "2026-03-04"
[extra]
categories = "studynotes-07_enterprise_systems"
+++

# 섀도우 IT (Shadow IT)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: IT 부서의 승인이나 통제 없이 현업 부서가 자체적으로 도입하여 사용하는 **비공식 IT 시스템, 소프트웨어, 클라우드 서비스**로, SaaS 확산과 함께 급격히 증가하고 있는 현상입니다.
> 2. **가치**: 현업의 민첩성과 혁신을 촉진하는 긍정적 측면과 보안, 규정 준수, 데이터 무결성을 위협하는 부정적 측면이 공존하는 **양날의 검(Double-edged Sword)**입니다.
> 3. **융합**: CASB(Cloud Access Security Broker), SASE(Secure Access Service Edge) 등의 클라우드 보안 솔루션과 결합하여 섀도우 IT를 **가시화(Discovery)하고 통제(Governance)**하는 방향으로 진화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 섀도우 IT의 개념 및 철학적 근간
섀도우 IT(Shadow IT)는 정식 IT 거버넌스 프로세스를 거치지 않고 조직 내 개인이나 부서가 독자적으로 도입하여 사용하는 정보기술 자산을 의미합니다. 과거에는 엑셀 매크로나 부서용 PC 프로그램 정도였으나, 클라우드 시대에는 SaaS(Software as a Service) 형태의 서비스가 주를 이룹니다.

섀도우 IT의 핵심 철학적 배경은 **"현업의 IT 니즈 충족 속도"와 "IT 부서의 통제 욕구" 사이의 갈등**입니다. 현업은 즉각적인 문제 해결을 원하지만, IT 부서는 보안, 표준화, 비용 효율성을 위해 승인 프로세스를 요구합니다. 이 간극이 클수록 섀도우 IT는 증가합니다.

### 2. 💡 비유를 통한 이해: 회사 외부의 비공식 심부름 센터
대기업의 본사 건물에 정식 심부름 센터(IT 부서)가 있습니다. 문서를 가져오려면 복잡한 승인 절차가 필요하고 3일이 걸립니다. 그런데 어떤 직원이 "그냥 건너편 카페 알바생에게 부탁하면 10분만에 됩니다"라는 사실을 알게 됩니다. **이 카페 알바생이 바로 섀도우 IT입니다.** 빠르고 편리하지만, 회사 규정을 벗어나고, 보안 검증도 안 되었으며, 나중에 그 직원이 퇴사하면 누가 책임질지도 불분명합니다.

### 3. 등장 배경 및 발전 과정
- **1990년대-2000년대**: 부서별 엑셀, 액세스 DB, 개인용 툴 도입. 주로 로컬 환경에서 제한적 사용.
- **2010년대 초**: 스마트폰, 태블릿의 보급으로 BYOD(Bring Your Own Device) 문제와 결합.
- **2010년대 중반**: Dropbox, Google Drive 등 클라우드 스토리지, Slack 등 협업 툴의 현업 자체 도입 급증.
- **2020년대**: COVID-19 팬데믹과 원격근무 확산으로 SaaS 섀도우 IT가 폭발적 증가. 가트너 조사에 따르면 **기업 IT 지출의 30-40%가 IT 부서 통제 밖에서 발생**하는 것으로 추정.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 섀도우 IT의 유형 분류
```
┌─────────────────────────────────────────────────────────────────────┐
│                      섀도우 IT 유형 분류                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [SaaS 서비스]                    [인프라/플랫폼]                    │
│  ├─ 협업 툴 (Slack, Notion)       ├─ 클라우드 IaaS (AWS, GCP)       │
│  ├─ 파일 공유 (Dropbox, GDrive)   ├─ PaaS 개발 환경                 │
│  ├─ CRM/영업 (HubSpot, Pipedrive) ├─ GitHub, GitLab                 │
│  ├─ 마케팅 (Mailchimp, Canva)     └─ Serverless Functions           │
│  └─ HR/채용 (Greenhouse, Lever)                                     │
│                                                                     │
│  [하드웨어/기기]                  [데이터/API]                       │
│  ├─ 개인 스마트폰/태블릿          ├─ Public API 연동                 │
│  ├─ IoT 기기                      ├─ Open Data 활용                 │
│  └─ 개인용 주변기기               └─ Third-party SDK                 │
│                                                                     │
│  [로우코드/노코드]                                                   │
│  ├─ Zapier, IFTTT 자동화                                            │
│  ├─ Airtable, Bubble 앱 빌더                                        │
│  └─ Microsoft Power Platform                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2. 섀도우 IT 발생 원인 분석 (Root Cause Analysis)

| 원인 카테고리 | 세부 요인 | 발생 메커니즘 |
|:---|:---|:---|
| **속도/민첩성** | IT 승인 프로세스 지연 | 현업이 1주일 기다리는 동안 업무 마감 기한 도래 |
| **기능성** | 표준 툴의 기능 부족 | IT 표준 툴이 현업 니즈(예: 마케팅 자동화)를 충족 못함 |
| **비용** | 예산 승인의 어려움 | 부서 예산으로 SaaS 구독비를 처리하는 것이 더 쉬움 |
| **사용성** | UX/UI 불만 | IT 표준 시스템의 복잡한 UI vs 직관적인 SaaS |
| **인지 부족** | 보안 위험 인식 부재 | "그냥 파일만 올리는 건데 뭐가 문제야?" |
| **조직 문화** | IT-현업 간 신뢰 부족 | "IT는 우리 일을 이해하지 못해" |

### 3. 섀도우 IT 탐지(Discovery) 아키텍처
엔터프라이즈 환경에서 섀도우 IT를 식별하기 위한 기술적 아키텍처입니다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                 섀도우 IT 탐지 및 통제 아키텍처                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Endpoint   │  │   Network    │  │    Cloud     │              │
│  │    Agent     │  │   Firewall   │  │    API       │              │
│  │  (DLP/EDR)   │  │   (SSL/TLS)  │  │  Connector   │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                 │                       │
│         └─────────────────┼─────────────────┘                       │
│                           ▼                                         │
│              ┌─────────────────────────┐                            │
│              │    CASB (Cloud Access   │                            │
│              │    Security Broker)     │                            │
│              │  ┌───────────────────┐  │                            │
│              │  │ Discovery Engine  │  │ ← SaaS 앱 식별             │
│              │  │ Risk Scoring      │  │ ← 위험도 평가              │
│              │  │ Policy Engine     │  │ ← 통제 정책 적용           │
│              │  │ Sanction/Block    │  │ ← 승인/차단                │
│              │  └───────────────────┘  │                            │
│              └───────────┬─────────────┘                            │
│                          │                                          │
│                          ▼                                          │
│              ┌─────────────────────────┐                            │
│              │   Shadow IT Dashboard   │                            │
│              │ - 앱별 사용 현황         │                            │
│              │ - 위험도 리포트          │                            │
│              │ - 사용자별 통계          │                            │
│              │ - 승인/미승인 앱 목록    │                            │
│              └─────────────────────────┘                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4. 핵심 알고리즘: SaaS 앱 위험도 평가 모델
CASB 솔루션에서 활용하는 SaaS 앱 위험도 평가 알고리즘입니다.

**[수학적 모델: SaaS Risk Score]**
$$Risk_{score} = \sum_{i=1}^{n} w_i \cdot R_i$$

여기서:
- $R_i$: i번째 위험 요소의 점수 (0-100)
- $w_i$: i번째 위험 요소의 가중치
- 주요 위험 요소: 데이터 보안, 컴플라이언스, 데이터 주권, 비즈니스 안정성, 법적 이슈

**[Python 예시: SaaS 앱 위험도 평가]**
```python
class SaaS_Risk_Assessment:
    """
    SaaS 애플리케이션의 위험도를 평가하는 모델
    """

    # 위험 요소별 가중치 (기업 정책에 따라 조정)
    WEIGHTS = {
        'data_security': 0.30,      # 데이터 보안 (암호화, 접근통제)
        'compliance': 0.25,         # 컴플라이언스 (SOC2, ISO27001, GDPR)
        'data_residency': 0.15,     # 데이터 주권 (데이터 저장 위치)
        'business_stability': 0.15, # 비즈니스 안정성 (재무, 운영 연속성)
        'legal_issues': 0.15        # 법적 이슈 (라이선스, 소송 이력)
    }

    def __init__(self, app_name):
        self.app_name = app_name
        self.risk_factors = {}

    def assess_data_security(self, encryption_at_rest, encryption_in_transit,
                             mfa_available, sso_support, audit_logs):
        """데이터 보안 평가"""
        score = 0
        if encryption_at_rest: score += 25
        if encryption_in_transit: score += 25
        if mfa_available: score += 20
        if sso_support: score += 15
        if audit_logs: score += 15

        # 역산: 보안 수준이 높을수록 위험도는 낮음
        self.risk_factors['data_security'] = 100 - score

    def assess_compliance(self, soc2, iso27001, gdpr_compliant, hipaa_compliant):
        """컴플라이언스 평가"""
        score = 0
        if soc2: score += 30
        if iso27001: score += 30
        if gdpr_compliant: score += 20
        if hipaa_compliant: score += 20

        self.risk_factors['compliance'] = 100 - score

    def assess_data_residency(self, data_location_approved, data_localization_option):
        """데이터 주권 평가"""
        if data_location_approved and data_localization_option:
            self.risk_factors['data_residency'] = 10
        elif data_location_approved:
            self.risk_factors['data_residency'] = 40
        else:
            self.risk_factors['data_residency'] = 90

    def assess_business_stability(self, years_in_business, revenue_visible,
                                   funding_rounds, customer_count):
        """비즈니스 안정성 평가"""
        score = 0
        if years_in_business >= 5: score += 30
        elif years_in_business >= 2: score += 15

        if revenue_visible: score += 25
        if funding_rounds >= 3: score += 20
        if customer_count >= 10000: score += 25

        self.risk_factors['business_stability'] = 100 - score

    def assess_legal_issues(self, has_lawsuits, license_clear, ip_issues):
        """법적 이슈 평가"""
        score = 100
        if has_lawsuits: score -= 40
        if not license_clear: score -= 30
        if ip_issues: score -= 30

        self.risk_factors['legal_issues'] = max(0, 100 - score)

    def calculate_overall_risk(self):
        """종합 위험도 계산"""
        if not self.risk_factors:
            return None

        total_risk = sum(
            self.risk_factors[factor] * self.WEIGHTS[factor]
            for factor in self.WEIGHTS.keys()
        )

        # 위험 등급 분류
        if total_risk < 30:
            rating = "LOW"
            recommendation = "승인 권장"
        elif total_risk < 60:
            rating = "MEDIUM"
            recommendation = "조건부 승인 (보안 통제 필요)"
        else:
            rating = "HIGH"
            recommendation = "승인 불가 또는 제한적 사용"

        return {
            'app_name': self.app_name,
            'risk_score': round(total_risk, 2),
            'risk_rating': rating,
            'recommendation': recommendation,
            'factor_scores': self.risk_factors
        }

# 실행 예시: Slack vs 알려지지 않은 협업 툴
slack = SaaS_Risk_Assessment("Slack")
slack.assess_data_security(True, True, True, True, True)
slack.assess_compliance(True, True, True, False)
slack.assess_data_residency(True, True)
slack.assess_business_stability(10, True, 10, 1000000)
slack.assess_legal_issues(False, True, False)

unknown_tool = SaaS_Risk_Assessment("Unknown Collaboration Tool")
unknown_tool.assess_data_security(False, True, False, False, False)
unknown_tool.assess_compliance(False, False, False, False)
unknown_tool.assess_data_residency(False, False)
unknown_tool.assess_business_stability(1, False, 1, 100)
unknown_tool.assess_legal_issues(False, False, True)

print("=== Slack Risk Assessment ===")
print(slack.calculate_overall_risk())
print("\n=== Unknown Tool Risk Assessment ===")
print(unknown_tool.calculate_overall_risk())
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 섀도우 IT 관리 전략 비교

| 전략 | 완전 금지 (Block) | 부분 허용 (Contain) | 적극 활용 (Enable) |
|:---|:---|:---|:---|
| **철학** | 모든 비공식 IT 차단 | 위험 기반 통제 | 혁신 도구로 승인 |
| **도구** | Firewall 차단 | CASB 정책 적용 | SaaS 승인 카탈로그 |
| **장점** | 보안 위험 최소화 | 균형 접근 | 현업 민첩성 극대화 |
| **단점** | 현업 저항, 생산성 저하 | 관리 부담 | 통제력 약화 가능성 |
| **적합 조직** | 금융, 공공, 보안 민감 | 대부분 기업 | 스타트업, 혁신 조직 |

### 2. 타 과목과의 융합 관점

#### 2-1. 보안 과목과의 연계
섀도우 IT는 전통적인 네트워크 경계 기반 보안(Perimeter Security)을 무력화합니다. 이를 해결하기 위해:
- **제로 트러스트(Zero Trust)**: 모든 접속을 신뢰하지 않고 검증
- **CASB (Cloud Access Security Broker)**: 클라우드 서비스 접속 통제
- **DLP (Data Loss Prevention)**: 민감 데이터 유출 방지

#### 2-2. IT 거버넌스 과목과의 연계
섀도우 IT는 IT 포트폴리오 관리의 가시성을 저해합니다. COBIT 프레임워크의 APO08(관계 관리), APO09(서비스 협정) 프로세스를 통해 IT-현업 간 협업 모델을 개선해야 합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단: 섀도우 IT 관리 체계 구축 시나리오

**[상황]** D사는 최근 보안 감사에서 200개 이상의 미승인 SaaS 앱이 사용 중인 것을 발견했습니다. 그중에는 민감한 고객 데이터를 처리하는 앱도 포함되어 있었습니다.

**[전략적 대응 및 아키텍처 결정]**

1. **Discovery Phase (탐지)**
   - CASB 솔루션 도입 (McAfee, Netskope, Zscaler 중 검토)
   - 네트워크 트래픽 분석, 방화벽 로그, DNS 쿼리 분석
   - 사용자 설문 조사 병행

2. **Risk Assessment Phase (평가)**
   - 식별된 200개 앱에 대한 위험도 평가
   - 데이터 분류: 민감/내부/공개
   - 앱 분류: 업무 필수/편의성/불필요

3. **Remediation Phase (조치)**
   - High Risk 앱: 즉시 차단 + 대체 승인 앱 제안
   - Medium Risk 앱: 조건부 승인 (CASB 정책 적용)
   - Low Risk 앱: 승인 카탈로그에 추가

4. **Governance Phase (지속 관리)**
   - 신규 SaaS 승인 프로세스 간소화 (Fast Track)
   - 정기 Shadow IT 스캔 수행
   - 현업 IT 니즈 선제적 파악

### 2. 도입 시 고려사항 (Checklist)
- **현업과의 소통**: 일방적 차단은 조직 내 갈등 유발. 충분한 소통과 대안 제시 필요
- **승인 프로세스 개선**: 섀도우 IT의 근본 원인인 느린 승인 프로세스 개선
- **기술적 통제와 교육 병행**: 기술적 차단만으로는 한계. 보안 인식 교육 병행

### 3. 안티패턴 (Anti-patterns)
- **"모두 차단하면 끝"**: VPN 사용, 개인 기기 활용 등 우회 방법 존재. 근본적 해결 안 됨
- **IT 부서만의 일방적 결정**: 현업 요구를 무시한 정책은 현장에서 무시됨

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 효과 구분 | 항목 | 효과 |
|:---|:---|:---|
| **보안** | 데이터 유출 사고 | 미승인 앱을 통한 유출 경로 차단 |
| **규정 준수** | GDPR, 개인정보보호법 | 데이터 처리 위탁 계약 누락 방지 |
| **비용** | 중복 SaaS 구독 | 부서별 중복 구독 식별 및 통합 |
| **가시성** | IT 자산 관리 | 전사 SaaS 사용 현황 파악 |

### 2. 미래 전망: SASE와 섀도우 IT 관리
Secure Access Service Edge(SASE) 아키텍처가 발전하면서, 네트워크와 보안 기능이 클라우드로 통합됩니다. 이는 섀도우 IT 탐지가 네트워크 엣지에서 실시간으로 수행될 수 있음을 의미합니다.

### 3. 참고 표준 및 컴플라이언스
- **ISO/IEC 27001**: 정보보호 관리체계 요구사항
- **GDPR**: 제28조 데이터 처리자 계약 의무 (미승인 SaaS 사용 시 위반 가능성)
- **ISMS-P**: 개인정보 처리 위탁 관리 요구사항

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [CASB (Cloud Access Security Broker)](@/studynotes/07_enterprise_systems/01_strategy/it_governance.md): 섀도우 IT 탐지 및 통제 핵심 솔루션
- [SASE (Secure Access Service Edge)](@/studynotes/06_ict_convergence/_index.md): 네트워크와 보안의 통합 엣지 아키텍처
- [IT 거버넌스 (IT Governance)](@/studynotes/07_enterprise_systems/01_strategy/it_governance.md): 섀도우 IT 관리의 거버넌스 체계
- [데이터 분류 (Data Classification)](@/studynotes/07_enterprise_systems/02_data/_index.md): 섀도우 IT 위험도 평가의 기준
- [제로 트러스트 (Zero Trust)](@/studynotes/01_security/_index.md): 섀도우 IT 환경에서의 보안 접근법

---

## 👶 어린이를 위한 3줄 비유 설명

1. 섀도우 IT는 학교 선생님(IT 부서) 몰래 친구들끼리 사용하는 "비밀 채팅방"과 같아요.
2. 선생님이 승인한 공지방은 너무 느리고 재미없어서, 친구들이 더 빠르고 편한 앱을 찾아서 쓰는 거예요.
3. 하지만 비밀 채팅방은 나쁜 사람이 들어올 수도 있고, 나중에 숙제를 잃어버릴 수도 있어서, 선생님이 알고 안전하게 도와주는 것이 중요해요!
