+++
title = "네트워크 주소 변환 (NAT)"
date = 2024-05-18
description = "NAT의 동작 원리, Static/Dynamic/PAT 유형 분석, NAT 횡단 기술(STUN/TURN/ICE) 및 보안·성능 영향 심층 분석"
weight = 35
[taxonomies]
categories = ["studynotes-03_network"]
tags = ["NAT", "PAT", "NAPT", "IPv4", "NetworkSecurity", "AddressTranslation"]
+++

# 네트워크 주소 변환 (NAT)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NAT(Network Address Translation)는 사설 IP 주소를 공인 IP 주소로 변환하여 IPv4 주소 고갈 문제를 완화하고, 내부 네트워크 구조를 외부로부터 숨겨 보안을 강화하는 L3/L4 계층 기술입니다.
> 2. **가치**: 전 세계 40억 개의 IPv4 주소 한계를 극복하여 수십억 개의 디바이스가 인터넷에 접속할 수 있게 하며, 기업 네트워크에서는 내부 토폴로지 은닉으로 공격 표면을 60% 이상 감소시킵니다.
> 3. **융합**: NAT는 VoIP, WebRTC, P2P 애플리케이션에서 NAT 횡단(Traversal) 문제를 야기하며, STUN/TURN/ICE 프로토콜과 결합하여 해결합니다. 또한 IPv6 전환을 위한 NAT64/DNS64 기술로 진화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

NAT(Network Address Translation)는 1994년 RFC 1631에서 처음 표준화된 기술로, 라우터나 방화벽에서 패킷의 IP 주소와 포트 번호를 동적으로 변환하여 사설 네트워크와 공용 인터넷 간의 연결성을 제공합니다.

**💡 비유**: NAT는 **'건물의 우편물 수발실'**과 같습니다.
- **내부 주소(사설 IP)**: 각 사무실의 내선 번호 (예: 101호, 202호)
- **외부 주소(공인 IP)**: 건물의 대표 주소 (예: 서울시 강남구 테헤란로 123)
- **NAT 테이블**: 수발실의 우편물 배송 기록부 (누가 언제 어디로 보냈는지)
- **PAT (Port Address Translation)**: 하나의 대표 주소로 여러 부서의 우편물을 구분하여 처리

**등장 배경 및 발전 과정**:
1. **IPv4 주소 고갈 위기**: 1990년대 인터넷 폭발적 성장으로 IPv4 주소(32비트, 약 43억 개)가 빠르게 소진되었습니다. IANA는 2011년에 마지막 /8 블록을 배포했습니다.
2. **사설 IP 주소 체계 (RFC 1918)**: 내부 네트워크용으로 예약된 주소 대역을 정의하여, 이 주소들은 인터넷에서 라우팅되지 않습니다.
3. **NAT의 표준화**: 사설 IP를 공인 IP로 변환하여 인터넷 접속을 가능하게 하는 NAT 기술이 필수적인 인프라가 되었습니다.

### 사설 IP 주소 대역 (RFC 1918)

| 클래스 | 주소 범위 | CIDR | 용도 |
|--------|----------|------|------|
| **A** | 10.0.0.0 ~ 10.255.255.255 | 10.0.0.0/8 | 대규모 기업, 클라우드 |
| **B** | 172.16.0.0 ~ 172.31.255.255 | 172.16.0.0/12 | 중형 기업, AWS VPC |
| **C** | 192.168.0.0 ~ 192.168.255.255 | 192.168.0.0/16 | 소규모 네트워크, 가정용 공유기 |

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: NAT 유형 분류

| NAT 유형 | 영문 명칭 | 변환 방식 | 매핑 특성 | 주요 적용 |
|---------|----------|----------|----------|----------|
| **Static NAT** | 1:1 NAT | 사설 IP ↔ 공인 IP (고정) | 영구 매핑 | 서버 공개, DMZ |
| **Dynamic NAT** | Pool-based NAT | 사설 IP → 공인 IP Pool (동적) | 세션 기반 매핑 | 일반 사용자 |
| **PAT/NAPT** | Port Address Translation | 사설 IP:Port → 공인 IP:Port | 포트 기반 매핑 | 가정용 공유기 |
| **Overloading** | PAT의 다른 명칭 | 다수 사설 IP → 단일 공인 IP | 포트 다중화 | ISP, 모바일 |
| **Bidirectional NAT** | Two-Way NAT | 양방향 변환 | 양쪽 모두 변환 | 데이터센터 |

### 정교한 구조 다이어그램: NAT 동작 메커니즘

```ascii
================================================================================
[ NAT (Network Address Translation) Architecture - PAT/NAPT ]
================================================================================

                        [ 인터넷 (Public Internet) ]
                                  |
                                  | 8.8.8.8 (Google DNS)
                                  |
                    +-------------+-------------+
                    |   NAT Router / Firewall   |
                    |   ====================   |
                    |   Outside: 203.0.113.1   |<-- 공인 IP (WAN)
                    |   Inside:  192.168.1.1   |<-- 사설 IP (LAN Gateway)
                    |                           |
                    |   NAT Translation Table:  |
                    |   =======================|
                    |   Inside Local     | Inside Global
                    |   (사설IP:Port)    | (공인IP:Port)
                    |   -----------------+----------------
                    |   192.168.1.10:5001| 203.0.113.1:20001
                    |   192.168.1.11:5002| 203.0.113.1:20002
                    |   192.168.1.12:5003| 203.0.113.1:20003
                    +-------------+-------------+
                                  |
                    +-------------+-------------+
                    |   Internal LAN Switch     |
                    +-------------+-------------+
                      /           |           \
                     /            |            \
        +-----------+--+  +------+-------+  +--+-----------+
        |   PC 1       |  |   PC 2       |  |   PC 3       |
        |192.168.1.10  |  |192.168.1.11  |  |192.168.1.12  |
        |Port: 5001    |  |Port: 5002    |  |Port: 5003    |
        +--------------+  +--------------+  +--------------+

================================================================================
[ Outbound Packet Transformation ]
================================================================================

PC 1에서 8.8.8.8:53으로 DNS 쿼리 전송:

[ 변환 전 (Inside Local) ]
+--------------------------------------------------+
| Source IP: 192.168.1.10                          |
| Source Port: 5001                                |
| Destination IP: 8.8.8.8                          |
| Destination Port: 53 (DNS)                       |
| Protocol: UDP                                    |
+--------------------------------------------------+
                         |
                         v NAT 변환
[ 변환 후 (Inside Global) ]
+--------------------------------------------------+
| Source IP: 203.0.113.1                           |
| Source Port: 20001                               |
| Destination IP: 8.8.8.8                          |
| Destination Port: 53 (DNS)                       |
| Protocol: UDP                                    |
+--------------------------------------------------+
                         |
                         v 인터넷 전송
                    [ 8.8.8.8 (Google DNS) ]


================================================================================
[ Inbound Response Transformation ]
================================================================================

Google DNS에서 응답:

[ 수신 패킷 (Outside) ]
+--------------------------------------------------+
| Source IP: 8.8.8.8                               |
| Source Port: 53                                  |
| Destination IP: 203.0.113.1                      |
| Destination Port: 20001                          |
+--------------------------------------------------+
                         |
                         v NAT 역변환
[ 변환 후 (Inside) ]
+--------------------------------------------------+
| Source IP: 8.8.8.8                               |
| Source Port: 53                                  |
| Destination IP: 192.168.1.10                     |
| Destination Port: 5001                           |
+--------------------------------------------------+
                         |
                         v
                    [ PC 1로 전달 ]

================================================================================
[ NAT 유형별 매핑 특성 ]
================================================================================

1. Full Cone NAT (완전 원뿔형)
   - 내부 주소:포트가 한 번 매핑되면, 모든 외부 호스트가 접근 가능
   - 가장 관대한 유형, P2P 친화적

2. Restricted Cone NAT (제한 원뿔형)
   - 내부에서 먼저 요청을 보낸 외부 호스트만 응답 가능
   - IP 기반 제한

3. Port Restricted Cone NAT (포트 제한 원뿔형)
   - 내부에서 요청한 외부 호스트의 특정 포트에서만 응답 가능
   - IP + Port 기반 제한

4. Symmetric NAT (대칭형)
   - 대상별로 다른 매핑 생성
   - 가장 엄격한 유형, P2P 어려움

================================================================================
```

### 심층 동작 원리: PAT (Port Address Translation)

**PAT의 핵심 원리**:
- 단일 공인 IP 주소를 여러 내부 호스트가 공유
- TCP/UDP 포트 번호를 사용하여 세션 구분
- 최대 65,536개의 동시 연결 가능 (이론적 한계)

**포트 할당 알고리즘**:
```
1. 내부 호스트에서 새 연결 시도
2. NAT 라우터가 사용 가능한 외부 포트 검색
3. (사설 IP, 내부 포트) → (공인 IP, 외부 포트) 매핑 생성
4. 매핑 타이머 시작 (TCP: 기본 24시간, UDP: 기본 5분)
5. 연결 종료 또는 타임아웃 시 매핑 삭제
```

### NAT 트래버설 (Traversal) 기술

```python
"""
NAT Traversal 기술 시뮬레이션

STUN, TURN, ICE 프로토콜의 동작 원리
"""

import socket
import struct
from dataclasses import dataclass
from typing import Tuple, Optional
from enum import Enum

class NATType(Enum):
    FULL_CONE = "Full Cone"
    RESTRICTED_CONE = "Restricted Cone"
    PORT_RESTRICTED_CONE = "Port Restricted Cone"
    SYMMETRIC = "Symmetric"

@dataclass
class NATMapping:
    """NAT 매핑 엔트리"""
    inside_ip: str
    inside_port: int
    outside_ip: str
    outside_port: int
    external_ip: str  # 공인 IP
    external_port: int  # 매핑된 외부 포트
    last_used: float  # 마지막 사용 시간

class NATSimulator:
    """
    NAT 장비 시뮬레이터

    다양한 NAT 유형의 동작을 모델링
    """

    def __init__(self, external_ip: str, nat_type: NATType):
        self.external_ip = external_ip
        self.nat_type = nat_type
        self.mappings: dict = {}  # (inside_ip, inside_port) -> NATMapping
        self.port_pool = iter(range(20000, 60000))  # 동적 포트 풀
        self.allowed_senders: dict = {}  # Restricted NAT용 허용 목록

    def process_outbound(self, inside_ip: str, inside_port: int,
                         dest_ip: str, dest_port: int) -> Tuple[str, int]:
        """
        아웃바운드 패킷 처리

        Returns:
            (외부 IP, 외부 포트) - 변환된 주소
        """
        key = (inside_ip, inside_port)

        # Symmetric NAT: 대상마다 다른 매핑
        if self.nat_type == NATType.SYMMETRIC:
            key = (inside_ip, inside_port, dest_ip, dest_port)

        # 기존 매핑 확인
        if key in self.mappings:
            mapping = self.mappings[key]
            mapping.last_used = 0  # 갱신
            return mapping.external_ip, mapping.external_port

        # 새 매핑 생성
        external_port = next(self.port_pool)
        mapping = NATMapping(
            inside_ip=inside_ip,
            inside_port=inside_port,
            outside_ip=dest_ip,
            outside_port=dest_port,
            external_ip=self.external_ip,
            external_port=external_port,
            last_used=0
        )
        self.mappings[key] = mapping

        # Restricted NAT: 허용 목록에 추가
        if self.nat_type in [NATType.RESTRICTED_CONE, NATType.PORT_RESTRICTED_CONE]:
            allowed_key = (inside_ip, inside_port, dest_ip)
            if self.nat_type == NATType.PORT_RESTRICTED_CONE:
                allowed_key = (inside_ip, inside_port, dest_ip, dest_port)
            self.allowed_senders[allowed_key] = True

        return self.external_ip, external_port

    def process_inbound(self, external_ip: str, external_port: int,
                        source_ip: str, source_port: int) -> Optional[Tuple[str, int]]:
        """
        인바운드 패킷 처리

        Returns:
            (내부 IP, 내부 포트) - 변환될 주소, 차단 시 None
        """
        # 외부 포트로 매핑 찾기
        mapping = None
        for m in self.mappings.values():
            if m.external_port == external_port:
                mapping = m
                break

        if not mapping:
            return None  # 매핑 없음

        # NAT 유형별 인바운드 필터링
        if self.nat_type == NATType.FULL_CONE:
            # 모든 외부 호스트 허용
            pass

        elif self.nat_type == NATType.RESTRICTED_CONE:
            # 이전에 통신한 IP에서만 허용
            allowed_key = (mapping.inside_ip, mapping.inside_port, source_ip)
            if allowed_key not in self.allowed_senders:
                return None

        elif self.nat_type == NATType.PORT_RESTRICTED_CONE:
            # 이전에 통신한 IP:Port에서만 허용
            allowed_key = (mapping.inside_ip, mapping.inside_port,
                          source_ip, source_port)
            if allowed_key not in self.allowed_senders:
                return None

        elif self.nat_type == NATType.SYMMETRIC:
            # 정확히 매칭되는 연결만 허용
            key = (mapping.inside_ip, mapping.inside_port, source_ip, source_port)
            if key not in self.mappings:
                return None

        return mapping.inside_ip, mapping.inside_port


class STUNClient:
    """
    STUN (Session Traversal Utilities for NAT) 클라이언트

    RFC 5389 기반 NAT 유형 감지 및 공인 IP/Port 획득
    """

    def __init__(self, stun_server: str, stun_port: int = 3478):
        self.stun_server = stun_server
        self.stun_port = stun_port

    def get_mapped_address(self, local_ip: str, local_port: int) -> Tuple[str, int]:
        """
        STUN 서버를 통해 매핑된 공인 주소 획득

        실제 구현에서는 STUN 프로토콜로 서버와 통신
        """
        # 시뮬레이션: NAT를 통한 매핑
        # 실제로는 STUN Binding Request/Response 교환
        print(f"[STUN] Querying mapped address from {self.stun_server}")
        # 시뮬레이션 결과 반환
        return "203.0.113.100", 25000

    def detect_nat_type(self) -> NATType:
        """
        NAT 유형 감지 (RFC 3489 절차)

        1. STUN 서버 1의 IP:Port로 요청 → 매핑 주소 확인
        2. 동일 IP의 다른 포트로 요청 → 매핑 변경 여부 확인
        3. 다른 IP의 포트로 요청 → 매핑 변경 여부 확인
        """
        print("[STUN] Detecting NAT type...")

        # 시뮬레이션 결과
        # 실제로는 여러 STUN 서버와의 통신으로 감지
        return NATType.PORT_RESTRICTED_CONE


class ICEAgent:
    """
    ICE (Interactive Connectivity Establishment) 에이전트

    RFC 8445 기반 P2P 연결 설정
    """

    def __init__(self):
        self.local_candidates = []
        self.remote_candidates = []
        self.checklist = []

    def gather_candidates(self, local_ip: str, stun_server: str):
        """
        후보 주소 수집

        1. Host Candidate: 로컬 IP 주소
        2. Server Reflexive Candidate: STUN으로 얻은 공인 주소
        3. Relayed Candidate: TURN 서버를 통한 릴레이 주소
        """
        # Host Candidate
        self.local_candidates.append({
            'type': 'host',
            'ip': local_ip,
            'port': 5000,
            'priority': 126  # 가장 높은 우선순위
        })

        # Server Reflexive Candidate (STUN)
        # 실제로는 STUN 서버와 통신
        self.local_candidates.append({
            'type': 'srflx',
            'ip': '203.0.113.100',  # 매핑된 공인 IP
            'port': 25000,
            'priority': 100
        })

        # Relayed Candidate (TURN)
        self.local_candidates.append({
            'type': 'relay',
            'ip': '198.51.100.1',  # TURN 서버 IP
            'port': 40000,
            'priority': 0  # 가장 낮은 우선순위
        })

        print(f"[ICE] Gathered {len(self.local_candidates)} candidates")
        return self.local_candidates

    def create_checklist(self, remote_candidates: list):
        """
        연결성 검사 체크리스트 생성

        각 로컬-원격 후보 쌍에 대해 검사 순서 결정
        """
        self.remote_candidates = remote_candidates
        self.checklist = []

        for local in self.local_candidates:
            for remote in remote_candidates:
                pair = {
                    'local': local,
                    'remote': remote,
                    'priority': min(local['priority'], remote['priority']),
                    'state': 'waiting'
                }
                self.checklist.append(pair)

        # 우선순위 기준 정렬
        self.checklist.sort(key=lambda x: x['priority'], reverse=True)
        print(f"[ICE] Created checklist with {len(self.checklist)} pairs")

    def perform_connectivity_checks(self):
        """
        연결성 검사 수행

        STUN Binding Request를 각 후보 쌍에 전송
        """
        for pair in self.checklist:
            print(f"[ICE] Checking {pair['local']['ip']}:{pair['local']['port']} -> "
                  f"{pair['remote']['ip']}:{pair['remote']['port']}")

            # 시뮬레이션: Host-to-Host가 가장 성공 확률 높음
            if pair['local']['type'] == 'host' and pair['remote']['type'] == 'host':
                pair['state'] = 'succeeded'
                print(f"[ICE] ✓ Direct connection possible!")
                return True

            pair['state'] = 'failed'

        # 직접 연결 실패 시 TURN 사용
        print("[ICE] Direct connection failed, using TURN relay")
        return False


# ================== 시뮬레이션 실행 ==================
if __name__ == "__main__":
    print("=" * 70)
    print("NAT and NAT Traversal Simulation Report")
    print("=" * 70)

    # NAT 시뮬레이션
    print("\n[1. NAT Type Simulation]")
    nat = NATSimulator("203.0.113.1", NATType.PORT_RESTRICTED_CONE)

    # 아웃바운드 패킷 변환
    ext_ip, ext_port = nat.process_outbound(
        "192.168.1.10", 5001, "8.8.8.8", 53
    )
    print(f"Inside: 192.168.1.10:5001 -> Outside: {ext_ip}:{ext_port}")

    # STUN 클라이언트
    print("\n[2. STUN Client]")
    stun = STUNClient("stun.l.google.com", 19302)
    mapped_ip, mapped_port = stun.get_mapped_address("192.168.1.10", 5000)
    nat_type = stun.detect_nat_type()
    print(f"Mapped Address: {mapped_ip}:{mapped_port}")
    print(f"Detected NAT Type: {nat_type.value}")

    # ICE 에이전트
    print("\n[3. ICE Agent - P2P Connection Setup]")
    ice = ICEAgent()
    local_candidates = ice.gather_candidates("192.168.1.10", "stun.l.google.com")

    # 원격 후보 (시뮬레이션)
    remote_candidates = [
        {'type': 'host', 'ip': '10.0.0.5', 'port': 5000, 'priority': 126},
        {'type': 'srflx', 'ip': '198.51.100.50', 'port': 30000, 'priority': 100},
    ]

    ice.create_checklist(remote_candidates)
    success = ice.perform_connectivity_checks()

    print(f"\n{'='*70}")
    print(f"ICE Result: {'Connected' if success else 'Relay Required'}")
    print(f"{'='*70}")
