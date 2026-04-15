+++
weight = 112
title = "서버리스 프레임워크 (Serverless Framework) 람다 배포 추상화"
date = "2024-05-22"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
- **멀티 클라우드 추상화:** AWS Lambda, Google Cloud Functions, Azure Functions 등 다양한 서버리스 환경을 단일 설정 파일(`serverless.yml`)로 배포 관리함.
- **인프라 통합 관리:** 함수 코드뿐 아니라 API Gateway, S3, DynamoDB 등 연관 인프라 리소스(IaC)를 한 번에 프로비저닝하여 개발 생산성을 극대화함.
- **개발 워크플로우 최적화:** 로컬 테스트, 스테이징 배포, 롤백, 로그 모니터링을 CLI 명령어로 단순화하여 '코드 작성'에만 집중할 수 있는 환경을 제공함.

### Ⅰ. 개요 (Context & Background)
1. **서버리스의 관리 복잡성:** 클라우드 콘솔에서 수동으로 함수를 관리하는 방식은 버전 관리와 재현성(Reproducibility) 측면에서 한계가 명확함.
2. **IaC의 필요성:** 서버리스 애플리케이션은 수많은 이벤트 트리거와 리소스가 얽혀 있어, 이를 코드로 관리(Infrastructure as Code)하고 자동화하는 프레임워크가 필수적으로 요구됨.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **Serverless Framework Workflow & Deployment Architecture**
```text
[ Local Environment ]         [ Cloud Provider (e.g., AWS) ]
+---------------------+        +----------------------------+
| serverless.yml      |        | API Gateway (Endpoint)     |
| handler.py / js     | -----> | AWS Lambda (Logic)         |
+---------------------+        | CloudFormation (Stack)     |
           |                   | S3 / DynamoDB (Resources)  |
   $ sls deploy                +----------------------------+
           |
[ Provider Transformation ] (YAML to CloudFormation/Terraform)
```

1. **프로바이더 불가지론 (Provider Agnostic):**
   - 특정 클라우드 벤더의 API에 종속되지 않고 공통된 명세를 사용함. 배포 시 내부적으로 AWS CloudFormation 등으로 변환되어 실행됨.
2. **이벤트 드리븐 구조 (Event-driven):**
   - HTTP 호출, S3 파일 업로드, 일정 시간(Cron), DB 변경 등 다양한 이벤트를 함수와 맵핑하여 자동 실행되도록 설정함.
3. **플러그인 생태계:**
   - 로컬 시뮬레이션(`serverless-offline`), 도커 레이어 관리, 도메인 자동 연결 등 방대한 플러그인을 통해 기능을 무한 확장 가능함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 서버리스 프레임워크 (SLS) | AWS SAM (Serverless Application Model) | CDK / Terraform |
| :--- | :--- | :--- | :--- |
| **추상화 수준** | 매우 높음 (함수 중심) | 중간 (AWS 전용) | 낮음 (범용 인프라 중심) |
| **클라우드 지원** | 멀티 클라우드 (AWS, GCP, Azure 등) | AWS 전용 | 멀티 클라우드 |
| **주요 사용자** | 애플리케이션 개발자 | AWS 특화 개발자 | 인프라/플랫폼 엔지니어 |
| **테스트 도구** | 로컬 오프라인 플러그인 강력 | SAM CLI 활용 | 모킹(Mocking) 위주 |
| **설정 언어** | YAML (선언적) | YAML / JSON | TS, Python, Go 등 (프로그래밍) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
1. **콜드 스타트 및 리소스 제한 관리:**
   - 실무 배포 시 `warmup` 플러그인을 사용하여 함수를 예열하거나, 패키지 크기 최소화(Tree Shaking)를 통해 기동 시간을 단축하는 전략이 필수임.
2. **기술사적 판단:** 단순 API 개발에는 서버리스 프레임워크가 압도적이지만, 복잡한 인프라 의존성이 생길 경우 Terraform과 병행하여 관리하는 '하이브리드 IaC' 전략이 안정적임. 보안 측면에서 IAM Role의 최소 권한 원칙(Least Privilege)을 `serverless.yml`에 명시적으로 반영해야 함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
1. **기대효과:** 인프라 관리 비용(Ops)을 '0'에 가깝게 줄이고, 비즈니스 로직 배포 속도(Time-to-Market)를 극대화하여 초기 스타트업이나 이벤트성 서비스에 최적의 효율을 제공함.
2. **결론:** 서버리스 프레임워크는 개발자가 클라우드 환경의 복잡성을 몰라도 고성능 애플리케이션을 배포할 수 있게 해주는 '현대적 개발의 지렛대'임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 서버리스 (Serverless), FaaS (Function as a Service)
- **하위 개념:** 람다 (Lambda), API 게이트웨이 (API Gateway)
- **연관 개념:** AWS SAM, 클라우드포메이션 (CloudFormation), IaC

### 👶 어린이를 위한 3줄 비유 설명
- **직접 만들기:** 요리 재료를 사고, 불을 켜고, 그릇을 닦는 일을 내가 다 하는 거예요.
- **서버리스 프레임워크:** "파스타 1인분!"이라고 주문서만 쓰면, 주방에서 요리사가 알아서 만들어서 내주는 식당 시스템이에요.
- **결론:** 나는 "무슨 요리를 할지"만 생각하면 되고, 주방 청소나 불 관리는 프레임워크가 다 해주는 마법의 요리 도우미랍니다.
