+++
title = "디지털 서명 (Digital Signature)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# 디지털 서명 (Digital Signature)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비대칭키 암호를 기반으로 메시지의 진위성(Authenticity), 무결성(Integrity), 부인방지(Non-repudiation)를 보장하는 암호학적 기법으로, 개인키로 서명하고 공개키로 검증합니다.
> 2. **가치**: 전자 문서의 법적 효력, 소프트웨어 배포 검증, 금융 거래 승인 등 디지털 경제의 신뢰 기반이며, 위조 방지를 위한 수학적 보증을 제공합니다.
> 3. **융합**: RSA-PSS, ECDSA, EdDSA 등 다양한 알고리즘이 있으며, 코드 서명, 문서 서명, 블록체인 트랜잭션, TLS 인증서 등 광범위하게 활용됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**디지털 서명(Digital Signature)**은 송신자의 개인키로 메시지에 서명하고, 수신자가 송신자의 공개키로 서명을 검증하는 암호학적 메커니즘입니다. 전자 서명(e-Signature)과 달리 수학적 보안 보장을 제공합니다.

```
디지털 서명의 3가지 보안 속성:
1. 진위성 (Authenticity)
   - 서명자가 주장하는 당사자가 맞음을 보장

2. 무결성 (Integrity)
   - 서명된 후 메시지가 변경되지 않았음을 보장

3. 부인방지 (Non-repudiation)
   - 서명자가 나중에 서명 사실을 부인할 수 없음
```

#### 2. 비유를 통한 이해
디지털 서명은 **'직인(官印)과 비밀 도장'**에 비유할 수 있습니다.
- **개인키**: 나만 가진 비밀 도장 (서명용)
- **공개키**: 누구나 볼 수 있는 직인 카드 (검증용)
- **서명**: 비밀 도장으로 찍은 흔적
- **검증**: 직인 카드와 대조하여 진품 확인
- **위조 불가**: 비밀 도장 없이는 동일한 흔적 생성 불가

#### 3. 등장 배경 및 발전 과정
1. **1976년**: Diffie-Hellman 논문에서 디지털 서명 개념 제시
2. **1977년**: RSA 알고리즘 발표 (서명 + 암호화 가능)
3. **1985년**: ElGamal 서명 체계 제안
4. **1991년**: NIST DSA(Digital Signature Algorithm) 표준화
5. **1992년**: Schnorr 서명 특허 (ECDSA 기반)
6. **1990년대**: PKI 구축, 전자서명법 제정 (한국 1999년)
7. **2010년대**: EdDSA (Ed25519) 보급
8. **2020년대**: PQC 디지털 서명 (CRYSTALS-Dilithium, SPHINCS+)

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 디지털 서명 알고리즘 비교

| 알고리즘 | 기반 문제 | 키 크기 | 서명 크기 | 서명 속도 | 검증 속도 | 보안 비트 |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **RSA-PKCS#1** | 소인수분해 | 2048비트 | 256B | 느림 | 빠름 | 112 |
| **RSA-PSS** | 소인수분해 | 2048비트 | 256B | 느림 | 빠름 | 112 |
| **DSA** | 이산대수 | 2048비트 | 40B | 중간 | 중간 | 112 |
| **ECDSA P-256** | ECDLP | 256비트 | 64B | 빠름 | 빠름 | 128 |
| **Ed25519** | ECDLP | 256비트 | 64B | 매우 빠름 | 매우 빠름 | 128 |
| **ECDSA P-384** | ECDLP | 384비트 | 96B | 빠름 | 빠름 | 192 |
| **Dilithium2** | 격자 | 2560비트 | 2420B | 빠름 | 빠름 | 128 (양자) |
| **SPHINCS+** | 해시 | 32B | 7856B | 느림 | 중간 | 128 (양자) |

#### 2. 디지털 서명 프로세스 다이어그램

```
=== 디지털 서명 생성 프로세스 ===

┌────────────────────────────────────────────────────────────┐
│                      서명자 (Signer)                         │
│                                                            │
│   ┌──────────────┐                                         │
│   │   Message    │                                         │
│   │     (M)      │                                         │
│   └──────┬───────┘                                         │
│          │                                                 │
│          ▼                                                 │
│   ┌──────────────┐      ┌──────────────┐                  │
│   │ Hash Function│─────►│   Hash(H)    │                  │
│   │  (SHA-256)   │      │              │                  │
│   └──────────────┘      └──────┬───────┘                  │
│                                │                          │
│                                ▼                          │
│   ┌──────────────┐      ┌──────────────┐                  │
│   │  Private Key │─────►│   Sign Alg   │                  │
│   │    (d)       │      │ (RSA/ECDSA)  │                  │
│   └──────────────┘      └──────┬───────┘                  │
│                                │                          │
│                                ▼                          │
│                         ┌──────────────┐                  │
│                         │  Signature   │                  │
│                         │    (S)       │                  │
│                         └──────────────┘                  │
└────────────────────────────────────────────────────────────┘

===========================================

=== 디지털 서명 검증 프로세스 ===

┌────────────────────────────────────────────────────────────┐
│                    검증자 (Verifier)                        │
│                                                            │
│   ┌──────────────┐                                         │
│   │   Message    │                                         │
│   │     (M)      │◄─────────────────────────────────┐     │
│   └──────┬───────┘                                  │     │
│          │                                          │     │
│          ▼                                          │     │
│   ┌──────────────┐      ┌──────────────┐           │     │
│   │ Hash Function│─────►│   Hash(H')   │           │     │
│   │  (SHA-256)   │      │              │           │     │
│   └──────────────┘      └──────┬───────┘           │     │
│                                │                   │     │
│   ┌──────────────┐             │  ┌──────────────┐ │     │
│   │  Public Key  │─────────────┼─►│   Verify Alg │ │     │
│   │    (Q)       │             │  │ (RSA/ECDSA)  │ │     │
│   └──────────────┘             │  └──────┬───────┘ │     │
│                                │         │         │     │
│   ┌──────────────┐             │         ▼         │     │
│   │  Signature   │─────────────┴──►   ┌────────┐  │     │
│   │    (S)       │                    │  H''   │  │     │
│   └──────────────┘                    └────┬───┘  │     │
│                                            │      │     │
│                                            ▼      │     │
│                                      ┌────────┐  │     │
│                                      │ H'==H''│  │     │
│                                      │   ?    │  │     │
│                                      └────┬───┘  │     │
│                                           │      │     │
│                          ┌────────────────┼──────┘     │
│                          ▼                ▼             │
│                    ┌─────────┐     ┌─────────┐         │
│                    │ VALID ✓ │     │INVALID ✗│         │
│                    └─────────┘     └─────────┘         │
└────────────────────────────────────────────────────────────┘
```

#### 3. 심층 동작 원리: RSA-PSS vs ECDSA

```python
import os
import hashlib
from typing import Tuple
from dataclasses import dataclass

# ============================================================
# RSA-PSS (Probabilistic Signature Scheme) 구현 개요
# ============================================================

class RSAPSSSignature:
    """
    RSA-PSS 서명 체계 (PKCS#1 v2.2, RFC 8017)

    특징:
    - 확률적 서명 (동일 메시지도 매번 다른 서명)
    - 안전한 패딩 (PSS = MGF1 + Salt)
    - 증명 가능한 보안 (Random Oracle Model)
    """

    def __init__(self, n: int, e: int, d: int = None):
        """
        Args:
            n: 모듈러스 (p * q)
            e: 공개 지수 (보통 65537)
            d: 개인 지수 (서명용)
        """
        self.n = n
        self.e = e
        self.d = d
        self.k = (n.bit_length() + 7) // 8  # 바이트 단위 모듈러스 크기
        self.hash_func = hashlib.sha256
        self.salt_len = 32  # 256비트 salt

    def _mgf1(self, seed: bytes, mask_len: int) -> bytes:
        """
        MGF1 (Mask Generation Function 1)
        RFC 8017 Section B.2.1
        """
        mask = b''
        counter = 0
        while len(mask) < mask_len:
            c = counter.to_bytes(4, 'big')
            mask += self.hash_func(seed + c).digest()
            counter += 1
        return mask[:mask_len]

    def sign(self, message: bytes) -> bytes:
        """
        RSA-PSS 서명 생성

        과정:
        1. mHash = Hash(M)
        2. M' = Padding1 || mHash || Salt
        3. H = Hash(M')
        4. DB = PS || 0x01 || Salt
        5. dbMask = MGF(H, emLen - hLen - 1)
        6. maskedDB = DB XOR dbMask
        7. EM = maskedDB || H || 0xbc
        8. S = EM^d mod n
        """
        if self.d is None:
            raise ValueError("Private key required for signing")

        # 1. 메시지 해시
        m_hash = self.hash_func(message).digest()
        h_len = len(m_hash)

        # 2. Salt 생성 (랜덤)
        salt = os.urandom(self.salt_len)

        # 3. M' = 0x00 00 00 00 00 00 00 00 || mHash || Salt
        m_prime = b'\x00' * 8 + m_hash + salt

        # 4. H = Hash(M')
        h = self.hash_func(m_prime).digest()

        # 5. DB = PS || 0x01 || Salt
        em_len = self.k
        ps_len = em_len - h_len - self.salt_len - 2
        db = b'\x00' * ps_len + b'\x01' + salt

        # 6. dbMask = MGF(H, emLen - hLen - 1)
        db_mask = self._mgf1(h, em_len - h_len - 1)

        # 7. maskedDB = DB XOR dbMask
        masked_db = bytes(a ^ b for a, b in zip(db, db_mask))

        # 8. maskedDB의 최상위 비트를 0으로
        masked_db = bytes([masked_db[0] & 0x7f]) + masked_db[1:]

        # 9. EM = maskedDB || H || 0xbc
        em = masked_db + h + b'\xbc'

        # 10. S = OS2IP(EM)^d mod n
        m = int.from_bytes(em, 'big')
        s = pow(m, self.d, self.n)

        return s.to_bytes(self.k, 'big')

    def verify(self, message: bytes, signature: bytes) -> bool:
        """
        RSA-PSS 서명 검증
        """
        # 1. 서명을 정수로 변환 후 공개키로 복원
        s = int.from_bytes(signature, 'big')
        if s >= self.n:
            return False

        # 2. EM = S^e mod n
        m = pow(s, self.e, self.n)
        em = m.to_bytes(self.k, 'big')

        # 3. 구조 검증
        h_len = 32  # SHA-256
        em_len = len(em)

        if em[-1] != 0xbc:
            return False

        # 4. maskedDB, H 분리
        masked_db = em[:em_len - h_len - 1]
        h = em[em_len - h_len - 1:-1]

        # 5. 최상위 비트 확인
        if masked_db[0] & 0x80:
            return False

        # 6. DB = maskedDB XOR MGF(H, ...)
        db_mask = self._mgf1(h, em_len - h_len - 1)
        db = bytes(a ^ b for a, b in zip(masked_db, db_mask))

        # 7. DB 구조 확인: PS || 0x01 || Salt
        salt_start = db.find(b'\x01')
        if salt_start == -1:
            return False

        salt = db[salt_start + 1:]

        # 8. M' 재구성 및 H' 계산
        m_hash = self.hash_func(message).digest()
        m_prime = b'\x00' * 8 + m_hash + salt
        h_prime = self.hash_func(m_prime).digest()

        # 9. H == H' 비교
        return h == h_prime


# ============================================================
# ECDSA (Elliptic Curve Digital Signature Algorithm) 구현 개요
# ============================================================

@dataclass
class ECDSASignature:
    """ECDSA 서명 (r, s) 쌍"""
    r: int
    s: int

    def to_der(self) -> bytes:
        """DER 인코딩"""
        def encode_integer(n: int) -> bytes:
            b = n.to_bytes((n.bit_length() + 7) // 8 or 1, 'big')
            if b[0] & 0x80:
                b = b'\x00' + b
            return bytes([0x02, len(b)]) + b

        r_enc = encode_integer(self.r)
        s_enc = encode_integer(self.s)
        seq = r_enc + s_enc
        return bytes([0x30, len(seq)]) + seq


class ECDSASigner:
    """
    ECDSA 서명 체계 (FIPS 186-5, ANSI X9.62)

    특징:
    - 타원곡선 기반 (작은 키, 효율적)
    - 결정론적 nonce 가능 (RFC 6979)
    - 비트코인, 이더리움 표준
    """

    def __init__(self, curve_order: int, private_key: int = None):
        """
        Args:
            curve_order: 타원곡선 위수 n
            private_key: 개인키 d (1 < d < n)
        """
        self.n = curve_order
        self.private_key = private_key

    def sign(self, message: bytes, k: int = None) -> ECDSASignature:
        """
        ECDSA 서명 생성

        과정:
        1. e = Hash(M)
        2. k ← Random(1, n-1)  또는 결정론적 k
        3. (x, y) = k × G
        4. r = x mod n (r = 0이면 2로)
        5. s = k^(-1) × (e + d × r) mod n (s = 0이면 2로)
        6. Return (r, s)
        """
        if self.private_key is None:
            raise ValueError("Private key required")

        # 1. 메시지 해시
        e = int.from_bytes(hashlib.sha256(message).digest(), 'big')

        # 2. nonce k (랜덤 또는 결정론적)
        if k is None:
            k = self._deterministic_k(message)
        else:
            if not (1 <= k < self.n):
                raise ValueError("Invalid k value")

        # 3. k × G 계산 (타원곡선 점 곱셈)
        # 실제 구현에서는 타원곡경 라이브러리 사용
        # 여기서는 개념적 표현
        # point = scalar_multiply(k, G)
        # x = point.x

        # 예시를 위한 임시값
        import hashlib
        x = int.from_bytes(hashlib.sha256(k.to_bytes(32, 'big')).digest(), 'big')

        # 4. r = x mod n
        r = x % self.n
        if r == 0:
            raise ValueError("r = 0, retry with new k")

        # 5. s = k^(-1) × (e + d × r) mod n
        k_inv = pow(k, -1, self.n)
        s = (k_inv * (e + self.private_key * r)) % self.n
        if s == 0:
            raise ValueError("s = 0, retry with new k")

        # Low-S 정규화 (malleability 방지)
        if s > self.n // 2:
            s = self.n - s

        return ECDSASignature(r, s)

    def _deterministic_k(self, message: bytes) -> int:
        """
        결정론적 k 생성 (RFC 6979)

        장점:
        - 난수 생성기 의존성 제거
        - k 재사용 공격 방지
        - 재현 가능한 서명
        """
        h = hashlib.sha256(message).digest()
        h_int = int.from_bytes(h, 'big')

        # HMAC-DRBG 기반 k 유도
        # 자세한 구현은 RFC 6979 참조
        v = b'\x01' * 32
        k = b'\x00' * 32

        # Step a-d
        k = hashlib.sha256(k + v + b'\x00' +
                          self.private_key.to_bytes(32, 'big') + h).digest()
        v = hashlib.sha256(k + v).digest()
        k = hashlib.sha256(k + v + b'\x01' +
                          self.private_key.to_bytes(32, 'big') + h).digest()
        v = hashlib.sha256(k + v).digest()

        # T생성 및 k 계산
        for _ in range(100):  # 최대 100회 시도
            v = hashlib.sha256(k + v).digest()
            k_candidate = int.from_bytes(v, 'big')
            if 1 <= k_candidate < self.n:
                return k_candidate
            k = hashlib.sha256(k + v + b'\x00').digest()
            v = hashlib.sha256(k + v).digest()

        raise RuntimeError("Failed to generate k")

    @staticmethod
    def verify(message: bytes, signature: ECDSASignature,
               public_key_point: tuple, curve_order: int,
               base_point: tuple) -> bool:
        """
        ECDSA 서명 검증

        과정:
        1. r, s ∈ [1, n-1] 확인
        2. e = Hash(M)
        3. w = s^(-1) mod n
        4. u1 = e × w mod n
        5. u2 = r × w mod n
        6. (x, y) = u1 × G + u2 × Q
        7. Return r == x mod n
        """
        r, s = signature.r, signature.s
        n = curve_order

        # 1. r, s 범위 확인
        if not (1 <= r < n and 1 <= s < n):
            return False

        # 2. 메시지 해시
        e = int.from_bytes(hashlib.sha256(message).digest(), 'big')

        # 3. w = s^(-1) mod n
        w = pow(s, -1, n)

        # 4, 5. u1, u2 계산
        u1 = (e * w) % n
        u2 = (r * w) % n

        # 6. u1 × G + u2 × Q 계산
        # 실제 구현: point_add(scalar_mult(u1, G), scalar_mult(u2, Q))
        # x = result.x

        # 예시용 단순화
        import hashlib
        x = int.from_bytes(
            hashlib.sha256(
                u1.to_bytes(32, 'big') + u2.to_bytes(32, 'big')
            ).digest(), 'big'
        )

        # 7. r == x mod n 확인
        return r == (x % n)


# ============================================================
# EdDSA (Edwards-curve Digital Signature Algorithm) - Ed25519
# ============================================================

class Ed25519Signer:
    """
    Ed25519 서명 (RFC 8032)

    특징:
    - 결정론적 (k 없음, 해시에서 유도)
    - 매우 빠름 (최적화된 곡선)
    - Side-channel 안전
    - 작은 서명 (64 bytes)
    """

    def __init__(self, private_key: bytes = None):
        if private_key is None:
            private_key = os.urandom(32)
        self.private_key = private_key

        # 키 유도
        h = hashlib.sha512(private_key).digest()
        self.scalar = int.from_bytes(h[:32], 'little') & (2**252 - 8) | (2**252)
        self.prefix = h[32:]

    def sign(self, message: bytes) -> bytes:
        """
        Ed25519 서명 생성

        1. r = H(prefix || M) mod n
        2. R = r × B (B: 기준점)
        3. K = H(R || A || M) mod n (A: 공개키)
        4. S = (r + K × s) mod n
        5. Return R || S (64 bytes)
        """
        # 실제 구현은 cryptography 라이브러리 사용
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

        private_key = Ed25519PrivateKey.from_private_bytes(self.private_key)
        signature = private_key.sign(message)

        return signature

    def get_public_key(self) -> bytes:
        """공개키 반환 (32 bytes)"""
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

        private_key = Ed25519PrivateKey.from_private_bytes(self.private_key)
        public_key = private_key.public_key()
        return public_key.public_bytes_raw()

    @staticmethod
    def verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
        """Ed25519 서명 검증"""
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        from cryptography.exceptions import InvalidSignature

        try:
            pk = Ed25519PublicKey.from_public_bytes(public_key)
            pk.verify(signature, message)
            return True
        except InvalidSignature:
            return False


# 사용 예시
def signature_demo():
    """디지털 서명 데모"""

    message = b"이 문서는 법적 효력을 가집니다."

    # Ed25519 서명
    signer = Ed25519Signer()
    signature = signer.sign(message)
    public_key = signer.get_public_key()

    print("=== Ed25519 서명 ===")
    print(f"메시지: {message.decode()}")
    print(f"공개키: {public_key.hex()}")
    print(f"서명: {signature.hex()}")
    print(f"서명 크기: {len(signature)} bytes")

    # 검증
    is_valid = Ed25519Signer.verify(message, signature, public_key)
    print(f"검증 결과: {'VALID ✓' if is_valid else 'INVALID ✗'}")

    # 변조된 메시지 검증
    tampered = b"이 문서는 법적 효력이 없습니다."
    is_valid_tampered = Ed25519Signer.verify(tampered, signature, public_key)
    print(f"변조 검증: {'VALID' if is_valid_tampered else 'INVALID ✗'} (예상: INVALID)")


if __name__ == "__main__":
    signature_demo()
```

#### 4. 서명 알고리즘 선택 가이드

| 용도 | 추천 알고리즘 | 이유 |
|:---|:---|:---|
| **TLS 인증서** | ECDSA P-256 | 표준, 효율적 |
| **코드 서명** | RSA-2048 / RSA-4096 | 호환성, 신뢰 |
| **JWT 토큰** | RS256 / ES256 | 검증 속도 |
| **블록체인** | ECDSA secp256k1 / Ed25519 | 표준, 효율 |
| **SSH 키** | Ed25519 | 보안, 성능 |
| **모바일** | ECDSA P-256 | 작은 키, 빠름 |
| **양자 대비** | CRYSTALS-Dilithium | PQC 표준 |

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. RSA vs ECDSA vs EdDSA 비교

| 특성 | RSA-2048 | ECDSA P-256 | Ed25519 |
|:---|:---|:---|:---|
| **개인키 크기** | 256B | 32B | 32B |
| **공개키 크기** | 256B | 64B | 32B |
| **서명 크기** | 256B | 64B | 64B |
| **서명 속도** | 느림 (~5ms) | 빠름 (~0.1ms) | 매우 빠름 (~0.05ms) |
| **검증 속도** | 빠름 (~0.1ms) | 빠름 (~0.2ms) | 매우 빠름 (~0.1ms) |
| **난수 필요** | X | O (필수!) | X |
| **Malleability** | 안전 | 취약 (Low-S 필요) | 안전 |

#### 2. 과목 융합 관점 분석

**네트워크 보안과 융합**
- TLS 1.3: ECDSA/EdDSA 인증서 지원
- mTLS: 상호 인증에 서명 사용
- Certificate Transparency: SCT(Signed Certificate Timestamp)

**데이터베이스와 융합**
- 감사 로그 서명
- 트랜잭션 무결성
- Change Data Capture 검증

**클라우드와 융합**
- AWS KMS: 비대칭 키 서명
- GCP Cloud KMS: ECDSA, RSA 지원
- Azure Key Vault: HSM 기반 서명

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: API 서버 JWT 서명 알고리즘 선택**
- 상황: 마이크로서비스 간 인증 토큰
- 판단: ES256 (ECDSA P-256 + SHA-256)
- 이유:
  - 작은 토큰 크기 (64B 서명 vs 256B RSA)
  - 빠른 검증
  - 표준 지원 (RFC 7518)

**시나리오 2: IoT 펌웨어 서명**
- 상황: OTA 업데이트 검증, 제한된 리소스
- 판단: Ed25519
- 이유:
  - 매우 빠른 검증
  - 작은 서명 크기
  - 난수 생성기 불필요

**시나리오 3: 장기 문서 보관**
- 상황: 10년 이상 보관, 법적 효력
- 판단: RSA-4096 또는 ECDSA P-384 + 타임스탬프
- 이유:
  - 미래 보안 마진
  - 장기 검증 가능

#### 2. 도입 시 고려사항 (체크리스트)

**기술적 체크리스트**
- [ ] 알고리즘 선택 (RSA vs ECDSA vs EdDSA)
- [ ] 키 길이 결정 (보안 vs 성능)
- [ ] 해시 함수 선택 (SHA-256/384)
- [ ] 난수 생성 품질 (ECDSA)
- [ ] DER vs Raw 인코딩

**운영 체크리스트**
- [ ] 키 저장 보안 (HSM 권장)
- [ ] 키 순환 정책
- [ ] 서명 로그 및 감사
- [ ] 타임스탬프 서비스 (장기 검증)

#### 3. 안티패턴 (Anti-patterns)

```
취약한 구현 (금지!)

1. ECDSA k 재사용 (Sony PS3 사건)
   ❌ k = 0xdeadbeef  # 고정값
   → 두 서명에서 개인키 복구 가능!
   → d = (s1-s2) / (k × (r1-r2)) mod n

2. RSA PKCS#1 v1.5 서명
   ❌ signature = rsa.sign(message, 'PKCS1-v1_5')
   → 선택적 위조 공격 가능
   → RSA-PSS 사용

3. ECDSA Malleability 방치
   ❌ s 그대로 사용
   → s' = n - s도 유효한 서명
   → Low-S 적용 필수

4. 취약한 해시 사용
   ❌ ecdsa.sign(message, hash='MD5')
   → 해시 충돌로 서명 위조 가능

올바른 구현:

1. 결정론적 k 또는 안전한 난수
   ✓ k = deterministic_k(message, private_key)  # RFC 6979
   또는
   ✓ k = secrets.randbelow(n)  # CSPRNG

2. RSA-PSS 사용
   ✓ signature = rsa.sign(message, padding.PSS(
   ...     mgf=padding.MGF1(hashes.SHA256()),
   ...     salt_length=padding.PSS.MAX_LENGTH
   ... ), hashes.SHA256())

3. Low-S 적용
   ✓ if s > n // 2: s = n - s

4. 강력한 해시
   ✓ ecdsa.sign(message, hash='SHA-256')
```

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 | 항목 | 수치/내용 |
|:---|:---|:---|
| **부인방지** | 법적 증거 | 전자서명법 제3조 |
| **무결성** | 변조 탐지 | 2^128 노력 필요 |
| **성능** | 서명/검증 | Ed25519: 50μs/100μs |
| **저장** | 토큰 크기 | ECDSA: 64B vs RSA: 256B |

#### 2. 미래 전망 및 진화 방향

```
디지털 서명 진화
├── Post-Quantum 전환
│   ├── CRYSTALS-Dilithium (NIST 선택)
│   ├── FALCON
│   └── SPHINCS+ (해시 기반)
├── 하이브리드 서명
│   ├── ECDSA + Dilithium
│   └── Ed25519 + SPHINCS+
└── Aggregated 서명
    ├── BLS 서명 (집계 가능)
    └── Schnorr 멀티시그
```

#### 3. 참고 표준/가이드

| 표준 | 내용 |
|:---|:---|
| **FIPS 186-5** | 디지털 서명 표준 (DSA, ECDSA, EdDSA) |
| **RFC 8017** | RSA-PSS (PKCS#1 v2.2) |
| **RFC 8032** | EdDSA (Ed25519, Ed448) |
| **RFC 6979** | 결정론적 DSA/ECDSA |
| **ISO/IEC 14888** | 디지털 서명 부속서 |
| **전자서명법** | 대한민국 법적 근거 |

---

### 관련 개념 맵 (Knowledge Graph)
- [RSA](@/studynotes/09_security/02_crypto/rsa.md) : RSA 서명의 수학적 기반
- [ECC](@/studynotes/09_security/02_crypto/ecc.md) : ECDSA의 타원곡선 기반
- [해시 함수](@/studynotes/09_security/02_crypto/hash_function.md) : 서명 전 메시지 해시
- [PKI](@/studynotes/09_security/10_pki/pki.md) : 서명 기반 공개키 기반구조
- [부인방지](@/studynotes/09_security/01_policy/non_repudiation.md) : 서명의 법적 효력

---

### 어린이를 위한 3줄 비유 설명
1. **비밀 도장**: 디지털 서명은 나만 가진 비밀 도장으로 문서에 찍는 것이에요. 내 도장이 찍힌 문서는 내가 승인했다는 뜻이죠.
2. **위조 불가**: 비밀 도장이 없으면 똑같은 흔적을 만들 수 없어요. 아무리 똑똑한 나쁜 사람도 위조할 수 없답니다.
3. **누구나 확인**: 내 도장 흔적은 누구나 볼 수 있는 공개 카드와 비교해서 확인할 수 있어요. 문서가 변조되었는지도 바로 알 수 있죠!
