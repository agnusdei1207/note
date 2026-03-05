+++
title = "무선 LAN (Wi-Fi) 아키텍처"
date = 2024-05-18
description = "IEEE 802.11 무선 LAN 표준, Wi-Fi 4/5/6/7 진화, CSMA/CA, WPA 보안, MIMO/OFDMA 기술의 심층 분석"
weight = 40
[taxonomies]
categories = ["studynotes-03_network"]
tags = ["WiFi", "WirelessLAN", "IEEE802.11", "CSMA/CA", "MIMO", "OFDMA", "WPA3"]
+++

# 무선 LAN (Wi-Fi) 아키텍처

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Wi-Fi(IEEE 802.11)는 무선 주파수(ISM 대역 2.4GHz/5GHz/6GHz)를 사용하여 이더넷과 동등한 수준의 MAC 계층 서비스를 제공하는 무선 근거리 통신망(WLAN) 기술입니다.
> 2. **가치**: Wi-Fi 6(802.11ax)은 OFDMA, MU-MIMO, TWT를 도입하여 밀집 환경에서 4배 향상된 처리량과 67% 개선된 전력 효율을 달성하여, IoT와 고밀도 공공장소의 연결성을 혁신했습니다.
> 3. **융합**: Wi-Fi 7(802.11be)은 320MHz 채널, 4K-QAM, MLO(Multi-Link Operation)를 통해 46Gbps 초고속 전송과 5ms 이하의 초저지연을 실현하여 AR/VR, 메타버스, 산업용 IoT의 핵심 인프라로 진화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

Wi-Fi는 1997년 IEEE 802.11 원본 표준을 시작으로, 25년 이상 지속적으로 진화해 왔습니다. 오늘날 전 세계 수십억 대의 디바이스가 Wi-Fi를 사용하며, 가정, 사무실, 공공장소의 필수 인프라가 되었습니다.

**💡 비유**: Wi-Fi는 **'무선 도로망'**과 같습니다.
- **ISM 대역(2.4/5/6GHz)**: 누구나 무료로 사용할 수 있는 공공 도로
- **AP(Access Point)**: 교통 신호등과 IC(Interchange)
- **CSMA/CA**: "먼저 말하세요" 규칙 - 누군가 말하고 있으면 기다렸다가 조용해지면 말합니다
- **채널(Channel)**: 도로의 차선 - 같은 차선을 쓰면 충돌 위험
- **MIMO**: 다차선 도로 - 여러 차량이 동시에 주행

**등장 배경 및 발전 과정**:
1. **케이블의 구속에서 해방**: 유선 이더넷은 이동성이 제한되어, 노트북과 모바일 기기의 보급과 함께 무선 연결의 필요성이 폭증했습니다.
2. **표준화의 혼란과 통일**: 초기에는 HomeRF, HiperLAN 등 경쟁 표준이 존재했으나, Wi-Fi Alliance의 상호 운용성 인증 프로그램이 802.11을 사실상 표준으로 확립했습니다.
3. **지속적 성능 향상**: 2Mbps(802.11) → 11Mbps(802.11b) → 54Mbps(802.11a/g) → 600Mbps(802.11n) → 6.9Gbps(802.11ac) → 9.6Gbps(802.11ax) → 46Gbps(802.11be)

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: IEEE 802.11 표준 진화

| 표준 | 연도 | 주파수 | 최대 속도 | 대역폭 | 변조 | MIMO | 핵심 기술 |
|------|------|--------|----------|--------|------|------|----------|
| **802.11b** | 1999 | 2.4GHz | 11Mbps | 20MHz | CCK | 1×1 | DSSS |
| **802.11a** | 1999 | 5GHz | 54Mbps | 20MHz | 64-QAM | 1×1 | OFDM |
| **802.11g** | 2003 | 2.4GHz | 54Mbps | 20MHz | 64-QAM | 1×1 | OFDM |
| **802.11n (Wi-Fi 4)** | 2009 | 2.4/5GHz | 600Mbps | 40MHz | 64-QAM | 4×4 | MIMO, 채널 결합 |
| **802.11ac (Wi-Fi 5)** | 2014 | 5GHz | 6.9Gbps | 160MHz | 256-QAM | 8×8 | MU-MIMO(DL) |
| **802.11ax (Wi-Fi 6)** | 2020 | 2.4/5/6GHz | 9.6Gbps | 160MHz | 1024-QAM | 8×8 | OFDMA, MU-MIMO, TWT |
| **802.11be (Wi-Fi 7)** | 2024 | 2.4/5/6GHz | 46Gbps | 320MHz | 4096-QAM | 16×16 | MLO, MRU |

### 정교한 구조 다이어그램: 무선 LAN 아키텍처

```ascii
================================================================================
[ Wireless LAN Architecture - Infrastructure Mode ]
================================================================================

                    [ Distribution System (DS) - 유선 백본 ]
                              |
           +------------------+------------------+
           |                  |                  |
    +------+------+    +------+------+    +------+------+
    |   AP 1      |    |   AP 2      |    |   AP 3      |
    | (Access     |    | (Access     |    | (Access     |
    |  Point)     |    |  Point)     |    |  Point)     |
    |  BSSID:     |    |  BSSID:     |    |  BSSID:     |
    |  AA:BB:CC:  |    |  AA:BB:CC:  |    |  AA:BB:CC:  |
    |  11:11:11   |    |  11:11:12   |    |  11:11:13   |
    +------+------+    +------+------+    +------+------+
           |                  |                  |
           | Wireless         | Wireless         | Wireless
           | Coverage         | Coverage         | Coverage
           | Cell 1           | Cell 2           | Cell 3
           |                  |                  |
    +------+------+    +------+------+    +------+------+
    |  Station    |    |  Station    |    |  Station    |
    |  (STA 1)    |    |  (STA 2)    |    |  (STA 3)    |
    |  Smartphone |    |  Laptop     |    |  IoT Device |
    +-------------+    +-------------+    +-------------+

    ESS (Extended Service Set) = BSS 1 + BSS 2 + BSS 3 + DS

================================================================================
[ 802.11 Frame Format ]
================================================================================

+-----------------------------------------------------------------------+
| Frame Control (2B) | Duration/ID (2B) | Address 1 (6B) | Address 2 (6B) |
+-----------------------------------------------------------------------+
| Address 3 (6B) | Seq Control (2B) | Address 4 (6B, optional)         |
+-----------------------------------------------------------------------+
|                   Frame Body (0~2312 Bytes)                           |
+-----------------------------------------------------------------------+
|                   FCS (Frame Check Sequence, 4B)                      |
+-----------------------------------------------------------------------+

Frame Control 필드 상세:
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
|Ver  |Type |Type |Sub  |Sub  |Sub  |To   |From |More |Retry|Pwr  |More |WEP  |Order|
|     |(b1) |(b2) |Type |Type |Type |DS   |DS   |Frag |     |Mgt  |Data |     |     |
|(2b) |     |     |(b1) |(b2) |(b3) |     |     |     |     |     |     |     |     |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+

주소 필드 용도 (ToDS/FromDS에 따라):
+--------+----------+----------+----------+----------+
|ToDS    | FromDS   | Addr 1   | Addr 2   | Addr 3   |
+--------+----------+----------+----------+----------+
|   0    |    0     | DA       | SA       | BSSID    | (IBSS)
|   0    |    1     | DA       | BSSID    | SA       | (From AP)
|   1    |    0     | BSSID    | SA       | DA       | (To AP)
|   1    |    1     | RA       | TA       | DA       | (WDS)
+--------+----------+----------+----------+----------+

================================================================================
[ CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance) ]
================================================================================

송신측 (Transmitter):
+------------------+
|  Data to Send?   |
+--------|---------+
         | Yes
         v
+--------|---------+
| Channel Idle     |<------------------+
| for DIFS?        |                   |
+--------|---------+                   |
         | Yes                       No
         v                            |
+--------|---------+                  |
| Random Backoff   |                  |
| (Contention Win) |                  |
+--------|---------+                  |
         |                           |
         v                           |
+--------|---------+                  |
| Channel Still     |-------No------->+
| Idle?             |
+--------|---------+
         | Yes
         v
+--------|---------+
| Send RTS Frame   | (Optional - Hidden Terminal 대응)
+--------|---------+
         |
         v
+--------|---------+
| Wait for CTS     |
+--------|---------+
         | CTS Received
         v
+--------|---------+
| Send Data Frame  |
+--------|---------+
         |
         v
+--------|---------+
| Wait for ACK     |
+--------|---------+
         | ACK Received
         v
+--------|---------+
|    Success!      |
+------------------+


수신측 (Receiver):
+------------------+     +------------------+
| Receive RTS      |     | Receive Data     |
+--------|---------+     +--------|---------+
         |                        |
         v                        v
+--------|---------+     +--------|---------+
| Wait SIFS       |     | Wait SIFS        |
+--------|---------+     +--------|---------+
         |                        |
         v                        v
+--------|---------+     +--------|---------+
| Send CTS        |     | Send ACK         |
+------------------+     +------------------+

RTS/CTS 메커니즘 (은닉 노드 문제 해결):
+-------------+                    +-------------+                    +-------------+
|   Node A    |                    |    AP       |                    |   Node B    |
| (Hidden     |                    |             |                    | (Hidden     |
|  from B)    |                    |             |                    |  from A)    |
+------+------+                    +------+------+                    +------+------+
       |                                  |                                  |
       |------------ RTS --------------->|                                  |
       |                                  |<---------- RTS ----------------|
       |                                  |                                  |
       |<----------- CTS ----------------|                                  |
       |                                  |------------ CTS --------------->|
       |                                  |                                  |
       |========== DATA =================>|                                  |
       |                                  |<=============== DATA ===========|
       |                                  |                                  |
       |<---------- ACK -----------------|                                  |
       |                                  |------------ ACK ---------------->|

================================================================================
[ OFDMA (Orthogonal Frequency Division Multiple Access) - Wi-Fi 6 ]
================================================================================

주파수 ↑
        |  RU1 |  RU2  |  RU3  |  RU4  |  RU5  |  RU6  |
        |(User1)|(User2)|(User3)|(User4)|(User5)|(User6)|
        | 26톤 | 26톤  | 26톤  | 52톤  | 106톤 | 26톤  |
        |      |       |       |       |       |       |
        |======|=======|=======|=======|=======|=======|  하나의 전송 기회(TXOP)
        |      |       |       |       |       |       |  여러 사용자 동시 전송
        |      |       |       |       |       |       |
        |__________________________________________________→ 시간

RU (Resource Unit) 크기:
- 26-subcarrier RU: 2Mbps~10Mbps (IoT, 낮은 대역폭)
- 52-subcarrier RU: 5Mbps~20Mbps
- 106-subcarrier RU: 10Mbps~40Mbps
- 242-subcarrier RU: 20MHz (기존 Wi-Fi 채널)
- 484-subcarrier RU: 40MHz
- 996-subcarrier RU: 80MHz
- 2x996-subcarrier RU: 160MHz

================================================================================
```

### 심층 동작 원리: 핵심 기술 분석

#### 1. CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance)

무선 환경에서는 유선과 달리 충돌 감지(Collision Detection)가 어렵습니다:
- **Half-Duplex 제약**: 송신 중에는 동시에 수신할 수 없어 자신의 신호와 충돌을 감지 불가
- **은닉 노드(Hidden Terminal) 문제**: A와 C가 서로 범위 밖에 있지만 AP는 중간에 있어 충돌 발생

**CSMA/CA 해결책**:
1. **이진 지수 백오프(Binary Exponential Backoff)**:
   ```
   초기 CW (Contention Window) = CWmin = 15
   충돌 시 CW = min(2 × CW + 1, CWmax)  // CWmax = 1023
   무작위 대기 시간 = random(0, CW) × Slot Time
   ```

2. **RTS/CTS (Request to Send / Clear to Send)**:
   - RTS: 송신 의사를 알리는 작은 프레임
   - CTS: 수신 가능을 알리는 응답
   - NAV (Network Allocation Vector): 다른 기기들이 채널을 예약된 시간 동안 사용하지 않도록 설정

#### 2. MIMO (Multiple-Input Multiple-Output)

**공간 다중화(Spatial Multiplexing)**:
```
단일 안테나 (SISO):
  Throughput = B × log2(1 + SNR)

MIMO (N×N):
  Throughput = N × B × log2(1 + SNR/N)

  // 이론적으로 안테나 수 N배 증가
```

**MU-MIMO (Multi-User MIMO) - Wi-Fi 5/6**:
- 다운링크: AP가 여러 기기에 동시에 다른 데이터 스트림 전송
- 업링크(Wi-Fi 6): 여러 기기가 동시에 AP로 전송 (UL MU-MIMO)

#### 3. OFDMA (Orthogonal Frequency Division Multiple Access) - Wi-Fi 6

**핵심 원리**:
- 20MHz 채널을 256개의 부반송파(subcarrier)로 분할
- 각 부반송파 그룹(RU, Resource Unit)을 다른 사용자에게 할당
- 직교성으로 인해 간섭 없이 주파수 영역 다중화

**이점**:
- 대기 시간 감소: 작은 데이터도 전체 채널을 기다릴 필요 없음
- 효율성 향상: 유휴 부반송파 활용

### 핵심 코드: Wi-Fi 성능 시뮬레이터 (Python)

```python
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum

class WiFiStandard(Enum):
    WIFI_4 = "802.11n (Wi-Fi 4)"
    WIFI_5 = "802.11ac (Wi-Fi 5)"
    WIFI_6 = "802.11ax (Wi-Fi 6)"
    WIFI_7 = "802.11be (Wi-Fi 7)"

@dataclass
class WiFiConfig:
    """Wi-Fi 구성 파라미터"""
    standard: WiFiStandard
    bandwidth_mhz: int  # 20, 40, 80, 160, 320
    mcs_index: int  # Modulation and Coding Scheme
    nss: int  # Number of Spatial Streams
    guard_interval_ns: int  # 400, 800, 1600, 3200

class WiFiThroughputCalculator:
    """
    Wi-Fi 처리량 계산기

    IEEE 802.11 표준 기반 이론적 최대 속도 계산
    """

    # MCS 테이블 (간소화)
    MCS_TABLE = {
        # (변조, 코드율, 비트/심볼)
        0: ('BPSK', 1/2, 1),
        1: ('QPSK', 1/2, 2),
        2: ('QPSK', 3/4, 2),
        3: ('16-QAM', 1/2, 4),
        4: ('16-QAM', 3/4, 4),
        5: ('64-QAM', 2/3, 6),
        6: ('64-QAM', 3/4, 6),
        7: ('64-QAM', 5/6, 6),
        8: ('256-QAM', 3/4, 8),
        9: ('256-QAM', 5/6, 8),
        10: ('1024-QAM', 3/4, 10),
        11: ('1024-QAM', 5/6, 10),
        12: ('4096-QAM', 3/4, 12),
        13: ('4096-QAM', 5/6, 12),
    }

    def __init__(self, config: WiFiConfig):
        self.config = config

    def calculate_ofdm_symbols_per_second(self) -> float:
        """OFDM 심볼 전송 속도 계산"""
        # 부반송파 수 (대역폭에 따라)
        subcarriers = {
            20: 64,
            40: 128,
            80: 256,
            160: 512,
            320: 1024
        }
        n_subcarriers = subcarriers.get(self.config.bandwidth_mhz, 64)

        # 데이터 부반송파 수 (파일럿, DC 제외)
        data_subcarriers = int(n_subcarriers * 0.8)  # 약 80%

        # 심볼 지속 시간
        symbol_time_us = 3.2 + self.config.guard_interval_ns / 1000  # μs

        # 초당 심볼 수
        symbols_per_sec = 1e6 / symbol_time_us

        return symbols_per_sec, data_subcarriers

    def calculate_theoretical_throughput(self) -> float:
        """이론적 최대 처리량 계산 (Mbps)"""
        # MCS 정보
        modulation, code_rate, bits_per_symbol = self.MCS_TABLE.get(
            self.config.mcs_index, ('64-QAM', 3/4, 6)
        )

        symbols_per_sec, data_subcarriers = self.calculate_ofdm_symbols_per_second()

        # 처리량 계산
        # Throughput = 심볼/초 × 데이터 부반송파 × 비트/심볼 × 코드율 × 공간 스트림
        throughput_mbps = (
            symbols_per_sec *
            data_subcarriers *
            bits_per_symbol *
            code_rate *
            self.config.nss
        ) / 1e6

        return throughput_mbps

    def calculate_effective_throughput(self, efficiency: float = 0.65) -> float:
        """
        실질적 처리량 계산

        Args:
            efficiency: 프로토콜 오버헤드, 간섭 등을 고려한 효율 (일반적으로 50~70%)
        """
        return self.calculate_theoretical_throughput() * efficiency


class CSMACASimulator:
    """
    CSMA/CA 시뮬레이터

    무선 채널 경쟁 및 백오프 알고리즘 시뮬레이션
    """

    def __init__(self, n_stations: int, cw_min: int = 15, cw_max: int = 1023):
        self.n_stations = n_stations
        self.cw_min = cw_min
        self.cw_max = cw_max
        self.slot_time_us = 9  # 802.11n/ac
        self.difs_us = 34  # DCF Interframe Space
        self.sifs_us = 16  # Short Interframe Space

    def simulate_transmission(self, n_attempts: int = 1000) -> dict:
        """
        전송 시도 시뮬레이션

        Returns:
            충돌률, 평균 백오프, 처리율 등
        """
        collisions = 0
        successful = 0
        total_backoff_slots = 0

        cw_values = [self.cw_min] * self.n_stations

        for attempt in range(n_attempts):
            # 각 스테이션의 백오프 값 생성
            backoffs = [np.random.randint(0, cw + 1) for cw in cw_values]
            min_backoff = min(backoffs)
            min_count = backoffs.count(min_backoff)

            total_backoff_slots += min_backoff

            if min_count > 1:
                # 충돌 발생
                collisions += 1
                # 충돌한 스테이션들의 CW 증가
                for i, bo in enumerate(backoffs):
                    if bo == min_backoff:
                        cw_values[i] = min(cw_values[i] * 2 + 1, self.cw_max)
            else:
                # 성공
                successful += 1
                # 성공한 스테이션의 CW 초기화
                winner_idx = backoffs.index(min_backoff)
                cw_values[winner_idx] = self.cw_min

        return {
            'collision_rate': collisions / n_attempts,
            'success_rate': successful / n_attempts,
            'avg_backoff_slots': total_backoff_slots / n_attempts,
            'avg_backoff_us': (total_backoff_slots / n_attempts) * self.slot_time_us
        }


class OFDMAAllocator:
    """
    OFDMA RU 할당 시뮬레이터 (Wi-Fi 6)
    """

    RU_SIZES = {
        26: 26,    # 26톤 RU (최소)
        52: 52,
        106: 106,
        242: 242,  # 20MHz
        484: 484,  # 40MHz
        996: 996,  # 80MHz
        1992: 1992 # 160MHz
    }

    def __init__(self, total_bandwidth_mhz: int = 80):
        self.bandwidth = total_bandwidth_mhz
        # 80MHz = 996개의 데이터 부반송파 (256톤 × 4 - 파일럿)
        self.total_subcarriers = {
            20: 234,
            40: 468,
            80: 936,
            160: 1872
        }.get(total_bandwidth_mhz, 936)

    def allocate_rus(self, user_demands: List[int]) -> List[Tuple[int, int]]:
        """
        사용자 요구에 따른 RU 할당

        Args:
            user_demands: 각 사용자의 대역폭 요구 (상대적 비율)

        Returns:
            [(user_id, ru_size), ...] 할당 결과
        """
        total_demand = sum(user_demands)
        allocations = []
        remaining = self.total_subcarriers

        for user_id, demand in enumerate(user_demands):
            # 요구 비율에 따른 부반송파 할당
            allocated = int((demand / total_demand) * self.total_subcarriers)

            # 가장 근접한 RU 크기로 매핑
            ru_size = min(self.RU_SIZES.values(), key=lambda x: abs(x - allocated))
            ru_size = min(ru_size, remaining)

            allocations.append((user_id, ru_size))
            remaining -= ru_size

        return allocations

    def calculate_ofdma_efficiency(self, allocations: List[Tuple[int, int]]) -> float:
        """OFDMA 대역폭 활용 효율 계산"""
        used = sum(ru for _, ru in allocations)
        return used / self.total_subcarriers


# ================== 시뮬레이션 실행 ==================
if __name__ == "__main__":
    print("=" * 70)
    print("Wi-Fi Performance Simulation Report")
    print("=" * 70)

    # 1. 처리량 계산
    print("\n[1. Throughput Calculation]")

    configs = [
        WiFiConfig(WiFiStandard.WIFI_4, 40, 7, 2, 400),
        WiFiConfig(WiFiStandard.WIFI_5, 80, 9, 3, 400),
        WiFiConfig(WiFiStandard.WIFI_6, 160, 11, 4, 800),
        WiFiConfig(WiFiStandard.WIFI_7, 320, 13, 8, 800),
    ]

    for config in configs:
        calc = WiFiThroughputCalculator(config)
        theoretical = calc.calculate_theoretical_throughput()
        effective = calc.calculate_effective_throughput(0.65)

        print(f"\n{config.standard.value}")
        print(f"  Bandwidth: {config.bandwidth_mhz}MHz")
        print(f"  Spatial Streams: {config.nss}")
        print(f"  Theoretical: {theoretical:.1f} Mbps")
        print(f"  Effective (65%): {effective:.1f} Mbps")

    # 2. CSMA/CA 시뮬레이션
    print("\n[2. CSMA/CA Simulation]")

    for n_sta in [5, 10, 20, 50]:
        sim = CSMACASimulator(n_stations=n_sta)
        result = sim.simulate_transmission(10000)
        print(f"\nStations: {n_sta}")
        print(f"  Collision Rate: {result['collision_rate']*100:.1f}%")
        print(f"  Avg Backoff: {result['avg_backoff_us']:.1f} μs")

    # 3. OFDMA 할당
    print("\n[3. OFDMA RU Allocation (Wi-Fi 6, 80MHz)]")

    allocator = OFDMAAllocator(80)

    # 6명의 사용자, 각각 다른 대역폭 요구
    demands = [10, 20, 30, 15, 10, 15]  # 비디오, 음성, 데이터 등
    allocations = allocator.allocate_rus(demands)
    efficiency = allocator.calculate_ofdma_efficiency(allocations)

    print(f"User demands: {demands}")
    print(f"Allocations (User ID, RU size): {allocations}")
    print(f"Bandwidth Efficiency: {efficiency*100:.1f}%")

    print(f"\n{'='*70}")
