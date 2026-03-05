+++
title = "CDC (Change Data Capture)"
date = 2026-03-05
description = "데이터베이스의 변경 사항을 실시간으로 캡처하여 데이터 웨어하우스, 검색 엔진, 캐시 등으로 동기화하는 데이터 통합 기술 심층 분석"
weight = 233
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["CDC", "Change-Data-Capture", "Debezium", "Binlog", "Event-Streaming", "Data-Integration"]
+++

# CDC (Change Data Capture) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CDC는 데이터베이스의 트랜잭션 로그(Redo Log, Binlog, WAL)를 실시간으로 읽어 INSERT/UPDATE/DELETE 변경 이벤트를 캡처하고, 이를 메시지 큐(Kafka)로 전파하여 다운스트림 시스템으로 데이터를 동기화하는 기술입니다.
> 2. **가치**: 기존 ETL의 **배치 지연(수시간~수일)**을 **초 단위 실시간**으로 단축하고, 소스 DB에 **부하 없이(Zero-overhead)** 데이터를 복제하여 마이크로서비스 간 데이터 일관성과 이벤트 소싱을 실현합니다.
> 3. **융합**: Debezium/Kafka Connect, 이벤트 소싱, CQRS, 데이터 레이크하우스(Delta Lake/Iceberg), 검색 엔진 동기화(Elasticsearch), 캐시 무효화(Redis)와 결합하여 실시간 데이터 파이프라인의 핵심 기술이 됩니다.

---

## Ⅰ. 개요 (Context & Background)

CDC(Change Data Capture)는 데이터베이스의 변경 사항을 실시간으로 감지하고 캡처하는 기술입니다. 전통적인 ETL은 주기적으로 전체 데이터를 읽어오는 '풀(Pull)' 방식이지만, CDC는 변경된 데이터만 실시간으로 '푸시(Push)' 받습니다. 이는 데이터 복제, 검색 인덱스 동기화, 캐시 무효화, 이벤트 기반 아키텍처의 핵심 기술입니다.

**💡 비유**: CDC는 **'우편물 포워딩 서비스'**와 같습니다. 이사를 가면 우체국에 주소 변경을 신청합니다. 그러면 우체국(트랜잭션 로그)은 새 주소로 오는 모든 우편물(변경 이벤트)을 자동으로 새 집(다운스트림 시스템)으로 전달합니다. 매일 우편물을 직접 확인하러 가지 않아도 됩니다.

**등장 배경 및 발전 과정**:
1. **ETL의 한계**: 전통적 ETL은 배치 처리로 인해 데이터가 최신이 아닙니다. 어제 밤에 실행된 ETL이라면 오늘 낮의 데이터는 반영되지 않습니다.
2. **데이터베이스 복제 기술의 진화**: Oracle GoldenGate, Attunity 등 상용 솔루션이 먼저 존재했으나, 오픈소스인 Debezium이 2016년 출시되면서 대중화되었습니다.
3. **이벤트 기반 아키텍처**: 마이크로서비스 간 데이터 동기화를 위해 이벤트가 필요해졌고, DB 변경 이벤트를 자동으로 생성하는 CDC가 주목받았습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### CDC 구현 방식 비교

| 방식 | 원리 | 장점 | 단점 | 대표 도구 |
|---|---|---|---|---|
| **로그 기반 (Log-based)** | 트랜잭션 로그 직접 읽기 | Zero-overhead, 모든 변경 캡처 | DB별 구현 상이 | Debezium, Oracle GoldenGate |
| **트리거 기반 (Trigger-based)** | DB 트리거로 변경 감지 | 범용적 | 성능 저하, 트리거 관리 |自定义 구현 |
| **타임스탬프 기반 (Timestamp-based)** | updated_at 컬럼 폴링 | 단순 구현 | 삭제 감지 불가, 폴링 부하 | Airbyte (일부 모드) |
| **쿼리 기반 (Query-based)** | 정기적으로 스냅샷 비교 | DB 독립적 | 높은 부하, 지연 | 기본 JDBC 소스 |

### CDC 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 기술 스택 예시 | 특성 |
|---|---|---|---|
| **Source Connector** | DB 로그 읽기 및 이벤트 생성 | Debezium MySQL/PostgreSQL Connector | DB별 구현 |
| **Transaction Log** | 변경 사항 기록 로그 | Binlog(MySQL), WAL(PostgreSQL), Redo Log(Oracle) | 순차 Append |
| **Message Broker** | 이벤트 스트림 저장 및 전파 | Apache Kafka, Pulsar, Kinesis | 고처리량, 내구성 |
| **Sink Connector** | 이벤트를 타겟 시스템에 적용 | Kafka Connect (JDBC, Elasticsearch, S3) | Exactly-once 지원 |
| **Schema Registry** | 이벤트 스키마 관리 | Confluent Schema Registry, Apicurio | 버전 관리, 호환성 |

### 정교한 구조 다이어그램: CDC 파이프라인

```ascii
================================================================================
                    CDC ARCHITECTURE (Debezium + Kafka)
================================================================================

    +-------------------+     +-------------------+     +-------------------+
    |   MySQL (Source)  |     |  PostgreSQL       |     |   MongoDB         |
    |                   |     |  (Source)         |     |   (Source)        |
    |  +-------------+  |     |  +-------------+  |     |  +-------------+  |
    |  | orders      |  |     |  | customers   |  |     |  | products    |  |
    |  | users       |  |     |  | addresses   |  |     |  | reviews     |  |
    |  | products    |  |     |  +------+------+  |     |  +------+------+  |
    |  +------+------+  |     |         |         |     |         |         |
    |         |         |     |         | WAL     |     |         | Oplog   |
    |         | Binlog  |     |         v         |     |         v         |
    |         v         |     |  +------+------+  |     |  +------+------+  |
    |  +-------------+  |     |  | WAL Files  |  |     |  | Oplog       |  |
    |  | Binlog Files|  |     |  +------+------+  |     |  +------+------+  |
    |  +------+------+  |     |         |         |     |         |         |
    +---------+---------+     +---------+---------+     +---------+---------+
              |                         |                         |
              | Read Binary Log         | Read WAL                | Read Oplog
              v                         v                         v
    +---------+-------------------------------------------------------------+
    |                    Kafka Connect (Distributed Mode)                  |
    |                                                                       |
    |  +------------------+  +------------------+  +------------------+    |
    |  | Debezium MySQL   |  | Debezium PG      |  | Debezium MongoDB |    |
    |  | Source Connector |  | Source Connector |  | Source Connector |    |
    |  +--------+---------+  +--------+---------+  +--------+---------+    |
    |           |                     |                     |              |
    +-----------+---------------------+---------------------+--------------+
                |                     |                     |
                v                     v                     v
    +-----------------------------------------------------------------------+
    |                         Apache Kafka Cluster                           |
    |                                                                         |
    |  Topics:                                                                |
    |  +-----------------+  +-----------------+  +-----------------+         |
    |  | db1.orders      |  | db2.customers   |  | db3.products    |         |
    |  | Partition: 6    |  | Partition: 3    |  | Partition: 3    |         |
    |  | Replication: 3  |  | Replication: 3  |  | Replication: 3  |         |
    |  +--------+--------+  +--------+--------+  +--------+--------+         |
    |           |                    |                    |                  |
    +-----------+--------------------+--------------------+------------------+
                |                    |                    |
                v                    v                    v
    +-----------------------------------------------------------------------+
    |                    Kafka Connect (Sink Connectors)                     |
    |                                                                        |
    |  +----------------+  +----------------+  +----------------+           |
    |  | Elasticsearch  |  | Snowflake      |  | S3 (Data Lake) |           |
    |  | Sink Connector |  | Sink Connector |  | Sink Connector |           |
    |  +-------+--------+  +-------+--------+  +-------+--------+           |
    |          |                   |                   |                    |
    +----------+-------------------+-------------------+--------------------+
               |                   |                   |
               v                   v                   v
    +------------------+  +------------------+  +------------------+
    | Elasticsearch    |  | Snowflake        |  | S3 (Parquet)     |
    | (Search Index)   |  | (Data Warehouse) |  | (Data Lake)      |
    |                  |  |                  |  |                  |
    | orders_idx       |  | ORDERS           |  | /orders/         |
    | customers_idx    |  | CUSTOMERS        |  | /customers/      |
    | products_idx     |  | PRODUCTS         |  | /products/       |
    +------------------+  +------------------+  +------------------+

================================================================================
                    DEBEZIUM EVENT STRUCTURE (JSON)
================================================================================

{
  "schema": { ... },  // Avro/JSON Schema
  "payload": {
    "before": {                    // 변경 전 상태 (UPDATE/DELETE만)
      "id": 1001,
      "name": "Old Name",
      "email": "old@email.com",
      "status": "PENDING"
    },
    "after": {                     // 변경 후 상태 (INSERT/UPDATE만)
      "id": 1001,
      "name": "New Name",
      "email": "new@email.com",
      "status": "CONFIRMED"
    },
    "source": {                    // 이벤트 메타데이터
      "version": "2.0.0.Final",
      "connector": "mysql",
      "name": "db1",
      "ts_ms": 1709612400000,     // 이벤트 발생 시각
      "db": "mydb",
      "table": "orders",
      "server_id": 1,
      "binlog": "mysql-bin.000003",
      "pos": 12345,
      "row": 0
    },
    "op": "u",                     // 연산 타입: c=create, u=update, d=delete
    "ts_ms": 1709612401234         // Debezium 처리 시각
  }
}

================================================================================
                    CDC USE CASES
================================================================================

1. Search Index Sync     2. Cache Invalidation    3. Data Warehouse ETL
   (MySQL -> ES)            (MySQL -> Redis)          (MySQL -> Snowflake)

2. Event Sourcing       5. Audit Trail           6. Microservice Sync
   (All changes -> Event    (All changes ->           (DB -> Kafka ->
    Store)                   Immutable Log)            Other Services)
```

### 심층 동작 원리: Debezium MySQL Connector

Debezium MySQL Connector는 MySQL의 Binlog를 읽어 변경 이벤트를 생성합니다.

1. **Binlog 위치 확인**: Connector는 주기적으로 Binlog 위치를(offset) Kafka 토픽(`connect-offsets`)에 저장합니다.
2. **Binlog 스트리밍**: MySQL 서버에 복제 클라이언트로 연결하여 Binlog 이벤트를 수신합니다.
3. **이벤트 변환**: Binlog 이벤트(Row-based)를 Debezium JSON/Avro 형식으로 변환합니다.
4. **스키마 추적**: DDL 문을 감지하여 테이블 스키마 변경을 Schema Registry에 반영합니다.
5. **토픽 라우팅**: `database.server.name.table_name` 형식의 토픽으로 이벤트를 전송합니다.

### 핵심 코드: Debezium Connector 설정

```json
{
  "name": "mysql-connector",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "mysql",
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "dbz",
    "database.server.id": "184054",
    "database.server.name": "db1",
    "database.include.list": "mydb",
    "table.include.list": "mydb.orders,mydb.customers",
    "database.history.kafka.bootstrap.servers": "kafka:9092",
    "database.history.kafka.topic": "schema-changes.mydb",

    // 초기 스냅샷 설정
    "snapshot.mode": "initial",  // initial, schema_only, never

    // Binlog 위치 관리
    "offset.storage.topic": "connect-offsets",
    "offset.storage.partitions": 25,
    "offset.storage.replication.factor": 3,

    // 이벤트 포맷
    "key.converter": "io.confluent.connect.avro.AvroConverter",
    "key.converter.schema.registry.url": "http://schema-registry:8081",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter.schema.registry.url": "http://schema-registry:8081",

    // 고급 설정
    "include.schema.changes": "true",  // DDL 이벤트 포함
    "include.query": "false",          // SQL 문 포함 (보안)
    "decimal.handling.mode": "double", // DECIMAL 타입 처리
    "time.precision.mode": "connect"   // 시간 타입 정밀도
  }
}
```

### CDC와 트랜잭션 일관성

CDC는 소스 DB의 트랜잭션 경계를 보존합니다.

```java
// 소스 DB에서의 트랜잭션
BEGIN;
  INSERT INTO orders (id, customer_id) VALUES (1001, 500);
  UPDATE customers SET last_order = NOW() WHERE id = 500;
  INSERT INTO audit_log (action, table, record_id) VALUES ('INSERT', 'orders', 1001);
COMMIT;

// CDC 이벤트 (Kafka)
// 동일한 트랜잭션 ID로 그룹화되어 순차 전송
[
  { "op": "c", "table": "orders", "after": {"id": 1001}, "ts_ms": 1000, "txId": "tx-123" },
  { "op": "u", "table": "customers", "after": {"id": 500}, "ts_ms": 1000, "txId": "tx-123" },
  { "op": "c", "table": "audit_log", "after": {"record_id": 1001}, "ts_ms": 1000, "txId": "tx-123" }
]
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: CDC 도구

| 도구 | 지원 DB | 특징 | 배포 방식 | 라이선스 |
|---|---|---|---|---|
| **Debezium** | MySQL, PG, Oracle, SQL Server, MongoDB, Cassandra | 오픈소스, Kafka Connect 통합 | Kafka Connect | Apache 2.0 |
| **Oracle GoldenGate** | Oracle, DB2, SQL Server | 엔터프라이즈급, 고가용성 | 에이전트 | 상용 |
| **AWS DMS** | Aurora, RDS, S3, Redshift | 관리형, AWS 통합 | Managed Service | 종량제 |
| **Fivetran** | 300+ 소스 | SaaS, 관리형 | Managed Service | 종량제 |
| **Airbyte** | 300+ 소스 | 오픈소스, 커스텀 커넥터 | Self-hosted/Cloud | MIT |

### 과목 융합 관점 분석: 데이터베이스 및 네트워크 연계

- **데이터베이스(DB)와의 융합**: CDC는 DB의 **Write-Ahead Logging(WAL)** 메커니즘과 밀접하게 연동됩니다. MySQL Binlog, PostgreSQL WAL, Oracle Redo Log는 모두 ACID 트랜잭션을 보장하기 위한 로그이며, CDC는 이를 읽기 전용으로 접근합니다. 이는 소스 DB에 거의 **Zero-overhead**로 동작합니다.

- **네트워크(Network)와의 융합**: CDC 이벤트는 **Apache Kafka**를 통해 전파됩니다. Kafka의 **파티셔닝**은 테이블별 또는 프라이머리 키별로 이벤트 순서를 보장합니다. **Exactly-once 처리**를 위해 Kafka Transactions과 Consumer의 `isolation.level=read_committed` 설정이 필요합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 이커머스 실시간 검색 동기화

**문제 상황**: 상품 정보는 MySQL에 저장되지만, 검색은 Elasticsearch를 사용합니다. 상품 정보 변경 시 검색 결과가 즉시 반영되어야 합니다. 기존 배치 ETL은 1시간 지연이 발생합니다.

**기술사의 전략적 의사결정**:

1. **Debezium + Kafka + Elasticsearch Sink**:
   - MySQL Binlog → Debezium → Kafka → Elasticsearch Sink
   - 지연 시간: 1시간 → 1초 이내

2. **데이터 변환 로직**:
   - 상품명, 설명, 가격, 재고, 카테고리를 Elasticsearch 문서로 매핑
   - SMT(Single Message Transform)로 필드 선택적 전송

3. **에러 처리**:
   - 파싱 실패 시 Dead Letter Queue(DLQ)로 이동
   - 재시도 정책: 3회 후 DLQ

4. **모니터링**:
   - CDC Lag: 소스 DB 커밋 시각 vs Kafka 적재 시각
   - Sink Lag: Kafka vs Elasticsearch 반영 시각

### 도입 시 고려사항 체크리스트

- **기술적 고려사항**:
  - [ ] 소스 DB의 로그 보존 기간 (Binlog expiration)
  - [ ] 스키마 변경(DDL) 대응 전략
  - [ ] 초기 스냅샷 vs CDC 전환 시점
  - [ ] 대용량 테이블의 파티셔닝 전략

- **운영/보안적 고려사항**:
  - [ ] CDC 계정의 최소 권한 (REPLICATION SLAVE)
  - [ ] PII 데이터 마스킹 (Transform)
  - [ ] 네트워크 암호화 (TLS)
  - [ ] 감사 로그 보관

### 안티패턴 (Anti-patterns)

1. **CDC로 전체 데이터 복사**: CDC는 변경 데이터만 전송합니다. 초기 전체 데이터는 스냅샷으로 복사한 후 CDC로 전환해야 합니다.

2. **스키마 변경 무시**: 테이블에 컬럼이 추가되면 CDC 이벤트 스키마도 변경됩니다. Schema Registry와 호환성 정책을 설정해야 합니다.

3. **무제한 재시도**: Sink 실패 시 무한 재시도는 데이터 지연을 유발합니다. DLQ로 격리 후 수동 복구해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 배치 ETL | CDC | 개선율 |
|---|---|---|---|
| **데이터 지연** | 1~24시간 | 1~5초 | 99.9% 단축 |
| **소스 DB 부하** | 높음 (풀 스캔) | 낮음 (로그 읽기) | 90% 감소 |
| **데이터 일관성** | 배치 간 불일치 | 실시간 일치 | 완전 일치 |
| **개발 복잡도** | 중간 | 높음 (초기) | 러닝 커브 |
| **운영 비용** | 중간 | 높음 (Kafka) | 인프라 비용 |

### 미래 전망 및 진화 방향

1. **CDC SaaS**: Fivetran, Airbyte Cloud와 같은 완전 관리형 CDC 서비스가 확산되어, 인프라 운영 없이 CDC를 사용할 수 있습니다.

2. **Delta Lake / Iceberg 통합**: CDC 이벤트를 데이터 레이크하우스의 테이블 포맷으로 직접 적재하는 커넥터가 표준화되고 있습니다.

3. **Serverless CDC**: AWS DMS Serverless, Google Cloud Datastream과 같이 사용량 기반 과금의 서버리스 CDC가 등장하고 있습니다.

### ※ 참고 표준/가이드

- **Debezium Documentation**: 공식 CDC 구현 가이드
- **Kafka Connect Documentation**: 커넥터 개발 가이드
- **AWS DMS Best Practices**: 관리형 CDC 운영 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [이벤트 소싱 (Event Sourcing)](@/studynotes/13_cloud_architecture/01_native/event_sourcing.md) : CDC 이벤트를 상태 변경 이력으로 활용
- [CQRS](@/studynotes/13_cloud_architecture/01_native/cqrs.md) : CDC로 Read Model 동기화
- [Apache Kafka](@/studynotes/13_cloud_architecture/04_data_engineering/apache_kafka.md) : CDC 이벤트 전송 메시지 브로커
- [사가 패턴 (Saga Pattern)](@/studynotes/13_cloud_architecture/01_native/saga_pattern.md) : CDC로 이벤트 발행
- [데이터 레이크하우스](@/studynotes/13_cloud_architecture/04_data_engineering/data_lakehouse.md) : CDC로 실시간 데이터 적재

---

### 👶 어린이를 위한 3줄 비유 설명
1. CDC는 **'자동 알림 서비스'**와 같아요. 친구가 새 게시물을 올리면, 내가 직접 확인하러 가지 않아도 자동으로 알림이 와요.
2. 데이터베이스에서 무엇이 바뀌었는지(INSERT, UPDATE, DELETE) 자동으로 감시하고, 다른 곳(검색, 캐시)에 알려줘요.
3. 덕분에 데이터가 바뀌면 즉시 다른 곳에도 반영돼서, 항상 최신 정보를 볼 수 있어요!
