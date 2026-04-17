+++
title = "마이크로서비스 아키텍처 & 서버리스 심층 분석 (MSA & Serverless Deep Dive)"
weight = 1
description = "현대적 애플리케이션 아키텍처인 MSA와 Serverless의 핵심 원리, 패턴 및 융합 분석"
+++

## 핵심 인사이트 (3줄 요약)
- **MSA (Microservices Architecture)**: 비즈니스 도메인(Bounded Context) 단위로 분리되어 독립적 배포와 확장이 가능한 결합도가 낮은 서비스 집합.
- **서버리스 (Serverless)**: 인프라 프로비저닝 및 관리를 클라우드 제공자(CSP)에 위임하고, 실제 사용한 컴퓨팅 자원(실행 시간)에 대해서만 비용을 지불하는 FaaS(Function as a Service) 중심의 모델.
- **융합 모델 (Convergence)**: MSA의 각 서비스 요소를 컨테이너(CaaS) 또는 서버리스(FaaS) 기반으로 구성하여 트래픽 변동에 극도로 유연한 하이브리드 이벤트 기반 아키텍처 설계 가능.

### Ⅰ. 개요 (Context & Background)
마이크로서비스 아키텍처(MSA)는 거대한 모놀리식(Monolithic) 시스템을 작고 독립적인 서비스들로 쪼개어 개발 속도와 확장성을 높이는 설계 방식입니다. 각 서비스는 고유한 데이터베이스를 가지며 API를 통해 통신합니다.
서버리스(Serverless)는 애플리케이션 개발자가 서버의 존재를 의식하지 않고 비즈니스 로직(함수) 코드에만 집중할 수 있게 해주는 클라우드 컴퓨팅 실행 모델입니다. 이 둘은 결합되어 인프라 관리 부담이 최소화된 고효율/고탄력 시스템을 만듭니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
MSA 설계 원리와 서버리스 환경에서의 이벤트 주도 아키텍처(EDA)가 결합된 구조입니다.

```text
+-------------------------------------------------------------+
|                    Client / API Gateway                     |
+-------------------------------------------------------------+
          |                               |
    [ REST / gRPC ]                 [ Events / Async ]
          |                               |
+-------------------+           +-------------------+
|  MSA (Container)  |           |   MSA (Serverless)|
|                   |           |   (FaaS - Lambda) |
| +---------------+ |           | +---------------+ |
| | Order Service | |           | | Event Handler | |
| +---------------+ |           | +---------------+ |
|        |          |           |        |          |
| [ Order DB ]      |           | [ Event Queue ]   |
+-------------------+           +-------------------+
          |                               |
          +---------- [ Event Bus / Message Broker ] ---------+
                                          |
                                +-------------------+
                                | Background Worker |
                                | (Notification)    |
                                +-------------------+
```

**핵심 패턴 (Core Patterns):**
1. **API Gateway 패턴**: 클라이언트의 모든 요청을 단일 진입점으로 받아 적절한 마이크로서비스로 라우팅.
2. **Database per Service**: 각 서비스는 자신만의 데이터베이스를 가져 독립성과 캡슐화를 보장. (Polyglot Persistence)
3. **Saga 패턴 / CQRS**: 분산 환경에서 데이터 정합성을 유지하기 위한 보상 트랜잭션 및 명령/조회 분리 패턴.
4. **FaaS (Function as a Service)**: 이벤트(HTTP, DB Trigger, Queue)가 발생할 때마다 짧은 시간 실행되고 사라지는 무상태(Stateless) 함수.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | 컨테이너 기반 MSA (Container CaaS) | 서버리스 기반 MSA (Serverless FaaS) |
| :--- | :--- | :--- |
| **운영 체제 (Control)** | OS, 런타임 환경에 대한 제어권이 있음 | 인프라 제어 불가 (CSP 종속) |
| **과금 모델 (Cost)** | 프로비저닝된 인스턴스 시간/자원에 비례 | 호출 횟수 및 실행 시간(밀리초)에 비례 (Zero-scale) |
| **초기 구동 (Start-up)** | 항상 실행 중 (Cold Start 이슈 없음) | 첫 호출 시 지연 발생 가능성 (Cold Start) |
| **실행 시간 (Duration)** | 긴 실행 시간의 배치 및 백그라운드 작업 적합 | 보통 짧은 실행 시간 제한 (예: 15분) |
| **상태 관리 (State)** | 상태 저장이 비교적 용이 (Stateful 구성 가능) | 완전한 Stateless (상태는 외부 저장소 이용) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **전략적 적용 가이드**:
  * 예측 가능한 트래픽과 무거운 로직을 처리하는 핵심 도메인은 컨테이너(EKS, ECS 등) 기반의 MSA로 구성.
  * 간헐적이거나 스파이크(Spike)성 트래픽, 이벤트 트리거 방식의 백그라운드 작업(이미지 리사이징, 알림 발송 등)은 서버리스(AWS Lambda 등)로 구성하는 **하이브리드 접근법** 권장.
* **아키텍처 설계 시 주의점**:
  * 마이크로서비스 간의 과도한 동기식 통신은 지연(Latency) 증가 및 연쇄 장애(Cascading Failure)를 유발하므로, **메시지 큐(Kafka, RabbitMQ)를 활용한 비동기 이벤트 기반 통신(Event-driven)**을 지향해야 함.
  * 서버리스 환경에서는 분산 추적(Distributed Tracing)이 매우 까다로우므로 AWS X-Ray, Datadog 등의 전문 도구 통합 필수.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
MSA와 Serverless는 상호 배타적인 기술이 아니라, 애플리케이션의 성격에 맞춰 결합해야 할 상호 보완적인 아키텍처입니다. 
이를 통해 개발팀은 더 빠르고 민첩하게 기능을 배포할 수 있으며, 인프라 팀은 서버 운영 부담을 줄이고 비즈니스 가치 창출에 집중할 수 있습니다. 
궁극적으로는 모든 관리형 서비스들이 서버리스 형태로 진화하여(Serverless Container, Serverless Database), 진정한 NoOps와 극대화된 비용 효율성을 달성하는 표준이 될 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **아키텍처 패턴**: MSA, Serverless, Event-Driven Architecture (EDA), Hexagonal Architecture
* **데이터 관리**: Saga Pattern, Event Sourcing, CQRS, 2PC
* **배포 및 관리**: API Gateway, Service Mesh, CI/CD, FaaS, BaaS (Backend as a Service)

### 👶 어린이를 위한 3줄 비유 설명
1. 기존 시스템이 모든 요리를 혼자서 다 만드는 커다란 식당 주방이라면, MSA는 각자 피자 굽기, 파스타 만들기만 전담하는 여러 개의 작은 푸드트럭이 모인 거예요.
2. 여기서 컨테이너는 주방장이 항상 대기하고 있는 푸드트럭이고, 서버리스는 손님이 주문을 할 때만 뿅 나타나서 요리를 만들어주고 다시 사라지는 마법의 요리사예요.
3. 그래서 마법 요리사를 쓰면 손님이 없을 때는 월급을 안 줘도 돼서 돈을 아낄 수 있답니다!
