+++
title = "SDN/NFV 아키텍처 (소프트웨어 정의 네트워킹)"
date = 2024-05-18
description = "SDN 제어/데이터 평면 분리, OpenFlow 프로토콜, NFV 가상화, MANO 프레임워크 및 클라우드 네트워크 자동화 심층 분석"
weight = 45
[taxonomies]
categories = ["studynotes-03_network"]
tags = ["SDN", "NFV", "OpenFlow", "VNF", "MANO", "CloudNetworking", "NetworkVirtualization"]
+++

# SDN/NFV 아키텍처 (소프트웨어 정의 네트워킹)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SDN(Software Defined Networking)은 네트워크의 제어 평면(Control Plane)과 데이터 평면(Data Plane)을 분리하고, 중앙 집중식 컨트롤러를 통해 전체 네트워크를 프로그래밍 방식으로 관리하는 아키텍처 패러다임입니다.
> 2. **가치**: 네트워크 구성 시간을 주 단위에서 분 단위로 단축하고, 트래픽 엔지니어링을 통해 대역폭 활용률을 30~50% 향상시키며, 벤더 종속성(Vendor Lock-in)을 완화하여 CapEx와 OpEx를 각각 40%, 60% 절감합니다.
> 3. **융합**: NFV(Network Functions Virtualization)와 결합하여 통신사 5G 코어망(5GC), 클라우드 데이터센터의 EVPN-VXLAN 오버레이, 엣지 컴퓨팅(MEC) 플랫폼의 핵심 기반 기술로 활용됩니다.

---

## Ⅰ. 개요 (Context & Background)

SDN과 NFV는 2010년대 초반 통신 사업자와 데이터센터 운영자들이 직면한 네트워크 유연성 부족과 높은 운영 비용 문제를 해결하기 위해 등장했습니다.

**💡 비유**: SDN/NFV는 **'스마트 팩토리 자동화'**와 같습니다.
- **기존 네트워크(분산형)**: 각 기계(라우터/스위치)가 독자적으로 판단하여 작동. 기계마다 다른 제조사의 프로그램이 설치되어 있어 통합 관리 어려움.
- **SDN(중앙집중형)**: 중앙 제어 시스템(컨트롤러)이 모든 기계를 통합 관리. 프로그래머가 제어 로직을 수정하면 전체 공장이 즉시 반응.
- **NFV(가상화)**: 전용 기계(라우터, 방화벽) 대신 범용 서버에서 소프트웨어(VNF)로 기능 구현. 필요할 때마다 소프트웨어를 복사하여 증설.

**등장 배경 및 발전 과정**:
1. **전통적 네트워크의 한계**: 각 벤더(Cisco, Juniper, Huawei)의 장비는 폐쇄적이고, 펌웨어 업그레이드에 수주~수개월 소요. 트래픽 변화에 유연하게 대응 불가.
2. **Stanford의 OpenFlow 연구 (2008)**: Martin Casado와 Nick McKeown 교수팀이 제어/데이터 평면 분리를 제안하며 OpenFlow 프로토콜 개발.
3. **Google B4 WAN (2012)**: Google이 전 세계 데이터센터를 연결하는 WAN에 SDN을 적용하여 대역폭 활용률을 30~40%에서 90% 이상으로 향상.
4. **ETSI NFV (2012)**: 통신 사업자 연합이 네트워크 기능 가상화 표준 프레임워크 제정.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: SDN 아키텍처 계층

| 계층 | 구성 요소 | 상세 역할 | 기술 스택 |
|------|----------|----------|----------|
| **애플리케이션 계층** | SDN Applications | 네트워크 정책, 서비스 체이닝, 트래픽 엔지니어링 | Python, Java, REST API |
| **북바운드 API** | NBI (Northbound Interface) | 앱과 컨트롤러 간 추상화 인터페이스 | REST, RESTCONF, gRPC |
| **제어 계층** | SDN Controller | 네트워크 상태 관리, 경로 계산, 정책 배포 | OpenDaylight, ONOS, Floodlight |
| **남바운드 API** | SBI (Southbound Interface) | 컨트롤러와 장비 간 통신 프로토콜 | OpenFlow, NETCONF, OVSDB |
| **인프라 계층** | Network Devices | 패킷 처리, 플로우 테이블 매칭, 포워딩 | Open vSwitch, 화이트박스 스위치 |

### 정교한 구조 다이어그램: SDN 아키텍처

```ascii
================================================================================
[ SDN (Software Defined Networking) 3-Layer Architecture ]
================================================================================

+-----------------------------------------------------------------------------+
|                      APPLICATION LAYER (애플리케이션 계층)                    |
|  +-----------+  +-----------+  +-----------+  +-----------+  +-----------+  |
|  | Network   |  | Load      |  | Firewall  |  | QoS       |  | Topology  |  |
|  | Management|  | Balancing |  | Service   |  | Manager   |  | Discovery |  |
|  +-----------+  +-----------+  +-----------+  +-----------+  +-----------+  |
+-----------------------------------------------------------------------------+
                                    |
                    +---------------|---------------+
                    |    NBI (Northbound Interface) |
                    |    REST API / RESTCONF / gRPC |
                    +---------------|---------------+
                                    v
+-----------------------------------------------------------------------------+
|                      CONTROL LAYER (제어 계층)                               |
|  +-----------------------------------------------------------------------+  |
|  |                    SDN Controller (네트워크 운영체제)                    |  |
|  |  +-------------+  +-------------+  +-------------+  +-------------+    |  |
|  |  | Topology    |  | Host        |  | Flow       |  | Statistics  |    |  |
|  |  | Manager     |  | Tracker     |  | Programmer |  | Collector   |    |  |
|  |  +-------------+  +-------------+  +-------------+  +-------------+    |  |
|  |                                                                       |  |
|  |  +-------------+  +-------------+  +-------------+  +-------------+    |  |
|  |  | Link        |  | Device      |  | Path       |  | Policy      |    |  |
|  |  | Discovery   |  | Manager     |  | Computation|  | Engine      |    |  |
|  |  +-------------+  +-------------+  +-------------+  +-------------+    |  |
|  +-----------------------------------------------------------------------+  |
|                                                                             |
|  Controller Examples: OpenDaylight, ONOS, Floodlight, Ryu                  |
+-----------------------------------------------------------------------------+
                                    |
                    +---------------|---------------+
                    |    SBI (Southbound Interface) |
                    |    OpenFlow / NETCONF / OVSDB |
                    +---------------|---------------+
                                    v
+-----------------------------------------------------------------------------+
|                    INFRASTRUCTURE LAYER (인프라 계층)                         |
|  +-----------+  +-----------+  +-----------+  +-----------+  +-----------+  |
|  |  Switch 1 |  |  Switch 2 |  |  Switch 3 |  |  Router   |  |   OVS     |  |
|  | (OpenFlow)|  | (OpenFlow)|  | (OpenFlow)|  | (NETCONF) |  | (vSwitch) |  |
|  +-----------+  +-----------+  +-----------+  +-----------+  +-----------+  |
|                                                                             |
|  Data Plane: 플로우 테이블 기반 고속 패킷 처리 (ASIC / 소프트웨어)            |
+-----------------------------------------------------------------------------+

================================================================================
[ OpenFlow Flow Table Structure ]
================================================================================

+-----------------------------------------------------------------------+
|                        Flow Table Entry                                |
+-----------------------------------------------------------------------+
| Match Fields               | Actions                  | Counters      |
| (매치 필드)                 | (액션)                   | (카운터)       |
+----------------------------+--------------------------+---------------+
| Ingress Port               | Output: Forward to port  | Received Pkts |
| Ethernet Src/Dst MAC       | Group: Group table       | Received Bytes|
| Ethernet Type (0x0800)     | Set-Field: Modify header | Transmitted   |
| VLAN ID, Priority          | Push/Pop VLAN            | Duration      |
| IPv4/IPv6 Src/Dst          | Decrement TTL            |               |
| TCP/UDP Src/Dst Port       | Drop                     |               |
| Metadata                   | Controller: Send to ctrl |               |
+----------------------------+--------------------------+---------------+

우선순위(Priority)에 따른 매칭:
1. 패킷 수신
2. 플로우 테이블 엔트리를 우선순위 순으로 검색
3. 첫 번째 매칭되는 엔트리의 액션 실행
4. 매칭되는 엔트리 없으면 Table-Miss → 컨트롤러로 Packet-In

================================================================================
[ NFV (Network Functions Virtualization) Architecture ]
================================================================================

+-----------------------------------------------------------------------------+
|                        OSS / BSS (운영 지원 시스템)                          |
+-----------------------------------------------------------------------------+
                                    |
+-----------------------------------------------------------------------------+
|                    MANO (Management and Orchestration)                      |
|  +-----------+  +-----------------------+  +-----------------------------+  |
|  |   NFVO    |  |        VNFM           |  |           VIM               |  |
|  | (Network  |  | (VNF Manager)         |  | (Virtualized Infrastructure |  |
|  | Function  |  |                       |  |         Manager)            |  |
|  | Orchestr. |  | VNF 라이프사이클 관리   |  | OpenStack, Kubernetes       |  |
|  +-----------+  +-----------------------+  +-----------------------------+  |
+-----------------------------------------------------------------------------+
                                    |
+-----------------------------------------------------------------------------+
|                    NFVI (NFV Infrastructure)                                |
|  +-----------------------------------------------------------------------+  |
|  |                  Virtual Network (가상 네트워크)                        |  |
|  |  +----------+  +----------+  +----------+  +----------+               |  |
|  |  |   vFW    |  |   vLB    |  |   vRouter|  |  vEPC    |               |  |
|  |  |  (VNF)   |  |  (VNF)   |  |  (VNF)   |  |  (VNF)   |  (VNF:       |  |
|  |  +----------+  +----------+  +----------+  +----------+   Virtual     |  |
|  |                                                           Network       |  |
|  |  +--------------------------------------------------------+ Function)  |  |
|  |  |           Virtualization Layer (Hypervisor/容器)      |            |  |
|  |  |           KVM, VMware ESXi, Docker, containerd        |            |  |
|  |  +--------------------------------------------------------+            |  |
|  |                                                                       |  |
|  |  +--------------------------------------------------------+            |  |
|  |  |           Hardware Resources (물리 자원)                |            |  |
|  |  |  Compute (x86/ARM) | Storage (SSD/HDD) | Network (NIC) |            |  |
|  |  +--------------------------------------------------------+            |  |
|  +-----------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------+

================================================================================
[ Service Function Chaining (SFC) ]
================================================================================

                     +------------------+
                     |   Classification |
                     |   (트래픽 분류)   |
                     +--------|---------+
                              |
                              v
    +--------+     +--------+     +--------+     +--------+     +--------+
    |  FW    |---->|  IDS   |---->|  LB    |---->|  NAT   |---->| Server |
    |(방화벽) |     |(침입탐지)|    |(로드밸런)|    |(NAT)   |     |(서버)   |
    +--------+     +--------+     +--------+     +--------+     +--------+
        |
        | Service Chain: FW → IDS → LB → NAT
        |
        | NSH (Network Service Header)로 경로 정보 캡슐화
        v

NSH 헤더 구조:
+----------------+----------------+----------------+----------------+
| Base Header    | Service Path   | Context Header | Original       |
| (4B)           | Header (4B)    | (가변)         | Packet         |
+----------------+----------------+----------------+----------------+
                 | SPI (Service   |
                 | Path ID)       |
                 | SI (Service    |
                 | Index)         |
                 +----------------+

================================================================================
```

### 심층 동작 원리: 핵심 메커니즘

#### 1. OpenFlow 프로토콜 동작

```python
"""
OpenFlow 메시지 타입 및 동작 시뮬레이션
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
import struct

class OFMessageType(Enum):
    """OpenFlow 메시지 타입"""
    HELLO = 0               # 연결 설정
    ECHO_REQUEST = 2        # 연결 유지 확인
    ECHO_REPLY = 3
    FEATURES_REQUEST = 5    # 스위치 기능 조회
    FEATURES_REPLY = 6
    PACKET_IN = 10          # 스위치 → 컨트롤러 (제어 불가 패킷)
    PACKET_OUT = 13         # 컨트롤러 → 스위치 (패킷 전송 지시)
    FLOW_MOD = 14           # 플로우 테이블 수정
    FLOW_REMOVED = 18       # 플로우 엔트리 삭제 알림

@dataclass
class FlowMatch:
    """플로우 매치 필드"""
    in_port: int = 0
    eth_src: str = "00:00:00:00:00:00"
    eth_dst: str = "00:00:00:00:00:00"
    eth_type: int = 0x0800  # IPv4
    ip_src: str = "0.0.0.0"
    ip_dst: str = "0.0.0.0"
    ip_proto: int = 0       # TCP=6, UDP=17
    tp_src: int = 0         # TCP/UDP 소스 포트
    tp_dst: int = 0         # TCP/UDP 목적지 포트

@dataclass
class FlowAction:
    """플로우 액션"""
    action_type: str  # OUTPUT, DROP, SET_FIELD, GROUP
    value: Any

@dataclass
class FlowEntry:
    """플로우 테이블 엔트리"""
    priority: int
    match: FlowMatch
    actions: List[FlowAction]
    idle_timeout: int = 0   # 초 단위 (0=무제한)
    hard_timeout: int = 0
    cookie: int = 0
    packet_count: int = 0
    byte_count: int = 0


class OpenFlowSwitch:
    """
    OpenFlow 스위치 시뮬레이터

    플로우 테이블 기반 패킷 처리
    """

    def __init__(self, dpid: int, n_ports: int = 4):
        self.dpid = dpid  # Data Path ID
        self.n_ports = n_ports
        self.flow_tables: List[FlowEntry] = []
        self.group_tables: Dict[int, List[FlowAction]] = {}
        self.controller = None
        self.packet_buffer = {}

    def connect_controller(self, controller):
        """컨트롤러 연결"""
        self.controller = controller
        # HELLO 메시지 교환
        controller.handle_hello(self)

    def receive_packet(self, in_port: int, packet: dict) -> Optional[dict]:
        """
        패킷 수신 및 처리

        Returns:
            처리 결과 (매칭된 액션 또는 None)
        """
        # 플로우 테이블 검색 (우선순위 순)
        for entry in sorted(self.flow_tables, key=lambda x: -x.priority):
            if self._match_packet(entry.match, in_port, packet):
                # 매칭 성공
                entry.packet_count += 1
                entry.byte_count += packet.get('size', 0)

                # 액션 실행
                return self._execute_actions(entry.actions, in_port, packet)

        # 매칭 실패 → 컨트롤러로 Packet-In
        if self.controller:
            self.controller.handle_packet_in(self, in_port, packet)

        return None

    def _match_packet(self, match: FlowMatch, in_port: int, packet: dict) -> bool:
        """패킷 매칭 검사"""
        if match.in_port and match.in_port != in_port:
            return False
        if match.eth_type and match.eth_type != packet.get('eth_type'):
            return False
        if match.ip_src != "0.0.0.0" and match.ip_src != packet.get('ip_src'):
            return False
        if match.ip_dst != "0.0.0.0" and match.ip_dst != packet.get('ip_dst'):
            return False
        if match.tp_dst and match.tp_dst != packet.get('tp_dst'):
            return False
        return True

    def _execute_actions(self, actions: List[FlowAction], in_port: int, packet: dict) -> dict:
        """액션 실행"""
        result = {'packet': packet, 'out_ports': []}

        for action in actions:
            if action.action_type == 'OUTPUT':
                if action.value == 'CONTROLLER':
                    # 컨트롤러로 전송
                    if self.controller:
                        self.controller.handle_packet_in(self, in_port, packet)
                elif action.value == 'FLOOD':
                    # 모든 포트로 플러딩 (입력 포트 제외)
                    result['out_ports'] = [p for p in range(1, self.n_ports + 1) if p != in_port]
                else:
                    result['out_ports'].append(action.value)

            elif action.action_type == 'DROP':
                result['out_ports'] = []
                break

            elif action.action_type == 'SET_FIELD':
                # 헤더 필드 수정
                field, value = action.value
                packet[field] = value

            elif action.action_type == 'GROUP':
                # 그룹 테이블 참조
                group_id = action.value
                if group_id in self.group_tables:
                    group_actions = self.group_tables[group_id]
                    self._execute_actions(group_actions, in_port, packet)

        return result

    def add_flow(self, entry: FlowEntry):
        """플로우 엔트리 추가 (FLOW_MOD)"""
        self.flow_tables.append(entry)
        self.flow_tables.sort(key=lambda x: -x.priority)  # 우선순위 정렬

    def remove_flow(self, cookie: int):
        """플로우 엔트리 삭제"""
        self.flow_tables = [e for e in self.flow_tables if e.cookie != cookie]


class SDNController:
    """
    SDN 컨트롤러 시뮬레이터

    네트워크 전역 상태 관리 및 플로우 프로그래밍
    """

    def __init__(self):
        self.switches: Dict[int, OpenFlowSwitch] = {}
        self.topology: Dict[int, List[tuple]] = {}  # 스위치 ID -> [(neighbor, port)]
        self.hosts: Dict[str, tuple] = {}  # MAC -> (switch_id, port)
        self.flow_rules_generated = []

    def handle_hello(self, switch: OpenFlowSwitch):
        """HELLO 메시지 처리"""
        print(f"[Controller] Switch {switch.dpid} connected")
        self.switches[switch.dpid] = switch
        # FEATURES_REQUEST 전송
        self._discover_switch_features(switch)

    def _discover_switch_features(self, switch: OpenFlowSwitch):
        """스위치 기능 발견"""
        # 실제로는 FEATURES_REQUEST/REPLY 교환
        print(f"[Controller] Discovered features of switch {switch.dpid}")

    def handle_packet_in(self, switch: OpenFlowSwitch, in_port: int, packet: dict):
        """Packet-In 처리 - 새로운 플로우 학습"""
        src_mac = packet.get('eth_src')
        dst_mac = packet.get('eth_dst')

        # 호스트 위치 학습
        if src_mac:
            self.hosts[src_mac] = (switch.dpid, in_port)
            print(f"[Controller] Learned host {src_mac} at switch {switch.dpid}:{in_port}")

        # 목적지가 알려진 경우 플로우 규칙 설치
        if dst_mac in self.hosts:
            dst_switch_id, dst_port = self.hosts[dst_mac]

            if dst_switch_id == switch.dpid:
                # 동일 스위치
                self._install_flow(switch, src_mac, dst_mac, dst_port)
            else:
                # 다른 스위치 - 경로 계산 필요
                path = self._compute_path(switch.dpid, dst_switch_id)
                if path:
                    self._install_path_flows(src_mac, dst_mac, path)
        else:
            # 알려지지 않은 목적지 - 플러딩
            flood_entry = FlowEntry(
                priority=100,
                match=FlowMatch(eth_dst=dst_mac),
                actions=[FlowAction('OUTPUT', 'FLOOD')]
            )
            switch.add_flow(flood_entry)

    def _install_flow(self, switch: OpenFlowSwitch, src_mac: str, dst_mac: str, out_port: int):
        """플로우 규칙 설치"""
        entry = FlowEntry(
            priority=1000,
            match=FlowMatch(eth_src=src_mac, eth_dst=dst_mac),
            actions=[FlowAction('OUTPUT', out_port)],
            idle_timeout=300
        )
        switch.add_flow(entry)
        self.flow_rules_generated.append(entry)
        print(f"[Controller] Installed flow: {src_mac} -> {dst_mac} via port {out_port}")

    def _compute_path(self, src_switch: int, dst_switch: int) -> List[int]:
        """최단 경로 계산 (BFS)"""
        if src_switch not in self.topology or dst_switch not in self.topology:
            return []

        from collections import deque

        visited = {src_switch}
        queue = deque([(src_switch, [src_switch])])

        while queue:
            current, path = queue.popleft()

            if current == dst_switch:
                return path

            for neighbor, _ in self.topology.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []

    def _install_path_flows(self, src_mac: str, dst_mac: str, path: List[int]):
        """경로를 따라 모든 스위치에 플로우 설치"""
        print(f"[Controller] Installing path {path} for {src_mac} -> {dst_mac}")
        # 각 스위치에 적절한 출력 포트로 플로우 설치
        for i, switch_id in enumerate(path):
            switch = self.switches.get(switch_id)
            if not switch:
                continue

            # 다음 홉 결정
            if i < len(path) - 1:
                next_switch = path[i + 1]
                # 토폴로지에서 연결 포트 찾기
                for neighbor, port in self.topology.get(switch_id, []):
                    if neighbor == next_switch:
                        self._install_flow(switch, src_mac, dst_mac, port)
                        break


# ================== 시뮬레이션 실행 ==================
if __name__ == "__main__":
    print("=" * 70)
    print("SDN/NFV Architecture Simulation Report")
    print("=" * 70)

    # 1. SDN 컨트롤러 및 스위치 생성
    print("\n[1. SDN Network Setup]")

    controller = SDNController()

    # 스위치 3개 생성 및 연결
    switch1 = OpenFlowSwitch(dpid=1, n_ports=4)
    switch2 = OpenFlowSwitch(dpid=2, n_ports=4)
    switch3 = OpenFlowSwitch(dpid=3, n_ports=4)

    for sw in [switch1, switch2, switch3]:
        sw.connect_controller(controller)

    # 토폴로지 구성
    controller.topology = {
        1: [(2, 2), (3, 3)],
        2: [(1, 1), (3, 3)],
        3: [(1, 1), (2, 2)]
    }

    # 2. 패킷 처리 시뮬레이션
    print("\n[2. Packet Processing Simulation]")

    # 첫 번째 패킷 (호스트 학습)
    packet1 = {
        'eth_src': 'AA:BB:CC:DD:EE:01',
        'eth_dst': 'AA:BB:CC:DD:EE:02',
        'eth_type': 0x0800,
        'ip_src': '192.168.1.10',
        'ip_dst': '192.168.1.20',
        'size': 1500
    }

    result = switch1.receive_packet(1, packet1)

    # 두 번째 패킷 (플로우 테이블 매칭)
    print("\n[3. Flow Table Match]")

    packet2 = packet1.copy()
    result = switch1.receive_packet(1, packet2)

    # 3. 통계 출력
    print("\n[4. Statistics]")

    print(f"Registered Switches: {len(controller.switches)}")
    print(f"Learned Hosts: {len(controller.hosts)}")
    print(f"Generated Flow Rules: {len(controller.flow_rules_generated)}")

    for entry in switch1.flow_tables[:3]:  # 상위 3개 규칙
        print(f"  Priority: {entry.priority}, Actions: {[a.action_type for a in entry.actions]}")

    print(f"\n{'='*70}")
