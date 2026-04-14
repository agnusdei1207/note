+++
weight = 113
title = "AWS SAM (Serverless Application Model) 서버리스 모델"
date = "2024-05-22"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
- **AWS 네이티브 서버리스 IaC:** CloudFormation의 확장판으로, AWS 환경에 최적화된 서버리스 애플리케이션(Lambda, API Gateway, DynamoDB)을 선언적으로 정의함.
- **로컬 개발 환경 강화:** SAM CLI를 통해 로컬에서 Lambda 함수를 에뮬레이션(Docker 기반)하고, 실제 AWS 환경과 유사하게 디버깅할 수 있는 강력한 툴체인을 제공함.
- **점진적 배포 자동화:** AWS CodeDeploy와 연계하여 Linear, Canary 배포 등 고도화된 릴리스 전략을 `template.yaml` 설정만으로 손쉽게 구현함.

### Ⅰ. 개요 (Context & Background)
1. **CloudFormation의 복잡성 해결:** 순수 CloudFormation으로 서버리스를 정의하려면 수백 줄의 코드가 필요하지만, SAM은 '서버리스 전용 문법'을 통해 이를 획기적으로 단축함.
2. **개발-배포 일치:** 로컬 테스트부터 CI/CD 파이프라인 배포까지 일관된 환경을 유지하여 서버리스 애플리케이션의 신뢰성을 확보함.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **AWS SAM Components & Deployment Lifecycle**
```text
[ Developer Machine ]         [ AWS Cloud Infrastructure ]
+---------------------+        +-----------------------------------+
| template.yaml       |        | CloudFormation Service (Engine)   |
| (Transform: SAM)    | -----> | [ Resources ]                     |
+---------------------+        | - AWS::Serverless::Function       |
| SAM CLI (Local)     |        | - AWS::Serverless::Api            |
| (sam build/deploy)  |        | - AWS::Serverless::SimpleTable    |
+---------------------+        +-----------------------------------+
           |                             ^
           +--- (Upload to S3) ----------+
```

1. **Transform 선언:**
   - `Transform: AWS::Serverless-2016-10-31` 구문을 통해 CloudFormation에 SAM 문법임을 알리며, 내부적으로 표준 CloudFormation 리소스로 확장(Expansion)됨.
2. **핵심 리소스 유형:**
   - `AWS::Serverless::Function`: 람다 함수 정의.
   - `AWS::Serverless::Api`: API 게이트웨이 및 라우팅 정의.
   - `AWS::Serverless::SimpleTable`: DynamoDB 테이블 생성(Primary Key 설정 등 단순화).
3. **SAM CLI 워크플로우:**
   - `sam init` (템플릿 생성) -> `sam build` (의존성 설치) -> `sam local invoke` (로컬 실행) -> `sam deploy` (클라우드 배포).

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | AWS SAM | CloudFormation (CFN) | Serverless Framework (SLS) |
| :--- | :--- | :--- | :--- |
| **태생/소속** | AWS 공식 오픈소스 | AWS 표준 IaC 서비스 | 서드파티 (Serverless Inc.) |
| **코드 가독성** | 매우 좋음 (간결) | 낮음 (장황) | 좋음 (추상화 높음) |
| **클라우드 범위** | AWS 전용 | AWS 전용 | 멀티 클라우드 가능 |
| **배포 전략** | CodeDeploy 기반 카나리 기본 지원 | 수동 구성 필요 | 플러그인 필요 |
| **로컬 디버깅** | SAM CLI (매우 강력) | 지원 안 함 | 플러그인 지원 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
1. **서버리스 CI/CD 파이프라인 (Strategy):**
   - SAM은 `sam pipeline init` 명령을 통해 Jenkins, GitLab, GitHub Actions용 CI/CD 구성을 자동으로 생성해주어, 데브옵스 환경 구축 속도를 획기적으로 높여줌.
2. **기술사적 판단:** AWS 환경에 완전히 정착한 프로젝트라면 서드파티 툴보다 SAM이 서비스 간 연동과 최신 기능 반영 속도 면에서 유리함. 특히 정책 템플릿(Policy Templates)을 사용하여 S3 Read, SNS Publish 등 흔한 권한을 한 줄로 정의할 수 있어 보안 설정 오류를 최소화함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
1. **기대효과:** 복잡한 인프라 코드를 줄여 유지보수성을 높이고, 로컬 테스트 환경을 통해 개발 주기를 단축하며 안정적인 배포 전략(Canary)을 내재화함.
2. **결론:** AWS SAM은 서버리스 개발의 표준 모델이며, 단순한 IaC 도구를 넘어 로컬 개발과 클라우드 배포를 잇는 완성도 높은 에코시스템임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** IaC (Infrastructure as Code), 서버리스
- **하위 개념:** CloudFormation, SAM CLI, CodeDeploy
- **연관 개념:** 서버리스 프레임워크, 람다 (Lambda), API 게이트웨이

### 👶 어린이를 위한 3줄 비유 설명
- **레고 만들기:** 설명서 없이 수천 개의 레고 조각을 하나하나 조립하는 게 기존 방식이라면,
- **AWS SAM:** "지붕", "벽", "문"이라는 큰 덩어리 조각을 미리 준비해줘서 뚝딱 집을 짓게 해주는 특별한 설명서예요.
- **결론:** 집을 짓기 전에 내 방 책상에서 미리 조립해보고(로컬 테스트), 마음에 들면 단번에 큰 마당(클라우드)으로 옮겨주는 편리한 도구랍니다.
