+++
title = "라인 부호화 기법 (Line Coding)"
date = 2024-05-18
description = "디지털 데이터를 디지털 신호로 변환하는 라인 부호화 기법의 원리, NRZ/RZ/Manchester/AMI 방식의 심층 분석 및 성능 비교"
weight = 15
[taxonomies]
categories = ["studynotes-03_network"]
tags = ["LineCoding", "NRZ", "Manchester", "AMI", "DigitalSignal", "Encoding"]
+++

# 라인 부호화 기법 (Line Coding Techniques)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 라인 부호화(Line Coding)는 디지털 비트 스트림을 전송 매체에 적합한 디지털 신호 파형으로 변환하는 기법으로, 직류 성분 제거, 동기화 보장, 대역폭 효율성, 오류 검출 능력을 핵심 설계 기준으로 합니다.
> 2. **가치**: 적절한 라인 부호화 선택은 전송 거리 연장(신호 감쇠 최소화), 클럭 복원 용이성(비트 동기화), 에러율 저감(BER, Bit Error Rate)에 결정적 영향을 미쳐 통신 시스템의 전체 성능을 30~50%까지 향상시킵니다.
> 3. **융합**: 현대의 고속 이더넷(1000BASE-T, 10GBASE-T), 광통신, USB, PCIe 등의 직렬 통신 인터페이스는 4B/5B, 8B/10B, 64B/66B와 같은 블록 부호화와 PAM(Pulse Amplitude Modulation)을 결합한 하이브리드 부호화 방식을 채택하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

라인 부호화(Line Coding) 또는 디지털-디지털 변조(Digital-to-Digital Encoding)는 이진 비트(0과 1)의 시퀀스를 전송 매체(구리선, 광섬유, 무선)를 통해 전송 가능한 디지털 신호 파형으로 변환하는 기술입니다. 이는 물리 계층(Physical Layer, OSI L1)의 핵심 기능으로, 단순한 0/1의 논리적 표현을 물리적 전압 레벨, 광 강도, 또는 위상과 같은 전송 가능한 신호로 매핑합니다.

**💡 비유**: 라인 부호화는 **'모스 부호'**와 같습니다. 단순히 A, B, C라는 문자(비트)를 전달하는 것이 아니라, 짧은 신호(·)와 긴 신호(—)의 조합으로 변환하여 전신선을 통해 전송할 수 있는 전기 신호로 바꾸는 과정입니다. 모스 부호에서 문자 간 구분이 필요하듯, 라인 부호화에서도 비트 경계를 식별하는 동기화가 핵심 과제입니다.

**등장 배경 및 발전 과정**:
1. **기존 기술의 한계 - 직류 성분(DC Component)**: 단순한 Unipolar NRZ(0V=0, +5V=1) 방식은 연속된 1이나 0이 전송될 때 평균 전압이 치우쳐, 직류 성분이 발생합니다. 이는 변압기나 커패시터와 같은 AC 결합 소자를 통과할 수 없어 장거리 전송이 불가능합니다.
2. **동기화 문제(Synchronization)**: 연속된 동일 비트가 길게 이어지면 신호 레벨의 변화가 없어 수신측에서 클럭을 복원할 수 없습니다. 이로 인해 비트 경계를 잃어버리는 '비트 슬립(Bit Slip)' 현상이 발생합니다.
3. **혁신적 해결책**: 맨체스터 부호화(Manchester), AMI(Alternate Mark Inversion)와 같은 기법은 신호 레벨의 주기적 변화를 강제하여 동기화 정보를 내장하고, 직류 성분을 제거하여 장거리 전송과 클럭 복원을 동시에 해결했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: 라인 부호화 기법 분류 체계

| 분류 | 부호화 방식 | 상세 원리 및 특징 | DC 성분 | 동기화 능력 | 대역폭 효율 | 주요 적용 |
|------|------------|-------------------|---------|------------|------------|-----------|
| **단극성(Unipolar)** | NRZ-L | 0=0V, 1=+V (High 레벨만 사용) | 존재 | 낮음 | 높음 | 내부 회로 |
| **극성(Polar)** | NRZ-L | 0=+V, 1=-V (정/부 레벨 사용) | 적음 | 낮음 | 높음 | 단거리 통신 |
| **극성(Polar)** | NRZ-I | 1에서 레벨 반전, 0은 유지 | 적음 | 낮음 | 높음 | USB |
| **양극성(Bipolar)** | AMI | 0=0V, 1=+V/-V 교대 | 없음 | 보통 | 높음 | T1/E1 전화망 |
| **양극성(Bipolar)** | Pseudoternary | 1=0V, 0=+V/-V 교대 | 없음 | 보통 | 높음 | 특수 통신 |
| **복귀형(Return-to-Zero)** | RZ | 비트 중간에 0V로 복귀 | 존재 | 높음 | 낮음 | 광통신 |
| **맨체스터** | Manchester | 비트 중간 반전 (0: High→Low, 1: Low→High) | 없음 | 매우 높음 | 낮음 | 이더넷 10BASE-T |
| **차분 맨체스터** | Diff Manchester | 비트 시작 반전 여부로 0/1 구분 | 없음 | 매우 높음 | 낮음 | 토큰 링 |
| **블록 부호화** | 4B/5B | 4비트를 5비트로 매핑 (DC 밸런스) | 없음 | 높음 | 보통 | 100BASE-TX |
| **블록 부호화** | 8B/10B | 8비트를 10비트로 매핑 | 없음 | 높음 | 보통 | Gigabit Ethernet |
| **스크램블링** | B8ZS | 8개 연속 0을 위반 코드로 대체 | 없음 | 높음 | 높음 | T1 WAN |
| **스크램블링** | HDB3 | 4개 연속 0을 위반 코드로 대체 | 없음 | 높음 | 높음 | E1 WAN |

### 정교한 구조 다이어그램: 주요 라인 부호화 파형 비교

```ascii
================================================================================
[ Line Coding Waveform Comparison - Binary Sequence: 1 0 1 1 0 0 0 1 ]
================================================================================

Original Bits:     1     0     1     1     0     0     0     1
                   |     |     |     |     |     |     |     |
Time Base:    |----|-----|-----|-----|-----|-----|-----|-----|---->

+V ───────────┐     ┌──────────┐                 ┌──────────────────
              │     │          │                 │
0V ───────────┼─────┼──────────┼─────────────────┼──────────────────
              │     │          │                 │
-V            └─────┘          └─────────────────┘
              [NRZ-L: Non-Return to Zero Level] (0=+V, 1=-V)
              DC 성분 존재, 동기화 어려움

+V ───────────┐     ┐     ┌──────────                 ┌──────────────
              │     │     │                           │
0V ───────────┼─────┼─────┼───────────────────────────┼──────────────
              │     │     │                           │
-V            └─────┘     └───────────────────────────┘
              [NRZ-I: Non-Return to Zero Inverted]
              1에서 반전, 0은 유지 (연속 0에서 동기화 문제)

+V ───────────┐           ┐     ┐                 ┌──────────────────
              │     ┌─────│─────│─────────────────│
0V ───────────┼─────┼─────┼─────┼─────────────────┼──────────────────
              │     │     │     │                 │
-V            └─────┘     └─────┘                 └──────────────────
              [AMI: Alternate Mark Inversion]
              1은 +V/-V 교대, DC 성분 제거, 연속 0에서 동기화 문제

+V ───────┐  ┌──┐  ┌──────┐  ┌──────┐        ┌──────┐  ┌──────────────
          │  │  │  │      │  │      │        │      │  │
0V ───────┼──┼──┼──┼──────┼──┼──────┼────────┼──────┼──┼──────────────
          │  │  │  │      │  │      │        │      │  │
-V        └──┘  └──┘      └──┘      └────────┘      └──┘
              [RZ: Return to Zero]
              비트 중간 0V 복귀, 대역폭 2배 필요, 동기화 용이

+V ───────┐  ┌──┐  ┌──────┐  ┌──────┐        ┌──────┐  ┌──────────────
          │  │  │  │      │  │      │        │      │  │
0V ───────┼──┼──┼──┼──────┼──┼──────┼────────┼──────┼──┼──────────────
          │  │  │  │      │  │      │        │      │  │
-V        └──┘  └──┘      └──┘      └────────┘      └──┘
              [Manchester (IEEE 802.3)]
              비트 중간 반전: 1=Low→High, 0=High→Low
              항상 천이 발생, 동기화 완벽, DC 성분 없음

+V ───────┐  ┌─────┐  ┌──────┐  ┌──────┐     ┌──────┐  ┌──────────────
          │  │     │  │      │  │      │     │      │  │
0V ───────┼──┼─────┼──┼──────┼──┼──────┼─────┼──────┼──┼──────────────
          │  │     │  │      │  │      │     │      │  │
-V        └──┘     └──┘      └──┘      └─────┘      └──┘
              [Differential Manchester (IEEE 802.5)]
              비트 시작 천이 여부: 0=천이 있음, 1=천이 없음
              토큰 링, DC 성분 없음, 동기화 완벽
================================================================================
```

### 심층 동작 원리: 핵심 알고리즘 상세 분석

#### 1. NRZ (Non-Return to Zero) 계열

**NRZ-L (Level)**:
- 가장 단순한 부호화 방식으로, 비트 값에 따라 전압 레벨을 직접 매핑
- `0` → `+V`, `1` → `-V` (또는 반대)
- **장점**: 구현 단순, 대역폭 효율 높음 (B bps 전송에 B Hz 필요)
- **단점**: 연속된 동일 비트에서 천이가 없어 클럭 복원 불가, DC 성분 발생

**NRZ-I (Inverted)**:
- 현재 비트가 `1`이면 이전 레벨 반전, `0`이면 유지
- **장점**: 연속된 1에 대해선 천이 보장
- **단점**: 연속된 0에서 여전히 동기화 문제
- **적용**: USB (Universal Serial Bus)

#### 2. AMI (Alternate Mark Inversion)

```
동작 원리:
- 비트 0: 0V (무신호)
- 비트 1: 이전 1의 극성과 반대로 +V 또는 -V 교대 출력

예시: 1 0 1 1 0 0 0 1
      +V 0V -V +V 0V 0V 0V -V
      ↑           ↑         ↑
      첫 번째 1   두 번째 1  마지막 1 (직전 1이 +V였으므로 -V)
```

- **장점**: DC 성분 완전 제거 (양/음 펄스가 균등), 오류 검출 가능 (연속 동극성 펄스 = 위반)
- **단점**: 연속된 0에서 동기화 상실
- **해결책**: B8ZS, HDB3 (연속 0을 특수 패턴으로 대체)

#### 3. Manchester 부호화 (IEEE 802.3 표준)

```
동작 원리:
- 비트 0: High → Low (비트 중간에서 하강 천이)
- 비트 1: Low → High (비트 중간에서 상승 천이)

핵심 특성:
- 모든 비트에서 반드시 1회 천이 발생 (동기화 보장)
- DC 성분 없음 (High와 Low 시간 동일)
- 대역폭 요구량 2배 (B bps 전송에 2B Hz 필요)
```

- **적용**: 10BASE-T 이더넷
- **수식 표현**: `Signal(t) = (bit XOR Clock(t)) * 2 - 1`

#### 4. 4B/5B 블록 부호화

```
인코딩 테이블 (4비트 입력 → 5비트 출력):

입력  | 출력  |  입력  | 출력  |  특성
------|-------|--------|-------|------------------
0000  | 11110 |  1000  | 10010 |  최대 1개 연속 0
0001  | 01001 |  1001  | 10011 |  DC 밸런스 유지
0010  | 10100 |  1010  | 10110 |  3개 이상 연속 0 없음
0011  | 10101 |  1011  | 10111 |  동기화 보장
0100  | 01010 |  1100  | 11010 |
0101  | 01011 |  1101  | 11011 |
0110  | 01110 |  1110  | 11100 |
0111  | 01111 |  1111  | 11101 |

제어 심볼:
IDLE  | 11111 |  JK    | 11000 |  시작 구분자
HALT  | 00111 |  ...   |       |
```

- **원리**: 4비트 데이터를 5비트 심볼로 매핑하여, 3개 이상 연속된 0이 발생하지 않도록 보장
- **장점**: AMI + 4B/5B 조합으로 DC 제거 + 동기화 동시 달성
- **효율**: 80% (5비트 중 4비트가 실제 데이터)
- **적용**: 100BASE-TX Fast Ethernet (4B/5B → MLT-3 변조)

### 핵심 코드: 라인 부호화 시뮬레이터 (Python)

```python
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from typing import List, Tuple

class LineCodeType(Enum):
    """라인 부호화 방식 열거형"""
    NRZ_L = "NRZ-L"
    NRZ_I = "NRZ-I"
    AMI = "AMI"
    MANCHESTER = "Manchester"
    DIFF_MANCHESTER = "Differential Manchester"
    RZ = "RZ"
    MILLER = "Miller"

class LineCoder:
    """
    다양한 라인 부호화 기법을 시뮬레이션하는 클래스
    입력 비트 스트림을 해당 부호화 방식의 파형으로 변환
    """

    def __init__(self, bit_rate: int = 1_000_000, samples_per_bit: int = 100):
        """
        Args:
            bit_rate: 비트 전송 속도 (bps)
            samples_per_bit: 비트당 샘플링 수 (파형 해상도)
        """
        self.bit_rate = bit_rate
        self.samples_per_bit = samples_per_bit
        self.voltage_high = 1.0   # +V 레벨
        self.voltage_low = -1.0   # -V 레벨
        self.voltage_zero = 0.0   # 0V 레벨

    def encode_nrz_l(self, bits: List[int]) -> np.ndarray:
        """
        NRZ-L (Non-Return to Zero Level) 부호화
        0 → +V, 1 → -V (극성은 설정에 따라 반대 가능)
        """
        signal = np.zeros(len(bits) * self.samples_per_bit)
        for i, bit in enumerate(bits):
            level = self.voltage_low if bit == 1 else self.voltage_high
            signal[i * self.samples_per_bit:(i + 1) * self.samples_per_bit] = level
        return signal

    def encode_nrz_i(self, bits: List[int]) -> np.ndarray:
        """
        NRZ-I (Non-Return to Zero Inverted) 부호화
        1에서 레벨 반전, 0은 유지
        """
        signal = np.zeros(len(bits) * self.samples_per_bit)
        current_level = self.voltage_high  # 초기 레벨

        for i, bit in enumerate(bits):
            if bit == 1:
                current_level = -current_level  # 반전
            signal[i * self.samples_per_bit:(i + 1) * self.samples_per_bit] = current_level
        return signal

    def encode_ami(self, bits: List[int]) -> np.ndarray:
        """
        AMI (Alternate Mark Inversion) 부호화
        0 → 0V, 1 → +V/-V 교대
        """
        signal = np.zeros(len(bits) * self.samples_per_bit)
        last_mark_level = self.voltage_low  # 마지막 1의 극성 추적

        for i, bit in enumerate(bits):
            if bit == 1:
                # 직전 1과 반대 극성
                last_mark_level = -last_mark_level
                level = last_mark_level
            else:
                level = self.voltage_zero
            signal[i * self.samples_per_bit:(i + 1) * self.samples_per_bit] = level
        return signal

    def encode_manchester(self, bits: List[int]) -> np.ndarray:
        """
        Manchester 부호화 (IEEE 802.3 표준)
        0 → High→Low (비트 중간 하강 천이)
        1 → Low→High (비트 중간 상승 천이)
        """
        signal = np.zeros(len(bits) * self.samples_per_bit)
        half = self.samples_per_bit // 2

        for i, bit in enumerate(bits):
            start_idx = i * self.samples_per_bit
            if bit == 0:
                # High → Low
                signal[start_idx:start_idx + half] = self.voltage_high
                signal[start_idx + half:start_idx + self.samples_per_bit] = self.voltage_low
            else:
                # Low → High
                signal[start_idx:start_idx + half] = self.voltage_low
                signal[start_idx + half:start_idx + self.samples_per_bit] = self.voltage_high
        return signal

    def encode_differential_manchester(self, bits: List[int]) -> np.ndarray:
        """
        차분 Manchester 부호화 (IEEE 802.5 토큰 링)
        비트 시작 천이: 0=천이 있음, 1=천이 없음
        비트 중간: 항상 천이 있음 (동기화)
        """
        signal = np.zeros(len(bits) * self.samples_per_bit)
        half = self.samples_per_bit // 2
        current_level = self.voltage_high

        for i, bit in enumerate(bits):
            start_idx = i * self.samples_per_bit

            # 비트 시작 천이 (0이면 천이, 1이면 유지)
            if bit == 0:
                current_level = -current_level

            # 전반부
            signal[start_idx:start_idx + half] = current_level

            # 비트 중간 천이 (항상)
            current_level = -current_level

            # 후반부
            signal[start_idx + half:start_idx + self.samples_per_bit] = current_level
        return signal

    def encode_4b5b(self, bits: List[int]) -> Tuple[List[int], List[int]]:
        """
        4B/5B 블록 부호화
        4비트 데이터를 5비트 심볼로 변환
        반환: (인코딩된 비트 리스트, 원본 4비트 블록 리스트)
        """
        # 4B/5B 인코딩 테이블
        encode_table = {
            (0,0,0,0): [1,1,1,1,0],  # 0x0
            (0,0,0,1): [0,1,0,0,1],  # 0x1
            (0,0,1,0): [1,0,1,0,0],  # 0x2
            (0,0,1,1): [1,0,1,0,1],  # 0x3
            (0,1,0,0): [0,1,0,1,0],  # 0x4
            (0,1,0,1): [0,1,0,1,1],  # 0x5
            (0,1,1,0): [0,1,1,1,0],  # 0x6
            (0,1,1,1): [0,1,1,1,1],  # 0x7
            (1,0,0,0): [1,0,0,1,0],  # 0x8
            (1,0,0,1): [1,0,0,1,1],  # 0x9
            (1,0,1,0): [1,0,1,1,0],  # 0xA
            (1,0,1,1): [1,0,1,1,1],  # 0xB
            (1,1,0,0): [1,1,0,1,0],  # 0xC
            (1,1,0,1): [1,1,0,1,1],  # 0xD
            (1,1,1,0): [1,1,1,0,0],  # 0xE
            (1,1,1,1): [1,1,1,0,1],  # 0xF
        }

        encoded_bits = []
        original_blocks = []

        # 4비트 단위로 처리
        for i in range(0, len(bits) - 3, 4):
            block = tuple(bits[i:i+4])
            if block in encode_table:
                encoded_bits.extend(encode_table[block])
                original_blocks.append(list(block))

        return encoded_bits, original_blocks

    def calculate_dc_component(self, signal: np.ndarray) -> float:
        """신호의 DC 성분 계산 (평균 전압)"""
        return np.mean(signal)

    def count_transitions(self, signal: np.ndarray) -> int:
        """신호의 천이 횟수 계산 (동기화 능력 지표)"""
        transitions = 0
        for i in range(1, len(signal)):
            if signal[i] != signal[i-1]:
                transitions += 1
        return transitions

    def analyze_encoding(self, bits: List[int], code_type: LineCodeType) -> dict:
        """부호화 방식 분석 (DC 성분, 천이 횟수, 대역폭 등)"""
        encoders = {
            LineCodeType.NRZ_L: self.encode_nrz_l,
            LineCodeType.NRZ_I: self.encode_nrz_i,
            LineCodeType.AMI: self.encode_ami,
            LineCodeType.MANCHESTER: self.encode_manchester,
            LineCodeType.DIFF_MANCHESTER: self.encode_differential_manchester,
        }

        if code_type not in encoders:
            raise ValueError(f"Unsupported encoding: {code_type}")

        signal = encoders[code_type](bits)

        return {
            "code_type": code_type.value,
            "dc_component": self.calculate_dc_component(signal),
            "transitions": self.count_transitions(signal),
            "transitions_per_bit": self.count_transitions(signal) / len(bits),
            "signal_length": len(signal),
            "bandwidth_factor": self.count_transitions(signal) / (2 * len(bits)),  # 대역폭 계수
        }


# 실무 사용 예시
if __name__ == "__main__":
    # 테스트 비트 시퀀스
    test_bits = [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1]

    coder = LineCoder(bit_rate=1_000_000, samples_per_bit=100)

    # 각 부호화 방식 분석
    print("=" * 60)
    print("Line Coding Analysis Report")
    print("=" * 60)
    print(f"Input Bits: {test_bits}")
    print(f"Bit Rate: {coder.bit_rate / 1e6} Mbps")
    print("-" * 60)

    for code_type in [LineCodeType.NRZ_L, LineCodeType.NRZ_I, LineCodeType.AMI,
                       LineCodeType.MANCHESTER, LineCodeType.DIFF_MANCHESTER]:
        analysis = coder.analyze_encoding(test_bits, code_type)
        print(f"\n[{analysis['code_type']}]")
        print(f"  DC Component: {analysis['dc_component']:.4f} V")
        print(f"  Total Transitions: {analysis['transitions']}")
        print(f"  Transitions/Bit: {analysis['transitions_per_bit']:.2f}")
        print(f"  Bandwidth Factor: {analysis['bandwidth_factor']:.2f}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 라인 부호화 방식 성능 매트릭스

| 비교 지표 | NRZ-L | NRZ-I | AMI | Manchester | Diff Manchester | 4B/5B+NRZ-I |
|----------|-------|-------|-----|------------|-----------------|-------------|
| **DC 성분** | 존재 (높음) | 존재 (보통) | 없음 | 없음 | 없음 | 없음 |
| **동기화 능력** | 낮음 (연속 0/1 불가) | 낮음 (연속 0 불가) | 낮음 (연속 0 불가) | 매우 높음 (항상 천이) | 매우 높음 | 높음 (최대 3연속 0) |
| **대역폭 효율** | 100% | 100% | 100% | 50% | 50% | 80% |
| **오류 검출** | 불가능 | 불가능 | 가능 (극성 위반) | 불가능 | 가능 (천이 규칙 위반) | 가능 (무효 심볼) |
| **구현 복잡도** | 매우 낮음 | 낮음 | 보통 | 낮음 | 보통 | 높음 |
| **전력 소모** | 높음 (DC 성분) | 보통 | 낮음 | 보통 | 보통 | 낮음 |
| **BER 성능** | 보통 | 보통 | 양호 | 보통 | 양호 | 우수 |
| **주요 적용** | 내부 버스 | USB | T1/E1 전화망 | 10BASE-T | Token Ring | 100BASE-TX |

### 과목 융합 관점 분석

1. **통신 이론(Shannon-Nyquist)과의 융합**:
   - 나이퀴스트 대역폭 한계에 따라 B bps 전송에는 최소 B/2 Hz 대역폭이 필요합니다.
   - Manchester 부호화는 B bps 전송에 2B Hz가 필요하여 스펙트럼 효율이 50%로 감소합니다.
   - 4B/5B는 80% 효율로, AMI와 결합하여 DC 제거와 대역폭 효율을 절충합니다.

2. **하드웨어 설계와의 융합**:
   - NRZ 방식은 간단한 디지털 회로(플립플롭, 버퍼)로 구현 가능하지만, 클럭 복원을 위한 PLL(Phase-Locked Loop)이 별도로 필요합니다.
   - Manchester는 XOR 게이트 하나로 인코딩 가능하지만, 대역폭이 2배 필요하여 고속 통신에 부적합합니다.

3. **보안과의 융합**:
   - AMI의 극성 위반(Bipolar Violation)은 전송 오류뿐만 아니라 의도적인 신호 변조(스푸핑) 탐지에도 활용됩니다.
   - 스크램블링(Scrambling) 기법은 데이터의 패턴을 숨겨 암호화와 유사한 보안 효과를 제공합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 산업용 제어 네트워크 설계

**문제 상황**: 자동차 제조 공장의 PLC(Programmable Logic Controller) 네트워크를 설계해야 합니다. 환경 특성은 다음과 같습니다:
- 전자파 간섭(EMI)이 심한 용접 로봇 근처
- 최대 전송 거리 500m
- 실시간 제어를 위한 지연 시간 1ms 이하
- 데이터 전송 속도 10 Mbps

**기술사의 전략적 의사결정**:

1. **부호화 방식 선정**:
   - **NRZ-L 배제**: DC 성분으로 인해 장거리 전송 시 신호 왜곡 심각
   - **Manchester 고려**: 강력한 동기화 능력으로 EMI 환경에서도 클럭 복원 용이, 하지만 10 Mbps 전송에 20 MHz 대역폭 필요
   - **AMI + 4B/5B 채택**: DC 성분 제거, 대역폭 효율 80%, 오류 검출 가능

2. **케이블 선정**:
   - 일반 UTP 대신 STP(Shielded Twisted Pair) Cat 6a 사용하여 EMI 차폐

3. **중계기 배치**:
   - 500m 전송을 위해 200m마다 중계기(Repeater) 설치하여 신호 재생

### 안티패턴 (Anti-patterns)

- **안티패턴 1: 고속 통신에 Manchester 사용**
  - 1 Gbps 이상의 고속 통신에서 Manchester 부호화는 2 GHz 이상의 대역폭을 요구하여 비현실적입니다. 대신 8B/10B 또는 64B/66B와 PAM-4/16을 조합한 방식을 사용해야 합니다.

- **안티패턴 2: 동기화 미고려 설계**
  - 연속 0이나 1이 많은 데이터(예: 이미지 파일)를 AMI로 전송할 때 동기화 상실로 인해 비트 슬립이 발생할 수 있습니다. 반드시 스크램블링이나 B8ZS/HDB3를 함께 적용해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 영역 | 측정 지표 | 개선 효과 |
|----------|----------|----------|
| **전송 거리 연장** | 최대 도달 거리 | DC 제거로 2~3배 연장 |
| **동기화 신뢰성** | 클럭 복원 시간 | Manchester/4B/5B로 50% 단축 |
| **오류율 저감** | BER (Bit Error Rate) | AMI 극성 검사로 10^-6 → 10^-8 개선 |
| **스펙트럼 효율** | bps/Hz | 4B/5B로 80% 효율 달성 |

### 미래 전망 및 진화 방향

- **PAM (Pulse Amplitude Modulation) 융합**: 현대의 400GbE 이더넷은 PAM-4(4레벨 펄스)를 사용하여 1 심볼당 2비트를 전송함으로써 대역폭 효율을 2배로 높이고 있습니다.
- **광통신용 라인 부호화**: 광섬유는 양극성 신호를 전송할 수 없어, NRZ-I나 맨체스터 대신 특수한 광 강도 변조 방식이 사용됩니다.

### ※ 참고 표준/가이드
- **IEEE 802.3**: Ethernet MAC and PHY specifications (10BASE-T, 100BASE-TX, 1000BASE-T)
- **ITU-T G.703**: Physical/electrical characteristics of hierarchical digital interfaces
- **ANSI X3.263**: FDDI Physical Layer Medium Dependent (PMD)

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [변조 기법(ASK/FSK/PSK)](@/studynotes/03_network/01_fundamentals/_index.md): 디지털-아날로그 변조와의 비교
- [동기화 기법](@/studynotes/03_network/01_fundamentals/_index.md): 비트/문자/프레임 동기화 메커니즘
- [대역폭 및 채널 용량](@/studynotes/03_network/01_fundamentals/_index.md): Nyquist/Shannon 한계 이론
- [오류 제어(ARQ/FEC)](@/studynotes/03_network/01_fundamentals/_index.md): 전진 오류 수정과의 연계
- [이더넷 물리 계층](@/studynotes/03_network/01_fundamentals/_index.md): 10/100/1000BASE-T PHY 표준

---

### 👶 어린이를 위한 3줄 비유 설명
1. **라인 부호화**는 컴퓨터가 말하는 0과 1을 전선으로 보낼 수 있는 **전기 신호로 바꾸는 번역기**예요.
2. 어떤 방식은 **천천히 말하기**(NRZ), 어떤 방식은 **빠르게 높낮이로 말하기**(Manchester)라서, 상황에 맞춰 선택해야 해요.
3. 좋은 번역기는 **듣는 사람이 헷갈리지 않게**(동기화) 하고, **멀리까지 잘 들리게**(DC 제거) 해줘요!
