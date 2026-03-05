+++
title = "방화벽 (Firewall)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# 방화벽 (Firewall)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 방화벽은 신뢰할 수 있는 내부 네트워크와 신뢰할 수 없는 외부 네트워크 사이에서 트래픽을 필터링하는 네트워크 보안 장치로, 패킷 필터, Stateful Inspection, Proxy, NGFW로 진화했습니다.
> 2. **가치**: 네트워크 경계 보안의 핵심으로 무단 접근 차단, 침입 방지, 트래픽 제어 기능을 제공하며, 현대 NGFW는 DPI, 앱 인식, IPS를 통합합니다.
> 3. **융합**: DMZ 설계, 내부 세그멘테이션(ISFW), 클라우드 보안 그룹, SASE로 확장되며 Zero Trust 아키텍처와 함께 심층 방어를 구성합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**방화벽(Firewall)**은 미리 정의된 보안 규칙에 따라 네트워크 트래픽을 모니터링하고 제어하는 보안 시스템입니다.

**방화벽 유형**:
| 유형 | 동작 계층 | 필터링 기준 | 특징 |
|:---|:---|:---|:---|
| **패킷 필터** | L3/L4 | IP, 포트, 프로토콜 | 기본적, 상태 비저장 |
| **Stateful Inspection** | L3/L4 | 연결 상태 추적 | 세션 기반, 보안 강화 |
| **Proxy 방화벽** | L7 | 애플리케이션 데이터 | 심층 검사, 느림 |
| **NGFW** | L3-L7 | 앱, 사용자, 콘텐츠 | 통합 보안, DPI |
| **WAF** | L7 | 웹 공격 패턴 | 웹 전용 |

#### 2. 비유를 통한 이해
방화벽은 **'건물 출입구 보안 요원'**에 비유할 수 있습니다:

```
패킷 필터: 명함만 보고 출입 허용 (IP, 포트 확인)
Stateful: 출입증 발급 후 확인 (세션 추적)
Proxy: 모든 짐 검사 (페이로드 검사)
NGFW: 얼굴 인식 + 소속 확인 + 짐 검사 (통합 보안)
```

#### 3. 등장 배경 및 발전 과정
| 시기 | 기술 | 특징 |
|:---|:---|:---|
| **1988** | 패킷 필터 | DEC, Morris Worm 대응 |
| **1990년대** | Stateful Inspection | Check Point, 세션 추적 |
| **1990년대 후** | Application Proxy | TIS FWTK, 심층 검사 |
| **2000년대** | UTM | 통합 위협 관리 |
| **2010년대** | NGFW | Palo Alto, 앱 인식 |
| **2020년대** | SASE/Cloud FW | 클라우드 네이티브 |

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 방화벽 아키텍처 다이어그램

```text
                    [ 방화벽 네트워크 배치 ]

                          [인터넷]
                              │
                              ▼
                    ┌─────────────────┐
                    │    외부 라우터   │
                    │   (Edge Router) │
                    └────────┬────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │      외부 방화벽 (Primary)    │
              │  ┌─────────────────────────┐ │
              │  │   Stateful Inspection   │ │
              │  │   - ACL 규칙            │ │
              │  │   - 세션 테이블         │ │
              │  │   - NAT/PAT            │ │
              │  └─────────────────────────┘ │
              └──────────────┬───────────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
    ┌────────────┐    ┌────────────┐    ┌────────────┐
    │    DMZ     │    │  내부망    │    │  관리망    │
    │ (공개 서버)│    │ (사용자)   │    │ (관리자)   │
    ├────────────┤    ├────────────┤    ├────────────┤
    │ Web Server │    │ Workstation│    │ Admin PC   │
    │ Mail Server│    │ File Server│    │ Monitoring │
    │ DNS Server │    │ DB Server  │    │ Log Server │
    └────────────┘    └────────────┘    └────────────┘
           │                 │
           └────────┬────────┘
                    │
                    ▼
              ┌──────────────────────────────┐
              │    내부 방화벽 (ISFW)         │
              │  ┌─────────────────────────┐ │
              │  │  Micro-segmentation     │ │
              │  │  East-West 트래픽 제어   │ │
              │  └─────────────────────────┘ │
              └──────────────────────────────┘


                    [ NGFW 내부 구조 ]

┌─────────────────────────────────────────────────────────────────────┐
│                        Next-Generation Firewall                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    트래픽 수집 계층                            │  │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐         │  │
│  │   │ 패킷    │  │ 세션    │  │ 앱      │  │ 사용자  │         │  │
│  │   │ 디코딩  │  │ 추적    │  │ 식별    │  │ 매핑    │         │  │
│  │   └─────────┘  └─────────┘  └─────────┘  └─────────┘         │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                    │                                │
│                                    ▼                                │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    보안 검사 계층                              │  │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐         │  │
│  │   │ DPI     │  │ IPS/IDS │  │ 안티    │  │ SSL     │         │  │
│  │   │ (페이로드)│ │ (공격탐지)│ │ 멀웨어  │  │ 복호화  │         │  │
│  │   └─────────┘  └─────────┘  └─────────┘  └─────────┘         │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                    │                                │
│                                    ▼                                │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    정책 결정 계층                              │  │
│  │   ┌─────────────────────────────────────────────────────┐    │  │
│  │   │  Rule 1: Allow Web Browsing from Group "Employees"  │    │  │
│  │   │  Rule 2: Block Social Media Apps                    │    │  │
│  │   │  Rule 3: Allow SaaS Apps with SSL Inspection        │    │  │
│  │   └─────────────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                    │                                │
│                                    ▼                                │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    로깅 및 보고 계층                           │  │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐         │  │
│  │   │ Syslog  │  │ SIEM    │  │ 리포트  │  │ 위협    │         │  │
│  │   │ 전송    │  │ 연동    │  │ 생성    │  │ 인텔    │         │  │
│  │   └─────────┘  └─────────┘  └─────────┘  └─────────┘         │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### 2. Stateful Inspection 동작 원리

```text
                    [ Stateful Inspection 세션 테이블 ]

세션 테이블 항목:
┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Source   │ Dest     │ Src Port │ Dst Port │ Protocol │ State    │
│ IP       │ IP       │          │          │          │          │
├──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│10.1.1.10 │8.8.8.8   │ 45123    │ 443      │ TCP      │ ESTABLISH│
│10.1.1.20 │1.1.1.1   │ 45124    │ 53       │ UDP      │ ACTIVE   │
│10.1.1.30 │ 웹서버   │ 45125    │ 80       │ TCP      │ SYN_SENT │
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘

TCP 상태 머신:
CLOSED → SYN_SENT → SYN_RECEIVED → ESTABLISHED → FIN_WAIT → CLOSED

필터링 로직:
1. 새 연결(SYN): 규칙 확인 → 허용 시 세션 생성
2. 기존 연결: 세션 테이블 조회 → 테이블에 있으면 통과
3. 세션 종료: FIN/RST 또는 타임아웃 시 제거
```

#### 3. 핵심 알고리즘 & 실무 코드

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import ipaddress

class Action(Enum):
    ALLOW = "allow"
    DENY = "deny"
    DROP = "drop"
    REJECT = "reject"

class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    ANY = "any"

class ConnectionState(Enum):
    CLOSED = "closed"
    SYN_SENT = "syn_sent"
    SYN_RECEIVED = "syn_received"
    ESTABLISHED = "established"
    FIN_WAIT = "fin_wait"
    TIME_WAIT = "time_wait"

@dataclass
class FirewallRule:
    """방화벽 규칙"""
    rule_id: int
    name: str
    source: str           # CIDR 또는 "any"
    destination: str      # CIDR 또는 "any"
    port_range: Tuple[int, int]  # (시작, 끝)
    protocol: Protocol
    action: Action
    enabled: bool = True
    log: bool = True

@dataclass
class Session:
    """세션 정보"""
    source_ip: str
    dest_ip: str
    source_port: int
    dest_port: int
    protocol: Protocol
    state: ConnectionState
    created_at: datetime
    last_seen: datetime
    bytes_sent: int = 0
    bytes_recv: int = 0

class StatefulFirewall:
    """Stateful Inspection 방화벽 구현"""

    def __init__(self):
        self.rules: List[FirewallRule] = []
        self.sessions: Dict[Tuple, Session] = {}
        self.session_timeout = timedelta(minutes=30)
        self.tcp_timeout = timedelta(hours=24)

    def add_rule(self, rule: FirewallRule):
        """규칙 추가 (우선순위 순)"""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.rule_id)

    def _match_rule(self, packet: dict, rule: FirewallRule) -> bool:
        """패킷이 규칙에 매치되는지 확인"""
        # 소스 IP 확인
        if rule.source != "any":
            try:
                network = ipaddress.ip_network(rule.source, strict=False)
                if ipaddress.ip_address(packet['source_ip']) not in network:
                    return False
            except:
                return False

        # 목적지 IP 확인
        if rule.destination != "any":
            try:
                network = ipaddress.ip_network(rule.destination, strict=False)
                if ipaddress.ip_address(packet['dest_ip']) not in network:
                    return False
            except:
                return False

        # 포트 확인
        if rule.port_range != (0, 65535):
            if not (rule.port_range[0] <= packet['dest_port'] <= rule.port_range[1]):
                return False

        # 프로토콜 확인
        if rule.protocol != Protocol.ANY:
            if packet['protocol'] != rule.protocol:
                return False

        return True

    def _get_session_key(self, packet: dict) -> Tuple:
        """세션 식별 키 생성"""
        return (
            packet['source_ip'], packet['dest_ip'],
            packet['source_port'], packet['dest_port'],
            packet['protocol']
        )

    def _get_reverse_key(self, packet: dict) -> Tuple:
        """역방향 세션 키"""
        return (
            packet['dest_ip'], packet['source_ip'],
            packet['dest_port'], packet['source_port'],
            packet['protocol']
        )

    def process_packet(self, packet: dict) -> Tuple[Action, str]:
        """
        패킷 처리

        Args:
            packet: {
                'source_ip': str,
                'dest_ip': str,
                'source_port': int,
                'dest_port': int,
                'protocol': Protocol,
                'flags': str (TCP: SYN, ACK, FIN, RST)
            }

        Returns:
            (Action, reason)
        """
        session_key = self._get_session_key(packet)
        reverse_key = self._get_reverse_key(packet)

        # 1. 기존 세션 확인
        if session_key in self.sessions:
            session = self.sessions[session_key]
            session.last_seen = datetime.utcnow()
            session.bytes_recv += packet.get('size', 0)

            # TCP 상태 업데이트
            if packet['protocol'] == Protocol.TCP:
                flags = packet.get('flags', '')
                if 'FIN' in flags:
                    session.state = ConnectionState.FIN_WAIT
                elif 'RST' in flags:
                    session.state = ConnectionState.CLOSED

            return (Action.ALLOW, "Existing session")

        # 역방향 세션 확인 (응답 패킷)
        if reverse_key in self.sessions:
            session = self.sessions[reverse_key]
            session.last_seen = datetime.utcnow()
            session.bytes_sent += packet.get('size', 0)
            return (Action.ALLOW, "Return traffic for existing session")

        # 2. 새 연결 - 규칙 평가
        for rule in self.rules:
            if not rule.enabled:
                continue

            if self._match_rule(packet, rule):
                # 세션 생성 (허용된 경우)
                if rule.action == Action.ALLOW:
                    session = Session(
                        source_ip=packet['source_ip'],
                        dest_ip=packet['dest_ip'],
                        source_port=packet['source_port'],
                        dest_port=packet['dest_port'],
                        protocol=packet['protocol'],
                        state=ConnectionState.SYN_SENT if packet['protocol'] == Protocol.TCP else ConnectionState.ESTABLISHED,
                        created_at=datetime.utcnow(),
                        last_seen=datetime.utcnow()
                    )
                    self.sessions[session_key] = session

                return (rule.action, f"Rule {rule.rule_id}: {rule.name}")

        # 3. 기본 정책: 거부
        return (Action.DENY, "Default deny")

    def cleanup_sessions(self):
        """만료된 세션 정리"""
        now = datetime.utcnow()
        expired = []

        for key, session in self.sessions.items():
            if session.protocol == Protocol.TCP:
                timeout = self.tcp_timeout
            else:
                timeout = self.session_timeout

            if now - session.last_seen > timeout:
                expired.append(key)

        for key in expired:
            del self.sessions[key]

        return len(expired)

    def get_statistics(self) -> dict:
        """방화벽 통계"""
        return {
            "total_rules": len(self.rules),
            "active_rules": sum(1 for r in self.rules if r.enabled),
            "active_sessions": len(self.sessions),
            "sessions_by_protocol": {
                p.value: sum(1 for s in self.sessions.values() if s.protocol == p)
                for p in Protocol
            }
        }


class NGFW(StatefulFirewall):
    """Next-Generation Firewall (확장)"""

    def __init__(self):
        super().__init__()
        self.app_signatures: Dict[str, dict] = {}
        self.user_mapping: Dict[str, str] = {}  # IP -> User

    def identify_application(self, packet: dict) -> str:
        """애플리케이션 식별 (DPI)"""
        # 실제로는 패턴 매칭, 행위 분석 등 사용
        port = packet['dest_port']

        app_map = {
            80: "http",
            443: "ssl",  # 실제로는 SNI, 인증서 등으로 식별
            53: "dns",
            22: "ssh",
            21: "ftp",
            3389: "rdp"
        }

        # 포트 기반 식별 (단순화)
        return app_map.get(port, "unknown")

    def map_user(self, ip: str) -> Optional[str]:
        """IP를 사용자로 매핑"""
        return self.user_mapping.get(ip)

    def process_packet_ng(self, packet: dict) -> Tuple[Action, dict]:
        """NGFW 패킷 처리"""
        # 기본 방화벽 처리
        action, reason = self.process_packet(packet)

        # 앱 식별
        app = self.identify_application(packet)

        # 사용자 매핑
        user = self.map_user(packet['source_ip'])

        result = {
            "action": action,
            "reason": reason,
            "application": app,
            "user": user,
            "session_id": str(self._get_session_key(packet))
        }

        return action, result


# 사용 예시
if __name__ == "__main__":
    fw = StatefulFirewall()

    # 규칙 추가
    fw.add_rule(FirewallRule(
        rule_id=1,
        name="Allow Web Browsing",
        source="10.1.1.0/24",
        destination="any",
        port_range=(80, 443),
        protocol=Protocol.TCP,
        action=Action.ALLOW
    ))

    fw.add_rule(FirewallRule(
        rule_id=2,
        name="Allow DNS",
        source="any",
        destination="any",
        port_range=(53, 53),
        protocol=Protocol.UDP,
        action=Action.ALLOW
    ))

    fw.add_rule(FirewallRule(
        rule_id=3,
        name="Block SSH from External",
        source="any",
        destination="10.1.1.0/24",
        port_range=(22, 22),
        protocol=Protocol.TCP,
        action=Action.DENY
    ))

    # 패킷 처리 테스트
    packets = [
        {"source_ip": "10.1.1.10", "dest_ip": "8.8.8.8", "source_port": 45123, "dest_port": 443, "protocol": Protocol.TCP, "flags": "SYN"},
        {"source_ip": "10.1.1.10", "dest_ip": "8.8.8.8", "source_port": 45124, "dest_port": 53, "protocol": Protocol.UDP},
        {"source_ip": "1.2.3.4", "dest_ip": "10.1.1.10", "source_port": 54321, "dest_port": 22, "protocol": Protocol.TCP, "flags": "SYN"},
    ]

    print("=== 방화벽 패킷 처리 결과 ===")
    for i, pkt in enumerate(packets, 1):
        action, reason = fw.process_packet(pkt)
        print(f"패킷 {i}: {action.value} - {reason}")

    print(f"\n=== 방화벽 통계 ===")
    stats = fw.get_statistics()
    print(f"활성 세션: {stats['active_sessions']}")
