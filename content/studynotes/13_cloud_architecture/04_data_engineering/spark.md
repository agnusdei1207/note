+++
title = "아파치 스파크 (Apache Spark)"
date = "2026-03-05"
[extra]
categories = "studynotes-cloud"
tags = ["spark", "bigdata", "in-memory", "distributed-computing", "data-engineering"]
+++

# 아파치 스파크 (Apache Spark)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 아파치 스파크는 RDD(Resilient Distributed Dataset)를 핵심 추상화로 하는 인메모리 분산 컴퓨팅 엔진으로, DAG(Directed Acyclic Graph) 기반 최적화와 Lazy Evaluation으로 하둡 MapReduce 대비 10-100배 빠른 처리 성능을 제공합니다.
> 2. **가치**: 배치 처리, 스트리밍, SQL(Structured API), 머신러닝(MLlib), 그래프 처리(GraphX)를 단일 통합 엔진에서 수행하며, 1PB+ 규모 데이터를 수십 분 내에 분석할 수 있습니다.
> 3. **융합**: Delta Lake와 결합하여 ACID 트랜잭션을 제공하고, Kubernetes/YARN/Mesos에서 실행되며, 데이터 레이크하우스 아키텍처의 핵심 처리 엔진으로 자리 잡았습니다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의
아파치 스파크(Apache Spark)는 UC 버클리 AMPLab에서 개발된 후 2013년 아파치 재단에 기부된 오픈소스 통합 분석 엔진입니다. 스파크는 데이터를 메모리에 캐싱하여 반복적 접근 시 디스크 I/O 병목을 제거하고, 통합 API(Scala, Java, Python, R)로 배치, 스트리밍, ML, 그래프 처리를 일관되게 수행합니다.

### 💡 비유
스파크는 "초고속 분산 주방"과 같습니다. 하둡 MapReduce가 요리할 때마다 재료를 창고(디스크)에서 꺼내고 다시 넣는 방식이라면, 스파크는 재료를 조리대(메모리) 위에 올려두고 여러 요리를 연달아 만듭니다. 수십 명의 요리사(Executor)가 레시피(DAG)를 보고 병렬로 요리하며, 한 요리사가 아파도 다른 요리사가 대신합니다.

### 등장 배경 및 발전 과정

#### 1. MapReduce의 한계
- **디스크 I/O 병목**: Map → Shuffle → Reduce 간 매번 디스크 쓰기
- **반복 알고리즘 비효율**: ML 알고리즘은 동일 데이터에 여러 번 접근
- **복잡한 파이프라인**: 여러 MR 잡을 연결하면 중간 결과 디스크 저장

#### 2. 패러다임 변화
```
2009년: UC Berkeley AMPLab, Spark 프로젝트 시작
2013년: Apache Spark 0.8.0, Top-level 프로젝트 승격
2014년: Spark 1.0, DataFrames API 도입
2015년: Spark 1.3, DataFrame → Dataset 통합 시작
2016년: Spark 2.0, Structured Streaming 발표
2017년: Spark 2.2, Spark R 개선
2019년: Spark 3.0, GPU 지원, Adaptive Query Execution
2022년: Spark 3.3, Photon(C++ 엔진), Python 지원 강화
2024년: Spark 4.0, Connect Protocol, AI/LLM 통합
```

#### 3. 비즈니스적 요구사항
- **실시간 분석**: 로그/센서 데이터 실시간 처리
- **ML 파이프라인**: 특징 추출 → 학습 → 예측 통합
- **대화형 쿼리**: BI 도구로 수초 내 응답

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|-----------|------|
| **Driver Program** | 잡 실행 제어 | SparkContext, DAG 생성, 스케줄링 | main(), SparkSession | 총괄 셰프 |
| **Cluster Manager** | 자원 할당 | Executor 실행, 자원 요청/해제 | YARN, K8s, Mesos, Standalone | 주방 관리자 |
| **Executor** | 태스크 실행 | 스레드 풀, 메모리 저장소, 셔플 서비스 | JVM Process | 요리사 |
| **RDD** | 불변 분산 데이터셋 | 파티션, 의존성(Lineage), 계산 함수 | Transformation, Action | 식재료 묶음 |
| **DataFrame/Dataset** | 구조화된 분산 데이터셋 | Catalyst 옵티마이저, Tungsten 실행 | SQL, DSL | 레시피 카드 |
| **DAG Scheduler** | 스테이지 분할 | Shuffle Boundary 기준, 스테이지 생성 | Stage, Task | 요리 순서 계획 |
| **TaskScheduler** | 태스크 할당 | 파티션 → 태스크 매핑, 재시도 | TaskSet, Speculation | 주문 배정 |
| **Shuffle Service** | 데이터 교환 | Map 출력 정렬/병합, Reduce Fetch | SortShuffleManager | 재료 전달대 |
| **BlockManager** | 메모리/디스크 저장소 | LRU 캐시, 메모리 관리 | MemoryStore, DiskStore | 냉장고/창고 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          아파치 스파크 실행 아키텍처                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │                        Driver Program                                    │  │
│   │  ┌───────────────────────────────────────────────────────────────────┐  │  │
│   │  │                        SparkSession                                │  │  │
│   │  │                                                                   │  │  │
│   │  │  val spark = SparkSession.builder()                              │  │  │
│   │  │    .appName("DataPipeline")                                      │  │  │
│   │  │    .master("yarn")                                               │  │  │
│   │  │    .config("spark.sql.shuffle.partitions", 200)                  │  │  │
│   │  │    .getOrCreate()                                                │  │  │
│   │  │                                                                   │  │  │
│   │  │  ┌─────────────────────────────────────────────────────────────┐ │  │  │
│   │  │  │              SparkContext                                    │ │  │  │
│   │  │  │  - DAGScheduler: Stage 분할                                  │ │  │  │
│   │  │  │  - TaskScheduler: Task 배분                                  │ │  │  │
│   │  │  │  - SchedulerBackend: Cluster Manager 통신                   │ │  │  │
│   │  │  └─────────────────────────────────────────────────────────────┘ │  │  │
│   │  │                                                                   │  │  │
│   │  │  ┌─────────────────────────────────────────────────────────────┐ │  │  │
│   │  │  │              Catalyst Optimizer                              │ │  │  │
│   │  │  │                                                              │ │  │  │
│   │  │  │  Unresolved Logical Plan                                     │ │  │  │
│   │  │  │       ↓ (Analysis)                                           │ │  │  │
│   │  │  │  Resolved Logical Plan                                       │ │  │  │
│   │  │  │       ↓ (Optimization)                                       │ │  │  │
│   │  │  │  Optimized Logical Plan                                      │ │  │  │
│   │  │  │       ↓ (Physical Planning)                                  │ │  │  │
│   │  │  │  Physical Plan (SparkPlan)                                   │ │  │  │
│   │  │  │       ↓ (Code Generation)                                    │ │  │  │
│   │  │  │  RDDs (Execution)                                            │ │  │  │
│   │  │  └─────────────────────────────────────────────────────────────┘ │  │  │
│   │  └───────────────────────────────────────────────────────────────────┘  │  │
│   └─────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                          │
│                                      ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │                      Cluster Manager                                     │  │
│   │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │  │
│   │  │    YARN     │ │ Kubernetes  │ │   Mesos     │ │ Standalone  │       │  │
│   │  │ ResourceManager│ │ K8s API │ │ Mesos Master│ │ Master      │       │  │
│   │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘       │  │
│   │                                                                         │  │
│   │  리소스 요청: driver.memory, executor.memory, executor.cores          │  │
│   └─────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                          │
│          ┌───────────────────────────┼───────────────────────────┐              │
│          │                           │                           │              │
│          ▼                           ▼                           ▼              │
│   ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐     │
│   │   Worker Node 1 │       │   Worker Node 2 │       │   Worker Node 3 │     │
│   │  ┌───────────┐  │       │  ┌───────────┐  │       │  ┌───────────┐  │     │
│   │  │ Executor  │  │       │  │ Executor  │  │       │  │ Executor  │  │     │
│   │  │ (JVM)     │  │       │  │ (JVM)     │  │       │  │ (JVM)     │  │     │
│   │  │           │  │       │  │           │  │       │  │           │  │     │
│   │  │ ┌───────┐ │  │       │  │ ┌───────┐ │  │       │  │ ┌───────┐ │  │     │
│   │  │ │ Task  │ │  │       │  │ │ Task  │ │  │       │  │ │ Task  │ │  │     │
│   │  │ │Thread1│ │  │       │  │ │Thread1│ │  │       │  │ │Thread1│ │  │     │
│   │  │ ├───────┤ │  │       │  │ ├───────┤ │  │       │  │ ├───────┤ │  │     │
│   │  │ │ Task  │ │  │       │  │ │ Task  │ │  │       │  │ │ Task  │ │  │     │
│   │  │ │Thread2│ │  │       │  │ │Thread2│ │  │       │  │ │Thread2│ │  │     │
│   │  │ ├───────┤ │  │       │  │ ├───────┤ │  │       │  │ ├───────┤ │  │     │
│   │  │ │ Task  │ │  │       │  │ │ Task  │ │  │       │  │ │ Task  │ │  │     │
│   │  │ │Thread3│ │  │       │  │ │Thread3│ │  │       │  │ │Thread3│ │  │     │
│   │  │ ├───────┤ │  │       │  │ ├───────┤ │  │       │  │ ├───────┤ │  │     │
│   │  │ │ Task  │ │  │       │  │ │ Task  │ │  │       │  │ │ Task  │ │  │     │
│   │  │ │Thread4│ │  │       │  │ │Thread4│ │  │       │  │ │Thread4│ │  │     │
│   │  │ └───────┘ │  │       │  │ └───────┘ │  │       │  │ └───────┘ │  │     │
│   │  │           │  │       │  │           │  │       │  │           │  │     │
│   │  │ ┌───────┐ │  │       │  │ ┌───────┐ │  │       │  │ ┌───────┐ │  │     │
│   │  │ │Memory │ │  │       │  │ │Memory │ │  │       │  │ │Memory │ │  │     │
│   │  │ │Store  │ │  │       │  │ │Store  │ │  │       │  │ │Store  │ │  │     │
│   │  │ │(Cache)│ │  │       │  │ │(Cache)│ │  │       │  │ │(Cache)│ │  │     │
│   │  │ └───────┘ │  │       │  │ └───────┘ │  │       │  │ └───────┘ │  │     │
│   │  │           │  │       │  │           │  │       │  │           │  │     │
│   │  │ ┌───────┐ │  │       │  │ ┌───────┐ │  │       │  │ ┌───────┐ │  │     │
│   │  │ │Shuffle│ │  │       │  │ │Shuffle│ │  │       │  │ │Shuffle│ │  │     │
│   │  │ │Service│ │◀─┼───────┼─▶│Service│ │◀─┼───────┼─▶│Service│ │  │     │
│   │  │ └───────┘ │  │       │  │ └───────┘ │  │       │  │ └───────┘ │  │     │
│   │  └───────────┘  │       │  └───────────┘  │       │  └───────────┘  │     │
│   └─────────────────┘       └─────────────────┘       └─────────────────┘     │
│                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │                          DAG Execution                                   │  │
│   │                                                                          │  │
│   │   DataFrame API:                                                         │  │
│   │   df.filter($"age" > 18)                                                │  │
│   │     .groupBy($"country")                                                │  │
│   │     .agg(avg($"salary"))                                                │  │
│   │     .write.parquet("/output")                                           │  │
│   │                                                                          │  │
│   │   ┌────────────────────────────────────────────────────────────────┐   │  │
│   │   │                     Logical Plan                                │   │  │
│   │   │                                                                 │   │  │
│   │   │   [Parquet Scan] → [Filter (age > 18)] → [HashAggregate]       │   │  │
│   │   │                          ↓                                     │   │  │
│   │   │                    [Exchange (Shuffle)]                         │   │  │
│   │   │                          ↓                                     │   │  │
│   │   │                    [HashAggregate (Final)]                     │   │  │
│   │   │                          ↓                                     │   │  │
│   │   │                    [Parquet Write]                             │   │  │
│   │   └────────────────────────────────────────────────────────────────┘   │  │
│   │                                                                          │  │
│   │   ┌────────────────────────────────────────────────────────────────┐   │  │
│   │   │                   Stage Division                                │   │  │
│   │   │                                                                 │   │  │
│   │   │   Stage 1 (No Shuffle)          Stage 2 (After Shuffle)        │   │  │
│   │   │   ┌──────────────────┐          ┌──────────────────┐          │   │  │
│   │   │   │ Scan → Filter    │ ───────▶ │ Aggregate Final  │          │   │  │
│   │   │   │ Aggregate Partial│ Shuffle  │ Write            │          │   │  │
│   │   │   └──────────────────┘          └──────────────────┘          │   │  │
│   │   │                                                                 │   │  │
│   │   │   Tasks: 200 partitions        Tasks: 200 partitions          │   │  │
│   │   │   (Parallel across nodes)       (After shuffle)                │   │  │
│   │   └────────────────────────────────────────────────────────────────┘   │  │
│   └─────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

#### ① Lazy Evaluation과 RDD Lineage

```python
"""
Spark Lazy Evaluation 및 Lineage 메커니즘
"""

from pyspark.sql import SparkSession
from pyspark import SparkContext

# ============================================
# Lazy Evaluation (지연 평가)
# ============================================
"""
Spark의 핵심 원리: Transformation은 즉시 실행되지 않음

Transformation (지연):
- map, filter, groupBy, join, flatMap
- DAG에 연산만 기록
- 실제 데이터 처리 안 함

Action (즉시 실행):
- count, collect, save, show, take
- DAG 실행 트리거
- 결과 반환 또는 저장
"""

# 예시
spark = SparkSession.builder.appName("LazyEval").getOrCreate()
df = spark.read.parquet("/data/users")  # 1. 메타데이터만 읽음

# Transformation - 실행 안 됨 (Logical Plan만 생성)
filtered = df.filter(df.age > 18)       # 2. Plan에 추가
grouped = filtered.groupBy("country")   # 3. Plan에 추가
result = grouped.count()                # 4. Plan에 추가

# 여기까지는 아무런 데이터 처리가 일어나지 않음!

# Action - 이때 실행 시작
result.show()  # 5. DAG 실행, 결과 반환

# ============================================
# RDD Lineage (계보)와 Fault Tolerance
# ============================================
"""
Lineage: RDD가 어떻게 생성되었는지의 전체 이력

복구 메커니즘:
- Executor 장애 시 Lineage를 따라 재계산
- 체크포인트로 Lineage 단축 가능
"""

class RDDLineageExample:
    """RDD Lineage 시뮬레이션"""

    def __init__(self, spark_context: SparkContext):
        self.sc = spark_context

    def demonstrate_lineage(self):
        # 원본 데이터
        rdd1 = self.sc.textFile("hdfs:///data/input.txt")
        # Lineage: HadoopRDD

        rdd2 = rdd1.map(lambda x: x.split(","))
        # Lineage: HadoopRDD -> MapPartitionsRDD

        rdd3 = rdd2.filter(lambda x: len(x) > 3)
        # Lineage: HadoopRDD -> MapPartitionsRDD -> MapPartitionsRDD

        rdd4 = rdd3.map(lambda x: (x[0], int(x[1])))
        # Lineage: HadoopRDD -> MapPartitionsRDD -> MapPartitionsRDD -> MapPartitionsRDD

        # Lineage 확인
        print(rdd4.toDebugString())
        # 출력:
        # (4) MapPartitionsRDD[3] at map
        #  |  MapPartitionsRDD[2] at filter
        #  |  MapPartitionsRDD[1] at map
        #  |  hdfs:///data/input.txt HadoopRDD[0] at textFile

        # 장애 복구:
        # Executor 2가 rdd4의 파티션 1을 처리하다 장애 발생
        # -> Driver는 Lineage를 참조하여
        # -> hdfs:///data/input.txt의 해당 파티션부터 재계산

    def checkpoint_example(self):
        """
        체크포인트: Lineage를 끊고 디스크에 저장
        긴 Lineage의 메모리 절약 및 복구 시간 단축
        """
        self.sc.setCheckpointDir("hdfs:///checkpoints")

        rdd = self.sc.textFile("hdfs:///data/input.txt")
        rdd = rdd.map(...).filter(...).map(...)  # 긴 Lineage

        # 체크포인트
        rdd.checkpoint()
        rdd.count()  # Action 시 체크포인트 저장

        # 이후 Lineage는 체크포인트 파일에서 시작
        print(rdd.toDebugString())
        # 출력:
        # (4) MapPartitionsRDD[3] at checkpoint
        #  |  ReliableCheckpointRDD[4] at checkpoint


# ============================================
# Catalyst Optimizer (SQL 최적화)
# ============================================
"""
Catalyst: Spark SQL의 옵티마이저

최적화 규칙:
1. Predicate Pushdown: 필터를 데이터 소스 쪽으로 이동
2. Column Pruning: 필요한 컬럼만 읽기
3. Constant Folding: 상수 계산 미리 수행
4. Join Reordering: 조인 순서 최적화
"""

# 최적화 예시
"""
원본 쿼리:
SELECT name, age
FROM users
WHERE age > 18 AND country = 'KR'

Catalyst 최적화:
1. Predicate Pushdown:
   - Parquet에서 age > 18 AND country = 'KR' 필터 적용
   - 데이터 소스 레벨에서 행 스킵

2. Column Pruning:
   - name, age 컬럼만 읽기
   - 다른 컬럼 무시

결과:
- I/O 90% 감소 (필요한 데이터만 읽음)
- 처리 시간 80% 감소
"""
```

#### ② 메모리 관리와 Tungsten

```python
"""
Spark 메모리 관리 및 Tungsten 엔진
"""

# ============================================
# Executor 메모리 구조
# ============================================
"""
spark.executor.memory = 16g (예시)

┌─────────────────────────────────────────────────────────────┐
│                    Executor Memory (16GB)                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          Reserved Memory (300MB)                    │   │
│  │          (JVM 내부 오브젝트)                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          Spark Memory (15.7GB)                      │   │
│  │                                                     │   │
│  │  ┌─────────────────────┐  ┌─────────────────────┐  │   │
│  │  │  Storage Memory     │  │  Execution Memory   │  │   │
│  │  │  (spark.memory.     │  │  (spark.memory.     │  │   │
│  │  │   storageFraction   │  │   storageFraction   │  │   │
│  │  │   = 0.5)            │  │   = 1 - 0.5)        │  │   │
│  │  │                     │  │                     │  │   │
│  │  │  - Cached 데이터    │  │  - Shuffle 버퍼     │  │   │
│  │  │  - Broadcast 변수   │  │  - Join 버퍼        │  │   │
│  │  │  - RDD 파티션       │  │  - 집계 버퍼        │  │   │
│  │  │                     │  │                     │  │   │
│  │  │  7.85GB             │  │  7.85GB             │  │   │
│  │  └─────────────────────┘  └─────────────────────┘  │   │
│  │                                                     │   │
│  │  Unified Memory Management (서로 차용 가능)         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
"""

# ============================================
# Tungsten Execution Engine
# ============================================
"""
Tungsten: CPU/메모리 효율 극대화

핵심 기술:
1. Off-Heap Memory: JVM GC 회피
2. Cache-Aware Layout: CPU 캐시 친화적 데이터 배치
3. Code Generation: 런타임 바이트코드 생성
"""

# Whole-Stage Code Generation 예시
"""
쿼리:
SELECT name FROM users WHERE age > 18

Before (Volcano Model):
- 각 연산자가 iterator로 next() 호출
- 가상 함수 호출 오버헤드
- 중간 데이터 materialization

After (Whole-Stage Code Gen):
- 전체 스테이지를 하나의 함수로 컴파일
- LLVM 최적화 적용
- CPU 레지스터 최대 활용

생성된 코드 (개념적):
"""
def generated_pipeline(batch):
    results = []
    for row in batch:
        # Filter
        if row.age > 18:
            # Project
            results.append(row.name)
    return results


# ============================================
# Spark 3.0+ Adaptive Query Execution (AQE)
# ============================================
"""
AQE: 런타임 쿼리 최적화

특징:
1. 동적 Shuffle 파티션 병합
2. 동적 조인 전략 전환
3. 스큐(Skew) 조인 최적화
"""

AQE_CONFIG = {
    # AQE 활성화
    "spark.sql.adaptive.enabled": "true",

    # Shuffle 파티션 병합
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.initialPartitionNum": "200",
    "spark.sql.adaptive.coalescePartitions.minPartitionSize": "1MB",
    "spark.sql.adaptive.coalescePartitions.maxPartitionSize": "128MB",

    # 조인 전략 전환
    "spark.sql.adaptive.localShuffleReader.enabled": "true",

    # 스큐 조인
    "spark.sql.adaptive.skewJoin.enabled": "true",
    "spark.sql.adaptive.skewJoin.skewedPartitionFactor": "5",
    "spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes": "256MB",
}

"""
AQE 동작 예시:

1. Shuffle 파티션 병합:
   - 초기: 200 파티션
   - 런타임 측정: 대부분 파티션이 1MB 미만
   - 병합: 200 → 20 파티션
   - 효과: 태스크 스케줄링 오버헤드 90% 감소

2. 스큐 조인:
   - 감지: 파티션 A가 평균의 10배 크기
   - 처리: 파티션 A를 10개로 분할
   - 효과: 스트라글러 태스크 제거
"""
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Spark vs MapReduce

| 비교 항목 | Hadoop MapReduce | Apache Spark | 차이 분석 |
|-----------|------------------|--------------|-----------|
| **처리 방식** | 디스크 기반 | 메모리 기반 | 10-100배 빠름 |
| **I/O 패턴** | 매 단계 디스크 쓰기 | 메모리 캐싱 | 반복 알고리즘에 유리 |
| **프로그래밍 모델** | Map/Reduce 고정 | DAG 기반 유연 | 복잡한 파이프라인 용이 |
| **API** | Java Verbose | Scala/Python/R 간결 | 생산성 5-10배 |
| **실시간 처리** | 불가능 | Structured Streaming | 통합 엔진 |
| **ML 지원** | Mahout (MR 기반) | MLlib (인메모리) | 10-100배 빠름 |
| **내고장성** | 재시작 | Lineage 기반 복구 | 둘 다 강력 |

### 과목 융합 관점 분석

#### [클라우드 + 운영체제] 메모리 관리와 GC
```
Spark JVM 튜닝:

1. G1GC 설정 (기본)
   -XX:+UseG1GC
   -XX:MaxGCPauseMillis=200
   -XX:InitiatingHeapOccupancyPercent=35

2. 메모리 설정
   spark.executor.memory=16g
   spark.memory.fraction=0.6
   spark.memory.storageFraction=0.5

3. Off-Heap 메모리 (Tungsten)
   spark.memory.offHeap.enabled=true
   spark.memory.offHeap.size=4g

4. 문제 해결:
   - OOM: executor.memory 증가 또는 파티션 수 증가
   - GC 과다: G1GC로 전환, off-heap 사용
   - Shuffle Spill: memory.fraction 증가
```

#### [클라우드 + 데이터베이스] Spark SQL과 Delta Lake
```
Delta Lake + Spark 통합:

CREATE TABLE events (
  event_id BIGINT,
  event_time TIMESTAMP,
  user_id STRING,
  event_data STRUCT<...>
) USING DELTA
PARTITIONED BY (date DATE)
LOCATION 's3://lake/events';

-- ACID 트랜잭션
INSERT INTO events VALUES ...;

-- Time Travel (과거 데이터 조회)
SELECT * FROM events VERSION AS OF 5;
SELECT * FROM events TIMESTAMP AS OF '2024-01-01';

-- MERGE (Upsert)
MERGE INTO events t
USING updates s
ON t.event_id = s.event_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- Spark 스트리밍과 통합
stream_df.writeStream
  .format("delta")
  .outputMode("append")
  .option("checkpointLocation", "/checkpoints/events")
  .start("/delta/events")
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 시나리오

#### 시나리오 1: 데이터 레이크하우스 ETL
```
요구사항:
- 일일 10TB 원시 데이터 처리
- 30분 내 ETL 완료
- S3 → Delta Lake 변환
- 비용 최적화

기술사 판단:

1. 클러스터 구성:
   - EMR on EKS (Spot 인스턴스 80%)
   - Driver: 1대 (m5.xlarge)
   - Executor: 50대 (r5.4xlarge, 16vCPU, 128GB)

2. 최적화 설정:
   spark = SparkSession.builder \
       .config("spark.sql.adaptive.enabled", "true") \
       .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
       .config("spark.sql.shuffle.partitions", "auto") \
       .config("spark.executor.memory", "100g") \
       .config("spark.executor.cores", "12") \
       .config("spark.dynamicAllocation.enabled", "true") \
       .config("spark.dynamicAllocation.maxExecutors", "100") \
       .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
       .getOrCreate()

3. Delta Lake 활용:
   - ACID 트랜잭션
   - MERGE for Upsert
   - OPTIMIZE for Compaction

4. 비용:
   - Spot 80% 활용으로 70% 비용 절감
   - Dynamic Allocation으로 유휴 자원 해제
```

### 도입 시 고려사항 체크리스트

#### 기술적 고려사항
- [ ] **파티셔닝**: 데이터 크기에 맞는 파티션 수
- [ ] **메모리 설정**: executor.memory, memory.fraction
- [ ] **Shuffle 최적화**: shuffle.partitions, AQE
- [ ] **직렬화**: KryoSerializer

#### 운영적 고려사항
- [ ] **모니터링**: Spark UI, Ganglia, Prometheus
- [ ] **로깅**: Log4j, S3 업로드
- [ ] **보안**: Kerberos, Ranger

### 주의사항 및 안티패턴

#### 안티패턴 1: 너무 적은 파티션
```
잘못된 접근:
- 1TB 데이터, 10 파티션
- 각 파티션 100GB

문제:
- 일부 태스크만 오래 실행 (Straggler)
- 메모리 부족 (OOM)

해결:
- 파티션당 128-256MB 권장
- spark.sql.shuffle.partitions=2000 (1TB)
- 또는 AQE로 자동 조정
```

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 구분 | MapReduce | Spark | 개선효과 |
|-----------|-----------|-------|---------|
| 처리 속도 | 1x | 10-100x | 최대 100배 |
| 코드 라인 | 100행 | 10행 | 90% 감소 |
| ML 학습 시간 | 10시간 | 30분 | 95% 감소 |
| 실시간 처리 | 불가능 | 가능 | 스트리밍 통합 |

### 미래 전망 및 진화 방향

1. **Photon**: C++ 기반 고속 엔진
2. **Spark Connect**: 원격 클라이언트
3. **AI/LLM 통합**: Spark + Deep Learning

### 참고 표준/가이드
- **Apache Spark**: spark.apache.org
- **Delta Lake**: delta.io
- **Spark Tuning**: spark.apache.org/docs/latest/tuning.html

---

## 관련 개념 맵 (Knowledge Graph)

1. [하둡 에코시스템 (Hadoop Ecosystem)](./hadoop_ecosystem.md)
   - 관계: MapReduce를 대체하는 차세대 엔진

2. [데이터 레이크하우스 (Data Lakehouse)](./data_lakehouse.md)
   - 관계: Delta Lake와 결합한 통합 분석

3. [카프카 (Apache Kafka)](./kafka.md)
   - 관계: Structured Streaming 소스

4. [쿠버네티스 (Kubernetes)](./kubernetes.md)
   - 관계: K8s에서 Spark 실행

5. [MLlib (머신러닝)](./mllib.md)
   - 관계: Spark 내장 ML 라이브러리

6. [옵저버빌리티 (Observability)](./observability.md)
   - 관계: Spark UI, 메트릭 수집

---

## 어린이를 위한 3줄 비유 설명

**비유: 초고속 분산 주방**

스파크는 엄청나게 큰 주방 같아요. 요리사들이(Executor) 각자 조리대(메모리)에서 요리해요. 재료를 창고(디스크)에서 매번 꺼내는 대신 조리대 위에 올려두고 여러 요리를 연달아 만들죠.

**원리:**
주문이 들어오면(DAG) 총괄 셰프(Driver)가 요리 순서를 정해요. 요리사들이 병렬로 작업하고, 한 명이 아파도 다른 요리사가 대신해요. 재료 부족하면 냉장고(디스크)를 쓰지만, 대부분 조리대에서 바로 요리해요.

**효과:**
이렇게 하면 엄청나게 많은 요리를 빨리 만들 수 있어요. 창고를 왔다 갔다 하는 시간이 없으니까요! 100명분 요리를 1명이 만드는 시간에 100명이 같이 만드는 거예요!
