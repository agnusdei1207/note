+++
weight = 798
title = "798. 주키퍼 (ZooKeeper)를 활용한 분산 락(Distributed Lock)과 합의 동기화"
date = "2026-03-10"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "ZooKeeper", "분산 락", "Distributed Lock", "합의 알고리즘", "Zab", "임계 구역", "클라우드 동기화"]
series = "운영체제 800제"
+++

# 주키퍼 (ZooKeeper)를 활용한 분산 락과 합의 동기화

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 여러 대의 서버로 구성된 분산 환경에서 특정 공유 자원에 대해 오직 하나의 프로세스만 접근할 수 있도록 제어하는 **분산 상호 배제(Distributed Mutual Exclusion)** 기술.
> 2. **가치**: 단일 서버의 뮤텍스(Mutex)를 네트워크 레벨로 확장한 것으로, 주키퍼의 **Znode(임시 순차 노드)**와 **Watch** 기능을 통해 데드락 없는 안정적인 분산 동기화를 제공한다.
> 3. **융합**: 운영체제의 동기화 이론과 분산 시스템의 합의 알고리즘(Zab)이 결합되어, 현대 마이크로서비스 아키텍처(MSA)의 데이터 정합성을 지탱하는 핵심 인프라가 된다.

---

### Ⅰ. 분산 락 (Distributed Lock)의 필요성

- **문제 상황**: 단일 서버 내부에서는 OS 커널이 락을 관리하지만, 서버 A와 서버 B가 서로 다른 물리적 장비에 있을 때는 공통된 커널이 없어 상호 배제가 불가능하다.
- **해결책**: 모든 서버가 공통으로 신뢰할 수 있는 외부 조정자(Coordinator)인 **주키퍼**를 사용하여 락 상태를 관리한다.

---

### Ⅱ. 주키퍼 분산 락 동작 메커니즘 (ASCII)

임시 순차 노드(Ephemeral Sequential Node)를 이용한 '번호표' 방식이다.

```ascii
    [ ZooKeeper Cluster ]
    /locks
       |-- lock-0000001 (Server A) <--- Lowest: ACQUIRED LOCK
       |-- lock-0000002 (Server B) <--- Waiting (Watching 001)
       |-- lock-0000003 (Server C) <--- Waiting (Watching 002)
    
    1. Each server creates a Sequential Znode.
    2. Server with the LOWEST number gets the lock.
    3. Others set a "WATCH" on the node immediately before them.
    4. When lock-001 is deleted (Done/Failed), ZK notifies lock-002.
    5. Server B now holds the lock.
```

---

### Ⅲ. 주키퍼의 핵심 기술 요소

| 기능 | 설명 | 효과 |
|:---|:---|:---|
| **Znode** | 주키퍼 내부의 데이터 단위 (파일/폴더). | 상태 정보 저장 |
| **Ephemeral Node** | 클라이언트 연결이 끊기면 자동으로 삭제되는 노드. | **데드락 방지 (자동 해제)** |
| **Watch** | 노드의 변화를 실시간으로 통지받는 기능. | 바쁜 대기(Busy Wait) 제거 |
| **Zab Protocol** | 주키퍼 노드 간 데이터 일관성을 유지하는 합의 규약. | 분산 환경의 무결성 보장 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 분산 락 구현 시 고려사항: 성능 vs 신뢰성
- **문제**: 주키퍼는 모든 쓰기 작업을 합의해야 하므로 성능(Latency)이 다소 느릴 수 있다.
- **기술사적 결단**: 
  - 극도의 속도가 중요하다면 Redis 기반의 **Redlock**을 검토한다. 
  - 데이터의 엄격한 일관성과 선입선출(FIFO) 보장이 중요하다면 **주키퍼(Curator Recipe)**를 선택하는 것이 기술사적 정석이다.

#### 2. 기술사적 인사이트: 부분 실패 (Partial Failure) 대응
- 네트워크 파티션 발생 시, 주키퍼는 과반수(Quorum) 원칙에 따라 동작한다. 락을 쥔 서버가 네트워크에서 격리되면 임시 노드가 사라져 락이 풀릴 수 있으므로, 세션 타임아웃 설정을 서비스 특성에 맞게 세밀하게 조정해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량/정성 기대효과
- **데이터 정합성 확보**: 분산 DB 업데이트 및 중복 결제 방지.
- **시스템 가용성 향상**: 조정자 장애 시에도 클러스터 합의를 통해 중단 없는 서비스 유지.

#### 2. 미래 전망
최근에는 주키퍼보다 더 빠르고 관리가 쉬운 **etcd (Raft 기반)**가 쿠버네티스의 분산 락과 설정 관리 표준으로 자리 잡고 있다. 하지만 분산 락의 근본적인 원리와 '순차 노드를 이용한 공정성 확보'라는 주키퍼의 사상은 모든 현대적 분산 동기화 시스템의 교과서적인 모델로 계속 남을 것이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[세마포어 P/V 연산](./701_semaphore_pv.md)**: 분산 락의 논리적 모태.
- **[데드락 예방](./705_deadlock_four_conditions.md)**: 임시 노드를 통해 주키퍼가 해결하는 핵심 이슈.
- **[합의 알고리즘 (Raft/Paxos)](../../16_bigdata/TBD_consensus.md)**: 주키퍼 이면에서 돌아가는 물리적 보증 기술.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **분산 락**은 여러 마을(서버) 사람들이 공통으로 쓰는 우물을 한 명씩만 쓰게 해주는 **'공동 마을 회관'**과 같아요.
2. 회관에서 번호표를 나눠주고, 1번이 물을 다 뜨면 2번에게 종(Watch)을 쳐서 알려주는 방식이죠.
3. 만약 1번이 번호표를 쥐고 쓰러져도 회관에서 자동으로 번호표를 회수하니까, 마을 사람들이 우물을 영영 못 쓰는 일은 없답니다!
