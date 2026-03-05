+++
title = "IDS / IPS (침입 탐지/방지 시스템)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# IDS / IPS (Intrusion Detection/Prevention System)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: IDS는 네트워크/시스템 침입을 탐지하고 알림을 발송하는 수동적 시스템이고, IPS는 탐지 후 자동으로 공격을 차단하는 능동적 인라인 시스템입니다.
> 2. **가치**: 서명 기반(알려진 공격)과 이상 탐지(행위 기반) 방식으로 APT, 제로데이, 내부자 위협을 식별하며, NGFW, EDR과 통합되어 심층 방어를 구성합니다.
> 3. **융합**: Snort, Suricata, Zeek(Bro)가 대표적 오픈소스이며, SIEM과 연동하여 보안 운영(SOC)의 핵심 센서 역할을 합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**IDS (Intrusion Detection System)**
- **정의**: 네트워크 또는 시스템에서 악의적 활동이나 정책 위반을 탐지하여 알림
- **위치**: 미러링 포트(SPAN), TAP (수동적 관찰)
- **동작**: 탐지 → 알림 → 수동 대응

**IPS (Intrusion Prevention System)**
- **정의**: IDS 기능에 자동 차단 기능을 추가한 인라인 보안 장비
- **위치**: 네트워크 경로상 (인라인)
- **동작**: 탐지 → 차단 → 알림

**탐지 방식**:
| 방식 | 원리 | 장점 | 단점 |
|:---|:---|:---|:---|
| **서명 기반 (Signature-based)** | 알려진 공격 패턴 매칭 | 정확도 높음, FP 낮음 | 제로데이 탐지 불가 |
| **이상 탐지 (Anomaly-based)** | 정상 행위 학습, 이상 식별 | 제로데이 탐지 가능 | FP 높음, 학습 필요 |
| **행위 기반 (Behavior-based)** | 의심스러운 행위 패턴 | APT 탐지 | 복잡함 |

#### 2. 비유를 통한 이해
IDS/IPS는 **'CCTV 감시 시스템'**에 비유할 수 있습니다:

```
IDS (CCTV):
[카메라] → [녹화] → [이상 발견 시 알림] → [경비원 출동]
특징: 공격을 막지는 못함, 기록과 알림만

IPS (자동문 + CCTV):
[카메라] → [이상 발견] → [자동문 잠금] → [알림]
특징: 공격을 자동으로 차단
```

#### 3. 등장 배경 및 발전 과정
| 시기 | 기술 | 특징 |
|:---|:---|:---|
| **1980년대** | 감사 로그 분석 | 수동적, 사후 분석 |
| **1990년대** | 네트워크 IDS | NetRanger, RealSecure |
| **1998** | Snort | 오픈소스 IDS 표준 |
| **2000년대** | IPS 등장 | 인라인 차단 |
| **2010년대** | NGIPS | 컨텍스트 인식, 앱 식별 |
| **2020년대** | AI 기반 탐지 | 머신러닝, UEBA 통합 |

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. IDS/IPS 배치 아키텍처

```text
                    [ 네트워크 IDS/IPS 배치 ]

                          [인터넷]
                              │
                              ▼
                    ┌─────────────────┐
                    │    외부 라우터   │
                    └────────┬────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │      NIPS (Network IPS)      │◄── 인라인 배치
              │  ┌─────────────────────────┐ │
              │  │  - 서명 기반 탐지        │ │
              │  │  - 프로토콜 이상 탐지    │ │
              │  │  - 자동 차단            │ │
              │  └─────────────────────────┘ │
              └──────────────┬───────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
         ┌────────┐    ┌────────┐    ┌────────┐
         │  DMZ   │    │ 내부망 │    │ 내부망 │
         └────┬───┘    └────┬───┘    └────┬───┘
              │              │              │
              │              │              │
              ▼              ▼              ▼
         ┌────────────────────────────────────────┐
         │   NIDS (Network IDS) - SPAN Port       │◄── 수동 미러링
         │   ┌──────────────────────────────────┐ │
         │   │  - 전체 트래픽 모니터링           │ │
         │   │  - 포렌식 데이터 수집            │ │
         │   │  - 탐지 알림                     │ │
         │   └──────────────────────────────────┘ │
         └────────────────────────────────────────┘


                    [ Snort/Suricata 규칙 구조 ]

┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  [Action] [Protocol] [Source IP] [Source Port] ->                  │
│           [Dest IP] [Dest Port] [Options]                          │
│                                                                     │
│  예시:                                                              │
│  alert tcp any any -> any 22 (msg:"SSH Brute Force";               │
│      threshold:type threshold, track by_src, count 5, seconds 60;) │
│                                                                     │
│  alert tcp any any -> any 80 (msg:"SQL Injection Attempt";         │
│      content:"SELECT"; nocase; content:"UNION"; nocase;)           │
│                                                                     │
│  drop tcp any any -> any 445 (msg:"SMB Exploit Block";             │
│      content:"|FF|SMB"; depth:4;)                                   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  Action 유형:                                                       │
│  • alert: 알림만                                                    │
│  • log: 로그만                                                      │
│  • drop: 차단 (IPS 모드)                                            │
│  • reject: 차단 + RST 전송                                          │
│  • pass: 통과                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

#### 2. 탐지 엔진 구조

```text
                    [ IDS/IPS 탐지 엔진 ]

┌─────────────────────────────────────────────────────────────────────┐
│                        Packet Capture                               │
│                   (libpcap / AF_PACKET / DPDK)                      │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Protocol Decoder                               │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐              │
│   │ Ethernet│  │   IP    │  │   TCP   │  │  HTTP   │              │
│   │ Decoder │  │ Decoder │  │ Decoder │  │ Decoder │              │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘              │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Preprocessors                                   │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐              │
│   │ Stream  │  │ Frag    │  │ HTTP    │  │ Portscan│              │
│   │Reassembly│ │Reassembly│ │ Normalize│ │Detector │              │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘              │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Detection Engine                                │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │                    Rule Matching                             │  │
│   │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │  │
│   │   │  Content    │  │   PCRE      │  │   Flowbit   │        │  │
│   │   │  Matching   │  │   Regex     │  │   Tracking  │        │  │
│   │   └─────────────┘  └─────────────┘  └─────────────┘        │  │
│   └─────────────────────────────────────────────────────────────┘  │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │                  Anomaly Detection                           │  │
│   │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │  │
│   │   │  Protocol   │  │  Threshold  │  │  Behavior   │        │  │
│   │   │  Anomaly    │  │  Exceeded   │  │  Profiling  │        │  │
│   │   └─────────────┘  └─────────────┘  └─────────────┘        │  │
│   └─────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Output / Response                                │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐              │
│   │  Alert  │  │   Log   │  │  Block  │  │  SIEM   │              │
│   │  File   │  │  File   │  │ (IPS)   │  │Forward  │              │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘              │
└─────────────────────────────────────────────────────────────────────┘
```

#### 3. 핵심 알고리즘 & 실무 코드

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
from datetime import datetime
import re
import struct

class ActionType(Enum):
    ALERT = "alert"
    LOG = "log"
    PASS = "pass"
    DROP = "drop"
    REJECT = "reject"

class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    IP = "ip"
    ANY = "any"

@dataclass
class IDSRule:
    """IDS/IPS 규칙"""
    rule_id: int
    action: ActionType
    protocol: Protocol
    source_ip: str
    source_port: str
    dest_ip: str
    dest_port: str
    message: str
    content_matches: List[str] = field(default_factory=list)
    pcre_pattern: Optional[str] = None
    threshold_count: int = 1
    threshold_seconds: int = 60
    enabled: bool = True
    sid: int = 0
    rev: int = 1
    reference: List[str] = field(default_factory=list)

@dataclass
class Alert:
    """탐지 알림"""
    timestamp: datetime
    rule_id: int
    message: str
    source_ip: str
    dest_ip: str
    source_port: int
    dest_port: int
    protocol: str
    priority: int
    classification: str
    payload_snippet: bytes

class IDSEngine:
    """IDS/IPS 탐지 엔진"""

    def __init__(self):
        self.rules: List[IDSRule] = []
        self.alerts: List[Alert] = []
        self.threshold_tracker: Dict[Tuple, List[datetime]] = {}
        self.packet_count = 0

    def load_rule(self, rule: IDSRule):
        """규칙 로드"""
        self.rules.append(rule)

    def load_rules_from_snort(self, snort_rule: str) -> Optional[IDSRule]:
        """Snort 규칙 파싱 (간소화)"""
        # 예: alert tcp any any -> any 80 (msg:"Test"; content:"GET";)
        try:
            parts = snort_rule.split('(')
            header = parts[0].strip().split()
            options = parts[1].rstrip(')') if len(parts) > 1 else ""

            action = ActionType(header[0].upper())
            protocol = Protocol(header[1].lower())

            # 소스/목적지 파싱
            source_ip = header[2]
            source_port = header[3]
            dest_ip = header[5]  # -> 다음
            dest_port = header[6]

            # 옵션 파싱
            msg_match = re.search(r'msg:"([^"]+)"', options)
            content_matches = re.findall(r'content:"([^"]+)"', options)

            rule = IDSRule(
                rule_id=len(self.rules) + 1,
                action=action,
                protocol=protocol,
                source_ip=source_ip,
                source_port=source_port,
                dest_ip=dest_ip,
                dest_port=dest_port,
                message=msg_match.group(1) if msg_match else "No message",
                content_matches=content_matches
            )

            self.rules.append(rule)
            return rule

        except Exception as e:
            print(f"Rule parsing error: {e}")
            return None

    def _match_ip(self, packet_ip: str, rule_ip: str) -> bool:
        """IP 매칭"""
        if rule_ip == "any":
            return True
        # CIDR 처리 (간소화)
        if '/' in rule_ip:
            import ipaddress
            try:
                network = ipaddress.ip_network(rule_ip, strict=False)
                return ipaddress.ip_address(packet_ip) in network
            except:
                return False
        return packet_ip == rule_ip

    def _match_port(self, packet_port: int, rule_port: str) -> bool:
        """포트 매칭"""
        if rule_port == "any":
            return True
        if ':' in rule_port:
            start, end = map(int, rule_port.split(':'))
            return start <= packet_port <= end
        return packet_port == int(rule_port)

    def _match_content(self, payload: bytes, content: str) -> bool:
        """페이로드 내용 매칭"""
        try:
            pattern = content.encode('utf-8', errors='ignore')
            return pattern in payload
        except:
            return False

    def _check_threshold(self, rule: IDSRule, packet: dict) -> bool:
        """임계값 확인 (threshold)"""
        key = (rule.rule_id, packet['source_ip'])

        now = datetime.utcnow()
        if key not in self.threshold_tracker:
            self.threshold_tracker[key] = []

        # 만료된 타임스탬프 제거
        cutoff = now - __import__('datetime').timedelta(seconds=rule.threshold_seconds)
        self.threshold_tracker[key] = [
            ts for ts in self.threshold_tracker[key] if ts > cutoff
        ]

        # 카운트 증가
        self.threshold_tracker[key].append(now)

        return len(self.threshold_tracker[key]) >= rule.threshold_count

    def process_packet(self, packet: dict) -> List[Alert]:
        """
        패킷 처리 및 규칙 매칭

        Args:
            packet: {
                'source_ip': str,
                'dest_ip': str,
                'source_port': int,
                'dest_port': int,
                'protocol': Protocol,
                'payload': bytes,
                'flags': str
            }
        """
        self.packet_count += 1
        alerts = []

        for rule in self.rules:
            if not rule.enabled:
                continue

            # 프로토콜 매칭
            if rule.protocol != Protocol.ANY and packet['protocol'] != rule.protocol:
                continue

            # IP/포트 매칭
            if not self._match_ip(packet['source_ip'], rule.source_ip):
                continue
            if not self._match_port(packet['source_port'], rule.source_port):
                continue
            if not self._match_ip(packet['dest_ip'], rule.dest_ip):
                continue
            if not self._match_port(packet['dest_port'], rule.dest_port):
                continue

            # 콘텐츠 매칭
            if rule.content_matches:
                all_match = all(
                    self._match_content(packet['payload'], c)
                    for c in rule.content_matches
                )
                if not all_match:
                    continue

            # PCRE 매칭
            if rule.pcre_pattern:
                try:
                    if not re.search(rule.pcre_pattern, packet['payload'].decode('utf-8', errors='ignore')):
                        continue
                except:
                    continue

            # 임계값 확인
            if not self._check_threshold(rule, packet):
                continue

            # 알림 생성
            alert = Alert(
                timestamp=datetime.utcnow(),
                rule_id=rule.rule_id,
                message=rule.message,
                source_ip=packet['source_ip'],
                dest_ip=packet['dest_ip'],
                source_port=packet['source_port'],
                dest_port=packet['dest_port'],
                protocol=packet['protocol'].value,
                priority=1,
                classification="attempted-admin",
                payload_snippet=packet['payload'][:100]
            )
            alerts.append(alert)
            self.alerts.append(alert)

        return alerts

    def get_statistics(self) -> dict:
        """통계 반환"""
        return {
            "total_packets": self.packet_count,
            "total_alerts": len(self.alerts),
            "total_rules": len(self.rules),
            "active_rules": sum(1 for r in self.rules if r.enabled),
            "alerts_by_protocol": self._count_by_protocol()
        }

    def _count_by_protocol(self) -> Dict[str, int]:
        counts = {}
        for alert in self.alerts:
            counts[alert.protocol] = counts.get(alert.protocol, 0) + 1
        return counts


# 사용 예시
if __name__ == "__main__":
    ids = IDSEngine()

    # 규칙 로드
    ids.load_rule(IDSRule(
        rule_id=1,
        action=ActionType.ALERT,
        protocol=Protocol.TCP,
        source_ip="any",
        source_port="any",
        dest_ip="any",
        dest_port="80",
        message="HTTP GET Request Detected",
        content_matches=["GET"]
    ))

    ids.load_rule(IDSRule(
        rule_id=2,
        action=ActionType.ALERT,
        protocol=Protocol.TCP,
        source_ip="any",
        source_port="any",
        dest_ip="any",
        dest_port="22",
        message="SSH Brute Force Attempt",
        threshold_count=5,
        threshold_seconds=60
    ))

    ids.load_rule(IDSRule(
        rule_id=3,
        action=ActionType.DROP,
        protocol=Protocol.TCP,
        source_ip="any",
        source_port="any",
        dest_ip="any",
        dest_port="445",
        message="SMB Exploit Attempt",
        content_matches=["|FF|SMB"]
    ))

    # 패킷 테스트
    packets = [
        {
            "source_ip": "192.168.1.10",
            "dest_ip": "10.0.0.1",
            "source_port": 45123,
            "dest_port": 80,
            "protocol": Protocol.TCP,
            "payload": b"GET /index.html HTTP/1.1\r\nHost: example.com\r\n"
        },
        {
            "source_ip": "192.168.1.20",
            "dest_ip": "10.0.0.2",
            "source_port": 45124,
            "dest_port": 22,
            "protocol": Protocol.TCP,
            "payload": b"SSH-2.0-OpenSSH_8.0"
        }
    ]

    print("=== IDS/IPS 패킷 처리 ===")
    for pkt in packets:
        alerts = ids.process_packet(pkt)
        for alert in alerts:
            print(f"[ALERT] {alert.message}")
            print(f"  Source: {alert.source_ip}:{alert.source_port}")
            print(f"  Dest: {alert.dest_ip}:{alert.dest_port}")

    print(f"\n=== 통계 ===")
    stats = ids.get_statistics()
    print(f"총 패킷: {stats['total_packets']}")
    print(f"총 알림: {stats['total_alerts']}")
