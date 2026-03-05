+++
title = "데이터바우처 사업"
categories = ["studynotes-16_bigdata"]
+++

# 데이터바우처 사업

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터바우처는 정부가 중소기업·스타트업에게 데이터 구매·가공·분석 비용을 지원하여 데이터 기반 혁신을 촉진하는 정책 프로그램이다.
> 2. **가치**: 데이터바우처는 기업당 최대 1억 원까지 지원하여 데이터 활용 진입장벽을 낮추고, 데이터 산업 생태계를 조성한다.
> 3. **융합**: AI 학습 데이터, 마이데이터, 공공데이터와 결합하여 중소기업의 디지털 전환을 가속화한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

데이터바우처 사업은 과학기술정보통신부와 한국데이터산업진흥원이 주관하여 중소기업·벤처기업의 데이터 구매, 가공, 분석 활용을 지원하는 정부 지원 사업이다. 기업은 데이터바우처를 통해 필요한 데이터를 구매하거나, 데이터 가공·분석 서비스를 할인받을 수 있다.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    데이터바우처 사업 구조                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  정부 (과기정통부, 한국데이터산업진흥원)                         │   │
│  │                         │                                       │   │
│  │         바우처 발급      │                                       │   │
│  │                         ▼                                       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  중소기업·스타트업 (수요기업)                                    │   │
│  │  - 데이터 구매                                                   │   │
│  │  - 데이터 가공                                                   │   │
│  │  - 데이터 분석                                                   │   │
│  └───────────────────────────┬─────────────────────────────────────┘   │
│                              │                                        │
│        바우처 사용           │                                        │
│                              ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  데이터 공급기관                                                 │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐   │   │
│  │  │데이터    │  │데이터    │  │데이터    │  │플랫폼    │   │   │
│  │  │판매기관  │  │가공기관  │  │분석기관  │  │운영사   │   │   │
│  │  └───────────┘  └───────────┘  └───────────┘  └───────────┘   │   │
│  └───────────────────────────┬─────────────────────────────────────┘   │
│                              │                                        │
│        정산                  │                                        │
│                              ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  정부 → 공급기관                                                 │   │
│  │  (바우처 금액 정산)                                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 💡 비유

데이터바우처는 "정부 지원 상품권"에 비유할 수 있다. 정부가 중소기업에게 "이 상품권으로 데이터를 사거나 분석 서비스를 받으세요"라고 주면, 기업은 돈을 내지 않고도 고가의 데이터를 활용할 수 있다. 나중에 정부가 상점(데이터 공급기관)에 돈을 지불한다.

### 지원 내용 및 규모

| 지원 유형 | 지원 한도 | 지원 비율 | 지원 대상 |
|-----------|-----------|-----------|-----------|
| **데이터 구매** | 5,000만 원 | 80% | 중소기업, 벤처 |
| **데이터 가공** | 5,000만 원 | 75% | 중소기업, 벤처 |
| **데이터 분석** | 1억 원 | 70% | 중소기업, 벤처 |
| **종합 지원** | 1억 원 | 70~80% | 중소기업, 벤처 |

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 지원 분야별 상세 내용

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    데이터바우처 지원 분야                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. 데이터 구매 지원                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  목적: 기업에 필요한 데이터셋 구매 비용 지원                     │   │
│  │  대상 데이터:                                                    │   │
│  │  - 공공데이터 가공 데이터                                        │   │
│  │  - 민간 데이터 (위치, 소비, SNS 등)                              │   │
│  │  - AI 학습용 데이터                                              │   │
│  │  지원 한도: 5,000만 원 (80% 지원)                               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  2. 데이터 가공 지원                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  목적: 데이터 라벨링, 정제, 변환 등 가공 비용 지원               │   │
│  │  지원 내용:                                                      │   │
│  │  - 라벨링 (이미지, 텍스트, 음성)                                 │   │
│  │  - 데이터 정제 (클렌징, 표준화)                                  │   │
│  │  - 비식별화 (개인정보 보호)                                      │   │
│  │  지원 한도: 5,000만 원 (75% 지원)                               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  3. 데이터 분석 지원                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  목적: 데이터 기반 분석 컨설팅 및 AI 모델 개발 지원              │   │
│  │  지원 내용:                                                      │   │
│  │  - 탐색적 데이터 분석 (EDA)                                      │   │
│  │  - 머신러닝 모델 개발                                            │   │
│  │  - 비즈니스 인텔리전스 (BI) 구축                                 │   │
│  │  지원 한도: 1억 원 (70% 지원)                                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  4. 종합 지원 (패키지)                                                  │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  목적: 구매 + 가공 + 분석 통합 지원                              │   │
│  │  지원 한도: 1억 원 (70~80% 지원)                                 │   │
│  │  특징: 데이터 확보부터 분석까지 원스톱 지원                      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 신청 자격 및 절차

```python
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class BusinessType(Enum):
    SMALL_BUSINESS = "small_business"      # 중소기업
    VENTURE = "venture"                    # 벤처기업
    STARTUP = "startup"                    # 스타트업

class SupportType(Enum):
    DATA_PURCHASE = "data_purchase"        # 데이터 구매
    DATA_PROCESSING = "data_processing"    # 데이터 가공
    DATA_ANALYSIS = "data_analysis"        # 데이터 분석
    COMPREHENSIVE = "comprehensive"        # 종합 지원

@dataclass
class VoucherApplication:
    """데이터바우처 신청서"""
    company_name: str
    business_type: BusinessType
    support_type: SupportType
    project_name: str
    project_description: str
    requested_amount: int
    company_contribution: int  # 자부담금
    expected_outcome: str
    data_types: List[str]
    data_provider: Optional[str]
    data_processor: Optional[str]

class DataVoucherSimulator:
    """데이터바우처 시뮬레이터"""

    # 지원 비율
    SUPPORT_RATES = {
        SupportType.DATA_PURCHASE: 0.80,
        SupportType.DATA_PROCESSING: 0.75,
        SupportType.DATA_ANALYSIS: 0.70,
        SupportType.COMPREHENSIVE: 0.75
    }

    # 지원 한도
    SUPPORT_LIMITS = {
        SupportType.DATA_PURCHASE: 50_000_000,
        SupportType.DATA_PROCESSING: 50_000_000,
        SupportType.DATA_ANALYSIS: 100_000_000,
        SupportType.COMPREHENSIVE: 100_000_000
    }

    def calculate_support(self, application: VoucherApplication) -> dict:
        """지원 금액 계산"""

        support_rate = self.SUPPORT_RATES[application.support_type]
        support_limit = self.SUPPORT_LIMITS[application.support_type]

        # 총 사업비
        total_cost = application.requested_amount + application.company_contribution

        # 정부 지원금 계산
        calculated_support = int(total_cost * support_rate)
        actual_support = min(calculated_support, support_limit)

        # 자부담금 재계산
        company_contribution = total_cost - actual_support

        return {
            "total_cost": total_cost,
            "government_support": actual_support,
            "company_contribution": company_contribution,
            "support_rate": f"{support_rate * 100:.0f}%",
            "within_limit": calculated_support <= support_limit
        }

    def check_eligibility(self, application: VoucherApplication) -> dict:
        """신청 자격 확인"""

        issues = []

        # 중소기업 확인 (매출액 기준)
        # 실제로는 중소벤처기업부 확인 필요

        # 지원 한도 확인
        support_limit = self.SUPPORT_LIMITS[application.support_type]
        if application.requested_amount > support_limit:
            issues.append(f"요청 금액이 한도({support_limit:,}원) 초과")

        # 자부담금 비율 확인
        support_rate = self.SUPPORT_RATES[application.support_type]
        min_contribution_rate = 1 - support_rate
        actual_contribution_rate = application.company_contribution / (
            application.requested_amount + application.company_contribution
        )
        if actual_contribution_rate < min_contribution_rate:
            issues.append(
                f"자부담금 비율이 {min_contribution_rate*100:.0f}% 미만"
            )

        return {
            "eligible": len(issues) == 0,
            "issues": issues
        }


# 사용 예시
if __name__ == "__main__":
    simulator = DataVoucherSimulator()

    application = VoucherApplication(
        company_name="(주)AI스타트업",
        business_type=BusinessType.VENTURE,
        support_type=SupportType.DATA_ANALYSIS,
        project_name="AI 기반 소비자 행동 분석 시스템 개발",
        project_description="구매 데이터를 활용한 AI 추천 시스템 개발",
        requested_amount=80_000_000,
        company_contribution=35_000_000,
        expected_outcome="매출 20% 증대 예상",
        data_types=["구매 내역", "고객 행동 로그"],
        data_provider=None,
        data_processor=None
    )

    # 자격 확인
    eligibility = simulator.check_eligibility(application)
    print(f"신청 자격: {'적격' if eligibility['eligible'] else '부적격'}")

    # 지원금 계산
    support = simulator.calculate_support(application)
    print(f"총 사업비: {support['total_cost']:,}원")
    print(f"정부 지원금: {support['government_support']:,}원")
    print(f"자부담금: {support['company_contribution']:,}원")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 데이터바우처 vs 유사 제도 비교

| 구분 | 데이터바우처 | AI바우처 | 클라우드바우처 |
|------|--------------|----------|----------------|
| **주관** | 과기정통부 | 과기정통부 | 과기정통부 |
| **지원 대상** | 데이터 | AI 솔루션 | 클라우드 |
| **지원 한도** | 1억 원 | 5억 원 | 1억 원 |
| **지원 비율** | 70~80% | 50~80% | 50~80% |

### 연도별 추진 실적

| 연도 | 예산 | 지원 기업 수 | 기업당 평균 지원 |
|------|------|--------------|-------------------|
| 2021 | 200억 원 | 300개사 | 6,700만 원 |
| 2022 | 300억 원 | 450개사 | 6,700만 원 |
| 2023 | 400억 원 | 600개사 | 6,700만 원 |
| 2024 | 500억 원 | 750개사 | 6,700만 원 |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 데이터바우처 활용 AI 서비스 개발

```
┌─────────────────────────────────────────────────────────────────────────┐
│  시나리오: 중소 제조기업 AI 품질 검사 시스템 개발                       │
├─────────────────────────────────────────────────────────────────────────┤
│  기업 현황:                                                             │
│  - 중소 제조기업 (직원 50명)                                           │
│  - 연 매출 100억 원                                                    │
│  - 불량률 5% → 2% 감소 목표                                            │
│                                                                         │
│  프로젝트 구성:                                                         │
│  1. 데이터 구매 (5,000만 원)                                           │
│     - 제품 이미지 데이터셋 (정상/불량)                                 │
│     - 공정 센서 데이터                                                 │
│                                                                         │
│  2. 데이터 가공 (3,000만 원)                                           │
│     - 이미지 라벨링                                                    │
│     - 센서 데이터 정제                                                 │
│                                                                         │
│  3. 데이터 분석 (4,000만 원)                                           │
│     - 딥러닝 불량 검사 모델 개발                                       │
│     - 실시간 모니터링 대시보드                                         │
│                                                                         │
│  비용 구조:                                                             │
│  - 총 사업비: 1.2억 원                                                 │
│  - 정부 지원: 8,000만 원 (67%)                                         │
│  - 자부담: 4,000만 원 (33%)                                            │
│                                                                         │
│  기대 효과:                                                             │
│  - 불량률 5% → 2% 감소                                                 │
│  - 연간 약 3억 원 비용 절감                                            │
│  - ROI: 750% (1년)                                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

### 신청 체크리스트

**자격 요건**
- [ ] 중소기업·벤처기업 확인
- [ ] 직전 연도 재무제표 준비
- [ ] 데이터 활용 계획서 작성

**신청 서류**
- [ ] 사업계획서
- [ ] 데이터바우처 신청서
- [ ] 견적서 (데이터 공급/가공/분석 기관)
- [ ] 사업자등록증

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대효과

| 구분 | 효과 |
|------|------|
| **기업** | 데이터 활용 진입장벽 완화, AI 도입 가속 |
| **데이터 산업** | 시장 확대, 데이터 공급 생태계 조성 |
| **국가** | 데이터 경제 활성화, 디지털 전환 가속 |

### 참고 규정

- **데이터산업 진흥법**
- **데이터바우처 사업 운영 가이드라인** (한국데이터산업진흥원)

---

## 📌 관련 개념 맵

- [공공 빅데이터](./public_bigdata.md) - 공공데이터 활용
- [데이터 경제](./data_economy.md) - 데이터 시장 조성
- [AI 학습 데이터](../04_analysis/machine_learning_analytics.md) - 데이터바우처 활용 분야
- [중소기업 디지털 전환](../10_industry/sme_digital_transformation.md)

---

## 👶 어린이를 위한 3줄 비유

**1단계 (무엇인가요?)**: 데이터바우처는 정부가 주는 "데이터 상품권"이에요. 작은 회사가 데이터를 사거나 분석할 때 쓸 수 있어요.

**2단계 (어떻게 쓰나요?)**: 회사가 "이 데이터가 필요해요!"라고 신청하면, 정부가 돈의 대부분을 내줘요. 회사는 조금만 내면 돼요. 그 데이터로 새로운 앱이나 서비스를 만들 수 있어요.

**3단계 (왜 중요한가요?)**: 데이터는 비싸서 작은 회사는 사기 어려워요. 하지만 데이터바우처가 있으면 싸게 구할 수 있어요. 그래서 작은 회사도 큰 회사처럼 AI를 만들 수 있어요!
