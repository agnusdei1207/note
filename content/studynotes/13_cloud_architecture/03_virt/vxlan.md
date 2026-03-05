+++
title = "VXLAN (Virtual eXtensible LAN)"
date = 2024-05-18
description = "기존 VLAN의 식별자 한계를 극복하기 위해 L2 프레임을 UDP로 캡슐화하여 수천만 개의 논리망 제공하는 오버레이 프로토콜"
weight = 59
[taxonomies]
categories = ["studynotes-13_cloud_architecture"]
tags = ["VXLAN", "Overlay", "L2 Extension", "VNI", "EVPN", "Data Center"]
+++

# VXLAN (Virtual eXtensible LAN)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: VXLAN(Virtual eXtensible LAN)은 L2 이더넷 프레임을 UDP 패킷으로 캡슐화하여 L3 IP 네트워크 위에서 전송함으로써, VLAN의 4096개 ID 한계를 1600만 개(24비트 VNI)로 확장하고 물리적 위치와 무관하게 L2 세그먼트를 확장하는 데이터센터 네트워크 가상화 프로토콜입니다.
> 2. **가치**: 대규모 멀티 테넌시(1600만 네트워크), VM 마이그레이션(vMotion) 시 IP 유지, 물리 네트워크 재구성 없는 유연성, 스파인-리프 아키텍처와의 호환성을 제공합니다.
> 3. **융합**: EVPN(Ethernet VPN) 컨트롤 플레인, NSX/ACI SDN, Kubernetes CNI, 하이브리드 클라우드 L2 확장과 결합하여 현대적 데이터센터의 표준 오버레이 기술로 자리잡았습니다.

---

## Ⅰ. 개요 (Context & Background)

VXLAN은 2011년 VMware, Cisco, Arista, Broadcom 등이 주도하여 RFC 7348로 표준화된 오버레이 네트워크 프로토콜입니다. 기존 VLAN의 12비트 ID(최대 4096개)는 대규모 클라우드 환경에서 테넌트 격리에 부족했으며, VXLAN은 24비트 VNI(VXLAN Network Identifier)로 16,777,216개 네트워크를 지원합니다. 또한 L3 네트워크 위에서 L2를 전송하므로 STP(Spanning Tree) 문제를 회피합니다.

**💡 비유**: VXLAN은 **'국제 택배 포장'**과 같습니다. 한국에서 미국으로 편지(VLAN 프레임)를 보낼 때, 편지에 국제 우표만 붙이면 배달됩니다. 하지만 VXLAN은 이 편지를 **'국제 택배 상자'**(UDP 패킷)에 넣어 보냅니다. 상자에는 목적지 국가(IP 주소)가 적혀 있고, 안에는 편지(원본 프레임)가 그대로 있습니다. 상자가 비행기(L3 네트워크)를 타고 미국에 도착하면, 편지를 꺼내 배달합니다. 편지는 자신이 상자에 담겼는지 모릅니다.

**등장 배경 및 발전 과정**:
1. **VLAN ID 고갈**: 4096개 VLAN은 대규모 클라우드에서 테넌트 수보다 적음.
2. **L2 도메인 확장**: vMotion을 위해 여러 랙에 걸친 L2 필요, STP는 이에 부적합.
3. **멀티 테넌시**: 각 테넌트에 독립 IP 주소 공간(10.0.0.0/8 등) 허용 필요.
4. **VXLAN RFC 7348 (2014)**: IETF에서 표준화.
5. **EVPN-VXLAN**: BGP EVPN(RFC 7432)과 결합하여 컨트롤 플레인 표준화.
6. **클라우드 네이티브**: Kubernetes, OpenStack에서 기본 오버레이로 채택.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### VXLAN 패킷 구조 (표)

| 필드 | 크기 | 설명 | 값/범위 |
|---|---|---|---|
| **Outer Ethernet Header** | 14 bytes | 물리 네트워크 이더넷 헤더 | Dst/Src MAC |
| **Outer IPv4 Header** | 20 bytes | VTEP 간 IP 통신 | Dst/Src VTEP IP |
| **Outer UDP Header** | 8 bytes | VXLAN 포트 | Dst Port: 4789 |
| **VXLAN Header** | 8 bytes | VNI 및 플래그 | VNI (24-bit) |
| **Inner Ethernet Header** | 14 bytes | 원본 VM 이더넷 헤더 | VM MAC 주소 |
| **Inner IP Header** | 20 bytes | 원본 VM IP 헤더 | VM IP 주소 |
| **Inner Payload** | 가변 | 원본 데이터 | 46~1500 bytes |
| **Total Overhead** | 50 bytes | VXLAN 추가 헤더 | - |

### VXLAN vs VLAN 비교 (표)

| 비교 항목 | VLAN | VXLAN |
|---|---|---|
| **ID 비트 수** | 12-bit | 24-bit |
| **최대 네트워크** | 4,096 | 16,777,216 |
| **전송 계층** | L2 (Ethernet) | L3 (UDP over IP) |
| **트렁크 프로토콜** | 802.1Q | UDP 캡슐화 |
| **스패닝 트리** | 필요 (STP) | 불필요 (L3 라우팅) |
| **멀티캐스트 필요** | 선택적 | BUM 트래픽 처리용 |
| **하드웨어 지원** | 모든 스위치 | VTEP 지원 필요 |

### 정교한 VXLAN 패킷 캡슐화 다이어그램

```ascii
+===========================================================================+
|                        VXLAN Packet Structure                             |
|                                                                           |
|  [Original L2 Frame (from VM)]                                           |
|  +-------------------------------------------------------------------+   |
|  | Inner Eth Dst | Inner Eth Src | EtherType | Inner IP |   Payload   |   |
|  |   (VM-B MAC)  |   (VM-A MAC)  |  (0x0800) |(10.1.1.x)|   (Data)    |   |
|  |   6 bytes     |   6 bytes     |  2 bytes  | 20+ bytes|  Variable   |   |
|  +-------------------------------------------------------------------+   |
|                                    |                                      |
|                                    v (Encapsulation)                     |
|                                                                           |
|  [VXLAN Encapsulated Packet]                                              |
|  +-------------------------------------------------------------------+   |
|  | Outer Eth | Outer IP | UDP Hdr | VXLAN Hdr | Original L2 Frame     |   |
|  +-------------------------------------------------------------------+   |
|       |          |          |          |             |                    |
|       v          v          v          v             v                    |
|  +--------+ +--------+ +--------+ +---------+ +-------------------+       |
|  |Dst MAC:| |Src IP: | |Src:rndm| |Flags:0x8| |Inner Eth + IP +   |       |
|  |Next Hop| |10.0.1.1| |Dst:4789| |VNI:5...| |   Payload         |       |
|  |8 bytes | |Dst IP: | |8 bytes  | |24-bit +| |   (Original)      |       |
|  |Src MAC:| |10.0.1.2| |         | |8 bytes | |                   |       |
|  |VTEP-A | |20+ b   | |         | |         | |                   |       |
|  |14 bytes| +--------+ +---------+ +---------+ +-------------------+       |
|  +--------+                                                            |
|                                                                           |
|  Total VXLAN Overhead: 50 bytes (Eth 14 + IP 20 + UDP 8 + VXLAN 8)      |
|                                                                           |
+===========================================================================+

[VXLAN Header Detail (8 bytes)]
+---------------------------------------------------------------------------+
| Bits  0-7  | Bits 8-15 | Bits 16-23 | Bits 24-31 | Bits 32-55 | Bits 56-63|
|   Flags    | Reserved  | Reserved   | Reserved   |    VNI     | Reserved  |
|   (0x08)   |   (0)     |    (0)     |    (0)     |  (24-bit)  |   (0)     |
+---------------------------------------------------------------------------+
| Flag bit 3 (I flag): VNI valid indicator                                 |
| VNI: VXLAN Network Identifier (24-bit, up to 16M networks)               |
+---------------------------------------------------------------------------+
```

### VXLAN 통신 시퀀스 다이어그램

```ascii
+-----------+     +-----------+     +-----------+     +-----------+
|   VM-A    |     |  VTEP-A   |     |  VTEP-B   |     |   VM-B    |
|10.1.1.10  |     | 10.0.1.1  |     | 10.0.1.2  |     |10.1.1.20  |
+-----------+     +-----------+     +-----------+     +-----------+
      |                 |                 |                 |
      | 1. ARP Request  |                 |                 |
      | (Who has 10.1.1.20?)              |                 |
      |---------------->|                 |                 |
      |                 | 2. MAC Lookup   |                 |
      |                 | (Check local DB)|                 |
      |                 |                 |                 |
      |                 | 3. If unknown,  |                 |
      |                 | send to Mcast   |                 |
      |                 | or Controller   |                 |
      |                 |---------------->|                 |
      |                 |                 | 4. Flood to     |
      |                 |                 | local VMs       |
      |                 |                 |---------------->|
      |                 |                 |                 |
      |                 |                 | 5. ARP Reply    |
      |                 |                 |<----------------|
      |                 | 6. Learn VM-B's |                 |
      |                 | MAC & VTEP-B    |                 |
      |                 |<----------------|                 |
      |                 |                 |                 |
      | 7. ARP Reply    |                 |                 |
      | (VM-B MAC)      |                 |                 |
      |<----------------|                 |                 |
      |                 |                 |                 |
      | 8. IP Packet    |                 |                 |
      | (Src:10.1.1.10, |                 |                 |
      |  Dst:10.1.1.20) |                 |                 |
      |---------------->|                 |                 |
      |                 | 9. VXLAN Encap  |                 |
      |                 | (VNI:50001)     |                 |
      |                 |---------------->|                 |
      |                 |                 | 10. Decap & Fwd |
      |                 |                 |---------------->|
      |                 |                 |                 |
      |                 |                 | 11. IP Packet   |
      |                 |                 |     received    |
      |                 |                 |                 |
```

### 핵심 코드: VXLAN VTEP 구성 (OVS + Linux)

```bash
#!/bin/bash
# VXLAN VTEP 구성 스크립트
# 호스트: VTEP-A (10.0.1.1), VNI: 50001

# 1. OVS 브리지 생성
ovs-vsctl add-br br-int

# 2. VXLAN 포트 생성 (EVPN 모드)
ovs-vsctl add-port br-int vxlan0 \
    -- set interface vxlan0 type=vxlan \
    options:remote_ip=flow \
    options:key=flow \
    options:dst_port=4789

# 3. OpenFlow 규칙 설정 (EVPN 스타일)
# 유니캐스트 트래픽: 학습된 MAC으로 직접 전송
ovs-ofctl add-flow br-int \
    "table=0,dl_dst=00:00:00:00:00:00/01:00:00:00:00:00,actions=output:vxlan0"

# 브로드캐스트/멀티캐스트: 모든 VTEP로 플러딩
ovs-ofctl add-flow br-int \
    "table=0,dl_dst=ff:ff:ff:ff:ff:ff,actions=output:vxlan0"

# 4. VTEP IP 설정 (언더레이)
ip addr add 10.0.1.1/24 dev eth0

# 5. VM 인터페이스 연결
ip tuntap add tap0 mode tap
ip link set tap0 up
ovs-vsctl add-port br-int tap0
```

```python
# Python: VXLAN 패킷 생성 및 분석
import socket
import struct
from scapy.all import Ether, IP, UDP, Raw, sendp

class VXLANProcessor:
    """VXLAN 캡슐화/역캡슐화 프로세서"""

    VXLAN_PORT = 4789
    VXLAN_HEADER_SIZE = 8

    @staticmethod
    def encapsulate(inner_frame: bytes, vni: int,
                    src_vtep_ip: str, dst_vtep_ip: str,
                    src_vtep_mac: str, dst_vtep_mac: str) -> bytes:
        """
        VXLAN 캡슐화
        """
        # VXLAN 헤더 (8 bytes)
        # Flags (1 byte) | Reserved (3 bytes) | VNI (3 bytes) | Reserved (1 byte)
        flags = 0x08  # I flag set
        vxlan_header = struct.pack('!B', flags) + b'\x00\x00\x00'
        vxlan_header += struct.pack('!I', vni << 8)  # VNI in upper 24 bits

        # UDP 헤더
        src_port = 12345  # 무작위 포트
        dst_port = VXLANProcessor.VXLAN_PORT
        udp_length = 8 + VXLANProcessor.VXLAN_HEADER_SIZE + len(inner_frame)
        udp_checksum = 0  # 선택적

        udp_header = struct.pack('!HHHH',
                                 src_port, dst_port,
                                 udp_length, udp_checksum)

        # 외부 IP 헤더 (간소화)
        outer_ip = IP(src=src_vtep_ip, dst=dst_vtep_ip,
                      proto=17,  # UDP
                      len=20 + len(udp_header) + 8 + len(inner_frame))

        # 외부 이더넷
        outer_eth = Ether(src=src_vtep_mac, dst=dst_vtep_mac)

        # 완전한 VXLAN 패킷
        vxlan_packet = outer_eth / outer_ip / UDP(
            sport=src_port, dport=VXLANProcessor.VXLAN_PORT
        ) / Raw(load=vxlan_header + inner_frame)

        return bytes(vxlan_packet)

    @staticmethod
    def decapsulate(vxlan_packet: bytes) -> tuple:
        """
        VXLAN 역캡슐화
        Returns: (vni, inner_frame)
        """
        # 이더넷 헤더 건너뛰기 (14 bytes)
        ip_start = 14

        # IP 헤더 길이 확인
        ip_header = vxlan_packet[ip_start:ip_start + 20]
        ip_header_length = (ip_header[0] & 0x0F) * 4

        # UDP 헤더 시작
        udp_start = ip_start + ip_header_length
        udp_header = vxlan_packet[udp_start:udp_start + 8]

        # VXLAN 헤더 시작
        vxlan_start = udp_start + 8
        vxlan_header = vxlan_packet[vxlan_start:vxlan_start + 8]

        # VNI 추출 (24-bit, bytes 4-6)
        vni = struct.unpack('!I', vxlan_header[0:4])[0] >> 8

        # 내부 프레임
        inner_frame = vxlan_packet[vxlan_start + 8:]

        return vni, inner_frame

# 사용 예시
if __name__ == "__main__":
    # 원본 이더넷 프레임 (VM 간)
    inner_frame = Ether(src="aa:bb:cc:00:00:01",
                       dst="aa:bb:cc:00:00:02") / \
                  IP(src="10.1.1.10", dst="10.1.1.20") / \
                  Raw(b"Hello VXLAN")

    # 캡슐화
    vxlan_packet = VXLANProcessor.encapsulate(
        inner_frame=bytes(inner_frame),
        vni=50001,
        src_vtep_ip="10.0.1.1",
        dst_vtep_ip="10.0.1.2",
        src_vtep_mac="00:11:22:33:44:55",
        dst_vtep_mac="66:77:88:99:aa:bb"
    )

    print(f"VXLAN Packet Size: {len(vxlan_packet)} bytes")
    print(f"Original Frame Size: {len(inner_frame)} bytes")
    print(f"Overhead: {len(vxlan_packet) - len(inner_frame)} bytes")

    # 역캡슐화
    vni, recovered_frame = VXLANProcessor.decapsulate(vxlan_packet)
    print(f"VNI: {vni}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### VXLAN 구현체 비교

| 구현체 | 유형 | 컨트롤 플레인 | 특징 | 적합 시나리오 |
|---|---|---|---|---|
| **VMware NSX-V** | 하이퍼바이저 | NSX Controller | vSphere 통합 | 프라이빗 클라우드 |
| **Cisco ACI** | 하드웨어+소프트웨어 | APIC | 하드웨어 VTEP | 대형 데이터센터 |
| **OVS + OVN** | 오픈소스 | OVN Controller | Linux 네이티브 | OpenStack, K8s |
| **Linux Bridge** | 오픈소스 | 커널 (FDB) | 단순, 경량 | 소규모, 테스트 |
| **Cumulus VX** | 네트워크 OS | FRR (BGP EVPN) | 화이트박스 스위치 | Spine-Leaf |

### 과목 융합 관점 분석

- **네트워크와의 융합**: VXLAN은 Spine-Leaf 아키텍처에서 ECMP(Equal-Cost Multi-Path) 로드밸런싱을 활용합니다. BGP EVPN이 컨트롤 플레인으로 MAC/IP 매핑을 분산합니다.

- **데이터베이스와의 융합**: 대규모 멀티 테넌트 환경에서 각 테넌트 DB 클러스터를 격리된 VXLAN 네트워크에 배치합니다. IP 충돌 없이 동일 대역 사용 가능.

- **보안과의 융합**: VNI가 다른 테넌트 간 통신은 원천 차단됩니다. 추가로 VXLAN 위에 IPsec 암호화 계층을 적용할 수 있습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 데이터센터 2지간 L2 확장**
- **요구사항**: 서울-부산 DC 간 vMotion, IP 유지
- **기술사의 의사결정**:
  1. DCI(Data Center Interconnect)로 VXLAN over WAN
  2. EVPN으로 컨트롤 플레인 통일
  3. 지연 <10ms 보장을 위한 전용선 사용
  4. **효과**: 재해 복구(DR) 시 VM 실시간 이동

**시나리오 2: Kubernetes 멀티 클러스터**
- **요구사항**: 3개 클러스터 간 Pod 통신, 동일 IP 대역
- **기술사의 의사결정**:
  1. Submariner 또는 Skupper로 멀티 클러스터 VXLAN
  2. 각 클러스터에 VNI 할당
  3. Global 시드 DNS로 서비스 디스커버리
  4. **효과**: 클러스터 간 투명한 Pod 통신

### 도입 시 고려사항

- [ ] MTU 설정: Jumbo Frame(9000) 사용, 50 bytes 오버헤드 고려
- [ ] BUM 트래픽: 멀티캐스트 or Head-End Replication 선택
- [ ] 하드웨어 오프로드: SmartNIC VTEP 오프로드 고려

### 안티패턴

1. **MTU 미조정**: 단편화로 인한 성능 저하
2. **멀티캐스트 과의존**: 대규모에서 플러딩 폭증
3. **VNI 낭비**: 불필요한 VNI 할당으로 관리 복잡성 증가

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대효과

| 구분 | VLAN | VXLAN | 개선 |
|---|---|---|---|
| **네트워크 수** | 4,096 | 16,777,216 | 4,000배 |
| **L2 도메인** | 랙 한정 | 데이터센터 전체 | 무제한 |
| **VM 이동성** | 제한 | 자유로움 | 운영 효율 |

### 미래 전망

1. **EVPN-VXLAN 표준화**: BGP EVPN이 VXLAN 컨트롤 플레인 표준으로 정착
2. **SRv6 오버레이**: Segment Routing으로 오버레이 단순화
3. **Hardware VTEP**: SmartNIC/DPU에서 VXLAN 오프로드

### ※ 참고 표준
- **RFC 7348**: Virtual eXtensible Local Area Network (VXLAN)
- **RFC 8365**: A Network Virtualization Overlay Solution Using EVPN
- **RFC 7432**: BGP MPLS-Based Ethernet VPN

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [오버레이 네트워크](@/studynotes/13_cloud_architecture/03_virt/overlay_network.md) : VXLAN의 상위 개념
- [언더레이 네트워크](@/studynotes/13_cloud_architecture/03_virt/underlay_network.md) : VXLAN의 기반
- [EVPN](@/studynotes/13_cloud_architecture/03_virt/evpn.md) : VXLAN 컨트롤 플레인
- [SDN](@/studynotes/13_cloud_architecture/03_virt/sdn.md) : VXLAN 제어
- [Spine-Leaf](@/studynotes/13_cloud_architecture/03_virt/spine_leaf.md) : VXLAN 언더레이 아키텍처

---

### 👶 어린이를 위한 3줄 비유 설명
1. VXLAN은 **'국제 택배 상자'**예요. 편지(데이터)를 상자에 넣어서 비행기(L3 네트워크)로 보내요.
2. 상자에는 **'목적지 주소'**(IP)가 적혀 있어서, 어디로 가야 할지 알 수 있어요.
3. 상자를 열면 **'편지가 그대로'** 나와요. 편지는 자신이 상자에 담겼는지 몰라요!
