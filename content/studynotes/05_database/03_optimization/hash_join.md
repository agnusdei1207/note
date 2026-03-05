+++
title = "해시 조인 (Hash Join)"
date = "2026-03-04"
[extra]
categories = "studynotes-05_database"
+++

# 해시 조인 (Hash Join)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 두 테이블 간의 조인 연산을 수행할 때, 작은 테이블(Build Input)을 메모리에 해시 테이블(Hash Table)로 구축한 후, 큰 테이블(Probe Input)을 스캔하며 해시 함수로 매칭을 수행하는 $O(N+M)$ 시간 복잡도의 고성능 조인 알고리즘입니다.
> 2. **가치**: 대용량 데이터 웨어하우스(DW) 환경에서 인덱스 유무와 무관하게 Nested Loop Join 대비 수십~수백 배 빠른 성능을 발휘하며, 동등 조인(Equi-Join) 조건에서 최적의 처리량(Throughput)을 제공합니다.
> 3. **융합**: 메모리 관리(Grace Hash Join, Hybrid Hash Join), 디스크 스파일(Spilling) 처리, 병렬 처리(Parallel Hash Join) 기법과 결합하여 현대 데이터베이스 엔진의 핵심 조인 전략으로 자리 잡았습니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**해시 조인(Hash Join)**은 조인 컬럼의 값을 해시 함수(Hash Function)에 입력하여 해시 버킷(Hash Bucket)에 분배하고, 동일한 버킷 내에서만 실제 값을 비교하여 조인을 수행하는 알고리즘입니다. 1970년대 후반에 제안되었으며, 현대 RDBMS(Oracle, PostgreSQL, SQL Server, MySQL 8.0+)의 비용 기반 옵티마이저(CBO)가 대용량 데이터 조인 시 우선적으로 선택하는 방식입니다.

- **Build Phase (구축 단계)**: 작은 테이블을 읽어 해시 테이블을 메모리에 생성
- **Probe Phase (탐색 단계)**: 큰 테이블을 순차 스캔하며 해시 테이블에서 매칭되는 레코드 검색
- **Equi-Join 전용**: `=` (등호) 조건의 조인에서만 사용 가능 (범위 조인 불가)

#### 2. 💡 비유를 통한 이해
**'도서관에서 책 찾기 vs 사전 만들기'**에 비유할 수 있습니다.

- **Nested Loop Join (이중 루프)**: 학생 A(B 테이블)가 도서관에 와서, 책장의 책 하나하나(Y 테이블)를 꺼내 보며 "이거 내가 찾는 책이야?"라고 물어보는 방식입니다. 책이 1만 권이면 1만 번 확인해야 합니다.

- **Hash Join (해시 조인)**:
  1. **Build Phase**: 먼저 "찾아야 할 책 제목 목록"(작은 테이블)을 받아, 알파벳별(A, B, C...)로 정리된 '색인 카드 박스'(해시 테이블)를 만듭니다.
  2. **Probe Phase**: 도서관 책장을 순서대로 돌며 책을 발견할 때마다, 책 제목의 첫 글자를 보고 해당하는 색인 카드 박스로 가서 "이거 있어?"라고 확인합니다.

  이 방식은 목록(해시 테이블)만 만들어두면, 책장의 책을 한 번씩만 쭉 훑어보면 됩니다!

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계 (NL Join의 Random I/O)**: Nested Loop Join은 외부 테이블의 각 행마다 내부 테이블을 인덱스로 탐색합니다. 내부 테이블이 크고 인덱스가 없으면 Full Scan을 반복해야 하고, 인덱스가 있어도 Random I/O가 발생하여 성능이 급격히 저하되었습니다. 특히 DW(데이터 웨어하우스) 환경의 수억 건 조인에서는 치명적이었습니다.

2. **혁신적 패러다임의 도입 (해시 기반 매칭)**: 해시 조인은 "전체를 한 번에 읽어서 해시 테이블을 만들고, 그 다음 한 번만 스캔하자"는 접근법을 도입했습니다. 이는 Sequential I/O를 극대화하고 Random I/O를 원천 차단합니다.

3. **현대적 요구사항**: 빅데이터 분석, 실시간 리포팅, 머신러닝 파이프라인에서 대규모 Fact-Dimension 테이블 조인이 빈번해지면서, Hash Join은 DW 환경의 표준 조인 방식이 되었습니다. MySQL 8.0.18부터도 Hash Join이 공식 도입되었습니다.

---

### Ⅱ. 아키테처 및 핵심 원리 (Deep Dive)

#### 1. 해시 조인 구성 요소 (표)

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Build Input** | 해시 테이블 생성을 위한 작은 테이블 | 전체 로우를 읽어 Hash Function 적용 후 메모리에 적재 | 작은 테이블 우선 | 색인 카드 |
| **Hash Function** | 키 값을 버킷 번호로 변환 | $bucket = hash(key) \mod N$, 균등 분배 목표 | MurmurHash, xxHash | 분류 기준 |
| **Hash Bucket** | 동일한 해시 값을 가진 엔트리 저장 | Linked List 또는 Open Addressing으로 충돌 처리 | Chain, Probe | 카드 보관함 |
| **Probe Input** | 해시 테이블 탐색을 위한 큰 테이블 | 순차 스캔하며 각 로우의 키로 해시 테이블 조회 | Full Table Scan | 도서관 책장 |
| **Hash Table** | 메모리 상의 조인 매칭 구조 | PGA(Program Global Area) 또는 work_mem에 저장 | In-Memory Structure | 정리된 목록 |
| **Partition** | 메모리 초과 시 디스크 분할 | Grace Hash Join: 해시 값 기준 디스크 파티셔닝 | Spill to Disk | 임시 보관함 |

#### 2. 해시 조인 아키텍처 다이어그램

```text
================================================================================
                     [ Hash Join Algorithm Architecture ]
================================================================================

[ Phase 1: Build Phase - 해시 테이블 구축 ]

    [ Build Input: DEPARTMENT (10 rows) ]           [ Memory: Hash Table ]
    +-------------+-----------+                     +------------------------+
    | dept_id(PK) | dept_name |                     | Bucket 0 | Bucket 1 | ... |
    +-------------+-----------+                     +----------+----------+-----+
    | 10          | Sales     | --hash(10)--> 3 --> |          |          | 3: [10,Sales] |
    | 20          | Marketing| --hash(20)--> 7 --> |          |          | ...          |
    | 30          | Research  | --hash(30)--> 1 --> |          | [30,Res] | 7: [20,Mkt]  |
    | ...         | ...       |                     |          |          |              |
    +-------------+-----------+                     +------------------------+
                                                                 |
    (작은 테이블을 메모리에 해시 테이블로 적재 완료)              |
                                                                 v

[ Phase 2: Probe Phase - 해시 테이블 탐색 ]

    [ Probe Input: EMPLOYEE (1,000,000 rows) ]
    +-------------+-----------+---------+
    | emp_id      | emp_name  | dept_id |
    +-------------+-----------+---------+
    | 1001        | Alice     | 10      | --hash(10)--> 3 --> Bucket 3 탐색
    | 1002        | Bob       | 20      | --hash(20)--> 7 --> Bucket 7 탐색
    | 1003        | Charlie   | 30      | --hash(30)--> 1 --> Bucket 1 탐색
    | ...         | ...       | ...     |       |
    +-------------+-----------+---------+       |
                                                  v
                                    [ Hash Table Lookup ]
                                    Bucket 3에서 dept_id=10 찾음
                                    매칭 성공! -> 결과 반환

    [ 결과 Output ]
    +-------------+-----------+---------+-----------+
    | emp_id      | emp_name  | dept_id | dept_name |
    +-------------+-----------+---------+-----------+
    | 1001        | Alice     | 10      | Sales     |
    | 1002        | Bob       | 20      | Marketing |
    | 1003        | Charlie   | 30      | Research  |
    +-------------+-----------+---------+-----------+

================================================================================
                     [ Grace Hash Join (메모리 초과 시) ]
================================================================================

    [ Build Input이 메모리보다 클 경우 ]

    Step 1: Partition Phase (양쪽 테이블 모두 파티셔닝)
    +------------------+     +------------------+
    | Build Table      |     | Probe Table      |
    +------------------+     +------------------+
            |                         |
            v                         v
    [Partition 0] [Partition 1] ... [Partition N]
        |             |                  |
        +------+------+--------+---------+
               |             |
               v             v
    Step 2: 각 파티션 쌍을 메모리에 올려 Hash Join 수행
    (디스크 I/O는 추가되지만, 여전히 O(N+M) 복잡도 유지)

================================================================================
                     [ 시간 복잡도 분석 ]
================================================================================

    Nested Loop Join:  O(N × M)  -- 외부 × 내부 스캔
    Sort Merge Join:   O(N log N + M log M)  -- 정렬 비용
    Hash Join:         O(N + M)   -- 선형 시간! (메모리 충분 시)

    ※ N = Build Input 크기, M = Probe Input 크기
    ※ Hash Join이 대용량 조인에서 압도적으로 빠른 이유
```

#### 3. 심층 동작 원리: 해시 조인의 3가지 변형

**① In-Memory Hash Join (Classic)**
```
전제조건: Build Input이 메모리에 완전히 적재될 수 있음

1. Build Input의 모든 행을 읽음
2. 각 행의 조인 키에 hash() 적용 -> 버킷 번호 계산
3. 해당 버킷에 행 전체(또는 포인터) 저장
4. Probe Input을 순차 스캔하며 hash() -> 버킷 조회
5. 버킷 내에서 실제 키 값 비교 (해시 충돌 해결)
6. 매칭되면 결과 반환

장점: 가장 빠름 (순수 메모리 연산)
단점: 메모리보다 큰 테이블은 처리 불가
```

**② Grace Hash Join (Partitioned Hash Join)**
```
전제조건: Build Input이 메모리보다 큼

1. Partition Phase:
   - Build Input과 Probe Input을 동일한 해시 함수로 파티셔닝
   - 각 파티션을 디스크에 저장
   - 같은 파티션 번호끼리만 조인하면 됨 (p1.build <-> p1.probe)

2. Join Phase:
   - 각 파티션 쌍을 메모리에 올려 In-Memory Hash Join 수행
   - 결과를 합쳐서 최종 결과 반환

장점: 메모리보다 큰 테이블도 처리 가능
단점: 디스크 I/O 추가로 성능 저하
```

**③ Hybrid Hash Join**
```
Grace Hash Join의 최적화 버전

1. 첫 번째 파티션은 메모리에 유지 (Spill 안 함)
2. 나머지 파티션만 디스크에 Spill
3. Probe Phase에서 첫 번째 파티션은 바로 조인 가능
4. 나머지 파티션은 Grace Hash Join처럼 처리

장점: 자주 조인되는 데이터(첫 파티션)는 빠르게 처리
```

#### 4. 실무 수준의 해시 조인 튜닝 (PostgreSQL / Oracle)

```sql
-- ==================== PostgreSQL 해시 조인 ====================

-- 1. 실행 계획 확인
EXPLAIN (ANALYZE, BUFFERS)
SELECT e.emp_name, d.dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id;

-- 결과 예시:
-- Hash Join  (cost=... rows=... width=...)
--   Hash Cond: (e.dept_id = d.dept_id)
--   ->  Seq Scan on employees e  (Probe Input)
--   ->  Hash  (Build Input)
--         ->  Seq Scan on departments d

-- 2. 해시 조인 강제/비강제
SET enable_hashjoin = on;   -- 해시 조인 활성화 (기본값)
SET enable_hashjoin = off;  -- 해시 조인 비활성화 (다른 조인 유도)

-- 3. work_mem 튜닝 (해시 테이블 메모리 크기)
SET work_mem = '256MB';  -- 세션 레벨 설정
-- work_mem이 클수록 Spill 감소 -> 성능 향상

-- 4. 해시 조인 비용 추정 확인
EXPLAIN (ANALYZE) SELECT ...
-- "Hash Buckets: 65536"  -- 버킷 개수
-- "Hash Batches: 1"      -- 배치 수 (1이면 In-Memory)
-- "Peak Memory Usage: 64kB"  -- 메모리 사용량

-- ==================== Oracle 해시 조인 ====================

-- 1. 해시 조인 힌트
SELECT /*+ HASH(d) */ e.emp_name, d.dept_name
FROM employees e, departments d
WHERE e.dept_id = d.dept_id;
-- d(departments)를 Build Input으로 사용

-- 2. PGA(Private Global Area) 메모리 튜닝
ALTER SYSTEM SET pga_aggregate_target = 4G SCOPE=BOTH;
-- PGA가 클수록 해시 테이블 Spill 감소

-- 3. 해시 조인 스위치
ALTER SESSION SET "_hash_join_enabled" = TRUE;

-- 4. 실행 계획에서 해시 조인 확인
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR);

-- ==================== MySQL 8.0+ 해시 조인 ====================

-- 1. 해시 조인 힌트
SELECT /*+ HASH_JOIN(e, d) */ e.emp_name, d.dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id;

-- 2. 해시 조인 비활성화
SELECT /*+ NO_HASH_JOIN(e, d) */ ...

-- 3. 조인 버퍼 크기 튜닝
SET join_buffer_size = 262144;  -- 256KB
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 조인 알고리즘 심층 비교 (NL vs Sort Merge vs Hash)

| 비교 항목 | Nested Loop Join | Sort Merge Join | Hash Join |
|:---|:---|:---|:---|
| **시간 복잡도** | $O(N \times M)$ | $O(N \log N + M \log M)$ | $O(N + M)$ |
| **메모리 사용** | 최소 | 정렬용 버퍼 | 해시 테이블 (많이 필요) |
| **인덱스 요구** | 내부 테이블에 필수 | 불필요 | 불필요 |
| **조인 조건** | 모든 조건 가능 | 등호 + 범위 가능 | 등호(Equi)만 가능 |
| **최적 시나리오** | 소량 데이터 OLTP | 정렬된 데이터, 범위 조인 | 대용량 DW 분석 |
| **첫 응답 속도** | 즉시 (First Row 빠름) | 정렬 후 (느림) | Build 후 (중간) |
| **총 처리량** | 느림 (대량 시) | 중간 | 가장 빠름 |

#### 2. 과목 융합 관점 분석

- **[메모리 관리 융합] 버퍼 할당 전략**: 해시 조인의 성능은 메모리 크기에 직결됩니다. PostgreSQL의 `work_mem`, Oracle의 `PGA_AGGREGATE_TARGET`은 OS의 가상 메모리 관리와 연동됩니다. 메모리 부족 시 Spill은 OS의 스왑(Swap)이 아닌 DB 엔진이 직접 관리하는 임시 테이블스페이스를 사용합니다.

- **[알고리즘 융합] 해시 함수 선택**: 좋은 해시 함수(MurmurHash, xxHash)는 키 분포가 균등해야 충돌(Collision)이 적습니다. 충돌이 많으면 한 버킷에 데이터가 몰려 성능이 $O(N \times M)$에 가까워집니다. 암호학적 해시(SHA-256)는 느리므로 사용하지 않습니다.

- **[분산 시스템 융합] 병렬 해시 조인**: Spark, Flink, Presto 같은 분산 처리 엔진에서는 파티셔닝 기반 해시 조인을 사용합니다. 각 노드가 독립적으로 로컬 해시 조인을 수행하고 결과를 합칩니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: DW에서 Star Schema 조인 최적화**
- **상황**: Fact 테이블(10억 건)과 Dimension 테이블(10만 건)을 조인하는 쿼리가 있습니다. 현재 Nested Loop Join이 선택되어 30분 이상 소요됩니다.
- **기술사적 결단**:
  1. **Hash Join 강제**: Dimension 테이블을 Build Input으로 하는 Hash Join 힌트 적용
  2. **work_mem 증설**: Dimension 테이블 전체가 메모리에 적재되도록 설정
  3. **통계 정보 갱신**: 옵티마이저가 잘못된 선택을 하지 않도록 최신 통계 확보
  ```sql
  SELECT /*+ HASH_JOIN(d) */ f.*, d.dept_name
  FROM fact_sales f
  JOIN dim_department d ON f.dept_id = d.dept_id;
  ```
  - 결과: 30분 -> 30초로 단축

**시나리오 2: 해시 조인 Spill로 인한 성능 저하**
- **상황**: Build Input이 메모리보다 커서 Grace Hash Join이 동작 중인데, 임시 테이블스페이스 I/O가 병목입니다.
- **기술사적 결단**:
  1. **메모리 증설**: `work_mem` 또는 `pga_aggregate_target` 증가
  2. **임시 테이블스페이스 최적화**: SSD 또는 TempDB 분리
  3. **파티셔닝 전략**: Probe Input도 파티셔닝하여 파티션 간 조인 수행

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **메모리 크기 산정**: Build Input의 예상 크기 < work_mem (또는 PGA)
- [ ] **해시 충돌 모니터링**: 버킷 당 평균 엔트리 수 확인 (너무 많으면 충돌 과다)
- [ ] **동등 조건 확인**: Non-Equi Join (`<`, `>`, `BETWEEN`)은 Hash Join 불가

#### 3. 주의사항 및 안티패턴 (Anti-patterns)

- **잘못된 Build Input 선택**: 큰 테이블을 Build Input으로 선택하면 메모리 부족으로 Spill 발생. 반드시 작은 테이블을 Build Input으로!
- **Non-Equi Join에 Hash Join 사용 시도**: `WHERE a.col > b.col` 조건은 Hash Join 불가. Sort Merge Join 사용 필요.
- **스케일 아웃 시 해시 파티셔닝 일치**: 분산 환경에서 조인 키가 같은 파티션에 없으면 네트워크 셔플 발생.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 영역 | 내용 | 정량적 목표 / 지표 |
|:---|:---|:---|
| **조인 성능** | 대용량 테이블 조인 시간 단축 | Nested Loop 대비 **10~100배 향상** |
| **메모리 효율** | In-Memory Hash Join 시 디스크 I/O 제로 | Logical Reads만 발생 |
| **DW 처리량** | 복잡한 Star Join 쿼리 응답 시간 | 수십 분 -> 수십 초 |

#### 2. 미래 전망 및 진화 방향

- **Adaptive Hash Join**: 런타임에 Build Input의 실제 크기를 확인하여 메모리에 적재할지, 즉시 Spill할지 동적으로 결정하는 적응형 알고리즘이 표준화되고 있습니다.

- **GPU 가속 해시 조인**: GPU의 대규모 병렬 처리 능력을 활용하여 해시 함수 계산과 버킷 탐색을 가속화하는 연구가 진행 중입니다.

- **벡터화된 해시 조인**: CPU의 SIMD(Single Instruction Multiple Data) 명령어를 활용하여 여러 행을 동시에 처리하는 벡터화 기법이 최신 DBMS(ClickHouse, DuckDB)에서 구현되고 있습니다.

#### 3. ※ 참고 표준/가이드

- **Grace Hash Join (DeWitt et al., 1984)**: "Implementation Techniques for Main Memory Database Systems"
- **Hybrid Hash Join (Shapiro, 1986)**: "Join Processing in Database Systems with Large Main Memories"
- **PostgreSQL Hash Join**: src/backend/executor/nodeHashjoin.c

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[옵티마이저](@/studynotes/05_database/03_optimization/query_optimization.md)**: CBO가 해시 조인 선택 여부를 비용 기반으로 결정합니다.
- **[Nested Loop Join](@/studynotes/05_database/03_optimization/query_optimization.md)**: 해시 조인과 대조되는 OLTP 중심의 조인 알고리즘입니다.
- **[버퍼 풀](@/studynotes/05_database/03_optimization/query_optimization.md)**: 해시 테이블은 PGA(프로세스 전용 메모리)에 생성되어 버퍼 풀과 독립적입니다.
- **[해시 테이블](@/studynotes/08_algorithm_stats/03_hashing/_index.md)**: 자료구조 관점에서의 해시 테이블 원리와 충돌 해결 기법입니다.
- **[데이터 웨어하우스](@/studynotes/05_database/04_dw_olap/data_warehouse_olap.md)**: Star Schema 조인에서 해시 조인이 가장 빈번하게 사용됩니다.

---

### 👶 어린이를 위한 3줄 비유 설명

1. **해시 조인**은 두 반의 학생이 짝을 찾는 게임과 같아요! 먼저 1반(작은 테이블) 학생들의 이름을 'ㄱ, ㄴ, ㄷ...' 순서대로 정리된 명부(해시 테이블)를 만들어요.
2. 그 다음 2반(큰 테이블) 학생들이 한 명씩 들어와서, 자신의 이름 첫 글자에 맞는 명부 칸을 확인해서 짝을 찾아요.
3. 이렇게 하면 2반 학생들이 1반 전체를 매번 다 훑어보지 않아도(중첩 루프 X), 명부만 보고 쏙쏙 짝을 찾을 수 있어서 엄청나게 빠르답니다!
