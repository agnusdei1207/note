+++
title = "MSA (Microservices Architecture, 마이크로서비스 아키텍처)"
date = "2026-03-04"
[extra]
categories = "studynotes-enterprise"
+++

# MSA (Microservices Architecture, 마이크로서비스 아키텍처)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 거대한 모놀리식(Monolithic) 애플리케이션을 **독립적으로 개발, 배포, 확장 가능한 수십~수백 개의 작은 서비스로 분해**하는 아키텍처 스타일로, 각 서비스는 자체 데이터베이스를 소유하고 API로 통신합니다.
> 2. **가치**: 배포 주기 단축(일/주 단위), 기술 스택의 유연성, 장애 격리(Fault Isolation), 조직 단위의 자율성(Conway's Law 활용)을 통해 비즈니스 민첩성을 극대화합니다.
> 3. **융합**: Container(Docker), Orchestration(Kubernetes), Service Mesh(Istio), API Gateway, Event-Driven Architecture(Kafka) 등 클라우드 네이티브 기술 스택과 필연적으로 결합됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. MSA의 개념 및 철학적 근간
마이크로서비스 아키텍처(MSA)는 2014년 마틴 파울러(Martin Fowler)와 제임스 루이스(James Lewis)가 정립한 아키텍처 스타일으로, **"하나의 애플리케이션을 작고, 자율적이며, 느슨하게 결합된 서비스들의 집합으로 구성하는 접근법"**입니다. MSA의 핵심 철학은 **"Smart Endpoints, Dumb Pipes"**입니다. 즉, 비즈니스 로직은 서비스 내부에 캡슐화(Smart Endpoints)하고, 서비스 간 통신은 가능한 한 단순한 프로토콜(Dumb Pipes)로 수행합니다. 이는 ESB(Enterprise Service Bus)의 "Smart Pipe, Dumb Endpoint"와 정반대되는 철학입니다. 각 서비스는 **단일 비즈니스 역량(Single Business Capability)**에 집중하며, 자체 데이터베이스를 소유(Database per Service)함으로써 진정한 독립성을 확보합니다.

#### 2. 💡 비유를 통한 이해: 대형 병원 vs 전문 클리닉
모놀리식 아키텍처는 모든 진료과가 하나의 거대한 건물에 모여 있고, 모든 환자 기록이 중앙 파일실에 보관되는 '대형 종합병원'입니다. 내과에서 수술을 변경하면 병원 전체가 리노베이션되어야 합니다. **MSA는 각 진료과가 독립적인 건물에 위치한 '전문 클리닉들의 네트워크'입니다.** 피부과 클리닉을 확장해도 내과 클리닉에 영향이 없습니다. 각 클리닉은 자체 환자 기록을 보관하고, 다른 클리닉과는 전화(API)로 협진합니다. 한 클리닉이 잠시 문을 닫아도 다른 클리닉은 정상 진료가 가능합니다.

#### 3. 등장 배경 및 발전 과정
- **2000년대 초~중반**: SOA(Service Oriented Architecture) 열풍, ESB 중심 통합
- **2011년**: Vimeo의 Adrian Cockcroft가 Netflix의 아키텍처를 'Microservices'라고 명명
- **2014년**: Martin Fowler의 "Microservices" 글 게재, MSA 개념 정립
- **2014~2015년**: Netflix OSS, Spring Cloud 등 MSA 프레임워크 등장
- **2015~2017년**: Docker, Kubernetes의 폭발적 성장으로 MSA 구현 용이
- **2018년~현재**: Cloud Native, Service Mesh, Event-Driven MSA로 진화

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 모놀리식 vs 마이크로서비스 아키텍처 비교

| 구분 | 모놀리식 (Monolithic) | 마이크로서비스 (MSA) |
| :--- | :--- | :--- |
| **구조** | 단일 코드베이스, 단일 배포 아티팩트 | 다중 서비스, 독립 배포 |
| **데이터베이스** | 공유 데이터베이스 | Database per Service |
| **확장성** | 전체 애플리케이션 확장 (Scale-up/Clone) | 서비스별 개별 확장 |
| **기술 스택** | 단일 기술 스택 강제 | 서비스별 기술 선택 가능 (Polyglot) |
| **장애 격리** | 전체 장애 가능성 | 부분 장애 격리 |
| **배포 주기** | 월/분기 단위 | 일/주 단위 (CI/CD) |
| **팀 구조** | 기능별 팀 (DB팀, Front팀) | Cross-functional 팀 (Service별) |
| **통신** | In-process 호출 (함수 호출) | Network 호출 (API, Event) |
| **복잡도** | 단순 (초기) / 복잡 (후기) | 복잡 (초기부터) |

#### 2. MSA 전체 아키텍처 다이어그램

```text
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              [ CLIENT LAYER ]                                       │
│          ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│          │   Web App   │    │  Mobile App │    │  3rd Party  │                     │
│          └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                     │
└─────────────────┼──────────────────┼──────────────────┼────────────────────────────┘
                  │                  │                  │
                  └──────────────────┼──────────────────┘
                                     │
┌────────────────────────────────────▼────────────────────────────────────────────────┐
│                         [ API GATEWAY LAYER ]                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                         API Gateway (Kong / AWS API Gateway)                │   │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────────┐  │   │
│  │  │ Routing   │ │ Rate      │ │ Auth/     │ │ Load      │ │ Request/     │  │   │
│  │  │           │ │ Limiting  │ │ Authz     │ │ Balancing │ │ Response Agg │  │   │
│  │  └───────────┘ └───────────┘ └───────────┘ └───────────┘ └───────────────┘  │   │
│  └─────────────────────────────────────┬───────────────────────────────────────┘   │
└────────────────────────────────────────┼────────────────────────────────────────────┘
                                         │
┌────────────────────────────────────────▼────────────────────────────────────────────┐
│                       [ SERVICE MESH LAYER (Istio/Linkerd) ]                        │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │   ┌──────────────────────────────────────────────────────────────────────┐  │   │
│  │   │  Sidecar Proxy (Envoy) per Service                                   │  │   │
│  │   │  - Service Discovery   - Circuit Breaker    - mTLS Encryption        │  │   │
│  │   │  - Traffic Shifting    - Observability       - Retry & Timeout       │  │   │
│  │   └──────────────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────┬───────────────────────────────────────┘   │
└────────────────────────────────────────┼────────────────────────────────────────────┘
                                         │
┌────────────────────────────────────────▼────────────────────────────────────────────┐
│                         [ MICROSERVICES LAYER ]                                     │
│                                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │
│  │   User      │  │   Order     │  │  Payment    │  │  Inventory  │               │
│  │  Service    │  │  Service    │  │  Service    │  │  Service    │               │
│  │  (Java)     │  │  (Go)       │  │  (Python)   │  │  (Node.js)  │               │
│  │  ┌───────┐  │  │  ┌───────┐  │  │  ┌───────┐  │  │  ┌───────┐  │               │
│  │  │ User  │  │  │  │Order  │  │  │  │Pay    │  │  │  │Invent │  │               │
│  │  │  DB   │  │  │  │  DB   │  │  │  │  DB   │  │  │  │  DB   │  │               │
│  │  │(Postgr│  │  │  │(MongoDB)  │  │  │(MySQL)│  │  │  │(Redis)│  │               │
│  │  └───────┘  │  │  └───────┘  │  │  └───────┘  │  │  └───────┘  │               │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘               │
│         │                │                │                │                       │
└─────────┼────────────────┼────────────────┼────────────────┼───────────────────────┘
          │                │                │                │
          └────────────────┴────────────────┴────────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │   [ EVENT BUS (Kafka) ]     │
                    │  - OrderCreated             │
                    │  - PaymentCompleted         │
                    │  - InventoryReserved        │
                    └─────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         [ INFRASTRUCTURE LAYER ]                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │
│  │ Kubernetes  │  │ Service     │  │ Config      │  │ Centralized │               │
│  │ (Orchestrate)│  │ Discovery   │  │ Server      │  │ Logging     │               │
│  │             │  │ (Eureka)    │  │ (Consul)    │  │ (ELK Stack) │               │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                                │
│  │ Distributed │  │ Metrics     │  │ CI/CD       │                                │
│  │ Tracing     │  │ (Prometheus)│  │ (Jenkins/   │                                │
│  │ (Jaeger)    │  │             │  │  ArgoCD)    │                                │
│  └─────────────┘  └─────────────┘  └─────────────┘                                │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

#### 3. MSA 핵심 패턴 상세 분석

| 패턴 명칭 | 문제 정의 | 해결 방안 | 기술 예시 |
| :--- | :--- | :--- | :--- |
| **API Gateway** | 클라이언트가 여러 서비스에 직접 접근 시 복잡성 증가 | 단일 진입점 제공, 라우팅, 인증, Rate Limiting | Kong, AWS API Gateway, Zuul |
| **Service Discovery** | 동적 IP/Port의 서비스 위치 확인 | 서비스 레지스트리에 등록/조회 | Eureka, Consul, K8s Service |
| **Circuit Breaker** | 서비스 장애 시 연쇄 장애(Cascading Failure) 방지 | 장애 감지 시 호출 차단(Open), Fallback 제공 | Hystrix, Resilience4j |
| **Saga Pattern** | 분산 트랜잭션에서 ACID 보장 불가 | 각 서비스 로컬 트랜잭션 + 보상 트랜잭션 | Choreography, Orchestration |
| **CQRS** | 복잡한 도메인에서 조회 성능 저하 | 명령(Command)과 조회(Query) 모델 분리 | Event Sourcing과 결합 |
| **Event Sourcing** | 상태 변경 이력 추적 불가 | 이벤트 로그를 Append-Only 저장 | Kafka, EventStore |
| **Database per Service** | 서비스 간 데이터 결합도 증가 | 각 서비스가 자체 DB 소유 | Polyglot Persistence |
| **Sidecar** | 횡단 관심사(Cross-cutting) 중복 구현 | 프록시 컨테이너를 메인 컨테이너 옆에 배치 | Envoy, Istio Sidecar |
| **Strangler Fig** | 모놀리식을 일시 중단 없이 MSA로 전환 | API Gateway에서 트래픽을 점진적 신규 서비스로 라우팅 | - |

#### 4. Saga 패턴 구현 Python 코드 (오케스트레이션 방식)

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SagaStatus(Enum):
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"
    COMPENSATING = "COMPENSATING"
    FAILED = "FAILED"

@dataclass
class SagaStep:
    """Saga 단계 정의"""
    name: str
    action: callable           # 실행할 액션
    compensation: callable     # 보상 트랜잭션
    status: str = "PENDING"

class OrderSagaOrchestrator:
    """주문 처리 Saga 오케스트레이터"""

    def __init__(self):
        self.steps: List[SagaStep] = []
        self.current_step = 0
        self.status = SagaStatus.STARTED
        self.completed_actions: List[str] = []

    def add_step(self, name: str, action: callable, compensation: callable):
        """Saga 단계 추가"""
        self.steps.append(SagaStep(name, action, compensation))

    def execute(self):
        """Saga 실행"""
        logger.info("=== Saga 실행 시작 ===")

        for i, step in enumerate(self.steps):
            self.current_step = i
            logger.info(f"Step {i+1}/{len(self.steps)}: {step.name} 실행 중...")

            try:
                result = step.action()
                step.status = "COMPLETED"
                self.completed_actions.append(step.name)
                logger.info(f"✓ {step.name} 완료: {result}")

            except Exception as e:
                logger.error(f"✗ {step.name} 실패: {e}")
                step.status = "FAILED"
                self.status = SagaStatus.COMPENSATING
                self._compensate()
                self.status = SagaStatus.FAILED
                return False

        self.status = SagaStatus.COMPLETED
        logger.info("=== Saga 실행 완료 ===")
        return True

    def _compensate(self):
        """보상 트랜잭션 실행 (역순)"""
        logger.warning("=== 보상 트랜잭션 시작 ===")

        # 완료된 단계의 역순으로 보상 실행
        for i in range(self.current_step, -1, -1):
            step = self.steps[i]
            if step.status == "COMPLETED":
                logger.info(f"Compensating: {step.name}...")
                try:
                    step.compensation()
                    logger.info(f"✓ {step.name} 보상 완료")
                except Exception as e:
                    logger.error(f"✗ {step.name} 보상 실패: {e}")

        logger.warning("=== 보상 트랜잭션 완료 ===")

# === 예시: 주문 생성 Saga ===

# Mock 서비스들
class InventoryService:
    def reserve(self, order_id: str, items: list) -> dict:
        """재고 예약"""
        logger.info(f"[InventoryService] 재고 예약: {order_id}")
        return {"reservation_id": f"RES-{order_id}", "status": "RESERVED"}

    def release(self, reservation_id: str):
        """재고 예약 해제 (보상)"""
        logger.info(f"[InventoryService] 재고 예약 해제: {reservation_id}")

class PaymentService:
    def charge(self, order_id: str, amount: int) -> dict:
        """결제 처리"""
        logger.info(f"[PaymentService] 결제 처리: {order_id}, 금액: {amount}")
        # 시나리오: 결제 실패를 시뮬레이션
        if amount > 100000:
            raise Exception("결제 한도 초과")
        return {"transaction_id": f"TXN-{order_id}", "status": "APPROVED"}

    def refund(self, transaction_id: str):
        """결제 취소 (보상)"""
        logger.info(f"[PaymentService] 결제 취소: {transaction_id}")

class OrderService:
    def create(self, order_id: str) -> dict:
        """주문 생성"""
        logger.info(f"[OrderService] 주문 생성: {order_id}")
        return {"order_id": order_id, "status": "CREATED"}

    def cancel(self, order_id: str):
        """주문 취소 (보상)"""
        logger.info(f"[OrderService] 주문 취소: {order_id}")

# Saga 실행 예시
if __name__ == "__main__":
    inventory_svc = InventoryService()
    payment_svc = PaymentService()
    order_svc = OrderService()

    # Saga 오케스트레이터 생성
    saga = OrderSagaOrchestrator()

    # 단계 추가
    order_id = "ORD-2024-001"
    saga.add_step(
        name="Create Order",
        action=lambda: order_svc.create(order_id),
        compensation=lambda: order_svc.cancel(order_id)
    )
    saga.add_step(
        name="Reserve Inventory",
        action=lambda: inventory_svc.reserve(order_id, [{"product": "A", "qty": 2}]),
        compensation=lambda: inventory_svc.release(f"RES-{order_id}")
    )
    saga.add_step(
        name="Process Payment",
        action=lambda: payment_svc.charge(order_id, 50000),  # 정상
        # action=lambda: payment_svc.charge(order_id, 150000),  # 실패 시나리오
        compensation=lambda: payment_svc.refund(f"TXN-{order_id}")
    )

    # Saga 실행
    success = saga.execute()
    print(f"\n최종 상태: {saga.status.value}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. SOA vs MSA 비교 분석

| 구분 | SOA (Service Oriented Architecture) | MSA (Microservices Architecture) |
| :--- | :--- | :--- |
| **서비스 규모** | 대형, 엔터프라이즈급 | 소형, 단일 책임 |
| **통신 방식** | Smart Pipe (ESB 중심) | Dumb Pipe (API/Event) |
| **데이터 공유** | 공유 데이터베이스 | Database per Service |
| **표준** | WS-*, SOAP, WSDL | REST, gRPC, Async Event |
| **거버넌스** | 중앙 집중형 | 분산형, 팀 자율 |
| **배포** | ESB 포함 전체 배포 | 서비스별 독립 배포 |
| **적합한 환경** | 엔터프라이즈, 레거시 통합 | 클라우드 네이티브, 스타트업 |

#### 2. 과목 융합 관점 분석
- **클라우드 컴퓨팅 (Cloud Native)**: MSA는 클라우드 네이티브의 핵심 아키텍처입니다. Container(Docker), Orchestration(Kubernetes), DevOps, CI/CD와 필연적으로 결합됩니다.
- **네트워크 (Service Mesh)**: MSA의 서비스 간 통신, 보안(mTLS), 관측성(Observability)은 Service Mesh(Istio, Linkerd)가 담당합니다.
- **데이터베이스 (Polyglot Persistence)**: 각 서비스가 목적에 맞는 DB를 선택할 수 있습니다. (예: 사용자 서비스-PostgreSQL, 캐시-Redis, 검색-Elasticsearch)

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단: 모놀리식 vs MSA 선택 기준
**[상황]** 스타트업 G사가 초기 제품을 개발 중입니다. MSA를 도입할까요?

**[의사결정 매트릭스]**

| 평가 기준 | 모놀리식 권장 | MSA 권장 |
| :--- | :--- | :--- |
| **팀 규모** | 1~2개 팀 (5~10명) | 3개 팀 이상 (20명+) |
| **도메인 복잡도** | 단순 | 복잡 (여러 비즈니스 도메인) |
| **배포 빈도** | 주/월 1회 | 일/주 다회 |
| **확장성 요구** | 전체 확장으로 충분 | 특정 기능만 확장 필요 |
| **개발 단계** | 초기 (Product-Market Fit 전) | 성숙기 (트래픽 폭증) |

**[권장사항]**
- **초기 스타트업**: 모놀리식으로 빠르게 개발 → 성공 후 MSA로 분리
- **대기업 디지털 플랫폼**: MSA 또는 Modular Monolith
- **레거시 현대화**: Strangler Fig 패턴으로 점진적 MSA 전환

#### 2. 도입 시 고려사항 (Checklist)
- **조직적 준비**: DevOps 문화, Cross-functional 팀 구성
- **기술적 준비**: Container, Kubernetes, CI/CD Pipeline, Observability Stack
- **데이터 분리 전략**: 공유 DB → Database per Service 전환 계획
- **테스트 전략**: Contract Testing, Consumer-Driven Contract

#### 3. 안티패턴 (Anti-patterns): MSA 실패의 대표적 원인
1. **"분산 모놀리식 (Distributed Monolith)"**: 서비스는 분리했지만 여전히 강결합(Tight Coupling)되어, 하나 변경하면 모두 재배포해야 하는 상황
2. **"데이터 일관성 무시"**: 분산 트랜잭션 문제를 간과하여 데이터 불일치 발생
3. **"나노 서비스 (Nano-services)"**: 너무 잘게 쪼개어 통신 오버헤드와 복잡도 폭증
4. **"관측성(Observability) 부재"**: 분산 환경에서 장애 원인 파악 불가

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 개선 항목 | MSA 도입 시 기대효과 |
| :--- | :--- | :--- |
| **배포 속도** | 배포 주기 | 월 1회 → 일 1회 이상 |
| **장애 영향** | 서비스 장애 범위 | 전체 서비스 → 단일 서비스 격리 |
| **확장 효율** | 리소스 활용률 | 30~40% → 60~80% (개별 확장) |
| **개발 생산성** | 기능 개발 속도 | 20~30% 향상 (팀 자율성) |

#### 2. 미래 전망: MSA 2.0 & Beyond
- **Dapr (Distributed Application Runtime)**: 분산 애플리케이션의 횡단 관심사를 추상화한 런타임
- **Serverless Microservices**: FaaS(Function as a Service) 기반 마이크로서비스
- **Edge Computing**: 엣지에서 실행되는 초경량 마이크로서비스
- **WASM (WebAssembly)**: 폴리글랏 서비스를 위한 경량 런타임

#### 3. 참고 표준 및 기술
- **12-Factor App**: 클라우드 네이티브 애플리케이션 설계 원칙
- **OpenAPI Specification**: API 계약 정의 표준
- **Cloud Native Computing Foundation (CNCF)**: 클라우드 네이티브 기술 표준화

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [API Gateway](@/studynotes/03_network/03_modern/api_gateway.md): MSA의 단일 진입점
- [Service Mesh (Istio)](@/studynotes/06_ict_convergence/02_devops/service_mesh.md): MSA 서비스 간 통신 인프라
- [Kubernetes](@/studynotes/06_ict_convergence/01_cloud/kubernetes.md): MSA 오케스트레이션 플랫폼
- [Saga Pattern](@/studynotes/07_enterprise_systems/02_data/saga_pattern.md): MSA 분산 트랜잭션 패턴
- [SOA (Service Oriented Architecture)](@/studynotes/07_enterprise_systems/02_data/soa.md): MSA의 전신

---

### 👶 어린이를 위한 3줄 비유 설명
1. MSA는 큰 레고 성을 작은 레고 조각들로 만드는 것과 같아요. 각 조각이 따로따로 만들어지고 바꿀 수 있어요.
2. 하나의 조각이 망가져도 다른 조각들은 그대로 있을 수 있고, 필요한 조각만 더 많이 만들어서 큰 성을 쉽게 키울 수 있어요.
3. 이렇게 하면 어떤 부분이 문제가 생겨도 전체 성이 무너지지 않고, 새로운 모양도 쉽게 만들 수 있답니다!
