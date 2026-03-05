+++
title = "오버레이 네트워크 (Overlay Network)"
date = 2024-05-18
description = "언더레이 위에 논리적으로 얹혀진 가상 네트워크 터널로 VXLAN, NVGRE 프로토콜 활용하여 대규모 멀티테넌시 지원"
weight = 58
[taxonomies]
categories = ["studynotes-13_cloud_architecture"]
tags = ["Overlay Network", "VXLAN", "Underlay", "Tunneling", "SDN", "Network Virtualization"]
+++

# 오버레이 네트워크 (Overlay Network)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 오버레이 네트워크는 기존 물리 네트워크(Underlay) 위에 논리적인 가상 네트워크 계층을 터널링(VXLAN, NVGRE, GRE)으로 구축하여, 물리적 위치와 무관하게 VM/컨테이너를 동일 L2 도메인에 배치하고 IP 주소를 자율적으로 관리할 수 있는 네트워크 가상화 기술입니다.
> 2. **가치**: VLAN ID 제한(4096개)을 극복(1600만 개), 물리 네트워크 재구성 없이 워크로드 이동(VM Migration), 멀티 테넌시 격리, IP 주소 중복 사용, 클라우드 네이티브 네트워킹을 가능하게 합니다.
> 3. **융합**: SDN(Software Defined Networking), 컨테이너 네트워크(CNI), 서비스 메시(Istio), 하이브리드 클라우드 연결, 재해 복구(DR)와 결합하여 현대적 데이터센터 네트워크의 핵심 기반이 됩니다.

---

## Ⅰ. 개요 (Context & Background)

오버레이 네트워크(Overlay Network)는 물리 네트워크 인프라(Underlay)를 변경하지 않고, 그 위에 소프트웨어로 논리적 네트워크를 구축하는 기술입니다. 가상화와 컨테이너 환경에서 VM/Pod의 이동성, 확장성, 격리를 위해 필수적으로 사용됩니다. 대표적인 오버레이 프로토콜로 VXLAN(Virtual eXtensible LAN)이 있으며, 이는 VLAN의 12비트 ID(4096개) 한계를 24비트 VNID(1600만 개)로 확장합니다.

**💡 비유**: 오버레이 네트워크는 **'지하철 위에 떠다니는 고속 열차'**와 같습니다. 지하철(언더레이)은 이미 깔려 있는 선로를 사용하지만, 그 위를 나는 열차(오버레이)는 지하철과 무관하게 자신만의 경로와 목적지를 가집니다. 지하철이 어디로 가든, 떠다니는 열차는 자신의 승객(Pod/VM)을 원하는 목적지로 데려다줍니다. 지하철 노선도(물리 네트워크)를 바꿀 필요가 없습니다.

**등장 배경 및 발전 과정**:
1. **VLAN 한계**: 12비트 VLAN ID는 최대 4096개 네트워크만 생성 가능, 대규모 클라우드에서 부족.
2. **L2 스트레칭 문제**: 물리 스위치 STP(Spanning Tree)는 대규모 L2 도메인에서 수렴 시간 지연.
3. **VM 이동성 요구**: vMotion 등으로 VM이 호스트 간 이동 시 동일 서브넷 유지 필요.
4. **VXLAN 표준화 (2011)**: RFC 7348로 VXLAN 사양 정의.
5. **컨테이너 네이티브**: Kubernetes CNI(Calico, Flannel, Cilium)가 오버레이 기반.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 오버레이 네트워크 핵심 구성 요소 (표)

| 구성 요소 | 상세 역할 | 내부 동작 | 관련 기술 | 비유 |
|---|---|---|---|---|
| **VTEP (VXLAN Tunnel Endpoint)** | 오버레이 터널의 시작/끝점 | 캡슐화/역캡슐화, VNID 태깅 | OVS, Linux Bridge, NIC | 터널 입구/출구 |
| **Underlay Network** | 물리적 IP 네트워크 | L3 라우팅으로 VTEP 간 연결 | Spine-Leaf, BGP, ECMP | 지하철 선로 |
| **Overlay Network** | 논리적 L2 네트워크 | VM/Pod 간 L2 통신 제공 | VXLAN, NVGRE, GENEVE | 떠다니는 열차 |
| **VNID (VXLAN Network Identifier)** | 오버레이 네트워크 식별자 | 24비트 ID로 16M 네트워크 구분 | 24-bit ID | 열차 노선 번호 |
| **Controller** | 오버레이 제어 평면 | VTEP 간 MAC/IP 매핑 분배 | NSX Controller, OVN | 관제실 |

### 오버레이 프로토콜 비교 (표)

| 프로토콜 | 캡슐화 방식 | 헤더 크기 | 최대 네트워크 | 특징 | 지원 |
|---|---|---|---|---|---|
| **VXLAN** | UDP 캡슐화 | 50 bytes | 16M (24-bit VNI) | 가장 널리 사용 | 모든 벤더 |
| **NVGRE** | GRE 캡슐화 | 42 bytes | 16M (24-bit VSID) | Microsoft 주도 | Hyper-V |
| **GENEVE** | 유연한 캡슐화 | 가변 | 16M | 확장 가능한 헤더 | 최신 표준 |
| **GRE** | 범용 터널링 | 24 bytes | 4K (Key 필드) | 단순, 오래된 기술 | Cisco, Juniper |
| **IPIP** | IP-in-IP | 20 bytes | N/A | 오버헤드 최소 | Linux |

### 정교한 VXLAN 오버레이 아키텍처 다이어그램

```ascii
+===========================================================================+
|                        VXLAN Overlay Architecture                         |
|                                                                           |
|  [Overlay Layer - Logical L2 Network (VM Perspective)]                   |
|                                                                           |
|     VM-A (10.1.1.10)          VM-B (10.1.1.20)          VM-C (10.1.1.30)|
|     MAC: AA:BB:CC:00:01      MAC: AA:BB:CC:00:02       MAC: AA:BB:CC:00:03
|           |                         |                         |           |
|     +-----v-----+           +-------v-------+         +-------v-------+  |
|     | vSwitch   |           | vSwitch       |         | vSwitch       |  |
|     | (VTEP-A)  |           | (VTEP-B)      |         | (VTEP-C)      |  |
|     +-----------+           +---------------+         +---------------+  |
|           |                         |                         |           |
|     +-----v-------------------------v-------------------------v-------+  |
|     |              VXLAN Tunnel (Logical L2 over L3)                  |  |
|     |                    VNID: 50001                                  |  |
|     |    [Overlay Frame: Eth + IP + Payload + VXLAN Header]          |  |
|     +------------------------+----------------------------------------+  |
|                              |                                           |
+==============================|===========================================+
                               | Encapsulation/Decapsulation
+==============================v===========================================+
|  [Underlay Layer - Physical L3 Network]                                 |
|                                                                          |
|     +---------------+          +---------------+         +---------------+
|     |  Host-1       |          |  Host-2       |         |  Host-3       |
|     |  IP: 10.0.1.1 |          |  IP: 10.0.1.2 |         |  IP: 10.0.1.3 |
|     +-------+-------+          +-------+-------+         +-------+-------+
|             |                          |                         |        |
|     +-------v-------+          +-------v-------+         +-------v-------+
|     |  Leaf Switch  |          |  Leaf Switch  |         |  Leaf Switch  |
|     +-------+-------+          +-------+-------+         +-------+-------+
|             |                          |                         |        |
|     +-------v--------------------------v-------------------------v-------+
|     |                    Spine Switch (L3 Routing)                      |
|     |                    BGP/ECMP for Load Balancing                    |
|     +-------------------------------------------------------------------+
|                                                                          |
+==========================================================================+

[VXLAN Packet Encapsulation]
+--------------------------------------------------------------------------+
| Original Frame (VM to VM)                                               |
| +--------+--------+--------+--------+                                   |
| | Dst MAC| Src MAC| EType  | Payload|                                   |
| |(VM-B)  |(VM-A)  |(0x0800)| (IP)   |                                   |
| +--------+--------+--------+--------+                                   |
|                         |                                                |
|                         v (Encapsulation at VTEP-A)                      |
| +--------------------------------------------------------------------+  |
| | Outer Eth | Outer IP  | UDP   | VXLAN  | Original Frame           |  |
| | Dst: VTEP | Src: 10.0 | Dst:  | VNID:  | (VM-A to VM-B)           |  |
| |     B MAC |   .1.1    | 4789  | 50001  |                          |  |
| +--------------------------------------------------------------------+  |
|                         |                                                |
|                         v (Transmit via Underlay L3)                    |
|                    [Physical Network]                                   |
|                         |                                                |
|                         v (Decapsulation at VTEP-B)                     |
| +--------+--------+--------+--------+                                   |
| | Dst MAC| Src MAC| EType  | Payload|  -> Delivered to VM-B          |
| |(VM-B)  |(VM-A)  |(0x0800)| (IP)   |                                   |
| +--------+--------+--------+--------+                                   |
+--------------------------------------------------------------------------+
```

### 심층 동작 원리: VXLAN 캡슐화/역캡슐화

1. **VM 송신 (VM Transmission)**:
   - VM-A가 VM-B의 IP(10.1.1.20)로 패킷 송신
   - VM은 이를 동일 L2 네트워크로 인식

2. **ARP 해결 (ARP Resolution)**:
   - VM-A가 ARP Request 브로드캐스트
   - VTEP-A가 ARP를 가로채어 컨트롤러에 VM-B의 MAC/MAC 조회
   - 컨트롤러가 VM-B가 VTEP-B(10.0.1.2)에 있음을 응답
   - VTEP-A가 VM-B의 MAC으로 ARP Reply 생성

3. **캡슐화 (Encapsulation)**:
   - VTEP-A가 원본 이더넷 프레임에 VXLAN 헤더 추가
   - UDP 헤더 (Dst Port: 4789, Src Port: Flow Hash)
   - 외부 IP 헤더 (Src: 10.0.1.1, Dst: 10.0.1.2)
   - 외부 이더넷 헤더 (물리 스위치 MAC)

4. **언더레이 전송 (Underlay Transmission)**:
   - 캡슐화된 패킷이 L3 네트워크를 통해 라우팅
   - Spine-Leaf 스위치가 ECMP로 로드밸런싱

5. **역캡슐화 (Decapsulation)**:
   - VTEP-B가 UDP 4789 포트 패킷 수신
   - VXLAN 헤더 제거, VNID(50001) 확인
   - 원본 프레임을 해당 VNID의 브리지로 전송
   - VM-B가 패킷 수신

### 핵심 코드: Linux VXLAN 구성

```bash
# Linux VXLAN VTEP 구성 스크립트

# 1. VXLAN 인터페이스 생성
ip link add vxlan0 type vxlan \
    id 50001 \                    # VNID
    dstport 4789 \                # UDP 포트 (IANA 표준)
    local 10.0.1.1 \              # 로컬 VTEP IP
    group 239.1.1.1 \             # 멀티캐스트 그룹 (또는 remote)
    dev eth0                      # 언더레이 인터페이스

# 2. 브리지 생성 및 VXLAN 연결
ip link add br-vxlan type bridge
ip link set vxlan0 master br-vxlan
ip link set vxlan0 up
ip link set br-vxlan up

# 3. VM/TAP 인터페이스 연결
ip link set tap0 master br-vxlan
ip link set tap0 up

# 4. 브리지에 IP 할당 (필요 시)
ip addr add 10.1.1.1/24 dev br-vxlan
```

```python
# Python: VXLAN 패킷 생성 및 분석 (Scapy)
from scapy.all import *

def create_vxlan_packet(src_vm_ip, dst_vm_ip, src_vm_mac, dst_vm_mac,
                        src_vtep_ip, dst_vtep_ip, vni):
    """
    VXLAN 캡슐화 패킷 생성
    """
    # 내부 프레임 (VM 간 통신)
    inner_eth = Ether(src=src_vm_mac, dst=dst_vm_mac)
    inner_ip = IP(src=src_vm_ip, dst=dst_vm_ip)
    inner_tcp = TCP(sport=12345, dport=80)
    inner_payload = Raw(b"Hello from VM-A")

    inner_frame = inner_eth / inner_ip / inner_tcp / inner_payload

    # VXLAN 캡슐화
    vxlan_header = VXLAN(vni=vni, flags=0x8)  # I flag set

    # 외부 UDP (VXLAN 포트: 4789)
    outer_udp = UDP(sport=12345, dport=4789)

    # 외부 IP (VTEP 간 통신)
    outer_ip = IP(src=src_vtep_ip, dst=dst_vtep_ip)

    # 외부 이더넷
    outer_eth = Ether(src="00:11:22:33:44:55", dst="66:77:88:99:aa:bb")

    # 완전한 VXLAN 패킷
    vxlan_packet = outer_eth / outer_ip / outer_udp / vxlan_header / inner_frame

    return vxlan_packet

def parse_vxlan_packet(packet):
    """
    VXLAN 패킷 분석
    """
    if packet.haslayer(VXLAN):
        vni = packet[VXLAN].vni
        print(f"VNID: {vni}")

        # 내부 프레임 추출
        inner = packet[VXLAN].payload
        if inner.haslayer(IP):
            print(f"Inner Src IP: {inner[IP].src}")
            print(f"Inner Dst IP: {inner[IP].dst}")
        if inner.haslayer(Ether):
            print(f"Inner Src MAC: {inner[Ether].src}")
            print(f"Inner Dst MAC: {inner[Ether].dst}")

# 사용 예시
if __name__ == "__main__":
    packet = create_vxlan_packet(
        src_vm_ip="10.1.1.10",
        dst_vm_ip="10.1.1.20",
        src_vm_mac="aa:bb:cc:00:00:01",
        dst_vm_mac="aa:bb:cc:00:00:02",
        src_vtep_ip="10.0.1.1",
        dst_vtep_ip="10.0.1.2",
        vni=50001
    )

    print("VXLAN Packet Created:")
    packet.show()

    print("\nParsing:")
    parse_vxlan_packet(packet)
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 오버레이 vs 언더레이 네트워크 비교

| 비교 항목 | Underlay Network | Overlay Network |
|---|---|---|
| **목적** | 물리적 연결성 | 논리적 연결성 |
| **주소 체계** | 물리 IP (관리자 할당) | 가상 IP (테넌트 자율) |
| **프로토콜** | IP, BGP, OSPF | VXLAN, GRE, GENEVE |
| **장비** | 물리 스위치, 라우터 | vSwitch, VTEP |
| **확장성** | 제한적 (VLAN 4K) | 높음 (VNID 16M) |
| **이동성** | 제한적 | 자유로움 (VM Migration) |
| **복잡성** | 낮음 | 높음 (캡슐화 오버헤드) |

### 과목 융합 관점 분석

- **네트워크와의 융합**: 오버레이는 언더레이 L3 네트워크 위에 L2 가상화를 제공합니다. Spine-Leaf 아키텍처, ECMP, BGP EVPN과 결합하여 고가용성과 로드밸런싱을 실현합니다.

- **보안과의 융합**: 오버레이 네트워크 자체가 테넌트 격리를 제공합니다. VNID가 다른 VM 간 통신은 물리적으로 차단됩니다. 추가로 IPsec 암호화로 데이터 보호 가능.

- **컨테이너와의 융합**: Kubernetes CNI가 오버레이 기반 네트워크를 제공합니다. Flannel(VXLAN), Calico(IPIP), Cilium(VXLAN/Geneve)이 대표적입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 멀티 테넌트 프라이빗 클라우드**
- **요구사항**: 500개 테넌트, 각 테넌트 독립 네트워크, IP 중복 허용
- **기술사의 의사결정**:
  1. VMware NSX 또는 OpenStack Neutron + OVS
  2. VXLAN으로 각 테넌트에 VNID 할당
  3. 테넌트는 10.0.0.0/8 자유 사용 가능
  4. **효과**: VLAN 한계 극복, 완전한 테넌트 격리

**시나리오 2: Kubernetes 클러스터 네트워킹**
- **요구사항**: 1000개 Pod, 동적 스케일링, 서비스 디스커버리
- **기술사의 의사결정**:
  1. Calico 또는 Cilium CNI
  2. VXLAN 오버레이로 Pod 네트워크 구성
  3. Network Policy로 마이크로 세그멘테이션
  4. **효과**: Pod IP 자동 할당, 이동성 확보

### 도입 시 고려사항

- [ ] MTU 크기: 오버레이 헤더(50 bytes) 고려하여 MTU 조정 (9000 -> 8950)
- [ ] CPU 오버헤드: 캡슐화/역캡슐화 CPU 소모. Hardware Offload 고려.
- [ ] 멀티캐스트 vs 유니캐스트: 대규모는 EVPN+BGP 유니캐스트 권장.

### 안티패턴

1. **MTU 미조정**: 오버레이 헤더로 인한 단편화 발생, 성능 저하.
2. **과도한 오버레이 계층**: 이중/삼중 오버레이는 피해야 함.
3. **컨트롤러 SPOF**: 분산 컨트롤러로 고가용성 확보 필수.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대효과

| 구분 | VLAN Only | VXLAN Overlay | 개선 |
|---|---|---|---|
| **네트워크 수** | 4,096 | 16,777,216 | 4000배 증가 |
| **IP 주소 관리** | 중앙 집중 | 테넌트 자율 | 유연성 향상 |
| **VM 이동성** | 제한적 | 자유로움 | 운영 효율 |
| **배포 시간** | 일~주 | 분~시간 | 99% 단축 |

### 미래 전망

1. **EVPN-VXLAN**: BGP EVPN으로 컨트롤 플레인 표준화
2. **SRv6**: Segment Routing over IPv6로 오버레이 단순화
3. **Hardware Offload**: SmartNIC/DPU로 VXLAN 오프로드

### ※ 참고 표준
- **RFC 7348**: Virtual eXtensible Local Area Network (VXLAN)
- **RFC 8365**: BGP EVPN for VXLAN
- **RFC 8926**: Geneve Encapsulation

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [SDN](@/studynotes/13_cloud_architecture/03_virt/sdn.md) : 오버레이 제어 기반
- [VXLAN](@/studynotes/13_cloud_architecture/03_virt/vxlan.md) : 대표적 오버레이 프로토콜
- [언더레이 네트워크](@/studynotes/13_cloud_architecture/03_virt/underlay_network.md) : 물리적 기반 네트워크
- [CNI](@/studynotes/13_cloud_architecture/01_native/cni.md) : 컨테이너 네트워크 인터페이스
- [마이크로 세그멘테이션](@/studynotes/13_cloud_architecture/03_virt/micro_segmentation.md) : 오버레이 보안 적용

---

### 👶 어린이를 위한 3줄 비유 설명
1. 오버레이 네트워크는 **'지하철 위를 나는 열차'**예요. 지하철 선로(물리 네트워크) 위를 자유롭게 날아요.
2. 지하철이 어디로 가든 상관없이, **'나는 열차'**는 자신만의 목적지로 가요.
3. 그래서 **'새로운 선로를 깔지 않아도'** 많은 사람을 서로 다른 곳으로 데려다줄 수 있어요!
