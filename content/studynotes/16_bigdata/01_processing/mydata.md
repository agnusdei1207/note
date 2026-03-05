+++
title = "마이데이터 (MyData)"
categories = ["studynotes-16_bigdata"]
+++

# 마이데이터 (MyData)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 마이데이터는 개인이 자신의 데이터를 직접 관리하고 통제하며, 이를 통해 서비스를 받거나 경제적 가치를 창출할 수 있는 권리와 시스템이다.
> 2. **가치**: 마이데이터는 개인에게 데이터 주권을 부여하고, 기업에게는 개인 동의 하에 데이터를 활용할 수 있는 법적 근거를 제공하여 신뢰 기반 데이터 경제를 조성한다.
> 3. **융합**: 오픈뱅킹, API 표준, 데이터 3법, 개인정보 동의 시스템과 결합하여 금융, 의료, 공공 분야에서 확산되고 있다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

마이데이터(MyData)는 "개인정보 자기결정권"을 기반으로 개인이 자신의 데이터를 직접 관리, 통제, 활용할 수 있도록 하는 제도와 기술적 체계를 의미한다. 기존에는 기업이 수집한 개인 데이터를 기업이 독점했으나, 마이데이터는 개인이 데이터를 직접 넘겨받아 원하는 서비스에 제공할 수 있다.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                 기존 모델 vs 마이데이터 모델 비교                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  [기존 모델: 기업 중심 데이터 독점]                                     │
│                                                                         │
│  ┌─────────┐     데이터 제공      ┌─────────┐                         │
│  │  개인   │ ───────────────────▶ │ 기업 A  │                         │
│  └─────────┘     (동의 시 일괄)    └────┬────┘                         │
│       │                              │                                │
│       │                              │ 데이터 독점                     │
│       │                              ▼                                │
│       │                         ┌─────────┐                          │
│       │                         │ 기업 A  │                          │
│       │                         │ 서비스  │                          │
│       │                         └─────────┘                          │
│       │                                                              │
│       │     다른 서비스 이용 시                                      │
│       └──────────────────────▶ 데이터를 다시 제공해야 함              │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  [마이데이터 모델: 개인 중심 데이터 주권]                               │
│                                                                         │
│                          ┌─────────────┐                               │
│                          │  MyData     │                               │
│                          │  허브/API   │                               │
│                          └──────┬──────┘                               │
│                                 │                                       │
│       ┌─────────────────────────┼─────────────────────────┐            │
│       │                         │                         │            │
│       ▼                         ▼                         ▼            │
│  ┌─────────┐              ┌─────────┐              ┌─────────┐        │
│  │ 기업 A  │              │ 기업 B  │              │ 기업 C  │        │
│  │ (은행)  │              │ (카드)  │              │ (증권)  │        │
│  └────┬────┘              └────┬────┘              └────┬────┘        │
│       │                        │                        │              │
│       │    개인 동의 하에      │                        │              │
│       └────────────────────────┼────────────────────────┘              │
│                                │                                       │
│                                ▼                                       │
│                          ┌─────────┐                                  │
│                          │  개인   │ ← 데이터 통제권                   │
│                          └─────────┘                                  │
│                                                                         │
│  개인이 원할 때마다 언제든 데이터 전송 중지 가능                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 💡 비유

마이데이터는 "개인 금고"에 비유할 수 있다. 예전에는 은행이 내 돈을 관리했고, 내가 원할 때마다 은행에 가서 요청해야 했다. 이제는 내 계좌의 돈을 내가 직접 관리하고, 원하는 곳에 언제든 이체할 수 있다. 마이데이터는 내 데이터를 "내 금고"에 넣어두고, 내가 원하는 서비스에만 선택적으로 제공하는 것이다.

### 등장 배경 및 발전 과정

1. **2016년**: EU GDPR 제20조 '이식 가능한 권리(Portability Right)' 도입
2. **2018년**: 영국 오픈뱅킹 의무화 - 금융 데이터 이동 권리
3. **2020년**: 한국 데이터 3법(개인정보보호법, 신용정보법, 정보통신망법) 개정
4. **2022년**: 한국 금융 마이데이터 서비스 본격 시행
5. **2024년~**: 의료, 공공 분야 마이데이터 확대

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 마이데이터 아키텍처

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    마이데이터 서비스 아키텍처                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    MyData App (마이데이터 앱)                    │   │
│  │  ┌─────────────────────────────────────────────────────────────┐│   │
│  │  │  개인 대시보드                                               ││   │
│  │  │  - 연동 기관 관리     - 데이터 전송 내역                     ││   │
│  │  │  - 동의 현황          - 서비스 이용 현황                     ││   │
│  │  └─────────────────────────────────────────────────────────────┘│   │
│  └───────────────────────────────┬─────────────────────────────────┘   │
│                                  │                                    │
│                                  ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    MyData Platform (플랫폼)                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │   │
│  │  │ 동의 관리   │  │ ID 인증     │  │ API Gateway │            │   │
│  │  │ 서버       │  │ 서버       │  │             │            │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘            │   │
│  └───────────────────────────────┬─────────────────────────────────┘   │
│                                  │                                    │
│         ┌────────────────────────┼────────────────────────┐           │
│         │                        │                        │            │
│         ▼                        ▼                        ▼            │
│  ┌─────────────┐          ┌─────────────┐          ┌─────────────┐   │
│  │ 데이터 제공 │          │ 데이터 제공 │          │ 데이터 제공 │   │
│  │ 기관 A      │          │ 기관 B      │          │ 기관 C      │   │
│  │ (은행)      │          │ (카드사)    │          │ (보험)      │   │
│  └─────────────┘          └─────────────┘          └─────────────┘   │
│                                                                         │
│  ──────────────────────────────────────────────────────────────────── │
│                                                                         │
│  핵심 프로토콜:                                                         │
│  1. OAuth 2.0 / OpenID Connect: 인증 및 권한 위임                      │
│  2. FAPI (Financial-grade API): 금융급 보안 API                       │
│  3. 데이터 표준: 금융분야 마이데이터 표준API                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 마이데이터 핵심 구성 요소

| 구성 요소 | 역할 | 기술 스택 | 비고 |
|-----------|------|-----------|------|
| **MyData App** | 사용자 인터페이스 | React Native, Flutter | 사용자 동의 관리 |
| **MyData Provider** | 데이터 제공 기관 | REST API, OAuth 2.0 | 은행, 카드, 보험 |
| **MyData Consumer** | 데이터 수신 기관 | REST Client | 핀테크, 자산관리 |
| **Consent Server** | 동의 관리 | DB, Audit Log | 동의 내역 저장 |
| **ID Provider** | 본인 인증 | 인증서, 생체인식 | 금융인증원 등 |
| **API Gateway** | 보안, 로깅 | Kong, Apigee | Rate Limiting |

### 심층 동작 원리: OAuth 2.0 기반 데이터 전송

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum
import jwt
import hashlib

class ConsentScope(Enum):
    """마이데이터 동의 범위"""
    BASIC_IDENTITY = "basic_identity"      # 기본 신원 정보
    ACCOUNT_LIST = "account_list"          # 계좌 목록
    TRANSACTION_HISTORY = "transaction"    # 거래 내역
    CREDIT_INFO = "credit_info"            # 신용 정보
    INSURANCE_INFO = "insurance"           # 보험 정보

class ConsentStatus(Enum):
    """동의 상태"""
    PENDING = "pending"
    GRANTED = "granted"
    REVOKED = "revoked"
    EXPIRED = "expired"

@dataclass
class Consent:
    """동의 정보"""
    consent_id: str
    user_id: str
    provider_id: str        # 데이터 제공 기관
    consumer_id: str        # 데이터 수신 기관
    scopes: List[ConsentScope]
    status: ConsentStatus
    granted_at: Optional[datetime]
    expires_at: Optional[datetime]
    revoked_at: Optional[datetime]

@dataclass
class DataTransferRequest:
    """데이터 전송 요청"""
    request_id: str
    user_id: str
    consumer_id: str
    provider_id: str
    scopes: List[ConsentScope]
    access_token: str

class MyDataConsentManager:
    """마이데이터 동의 관리자"""

    def __init__(self, jwt_secret: str):
        self.jwt_secret = jwt_secret
        self.consents: Dict[str, Consent] = {}
        self.access_tokens: Dict[str, Dict] = {}

    def request_consent(
        self,
        user_id: str,
        provider_id: str,
        consumer_id: str,
        scopes: List[ConsentScope],
        duration_days: int = 365
    ) -> str:
        """동의 요청 생성"""
        import uuid

        consent_id = str(uuid.uuid4())
        consent = Consent(
            consent_id=consent_id,
            user_id=user_id,
            provider_id=provider_id,
            consumer_id=consumer_id,
            scopes=scopes,
            status=ConsentStatus.PENDING,
            granted_at=None,
            expires_at=None,
            revoked_at=None
        )

        self.consents[consent_id] = consent
        return consent_id

    def grant_consent(self, consent_id: str) -> str:
        """동의 승인 (사용자가 승인 버튼 클릭)"""
        consent = self.consents.get(consent_id)
        if not consent:
            raise ValueError("동의 요청을 찾을 수 없음")

        # 동의 상태 업데이트
        consent.status = ConsentStatus.GRANTED
        consent.granted_at = datetime.now()
        consent.expires_at = datetime.now() + timedelta(days=365)

        # 액세스 토큰 발급
        access_token = self._generate_access_token(consent)

        return access_token

    def revoke_consent(self, consent_id: str):
        """동의 철회"""
        consent = self.consents.get(consent_id)
        if not consent:
            raise ValueError("동의 요청을 찾을 수 없음")

        consent.status = ConsentStatus.REVOKED
        consent.revoked_at = datetime.now()

        # 관련 액세스 토큰 무효화
        self._invalidate_tokens(consent_id)

    def verify_access_token(
        self,
        token: str,
        required_scopes: List[ConsentScope]
    ) -> bool:
        """액세스 토큰 검증"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])

            # 토큰 만료 확인
            if datetime.fromtimestamp(payload["exp"]) < datetime.now():
                return False

            # 동의 상태 확인
            consent_id = payload["consent_id"]
            consent = self.consents.get(consent_id)
            if not consent or consent.status != ConsentStatus.GRANTED:
                return False

            # 스코프 확인
            granted_scopes = [ConsentScope(s) for s in payload["scopes"]]
            for required in required_scopes:
                if required not in granted_scopes:
                    return False

            return True

        except jwt.InvalidTokenError:
            return False

    def _generate_access_token(self, consent: Consent) -> str:
        """JWT 액세스 토큰 생성"""
        payload = {
            "consent_id": consent.consent_id,
            "user_id": consent.user_id,
            "provider_id": consent.provider_id,
            "consumer_id": consent.consumer_id,
            "scopes": [s.value for s in consent.scopes],
            "iat": datetime.now().timestamp(),
            "exp": (datetime.now() + timedelta(hours=1)).timestamp()  # 1시간 유효
        }

        token = jwt.encode(payload, self.jwt_secret, algorithm="HS256")
        self.access_tokens[token] = payload

        return token

    def _invalidate_tokens(self, consent_id: str):
        """동의 철회 시 토큰 무효화"""
        tokens_to_remove = [
            token for token, payload in self.access_tokens.items()
            if payload["consent_id"] == consent_id
        ]
        for token in tokens_to_remove:
            del self.access_tokens[token]


class MyDataProviderAPI:
    """데이터 제공 기관 API"""

    def __init__(self, consent_manager: MyDataConsentManager):
        self.consent_manager = consent_manager

    def get_account_list(
        self,
        access_token: str,
        user_id: str
    ) -> Dict:
        """계좌 목록 조회"""
        # 동의 검증
        if not self.consent_manager.verify_access_token(
            access_token,
            [ConsentScope.ACCOUNT_LIST]
        ):
            raise PermissionError("동의하지 않은 데이터 접근")

        # 실제 데이터 반환 (예시)
        return {
            "user_id": user_id,
            "accounts": [
                {
                    "account_id": "ACC001",
                    "bank_name": "국민은행",
                    "account_type": "입출금",
                    "balance": 1500000
                },
                {
                    "account_id": "ACC002",
                    "bank_name": "신한은행",
                    "account_type": "적금",
                    "balance": 5000000
                }
            ],
            "retrieved_at": datetime.now().isoformat()
        }

    def get_transaction_history(
        self,
        access_token: str,
        account_id: str,
        start_date: str,
        end_date: str
    ) -> Dict:
        """거래 내역 조회"""
        # 동의 검증
        if not self.consent_manager.verify_access_token(
            access_token,
            [ConsentScope.TRANSACTION_HISTORY]
        ):
            raise PermissionError("동의하지 않은 데이터 접근")

        # 실제 데이터 반환 (예시)
        return {
            "account_id": account_id,
            "transactions": [
                {
                    "date": "2024-03-01",
                    "type": "입금",
                    "amount": 3000000,
                    "description": "월급"
                },
                {
                    "date": "2024-03-02",
                    "type": "출금",
                    "amount": 50000,
                    "description": "편의점"
                }
            ],
            "period": {"start": start_date, "end": end_date}
        }


# 사용 예시: 마이데이터 서비스 흐름
if __name__ == "__main__":
    consent_manager = MyDataConsentManager(jwt_secret="my-secret-key")
    provider_api = MyDataProviderAPI(consent_manager)

    user_id = "user-001"
    provider_id = "bank-a"  # 데이터 제공 기관 (은행)
    consumer_id = "fintech-app"  # 데이터 수신 기관 (핀테크 앱)

    # 1. 핀테크 앱이 사용자에게 동의 요청
    consent_id = consent_manager.request_consent(
        user_id=user_id,
        provider_id=provider_id,
        consumer_id=consumer_id,
        scopes=[
            ConsentScope.BASIC_IDENTITY,
            ConsentScope.ACCOUNT_LIST,
            ConsentScope.TRANSACTION_HISTORY
        ]
    )
    print(f"동의 요청 생성: {consent_id}")

    # 2. 사용자가 동의 승인
    access_token = consent_manager.grant_consent(consent_id)
    print(f"액세스 토큰 발급: {access_token[:20]}...")

    # 3. 핀테크 앱이 데이터 조회
    accounts = provider_api.get_account_list(access_token, user_id)
    print(f"계좌 목록: {len(accounts['accounts'])}개")

    transactions = provider_api.get_transaction_history(
        access_token,
        accounts["accounts"][0]["account_id"],
        "2024-03-01",
        "2024-03-31"
    )
    print(f"거래 내역: {len(transactions['transactions'])}건")

    # 4. 사용자가 동의 철회
    consent_manager.revoke_consent(consent_id)
    print("동의 철회 완료")

    # 5. 철회 후 데이터 접근 시도 → 실패
    try:
        provider_api.get_account_list(access_token, user_id)
    except PermissionError:
        print("동의 철회로 데이터 접근 불가")
```

### 데이터 3법 핵심 내용

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    데이터 3법 (2020년 개정) 핵심 내용                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. 개인정보보호법 개정                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  - 가명정보 도입: 통계, 연구, 공익 목적으로 가명정보 활용 가능   │   │
│  │  - 개인정보처리 방침 자율화: 일부 항목 선택적 기재               │   │
│  │  - 개인정보 영향평가 의무화: 대량 처리 시 필수                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  2. 신용정보법 개정 (마이데이터 핵심 법적 근거)                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  - 신용정보 전송요구권: 개인이 자신의 신용정보 전송 요구 가능     │   │
│  │  - 마이데이터 사업 법적 근거 마련                               │   │
│  │  - 금융사 의무 제공: 개인 요청 시 데이터 제공 의무               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  3. 정보통신망법 개정                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  - 마케팅 정보 수신 동의 세분화: 야간, 주간 구분 등              │   │
│  │  - 개인정보 처리 현황 공개 의무                                 │   │
│  │  - 개인정보 유출 통지 의무 강화                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ───────────────────────────────────────────────────────────────────── │
│                                                                         │
│  핵심 개념:                                                             │
│  - 가명정보: 개인을 식별할 수 없도록 처리된 정보                       │
│  - 동의 철회권: 언제든 동의를 철회할 수 있는 권리                       │
│  - 이동 요구권: 데이터 이동을 요구할 수 있는 권리                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 국가별 마이데이터/오픈뱅킹 비교

| 구분 | 한국 | 영국 | EU | 일본 |
|------|------|------|-----|------|
| **서비스명** | 마이데이터 | Open Banking | PSD2 | Open Banking |
| **시작 연도** | 2022 | 2018 | 2018 | 2020 |
| **대상 분야** | 금융→의료/공공 확대 | 금융 | 금융 | 금융 |
| **의무화 여부** | 금융 의무 | 금융 의무 | 금융 의무 | 대형은행 의무 |
| **기술 표준** | 금융보안원 | Open Banking Ltd | Berlin Group | 日本銀行協会 |
| **참여 기관** | 50+ | 300+ | 4000+ | 100+ |

### 마이데이터 서비스 분야별 현황

| 분야 | 시작 | 주요 서비스 | 참여 기관 | 이용자 수 |
|------|------|-------------|-----------|-----------|
| **금융** | 2022 | 자산관리, 대출비교 | 은행, 카드, 보험 | 1,500만+ |
| **의료** | 2023 | 건강기록 통합 | 병원, 보험공단 | 100만+ |
| **공공** | 2023 | 행정서비스 간소화 | 행정기관 | 500만+ |
| **통신** | 2024 | 요금제 비교 | 통신 3사 | 시작 단계 |

### 과목 융합: 보안 관점

마이데이터는 보안이 핵심이다:

1. **인증**: 금융인증서, 생체인식, PASS 앱
2. **암호화**: 전송 구간 TLS 1.3, 저장 데이터 AES-256
3. **감사**: 모든 데이터 접근 내역 기록 (Audit Log)
4. **무결성**: 데이터 위변조 방지 (전자서명)

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 마이데이터 기반 자산관리 앱 개발

```
┌─────────────────────────────────────────────────────────────────────────┐
│  시나리오: 핀테크 스타트업 마이데이터 자산관리 앱 개발                   │
├─────────────────────────────────────────────────────────────────────────┤
│  서비스 개요:                                                           │
│  - 전 계좌 통합 자산 현황                                               │
│  - 자동 재무 분석 리포트                                                │
│  - 맞춤형 금융 상품 추천                                                │
│                                                                         │
│  개발 프로세스:                                                         │
│  1. 마이데이터 사업자 등록 (금융위원회)                                 │
│  2. 정보보호 관리체계(ISMS) 인증                                       │
│  3. 금융분야 마이데이터 표준API 연동 개발                               │
│  4. 정보통신망법 개인정보 처리 방침 준수                                │
│                                                                         │
│  기술 스택:                                                             │
│  - Frontend: React Native                                              │
│  - Backend: Spring Boot + MyData API Client                            │
│  - Security: OAuth 2.0, JWT, FAPI                                      │
│  - Database: PostgreSQL (암호화 저장)                                   │
│  - Compliance: ISMS, GDPR 준수                                         │
│                                                                         │
│  비용:                                                                  │
│  - 사업자 등록: 5천만원 자본금 요건                                     │
│  - ISMS 인증: 2천만원                                                  │
│  - 개발: 3억원 (6개월)                                                 │
│  - 연간 운영: 1억원                                                    │
│                                                                         │
│  기대 수익:                                                             │
│  - 구독료: 4,900원/월 × 10만 명 = 4.9억원/년                           │
│  - 제휴 수수료: 2억원/년                                               │
└─────────────────────────────────────────────────────────────────────────┘
```

### 도입 체크리스트

**법적/규제 준비**
- [ ] 마이데이터 사업자 신청 (금융위원회)
- [ ] ISMS 인증 취득
- [ ] 개인정보처리방침 작성
- [ ] 개인정보 영향평가 (PIA)

**기술적 준비**
- [ ] OAuth 2.0 / OpenID Connect 구현
- [ ] FAPI 보안 표준 준수
- [ ] 데이터 암호화 (전송/저장)
- [ ] Audit Log 시스템 구축

### 안티패턴 (Anti-patterns)

1. **과도한 데이터 요청**: 필요 이상의 동의 범위 요청 → 사용자 거부
2. **데이터 장기 보관**: 동의 기간 만료 후에도 데이터 보관 → 법적 위반
3. **불투명한 동의서**: 이해하기 어려운 동의서 → 이용자 신뢰 하락
4. **보안 소홀**: 액세스 토큰 탈취 → 대규모 정보 유출

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 도입 전 | 도입 후 | 개선 효과 |
|------|---------|---------|-----------|
| 금융 서비스 비교 시간 | 3일 | 10분 | -99.8% |
| 개인 자산 파악 시간 | 1시간 | 1분 | -98.3% |
| 금융 상품 가입 시간 | 1주 | 1일 | -85.7% |
| 데이터 주권 인식 | 20% | 75% | +275% |

### 미래 전망

1. **의료 마이데이터 확대**: EMR, 건강검진, 처방 데이터 통합
2. **공공 마이데이터**: 행정 서비스 원스톱 처리
3. **크로스보더 마이데이터**: 국경 간 데이터 이동
4. **AI + 마이데이터**: 개인 맞춤 AI 비서

### 참고 표준/가이드

- **GDPR Article 20**: 데이터 이동권
- **PSD2 (EU)**: 결제 서비스 지침
- **금융분야 마이데이터 표준API**: 금융보안원
- **개인정보보호법 제정법률**: 제15조~제22조

---

## 📌 관련 개념 맵

- [데이터 경제](./data_economy.md) - 마이데이터의 경제적 맥락
- [개인정보 비식별화](../09_governance/data_pseudonymization.md) - 가명정보 처리 기술
- [데이터 거버넌스](../09_governance/data_governance.md) - 데이터 관리 체계
- [OAuth 2.0](../08_platform/oauth2_security.md) - 인증 및 권한 위임 프로토콜
- [오픈뱅킹](../08_platform/open_banking.md) - 금융 데이터 공유 플랫폼
- [ISMS](../09_governance/isms_certification.md) - 정보보호 관리체계

---

## 👶 어린이를 위한 3줄 비유

**1단계 (무엇인가요?)**: 마이데이터는 내 정보를 내가 주인이 되게 하는 거예요. 예전에는 회사가 내 정보를 가지고 있었는데, 이제는 내가 내 정보를 가지고 원하는 곳에 보여줄 수 있어요.

**2단계 (어떻게 쓰나요?)**: 마이데이터 앱을 켜면 내 모든 은행 계좌가 한눈에 보여요. 그리고 "이 앱에게 내 정보를 줘도 돼?"라고 물어보면, 내가 "응!" 또는 "아니!"라고 정할 수 있어요. 나중에 마음이 바뀌면 언제든 "그만!"이라고 할 수도 있어요.

**3단계 (왜 중요한가요?)**: 마이데이터가 있으면 내 돈이 어디에 얼마나 있는지 쉽게 알 수 있어요. 또 다른 은행의 좋은 상품을 쉽게 찾아서 바꿀 수도 있어요. 내 정보는 내가 관리하니까 더 안심하고 쓸 수 있어요!
