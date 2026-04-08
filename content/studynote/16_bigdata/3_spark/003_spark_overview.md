+++
weight = 15003
title = "3. 7V — 5V + Visualization(시각화) + Variability(가변성)"
date = "2026-03-26"
[extra]
categories = "studynote-bigdata"
+++

> **핵심 인사이트**
> 1. **본질**: Apache Spark는 하둡 MapReduce의 디스크 기반 연산을 인메모리 RDD (Resilient Distributed Dataset)로 대체하여, 반복적 기계학습 알고리즘과 대화형 분석에서 10~100배高速化した 분산 컴퓨팅 엔진이다.
> 2. **가치**: 배치 처리뿐 아니라 SQL 질의, 스트리밍, 머신러닝, 그래프 분석을单一 엔진으로 통합하여, 별도의 시스템을 운영해야 하는 복잡성을 크게 줄였다.
> 3. **융합**: Scala (JVM 기반)로 작성되어 하둡 YARN, Mesos, Kubernetes 등 다양한 클러스터 매니저 위에서 동작하며, Python, R, Java 등 다중 언어를 지원하여 대중성을 확보했다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### MapReduce의 한계와 Spark의 탄생

하둡 MapReduce는 대용량 데이터 처리를 위한 혁신적 패러다임을 제시했지만, 몇 가지 근본적 한계를 내포하고 있었다. 가장 큰 문제는 반복적 연산의 비효율성이다. PageRank, k-Means, 로지스틱 회귀와 같은 기계학습 알고리즘은 동일한 데이터셋을何度も繰り返し 처리해야 하는데, MapReduce는 각 iteration마다 디스크에 데이터를 읽고 써야 했다. 수십 번의 iteration을 거치는 알고리즘에서는, 실제 연산 시간보다 디스크 I/O에 소비되는 시간이 지배적이었다.

2009년, UC Berkeley AMPLab의 마테이 자하리아 (Matei Zaharia)가 이 문제를 해결하기 위해 Spark를 개발했다. 핵심 발상은 "중간 결과물을 디스크가 아닌 메모리에 유지하면 어떨까"였다.當時主流 16GB~64GB RAM 서버에서 동작하는 Spark는, 디스크 기반 MapReduce 대비 수십 배에서 수백 배高速の性能向上を達成した。2010년 Apache 오픈소스 프로젝트로 공개되었으며, 2014년 Apache Top-Level Project로 승격되어 현재까지 가장 활발히 사용되는 빅데이터 처리 엔진 중 하나다.

### Spark의 5가지 핵심 장점

Spark가 MapReduce를 압도하고 주류로 자리 잡은 이유는 다섯 가지로 집약된다.

첫째, 속도 (Speed)다. 인메모리 연산은 디스크 I/O의 bottleneck을 제거하며, 특히 반복적 workload에서威力が 발휘된다. 둘째, 단순성 (Simplicity)이다. MapReduce는 수십 줄의 Boilerplate 코드가 필요한 반면, Spark는 몇 줄의 코드로 동일 연산을 표현할 수 있다. 셋째, 통합성 (Unification)이다. Batch Processing (Spark Core), SQL (Spark SQL), Streaming (Spark Structured Streaming), Machine Learning (MLlib), Graph Analysis (GraphX)를单一 엔진으로 제공한다. 넷째, 유연성 (Flexibility)이다. Hadoop YARN, Mesos, Kubernetes, Standalone 등 다양한 클러스터 매니저 위에서 동작한다. 다섯째, 생태계 (Ecosystem)다. Delta Lake, Apache Iceberg, Spark Connector 등을 통해 데이터 레이크 하부구조와 긴밀히 연동된다.

```text
┌─────────────────────────────────────────────────────────────────┐
│           Spark vs MapReduce: 반복적 기계학습 워크로드 비교         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [MapReduce 방식: 매 Iteration마다 디스크 읽기/쓰기]               │
│                                                                 │
│  Iteration 1:  [Disk Read] → Map → [Disk Write] → Shuffle → [Disk Read] → Reduce → [Disk Write] │
│  Iteration 2:  [Disk Read] → Map → [Disk Write] → Shuffle → [Disk Read] → Reduce → [Disk Write] │
│  Iteration 3:  [Disk Read] → Map → [Disk Write] → Shuffle → [Disk Read] → Reduce → [Disk Write] │
│  ...                                                            │
│  Iteration N:  [Disk Read] → Map → [Disk Write] → Shuffle → [Disk Read] → Reduce → [Disk Write] │
│                                                                 │
│  총 소요 시간: (디스크 I/O 시간 × N) + (연산 시간 × N)              │
│  문제: N이 클수록 I/O 시간이 지배적                                │
│                                                                 │
│  ────────────────────────────────────────────────────────────── │
│                                                                 │
│  [Spark 방식: 메모리에 데이터 적재 후 반복 연산]                     │
│                                                                 │
│  Initial Load:  [Disk Read] → 메모리 (RDD Cache)                 │
│  Iteration 1:    메모리 → 연산 1 → 결과                            │
│  Iteration 2:    메모리 → 연산 2 → 결과                            │
│  Iteration 3:    메모리 → 연산 3 → 결과                            │
│  ...                                                            │
│  Iteration N:    메모리 → 연산 N → 결과                            │
│                                                                 │
│  총 소요 시간: (초기 디스크 Read 1회) + (연산 시간 × N)             │
│  효과: 디스크 I/O 시간 N분의 1로 감소                              │
│                                                                 │
│  벤치마크 예시: 100GB 데이터, 10 Iteration K-Means                  │
│  - MapReduce: 2시간                                              │
│  - Spark (인메모리): 20분 (6배高速)                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 비교는 Spark 인메모리 연산의威力을 명확히 보여준다. MapReduce에서 각 iteration은 독립적인 Job으로 취급되어, 이전 iteration의 결과는 HDFS에 저장되고 다음 iteration에서 다시 읽어야 한다. 이 과정에서 디스크 Seek 시간, 읽기/쓰기 throughput, 네트워크 복제 시간이 반복적으로 발생한다. 반면 Spark는 데이터를 RDD로 메모리에 적재한 뒤에는 메모리 버스 내에서 연산이 이루어진다. 현재主流 서버의 메모리 대역폭은 수십 GB/s로, SATA SSD의 수백 MB/s보다 수십 배 빠르다. 따라서 10 iteration 머신러닝 알고리즘에서는 실제 연산 시간보다 디스크 I/O가 bottleneck이 되어, Spark의高速화가 극적으로 나타난다. 다만 Spark도全ノード故障시 자동으로 디스크에서 RDD를 재구성하는 lineage 복구 기능을 갖추고 있어, 메모리 장애에 대한 내성 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### RDD 아키텍처와 Lazy Evaluation

RDD (Resilient Distributed Dataset)는 Spark의 핵심 데이터 추상화 구조다. 변경 불가능한 (Immutable) 분산 객체 컬렉션으로, RDD를 transformations (맵, 필터, 조인 등)를 통해 다른 RDD로 변환할 수 있다. RDD는 데이터를パーティション별로 분할하여 클러스터 노드에 저장하며, 각 파티션에 대해 병렬 연산이 가능하다.

RDD의 가장 중요한 설계 특성은 Lazy Evaluation (지연 평가)이다. RDD transformation (예: map, filter)을 호출해도 즉시 실행되지 않고, transformation을 기록한 lineage (계보) 그래프만 구축된다. 실제 연산은 action (예: count, collect, save)을 호출하는 시점에 실행된다. 이 설계의 장점은 두 가지다. 첫째, 불필요한 intermediate 결과를 만들지 않아 메모리使用량을 줄일 수 있다. 둘째, 전체 lineage 그래프를 파악한 뒤 최적의 실행 계획을 세울 수 있다 (DAG 스케줄링).

```text
┌─────────────────────────────────────────────────────────────────┐
│                    RDD Lazy Evaluation 동작                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Transformation 호출 시: 실제 연산 없음, Lineage만 기록]           │
│                                                                 │
│  val lines = sc.textFile("hdfs://data/logs/*.txt")  // 새 RDD   │
│       │                                                         │
│       ▼                                                         │
│  val errors = lines.filter(_.contains("ERROR"))  // 새 RDD,     │
│       │                        // 하지만 실행되지 않음          │
│       ▼                                                         │
│  val count = errors.count()  // Action 호출 → 실행 시작!       │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  DAG 실행 계획 (최적화됨)                   │   │
│  │                                                         │   │
│  │  textFile → filter → count                             │   │
│  │  (실행 시 하나의 Task로 통합되어 불필요한 임시 RDD 생성 방지) │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [Lineage (계보) 그래프 예시]                                    │
│                                                                 │
│  HadoopRDD (textFile)                                           │
│       │                                                         │
│  MapPartitionsRDD (filter)                                      │
│       │                                                         │
│  ShuffledRDD (groupBy)                                          │
│       │                                                         │
│  MapPartitionsRDD (map)                                         │
│       │                                                         │
│  result: collect()                                               │
│                                                                 │
│  장애 복구: 특정 파티션 유실 시 → Lineage 역추적 → 해당 단계부터   │
│  재연산 (Disk에 checkpoint가 있다면 그 지점부터 재연산)            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Lazy Evaluation의 실용적 가치는다. 개발자가 transformations을 chained로 연결하면, Spark는 전체 파이프라인을 하나의 stage로 통합 최적화한다. 예를 들어, `rdd.filter().map().filter().collect()`에서 불필요한 `map()` 결과를 메모리에 저장하지 않고, 첫 번째 `filter()` 결과를 두 번째 `filter()`로 직접 전달하여 메모리 사용량을 줄인다. 또한 lineage 기반 장애 복구는 checkpoint와 결합하여 全ノード故障 시에도 효율적으로 RDD를 재구성할 수 있게 한다. Spark의 `cache()` vs `persist()` 선택도 중요한 설계 결정이며, `cache()`는 메모드만 사용하는 반면 `persist(StorageLevel.DISK_AND_MEMORY)`는 메모리 부족 시 디스크까지 활용한다.

### Spark 클러스터 아키텍처

Spark 애플리케이션은 Driver, Cluster Manager, Worker Node의 세 축으로 구성된다. Driver는 사용자의 Spark 코드를 실행하며 SparkContext를 통해 클러스터와 통신한다. Cluster Manager (YARN, Mesos, Kubernetes, Standalone)는 클러스터 자원을 할당하고 스케줄링한다. Worker Node는 실제 연산이 실행되는 노드로, Executor 프로세스가 동작하며 Task를 실행한다.

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Spark 클러스터 아키텍처                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Spark Application 코드]                                       │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Driver Process                        │   │
│  │                                                         │   │
│  │  SparkContext ──── 클러스터와 통신하는 진입점             │   │
│  │       │                                                 │   │
│  │  DAGScheduler ─── RDD 그래프 → Stage로 분할              │   │
│  │       │                                                 │   │
│  │  TaskScheduler ─── Stage 내 Task을 클러스터에 제출        │   │
│  │       │                                                 │   │
│  │  SchedulerBackend ── Executor과 직접 통신하여 Task 할당  │   │
│  └──────────────┬──────────────────────────────────────────┘   │
│                 │                                                 │
│                 ▼                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Cluster Manager (YARN / Mesos / K8s)         │   │
│  │                                                         │   │
│  │    ResourceManager / Master                             │   │
│  │         │                                                │   │
│  │    ┌────┴────┐                                         │   │
│  │    ▼         ▼                                          │   │
│  │ Container  Container  Container                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                 │                                                │
│     ┌───────────┼───────────┐                                   │
│     ▼           ▼           ▼                                    │
│  ┌────────┐ ┌────────┐ ┌────────┐                              │
│  │Worker 1│ │Worker 2│ │Worker 3│                              │
│  │ ┌────┐ │ │ ┌────┐ │ │ ┌────┐ │                              │
│  │ │Exec │ │ │ │Exec │ │ │ │Exec │ │                              │
│  │ │Task │ │ │ │Task │ │ │ │Task │ │                              │
│  │ │Task │ │ │ │Task │ │ │ │Task │ │                              │
│  │ └────┘ │ │ └────┘ │ │ └────┘ │                              │
│  │ Cache  │ │ Cache  │ │ Cache  │                              │
│  └────────┘ └────────┘ └────────┘                              │
│                                                                 │
│  핵심 동작 흐름:                                                 │
│  1. Driver가 코드를 받고 DAG를 구성한다                          │
│  2. DAGScheduler가 Stage를 나누고, TaskScheduler에 넘긴다      │
│  3. TaskScheduler가 ClusterManager에 Container를 요청한다       │
│  4. Worker의 Executor가 Task를 실행하고 결과를 Driver에 반환한다 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Spark의 클러스터 내 통신 구조에서 핵심은 Driver-Executor 모델이다. Driver가 전체 연산의的大脑 역할을 하며, 실제 데이터는 Worker 노드의 Executor 메모리에分布式으로 저장된다. Task는 데이터가 있는 Worker 노드로 스케줄링되어 (데이터 지역성) 네트워크 전송을 최소화한다. Executor는 하나의 JVM 프로세스로, 여러 Task를 병렬로 실행하며, GC 관리와 메모리 관리를 Executor 레벨에서 수행한다. Cluster Manager는 Spark 전용이 아니라,YARN이나 쿠버네티스처럼 Spark뿐 아니라 다른 애플리케이션도 동시에 실행할 수 있는 범용 리소스 매니저다. 실무에서는 Executor 메모리 크기, Executor 당 코어 수, Executor 수를 Spark job 특성에 맞게 튜닝하는 것이 성능 최적화의 핵심이다.

### DataFrame, Dataset, SQL의 통합

Spark 2.0부터 DataFrame과 Dataset API가 통합되어, 구조화 데이터를 처리하는 unified된 API가 제공된다. DataFrame은 행 기반의 tabular 데이터 구조로, 이름이 있는 컬럼으로 구성되며, Dataset은 타입이 있는 DataFrame이다. SQL도 동일한 Catalyst Optimizer를 통해 최적화되어, DataFrame operations과 SQL 쿼리가 동일한 성능으로 실행된다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### Spark vs Hadoop MapReduce vs Flink 비교

| 비교 항목 | Hadoop MapReduce | Apache Spark | Apache Flink |
|:---|:---|:---|:---|
| **데이터 처리 위치** | 디스크 (반복 시 매번 재读写) | 인메모리 (RDD 캐싱) | 네이티브 스트리밍 |
| **처리 모델** | 배치 전용 | 배치 + 마이크로배치 | 배치 + 네이티브 스트리밍 |
| **레이턴시** | 수십 초~수 분 | 수 초~수십 초 | 밀리초~수 초 |
| **반복 연산** | 비효율적 (매번 디스크) | 효율적 (인메모리) | 매우 효율적 |
| **실시간 처리** | 불가 | Spark Structured Streaming | 완전 지원 |
| **내결함성** | Task 실패 시 자체 재실행 | RDD Lineage + Checkpoint | Checkpoint 기반 상태 복구 |
| **주 사용처** | 일회성 대량 배치 | ML 파이프라인, 대화형 분석 | 순수 실시간 분석 |

```text
┌─────────────────────────────────────────────────────────────────┐
│              처리 지연 vs 처리량: 각 엔진의 포지셔닝                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  처리량 (throughput) ↑                                          │
│       │                                                           │
│       │     ┌──────────────────┐                                 │
│       │     │  Hadoop MapReduce │                                 │
│       │     │  (고처리량 배치)   │                                 │
│       │     └──────────────────┘                                 │
│       │                ┌──────────────────┐                      │
│       │                │     Apache Spark  │                      │
│       │                │ (균형점, 범용)    │                      │
│       │                └──────────────────┘                      │
│       │                         ┌──────────────────┐             │
│       │                         │    Apache Flink   │            │
│       │                         │  (저지연 스트리밍) │            │
│       │                         └──────────────────┘             │
│       └──────────────────────────────────────────────▶           │
│                                       처리 지연 (latency) ↓        │
│                                                                 │
│       초(1)    초(10)   초(30)   분(1)    분(10)   시간(1)       │
│  ─────────────────────────────────────────────────────────────── │
│                     목표 SLA 구간 (실시간~准实时)                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 매트릭스에서 확인할 수 있듯이, 세 엔진은 서로 다른 최적화 목표를 가지고 있다. MapReduce는 초대용량 배치 처리의处理量을 극대화하지만 지연이 크다. Spark는内存 비용과 처리량 사이의 균형점을 찾은 설계며, 대부분의 기업用 배치 및 대화형 분석에 적합하다. Flink는 지연 시간을 극적으로 줄이지만, 단일 잡의 최대处理량에서는 MapReduce에 비해劣势가 있다. 따라서 동일한 클러스터에서 YARN을 사용하여 Spark job과 Flink job을 동시에 운영하는 것도 일반적이다.

### Spark와 Python, R의 통합

Spark는 Scala/JVM 기반이지만, Python (PySpark)과 R (SparkR)을 위한 Language Binding을 제공한다. PySpark는 Python 표준인 pandas와 호환되는 DataFrame API를 제공하여, Python 데이터 분석가들이 기존 스킬을 활용한 채 대규모 분산 데이터를 처리할 수 있게 한다. SparkR은 R 사용자에게 distributed dataset 연산을 가능하게 한다.

Python과 Scala의 성능 차이는 JVM 기반 코덱의 차이에서 비롯된다. Python UDF (User Defined Function)는 JVM 데이터 타입과 Python 데이터 타입 간의 직렬화/역직렬화 오버헤드가 발생하므로, 성능이 중요한 경로에서는 Scala 구현이 권장된다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오

**시나리오 1: 수백 GB 로그 데이터의 일별 집계 파이프라인**

웹 서비스의 일별 접근 로그 (수백 GB)를 분석하여 방문자 수, 페이지 뷰, 주요 에러 빈도 등을 집계하는 파이프라인을 Spark로 구현해야 한다. 핵심 설계 결정 사항은 다음과 같다.

데이터 읽기 형식 선택이 중요하다. 텍스트 파일 대신 Parquet (컬럼형 압축 포맷)를 사용하면, 분석에 필요한 컬럼만 읽어 들여 I/O 비용을 크게 줄일 수 있다. Parquet는 컬럼 기반 압축으로 일반 텍스트 대비 2~10배 스토리지 절약과 동시에 쿼리 성능을 향상시킨다.

셔플(shuffle) 최적화가 핵심이다. groupBy, join, reduceByKey 등의 셔플이 발생하는 operation에서는 네트워크를 통한 데이터 재분배가 이루어지므로, 파티션 수를 적절히 설정하는 것이 중요하다. 일반적으로 파티션당 100MB~200MB가 적정하며, 너무 적은 파티션은 병렬성을活用 못하고 너무 많은 파티션은 태스크 스케줄링 오버헤드를 증가시킨다.

**시나리오 2: ML 파이프라인의的特征工程과 모델 학습**

고객 이탈 예측 모델을 위한 ML 파이프라인을 Spark MLlib로 구축해야 한다. Spark MLlib는 분산 머신러닝을 위한 라이브러리로, ALS (Alternating Least Squares), Logistic Regression, Decision Tree, Random Forest 등을 제공한다.

특징 추출 (Feature Engineering)이 모델 성능을 결정한다. one-hot encoding, 정규화 (Normalization), 문자열 인덱싱 (String Indexing) 등의 전처리가 Spark DataFrame API로 구현되며, Pipeline API를 통해 일관된 워크플로우로 구성된다. Spark MLlib의 Logistic Regression은 L-BFGS optimizer를 사용하며, 수렴 반복 횟수와 regularization 파라미터가 학습 결과에 큰 영향을 미친다.

```text
┌─────────────────────────────────────────────────────────────────┐
│           Spark ML 파이프라인: 특징 工程からモデル 평가까지            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [데이터 소스: HDFS Parquet]                                     │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Pipeline Stage 구성                          │   │
│  │                                                         │   │
│  │  Stage 1: StringIndexer (범주형 → 숫자)                  │   │
│  │       │                                                 │   │
│  │  Stage 2: OneHotEncoder (숫자 → 이진 벡터)                │   │
│  │       │                                                 │   │
│  │  Stage 3: VectorAssembler (여러 컬럼 → 특징 벡터)         │   │
│  │       │                                                 │   │
│  │  Stage 4: StandardScaler (정규화)                        │   │
│  │       │                                                 │   │
│  │  Stage 5: LogisticRegression (모델 학습)                  │   │
│  │       │                                                 │   │
│  │  Stage 6: BinaryClassificationEvaluator (AUC 평가)        │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  [모델 저장: HDFS / Model Registry]                              │
│                                                                 │
│  튜닝 포인트:                                                    │
│  - maxIter: 클수록 정확하지만 학습 시간 증가                      │
│  - regParam: 클수록 과적합 감소 but 언더피팅 위험                  │
│  - elasticNetParam: L1/L2 혼합 비율                              │
│                                                                 │
│  병렬 학습: LogisticRegression는 단일 모델이지만, 데이터 파티션별   │
│  미니배치 SGD로 분산 병렬 학습됨                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Spark ML Pipeline의 핵심 가치는 전처리와 모델 학습이 единый 워크플로우로 통합된다는 점이다.传统的에는 Python (scikit-learn)으로 전처리를 하고, 학습된 모델을 다시 Spark로 배포하는 번거로움이 있었다. Pipeline API를 사용하면 하나의 코드베이스로 ETL에서 모델 서빙까지 관리할 수 있다. VectorAssembler는 여러 컬럼을 단일 특징 벡터로 통합하는 stage로, MLlib의 모든 알고리즘이 이 벡터 형태를 입력으로 받는다. 실무에서는 데이터 skew (편향)이 심한 categorical 변수의 인코딩 전략이 모델 성능에 큰 영향을 미치므로, 인코딩 방식 선택이 중요한 설계 결정이 된다.

### 도입 체크리스트

Spark 도입 전 검토해야 할 기술적 항목은 다음과 같다.

클러스터 규모 산정에서 가장 중요한 것은 데이터 크기와 사용 패턴이다.Executor 수 × Executor 메모리가 클러스터 총 캐싱 용량을 결정하며, 반복적 ML workload에서는 데이터셋 크기의 2~3배 여유 메모리가 권장된다. 네트워크 대역폭도 중요한 요소로, 셔플 볼륨이 크면 10Gbps 이상의 네트워크 인프라가 필요하다.

데이터 포맷 선택도 핵심이다. Parquet 또는 ORC (Optimized Row Columnar) 사용을 권장하며, 텍스트 파일 대비 I/O 비용을 크게 줄일 수 있다. 파티션 컬럼 (날짜, 카테고리 등)을 활용하면 쿼리 시 스캔 범위를 줄일 수 있다.

### 안티패턴

**셔플 데이터 과적재 (Shuffle Hash Join 오남용)** 는 큰 테이블끼리의 조인에서 셔플되는 데이터양이 클러스터 전체 네트워크를 포화시킬 수 있다. Broadcast Join (작은 테이블을全ノード에 브로드캐스트)을 우선 시도하고, 큰 테이블끼리 조인 시에는 Sort-Merge Join을 사용해야 한다.

**collect() 남용** 도 심각한 문제다. `collect()`는全파티션의 데이터를 Driver JVM 메모리로 모으므로, 수십 GB 데이터를 Driver로 모으면 곧바로 OOM (Out Of Memory) 에러가 발생한다. `take()`, `sample()`, `toPandas()` 등 샘플링 operation을 우선 사용해야 한다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적 효과

| 구분 | MapReduce 대비 | Spark 효과 |
|:---|:---|:---|
| **반복 ML 작업** | 2시간 | 20분 (**6배高速**) |
| **대화형 SQL 쿼리** | 수십 초 | 수 초 |
| **배치 처리** | 동일 (데이터 크기에 좌우) | 코드량 80% 절감 |
| **개발 생산성** | Boilerplate 코드 다수 | 함수형 API, 80% 코드 감소 |

### 미래 전망

Spark의 미래는 네 가지 방향으로 진화하고 있다.

첫째, LLVM 기반의 벡터화된 쿼리 실행 엔진 (Spark 3.x의 Adaptive Query Execution)이 더 강력해지고 있다. 바이트코드 수준 최적화와 SIMD (Single Instruction Multiple Data) 활용으로, 기존 Volcano 모델 기반 실행보다 훨씬 빠른 쿼리 성능을 달성한다.

둘째, Kubernetes-native 통합이加速되고 있다. Spark 3.0부터 Kubernetes가 공식 Cluster Manager로 지원되며, 컨테이너화된 Spark 애플리케이션의 실행과 관리가 더 간편해졌다. 이는 serverless Spark (Databricks, Amazon EMR on EKS 등)로의 전환을 촉진한다.

셋째, 구조화된 스트리밍 (Structured Streaming)의 강화다. Trigger Interval, Watermark, state store 등 advanced 기능이 보강되어, 순수 스트리밍 워크로드에서 Flink와 기능적으로 사실상 동등해졌다.

넷째, Delta Lake와 Apache Iceberg 같은湖house 포맷과의 통합深化이다. ACID 트랜잭션, 스키마 evolution, time travel 기능을 Spark DataFrame과 원활하게 연동하여, 데이터 레이크의 신뢰성이 크게 향상되었다.

### 참고 표준

- Apache Spark Official Documentation: 사실상 API 표준
- Spark SQL, DataFrames, Datasets Guide: 구조화 데이터 처리 표준
- Delta Lake Protocol: 데이터 레이크ouses ACID 트랜잭션 표준

---

## 📌 관련 개념 맵 (Knowledge Graph)

- `[RDD (Resilient Distributed Dataset)]`: Spark의核心 추상화로, 변경 불가능한 분산 컬렉션과 lineage 기반 장애 복구 기능
- `[DAG (Directed Acyclic Graph)]`: RDD transformation들로 구성된 연산 그래프로, stage 분할 및 최적화의 기반
- `[Lazy Evaluation]`: transformation 호출 시 실제 실행 없이 lineage만 기록, action 호출 시 한꺼번에 실행
- `[DataFrame]`: 이름이 있는 컬럼으로 구성된 tabular 데이터 구조로, Catalyst Optimizer가 쿼리를 최적화
- `[シャフル (Shuffle)]`: 파티션 간 데이터를 재분배하는 과정으로, 네트워크 I/O의主要 원인

---

## 👶 어린이를 위한 3줄 비유 설명

1. Spark는 **맛집中央주방** 같아요. 수백 가지 레시피 (데이터 처리)를 한 주방 (클러스터)에서 모두 만들 수 있어요. MapReduce는 냉장고 (디스크)를 매번 열어서 재료 (데이터)를 꺼내는 반면, Spark는 재료를 한 번 꺼내서 냉장고 위의 작업대 (메모리)에 펼쳐두고 여러 번 요리할 수 있어요.

2. RDD는 **냉장고 속 보관함** 같아요. 작은 칸막이 (파티션)마다 다른 재료가 들어있고, 칸막이 전체가 고장 나면 보관함에 적힌 메모 (Lineage)를 보고 다시 채울 수 있어요. 재료를 꺼내서 새로운 요리로 만들 때 (Transformation)마다 메모가 추가되고, 최종 요리 (Action)를 만들기 전까지는 실제로 요리하지 않아요 (Lazy Evaluation).

3. Spark의 파이프라인은 **기차 노선도**와 같아요. 기차 (Task)가 여러 역 (Stage)을 지나가는데, 각 역에서 다른 기차회사와 협력 (Cluster Manager)하며 운행해요. 기차 운행 스케줄러 (DAGScheduler)가 가장 빠른 경로를 미리 계산해서 배차해 주니까, 승객 (개발자)은 경로를 몰라도目的地에 도착할 수 있어요!
