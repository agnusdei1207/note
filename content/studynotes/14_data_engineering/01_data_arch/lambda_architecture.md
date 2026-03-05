+++
title = "람다 아키텍처 (Lambda Architecture)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 람다 아키텍처 (Lambda Architecture)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 람다 아키텍처는 배치 레이어(Batch Layer)와 스피드 레이어(Speed Layer)를 결합하여, 대용량 데이터의 정확한 배치 처리와 실시간 처리를 동시에 제공하는 하이브리드 아키텍처입니다.
> 2. **가치**: 과거 데이터의 정확한 분석과 실시간 데이터의 빠른 처리를 모두 만족하며, 장애 시 배치 레이어로 복구가 가능합니다.
> 3. **융합**: 하둡(배치) + 스톰/스파크 스트리밍(실시간) 조합으로 구현되었으나, 현재는 카파 아키텍처나 레이크하우스로 대체되는 추세입니다.

---

### Ⅰ. 개요

#### 1. 3계층 구조
| 계층 | 역할 | 기술 스택 |
|:---|:---|:---|
| **Batch Layer** | 전체 데이터 저장, 배치 처리 | Hadoop, Spark |
| **Speed Layer** | 실시간 데이터 처리 | Storm, Spark Streaming |
| **Serving Layer** | 쿼리 결과 병합, 응답 | Cassandra, Druid |

#### 2. 핵심 철학
- **Accuracy + Latency**: 정확성과 지연 시간 모두 충족
- **Fault Tolerance**: 스피드 레이어 장애 시 배치 레이어로 복구
- **Immutability**: 원본 데이터 불변 저장

---

### Ⅱ. 아키텍처

```text
<<< Lambda Architecture >>>

                         +----------------+
                         |  Data Source   |
                         +-------+--------+
                                 |
                 +---------------+---------------+
                 |                               |
                 v                               v
        +--------+--------+            +--------+--------+
        |  Batch Layer    |            |  Speed Layer    |
        | - Master Dataset|            | - Real-time     |
        | - Batch Views   |            | - Delta Views   |
        | (Hadoop/Spark)  |            | (Storm/Flink)   |
        +--------+--------+            +--------+--------+
                 |                               |
                 v                               v
        +--------+--------+            +--------+--------+
        |  Batch Views    |            |  Real-time Views|
        +--------+--------+            +--------+--------+
                 |                               |
                 +---------------+---------------+
                                 |
                                 v
                        +--------+--------+
                        |  Serving Layer  |
                        | Query = Batch + RT|
                        +--------+--------+
                                 |
                                 v
                        +--------+--------+
                        |     Query       |
                        +-----------------+
```

---

### Ⅲ. 장단점

**장점**:
- 정확성과 실시간성 동시 충족
- 장애 복구 용이
- 확장성

**단점**:
- 복잡성 (두 개의 코드 베이스)
- 운영 오버헤드
- 데이터 일관성 관리 어려움

---

### Ⅳ. 실무 적용

**Netflix, Twitter, LinkedIn** 등에서 초기에 채택했으나, 현재는 카파 아키텍처나 스트리밍 우선 아키텍처로 전환하는 추세입니다.

---

### Ⅴ. 결론

람다 아키텍처는 빅데이터 실시간 처리의 초기 모델이었으나, 복잡성 문제로 현재는 카파 아키텍처나 레이크하우스로 진화하고 있습니다.

---

### 관련 개념 맵
- **[카파 아키텍처](@/studynotes/14_data_engineering/01_data_arch/kappa_architecture.md)**
- **[Apache Kafka](@/studynotes/14_data_engineering/03_pipelines/apache_kafka.md)**
- **[Apache Spark](@/studynotes/14_data_engineering/01_data_arch/apache_spark.md)**

---

### 어린이를 위한 3줄 비유
1. **두 개의 주방**: 큰 주방에서는 하루 종일 음식을 만들어요. 작은 주방에서는 주문 들어오자마자 바로 만들어요.
2. **합쳐서 서빙**: 손님에게는 두 주방의 음식을 합쳐서 내줘요.
3. **작은 주방이 고장 나도**: 큰 주방이 있으니까 음식은 계속 나와요!
