+++
title = "CAP 정리 (CAP Theorem)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# CAP 정리 (CAP Theorem)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CAP 정리는 분산 데이터베이스 시스템이 일관성(Consistency), 가용성(Availability), 파티션 감내(Partition Tolerance) 중 동시에 3가지를 모두 만족할 수 없음을 나타내는 이론입니다.
> 2. **가치**: 분산 시스템 설계 시 트레이드오프를 명확히 이해하고, 비즈니스 요구사항에 맞는 두 가지 속성을 선택하도록 돕습니다.
> 3. **융합**: PACELC 정리로 확장되어, 정상 상태에서의 지연-일관성 트레이드오프까지 고려합니다.

---

### Ⅰ. 개요

#### 1. CAP의 3가지 속성
| 속성 | 의미 | 설명 |
|:---|:---|:---|
| **C (Consistency)** | 일관성 | 모든 노드가 동시에 동일한 데이터 반환 |
| **A (Availability)** | 가용성 | 모든 요청이 응답을 받음 |
| **P (Partition Tolerance)** | 파티션 감내 | 네트워크 분할 시에도 시스템 동작 |

#### 2. 트레이드오프
- **CP**: 일관성 + 파티션 감내 (가용성 희생) - MongoDB, HBase
- **AP**: 가용성 + 파티션 감내 (일관성 희생) - Cassandra, DynamoDB
- **CA**: 일관성 + 가용성 (파티션 감내 불가) - 단일 노드 RDBMS

---

### Ⅱ. 시각화

```text
<<< CAP Theorem Triangle >>~

                    C (Consistency)
                   /\
                  /  \
                 /    \
                /      \
               /   ?    \
              /          \
             /____________\
       A (Availability)   P (Partition Tolerance)

[현실]
- P는 네트워크 분할이 불가피하므로 필수
- 실제로는 CP 또는 AP 선택
```

---

### Ⅲ. 실제 적용

| 데이터베이스 | CAP 분류 | 특징 |
|:---|:---|:---|
| **MongoDB** | CP | 강한 일관성, 장애 시 쓰기 불가 |
| **Cassandra** | AP | 높은 가용성, 결과적 일관성 |
| **Redis** | CP | 단일 노드에서 일관성 우선 |
| **DynamoDB** | AP | 가용성 우선, 결과적 일관성 |

---

### Ⅳ. PACELC 확장

```text
CAP의 한계: 장애 상황만 고려
PACELC: 정상 상황도 고려

P (Partition) → A vs C (장애 시)
E (Else) → L (Latency) vs C (정상 시)

예: Cassandra
- 장애 시: A 선택 (가용성)
- 정상 시: L 선택 (낮은 지연)
```

---

### Ⅴ. 결론

CAP 정리는 분산 시스템 설계의 근간이며, 비즈니스 요구사항에 따라 적절한 트레이드오프를 선택해야 합니다.

---

### 관련 개념 맵
- **[NoSQL 데이터베이스](@/studynotes/14_data_engineering/01_data_arch/nosql_databases.md)**
- **[BASE 특성](@/studynotes/14_data_engineering/01_data_arch/base_properties.md)**
- **[분산 시스템](@/studynotes/14_data_engineering/01_data_arch/distributed_systems.md)**

---

### 어린이를 위한 3줄 비유
1. **세 가지 소원**: 요정이 세 가지 소원을 들어주는데, 두 가지만 골라야 해요.
2. **다 고를 수 없어**: 빠르고, 정확하고, 튼튼한 건 하나도 못 골라요. 두 개만!
3. **상황에 따라**: 뭘 고를지는 내가 뭘 더 중요하게 생각하는지에 달렸어요!
