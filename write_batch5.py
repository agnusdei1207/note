import os
BASE = "/Users/pf/workspace/brainscience/content/studynote/07_enterprise_systems/05_data_bi"
def w(fn, txt):
    path = os.path.join(BASE, fn)
    if os.path.exists(path): print(f"SKIP: {fn}"); return
    with open(path, 'w', encoding='utf-8') as f: f.write(txt)
    print(f"OK: {fn}")

w("309_influxdb_downsampling.md", """\
+++
weight = 309
title = "309. 시계열 데이터베이스 InfluxDB 다운샘플링 롤업 (Time-Series DB Downsampling)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 시계열 DB의 다운샘플링(Downsampling)은 고해상도 데이터를 시간 경과에 따라 자동으로 저해상도로 롤업하여 스토리지를 최대 99.97%까지 절감한다.
> 2. **가치**: 1초 단위 원시 데이터를 무기한 보관하면 연간 TB~PB 급 스토리지가 필요하지만, 다운샘플링으로 실제 비용 지출을 1%대로 압축할 수 있다.
> 3. **판단 포인트**: 롤업 후 원시 데이터는 삭제되므로, 어느 시간 해상도까지 보존할지를 사전에 비즈니스 요구사항과 함께 결정해야 한다.

## Ⅰ. 개요 및 필요성

IoT 센서, 서버 메트릭, 금융 시세 데이터는 초당 수천~수백만 건의 데이터 포인트를 생성한다.
이 데이터를 모두 원시 형태로 무기한 보관하면 스토리지 비용이 폭발적으로 증가한다.

InfluxDB는 시계열 전용 TSDB (Time-Series Database)로, 리텐션 정책(Retention Policy)과 연속 쿼리(Continuous Query) 또는 Task(InfluxDB 2.x)를 통해 자동 다운샘플링을 지원한다.

스토리지 절감 계산:
- 1초 데이터 1일 = 86,400 포인트 (100%)
- 1분 롤업 1일 = 1,440 포인트 (절감 98.3%, 1.7% 남음)
- 1시간 롤업 1일 = 24 포인트 (절감 99.97%, 0.03% 남음)

📢 **섹션 요약 비유**: 다운샘플링은 사진 원본을 수년 후 썸네일로 압축 저장하는 것이다. 오래될수록 해상도는 낮아지지만 공간은 훨씬 절약된다.

## Ⅱ. 아키텍처 및 핵심 원리

### InfluxDB 핵심 개념

| 개념 | 설명 | 예시 |
|:---|:---|:---|
| Measurement | 테이블에 해당 | cpu_usage |
| Tag | 인덱스되는 메타데이터 (String) | host=server01 |
| Field | 실제 측정값 (Number) | value=82.5 |
| Timestamp | 나노초 정밀도 | 2024-01-15T12:00:00Z |
| Retention Policy | 데이터 보관 기간 | 30d, INF |
| Continuous Query | 자동 집계 작업 | MEAN 1분 롤업 |

### Tag vs Field 설계 원칙

- **Tag** (인덱싱됨): 자주 필터링하는 저카디널리티 값 (host, region, env)
- **Field** (비인덱싱): 측정 수치 (CPU%, 온도, 응답시간)
- 고카디널리티 값을 Tag로 쓰면 인덱스 폭발 → DB 성능 급락

### ASCII 다이어그램: 데이터 보존 계층 (Retention Tier)

```
  실시간 수집 (초당 수천 포인트)
        │
        ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  Tier 1: Raw (1초 해상도)                                    │
  │  보관: 30일  스토리지: 100%  용도: 실시간 모니터링·알람       │
  └───────────────────────────┬──────────────────────────────────┘
                              │ Continuous Query: MEAN(value) 1분
                              ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  Tier 2: 1분 롤업                                            │
  │  보관: 1년   스토리지: 1.7%  용도: 일간 트렌드·용량 계획     │
  └───────────────────────────┬──────────────────────────────────┘
                              │ Continuous Query: MEAN(value) 1시간
                              ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  Tier 3: 1시간 롤업                                          │
  │  보관: 5년+  스토리지: 0.03%  용도: 연간 리포트·장기 분석    │
  └──────────────────────────────────────────────────────────────┘
```

### TSM 스토리지 엔진 (Time-Structured Merge Tree)

InfluxDB는 LSM (Log-Structured Merge Tree) 변형인 TSM 엔진을 사용한다.
- WAL (Write-Ahead Log) → 인메모리 Cache → TSM 파일 → Compaction
- 시계열 특성상 쓰기는 항상 최신 타임스탬프 → 압축 효율 극대화

| TSDB 비교 | InfluxDB | TimescaleDB | Prometheus |
|:---|:---|:---|:---|
| 기반 | 전용 TSM | PostgreSQL 확장 | 자체 TSDB |
| 쿼리 언어 | Flux/InfluxQL | SQL | PromQL |
| 주요 용도 | IoT, 메트릭 | 금융, 이벤트 | K8s 모니터링 |

📢 **섹션 요약 비유**: TSM 엔진은 날짜별로 자동 정리되는 일기장이다. 새 내용은 날짜 순서대로 추가되고, 오래된 페이지는 자동으로 요약·압축된다.

## Ⅲ. 비교 및 연결

### 시계열 DB 활용 패턴

| 패턴 | 도구 선택 | 이유 |
|:---|:---|:---|
| Kubernetes 메트릭 | Prometheus | PromQL 생태계, Alert 통합 |
| IoT 장비 데이터 | InfluxDB | 고쓰기 처리량, 다운샘플링 |
| 금융 시계열 분석 | TimescaleDB | SQL 쿼리, 복잡 JOIN |

📢 **섹션 요약 비유**: Prometheus는 단거리 달리기 선수(짧은 보관, 빠른 조회), InfluxDB는 중거리 선수(중기 보관, 다운샘플링), TimescaleDB는 마라톤 선수(장기 보관, SQL 분석)다.

## Ⅳ. 실무 적용 및 기술사 판단

### 다운샘플링 설계 체크리스트

- [ ] 데이터 소스별 수집 빈도 파악 (초당 포인트 수)
- [ ] 비즈니스별 최소 필요 해상도 정의 (알람: 1초, 트렌드: 1분, 리포트: 1시간)
- [ ] 롤업 집계 함수 선정: MEAN, MAX, MIN, SUM
- [ ] 원시 데이터 보관 기간 결정 (스토리지 비용과 분석 요구 균형)
- [ ] 고카디널리티 Tag 사용 금지 (UUID, 사용자 ID는 Field로)

### 안티패턴

| 안티패턴 | 문제 | 해결 방법 |
|:---|:---|:---|
| 모든 데이터 무기한 보관 | 스토리지 폭발, 성능 저하 | Retention Policy 필수 설계 |
| UUID를 Tag로 사용 | 카디널리티 폭발 → DB 메모리 부족 | Field로 변경 |
| 단일 Measurement에 모든 메트릭 | 태그 조합 폭발 | 도메인별 Measurement 분리 |

📢 **섹션 요약 비유**: 고카디널리티 Tag는 도서관에서 책마다 새 서가를 만드는 것이다. 서가가 폭발해 도서관이 무너진다.

## Ⅴ. 기대효과 및 결론

| 항목 | 다운샘플링 미적용 | 적용 후 |
|:---|:---|:---|
| 스토리지 (1년) | 100% | 1초→1분: 1.7%, 1초→1시간: 0.03% |
| 장기 쿼리 속도 | 수분 (수억 행 스캔) | 수초 (소량 롤업 데이터) |
| 인프라 비용 | 매월 증가 | 예측 가능한 고정 비용 |

📢 **섹션 요약 비유**: 다운샘플링 후 원시 데이터 삭제는 음식을 냉동 건조하는 것이다. 공간은 극적으로 줄지만 원래 맛(세밀한 분석)을 완전히 재현하기는 어렵다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| InfluxDB | 플랫폼 | 시계열 전용 TSDB |
| Retention Policy | 핵심 설정 | 데이터 보관 기간 정책 |
| Continuous Query | 핵심 기능 | 자동 집계·롤업 |
| TSM Engine | 저장 엔진 | 시계열 최적화 저장 구조 |
| Tag vs Field | 설계 원칙 | 인덱스 폭발 방지 |

### 👶 어린이를 위한 3줄 비유 설명

1. 시계열 DB는 매초 사진을 찍는 카메라예요. 오래된 사진은 자동으로 작은 썸네일로 압축돼요.
2. 다운샘플링은 1분치 사진 60장을 1장의 평균 사진으로 만드는 거예요.
3. Tag는 서랍 라벨, Field는 서랍 안 물건이에요. 라벨이 너무 많으면 서랍장이 꽉 차서 못 열어요.
""")

w("310_neo4j_fraud_detection.md", """\
+++
weight = 310
title = "310. 그래프 데이터베이스 Neo4j 사기 탐지 최단 경로 (Neo4j Fraud Detection)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 그래프 DB는 관계(엣지)가 1등 시민인 구조로, SQL의 다중 JOIN이 필요한 관계 탐색을 단일 그래프 순회로 처리해 수십~수백 배 빠른 성능을 달성한다.
> 2. **가치**: 사기 탐지에서 공유 전화번호·주소·디바이스로 연결된 사기 링(Ring) 패턴은 SQL로는 수분이 걸리지만, Neo4j 2-hop 분석으로 수십 ms 내에 탐지된다.
> 3. **판단 포인트**: 4-hop 이상 관계 탐색은 그래프 DB가 압도적이지만, 대량 집계 분석(SUM, GROUP BY)은 여전히 관계형 DB나 컬럼 스토어가 유리하다.

## Ⅰ. 개요 및 필요성

전통 관계형 DB에서 "이 계정과 3단계 이내 연결된 모든 계정 찾기"는 복잡한 자기참조 JOIN이 필요하고 데이터 규모에 따라 지수적으로 느려진다.

그래프 DB는 노드(Node)와 엣지(Edge·Relationship)로 데이터를 표현하며, 관계를 포인터처럼 직접 따라가므로 JOIN 없이 관계 탐색이 가능하다.

Neo4j는 세계 1위 그래프 DB로 Cypher 쿼리 언어와 네이티브 그래프 처리 엔진을 제공한다.

주요 활용 사례:
- 금융 사기 탐지: 공유 연락처·주소 기반 링 탐지
- 추천 시스템: 협업 필터링 (공통 구매 패턴)
- 지식 그래프: 엔티티 간 관계 탐색
- 네트워크 보안: 침해 경로 분석

📢 **섹션 요약 비유**: 그래프 DB는 관계를 직접 연결한 거미줄이다. 한 점에서 줄을 따라가면 연결된 모든 점에 즉시 도달한다.

## Ⅱ. 아키텍처 및 핵심 원리

### Neo4j 핵심 개념

| 개념 | 설명 | 예시 |
|:---|:---|:---|
| Node | 엔티티 | (:Person {name: "Kim"}) |
| Relationship | 방향성 있는 엣지 | -[:OWNS]->, -[:CALLED]-> |
| Label | 노드 타입 분류 | :Person, :Account, :Phone |
| Property | 노드/엣지 속성 | {amount: 50000} |
| Cypher | 쿼리 언어 | MATCH, WHERE, RETURN |

### Cypher 사기 탐지 쿼리

```cypher
MATCH (suspect:Account)-[:REGISTERED_WITH]->(phone:Phone)
      <-[:REGISTERED_WITH]-(other:Account)
WHERE suspect.flagged = true
  AND other.id <> suspect.id
RETURN other.id, other.name, phone.number
ORDER BY other.created_at DESC
LIMIT 100
```

### ASCII 다이어그램: 사기 링 탐지 그래프

```
  ┌───────────────────────────────────────────────────────────────┐
  │                    사기 링 탐지 그래프                         │
  │                                                               │
  │    [Account A]────REGISTERED_WITH────[Phone: 010-1234-5678]  │
  │         │                                       │            │
  │    TRANS_TO                           REGISTERED_WITH        │
  │         │                                       │            │
  │    [Account B]                        [Account C] ★의심      │
  │         │                                       │            │
  │    REGISTERED_WITH                SHARES_ADDRESS             │
  │         │                                       │            │
  │    [Email: x@fake.com]            [Address: 서울 강남구]       │
  │         │                                       │            │
  │    REGISTERED_WITH                    REGISTERED_WITH        │
  │         │                                       │            │
  │    [Account D] ★의심              [Account E] ★의심           │
  │                                                               │
  │  → A-B-C-D-E가 공유 식별자로 연결된 사기 링 (Ring)             │
  │  → 4-hop: SQL JOIN 12개 vs Neo4j Cypher 단일 쿼리             │
  └───────────────────────────────────────────────────────────────┘
```

### 그래프 알고리즘 비교

| 알고리즘 | 사용 사례 | 복잡도 |
|:---|:---|:---|
| Dijkstra (최단 경로) | 네트워크 라우팅 | O(V log V + E) |
| BFS (너비 우선 탐색) | N-hop 연결 탐색 | O(V + E) |
| PageRank | 영향력 있는 노드 식별 | 반복 수렴 |
| Community Detection | 군집 분석 (Louvain) | O(n log n) |

📢 **섹션 요약 비유**: 사기 링 탐지는 동일 은행 계좌를 여러 이름으로 쓰는 사람을 전화번호부에서 공통 번호로 찾는 것이다.

## Ⅲ. 비교 및 연결

### Neo4j vs SQL JOIN (관계 탐색 성능)

| 항목 | SQL JOIN | Neo4j Cypher |
|:---|:---|:---|
| 2-hop 탐색 | 빠름 | 빠름 |
| 4-hop 탐색 | 느림 (중간 임시 테이블) | 빠름 (포인터 직접 추적) |
| 6-hop 탐색 | 매우 느림 (수분) | 수십ms |
| 집계 분석 | 빠름 | 느림 |

📢 **섹션 요약 비유**: SQL JOIN은 주소록 전체를 복사해 공통 주소를 찾는 것, 그래프 DB는 지도에서 연결선을 따라가는 것이다.

## Ⅳ. 실무 적용 및 기술사 판단

### 그래프 DB 도입 체크리스트

- [ ] 쿼리 패턴이 관계 중심 탐색인가? (3-hop 이상이면 도입 강력 권장)
- [ ] 슈퍼노드 존재 여부 확인 (수백만 관계 가진 노드 성능 문제)
- [ ] Neo4j Community(단일 서버) vs Enterprise(클러스터) 선택
- [ ] 기존 RDB와 병행: OLTP는 RDB, 관계 탐색은 Neo4j 이중 저장

### 안티패턴

| 안티패턴 | 문제 | 해결 방법 |
|:---|:---|:---|
| 슈퍼노드 (Super Node) | 수백만 관계 → 탐색 급격 저하 | 관계 유형 분리, 시간 범위 제한 |
| 그래프를 집계 DB로 사용 | SUM, GROUP BY 성능 최악 | 집계는 별도 DW 사용 |
| 단순 key-value 조회에 그래프 | 과도한 복잡성 | Redis나 RDB로 충분 |

📢 **섹션 요약 비유**: 슈퍼노드는 모든 사람이 연결된 허브 공항이다. 허브 경유 경로 탐색이 폭발적으로 느려진다.

## Ⅴ. 기대효과 및 결론

| 항목 | SQL | Neo4j |
|:---|:---|:---|
| 4-hop 관계 탐색 | 수분~수십분 | 수십ms |
| 사기 링 탐지율 | 30~50% | 70~90% (숨겨진 관계 발견) |
| 스키마 변경 비용 | 높음 (ALTER TABLE) | 낮음 (노드/관계 타입 추가) |

📢 **섹션 요약 비유**: Neo4j는 관계의 달인이다. 관계 탐색은 1등이지만, 숫자 계산(집계)은 엑셀(관계형 DB)이 더 빠르다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Neo4j | 플랫폼 | 네이티브 그래프 DB |
| Cypher | 쿼리 언어 | 그래프 패턴 매칭 쿼리 |
| Node/Relationship | 데이터 구조 | 엔티티와 관계 |
| Shortest Path | 알고리즘 | Dijkstra, BFS |
| Fraud Ring | 적용 사례 | 사기 링 탐지 |
| Super Node | 성능 문제 | 수백만 관계 단일 노드 |

### 👶 어린이를 위한 3줄 비유 설명

1. 그래프 DB는 친구 관계 지도예요. "나→친구→친구의 친구"를 줄을 따라 즉시 찾을 수 있어요.
2. 사기 링 탐지는 같은 전화번호를 여러 계정이 쓰는 걸 찾는 거예요.
3. SQL은 전화번호부 전체를 비교해야 하지만, 그래프 DB는 줄을 따라가기만 하면 돼요.
""")

w("311_parquet_orc_rle_compression.md", """\
+++
weight = 311
title = "311. 컬럼 지향 저장소 Parquet ORC 압축 효율 RLE 메커니즘 (Columnar Storage Compression)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 컬럼 지향 저장(Parquet, ORC)은 동일 컬럼 값을 연속 저장해 RLE (Run-Length Encoding)와 사전 인코딩이 극적인 압축 효율(10배 이상)을 달성한다.
> 2. **가치**: Predicate Pushdown과 Column Pruning으로 필요한 컬럼·행만 I/O해 Spark/Hive 쿼리 비용을 최대 90%까지 절감한다.
> 3. **판단 포인트**: 행 삽입·수정이 잦은 OLTP는 여전히 행 지향 저장이 적합하고, Parquet/ORC는 읽기 집중 OLAP/빅데이터 분석에 최적화된다.

## Ⅰ. 개요 및 필요성

전통 행 지향 저장(Row-based)은 한 행의 모든 컬럼을 연속 저장해 레코드 삽입·수정에 유리하다.
반면 분석 쿼리는 수백 개 컬럼 중 3~5개만 읽는 경우가 대부분이므로, 불필요한 컬럼까지 모두 읽는 I/O 낭비가 발생한다.

컬럼 지향 저장(Columnar Storage)은 동일 컬럼 값을 연속 배치해:
1. 필요한 컬럼만 선택적으로 읽는 Column Pruning 가능
2. 같은 타입 값이 연속되어 압축 효율 극대화
3. Predicate Pushdown으로 파일 수준에서 스캔 대상 행 그룹 제외

Apache Parquet (Cloudera+Twitter 개발)와 Apache ORC (Hive 최적화)가 양대 표준이다.

📢 **섹션 요약 비유**: 컬럼 저장은 같은 색 구슬을 한 통에 모아 담는 것이다. "빨간 구슬만 주세요"라는 요청에 빨간 통만 열면 된다.

## Ⅱ. 아키텍처 및 핵심 원리

### RLE (Run-Length Encoding) 메커니즘

```
원본: [A, A, A, A, B, B, C, C, C, C, C]  (11 bytes)
RLE:  [(A,4), (B,2), (C,5)]              (3 pairs → 73% 압축)
```

저카디널리티 컬럼(성별: M/F, 상태: ACTIVE/INACTIVE)에서 효율 극대화.

사전 인코딩 (Dictionary Encoding):
```
원본: ["Seoul", "Seoul", "Busan", "Seoul", "Daegu"]
사전: {Seoul:0, Busan:1, Daegu:2}
인코딩: [0, 0, 1, 0, 2]  (int 저장 = 4~8배 절감)
```

### 압축 코덱 비교

| 코덱 | 압축비 | 압축 속도 | 압축 해제 속도 | 적합 용도 |
|:---|:---|:---|:---|:---|
| Snappy | 2~3x | 매우 빠름 | 매우 빠름 | 스트리밍, 중간 결과 |
| ZSTD | 4~7x | 빠름 | 빠름 | 프로덕션 장기 보관 |
| GZIP | 5~8x | 느림 | 중간 | 아카이브 |
| LZ4 | 2~3x | 초고속 | 초고속 | 실시간 처리 |

### ASCII 다이어그램: 행 지향 vs 컬럼 지향 저장 레이아웃

```
  행 지향 저장 (Row-based: CSV, JSON)
  ┌────────────────────────────────────────────────────────────┐
  │ Row1: [id=1, name="Kim", age=30, city="Seoul", sal=5000]  │
  │ Row2: [id=2, name="Lee", age=25, city="Busan", sal=4500]  │
  │ Row3: [id=3, name="Park",age=35, city="Seoul", sal=6000]  │
  └────────────────────────────────────────────────────────────┘
  → "age 평균" 쿼리 시 불필요한 name, city, salary도 모두 읽음

  컬럼 지향 저장 (Parquet / ORC)
  ┌─────────┬────────────────┬───────────┬──────────┬──────────┐
  │ id 컬럼 │   name 컬럼    │ age 컬럼  │city 컬럼 │ sal 컬럼 │
  │ [1,2,3] │["Kim","Lee",..]│[30,25,35] │[S,B,S]   │[5000,...] │
  │ RLE/Dict│ Dict Encoding  │ Delta     │ RLE      │ Delta    │
  └─────────┴────────────────┴───────────┴──────────┴──────────┘
  → "age 평균" 쿼리 시 age 컬럼만 읽음 (I/O 80% 절감)
```

### Parquet Row Group vs ORC Stripe

| 항목 | Parquet | ORC |
|:---|:---|:---|
| 데이터 블록 단위 | Row Group (기본 128MB) | Stripe (기본 64MB) |
| 통계 저장 | Page Header (min/max) | Stripe Footer |
| 최적화 대상 | Spark, Flink, Presto | Hive, ORC-vectorized |

📢 **섹션 요약 비유**: Parquet Row Group은 챕터별로 정리된 책이다. 원하는 챕터(Row Group)만 열면 필요 없는 다른 챕터는 읽지 않아도 된다.

## Ⅲ. 비교 및 연결

### 컬럼 저장 vs 행 저장 사용 기준

| 기준 | 행 저장 (CSV, Avro) | 컬럼 저장 (Parquet, ORC) |
|:---|:---|:---|
| 워크로드 | INSERT/UPDATE 집중 | SELECT/SCAN 집중 |
| 조회 패턴 | 전체 컬럼 필요 | 일부 컬럼만 필요 |
| 데이터 규모 | 수GB 이하 | 수TB 이상 |

📢 **섹션 요약 비유**: 행 저장은 손님 한 명의 모든 정보를 한 카드에, 컬럼 저장은 "나이" 정보만 따로 모아둔 서랍이다.

## Ⅳ. 실무 적용 및 기술사 판단

### Parquet 최적화 체크리스트

- [ ] Row Group 크기: 128MB (기본값) 유지
- [ ] 코덱 선택: 읽기 성능 우선이면 Snappy, 저장 비용 우선이면 ZSTD
- [ ] 파티셔닝 컬럼: 날짜·카테고리 등 저카디널리티
- [ ] Column Stats 수집: min/max 통계로 Predicate Pushdown 극대화
- [ ] 파티션당 최소 128MB 이상 권장 (Small File 문제 방지)

### 안티패턴

| 안티패턴 | 문제 | 해결 방법 |
|:---|:---|:---|
| 고카디널리티 파티셔닝 | 수백만 파티션 → 메타데이터 폭발 | 날짜·카테고리 등으로 제한 |
| GZIP on Spark | 병렬 압축 해제 불가 → 성능 저하 | Snappy 또는 ZSTD 권장 |

📢 **섹션 요약 비유**: 고카디널리티 파티셔닝은 사람마다 서랍을 만드는 것이다. 서랍이 백만 개가 되면 서랍장 자체가 무너진다.

## Ⅴ. 기대효과 및 결론

| 항목 | CSV (행 저장) | Parquet (컬럼 저장) |
|:---|:---|:---|
| 스토리지 | 100% | 10~30% (10배 압축) |
| 컬럼 선택 쿼리 I/O | 100% | 10~20% (Column Pruning) |
| Spark 쿼리 비용 | 기준 | 70~90% 절감 |

📢 **섹션 요약 비유**: Parquet는 분석 쿼리를 위한 전용 창고다. 창고 정리에 시간이 들지만, 필요한 물건을 찾는 속도가 10배 빠르다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Parquet | 포맷 | 컬럼 지향 오픈소스 포맷 |
| ORC | 포맷 | Hive 최적화 컬럼 포맷 |
| RLE | 압축 기법 | 반복값 (값, 횟수) 압축 |
| Predicate Pushdown | 최적화 | 파일 수준 조건 필터링 |
| Column Pruning | 최적화 | 필요 컬럼만 I/O |
| Row Group | 구조 단위 | Parquet 데이터 블록 128MB |

### 👶 어린이를 위한 3줄 비유 설명

1. Parquet는 색깔별로 구슬을 통에 모아 담은 것이에요. 빨간 구슬만 필요하면 빨간 통만 열어요.
2. RLE는 "빨강 100개"를 "빨강×100"으로 짧게 쓰는 방법이에요.
3. Predicate Pushdown은 "서울 사람만 필요해"라고 미리 말하면 서울 통만 열어주는 스마트 창고 직원이에요.
""")

print("309~311 완료")
