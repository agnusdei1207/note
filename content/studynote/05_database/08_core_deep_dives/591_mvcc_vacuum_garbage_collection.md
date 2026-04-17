+++
title = "591. 가비지 컬렉터와 MVCC 진공 프로세스 (MVCC Vacuum Garbage Collection)"
weight = 591
date = "2026-03-04"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)
1. **MVCC의 양날의 검:** 읽기와 쓰기의 동시성을 극대화하기 위해 구버전(Old Version) 데이터를 유지하는 MVCC 아키텍처는 필연적으로 쓸모없는 데드 튜플(Dead Tuple)을 양산합니다.
2. **가비지 컬렉션의 필수성:** 데드 튜플이 디스크 공간을 차지하고 인덱스 스캔 비용을 기하급수적으로 증가시키는 것을 막기 위해, 데이터베이스는 백그라운드에서 주기적인 데이터 정리(Vacuum) 프로세스를 수행해야 합니다.
3. **DBMS별 수거 전략:** Oracle/MySQL은 별도의 Undo 세그먼트에 구버전을 저장하여 비교적 오버헤드가 적으나, PostgreSQL 등은 테이블 내에 구버전을 누적하므로 강력한 Vacuum 정책 및 오토 배큠(Autovacuum) 튜닝이 성능의 핵심입니다.

### Ⅰ. 개요 (Context & Background)
다중 버전 동시성 제어(Multi-Version Concurrency Control, MVCC)는 현대 데이터베이스에서 동시성 문제(Lock 경합)를 해결하는 사실상의 표준입니다. 트랜잭션이 데이터를 업데이트(UPDATE)할 때 기존 데이터를 바로 덮어쓰지 않고 새로운 버전을 생성함으로써, 다른 트랜잭션이 일관된 읽기를 수행할 수 있도록 돕습니다. 그러나 이러한 설계는 더 이상 어느 트랜잭션도 참조하지 않는 과거의 쓰레기 데이터(Dead Tuple)를 디스크에 방치하게 만들며, 이를 지속적으로 청소(Garbage Collection, Vacuum)하지 않으면 심각한 성능 저하(Bloat 현상)가 발생합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
+-----------------------------------------------------------+
|               MVCC Vacuum / Garbage Collection            |
+-----------------------------------------------------------+
|  Time T1: Insert Row A (xmin=100, xmax=0)                 |
|  Time T2: Update Row A -> A'                              |
|           Row A  (xmin=100, xmax=101) => [Dead Tuple]     |
|           Row A' (xmin=101, xmax=0)   => [Live Tuple]     |
|                                                           |
|       +-------------------------------------------+       |
|       | Autovacuum Daemon / Garbage Collector     |       |
|       +-------------------------------------------+       |
|              | (Scans for Tuples where xmax < Oldest TX)  |
|              V                                            |
|    [ Reclaims Space of Row A for future Inserts ]         |
|    [ Updates Visibility Map (VM) and FSM        ]         |
+-----------------------------------------------------------+
```

1. **데드 튜플(Dead Tuple)의 발생**
   - UPDATE 연산은 내부적으로 DELETE 후 새로운 버전을 INSERT 하는 방식으로 동작합니다.
   - 현재 실행 중인 활성 트랜잭션 중 가장 오래된 트랜잭션의 시작 시점보다 더 과거에 삭제/수정된 튜플은 더 이상 누구에게도 보일 필요가 없는 데드 튜플이 됩니다.
2. **Vacuum (진공) 메커니즘**
   - **일반 Vacuum:** 락(Lock)을 걸지 않고 테이블을 스캔하며 데드 튜플을 식별하여 빈 공간(Free Space Map, FSM)으로 반환합니다. OS에 디스크 공간을 즉시 반환하지는 않지만, 미래의 트랜잭션이 그 공간을 재사용하게 합니다.
   - **Vacuum Full:** 테이블 전체를 새로 작성하여 단편화(Fragmentation)를 제거하고 OS에 디스크 용량을 반환합니다. 이 과정에서 강력한 배타적 락(Table Lock)이 발생하여 서비스가 중단될 수 있습니다.
3. **가시성 맵 (Visibility Map, VM)**
   - Vacuum 스캔 최적화를 위해, 각 데이터 블록에 데드 튜플이 존재하는지 여부를 비트맵으로 관리하여 청소 대상을 빠르게 식별합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 특성 | PostgreSQL 방식 (Table-level MVCC) | Oracle / MySQL 방식 (Undo Segment MVCC) | 인메모리 DB 방식 (Epoch-based GC) |
| :--- | :--- | :--- | :--- |
| **구버전 저장 위치** | 원본 데이터 블록과 동일한 테이블 파일 내 | 별도의 롤백/Undo 세그먼트 블록 | 메모리 상의 버전 체인 (Linked List) |
| **Bloat(비대화) 현상** | 잦은 UPDATE 시 테이블과 인덱스가 급격히 비대해짐 | 테이블 자체는 비대해지지 않으나 Undo 공간 관리 필요 | 메모리 누수 방지를 위한 주기적 해제 |
| **GC 수행 주체** | Autovacuum 데몬 프로새스 | Undo 자동 덮어쓰기 (별도 백그라운드 데몬 불필요) | Epoch 관리를 통한 스레드 안전성 기반 GC |
| **관리 난이도** | 높음 (Vacuum 임계치 및 스케줄링 섬세한 튜닝 필요) | 낮음 (Undo Retention 크기만 적절히 설정) | 중간 (메모리 단편화 제어 로직 의존) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **성능 튜닝 전략:** PostgreSQL 기반 시스템 운영 시 가장 흔히 접하는 장애 요인이 바로 Vacuum 지연으로 인한 테이블 팽창입니다. 시스템 자원이 여유로운 새벽 시간에 수동으로 `VACUUM ANALYZE`를 수행하도록 크론(Cron) 작업을 배치하고, 잦은 변경이 일어나는 테이블은 `autovacuum_vacuum_scale_factor`를 낮추어 더 자주 청소되도록 튜닝해야 합니다.
- **아키텍처 관점:** 설계 단계에서 이력 테이블(History Table)을 분리하거나 논리적 삭제(Use_YN 플래그 업데이트) 패턴을 남용하는 경우, UPDATE가 빈번히 발생하여 막대한 가비지를 유발하므로 쓰기 전용(Append-only) 아키텍처 설계를 적극 고려해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
MVCC 환경에서 가비지 컬렉션(Vacuum) 프로세스의 정교한 통제는 동시성 성능과 직결됩니다. 지속적인 블로트 현상은 I/O 대역폭 낭비와 캐시 효율성 저하를 유발하므로, 최신 RDBMS 릴리스들은 인덱스 파티셜 청소 구조 도입 및 가시성 맵 최적화 등을 통해 이 과정을 투명하고 가볍게 진화시키고 있습니다. 안정적인 대용량 트랜잭션 처리를 위해서는 내부 쓰레기 수거 알고리즘에 대한 DBA와 엔지니어의 깊은 이해가 필수적입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 트랜잭션, 동시성 제어 (Concurrency Control)
- **연관 개념:** MVCC, 롤백 세그먼트 (Undo Segment), 단편화 (Fragmentation), 옵티마이저 통계 정보
- **파생 기술:** Autovacuum 튜닝, Free Space Map (FSM), Append-only Architecture

### 👶 어린이를 위한 3줄 비유 설명
1. 여러 친구들이 그림을 그릴 때 스케치북 하나에 계속 지웠다 그렸다 하면 구멍이 나기 쉬워서, 새로운 종이를 겹쳐서 그리는 방식을 사용해요.
2. 하지만 계속 새로운 종이를 겹치다 보면 방 안이 온통 필요 없는 옛날 스케치들로 가득 차서 발 디딜 틈이 없게 된답니다.
3. 그래서 로봇 청소기(가비지 컬렉터)가 몰래 돌아다니며 더 이상 아무도 보지 않는 옛날 그림들을 치워주고 새로운 종이를 놓을 자리를 만들어주는 거예요!