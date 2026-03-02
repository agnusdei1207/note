+++
title = "라우팅 (Routing)"
date = 2025-03-01

[extra]
categories = "pe_exam-network"
+++

# 라우팅 (Routing)

## 핵심 인사이트 (3줄 요약)
> **출발지에서 목적지까지 패킷의 최적 경로를 결정하고 전달하는 과정**. 정적(수동)과 동적(프로토콜 기반)으로 구분. 거리벡터·링크상태·경로벡터 알고리즘이 핵심이다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 라우팅(Routing)은 **네트워크에서 패킷이 출발지에서 목적지까지 도달하기 위한 최적 경로를 결정**하고, 라우팅 테이블을 기반으로 해당 경로로 패킷을 전달하는 Layer 3(네트워크 계층)의 핵심 기능이다.

> 💡 **비유**: 라우팅은 **"네비게이션 시스템"** 같아요. 출발지에서 목적지까지 가장 빠르거나 효율적인 경로를 찾아주죠. 도로 상황(네트워크 상태)에 따라 우회 경로를 추천하기도 하고, 고속도로(고대역폭 링크)를 우선 선택하기도 해요!

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 네트워크 확장성**: 단일 브로드캐스트 도메인은 호스트 수 증가 시 충돌·브로드캐스트 스톰으로 마비
2. **기술적 필요성 - 경로 최적화**: 복잡한 인터네트워크에서 최적 경로 산출 알고리즘 필요
3. **시장/산업 요구 - 인터넷 연결**: 수십억 개의 네트워크를 상호 연결하는 글로벌 인프라 구축

**핵심 목적**: **네트워크 간 연결성 제공, 최적 경로 선택, 트래픽 효율화, 장애 시 우회**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**라우팅 테이블 구조** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        라우팅 테이블 (Routing Table)                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌───────────────────────────────────────────────────────────────────┐ │
│   │ 목적지 네트워크 │  서브넷마스크  │  다음 홉(NH)  │ 인터페이스 │ AD │ │
│   ├───────────────────────────────────────────────────────────────────┤ │
│   │  10.0.1.0      │ 255.255.255.0  │  직접 연결    │   eth0     │ 0  │ │
│   │  10.0.2.0      │ 255.255.255.0  │  10.0.1.1     │   eth0     │ 1  │ │
│   │  192.168.1.0   │ 255.255.255.0  │  10.0.1.254   │   eth0     │110 │ │
│   │  0.0.0.0       │ 0.0.0.0        │  10.0.1.254   │   eth0     │ 1  │ │
│   └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│   용어 설명:                                                            │
│   - 목적지 네트워크: 패킷이 향할 최종 네트워크 주소                       │
│   - 서브넷 마스크: 목적지 네트워크 식별용 비트 마스크                     │
│   - 다음 홉(Next Hop): 패킷이 전달될 다음 라우터의 IP                    │
│   - 인터페이스: 패킷이 나갈 로컬 포트                                    │
│   - AD(Administrative Distance): 경로 신뢰도 (낮을수록 우선)             │
│                                                                         │
│   AD 값 예시:                                                           │
│   - 직접 연결: 0                                                        │
│   - 정적 라우팅: 1                                                      │
│   - eBGP: 20                                                            │
│   - OSPF: 110                                                           │
│   - RIP: 120                                                            │
│   - iBGP: 200                                                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**라우팅 분류** (필수: 표):
| 분류 | 정적 라우팅 (Static) | 동적 라우팅 (Dynamic) |
|------|---------------------|----------------------|
| **설정 방식** | 관리자 수동 입력 | 프로토콜 자동 계산 |
| **경로 변경** | 수동 (재설정 필요) | 자동 (장애 감지 시) |
| **리소스 사용** | CPU/메모리 거의 없음 | CPU/메모리/대역폭 사용 |
| **확장성** | 소규모에 적합 | 대규모에 적합 |
| **복잡도** | 단순 | 복잡 (프로토콜 이해 필요) |
| **예측성** | 높음 (고정 경로) | 낮음 (상황에 따라 변화) |
| **사용 사례** | 스텁 네트워크, 기본 경로 | 엔터프라이즈, 인터넷 |

**라우팅 알고리즘 비교** (필수: 상세):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    라우팅 알고리즘 분류                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. 거리 벡터 (Distance Vector)                                         │
│     ┌───────────────────────────────────────────────────────────────┐  │
│     │ 핵심 개념: 인접 라우터와 거리 정보 교환                         │  │
│     │ 알고리즘: 벨만-포드 (Bellman-Ford)                             │  │
│     │ 메트릭: 홉 수 (Hop Count)                                      │  │
│     │ 프로토콜: RIP, IGRP                                            │  │
│     │                                                                 │  │
│     │ 장점: 구현 단순, 메모리 적음                                    │  │
│     │ 단점: 느린 수렴, 루프 가능성 (Count-to-Infinity)               │  │
│     │                                                                 │  │
│     │ 동작 예시:                                                      │  │
│     │   A ──1── B ──1── C                                            │  │
│     │                                                                 │  │
│     │   A의 거리 벡터: {B:1, C:2}                                    │  │
│     │   B의 거리 벡터: {A:1, C:1}                                    │  │
│     │   C의 거리 벡터: {A:2, B:1}                                    │  │
│     └───────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  2. 링크 상태 (Link State)                                              │
│     ┌───────────────────────────────────────────────────────────────┐  │
│     │ 핵심 개념: 전체 네트워크 토폴로지 파악 후 SPF 계산              │  │
│     │ 알고리즘: 다익스트라 (Dijkstra's Shortest Path First)          │  │
│     │ 메트릭: 비용 (Cost, 대역폭 기반)                               │  │
│     │ 프로토콜: OSPF, IS-IS                                          │  │
│     │                                                                 │  │
│     │ 장점: 빠른 수렴, 루프 방지, 계층적 확장                         │  │
│     │ 단점: 메모리/CPU 사용 많음, 구현 복잡                          │  │
│     │                                                                 │  │
│     │ 동작 과정:                                                      │  │
│     │   ① Hello 패킷으로 인접 라우터 발견                            │  │
│     │   ② LSA(Link State Advertisement) 전파                         │  │
│     │   ③ 전체 토폴로지 맵 구성 (LSDB)                               │  │
│     │   ④ 다익스트라로 SPF 트리 계산                                 │  │
│     │   ⑤ 라우팅 테이블 생성                                         │  │
│     └───────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  3. 경로 벡터 (Path Vector)                                             │
│     ┌───────────────────────────────────────────────────────────────┐  │
│     │ 핵심 개념: AS 경로 정보 포함으로 루프 방지                      │  │
│     │ 프로토콜: BGP (Border Gateway Protocol)                        │  │
│     │ 메트릭: AS-PATH 길이, 정책                                     │  │
│     │                                                                 │  │
│     │ 장점: 대규모 네트워크 확장, 정책 기반 라우팅                    │  │
│     │ 단점: 느린 수렴, 설정 복잡                                      │  │
│     │                                                                 │  │
│     │ BGP 경로 선택 순서:                                             │  │
│     │   1. Highest Weight (Cisco 전용)                               │  │
│     │   2. Highest Local Preference                                  │  │
│     │   3. Shortest AS-PATH                                          │  │
│     │   4. Lowest Origin Type                                        │  │
│     │   5. Lowest MED                                                │  │
│     │   6. eBGP > iBGP                                               │  │
│     │   7. Lowest IGP cost to BGP next-hop                          │  │
│     └───────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**주요 라우팅 프로토콜 구조** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        OSPF 계층 구조                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                     AS (Autonomous System)                       │  │
│   │  ┌───────────────────────────────────────────────────────────┐  │  │
│   │  │                    Area 0 (Backbone)                       │  │  │
│   │  │         ┌─────────────────────────────────────┐           │  │  │
│   │  │         │           Backbone 라우터            │           │  │  │
│   │  │         │   ┌─────┐         ┌─────┐          │           │  │  │
│   │  │         │   │ ABR │─────────│ ABR │          │           │  │  │
│   │  │         │   └──┬──┘         └──┬──┘          │           │  │  │
│   │  │         └──────┼───────────────┼─────────────┘           │  │  │
│   │  └────────────────┼───────────────┼─────────────────────────┘  │  │
│   │                   │               │                             │  │
│   │  ┌────────────────┴────┐    ┌────┴────────────────────────┐   │  │
│   │  │      Area 1          │    │         Area 2              │   │  │
│   │  │  ┌─────┐   ┌─────┐   │    │   ┌─────┐   ┌─────┐        │   │  │
│   │  │  │내부 │───│내부 │   │    │   │내부 │───│내부 │        │   │  │
│   │  │  │라우터│   │라우터│   │    │   │라우터│   │라우터│        │   │  │
│   │  │  └─────┘   └─────┘   │    │   └─────┘   └─────┘        │   │  │
│   │  └──────────────────────┘    └─────────────────────────────┘   │  │
│   │                                                                  │  │
│   │  라우터 유형:                                                    │  │
│   │  - Internal Router: 단일 Area 내부                               │  │
│   │  - ABR (Area Border Router): Area 간 연결                        │  │
│   │  - ASBR (AS Boundary Router): 외부 AS 연결                       │  │
│   │  - Backbone Router: Area 0 내부                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        BGP 인터넷 구조                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                     ┌─────────────────────┐                            │
│                     │      Tier 1 ISP     │                            │
│                     │    (AT&T, Verizon)  │                            │
│                     └──────────┬──────────┘                            │
│                    ┌───────────┼───────────┐                           │
│                    ▼           ▼           ▼                           │
│           ┌────────────┐ ┌────────────┐ ┌────────────┐                │
│           │ Tier 2 ISP │ │ Tier 2 ISP │ │ Tier 2 ISP │                │
│           └─────┬──────┘ └─────┬──────┘ └─────┬──────┘                │
│                 │              │              │                         │
│        ┌────────┴───┐   ┌──────┴────┐   ┌────┴────────┐               │
│        ▼            ▼   ▼           ▼   ▼             ▼               │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│   │기업망 AS│ │클라우드 │ │기업망 AS│ │대학 AS  │ │CDN AS   │        │
│   │ (AS1)   │ │(AS2)    │ │(AS3)    │ │(AS4)    │ │(AS5)    │        │
│   └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘        │
│                                                                         │
│   BGP 용어:                                                             │
│   - eBGP: 서로 다른 AS 간 BGP 세션                                      │
│   - iBGP: 동일 AS 내부 BGP 세션                                         │
│   - AS-PATH: 패킷가 거친 AS 번호 목록                                   │
│   - Peering: ISP 간 상호 연결                                           │
│   - Transit: 인터넷 연결성 제공 서비스                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**핵심 알고리즘/공식** (해당 시 필수):
```
[다익스트라 알고리즘 (OSPF SPF)]

1. 초기화:
   - 시작 노드 거리 = 0, 다른 모든 노드 = ∞
   - 방문하지 않은 모든 노드를 집합 Q에 추가

2. 반복:
   - Q에서 거리가 가장 작은 노드 u 선택
   - u를 Q에서 제거
   - u의 모든 인접 노드 v에 대해:
     if d[u] + cost(u,v) < d[v]:
         d[v] = d[u] + cost(u,v)
         prev[v] = u

3. 종료:
   - Q가 비면 종료
   - prev[] 배열로 최단 경로 역추적

시간 복잡도: O((V+E) log V) with priority queue

[OSPF 비용 계산]

Cost = 참조 대역폭 / 인터페이스 대역폭

기본 참조 대역폭: 10^8 bps (100 Mbps)

예시:
- FastEthernet (100 Mbps): 10^8 / 10^8 = 1
- GigabitEthernet (1 Gbps): 10^8 / 10^9 = 0.1 → 1 (최소값)
- 10 GigabitEthernet: 10^8 / 10^10 = 0.01 → 1

참조 대역폭 변경 (고속 링크 권장):
  auto-cost reference-bandwidth 100000  (100 Gbps 기준)

[최장 프리픽스 매칭 (Longest Prefix Match)]

라우팅 결정 시 가장 구체적인(긴) 프리픽스 선택

예시: 목적지 10.1.1.5
  10.0.0.0/8    → 매칭 (프리픽스 길이 8)
  10.1.0.0/16   → 매칭 (프리픽스 길이 16) ★ 선택
  10.1.1.0/24   → 매칭 (프리픽스 길이 24) ★★ 선택

→ 10.1.1.0/24로 라우팅 (가장 긴 프리픽스)

[관리 거리 (Administrative Distance)]

같은 목적지에 여러 프로토콜이 경로를 제공할 때 우선순위 결정

┌─────────────────────────────────────────┐
│ 출처           │ AD 값 │ 설명           │
├─────────────────────────────────────────┤
│ 직접 연결       │   0  │ 인터페이스 직접│
│ 정적 라우팅     │   1  │ ip route       │
│ EIGRP 요약     │   5  │                │
│ eBGP           │  20  │ 외부 BGP       │
│ EIGRP 내부     │  90  │                │
│ IGRP           │ 100  │ (구식)         │
│ OSPF           │ 110  │                │
│ IS-IS          │ 115  │                │
│ RIP            │ 120  │                │
│ EIGRP 외부     │ 170  │                │
│ iBGP           │ 200  │ 내부 BGP       │
│ Unknown        │ 255  │ 사용 안 함     │
└─────────────────────────────────────────┘
```

**코드 예시** (필수: Python 라우팅 시뮬레이터):
```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum, auto
from collections import defaultdict
import heapq

# ============================================================
# 라우팅 테이블 및 프로토콜 시뮬레이터
# ============================================================

class RouteType(Enum):
    """라우트 타입"""
    CONNECTED = auto()   # 직접 연결
    STATIC = auto()      # 정적 라우팅
    OSPF = auto()        # OSPF
    RIP = auto()         # RIP
    BGP = auto()         # BGP


@dataclass
class Route:
    """라우트 엔트리"""
    network: str          # 목적지 네트워크
    prefix_len: int       # 프리픽스 길이
    next_hop: str         # 다음 홉
    interface: str        # 인터페이스
    metric: int           # 메트릭
    route_type: RouteType
    admin_distance: int   # 관리 거리

    @property
    def network_address(self) -> Tuple[int, ...]:
        """네트워크 주소를 튜플로 변환"""
        return tuple(int(x) for x in self.network.split('.'))

    def matches(self, dest_ip: str) -> bool:
        """목적지 IP가 이 라우트와 매칭되는지 확인"""
        dest_parts = [int(x) for x in dest_ip.split('.')]
        net_parts = self.network_address

        # 프리픽스 길이만큼 비트 비교
        bits_to_check = self.prefix_len
        for i in range(4):
            if bits_to_check <= 0:
                break
            mask_bits = min(8, bits_to_check)
            mask = (0xFF << (8 - mask_bits)) & 0xFF
            if (dest_parts[i] & mask) != (net_parts[i] & mask):
                return False
            bits_to_check -= 8
        return True

    def __str__(self):
        return (f"{self.network}/{self.prefix_len} via {self.next_hop} "
                f"[{self.route_type.name}, AD:{self.admin_distance}, "
                f"Metric:{self.metric}]")


class RoutingTable:
    """라우팅 테이블"""

    def __init__(self):
        self.routes: List[Route] = []

    def add_route(self, route: Route) -> None:
        """라우트 추가"""
        self.routes.append(route)
        # 프리픽스 길이 내림차순 정렬 (최장 매칭 우선)
        self.routes.sort(key=lambda r: r.prefix_len, reverse=True)

    def lookup(self, dest_ip: str) -> Optional[Route]:
        """최장 프리픽스 매칭으로 라우트 검색"""
        matching_routes = []

        for route in self.routes:
            if route.matches(dest_ip):
                matching_routes.append(route)

        if not matching_routes:
            return None

        # 1. 최장 프리픽스 매칭
        max_prefix = max(r.prefix_len for r in matching_routes)
        longest_matches = [r for r in matching_routes if r.prefix_len == max_prefix]

        # 2. 가장 낮은 AD 선택
        min_ad = min(r.admin_distance for r in longest_matches)
        best_routes = [r for r in longest_matches if r.admin_distance == min_ad]

        # 3. 가장 낮은 메트릭 선택
        return min(best_routes, key=lambda r: r.metric)

    def print_table(self) -> None:
        """라우팅 테이블 출력"""
        print("\n" + "=" * 70)
        print("                    라우팅 테이블")
        print("=" * 70)
        print(f"{'목적지':<20} {'다음 홉':<15} {'AD':<5} {'메트릭':<8} {'타입'}")
        print("-" * 70)
        for route in self.routes:
            print(f"{route.network}/{route.prefix_len:<15} {route.next_hop:<15} "
                  f"{route.admin_distance:<5} {route.metric:<8} {route.route_type.name}")
        print("=" * 70)


# ============================================================
# 다익스트라 알고리즘 (OSPF SPF 시뮬레이션)
# ============================================================

@dataclass
class Link:
    """링크 정보"""
    router1: str
    router2: str
    cost: int


class NetworkTopology:
    """네트워크 토폴로지"""

    def __init__(self):
        self.routers: Set[str] = set()
        self.links: List[Link] = []
        self.adjacency: Dict[str, Dict[str, int]] = defaultdict(dict)

    def add_router(self, name: str) -> None:
        """라우터 추가"""
        self.routers.add(name)

    def add_link(self, router1: str, router2: str, cost: int) -> None:
        """링크 추가 (양방향)"""
        self.links.append(Link(router1, router2, cost))
        self.adjacency[router1][router2] = cost
        self.adjacency[router2][router1] = cost

    def dijkstra(self, source: str) -> Tuple[Dict[str, int], Dict[str, str]]:
        """다익스트라 알고리즘으로 최단 경로 계산"""
        distances = {router: float('infinity') for router in self.routers}
        previous = {router: None for router in self.routers}
        distances[source] = 0

        # 우선순위 큐: (거리, 라우터)
        pq = [(0, source)]
        visited = set()

        while pq:
            current_dist, current = heapq.heappop(pq)

            if current in visited:
                continue
            visited.add(current)

            for neighbor, cost in self.adjacency[current].items():
                if neighbor in visited:
                    continue
                new_dist = current_dist + cost
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))

        return distances, previous

    def get_path(self, source: str, dest: str) -> List[str]:
        """소스에서 목적지까지의 경로 반환"""
        _, previous = self.dijkstra(source)
        path = []
        current = dest
        while current:
            path.append(current)
            current = previous[current]
        return list(reversed(path))

    def print_topology(self) -> None:
        """토폴로지 출력"""
        print("\n" + "=" * 50)
        print("          네트워크 토폴로지")
        print("=" * 50)
        for link in self.links:
            print(f"  {link.router1} ←──({link.cost})──→ {link.router2}")
        print("=" * 50)


# ============================================================
# RIP (거리 벡터) 시뮬레이터
# ============================================================

class RIPRouter:
    """RIP 라우터 시뮬레이터"""

    MAX_HOPS = 15
    INFINITY = 16

    def __init__(self, name: str):
        self.name = name
        self.neighbors: Dict[str, 'RIPRouter'] = {}  # 이름 → 라우터
        self.distance_vector: Dict[str, Tuple[int, str]] = {}  # 목적지 → (거리, 다음홉)
        self.distance_vector[name] = (0, name)  # 자기 자신

    def add_neighbor(self, neighbor: 'RIPRouter') -> None:
        """인접 라우터 추가"""
        self.neighbors[neighbor.name] = neighbor
        self.distance_vector[neighbor.name] = (1, neighbor.name)

    def receive_update(self, from_router: str,
                       vector: Dict[str, Tuple[int, str]]) -> bool:
        """인접 라우터로부터 거리 벡터 수신"""
        changed = False

        for dest, (dist, _) in vector.items():
            if dest == self.name:
                continue

            new_dist = dist + 1  # 1홉 추가

            if new_dist > self.MAX_HOPS:
                new_dist = self.INFINITY

            if dest not in self.distance_vector or \
               new_dist < self.distance_vector[dest][0]:
                self.distance_vector[dest] = (new_dist, from_router)
                changed = True

        return changed

    def send_update(self) -> Dict[str, Tuple[int, str]]:
        """자신의 거리 벡터를 인접 라우터에게 전송"""
        return self.distance_vector.copy()

    def print_routing_table(self) -> None:
        """라우팅 테이블 출력"""
        print(f"\n[{self.name}] RIP 라우팅 테이블:")
        print(f"{'목적지':<15} {'홉 수':<10} {'다음 홉'}")
        print("-" * 40)
        for dest, (dist, next_hop) in sorted(self.distance_vector.items()):
            if dist < self.INFINITY:
                print(f"{dest:<15} {dist:<10} {next_hop}")


class RIPNetwork:
    """RIP 네트워크 시뮬레이터"""

    def __init__(self):
        self.routers: Dict[str, RIPRouter] = {}

    def add_router(self, name: str) -> RIPRouter:
        router = RIPRouter(name)
        self.routers[name] = router
        return router

    def connect(self, r1: str, r2: str) -> None:
        """두 라우터 연결"""
        self.routers[r1].add_neighbor(self.routers[r2])
        self.routers[r2].add_neighbor(self.routers[r1])

    def simulate_convergence(self, max_iterations: int = 10) -> None:
        """RIP 수렴 시뮬레이션"""
        print("\n" + "=" * 50)
        print("     RIP 거리 벡터 교환 시뮬레이션")
        print("=" * 50)

        for iteration in range(max_iterations):
            print(f"\n--- Iteration {iteration + 1} ---")
            any_changed = False

            for router in self.routers.values():
                # 인접 라우터에게 자신의 벡터 전송
                my_vector = router.send_update()

                for neighbor_name, neighbor in router.neighbors.items():
                    changed = neighbor.receive_update(router.name, my_vector)
                    if changed:
                        any_changed = True
                        print(f"  {neighbor_name}: {router.name}으로부터 업데이트 수신")

            if not any_changed:
                print("\n✓ 수렴 완료!")
                break

        # 최종 상태 출력
        for router in self.routers.values():
            router.print_routing_table()


# ============================================================
# BGP 경로 선택 시뮬레이터
# ============================================================

@dataclass
class BGPRoute:
    """BGP 라우트"""
    prefix: str
    as_path: List[int]           # AS 경로
    next_hop: str
    local_pref: int = 100        # 로컬 선호도
    med: int = 0                 # Multi-Exit Discriminator
    origin: str = "IGP"          # IGP, EGP, INCOMPLETE
    is_ebgp: bool = True         # eBGP 여부
    igp_cost: int = 0            # Next-hop까지의 IGP 비용


class BGPPathSelector:
    """BGP 경로 선택기"""

    def __init__(self):
        self.routes: List[BGPRoute] = []

    def add_route(self, route: BGPRoute) -> None:
        self.routes.append(route)

    def select_best_path(self) -> Optional[BGPRoute]:
        """BGP 경로 선택 알고리즘"""
        if not self.routes:
            return None

        candidates = self.routes.copy()

        # 1. Highest Weight (로컬 설정, 생략)

        # 2. Highest Local Preference
        max_lp = max(r.local_pref for r in candidates)
        candidates = [r for r in candidates if r.local_pref == max_lp]
        if len(candidates) == 1:
            return candidates[0]

        # 3. Shortest AS-PATH
        min_as_len = min(len(r.as_path) for r in candidates)
        candidates = [r for r in candidates if len(r.as_path) == min_as_len]
        if len(candidates) == 1:
            return candidates[0]

        # 4. Lowest Origin Type (IGP < EGP < INCOMPLETE)
        origin_order = {"IGP": 0, "EGP": 1, "INCOMPLETE": 2}
        min_origin = min(origin_order[r.origin] for r in candidates)
        candidates = [r for r in candidates if origin_order[r.origin] == min_origin]
        if len(candidates) == 1:
            return candidates[0]

        # 5. Lowest MED
        min_med = min(r.med for r in candidates)
        candidates = [r for r in candidates if r.med == min_med]
        if len(candidates) == 1:
            return candidates[0]

        # 6. eBGP over iBGP
        ebgp_routes = [r for r in candidates if r.is_ebgp]
        if ebgp_routes:
            candidates = ebgp_routes
            if len(candidates) == 1:
                return candidates[0]

        # 7. Lowest IGP cost to BGP next-hop
        min_igp = min(r.igp_cost for r in candidates)
        candidates = [r for r in candidates if r.igp_cost == min_igp]

        # 8. Oldest route (첫 번째 선택)
        return candidates[0] if candidates else None

    def print_candidates(self) -> None:
        """후보 경로 출력"""
        print("\n" + "=" * 70)
        print("                    BGP 경로 후보")
        print("=" * 70)
        print(f"{'프리픽스':<18} {'AS-PATH':<20} {'LP':<5} {'MED':<5} {'Origin'}")
        print("-" * 70)
        for route in self.routes:
            as_path = ' '.join(str(asn) for asn in route.as_path)
            print(f"{route.prefix:<18} {as_path:<20} {route.local_pref:<5} "
                  f"{route.med:<5} {route.origin}")
        print("=" * 70)


# ============================================================
# 사용 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("         라우팅 프로토콜 시뮬레이터 데모")
    print("=" * 60)

    # 1. 라우팅 테이블 조회 테스트
    print("\n1. 라우팅 테이블 최장 프리픽스 매칭")
    print("-" * 40)

    rt = RoutingTable()
    rt.add_route(Route("0.0.0.0", 0, "10.0.0.1", "eth0", 1, RouteType.STATIC, 1))
    rt.add_route(Route("10.0.0.0", 8, "10.0.0.1", "eth0", 1, RouteType.OSPF, 110))
    rt.add_route(Route("10.1.1.0", 24, "10.0.0.254", "eth0", 2, RouteType.OSPF, 110))
    rt.add_route(Route("192.168.1.0", 24, "10.0.0.254", "eth0", 3, RouteType.RIP, 120))

    rt.print_table()

    # 조회 테스트
    test_ips = ["10.1.1.5", "10.2.3.4", "192.168.1.100", "8.8.8.8"]
    for ip in test_ips:
        route = rt.lookup(ip)
        if route:
            print(f"  {ip} → {route.network}/{route.prefix_len}")
        else:
            print(f"  {ip} → 매칭되는 라우트 없음")

    # 2. 다익스트라 (OSPF SPF) 테스트
    print("\n\n2. 다익스트라 알고리즘 (OSPF SPF)")
    print("-" * 40)

    topo = NetworkTopology()
    for r in ['A', 'B', 'C', 'D', 'E']:
        topo.add_router(r)

    topo.add_link('A', 'B', 2)
    topo.add_link('A', 'C', 5)
    topo.add_link('B', 'C', 1)
    topo.add_link('B', 'D', 3)
    topo.add_link('C', 'D', 1)
    topo.add_link('D', 'E', 2)

    topo.print_topology()

    distances, previous = topo.dijkstra('A')
    print(f"\nA에서 각 라우터까지의 최단 거리:")
    for router, dist in sorted(distances.items()):
        path = topo.get_path('A', router)
        print(f"  {router}: {dist} (경로: {' → '.join(path)})")

    # 3. RIP 거리 벡터 시뮬레이션
    print("\n\n3. RIP 거리 벡터 시뮬레이션")
    print("-" * 40)

    rip_net = RIPNetwork()
    for name in ['R1', 'R2', 'R3', 'R4']:
        rip_net.add_router(name)

    rip_net.connect('R1', 'R2')
    rip_net.connect('R2', 'R3')
    rip_net.connect('R3', 'R4')
    rip_net.connect('R1', 'R4')

    rip_net.simulate_convergence()

    # 4. BGP 경로 선택
    print("\n\n4. BGP 경로 선택 알고리즘")
    print("-" * 40)

    bgp = BGPPathSelector()
    bgp.add_route(BGPRoute(
        prefix="203.0.113.0/24",
        as_path=[100, 200, 300],
        next_hop="10.0.1.1",
        local_pref=100,
        med=10
    ))
    bgp.add_route(BGPRoute(
        prefix="203.0.113.0/24",
        as_path=[100, 300],  # 더 짧은 AS-PATH
        next_hop="10.0.2.1",
        local_pref=100,
        med=20
    ))
    bgp.add_route(BGPRoute(
        prefix="203.0.113.0/24",
        as_path=[100, 400, 300],
        next_hop="10.0.3.1",
        local_pref=200,  # 더 높은 Local Pref
        med=5
    ))

    bgp.print_candidates()
    best = bgp.select_best_path()
    print(f"\n✓ 선택된 최적 경로: AS-PATH {best.as_path} "
          f"(Local Pref: {best.local_pref})")
