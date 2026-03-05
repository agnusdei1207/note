+++
title = "아파치 플링크 (Apache Flink)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 아파치 플링크 (Apache Flink)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 아파치 플링크는 네이티브 스트림 처리 엔진으로, 배치를 스트림의 특수한 경우로 취급하여 진정한 실시간(Real-time) 이벤트 처리와 상태 관리(Stateful Processing)를 제공합니다.
> 2. **가치**: 이벤트 타임(Event Time) 기반 윈도우 처리, 워터마크(Watermark)를 통한 늦은 데이터 처리, Exactly-once 시맨틱으로 정확한 스트림 분석을 보장합니다.
> 3. **융합**: 카프카(Kafka)와 결합하여 실시간 ETL, 이상 탐지, 실시간 대시보드를 구축하며, K8s 기반 클라우드 네이티브 배포가 가능합니다.

---

### Ⅰ. 개요

#### 1. 개념 및 정의
**아파치 플링크(Apache Flink)**는 2014년 오픈소스로 공개된 분산 스트림 처리 프레임워크입니다. 스파크 스트리밍이 마이크로 배치(Micro-batch) 방식인 반면, 플링크는 진정한 이벤트 기반 스트림 처리를 제공합니다.

#### 2. 핵심 특성
- **네이티브 스트리밍**: 이벤트 단위 실시간 처리
- **상태 관리**: Keyed State, Operator State
- **이벤트 타임**: 시간 순서 보장 처리
- **Exactly-once**: 정확히 한 번 처리 보장

---

### Ⅱ. 아키텍처

```text
<<< Apache Flink Architecture >>>

+--------------------------------------------------------------------------+
|                        Flink Cluster                                      |
+--------------------------------------------------------------------------+

+------------------+                      +------------------+
| JobManager       |  (Master)            | Client           |
| - Dispatcher     |                      | (Job Submit)     |
| - ResourceManager|                      +------------------+
| - JobMaster      |
+--------+---------+
         |
    +----+----+----+----+
    |    |    |    |    |
    v    v    v    v    v
+-------+ +-------+ +-------+
| TM 1  | | TM 2  | | TM 3  |
| Task  | | Task  | | Task  |
| Manager| | Manager| | Manager|
+---+---+ +---+---+ +---+---+
    |         |         |
+---+---+ +---+---+ +---+---+
|Slot 1 | |Slot 1 | |Slot 1 |
|Slot 2 | |Slot 2 | |Slot 2 |
+-------+ +-------+ +-------+

[State Backend]
- MemoryStateStore (개발용)
- FsStateStore (생산용)
- RocksDBStateStore (대용량)
```

---

### Ⅲ. 핵심 개념

#### 1. 윈도우 처리
```java
// 이벤트 타임 윈도우 예시
DataStream<Event> events = ...;

events
    .keyBy(event -> event.getUserId())
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new CountAggregate())
    .addSink(...);
```

#### 2. 워터마크
```text
이벤트: e1(t=1), e2(t=3), e3(t=2), e4(t=5)
워터마크: t=3 (t=3 이전 이벤트는 모두 도착했다고 가정)

[처리 순서]
1. e1(t=1) 도착 → 처리
2. e2(t=3) 도착 → 워터마크 t=3 발행 → 윈도우 [0,3] 트리거
3. e3(t=2) 도착 → 늦은 데이터 (워터마크 t=3 초과) → Side Output 또는 무시
4. e4(t=5) 도착 → 처리
```

---

### Ⅳ. 실무 적용

```java
// 카프카 소스 → 처리 → 카프카 싱크
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// 카프카 소스
KafkaSource<String> source = KafkaSource.<String>builder()
    .setBootstrapServers("kafka:9092")
    .setTopics("input-topic")
    .setGroupId("flink-consumer")
    .setStartingOffsets(OffsetsInitializer.earliest())
    .build();

DataStream<String> stream = env.fromSource(source, WatermarkStrategy.noWatermarks(), "Kafka Source");

// 처리
DataStream<Result> processed = stream
    .map(new ParseFunction())
    .keyBy(event -> event.getUserId())
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new CountAggregate());

// 카프카 싱크
KafkaSink<Result> sink = KafkaSink.<Result>builder()
    .setBootstrapServers("kafka:9092")
    .setRecordSerializer(new ResultSerializer("output-topic"))
    .build();

processed.sinkTo(sink);

env.execute("Real-time Processing");
```

---

### Ⅴ. Flink vs Spark Streaming

| 비교 | Flink | Spark Streaming |
|:---|:---|:---|
| **처리 방식** | 네이티브 스트리밍 | 마이크로 배치 |
| **지연 시간** | ms | 초 단위 |
| **이벤트 타임** | 완벽 지원 | 제한적 |
| **상태 관리** | 강력 | 제한적 |

---

### Ⅴ. 결론

플링크는 진정한 실시간 처리가 필요한 경우 최적의 선택이며, 카프카와 결합하여 실시간 데이터 파이프라인의 핵심 엔진으로 활용됩니다.

---

### 관련 개념 맵
- **[Apache Kafka](@/studynotes/14_data_engineering/03_pipelines/apache_kafka.md)**
- **[스트림 처리](@/studynotes/14_data_engineering/03_pipelines/stream_processing.md)**
- **[Apache Spark](@/studynotes/14_data_engineering/01_data_arch/apache_spark.md)**

---

### 어린이를 위한 3줄 비유
1. **실시간 주문**: 햄버거 가게에서 주문이 들어오자마자 바로 만들어요. 모아서 안 만들어요.
2. **순서대로 처리**: 주문이 늦게 와도 주문 시간 순서대로 만들어요.
3. **기억력 좋아요**: 어떤 손님이 무엇을 주문했는지 기억해서, 추가 주문할 때 알아들어요!
