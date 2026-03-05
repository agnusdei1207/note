+++
title = "해시 함수 (Hash Function)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# 해시 함수 (Hash Function)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 해시 함수는 임의 길이 입력을 고정 길이 출력(해시값/다이제스트)으로 매핑하는 단방향 함수로, 암호학적 해시는 충돌 저항성, 역상 저항성, 제2역상 저항성을 만족합니다.
> 2. **가치**: 데이터 무결성 검증, 패스워드 저장, 디지털 서명, 블록체인, 파일 식별 등 보안의 근간이 되며, 취약한 해시(MD5, SHA-1)는 사용이 금지되었습니다.
> 3. **융합**: SHA-2(SHA-256, SHA-512), SHA-3(Keccak), BLAKE2/3가 현대 표준이며, HMAC, KDF, Merkle Tree 등 다양한 보안 구성요소의 기반이 됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**암호학적 해시 함수(Cryptographic Hash Function)**는 다음 세 가지 보안 속성을 만족하는 함수 H입니다:

| 속성 | 정의 | 수학적 표현 |
|:---|:---|:---|
| **역상 저항성 (Pre-image Resistance)** | 해시값으로부터 원문을 찾기 어려움 | H(x) = h일 때, x 찾기 어려움 |
| **제2역상 저항성 (Second Pre-image Resistance)** | 원문과 같은 해시를 갖는 다른 원문 찾기 어려움 | x가 주어질 때, H(y) = H(x)인 y≠x 찾기 어려움 |
| **충돌 저항성 (Collision Resistance)** | 같은 해시를 갖는 두 원문 찾기 어려움 | H(x) = H(y)인 x≠y 찾기 어려움 |

#### 2. 비유를 통한 이해
해시 함수는 **'지문(Fingerprint)'**에 비유할 수 있습니다:

```
[사람] → [지문 채취] → [지문 패턴]
[파일] → [해시 함수] → [해시값]

특징:
- 모든 사람이 고유한 지문을 가짐 (충돌 저항성)
- 지문으로 사람을 유추할 수 없음 (역상 저항성)
- 같은 사람은 같은 지문 (결정론적)
- 작은 지문으로 사람 식별 (고정 길이)
```

#### 3. 등장 배경 및 발전 과정

| 연도 | 알고리즘 | 출력 길이 | 상태 |
|:---|:---|:---|:---|
| **1990** | MD4 | 128비트 | 깨짐 |
| **1992** | MD5 | 128비트 | 깨짐 (2012) |
| **1993** | SHA-0 | 160비트 | 깨짐 |
| **1995** | SHA-1 | 160비트 | 깨짐 (2017 SHAttered) |
| **2001** | SHA-2 | 224/256/384/512비트 | 안전 |
| **2015** | SHA-3 (Keccak) | 가변 | 안전 |
| **2012** | BLAKE2 | 256/512비트 | 안전 |
| **2020** | BLAKE3 | 256비트 (확장 가능) | 안전 |

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 해시 함수 구조 (Merkle-Damgard)

```text
                    [ Merkle-Damgard 구조 ]

              ┌─────────────────────────────────────┐
              │           메시지 M                   │
              └──────────────┬──────────────────────┘
                             │
                             ▼
              ┌─────────────────────────────────────┐
              │  메시지 패딩 (Padding)               │
              │  M || 1 || 00...0 || len(M)         │
              └──────────────┬──────────────────────┘
                             │
                             ▼
              ┌─────────────────────────────────────┐
              │  블록 분할: M1, M2, ..., Mn          │
              │  (각 블록 = 해시 함수 입력 크기)      │
              └──────────────┬──────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
    ┌───────┐           ┌───────┐           ┌───────┐
    │   IV  │           │  H1   │           │ Hn-1  │
    └───┬───┘           └───┬───┘           └───┬───┘
        │                   │                   │
        ▼                   ▼                   ▼
    ┌───────┐           ┌───────┐           ┌───────┐
    │  M1   │           │  M2   │           │  Mn   │
    └───┬───┘           └───┬───┘           └───┬───┘
        │                   │                   │
        ▼                   ▼                   ▼
    ┌───────┐           ┌───────┐           ┌───────┐
    │  f    │           │  f    │           │  f    │
    │(압축함수)│         │(압축함수)│         │(압축함수)│
    └───┬───┘           └───┬───┘           └───┬───┘
        │                   │                   │
        ▼                   ▼                   ▼
    ┌───────┐           ┌───────┐           ┌───────┐
    │  H1   │──────────►│  H2   │─── ... ──►│  Hn   │
    └───────┘           └───────┘           └───┬───┘
                                                │
                                                ▼
                                           [ 최종 해시 ]
```

#### 2. SHA-256 구조

```text
                    [ SHA-256 압축 함수 ]

입력: 512비트 블록 Wi, 256비트 체인 변수 Hi-1
출력: 256비트 체인 변수 Hi

1. 메시지 스케줄 준비 (64개 32비트 워드)
   W0..W15 = Mi (입력 블록)
   W16..W63 = σ1(Wi-2) + Wi-7 + σ0(Wi-15) + Wi-16

2. 64 라운드 수행
   초기화: a,b,c,d,e,f,g,h = Hi-1의 8개 워드

   for i = 0 to 63:
       T1 = h + Σ1(e) + Ch(e,f,g) + Ki + Wi
       T2 = Σ0(a) + Maj(a,b,c)
       h = g
       g = f
       f = e
       e = d + T1
       d = c
       c = b
       b = a
       a = T1 + T2

   Hi = (a||b||c||d||e||f||g||h) + Hi-1

3. 최종 해시 = Hn
```

#### 3. 해시 함수 보안 속성 비교

| 알고리즘 | 출력 | 역상 | 제2역상 | 충돌 | 상태 |
|:---|:---|:---|:---|:---|:---|
| MD5 | 128비트 | 깨짐 | 깨짐 | 깨짐 | 사용 금지 |
| SHA-1 | 160비트 | 이론적 | 이론적 | 깨짐 | 사용 금지 |
| SHA-256 | 256비트 | 안전 | 안전 | 안전 | 권장 |
| SHA-512 | 512비트 | 안전 | 안전 | 안전 | 권장 |
| SHA3-256 | 256비트 | 안전 | 안전 | 안전 | 권장 |
| BLAKE3 | 256비트 | 안전 | 안전 | 안전 | 권장 |

#### 4. 핵심 알고리즘 & 실무 코드

```python
import hashlib
import struct
from typing import Union

class SHA256:
    """SHA-256 해시 함수 구현 (교육용)"""

    # 초기 해시값 (처음 32비트 소수의 세제곱근 소수부)
    H0 = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

    # 라운드 상수 (처음 64비트 소수의 세제곱근 소수부)
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        # ... 나머지 56개 상수 생략
    ]

    @staticmethod
    def rotr(x: int, n: int) -> int:
        """오른쪽 회전 (32비트)"""
        return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

    @staticmethod
    def shr(x: int, n: int) -> int:
        """오른쪽 시프트"""
        return x >> n

    @staticmethod
    def ch(x: int, y: int, z: int) -> int:
        """Choose 함수"""
        return (x & y) ^ (~x & z)

    @staticmethod
    def maj(x: int, y: int, z: int) -> int:
        """Majority 함수"""
        return (x & y) ^ (x & z) ^ (y & z)

    @staticmethod
    def sigma0(x: int) -> int:
        """Σ0(x) = ROTR²(x) ⊕ ROTR¹³(x) ⊕ ROTR²²(x)"""
        return (SHA256.rotr(x, 2) ^ SHA256.rotr(x, 13) ^
                SHA256.rotr(x, 22))

    @staticmethod
    def sigma1(x: int) -> int:
        """Σ1(x) = ROTR⁶(x) ⊕ ROTR¹¹(x) ⊕ ROTR²⁵(x)"""
        return (SHA256.rotr(x, 6) ^ SHA256.rotr(x, 11) ^
                SHA256.rotr(x, 25))

    @staticmethod
    def gamma0(x: int) -> int:
        """σ0(x) = ROTR⁷(x) ⊕ ROTR¹⁸(x) ⊕ SHR³(x)"""
        return (SHA256.rotr(x, 7) ^ SHA256.rotr(x, 18) ^
                SHA256.shr(x, 3))

    @staticmethod
    def gamma1(x: int) -> int:
        """σ1(x) = ROTR¹⁷(x) ⊕ ROTR¹⁹(x) ⊇ SHR¹⁰(x)"""
        return (SHA256.rotr(x, 17) ^ SHA256.rotr(x, 19) ^
                SHA256.shr(x, 10))

    @classmethod
    def pad_message(cls, message: bytes) -> bytes:
        """메시지 패딩"""
        msg_len = len(message)
        bit_len = msg_len * 8

        # 1 비트 추가 + 0 패딩
        message += b'\x80'
        message += b'\x00' * ((55 - msg_len) % 64)

        # 길이 추가 (64비트 빅엔디안)
        message += struct.pack('>Q', bit_len)

        return message

    @classmethod
    def hash(cls, message: Union[str, bytes]) -> str:
        """
        SHA-256 해시 계산

        Args:
            message: 입력 메시지 (문자열 또는 바이트)

        Returns:
            64자리 16진수 해시값
        """
        if isinstance(message, str):
            message = message.encode('utf-8')

        # 패딩
        padded = cls.pad_message(message)

        # 초기화
        h = cls.H0.copy()

        # 각 512비트 블록 처리
        for i in range(0, len(padded), 64):
            block = padded[i:i+64]

            # 메시지 스케줄 W
            W = list(struct.unpack('>16I', block))
            for t in range(16, 64):
                W.append((cls.gamma1(W[t-2]) + W[t-7] +
                         cls.gamma0(W[t-15]) + W[t-16]) & 0xFFFFFFFF)

            # 작업 변수
            a, b, c, d, e, f, g, h_var = h

            # 64 라운드
            for t in range(64):
                if t < len(cls.K):
                    K_t = cls.K[t]
                else:
                    K_t = 0

                T1 = (h_var + cls.sigma1(e) + cls.ch(e, f, g) +
                      K_t + W[t]) & 0xFFFFFFFF
                T2 = (cls.sigma0(a) + cls.maj(a, b, c)) & 0xFFFFFFFF

                h_var = g
                g = f
                f = e
                e = (d + T1) & 0xFFFFFFFF
                d = c
                c = b
                b = a
                a = (T1 + T2) & 0xFFFFFFFF

            # 중간 해시 업데이트
            h[0] = (h[0] + a) & 0xFFFFFFFF
            h[1] = (h[1] + b) & 0xFFFFFFFF
            h[2] = (h[2] + c) & 0xFFFFFFFF
            h[3] = (h[3] + d) & 0xFFFFFFFF
            h[4] = (h[4] + e) & 0xFFFFFFFF
            h[5] = (h[5] + f) & 0xFFFFFFFF
            h[6] = (h[6] + g) & 0xFFFFFFFF
            h[7] = (h[7] + h_var) & 0xFFFFFFFF

        # 최종 해시값
        return ''.join(f'{x:08x}' for x in h)


class HashUtils:
    """해시 함수 유틸리티"""

    @staticmethod
    def sha256(data: Union[str, bytes]) -> str:
        """SHA-256 (표준 라이브러리)"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def sha512(data: Union[str, bytes]) -> str:
        """SHA-512"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha512(data).hexdigest()

    @staticmethod
    def sha3_256(data: Union[str, bytes]) -> str:
        """SHA3-256"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha3_256(data).hexdigest()

    @staticmethod
    def blake2b(data: Union[str, bytes]) -> str:
        """BLAKE2b"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.blake2b(data).hexdigest()

    @staticmethod
    def verify_hash(data: Union[str, bytes], expected_hash: str) -> bool:
        """해시 검증"""
        computed = HashUtils.sha256(data)
        import hmac
        return hmac.compare_digest(computed, expected_hash)


# 사용 예시
if __name__ == "__main__":
    # 표준 라이브러리 사용
    print("=== 표준 라이브러리 SHA-256 ===")
    message = "Hello, World!"
    hash_value = HashUtils.sha256(message)
    print(f"메시지: {message}")
    print(f"SHA-256: {hash_value}")
    print(f"길이: {len(hash_value)} 자 (256비트)")

    # 다양한 해시 함수 비교
    print("\n=== 해시 함수 비교 ===")
    test_data = "The quick brown fox jumps over the lazy dog"
    print(f"입력: {test_data}")
    print(f"SHA-256: {HashUtils.sha256(test_data)}")
    print(f"SHA-512: {HashUtils.sha512(test_data)[:64]}...")
    print(f"SHA3-256: {HashUtils.sha3_256(test_data)}")
    print(f"BLAKE2b: {HashUtils.blake2b(test_data)[:64]}...")

    # 충돌 예시 (다른 입력, 다른 해시)
    print("\n=== 작은 변화, 큰 차이 (Avalanche Effect) ===")
    msg1 = "Hello"
    msg2 = "Hella"  # 1글자만 다름
    print(f"'{msg1}' -> {HashUtils.sha256(msg1)}")
    print(f"'{msg2}' -> {HashUtils.sha256(msg2)}")
