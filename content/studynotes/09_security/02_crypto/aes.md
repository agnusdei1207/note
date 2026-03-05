+++
title = "AES (Advanced Encryption Standard)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# AES (Advanced Encryption Standard)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 미국 NIST가 2001년 표준으로 채택한 블록 암호 알고리즘으로, Rijndael 알고리즘 기반의 SPN(Substitution-Permutation Network) 구조로 128/192/256비트 키를 지원합니다.
> 2. **가치**: 현재 전 세계에서 가장 널리 사용되는 대칭키 암호로, TLS, VPN, 디스크 암호화, 데이터베이스 암호화 등 모든 보안 영역의 핵심입니다.
> 3. **융합**: AES-GCM(인증 암호화), AES-NI(하드웨어 가속), HSM(키 보호)과 결합하여 성능과 보안을 동시에 확보합니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**AES(Advanced Encryption Standard)**는 2001년 미국 국립표준기술연구소(NIST)가 FIPS 197로 발표한 대칭키 블록 암호입니다. 벨기에 암호학자 Joan Daemen과 Vincent Rijmen이 개발한 Rijndael 알고리즘을 기반으로 합니다.

**핵심 특성**:

| 특성 | 값 | 설명 |
|:---|:---|:---|
| **블록 크기** | 128비트 (16바이트) | 고정 |
| **키 길이** | 128/192/256비트 | 선택 가능 |
| **라운드 수** | 10/12/14 | 키 길이에 따라 결정 |
| **구조** | SPN (Substitution-Permutation Network) | Feistel 구조 아님 |
| **보안 강도** | 128/192/256비트 | 키 길이와 동일 |

**AES 변종**:
```
┌─────────────────────────────────────────────────────────────────┐
│                    AES 변종 비교                                │
├─────────────────────────────────────────────────────────────────┤
│  변종      │ 키 길이  │ 라운드 │ 보안 강도 │ 권장 용도         │
│  ─────────────────────────────────────────────────────────────  │
│  AES-128   │ 128비트  │ 10     │ 128비트   │ 일반적 용도       │
│  AES-192   │ 192비트  │ 12     │ 192비트   │ 정부/군사         │
│  AES-256   │ 256비트  │ 14     │ 256비트   │ 최고 보안 요구    │
│                                                                 │
│  ※ AES-256은 양자 컴퓨팅에도 안전할 것으로 예상됨              │
└─────────────────────────────────────────────────────────────────┘
```

#### 2. 비유를 통한 이해
AES는 **'디지털 금고의 자물쇠'**에 비유할 수 있습니다.
- **평문**: 금고에 넣을 보석
- **암호문**: 금고에 넣어 잠근 상태
- **키**: 금고 열쇠 (128/192/256비트 = 열쇠 복잡도)
- **라운드**: 자물쇠의 걸쇠 수 (많을수록 풀기 어려움)
- **S-Box**: 걸쇠의 특수한 모양 (예측 불가능하게 섞음)

#### 3. 등장 배경 및 발전 과정
1. **1977년**: DES 표준화 (56비트 키)
2. **1990년대**: DES 무력화 (전사력 공격 가능)
3. **1997년**: NIST, 새로운 표준 공모 시작
4. **2000년**: Rijndael 최종 선정 (15개 후보 중)
5. **2001년**: FIPS 197로 공식 표준화
6. **현재**: 전 세계 사실상 표준, AES-NI 하드웨어 가속

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. AES 구조 다이어그램

```text
<<< AES 암호화 프로세스 상세 >>>

    ┌──────────────────────────────────────────────────────────────────────┐
    │                    AES 암호화 아키텍처                               │
    └──────────────────────────────────────────────────────────────────────┘
                                    │
    [평문 128비트] ─────────────────┼─────────────────────────────────────►
                                    │
                                    ▼
    ┌──────────────────────────────────────────────────────────────────────┐
    │  Key Expansion (키 확장)                                             │
    │  ┌────────────────────────────────────────────────────────────────┐ │
    │  │  원본 키(128/192/256비트) → (라운드+1)개의 라운드 키 생성      │ │
    │  │                                                                │ │
    │  │  AES-128: 128비트 키 → 11개 × 128비트 = 1408비트              │ │
    │  │  AES-256: 256비트 키 → 15개 × 128비트 = 1920비트              │ │
    │  └────────────────────────────────────────────────────────────────┘ │
    └──────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    ┌──────────────────────────────────────────────────────────────────────┐
    │  Initial Round (라운드 0)                                           │
    │  ┌────────────────────────────────────────────────────────────────┐ │
    │  │  AddRoundKey: State ⊕ RoundKey[0]                              │ │
    │  │                                                                │ │
    │  │     State Matrix (4×4 바이트):                                │ │
    │  │     ┌────────┬────────┬────────┬────────┐                     │ │
    │  │     │  b0    │  b4    │  b8    │  b12   │                     │ │
    │  │     ├────────┼────────┼────────┼────────┤                     │ │
    │  │     │  b1    │  b5    │  b9    │  b13   │                     │ │
    │  │     ├────────┼────────┼────────┼────────┤                     │ │
    │  │     │  b2    │  b6    │  b10   │  b14   │                     │ │
    │  │     ├────────┼────────┼────────┼────────┤                     │ │
    │  │     │  b3    │  b7    │  b11   │  b15   │                     │ │
    │  │     └────────┴────────┴────────┴────────┘                     │ │
    │  └────────────────────────────────────────────────────────────────┘ │
    └──────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    ┌──────────────────────────────────────────────────────────────────────┐
    │  Main Rounds (1 ~ N-1) ─────────────────────────────────────────    │
    │  ┌────────────────────────────────────────────────────────────────┐ │
    │  │                                                                │ │
    │  │  ┌──────────────────────────────────────────────────────────┐ │ │
    │  │  │  1. SubBytes (바이트 치환)                                │ │ │
    │  │  │     - 각 바이트를 S-Box를 통해 치환                       │ │ │
    │  │  │     - 비선형 변환으로 차분/선형 공격 방어                 │ │ │
    │  │  │     - 예: 0x53 → S-Box[0x53] = 0xed                      │ │ │
    │  │  └──────────────────────────────────────────────────────────┘ │ │
    │  │                           │                                    │ │
    │  │                           ▼                                    │ │
    │  │  ┌──────────────────────────────────────────────────────────┐ │ │
    │  │  │  2. ShiftRows (행 이동)                                   │ │ │
    │  │  │     - Row 0: 이동 없음                                    │ │ │
    │  │  │     - Row 1: 1바이트 좌측 순환 이동                       │ │ │
    │  │  │     - Row 2: 2바이트 좌측 순환 이동                       │ │ │
    │  │  │     - Row 3: 3바이트 좌측 순환 이동                       │ │ │
    │  │  │     - 바이트 간 확산(Diffusion) 제공                      │ │ │
    │  │  └──────────────────────────────────────────────────────────┘ │ │
    │  │                           │                                    │ │
    │  │                           ▼                                    │ │
    │  │  ┌──────────────────────────────────────────────────────────┐ │ │
    │  │  │  3. MixColumns (열 혼합)                                  │ │ │
    │  │  │     - 각 열에 고정 행렬 곱셈 (GF(2^8))                    │ │ │
    │  │  │     - 4바이트가 서로 영향을 주며 혼합                      │ │ │
    │  │  │     - 추가적인 확산 제공                                   │ │ │
    │  │  │                                                          │ │ │
    │  │  │     [s'0]   [02 03 01 01] [s0]                          │ │ │
    │  │  │     [s'1] = [01 02 03 01] [s1]                          │ │ │
    │  │  │     [s'2]   [01 01 02 03] [s2]                          │ │ │
    │  │  │     [s'3]   [03 01 01 02] [s3]                          │ │ │
    │  │  └──────────────────────────────────────────────────────────┘ │ │
    │  │                           │                                    │ │
    │  │                           ▼                                    │ │
    │  │  ┌──────────────────────────────────────────────────────────┐ │ │
    │  │  │  4. AddRoundKey (라운드 키 XOR)                          │ │ │
    │  │  │     - State ⊕ RoundKey[i]                                │ │ │
    │  │  │     - 키 의존성 추가                                       │ │ │
    │  │  └──────────────────────────────────────────────────────────┘ │ │
    │  │                                                                │ │
    │  └────────────────────────────────────────────────────────────────┘ │
    │                        ↑ 반복 (AES-128: 9회) ───────────────────────│
    └──────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    ┌──────────────────────────────────────────────────────────────────────┐
    │  Final Round (라운드 N) ─ MixColumns 제외                           │
    │  ┌────────────────────────────────────────────────────────────────┐ │
    │  │  SubBytes → ShiftRows → AddRoundKey                            │ │
    │  └────────────────────────────────────────────────────────────────┘ │
    └──────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    [암호문 128비트] ◄─────────────────────────────────────────────────────


<<< AES 복호화 프로세스 >>>

    암호화의 역순으로 수행:
    - InvSubBytes (역 S-Box)
    - InvShiftRows (역 행 이동)
    - InvMixColumns (역 열 혼합)
    - AddRoundKey (동일, XOR은 자기 자신이 역)
```

#### 2. AES S-Box 구조

```text
<<< AES S-Box (치환 테이블) >>>

    S-Box 생성 공식:
    1. 입력 바이트 x의 GF(2^8) 역원 계산: y = x^(-1)
    2. 아핀 변환 적용: S[x] = A·y + c

    아핀 변환 행렬 (GF(2)):
    ┌───────────────────────────────────┐
    │ 1 1 1 1 1 0 0 0 │   │ 0 │
    │ 0 1 1 1 1 1 0 0 │   │ 1 │
    │ 0 0 1 1 1 1 1 0 │   │ 1 │
    │ 0 0 0 1 1 1 1 1 │ + │ 0 │
    │ 1 0 0 0 1 1 1 1 │   │ 0 │
    │ 1 1 0 0 0 1 1 1 │   │ 0 │
    │ 1 1 1 0 0 0 1 1 │   │ 1 │
    │ 1 1 1 1 0 0 0 1 │   │ 1 │
    └───────────────────────────────────┘

    S-Box 예시 (일부):
    ┌─────────────────────────────────────────────────────────────────────┐
    │     0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f │
    │ ─────────────────────────────────────────────────────────────────  │
    │ 0│ 63  7c  77  7b  f2  6b  6f  c5  30  01  67  2b  fe  d7  ab  76 │
    │ 1│ ca  82  c9  7d  fa  59  47  f0  ad  d4  a2  af  9c  a4  72  c0 │
    │ 2│ b7  fd  93  26  36  3f  f7  cc  34  a5  e5  f1  71  d8  31  15 │
    │...                                                                  │
    │ f│ 8c  a1  89  0d  bf  e6  42  68  41  99  2d  0f  b0  54  bb  16 │
    └─────────────────────────────────────────────────────────────────────┘

    특징:
    - 고정된 256바이트 테이블
    - 비선형성: 입력과 출력 간 선형 관계 없음
    - 역원 존재: InvSubBytes를 위한 역 S-Box 존재
```

#### 3. AES 운영 모드 (Block Cipher Modes)

```text
<<< AES 운영 모드 비교 >>>

    1. ECB (Electronic Codebook) ─ [사용 권장 안 함]
    ┌─────────────────────────────────────────────────────────────────────┐
    │  P1    P2    P3    P4                                              │
    │  │     │     │     │     각 블록 독립 암호화                      │
    │  ▼     ▼     ▼     ▼     동일 평문 → 동일 암호문                  │
    │ AES   AES   AES   AES    패턴 노출 위험                           │
    │  │     │     │     │                                               │
    │  ▼     ▼     ▼     ▼                                               │
    │  C1    C2    C3    C4                                              │
    └─────────────────────────────────────────────────────────────────────┘

    2. CBC (Cipher Block Chaining) ─ [일반적 사용]
    ┌─────────────────────────────────────────────────────────────────────┐
    │  IV    P1    P2    P3                                              │
    │  │     │     │     │     이전 암호문과 XOR 후 암호화              │
    │  ⊕     ⊕     ⊕     ⊕     동일 평문 → 다른 암호문                  │
    │  │     │     │     │     순차적 처리만 가능 (병렬 불가)           │
    │  ▼     ▼     ▼     ▼                                               │
    │ AES   AES   AES   AES                                              │
    │  │     │     │     │                                               │
    │  ▼     ▼     ▼     ▼                                               │
    │  C1───►C2───►C3───►C4    IV는 예측 불가능해야 함                   │
    └─────────────────────────────────────────────────────────────────────┘

    3. CTR (Counter Mode) ─ [병렬 처리 가능]
    ┌─────────────────────────────────────────────────────────────────────┐
    │  Nonce│Nonce│Nonce│Nonce                                           │
    │   +1   +2   +3   +4     카운터 값을 암호화 후 XOR                  │
    │  │     │     │     │     병렬 암호화/복호화 가능                   │
    │  ▼     ▼     ▼     ▼     랜덤 접근 가능                           │
    │ AES   AES   AES   AES                                              │
    │  │     │     │     │                                               │
    │  ⊕     ⊕     ⊕     ⊕                                               │
    │  │     │     │     │                                               │
    │ P1─┴─►C1 P2─┴─►C2 P3─┴─►C3 P4─┴─►C4                               │
    └─────────────────────────────────────────────────────────────────────┘

    4. GCM (Galois/Counter Mode) ─ [권장: AEAD]
    ┌─────────────────────────────────────────────────────────────────────┐
    │  Nonce  Counter                                                    │
    │    │       │                                                       │
    │    ▼       ▼                                                       │
    │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                                  │
    │  │AES-K│ │AES-K│ │AES-K│ │AES-K│   CTR 모드 암호화                │
    │  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘   + GHASH 인증 태그              │
    │     │       │       │       │      병렬 처리 가능                  │
    │     ⊕       ⊕       ⊕       ⊕      무결성 + 기밀성 동시 보장      │
    │     │       │       │       │                                       │
    │  P1─┴─►C1 P2─┴─►C2 P3─┴─►C3 P4─┴─►C4                               │
    │                                                                     │
    │  ┌──────────────────────────────────────┐                         │
    │  │  GHASH (Galois 필드 상 해시)          │                         │
    │  │  Tag = GHASH(AAD, C1||C2||C3||C4)    │                         │
    │  └──────────────────────────────────────┘                         │
    └─────────────────────────────────────────────────────────────────────┘
```

#### 4. Python 구현: AES 암호화 (개념적)

```python
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum
import os

class AESKeySize(Enum):
    """AES 키 크기"""
    AES_128 = 16  # 128비트 = 16바이트
    AES_192 = 24  # 192비트 = 24바이트
    AES_256 = 32  # 256비트 = 32바이트

# AES S-Box (미리 계산된 치환 테이블)
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

# 라운드 상수
RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

class AES:
    """AES 암호화 클래스 (개념적 구현)"""

    def __init__(self, key: bytes):
        """초기화"""
        self.key = key
        self.key_size = len(key)

        # 키 크기에 따른 라운드 수 결정
        if self.key_size == 16:
            self.rounds = 10
        elif self.key_size == 24:
            self.rounds = 12
        elif self.key_size == 32:
            self.rounds = 14
        else:
            raise ValueError("Invalid key size")

        # 키 확장
        self.round_keys = self._key_expansion(key)

    def _key_expansion(self, key: bytes) -> List[List[int]]:
        """키 확장 (Key Schedule)"""
        Nk = self.key_size // 4  # 키의 32비트 워드 수
        Nb = 4  # 블록의 32비트 워드 수 (항상 4)
        Nr = self.rounds

        # 확장된 키 배열
        w = []

        # 초기 키 복사
        for i in range(Nk):
            w.append(list(key[4*i:4*i+4]))

        # 확장
        for i in range(Nk, Nb * (Nr + 1)):
            temp = w[i - 1][:]

            if i % Nk == 0:
                # RotWord
                temp = temp[1:] + temp[:1]
                # SubWord
                temp = [S_BOX[b] for b in temp]
                # XOR with Rcon
                temp[0] ^= RCON[i // Nk]
            elif Nk > 6 and i % Nk == 4:
                # AES-256 추가 SubWord
                temp = [S_BOX[b] for b in temp]

            w.append([w[i - Nk][j] ^ temp[j] for j in range(4)])

        return w

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
        """GF(2^8)에서 x 곱셈"""
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
        d = [self._xtime(self._xtime(self._xtime(x))) for x in a]

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
        """바이트 → 상태 행렬"""
        return [[block[r + 4*c] for c in range(4)] for r in range(4)]

    def _state_to_bytes(self, state: List[List[int]]) -> bytes:
        """상태 행렬 → 바이트"""
        return bytes([state[r][c] for c in range(4) for r in range(4)])

    def encrypt_block(self, plaintext: bytes) -> bytes:
        """단일 블록 암호화"""
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
        """단일 블록 복호화"""
        if len(ciphertext) != 16:
            raise ValueError("Block must be 16 bytes")

        state = self._bytes_to_state(ciphertext)

        # Initial Round (역순)
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
    """AES-CBC 모드"""

    def __init__(self, key: bytes):
        self.aes = AES(key)

    def encrypt(self, plaintext: bytes, iv: bytes) -> bytes:
        """CBC 암호화"""
        # PKCS7 패딩
        pad_len = 16 - (len(plaintext) % 16)
        padded = plaintext + bytes([pad_len] * pad_len)

        ciphertext = b""
        prev = iv

        for i in range(0, len(padded), 16):
            block = padded[i:i+16]
            # XOR with previous
            xored = bytes([block[j] ^ prev[j] for j in range(16)])
            # Encrypt
            encrypted = self.aes.encrypt_block(xored)
            ciphertext += encrypted
            prev = encrypted

        return ciphertext

    def decrypt(self, ciphertext: bytes, iv: bytes) -> bytes:
        """CBC 복호화"""
        plaintext = b""
        prev = iv

        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            # Decrypt
            decrypted = self.aes.decrypt_block(block)
            # XOR with previous
            xored = bytes([decrypted[j] ^ prev[j] for j in range(16)])
            plaintext += xored
            prev = block

        # PKCS7 언패딩
        pad_len = plaintext[-1]
        return plaintext[:-pad_len]


# 사용 예시
if __name__ == "__main__":
    # 키 생성
    key_256 = os.urandom(32)

    # AES 인스턴스 생성
    aes = AES(key_256)
    print(f"AES-256 초기화 완료")
    print(f"라운드 수: {aes.rounds}")
    print(f"라운드 키 수: {len(aes.round_keys)}")

    # 단일 블록 암호화 테스트
    plaintext = b"Hello World!!!!!"  # 16바이트
    ciphertext = aes.encrypt_block(plaintext)
    decrypted = aes.decrypt_block(ciphertext)

    print(f"\n단일 블록 테스트:")
    print(f"평문: {plaintext}")
    print(f"암호문: {ciphertext.hex()}")
    print(f"복호문: {decrypted}")
    print(f"일치: {plaintext == decrypted}")

    # CBC 모드 테스트
    aes_cbc = AES_CBC(key_256)
    iv = os.urandom(16)
    message = b"This is a longer message for AES-CBC encryption test!"

    encrypted = aes_cbc.encrypt(message, iv)
    decrypted = aes_cbc.decrypt(encrypted, iv)

    print(f"\nCBC 모드 테스트:")
    print(f"평문: {message}")
    print(f"암호문 길이: {len(encrypted)} bytes")
    print(f"복호문: {decrypted}")
    print(f"일치: {message == decrypted}")
```

#### 5. AES 성능 및 보안 특성

| 특성 | AES-128 | AES-192 | AES-256 |
|:---|:---|:---|:---|
| **라운드 수** | 10 | 12 | 14 |
| **키 스케줄링** | 44워드 | 52워드 | 60워드 |
| **보안 비트** | 128 | 192 | 256 |
| **전수 조사** | 2^128 | 2^192 | 2^256 |
| **최적 공격** | 2^126.1 (이론) | 2^189.7 (이론) | 2^254.4 (이론) |
| **소프트웨어** | ~20 cycle/block | ~25 cycle/block | ~30 cycle/block |
| **AES-NI** | ~3 cycle/block | ~4 cycle/block | ~5 cycle/block |

---

### III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. AES vs 다른 대칭키 알고리즘

| 알고리즘 | 키 길이 | 블록 크기 | 라운드 | 보안 | 속도 |
|:---|:---|:---|:---|:---|:---|
| **AES-256** | 256비트 | 128비트 | 14 | 높음 | 빠름 |
| **ChaCha20** | 256비트 | 스트림 | 20 | 높음 | 매우 빠름 |
| **3DES** | 168비트 | 64비트 | 48 | 중간 | 느림 |
| **Camellia-256** | 256비트 | 128비트 | 24 | 높음 | 빠름 |
| **SM4** | 128비트 | 128비트 | 32 | 높음 | 빠름 |

#### 2. AES 운영 모드 비교

| 모드 | 병렬화 | 인증 | 패딩 | 오류 전파 | 권장 용도 |
|:---|:---|:---|:---|:---|:---|
| **ECB** | 가능 | 없음 | 필요 | 없음 | 사용 금지 |
| **CBC** | 암호화만 | 없음 | 필요 | 2블록 | 파일 암호화 |
| **CTR** | 가능 | 없음 | 불필요 | 없음 | 스트리밍 |
| **GCM** | 가능 | 있음(AEAD) | 불필요 | 없음 | 네트워크 |
| **XTS** | 가능 | 없음 | 불필요 | 없음 | 디스크 |

#### 3. 과목 융합 관점 분석
- **네트워크 보안**: TLS 1.3의 필수 암호 스위트 (AES-GCM)
- **데이터베이스**: TDE(Transparent Data Encryption), 컬럼 암호화
- **시스템 보안**: 디스크 암호화(BitLocker, FileVault), 메모리 암호화
- **클라우드**: S3 SSE, EBS 암호화, KMS 연동
- **애플리케이션**: JWT 암호화, 세션 암호화, 쿠키 암호화

---

### IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 대용량 파일 암호화 시스템**
- 요구사항: 10GB 이상 파일 암호화, 랜덤 접근 필요
- 판단: AES-256-XTS 또는 AES-256-CTR
- 이유: XTS는 디스크 암호화에 최적, CTR은 랜덤 접근 가능

**시나리오 2: 실시간 스트리밍 데이터 암호화**
- 요구사항: 저지연, 패킷 손실 허용
- 판단: AES-GCM 또는 ChaCha20-Poly1305
- 이유: AEAD로 무결성+기밀성, 병렬 처리 가능

**시나리오 3: IoT 디바이스 데이터 암호화**
- 요구사항: 저전력, 하드웨어 가속 없음
- 판단: AES-128-CTR 또는 ChaCha20
- 이유: AES-NI 없으면 ChaCha20이 더 빠를 수 있음

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] 키 길이 선택 (128/192/256비트)
- [ ] 운영 모드 선택 (GCM 권장)
- [ ] IV/Nonce 생성 방식 (암호학적 난수)
- [ ] 키 관리 체계 (KMS, HSM)
- [ ] 하드웨어 가속 (AES-NI) 활용
- [ ] 패딩 oracle 공격 방지

#### 3. 안티패턴 (Anti-patterns)
- **ECB 모드 사용**: 패턴 노출 위험
- **고정 IV/Nonce**: 동일 키+IV 재사용 치명적
- **키 하드코딩**: 소스코드에 키 포함
- **약한 키 생성**: 예측 가능한 난수 사용

---

### V. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | 내용 | 측정 방법 |
|:---|:---|:---|
| 기밀성 보장 | 무단 접근 시 데이터 보호 | 암호화율 100% |
| 성능 | AES-NI 활용 시 초고속 처리 | 10+ Gbps |
| 상호 운용성 | 전 세계 표준 호환 | 표준 준수율 |
| 미래 보안 | 20년+ 안전성 예상 | 양자 내성 (AES-256) |

#### 2. 미래 전망 및 진화 방향
- **AES-NI 확장**: 더 많은 CPU에 하드웨어 가속 내장
- **AES-GCM-SIV**: nonce-reuse 안전한 변종
- **양자 내성**: AES-256은 양자 공격에도 안전
- **하이브리드 암호**: PQC와 결합한 미래 대비

#### 3. 참고 표준/가이드
- **FIPS 197**: AES 공식 표준
- **NIST SP 800-38A**: 블록 암호 운영 모드
- **NIST SP 800-38D**: GCM 모드 표준
- **RFC 5116**: AEAD 인터페이스

---

### 관련 개념 맵 (Knowledge Graph)
- [대칭키 암호](@/studynotes/09_security/02_crypto/symmetric_encryption.md) : AES의 상위 개념
- [운영 모드](@/studynotes/09_security/02_crypto/symmetric_encryption.md) : ECB, CBC, GCM 등
- [GCM](@/studynotes/09_security/02_crypto/symmetric_encryption.md) : 인증 암호화 모드
- [HSM](@/studynotes/09_security/02_crypto/encryption_algorithms.md) : 키 보호 하드웨어
- [TLS](@/studynotes/09_security/03_network/network_security_systems.md) : AES를 사용하는 프로토콜

---

### 어린이를 위한 3줄 비유 설명
1. **비밀 상자**: 보석을 상자에 넣고 잠그는 것처럼, 데이터를 암호화로 잠가요.
2. **특수 열쇠**: 128/192/256비트 열쇠가 있는데, 숫자가 클수록 더 안전해요.
3. **섞기 놀이**: 데이터를 10~14번 섞어서 아무도 원래 모양을 알 수 없게 해요.
