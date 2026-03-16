---
title = "207. 유령 읽기 (Phantom Read) - 사라졌다 나타나는 데이터"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 207
---

# 207. 유령 읽기 (Phantom Read) - 사라졌다 나타나는 데이터

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 유령 읽기(Phantom Read)는 한 트랜잭션 내에서 **동일한 조건의 집합 조회를 두 번 수행했을 때, 다른 트랜잭션의 INSERT로 인해 이전에 없던 행(Row)이 결과에 나타나는 현상**이다.
> 2. **가치**: 단일 행의 수정을 다루는 비반복 읽기(Non-repeatable Read)와 달리 '집합의 변화'를 다루며, 이를 완벽히 차단하기 위해서는 'Serializable' 격리 수준이나 '넥스트 키 락(Next-Key Lock)'이 필요하다.
> 3. **융합**: MVCC(Multi-Version Concurrency Control) 기술이 보편화된 현대 DB(MySQL InnoDB 등)에서는 'Repeatable Read' 레벨에서도 스냅샷을 통해 상당 부분 방어되나, 특정 조건의 락 획득 시 여전히 주의가 필요하다.

---

### Ⅰ. 유령 읽기 (Phantom Read)의 정의

- **정의**: 트랜잭션 T1이 특정 범위의 데이터를 조회한 후, T2가 해당 범위에 새로운 데이터를 삽입(INSERT)하고 커밋했을 때, T1이 다시 조회하면 이전에 없던 새로운 데이터(유령)가 보이는 현상입니다.
- **차이점**: 
    - **Non-repeatable Read**: 기존에 있던 데이터의 **값(Update)**이 변함.
    - **Phantom Read**: 없던 데이터가 **새로 나타나거나 있던 데이터가 사라짐(Insert/Delete)**.

---

### Ⅱ. 유령 읽기 발생 시나리오 (ASCII Flow)

```text
[유령 읽기 (Phantom Read) 발생 사례]

  Time │      Transaction 1 (T1)      │      Transaction 2 (T2)
  ─────┼──────────────────────────────┼──────────────────────────────
   t1  │  SELECT count(*) FROM User   │
       │  WHERE age > 20; (Result: 5) │
   t2  │                              │  INSERT INTO User(name, age)
       │                              │  VALUES ('Bob', 25);
   t3  │                              │  Commit!
   t4  │  SELECT count(*) FROM User   │
       │  WHERE age > 20; (Result: 6) │ ◀──💥 GHOST RECORD!
  ─────┴──────────────────────────────┴──────────────────────────────
  Result: T1 is confused because the number of users changed mid-flight.
```

---

### Ⅲ. 대응 기술 및 아키텍처적 방어

#### 1. Serializable 격리 수준 적용
- 가장 강력한 레벨로, 조회한 범위 전체에 대해 공유 락을 걸어 다른 트랜잭션의 삽입 자체를 막습니다. (성능 저하 심함)

#### 2. 넥스트 키 락 (Next-Key Lock)
- MySQL InnoDB 등에서 사용하는 기술로, 레코드 락(Record Lock)과 간격 락(Gap Lock)을 결합하여 데이터 사이사이의 빈 공간에 새로운 데이터가 들어오지 못하게 막습니다.

#### 3. MVCC 기반 스냅샷 관리
- 트랜잭션 시작 시점의 데이터 상태(버전)를 고정하여, 이후에 삽입된 데이터는 자신의 스냅샷에 포함되지 않도록 필터링합니다.

- **📢 섹션 요약 비유**: 유령 읽기는 **'출석 체크를 다 했는데, 화장실 갔던 학생이 몰래 들어와서 앉아 있는 바람에 다시 세어보니 인원수가 늘어난 상황'**과 같습니다. 이를 막으려면 출석 체크가 끝날 때까지 교실 문을 잠가야(Serializable / Gap Lock) 합니다.

---

### Ⅳ. 개념 맵 및 요약

- **[격리 수준]**: Serializable 단계에서만 완벽히 정의상 차단됨.
- **[간격 락 (Gap Lock)]**: 인덱스 사이의 빈 공간을 보호하는 핵심 기술.
- **[일관성]**: 집합적 연산의 결과가 트랜잭션 내내 변하지 않아야 함.

📢 **마무리 요약**: 유령 읽기는 대규모 통계나 정산 쿼리에서 숫자가 맞지 않는 원인이 됩니다. **격리 수준과 인덱스 설계**를 최적화하여 유령의 출현을 통제해야 합니다.
