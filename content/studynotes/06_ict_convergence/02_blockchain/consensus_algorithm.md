+++
title = "합의 알고리즘 (Consensus Algorithm)"
description = "분산 시스템의 상태 일치 달성 메커니즘: PoW, PoS, PBFT 등 합의 알고리즘의 원리, 장단점 및 실무 적용 전략을 다루는 심층 기술 백서"
date = 2024-05-16
[taxonomies]
tags = ["Consensus Algorithm", "PoW", "PoS", "PBFT", "Byzantine Fault", "Distributed System"]
+++

# 합의 알고리즘 (Consensus Algorithm)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산된 노드들이 통신 지연, 장애, 악의적 공격이 존재하는 불완전한 네트워크 환경에서도, 시스템의 상태(State)에 대한 단일한 합의를 도출하여 데이터의 일관성(Consistency)과 무결성(Integrity)을 보장하는 분산 컴퓨팅의 근본 메커니즘입니다.
> 2. **가치**: 비잔틴 장애 허용(BFT)을 통해 악의적 노드가 1/3 미만일 때 시스템의 정상 작동을 보장하며, 경제적 인센티브 구조(PoW, PoS)를 통해 탈중앙화된 신뢰(Trustless)를 창출하여 블록체인 네트워크의 보안성을 확보합니다.
> 3. **융합**: 암호학(해시 함수, 전자 서명), 게임 이론(내쉬 균형), 분산 시스템(FLP 불가능성 증명)이 결합되어, 퍼블릭 블록체인, 프라이빗 블록체인, 분산 데이터베이스 등 다양한 분산 시스템의 핵심 알고리즘으로 활용됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
합의 알고리즘(Consensus Algorithm)은 분산 시스템을 구성하는 여러 노드들이 특정 데이터 값이나 상태에 대해 **동의(Agreement)**하는 절차와 규칙을 정의한 프로토콜입니다. 블록체인에서는 누가 다음 블록을 생성할 권한(Leader Election)을 부여받을지, 그리고 생성된 블록이 올바른지 검증(Validation)하고 거부할지를 결정하는 핵심 거버넌스 메커니즘입니다. 대표적인 합의 알고리즘으로는 작업 증명(PoW), 지분 증명(PoS), 위임 지분 증명(DPoS), 실용적 비잔틴 장애 허용(PBFT), 권위 증명(PoA) 등이 있습니다.

### 💡 2. 구체적인 일상생활 비유
합의 알고리즘은 '마을 회의의 투표 규칙'과 같습니다. 마을 사람들(노드)이 각자 다른 집에 흩어져 있고, 어떤 사람은 거짓말쟁이(악의적 노드)이며, 전화선(네트워크)이 불안정해서 메시지가 늦게 도착하거나 유실되기도 합니다. 이런 상황에서 "내년 마을 축제 날짜를 언제로 정할까?"라는 질문에 대해, 모든 정직한 사람들이 동일한 결론에 도달하도록 보장하는 규칙이 합의 알고리즘입니다. PoW는 "가장 오래 달리기 시합을 한 사람의 제안을 따른다", PoS는 "마을에 가장 많은 기여를 한 사람의 제안을 따른다", PBFT는 "과반수 이상이 동의하면 확정한다"는 식의 규칙입니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (비잔틴 장군 문제)**:
   1982년 레슬리 램포트(Leslie Lamport) 등이 제시한 **비잔틴 장군 문제(Byzantine Generals Problem)**는, 분산된 장군들이 배신자(악의적 노드)의 존재와 신뢰할 수 없는 통신망 환경에서도 어떻게 합의에 도달할 것인가라는 문제입니다. 전통적인 분산 시스템(Paxos, Raft)은 장애 노드(Crash Fault)는 허용하지만, 악의적 행위(Byzantine Fault)는 다루지 못했습니다.

2. **혁신적 패러다임 변화의 시작**:
   2008년 사토시 나카모토는 **작업 증명(PoW, Proof of Work)**을 통해 비잔틴 장애 허용(BFT)을 경제적 관점에서 해결했습니다. "거짓말을 하는 것보다 정직하게 행동하는 것이 더 이익"이 되도록 설계된 게임 이론적 인센티브 구조가 핵심입니다. 2012년 Peercoin은 **지분 증명(PoS)**을 제안하여 전력 낭비 문제를 해결하고자 했습니다. 1999년 Castro와 Liskov는 **PBFT(Practical BFT)**를 발표하여 허가형(Permissioned) 환경에서의 효율적인 합의를 가능하게 했습니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   비트코인과 이더리움의 PoW는 막대한 전력 소모(연간 핀란드 전력 소비량 상당)와 낮은 TPS(초당 7~15 트랜잭션)로 인해 확장성 문제에 직면했습니다. 이더리움 2.0(The Merge)은 PoS로 전환하여 에너지 효율을 99.95% 개선했습니다. 기업용 프라이빗 블록체인(Hyperledger Fabric)은 PBFT 기반으로 높은 TPS(수만)와 즉각적 완결성(Finality)을 요구합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Module) | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Leader Election** | 블록 생성 권한자 선정 | 해시 퍼즐 풀이(PoW), 스테이킹 양/기간(PoS), 투표(DPoS) | Mining, Staking, Voting | 반장 선출 |
| **Block Validation** | 생성된 블록의 유효성 검증 | 서명 검증, 트랜잭션 유효성, 머클 루트 계산 | ECDSA, Merkle Tree | 투표 용지 검사 |
| **Finality** | 블록의 최종 확정 상태 보장 | 확률적 완결성(6 confirmations), 즉각적 완결성(BFT) | Longest Chain Rule, BFT Commit | 판결 확정 |
| **Fault Tolerance** | 악의적/장애 노드 내성 | 비잔틴 장애(1/3 미만), 크래시 장애(1/2 미만) | BFT, CFT | 거짓말쟁이 방어 |
| **Slashing** | 악의적 행위에 대한 처벌 | 스테이킹 몰수, 네트워크 추방 | PoS Penalty, PoW orphan | 벌금/추방 |

### 2. 정교한 구조 다이어그램: 합의 알고리즘 분류 체계

```text
=====================================================================================================
                          [ Consensus Algorithm Taxonomy ]
=====================================================================================================

                                    [ Consensus Algorithms ]
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    │                         │                         │
            [ Proof-Based ]            [ Voting-Based ]          [ Hybrid ]
                    │                         │                         │
         ┌──────────┼──────────┐      ┌───────┴───────┐         ┌──────┴──────┐
         │          │          │      │               │         │             │
      [PoW]      [PoS]      [PoST]  [PBFT]         [Raft]   [PoA]        [Tendermint]
         │          │          │      │               │         │             │
    Bitcoin    Ethereum 2.0  Chia   Hyperledger    etcd     VeChain      Cosmos
    Ethereum*  Cardano      Filecoin Fabric        Consul   xDAI         Polkadot
                            (Space+Time)

=====================================================================================================

    [ PoW (Proof of Work) Flow ]                [ PBFT (3-Phase Voting) Flow ]

    +----------+                                  +----------+
    |  Miner 1 | ─────┐                          |  Client  | ── Request ──>|
    +----------+      │                          +----------+               │
                      │                                                     ▼
    +----------+      │     +------------+           +------------------------------------------+
    |  Miner 2 | ─────┼────>│ Longest    │           |              Primary (Leader)             |
    +----------+      │     │ Chain Wins │           |  1. Pre-prepare (Block Proposal)         |
                      │     +------------+           +------------------------------------------+
    +----------+      │            │                           │ Broadcast               │
    |  Miner 3 | ─────┘            │                           ▼                         ▼
    +----------+                   │              +------------------------+  +------------------------+
                                 │              | Replica 1              |  | Replica 2              |
                                 ▼              | 2. Prepare (Broadcast) |  | 2. Prepare (Broadcast) |
                          +-------------+       | 3. Commit (2f+1 ACK)   |  | 3. Commit (2f+1 ACK)   |
                          | Next Block  |       +------------------------+  +------------------------+
                          | Added to    |                  │                         │
                          | Blockchain  |                  └───────────┬─────────────┘
                          +-------------+                              │
                                                                      ▼
                                                          +--------------------------+
                                                          | Block Finalized          |
                                                          | (Immediate Finality)     |
                                                          +--------------------------+
```

### 3. 심층 동작 원리 (PoW vs PoS vs PBFT)

#### (1) 작업 증명 (PoW - Proof of Work)
```text
1. [트랜잭션 수집] 채굴자가 멤풀에서 트랜잭션을 수집하여 블록 구성
2. [머클 루트 계산] 트랜잭션들의 해시를 머클 트리로 구성하여 루트 해시 도출
3. [블록 헤더 구성] 버전 + 이전 블록 해시 + 머클 루트 + 타임스탬프 + 난이도 목표 + 논스(Nonce)
4. [해시 퍼즐 풀이] SHA-256(블록 헤더) < Target 난이도가 될 때까지 Nonce를 증가시키며 반복 연산
5. [브로드캐스트] 조건을 만족하는 Nonce를 찾으면 전 네트워크에 블록 전파
6. [검증 및 체인 연결] 다른 노드들이 블록을 검증하고, 자신의 체인에 연결
7. [보상] 채굴자는 블록 보상(코인) + 트랜잭션 수수료 획득

수학적 복잡도:
- 난이도 D일 때, 평균 D번의 해시 연산이 필요 (기댓값 E[Nonce] = D)
- 비트코인의 경우, 전 세계 해시 파워 약 400 EH/s, 평균 10분당 1개 블록 생성
```

#### (2) 지분 증명 (PoS - Proof of Stake)
```text
이더리움 2.0 (Gasper: Casper FFG + LMD-GHOST) 기준:

1. [스테이킹] 검증자(Validator)가 32 ETH를 스테이킹하여 활성 검증자 풀에 참여
2. [에포크/슬롯] 32슬롯 = 1에포크, 각 슬롯(12초)마다 1개 블록 생성
3. [프로포저 선정] 스테이킹 양에 비례한 확률로 블록 프로포저 무작위 선정
4. [어테스테이션] 128명의 커미티 검증자가 블록에 서명(Attestation)하여 투표
5. [파이널리티] 2연속 에포크에서 2/3 이상 스테이킹의 체크포인트 투표 시 파이널라이즈
6. [슬래싱] 이중 서명, 충돌하는 블록 생성 등 악의적 행위 시 스테이킹 몰수

수학적 보안:
- 경제적 보안 = 총 스테이킹 양 × 2/3 (공격 비용)
- 이더리움 2.0: 약 3,000만 ETH 스테이킹 → 약 600억 달러 규모의 공격 비용
```

#### (3) 실용적 비잔틴 장애 허용 (PBFT)
```text
노드 수 N = 3f + 1일 때, 최대 f개의 비잔틴(악의적) 노드를 허용

1. [Request] 클라이언트가 프라이머리(리더)에게 요청 전송
2. [Pre-prepare] 프라이머리가 요청에 시퀀스 번호를 할당하고 모든 복제본에게 브로드캐스트
3. [Prepare] 각 복제본이 검증 후 2f개의 Prepare 메시지를 수신하면 Prepare 상태로 전이
4. [Commit] 2f+1개의 Commit 메시지를 수신하면 로컬에 실행하고 클라이언트에게 응답
5. [Reply] f+1개의 동일한 응답을 수신한 클라이언트는 결과 확정

수학적 보장 (Safety & Liveness):
- Safety: 모든 정직한 노드는 동일한 순서로 동일한 트랜잭션을 실행
- Liveness: 최종적으로 모든 정직한 노드가 결정에 도달
- 메시지 복잡도: O(N²) - 노드 수 증가 시 통신량이 제곱으로 증가 (확장성 한계)
```

### 4. 핵심 알고리즘 및 실무 코드 예시

간소화된 PBFT 합의 시뮬레이션 Python 코드입니다.

```python
import hashlib
from typing import List, Dict, Set
from dataclasses import dataclass
from enum import Enum

class MessageType(Enum):
    PRE_PREPARE = "PRE_PREPARE"
    PREPARE = "PREPARE"
    COMMIT = "COMMIT"

@dataclass
class Message:
    msg_type: MessageType
    view: int
    sequence: int
    digest: str
    sender: int
    signature: str  # 실제로는 암호화 서명

class PBFTNode:
    """
    PBFT 합의 노드 시뮬레이션
    N = 3f + 1 개의 노드로 구성, 최대 f개의 비잔틴 노드 허용
    """

    def __init__(self, node_id: int, total_nodes: int, is_byzantine: bool = False):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.f = (total_nodes - 1) // 3  # 허용 가능한 비잔틴 노드 수
        self.is_byzantine = is_byzantine
        self.is_primary = False
        self.log: Dict[str, List[Message]] = {}  # 메시지 로그
        self.state: Dict[int, str] = {}  # 시퀀스별 확정 상태

    def pre_prepare(self, view: int, sequence: int, request: str) -> Message:
        """프라이머리만 실행: 요청에 시퀀스 번호 할당 및 브로드캐스트"""
        digest = hashlib.sha256(request.encode()).hexdigest()
        msg = Message(MessageType.PRE_PREPARE, view, sequence, digest, self.node_id, "")

        if self.is_byzantine:
            # 악의적 노드: 잘못된 다이제스트 전송
            msg.digest = "malicious_digest"

        return msg

    def process_message(self, msg: Message) -> List[Message]:
        """메시지 수신 및 처리"""
        key = f"{msg.view}:{msg.sequence}"

        if key not in self.log:
            self.log[key] = []
        self.log[key].append(msg)

        responses = []

        # PREPARE 단계: PRE-PREPARE 수신 후 PREPARE 브로드캐스트
        if msg.msg_type == MessageType.PRE_PREPARE:
            prepare_msg = Message(
                MessageType.PREPARE, msg.view, msg.sequence,
                msg.digest, self.node_id, ""
            )
            responses.append(prepare_msg)

        # COMMIT 단계: 2f+1개의 PREPARE 수신 시 COMMIT 브로드캐스트
        elif msg.msg_type == MessageType.PREPARE:
            prepare_count = sum(
                1 for m in self.log[key]
                if m.msg_type == MessageType.PREPARE and m.digest == msg.digest
            )
            if prepare_count >= 2 * self.f:  # 2f + 1 (자신 포함)
                commit_msg = Message(
                    MessageType.COMMIT, msg.view, msg.sequence,
                    msg.digest, self.node_id, ""
                )
                responses.append(commit_msg)

        # FINALIZE: 2f+1개의 COMMIT 수신 시 상태 확정
        elif msg.msg_type == MessageType.COMMIT:
            commit_count = sum(
                1 for m in self.log[key]
                if m.msg_type == MessageType.COMMIT and m.digest == msg.digest
            )
            if commit_count >= 2 * self.f + 1:
                self.state[msg.sequence] = msg.digest
                print(f"[Node {self.node_id}] Sequence {msg.sequence} FINALIZED: {msg.digest[:8]}...")

        return responses


def simulate_pbft():
    """PBFT 합의 시뮬레이션: 4개 노드, 1개 비잔틴 노드 포함"""
    nodes = [
        PBFTNode(0, 4, is_byzantine=False),
        PBFTNode(1, 4, is_byzantine=True),   # 악의적 노드
        PBFTNode(2, 4, is_byzantine=False),
        PBFTNode(3, 4, is_byzantine=False),
    ]
    nodes[0].is_primary = True

    request = "Transfer 100 ETH from Alice to Bob"

    # 1. Pre-prepare (Primary)
    pre_prepare_msg = nodes[0].pre_prepare(view=0, sequence=1, request=request)

    # 2. Prepare phase (모든 노드에게 전파)
    prepare_msgs = []
    for node in nodes:
        responses = node.process_message(pre_prepare_msg)
        prepare_msgs.extend(responses)

    # 3. Prepare 메시지 전파
    commit_msgs = []
    for msg in prepare_msgs:
        for node in nodes:
            if node.node_id != msg.sender:
                responses = node.process_message(msg)
                commit_msgs.extend(responses)

    # 4. Commit 메시지 전파 및 파이널라이즈
    for msg in commit_msgs:
        for node in nodes:
            if node.node_id != msg.sender:
                node.process_message(msg)

    print("\n=== 최종 상태 ===")
    for node in nodes:
        if not node.is_byzantine:
            print(f"Node {node.node_id}: {node.state}")


if __name__ == "__main__":
    simulate_pbft()
    # 출력: 정직한 3개 노드 모두 동일한 상태로 파이널라이즈됨
    # 비잔틴 노드의 잘못된 메시지는 2f+1개의 합의에 도달하지 못해 무시됨
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 주요 합의 알고리즘

| 평가 지표 | PoW (Bitcoin) | PoS (Ethereum 2.0) | PBFT (Hyperledger) | DPoS (EOS) |
| :--- | :--- | :--- | :--- | :--- |
| **에너지 소모** | 극도로 높음 (국가 규모) | **매우 낮음** (99.95% 절감) | 낮음 | 낮음 |
| **TPS (처리량)** | 7 TPS | 15~30 TPS (L2로 확장) | **10,000+ TPS** | 4,000+ TPS |
| **완결성 (Finality)** | 확률적 (6 confirmations) | 확률적 + 에포크 파이널리티 | **즉각적 (1 블록)** | 확률적 |
| **탈중앙화** | **높음** (누구나 참여) | 높음 (32 ETH 스테이킹) | 낮음 (허가형) | 낮음 (21개 BP) |
| **비잔틴 내성** | 50% 해시 파워 | 33% 스테이킹 | **33% 노드** | 33% BP |
| **공격 비용** | 51% 해시 파워 구매 | 51% 스테이킹 매수 | 노드 탈취 | BP 선거 조작 |
| **적합한 환경** | 퍼블릭, 최대 보안 | 퍼블릭, 스마트 컨트랙트 | **기업용, 프라이빗** | 고성능 dApp |

### 2. CAP 정리와 합의 알고리즘 트레이드오프

| CAP 속성 | 설명 | PoW/PoS | PBFT |
| :--- | :--- | :--- | :--- |
| **Consistency (일관성)** | 모든 노드가 동시에 동일한 데이터 조회 | ** eventual consistency** | **Strong consistency** |
| **Availability (가용성)** | 항상 응답 가능 | **높음** (일부 노드 장애 허용) | 낮음 (2f+1 노드 필요) |
| **Partition Tolerance (분할 내성)** | 네트워크 분할 시에도 작동 | **높음** (Longest Chain Rule) | 낮음 (분할 시 합의 불가) |

**FLP 불가능성 증명**: 비동기 분산 시스템에서는 장애가 하나라도 존재하면 합의 알고리즘이 종료됨을 보장할 수 없습니다. PoW/PoS는 **확률적 종료**로, PBFT는 **부분 동기성 가정**으로 이를 우회합니다.

### 3. 과목 융합 관점 분석 (합의 알고리즘 + 타 도메인 시너지)
- **합의 알고리즘 + 암호학 (VRF, Threshold Signature)**: 최신 합의 알고리즘은 **VRF(Verifiable Random Function)**를 사용하여 리더를 무작위로 선정합니다. 이는 예측 불가능한 리더 선정으로 공격을 방지합니다. **임계값 서명(Threshold Signature)**은 수천 개의 서명을 하나로 압축하여 PBFT의 O(N²) 통신 복잡도를 O(N)으로 개선합니다.

- **합의 알고리즘 + 경제학 (게임 이론, 메커니즘 디자인)**: PoW와 PoS는 **내쉬 균형(Nash Equilibrium)**을 이용합니다. "정직하게 행동하는 것이 기대 수익이 더 높다"는 경제적 유인 구조를 설계하여, 이기적인 참여자들이 자연스럽게 정직하게 행동하도록 유도합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략
- **[상황 A] 기업 간 무역 금융 플랫폼 구축**
  - **문제점**: 여러 은행과 기업이 참여하는 컨소시엄에서, 높은 TPS와 즉각적 파이널리티가 필요. 거래 내역은 기밀성이 요구됨.
  - **기술사 판단 (전략)**: **Hyperledger Fabric (PBFT 기반)** 도입. 채널(Channel)을 통한 데이터 격리, MSP(멤버십 서비스 제공자)를 통한 허가형 접근 제어. PBFT의 즉각적 파이널리티로 거래 확정 지연 없음. 노드 수가 적은 컨소시엄 환경에서 O(N²) 통신 복잡도는 감수 가능.

- **[상황 B] 글로벌 NFT 마켓플레이스 서비스**
  - **문제점**: 전 세계 사용자가 참여해야 하며, 검열 저항성이 중요. 수수료와 속도 모두 중요.
  - **기술사 판단 (전략)**: **Polygon (PoS + L2)** 또는 **Solana (PoH + PoS)** 도입. 이더리움의 보안성을 계승하면서도 낮은 가스비와 높은 TPS 제공. 탈중앙화된 퍼블릭 네트워크로 검열 저항성 확보.

### 2. 도입 시 고려사항 (기술적/보안적 체크리스트)
- **51% 공격 대비책**: PoW/PoS 네트워크에서 51% 공격이 발생할 경우를 대비한 **포크(Fork) 전략**과 **커뮤니티 거버넌스** 프로세스를 사전에 정의해야 합니다. PoS에서는 슬래싱(Slashing) 메커니즘으로 경제적 처벌을 자동화합니다.

- **노드 운영 복잡도**: PBFT는 노드 수가 증가할수록 통신량이 제곱으로 증가하여, 100개 이상의 노드에서는 성능이 급격히 저하됩니다. 대규모 노드 환경에서는 **Istanbul BFT** 또는 **Tendermint**와 같은 개선된 BFT 변형을 고려해야 합니다.

### 3. 주의사항 및 안티패턴 (Anti-patterns)
- **Nothing at Stake 문제 (PoS)**: PoS에서 검증자가 모든 포크에 동시에 투표해도 페널티가 없는 문제입니다. 이더리움 2.0은 **슬래싱(Slashing)**으로 충돌하는 블록에 서명한 검증자의 스테이크를 몰수하여 해결합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과 (도입 전후 ROI)

| 구분 | 중앙 집중형 서버 (AS-IS) | 분산 합의 시스템 (TO-BE) | 개선 지표 (Impact) |
| :--- | :--- | :--- | :--- |
| **단일 장애점 (SPOF)** | 존재 (서버 다운 시 서비스 중단) | **없음** (노드 분산) | 가용성 99.99% 이상 |
| **데이터 무결성** | 관리자가 수정/삭제 가능 | **위변조 불가능** (합의 필요) | 데이터 신뢰성 100% |
| **거래 투명성** | 내부 DB (불투명) | **공개 원장** (누구나 검증) | 감사 비용 90% 절감 |

### 2. 미래 전망 및 진화 방향
- **Proof of History (Solana)**: 시간의 흐름 자체를 암호학적으로 증명하여, 합의 전에 트랜잭션 순서를 미리 정할 수 있습니다. 이를 통해 병렬 실행과 65,000 TPS를 달성합니다.

- **DAG 기반 합의 (Avalanche, Fantom)**: 블록체인의 선형 구조 대신 DAG(방향성 비순환 그래프)를 사용하여, 트랜잭션이 서로를 직접 참조하며 병렬로 합의가 이루어집니다. 확장성과 속도가 비약적으로 향상됩니다.

### 3. 참고 표준/가이드
- **Raft Consensus Algorithm**: 크래시 장애 허용(CFT) 합의의 사실상 표준 (etcd, Consul)
- **PBFT (Practical Byzantine Fault Tolerance)**: MIT LCS-TR-1999, 허가형 블록체인의 기반
- **Casper FFG (Ethereum)**: PoS 파이널리티 가젯 표준

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **[블록체인 (Blockchain)](@/studynotes/06_ict_convergence/02_blockchain/blockchain.md)**: 합의 알고리즘이 적용되는 분산 원장 인프라.
- **[비잔틴 장애 허용 (BFT)](./bft.md)**: 악의적 노드가 존재해도 합의를 보장하는 이론적 기반.
- **[이더리움 2.0 (PoS)](./ethereum2.md)**: 지분 증명 기반의 대규모 블록체인 플랫폼.
- **[하이퍼레저 패브릭 (Hyperledger Fabric)](./hyperledger_fabric.md)**: PBFT 기반의 기업용 블록체인 프레임워크.

---

## 👶 어린이를 위한 3줄 비유 설명
1. 합의 알고리즘은 친구들이 모여서 '무슨 놀이를 할지' 정할 때의 '투표 규칙'이에요!
2. 어떤 규칙은 '달리기 시합에서 1등 한 친구의 말을 따른다'(PoW), 어떤 규칙은 '가장 많은 사탕을 가진 친구의 말을 따른다'(PoS)예요.
3. 이 규칙 덕분에 거짓말쟁이 친구가 있어도, 우리 모두가 똑같은 놀이를 할 수 있게 돼요!
