+++
title = "블록의 구조 (Block Structure)"
description = "블록체인을 구성하는 개별 블록의 내부 구조로서, 블록 헤더와 바디로 구성되며 거래 무결성과 체인 연결성을 보장하는 핵심 아키텍처 분석"
date = 2024-05-15
[taxonomies]
tags = ["Block Structure", "Blockchain", "Block Header", "Merkle Root", "ICT Convergence"]
+++

# 블록의 구조 (Block Structure)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 블록은 블록체인의 기본 데이터 단위로, **블록 헤더(Header)**와 **블록 바디(Body)**로 구성되며, 헤더는 버전, 이전 블록 해시, 머클 루트, 타임스탬프, 난이도, 논스를 포함하고, 바디는 트랜잭션 리스트를 포함하여 거래 데이터의 무결성과 체인의 연속성을 동시에 보장합니다.
> 2. **가치**: 블록 구조는 SHA-256과 같은 암호학적 해시 함수를 통해 이전 블록과 연결되어 '체인'을 형성하며, 머클 트리 구조를 통해 개별 트랜잭션의 위변조를 감지하고, 라이트 노드가 전체 블록을 다운로드하지 않고도 거래 유효성을 검증할 수 있게 합니다.
> 3. **융합**: 블록 구조는 비트코인의 1MB 고정 크기에서 이더리움의 가스 리미트 기반 동적 크기로 진화했으며, 세그윗(SegWit), 머클화된 추상 구문 트리(MAST) 등의 개선을 통해 확장성과 프라이버시를 강화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
블록(Block)은 블록체인 네트워크에서 일정 기간(비트코인의 경우 약 10분) 동안 발생한 트랜잭션들을 모아 하나의 단위로 묶은 데이터 구조입니다. 각 블록은 **블록 헤더(Block Header)**와 **블록 바디(Block Body)** 두 부분으로 구성됩니다.

- **블록 헤더**: 블록의 메타데이터를 포함하며, 블록체인의 '체인'을 형성하는 핵심 요소입니다. 이전 블록 해시, 머클 루트, 타임스탬프, 난이도 타겟, 논스(Nonce) 등을 포함하며, 채굴 시 해시 퍼즐의 입력값으로 사용됩니다.
- **블록 바디**: 실제 트랜잭션들의 리스트를 포함합니다. 코인베이스 트랜잭션(채굴 보상)이 첫 번째로 위치하며, 그 뒤로 일반 트랜잭션들이 나열됩니다.

### 2. 구체적인 일상생활 비유
블록을 **하나의 '페이지'가 있는 장부**라고 비유할 수 있습니다.

- **블록 헤더**는 페이지 상단의 **헤더 정보**입니다. "이 페이지 번호", "이전 페이지 번호", "이 페이지에 있는 모든 거래의 요약(머클 루트)", "작성 날짜", "승인 도장(논스)"이 적혀 있습니다.
- **블록 바디**는 페이지 본문에 적힌 **거래 내역 리스트**입니다. "홍길동이 철수에게 100원 송금", "영희가 민수에게 50원 송금" 등의 구체적인 거래들이 나열됩니다.

각 페이지(블록)는 이전 페이지의 "요약 해시"를 포함하고 있어, 어떤 페이지가 찢어지거나 수정되면 다음 모든 페이지의 해시가 맞지 않게 되어 위조가 즉시 감지됩니다.

### 3. 등장 배경 및 발전 과정
1. **일괄 처리와 효율성**:
   - 개별 트랜잭션을 실시간으로 처리하는 대신, 일정 시간 동안 발생한 트랜잭션을 모아 블록으로 묶어 일괄 처리하면 네트워크 효율성이 향상됩니다. 채굴자는 블록 단위로 해시 퍼즐을 풀어 검증 비용을 절감합니다.

2. **해시 체인 구조의 구현**:
   - 각 블록 헤더에 '이전 블록 해시'를 포함함으로써, 블록들이 마치 체인처럼 연결됩니다. 이는 1991년 해리버트(Haber)와 스토르네타(Stornetta)가 제안한 "안전한 타임스탬프 서비스" 아이디어에서 유래했습니다.

3. **블록 크기 논쟁과 개선**:
   - 비트코인의 초기 블록 크기는 1MB로 제한되어 있었으나, 트래픽 증가로 확장성 논쟁이 발생했습니다. 2017년 세그윗(SegWit) 도입으로 실질적 용량이 증가했고, 비트코인 캐시는 8MB(현재 32MB)로 확장했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 필드명 (Field) | 크기 (비트코인) | 상세 역할 | 내부 동작 메커니즘 | 비고 |
|:---|:---|:---|:---|:---|
| **Version** | 4바이트 | 블록 구조 버전 | 소프트웨어 업그레이드 시 변경 | 현재 버전 2 |
| **Previous Block Hash** | 32바이트 | 이전 블록 헤더의 SHA-256 해시 | 체인 연결의 핵심, 위변조 방지 | 제네시스 블록은 0 |
| **Merkle Root** | 32바이트 | 블록 내 모든 트랜잭션의 머클 트리 루트 해시 | 트랜잭션 추가/변경 시 루트 해시 변화 | 무결성 검증 |
| **Timestamp** | 4바이트 | 블록 생성 시각 (Unix Epoch) | 채굴자가 기록, 평균 10분 간격 검증에 사용 | 난이도 조절 기준 |
| **Difficulty Target (Bits)** | 4바이트 | 해시 퍼즐의 난이도 타겟값 | 2016블록마다 전체 해시파워에 따라 조절 | 작은 값일수록 어려움 |
| **Nonce** | 4바이트 | 채굴자가 찾아야 하는 해시 퍼즐 해답 | 0부터 증가하며 해시 < 타겟 조건 충족 시 발견 | 브루트포스 탐색 |
| **Transaction Count** | 가변 | 블록 내 트랜잭션 개수 | VarInt 인코딩으로 표현 | |
| **Transactions** | 가변 | 실제 트랜잭션 리스트 | 코인베이스 트랜잭션이 첫 번째 | |

### 2. 정교한 구조 다이어그램: 블록 구조 상세

```text
================================================================================
                    [ Bitcoin Block Structure (80-byte Header + Body) ]
================================================================================

+-----------------------------------------------------------------------+
|                         Block Header (80 Bytes)                        |
|-----------------------------------------------------------------------|
| +----------------------------------+--------------------------------+ |
| | Version (4 bytes)                | 0x20000000                     | |
| +----------------------------------+--------------------------------+ |
| | Previous Block Hash (32 bytes)   | 0000000000000000000...         | |
| |                                  | (이전 블록 헤더의 SHA-256²)     | |
| +----------------------------------+--------------------------------+ |
| | Merkle Root (32 bytes)           | 4a5e1e4baab89f3a3251...       | |
| |                                  | (모든 트랜잭션의 머클 트리 루트)| |
| +----------------------------------+--------------------------------+ |
| | Timestamp (4 bytes)              | 1231006505 (2009-01-03)        | |
| +----------------------------------+--------------------------------+ |
| | Difficulty Bits (4 bytes)        | 0x1d00ffff (난이도 1)          | |
| +----------------------------------+--------------------------------+ |
| | Nonce (4 bytes)                  | 2083236893 (채굴로 발견)       | |
| +----------------------------------+--------------------------------+ |
|                                                                        |
| => 위 80바이트를 입력으로 SHA-256(SHA-256(Header)) 해시 계산          |
| => 결과값이 Difficulty Target 미만이면 유효한 블록                     |
+-----------------------------------------------------------------------+
                                    |
                                    | (Merkle Root 계산의 입력)
                                    v
+-----------------------------------------------------------------------+
|                         Block Body (Variable Size)                    |
|-----------------------------------------------------------------------|
| +-------------------------------------------------------------------+ |
| | Transaction Count (VarInt)                                        | |
| +-------------------------------------------------------------------+ |
| | Transaction 1: Coinbase Transaction (채굴 보용 지급)              | |
| |   - Version | Input(무입력) | Output(50BTC→채굴자) | Locktime   | |
| +-------------------------------------------------------------------+ |
| | Transaction 2: 일반 거래                                          | |
| |   - Version | Inputs | Outputs | Witnesses(선택) | Locktime     | |
| +-------------------------------------------------------------------+ |
| | Transaction 3: 일반 거래                                          | |
| +-------------------------------------------------------------------+ |
| | ...                                                               | |
| +-------------------------------------------------------------------+ |
| | Transaction N                                                     | |
| +-------------------------------------------------------------------+ |
+-----------------------------------------------------------------------+

=> 블록 크기 제한: 비트코인 1MB (SegWit 적용 시 실질적 4MB)
=> 이더리움: 가스 리미트(30M 가스) 기반 동적 크기
```

### 3. 머클 트리와 트랜잭션 무결성 검증
머클 트리(Merkle Tree)는 블록 내 모든 트랜잭션의 무결성을 효율적으로 검증하기 위한 이진 트리 구조입니다.

```text
                    Merkle Root (블록 헤더에 저장)
                           /              \
                  Hash(AB)                  Hash(CD)
                   /    \                    /    \
              Hash(A)  Hash(B)          Hash(C)  Hash(D)
                 |        |                |        |
              Tx A     Tx B             Tx C     Tx D

=> 트랜잭션 D가 변경되면 Hash(D) → Hash(CD) → Merkle Root까지 모두 변경됨
=> 라이트 노드는 Merkle Root + Merkle Path만으로 Tx D의 포함 여부 검증 가능
```

### 4. 핵심 알고리즘 및 실무 코드 예시

```python
import hashlib
import struct
from typing import List

class BlockHeader:
    """비트코인 블록 헤더 구조"""
    def __init__(self, version, prev_hash, merkle_root, timestamp, bits, nonce):
        self.version = version          # 4 bytes
        self.prev_hash = prev_hash      # 32 bytes
        self.merkle_root = merkle_root  # 32 bytes
        self.timestamp = timestamp      # 4 bytes
        self.bits = bits                # 4 bytes (difficulty target)
        self.nonce = nonce              # 4 bytes

    def serialize(self) -> bytes:
        """블록 헤더를 바이트로 직렬화"""
        return (
            struct.pack('<I', self.version) +
            bytes.fromhex(self.prev_hash)[::-1] +  # Little Endian
            bytes.fromhex(self.merkle_root)[::-1] +
            struct.pack('<I', self.timestamp) +
            bytes.fromhex(self.bits)[::-1] +
            struct.pack('<I', self.nonce)
        )

    def calculate_hash(self) -> str:
        """블록 해시 계산 (SHA-256 두 번 적용)"""
        header_bytes = self.serialize()
        hash1 = hashlib.sha256(header_bytes).digest()
        hash2 = hashlib.sha256(hash1).digest()
        return hash2[::-1].hex()  # Little Endian으로 표시

    def verify_pow(self) -> bool:
        """작업 증명 검증: 블록 해시가 난이도 타겟 미만인지 확인"""
        block_hash = int(self.calculate_hash(), 16)
        target = self.bits_to_target(self.bits)
        return block_hash < target

    @staticmethod
    def bits_to_target(bits_hex: str) -> int:
        """Bits 필드를 타겟 정수로 변환"""
        bits_bytes = bytes.fromhex(bits_hex)
        exponent = bits_bytes[0]
        coefficient = struct.unpack('>I', b'\x00' + bits_bytes[1:4])[0]
        return coefficient * (256 ** (exponent - 3))


def calculate_merkle_root(transactions: List[str]) -> str:
    """
    트랜잭션 해시 리스트로부터 머클 루트 계산
    """
    if len(transactions) == 0:
        return '0' * 64
    if len(transactions) == 1:
        return transactions[0]

    # 트랜잭션 개수가 홀수면 마지막 트랜잭션을 복제
    if len(transactions) % 2 == 1:
        transactions.append(transactions[-1])

    # 두 개씩 묶어서 해시 계산
    next_level = []
    for i in range(0, len(transactions), 2):
        combined = bytes.fromhex(transactions[i]) + bytes.fromhex(transactions[i + 1])
        hash_result = hashlib.sha256(hashlib.sha256(combined).digest()).digest()
        next_level.append(hash_result.hex())

    # 재귀적으로 루트까지 계산
    return calculate_merkle_root(next_level)


# 블록 구조 실습
if __name__ == "__main__":
    # 예시: 간소화된 블록 헤더 생성
    header = BlockHeader(
        version=0x20000000,
        prev_hash="0000000000000000000000000000000000000000000000000000000000000000",
        merkle_root="4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab212a385c1e0555ad",
        timestamp=1231006505,
        bits="1d00ffff",
        nonce=2083236893
    )

    print("=== Block Header Analysis ===")
    print(f"Block Hash: {header.calculate_hash()}")
    print(f"PoW Valid: {header.verify_pow()}")

    # 머클 루트 계산 예시
    txs = [
        "3ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a",
        "dummy_tx_hash_1",
        "dummy_tx_hash_2",
        "dummy_tx_hash_3"
    ]
    print(f"\nMerkle Root: {calculate_merkle_root(txs)}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 비트코인 vs 이더리움 블록 구조

| 구성 요소 | 비트코인 (UTXO 모델) | 이더리움 (계정 모델) |
|:---|:---|:---|
| **블록 크기 제한** | 1MB (SegWit 적용 시 가중치 4MWU) | 가스 리미트 (약 30M 가스) 동적 |
| **블록 생성 주기** | 약 10분 | 약 12~15초 |
| **블록 헤더 필드** | 6개 (Version, PrevHash, MerkleRoot, Time, Bits, Nonce) | 15개 (ParentHash, StateRoot, TxRoot, ReceiptRoot, GasLimit, 등) |
| **상태 저장** | 없음 (UTXO만 추적) | 상태 트리(State Trie)의 루트 해시 포함 |
| **스마트 컨트랙트** | 미지원 (OP_RETURN 데이터만) | EVM 바이트코드 실행 |
| **확장 기술** | SegWit, Lightning Network | 샤딩, 롤업(L2) |

### 2. 과목 융합 관점 분석
- **블록 구조 + 데이터베이스**: 블록체인은 '추가 전용(Append-Only) 데이터베이스'로 볼 수 있습니다. 각 블록은 불변성을 보장하며, LevelDB, RocksDB 같은 키-값 스토어가 블록 인덱싱에 사용됩니다.
- **블록 구조 + 네트워크**: 블록은 P2P 네트워크를 통해 전파됩니다. 블록 헤더만 먼저 전송하고(Compact Block), 필요 시 트랜잭션을 요청하는 방식으로 대역폭을 절약합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략
- **[상황 A] 블록 탐색기(Block Explorer) 개발**
  - **요구사항**: 사용자가 블록 번호로 상세 정보를 조회할 수 있는 웹 서비스 구축.
  - **기술사 판단**: 블록 헤더는 인덱싱하여 빠르게 조회하고, 트랜잭션은 별도 테이블에 정규화하여 저장. 머클 루트를 이용해 특정 트랜잭션의 블록 포함 여부를 API로 제공.

- **[상황 B] 프라이빗 블록체인 블록 크기 설계**
  - **요구사항**: 기업 내부 거래 처리량에 맞는 블록 크기와 생성 주기 결정.
  - **기술사 판단**: 평균 트랜잭션 크기(약 250바이트)와 목표 TPS를 기반으로 블록 크기 계산. 예: 1000 TPS × 10초 × 250B = 2.5MB 블록 크기 필요.

### 2. 도입 시 고려사항
- **블록 크기와 보안의 트레이드오프**: 블록 크기를 키우면 처리량(throughput)은 증가하지만, 전파 지연으로 인해 '오브(orphan) 블록' 비율이 증가하고 채굴 중앙화 위험이 있습니다.
- **세그윗(SegWit) 호환성**: SegWit이 적용된 블록은 트랜잭션 데이터 구조가 다르므로, 레거시 노드와 호환성 검증이 필요합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 블록 구조의 기여 | 효과 |
|:---|:---|:---|
| **무결성** | 머클 루트 | 트랜잭션 위변조 감지 |
| **연결성** | 이전 블록 해시 | 체인 구조 형성, 이력 추적 |
| **검증 효율** | 블록 헤더 분리 | SPV(간편 결제 검증) 가능 |
| **확장성** | 동적 블록 크기 | 네트워크 상태에 따른 유연한 처리 |

### 2. 미래 전망
- **블록 네임스페이스(MAST)**: 머클화된 추상 구문 트리를 통해 복잡한 스마트 컨트랙트의 실행 경로만 공개하여 프라이버시와 효율성을 동시에 확보합니다.
- **블록 프루닝(Pruning)**: 전체 노드의 저장소 부담을 줄이 위해, 검증된 오래된 블록의 트랜잭션 데이터를 삭제하고 헤더만 유지하는 기술이 보편화됩니다.

### 3. 참고 표준
- **BIP 141 (SegWit)**: 세그윗 도입으로 블록 구조 변경.
- **Ethereum Yellow Paper**: 이더리움 블록 구조의 공식 사양.

---

## 관련 개념 맵 (Knowledge Graph)
- **[머클 트리 (Merkle Tree)](@/studynotes/06_ict_convergence/02_blockchain/merkle_tree.md)**: 블록 내 트랜잭션 무결성 검증 구조.
- **[작업 증명 (Proof of Work)](@/studynotes/06_ict_convergence/02_blockchain/pow.md)**: 블록 헤더를 이용한 합의 알고리즘.
- **[트랜잭션 (Transaction)](@/studynotes/06_ict_convergence/02_blockchain/transaction.md)**: 블록 바디에 포함되는 거래 데이터.
- **[세그윗 (SegWit)](@/studynotes/06_ict_convergence/02_blockchain/segwit.md)**: 블록 구조를 개선한 확장성 기술.
- **[제네시스 블록 (Genesis Block)](@/studynotes/06_ict_convergence/02_blockchain/genesis_block.md)**: 첫 번째 블록의 특수 구조.

---

## 어린이를 위한 3줄 비유 설명
1. 블록은 **한 페이지짜리 거래 장부**예요! 윗부분에는 "이 페이지 번호, 이전 페이지 번호, 모든 거래의 암호 요약"이 적혀 있고, 아랫부분에는 실제 거래 내역들이 쭉 나열되어 있어요.
2. 윗부분(헤더)에 있는 "이전 페이지 번호" 덕분에, 누군가 몰래 페이지를 찢거나 수정하면 바로 다음 페이지들과 번호가 안 맞게 돼서 **위조가 들켜버려요**!
3. 아랫부분에 있는 거래들은 모두 암호 요약(머클 루트)으로 압축되어 윗부분에 저장돼요. 그래서 거래 하나만 살짝 바꿔도 암호 요약이 완전히 달라져서 **못 믿는 사람도 위조를 잡아낼 수 있어요**!
