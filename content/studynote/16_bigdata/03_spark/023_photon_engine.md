+++
weight = 23
title = "23. Photon Engine (Databricks) — 네이티브 벡터화 실행 엔진"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)

- **본질**: Photon Engine (포톤 엔진)은 Databricks가 개발한 C++ 기반 네이티브 벡터화(Vectorized) SQL 실행 엔진으로, JVM 위에서 동작하는 기존 Spark 실행 엔진의 JVM 오버헤드와 행(Row) 단위 처리 한계를 극복하기 위해 컬럼(Column) 단위 배치 처리와 SIMD (Single Instruction Multiple Data) 명령어를 활용한다.
- **가치**: Photon은 Spark API와 완전 호환되어 기존 코드 변경 없이 특히 SQL 집계, 조인, 필터 등 쿼리 집약적 워크로드에서 최대 12배 이상의 성능 향상을 제공하며, Databricks SQL Warehouse에서 기본 실행 엔진으로 사용된다.
- **판단 포인트**: Photon은 Databricks Runtime 전용이므로 오픈소스 Spark 환경에서는 사용 불가이며, Python UDF나 복잡한 사용자 정의 함수처럼 JVM이 필요한 연산은 여전히 Spark JVM 엔진으로 폴백(Fallback)되므로 모든 워크로드에서 동일한 성능 향상을 기대할 수는 없다.

---

## Ⅰ. 개요 및 필요성

### 1. 기존 Spark 실행 엔진의 한계

Tungsten 엔진이 Spark의 JVM 오버헤드를 크게 줄였지만, 근본적인 한계가 있었다.

- **JVM 인터프리터 오버헤드**: Java Bytecode 실행, JIT 컴파일 지연
- **행 단위 처리(Row-at-a-time)**: 각 행을 개별 처리하여 CPU 캐시 효율이 낮음
- **동적 타입 해석**: 런타임에 타입 체크 비용 발생

CPU의 SIMD 명령어(AVX-512 등)를 활용하면 한 번에 16개 이상의 정수를 동시에 처리할 수 있지만, JVM에서는 이를 완전히 활용하기 어렵다.

### 2. Photon의 접근 방식

Photon은 C++로 작성된 **네이티브 실행 엔진**이다. JVM 위에서 실행되지 않고, JNI (Java Native Interface)를 통해 Spark Driver와 통신하면서 실제 데이터 처리는 C++ 레이어에서 직접 수행한다.

**📢 섹션 요약 비유**
> 기존 Spark는 "번역가(JVM)를 통해 소통하는 외국인 직원"이다. 말이 전달되지만 번역 시간(오버헤드)이 있다. Photon은 "그 나라 언어(C++)를 직접 하는 직원"이라 번역 없이 즉각 처리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Photon 아키텍처 다이어그램

```
┌────────────────────────────────────────────────────────────┐
│  Spark Driver (JVM)                                        │
│  SQL 파싱 → Catalyst 최적화 → 물리 계획                   │
│                         │                                  │
│                         │ 물리 계획 전달                   │
└─────────────────────────┼──────────────────────────────────┘
                          │ JNI 인터페이스
┌─────────────────────────▼──────────────────────────────────┐
│  Photon Engine (C++ Native Layer) — Executor 내부          │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  컬럼형 배치 처리 (Columnar Batch Processing)         │  │
│  │  · 컬럼 단위 벡터(Vector) = CPU 레지스터 크기로 처리  │  │
│  │  · SIMD (AVX-512) 활용 → 병렬 산술 연산               │  │
│  │  · 런타임 코드 생성 (LLVM 기반)                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  지원: 필터, 프로젝션, 집계, 해시 조인, 윈도우 함수         │
│                                                            │
│  미지원 → JVM Spark 폴백:                                  │
│    · Python/Scala UDF                                      │
│    · 일부 복잡한 서브쿼리                                   │
└────────────────────────────────────────────────────────────┘
```

### 2. 벡터화 처리(Vectorized Processing) 원리

```
행 단위(Row-at-a-time) 처리:          컬럼 단위(Columnar) 벡터화:
  Row 1: filter(a) → project(b,c)      컬럼 a: [1,3,5,7,9,2,4,6]
  Row 2: filter(a) → project(b,c)       → SIMD 필터 적용: [3,5,7] (한 번에)
  Row 3: filter(a) → project(b,c)       → SIMD 프로젝션 (한 번에)
  ...N번 반복                           → CPU 캐시 최적화

CPU 명령 수: N개                        CPU 명령 수: N/16개 (SIMD 16-wide)
```

### 3. Photon 지원 연산 범위

| 연산 종류 | Photon 지원 | 비고 |
|:---|:---|:---|
| 필터 (Filter) | ✅ | `WHERE`, `HAVING` 절 |
| 집계 (Aggregation) | ✅ | `GROUP BY`, `SUM`, `COUNT` |
| 해시 조인 (Hash Join) | ✅ | BroadcastHashJoin, ShuffleHashJoin |
| 정렬 (Sort) | ✅ | `ORDER BY` |
| 윈도우 함수 (Window) | ✅ | `RANK`, `ROW_NUMBER` |
| Python UDF | ❌ | JVM 폴백 |
| RDD API | ❌ | Photon은 SQL/DataFrame 전용 |
| 복잡한 중첩 서브쿼리 | 부분 지원 | 일부만 네이티브 처리 |

**📢 섹션 요약 비유**
> Photon의 벡터화는 "100미터 달리기 선수가 한 번에 1명씩 뛰는 것(행 처리) vs 100명이 나란히 동시에 출발하는 것(컬럼 처리)"이다. SIMD는 총 한 방에 100명을 동시에 출발시키는 출발 신호와 같다.

---

## Ⅲ. 비교 및 연결

### 1. Photon vs Tungsten vs DuckDB

| 비교 항목 | Tungsten | Photon | DuckDB |
|:---|:---|:---|:---|
| 구현 언어 | Java (JVM) | C++ (네이티브) | C++ (네이티브) |
| 벡터화 | 부분 (Codegen) | 완전 SIMD 벡터화 | 완전 벡터화 |
| 환경 | 오픈소스 Spark | Databricks 전용 | 단일 노드/임베디드 |
| 분산 처리 | ✅ | ✅ | ❌ (단일 노드) |
| Python UDF | 느림 | 폴백 (JVM) | 지원 안함 |
| 성능 개선 배율 | 기준 | 최대 12배 (쿼리 집약) | 단일 노드 최고 수준 |

### 2. 연결 개념

- **Tungsten Engine**: Photon이 대체/보완하는 Spark의 기존 실행 최적화
- **Vectorized Query Execution**: Photon이 채택한 Apache Arrow 기반 컬럼형 처리 패러다임
- **SIMD (Single Instruction Multiple Data)**: 현대 CPU의 병렬 처리 명령어 집합

**📢 섹션 요약 비유**
> Tungsten이 "튜닝된 일반 자동차"라면, Photon은 "F1 레이서카"다. 일반 도로(범용 워크로드)에서는 튜닝 자동차도 충분하지만, 트랙(SQL 쿼리 집약 워크로드)에서는 F1 레이서카가 압도적이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 1. Photon 활성화 (Databricks 환경)

```python
# Databricks Runtime 자동 활성화 - 별도 설정 불필요
# Databricks SQL Warehouse는 기본적으로 Photon 사용

# 확인 방법: Spark UI의 Execution Plan에서 "PhotonXxx" 노드 확인
# 예: PhotonSortMergeJoin, PhotonGroupByAggregate

# Python UDF 성능 문제 시 Pandas UDF(벡터화)로 전환 권장
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf("double")
def my_udf(x: pd.Series) -> pd.Series:
    return x * 2.0  # Pandas UDF는 컬럼 단위 처리
```

### 2. Photon이 효과적인 워크로드

| 워크로드 유형 | Photon 효과 | 이유 |
|:---|:---|:---|
| BI/대시보드 SQL 쿼리 | ✅ 최대 | 집계, 필터, 조인 중심 |
| ETL 변환 (SQL 기반) | ✅ 높음 | 필터링, 변환 다량 |
| ML Feature Engineering | ✅ 보통 | SQL 연산 비율에 따라 |
| Python UDF 집약 | ❌ 낮음 | Photon 폴백 발생 |
| 단순 스트리밍 수집 | △ | 변환이 단순할수록 효과 낮음 |

### 3. 도입 체크리스트

- [ ] Databricks Runtime LTS 버전 사용 확인
- [ ] SQL Warehouse 타입: Classic → Pro/Serverless (Photon 기본 활성화)
- [ ] Photon 폴백이 잦은 Python UDF → pandas_udf로 교체 검토
- [ ] Photon 성능 확인: Databricks Query History에서 쿼리별 Photon 사용 비율 확인

**📢 섹션 요약 비유**
> Photon 도입 판단은 "기업 식당 메뉴에 따라 주방 장비를 업그레이드하는 결정"이다. 메뉴가 SQL 중심이면 새 장비(Photon)가 압도적 효과를 내지만, 메뉴가 파이썬 UDF 위주면 장비만 바꿔도 요리사(JVM 폴백) 병목이 남는다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 수치 |
|:---|:---|
| SQL 쿼리 성능 | 최대 12배 향상 (Databricks 발표) |
| CPU 활용 효율 | SIMD로 단일 코어 처리량 대폭 증가 |
| 비용 절감 | 동일 연산에 더 짧은 클러스터 실행 시간 |

### 2. 결론

Photon Engine은 Databricks 생태계에서 SQL/데이터 엔지니어링 워크로드의 성능을 획기적으로 향상시키는 네이티브 실행 엔진이다. 기술사 답안에서는 "JVM 한계 → C++ 네이티브 + 벡터화 → SIMD 활용 → SQL 쿼리 집약 워크로드에서 극대화"의 논리 흐름과, Databricks 전용이라는 **벤더 종속(Vendor Lock-in) 리스크**를 함께 서술하는 것이 균형 잡힌 답안이다.

**📢 섹션 요약 비유**
> Photon Engine은 "스포츠카 전용 엔진을 일반 자동차 섀시에 이식한 것"이다. 직선 도로(SQL 쿼리)에서는 믿을 수 없는 속도를 내지만, 오프로드(Python UDF)에서는 다시 일반 엔진(JVM)으로 전환해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Tungsten Engine | 대체/보완 대상 | Photon이 등장한 배경, JVM 기반 한계 |
| SIMD | 핵심 기술 | CPU 레벨 병렬 처리 명령어 활용 |
| Apache Arrow | 연관 표준 | 컬럼형 메모리 포맷, Photon의 데이터 교환 기반 |
| Databricks SQL Warehouse | 활용 환경 | Photon 기본 엔진으로 사용 |
| Pandas UDF | 폴백 대안 | Python 로직의 벡터화 처리를 위한 권장 방식 |

### 👶 어린이를 위한 3줄 비유 설명

기존 Spark는 줄 세워서 한 명씩 처리하는 슈퍼마켓 계산대이고, Photon은 여러 계산대를 동시에 운영하는 셀프 스캔 자동화 계산대예요. C++로 직접 만들어서 번역(JVM) 없이 바로 계산하니까 훨씬 빨라요! 단, 자동화 계산대(Photon)가 인식 못 하는 특수 물건(Python UDF)은 여전히 일반 계산대(JVM)에서 처리해야 해요.
