+++
title = "SHA-2 / SHA-3 해시 함수"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# SHA-2 / SHA-3 해시 함수

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SHA-2(SHA-224/256/384/512)는 Merkle-Damgård 구조의 반복형 해시 함수이며, SHA-3(Keccak)은 스펀지 구조를 기반으로 한 경쟁적 표준으로, 충돌 저항성과 역상 저항성을 제공합니다.
> 2. **가치**: 디지털 서명, 메시지 인증, 블록체인, 비밀번호 저장 등 모든 암호학적 응용의 기반이며, 데이터 무결성 검증의 핵심 도구입니다.
> 3. **융합**: SHA-2는 TLS, PGP, Bitcoin에 필수적이고, SHA-3은 경량 구현과 하드웨어 가속에 유리하며, 두 표준은 상호 보완적으로 공존합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**해시 함수(Hash Function)**는 임의 길이의 입력을 고정 길이의 출력(해시값, 다이제스트)으로 변환하는 단방향 함수입니다. **SHA-2**와 **SHA-3**은 NIST가 표준화한 암호학적 해시 함수 패밀리입니다.

```
해시 함수의 보안 속성:
1. 역상 저항성 (Pre-image Resistance)
   H(m) = h가 주어졌을 때, m을 찾기 어려움 (일방향성)

2. 제2역상 저항성 (Second Pre-image Resistance)
   m이 주어졌을 때, H(m') = H(m)인 다른 m'을 찾기 어려움

3. 충돌 저항성 (Collision Resistance)
   H(m1) = H(m2)인 서로 다른 m1, m2를 찾기 어려움
```

#### 2. 비유를 통한 이해
해시 함수는 **'지문 채취기'**에 비유할 수 있습니다.
- **입력**: 사람 (어른, 아이, 키 큰 사람, 작은 사람 모두 가능)
- **출력**: 지문 (모두 동일한 크기의 지문 카드)
- **역상 저항성**: 지문만 보고 어떤 사람인지 알 수 없음
- **충돌 저항성**: 두 사람이 같은 지문을 가질 확률은 거의 0

#### 3. 등장 배경 및 발전 과정
1. **1993년**: SHA-0 발표 (곧 결함 발견으로 철회)
2. **1995년**: SHA-1 발표 (160비트, 2017년 SHAttered 공격으로 붕괴)
3. **2001년**: SHA-2 패밀리 발표 (224/256/384/512비트)
4. **2007년**: SHA-3 공모 시작 (NIST Hash Competition)
5. **2012년**: Keccak이 SHA-3로 선정
6. **2015년**: FIPS 202로 SHA-3 표준화
7. **현재**: SHA-2 주류, SHA-3 보완적 사용

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. SHA 패밀리 구성 비교

| 알고리즘 | 출력 길이 | 블록 크기 | 구조 | 라운드 | 보안 비트 |
|:---|:---:|:---:|:---|:---:|:---:|
| **SHA-224** | 224 | 512 | Merkle-Damgård | 64 | 112 |
| **SHA-256** | 256 | 512 | Merkle-Damgård | 64 | 128 |
| **SHA-384** | 384 | 1024 | Merkle-Damgård | 80 | 192 |
| **SHA-512** | 512 | 1024 | Merkle-Damgård | 80 | 256 |
| **SHA-3-224** | 224 | 1152 | Sponge | 24 | 112 |
| **SHA-3-256** | 256 | 1088 | Sponge | 24 | 128 |
| **SHA-3-384** | 384 | 832 | Sponge | 24 | 192 |
| **SHA-3-512** | 512 | 576 | Sponge | 24 | 256 |

#### 2. SHA-2 vs SHA-3 구조 다이어그램

```
=== SHA-2 (Merkle-Damgård Construction) ===

┌────────────────────────────────────────────────────────────┐
│                    Message Padding                          │
│  M || 1 || 0...0 || length(M) as 64/128-bit integer        │
└────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│                    Message Block Processing                 │
│                                                            │
│   ┌──────────┐    ┌──────────┐         ┌──────────┐       │
│   │  Block 1 │    │  Block 2 │   ...   │  Block N │       │
│   └────┬─────┘    └────┬─────┘         └────┬─────┘       │
│        │               │                    │              │
│        ▼               ▼                    ▼              │
│   ┌──────────┐    ┌──────────┐         ┌──────────┐       │
│   │   IV     │───►│ Compress │───►...─►│ Compress │───► H │
│   └──────────┘    └──────────┘         └──────────┘       │
│                                                            │
│   Compress Function (64 or 80 rounds):                    │
│   - Message Schedule (W_t)                                 │
│   - 8 Working Variables (a,b,c,d,e,f,g,h)                  │
│   - Round Constants (K_t)                                  │
│   - Ch, Maj, Σ0, Σ1 functions                              │
└────────────────────────────────────────────────────────────┘

문제점: 길이 확장 공격(Length Extension Attack) 취약
→ HMAC 또는 SHA-3 사용으로 해결

===========================================

=== SHA-3 (Keccak Sponge Construction) ===

┌────────────────────────────────────────────────────────────┐
│                     Sponge Construction                     │
│                                                            │
│   State: 5×5×64 = 1600 bits (b)                           │
│                                                            │
│   ┌─────────────────────────────────────────────────────┐  │
│   │              1600-bit State (5×5 lanes)             │  │
│   │  ┌───┬───┬───┬───┬───┐                             │  │
│   │  │   │   │   │   │   │  ← r bits (rate)            │  │
│   │  ├───┼───┼───┼───┼───┤    (absorbed/xor'd)          │  │
│   │  │   │   │   │   │   │                             │  │
│   │  ├───┼───┼───┼───┼───┤                             │  │
│   │  │   │   │   │   │   │                             │  │
│   │  ├───┼───┼───┼───┼───┤                             │  │
│   │  │   │   │   │   │   │  ← c bits (capacity)         │  │
│   │  └───┴───┴───┴───┴───┘    (security margin)          │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                            │
│   Absorbing Phase:                                        │
│   ┌────────┐    ┌────────┐         ┌────────┐            │
│   │ P1⊕S   │───►│ P2⊕S   │───►...─►│ Pn⊕S   │            │
│   └────────┘    └────────┘         └────────┘            │
│       │             │                  │                  │
│       ▼             ▼                  ▼                  │
│   ┌────────────────────────────────────────────────────┐  │
│   │           Keccak-f[1600] Permutation                │  │
│   │                                                     │  │
│   │   24 rounds of:                                     │  │
│   │   θ (theta) - column parity diffusion              │  │
│   │   ρ (rho)   - lane rotation                        │  │
│   │   π (pi)    - lane permutation                     │  │
│   │   χ (chi)   - non-linear layer (only non-linear!)  │  │
│   │   ι (iota)  - round constant addition              │  │
│   └────────────────────────────────────────────────────┘  │
│                                                            │
│   Squeezing Phase:                                        │
│   ┌────────┐    ┌────────┐                               │
│   │ Output │◄───│ Keccak │◄── Z = S[0..r-1]             │
│   │   Z    │    │   -f   │                               │
│   └────────┘    └────────┘                               │
│                                                            │
└────────────────────────────────────────────────────────────┘

장점: 길이 확장 공격 면역, 가변 출력, XOF 지원
```

#### 3. 심층 동작 원리: SHA-256 구현

```python
import struct
from typing import List

class SHA256:
    """
    SHA-256 구현 (FIPS 180-4)

    특징:
    - 256비트 출력
    - 512비트 블록 처리
    - 64 라운드
    - Merkle-Damgård 구조
    """

    # 초기 해시값 (소수의 제곱근의 소수부)
    H0 = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

    # 라운드 상수 (소수의 세제곱근의 소수부)
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    def __init__(self):
        self.h = self.H0.copy()
        self.message_length = 0
        self.buffer = b''

    @staticmethod
    def _rotr(x: int, n: int) -> int:
        """32비트 오른쪽 회전"""
        return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

    @staticmethod
    def _shr(x: int, n: int) -> int:
        """32비트 오른쪽 시프트"""
        return x >> n

    @staticmethod
    def _ch(x: int, y: int, z: int) -> int:
        """Choice: (x AND y) XOR (NOT x AND z)"""
        return (x & y) ^ (~x & z) & 0xFFFFFFFF

    @staticmethod
    def _maj(x: int, y: int, z: int) -> int:
        """Majority: (x AND y) XOR (x AND z) XOR (y AND z)"""
        return (x & y) ^ (x & z) ^ (y & z) & 0xFFFFFFFF

    def _sigma0(self, x: int) -> int:
        """Σ0: ROTR²(x) XOR ROTR¹³(x) XOR ROTR²²(x)"""
        return self._rotr(x, 2) ^ self._rotr(x, 13) ^ self._rotr(x, 22)

    def _sigma1(self, x: int) -> int:
        """Σ1: ROTR⁶(x) XOR ROTR¹¹(x) XOR ROTR²⁵(x)"""
        return self._rotr(x, 6) ^ self._rotr(x, 11) ^ self._rotr(x, 25)

    def _gamma0(self, x: int) -> int:
        """σ0: ROTR⁷(x) XOR ROTR¹⁸(x) XOR SHR³(x)"""
        return self._rotr(x, 7) ^ self._rotr(x, 18) ^ self._shr(x, 3)

    def _gamma1(self, int) -> int:
        """σ1: ROTR¹⁷(x) XOR ROTR¹⁹(x) XOR SHR¹⁰(x)"""
        return self._rotr(x, 17) ^ self._rotr(x, 19) ^ self._shr(x, 10)

    def _pad_message(self, message: bytes) -> bytes:
        """
        메시지 패딩 (MD-strengthening)
        M || 1 || 0...0 || length(M) as 64-bit big-endian
        """
        ml = len(message) * 8  # 비트 단위 길이

        # 1 비트 추가 + 0 패딩
        message += b'\x80'

        # 448 mod 512가 될 때까지 0 추가 (64비트 길이 필드 공간 확보)
        while (len(message) % 64) != 56:
            message += b'\x00'

        # 64비트 길이 필드 추가
        message += struct.pack('>Q', ml)

        return message

    def _process_block(self, block: bytes):
        """512비트 블록 처리 (64 라운드)"""
        # 메시지 스케줄 W 생성
        W = list(struct.unpack('>16I', block))

        # W[16..63] 확장
        for i in range(16, 64):
            W.append(
                (self._gamma1(W[i-2]) + W[i-7] +
                 self._gamma0(W[i-15]) + W[i-16]) & 0xFFFFFFFF
            )

        # 작업 변수 초기화
        a, b, c, d, e, f, g, h = self.h

        # 64 라운드
        for i in range(64):
            T1 = (h + self._sigma1(e) + self._ch(e, f, g) +
                  self.K[i] + W[i]) & 0xFFFFFFFF
            T2 = (self._sigma0(a) + self._maj(a, b, c)) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + T1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (T1 + T2) & 0xFFFFFFFF

        # 해시값 갱신
        self.h[0] = (self.h[0] + a) & 0xFFFFFFFF
        self.h[1] = (self.h[1] + b) & 0xFFFFFFFF
        self.h[2] = (self.h[2] + c) & 0xFFFFFFFF
        self.h[3] = (self.h[3] + d) & 0xFFFFFFFF
        self.h[4] = (self.h[4] + e) & 0xFFFFFFFF
        self.h[5] = (self.h[5] + f) & 0xFFFFFFFF
        self.h[6] = (self.h[6] + g) & 0xFFFFFFFF
        self.h[7] = (self.h[7] + h) & 0xFFFFFFFF

    def update(self, message: bytes):
        """스트리밍 업데이트"""
        self.message_length += len(message)
        self.buffer += message

        # 512비트(64바이트) 블록 단위로 처리
        while len(self.buffer) >= 64:
            self._process_block(self.buffer[:64])
            self.buffer = self.buffer[64:]

    def digest(self) -> bytes:
        """최종 해시값 반환"""
        # 남은 버퍼 패딩
        padded = self._pad_message(self.buffer)

        # 모든 블록 처리
        for i in range(0, len(padded), 64):
            self._process_block(padded[i:i+64])

        # 256비트 해시값 생성
        return struct.pack('>8I', *self.h)

    def hexdigest(self) -> str:
        """16진수 문자열로 반환"""
        return self.digest().hex()

    @classmethod
    def hash(cls, message: bytes) -> str:
        """편의 메서드: 한 번에 해시 계산"""
        sha = cls()
        sha.update(message)
        return sha.hexdigest()


class SHA3_256:
    """
    SHA3-256 (Keccak) 구현 개요

    Sponge 구조:
    - State: 5×5×64 = 1600 bits
    - Rate (r): 1088 bits (for SHA3-256)
    - Capacity (c): 512 bits
    - Security: 256 bits (collision resistance)
    """

    def __init__(self):
        self.state = [[0] * 5 for _ in range(5)]  # 5×5 lanes, each 64 bits
        self.rate = 1088 // 64  # 17 lanes
        self.capacity = 512
        self.buffer = b''

    def _keccak_f(self):
        """
        Keccak-f[1600] 순열 (24 라운드)
        θ, ρ, π, χ, ι 단계
        """
        # 실제 구현은 매우 복잡함
        # 여기서는 개념적 설명
        RC = [  # 라운드 상수
            0x0000000000000001, 0x0000000000008082, 0x800000000000808a,
            0x8000000080008000, 0x000000000000808b, 0x0000000080000001,
            # ... 24개
        ]

        for round_idx in range(24):
            # θ: Column parity
            # ρ: Lane rotation
            # π: Lane permutation
            # χ: Non-linear (only non-linear operation!)
            # ι: Round constant XOR
            pass

    def absorb(self, message: bytes):
        """Absorbing phase"""
        # 패딩: 10*1
        message = message + b'\x06' + b'\x00' * ((136 - len(message) - 1) % 136) + b'\x80'

        for block in self._split_blocks(message, 136):
            # XOR with rate portion of state
            for i, byte in enumerate(block):
                self.state[i // 8 // 5][i // 8 % 5] ^= byte << ((i % 8) * 8)

            # Apply Keccak-f
            self._keccak_f()

    def squeeze(self, length: int = 32) -> bytes:
        """Squeezing phase"""
        output = b''
        while len(output) < length:
            # Extract rate portion
            block = b''
            for y in range(5):
                for x in range(5):
                    for b in range(8):
                        block += bytes([(self.state[y][x] >> (b * 8)) & 0xff])
            output += block[:136]

            if len(output) < length:
                self._keccak_f()

        return output[:length]

    @staticmethod
    def _split_blocks(data: bytes, block_size: int) -> list:
        return [data[i:i+block_size] for i in range(0, len(data), block_size)]


# 사용 예시
def demo_hash_functions():
    """해시 함수 데모"""

    test_messages = [
        b"",
        b"Hello, World!",
        b"The quick brown fox jumps over the lazy dog",
        b"a" * 1000000  # 1MB 테스트
    ]

    print("=" * 60)
    print("SHA-256 vs SHA3-256 비교")
    print("=" * 60)

    for msg in test_messages:
        sha256_hash = SHA256.hash(msg)

        # 실제로는 hashlib 사용
        import hashlib
        sha3_hash = hashlib.sha3_256(msg).hexdigest()

        print(f"\n입력: {msg[:50]}{'...' if len(msg) > 50 else ''}")
        print(f"SHA-256:   {sha256_hash}")
        print(f"SHA3-256:  {sha3_hash}")


# 충돌 저항성 시연 (생일 공격)
def birthday_attack_analysis():
    """생일 역설 기반 충돌 분석"""
    import math

    print("\n" + "=" * 60)
    print("충돌 저항성 분석 (생일 역설)")
    print("=" * 60)

    algorithms = [
        ("SHA-256", 256),
        ("SHA-384", 384),
        ("SHA-512", 512),
        ("SHA3-256", 256),
        ("SHA3-512", 512)
    ]

    for name, bits in algorithms:
        # 충돌 찾을 확률 50%에 필요한 시도 횟수
        # ≈ sqrt(2^bits * ln(2)) ≈ 1.177 * 2^(bits/2)
        attempts_50 = 1.177 * (2 ** (bits / 2))

        # 초당 10^12 해시 계산 가능하다고 가정
        hash_rate = 1e12
        time_years = attempts_50 / hash_rate / (365.25 * 24 * 3600)

        print(f"\n{name}:")
        print(f"  출력 비트: {bits}")
        print(f"  충돌 찾기 (50%): 2^{bits/2:.0f} ≈ {attempts_50:.2e} 회")
        print(f"  예상 시간 (10^12 H/s): {time_years:.2e} 년")


if __name__ == "__main__":
    demo_hash_functions()
    birthday_attack_analysis()
```

#### 4. SHA-2 vs SHA-3 성능 및 보안 비교

| 특성 | SHA-2 (256) | SHA-3 (256) | 비고 |
|:---|:---|:---|:---|
| **구조** | Merkle-Damgård | Sponge | 근본적 차이 |
| **충돌 공격** | 2^128 | 2^128 | 동등 |
| **역상 공격** | 2^256 | 2^256 | 동등 |
| **길이 확장** | 취약 | 안전 | SHA-3 장점 |
| **소프트웨어** | 빠름 | 중간 | SHA-2 우세 |
| **하드웨어** | 중간 | 빠름 | SHA-3 우세 |
| **XOF 지원** | 없음 | SHAKE | SHA-3 장점 |

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 용도별 해시 함수 선택 가이드

| 용도 | 추천 | 이유 | 대안 |
|:---|:---|:---|:---|
| **디지털 서명** | SHA-256 | 검증됨, 빠름 | SHA-384 |
| **TLS/SSL** | SHA-256 | 표준 | SHA-384 |
| **블록체인** | SHA-256 | Bitcoin 표준 | Keccak-256 |
| **비밀번호 저장** | Argon2id | 전용 KDF | bcrypt |
| **파일 무결성** | SHA-256 | 빠름, 충분 | SHA3-256 |
| **XOF 필요시** | SHAKE256 | 가변 출력 | BLAKE3 |
| **경량 IoT** | SHA3-256 | 하드웨어 효율 | SHA-256 |

#### 2. 해시 함수 공격 연혁

| 연도 | 공격 | 대상 | 영향 |
|:---|:---|:---|:---|
| 2004 | Wang's attack | MD5, SHA-0 | MD5 붕괴 |
| 2005 | Collision attack | SHA-1 | 이론적 위협 |
| 2017 | SHAttered | SHA-1 | 실제 충돌 |
| 2019 | SHA-1 chosen-prefix | SHA-1 | PGP 영향 |
| 2020 | Savings attack | SHA-256 | 이론적 (4.3비트 절약) |

#### 3. 과목 융합 관점 분석

**데이터베이스와 융합**
- 인덱스: 해시 인덱스 (Equality 검색)
- 파티셔닝: 해시 기반 분산
- Change Data Capture: 해시 기반 변경 감지

**블록체인과 융합**
- Bitcoin: SHA-256 (이중 해시)
- Ethereum: Keccak-256
- Merkle Tree: 트랜잭션 무결성

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 레거시 MD5 → SHA-256 마이그레이션**
- 상황: 기존 시스템이 MD5로 파일 무결성 검증
- 판단: SHA-256으로 전환 필요
- 전략:
  1. 새 파일: SHA-256만 저장
  2. 기존 파일: MD5 + SHA-256 병행 저장
  3. 점진적 마이그레이션

**시나리오 2: 길이 확장 공격 방지**
- 상황: H(secret || message) 패턴 사용 중
- 판단: SHA-256 취약 → HMAC 또는 SHA-3
- 해결: HMAC-SHA256 사용

**시나리오 3: 대용량 파일 해시**
- 상황: 수 GB 파일의 해시 계산
- 판단: 스트리밍 방식 필요
- 구현: 청크 단위 업데이트

#### 2. 도입 시 고려사항 (체크리스트)

**기술적 체크리스트**
- [ ] 출력 길이 요구사항 (128/256/512비트)
- [ ] 성능 요구사항 (처리량)
- [ ] 길이 확장 공격 방지 필요 여부
- [ ] XOF (가변 출력) 필요 여부

**운영 체크리스트**
- [ ] 라이브러리 선택 (OpenSSL, cryptography)
- [ ] 하드웨어 가산 활용 (SHA-NI)
- [ ] 타이밍 공격 방지 (constant-time)

#### 3. 안티패턴 (Anti-patterns)

```
취약한 구현 (금지!)

1. MD5/SHA-1 사용
   ❌ hash = hashlib.md5(data).hexdigest()
   → 충돌 공격 취약, 사용 금지

2. 길이 확장 취약 패턴
   ❌ mac = sha256(secret + message)
   → H(secret || msg) → H(secret || msg || extension) 계산 가능

3. 비밀번호 평문 해시
   ❌ stored = sha256(password)
   → 레인보우 테이블 공격 취약

4. 사용자 입력 직접 해시
   ❌ token = sha256(user_input)
   → 긴 입력으로 DoS 가능

올바른 구현:

1. SHA-256/384/512 사용
   ✓ hash = hashlib.sha256(data).hexdigest()

2. HMAC 또는 SHA-3
   ✓ mac = hmac.new(secret, message, 'sha256').hexdigest()
   ✓ hash = hashlib.sha3_256(message).hexdigest()

3. 비밀번호는 전용 KDF
   ✓ stored = argon2id.hash(password)

4. 입력 길이 제한
   ✓ if len(user_input) > MAX_LENGTH: raise ValueError()
   ✓ hash = hashlib.sha256(user_input).hexdigest()
```

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 | 항목 | 수치/내용 |
|:---|:---|:---|
| **무결성** | 충돌 방지 | 2^128 노력 필요 (SHA-256) |
| **성능** | 처리량 | SHA-256: ~500 MB/s (SW), ~3 GB/s (HW) |
| **표준** | 호환성 | FIPS 180-4, FIPS 202 준수 |
| **보안** | 내성 | 2030년까지 안전 예상 |

#### 2. 미래 전망 및 진화 방향

```
해시 함수 진화
├── SHA-3 확대
│   ├── XOF (SHAKE128/256) 활용 증가
│   └── 경량 구현 (KMAC, TupleHash)
├── BLAKE3
│   ├── 병렬화 친화적
│   └── 10x faster than SHA-256
└── 양자 시대
    └── 충돌 내성: 2^128 → 2^64 (Grover)
    → SHA-384/512 권장
```

#### 3. 참고 표준/가이드

| 표준 | 내용 |
|:---|:---|
| **FIPS 180-4** | SHA-2 패밀리 표준 |
| **FIPS 202** | SHA-3 표준 (Keccak) |
| **NIST SP 800-185** | SHA-3 파생 함수 (KMAC 등) |
| **RFC 6234** | SHA 표준 알고리즘 |
| **ISO/IEC 10118-3** | 전용 해시 함수 |

---

### 관련 개념 맵 (Knowledge Graph)
- [HMAC](@/studynotes/09_security/02_crypto/mac_hmac.md) : 해시 기반 메시지 인증 코드
- [디지털 서명](@/studynotes/09_security/02_crypto/digital_signature.md) : 해시를 사용한 서명
- [KDF](@/studynotes/09_security/02_crypto/kdf_password_hashing.md) : 키 유도 함수
- [블록체인](@/studynotes/09_security/06_advanced/blockchain_security.md) : 해시 기반 분산 원장
- [Merkle Tree](@/studynotes/09_security/06_advanced/merkle_tree.md) : 해시 트리 구조

---

### 어린이를 위한 3줄 비유 설명
1. **지문 채취**: 해시 함수는 모든 사람에게서 똑같은 크기의 지문 카드를 만드는 기계예요. 아무리 큰 파일이나 작은 파일도 같은 크기의 지문이 나와요.
2. **되돌릴 수 없어요**: 지문만 보고 어떤 사람인지 알 수 없는 것처럼, 해시값만 보고 원래 내용을 알 수 없어요. 이게 보안의 핵심이에요!
3. **하나라도 다르면**: 원래 내용이 한 글자만 바뀌어도 해시값은 완전히 달라져요. 문서가 조금이라도 변했는지 바로 알 수 있어요.
