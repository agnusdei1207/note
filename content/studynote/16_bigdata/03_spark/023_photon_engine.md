+++
weight = 23
title = "23. Photon Engine (Databricks) — 네이티브 벡터화 실행 엔진"
date = "2026-04-29"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Photon Engine (포톤 엔진)은 Databricks가 개발한 C++ 기반 네이티브 벡터화 실행 엔진으로, JVM (Java Virtual Machine) 오버헤드를 제거하고 SIMD (Single Instruction Multiple Data) 명령어를 활용해 컬럼(Column) 단위 배치 처리를 수행한다.
> 2. **가치**: 기존 Spark 코드 변경 없이 SQL 집계·조인·필터 등 쿼리 집약적 워크로드에서 최대 12배 이상의 성능 향상을 제공하며, Databricks SQL Warehouse의 기본 실행 엔진으로 동작한다.
> 3. **판단 포인트**: Databricks Runtime 전용이므로 오픈소스 Spark에서는 사용 불가이며, Python UDF처럼 JVM이 필요한 연산은 JVM Spark 엔진으로 폴백(Fallback)되므로 워크로드 구성에 따라 기대 효과가 달라진다.

---

## Ⅰ. 개요 및 필요성

Photon Engine은 Databricks가 2021년 발표한 **C++ 기반 네이티브 벡터화 쿼리 실행 엔진**으로, Apache Spark의 JVM 기반 실행 계층이 가진 구조적 성능 한계를 극복하기 위해 설계되었다.

### 1. 기존 Spark Tungsten 엔진의 한계

Apache Spark의 Tungsten 엔진은 JVM 힙 관리와 런타임 코드 생성(Codegen)으로 성능을 개선했으나 근본적인 한계가 남아 있었다.

| 한계 영역 | 상세 내용 |
|:---|:---|
| JVM 인터프리터 오버헤드 | Java Bytecode 실행, JIT (Just-In-Time) 컴파일 지연 |
| 행 단위 처리 | Row-at-a-time 처리로 CPU 캐시 효율 저하 |
| SIMD 미활용 | JVM에서 AVX-512 등 현대 CPU 명령어 완전 활용 불가 |
| GC (Garbage Collection) 압박 | 객체 생성·소멸로 인한 Stop-the-World 지연 |

현대 CPU는 AVX-512 SIMD 명령어 한 번으로 16개 이상의 64비트 정수를 동시에 처리할 수 있다. JVM은 이를 완전히 활용하기 어렵다.

### 2. Photon의 등장 배경

```
[JVM 기반 Spark 처리 경로]
  SQL 쿼리
      │
      ▼
  Catalyst Optimizer (JVM)
      │ 물리 계획 생성
      ▼
  Tungsten Codegen (JVM)
      │ Java Bytecode 실행
      ▼
  CPU 처리 (행 단위, SIMD 미활용)
  문제: JVM ↔ CPU 사이의 번역 계층이 병목

[Photon 처리 경로]
  SQL 쿼리
      │
      ▼
  Catalyst Optimizer (JVM)
      │ 물리 계획 전달 (JNI)
      ▼
  Photon C++ Native Engine
      │ SIMD 벡터화 직접 실행
      ▼
  CPU 처리 (컬럼 단위, AVX-512 완전 활용)
  개선: JVM 번역 계층 제거 → CPU 직접 활용
```

**📢 섹션 요약 비유**
> 기존 Spark는 "번역가(JVM)를 끼고 소통하는 외국인 직원"이다. 말은 전달되지만 번역 시간(오버헤드)이 필연적이다. Photon은 "그 나라 언어(C++)를 직접 구사하는 직원"이라 번역 없이 즉각 처리한다. 같은 일을 하지만 속도가 다르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Photon 통합 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│  Spark Driver (JVM)                                         │
│                                                             │
│  SQL 파싱 → Catalyst Optimizer → Physical Plan 생성         │
│                        │                                    │
│                        │  JNI (Java Native Interface)       │
└────────────────────────┼────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│  Spark Executor — Photon Native Layer (C++)                 │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Vectorized Column Batch Processing                   │  │
│  │                                                       │  │
│  │  컬럼 A: [1, 3, 5, 7, 9, 2, 4, 6, …]                │  │
│  │           ↓  SIMD (AVX-512) 적용                     │  │
│  │          한 번에 16개 요소 병렬 연산                   │  │
│  │                                                       │  │
│  │  지원 연산:                                           │  │
│  │    필터 · 프로젝션 · 집계 · 해시 조인 · 윈도우 함수   │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  폴백(Fallback) → JVM Spark 엔진:                           │
│    Python UDF · Scala UDF · 일부 복잡한 서브쿼리            │
└─────────────────────────────────────────────────────────────┘
```

### 2. 벡터화 처리(Vectorized Processing) 원리

행 단위 처리(Row-at-a-time)와 컬럼 단위 벡터화의 차이를 CPU 명령 수로 비교한다.

```
[행 단위 처리 — Tungsten]           [컬럼 단위 벡터화 — Photon]

Row 1: filter(a) → project(b,c)     컬럼 a: [1,3,5,7,9,2,4,6]
Row 2: filter(a) → project(b,c)       → SIMD 필터:  [3,5,7,9] (한 번에)
Row 3: filter(a) → project(b,c)       → SIMD 프로젝션 (한 번에)
Row 4: filter(a) → project(b,c)       → CPU 캐시 히트율 극대화
…N번 개별 반복 …

CPU 명령 수: N × 2회                CPU 명령 수: (N/16) × 2회
                                    → 최대 16배 처리량 증가
```

### 3. Photon 지원 연산 범위

| 연산 종류 | Photon 지원 | 비고 |
|:---|:---|:---|
| 필터 (Filter) | ✅ | `WHERE`, `HAVING` 절 |
| 프로젝션 (Projection) | ✅ | 컬럼 선택·표현식 |
| 집계 (Aggregation) | ✅ | `GROUP BY`, `SUM`, `COUNT`, `AVG` |
| 해시 조인 (Hash Join) | ✅ | BroadcastHashJoin, ShuffleHashJoin |
| 정렬 (Sort) | ✅ | `ORDER BY` |
| 윈도우 함수 (Window) | ✅ | `RANK`, `ROW_NUMBER`, `LAG` |
| Python UDF | ❌ | JVM 폴백 발생 |
| RDD API | ❌ | SQL/DataFrame 전용 |
| 복잡한 중첩 서브쿼리 | 부분 지원 | 일부만 네이티브 처리 |

**📢 섹션 요약 비유**
> Photon의 벡터화는 "100명 달리기 선수를 한 명씩 출발시키는 것(행 처리)과 동시에 100명을 출발시키는 것(컬럼 처리)"의 차이다. SIMD는 단 한 번의 출발 신호로 16명을 동시에 뛰게 하는 스타터 피스톨이다.

---

## Ⅲ. 비교 및 연결

### 1. Photon vs Tungsten vs Velox vs DuckDB

| 비교 항목 | Tungsten | Photon | Velox (Meta) | DuckDB |
|:---|:---|:---|:---|:---|
| 구현 언어 | Java (JVM) | C++ (네이티브) | C++ (네이티브) | C++ (네이티브) |
| 벡터화 방식 | 부분 (Codegen) | 완전 SIMD | 완전 SIMD | 완전 벡터화 |
| 실행 환경 | 오픈소스 Spark | Databricks 전용 | Meta 내부/OSS | 단일 노드 임베디드 |
| 분산 처리 | ✅ | ✅ | ✅ | ❌ |
| 오픈소스 여부 | ✅ | ❌ | ✅ | ✅ |
| 최대 성능 개선 | 기준 | 최대 12배 | 최대 10배+ | 단일 노드 최고 수준 |

### 2. 연결 개념

- **Tungsten Engine**: Photon이 대체·보완하는 Spark의 기존 실행 최적화 계층
- **Apache Arrow**: 컬럼형 메모리 포맷 표준 — Photon의 데이터 교환 기반
- **SIMD**: 현대 CPU의 병렬 처리 명령어 집합 (AVX-256, AVX-512)
- **JNI (Java Native Interface)**: Spark Driver(JVM)와 Photon C++ 레이어 간 통신 인터페이스

**📢 섹션 요약 비유**
> Tungsten이 "튜닝된 일반 자동차"라면 Photon은 "F1 레이서카"다. 일반 도로(범용 워크로드)에서는 튜닝 자동차도 충분하지만, 트랙(SQL 쿼리 집약 워크로드)에서는 F1이 압도적이다. 단, F1은 특정 트랙(Databricks) 전용이라 아무 도로나 달릴 수는 없다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 1. Photon 활성화 확인 (Databricks 환경)

```python
# Databricks Runtime — Photon은 자동 활성화 (별도 설정 불필요)
# SQL Warehouse는 Pro/Serverless 타입에서 Photon 기본 사용

# Spark UI → Physical Plan에서 PhotonXxx 노드 확인
# 예: PhotonSortMergeJoin, PhotonGroupByAggregate, PhotonFilter

# Python UDF → Pandas UDF(벡터화)로 전환하여 폴백 최소화
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf("double")
def multiply_udf(x: pd.Series) -> pd.Series:
    return x * 2.0   # 컬럼 단위 처리 → Photon 파이프라인 유지
```

### 2. 워크로드별 Photon 효과

| 워크로드 유형 | Photon 효과 | 핵심 이유 |
|:---|:---|:---|
| BI/대시보드 SQL | ✅ 최대 (최대 12배) | 집계·필터·조인 중심 |
| SQL 기반 ETL | ✅ 높음 | 대량 필터링·변환 반복 |
| ML Feature Engineering | ✅ 보통 | SQL 연산 비율에 따라 가변 |
| Python UDF 집약 | ❌ 낮음 | 빈번한 JVM 폴백 발생 |
| 단순 스트리밍 수집 | △ 제한적 | 변환이 단순할수록 효과 낮음 |

### 3. 도입 체크리스트

- [ ] Databricks Runtime LTS 버전 사용 확인 (11.3 LTS 이상 권장)
- [ ] SQL Warehouse 타입: Classic → Pro/Serverless (Photon 기본 활성화)
- [ ] Photon 폴백 빈발 원인 분석 — Python UDF → `pandas_udf` 교체 검토
- [ ] Databricks Query History에서 쿼리별 Photon 사용 비율 모니터링
- [ ] 벤더 종속(Vendor Lock-in) 리스크 평가 — 오픈소스 대안(Velox, DuckDB) 비교

### 4. 안티패턴

| 안티패턴 | 문제점 | 권장 대안 |
|:---|:---|:---|
| Python UDF 남발 | 모든 연산이 JVM 폴백 → Photon 무효화 | Spark SQL 함수 또는 `pandas_udf` 사용 |
| RDD API 혼용 | Photon 적용 불가 영역 발생 | DataFrame/SQL API로 전환 |
| 폴백 미모니터링 | 성능 저하 원인 파악 불가 | Spark UI · Photon 지표 정기 검토 |

**📢 섹션 요약 비유**
> Photon 도입 판단은 "주방 메뉴에 따라 최신 조리 장비를 투자하는 결정"이다. 메뉴가 SQL 중심이면 최신 장비(Photon)가 압도적 효과를 내지만, 메뉴가 Python UDF 위주면 장비를 바꿔도 요리사(JVM 폴백) 병목이 남는다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 범주 | 내용 | 수치 |
|:---|:---|:---|
| 쿼리 성능 향상 | SQL 집계·조인·필터 워크로드 | 최대 12배 (Databricks 발표) |
| CPU 활용 효율 | SIMD 병렬 처리로 단일 코어 처리량 증가 | 이론 최대 16배 (AVX-512) |
| 비용 절감 | 동일 연산에 클러스터 실행 시간 단축 | 클러스터 비용 최대 수십 % 절감 |
| 개발 생산성 | 코드 변경 없이 성능 향상 | 마이그레이션 비용 Zero |

### 2. 미래 방향

Databricks는 Photon을 Delta Lake와 더 깊이 통합하고 있으며, Python 로직 포함 적용 범위를 지속 확장 중이다. Meta의 Velox, Intel의 OAP (Optimized Analytics Package) 등 유사한 네이티브 실행 엔진이 경쟁적으로 발전하고 있어, 오픈소스 Spark에도 유사한 네이티브 엔진이 통합될 전망이다.

### 3. 결론

Photon Engine은 JVM의 구조적 한계(GC, 인터프리터 오버헤드, SIMD 미활용)를 C++ 네이티브 실행으로 우회하는 현실적 해법이다. 기술사 답안에서는 "JVM 한계 → C++ 네이티브 + 벡터화 → SIMD 활용 → SQL 집약 워크로드에서 극대화"의 논리 흐름과 함께, **Databricks 전용이라는 벤더 종속 리스크**를 균형 있게 서술해야 한다.

**📢 섹션 요약 비유**
> Photon Engine은 "스포츠카 전용 엔진을 일반 자동차 섀시에 이식한 것"이다. 직선 도로(SQL 쿼리)에서는 믿기 어려운 속도를 내지만, 오프로드(Python UDF)에서는 다시 일반 엔진(JVM)으로 전환해야 한다. 그리고 이 엔진은 특정 차고(Databricks)에서만 정비·제공된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Tungsten Engine | Photon이 대체·보완하는 JVM 기반 Spark 실행 최적화 계층 |
| SIMD (AVX-512) | CPU 레벨 병렬 처리 명령어 — Photon 벡터화의 핵심 기반 기술 |
| Apache Arrow | 컬럼형 메모리 포맷 표준 — Photon의 데이터 교환 기반 |
| JNI | Spark Driver(JVM)와 Photon C++ 레이어 간 통신 인터페이스 |
| Databricks SQL Warehouse | Photon이 기본 실행 엔진으로 사용되는 서비스 환경 |
| Pandas UDF | Python 로직의 벡터화 처리를 위한 JVM 폴백 최소화 대안 |
| Velox (Meta) | Meta가 개발한 유사 목적의 오픈소스 네이티브 벡터화 엔진 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Apache Spark 초기 — RDD, JVM 기반 분산 처리]
    │
    ▼
[Tungsten Engine — JVM 내 메모리 관리 + Codegen 최적화]
    │
    ▼
[Photon Engine — C++ 네이티브 + SIMD 벡터화 (Databricks)]
    │
    ▼
[Velox / OAP — 오픈소스 네이티브 벡터화 엔진 경쟁]
    │
    ▼
[차세대 — Python 로직 포함 전체 파이프라인 네이티브화]
```

Tungsten이 JVM 안에서의 최적화였다면, Photon은 JVM 자체를 우회하는 아키텍처 전환이다. 네이티브 실행 엔진 경쟁은 오픈소스 생태계 전반으로 확산되고 있다.

### 👶 어린이를 위한 3줄 비유 설명

1. 기존 Spark는 계산원이 숫자를 하나씩 입력하는 마트 계산대예요. Photon은 모든 물건을 한 번에 스캔하는 첨단 자동 계산대라 훨씬 빠르게 계산해요.
2. C++로 만들어서 통역사(JVM) 없이 컴퓨터가 바로 알아듣는 말을 하니까, 통역 시간 낭비 없이 바로 처리할 수 있어요.
3. 단, 이 자동 계산대는 특수 바코드(Python UDF)는 인식 못 해서 그런 물건은 일반 계산대(JVM)에 다시 가져가야 해요.
