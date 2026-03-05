+++
title = "아파치 하둡 (Apache Hadoop)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 아파치 하둡 (Apache Hadoop)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 아파치 하둡(Apache Hadoop)은 대용량 데이터를 분산 저장하고 병렬 처리하기 위한 오픈소스 자바 프레임워크로, HDFS(분산 파일 시스템)와 MapReduce(분산 처리 엔진), YARN(리소스 관리자)을 핵심 구성요소로 합니다.
> 2. **가치**: 페타바이트 이상의 데이터를 저가형 범용 서버(Commodity Hardware) 클러스터에서 처리할 수 있게 하여, 빅데이터 시대를 열었던 획기적인 기술입니다.
> 3. **융합**: 구글 GFS와 MapReduce 논문을 기반으로 개발되었으며, 현재는 스파크가 MapReduce를 대체하고, 데이터 레이크하우스 아키텍처로 진화하고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**아파치 하둡(Apache Hadoop)**은 분산 컴퓨팅 환경에서 대용량 데이터를 저장하고 처리하기 위한 오픈소스 소프트웨어 프레임워크입니다. 2006년 더그 커팅(Doug Cutting)이 구글의 GFS(Google File System)와 MapReduce 논문을 참고하여 개발했습니다.

**하둡 핵심 구성요소 (Hadoop 2.x/3.x)**:
| 구성요소 | 역할 | 설명 |
|:---|:---|:---|
| **HDFS** | 분산 저장 | 데이터를 블록 단위로 분산 저장 |
| **YARN** | 리소스 관리 | CPU, 메모리 스케줄링 |
| **MapReduce** | 분산 처리 | 디스크 기반 병렬 연산 |
| **Hadoop Common** | 공통 유틸리티 | 다른 모듈 지원 라이브러리 |

#### 2. 등장 배경
1. **2003~2004**: 구글이 GFS와 MapReduce 논문 발표
2. **2006**: 더그 커팅이 하둡을 오픈소스로 공개 (야후 후원)
3. **2008**: 하둡이 아파치 최상위 프로젝트로 승격
4. **2010s**: 하둡 생태계(Hive, HBase, Spark) 확장

#### 3. 비유를 통한 이해
하둡을 **'분할 정복 청소팀'**에 비유할 수 있습니다.
- 큰 창고를 청소할 때, 혼자서 하면 며칠이 걸립니다.
- 하둡은 100명의 청소부에게 창고를 100구역으로 나누어 맡깁니다.
- 각 청소부는 자신의 구역만 청소하고, 결과를 합칩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. HDFS 아키텍처 다이어그램

```text
<<< HDFS (Hadoop Distributed File System) Architecture >>>

+--------------------------------------------------------------------------+
|                           HDFS Cluster                                    |
+--------------------------------------------------------------------------+

     +------------------+
     |   NameNode       |  (Master - 메타데이터 관리)
     |   - FsImage      |  - 파일 시스템 트리
     |   - EditLog      |  - 변경 이력
     |   - Block Map    |  - 블록 위치 정보
     +--------+---------+
              |
    +---------+---------+---------+---------+
    |         |         |         |         |
    v         v         v         v         v
+-------+ +-------+ +-------+ +-------+ +-------+
|DN 1   | |DN 2   | |DN 3   | |DN 4   | |DN 5   |
|Data   | |Data   | |Data   | |Data   | |Data   |
|Node   | |Node   | |Node   | |Node   | |Node   |
+-------+ +-------+ +-------+ +-------+ +-------+

[블록 저장 예시]
파일: bigdata.tar.gz (1GB)
- 블록 크기: 128MB
- 복제 계수: 3
- 총 블록 수: 8개
- 각 블록은 3개의 DataNode에 복제 저장

[복제 배치 (Rack Awareness)]
Block 1: DN1(Rack1), DN2(Rack1), DN4(Rack2)
Block 2: DN2(Rack1), DN3(Rack1), DN5(Rack2)
...
```

#### 2. MapReduce 처리 과정

```text
<<< MapReduce Word Count Example >>>

Input: "hello world hello hadoop hello spark"

[Map Phase]
Split 1: "hello world"    → Map → (hello,1), (world,1)
Split 2: "hello hadoop"   → Map → (hello,1), (hadoop,1)
Split 3: "hello spark"    → Map → (hello,1), (spark,1)

[Shuffle & Sort]
hello: [1, 1, 1]  ← 같은 키끼리 모음
world: [1]
hadoop: [1]
spark: [1]

[Reduce Phase]
hello:  1+1+1 = 3
world:  1
hadoop: 1
spark:  1

Output: (hello,3), (hadoop,1), (spark,1), (world,1)
```

#### 3. YARN 아키텍처

```text
<<< YARN (Yet Another Resource Negotiator) >>>

+--------------------------------------------------------------------------+
|                        YARN Architecture                                  |
+--------------------------------------------------------------------------+

+------------------+                      +------------------+
| ResourceManager  |  (Master)            |   Client         |
| - Scheduler      | ←---- 요청 ----      |   (App Submit)   |
| - AppManager     |                      +------------------+
+--------+---------+
         |
    +----+----+----+----+
    |    |    |    |    |
    v    v    v    v    v
+-------+ +-------+ +-------+
| NM 1  | | NM 2  | | NM 3  |
| Node  | | Node  | | Node  |
| Manager| | Manager| | Manager|
+---+---+ +---+---+ +---+---+
    |         |         |
+---+---+ +---+---+ +---+---+
|Contnr | |Contnr | |Contnr |
|App    | |App    | |App    |
|Master | |       | |       |
+-------+ +-------+ +-------+

[동작 원리]
1. Client가 App을 ResourceManager에 제출
2. ResourceManager가 NodeManager 중 하나에 AppMaster 실행
3. AppMaster가 필요한 Container 할당 요청
4. 각 Container에서 Map/Reduce Task 실행
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 1. Hadoop vs Spark 비교표

| 비교 항목 | Hadoop MapReduce | Apache Spark |
|:---|:---|:---|
| **처리 방식** | 디스크 기반 | 인메모리 기반 |
| **속도** | 느림 (디스크 I/O) | 빠름 (100배) |
| **반복 작업** | 비효율적 | 효율적 (RDD 캐싱) |
| **스트리밍** | 미지원 | Spark Streaming |
| **ML** | Mahout (제한적) | MLlib (강력) |
| **사용 언어** | Java 위주 | Scala, Python, Java |

---

### Ⅳ. 실무 적용 및 기술사적 판단

#### 1. 하둡 클러스터 설계

**권장 하드웨어 사양 (DataNode)**:
- CPU: 12~24 cores
- RAM: 64~128 GB
- Disk: 12~24 x 4TB HDD (JBOD)
- Network: 10 Gbps

**클러스터 규모 산정**:
```text
일일 데이터 생성량: 1TB
보관 기간: 3년
복제 계수: 3

총 저장 용량 = 1TB x 365일 x 3년 x 3복제 = 3,285 TB ≈ 3.3 PB
DataNode 수 (128TB/노드 가정) ≈ 26대 + 여유분 30대
```

#### 2. 현대적 대안

하둡 MapReduce는 느린 디스크 I/O로 인해 현재는 Apache Spark로 대체되는 추세입니다. 그러나 HDFS는 여전히 데이터 레이크 스토리지로 널리 사용됩니다.

---

### Ⅴ. 결론

아파치 하둡은 빅데이터 시대를 연 선구적 기술입니다. 현재는 Spark, Flink 등 더 빠른 처리 엔진이 등장했지만, HDFS와 YARN은 여전히 많은 기업의 데이터 인프라에서 활용되고 있습니다.

---

### 관련 개념 맵 (Knowledge Graph)
- **[HDFS](@/studynotes/14_data_engineering/01_data_arch/hdfs.md)**
- **[MapReduce](@/studynotes/14_data_engineering/01_data_arch/mapreduce.md)**
- **[Apache Spark](@/studynotes/14_data_engineering/01_data_arch/apache_spark.md)**
- **[YARN](@/studynotes/14_data_engineering/01_data_arch/yarn.md)**

---

### 어린이를 위한 3줄 비유 설명
1. **100명의 요리사**: 큰 잔치 음식을 혼자 하면 너무 오래 걸려요. 하둡은 100명의 요리사가 나눠서 요리해요.
2. **나눠서 저장**: 재료도 여러 냉장고에 나눠서 보관해요. 하나가 고장 나도 다른 냉장고가 있어요.
3. **합치면 완성**: 각자 만든 요리를 합치면 거대한 잔치 음식이 완성돼요!
