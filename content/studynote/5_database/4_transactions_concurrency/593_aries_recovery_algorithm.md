+++
weight = 593
title = "593. ARIES 복구 알고리즘 (ARIES Recovery Algorithm)"
date = "2024-03-20"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)
- **현대 DBMS의 표준 복구 프로토콜**: IBM에서 개발한 알고리즘으로, 분석(Analysis), Redo, Undo의 3단계 페이즈를 통해 데이터베이스를 일관된 상태로 복구합니다.
- **Repeating History 원칙**: 장애 발생 시점까지의 모든 작업을 로그를 통해 재현(Redo)하여, 장애 당시 시스템 상태를 완벽하게 복원한 후 미완료 트랜잭션을 취소합니다.
- **LSN 기반 추적**: Log Sequence Number를 사용하여 데이터 페이지와 로그 레코드 간의 정합성을 정밀하게 관리하며, 체크포인트 오버헤드를 최소화합니다.

---

### Ⅰ. 개요 (Context & Background)
대용량 데이터베이스 환경에서 시스템 장애 발생 시, 수천 개의 트랜잭션 중 어떤 것을 살리고(Redo) 어떤 것을 버려야 할지(Undo)를 결정하는 것은 매우 복잡한 문제입니다. **ARIES (Algorithms for Recovery and Isolation Exploiting Semantics)**는 미디어 장애나 시스템 다운 상황에서 데이터의 **영속성(Durability)**을 보장하는 가장 정교하고 성능이 검증된 알고리즘입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
[ ARIES Recovery Process / ARIES 복구 프로세스 ]

  (Log in Stable Storage)
  <--- [T1: Start] --- [T2: Update] --- [Checkpoint] --- [T1: Commit] --- (CRASH!)
                                            |
    +---------------------------------------V-----------------------------------+
    | Phase 1: 분석 (Analysis)                                                  |
    | - 로그 스캔: Dirty Page Table(DPT) 및 Transaction Table(TT) 복구           |
    | - 복구 시작 지점(RedoLSN) 결정                                            |
    +---------------------------------------|-----------------------------------+
                                            V
    +---------------------------------------|-----------------------------------+
    | Phase 2: Redo (Repeating History)     | <--- "장애 시점까지 시간 여행"     |
    | - RedoLSN부터 정방향 스캔하며 모든 변경사항 재반영                        |
    | - 커밋 여부와 상관없이 모든 로그 실행 (History 재현)                       |
    +---------------------------------------|-----------------------------------+
                                            V
    +---------------------------------------|-----------------------------------+
    | Phase 3: Undo (Rollback)              | <--- "미완료 작업만 취소"          |
    | - 역방향 스캔: 커밋되지 않은 트랜잭션의 작업만 취소                       |
    | - CLR(Compensation Log Record) 작성하여 중복 Undo 방지                    |
    +---------------------------------------------------------------------------+
```

1. **LSN (Log Sequence Number)**: 각 로그 레코드에 고유 번호를 부여하고, 데이터 페이지에도 마지막 수정 LSN(pageLSN)을 기록하여 Redo 필요 여부를 즉시 판단합니다.
2. **Analysis 페이즈**: 로그를 분석하여 장애 당시 활성 트랜잭션 목록과 메모리에서 디스크로 아직 쓰이지 않은 Dirty 페이지들을 식별합니다.
3. **Redo 페이즈**: "실패를 두려워하지 않는 복구"를 위해 커밋되지 않은 트랜잭션이라도 일단 Redo를 수행하여 장애 시점의 상태를 그대로 복원합니다.
4. **Undo 페이즈**: Transaction Table을 참조하여 커밋되지 못한 트랜잭션들을 역순으로 롤백합니다. 이때 '보상 로그(CLR)'를 남겨 복구 중 재장애가 발생해도 중복 작업을 피합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | ARIES 알고리즘 | 전통적 지연/즉시 갱신 회복 |
|:---:|:---:|:---:|
| **복구 철학** | Repeating History (역사 재현) | selective Redo/Undo (선택적 복구) |
| **중단 시점** | CLR을 통해 안전한 재복구 가능 | 복구 도중 장애 시 일관성 훼손 위험 |
| **체크포인트** | Fuzzy Checkpoint (비차단형) | 정적 체크포인트 (시스템 일시 중지) |
| **LSN 활용** | 페이지별 LSN 기록으로 정밀 제어 | 대체로 전체 트랜잭션 단위 관리 |
| **주요 특징** | Fine-grained Locking과 병행 가능 | 복구 로직이 단순한 만큼 제약이 많음 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **적용 사례**: **Oracle**, **SQL Server**, **DB2**, **PostgreSQL** 등 대부분의 상용 및 오픈소스 RDBMS는 ARIES의 변형 또는 핵심 메커니즘을 채택하고 있습니다.
- **기술사적 판단**: ARIES의 위대함은 **Fuzzy Checkpointing**에 있습니다. 시스템 운영을 중단하지 않고도 복구에 필요한 정보를 로그에 남길 수 있어 가용성을 극대화합니다. 기술사는 단순 복구뿐 아니라, **WAL (Write Ahead Logging)** 프로토콜과 ARIES의 유기적 결합을 통해 '무결성'과 '성능'의 트레이드오프를 최적화해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
ARIES는 데이터베이스 복구 이론의 정점이자 실무적 표준입니다. 복구 과정 자체를 '로그가 이끄는 상태 기계(State Machine)'로 정의함으로써 데이터 유실 가능성을 0%에 가깝게 수렴시켰습니다. 클라우드 환경의 **분산 DB(Distributed ARIES)**나 **비휘발성 메모리 기반 로깅** 기술이 발전하더라도, 'History를 재현하고 실패한 것만 골라낸다'는 ARIES의 철학은 불변의 표준으로 남을 것입니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 로그 기반 회복 (Log-based Recovery), WAL (Write Ahead Logging)
- **유사 개념**: Fuzzy Checkpoint, CLR (Compensation Log Record), Steal/No-Force Policy
- **하위 기술**: Dirty Page Table (DPT), Transaction Table (TT), LSN (Log Sequence Number)

---

### 👶 어린이를 위한 3줄 비유 설명
- 로봇이 블록 성을 쌓다가 무너졌을 때, 로봇의 작업 일기장을 처음부터 끝까지 다시 읽어요.
- 일단 무너진 곳까지 일기대로 똑같이 다시 쌓아서 성을 만든 다음에,
- 마지막에 실수로 잘못 끼운 블록들만 하나씩 쏙쏙 빼서 원래대로 예쁘게 고치는 거예요.
