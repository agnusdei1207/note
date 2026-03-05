+++
title = "키 유도 함수 (KDF) 및 패스워드 해싱"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# 키 유도 함수 (KDF) 및 패스워드 해싱

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: KDF는 비밀(패스워드, 마스터 키)로부터 암호학적으로 안전한 키를 유도하는 함수이며, 패스워드 해싱은 무차별 대입 공격을 느리게 만들기 위해 의도적으로 연산 비용을 높입니다.
> 2. **가치**: PBKDF2, bcrypt, scrypt, Argon2는 각각 CPU 비용, 메모리 비용, 병렬화 저항을 통해 무차별 대입 공격을 방어합니다.
> 3. **융합**: NIST 권장(Argon2id), OWASP 권장(Argon2/bcrypt), PKCS#5(PBKDF2) 등 표준화되어 있으며, TLS, WPA3, 디스크 암호화 등에 사용됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**KDF (Key Derivation Function)**
- **정의**: 입력 비밀(패스워드, 난수 시드)로부터 하나 이상의 암호학적 키를 유도하는 함수
- **용도**:
  - 패스워드 → 저장용 해시
  - 패스워드 → 암호화 키
  - 마스터 키 → 세션 키
  - Diffie-Hellman 공유 비밀 → 대칭 키

**패스워드 해싱 요구사항**
1. **느림 (Slow)**: 무차별 대입 공격 방어
2. **솔트 (Salt)**: 레인보우 테이블 방어
3. **메모리 비용**: GPU/ASIC 병렬화 방어
4. **조정 가능**: 하드웨어 발전에 대응

#### 2. KDF/패스워드 해싱 알고리즘 비교

| 알고리즘 | 연도 | CPU 비용 | 메모리 비용 | 병렬화 저항 | 상태 |
|:---|:---|:---|:---|:---|:---|
| **PBKDF2** | 2000 | O(반복) | 없음 | 낮음 | 레거시 |
| **bcrypt** | 1999 | O(반복) | 4KB | 중간 | 권장 |
| **scrypt** | 2009 | O(반복) | O(메모리) | 높음 | 권장 |
| **Argon2d** | 2015 | O(반복) | O(메모리) | 높음 | 권장 |
| **Argon2i** | 2015 | O(반복) | O(메모리) | 높음 | 권장 |
| **Argon2id** | 2015 | O(반복) | O(메모리) | 높음 | **최고 권장** |

#### 3. 비유를 통한 이해
패스워드 해싱은 **'보안 금고 여는 시간'**에 비유할 수 있습니다:

```
일반 해시 (SHA-256):
[비밀번호] → [빠른 확인] → [금고 열림]
문제: 1초에 수십억 번 시도 가능

패스워드 해싱 (Argon2):
[비밀번호] → [1초 대기] → [금고 열림]
장점: 1초에 1번만 시도 가능 → 공격자에게 치명적

추가 방어:
- 솔트: 각 금고마다 다른 열쇠 구멍
- 메모리: 금고를 열 때 큰 공간 필요 (GPU 사용 불가)
```

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. PBKDF2 구조

```text
                    [ PBKDF2 구조 ]

PBKDF2(PRF, Password, Salt, c, dkLen)

PRF: 의사난수 함수 (보통 HMAC-SHA256)
Password: 패스워드
Salt: 솔트 (최소 16바이트)
c: 반복 횟수 (최소 600,000회 for SHA-256)
dkLen: 유도할 키 길이

구조:
DK = T1 || T2 || ... || TdkLen/hlen

Ti = F(Password, Salt, c, i)

F(Password, Salt, c, i) = U1 ^ U2 ^ ... ^ Uc

U1 = PRF(Password, Salt || INT(i))
U2 = PRF(Password, U1)
...
Uc = PRF(Password, Uc-1)

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Password ──┐                                               │
│             │                                               │
│  Salt || i ─┼──► PRF ──► U1 ──► PRF ──► U2 ──► ... ──► Uc  │
│             │      │           │                           │
│             └──────┴───────────┴───────────────────────────│
│                                                             │
│  결과: U1 ⊕ U2 ⊕ ... ⊕ Uc                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 2. bcrypt 구조

```text
                    [ bcrypt 구조 ]

bcrypt(cost, salt, password)

cost: 비용 인자 (2^cost 라운드)
salt: 128비트 솔트
password: 최대 72바이트 패스워드

구조:
1. OrpheanBeholderScryDoubt (64비트 초기 상태)
2. EksBlowfishSetup(cost, salt, key)
   - Blowfish 키 스케줄 변형
   - 2^cost 라운드
3. 64비트 블록 3회 암호화

출력: $2b$cost$salt(22자)hash(31자)

예: $2b$12$GhvMmNVjRW29ulnudl.LbuAnUtN/LRfe1UiBvd8vTLoUt
    │   │   │                      │
    │   │   │                      └── 해시 (31자, 184비트)
    │   │   └── 솔트 (22자, 128비트 base64)
    │   └── 비용 인자 (2^12 = 4096 라운드)
    └── 버전
```

#### 3. Argon2 구조

```text
                    [ Argon2 구조 ]

Argon2d: 데이터 의존적 메모리 접근 (고성능, Side-channel 취약)
Argon2i: 데이터 독립적 메모리 접근 (Side-channel 강건)
Argon2id: 하이브리드 (1패스 i, 나머지 d) ← NIST 권장

입력 파라미터:
- t: 시간 비용 (패스 수)
- m: 메모리 비용 (KB)
- p: 병렬성 (스레드 수)
- password, salt, key, AD

내부 구조:
┌─────────────────────────────────────────────────────────────┐
│                      [메모리 블록 B]                         │
│   ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐        │
│   │ B0  │ B1  │ B2  │ B3  │ ... │     │     │Bm-1 │        │
│   └──┬──┴──┬──┴──┬──┴──┬──┴─────┴─────┴─────┴──┬──┘        │
│      │     │     │     │                       │           │
│      ▼     ▼     ▼     ▼                       ▼           │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              Compression Function G                  │   │
│   │   G(Bi) = H(Bi xor Bref1 xor Bref2 ...)             │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   패스 1 (Argon2i): 데이터 독립적 참조                       │
│   패스 2+ (Argon2d): 데이터 의존적 참조                      │
│                                                             │
│   최종 출력 = H(Bm-1)                                       │
└─────────────────────────────────────────────────────────────┘
```

#### 4. 핵심 알고리즘 & 실무 코드

```python
import hashlib
import os
import secrets
import base64
from typing import Tuple, Optional

class PBKDF2:
    """PBKDF2 구현"""

    @staticmethod
    def derive_key(password: str, salt: bytes,
                   iterations: int = 600000,
                   key_length: int = 32) -> bytes:
        """
        PBKDF2-HMAC-SHA256 키 유도

        Args:
            password: 패스워드
            salt: 솔트 (16바이트 이상 권장)
            iterations: 반복 횟수 (600,000 이상 권장)
            key_length: 유도할 키 길이 (바이트)

        Returns:
            유도된 키
        """
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            iterations,
            key_length
        )

    @staticmethod
    def generate_salt(length: int = 16) -> bytes:
        """솔트 생성"""
        return secrets.token_bytes(length)


class BcryptSimulation:
    """bcrypt 시뮬레이션 (실제는 bcrypt 라이브러리 사용 권장)"""

    # 실제 구현은 복잡하므로 개념적 시뮬레이션

    @staticmethod
    def hash_password(password: str, cost: int = 12) -> str:
        """
        bcrypt 패스워드 해싱 (시뮬레이션)

        실제 사용:
        import bcrypt
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
        """
        salt = secrets.token_bytes(16)
        # 시뮬레이션: 실제로는 EksBlowfishSetup 사용
        iterations = 2 ** cost
        key = hashlib.pbkdf2_hmac('sha256', password.encode(),
                                   salt, iterations, 24)
        salt_b64 = base64.b64encode(salt).decode('ascii')[:22]
        hash_b64 = base64.b64encode(key).decode('ascii')[:31]
        return f"$2b${cost}${salt_b64}${hash_b64}"

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """bcrypt 검증 (시뮬레이션)"""
        # 실제 구현에서는 저장된 솔트와 비용으로 재계산
        pass


class Argon2Config:
    """Argon2 설정 (권장값)"""

    # OWASP 권장 설정
    TIME_COST = 2          # 패스 수
    MEMORY_COST = 65536    # 64 MB
    PARALLELISM = 4        # 스레드 수
    HASH_LENGTH = 32       # 해시 길이
    SALT_LENGTH = 16       # 솔트 길이

    @staticmethod
    def get_recommended_params() -> dict:
        """OWASP 권장 파라미터"""
        return {
            'time_cost': Argon2Config.TIME_COST,
            'memory_cost': Argon2Config.MEMORY_COST,
            'parallelism': Argon2Config.PARALLELISM,
            'hash_len': Argon2Config.HASH_LENGTH,
            'salt_len': Argon2Config.SALT_LENGTH
        }


class PasswordHasher:
    """안전한 패스워드 해싱 (Argon2id)"""

    def __init__(self, time_cost: int = 2, memory_cost: int = 65536,
                 parallelism: int = 4, hash_len: int = 32,
                 salt_len: int = 16):
        """
        Args:
            time_cost: 반복 패스 수
            memory_cost: 메모리 비용 (KB)
            parallelism: 병렬 스레드 수
            hash_len: 해시 출력 길이
            salt_len: 솔트 길이
        """
        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism
        self.hash_len = hash_len
        self.salt_len = salt_len

    def hash(self, password: str) -> str:
        """
        패스워드 해싱

        Args:
            password: 패스워드

        Returns:
            해시 문자열 (Argon2id 포맷)
        """
        # 실제 사용: import argon2; argon2.PasswordHasher().hash(password)
        # 여기서는 PBKDF2로 시뮬레이션
        salt = secrets.token_bytes(self.salt_len)

        # 메모리 비용 시뮬레이션 (실제로는 Argon2 사용)
        # PBKDF2는 메모리 비용이 없으므로 반복으로 보정
        adjusted_iterations = self.time_cost * 300000

        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            adjusted_iterations,
            self.hash_len
        )

        # Argon2id 형식으로 저장 (시뮬레이션)
        salt_b64 = base64.b64encode(salt).decode('ascii').rstrip('=')
        hash_b64 = base64.b64encode(key).decode('ascii').rstrip('=')

        return (f"$argon2id$v=19$t={self.time_cost},"
                f"m={self.memory_cost},p={self.parallelism}$"
                f"{salt_b64}${hash_b64}")

    def verify(self, password: str, hash_string: str) -> bool:
        """
        패스워드 검증

        Args:
            password: 검증할 패스워드
            hash_string: 저장된 해시

        Returns:
            검증 성공 여부
        """
        # 파라미터 파싱
        parts = hash_string.split('$')
        if len(parts) < 6:
            return False

        params = parts[3].split(',')
        time_cost = int(params[0][2:])
        memory_cost = int(params[1][2:])
        parallelism = int(params[2][2:])

        salt_b64 = parts[4] + '=='  # 패딩 복원
        stored_hash_b64 = parts[5] + '=='

        try:
            salt = base64.b64decode(salt_b64)
            stored_hash = base64.b64decode(stored_hash_b64)
        except:
            return False

        # 재계산
        adjusted_iterations = time_cost * 300000
        computed_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            adjusted_iterations,
            len(stored_hash)
        )

        # Constant-time 비교
        import hmac
        return hmac.compare_digest(computed_hash, stored_hash)


class KeyDerivation:
    """암호화 키 유도"""

    @staticmethod
    def derive_from_password(password: str, salt: bytes,
                             key_length: int = 32) -> bytes:
        """
        패스워드에서 암호화 키 유도

        Args:
            password: 패스워드
            salt: 솔트
            key_length: 키 길이 (32 = AES-256)

        Returns:
            암호화 키
        """
        return PBKDF2.derive_key(password, salt, 600000, key_length)

    @staticmethod
    def derive_multiple_keys(master_key: bytes, info: str,
                             lengths: list) -> list:
        """
        마스터 키에서 여러 키 유도 (HKDF)

        Args:
            master_key: 마스터 키
            info: 컨텍스트 정보
            lengths: 각 키 길이 리스트

        Returns:
            유도된 키 리스트
        """
        import hmac

        # HKDF-Extract (Salt 없이)
        prk = master_key

        # HKDF-Expand
        keys = []
        okm = b''
        counter = 1
        total_length = sum(lengths)

        while len(okm) < total_length:
            t = okm[-32:] if okm else b''
            okm += hmac.new(prk, t + info.encode() + bytes([counter]),
                           hashlib.sha256).digest()
            counter += 1

        # 키 분할
        offset = 0
        for length in lengths:
            keys.append(okm[offset:offset+length])
            offset += length

        return keys


# 사용 예시
if __name__ == "__main__":
    print("=== PBKDF2 예시 ===")
    salt = PBKDF2.generate_salt()
    password = "MySecurePassword123!"

    key = PBKDF2.derive_key(password, salt)
    print(f"솔트: {salt.hex()}")
    print(f"유도된 키: {key.hex()}")

    print("\n=== 패스워드 해싱 예시 ===")
    hasher = PasswordHasher()
    password = "UserPassword456!"

    hashed = hasher.hash(password)
    print(f"원본: {password}")
    print(f"해시: {hashed}")

    is_valid = hasher.verify(password, hashed)
    print(f"검증: {'성공' if is_valid else '실패'}")

    is_valid_wrong = hasher.verify("WrongPassword", hashed)
    print(f"잘못된 패스워드: {'성공' if is_valid_wrong else '실패'}")

    print("\n=== 키 유도 예시 ===")
    master = secrets.token_bytes(32)
    keys = KeyDerivation.derive_multiple_keys(
        master, "encryption_keys", [32, 32, 16]
    )
    print(f"암호화 키: {keys[0].hex()[:32]}...")
    print(f"MAC 키: {keys[1].hex()[:32]}...")
    print(f"IV: {keys[2].hex()}")
