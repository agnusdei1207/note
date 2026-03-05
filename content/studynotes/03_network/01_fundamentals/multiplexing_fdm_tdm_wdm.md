+++
title = "다중화 기술 (Multiplexing: FDM, TDM, WDM)"
date = 2024-05-18
description = "통신 자원의 효율적 공유를 위한 다중화 기술의 심층 분석 - 주파수 분할(FDM), 시분할(TDM), 파장 분할(WDM)의 원리와 실무 적용"
weight = 25
[taxonomies]
categories = ["studynotes-network"]
tags = ["Multiplexing", "FDM", "TDM", "WDM", "CDM", "Bandwidth"]
+++

# 다중화 기술 (Multiplexing: FDM, TDM, WDM)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 다중화(Multiplexing)는 단일 전송 매체를 통해 다수의 독립적인 신호를 동시에 전송하는 기술로, 주파수(FDM), 시간(TDM), 파장(WDM), 코드(CDM) 등의 직교 자원을 분할하여 통신 자원의 활용 효율을 극대화합니다.
> 2. **가치**: 다중화는 통신 인프라 구축 비용을 50~80% 절감하며, 현대의 광통신(DWDM 80파장 이상), 이동통신(OFDMA), 위성 통신의 핵심 기반 기술입니다.
> 3. **융합**: 5G NR의 OFDMA는 FDM+TDM 융합, GPON은 TDM+WDM 결합 등 현대 통신은 하이브리드 다중화가 표준이며, SDN/NFV와 결합한 동적 자원 할당이 진화 방향입니다.

---

## Ⅰ. 개요 (Context & Background)

다중화(Multiplexing)는 N개의 입력 신호를 하나의 전송 매체(케이블, 광섬유, 무선 채널)를 통해 전송하고, 수신측에서 이를 다시 N개의 원래 신호로 분리하는 기술입니다. 이는 통신 자원(대역폭, 시간, 공간, 코드)을 효율적으로 공유하여 단위 비용당 전송 용량을 극대화하는 것이 핵심 목표입니다.

**💡 비유**: 다중화는 **'고속도로의 차선 분리'**와 같습니다. 1차선 도로를 4차선으로 확장하면 4배의 차량이 동시에 통과할 수 있습니다. FDM은 각 차선을 주파수별로 나누는 것, TDM은 시간대별로 차량을 번갈아 보내는 것, WDM은 다른 색깔의 차량을 보내는 것(광통신에서)에 비유할 수 있습니다.

**등장 배경 및 발전 과정**:
1. **기존 기술의 치명적 한계점**: 초기 통신 시스템은 하나의 통신 회선이 하나의 통화만 지원했습니다. 예를 들어, 1920년대 장거리 전화는 하나의 구리선 쌍으로 단 하나의 통화만 가능하여, 통신 비용이 천문학적이었습니다.
2. **혁신적 패러다임 변화**: 1910년대 캐리어 시스템(Carrier System)으로 FDM이 도입되면서 하나의 케이블로 12~60회선 동시 지원이 가능해졌습니다. 이후 1960년대 디지털 T1(1.544 Mbps, 24채널), 1990년대 DWDM(초기 8~16파장)으로 급격히 발전했습니다.
3. **비즈니스적 요구사항**: 현대 데이터센터 간 연결, 5G 백홀, 초고속 인터넷 가입자망 등에서는 Tbps급 트래픽을 처리해야 하며, 이는 다중화 기술 없이는 경제적으로 불가능합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: 다중화 기술 분류 체계

```
                        다중화 (Multiplexing)
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
    ┌────┴────┐         ┌────┴────┐         ┌────┴────┐
    │  아날로그 │         │  디지털  │         │  광학적  │
    │   다중화 │         │  다중화  │         │  다중화  │
    └────┬────┘         └────┬────┘         └────┬────┘
         │                   │                   │
    ┌────┴────┐         ┌────┴────┐         ┌────┴────┐
    │   FDM   │         │ 동기 TDM │         │   WDM   │
    │ (주파수)│         │  (시간)  │         │ (파장)  │
    └─────────┘         └────┬────┘         └────┬────┘
                             │                   │
                        ┌────┴────┐         ┌────┴────┐
                        │ 비동기  │         │  CWDM   │
                        │  TDM    │         │(저밀도) │
                        │(통계적) │         └────┬────┘
                        └─────────┘              │
                                             ┌────┴────┐
                                             │  DWDM   │
                                             │(고밀도) │
                                             └─────────┘
```

### 주요 다중화 방식 상세 비교

| 특성 | FDM (Frequency Division) | TDM (Time Division) | WDM (Wavelength Division) | CDM (Code Division) |
|---|---|---|---|---|
| **분할 자원** | 주파수 대역 | 시간 슬롯 | 광파장(λ) | 직교 코드 |
| **전송 매체** | 구리선, 무선 | 구리선, 광섬유 | 광섬유 | 무선, 광섬유 |
| **채널 간 간섭** | 보호대역(Guard Band) 필요 | 보호시간(Guard Time) 필요 | 채널 간격 관리 | 코드 직교성 유지 |
| **대역폭 효율** | 중간 | 높음 | 매우 높음 | 높음 |
| **동기화 필요** | 없음 | 필수 | 없음 | 필수 |
| **주요 적용** | 라디오 방송, ADSL | T1/E1, SONET/SDH | 광통신 백본 | CDMA, 3G |
| **복잡도** | 낮음 | 중간 | 높음 | 높음 |

### 정교한 구조 다이어그램: FDM vs TDM vs WDM

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FDM (주파수 분할 다중화)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   입력 채널                    주파수 스펙트럼                    출력 채널   │
│   ┌─────┐                                                         ┌─────┐   │
│   │ Ch1 │──→ ┌─────────┐     f1 │███│      ┌─────────┐──→         │ Ch1 │   │
│   └─────┘    │         │         │   │ GB   │         │            └─────┘   │
│   ┌─────┐    │   MUX   │     f2  │███│      │  DEMUX  │──→ ┌─────┐           │
│   │ Ch2 │──→ │(변조+혼합)│         │   │      │(필터링) │    │ Ch2 │           │
│   └─────┘    │         │     f3  │███│      │         │    └─────┘           │
│   ┌─────┐    │         │         │   │      │         │                        │
│   │ Ch3 │──→ └─────────┘     f4  │███│      └─────────┘                        │
│   └─────┘                         └───┘                                      │
│                                   ↑                                          │
│                              보호 대역(Guard Band)                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           TDM (시분할 다중화)                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   시간 축 →                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ Ch1 │ Ch2 │ Ch3 │ Ch4 │ Ch1 │ Ch2 │ Ch3 │ Ch4 │ Ch1 │ Ch2 │...   │   │
│   ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┤   │
│   │  TS1 │ TS2 │ TS3 │ TS4 │ TS1 │ TS2 │ TS3 │ TS4 │ TS1 │ TS2 │ ...  │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│         ↑              ↑                                                    │
│       프레임 시작    하나의 TDM 프레임 (125μs for E1)                       │
│                                                                             │
│   특징: 각 채널은 고정된 타임슬롯에 할당, 클럭 동기화 필수                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           WDM (파장 분할 다중화)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   광섬유 단면                                                                │
│       ╭────────╮                                                            │
│      ╱  Core    ╲←── λ1 (1310nm): Data Ch1                                  │
│     │  (9~50μm)  │←── λ2 (1490nm): Data Ch2                                 │
│     │            │←── λ3 (1550nm): Data Ch3                                 │
│      ╲          ╱←── λ4 (1550.8nm): Data Ch4                                │
│       ╰────────╯    ... (DWDM: 최대 160파장까지)                            │
│                                                                             │
│   파장 분포 (C-Band DWDM)                                                   │
│   ┌────────────────────────────────────────────────────────────────────┐    │
│   │ λ1  λ2  λ3  λ4  λ5  ...  λ40  (간격: 0.8nm = 100GHz)              │    │
│   │ ██  ██  ██  ██  ██  ...  ██                                       │    │
│   │ 1530nm              →              1565nm                         │    │
│   └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│   핵심 구성요소: MUX/DEMUX (AWG), OADM, EDFA (광증폭기)                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

**1. FDM (Frequency Division Multiplexing)**

FDM은 사용 가능한 전체 대역폭을 여러 개의 비중첩 주파수 대역으로 나누어 각 채널에 할당합니다.

```
동작 과정:
① 각 입력 신호를 서로 다른 반송 주파수(fc1, fc2, fc3...)로 변조
② 변조된 신호들을 혼합(Mixing)하여 하나의 복합 신호 생성
③ 전송 매체를 통해 복합 신호 전송
④ 수신측에서 대역통과 필터(BPF)로 각 주파수 대역 분리
⑤ 각 채널을 복조(Demodulation)하여 원 신호 복원

수학적 표현:
s(t) = Σ s_i(t) × cos(2πf_i × t)  [i = 1 to N]

보호 대역(Guard Band):
- 인접 채널 간 간섭을 방지하기 위한 미사용 주파수 영역
- 일반적으로 채널 대역폭의 10~20%
```

**2. TDM (Time Division Multiplexing)**

TDM은 전송 시간을 고정된 크기의 타임슬롯(Time Slot)으로 나누어 각 채널에 순차적으로 할당합니다.

```
동기식 TDM (Synchronous TDM):
- 각 채널에 고정된 타임슬롯 할당 (활성/비활성 무관)
- 프레임 구조: [Sync | Ch1 | Ch2 | ... | ChN]
- E1 프레임: 32 타임슬롯 × 8비트 = 256비트/프레임, 8000프레임/초 = 2.048 Mbps

비동기식/통계적 TDM (Statistical TDM):
- 활성 채널에만 타임슬롯 동적 할당
- 채널 식별자(Address) 포함 필요
- 대역폭 효율 2~4배 향상, 버퍼링 복잡도 증가

T1 (DS1) 구조:
┌──────────────────────────────────────────────────────────────┐
│ Frame: [F | Ch1 | Ch2 | ... | Ch23 | Ch24] = 193 bits       │
│         ↑                                                    │
│       Framing bit (1bit)                                     │
│                                                              │
│ 각 채널: 8 bits × 24 channels = 192 bits + 1 = 193 bits     │
│ 전송률: 193 bits × 8000 frames/s = 1.544 Mbps               │
└──────────────────────────────────────────────────────────────┘
```

**3. WDM (Wavelength Division Multiplexing)**

WDM은 광섬유의 서로 다른 파장(λ)을 이용하여 다중 채널을 동시에 전송합니다.

```
CWDM (Coarse WDM):
- 파장 간격: 20nm
- 파장 수: 18개 (1270~1610nm)
- 거리: 최대 80km
- 적용: 도시권(Metro), 기업망

DWDM (Dense WDM):
- 파장 간격: 0.8nm (100GHz) ~ 0.4nm (50GHz)
- 파장 수: 40, 80, 160개 이상
- 거리: 수천 km (EDFA 증폭 활용)
- 적용: 장거리 백본, 해저 케이블

광 증폭기 EDFA (Erbium-Doped Fiber Amplifier):
- 1550nm 대역(C-Band) 증폭
- 모든 파장을 동시에 증폭 (투명성)
- 증폭 이득: 20~40 dB
- 잡음 지수: 4~6 dB
```

### 핵심 코드: TDM 프레임 구조 시뮬레이션 (Python)

```python
import numpy as np
from dataclasses import dataclass
from typing import List, Dict
import matplotlib.pyplot as plt

@dataclass
class TDMChannel:
    """TDM 채널 정의"""
    id: int
    name: str
    data_rate_bps: int
    slot_size_bits: int = 8

class TDMMultiplexer:
    """시분할 다중화 시뮬레이터"""

    def __init__(self, frame_rate: int = 8000):
        """
        Args:
            frame_rate: 초당 프레임 수 (음성: 8000)
        """
        self.frame_rate = frame_rate
        self.channels: List[TDMChannel] = []
        self.frame_format = 'E1'  # E1, T1, or custom

    def add_channel(self, channel: TDMChannel):
        """채널 추가"""
        self.channels.append(channel)

    def calculate_frame_structure(self) -> Dict:
        """프레임 구조 계산"""
        num_channels = len(self.channels)
        payload_bits = sum(ch.slot_size_bits for ch in self.channels)
        framing_bits = 1  # 기본 프레이밍 비트

        total_frame_bits = payload_bits + framing_bits
        total_bitrate = total_frame_bits * self.frame_rate

        return {
            'num_channels': num_channels,
            'payload_bits_per_frame': payload_bits,
            'framing_bits': framing_bits,
            'total_frame_bits': total_frame_bits,
            'frame_duration_us': 1e6 / self.frame_rate,
            'total_bitrate_mbps': total_bitrate / 1e6,
            'efficiency': payload_bits / total_frame_bits * 100
        }

    def generate_e1_frame(self) -> np.ndarray:
        """
        E1 프레임 생성 (2.048 Mbps)
        - 32 타임슬롯 (TS0~TS31)
        - TS0: 프레임 정렬, TS16: 신호
        - TS1~TS15, TS17~TS31: 음성 채널 (30채널)
        """
        frame = np.zeros(256, dtype=np.uint8)  # 32 slots × 8 bits

        # TS0: 프레임 정렬 신호 (FAS)
        frame[0:8] = [1, 0, 0, 1, 1, 0, 1, 1]  # International FAS

        # TS1~TS15, TS17~TS31: 음성 데이터 (시뮬레이션)
        for ts in range(1, 16):
            frame[ts*8:(ts+1)*8] = np.random.randint(0, 2, 8)
        for ts in range(17, 32):
            frame[ts*8:(ts+1)*8] = np.random.randint(0, 2, 8)

        # TS16: 신호 채널 (CAS 또는 CCS)
        frame[16*8:(16+1)*8] = [0, 0, 0, 0, 1, 1, 1, 1]  # 예시

        return frame

    def generate_t1_frame(self) -> np.ndarray:
        """
        T1 프레임 생성 (1.544 Mbps)
        - 24 채널 × 8 bits + 1 framing bit = 193 bits
        """
        frame = np.zeros(193, dtype=np.uint8)

        # Framing bit (F-bit)
        frame[0] = 1

        # 24 채널 데이터
        for ch in range(24):
            frame[1 + ch*8 : 1 + (ch+1)*8] = np.random.randint(0, 2, 8)

        return frame

    def multiplex_frames(self, num_frames: int = 10) -> np.ndarray:
        """다중 프레임 생성"""
        if self.frame_format == 'E1':
            frames = np.array([self.generate_e1_frame() for _ in range(num_frames)])
        else:
            frames = np.array([self.generate_t1_frame() for _ in range(num_frames)])
        return frames.flatten()

    def analyze_bandwidth_efficiency(self, active_channels: int) -> Dict:
        """
        대역폭 효율 분석 (동기식 vs 통계적 TDM)

        Args:
            active_channels: 실제 활성 채널 수
        """
        total_channels = len(self.channels)

        # 동기식 TDM: 항상 모든 슬롯 전송
        sync_efficiency = active_channels / total_channels * 100

        # 통계적 TDM: 활성 채널만 전송 (오버헤드 10% 가정)
        stat_efficiency = 90  # 활성 채널에 대한 효율
        stat_bandwidth_saving = (1 - active_channels / total_channels) * 100

        return {
            'sync_tdm_efficiency': sync_efficiency,
            'stat_tdm_efficiency': stat_efficiency,
            'stat_bandwidth_saving_percent': stat_bandwidth_saving,
            'active_ratio': f"{active_channels}/{total_channels}"
        }


class WDMSimulator:
    """파장 분할 다중화 시뮬레이터"""

    # ITU-T G.694.1 표준 DWDM 파장 그리드
    C_BAND_START = 1527.60  # nm
    C_BAND_END = 1565.50    # nm

    def __init__(self, channel_spacing_ghz: float = 100):
        """
        Args:
            channel_spacing_ghz: 채널 간격 (100, 50, 25 GHz)
        """
        self.channel_spacing = channel_spacing_ghz

    def calculate_wavelength_grid(self) -> List[float]:
        """DWDM 파장 그리드 계산"""
        c = 299792458  # 빛의 속도 (m/s)
        freq_start = c / (self.C_BAND_END * 1e-9)  # THz
        freq_end = c / (self.C_BAND_START * 1e-9)

        wavelengths = []
        freq = freq_start
        while freq <= freq_end:
            wavelength = c / freq * 1e9  # nm
            wavelengths.append(round(wavelength, 2))
            freq += self.channel_spacing * 1e9

        return wavelengths

    def calculate_channel_capacity(self, num_wavelengths: int,
                                    bitrate_per_lambda_gbps: float = 100) -> Dict:
        """전체 채널 용량 계산"""
        total_capacity = num_wavelengths * bitrate_per_lambda_gbps

        return {
            'num_wavelengths': num_wavelengths,
            'bitrate_per_lambda_gbps': bitrate_per_lambda_gbps,
            'total_capacity_gbps': total_capacity,
            'total_capacity_tbps': total_capacity / 1000,
            'fiber_type': 'SMF-28e+' if num_wavelengths <= 96 else 'Wideband'
        }


def main():
    """실행 예시"""
    print("=" * 60)
    print("다중화 기술 시뮬레이션")
    print("=" * 60)

    # TDM 분석
    tdm = TDMMultiplexer(frame_rate=8000)
    tdm.frame_format = 'E1'
    for i in range(30):
        tdm.add_channel(TDMChannel(i, f"Voice_{i}", 64000))

    print("\n[E1 TDM 구조 분석]")
    structure = tdm.calculate_frame_structure()
    for key, value in structure.items():
        print(f"  {key}: {value}")

    # WDM 분석
    print("\n[DWDM 파장 분석]")
    wdm = WDMSimulator(channel_spacing_ghz=100)
    wavelengths = wdm.calculate_wavelength_grid()
    print(f"  C-Band 파장 수: {len(wavelengths)}")
    print(f"  파장 범위: {wavelengths[0]}nm ~ {wavelengths[-1]}nm")

    capacity = wdm.calculate_channel_capacity(80, 100)
    print(f"\n  80파장 × 100Gbps 용량:")
    print(f"    총 용량: {capacity['total_capacity_tbps']:.1f} Tbps")


if __name__ == "__main__":
    main()
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교표: 다중화 방식별 성능 분석

| 성능 지표 | FDM | 동기 TDM | 비동기 TDM | CWDM | DWDM |
|---|---|---|---|---|---|
| **스펙트럼 효율 (bits/s/Hz)** | 0.5~2 | 1~4 | 2~8 | 0.1~0.5 | 1~10 |
| **지연 시간 (Latency)** | 낮음 | 중간 | 가변 | 낮음 | 낮음 |
| **동기화 요구** | 없음 | 필수 | 선택적 | 없음 | 없음 |
| **확장성** | 제한적 | 제한적 | 유연함 | 제한적 | 매우 유연 |
| **장비 비용** | 낮음 | 중간 | 중간 | 중간 | 높음 |
| **적용 거리** | km | km | km | ~80km | 수천 km |
| **전력 효율** | 중간 | 높음 | 높음 | 중간 | 중간 |

### 과목 융합 관점 분석

**1. 5G/6G 이동통신과의 융합 - OFDMA**
- OFDMA(Orthogonal Frequency Division Multiple Access)는 FDM + TDM의 하이브리드
- 직교 부반송파(15kHz 간격)를 시간 자원(Symbol)과 결합
- 사용자별로 서로 다른 자원 블록(RB) 할당 가능

**2. 데이터센터 네트워킹과의 융합**
- DWDM 기반 DCI(Data Center Interconnect): 400G × 80λ = 32Tbps
- Coherent Optics: DP-QPSK/16QAM 변조로 스펙트럼 효율 2~4배 향상

**3. 클라우드/SDN과의 융합**
- 동적 파장 할당 (ROADM: Reconfigurable OADM)
- SDN 컨트롤러 기반 광 경로(Path) 프로비저닝

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 통신사 백홀 망 설계

**문제 상황**: 5G 기지국 100개를 CORE망에 연결하는 백홀(Backhaul) 네트워크를 설계하라.
- 요구 대역폭: 기지국당 10 Gbps
- 거리: 최대 50 km
- 예산 제약: 장비 비용 최소화

**기술사의 전략적 의사결정**:

1. **요구 총 대역폭**: 100 × 10 Gbps = 1 Tbps

2. **방안 비교**:
   | 방안 | 기술 | 장비 수 | 비용 | 장점 | 단점 |
   |---|---|---|---|---|---|
   | A | 100G × 10회선 DWDM | 20 (MUX/DEMUX×10) | 높음 | 확장성 | 과잉 투자 |
   | B | 10G × 100회선 Dark Fiber | 200 (트랜시버) | 매우 높음 | 단순함 | 광섬유 부족 |
   | C | 10G × 40λ CWDM + aggregation | 5 | 중간 | 경제적 | 확장성 제한 |

3. **최종 선택**: 방안 A (DWDM 40채널 × 25G)
   - 총 용량: 1 Tbps
   - 장비: MUX/DEMUX × 2, 트랜시버 × 40
   - 향후 확장: 50GHz 간격 → 25GHz로 변경 시 80채널 가능

### 도입 시 고려사항 체크리스트

**기술적 고려사항**:
- [ ] 광섬유 타입 확인 (G.652D vs G.655)
- [ ] OSNR(Optical SNR) 예산 계산
- [ ] 비선형 효과(FWM, SRS, SBS) 평가
- [ ] PMD(편파 모드 분산) 확인

**운영/경제적 고려사항**:
- [ ] OPEX vs CAPEX 분석
- [ ] 향후 5~10년 트래픽 증가 예측
- [ ] 벤더 호환성 (Multi-vendor 환경)

### 안티패턴 (Anti-patterns)

**안티패턴 1: Dark Fiber 과다 사용**
- 10G 회선 100개를 위해 Dark Fiber 100쌍 사용은 비경제적. DWDM 10채널로 1쌍으로 해결 가능.

**안티패턴 2: 저가 CWDM으로 장거리 설계**
- CWDM은 EDFA 증폭 불가. 80km 이상은 필연적으로 DWDM 선택 필요.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 항목 | 측정 지표 | 개선 폭 |
|---|---|---|
| **광섬유 활용률** | Gbps/파이버 | 1G → 32T (32,000배) |
| **CAPEX 절감** | 장비 비용 | 70~80% 절감 (DWDM vs 다중 광섬유) |
| **전력 효율** | W/Gbps | 50~70% 절감 |
| **운영 단순화** | 회선 관리 복잡도 | 80% 감소 |

### 미래 전망 및 진화 방향

**1. Flexi-Grid DWDM (ITU-T G.694.1)**
- 고정 50/100GHz 간격 → 가변 12.5GHz 단위 할당
- 스펙트럼 효율 30% 향상

**2. Space Division Multiplexing (SDM)**
- 다중 코어 광섬유(MCF), 다중 모드 광섬유(FMF)
- Pb/s급 전송 실현

**3. AI 기반 동적 자원 할당**
- 트래픽 패턴 학습 후 실시간 파장/대역폭 재할당

### ※ 참고 표준/가이드

- **ITU-T G.694.1**: Spectral grids for WDM applications: DWDM frequency grid
- **ITU-T G.694.2**: Spectral grids for WDM applications: CWDM wavelength grid
- **ITU-T G.7041**: Generic Framing Procedure (GFP)
- **IEEE 802.3**: Ethernet (다양한 PHY 표준 포함)

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [OFDM/OFDMA](@/studynotes/03_network/05_wireless/ofdm_ofdma.md) : 무선 통신에서의 FDM 진화 형태.
- [SONET/SDH](@/studynotes/03_network/02_wan/sonet_sdh.md) : TDM 기반 광전송 표준.
- [광증폭기 EDFA](@/studynotes/03_network/03_physical/edfa_optical_amplifier.md) : DWDM 장거리 전송의 핵심.
- [PON (Passive Optical Network)](@/studynotes/03_network/02_wan/pon_network.md) : WDM 기반 가입자망.
- [CDMA 방식](@/studynotes/03_network/05_wireless/cdma_systems.md) : 코드 분할 다중화 기술.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 다중화는 **'한 도로에 여러 차선을 만드는 것'**과 같아요. 한 차선만 있으면 한 대씩밖에 못 가지만, 4차선이면 4대가 동시에 갈 수 있죠.
2. FDM은 **'라디오 채널'**처럼 각 차선이 다른 주파수를 쓰고, TDM은 **'교통신호'**처럼 시간을 나누어 번갈아 가며 보내요.
3. WDM은 **'무지개 빛'**처럼 여러 색깔의 빛을 한 광섬유로 보내서, 한 번에 엄청나게 많은 정보를 보낼 수 있어요.
