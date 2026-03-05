+++
title = "Rack Awareness (랙 인식)"
categories = ["studynotes-16_bigdata"]
+++

# Rack Awareness (랙 인식)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 랙 인식은 HDFS가 데이터 복제본을 여러 랙에 분산 저장하여 랙 장애 시에도 데이터 가용성을 보장하는 기술이다.
> 2. **가치**: 랙 인식을 통해 단일 랙 장애, 네트워크 스위치 장애, 전원 장애 시에도 데이터 손실을 방지할 수 있다.
> 3. **융합**: 복제 배치 정책, 네트워크 토폴로지, 읽기 최적화와 결합하여 HDFS의 신뢰성과 성능을 향상시킨다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

Rack Awareness는 HDFS가 각 DataNode가 속한 랙(Rack) 정보를 인식하고, 이를 바탕으로 블록 복제본의 배치를 최적화하는 기능이다. 기본 복제 정책은 첫 번째 복제본은 로컬 랙, 두 번째는 다른 랙, 세 번째는 두 번째와 같은 랙의 다른 노드에 저장한다.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    랙 인식 복제 배치 정책                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  랙 1 (Rack 1)                                                   │   │
│  │  ┌─────────┐   ┌─────────┐                                      │   │
│  │  │ Node A  │   │ Node B  │                                      │   │
│  │  │ [복제1] │   │         │                                      │   │
│  │  └─────────┘   └─────────┘                                      │   │
│  │         스위치 1                                                 │   │
│  └─────────────────────────────┬───────────────────────────────────┘   │
│                                │ 코어 스위치                            │
│  ┌─────────────────────────────┴───────────────────────────────────┐   │
│  │  랙 2 (Rack 2)                                                   │   │
│  │  ┌─────────┐   ┌─────────┐                                      │   │
│  │  │ Node C  │   │ Node D  │                                      │   │
│  │  │ [복제2] │   │ [복제3] │                                      │   │
│  │  └─────────┘   └─────────┘                                      │   │
│  │         스위치 2                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  복제 배치 규칙 (복제 계수 = 3):                                        │
│  1. 복제본 1: 쓰기 요청한 클라이언트와 같은 노드 (없으면 같은 랙)       │
│  2. 복제본 2: 복제본 1과 다른 랙의 임의 노드                            │
│  3. 복제본 3: 복제본 2와 같은 랙의 다른 노드                            │
│                                                                         │
│  장애 시나리오 대응:                                                    │
│  - 랙 1 전체 장애 → 복제본 2, 3 사용 가능                              │
│  - 랙 2 전체 장애 → 복제본 1 사용 가능                                 │
│  - 노드 A 장애 → 복제본 2, 3 사용 가능                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 💡 비유

랙 인식은 "비상구 분산 배치"에 비유할 수 있다. 건물의 비상구가 모두 1층에만 있으면 1층 화재 시 대피할 수 없다. 각 층에 비상구를 두면 어떤 층에 화재가 나도 대피할 수 있다. 랙 인식은 데이터의 복제본을 여러 랙(층)에 분산하여 장애에 대비한다.

### 등장 배경

1. **데이터 센터 구조**: 실제 데이터 센터는 랙 단위로 구성
2. **공통 장애**: 전원, 네트워크 스위치 등 랙 단위 공통 장애 발생
3. **네트워크 최적화**: 랙 내 전송은 빠르고, 랙 간 전송은 느림

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 랙 토폴로지 구성

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class NodeType(Enum):
    ROOT = "/"
    RACK = "rack"
    HOST = "host"

@dataclass
class DatanodeDescriptor:
    """DataNode 정보"""
    hostname: str
    ip_address: str
    rack_location: str
    port: int
    capacity: int
    remaining: int

class NetworkTopology:
    """네트워크 토폴로지 관리"""

    def __init__(self):
        self.datanodes: Dict[str, DatanodeDescriptor] = {}
        self.rack_map: Dict[str, List[str]] = {}  # rack -> [datanodes]

    def add_datanode(self, dn: DatanodeDescriptor):
        """DataNode 추가"""
        self.datanodes[dn.hostname] = dn

        rack = dn.rack_location
        if rack not in self.rack_map:
            self.rack_map[rack] = []
        self.rack_map[rack].append(dn.hostname)

    def get_rack(self, hostname: str) -> str:
        """DataNode의 랙 위치 반환"""
        dn = self.datanodes.get(hostname)
        return dn.rack_location if dn else "/default-rack"

    def is_on_same_rack(self, host1: str, host2: str) -> bool:
        """두 노드가 같은 랙에 있는지 확인"""
        return self.get_rack(host1) == self.get_rack(host2)

    def get_distance(self, host1: str, host2: str) -> int:
        """두 노드 간 거리 계산"""
        if host1 == host2:
            return 0  # 같은 노드

        rack1 = self.get_rack(host1)
        rack2 = self.get_rack(host2)

        if rack1 == rack2:
            return 2  # 같은 랙, 다른 노드
        else:
            return 4  # 다른 랙

    def get_nodes_in_rack(self, rack: str) -> List[str]:
        """특정 랙의 모든 노드 반환"""
        return self.rack_map.get(rack, [])

    def get_other_racks(self, rack: str) -> List[str]:
        """지정된 랙 외의 모든 랙 반환"""
        return [r for r in self.rack_map.keys() if r != rack]


class BlockPlacementPolicy:
    """블록 배치 정책 (기본: 3복제)"""

    def __init__(self, topology: NetworkTopology, replication: int = 3):
        self.topology = topology
        self.replication = replication

    def choose_targets(
        self,
        writer: str,           # 쓰기 요청 노드
        excluded: List[str],   # 제외할 노드
        block_size: int        # 블록 크기
    ) -> List[str]:
        """복제본 배치 대상 선택"""

        targets = []

        # 1. 첫 번째 복제본: 쓰기 요청자와 같은 노드 또는 랙
        if writer and writer not in excluded:
            targets.append(writer)
        else:
            # 같은 랙의 다른 노드
            same_rack_nodes = self._choose_from_same_rack(writer, excluded)
            if same_rack_nodes:
                targets.append(same_rack_nodes[0])

        if len(targets) >= self.replication:
            return targets[:self.replication]

        # 2. 두 번째 복제본: 다른 랙의 노드
        writer_rack = self.topology.get_rack(writer) if writer else None
        other_racks = self.topology.get_other_racks(writer_rack)

        if other_racks:
            # 임의의 다른 랙 선택
            import random
            target_rack = random.choice(other_racks)
            nodes_in_rack = self.topology.get_nodes_in_rack(target_rack)
            available = [n for n in nodes_in_rack if n not in excluded and n not in targets]
            if available:
                second_replica = random.choice(available)
                targets.append(second_replica)

        if len(targets) >= self.replication:
            return targets[:self.replication]

        # 3. 세 번째 복제본: 두 번째와 같은 랙의 다른 노드
        if len(targets) >= 2:
            second_rack = self.topology.get_rack(targets[1])
            nodes_in_rack = self.topology.get_nodes_in_rack(second_rack)
            available = [
                n for n in nodes_in_rack
                if n not in excluded and n not in targets
            ]
            if available:
                targets.append(available[0])

        # 추가 복제본: 다른 랙에서 선택
        while len(targets) < self.replication:
            for rack in self.topology.rack_map.keys():
                nodes = self.topology.get_nodes_in_rack(rack)
                available = [n for n in nodes if n not in excluded and n not in targets]
                if available:
                    targets.append(available[0])
                    if len(targets) >= self.replication:
                        break

        return targets[:self.replication]

    def _choose_from_same_rack(self, node: str, excluded: List[str]) -> List[str]:
        """같은 랙에서 노드 선택"""
        if not node:
            return []

        rack = self.topology.get_rack(node)
        nodes = self.topology.get_nodes_in_rack(rack)
        return [n for n in nodes if n not in excluded and n != node]

    def verify_block_placement(self, locations: List[str]) -> Dict:
        """블록 배치 검증"""
        if not locations:
            return {"valid": False, "reason": "No replicas"}

        racks = set()
        for loc in locations:
            racks.add(self.topology.get_rack(loc))

        return {
            "valid": len(racks) >= 2,  # 최소 2개 랙에 분산
            "replica_count": len(locations),
            "rack_count": len(racks),
            "racks": list(racks)
        }


# 랙 토폴로지 스크립트 예시 (shell script)
RACK_TOPOLOGY_SCRIPT = '''#!/bin/bash
# Hadoop Rack Awareness Script
# 입력: IP 주소 또는 호스트명 목록
# 출력: 각 호스트의 랙 위치

while read line; do
    case $line in
        192.168.1.*) echo "/rack1" ;;
        192.168.2.*) echo "/rack2" ;;
        192.168.3.*) echo "/rack3" ;;
        node0[1-9].*) echo "/rack1" ;;
        node1[0-9].*) echo "/rack2" ;;
        node2[0-9].*) echo "/rack3" ;;
        *) echo "/default-rack" ;;
    esac
done
'''


# 사용 예시
if __name__ == "__main__":
    topology = NetworkTopology()

    # DataNode 등록
    topology.add_datanode(DatanodeDescriptor(
        hostname="node01",
        ip_address="192.168.1.1",
        rack_location="/rack1",
        port=9866,
        capacity=10 * 1024**12,
        remaining=8 * 1024**12
    ))
    topology.add_datanode(DatanodeDescriptor(
        hostname="node02",
        ip_address="192.168.1.2",
        rack_location="/rack1",
        port=9866,
        capacity=10 * 1024**12,
        remaining=7 * 1024**12
    ))
    topology.add_datanode(DatanodeDescriptor(
        hostname="node03",
        ip_address="192.168.2.1",
        rack_location="/rack2",
        port=9866,
        capacity=10 * 1024**12,
        remaining=9 * 1024**12
    ))
    topology.add_datanode(DatanodeDescriptor(
        hostname="node04",
        ip_address="192.168.2.2",
        rack_location="/rack2",
        port=9866,
        capacity=10 * 1024**12,
        remaining=6 * 1024**12
    ))

    # 블록 배치 정책
    policy = BlockPlacementPolicy(topology, replication=3)

    # 클라이언트가 node01에서 쓰기 요청
    targets = policy.choose_targets(
        writer="node01",
        excluded=[],
        block_size=128 * 1024 * 1024
    )

    print(f"복제본 배치 대상: {targets}")

    # 배치 검증
    verification = policy.verify_block_placement(targets)
    print(f"배치 검증: {verification}")
