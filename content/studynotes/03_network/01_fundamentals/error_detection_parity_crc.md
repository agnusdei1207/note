+++
title = "오류 검출 코드 (Error Detection: Parity, Checksum, CRC)"
date = 2024-05-18
description = "데이터 전송 중 발생하는 오류를 검출하는 기술 - 패리티, 체크섬, CRC의 원리, 알고리즘, 그리고 실무 적용"
weight = 45
[taxonomies]
categories = ["studynotes-network"]
tags = ["Parity", "Checksum", "CRC", "Error Detection", "FCS", "Hamming"]
+++

# 오류 검출 코드 (Error Detection: Parity, Checksum, CRC)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 오류 검출 코드는 데이터 전송/저장 시 발생하는 비트 오류를 수신측에서 식별할 수 있도록 송신측에서 추가하는 중복 정보(Redundancy)로, 패리티(1비트), 체크섬(합 기반), CRC(다항식 나눗셈) 등이 있습니다.
> 2. **가치**: CRC-32는 이더넷 프레임에서 99.998%의 오류 검출률을 제공하며, 단일 비트 오류, 버스트 오류까지 검출 가능하여 네트워크 신뢰성의 핵심 기반이 됩니다.
> 3. **융합**: 현대 통신에서는 CRC와 FEC(Forward Error Correction)를 결합하여 HARQ(Hybrid ARQ)를 구현하며, 저장 시스템(SSD, HDD)에서는 ECC와 함께 데이터 무결성을 보장합니다.

---

## Ⅰ. 개요 (Context & Background)

디지털 통신 및 저장 시스템에서 데이터는 잡음, 간섭, 하드웨어 결함 등으로 인해 비트 오류가 발생할 수 있습니다. 오류 검출(Error Detection)은 이러한 오류를 수신측에서 식별하여 재전송을 요청(ARQ)하거나 폐기하는 기술입니다.

**💡 비유**: 오류 검출 코드는 **'우편물의 요금 확인'**과 같습니다. 편지에 요금을 적어두면(체크섬), 우체국에서 총액이 맞는지 확인하여 분실/변조 여부를 알 수 있습니다. CRC는 더 정교한 **'디지털 지문'**으로, 데이터의 내용이 1비트라도 바뀌면 지문이 완전히 달라집니다.

**등장 배경 및 발전 과정**:
1. **기존 기술의 치명적 한계점**: 초기 통신 시스템에서는 오류 검출이 없어 데이터 변형이 그대로 수신되어 잘못된 정보가 전달되었습니다.
2. **혁신적 패러다임 변화**: 1961년 CRC(Cyclic Redundancy Check)가 개발되어 강력한 오류 검출 능력을 갖추게 되었습니다. 이는 이더넷, HDLC, ZIP 파일 등 현대 디지털 시스템의 표준이 되었습니다.
3. **비즈니스적 요구사항**: 금융 거래, 의료 데이터, 자율주행 등에서 데이터 무결성은 필수적이며, 10⁻¹² 이하의 오류율을 요구합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 오류 검출 기술 분류

```
                        오류 검출 (Error Detection)
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
   ┌────┴────┐            ┌────┴────┐            ┌────┴────┐
   │ 패리티   │            │ 체크섬   │            │   CRC   │
   │ Parity  │            │Checksum │            │(다항식)  │
   └────┬────┘            └────┬────┘            └────┬────┘
        │                      │                      │
   ┌────┴────────┐        ┌────┴────┐          ┌─────┴─────┐
   │ 단순 패리티  │        │IP/UDP/  │          │ CRC-8     │
   │ 2차원 패리티 │        │TCP Check│          │ CRC-16    │
   │ 홀수/짝수   │        │sum      │          │ CRC-32    │
   └─────────────┘        └─────────┘          │ CRC-CCITT │
                                               └───────────┘
```

### 오류 검출 방식 상세 비교

| 특성 | 패리티 (Parity) | 체크섬 (Checksum) | CRC (Cyclic Redundancy Check) |
|---|---|---|---|
| **추가 비트 수** | 1비트 | 16/32비트 | 8/16/32비트 |
| **오버헤드** | 최소 | 작음 | 중간 |
| **단일 비트 오류** | 100% 검출 | 높음 | 100% 검출 |
| **버스트 오류** | 낮음 | 중간 | 매우 높음 |
| **구현 복잡도** | 매우 낮음 | 낮음 | 중간 (LFSR) |
| **주요 적용** | 시리얼 통신, 메모리 | IP/TCP/UDP | 이더넷, HDLC, ZIP |

### 정교한 구조 다이어그램: CRC 동작 원리

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CRC (Cyclic Redundancy Check)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  송신 과정 (Transmitter):                                                    │
│                                                                             │
│  ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐    │
│  │   데이터 메시지   │ ──→ │ r개 0 추가 (패딩) │ ──→ │   다항식 나눗셈   │    │
│  │   M(x) [m비트]   │     │   M(x) × x^r     │     │  G(x)로 나눔     │    │
│  └──────────────────┘     └──────────────────┘     └────────┬─────────┘    │
│                                                              │              │
│                                                              ↓              │
│                                                     ┌──────────────────┐    │
│                                                     │    나머지 R(x)    │    │
│                                                     │    [r비트 CRC]    │    │
│                                                     └────────┬─────────┘    │
│                                                              │              │
│                                                              ↓              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │               전송 프레임 = M(x) × x^r + R(x)                          │  │
│  │                   [원본 데이터]      [CRC]                            │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  수신 과정 (Receiver):                                                       │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      수신된 프레임                                     │  │
│  └──────────────────────────────┬───────────────────────────────────────┘  │
│                                 │                                           │
│                                 ↓                                           │
│                    ┌────────────────────────┐                               │
│                    │  G(x)로 나눗셈 수행     │                               │
│                    └────────────┬───────────┘                               │
│                                 │                                           │
│                    ┌────────────┴───────────┐                               │
│                    │                        │                               │
│                 나머지 = 0               나머지 ≠ 0                          │
│                    │                        │                               │
│                    ↓                        ↓                               │
│            ┌──────────────┐         ┌──────────────┐                       │
│            │  오류 없음    │         │  오류 검출!   │                       │
│            │  데이터 수용  │         │  재전송 요청  │                       │
│            └──────────────┘         └──────────────┘                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

**1. 패리티 비트 (Parity Bit)**

```
짝수 패리티 (Even Parity):
- 전체 1의 개수가 짝수가 되도록 패리티 비트 설정

데이터: 1 0 1 1 0 0 1  →  1의 개수 = 4 (짝수)
패리티 비트: 0

데이터: 1 0 1 1 0 1 1  →  1의 개수 = 5 (홀수)
패리티 비트: 1

장점:
- 구현이 매우 간단 (XOR 게임)
- 1비트 오차 100% 검출

단점:
- 2비트 오차 검출 불가
- 오류 위치 식별 불가
```

**2. 2차원 패리티 (2D Parity / Block Parurity)**

```
        비트 위치
        1 2 3 4 5 6 7 8  행 패리티
      ┌─────────────────┬───┐
    1 │ 1 0 1 1 0 0 1 0 │ 1 │
    2 │ 0 1 1 0 1 1 0 1 │ 1 │
    3 │ 1 1 0 1 0 1 1 0 │ 0 │
    4 │ 0 0 1 1 1 0 0 1 │ 0 │
      ├─────────────────┼───┤
열패리티│ 0 0 1 1 0 0 0 0 │ 0 │
      └─────────────────┴───┘

장점:
- 1비트 오차 위치 식별 가능 (행, 열 교차점)
- 2비트 오차도 검출 가능

적용: RAID-2, 일부 메모리 시스템
```

**3. 체크섬 (Internet Checksum)**

```
IP/TCP/UDP 체크섬 알고리즘:

1. 헤더를 16비트 단위로 분할
2. 모든 16비트 워드를 더함 (캐리 발생 시 wrap-around)
3. 결과의 1의 보수를 취함 → 체크섬

예시:
데이터: 4500 0073 0000 4000 4011 [checksum] c0a8 0001 c0a8 00c7

계산:
4500 + 0073 + 0000 + 4000 + 4011 + c0a8 + 0001 + c0a8 + 00c7
= 1B169 (캐리 포함)

Wrap-around: B169 + 1 = B16A
1의 보수: 4E95 (이것이 checksum)

검증:
수신 측에서 모든 워드(체크섬 포함)를 더하면
오류가 없을 경우 FFFF(모두 1)가 되어야 함

장점:
- 소프트웨어 구현 간단
- 임의 길이 데이터 처리 가능

단점:
- 버스트 오류에 취약
- 순서 변경 검출 불가
```

**4. CRC (Cyclic Redundancy Check)**

```
CRC 다항식 표현:

CRC-32 (IEEE 802.3):
G(x) = x^32 + x^26 + x^23 + x^22 + x^16 + x^12 + x^11 + x^10 +
       x^8 + x^7 + x^5 + x^4 + x^2 + x + 1

이진 표현: 100000100110000010001110110110111 (33비트)

CRC 계산 예시:
메시지: 11010011101100 (14비트)
생성 다항식: 1011 (4비트, CRC-3)

Step 1: 메시지 뒤에 3개의 0 추가
        11010011101100000

Step 2: XOR 나눗셈
        11010011101100000
        1011______________  (첫 4비트에 대해)
        ----
         1100
         1011
         ----
          1110
          1011
          ----
           1011
           1011
           ----
            0000...
            ...

Step 3: 최종 나머지가 CRC

이더넷 FCS (Frame Check Sequence):
- CRC-32 사용
- 프레임 끝에 4바이트 추가
- 모든 오류의 99.998% 검출
```

### CRC 오류 검출 능력

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CRC 오류 검출 능력 분석                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  r비트 CRC의 검출 능력:                                                      │
│                                                                             │
│  1. 모든 단일 비트 오류: 100% 검출                                           │
│     - G(x)이 2개 이상의 항을 가지면 충족                                     │
│                                                                             │
│  2. 모든 이중 비트 오류: 100% 검출                                           │
│     - G(x)이 3항 이상의 원시 다항식이면 충족                                 │
│                                                                             │
│  3. 홀수 개의 오류: 100% 검출                                                │
│     - G(x)이 (x+1)을 인수로 가지면 충족                                      │
│                                                                             │
│  4. 길이 ≤ r인 버스트 오류: 100% 검출                                        │
│     - r비트 CRC는 r비트 이하의 연속 오차 모두 검출                            │
│                                                                             │
│  5. 길이 = r+1인 버스트 오류: 1 - 2^(1-r) 확률로 검출                         │
│     - 예: CRC-32 → 99.99999995% 검출                                        │
│                                                                             │
│  6. 길이 > r+1인 버스트 오류: 1 - 2^(-r) 확률로 검출                          │
│     - 예: CRC-32 → 99.99999998% 검출                                        │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  CRC-32 이더넷 예시                                                 │    │
│  │  • 단일 비트 오류: 100%                                             │    │
│  │  • 32비트 이하 버스트: 100%                                         │    │
│  │  • 33비트 버스트: 99.99999995%                                      │    │
│  │  • 33비트 초과 버스트: 99.99999998%                                 │    │
│  │  • 미검출 오류 확률: < 2.3 × 10⁻¹⁰                                   │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: CRC 구현 (Python)

```python
import numpy as np
from typing import List, Tuple

class ErrorDetectionCodes:
    """오류 검출 코드 구현"""

    @staticmethod
    def parity_bit(data: List[int], even: bool = True) -> int:
        """
        패리티 비트 계산

        Args:
            data: 비트 리스트
            even: True면 짝수 패리티, False면 홀수 패리티

        Returns:
            패리티 비트 (0 또는 1)
        """
        ones_count = sum(data)
        if even:
            return ones_count % 2
        else:
            return (ones_count + 1) % 2

    @staticmethod
    def check_parity(data: List[int], parity_bit: int, even: bool = True) -> bool:
        """패리티 검증"""
        expected = ErrorDetectionCodes.parity_bit(data, even)
        return expected == parity_bit

    @staticmethod
    def internet_checksum(data: bytes) -> int:
        """
        Internet Checksum (IP/TCP/UDP)

        Args:
            data: 바이트 데이터

        Returns:
            16비트 체크섬
        """
        # 패딩 (홀수 길이인 경우)
        if len(data) % 2 != 0:
            data = data + b'\x00'

        # 16비트 워드로 분할하여 합계
        total = 0
        for i in range(0, len(data), 2):
            word = (data[i] << 8) + data[i + 1]
            total += word

        # 캐리 wrap-around
        while total > 0xFFFF:
            carry = total >> 16
            total = (total & 0xFFFF) + carry

        # 1의 보수
        checksum = ~total & 0xFFFF
        return checksum

    @staticmethod
    def verify_checksum(data: bytes, checksum: int) -> bool:
        """체크섬 검증"""
        # 데이터 + 체크섬의 체크섬이 0xFFFF면 OK
        # 구현 단순화를 위해 별도 계산
        calculated = ErrorDetectionCodes.internet_checksum(data)
        return calculated == checksum


class CRC:
    """CRC (Cyclic Redundancy Check) 구현"""

    # 표준 CRC 다항식들
    POLYNOMIALS = {
        'CRC-8': 0x07,           # x^8 + x^2 + x + 1
        'CRC-16-CCITT': 0x1021,  # x^16 + x^12 + x^5 + 1
        'CRC-16-IBM': 0x8005,    # x^16 + x^15 + x^2 + 1
        'CRC-32': 0x04C11DB7,    # IEEE 802.3
        'CRC-32C': 0x1EDC6F41,   # Castagnoli (iSCSI)
    }

    def __init__(self, polynomial: str = 'CRC-32'):
        self.name = polynomial
        self.poly = self.POLYNOMIALS.get(polynomial, 0x04C11DB7)
        self.width = self._get_width()

        # 조회 테이블 생성 (성능 최적화)
        self.table = self._generate_table()

    def _get_width(self) -> int:
        """CRC 비트 폭 결정"""
        if '32' in self.name:
            return 32
        elif '16' in self.name:
            return 16
        elif '8' in self.name:
            return 8
        return 32

    def _generate_table(self) -> List[int]:
        """CRC 계산용 조회 테이블 생성"""
        table = []
        for byte in range(256):
            crc = byte << (self.width - 8)
            for _ in range(8):
                if crc & (1 << (self.width - 1)):
                    crc = ((crc << 1) ^ self.poly) & ((1 << self.width) - 1)
                else:
                    crc = (crc << 1) & ((1 << self.width) - 1)
            table.append(crc)
        return table

    def calculate(self, data: bytes, init: int = 0xFFFFFFFF) -> int:
        """
        CRC 계산 (테이블 기반)

        Args:
            data: 입력 데이터
            init: 초기값

        Returns:
            CRC 값
        """
        crc = init
        for byte in data:
            # 상위 바이트로 테이블 인덱싱
            index = ((crc >> (self.width - 8)) ^ byte) & 0xFF
            crc = ((crc << 8) ^ self.table[index]) & ((1 << self.width) - 1)

        # 최종 XOR (CRC-32의 경우)
        if self.width == 32:
            crc = crc ^ 0xFFFFFFFF

        return crc

    def calculate_bitwise(self, data: bytes) -> int:
        """
        CRC 계산 (비트 단위, 교육용)

        나눗셈 과정을 명시적으로 보여줌
        """
        # 데이터를 비트열로 변환 + r개의 0 패딩
        bits = []
        for byte in data:
            for i in range(7, -1, -1):
                bits.append((byte >> i) & 1)

        # r개의 0 추가
        bits.extend([0] * self.width)

        # 다항식 비트열
        poly_bits = []
        temp = self.poly
        for i in range(self.width, -1, -1):
            poly_bits.append((temp >> i) & 1)

        # XOR 나눗셈
        for i in range(len(data) * 8):
            if bits[i] == 1:
                for j in range(len(poly_bits)):
                    bits[i + j] ^= poly_bits[j]

        # 나머지 추출
        return int(''.join(map(str, bits[-self.width:])), 2)

    def verify(self, data: bytes, crc: int) -> bool:
        """CRC 검증"""
        calculated = self.calculate(data)
        return calculated == crc

    def get_hex(self, data: bytes) -> str:
        """CRC를 16진수 문자열로 반환"""
        crc = self.calculate(data)
        if self.width == 32:
            return f"0x{crc:08X}"
        elif self.width == 16:
            return f"0x{crc:04X}"
        else:
            return f"0x{crc:02X}"


def demonstrate_error_detection():
    """오류 검출 시연"""
    print("=" * 60)
    print("오류 검출 코드 시연")
    print("=" * 60)

    # 1. 패리티 비트
    print("\n[1] 패리티 비트")
    data = [1, 0, 1, 1, 0, 0, 1]
    parity = ErrorDetectionCodes.parity_bit(data)
    print(f"데이터: {data}")
    print(f"1의 개수: {sum(data)}")
    print(f"짝수 패리티 비트: {parity}")

    # 오류 발생 시뮬레이션
    corrupted = data.copy()
    corrupted[2] = 1 - corrupted[2]  # 비트 반전
    is_valid = ErrorDetectionCodes.check_parity(corrupted, parity)
    print(f"오류 데이터: {corrupted}")
    print(f"오류 검출: {'아니오' if is_valid else '예'}")

    # 2. 체크섬
    print("\n[2] Internet Checksum")
    message = b"Hello, Network!"
    checksum = ErrorDetectionCodes.internet_checksum(message)
    print(f"메시지: {message}")
    print(f"체크섬: 0x{checksum:04X}")

    # 3. CRC
    print("\n[3] CRC-32 (이더넷 FCS)")
    crc32 = CRC('CRC-32')
    ethernet_frame = b"\x00\x01\x02\x03\x04\x05" + b"\xFF\xFF\xFF\xFF\xFF\xFF" + b"\x08\x00" + b"Payload data here"
    crc_value = crc32.calculate(ethernet_frame)
    print(f"프레임 길이: {len(ethernet_frame)} bytes")
    print(f"CRC-32: {crc32.get_hex(ethernet_frame)}")

    # 오류 주입 후 검증
    corrupted_frame = bytearray(ethernet_frame)
    corrupted_frame[20] ^= 0x01  # 1비트 오류
    is_valid = crc32.verify(bytes(corrupted_frame), crc_value)
    print(f"오류 주입 후 검증: {'성공' if is_valid else '실패 (오류 검출됨)'}")


def compare_crc_performance():
    """CRC 성능 비교"""
    print("\n" + "=" * 60)
    print("CRC 다항식별 성능 비교")
    print("=" * 60)

    test_data = b"The quick brown fox jumps over the lazy dog" * 100

    print(f"\n테스트 데이터: {len(test_data)} bytes")
    print(f"{'CRC Type':<15} {'CRC Value':<12} {'Time (relative)':<15}")
    print("-" * 45)

    for poly_name in ['CRC-8', 'CRC-16-CCITT', 'CRC-16-IBM', 'CRC-32', 'CRC-32C']:
        crc = CRC(poly_name)
        value = crc.get_hex(test_data)
        print(f"{poly_name:<15} {value:<12} {'-':<15}")


if __name__ == "__main__":
    demonstrate_error_detection()
    compare_crc_performance()
