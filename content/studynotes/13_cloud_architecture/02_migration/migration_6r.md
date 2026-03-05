+++
title = "클라우드 마이그레이션 6R 전략"
date = 2024-05-20
description = "온프레미스에서 클라우드로 전환하는 6가지 전략(Rehost, Replatform, Refactor, Repurchase, Retire, Retain)의 분석과 적용 기준"
weight = 25
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Cloud Migration", "6R Strategy", "Rehost", "Refactor", "Lift and Shift", "AWS", "Azure"]
+++

# 클라우드 마이그레이션 6R 전략 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 온프레미스 워크로드를 클라우드로 전환하기 위한 6가지 전략적 접근법(Rehost, Replatform, Refactor, Repurchase, Retire, Retain)을 체계적으로 분류하여, 각 애플리케이션의 비즈니스 가치, 기술 부채, 마이그레이션 비용을 고려한 최적의 이관 경로를 수립하는 프레임워크입니다.
> 2. **가치**: 무분별한 "Lift and Shift"로 인한 **클라우드 비용 폭증(최대 2~3배)**을 방지하고, 각 워크로드에 맞는 전략을 적용하여 **ROI를 30~50% 향상**시키며, 마이그레이션 리스크를 체계적으로 관리합니다.
> 3. **융합**: 포트폴리오 평가 도구(AWS MAP, Azure Migrate)와 결합하여 자동화된 분석을 수행하고, DevOps 파이프라인, IaC(Terraform), 컨테이너화(Docker)와 연계하여 실행합니다.

---

## Ⅰ. 개요 (Context & Background)

클라우드 마이그레이션 6R 전략은 AWS가 제안한 클라우드 전환 방법론으로, 조직의 애플리케이션 포트폴리오를 분석하고 각 워크로드에 가장 적합한 이관 전략을 수립하는 데 활용됩니다. 이 프레임워크는 마이그레이션 결정을 체계화하고, 클라우드 이점을 극대화하는 데 도움을 줍니다.

**💡 비유**: 6R 전략은 **'이사 방법 선택'**과 같습니다. 이사할 집(클라우드)으로 옮길 때, 모든 짐을 똑같이 옮길 필요는 없습니다.
- **Rehost**: 짐을 박스에 담아 그대로 옮김 (가장 빠름)
- **Replatform**: 이삿짐 센터가 포장해주는 서비스 이용 (약간의 개선)
- **Refactor**: 새 집에 맞춰 가구를 새로 맞춤 (가장 큰 변화)
- **Repurchase**: 이불, 커튼 등은 새로 구매 (SaaS로 대체)
- **Retire**: 낡은 안 쓰는 물건은 버림 (폐기)
- **Retain**: 당장 옮기지 않을 물건은 기존 집에 둠 (유지)

**등장 배경 및 발전 과정**:
1. **초기 클라우드 마이그레이션의 무질서**: 2010년대 초, 많은 기업이 단순히 VM을 클라우드로 복제(Lift and Shift)하여 비용이 오히려 증가하는 사례가 빈번했습니다.
2. **AWS MAP (Migration Acceleration Program)**: AWS가 체계적인 마이그레이션 방법론을 정립하고 6R 전략을 공식화했습니다.
3. **Gartner의 5R 모델 확장**: Rearchitect, Replatform, Rehost, Retire, Replace의 5R을 AWS가 6R로 확장했습니다.
4. **하이브리드 전략의 대중화**: 모든 워크로드를 클라우드로 옮기는 것이 아니라, 온프레미스와 클라우드를 혼합하는 전략이 정립되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: 6R 전략 상세 분석

| 전략 | 정의 | 변경 수준 | 소요 기간 | 비용 | 클라우드 이점 | 적용 대상 |
|---|---|---|---|---|---|---|
| **Rehost** | 앱 변경 없이 IaaS로 이관 | 없음 | 1~3개월 | 낮음 | 낮음 | 레거시, 긴급 이관 |
| **Replatform** | 일부 최적화 (관리형 서비스) | 적음 | 3~6개월 | 중간 | 중간 | DB, 미들웨어 |
| **Refactor** | 클라우드 네이티브로 재설계 | 큼 | 6~18개월 | 높음 | 높음 | 핵심 앱, 확장 필요 |
| **Repurchase** | SaaS로 대체 | 완전 교체 | 1~3개월 | 중간 | 중간 | CRM, 이메일, 협업 |
| **Retire** | 시스템 폐기 | 삭제 | 즉시 | 없음 | - | 미사용, 중복 |
| **Retain** | 온프레미스 유지 | 없음 | - | - | - | 규제, 민감 데이터 |

### 정교한 구조 다이어그램: 6R 전략 결정 트리

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ 6R Strategy Decision Tree ]                            │
│                     (Cloud Migration Strategy)                              │
└─────────────────────────────────────────────────────────────────────────────┘

                         [ Application Assessment ]
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
            [ 비즈니스 가치 있음? ]           [ 사용 중? ]
                    │                               │
           ┌────────┴────────┐              ┌──────┴──────┐
           │                 │              │             │
          YES               NO             YES           NO
           │                 │              │             │
           │                 ▼              │             ▼
           │         ┌────────────┐         │      ┌────────────┐
           │         │  RETIRE    │         │      │  RETIRE    │
           │         │  (폐기)     │         │      │  (폐기)     │
           │         └────────────┘         │      └────────────┘
           │                                │
           ▼                                │
    [ 즉시 이관 가능? ]                      │
           │                                │
    ┌──────┴──────┐                        │
    │             │                        │
   YES           NO                        │
    │             │                        │
    │             ▼                        │
    │    [ 규제/기술 제약? ]                │
    │             │                        │
    │     ┌───────┴───────┐               │
    │     │               │               │
    │    YES             NO               │
    │     │               │               │
    │     ▼               ▼               │
    │ ┌────────┐   [ SaaS 대체 가능? ]     │
    │ │ RETAIN │        │                 │
    │ │(유지)   │  ┌─────┴─────┐          │
    │ └────────┘  │           │          │
    │            YES         NO          │
    │             │           │          │
    │             ▼           ▼          │
    │      ┌──────────┐ [ 리팩터링 필요? ]
    │      │REPURCHASE│      │          │
    │      │ (SaaS)   │ ┌────┴────┐     │
    │      └──────────┘ │         │     │
    │                  YES       NO     │
    │                   │         │     │
    │                   ▼         ▼     │
    │            ┌──────────┐ ┌────────┐
    │            │REFACTOR  │ │최적화? │
    │            │(재설계)   │ │        │
    │            └──────────┘ └───┬────┘
    │                             │
    │                     ┌───────┴───────┐
    │                     │               │
    │                    YES             NO
    │                     │               │
    │                     ▼               ▼
    │              ┌───────────┐   ┌───────────┐
    │              │REPLATFORM │   │  REHOST   │
    │              │(관리형)    │   │(이관)     │
    │              └───────────┘   └───────────┘
    │
    └──────────────────────────────────────────────►


[ 6R Strategy Summary ]

┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                    Cloud Native (최대 클라우드 이점)                     ││
│  │                                                                         ││
│  │    ◄──────────────────────────────────────────────────────────────►    ││
│  │                                                                         ││
│  │    Rehost      Replatform     Refactor      Repurchase                 ││
│  │    (Lift&Shift) (Lift&Reshape)(Re-architect)(Drop&Shop)                ││
│  │        │            │              │              │                     ││
│  │     낮음 ◄───── 변경 수준/복잡성/클라우드 이점 ─────► 높음              ││
│  │     높음 ◄───── 리스크/시간/비용 ─────► 낮음 (단기)                     ││
│  │                                                                         ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌────────────────────┐  ┌────────────────────┐                            │
│  │      Retire        │  │      Retain        │                            │
│  │   (앱 폐기)         │  │  (온프레미스 유지) │                            │
│  │   - 미사용 앱       │  │  - 규제 요구사항   │                            │
│  │   - 중복 시스템     │  │  - 민감 데이터     │                            │
│  │   - 레거시 교체     │  │  - 아직 준비 안 됨 │                            │
│  └────────────────────┘  └────────────────────┘                            │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: 각 전략별 상세 분석

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    Migration Strategy Deep Dive                             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ 1. Rehost (Lift and Shift) ]                                            │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │                                                                    │   │
│  │  On-Premises                        AWS Cloud                      │   │
│  │  ┌──────────────┐                  ┌──────────────┐               │   │
│  │  │   App Server │  ───────────►    │   EC2 VM     │               │   │
│  │  │   (VM)       │   VM Copy        │  (Same Spec) │               │   │
│  │  └──────────────┘                  └──────────────┘               │   │
│  │  ┌──────────────┐                  ┌──────────────┐               │   │
│  │  │   Database   │  ───────────►    │   EC2 DB     │               │   │
│  │  │  (Oracle)    │   DB Dump/Restore│  (Oracle)    │               │   │
│  │  └──────────────┘                  └──────────────┘               │   │
│  │                                                                    │   │
│  │  장점: 가장 빠름, 낮은 리스크, 앱 변경 없음                        │   │
│  │  단점: 클라우드 이점 적음, 비용 최적화 어려움                      │   │
│  │  도구: AWS MGN, Azure Migrate, VMware HCX                         │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  [ 2. Replatform (Lift and Reshape) ]                                      │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │                                                                    │   │
│  │  On-Premises                        AWS Cloud                      │   │
│  │  ┌──────────────┐                  ┌──────────────┐               │   │
│  │  │   App Server │  ───────────►    │   EC2 VM     │               │   │
│  │  │   (VM)       │   VM Copy        │  (Same Spec) │               │   │
│  │  └──────────────┘                  └──────────────┘               │   │
│  │  ┌──────────────┐                  ┌──────────────┐               │   │
│  │  │   Database   │  ───────────►    │   RDS        │  ◄── 관리형   │   │
│  │  │  (Oracle)    │   Migration      │  (Aurora)    │               │   │
│  │  └──────────────┘                  └──────────────┘               │   │
│  │                                                                    │   │
│  │  장점: 일부 클라우드 이점, DB 관리 부담 감소                       │   │
│  │  단점: 일부 호환성 문제, 제한적인 변경                             │   │
│  │  도구: AWS DMS, Azure Database Migration                          │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  [ 3. Refactor / Re-architect ]                                            │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │                                                                    │   │
│  │  On-Premises                        AWS Cloud                      │   │
│  │  ┌──────────────┐                  ┌──────────────┐               │   │
│  │  │  Monolithic  │  ───────────►    │ Microservices│               │   │
│  │  │    App       │   Decompose      │  in EKS/ECS  │               │   │
│  │  │              │                  │              │               │   │
│  │  │ ┌──────────┐ │                  │ ┌────┐┌────┐│               │   │
│  │  │ │ UI       │ │                  │ │Svc ││Svc ││               │   │
│  │  │ │ Business │ │                  │ │ A  ││ B  ││               │   │
│  │  │ │ DB       │ │                  │ └────┘└────┘│               │   │
│  │  │ └──────────┘ │                  └──────────────┘               │   │
│  │  └──────────────┘                  ┌──────────────┐               │   │
│  │                                    │  DynamoDB    │  ◄── NoSQL   │   │
│  │                                    │  Lambda      │  ◄── Serverless│   │
│  │                                    └──────────────┘               │   │
│  │                                                                    │   │
│  │  장점: 최대 클라우드 이점, 확장성, 비용 효율                        │   │
│  │  단점: 높은 복잡성, 긴 기간, 높은 비용                             │   │
│  │  적용: 핵심 비즈니스 앱, 확장성 필요, 혁신 프로젝트                │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  [ 4. Repurchase (Drop and Shop) ]                                         │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │                                                                    │   │
│  │  On-Premises                        SaaS Cloud                     │   │
│  │  ┌──────────────┐                  ┌──────────────┐               │   │
│  │  │   SAP ERP    │  ───────────►    │  SAP S/4HANA │               │   │
│  │  │  (On-Prem)   │   Migration      │    Cloud     │               │   │
│  │  └──────────────┘                  └──────────────┘               │   │
│  │  ┌──────────────┐                  ┌──────────────┐               │   │
│  │  │   Exchange   │  ───────────►    │  Office 365  │               │   │
│  │  │   Email      │   Replace        │   (SaaS)     │               │   │
│  │  └──────────────┘                  └──────────────┘               │   │
│  │                                                                    │   │
│  │  장점: 빠른 전환, 관리 부담 감소, 최신 기능                        │   │
│  │  단점: 커스터마이징 제한, 데이터 이관 복잡, 벤더 종속              │   │
│  │  적용: CRM(Salesforce), 이메일(O365), 협업(Slack)                 │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  [ 5. Retire (애플리케이션 폐기) ]                                          │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │                                                                    │   │
│  │  애플리케이션 포트폴리오의 평균 10~20%가 폐기 대상                 │   │
│  │                                                                    │   │
│  │  폐기 기준:                                                        │   │
│  │  - 6개월 이상 미사용                                               │   │
│  │  - 다른 시스템으로 대체 완료                                       │   │
│  │  - 비즈니스 가치 없음                                              │   │
│  │  - 기술적 부채가 너무 심각                                         │   │
│  │                                                                    │   │
│  │  폐기 절차:                                                        │   │
│  │  1. 사용자 확인 → 2. 데이터 백업 → 3. 아카이브 → 4. 시스템 종료   │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  [ 6. Retain (온프레미스 유지) ]                                            │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │                                                                    │   │
│  │  유지 기준:                                                        │   │
│  │  - 데이터 주권/상주 요구사항 (금융, 공공)                          │   │
│  │  - 레거시 하드웨어 의존성 (메인프레임)                             │   │
│  │  - 클라우드 비용이 더 높음 (고정 워크로드)                         │   │
│  │  - 규제/컴플라이언스 제약                                          │   │
│  │  - 아직 마이그레이션 준비 안 됨                                    │   │
│  │                                                                    │   │
│  │  재평가 주기: 6~12개월마다 다시 검토                               │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: 마이그레이션 평가 및 실행 스크립트

```python
#!/usr/bin/env python3
"""
클라우드 마이그레이션 6R 분석 및 추천 도구
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional

class MigrationStrategy(Enum):
    REHOST = "Rehost"
    REPLATFORM = "Replatform"
    REFACTOR = "Refactor"
    REPURCHASE = "Repurchase"
    RETIRE = "Retire"
    RETAIN = "Retain"

@dataclass
class Application:
    """애플리케이션 정보"""
    name: str
    business_value: str  # high, medium, low
    usage_frequency: str  # daily, weekly, monthly, rarely, never
    technical_debt: str  # low, medium, high
    data_sensitivity: str  # public, internal, confidential, restricted
    dependencies: List[str]
    has_saas_alternative: bool
    cloud_ready: bool
    regulatory_constraints: bool
    last_used_days: int

class MigrationAnalyzer:
    """마이그레이션 분석기"""

    def __init__(self):
        self.strategies = {
            MigrationStrategy.REHOST: [],
            MigrationStrategy.REPLATFORM: [],
            MigrationStrategy.REFACTOR: [],
            MigrationStrategy.REPURCHASE: [],
            MigrationStrategy.RETIRE: [],
            MigrationStrategy.RETAIN: []
        }

    def analyze(self, app: Application) -> MigrationStrategy:
        """애플리케이션에 대한 최적 마이그레이션 전략 분석"""

        # 1. Retire: 미사용 애플리케이션
        if app.usage_frequency == "never" or app.last_used_days > 180:
            return MigrationStrategy.RETIRE

        # 2. Retire: 비즈니스 가치가 낮고 기술 부채가 높음
        if app.business_value == "low" and app.technical_debt == "high":
            return MigrationStrategy.RETIRE

        # 3. Retain: 규제 제약 또는 민감 데이터
        if app.regulatory_constraints or app.data_sensitivity == "restricted":
            if not app.cloud_ready:
                return MigrationStrategy.RETAIN

        # 4. Repurchase: SaaS 대안이 있고 비즈니스 가치가 중간 이하
        if app.has_saas_alternative and app.business_value in ["low", "medium"]:
            return MigrationStrategy.REPURCHASE

        # 5. Refactor: 핵심 비즈니스 앱, 높은 확장성 필요
        if (app.business_value == "high" and
            app.technical_debt in ["medium", "high"] and
            app.cloud_ready):
            return MigrationStrategy.REFACTOR

        # 6. Replatform: DB/미들웨어가 있고 일부 최적화 가능
        if app.cloud_ready and app.business_value in ["medium", "high"]:
            return MigrationStrategy.REPLATFORM

        # 7. Rehost: 기본값 (가장 빠른 이관)
        return MigrationStrategy.REHOST

    def analyze_portfolio(self, apps: List[Application]) -> Dict[str, List[str]]:
        """전체 포트폴리오 분석"""

        results = {strategy.value: [] for strategy in MigrationStrategy}

        for app in apps:
            strategy = self.analyze(app)
            results[strategy.value].append(app.name)

        return results

    def generate_report(self, results: Dict[str, List[str]]) -> str:
        """마이그레이션 계획 보고서 생성"""

        total_apps = sum(len(apps) for apps in results.values())

        report = f"""
╔══════════════════════════════════════════════════════════════════════════╗
║              Cloud Migration 6R Strategy Analysis Report                 ║
╠══════════════════════════════════════════════════════════════════════════╣
║  Total Applications: {total_apps:<50} ║
╠══════════════════════════════════════════════════════════════════════════╣
"""

        for strategy, apps in results.items():
            count = len(apps)
            percentage = (count / total_apps * 100) if total_apps > 0 else 0
            bar = "█" * int(percentage / 2) + "░" * (50 - int(percentage / 2))
            report += f"""║  {strategy:<12} {count:>3} apps ({percentage:>5.1f}%)                        ║
║  {bar} ║
"""

            if apps:
                apps_str = ", ".join(apps[:5])
                if len(apps) > 5:
                    apps_str += f", ... ({len(apps) - 5} more)"
                report += f"""║  Applications: {apps_str:<53} ║
"""
            report += """╠══════════════════════════════════════════════════════════════════════════╣
"""

        report += """╚══════════════════════════════════════════════════════════════════════════╝
"""
        return report

# 실행 예시
if __name__ == "__main__":
    # 샘플 애플리케이션 포트폴리오
    portfolio = [
        Application(
            name="ERP System",
            business_value="high",
            usage_frequency="daily",
            technical_debt="medium",
            data_sensitivity="confidential",
            dependencies=["Oracle DB", "LDAP"],
            has_saas_alternative=True,
            cloud_ready=True,
            regulatory_constraints=False,
            last_used_days=0
        ),
        Application(
            name="Legacy Reporting",
            business_value="low",
            usage_frequency="monthly",
            technical_debt="high",
            data_sensitivity="internal",
            dependencies=[],
            has_saas_alternative=True,
            cloud_ready=False,
            regulatory_constraints=False,
            last_used_days=30
        ),
        Application(
            name="Internal Wiki",
            business_value="medium",
            usage_frequency="daily",
            technical_debt="low",
            data_sensitivity="internal",
            dependencies=["MySQL"],
            has_saas_alternative=True,
            cloud_ready=True,
            regulatory_constraints=False,
            last_used_days=0
        ),
        Application(
            name="Archive System",
            business_value="low",
            usage_frequency="never",
            technical_debt="high",
            data_sensitivity="confidential",
            dependencies=[],
            has_saas_alternative=False,
            cloud_ready=False,
            regulatory_constraints=False,
            last_used_days=365
        ),
        Application(
            name="Payment Gateway",
            business_value="high",
            usage_frequency="daily",
            technical_debt="low",
            data_sensitivity="restricted",
            dependencies=["HSM"],
            has_saas_alternative=False,
            cloud_ready=False,
            regulatory_constraints=True,
            last_used_days=0
        ),
    ]

    analyzer = MigrationAnalyzer()
    results = analyzer.analyze_portfolio(portfolio)
    print(analyzer.generate_report(results))
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 전략별 TCO 분석 (5년 기준)

| 전략 | 초기 비용 | 운영 비용/년 | 5년 총비용 | 클라우드 이점 | ROI |
|---|---|---|---|---|---|
| **Rehost** | $50K | $200K | $1,050K | 10% | 110% |
| **Replatform** | $100K | $150K | $850K | 30% | 150% |
| **Refactor** | $500K | $100K | $1,000K | 70% | 200% |
| **Repurchase** | $30K | $180K | $930K | 40% | 130% |
| **Retain** | $0 | $250K | $1,250K | 0% | 100% |

### 과목 융합 관점 분석

**보안(Security)과의 융합**:
- **데이터 분류**: 민감도에 따른 마이그레이션 전략 수립
- **암호화 마이그레이션**: 기존 암호화 체계와 클라우드 KMS 통합
- **규정 준수**: GDPR, HIPAA 등 규제에 따른 Retain 결정

**비용 관리(FinOps)와의 융합**:
- **Reserved Instance**: Rehost 후 비용 최적화
- **Right Sizing**: Replatform 시 인스턴스 크기 최적화
- **Serverless**: Refactor 시 종량제 비용 모델 활용

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 대기업 마이그레이션 전략 수립

**문제 상황**: 제조업체 F사는 200개 애플리케이션을 보유하고 있으며, 2년 내 클라우드 마이그레이션을 완료해야 합니다.

**기술사의 전략적 의사결정**:

1. **포트폴리오 분석 결과**:

   | 전략 | 앱 수 | 비율 | 기간 |
   |---|---|---|---|
   | Rehost | 80 | 40% | 6개월 |
   | Replatform | 40 | 20% | 12개월 |
   | Refactor | 20 | 10% | 18개월 |
   | Repurchase | 10 | 5% | 6개월 |
   | Retire | 30 | 15% | 즉시 |
   | Retain | 20 | 10% | - |

2. **단계별 실행 계획**:

   - **Wave 1 (0~6개월)**: Retire(30개) + Rehost(50개)
   - **Wave 2 (6~12개월)**: Rehost(30개) + Replatform(20개)
   - **Wave 3 (12~18개월)**: Replatform(20개) + Repurchase(10개)
   - **Wave 4 (18~24개월)**: Refactor(20개)

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - 모든 것을 Rehost**: 단순 Lift and Shift는 비용이 오히려 증가할 수 있습니다. Rehost 후 6개월 내 최적화 필수.

- **안티패턴 - 과도한 Refactor**: 모든 앱을 클라우드 네이티브로 재작성하려 하면 기간과 비용이 폭증합니다.

- **체크리스트**:
  - [ ] 애플리케이션 인벤토리 구축
  - [ ] 비즈니스 가치 평가
  - [ ] 기술 부채 분석
  - [ ] 의존성 매핑
  - [ ] 데이터 민감도 분류
  - [ ] 마이그레이션 파도(Wave) 계획

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 마이그레이션 전 | 6R 전략 적용 후 | 개선율 |
|---|---|---|---|
| **인프라 비용** | $10M/년 | $6M/년 | 40% 절감 |
| **운영 효율** | Baseline | 2배 향상 | 100% |
| **출시 속도** | 6개월 | 2주 | 90% 단축 |
| **앱 가용성** | 99.5% | 99.99% | 10배 향상 |

### 미래 전망 및 진화 방향

- **AI 기반 마이그레이션 분석**: 머신러닝으로 최적 전략 자동 추천
- **자동화된 리팩터링 도구**: 코드 변환 자동화 (AWS App2Container)
- **멀티 클라우드 마이그레이션**: 여러 CSP로의 분산 이관

### ※ 참고 표준/가이드
- **AWS Migration Acceleration Program (MAP)**: AWS 공식 마이그레이션 프레임워크
- **Azure Cloud Adoption Framework**: Microsoft 마이그레이션 가이드
- **Gartner 5R Model**: 마이그레이션 전략 분류 표준

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [하이브리드 클라우드](@/studynotes/13_cloud_architecture/02_migration/hybrid_cloud.md) : Retain 전략과 연계
- [클라우드 마이그레이션 전략](@/studynotes/13_cloud_architecture/02_migration/cloud_migration_strategies.md) : 전략 수립 방법론
- [IaaS](@/studynotes/13_cloud_architecture/03_virt/iaas.md) : Rehost 전략의 기반
- [SaaS](@/studynotes/13_cloud_architecture/03_virt/saas.md) : Repurchase 전략의 기반
- [마이크로서비스 아키텍처](@/studynotes/13_cloud_architecture/01_native/msa.md) : Refactor 전략의 목표

---

### 👶 어린이를 위한 3줄 비유 설명
1. 6R 전략은 **'이사 방법 선택'**과 같아요. 모든 짐을 똑같이 옮길 필요 없어요.
2. **Rehost**는 짐을 그대로 옮기고, **Refactor**는 새 집에 맞춰 가구를 새로 맞추는 것이에요.
3. 안 쓰는 물건은 **Retire(버리기)**, 당장 안 옮길 건 **Retain(유지)**. 이렇게 계획적으로 이사해요!
