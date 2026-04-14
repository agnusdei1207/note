+++
title = "라우팅 및 스위칭 핵심 (Routing & Switching Core)"
weight = 1
description = "네트워크 트래픽 포워딩 메커니즘과 경로 설정 알고리즘 분석"
tags = ["Network", "Routing", "Switching", "OSPF", "BGP"]
+++

## 핵심 인사이트 (3줄 요약)
- **역할의 분리:** 스위칭(Switching)은 동일 네트워크 내에서 MAC 주소 기반의 고속 전송을 담당하고, 라우팅(Routing)은 이기종 네트워크 간 IP 주소 기반의 최적 경로 탐색을 수행.
- **동적 경로 설정:** 라우팅 알고리즘(Distance Vector, Link State)을 통해 네트워크 토폴로지 변화에 능동적으로 대응하며 신뢰성을 확보.
- **스위칭 고도화:** VLAN 기반 논리적 망분리와 STP(Spanning Tree Protocol)를 이용한 루프 방지로 안정적이고 유연한 L2 인프라 구축.

### Ⅰ. 개요 (Context & Background)
라우팅(Routing)과 스위칭(Switching)은 패킷 교환망에서 데이터를 출발지에서 목적지까지 정확하고 효율적으로 전달하기 위한 두 가지 핵심 메커니즘입니다. 스위칭은 OSI 2계층(Data Link Layer)에서 동작하며 로컬 영역(LAN) 내의 통신을 책임집니다. 반면, 라우팅은 OSI 3계층(Network Layer)에서 동작하며 서로 다른 네트워크(WAN 포함) 간의 경로를 설정하여 트래픽을 중계합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
스위치와 라우터의 트래픽 처리 과정은 Forwarding Table 구성 방식에 차이가 있습니다.

```text
+-------------------------------------------------------------+
|               Routing vs. Switching Mechanism               |
+-------------------------------------------------------------+
| [ L2 Switch ]                           [ L3 Router ]       |
|                                                             |
| +-----------------+               +-------------------+     |
| |  MAC Table      |               |  Routing Table    |     |
| | (CAM Table)     |               | (RIB/FIB)         |     |
| +-----------------+               +-------------------+     |
| | Port | MAC Addr |               | Dest Net | NextHop|     |
| |   1  | AA:BB:.. |               | 10.0/16  | 1.1.1.2|     |
| |   2  | CC:DD:.. |               | 20.0/16  | 1.1.1.3|     |
| +-----------------+               +-------------------+     |
|        |                                    |               |
| Frame Forwarding by MAC           Packet Routing by IP      |
+-------------------------------------------------------------+
```

1. **스위칭(Switching) 핵심 메커니즘:**
   - **Learning:** 수신 프레임의 Source MAC을 확인하여 MAC Table을 갱신.
   - **Flooding:** Destination MAC이 Table에 없거나 Broadcast 프레임일 경우 전체 포트로 전달.
   - **Forwarding/Filtering:** Destination MAC이 Table에 있으면 해당 포트로만 전송(Forwarding)하고, 수신 포트와 같으면 폐기(Filtering).
2. **라우팅(Routing) 핵심 알고리즘:**
   - **Distance Vector:** 이웃 라우터와 전체 라우팅 테이블을 교환하여 경로(Hop count) 계산 (예: RIP, EIGRP).
   - **Link State:** 토폴로지 정보를 전체 네트워크에 브로드캐스팅하여 최단 경로 트리를 구성(Dijkstra 알고리즘) (예: OSPF, IS-IS).
   - **Path Vector:** AS(Autonomous System) 간 정책 기반 경로 설정 (예: BGP).

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구분 (Category) | 스위칭 (Switching) | 라우팅 (Routing) |
|---|---|---|
| **동작 계층** | OSI 2계층 (데이터 링크) | OSI 3계층 (네트워크) |
| **기준 주소** | MAC Address (물리 주소) | IP Address (논리 주소) |
| **기본 장비** | L2 Switch | Router, L3 Switch |
| **주요 기능** | 동일 서브넷 내 프레임 전달, 루프 방지(STP) | 서브넷 간 통신, 최적 경로 설정, 패킷 필터링 |
| **확장성** | 로컬 도메인 (VLAN 단위) | 글로벌 인터넷 망 (AS 단위) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
엔터프라이즈 아키텍처에서 L3 스위치의 도입은 스위칭의 고속(Hardware-based) 처리 능력과 라우팅의 유연성을 융합한 대표적 사례입니다.
- **망 분리 및 보안:** 부서별 또는 서비스별로 VLAN을 구성하여 브로드캐스트 도메인을 분할하고, VLAN 간 통신은 라우터나 L3 스위치의 ACL(Access Control List)을 통해 철저히 통제해야 합니다.
- **고가용성 아키텍처:** L2 구간 루프 방지를 위해 RSTP(Rapid STP)나 VPC(Virtual PortChannel)를 적용하고, L3 구간 라우팅 이중화를 위해 VRRP/HSRP를 구성하여 무중단 서비스를 달성합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
클라우드 컴퓨팅과 5G 시대에서는 하드웨어 중심의 라우팅/스위칭이 SDN(Software-Defined Networking) 환경으로 진화하고 있습니다. 컨트롤 플레인(Control Plane)과 데이터 플레인(Data Plane)이 분리되어 중앙 집중적인 트래픽 제어가 가능해짐으로써, 네트워크 엔지니어는 더욱 민첩하고 프로그래밍 가능한 자동화된 네트워크 인프라를 구축할 수 있습니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **L2 기술:** VLAN(Virtual LAN), STP(Spanning Tree Protocol), ARP(Address Resolution Protocol)
- **L3 기술:** OSPF, BGP, 서브네팅(Subnetting), NAT(Network Address Translation)
- **차세대 기술:** SDN, VXLAN, SD-WAN

### 👶 어린이를 위한 3줄 비유 설명
1. **스위치**는 같은 아파트 단지 내에서 동과 호수(MAC 주소)를 보고 택배를 배달해 주는 경비실이에요.
2. **라우터**는 다른 도시로 물건을 보낼 때 어떤 고속도로(IP 주소와 경로)를 타야 가장 빠른지 알려주는 내비게이션이에요.
3. 둘이 힘을 합치면 아주 멀리 있는 친구에게도 가장 빠르고 정확하게 선물을 보낼 수 있답니다!