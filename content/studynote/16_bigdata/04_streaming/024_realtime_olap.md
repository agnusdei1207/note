+++
weight = 24
title = "24. 실시간 OLAP (Real-time OLAP) — Apache Druid/Pinot/ClickHouse"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)

- **본질**: 실시간 OLAP (Real-time OLAP, Online Analytical Processing)은 수 초 이내에 수십억 행에 대한 집계 쿼리를 응답하는 분석 데이터베이스로, 세그먼트 기반 컬럼형 저장소와 사전 집계(Pre-aggregation)·비트맵 인덱스·벡터화 실행을 결합하여 기존 데이터 웨어하우스보다 10~1000배 빠른 쿼리를 제공한다.
- **가치**: 전통적 DW(Redshift, BigQuery)가 수 분~수십 분 걸리는 "어제 데이터"를 분석하는 반면, 실시간 OLAP는 "방금 들어온 데이터"를 초 단위로 분석하여 실시간 대시보드·이상 감지·A/B 테스트 결과를 즉각 제공한다.
- **판단 포인트**: 세 시스템의 핵심 차이는 수집 모델이다. Apache Druid (세그먼트+사전집계, Kafka 직접 수집), Apache Pinot (StarTree 인덱스, Upsert 지원), ClickHouse (완전 컬럼형, SQL 호환성 최고)이며 용도와 쿼리 패턴에 따라 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1. 실시간 OLAP의 등장 배경

```
데이터 분석의 지연 시간 스펙트럼:
  전통 DW (Redshift/Snowflake):
    - 데이터 수집 지연: T+1일 (ETL 파이프라인)
    - 쿼리 응답: 수십 초~수 분
    - 적합 용도: 일간 리포트, BI

  실시간 OLAP (Druid/Pinot/ClickHouse):
    - 데이터 수집 지연: 초 단위 (Kafka 직접 수집)
    - 쿼리 응답: < 1초 (수십억 행 집계)
    - 적합 용도: 실시간 대시보드, A/B 테스트

실시간 OLAP가 필요한 순간:
  - "지금 이 순간 어느 지역에서 구매가 급증하는가?"
  - "마지막 1분간 에러 비율이 임계값을 초과했는가?"
  - "A/B 테스트 그룹별 실시간 전환율 비교"
```

### 2. 세 가지 주요 실시간 OLAP 시스템

| 시스템 | 개발사 | 핵심 강점 | 대표 사용자 |
|:---|:---|:---|:---|
| Apache Druid | MetaMarkets/Apache | 이벤트 시계열 집계, 사전집계 | Netflix, Airbnb, 카카오 |
| Apache Pinot | LinkedIn/Uber/Apache | Upsert, StarTree 인덱스, 실시간 업데이트 | LinkedIn, Uber, Slack |
| ClickHouse | Yandex/ClickHouse Inc. | SQL 호환성, 단순 운영, 압축률 | Cloudflare, Shopify |

**📢 섹션 요약 비유**
> 실시간 OLAP는 "도서관 vs 편의점"의 차이다. DW는 모든 책이 있는 도서관(정확하지만 느림), 실시간 OLAP는 인기 상품을 미리 정리해 둔 편의점(빠르지만 범위 제한). 편의점이 모든 DW를 대체하지는 못하지만, 빠른 응답이 필요한 상황에서는 편의점이 훨씬 유용하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Apache Druid 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│  Apache Druid 아키텍처                                       │
│                                                             │
│  데이터 소스                                                 │
│    Kafka/S3 → 수집 계층 (Overlord + MiddleManager)          │
│                    │ 실시간 Segment 생성                     │
│                    ▼                                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  히스토리컬 노드 (Historical) — 세그먼트 저장         │   │
│  │  · 세그먼트: 시간 단위로 분할된 컬럼형 데이터 덩어리  │   │
│  │  · 사전집계 (Roll-up): 같은 차원 조합 집계 미리 계산  │   │
│  │  · 비트맵 인덱스: 필터 연산 초고속                    │   │
│  └─────────────────────┬────────────────────────────────┘   │
│                        │ 쿼리                               │
│  ┌─────────────────────▼────────────────────────────────┐   │
│  │  브로커 노드 (Broker) — 쿼리 라우팅 및 집계           │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  메타데이터: Zookeeper + 메타데이터 스토리지 (MySQL)         │
└─────────────────────────────────────────────────────────────┘
```

### 2. 사전집계 (Roll-up) — Druid의 핵심

```
원본 데이터:
  timestamp=2024-01-01 10:00:00, country=KR, product=A, sales=100
  timestamp=2024-01-01 10:00:30, country=KR, product=A, sales=200
  timestamp=2024-01-01 10:01:00, country=KR, product=A, sales=150
  timestamp=2024-01-01 10:00:45, country=US, product=B, sales=300

Druid Roll-up (1분 단위, country+product 차원으로 집계):
  timestamp=2024-01-01 10:00:00, country=KR, product=A, sum_sales=450, count=2
  timestamp=2024-01-01 10:01:00, country=KR, product=A, sum_sales=150, count=1
  timestamp=2024-01-01 10:00:00, country=US, product=B, sum_sales=300, count=1

→ 원본 4행 → 집계 3행 (압축율 25%)
→ 집계 쿼리 속도 대폭 향상!
```

### 3. 세 시스템 기능 비교

| 기능 | Druid | Pinot | ClickHouse |
|:---|:---|:---|:---|
| 핵심 강점 | 이벤트 시계열 + 사전집계 | Upsert + StarTree 인덱스 | SQL 완전성 + 단순 운영 |
| 수집 방식 | Kafka, S3, HTTP | Kafka, Kinesis, HDFS | INSERT INTO + Kafka Engine |
| Upsert | 제한적 (1.1+) | ✅ 완전 지원 | ✅ (ReplacingMergeTree) |
| 쿼리 언어 | Druid SQL, Native | PQL, SQL | ANSI SQL (완전) |
| 조인 | 제한적 | 제한적 | 완전 지원 |
| 운영 복잡도 | 높음 (5+종 노드) | 높음 (Zookeeper 필요) | 낮음 (단일 프로세스) |
| 스토리지 압축 | ✅ (컬럼형) | ✅ (컬럼형) | ✅ (최고 수준) |

**📢 섹션 요약 비유**
> Druid는 "미리 요약 정리된 보고서(사전집계)"로 빠른 조회, Pinot은 "항상 최신 정보로 업데이트되는 게시판(Upsert)", ClickHouse는 "SQL을 잘 아는 누구나 쓸 수 있는 고속 데이터베이스"이다.

---

## Ⅲ. 비교 및 연결

### 1. 전통 DW vs 실시간 OLAP

| 비교 항목 | 전통 DW (Redshift/BigQuery) | 실시간 OLAP (Druid/Pinot/ClickHouse) |
|:---|:---|:---|
| 데이터 신선도 | T+1일 (ETL 배치) | T+수 초 (스트리밍 수집) |
| 쿼리 응답시간 | 수십 초~수 분 | < 1초 (수십억 행) |
| 데이터 수정 | 쉬움 (UPDATE/DELETE) | 어려움 (Append-only 기본) |
| 쿼리 유연성 | 높음 (복잡 조인, 서브쿼리) | 제한적 (미리 정의된 차원) |
| 비용 | 쿼리 비용 | 인프라 고정 비용 |

### 2. 실시간 OLAP + Kafka 스트리밍 연동

```
Kafka → Druid Realtime Ingestion → Segment 생성 → 쿼리 가능
    └──→ S3 (백업) → Druid Historical Ingestion → 히스토리 세그먼트

Kafka → Pinot Controller → Table → Upsert 처리 → 실시간 쿼리
Kafka → ClickHouse Kafka Engine Table → MergeTree → 집계
```

**📢 섹션 요약 비유**
> 실시간 OLAP vs DW는 "즉석 요리 vs 전통 코스 요리"이다. 즉석 요리(실시간 OLAP)는 빠르지만 메뉴(쿼리 패턴)가 제한적이고, 코스 요리(DW)는 뭐든 만들 수 있지만 시간이 오래 걸린다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 1. 시스템 선택 가이드

| 사용 사례 | 권장 시스템 | 이유 |
|:---|:---|:---|
| 클릭스트림 실시간 대시보드 | Apache Druid | 이벤트 시계열 + 사전집계 강점 |
| 사용자 프로파일 조회 (자주 업데이트) | Apache Pinot | Upsert + 낮은 지연 조회 |
| 로그 분석 (단순 SQL) | ClickHouse | SQL 완전성 + 단순 운영 |
| 광고 클릭 집계 | Apache Druid | Roll-up으로 집계 압축 |
| 금융 거래 실시간 조회 | Apache Pinot | 정확한 Upsert + 실시간 |

### 2. 도입 체크리스트

- [ ] 데이터 신선도(Freshness) SLA: "몇 초 이내 쿼리 가능?" 요건 수립
- [ ] 차원(Dimension) 설계: Roll-up/Star Schema 사전 설계 필수
- [ ] 쿼리 패턴 분석: 미리 알 수 없는 임의 쿼리 → DW 혼용
- [ ] 클러스터 규모 계산: 세그먼트 크기 × 보존 기간 × 복제 인자
- [ ] Druid/Pinot 운영 복잡도 평가: 소규모 팀에는 ClickHouse가 현실적

**📢 섹션 요약 비유**
> 실시간 OLAP 설계는 "편의점 상품 배치 결정"과 같다. 자주 팔리는 상품(자주 쿼리되는 차원)을 앞쪽 선반(사전집계)에 배치해야 빠르게 찾는다. 처음부터 어떤 상품이 많이 팔릴지(쿼리 패턴) 예측해야 효율적인 가게가 된다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 수치 예시 |
|:---|:---|
| 쿼리 응답시간 | DW 30초 → 실시간 OLAP 0.3초 (100배 향상) |
| 데이터 신선도 | T+1일 → T+수 초 (1000배 향상) |
| 대시보드 인터랙티비티 | 페이지 새로고침 → 실시간 업데이트 |

### 2. 결론

실시간 OLAP는 **실시간 의사결정이 필요한 모든 분야의 분석 인프라 혁신**을 이끌고 있다. 기술사 답안에서는 전통 DW와의 지연-유연성 트레이드오프, 세 시스템(Druid/Pinot/ClickHouse)의 핵심 차이점, 사전집계(Roll-up)와 컬럼형 저장소의 성능 원리, Kafka와의 실시간 수집 연계를 함께 서술해야 한다.

**📢 섹션 요약 비유**
> 실시간 OLAP는 "도서관 사서가 밤새 인기 도서 요약본을 만들어 두는 것"이다. 다음 날 아침 방문객이 "이 주제의 요약이 뭐예요?"라고 물으면 즉각 답할 수 있다. 요약이 없는 주제(사전 정의되지 않은 쿼리)는 여전히 원본 책(DW)을 찾아야 한다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Apache Kafka | 데이터 소스 | 실시간 OLAP의 스트리밍 수집 소스 |
| Columnar Storage | 핵심 기술 | 컬럼형 저장으로 집계 쿼리 최적화 |
| Pre-aggregation (Roll-up) | 핵심 기술 | 사전집계로 쿼리 시점 연산 최소화 |
| Lambda/Kappa Architecture | 아키텍처 연계 | 실시간 OLAP는 서빙 레이어 역할 |
| 전통 DW (Redshift/BigQuery) | 비교 대상 | 유연성 높으나 지연 있는 대안 |

### 👶 어린이를 위한 3줄 비유 설명

실시간 OLAP는 "미리 준비된 빠른 답변 창구"예요. 선생님이 "이번 주 어느 문제를 가장 많이 틀렸어?"라고 물으면, 준비 없이는 수천 장의 시험지를 다 뒤져야 하지만, Druid/Pinot/ClickHouse는 미리 문제별 오답 수를 세어 두어서(사전집계) 즉시 답할 수 있어요. 단, 미리 생각하지 못한 질문("이번 주 월요일 오전에 비 올 때 틀린 문제는?")은 여전히 천천히 찾아야 한답니다!
