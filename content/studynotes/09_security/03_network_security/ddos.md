+++
title = "DDoS 공격 및 방어"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# DDoS 공격 및 방어

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DDoS(Distributed Denial of Service)는 여러 출발지에서 동시에 대량의 트래픽을 전송하여 타겟 시스템의 자원을 고갈시키는 가용성 공격입니다.
> 2. **가치**: 볼류메트릭(대역폭), 프로토콜(상태 테이블), 애플리케이션(리소스) 계층 공격이 있으며, Anycast, Scrubbing Center, CDN, WAF로 방어합니다.
> 3. **융합**: IoT 봇넷(Mirai), 증폭 공격(DNS/NTP), 랜섬 DDoS로 진화했으며, AI 기반 실시간 탐지와 클라우드 DDoS 서비스가 표준입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**DoS vs DDoS**
- **DoS (Denial of Service)**: 단일 출발지에서의 공격
- **DDoS (Distributed DoS)**: 분산된 다수 출발지(봇넷)에서의 동시 공격

**DDoS 공격 유형**:
| 계층 | 공격 유형 | 원리 | 대표 사례 |
|:---|:---|:---|:---|
| **볼류메트릭** | 대역폭 고갈 | 대량 트래픽으로 링크 포화 | UDP Flood, ICMP Flood |
| **프로토콜** | 상태 테이블 고갈 | 연결 상태 자원 소진 | SYN Flood, ACK Flood |
| **애플리케이션** | 리소스 고갈 | HTTP 요청, DB 쿼리 과부하 | HTTP Flood, Slowloris |

**증폭/반사 공격**:
| 공격 | 증폭 비율 | 포트 | 방어 |
|:---|:---|:---|:---|
| DNS Amplification | 28~54x | 53/UDP | DNS 서버 설정, BCP38 |
| NTP Amplification | 556x | 123/UDP | monlist 비활성화 |
| Memcached | 51,000x | 11211/UDP | UDP 비활성화 |
| SSDP | 30x | 1900/UDP | UPnP 비활성화 |

#### 2. 비유를 통한 이해
DDoS는 **'출근길 지하철 혼잡'**에 비유할 수 있습니다:

```
정상 상황:
[사람들] → [지하철역] → [회사]
         100명/분   정상 운행

DDoS 공격:
[가짜 승객 10만 명] → [지하철역 붕괴] → [출근 불가]
                역 용량 초과

볼류메트릭: 모든 출입구 동시 진입
프로토콜: 개찰구만 붙잡고 있기 (SYN Flood)
애플리케이션: 안내소에 질문만 계속하기 (HTTP Flood)
```

#### 3. 등장 배경 및 발전 과정
| 연도 | 사건 | 특징 |
|:---|:---|:---|
| **1999** | Mafiaboy | Yahoo, eBay 공격, 1.5G 월 서비스 중단 |
| **2000년대** | 봇넷 등장 | 대규모 좀비 PC |
| **2007** | Estonia 공격 | 국가 차원 DDoS |
| **2013** | Spamhaus | 300Gbps, 당시 최대 |
| **2016** | Mirai | IoT 봇넷, Dyn 공격 1Tbps |
| **2018** | GitHub | 1.35Tbps, Memcached 증폭 |
| **2020** | 랜섬 DDoS | Ragnar, Lazarus |
| **2023** | HTTP/2 Rapid Reset | 프로토콜 취약점 악용 |

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. DDoS 공격 아키텍처

```text
                    [ DDoS 공격 구조 ]

┌─────────────────────────────────────────────────────────────────────┐
│                          공격자 (Attacker)                          │
│                         C2 서버 (Command & Control)                 │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌────────────┐      ┌────────────┐      ┌────────────┐
    │   봇넷 1   │      │   봇넷 2   │      │   봇넷 3   │
    │ (IoT 기기) │      │ (PC 좀비)  │      │ (증폭 서버)│
    ├────────────┤      ├────────────┤      ├────────────┤
    │ IP: 1.1.1.1│      │ IP: 2.2.2.2│      │ DNS 서버   │
    │ IP: 1.1.1.2│      │ IP: 2.2.2.3│      │ NTP 서버   │
    │    ...     │      │    ...     │      │ Memcached  │
    └─────┬──────┘      └─────┬──────┘      └─────┬──────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                              ▼
              ┌──────────────────────────────┐
              │         타겟 시스템           │
              │   ┌──────────────────────┐   │
              │   │  방화벽 (State Table)│   │ ← SYN Flood 대상
              │   └──────────────────────┘   │
              │   ┌──────────────────────┐   │
              │   │  웹 서버 (HTTP)      │   │ ← HTTP Flood 대상
              │   └──────────────────────┘   │
              │   ┌──────────────────────┐   │
              │   │  대역폭 (ISP Link)   │   │ ← 볼류메트릭 대상
              │   └──────────────────────┘   │
              └──────────────────────────────┘


                    [ DDoS 방어 아키텍처 ]

┌─────────────────────────────────────────────────────────────────────┐
│                        클라우드 DDoS 방어                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [ 사용자 ] ──────────► [ Anycast DNS ] ◄────────── [ 사용자 ]    │
│                              │                                      │
│                    ┌─────────┴─────────┐                           │
│                    │                   │                           │
│                    ▼                   ▼                           │
│            ┌─────────────┐     ┌─────────────┐                    │
│            │ Scrubbing   │     │ Scrubbing   │  (지역 1)           │
│            │ Center 1    │     │ Center 2    │  (지역 2)           │
│            │ ┌─────────┐ │     │ ┌─────────┐ │                    │
│            │ │ 볼류메트릭│ │     │ │ 볼류메트릭│ │                    │
│            │ │ 필터링   │ │     │ │ 필터링   │ │                    │
│            │ └─────────┘ │     │ └─────────┘ │                    │
│            │ ┌─────────┐ │     │ ┌─────────┐ │                    │
│            │ │ 프로토콜 │ │     │ │ 프로토콜 │ │                    │
│            │ │ 필터링   │ │     │ │ 필터링   │ │                    │
│            │ └─────────┘ │     │ └─────────┘ │                    │
│            └──────┬──────┘     └──────┬──────┘                    │
│                   │                   │                           │
│                   └─────────┬─────────┘                           │
│                             │                                      │
│                             ▼ Clean Traffic                       │
│   ┌────────────────────────────────────────────────────────────┐  │
│   │                     고객 데이터센터                         │  │
│   │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │  │
│   │   │   WAF   │  │   FW    │  │   LB    │  │ Web Srv │      │  │
│   │   │(App 계층)│  │(네트워크)│  │         │  │         │      │  │
│   │   └─────────┘  └─────────┘  └─────────┘  └─────────┘      │  │
│   └────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### 2. 공격 유형별 상세 분석

```text
                    [ SYN Flood 공격 원리 ]

정상 TCP 핸드쉐이크:
Client ──SYN──► Server
Client ◄─SYN+ACK─ Server
Client ──ACK──► Server  → 연결 완료

SYN Flood 공격:
공격자 ──SYN──► Server (소스 IP 위조)
공격자 ◄─SYN+ACK─ Server (도달하지 않음)
공격자 (무응답)     Server → SYN_RECEIVED 상태 유지
     반복...       Server → 백로그 큐 포화 → 정상 연결 불가

대응:
1. SYN Cookies: 시퀀스 번호로 클라이언트 식별, 상태 미저장
2. SYN Proxy: 방화벽이 대신 SYN+ACK 응답
3. Rate Limiting: SYN 패킷 속도 제한


                    [ DNS 증폭 공격 원리 ]

정상 DNS 쿼리:
Client ──Query(1개)──► DNS Server
Client ◄──Response(1개)── DNS Server

DNS 증폭 공격:
공격자 ──Query(any, 위조된 소스IP)──► Open DNS Server
타겟   ◄──Response(수천 배 증폭)─── Open DNS Server

쿼리: dig ANY target.com @open-dns (30바이트)
응답: 4,000바이트 (130배 증폭)

대응:
1. Open DNS 서버 설정 금지
2. BCP38 (소스 IP 검증)
3. DNS 서버 응답 크기 제한 (EDNS0)
```

#### 3. 핵심 알고리즘 & 실무 코드

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict
import ipaddress

class AttackType(Enum):
    SYN_FLOOD = "syn_flood"
    UDP_FLOOD = "udp_flood"
    ICMP_FLOOD = "icmp_flood"
    HTTP_FLOOD = "http_flood"
    DNS_AMP = "dns_amplification"
    SLOWLORIS = "slowloris"

class MitigationAction(Enum):
    ALLOW = "allow"
    RATE_LIMIT = "rate_limit"
    CHALLENGE = "challenge"
    BLOCK = "block"

@dataclass
class TrafficStats:
    """트래픽 통계"""
    packets_per_second: float = 0.0
    bytes_per_second: float = 0.0
    syn_count: int = 0
    udp_count: int = 0
    icmp_count: int = 0
    http_count: int = 0
    unique_sources: int = 0

@dataclass
class DDoSAlert:
    """DDoS 탐지 알림"""
    timestamp: datetime
    attack_type: AttackType
    source_ip: str
    target_ip: str
    pps: float
    bps: float
    severity: str
    mitigation: str

class DDoSDetector:
    """DDoS 탐지 엔진"""

    def __init__(self):
        # 임계값 설정
        self.thresholds = {
            'pps_high': 100000,      # 초당 패킷 높음
            'pps_critical': 500000,  # 초당 패킷 위험
            'bps_high': 1000000000,  # 1 Gbps
            'bps_critical': 5000000000,  # 5 Gbps
            'syn_ratio': 0.3,        # SYN 패킷 비율
            'udp_ratio': 0.5,        # UDP 패킷 비율
            'source_entropy': 0.5,   # 소스 IP 엔트로피
        }

        # 통계 추적
        self.packet_window: List[Tuple[datetime, dict]] = []
        self.window_size = timedelta(seconds=10)

        # IP별 추적
        self.ip_syn_count: Dict[str, int] = defaultdict(int)
        self.ip_packet_count: Dict[str, int] = defaultdict(int)

        # 알림
        self.alerts: List[DDoSAlert] = []

    def process_packet(self, packet: dict) -> Optional[DDoSAlert]:
        """
        패킷 분석 및 공격 탐지

        Args:
            packet: {
                'timestamp': datetime,
                'source_ip': str,
                'dest_ip': str,
                'source_port': int,
                'dest_port': int,
                'protocol': str,
                'size': int,
                'flags': str (TCP)
            }
        """
        now = datetime.utcnow()

        # 윈도우에 패킷 추가
        self.packet_window.append((now, packet))

        # 오래된 패킷 제거
        cutoff = now - self.window_size
        self.packet_window = [(ts, p) for ts, p in self.packet_window if ts > cutoff]

        # SYN 카운트 업데이트
        if packet['protocol'] == 'tcp' and 'SYN' in packet.get('flags', ''):
            self.ip_syn_count[packet['source_ip']] += 1

        self.ip_packet_count[packet['source_ip']] += 1

        # 주기적 분석 (100패킷마다)
        if len(self.packet_window) % 100 == 0:
            return self._analyze_traffic(now)

        return None

    def _analyze_traffic(self, now: datetime) -> Optional[DDoSAlert]:
        """트래픽 분석 및 공격 탐지"""
        if not self.packet_window:
            return None

        # 통계 계산
        total_packets = len(self.packet_window)
        total_bytes = sum(p['size'] for _, p in self.packet_window)
        window_seconds = self.window_size.total_seconds()

        pps = total_packets / window_seconds
        bps = total_bytes * 8 / window_seconds  # bits per second

        # 프로토콜별 카운트
        syn_count = sum(1 for _, p in self.packet_window
                       if p['protocol'] == 'tcp' and 'SYN' in p.get('flags', ''))
        udp_count = sum(1 for _, p in self.packet_window if p['protocol'] == 'udp')

        # 고유 소스 IP
        unique_sources = len(set(p['source_ip'] for _, p in self.packet_window))

        # 1. 볼류메트릭 공격 탐지
        if bps > self.thresholds['bps_critical']:
            return self._create_alert(
                now, AttackType.UDP_FLOOD, "0.0.0.0", "target",
                pps, bps, "critical",
                "Redirect to scrubbing center"
            )

        # 2. SYN Flood 탐지
        if total_packets > 0 and syn_count / total_packets > self.thresholds['syn_ratio']:
            # SYN Cookie 활성화 권장
            top_syn_sources = sorted(
                self.ip_syn_count.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]

            return self._create_alert(
                now, AttackType.SYN_FLOOD,
                top_syn_sources[0][0] if top_syn_sources else "0.0.0.0",
                "target", pps, bps, "high",
                "Enable SYN cookies, Rate limit SYN packets"
            )

        # 3. UDP Flood 탐지
        if total_packets > 0 and udp_count / total_packets > self.thresholds['udp_ratio']:
            return self._create_alert(
                now, AttackType.UDP_FLOOD, "0.0.0.0", "target",
                pps, bps, "high",
                "Rate limit UDP, Block unnecessary UDP ports"
            )

        # 4. 분산 공격 탐지 (높은 엔트로피)
        if unique_sources > 10000 and pps > self.thresholds['pps_high']:
            return self._create_alert(
                now, AttackType.HTTP_FLOOD, "distributed", "target",
                pps, bps, "critical",
                "Enable JS challenge, Geo-blocking"
            )

        return None

    def _create_alert(self, timestamp: datetime, attack_type: AttackType,
                      source_ip: str, target_ip: str,
                      pps: float, bps: float,
                      severity: str, mitigation: str) -> DDoSAlert:
        alert = DDoSAlert(
            timestamp=timestamp,
            attack_type=attack_type,
            source_ip=source_ip,
            target_ip=target_ip,
            pps=pps,
            bps=bps,
            severity=severity,
            mitigation=mitigation
        )
        self.alerts.append(alert)
        return alert


class DDoSMitigator:
    """DDoS 완화 엔진"""

    def __init__(self):
        self.blocked_ips: set = set()
        self.rate_limits: Dict[str, int] = {}  # IP -> packets/sec
        self.geo_block: set = set()  # 국가 코드

    def block_ip(self, ip: str, duration_minutes: int = 60):
        """IP 차단"""
        self.blocked_ips.add(ip)
        # 실제로는 방화벽 API 호출

    def rate_limit(self, ip: str, pps: int):
        """속도 제한 설정"""
        self.rate_limits[ip] = pps

    def geo_block_country(self, country_code: str):
        """국가 차단"""
        self.geo_block.add(country_code)

    def get_mitigation_rules(self) -> List[str]:
        """완화 규칙 목록"""
        rules = []

        # IP 차단 규칙
        for ip in self.blocked_ips:
            rules.append(f"deny {ip} any any")

        # 속도 제한 규칙
        for ip, pps in self.rate_limits.items():
            rules.append(f"rate-limit {ip} {pps}pps")

        # Geo 차단 규칙
        for country in self.geo_block:
            rules.append(f"geo-block {country}")

        return rules

    def apply_challenge(self, source_ip: str) -> dict:
        """JavaScript 챌린지 적용"""
        import secrets
        challenge_token = secrets.token_hex(16)

        return {
            "action": "challenge",
            "token": challenge_token,
            "expires_in": 30,
            "script": f"""
            <script>
            function solve() {{
                // 간단한 계산 챌린지
                var answer = {int(challenge_token[:8], 16) % 1000};
                document.cookie = "ddos_challenge={challenge_token}; path=/";
                location.reload();
            }}
            setTimeout(solve, 100);
            </script>
            """
        }


# 사용 예시
if __name__ == "__main__":
    import random

    detector = DDoSDetector()
    mitigator = DDoSMitigator()

    print("=== DDoS 탐지 시뮬레이션 ===")

    # 정상 트래픽 + 공격 트래픽 생성
    for i in range(1000):
        # 80% 정상, 20% 공격
        if random.random() < 0.8:
            # 정상 트래픽
            packet = {
                'timestamp': datetime.utcnow(),
                'source_ip': f"192.168.1.{random.randint(1, 100)}",
                'dest_ip': "10.0.0.1",
                'source_port': random.randint(40000, 60000),
                'dest_port': 80,
                'protocol': 'tcp',
                'size': random.randint(100, 1500),
                'flags': 'ACK'
            }
        else:
            # SYN Flood 공격
            packet = {
                'timestamp': datetime.utcnow(),
                'source_ip': f"1.2.3.{random.randint(1, 255)}",
                'dest_ip': "10.0.0.1",
                'source_port': random.randint(1024, 65535),
                'dest_port': 80,
                'protocol': 'tcp',
                'size': 64,
                'flags': 'SYN'
            }

        alert = detector.process_packet(packet)
        if alert:
            print(f"\n[ALERT] {alert.attack_type.value}")
            print(f"  PPS: {alert.pps:.0f}, BPS: {alert.bps/1e6:.1f} Mbps")
            print(f"  Severity: {alert.severity}")
            print(f"  Mitigation: {alert.mitigation}")

            # 자동 완화
            if alert.severity == "critical":
                mitigator.block_ip(alert.source_ip)

    print(f"\n=== 완화 규칙 ===")
    for rule in mitigator.get_mitigation_rules()[:5]:
        print(f"  {rule}")
