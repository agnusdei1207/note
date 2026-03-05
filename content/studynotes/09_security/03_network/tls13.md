+++
title = "TLS 1.3 (Transport Layer Security)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# TLS 1.3 (Transport Layer Security)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인터넷 보안 통신의 핵심 프로토콜로, 1-RTT 핸드쉐이크, 전방 비밀성(PFS) 필수화, 레거시 암호 제거로 보안성과 성능을 동시에 혁신한 2018년 표준입니다.
> 2. **가치**: 핸드쉐이크 지연 50% 단축, 0-RTT 재연결, 모든 레거시 취약점(POODLE, BEAST, etc.) 근본 제거로 현대적 HTTPS의 기반이 되었습니다.
> 3. **융합**: ECDHE 필수, AES-GCM/ChaCha20-Poly1305 AEAD만 허용, HSTS/CT와 결합하여 웹 보안 생태계 전반을 재정의합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**TLS 1.3**은 IETF에서 2018년 8월 RFC 8446으로 표준화된 전송 계층 보안 프로토콜입니다. 이전 버전(TLS 1.2 이하)의 모든 안전하지 않은 알고리즘과 설계 결함을 제거하고, 현대적 암호학적 모범 사례를 적용했습니다.

```
TLS 1.3 핵심 변화:
1. 핸드쉐이크 간소화: 2-RTT → 1-RTT (또는 0-RTT)
2. 레거시 제거: RSA 키 교환, CBC 모드, MD5, SHA-1 등 금지
3. PFS 필수: 모든 키 교환은 (EC)DHE
4. 암호화 확장: 핸드쉐이크 메시지도 암호화
5. 세션 재개: Session Ticket + 0-RTT
```

#### 2. 비유를 통한 이해
TLS 1.3은 **'여권 검사 개선'**에 비유할 수 있습니다.

- **TLS 1.2**: 입국 심사 2번 거쳐야 함, 여권만 보여주면 됨
- **TLS 1.3**: 입국 심사 1번으로 통합, 생체 인식(강력한 인증) 필수

#### 3. 등장 배경 및 발전 과정
1. **1994년**: SSL 1.0 (내부용, 미공개)
2. **1995년**: SSL 2.0 (Netscape)
3. **1996년**: SSL 3.0
4. **1999년**: TLS 1.0 (RFC 2246)
5. **2006년**: TLS 1.1 (RFC 4346)
6. **2008년**: TLS 1.2 (RFC 5246) - SHA-256, GCM 추가
7. **2014년**: TLS 1.3 작업 시작 (IETF 90)
8. **2018년**: TLS 1.3 (RFC 8446) - 완전 재설계
9. **2020년**: TLS 1.2/1.0 지원 중단 가속화

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. TLS 1.2 vs TLS 1.3 핸드쉐이크 비교

```
=== TLS 1.2 핸드쉐이크 (2-RTT) ===

Client                                              Server
   │                                                   │
   │  1. ClientHello                                   │
   │     - Random                                      │
   │     - Cipher Suites (RSA, DHE, ECDHE...)         │
   │     - Extensions                                  │
   │─────────────────────────────────────────────────►│
   │                                                   │
   │  2. ServerHello                                   │
   │     - Random                                      │
   │     - Selected Cipher Suite                       │
   │  ─────────────────────────────────────────────    │
   │  3. Certificate                                   │
   │  ─────────────────────────────────────────────    │
   │  4. ServerKeyExchange (if DHE/ECDHE)              │
   │  ─────────────────────────────────────────────    │
   │  5. ServerHelloDone                               │
   │◄─────────────────────────────────────────────────│
   │                                                   │
   │  6. ClientKeyExchange                             │
   │     (PremasterSecret 전송)                        │
   │  ─────────────────────────────────────────────    │
   │  7. ChangeCipherSpec                              │
   │  ─────────────────────────────────────────────    │
   │  8. Finished                                      │
   │─────────────────────────────────────────────────►│
   │                                                   │
   │  9. ChangeCipherSpec                              │
   │  ─────────────────────────────────────────────    │
   │  10. Finished                                     │
   │◄─────────────────────────────────────────────────│
   │                                                   │
   │  === 암호화된 데이터 통신 ===                     │
   │◄────────────────────────────────────────────────►│

문제점:
- 2-RTT 필요 (지연 발생)
- ServerHello 후 메시지가 평문
- RSA 키 교환 허용 (PFS 없음)
- 불필요한 ChangeCipherSpec 메시지

===========================================

=== TLS 1.3 핸드쉐이크 (1-RTT) ===

Client                                              Server
   │                                                   │
   │  1. ClientHello                                   │
   │     - Random                                      │
   │     - Key Share (Client ECDHE Public)            │
   │     - Supported Groups, Signatures               │
   │     - PSK (if available)                          │
   │─────────────────────────────────────────────────►│
   │                                                   │
   │         [이 시점에서 Server는 공유 비밀 계산 가능]│
   │                                                   │
   │  2. ServerHello                                   │
   │     - Random                                      │
   │     - Key Share (Server ECDHE Public)            │
   │     - Selected Cipher Suite (AEAD only)          │
   │  ═════════════════════════════════════════════    │
   │  3. {EncryptedExtensions}     ← 암호화 시작!      │
   │  ═════════════════════════════════════════════    │
   │  4. {Certificate}                                 │
   │  ═════════════════════════════════════════════    │
   │  5. {CertificateVerify}                           │
   │  ═════════════════════════════════════════════    │
   │  6. {Finished}                                    │
   │◄─────────────────────────────────────────────────│
   │                                                   │
   │         [이 시점에서 Client도 공유 비밀 계산]     │
   │                                                   │
   │  7. {Finished}                                    │
   │─────────────────────────────────────────────────►│
   │                                                   │
   │  === 암호화된 데이터 통신 ===                     │
   │◄────────────────────────────────────────────────►│

개선점:
- 1-RTT로 단축
- ServerHello 직후 모든 메시지 암호화
- ECDHE 필수 (PFS 보장)
- ChangeCipherSpec 제거
- Certificate 메시지도 암호화됨!
```

#### 2. TLS 1.3 암호 스위트

| 암호 스위트 | 키 교환 | 인증 | 대칭 암호 | 해시 |
|:---|:---|:---|:---|:---|
| TLS_AES_128_GCM_SHA256 | ECDHE | RSA/ECDSA | AES-128-GCM | SHA-256 |
| TLS_AES_256_GCM_SHA384 | ECDHE | RSA/ECDSA | AES-256-GCM | SHA-384 |
| TLS_CHACHA20_POLY1305_SHA256 | ECDHE | RSA/ECDSA | ChaCha20-Poly1305 | SHA-256 |
| TLS_AES_128_CCM_SHA256 | ECDHE | RSA/ECDSA | AES-128-CCM | SHA-256 |

**TLS 1.3에서 제거된 것들:**
- RSA 키 교환 (PFS 없음)
- DH (static)
- 3DES, RC4, DES
- CBC 모드
- MD5, SHA-1
- Compression
- Renegotiation
- Non-AEAD ciphers

#### 3. 0-RTT (Zero Round Trip Time) 재연결

```
=== TLS 1.3 0-RTT 연결 ===

         Client                                    Server
           │                                        │
           │  이전 연결에서 받은 PSK 사용           │
           │                                        │
           │  1. ClientHello                        │
           │     + Key Share                        │
           │     + Pre-Shared Key                   │
           │     + Early Data (0-RTT Data!)         │
           │────────────────────────────────────►  │
           │                                        │
           │  ⚡ 서버 검증 없이 즉시 데이터 전송!   │
           │                                        │
           │  2. ServerHello                        │
           │     + Key Share                        │
           │  ═══════════════════════════════════   │
           │  3. {EncryptedExtensions}              │
           │     + early_data indication            │
           │  ═══════════════════════════════════   │
           │  4. {Finished}                         │
           │◄────────────────────────────────────  │
           │                                        │
           │  5. {Finished}                         │
           │────────────────────────────────────►  │
           │                                        │
           │  === 일반 암호화 통신 ===              │

0-RTT 특징:
✓ 연결 재개 시 즉시 데이터 전송 (0 RTT)
✓ 성능 대폭 개선 (모바일, CDN에 유리)
⚠ 재생 공격(replay) 가능 → 멱등성 필요
```

#### 4. 심층 동작 원리: TLS 1.3 Key Schedule

```python
"""
TLS 1.3 Key Schedule 구현 (RFC 8446)
"""

import hashlib
import hmac
import os
from typing import Tuple, Optional

class TLS13KeySchedule:
    """
    TLS 1.3 키 유도 체계

    HKDF 기반:
    - Early Secret (PSK용)
    - Handshake Secret (ECDHE로 유도)
    - Master Secret (응용 데이터용)
    """

    HASH_LEN = 32  # SHA-256

    def __init__(self):
        self.early_secret: Optional[bytes] = None
        self.handshake_secret: Optional[bytes] = None
        self.master_secret: Optional[bytes] = None

    @staticmethod
    def hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
        """HKDF-Extract: PRK = HMAC-Hash(salt, IKM)"""
        if salt is None or len(salt) == 0:
            salt = b'\x00' * TLS13KeySchedule.HASH_LEN
        return hmac.new(salt, ikm, hashlib.sha256).digest()

    @staticmethod
    def hkdf_expand(prk: bytes, info: bytes, length: int) -> bytes:
        """HKDF-Expand"""
        hash_len = TLS13KeySchedule.HASH_LEN
        n = (length + hash_len - 1) // hash_len

        okm = b''
        prev = b''
        for i in range(1, n + 1):
            prev = hmac.new(prk, prev + info + bytes([i]), hashlib.sha256).digest()
            okm += prev
        return okm[:length]

    @staticmethod
    def hkdf_expand_label(secret: bytes, label: str, context: bytes, length: int) -> bytes:
        """
        TLS 1.3 HKDF-Expand-Label

        struct {
            uint16 length = Length;
            opaque label<7..255> = "tls13 " + Label;
            opaque context<0..255> = Context;
        } HkdfLabel;
        """
        tls13_label = f"tls13 {label}".encode()
        info = (
            length.to_bytes(2, 'big') +
            bytes([len(tls13_label)]) + tls13_label +
            bytes([len(context)]) + context
        )
        return TLS13KeySchedule.hkdf_expand(secret, info, length)

    @staticmethod
    def derive_secret(secret: bytes, label: str, messages: bytes) -> bytes:
        """Derive-Secret: HKDF-Expand-Label(secret, label, Hash(messages))"""
        transcript_hash = hashlib.sha256(messages).digest()
        return TLS13KeySchedule.hkdf_expand_label(secret, label, transcript_hash, TLS13KeySchedule.HASH_LEN)

    def compute_handshake_secrets(self, shared_secret: bytes,
                                   client_hello: bytes,
                                   server_hello: bytes) -> dict:
        """
        Handshake Secret 계산

        1. early_secret = HKDF-Extract(0, 0)
        2. derived_secret = Derive-Secret(early_secret, "derived", "")
        3. handshake_secret = HKDF-Extract(derived_secret, shared_secret)
        4. client_hs_traffic = Derive-Secret(handshake_secret, "c hs traffic", ClientHello...ServerHello)
        5. server_hs_traffic = Derive-Secret(handshake_secret, "s hs traffic", ClientHello...ServerHello)
        """
        # Early Secret
        self.early_secret = self.hkdf_extract(b'', b'\x00' * self.HASH_LEN)

        # Derived Secret
        derived = self.derive_secret(self.early_secret, "derived", b'')

        # Handshake Secret
        self.handshake_secret = self.hkdf_extract(derived, shared_secret)

        # Traffic Secrets
        transcript = client_hello + server_hello
        client_hs_traffic = self.derive_secret(self.handshake_secret, "c hs traffic", transcript)
        server_hs_traffic = self.derive_secret(self.handshake_secret, "s hs traffic", transcript)

        return {
            'handshake_secret': self.handshake_secret,
            'client_handshake_traffic_secret': client_hs_traffic,
            'server_handshake_traffic_secret': server_hs_traffic,
        }

    def compute_master_secrets(self, handshake_messages: bytes) -> dict:
        """
        Master Secret 계산

        1. derived_secret = Derive-Secret(handshake_secret, "derived", "")
        2. master_secret = HKDF-Extract(derived_secret, 0)
        3. client_ap_traffic = Derive-Secret(master_secret, "c ap traffic", handshake_hash)
        4. server_ap_traffic = Derive-Secret(master_secret, "s ap traffic", handshake_hash)
        """
        # Derived Secret
        derived = self.derive_secret(self.handshake_secret, "derived", b'')

        # Master Secret
        self.master_secret = self.hkdf_extract(derived, b'\x00' * self.HASH_LEN)

        # Application Traffic Secrets
        client_ap_traffic = self.derive_secret(self.master_secret, "c ap traffic", handshake_messages)
        server_ap_traffic = self.derive_secret(self.master_secret, "s ap traffic", handshake_messages)

        return {
            'master_secret': self.master_secret,
            'client_application_traffic_secret': client_ap_traffic,
            'server_application_traffic_secret': server_ap_traffic,
        }

    @staticmethod
    def derive_traffic_key(traffic_secret: bytes) -> Tuple[bytes, bytes]:
        """Traffic Key와 IV 유도"""
        key = TLS13KeySchedule.hkdf_expand_label(traffic_secret, "key", b'', 16)
        iv = TLS13KeySchedule.hkdf_expand_label(traffic_secret, "iv", b'', 12)
        return key, iv


class TLS13RecordLayer:
    """
    TLS 1.3 Record Layer

    AEAD 암호화:
    - nonce = IV XOR sequence_number
    - additional_data = TLSCiphertext.opaque_type || TLSCiphertext.legacy_record_version || length
    """

    @staticmethod
    def encrypt(key: bytes, iv: bytes, sequence: int,
                content_type: int, plaintext: bytes) -> bytes:
        """
        TLS 1.3 Record 암호화

        结构:
        struct {
            opaque_type = application_data(23),
            legacy_record_version = 0x0303,
            length,
            encrypted_record
        } TLSCiphertext
        """
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM

        # Nonce = IV XOR sequence_number
        nonce = TLS13RecordLayer._compute_nonce(iv, sequence)

        # Additional Data (TLS 1.3에서는 비어있음!)
        # TLS 1.2와 달리 헤더를 포함하지 않음
        aad = b''

        # AEAD 암호화
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, plaintext, aad)

        # Content Type을 마지막에 추가
        ciphertext += bytes([content_type])

        # 레코드 구성
        record = bytes([23, 3, 3])  # type, version
        record += len(ciphertext).to_bytes(2, 'big')
        record += ciphertext

        return record

    @staticmethod
    def _compute_nonce(iv: bytes, sequence: int) -> bytes:
        """Nonce = IV XOR sequence_number (big-endian)"""
        nonce = bytearray(iv)
        seq_bytes = sequence.to_bytes(len(iv), 'big')
        for i in range(len(iv)):
            nonce[i] ^= seq_bytes[i]
        return bytes(nonce)


# 사용 예시
def tls13_handshake_demo():
    """TLS 1.3 핸드쉐이크 데모"""

    print("=" * 60)
    print("TLS 1.3 Key Schedule 데모")
    print("=" * 60)

    # 1. ECDHE 공유 비밀 (시뮬레이션)
    shared_secret = hashlib.sha256(b"ecdhe_shared_secret").digest()
    print(f"\n1. ECDHE 공유 비밀: {shared_secret.hex()[:32]}...")

    # 2. ClientHello, ServerHello (시뮬레이션)
    client_hello = b"ClientHello_message_content..."
    server_hello = b"ServerHello_message_content..."

    # 3. 키 스케줄 계산
    ks = TLS13KeySchedule()
    hs_secrets = ks.compute_handshake_secrets(shared_secret, client_hello, server_hello)

    print(f"\n2. Handshake Secret: {hs_secrets['handshake_secret'].hex()[:32]}...")
    print(f"   Client HS Traffic: {hs_secrets['client_handshake_traffic_secret'].hex()[:32]}...")
    print(f"   Server HS Traffic: {hs_secrets['server_handshake_traffic_secret'].hex()[:32]}...")

    # 4. Master Secret
    handshake_messages = client_hello + server_hello + b"Certificate...Finished"
    ap_secrets = ks.compute_master_secrets(handshake_messages)

    print(f"\n3. Master Secret: {ap_secrets['master_secret'].hex()[:32]}...")
    print(f"   Client AP Traffic: {ap_secrets['client_application_traffic_secret'].hex()[:32]}...")
    print(f"   Server AP Traffic: {ap_secrets['server_application_traffic_secret'].hex()[:32]}...")

    # 5. Traffic Key 유도
    key, iv = TLS13KeySchedule.derive_traffic_key(ap_secrets['client_application_traffic_secret'])
    print(f"\n4. Traffic Key: {key.hex()}")
    print(f"   Traffic IV: {iv.hex()}")


def tls13_comparison():
    """TLS 1.2 vs TLS 1.3 비교"""
    print("\n" + "=" * 60)
    print("TLS 1.2 vs TLS 1.3 비교")
    print("=" * 60)

    comparisons = [
        ("핸드쉐이크 RTT", "2-RTT", "1-RTT"),
        ("0-RTT 재연결", "없음", "지원"),
        ("PFS", "선택적", "필수"),
        ("레거시 암호", "허용", "금지"),
        ("인증서 암호화", "평문", "암호화"),
        ("서버 검증", "완료 후", "ServerHello 직후"),
        ("지원 알고리즘", "37개", "5개"),
        ("복잡성", "높음", "낮음"),
    ]

    print(f"\n{'특성':<20} {'TLS 1.2':<20} {'TLS 1.3'}")
    print("-" * 60)
    for feature, v12, v13 in comparisons:
        print(f"{feature:<20} {v12:<20} {v13}")


if __name__ == "__main__":
    tls13_handshake_demo()
    tls13_comparison()
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. TLS 1.3 vs TLS 1.2 보안 비교

| 공격 | TLS 1.2 | TLS 1.3 |
|:---|:---:|:---:|
| **POODLE** | 취약 (SSL 3.0 fallback) | 안전 |
| **BEAST** | 취약 (CBC) | 안전 |
| **CRIME** | 취약 (compression) | 안전 |
| **Heartbleed** | 취약 (구현) | 안전 |
| **Logjam** | 취약 (DH-1024) | 안전 |
| **DROWN** | 취약 (SSL 2.0) | 안전 |
| **ROBOT** | 취약 (RSA) | 안전 |
| **Downgrade** | 취약 | 안전 (signature) |

#### 2. 성능 비교

| 지표 | TLS 1.2 | TLS 1.3 | 개선 |
|:---|:---|:---|:---:|
| **핸드쉐이크 RTT** | 2 | 1 | 50% |
| **재연결** | 1-RTT | 0-RTT | 100% |
| **CPU 오버헤드** | 중간 | 낮음 | 30% |
| **처리량** | 100% | 105-110% | +5-10% |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 웹 서버 TLS 1.3 도입**
```nginx
# Nginx TLS 1.3 설정
ssl_protocols TLSv1.3 TLSv1.2;  # 1.3 우선, 1.2 폴백
ssl_prefer_server_ciphers off;   # TLS 1.3은 무시됨
ssl_ciphers TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256;

# 0-RTT 활성화 (주의: replay 공격 고려)
ssl_early_data on;
```

**시나리오 2: 레거시 시스템 호환성**
- 상황: Java 8, Windows XP 등 TLS 1.3 미지원
- 판단: TLS 1.2 병행 지원, 점진적 전환
- 전략: User-Agent 기반 프로토콜 선택

#### 2. 0-RTT 보안 고려사항

```
0-RTT 위험:
1. 재생 공격 (Replay Attack)
   - 동일 요청이 여러 번 처리될 수 있음
   - 해결: 서버측 재생 캐시, 멱등성 보장

2. 전방 비밀성 없음
   - PSK 노출 시 0-RTT 데이터 복호화 가능
   - 해결: 짧은 PSK 수명, 민감 데이터 제외

0-RTT 안전 사용:
✓ GET 요청
✓ 멱등한 API
✓ 캐시 가능한 정적 리소스
✗ 결제 요청
✗ 비멱등 POST
✗ 상태 변경 요청
```

#### 3. 안티패턴 (Anti-patterns)

```
취약한 구현 (금지!)

1. TLS 1.3 미도입
   ❌ ssl_protocols TLSv1.2;
   → 레거시 공격에 취약

2. 불필요한 하위 호환
   ❌ ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
   → POODLE, BEAST 등에 노출

3. 0-RTT 무분별한 사용
   ❌ 모든 POST에 0-RTT 허용
   → 재생 공격으로 이중 결제 가능

올바른 구현:

1. TLS 1.3 우선
   ✓ ssl_protocols TLSv1.3 TLSv1.2;

2. 강력한 암호만
   ✓ ssl_ciphers TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256;

3. 0-RTT 신중 사용
   ✓ GET/HEAD만 0-RTT
   ✓ POST는 1-RTT 후 처리
```

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 | 항목 | 수치/내용 |
|:---|:---|:---|
| **성능** | 핸드쉐이크 | 50% 단축 |
| **보안** | 레거시 공격 | 100% 방지 |
| **규정** | PCI DSS | 4.1 준수 |
| **사용자** | 체감 속도 | 30% 향상 |

#### 2. 참고 표준/가이드

| 표준 | 내용 |
|:---|:---|
| **RFC 8446** | TLS 1.3 |
| **RFC 8446 Appendix E** | 0-RTT 보안 고려사항 |
| **RFC 8446 Appendix D** | TLS 1.2와의 차이점 |

---

### 관련 개념 맵 (Knowledge Graph)
- [전방 비밀성 (PFS)](@/studynotes/09_security/02_crypto/pfs.md) : TLS 1.3의 필수 속성
- [ECDH](@/studynotes/09_security/02_crypto/dh_ecdh.md) : TLS 1.3 키 교환
- [AES-GCM](@/studynotes/09_security/02_crypto/gcm.md) : TLS 1.3 AEAD
- [HSTS](@/studynotes/09_security/03_network/hsts.md) : HTTPS 강제
- [Certificate Transparency](@/studynotes/09_security/10_pki/ct.md) : 인증서 투명성

---

### 어린이를 위한 3줄 비유 설명
1. **빠른 인사**: TLS 1.3은 친구를 만날 때 한 번에 인사를 끝내요. 예전에는 두 번 인사를 해야 했는데, 이제는 한 번이면 돼요!
2. **비밀 편지**: 친구와 비밀 편지를 주고받을 때, 편지봉투만 보고도 누가 보냈는지 몰랐는데, 이제는 편지봉투마저 감춰서 보내요.
3. **다시 만날 때**: 친구를 다시 만나면 인사도 없이 바로 대화를 시작할 수 있어요. 이미 비밀 암호를 알고 있으니까요!
