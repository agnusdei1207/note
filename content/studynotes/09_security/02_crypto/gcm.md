+++
title = "GCM (Galois/Counter Mode)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# GCM (Galois/Counter Mode)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CTR 모드 기반의 인증 암호화(AEAD) 방식으로, AES와 결합하여 AES-GCM으로 사용되며 기밀성과 무결성을 단일 연산으로 동시에 보장합니다.
> 2. **가치**: TLS 1.3의 필수 암호 스위트이며, 하드웨어 가속(AES-NI + PCLMULQDQ)으로 10Gbps+ 성능을 달성합니다.
> 3. **융합**: VPN, HTTPS, WiFi(WPA3), 클라우드 스토리지 암호화 등 실시간 통신 보안의 핵심입니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**GCM(Galois/Counter Mode)**은 2004년 David McGrew와 John Viega가 제안한 인증 암호화(Authenticated Encryption) 모드입니다. CTR 모드의 암호화와 GHASH의 인증을 결합하여 AEAD(Authenticated Encryption with Associated Data)를 제공합니다.

**핵심 특성**:

| 특성 | 값 | 설명 |
|:---|:---|:---|
| **기반 모드** | CTR (Counter) | 스트림 암호화 방식 |
| **인증 방식** | GHASH (Galois Hash) | GF(2^128) 상에서 연산 |
| **태그 크기** | 128비트 (권장) | 96/112/120/124/128비트 선택 가능 |
| **Nonce 크기** | 96비트 (권장) | 96비트 시 효율적 |
| **AEAD 지원** | 지원 | AAD(Additional Authenticated Data) 가능 |
| **병렬 처리** | 완전 지원 | 암호화/인증 모두 병렬 가능 |

**AEAD (Authenticated Encryption with Associated Data)**:
```
┌─────────────────────────────────────────────────────────────────────┐
│                    AEAD 개념                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  입력:                                                              │
│  - Key (K): 암호화 키                                              │
│  - Nonce (IV): 재사용 금지                                         │
│  - Plaintext (P): 암호화할 데이터                                  │
│  - AAD: 인증만 할 데이터 (암호화 안 함)                            │
│                                                                     │
│  출력:                                                              │
│  - Ciphertext (C): 암호문                                          │
│  - Authentication Tag (T): 무결성 검증 태그                        │
│                                                                     │
│  보장:                                                              │
│  - 기밀성: 평문은 암호문으로 변환                                  │
│  - 무결성: 태그를 통해 변조 탐지                                   │
│  - 인증: AAD까지 포함한 인증                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### 2. GCM 구조 다이어그램

```text
<<< GCM 암호화 구조 >>>

    ┌────────────────────────────────────────────────────────────────────────┐
    │                        GCM Encryption                                   │
    └────────────────────────────────────────────────────────────────────────┘
                                    │
    ┌────────────────────────────────────────────────────────────────────────┐
    │  Key (K) ────────┐                                                     │
    │                  │                                                     │
    │  Nonce (IV) ─────┼───────────────────────────────────────────┐        │
    │                  │                                           │        │
    │  Counter ────────┘                                           │        │
    │    │                                                          │        │
    │    ▼                                                          ▼        │
    │  ┌──────────────────────────────────────┐    ┌──────────────────────┐ │
    │  │           CTR 모드 암호화             │    │   GHASH 인증         │ │
    │  │                                      │    │                      │ │
    │  │  Counter[1] → AES_K → ⊕ P1 → C1 ────┼───►│                      │ │
    │  │  Counter[2] → AES_K → ⊕ P2 → C2 ────┼───►│  H = AES_K(0^128)   │ │
    │  │  Counter[3] → AES_K → ⊕ P3 → C3 ────┼───►│                      │ │
    │  │    ...                              │    │  Tag = GHASH_H()     │ │
    │  │                                      │    │       ⊕ AES_K(J0)   │ │
    │  └──────────────────────────────────────┘    └──────────────────────┘ │
    │                                                                          │
    │  출력: Ciphertext (C1||C2||C3||...) + Authentication Tag (T)           │
    └────────────────────────────────────────────────────────────────────────┘


<<< GCM GHASH 연산 상세 >>>

    ┌────────────────────────────────────────────────────────────────────────┐
    │  GHASH_H(AAD, C) = X_m                                                 │
    │                                                                        │
    │  여기서:                                                               │
    │  - H = AES_K(0^128) : 해시 서브키                                     │
    │  - X_0 = 0^128                                                        │
    │  - X_i = (X_{i-1} ⊕ Block_i) · H (GF(2^128) 곱셈)                    │
    │                                                                        │
    │  GF(2^128) 곱셈:                                                       │
    │  - 기약 다항식: x^128 + x^7 + x^2 + x + 1                             │
    │  - 하드웨어 가산: PCLMULQDQ 명령어 활용                               │
    │                                                                        │
    │  ┌─────────────────────────────────────────────────────────────────┐  │
    │  │    AAD_1        AAD_2        C1          C2        LenBlock    │  │
    │  │      │            │          │           │            │        │  │
    │  │      ▼            ▼          ▼           ▼            ▼        │  │
    │  │   ┌───┐        ┌───┐      ┌───┐       ┌───┐       ┌───┐       │  │
    │  │   │ ⊕ │◄──X0──►│ ⊕ │◄──►│ ⊕ │◄────►│ ⊕ │◄────►│ ⊕ │       │  │
    │  │   └─┬─┘        └─┬─┘      └─┬─┘       └─┬─┘       └─┬─┘       │  │
    │  │     │            │          │           │            │        │  │
    │  │     ▼            ▼          ▼           ▼            ▼        │  │
    │  │   × H          × H        × H         × H          × H       │  │
    │  │     │            │          │           │            │        │  │
    │  │     └────────────┴──────────┴───────────┴────────────┘        │  │
    │  │                               │                                │  │
    │  │                               ▼                                │  │
    │  │                            GHASH                               │  │
    │  └─────────────────────────────────────────────────────────────────┘  │
    └────────────────────────────────────────────────────────────────────────┘
```

#### 3. 비유를 통한 이해
GCM은 **'봉투와 도장'**에 비유할 수 있습니다.
- **암호화(CTR)**: 편지를 봉투에 넣어 내용을 숨김
- **인증(GHASH)**: 봉투에 밀랍 도장을 찍어 변조 방지
- **AAD**: 봉투 겉면의 주소 (암호화 안 되지만 인증됨)
- **태그**: 밀랍 도장의 고유 패턴

#### 4. 등장 배경 및 발전 과정
1. **2000년 이전**: CBC + HMAC으로 별도 수행 (느리고 오류 가능)
2. **2004년**: GCM 제안 (McGrew & Viega)
3. **2007년**: NIST SP 800-38D로 표준화
4. **2010년대**: TLS 1.2에서 선택적, TLS 1.3에서 필수
5. **현재**: HTTPS, VPN, WiFi, 클라우드의 표준

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. GCM 수학적 기초

```text
<<< GF(2^128) 갈루아 필드 >>>

    GCM의 인증은 GF(2^128) 상에서의 곱셈을 기반:

    필드 정의:
    - 원소: 128비트 벡터
    - 덧셈: XOR 연산
    - 곱셈: 다항식 곱셈 후 기약 다항식으로 모듈로

    기약 다항식:
    G(x) = x^128 + x^7 + x^2 + x + 1

    곱셈 알고리즘 (간소화):
    ┌─────────────────────────────────────────────────────────────────────┐
    │  function GF_Multiply(X, Y):                                        │
    │      Z = 0                                                          │
    │      V = X                                                          │
    │      for i = 0 to 127:                                              │
    │          if Y[i] == 1:                                              │
    │              Z = Z XOR V                                            │
    │          if V[127] == 0:                                            │
    │              V = V << 1                                             │
    │          else:                                                      │
    │              V = (V << 1) XOR 0x87  # 기약 다항식                  │
    │      return Z                                                       │
    └─────────────────────────────────────────────────────────────────────┘

    하드웨어 가속 (Intel):
    - PCLMULQDQ: 캐리리스 64비트 곱셈
    - AES-NI: AES 암호화 가속
    - 결합: 10배 이상 성능 향상
```

#### 2. GCM 보안 요구사항

| 요구사항 | 설명 | 위반 시 결과 |
|:---|:---|:---|
| **Nonce 유일성** | 동일 키로 절대 동일 Nonce 재사용 금지 | 기밀성 완전 상실 |
| **태크 검증** | 복호화 전 태그 반드시 검증 | 선택 암호문 공격 |
| **태그 길이** | 최소 128비트 권장 | 위조 공격 가능성 증가 |
| **키 길이** | AES-128 이상 권장 | 전수 조사 위험 |
| **Nonce 예측** | 예측 불가능한 Nonce 사용 | 보안 감소 |

**Nonce 재사용의 치명적 결과**:
```
동일 Key K와 Nonce N으로 두 메시지 암호화:
C1 = P1 ⊕ AES_K(Counter)
C2 = P2 ⊕ AES_K(Counter)

→ C1 ⊕ C2 = P1 ⊕ P2
→ 평문 XOR 획득 → 기밀성 완전 상실
→ GHASH도 동일 H 사용 → 인증도 무력화
```

#### 3. Python 구현: GCM (개념적)

```python
from dataclasses import dataclass
from typing import Tuple, Optional
import os

@dataclass
class GCMResult:
    """GCM 연산 결과"""
    ciphertext: bytes
    tag: bytes

class AES_GCM:
    """AES-GCM 구현 (개념적)"""

    TAG_SIZE = 16  # 128비트 태그
    NONCE_SIZE = 12  # 96비트 논스 (권장)

    def __init__(self, key: bytes):
        """초기화"""
        if len(key) not in [16, 24, 32]:
            raise ValueError("Key must be 16, 24, or 32 bytes")

        self.key = key
        self.aes = self._init_aes(key)
        self.h = self.aes.encrypt(b'\x00' * 16)  # 해시 서브키 H

    def _init_aes(self, key: bytes):
        """AES 초기화 (실제로는 cryptography 라이브러리 사용)"""
        # 간소화된 플레이스홀더
        class SimpleAES:
            def __init__(self, k):
                self.key = k
            def encrypt(self, data):
                # 실제 구현 필요
                return data  # placeholder

        return SimpleAES(key)

    def _gf_multiply(self, x: bytes, y: bytes) -> bytes:
        """GF(2^128) 곱셈"""
        # 간소화된 구현
        # 실제로는 PCLMULQDQ 활용 또는 최적화된 알고리즘 필요
        result = 0
        x_int = int.from_bytes(x, 'big')
        y_int = int.from_bytes(y, 'big')

        for i in range(128):
            if y_int & (1 << (127 - i)):
                result ^= x_int
            if x_int & 1:
                x_int = (x_int >> 1) ^ 0xe1000000000000000000000000000000
            else:
                x_int >>= 1

        return result.to_bytes(16, 'big')

    def _ghash(self, data: bytes) -> bytes:
        """GHASH 계산"""
        # 패딩
        pad_len = (16 - (len(data) % 16)) % 16
        padded = data + b'\x00' * pad_len

        result = b'\x00' * 16

        for i in range(0, len(padded), 16):
            block = padded[i:i+16]
            xored = bytes([result[j] ^ block[j] for j in range(16)])
            result = self._gf_multiply(xored, self.h)

        return result

    def _gctr(self, icb: bytes, data: bytes) -> bytes:
        """GCTR (Counter Mode) 암호화"""
        result = b""
        cb = icb

        for i in range(0, len(data), 16):
            block = data[i:i+16]

            # 키 스트림 생성
            keystream = self.aes.encrypt(cb)

            # XOR
            xored = bytes([block[j] ^ keystream[j] for j in range(len(block))])
            result += xored

            # 카운터 증가
            cb_int = int.from_bytes(cb, 'big') + 1
            cb = cb_int.to_bytes(16, 'big')

        return result

    def encrypt(self, plaintext: bytes, nonce: bytes,
                aad: bytes = b"") -> GCMResult:
        """GCM 암호화"""
        if len(nonce) != self.NONCE_SIZE:
            # 96비트가 아니면 GHASH로 J0 계산
            j0 = self._ghash(nonce + b'\x00' * (16 - len(nonce) % 16) +
                           (len(nonce) * 8).to_bytes(8, 'big'))
        else:
            # 96비트면 J0 = Nonce || 0^31 || 1
            j0 = nonce + b'\x00\x00\x00\x01'

        # 암호화
        ciphertext = self._gctr(j0, plaintext)

        # GHASH 입력 구성
        aad_bits = len(aad) * 8
        ct_bits = len(ciphertext) * 8
        len_block = aad_bits.to_bytes(8, 'big') + ct_bits.to_bytes(8, 'big')

        # AAD 패딩
        aad_padded = aad + b'\x00' * ((16 - len(aad) % 16) % 16)
        # 암호문 패딩
        ct_padded = ciphertext + b'\x00' * ((16 - len(ciphertext) % 16) % 16)

        ghash_input = aad_padded + ct_padded + len_block
        s = self._ghash(ghash_input)

        # 태그 생성
        tag = self._gctr(j0, s)[:self.TAG_SIZE]

        return GCMResult(ciphertext=ciphertext, tag=tag)

    def decrypt(self, ciphertext: bytes, nonce: bytes,
                tag: bytes, aad: bytes = b"") -> Optional[bytes]:
        """GCM 복호화"""
        if len(nonce) != self.NONCE_SIZE:
            j0 = self._ghash(nonce + b'\x00' * (16 - len(nonce) % 16) +
                           (len(nonce) * 8).to_bytes(8, 'big'))
        else:
            j0 = nonce + b'\x00\x00\x00\x01'

        # 태그 검증 먼저 수행
        aad_bits = len(aad) * 8
        ct_bits = len(ciphertext) * 8
        len_block = aad_bits.to_bytes(8, 'big') + ct_bits.to_bytes(8, 'big')

        aad_padded = aad + b'\x00' * ((16 - len(aad) % 16) % 16)
        ct_padded = ciphertext + b'\x00' * ((16 - len(ciphertext) % 16) % 16)

        ghash_input = aad_padded + ct_padded + len_block
        s = self._ghash(ghash_input)
        expected_tag = self._gctr(j0, s)[:self.TAG_SIZE]

        # 상수 시간 비교 (타이밍 공격 방지)
        if not self._constant_time_compare(tag, expected_tag):
            return None  # 인증 실패

        # 복호화
        plaintext = self._gctr(j0, ciphertext)
        return plaintext

    def _constant_time_compare(self, a: bytes, b: bytes) -> bool:
        """상수 시간 비교"""
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a, b):
            result |= x ^ y
        return result == 0


# 사용 예시
if __name__ == "__main__":
    # 실제 사용 시 cryptography 라이브러리 권장
    # from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    print("AES-GCM 개념 설명")
    print("=" * 50)
    print("Key: 256비트 (32바이트)")
    print("Nonce: 96비트 (12바이트) 권장")
    print("Tag: 128비트 (16바이트)")
    print()
    print("주의사항:")
    print("1. 동일 키로 절대 동일 Nonce 재사용 금지")
    print("2. 복호화 전 반드시 태그 검증")
    print("3. 96비트 Nonce 사용 시 성능 최적")
    print()
    print("실제 사용 예시 (cryptography 라이브러리):")
    print("""
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

key = AESGCM.generate_key(bit_length=256)
aesgcm = AESGCM(key)
nonce = os.urandom(12)

# 암호화
ct = aesgcm.encrypt(nonce, plaintext, aad)

# 복호화
pt = aesgcm.decrypt(nonce, ct, aad)
""")
```

#### 4. GCM 성능 특성

| 플랫폼 | AES-NI 없음 | AES-NI + PCLMULQDQ | 향상률 |
|:---|:---|:---|:---|
| **Intel x86** | ~3 cycles/byte | ~0.5 cycles/byte | 6x |
| **ARM NEON** | ~5 cycles/byte | ~1 cycle/byte | 5x |
| **GPU** | ~0.1 cycles/byte | - | 병렬 처리 |

---

### III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. AEAD 모드 비교

| 모드 | 기반 | 병렬화 | 온라인 | 성능 | 표준 |
|:---|:---|:---|:---|:---|:---|
| **GCM** | CTR + GHASH | 완전 | 가능 | 매우 빠름 | NIST SP 800-38D |
| **CCM** | CBC-MAC + CTR | 부분 | 불가 | 중간 | NIST SP 800-38C |
| **ChaCha20-Poly1305** | 스트림 + Poly1305 | 완전 | 가능 | 빠름 | RFC 8439 |
| **OCB** | XOR-Encrypt-XOR | 완전 | 가능 | 매우 빠름 | RFC 7253 |
| **SIV** | CMAC + CTR | 부분 | 불가 | 중간 | RFC 5297 |

#### 2. GCM vs ChaCha20-Poly1305

| 특성 | AES-GCM | ChaCha20-Poly1305 |
|:---|:---|:---|
| **키 길이** | 128/192/256비트 | 256비트 |
| **하드웨어 가속** | AES-NI 필요 | 소프트웨어만으로 빠름 |
| **모바일 성능** | 중간 (가속 없으면 느림) | 빠름 (ARM 최적화) |
| **Nonce 재사용** | 치명적 | 치명적 |
| **TLS 지원** | 필수 (TLS 1.3) | 필수 (TLS 1.3) |

#### 3. 과목 융합 관점 분석
- **네트워크 보안**: TLS 1.3의 필수 암호 스위트
- **프로토콜 보안**: SSH, VPN (WireGuard, IPsec)
- **무선 보안**: WPA3, WiFi 6
- **클라우드**: S3 SSE-C, EBS 암호화
- **API 보안**: gRPC, REST API 암호화

---

### IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: TLS 1.3 서버 구성**
- 요구사항: 고성능 HTTPS 서버
- 판단: AES-256-GCM 우선, 모바일 고려 시 ChaCha20-Poly1305 폴백
- 구현: OpenSSL, BoringSSL 등 활용

**시나리오 2: IoT 디바이스 통신**
- 요구사항: 저전력 MCU, AES-NI 없음
- 판단: ChaCha20-Poly1305 권장
- 이유: 소프트웨어 구현에서도 빠름

**시나리오 3: 데이터베이스 암호화**
- 요구사항: 대용량, 랜덤 액세스
- 판단: AES-GCM-SIV 또는 XTS 고려
- 이유: Nonce 재사용 방지 중요

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] 하드웨어 가속(AES-NI) 지원 여부 확인
- [ ] Nonce 생성 정책 수립 (절대 재사용 금지)
- [ ] 태그 길이 선택 (128비트 권장)
- [ ] AAD 활용 방안 (헤더 인증 등)
- [ ] 타이밍 공격 방지 (상수 시간 비교)

#### 3. 안티패턴 (Anti-patterns)
- **Nonce 재사용**: 동일 키+Nonce 조합 재사용 → 기밀성 상실
- **태그 검증 생략**: 복호화만 하고 태그 확인 안 함 → 공격 가능
- **짧은 태그**: 32/64비트 태그 사용 → 위조 공격 취약
- **예측 가능한 Nonce**: 카운터를 그대로 Nonce로 사용

---

### V. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | 내용 | 측정 방법 |
|:---|:---|:---|
| 기밀성+무결성 | 단일 연산으로 두 가지 보장 | 구현 복잡도 감소 |
| 성능 | 하드웨어 가속 시 초고속 | 10+ Gbps |
| 상호 운용성 | TLS 1.3 필수, 전 세계 호환 | 호환성 테스트 |
| 보안 | 검증된 표준, 20년+ 안전 | 암호 분석 결과 |

#### 2. 미래 전망 및 진화 방향
- **AES-GCM-SIV**: Nonce-reuse 안전한 변종 (RFC 8452)
- **XChaCha20-Poly1305**: 192비트 Nonce로 안전성 향상
- **양자 내성**: GCM 자체는 안전, AES는 256비트 권장
- **하드웨어 진화**: 더 강력한 가속 명령어

#### 3. 참고 표준/가이드
- **NIST SP 800-38D**: GCM 공식 표준
- **RFC 5116**: AEAD 인터페이스
- **RFC 8439**: ChaCha20-Poly1305
- **RFC 8446**: TLS 1.3 (GCM 필수)

---

### 관련 개념 맵 (Knowledge Graph)
- [AES](@/studynotes/09_security/02_crypto/aes.md) : GCM의 기반이 되는 암호
- [대칭키 암호](@/studynotes/09_security/02_crypto/symmetric_encryption.md) : GCM의 상위 개념
- [HMAC](@/studynotes/09_security/02_crypto/encryption_algorithms.md) : 인증의 대안
- [TLS](@/studynotes/09_security/03_network/network_security_systems.md) : GCM을 사용하는 프로토콜
- [ChaCha20](@/studynotes/09_security/02_crypto/symmetric_encryption.md) : GCM의 대안

---

### 어린이를 위한 3줄 비유 설명
1. **봉투와 도장**: 편지를 봉투에 넣고(암호화), 밀랍 도장을 찍어요(인증). 누군가 뜯으면 도장이 망가져서 알 수 있어요.
2. **한 번에 두 가지**: 비밀 유지와 변조 방지를 한 번에 해결해요. 따로 하면 느리고 실수하기 쉬워요.
3. **열쇠와 번호**: 열쇠(키)는 비밀이고, 번호(Nonce)는 매번 달라야 해요. 같은 번호를 쓰면 안 돼요!
