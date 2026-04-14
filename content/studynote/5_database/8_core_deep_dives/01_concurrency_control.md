+++
title = "데이터베이스 동시성 제어 (Concurrency Control)"
weight = 1
description = "다중 사용자 환경에서의 데이터 무결성 보장과 트랜잭션 격리 메커니즘"
tags = ["Database", "Transaction", "Concurrency", "Locking", "MVCC"]
+++

## 핵심 인사이트 (3줄 요약)
- **ACID와 동시성의 상충:** 트랜잭션의 격리성(Isolation)을 높이면 데이터 일관성은 완벽해지나 동시 처리 성능이 저하되는 강력한 트레이드오프 관계가 존재.
- **락(Locking) 기반 제어:** 비관적 제어 방식인 Lock(Shared, Exclusive) 메커니즘을 통해 갱신 분실(Lost Update) 등 이상 현상을 방지.
- **다중 버전 동시성 제어(MVCC):** 락 대기를 최소화하기 위해 데이터의 변경 버전을 여러 개 유지하여 읽기와 쓰기 작업이 서로를 블로킹하지 않도록 하는 현대적 DBMS의 핵심 기술.

### Ⅰ. 개요 (Context & Background)
다중 사용자 환경의 데이터베이스에서는 여러 트랜잭션이 동시에 동일한 데이터에 접근하고 수정하려는 시도가 끊임없이 발생합니다. 이때 아무런 제어가 없다면 갱신 분실(Lost Update), 오손 읽기(Dirty Read), 반복 불가능한 읽기(Non-Repeatable Read), 팬텀 읽기(Phantom Read) 등의 이상 현상(Anomaly)이 발생하여 데이터의 무결성이 훼손됩니다. 동시성 제어(Concurrency Control)는 이러한 이상 현상을 방지하면서도 시스템의 처리량을 최대화하기 위한 동기화 기법입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
데이터베이스는 락(Lock)과 UNDO 데이터를 활용하여 동시성을 제어합니다.

```text
+-------------------------------------------------------------+
|             MVCC (Multi-Version Concurrency Control)        |
+-------------------------------------------------------------+
| Time |  Transaction A (Writer)   |  Transaction B (Reader)  |
|------+---------------------------+--------------------------|
|  T1  | BEGIN;                    | BEGIN;                   |
|  T2  | UPDATE Account SET bal=50 |                          |
|      | (Lock Acquired)           |                          |
|      | (Original bal=100 -> UNDO)|                          |
|  T3  |                           | SELECT bal FROM Account; |
|      |                           | -> Reads 100 from UNDO   |
|      |                           |    (No Lock Waiting!)    |
|  T4  | COMMIT; (Lock Released)   |                          |
|  T5  |                           | SELECT bal FROM Account; |
|      |                           | -> Reads 50 (Committed)  |
+-------------------------------------------------------------+
```

1. **Locking 기반 제어 (Pessimistic Concurrency Control):**
   - **Shared Lock (S-Lock):** 데이터를 읽을 때 사용. S-Lock 간에는 호환되나 X-Lock과는 호환 불가.
   - **Exclusive Lock (X-Lock):** 데이터를 쓸(변경) 때 사용. 다른 어떤 Lock과도 호환되지 않아 독점적 접근 보장.
   - **Deadlock (교착 상태):** 두 개 이상의 트랜잭션이 서로의 Lock 해제를 무한정 기다리는 상태로, DBMS의 Deadlock 감지 알고리즘에 의해 하나를 롤백(Rollback)하여 해결.
2. **다중 버전 동시성 제어 (MVCC):**
   - 레코드가 업데이트될 때, 변경 전의 데이터를 UNDO 영역(또는 Rollback Segment)에 보관합니다.
   - 다른 트랜잭션이 해당 레코드를 조회할 때, 현재 트랜잭션의 격리 수준(Isolation Level)과 기준 시간(SCN)에 맞춰 UNDO 영역의 데이터를 조합하여 일관된 읽기(Consistent Read)를 제공합니다.
   - 이로 인해 **"읽기는 쓰기를 블로킹하지 않고, 쓰기는 읽기를 블로킹하지 않는다"**는 장점이 있습니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 이상 현상 (Anomaly) | 설명 | 트랜잭션 격리 수준 (Isolation Level) 기반 방어 |
|---|---|---|
| **Dirty Read** | 커밋되지 않은 데이터를 읽음 | `READ COMMITTED` 이상에서 방지됨 |
| **Non-Repeatable Read** | 한 트랜잭션 내에서 같은 조회 결과가 달라짐 (중간에 타 트랜잭션이 Update) | `REPEATABLE READ` 이상에서 방지됨 |
| **Phantom Read** | 한 트랜잭션 내에서 없던 데이터가 나타남 (중간에 타 트랜잭션이 Insert) | `SERIALIZABLE` 에서 방지됨 (일부 DBMS는 MVCC로 `REPEATABLE READ`에서도 방지) |

*참고: 격리 수준이 `SERIALIZABLE`에 가까울수록 정합성은 높아지나 동시성은 크게 저하됩니다.*

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
기술사는 비즈니스 도메인의 특성에 맞춰 최적의 격리 수준과 동시성 제어 전략을 설계해야 합니다.
- **낙관적 제어 vs 비관적 제어:** 충돌 발생 확률이 낮은 일반적인 웹 서비스에서는 애플리케이션 레벨의 버전 컬럼(Version Column)을 이용한 낙관적 락(Optimistic Lock)을 사용하여 DB 부하를 줄입니다. 반면, 금융/티켓팅 등 충돌이 빈번하고 엄격한 정합성이 요구되는 도메인에서는 비관적 락(`SELECT ... FOR UPDATE`)을 적극 사용해야 합니다.
- **MVCC 한계 고려:** MVCC는 높은 동시성을 제공하지만 UNDO 영역의 과도한 확장을 초래할 수 있으므로, 장기 실행 트랜잭션(Long-running Transaction)을 최소화하도록 애플리케이션 트랜잭션 바운더리를 짧게 설계하는 것이 필수적입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
정교한 동시성 제어는 대규모 트래픽을 처리하는 분산 시스템에서 데이터 신뢰성을 지탱하는 가장 근본적인 토대입니다. 현대의 분산 데이터베이스 환경(NewSQL 등)에서도 2PC(Two-Phase Commit) 및 합의 알고리즘(Raft/Paxos)과 결합된 글로벌 동시성 제어가 연구/적용되고 있으며, 관계형 데이터베이스의 트랜잭션 처리 기술은 앞으로도 무결성 보장의 핵심 표준으로 작용할 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **트랜잭션 속성:** ACID (Atomicity, Consistency, Isolation, Durability)
- **동시성 제어 기법:** 2-Phase Locking (2PL), MVCC, Timestamp Ordering
- **이상 현상:** Lost Update, Dirty Read, Phantom Read

### 👶 어린이를 위한 3줄 비유 설명
1. 여러 명의 친구가 하나의 **도화지(데이터베이스)**에 동시에 그림을 그리려고 하면 서로 손이 부딪혀서 그림이 망가질 수 있어요(이상 현상).
2. 그래서 한 친구가 그릴 때는 다른 친구가 기다리도록 **규칙(Locking)**을 정해요.
3. 똑똑한 도화지는 친구가 그림을 수정하는 동안, 다른 친구들에게는 **수정하기 전의 그림(MVCC)**을 보여줘서 서로 방해받지 않고 그림을 볼 수 있게 해준답니다!