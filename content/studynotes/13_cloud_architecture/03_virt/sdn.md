+++
title = "SDN (Software Defined Networking)"
date = 2024-05-15
description = "네트워크 제어 평면과 데이터 평면을 분리하여 소프트웨어로 네트워크를 프로그래밍 방식으로 관리하는 아키텍처"
weight = 81
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["SDN", "Software Defined Networking", "OpenFlow", "SD-WAN", "NFV", "Control Plane", "Data Plane"]
+++

# SDN (Software Defined Networking) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전통적인 네트워크 장비(라우터, 스위치)에 통합되어 있던 제어 평면(Control Plane, "어디로 보낼까?")과 데이터 평면(Data Plane, "패킷 전달")을 분리하고, 중앙 집중식 SDN 컨트롤러가 전체 네트워크를 소프트웨어로 프로그래밍하여 관리하는 네트워크 아키텍처 패러다임입니다.
> 2. **가치**: 네트워크 구성 변경 시간을 **수주에서 수분으로 단축**, **중앙 집중식 정책 관리**, **자동화된 트래픽 엔지니어링**, **네트워크 가상화**를 통해 클라우드 및 데이터센터 운영 효율을 획기적으로 향상시킵니다.
> 3. **융합**: OpenFlow 프로토콜, NFV(Network Function Virtualization), SD-WAN, 클라우드 네이티브 네트워킹(CNI), Intent-Based Networking과 결합하여 현대적 네트워크 인프라의 핵심 기술입니다.

---

## Ⅰ. 개요 (Context & Background)

SDN(Software Defined Networking)은 네트워크의 제어 기능을 데이터 전달 기능에서 분리하여, 네트워크 관리자가 추상화된 고수준 정책을 통해 네트워크를 프로그래밍 방식으로 제어할 수 있게 하는 아키텍처입니다.

**💡 비유**: SDN은 **'스마트 신호등 시스템'**과 같습니다. 전통적 신호등은 각 교차로마다 독립적으로 고정된 주기로 작동합니다. 반면 스마트 신호등 시스템은 중앙 통제 센터(SDN 컨트롤러)가 전체 도로 상황을 파악하고, 실시간 교통량에 따라 각 신호등(스위치)의 신호 주기를 소프트웨어로 제어합니다. "병원 앞은 항상 우선 통과", "출근 시간대에는 A도로 녹색 신호 연장" 같은 정책을 중앙에서 일괄 적용할 수 있습니다.

**등장 배경 및 발전 과정**:
1. **전통적 네트워크의 한계**: 각 네트워크 장비가 독립적으로 제어 로직을 포함하여, 전체 네트워크 정책 변경 시 모든 장비를 개별 설정해야 했습니다.
2. **Stanford Clean Slate 프로그램 (2006~)**: OpenFlow 프로토콜 개발, SDN 개념 정립.
3. **OpenFlow 1.0 (2009)**: 최초의 SDN 표준 프로토콜 발표.
4. **ONF (Open Networking Foundation, 2011)**: SDN 표준화 및 생태계 구축.
5. **클라우드/데이터센터 도입**: Google, Facebook, Amazon 등이 대규모 데이터센터에 SDN 도입.
6. **SD-WAN 대중화 (2015~)**: 기업 WAN에 SDN 개념 적용.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: SDN 아키텍처 3계층

| 계층 | 구성 요소 | 상세 역할 | 예시 | 비유 |
|---|---|---|---|---|
| **애플리케이션 계층** | SDN Applications | 네트워크 서비스, 정책 정의 | OpenStack Neutron, 수요 대역폭 | 교통 앱 |
| **제어 계층** | SDN Controller | 네트워크 상태 관리, 플로우 규칙 배포 | OpenDaylight, ONOS | 교통 관제 센터 |
| **인프라 계층** | SDN Datapath | 패킷 처리, 플로우 테이블 실행 | Open vSwitch, 물리 스위치 | 신호등 |

### 정교한 구조 다이어그램: SDN 아키텍처

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ SDN (Software Defined Networking) Architecture ]        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        Application Layer (Northbound API)                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │   Network   │  │   Firewall  │  │   Load      │  │   QoS       │       │
│  │  Management │  │   App       │  │   Balancer  │  │   Manager   │       │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │
│         │                │                │                │               │
│         └────────────────┴────────────────┴────────────────┘               │
│                                   │                                         │
│                          REST API / NB API                                 │
│                         (Northbound Interface)                             │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Control Layer (SDN Controller)                      │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                        SDN Controller                                 │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │  │
│  │  │   Network   │  │   Topology  │  │   Path      │  │   Policy    │ │  │
│  │  │   State     │  │   Manager   │  │   Compute   │  │   Engine    │ │  │
│  │  │   Manager   │  │             │  │             │  │             │ │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │  │
│  │                                                                       │  │
│  │  [ Network View ]                                                     │  │
│  │  ┌───────────────────────────────────────────────────────────────┐   │  │
│  │  │  Topology: Host1 ↔ Switch1 ↔ Switch2 ↔ Switch3 ↔ Host2       │   │  │
│  │  │  Links: S1-S2 (10Gbps), S2-S3 (10Gbps), S1-S3 (1Gbps backup) │   │  │
│  │  │  Flows: 1234 active flow entries                              │   │  │
│  │  │  Stats: Bandwidth, Latency, Packet Loss per link              │   │  │
│  │  └───────────────────────────────────────────────────────────────┘   │  │
│  │                                                                       │  │
│  │  대표 컨트롤러: OpenDaylight, ONOS, Floodlight, Ryu                  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                   │                                         │
│                          OpenFlow / Netconf                                 │
│                         (Southbound Interface)                             │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Infrastructure Layer (Data Plane)                   │
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │   SDN Switch 1  │  │   SDN Switch 2  │  │   SDN Switch 3  │             │
│  │  (Open vSwitch) │  │ (Physical SW)   │  │ (Physical SW)   │             │
│  │                 │  │                 │  │                 │             │
│  │ [Flow Table]    │  │ [Flow Table]    │  │ [Flow Table]    │             │
│  │ Match │ Action  │  │ Match │ Action  │  │ Match │ Action  │             │
│  │ ─────┼───────  │  │ ─────┼───────  │  │ ─────┼───────  │             │
│  │ *:*  │ Port:2  │  │ *:*  │ Port:3  │  │ *:*  │ Port:1  │             │
│  │ 10.1 │ Forward │  │ 10.2 │ Forward │  │ 10.3 │ Drop    │             │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘             │
│           │                    │                    │                       │
│           └────────────────────┼────────────────────┘                       │
│                                │                                            │
│                         [ Data Plane ]                                      │
│                    (패킷 처리, 포워딩, 드롭)                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


[ Traditional vs SDN Architecture ]

┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  [ Traditional Network ]             [ SDN Network ]                         │
│                                                                              │
│  각 장비가 독립적 제어               중앙 집중식 제어                        │
│                                                                              │
│  ┌─────────────┐                    ┌─────────────┐                         │
│  │   Router A  │                    │  Controller │                         │
│  │ ┌─────────┐ │                    │   (Brain)   │                         │
│  │ │Control  │ │                    └──────┬──────┘                         │
│  │ │Plane    │ │                           │                                │
│  │ ├─────────┤ │              ┌────────────┼────────────┐                  │
│  │ │Data     │ │              │            │            │                  │
│  │ │Plane    │ │              ▼            ▼            ▼                  │
│  │ └─────────┘ │           ┌──────┐   ┌──────┐   ┌──────┐                 │
│  └─────────────┘           │ SW 1 │   │ SW 2 │   │ SW 3 │                 │
│  ┌─────────────┐           │Data  │   │Data  │   │Data  │                 │
│  │   Router B  │           │Plane │   │Plane │   │Plane │                 │
│  │ ┌─────────┐ │           │ Only │   │ Only │   │ Only │                 │
│  │ │Control  │ │           └──────┘   └──────┘   └──────┘                 │
│  │ │Plane    │ │                                                           │
│  │ ├─────────┤ │          스위치는 패킷만 처리                              │
│  │ │Data     │ │          제어는 컨트롤러가 담당                            │
│  │ │Plane    │ │                                                           │
│  │ └─────────┘ │                                                           │
│  └─────────────┘                                                           │
│                                                                              │
│  문제: 장비 간 설정 불일치           장점: 일관된 정책 적용                  │
│        장애 원인 파악 어려움               중앙 집중식 모니터링              │
│        수동 설정 반복                       자동화 용이                      │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: OpenFlow 프로토콜

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    OpenFlow Protocol Flow                                   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ Flow Table Entry Structure ]                                            │
│                                                                            │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ Match Fields              │ Actions          │ Counters           │   │
│  ├────────────────────────────────────────────────────────────────────┤   │
│  │ Ingress Port: 1           │ Output: Port 2   │ Packets: 1,234     │   │
│  │ Eth Src: aa:bb:cc:11:22   │ Set VLAN: 100    │ Bytes: 98,765      │   │
│  │ Eth Dst: dd:ee:ff:33:44   │ Push MPLS        │ Duration: 120s     │   │
│  │ Eth Type: 0x0800 (IPv4)   │ Group: 1         │                     │   │
│  │ IP Src: 10.0.1.0/24       │ Drop             │                     │   │
│  │ IP Dst: 10.0.2.0/24       │ Controller       │                     │   │
│  │ IP Proto: 6 (TCP)         │                  │                     │   │
│  │ TCP Src: *                │                  │                     │   │
│  │ TCP Dst: 80               │                  │                     │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  [ Packet Processing Flow ]                                                │
│                                                                            │
│  Incoming Packet                                                          │
│       │                                                                    │
│       ▼                                                                    │
│  ┌─────────────┐                                                          │
│  │ Parse Header│  Extract: Ingress Port, MAC, IP, TCP/UDP, etc.          │
│  └──────┬──────┘                                                          │
│         │                                                                  │
│         ▼                                                                  │
│  ┌─────────────┐                                                          │
│  │ Flow Lookup │  Match against Flow Tables (Table 0 → Table N)          │
│  └──────┬──────┘                                                          │
│         │                                                                  │
│    ┌────┴────┐                                                            │
│    │         │                                                            │
│  Match    No Match                                                        │
│  Found    Found                                                           │
│    │         │                                                            │
│    ▼         ▼                                                            │
│ ┌──────┐  ┌────────────────┐                                              │
│ │Execute│  │ Table-miss    │                                              │
│ │Action │  │ Instruction   │                                              │
│ └──────┘  │                │                                              │
│    │      │ • Send to      │                                              │
│    │      │   Controller   │                                              │
│    │      │ • Drop         │                                              │
│    │      │ • Goto Next    │                                              │
│    │      │   Table        │                                              │
│    │      └────────────────┘                                              │
│    │                                                                       │
│    ▼                                                                       │
│  Output Port / Buffer                                                      │
│                                                                            │
│  [ Controller-Switch Communication ]                                       │
│                                                                            │
│  Controller                          Switch                                │
│     │                                  │                                   │
│     │──── Features Request ──────────►│                                   │
│     │◄─── Features Reply ─────────────│ (Switch capabilities)             │
│     │                                  │                                   │
│     │──── Flow Mod (Add Entry) ──────►│ (Push flow rule)                  │
│     │                                  │                                   │
│     │◄─── Packet-In ──────────────────│ (Unknown packet, ask controller)  │
│     │──── Packet-Out ────────────────►│ (Action for packet)               │
│     │                                  │                                   │
│     │◄─── Flow-Removed ───────────────│ (Flow entry timeout)              │
│     │◄─── Port-Status ────────────────│ (Link up/down)                    │
│     │                                  │                                   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: OpenFlow 컨트롤러 (Ryu)

```python
#!/usr/bin/env python3
"""
Ryu SDN Controller - Simple Layer 2 Switch
OpenFlow 기반 SDN 컨트롤러 구현
"""

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, arp
from ryu.lib import hub

class SimpleSwitch(app_manager.RyuApp):
    """
    간단한 L2 스위치 SDN 컨트롤러
    OpenFlow 1.3 프로토콜 사용
    """
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch, self).__init__(*args, **kwargs)
        self.mac_table = {}  # MAC -> Port 매핑 테이블
        self.datapaths = {}  # 연결된 스위치들

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """
        스위치 연결 시 호출
        초기 flow entry (table-miss) 설치
        """
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Table-miss 엔트리: 매칭되지 않는 패킷을 컨트롤러로 전송
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        self.logger.info(f"Switch connected: datapath_id={datapath.id}")

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        """
        스위치에 flow entry 추가
        """
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]

        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)

        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        """
        스위치에서 처리하지 못한 패킷 수신 시 호출
        MAC 학습 및 포워딩
        """
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # 포트 정보 추출
        in_port = msg.match['in_port']

        # 패킷 파싱
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        dst_mac = eth.dst
        src_mac = eth.src

        dpid = datapath.id
        self.mac_table.setdefault(dpid, {})

        self.logger.info(f"Packet in: dpid={dpid}, src={src_mac}, dst={dst_mac}, port={in_port}")

        # MAC 학습: Src MAC → In Port
        self.mac_table[dpid][src_mac] = in_port

        # 목적지 MAC이 알려진 경우
        if dst_mac in self.mac_table[dpid]:
            out_port = self.mac_table[dpid][dst_mac]
        else:
            # 알려지지 않은 경우: 플러딩
            out_port = ofproto.OFPP_FLOOD

        # 액션 정의
        actions = [parser.OFPActionOutput(out_port)]

        # 플러딩이 아닌 경우 flow entry 설치 (이후 패킷은 하드웨어 처리)
        if out_port != ofproto.OFPP_FLOOD:
            # 목적지 MAC 매칭 규칙
            match = parser.OFPMatch(eth_dst=dst_mac)
            self.add_flow(datapath, 1, match, actions)

        # 현재 패킷 처리
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, CONFIG_DISPATCHER])
    def state_change_handler(self, ev):
        """
        스위치 상태 변경 (연결/해제) 처리
        """
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            self.datapaths[datapath.id] = datapath
            self.logger.info(f"Switch registered: {datapath.id}")
        elif ev.state == CONFIG_DISPATCHER and datapath.id in self.datapaths:
            del self.datapaths[datapath.id]
            self.logger.info(f"Switch unregistered: {datapath.id}")


# 실행: ryu-manager simple_switch.py
```

### SDN-WAN 구성 (Cisco Viptela 스타일)

```yaml
# SD-WAN Configuration (Viptela/cEdge Style)

# 1. SD-WAN 컨트롤러 설정
system:
  system-ip: 10.0.0.1
  site-id: 100
  organization-name: "BrainScience Corp"
  vbond: "vbond.brainscience.com"

# 2. WAN 인터페이스 설정
vpn 0:
  interface ge0/0:
    ip-address: 203.0.113.10/24
    tunnel-interface:
      encapsulation: ipsec
      color: public-internet
      allow-service:
        - all
    bandwidth:
      upstream: 100  # Mbps
      downstream: 100

  interface ge0/1:
    ip-address: 198.51.100.10/24
    tunnel-interface:
      encapsulation: ipsec
      color: mpls
      allow-service:
        - all
    bandwidth:
      upstream: 50
      downstream: 50

# 3. 트래픽 정책 (애플리케이션 인식 라우팅)
policy:
  app-aware-routing:
    - name: "critical-apps-policy"
      sequence:
        - match:
            app-list: "critical-apps"  # VoIP, Video, ERP
          action:
            preferred-color: mpls
            backup-color: public-internet
            loss-limit: 1%
            latency-limit: 150ms

        - match:
            app-list: "bulk-transfer"  # Backup, File Sync
          action:
            preferred-color: public-internet
            backup-color: lte

  # 중앙 집중식 보안 정책
  security:
    - name: "zone-firewall"
      sequence:
        - match:
            source-zone: "vpn-10"
            destination-zone: "vpn-20"
          action:
            inspect: true
            log: true

# 4. VPN (VRF) 설정
vpn 10:
  name: "CORPORATE"
  interface ge0/2:
    ip-address: 10.10.0.1/24
    service:
      - dhcp-server
      - dns

vpn 20:
  name: "GUEST"
  interface ge0/3:
    ip-address: 10.20.0.1/24
    service:
      - dhcp-server
      - dns
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: SDN 구현 방식

| 비교 관점 | OpenFlow | Overlay (VXLAN) | Cisco ACI | VMware NSX |
|---|---|---|---|---|
| **접근 방식** | 프로토콜 기반 | 터널링 기반 | 하드웨어+소프트웨어 | 소프트웨어 기반 |
| **중앙 제어** | 강함 | 중간 | 강함 | 강함 |
| **하드웨어 의존** | 높음 | 낮음 | 높음 (Cisco) | 낮음 |
| **확장성** | 중간 | 높음 | 높음 | 높음 |
| **복잡성** | 높음 | 중간 | 높음 | 중간 |
| **주요 용도** | 데이터센터 | 클라우드 | 엔터프라이즈 | 가상화 |

### 과목 융합 관점 분석

**운영체제(OS)와의 융합**:
- **가상 스위치**: OVS(Open vSwitch)가 리눅스 커널 모듈로 동작
- **네트워크 네임스페이스**: 컨테이너 네트워킹의 기반

**네트워크와의 융합**:
- **BGP/OSPF와 SDN**: 기존 라우팅 프로토콜과의 통합
- **VXLAN/NVGRE**: 오버레이 네트워크 프로토콜

**보안과의 융합**:
- **마이크로 세그멘테이션**: SDN 기반 세밀한 접근 통제
- **서비스 체이닝**: 방화벽, IPS 등을 경유하는 트래픽 경로 제어

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 데이터센터 SDN 도입

**문제 상황**: 금융사 H사의 데이터센터는 1000대 이상의 서버를 운영하며, 네트워크 변경에 2주가 소요됩니다.

**기술사의 전략적 의사결정**:

1. **요구사항 분석**:
   - 네트워크 변경 시간: 2주 → 1시간
   - 자동화된 네트워크 프로비저닝
   - 멀티 테넌시 지원
   - 규정 준수 (감사 로그)

2. **솔루션 선정**:

   | 옵션 | 장점 | 단점 | 추천 |
   |---|---|---|---|
   | **Cisco ACI** | 하드웨어 성능, 엔터프라이즈 | 비용, 벤더 종속 | 대규모 |
   | **VMware NSX** | 가상화 친화적 | 성능 오버헤드 | 가상화 환경 |
   | **OpenDaylight** | 오픈소스 | 구축 난이도 | 비용 민감 |

3. **도입 전략**: **Cisco ACI** 채택
   - 이유: 기존 Cisco 장비 활용, 높은 성능, 규정 준수 용이

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - Controller SPOF**: SDN 컨트롤러가 단일 실패점이 되지 않도록 고가용성 구성 필수.

- **안티패턴 - Over-Engineering**: 모든 네트워크를 SDN화하려 하지 말고, 필요한 부분부터 단계적으로.

- **체크리스트**:
  - [ ] 컨트롤러 고가용성 구성
  - [ ] 기존 네트워크와의 통합 계획
  - [ ] 운영팀 교육
  - [ ] 롤백 계획
  - [ ] 모니터링 체계

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 전통적 네트워크 | SDN 도입 | 개선율 |
|---|---|---|---|
| **구성 변경 시간** | 2주 | 1시간 | 99% 단축 |
| **운영 비용** | 100% | 50% | 50% 절감 |
| **장애 복구 시간** | 4시간 | 30분 | 87% 단축 |
| **네트워크 활용률** | 40% | 80% | 100% 향상 |

### 미래 전망 및 진화 방향

- **Intent-Based Networking**: 자연어로 네트워크 정책 정의
- **AI 기반 자동 복구**: 장애 자동 탐지 및 복구
- **Segment Routing (SRv6)**: 프로그래밍 가능한 패킷 포워딩

### ※ 참고 표준/가이드
- **OpenFlow 1.5+**: ONF 표준 프로토콜
- **NETCONF/YANG**: IETF 네트워크 설정 표준
- **ETSI NFV**: 네트워크 기능 가상화 표준

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [가상화 (Virtualization)](@/studynotes/13_cloud_architecture/03_virt/virtualization.md) : SDN의 기반 기술
- [VPC](@/studynotes/13_cloud_architecture/03_virt/vpc.md) : 클라우드 네트워크 가상화
- [NFV](@/studynotes/13_cloud_architecture/03_virt/nfv.md) : 네트워크 기능 가상화
- [오버레이 네트워크](@/studynotes/10_network/_index.md) : VXLAN, NVGRE
- [SD-WAN](@/studynotes/10_network/_index.md) : WAN에 SDN 적용

---

### 👶 어린이를 위한 3줄 비유 설명
1. SDN은 **'스마트 신호등 시스템'**과 같아요. 전통적 신호등은 각자 따로 작동하지만, SDN은 중앙에서 모든 신호를 제어해요.
2. **'교통 관제 센터'(SDN 컨트롤러)**가 전체 도로 상황을 보고, 실시간으로 신호를 조정해요. "병원 앞은 항상 우선!" 같은 정책을 한 번에 적용할 수 있어요.
3. 덕분에 **'교통 체증이 줄어들어요'**. 네트워크에서도 데이터가 막히지 않고 빠르게 이동할 수 있어요!
