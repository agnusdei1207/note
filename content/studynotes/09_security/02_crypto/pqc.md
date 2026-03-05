+++
title = "양자 내성 암호 (PQC, Post-Quantum Cryptography)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# 양자 내성 암호 (PQC, Post-Quantum Cryptography)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 양자 컴퓨터의 Shor 알고리즘에 의해 깨지는 RSA, ECC 등 기존 공개키 암호를 대체하기 위해 개발된 새로운 암호 알고리즘들로, 격자(Lattice), 해시(Hash), 부호(Code), 다변수(Multivariate) 등의 수학적 난제에 기반합니다.
> 2. **가치**: 2024년 NIST PQC 표준화 완료로 CRYSTALS-Kyber (KEM), CRYSTALS-Dilithium, FALCON, SPHINCS+ (서명)이 선정되었으며, "Harvest Now, Decrypt Later" 위협의 유일한 대응책입니다.
> 3. **융합**: TLS, VPN, PKI, 블록체인 등 모든 공개키 인프라에 점진적 마이그레이션이 필요하며, 하이브리드 모드(기존 + PQC)로 전환 기간을 안전하게 관리합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**양자 내성 암호(Post-Quantum Cryptography, PQC)**는 양자 컴퓨터의 공격에도 안전한 암호 알고리즘들을 말합니다. 1994년 Peter Shor가 발견한 양자 알고리즘은 다항 시간에 소인수분해와 이산대수문제를 해결할 수 있어, RSA와 ECC를 완전히 무력화합니다.

```
양자 컴퓨터의 암호 공격 능력:
┌─────────────────┬───────────────┬────────────────┐
│ 암호 시스템     │ 고전 컴퓨터   │ 양자 컴퓨터    │
├─────────────────┼───────────────┼────────────────┤
│ RSA-2048        │ 2^112 연산    │ 2^40 연산      │
│ ECC P-256       │ 2^128 연산    │ 2^40 연산      │
│ AES-256         │ 2^256 연산    │ 2^128 연산     │
│ SHA-256         │ 2^128 충돌    │ 2^64 충돌      │
└─────────────────┴───────────────┴────────────────┘
→ RSA, ECC는 완전 붕괴
→ AES, SHA는 키 길이 2배로 대응 가능
```

#### 2. 비유를 통한 이해
PQC는 **'양자 지갑'**에 비유할 수 있습니다.

- **기존 암호 (RSA/ECC)**: 일반 자물쇠
  - 일반 도둑(고전 컴퓨터)은 못 열지만
  - 마법 도구(양자 컴퓨터)가 있으면 1초에 열림
- **양자 내성 암호 (PQC)**: 특수 자물쇠
  - 마법 도구로도 열기 어려움
  - 새로운 종류의 잠금 장치

#### 3. 등장 배경 및 발전 과정
1. **1994년**: Shor 알고리즘 발견 (양자 소인수분해)
2. **1996년**: Grover 알고리즘 (양자 검색)
3. **2006년**: PQCrypto 학회 시작
4. **2012년**: NSA "Suite B" 암호 알고리즘 전환 권고 철회
5. **2015년**: NSA PQC 전환 발표
6. **2016년**: NIST PQC 표준화 공모 시작 (82개 후보)
7. **2020년**: 7개 최종 후보 선정
8. **2022년**: 4개 알고리즘 최종 선정
9. **2024년**: FIPS 203, 204, 205 발표 (공식 표준)
10. **2030년 예상**: 양자 컴퓨터 실용화, PQC 의무화

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. PQC 알고리즘 분류

| 범주 | 수학적 기반 | 장점 | 단점 | 대표 알고리즘 |
|:---|:---|:---|:---|:---|
| **격자 (Lattice)** | 최단 벡터 문제 | 효율적, 다양한 기능 | 큰 키/서명 | Kyber, Dilithium |
| **해시 (Hash)** | 충돌 저항성 | 단순, 검증됨 | 큰 서명 | SPHINCS+ |
| **부호 (Code)** | 디코딩 문제 | 빠른 암호화 | 큰 키 | Classic McEliece |
| **다변수** | MQ 문제 | 작은 서명 | 큰 키, 안전성 논란 | Rainbow (탈락) |
| **동형** | 격자 기반 | 완전 동형 암호 | 매우 느림 | FHE |

#### 2. NIST PQC 표준 알고리즘

| 알고리즘 | 용도 | FIPS | 기반 | 공개키 | 서명/암호문 | 보안 레벨 |
|:---|:---|:---|:---|:---:|:---:|:---|
| **ML-KEM (Kyber)** | KEM | 203 | Lattice | 1,188 B | 1,088 B | Level 1-5 |
| **ML-DSA (Dilithium)** | 서명 | 204 | Lattice | 1,312 B | 2,420 B | Level 2-5 |
| **FN-DSA (FALCON)** | 서명 | 206 | Lattice | 897 B | 666 B | Level 1-5 |
| **SLH-DSA (SPHINCS+)** | 서명 | 205 | Hash | 32 B | 7,856 B | Level 1-5 |

#### 3. 격자 기반 암호 (Lattice-based) 원리

```
=== Lattice (격자) 기반 암호 원리 ===

격자(Lattice)란?
- n차원 공간에서 규칙적으로 배치된 점들의 집합
- 기저 벡터 B = {b1, b2, ..., bn}의 정수 선형 결합

     ↑
   4 │     ●     ●     ●     ●
     │
   3 │     ●     ●     ●     ●
     │
   2 │     ●     ●     ●     ●   격자 점들
     │
   1 │     ●     ●     ●     ●
     │
   0 └──────────────────────────→
     0     1     2     3     4

최단 벡터 문제 (SVP, Shortest Vector Problem):
- 격자에서 0이 아닌 가장 짧은 벡터를 찾는 문제
- NP-hard로 알려진 어려운 문제
- 양자 컴퓨터로도 다항 시간 해결 불가

Learning With Errors (LWE):
- 격자 기반 암호의 핵심 문제
- b = A·s + e (mod q)
  - A: 공개 행렬
  - s: 비밀 벡터
  - e: 작은 오차 벡터
  - b: 공개 벡터
- A, b가 주어졌을 때 s를 찾는 것은 어려움

===========================================

=== CRYSTALS-Kyber (ML-KEM) 구조 ===

Key Generation:
┌─────────────────────────────────────────────┐
│ 1. A ← Random Matrix (k × k, mod q)         │
│ 2. s, e ← Random Small Vectors              │
│ 3. t = A·s + e (mod q)                      │
│                                             │
│ Public Key: (A, t)                          │
│ Private Key: s                              │
└─────────────────────────────────────────────┘

Encapsulation (KEM):
┌─────────────────────────────────────────────┐
│ Input: Public Key (A, t)                    │
│                                             │
│ 1. r, e1, e2 ← Random Small Vectors         │
│ 2. u = A^T·r + e1 (mod q)                   │
│ 3. v = t^T·r + e2 (mod q)                   │
│ 4. KDF로 키 유도                            │
│                                             │
│ Output: (u, v) = Ciphertext, Key            │
└─────────────────────────────────────────────┘

Decapsulation:
┌─────────────────────────────────────────────┐
│ Input: Ciphertext (u, v), Private Key s     │
│                                             │
│ 1. m' = v - s^T·u (mod q)                   │
│ 2. KDF로 키 복구                            │
│                                             │
│ Output: Key                                 │
└─────────────────────────────────────────────┘

===========================================

=== CRYSTALS-Dilithium (ML-DSA) 구조 ===

Signing:
┌─────────────────────────────────────────────┐
│ 1. y ← Random Mask                         │
│ 2. w = A·y (mod q)                          │
│ 3. c = H(message || w)                      │
│ 4. z = y + c·s                              │
│ 5. Bound Check (z, r)                       │
│    - |z|∞ < γ1 - β                          │
│    - |r|∞ < γ2 - β                          │
│    - 실패 시 1로                            │
│                                             │
│ Output: (z, c)                              │
└─────────────────────────────────────────────┘

Verification:
┌─────────────────────────────────────────────┐
│ 1. w' = A·z - c·t                           │
│ 2. c' = H(message || w')                    │
│ 3. Return c == c'                           │
└─────────────────────────────────────────────┘
```

#### 4. 심층 동작 원리: Kyber KEM 구현

```python
"""
CRYSTALS-Kyber (ML-KEM) 개념적 구현

실제 구현은 최적화된 C/Assembly 사용
Python은 교육용 단순화
"""

import hashlib
import os
from dataclasses import dataclass
from typing import Tuple, List
import struct

# Kyber 파라미터 (Kyber-768)
K = 3  # 격자 차원
Q = 3329  # 모듈러스
N = 256  # 다항식 차수
ETA1 = 2  # 비밀 분포 표준편차
ETA2 = 2
DU = 10  # 압축 파라미터
DV = 4


@dataclass
class Polynomial:
    """다항식 (N개의 계수)"""
    coeffs: List[int]

    @staticmethod
    def random_poly(n: int, eta: int) -> 'Polynomial':
        """중심 이항 분포에서 샘플링"""
        coeffs = []
        for _ in range(N):
            # CBD (Centered Binomial Distribution)
            a = sum(os.urandom(1)[0] & 1 for _ in range(2 * eta))
            b = sum((os.urandom(1)[0] >> 1) & 1 for _ in range(2 * eta))
            coeffs.append(a - b)
        return Polynomial(coeffs)

    @staticmethod
    def random_matrix(k: int, n: int, q: int) -> List[List['Polynomial']]:
        """랜덤 행렬 A 생성"""
        matrix = []
        for i in range(k):
            row = []
            for j in range(k):
                # XOF에서 유도 (실제로는 SHAKE)
                coeffs = [struct.unpack('<H', os.urandom(2))[0] % q for _ in range(n)]
                row.append(Polynomial(coeffs))
            matrix.append(row)
        return matrix

    def __add__(self, other: 'Polynomial') -> 'Polynomial':
        return Polynomial([(a + b) % Q for a, b in zip(self.coeffs, other.coeffs)])

    def __sub__(self, other: 'Polynomial') -> 'Polynomial':
        return Polynomial([(a - b) % Q for a, b in zip(self.coeffs, other.coeffs)])

    def __mul__(self, other: 'Polynomial') -> 'Polynomial':
        """다항식 곱셈 (NTT 도메인에서는 단순 계수 곱)"""
        # 실제로는 NTT(Number Theoretic Transform) 사용
        result = [0] * N
        for i in range(N):
            for j in range(N):
                result[(i + j) % N] = (result[(i + j) % N] +
                                       self.coeffs[i] * other.coeffs[j]) % Q
        return Polynomial(result)

    def compress(self, d: int) -> 'Polynomial':
        """압축: d 비트로 표현"""
        scale = (1 << d)
        return Polynomial([round(c * scale / Q) % scale for c in self.coeffs])

    def decompress(self, d: int) -> 'Polynomial':
        """복원"""
        scale = (1 << d)
        return Polynomial([round(c * Q / scale) for c in self.coeffs])


@dataclass
class KyberPublicKey:
    """Kyber 공개키"""
    t: List[Polynomial]  # k개의 다항식
    rho: bytes  # 시드 (A 생성용)

    def encode(self) -> bytes:
        """공개키 인코딩"""
        data = b''
        for poly in self.t:
            for c in poly.coeffs:
                data += struct.pack('<H', c)
        data += self.rho
        return data


@dataclass
class KyberPrivateKey:
    """Kyber 개인키"""
    s: List[Polynomial]  # 비밀 벡터

    def encode(self) -> bytes:
        """개인키 인코딩"""
        data = b''
        for poly in self.s:
            for c in poly.coeffs:
                data += struct.pack('<H', c % (2**12))  # 12비트
        return data


@dataclass
class KyberCiphertext:
    """Kyber 암호문"""
    u: List[Polynomial]  # k개의 다항식
    v: Polynomial  # 1개의 다항식

    def encode(self) -> bytes:
        """암호문 인코딩"""
        data = b''
        for poly in self.u:
            for c in poly.compress(DU).coeffs:
                data += struct.pack('<H', c)
        for c in self.v.compress(DV).coeffs:
            data += struct.pack('B', c)
        return data


class KyberKEM:
    """
    CRYSTALS-Kyber KEM (Key Encapsulation Mechanism)

    NIST FIPS 203 표준
    """

    def __init__(self, k: int = 3):
        """
        Args:
            k: 보안 파라미터 (2, 3, 5)
               k=2: Kyber-512 (AES-128 상당)
               k=3: Kyber-768 (AES-192 상당)
               k=5: Kyber-1024 (AES-256 상당)
        """
        self.k = k

    def keygen(self) -> Tuple[KyberPublicKey, KyberPrivateKey]:
        """
        키 쌍 생성

        1. A ← Random k×k matrix (공개)
        2. s, e ← CBD 샘플링 (비밀)
        3. t = A·s + e (mod q)
        4. pk = (A, t), sk = s
        """
        # 랜덤 시드 생성
        rho = os.urandom(32)  # A 생성용
        sigma = os.urandom(32)  # s, e 생성용

        # 행렬 A 생성
        A = Polynomial.random_matrix(self.k, N, Q)

        # 비밀 벡터 s
        s = [Polynomial.random_poly(N, ETA1) for _ in range(self.k)]

        # 오차 벡터 e
        e = [Polynomial.random_poly(N, ETA1) for _ in range(self.k)]

        # t = A·s + e 계산
        t = []
        for i in range(self.k):
            ti = Polynomial([0] * N)
            for j in range(self.k):
                # 다항식 곱셈 (실제로는 NTT)
                prod = s[j]  # 단순화
                ti = ti + prod
            ti = ti + e[i]
            t.append(ti)

        pk = KyberPublicKey(t=t, rho=rho)
        sk = KyberPrivateKey(s=s)

        return pk, sk

    def encaps(self, pk: KyberPublicKey) -> Tuple[KyberCiphertext, bytes]:
        """
        키 캡슐화

        1. r, e1, e2 ← 샘플링
        2. u = A^T·r + e1
        3. v = t^T·r + e2 + encode(m)
        4. K = KDF(m, u, v)
        5. ct = (u, v)
        """
        # 랜덤 메시지 m
        m = os.urandom(32)

        # r, e1, e2 샘플링
        r = [Polynomial.random_poly(N, ETA1) for _ in range(self.k)]
        e1 = [Polynomial.random_poly(N, ETA2) for _ in range(self.k)]
        e2 = Polynomial.random_poly(N, ETA2)

        # u = A^T·r + e1 (단순화)
        u = []
        for i in range(self.k):
            ui = Polynomial([0] * N)
            for j in range(self.k):
                ui = ui + r[j]  # 실제로는 A^T와 행렬 곱
            ui = ui + e1[i]
            u.append(ui)

        # v = t^T·r + e2 + encode(m)
        v = Polynomial([0] * N)
        for i in range(self.k):
            v = v + pk.t[i]  # 단순화
        v = v + e2

        # 암호문
        ct = KyberCiphertext(u=u, v=v)

        # 키 유도
        shared_key = hashlib.sha3_256(m + ct.encode()).digest()

        return ct, shared_key

    def decaps(self, ct: KyberCiphertext, sk: KyberPrivateKey) -> bytes:
        """
        키 복구

        1. m' = v - s^T·u
        2. K = KDF(m', u, v)
        """
        # m' = v - s^T·u (단순화)
        m_prime = ct.v
        for i in range(self.k):
            m_prime = m_prime - sk.s[i]  # 실제로는 s^T·u

        # 키 유도
        shared_key = hashlib.sha3_256(
            b"recovered_key" + ct.encode()
        ).digest()

        return shared_key


# 하이브리드 키 교환 (Classic + PQC)
class HybridKEM:
    """
    하이브리드 KEM: ECDH + Kyber

    두 키 교환을 병행하여 수행
    - 하나만 깨져도 안전
    - 전환 기간 동안 보안 보장
    """

    def __init__(self):
        self.kyber = KyberKEM(k=3)

    def hybrid_keygen(self) -> Tuple[dict, dict]:
        """
        하이브리드 키 쌍 생성

        Returns:
            (ec_keypair, kyber_keypair)
        """
        # ECDH 키 (실제로는 cryptography 라이브러리)
        ec_private = os.urandom(32)
        ec_public = hashlib.sha256(ec_private).digest()

        # Kyber 키
        kyber_pk, kyber_sk = self.kyber.keygen()

        return (
            {'ec_private': ec_private, 'ec_public': ec_public},
            {'kyber_pk': kyber_pk, 'kyber_sk': kyber_sk}
        )

    def hybrid_encaps(self, ec_pk: bytes, kyber_pk: KyberPublicKey) -> Tuple[dict, bytes]:
        """
        하이브리드 캡슐화

        두 키 교환의 결과를 결합:
        K = KDF(ECDH_shared || Kyber_shared)
        """
        # ECDH (시뮬레이션)
        ec_shared = hashlib.sha256(ec_pk + b"ecdh").digest()

        # Kyber
        kyber_ct, kyber_shared = self.kyber.encaps(kyber_pk)

        # 결합
        combined_key = hashlib.sha3_256(ec_shared + kyber_shared).digest()

        ciphertext = {
            'ec_ciphertext': b"ec_ct_placeholder",
            'kyber_ciphertext': kyber_ct.encode()
        }

        return ciphertext, combined_key


# 사용 예시
def pqc_demo():
    """PQC 데모"""
    print("=" * 60)
    print("CRYSTALS-Kyber (ML-KEM) 데모")
    print("=" * 60)

    # 키 생성
    kyber = KyberKEM(k=3)
    pk, sk = kyber.keygen()

    print(f"\n[Key Generation]")
    print(f"  공개키 크기: {len(pk.encode())} bytes")
    print(f"  개인키 크기: {len(sk.encode())} bytes")

    # 캡슐화
    ct, shared_key_enc = kyber.encaps(pk)
    print(f"\n[Encapsulation]")
    print(f"  암호문 크기: {len(ct.encode())} bytes")
    print(f"  공유 키: {shared_key_enc.hex()[:32]}...")

    # 복구
    shared_key_dec = kyber.decaps(ct, sk)
    print(f"\n[Decapsulation]")
    print(f"  복구된 키: {shared_key_dec.hex()[:32]}...")

    # 하이브리드 데모
    print("\n" + "=" * 60)
    print("하이브리드 (ECDH + Kyber) 데모")
    print("=" * 60)

    hybrid = HybridKEM()
    ec_keys, kyber_keys = hybrid.hybrid_keygen()

    print(f"\n[Hybrid Keys Generated]")
    print(f"  ECDH 공개키: {ec_keys['ec_public'].hex()[:32]}...")
    print(f"  Kyber 공개키: {len(kyber_keys['kyber_pk'].encode())} bytes")


def security_comparison():
    """보안 비교표"""
    print("\n" + "=" * 60)
    print("PQC vs 기존 암호 보안 비교")
    print("=" * 60)

    algorithms = [
        ("RSA-2048", "소인수분해", 112, "취약 (Shor)"),
        ("ECC P-256", "ECDLP", 128, "취약 (Shor)"),
        ("Kyber-768", "격자 (LWE)", 192, "안전"),
        ("Dilithium3", "격자 (LWE)", 192, "안전"),
        ("SPHINCS+-256s", "해시", 256, "안전"),
    ]

    print(f"\n{'알고리즘':<15} {'수학적 기반':<15} {'보안 비트':<10} {'양자 내성'}")
    print("-" * 60)
    for name, basis, bits, quantum in algorithms:
        print(f"{name:<15} {basis:<15} {bits:<10} {quantum}")


if __name__ == "__main__":
    pqc_demo()
    security_comparison()
```

#### 5. PQC 마이그레이션 전략

```
=== PQC 마이그레이션 단계 ===

Phase 1: 평가 및 계획 (2024-2025)
├── 현재 암호 사용 현황 파악
├── 장기 기밀 데이터 식별
├── PQC 도입 로드맵 수립
└── 하드웨어/소프트웨어 호환성 확인

Phase 2: 하이브리드 전환 (2025-2027)
├── TLS: ECDHE + Kyber 하이브리드
├── 서명: ECDSA + Dilithium 하이브리드
├── 인증서: Dual 인증서 발급
└── 테스트 환경 구축

Phase 3: PQC 우선 (2027-2030)
├── PQC를 기본, 기존 알고리즘 폴백
├── 레거시 시스템 격리
└── 운영 경험 축적

Phase 4: PQC 단독 (2030+)
├── 기존 RSA/ECC 비활성화
├── PQC만 사용
└── 양자 컴퓨터 실용화 대비
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. PQC 알고리즘 비교

| 알고리즘 | 용도 | 공개키 | 암호문/서명 | 속도 | 권장 용도 |
|:---|:---|:---:|:---:|:---:|:---|
| **Kyber-768** | KEM | 1,188B | 1,088B | 빠름 | TLS, VPN |
| **Dilithium3** | 서명 | 1,952B | 3,293B | 빠름 | 인증서, 코드서명 |
| **FALCON-512** | 서명 | 897B | 666B | 중간 | 작은 서명 필요시 |
| **SPHINCS+-128s** | 서명 | 32B | 7,856B | 느림 | 하드웨어 단순 |

#### 2. 하이브리드 vs 단독 비교

| 특성 | 하이브리드 | PQC 단독 |
|:---|:---:|:---:|
| **양자 전 보안** | O | O |
| **양자 후 보안** | O | O |
| **복잡성** | 높음 | 낮음 |
| **오버헤드** | 높음 | 중간 |
| **전환 기간** | 필수 | 최종 목표 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 금융 PKI PQC 전환**
- 상황: 장기 인증서 (10년), 높은 보안 요구
- 판단: 2025년부터 하이브리드 인증서 발급
- 전략:
  1. Dilithium + ECDSA 이중 서명
  2. 2027년부터 Dilithium 단독 옵션

**시나리오 2: IoT 디바이스**
- 상황: 제한된 CPU, 메모리
- 판단: Kyber (KEM) 우선 도입
- 이유: 작은 암호문, 빠른 연산

#### 2. 도입 시 고려사항 (체크리스트)

**기술적 체크리스트**
- [ ] PQC 라이브러리 선택 (liboqs, Open Quantum Safe)
- [ ] 하이브리드 모드 구현
- [ ] 성능 테스트 (지연 시간, 처리량)
- [ ] 키/서명 크기 영향 평가

**운영 체크리스트**
- [ ] 마이그레이션 계획 수립
- [ ] 레거시 호환성 유지
- [ ] 모니터링 체계 구축

#### 3. 안티패턴 (Anti-patterns)

```
취약한 접근 (금지!)

1. PQC 미도입
   ❌ "양자 컴퓨터는 아직 멀었다"
   → Harvest Now, Decrypt Later 위험

2. 단독 PQC 즉시 도입
   ❌ Kyber만 사용
   → 구현 버그, 알고리즘 취약점 발견 시 대안 없음

3. 하이브리드 없이 전환
   ❌ 기존 알고리즘 즉시 제거
   → 호환성 문제, 서비스 중단

올바른 접근:

1. 하이브리드 전환
   ✓ ECDHE + Kyber (TLS)
   ✓ ECDSA + Dilithium (서명)

2. 점진적 마이그레이션
   ✓ 테스트 → 스테이징 → 프로덕션

3. 모니터링
   ✓ 성능, 호환성, 보안 지표 추적
```

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 | 항목 | 수치/내용 |
|:---|:---|:---|
| **양자 내성** | Shor 알고리즘 | 영향 없음 |
| **장기 보안** | 20년+ | 데이터 보호 |
| **표준 준수** | NIST FIPS | 203, 204, 205 |
| **미래 대비** | 2030+ | 양자 시대 준비 |

#### 2. 미래 전망

```
PQC 진화
├── 2024-2025: NIST 표준 완료, 라이브러리 안정화
├── 2025-2027: 하이브리드 배포, 테스트
├── 2027-2030: PQC 우선, 레거시 폴백
└── 2030+: PQC 단독, 양자 컴퓨터 실용화
```

#### 3. 참고 표준/가이드

| 표준 | 내용 |
|:---|:---|
| **FIPS 203** | ML-KEM (Kyber) |
| **FIPS 204** | ML-DSA (Dilithium) |
| **FIPS 205** | SLH-DSA (SPHINCS+) |
| **FIPS 206** | FN-DSA (FALCON) |
| **NIST SP 800-208** | PQC 권고사항 |

---

### 관련 개념 맵 (Knowledge Graph)
- [전방 비밀성 (PFS)](@/studynotes/09_security/02_crypto/pfs.md) : PQC와 결합한 하이브리드
- [디지털 서명](@/studynotes/09_security/02_crypto/digital_signature.md) : PQC 서명 알고리즘
- [TLS 1.3](@/studynotes/09_security/03_network/tls13.md) : PQC 확장
- [PKI](@/studynotes/09_security/10_pki/pki.md) : PQC 인증서
- [HSM](@/studynotes/09_security/02_crypto/hsm.md) : PQC 키 보호

---

### 어린이를 위한 3줄 비유 설명
1. **마법 열쇠**: 지금의 자물쇠는 특별한 마법 열쇠(양자 컴퓨터)로 열릴 수 있어요. 하지만 새로운 자물쇠(PQC)는 마법으로도 안 열려요!
2. **새로운 비밀번호**: 비밀번호를 더 어렵게 만드는 게 아니에요. 완전히 다른 종류의 비밀번호를 쓰는 거예요.
3. **미리 준비**: 나쁜 사람들이 마법 열쇠를 갖기 전에 미리 자물쇠를 바꿔야 해요. 그게 바로 양자 내성 암호예요!
