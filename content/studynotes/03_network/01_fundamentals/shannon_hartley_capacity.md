+++
title = "샤논-하틀리 정리 (Shannon-Hartley Theorem)"
date = 2024-05-18
description = "통신 채널의 최대 데이터 전송 용량을 결정하는 샤논-하틀리 정리의 수학적 원리, 실무적용, 그리고 현대 통신 시스템에서의 한계 돌파 방안"
weight = 20
[taxonomies]
categories = ["studynotes-network"]
tags = ["Shannon", "Hartley", "Channel Capacity", "SNR", "Bandwidth", "Information Theory"]
+++

# 샤논-하틀리 정리 (Shannon-Hartley Theorem)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 샤논-하틀리 정리는 잡음이 존재하는 통신 채널에서 오류 없이 전송할 수 있는 최대 데이터 전송률(채널 용량)을 대역폭(B)과 신호 대 잡음비(SNR)의 함수로 정의하는 정보이론의 기본 법칙입니다: C = B × log₂(1 + S/N).
> 2. **가치**: 이 정리는 5G, Wi-Fi 6, 광통신 등 모든 현대 통신 시스템의 성능 상한선을 제시하며, 대역폭 확장, MIMO, 고차 변조(QAM) 등의 기술이 왜 필요한지를 이론적으로 설명합니다.
> 3. **융합**: 양자 통신, DNA 저장, 뇌-컴퓨터 인터페이스 등 신규 분야에서도 정보 전송의 물리적 한계를 규명하는 기준으로 활용되며, 통신·반도체·AI 융합 설계의 핵심 지표입니다.

---

## Ⅰ. 개요 (Context & Background)

샤논-하틀리 정리(Shannon-Hartley Theorem)는 1948년 클로드 샤논(Claude Shannon)이 발표한 "A Mathematical Theory of Communication" 논문에서 정립된 정보이론의 핵심 정리입니다. 이 정리는 잡음이 존재하는 연속 시간 채널(아날로그 채널)에서 무오류 전송이 가능한 최대 정보 전송률, 즉 채널 용량(Channel Capacity)을 수학적으로 도출합니다.

**💡 비유**: 샤논-하틀리 정리는 **'도로의 교통 용량 법칙'**과 같습니다. 도로의 차선 수(대역폭 B)가 많을수록, 그리고 차량 간 안전거리를 줄일수록(높은 SNR = 잡음이 적음) 더 많은 차량(데이터)이 통과할 수 있습니다. 그러나 아무리 노력해도 도로의 물리적 한계 이상으로 차량을 통과시킬 수 없듯, 통신 채널에도 물리적 한계가 존재하며 이를 샤논 한계(Shannon Limit)라고 합니다.

**등장 배경 및 발전 과정**:
1. **기존 기술의 치명적 한계점**: 1940년대 통신 엔지니어들은 잡음이 많은 채널에서 신뢰성을 높이기 위해 신호 전력을 무작정 증가시키거나, 데이터 전송률을 낮추는 보수적 접근을 사용했습니다. 이는 비효율적이며, 이론적 근거가 부족했습니다.
2. **혁신적 패러다임 변화**: 샤논은 잡음이 있어도 적절한 부호화(Encoding)를 통해 오류율을 0에 근접시키면서도, 특정 전송률 이하에서는 완벽한 통신이 가능함을 수학적으로 증명했습니다. 이는 "디지털 통신의 빅뱅"으로 불립니다.
3. **비즈니스적 요구사항**: 현대의 5G, 위성 통신, 해저 케이블 등에서는 대역폭과 전력이 제한된 환경에서 최대 throughput을 끌어내는 것이 경쟁력의 핵심입니다. 샤논 한계에 얼마나 근접하느냐가 통신 장비의 기술력을 결정합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 수학적 정의: 샤논-하틀리 공식

```
┌─────────────────────────────────────────────────────────────┐
│                    샤논-하틀리 채널 용량 공식                   │
│                                                             │
│              C = B × log₂(1 + S/N)                          │
│                                                             │
│  C: 채널 용량 (Channel Capacity) [bits/second, bps]        │
│  B: 대역폭 (Bandwidth) [Hertz, Hz]                          │
│  S: 신호 전력 (Signal Power) [Watts]                        │
│  N: 잡음 전력 (Noise Power) [Watts]                         │
│  S/N: 신호 대 잡음비 (Signal-to-Noise Ratio)                │
│                                                             │
│  ※ S/N을 선형 스케일이 아닌 dB로 표현 시:                    │
│     S/N(dB) = 10 × log₁₀(S/N)                              │
│     C = B × log₂(1 + 10^(SNR_dB/10))                       │
└─────────────────────────────────────────────────────────────┘
```

### 구성 요소 심층 분석

| 구성 요소 | 정의 | 단위 | 물리적 의미 | 영향 |
|---|---|---|---|---|
| **C (Channel Capacity)** | 최대 오류 없는 데이터 전송률 | bps | 이론적 성능 상한선 | 모든 통신 시스템의 목표 |
| **B (Bandwidth)** | 사용 가능한 주파수 범위 | Hz | 전송 매체의 주파수 자원 | B↑ → C 선형 증가 |
| **S (Signal Power)** | 전송 신호의 평균 전력 | W | 송신기의 전력 소모 | S↑ → C 로그 증가 |
| **N (Noise Power)** | 채널 내 잡음의 평균 전력 | W | 열잡음, 간섭 등 | N↑ → C 감소 |
| **S/N (SNR)** | 신호 강도 대 잡음 강도 비율 | 무차원 (또는 dB) | 신호 품질 척도 | SNR↑ → C 로그 증가 |

### 정교한 구조 다이어그램: 채널 용량 시각화

```ascii
                    채널 용량 C (Mbps)
                         ↑
                         │                                    ···· 40 dB SNR
                    400  │                               ····
                         │                          ····
                    300  │                     ····
                         │                ····
                    200  │           ····
                         │      ···· ···· 20 dB SNR
                    100  │ ····
                         │···               ···· 10 dB SNR
                      0  └──────────────────────────────────────→
                         0    5    10   15   20   25   30   35   대역폭 B (MHz)

    ┌─────────────────────────────────────────────────────────────────────┐
    │  핵심 통찰:                                                          │
    │  • 대역폭 증가는 용량을 "선형적"으로 증가시킴                          │
    │  • SNR 증가는 용량을 "로그적"으로 증가시킴 (한계 효과 체감)            │
    │  • 대역폭 2배 = 용량 2배, SNR 2배 = 용량 약 1.58배 (log₂3 ≈ 1.585)  │
    └─────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: 공식 도출 및 의미

**1. 나이퀴스트 식에서의 확장**
무잡음 채널에서의 나이퀴스트 식은 다음과 같습니다:
```
C_no_noise = 2B × log₂(M)
```
여기서 M은 신호 레벨 수(심볼 당 비트 수 결정)입니다.

샤논은 잡음이 존재할 때 구별 가능한 신호 레벨 수가 제한됨을 보였습니다:
```
M_max = √(1 + S/N)  (잡음에 의한 레벨 구분 한계)
```

이를 대입하면:
```
C = 2B × log₂(√(1 + S/N))
  = 2B × (1/2) × log₂(1 + S/N)
  = B × log₂(1 + S/N)  ✓
```

**2. AWGN (Additive White Gaussian Noise) 채널**
샤논의 공식은 AWGN 채널을 가정합니다:
- 잡음은 백색(White): 모든 주파수에 고르게 분포
- 잡음은 가우스 분포: 열잡음(Thermal Noise) 모델링
- 잡음 전력: N = k × T × B (k: 볼츠만 상수, T: 절대 온도, B: 대역폭)

**3. 스펙트럼 효율 (Spectral Efficiency)**
대역폭당 전송 용량을 나타내는 지표:
```
η = C/B = log₂(1 + S/N)  [bits/s/Hz]
```

### 핵심 수치 예시: 실제 시스템 분석

```
┌─────────────────────────────────────────────────────────────────────────┐
│  예시 1: 전화선 (POTS)                                                   │
│  대역폭 B = 3,100 Hz (300~3,400 Hz)                                     │
│  SNR = 30 dB (S/N = 1000)                                               │
│  C = 3100 × log₂(1 + 1000) = 3100 × 9.97 ≈ 30.9 kbps                   │
│  → 실제 모뎀: V.34 표준 28.8 kbps (이론의 93% 달성)                       │
├─────────────────────────────────────────────────────────────────────────┤
│  예시 2: Wi-Fi 6 (802.11ax) 20MHz 채널                                   │
│  대역폭 B = 20 MHz (실제 사용 ~18 MHz)                                   │
│  SNR = 40 dB (S/N = 10,000)                                             │
│  C = 18×10⁶ × log₂(10001) = 18×10⁶ × 13.29 ≈ 239 Mbps                  │
│  → 실제: 1024-QAM + OFDMA으로 약 143 Mbps (MIMO 미적용 시)              │
├─────────────────────────────────────────────────────────────────────────┤
│  예시 3: 5G NR (mmWave 100MHz)                                          │
│  대역폭 B = 100 MHz                                                      │
│  SNR = 25 dB (S/N = 316)                                                │
│  C = 100×10⁶ × log₂(317) = 100×10⁶ × 8.31 ≈ 831 Mbps                   │
│  → 4×4 MIMO 적용 시 이론적으로 4배까지 확장 가능 (약 3.3 Gbps)           │
├─────────────────────────────────────────────────────────────────────────┤
│  예시 4: 광섬유 (DWDM 50GHz 간격)                                         │
│  대역폭 B = 50 GHz (단일 파장 채널)                                      │
│  SNR = 30 dB (OSNR 광학적 신호 대 잡음비)                                │
│  C = 50×10⁹ × log₂(1001) ≈ 500 Gbps (단일 파장)                         │
│  → 80 파장 DWDM × DP-16QAM: 실제 400 Gbps × 80 = 32 Tbps               │
└─────────────────────────────────────────────────────────────────────────┘
```

### 실무 코드: 샤논 용량 계산기 및 시각화 (Python)

```python
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List

class ShannonCapacityAnalyzer:
    """샤논-하틀리 정리 기반 채널 용량 분석 도구"""

    # 물리 상수
    BOLTZMANN_CONST = 1.380649e-23  # J/K

    def __init__(self):
        self.results = {}

    def db_to_linear(self, db: float) -> float:
        """dB → 선형 스케일 변환"""
        return 10 ** (db / 10)

    def linear_to_db(self, linear: float) -> float:
        """선형 스케일 → dB 변환"""
        return 10 * np.log10(linear)

    def calculate_capacity(self, bandwidth_hz: float, snr_db: float) -> float:
        """
        샤논-하틀리 공식을 이용한 채널 용량 계산

        Args:
            bandwidth_hz: 대역폭 (Hz)
            snr_db: 신호 대 잡음비 (dB)

        Returns:
            채널 용량 (bps)
        """
        snr_linear = self.db_to_linear(snr_db)
        capacity = bandwidth_hz * np.log2(1 + snr_linear)
        return capacity

    def calculate_spectral_efficiency(self, snr_db: float) -> float:
        """
        스펙트럼 효율 계산 (bits/s/Hz)

        이는 단위 대역폭당 전송 가능한 비트 수입니다.
        """
        snr_linear = self.db_to_linear(snr_db)
        return np.log2(1 + snr_linear)

    def thermal_noise_power(self, bandwidth_hz: float, temperature_k: float = 290) -> float:
        """
        열잡음 전력 계산 (Johnson-Nyquist Noise)

        N = k × T × B

        Args:
            bandwidth_hz: 대역폭 (Hz)
            temperature_k: 온도 (K), 기본값 290K (약 17°C)

        Returns:
            잡음 전력 (W)
        """
        return self.BOLTZMANN_CONST * temperature_k * bandwidth_hz

    def required_snr_for_rate(self, target_rate_bps: float, bandwidth_hz: float) -> float:
        """
        목표 전송률 달성에 필요한 최소 SNR 계산

        C = B × log₂(1 + SNR)에서 SNR 역계산:
        SNR = 2^(C/B) - 1
        """
        snr_linear = 2 ** (target_rate_bps / bandwidth_hz) - 1
        return self.linear_to_db(snr_linear)

    def required_bandwidth_for_rate(self, target_rate_bps: float, snr_db: float) -> float:
        """
        목표 전송률 달성에 필요한 최소 대역폭 계산

        B = C / log₂(1 + SNR)
        """
        snr_linear = self.db_to_linear(snr_db)
        return target_rate_bps / np.log2(1 + snr_linear)

    def analyze_tradeoff(self, rate_range: Tuple[float, float],
                         snr_range: Tuple[float, float]) -> dict:
        """
        전송률-대역폭-SNR 트레이드오프 분석
        """
        rates = np.linspace(rate_range[0], rate_range[1], 50)
        snrs = np.linspace(snr_range[0], snr_range[1], 50)

        analysis = {
            'rates_gbps': rates / 1e9,
            'snrs_db': snrs,
            'bandwidths_mhz': []
        }

        for rate in rates:
            bw_row = []
            for snr in snrs:
                bw = self.required_bandwidth_for_rate(rate, snr)
                bw_row.append(bw / 1e6)  # MHz 변환
            analysis['bandwidths_mhz'].append(bw_row)

        analysis['bandwidths_mhz'] = np.array(analysis['bandwidths_mhz'])
        return analysis

    def shannon_gap_analysis(self, actual_rate: float, bandwidth: float, snr_db: float) -> dict:
        """
        실제 시스템과 샤논 한계 간의 갭 분석

        Returns:
            theoretical_capacity: 이론적 최대 용량 (bps)
            efficiency: 샤논 한계 대비 효율 (%)
            gap_db: 구현 손실 (dB)
        """
        theoretical = self.calculate_capacity(bandwidth, snr_db)
        efficiency = (actual_rate / theoretical) * 100

        # 실제 시스템이 같은 용량을 내기 위해 필요한 추가 SNR
        required_snr = self.required_snr_for_rate(actual_rate, bandwidth)
        gap_db = snr_db - required_snr

        return {
            'theoretical_capacity_bps': theoretical,
            'actual_rate_bps': actual_rate,
            'efficiency_percent': efficiency,
            'implementation_loss_db': gap_db,
            'spectral_efficiency_bps_per_hz': actual_rate / bandwidth
        }


def main():
    """분석 실행 예시"""
    analyzer = ShannonCapacityAnalyzer()

    print("=" * 60)
    print("샤논-하틀리 채널 용량 분석 리포트")
    print("=" * 60)

    # 5G NR 분석
    print("\n[5G NR mmWave 분석]")
    bandwidth_5g = 100e6  # 100 MHz
    snr_5g = 25  # dB
    capacity_5g = analyzer.calculate_capacity(bandwidth_5g, snr_5g)
    print(f"  대역폭: {bandwidth_5g/1e6:.0f} MHz")
    print(f"  SNR: {snr_5g} dB")
    print(f"  이론적 최대 용량: {capacity_5g/1e6:.2f} Mbps")
    print(f"  스펙트럼 효율: {analyzer.calculate_spectral_efficiency(snr_5g):.2f} bits/s/Hz")

    # Wi-Fi 6 분석
    print("\n[Wi-Fi 6 (802.11ax) 분석]")
    actual_wifi6 = 143e6  # 실제 throughput
    bandwidth_wifi6 = 20e6  # 20 MHz
    snr_wifi6 = 40  # dB
    gap_analysis = analyzer.shannon_gap_analysis(actual_wifi6, bandwidth_wifi6, snr_wifi6)
    print(f"  이론적 용량: {gap_analysis['theoretical_capacity_bps']/1e6:.2f} Mbps")
    print(f"  실제 throughput: {gap_analysis['actual_rate_bps']/1e6:.2f} Mbps")
    print(f"  샤논 한계 효율: {gap_analysis['efficiency_percent']:.1f}%")
    print(f"  구현 손실: {gap_analysis['implementation_loss_db']:.2f} dB")

    # 열잡음 분석
    print("\n[열잡음 전력 분석 @ 290K]")
    noise_power = analyzer.thermal_noise_power(100e6, 290)
    noise_dbm = 10 * np.log10(noise_power * 1000)
    print(f"  100MHz 대역폭 열잡음: {noise_power:.2e} W = {noise_dbm:.2f} dBm")

if __name__ == "__main__":
    main()
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 통신 시스템별 샤논 한계 달성률

| 통신 시스템 | 대역폭 | 전형적 SNR | 이론적 용량 | 실제 성능 | 효율 (%) | 갭 (dB) |
|---|---|---|---|---|---|---|
| **V.92 다이얼업 모뎀** | 4 kHz | 35 dB | 46 kbps | 56 kbps* | 121% | - |
| **ADSL2+** | 2.2 MHz | 20 dB | 15 Mbps | 24 Mbps* | 160% | - |
| **LTE Cat.6** | 20 MHz | 15 dB | 80 Mbps | 300 Mbps** | 375% | - |
| **Wi-Fi 5 (802.11ac)** | 80 MHz | 30 dB | 796 Mbps | 1.3 Gbps** | 163% | - |
| **5G NR (Sub-6)** | 100 MHz | 20 dB | 665 Mbps | 2 Gbps** | 300% | - |
| **DOCSIS 3.1** | 192 MHz | 35 dB | 2.1 Gbps | 1.2 Gbps | 57% | 2.5 |
| **광섬유 (DP-QPSK)** | 50 GHz | 12 dB | 200 Gbps | 100 Gbps | 50% | 1.2 |

\* DMT(Discrete Multi-Tone)로 주파수별 최적화 시 초과 달성 가능
\*\* MIMO, CA(Carrier Aggregation) 적용 시

**핵심 통찰**: MIMO와 같은 공간 다중화 기술은 샤논 공식을 단일 채널로 해석할 때 "한계 초과"처럼 보이지만, 실제로는 독립적인 다중 채널로 간주하므로 샤논 정리를 위배하지 않습니다.

### 과목 융합 관점 분석

**1. 5G/6G 이동통신과의 융합**
- **Massive MIMO**: 공간 자유도(Spatial Degrees of Freedom)를 활용하여 유효 채널 수를 증가시켜, C = M × B × log₂(1 + SNR/M) 형태로 용량 확장
- **mmWave/THz**: 대역폭 B를 GHz~THz 단위로 확장하여 선형적 용량 증대
- **NOMA (Non-Orthogonal Multiple Access)**: power domain을 활용한 다중 접속으로 스펙트럼 효율 향상

**2. 반도체 설계와의 융합**
- **ADC/DAC 해상도**: 높은 SNR을 얻기 위해 12-bit 이상의 고해상도 ADC 필요
- **SERDES 설계**: 112 Gbps PAM-4 SerDES에서 SNR 30dB 이상 유지가 설계 과제
- **전력 효율**: E_b/N₀ (에너지 대 잡음 스펙트럼 밀도) 최적화

**3. 정보보안과의 융합**
- **물리 계층 보안 (Physical Layer Security)**:窃聴者(eavesdropper)의 채널이 정당 수신자보다 열악하다는 가정하에, 샤논 한계 이하의 전송률로 완벽한 비밀 통신(Perfect Secrecy) 가능
- **양자 키 분배 (QKD)**: 양자 역학적 원리로窃聴 감지, 정보이론적 보안 달성

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 위성 통신 링크 예산 설계

**문제 상황**: 정지 궤도(GEO) 위성으로부터 한국 지상국으로 500 Mbps 데이터를 전송하는 링크를 설계해야 합니다.

**주어진 조건**:
- 위성 EIRP: 50 dBW
- 주파수: Ku-band (12 GHz downlink)
- 대역폭: 500 MHz 할당 가능
- 지상국 안테나 이득: 40 dBi
- 거리: 36,000 km (GEO)
- 목표 BER: < 10⁻⁷ (FEC 적용 후)

**기술사의 전략적 의사결정**:

1. **자유 공간 경로 손실 (FSPL) 계산**:
```
FSPL = 20log₁₀(d) + 20log₁₀(f) + 92.45
     = 20log₁₀(36000) + 20log₁₀(12000) + 92.45
     = 91.1 + 81.6 + 92.45
     = 205.2 dB
```

2. **수신 전력 계산**:
```
P_rx = EIRP - FSPL + G_rx
     = 50 - 205.2 + 40
     = -115.2 dBW = -85.2 dBm
```

3. **잡음 전력 계산 (LNB 온도 150K 가정)**:
```
N = k × T × B
  = 1.38×10⁻²³ × 150 × 500×10⁶
  = 1.04×10⁻¹² W = -119.8 dBW
```

4. **SNR 계산**:
```
SNR = P_rx - N = -115.2 - (-119.8) = 4.6 dB
```

5. **샤논 용량 계산**:
```
C = 500×10⁶ × log₂(1 + 10^(4.6/10))
  = 500×10⁶ × 2.17
  = 1.08 Gbps
```

6. **결론**: 이론적 용량 1.08 Gbps > 목표 500 Mbps이므로, 적절한 FEC(LDPC rate 1/2)와 16APSK 변조를 적용하면 목표 달성 가능.

### 도입 시 고려사항 체크리스트

**기술적 고려사항**:
- [ ] 실제 채널 모델 확인 (AWGN 외에 페이딩, 간섭 고려)
- [ ] FEC 오버헤드 감안한 net throughput 계산
- [ ] 하드웨어 구현 손실 (Implementation Loss) 2~3 dB 마진 확보
- [ ] 주파수 규제 (ITU, KCC) 대역폭 제한 확인

**운영/경제적 고려사항**:
- [ ] 전력 증설 비용 vs 대역폭 확장 비용 비교
- [ ] 링크 가용성 (Availability) 99.9% 이상 요구사항
- [ ] 레인 페드(Rain Fade) 마진 (Ku-band: 약 3~6 dB)

### 안티패턴 (Anti-patterns)

**안티패턴 1: 무작정 SNR 증가 시도**
- SNR을 10dB에서 20dB로 증가하면 용량은 약 1.77배 증가하지만, 전력은 10배 필요. 대역폭 확장이 더 경제적일 수 있음.

**안티패턴 2: 샤논 한계 100% 달성 목표**
- 실제 시스템은 70~85% 효율이 현실적. 100% 달성을 위한 복잡도 증가는 ROI 악화.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 항목 | 측정 지표 | 개선 폭 |
|---|---|---|
| **링크 설계 정확도** | 예측 vs 실제 성능 편차 | ±5% 이내 |
| **주파수 효율성** | bits/s/Hz | 30~50% 향상 (최적화 시) |
| **CAPEX 절감** | 기지국/위성 당 투자비 | 15~25% 절감 |
| **전력 효율** | W/Mbps | 20~30% 개선 |

### 미래 전망 및 진화 방향

**1. 6G 및 THz 통신**
- 0.1~10 THz 대역 활용으로 대역폭 B를 100배 이상 확장
- 새로운 잡음 모델 (phase noise, molecular absorption) 고려 필요

**2. 양자 통신의 샤논 한계**
- 양자 채널에서의 고전적 정보 용량 (Holevo bound)
- 양자 얽힘(Entanglement) 활용 시 용량 증대 가능성

**3. AI 기반 적응형 부호화**
- 채널 상태에 따라 실시간으로 변조/부호화 rate 조정
- 샤논 한계에 95% 이상 근접하는 실시간 시스템 구현

### ※ 참고 표준/가이드

- **C.E. Shannon (1948)**: "A Mathematical Theory of Communication", Bell System Technical Journal
- **ITU-R P.372**: Radio noise (잡음 모델 표준)
- **3GPP TR 38.802**: Study on New Radio Access Technology Physical Layer Aspects
- **IEEE 802.11ax**: High Efficiency WLAN (Wi-Fi 6) Specification

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [나이퀴스트 정리](@/studynotes/03_network/01_fundamentals/nyquist_sampling.md) : 무잡음 채널에서의 최대 전송률 정리.
- [변조 기술 (QAM, PSK)](@/studynotes/03_network/01_fundamentals/modulation_qam_psk.md) : 스펙트럼 효율 향상을 위한 고차 변조.
- [MIMO 시스템](@/studynotes/03_network/05_wireless/mimo_systems.md) : 공간 다중화를 통한 용량 확장.
- [FEC 오류 정정](@/studynotes/03_network/04_data_link/fec_forward_error_correction.md) : 샤논 한계 근접을 위한 채널 부호화.
- [광섬유 통신 용량](@/studynotes/03_network/03_physical/optical_fiber_capacity.md) : 광통신에서의 샤논 한계 적용.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 샤논-하틀리 정리는 **'파이프의 물 흐름 법칙'**이에요. 파이프 굵기(대역폭)가 클수록, 물이 깨끗할수록(잡음이 적을수록) 더 많은 물을 보낼 수 있답니다.
2. 하지만 파이프가 아무리 굵어도 **'물리적 한계'**가 있어요. 아무리 노력해도 이 한계 이상으로는 물을 보낼 수 없답니다.
3. 과학자 삼촌들은 이 한계에 최대한 가까워지려고, 파이프를 여러 개 놓거나(MIMO), 물을 압축해서(고차 변조) 보내는 똑똑한 방법들을 연구하고 있어요.
