+++
title = "RSA (Rivest-Shamir-Adleman)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# RSA (Rivest-Shamir-Adleman)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 큰 소수의 곱을 인수분해하기 어렵다는 수학적 난제에 기반한 공개키 암호 시스템으로, 암호화와 전자서명에 사용됩니다.
> 2. **가치**: PKI, TLS, 디지털 서명의 핵심 알고리즘이며, 40년 이상 전 세계 보안 인프라의 기반이었습니다.
> 3. **융합**: ECC로 대체 추세이나 여전히 레거시 호환성, 전자서명 표준(RFC 8017)에서 필수입니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**RSA**는 1977년 Ron Rivest, Adi Shamir, Leonard Adleman이 개발한 최초의 실용적 공개키 암호 시스템입니다. 두 개의 키(공개키, 개인키)를 사용하며, 그 보안성은 큰 정수의 인수분해 난이도에 의존합니다.

**핵심 수학적 원리**:
```
┌─────────────────────────────────────────────────────────────────────┐
│                    RSA 수학적 기초                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. 키 생성 (Key Generation)                                        │
│     ────────────────────────────                                    │
│     ① 두 큰 소수 p, q 선택 (각 1024비트 이상)                       │
│     ② n = p × q 계산 (모듈러스)                                     │
│     ③ φ(n) = (p-1)(q-1) 계산 (오일러 파이 함수)                     │
│     ④ e 선택: 1 < e < φ(n), gcd(e, φ(n)) = 1                       │
│        → 일반적으로 e = 65537 (0x10001) 사용                        │
│     ⑤ d 계산: d ≡ e^(-1) (mod φ(n))                                │
│        → 확장 유클리드 알고리즘 사용                                │
│                                                                     │
│     공개키: (n, e)                                                  │
│     개인키: (n, d) 또는 (p, q, d)                                   │
│                                                                     │
│  2. 암호화 (Encryption)                                             │
│     ────────────────────────                                        │
│     C = M^e mod n                                                   │
│                                                                     │
│  3. 복호화 (Decryption)                                             │
│     ────────────────────────                                        │
│     M = C^d mod n                                                   │
│                                                                     │
│  4. 전자서명 (Signature)                                            │
│     ────────────────────────                                        │
│     서명: S = M^d mod n (개인키로 서명)                             │
│     검증: M' = S^e mod n (공개키로 검증), M == M'                   │
│                                                                     │
│  5. 보안 근거                                                       │
│     ────────────────────────                                        │
│     - n을 인수분해하여 p, q를 찾으면 d를 계산 가능                  │
│     - 2048비트 n의 인수분해는 현재 계산 능력으로 불가능              │
│     - 양자 컴퓨터(Shor 알고리즘) 위협 존재                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### 2. RSA 키 길이와 보안 강도

| 키 길이 | 보안 비트 | 인수분해 복잡도 | 권장 용도 | 유효기간 |
|:---|:---|:---|:---|:---|
| **1024비트** | 80비트 | 2^80 | 사용 금지 | 만료됨 |
| **2048비트** | 112비트 | 2^112 | 일반적 용도 | ~2030년 |
| **3072비트** | 128비트 | 2^128 | 높은 보안 | ~2040년 |
| **4096비트** | 150비트 | 2^150 | 최고 보안 | 장기 |

#### 3. 비유를 통한 이해
RSA는 **'특수 자물쇠와 열쇠'**에 비유할 수 있습니다.
- **공개키(자물쇠)**: 누구나 사용 가능, 편지 봉투를 잠그는 용도
- **개인키(열쇠)**: 오직 소유자만 보관, 봉투를 여는 용도
- **소수 p, q**: 자물쇠의 비밀 구조 (알면 열쇠를 만들 수 있음)
- **n = p × q**: 자물쇠의 겉모습 (공개되어도 비밀 구조를 알기 어려움)

#### 4. 등장 배경 및 발전 과정
1. **1976년**: Diffie-Hellman 키 교환 발명 (공개키 암호 개념)
2. **1977년**: RSA 발명 (최초의 공개키 암호/서명)
3. **1983년**: RSA 특허 획득 (2000년 만료)
4. **1998년**: PKCS#1 표준화
5. **2000년대**: ECC 등장으로 일부 대체
6. **현재**: TLS, 코드 서명, 전자서명에 여전히 필수

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. RSA 연산 프로세스 다이어그램

```text
<<< RSA 키 생성 및 사용 프로세스 >>>

    ┌────────────────────────────────────────────────────────────────────────┐
    │                    RSA 키 생성 (Key Generation)                        │
    └────────────────────────────────────────────────────────────────────────┘
                                    │
    ┌────────────────────────────────────────────────────────────────────────┐
    │  ① 소수 생성                                                          │
    │  ┌────────────────────────────────────────────────────────────────┐   │
    │  │  p = random_prime(1024비트)  // 안전한 난수 생성기 사용        │   │
    │  │  q = random_prime(1024비트)  // p ≠ q, p-q가 충분히 큼         │   │
    │  │                                                                │   │
    │  │  소수 판정: Miller-Rabin 테스트 (k=64회 권장)                  │   │
    │  └────────────────────────────────────────────────────────────────┘   │
    │                              │                                         │
    │                              ▼                                         │
    │  ② 모듈러스 및 파이 함수 계산                                         │
    │  ┌────────────────────────────────────────────────────────────────┐   │
    │  │  n = p × q  // 2048비트 모듈러스                               │   │
    │  │  φ(n) = (p-1) × (q-1)  // 오일러 파이 함수                     │   │
    │  └────────────────────────────────────────────────────────────────┘   │
    │                              │                                         │
    │                              ▼                                         │
    │  ③ 공개 지수 선택                                                     │
    │  ┌────────────────────────────────────────────────────────────────┐   │
    │  │  e = 65537 (0x10001)  // 표준값, 빠른 암호화/검증              │   │
    │  │  조건: 1 < e < φ(n), gcd(e, φ(n)) = 1                          │   │
    │  └────────────────────────────────────────────────────────────────┘   │
    │                              │                                         │
    │                              ▼                                         │
    │  ④ 개인 지수 계산                                                     │
    │  ┌────────────────────────────────────────────────────────────────┐   │
    │  │  d = modular_inverse(e, φ(n))                                  │   │
    │  │  // 확장 유클리드 알고리즘                                     │   │
    │  │  // d × e ≡ 1 (mod φ(n))                                       │   │
    │  └────────────────────────────────────────────────────────────────┘   │
    │                              │                                         │
    │                              ▼                                         │
    │  ┌────────────────────────────────────────────────────────────────┐   │
    │  │  공개키: (n, e) = (모듈러스, 공개지수)                         │   │
    │  │  개인키: (n, d) = (모듈러스, 개인지수)                         │   │
    │  │           또는 (p, q, d, dP, dQ, qInv) - CRT 최적화            │   │
    │  └────────────────────────────────────────────────────────────────┘   │
    └────────────────────────────────────────────────────────────────────────┘

    ┌────────────────────────────────────────────────────────────────────────┐
    │                    RSA 암호화 (Encryption)                             │
    └────────────────────────────────────────────────────────────────────────┘

    ┌────────────────────────────────────────────────────────────────────────┐
    │  입력: 평문 M (0 ≤ M < n), 수신자 공개키 (n, e)                       │
    │                                                                        │
    │  ① 패딩 적용 (OAEP 권장)                                              │
    │     M_padded = OAEP_Encode(M, Label, Hash)                            │
    │                                                                        │
    │  ② 모듈러 거듭제곱                                                     │
    │     C = M_padded^e mod n                                               │
    │     // Square-and-Multiply 알고리즘                                    │
    │     // 또는 Sliding Window, Montgomery Reduction                      │
    │                                                                        │
    │  출력: 암호문 C                                                        │
    └────────────────────────────────────────────────────────────────────────┘

    ┌────────────────────────────────────────────────────────────────────────┐
    │                    RSA 복호화 (Decryption)                             │
    └────────────────────────────────────────────────────────────────────────┘

    ┌────────────────────────────────────────────────────────────────────────┐
    │  입력: 암호문 C, 개인키 (n, d) 또는 (p, q, dP, dQ, qInv)              │
    │                                                                        │
    │  ① 모듈러 거듭제곱 (CRT 최적화)                                        │
    │     M1 = C^dP mod p                                                    │
    │     M2 = C^dQ mod q                                                    │
    │     h = qInv × (M1 - M2) mod p                                         │
    │     M_padded = M2 + h × q                                              │
    │                                                                        │
    │  ② 패딩 제거 (OAEP)                                                    │
    │     M = OAEP_Decode(M_padded, Label, Hash)                             │
    │                                                                        │
    │  출력: 평문 M                                                          │
    └────────────────────────────────────────────────────────────────────────┘
```

#### 2. RSA 패딩 스킴 비교

| 패딩 | 설명 | 보안 | 용도 | 상태 |
|:---|:---|:---|:---|:---|
| **PKCS#1 v1.5** | 구형 표준 패딩 | 취약(Bleichenbacher) | 레거시 | 사용 권장 안 함 |
| **OAEP** | Optimal Asymmetric Encryption Padding | 안전 | 암호화 | 권장 |
| **PSS** | Probabilistic Signature Scheme | 안전 | 서명 | 권장 |
| **None (교과서 RSA)** | 패딩 없음 | 매우 취약 | - | 절대 금지 |

#### 3. Python 구현: RSA (개념적)

```python
import random
from typing import Tuple, Optional
import hashlib

def gcd(a: int, b: int) -> int:
    """최대공약수"""
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """확장 유클리드 알고리즘: (gcd, x, y) where ax + by = gcd"""
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(a: int, m: int) -> int:
    """모듈러 역원: a^(-1) mod m"""
    gcd_val, x, _ = extended_gcd(a % m, m)
    if gcd_val != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % m + m) % m

def is_prime_miller_rabin(n: int, k: int = 64) -> bool:
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
        a = random.randrange(2, n - 1)
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
        # 상위 비트와 하위 비트를 1로 설정
        p = random.getrandbits(bits)
        p |= (1 << (bits - 1)) | 1

        if is_prime_miller_rabin(p):
            return p

class RSA:
    """RSA 암호 시스템 (교육용 구현)"""

    def __init__(self, key_size: int = 2048):
        """RSA 키 생성"""
        self.key_size = key_size
        self.e = 65537  # 표준 공개 지수

        # 키 생성
        self._generate_keys()

    def _generate_keys(self):
        """키 쌍 생성"""
        # 두 소수 생성
        p_bits = self.key_size // 2
        q_bits = self.key_size - p_bits

        print(f"Generating {p_bits}-bit prime p...")
        self.p = generate_prime(p_bits)
        print(f"Generating {q_bits}-bit prime q...")
        self.q = generate_prime(q_bits)

        # p와 q가 충분히 다른지 확인
        while abs(self.p - self.q) < 2 ** (self.key_size // 2 - 100):
            self.q = generate_prime(q_bits)

        # 모듈러스 및 파이 함수
        self.n = self.p * self.q
        self.phi_n = (self.p - 1) * (self.q - 1)

        # 개인 지수
        self.d = mod_inverse(self.e, self.phi_n)

        # CRT 파라미터 (최적화)
        self.dP = self.d % (self.p - 1)
        self.dQ = self.d % (self.q - 1)
        self.qInv = mod_inverse(self.q, self.p)

        print(f"RSA-{self.key_size} keys generated successfully")

    @property
    def public_key(self) -> Tuple[int, int]:
        """공개키 반환"""
        return (self.n, self.e)

    @property
    def private_key(self) -> Tuple[int, int]:
        """개인키 반환"""
        return (self.n, self.d)

    def encrypt(self, plaintext: bytes) -> bytes:
        """암호화 (교과서 RSA - 실제로는 OAEP 필수)"""
        # 정수로 변환
        m = int.from_bytes(plaintext, 'big')

        if m >= self.n:
            raise ValueError("Message too long")

        # 암호화: c = m^e mod n
        c = pow(m, self.e, self.n)

        # 바이트로 변환
        return c.to_bytes((self.n.bit_length() + 7) // 8, 'big')

    def decrypt(self, ciphertext: bytes) -> bytes:
        """복호화 (CRT 최적화)"""
        c = int.from_bytes(ciphertext, 'big')

        # CRT 복호화
        m1 = pow(c, self.dP, self.p)
        m2 = pow(c, self.dQ, self.q)
        h = (self.qInv * (m1 - m2)) % self.p
        m = m2 + h * self.q

        # 바이트로 변환
        byte_len = (m.bit_length() + 7) // 8
        return m.to_bytes(max(1, byte_len), 'big')

    def sign(self, message: bytes) -> bytes:
        """전자서명 (교과서 RSA - 실제로는 PSS 필수)"""
        # 해시
        h = hashlib.sha256(message).digest()
        h_int = int.from_bytes(h, 'big')

        # 서명: s = h^d mod n
        s = pow(h_int, self.d, self.n)

        return s.to_bytes((self.n.bit_length() + 7) // 8, 'big')

    def verify(self, message: bytes, signature: bytes) -> bool:
        """서명 검증"""
        s = int.from_bytes(signature, 'big')

        # 검증: h' = s^e mod n
        h_int = pow(s, self.e, self.n)

        # 실제 해시
        h = hashlib.sha256(message).digest()
        expected_h = int.from_bytes(h, 'big')

        return h_int == expected_h


# OAEP 패딩 (개념적)
class OAEP:
    """OAEP 패딩 (Optimal Asymmetric Encryption Padding)"""

    def __init__(self, hash_func=hashlib.sha256):
        self.hash_func = hash_func
        self.hash_len = hash_func().digest_size

    def _mgf1(self, seed: bytes, mask_len: int) -> bytes:
        """MGF1 (Mask Generation Function)"""
        mask = b''
        counter = 0

        while len(mask) < mask_len:
            c = counter.to_bytes(4, 'big')
            mask += self.hash_func(seed + c).digest()
            counter += 1

        return mask[:mask_len]

    def encode(self, message: bytes, k: int, label: bytes = b'') -> bytes:
        """OAEP 인코딩"""
        h_len = self.hash_len

        # 1. 길이 확인
        max_msg_len = k - 2 * h_len - 2
        if len(message) > max_msg_len:
            raise ValueError("Message too long")

        # 2. lHash = Hash(L)
        l_hash = self.hash_func(label).digest()

        # 3. PS (패딩 문자열)
        ps = b'\x00' * (max_msg_len - len(message))

        # 4. DB = lHash || PS || 0x01 || M
        db = l_hash + ps + b'\x01' + message

        # 5. 랜덤 seed
        seed = random.randbytes(h_len)

        # 6. dbMask = MGF(seed, k-h_len-1)
        db_mask = self._mgf1(seed, k - h_len - 1)

        # 7. maskedDB = DB XOR dbMask
        masked_db = bytes([db[i] ^ db_mask[i] for i in range(len(db))])

        # 8. seedMask = MGF(maskedDB, h_len)
        seed_mask = self._mgf1(masked_db, h_len)

        # 9. maskedSeed = seed XOR seedMask
        masked_seed = bytes([seed[i] ^ seed_mask[i] for i in range(len(seed))])

        # 10. EM = 0x00 || maskedSeed || maskedDB
        em = b'\x00' + masked_seed + masked_db

        return em

    def decode(self, encoded: bytes, k: int, label: bytes = b'') -> bytes:
        """OAEP 디코딩"""
        h_len = self.hash_len

        # 1. 길이 확인
        if len(encoded) != k or k < 2 * h_len + 2:
            raise ValueError("Decoding error")

        # 2. EM 파싱
        masked_seed = encoded[1:1 + h_len]
        masked_db = encoded[1 + h_len:]

        # 3. seedMask = MGF(maskedDB, h_len)
        seed_mask = self._mgf1(masked_db, h_len)

        # 4. seed = maskedSeed XOR seedMask
        seed = bytes([masked_seed[i] ^ seed_mask[i] for i in range(len(masked_seed))])

        # 5. dbMask = MGF(seed, k-h_len-1)
        db_mask = self._mgf1(seed, k - h_len - 1)

        # 6. DB = maskedDB XOR dbMask
        db = bytes([masked_db[i] ^ db_mask[i] for i in range(len(masked_db))])

        # 7. DB 파싱
        l_hash = self.hash_func(label).digest()

        if db[:h_len] != l_hash:
            raise ValueError("Decoding error")

        # 메시지 추출
        i = h_len
        while i < len(db) and db[i] == 0:
            i += 1

        if i >= len(db) or db[i] != 0x01:
            raise ValueError("Decoding error")

        return db[i + 1:]


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("RSA 암호 시스템 (교육용 구현)")
    print("=" * 60)

    # 키 생성 (테스트용 1024비트)
    print("\n[1] 키 생성 (1024비트 - 테스트용)")
    rsa = RSA(key_size=1024)

    print(f"\n공개키 (n, e):")
    print(f"  n = {rsa.public_key[0]}")
    print(f"  e = {rsa.public_key[1]}")

    # 암호화/복호화 테스트
    print("\n[2] 암호화/복호화 테스트")
    message = b"Hello, RSA!"
    print(f"평문: {message}")

    ciphertext = rsa.encrypt(message)
    print(f"암호문: {ciphertext.hex()[:64]}...")

    decrypted = rsa.decrypt(ciphertext)
    print(f"복호문: {decrypted}")
    print(f"일치: {message == decrypted}")

    # 서명/검증 테스트
    print("\n[3] 서명/검증 테스트")
    signature = rsa.sign(message)
    print(f"서명: {signature.hex()[:64]}...")

    verified = rsa.verify(message, signature)
    print(f"검증: {'성공' if verified else '실패'}")

    # 변조된 메시지 검증
    tampered = message + b"!"
    verified_tampered = rsa.verify(tampered, signature)
    print(f"변조 메시지 검증: {'성공' if verified_tampered else '실패 (정상)'}")

    print("\n" + "=" * 60)
    print("주의: 실제 사용 시 반드시 OAEP/PSS 패딩 적용 필수!")
    print("권장 키 크기: 2048비트 이상")
    print("=" * 60)
```

---

### III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. RSA vs ECC 비교

| 특성 | RSA-2048 | ECC P-256 |
|:---|:---|:---|
| **키 크기** | 2048비트 | 256비트 |
| **서명 크기** | 256바이트 | 64바이트 |
| **보안 강도** | 112비트 | 128비트 |
| **암호화 속도** | 빠름 (공개키) | 느림 |
| **복호화 속도** | 느림 (개인키) | 빠름 |
| **서명 속도** | 느림 (개인키) | 빠름 |
| **키 생성** | 느림 | 빠름 |
| **TLS 사용** | 감소 추세 | 증가 추세 |

#### 2. RSA 활용 영역

| 영역 | RSA 활용 | 대안 |
|:---|:---|:---|
| **TLS/SSL** | 키 교환, 서명 | ECDHE, ECDSA |
| **코드 서명** | Authenticode | ECDSA |
| **S/MIME** | 암호화, 서명 | ECDSA, ECDH |
| **SSH** | 키 교환 | Ed25519, ECDH |
| **PGP** | 암호화, 서명 | Curve25519 |
| **JWT** | 서명 | ECDSA, EdDSA |

#### 3. 과목 융합 관점 분석
- **PKI**: 인증서 서명, 키 교환
- **전자서명법**: RSA-PSS 기반 전자서명
- **금융보안**: 공인인증서, 전자뱅킹
- **클라우드**: SSH 키, 암호화 키 랩핑
- **블록체인**: 계정 키, 트랜잭션 서명

---

### IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 레거시 시스템 호환성**
- 상황: 10년 된 시스템, RSA-1024 사용 중
- 판단: RSA-2048 이상으로 마이그레이션 필수
- 이유: 1024비트는 이미 취약, 2030년까지 2048비트 유효

**시나리오 2: 신규 PKI 구축**
- 상황: 새로운 기업 PKI 설계
- 판단: RSA-4096 또는 ECC P-384 혼합 사용
- 이유: 레거시 호환(RSA) + 성능(ECC)

**시나리오 3: IoT 디바이스 인증**
- 상황: 제한된 리소스, 저전력
- 판단: ECC (P-256 또는 Ed25519) 권장
- 이유: RSA는 키/서명 크기가 크고 느림

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] 키 길이 2048비트 이상 선택
- [ ] OAEP 암호화 패딩 사용
- [ ] PSS 서명 패딩 사용
- [ ] 안전한 난수 생성기 사용
- [ ] 개인키 안전 저장 (HSM 권장)
- [ ] 정기적 키 교체 (2년 권장)

#### 3. 안티패턴 (Anti-patterns)
- **교과서 RSA**: 패딩 없이 직접 사용 → 위험
- **PKCS#1 v1.5**: Bleichenbacher 공격 취약
- **작은 지수 e=3**: Coppersmith 공격 취약
- **공통 모듈러스**: 동일 n 사용 → 키 복구 가능

---

### V. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | 내용 | 비고 |
|:---|:---|:---|
| 상호 운용성 | 40년+ 표준, 광범위 지원 | 모든 시스템 호환 |
| 레거시 호환 | 기존 시스템과의 호환성 | 마이그레이션 여유 |
| 보안 | 2048비트 이상 시 안전 | 2030년까지 유효 |
| 성능 | 암호화는 빠름, 복호화는 느림 | 용도에 따라 선택 |

#### 2. 미래 전망 및 진화 방향
- **ECC로 대체**: TLS 1.3에서 ECDHE/ECDSA 선호
- **양자 위협**: Shor 알고리즘으로 RSA 깨짐
- **PQC 전환**: 2030년까지 양자 내성 암호로 이관
- **하이브리드**: RSA + PQC 혼합 체계

#### 3. 참고 표준/가이드
- **RFC 8017**: PKCS#1 v2.2 (RSA 표준)
- **FIPS 186-5**: 디지털 서명 표준
- **NIST SP 800-56B**: RSA 키 교환
- **RFC 8446**: TLS 1.3

---

### 관련 개념 맵 (Knowledge Graph)
- [비대칭키 암호](@/studynotes/09_security/02_crypto/asymmetric_encryption.md) : RSA의 상위 개념
- [PKI](@/studynotes/09_security/01_policy/pki.md) : RSA 기반 인증 기반 구조
- [ECC](@/studynotes/09_security/02_crypto/encryption_algorithms.md) : RSA의 대안
- [전자서명](@/studynotes/09_security/02_crypto/encryption_algorithms.md) : RSA-PSS
- [TLS](@/studynotes/09_security/03_network/network_security_systems.md) : RSA 사용 프로토콜

---

### 어린이를 위한 3줄 비유 설명
1. **자물쇠와 열쇠**: 누구나 쓸 수 있는 자물쇠(공개키)를 나눠주고, 열쇠(개인키)는 나만 가져요.
2. **비밀 곱셈**: 두 개의 엄청 큰 비밀 숫자를 곱해서 만든 문제예요. 그 숫자들을 알면 열쇠를 만들 수 있어요.
3. **서명**: 내 열쇠로 문서에 도장을 찍으면, 자물쇠로 누가 찍었는지 확인할 수 있어요.
