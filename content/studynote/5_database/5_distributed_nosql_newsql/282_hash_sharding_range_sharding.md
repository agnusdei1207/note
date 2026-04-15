+++
title = "282. 해시 샤딩 (Hash Sharding) 및 레인지 샤딩 (Range Sharding) - 데이터 분산 전략의 두 축"
weight = 282
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 해시 샤딩은 키 값을 해시 함수에 통과시켜 데이터를 균등하게 분산하고, 레인지 샤딩은 키 값의 정렬된 범위에 따라 데이터를 배치하는 전략이다.
> 2. **트레이드오프**: 해시 샤딩은 부하 분산(Load Balancing)에 유리하나 범위 조회가 어렵고, 레인지 샤딩은 범위 조회(Range Query)에 최적화되어 있으나 핫스팟(Hotspot) 발생 위험이 크다.
> 3. **융합**: 현대 분산 DB는 두 방식의 장점을 결합한 하이브리드 방식이나 일관된 해싱(Consistent Hashing)을 통해 재배치 비용을 최소화하는 방향으로 발전하고 있다.

---

### Ⅰ. 개요 (Context & Background)
대규모 트래픽을 처리하는 분산 데이터베이스에서 데이터를 어떻게 나눌 것인가는 시스템 성능과 직결된다. **해시 샤딩(Hash Sharding)**은 알고리즘을 통해 데이터를 기계적으로 골고루 뿌려주는 방식인 반면, **레인지 샤딩(Range Sharding)**은 의미 있는 값의 범위에 따라 데이터를 모아두는 방식이다. 전자는 NoSQL(Cassandra, Redis Cluster 등)에서 수평적 확장을 위해 주로 사용되며, 후자는 RDBMS의 파티셔닝이나 HBase와 같은 대용량 분석용 DB에서 순차적 데이터 접근을 위해 선호된다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 해시 샤딩 vs 레인지 샤딩 비교 아키텍처
```text
[Hash Sharding]                         [Range Sharding]
Key -> Hash(Key) % N -> Node ID         Key Value -> Range Mapping -> Node ID

      Hash Function                           Value Range
    ┌───────────────┐                       ┌───────────────┐
    │   f(id)=id%3  │                       │ 1~100, 101~200│
    └───────┬───────┘                       └───────┬───────┘
            │                                       │
    ┌───────┼───────┐                       ┌───────┴───────┐
    ▼       ▼       ▼                       ▼               ▼
 [Node 0] [Node 1] [Node 2]              [Node A]        [Node B]
 (1, 4, 7) (2, 5, 8) (3, 6, 9)           (1 ~ 100)      (101 ~ 200)

[Bilingual Description]
- Deterministic Mapping: Predefined rules for placement. (결정론적 데이터 배치)
- Range Scan: Scanning continuous data. (연속된 데이터 스캔)
- Load Balancing: Equal distribution of traffic. (부하의 균등한 분산)
```

#### 2. 핵심 메커니즘 상세
- **해시 샤딩(Hash Sharding)**:
  - **알고리즘**: `Shard = Hash(Key) % Number_of_Shards`
  - **특징**: 키의 분포와 상관없이 샤드 수만큼 데이터가 고르게 분산됨.
  - **문제**: 샤드 추가/삭제 시 대규모 데이터 재배치(Rebalancing) 발생. 이를 해결하기 위해 Consistent Hashing 사용.
- **레인지 샤딩(Range Sharding)**:
  - **알고리즘**: `Shard = Find_Shard_By_Range(Key)`
  - **특징**: 유사한 키 값들이 물리적으로 인접한 위치에 저장되어 `BETWEEN`, `ORDER BY` 쿼리에 매우 빠름.
  - **문제**: 특정 날짜나 최신 ID에 트래픽이 몰리면 해당 샤드만 과부하(Hotspotting) 발생.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 데이터 분산 전략 상세 비교
| 비교 항목 | 해시 샤딩 (Hash Sharding) | 레인지 샤딩 (Range Sharding) |
| :--- | :--- | :--- |
| **분산 균등도** | 매우 높음 (Uniform) | 낮음 (Data Skew 가능성) |
| **범위 쿼리 성능** | 낮음 (Scatter-Gather 필요) | 매우 높음 (Locality 활용) |
| **확장 용이성** | 복잡함 (전체 재배치 필요성) | 쉬움 (범위 분할만 수행) |
| **데이터 지역성** | 없음 | 높음 |
| **적합한 키** | 고유 ID, 랜덤 문자열 | 날짜, 일련번호, 사전순 이름 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
**[기술사적 판단]**
시스템 설계자는 애플리케이션의 **Read/Write 패턴**을 먼저 분석해야 한다.
1. **쓰기 위주 시스템(Write-heavy)**: 데이터 분산이 최우선이므로 해시 샤딩을 선택한다. 특히 단조 증가하는 PK를 가진 경우 해시 샤딩은 필수적이다.
2. **조회 위주 시스템(Read-heavy)**: 특정 범위의 데이터를 묶어서 가져오는 요건이 많다면 레인지 샤딩을 선택하되, 핫스팟 방지를 위해 키 설계 시 'Salting' 기법이나 'Shard Split' 기능을 지원하는 DB를 선정해야 한다.
3. **하이브리드 전략**: 카산드라(Cassandra)처럼 파티션 키는 해시로 분산하고, 클러스터링 키는 레인지로 정렬하는 복합 구조를 활용하여 두 방식의 장점을 모두 취할 수 있다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
클라우드 DB 환경이 고도화되면서 사용자가 샤딩 방식을 직접 고민하지 않아도 되는 **Auto-sharding** 기술이 보편화되고 있다. 하지만 데이터의 물리적 배치 원리를 이해하지 못한 설계는 결국 성능 병목을 야기한다. 미래의 데이터베이스는 워크로드를 실시간으로 감지하여 해시와 레인지 방식을 동적으로 전환하거나, 머신러닝을 통해 최적의 경계 지점을 찾는 지능형 샤딩으로 진화할 것으로 전망된다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: Sharding, Partitioning
- **핵심 기술**: Consistent Hashing, Virtual Nodes, Shard Splitting
- **연관 개념**: Hotspot, Scatter-Gather, Data Locality, Rebalancing

---

### 👶 어린이를 위한 3줄 비유 설명
> 1. **해시 샤딩**은 사탕을 친구들에게 줄 때 "가위바위보" 순서대로 무작위로 나눠주는 것과 같아요. 사탕이 골고루 나눠지죠.
> 2. **레인지 샤딩**은 사탕을 "딸기맛", "포도맛"처럼 맛별로 모아서 상자에 넣는 것과 같아요. 같은 맛을 찾기는 쉽지만 한 가지 맛만 인기가 많으면 그 상자만 금방 비어버려요.
> 3. 상황에 따라 사탕을 골고루 나눌지, 종류별로 모을지 결정하는 것이 샤딩 전략이랍니다!
