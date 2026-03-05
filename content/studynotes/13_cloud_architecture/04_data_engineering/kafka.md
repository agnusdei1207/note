+++
title = "아파치 카프카 (Apache Kafka)"
date = "2026-03-05"
[extra]
categories = "studynotes-cloud"
tags = ["kafka", "messaging", "streaming", "event-driven", "distributed-system"]
+++

# 아파치 카프카 (Apache Kafka)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 아파치 카프카는 분산 커밋 로그(Distributed Commit Log) 기반의 고성능 메시징/스트리밍 플랫폼으로, 프로듀서가 발행한 이벤트를 파티션에 순차 저장하고 컨슈머가 오프셋 기반으로 폴링하는 Pub/Sub 모델을 구현합니다.
> 2. **가치**: 초당 수백만 메시지 처리, 서브밀리초 지연, 무제한 보존(Retention)으로 실시간 데이터 파이프라인, 이벤트 소싱, 로그 집계의 핵심 인프라 역할을 수행합니다.
> 3. **융합**: CDC(Change Data Capture), 스트림 처리(Kafka Streams, Flink), 마이크로서비스 이벤트 버스와 결합하여 이벤트 기반 아키텍처(EDA)의 중추를 형성합니다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의
아파치 카프카(Apache Kafka)는 링크드인(LinkedIn)에서 개발된 후 2011년 아파치 재단에 기부된 분산 이벤트 스트리밍 플랫폼입니다. 카프카는 메시지를 토픽(Topic)으로 분류하고, 각 토픽을 파티션(Partition)으로 분할하여 순차적인 로그 파일에 저장합니다. 컨슈머는 자신의 오프셋(Offset)을 관리하며, 언제든지 이전 메시지를 재처리(Replay)할 수 있습니다.

### 💡 비유
카프카는 "분산 택배 분류 센터"와 같습니다. 택배(메시지)가 도착하면 목적지별(토픽) 컨베이어 벨트(파티션)에 올라갑니다. 여러 택배 기사(컨슈머)가 각자 담당 벨트에서 자신이 마지막으로 가져간 위치(오프셋) 이후의 택배만 가져갑니다. 센터는 모든 택배를 7일간 보관하므로, 필요하면 지난 택배를 다시 찾을 수 있습니다.

### 등장 배경 및 발전 과정

#### 1. 기존 메시징 시스템의 한계
- **JMS/ActiveMQ**: 메시지 처리 후 삭제, 재처리 불가, 처리량 제한
- **RabbitMQ**: 브로커 중심 라우팅, 확장성 한계
- **로그 분석**: 실시간 처리 어려움, 배치 위주

#### 2. 패러다임 변화
```
2011년: LinkedIn, Apache Kafka 0.7 오픈소스 공개
2012년: Kafka 0.8 - 복제(Replication) 기능 추가
2014년: Confluent 설립 (Kafka 창시자들)
2016년: Kafka 0.10 - Kafka Streams 도입
2017년: Kafka 0.11 - Exactly-Once Semantics (EOS)
2019년: Kafka 2.4 - 멀티 테넌시 개선
2021년: Kafka 3.0 - KRaft 모드 (ZooKeeper 제거 시작)
2023년: Kafka 3.6 - KRaft 프로덕션 준비 완료
```

#### 3. 비즈니스적 요구사항
- **실시간 로그 수집**: 수천 대 서버의 로그를 중앙 집중
- **이벤트 소싱**: 상태 변경 이력 보존
- **마이크로서비스 통신**: 비동기 이벤트 기반 느슨한 결합
- **CDC**: 데이터베이스 변경 사항 실시간 전파

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|-----------|------|
| **Producer** | 메시지 발행 | 파티셔너로 파티션 결정, 배치 전송 | idempotent, transactions | 택배 보내는 사람 |
| **Broker** | 메시지 저장/전달 | 로그 세그먼트 파일, 페이지 캐시 | Zero-Copy, mmap | 분류 센터 창고 |
| **Topic** | 메시지 분류 단위 | 논리적 채널, N개 파티션으로 구성 | partition count | 목적지 도시 |
| **Partition** | 병렬 처리 단위 | 순차 로그 파일, 오프셋 인덱싱 | segment file | 컨베이어 벨트 |
| **Consumer** | 메시지 구독/처리 | 오프셋 기반 폴링, 커밋 | manual/automatic | 택배 기사 |
| **Consumer Group** | 병렬 소비 그룹 | 파티션 분배, 리밸런싱 | cooperative sticky | 배송 팀 |
| **Offset** | 메시지 위치 식별자 | 파티션 내 순차 번호 (0부터) | __consumer_offsets | 택배 영수증 번호 |
| **Replica** | 고가용성 복제본 | Leader(쓰기/읽기), Follower(동기화) | ISR, acks | 백업 창고 |
| **ZooKeeper / KRaft** | 메타데이터 관리 | 브로커 상태, 컨트롤러 선출 | ZAB / Raft | 센터 관리 시스템 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         아파치 카프카 아키텍처                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │                            Producers                                     │  │
│   │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐           │  │
│   │  │ Web App   │  │ Mobile API│  │ IoT Device│  │ DB CDC    │           │  │
│   │  │ Producer  │  │ Producer  │  │ Producer  │  │ Producer  │           │  │
│   │  └───────────┘  └───────────┘  └───────────┘  └───────────┘           │  │
│   │        │              │              │              │                  │  │
│   │        └──────────────┼──────────────┼──────────────┘                  │  │
│   │                       ▼              ▼                                  │  │
│   │              ┌──────────────────────────────┐                          │  │
│   │              │     Producer Buffer Batch    │                          │  │
│   │              │  (batch.size=16KB, linger=5ms)│                         │  │
│   │              └──────────────────────────────┘                          │  │
│   └─────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                          │
│                                      ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │                    Kafka Cluster (Brokers)                               │  │
│   │  ┌───────────────────────────────────────────────────────────────────┐  │  │
│   │  │                   Topic: "user-events"                             │  │  │
│   │  │                                                                   │  │  │
│   │  │  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐    │  │  │
│   │  │  │  Partition 0    │ │  Partition 1    │ │  Partition 2    │    │  │  │
│   │  │  │   (Leader)      │ │   (Leader)      │ │   (Leader)      │    │  │  │
│   │  │  │                 │ │                 │ │                 │    │  │  │
│   │  │  │ Broker 1        │ │ Broker 2        │ │ Broker 3        │    │  │  │
│   │  │  │ ┌─────────────┐ │ │ ┌─────────────┐ │ │ ┌─────────────┐ │    │  │  │
│   │  │  │ │ Segment     │ │ │ │ Segment     │ │ │ │ Segment     │ │    │  │  │
│   │  │  │ │ 000000.log  │ │ │ │ 000000.log  │ │ │ │ 000000.log  │ │    │  │  │
│   │  │  │ │ 000000.idx  │ │ │ │ 000000.idx  │ │ │ │ 000000.idx  │ │    │  │  │
│   │  │  │ └─────────────┘ │ │ └─────────────┘ │ │ └─────────────┘ │    │  │  │
│   │  │  │ ┌─────────────┐ │ │ ┌─────────────┐ │ │ ┌─────────────┐ │    │  │  │
│   │  │  │ │ Follower    │ │ │ │ Follower    │ │ │ │ Follower    │ │    │  │  │
│   │  │  │ │ (Broker 2)  │ │ │ │ (Broker 3)  │ │ │ │ (Broker 1)  │ │    │  │  │
│   │  │  │ └─────────────┘ │ │ └─────────────┘ │ │ └─────────────┘ │    │  │  │
│   │  │  └─────────────────┘ └─────────────────┘ └─────────────────┘    │  │  │
│   │  │                                                                   │  │  │
│   │  │  Replica Assignment:                                              │  │  │
│   │  │  Partition 0: [1, 2, 3]  (Leader=1, ISR=[1,2,3])                 │  │  │
│   │  │  Partition 1: [2, 3, 1]  (Leader=2, ISR=[2,3,1])                 │  │  │
│   │  │  Partition 2: [3, 1, 2]  (Leader=3, ISR=[3,1,2])                 │  │  │
│   │  └───────────────────────────────────────────────────────────────────┘  │  │
│   │                                                                         │  │
│   │  ┌─────────────────────────────────────────────────────────────────┐   │  │
│   │  │                     Broker Internal                              │   │  │
│   │  │                                                                 │   │  │
│   │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │   │  │
│   │  │  │  Page Cache  │  │  Log Cleaner │  │  Replica Mgr │         │   │  │
│   │  │  │  (OS Level)  │  │  (Compaction)│  │  (Fetch/Fetch│         │   │  │
│   │  │  │              │  │              │  │   Thread)    │         │   │  │
│   │  │  └──────────────┘  └──────────────┘  └──────────────┘         │   │  │
│   │  └─────────────────────────────────────────────────────────────────┘   │  │
│   └─────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                          │
│                                      ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │                          Consumers                                       │  │
│   │  ┌───────────────────────────────────────────────────────────────────┐  │  │
│   │  │                    Consumer Group: "analytics"                     │  │  │
│   │  │                                                                   │  │  │
│   │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │  │  │
│   │  │  │ Consumer 1  │  │ Consumer 2  │  │ Consumer 3  │               │  │  │
│   │  │  │             │  │             │  │             │               │  │  │
│   │  │  │ Partition 0 │  │ Partition 1 │  │ Partition 2 │               │  │  │
│   │  │  │ offset: 150 │  │ offset: 200 │  │ offset: 175 │               │  │  │
│   │  │  └─────────────┘  └─────────────┘  └─────────────┘               │  │  │
│   │  │                                                                   │  │  │
│   │  │  Group Coordinator: Broker 1                                      │  │  │
│   │  │  Rebalance Strategy: CooperativeSticky                            │  │  │
│   │  └───────────────────────────────────────────────────────────────────┘  │  │
│   │                                                                         │  │
│   │  ┌───────────────────────────────────────────────────────────────────┐  │  │
│   │  │                    Consumer Group: "realtime"                      │  │  │
│   │  │  ┌─────────────┐  ┌─────────────┐                                 │  │  │
│   │  │  │ Consumer 4  │  │ Consumer 5  │                                 │  │  │
│   │  │  │ Partition 0 │  │ Partition 1 │  Partition 2 (할당 없음)         │  │  │
│   │  │  │ Partition 2 │  │             │  (Consumer < Partition)         │  │  │
│   │  │  └─────────────┘  └─────────────┘                                 │  │  │
│   │  └───────────────────────────────────────────────────────────────────┘  │  │
│   └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │                    Metadata Management                                   │  │
│   │  ┌──────────────────────────────┐  ┌──────────────────────────────┐    │  │
│   │  │      ZooKeeper Ensemble      │  │        KRaft Mode            │    │  │
│   │  │    (Legacy, v3.x 이전)       │  │    (New, v3.x+ )             │    │  │
│   │  │                              │  │                              │    │  │
│   │  │  [ZK1]──[ZK2]──[ZK3]        │  │  [Controller1]──[Controller2]│    │  │
│   │  │   │      │      │            │  │   │              │           │    │  │
│   │  │   └──────┴──────┘            │  │   └──────────────┘           │    │  │
│   │  │  - 브로커 메타데이터         │  │  - Raft 기반 합의            │    │  │
│   │  │  - 컨트롤러 선출             │  │  - ZooKeeper 불필요          │    │  │
│   │  │  - ACL 저장                  │  │  - 단순화된 아키텍처         │    │  │
│   │  └──────────────────────────────┘  └──────────────────────────────┘    │  │
│   └─────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

#### ① 프로듀서 메시지 전송 프로세스

```
Producer 메시지 전송 7단계:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: 메시지 직렬화 (Serializer)
        │
        │  Key Serializer: String → byte[]
        │  Value Serializer: JSON/Avro/Protobuf → byte[]
        │
        ▼
Step 2: 파티션 결정 (Partitioner)
        │
        │  if (key != null):
        │      partition = hash(key) % num_partitions
        │  else:
        │      partition = sticky_partition (batch 단위 라운드로빈)
        │
        ▼
Step 3: 배치 버퍼에 추가 (RecordAccumulator)
        │
        │  배치 조건:
        │  - batch.size = 16KB (가득 차면 전송)
        │  - linger.ms = 5ms (시간 경과 시 전송)
        │  - buffer.memory = 32MB (전체 버퍼)
        │
        ▼
Step 4: Sender 스레드가 배치 전송
        │
        │  NetworkClient가 NIO 비동기 전송
        │  여러 파티션의 배치를 하나의 요청으로 묶음
        │
        ▼
Step 5: 브로커 Leader 파티션에 기록
        │
        │  Log Segment 파일에 Append-Only 쓰기
        │  순차 디스크 쓰기 = 매우 빠름 (수백 MB/s)
        │  페이지 캐시 활용 (OS 수준)
        │
        ▼
Step 6: Follower 동기화
        │
        │  acks=all (ISR 모든 복제본 확인):
        │  - Leader가 기록
        │  - 모든 ISR Follower가 복제 완료 대기
        │  - Producer에게 응답
        │
        │  acks=1 (Leader만 확인):
        │  - Leader 기록 후 즉시 응답
        │  - Follower 동기화는 비동기
        │
        │  acks=0 (확인 없음):
        │  - 전송 후 응답 대기 없음
        │  - 최고 속도, 메시지 손실 가능
        │
        ▼
Step 7: 오프셋 할당 및 응답
        │
        │  Response: { partition: 0, offset: 12345, timestamp: ... }
        │  Producer Callback 호출
        │

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### ② 컨슈머 폴링 및 오프셋 커밋

```python
"""
Kafka Consumer 폴링 메커니즘 상세
"""

from kafka import KafkaConsumer
from kafka.structs import TopicPartition

class KafkaConsumerDeepDive:
    """카프카 컨슈머 내부 동작 시뮬레이션"""

    def __init__(self, config: dict):
        self.config = config
        self.fetched_records = {}
        self.last_consumed_offset = {}

    def poll_process(self, timeout_ms: int = 500):
        """
        Consumer.poll() 내부 동작
        """
        # ============================================
        # Phase 1: 코디네이터 발견 및 그룹 조인
        # ============================================
        """
        1. Group Coordinator 브로커 찾기
           - KafkaInternal.__consumer_offsets 파티션 ID:
             hash(group_id) % 50
           - 해당 파티션의 Leader 브로커가 Coordinator

        2. JoinGroup 요청
           - 모든 컨슈머가 Coordinator에 조인
           - 가장 먼저 조인한 컨슈머가 Leader
           - Leader가 파티션 할당 계획 수립

        3. SyncGroup 요청
           - Leader가 할당 계획 전파
           - 모든 컨슈머가 자신의 파티션 확인
        """

        # ============================================
        # Phase 2: 오프셋 조회
        # ============================================
        """
        1. __consumer_offsets 토픽에서 오프셋 조회
           Key: (group_id, topic, partition)
           Value: { offset: 12345, metadata: "" }

        2. 커밋된 오프셋이 없으면:
           - auto.offset.reset = "earliest": 처음부터
           - auto.offset.reset = "latest": 최근부터
        """

        # ============================================
        # Phase 3: Fetch 요청 (데이터 가져오기)
        # ============================================
        """
        1. 각 파티션 리더 브로커에게 Fetch 요청
           - fetch.min.bytes = 1 (기본)
           - fetch.max.wait.ms = 500
           - max.poll.records = 500

        2. 브로커 응답:
           - 오프셋 12345부터 레코드 100개
           - High Watermark (HW): 12500 (복제 완료된 오프셋)
           - Log Start Offset (LSO): 0 (보존 기간 내 시작)
        """

        # ============================================
        # Phase 4: 레코드 처리
        # ============================================
        for record in self.fetched_records:
            print(f"Processing: partition={record.partition}, "
                  f"offset={record.offset}, key={record.key}")

            # 비즈니스 로직 실행
            self.process_record(record)

        # ============================================
        # Phase 5: 오프셋 커밋
        # ============================================
        """
        자동 커밋 (enable.auto.commit=true):
          - 주기적 (auto.commit.interval.ms=5000)
          - poll() 호출 시점에 체크
          - 데이터 손실 가능성 (처리 전 커밋)

        수동 커밋 (enable.auto.commit=false):
          - commitSync(): 동기 커밋 (블로킹)
          - commitAsync(): 비동기 커밋 (논블로킹)
          - 정확히 한 번 처리 위해 필수
        """

    def consumer_rebalance_listener(self):
        """
        리밸런싱 이벤트 처리
        """
        """
        리밸런싱 트리거:
        1. 새 컨슈머 조인
        2. 기존 컨슈머 이탈 (session.timeout.ms 초과)
        3. 컨슈머 그룹 구독 토픽 변경

        리밸런싱 알고리즘:
        - Eager: 전체 정지 → 재할당 → 재시작 (Stop-the-World)
        - Cooperative: 점진적 이전 (중단 최소화)

        Rebalance Listener 활용:
        def on_partitions_revoked(partitions):
            # 할당 해제 전 오프셋 커밋
            commit_current_offsets()

        def on_partitions_assigned(partitions):
            # 새 파티션 할당 시 초기화
            seek_to_beginning_or_committed(partitions)
        """


# 실제 운영 설정 예시
PRODUCER_CONFIG = {
    'bootstrap.servers': 'kafka1:9092,kafka2:9092,kafka3:9092',
    'key.serializer': 'org.apache.kafka.common.serialization.StringSerializer',
    'value.serializer': 'io.confluent.kafka.serializers.KafkaAvroSerializer',
    'schema.registry.url': 'http://schema-registry:8081',

    # 성능 튜닝
    'batch.size': 32768,           # 32KB 배치
    'linger.ms': 10,               # 10ms 대기
    'buffer.memory': 67108864,     # 64MB 버퍼
    'compression.type': 'lz4',     # 압축 (none/gzip/snappy/lz4/zstd)

    # 신뢰성
    'acks': 'all',                 # 모든 ISR 확인
    'enable.idempotence': True,    # 중복 방지
    'max.in.flight.requests.per.connection': 5,

    # Exactly-Once (트랜잭션)
    'transactional.id': 'order-service-producer',
}

CONSUMER_CONFIG = {
    'bootstrap.servers': 'kafka1:9092,kafka2:9092,kafka3:9092',
    'group.id': 'order-processor-group',
    'key.deserializer': 'org.apache.kafka.common.serialization.StringDeserializer',
    'value.deserializer': 'io.confluent.kafka.serializers.KafkaAvroDeserializer',
    'schema.registry.url': 'http://schema-registry:8081',

    # 오프셋 관리
    'enable.auto.commit': False,   # 수동 커밋
    'auto.offset.reset': 'earliest',

    # 성능
    'fetch.min.bytes': 1024,       # 1KB 이상이면 응답
    'fetch.max.wait.ms': 500,
    'max.poll.records': 500,

    # 하트비트 / 세션
    'session.timeout.ms': 30000,   # 30초 무응답 시 이탈로 간주
    'heartbeat.interval.ms': 10000, # 10초마다 하트비트
    'max.poll.interval.ms': 300000, # 5분 내 poll() 없으면 이탈

    # Exactly-Once (트랜잭션)
    'isolation.level': 'read_committed',
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 메시징 시스템

| 비교 항목 | Kafka | RabbitMQ | ActiveMQ | AWS Kinesis | Pulsar |
|-----------|-------|----------|----------|-------------|--------|
| **아키텍처** | Pull-based | Push-based | Push-based | Pull-based | Pull-based |
| **메시지 보존** | 무제한 (설정) | 소비 후 삭제 | 소비 후 삭제 | 1-365일 | 무제한 |
| **순서 보장** | 파티션 내 | 큐 내 | 큐 내 | 샤드 내 | 파티션 내 |
| **처리량** | 100K+/s | 20K/s | 10K/s | 100K+/s | 100K+/s |
| **지연** | < 5ms | < 1ms | < 5ms | < 100ms | < 5ms |
| **파티셔닝** | 네이티브 | 없음 | 없음 | 샤드 | 네이티브 |
| **스트리밍** | Kafka Streams | 없음 | 없음 | Kinesis Analytics | Pulsar Functions |
| **프로토콜** | TCP (자체) | AMQP | JMS/AMQP | HTTP/TCP | TCP (자체) |

### 과목 융합 관점 분석

#### [클라우드 + 운영체제] Zero-Copy와 페이지 캐시
```
Kafka의 고성능 비밀: Zero-Copy I/O

전통적인 데이터 전송 (4번 복사):
┌───────────────────────────────────────────────────────────────┐
│  [Disk] ─read()──▶ [Kernel Buffer] ─copy──▶ [User Buffer]    │
│                                                      │        │
│  [Socket] ◀─write()── [Socket Buffer] ◀─copy────────┘        │
└───────────────────────────────────────────────────────────────┘

Kafka의 Zero-Copy (sendfile 시스템 콜):
┌───────────────────────────────────────────────────────────────┐
│  [Disk] ─sendfile()──▶ [Kernel Buffer] ─DMA──▶ [NIC]         │
│         (사용자 공간 거치지 않음)                              │
└───────────────────────────────────────────────────────────────┘

성능 향상:
- CPU 사이클 50% 절감
- 메모리 대역폭 50% 절감
- 컨텍스트 스위치 50% 감소

페이지 캐시 활용:
1. 프로듀서가 쓴 데이터가 OS 페이지 캐시에 상주
2. 컨슈머가 읽을 때 디스크가 아닌 메모리에서 읽기
3. hot 데이터는 디스크 접근 없이 전송

Kafka 설정:
log.flush.interval.messages=Long.MAX_VALUE  # OS에 맡김
```

#### [클라우드 + 네트워크] Exactly-Once Semantics (EOS)
```
카프카 Exactly-Once 구현 메커니즘:

문제: At-Least-Once에서 중복 처리
- 프로듀서 재시도로 중복 메시지 발생
- 컨슈머 처리 후 커밋 전 장애 → 재처리

해결: 트랜잭션 + 아이덴턴트 프로듀서

1. Idempotent Producer:
   - 각 메시지에 PID(Producer ID)와 Sequence Number 부여
   - 브로커가 (PID, Partition, SeqNum)으로 중복 감지
   - 중복 메시지 무시

2. Transactions:
   begin_transaction()
   │
   ├─ send(topic_A, msg1)  # 원자성 보장
   ├─ send(topic_A, msg2)
   ├─ send(topic_B, msg3)
   ├─ send_offsets_to_consumer_group(offsets)  # 소비-생성 패턴
   │
   commit_transaction()  # 모두 성공 또는 모두 실패

3. Consumer isolation.level:
   - read_uncommitted: 모든 메시지 읽기 (기본)
   - read_committed: 커밋된 트랜잭션만 읽기

구현 예시 (Consume-Process-Produce):
```java
// Kafka Streams의 Exactly-Once
Properties props = new Properties();
props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG,
          StreamsConfig.EXACTLY_ONCE_V2);

KStream<String, Order> orders = builder.stream("orders");
orders.groupByKey()
      .aggregate(
          () -> 0.0,
          (key, order, total) -> total + order.getAmount(),
          Materialized.as("order-totals")
      )
      .toStream()
      .to("order-summaries");
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 시나리오

#### 시나리오 1: 대규모 이벤트 스트리밍 플랫폼
```
요구사항:
- 일일 이벤트 100억 건 (100K TPS 피크)
- 보존 기간 7일
- 멀티 리전 복제
- 스키마 진화 지원

기술사 판단:
1. 클러스터 구성:
   - 브로커: 30대 (r5.4xlarge, 16vCPU, 128GB RAM)
   - 토픽: 500개, 파티션: 6000개 (토픽당 12개)
   - 복제 팩터: 3

2. 튜닝:
   # 브로커
   num.network.threads=8
   num.io.threads=8
   socket.send.buffer.bytes=1024000
   socket.receive.buffer.bytes=1024000
   log.retention.hours=168
   log.segment.bytes=1073741824  # 1GB

   # 프로듀서
   batch.size=65536
   linger.ms=10
   compression.type=zstd

3. 멀티 리전:
   - Cluster Linking (MirrorMaker 2)
   - 비동기 복제, RPO < 1초

4. 스키마 관리:
   - Confluent Schema Registry
   - Avro 포맷, 호환성: BACKWARD
```

### 도입 시 고려사항 체크리스트

#### 기술적 고려사항
- [ ] **파티션 수**: TPS / 파티션당 성능 (10K TPS/파티션)
- [ ] **복제 팩터**: 3 (프로덕션), 1 (개발)
- [ ] **acks 설정**: all (신뢰성), 1 (성능)
- [ ] **보존 정책**: 시간/크기 기반, Compaction

#### 운영적 고려사항
- [ ] **모니터링**: Prometheus + Grafana, Burrow
- [ ] **백업**: 미러링, 스냅샷
- [ ] **보안**: SASL/SCRAM, TLS, ACL

### 주의사항 및 안티패턴

#### 안티패턴 1: 과도한 파티션 수
```
잘못된 접근:
- 100개 토픽 × 100파티션 = 10,000파티션
- 브로커 5대

문제:
- 리밸런싱 시간 증가 (파티션당 1-2초)
- ZooKeeper 메타데이터 부하
- 페이지 캐시 분산으로 성능 저하

해결:
- 파티션당 10K TPS 기준으로 산정
- 100K TPS → 10-15 파티션 충분
```

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 구분 | 기존 (JMS/RabbitMQ) | Kafka | 개선효과 |
|-----------|---------------------|-------|---------|
| 처리량 (TPS) | 10K | 1M+ | 100배 |
| 지연 (p99) | 50ms | 5ms | 90% 감소 |
| 데이터 보존 | 즉시 삭제 | 7일+ | 재처리 가능 |
| 확장성 | 수직 | 수평 | 무제한 |

### 미래 전망 및 진화 방향

1. **KRaft 모드**: ZooKeeper 제거, 단순화
2. **Tiered Storage**: S3/ABFS로 콜드 데이터 이동
3. **Kafka 4.0**: KRaft 전환, JBOD 개선

### 참고 표준/가이드
- **Apache Kafka**: kafka.apache.org
- **Confluent Docs**: docs.confluent.io
- **Kafka Papers**: "Kafka: a Distributed Messaging System"

---

## 관련 개념 맵 (Knowledge Graph)

1. [이벤트 기반 아키텍처 (EDA)](./event_driven_architecture.md)
   - 관계: 카프카가 EDA의 핵심 이벤트 버스

2. [CDC (Change Data Capture)](./cdc.md)
   - 관계: Debezium으로 DB 변경을 카프카에 전송

3. [사가 패턴 (Saga Pattern)](./saga_pattern.md)
   - 관계: 카프카로 코레오그래피 사가 구현

4. [아파치 스파크 (Apache Spark)](./spark.md)
   - 관계: Structured Streaming으로 카프카 소비

5. [옵저버빌리티 (Observability)](./observability.md)
   - 관계: 분산 추적을 위한 헤더 전파

6. [데이터 레이크 (Data Lake)](./data_lake.md)
   - 관계: 카프카 → S3/HDFS 싱크

---

## 어린이를 위한 3줄 비유 설명

**비유: 분산 택배 분류 센터**

카프카는 엄청나게 큰 택배 분류 센터 같아요. 택배(메시지)가 도착하면 목적지별(토픽) 컨베이어 벨트(파티션)에 올라가서 줄을 서죠. 택배 기사님들(컨슈머)이 각자 맡은 벨트에서 자기가 마지막으로 가져간 곳(오프셋) 다음 택배만 가져가요.

**원리:**
센터는 택배를 일주일 동안 보관해요. 그래서 필요하면 지난번에 받은 택배를 또 찾아볼 수 있죠. 택배가 너무 많으면 컨베이어 벨트를 늘리면 되고, 기사님도 더 뽑으면 돼요!

**효과:**
이렇게 하면 아무리 많은 택배도 놓치지 않고 정확하게 배달할 수 있어요. 기사님이 아파도 다른 기사님이 대신할 수 있고, 센터가 불타도 택배는 여러 곳에 복사되어 있어서 안전해요!
