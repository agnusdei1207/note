+++
title = "전송 모드 (Transmission Modes: Simplex, Half/Full Duplex)"
date = 2024-05-18
description = "통신 시스템의 데이터 전송 방향성에 따른 분류 - 단방향(Simplex), 반이중(Half-Duplex), 전이중(Full-Duplex)의 원리, 장단점, 그리고 실무 적용"
weight = 40
[taxonomies]
categories = ["studynotes-network"]
tags = ["Simplex", "Half-Duplex", "Full-Duplex", "Transmission", "CSMA/CD"]
+++

# 전송 모드 (Transmission Modes: Simplex, Half/Full Duplex)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전송 모드는 통신 채널에서 데이터가 흐를 수 있는 방향성을 정의하는 것으로, 단방향(Simplex), 양방향 교대(Half-Duplex), 양방향 동시(Full-Duplex)의 세 가지 유형이 있습니다.
> 2. **가치**: 전송 모드 선택은 채널 용량 활용 효율, 하드웨어 복잡도, 충돌 관리에 직접적 영향을 미치며, 이더넷(Full-Duplex switching), 무선 LAN(Half-Duplex CSMA/CA), 위성 통신(Simplex broadcast)의 핵심 설계 요소입니다.
> 3. **융합**: 5G TDD/FDD, Wi-Fi 6/7의 MU-MIMO, DOCSIS 3.1/4.0 등 현대 통신은 전송 모드와 다중화 기술을 결합하여 대역폭 효율을 극대화합니다.

---

## Ⅰ. 개요 (Context & Background)

전송 모드(Transmission Mode) 또는 통신 모드(Communication Mode)는 통신 시스템에서 데이터가 전송될 수 있는 방향과 시점을 정의하는 특성입니다. 이는 두 장치 간의 통신이 한 방향으로만 이루어지는지, 양방향으로 이루어지되 동시인지 교대인지를 결정합니다.

**💡 비유**: 전송 모드는 **'도로의 교통 흐름'**과 같습니다.
- **단방향(Simplex)**: 일방통행 도로 - 차가 한 방향으로만 갈 수 있음 (라디오 방송)
- **반이중(Half-Duplex)**: 좁은 다리 - 양 방향 모두 가능하지만 한 번에 한쪽만 (무전기)
- **전이중(Full-Duplex)**: 왕복 4차선 도로 - 양 방향이 동시에 가능 (전화)

**등장 배경 및 발전 과정**:
1. **기존 기술의 치명적 한계점**: 초기 통신 시스템은 단방향(방송) 또는 교대식(전보)이었습니다. 전화가 등장했을 때도 초기에는 한 쌍의 선으로 한 번에 한 사람만 말할 수 있었습니다.
2. **혁신적 패러다임 변화**: 20세기 초 4선식 회선(4-wire circuit) 도입으로 전이중 통신이 가능해졌고, 이더넷에서 스위칭 허브의 등장으로 Full-Duplex가 표준이 되었습니다.
3. **비즈니스적 요구사항**: 현대의 실시간 화상 회의, 온라인 게이밍, 고주파 거래(HFT) 등은 대칭형 초저지연 양방향 통신을 요구하며, Full-Duplex 설계가 필수적입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 전송 모드 분류 구조

```ascii
                        전송 모드 (Transmission Modes)
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
    ┌────┴────┐              ┌────┴────┐              ┌────┴────┐
    │단방향    │              │ 반이중   │              │ 전이중   │
    │ Simplex │              │Half-Dup.│              │Full-Dup.│
    └────┬────┘              └────┬────┘              └────┬────┘
         │                        │                        │
    ┌────┴────────┐          ┌────┴────┐          ┌───────┴───────┐
    │ • 라디오 방송│          │ 무전기   │          │ • 전화망       │
    │ • TV 방송    │          │ 이더넷   │          │ • 이더넷 스위치 │
    │ • 키보드→PC  │          │ Walkie-  │          │ • 셀룰러 (FDD) │
    │ • GPS 위성   │          │  Talkie  │          │ • 광섬유       │
    └─────────────┘          │ • 대형사  │          └───────────────┘
                              └──────────┘
```

### 전송 모드 상세 비교

| 특성 | Simplex (단방향) | Half-Duplex (반이중) | Full-Duplex (전이중) |
|---|---|---|---|
| **데이터 흐름** | 한 방향만 | 양방향 교대 | 양방향 동시 |
| **필요 채널 수** | 1개 | 1개 (시간 분할) | 2개 (또는 주파수 분할) |
| **전송 효율** | 최고 (100%) | 중간 (50% 이론) | 최고 (200%) |
| **하드웨어 복잡도** | 낮음 | 중간 | 높음 |
| **충돌 가능성** | 없음 | 있음 | 없음 |
| **예시** | 라디오, TV, 키보드 | 무전기, Hub 이더넷 | 전화, Switch 이더넷 |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Simplex (단방향 전송)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│     송신기 (Transmitter)              수신기 (Receiver)                     │
│     ┌──────────────┐                 ┌──────────────┐                      │
│     │    라디오     │ ───────────────→│   라디오      │                      │
│     │   방송국     │      신호       │   수신기      │                      │
│     └──────────────┘                 └──────────────┘                      │
│           ↑                                │                               │
│           │                                │                               │
│     데이터는 송신기에서 수신기로만 흐름                                       │
│     수신기가 송신기에게 응답할 방법 없음                                       │
│                                                                             │
│     예: TV 방송, GPS 위성, 키보드 → 컴퓨터, 센서 → 모니터                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         Half-Duplex (반이중 전송)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│     장치 A                           장치 B                                 │
│     ┌──────────────┐                 ┌──────────────┐                      │
│     │              │ ═══════════════→│              │  시간 t1: A → B      │
│     │   무전기     │    송신 모드     │   무전기     │                      │
│     │              │                 │              │                      │
│     └──────────────┘                 └──────────────┘                      │
│           │                                ↑                               │
│           │                                │                               │
│     ┌──────────────┐                 ┌──────────────┐                      │
│     │              │←═══════════════ │              │  시간 t2: B → A      │
│     │   무전기     │    수신 모드     │   무전기     │                      │
│     │              │                 │              │                      │
│     └──────────────┘                 └──────────────┘                      │
│                                                                             │
│     같은 채널을 시간 분할하여 사용, 동시 송수신 불가                           │
│     충돌 방지를 위한 프로토콜 필요 (CSMA/CD, RTS/CTS 등)                      │
│                                                                             │
│     예: 무전기, 이더넷 Hub, CB 라디오, 초기 이더넷                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         Full-Duplex (전이중 전송)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│     장치 A                           장치 B                                 │
│     ┌──────────────┐                 ┌──────────────┐                      │
│     │              │ ──────────────→ │              │                      │
│     │   전화기     │    채널 1       │   전화기     │                      │
│     │              │ ←────────────── │              │                      │
│     └──────────────┘    채널 2       └──────────────┘                      │
│                                                                             │
│     송신과 수신이 서로 다른 채널(또는 주파수)을 사용하여 동시 가능             │
│     충돌 없음, 이론적 용량 2배                                               │
│                                                                             │
│     구현 방식:                                                               │
│     • 공간 분할: 2쌍의선 (4-wire), 별도 TX/RX 케이블                        │
│     • 주파수 분할: FDD (상이한 주파수 대역 사용)                             │
│     • 시간 분할: TDD (시간 슬롯 교차 할당) - 사실상 Half-Duplex              │
│                                                                             │
│     예: 전화망, 이더넷 스위치, 광섬유, LTE FDD                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

**1. 이더넷에서의 Half-Duplex vs Full-Duplex**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    이더넷 Half-Duplex (Hub 기반)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────┐        ┌─────────────────────────────────┐        ┌─────┐         │
│  │ PC1 │────────│           HUB (Repeater)         │────────│ PC2 │         │
│  └─────┘        │    모든 포트로 동일 신호 브로드캐스트  │        └─────┘         │
│                 └─────────────────────────────────┘                         │
│                              │                                              │
│                              │                                              │
│                         ┌────┴────┐                                        │
│                         │   PC3   │                                        │
│                         └─────────┘                                        │
│                                                                             │
│  특징:                                                                       │
│  • 단일 충돌 도메인 (Single Collision Domain)                               │
│  • CSMA/CD (Carrier Sense Multiple Access / Collision Detection) 필요      │
│  • 동시에 하나의 장치만 전송 가능                                            │
│  • 최대 유효 처리량: ~37% (이론 50% - 충돌 오버헤드)                         │
│  • 10BASE-T, 100BASE-TX (Hub 사용 시)                                       │
│                                                                             │
│  CSMA/CD 동작:                                                               │
│  1. 채널이 비어있는지 감지 (Carrier Sense)                                   │
│  2. 비어있으면 전송 시작                                                     │
│  3. 전송 중 충돌 감지 (Collision Detection)                                  │
│  4. 충돌 시 Jam 신호 전송 후 Random Backoff                                  │
│  5. 재전송 시도                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    이더넷 Full-Duplex (Switch 기반)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────┐        ┌─────────────────────────────────┐        ┌─────┐         │
│  │ PC1 │←──────→│                                 │←──────→│ PC2 │         │
│  └─────┘  TX   │          SWITCH (L2)              │  TX   └─────┘         │
│          RX   │   각 포트별 독립된 충돌 도메인      │  RX                   │
│                 │   MAC 주소 학습 및 포워딩          │                        │
│                 └─────────────────────────────────┘                         │
│                              │                                              │
│                              │                                              │
│                         ┌────┴────┐                                        │
│                         │   PC3   │                                        │
│                         └─────────┘                                        │
│                                                                             │
│  특징:                                                                       │
│  • 포트별 독립 충돌 도메인 (Per-Port Collision Domain)                      │
│  • CSMA/CD 불필요 (충돌 없음)                                                │
│  • 동시 양방향 전송 가능                                                     │
│  • 유효 대역폭: 2배 (예: 1Gbps → 2Gbps 양방향 합계)                          │
│  • 1000BASE-T, 10GBASE-T (기본 Full-Duplex)                                 │
│                                                                             │
│  Auto-Negotiation:                                                          │
│  • 링크 파트너 간 속도 및 Duplex 모드 자동 협상                              │
│  • Fast Link Pulse (FLP) 교환                                               │
│  • 불일치 시 성능 저하 (Duplex Mismatch 문제)                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

**2. 무선 통신에서의 Half-Duplex**

```
Wi-Fi (802.11) - Half-Duplex 이유:
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  1. 하드웨어 제약:                                                           │
│     • 단일 안테나로 송수신 시 Self-Interference 발생                        │
│     • 송신 신호가 수신 신호보다 100dB 이상 강함                              │
│     • Self-Interference 제거 기술이 복잡하고 비용 high                      │
│                                                                             │
│  2. 채널 공유:                                                               │
│     • 동일 주파수 대역을 여러 장치가 공유                                    │
│     • CSMA/CA (Collision Avoidance) 사용                                    │
│     • RTS/CTS로 Hidden Terminal 문제 완화                                   │
│                                                                             │
│  3. TDD (Time Division Duplexing)                                           │
│     • 업링크/다운링크를 시간 분할                                            │
│     • Wi-Fi 6/7: UL/DL MU-MIMO로 효율 개선                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**3. 전이중 무선 (Full-Duplex Wireless) - 연구/상용화 진행 중**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Full-Duplex Wireless (Self-Interference Cancellation)     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  문제: 송신 신호가 자신의 수신 안테나에 간섭                                  │
│                                                                             │
│       ┌──────────────────┐                                                  │
│       │     송신기       │───→ 자기 자신의 수신기에 간섭!                    │
│       │  (강한 신호)     │         ↓↓↓↓↓↓↓↓                                 │
│       └──────────────────┘         │                                        │
│                                 ┌──┴───┐                                    │
│                                 │ 수신기│ ← 약한 외부 신호                   │
│                                 └──────┘                                    │
│                                                                             │
│  해결 기술:                                                                  │
│  1. 안테나 기법 (Analog Cancellation)                                       │
│     • 송신 신호를 180° 위상 반전시켜 수신 안테나에서 상쇄                    │
│     •circulator, directional antenna 사용                                   │
│                                                                             │
│  2. 디지털 신호 처리 (Digital Cancellation)                                 │
│     • 송신 신호를 알고 있으므로 수신 신호에서 subtract                       │
│     • 50~60 dB 감쇠 가능                                                    │
│                                                                             │
│  3. 혼합 기법                                                                │
│     • Analog + Digital 조합으로 100dB+ 달성                                 │
│     • Columbia University, Stanford 등 연구 성과                            │
│                                                                             │
│  상용화 현황:                                                                │
│  • Kumu Networks: Self-backhauling                                         │
│  • 5G Relay, In-band Full-Duplex                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: 전송 모드 시뮬레이션 (Python)

```python
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum

class TransmissionMode(Enum):
    SIMPLEX = "simplex"
    HALF_DUPLEX = "half_duplex"
    FULL_DUPLEX = "full_duplex"

@dataclass
class Packet:
    id: int
    source: int
    destination: int
    size_bits: int
    arrival_time: float
    transmission_time: float = 0.0
    collision: bool = False

class ChannelSimulator:
    """전송 모드별 채널 시뮬레이터"""

    def __init__(self, bandwidth_bps: float, mode: TransmissionMode):
        self.bandwidth = bandwidth_bps
        self.mode = mode
        self.packets: List[Packet] = []
        self.collisions = 0
        self.total_transmission_time = 0.0

    def simulate_simplex(self, packets: List[Packet]) -> dict:
        """단방향 전송 시뮬레이션"""
        transmitted = []
        current_time = 0.0

        for pkt in packets:
            transmission_duration = pkt.size_bits / self.bandwidth
            pkt.transmission_time = current_time + transmission_duration
            transmitted.append(pkt)
            current_time = pkt.transmission_time

        return {
            'mode': 'Simplex',
            'packets_sent': len(transmitted),
            'total_time': current_time,
            'throughput_bps': sum(p.size_bits for p in transmitted) / current_time if current_time > 0 else 0,
            'collisions': 0,
            'efficiency': 1.0
        }

    def simulate_half_duplex(self, packets_a_to_b: List[Packet],
                             packets_b_to_a: List[Packet]) -> dict:
        """반이중 전송 시뮬레이션 (간소화된 CSMA/CD)"""
        transmitted_a = []
        transmitted_b = []
        current_time = 0.0
        current_direction = None  # None, 'A_to_B', 'B_to_A'

        # 패킷을 시간 순으로 병합
        all_packets = []
        for p in packets_a_to_b:
            all_packets.append((p, 'A_to_B'))
        for p in packets_b_to_a:
            all_packets.append((p, 'B_to_A'))

        all_packets.sort(key=lambda x: x[0].arrival_time)

        for pkt, direction in all_packets:
            # 간소화된 충돌 시뮬레이션
            if current_direction is not None and current_direction != direction:
                # 방향 전환 필요 - 백오프 시뮬레이션
                backoff = np.random.uniform(0.001, 0.01)  # 1-10ms 백오프
                current_time += backoff

            # 충돌 확률 (단순화)
            if np.random.random() < 0.05:  # 5% 충돌 확률
                pkt.collision = True
                self.collisions += 1
                # 재전송 시뮬레이션
                current_time += np.random.uniform(0.01, 0.05)
                transmission_duration = pkt.size_bits / self.bandwidth
                pkt.transmission_time = current_time + transmission_duration
            else:
                transmission_duration = pkt.size_bits / self.bandwidth
                pkt.transmission_time = max(current_time, pkt.arrival_time) + transmission_duration

            current_time = pkt.transmission_time
            current_direction = direction

            if direction == 'A_to_B':
                transmitted_a.append(pkt)
            else:
                transmitted_b.append(pkt)

        total_bits = sum(p.size_bits for p in transmitted_a + transmitted_b)
        efficiency = total_bits / (current_time * self.bandwidth) if current_time > 0 else 0

        return {
            'mode': 'Half-Duplex',
            'packets_a_to_b': len(transmitted_a),
            'packets_b_to_a': len(transmitted_b),
            'total_time': current_time,
            'throughput_bps': total_bits / current_time if current_time > 0 else 0,
            'collisions': self.collisions,
            'efficiency': efficiency
        }

    def simulate_full_duplex(self, packets_a_to_b: List[Packet],
                            packets_b_to_a: List[Packet]) -> dict:
        """전이중 전송 시뮬레이션"""
        # 양 방향 독립적으로 처리
        time_a = self._process_packets(packets_a_to_b)
        time_b = self._process_packets(packets_b_to_a)

        total_time = max(time_a, time_b)
        total_bits = (sum(p.size_bits for p in packets_a_to_b) +
                     sum(p.size_bits for p in packets_b_to_a))

        # 이론적 대역폭 활용률
        effective_bandwidth = total_bits / total_time if total_time > 0 else 0
        efficiency = effective_bandwidth / (2 * self.bandwidth)  # 2배 대역폭 기준

        return {
            'mode': 'Full-Duplex',
            'packets_a_to_b': len(packets_a_to_b),
            'packets_b_to_a': len(packets_b_to_a),
            'total_time': total_time,
            'throughput_bps': total_bits / total_time if total_time > 0 else 0,
            'collisions': 0,
            'efficiency': min(efficiency, 1.0),
            'direction_a_time': time_a,
            'direction_b_time': time_b
        }

    def _process_packets(self, packets: List[Packet]) -> float:
        """단일 방향 패킷 처리"""
        current_time = 0.0
        for pkt in packets:
            transmission_duration = pkt.size_bits / self.bandwidth
            start_time = max(current_time, pkt.arrival_time)
            pkt.transmission_time = start_time + transmission_duration
            current_time = pkt.transmission_time
        return current_time


def compare_modes():
    """전송 모드 비교 시뮬레이션"""
    print("=" * 70)
    print("전송 모드 성능 비교 시뮬레이션")
    print("=" * 70)

    # 파라미터 설정
    bandwidth = 100e6  # 100 Mbps
    num_packets = 100
    packet_size = 1500 * 8  # 1500 bytes = 12000 bits

    # 패킷 생성
    packets_a_to_b = [
        Packet(id=i, source=0, destination=1,
               size_bits=packet_size, arrival_time=i * 0.001)
        for i in range(num_packets)
    ]
    packets_b_to_a = [
        Packet(id=i+num_packets, source=1, destination=0,
               size_bits=packet_size, arrival_time=i * 0.001 + 0.0005)
        for i in range(num_packets)
    ]

    # Simplex 시뮬레이션
    sim_simplex = ChannelSimulator(bandwidth, TransmissionMode.SIMPLEX)
    result_simplex = sim_simplex.simulate_simplex(packets_a_to_b)

    # Half-Duplex 시뮬레이션
    sim_half = ChannelSimulator(bandwidth, TransmissionMode.HALF_DUPLEX)
    result_half = sim_half.simulate_half_duplex(packets_a_to_b, packets_b_to_a)

    # Full-Duplex 시뮬레이션
    sim_full = ChannelSimulator(bandwidth, TransmissionMode.FULL_DUPLEX)
    result_full = sim_full.simulate_full_duplex(packets_a_to_b, packets_b_to_a)

    # 결과 출력
    print(f"\n{'Mode':<15} {'Packets':<12} {'Time(s)':<12} {'Throughput':<15} {'Efficiency':<12}")
    print("-" * 70)

    for result in [result_simplex, result_half, result_full]:
        if result['mode'] == 'Simplex':
            packets = result['packets_sent']
        else:
            packets = result['packets_a_to_b'] + result['packets_b_to_a']

        print(f"{result['mode']:<15} {packets:<12} "
              f"{result['total_time']:<12.4f} "
              f"{result['throughput_bps']/1e6:<15.2f} Mbps "
              f"{result['efficiency']*100:<12.1f}%")

    print("\n[분석]")
    print(f"  Half-Duplex 충돌: {result_half['collisions']}회")
    print(f"  Full-Duplex 이론적 용량: {2*bandwidth/1e6:.0f} Mbps (양방향 합)")
    print(f"  Full-Duplex 실제 처리량: {result_full['throughput_bps']/1e6:.2f} Mbps")


if __name__ == "__main__":
    compare_modes()
