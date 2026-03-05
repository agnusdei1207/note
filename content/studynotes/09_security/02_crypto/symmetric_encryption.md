+++
title = "대칭키 암호 (Symmetric Encryption)"
date = "2026-03-04"
[extra]
categories = "studynotes-09_security"
+++

# 대칭키 암호 (Symmetric Encryption)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 암호화와 복호화에 동일한 키를 사용하는 암호 방식으로, 빠른 처리 속도와 효율성으로 대량 데이터 보호에 최적화되어 있습니다.
> 2. **가치**: AES, ChaCha20 등 대용량 데이터 암호화, VPN, 디스크 암호화, 통신 보안의 핵심 기술입니다.
> 3. **융합**: 비대칭키 암호와 결합하여 하이브리드 암호 시스템 구성, TLS, PGP 등에 활용됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**대칭키 암호(Symmetric Encryption)**는 암호화(Encryption)와 복호화(Decryption)에 동일한 비밀키(Secret Key)를 사용하는 암호 시스템입니다. 송신자와 수신자가 사전에 키를 안전하게 공유해야 하는 특성이 있습니다.

**핵심 특성**:
- **동일 키 사용**: E_k(m) = c, D_k(c) = m
- **고속 처리**: 비대칭키 대비 100~1000배 빠름
- **키 분배 문제**: 안전한 키 전달이 핵심 과제
- **키 관리 복잡도**: n명 통신 시 n(n-1)/2개 키 필요

**주요 알고리즘**:
- **블록 암호**: AES, DES, 3DES, Blowfish, Camellia
- **스트림 암호**: ChaCha20, RC4(취약), Salsa20

#### 2. 💡 비유를 통한 이해
대칭키 암호는 **'동일 열쇠 자물쇠'**에 비유할 수 있습니다.
- **암호화**: 문을 잠그는 것 - 열쇠로 잠금
- **복호화**: 문을 여는 것 - 같은 열쇠로 열기
- **키 공유**: 열쇠를 상대방에게 안전하게 전달
- **문제**: 열쇠가 도난당하면 누구나 열 수 있음

#### 3. 등장 배경 및 발전 과정
1. **고전 암호**: 카이사르, 전치/치환 암호
2. **기계식 암호**: Enigma (2차대전)
3. **DES (1977)**: 미국 표준, 56비트
4. **AES (2001)**: Rijndael, 128/192/256비트
5. **ChaCha20 (2008)**: Daniel Bernstein, 스트림 암호
6. **TLS 1.3**: AES-GCM, ChaCha20-Poly1305 채택

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 대칭키 암호 알고리즘 비교 (표)

| 알고리즘 | 유형 | 키 길이 | 블록 크기 | 라운드 | 속도 | 보안 강도 |
|:---|:---|:---|:---|:---|:---|:---|
| **AES-128** | 블록 | 128비트 | 128비트 | 10 | 매우 빠름 | 높음 |
| **AES-256** | 블록 | 256비트 | 128비트 | 14 | 빠름 | 매우 높음 |
| **ChaCha20** | 스트림 | 256비트 | - | 20 | 매우 빠름 | 매우 높음 |
| **3DES** | 블록 | 168비트 | 64비트 | 48 | 느림 | 중간 |
| **DES** | 블록 | 56비트 | 64비트 | 16 | 빠름 | 취약 |
| **Camellia** | 블록 | 256비트 | 128비트 | 24 | 빠름 | 높음 |

#### 2. AES 구조 다이어그램

```text
<<< AES (Advanced Encryption Standard) Architecture >>>

    +------------------------------------------------------------------+
    |                    AES 암호화 프로세스                            |
    +------------------------------------------------------------------+
                                │
    [ 평문 128비트 ] ───────────┼─────────────────────────────────────►
                                │
                                v
    +------------------------------------------------------------------+
    |  Round 0: Initial Round Key Addition (AddRoundKey)               |
    |  ┌──────────────────────────────────────────────────────────┐   |
    |  │  Plaintext ⊕ RoundKey[0]                                 │   |
    |  └──────────────────────────────────────────────────────────┘   |
    +------------------------------------------------------------------+
                                │
                                v
    +------------------------------------------------------------------+
    |  Rounds 1 to N-1 (AES-128: 9, AES-256: 13)                      |
    |  ┌──────────────────────────────────────────────────────────┐   |
    |  │  SubBytes (S-Box 치환)                                    │   |
    |  │  - 각 바이트를 S-Box로 치환                               │   |
    |  │  - 비선형 변환으로 보안 제공                              │   |
    |  └──────────────────────────────────────────────────────────┘   |
    |  ┌──────────────────────────────────────────────────────────┐   |
    |  │  ShiftRows (행 이동)                                      │   |
    |  │  - 행별로 좌측 순환 이동 (0,1,2,3 바이트)                 │   |
    |  │  - 바이트 확산 효과                                       │   |
    |  └──────────────────────────────────────────────────────────┘   |
    |  ┌──────────────────────────────────────────────────────────┐   |
    |  │  MixColumns (열 혼합)                                     │   |
    |  │  - GF(2^8) 상에서 행렬 곱셈                              │   |
    |  │  - 각 열을 선형 변환                                      │   |
    |  └──────────────────────────────────────────────────────────┘   |
    |  ┌──────────────────────────────────────────────────────────┐   |
    |  │  AddRoundKey (라운드 키 XOR)                              │   |
    |  │  - 현재 상태 ⊕ RoundKey[i]                               │   |
    |  └──────────────────────────────────────────────────────────┘   |
    +------------------------------------------------------------------+
                                │
                                v
    +------------------------------------------------------------------+
    |  Round N (Final Round - MixColumns 제외)                        |
    |  ┌──────────────────────────────────────────────────────────┐   |
    |  │  SubBytes → ShiftRows → AddRoundKey                      │   |
    |  └──────────────────────────────────────────────────────────┘   |
    +------------------------------------------------------------------+
                                │
                                v
    [ 암호문 128비트 ] ◄──────────────────────────────────────────────


<<< AES State Matrix (상태 행렬) >>@

    입력 128비트를 4×4 바이트 행렬로 구성:

    ┌────────┬────────┬────────┬────────┐
    │  in0   │  in4   │  in8   │  in12  │
    ├────────┼────────┼────────┼────────┤
    │  in1   │  in5   │  in9   │  in13  │
    ├────────┼────────┼────────┼────────┤
    │  in2   │  in6   │  in10  │  in14  │
    ├────────┼────────┼────────┼────────┤
    │  in3   │  in7   │  in11  │  in15  │
    └────────┴────────┴────────┴────────┘

    ShiftRows 후:

    ┌────────┬────────┬────────┬────────┐
    │  s0,0  │  s0,1  │  s0,2  │  s0,3  │  ← 이동 없음
    ├────────┼────────┼────────┼────────┤
    │  s1,1  │  s1,2  │  s1,3  │  s1,0  │  ← 1바이트 좌측 이동
    ├────────┼────────┼────────┼────────┤
    │  s2,2  │  s2,3  │  s2,0  │  s2,1  │  ← 2바이트 좌측 이동
    ├────────┼────────┼────────┼────────┤
    │  s3,3  │  s3,0  │  s3,1  │  s3,2  │  ← 3바이트 좌측 이동
    └────────┴────────┴────────┴────────┘


<<< AES 운영 모드 (Block Cipher Modes) >>>

    1. ECB (Electronic Codebook) - 사용 권장 X
    ┌─────────────────────────────────────────────────────────────┐
    │  P1    P2    P3    P4                                      │
    │  │     │     │     │                                       │
    │  ▼     ▼     ▼     ▼     각 블록 독립적 암호화             │
    │  AES   AES   AES   AES    동일 평문 → 동일 암호문          │
    │  │     │     │     │     패턴 노출 위험                    │
    │  ▼     ▼     ▼     ▼                                       │
    │  C1    C2    C3    C4                                      │
    └─────────────────────────────────────────────────────────────┘

    2. CBC (Cipher Block Chaining)
    ┌─────────────────────────────────────────────────────────────┐
    │  IV    P1    P2    P3                                      │
    │  │     │     │     │                                       │
    │  ⊕     ⊕     ⊕     ⊕     이전 암호문과 XOR                 │
    │  │     │     │     │     순차적 처리 (병렬 불가)            │
    │  ▼     ▼     ▼     ▼                                       │
    │  AES   AES   AES   AES                                     │
    │  │     │     │     │                                       │
    │  ▼     ▼     ▼     ▼                                       │
    │  C1───►C2───►C3───►C4                                      │
    └─────────────────────────────────────────────────────────────┘

    3. GCM (Galois/Counter Mode) - 권장
    ┌─────────────────────────────────────────────────────────────┐
    │  Nonce  Counter                                           │
    │    │       │                                              │
    │    ▼       ▼                                              │
    │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                         │
    │  │AES-K│ │AES-K│ │AES-K│ │AES-K│  병렬 처리 가능         │
    │  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘  인증+암호화 (AEAD)     │
    │     │       │       │       │                              │
    │     ⊕       ⊕       ⊕       ⊕                              │
    │     │       │       │       │                              │
    │  P1─┴─►C1 P2─┴─►C2 P3─┴─►C3 P4─┴─►C4                      │
    │                                                             │
    │  ┌──────────────────────────────────────┐                 │
    │  │  GHASH (인증 태그 생성)               │                 │
    │  │  Tag = GHASH(AAD, C1||C2||C3||C4)    │                 │
    │  └──────────────────────────────────────┘                 │
    └─────────────────────────────────────────────────────────────┘
```

#### 3. 심층 동작 원리: AES 구현

```python
import os
import struct
from typing import Tuple, List, Optional
from dataclasses import dataclass
from enum import Enum

class AESMode(Enum):
    ECB = "ecb"
    CBC = "cbc"
    CTR = "ctr"
    GCM = "gcm"

# AES S-Box (Substitution Box)
S_BOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# 역 S-Box (복호화용)
INV_S_BOX = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

# Rcon (Round Constants)
RCON = [
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36
]

class AES:
    """
    AES (Advanced Encryption Standard) 구현
    AES-128, AES-192, AES-256 지원
    """

    def __init__(self, key: bytes):
        """
        AES 초기화

        Args:
            key: 16, 24, 또는 32바이트 키
        """
        self.key = key
        self.key_size = len(key)

        if self.key_size == 16:
            self.rounds = 10
        elif self.key_size == 24:
            self.rounds = 12
        elif self.key_size == 32:
            self.rounds = 14
        else:
            raise ValueError("Key must be 16, 24, or 32 bytes")

        # 키 확장
        self.round_keys = self._key_expansion(key)

    def _key_expansion(self, key: bytes) -> List[List[int]]:
        """키 확장 (Key Schedule)"""
        # 초기 키를 4바이트 단위로 분할
        expanded = []
        for i in range(0, len(key), 4):
            expanded.append(list(key[i:i+4]))

        # 확장
        for i in range(self.key_size // 4, 4 * (self.rounds + 1)):
            temp = expanded[i - 1][:]

            if i % (self.key_size // 4) == 0:
                # RotWord
                temp = temp[1:] + temp[:1]
                # SubWord
                temp = [S_BOX[b] for b in temp]
                # XOR with Rcon
                temp[0] ^= RCON[i // (self.key_size // 4)]

            elif self.key_size == 32 and i % 8 == 4:
                # AES-256 추가 SubWord
                temp = [S_BOX[b] for b in temp]

            expanded.append([
                expanded[i - self.key_size // 4][j] ^ temp[j]
                for j in range(4)
            ])

        return expanded

    def _sub_bytes(self, state: List[List[int]]) -> List[List[int]]:
        """SubBytes 변환"""
        return [[S_BOX[state[r][c]] for c in range(4)] for r in range(4)]

    def _inv_sub_bytes(self, state: List[List[int]]) -> List[List[int]]:
        """역 SubBytes 변환"""
        return [[INV_S_BOX[state[r][c]] for c in range(4)] for r in range(4)]

    def _shift_rows(self, state: List[List[int]]) -> List[List[int]]:
        """ShiftRows 변환"""
        return [
            [state[0][0], state[0][1], state[0][2], state[0][3]],
            [state[1][1], state[1][2], state[1][3], state[1][0]],
            [state[2][2], state[2][3], state[2][0], state[2][1]],
            [state[3][3], state[3][0], state[3][1], state[3][2]]
        ]

    def _inv_shift_rows(self, state: List[List[int]]) -> List[List[int]]:
        """역 ShiftRows 변환"""
        return [
            [state[0][0], state[0][1], state[0][2], state[0][3]],
            [state[1][3], state[1][0], state[1][1], state[1][2]],
            [state[2][2], state[2][3], state[2][0], state[2][1]],
            [state[3][1], state[3][2], state[3][3], state[3][0]]
        ]

    def _xtime(self, a: int) -> int:
        """GF(2^8) 곱셈 (x)"""
        return ((a << 1) ^ 0x1b) & 0xff if a & 0x80 else (a << 1) & 0xff

    def _mix_column(self, col: List[int]) -> List[int]:
        """단일 열 MixColumns"""
        a = col[:]
        b = [self._xtime(x) for x in a]

        return [
            b[0] ^ a[1] ^ b[1] ^ a[2] ^ a[3],
            a[0] ^ b[1] ^ a[2] ^ b[2] ^ a[3],
            a[0] ^ a[1] ^ b[2] ^ a[3] ^ b[3],
            a[0] ^ b[0] ^ a[1] ^ a[2] ^ b[3]
        ]

    def _mix_columns(self, state: List[List[int]]) -> List[List[int]]:
        """MixColumns 변환"""
        result = [[0] * 4 for _ in range(4)]
        for c in range(4):
            col = [state[r][c] for r in range(4)]
            mixed = self._mix_column(col)
            for r in range(4):
                result[r][c] = mixed[r]
        return result

    def _inv_mix_column(self, col: List[int]) -> List[int]:
        """단일 열 역 MixColumns"""
        a = col[:]
        b = [self._xtime(x) for x in a]
        c = [self._xtime(self._xtime(x)) for x in a]

        return [
            a[0] ^ b[0] ^ c[0] ^ a[1] ^ c[1] ^ a[2] ^ b[2] ^ c[2] ^ a[3] ^ c[3],
            a[0] ^ c[0] ^ a[1] ^ b[1] ^ c[1] ^ a[2] ^ c[2] ^ a[3] ^ b[3] ^ c[3],
            a[0] ^ b[0] ^ c[0] ^ a[1] ^ c[1] ^ a[2] ^ b[2] ^ c[2] ^ a[3] ^ c[3],
            a[0] ^ c[0] ^ a[1] ^ b[1] ^ c[1] ^ a[2] ^ c[2] ^ a[3] ^ b[3] ^ c[3]
        ]

    def _inv_mix_columns(self, state: List[List[int]]) -> List[List[int]]:
        """역 MixColumns 변환"""
        result = [[0] * 4 for _ in range(4)]
        for c in range(4):
            col = [state[r][c] for r in range(4)]
            mixed = self._inv_mix_column(col)
            for r in range(4):
                result[r][c] = mixed[r]
        return result

    def _add_round_key(self, state: List[List[int]], round_num: int) -> List[List[int]]:
        """AddRoundKey 변환"""
        result = [[0] * 4 for _ in range(4)]
        for c in range(4):
            for r in range(4):
                result[r][c] = state[r][c] ^ self.round_keys[round_num * 4 + c][r]
        return result

    def _bytes_to_state(self, block: bytes) -> List[List[int]]:
        """바이트 → 상태 행렬 변환"""
        return [[block[r + 4*c] for c in range(4)] for r in range(4)]

    def _state_to_bytes(self, state: List[List[int]]) -> bytes:
        """상태 행렬 → 바이트 변환"""
        return bytes([state[r][c] for c in range(4) for r in range(4)])

    def encrypt_block(self, plaintext: bytes) -> bytes:
        """
        단일 블록 암호화 (128비트)

        Args:
            plaintext: 16바이트 평문 블록

        Returns:
            16바이트 암호문 블록
        """
        if len(plaintext) != 16:
            raise ValueError("Block must be 16 bytes")

        state = self._bytes_to_state(plaintext)

        # Initial Round
        state = self._add_round_key(state, 0)

        # Main Rounds
        for round_num in range(1, self.rounds):
            state = self._sub_bytes(state)
            state = self._shift_rows(state)
            state = self._mix_columns(state)
            state = self._add_round_key(state, round_num)

        # Final Round
        state = self._sub_bytes(state)
        state = self._shift_rows(state)
        state = self._add_round_key(state, self.rounds)

        return self._state_to_bytes(state)

    def decrypt_block(self, ciphertext: bytes) -> bytes:
        """
        단일 블록 복호화 (128비트)

        Args:
            ciphertext: 16바이트 암호문 블록

        Returns:
            16바이트 평문 블록
        """
        if len(ciphertext) != 16:
            raise ValueError("Block must be 16 bytes")

        state = self._bytes_to_state(ciphertext)

        # Initial Round (inverse order)
        state = self._add_round_key(state, self.rounds)

        # Main Rounds
        for round_num in range(self.rounds - 1, 0, -1):
            state = self._inv_shift_rows(state)
            state = self._inv_sub_bytes(state)
            state = self._add_round_key(state, round_num)
            state = self._inv_mix_columns(state)

        # Final Round
        state = self._inv_shift_rows(state)
        state = self._inv_sub_bytes(state)
        state = self._add_round_key(state, 0)

        return self._state_to_bytes(state)


class AES_CBC:
    """
    AES-CBC 모드 구현
    """

    def __init__(self, key: bytes):
        self.aes = AES(key)

    def encrypt(self, plaintext: bytes, iv: bytes) -> bytes:
        """
        CBC 모드 암호화

        Args:
            plaintext: 평문 (16의 배수여야 함 - PKCS7 패딩 필요)
            iv: 16바이트 초기화 벡터
        """
        if len(iv) != 16:
            raise ValueError("IV must be 16 bytes")

        # PKCS7 패딩
        pad_len = 16 - (len(plaintext) % 16)
        padded = plaintext + bytes([pad_len] * pad_len)

        ciphertext = b""
        prev_block = iv

        for i in range(0, len(padded), 16):
            block = padded[i:i+16]
            # XOR with previous ciphertext (or IV for first block)
            xored = bytes([block[j] ^ prev_block[j] for j in range(16)])
            # Encrypt
            encrypted = self.aes.encrypt_block(xored)
            ciphertext += encrypted
            prev_block = encrypted

        return ciphertext

    def decrypt(self, ciphertext: bytes, iv: bytes) -> bytes:
        """
        CBC 모드 복호화
        """
        if len(iv) != 16:
            raise ValueError("IV must be 16 bytes")

        if len(ciphertext) % 16 != 0:
            raise ValueError("Ciphertext must be multiple of 16 bytes")

        plaintext = b""
        prev_block = iv

        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            # Decrypt
            decrypted = self.aes.decrypt_block(block)
            # XOR with previous ciphertext (or IV for first block)
            xored = bytes([decrypted[j] ^ prev_block[j] for j in range(16)])
            plaintext += xored
            prev_block = block

        # PKCS7 언패딩
        pad_len = plaintext[-1]
        if pad_len > 16 or pad_len == 0:
            raise ValueError("Invalid padding")
        if plaintext[-pad_len:] != bytes([pad_len] * pad_len):
            raise ValueError("Invalid padding")

        return plaintext[:-pad_len]


class AES_GCM:
    """
    AES-GCM (Galois/Counter Mode) 구현
    AEAD (Authenticated Encryption with Associated Data)
    """

    def __init__(self, key: bytes):
        self.aes = AES(key)
        # GHASH를 위한 H 키 계산
        self.h = self.aes.encrypt_block(b'\x00' * 16)

    def _gcm_mult(self, x: bytes, y: bytes) -> bytes:
        """GF(2^128) 곱셈 (간소화된 구현)"""
        # 실제 구현에서는 더 효율적인 알고리즘 사용
        result = 0
        x_int = int.from_bytes(x, 'big')
        y_int = int.from_bytes(y, 'big')

        for i in range(128):
            if y_int & (1 << (127 - i)):
                result ^= x_int
            if x_int & 1:
                x_int = (x_int >> 1) ^ 0xe1000000000000000000000000000000
            else:
                x_int >>= 1

        return result.to_bytes(16, 'big')

    def _ghash(self, data: bytes) -> bytes:
        """GHASH 계산"""
        # 패딩
        pad_len = (16 - (len(data) % 16)) % 16
        padded = data + b'\x00' * pad_len

        result = b'\x00' * 16
        for i in range(0, len(padded), 16):
            block = padded[i:i+16]
            xored = bytes([result[j] ^ block[j] for j in range(16)])
            result = self._gcm_mult(xored, self.h)

        return result

    def _gctr(self, icb: bytes, data: bytes) -> bytes:
        """GCTR (Counter Mode) 암호화"""
        result = b""
        cb = icb

        for i in range(0, len(data), 16):
            block = data[i:i+16]
            # 패딩
            if len(block) < 16:
                block = block + b'\x00' * (16 - len(block))

            encrypted_cb = self.aes.encrypt_block(cb)
            xored = bytes([block[j] ^ encrypted_cb[j] for j in range(len(block) if i + 16 <= len(data) else len(data) - i)])

            if i + 16 <= len(data):
                result += xored
            else:
                result += xored[:len(data) - i]

            # Counter 증가
            cb_int = int.from_bytes(cb, 'big') + 1
            cb = cb_int.to_bytes(16, 'big')

        return result

    def encrypt(self,
                plaintext: bytes,
                nonce: bytes,
                aad: bytes = b"") -> Tuple[bytes, bytes]:
        """
        GCM 암호화

        Args:
            plaintext: 평문
            nonce: 12바이트 논스 (IV)
            aad: Additional Authenticated Data

        Returns:
            (ciphertext, auth_tag)
        """
        if len(nonce) != 12:
            raise ValueError("Nonce must be 12 bytes")

        # J0 계산
        j0 = nonce + b'\x00\x00\x00\x01'

        # 암호화
        ciphertext = self._gctr(j0, plaintext)

        # GHASH 입력 구성
        aad_bits = len(aad) * 8
        ct_bits = len(ciphertext) * 8
        len_block = aad_bits.to_bytes(8, 'big') + ct_bits.to_bytes(8, 'big')

        ghash_input = aad + b'\x00' * ((16 - len(aad) % 16) % 16)
        ghash_input += ciphertext + b'\x00' * ((16 - len(ciphertext) % 16) % 16)
        ghash_input += len_block

        s = self._ghash(ghash_input)

        # 인증 태그
        tag = self._gctr(j0, s)[:16]

        return ciphertext, tag

    def decrypt(self,
                ciphertext: bytes,
                nonce: bytes,
                tag: bytes,
                aad: bytes = b"") -> Optional[bytes]:
        """
        GCM 복호화

        Returns:
            평문 (인증 실패 시 None)
        """
        if len(nonce) != 12:
            raise ValueError("Nonce must be 12 bytes")

        # J0 계산
        j0 = nonce + b'\x00\x00\x00\x01'

        # 태그 검증
        aad_bits = len(aad) * 8
        ct_bits = len(ciphertext) * 8
        len_block = aad_bits.to_bytes(8, 'big') + ct_bits.to_bytes(8, 'big')

        ghash_input = aad + b'\x00' * ((16 - len(aad) % 16) % 16)
        ghash_input += ciphertext + b'\x00' * ((16 - len(ciphertext) % 16) % 16)
        ghash_input += len_block

        s = self._ghash(ghash_input)
        expected_tag = self._gctr(j0, s)[:16]

        if not self._constant_time_compare(tag, expected_tag):
            return None  # 인증 실패

        # 복호화
        plaintext = self._gctr(j0, ciphertext)
        return plaintext

    def _constant_time_compare(self, a: bytes, b: bytes) -> bool:
        """상수 시간 비교 (타이밍 공격 방지)"""
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a, b):
            result |= x ^ y
        return result == 0


# 사용 예시
if __name__ == "__main__":
    # 키 생성 (실제로는 안전한 난수 사용)
    key_256 = os.urandom(32)

    # 1. 기본 AES 블록 암호화
    print("=== AES Block Encryption ===")
    aes = AES(key_256)
    plaintext_block = b"Hello World!!!!!"  # 정확히 16바이트
    ciphertext_block = aes.encrypt_block(plaintext_block)
    decrypted_block = aes.decrypt_block(ciphertext_block)

    print(f"Plaintext: {plaintext_block}")
    print(f"Ciphertext: {ciphertext_block.hex()}")
    print(f"Decrypted: {decrypted_block}")
    print(f"Match: {plaintext_block == decrypted_block}")

    # 2. AES-CBC 모드
    print("\n=== AES-CBC Mode ===")
    aes_cbc = AES_CBC(key_256)
    iv = os.urandom(16)
    plaintext = b"This is a longer message that needs multiple blocks to encrypt!"

    ciphertext = aes_cbc.encrypt(plaintext, iv)
    decrypted = aes_cbc.decrypt(ciphertext, iv)

    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext length: {len(ciphertext)} bytes")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {plaintext == decrypted}")

    # 3. AES-GCM 모드
    print("\n=== AES-GCM Mode (AEAD) ===")
    aes_gcm = AES_GCM(key_256)
    nonce = os.urandom(12)
    aad = b"Additional authenticated data"

    ct, tag = aes_gcm.encrypt(plaintext, nonce, aad)
    decrypted = aes_gcm.decrypt(ct, nonce, tag, aad)

    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext length: {len(ct)} bytes")
    print(f"Auth tag: {tag.hex()}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {plaintext == decrypted}")

    # 잘못된 태그 테스트
    bad_tag = os.urandom(16)
    result = aes_gcm.decrypt(ct, nonce, bad_tag, aad)
    print(f"Bad tag decryption: {'Failed' if result is None else 'Unexpected success'}")
