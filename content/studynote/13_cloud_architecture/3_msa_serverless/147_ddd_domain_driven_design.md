+++
weight = 147
title = "도메인 주도 설계 (DDD)"
date = "2024-03-20"
[extra]
categories = ["cloud-architecture", "msa", "design"]
+++

## 핵심 인사이트 (3줄 요약)
1. 소프트웨어의 복잡성을 해결하기 위해 기술보다 비즈니스 도메인(업무 본질)을 설계의 중심에 두는 방법론입니다.
2. 기획자와 개발자가 동일한 '보편 언어(Ubiquitous Language)'를 사용하여 의사소통 오류를 줄이고 설계와 구현의 일관성을 유지합니다.
3. 바운디드 컨텍스트(Bounded Context)를 통해 시스템의 경계를 나누며, 이는 마이크로서비스(MSA)를 나누는 가장 강력한 논리적 근거가 됩니다.

### Ⅰ. 개요 (Context & Background)
시스템이 거대해질수록 비즈니스 요구사항과 실제 구현 코드 사이의 간극은 벌어지고 유지보수는 불가능해집니다. 에릭 에반스가 제안한 도메인 주도 설계(Domain-Driven Design, DDD)는 "소프트웨어의 진정한 가치는 기술적 화려함이 아닌 비즈니스 문제를 얼마나 정확히 해결하느냐"에 있다는 사상입니다. 이는 클라우드 네이티브 환경에서 서비스 간의 결합도를 낮추고 도메인 응집도를 높이기 위한 필수 설계 도구입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
[ Strategic Design ]         [ Tactical Design ]
+-------------------+        +---------------------+
| Ubiquitous Lang   |        |  Entity / Value Obj |
|         |         |        +----------|----------+
| Bounded Context   | ---->  |   Aggregate Root    |
|         |         |        +----------|----------+
|   Context Map     |        | Repository / Service|
+-------------------+        +---------------------+
```

**Bilingual Key Components:**
- **전략적 설계 (Strategic Design):** 비즈니스 경계를 나누고 컨텍스트 맵(Context Map)을 통해 서비스 간의 관계를 정의하는 거시적 설계입니다.
- **전술적 설계 (Tactical Design):** 엔티티(Entity), 값 객체(Value Object), 애그리게이트(Aggregate) 등을 활용해 도메인 모델을 구체화하는 미시적 설계입니다.
- **애그리게이트 (Aggregate):** 데이터 변경의 단위로 묶이는 객체들의 집합이며, 루트(Root)를 통해서만 일관성을 유지하며 접근합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 데이터 주도 설계 (Data-Driven) | 도메인 주도 설계 (DDD) |
| :--- | :--- | :--- |
| **설계 중심** | DB 테이블 및 관계 중심 | 비즈니스 행위 및 로직 중심 |
| **주요 모델** | E-R Diagram (ERD) | Domain Model (Object) |
| **변경 영향** | 스키마 변경 시 전체 영향 큼 | 도메인 경계 내에서 변경 격리 가능 |
| **적합성** | 단순 CRUD 위주 시스템 | 복잡한 비즈니스 규칙이 있는 시스템 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
기술사로서 DDD 도입 시 가장 주의해야 할 점은 '전술적 설계'에만 매몰되는 것입니다.
- **실행 전략:** 코드 레벨의 기술 패턴(Entity, Repository)보다 기획자와 소통하며 '보편 언어'를 정립하고 '바운디드 컨텍스트'를 정의하는 **전략적 설계**가 선행되어야 합니다.
- **감리 주안점:** 서비스 간의 불필요한 의존성(Anti-Corruption Layer 미비 등)이 있는지, 애그리게이트가 너무 크게 설계되어 트랜잭션 충돌이 발생하지 않는지 점검해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
DDD는 복잡한 소프트웨어 생태계에서 '변하지 않는 핵심 비즈니스 가치'를 보호하는 최선의 방안입니다. 최근에는 MSA뿐만 아니라 이벤트 주도 아키텍처(EDA)와 결합되어 비즈니스 이벤트를 설계의 중심에 두는 **이벤트 스토밍(Event Storming)** 기법으로 진화하고 있습니다. 결론적으로 DDD는 기술 부채를 최소화하고 지속 가능한 아키텍처를 구축하기 위한 기술사들의 강력한 설계 표준입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Software Architecture, Object-Oriented Design
- **하위 개념:** Bounded Context, Aggregate, Entity, VO, Repository
- **연관 개념:** MSA, Event Storming, Context Map, Ubiquitous Language

### 👶 어린이를 위한 3줄 비유 설명
1. **DDD**는 장난감 집을 지을 때, 건물을 튼튼하게 만드는 법보다 "누가 어디서 무엇을 하며 놀 것인가"를 먼저 생각하는 거예요.
2. 부엌 놀이를 하는 곳과 잠을 자는 침실의 경계를 확실히 나누어서 서로 방해하지 않게 하죠.
3. 요리사와 목수가 똑같은 이름으로 방을 불러야 헷갈리지 않고 멋진 집을 완성할 수 있답니다!
