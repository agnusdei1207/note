+++
title = "SASE / ZTNA (Secure Access Service Edge)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# SASE / ZTNA (Secure Access Service Edge)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SASE는 네트워크(SD-WAN)와 보안(NGFW, SWG, CASB, ZTNA)을 클라우드 엣지에서 통합 제공하는 아키텍처이며, ZTNA는 "절대 신뢰하지 말고 항상 검증하라"는 원칙으로 애플리케이션별 세분화된 접근 통제를 제공합니다.
> 2. **가치**: 원격 근무, 클라우드 전환으로 기업 경계가 사라진 시대에 사용자/디바이스/위치에 무관하게 일관된 보안을 제공하며, VPN의 한계(과도한 권한, 측면 이동)를 근본적으로 해결합니다.
> 3. **융합**: CASB, SWG, FWaaS, DLP와 결합하여 SASE 프레임워크를 완성하며, NIST SP 800-207 제로 트러스트 아키텍처의 핵심 구현체입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**SASE(Secure Access Service Edge)**는 Gartner가 2019년 정의한 프레임워크로, 네트워크와 보안 기능을 클라우드 서비스로 통합하여 엣지에서 제공합니다. **ZTNA(Zero Trust Network Access)**는 SASE의 핵심 구성요소로, 사용자와 애플리케이션 간의 안전한 접근을 제어합니다.

```
SASE 구성 요소:
┌─────────────────────────────────────────────────────────┐
│                        SASE                              │
│                                                          │
│  네트워크 기능              보안 기능                     │
│  ┌────────────────┐       ┌────────────────────────┐    │
│  │ SD-WAN         │       │ NGFW / FWaaS           │    │
│  │ CDN            │       │ SWG (Secure Web GW)    │    │
│  │ WAN Optimizer  │       │ CASB (Cloud Access)    │    │
│  │                │       │ ZTNA (Zero Trust NA)   │    │
│  │                │       │ DLP                    │    │
│  │                │       │ RBI (Remote Browser)   │    │
│  └────────────────┘       └────────────────────────┘    │
│                                                          │
│  공통: 정책 엔진, ID 관리, 위협 방지, 로깅              │
└─────────────────────────────────────────────────────────┘
```

#### 2. 비유를 통한 이해
SASE/ZTNA는 **'호텔 키카드 시스템'**에 비유할 수 있습니다.

- **VPN (전통적)**: 마스터 키를 받아 모든 방에 접근 가능
  - 로비에서 한 번 인증 → 건물 전체 접근
- **ZTNA**: 필요한 방만 열리는 키카드
  - 각 방마다 권한 확인
  - 101호 키 → 101호만 접근, 102호 불가
- **SASE**: 키카드 + 컨시어지 + 보안 서비스 통합

#### 3. 등장 배경 및 발전 과정
1. **2010년**: BeyondCorp (Google) - "No more VPN"
2. **2017년**: Google BeyondCorp Commercial (now Google BeyondCorp Enterprise)
3. **2018년**: Zscaler ZPA 상용화
4. **2019년**: Gartner SASE 용어 정의
5. **2020년**: COVID-19로 원격 근무 급증 → SASE 도입 가속
6. **2021년**: NIST SP 800-207 Zero Trust Architecture
7. **2022년**: SASE 시장 $50억+ 성장
8. **2025년 예상**: SASE 표준화, PQC 통합

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. VPN vs ZTNA 비교

| 특성 | VPN | ZTNA |
|:---|:---|:---|
| **접근 범위** | 네트워크 전체 | 애플리케이션별 |
| **신뢰 모델** | 경계 내 신뢰 | 무조건 불신 |
| **인증** | 1회 (연결 시) | 지속적 (세션마다) |
| **가시성** | 제한적 (암호화) | 전체 (에이전트) |
| **측면 이동** | 가능 | 불가능 |
| **성능** | 백홀 필요 | 분산 엣지 |
| **관리** | 하드웨어 VPN 집중 | 클라우드 분산 |

#### 2. ZTNA 아키텍처 다이어그램

```
=== ZTNA 아키텍처 (Controller + Gateway 모델) ===

┌─────────────────────────────────────────────────────────────────────┐
│                        ZTNA Control Plane                            │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    Policy Decision Point                        │ │
│  │                                                                 │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │ │
│  │  │    Identity  │  │   Device     │  │   Policy     │         │ │
│  │  │    Provider  │  │   Trust      │  │   Engine     │         │ │
│  │  │    (IdP)     │  │   Score      │  │              │         │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │ │
│  │          │                 │                 │                  │ │
│  │          └─────────────────┼─────────────────┘                  │ │
│  │                            ▼                                    │ │
│  │  ┌──────────────────────────────────────────────────────────┐  │ │
│  │  │                  Access Decision                          │  │ │
│  │  │                                                           │  │ │
│  │  │   IF user = "alice"                                       │  │ │
│  │  │   AND device_trust > 70                                   │  │ │
│  │  │   AND location = "allowed_country"                        │  │ │
│  │  │   AND time = business_hours                               │  │ │
│  │  │   THEN allow access to App "Sales-Portal"                 │  │ │
│  │  │                                                           │  │ │
│  │  └──────────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ ZTNA Gateway  │       │ ZTNA Gateway  │       │ ZTNA Gateway  │
│   (Region A)  │       │   (Region B)  │       │   (Cloud)     │
│               │       │               │       │               │
│  App Broker   │       │  App Broker   │       │  App Broker   │
└───────┬───────┘       └───────┬───────┘       └───────┬───────┘
        │                       │                       │
        │         Micro-tunnel (mTLS)                   │
        │              ▲                                │
        │              │                                │
┌───────┴───────┐     │        ┌───────────────────────┴───────┐
│   Private     │     │        │        Application            │
│ Application   │◄────┼────────│        Connector              │
│   Server      │     │        │   (App-Side Component)        │
└───────────────┘     │        └───────────────────────────────┘
                      │
              ┌───────┴───────┐
              │    User       │
              │   Endpoint    │
              │  (ZTNA Agent) │
              └───────────────┘

동작 원리:
1. 사용자 에이전트 → Control Plane 인증 요청
2. IdP + Device Trust 평가
3. 정책 엔진 → 앱별 접근 권한 결정
4. 승인 시 → 해당 Gateway로 Micro-tunnel 생성
5. Gateway → App Connector → Private App 연결
6. 세션 종료 시 tunnel 즉시 해제

===========================================

=== SASE 통합 아키텍처 ===

                         [ Internet ]
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │              SASE Edge (PoP)                │
        │                                              │
        │  ┌──────────────────────────────────────┐   │
        │  │         Security Stack               │   │
        │  │                                      │   │
        │  │  ┌────────┐  ┌────────┐  ┌────────┐ │   │
        │  │  │  SWG   │  │  CASB  │  │  FWaaS │ │   │
        │  │  │        │  │        │  │        │ │   │
        │  │  └────────┘  └────────┘  └────────┘ │   │
        │  │                                      │   │
        │  │  ┌────────┐  ┌────────┐  ┌────────┐ │   │
        │  │  │  ZTNA  │  │  DLP   │  │  RBI   │ │   │
        │  │  │        │  │        │  │        │ │   │
        │  │  └────────┘  └────────┘  └────────┘ │   │
        │  │                                      │   │
        │  └──────────────────────────────────────┘   │
        │                                              │
        │  ┌──────────────────────────────────────┐   │
        │  │         Network Stack                │   │
        │  │                                      │   │
        │  │  ┌────────┐  ┌────────┐  ┌────────┐ │   │
        │  │  │ SD-WAN │  │  CDN   │  │  QoS   │ │   │
        │  │  │        │  │        │  │        │ │   │
        │  │  └────────┘  └────────┘  └────────┘ │   │
        │  │                                      │   │
        │  └──────────────────────────────────────┘   │
        │                                              │
        └─────────────────────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │   Remote    │    │   Branch    │    │   Cloud     │
    │   User      │    │   Office    │    │   Apps      │
    │             │    │             │    │             │
    │ (ZTNA Agent)│    │ (SD-WAN CPE)│    │  (SaaS/IaaS)│
    └─────────────┘    └─────────────┘    └─────────────┘
```

#### 3. 심층 동작 원리: ZTNA 정책 엔진

```python
"""
ZTNA 정책 엔진 및 접근 제어 구현
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime, time
import hashlib

class TrustLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4

@dataclass
class Device:
    """디바이스 정보"""
    device_id: str
    hostname: str
    os_type: str
    os_version: str
    compliance_status: bool  # MDM/Patch 상태
    disk_encrypted: bool
    antivirus_running: bool
    firewall_enabled: bool
    last_checkin: datetime

    @property
    def trust_score(self) -> int:
        """디바이스 신뢰 점수 (0-100)"""
        score = 0
        if self.compliance_status:
            score += 25
        if self.disk_encrypted:
            score += 25
        if self.antivirus_running:
            score += 25
        if self.firewall_enabled:
            score += 15
        if self.os_version:  # 최신 버전 확인 로직
            score += 10
        return score

@dataclass
class User:
    """사용자 정보"""
    user_id: str
    username: str
    email: str
    groups: List[str]
    department: str
    mfa_enabled: bool
    last_login: datetime
    risk_score: int  # 0-100, UEBA 기반

@dataclass
class Context:
    """접속 컨텍스트"""
    source_ip: str
    geolocation: str
    device: Device
    timestamp: datetime
    network_type: str  # "corporate", "public", "mobile"

@dataclass
class Application:
    """애플리케이션 정의"""
    app_id: str
    name: str
    protocol: str
    host: str
    port: int
    sensitivity: str  # "public", "internal", "confidential"
    allowed_groups: List[str]

@dataclass
class AccessPolicy:
    """접근 정책"""
    name: str
    priority: int
    applications: List[str]  # 대상 앱
    users: List[str]  # 대상 사용자/그룹
    conditions: Dict  # 조건
    action: str  # "allow", "deny", "step_up_auth"

class ZTNAPolicyEngine:
    """
    ZTNA 정책 엔진

    지속적 검증 (Continuous Verification):
    - 사용자 신원
    - 디바이스 상태
    - 위치/시간
    - 행위 이상
    """

    def __init__(self):
        self.policies: List[AccessPolicy] = []
        self.session_cache = {}

    def evaluate_access(self, user: User, context: Context,
                        application: Application) -> dict:
        """
        접근 요청 평가

        Returns:
            {
                'decision': 'allow' | 'deny' | 'step_up',
                'reason': str,
                'session_duration': int (seconds),
                'conditions': list
            }
        """
        result = {
            'decision': 'deny',
            'reason': '',
            'session_duration': 0,
            'conditions': []
        }

        # 1. 사용자 그룹 확인
        group_match = any(
            g in application.allowed_groups
            for g in user.groups
        )
        if not group_match:
            result['reason'] = f"User groups {user.groups} not in allowed groups {application.allowed_groups}"
            return result

        # 2. 디바이스 신뢰 점수 확인
        device_score = context.device.trust_score
        min_score = self._get_min_device_score(application.sensitivity)

        if device_score < min_score:
            result['decision'] = 'step_up'
            result['reason'] = f"Device trust score {device_score} below minimum {min_score}"
            result['conditions'] = ['device_remediation']
            return result

        # 3. 위치 기반 검증
        if not self._check_geolocation(context.geolocation, application.sensitivity):
            result['reason'] = f"Geolocation {context.geolocation} not allowed"
            return result

        # 4. 시간 기반 검증
        if not self._check_time_access(context.timestamp):
            result['reason'] = "Access outside allowed hours"
            return result

        # 5. 사용자 위험 점수 확인
        if user.risk_score > 70:
            result['decision'] = 'step_up'
            result['reason'] = f"User risk score {user.risk_score} requires additional verification"
            result['conditions'] = ['mfa_required']
            return result

        # 6. 네트워크 타입 확인
        if context.network_type == "public" and application.sensitivity == "confidential":
            result['decision'] = 'step_up'
            result['reason'] = "Confidential app access from public network requires VPN"
            result['conditions'] = ['vpn_required']
            return result

        # 모든 검증 통과
        result['decision'] = 'allow'
        result['reason'] = "Access granted"
        result['session_duration'] = self._calculate_session_duration(application.sensitivity)

        return result

    def _get_min_device_score(self, sensitivity: str) -> int:
        """민감도별 최소 디바이스 점수"""
        scores = {
            'public': 30,
            'internal': 50,
            'confidential': 80
        }
        return scores.get(sensitivity, 70)

    def _check_geolocation(self, location: str, sensitivity: str) -> bool:
        """위치 기반 접근 확인"""
        # 실제로는 GeoIP DB + 정책 사용
        blocked_countries = ['XX', 'YY']  # 예시
        if location in blocked_countries:
            return False

        if sensitivity == 'confidential':
            allowed_countries = ['KR', 'US']
            return location in allowed_countries

        return True

    def _check_time_access(self, timestamp: datetime) -> bool:
        """시간 기반 접근 확인"""
        # 업무 시간 (9:00 - 18:00)
        current_time = timestamp.time()
        start_time = time(9, 0)
        end_time = time(18, 0)

        # 주말 제외
        if timestamp.weekday() >= 5:
            return False

        return start_time <= current_time <= end_time

    def _calculate_session_duration(self, sensitivity: str) -> int:
        """세션 지속 시간 계산"""
        durations = {
            'public': 8 * 3600,      # 8시간
            'internal': 4 * 3600,    # 4시간
            'confidential': 1 * 3600 # 1시간
        }
        return durations.get(sensitivity, 3600)


class ZTNAConnector:
    """
    ZTNA Connector (애플리케이션 측 컴포넌트)

    역할:
    - Private App과 Gateway 간의 터널 관리
    - 아웃바운드 연결만 (인바운드 방화벽 불필요)
    """

    def __init__(self, app_id: str, gateway_url: str):
        self.app_id = app_id
        self.gateway_url = gateway_url
        self.tunnel_active = False

    def register(self, token: str) -> bool:
        """
        Connector 등록

        1. Gateway로 아웃바운드 연결
        2. mTLS 핸드쉐이크
        3. 앱 ID 바인딩
        """
        # 실제로는 WebSocket/mTLS 연결
        print(f"[Connector] Registering app {self.app_id} with gateway {self.gateway_url}")
        self.tunnel_active = True
        return True

    def handle_request(self, request: dict) -> dict:
        """사용자 요청 처리"""
        if not self.tunnel_active:
            raise RuntimeError("Tunnel not active")

        # 로컬 앱으로 요청 전달
        print(f"[Connector] Forwarding request to local app: {request}")
        return {'status': 'ok', 'data': 'response_from_app'}


# SASE 시뮬레이션
class SASEGateway:
    """
    SASE Gateway (PoP)

    통합 보안 스택:
    - SWG: 웹 트래픽 필터링
    - CASB: 클라우드 앱 가시성
    - ZTNA: Private App 접근
    - FWaaS: 네트워크 방화벽
    """

    def __init__(self, pop_location: str):
        self.pop_location = pop_location
        self.ztna_engine = ZTNAPolicyEngine()

    def process_request(self, user: User, context: Context,
                        destination: str, traffic_type: str) -> dict:
        """
        요청 처리

        traffic_type:
        - "web": SWG 처리
        - "cloud_app": CASB 처리
        - "private_app": ZTNA 처리
        """
        result = {
            'action': 'allow',
            'logs': [],
            'transformations': []
        }

        # 1. 트래픽 분류
        result['logs'].append(f"Classified as {traffic_type}")

        # 2. 보안 검사
        if traffic_type == "web":
            # SWG: URL 필터링, 악성코드 검사
            if self._is_malicious_url(destination):
                result['action'] = 'block'
                result['logs'].append(f"Blocked malicious URL: {destination}")
                return result

        elif traffic_type == "cloud_app":
            # CASB: 섀도우 IT 탐지, DLP
            if self._contains_sensitive_data(context):
                result['action'] = 'alert'
                result['logs'].append("DLP alert: Sensitive data detected")

        elif traffic_type == "private_app":
            # ZTNA: 접근 정책 평가
            app = Application(
                app_id="sales-portal",
                name="Sales Portal",
                protocol="https",
                host="sales.internal",
                port=443,
                sensitivity="confidential",
                allowed_groups=["sales", "executives"]
            )

            access_result = self.ztna_engine.evaluate_access(user, context, app)
            result['action'] = access_result['decision']
            result['logs'].append(f"ZTNA decision: {access_result['reason']}")

        return result

    def _is_malicious_url(self, url: str) -> bool:
        """악성 URL 확인 (실제로는 위협 intelligence 사용)"""
        malicious_domains = ['malware.com', 'phishing.net']
        return any(d in url for d in malicious_domains)

    def _contains_sensitive_data(self, context: Context) -> bool:
        """민감 데이터 포함 확인"""
        # 실제로는 DLP 엔진 사용
        return False


# 사용 예시
def sase_ztna_demo():
    """SASE/ZTNA 데모"""

    print("=" * 60)
    print("ZTNA 접근 제어 데모")
    print("=" * 60)

    # 사용자 생성
    user = User(
        user_id="u001",
        username="alice",
        email="alice@company.com",
        groups=["sales"],
        department="Sales",
        mfa_enabled=True,
        last_login=datetime.now(),
        risk_score=20
    )

    # 디바이스 생성
    device = Device(
        device_id="d001",
        hostname="alice-laptop",
        os_type="Windows",
        os_version="10.0.19045",
        compliance_status=True,
        disk_encrypted=True,
        antivirus_running=True,
        firewall_enabled=True,
        last_checkin=datetime.now()
    )

    # 컨텍스트 생성
    context = Context(
        source_ip="203.0.113.50",
        geolocation="KR",
        device=device,
        timestamp=datetime.now(),
        network_type="public"
    )

    # 정책 엔진 평가
    engine = ZTNAPolicyEngine()
    app = Application(
        app_id="sales-portal",
        name="Sales Portal",
        protocol="https",
        host="sales.internal",
        port=443,
        sensitivity="confidential",
        allowed_groups=["sales", "executives"]
    )

    result = engine.evaluate_access(user, context, app)

    print(f"\n[접근 요청]")
    print(f"  사용자: {user.username} (그룹: {user.groups})")
    print(f"  디바이스: {device.hostname} (점수: {device.trust_score})")
    print(f"  위치: {context.geolocation}")
    print(f"  네트워크: {context.network_type}")
    print(f"  앱: {app.name} (민감도: {app.sensitivity})")

    print(f"\n[평가 결과]")
    print(f"  결정: {result['decision']}")
    print(f"  사유: {result['reason']}")
    if result['conditions']:
        print(f"  추가 조건: {result['conditions']}")


def vpn_vs_ztna_comparison():
    """VPN vs ZTNA 비교"""
    print("\n" + "=" * 60)
    print("VPN vs ZTNA 비교")
    print("=" * 60)

    comparisons = [
        ("접근 범위", "네트워크 전체 (10.0.0.0/8)", "앱별 (sales-portal)"),
        ("신뢰 모델", "VPN 연결 = 신뢰", "항상 검증"),
        ("측면 이동", "가능 (동일 네트워크)", "불가능 (격리 터널)"),
        ("공격 노출", "전체 네트워크", "단일 앱"),
        ("성능", "백홀로 중앙 집중", "엣지 분산"),
        ("인바운드 포트", "필요 (방화벽 오픈)", "불필요 (아웃바운드만)"),
    ]

    print(f"\n{'특성':<15} {'VPN':<30} {'ZTNA'}")
    print("-" * 70)
    for feature, vpn, ztna in comparisons:
        print(f"{feature:<15} {vpn:<30} {ztna}")


if __name__ == "__main__":
    sase_ztna_demo()
    vpn_vs_ztna_comparison()
```

#### 4. SASE 벤더 비교

| 벤더 | 제품 | 강점 | 약점 |
|:---|:---|:---|:---|
| **Zscaler** | ZIA/ZPA | 클라우드 선도, 규모 | 네트워크 기능 |
| **Palo Alto** | Prisma SASE | NGFW 통합 | 복잡성 |
| **Cisco** | SASE | 네트워크 장비 | 클라우드 |
| **Fortinet** | FortiSASE | 가성비 | 규모 |
| **Cloudflare** | Zero Trust | CDN 기반 | 엔터프라이즈 |
| **Netskope** | Next Gen SASE | CASB 강점 | 네트워크 |

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. SASE 구성요소 상관관계

```
사용자 요청
    │
    ▼
┌─────────────────────────────────────────────────┐
│                  SASE Policy Engine              │
│                                                  │
│   트래픽 분류 → 목적지별 라우팅                  │
└─────────────────────────────────────────────────┘
    │
    ├── 공개 웹사이트 ────────────────► SWG
    │                                  (URL 필터, AV, SSL 검사)
    │
    ├── SaaS 앱 (Office 365) ────────► CASB
    │                                  (API 연동, DLP, Shadow IT)
    │
    ├── IaaS (AWS/Azure) ─────────────► FWaaS + ZTNA
    │                                  (마이크로 세그멘테이션)
    │
    └── Private App (사내 ERP) ──────► ZTNA
                                       (앱별 터널, ID 기반)
```

#### 2. 과목 융합 관점

**신원 관리와 융합**
- IdP: Azure AD, Okta 연동
- MFA: 조건부 액세스
- UEBA: 행위 분석

**클라우드와 융합**
- Cloud Access Security: CASB
- Workload Protection: CWPP
- Container Security

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 글로벌 기업 SASE 전환**
- 상황: 50개국, 10,000 사용자, VPN 성능 한계
- 판단: Zscaler/ZPA 도입
- 단계:
  1. 파일럿: 500명 대상 ZTNA 테스트
  2. SWG: 웹 트래픽 먼저 전환
  3. ZTNA: VPN 대체
  4. CASB: SaaS 가시성 확보

**시나리오 2: 하이브리드 클라우드**
- 상황: 온프레미스 + AWS/Azure
- 판단: Palo Alto Prisma SASE
- 이유: 기존 NGFW와 통합 관리

#### 2. 안티패턴 (Anti-patterns)

```
취약한 구현 (금지!)

1. VPN 병행 사용
   ❌ ZTNA + VPN 동시 운영
   → 사용자 혼란, 보안 구멍

2. 과도한 Allow 정책
   ❌ Allow Any to Any (초기 설정 유지)
   → ZTNA 의미 없음

3. 디바이스 검증 생략
   ❌ User 인증만
   → 악성 디바이스로 접근 가능

올바른 구현:

1. 단계적 VPN 제거
   ✓ ZTNA 먼저 검증 → VPN 폐지

2. 최소 권한
   ✓ Allow Sales-Group to Sales-App ONLY

3. 지속적 검증
   ✓ User + Device + Context + Behavior
```

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 | 항목 | 수치/내용 |
|:---|:---|:---|
| **측면 이동** | 방지 | 100% (격리 터널) |
| **지연 시간** | 단축 | 30-50% (엣지) |
| **운영** | 복잡성 | 장비 5→1 |
| **공격 노출** | 감소 | 네트워크 → 앱 |

#### 2. 참고 표준/가이드

| 표준 | 내용 |
|:---|:---|
| **NIST SP 800-207** | Zero Trust Architecture |
| **Gartner SASE** | Market Guide |
| **Forrester TEI** | ZTNA ROI |

---

### 관련 개념 맵 (Knowledge Graph)
- [제로 트러스트](@/studynotes/09_security/01_policy/zero_trust.md) : SASE의 철학적 기반
- [NGFW](@/studynotes/09_security/03_network/ngfw.md) : FWaaS 구현
- [CASB](@/studynotes/09_security/06_cloud/casb.md) : SASE 구성요소
- [IAM](@/studynotes/09_security/07_identity/iam.md) : 신원 기반 접근
- [마이크로 세그멘테이션](@/studynotes/09_security/01_policy/micro_segmentation.md) : 네트워크 분할

---

### 어린이를 위한 3줄 비유 설명
1. **개별 티켓**: ZTNA는 놀이공원에서 모든 놀이기구를 자유롭게 쓰는 VIP 패스가 아니에요. 필요한 놀이기구만 이용할 수 있는 개별 티켓을 받아요.
2. **지속적 확인**: 입구에서 한 번만 검사하는 게 아니에요. 놀이기구를 탈 때마다 다시 확인받아요. 그래서 더 안전해요!
3. **클라우드 문지기**: SASE는 인터넷 곳곳에 있는 똑똑한 문지기예요. 어디서든 회사 앱에 접속할 때, 문지기가 안전한지 확인해 줘요.
