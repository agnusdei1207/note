+++
title = "채널 용량 (Shannon-Hartley 정리)"
date = 2024-05-18
description = "Shannon-Hartley 정리에 의한 채널 용량 계산, Nyquist 한계, SNR, 대역폭과 전송 속도의 관계 심층 분석"
weight = 18
[taxonomies]
categories = ["studynotes-03_network"]
tags = ["Shannon", "Nyquist", "ChannelCapacity", "SNR", "Bandwidth", "InformationTheory"]
+++

# 채널 용량 (Shannon-Hartley 정리)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 채널 용량(Channel Capacity)은 주어진 통신 채널에서 오류 없이 전송할 수 있는 최대 정보 전송 속도의 이론적 상한으로, Claude Shannon이 1948년 제시한 Shannon-Hartley 정리에 의해 대역폭(B), 신호 대 잡음비(SNR)의 함수로 정의됩니다.
> 2. **가치**: 통신 시스템 설계의 근본적인 한계를 제시하여, 무제한적인 성능 향상 불가능함을 증명하고, 5G/6G, Wi-Fi, 광통신 등 모든 현대 통신 시스템의 성능 목표 설정의 기준이 됩니다.
> 3. **융합**: MIMO, OFDM, LDPC, Turbo Code 등 모든 현대 통신 기술은 Shannon 한계에 근접하기 위해 개발되었으며, 양자 통신은 이 한계를 돌파할 수 있는 잠재적 기술로 연구되고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

Shannon-Hartley 정리는 정보 이론(Information Theory)의 핵심 정리로, 잡음이 있는 아날로그 통신 채널의 최대 데이터 전송 속도(채널 용량)를 계산합니다.

**핵심 공식**:
```
C = B × log₂(1 + S/N)

여기서:
- C: 채널 용량 (bits/sec)
- B: 채널 대역폭 (Hz)
- S: 신호 전력 (Watts)
- N: 잡음 전력 (Watts)
- S/N: 신호 대 잡음비 (Signal-to-Noise Ratio, 무단위 또는 dB)
```

**💡 비유**: 채널 용량은 **'도로의 최대 교통량'**과 같습니다.
- **대역폭(B)**: 도로의 차선 수 (넓을수록 많은 차량 통과 가능)
- **SNR(S/N)**: 도로 상태 (잡음이 적고 신호가 명확할수록 더 빠르고 밀집하게 주행 가능)
- **용량(C)**: 단위 시간당 통과할 수 있는 최대 차량 수

**Nyquist 무잡음 채널 용량**:
```
C = 2B × log₂(M)

여기서 M: 신호 레벨 수 (예: 16-QAM에서 M=16)
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 대역폭, SNR, 채널 용량 관계표

| 대역폭 (B) | SNR (dB) | SNR (선형) | 채널 용량 C (bps) | 응용 |
|-----------|----------|-----------|------------------|------|
| 3 kHz | 30 dB | 1000 | ~30 kbps | 전화 음성 |
| 200 kHz | 40 dB | 10000 | ~2.66 Mbps | FM 라디오 데이터 |
| 6 MHz | 20 dB | 100 | ~40 Mbps | 지상파 TV |
| 20 MHz | 30 dB | 1000 | ~200 Mbps | LTE 채널 |
| 100 MHz | 40 dB | 10000 | ~1.33 Gbps | 5G NR |
| 1 GHz | 50 dB | 100000 | ~16.6 Gbps | Wi-Fi 6 |

### 핵심 코드: Shannon 용량 계산기 (Python)

```python
import numpy as np

def shannon_capacity(bandwidth_hz, snr_db):
    """Shannon 채널 용량 계산"""
    snr_linear = 10 ** (snr_db / 10)
    capacity = bandwidth_hz * np.log2(1 + snr_linear)
    return capacity

def snr_from_capacity(bandwidth_hz, capacity_bps):
    """역계산: 용량으로부터 필요 SNR"""
    snr_linear = 2 ** (capacity_bps / bandwidth_hz) - 1
    snr_db = 10 * np.log10(snr_linear)
    return snr_db

# 예시
print(f"5G 100MHz 채널, 30dB SNR: {shannon_capacity(100e6, 30)/1e9:.2f} Gbps")
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### Shannon 한계 달성 기술

| 기술 | 목표 | 달성률 | 방식 |
|------|------|--------|------|
| LDPC 코드 | FEC | ~0.0045 dB | 선형 블록 코드 |
| Turbo 코드 | FEC | ~0.5 dB | 반복 복호화 |
| 1024-QAM | 변조 | 높은 SNR 필요 | 10 bits/symbol |
| MIMO | 공간 다중화 | 선형 증가 | 다중 안테나 |

---

## Ⅳ. 실무 적용

### 5G NR 설계 시 고려사항
- FR1 (Sub-6GHz): 100MHz 대역폭 → ~1Gbps 이론적 최대
- FR2 (mmWave): 400MHz 대역폭 → ~10Gbps 이론적 최대
- 실제는 오버헤드, 채널 추정 오차로 50~70% 달성

---

## Ⅴ. 기대효과 및 결론

### 정량적 기대효과
- 통신 시스템 설계 시 불가능한 목표 설정 방지
- 투자 대비 최대 성능 예측 가능

### ※ 참고 표준
- **Shannon, C.E. (1948)**: "A Mathematical Theory of Communication"
- **Hartley, R.V.L. (1928)**: "Transmission of Information"

---

## 📌 관련 개념 맵
- [변조 기법(ASK/FSK/PSK/QAM)](./modulation_ask_fsk_psk_qam.md): 대역폭 효율적 사용
- [오류 정정 코드(LDPC/Turbo)](./error_correction_codes.md): Shannon 한계 접근
- [MIMO 시스템](../05_wireless/wireless_5g_6g.md): 공간 분할로 용량 확장

---

### 👶 어린이를 위한 3줄 비유
1. **채널 용량**은 도로가 1초에 보낼 수 있는 최대 차 수예요.
2. 도로가 넓고(**대역폭**), 날씨가 맑으면(**SNR**) 더 많은 차가 지나갈 수 있어요.
3. 아무리 좋은 자동차를 만들어도, 도로의 한계를 넘을 수는 없답니다!
