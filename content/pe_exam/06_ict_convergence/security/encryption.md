+++
title = "암호화 (Encryption)"
date = 2025-03-01

[extra]
categories = "pe_exam-ict_convergence"
+++

# 암호화 (Encryption)

## 핵심 인사이트 (3줄 요약)
> **평문을 암호문으로 변환하여 기밀성을 보장하는 기술**. 대칭키(AES, ChaCha20)는 빠르고 비대칭키(RSA, ECC)는 안전한 키 분배. 실무는 하이브리드 방식(TLS)으로 조합한다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 암호화(Encryption)는 **평문(Plaintext)을 수학적 알고리즘과 키를 사용하여 암호문(Ciphertext)으로 변환**하여, 권한이 없는 사용자가 내용을 알 수 없게 하는 기밀성 보장 기술이다. 복호화(Decryption)는 반대 과정이다.

> 💡 **비유**: 암호화는 **"비밀 금고"** 같아요. 열쇠(키)가 있어야만 내용물(평문)을 꺼낼 수 있죠. 금고가 아무리 튼튼해도(알고리즘이 좋아도), 열쇠를 잃어버리면(키 유출) 끝이에요!

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 도청 위험**: 네트워크로 전송되는 데이터는 누구나 가로챌 수 있음 (Wi-Fi 스니핑, ISP 로깅)
2. **기술적 필요성 - CIA 3요소**: 기밀성(Confidentiality), 무결성(Integrity), 가용성(Availability) 중 기밀성과 무결성 확보
3. **시장/산업 요구 - 규제 준수**: GDPR, 개인정보보호법 등 데이터 보호 의무화. 미암호화 시 과태료 부과

**핵심 목적**: **기밀성 보장, 무결성 검증, 부인방지, 인증**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**암호화 분류 체계** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        암호화 기술 분류                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   암호화                                                                 │
│   ├── 양자 암호 (Quantum)                                               │
│   │   └── QKD (Quantum Key Distribution)                               │
│   │                                                                     │
│   └── 고전 암호 (Classical)                                             │
│       ├── 대칭키 (Symmetric)                                           │
│       │   ├── 블록 암호 (Block Cipher)                                 │
│       │   │   ├── AES (128/192/256 bit)                               │
│       │   │   ├── DES → 3DES (deprecated)                             │
│       │   │   └── ChaCha20 (stream cipher로도 사용)                    │
│       │   │                                                            │
│       │   └── 스트림 암호 (Stream Cipher)                              │
│       │       ├── RC4 (deprecated)                                    │
│       │       └── ChaCha20-Poly1305                                   │
│       │                                                                │
│       └── 비대칭키 (Asymmetric / Public Key)                            │
│           ├── 정수 인수분해 기반                                        │
│           │   └── RSA (1024 deprecated → 2048+ 권장)                   │
│           │                                                            │
│           ├── 이산대수 문제 기반                                        │
│           │   ├── DSA (Digital Signature Algorithm)                    │
│           │   └── DH (Diffie-Hellman), ECDH                           │
│           │                                                            │
│           └── 타원곡선 (Elliptic Curve)                                 │
│               ├── ECDSA (P-256, P-384)                                │
│               ├── EdDSA (Ed25519, Ed448)                              │
│               └── ECDH (X25519)                                       │
│                                                                        │
│   [암호화 vs 서명 vs 해시]                                               │
│                                                                        │
│   암호화: 평문 ──(공개키)──► 암호문 ──(개인키)──► 평문                   │
│   서명:  평문 ──(개인키)──► 서명    ──(공개키)──► 검증                   │
│   해시:  평문 ──(단방향)──► 다이제스트 (복호 불가)                        │
│                                                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

**대칭키 vs 비대칭키 비교** (필수: 표):
| 비교 항목 | 대칭키 암호화 | 비대칭키 암호화 |
|----------|--------------|----------------|
| **키 개수** | 1개 (송수신 동일) | 2개 (공개키 + 개인키) |
| **속도** | ★ 빠름 (100~1000배) | 느림 (연산 복잡) |
| **키 분배** | 어려움 (안전한 전달 필요) | 쉬움 (공개키 공개 가능) |
| **확장성** | O(n²) 키 필요 | O(n) 키 쌍 |
| **대표 알고리즘** | AES-256, ChaCha20 | RSA-2048, ECDSA-P256 |
| **주요 용도** | 대용량 데이터 암호화 | 키 교환, 서명, 인증 |
| **보안 강도** | 키 길이에 비례 | 수학적 난제에 의존 |

**블록 암호화 모드** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                      블록 암호화 모드 (Block Cipher Modes)               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. ECB (Electronic Codebook) - ❌ 사용 금지                            │
│     ┌───────────────────────────────────────────────────────────┐      │
│     │ P1 ──► AES ──► C1    P2 ──► AES ──► C2    ...            │      │
│     │    (같은 키)             (같은 키)                        │      │
│     │                                                            │      │
│     │ 문제: 같은 평문 → 같은 암호문 (패턴 노출)                  │      │
│     │ 예: 펭귄 이미지 암호화 → 펭귄 실루엣 보임                  │      │
│     └───────────────────────────────────────────────────────────┘      │
│                                                                         │
│  2. CBC (Cipher Block Chaining) - TLS 1.2까지 사용                      │
│     ┌───────────────────────────────────────────────────────────┐      │
│     │ IV ─┐                C1 ─┐                                │      │
│     │     ▼                    ▼                                │      │
│     │ P1 ──XOR──► AES ──► C1   P2 ──XOR──► AES ──► C2          │      │
│     │                                                            │      │
│     │ 특징: 이전 암호문과 XOR → 패턴 숨김                        │      │
│     │ 단점: 병렬 암호화 불가, 패딩 오라클 공격 가능              │      │
│     └───────────────────────────────────────────────────────────┘      │
│                                                                         │
│  3. CTR (Counter Mode) - 병렬 처리 가능                                 │
│     ┌───────────────────────────────────────────────────────────┐      │
│     │ Nonce||1 ──► AES ──► Key1 ──XOR P1 ──► C1                │      │
│     │ Nonce||2 ──► AES ──► Key2 ──XOR P2 ──► C2                │      │
│     │ ...                                                        │      │
│     │                                                            │      │
│     │ 장점: 병렬 처리, 랜덤 접근, 스트림처럼 사용 가능            │      │
│     │ 단점: IV 재사용 시 완전 붕괴                               │      │
│     └───────────────────────────────────────────────────────────┘      │
│                                                                         │
│  4. GCM (Galois/Counter Mode) - ★ TLS 1.3 기본, 권장                    │
│     ┌───────────────────────────────────────────────────────────┐      │
│     │                    ┌──────────────────────┐               │      │
│     │ 암호화 경로:        │ 인증 태그 생성       │               │      │
│     │ CTR 모드로 암호화   │ GHASH(C, AAD) → Tag │               │      │
│     │                    └──────────────────────┘               │      │
│     │                                                            │      │
│     │ AEAD (Authenticated Encryption with Associated Data)       │      │
│     │ → 기밀성 + 무결성을 동시에 보장                            │      │
│     │                                                            │      │
│     │ 출력: Ciphertext || Tag (16바이트)                        │      │
│     └───────────────────────────────────────────────────────────┘      │
│                                                                         │
│  [모드 선택 가이드]                                                      │
│  • 파일 암호화: AES-GCM (AEAD)                                          │
│  • TLS 통신: AES-GCM 또는 ChaCha20-Poly1305                             │
│  • 디스크 암호화: AES-XTS (XTS 모드)                                     │
│  • 레거시 호환: AES-CBC (HMAC 추가 필수)                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**RSA vs ECC 보안 강도** (필수: 표):
| 대칭키 | RSA | ECC (NIST) | ECC (Curve25519) |
|--------|-----|------------|------------------|
| 80bit | 1024bit | 160bit | - |
| 112bit | 2048bit | 224bit | - |
| 128bit | 3072bit | 256bit | 256bit |
| 192bit | 7680bit | 384bit | - |
| 256bit | 15360bit | 521bit | 448bit |

**핵심 알고리즘/공식** (해당 시 필수):
```
[AES (Advanced Encryption Standard)]

블록 크기: 128비트 (고정)
키 길이: 128/192/256비트 (라운드 수: 10/12/14)

AES-128 구조:
┌──────────────────────────────────────────────────┐
│  입력 (128비트)                                  │
│       ↓                                          │
│  [AddRoundKey - 초기 라운드]                     │
│       ↓                                          │
│  ┌──────────────────────────────────────────┐   │
│  │ Round 1~10 (또는 12, 14):                │   │
│  │   SubBytes (S-Box 치환)                  │   │
│  │   ShiftRows (행 이동)                    │   │
│  │   MixColumns (열 혼합) ← 마지막 라운드 제외│   │
│  │   AddRoundKey (라운드 키 XOR)            │   │
│  └──────────────────────────────────────────┘   │
│       ↓                                          │
│  출력 (128비트 암호문)                           │
└──────────────────────────────────────────────────┘

[RSA 암호화]

1. 키 생성:
   - 두 소수 p, q 선택 (n = p × q)
   - φ(n) = (p-1)(q-1) 계산
   - e 선택: 1 < e < φ(n), gcd(e, φ(n)) = 1
   - d 계산: d × e ≡ 1 (mod φ(n))

   공개키: (n, e)
   개인키: (n, d)

2. 암호화: C = M^e mod n
3. 복호화: M = C^d mod n
4. 서명: S = H(M)^d mod n
5. 검증: H(M) ≡ S^e mod n

[ECDH (타원곡선 Diffie-Hellman)]

곡선: y² = x³ + ax + b (mod p)
예: P-256 (secp256r1)

키 교환:
  Alice: 개인키 a, 공개키 A = aG
  Bob:   개인키 b, 공개키 B = bG

  공유 비밀:
    Alice: S = aB = a(bG) = abG
    Bob:   S = bA = b(aG) = abG

  → S의 x좌표에서 대칭키 유도

[ChaCha20-Poly1305]

ChaCha20: 스트림 암호 (Salsa20 후속)
  - 256비트 키, 96비트 논스, 32비트 카운터
  - ARX (Add-Rotate-XOR) 연산만 사용
  - 하드웨어 가속 없어도 AES보다 빠름 (모바일)

Poly1305: MAC (Message Authentication Code)
  - 일회용 키로 다이제스트 생성
  - AEAD 구성: ChaCha20 + Poly1305

[키 유도 함수 (KDF)]

PBKDF2: DK = PRF(Password, Salt, c, dkLen)
  - c: 반복 횟수 (10만~100만 권장)
  - 느려서 무차별 대입 방어

HKDF: PRK = HMAC-Hash(salt, IKM)
      OKM = HMAC-Hash(PRK, info || counter)
  - TLS 1.3에서 사용

Argon2 (2015 PWHC 우승):
  - 메모리 하드 함수 (GPU/ASIC 방어)
  - Argon2id 권장
```

**코드 예시** (필수: Python 암호화 구현):
```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Callable
from enum import Enum, auto
import hashlib
import hmac
import secrets
import os

# ============================================================
# 대칭키 암호화 시뮬레이터
# ============================================================

class BlockCipherMode(Enum):
    """블록 암호화 모드"""
    ECB = auto()
    CBC = auto()
    CTR = auto()
    GCM = auto()


@dataclass
class EncryptedData:
    """암호화 결과"""
    ciphertext: bytes
    iv: bytes = b''
    tag: bytes = b''  # GCM용
    mode: BlockCipherMode = BlockCipherMode.CBC


class SimpleBlockCipher:
    """간단한 블록 암호 시뮬레이션 (교육용)"""

    BLOCK_SIZE = 16  # 128비트

    def __init__(self, key: bytes):
        if len(key) not in (16, 24, 32):
            raise ValueError("키는 16, 24, 32바이트여야 함")
        self.key = key
        self._key_schedule = self._expand_key(key)

    def _expand_key(self, key: bytes) -> List[int]:
        """키 스케줄 생성 (시뮬레이션)"""
        # 실제 AES는 복잡한 키 확장 알고리즘 사용
        schedule = list(key)
        for i in range(10):
            schedule.append((schedule[-1] + i) % 256)
        return schedule

    def _encrypt_block(self, block: bytes) -> bytes:
        """단일 블록 암호화 (시뮬레이션)"""
        # 실제 AES: SubBytes, ShiftRows, MixColumns, AddRoundKey
        result = []
        for i, b in enumerate(block):
            key_byte = self._key_schedule[i % len(self._key_schedule)]
            result.append(b ^ key_byte)
        return bytes(result)

    def _decrypt_block(self, block: bytes) -> bytes:
        """단일 블록 복호화"""
        return self._encrypt_block(block)  # XOR은 역연산 동일


class SymmetricEncryption:
    """대칭키 암호화"""

    @staticmethod
    def pad(data: bytes, block_size: int = 16) -> bytes:
        """PKCS#7 패딩"""
        pad_len = block_size - (len(data) % block_size)
        return data + bytes([pad_len] * pad_len)

    @staticmethod
    def unpad(data: bytes) -> bytes:
        """PKCS#7 패딩 제거"""
        pad_len = data[-1]
        if pad_len > 16 or pad_len == 0:
            raise ValueError("잘못된 패딩")
        for i in range(1, pad_len + 1):
            if data[-i] != pad_len:
                raise ValueError("잘못된 패딩")
        return data[:-pad_len]

    @staticmethod
    def xor_bytes(a: bytes, b: bytes) -> bytes:
        """바이트 XOR"""
        return bytes(x ^ y for x, y in zip(a, b))

    @classmethod
    def encrypt_ecb(cls, cipher: SimpleBlockCipher,
                    plaintext: bytes) -> EncryptedData:
        """ECB 모드 암호화"""
        padded = cls.pad(plaintext)
        ciphertext = b''
        for i in range(0, len(padded), 16):
            block = padded[i:i+16]
            ciphertext += cipher._encrypt_block(block)
        return EncryptedData(ciphertext=ciphertext, mode=BlockCipherMode.ECB)

    @classmethod
    def decrypt_ecb(cls, cipher: SimpleBlockCipher,
                    data: EncryptedData) -> bytes:
        """ECB 모드 복호화"""
        plaintext = b''
        for i in range(0, len(data.ciphertext), 16):
            block = data.ciphertext[i:i+16]
            plaintext += cipher._decrypt_block(block)
        return cls.unpad(plaintext)

    @classmethod
    def encrypt_cbc(cls, cipher: SimpleBlockCipher,
                    plaintext: bytes, iv: bytes = None) -> EncryptedData:
        """CBC 모드 암호화"""
        iv = iv or secrets.token_bytes(16)
        padded = cls.pad(plaintext)
        ciphertext = b''
        prev = iv

        for i in range(0, len(padded), 16):
            block = padded[i:i+16]
            xored = cls.xor_bytes(block, prev)
            encrypted = cipher._encrypt_block(xored)
            ciphertext += encrypted
            prev = encrypted

        return EncryptedData(ciphertext=ciphertext, iv=iv, mode=BlockCipherMode.CBC)

    @classmethod
    def decrypt_cbc(cls, cipher: SimpleBlockCipher,
                    data: EncryptedData) -> bytes:
        """CBC 모드 복호화"""
        plaintext = b''
        prev = data.iv

        for i in range(0, len(data.ciphertext), 16):
            block = data.ciphertext[i:i+16]
            decrypted = cipher._decrypt_block(block)
            plaintext += cls.xor_bytes(decrypted, prev)
            prev = block

        return cls.unpad(plaintext)

    @classmethod
    def encrypt_ctr(cls, cipher: SimpleBlockCipher,
                    plaintext: bytes, nonce: bytes = None) -> EncryptedData:
        """CTR 모드 암호화"""
        nonce = nonce or secrets.token_bytes(12)
        counter = 0
        ciphertext = b''

        for i in range(0, len(plaintext), 16):
            # 카운터 블록 생성
            counter_block = nonce + counter.to_bytes(4, 'big')
            keystream = cipher._encrypt_block(counter_block)

            block = plaintext[i:i+16]
            ciphertext += cls.xor_bytes(block, keystream[:len(block)])
            counter += 1

        return EncryptedData(ciphertext=ciphertext, iv=nonce, mode=BlockCipherMode.CTR)

    @classmethod
    def decrypt_ctr(cls, cipher: SimpleBlockCipher,
                    data: EncryptedData) -> bytes:
        """CTR 모드 복호화 (암호화와 동일)"""
        return cls.encrypt_ctr(cipher, data.ciphertext, data.iv).ciphertext


# ============================================================
# 비대칭키 암호화 시뮬레이터 (RSA 단순화)
# ============================================================

@dataclass
class RSAKeyPair:
    """RSA 키 쌍"""
    n: int  # 모듈러스
    e: int  # 공개 지수
    d: int  # 개인 지수
    p: int = 0  # 소수1 (개인키)
    q: int = 0  # 소수2 (개인키)

    @property
    def public_key(self) -> Tuple[int, int]:
        return (self.n, self.e)

    @property
    def private_key(self) -> Tuple[int, int]:
        return (self.n, self.d)

    @property
    def key_size(self) -> int:
        return self.n.bit_length()


class SimpleRSA:
    """RSA 시뮬레이션 (교육용 - 작은 소수만 사용)"""

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """최대공약수"""
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """확장 유클리드 알고리즘"""
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = SimpleRSA.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y

    @staticmethod
    def mod_inverse(e: int, phi: int) -> int:
        """모듈러 역원 계산"""
        gcd_val, x, _ = SimpleRSA.extended_gcd(e % phi, phi)
        if gcd_val != 1:
            raise ValueError("역원이 존재하지 않음")
        return (x % phi + phi) % phi

    @staticmethod
    def is_prime(n: int, k: int = 5) -> bool:
        """밀러-라빈 소수 판정"""
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False

        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        for _ in range(k):
            a = secrets.randbelow(n - 3) + 2
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    @staticmethod
    def generate_prime(bits: int) -> int:
        """소수 생성"""
        while True:
            p = secrets.randbits(bits)
            p |= (1 << bits - 1) | 1  # 최상위/최하위 비트 1
            if SimpleRSA.is_prime(p):
                return p

    @classmethod
    def generate_keypair(cls, bits: int = 2048) -> RSAKeyPair:
        """RSA 키 쌍 생성"""
        # 실제로는 더 큰 소수 사용 (여기서는 시뮬레이션)
        half_bits = bits // 2

        p = cls.generate_prime(half_bits)
        q = cls.generate_prime(half_bits)
        while p == q:
            q = cls.generate_prime(half_bits)

        n = p * q
        phi = (p - 1) * (q - 1)

        # 공개 지수 선택 (일반적으로 65537)
        e = 65537
        while cls.gcd(e, phi) != 1:
            e += 2

        # 개인 지수 계산
        d = cls.mod_inverse(e, phi)

        return RSAKeyPair(n=n, e=e, d=d, p=p, q=q)

    @staticmethod
    def encrypt(plaintext: bytes, public_key: Tuple[int, int]) -> int:
        """RSA 암호화"""
        n, e = public_key
        m = int.from_bytes(plaintext, 'big')
        if m >= n:
            raise ValueError("평문이 너무 김")
        return pow(m, e, n)

    @staticmethod
    def decrypt(ciphertext: int, private_key: Tuple[int, int]) -> bytes:
        """RSA 복호화"""
        n, d = private_key
        m = pow(ciphertext, d, n)
        # 바이트로 변환 (길이 계산)
        byte_len = (n.bit_length() + 7) // 8
        return m.to_bytes(byte_len, 'big').lstrip(b'\x00')

    @staticmethod
    def sign(message: bytes, private_key: Tuple[int, int]) -> int:
        """RSA 서명"""
        n, d = private_key
        h = int.from_bytes(hashlib.sha256(message).digest(), 'big')
        return pow(h, d, n)

    @staticmethod
    def verify(message: bytes, signature: int,
               public_key: Tuple[int, int]) -> bool:
        """RSA 서명 검증"""
        n, e = public_key
        h = int.from_bytes(hashlib.sha256(message).digest(), 'big')
        verified = pow(signature, e, n)
        return h == verified


# ============================================================
# 해시 함수 및 MAC
# ============================================================

class HashFunctions:
    """해시 함수"""

    @staticmethod
    def sha256(data: bytes) -> bytes:
        """SHA-256"""
        return hashlib.sha256(data).digest()

    @staticmethod
    def sha512(data: bytes) -> bytes:
        """SHA-512"""
        return hashlib.sha512(data).digest()

    @staticmethod
    def hmac_sha256(key: bytes, data: bytes) -> bytes:
        """HMAC-SHA256"""
        return hmac.new(key, data, hashlib.sha256).digest()


class PasswordHashing:
    """비밀번호 해싱"""

    @staticmethod
    def pbkdf2(password: str, salt: bytes = None,
               iterations: int = 100000,
               key_length: int = 32) -> Tuple[bytes, bytes]:
        """PBKDF2 키 유도"""
        salt = salt or secrets.token_bytes(16)
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations, key_length)
        return key, salt

    @staticmethod
    def verify_password(password: str, stored_key: bytes,
                        salt: bytes, iterations: int) -> bool:
        """비밀번호 검증"""
        key, _ = PasswordHashing.pbkdf2(password, salt, iterations, len(stored_key))
        return hmac.compare_digest(key, stored_key)


# ============================================================
# 하이브리드 암호화 (TLS 방식 시뮬레이션)
# ============================================================

class HybridEncryption:
    """하이브리드 암호화 (RSA + AES)"""

    @staticmethod
    def encrypt(plaintext: bytes,
                recipient_public_key: Tuple[int, int]) -> Dict:
        """
        하이브리드 암호화:
        1. 무작위 AES 키 생성
        2. AES 키로 평문 암호화
        3. RSA로 AES 키 암호화
        """
        # 1. AES-256 키 생성
        aes_key = secrets.token_bytes(32)
        iv = secrets.token_bytes(16)

        # 2. AES로 평문 암호화 (CBC 모드)
        cipher = SimpleBlockCipher(aes_key)
        encrypted = SymmetricEncryption.encrypt_cbc(cipher, plaintext, iv)

        # 3. RSA로 AES 키 암호화
        encrypted_key = SimpleRSA.encrypt(aes_key, recipient_public_key)

        return {
            'encrypted_key': encrypted_key,
            'iv': iv,
            'ciphertext': encrypted.ciphertext
        }

    @staticmethod
    def decrypt(encrypted_data: Dict,
                recipient_private_key: Tuple[int, int]) -> bytes:
        """하이브리드 복호화"""
        # 1. RSA로 AES 키 복호화
        aes_key = SimpleRSA.decrypt(encrypted_data['encrypted_key'],
                                     recipient_private_key)

        # 2. AES로 암호문 복호화
        cipher = SimpleBlockCipher(aes_key)
        data = EncryptedData(
            ciphertext=encrypted_data['ciphertext'],
            iv=encrypted_data['iv'],
            mode=BlockCipherMode.CBC
        )
        return SymmetricEncryption.decrypt_cbc(cipher, data)


# ============================================================
# 사용 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("         암호화 기술 데모")
    print("=" * 60)

    # 1. 대칭키 암호화
    print("\n1. 대칭키 암호화 (AES)")
    print("-" * 40)

    key = secrets.token_bytes(32)  # AES-256
    cipher = SimpleBlockCipher(key)
    plaintext = b"Hello, World! This is a secret message."

    # CBC 모드
    encrypted_cbc = SymmetricEncryption.encrypt_cbc(cipher, plaintext)
    decrypted_cbc = SymmetricEncryption.decrypt_cbc(cipher, encrypted_cbc)
    print(f"원문: {plaintext}")
    print(f"CBC 암호화: {encrypted_cbc.ciphertext.hex()[:50]}...")
    print(f"CBC 복호화: {decrypted_cbc}")
    print(f"일치: {plaintext == decrypted_cbc}")

    # CTR 모드
    encrypted_ctr = SymmetricEncryption.encrypt_ctr(cipher, plaintext)
    decrypted_ctr = SymmetricEncryption.decrypt_ctr(cipher, encrypted_ctr)
    print(f"\nCTR 복호화: {decrypted_ctr}")
    print(f"일치: {plaintext == decrypted_ctr}")

    # 2. 비대칭키 암호화 (RSA)
    print("\n\n2. 비대칭키 암호화 (RSA)")
    print("-" * 40)

    # 키 생성 (시뮬레이션 - 작은 키)
    keypair = SimpleRSA.generate_keypair(bits=512)  # 실제는 2048+
    print(f"키 크기: {keypair.key_size}비트")
    print(f"공개 지수 e: {keypair.e}")

    # 암호화/복호화
    message = b"Secret"
    encrypted = SimpleRSA.encrypt(message, keypair.public_key)
    decrypted = SimpleRSA.decrypt(encrypted, keypair.private_key)
    print(f"\n원문: {message}")
    print(f"암호화: {encrypted}")
    print(f"복호화: {decrypted.strip(b'\\x00')}")

    # 서명/검증
    signature = SimpleRSA.sign(message, keypair.private_key)
    verified = SimpleRSA.verify(message, signature, keypair.public_key)
    print(f"\n서명: {signature}")
    print(f"검증: {'성공' if verified else '실패'}")

    # 3. 해시 및 MAC
    print("\n\n3. 해시 함수 및 MAC")
    print("-" * 40)

    data = b"Hello, World!"
    print(f"SHA-256: {HashFunctions.sha256(data).hex()}")
    print(f"SHA-512: {HashFunctions.sha512(data).hex()[:64]}...")

    mac_key = b"secret_key"
    mac = HashFunctions.hmac_sha256(mac_key, data)
    print(f"HMAC-SHA256: {mac.hex()}")

    # 4. 비밀번호 해싱
    print("\n\n4. 비밀번호 해싱 (PBKDF2)")
    print("-" * 40)

    password = "MySecurePassword123!"
    key, salt = PasswordHashing.pbkdf2(password, iterations=100000)
    print(f"솔트: {salt.hex()}")
    print(f"유도된 키: {key.hex()}")

    # 검증
    valid = PasswordHashing.verify_password(password, key, salt, 100000)
    print(f"비밀번호 검증: {'성공' if valid else '실패'}")

    # 잘못된 비밀번호
    invalid = PasswordHashing.verify_password("wrong", key, salt, 100000)
    print(f"잘못된 비밀번호: {'성공' if invalid else '실패'}")

    # 5. 하이브리드 암호화
    print("\n\n5. 하이브리드 암호화 (RSA + AES)")
    print("-" * 40)

    message = b"This is a large message that needs to be encrypted securely."
    encrypted = HybridEncryption.encrypt(message, keypair.public_key)
    decrypted = HybridEncryption.decrypt(encrypted, keypair.private_key)

    print(f"원문: {message}")
    print(f"암호화된 AES 키: {encrypted['encrypted_key']}")
    print(f"암호문 길이: {len(encrypted['ciphertext'])}바이트")
    print(f"복호화: {decrypted}")
    print(f"일치: {message == decrypted}")
