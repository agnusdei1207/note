+++
title = "Apache Flink (아파치 플링크)"
categories = ["studynotes-16_bigdata"]
+++

# Apache Flink (아파치 플링크)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Flink는 **네이티브 스트리밍(Native Streaming)** 방식의 분산 데이터 처리 엔진으로, 이벤트 시간(Event Time) 기반 처리, 상태 관리(State Management), 정확히 한 번(Exactly-Once) 처리 보장을 통해 실시간 분석의 새로운 표준을 제시합니다.
> 2. **가치**: Flink는 Spark의 마이크로배치 방식과 달리 **진정한 실시간(ms 단위)** 처리를 제공하며, 유한한 상태 머신(State Machine) 기반으로 무한한 스트림을 처리하는 **상태 기반 스트리밍(Stateful Streaming)** 아키텍처를 구현합니다.
> 3. **융합**: Kafka(Kinesis)와 결합하여 실시간 ETL, CEP(Complex Event Processing), 실시간 머신러닝 추론, IoT 데이터 파이프라인 등 **Mission-critical 스트리밍 애플리케이션**의 핵심 엔진으로 활용됩니다.

---

## Ⅰ. 개요 (Context & Background)

Apache Flink는 2015년 Apache 최상위 프로젝트가 된 이후, 실시간 데이터 처리 분야에서 가장 빠르게 성장하는 오픈소스입니다. Flink의 핵심 철학은 **"스트림은 스트림이다(Streams are streams)"**입니다. 배치 처리는 스트림 처리의 특수한 경우(유한한 스트림)로 간주하며, 이를 통해 **단일 API로 배치와 스트리밍을 통합**합니다.

**💡 비유: 절대 멈추지 않는 컨베이어 벨트 공장**
Flink는 **24시간 가동되는 컨베이어 벨트 공장**에 비유할 수 있습니다. 부품(이벤트)이 컨베이어 벨트 위를 끊임없이 흘러갑니다. 작업자(Flink Task)는 부품이 지나가는 즉시 조립(처리)합니다. 특징은 작업자가 **메모장(State)**을 가지고 있어서, 이전에 처리한 부품 정보를 기억하고 현재 부품과 함께 사용할 수 있다는 점입니다. 만약 공장이 잠시 멈추면, 체크포인트(Checkpoint)를 통해 메모장 내용을 저장해 두었다가 다시 시작할 때 복원합니다.

**등장 배경 및 발전 과정:**
1. **기존 기술의 치명적 한계점**: Spark Streaming의 마이크로배치 방식은 최소 100ms~수 초의 지연이 발생하며, 이벤트 시간 처리와 상태 관리가 복잡했습니다. Storm은 낮은 지연은 가능하지만 Exactly-Once 보장이 어려웠습니다.
2. **혁신적 패러다임 변화 (Native Streaming + Stateful)**: Flink는 각 이벤트를 독립적으로 처리하면서도 **상태(State)**를 관리하여 복잡한 연산(윈도우, 조인, 집계)을 가능하게 했습니다. 또한 **체크포인트 기반 장애 복구**로 Exactly-Once Semantics를 달성했습니다.
3. **비즈니스적 요구사항**: 금융 사기 탐지, 실시간 추천, IoT 이상 감지 등 **밀리초 단위의 응답**이 필요한 Use Case가 증가하면서 Flink의 필요성이 커졌습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Flink 핵심 구성 요소

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|---|---|---|---|---|
| **JobManager** | 작업 조정 및 메타데이터 관리 | 잡 그래프 실행, 체크포인트 코디네이션, 장애 복구 | Dispatcher, ResourceManager | 공장 관리자 |
| **TaskManager** | 실제 태스크 실행 | 슬롯 기반 자원 격리, 상태 저장, 네트워크 버퍼 관리 | TaskSlot, Network Stack | 작업자 |
| **State Backend** | 상태 저장소 | RocksDB(디스크), HashMapStateBackend(메모리) | Incremental Checkpoint | 메모장 |
| **Checkpoint** | 장애 복구를 위한 상태 스냅샷 | Async Barrier Snapshotting, Chandy-Lamport 변형 | Savepoint, Snapshot | 백업 파일 |
| **Window** | 이벤트 그룹화 단위 | Tumbling, Sliding, Session, Global 윈도우 | Event Time, Processing Time | 조립 단위 |
| **Watermark** | 이벤트 시간 진행 표시자 | 지연 이벤트 허용 임계값, Late Data 처리 | Allowed Lateness | 시계 |

### 정교한 구조 다이어그램 (ASCII Art)

```text
========================================================================================================
                              [ APACHE FLINK CLUSTER ARCHITECTURE ]
========================================================================================================

  [ CLIENT ]                           [ FLINK CLUSTER ]                      [ EXTERNAL SYSTEMS ]

  +-------------+                 +-----------------------------------+       +-------------+
  | Job Submit  |                 |         JobManager                |       | Kafka       |
  | (JAR/SQL)   |---------------->|  +-----------+  +--------------+  |       | (Source)    |
  +-------------+                 |  | Dispatcher|  | Resource Mgr |  |       +-------------+
                                  |  +-----------+  +--------------+  |             |
                                  |         |            |            |             v
                                  |  +------▼------------▼-------+    |       +-------------+
                                  |  |     JobMaster (per Job)   |<---|-------| Kinesis     |
                                  |  |  - Execution Graph        |    |       | (Source)    |
                                  |  |  - Checkpoint Coordinator|    |       +-------------+
                                  |  +---------------------------+    |
                                  +-----------------------------------+
                                             |
                           +-----------------+-----------------+
                           |                 |                 |
                    +------▼------+   +------▼------+   +------▼------+
                    | TaskManager |   | TaskManager |   | TaskManager |
                    |  [Slot 1]   |   |  [Slot 1]   |   |  [Slot 1]   |
                    |  [Slot 2]   |   |  [Slot 2]   |   |  [Slot 2]   |
                    |  [Slot 3]   |   |  [Slot 3]   |   |  [Slot 3]   |
                    |  [Slot 4]   |   |  [Slot 4]   |   |  [Slot 4]   |
                    |             |   |             |   |             |
                    | [State:     |   | [State:     |   | [State:     |
                    |  RocksDB]   |   |  RocksDB]   |   |  RocksDB]   |
                    +------+------+   +------+------+   +-------------+
                           |                 |                 |
                           +-----------------+-----------------+
                                             |
                                      +------▼------+
                                      | Kafka       |
                                      | (Sink)      |
                                      +-------------+

========================================================================================================
                              [ EVENT TIME & WATERMARK FLOW ]
========================================================================================================

  Time Progression: --------------------------------------------------------->

  Events:     E1(t=1)  E2(t=2)    E3(t=5)    E4(t=3)    E5(t=7)    E6(t=4)    E7(t=9)
              |        |          |          |          |          |          |
              ▼        ▼          ▼          ▼          ▼          ▼          ▼
  Stream: ────●────────●──────────●──────────●──────────●──────────●──────────●────────>

  Watermark:  W(2)                W(5)                  W(7)                  W(9)
              |                   |                     |                     |
              ▼                   ▼                     ▼                     ▼
           ────▽──────────────────▽─────────────────────▽─────────────────────▽────────>

  Window [0-5]: Triggers when W(5) arrives
    - Includes: E1, E2, E3, E4 (E4 is late but still included if within allowed lateness)
    - Late: E6 (t=4) arrives after W(5), handled as late data

========================================================================================================
                              [ CHECKPOINT BARRIER PROPAGATION ]
========================================================================================================

  JobManager: Checkpoint Request (CID=100)
                     |
                     v Barrier
  Source ────────────|───────────────────────────────────────────────────────>
                     |
  Operator A ────────|──[Process]──[Save State]────────────────────────────>
                     |
  Operator B ────────|──[Process]──[Save State]──(Ack to JobManager)───────>
                     |
  Sink ──────────────|──[Commit]──(Ack to JobManager)──────────────────────>

  Checkpoint Complete: All operators acknowledged → Snapshot is consistent

========================================================================================================
```

### 심층 동작 원리: 상태 기반 스트리밍과 체크포인트

**1. Flink 상태 관리 (State Management)**
```java
// Flink Java API: 상태 기반 스트리밍 처리
public class FraudDetector extends KeyedProcessFunction<String, Transaction, Alert> {

    // 상태 정의: 일정 시간 내 소액 거래 횟수 추적
    private transient MapState<String, Integer> smallTransactionCount;

    @Override
    public void open(Configuration parameters) {
        // 상태 초기화 (RocksDB에 저장됨)
        MapStateDescriptor<String, Integer> descriptor =
            new MapStateDescriptor<>(
                "small-transactions",
                String.class,
                Integer.class
            );
        smallTransactionCount = getRuntimeContext().getMapState(descriptor);
    }

    @Override
    public void processElement(
        Transaction transaction,
        Context context,
        Collector<Alert> collector
    ) throws Exception {

        // 상태 읽기
        String cardId = transaction.getCardId();
        Integer count = smallTransactionCount.get(cardId);
        if (count == null) count = 0;

        // 비즈니스 로직: 소액 거래가 10회 이상이면 사기 의심
        if (transaction.getAmount() < 1.0) {
            count++;
            smallTransactionCount.put(cardId, count);

            if (count >= 10) {
                collector.collect(new Alert(cardId, "Potential fraud detected"));
                smallTransactionCount.remove(cardId);
            }
        } else {
            // 큰 금액 거래 시 카운터 리셋
            smallTransactionCount.remove(cardId);
        }

        // 이벤트 타임 타이머 등록
        context.timerService().registerEventTimeTimer(
            transaction.getTimestamp() + 60000  // 1분 후 타이머
        );
    }

    @Override
    public void onTimer(long timestamp, OnTimerContext ctx, Collector<Alert> out) {
        // 타이머 만료 시 상태 정리
        smallTransactionCount.clear();
    }
}
```

**2. Exactly-Once Semantics를 위한 체크포인트**
```python
# Flink 체크포인트 설정 (Python PyFlink)
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.checkpoint_config import CheckpointingMode

env = StreamExecutionEnvironment.get_execution_environment()

# 체크포인트 활성화 (60초 간격)
env.enable_checkpointing(60000)

# 체크포인트 설정
checkpoint_config = env.get_checkpoint_config()
checkpoint_config.set_checkpointing_mode(CheckpointingMode.EXACTLY_ONCE)
checkpoint_config.set_checkpoint_timeout(600000)  # 10분 타임아웃
checkpoint_config.set_min_pause_between_checkpoints(30000)  # 체크포인트 간 최소 30초
checkpoint_config.set_max_concurrent_checkpoints(1)  # 동시 체크포인트 1개
checkpoint_config.enable_externalized_checkpoints(True)  # 외부 체크포인트 활성화

# 상태 백엔드 설정 (RocksDB)
from pyflink.datastream import RocksDBStateBackend
env.set_state_backend(RocksDBStateBackend("file:///tmp/flink/checkpoints", True))

# Kafka Source 설정 (체크포인트와 연동)
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.datastream.formats.json import JsonRowDeserializationSchema

kafka_source = FlinkKafkaConsumer(
    topics="transactions",
    deserialization_schema=JsonRowDeserializationSchema(),
    properties={
        "bootstrap.servers": "kafka:9092",
        "group.id": "fraud-detector"
    },
    start_from_latest=True
)

# 체크포인트에서 오프셋 커밋
kafka_source.set_commit_offsets_on_checkpoints(True)
```

**3. 윈도우 연산 (Event Time 기반)**
```java
// Flink DataStream API: 이벤트 타임 윈도우
DataStream<Event> events = env
    .addSource(new FlinkKafkaConsumer<>("events", new EventDeserializer(), properties))
    .assignTimestampsAndWatermarks(
        WatermarkStrategy
            .<Event>forBoundedOutOfOrderness(Duration.ofSeconds(5))  // 5초 허용
            .withTimestampAssigner((event, timestamp) -> event.getTimestamp())
    );

// 텀블링 윈도우 (5분)
events
    .keyBy(event -> event.getUserId())
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new CountAggregate())
    .addSink(new FlinkKafkaProducer<>("results", new ResultSerializer(), producerConfig));

// 세션 윈도우 (30분 비활동 시 종료)
events
    .keyBy(event -> event.getSessionId())
    .window(EventTimeSessionWindows.withGap(Time.minutes(30)))
    .process(new SessionProcessWindowFunction())
    .addSink(...);
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Flink vs Spark Streaming vs Kafka Streams

| 비교 지표 | Apache Flink | Spark Streaming | Kafka Streams |
|---|---|---|---|
| **처리 모델** | Native Streaming (이벤트 단위) | Micro-batch (배치 단위) | Native Streaming |
| **지연 시간** | 1~10ms | 100ms~수 초 | 1~10ms |
| **이벤트 시간** | 완벽 지원 (Watermark) | 지원하나 제한적 | 지원 |
| **상태 관리** | RocksDB + Incremental Checkpoint | RDD Cache | RocksDB |
| **Exactly-Once** | 완벽 지원 (Checkpoint + 2PC) | 지원하나 제한적 | 지원 (Transaction) |
| **배치 처리** | 지원 (Stream의 특수 케이스) | 기본 모델 | 미지원 |
| **배포 모델** | 전용 클러스터 | YARN/K8s/Mesos | 애플리케이션 내장 |
| **학습 곡선** | 높음 (DataStream API) | 낮음 (SQL/DataFrame) | 중간 |
| **운영 복잡도** | 높음 (JobManager HA) | 중간 | 낮음 |

### 과목 융합 관점 분석

- **[운영체제 + Flink]**: Flink의 상태 관리는 **메모리 매핑(mmap)**을 활용하는 RocksDB에 의존합니다. 대규모 상태(TB 단위)를 디스크로 스풀링하면서도 성능을 유지하기 위해 OS의 페이지 캐시와 Flink의 자체 버퍼 관리가 상호작용합니다.

- **[네트워크 + Flink]**: Flink는 **Asynchronous Barrier Snapshotting(ABS)** 알고리즘을 사용하여 체크포인트를 수행합니다. 이는 네트워크를 통해 장벽(Barrier)을 전파하고, 모든 태스크가 동기화된 상태에서 스냅샷을 찍는 방식입니다.

- **[데이터베이스 + Flink]**: Flink의 **상태(State)**는 일종의 인메모리 데이터베이스입니다. Keyed State, Operator State, Broadcast State 등 다양한 상태 유형을 지원하며, 체크포인트를 통해 **ACID 속성**을 보장합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 실시간 사기 탐지 시스템**
- **문제**: 신용카드 거래의 사기 패턴을 밀리초 내에 탐지하여 거래 차단 필요
- **전략적 의사결정**:
  1. **이벤트 시간 기반 윈도우**: 거래 시간 기준으로 정확한 시간 윈도우 집계
  2. **상태 기반 규칙 엔진**: 고객별 과거 거래 패턴을 상태로 저장하여 실시간 비교
  3. **CEP(Complex Event Processing)**: "소액 10회 후 고액 1회"와 같은 복합 패턴 탐지
  4. **지연 이벤트 처리**: Watermark + Side Output으로 늦게 도착한 이벤트 처리

**시나리오 2: 실시간 데이터 웨어하우스 동기화**
- **문제**: 운영 DB의 변경 사항을 실시간으로 데이터 웨어하우스에 반영
- **전략적 의사결정**:
  1. **CDC(Change Data Capture)**: Debezium으로 DB 로그를 Kafka로 전송
  2. **Flink SQL CDC**: CREATE TABLE ... WITH ('connector' = 'kafka')로 간편한 동기화
  3. **Upsert 모드**: Primary Key 기반으로 중복 제거 및 최신 상태 유지
  4. **Schema Evolution**: Avro Schema Registry로 스키마 변경 관리

**시나리오 3: 대규모 Flink 클러스터 운영**
- **문제**: 100개 이상의 Flink Job을 운영하며 리소스 효율성과 격리성 확보 필요
- **전략적 의사결정**:
  1. **Session Cluster vs Per-Job Cluster**: 고립성 중시 → Per-Job, 효율성 중시 → Session
  2. **Resource Profile**: CPU/메모리 intensive 작업에 다른 슬롯 프로필 할당
  3. **Application Mode**: Main() 메서드를 클러스터에서 실행하여 네트워크 오버헤드 감소

### 주의사항 및 안티패턴 (Anti-patterns)

- **안티패턴 - 과도한 상태 크기**: 상태가 너무 커지면 체크포인트 시간이 길어져 전체 성능 저하. **TTL(Time-To-Live)** 설정으로 상태 크기 관리 필요

- **안티패턴 - 잘못된 Watermark 설정**: Watermark가 너무 느리면 윈도우가 늦게 트리거, 너무 빠르면 지연 이벤트 손실. **BoundedOutOfOrderness**를 데이터 특성에 맞게 튜닝

- **안티패턴 - Backpressure 무시**: downstream 처리가 느려지면 upstream으로 전파. **네트워크 버퍼**와 **체크포인트 시간** 모니터링 필수

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | 내용 및 지표 |
|---|---|
| **정성적 효과** | - 진정한 실시간(ms 단위) 데이터 처리<br>- 이벤트 시간 기반 정확한 분석<br>- 상태 기반 복잡한 스트리밍 로직 구현 |
| **정량적 효과** | - 처리 지연 시간 **99% 단축** (Spark 대비)<br>- 이벤트 처리 정확도 **99.99%** (Exactly-Once)<br>- 장애 복구 시간 **초 단위** (Savepoint) |

### 미래 전망 및 진화 방향

- **Flink SQL & Table API**: SQL만으로 스트리밍 처리 가능, 진입 장벽 낮춤
- **Flink ML**: 실시간 머신러닝 추론 및 온라인 학습 지원
- **Flink Stateful Functions**: Serverless + Stateful의 결합, 이벤트 기반 마이크로서비스

**※ 참고 표준/가이드**:
- **Apache Flink Documentation**: 공식 문서 및 Best Practices
- **Flink Forward Conference**: 연례 컨퍼런스 발표 자료

---

## 📌 관련 개념 맵 (Knowledge Graph)

- `[Apache Kafka](@/studynotes/16_bigdata/03_streaming/apache_kafka.md)`: Flink의 주요 데이터 소스/싱크
- `[Spark Streaming](@/studynotes/16_bigdata/01_processing/apache_spark.md)`: Flink의 주요 경쟁 기술
- `[Window Operations](@/studynotes/16_bigdata/03_streaming/window_operations.md)`: 스트리밍 데이터 그룹화 기법
- `[Exactly-Once Semantics](@/studynotes/16_bigdata/03_streaming/exactly_once.md)`: 데이터 처리 신뢰성 보장
- `[CEP (Complex Event Processing)](@/studynotes/16_bigdata/03_streaming/cep.md)**: Flink의 이벤트 패턴 매칭

---

## 👶 어린이를 위한 3줄 비유 설명

1. **Flink가 뭔가요?**: 레스토랑에서 주문이 들어올 때마다 바로 요리해서 내놓는 **"실시간 주방"** 같아요. 미리 만들어두는 게 아니라 주문하는 즉시 요리해요!
2. **특별한 게 뭔가요?**: 요리사가 **"기억장부"**를 가지고 있어서, 어떤 손님이 무슨 요리를 시켰는지 기억하고 있어요. 그래서 "이 손님은 매운 거 안 드셨지?" 하고 알 수 있어요.
3. **왜 중요한가요?**: 은행에서 나쁜 사람이 돈을 훔치려고 할 때 **즉시** 알아채서 막을 수 있어요. 1분만 늦어도 이미 돈이 사라진 후니까요!
