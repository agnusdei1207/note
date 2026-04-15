+++
weight = 27
title = "데이터 직렬화 (Serialization): Avro, Protobuf, Thrift"
date = "2024-03-24"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
- **객체와 바이트의 변환:** 메모리상의 객체를 네트워크 전송이나 디스크 저장이 가능한 바이트 스트림으로 변환하는 기술이며, 분산 컴퓨팅의 성능 병목을 결정하는 핵심 요소.
- **스키마 기반 최적화:** 스키마 정보를 별도로 관리하여 데이터 크기를 획기적으로 줄이고, 버전 간 호환성(Evolution)을 지원하여 대규모 시스템의 안정성 보장.
- **빅데이터 표준:** 하둡 에코시스템의 Avro, 구글의 Protobuf, 페이스북의 Thrift 등 용도에 맞는 바이너리 포맷 선택이 시스템 아키텍처의 필수 역량.

### Ⅰ. 개요 (Context & Background)
빅데이터 분산 환경에서는 수많은 서버 간에 끊임없이 데이터를 주고받습니다. 이때 Java 기본 직렬화나 JSON/XML 같은 텍스트 포맷은 속도가 느리거나 크기가 너무 커서 네트워크 대역폭을 낭비하게 됩니다. 따라서 고속 연산과 효율적 저장을 위해 이진(Binary) 형태의 직렬화 프레임워크가 등장했습니다. 이는 특히 하둡 HDFS나 카프카(Kafka) 스트림 처리에서 성능 최적화의 제1지표가 됩니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
데이터 직렬화는 스키마 정의를 바탕으로 데이터를 압축된 바이너리로 변환합니다.

```text
[ Data Serialization Workflow ]

 (Source: Object)       (Serialization Engine)      (Target: Byte Stream)
 +--------------+       +-------------------+       +-------------------+
 | User Profile |       |  IDL (Interface   |       |  0101 1010 1100   |
 | - ID: 123    | ----> |  Definition Lang) | ----> |  (Binary Data)    |
 | - Name: "PF" |       |  + Code Gen       |       |                   |
 +--------------+       +-------------------+       +-------------------+
                                                          | (Network / Disk)
                                                          v
                                                    +-------------------+
                                                    |  Deserialization  |
                                                    +-------------------+

[ Comparison of Formats ]
1. Apache Avro: Schema in JSON, Binary data. Self-describing, Excellent for Hadoop.
2. Protocol Buffers: Google's standard. Compact, Fast, Strongly typed.
3. Apache Thrift: Facebook's standard. Focuses on RPC and cross-language support.
```

**핵심 원리:**
1. **바이너리 인코딩:** 정수형 가변 길이 인코딩(Varint), 문자열 태그 생략 등을 통해 데이터 크기를 최소화.
2. **스키마 에볼루션 (Schema Evolution):** 새로운 필드가 추가되거나 삭제되어도 이전 버전의 코드와 데이터가 서로 호환(Forward/Backward Compatibility)되도록 설계.
3. **코드 생성 (Code Generation):** IDL 파일을 컴파일하여 특정 언어(Java, Python 등)에 맞는 최적화된 클래스 코드를 자동 생성.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | Apache Avro | Protocol Buffers (Protobuf) | Apache Thrift |
| :--- | :--- | :--- | :--- |
| **개발 주체** | Apache (Doug Cutting) | Google | Facebook |
| **스키마 저장** | 데이터와 함께 저장 | 별도 .proto 파일 관리 | 별도 .thrift 파일 관리 |
| **호환성 강점** | 동적 언어(Python 등) 최적 | 메시지 크기 및 속도 최적 | 다국어 RPC 통신 최적 |
| **주요 활용** | 하둡(HDFS), 카프카(Kafka) | gRPC, 구글 내부 통신 | MSA 간 서비스 호출 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **실무 적용:** 카프카 기반의 이벤트 드리븐 아키텍처를 구축할 때, 메시지 포맷으로 Avro를 사용하고 Confluent Schema Registry를 연동하면, 데이터 생산자와 소비자 간의 데이터 형식을 강제하고 버전 충돌을 원천 차단할 수 있습니다.
- **기술사적 판단:** 직렬화 포맷 선택은 '성능'과 '유연성'의 트레이드오프입니다. 하둡 기반의 데이터 파이프라인이라면 생태계 호환성이 높은 Avro를, 고성능 실시간 통신이 중심이라면 gRPC와 결합된 Protobuf를 선택하는 것이 기술사적 통찰에 기반한 정석적인 판단입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
데이터 직렬화는 단순한 포맷 변환을 넘어 클라우드 네이티브 환경의 상호운용성(Interoperability)을 보장하는 규격입니다. 향후 양자 컴퓨팅이나 초고속 네트워크 환경에서도 데이터의 본질적 정보를 가장 효율적으로 압축하여 전달하는 직렬화 기술은 분산 시스템 아키텍처의 뿌리로 남을 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Distributed Computing, Data Format
- **하위 개념:** IDL, Schema Evolution, Binary Encoding
- **연관 기술:** gRPC, Apache Kafka, Parquet (Storage), ORC

### 👶 어린이를 위한 3줄 비유 설명
1. 이삿짐을 쌀 때 가구를 다 분해해서 상자에 꽉꽉 채워 담는 것이 '직렬화'예요.
2. 새집에 도착해서 상자를 열고 가구를 다시 조립하는 것이 '역직렬화'랍니다.
3. 설명서(스키마)가 잘 되어 있으면 어떤 가구든 작게 줄여서 안전하게 옮길 수 있겠죠?
