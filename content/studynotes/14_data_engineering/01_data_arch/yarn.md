+++
title = "YARN (Yet Another Resource Negotiator)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# YARN (Yet Another Resource Negotiator)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: YARN은 하둡 2.0의 클러스터 리소스 관리자로, CPU와 메모리를 효율적으로 스케줄링하여 여러 데이터 처리 엔진(Spark, MapReduce, Flink)이 공존할 수 있게 합니다.
> 2. **가치**: 리소스 격리와 멀티테넌시를 제공하여, 단일 클러스터에서 다양한 워크로드를 효율적으로 실행합니다.
> 3. **융합**: 현재는 Kubernetes로 대체되는 추세지만, 기존 하둡 클러스터에서 여전히 널리 사용됩니다.

---

### Ⅰ. 개요

#### 1. 핵심 구성요소
- **ResourceManager**: 마스터, 전체 리소스 관리
- **NodeManager**: 슬레이브, 노드 리소스 관리
- **ApplicationMaster**: 애플리케이션별 리소스 요청
- **Container**: 리소스 할당 단위

---

### Ⅱ. 아키텍처

```text
+------------------+
| ResourceManager  |  (Master)
| - Scheduler      |
| - AppManager     |
+--------+---------+
         |
    +----+----+----+
    |    |    |    |
    v    v    v    v
+-------+ +-------+ +-------+
| NM 1  | | NM 2  | | NM 3  |
| +---+ | | +---+ | | +---+ |
| |AM | | | |   | | | |   | |
| |C1 | | | |C2 | | | |C3 | |
| +---+ | | +---+ | | +---+ |
+-------+ +-------+ +-------+
```

---

### Ⅲ. 스케줄러

- **FIFO**: 선입선출
- **Capacity**: 큐별 용량 할당
- **Fair**: 공정한 리소스 분배

---

### Ⅳ. 결론

YARN은 하둡 생태계의 리소스 관리 표준이나, 현재는 Kubernetes로 전환 중입니다.

---

### 관련 개념 맵
- **[Apache Hadoop](@/studynotes/14_data_engineering/01_data_arch/apache_hadoop.md)**
- **[HDFS](@/studynotes/14_data_engineering/01_data_arch/hdfs.md)**

---

### 어린이를 위한 3줄 비유
1. **학교 선생님**: 선생님이 교실과 교구를 배분해요.
2. **반마다 다른 수업**: 어떤 반은 미술, 어떤 반은 체육을 해요.
3. **공정하게 나눠요**: 누가 많이 쓰고 적이 쓰는지 봐서 공정하게 나눠요!
