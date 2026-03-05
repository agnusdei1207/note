+++
title = "ECC (타원 곡선 암호학)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# ECC (Elliptic Curve Cryptography)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ECC는 타원 곡선(Elliptic Curve) 위의 이산 로그 문제(ECDLP)의 어려움을 기반으로 하는 공개키 암호 시스템으로, RSA 대비 1/8~1/12 키 길이로 동등 보안 강도를 제공합니다.
> 2. **가치**: 모바일/IoT 기기, TLS 1.3, 블록체인, 디지털 서명에서 핵심적 역할을 하며, 계산 효율성과 대역폭 절약으로 현대 보안의 표준이 되었습니다.
> 3. **융합**: ECDSA, ECDH, EdDSA, ECIES 등의 프로토콜로 확장되며, Bitcoin(secp256k1), TLS(P-256, P-384), SSH(ed25519)에广泛하게 사용됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**타원 곡선 (Elliptic Curve)**
- **Weierstrass 형식**: y² = x³ + ax + b (4a³ + 27b² ≠ 0)
- **유한체 위에서 정의**: Fp (소수 p) 또는 F2^m
- **점 덧셈(Point Addition)**: P + Q = R (기하학적 연산)
- **스칼라 곱셈(Scalar Multiplication)**: k × P = P + P + ... + P (k번)

**ECC 보안 기반: ECDLP**
- **타원 곡선 이산 로그 문제 (ECDLP)**: P와 Q = k×P가 주어졌을 때 k를 찾는 것은 계산적으로 어려움
- **보안 강도**: n비트 곡선은 n/2비트 대칭키와 동등

**표준 곡선**
| 곡선 | 키 길이 | 용도 | 특징 |
|:---|:---|:---|:---|
| **P-256 (secp256r1)** | 256비트 | TLS, 일반 용도 | NIST 표준 |
| **P-384** | 384비트 | 정부, 고보안 | NIST 표준 |
| **P-521** | 521비트 | 최고 보안 | NIST 표준 |
| **secp256k1** | 256비트 | Bitcoin, Ethereum | Koblitz 곡선 |
| **Curve25519** | 255비트 | 키 교환 (X25519) | Daniel J. Bernstein |
| **Ed25519** | 255비트 | 서명 (EdDSA) | Daniel J. Bernstein |

#### 2. 비유를 통한 이해
ECC는 **'비밀 경로 찾기'**에 비유할 수 있습니다:

```
RSA: 큰 숫자의 소인수분해
[거대한 숫자] → [두 소수를 찾으세요] → (어려움)

ECC: 타원 곡선 위에서의 비밀 경로
[시작점 P] → [k번 점프해서 도착점 Q] → [k를 맞추세요] → (어려움)

핵심: 암호화는 쉽고(점프), 복호화는 어려움(역추적)
```

타원 곡선 시각화 (단순화):
```
        y
        │     ●        ●
        │   ●    ●  ●    ●
        │  ●      ●●      ●
    ────┼──────────────────── x
        │         ●●
        │        ●  ●
        │       ●    ●
        │      ●      ●
```

#### 3. 등장 배경 및 발전 과정

| 연도 | 사건 | 의미 |
|:---|:---|:---|
| **1985** | Koblitz, Miller 제안 | 타원 곡선 암호 독립 제안 |
| **1992** | ANSI X9.62 | ECDSA 표준화 |
| **1999** | NIST FIPS 186-2 | ECDSA 디지털 서명 표준 |
| **2000** | NSA Suite B | ECC 기반 암호 제품군 |
| **2005** | DNSSEC | ECC 옵션 추가 |
| **2009** | Bitcoin | secp256k1 사용 |
| **2013** | Snowden 사건 | NSA 백도어 의혹으로 NIST 곡선 불신 |
| **2014** | Apple, Google | P-256 → Curve25519/Ed25519 전환 |
| **2016** | TLS 1.3 | ECDHE 필수, RSA 제거 |
| **2018** | NIST Post-Quantum | PQC 표준화 시작 (ECC 대체 준비) |

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 타원 곡선 수학 기초

```text
                [ 타원 곡선 위의 연산 ]

1. 점 덧셈 (Point Addition): P + Q = R
   - P와 Q를 지나는 직선 그리기
   - 곡선과의 세 번째 교점 찾기
   - x축 대칭으로 반전 → R

2. 점 배가 (Point Doubling): P + P = 2P
   - P에서의 접선 그리기
   - 곡선과의 두 번째 교점 찾기
   - x축 대칭으로 반전 → 2P

3. 스칼라 곱셈 (Scalar Multiplication): k × P
   - Double-and-Add 알고리즘
   - 예: 13 × P = 8P + 4P + P
     = 2(2(2(2P))) + 2(2P) + P

                    y
                    │         ●
                    │      ●     ●R
                    │    ●    P●───┼───●Q
                    │   ●      ╲   │ ╱
                    │  ●        ╲  │╱
                ────┼─────────────●───────── x
                    │            ╱│
                    │           ╱ │
                    │          ╱  │
                    │         ╱   │
                    │        ●    │

                [ Double-and-Add 알고리즘 ]

입력: k (스칼라), P (점)
출력: k × P

k를 이진수로 표현: k = (bn-1 ... b1 b0)2
결과 = O (무한원점)
for i from n-1 down to 0:
    결과 = 결과 + 결과  (Doubling)
    if bi == 1:
        결과 = 결과 + P  (Addition)
return 결과

시간 복잡도: O(log k) ≈ O(n)
```

#### 2. ECC vs RSA 키 길이 비교

| 보안 강도 | RSA 키 | ECC 키 | 비율 |
|:---|:---|:---|:---|
| 80비트 | 1024 | 160 | 6.4:1 |
| 112비트 | 2048 | 224 | 9.1:1 |
| 128비트 | 3072 | 256 | 12:1 |
| 192비트 | 7680 | 384 | 20:1 |
| 256비트 | 15360 | 512 | 30:1 |

#### 3. 주요 ECC 알고리즘

```text
┌─────────────────────────────────────────────────────────────────┐
│                        ECC 알고리즘 체계                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [ 키 교환 ]                    [ 디지털 서명 ]                 │
│                                                                 │
│  ┌───────────────┐              ┌───────────────┐              │
│  │    ECDH       │              │    ECDSA      │              │
│  │ (Diffie-Hell- │              │ (Digital Sig- │              │
│  │  man on ECC)  │              │  nature Alg)  │              │
│  └───────┬───────┘              └───────┬───────┘              │
│          │                              │                       │
│          ▼                              ▼                       │
│  ┌───────────────┐              ┌───────────────┐              │
│  │   X25519      │              │    EdDSA      │              │
│  │ (Curve25519   │              │ (Ed25519,     │              │
│  │  기반 DH)     │              │  Ed448)       │              │
│  └───────────────┘              └───────────────┘              │
│                                                                 │
│  [ 암호화 ]                                                     │
│                                                                 │
│  ┌───────────────┐                                              │
│  │    ECIES      │                                              │
│  │ (Integrated   │                                              │
│  │  Encryption   │                                              │
│  │  Scheme)      │                                              │
│  └───────────────┘                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 4. ECDSA 서명 알고리즘

```python
import secrets
from typing import Tuple

class EllipticCurve:
    """타원 곡선 정의 (Weierstrass 형식)"""

    def __init__(self, a: int, b: int, p: int, G: Tuple[int, int], n: int):
        """
        Args:
            a, b: 곡선 계수 (y² = x³ + ax + b)
            p: 유한체 소수
            G: 생성점 (generator point)
            n: 생성점의 위수 (order)
        """
        self.a = a
        self.b = b
        self.p = p
        self.Gx, self.Gy = G
        self.n = n

    def point_add(self, P: Tuple[int, int], Q: Tuple[int, int]) -> Tuple[int, int]:
        """점 덧셈: P + Q"""
        if P is None:
            return Q
        if Q is None:
            return P

        x1, y1 = P
        x2, y2 = Q

        if x1 == x2:
            if y1 != y2:  # P + (-P) = O
                return None
            if y1 == 0:   # 접선이 수직
                return None
            # 점 배가 (Point Doubling)
            lam = (3 * x1 * x1 + self.a) * pow(2 * y1, -1, self.p)
        else:
            # 일반 덧셈
            lam = (y2 - y1) * pow(x2 - x1, -1, self.p)

        lam %= self.p
        x3 = (lam * lam - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p

        return (x3, y3)

    def scalar_mult(self, k: int, P: Tuple[int, int]) -> Tuple[int, int]:
        """스칼라 곱셈: k × P (Double-and-Add)"""
        result = None
        addend = P

        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            k >>= 1

        return result

    def is_on_curve(self, P: Tuple[int, int]) -> bool:
        """점 P가 곡선 위에 있는지 확인"""
        if P is None:
            return True
        x, y = P
        return (y * y - x * x * x - self.a * x - self.b) % self.p == 0


# P-256 (secp256r1) 곡선 정의
P256 = EllipticCurve(
    a=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC,
    b=0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B,
    p=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF,
    G=(
        0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
        0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5
    ),
    n=0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
)


class ECDSA:
    """ECDSA 디지털 서명 알고리즘"""

    def __init__(self, curve: EllipticCurve):
        self.curve = curve

    def generate_keypair(self) -> Tuple[int, Tuple[int, int]]:
        """
        키 쌍 생성

        Returns:
            (private_key, public_key)
        """
        # 개인키: 1 < d < n 인 난수
        private_key = secrets.randbelow(self.curve.n - 1) + 1

        # 공개키: Q = d × G
        public_key = self.curve.scalar_mult(private_key, (self.curve.Gx, self.curve.Gy))

        return private_key, public_key

    def sign(self, private_key: int, message_hash: int) -> Tuple[int, int]:
        """
        서명 생성

        Args:
            private_key: 개인키 d
            message_hash: 메시지 해시 e

        Returns:
            (r, s) 서명
        """
        n = self.curve.n

        while True:
            # 1. 난수 k 선택 (1 < k < n)
            k = secrets.randbelow(n - 1) + 1

            # 2. 점 계산: (x1, y1) = k × G
            point = self.curve.scalar_mult(k, (self.curve.Gx, self.curve.Gy))
            if point is None:
                continue
            x1, _ = point

            # 3. r = x1 mod n
            r = x1 % n
            if r == 0:
                continue

            # 4. s = k⁻¹(e + dr) mod n
            k_inv = pow(k, -1, n)
            s = (k_inv * (message_hash + private_key * r)) % n
            if s == 0:
                continue

            return (r, s)

    def verify(self, public_key: Tuple[int, int], message_hash: int,
               signature: Tuple[int, int]) -> bool:
        """
        서명 검증

        Args:
            public_key: 공개키 Q
            message_hash: 메시지 해시 e
            signature: (r, s)

        Returns:
            검증 성공 여부
        """
        r, s = signature
        n = self.curve.n

        # 1. r, s 범위 확인
        if not (1 <= r < n and 1 <= s < n):
            return False

        # 2. w = s⁻¹ mod n
        w = pow(s, -1, n)

        # 3. u1 = ew mod n, u2 = rw mod n
        u1 = (message_hash * w) % n
        u2 = (r * w) % n

        # 4. 점 계산: (x1, y1) = u1×G + u2×Q
        G = (self.curve.Gx, self.curve.Gy)
        point1 = self.curve.scalar_mult(u1, G)
        point2 = self.curve.scalar_mult(u2, public_key)
        result = self.curve.point_add(point1, point2)

        if result is None:
            return False

        x1, _ = result

        # 5. 검증: r ≡ x1 mod n
        return r == x1 % n


class ECDH:
    """ECDH 키 교환 프로토콜"""

    def __init__(self, curve: EllipticCurve):
        self.curve = curve
        self.ecdsa = ECDSA(curve)

    def generate_keypair(self) -> Tuple[int, Tuple[int, int]]:
        """키 쌍 생성"""
        return self.ecdsa.generate_keypair()

    def compute_shared_secret(self, private_key: int,
                               other_public_key: Tuple[int, int]) -> int:
        """
        공유 비밀 계산

        Args:
            private_key: 나의 개인키
            other_public_key: 상대방의 공개키

        Returns:
            공유 비밀 (x좌표)
        """
        # shared_point = private_key × other_public_key
        shared_point = self.curve.scalar_mult(private_key, other_public_key)

        if shared_point is None:
            raise ValueError("Invalid public key")

        # x좌표를 공유 비밀로 사용
        return shared_point[0]


# 사용 예시
if __name__ == "__main__":
    # ECDSA 예시
    ecdsa = ECDSA(P256)

    # 키 쌍 생성
    private_key, public_key = ecdsa.generate_keypair()
    print(f"개인키: {hex(private_key)[:20]}...")
    print(f"공개키: ({hex(public_key[0])[:20]}..., {hex(public_key[1])[:20]}...)")

    # 메시지 해시 (실제로는 SHA-256 등 사용)
    message = b"Hello, ECC!"
    message_hash = int.from_bytes(message.ljust(32, b'\x00')[:32], 'big')

    # 서명
    signature = ecdsa.sign(private_key, message_hash)
    print(f"서명: (r={hex(signature[0])[:20]}..., s={hex(signature[1])[:20]}...)")

    # 검증
    is_valid = ecdsa.verify(public_key, message_hash, signature)
    print(f"서명 검증: {'성공' if is_valid else '실패'}")

    # ECDH 예시
    ecdh = ECDH(P256)

    # Alice 키 쌍
    alice_priv, alice_pub = ecdh.generate_keypair()

    # Bob 키 쌍
    bob_priv, bob_pub = ecdh.generate_keypair()

    # 공유 비밀 계산
    alice_secret = ecdh.compute_shared_secret(alice_priv, bob_pub)
    bob_secret = ecdh.compute_shared_secret(bob_priv, alice_pub)

    print(f"\nAlice 공유 비밀: {hex(alice_secret)[:20]}...")
    print(f"Bob 공유 비밀: {hex(bob_secret)[:20]}...")
    print(f"공유 비밀 일치: {alice_secret == bob_secret}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 공개키 알고리즘 비교

| 특성 | RSA | ECC |
|:---|:---|:---|
| **수학적 기반** | 정수 분해 | 타원 곡선 이산 로그 |
| **키 길이 (128비트 보안)** | 3072비트 | 256비트 |
| **서명 속도** | 느림 | 빠름 |
| **서명 크기** | 3072비트 | 512비트 (r+s) |
| **키 생성** | 느림 | 빠름 |
| **특허** | 만료 | 만료 |
| **채택** | 감소 | 증가 |

#### 2. ECC 곡선 선택 가이드

| 용도 | 권장 곡선 | 이유 |
|:---|:---|:---|
| **TLS (일반)** | P-256 | 널리 지원, 충분한 보안 |
| **TLS (고보안)** | P-384, Curve25519 | 높은 보안 강도 |
| **Bitcoin/Ethereum** | secp256k1 | 생태계 표준 |
| **SSH** | Ed25519 | 빠른 서명, 작은 키 |
| **정부/군사** | P-384, P-521 | NSA Suite B |

#### 3. 과목 융합 관점 분석

- **네트워크**: TLS 1.3 ECDHE, TLS certificate 서명
- **블록체인**: Bitcoin secp256k1, Ethereum 서명
- **SSH**: Ed25519 호스트/사용자 인증
- **코드 서명**: ECDSA P-256
- **모바일**: Apple Secure Enclave, Android KeyStore

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 웹 서비스 TLS 인증서 선택**
- 상황: 새로운 웹 서비스 TLS 인증서 발급
- 판단: ECDSA P-256 인증서 사용
- 핵심 결정:
  - 인증서: ECDSA P-256
  - 키 교환: ECDHE (P-256 또는 X25519)
  - 서명: ECDSA P-256
- 효과: 인증서 크기 50% 감소, 핸드쉐이크 속도 향상

**시나리오 2: IoT 디바이스 인증**
- 상황: 저전력 IoT 디바이스, 인증 필요
- 판단: Ed25519 기기 인증
- 핵심 결정:
  - 기기별 개인키: Secure Element에 저장
  - 서명: Ed25519 (매우 빠름)
  - 인증서: Ed25519 공개키
- 효과: 전력 소모 90% 감소 vs RSA

**시나리오 3: 블록체인 DApp 서명**
- 상황: 지갑 서명, 스마트 컨트랙트 검증
- 판단: secp256k1 (생태계 호환성)
- 핵심 결정:
  - 곡선: secp256k1 (Bitcoin/Ethereum 표준)
  - 서명: ECDSA (k값 안전 생성 필수)
- 효과: 기존 인프라 완전 호환

#### 2. 도입 시 고려사항 (체크리스트)

**보안 체크리스트**
- [ ] 난수 생성기 안전성 (CSPRNG)
- [ ] 스칼라 k 재사용 방지 (ECDSA)
- [ ] Side-channel 방어 (constant-time)
- [ ] 곡선 검증 (NIST vs Safe Curves)

**운영 체크리스트**
- [ ] 라이브러리 호환성 (OpenSSL, mbedTLS)
- [ ] 하드웨어 가속 지원 여부
- [ ] 키 백업 및 복구 절차
- [ ] 인증서 PKI 연동

#### 3. 안티패턴 (Anti-patterns)

| 안티패턴 | 문제점 | 올바른 접근 |
|:---|:---|:---|
| **커스텀 곡선 사용** | 검증 부족, 취약점 | 표준 곡선 사용 |
| **k값 재사용** | 개인키 노출 | 난수 k를 매번 생성 |
| **점 검증 생략** | 잘못된 공개키 수용 | is_on_curve 검증 |
| **Side-channel 미방어** | 타이밍 공격 | Constant-time 구현 |

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | RSA 대비 |
|:---|:---|
| 키 크기 | 1/12로 축소 (128비트 보안) |
| 서명 속도 | 10~100배 향상 |
| 대역폭 | 50% 이상 절약 |
| 전력 소모 | 90% 감소 (IoT) |

#### 2. 미래 전망 및 진화 방향

- **Post-Quantum**: 양자 컴퓨터에 취약 → PQC 전환 준비
- **Hybrid 인증서**: ECC + PQC 병행 (전환기)
- **Curve25519 확대**: NIST 곡선 불신으로 대안 확산
- **하드웨어 가속**: CPU/TPM 내장 ECC 가속

#### 3. 참고 표준/가이드

- **SEC 2**: Recommended Elliptic Curve Domain Parameters
- **FIPS 186-5**: Digital Signature Standard (ECDSA, EdDSA)
- **RFC 7748**: Elliptic Curves for Security (X25519, X448)
- **RFC 8032**: Edwards-Curve Digital Signature (EdDSA)
- **SafeCurves**: https://safecurves.cr.yp.to

---

### 관련 개념 맵 (Knowledge Graph)

- [RSA](@/studynotes/09_security/02_crypto/rsa.md) : 대안 공개키 알고리즘
- [디지털 서명](@/studynotes/09_security/02_crypto/digital_signature.md) : ECDSA 기반
- [DH 키 교환](@/studynotes/09_security/02_crypto/dh_key_exchange.md) : ECDH 기반
- [TLS 1.3](@/studynotes/09_security/03_network_security/tls13.md) : ECC 필수 사용
- [블록체인 보안](@/studynotes/09_security/06_compliance/blockchain_security.md) : secp256k1

---

### 어린이를 위한 3줄 비유 설명

1. **곡선 위 게임**: 특별한 모양의 곡선 위에서 점프 놀이를 해요. 시작점에서 몇 번 점프했는지 아무도 모르게 숨길 수 있죠.
2. **짧고 강한 열쇠**: RSA는 아주 긴 열쇠가 필요해요. 하지만 ECC는 짧은 열쇠로도 똑같이 튼튼한 자물쇠를 만들 수 있어요.
3. **빠르고 가벼워**: 작은 컴퓨터나 스마트워치에서도 잘 돌아가요. 무거운 RSA 대신 가벼운 ECC를 쓰면 배터리도 오래가죠.
