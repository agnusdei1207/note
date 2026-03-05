+++
title = "DES / 3DES (Data Encryption Standard)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# DES / 3DES (Data Encryption Standard)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DES는 56비트 키를 사용하는 대칭키 블록 암호(64비트 블록)로, 1977년 NIST 표준으로 채택되었으나 1998년 완전 브루트포스 공격 가능으로 더 이상 안전하지 않습니다.
> 2. **가치**: 3DES는 DES를 3회 적용하여 유효 키 길이를 112~168비트로 확장했으나, AES로의 마이그레이션이 강력 권장되며 PCI DSS 4.0에서는 2024년부터 신규 사용 금지입니다.
> 3. **융합**: Feistel 구조는 현대 암호 설계의 기초가 되었으며, DES의 역사적 분석은 암호 분석 기법(차분 공격, 선형 공격) 발전에 핵심적 역할을 했습니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**DES (Data Encryption Standard)**
- **정의**: 1977년 미국 NIST(NBS)가 표준으로 채택한 대칭키 블록 암호
- **구조**: Feistel 구조 기반, 16라운드
- **블록 크기**: 64비트
- **키 길이**: 64비트 (유효 56비트, 8비트 패리티)
- **설계자**: IBM (Horst Feistel 팀), NSA 수정

**3DES (Triple DES / TDEA)**
- **정의**: DES 알고리즘을 3회 연속 적용하여 보안 강화
- **키 옵션**:
  - Keying Option 1: 3개 독립 키 (168비트 유효)
  - Keying Option 2: K1=K3 (112비트 유효)
  - Keying Option 3: K1=K2=K3 (단일 DES와 동일, 사용 금지)
- **모드**: EDE (Encrypt-Decrypt-Encrypt)

#### 2. 비유를 통한 이해
DES는 **'짧은 열쇠의 금고'**에 비유할 수 있습니다:
- DES: 56개의 숫자로만 조합 가능한 자물쇠 (약 7×10^16 조합)
- 3DES: 같은 자물쇠를 3개 연결, 각각 다른 열쇠 필요
- 문제: 현대 컴퓨터는 56개 숫자를 몇 시간 내에 모두 시도 가능

```
DES 암호화 과정 비유:
[평문] → [자물쇠1(56비트)] → [암호문]

3DES 암호화 과정 비유:
[평문] → [자물쇠1] → [자물쇠2] → [자물쇠3] → [암호문]
```

#### 3. 등장 배경 및 발전 과정

| 연도 | 사건 | 의미 |
|:---|:---|:---|
| **1973** | NBS 공모 | 미국 정부 표준 암호 요청 |
| **1974** | IBM Lucifer 제출 | Feistel 구조 기반 128비트 |
| **1977** | DES FIPS 46 발행 | 56비트로 축소, NSA 개입 의혹 |
| **1990** | 차분 공격 발표 | Biham-Shamir, 이론적 공격 |
| **1993** | 선형 공격 발표 | Matsui, 실제보다 적은 연산 |
| **1998** | EFF Deep Crack | 56시간 브루트포스 성공 |
| **1999** | 3DES 표준화 | FIPS 46-3, DES 대체 |
| **2001** | AES 표준화 | FIPS 197, DES/3DES 대체 |
| **2017** | PCI DSS 3.2 | 3DES 사용 제한 권고 |
| **2024** | PCI DSS 4.0 | 3DES 신규 사용 금지 |

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. DES 알고리즘 구조

```text
                    [ DES 알고리즘 구조도 ]

[64비트 평문]
      │
      ▼
┌─────────────────────────────────────────┐
│          초기 순열 (Initial Permutation)   │
│         IP 테이블에 따른 비트 재배치         │
└────────────────────┬────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
      [L0:32비트]            [R0:32비트]
         │                       │
         │           ┌───────────┴───────────┐
         │           │    라운드 함수 f       │
         │           │  ┌─────────────────┐  │
         │           │  │  1. 확장(E)     │  │
         │           │  │  32→48비트 확장 │  │
         │           │  └────────┬────────┘  │
         │           │           ▼           │
         │           │  ┌─────────────────┐  │
         │           │  │  2. XOR with Ki │  │
         │           │  │  48비트 라운드키 │  │
         │           │  └────────┬────────┘  │
         │           │           ▼           │
         │           │  ┌─────────────────┐  │
         │           │  │  3. S-box 치환  │  │
         │           │  │  48→32비트      │  │
         │           │  │  8개 S-box 사용 │  │
         │           │  └────────┬────────┘  │
         │           │           ▼           │
         │           │  ┌─────────────────┐  │
         │           │  │  4. 순열(P)     │  │
         │           │  │  비트 재배치    │  │
         │           │  └────────┬────────┘  │
         │           └───────────┼───────────┘
         │                       │
         │◄──────────────────────┤ XOR
         │                       │
      [L1=R0]               [R1=L0⊕f(R0,K1)]
         │                       │
         └───────────┬───────────┘
                     │
              (16라운드 반복)
                     │
         ┌───────────┴───────────┐
      [L16]                  [R16]
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
              [R16 || L16]  (역순)
                     │
                     ▼
┌─────────────────────────────────────────┐
│        역 초기 순열 (Final Permutation)   │
│              IP⁻¹ 테이블                  │
└────────────────────┬────────────────────┘
                     │
                     ▼
               [64비트 암호문]
```

#### 2. DES 구성 요소 상세 분석

| 구성 요소 | 입력 | 출력 | 역할 | 특성 |
|:---|:---|:---|:---|:---|
| **초기 순열(IP)** | 64비트 | 64비트 | 비트 재배치 | 고정 테이블 |
| **확장 순열(E)** | 32비트 | 48비트 | 라운드 키와 XOR | 16비트 중복 |
| **S-box** | 48비트 | 32비트 | 비선형 치환 | 핵심 보안 요소 |
| **순열(P)** | 32비트 | 32비트 | 확산(Diffusion) | 비트 재배치 |
| **키 스케줄** | 56비트 | 16×48비트 | 라운드 키 생성 | PC1, PC2, Shift |
| **역 초기 순열(IP⁻¹)** | 64비트 | 64비트 | 최종 재배치 | IP의 역함수 |

#### 3. S-box 구조 (핵심 비선형성)

```python
# DES S-box 예시 (S-box 1)
SBOX_1 = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
]

def sbox_lookup(sbox: list, input_6bit: int) -> int:
    """
    S-box 조회
    입력: 6비트 (b1 b2 b3 b4 b5 b6)
    행: b1||b6 (2비트)
    열: b2||b3||b4||b5 (4비트)
    출력: 4비트
    """
    row = ((input_6bit >> 5) << 1) | (input_6bit & 1)  # b1, b6
    col = (input_6bit >> 1) & 0xF  # b2-b5
    return sbox[row][col]
```

#### 4. 3DES EDE 모드

```text
                    [ 3DES EDE (Encrypt-Decrypt-Encrypt) ]

[평문] ──────────────────────────────────────────────────► [암호문]
         │                 │                 │
         ▼                 ▼                 ▼
    ┌─────────┐       ┌─────────┐       ┌─────────┐
    │DES 암호화│       │DES 복호화│       │DES 암호화│
    │  키 K1  │       │  키 K2  │       │  키 K3  │
    └─────────┘       └─────────┘       └─────────┘

특징:
- K1=K2=K3이면 단일 DES와 동일 (하위 호환)
- K1≠K2≠K3이면 168비트 유효 키 (Keying Option 1)
- K1=K3≠K2이면 112비트 유효 키 (Keying Option 2)
- 암호화-복호화 순서는 하위호환성 때문

[암호문] ────────────────────────────────────────────────► [평문]
         │                 │                 │
         ▼                 ▼                 ▼
    ┌─────────┐       ┌─────────┐       ┌─────────┐
    │DES 복호화│       │DES 암호화│       │DES 복호화│
    │  키 K3  │       │  키 K2  │       │  키 K1  │
    └─────────┘       └─────────┘       └─────────┘
```

#### 5. 핵심 알고리즘 & 실무 코드: DES 구현

```python
from typing import Tuple
import struct

# DES 테이블들 (실제 구현에서는 전체 테이블 필요)
IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

IP_INV = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

# S-boxes (8개)
S_BOXES = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2-S8 생략 (실제 구현에서는 모두 필요)
]

PC1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

class DES:
    """DES 암호화 알고리즘 구현"""

    def __init__(self, key: bytes):
        """
        Args:
            key: 8바이트 (64비트) 키
        """
        if len(key) != 8:
            raise ValueError("DES key must be 8 bytes")
        self.subkeys = self._generate_subkeys(key)

    def _permute(self, block: int, table: list, in_size: int) -> int:
        """순열(Permutation) 적용"""
        result = 0
        for i, pos in enumerate(table):
            bit = (block >> (in_size - pos)) & 1
            result = (result << 1) | bit
        return result

    def _left_shift(self, value: int, shift: int, size: int) -> int:
        """왼쪽 순환 시프트"""
        return ((value << shift) | (value >> (size - shift))) & ((1 << size) - 1)

    def _generate_subkeys(self, key: bytes) -> list:
        """16개 라운드 서브키 생성"""
        # 64비트 정수로 변환
        key_int = int.from_bytes(key, 'big')

        # PC1 적용 (64→56비트)
        key_56 = self._permute(key_int, PC1, 64)

        # C, D 분리 (각 28비트)
        c = (key_56 >> 28) & 0xFFFFFFF
        d = key_56 & 0xFFFFFFF

        subkeys = []
        for shift in SHIFT_SCHEDULE:
            # 좌측 시프트
            c = self._left_shift(c, shift, 28)
            d = self._left_shift(d, shift, 28)

            # CD 결합 후 PC2 적용 (56→48비트)
            cd = (c << 28) | d
            subkey = self._permute(cd, PC2, 56)
            subkeys.append(subkey)

        return subkeys

    def _sbox_substitution(self, input_48: int) -> int:
        """S-box 치환 (48→32비트)"""
        output = 0
        for i in range(8):
            # 6비트 추출
            chunk = (input_48 >> (42 - i * 6)) & 0x3F

            # S-box 조회 (간소화, 실제로는 8개 S-box 필요)
            if i < len(S_BOXES):
                sbox = S_BOXES[i]
                row = ((chunk >> 5) << 1) | (chunk & 1)
                col = (chunk >> 1) & 0xF
                value = sbox[row][col]
            else:
                value = chunk & 0xF  # Placeholder

            output = (output << 4) | value

        return output

    def _f_function(self, r: int, subkey: int) -> int:
        """Feistel 라운드 함수"""
        # 1. 확장 순열 (32→48비트)
        expanded = self._permute(r, E, 32)

        # 2. 서브키와 XOR
        xored = expanded ^ subkey

        # 3. S-box 치환 (48→32비트)
        substituted = self._sbox_substitution(xored)

        # 4. P 순열 (32→32비트)
        return self._permute(substituted, P, 32)

    def _des_block(self, block: int, subkeys: list) -> int:
        """단일 블록 암호화/복호화"""
        # 초기 순열
        permuted = self._permute(block, IP, 64)

        # L, R 분리
        l = (permuted >> 32) & 0xFFFFFFFF
        r = permuted & 0xFFFFFFFF

        # 16 라운드
        for subkey in subkeys:
            new_r = l ^ self._f_function(r, subkey)
            l = r
            r = new_r

        # 최종 스왑 (R16 || L16)
        combined = (r << 32) | l

        # 역 초기 순열
        return self._permute(combined, IP_INV, 64)

    def encrypt(self, plaintext: bytes) -> bytes:
        """암호화 (ECB 모드, 단일 블록)"""
        if len(plaintext) != 8:
            raise ValueError("Plaintext must be 8 bytes")
        block = int.from_bytes(plaintext, 'big')
        ciphertext = self._des_block(block, self.subkeys)
        return ciphertext.to_bytes(8, 'big')

    def decrypt(self, ciphertext: bytes) -> bytes:
        """복호화 (역순 서브키 사용)"""
        if len(ciphertext) != 8:
            raise ValueError("Ciphertext must be 8 bytes")
        block = int.from_bytes(ciphertext, 'big')
        plaintext = self._des_block(block, self.subkeys[::-1])
        return plaintext.to_bytes(8, 'big')


class TripleDES:
    """3DES (EDE 모드) 구현"""

    def __init__(self, key1: bytes, key2: bytes, key3: bytes):
        """
        Args:
            key1, key2, key3: 각각 8바이트 키
        """
        self.des1 = DES(key1)
        self.des2 = DES(key2)
        self.des3 = DES(key3)

    def encrypt(self, plaintext: bytes) -> bytes:
        """EDE 암호화: Encrypt(K1) -> Decrypt(K2) -> Encrypt(K3)"""
        step1 = self.des1.encrypt(plaintext)
        step2 = self.des2.decrypt(step1)
        step3 = self.des3.encrypt(step2)
        return step3

    def decrypt(self, ciphertext: bytes) -> bytes:
        """EDE 복호화: Decrypt(K3) -> Encrypt(K2) -> Decrypt(K1)"""
        step1 = self.des3.decrypt(ciphertext)
        step2 = self.des2.encrypt(step1)
        step3 = self.des1.decrypt(step2)
        return step3

# 사용 예시
if __name__ == "__main__":
    # DES 예시
    key = bytes([0x13, 0x34, 0x57, 0x79, 0x9B, 0xBC, 0xDF, 0xF1])
    plaintext = bytes([0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF])

    des = DES(key)
    ciphertext = des.encrypt(plaintext)
    decrypted = des.decrypt(ciphertext)

    print(f"평문: {plaintext.hex()}")
    print(f"암호문: {ciphertext.hex()}")
    print(f"복호문: {decrypted.hex()}")
    print(f"일치: {plaintext == decrypted}")

    # 3DES 예시
    key1 = bytes([1, 2, 3, 4, 5, 6, 7, 8])
    key2 = bytes([8, 7, 6, 5, 4, 3, 2, 1])
    key3 = bytes([1, 1, 2, 2, 3, 3, 4, 4])

    triple_des = TripleDES(key1, key2, key3)
    cipher_3des = triple_des.encrypt(plaintext)
    plain_3des = triple_des.decrypt(cipher_3des)

    print(f"\n3DES 암호문: {cipher_3des.hex()}")
    print(f"3DES 복호문: {plain_3des.hex()}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. DES/AES/3DES 비교

| 특성 | DES | 3DES | AES |
|:---|:---|:---|:---|
| **키 길이** | 56비트 | 112/168비트 | 128/192/256비트 |
| **블록 크기** | 64비트 | 64비트 | 128비트 |
| **라운드 수** | 16 | 48 (16×3) | 10/12/14 |
| **구조** | Feistel | Feistel | SPN (Substitution-Permutation) |
| **보안 강도** | 깨짐 | 유효 ~112비트 | 128/192/256비트 |
| **속도** | 중간 | 느림 (3배) | 빠름 |
| **하드웨어** | 지원 | 지원 | AES-NI |
| **현재 상태** | 사용 금지 | 레거시만 | 권장 |

#### 2. DES 취약점 분석

| 공격 기법 | 연도 | 필요 연산 | 실용성 |
|:---|:---|:---|:---|
| **브루트포스** | 1998 | 2^55 | Deep Crack 56시간 |
| **차분 공격** | 1990 | 2^47 | 이론적 |
| **선형 공격** | 1993 | 2^43 | 이론적 |
| **관련 키 공격** | 1993 | 다양 | 특수 조건 |
| **사이드채널** | 현재 | 소량 | 실제 위험 |

#### 3. 과목 융합 관점 분석

- **컴퓨터구조**: AES-NI 명령어, DES 하드웨어 가속
- **운영체제**: 커널 암호화 API, /dev/random
- **네트워크**: TLS 레거시 cipher suite, IPsec
- **데이터베이스**: TDE, 컬럼 암호화
- **금융시스템**: PIN 암호화 (ISO 0), 카드 데이터 (PCI DSS)

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 레거시 금융시스템 3DES 마이그레이션**
- 상황: ATM, POS 단말기 3DES 사용, PCI DSS 4.0 준수
- 판단: 단계적 AES-256 마이그레이션
- 핵심 결정:
  - 신규: AES-256-GCM만 허용
  - 기존: 2025년까지 3DES 완전 폐지
  - 과도기: 암호화 게이트웨이로 투명 전환
- 효과: PCI DSS 4.0 준수, 성능 3배 향상

**시나리오 2: 레거시 프로토콜 호환성 유지**
- 상황: 구형 장비와 통신 필요, DES만 지원
- 판단: 프로토콜 게이트웨이로 격리
- 핵심 결정:
  - 내부: AES-256 사용
  - 외부: 게이트웨이에서 DES 변환
  - 네트워크: 격리된 세그먼트
- 효과: 보안 유지, 호환성 확보

**시나리오 3: 암호화 키 마이그레이션**
- 상황: 3DES 키를 AES 키로 전환
- 판단: 암호화 키 회전 절차 수립
- 핵심 결정:
  - 이중 암호화 (3DES + AES 병행)
  - 데이터 마이그레이션 배치 처리
  - 키 관리 시스템(KMS) 도입
- 효과: 무중단 마이그레이션

#### 2. 도입 시 고려사항 (체크리스트)

**보안 체크리스트**
- [ ] DES/3DES 사용 여부 전수 조사
- [ ] PCI DSS 요구사항 확인
- [ ] AES 마이그레이션 계획 수립
- [ ] 레거시 장비 교체 일정

**기술 체크리스트**
- [ ] AES-NI 지원 하드웨어 확인
- [ ] TLS 1.3 호환성 확인
- [ ] 암호화 라이브러리 업데이트
- [ ] 성능 벤치마크

#### 3. 안티패턴 (Anti-patterns)

| 안티패턴 | 문제점 | 올바른 접근 |
|:---|:---|:---|
| **신규에 DES/3DES 사용** | 보안 미달, 규정 위반 | AES-256 사용 |
| **3DES 영구 사용** | 성능 저하, 향후 폐지 | AES로 마이그레이션 |
| **ECB 모드 사용** | 패턴 노출 | CBC/CTR/GCM 사용 |
| **키 재사용** | 취약점 증가 | 정기적 키 교체 |

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | DES → AES 전환 시 |
|:---|:---|
| 보안 강도 | 56비트 → 256비트 (2^200배 향상) |
| 처리 속도 | 3배 향상 (AES-NI 시 10배) |
| 규정 준수 | PCI DSS 4.0 준수 |
| 레거시 부채 | 기술 부채 해소 |

#### 2. 미래 전망 및 진화 방향

- **2025년**: 3DES 완전 폐지 예정 (PCI DSS)
- **AES 전환**: 모든 신규 시스템 필수
- **양자 내성**: AES-256은 양자 컴퓨터에도 안전
- **경량 암호**: IoT용 PRESENT, SIMON 등

#### 3. 참고 표준/가이드

- **FIPS 46-3**: Data Encryption Standard (DES)
- **FIPS 197**: Advanced Encryption Standard (AES)
- **SP 800-67 Rev. 2**: Recommendation for TDEA
- **PCI DSS v4.0**: Requirement 2.3.1 (3DES 금지)

---

### 관련 개념 맵 (Knowledge Graph)

- [AES](@/studynotes/09_security/02_crypto/aes.md) : DES 대체 표준
- [대칭키 암호](@/studynotes/09_security/02_crypto/symmetric_encryption.md) : 암호화 기본 개념
- [GCM](@/studynotes/09_security/02_crypto/gcm.md) : 인증 암호화 모드
- [블록 암호 모드](@/studynotes/09_security/02_crypto/block_cipher_modes.md) : 운영 모드
- [키 관리](@/studynotes/09_security/02_crypto/key_management.md) : 키 수명주기

---

### 어린이를 위한 3줄 비유 설명

1. **짧은 비밀번호**: DES는 56글자 비밀번호예요. 요즘 컴퓨터는 이 정도면 며칠 만에 알아낼 수 있어요.
2. **세 번 잠그기**: 3DES는 자물쇠를 3개 달아요. 3개의 다른 열쇠가 필요하죠. 훨씬 튼튼해요.
3. **새 자물쇠로 바꾸기**: 하지만 이제 더 튼튼한 AES라는 새 자물쇠가 있어요. DES와 3DES는 옛날 이야기가 되어가요.
