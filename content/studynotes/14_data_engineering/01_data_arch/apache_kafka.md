+++
title = "아파치 카프카 (Apache Kafka)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 아파치 카프카 (Apache Kafka)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 아파치 카프카는 고처리량, 저지연의 분산 이벤트 스트리밍 플랫폼으로, Pub/Sub 메시지 큐 모델과 영속적 저장을 결합하여 실시간 데이터 파이프라인의 중추 역할을 합니다.
> 2. **가치**: 초당 수백만 메시지 처리, 파티션 기반 병렬 처리, 데이터 영속성(디스크 저장)으로 안정적인 메시지 전달을 보장합니다.
> 3. **융합**: 마이크로서비스 이벤트 버스, 로그 집계, 스트리밍 ETL, 실시간 분석의 핵심 인프라로, Flink, Spark Streaming, Kafka Connect와 결합됩니다.

---

### Ⅰ. 개요

#### 1. 개념 및 정의
**아파치 카프카(Apafka Kafka)**는 2011년 LinkedIn에서 개발된 분산 이벤트 스트리밍 플랫폼입니다. 높은 처리량과 낮은 지연 시간으로 대규모 실시간 데이터 스트리밍을 지원합니다.

#### 2. 핵심 구성요소
| 구성요소 | 역할 |
|:---|:---|
| **Producer** | 메시지 생성 및 발행 |
| **Broker** | 메시지 저장 및 전달 (서버) |
| **Consumer** | 메시지 구독 및 처리 |
| **Topic** | 메시지 분류 카테고리 |
| **Partition** | 병렬 처리를 위한 토픽 분할 |
| **ZooKeeper** | 클러스터 코디네이션 (KRaft 모드에서는 제거됨) |

---

### Ⅱ. 아키텍처

```text
<<< Apache Kafka Architecture >>~

+--------------------------------------------------------------------------+
|                        Kafka Cluster                                      |
+--------------------------------------------------------------------------+

[Producer]                    [Topic: orders]
    |                              |
    +----> +----------------------+----------------------+
           |                      |                      |
           v                      v                      v
     +----------+           +----------+           +----------+
     | Broker 1 |           | Broker 2 |           | Broker 3 |
     | Partition|           | Partition|           | Partition|
     | 0, 3     |           | 1, 4     |           | 2, 5     |
     | (Leader) |           | (Leader) |           | (Leader) |
     +----------+           +----------+           +----------+
           |                      |                      |
           +----------------------+----------------------+
                                  |
    +-----------------------------+-----------------------------+
    |                             |                             |
    v                             v                             v
[Consumer 1]               [Consumer 2]               [Consumer 3]
(Partition 0, 3)           (Partition 1, 4)           (Partition 2, 5)

[Consumer Group A - 병렬 처리]

[핵심 개념]
- 파티션: 병렬 처리 단위, 순서 보장 (파티션 내)
- 오프셋: 각 메시지의 고유 위치 (Consumer가 관리)
- 복제: 파티션 복제 (Leader/Follower)로 고가용성
```

---

### Ⅲ. 핵심 원리

#### 1. 파티셔닝과 병렬 처리
```python
# 파티션 결정 로직
def get_partition(key, num_partitions):
    return hash(key) % num_partitions

# 같은 키 → 같은 파티션 → 순서 보장
# 다른 키 → 다른 파티션 → 병렬 처리
```

#### 2. 오프셋 관리
```text
Consumer Group이 각 파티션의 오프셋을 저장
- 장애 시 마지막 커밋 오프셋부터 재시작
- at-least-once / exactly-once 시맨틱 선택
```

#### 3. 영속성
```text
- 로그 파일로 디스크에 저장
- 순차 쓰기로 높은 처리량
- 설정된 보존 기간(Retention) 동안 보관
```

---

### Ⅳ. 실무 적용

```python
# Producer 예시
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# 메시지 전송
producer.send('orders', key=b'order-123', value={'product': 'laptop', 'price': 1500})
producer.flush()

# Consumer 예시
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'orders',
    bootstrap_servers=['kafka:9092'],
    group_id='order-processor',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    print(f"Received: {message.value}")
    # 처리 로직
```

---

### Ⅴ. Kafka vs 기타 메시지 큐

| 비교 | Kafka | RabbitMQ | AWS SQS |
|:---|:---|:---|:---|
| **처리량** | 초당 수백만 | 초당 수만 | 초당 수천 |
| **지연** | ms | ms | ms~초 |
| **영속성** | 디스크 | 메모리/디스크 | 디스크 |
| **순서 보장** | 파티션 내 | 큐 내 | 미보장 |
| **재생** | 가능 | 불가능 | 불가능 |

---

### Ⅴ. 결론

카프카는 현대 데이터 파이프라인의 중추이며, 실시간 스트리밍, 이벤트 소싱, 로그 집계의 핵심 인프라입니다.

---

### 관련 개념 맵
- **[Apache Flink](@/studynotes/14_data_engineering/01_data_arch/apache_flink.md)**
- **[CDC](@/studynotes/14_data_engineering/03_pipelines/cdc.md)**
- **[Kafka Connect](@/studynotes/14_data_engineering/03_pipelines/kafka_connect.md)**

---

### 어린이를 위한 3줄 비유
1. **우편함**: 카프카는 큰 우편함이에요. 누구나 편지를 넣을 수 있고, 여러 사람이 읽을 수 있어요.
2. **편지 분류**: 편지를 종류별로 다른 칸에 넣어요. '편지 칸', '엽서 칸', '소포 칸'처럼요.
3. **순서대로 읽기**: 편지를 읽을 때는 넣은 순서대로 읽어요. 나중에 다시 읽을 수도 있어요!
