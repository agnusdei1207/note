+++
title = "ChaCha20-Poly1305 (AEAD 스트림 암호)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# ChaCha20-Poly1305 (AEAD 스트림 암호)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ChaCha20-Poly1305는 Daniel J. Bernstein이 설계한 ChaCha20 스트림 암호와 Poly1305 MAC을 결합한 AEAD(Authenticated Encryption with Associated Data) 알고리즘으로, TLS 1.3의 필수 cipher suite입니다.
> 2. **가치**: AES-NI가 없는 모바일/IoT 기기에서 AES 대비 3배 빠른 성능을 제공하며, 타이밍 공격에 강하고 256비트 키로 강력한 보안을 보장합니다.
> 3. **융합**: TLS 1.3, WireGuard VPN, SSH, HTTP/2, QUIC 등에서广泛하게 사용되며, Google, Cloudflare, Apple 등이 주요 채택자입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**ChaCha20**
- **정의**: Daniel J. Bernstein이 2008년 설계한 스트림 암호
- **기반**: Salsa20의 변형 (Quarter Round 개선)
- **키 길이**: 256비트
- **Nonce**: 96비트
- **블록 카운터**: 32비트
- **구조**: ARX (Add-Rotate-XOR)

**Poly1305**
- **정의**: Daniel J. Bernstein이 설계한 MAC(Message Authentication Code)
- **기반**: 유한체 위의 다항식 인증
- **키 길이**: 256비트 (r: 128비트, s: 128비트)
- **출력**: 128비트 태그

**ChaCha20-Poly1305 (AEAD)**
- **정의**: ChaCha20 암호화 + Poly1305 인증을 결합한 AEAD
- **입력**: 256비트 키, 96비트 nonce, 평문, AAD
- **출력**: 암호문 + 128비트 인증 태그
- **RFC**: RFC 8439 (2018)

#### 2. 비유를 통한 이해
ChaCha20-Poly1305는 **'자동으로 봉투를 밀랍으로 봉하는 편지'**에 비유할 수 있습니다:

```
ChaCha20 (암호화):
[편지 내용] → [비밀번호로 섞기] → [아무도 읽을 수 없는 암호문]

Poly1305 (인증):
[암호문] → [특수 밀랍으로 봉인] → [봉투가 뜯겼는지 확인 가능]

ChaCha20-Poly1305:
[편지] → [섞기 + 밀랍 봉인] → [안전하고 무결한 전달]
```

AES vs ChaCha20 비유:
- AES: 정교한 금고 (하드웨어 가속 필요)
- ChaCha20: 가볍고 튼튼한 자물쇠 (소프트웨어만으로 빠름)

#### 3. 등장 배경 및 발전 과정

| 연도 | 사건 | 의미 |
|:---|:---|:---|
| **2005** | Salsa20 설계 | Bernstein, eSTREAM 프로젝트 |
| **2008** | ChaCha20 설계 | Salsa20 변형, 보안 강화 |
| **2014** | Google 채택 | Chrome, Android에서 TLS에 사용 |
| **2015** | RFC 7539 | ChaCha20-Poly1305 표준화 |
| **2016** | WireGuard | VPN 프로토콜에 채택 |
| **2018** | TLS 1.3 | 필수 cipher suite로 지정 |
| **2018** | RFC 8439 | RFC 7539 개정 |

**등장 배경**:
1. **AES 타이밍 공격**: AES는 테이블 조회 기반으로 캐시 타이밍 공격 취약
2. **모바일/IoT 성능**: AES-NI 없는 ARM 기기에서 AES 성능 저하
3. **소프트웨어 구현**: 일정 시간(constant-time) 구현 용이

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. ChaCha20 내부 구조

```text
                    [ ChaCha20 State Matrix ]

초기 상태 (512비트 = 16 × 32비트):
┌────────────┬────────────┬────────────┬────────────┐
│ 0x61707865 │ 0x3320646e │ 0x79622d32 │ 0x6b206574 │  ← Constants ("expand 32-byte k")
├────────────┼────────────┼────────────┼────────────┤
│    Key     │    Key     │    Key     │    Key     │  ← 256비트 키 (8 words)
├────────────┼────────────┼────────────┼────────────┤
│    Key     │    Key     │    Key     │    Key     │
├────────────┼────────────┼────────────┼────────────┤
│  Counter   │   Nonce    │   Nonce    │   Nonce    │  ← 32비트 카운터 + 96비트 nonce
└────────────┴────────────┴────────────┴────────────┘

Quarter Round (핵심 연산):
  a += b; d ^= a; d <<<= 16;
  c += d; b ^= c; b <<<= 12;
  a += b; d ^= a; d <<<= 8;
  c += d; b ^= c; b <<<= 7;

ChaCha20 라운드 (20라운드 = 10 double-rounds):
  - Column Rounds: (0,4,8,12), (1,5,9,13), (2,6,10,14), (3,7,11,15)
  - Diagonal Rounds: (0,5,10,15), (1,6,11,12), (2,7,8,13), (3,4,9,14)
```

#### 2. ChaCha20-Poly1305 AEAD 구조

```text
                    [ ChaCha20-Poly1305 AEAD ]

입력:
┌──────────────────────────────────────────────────────────┐
│  Key (256비트)    Nonce (96비트)                          │
├──────────────────────────────────────────────────────────┤
│  AAD (Additional Authenticated Data)                     │
├──────────────────────────────────────────────────────────┤
│  Plaintext (가변 길이)                                    │
└──────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────┐
│                    ChaCha20 암호화                        │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ 1. 초기 상태 생성 (Key || Nonce || Counter=0)      │ │
│  │ 2. Poly1305 키 생성 (첫 64바이트 키스트림)          │ │
│  │ 3. Counter=1부터 평문 암호화                        │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────┐
│                    Poly1305 인증                         │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Poly1305(                                         │ │
│  │   AAD || pad16(AAD) ||                            │ │
│  │   Ciphertext || pad16(Ciphertext) ||              │ │
│  │   len(AAD) || len(Ciphertext)                     │ │
│  │ )                                                  │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
                              │
                              ▼
출력:
┌──────────────────────────────────────────────────────────┐
│  Ciphertext || Tag (128비트)                             │
└──────────────────────────────────────────────────────────┘
```

#### 3. 구성 요소 상세 분석

| 구성 요소 | 입력 | 출력 | 역할 | 특성 |
|:---|:---|:---|:---|:---|
| **Constants** | - | 128비트 | 알고리즘 식별 | "expand 32-byte k" |
| **Key** | 256비트 | - | 암호화 키 | 랜덤 생성 |
| **Nonce** | 96비트 | - | 일회용 번호 | 키별 유일성 필수 |
| **Counter** | 32비트 | - | 블록 카운터 | 0부터 증가 |
| **Quarter Round** | 4 words | 4 words | 기본 연산 단위 | ARX 구조 |
| **Poly1305 Key** | 256비트 | - | MAC 키 | ChaCha20에서 파생 |
| **Tag** | - | 128비트 | 인증 태그 | 무결성 보장 |

#### 4. 핵심 알고리즘 & 실무 코드

```python
import struct
from typing import Tuple

class ChaCha20:
    """ChaCha20 스트림 암호 구현"""

    # Constants: "expand 32-byte k"
    CONSTANTS = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]

    @staticmethod
    def rotl32(v: int, c: int) -> int:
        """32비트 왼쪽 회전"""
        return ((v << c) | (v >> (32 - c))) & 0xFFFFFFFF

    @staticmethod
    def quarter_round(state: list, a: int, b: int, c: int, d: int):
        """쿼터 라운드 (핵심 연산)"""
        state[a] = (state[a] + state[b]) & 0xFFFFFFFF
        state[d] ^= state[a]
        state[d] = ChaCha20.rotl32(state[d], 16)

        state[c] = (state[c] + state[d]) & 0xFFFFFFFF
        state[b] ^= state[c]
        state[b] = ChaCha20.rotl32(state[b], 12)

        state[a] = (state[a] + state[b]) & 0xFFFFFFFF
        state[d] ^= state[a]
        state[d] = ChaCha20.rotl32(state[d], 8)

        state[c] = (state[c] + state[d]) & 0xFFFFFFFF
        state[b] ^= state[c]
        state[b] = ChaCha20.rotl32(state[b], 7)

    @staticmethod
    def chacha20_block(key: bytes, counter: int, nonce: bytes) -> bytes:
        """
        ChaCha20 블록 함수
        64바이트 키스트림 생성

        Args:
            key: 32바이트 키
            counter: 32비트 블록 카운터
            nonce: 12바이트 nonce
        """
        # 초기 상태 구성
        state = list(ChaCha20.CONSTANTS)

        # 키 (8 words)
        for i in range(8):
            state.append(struct.unpack('<I', key[i*4:(i+1)*4])[0])

        # 카운터 + 논스 (4 words)
        state.append(counter & 0xFFFFFFFF)
        for i in range(3):
            state.append(struct.unpack('<I', nonce[i*4:(i+1)*4])[0])

        # 작업용 상태
        working = state[:]

        # 20 라운드 (10 double rounds)
        for _ in range(10):
            # Column rounds
            ChaCha20.quarter_round(working, 0, 4, 8, 12)
            ChaCha20.quarter_round(working, 1, 5, 9, 13)
            ChaCha20.quarter_round(working, 2, 6, 10, 14)
            ChaCha20.quarter_round(working, 3, 7, 11, 15)
            # Diagonal rounds
            ChaCha20.quarter_round(working, 0, 5, 10, 15)
            ChaCha20.quarter_round(working, 1, 6, 11, 12)
            ChaCha20.quarter_round(working, 2, 7, 8, 13)
            ChaCha20.quarter_round(working, 3, 4, 9, 14)

        # 입력 상태 더하기
        for i in range(16):
            working[i] = (working[i] + state[i]) & 0xFFFFFFFF

        # 바이트로 변환
        return b''.join(struct.pack('<I', w) for w in working)

    @staticmethod
    def chacha20_encrypt(key: bytes, counter: int, nonce: bytes,
                         plaintext: bytes) -> bytes:
        """
        ChaCha20 암호화/복호화 (동일)

        Args:
            key: 32바이트 키
            counter: 초기 카운터
            nonce: 12바이트 nonce
            plaintext: 평문
        """
        ciphertext = b''
        for i in range(0, len(plaintext), 64):
            block = ChaCha20.chacha20_block(key, counter + i // 64, nonce)
            chunk = plaintext[i:i+64]
            ciphertext += bytes(a ^ b for a, b in zip(chunk, block))
        return ciphertext


class Poly1305:
    """Poly1305 MAC 구현"""

    @staticmethod
    def poly1305_mac(msg: bytes, key: bytes) -> bytes:
        """
        Poly1305 메시지 인증 코드

        Args:
            msg: 메시지
            key: 32바이트 키 (r || s)

        Returns:
            16바이트 태그
        """
        # r, s 분리
        r = int.from_bytes(key[:16], 'little')
        s = int.from_bytes(key[16:], 'little')

        # r 클램핑 (Clamping)
        r &= 0x0ffffffc0ffffffc0ffffffc0fffffff

        # 소수 p = 2^130 - 5
        p = (1 << 130) - 5

        # 다항식 계산
        acc = 0
        for i in range(0, len(msg), 16):
            block = msg[i:i+16]
            # 블록을 숫자로 변환 (128비트 + 1비트 패딩)
            n = int.from_bytes(block, 'little')
            n += 1 << (8 * len(block))  # 패딩 비트 추가
            acc = ((acc + n) * r) % p

        # 태그 계산
        tag = (acc + s) & ((1 << 128) - 1)
        return tag.to_bytes(16, 'little')


class ChaCha20Poly1305:
    """ChaCha20-Poly1305 AEAD 구현"""

    @staticmethod
    def encrypt(key: bytes, nonce: bytes, plaintext: bytes,
                aad: bytes = b'') -> Tuple[bytes, bytes]:
        """
        AEAD 암호화

        Args:
            key: 32바이트 키
            nonce: 12바이트 nonce
            plaintext: 평문
            aad: Additional Authenticated Data

        Returns:
            (ciphertext, tag)
        """
        # 1. Poly1305 키 생성 (counter=0)
        poly_key = ChaCha20.chacha20_block(key, 0, nonce)[:32]

        # 2. 평문 암호화 (counter=1부터)
        ciphertext = ChaCha20.chacha20_encrypt(key, 1, nonce, plaintext)

        # 3. Poly1305 인증 데이터 구성
        aad_padded = aad + b'\x00' * ((16 - len(aad) % 16) % 16)
        ct_padded = ciphertext + b'\x00' * ((16 - len(ciphertext) % 16) % 16)

        auth_data = (
            aad_padded +
            ct_padded +
            struct.pack('<Q', len(aad)) +
            struct.pack('<Q', len(ciphertext))
        )

        # 4. 태그 계산
        tag = Poly1305.poly1305_mac(auth_data, poly_key)

        return ciphertext, tag

    @staticmethod
    def decrypt(key: bytes, nonce: bytes, ciphertext: bytes,
                tag: bytes, aad: bytes = b'') -> bytes:
        """
        AEAD 복호화

        Args:
            key: 32바이트 키
            nonce: 12바이트 nonce
            ciphertext: 암호문
            tag: 16바이트 인증 태그
            aad: Additional Authenticated Data

        Returns:
            평문 (인증 실패 시 예외)

        Raises:
            ValueError: 인증 태그 불일치
        """
        import hmac

        # 1. Poly1305 키 생성
        poly_key = ChaCha20.chacha20_block(key, 0, nonce)[:32]

        # 2. 태그 재계산
        aad_padded = aad + b'\x00' * ((16 - len(aad) % 16) % 16)
        ct_padded = ciphertext + b'\x00' * ((16 - len(ciphertext) % 16) % 16)

        auth_data = (
            aad_padded +
            ct_padded +
            struct.pack('<Q', len(aad)) +
            struct.pack('<Q', len(ciphertext))
        )

        expected_tag = Poly1305.poly1305_mac(auth_data, poly_key)

        # 3. 태그 검증 (constant-time comparison)
        if not hmac.compare_digest(tag, expected_tag):
            raise ValueError("Authentication tag verification failed")

        # 4. 복호화
        plaintext = ChaCha20.chacha20_encrypt(key, 1, nonce, ciphertext)

        return plaintext


# 사용 예시
if __name__ == "__main__":
    import secrets

    # 키 및 논스 생성
    key = secrets.token_bytes(32)  # 256비트
    nonce = secrets.token_bytes(12)  # 96비트

    # 암호화할 데이터
    plaintext = b"Hello, ChaCha20-Poly1305! This is a secret message."
    aad = b"Additional authenticated data (e.g., headers)"

    # 암호화
    ciphertext, tag = ChaCha20Poly1305.encrypt(key, nonce, plaintext, aad)

    print(f"평문: {plaintext}")
    print(f"암호문: {ciphertext.hex()}")
    print(f"태그: {tag.hex()}")

    # 복호화
    decrypted = ChaCha20Poly1305.decrypt(key, nonce, ciphertext, tag, aad)
    print(f"복호문: {decrypted}")

    # 검증
    assert plaintext == decrypted
    print("검증 성공!")

    # 변조 감지 테스트
    try:
        tampered_ct = bytearray(ciphertext)
        tampered_ct[0] ^= 0xFF
        ChaCha20Poly1305.decrypt(key, nonce, bytes(tampered_ct), tag, aad)
        print("ERROR: 변조 감지 실패")
    except ValueError:
        print("변조 감지 성공!")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. AEAD 알고리즘 비교

| 특성 | AES-GCM | ChaCha20-Poly1305 |
|:---|:---|:---|
| **암호화** | 블록 암호 (AES) | 스트림 암호 (ChaCha20) |
| **인증** | GHASH (Galois Field) | Poly1305 (다항식) |
| **키 길이** | 128/192/256비트 | 256비트 |
| **Nonce** | 96비트 (IV) | 96비트 |
| **태그** | 128비트 | 128비트 |
| **하드웨어 가속** | AES-NI | 없음 |
| **소프트웨어 성능** | 느림 (AES-NI 없을 시) | 빠름 |
| **Side-channel** | 캐시 타이밍 취약 | 강건 |
| **Nonce 재사용** | 치명적 | 치명적 |

#### 2. 성능 비교 (ARM Cortex-A8)

| 알고리즘 | 사이클/바이트 | 상대 속도 |
|:---|:---|:---|
| AES-128-CBC | 25.6 | 1.0x |
| AES-256-CBC | 35.2 | 0.7x |
| AES-128-GCM | 30.1 | 0.9x |
| **ChaCha20-Poly1305** | **8.2** | **3.1x** |

#### 3. 과목 융합 관점 분석

- **네트워크**: TLS 1.3 cipher suite, QUIC, WireGuard
- **모바일/IoT**: ARM 기기에서 AES-NI 없을 때 최적 선택
- **클라우드**: Google, Cloudflare CDN 기본 사용
- **VPN**: WireGuard, Tailscale, OpenVPN (옵션)
- **SSH**: OpenSSH 6.9+ 지원

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 모바일 앱 통신 보안**
- 상황: iOS/Android 앱, AES-NI 미지원 기기 존재
- 판단: ChaCha20-Poly1305 기본 사용
- 핵심 결정:
  - TLS 1.3으로 ChaCha20-Poly1305 우선
  - 서버: OpenSSL 1.1.0+ 필요
  - 클라이언트: iOS 9+, Android 5.0+ 지원
- 효과: 배터리 30% 절감, 응답 시간 20% 단축

**시나리오 2: IoT 디바이스 통신**
- 상황: ARM Cortex-M4, 256KB RAM, TLS 필요
- 판단: ChaCha20-Poly1305 + TLS 1.3 (mbedtls)
- 핵심 결정:
  - 코드 크기: AES 대비 50% 작음
  - RAM 사용: 64바이트 state만 필요
  - 전력 소모: 현저히 낮음
- 효과: 저사양 IoT에서 보안 통신 구현

**시나리오 3: 서버 간 고속 통신**
- 상황: x86 서버, AES-NI 지원, 고처리량 필요
- 판단: AES-GCM 사용 (AES-NI 활용)
- 핵심 결정:
  - 하드웨어 가속 시 AES-GCM이 더 빠름
  - ChaCha20-Poly1305는 fallback으로 유지
- 효과: 최대 처리량 달성

#### 2. 도입 시 고려사항 (체크리스트)

**보안 체크리스트**
- [ ] Nonce 재사용 방지 (카운터 또는 랜덤 + 중복 체크)
- [ ] 키는 256비트 랜덤 사용
- [ ] 태그 검증 실패 시 평문 폐기
- [ ] Constant-time 비교 사용

**운영 체크리스트**
- [ ] TLS 1.3 지원 서버/클라이언트
- [ ] 라이브러리 버전 확인 (OpenSSL 1.1.0+)
- [ ] Fallback cipher suite 준비
- [ ] 성능 모니터링

#### 3. 안티패턴 (Anti-patterns)

| 안티패턴 | 문제점 | 올바른 접근 |
|:---|:---|:---|
| **Nonce 재사용** | 태그 위조 가능 | 키별 카운터 또는 랜덤+체크 |
| **태그 무시** | 무결성 보장 없음 | 태그 검증 필수 |
| **AAD 미사용** | 헤더 변조 가능 | 중요 메타데이터 AAD 포함 |
| **직접 구현** | 구현 오류 위험 | 검증된 라이브러리 사용 |

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | AES-GCM 대비 |
|:---|:---|
| 성능 (소프트웨어) | 3배 향상 |
| 배터리 (모바일) | 30% 절감 |
| Side-channel | 강건 |
| 코드 크기 | 50% 감소 |

#### 2. 미래 전망 및 진화 방향

- **TLS 1.3 필수**: 모든 TLS 1.3 구현에 필수 cipher suite
- **QUIC 표준**: HTTP/3 기본 암호화
- **Post-Quantum**: 양자 내성 KEM과 결합 가능
- **경량화**: 더 작은 변형 (ChaCha12, ChaCha8) 연구

#### 3. 참고 표준/가이드

- **RFC 8439**: ChaCha20 and Poly1305
- **RFC 7905**: ChaCha20-Poly1305 Cipher Suites for TLS
- **RFC 8446**: TLS 1.3 (필수 cipher suite)
- **NIST SP 800-202**: Guidelines on Using ChaCha

---

### 관련 개념 맵 (Knowledge Graph)

- [AES](@/studynotes/09_security/02_crypto/aes.md) : 대안 블록 암호
- [GCM](@/studynotes/09_security/02_crypto/gcm.md) : 대안 AEAD 모드
- [TLS 1.3](@/studynotes/09_security/03_network_security/tls13.md) : 주요 사용처
- [MAC](@/studynotes/09_security/02_crypto/mac.md) : Poly1305 기반
- [WireGuard](@/studynotes/09_security/03_network_security/wireguard.md) : VPN 활용

---

### 어린이를 위한 3줄 비유 설명

1. **섞기와 도장**: 편지를 아주 복잡하게 섞어서 아무도 읽을 수 없게 해요. 그리고 특별한 도장을 찍어서 중간에 누가 뜯었는지 알 수 있어요.
2. **빠른 가위**: AES는 커다란 금고인데, ChaCha20은 빠르고 날렵한 가위예요. 종이를 자르듯 빠르게 데이터를 섞을 수 있죠.
3. **작고 튼튼**: 아주 작은 기계에서도 잘 돌아가요. 스마트워치나 작은 센서도 이 암호를 쓸 수 있어요. 가볍지만 아주 튼튼하죠.
