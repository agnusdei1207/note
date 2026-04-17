+++
title = "Apache Samza — LinkedIn, Kafka 네이티브 스트리밍"
weight = 45
date = "2026-03-04"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
1. **Kafka 네이티브 연동**: Apache Samza는 LinkedIn에서 개발된 분산 스트림 처리 프레임워크로, Apache Kafka와의 강력한 결합을 통해 메시지의 내구성과 순서를 보장합니다.
2. **상태 관리(Stateful Processing)의 최적화**: 로컬 Key-Value 저장소(RocksDB)와 Kafka의 Changelog 토픽을 활용하여 장애 발생 시에도 빠르고 정확한 상태 복구를 지원합니다.
3. **컴퓨팅과 스토리지의 철저한 분리**: YARN을 통해 자원을 관리하며, 스트리밍 워크로드의 스케일아웃을 투명하게 처리하여 고성능 실시간 데이터 파이프라인 구축에 적합합니다.

### Ⅰ. 개요 (Context & Background)
- **도입 배경**: 기존 배치 처리(MapReduce) 방식은 실시간으로 발생하는 소셜 미디어 피드, 로그 분석, 실시간 알림 등 지연 시간이 중요한 서비스에 부적합했습니다. 이에 LinkedIn은 자사가 개발한 Kafka 생태계와 매끄럽게 통합되는 고성능 실시간 스트림 처리 엔진이 필요했습니다.
- **개념 정의**: Apache Samza는 Kafka를 메시징 계층으로, YARN을 리소스 관리 계층으로 사용하여, 분산된 데이터 스트림을 안정적으로 처리하는 프레임워크입니다.
- **설계 철학**: "심플함과 안정성". 파티션 모델을 Kafka와 동일하게 가져감으로써 데이터의 순서를 보장하고 병렬 처리를 직관적으로 수행합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
Samza의 아키텍처는 스트림(Stream), 작업(Job), 파티션(Partition)이라는 세 가지 핵심 개념으로 이루어지며, 상태 복구를 위한 로컬 저장소와 Changelog 토픽 메커니즘을 특징으로 합니다.

```text
+-------------------------------------------------------------+
|                Apache Samza Architecture                    |
|                                                             |
|  [ Input Streams (Kafka) ]       [ Output Streams (Kafka) ] |
|         Partition 0                      Partition 0        |
|         Partition 1                      Partition 1        |
|             |                                ^              |
|             v                                |              |
|  +-------------------------------------------------------+  |
|  |                       YARN Cluster                    |  |
|  |  +--------------------+       +--------------------+  |  |
|  |  | Samza Container 1  |       | Samza Container 2  |  |  |
|  |  | +----------------+ |       | +----------------+ |  |  |
|  |  | | Task (Part 0)  | |       | | Task (Part 1)  | |  |  |
|  |  | | - Process      | |       | | - Process      | |  |  |
|  |  | | - RocksDB(Local| |       | | - RocksDB(Local| |  |  |
|  |  | +-------|--------+ |       | +-------|--------+ |  |  |
|  |  +---------|----------+       +---------|----------+  |  |
|  +------------|----------------------------|-------------+  |
|               | (Write State)              |                |
|               v                            v                |
|  [ Changelog Topic (Kafka) ]    [ Changelog Topic (Kafka) ] |
|  (Backup for Local State)       (Backup for Local State)    |
+-------------------------------------------------------------+
```

1. **Samza Container & Task**: 하나의 Samza 작업(Job)은 여러 태스크(Task)로 나뉘며, 각 태스크는 YARN을 통해 할당된 컨테이너 내부에서 실행됩니다. 태스크는 입력 스트림의 1개 파티션을 전담하여 처리하므로 병렬성과 순서 보장이 동시에 달성됩니다.
2. **상태 관리 (Local State & Changelog)**: 각 태스크는 RocksDB를 로컬 상태 저장소로 활용하여 빠른 읽기/쓰기를 보장합니다. 이 로컬 상태의 변경 사항은 Kafka의 Changelog 토픽에 동기화되어, 컨테이너 장애 시 Changelog를 읽어 로컬 상태를 완벽히 복원합니다.
3. **Kafka와의 공생 (Symbiosis)**: 데이터 파티셔닝 전략과 오프셋 관리를 Kafka에 위임함으로써 시스템 복잡도를 낮추고 데이터 내구성을 극대화합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | Apache Samza | Apache Storm | Apache Flink |
| :--- | :--- | :--- | :--- |
| **상태 관리** | 로컬 RocksDB + Kafka Changelog 토픽 | 초창기는 무상태(Stateless), 이후 Trident 도입 | 글로벌 스냅샷 (Checkpointing/Savepoint) |
| **전송 보장** | At-least-once (상태 복구 시 제어 가능) | At-least-once (Tuple Tree 추적) | Exactly-once 보장 |
| **스트림 추상화** | Kafka 파티션과 1:1 매핑 | Spout / Bolt 토폴로지 | DataStream API, 풍부한 윈도우 기능 |
| **에코시스템 종속성**| Kafka & YARN 의존도 높음 | 독립적 실행 가능 | 스탠드얼론, YARN, K8s 등 다양함 |
| **유스케이스** | Kafka 중심의 파이프라인, 상태 기반 ETL | 실시간 단순 알럿, 밀리초 단위 반응 | 복잡한 이벤트 처리(CEP), 마이크로서비스 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **적입 기준**: 이미 Apache Kafka가 핵심 메시지 버스로 구축된 엔터프라이즈 환경에서, 단순하면서도 내결함성이 강한 스트림 ETL 및 실시간 집계가 필요할 때 가장 적합합니다.
- **기술사적 의사결정**:
  - Samza는 아키텍처를 단순화하기 위해 무거운 엔진 기능(메시지 전송, 리소스 할당)을 각각 Kafka와 YARN으로 오프로딩했습니다. 이는 "관심사의 분리(Separation of Concerns)" 원칙을 극대화한 모범 사례입니다.
  - 복잡한 윈도잉(Windowing)이나 머신러닝 연산이 필요한 경우에는 Flink나 Spark Structured Streaming 도입이 유리하지만, 수억 건의 메시지를 초저지연으로 라우팅/집계하는 순수 파이프라인에는 Samza가 유지보수 측면에서 탁월합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **비즈니스 가치**: Kafka를 통한 데이터 흐름의 투명성을 유지하면서 실시간 인사이트를 도출하여, 빠른 장애 감지와 사용자 맞춤형 서비스 제공에 기여합니다.
- **결론 및 미래 전망**: Samza는 LinkedIn 내부를 넘어 수많은 실시간 데이터 아키텍처의 표준 중 하나로 자리 잡았습니다. 다만 최근에는 Flink의 강세로 인해 점유율 성장은 둔화되고 있으나, Samza의 "Kafka Native State Management" 설계 철학은 최신 스트리밍 플랫폼(예: ksqlDB)에 지속적인 영감을 주고 있습니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 실시간 스트림 처리 (Real-time Stream Processing)
- **하위 개념**: Samza Task, Changelog Topic, Local State (RocksDB)
- **연관 기술**: Apache Kafka, YARN, Apache Flink, ksqlDB

### 👶 어린이를 위한 3줄 비유 설명
1. 공장에서 컨베이어 벨트(Kafka)를 타고 물건들이 끝없이 밀려오고 있어요.
2. Samza는 벨트마다 서 있는 숙련된 작업자(Task)예요. 작업자들은 자기가 맡은 줄의 물건만 순서대로 빠르게 처리하죠.
3. 작업자가 자리를 비워도 개인 수첩(RocksDB)과 공장 중앙 기록(Changelog)이 있어서, 다음 사람이 와서 바로 이어서 일할 수 있답니다!