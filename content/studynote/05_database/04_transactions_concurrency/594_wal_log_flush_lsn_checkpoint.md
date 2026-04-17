+++
weight = 594
title = "WAL 로그 플러시 및 LSN 기반 체크포인트 (WAL Log Flush & LSN Checkpoint)"
date = "2024-03-20"
[extra]
categories = "database"
+++

## 핵심 인사이트 (3줄 요약)
- **지연 쓰기 보장**: 데이터 변경 시 데이터 페이지보다 로그를 먼저 디스크에 기록(Write-Ahead Logging)하여 원자성과 영속성을 보장함.
- **LSN 관리**: 로그 레코드에 순차적 번호(Log Sequence Number)를 부여하여 복구 시 재실행(Redo) 및 취소(Undo)의 기준점으로 활용함.
- **체크포인트 최적화**: 메모리 내 더티 페이지를 디스크와 동기화하고 복구 시작 지점을 전진시켜 장애 복구 시간(RTO)을 단축함.

### Ⅰ. 개요 (Context & Background)
데이터베이스 장애 시 데이터의 무결성을 보존하기 위해서는 변경 내용을 즉시 데이터 파일에 기록하는 대신, 순차적 쓰기가 가능한 로그 파일에 먼저 기록하는 **WAL(Write-Ahead Logging)** 매커니즘이 필수적이다. 특히 대규모 트랜잭션 환경에서 **LSN(Log Sequence Number)**은 로그의 순서를 정의하고, **체크포인트(Checkpoint)**는 로그 파일의 비대화를 막고 복구 속도를 높이는 핵심 기술이다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
WAL 매커니즘은 로그 버퍼의 내용을 로그 파일로 플러시(Flush)한 후에야 데이터 페이지를 디스크에 기록할 수 있다는 제약 조건을 가진다.

```text
[ Database Memory (Buffer Pool) ]           [ Persistent Storage (Disk) ]
+-------------------------------+           +---------------------------+
|  Dirty Data Page (LSN: 150)   | --------> |   Data File (.mdf / .dbf) |
|  (Not yet flushed to Disk)    |  Step 2   |   (Sync after Log Flush)  |
+-------------------------------+           +---------------------------+
               |                                         ^
               | (Constraint: Log LSN >= Page LSN)       |
               v                                         |
+-------------------------------+           +---------------------------+
|  Log Buffer (LSN: 100-200)    | --------> |   WAL Log File (.log)     |
|  (Sequential Writes)          |  Step 1   |   (LSN: 100, 110, 120...) |
+-------------------------------+           +---------------------------+
         "Log Flush First"                   "Write-Ahead Logging"
```

1. **Log Record Generation**: 트랜잭션 발생 시 변경 전/후 이미지를 포함한 로그 레코드가 LSN과 함께 로그 버퍼에 생성됨.
2. **Log Flush (Commit 시점)**: 트랜잭션이 커밋되거나 로그 버퍼가 가득 차면 OS 캐시를 거치지 않고 직접 디스크(WAL File)에 동기적으로 쓰여짐.
3. **LSN (Log Sequence Number)**: 로그 레코드의 위치를 나타내는 64비트 정수로, 데이터 페이지 내에도 포함되어 복구 시 중복 Redo 여부를 판단함.
4. **Checkpoint**: 버퍼 풀의 더티 페이지를 디스크에 쓰고, 복구 성공 지점을 로그 파일에 기록하여 이후 로그를 재사용 가능하게 함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | WAL (Log-based) | Shadow Paging (Page-based) |
| :--- | :--- | :--- |
| **작동 원리** | 변경 이력을 로그에 추가 기록 | 변경된 페이지의 복사본(Shadow) 생성 |
| **쓰기 오버헤드** | 적음 (순차 쓰기 위주) | 많음 (복사본 생성 및 포인터 갱신) |
| **복구 방식** | Redo / Undo 로그 재현 | Current와 Shadow 페이지 교체 |
| **적합성** | 대부분의 고성능 RDBMS (Oracle, MySQL, PG) | SQLite, 일부 NoSQL 엔진 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **DBA의 판단**: 체크포인트 주기가 너무 짧으면 I/O 부하가 증가하고, 너무 길면 복구 시간(RTO)이 늘어난다. 따라서 서비스의 특성에 따라 '점진적 체크포인트(Fuzzy Checkpoint)'를 설정하여 부하를 분산해야 한다.
- **LSN Gap 모니터링**: 복제(Replication) 환경에서 마스터와 슬레이브 간의 LSN 차이를 모니터링하여 복제 지연(Lag)을 조기에 감지하고 장애에 대비해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
WAL과 LSN 기반의 복구 매커니즘은 ACID를 보장하는 현대 데이터베이스의 근간이다. 클라우드 네이티브 환경(예: Amazon Aurora)에서는 로그 자체를 네트워크를 통해 스토리지 노드로 전송하고, 스토리지 레벨에서 Redo를 수행함으로써 I/O 병목을 해결하는 방향으로 진화하고 있다. 결론적으로 WAL은 안정성과 성능의 균형을 맞추는 최적의 표준이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: ACID Properties, Transaction Recovery
- **연관 기술**: Redo/Undo Logs, ARIES Algorithm, Fuzzy Checkpoint, Steal/No-Force Policy
- **확장 개념**: Log-Structured Merge Tree (LSM), Change Data Capture (CDC)

### 👶 어린이를 위한 3줄 비유 설명
1. 엄마랑 약속을 할 때, 약속 내용을 먼저 일기장(로그)에 적어야 나중에 잊어버려도 다시 기억해낼 수 있어요.
2. 장난감을 정리(체크포인트)하기 전까지는 일기장을 버리면 안 돼요.
3. 일기장에 적힌 번호(LSN)를 보면 어떤 순서로 놀았는지 정확히 알 수 있답니다.
