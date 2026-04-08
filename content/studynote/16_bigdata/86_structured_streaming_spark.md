+++
title = "86. Consumer Lag — Kafka 소비 지연 모니터링, Burrow / JMX"
date = "2026-04-07"
[extra]
categories = "studynote-bigdata"
+++

# Structured Streaming: Spark 기반 실시간 스트리밍 처리

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Structured Streaming (구조적 스트리밍) 은 Apache Spark의 기존 배치 DataFrame/Dataset API를 그대로 사용하여 실시간 데이터 스트림을 "끝없이 증가하는 테이블 (Unbounded Table)"로 추상화하고 처리하는 통합 스트리밍 엔진으로, "동일한 코드로 배치와 스트리밍을 모두 처리"하는 Unified Computing Model을 실현한다.
> 2. **가치**: 기존 일회성 배치(Batch)와 스트리밍(DStream)이 분리되어 있던 코드베이스를 하나의 DataFrame API로 통합함으로써, 람다 아키텍처(Lambda Architecture)의 복잡한 이중 유지보수 문제를 근본적으로 해결한다.
> 3. **융합**: Kafka 소스 연동, Delta Lake 싱크, Watermark를 통한 지연 이벤트 처리, Exactly-Once 시맨틱스 보장이 결합되어 실시간 ETL (Real-Time ETL), 이상 탐지 (Anomaly Detection), 실시간 KPI 대시보드의 백엔드 엔진으로 현대 빅데이터 플랫폼에서 핵심 역할을 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: Structured Streaming은 Spark 2.0(2016)에서 도입된 스트리밍 처리 API다. 데이터를 "스트림으로 처리한다"는 개념 대신 "입력 데이터가 무한히 추가되는 테이블"로 바라본다. 개발자는 이 테이블을 대상으로 SQL 쿼리 또는 DataFrame 연산을 작성하면, Spark 엔진이 내부적으로 마이크로배치(Micro-Batch) 또는 연속 처리(Continuous Processing)로 실행한다.
- **필요성**: 기존 Spark Streaming (DStream API)은 RDD 기반이라 SQL 최적화가 미적용되고, 배치 코드와 완전히 다른 API를 사용해야 했다. Structured Streaming은 Catalyst 옵티마이저를 그대로 적용받아 배치와 동일한 성능 최적화 이점을 누린다.
- **💡 비유**: 개울물이 흘러오는 것을 매 순간 뜨는 것(DStream)이 아니라, 물이 흘러 들어와 계속 커지는 큰 수조(Unbounded Table)로 보고 수조 안의 물을 분석하는 방식이다. 새로운 물이 들어올 때마다 수조가 업데이트되고 분석 결과가 갱신된다.

```text
┌────────────────────────────────────────────────────────┐
│       Structured Streaming의 Unbounded Table 모델         │
├────────────────────────────────────────────────────────┤
│                                                        │
│  [실시간 입력 스트림: Kafka, File, Socket]               │
│       │                                                │
│       ▼                                                │
│  ┌──────────────────────────────────────────┐         │
│  │           입력 테이블 (Unbounded)           │         │
│  │  Row1 [T=0s]                              │         │
│  │  Row2 [T=1s]  ← 계속 행이 추가됨            │         │
│  │  Row3 [T=2s]                              │         │
│  │  Row4 [T=3s]  ← 새 이벤트 = 새 행           │         │
│  └──────────────────────────────────────────┘         │
│       │                                                │
│       ▼  (배치와 동일한 DataFrame/SQL 쿼리 적용)          │
│  SELECT window, COUNT(*) FROM input GROUP BY window    │
│       │                                                │
│       ▼                                                │
│  ┌──────────────────┐                                  │
│  │ 결과 테이블       │ ← 트리거마다 업데이트              │
│  │ (Result Table)   │                                  │
│  └──────────────────┘                                  │
│       │                                                │
│  [출력 싱크: Console / Kafka / Delta Lake / JDBC]       │
└────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 모델의 핵심은 "스트리밍을 배치처럼 생각하게 한다"는 추상화다. 개발자는 입력 데이터가 모두 한 테이블에 있다고 가정하고 SQL/DataFrame 쿼리를 작성한다. Spark 엔진이 내부적으로 마이크로배치를 실행하여 새로 들어온 행에 대해서만 증분(Incremental) 처리를 하고 결과 테이블을 업데이트한다. 기존 Spark 배치코드를 그대로 재활용할 수 있어 개발 생산성과 코드 일관성이 극적으로 향상된다.

- **📢 섹션 요약 비유**: 신문 기사가 매시간 추가되는 아카이브 DB에 "오늘 자 기사 중 조회수 상위 10위"를 쿼리하는 것처럼, 스트리밍 데이터도 계속 커지는 테이블로 쿼리합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Structured Streaming 출력 모드 (Output Mode)

| 출력 모드 | 동작 | 적합 사용처 |
|:---|:---|:---|
| **Append Mode** | 새로 추가된 행만 싱크에 출력 | 집계 없는 단순 ETL, 이벤트 로그 |
| **Complete Mode** | 매 트리거마다 전체 결과 테이블 다시 출력 | 집계 결과 전체가 필요한 대시보드 |
| **Update Mode** | 변경된 행만 출력 (Complete 대비 네트워크 효율적) | 집계 결과 일부가 변경될 때, DB Upsert |

---

### Watermark를 통한 지연 이벤트 처리

실시간 스트리밍의 가장 큰 도전은 네트워크 지연으로 인해 이벤트가 늦게 도착하는 "지연 이벤트(Late Data)" 처리다. Watermark는 Spark에게 "이 시간 이후로 늦게 도착한 이벤트는 버린다"는 임계값을 설정한다.

```text
┌───────────────────────────────────────────────────────────┐
│        Watermark를 통한 지연 이벤트 처리 원리                 │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  [이벤트 시간 vs 처리 시간 불일치 문제]                        │
│                                                           │
│  현재 처리 시간: 10:05                                      │
│  수신된 이벤트: {event_time: 10:01, data: "A"}              │
│                {event_time: 10:00, data: "B"}  ← 늦게 도착 │
│                {event_time: 09:55, data: "C"}  ← 매우 늦음 │
│                                                           │
│  Watermark 설정: .withWatermark("event_time", "10 minutes")│
│                                                           │
│  → watermark = max(event_time) - 10분 = 10:01 - 10분      │
│              = 09:51                                       │
│                                                           │
│  09:55 이벤트(C): 09:55 > 09:51 → 허용 (윈도우에 포함)       │
│  09:40 이벤트(D): 09:40 < 09:51 → 폐기 (너무 늦음)          │
│                                                           │
│  → Watermark로 허용 지연 범위를 명시하고                       │
│    범위 초과 이벤트는 폐기하여 상태 저장소(State) 무한 증가 방지  │
└───────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Watermark가 없으면 Structured Streaming은 이론상 모든 과거 이벤트를 기다려야 하므로 상태(State) 저장소가 무한히 커진다. Watermark는 "최대 10분까지 지연된 이벤트는 기다리지만 그 이상 늦으면 버린다"는 계약을 통해 메모리 사용량을 경계 지운다. 이 값은 비즈니스 요구사항(몇 초 지연까지 허용?)과 기술적 제약(메모리 한계)의 균형점으로 설정해야 한다. Apache Flink의 Watermark 개념을 Spark에서 동일하게 구현한 것이다.

- **📢 섹션 요약 비유**: "비행기 탑승 마감 10분 전까지 온 승객만 태운다"는 규칙처럼, Watermark는 "몇 분 늦게 도착한 이벤트까지 처리에 포함할지"의 탑승 마감 기준입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### DStream (구세대) vs Structured Streaming 비교

| 비교 기준 | Spark Streaming (DStream) | Structured Streaming |
|:---|:---|:---|
| **API** | RDD 기반, 저수준 | DataFrame/Dataset, 고수준 |
| **최적화** | Catalyst 옵티마이저 미적용 | Catalyst+Tungsten 완전 적용 |
| **이벤트 시간 처리** | 직접 구현 필요, 복잡 | Watermark 내장 지원 |
| **Exactly-Once 지원** | 부분적 | Checkpoint + Kafka 연동 완전 지원 |
| **코드 공유** | 배치와 완전히 다른 코드 | 배치 코드 그대로 재사용 가능 |
| **현재 상태** | 유지보수 모드 (권장하지 않음) | Spark의 표준 스트리밍 API |

```text
┌───────────────────────────────────────────────────────────┐
│       Kafka → Structured Streaming → Delta Lake 파이프라인  │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  [Kafka 토픽]                                              │
│   clicks_topic → (실시간 클릭 이벤트)                       │
│       │                                                   │
│       ▼                                                   │
│  [Structured Streaming 처리]                               │
│   spark.readStream                                        │
│     .format("kafka")                                      │
│     .option("subscribe", "clicks_topic")                  │
│       │                                                   │
│       ▼  (JSON 파싱 + 집계)                                │
│   .withWatermark("event_time", "5 minutes")               │
│   .groupBy(window("event_time", "1 hour"), "user_id")     │
│   .count()                                                │
│       │                                                   │
│       ▼                                                   │
│  [Delta Lake 싱크 — Exactly-Once 보장]                     │
│   .writeStream.format("delta")                            │
│   .option("checkpointLocation", "/checkpoints/clicks")    │
│   → 시간당 사용자별 클릭 수 실시간 적재                       │
│   → Power BI가 Delta Lake를 폴링하여 실시간 대시보드 갱신     │
└───────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 파이프라인은 Kafka에서 실시간 클릭 이벤트를 스트리밍으로 구독하여 1시간 윈도우 기반 사용자별 클릭 집계를 Delta Lake에 적재하는 전형적인 실시간 ETL 패턴이다. Checkpoint 위치를 지정함으로써 Spark가 소비한 Kafka 오프셋과 처리 상태를 영구 저장하여, 장애 재시작 시 중복 없이 정확히 한 번(Exactly-Once) 처리를 보장한다. Delta Lake의 ACID 트랜잭션이 스트리밍 쓰기에도 적용되어 "스트리밍 덮어쓰기" 중에 BI 도구가 일관된(Consistent) 데이터를 읽을 수 있다.

- **📢 섹션 요약 비유**: 편의점 CCTV 영상(Kafka)을 AI(Structured Streaming)가 실시간으로 분석해 "지난 1시간 동안 진열대별 방문 고객 수"를 계속 갱신해서 대시보드에 보여주는 시스템입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오
1. **시나리오 — Kafka 파티션 증가 후 Structured Streaming 처리 지연**: 트래픽 급증으로 Kafka 파티션을 4개→16개로 늘렸는데 Structured Streaming 쿼리가 새 파티션을 인식하지 못해 처리 지연 발생.
   - **판단**: Structured Streaming은 Kafka 파티션 수 변경을 동적으로 감지하여 자동 처리한다. 단, 기존 체크포인트에서 재시작할 때 파티션 변경이 올바르게 적용되는지 확인이 필요하며, `maxOffsetsPerTrigger` 옵션으로 처리 속도를 조절해야 한다.
2. **시나리오 — Structured Streaming 상태 저장소 OOM**: Watermark 미설정 상태에서 시간 기반 집계를 수행하다 수 GiB의 상태가 메모리에 누적되어 Executor OOM(Out of Memory) 장애.
   - **판단**: 모든 시간 기반 집계(window, groupBy event_time)에는 반드시 `.withWatermark()` 설정이 필수다. 선정된 Watermark 임계값(예: 10분)이 지나면 Spark가 해당 상태를 메모리에서 제거한다.

### 도입 체크리스트
- **기술적**: Checkpoint 디렉터리가 HDFS/S3/GCS와 같은 내결함성 있는 분산 스토리지에 설정되어 있는가? 로컬 파일시스템 체크포인트는 노드 장애 시 상태를 잃는다.
- **운영적**: Structured Streaming 쿼리의 처리 속도(Processing Rate)와 입력 속도(Input Rate)를 Spark UI 또는 Prometheus로 모니터링하여 백로그(Lag)가 쌓이는 것을 감지하고 있는가?

### 안티패턴
- **Complete 모드 대형 집계**: 글로벌 집계(GROUP BY 없이 전체 COUNT)에 Complete 모드를 사용하면 매 트리거마다 전체 결과를 싱크에 쓰여 네트워크·스토리지 비용이 폭발한다. Update 모드와 변경분만 업서트(Upsert)하는 Delta MERGE로 대체해야 한다.

- **📢 섹션 요약 비유**: 매시간 대화 전체 내역을 카카오톡에 다시 전송하는 것(Complete 모드)이 아니라, 새로 바뀐 메시지만 전송하는 것(Update 모드)이 효율적입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | DStream 방식 | Structured Streaming 전환 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 배치+스트리밍 코드 이원화로 유지보수 비용 2배 | 단일 DataFrame API 통합 | 코드베이스 **50% 축소** |
| **정량** | 이벤트 시간 처리 직접 구현으로 오류 원인 多 | Watermark 내장으로 지연 이벤트 자동 처리 | 파이프라인 정확도 향상 |
| **정성** | 람다 아키텍처 유지의 팀 피로도 높음 | 카파 아키텍처 단일 파이프라인 구현 가능 | 운영 복잡도 대폭 감소 |

### 미래 전망
- **Project Lightspeed (Spark 4.x)**: Structured Streaming의 연속 처리(Continuous Processing) 모드를 마이크로배치 지연(수백 ms)에서 진짜 밀리초(ms) 수준으로 낮추는 Spark 차세대 스트리밍 엔진 개선이 진행 중이다.

### 참고 표준
- **Spark Structured Streaming Programming Guide (Databricks/Apache)**: 공식 API 레퍼런스. Watermark·Trigger·Output Mode의 모든 조합 설명.

Structured Streaming은 "스트리밍은 느리고 어렵다"는 편견을 깼다. DataFrame의 선언적 API, Catalyst 최적화, Delta Lake와의 네이티브 통합으로 배치 개발자도 몇 줄의 코드 변경만으로 실시간 파이프라인을 구축할 수 있게 했다. 이것이 카파 아키텍처(Kappa Architecture)의 현실적 구현체가 된 이유다.

- **📢 섹션 요약 비유**: 예전에는 기차(배치)와 자동차(스트리밍)를 따로 운전하는 법을 배워야 했지만, Structured Streaming은 하나의 운전법으로 두 가지 탈것을 모두 다룰 수 있게 해준 통합 면허제와 같습니다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

- **Apache Kafka** | Structured Streaming의 가장 일반적인 소스. 고처리량 내구성 이벤트 큐. 오프셋 기반 Exactly-Once 연동.
- **Delta Lake** | Structured Streaming의 가장 권장되는 싱크. ACID 스트리밍 쓰기, 타임 트래블 지원.
- **Watermark** | 지연 이벤트 허용 시간 임계값. Structured Streaming 상태 저장소 크기를 경계 짓는 핵심 설정.
- **Apache Flink** | Structured Streaming의 경쟁자. 진정한 이벤트 기반 스트리밍, 낮은 지연 시간에서 Flink가 우위.
- **람다 아키텍처 (Lambda Architecture)** | 배치(정확성)와 스트리밍(속도)를 분리 운영하는 구조. Structured Streaming이 해결하는 이원화 문제.

---

## 👶 어린이를 위한 3줄 비유 설명
1. 예전 스트리밍 처리는 흐르는 강물을 매 초 바가지로 뜨는 것과 같아서 불편했어요.
2. Structured Streaming은 그 강물을 큰 수조에 계속 채워 넣고, 수조 안 물을 분석하는 방식으로 바꾼 거예요. 새 물이 들어올 때마다 분석 결과가 자동 업데이트되죠.
3. 가장 좋은 점은 평소에 수조(배치 처리)를 분석하던 방법 그대로 강물(실시간 스트리밍)도 분석할 수 있어서, 개발자들이 새로운 방법을 배울 필요가 없다는 거예요!
