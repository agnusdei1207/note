+++
weight = 132
title = "폴리글랏 퍼시스턴스 (Polyglot Persistence)"
date = "2024-03-20"
[extra]
categories = "studynote-cloud"
+++

## 핵심 인사이트 (3줄 요약)
- '하나의 DB가 모든 문제를 해결한다'는 고정관념에서 벗어나, 데이터의 특성과 서비스 요건에 맞춰 **다양한 종류의 DB(RDBMS, NoSQL 등)를 혼용**하는 전략임.
- 각 서비스에 최적화된 데이터 저장소를 선택하여 **성능(Performance), 확장성(Scalability), 유연성**을 극대화함.
- 마이크로서비스 아키텍처(MSA)의 '서비스별 DB' 패턴을 구현하기 위한 핵심적인 기술적 방법론임.

### Ⅰ. 개요 (Context & Background)
- 과거에는 오라클이나 MySQL 같은 RDBMS 하나에 모든 데이터를 담았으나, 대규모 트래픽과 다양한 데이터 형태(비정형, 시계열, 관계)를 처리하는 데 한계가 발생함.
- "한 가지 도구가 모든 작업에 최선일 수 없다(One Size Does Not Fit All)"는 철학을 바탕으로 데이터 저장 기술의 적재적소(Right Tool for the Job) 활용을 지향함.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ Polyglot Persistence Architecture ]

        (Microservice Architecture)
          /       |        \
    [Order]    [Catalog]    [Search]    [Analysis]
      |           |           |           |
    /---\       /---\       /---\       /---\
    |RDB |      |Cache|     |Search|    |Graph|  <--- 데이터 특성별 DB 매핑
    |SQL |      |Redis|     |ES    |    |Neo4j|
    \---/       \---/       \---/       \---/
    (관계/트랜잭션) (고속 조회) (Full-Text) (복잡한 관계)

* 원리: 데이터의 '모델'과 '액세스 패턴'에 따른 최적화
```
- **RDBMS (Relational)**: 정규화, 복잡한 조인, 강력한 ACID 트랜잭션이 필요한 금융, 주문 데이터에 활용.
- **Key-Value (NoSQL)**: 세션 관리, 장바구니 등 단순하고 빠른 조회가 필요한 영역에 Redis, DynamoDB 활용.
- **Document (NoSQL)**: 상품 설명, 로그 등 스키마가 유연한 데이터에 MongoDB 활용.
- **Search Engine**: 대량의 텍스트 검색 및 분석에 Elasticsearch 활용.
- **Graph DB**: 추천 시스템, 소셜 네트워크 등 객체 간의 복잡한 관계 쿼리에 Neo4j 활용.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 단일 데이터베이스 (Single DB) | 폴리글랏 퍼시스턴스 (Polyglot) |
| :--- | :--- | :--- |
| **개발 난이도** | 상대적으로 쉬움 (일관된 모델) | 높음 (다양한 DB 기술 습득 필요) |
| **성능 최적화** | 한계 존재 (특수 쿼리 취약) | 각 영역에서 최상의 성능 발휘 |
| **운영 비용** | 라이선스 및 관리 단일화 | 백업/모니터링 대상 증가 (복잡도 상승) |
| **데이터 정합성** | 즉각적인 ACID 보장 | 결과적 일관성 (Eventual Consistency) 중심 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **판단 지표**: 서비스별로 트래픽의 성격이 극명하게 다르고, 데이터 모델이 관계형으로만 표현하기 어렵거나, 대규모 수평 확장이 필수적일 때 도입함.
- **적용 전략**: 초기에는 RDBMS를 중심으로 운영하되, 병목이 발생하는 특정 기능부터 NoSQL이나 전용 검색 엔진으로 분리하는 '점진적 전환' 전략이 유효함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- 시스템의 **확장성(Scalability)**과 **가용성(Availability)**을 비약적으로 향상시켜 현대의 초대규모 서비스 운영을 가능케 함.
- 향후 AI 및 빅데이터와 결합하여 데이터 레이크하우스(Lakehouse) 환경과 유기적으로 연동되는 필수적인 데이터 아키텍처 표준이 됨.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 마이크로서비스 아키텍처 (MSA), 서비스별 DB
- **관련 기술**: NoSQL (CAP 이론), RDBMS (ACID), 검색 엔진
- **핵심 이론**: CAP 정리, PACELC 정리

### 👶 어린이를 위한 3줄 비유 설명
- 학용품을 필통 하나에 다 넣지 않고, 색칠할 땐 '색연필', 글씨 쓸 땐 '연필', 선 그을 땐 '자'를 쓰는 것과 같아요.
- 연필로 색칠할 순 있지만, 색연필을 쓰면 훨씬 예쁘고 빠르게 색칠할 수 있는 것과 같은 원리에요.
- 해야 할 일에 가장 잘 어울리는 도구를 골라서 쓰는 똑똑한 방법이랍니다.
