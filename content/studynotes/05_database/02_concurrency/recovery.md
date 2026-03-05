+++
title = "데이터베이스 복구 (Recovery) 및 ARIES 알고리즘"
date = "2026-03-04"
[extra]
categories = "studynotes-05_database"
+++

# 데이터베이스 복구 (Recovery) 및 ARIES 알고리즘

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시스템 장애(Crash), 미디어 장애(Disk Failure), 트랜잭션 장애 발생 시, ACID 특성 중 원자성(Atomicity)과 영속성(Durability)을 보장하기 위해 로그(Log)를 활용하여 데이터베이스를 일관된 상태로 복원하는 DBMS 핵심 기술입니다.
> 2. **가치**: REDO(재실행)와 UNDO(취소) 연산을 통해 커밋된 트랜잭션의 결과는 보장하고, 미완료된 트랜잭션의 영향은 제거하여, 어떠한 장애 상황에서도 'Zero Data Loss'와 'Point-in-Time Recovery'를 실현합니다.
> 3. **융합**: 운영체제의 파일 시스템 저널링(Journaling), 분산 시스템의 합의 알고리즘(Raft Log), 그리고 블록체인의 불변 원장(Ledger) 기술과 동일한 '로그 기반 복구' 철학을 공유합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**데이터베이스 복구(Recovery)**는 장애가 발생했을 때 데이터베이스를 장애 직전의 일관된(Consistent) 상태로 되돌리는 기술입니다. 현대 DBMS는 **WAL(Write-Ahead Logging)** 프로토콜을 기반으로, 모든 데이터 변경 사항을 로그 파일에 먼저 기록한 후 실제 데이터 파일에 반영함으로써, 장애 발생 시 로그를 재생(REDO)하거나 취소(UNDO)하여 복구를 수행합니다.

- **REDO (재실행)**: 커밋되었으나 디스크에 반영되지 않은 변경사항을 로그에서 찾아 다시 적용 (영속성 보장)
- **UNDO (취소)**: 커밋되지 않은 채로 장애가 발생한 변경사항을 로그에서 찾아 원상 복구 (원자성 보장)
- **WAL (Write-Ahead Logging)**: 데이터 페이지를 디스크에 쓰기 전에 반드시 로그를 먼저 기록하는 프로토콜

#### 2. 💡 비유를 통한 이해
**'은행의 이중 장부와 타임머신'**에 비유할 수 있습니다.

- **로그 파일 = 보조 장부**: 모든 거래 내역을 순서대로 적어두는 별도의 장부입니다. 주 장부(데이터 파일)가 화재로 타버려도 보조 장부만 있으면 모든 거래를 복원할 수 있습니다.
- **REDO = 타임머신으로 미래로**: "10:00에 A 계좌에서 B 계좌로 100만 원 이체 완료(커밋)"라는 기록이 있는데 주 장부에는 반영이 안 되어 있다면, 이 기록을 찾아 다시 실행합니다.
- **UNDO = 타임머신으로 과거로**: "9:55에 C 계좌에서 D 계좌로 50만 원 이체 시작(미커밋)"했는데 9:58에 정전이 났다면, 이 거래를 없었던 일로 되돌립니다.
- **체크포인트 = 마감 시간**: 매시 정각에 "여기까지 정상 완료"라고 표시해두면, 복구할 때 그 시점 이후만 검사하면 됩니다.

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계 (데이터 유실 위험)**: 초기 데이터베이스 시스템은 데이터를 메모리에서 수정하고 즉시 디스크에 기록했습니다. 그러나 시스템 크래시(Crash)가 발생하면 메모리의 모든 데이터가 사라져, 커밋된 트랜잭션의 결과마저 영구 소실되는 치명적인 문제가 있었습니다.
2. **혁신적 패러다임의 도입 (WAL 프로토콜)**: 1970년대 Jim Gray 등이 제안한 WAL 프로토콜은 "데이터 변경 전에 로그를 먼저 쓰라"는 원칙을 확립했습니다. 로그는 순차적(Sequential)으로 쓰기 때문에 랜덤 액세스(Random Access)인 데이터 파일 쓰기보다 훨씬 빠르고 안전합니다.
3. **ARIES 알고리즘의 등장 (1992)**: IBM의 C. Mohan 등이 개발한 ARIES(Algorithm for Recovery and Isolation Exploiting Semantic Semantics)는 현대 모든 RDBMS(Oracle, SQL Server, PostgreSQL, MySQL)의 복구 알고리즘 표준이 되었습니다. "Redo before Undo", "Page-oriented Recovery", "Compensation Log Records" 등의 혁신적 개념을 도입했습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 복구 시스템 구성 요소 (표)

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:|
| **WAL 로그 버퍼** | 메모리 내 로그 임시 저장 | 로그 레코드를 모아서 한 번에 디스크로 플러시 (I/O 최소화) | Log Buffer Pool | 메모장 |
| **Redo 로그 파일** | 영구적인 로그 저장소 | 순차 쓰기(Sequential Write) 전용 파일, Circular Buffer | Redo Log, WAL File | 보조 장부 |
| **데이터 버퍼 풀** | 데이터 페이지 캐싱 | Dirty Page(수정된 페이지) 관리, Checkpoint 시 일괄 플러시 | Buffer Pool, Page Cache | 작업대 |
| **체크포인트 (Checkpoint)** | 복구 기준점 설정 | 주기적으로 버퍼 풀의 Dirty Page를 디스크에 동기화 | Fuzzy Checkpoint | 마감 표시 |
| **LSN (Log Sequence Number)** | 로그 레코드 고유 번호 | 단조 증가하는 번호, 복구 시점 식별에 사용 | Monotonic Counter | 페이지 번호 |
| **CLR (Compensation Log Record)** | UNDO 수행 중 생성되는 로그 | UNDO 도중 장애가 나도 중복 UNDO 방지 | ARIES 전용 | 취소 영수증 |

#### 2. ARIES 복구 알고리즘 아키텍처 다이어그램

```text
================================================================================
                     [ ARIES Recovery Algorithm Architecture ]
================================================================================

[ 정상 운영 시 (Normal Operation) ]

    [Transaction]          [Log Buffer]              [Redo Log File]
         |                       |                         |
         | BEGIN TRANSACTION     |                         |
         |---------------------->| Log: <T1, BEGIN>        |
         |                       |------------------------>| (LSN: 100)
         | UPDATE: SET x = 10    |                         |
         |---------------------->| Log: <T1, X, 5→10, LSN:101>
         |                       |------------------------>| (Force at Commit)
         | COMMIT                |                         |
         |---------------------->| Log: <T1, COMMIT>       |
         |                       |------------------------>| (LSN: 102, Force!)

[ 장애 발생 및 복구 시 (Crash Recovery) ]

         시스템 재기동
               │
               ▼
    ┌─────────────────────────────────────────────────────────────────────┐
    │                   [ Phase 1: Analysis ]                              │
    │  - 마지막 Checkpoint 위치 파악                                        │
    │  - RedoLSN 결정 (어디서부터 Redo를 시작할지)                           │
    │  - Dirty Page Table (DPT) 복원: 메모리에 있던 수정된 페이지 목록         │
    │  - Active Transaction List: 장애 시점에 진행 중이던 트랜잭션 식별        │
    └─────────────────────────────────────────────────────────────────────┘
               │
               ▼
    ┌─────────────────────────────────────────────────────────────────────┐
    │                   [ Phase 2: Redo ]                                  │
    │  - RedoLSN부터 로그 끝까지 순차적으로 재생                             │
    │  - 커밋 여부와 관계없이 모든 변경사항을 다시 적용                        │
    │  - Page LSN vs Log LSN 비교: 이미 적용된 것은 스킵                      │
    │  - 목표: 데이터베이스을 Crash 직전의 정확한 상태로 복원                   │
    │                                                                      │
    │  for each log record from RedoLSN to End:                           │
    │      if (PageLSN < LogLSN):                                         │
    │          apply change to page                                       │
    │          PageLSN = LogLSN                                           │
    └─────────────────────────────────────────────────────────────────────┘
               │
               ▼
    ┌─────────────────────────────────────────────────────────────────────┐
    │                   [ Phase 3: Undo ]                                  │
    │  - Analysis에서 식별한 '미완료 트랜잭션'들을 롤백                       │
    │  - 로그를 역순(최신→과거)으로 탐색하며 변경사항 취소                     │
    │  - UNDO 수행 시 CLR(Compensation Log Record) 작성                    │
    │  - 목표: 원자성 보장 (All-or-Nothing)                                 │
    │                                                                      │
    │  for each incomplete transaction:                                   │
    │      rollback changes in reverse order                              │
    │      write CLR for each undo operation                              │
    └─────────────────────────────────────────────────────────────────────┘
               │
               ▼
         [ Recovery Complete ]
         [ Database Consistent ]

================================================================================
                     [ 로그 레코드 구조 (Log Record Structure) ]
================================================================================

+--------+------+----------+----------+-----------+------------+
|  LSN   | TxID |  Type    | PageID   | PrevLSN   | UndoNextLSN|
+--------+------+----------+----------+-----------+------------+
|  101   | T1   | UPDATE   | P5       | 100       | NULL       |
+--------+------+----------+----------+-----------+------------+
|  102   | T2   | UPDATE   | P3       | 95        | NULL       |
+--------+------+----------+----------+-----------+------------+
|  103   | T1   | COMMIT   | -        | 101       | NULL       |
+--------+------+----------+----------+-----------+------------+
|  104   | T2   | CLR      | P3       | 102       | 94         | <- UNDO 수행 시 생성
+--------+------+----------+----------+-----------+------------+

[ CLR (Compensation Log Record) 설명 ]
- T2가 롤백되는 과정에서 P3에 대한 UNDO를 수행하면 CLR이 생성됨
- UndoNextLSN(94)은 "T2의 다음 UNDO 대상은 LSN 94번이다"를 의미
- 이로 인해 반복 장애 발생 시 이미 UNDO한 작업을 건너뛸 수 있음
```

#### 3. 심층 동작 원리: ARIES의 3단계 복구 메커니즘

**① Analysis Phase (분석 단계)**
```
목표: 복구에 필요한 정보를 수집

1. 마지막 Checkpoint 레코드 위치 확인
2. Checkpoint 이후의 로그를 순차 스캔
3. Dirty Page Table (DPT) 구축
   - 메모리에 있었으나 디스크에 안 쓰인 페이지 목록
4. Active Transaction Table (ATT) 구축
   - 장애 시점에 진행 중이던 트랜잭션 목록
   - 이 트랜잭션들은 Undo 단계에서 롤백됨
5. RedoLSN 계산
   - DPT에서 가장 오래된 페이지의 LSN
   - Redo는 이 지점부터 시작
```

**② Redo Phase (재실행 단계)**
```
목표: 데이터베이스를 Crash 직전 상태로 정확히 복원

1. RedoLSN부터 로그 끝까지 순차 처리
2. 각 로그 레코드에 대해:
   - 해당 페이지가 DPT에 있고, PageLSN < LogLSN이면:
     - 로그의 변경 내용을 페이지에 적용
     - PageLSN = LogLSN으로 업데이트
   - 그렇지 않으면 스킵 (이미 적용됨)
3. 모든 페이지를 Crash 직전 상태로 복원
4. 커밋된 트랜잭션의 영속성(Durability) 보장
```

**③ Undo Phase (취소 단계)**
```
목표: 미완료 트랜잭션의 영향을 제거 (원자성 보장)

1. ATT에 있는 미완료 트랜잭션 목록 확인
2. 각 트랜잭션에 대해 로그를 역순으로 탐색:
   - 로그 레코드의 변경 내용을 취소 (이전 값으로 복원)
   - CLR(Compensation Log Record) 작성
   - PrevLSN을 따라 계속 역순 탐색
3. 모든 미완료 트랜잭션이 롤백 완료되면 종료
4. CLR 덕분에 Undo 도중 다시 장애가 나도 중복 Undo 방지
```

#### 4. 실무 수준의 복구 시나리오 (Oracle/MySQL 예시)

```sql
-- [시나리오] 트랜잭션 T1, T2, T3가 실행 중이고 T2만 커밋된 상태에서 Crash 발생

-- Crash 직전 로그 상태:
-- LSN 100: T1 BEGIN
-- LSN 101: T1 UPDATE accounts SET balance=900 WHERE id=1 (Before: 1000)
-- LSN 102: T2 BEGIN
-- LSN 103: T2 UPDATE accounts SET balance=1100 WHERE id=2 (Before: 1000)
-- LSN 104: T2 COMMIT
-- LSN 105: T3 BEGIN
-- LSN 106: T3 UPDATE accounts SET balance=800 WHERE id=3 (Before: 1000)
-- [CRASH!!!] <- T1과 T3는 커밋하지 않음

-- ==================== RECOVERY PROCESS ====================

-- [Phase 1: Analysis]
-- ATT (Active Transaction Table) = {T1, T3}
-- DPT (Dirty Page Table) = {Page1, Page2, Page3}
-- RedoLSN = 100

-- [Phase 2: Redo] - 모든 변경사항 재적용
-- LSN 101: T1의 변경 (balance=900) 재적용
-- LSN 103: T2의 변경 (balance=1100) 재적용
-- LSN 106: T3의 변경 (balance=800) 재적용
-- 현재 DB 상태: id1=900, id2=1100, id3=800 (Crash 직전과 동일)

-- [Phase 3: Undo] - 미완료 트랜잭션 롤백
-- T3 롤백: LSN 106 취소 -> id3 = 1000으로 복원, CLR 작성
-- T1 롤백: LSN 101 취소 -> id1 = 1000으로 복원, CLR 작성
-- 최종 DB 상태: id1=1000, id2=1100, id3=1000
-- T2(커밋됨)의 변경만 남고, T1, T3(미커밋)는 롤백됨 -> 원자성/영속성 보장!

-- ==================== Oracle Recovery 명령어 ====================

-- 1. 미디어 복구 (데이터 파일 손상 시)
RECOVER DATABASE;
RECOVER TABLESPACE users;
RECOVER DATAFILE '/path/to/file.dbf';

-- 2. Point-in-Time Recovery (특정 시점으로 복원)
RMAN> RUN {
    SET UNTIL TIME '2024-03-15 14:30:00';
    RESTORE DATABASE;
    RECOVER DATABASE;
}

-- 3. 로그 시퀀스 확인
SELECT sequence#, first_change#, next_change#, archived
FROM v$log_history
ORDER BY sequence# DESC;

-- ==================== MySQL InnoDB 복구 설정 ====================

-- my.cnf 설정
[mysqld]
innodb_flush_log_at_trx_commit = 1  -- 커밋 시 로그 강제 플러시 (영속성 보장)
innodb_log_file_size = 256M          -- Redo 로그 파일 크기
innodb_log_files_in_group = 2        -- Redo 로그 파일 개수
innodb_log_buffer_size = 16M         -- 로그 버퍼 크기
innodb_doublewrite = 1               -- Doublewrite Buffer 활성화 (페이지 손상 방지)

-- 복구 모드로 시작
SET GLOBAL innodb_force_recovery = 1;  -- 1~6 단계, 높을수록 제한적
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 복구 기법 비교 (Log-based vs Shadow Paging)

| 비교 항목 | WAL (Write-Ahead Logging) | Shadow Paging (그림자 페이징) |
|:---|:---|:---|
| **기본 원리** | 로그에 변경 내역 기록 | 현재 페이지와 그림자 페이지 이중 유지 |
| **Redo 지원** | 지원 (로그 재생) | 불필요 (페이지 교체) |
| **Undo 지원** | 지원 (로그 역재생) | 불필요 (그림자 페이지로 복원) |
| **트랜잭션 커밋** | 로그 플러시만 하면 됨 (빠름) | 페이지 테이블 스위치 (느림) |
| **저장 공간** | 로그 파일 필요 | 페이지 2배 필요 |
| **현대적 사용** | 모든 RDBMS 표준 | SQLite (WAL 모드 이전) |

#### 2. 과목 융합 관점 분석

- **[운영체제 융합] 파일 시스템 저널링**: Linux ext4, NTFS 등의 파일 시스템도 데이터 손상을 방지하기 위해 저널(Journal)을 사용합니다. 이는 DBMS의 WAL과 동일한 원리입니다. 메타데이터 저널링 vs 전체 데이터 저널링의 트레이드오프가 있습니다.

- **[분산 시스템 융합] Raft/Paxos 로그**: 분산 합의 알고리즘(Raft, Paxos)도 로그를 기반으로 동작합니다. 리더가 로그를 기록하고 팔로워에게 복제하는 과정은 DBMS의 WAL 복제와 유사합니다.

- **[블록체인 융합] 불변 원장**: 블록체인의 트랜잭션 로그는 삭제나 수정이 불가능한 불변 원장(Immutable Ledger)입니다. ARIES의 로그도 일단 기록되면 덮어쓰지 않고 순차적으로만 증가한다는 점에서 유사합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: SSD에서의 Doublewrite Buffer 비활성화 논쟁**
- **상황**: MySQL InnoDB의 Doublewrite Buffer는 페이지 손상 방지를 위해 데이터를 두 번 쓰지만, SSD에서는 쓰기 수명을 단축시키는 우려가 있습니다.
- **기술사적 결단**:
  - Doublewrite Buffer는 **Partial Page Write**(페이지의 일부만 기록되는 현상)를 방지합니다.
  - SSD라도 전원 장애 시 Partial Page Write는 발생할 수 있습니다.
  - 따라서 영속성이 중요한 금융/결제 시스템에서는 Doublewrite를 유지해야 합니다.
  - 쓰기 성능이 극도로 중요하고 일시적 데이터 손실을 감수할 수 있는 캐싱 계층에서만 비활성화를 고려합니다.

**시나리오 2: Point-in-Time Recovery (PITR) 전략**
- **상황**: 오후 2시에 운영자가 실수로 `DELETE FROM users`를 실행했습니다. 전체 백업은 매일 새벽 2시에 수행됩니다.
- **기술사적 결단**:
  1. 즉시 새로운 백업을 수행하여 현재 상태 보존
  2. 전체 백업(새벽 2시)을 별도 서버에 복원
  3. Redo 로그(Archive Log)를 오후 1시 59분 59초까지 순차 적용
  4. 복원된 데이터를 운영 서버로 마이그레이션
  - 이것이 PITR(Point-in-Time Recovery)이며, ARIES 알고리즘의 Redo 원리를 활용합니다.

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **Redo 로그 파일 크기**: 너무 작으면 체크포인트 빈도 증가로 성능 저하, 너무 크면 복구 시간 증가
- [ ] **로그 플러시 주기**: `innodb_flush_log_at_trx_commit=1`(항상) vs `2`(초 단위) 트레이드오프
- [ ] **백업 전략**: Full Backup + Incremental Backup + Archive Log의 3단계 백업 체계 수립

#### 3. 주의사항 및 안티패턴 (Anti-patterns)

- **로그 없는 직접 쓰기**: `O_DIRECT`나 `innodb_flush_method` 설정을 잘못하여 OS 캐시를 우회하되 로그도 안 쓰는 경우, 장애 시 완전히 복구 불가능한 상태가 됩니다.
- **아카이브 로그 미백업**: Redo 로그가 덮어쓰기되면 PITR이 불가능합니다. 반드시 Archive Log로 백업해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 영역 | 내용 | 정량적 목표 / 지표 |
|:---|:---|:---|
| **데이터 무결성** | 장애 후에도 커밋된 데이터 100% 보존 | Zero Data Loss 달성 |
| **복구 시간 (RTO)** | 장애 발생부터 서비스 재개까지의 시간 | RTO < 15분 (Hot Standby) |
| **복구 지점 (RPO)** | 복구 가능한 가장 최근 시점 | RPO < 1초 (Sync Replication) |

#### 2. 미래 전망 및 진화 방향

- **NVM (Non-Volatile Memory) 활용**: Intel Optane과 같은 비휘발성 메모리가 보편화되면, 로그를 디스크에 쓰는 오버헤드가 사라집니다. 메모리 속도로 로그를 기록할 수 있어 복구 성능이 비약적으로 향상될 것입니다.

- **분산 복구 (Distributed Recovery)**: 클라우드 네이티브 데이터베이스(Aurora, Spanner)는 스토리지 계층에서 복구를 수행합니다. 컴퓨팅 노드는 장애 시 즉시 교체되고, 스토리지 계층의 로그 기반 복구가 독립적으로 동작합니다.

- **AI 기반 장애 예측**: 머신러닝을 활용하여 로그 패턴을 분석하고 장애를 사전에 예측하여, 문제가 발생하기 전에 선제적 조치를 취하는 자율 복구 시스템으로 발전할 것입니다.

#### 3. ※ 참고 표준/가이드

- **ARIES Paper (1992)**: C. Mohan et al., "ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks"
- **ACID Properties**: ISO/IEC 10026 (Distributed Transaction Processing)
- **Database Backup Standards**: NIST Special Publication 800-34 (Contingency Planning Guide)

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[ACID](@/studynotes/05_database/01_relational/acid.md)**: 복구는 ACID 중 원자성(A)과 영속성(D)을 보장하는 핵심 메커니즘입니다.
- **[트랜잭션 격리 수준](@/studynotes/05_database/02_concurrency/isolation_level.md)**: 격리 수준과 복구는 MVCC의 Undo 세그먼트를 공유합니다.
- **[버퍼 풀](@/studynotes/05_database/03_optimization/query_optimization.md)**: Dirty Page 관리와 체크포인트는 버퍼 풀과 긴밀하게 연동됩니다.
- **[분산 합의 (Raft/Paxos)](@/studynotes/02_operating_system/02_process_thread/_index.md)**: 분산 DB의 복구는 합의 알고리즘 기반 로그 복제를 사용합니다.
- **[파일 시스템 저널링](@/studynotes/02_operating_system/06_file_system/_index.md)**: OS 파일 시스템도 동일한 WAL 원리를 사용합니다.

---

### 👶 어린이를 위한 3줄 비유 설명

1. **복구**는 마법의 타임머신과 같아요! 컴퓨터가 갑자기 꺼져도, '비디오 테이프(로그)'에 녹화된 내용을 다시 보면서 어디까지 했는지 확인할 수 있거든요.
2. **REDO**는 "녹화된 대로 다시 해보자!" 하는 거예요. 완성했다고 한 숙제(커밋)가 날아갔을 때, 녹화를 보면서 똑같이 다시 쓰는 것이죠.
3. **UNDO**는 "이건 없었던 일로 하자!" 하는 거예요. 다 하지 못한 숙제(미커밋)는 지워버리고 처음처럼 깨끗하게 되돌리는 거예요. 이렇게 하면 어떤 일이 있어도 공책이 엉망이 되지 않아요!
