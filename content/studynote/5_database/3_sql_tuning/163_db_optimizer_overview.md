+++
weight = 163
title = "데이터베이스 옵티마이저 (Database Optimizer)"
date = "2024-03-21"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)
1. **최적의 실행 계획(Execution Plan) 생성**: 옵티마이저는 SQL 질의를 수행하기 위해 통계 정보나 규칙을 바탕으로 가장 효율적인 네비게이션 경로를 결정하는 DBMS의 두뇌이다.
2. **비용 기반(CBO) 및 규칙 기반(RBO) 진화**: 과거 수동적인 규칙 기반에서 현대에는 데이터 분포와 시스템 부하를 고려한 비용 기반 옵티마이저가 표준으로 자리 잡았다.
3. **쿼리 성능의 핵심 통제점**: 인덱스 스캔, 조인 방식(NL, Hash, Sort Merge) 선택 등 전체 시스템 처리량(Throughput)과 응답 시간(Response Time)을 결정하는 핵심 요소이다.

---

### Ⅰ. 개요 (Context & Background)
데이터베이스 옵티마이저(Database Optimizer)는 사용자가 작성한 SQL 문을 받아 실제 데이터를 추출하기 위한 최적의 실행 방법인 **실행 계획(Execution Plan)**을 생성하는 핵심 모듈이다. 비절차적 언어인 SQL의 특성상 "무엇(What)"을 요구하느냐에 따라 DBMS가 "어떻게(How)" 가져올지를 스스로 결정해야 하며, 이 과정에서 수많은 선택지(Access Path, Join Order, Join Method) 중 최적의 경로를 찾아내는 것이 옵티마이저의 숙명이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

옵티마이저의 처리 과정은 크게 **쿼리 변환(Query Transformer)**, **비용 산정(Estimator)**, **계획 생성(Plan Generator)**의 3단계로 구분된다.

```text
[ SQL Query ] --+--> ( Parser ) --> ( Query Transformer ) --+
                |      [Syntax]       [Rewrite SQL]         |
                |                                           v
                +-----------------------------------> ( Optimizer ) <---+
                                                            |           |
       +----------------------------------------------------+           |
       |                   [ Execution Plan Generation ]                |
       |  1. Access Path (Index vs Table Scan)                          |
       |  2. Join Order (Which table first?)      ( Data Dictionary )---+
       |  3. Join Method (NL, Hash, Sort Merge)   ( Statistics )
       v
[ Final Execution Plan ]
```

1. **Parser (파서)**: SQL 구문을 분석하여 Syntax와 Semantic 오류를 체크하고 파스 트리(Parse Tree)를 생성한다.
2. **Query Transformer (쿼리 변환기)**: 전달받은 SQL을 논리적으로 동일하지만 더 효율적인 구조로 변환한다(예: View Merging, Subquery Unnesting).
3. **Estimator (비용 산정기)**: 데이터 딕셔너리의 통계 정보를 바탕으로 각 실행 계획의 비용(CPU, I/O, Memory)을 계산한다.
4. **Plan Generator (계획 생성기)**: 후보 계획들 중 가장 낮은 비용의 계획을 최종 선택한다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 규칙 기반 옵티마이저 (RBO) | 비용 기반 옵티마이저 (CBO) |
| :--- | :--- | :--- |
| **기준 (Criteria)** | 사전에 정의된 우선순위 규칙 (15단계 등) | 데이터 분포, 카디널리티 등 실제 비용(Cost) |
| **통계 정보** | 필요 없음 (인덱스 유무 등 구조 중심) | 필수 (건수, 선택도, 히스토그램 등) |
| **장점** | 실행 계획이 예측 가능하고 일관됨 | 현실적인 데이터 상태를 반영하여 최적화 |
| **단점** | 실제 데이터 양에 따른 유연성 부족 | 통계 정보의 정확도에 따른 의존성 큼 |
| **현재 추세** | 거의 사용되지 않음 (Legacy) | 현대 RDBMS(Oracle, MySQL, Postgres) 표준 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
1. **통계 정보의 무결성 관리**: CBO 체계에서 옵티마이저가 오판하는 가장 큰 원인은 낡은 통계 정보이다. 주기적인 `ANALYZE` 또는 `DBMS_STATS` 수행이 필수적이다.
2. **힌트(Hint)의 전략적 활용**: 옵티마이저가 항상 완벽하지는 않으므로, 개발자가 특정 인덱스 스캔이나 조인 방식을 강제하는 힌트를 사용하여 성능을 직접 튜닝할 수 있다.
3. **기술사적 판단**: 옵티마이저는 단순히 '빠른 길'을 찾는 것을 넘어, 전체 시스템의 자원 평형을 맞추는 역할을 한다. 따라서 튜닝 시에는 단일 쿼리의 속도뿐 아니라 전체 동시 부하(Concurrency) 상황에서의 자원 점유율을 함께 고려해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
옵티마이저 기술은 **지능형 자동 튜닝(Self-Tuning)**과 **적응형 쿼리 최적화(Adaptive Query Optimization)**로 진화하고 있다. 실행 도중 계획을 바꾸는 기능이나 AI/ML을 이용한 통계 예측 등이 도입되면서 DBA의 수동 튜닝 부담을 줄이고 있다. 결론적으로 옵티마이저에 대한 깊은 이해는 고성능 엔터프라이즈 데이터베이스 설계의 근간이 된다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: DBMS Architecture, Query Processor
- **자식 개념**: RBO, CBO, Execution Plan, Access Path
- **연관 개념**: Indexing, SQL Tuning, Statistics, Join Methods

---

### 👶 어린이를 위한 3줄 비유 설명
1. 옵티마이저는 우리가 보물찾기를 할 때 어디로 가야 가장 빨리 보물을 찾을지 알려주는 **똑똑한 길잡이 지도**예요.
2. 지도가 옛날 지도면 길을 잃을 수 있듯이, **최신 정보(통계)**를 계속 업데이트해줘야 정확한 길을 알려줘요.
3. 가끔은 우리가 지름길을 더 잘 알 때 **"여기로 가!"(힌트)**라고 직접 알려줄 수도 있답니다.
