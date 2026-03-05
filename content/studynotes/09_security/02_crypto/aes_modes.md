+++
title = "AES 운영 모드 (AES Operation Modes)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# AES 운영 모드 (AES Operation Modes)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: AES 블록 암호(128비트 고정 블록)를 다양한 길이의 데이터를 안전하게 암호화하기 위한 운영 방식으로, ECB/CBC/CFB/OFB/CTR/GCM 등이 있으며 각각 보안성·성능·기능적 특성이 상이합니다.
> 2. **가치**: 적절한 모드 선택은 암호화 시스템의 전체 보안을 결정하며, GCM은 인증 암호화(AEAD)로 기밀성과 무결성을 동시에 보장하는 현대적 표준입니다.
> 3. **융합**: TLS 1.3의 필수 사이퍼 스위트, 디스크 암호화(XTS), IoT 경량 암호, 클라우드 스토리지 암호화 등 다양한 영역에서 상황에 맞는 모드가 적용됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**AES 운영 모드**는 128비트 고정 블록을 처리하는 AES 암호 알고리즘을 임의 길이의 평문에 적용하기 위한 체계입니다. 블록 암호는 단독으로 사용될 수 없으며, 반드시 운영 모드와 결합하여야 실제 데이터 암호화가 가능합니다.

```
핵심 문제: 128비트 블록만 처리 가능 → 여러 블록 처리 방식 필요
해결 방안: 운영 모드를 통한 블록 간 연결 및 난수성 확보
```

#### 2. 비유를 통한 이해
AES 운영 모드는 **'페이지 번호 매기기 방식'**에 비유할 수 있습니다.
- **ECB**: 각 페이지에 동일한 도장 찍기 → 같은 내용은 같은 패턴
- **CBC**: 앞 페이지 내용이 다음 페이지에 영향 → 연쇄적 관계
- **CTR**: 카운터로 페이지 번호 암호화 → 병렬 처리 가능
- **GCM**: 페이지 번호 암호화 + 무결성 인증서 첨부 → 변조 탐지

#### 3. 등장 배경 및 발전 과정
1. **블록 암호의 근본적 한계**: AES는 128비트 블록만 처리 가능
2. **ECB의 치명적 취약점**: 동일 평문 블록 → 동일 암호문 블록 (패턴 노출)
3. **CBC의 등장 (1980)**: NIST FIPS 81, 앞 블록과 XOR로 패턴 은폐
4. **스트림 시뮬레이션 모드**: CFB, OFB - 블록 암호를 스트림 암호처럼 사용
5. **CTR 모드 표준화 (2001)**: 병렬 처리 가능, 랜덤 액세스 지원
6. **AEAD 모드 등장 (2007)**: GCM, CCM - 인증과 암호화를 하나로

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. AES 운영 모드 구성 요소 상세 분석

| 모드 | 정식 명칭 | 병렬화 | 패딩 | 특징 | 보안 등급 | 주요 용도 |
|:---|:---|:---:|:---:|:---|:---:|:---|
| **ECB** | Electronic Codebook | O | 필수 | 동일 평문→동일 암호문 | 위험 | 사용 금지 |
| **CBC** | Cipher Block Chaining | 암호화X/복호화O | 필수 | 이전 암호문과 XOR | 양호 | 파일 암호화 |
| **CFB** | Cipher Feedback | 암호화X/복호화O | 불필요 | 스트림 시뮬레이션 | 양호 | 레거시 시스템 |
| **OFB** | Output Feedback | X | 불필요 | 스트림 키 생성 | 양호 | 위성 통신 |
| **CTR** | Counter | O | 불필요 | 카운터 기반, 랜덤 액세스 | 양호 | 고속 암호화 |
| **GCM** | Galois/Counter | O | 불필요 | AEAD (암호화+인증) | 최상 | TLS 1.3, VPN |
| **XTS** | XEX Tweakable | O | 불필요 | 트윅 가능, 랜덤 액세스 | 양호 | 디스크 암호화 |
| **CCM** | Counter with CBC-MAC | 암호화O/복호화X | 불필요 | AEAD (CTR+CBC-MAC) | 양호 | WiFi WPA2 |

#### 2. 각 모드별 동작 원리 다이어그램

```
=== ECB (Electronic Codebook) Mode ===
┌─────────┐     ┌─────────┐     ┌─────────┐
│ P1      │     │ P2      │     │ Pn      │
│(128bit) │     │(128bit) │     │(128bit) │
└────┬────┘     └────┬────┘     └────┬────┘
     │               │               │
     ▼               ▼               ▼
┌─────────┐     ┌─────────┐     ┌─────────┐
│ AES Enc │     │ AES Enc │     │ AES Enc │
│  (Key)  │     │  (Key)  │     │  (Key)  │
└────┬────┘     └────┬────┘     └────┬────┘
     │               │               │
     ▼               ▼               ▼
┌─────────┐     ┌─────────┐     ┌─────────┐
│ C1      │     │ C2      │     │ Cn      │
└─────────┘     └─────────┘     └─────────┘

문제점: P1 == P2 → C1 == C2 (패턴 노출!)
===========================================

=== CBC (Cipher Block Chaining) Mode ===
                    ┌──────────┐
                    │    IV    │
                    └────┬─────┘
                         │ XOR
┌─────────┐              ▼     ┌─────────┐              ┌─────────┐
│ P1      │──XOR──┬──────────►│ P2      │──XOR──┬─────►│ Pn      │
└─────────┘       │          └─────────┘       │       └─────────┘
                  │                            │
                  ▼                            ▼
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│ AES Enc │  │ C1      │  │ AES Enc │  │ C2      │  │ AES Enc │
└────┬────┘  └─────────┘  └────┬────┘  └─────────┘  └────┬────┘
     │                         │                         │
     ▼                         ▼                         ▼
┌─────────┐               ┌─────────┐               ┌─────────┐
│ C1 ──────────────────►  │ C2 ──────────────────►  │ Cn      │
└─────────┘               └─────────┘               └─────────┘

특징: 암호화는 순차적, 복호화는 병렬 가능
===========================================

=== CTR (Counter) Mode ===

┌─────────────────────────────────────────────────────┐
│                    Counter Generator                 │
│  ┌─────┐   ┌─────┐   ┌─────┐       ┌─────┐          │
│  │Ctr+0│   │Ctr+1│   │Ctr+2│  ...  │Ctr+n│          │
│  └──┬──┘   └──┬──┘   └──┬──┘       └──┬──┘          │
└─────┼─────────┼─────────┼─────────────┼─────────────┘
      │         │         │             │
      ▼         ▼         ▼             ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ AES Enc │ │ AES Enc │ │ AES Enc │ │ AES Enc │
└────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
     │           │           │           │
     ▼ XOR       ▼ XOR       ▼ XOR       ▼ XOR
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ P1      │ │ P2      │ │ P3      │ │ Pn      │
└────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
     │           │           │           │
     ▼           ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ C1      │ │ C2      │ │ C3      │ │ Cn      │
└─────────┘ └─────────┘ └─────────┘ └─────────┘

특징: 완전 병렬화 가능, 랜덤 액세스 지원
===========================================

=== GCM (Galois/Counter) Mode ===

┌──────────────────────────────────────────────────────────────┐
│                        GCM Architecture                       │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              CTR Mode (Encryption)                       │ │
│  │   ┌─────┐    ┌─────┐    ┌─────┐                         │ │
│  │   │ J0  │    │ J+1 │    │ J+2 │   (Counter Blocks)      │ │
│  │   └──┬──┘    └──┬──┘    └──┬──┘                         │ │
│  │      │          │          │                             │ │
│  │      ▼          ▼          ▼                             │ │
│  │   ┌─────┐    ┌─────┐    ┌─────┐                         │ │
│  │   │ E_K │    │ E_K │    │ E_K │   (AES Encryption)      │ │
│  │   └──┬──┘    └──┬──┘    └──┬──┘                         │ │
│  │      │          │          │                             │ │
│  │      ▼ XOR      ▼ XOR      ▼ XOR                         │ │
│  │   ┌─────┐    ┌─────┐    ┌─────┐                         │ │
│  │   │Plaintext│ │Plaintext│ │Plaintext│                   │ │
│  │   └──┬──┘    └──┬──┘    └──┬──┘                         │ │
│  │      │          │          │                             │ │
│  │      ▼          ▼          ▼                             │ │
│  │   ┌─────┐    ┌─────┐    ┌─────┐                         │ │
│  │   │ C1  │    │ C2  │    │ Cn  │   (Ciphertext)          │ │
│  │   └──┬──┘    └──┬──┘    └──┬──┘                         │ │
│  └──────┼──────────┼──────────┼────────────────────────────┘ │
│         │          │          │                               │
│         └──────────┼──────────┘                               │
│                    │                                          │
│  ┌─────────────────▼───────────────────────────────────────┐ │
│  │          GHASH (Authentication)                          │ │
│  │                                                          │ │
│  │   AAD ──┐                                               │ │
│  │         │   ┌───────────────────────────────┐           │ │
│  │   C1 ───┼──►│   GHASH Function (GF(2^128))  │──► Tag    │ │
│  │   C2 ───┤   │   H = E_K(0^128)              │           │ │
│  │   ... ──┘   │   Y_i = (Y_{i-1} ⊕ X_i) · H  │           │ │
│  │             └───────────────────────────────┘           │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  Output: Ciphertext || Tag (128-bit)                         │
└──────────────────────────────────────────────────────────────┘

특징: 기밀성 + 무결성 + 인증을 한 번에 (AEAD)
```

#### 3. 심층 동작 원리: GCM 모드 상세 분석

```python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct

class AESGCMImplementation:
    """
    AES-GCM 구현 - AEAD (Authenticated Encryption with Associated Data)

    보안 속성:
    - 기밀성: CTR 모드 암호화
    - 무결성: GHASH를 통한 인증 태그
    - 인증: AAD(Additional Authenticated Data) 지원
    """

    def __init__(self, key: bytes):
        """
        Args:
            key: 128, 192, 또는 256비트 AES 키
        """
        if len(key) not in (16, 24, 32):
            raise ValueError("Key must be 16, 24, or 32 bytes")
        self.key = key
        self.key_size = len(key) * 8
        self._aesgcm = AESGCM(key)

    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> tuple:
        """
        AES-GCM 암호화

        Args:
            plaintext: 암호화할 평문
            aad: Additional Authenticated Data (암호화되지 않지만 인증됨)

        Returns:
            (nonce, ciphertext, tag)
        """
        # 96-bit nonce (IV) 생성 - 재사용 절대 금지!
        nonce = os.urandom(12)

        # 암호화 및 태그 생성
        # AESGCM.encrypt() returns ciphertext + tag concatenated
        ciphertext_with_tag = self._aesgcm.encrypt(nonce, plaintext, aad)

        # 태그는 마지막 16바이트
        ciphertext = ciphertext_with_tag[:-16]
        tag = ciphertext_with_tag[-16:]

        return nonce, ciphertext, tag

    def decrypt(self, nonce: bytes, ciphertext: bytes, tag: bytes,
                aad: bytes = b"") -> bytes:
        """
        AES-GCM 복호화

        Args:
            nonce: 암호화 시 사용된 12바이트 nonce
            ciphertext: 암호문
            tag: 16바이트 인증 태그
            aad: 암호화 시 사용된 AAD

        Returns:
            평문

        Raises:
            InvalidTag: 태그 검증 실패 시
        """
        ciphertext_with_tag = ciphertext + tag
        plaintext = self._aesgcm.decrypt(nonce, ciphertext_with_tag, aad)
        return plaintext

    @staticmethod
    def ghash(h: int, data: bytes) -> int:
        """
        GHASH 함수 구현 (교육용)

        GHASH_H(X) = X_1·H^m ⊕ X_2·H^{m-1} ⊕ ... ⊕ X_m·H
        여기서 ·은 GF(2^128) 상의 곱셈

        실제 구현은 cryptography 라이브러리 사용 권장
        """
        # GF(2^128) 상의 곱셈 구현
        # 기약 다항식: x^128 + x^7 + x^2 + x + 1
        R = 0xe1 << 120  # 기약 다항식

        def gf128_mul(x: int, y: int) -> int:
            """GF(2^128) 곱셈"""
            result = 0
            for i in range(128):
                if (y >> (127 - i)) & 1:
                    result ^= x
                carry = x & 1
                x >>= 1
                if carry:
                    x ^= R
            return result

        # 블록 단위 처리
        y = 0
        block_size = 16
        for i in range(0, len(data), block_size):
            block = data[i:i+block_size]
            x = int.from_bytes(block.ljust(block_size, b'\x00'), 'big')
            y = gf128_mul(y ^ x, h)

        return y


class AESCTRPImplementation:
    """
    AES-CTR 모드 구현 - 스트림 암호 시뮬레이션
    """

    def __init__(self, key: bytes):
        self.cipher = Cipher(
            algorithms.AES(key),
            modes.CTR(b'\x00' * 16),  # 실제 사용 시 랜덤 nonce 필요
            backend=default_backend()
        )

    def encrypt(self, plaintext: bytes, nonce: bytes) -> bytes:
        """
        CTR 모드 암호화

        장점:
        - 병렬 처리 가능
        - 랜덤 액세스 가능 (임의 블록부터 복호화)
        - 패딩 불필요
        """
        encryptor = self.cipher.encryptor()
        return encryptor.update(plaintext) + encryptor.finalize()

    def decrypt(self, ciphertext: bytes, nonce: bytes) -> bytes:
        """CTR 모드 복호화 (암호화와 동일)"""
        decryptor = self.cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()


# 보안 비교 테스트
def demonstrate_ecb_weakness():
    """ECB 모드의 취약점 시연"""
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    key = b'sixteenbytekey!!'  # 16 bytes
    plaintext = b'REPEAT' * 100  # 반복되는 패턴

    # ECB 암호화
    cipher_ecb = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher_ecb.encryptor()

    # 패딩
    padded = plaintext + b'\x00' * (16 - len(plaintext) % 16)
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    # 패턴 분석
    block_count = len(ciphertext) // 16
    unique_blocks = len(set(ciphertext[i*16:(i+1)*16] for i in range(block_count)))

    print(f"총 블록 수: {block_count}")
    print(f"고유 블록 수: {unique_blocks}")
    print(f"패턴 반복률: {(block_count - unique_blocks) / block_count * 100:.1f}%")
    # 결과: ECB에서는 동일 평문 블록이 동일 암호문 블록이 됨!
```

#### 4. 운영 모드 보안 분석표

| 공격 유형 | ECB | CBC | CTR | GCM | 대응 방안 |
|:---|:---:|:---:|:---:|:---:|:---|
| **패턴 분석** | 취약 | 안전 | 안전 | 안전 | CBC/CTR/GCM 사용 |
| **IV 재사용** | N/A | 치명적 | 치명적 | 치명적 | 랜덤/고유 IV 필수 |
| **패딩 오라클** | 취약 | 취약 | 안전 | 안전 | 인증 암호화 사용 |
| **비트 플리핑** | 탐지X | 탐지X | 탐지X | 탐지O | GCM/CCM 사용 |
| **블록 재정렬** | 취약 | 부분취약 | 부분취약 | 안전 | AEAD 모드 사용 |
| **병렬 처리** | O | 암호화X | O | O | 고성능 필요 시 CTR/GCM |

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 용도별 최적 모드 선택 매트릭스

| 용도 | 추천 모드 | 이유 | 대안 | 금지 모드 |
|:---|:---|:---|:---|:---|
| **TLS/VPN** | GCM | AEAD, 고성능, PFS | ChaCha20-Poly1305 | ECB, CBC |
| **디스크 암호호** | XTS-512 | 랜덤 액세스, 트윅 | LRW | ECB, CBC |
| **파일 암호화** | CBC + HMAC | 호환성, 무결성 | GCM | ECB |
| **데이터베이스** | CTR | 랜덤 액세스, 인덱싱 | GCM | ECB |
| **IoT/임베디드** | CCM | 적은 메모리 | GCM-SIV | OFB |
| **실시간 스트림** | CTR | 지연 없음, 병렬 | OFB | CBC |
| **메시지 전송** | GCM | 무결성 보장 | AES-CBC-HMAC | ECB |

#### 2. 성능 비교 (2024 기준, Skylake CPU)

| 모드 | 암호화 (MB/s) | 복호화 (MB/s) | 병렬 효율 | 메모리 사용 |
|:---|:---:|:---:|:---:|:---:|
| **ECB** | 4,500 | 4,500 | 최상 | 최소 |
| **CBC (Enc)** | 2,800 | 4,500 | 낮음/높음 | 적음 |
| **CTR** | 4,500 | 4,500 | 최상 | 적음 |
| **GCM** | 3,800 | 3,800 | 높음 | 중간 |
| **XTS** | 4,200 | 4,200 | 높음 | 중간 |

#### 3. 과목 융합 관점 분석

**네트워크 보안과 융합**
- TLS 1.3: AES-128-GCM, AES-256-GCM 필수 지원
- IPsec: ESP with AES-GCM (RFC 4106)
- SSH: aes256-gcm@openssh.com

**데이터베이스와 융합**
- TDE(Transparent Data Encryption): CBC 모드 일반적
- 컬럼 암호화: GCM 권장 (무결성 포함)
- 인덱스 가능 암호화: CTR 모드 (동일 평문 = 동일 암호문 주의)

**시스템 아키텍처와 융합**
- AES-NI 활용: GCM이 하드웨어 가속 최대 활용
- SIMD 병렬화: CTR, GCM이 벡터화에 적합

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 레거시 시스템 CBC → GCM 마이그레이션**
- 상황: 기존 파일 암호화 시스템이 CBC 사용, 무결성 검증 없음
- 판단: CBC+HMAC 조합 또는 GCM으로 전환
- 전략:
  1. 새 파일: GCM 적용
  2. 기존 파일: 복호화 후 GCM으로 재암호화
  3. 호환성 계층: 형식 식별자 추가

**시나리오 2: IoT 디바이스 암호화 모드 선택**
- 상황: 제한된 RAM(64KB), 저전력 MCU
- 판단: CCM 또는 GCM-SIV 선택
- 이유: 메모리 효율적, 인증 포함

**시나리오 3: 클라우드 스토리지 암호화**
- 상황: S3 객체 암호화, 랜덤 액세스 필요
- 판단: CTR 모드 + HMAC 또는 GCM
- 주의: CTR의 nonce 재사용 절대 금지

#### 2. 도입 시 고려사항 (체크리스트)

**기술적 체크리스트**
- [ ] AES 키 길이 결정 (128/192/256)
- [ ] IV/Nonce 생성 정책 수립 (절대 재사용 금지)
- [ ] 패딩 방식 결정 (PKCS#7, Zero padding)
- [ ] 태그 길이 결정 (GCM: 128/120/112/104/96비트)
- [ ] AAD 사용 여부 및 설계

**운영 체크리스트**
- [ ] 키 로테이션 정책
- [ ] 암호화 메타데이터 저장 방안
- [ ] 에러 처리 (태그 검증 실패 시)

#### 3. 안티패턴 (Anti-patterns)

```
취약한 구현 예시 (절대 사용 금지!)

1. ECB 모드 사용
   ❌ cipher = AES(key, mode=ECB)
   → 패턴 노출, 구조적 정보 유출

2. IV 고정 사용
   ❌ iv = b'0123456789abcdef'  # 항상 동일
   → CBC: 동일 평문 = 동일 암호문
   → CTR: XOR 키스트림 재사용 = 평문 노출
   → GCM: nonce 재사용 = 인증 완전 붕괴

3. GCM 태그 길이 단축
   ❌ tag_length = 8  # 64비트
   →生日 공격 취약 (2^32로 위조 가능)

4. 패딩 오라클 노출
   ❌ if padding_invalid: raise Exception("Padding Error")
   → 공격자가 패딩 오류 여부로 평문 복구 가능

올바른 구현:

1. GCM 권장 사용
   ✓ aesgcm = AESGCM(key)
   ✓ nonce = os.urandom(12)  # 매번 새로운 nonce
   ✓ ct = aesgcm.encrypt(nonce, plaintext, aad)

2. IV/Nonce 관리
   ✓ nonce = os.urandom(12)  # 96비트 권장
   ✓ key-nonce 쌍은 절대 재사용 금지

3. 에러 처리
   ✓ try: decrypt(...)
   ✓ except InvalidTag: return "Decryption Failed"  # 상세 정보 노출 금지
```

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 | 항목 | 수치/내용 |
|:---|:---|:---|
| **보안성** | 패턴 분석 방지 | ECB 제거로 100% 개선 |
| **무결성** | 변조 탐지 | GCM 도입 시 128비트 태그 |
| **성능** | 처리량 | GCM 하드웨어 가속 시 3GB/s+ |
| **컴플라이언스** | 표준 준수 | NIST SP 800-38D 준수 |

#### 2. 미래 전망 및 진화 방향

```
AES-GCM-SIV (RFC 8452)
├── nonce 재사용에 대한 내성 추가
├── 두 번 암호화로 안전성 강화
└── 클라우드 스토리지에 적합

AES-GCM-IV (NIST SP 800-38D Rev. 1)
├── 96비트 외 다양한 IV 길이 지원
└── 유연성 향상

양자 내성 AEAD
├── NIST PQC와 결합
└── CRYSTALS-Kyber + AEAD 조합
```

#### 3. 참고 표준/가이드

| 표준 | 내용 |
|:---|:---|
| **NIST SP 800-38A** | 블록 암호 운영 모드 (ECB, CBC, OFB, CFB, CTR) |
| **NIST SP 800-38D** | GCM 및 GMAC 명세 |
| **RFC 5116** | AEAD (Authenticated Encryption with Associated Data) |
| **RFC 8452** | AES-GCM-SIV: nonce-misuse resistant AEAD |
| **ISO/IEC 19772** | AEAD 암호 메커니즘 |

---

### 관련 개념 맵 (Knowledge Graph)
- [AES (Advanced Encryption Standard)](@/studynotes/09_security/02_crypto/aes.md) : 운영 모드가 적용되는 기본 블록 암호
- [대칭키 암호](@/studynotes/09_security/02_crypto/symmetric_encryption.md) : AES의 상위 개념
- [GCM (Galois/Counter Mode)](@/studynotes/09_security/02_crypto/gcm.md) : 인증 암호화의 대표 모드
- [해시 함수](@/studynotes/09_security/02_crypto/hash_function.md) : GHASH의 수학적 기반
- [TLS 1.3](@/studynotes/09_security/03_network/tls13.md) : AES-GCM 필수 사용 프로토콜

---

### 어린이를 위한 3줄 비유 설명
1. **각각의 방식**: 암호화는 여러 쪽지를 보내는 것과 같아요. 각 쪽지를 똑같이 접는 방식(ECB)도 있고, 앞 쪽지를 참고해서 접는 방식(CBC)도 있어요.
2. **빠르고 안전하게**: 카운터 방식(CTR)은 쪽지에 번호를 매겨서 순서대로 빠르게 처리할 수 있고, 여러 친구가 동시에 도와줄 수 있어요.
3. **도장 찍기**: GCM은 쪽지를 보낼 때 비밀 도장도 함께 찍어서, 누군가 내용을 바꿨는지 알 수 있게 해요. 내용도 숨기고, 변조도 막아요!
