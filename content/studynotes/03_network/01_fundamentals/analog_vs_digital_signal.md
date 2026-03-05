+++
title = "아날로그 신호 vs 디지털 신호"
date = 2024-05-18
description = "아날로그 신호와 디지털 신호의 근본적 차이, 장단점, 그리고 통신 시스템에서의 역할과 상호 변환 메커니즘을 심도 있게 분석합니다."
weight = 15
[taxonomies]
categories = ["studynotes-03_network"]
tags = ["Analog", "Digital", "Signal", "Sampling", "Quantization"]
+++

# 아날로그 신호 vs 디지털 신호 (Analog vs Digital Signal)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 아날로그 신호는 시간과 진폭이 연속적인(Continuous) 물리적 파형으로, 자연계의 소리, 빛, 열 등을 직접 표현합니다. 디지털 신호는 시간과 진폭을 이산적인(Discrete) 비트열로 표현하여, 컴퓨터가 처리 가능한 0과 1의 논리 값으로 추상화합니다.
> 2. **가치**: 아날로그 신호는 무한한 해상도와 자연스러움을 제공하지만 잡음에 취약합니다. 디지털 신호는 잡음 내성, 오류 정정, 암호화, 압축이 가능하여 장거리 전송과 저장에 압도적으로 유리합니다.
> 3. **융합**: 현대 통신 시스템은 아날로그와 디지털의 하이브리드로, 아날로그 세계(음성, 영상)를 ADC(Analog-to-Digital Converter)로 디지털화하여 전송/저장/처리한 후, DAC(Digital-to-Analog Converter)로 다시 아날로그로 재생하여 인간이 인식합니다.

---

## Ⅰ. 개요 (Context & Background)

아날로그 신호(Analog Signal)와 디지털 신호(Digital Signal)는 정보를 표현하고 전달하는 두 가지 근본적으로 다른 방식입니다. 이 둘의 차이는 '연속성(Continuity)'과 '이산성(Discreteness)'에 있습니다.

**개념 정의**:
- **아날로그 신호**: 시간에 따라 연속적으로 변화하는 물리량(전압, 전류, 주파수 등)으로 정보를 표현합니다. 신호의 진폭이나 주파수가 정보의 크기나 내용에 비례합니다. 예: 음성, 아날로그 라디오, 아날로그 TV.
- **디지털 신호**: 정해진 시각에만 존재하는 이산적인 값(주로 0과 1)으로 정보를 표현합니다. 일정한 구간(Pulse)으로 나누고, 각 구간의 값을 유한한 레벨로 근사화합니다. 예: 컴퓨터 데이터, 디지털 TV, MP3.

**💡 비유**: 시계로 비유하면:
- **아날로그 신호**는 **아날로그 시계**와 같습니다. 초침이 시계 바늘 위를 연속적으로 미끄러지듯이 움직이며, 시간의 어떤 순간이든 정확한 위치를 가리킵니다. 이론적으로 무한한 정밀도를 가집니다.
- **디지털 신호**는 **디지털 시계**와 같습니다. 시간이 "14:35:27"처럼 숫자로 표시되며, 초 단위로 딱딱 끊어져서 바뀝니다. 14:35:27과 14:35:28 사이의 시간은 표시되지 않습니다.

**등장 배경 및 발전 과정**:
1. **자연계는 아날로그**: 인간의 음성, 음악, 빛, 열 등 모든 자연 현상은 본질적으로 아날로그입니다. 초기 통신(전신, 전화)도 아날로그 방식으로 시작했습니다.
2. **디지털의 등장**: 1940년대 디지털 컴퓨터의 등장과 함께 0과 1로 정보를 처리하는 디지털 방식이 탄생했습니다. 1960년대 PCM(Pulse Code Modulation)이 상용화되면서 음성 통신의 디지털화가 시작되었습니다.
3. **디지털 혁명**: 1990년대 이후 인터넷, 이동통신, 디지털 방송의 폭발적 성장으로 디지털 신호 처리가 통신의 주류가 되었습니다. 오늘날 대부분의 통신 시스템은 디지털 기반입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: 아날로그 vs 디지털 신호 특성 비교

| 특성 | 아날로그 신호 (Analog) | 디지털 신호 (Digital) | 상세 분석 |
|------|----------------------|---------------------|----------|
| **시간 연속성** | 연속적 (Continuous) | 이산적 (Discrete) | 아날로그는 모든 시점에 값 존재, 디지털은 샘플링 시점에만 값 존재 |
| **진폭 레벨** | 무한 (Infinite) | 유한 (Finite) | 아날로그는 이론적 무한 해상도, 디지털은 비트 수에 따른 유한 레벨 |
| **표현 방식** | 파형 (Sine Wave 등) | 펄스열 (Pulse Train) | 아날로그는 사인파 합성, 디지털은 직사각형 펄스 |
| **잡음 영향** | 누적됨 (Accumulative) | 재생 가능 (Regenerable) | 아날로그는 잡음이 누적되어 품질 저하, 디지털은 중계기에서 신호 재생 |
| **대역폭 효율** | 상대적으로 낮음 | 압축으로 높일 수 있음 | 디지털은 압축(CODEC)으로 대역폭 효율화 가능 |
| **처리 장비** | 증폭기, 필터 (아날로그 회로) | 프로세서, 메모리 (디지털 회로) | 디지털은 소프트웨어로 유연한 처리 가능 |
| **보안성** | 낮음 (도청 쉬움) | 높음 (암호화 가능) | 디지털은 AES 등 강력한 암호화 적용 가능 |

### 정교한 구조 다이어그램: 아날로그-디지털 변환 과정

```ascii
================================================================================
[ Analog-to-Digital Conversion (ADC) Pipeline: 음성 신호 디지털화 ]
================================================================================

[ 아날로그 영역 ]                    [ 변환 경계 ]              [ 디지털 영역 ]

음성 (소리)                                                   컴퓨터/네트워크
    |                                                              ^
    v                                                              |
+------------+          +------------+         +------------+  +------------+
| 마이크론   |  아날로그 | Anti-Alias |  샘플링  |   Sample   |  양자화  | Quantizer  |
| (Transducer)|=========>| Filter     |========>| & Hold     |=========>| (ADC)      |
+------------+  전압    | (LPF)      |  fs Hz  | Circuit    |  Q 레벨  +------------+
                  신호    +------------+         +------------+             |
                                                    ^                     v
                                                    |               +------------+
                    샘플링 주기: Ts = 1/fs           |               | 인코더     |
                    (예: fs=8000Hz, Ts=125us)       |               | (Encoder)  |
                                                    |               +------------+
                                                    |                     |
                                                    |  n-bit              | 디지털
                                                    |  코드워드           | 비트열
                                                    v                     v
                                              +------------+        +------------+
                                              |  PCM 출력  |        | 전송/저장  |
                                              |  8-bit/sample       | 처리       |
                                              +------------+        +------------+

================================================================================
[ Digital-to-Analog Conversion (DAC) Pipeline: 디지털 신호 복원 ]
================================================================================

+------------+          +------------+         +------------+  +------------+
| 수신/재생  |  디지털  | 디코더     |  n-bit  | DAC        |  아날로그 | Reconstruction
| (Playback) |=========>| (Decoder)  |=========>| (변환기)   |=========>| Filter     |
+------------+  비트열  +------------+  코드워드+------------+  계단파형 +------------+
                                                                       |
                                                                       | 평활화
                                                                       v
                                                                   +------------+
                                                                   | 스피커     |
                                                                   | (Speaker)  |
                                                                   +------------+
                                                                        |
                                                                        v
                                                                    소리 (음성)

================================================================================
[ 신호 파형 비교 ]

아날로그 신호 (연속):
  Amplitude
      ^
  +1V |    /\      /\
      |   /  \    /  \    /\      자연스러운 연속 파형
   0V |__/    \__/    \__/  \__   (잡음 포함 가능)
      +-------------------------> Time

디지털 신호 (이산):
  Amplitude
      ^
  +5V |    ___      ___      ___  직사각형 펄스
      |   |   |    |   |    |   |  0과 1 두 레벨만 존재
   0V |___|   |____|   |____|   | (잡음 내성 강함)
      +-------------------------> Time

양자화 과정 (Quantization):
  Amplitude                      원본 아날로그 (점선)
      ^                          양자화된 값 (실선)
  Q7  |--------*--------*---------
      |        |        |
  Q6  |--------|--------|--------  양자화 레벨 (8레벨 = 3bit)
      |        |        |         연속값 -> 이산값 근사화
  Q5  |--------|--------*--------
      |        |        |         * = 샘플링된 값
  Q4  |--------|--------|--------
      |        |        |         양자화 오차 = 원본 - 양자화값
  Q3  |---*----|--------|--------
      |   |    |        |
  Q2  |---|----|---*----|--------
      |   |    |   |    |
  Q1  |---|----|---|----|--------
      |   |    |   |    |
  Q0  +---|----|---|----|--------> Time
          Ts       Ts
================================================================================
```

### 심층 동작 원리: ADC(아날로그-디지털 변환) 3단계 프로세스

1. **표본화 (Sampling)**:
   - 연속적인 아날로그 신호를 일정한 시간 간격(Ts)으로 샘플링합니다.
   - **나이퀴스트 정리(Nyquist Theorem)**: 원신호의 최고 주파수를 f_max라 할 때, 샘플링 주파수 fs >= 2 × f_max여야 원신호 완전 복원 가능합니다.
   - 예: 음성 전화는 3.4kHz까지만 전송하므로 fs = 8kHz로 샘플링합니다.
   - 샘플링 주파수가 부족하면 **에일리어싱(Aliasing)** 현상이 발생하여 고주파 신호가 저주파로 왜곡됩니다.

2. **양자화 (Quantization)**:
   - 샘플링된 각 값(연속적인 진폭)을 가장 가까운 유한한 레벨(Q0, Q1, Q2, ...)로 근사화합니다.
   - n비트로 표현 가능한 레벨 수는 2^n개입니다. 8비트 = 256레벨, 16비트 = 65,536레벨.
   - **양자화 오차(Quantization Error)**: 원본 값과 양자화된 값의 차이. 이는 **양자화 잡음(Quantization Noise)**으로 나타납니다.
   - **비선형 양자화(μ-law, A-law)**: 작은 진폭 신호에 더 많은 레벨을 할당하여 음성 신호의 SNR(신호 대 잡음비)을 개선합니다.

3. **부호화 (Encoding)**:
   - 양자화된 각 레벨을 n비트의 이진 코드(코드워드)로 변환합니다.
   - 예: 256레벨(8비트) 양자화에서 레벨 127은 "01111111", 레벨 128은 "10000000"으로 인코딩.
   - PCM(Pulse Code Modulation)에서는 각 샘플을 독립적으로 부호화합니다.
   - 압축을 위해 DPCM(차분 PCM), ADPCM(적응 차분 PCM) 등을 사용하기도 합니다.

### 핵심 수식: 샤논의 채널 용량과 나이퀴스트-샤논 정리

```
[ 나이퀴스트 샘플링 정리 ]
fs >= 2 × f_max

여기서:
- fs: 샘플링 주파수 (samples/sec, Hz)
- f_max: 원신호의 최고 주파수 성분 (Hz)

[ 양자화 신호 대 잡음비 (SQNR) ]
SQNR(dB) = 6.02 × n + 1.76

여기서:
- n: 비트 수 (bits per sample)
- SQNR: Signal-to-Quantization-Noise Ratio

예: 8비트 양자화 시 SQNR = 6.02 × 8 + 1.76 = 49.92 dB
    16비트 양자화 시 SQNR = 6.02 × 16 + 1.76 = 98.08 dB

[ 샤논의 채널 용량 (무잡음) - 나이퀴스트 용량 ]
C = 2 × B × log2(M)

여기서:
- C: 채널 용량 (bps)
- B: 대역폭 (Hz)
- M: 신호 레벨 수 (심볼 당 비트)
```

### 핵심 코드: PCM 부호화 및 디코딩 시뮬레이션 (Python)

```python
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

class PCMCodec:
    """
    PCM(Pulse Code Modulation) 부호화/복호화 코덱
    샘플링, 양자화, 부호화 과정을 시뮬레이션합니다.
    """

    def __init__(self, sample_rate: int = 8000, bits_per_sample: int = 8):
        """
        Args:
            sample_rate: 샘플링 주파수 (Hz), 기본값 8kHz (전화 품질)
            bits_per_sample: 샘플 당 비트 수, 기본값 8비트
        """
        self.sample_rate = sample_rate
        self.bits_per_sample = bits_per_sample
        self.num_levels = 2 ** bits_per_sample
        self.max_amplitude = 1.0  # 정규화된 최대 진폭

        # 양자화 레벨 생성 (균등 양자화)
        self.quant_levels = np.linspace(
            -self.max_amplitude,
            self.max_amplitude,
            self.num_levels
        )

        print(f"[PCM Codec 초기화]")
        print(f"  샘플링 주파수: {sample_rate} Hz")
        print(f"  비트 수: {bits_per_sample} bits")
        print(f"  양자화 레벨: {self.num_levels}")
        print(f"  이론적 SQNR: {6.02 * bits_per_sample + 1.76:.2f} dB")

    def sample(self, analog_signal: np.ndarray, original_rate: int) -> np.ndarray:
        """
        아날로그 신호를 샘플링합니다.

        Args:
            analog_signal: 원본 아날로그 신호
            original_rate: 원본 신호의 샘플링 주파수 (시뮬레이션용)

        Returns:
            샘플링된 신호
        """
        # 리샘플링 비율 계산
        if original_rate == self.sample_rate:
            return analog_signal

        ratio = original_rate / self.sample_rate
        num_samples = int(len(analog_signal) / ratio)
        sample_indices = np.linspace(0, len(analog_signal) - 1, num_samples, dtype=int)

        sampled = analog_signal[sample_indices]
        print(f"[샘플링] {len(analog_signal)} -> {len(sampled)} 샘플")
        return sampled

    def quantize(self, sampled_signal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        샘플링된 신호를 양자화합니다.

        Args:
            sampled_signal: 샘플링된 신호

        Returns:
            (양자화된 신호, 양자화 인덱스)
        """
        # 신호를 -1 ~ 1 범위로 클리핑
        clipped = np.clip(sampled_signal, -self.max_amplitude, self.max_amplitude)

        # 가장 가까운 양자화 레벨 찾기
        quantized = np.zeros_like(clipped)
        indices = np.zeros(len(clipped), dtype=int)

        for i, sample in enumerate(clipped):
            # 절대 차이가 최소인 레벨의 인덱스
            idx = np.argmin(np.abs(self.quant_levels - sample))
            quantized[i] = self.quant_levels[idx]
            indices[i] = idx

        # 양자화 오차 계산
        quantization_error = clipped - quantized
        mse = np.mean(quantization_error ** 2)
        print(f"[양자화] MSE: {mse:.6f}, 최대 오차: {np.max(np.abs(quantization_error)):.4f}")

        return quantized, indices

    def encode(self, quant_indices: np.ndarray) -> bytes:
        """
        양자화 인덱스를 비트열로 부호화합니다.

        Args:
            quant_indices: 양자화 인덱스 배열

        Returns:
            부호화된 바이트열
        """
        if self.bits_per_sample == 8:
            # 8비트: 바이트로 직접 변환
            return quant_indices.astype(np.uint8).tobytes()
        else:
            # n비트: 비트 패킹 필요
            bitstream = []
            for idx in quant_indices:
                binary = format(idx, f'0{self.bits_per_sample}b')
                bitstream.append(binary)

            bit_string = ''.join(bitstream)
            # 비트열을 바이트로 변환
            return bytes(int(bit_string[i:i+8], 2)
                        for i in range(0, len(bit_string), 8))

    def decode(self, encoded_data: bytes) -> np.ndarray:
        """
        부호화된 데이터를 복호화합니다.

        Args:
            encoded_data: 부호화된 바이트열

        Returns:
            복호화된 양자화 레벨 (아날로그 근사값)
        """
        if self.bits_per_sample == 8:
            indices = np.frombuffer(encoded_data, dtype=np.uint8)
        else:
            # 비트 언패킹 (간소화된 버전)
            indices = []
            # ... 복잡한 비트 언패킹 로직
            indices = np.array(indices)

        # 인덱스를 양자화 레벨로 변환
        return self.quant_levels[indices]

    def measure_sqnr(self, original: np.ndarray, reconstructed: np.ndarray) -> float:
        """
        실제 신호 대 양자화 잡음비 측정

        Returns:
            SQNR in dB
        """
        signal_power = np.mean(original ** 2)
        noise_power = np.mean((original - reconstructed) ** 2)

        if noise_power == 0:
            return float('inf')

        sqnr = 10 * np.log10(signal_power / noise_power)
        return sqnr


# [실무 사용 예시]
def demo_pcm_codec():
    """PCM 코덱 데모: 사인파 신호의 디지털화"""

    # 1. 원본 아날로그 신호 생성 (440Hz 사인파, 1초)
    duration = 1.0
    freq = 440  # Hz (A4 음)
    original_rate = 44100  # 오디오 CD 품질

    t = np.linspace(0, duration, int(original_rate * duration), endpoint=False)
    analog_signal = 0.8 * np.sin(2 * np.pi * freq * t)

    print("=" * 60)
    print("PCM 부호화/복호화 데모")
    print("=" * 60)

    # 2. PCM 코덱 생성 (전화 품질)
    codec = PCMCodec(sample_rate=8000, bits_per_sample=8)

    # 3. 샘플링
    sampled = codec.sample(analog_signal, original_rate)

    # 4. 양자화
    quantized, indices = codec.quantize(sampled)

    # 5. 부호화
    encoded = codec.encode(indices)
    print(f"[부호화] 비트 전송률: {8000 * 8 / 1000:.1f} kbps")
    print(f"[부호화] 총 바이트 수: {len(encoded)} bytes")

    # 6. 복호화
    decoded = codec.decode(encoded)

    # 7. SQNR 측정
    # 길이 맞추기 (리샘플링된 원본과 비교)
    t_sampled = np.linspace(0, duration, len(sampled), endpoint=False)
    original_resampled = 0.8 * np.sin(2 * np.pi * freq * t_sampled)
    sqnr = codec.measure_sqnr(original_resampled, decoded)
    print(f"[SQNR] 실측: {sqnr:.2f} dB (이론값: {6.02 * 8 + 1.76:.2f} dB)")

    return codec, sampled, quantized, decoded


if __name__ == "__main__":
    demo_pcm_codec()
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 아날로그 vs 디지털 통신 시스템

| 비교 관점 | 아날로그 통신 (Analog) | 디지털 통신 (Digital) | 기술사적 분석 |
|----------|----------------------|---------------------|--------------|
| **전송 품질** | 거리 증가 시 품질 저하 | 중계기에서 신호 재생으로 품질 유지 | 장거리 통신에서 디지털 압도적 우위 |
| **잡음 내성** | 취약 (잡음 누적) | 강함 (오류 정정 가능) | 열 잡음, 충격 잡음에 디지털 유리 |
| **대역폭 요구** | 상대적으로 적음 | 샘플링/양자화로 증가하나 압축 가능 | 디지털은 압축 기술로 효율화 |
| **보안** | 도청 쉬움 | 강력한 암호화 가능 | 군사, 금융 분야에서 디지털 필수 |
| **다중화** | FDM(주파수 분할) 위주 | TDM(시분할), CDM, WDM 활용 | 디지털 다중화가 더 유연하고 효율적 |
| **장비 복잡도** | 단순 (증폭기, 필터) | 복잡 (ADC, DSP, 프로세서) | 디지털은 초기 비용 높으나 기능 다양 |
| **유지보수** | 튜닝 필요, 노화 민감 | 소프트웨어 업데이트 가능 | 디지털이 운영 비용 절감 효과 |
| **적용 분야** | 라디오, 아날로그 TV(구형) | 인터넷, 디지털 TV, 이동통신 | 대부분 신규 시스템은 디지털 |

### 과목 융합 관점 분석 (운영체제 및 하드웨어 연계)

1. **운영체제(OS)와의 융합**:
   - **사운드 카드 드라이버**: OS의 오디오 드라이버(ALSA, Core Audio)가 ADC/DAC 하드웨어를 제어합니다. 샘플링 주파수, 비트 깊이, 버퍼 크기를 설정합니다.
   - **실시간 처리**: 디지털 신호 처리(DSP)를 위해 OS는 낮은 지연(Low Latency)을 보장하는 실시간 스케줄링(RT-Preempt 패치)을 적용합니다.
   - **메모리 관리**: 오디오/비디오 스트림 처리 시 순환 버퍼(Ring Buffer)를 사용하여 연속적인 데이터 흐름을 관리합니다.

2. **하드웨어(Hardware)와의 융합**:
   - **ADC/DAC 칩**: 스마트폰의 코덱 칩(Cirrus Logic, Qualcomm)이 24비트/192kHz 이상의 고해상도 변환을 수행합니다.
   - **DSP(Digital Signal Processor)**: 전용 하드웨어가 실시간 FFT, 필터링, 노이즈 캔슬링을 수행하여 CPU 부하를 경감합니다.
   - **FPGA/GPU 가속**: 대용량 신호 처리(5G 기지국, 레이더)를 위해 FPGA나 GPU의 병렬 처리 능력을 활용합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: VoIP 시스템 코덱 선택

**문제 상황**: 기업 내부 VoIP 전화 시스템을 구축해야 합니다. 음성 품질, 대역폭, 지연 시간을 고려하여 최적의 코덱을 선택해야 합니다.

**기술사의 전략적 의사결정**:

1. **요구사항 분석**:
   - 음성 품질: MOS 4.0 이상 (고품질)
   - 대역폭: 제한적 (지사 간 2Mbps 회선)
   - 지연 시간: 150ms 이하 (실시간 대화 가능)

2. **코덱 비교 분석**:
   | 코덱 | 비트레이트 | 대역폭 | MOS | 지연 |
   |------|----------|-------|-----|------|
   | G.711 (PCM) | 64 kbps | 3.4kHz | 4.1 | 0.125ms |
   | G.729 (CS-ACELP) | 8 kbps | 3.4kHz | 3.9 | 15ms |
   | G.722.2 (AMR-WB) | 12.65-23.85 kbps | 7kHz | 4.2 | 20ms |
   | Opus | 6-510 kbps | 4-20kHz | 4.5+ | 2.5-60ms |

3. **선택 및 근거**:
   - **1순위: G.722.2 (AMR-WB)** - 광대역 음성(7kHz)으로 자연스러운 음질, 대역폭 효율
   - **2순위(fallback): G.711 (PCM)** - 호환성 최고, 지연 최소, 대역폭 충분 시 사용
   - **Opus 고려**: WebRTC 기반 화상회의에는 Opus 권장 (적응형 비트레이트)

### 도입 시 고려사항 및 안티패턴 (Anti-patterns)

- **안티패턴 - 과도한 압축**:
  G.729(8kbps)로 압축률을 높이면 대역폭은 절약되지만, 음성 품질이 저하되고 처리 지연이 증가합니다. 100명 동시 통화 시에도 8Mbps만 필요하므로, 현대 네트워크에서는 G.711(64kbps)이나 G.722를 사용하는 것이 TCO 측면에서 더 유리할 수 있습니다.

- **체크리스트**:
  - 샘플링 주파수가 나이퀴스트 정리를 만족하는가?
  - 양자화 비트 수가 요구 SNR을 충족하는가?
  - ADC/DAC의 선형성(Linearity)이 요구 정밀도를 만족하는가?
  - 에일리어싱 방지 필터(Anti-Alias Filter)가 적절한가?

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 영역 | 아날로그 방식 | 디지털 방식 | 개선 효과 |
|----------|--------------|------------|----------|
| **전송 품질** | 거리당 3dB 감쇠 | 중계기에서 재생 | 거리 무관 품질 유지 |
| **암호화** | 아날로그 스크램블링 (취약) | AES-256 (강력) | 보안성 획기적 향상 |
| **다중화 효율** | FDM (제한적) | TDM/CDM (고효율) | 채널 용량 10배 증가 |
| **오류 정정** | 불가능 | FEC, ARQ 가능 | 무오류 전송 가능 |

### 미래 전망 및 진화 방향

- **소프트웨어 정의 라디오(SDR)**: ADC/DAC를 안테나 직후에 배치하여, 하드웨어 변경 없이 소프트웨어만으로 다양한 무선 표준(Wi-Fi, LTE, 5G)을 지원합니다.
- **양자 아날로그 컴퓨팅**: 아날로그 방식의 병렬 처리 능력과 양자 중첩을 결합하여, 디지털 컴퓨터로 불가능한 문제를 해결하는 하이브리드 시스템이 등장할 것입니다.
- **뉴로모픽(Neuromorphic) 칩**: 인간 뇌의 아날로그 신경망을 모방한 칩이 디지털 방식보다 에너지 효율적인 AI 처리를 가능하게 할 것입니다.

### ※ 참고 표준/가이드
- **ITU-T G.711**: Pulse Code Modulation (PCM) of Voice Frequencies
- **ITU-T G.722**: 7 kHz Audio-Coding within 64 kbit/s
- **IEEE 1241**: Standard for Terminology and Test Methods for Analog-to-Digital Converters

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [PCM 펄스 부호 변조](@/studynotes/03_network/01_fundamentals/_index.md): 아날로그 음성을 디지털로 변환하는 핵심 기술
- [나이퀴스트/샤논 정리](@/studynotes/03_network/01_fundamentals/_index.md): 샘플링 이론과 채널 용량의 수학적 기반
- [변조 기법](@/studynotes/03_network/01_fundamentals/_index.md): ASK, FSK, PSK, QAM 등 디지털 변조 방식
- [오류 정정 부호](@/studynotes/03_network/01_fundamentals/_index.md): 디지털 신호의 오류 검출 및 정정 기법
- [DSP 디지털 신호 처리](@/studynotes/03_network/01_fundamentals/_index.md): 디지털 신호의 필터링, 변환, 압축 기술

---

### 👶 어린이를 위한 3줄 비유 설명
1. **아날로그 신호**는 **물이 호스를 타고 연속적으로 흐르는 것**과 같아요. 물의 양이 조금씩 부드럽게 변하듯, 신호도 끊김 없이 조금씩 변합니다.
2. **디지털 신호**는 **계단을 오르내리는 것**과 같아요. 한 계단, 두 계단처럼 딱딱 끊어져서 올라가죠. 0과 1, 참과 거짓처럼 명확합니다.
3. **ADC 변환기**는 **연속적인 물줄기를 일정한 간격으로 컵에 담는 기계**예요. 호스에서 흐르는 물(아날로그)을 1초에 8번 컵에 담아(샘플링), 컵의 물 양을 숫자로 적어요(디지털)!
