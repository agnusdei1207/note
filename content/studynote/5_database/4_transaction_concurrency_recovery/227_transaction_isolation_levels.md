---
title = "227. 트랜잭션 고립화 수준 (Isolation Level) - 정합성과 성능의 저울질"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 227
---

# 227. 트랜잭션 고립화 수준 (Isolation Level) - 정합성과 성능의 저울질

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트랜잭션 격리 수준(Isolation Level)은 동시에 실행되는 여러 트랜잭션이 서로의 데이터를 얼마나 볼 수 있는지, 즉 **'데이터의 일관성'과 '시스템의 병렬성' 사이의 타협점**을 정의한 표준 설정이다.
> 2. **가치**: ANSI/ISO SQL 표준 4단계(Read Uncommitted ~ Serializable)를 통해, 비즈니스 요건에 맞춰 오손 읽기(Dirty Read), 유령 읽기(Phantom Read) 등 동시성 이상 현상을 선택적으로 제어한다.
> 3. **융합**: 격리 수준은 단순한 설정값이 아니라 DB 스토리지 엔진의 락킹(Locking) 범위와 MVCC 스냅샷 생성 시점을 결정짓는 아키텍처의 설계 기준이다.

---

### Ⅰ. 격리 수준의 필요성

- **트레이드오프**: 격리를 완벽하게 하면(Serializable) 데이터는 100% 안전하지만 아무도 동시에 일을 못 합니다. 격리를 풀면(Read Uncommitted) 엄청 빠르지만 데이터가 엉망이 됩니다. 이 중간의 적절한 균형을 찾는 것이 엔지니어의 핵심 역량입니다.

---

### Ⅱ. 격리 수준별 이상 현상 발생 여부 (ASCII Matrix)

| 격리 수준 | Dirty Read | Non-Repeatable Read | Phantom Read |
|:---|:---:|:---:|:---:|
| **Read Uncommitted** | **O** (발생) | O | O |
| **Read Committed** | X | **O** | O |
| **Repeatable Read** | X | X | **O** |
| **Serializable** | X | X | X |

```text
[격리 수준과 성능의 관계]

  Level 3: Serializable (정합성 최상 / 성능 최악) ─────┐
  Level 2: Repeatable Read                           │
  Level 1: Read Committed                            │ (격리 강도 강화 방향)
  Level 0: Read Uncommitted (정합성 최악 / 성능 최상) ──┘
```

---

### Ⅲ. 단계별 특징 요약

1. **Read Uncommitted**: 커밋 안 된 데이터도 읽음. 정확도가 전혀 필요 없는 로그성 데이터 처리에나 쓰임.
2. **Read Committed**: 커밋된 것만 읽음. 현대 기업용 DB(Oracle 등)의 가장 일반적인 기본값.
3. **Repeatable Read**: 트랜잭션 시작 시점의 데이터를 계속 보여줌. MySQL(InnoDB)의 기본값.
4. **Serializable**: 읽기 작업도 락을 걸어버림. 금융 거래 등 극강의 안전이 필요한 곳에만 제한적 사용.

- **📢 섹션 요약 비유**: 격리 수준은 **'옆 사람과의 대화 차단 수준'**과 같습니다. 뻥 뚫린 광장(Level 0)에서 일할지, 칸막이 책상(Level 1)에서 일할지, 아예 방 문을 잠그고 혼자 들어갈지(Level 3)를 업무의 중요도에 따라 결정하는 것입니다.

---

### Ⅳ. 개념 맵 및 요약

- **[Dirty Read]**: 남의 실패한 작업을 내 것처럼 믿는 실수.
- **[MVCC]**: 높은 격리 수준에서도 성능을 유지하게 돕는 마법.
- **[S-Lock / X-Lock]**: 격리 수준을 물리적으로 구현하는 열쇠.

📢 **마무리 요약**: **Isolation Level**은 데이터베이스 튜닝의 핵심 지표입니다. 무조건 높은 수준을 고집하기보다, 서비스 성격에 맞는 **최적의 격리 단계**를 선정하는 혜안이 필요합니다.
