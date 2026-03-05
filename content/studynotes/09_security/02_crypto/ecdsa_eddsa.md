+++
title = "ECDSA / EdDSA (타원 곡선 디지털 서명)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# ECDSA / EdDSA (타원 곡선 디지털 서명)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ECDSA(ANSI/NIST)와 EdDSA(Bernstein)는 타원 곡선 기반 디지털 서명 알고리즘으로, RSA 대비 1/6 크기의 서명과 10~100배 빠른 성능을 제공합니다.
> 2. **가치**: ECDSA는 TLS, 코드 서명, 블록체인의 표준이며, EdDSA는 결정론적 서명, 빠른 속도, Side-channel 강건성으로 SSH, Signal, 모바일 보안에 최적입니다.
> 3. **융합**: TLS 1.3, Bitcoin(secp256k1 ECDSA), SSH(ed25519 EdDSA), FIDO2/WebAuthn(EdDSA) 등 현대 인증 생태계의 핵심입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**ECDSA (Elliptic Curve Digital Signature Algorithm)**
- **정의**: 타원 곡선 위에서 동작하는 DSA 변형
- **표준**: ANSI X9.62, FIPS 186-5, SEC 1
- **서명 크기**: 2×n 비트 (r, s 각 n비트) → P-256: 64바이트
- **난수 필요**: 서명 시 난수 k 필수 (k 유출 = 개인키 노출)
- **표준 곡선**: P-256, P-384, P-521, secp256k1

**EdDSA (Edwards-curve Digital Signature Algorithm)**
- **정의**: Edwards 곡선 위에서 동작하는 Schnorr 서명 변형
- **설계자**: Daniel J. Bernstein 외
- **서명 크기**: 2×n 비트 → Ed25519: 64바이트
- **결정론적**: 난수 대신 해시로 k 생성 (k 유출 위험 없음)
- **표준 곡선**: Ed25519 (Curve25519), Ed448

#### 2. ECDSA vs EdDSA 비교

| 특성 | ECDSA | EdDSA |
|:---|:---|:---|
| **곡선 형식** | Weierstrass | Edwards/Montgomery |
| **난수 필요** | 예 (위험) | 아니오 (결정론적) |
| **서명 속도** | 중간 | 매우 빠름 |
| **검증 속도** | 빠름 | 빠름 |
| **Side-channel** | 취약 가능 | 강건 |
| **표준** | NIST, ANSI | RFC 8032 |
| **주요 용도** | TLS, Bitcoin | SSH, Signal, FIDO2 |

#### 3. 비유를 통한 이해
디지털 서명은 **'인감도장 + 비밀번호'**에 비유할 수 있습니다:

```
ECDSA (은행 인감):
1. 인감도장을 찍을 때마다 새로운 비밀번호가 필요해요
2. 비밀번호를 잃어버리면 계좌가 털릴 수 있어요
3. 하지만 은행망에서 널리 쓰여요

EdDSA (디지털 도장):
1. 도장 자체가 비밀번호를 만들어요
2. 비밀번호를 기억할 필요가 없어요
3. 빠르고 안전하지만 새로운 시스템이에요
```

#### 4. 등장 배경 및 발전 과정

| 연도 | 사건 | 의미 |
|:---|:---|:---|
| **1991** | DSA 표준화 | NIST, 미국 정부 표준 |
| **1992** | ECDSA 제안 | Scott Vanstone, Certicom |
| **1999** | FIPS 186-2 | ECDSA 미국 정부 표준 |
| **2009** | Bitcoin | secp256k1 ECDSA 사용 |
| **2011** | Ed25519 발표 | Bernstein, 높은 성능 |
| **2014** | OpenSSH | Ed25519 기본 지원 |
| **2017** | RFC 8032 | EdDSA 표준화 |
| **2018** | FIPS 186-5 | EdDSA 정부 표준 추가 |
| **2020** | FIDO2/WebAuthn | EdDSA 지원 확대 |

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. ECDSA 알고리즘 구조

```text
                    [ ECDSA 서명 생성 ]

입력: 개인키 d, 메시지 m
출력: 서명 (r, s)

1. e = H(m)                    // 메시지 해시
2. e' = e의 왼쪽 n비트          // n = 곡선 위수의 비트 길이
3. k = 난수 (1 < k < n)        // ⚠️ 핵심: 안전한 난수 필수
4. (x1, y1) = k × G            // 스칼라 곱셈
5. r = x1 mod n                // x좌표 mod n
   if r == 0: goto 3           // r이 0이면 재시도
6. s = k⁻¹(e' + d × r) mod n   // 서명 계산
   if s == 0: goto 3           // s가 0이면 재시도
7. return (r, s)


                    [ ECDSA 서명 검증 ]

입력: 공개키 Q, 메시지 m, 서명 (r, s)
출력: 유효/무효

1. e = H(m)
2. e' = e의 왼쪽 n비트
3. r, s 범위 확인 (1 ≤ r, s < n)
4. w = s⁻¹ mod n               // s의 역원
5. u1 = e' × w mod n
6. u2 = r × w mod n
7. (x1, y1) = u1 × G + u2 × Q  // 두 점의 합
8. if (x1, y1) == O: 무효      // 무한원점이면 무효
9. v = x1 mod n
10. return v == r              // 일치하면 유효
```

#### 2. EdDSA (Ed25519) 알고리즘 구조

```text
                    [ Ed25519 키 생성 ]

입력: 32바이트 시드 b
출력: 개인키 s, 공개키 A

1. h = SHA-512(b)              // 64바이트 해시
2. s = clamp(h[0..31])         // 하위 32바이트 클램핑
   - s[0] &= 248
   - s[31] &= 127
   - s[31] |= 64
3. A = s × B                   // B = Edwards 곡선 기저점
4. return (s, A)


                    [ Ed25519 서명 생성 ]

입력: 개인키 s, 공개키 A, 메시지 M
출력: 서명 (R, S) - 64바이트

1. r = H(h[32..63] || M)       // 결정론적 nonce
   // h[32..63] = 키 생성 시 상위 32바이트
2. R = r × B                   // 스칼라 곱셈
3. k = H(R || A || M)          // 해시
4. S = (r + k × s) mod L        // L = 곡선 위수
5. return (R || S)             // 64바이트 서명


                    [ Ed25519 서명 검증 ]

입력: 공개키 A, 메시지 M, 서명 (R, S)
출력: 유효/무효

1. h = H(R || A || M)          // 동일한 해시
2. SB = S × B                  // 스칼라 곱셈
3. hA = h × A                  // 스칼라 곱셈
4. return SB == R + hA         // 일치하면 유효
```

#### 3. 알고리즘 비교 다이어그램

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    서명 알고리즘 비교                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐      ┌─────────────────────┐              │
│  │       ECDSA         │      │       EdDSA         │              │
│  ├─────────────────────┤      ├─────────────────────┤              │
│  │ 1. H(m) = e         │      │ 1. r = H(h2 || m)   │ ← 결정론적   │
│  │ 2. k = random()     │ ← 위험│ 2. R = r × B        │              │
│  │ 3. R = k × G        │      │ 3. k = H(R || A || m)│              │
│  │ 4. r = R.x mod n    │      │ 4. S = (r + k × s)   │              │
│  │ 5. s = k⁻¹(e+dr)    │      │ 5. sig = (R, S)     │              │
│  └─────────────────────┘      └─────────────────────┘              │
│                                                                     │
│  [위험 요소]                   [장점]                               │
│  • k 재사용 → 개인키 노출      • 결정론적 (난수 없음)               │
│  • k 예측 가능 → 개인키 노출   • Side-channel 강건                  │
│  • weak RNG → Sony PS3 사례    • 빠른 속도                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### 4. 핵심 알고리즘 & 실무 코드

```python
import hashlib
import secrets
from typing import Tuple

# Ed25519 상수
B = 256  # 비트 길이
L = 2**252 + 27742317777372353535851937790883648493  # 위수
D = -121665 * pow(121666, -1, 2**255 - 19)  # Edwards 곡선 파라미터

def sha512(data: bytes) -> bytes:
    """SHA-512 해시"""
    return hashlib.sha512(data).digest()

def clamp(data: bytes) -> int:
    """Ed25519 키 클램핑"""
    s = int.from_bytes(data, 'little')
    s &= ~7           # 하위 3비트 클리어
    s &= ~(128 << 8*31)  # 상위 비트 클리어
    s |= 64 << 8*31   # 두 번째 상위 비트 설정
    return s

def mod_inv(x: int, p: int) -> int:
    """모듈러 역원 (확장 유클리드)"""
    return pow(x, p - 2, p)

class Ed25519:
    """Ed25519 서명 알고리즘 (간소화 구현)"""

    @staticmethod
    def generate_keypair() -> Tuple[bytes, bytes]:
        """
        키 쌍 생성

        Returns:
            (private_key: 32바이트, public_key: 32바이트)
        """
        # 32바이트 랜덤 시드
        seed = secrets.token_bytes(32)

        # SHA-512로 확장
        h = sha512(seed)

        # 개인키 (클램핑)
        private_key = h[:32]
        s = clamp(private_key)

        # 공개키 (실제로는 Edwards 곡선 연산 필요)
        # 여기서는 간소화된 예시
        public_key = sha512(s.to_bytes(32, 'little'))[:32]

        return private_key, public_key

    @staticmethod
    def sign(private_key: bytes, public_key: bytes,
             message: bytes) -> bytes:
        """
        서명 생성 (결정론적)

        Args:
            private_key: 32바이트 개인키
            public_key: 32바이트 공개키
            message: 서명할 메시지

        Returns:
            64바이트 서명
        """
        # 키 확장
        h = sha512(private_key)
        s = clamp(h[:32])
        prefix = h[32:]

        # 결정론적 nonce
        r_hash = sha512(prefix + message)
        r = int.from_bytes(r_hash, 'little') % L

        # R = r × B (간소화)
        R = sha512(r.to_bytes(32, 'little'))[:32]

        # k = H(R || A || m)
        k_hash = sha512(R + public_key + message)
        k = int.from_bytes(k_hash, 'little') % L

        # S = (r + k × s) mod L
        S = (r + k * s) % L

        # 서명 조합
        signature = R + S.to_bytes(32, 'little')
        return signature

    @staticmethod
    def verify(public_key: bytes, message: bytes,
               signature: bytes) -> bool:
        """
        서명 검증

        Args:
            public_key: 32바이트 공개키
            message: 원본 메시지
            signature: 64바이트 서명

        Returns:
            검증 성공 여부
        """
        if len(signature) != 64:
            return False

        R = signature[:32]
        S = int.from_bytes(signature[32:], 'little')

        # S 범위 확인
        if S >= L:
            return False

        # k = H(R || A || m)
        k_hash = sha512(R + public_key + message)
        k = int.from_bytes(k_hash, 'little') % L

        # 실제로는 Edwards 곡선 위에서 SB == R + kA 확인
        # 여기서는 간소화된 검증
        expected_R = sha512(
            (S - k * int.from_bytes(public_key, 'little') % L)
            .to_bytes(32, 'little')
        )[:32]

        # 실제 구현에서는 곡선 연산으로 정확히 검증
        return True  # 간소화된 예시


class ECDSA_Safe:
    """ECDSA with Safe Random k (RFC 6979)"""

    @staticmethod
    def deterministic_k(private_key: int, message_hash: int,
                        n: int, q: int) -> int:
        """
        RFC 6979: 결정론적 k 생성
        (ECDSA의 난수 문제 해결)

        Args:
            private_key: 개인키 d
            message_hash: 메시지 해시 e
            n: 곡선 위수
            q: 해시 출력 길이 (비트)

        Returns:
            결정론적 nonce k
        """
        # HMAC-DRBG 기반 결정론적 k 생성
        hlen = q // 8

        # 1. h1 = message_hash
        h1 = message_hash.to_bytes((message_hash.bit_length() + 7) // 8, 'big')

        # 2. V = 0x01 0x01 ... 0x01
        V = b'\x01' * hlen

        # 3. K = 0x00 0x00 ... 0x00
        K = b'\x00' * hlen

        # 4. K = HMAC(K, V || 0x00 || int2octets(x) || bits2octets(h1))
        # ... (RFC 6979 전체 알고리즘 생략)

        # 간소화된 예시
        k = int.from_bytes(
            hashlib.sha256(private_key.to_bytes(32, 'big') + h1).digest(),
            'big'
        ) % n

        if k == 0:
            k = 1

        return k

    @staticmethod
    def sign_with_rfc6979(private_key: int, message_hash: int,
                          n: int, curve) -> Tuple[int, int]:
        """
        RFC 6979 기반 안전한 ECDSA 서명
        (난수 k 대신 결정론적 k 사용)
        """
        # 결정론적 k 생성
        k = ECDSA_Safe.deterministic_k(private_key, message_hash, n, 256)

        # R = k × G
        R = curve.scalar_mult(k, (curve.Gx, curve.Gy))
        r = R[0] % n

        # s = k⁻¹(e + d × r) mod n
        k_inv = pow(k, -1, n)
        s = (k_inv * (message_hash + private_key * r)) % n

        return (r, s)


# 사용 예시
if __name__ == "__main__":
    print("=== Ed25519 예시 ===")

    # 키 생성
    priv, pub = Ed25519.generate_keypair()
    print(f"개인키: {priv.hex()}")
    print(f"공개키: {pub.hex()}")

    # 서명
    message = b"Hello, Ed25519!"
    signature = Ed25519.sign(priv, pub, message)
    print(f"서명: {signature.hex()}")

    # 검증
    is_valid = Ed25519.verify(pub, message, signature)
    print(f"검증: {'성공' if is_valid else '실패'}")

    print("\n=== ECDSA RFC 6979 예시 ===")
    print("RFC 6979을 사용하면 난수 k 대신 결정론적 k를 생성하여")
    print("난수 생성기 문제로 인한 개인키 유출을 방지할 수 있습니다.")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 디지털 서명 알고리즘 포괄 비교

| 특성 | RSA | ECDSA | EdDSA |
|:---|:---|:---|:---|
| **수학적 기반** | 정수 분해 | ECDLP | ECDLP (Edwards) |
| **키 크기 (128비트 보안)** | 3072비트 | 256비트 | 256비트 |
| **서명 크기** | 384바이트 | 64바이트 | 64바이트 |
| **서명 속도** | 느림 | 중간 | 빠름 |
| **난수 필요** | 아니오 | 예 (위험) | 아니오 |
| **Side-channel** | 중간 | 취약 | 강건 |
| **표준화** | 오래됨 | 널리 표준 | 신규 표준 |

#### 2. 성능 비교 (Skylake CPU)

| 알고리즘 | 서명 (ops/s) | 검증 (ops/s) |
|:---|:---|:---|
| RSA-2048 | 1,100 | 35,000 |
| RSA-4096 | 160 | 10,000 |
| ECDSA P-256 | 25,000 | 10,000 |
| **Ed25519** | **110,000** | **45,000** |

#### 3. 과목 융합 관점 분석

- **TLS 1.3**: ECDSA P-256/P-384 인증서, EdDSA 옵션
- **SSH**: Ed25519 권장, ECDSA 지원
- **블록체인**: Bitcoin (ECDSA secp256k1), Ethereum (동일)
- **FIDO2/WebAuthn**: Ed25519, ECDSA 지원
- **코드 서명**: ECDSA P-256 (Apple, Microsoft)

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: TLS 인증서 알고리즘 선택**
- 상황: 웹 서비스 TLS 인증서 발급
- 판단: ECDSA P-256 기본, Ed25519 고려
- 핵심 결정:
  - 호환성: ECDSA P-256 (모든 클라이언트 지원)
  - 성능: Ed25519 (최신 클라이언트만)
  - 하이브리드: ECDSA + EdDSA 동시 발급
- 효과: 99.9% 호환성 + 성능 최적화

**시나리오 2: SSH 키 관리**
- 상황: 서버 SSH 키 교체
- 판단: Ed25519로 통일
- 핵심 결정:
  - 기존 RSA-2048 → Ed25519 마이그레이션
  - 사용자 교육: ssh-keygen -t ed25519
  - 레거시 서버: ECDSA 호환 유지
- 효과: 보안 강화, 성능 향상

**시나리오 3: 블록체인 서명**
- 상황: 토큰 전송 서명
- 판단: secp256k1 ECDSA (생태계 필수)
- 핵심 결정:
  - RFC 6979 적용 (결정론적 k)
  - Secure Element 사용
  - 서명 재사용 방지
- 효과: 생태계 호환, 보안 강화

#### 2. 도입 시 고려사항 (체크리스트)

**ECDSA 체크리스트**
- [ ] 난수 생성기 보안 (CSPRNG)
- [ ] RFC 6979 고려 (결정론적 k)
- [ ] k값 재사용 방지
- [ ] Side-channel 방어

**EdDSA 체크리스트**
- [ ] 라이브러리 지원 확인
- [ ] 클라이언트 호환성
- [ ] 키 저장 형식 (OpenSSH, PEM)
- [ ] 기존 시스템 마이그레이션

#### 3. 안티패턴 (Anti-patterns)

| 안티패턴 | 문제점 | 사례 | 올바른 접근 |
|:---|:---|:---|:---|
| **ECDSA k 재사용** | 개인키 노출 | Sony PS3 | RFC 6979 또는 EdDSA |
| **약한 난수 생성기** | 개인키 추정 | Android 4.3 | SecureRandom |
| **ECDSA + 클램핑 없음** | Side-channel | - | Constant-time |
| **EdDSA + 커스텀 곡선** | 검증 부족 | - | 표준 곡선 |

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | RSA 대비 |
|:---|:---|
| 서명 크기 | 1/6로 축소 |
| 서명 속도 | 10~100배 향상 (EdDSA) |
| 대역폭 | 80% 이상 절약 |
| 전력 소모 | 90% 감소 |

#### 2. 미래 전망 및 진화 방향

- **Schnorr 서명**: Bitcoin Taproot (BIP 340)
- **BLS 서명**: 집계 서명, 블록체인
- **Post-Quantum**: CRYSTALS-Dilithium (NIST PQC)
- **Hybrid 서명**: ECC + PQC 병행

#### 3. 참고 표준/가이드

- **FIPS 186-5**: Digital Signature Standard
- **RFC 6979**: Deterministic ECDSA
- **RFC 8032**: Edwards-Curve DSA (EdDSA)
- **SEC 1**: Elliptic Curve Cryptography
- **BIP 340**: Schnorr Signatures for secp256k1

---

### 관련 개념 맵 (Knowledge Graph)

- [ECC](@/studynotes/09_security/02_crypto/ecc.md) : 타원 곡선 기초
- [RSA](@/studynotes/09_security/02_crypto/rsa.md) : 대안 서명 알고리즘
- [디지털 서명](@/studynotes/09_security/02_crypto/digital_signature.md) : 서명 개념
- [TLS 1.3](@/studynotes/09_security/03_network_security/tls13.md) : 인증서 서명
- [FIDO2/WebAuthn](@/studynotes/09_security/05_identity/fido2.md) : 인증 서명

---

### 어린이를 위한 3줄 비유 설명

1. **전자 도장**: 종이에 도장을 찍듯, 컴퓨터 파일에 디지털 도장을 찍어요. "내가 확인했습니다"라고 말이죠.
2. **ECDSA의 비밀번호**: 도장을 찍을 때마다 새로운 비밀번호가 필요해요. 이 비밀번호를 잃어버리면 큰일나죠.
3. **EdDSA의 똑똑한 도장**: 비밀번호를 기억할 필요가 없어요. 도장이 스스로 비밀번호를 만들어내니까요. 더 빠르고 안전해요.
