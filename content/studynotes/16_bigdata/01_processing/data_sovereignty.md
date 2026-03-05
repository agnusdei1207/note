+++
title = "데이터 주권 (Data Sovereignty)"
categories = ["studynotes-16_bigdata"]
+++

# 데이터 주권 (Data Sovereignty)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 주권은 국가가 자국 내에서 생성된 데이터에 대해 법적 관할권을 행사할 수 있는 권리로, 데이터의 국경 간 이동과 저장 위치를 규제한다.
> 2. **가치**: 데이터 주권은 국가 안보, 개인정보 보호, 경제적 이익 보호를 위해 필수적이며, 글로벌 기업의 클라우드 전략에 큰 영향을 미친다.
> 3. **융합**: GDPR, 클라우드 규제, 데이터 현지화 법안과 결합하여 글로벌 데이터 거버넌스의 핵심 이슈로 부상했다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

데이터 주권(Data Sovereignty)은 데이터가 생성된 국가의 법률과 규제가 해당 데이터에 적용된다는 원칙이다. 이는 데이터가 저장된 물리적 위치(서버의 위치)가 어디냐에 따라 데이터에 적용되는 법률이 결정됨을 의미한다.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    데이터 주권 개념도                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  국가 A (한국)                                                   │   │
│  │  ┌─────────────────┐                                            │   │
│  │  │ 개인정보보호법   │                                            │   │
│  │  │ 네트워크법       │                                            │   │
│  │  │ 데이터 3법      │                                            │   │
│  │  └────────┬────────┘                                            │   │
│  │           │                                                      │   │
│  │           ▼                                                      │   │
│  │  ┌─────────────────┐      데이터 전송      ┌─────────────────┐ │   │
│  │  │ 한국 데이터     │ ─────────────────────▶│ 해외 클라우드   │ │   │
│  │  │ (국내 생성)     │                       │ (미국 리전)     │ │   │
│  │  └─────────────────┘                       └────────┬────────┘ │   │
│  │                                                     │          │   │
│  └─────────────────────────────────────────────────────┼──────────┘   │
│                                                        │              │
│                                                        ▼              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  국가 B (미국)                                                   │   │
│  │  ┌─────────────────┐                                            │   │
│  │  │ CLOUD Act       │                                            │   │
│  │  │ Patriot Act     │                                            │   │
│  │  │ CCPA            │                                            │   │
│  │  └─────────────────┘                                            │   │
│  │           │                                                      │   │
│  │           ▼                                                      │   │
│  │  미국 법률이 저장된 데이터에 적용?                               │   │
│  │  - 미국 정부의 데이터 접근 요청 가능?                            │   │
│  │  - 한국 법률의 적용 여부?                                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  핵심 질문: 한국 데이터가 미국 서버에 있을 때, 누구의 법이 적용되나?    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 💡 비유

데이터 주권은 "외교관 면책 특권"의 반대 개념에 비유할 수 있다. 외교관은 외국에 있어도 자국 법률의 보호를 받지만, 데이터는 반대로 저장된 나라의 법률 적용을 받는다. 한국 기업의 데이터라도 미국 서버에 저장되면 미국 법률의 영향을 받을 수 있다.

### 등장 배경

1. **2013년**: 스노든 사건으로 미국 NSA의 해외 데이터 수집 폭로
2. **2015년**: EU Safe Harbor 판결 무효화 (Schrems I)
3. **2020년**: EU Privacy Shield 판결 무효화 (Schrems II)
4. **2022년**: 미국 CLOUD Act로 해외 데이터 접근권 명문화

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 국가별 데이터 현지화 정책 비교

| 국가 | 정책 | 요구사항 | 예외 |
|------|------|----------|------|
| **러시아** | Federal Law 242-FZ | 개인정보 로컬 저장 | 승인된 이전 |
| **중국** | 사이버보안법 | 핵심 데이터 로컬 저장 | 보안 심사 후 이전 |
| **인도네시아** | GR 71/2019 | 공공데이터 로컬 저장 | - |
| **브라질** | LGPD | 동의 기반 이전 | 적절성 결정 |
| **EU** | GDPR | 적절성 결정 또는 보호 조치 | BCR, SCC |
| **호주** | Privacy Act | 개인정보 보호 의무 | 해외 이전 제한 |

### 클라우드 리전 선택과 데이터 주권

```
┌─────────────────────────────────────────────────────────────────────────┐
│            클라우드 리전 선택과 데이터 주권 고려사항                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  AWS 리전 예시                                                   │   │
│  │                                                                  │   │
│  │  미국 (미국 법률)         유럽 (GDPR)         아시아 (각국 법률)  │   │
│  │  ┌─────────┐             ┌─────────┐         ┌─────────┐       │   │
│  │  │us-east-1│             │eu-west-1│         │ap-northeast-2│   │   │
│  │  │(버지니아)│             │(아일랜드)│         │(서울)        │   │   │
│  │  └─────────┘             └─────────┘         └─────────┘       │   │
│  │                                                                  │   │
│  │  - CLOUD Act 적용        - GDPR 준수          - 한국 법률 적용 │   │
│  │  - Patriot Act           - EU-미국 이전 제한   - 네트워크법    │   │
│  │  - FISA Court            - Schrems II 영향     - 개인정보보호법│   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  선택 기준:                                                             │
│  1. 데이터 생성 위치 (Data Origin)                                      │
│  2. 규제 요구사항 (Regulatory Requirements)                             │
│  3. 지연 시간 요구사항 (Latency)                                        │
│  4. 비용 (Cost)                                                         │
│  5. 재해 복구 (DR) 전략                                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 데이터 이전 메커니즘 (GDPR 기준)

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class TransferMechanism(Enum):
    ADEQUACY_DECISION = "adequacy_decision"      # 적절성 결정
    SCC = "standard_contractual_clauses"         # 표준계약조항
    BCR = "binding_corporate_rules"              # 구속력 있는 기업규칙
    CONSENT = "explicit_consent"                 # 명시적 동의
    DEROGATIONS = "derogations"                  # 예외 조항

@dataclass
class DataTransferAssessment:
    """데이터 이전 평가"""
    source_country: str
    destination_country: str
    data_types: List[str]
    transfer_mechanism: TransferMechanism
    legal_basis: str
    risks: List[str]
    safeguards: List[str]

class DataSovereigntyChecker:
    """데이터 주권 검사기"""

    # 적절성 결정 국가 목록 (GDPR 기준)
    ADEQUACY_COUNTRIES = [
        "ANDORRA", "ARGENTINA", "CANADA", "FAROE_ISLANDS",
        "GUERNSEY", "ISRAEL", "ISLE_OF_MAN", "JAPAN",
        "JERSEY", "NEW_ZEALAND", "REPUBLIC_OF_KOREA",
        "SWITZERLAND", "UK", "URUGUAY", "USA_DPF"  # Data Privacy Framework
    ]

    def __init__(self):
        self.country_regulations = self._load_regulations()

    def assess_transfer(
        self,
        source: str,
        destination: str,
        data_types: List[str]
    ) -> DataTransferAssessment:
        """데이터 이전 가능성 평가"""

        # 1. 적절성 결정 확인
        if destination.upper() in self.ADEQUACY_COUNTRIES:
            mechanism = TransferMechanism.ADEQUACY_DECISION
            legal_basis = f"{destination}은(는) 적절성 결정 국가"
            risks = []
            safeguards = []
        else:
            # 2. 표준계약조항 필요
            mechanism = TransferMechanism.SCC
            legal_basis = "표준계약조항(SCC) 체결 필요"
            risks = self._assess_risks(destination)
            safeguards = self._recommend_safeguards(destination)

        return DataTransferAssessment(
            source_country=source,
            destination_country=destination,
            data_types=data_types,
            transfer_mechanism=mechanism,
            legal_basis=legal_basis,
            risks=risks,
            safeguards=safeguards
        )

    def _assess_risks(self, destination: str) -> List[str]:
        """목적지 국가 리스크 평가"""
        risks = []
        # 실제로는 국가별 평가 DB 사용
        high_risk_countries = ["CN", "RU"]  # 예시

        if destination.upper() in high_risk_countries:
            risks.append("높은 감시 리스크")
            risks.append("정부 데이터 접근 가능성")

        return risks

    def _recommend_safeguards(self, destination: str) -> List[str]:
        """보호 조치 권장"""
        return [
            "표준계약조항(SCC) 체결",
            "이전 영향 평가(TIA) 수행",
            "추가 기술적 보호조치 (암호화)",
            "정기적 감사"
        ]

    def check_local_storage_requirement(
        self,
        country: str,
        data_type: str
    ) -> Dict:
        """로컬 저장 의무 확인"""

        # 국가별 로컬 저장 의무 데이터
        local_requirements = {
            "RU": {"personal_data": True, "financial": True},
            "CN": {"personal_data": True, "critical_infra": True},
            "KR": {"financial": "partial", "healthcare": "partial"}
        }

        requirement = local_requirements.get(country.upper(), {})
        required = requirement.get(data_type, False)

        return {
            "country": country,
            "data_type": data_type,
            "local_storage_required": required,
            "recommendation": "로컬 리전 사용 권장" if required else "해외 리전 사용 가능"
        }


# 사용 예시
if __name__ == "__main__":
    checker = DataSovereigntyChecker()

    # 한국 → 미국 데이터 이전 평가
    assessment = checker.assess_transfer(
        source="KR",
        destination="US",
        data_types=["personal_data", "transaction_history"]
    )

    print(f"이전 메커니즘: {assessment.transfer_mechanism.value}")
    print(f"법적 근거: {assessment.legal_basis}")
    print(f"리스크: {assessment.risks}")
    print(f"보호조치: {assessment.safeguards}")

    # 러시아 로컬 저장 의무 확인
    local_req = checker.check_local_storage_requirement("RU", "personal_data")
    print(f"\n러시아 개인정보 로컬 저장 의무: {local_req['local_storage_required']}")
