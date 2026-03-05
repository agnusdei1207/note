+++
title = "CDC (Change Data Capture)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# CDC (Change Data Capture)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CDC는 데이터베이스의 변경 사항(Insert, Update, Delete)을 실시간으로 감지하여 캡처하는 기술로, 운영 DB의 트랜잭션 로그를 읽어 변경 데이터를 추출합니다.
> 2. **가치**: 운영 DB에 부하를 주지 않고 실시간 데이터 동기화가 가능하며, 데이터 웨어하우스, 검색 엔진, 캐시 등의 실시간 업데이트에 활용됩니다.
> 3. **융합**: Debezium이 대표적인 오픈소스 CDC 도구이며, 카프카와 결합하여 실시간 데이터 파이프라인의 핵심 기술입니다.

---

### Ⅰ. 개요

#### 1. CDC 방식

| 방식 | 설명 | 장단점 |
|:---|:---|:---|
| **로그 기반** | DB 트랜잭션 로그 읽기 | 실시간, 저지연 |
| **트리거 기반** | DB 트리거로 변경 감지 | 높은 부하 |
| **타임스탬프 기반** | Updated_at 컬럼 폴링 | 지연 발생 |

---

### Ⅱ. 아키텍처

```text
[Source DB] → [CDC Tool] → [Kafka] → [Target]
    |              |
    +-- Binlog ----+
    (MySQL)
    +-- WAL -------+
    (PostgreSQL)
```

---

### Ⅲ. Debezium 예시

```yaml
# Debezium Connector 설정
{
  "name": "mysql-connector",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "mysql",
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "password",
    "database.server.id": "1",
    "database.server.name": "dbserver1",
    "database.include.list": "inventory",
    "database.history.kafka.bootstrap.servers": "kafka:9092"
  }
}
```

---

### Ⅳ. 활용 사례

- 실시간 DW 동기화
- 검색 인덱스 갱신
- 캐시 무효화
- 이벤트 소싱

---

### Ⅴ. 결론

CDC는 실시간 데이터 동기화의 핵심 기술이며, 현대 데이터 아키텍처에서 필수적입니다.

---

### 관련 개념 맵
- **[Apache Kafka](@/studynotes/14_data_engineering/03_pipelines/apache_kafka.md)**
- **[ETL vs ELT](@/studynotes/14_data_engineering/03_pipelines/etl_vs_elt.md)**

---

### 어린이를 위한 3줄 비유
1. **변화 감지 카메라**: 방에 무언가 움직이면 카메라가 찍어요.
2. **바로 알림**: 무슨 일이 일어났는지 바로 알려줘요.
3. **기록 남기기**: 누가 언제 무엇을 했는지 다 적어둬요!
