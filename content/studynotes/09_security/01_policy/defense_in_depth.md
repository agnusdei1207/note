+++
title = "심층 방어 (Defense in Depth)"
date = "2026-03-04"
[extra]
categories = "studynotes-09_security"
+++

# 심층 방어 (Defense in Depth)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 단일 보안 통제에 의존하지 않고 다층(Layered) 보안 통제를 적용하여, 하나가 실패해도 다른 계층이 보호하는 견고한 보안 아키텍처 전략입니다.
> 2. **가치**: 단일 장애점(SPOF) 제거, 공격자의 진출 지연, 다양한 공격 벡터 대응, 보안 사고 시 피해 최소화를 실현합니다.
> 3. **융합**: 네트워크, 엔드포인트, 애플리케이션, 데이터, 사용자 계층에 걸친 통합 방어 체계입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**심층 방어(Defense in Depth, DiD)**는 정보보안 시스템에서 여러 계층의 보안 통제를 중첩하여 배치하는 전략입니다. 미 국방부(DoD)에서 개념화되었으며, 군사적 방어 전략에서 유래했습니다.

**핵심 원리**:
- **다층성 (Layering)**: 여러 독립적 보안 계층
- **다양성 (Diversity)**: 서로 다른 유형의 통제
- **중복성 (Redundancy)**: 백업 및 대체 수단
- **상호 보완성 (Complementarity)**: 계층 간 협력

**NSA 정의**:
> "정보 시스템과 데이터를 보호하기 위해 여러 보안 통제를 배치하는 전략적 접근법"

#### 2. 💡 비유를 통한 이해
심층 방어는 **'성곽 도시'**에 비유할 수 있습니다.
- **외성**: 도시 외곽 벽 - 경계 방화벽
- **내성**: 내부 요새 - 내부 세그멘테이션
- **해자**: 물리적 장벽 - DDoS 방어
- **문지기**: 출입 통제 - IAM
- **순찰병**: 감시 - SIEM
- **개인 갑옷**: 개별 보호 - EDR

#### 3. 등장 배경 및 발전 과정
1. **군사 전략**: 고대 성곽, 중세 요새의 다층 방어
2. **정보보안 초기**: 방화벽 단일 계층 (1990년대)
3. **다계층 보안**: IDS, 안티바이러스 추가 (2000년대)
4. **종합 보안**: NGFW, SIEM, EDR 통합 (2010년대)
5. **Zero Trust**: "경계 없는" 심층 방어 (2020년대~)

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 심층 방어 계층 구조 (표)

| 계층 | 통제 유형 | 기술 예시 | 목표 |
|:---|:---|:---|:---|
| **물리적** | 예방/감시 | CCTV, 출입통제, 잠금장치 | 물리적 접근 차단 |
| **네트워크** | 예방/탐지 | 방화벽, IDS/IPS, WAF | 네트워크 공격 차단 |
| **엔드포인트** | 탐지/대응 | EDR, 안티바이러스, DLP | 기기 보호 |
| **애플리케이션** | 예방/교정 | WAF, 코드검사, 보안헤더 | 앱 취약점 방어 |
| **데이터** | 예방/복구 | 암호화, 백업, 마스킹 | 데이터 보호 |
| **사용자** | 예방/탐지 | IAM, MFA, 보안교육 | 내부자 위협 방어 |
| **관리** | 탐지/대응 | SIEM, SOAR, 감사 | 전체 가시성 |

#### 2. 심층 방어 아키텍처 다이어그램

```text
<<< Defense in Depth - Multi-Layer Security Architecture >>>

                         [ 인터넷 / 외부 ]
                                │
                                v
    ╔════════════════════════════════════════════════════════════╗
    ║  Layer 1: 외부 경계 (External Perimeter)                   ║
    ║  ┌────────────────────────────────────────────────────┐   ║
    ║  │  DDoS 방어 (Cloudflare, AWS Shield)               │   ║
    ║  │  DNS 보안 (DNSSEC)                                │   ║
    ║  │  WAF (Web Application Firewall)                   │   ║
    ║  └────────────────────────────────────────────────────┘   ║
    ╚════════════════════════════════════════════════════════════╝
                                │
                                v
    ╔════════════════════════════════════════════════════════════╗
    ║  Layer 2: 네트워크 경계 (Network Perimeter)                ║
    ║  ┌────────────────────────────────────────────────────┐   ║
    ║  │  차세대 방화벽 (NGFW)                              │   ║
    ║  │  IDS/IPS (침입 탐지/방지)                          │   ║
    ║  │  VPN 게이트웨이                                    │   ║
    ║  │  네트워크 세그멘테이션                             │   ║
    ║  └────────────────────────────────────────────────────┘   ║
    ╚════════════════════════════════════════════════════════════╝
                                │
                                v
    ╔════════════════════════════════════════════════════════════╗
    ║  Layer 3: 내부 네트워크 (Internal Network)                 ║
    ║  ┌────────────────────────────────────────────────────┐   ║
    ║  │  내부 방화벽 (ISFW)                               │   ║
    ║  │  마이크로 세그멘테이션                            │   ║
    ║  │  NAC (네트워크 접근 제어)                          │   ║
    ║  │  네트워크 트래픽 분석 (NTA)                        │   ║
    ║  └────────────────────────────────────────────────────┘   ║
    ╚════════════════════════════════════════════════════════════╝
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
            v                   v                   v
    ╔═══════════════╗   ╔═══════════════╗   ╔═══════════════╗
    ║ Layer 4: 호스트║   ║ Layer 4: 호스트║   ║ Layer 4: 호스트║
    ║ ┌───────────┐ ║   ║ ┌───────────┐ ║   ║ ┌───────────┐ ║
    ║ │ EDR       │ ║   ║ │ EDR       │ ║   ║ │ EDR       │ ║
    ║ │ Host IDS  │ ║   ║ │ Host IDS  │ ║   ║ │ Host IDS  │ ║
    ║ │ Disk Enc  │ ║   ║ │ Disk Enc  │ ║   ║ │ Disk Enc  │ ║
    ║ │ Patch Mgmt│ ║   ║ │ Patch Mgmt│ ║   ║ │ Patch Mgmt│ ║
    ║ └───────────┘ ║   ║ └───────────┘ ║   ║ └───────────┘ ║
    ╚═══════════════╝   ╚═══════════════╝   ╚═══════════════╝
            │                   │                   │
            v                   v                   v
    ╔════════════════════════════════════════════════════════════╗
    ║  Layer 5: 애플리케이션 (Application)                       ║
    ║  ┌────────────────────────────────────────────────────┐   ║
    ║  │  입력 검증 / 출력 인코딩                           │   ║
    ║  │  세션 관리 / 인증/인가                             │   ║
    ║  │  보안 코딩 / 코드 리뷰                             │   ║
    ║  │  런타임 보호 (RASP)                                │   ║
    ║  └────────────────────────────────────────────────────┘   ║
    ╚════════════════════════════════════════════════════════════╝
                                │
                                v
    ╔════════════════════════════════════════════════════════════╗
    ║  Layer 6: 데이터 (Data)                                    ║
    ║  ┌────────────────────────────────────────────────────┐   ║
    ║  │  저장 암호화 (AES-256)                             │   ║
    ║  │  전송 암호화 (TLS 1.3)                             │   ║
    ║  │  데이터 마스킹 / 토큰화                            │   ║
    ║  │  백업 / 복구                                      │   ║
    ║  └────────────────────────────────────────────────────┘   ║
    ╚════════════════════════════════════════════════════════════╝

    ╔════════════════════════════════════════════════════════════╗
    ║  Layer 7: 사용자 & 관리 (User & Management)                ║
    ║  ┌────────────────────────────────────────────────────┐   ║
    ║  │  IAM / MFA / PAM                                  │   ║
    ║  │  보안 교육 / 인식 프로그램                         │   ║
    ║  │  SIEM / SOAR (통합 모니터링)                       │   ║
    ║  │  포렌식 / 인시던트 대응                            │   ║
    ║  └────────────────────────────────────────────────────┘   ║
    ╚════════════════════════════════════════════════════════════╝

<<< 공격 시나리오별 심층 방어 작동 예시 >>>

    시나리오 1: 웹 공격 (SQL Injection)
    ┌─────────────────────────────────────────────────────────┐
    │ Layer 1 (WAF): 공격 패턴 탐지 → 차단 시도              │
    │ Layer 2 (IPS): SQL 구문 탐지 → 차단                    │
    │ Layer 5 (App): 파라미터화 쿼리 → 공격 무력화           │
    │ Layer 6 (DB): 최소 권한 → 데이터 접근 제한             │
    │                                                         │
    │ → 어떤 계층이 뚫려도 다른 계층이 방어                  │
    └─────────────────────────────────────────────────────────┘

    시나리오 2: 랜섬웨어 감염
    ┌─────────────────────────────────────────────────────────┐
    │ Layer 2 (IPS): C2 통신 차단                             │
    │ Layer 3 (NTA): 이상 트래픽 탐지                         │
    │ Layer 4 (EDR): 악성 행위 탐지/차단                      │
    │ Layer 6 (Backup): 암호화 데이터 복구                    │
    │                                                         │
    │ → 단일 계층 실패해도 백업으로 복구 가능                 │
    └─────────────────────────────────────────────────────────┘
```

#### 3. 심층 동작 원리: 다계층 보안 통제 구현

```python
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Optional, Tuple, Any
from enum import Enum
from datetime import datetime
import hashlib
import re

class SecurityLayer(Enum):
    PHYSICAL = "physical"
    NETWORK_PERIMETER = "network_perimeter"
    NETWORK_INTERNAL = "network_internal"
    ENDPOINT = "endpoint"
    APPLICATION = "application"
    DATA = "data"
    USER = "user"
    MANAGEMENT = "management"

class ControlType(Enum):
    PREVENTIVE = "preventive"      # 예방
    DETECTIVE = "detective"        # 탐지
    CORRECTIVE = "corrective"      # 교정
    RECOVERY = "recovery"          # 복구
    DETERRENT = "deterrent"        # 억제

@dataclass
class SecurityControl:
    """보안 통제"""
    id: str
    name: str
    layer: SecurityLayer
    control_type: ControlType
    description: str
    check_function: Callable
    enabled: bool = True

    def check(self, context: Dict) -> Tuple[bool, str]:
        """통제 검사 실행"""
        if not self.enabled:
            return True, "Control disabled"
        return self.check_function(context)

@dataclass
class SecurityEvent:
    """보안 이벤트"""
    timestamp: str
    layer: SecurityLayer
    control_id: str
    result: str  # BLOCK, ALLOW, ALERT
    details: str
    context: Dict

class DefenseInDepthSystem:
    """
    심층 방어 시스템
    - 다계층 보안 통제 관리
    - 계층별 독립적 검사
    - 통합 로깅 및 대응
    """

    def __init__(self):
        self.layers: Dict[SecurityLayer, List[SecurityControl]] = {
            layer: [] for layer in SecurityLayer
        }
        self.events: List[SecurityEvent] = []
        self.blocked_count = 0
        self.allowed_count = 0

    def register_control(self, control: SecurityControl):
        """보안 통제 등록"""
        self.layers[control.layer].append(control)

    def evaluate_request(self, context: Dict) -> Tuple[bool, List[Dict]]:
        """
        모든 계층에 대한 요청 평가
        모든 계층을 통과해야 허용
        """
        results = []
        overall_allowed = True

        # 계층 순서대로 평가
        layer_order = [
            SecurityLayer.PHYSICAL,
            SecurityLayer.NETWORK_PERIMETER,
            SecurityLayer.NETWORK_INTERNAL,
            SecurityLayer.ENDPOINT,
            SecurityLayer.APPLICATION,
            SecurityLayer.DATA,
            SecurityLayer.USER
        ]

        for layer in layer_order:
            layer_result = self._evaluate_layer(layer, context)
            results.extend(layer_result['details'])

            if not layer_result['passed']:
                overall_allowed = False
                # 실패 시 상위 계층 평가 중단 (선택적)
                # break  # 실제 환경에서는 정책에 따라 결정

        if overall_allowed:
            self.allowed_count += 1
        else:
            self.blocked_count += 1

        return overall_allowed, results

    def _evaluate_layer(self, layer: SecurityLayer, context: Dict) -> Dict:
        """단일 계층 평가"""
        controls = self.layers[layer]
        details = []
        passed = True

        for control in controls:
            is_allowed, message = control.check(context)

            event = SecurityEvent(
                timestamp=datetime.utcnow().isoformat(),
                layer=layer,
                control_id=control.id,
                result="ALLOW" if is_allowed else "BLOCK",
                details=message,
                context=context
            )
            self.events.append(event)

            details.append({
                'layer': layer.value,
                'control': control.name,
                'type': control.control_type.value,
                'result': 'PASS' if is_allowed else 'FAIL',
                'message': message
            })

            if not is_allowed:
                passed = False

        return {
            'layer': layer,
            'passed': passed,
            'details': details
        }

    def get_layer_statistics(self) -> Dict:
        """계층별 통계"""
        stats = {}
        for layer in SecurityLayer:
            controls = self.layers[layer]
            layer_events = [e for e in self.events if e.layer == layer]

            stats[layer.value] = {
                'controls_count': len(controls),
                'enabled_count': len([c for c in controls if c.enabled]),
                'total_checks': len(layer_events),
                'blocked': len([e for e in layer_events if e.result == 'BLOCK']),
                'allowed': len([e for e in layer_events if e.result == 'ALLOW'])
            }

        return stats

class SecurityControlFactory:
    """
    보안 통제 팩토리
    - 사전 정의된 통제 생성
    """

    @staticmethod
    def create_ddos_protection() -> SecurityControl:
        """DDoS 방어 통제"""
        def check_ddos(context: Dict) -> Tuple[bool, str]:
            request_rate = context.get('request_rate', 0)
            source_ip = context.get('source_ip', '')

            # 요청 속도 제한
            if request_rate > 10000:
                return False, f"Rate limit exceeded: {request_rate} req/s"

            # 알려진 봇넷 IP 차단
            blocked_ips = context.get('blocked_ips', set())
            if source_ip in blocked_ips:
                return False, f"Blocked IP: {source_ip}"

            return True, "DDoS check passed"

        return SecurityControl(
            id="NET-001",
            name="DDoS Protection",
            layer=SecurityLayer.NETWORK_PERIMETER,
            control_type=ControlType.PREVENTIVE,
            description="요청 속도 제한 및 봇넷 차단",
            check_function=check_ddos
        )

    @staticmethod
    def create_firewall() -> SecurityControl:
        """방화벽 통제"""
        def check_firewall(context: Dict) -> Tuple[bool, str]:
            source_ip = context.get('source_ip', '')
            dest_port = context.get('dest_port', 0)
            protocol = context.get('protocol', 'TCP')

            # 기본 거부 정책
            allowed_ports = {80, 443, 22, 3389}
            if dest_port not in allowed_ports:
                return False, f"Port {dest_port} not allowed"

            # IP 화이트리스트 (내부 포트)
            internal_ports = {22, 3389}
            if dest_port in internal_ports:
                allowed_ips = context.get('allowed_internal_ips', set())
                if source_ip not in allowed_ips:
                    return False, f"Access denied to internal port {dest_port}"

            return True, f"Firewall rule passed: {protocol}:{dest_port}"

        return SecurityControl(
            id="NET-002",
            name="Next-Gen Firewall",
            layer=SecurityLayer.NETWORK_PERIMETER,
            control_type=ControlType.PREVENTIVE,
            description="포트 및 IP 기반 접근 제어",
            check_function=check_firewall
        )

    @staticmethod
    def create_waf() -> SecurityControl:
        """WAF 통제"""
        def check_waf(context: Dict) -> Tuple[bool, str]:
            request_body = context.get('request_body', '')
            query_string = context.get('query_string', '')
            headers = context.get('headers', {})

            # SQL Injection 패턴
            sql_patterns = [
                r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP)\b.*\b(FROM|INTO|TABLE)\b)",
                r"(--|\#|\/\*)",
                r"(\bUNION\b.*\bSELECT\b)",
                r"(\bOR\b.*=.*)",
            ]

            combined_input = request_body + query_string
            for pattern in sql_patterns:
                if re.search(pattern, combined_input, re.IGNORECASE):
                    return False, f"SQL Injection pattern detected"

            # XSS 패턴
            xss_patterns = [
                r"<script[^>]*>.*</script>",
                r"javascript:",
                r"on\w+\s*=",
                r"<iframe",
            ]

            for pattern in xss_patterns:
                if re.search(pattern, combined_input, re.IGNORECASE):
                    return False, f"XSS pattern detected"

            # 악의적 헤더
            malicious_headers = ['X-Forwarded-For', 'X-Original-URL']
            for header in malicious_headers:
                if header in headers:
                    value = headers[header]
                    if re.search(r"[;<>\(\)]", str(value)):
                        return False, f"Malicious header detected: {header}"

            return True, "WAF check passed"

        return SecurityControl(
            id="APP-001",
            name="Web Application Firewall",
            layer=SecurityLayer.APPLICATION,
            control_type=ControlType.PREVENTIVE,
            description="웹 공격 패턴 탐지 및 차단",
            check_function=check_waf
        )

    @staticmethod
    def create_endpoint_protection() -> SecurityControl:
        """엔드포인트 보호 통제"""
        def check_endpoint(context: Dict) -> Tuple[bool, str]:
            device_id = context.get('device_id', '')
            device_status = context.get('device_status', {})

            # 디바이스 등록 확인
            if not device_status.get('registered', False):
                return False, "Device not registered"

            # OS 패치 상태
            os_version = device_status.get('os_version', '')
            min_os_version = context.get('min_os_version', '10.0')
            if os_version < min_os_version:
                return False, f"OS version {os_version} below minimum {min_os_version}"

            # 안티바이러스 상태
            av_status = device_status.get('antivirus', {})
            if not av_status.get('running', False):
                return False, "Antivirus not running"

            if av_status.get('definitions_age_days', 999) > 7:
                return False, "Antivirus definitions outdated"

            # 디스크 암호화
            if not device_status.get('disk_encrypted', False):
                return False, "Disk encryption not enabled"

            return True, "Endpoint check passed"

        return SecurityControl(
            id="EP-001",
            name="Endpoint Protection",
            layer=SecurityLayer.ENDPOINT,
            control_type=ControlType.PREVENTIVE,
            description="디바이스 보안 상태 확인",
            check_function=check_endpoint
        )

    @staticmethod
    def create_iam_control() -> SecurityControl:
        """IAM 통제"""
        def check_iam(context: Dict) -> Tuple[bool, str]:
            user_id = context.get('user_id', '')
            session = context.get('session', {})
            resource = context.get('resource', '')
            action = context.get('action', 'read')

            # 세션 유효성
            if not session.get('active', False):
                return False, "Session inactive"

            # 세션 만료 확인
            session_expiry = session.get('expiry', 0)
            if datetime.utcnow().timestamp() > session_expiry:
                return False, "Session expired"

            # MFA 확인 (민감 리소스)
            sensitive_resources = ['admin', 'financial', 'pii']
            if any(s in resource for s in sensitive_resources):
                if not session.get('mfa_verified', False):
                    return False, "MFA required for sensitive resource"

            # 권한 확인
            permissions = session.get('permissions', [])
            required_permission = f"{resource}:{action}"
            if required_permission not in permissions:
                return False, f"Permission denied: {required_permission}"

            return True, "IAM check passed"

        return SecurityControl(
            id="USER-001",
            name="Identity & Access Management",
            layer=SecurityLayer.USER,
            control_type=ControlType.PREVENTIVE,
            description="사용자 인증 및 권한 확인",
            check_function=check_iam
        )

    @staticmethod
    def create_data_encryption() -> SecurityControl:
        """데이터 암호화 통제"""
        def check_encryption(context: Dict) -> Tuple[bool, str]:
            data_classification = context.get('data_classification', 'public')
            encryption_status = context.get('encryption', {})

            # 민감 데이터는 암호화 필수
            if data_classification in ['confidential', 'secret', 'top_secret']:
                # 전송 중 암호화
                if not encryption_status.get('in_transit', False):
                    return False, "In-transit encryption required"

                # 저장 암호화
                if not encryption_status.get('at_rest', False):
                    return False, "At-rest encryption required"

                # 암호화 알고리즘 확인
                algorithm = encryption_status.get('algorithm', '')
                if algorithm not in ['AES-256', 'AES-256-GCM', 'ChaCha20-Poly1305']:
                    return False, f"Weak encryption algorithm: {algorithm}"

            return True, "Data encryption check passed"

        return SecurityControl(
            id="DATA-001",
            name="Data Encryption",
            layer=SecurityLayer.DATA,
            control_type=ControlType.PREVENTIVE,
            description="데이터 암호화 상태 확인",
            check_function=check_encryption
        )

    @staticmethod
    def create_intrusion_detection() -> SecurityControl:
        """침입 탐지 통제"""
        def check_ids(context: Dict) -> Tuple[bool, str]:
            network_traffic = context.get('network_traffic', {})
            signatures_matched = network_traffic.get('signatures_matched', [])
            anomaly_score = network_traffic.get('anomaly_score', 0)

            # 알려진 공격 시그니처
            critical_signatures = [
                'CVE-2021-44228',  # Log4Shell
                'CVE-2021-34527',  # PrintNightmare
            ]

            for sig in signatures_matched:
                if sig in critical_signatures:
                    return False, f"Critical signature matched: {sig}"

            # 이상 징후 점수
            if anomaly_score > 0.8:
                return False, f"High anomaly score: {anomaly_score}"

            return True, "IDS check passed"

        return SecurityControl(
            id="NET-003",
            name="Intrusion Detection System",
            layer=SecurityLayer.NETWORK_INTERNAL,
            control_type=ControlType.DETECTIVE,
            description="네트워크 침입 탐지",
            check_function=check_ids
        )

# 사용 예시
if __name__ == "__main__":
    # 심층 방어 시스템 구축
    did_system = DefenseInDepthSystem()

    # 보안 통제 등록
    factory = SecurityControlFactory()

    did_system.register_control(factory.create_ddos_protection())
    did_system.register_control(factory.create_firewall())
    did_system.register_control(factory.create_waf())
    did_system.register_control(factory.create_endpoint_protection())
    did_system.register_control(factory.create_iam_control())
    did_system.register_control(factory.create_data_encryption())
    did_system.register_control(factory.create_intrusion_detection())

    # 테스트 시나리오 1: 정상 요청
    print("=== Scenario 1: Normal Request ===")
    context1 = {
        'source_ip': '192.168.1.100',
        'dest_port': 443,
        'protocol': 'TCP',
        'request_rate': 50,
        'request_body': 'username=test&password=pass123',
        'query_string': 'page=1',
        'headers': {'User-Agent': 'Mozilla/5.0'},
        'device_id': 'device-001',
        'device_status': {
            'registered': True,
            'os_version': '10.0.19044',
            'antivirus': {'running': True, 'definitions_age_days': 2},
            'disk_encrypted': True
        },
        'user_id': 'user001',
        'session': {
            'active': True,
            'expiry': datetime.utcnow().timestamp() + 3600,
            'mfa_verified': True,
            'permissions': ['app:read', 'app:write']
        },
        'resource': 'app',
        'action': 'read',
        'data_classification': 'internal',
        'encryption': {'in_transit': True, 'at_rest': True, 'algorithm': 'AES-256'}
    }

    allowed, results = did_system.evaluate_request(context1)
    print(f"Result: {'ALLOWED' if allowed else 'BLOCKED'}")
    for r in results:
        if r['result'] == 'FAIL':
            print(f"  [{r['layer']}] {r['control']}: {r['message']}")

    # 테스트 시나리오 2: SQL Injection 공격
    print("\n=== Scenario 2: SQL Injection Attack ===")
    context2 = context1.copy()
    context2['query_string'] = "id=1' OR '1'='1"

    allowed, results = did_system.evaluate_request(context2)
    print(f"Result: {'ALLOWED' if allowed else 'BLOCKED'}")
    for r in results:
        if r['result'] == 'FAIL':
            print(f"  [{r['layer']}] {r['control']}: {r['message']}")

    # 테스트 시나리오 3: 미승인 디바이스
    print("\n=== Scenario 3: Unauthorized Device ===")
    context3 = context1.copy()
    context3['device_status'] = {
        'registered': False,
        'os_version': '10.0.19044',
        'antivirus': {'running': True, 'definitions_age_days': 2},
        'disk_encrypted': True
    }

    allowed, results = did_system.evaluate_request(context3)
    print(f"Result: {'ALLOWED' if allowed else 'BLOCKED'}")
    for r in results:
        if r['result'] == 'FAIL':
            print(f"  [{r['layer']}] {r['control']}: {r['message']}")

    # 통계
    print("\n=== Layer Statistics ===")
    stats = did_system.get_layer_statistics()
    for layer, data in stats.items():
        if data['controls_count'] > 0:
            print(f"{layer}: {data['controls_count']} controls, {data['blocked']} blocked")

    print(f"\nTotal: {did_system.blocked_count} blocked, {did_system.allowed_count} allowed")
