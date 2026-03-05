+++
title = "Diffie-Hellman / ECDH 키 교환"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# Diffie-Hellman / ECDH 키 교환

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 두 당사자가 공개 채널에서 대칭키를 안전하게 합의할 수 있는 최초의 공개키 암호학적 프로토콜로, 이산대수 문제(DH) 또는 타원곡선 이산대수 문제(ECDH)의 어려움에 기반합니다.
> 2. **가치**: 매 연결마다 새로운 세션 키를 생성하여 전방 비밀성(PFS)을 달성하며, TLS, VPN, SSH 등 모든 보안 통신의 기반 기술입니다.
> 3. **융합**: ECDH는 동등 보안 강도에서 DH 대비 10배 작은 키로 효율성을 달성하며, 모바일/IoT 환경과 하이브리드 암호 시스템의 핵심 구성요소입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**Diffie-Hellman(DH) 키 교환**은 1976년 Whitfield Diffie와 Martin Hellman이 발표한 혁신적인 프로토콜로, 두 당사자가 비밀 채널 없이도 공유 비밀키를 생성할 수 있게 합니다. **ECDH(Elliptic Curve Diffie-Hellman)**는 DH의 타원곡선 변형으로, 더 적은 비트 수로 동등한 보안을 제공합니다.

```
핵심 원리: 일방향 함수 (One-way Function)
- 정방향: g^a mod p 계산 → 쉬움 (O(log a))
- 역방향: g^x ≡ A (mod p)에서 x 찾기 → 어려움 (Discrete Logarithm Problem)

ECDH 원리:
- 정방향: k × G = P 계산 → 쉬움
- 역방향: P = k × G에서 k 찾기 → 어려움 (Elliptic Curve DLP)
```

#### 2. 비유를 통한 이해
DH 키 교환은 **'혼합 색상 만들기'**에 비유할 수 있습니다.
- **공개 값**: 노란색 (공통 베이스)
- **Alice의 비밀**: 빨간색
- **Bob의 비밀**: 파란색
- **교환**: Alice는 노란+빨간=주황색, Bob은 노란+파란=초록색을 서로 공개
- **공통 비밀**: 각자 자신의 비밀 색을 더하면 둘 다 노란+빨강+파랑=갈색이 됨
- **공격자**: 주황과 초록만 보고 갈색을 만들 수 없음

#### 3. 등장 배경 및 발전 과정
1. **1976년**: Diffie-Hellman "New Directions in Cryptography" 논문 발표
2. **1978년**: RSA 발표 전까지 유일한 공개키 방식
3. **1985년**: Neal Koblitz, Victor Miller가 타원곡선 암호(ECC) 제안
4. **1990년대**: DSA(Digital Signature Algorithm)에 DH 변형 사용
5. **2000년대**: ECDH가 TLS, SSH에 도입
6. **2010년대**: NSA Suite B, TLS 1.3에서 ECDHE 필수화
7. **현재**: PQC(양자내성암호)로 진화 중

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. DH/ECDH 구성 요소 상세 분석

| 요소 | DH (Classic) | ECDH | 역할 | 보안 요구사항 |
|:---|:---|:---|:---|:---|
| **그룹** | Z_p^* (소수 순환군) | 타원곡선 점군 | 연산 기반 | 충분한 크기 |
| **생성원** | g (primitive root) | G (기준점) | 공개 베이스 | 높은 위수 |
| **비밀키** | a, b ∈ {1, ..., p-1} | d_A, d_B ∈ {1, ..., n-1} | 각자의 비밀 | 난수성 |
| **공개키** | A = g^a mod p | P_A = d_A × G | 상대방에게 전송 | 인증 필요 |
| **공유 비밀** | K = g^(ab) mod p | K = d_A × P_B = d_B × P_A | 세션 키 유도 | 유일성 |

#### 2. DH 키 교환 프로토콜 다이어그램

```
=== 기본 Diffie-Hellman 키 교환 ===

         Alice                                    Bob
           │                                        │
           │    ┌─────────────────────┐            │
           │    │  공개 파라미터       │            │
           │    │  p (큰 소수)         │            │
           │    │  g (생성원)          │            │
           │    └─────────────────────┘            │
           │                                        │
           │  a ← Random(1, p-1)                   │  b ← Random(1, p-1)
           │                                        │
           │  A = g^a mod p                         │  B = g^b mod p
           │                                        │
           │───────────── A ─────────────────────►│
           │                                        │
           │◄──────────── B ──────────────────────│
           │                                        │
           │  K = B^a mod p                         │  K = A^b mod p
           │  = (g^b)^a mod p                       │  = (g^a)^b mod p
           │  = g^(ab) mod p                        │  = g^(ab) mod p
           │                                        │
           │         🎉 동일한 K 획득! 🎉           │

===========================================

=== ECDH (Elliptic Curve DH) 키 교환 ===

         Alice                                    Bob
           │                                        │
           │    ┌─────────────────────┐            │
           │    │  공개 파라미터       │            │
           │    │  Curve: secp256r1   │            │
           │    │  G: 기준점           │            │
           │    │  n: G의 위수         │            │
           │    └─────────────────────┘            │
           │                                        │
           │  d_A ← Random(1, n-1)                 │  d_B ← Random(1, n-1)
           │                                        │
           │  P_A = d_A × G                         │  P_B = d_B × G
           │  (타원곡선 상의 점)                    │  (타원곡선 상의 점)
           │                                        │
           │─────────── P_A ─────────────────────►│
           │                                        │
           │◄────────── P_B ──────────────────────│
           │                                        │
           │  K = d_A × P_B                         │  K = d_B × P_A
           │  = d_A × (d_B × G)                     │  = d_B × (d_A × G)
           │  = (d_A × d_B) × G                     │  = (d_B × d_A) × G
           │                                        │
           │         🎉 동일한 K 획득! 🎉           │

===========================================

=== Ephemeral DH (DHE/ECDHE) - Perfect Forward Secrecy ===

         Alice                                    Bob
           │                                        │
           │  세션마다 새로운 a 생성                 │  세션마다 새로운 b 생성
           │  (Ephemeral = 일시적)                  │
           │                                        │
           │  a_1 ← Random()                        │  b_1 ← Random()
           │  A_1 = g^a_1 mod p                     │  B_1 = g^b_1 mod p
           │                                        │
           │──────────── A_1 ─────────────────────►│
           │◄─────────── B_1 ──────────────────────│
           │                                        │
           │  K_1 = g^(a_1*b_1) mod p               │
           │                                        │
           │  ⏰ 시간 경과, 새 세션                  │
           │                                        │
           │  a_2 ← Random()  ← 새로운 키!          │  b_2 ← Random()
           │  A_2 = g^a_2 mod p                     │  B_2 = g^b_2 mod p
           │                                        │
           │──────────── A_2 ─────────────────────►│
           │◄─────────── B_2 ──────────────────────│
           │                                        │
           │  K_2 = g^(a_2*b_2) mod p               │
           │                                        │
           │  🔒 K_1 노출되어도 K_2 안전!           │
           │     → Perfect Forward Secrecy          │
```

#### 3. 심층 동작 원리: ECDH 구현

```python
import os
import hashlib
from dataclasses import dataclass
from typing import Tuple, Optional

# 실제 구현은 cryptography 라이브러리 사용 권장
# 이 코드는 교육용 단순화된 구현

@dataclass
class EllipticCurvePoint:
    """타원곡선 상의 점 (y^2 = x^3 + ax + b mod p)"""
    x: int
    y: int
    curve: 'EllipticCurve'

    def is_infinity(self) -> bool:
        return self.x is None and self.y is None

    @classmethod
    def infinity(cls, curve: 'EllipticCurve') -> 'EllipticCurvePoint':
        return cls(None, None, curve)


class EllipticCurve:
    """
    타원곡선 정의: y^2 = x^3 + ax + b (mod p)

    보안에 사용되는 곡선:
    - secp256r1 (P-256): NIST 표준
    - secp384r1 (P-384): 높은 보안
    - Curve25519: 현대적, 안전한 구현
    """

    def __init__(self, a: int, b: int, p: int, n: int, G: Tuple[int, int]):
        self.a = a
        self.b = b
        self.p = p  # 소수 modulus
        self.n = n  # 기준점 G의 위수 (order)
        self.G = EllipticCurvePoint(G[0], G[1], self)

    def point_add(self, P: EllipticCurvePoint, Q: EllipticCurvePoint) -> EllipticCurvePoint:
        """
        타원곡선 점 덧셈: P + Q

        기하학적 의미:
        - P, Q를 지나는 직선이 곡선과 만나는 세 번째 점의 대칭점
        - P = Q인 경우 접선 사용 (점 doubling)
        """
        if P.is_infinity():
            return Q
        if Q.is_infinity():
            return P

        if P.x == Q.x and P.y != Q.y:
            # P = -Q인 경우
            return EllipticCurvePoint.infinity(self)

        if P == Q:
            # 점 doubling: 2P
            # λ = (3x_1^2 + a) / (2y_1) mod p
            lam = ((3 * P.x * P.x + self.a) * pow(2 * P.y, -1, self.p)) % self.p
        else:
            # 일반 덧셈: P + Q
            # λ = (y_2 - y_1) / (x_2 - x_1) mod p
            lam = ((Q.y - P.y) * pow(Q.x - P.x, -1, self.p)) % self.p

        x_3 = (lam * lam - P.x - Q.x) % self.p
        y_3 = (lam * (P.x - x_3) - P.y) % self.p

        return EllipticCurvePoint(x_3, y_3, self)

    def scalar_mult(self, k: int, P: EllipticCurvePoint) -> EllipticCurvePoint:
        """
        스칼라 곱셈: k × P = P + P + ... + P (k번)

        Double-and-Add 알고리즘 (O(log k)):
        - 이진 표현을 이용한 효율적 계산
        - 타원곡선 암호의 핵심 연산
        """
        if k == 0 or P.is_infinity():
            return EllipticCurvePoint.infinity(self)

        if k < 0:
            k = -k
            P = EllipticCurvePoint(P.x, (-P.y) % self.p, self)

        result = EllipticCurvePoint.infinity(self)
        addend = P

        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            k >>= 1

        return result


# secp256r1 (P-256) 곡선 정의
SECP256R1 = EllipticCurve(
    a=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC,
    b=0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B,
    p=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF,
    n=0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551,
    G=(
        0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
        0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5
    )
)


class ECDHKeyExchange:
    """
    ECDH 키 교환 구현

    보안 고려사항:
    1. 비밀키는 안전한 난수 생성기로 생성
    2. 공개키는 반드시 검증 후 사용
    3. 공유 비밀은 KDF를 통해 세션 키로 변환
    4. 일회성 키 사용으로 PFS 달성 (ECDHE)
    """

    def __init__(self, curve: EllipticCurve = SECP256R1):
        self.curve = curve

    def generate_keypair(self) -> Tuple[int, EllipticCurvePoint]:
        """개인키/공개키 쌍 생성"""
        # 안전한 난수로 개인키 생성
        private_key = int.from_bytes(os.urandom(32), 'big') % self.curve.n
        while private_key < 1:
            private_key = int.from_bytes(os.urandom(32), 'big') % self.curve.n

        # 공개키 = d × G
        public_key = self.curve.scalar_mult(private_key, self.curve.G)

        return private_key, public_key

    def compute_shared_secret(self, private_key: int,
                              other_public_key: EllipticCurvePoint) -> bytes:
        """공유 비밀 계산: K = d_A × P_B"""
        shared_point = self.curve.scalar_mult(private_key, other_public_key)

        if shared_point.is_infinity():
            raise ValueError("Invalid shared secret (point at infinity)")

        # x좌표를 공유 비밀로 사용 (33/65바이트 형식도 가능)
        return shared_point.x.to_bytes(32, 'big')

    def derive_session_key(self, shared_secret: bytes,
                          context_info: bytes = b"") -> bytes:
        """
        HKDF를 통한 세션 키 유도

        공유 비밀을 직접 사용하지 않고 KDF를 거쳐야 함:
        - 비트 보존 방지
        - 키 분리 (Key Separation)
        - 문맥 바인딩
        """
        # HKDF-Extract (salt가 없으면 zeros 사용)
        prk = hashlib.sha256(b'\x00' * 32 + shared_secret).digest()

        # HKDF-Expand
        info = b'tls13 derived' + context_info
        okm = hashlib.sha256(prk + b'\x01' + info).digest()

        return okm

    def validate_public_key(self, public_key: EllipticCurvePoint) -> bool:
        """
        공개키 검증 (필수!)

        공격 방지:
        - Invalid curve attack
        - Small subgroup attack
        - Twist attack
        """
        if public_key.is_infinity():
            return False

        # 점이 곡선 위에 있는지 확인
        left = pow(public_key.y, 2, self.curve.p)
        right = (pow(public_key.x, 3, self.curve.p) +
                 self.curve.a * public_key.x +
                 self.curve.b) % self.curve.p

        if left != right:
            return False

        # n × P = ∞ 확인 (small subgroup attack 방지)
        n_times_p = self.curve.scalar_mult(self.curve.n, public_key)
        if not n_times_p.is_infinity():
            return False

        return True


# DH (Classic) 구현
class DHKeyExchange:
    """
    기본 Diffie-Hellman 키 교환

    권장 파라미터 (RFC 3526):
    - MODP 2048-bit Group (Group 14)
    - MODP 3072-bit Group (Group 15)
    - MODP 4096-bit Group (Group 16)
    """

    # RFC 3526 2048-bit Group
    MODP_2048_P = int(
        "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
        "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
        "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
        "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
        "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D"
        "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
        "83655D23DCA3AD961C62F356208552BB9ED529077096966D"
        "670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
        "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9"
        "DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
        "15728E5A8AACAA68FFFFFFFFFFFFFFFF", 16)

    MODP_2048_G = 2

    def __init__(self, p: int = MODP_2048_P, g: int = MODP_2048_G):
        self.p = p
        self.g = g

    def generate_keypair(self) -> Tuple[int, int]:
        """개인키/공개키 쌍 생성"""
        # 2048비트 개인키
        private_key = int.from_bytes(os.urandom(256), 'big') % (self.p - 2) + 2
        public_key = pow(self.g, private_key, self.p)
        return private_key, public_key

    def compute_shared_secret(self, private_key: int, other_public_key: int) -> bytes:
        """공유 비밀 계산"""
        shared_secret = pow(other_public_key, private_key, self.p)
        return shared_secret.to_bytes(256, 'big')


# 사용 예시
def ecdh_demo():
    """ECDH 키 교환 데모"""
    ecdh = ECDHKeyExchange()

    # Alice 키 생성
    alice_private, alice_public = ecdh.generate_keypair()
    print(f"Alice 공개키: ({hex(alice_public.x)[:20]}..., {hex(alice_public.y)[:20]}...)")

    # Bob 키 생성
    bob_private, bob_public = ecdh.generate_keypair()
    print(f"Bob 공개키: ({hex(bob_public.x)[:20]}..., {hex(bob_public.y)[:20]}...)")

    # 공개키 검증
    assert ecdh.validate_public_key(alice_public)
    assert ecdh.validate_public_key(bob_public)

    # 공유 비밀 계산
    alice_shared = ecdh.compute_shared_secret(alice_private, bob_public)
    bob_shared = ecdh.compute_shared_secret(bob_private, alice_public)

    # 동일한지 확인
    assert alice_shared == bob_shared
    print(f"공유 비밀 일치! {alice_shared.hex()[:32]}...")

    # 세션 키 유도
    session_key = ecdh.derive_session_key(alice_shared)
    print(f"세션 키: {session_key.hex()}")


if __name__ == "__main__":
    ecdh_demo()
```

#### 4. DH vs ECDH 비교 분석

| 특성 | DH (2048-bit) | ECDH (P-256) | 비고 |
|:---|:---:|:---:|:---|
| **공개키 크기** | 256 bytes | 64 bytes | ECDH 4배 작음 |
| **공유 비밀 크기** | 256 bytes | 32 bytes | |
| **키 생성 시간** | ~2ms | ~0.2ms | ECDH 10배 빠름 |
| **스칼라 곱셈** | - | O(log n) | 효율적 |
| **모듈러 거듭제곱** | O(log n) | - | 느림 |
| **보안 비트** | 112-bit | 128-bit | ECDH 더 강함 |
| **메모리 사용** | 높음 | 낮음 | IoT에 유리 |

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. DH 변형 비교표

| 변형 | 설명 | PFS | 용도 | 보안 등급 |
|:---|:---|:---:|:---|:---|
| **DH (Static)** | 고정 키 쌍 사용 | X | 레거시, 키 래핑 | 낮음 |
| **DHE (Ephemeral)** | 일회성 키 쌍 | O | TLS 1.2 | 양호 |
| **ECDH (Static)** | 타원곡선 고정 키 | X | 코드 서명 | 양호 |
| **ECDHE (Ephemeral)** | 타원곡선 일회성 | O | TLS 1.3 필수 | 최상 |

#### 2. 곡선 선택 가이드

| 곡선 | 보안 비트 | 성능 | 용도 | 비고 |
|:---|:---:|:---:|:---|:---|
| **secp256r1 (P-256)** | 128 | 빠름 | 일반 용도 | NIST 표준 |
| **secp384r1 (P-384)** | 192 | 중간 | 높은 보안 | 정부/군사 |
| **Curve25519** | 128 | 최상 | 현대적 권장 | safe curve |
| **Curve448** | 224 | 느림 | 초고보안 | Goldilocks |
| **secp256k1** | 128 | 빠름 | 비트코인 | Koblitz 곡선 |

#### 3. 과목 융합 관점 분석

**네트워크 보안과 융합**
- TLS 1.3: ECDHE 필수, DH/Static 금지
- IPsec: IKEv2에서 ECDH 그룹 지원
- WireGuard: Curve25519 전용

**암호학과 융합**
- 하이브리드 암호: DH/ECDH로 대칭키 교환, AES-GCM으로 데이터 암호화
- KEM/DEM 패러다임: Key Encapsulation + Data Encapsulation

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: TLS 1.2 → 1.3 마이그레이션**
- 상황: 레거시 시스템에서 RSA 키 교환 사용 중
- 판단: ECDHE로 전환 필요
- 전략:
  1. ECDHE 지원 서버 설정
  2. P-256 또는 Curve25519 선택
  3. 클라이언트 호환성 테스트

**시나리오 2: IoT 디바이스 키 교환**
- 상황: 제한된 CPU(ARM Cortex-M0), 저전력
- 판단: Curve25519 또는 X25519
- 이유: constant-time 구현, 작은 코드 크기

**시나리오 3: 고보안 금융 시스템**
- 상황: 10년 이상 장기 보안 요구
- 판단: ECDHE + P-384 또는 하이브리드 PQC
- 이유: 양자 컴퓨팅 대비

#### 2. 도입 시 고려사항 (체크리스트)

**기술적 체크리스트**
- [ ] 곡선/그룹 선택 (NIST vs Safe Curves)
- [ ] PFS 요구사항 확인
- [ ] 공개키 검증 구현
- [ ] KDF 선택 (HKDF-SHA256 등)

**운영 체크리스트**
- [ ] 키 캐싱 정책 (session ticket)
- [ ] 키 로깅 방지
- [ ] 타임아웃 및 재협상

#### 3. 안티패턴 (Anti-patterns)

```
취약한 구현 (금지!)

1. 정적 DH 사용 (PFS 없음)
   ❌ server_dh_private 고정 사용
   → 장기 키 노출 시 모든 과거 세션 복호화 가능

2. 공개키 검증 생략
   ❌ shared = private * received_point  # 검증 없이
   → Invalid Curve Attack 취약

3. 작은 그룹 사용
   ❌ DH 1024-bit 그룹
   → 80비트 보안만 제공, 현대적 기준 부족

4. 공유 비밀 직접 사용
   ❌ aes_key = shared_secret[:16]
   → KDF 없이 비트 누출 위험

올바른 구현:

1. Ephemeral 키 사용
   ✓ dh = ECDHKeyExchange()
   ✓ private, public = dh.generate_keypair()  # 매 세션 새로 생성

2. 공개키 검증
   ✓ if not dh.validate_public_key(received_public):
   ✓     raise InvalidKeyError()

3. KDF 적용
   ✓ shared_secret = dh.compute_shared_secret(private, received_public)
   ✓ session_key = hkdf(shared_secret, salt, info, 32)
```

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 | 항목 | 수치/내용 |
|:---|:---|:---|
| **전방 비밀성** | 과거 세션 보호 | 장기 키 노출 시도 과거 복호화 불가 |
| **성능** | 핸드쉐이크 시간 | ECDHE: ~10ms (vs RSA: ~50ms) |
| **대역폭** | 메시지 크기 | ECDH: 64 bytes (vs DH: 256 bytes) |
| **컴플라이언스** | 표준 준수 | PCI DSS 4.0, TLS 1.3 |

#### 2. 미래 전망 및 진화 방향

```
하이브리드 키 교환 (Post-Quantum Transition)
├── Classic + PQC 결합
│   ├── X25519 + CRYSTALS-Kyber
│   └── ECDHE + NTRU
├── TLS 1.3 확장
│   └── RFC 9370: Multiple Key Shares
└── 점진적 마이그레이션
    └── 레거시 호환성 유지

양자 시대 대응
├── "Harvest Now, Decrypt Later" 위협
├── 2024-2030: 하이브리드 전환기
└── 2030+: PQC 단독 사용
```

#### 3. 참고 표준/가이드

| 표준 | 내용 |
|:---|:---|
| **RFC 3526** | MODP 그룹 (DH용 소수) |
| **RFC 5903** | ECP 그룹 (ECDH용 곡선) |
| **RFC 7748** | Curve25519, Curve448 |
| **RFC 8446** | TLS 1.3 (ECDHE 필수) |
| **NIST SP 800-56A** | DH/ECDH 권장사항 |
| **RFC 9370** | Multiple Key Shares (PQC 하이브리드) |

---

### 관련 개념 맵 (Knowledge Graph)
- [대칭키 암호](@/studynotes/09_security/02_crypto/symmetric_encryption.md) : DH로 교환한 키로 데이터 암호화
- [ECC (타원곡선 암호)](@/studynotes/09_security/02_crypto/ecc.md) : ECDH의 수학적 기반
- [전방 비밀성 (PFS)](@/studynotes/09_security/02_crypto/pfs.md) : Ephemeral DH의 핵심 보안 속성
- [TLS 1.3](@/studynotes/09_security/03_network/tls13.md) : ECDHE 필수 사용 프로토콜
- [키 관리](@/studynotes/09_security/02_crypto/key_management.md) : DH 키의 수명 주기 관리

---

### 어린이를 위한 3줄 비유 설명
1. **비밀 암호 만들기**: 두 친구가 공개적으로 대화하면서도 둘만 아는 비밀 암호를 만들 수 있어요. 각자 비밀 숫자를 선택하고, 섞인 결과만 주고받아요.
2. **색 섞기**: 노란색에 내 비밀 색(빨강)을 섞어 주황색을 만들고, 친구는 노란색에 파란색을 섞어 초록색을 만들어요. 서로의 색에 다시 내 비밀 색을 섞으면 둘 다 갈색이 돼요!
3. **도둑이 몰라요**: 도둑은 주황색과 초록색만 봐서는 갈색을 만들 수 없어요. 우리의 비밀 색을 모르니까요. 이게 바로 안전한 키 교환입니다!
