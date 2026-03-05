+++
title = "PCM 및 표본화 이론 (PCM and Sampling Theorem)"
date = 2024-05-18
description = "아날로그 신호를 디지털로 변환하는 PCM(Pulse Code Modulation)의 표본화, 양자화, 부호화 과정과 나이퀴스트 정리의 심층 분석"
weight = 35
[taxonomies]
categories = ["studynotes-network"]
tags = ["PCM", "Sampling", "Nyquist", "Quantization", "Aliasing", "A-law", "mu-law"]
+++

# PCM 및 표본화 이론 (PCM and Sampling Theorem)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: PCM(Pulse Code Modulation)은 아날로그 신호를 표본화(Sampling), 양자화(Quantization), 부호화(Encoding)의 3단계를 거쳐 디지털 비트 열로 변환하는 기술로, 현대 디지털 통신(음성, 오디오, 비디오)의 기초입니다.
> 2. **가치**: 나이퀴스트 표본화 정리에 따르면 대역폭 B의 신호는 최소 2B Hz로 표본화해야 완전한 복원이 가능하며, 이는 음성 통신(8kHz), 오디오 CD(44.1kHz), 5G RF(수GHz)의 표본화율 결정 근거입니다.
> 3. **융합**: PCM은 VoIP, 디지털 방송, 의료 영상(MRI/CT), 소나/레이더 등 광범위하게 적용되며, 최근 AI 기반 음성인식, 이미지 압축, 그리고 뇌-컴퓨터 인터페이스의 신호 처리 기반이기도 합니다.

---

## Ⅰ. 개요 (Context & Background)

PCM(Pulse Code Modulation)은 1937년 영국의 알렉스 리브스(Alec Reeves)가 발명한 기술로, 연속적인 아날로그 신호를 이산적인 디지털 샘플로 변환하는 과정입니다. 이 과정은 세 단계로 구성됩니다:

1. **표본화(Sampling)**: 시간 영역의 연속 신호를 이산 시점에서 샘플링
2. **양자화(Quantization)**: 연속 진폭 값을 유한한 레벨로 근사화
3. **부호화(Encoding)**: 양자화된 레벨을 이진 코드로 변환

**💡 비유**: PCM은 **'영화 필름 만들기'**와 같습니다. 연속적인 움직임(아날로그)을 1초에 24장의 정지 사진(표본화)으로 촬영하고, 각 사진의 색상을 16만 색(양자화)으로 제한한 후, 이를 숫자로 저장(부호화)하는 것입니다. 충분히 빠르게 촬영하면 우리 눈은 연속적인 영상으로 인식합니다.

**등장 배경 및 발전 과정**:
1. **기존 기술의 치명적 한계점**: 초기 아날로그 전화는 증폭 과정에서 잡음이 누적되어 장거리 통화 품질이 심각히 저하되었습니다. 1940년대 벨 연구소는 이를 해결하기 위해 디지털 재생 중계기를 필요로 했습니다.
2. **혁신적 패러다임 변화**: PCM은 잡음이 추가되어도 0/1 판별만 가능하면 완벽한 재생이 가능하다는 '디지털 이점'을 처음으로 구현했습니다. 1962년 T1 디지털 전송 시스템이 상용화되었습니다.
3. **비즈니스적 요구사항**: 현대 스트리밍 서비스(Netflix, Spotify), VoIP(Zoom, Teams), 디지털 방송(ATSC 3.0)은 모두 PCM 기반의 디지털 신호 처리에 의존하며, 고품질-저지연-저용량의 상충 관계를 최적화하는 것이 경쟁력입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### PCM 시스템 구성도

```ascii
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          PCM 송신 시스템 (A/D 변환)                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  아날로그        ┌──────────┐      ┌──────────┐      ┌──────────┐    디지털     │
│   신호          │          │      │          │      │          │     비트      │
│   ────→         │ 표본화    │ ───→ │ 양자화    │ ───→ │  부호화   │ ───→  0101... │
│  (음성 등)       │(Sampling)│      │(Quantize)│      │(Encoding)│              │
│                 └──────────┘      └──────────┘      └──────────┘              │
│                      ↑                ↑                 ↑                       │
│                 fs ≥ 2B           L 레벨           n = log₂L                  │
│                (나이퀴스트)       (양자화 레벨)        (비트/샘플)               │
│                                                                                 │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │  예: 전화 음성 (G.711)                                                   │    │
│  │  • 대역폭: 4kHz → 표본화율: 8kHz                                        │    │
│  │  • 양자화 레벨: 256 (8bit μ-law)                                        │    │
│  │  • 전송률: 8kHz × 8bit = 64 kbps                                        │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                          PCM 수신 시스템 (D/A 변환)                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  디지털         ┌──────────┐      ┌──────────┐      ┌──────────┐    아날로그   │
│   비트          │          │      │          │      │          │     신호      │
│  0101... ───→   │  복호화   │ ───→ │  역양자화 │ ───→ │  보간     │ ───→  ─────   │
│                 │(Decoding)│      │(Dequant) │      │(Interp.) │              │
│                 └──────────┘      └──────────┘      └──────────┘              │
│                                                         │                       │
│                                              Low-Pass Filter                │
│                                              (재생 필터)                      │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 이론: 나이퀴스트-샤논 표본화 정리

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    나이퀴스트 표본화 정리 (Nyquist Sampling Theorem)           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  "대역폭이 B Hz인 신호는 최소 2B Hz의 속도로 표본화해야 정보 손실 없이        │
│   원래 신호를 완벽하게 재구성할 수 있다."                                    │
│                                                                             │
│  최소 표본화 주파수: f_s ≥ 2B                                               │
│                                                                             │
│  나이퀴스트 속도: f_N = 2B (최소 표본화율)                                  │
│  나이퀴스트 주파수: f_Nyquist = f_s / 2 (표본화 가능한 최대 주파수)          │
│                                                                             │
│  수학적 표현:                                                                │
│  x(t) = Σ x(nT_s) · sinc(π(t - nT_s)/T_s)                                  │
│         n=-∞                                                               │
│                                                                             │
│  여기서 sinc(x) = sin(x)/x, T_s = 1/f_s                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 표본화(Sampling) 심층 분석

**1. 이상적 표본화 (Ideal Sampling)**
```
이상적 표본화는 순간적인 델타 함수로 샘플링:

x_s(t) = x(t) · Σ δ(t - nT_s)
              n

주파수 영역에서:
X_s(f) = f_s · Σ X(f - n·f_s)
                n

- 스펙트럼이 f_s 간격으로 무한히 반복됨
- f_s > 2B 이면 복제 스펙트럼이 겹치지 않음
- Low-Pass Filter로 원 신호 복원 가능
```

**2. 에일리어싱 (Aliasing) 현상**
```
f_s < 2B 인 경우 발생:

        │ X(f) 원본         │ 복제 스펙트럼이 겹침
        │    ████           │
        │   █    █          │    ┌─────────────────────┐
        │  █      █         │    │  겹침 영역 (Aliasing) │
        └──┴──────┴───→ f   │    │  정보 왜곡 발생      │
           -B    B          │    └─────────────────────┘
                              → 복원 불가능!

해결책:
1. 표본화 전 Anti-Aliasing Filter (LPF) 적용
2. 표본화율을 대역폭의 2배 이상으로 설정
```

**3. 실제 응용별 표본화율**

| 응용 분야 | 신호 대역폭 | 표본화율 fs | 비트/샘플 | 총 비트율 |
|---|---|---|---|---|
| **전화 음성 (G.711)** | 3.4 kHz | 8 kHz | 8 | 64 kbps |
| **CD 오디오** | 20 kHz | 44.1 kHz | 16 | 1.41 Mbps |
| **DVD 오디오** | 96 kHz | 192 kHz | 24 | 4.6 Mbps |
| **VoIP (G.729)** | 3.4 kHz | 8 kHz | 2 (압축) | 16 kbps |
| **SDR (Software Defined Radio)** | 20 MHz | 56 MHz | 14 | 784 Mbps |

### 양자화(Quantization) 심층 분석

**1. 균일 양자화 (Uniform Quantization)**
```
양자화 스텝: Δ = V_pp / L

V_pp: 피크-투-피크 전압 범위
L: 양자화 레벨 수 (L = 2^n)

양자화 오차: e = x_q - x
범위: -Δ/2 ≤ e ≤ Δ/2

양자화 잡음 전력:
N_q = Δ²/12 = V_pp² / (12 × L²)

신호 대 양자화잡음비 (SQNR):
SQNR(dB) = 6.02n + 1.76 dB

예: n=8bit → SQNR ≈ 49.9 dB
    n=16bit → SQNR ≈ 98.0 dB
```

**2. 비균일 양자화 (Non-Uniform Quantization)**
```
작은 신호에는 작은 스텝, 큰 신호에는 큰 스텝 사용

μ-law (북미/일본):
y = sgn(x) × ln(1 + μ|x|) / ln(1 + μ)
μ = 255 (표준)

A-law (유럽/국제):
y = sgn(x) × A|x| / (1 + ln(A))    for |x| < 1/A
y = sgn(x) × (1 + ln(A|x|)) / (1 + ln(A))  for |x| ≥ 1/A
A = 87.6 (표준)

효과:
- 동적 범위 30~40 dB 개선
- 작은 신호 SQNR 개선
- 전화 음성 품질 향상
```

### PCM 파형 형식

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PCM 파형 형식 비교                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. NRZ (Non-Return to Zero)                                               │
│     1: ████████████     0:             (레벨 유지)                          │
│                                                                             │
│  2. RZ (Return to Zero)                                                    │
│     1: ████              0:           (비트 중간 0 복귀)                    │
│                                                                             │
│  3. Manchester (Biphase)                                                   │
│     1:     ████       0: ████          (비트 중간 전이)                     │
│            ████             ████                                            │
│                                                                             │
│  4. AMI (Alternate Mark Inversion)                                         │
│     1: +V, -V 교차      0: 0V          (0이 아닌 1은 교대로 +V, -V)         │
│                                                                             │
│  전송 효율: NRZ > AMI > Manchester                                          │
│  동기화 능력: Manchester > AMI > NRZ                                        │
│  DC 성분 제거: AMI, Manchester > NRZ                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: PCM 시스템 시뮬레이션 (Python)

```python
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List
from scipy import signal

class PCMSimulator:
    """PCM 변환 시뮬레이터"""

    def __init__(self, sample_rate: int = 8000, bits_per_sample: int = 8):
        self.fs = sample_rate
        self.bits = bits_per_sample
        self.levels = 2 ** bits_per_sample

    # ===================== 표본화 (Sampling) =====================
    def sample_signal(self, analog_signal: np.ndarray,
                      original_fs: float) -> np.ndarray:
        """
        아날로그 신호 표본화

        Args:
            analog_signal: 원본 아날로그 신호
            original_fs: 원본 샘플링 레이트

        Returns:
            표본화된 신호
        """
        # 다운샘플링 비율 계산
        if original_fs > self.fs:
            ratio = int(original_fs / self.fs)
            return analog_signal[::ratio]
        elif original_fs < self.fs:
            # 업샘플링 (보간)
            ratio = int(self.fs / original_fs)
            return np.repeat(analog_signal, ratio)
        return analog_signal

    def ideal_sample(self, continuous_time: np.ndarray,
                     signal: np.ndarray, n_samples: int) -> Tuple[np.ndarray, np.ndarray]:
        """이상적 표본화 (델타 함수 근사)"""
        sample_times = np.linspace(continuous_time[0], continuous_time[-1], n_samples)
        sample_indices = np.searchsorted(continuous_time, sample_times)
        sample_values = signal[sample_indices]
        return sample_times, sample_values

    def reconstruct_signal(self, sample_times: np.ndarray,
                           sample_values: np.ndarray,
                           output_times: np.ndarray) -> np.ndarray:
        """
        sinc 보간을 통한 신호 재구성

        x(t) = Σ x(nT) · sinc((t - nT)/T)
        """
        T = sample_times[1] - sample_times[0] if len(sample_times) > 1 else 1
        reconstructed = np.zeros_like(output_times, dtype=float)

        for n, t_n in enumerate(sample_times):
            sinc_arg = np.pi * (output_times - t_n) / T
            # 0으로 나누기 방지
            with np.errstate(divide='ignore', invalid='ignore'):
                sinc_val = np.where(sinc_arg == 0, 1.0, np.sin(sinc_arg) / sinc_arg)
            reconstructed += sample_values[n] * sinc_val

        return reconstructed

    # ===================== 양자화 (Quantization) =====================
    def uniform_quantize(self, signal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        균일 양자화

        Returns:
            quantized: 양자화된 신호 값
            code: 이진 코드 (인덱스)
        """
        # 정규화 (-1 ~ 1)
        signal_normalized = signal / np.max(np.abs(signal))

        # 양자화 레벨 계산
        delta = 2.0 / self.levels  # 스텝 크기

        # 양자화 인덱스
        code = np.floor((signal_normalized + 1) / delta)
        code = np.clip(code, 0, self.levels - 1).astype(int)

        # 양자화된 값 (중간값)
        quantized = (code + 0.5) * delta - 1

        return quantized, code

    def mu_law_compress(self, signal: np.ndarray, mu: float = 255) -> np.ndarray:
        """μ-law 압신 (Companding)"""
        signal_normalized = signal / np.max(np.abs(signal))
        compressed = np.sign(signal_normalized) * np.log(1 + mu * np.abs(signal_normalized)) / np.log(1 + mu)
        return compressed

    def mu_law_expand(self, signal: np.ndarray, mu: float = 255) -> np.ndarray:
        """μ-law 신장 (Expanding)"""
        expanded = np.sign(signal) * (1 / mu) * ((1 + mu) ** np.abs(signal) - 1)
        return expanded

    def a_law_compress(self, signal: np.ndarray, A: float = 87.6) -> np.ndarray:
        """A-law 압신"""
        signal_normalized = signal / np.max(np.abs(signal))
        abs_x = np.abs(signal_normalized)

        compressed = np.where(
            abs_x < 1/A,
            A * abs_x / (1 + np.log(A)),
            (1 + np.log(A * abs_x)) / (1 + np.log(A))
        )
        return np.sign(signal_normalized) * compressed

    # ===================== 성능 분석 =====================
    def calculate_sqnr(self, original: np.ndarray,
                       quantized: np.ndarray) -> float:
        """신호 대 양자화잡음비 (SQNR) 계산"""
        signal_power = np.mean(original ** 2)
        noise_power = np.mean((original - quantized) ** 2)
        return 10 * np.log10(signal_power / noise_power)

    def calculate_snr(self, original: np.ndarray,
                      reconstructed: np.ndarray) -> float:
        """신호 대 잡음비 (SNR) 계산"""
        signal_power = np.mean(original ** 2)
        noise_power = np.mean((original - reconstructed) ** 2)
        return 10 * np.log10(signal_power / noise_power)

    def analyze_aliasing(self, signal_freq: float, sample_rate: float) -> dict:
        """에일리어싱 분석"""
        nyquist = sample_rate / 2

        if signal_freq <= nyquist:
            alias_freq = signal_freq
            is_aliased = False
        else:
            # 에일리어싱 발생: 주파수가 [0, nyquist] 범위로 "접힘"
            alias_freq = abs(signal_freq - sample_rate * round(signal_freq / sample_rate))
            is_aliased = True

        return {
            'original_freq': signal_freq,
            'sample_rate': sample_rate,
            'nyquist_freq': nyquist,
            'alias_freq': alias_freq,
            'is_aliased': is_aliased,
            'min_sample_rate': 2 * signal_freq
        }


class AudioPCMAnalyzer:
    """오디오 PCM 분석"""

    @staticmethod
    def cd_audio_params() -> dict:
        """CD 오디오 파라미터"""
        return {
            'sample_rate': 44100,  # Hz
            'bits_per_sample': 16,
            'channels': 2,
            'bandwidth': 20000,  # Hz (사람 가청 주파수)
            'bit_rate': 44100 * 16 * 2,  # 1,411,200 bps
            'nyquist_freq': 22050,  # Hz
        }

    @staticmethod
    def voip_params(codec: str = 'G.711') -> dict:
        """VoIP 코덱 파라미터"""
        codecs = {
            'G.711': {'sample_rate': 8000, 'bits': 8, 'bitrate': 64000},
            'G.729': {'sample_rate': 8000, 'bits': 2, 'bitrate': 16000},
            'G.722': {'sample_rate': 16000, 'bits': 8, 'bitrate': 64000},
            'Opus': {'sample_rate': 48000, 'bits': 'variable', 'bitrate': 6000~510000},
        }
        return codecs.get(codec, {})


def demonstrate_aliasing():
    """에일리어싱 시연"""
    print("=" * 60)
    print("에일리어싱 (Aliasing) 시연")
    print("=" * 60)

    pcm = PCMSimulator()

    # 1kHz 신호를 다양한 샘플링 레이트로 표본화
    test_cases = [
        (1000, 8000, "정상 (fs > 2f)"),
        (1000, 1500, "에일리어싱 (fs < 2f)"),
        (4000, 8000, "나이퀴스트 경계"),
        (5000, 8000, "심각한 에일리어싱"),
    ]

    for freq, fs, desc in test_cases:
        result = pcm.analyze_aliasing(freq, fs)
        print(f"\n{desc}:")
        print(f"  신호 주파수: {freq} Hz")
        print(f"  표본화율: {fs} Hz")
        print(f"  나이퀴스트 주파수: {result['nyquist_freq']} Hz")
        print(f"  에일리어싱 여부: {'예' if result['is_aliased'] else '아니오'}")
        if result['is_aliased']:
            print(f"  에일리어싱된 주파수: {result['alias_freq']} Hz")


def demonstrate_quantization():
    """양자화 시연"""
    print("\n" + "=" * 60)
    print("양자화 품질 분석")
    print("=" * 60)

    # 테스트 신호 생성
    t = np.linspace(0, 1, 1000)
    test_signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 10 * t)

    for bits in [4, 8, 12, 16]:
        pcm = PCMSimulator(bits_per_sample=bits)
        quantized, code = pcm.uniform_quantize(test_signal)
        sqnr = pcm.calculate_sqnr(test_signal, quantized)

        # 이론적 SQNR: 6.02n + 1.76
        theoretical_sqnr = 6.02 * bits + 1.76

        print(f"\n{bits}비트 양자화:")
        print(f"  레벨 수: {2**bits}")
        print(f"  실제 SQNR: {sqnr:.2f} dB")
        print(f"  이론적 SQNR: {theoretical_sqnr:.2f} dB")


if __name__ == "__main__":
    demonstrate_aliasing()
    demonstrate_quantization()

    print("\n" + "=" * 60)
    print("CD 오디오 vs 전화 음성 비교")
    print("=" * 60)

    cd = AudioPCMAnalyzer.cd_audio_params()
    print(f"\nCD 오디오:")
    print(f"  표본화율: {cd['sample_rate']} Hz")
    print(f"  비트/샘플: {cd['bits_per_sample']}")
    print(f"  비트 전송률: {cd['bit_rate']/1000:.1f} kbps")

    voip = AudioPCMAnalyzer.voip_params('G.711')
    print(f"\n전화 음성 (G.711):")
    print(f"  표본화율: {voip['sample_rate']} Hz")
    print(f"  비트/샘플: {voip['bits']}")
    print(f"  비트 전송률: {voip['bitrate']/1000:.0f} kbps")
    print(f"\nCD vs 전화 품질 차이: {cd['bit_rate']/voip['bitrate']:.1f}배")
