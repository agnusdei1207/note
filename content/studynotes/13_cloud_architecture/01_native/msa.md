+++
title = "마이크로서비스 아키텍처 (MSA)"
date = 2024-05-13
description = "애플리케이션을 비즈니스 도메인 중심의 작고 독립적인 서비스들로 쪼개어(Loosely Coupled), 각기 다른 팀이 자율적으로 선택한 언어/DB로 개발 및 독립 배포하는 구조"
weight = 90
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["MSA", "Microservices", "SOA", "API Gateway", "Service Discovery", "DDD"]
+++

# 마이크로서비스 아키텍처 (MSA) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 모놀리식 애플리케이션을 비즈니스 도메인 단위로 분해하여, 각 서비스가 **독립적으로 개발, 배포, 확장**될 수 있도록 하는 분산 시스템 아키텍처 패턴입니다.
> 2. **가치**: 대규모 팀의 **조직 민첩성(Conway's Law 활용)**, 장애 격리, 기술 스택 자율성, 독립적 스케일링을 통해 복잡한 시스템을 효과적으로 관리합니다.
> 3. **융합**: 컨테이너(Docker), 오케스트레이션(Kubernetes), 서비스 메시(Istio), 이벤트 버스(Kafka), API 게이트웨이, 분산 추적(Jaeger) 등의 기술 스택과 결합합니다.

---

## Ⅰ. 개요 (Context & Background)

마이크로서비스 아키텍처(Microservices Architecture, MSA)는 단일 애플리케이션을 여러 작은 서비스로 분해하는 아키텍처 스타일입니다. 각 서비스는 특정 비즈니스 기능을 담당하며, 자체 데이터베이스를 소유하고, API를 통해서만 통신합니다. 서비스는 서로 느슨하게 결합(Loosely Coupled)되어 있어, 하나의 서비스 변경이 다른 서비스에 영향을 주지 않습니다.

**💡 비유**: MSA는 **'푸드트럭 단지'**와 같습니다. 모놀리식은 거대한 뷔페 레스토랑 하나에서 모든 음식을 만드는 것입니다. 주방이 꽉 막히면 전체가 느려지고, 파스타 담당 요리사가 아파도 전체가 문제입니다. 반면 푸드트럭 단지는 각 트럭(서비스)이 독립적으로 운영됩니다. 한 트럭이 고장 나도 다른 트ruck은 정상 영업합니다. 각 트럭은 자신만의 재료(DB), 조리법(기술 스택)을 사용할 수 있습니다.

**등장 배경 및 발전 과정**:
1. **모놀리식의 한계**: Netflix, Amazon, Uber 등 대규모 서비스 기업이 단일 코드베이스의 복잡성, 배포 리스크, 확장성 문제에 직면했습니다.
2. **SOA와의 차별화**: SOA(Service-Oriented Architecture)는 ESB(Enterprise Service Bus)라는 중앙 집중식 허브에 의존했으나, MSA는 분산된 지능(Choreography)을 지향합니다.
3. **Martin Fowler의 정리 (2014)**: Martin Fowler와 James Lewis가 마이크로서비스의 특징과 원칙을 체계화했습니다.
4. **클라우드 네이티브의 표준**: Kubernetes와 함께 클라우드 네이티브 아키텍처의 핵심 패턴이 되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 모놀리식 vs 마이크로서비스 비교

| 비교 관점 | 모놀리식 | 마이크로서비스 | 상세 분석 |
|---|---|---|---|
| **코드베이스** | 단일 리포지토리 | 다중 리포지토리 (Polyrepo) | MSA는 서비스별 독립 버전 관리 |
| **배포 단위** | 전체 애플리케이션 | 개별 서비스 | MSA는 부분 배포 가능 |
| **확장성** | 전체 인스턴스 복제 | 서비스별 개별 확장 | MSA는 효율적 리소스 사용 |
| **기술 스택** | 통일 필수 | 서비스별 자율 (Polyglot) | MSA는 최적 기술 선택 가능 |
| **데이터베이스** | 공유 DB | DB per Service | MSA는 데이터 소유권 분리 |
| **장애 영향** | 전체 장애 가능 | 부분 장애 격리 | MSA는 Blast Radius 제한 |
| **통신** | In-process Call | Network Call (REST/gRPC) | MSA는 네트워크 지연 고려 |
| **복잡도** | 코드 복잡도 | 운영 복잡도 | MSA는 분산 시스템 과제 |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                  [ Microservices Architecture ]                             │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌───────────────┐
                              │   Clients     │
                              │ Web / Mobile  │
                              └───────┬───────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          [ API Gateway ]                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Routing    │  │   Auth       │  │ Rate Limit   │  │  Request     │   │
│  │              │  │   (OAuth)    │  │  Throttling  │  │  Transform   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         │                            │                            │
         ▼                            ▼                            ▼
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  User Service   │         │ Order Service   │         │ Product Service │
│  ┌───────────┐  │         │  ┌───────────┐  │         │  ┌───────────┐  │
│  │   API     │  │         │  │   API     │  │         │  │   API     │  │
│  │  (Java)   │  │         │  │ (Python)  │  │         │  │  (Go)     │  │
│  └───────────┘  │         │  └───────────┘  │         │  └───────────┘  │
│  ┌───────────┐  │         │  ┌───────────┐  │         │  ┌───────────┐  │
│  │  Business │  │         │  │  Business │  │         │  │  Business │  │
│  │   Logic   │  │         │  │   Logic   │  │         │  │   Logic   │  │
│  └───────────┘  │         │  └───────────┘  │         │  └───────────┘  │
│  ┌───────────┐  │         │  ┌───────────┐  │         │  ┌───────────┐  │
│  │   MySQL   │  │         │  │ PostgreSQL│  │         │  │  MongoDB  │  │
│  │  (User DB)│  │         │  │(Order DB) │  │         │  │ (Prod DB) │  │
│  └───────────┘  │         │  └───────────┘  │         │  └───────────┘  │
└────────┬────────┘         └────────┬────────┘         └────────┬────────┘
         │                           │                           │
         │         Service Mesh (Istio / Linkerd)               │
         └───────────────────────────┬───────────────────────────┘
                                     │
┌────────────────────────────────────▼────────────────────────────────────────┐
│                      [ Infrastructure Layer ]                               │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                      Kubernetes Cluster                              │  │
│  │  ┌────────────────────────────────────────────────────────────────┐│  │
│  │  │                    Service Discovery (CoreDNS)                  ││  │
│  │  └────────────────────────────────────────────────────────────────┘│  │
│  │  ┌────────────────────────────────────────────────────────────────┐│  │
│  │  │                    ConfigMap / Secrets                          ││  │
│  │  └────────────────────────────────────────────────────────────────┘│  │
│  │  ┌────────────────────────────────────────────────────────────────┐│  │
│  │  │                    Ingress / LoadBalancer                       ││  │
│  │  └────────────────────────────────────────────────────────────────┘│  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │ Message Queue   │  │ Distributed     │  │ Observability   │            │
│  │ (Kafka/RabbitMQ)│  │ Tracing (Jaeger)│  │ (Prometheus/    │            │
│  │                 │  │                 │  │  Grafana)       │            │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: 서비스 간 통신 패턴

```
┌────────────────────────────────────────────────────────────────────────────┐
│                Service Communication Patterns                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ 1. Synchronous (동기) - REST/gRPC ]                                     │
│                                                                            │
│     Service A ──────── HTTP/gRPC ────────► Service B                       │
│                 (Request/Response)                                         │
│     Service A ◄──────── Response ───────── Service B                       │
│                                                                            │
│     장점: 간단, 즉시 응답                                                   │
│     단점: 결합도 높음, 장애 전파, 타임아웃                                  │
│                                                                            │
│  [ 2. Asynchronous (비동기) - Message Queue ]                              │
│                                                                            │
│     Service A ──── Publish Event ────► Message Queue ────► Service B       │
│                  (Fire and Forget)         (Kafka/RabbitMQ)                │
│                                                                            │
│     장점: 결합도 낮음, 장애 격리, 버퍼링                                     │
│     단점: 복잡성, 결과적 일관성                                             │
│                                                                            │
│  [ 3. Event-Driven Architecture (EDA) ]                                    │
│                                                                            │
│                    ┌──────────────────┐                                    │
│                    │   Event Bus      │                                    │
│                    │   (Kafka)        │                                    │
│                    └────────┬─────────┘                                    │
│                             │                                              │
│        ┌────────────────────┼────────────────────┐                        │
│        │ Publish            │ Subscribe          │ Subscribe              │
│        ▼                    ▼                    ▼                        │
│  ┌───────────┐        ┌───────────┐        ┌───────────┐                  │
│  │  Order    │        │  Payment  │        │ Inventory │                  │
│  │  Service  │        │  Service  │        │  Service  │                  │
│  └───────────┘        └───────────┘        └───────────┘                  │
│                                                                            │
│  [ 4. Service Mesh 통신 (mTLS) ]                                           │
│                                                                            │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐    │
│  │ Service A  │───►│  Envoy     │───►│  Envoy     │───►│ Service B  │    │
│  │ (Pod)      │    │ (Sidecar)  │    │ (Sidecar)  │    │ (Pod)      │    │
│  └────────────┘    └────────────┘    └────────────┘    └────────────┘    │
│                          mTLS encrypted                                    │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 패턴: Saga Pattern (분산 트랜잭션)

```python
# Saga Pattern - Choreography 방식 (Python 예시)

"""
주문 생성 Saga: Order → Payment → Inventory → Shipping
각 서비스가 이벤트를 발행/구독하여 순차적으로 진행
실패 시 보상 트랜잭션(Compensating Transaction) 역순 실행
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

class SagaStatus(Enum):
    STARTED = "started"
    PAYMENT_COMPLETED = "payment_completed"
    INVENTORY_RESERVED = "inventory_reserved"
    SHIPPING_SCHEDULED = "shipping_scheduled"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"

@dataclass
class OrderSaga:
    order_id: str
    status: SagaStatus
    payment_id: Optional[str] = None
    reservation_id: Optional[str] = None
    shipping_id: Optional[str] = None

class OrderSagaOrchestrator:
    """Saga 상태 기계 관리"""

    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.sagas = {}

    async def start_saga(self, order_id: str, order_data: dict):
        """Saga 시작"""
        saga = OrderSaga(order_id=order_id, status=SagaStatus.STARTED)
        self.sagas[order_id] = saga

        # Step 1: 결제 요청 이벤트 발행
        await self.event_bus.publish("PaymentRequested", {
            "order_id": order_id,
            "amount": order_data["amount"],
            "customer_id": order_data["customer_id"]
        })

    async def handle_payment_completed(self, event: dict):
        """결제 완료 이벤트 처리"""
        saga = self.sagas[event["order_id"]]
        saga.payment_id = event["payment_id"]
        saga.status = SagaStatus.PAYMENT_COMPLETED

        # Step 2: 재고 예약 요청 이벤트 발행
        await self.event_bus.publish("InventoryReservationRequested", {
            "order_id": saga.order_id,
            "items": event["items"]
        })

    async def handle_inventory_reserved(self, event: dict):
        """재고 예약 완료 이벤트 처리"""
        saga = self.sagas[event["order_id"]]
        saga.reservation_id = event["reservation_id"]
        saga.status = SagaStatus.INVENTORY_RESERVED

        # Step 3: 배송 예약 요청 이벤트 발행
        await self.event_bus.publish("ShippingRequested", {
            "order_id": saga.order_id,
            "address": event["shipping_address"]
        })

    async def handle_shipping_scheduled(self, event: dict):
        """배송 예약 완료 - Saga 완료"""
        saga = self.sagas[event["order_id"]]
        saga.shipping_id = event["shipping_id"]
        saga.status = SagaStatus.COMPLETED

        await self.event_bus.publish("OrderCompleted", {
            "order_id": saga.order_id
        })

    async def compensate(self, order_id: str, failed_step: str):
        """보상 트랜잭션 실행 (역순)"""
        saga = self.sagas[order_id]
        saga.status = SagaStatus.COMPENSATING

        # 실패 단계 이전의 완료된 작업들 역순 보상
        if saga.shipping_id:
            await self.event_bus.publish("ShippingCancelled", {
                "shipping_id": saga.shipping_id
            })
        if saga.reservation_id:
            await self.event_bus.publish("InventoryReservationReleased", {
                "reservation_id": saga.reservation_id
            })
        if saga.payment_id:
            await self.event_bus.publish("PaymentRefunded", {
                "payment_id": saga.payment_id
            })

        saga.status = SagaStatus.FAILED
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 모놀리식 vs MSA

| 비교 관점 | 모놀리식 | MSA | 선택 기준 |
|---|---|---|---|
| **팀 규모** | Small (5-10명) | Large (50명+) | 작은 팀은 모놀리식 효율적 |
| **복잡도** | 낮음 | 높음 (분산 시스템) | 단순 서비스는 모놀리식 |
| **배포 빈도** | 낮음 (월/주) | 높음 (일/시간) | 잦은 배포는 MSA |
| **확장성 요구** | 균일 | 서비스별 상이 | 불균등 확장은 MSA |
| **SLA 요구** | 일반 | 엄격 (부분 장애 허용) | 고가용성은 MSA |
| **개발 속도** | 느림 (전체 빌드) | 빠름 (서비스별) | 민첩성은 MSA |

### 과목 융합 관점 분석

**DDD(Domain-Driven Design)와의 융합**:
- MSA의 서비스 경계는 DDD의 **Bounded Context**에서 도출됩니다.
- 각 서비스는 하나의 **Aggregate Root**를 중심으로 설계됩니다.

**데이터베이스와의 융합**:
- **Database per Service**: 각 서비스가 자체 DB 소유
- **Polyglot Persistence**: 서비스별 최적 DB 선택 (RDBMS, NoSQL, Graph)
- **CDC(Change Data Capture)**: 서비스 간 데이터 동기화

**보안(Security)과의 융합**:
- **Zero Trust**: 서비스 간 모든 통신 인증/인가
- **mTLS**: 서비스 메시에서 자동 암호화
- **API Gateway**: 중앙 집중식 인증

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 모놀리식 → MSA 전환

**문제 상황**: 전자상거래 모놀리식 애플리케이션이 500만 라인, 배포에 4시간 소요, 장애 시 전체 다운.

**기술사의 전략적 의사결정**:
1. **Strangler Fig Pattern**: API Gateway 뒤에서 점진적 전환
2. **우선 분리 서비스**: 가장 변경 빈도 높은 서비스부터 (예: 상품 검색)
3. **데이터 분리**: 공유 DB → DB per Service 점진적 이관
4. **운영 도구 선도 구축**: Observability, CI/CD, Service Mesh

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - Distributed Monolith**: 서비스를 나눴지만 강결합(동기 호출 체인)으로 인해 여전히 전체 장애 발생.
- **체크리스트**:
  - [ ] 비즈니스 도메인 분석 완료 (DDD)
  - [ ] 서비스 경계 정의 (Bounded Context)
  - [ ] API 계약 정의 (OpenAPI)
  - [ ] Observability 구축 계획
  - [ ] 팀 구조 재편 (Two-Pizza Team)

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 모놀리식 | MSA | 개선율 |
|---|---|---|---|
| **배포 빈도** | 월 1회 | 일 10회+ | 300x |
| **복구 시간 (MTTR)** | 4시간 | 15분 | 94% 단축 |
| **확장 효율** | 100% (전체) | 20% (필요 서비스만) | 80% 절감 |
| **팀 생산성** | Baseline | 2x | 100% 향상 |

### 미래 전망 및 진화 방향

- **Modular Monolith**: MSA의 복잡도를 피하면서 모듈성을 유지하는 중간 지점
- **Serverless Microservices**: FaaS 기반으로 더 작은 단위로 분해
- **WASM Microservices**: WebAssembly로 언어 중립적 서비스 구현

### ※ 참고 표준/가이드
- **Martin Fowler's Microservices Guide**: 마이크로서비스 원칙
- **12-Factor App**: 클라우드 네이티브 애플리케이션 설계 원칙
- **Sam Newman's Building Microservices**: 실무 가이드북

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [API 게이트웨이 (API Gateway)](@/studynotes/13_cloud_architecture/01_native/api_gateway.md) : MSA 진입점
- [서비스 디스커버리 (Service Discovery)](@/studynotes/13_cloud_architecture/01_native/service_discovery.md) : 서비스 위치 찾기
- [서비스 메시 (Service Mesh)](@/studynotes/13_cloud_architecture/01_native/service_mesh.md) : 서비스 간 통신 관리
- [사가 패턴 (Saga Pattern)](@/studynotes/13_cloud_architecture/01_native/saga_pattern.md) : 분산 트랜잭션
- [이벤트 기반 아키텍처 (EDA)](@/studynotes/13_cloud_architecture/01_native/eda.md) : 비동기 통신

---

### 👶 어린이를 위한 3줄 비유 설명
1. MSA는 **'푸드트럭 단지'**예요. 거대한 뷔페(모놀리식) 대신, 여러 푸드트럭(서비스)이 각자 음식을 만들어요.
2. 각 트럭은 **'자신만의 재료와 조리법'**을 써요. 파스타 트럭은 이탈리아 재료, 타코 트럭은 멕시코 재료!
3. 한 트럭이 고장 나도 **'다른 트럭은 정상 영업해요'**. 그래서 전체가 멈추는 일이 없어요!
