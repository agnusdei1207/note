+++
title = "게이트웨이 모델 vs 제로 트러스트 모델 비교"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# 게이트웨이 모델 vs 제로 트러스트 모델 비교

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 게이트웨이 모델은 "경계 내부는 신뢰, 외부는 불신"하는 성곽(Castle) 모델이고, 제로 트러스트는 "위치无关 무조건 검증"하는 신뢰 없는 보안 패러다임입니다.
> 2. **가치**: 제로 트러스트는 클라우드, 원격 근무, BYOD 환경에서 내부자 위협과 측면 이동을 차단하여 침해 피해를 90%까지 축소합니다.
> 3. **융합**: NIST SP 800-207, Google BeyondCorp, Microsoft Zero Trust가 대표적 구현이며, SASE/ZTNA로 클라우드 서비스화되고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**게이트웨이 모델 (Perimeter-Based Security)**
- **정의**: 조직 네트워크의 경계(Perimeter)에 방화벽, IDS/IPS, VPN 등의 보안 게이트웨이를 배치하여 외부 위협을 차단하고, 내부는 신뢰하는 전통적 보안 모델
- **핵심 가정**: "내부망 사용자와 자산은 신뢰할 수 있다"
- **대표 기술**: 방화벽, DMZ, VPN, IDS/IPS, 프록시 서버

**제로 트러스트 모델 (Zero Trust Architecture)**
- **정의**: 네트워크 위치에 상관없이 모든 사용자, 기기, 애플리케이션을 불신하고, 접근 시마다 지속적으로 검증하는 보안 아키텍처 (NIST SP 800-207)
- **핵심 원칙**: "Never Trust, Always Verify" (절대 신뢰하지 말고 항상 검증하라)
- **대표 기술**: ZTNA, SASE, Micro-segmentation, IAM, MFA, EDR

#### 2. 비유를 통한 이해

**게이트웨이 모델 = 성곽(Castle)과 해자(Moat)**
```
        [ 외부: 위험한 세상 ]
               │
    ═══════════╪═══════════  (해자: 방화벽)
          ┌────┴────┐
          │  성문   │  (VPN, IDS/IPS)
          └────┬────┘
    ┌───────────┴───────────┐
    │                       │
    │   [내부: 안전한 곳]    │  ← 모든 내부인 신뢰
    │   ┌───┐ ┌───┐ ┌───┐  │
    │   │금고│ │창고│ │병영│  │
    │   └───┘ └───┘ └───┘  │
    │                       │
    └───────────────────────┘
```

**제로 트러스트 = 호텔 키카드 시스템**
```
        [ 누구나 입장 가능 ]
               │
          ┌────┴────┐
          │ 로비    │  ← 공간 자체는 개방
          └────┬────┘
    ┌───────────┴───────────┐
    │  각 객실마다 별도 인증  │
    │  ┌───┐ ┌───┐ ┌───┐   │
    │  │🔑101│ │🔑201│ │🔑301│  ← 각 방마다 키카드
    │  └───┘ └───┘ └───┘   │
    │                       │
    │  복도에서도 객실 접근  │  ← 내부 이동도 검증
    │  불가 (키카드 필요)    │
    └───────────────────────┘
```

#### 3. 등장 배경 및 발전 과정

| 시기 | 게이트웨이 모델 | 제로 트러스트 |
|:---|:---|:---|
| **1990년대** | 방화벽 보급, DMZ 개념 정립 | - |
| **2000년대 초** | VPN 도입, UTM 통합 | - |
| **2004년** | - | Jericho Forum: "De-perimeterization" 제안 |
| **2010년** | - | Google BeyondCorp 시작 |
| **2013년** | APT 공격 증가, 내부 위협 대두 | Forrester: Zero Trust 개념화 |
| **2017년** | - | NIST SP 800-207 초안 |
| **2020년** | 코로나19로 원격근무 확대 | 급격한 Zero Trust 도입 |
| **2021년** | - | 미국 행정명령 14028 (Zero Trust 의무화) |
| **현재** | 레거시 시스템에 잔존 | SASE, ZTNA로 클라우드 서비스화 |

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 두 모델의 아키텍처 비교

**게이트웨이 모델 아키텍처**
```text
                        [인터넷]
                           │
                    ┌──────▼──────┐
                    │   방화벽    │ ← 경계 보안 (Single Gateway)
                    │ (VPN/IDS)   │
                    └──────┬──────┘
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
    ▼                      ▼                      ▼
┌────────┐           ┌────────┐           ┌────────┐
│  DMZ   │           │ 내부망 │           │ 내부망 │
│ (공개) │           │ (신뢰) │           │ (신뢰) │
├────────┤           ├────────┤           ├────────┤
│Web Serv│           │DB Serv │           │File Srv│
│Mail Srv│           │App Serv│           │AD Serv │
└────────┘           └────────┘           └────────┘

특징:
- 내부망은 평문 통신
- 한 번 인증하면 자유 이동 (Lateral Movement 허용)
- 경계 뚫리면 전체 노출
```

**제로 트러스트 아키텍처**
```text
                        [인터넷]
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
    ▼                      ▼                      ▼
┌────────┐           ┌────────┐           ┌────────┐
│ 사용자 │           │  IoT   │           │ Branch │
│(재택)  │           │ Device │           │ Office │
└───┬────┘           └───┬────┘           └───┬────┘
    │                    │                    │
    └────────────────────┼────────────────────┘
                         │
              ┌──────────▼──────────┐
              │  Policy Decision    │
              │  Point (PDP)        │ ← 중앙 정책 엔진
              │  - Identity: IAM    │
              │  - Device: MDM/EDR  │
              │  - Context: UEBA    │
              └──────────┬──────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
    │ Policy  │    │ Policy  │    │ Policy  │
    │Enforce- │    │Enforce- │    │Enforce- │
    │ment(PEP)│    │ment(PEP)│    │ment(PEP)│
    └────┬────┘    └────┬────┘    └────┬────┘
         │               │               │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
    │ App A   │    │ App B   │    │ App C   │
    │(마이크로│    │(마이크로│    │(마이크로│
    │ 세그먼트)│    │ 세그먼트)│    │ 세그먼트)│
    └─────────┘    └─────────┘    └─────────┘

특징:
- 모든 통신 암호화 (mTLS)
- 접근마다 정책 평가
- 마이크로 세그멘테이션
- 최소 권한 원칙
```

#### 2. 핵심 구성 요소 비교

| 구성 요소 | 게이트웨이 모델 | 제로 트러스트 |
|:---|:---|:---|
| **신뢰 기준** | 네트워크 위치 (내부/외부) | 다중 요소 (Identity + Device + Context) |
| **인증 지점** | 네트워크 진입 시 1회 | 모든 리소스 접근 시마다 |
| **권한 범위** | 네트워크 전체 | 특정 애플리케이션/데이터 |
| **암호화** | 경계 간만 (VPN) | 모든 통신 (mTLS) |
| **가시성** | 경계 트래픽만 | 모든 트래픽 |
| **정책 단위** | IP/Subnet | 사용자/기기/앱/데이터 |

#### 3. 심층 동작 원리: 접근 제어 흐름 비교

**게이트웨이 모델 접근 흐름**
```
① 사용자 VPN 연결
   └─ [인증: ID/PW] → 성공 시 내부망 접근 권한 획득

② 내부 리소스 접근
   └─ [추가 인증 없음] → 모든 내부 서버 접근 가능

③ 측면 이동
   └─ [제한 없음] → Web서버 → DB서버 → 파일서버 자유 이동

④ 문제점
   └─ VPN 계정 탈취 시 내부망 전체 노출
   └─ 내부자 위협에 무방비
```

**제로 트러스트 접근 흐름**
```
① 사용자 앱 접근 요청
   └─ [Identity 평가] → MFA, SSO, 행위 분석

② 기기 상태 평가
   └─ [Device 평가] → EDR, MDM, 패치 상태, 인증서

③ 컨텍스트 평가
   └─ [Context 평가] → 위치, 시간, 위험 점수, 행위 이상

④ 정책 결정 (PDP)
   └─ [Policy 평가] → 5개 신호 종합 → 허용/거부/조건부

⑤ 정책 시행 (PEP)
   └─ [Enforcement] → 세션 수립, 지속적 검증, 로깅

⑥ 세션 모니터링
   └─ [지속 검증] → 행위 이상 시 세션 종료
```

#### 4. 핵심 알고리즘 & 실무 코드: Zero Trust 정책 엔진

```python
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime
import hashlib

class TrustLevel(Enum):
    FULL = "full"           # 완전 신뢰
    LIMITED = "limited"     # 제한적 신뢰
    UNTRUSTED = "untrusted" # 불신

class AccessDecision(Enum):
    ALLOW = "allow"
    DENY = "deny"
    STEP_UP = "step_up"     # 추가 인증 필요
    MONITOR = "monitor"     # 허용하되 모니터링

@dataclass
class AccessRequest:
    """접근 요청 컨텍스트"""
    user_id: str
    device_id: str
    resource_id: str
    action: str  # read, write, execute, delete
    source_ip: str
    location: Tuple[float, float]  # 위도, 경도
    timestamp: datetime
    session_id: str

@dataclass
class IdentityScore:
    """신원 신뢰 점수"""
    mfa_verified: bool
    password_age_days: int
    recent_failed_logins: int
    behavior_anomaly_score: float  # 0.0 ~ 1.0

@dataclass
class DeviceScore:
    """기기 신뢰 점수"""
    is_managed: bool
    has_edr: bool
    os_patched: bool
    certificate_valid: bool
    malware_detected: bool

@dataclass
class ContextScore:
    """컨텍스트 신뢰 점수"""
    is_normal_location: bool
    is_normal_time: bool
    network_trust_level: TrustLevel
    concurrent_sessions: int

class ZeroTrustPolicyEngine:
    """제로 트러스트 정책 결정 엔진"""

    def __init__(self):
        self.identity_weight = 0.35
        self.device_weight = 0.30
        self.context_weight = 0.35
        self.trust_threshold = 0.7  # 70% 이상이어야 허용

    def evaluate_access(
        self,
        request: AccessRequest,
        identity: IdentityScore,
        device: DeviceScore,
        context: ContextScore
    ) -> Dict:
        """
        접근 요청 평가

        Returns:
            {
                "decision": AccessDecision,
                "trust_score": float,
                "breakdown": dict,
                "conditions": list,
                "log_id": str
            }
        """
        # 각 영역별 점수 계산
        identity_score = self._calculate_identity_score(identity)
        device_score = self._calculate_device_score(device)
        context_score = self._calculate_context_score(context)

        # 가중 평균
        trust_score = (
            identity_score * self.identity_weight +
            device_score * self.device_weight +
            context_score * self.context_weight
        )

        # 결정 로직
        decision, conditions = self._make_decision(
            trust_score,
            identity,
            device,
            context
        )

        # 로그 ID 생성
        log_id = self._generate_log_id(request)

        return {
            "decision": decision,
            "trust_score": round(trust_score, 3),
            "breakdown": {
                "identity": round(identity_score, 3),
                "device": round(device_score, 3),
                "context": round(context_score, 3)
            },
            "conditions": conditions,
            "log_id": log_id,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _calculate_identity_score(self, identity: IdentityScore) -> float:
        """신원 신뢰 점수 계산"""
        score = 0.0

        # MFA 인증 (가장 중요)
        if identity.mfa_verified:
            score += 0.4

        # 비밀번호 나이 (최신일수록 좋음)
        if identity.password_age_days <= 90:
            score += 0.2
        elif identity.password_age_days <= 180:
            score += 0.1

        # 최근 로그인 실패
        if identity.recent_failed_logins == 0:
            score += 0.2
        elif identity.recent_failed_logins <= 2:
            score += 0.1

        # 행위 이상 점수 (낮을수록 좋음)
        score += 0.2 * (1 - identity.behavior_anomaly_score)

        return min(score, 1.0)

    def _calculate_device_score(self, device: DeviceScore) -> float:
        """기기 신뢰 점수 계산"""
        score = 0.0

        if device.is_managed:
            score += 0.3

        if device.has_edr:
            score += 0.25

        if device.os_patched:
            score += 0.25

        if device.certificate_valid:
            score += 0.2

        # 악성코드 탐지 시 0점
        if device.malware_detected:
            score = 0.0

        return score

    def _calculate_context_score(self, context: ContextScore) -> float:
        """컨텍스트 신뢰 점수 계산"""
        score = 0.0

        if context.is_normal_location:
            score += 0.3

        if context.is_normal_time:
            score += 0.2

        if context.network_trust_level == TrustLevel.FULL:
            score += 0.3
        elif context.network_trust_level == TrustLevel.LIMITED:
            score += 0.15

        if context.concurrent_sessions <= 2:
            score += 0.2
        elif context.concurrent_sessions <= 5:
            score += 0.1

        return score

    def _make_decision(
        self,
        trust_score: float,
        identity: IdentityScore,
        device: DeviceScore,
        context: ContextScore
    ) -> Tuple[AccessDecision, List[str]]:
        """접근 결정 및 조건 도출"""
        conditions = []

        # 악성코드 탐지 시 즉시 거부
        if device.malware_detected:
            return AccessDecision.DENY, ["악성코드 탐지됨"]

        # MFA 미인증 시 추가 인증 요구
        if not identity.mfa_verified:
            return AccessDecision.STEP_UP, ["MFA 인증 필요"]

        # 신뢰 점수 기반 결정
        if trust_score >= self.trust_threshold:
            if trust_score < 0.85:
                conditions.append("모니터링 강화")
            return AccessDecision.ALLOW, conditions

        elif trust_score >= 0.5:
            return AccessDecision.STEP_UP, ["추가 인증 필요"]

        else:
            return AccessDecision.DENY, ["신뢰 점수 미달"]

    def _generate_log_id(self, request: AccessRequest) -> str:
        """감사 로그 ID 생성"""
        data = f"{request.user_id}{request.device_id}{request.resource_id}{request.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

# 사용 예시
engine = ZeroTrustPolicyEngine()

# 접근 요청
request = AccessRequest(
    user_id="user@company.com",
    device_id="laptop-001",
    resource_id="s3://confidential-data",
    action="read",
    source_ip="203.0.113.50",
    location=(37.5665, 126.9780),  # 서울
    timestamp=datetime.utcnow(),
    session_id="sess_abc123"
)

# 신원 평가
identity = IdentityScore(
    mfa_verified=True,
    password_age_days=30,
    recent_failed_logins=0,
    behavior_anomaly_score=0.1
)

# 기기 평가
device = DeviceScore(
    is_managed=True,
    has_edr=True,
    os_patched=True,
    certificate_valid=True,
    malware_detected=False
)

# 컨텍스트 평가
context = ContextScore(
    is_normal_location=True,
    is_normal_time=True,
    network_trust_level=TrustLevel.LIMITED,
    concurrent_sessions=1
)

# 접근 평가
result = engine.evaluate_access(request, identity, device, context)

print(f"결정: {result['decision'].value}")
print(f"신뢰 점수: {result['trust_score']}")
print(f"세부 점수: {result['breakdown']}")
print(f"조건: {result['conditions']}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 포괄적 비교표

| 비교 항목 | 게이트웨이 모델 | 제로 트러스트 |
|:---|:---|:---|
| **기본 가정** | 내부는 신뢰, 외부는 불신 | 모든 것을 불신 |
| **보안 경계** | 네트워크 경계 (방화벽) | 각 리소스/데이터 |
| **인증 시점** | 네트워크 진입 시 1회 | 모든 접근 시 |
| **권한 범위** | 네트워크 전체 | 특정 앱/데이터 |
| **암호화** | 경계 간만 (VPN) | 모든 통신 (mTLS) |
| **가시성** | 경계 트래픽만 | 전체 트래픽 |
| **측면 이동** | 허용 | 차단 |
| **내부자 위협** | 취약 | 강력 대응 |
| **원격 근무** | VPN 필요 | 위치 무관 |
| **클라우드 적합** | 낮음 | 높음 |
| **구현 복잡도** | 낮음 | 높음 |
| **도입 비용** | 낮음 | 높음 |
| **운영 비용** | 중간 | 높음 |

#### 2. 위협 시나리오별 방어력 비교

| 위협 시나리오 | 게이트웨이 모델 | 제로 트러스트 | 이유 |
|:---|:---|:---|:---|
| **외부 해킹** | 중간 | 높음 | 둘 다 방어하지만 ZT는 내부 이동 차단 |
| **피싱 공격** | 낮음 | 높음 | ZT는 계정 탈취 후에도 행위 분석 |
| **내부자 위협** | 매우 낮음 | 높음 | ZT는 최소 권한, 행위 모니터링 |
| **측면 이동** | 매우 낮음 | 높음 | ZT는 마이크로 세그멘테이션 |
| **랜섬웨어 확산** | 낮음 | 높음 | ZT는 세그먼트 격리 |
| **APT 공격** | 낮음 | 높음 | ZT는 지속적 검증 |
| **클라우드 데이터 유출** | 낮음 | 높음 | ZT는 클라우드 네이티브 |
| **공급망 공격** | 낮음 | 중간 | ZT는 제3자 접근 통제 |

#### 3. 과목 융합 관점 분석

- **네트워크**: SDN, Micro-segmentation, SASE/ZTNA
- **시스템**: EDR, MDM, TPM, HSM
- **애플리케이션**: mTLS, API Gateway, OAuth 2.0, OIDC
- **데이터베이스**: Row-Level Security, Dynamic Data Masking
- **클라우드**: IAM, KMS, CloudTrail, GuardDuty

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 중견 금융사 Zero Trust 전환**
- 상황: 기존 VPN 기반 게이트웨이 모델, 내부자 위협 우려
- 판단: 단계적 Zero Trust 전환
- 핵심 결정:
  - Phase 1 (6개월): IAM 강화, MFA 100%, PAM 도입
  - Phase 2 (1년): ZTNA 도입, VPN 대체
  - Phase 3 (1년): 마이크로 세그멘테이션, 데이터 보호
- 효과: 내부자 위협 탐지율 95% 향상, VPN 운영비 60% 절감

**시나리오 2: SaaS 스타트업 보안 설계**
- 상황: 신규 서비스, 클라우드 네이티브, Zero Trust 원칙 적용
- 판단: 게이트웨이 없이 Zero Trust로 시작
- 핵심 결정:
  - IdP (Okta) 중심 인증
  - Cloudflare Access로 ZTNA
  - 모든 통신 mTLS
  - RBAC + ABAC 하이브리드
- 효과: VPN 없는 보안, 고객 신뢰도 향상

**시나리오 3: 제조업 OT/IT 융합 보안**
- 상황: 스마트팩토리, IT망 Zero Trust, OT망은 격리 유지
- 판단: 하이브리드 모델
- 핵심 결정:
  - IT망: Zero Trust 원칙
  - OT망: 에어갭 + 일방향 게이트웨이
  - IT-OT 경계: 데이터 다이오드 + Zero Trust
- 효과: OT 가용성 유지, IT 보안 강화

#### 2. 도입 시 고려사항 (체크리스트)

**Zero Trust 도입 전제 조건**
- [ ] IAM/IdP 인프라 준비 (SSO, MFA)
- [ ] 자산 인벤토리 완비 (사용자, 기기, 앱, 데이터)
- [ ] 데이터 분류 완료
- [ ] 네트워크 토폴로지 파악
- [ ] 레거시 시스템 영향도 분석

**단계적 도입 로드맵**
1. **가시화**: 자산 발견, 트래픽 분석, 의존성 매핑
2. **ID 강화**: MFA, SSO, PAM, 권한 정리
3. **기기 보안**: EDR, MDM, 인증서
4. **네트워크**: ZTNA, 마이크로 세그멘테이션
5. **데이터**: 분류, DLP, 암호화
6. **모니터링**: SIEM, UEBA, SOAR

#### 3. 안티패턴 (Anti-patterns)

| 안티패턴 | 문제점 | 올바른 접근 |
|:---|:---|:---|
| **VPN 위에 Zero Trust** | 내부망 신뢰 유지 | VPN 제거, ZTNA로 대체 |
| **도구만 도입** | 정책 없이 기술만 투입 | 정책 먼저 정의, 기술은 구현 수단 |
| **일시 전환** | 서비스 중단, 사용자 반발 | 단계적 마이그레이션 |
| **100% Zero Trust 고집** | 레거시 호환 불가 | 하이브리드 허용, 격리된 레거시 |

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | 게이트웨이 | 제로 트러스트 | 비고 |
|:---|:---|:---|:---|
| 침해 피해 범위 | 전체 네트워크 | 단일 세그먼트 | 90% 축소 |
| 내부자 위협 탐지 | 20% | 85% | UEBA 기반 |
| VPN 운영 비용 | 100% | 30% | ZTNA 전환 시 |
| 원격근무 보안 | 낮음 | 높음 | 위치 무관 보안 |
| 규정 준수 | 중간 | 높음 | NIST SP 800-207 |

#### 2. 미래 전망 및 진화 방향

- **SASE로 통합**: 네트워크 + 보안 클라우드 서비스
- **AI 기반 지속 검증**: 실시간 행위 분석, 예측적 차단
- **Decentralized Identity**: 블록체인 기반 자기 주권 ID
- **Hardware-Backed Trust**: TPM, HSM, SGX 기반 루트 오브 트러스트

#### 3. 참고 표준/가이드

- **NIST SP 800-207**: Zero Trust Architecture (2020)
- **NIST SP 800-207A**: Zero Trust Architecture Maturity Model
- **CISA Zero Trust Maturity Model**: 5 Pillars (Identity, Device, Network, App, Data)
- **DoD Zero Trust Strategy**: US Department of Defense
- **Google BeyondCorp**: Zero Trust 구현 사례

---

### 관련 개념 맵 (Knowledge Graph)

- [제로 트러스트 아키텍처](@/studynotes/09_security/01_policy/zero_trust_architecture.md) : Zero Trust 심화
- [마이크로 세그멘테이션](@/studynotes/09_security/01_policy/micro_segmentation.md) : 측면 이동 차단
- [심층 방어](@/studynotes/09_security/01_policy/defense_in_depth.md) : 다층 보안 전략
- [SASE/ZTNA](@/studynotes/09_security/03_network_security/sase.md) : 클라우드 네이티브 Zero Trust
- [최소 권한 원칙](@/studynotes/09_security/01_policy/security_principles.md) : Zero Trust의 권한 철학

---

### 어린이를 위한 3줄 비유 설명

1. **성곽 같은 게이트웨이**: 옛날에는 큰 성벽을 쌓았어요. 성벽 안은 안전하니까 문만 잘 지키면 됐죠. 하지만 스파이가 안에 들어오면 끝이에요.
2. **호텔 키카드 같은 제로 트러스트**: 요즘 호텔은 각 방마다 키카드가 필요해요. 로비를 지나서도, 복도를 지나서도 방마다 키를 대야 하죠.
3. **왜 바뀌었을까요**: 컴퓨터도 마찬가지예요. 집에서 회사로, 카페에서 어디서나 일하니까 성벽이 필요 없어요. 대신 모든 문마다 열쇠를 확인하는 거죠.
