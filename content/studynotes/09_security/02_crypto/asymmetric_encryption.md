+++
title = "비대칭키 암호 (Asymmetric Encryption)"
date = "2026-03-04"
[extra]
categories = "studynotes-09_security"
+++

# 비대칭키 암호 (Asymmetric Encryption)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 공개키와 개인키 두 개의 서로 다른 키를 사용하여 암호화/복호화하거나 서명/검증하는 암호 방식으로, 키 분배 문제를 근본적으로 해결합니다.
> 2. **가치**: 디지털 서명, 키 교환, 인증서 기반 인증, PGP, TLS 핸드쉐이크 등 현대 인터넷 보안의 기반입니다.
> 3. **융합**: RSA, ECC, DH 등이 대칭키 암호와 결합하여 하이브리드 암호 시스템 구성에 활용됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**비대칭키 암호(Asymmetric Encryption)**, 또는 **공개키 암호(Public Key Cryptography)**는 한 쌍의 키(공개키, 개인키)를 사용하는 암호 시스템입니다. 공개키로 암호화한 것은 개인키로만 복호화할 수 있고, 개인키로 서명한 것은 공개키로만 검증할 수 있습니다.

**핵심 특성**:
- **두 개의 키**: 공개키(Public Key) + 개인키(Private Key)
- **수학적 관계**: 키 쌍은 수학적으로 연관되나 역계산 불가
- **키 분배 해결**: 공개키는 공개해도 안전
- **계산 비용**: 대칭키 대비 느림 (100~1000배)

**주요 용도**:
- **기밀성**: 공개키 암호 → 개인키 복호
- **서명**: 개인키 서명 → 공개키 검증
- **키 교환**: DH, ECDH

#### 2. 💡 비유를 통한 이해
비대칭키 암호는 **'우편함과 열쇠'**에 비유할 수 있습니다.
- **공개키 = 우편함 슬롯**: 누구나 편지를 넣을 수 있음
- **개인키 = 우편함 열쇠**: 주인만 열어볼 수 있음
- **암호화**: 편지를 슬롯에 넣는 것
- **복호화**: 열쇠로 열어서 편지를 꺼내는 것

#### 3. 등장 배경 및 발전 과정
1. **Diffie-Hellman (1976)**: 최초의 공개키 키교환 알고리즘
2. **RSA (1977)**: Rivest, Shamir, Adleman - 최초의 실용적 공개키 암호
3. **ElGamal (1985)**: 이산대수 기반
4. **ECC (1985)**: 타원곡선 암호 - 더 짧은 키로 동등 보안
5. **EdDSA (2011)**: Edwards曲线 기반 고속 서명
6. **PQC (2024)**: 양자 내성 암호 NIST 표준화

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 비대칭키 알고리즘 비교 (표)

| 알고리즘 | 기반 문제 | 키 길이 (128비트 보안) | 속도 | 용도 |
|:---|:---|:---|:---|:---|
| **RSA-3072** | 소인수분해 | 3072비트 | 느림 | 암호화, 서명 |
| **RSA-4096** | 소인수분해 | 4096비트 | 매우 느림 | 고보안 서명 |
| **ECDSA P-256** | 이산대수(ECC) | 256비트 | 중간 | 디지털 서명 |
| **ECDSA P-384** | 이산대수(ECC) | 384비트 | 중간 | 고보안 서명 |
| **Ed25519** | Edwards曲线 | 256비트 | 빠름 | 고속 서명 |
| **ECDH P-256** | 이산대수(ECC) | 256비트 | 중간 | 키 교환 |
| **X25519** | Montgomery曲线 | 256비트 | 빠름 | 키 교환 |

#### 2. RSA 작동 원리 다이어그램

```text
<<< RSA (Rivest-Shamir-Adleman) Algorithm >>>

    [키 생성 (Key Generation)]
    ┌─────────────────────────────────────────────────────────────┐
    │  1. 두 소수 p, q 선택 (큰 소수, 1024비트 이상)            │
    │  2. n = p × q 계산 (모듈러스)                              │
    │  3. φ(n) = (p-1) × (q-1) 계산 (오일러 함수)                │
    │  4. e 선택: 1 < e < φ(n), gcd(e, φ(n)) = 1                 │
    │     (일반적으로 65537 사용)                                 │
    │  5. d 계산: d × e ≡ 1 (mod φ(n))                           │
    │                                                             │
    │  공개키: (n, e)                                            │
    │  개인키: (n, d) 또는 (p, q, d)                             │
    └─────────────────────────────────────────────────────────────┘

    [암호화 (Encryption)]
    ┌─────────────────────────────────────────────────────────────┐
    │  평문 m를 공개키 (n, e)로 암호화:                          │
    │                                                             │
    │  c = m^e mod n                                             │
    │                                                             │
    │  예시:                                                      │
    │  m = 123 (평문)                                            │
    │  e = 65537 (공개 지수)                                     │
    │  n = 3233 (모듈러스)                                       │
    │  c = 123^65537 mod 3233 = 855 (암호문)                     │
    └─────────────────────────────────────────────────────────────┘

    [복호화 (Decryption)]
    ┌─────────────────────────────────────────────────────────────┐
    │  암호문 c를 개인키 (n, d)로 복호화:                        │
    │                                                             │
    │  m = c^d mod n                                             │
    │                                                             │
    │  복호화가 작동하는 이유:                                    │
    │  c^d = (m^e)^d = m^(e×d) = m^(1 + k×φ(n))                 │
    │       ≡ m × m^(k×φ(n)) ≡ m × 1 ≡ m (mod n)                │
    └─────────────────────────────────────────────────────────────┘

    [서명 (Digital Signature)]
    ┌─────────────────────────────────────────────────────────────┐
    │  메시지 m에 대한 서명 생성 (개인키 사용):                  │
    │                                                             │
    │  s = H(m)^(d) mod n                                        │
    │                                                             │
    │  서명 검증 (공개키 사용):                                   │
    │  H(m) ≟ s^e mod n                                          │
    └─────────────────────────────────────────────────────────────┘

<<< 타원곡선 암호 (ECC) 구조 >>>

    [타원곡선 방정식]
    y² = x³ + ax + b (mod p)

    예시: secp256k1 (Bitcoin)
    y² = x³ + 7 (mod p)
    p = 2^256 - 2^32 - 977

    [점 덧셈 (Point Addition)]
    ┌─────────────────────────────────────────────────────────────┐
    │                                                              │
    │           • P                          • R = P + Q          │
    │          /│                              /                  │
    │         / │                             /                   │
    │        /  │                            /                    │
    │  ─────┼───┼─────x³+ax+b───────┬───────/──────              │
    │        \  │                    \    /                       │
    │         \ │                     \  /                        │
    │          \│                      \/                         │
    │           • Q                     •                         │
    │                                   (P+Q의 x좌표)             │
    │                                                              │
    │  P + Q: P와 Q를 잇는 직선이 곡선과 만나는 제3점의 대칭점   │
    │  2P: P에서의 접선이 곡선과 만나는 점의 대칭점              │
    └─────────────────────────────────────────────────────────────┘

    [ECDH 키 교환]
    ┌─────────────────────────────────────────────────────────────┐
    │  Alice                    Bob                              │
    │  ────                     ────                             │
    │  개인키 a                 개인키 b                          │
    │  공개키 A = a×G           공개키 B = b×G                    │
    │       │                       │                             │
    │       │─────── A ────────────►│                             │
    │       │◄─────── B ────────────│                             │
    │       │                       │                             │
    │  공유비밀 = a×B           공유비밀 = b×A                    │
    │           = a×(b×G)            = b×(a×G)                    │
    │           = (a×b)×G            = (b×a)×G                    │
    │           = 동일함              = 동일함                    │
    └─────────────────────────────────────────────────────────────┘
```

#### 3. 심층 동작 원리: RSA 구현

```python
import os
import secrets
from typing import Tuple, Optional
import hashlib

def gcd(a: int, b: int) -> int:
    """최대공약수 계산"""
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """확장 유클리드 알고리즘"""
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(e: int, phi: int) -> Optional[int]:
    """모듈러 역원 계산"""
    gcd_val, x, _ = extended_gcd(e % phi, phi)
    if gcd_val != 1:
        return None
    return (x % phi + phi) % phi

def is_prime(n: int, k: int = 20) -> bool:
    """Miller-Rabin 소수 판정"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # n-1 = 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # k번 테스트
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

def generate_prime(bits: int) -> int:
    """지정된 비트 수의 소수 생성"""
    while True:
        # 홀수 생성
        n = secrets.randbits(bits)
        n |= (1 << bits - 1) | 1  # 최상위 비트와 최하위 비트 설정

        if is_prime(n):
            return n

class RSA:
    """
    RSA 암호 시스템 구현
    """

    def __init__(self, key_size: int = 2048):
        """
        RSA 키 쌍 생성

        Args:
            key_size: 키 크기 (비트) - 2048, 3072, 4096 권장
        """
        self.key_size = key_size
        self.public_key, self.private_key = self._generate_keypair()

    def _generate_keypair(self) -> Tuple[Tuple[int, int], Tuple[int, int, int, int]]:
        """RSA 키 쌍 생성"""
        # 두 소수 생성
        p_bits = self.key_size // 2
        q_bits = self.key_size - p_bits

        p = generate_prime(p_bits)
        q = generate_prime(q_bits)

        while p == q:
            q = generate_prime(q_bits)

        n = p * q
        phi = (p - 1) * (q - 1)

        # 공개 지수 e (일반적으로 65537)
        e = 65537
        while gcd(e, phi) != 1:
            e += 2

        # 개인 지수 d
        d = mod_inverse(e, phi)

        # 공개키: (n, e)
        # 개인키: (n, d, p, q)
        return (n, e), (n, d, p, q)

    def encrypt(self, plaintext: bytes, public_key: Tuple[int, int] = None) -> bytes:
        """
        RSA 암호화 (PKCS#1 v1.5 패딩)

        Args:
            plaintext: 평문 (최대 key_size/8 - 11 바이트)
            public_key: 공개키 (기본값: 자신의 공개키)
        """
        if public_key is None:
            public_key = self.public_key

        n, e = public_key
        max_len = (n.bit_length() // 8) - 11

        if len(plaintext) > max_len:
            raise ValueError(f"Plaintext too long. Max: {max_len} bytes")

        # PKCS#1 v1.5 패딩
        # EM = 0x00 || 0x02 || PS || 0x00 || M
        ps_len = max_len - len(plaintext)
        ps = bytes([secrets.randbelow(254) + 1 for _ in range(ps_len)])
        padded = b'\x00\x02' + ps + b'\x00' + plaintext

        # 정수 변환 및 암호화
        m = int.from_bytes(padded, 'big')
        c = pow(m, e, n)

        # 바이트 변환
        return c.to_bytes((n.bit_length() + 7) // 8, 'big')

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        RSA 복호화

        Args:
            ciphertext: 암호문
        """
        n, d, p, q = self.private_key

        # 정수 변환 및 복호화
        c = int.from_bytes(ciphertext, 'big')
        m = pow(c, d, n)

        # 바이트 변환
        padded = m.to_bytes((n.bit_length() + 7) // 8, 'big')

        # PKCS#1 v1.5 패딩 제거
        if len(padded) < 11 or padded[0:2] != b'\x00\x02':
            raise ValueError("Invalid padding")

        # 0x00 구분자 찾기
        separator_idx = padded.index(b'\x00', 2)

        return padded[separator_idx + 1:]

    def sign(self, message: bytes, hash_algorithm: str = "sha256") -> bytes:
        """
        RSA 서명 (PKCS#1 v1.5)

        Args:
            message: 서명할 메시지
            hash_algorithm: 해시 알고리즘
        """
        n, d, p, q = self.private_key

        # 메시지 해시
        h = hashlib.new(hash_algorithm)
        h.update(message)
        digest = h.digest()

        # DigestInfo 구성 (간소화)
        # 실제로는 ASN.1 DER 인코딩 필요
        t = b'\x00\x01' + b'\xff' * ( (n.bit_length() // 8) - len(digest) - 3 )
        t += b'\x00' + digest

        # 서명
        m = int.from_bytes(t, 'big')
        s = pow(m, d, n)

        return s.to_bytes((n.bit_length() + 7) // 8, 'big')

    def verify(self,
               message: bytes,
               signature: bytes,
               public_key: Tuple[int, int] = None,
               hash_algorithm: str = "sha256") -> bool:
        """
        RSA 서명 검증
        """
        if public_key is None:
            public_key = self.public_key

        n, e = public_key

        # 서명 검증
        s = int.from_bytes(signature, 'big')
        m = pow(s, e, n)

        t = m.to_bytes((n.bit_length() + 7) // 8, 'big')

        # 메시지 해시
        h = hashlib.new(hash_algorithm)
        h.update(message)
        digest = h.digest()

        # DigestInfo에서 해시 추출 (간소화)
        if len(t) < 11 or t[0:2] != b'\x00\x01':
            return False

        try:
            separator_idx = t.index(b'\x00', 2)
            extracted_digest = t[separator_idx + 1:]
            return extracted_digest == digest
        except ValueError:
            return False

    def get_public_key_pem(self) -> str:
        """공개키 PEM 형식 반환"""
        n, e = self.public_key
        return f"-----BEGIN RSA PUBLIC KEY-----\n(n={n}, e={e})\n-----END RSA PUBLIC KEY-----"

# ECDH 간소화 구현
class EllipticCurve:
    """
    타원곡선 암호 (간소화 구현)
    secp256k1 곡선 사용
    """

    def __init__(self):
        # secp256k1 파라미터
        self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        self.a = 0
        self.b = 7
        self.n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        self.G = (
            0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
            0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        )

    def point_add(self, P: Tuple[int, int], Q: Tuple[int, int]) -> Tuple[int, int]:
        """점 덧셈"""
        if P is None:
            return Q
        if Q is None:
            return P

        x1, y1 = P
        x2, y2 = Q

        if x1 == x2:
            if y1 != y2:
                return None  # 무한원점
            # 점 배가
            lam = (3 * x1 * x1 + self.a) * pow(2 * y1, -1, self.p) % self.p
        else:
            lam = (y2 - y1) * pow(x2 - x1, -1, self.p) % self.p

        x3 = (lam * lam - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p

        return (x3, y3)

    def point_multiply(self, k: int, P: Tuple[int, int]) -> Tuple[int, int]:
        """스칼라 곱셈 (이중법)"""
        result = None
        addend = P

        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            k >>= 1

        return result

    def generate_keypair(self) -> Tuple[int, Tuple[int, int]]:
        """키 쌍 생성"""
        private_key = secrets.randbelow(self.n - 1) + 1
        public_key = self.point_multiply(private_key, self.G)
        return private_key, public_key

    def compute_shared_secret(self,
                              private_key: int,
                              public_key: Tuple[int, int]) -> int:
        """공유 비밀 계산"""
        shared_point = self.point_multiply(private_key, public_key)
        return shared_point[0] if shared_point else 0

# 사용 예시
if __name__ == "__main__":
    # 1. RSA 테스트
    print("=== RSA Encryption ===")
    rsa = RSA(key_size=2048)

    plaintext = b"Hello, RSA!"
    ciphertext = rsa.encrypt(plaintext)
    decrypted = rsa.decrypt(ciphertext)

    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext length: {len(ciphertext)} bytes")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {plaintext == decrypted}")

    # 2. RSA 서명 테스트
    print("\n=== RSA Signature ===")
    message = b"This message is signed by RSA"
    signature = rsa.sign(message)
    verified = rsa.verify(message, signature)

    print(f"Message: {message}")
    print(f"Signature length: {len(signature)} bytes")
    print(f"Verified: {verified}")

    # 변조된 메시지 검증
    tampered = b"This message is NOT signed by RSA"
    verified_tampered = rsa.verify(tampered, signature)
    print(f"Tampered message verified: {verified_tampered}")

    # 3. ECDH 테스트
    print("\n=== ECDH Key Exchange ===")
    ec = EllipticCurve()

    # Alice 키 생성
    alice_private, alice_public = ec.generate_keypair()
    print(f"Alice public key: {alice_public[0]:x[:32]}...")

    # Bob 키 생성
    bob_private, bob_public = ec.generate_keypair()
    print(f"Bob public key: {bob_public[0]:x[:32]}...")

    # 공유 비밀 계산
    alice_shared = ec.compute_shared_secret(alice_private, bob_public)
    bob_shared = ec.compute_shared_secret(bob_private, alice_public)

    print(f"Alice shared secret: {alice_shared:x[:32]}...")
    print(f"Bob shared secret: {bob_shared:x[:32]}...")
    print(f"Shared secrets match: {alice_shared == bob_shared}")
