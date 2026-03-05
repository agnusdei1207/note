+++
title = "선로 부호화 (Line Coding: NRZ, RZ, Manchester)"
date = 2024-05-18
description = "디지털 데이터를 디지털 신호로 변환하는 선로 부호화 기술의 심층 분석 - NRZ, RZ, Manchester 부호화의 원리, 장단점, 그리고 실무적용"
weight = 15
[taxonomies]
categories = ["studynotes-network"]
tags = ["Line Coding", "NRZ", "RZ", "Manchester", "Digital Signal", "Encoding"]
+++

# 선로 부호화 (Line Coding: NRZ, RZ, Manchester)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 선로 부호화(Line Coding)는 디지털 데이터(0과 1의 비트 열)를 전송 매체에 적합한 디지털 신호 파형으로 변환하는 기술로, 신호의 동기화 유지, 직류 성분 제거, 대역폭 효율성 등을 달성하기 위해 다양한 부호화 방식이 개발되었습니다.
> 2. **가치**: 적절한 선로 부호화 선택은 전송 거리, 오류율(BER), 클록 동기화 복잡도, 전력 소모 등 네트워크 성능 지표를 30~50% 이상 개선할 수 있으며, 이더넷, USB, SATA 등 현대 디지털 통신의 기반이 됩니다.
> 3. **융합**: PHY(물리 계층) 칩 설계, 광섬유 통신의 광변조, 무선 통신의 심볼 매핑 등 다양한 통신 시스템과 연계되며, 특히 고속 직렬 버스(PCIe, USB 3.0+)의 신호 무결성 설계에 필수적입니다.

---

## Ⅰ. 개요 (Context & Background)

선로 부호화(Line Coding)는 디지털 통신 시스템의 송신측에서 디지털 데이터(이산적인 비트 열)를 전송 매체(구리선, 광섬유, 무선)를 통해 전송 가능한 디지털 신호(전압 레벨, 빛의 세기, 위상 등)로 변환하는 기술입니다. 이 과정은 단순한 0과 1의 매핑을 넘어, 신호의 스펙트럼 특성, 직류(DC) 성분, 동기화 능력, 오류 검출 능력 등 다각도의 전기적 특성을 고려하여 설계됩니다.

**💡 비유**: 선로 부호화는 모스 부호와 같습니다. 단순히 'A'라는 글자를 표현할 때도 '·-·-'(모스 부호)로 변환하여 전송하듯, 디지털 비트 '1'과 '0'을 전선에 흐를 수 있는 전압 패턴(예: +5V와 -5V, 또는 빛의 깜빡임)으로 변환하는 규칙입니다. 어떤 규칙을 쓰느냐에 따라 상대방이 신호를 얼마나 정확히 해석할 수 있는지, 얼마나 멀리 보낼 수 있는지가 결정됩니다.

**등장 배경 및 발전 과정**:
1. **기존 기술의 치명적 한계점**: 초기 디지털 통신에서는 단순히 비트 '1'을 고전압, '0'을 저전압으로 매핑하는 단극성(Unipolar) NRZ 방식을 사용했습니다. 그러나 이 방식은 연속된 '1'이나 '0'이 전송될 때 신호 레벨이 변하지 않아 수신측에서 클록 동기화를 잃는 문제(Clock Recovery Failure)와 전송선에 직류 성분이 축적되어 신호 왜곡이 발생하는 문제(DC Wander)가 심각했습니다.
2. **혁신적 패러다임 변화**: 이를 해결하기 위해 1960~1970년대에 RZ(Return to Zero), Manchester, AMI(Alternate Mark Inversion) 등의 부호화 방식이 개발되었습니다. 특히 Manchester 부호화는 이더넷(10BASE-T)의 표준으로 채택되어 동기화 신뢰성을 획기적으로 높였습니다.
3. **비즈니스적 요구사항**: 현대의 고속 통신(10Gbps 이상)에서는 대역폭 효율성이 극대화된 64b/66b, PAM-4(Pulse Amplitude Modulation) 등의 고급 부호화 기술이 요구되며, 이는 데이터센터, 5G 백홀, HPC(고성능 컴퓨팅) 환경에서 필수적인 기술 경쟁력이 되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: 주요 선로 부호화 방식 비교

| 부호화 방식 | 파형 특성 | 동기화 능력 | DC 성분 | 대역폭 요구 | 주요 적용 분야 |
|---|---|---|---|---|---|
| **NRZ-L (Non-Return to Zero Level)** | 1=고전압, 0=저전압 (레벨 고정) | 낮음 (연속 비트 시 클록 상실) | 존재 (데이터 패턴 의존) | 좁음 (1비트당 1Hz) | 저속 시리얼 통신, SATA |
| **NRZ-I (Non-Return to Zero Inverted)** | 1=레벨 전환, 0=레벨 유지 | 중간 (1의 밀도에 의존) | 존재 | 좁음 | USB 2.0, PCIe Gen1/2 |
| **RZ (Return to Zero)** | 비트 중간에 항상 0으로 복귀 | 높음 (비트마다 전이 발생) | 제거 가능 | 넓음 (2배 대역폭) | 광통신, 고신뢰 시스템 |
| **Manchester (IEEE 802.3)** | 비트 중간 필수 전이 (1=Low→High, 0=High→Low) | 매우 높음 (자체 동기화) | 완전 제거 | 넓음 (2배 대역폭) | 10BASE-T 이더넷, RFID |
| **Differential Manchester** | 비트 시작점 전이 여부로 0/1 구분 | 매우 높음 | 완전 제거 | 넓음 | 토큰 링 (IEEE 802.5) |
| **AMI (Alternate Mark Inversion)** | 1=교대로 +V/-V, 0=0V | 중간 | 완전 제거 | 중간 | T1/E1 디지털 전화망 |

### 정교한 구조 다이어그램: 파형 비교

```ascii
Data Bits:      1     0     1     1     0     0     1     0
             |_____|_____|_____|_____|_____|_____|_____|_____|

NRZ-L:       |█████|     |█████|█████|     |     |█████|     |
             |     |     |     |     |     |     |     |     |
             |_____|_____|_____|_____|_____|_____|_____|_____|

NRZ-I:       |█████|█████|     |█████|█████|█████|     |     |
(Initial=0)  |     |     |     |     |     |     |     |     |
             |_____|_____|_____|_____|_____|_____|_____|_____|

RZ:          |███  |     |███  |███  |     |     |███  |     |
             |   ██|     |   ██|   ██|     |     |   ██|     |
             |_____|_____|_____|_____|_____|_____|_____|_____|

Manchester:  |  ███|█████|███  |  ███|█████|█████|  ███|█████|
(Biphase)    |███  |     |   ██|███  |     |     |███  |     |
             |_____|_____|_____|_____|_____|_____|_____|_____|

              ^-- 중간 전이 (동기화 포인트) --^
```

### 심층 동작 원리: 각 방식의 상세 메커니즘

**1. NRZ-L (Non-Return to Zero Level)**
NRZ-L은 가장 직관적인 부호화 방식으로, 비트 '1'을 양의 전압(+V), '0'을 음의 전압(-V) 또는 0V로 매핑합니다. 'Non-Return to Zero'라는 명칭은 비트 구간 내에서 전압 레벨이 0으로 돌아오지 않음을 의미합니다.

```
장점:
- 구현이 간단하여 하드웨어 복잡도가 낮음
- 대역폭 효율이 높음 (1비트당 최소 대역폭)

단점:
- 연속된 0이나 1 전송 시 신호 전이가 없어 클록 동기화 불가
- 데이터 패턴에 따른 DC 성분 축적
- 긴 연속 동일 비트 시 baseline wandering 발생
```

**2. NRZ-I (Non-Return to Zero Inverted)**
NRZ-I는 비트 '1'이 입력될 때마다 전압 레벨을 반전시키고, '0'은 이전 레벨을 유지합니다. 이는 차분 부호화(Differential Encoding)의 일종으로, 극성 반전에 강건합니다.

```
동작 규칙:
- bit = 1: 현재 레벨 반전 (0→1 또는 1→0)
- bit = 0: 현재 레벨 유지

장점:
- 극성 반전(Polarity Reversal)에 영향을 받지 않음
- 1의 밀도가 높을 때 동기화 성능 향상

단점:
- 연속된 0 전송 시 여전히 동기화 문제
- DC 성분 문제 미해결
```

**3. RZ (Return to Zero)**
RZ 부호화는 각 비트 구간의 전반부에 신호를 전송하고, 후반부에는 항상 0 레벨로 복귀합니다. 비트 '1'은 +V → 0, '0'은 -V → 0으로 표현됩니다.

```
동작 메커니즘:
- bit = 1: |+V___| (전반부 +V, 후반부 0)
- bit = 0: |-V___| (전반부 -V, 후반부 0)

장점:
- 모든 비트에서 신호 전이 발생 → 자체 클록 동기화 가능
- DC 성분 제어 용이

단점:
- 대역폭이 2배 필요 (동일 데이터 전송 시)
- 송신 전력 효율 저하 (유휴 시간 존재)
```

**4. Manchester 부호화 (Biphase Coding)**
Manchester 부호화는 각 비트 구간의 정중앙에서 반드시 전압 전이를 발생시킵니다. 이 전이의 방향으로 0과 1을 구분합니다.

```
IEEE 802.3 Convention (이더넷):
- bit = 1: Low → High (비트 중간에서 상승 에지)
- bit = 0: High → Low (비트 중간에서 하강 에지)

G.E. Thomas Convention:
- bit = 1: High → Low
- bit = 0: Low → High

특징:
- 비트당 항상 1회의 전이 보장 → 클록 추출 용이
- DC 성분 완전 제거 (평균 전압 = 0)
- 오류 검출 가능 (전이 미발생 시 오류)
```

### 핵심 수학적 분석: 파워 스펙트럼 밀도 (PSD)

```
NRZ의 PSD (Single-Sided):
S(f) = A²·Tb · sinc²(π·f·Tb)  [Tb = 비트 주기, A = 진폭]

- 첫 번째 널(null) 위치: f = 1/Tb (비트율)
- 주파수 성분이 0 Hz(DC)에서 최대

Manchester의 PSD:
S(f) = A²·Tb · sinc⁴(π·f·Tb/2)
     = A²·Tb · [sin(π·f·Tb/2)/(π·f·Tb/2)]⁴

- 첫 번째 널 위치: f = 2/Tb (비트율의 2배)
- DC 성분이 0 (f=0에서 sinc⁴=0)
- 대역폭은 NRZ의 약 2배
```

### 실무 코드: 선로 부호화 시뮬레이션 (Python)

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

class LineCodingSimulator:
    """선로 부호화 방식별 파형 생성 및 분석 클래스"""

    def __init__(self, bitrate=1e6):  # 1 Mbps 기본
        self.bitrate = bitrate
        self.bit_period = 1 / bitrate

    def generate_bits(self, num_bits, pattern='random'):
        """테스트 비트 열 생성"""
        if pattern == 'random':
            return np.random.randint(0, 2, num_bits)
        elif pattern == 'worst_case':  # 동기화 테스트용
            return np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0] * (num_bits // 10))
        return np.ones(num_bits, dtype=int)

    def nrz_l_encode(self, bits, samples_per_bit=100):
        """NRZ-L 부호화"""
        signal = np.zeros(len(bits) * samples_per_bit)
        for i, bit in enumerate(bits):
            signal[i*samples_per_bit:(i+1)*samples_per_bit] = 2*bit - 1  # +1 or -1
        return signal

    def nrz_i_encode(self, bits, samples_per_bit=100):
        """NRZ-I 부호화 (차분 부호화)"""
        signal = np.zeros(len(bits) * samples_per_bit)
        current_level = -1  # 초기 레벨
        for i, bit in enumerate(bits):
            if bit == 1:
                current_level = -current_level  # 레벨 반전
            signal[i*samples_per_bit:(i+1)*samples_per_bit] = current_level
        return signal

    def manchester_encode(self, bits, samples_per_bit=100):
        """Manchester 부호화 (IEEE 802.3)"""
        signal = np.zeros(len(bits) * samples_per_bit)
        half = samples_per_bit // 2
        for i, bit in enumerate(bits):
            if bit == 1:  # Low → High
                signal[i*samples_per_bit:i*samples_per_bit+half] = -1
                signal[i*samples_per_bit+half:(i+1)*samples_per_bit] = 1
            else:  # High → Low
                signal[i*samples_per_bit:i*samples_per_bit+half] = 1
                signal[i*samples_per_bit+half:(i+1)*samples_per_bit] = -1
        return signal

    def analyze_spectrum(self, signal, fs):
        """주파수 스펙트럼 분석 (FFT)"""
        n = len(signal)
        freq = np.fft.fftfreq(n, 1/fs)[:n//2]
        spectrum = np.abs(np.fft.fft(signal))[:n//2] * 2 / n
        return freq, spectrum

    def analyze_dc_component(self, signal):
        """DC 성분 분석 (평균 전압)"""
        return np.mean(signal)

    def count_transitions(self, signal):
        """신호 전이 횟수 계산 (동기화 척도)"""
        transitions = np.sum(np.abs(np.diff(signal)) > 0.5)
        return transitions

# 실행 예시
if __name__ == "__main__":
    simulator = LineCodingSimulator(bitrate=1e6)
    bits = simulator.generate_bits(20, pattern='worst_case')

    nrz_l = simulator.nrz_l_encode(bits)
    nrz_i = simulator.nrz_i_encode(bits)
    manchester = simulator.manchester_encode(bits)

    print(f"[분석 결과]")
    print(f"NRZ-L DC 성분: {simulator.analyze_dc_component(nrz_l):.4f}")
    print(f"NRZ-I DC 성분: {simulator.analyze_dc_component(nrz_i):.4f}")
    print(f"Manchester DC 성분: {simulator.analyze_dc_component(manchester):.4f}")
    print(f"\nNRZ-L 전이 횟수: {simulator.count_transitions(nrz_l)}")
    print(f"NRZ-I 전이 횟수: {simulator.count_transitions(nrz_i)}")
    print(f"Manchester 전이 횟수: {simulator.count_transitions(manchester)}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교표: 성능 지표 기반 분석

| 평가 지표 | NRZ-L | NRZ-I | RZ | Manchester | AMI | 8B/10B |
|---|---|---|---|---|---|---|
| **대역폭 효율 (bits/Hz)** | 2.0 (최고) | 2.0 | 1.0 | 1.0 | 2.0 | 0.8 |
| **DC 성분** | 있음 | 있음 | 제거됨 | 완전 제거 | 완전 제거 | 제거됨 |
| **동기화 능력** | 낮음 | 중간 | 높음 | 매우 높음 | 중간 | 높음 |
| **오류 검출** | 없음 | 없음 | 제한적 | 가능 | 가능 | 강력 |
| **구현 복잡도** | 낮음 | 낮음 | 중간 | 중간 | 중간 | 높음 |
| **EMI/RFI 저항성** | 낮음 | 낮음 | 중간 | 높음 | 높음 | 높음 |
| **최장 연속 동일 극성** | 무제한 | 무제한 | 1비트 | 1비트 | 제한됨 | 5비트 |

### 과목 융합 관점 분석

**1. 물리 계층(PHY) 칩 설계와의 융합**
- **SerDes (Serializer/Deserializer)**: 고속 직렬 통신에서는 NRZ 또는 PAM-4를 사용하며, 클록 복구를 위한 CDR(Clock and Data Recovery) 회로가 필수적입니다. Manchester의 자체 동기화 특성은 CDR 복잡도를 낮추지만, 대역폭 비효율로 인해 1Gbps 이상에서는 8B/10B 또는 64B/66B가 선호됩니다.

**2. 운영체제 커널 네트워크 스택과의 융합**
- **TTY/시리얼 드라이버**: UART(Universal Asynchronous Receiver Transmitter)는 NRZ 부호화를 기본으로 사용하며, Start/Stop 비트를 통해 동기화를 수행합니다. Linux 커널의 `drivers/tty/serial/` 디렉토리에서 이 구현을 확인할 수 있습니다.

**3. 오류 정정 코드(ECC)와의 융합**
- **Scrambling + FEC**: 연속 동일 비트 문제를 완화하기 위해 스크램블러(Scrambler, LFSR 기반)를 NRZ와 결합하고, 추가로 FEC(Forward Error Correction) 코드를 적용하여 신뢰성을 확보합니다. 이는 DVB, DOCSIS 표준에서 사용됩니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 산업용 제어 네트워크 설계

**문제 상황**: 자동차 제조 라인의 PLC(Programmable Logic Controller) 네트워크를 설계해야 합니다. 환경 특성:
- 노이즈 환경 (용접 로봇, 대형 모터)
- 최대 100m 전송 거리
- 10 Mbps 데이터 전송률 요구
- 실시간성 보장 (지연 < 1ms)

**기술사의 전략적 의사결정**:

1. **부호화 방식 선택**: Manchester 부호화 채택
   - 이유: 강력한 전자기 노이즈 환경에서 DC 성분이 없고, 자체 동기화로 클록 복구 신뢰성 확보
   - 대안 기각: NRZ는 노이즈 환경에서 동기화 상실 위험

2. **대역폭 보정**: 20 MHz 이상의 케이블 및 커넥터 선정
   - Manchester는 10 Mbps 데이터 전송에 20 MHz 대역폭 필요

3. **케이블 선정**: STP(Shielded Twisted Pair) Cat 6 이상
   - 차폐(Shielding)로 EMI/RFI 차단

4. **추가 보안 조치**: Differential Manchester + 격리 트랜스포머
   - 접지 루프(Ground Loop) 방지 및 서지 보호

### 도입 시 고려사항 체크리스트

**기술적 고려사항**:
- [ ] 비트율 대 대역폭 비율 계산 (NRZ: 1:1, Manchester: 1:2)
- [ ] 전송 매체의 주파수 응답 특성 확인
- [ ] 클록 복구 방법 결정 (자체 동기화 vs 별도 클록 라인)
- [ ] DC 차단 커패시터 필요성 평가

**운영/보안적 고려사항**:
- [ ] EMI/EMC 규정 준수 여부 (FCC, CE)
- [ ] 장기 운영 시 신호 품질 저하 모니터링 계획
- [ ] 핫 스왑(Hot Swap) 시 부호화 상태 유지 방안

### 안티패턴 (Anti-patterns)

**안티패턴 1: 고속 통신에서의 Manchester 사용**
- 1Gbps 이상의 속도에서 Manchester 부호화는 대역폭 낭비가 심각합니다. PCIe Gen3 (8GT/s) 이상에서는 128b/130b를 사용하여 DC 균형과 동기화를 효율적으로 달성합니다.

**안티패턴 2: 장거리 전송에서의 NRZ-L 사용**
- 수 km 이상의 전송에서는 NRZ-L의 DC 성분이 신호 왜곡을 유발합니다. 이 경우 AMI, HDB3, 4B/5B 등 DC 균형 부호화를 사용해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 항목 | 측정 지표 | 개선 폭 |
|---|---|---|
| **전송 신뢰성** | BER (Bit Error Rate) | 10⁻⁶ → 10⁻⁹ (적절한 부호화 선택 시) |
| **동기화 안정성** | 클록 추출 오류율 | 95% → 99.9% (Manchester vs NRZ) |
| **EMI 방사** | dBμV/m @ 3m | 6~10 dB 감소 (DC 균형 부호화) |
| **전력 소모** | mW/Mbps | 15~25% 절감 (단순 부호화 방식) |

### 미래 전망 및 진화 방향

**1. PAM-4 (4-Level Pulse Amplitude Modulation)**
- 400GbE, 800GbE 이더넷에서 채택되는 차세대 부호화로, 2비트를 4개의 전압 레벨로 매핑하여 대역폭 효율을 2배 향상시킵니다.

**2. DMT (Discrete Multi-Tone)**
- xDSL, G.fast에서 사용되는 다중 반송파 부호화로, 주파수 선택적 페이딩 채널에서 최적의 성능을 발휘합니다.

**3. 양자 통신용 부호화**
- QKD(Quantum Key Distribution) 시스템에서는 단일 광자의 편광 상태를 부호화에 사용하는 BB84 프로토콜이 활용됩니다.

### ※ 참고 표준/가이드

- **IEEE 802.3**: Ethernet Physical Layer Specifications (Manchester for 10BASE-T)
- **ITU-T G.703**: Physical/electrical characteristics of hierarchical digital interfaces (AMI, HDB3)
- **ANSI X3.230**: Fibre Channel Physical and Signaling Interface (8B/10B)
- **PCI Express Base Specification**: 8b/10b (Gen1/2), 128b/130b (Gen3+)

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [대역폭 및 샤논 용량](@/studynotes/03_network/01_fundamentals/bandwidth_shannon_capacity.md) : 대역폭 효율과 채널 용량의 이론적 기반 이해.
- [PCM 및 펄스 변조](@/studynotes/03_network/01_fundamentals/pcm_pulse_modulation.md) : 아날로그-디지털 변환의 기본 원리.
- [이더넷 물리 계층](@/studynotes/03_network/01_fundamentals/ethernet_phy.md) : 실제 이더넷에서 사용되는 부호화 표준.
- [오류 검출 및 정정](@/studynotes/03_network/04_data_link/error_detection_correction.md) : 부호화와 결합되는 오류 제어 기술.
- [광섬유 통신 변조](@/studynotes/03_network/03_physical/optical_modulation.md) : 광통신에서의 디지털-광신호 변환.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 선로 부호화는 **'컴퓨터의 모스 부호'**예요. 0과 1이라는 숫자를 전선에 흐를 수 있는 전기 신호로 바꾸는 규칙이랍니다.
2. Manchester 방식은 **'깜빡이는 불빛'**처럼 항상 신호가 변해서, 상대방이 "어, 신호가 오고 있구나!" 하고 쉽게 알 수 있어요.
3. 반면 NRZ는 **'계속 켜진 전구'**처럼 변화가 없어서, 상대방이 "아직도 신호가 오나? 아니면 끝났나?" 헷갈릴 수 있어요.
