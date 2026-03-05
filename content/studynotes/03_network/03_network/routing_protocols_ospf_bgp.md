+++
title = "라우팅 프로토콜 (OSPF, BGP)"
date = 2024-05-18
description = "OSPF 링크 상태 프로토콜과 BGP 경로 벡터 프로토콜의 아키텍처, 동작 원리, 설정 방법 및 실무 적용 사례 심층 분석"
weight = 30
[taxonomies]
categories = ["studynotes-03_network"]
tags = ["OSPF", "BGP", "Routing", "IGP", "EGP", "NetworkLayer"]
+++

# 라우팅 프로토콜 (OSPF, BGP)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OSPF는 AS(Autonomous System) 내부에서 최단 경로를 계산하는 링크 상태(Link State) IGP로, Dijkstra SPF 알고리즘을 사용하여 계층적 Area 구조로 대규모 네트워크 확장성을 제공합니다.
> 2. **가치**: BGP는 인터넷의 백본을 구성하는 AS 간 라우팅을 담당하는 EGP로, 경로 벡터(Path Vector) 알고리즘과 다양한 속성(AS_PATH, LOCAL_PREF, MED)을 통해 정책 기반 라우팅을 가능하게 합니다.
> 3. **융합**: 현대 데이터센터와 클라우드 네트워크에서는 OSPF/IS-IS(언더레이) + BGP EVPN(오버레이) 결합 아키텍처가 표준으로 자리 잡았으며, SDN 컨트롤러와 연동하여 자동화된 라우팅 관리가 이루어집니다.

---

## Ⅰ. 개요 (Context & Background)

라우팅 프로토콜은 네트워크 계층(L3)의 핵심 기능으로, 패킷이 출발지에서 목적지까지 최적의 경로로 전달되도록 라우팅 테이블을 동적으로 구성합니다. OSPF와 BGP는 각각 IGP(Interior Gateway Protocol)와 EGP(Exterior Gateway Protocol)의 대표주자입니다.

**💡 비유**: 라우팅 프로토콜은 **'내비게이션 시스템'**과 같습니다.
- **OSPF**: 한 도시(AS) 내부의 상세 도로 지도를 모든 운전자(라우터)가 공유합니다. 각 도로의 상태(대역폭, 지연)를 교환하여 최단 경로를 계산합니다.
- **BGP**: 국가(AS) 간의 고속도로 네트워크를 관리합니다. 각 국가의 입구( Border Router)에서 이웃 국가들과 도달 가능한 목적지 정보를 교환합니다.

**등장 배경 및 발전 과정**:
1. **RIP의 한계**: 초기 라우팅 프로토콜인 RIP는 홉 카운트(최대 15)만을 메트릭으로 사용하고, 30초마다 전체 라우팅 테이블을 브로드캐스트하여 대규모 네트워크에 부적합했습니다.
2. **OSPF의 등장 (1998)**: IETF RFC 2328로 표준화된 OSPF는 링크 상태 정보를 교환하여 네트워크의 완전한 토폴로지를 파악하고, 대역폭 기반 비용으로 정교한 경로 선택이 가능합니다.
3. **BGP의 필요성**: 인터넷이 성장하면서 서로 다른 관리 영역(AS) 간의 라우팅이 필요해졌습니다. BGP는 정책 기반 라우팅과 루프 방지를 위해 경로 벡터 알고리즘을 채택했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: OSPF vs BGP 비교

| 비교 항목 | OSPF (Open Shortest Path First) | BGP (Border Gateway Protocol) |
|----------|--------------------------------|------------------------------|
| **분류** | IGP (Interior Gateway Protocol) | EGP (Exterior Gateway Protocol) |
| **알고리즘** | 링크 상태 (Link State) + Dijkstra SPF | 경로 벡터 (Path Vector) |
| **메트릭** | Cost (대역폭 기반: 10^8 / bandwidth) | 속성 조합 (AS_PATH, LOCAL_PREF 등) |
| **적용 범위** | 단일 AS 내부 | AS 간 (인터넷 백본) |
| **계층 구조** | Area (0, 1, 2, ...) | AS (1~65535, 4바이트 AS 지원) |
| **라우터 유형** | IR, ABR, ASBR, Backbone | iBGP, eBGP, Route Reflector |
| **통신 방식** | 멀티캐스트 (224.0.0.5, 224.0.0.6) | TCP 포트 179 (유니캐스트) |
| **수렴 속도** | 빠름 (초 단위) | 느림 (분~시간 단위) |
| **확장성** | 수천 대 라우터 | 10만+ 프리픽스 |
| **프로토콜 번호** | IP 프로토콜 89 | TCP 포트 179 |

### 정교한 구조 다이어그램: OSPF Area 아키텍처

```ascii
================================================================================
[ OSPF Hierarchical Area Architecture ]
================================================================================

                    +------------------------------------------+
                    |           AS 100 (Enterprise)            |
                    |                                          |
+-------------------+------------------+    +------------------+------------------+
|  Area 0 (Backbone)|                  |    |  Area 1 (Branch Office)            |
|  ================ |                  |    |  ==================                |
|                   |                  |    |                                    |
|  +-------------+  |    +----------+  |    |  +-------------+  +-------------+  |
|  |   Router A  |--+----|   ABR    |--+----+--|  Router D   |  |  Router E   |  |
|  | (Internal)  |  |    |(Area Bor-|  |    |  | (Internal)  |  | (Internal)  |  |
|  +-------------+  |    | der)     |  |    |  +-------------+  +-------------+  |
|                   |    +----------+  |    |                                    |
|  +-------------+  |         |        |    +------------------------------------+
|  |   Router B  |  |         |        |
|  | (Internal)  |  |         |        |    +----------------------------------+
|  +-------------+  |         |        |    |  Area 2 (Data Center)            |
|                   |         |        |    |  ==================              |
|  +-------------+  |    +----------+  |    |                                  |
|  |   Router C  |  |    |   ABR    |  |    |  +-------------+  +----------+   |
|  | (Internal)  |  |    |          |--+----+--|  Router F   |  | Server   |   |
|  +------+------+  |    +----------+  |    |  | (Internal)  |  | Farm     |   |
|         |         |                  |    |  +-------------+  +----------+   |
|         |         +------------------+    +----------------------------------+
|         |                                                              |
|  +------v------+                                                       |
|  |    ASBR     |<-------- External Routes (BGP, RIP, Static) ----------+
|  | (Autonomous |
|  |  System     |
|  |  Boundary)  |
|  +-------------+
|
+------------------------> Other AS (Internet)

================================================================================
[ OSPF Router Types ]
================================================================================

1. Internal Router (IR)
   - 모든 인터페이스가 동일 Area에 속함
   - Area 내부에서만 LSDB 유지

2. Area Border Router (ABR)
   - 여러 Area에 연결된 인터페이스 보유
   - Area 간 라우팅 요약(Summarization) 수행
   - Area 0에 반드시 연결되어야 함

3. Autonomous System Boundary Router (ASBR)
   - 외부 라우팅 도메인(BGP, RIP, Static)과 연결
   - 외부 경로를 OSPF로 재분배(Redistribution)

4. Backbone Router
   - Area 0에 연결된 라우터
   - 모든 ABR은 Backbone Router여야 함

================================================================================
[ OSPF LSA Types ]
================================================================================

| Type | Name              | Description                    | Scope      |
|------|-------------------|--------------------------------|------------|
| 1    | Router LSA        | 라우터의 링크 상태              | Area       |
| 2    | Network LSA       | DR이 생성, 멀티액세스 네트워크  | Area       |
| 3    | Summary LSA       | ABR이 생성, 네트워크 요약       | Area 간    |
| 4    | Summary ASBR LSA  | ASBR 위치 정보                 | Area 간    |
| 5    | AS External LSA   | ASBR이 생성, 외부 경로         | AS 전체    |
| 7    | NSSA External     | NSSA Area의 외부 경로          | NSSA Area  |

================================================================================
```

### 심층 동작 원리: OSPF 동작 메커니즘

#### 1. OSPF 인접성(Adjacency) 형성 과정

```
OSPF Neighbor State Machine:

1. Down State
   - 초기 상태, Hello 패킷 미수신

2. Init State
   - Hello 패킷 수신했으나, 자신의 Router ID 미포함

3. 2-Way State
   - 양방향 통신 확인 (Hello에 자신의 RID 포함)
   - DROther 간에는 여기서 종료

4. ExStart State
   - Master/Slave 선정, DB Description 시퀀스 번호 교환

5. Exchange State
   - Database Description (DBD) 패킷 교환
   - LSA 헤더 정보 전송

6. Loading State
   - Link State Request (LSR)로 필요한 LSA 요청
   - Link State Update (LSU)로 LSA 수신
   - Link State Acknowledgment (LSAck)로 확인

7. Full State
   - LSDB 동기화 완료, 인접성 형성 완료
```

#### 2. OSPF 비용(Cost) 계산

```
OSPF Cost 공식:
  Cost = Reference Bandwidth / Interface Bandwidth

기본 Reference Bandwidth: 100 Mbps (10^8 bps)

예시:
  FastEthernet (100 Mbps):  100 / 100 = 1
  GigabitEthernet (1 Gbps): 100 / 1000 = 0.1 → 1 (최소값)
  10Gigabit (10 Gbps):      100 / 10000 = 0.01 → 1

권장 설정 (고속 링크 대응):
  Router(config)# auto-cost reference-bandwidth 10000
  (10 Gbps를 Reference로 설정)

  10Gigabit: 10000 / 10000 = 1
  Gigabit:   10000 / 1000 = 10
  FastEthernet: 10000 / 100 = 100
```

#### 3. Dijkstra SPF 알고리즘

```python
import heapq
from typing import Dict, List, Tuple

def dijkstra_spf(graph: Dict[str, Dict[str, int]], source: str) -> Tuple[Dict[str, int], Dict[str, str]]:
    """
    Dijkstra 최단 경로 알고리즘 (OSPF SPF)

    Args:
        graph: {노드: {이웃노드: 비용}} 형태의 그래프
        source: 출발 노드 (SPF 트리의 루트)

    Returns:
        (최단 거리, 이전 홉)
    """
    # 초기화
    distances = {node: float('infinity') for node in graph}
    previous = {node: None for node in graph}
    distances[source] = 0

    # 우선순위 큐: (거리, 노드)
    pq = [(0, source)]
    visited = set()

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue
        visited.add(current_node)

        # 이웃 노드 탐색
        for neighbor, cost in graph[current_node].items():
            if neighbor in visited:
                continue

            new_dist = current_dist + cost

            # 더 짧은 경로 발견
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_node
                heapq.heappush(pq, (new_dist, neighbor))

    return distances, previous


# OSPF 네트워크 예시
ospf_network = {
    'Router_A': {'Router_B': 10, 'Router_C': 20},
    'Router_B': {'Router_A': 10, 'Router_C': 30, 'Router_D': 15},
    'Router_C': {'Router_A': 20, 'Router_B': 30, 'Router_D': 25},
    'Router_D': {'Router_B': 15, 'Router_C': 25}
}

# SPF 트리 계산 (Router_A가 루트)
distances, previous = dijkstra_spf(ospf_network, 'Router_A')

print("OSPF SPF Tree from Router_A:")
print(f"  To Router_B: Cost={distances['Router_B']}, NextHop={previous['Router_B']}")
print(f"  To Router_C: Cost={distances['Router_C']}, NextHop={previous['Router_C']}")
print(f"  To Router_D: Cost={distances['Router_D']}, NextHop={previous['Router_D']}")
```

### BGP 아키텍처 및 핵심 원리

```ascii
================================================================================
[ BGP Architecture - AS Interconnection ]
================================================================================

                    +------------------------------------------+
                    |              AS 100 (ISP-A)              |
                    |                                          |
                    |    +--------+       +--------+           |
                    |    |  RR-1  |<----->|  RR-2  |           |
                    |    |(Route  |       |(Route  |           |
                    |    |Reflector)      |Reflector)          |
                    |    +---|----+       +---|----+           |
                    |        |                |                |
                    |    +---|----+       +---|----+           |
+--------+    eBGP  |    | PE-1   |       | PE-2   |  eBGP    +--------+
| AS 200 |<-------->|    |(Edge)  |       |(Edge)  |<-------->| AS 300 |
|(ISP-B) |          |    +---|----+       +---|----+          |(ISP-C) |
+--------+          |        |                |               +--------+
                    |    +---|----+       +---|----+           |
                    |    | P-1    |<----->| P-2    |           |
                    |    |(Core)  |  iBGP |(Core)  |           |
                    |    +--------+       +--------+           |
                    |                                          |
                    +------------------------------------------+

================================================================================
[ BGP Path Attributes ]
================================================================================

| Attribute          | Type    | Description                              |
|--------------------|---------|------------------------------------------|
| ORIGIN             | Well-Known | 경로 출처 (IGP, EGP, Incomplete)      |
| AS_PATH            | Well-Known | 거쳐온 AS 번호 시퀀스 (루프 방지)     |
| NEXT_HOP           | Well-Known | 다음 홉 IP 주소                        |
| LOCAL_PREF         | Optional  | AS 내부 우선순위 (높을수록 우선)       |
| MED (MULTI_EXIT_   | Optional  | AS 진입点多중 선택 (낮을수록 우선)     |
|      DISC)         |           |                                         |
| COMMUNITY          | Optional  | 경로 분류 태그 (no-export 등)          |
| ATOMIC_AGGREGATE   | Optional  | 집약 경로 표시                         |

================================================================================
[ BGP Best Path Selection Algorithm ]
================================================================================

1. Weight (Cisco 전용, 높을수록 우선)
2. LOCAL_PREF (높을수록 우선)
3. 로컬 시작 (Local Origin)
4. AS_PATH (짧을수록 우선)
5. ORIGIN (IGP < EGP < Incomplete)
6. MED (낮을수록 우선)
7. eBGP > iBGP
8. NEXT_HOP까지의 IGP 비용 (낮을수록 우선)
9. 최적 경로 (Oldest Path)
10. 라우터 ID (낮을수록 우선)
11. 클러스터 리스트 길이 (짧을수록 우선)
12. 이웃 IP 주소 (낮을수록 우선)

================================================================================
```

### 핵심 코드: BGP 경로 선택 시뮬레이터 (Python)

```python
from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum

class OriginType(Enum):
    IGP = 0
    EGP = 1
    INCOMPLETE = 2

@dataclass
class BGPPath:
    """BGP 경로 속성"""
    prefix: str
    as_path: List[int]
    origin: OriginType
    local_pref: int = 100
    med: int = 0
    next_hop: str
    weight: int = 0
    is_ebgp: bool = True
    igp_cost: int = 0
    router_id: str
    neighbor_ip: str

    def __str__(self):
        return f"Path to {self.prefix} via ASes {self.as_path}"


class BGPBestPathSelector:
    """
    BGP Best Path Selection Algorithm 구현

    RFC 4271 기반 13단계 경로 선택 알고리즘
    """

    def __init__(self):
        self.paths: List[BGPPath] = []

    def add_path(self, path: BGPPath):
        """경로 추가"""
        self.paths.append(path)

    def select_best_path(self) -> Optional[BGPPath]:
        """
        BGP Best Path Selection Algorithm 실행

        Returns:
            선택된 최적 경로, 경로가 없으면 None
        """
        if not self.paths:
            return None

        candidates = self.paths.copy()

        # Step 1: Weight (Cisco 전용)
        max_weight = max(p.weight for p in candidates)
        candidates = [p for p in candidates if p.weight == max_weight]
        if len(candidates) == 1:
            return candidates[0]

        # Step 2: LOCAL_PREF (높을수록 우선)
        max_local_pref = max(p.local_pref for p in candidates)
        candidates = [p for p in candidates if p.local_pref == max_local_pref]
        if len(candidates) == 1:
            return candidates[0]

        # Step 3: Local Origin (로컬에서 생성된 경로 우선)
        # (간소화를 위해 생략)

        # Step 4: AS_PATH Length (짧을수록 우선)
        min_as_path_len = min(len(p.as_path) for p in candidates)
        candidates = [p for p in candidates if len(p.as_path) == min_as_path_len]
        if len(candidates) == 1:
            return candidates[0]

        # Step 5: ORIGIN (IGP < EGP < Incomplete)
        min_origin = min(p.origin.value for p in candidates)
        candidates = [p for p in candidates if p.origin.value == min_origin]
        if len(candidates) == 1:
            return candidates[0]

        # Step 6: MED (낮을수록 우선)
        min_med = min(p.med for p in candidates)
        candidates = [p for p in candidates if p.med == min_med]
        if len(candidates) == 1:
            return candidates[0]

        # Step 7: eBGP > iBGP
        ebgp_paths = [p for p in candidates if p.is_ebgp]
        if ebgp_paths:
            candidates = ebgp_paths
        if len(candidates) == 1:
            return candidates[0]

        # Step 8: IGP Cost to NEXT_HOP (낮을수록 우선)
        min_igp_cost = min(p.igp_cost for p in candidates)
        candidates = [p for p in candidates if p.igp_cost == min_igp_cost]
        if len(candidates) == 1:
            return candidates[0]

        # Step 9-12: Router ID, Cluster List, Neighbor IP (간소화)
        # Router ID가 가장 낮은 것 선택
        candidates.sort(key=lambda p: p.router_id)
        return candidates[0]


# ================== 시뮬레이션 실행 ==================
if __name__ == "__main__":
    print("=" * 70)
    print("BGP Best Path Selection Simulation")
    print("=" * 70)

    selector = BGPBestPathSelector()

    # 경로 1: eBGP를 통한 경로 (AS 200 -> 100)
    path1 = BGPPath(
        prefix="203.0.113.0/24",
        as_path=[200, 300, 400],
        origin=OriginType.IGP,
        local_pref=100,
        med=10,
        next_hop="192.0.2.1",
        weight=0,
        is_ebgp=True,
        igp_cost=5,
        router_id="1.1.1.1",
        neighbor_ip="192.0.2.1"
    )

    # 경로 2: iBGP를 통한 경로 (직접 연결)
    path2 = BGPPath(
        prefix="203.0.113.0/24",
        as_path=[200, 400],
        origin=OriginType.IGP,
        local_pref=200,  # 더 높은 LOCAL_PREF
        med=5,
        next_hop="198.51.100.1",
        weight=0,
        is_ebgp=False,
        igp_cost=3,
        router_id="2.2.2.2",
        neighbor_ip="198.51.100.1"
    )

    # 경로 3: 또 다른 eBGP 경로
    path3 = BGPPath(
        prefix="203.0.113.0/24",
        as_path=[200, 400],  # 동일 AS_PATH 길이
        origin=OriginType.IGP,
        local_pref=200,  # 경로 2와 동일
        med=5,
        next_hop="203.0.113.254",
        weight=100,  # 가장 높은 Weight
        is_ebgp=True,
        igp_cost=2,
        router_id="3.3.3.3",
        neighbor_ip="203.0.113.254"
    )

    selector.add_path(path1)
    selector.add_path(path2)
    selector.add_path(path3)

    best_path = selector.select_best_path()

    print(f"\nCandidate Paths for {path1.prefix}:")
    for i, path in enumerate(selector.paths, 1):
        print(f"\n  Path {i}:")
        print(f"    AS_PATH: {path.as_path}")
        print(f"    LOCAL_PREF: {path.local_pref}")
        print(f"    MED: {path.med}")
        print(f"    Weight: {path.weight}")
        print(f"    Type: {'eBGP' if path.is_ebgp else 'iBGP'}")

    print(f"\n{'='*70}")
    print(f"Selected Best Path:")
    if best_path:
        print(f"  Next Hop: {best_path.next_hop}")
        print(f"  AS_PATH: {best_path.as_path}")
        print(f"  Weight: {best_path.weight} (Step 1 winner)")
    print(f"{'='*70}")
