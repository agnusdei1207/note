+++
title = "동기식/비동기식 전송 (Synchronous vs Asynchronous Transmission)"
date = 2024-05-18
description = "데이터 통신에서 송수신 간 타이밍 동기화 방식 - 비동기식(Start/Stop Bit)과 동기식(SYN, HDLC, SDLC)의 원리, 장단점, 그리고 실무 적용"
weight = 50
[taxonomies]
categories = ["studynotes-network"]
tags = ["Synchronous", "Asynchronous", "Start-Stop", "HDLC", "Clock Recovery", "UART"]
+++

# 동기식/비동기식 전송 (Synchronous vs Asynchronous Transmission)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비동기식 전송은 각 문자 앞뒤에 Start/Stop 비트를 추가하여 독립적으로 전송하고, 동기식 전송은 클럭 동기화를 통해 연속적인 비트 스트림을 전송합니다.
> 2. **가치**: 비동기식은 구현이 간단하여 키보드, 시리얼 포트(UART)에 적합하고, 동기식은 오버헤드가 적어 고속 통신(이더넷, HDLC, SONET)에 필수적입니다.
> 3. **융합**: 현대 고속 통신은 모두 동기식을 사용하며, 클럭 복구(Clock Recovery)를 위한 PLL, 8B/10B, 64B/66B 등의 라인 코딩 기술과 결합됩니다.

---

## Ⅰ. 개요 (Context & Background)

데이터 통신에서 송신측과 수신측의 클럭 타이밍을 맞추는 것은 데이터를 정확히 해석하는 데 필수적입니다. 동기화 방식에 따라 비동기식(Asynchronous)과 동기식(Synchronous)으로 구분됩니다.

**💡 비유**: 동기화 방식은 **'대화 방식'**과 같습니다.
- **비동기식**: "안녕" (잠시 멈춤) "만나서" (잠시 멈춤) "반가워" - 단어마다 경계를 표시
- **동기식**: "안녕만나서반가워" - 문장 전체를 끊김 없이 말하며, 듣는 사람은 말의 속도에 맞춰 이해

**등장 배경 및 발전 과정**:
1. **기존 기술의 치명적 한계점**: 초기 원거리 통신은 전신(Telegraph)으로 Morse 부호를 사용했는데, 송수신 간 타이밍 동기화가 어려워 숙련된 오퍼레이터가 필요했습니다.
2. **혁신적 패러다임 변화**: 1960년대 RS-232C 표준으로 비동기식 시리얼 통신이 표준화되었고, 1970년대 HDLC, SDLC로 동기식 프로토콜이 개발되어 고속 대용량 전송이 가능해졌습니다.
3. **비즈니스적 요구사항**: 현대 데이터센터, 인터넷 백본은 Gbps~Tbps급 전송이 필요하며, 이는 동기식 전송 + 고급 클럭 복구 기술로만 가능합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 비교 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                     비동기식 전송 (Asynchronous Transmission)                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  데이터 프레임 구조 (UART 예시):                                             │
│                                                                             │
│      ┌────┬───┬───┬───┬───┬───┬───┬───┬───┬───┬────┐                       │
│      │Idle│S  │D0 │D1 │D2 │D3 │D4 │D5 │P  │St │Idle│                       │
│      │ 1  │0  │ x │ x │ x │ x │ x │ x │ x │ 1 │ 1  │                       │
│      └────┴───┴───┴───┴───┴───┴───┴───┴───┴───┴────┘                       │
│        ↑    ↑                        ↑   ↑    ↑                            │
│      idle  Start                   Parity Stop idle                         │
│            Bit                      Bit   Bit                               │
│                                                                             │
│  특징:                                                                       │
│  • 각 문자(바이트)가 독립적으로 전송                                         │
│  • Start 비트(0)로 동기화 시작                                               │
│  • Stop 비트(1)로 문자 끝 표시                                               │
│  • 문자 간 임의의 간격 허용                                                  │
│  • 오버헤드: 8비트 데이터 + 2~3비트 = 20~27%                                 │
│                                                                             │
│  클럭 허용 오차:                                                             │
│  • 양측 클럭이 약 5% 이내로 일치하면 OK                                       │
│  • Start 비트에서 재동기화                                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     동기식 전송 (Synchronous Transmission)                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  문자 동기식 (BSC - Binary Synchronous Communication):                       │
│                                                                             │
│  ┌────┬────┬────┬─────────────┬────┬────┬────┬─────────────┬────┐          │
│  │SYN │SYN │SOH │   Header    │STX │  Data   │ETX │  BCC   │    │          │
│  │16  │16  │01  │             │02  │         │03  │        │    │          │
│  └────┴────┴────┴─────────────┴────┴─────────┴────┴─────────┴────┘          │
│    ↑                                                                        │
│  동기 문자 (수신측 클럭 동기화용)                                            │
│                                                                             │
│  비트 동기식 (HDLC - High-Level Data Link Control):                         │
│                                                                             │
│  ┌────────┬────────┬────────┬─────────────┬─────┬────────┐                 │
│  │  Flag  │Address │Control │  Information│ FCS │  Flag  │                 │
│  │01111110│ 8bit   │ 8/16bit│   Variable  │16/32│01111110│                 │
│  └────────┴────────┴────────┴─────────────┴─────┴────────┘                 │
│                                                                             │
│  특징:                                                                       │
│  • 연속적인 비트 스트림 전송                                                 │
│  • 전용 클럭 선 또는 신호 인코딩(Manchester 등)으로 동기화                   │
│  • 프레임 단위으로 구조화                                                    │
│  • 오버헤드: 프레임당 고정 (약 2~4%)                                         │
│  • Bit Stuffing (HDLC): 1이 5개 연속되면 0 삽입                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 상세 비교표

| 특성 | 비동기식 (Asynchronous) | 동기식 (Synchronous) |
|---|---|---|
| **동기화 단위** | 문자 (byte) | 프레임/블록 |
| **동기화 방법** | Start/Stop 비트 | SYN 문자, Flag, 클럭 신호 |
| **클럭 필요** | 각 문자 내에서만 | 지속적 |
| **오버헤드** | 높음 (20~27%) | 낮음 (2~4%) |
| **전송 효율** | 낮음 | 높음 |
| **구현 복잡도** | 간단 | 복잡 |
| **오류 검출** | 패리티 (제한적) | CRC (강력) |
| **속도 범위** | 저~중속 (< 115.2 kbps 일반적) | 고속 (Gbps까지) |
| **주요 적용** | UART, 키보드, 모뎀 | 이더넷, HDLC, SONET, SDH |

### 심층 동작 원리

**1. 비동기식 UART (Universal Asynchronous Receiver Transmitter)**

```
UART 프레임 구조:

   idle   Start  D0  D1  D2  D3  D4  D5  D6  D7  P   Stop  idle
   ───┐    ┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┌───┐
      └────┘ └─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘   └────

비트 타이밍:
T_bit = 1 / Baud Rate

예: 9600 baud
T_bit = 1/9600 = 104.17 μs

샘플링:
- 수신측은 보통 16× 오버샘플링
- Start 비트 하강 에지 감지 후 중앙에서 샘플링
- 16 클럭 중 8, 9, 10번째에서 다수결로 판정

Baud Rate 흔한 값:
• 9600, 19200, 38400, 57600, 115200 bps
• RS-232C 표준

오차 허용 범위 계산:
- 10비트 프레임 (1 Start + 8 Data + 1 Stop)
- 마지막 비트에서 샘플링 오차 < 0.5 비트
- 허용 클럭 오차: ±5%
```

**2. 동기식 HDLC (High-Level Data Link Control)**

```
HDLC 프레임 구조:

┌──────────────┬─────────────┬──────────────┬─────────────┬───────┬──────────────┐
│    Flag      │   Address   │   Control    │ Information │  FCS  │    Flag      │
│  01111110    │   8 bits    │   8/16 bits  │  Variable   │16/32b │  01111110    │
└──────────────┴─────────────┴──────────────┴─────────────┴───────┴──────────────┘

Flag: 01111110 (0x7E) - 프레임 시작/끝, 동기화
Address: 종국(Station) 주소
Control: 프레임 유형, 시퀀스 번호
Information: 상위 계층 데이터 (I-프레임만)
FCS: Frame Check Sequence (CRC-16 또는 CRC-32)

Bit Stuffing (비트 스터핑):
- 데이터 내에 1이 5개 연속되면 강제로 0 삽입
- 수신측에서 1이 5개 연속 후 0이 나오면 0 제거
- Flag(01111110)와 데이터 구분 보장

예시:
원본: 01111110111111101
스터핑: 0111110101111101101
              ↑     ↑
          삽입된 0

Control 필드 형식:
┌────────────────────────────────────┐
│ I-Frame (정보 프레임)              │
│ [N(R):3][P/F:1][N(S):3][0:1]       │
│ - 사용자 데이터 전송                │
│ - 순서 번호로 신뢰성 보장           │
├────────────────────────────────────┤
│ S-Frame (감독 프레임)              │
│ [N(R):3][P/F:1][S:2][0:1][0:1]     │
│ - RR(수신 준비), REJ(거부)         │
│ - RNR(수신 미준비), SREJ(선택거부) │
├────────────────────────────────────┤
│ U-Frame (비번호 프레임)            │
│ [M:5][P/F:1][M:2][1:1]             │
│ - SABM, DISC, UA, DM, FRMR 등     │
│ - 링크 설정/해제, 응답             │
└────────────────────────────────────┘
```

**3. 동기식 전송의 클럭 복구 (Clock Recovery)**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        클럭 복구 방식                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. 별도 클럭 선 (외부 클럭)                                                 │
│     ┌───────┐      Clock Line      ┌───────┐                               │
│     │  TX   │────────────────────→ │  RX   │                               │
│     │       │      Data Line       │       │                               │
│     │       │────────────────────→ │       │                               │
│     └───────┘                      └───────┘                               │
│     예: I2C, SPI, Centronics                                              │
│                                                                             │
│  2. 신호 인코딩 (자체 동기화)                                               │
│     • Manchester: 모든 비트에서 전이 발생                                   │
│     • 8B/10B: DC 균형 + 충분한 전이                                         │
│     • 64B/66B: 이더넷 10G+                                                  │
│                                                                             │
│  3. PLL (Phase-Locked Loop)                                                │
│     수신 신호 → 위상 검출 → LPF → VCO → 복구된 클럭                         │
│                                                                             │
│        ┌────────────────────────────────────────────────────┐               │
│        │                      PLL                           │               │
│        │  ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐           │               │
│   In ──┼→│ PFD │→→│ LPF │→→│ VCO │→→│ /N │──┼──→ Out      │               │
│        │  └──┬──┘   └─────┘   └─────┘   └─────┘  │         │               │
│        │     └────────────────────────────────────┘         │               │
│        └────────────────────────────────────────────────────┘               │
│                                                                             │
│     PFD: Phase-Frequency Detector (위상-주파수 검출기)                      │
│     LPF: Low-Pass Filter (저역 통과 필터)                                   │
│     VCO: Voltage-Controlled Oscillator (전압 제어 발진기)                   │
│     /N: 분주기 (주파수 분할)                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: UART 및 HDLC 시뮬레이션 (Python)

```python
import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class FrameType(Enum):
    I_FRAME = 0  # Information
    S_FRAME = 1  # Supervisory
    U_FRAME = 2  # Unnumbered

@dataclass
class UARTConfig:
    baud_rate: int = 9600
    data_bits: int = 8
    parity: str = 'none'  # 'none', 'even', 'odd'
    stop_bits: int = 1

class UARTSimulator:
    """UART 비동기식 전송 시뮬레이터"""

    def __init__(self, config: UARTConfig = None):
        self.config = config or UARTConfig()
        self.bit_time = 1 / self.config.baud_rate

    def transmit_byte(self, data: int) -> List[int]:
        """
        바이트 전송 시뮬레이션

        Returns:
            비트 리스트 (Start + Data + Parity + Stop)
        """
        bits = []

        # Start bit (항상 0)
        bits.append(0)

        # Data bits (LSB first)
        for i in range(self.config.data_bits):
            bits.append((data >> i) & 1)

        # Parity bit
        if self.config.parity == 'even':
            bits.append(sum(bits[1:]) % 2)
        elif self.config.parity == 'odd':
            bits.append((sum(bits[1:]) + 1) % 2)

        # Stop bit(s) (항상 1)
        for _ in range(self.config.stop_bits):
            bits.append(1)

        return bits

    def receive_byte(self, bits: List[int]) -> Tuple[Optional[int], bool]:
        """
        바이트 수신 시뮬레이션

        Returns:
            (수신된 바이트, 오류 여부)
        """
        if len(bits) < self.config.data_bits + 2:
            return None, True

        # Start bit 확인
        if bits[0] != 0:
            return None, True  # Framing error

        # Data bits 추출
        data = 0
        for i in range(self.config.data_bits):
            data |= bits[1 + i] << i

        # Parity 확인
        if self.config.parity != 'none':
            parity_idx = 1 + self.config.data_bits
            expected_parity = sum(bits[1:parity_idx]) % 2
            if self.config.parity == 'odd':
                expected_parity = (expected_parity + 1) % 2
            if bits[parity_idx] != expected_parity:
                return data, True  # Parity error

        # Stop bit 확인
        stop_idx = 1 + self.config.data_bits
        if self.config.parity != 'none':
            stop_idx += 1
        if bits[stop_idx] != 1:
            return data, True  # Framing error

        return data, False

    def calculate_overhead(self) -> float:
        """전송 오버헤드 계산"""
        total_bits = 1 + self.config.data_bits + self.config.stop_bits
        if self.config.parity != 'none':
            total_bits += 1
        return (total_bits - self.config.data_bits) / total_bits * 100

    def calculate_effective_rate(self) -> float:
        """유효 데이터 전송률 계산"""
        total_bits = 1 + self.config.data_bits + self.config.stop_bits
        if self.config.parity != 'none':
            total_bits += 1
        return self.config.baud_rate * self.config.data_bits / total_bits


class HDLCSimulator:
    """HDLC 동기식 전송 시뮬레이터"""

    FLAG = 0x7E  # 01111110

    def __init__(self):
        self.tx_seq = 0  # 송신 시퀀스 번호 N(S)
        self.rx_seq = 0  # 수신 시퀀스 번호 N(R)

    def bit_stuff(self, data: bytes) -> bytes:
        """Bit Stuffing 수행"""
        bits = []
        for byte in data:
            for i in range(7, -1, -1):
                bits.append((byte >> i) & 1)

        # Bit stuffing: 1이 5개 연속되면 0 삽입
        stuffed = []
        consecutive_ones = 0

        for bit in bits:
            stuffed.append(bit)
            if bit == 1:
                consecutive_ones += 1
                if consecutive_ones == 5:
                    stuffed.append(0)  # 0 삽입
                    consecutive_ones = 0
            else:
                consecutive_ones = 0

        # 비트를 바이트로 변환
        result = []
        for i in range(0, len(stuffed), 8):
            byte = 0
            for j in range(8):
                if i + j < len(stuffed):
                    byte = (byte << 1) | stuffed[i + j]
                else:
                    byte = byte << 1
            result.append(byte)

        return bytes(result)

    def bit_unstuff(self, data: bytes) -> bytes:
        """Bit Unstuffing 수행"""
        bits = []
        for byte in data:
            for i in range(7, -1, -1):
                bits.append((byte >> i) & 1)

        # Bit unstuffing: 1이 5개 연속 후 0이 나오면 0 제거
        unstuffed = []
        consecutive_ones = 0

        for bit in bits:
            if consecutive_ones == 5 and bit == 0:
                consecutive_ones = 0
                continue  # 0 제거

            unstuffed.append(bit)
            if bit == 1:
                consecutive_ones += 1
            else:
                consecutive_ones = 0

        # 비트를 바이트로 변환
        result = []
        for i in range(0, len(unstuffed), 8):
            if i + 8 > len(unstuffed):
                break
            byte = 0
            for j in range(8):
                byte = (byte << 1) | unstuffed[i + j]
            result.append(byte)

        return bytes(result)

    def create_i_frame(self, address: int, data: bytes) -> bytes:
        """I-Frame (정보 프레임) 생성"""
        # Control 필드: N(R) P/F N(S) 0
        control = ((self.rx_seq & 0x07) << 5) | (0 << 4) | ((self.tx_seq & 0x07) << 1) | 0

        frame = bytes([self.FLAG, address, control]) + data
        fcs = self._calculate_fcs(frame[1:])  # Flag 제외
        frame += fcs + bytes([self.FLAG])

        self.tx_seq = (self.tx_seq + 1) % 8
        return frame

    def create_rr_frame(self, address: int) -> bytes:
        """RR (Receiver Ready) S-Frame 생성"""
        # Control: N(R) P/F 00 01
        control = ((self.rx_seq & 0x07) << 5) | (0 << 4) | 0x01

        frame = bytes([self.FLAG, address, control])
        fcs = self._calculate_fcs(frame[1:])
        frame += fcs + bytes([self.FLAG])

        return frame

    def _calculate_fcs(self, data: bytes) -> bytes:
        """간소화된 FCS 계산 (실제는 CRC-16-CCITT)"""
        crc = 0xFFFF
        for byte in data:
            crc ^= byte << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1
                crc &= 0xFFFF
        return bytes([crc >> 8, crc & 0xFF])


def compare_transmission_modes():
    """전송 모드 비교"""
    print("=" * 60)
    print("동기식 vs 비동기식 전송 비교")
    print("=" * 60)

    # UART 비동기식
    print("\n[비동기식 UART]")
    uart = UARTSimulator(UARTConfig(baud_rate=115200, data_bits=8, parity='none', stop_bits=1))
    print(f"  Baud Rate: {uart.config.baud_rate} bps")
    print(f"  오버헤드: {uart.calculate_overhead():.1f}%")
    print(f"  유효 속도: {uart.calculate_effective_rate()/1000:.1f} kbps")

    # 전송 예시
    data = ord('A')
    bits = uart.transmit_byte(data)
    print(f"  'A'(0x41) 전송: {bits}")

    # HDLC 동기식
    print("\n[동기식 HDLC]")
    hdlc = HDLCSimulator()
    frame = hdlc.create_i_frame(0x01, b"Hello")
    print(f"  Frame 길이: {len(frame)} bytes")
    print(f"  Frame (hex): {frame.hex()}")

    # Bit stuffing 예시
    test_data = bytes([0xFF, 0xFF])  # 모두 1
    stuffed = hdlc.bit_stuff(test_data)
    print(f"\n  Bit Stuffing 테스트:")
    print(f"    원본: {test_data.hex()} ({len(test_data)*8} bits)")
    print(f"    스터핑 후: {stuffed.hex()} ({len(stuffed)*8} bits)")

    # 효율 비교
    print("\n[전송 효율 비교]")
    print(f"  비동기식 (UART 8N1): {100 - uart.calculate_overhead():.1f}% 데이터 효율")
    print(f"  동기식 (HDLC): ~96-98% 데이터 효율 (대용량 시)")


if __name__ == "__main__":
    compare_transmission_modes()
