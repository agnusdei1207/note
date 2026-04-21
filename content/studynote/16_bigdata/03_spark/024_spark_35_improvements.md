+++
weight = 24
title = "24. Apache Spark 3.5+ 개선사항 — 최신 기능 및 Python API 강화"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)

- **본질**: Apache Spark 3.5+ (2023~)는 ANSI SQL 표준 호환성 대폭 확대, Spark Connect (클라이언트-서버 분리 아키텍처), Python UDF 벡터화 강화, PySpark DataFrame API 개선을 통해 데이터 엔지니어링 생산성과 원격 접근 유연성을 동시에 높였다.
- **가치**: Spark Connect는 클라이언트와 Spark 클러스터를 gRPC 프로토콜로 분리하여, 로컬 Python 환경에서 원격 클러스터를 직접 제어할 수 있게 함으로써 데이터 과학자의 개발-운영 경계를 허물고 보안성도 높인다.
- **판단 포인트**: Spark 3.5+의 ANSI SQL 강화는 기존 non-ANSI 동작에 의존하던 쿼리가 오류를 발생시킬 수 있어 마이그레이션 시 `spark.sql.ansi.enabled` 설정을 단계적으로 활성화하고 기존 쿼리를 사전 검증해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1. Spark 3.x 계열의 진화 맥락

| 버전 | 핵심 변화 | 출시 시점 |
|:---|:---|:---|
| Spark 3.0 | AQE 도입, Accelerator-aware 스케줄링 | 2020.06 |
| Spark 3.1 | K8s Production Ready, SQL 개선 | 2021.03 |
| Spark 3.2 | Pandas API on Spark, RocksDB StateStore | 2021.10 |
| Spark 3.3 | ANSI SQL 강화, Protobuf 지원 | 2022.06 |
| Spark 3.4 | Spark Connect Preview, PySpark UDF 개선 | 2023.04 |
| Spark 3.5 | Spark Connect GA, Python Connect SDK, ANSI 확대 | 2023.09 |

### 2. 왜 Spark 3.5+가 중요한가

빅데이터 생태계가 점차 Python 중심으로 이동하고, 원격 개발(클라우드 클러스터에서 로컬 IDE로 작업)이 보편화되면서, Spark의 아키텍처도 이에 맞게 진화해야 했다.

**📢 섹션 요약 비유**
> Spark 3.5는 "기존 대형 공장에 원격 제어 시스템(Spark Connect)을 설치한 것"이다. 공장 안에 직접 들어가지 않아도(드라이버 직접 접속 불필요) 밖에서 태블릿으로 모든 기계를 제어할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Spark Connect 아키텍처

Spark Connect (스파크 커넥트)는 클라이언트와 Spark 서버 간에 **Unresolved Logical Plan**을 gRPC/Protocol Buffers로 직렬화하여 전송하는 클라이언트-서버 분리 아키텍처다.

```
기존 Spark 아키텍처 (Spark 3.3 이전):
┌────────────────────────────────────────────┐
│  사용자 코드 + SparkSession (같은 프로세스) │
│  → Cluster Manager → Executors             │
└────────────────────────────────────────────┘

Spark Connect 아키텍처 (Spark 3.4+):
┌──────────────────────┐     gRPC      ┌──────────────────────────┐
│  클라이언트 프로세스  │ ────────────→ │  Spark Connect Server    │
│  (Python/Scala/Java)  │               │  (Spark 클러스터 내부)   │
│  로컬 PC / Notebook   │ ←──────────── │  Logical Plan 실행       │
└──────────────────────┘   결과 반환    └──────────────────────────┘
```

### 2. Spark Connect의 장점

| 장점 | 설명 |
|:---|:---|
| 클라이언트 격리 | 클라이언트 코드 오류가 Spark 서버에 영향을 주지 않음 |
| 원격 개발 | 로컬 IDE에서 원격 클러스터에 직접 접속 |
| 다양한 클라이언트 지원 | Python, Scala, Java, Go 클라이언트 독립 개발 가능 |
| 보안 강화 | 클러스터 접근을 gRPC 레이어에서 인증·인가 |
| 서버 안정성 | 클라이언트 충돌이 서버를 다운시키지 않음 |

### 3. Python API 강화 항목

```python
# Spark 3.5+ 주요 Python API 개선

# 1. Python UDF Inlining (일부 Python UDF가 JVM 없이 처리)
from pyspark.sql.functions import udf
# Arrow-optimized Python UDF (Pandas UDF 자동 최적화 강화)

# 2. PySpark DataFrame에서 파이썬 타입 힌트 강화
from pyspark.sql.types import IntegerType, StringType

# 3. ANSI SQL 함수 추가 (Spark 3.5)
spark.sql("SELECT TRY_CAST('abc' AS INT)")   # ANSI: NULL 반환 (예외 아님)
spark.sql("SELECT TRY_SUM(col) FROM t")      # ANSI: 오버플로 시 NULL

# 4. Spark Connect 클라이언트 사용
from pyspark.sql import SparkSession
# 원격 Connect 서버에 접속
spark = SparkSession.builder \
    .remote("sc://my-spark-server:15002") \
    .getOrCreate()
df = spark.read.parquet("hdfs:///data/")  # 원격 클러스터에서 실행
```

### 4. ANSI SQL 표준 강화 항목

| 기능 | Spark 3.3 이전 | Spark 3.5 (ANSI 활성화) |
|:---|:---|:---|
| 정수 오버플로 | 래핑(오버플로 무시) | ArithmeticException 발생 |
| 잘못된 CAST | NULL 반환 | 예외 발생 또는 TRY_CAST |
| `TRY_` 함수군 | 미지원 | TRY_CAST, TRY_ADD, TRY_DIVIDE |
| 서브쿼리 표준화 | 비표준 허용 | ANSI 표준 준수 강제 |
| `DATE_TRUNC` 등 | 제한적 | 표준 날짜/시간 함수 완전 지원 |

**📢 섹션 요약 비유**
> Spark Connect는 "회사 VPN 없이 노트북에서 회사 서버에 직접 원격 접속하는 것"이다. 이전에는 서버 방에 직접 들어가거나 복잡한 터널을 뚫어야 했는데, 이제 인터넷에서 직접 gRPC로 안전하게 접속한다.

---

## Ⅲ. 비교 및 연결

### 1. Spark Connect vs Thrift Server

| 비교 항목 | Thrift Server (기존) | Spark Connect (3.4+) |
|:---|:---|:---|
| 프로토콜 | JDBC/ODBC (Hive 호환) | gRPC + Protobuf |
| 클라이언트 | BI 툴, SQL 클라이언트 | Python/Java/Go SDK |
| 연산 표현력 | SQL만 가능 | 전체 DataFrame API |
| 확장성 | 단일 Thrift 서버 | 다중 클라이언트 동시 접속 |
| 클라이언트 격리 | 약함 | 강함 |

### 2. 연결 개념

- **AQE (Adaptive Query Execution)**: Spark 3.0 도입, 3.5+에서 더 넓은 연산에 확장
- **Photon Engine**: Databricks의 3.5+ 통합 강화
- **Delta Lake 3.x**: Spark 3.5와 함께 UniForm(Iceberg 호환 레이어) 도입

**📢 섹션 요약 비유**
> Spark의 버전 진화는 "스마트폰 OS 업데이트"와 같다. 겉모습(API)은 비슷하지만 내부 엔진이 계속 빨라지고, 새 기능(Spark Connect)이 생기며, 표준(ANSI SQL)이 강화된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 1. Spark 3.5+ 마이그레이션 체크리스트

- [ ] ANSI SQL 테스트: `spark.sql.ansi.enabled=true`로 기존 쿼리 테스트 실행
- [ ] 정수 오버플로 가능성 있는 컬럼에 `TRY_CAST`, `TRY_ADD` 도입
- [ ] Python UDF 성능 검토: pandas_udf (Arrow 기반) 또는 Spark UDF로 최적화
- [ ] Spark Connect 도입 검토: 클라이언트 격리 및 원격 개발 환경 개선
- [ ] Delta Lake 버전: Spark 3.5에 맞는 Delta Lake 버전(3.x) 호환성 확인

### 2. Spark Connect 도입 시 고려사항

```
고려 사항 1: 네트워크 지연
  로컬 클라이언트 → gRPC → 원격 서버
  작은 결과 수집 시 RTT 추가 발생

고려 사항 2: 클라이언트 독립 배포
  클라이언트 버전과 서버 버전 호환성 관리 필요

고려 사항 3: 인증/보안
  gRPC TLS, 토큰 기반 인증 설정 필수
```

**📢 섹션 요약 비유**
> Spark 3.5+ 마이그레이션은 "도로 규칙이 바뀐 교통 시스템 전환"이다. 새 표준(ANSI SQL)이 더 안전하지만, 기존 운전자(쿼리)가 구 습관(비표준 동작)을 바꾸는 과도기 충돌에 대비해야 한다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 개선 항목 | 기대 효과 |
|:---|:---|
| Spark Connect | 원격 개발 환경 표준화, 클라이언트 격리 |
| ANSI SQL 강화 | SQL 표준 호환성 → 다른 엔진으로의 이식성 향상 |
| Python API 강화 | Python 생태계와의 통합 심화, UDF 성능 개선 |
| AQE 확장 | 더 넓은 쿼리 패턴에서 자동 최적화 |

### 2. 결론

Apache Spark 3.5+는 단순한 버그 수정이 아니라 **아키텍처 수준의 진화**를 담고 있다. Spark Connect는 미래 클라우드 네이티브 환경에서 Spark의 위치를 재정의하며, ANSI SQL 강화는 Spark를 범용 SQL 엔진으로서의 표준화에 기여한다. 기술사 답안에서는 Spark Connect의 클라이언트-서버 분리의 의미와 ANSI SQL 마이그레이션 주의사항을 중심으로 서술하는 것이 효과적이다.

**📢 섹션 요약 비유**
> Spark 3.5+는 "빅데이터 플랫폼의 다음 세대 운영체제 버전"이다. 성능 개선(CPU 효율화)과 함께 원격 접속 표준(Spark Connect)을 도입하여, 데이터 엔지니어가 어디서나 클러스터를 다룰 수 있는 클라우드 네이티브 시대를 준비한다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Spark Connect | 핵심 신기능 | gRPC 기반 클라이언트-서버 분리 아키텍처 |
| AQE | 확장 대상 | 3.5에서 더 많은 연산에 AQE 적용 범위 확대 |
| Photon Engine | Databricks 대응 | Databricks의 Spark 3.5+ 기반 성능 엔진 |
| ANSI SQL | 표준화 방향 | SQL 표준 준수로 이식성·예측 가능성 향상 |
| PySpark | Python 생태계 | Python API 강화로 데이터 과학자 접근성 향상 |

### 👶 어린이를 위한 3줄 비유 설명

Spark 3.5는 마치 게임 앱 업데이트처럼, 더 빠르고(성능 개선) 더 많은 기기에서 플레이할 수 있게(Spark Connect: 원격 접속) 해줘요. 예전에는 게임 서버 컴퓨터 앞에 앉아야 했지만, 이제는 집에서 스마트폰(Python 클라이언트)으로 서버에 접속해서 플레이할 수 있답니다. SQL 규칙도 국제 표준(ANSI)에 맞게 더 엄격해져서 더 안전한 게임 환경이 됐어요!
