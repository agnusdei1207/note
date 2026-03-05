+++
title = "Apache Kafka (아파치 카프카)"
categories = ["studynotes-16_bigdata"]
+++

# Apache Kafka (아파치 카프카)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Kafka는 LinkedIn에서 개발된 **분산형 스트리밍 플랫폼**으로, 높은 처리량(초당 수백만 메시지), 낮은 지연 시간(ms 단위), 강력한 내구성(디스크 기반 저장)을 갖춘 이벤트 스트리밍 아키텍처의 핵심 인프라입니다.
> 2. **가치**: 마이크로서비스 간 비동기 통신, 실시간 데이터 파이프라인, 이벤트 소싱(Event Sourcing) 아키텍처를 가능하게 하며, 기존 메시지 큐(JMS, RabbitMQ) 대비 **10~100배 높은 처리량**을 제공합니다.
> 3. **융합**: Kafka Connect(Sink/Source Connector), Kafka Streams(스트림 처리), ksqlDB(SQL 기반 스트리밍), Schema Registry와 결합하여 **Event-Driven Architecture(EDA)**의 완전한 생태계를 구성합니다.

---

## Ⅰ. 개요 (Context & Background)

Apache Kafka는 2011년 LinkedIn에서 오픈소스로 공개된 후, 2024년 현재 전 세계 **포춘 100대 기업의 80% 이상**이 사용하는 이벤트 스트리밍의 사실상 표준(De facto Standard)입니다. Kafka는 단순한 메시지 큐가 아니라, **"분산 커밋 로그(Distributed Commit Log)"**라는 혁신적인 추상화를 도입하여 메시지의 순서 보장, 내구성, 재생 가능성(Replayability)을 모두 달성했습니다.

**💡 비유: 초고속 우편 분류 센터**
Kafka는 **전 세계 규모의 초고속 우편 분류 센터**에 비유할 수 있습니다. 보내는 사람(Producer)이 우편물(Message)을 센터(Topic/Partition)에 넣으면, 센터는 우편물을 분류대(Partition)에 순서대로 쌓아둡니다. 받는 사람(Consumer)은 자신이 원하는 분류대에서 순서대로 우편물을 가져갑니다. 특징은 우편물을 가져갔다고 사라지는 것이 아니라, **일정 기간(7일~무제한) 보관**되어 언제든 다시 읽을 수 있다는 점입니다. 또한, 분류대가 여러 개여서 여러 받는 사람이 동시에 작업할 수 있어 처리 속도가 매우 빠릅니다.

**등장 배경 및 발전 과정:**
1. **기존 기술의 치명적 한계점**: LinkedIn은 2010년대 초 모든 데이터 파이프라인을 개별 시스템(ETL, 메시지 큐, 로그 수집기)으로 구축했습니다. 이는 **데이터 복잡성 증가**, **지연 시간 누적**, **데이터 일관성 문제**를 야기했습니다.
2. **혁신적 패러다임 변화 (Log-based Architecture)**: Kafka는 모든 데이터를 **"이벤트 스트림"**으로 통합하고, 이를 **분산 로그(Distributed Log)**로 저장하는 새로운 아키텍처를 제안했습니다. 이는 메시지 큐의 실시간성과 데이터 웨어하우스의 내구성을 동시에 달성했습니다.
3. **비즈니스적 요구사항**: 실시간 추천, 사기 탐지, 모니터링, 로그 분석 등 다양한 용도로 동일한 데이터를 **여러 소비자가 구독(Pub/Sub)**하여 사용해야 하는 요구가 폭발적으로 증가했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Kafka 핵심 구성 요소

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|---|---|---|---|---|
| **Producer** | 메시지 생산 및 전송 | 배치 전송, 압축(Snappy/GZIP), 파티셔닝 전략 | Partitioner, Serializer | 우편 보내는 사람 |
| **Broker** | 메시지 저장 및 전달 | 페이지 캐시 활용, Zero-copy 전송, 로그 세그먼트 관리 | Log Segment, Index File | 분류 센터 직원 |
| **Topic** | 메시지 분류 단위 | 논리적 채널, 다중 파티션으로 확장 | Replication Factor | 우편함 카테고리 |
| **Partition** | 병렬 처리 단위 | 순서 보장, 오프셋 기반 위치 관리 | ISR(In-Sync Replicas) | 분류대 한 줄 |
| **Consumer** | 메시지 소비 및 처리 | Consumer Group, 오프셋 커밋, 리밸런싱 | Offset, Heartbeat | 우편 받는 사람 |
| **ZooKeeper/KRaft** | 클러스터 코디네이션 | 리더 선출, 메타데이터 관리, 컨트롤러 | ZAB/Raft Protocol | 센터 관리 시스템 |

### 정교한 구조 다이어그램 (ASCII Art)

```text
========================================================================================================
                              [ APACHE KAFKA CLUSTER ARCHITECTURE ]
========================================================================================================

  [ PRODUCERS ]                        [ KAFKA CLUSTER ]                      [ CONSUMERS ]

  +-------------+                 +-----------------------------------+       +-------------+
  | Web App     |                 |  TOPIC: user_events (Partitions)  |       | Analytics   |
  | (P1)        |--(Produce)----->|  +----+  +----+  +----+  +----+  |-----> | Service (C1)|
  +-------------+                 |  | P0 |  | P1 |  | P2 |  | P3 |  |       +-------------+
                                  |  +----+  +----+  +----+  +----+  |
  +-------------+                 |    ▲        ▲        ▲        ▲   |       +-------------+
  | Mobile App  |                 |    |        |        |        |   |-----> | ML Pipeline |
  | (P2)        |--(Produce)----->|    |        |        |        |   |       | (C2)        |
  +-------------+                 |  +----+  +----+  +----+  +----+  |       +-------------+
                                  |  | P0'|  | P1'|  | P2'|  | P3'|  |
  +-------------+                 |  |Rep |  |Rep |  |Rep |  |Rep |  |       +-------------+
  | IoT Sensor  |                 |  +----+  +----+  +----+  +----+  |-----> | Real-time   |
  | (P3)        |--(Produce)----->|     Leader  Follower Follower    |       | Dashboard   |
  +-------------+                 +-----------------------------------+       +-------------+

========================================================================================================
                              [ PARTITION INTERNAL STRUCTURE ]
========================================================================================================

  Partition (P0) on Broker 1                          Partition (P0 Replica) on Broker 2
  +------------------------------------------------+  +------------------------------------------------+
  | Log Segment (Active)                           |  | Log Segment (Replica)                         |
  | +----------------------------------------+     |  | +----------------------------------------+     |
  | | Offset 0: {user: "A", action: "click"} |     |  | | Offset 0: {user: "A", action: "click"} |     |
  | | Offset 1: {user: "B", action: "buy"}   |     |  | | Offset 1: {user: "B", action: "buy"}   |     |
  | | Offset 2: {user: "C", action: "view"}  |     |  | | Offset 2: {user: "C", action: "view"}  |     |
  | | ...                                    |     |  | | ...                                    |     |
  | +----------------------------------------+     |  | +----------------------------------------+     |
  |                                                |  |                                                |
  | Index File: Offset → Position mapping          |  | Index File: Offset → Position mapping          |
  | TimeIndex: Timestamp → Offset mapping          |  | TimeIndex: Timestamp → Offset mapping          |
  +------------------------------------------------+  +------------------------------------------------+

========================================================================================================
                              [ CONSUMER GROUP & REBALANCING ]
========================================================================================================

  Consumer Group: analytics-team (Group ID: "cg-analytics")

  Before Rebalance:                              After Rebalance (Consumer 3 added):
  +------------------------+                     +------------------------+
  | Consumer 1: P0, P1     |                     | Consumer 1: P0         |
  | Consumer 2: P2, P3     |                     | Consumer 2: P1, P2     |
  +------------------------+                     | Consumer 3: P3         |
                                                 +------------------------+

========================================================================================================
```

### 심층 동작 원리: 높은 처리량의 비밀

**1. Zero-copy와 페이지 캐시 활용**
```text
[ Traditional Data Transfer ]
  Disk → Kernel Buffer → User Buffer → Kernel Socket Buffer → Network
  (4번의 복사, 4번의 컨텍스트 스위치)

[ Kafka Zero-copy Transfer ]
  Disk (Page Cache) → Kernel Socket Buffer → Network
  (2번의 복사, sendfile 시스템 콜 1회)

성능 향상: CPU 사용량 50% 감소, 지연 시간 30% 감소
```

**2. 배치 처리와 압축**
```python
# Producer 배치 전송 최적화 설정
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['kafka1:9092', 'kafka2:9092', 'kafka3:9092'],

    # 배치 크기: 16KB 단위로 묶어서 전송
    batch_size=16384,

    # 대기 시간: 5ms 동안 모아서 배치 구성
    linger_ms=5,

    # 압축: snappy (빠른 압축/해제)
    compression_type='snappy',

    # 버퍼 메모리: 32MB
    buffer_memory=33554432,

    # ACK 설정: 리더 + 모든 ISR 확인 (강한 일관성)
    acks='all',

    # 직렬화
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# 이벤트 전송 (비동기)
for event in event_stream:
    producer.send('user_events', {
        'user_id': event.user_id,
        'action': event.action,
        'timestamp': event.timestamp,
        'metadata': event.metadata
    })

# 배치 플러시 및 종료
producer.flush()
producer.close()
```

**3. Consumer Group과 병렬 소비**
```python
# Consumer Group 설정으로 병렬 처리
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'user_events',

    # Consumer Group ID (중요!)
    group_id='analytics-processor',

    bootstrap_servers=['kafka1:9092', 'kafka2:9092', 'kafka3:9092'],

    # 오프셋 커밋 방식
    enable_auto_commit=False,  # 수동 커밋 (정확한 처리 보장)

    # 시작 오프셋
    auto_offset_reset='earliest',  # 또는 'latest'

    # 역직렬화
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),

    # 성능 튜닝
    max_poll_records=500,      # 한 번에 가져올 레코드 수
    fetch_max_bytes=52428800,  # 50MB
    max_partition_fetch_bytes=1048576  # 1MB per partition
)

# 메시지 처리 루프
for message in consumer:
    try:
        event = message.value
        process_event(event)  # 비즈니스 로직

        # 처리 완료 후 수동 커밋
        consumer.commit()

    except Exception as e:
        print(f"Error processing message: {e}")
        # 재시도 로직 또는 Dead Letter Queue로 이동

consumer.close()
```

### Exactly-Once Semantics 구현

```python
# Kafka Streams를 활용한 Exactly-Once 처리
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
import transaction

# Producer 설정 (트랜잭션 지원)
producer = KafkaProducer(
    bootstrap_servers=['kafka1:9092'],
    transactional_id='my-transactional-producer',  # 필수!
    acks='all'
)

# 트랜잭션 시작
producer.begin_transaction()

try:
    # 메시지 전송
    producer.send('output-topic', key=b'key1', value=b'value1')
    producer.send('output-topic', key=b'key2', value=b'value2')

    # Consumer 오프셋 커밋 (트랜잭션 내)
    consumer = KafkaConsumer('input-topic', group_id='my-group')
    # ... 메시지 처리 ...

    # 오프셋 커밋을 트랜잭션에 포함
    producer.send_offsets_to_transaction(
        consumer.position(),
        consumer.consumer_group_metadata()
    )

    # 트랜잭션 커밋 (원자적)
    producer.commit_transaction()

except Exception as e:
    # 트랜잭션 중단
    producer.abort_transaction()

producer.close()
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Kafka vs RabbitMQ vs AWS Kinesis

| 비교 지표 | Apache Kafka | RabbitMQ | AWS Kinesis |
|---|---|---|---|
| **아키텍처** | Pull-based, 로그 기반 | Push-based, 큐 기반 | Pull-based, 샤드 기반 |
| **메시지 보관** | O (설정 가능, 무제한 가능) | X (소비 후 삭제) | O (1~365일) |
| **순서 보장** | Partition 내 보장 | Queue 내 보장 | Shard 내 보장 |
| **처리량** | 초당 수백만 | 초당 수만 | 초당 수백만 |
| **지연 시간** | 2~5ms | 1~2ms | 50~200ms |
| **확장성** | Partition 추가로 수평 확장 | Cluster 추가 | Shard 추가 |
| **메시지 크기** | 1MB (기본), 조정 가능 | 무제한 | 1MB (Hard limit) |
| **비용 모델** | 오픈소스 (무료) | 오픈소스 (무료) | 샤드/데이터 양 기반 과금 |
| **운영 복잡도** | 높음 (ZooKeeper/Quorum) | 중간 | 낮음 (Managed) |

### 과목 융합 관점 분석

- **[운영체제 + Kafka]**: Kafka의 높은 성능은 **페이지 캐시**와 **Zero-copy**에 기반합니다. Kafka는 OS의 페이지 캐시를 그대로 활용하여 디스크 I/O를 최소화하고, sendfile 시스템 콜을 통해 커널 레벨에서 데이터를 직접 네트워크로 전송합니다.

- **[네트워크 + Kafka]**: Kafka는 **TCP 기반의 커스텀 프로토콜**을 사용하며, 배치 전송과 압축을 통해 네트워크 효율을 극대화합니다. 또한 **ISR(In-Sync Replicas)** 개념을 통해 리더와 팔로워 간의 데이터 동기화를 관리합니다.

- **[데이터베이스 + Kafka]**: Kafka는 **Change Data Capture(CDC)**의 소스로 활용됩니다. Debezium과 같은 커넥터가 RDBMS의 트랜잭션 로그를 읽어 Kafka로 전송하고, 이를 다시 데이터 웨어하우스나 검색 엔진으로 동기화합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 대규모 IoT 데이터 수집 및 처리**
- **문제**: 100만 대의 IoT 디바이스에서 초당 10만 개의 센서 데이터를 수집하여 실시간 모니터링 및 이상 탐지 필요
- **전략적 의사결정**:
  1. **토픽 설계**: 디바이스 타입별로 토픽 분리 (`sensors-temperature`, `sensors-pressure`)
  2. **파티셔닝 전략**: 디바이스 ID를 키로 사용하여 동일 디바이스의 데이터 순서 보장
  3. **보관 정책**: 원시 데이터 7일, 집계 데이터 1년
  4. **실시간 처리**: Kafka Streams + Flink로 윈도우 집계 및 이상 탐지

**시나리오 2: 마이크로서비스 간 이벤트 기반 통신**
- **문제**: 50개의 마이크로서비스 간 동기 HTTP 통신으로 인한 장애 전파 및 성능 저하
- **전략적 의사결정**:
  1. **이벤트 스키마 관리**: Schema Registry로 Avro 스키마 중앙 관리
  2. **도메인 이벤트 토픽**: `order-created`, `payment-completed` 등 도메인 이벤트별 토픽
  3. **CDC 도입**: Debezium으로 DB 변경 사항을 이벤트로 발행
  4. **SAGA 패턴**: 보상 트랜잭션을 위한 이벤트 기반 분산 트랜잭션

**시나리오 3: Kafka 클러스터 장애 복구**
- **문제**: 3대 브로커 중 2대가 동시에 장애 발생, 일부 파티션의 ISR이 1개로 감소
- **전략적 의사결정**:
  1. **최소 ISR 설정**: `min.insync.replicas=2`로 데이터 손실 방지
  2. **Unclean Leader Election**: 비활성화 (데이터 일관성 우선)
  3. **모니터링**: Under-replicated partitions, Offline partitions 메트릭 알람
  4. **백업 전략**: MirrorMaker 2로 DR 사이트 구축

### 주의사항 및 안티패턴 (Anti-patterns)

- **안티패턴 - 너무 많은 파티션**: 파티션 수가 수천 개를 넘으면 브로커의 파일 핸들과 메모리가 고갈됩니다. **파티션 수는 브로커당 수백 개 이내**로 유지해야 합니다.

- **안티패션 - Consumer Rebalancing Storm**: Consumer가 빈번하게 그룹을 떠나고 합류하면 지속적인 리밸런싱이 발생하여 처리가 중단됩니다. **Static Membership**과 **Heartbeat 튜닝**이 필요합니다.

- **안티패턴 - 메시지 크기 초과**: 기본 1MB를 초과하는 메시지를 전송하려고 하면 실패합니다. **Blob Storage에 저장하고 참조만 전송**하는 패턴을 권장합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | 내용 및 지표 |
|---|---|
| **정성적 효과** | - 시스템 간 느슨한 결합으로 장애 격리<br>- 실시간 데이터 파이프라인 통합<br>- 이벤트 기반 마이크로서비스 아키텍처 구현 |
| **정량적 효과** | - 데이터 처리 지연 시간 **95% 단축** (일일 배치 → 실시간)<br>- 시스템 처리량 **10배 증가** (초당 10만 → 100만 메시지)<br>- 장애 복구 시간 **90% 단축** (재생 가능한 로그) |

### 미래 전망 및 진화 방향

- **KRaft Mode (ZooKeeper 제거)**: Kafka 3.x부터 ZooKeeper 없이 자체적인 Raft 기반 컨트롤러로 운영 가능, 운영 복잡도 대폭 감소
- **Tiered Storage**: 로컬 디스크 + 클라우드 스토리지(S3) 계층화로 비용 최적화
- **Kafka 4.0**: 완전한 KRaft 모드, ZooKeeper 지원 중단 예정

**※ 참고 표준/가이드**:
- **Kafka Protocol Specification**: Apache Kafka Wire Protocol
- **Confluent Platform Documentation**: 엔터프라이즈 Kafka 운영 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)

- `[Apache Flink](@/studynotes/16_bigdata/03_streaming/apache_flink.md)`: Kafka와 결합하여 강력한 스트리밍 처리 구현
- `[Kafka Connect](@/studynotes/16_bigdata/03_streaming/kafka_connect.md)`: Kafka와 외부 시스템 연결을 위한 프레임워크
- `[Schema Registry](@/studynotes/16_bigdata/03_streaming/schema_registry.md)`: Kafka 메시지 스키마 관리
- `[Consumer Group](@/studynotes/16_bigdata/03_streaming/consumer_group.md)`: Kafka 병렬 소비 메커니즘
- `[Event Sourcing](@/studynotes/04_software_engineering/01_sdlc/event_sourcing.md)**: Kafka를 활용한 이벤트 소싱 아키텍처

---

## 👶 어린이를 위한 3줄 비유 설명

1. **Kafka가 뭔가요?**: 친구들에게 동시에 같은 이야기를 전해줘야 할 때, 중간에 **"이야기방"**을 만들어서 거기에 이야기를 적어두면 친구들이 언제든 와서 읽을 수 있는 거예요.
2. **왜 빠른가요?**: 이야기를 한 번에 여러 친구에게 동시에 전달할 수 있고, 이야기를 적어둔 공책을 여러 명이 나눠서 가지고 있어서 한 명이 아파도 다른 친구가 대신 보여줄 수 있어요.
3. **어디에 쓰나요?**: 넷플릭스에서 뭘 봤는지, 쿠팡에서 뭘 샀는지 같은 활동 기록을 모아서 추천해 주는 데 쓰여요!
