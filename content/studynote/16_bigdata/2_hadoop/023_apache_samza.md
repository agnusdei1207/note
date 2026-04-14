+++
weight = 23
title = "아파치 삼자 (Apache Samza) 및 카프카 기반 스트리밍"
date = "2024-03-24"
[extra]
categories = "bigdata-hadoop"
+++

## 핵심 인사이트 (3줄 요약)
- **카프카 네이티브 스트리밍:** 링크드인(LinkedIn)에서 개발한, 아파치 카프카를 분산 메시지 버퍼로 사용하여 초고속 처리를 구현한 스트림 처리 엔진.
- **컴퓨팅-스토리지 분리:** 메시지 전달(Kafka), 자원 관리(YARN), 상태 저장(RocksDB)을 각기 다른 시스템에 위임하여 유연한 스케일링 달성.
- **상태 보존(Stateful Processing):** 로컬 RocksDB와 카프카 체인지로그(Changelog)를 결합하여 대규모 상태를 효율적으로 관리하고 장애 시 신속하게 복구.

### Ⅰ. 개요 (Context & Background)
대규모 소셜 네트워크 서비스인 링크드인에서는 초당 수백만 건의 사용자 활동을 실시간으로 처리해야 했습니다. 기존의 Storm은 운영 복잡도가 높았고, Spark는 배치 위주였습니다. Samza는 "메시징 시스템(Kafka)과 연동된 분산 연산 환경"을 목표로 설계되어, 카프카의 파티션 구조를 그대로 연산 단위로 매핑함으로써 데이터 이동을 최소화하고 높은 처리량(Throughput)을 확보했습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
Samza는 3개의 레이어(Streaming, Execution, Storage)가 명확히 분리된 구조를 가집니다.

```text
[ Apache Samza Architecture: Layered Model ]

   (Streaming Layer)       (Execution Layer)        (Storage Layer)
   -----------------      -------------------      -----------------
   [ Apache Kafka  ] <--> [ Samza Container ] <--> [ Local RocksDB ]
   (Input/Output)         (Job Processing)         (State Store)
          |                      |                        |
          +----------------------+------------------------+
                        [ Apache YARN ]
                      (Resource Management)

[ Key Components ]
1. Samza Job: 데이터를 읽고 쓰는 실행 단위.
2. Partition: 카프카의 파티션과 Samza의 테스크가 1:1 대응하여 병렬성 확보.
3. RocksDB: 상태(State)가 있는 연산을 위해 각 컨테이너 로컬에 배치된 KV 저장소.
4. Changelog Topic: 로컬 상태의 모든 변경사항을 카프카에 백업하여 내구성 보장.
```

**핵심 원리:**
1. **파티션 레벨의 병렬성:** 소스 스트림의 파티션 개수만큼 워커 노드를 늘려 선형적으로 확장 가능.
2. **로컬 상태 관리:** 원격 DB가 아닌 로컬 디스크(RocksDB)를 사용하여 네트워크 오버헤드 없이 수 테라바이트(TB)의 상태 유지 가능.
3. **체인지로그(Changelog) 패턴:** 로컬 DB 장애 시 카프카에 저장된 로그를 다시 읽어(Replay) 상태를 즉시 재구축(Self-healing).

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | Apache Storm | Apache Samza | Apache Flink |
| :--- | :--- | :--- | :--- |
| **핵심 설계 사상** | 유연한 토폴로지 구조 | 카프카와의 완벽한 공생 | 데이터 흐름 및 상태 관리 최적화 |
| **상태 관리 방식** | 외부 DB 의존적 | 로컬 RocksDB + Kafka 로그 | 체크포인트 기반 인메모리 |
| **자원 관리** | 자체 Nimbus/Supervisor | YARN / Mesos 활용 | 전용 JobManager 활용 |
| **주요 장점** | 매우 낮은 지연 시간 | 운영 편의성 및 데이터 일관성 | 강력한 윈도우 연산 및 SQL |
| **주요 사용처** | 링크드인, 실시간 로깅 | 실시간 분석, 상태 기반 조인 | 금융, 정밀 실시간 처리 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **실무 적용:** 실시간 광고 과금 시스템이나 사용자 세션 관리처럼 '과거의 상태'를 기억하면서(Stateful) 새로운 이벤트를 처리해야 하는 환경에서, 카프카를 이미 도입한 인프라라면 Samza가 가장 궁합이 좋습니다.
- **기술사적 판단:** Samza는 카프카에 대한 의존성이 매우 높다는 특징이 있습니다. 기술사는 "카프카를 주력 메시지 버스로 사용하는 기업에게는 최고의 선택지이지만, 범용적인 스트림 처리를 원한다면 Flink와의 기술적 경쟁 우위를 면밀히 따져보아야 한다"고 제언해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
Apache Samza는 '상태가 있는 스트림 처리(Stateful Stream Processing)'의 표준적인 설계 패턴을 제시했습니다. 특히 링크드인의 대규모 트래픽을 견디며 검증된 안정성은 클라우드 네이티브 환경의 마이크로서비스 간 비동기 통신 및 실시간 분석 인프라의 중요한 레퍼런스로 지속 기여하고 있습니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Stream Processing, Message Queueing
- **하위 개념:** RocksDB, Changelog, State Store, Container
- **연관 기술:** Apache Kafka, Apache YARN, Apache Flink, Kafka Streams

### 👶 어린이를 위한 3줄 비유 설명
1. 거대한 기차역(Kafka)에 수많은 짐(데이터)이 실린 기차들이 들어와요.
2. Samza라는 짐꾼들은 자기가 맡은 번호의 기차에서만 짐을 내려서, 옆에 있는 개인 창고(RocksDB)에 차곡차곡 정리해요.
3. 창고에 짐을 쌓아두면서 "오늘 짐이 몇 개나 들어왔지?"라고 기억하며 일하는 똑똑한 짐꾼이랍니다.
