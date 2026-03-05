+++
title = "다중화 기술 (Multiplexing)"
date = 2024-05-18
description = "FDM, TDM, WDM, CDM 다중화 기술의 원리, 아키텍처, 성능 비교 및 현대 통신망 적용 사례 심층 분석"
weight = 20
[taxonomies]
categories = ["studynotes-03_network"]
tags = ["Multiplexing", "FDM", "TDM", "WDM", "CDM", "OFDM", "Telecommunications"]
+++

# 다중화 기술 (Multiplexing Techniques)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 다중화(Multiplexing)는 하나의 전송 매체(물리적 회선, 광섬유, 무선 채널)를 통해 여러 개의 독립적인 신호를 동시에 전송하는 기술로, 주파수, 시간, 파장, 코드의 직교성을 활용하여 채널 자원을 논리적으로 분할합니다.
> 2. **가치**: 통신 인프라 구축 비용을 50~80%까지 절감하고, 대역폭 활용 효율을 극대화하여 제한된 스펙트럼 자원으로 수백만 사용자의 동시 통신을 가능하게 합니다.
> 3. **융합**: 현대의 5G NR, Wi-Fi 6/7(OFDMA), 광통신(DWDM), 위성 통신(CDMA)은 모두 다중화 기술을 기반으로 하며, SDN/NFV와 결합하여 동적 대역폭 할당이 가능한 지능형 네트워크로 진화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

다중화(Multiplexing)는 통신 시스템의 가장 기본적이면서도 핵심적인 기술로, 하나의 고비용 전송 매체를 여러 저속 채널이 공유하여 경제적이고 효율적인 통신을 실현합니다. 송신측의 **MUX(다중화기, Multiplexer)**가 여러 신호를 하나로 결합하고, 수신측의 **DEMUX(역다중화기, Demultiplexer)**가 이를 다시 원래의 신호로 분리합니다.

**💡 비유**: 다중화는 **'고속도로'**와 같습니다.
- **FDM(주파수 분할)**: 고속도로를 여러 개의 차선으로 나누어, 각 차선에서 서로 다른 속도의 차량이 동시에 달립니다.
- **TDM(시분할)**: 하나의 차선을 시간대별로 나누어, 번갈아가며 차량이 통과합니다.
- **WDM(파장 분할)**: 같은 도로 위를 서로 다른 색깔(파장)의 빛 차량이 동시에 달립니다.
- **CDM(코드 분할)**: 모든 차량이 같은 도로를 동시에 달리지만, 각기 다른 언어(코드)로 대화하여 서로 구별합니다.

**등장 배경 및 발전 과정**:
1. **초기 통신의 비효율성**: 20세기 초, 전화 통신을 위해 각 가입자 쌍마다 별도의 구리선을 설치해야 했습니다. 이는 막대한 인프라 비용과 자원 낭비를 초래했습니다.
2. **혁신적 해결책 - FDM의 탄생**: 1910년대 AT&T에서 최초의 주파수 분할 다중화(Carrier Telephony)를 도입하여, 하나의 회선으로 4개의 음성 채널을 동시에 전송했습니다.
3. **디지털 시대의 TDM**: 1960년대 PCM(Pulse Code Modulation)과 함께 시분할 다중화가 등장하여, 디지털 전화망(T1/E1)의 기반이 되었습니다.
4. **광통신 혁명 - WDM**: 1990년대 광섬유의 여러 파장을 활용하는 WDM 기술이 개발되어, 단일 광섬유의 용량을 Tbps 단위로 끌어올렸습니다.
5. **모바일 혁명 - CDMA/OFDMA**: 이동통신에서 CDMA(3G)와 OFDMA(4G/5G)가 도입되어, 제한된 주파수 자원으로 수억 명의 사용자를 수용하게 되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: 다중화 기술 분류 체계

| 다중화 방식 | 영문 명칭 | 분할 자원 | 핵심 원리 | 채널 수 | 주요 적용 |
|------------|----------|----------|----------|---------|----------|
| **FDM** | Frequency Division Multiplexing | 주파수 | 서로 다른 주파수 대역 할당 | 대역폭/채널폭 | 라디오/TV 방송, ADSL |
| **TDM** | Time Division Multiplexing | 시간 | 타임슬롯(Time Slot) 순차 할당 | 프레임 길이/슬롯 길이 | T1/E1 전화망, GSM |
| **WDM** | Wavelength Division Multiplexing | 파장 | 서로 다른 광 파장(색상) 할당 | 광 대역폭/파장 간격 | 광통신 백본, 해저 케이블 |
| **CDM** | Code Division Multiplexing | 코드 | 직교 코드(Orthogonal Code) 할당 | 코드 공간 | CDMA 이동통신, GPS |
| **OFDM** | Orthogonal FDM | 주파수+직교성 | 직교 부반송파 다중화 | 부반송파 수 | Wi-Fi, LTE, 5G, DAB |
| **SDM** | Space Division Multiplexing | 공간 | 물리적 공간/안테나 분리 | 포트/안테나 수 | MIMO, 다중 안테나 |
| **PDM** | Polarization Division Multiplexing | 편파 | 광 신호의 편파 상태 분리 | 2 (수평/수직) | 고속 광통신 |

### 정교한 구조 다이어그램: 다중화 기술 비교

```ascii
================================================================================
[ Multiplexing Techniques Architecture Comparison ]
================================================================================

1. FDM (Frequency Division Multiplexing)
================================================================================
주파수 ↑
        |  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___
        | |   ||   ||   ||   ||   ||   ||   ||   ||   ||   |
        | |Ch1||Ch2||Ch3||Ch4||Ch5||Ch6||Ch7||Ch8||Ch9||Ch10|
        | |___||___||___||___||___||___||___||___||___||___|
        |_________________________________________________________→ 시간
           ↑                                   ↑
           보호대역(Guard Band) - 채널 간 간섭 방지

   특징: 아날로그/디지털 모두 가능, 연속 전송, 보호대역 필요


2. TDM (Time Division Multiplexing) - 동기식
================================================================================
시간슬롯 →
        |----|----|----|----|----|----|----|----|----|----|
        | Ch1| Ch2| Ch3| Ch4| Ch1| Ch2| Ch3| Ch4| Ch1| Ch2|
        |----|----|----|----|----|----|----|----|----|----|
           ↑    ↑    ↑    ↑
          1프레임 (125μs = 8000 samples/sec)

   특징: 디지털 전용, 고정 슬롯 할당, 유휴 슬롯 낭비 가능


3. TDM (Statistical) - 비동기식/통계적
================================================================================
시간슬롯 →
        |----|----|----|----|----|----|----|----|
        | Ch1| Ch3| Ch1| Ch2| Ch1| Ch3| Ch2| Ch1|
        |----|----|----|----|----|----|----|----|
           ↑    ↑
          활성 채널만 전송 (주소 비트 필요)

   특징: 동적 슬롯 할당, 대역폭 효율 높음, 오버헤드 존재


4. WDM (Wavelength Division Multiplexing)
================================================================================
파장(λ) ↑
        |  λ1  λ2  λ3  λ4  λ5  λ6  λ7  λ8
        |  🔴  🟠  🟡  🟢  🔵  🟣  ⚪  ⚫
        |  |   |   |   |   |   |   |   |
        |  +---+---+---+---+---+---+---+----→ 단일 광섬유
        |              결합기 (Coupler)

   CWDM: 20nm 간격, 18채널 (저비용)
   DWDM: 0.8nm/0.4nm 간격, 160+ 채널 (고밀도)


5. CDM (Code Division Multiplexing)
================================================================================
              채널 1 코드: [+1 +1 +1 +1]
              채널 2 코드: [+1 -1 +1 -1]  (왈시 코드)
              채널 3 코드: [+1 +1 -1 -1]
              채널 4 코드: [+1 -1 -1 +1]

   전송 신호 = Σ(데이터 × 코드)

   수신측: 상관관계(Correlation) 계산으로 원본 복원
   - 자기 상관: 최대값 (데이터 복원)
   - 교차 상관: 0 (간섭 제거)

   조건: 코드 간 직교성(Orthogonality) 필수


6. OFDM (Orthogonal Frequency Division Multiplexing)
================================================================================
주파수 ↑
   f12  | █     █     █     █     █     █
   f11  |   █     █     █     █     █     █
   f10  | █     █     █     █     █     █
   f9   |   █     █     █     █     █     █
   f8   | █     █     █     █     █     █
   f7   |   █     █     █     █     █     █
   f6   | █     █     █     █     █     █
   f5   |   █     █     █     █     █     █
   f4   | █     █     █     █     █     █
   f3   |   █     █     █     █     █     █
   f2   | █     █     █     █     █     █
   f1   |   █     █     █     █     █     █
        |__________________________________________→ 시간

   특징: 부반송파 간 겹침 허용 (직교성으로 분리)
         보호대역 불필요 → 스펙트럼 효율 극대화
         IFFT/FFT로 구현 (디지털 신호 처리)
================================================================================
```

### 심층 동작 원리: 각 다중화 기술 상세 분석

#### 1. FDM (Frequency Division Multiplexing)

**동작 원리**:
1. 각 입력 신호를 서로 다른 주파수 대역(Carrier Frequency)으로 변조(AM, FM 등)
2. 변조된 신호들을 하나의 광대역 채널로 결합
3. 수신측에서 대역 통과 필터(Bandpass Filter)로 원하는 채널 추출
4. 복조(Demodulation)하여 원본 신호 복원

**핵심 요소**:
- **보호대역(Guard Band)**: 인접 채널 간 간섭을 방지하기 위한 빈 주파수 영역
- **대역폭 계산**: `총 대역폭 = N × (채널 대역폭 + 보호대역)`

**수식**:
```
전송 신호: s(t) = Σ m_i(t) × cos(2πf_i × t)

여기서:
- m_i(t): i번째 채널의 베이스밴드 신호
- f_i: i번째 채널의 반송파 주파수
```

#### 2. TDM (Time Division Multiplexing)

**동기식 TDM (Synchronous TDM)**:
- 고정된 타임슬롯을 각 채널에 정적으로 할당
- **T1 프레임 구조**: 24음성채널 × 8비트 + 1프레임 비트 = 193비트/프레임
- **프레임 속도**: 8000 frames/sec (음성 샘플링 속도)
- **전송 속도**: 193 bits × 8000 = 1.544 Mbps

**비동기식/통계적 TDM (Statistical TDM)**:
- 활성 채널에만 동적으로 슬롯 할당
- 각 슬롯에 주소/식별자 필요
- 대역폭 효율 증가, 단 지연 및 오버헤드 발생

**비트 교차 vs 바이트 교차**:
```
비트 교차(Bit Interleaving):
Ch1: 1 0 1 1  Ch2: 0 1 1 0  Ch3: 1 1 0 0
→ 1|0|1|0|1|1|1|1|1|0|0|0 (비트 단위 교차)

바이트 교차(Byte Interleaving):
Ch1: A B C D  Ch2: W X Y Z
→ A|W|B|X|C|Y|D|Z (바이트 단위 교차)
```

#### 3. WDM (Wavelength Division Multiplexing)

**CWDM vs DWDM 비교**:

| 특성 | CWDM (Coarse WDM) | DWDM (Dense WDM) |
|------|------------------|------------------|
| 파장 간격 | 20 nm | 0.8 nm / 0.4 nm |
| 파장 범위 | 1270~1610 nm | 1530~1565 nm (C-band) |
| 채널 수 | 최대 18 | 최대 160+ |
| 광증폭기 | 불필요 | EDFA 필수 |
| 비용 | 저렴 | 고가 |
| 적용 | 도시권(MAN), FTTH | 장거리 백본, 해저 케이블 |

**DWDM 시스템 구성**:
```
[송신측]
클라이언트 신호 → O-E-O 변환 → 파장 할당 → WDM 결합기 → 광섬유

[전송로]
광섬유 → EDFA 증폭 → 광섬유 → EDFA 증폭 → ...

[수신측]
광섬유 → WDM 분리기 → 파장 필터링 → O-E-O 변환 → 클라이언트 신호
```

#### 4. CDM (Code Division Multiplexing)

**직교 코드(Orthogonal Code) 원리**:
```
왈시 코드(Walsh Code) 예시 - 4비트 코드:

W0 = [+1, +1, +1, +1]
W1 = [+1, -1, +1, -1]
W2 = [+1, +1, -1, -1]
W3 = [+1, -1, -1, +1]

직교성 검증:
W0 · W1 = (+1)(+1) + (+1)(-1) + (+1)(+1) + (+1)(-1) = 1 - 1 + 1 - 1 = 0
W1 · W3 = (+1)(+1) + (-1)(-1) + (+1)(-1) + (-1)(+1) = 1 + 1 - 1 - 1 = 0

→ 모든 서로 다른 코드 쌍의 내적 = 0 (직교성 성립)
```

**CDM 송수신 과정**:
1. **송신**: `전송 신호 = 데이터 × 확산 코드 (Spreading)`
2. **채널**: 모든 사용자의 신호가 중첩되어 전송
3. **수신**: `복원 데이터 = 수신 신호 × 확산 코드 (Desreading)`

#### 5. OFDM (Orthogonal Frequency Division Multiplexing)

**직교성의 수학적 원리**:
```
부반송파 간 직교성:

∫ cos(2πf_m × t) × cos(2πf_n × t) dt = 0  (m ≠ n)

여기서 f_m - f_n = k × (1/T_symbol), k는 정수

→ 부반송파 간격 = 1/T_symbol일 때 직교성 성립
→ 스펙트럼 겹침 허용, 보호대역 불필요
```

**IFFT/FFT 구현**:
```python
import numpy as np

def ofdm_modulate(data_bits, n_subcarriers=64):
    """
    OFDM 변조 (IFFT 기반)

    Args:
        data_bits: 직렬 비트 스트림
        n_subcarriers: 부반송파 수

    Returns:
        OFDM 심볼 (시간 영역)
    """
    # 직렬→병렬 변환
    n_symbols = len(data_bits) // n_subcarriers
    parallel_data = np.reshape(data_bits[:n_symbols * n_subcarriers],
                               (n_symbols, n_subcarriers))

    # 주파수 영역 심볼 (QPSK 매핑 예시)
    freq_symbols = parallel_data.astype(complex)

    # IFFT로 시간 영역 변환
    time_symbols = np.fft.ifft(freq_symbols, n=n_subcarriers, axis=1)

    # Cyclic Prefix 추가 (ISI 방지)
    cp_length = n_subcarriers // 4
    ofdm_symbols = np.concatenate([
        time_symbols[:, -cp_length:],  # CP
        time_symbols
    ], axis=1)

    return ofdm_symbols

def ofdm_demodulate(ofdm_symbols, n_subcarriers=64):
    """
    OFDM 복조 (FFT 기반)
    """
    cp_length = n_subcarriers // 4

    # Cyclic Prefix 제거
    time_symbols = ofdm_symbols[:, cp_length:]

    # FFT로 주파수 영역 변환
    freq_symbols = np.fft.fft(time_symbols, n=n_subcarriers, axis=1)

    return freq_symbols
```

### 핵심 코드: 다중화 기술 시뮬레이터 (Python)

```python
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from enum import Enum

class MultiplexingType(Enum):
    FDM = "Frequency Division Multiplexing"
    TDM = "Time Division Multiplexing"
    CDM = "Code Division Multiplexing"
    OFDM = "Orthogonal FDM"

class MultiplexerSimulator:
    """
    다양한 다중화 기술을 시뮬레이션하는 클래스
    """

    def __init__(self, n_channels: int = 4, sample_rate: int = 1000):
        self.n_channels = n_channels
        self.sample_rate = sample_rate

    # ================== FDM 시뮬레이션 ==================
    def fdm_modulate(self, channel_signals: List[np.ndarray],
                     carrier_frequencies: List[float]) -> np.ndarray:
        """
        FDM 변조: 각 채널을 서로 다른 주송파로 변조 후 결합

        Args:
            channel_signals: 각 채널의 베이스밴드 신호 리스트
            carrier_frequencies: 각 채널의 반송파 주파수 (Hz)

        Returns:
            FDM 결합 신호
        """
        t = np.arange(len(channel_signals[0])) / self.sample_rate
        fdm_signal = np.zeros_like(t)

        for i, (signal, f_c) in enumerate(zip(channel_signals, carrier_frequencies)):
            # AM 변조 (DSB-SC)
            modulated = signal * np.cos(2 * np.pi * f_c * t)
            fdm_signal += modulated

        return fdm_signal

    def fdm_demodulate(self, fdm_signal: np.ndarray,
                       carrier_frequencies: List[float],
                       channel_bandwidth: float) -> List[np.ndarray]:
        """
        FDM 복조: 대역통과 필터링 후 복조
        """
        from scipy.signal import butter, filtfilt

        t = np.arange(len(fdm_signal)) / self.sample_rate
        recovered_signals = []

        for f_c in carrier_frequencies:
            # 대역통과 필터
            low = (f_c - channel_bandwidth/2) / (self.sample_rate/2)
            high = (f_c + channel_bandwidth/2) / (self.sample_rate/2)
            b, a = butter(4, [low, high], btype='band')
            filtered = filtfilt(b, a, fdm_signal)

            # 동기 검파 (Coherent Detection)
            carrier = np.cos(2 * np.pi * f_c * t)
            demodulated = 2 * filtered * carrier

            # 저역통과 필터
            b_low, a_low = butter(4, channel_bandwidth/(self.sample_rate/2), btype='low')
            baseband = filtfilt(b_low, a_low, demodulated)

            recovered_signals.append(baseband)

        return recovered_signals

    # ================== TDM 시뮬레이션 ==================
    def tdm_multiplex(self, channel_data: List[List[int]],
                      bits_per_slot: int = 8) -> Tuple[np.ndarray, dict]:
        """
        동기식 TDM 다중화

        Args:
            channel_data: 각 채널의 데이터 (비트 리스트)
            bits_per_slot: 타임슬롯당 비트 수

        Returns:
            (다중화된 비트 스트림, 프레임 정보)
        """
        max_len = max(len(ch) for ch in channel_data)
        n_channels = len(channel_data)
        frame_size = n_channels * bits_per_slot

        multiplexed = []
        frame_info = {
            'n_channels': n_channels,
            'bits_per_slot': bits_per_slot,
            'frame_size': frame_size,
            'n_frames': 0
        }

        # 각 채널의 데이터를 슬롯 단위로 교차 배치
        for i in range(0, max_len, bits_per_slot):
            for ch in channel_data:
                slot = ch[i:i+bits_per_slot]
                # 패딩
                while len(slot) < bits_per_slot:
                    slot.append(0)
                multiplexed.extend(slot)
            frame_info['n_frames'] += 1

        return np.array(multiplexed), frame_info

    def tdm_demultiplex(self, multiplexed: np.ndarray,
                        frame_info: dict) -> List[List[int]]:
        """
        동기식 TDM 역다중화
        """
        n_channels = frame_info['n_channels']
        bits_per_slot = frame_info['bits_per_slot']
        frame_size = frame_info['frame_size']

        channels = [[] for _ in range(n_channels)]

        for frame_idx in range(frame_info['n_frames']):
            frame_start = frame_idx * frame_size
            for ch_idx in range(n_channels):
                slot_start = frame_start + ch_idx * bits_per_slot
                slot = multiplexed[slot_start:slot_start + bits_per_slot]
                channels[ch_idx].extend(slot.tolist())

        return channels

    # ================== CDM 시뮬레이션 ==================
    def generate_walsh_codes(self, n_codes: int) -> np.ndarray:
        """
        왈시 코드(Walsh Code) 생성

        Hadamard 행렬을 사용하여 직교 코드 생성
        """
        # Hadamard 행렬 초기화 (H1 = [1])
        h_size = 1
        while h_size < n_codes:
            h_size *= 2

        H = np.array([[1]])

        # Hadamard 행렬 확장 (H_2n = [H_n, H_n; H_n, -H_n])
        while H.shape[0] < h_size:
            H = np.block([[H, H], [H, -H]])

        return H[:n_codes]

    def cdm_spread(self, data_bits: np.ndarray,
                   spreading_code: np.ndarray) -> np.ndarray:
        """
        CDM 확산(Spreading)

        Args:
            data_bits: 원본 데이터 비트 (0/1 또는 -1/+1)
            spreading_code: 확산 코드 (칩 시퀀스)

        Returns:
            확산된 신호 (칩 단위)
        """
        # 비트를 -1/+1로 변환
        if np.any((data_bits != -1) & (data_bits != 1)):
            data_bits = 2 * data_bits - 1

        # 각 비트를 코드로 확산
        code_length = len(spreading_code)
        spread_signal = np.zeros(len(data_bits) * code_length)

        for i, bit in enumerate(data_bits):
            spread_signal[i * code_length:(i + 1) * code_length] = bit * spreading_code

        return spread_signal

    def cdm_despread(self, spread_signal: np.ndarray,
                     spreading_code: np.ndarray) -> np.ndarray:
        """
        CDM 역확산(Despreading)

        상관관계(Correlation)를 이용한 원본 복원
        """
        code_length = len(spreading_code)
        n_bits = len(spread_signal) // code_length
        recovered_bits = np.zeros(n_bits)

        for i in range(n_bits):
            # 코드와의 상관관계 계산
            chip_segment = spread_signal[i * code_length:(i + 1) * code_length]
            correlation = np.sum(chip_segment * spreading_code) / code_length
            recovered_bits[i] = 1 if correlation > 0 else 0

        return recovered_bits

    def cdm_multiplex(self, channel_data: List[np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
        """
        CDM 다중화: 모든 채널을 동시에 전송

        Returns:
            (다중화 신호, 확산 코드 행렬)
        """
        n_channels = len(channel_data)
        spreading_codes = self.generate_walsh_codes(n_channels)

        # 모든 채널 확산 후 합산
        multiplexed = np.zeros(len(channel_data[0]) * spreading_codes.shape[1])

        for i, data in enumerate(channel_data):
            spread = self.cdm_spread(data, spreading_codes[i])
            multiplexed += spread

        return multiplexed, spreading_codes

    def cdm_demultiplex(self, multiplexed: np.ndarray,
                        spreading_codes: np.ndarray) -> List[np.ndarray]:
        """
        CDM 역다중화: 각 코드로 역확산하여 채널 분리
        """
        channels = []
        for code in spreading_codes:
            recovered = self.cdm_despread(multiplexed, code)
            channels.append(recovered)

        return channels


# ================== 시뮬레이션 실행 예시 ==================
if __name__ == "__main__":
    sim = MultiplexerSimulator(n_channels=4)

    # 테스트 데이터 생성
    np.random.seed(42)
    test_data = [np.random.randint(0, 2, 100) for _ in range(4)]

    print("=" * 60)
    print("Multiplexing Techniques Simulation Report")
    print("=" * 60)

    # CDM 시뮬레이션
    print("\n[CDM Simulation]")
    multiplexed, codes = sim.cdm_multiplex(test_data)
    recovered = sim.cdm_demultiplex(multiplexed, codes)

    print(f"Number of Channels: {len(test_data)}")
    print(f"Spreading Code Length: {codes.shape[1]}")
    print(f"Processing Gain: {codes.shape[1]}x")
    print(f"Multiplexed Signal Length: {len(multiplexed)}")

    # 오류율 계산
    for i, (orig, rec) in enumerate(zip(test_data, recovered)):
        ber = np.mean(orig != rec)
        print(f"  Channel {i+1} BER: {ber:.4f}")
