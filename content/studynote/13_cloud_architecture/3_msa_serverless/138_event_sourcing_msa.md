+++
weight = 138
title = "이벤트 소싱 (Event Sourcing)"
date = "2026-03-04"
[extra]
categories = "studynote-cloud"
+++

## 핵심 인사이트 (3줄 요약)
1. **상태 대신 사건 저장**: 데이터의 최종 상태(Current State)를 저장하는 대신, 객체의 모든 상태 변화 과정(Event)을 순차적인 로그로 저장하는 기법입니다.
2. **완벽한 감사 및 복원**: 모든 사건이 영구 저장되므로 특정 시점의 상태로 완벽하게 복원(Time Travel)이 가능하며 신뢰할 수 있는 감사 로그(Audit Trail)를 제공합니다.
3. **비즈니스 중심 설계**: 데이터 중심이 아닌 비즈니스 도메인 내에서 발생하는 행위(Event) 중심으로 아키텍처를 설계하여 복잡한 비즈니스 로직을 명확히 모델링합니다.

### Ⅰ. 개요 (Context & Background)
전통적인 CRUD 기반의 데이터베이스 관리는 최종 상태만 유지하므로, '어떻게' 그 상태가 되었는지에 대한 맥락이 유실됩니다. 이벤트 소싱은 상태 변화를 유발하는 모든 사건을 불변(Immutable)의 스트림으로 기록하여, 언제든지 해당 스트림을 재생(Replay)함으로써 상태를 재구축할 수 있도록 합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
이벤트 소싱은 이벤트 스토어(Event Store), 도메인 엔티티(Entity), 그리고 투영(Projection)으로 구성됩니다.

```text
 [ Command ] ----> [ Command Handler ] ----> [ Domain Entity ]
                         |                         |
                         v                         v
 [ Snapshot ] <---- [ Event Store ] ----(Append) [ New Events ]
                         |
                         +---(Notify/Replay)---> [ Projections/Read Models ]

  <Bilingual Architectural Flow>
  1. Capture state changes as sequence of events. -> 상태 변화를 사건의 순차열로 캡처
  2. Append-only storage in Event Store. -> 이벤트 스토어에 추가 전용 저장
  3. Replay events to restore state. -> 사건을 재생하여 상태 복원
```

- **Event Store**: 삽입만 가능(Append-only)한 불변의 저장소입니다. 수정이나 삭제는 불가능합니다.
- **Snapshot**: 이벤트가 너무 많아질 경우 재생 시간을 단축하기 위해 특정 시점의 상태를 저장해두는 중간 체크포인트입니다.
- **Projection**: 저장된 이벤트를 바탕으로 사용자에게 보여줄 읽기 전용 데이터 모델을 생성합니다. (CQRS와 연계)

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
기존 상태 기반 저장 방식과 이벤트 소싱 방식을 비교합니다.

| 구분 | 상태 기반 (CRUD) | 이벤트 소싱 (Event Sourcing) |
| :--- | :--- | :--- |
| **저장 대상** | 현재의 최종 값 (Current Value) | 상태 변화의 원인 (Event) |
| **변경 방식** | 덮어쓰기 (Update/Delete) | 오직 추가 (Append-only) |
| **데이터 보존** | 과거 내역 유실 가능성 높음 | 모든 이력(History) 완벽 보존 |
| **성능 특징** | 조회는 빠르나 락(Lock) 경합 존재 | 쓰기가 매우 빠르고 락프리 구현 가능 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **적용 케이스**: 
    - 금융 시스템 (계좌 거래 내역, 이체 기록)
    - 전자상거래 (주문 상태 전이: 주문접수->결제완료->배송중)
    - 버전 관리 시스템 (Git의 커밋 히스토리)
- **기술사적 판단**: 이벤트 소싱은 **CQRS** 패턴과 결합했을 때 진정한 위력을 발휘합니다. 이벤트 스토어는 쓰기 모델(Write Model)이 되고, 이를 투영한 결과가 읽기 모델(Read Model)이 됩니다. 다만, **이벤트 스키마의 버전 관리(Versioning)**와 **데이터 보정(Compensation)** 처리가 매우 까다로우므로 모든 도메인에 적용하기보다 트래킹이 중요한 핵심 비즈니스 도메인에 우선 적용해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
이벤트 소싱은 데이터 무결성과 투명성을 극대화하며, 복잡한 분산 환경에서 시스템 간의 **동기화와 회복 탄력성**을 높여줍니다. 특히 머신러닝을 위한 원천 데이터(Raw Data)로 활용될 수 있어 미래 가치가 매우 높은 아키텍처 패러다임입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: 마이크로서비스 아키텍처(MSA), 불변 인프라(Immutable)
- **핵심 기술**: 카프카(Kafka), Axon Framework, 이벤트 스토어
- **연관 패턴**: CQRS, 사가 패턴(Saga)

### 👶 어린이를 위한 3줄 비유 설명
1. **은행 통장 내역**을 생각해보세요.
2. 내 통장의 마지막 '잔액'만 기록하는 게 아니라, '엄마가 용돈 준 사건', '장난감 산 사건'을 하나하나 적는 거예요.
3. 이 적힌 일기장만 다시 읽어보면, 내가 돈을 어떻게 썼는지 전부 알 수 있고 잔액도 다시 계산할 수 있답니다.
