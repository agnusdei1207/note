+++
title = "MAC / HMAC (메시지 인증 코드)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# MAC / HMAC (Message Authentication Code)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MAC은 비밀 키를 사용하여 메시지의 무결성과 인증을 동시에 보장하는 암호학적 코드이며, HMAC은 해시 함수 기반 MAC으로 RFC 2104 표준입니다.
> 2. **가치**: TLS, IPsec, JWT, API 인증에서 핵심적으로 사용되며, 중간자 공격, 메시지 변조를 방지합니다.
> 3. **융합**: HMAC-SHA256이 사실상 표준이며, CMAC, GMAC, Poly1305 등 다양한 MAC 변형이 존재합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**MAC (Message Authentication Code)**
- **정의**: 비밀 키와 메시지를 입력으로 받아 고정 길이 태그를 생성하는 암호학적 함수
- **목적**: 메시지 무결성 + 송신자 인증
- **속성**:
  - 키가 없으면 태그 생성 불가
  - 키가 없으면 태그 검증 불가
  - 같은 키로만 검증 가능

**HMAC (Hash-based MAC)**
- **정의**: 해시 함수를 이용한 MAC 구성 방식 (RFC 2104)
- **구조**: HMAC(K, m) = H((K ⊕ opad) || H((K ⊕ ipad) || m))
- **장점**: 어떤 해시 함수에도 적용 가능 (SHA-256, SHA-3, BLAKE2)

#### 2. 비유를 통한 이해
HMAC은 **'밀랍 봉인 + 비밀 문구'**에 비유할 수 있습니다:

```
일반 해시:
[편지] → [지문 찍기] → [누구나 확인 가능]

MAC/HMAC:
[편지] + [비밀 문구] → [밀랍 봉인] → [비밀 문구를 아는 사람만 확인 가능]
                      ↑
                 비밀 키 없이는 위조 불가
```

#### 3. MAC vs 해시 vs 서명

| 구분 | 목적 | 키 | 속도 | 사용처 |
|:---|:---|:---|:---|:---|
| **해시** | 무결성만 | 없음 | 매우 빠름 | 파일 무결성, 체크섬 |
| **MAC** | 무결성 + 인증 | 대칭키 | 빠름 | TLS, API 인증 |
| **서명** | 무결성 + 인증 + 부인방지 | 비대칭키 | 느림 | 계약서, 코드 서명 |

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. HMAC 구조

```text
                    [ HMAC 알고리즘 구조 ]

                    HMAC(K, m) = H((K ⊕ opad) || H((K ⊕ ipad) || m))

입력:
  K: 비밀 키
  m: 메시지
  H: 해시 함수 (SHA-256 등)
  B: 해시 블록 크기 (SHA-256: 64바이트)
  L: 해시 출력 크기 (SHA-256: 32바이트)

상수:
  ipad = 0x36 반복 (B바이트)
  opad = 0x5c 반복 (B바이트)

알고리즘:
1. K' = K가 B보다 길면 H(K), 짧으면 0 패딩
2. K'를 B바이트로 패딩

   ┌─────────────────────────────────────────────┐
   │                                             │
   │   ┌─────────────────────────────────────┐   │
   │   │          K' ⊕ ipad                  │   │
   │   │  (0x363636... XOR 키)               │   │
   │   └────────────────┬────────────────────┘   │
   │                    │                        │
   │                    ▼                        │
   │   ┌─────────────────────────────────────┐   │
   │   │              m (메시지)              │   │
   │   └────────────────┬────────────────────┘   │
   │                    │                        │
   │                    ▼                        │
   │   ┌─────────────────────────────────────┐   │
   │   │         H(K' ⊕ ipad || m)           │   │
   │   │           (내부 해시)                │   │
   │   └────────────────┬────────────────────┘   │
   │                    │                        │
   └────────────────────┼────────────────────────┘
                        │
                        ▼
   ┌─────────────────────────────────────────────┐
   │          K' ⊕ opad                         │
   │  (0x5c5c5c... XOR 키)                      │
   └────────────────┬────────────────────────────┘
                    │
                    ▼
   ┌─────────────────────────────────────────────┐
   │         H(K' ⊕ ipad || m)                  │
   └────────────────┬────────────────────────────┘
                    │
                    ▼
   ┌─────────────────────────────────────────────┐
   │    H((K' ⊕ opad) || H((K' ⊕ ipad) || m))   │
   │                 (외부 해시)                  │
   └────────────────┬────────────────────────────┘
                    │
                    ▼
             [ HMAC 태그 (L바이트) ]
```

#### 2. MAC 유형 비교

| 유형 | 기반 알고리즘 | 장점 | 단점 | 표준 |
|:---|:---|:---|:---|:---|
| **HMAC** | 해시 (SHA-256) | 범용, 빠름 | 해시 함수 의존 | RFC 2104 |
| **CMAC** | 블록 암호 (AES) | 하드웨어 친화적 | 블록 크기 제한 | NIST SP 800-38B |
| **GMAC** | GCM 모드 | 병렬 처리 | Nonce 재사용 치명 | NIST SP 800-38D |
| **Poly1305** | 다항식 | 매우 빠름 | 일회용 키 | RFC 8439 |
| **KMAC** | SHA-3 (Keccak) | 보안 강건 | 상대적 신규 | NIST SP 800-185 |

#### 3. 핵심 알고리즘 & 실무 코드

```python
import hashlib
import hmac
from typing import Union

class HMACImplementation:
    """HMAC 구현 (교육용)"""

    @staticmethod
    def hmac_sha256(key: bytes, message: bytes) -> bytes:
        """
        HMAC-SHA256 구현

        Args:
            key: 비밀 키
            message: 메시지

        Returns:
            32바이트 MAC 태그
        """
        # 해시 함수 블록 크기 (SHA-256: 64바이트)
        BLOCK_SIZE = 64

        # 키 전처리
        if len(key) > BLOCK_SIZE:
            key = hashlib.sha256(key).digest()
        if len(key) < BLOCK_SIZE:
            key = key + b'\x00' * (BLOCK_SIZE - len(key))

        # ipad, opad 생성
        ipad = bytes(b ^ 0x36 for b in key)
        opad = bytes(b ^ 0x5c for b in key)

        # 내부 해시
        inner_hash = hashlib.sha256(ipad + message).digest()

        # 외부 해시 (최종 MAC)
        outer_hash = hashlib.sha256(opad + inner_hash).digest()

        return outer_hash

    @staticmethod
    def verify_hmac(key: bytes, message: bytes,
                    received_mac: bytes) -> bool:
        """
        HMAC 검증 (Constant-time 비교)

        Args:
            key: 비밀 키
            message: 메시지
            received_mac: 수신한 MAC 태그

        Returns:
            검증 성공 여부
        """
        expected_mac = HMACImplementation.hmac_sha256(key, message)
        # Constant-time 비교 (타이밍 공격 방지)
        return hmac.compare_digest(expected_mac, received_mac)


class MACUtils:
    """MAC 유틸리티"""

    @staticmethod
    def hmac_sha256(key: Union[str, bytes],
                    message: Union[str, bytes]) -> str:
        """HMAC-SHA256 (표준 라이브러리)"""
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(message, str):
            message = message.encode('utf-8')
        return hmac.new(key, message, hashlib.sha256).hexdigest()

    @staticmethod
    def hmac_sha512(key: Union[str, bytes],
                    message: Union[str, bytes]) -> str:
        """HMAC-SHA512"""
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(message, str):
            message = message.encode('utf-8')
        return hmac.new(key, message, hashlib.sha512).hexdigest()

    @staticmethod
    def generate_key(length: int = 32) -> bytes:
        """안전한 MAC 키 생성"""
        import secrets
        return secrets.token_bytes(length)


class APIAuthenticator:
    """API 인증 (HMAC 기반)"""

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def generate_signature(self, method: str, path: str,
                           timestamp: str, body: str = "") -> str:
        """
        API 요청 서명 생성

        Args:
            method: HTTP 메서드 (GET, POST 등)
            path: 요청 경로
            timestamp: 타임스탬프
            body: 요청 본문

        Returns:
            서명 문자열
        """
        # 서명할 메시지 구성
        message = f"{method}\n{path}\n{timestamp}\n{body}"

        # HMAC-SHA256 서명
        signature = MACUtils.hmac_sha256(self.api_secret, message)

        return signature

    def verify_signature(self, method: str, path: str,
                         timestamp: str, body: str,
                         received_signature: str,
                         max_age_seconds: int = 300) -> bool:
        """
        API 요청 서명 검증

        Args:
            method: HTTP 메서드
            path: 요청 경로
            timestamp: 타임스탬프
            body: 요청 본문
            received_signature: 수신한 서명
            max_age_seconds: 최대 허용 시간 (초)

        Returns:
            검증 성공 여부
        """
        import time

        # 타임스탬프 검증 (Replay Attack 방지)
        try:
            ts = int(timestamp)
            if abs(time.time() - ts) > max_age_seconds:
                return False
        except ValueError:
            return False

        # 서명 생성 및 비교
        expected = self.generate_signature(method, path, timestamp, body)
        return hmac.compare_digest(expected, received_signature)


# 사용 예시
if __name__ == "__main__":
    print("=== HMAC-SHA256 예시 ===")
    key = b"secret_key_12345"
    message = b"Hello, HMAC!"

    # 직접 구현
    mac_direct = HMACImplementation.hmac_sha256(key, message)
    print(f"직접 구현: {mac_direct.hex()}")

    # 표준 라이브러리
    mac_std = MACUtils.hmac_sha256(key, message)
    print(f"표준 라이브러리: {mac_std}")

    # 검증
    is_valid = HMACImplementation.verify_hmac(key, message, mac_direct)
    print(f"검증: {'성공' if is_valid else '실패'}")

    print("\n=== API 인증 예시 ===")
    auth = APIAuthenticator("api_key_123", "api_secret_456")

    # 요청 서명
    signature = auth.generate_signature(
        method="POST",
        path="/api/v1/users",
        timestamp="1234567890",
        body='{"name": "test"}'
    )
    print(f"API 서명: {signature}")

    # 서명 검증
    is_valid = auth.verify_signature(
        method="POST",
        path="/api/v1/users",
        timestamp="1234567890",
        body='{"name": "test"}',
        received_signature=signature
    )
    print(f"API 검증: {'성공' if is_valid else '실패'}")
