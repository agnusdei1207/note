+++
weight = 183
title = "클라우드 서비스 모델 개요 (IaaS, PaaS, SaaS Overview)"
date = "2024-03-20"
[extra]
categories = "ict-convergence"
+++

## 핵심 인사이트 (3줄 요약)
- **책임 공유 모델**: 서비스 모델(IaaS, PaaS, SaaS)에 따라 고객과 클라우드 제공자(CSP) 간의 관리 책임 범위가 명확히 구분됨.
- **추상화의 진화**: 인프라 하단부터 애플리케이션 상단까지 가상화 및 관리 대행 범위를 넓혀가며 개발 생산성을 극대화함.
- **비용 및 통제권의 트레이드오프**: 통제권이 클수록(IaaS) 관리 부담이 늘고, 추상화가 높을수록(SaaS) 신속한 도입이 가능함.

### Ⅰ. 개요 (Context & Background)
클라우드 서비스 모델은 제공되는 자원의 범위와 관리 주체에 따라 계층화된 아키텍처를 가진다. 기업은 비즈니스 목표에 따라 직접 하드웨어를 제어해야 하는지(IaaS), 개발 환경만 필요한지(PaaS), 혹은 완제품 소프트웨어를 바로 사용해야 하는지(SaaS)에 따라 최적의 모델을 선택해야 한다. 최근에는 서버리스(FaaS), 백엔드(BaaS) 등으로 더욱 세분화되고 있다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
각 서비스 모델은 피라미드 계층 구조를 가지며, 상위 모델일수록 사용자의 관리 영역이 줄어든다.

```text
[ Cloud Service Stack & Responsibility ]
+---------------------------------------+   --- Responsibility ---
|       SaaS (Software as a Service)    |   [ Provider ] (CSP)
|   (App, Data, Runtime, OS, Infra)     |   Fully Managed
+---------------------------------------+
|       PaaS (Platform as a Service)    |   [ Shared ]
|   (Runtime, Middleware, OS, Infra)    |   Apps/Data by User
+---------------------------------------+
|    IaaS (Infrastructure as a Service) |   [ User ]
|   (Virtualization, Servers, Storage)  |   OS/App by User
+---------------------------------------+
|       Physical Infrastructure         |   [ Provider ]
|   (Datacenter, Network, Cooling)      |   Hardware Level
+---------------------------------------+
```

1. **IaaS (Infrastructure)**: 가상 서버, 네트워크, 스토리지를 제공함. 사용자가 OS, 미들웨어, 런타임을 직접 설치 및 관리함.
2. **PaaS (Platform)**: 애플리케이션 개발/배포에 필요한 환경(Runtime, DB 등)을 제공함. 사용자는 코드와 데이터에만 집중함.
3. **SaaS (Software)**: 모든 스택이 공급자에 의해 관리되는 완제품 서비스. 사용자는 웹 브라우저나 앱을 통해 기능만 이용함.
4. **책임 공유 모델 (Shared Responsibility)**: 인프라 보안은 공급자가, 데이터 및 애플리케이션 보안은 사용자가 책임지는 구조.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | IaaS (Infrastructure) | PaaS (Platform) | SaaS (Software) |
| :--- | :--- | :--- | :--- |
| **핵심 자원** | 가상 머신 (VM) | 개발 엔진, 프레임워크 | 완제품 애플리케이션 |
| **제어권** | 매우 높음 (OS 레벨) | 중간 (App 레벨) | 낮음 (설정 레벨) |
| **주요 사용자** | 시스템 관리자, 아키텍트 | 개발자 | 일반 사용자, 현업 |
| **비용 효율** | 유연한 리소스 조정 | 인건비/관리비 절감 | 초기 구축비 없음 |
| **예시** | AWS EC2, Azure VM | Google App Engine, Heroku | Salesforce, Slack, Gmail |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **기술사적 판단**: 단순한 비용 절감보다는 'Time-to-Market' 관점에서 모델을 선정해야 한다. 신규 서비스의 빠른 검증이 목표라면 PaaS/SaaS가 유리하고, 기존 레거시 시스템의 복잡한 커스터마이징이 필요하다면 IaaS 기반의 Rehosting이 적합하다.
- **실무 전략**: **Multi-Model 접근**이 권장된다. 핵심 비즈니스 로직은 PaaS/MSA로, 범용 업무(메일, 협업)는 SaaS로, 대규모 연산이 필요한 데이터베이스는 IaaS나 전용 서비스로 분산 배치하여 최적화한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
서비스 모델은 점차 사용자 중심의 고수준 추상화(Abstraction)로 진화하고 있다. 서버리스(Serverless)와 FaaS의 확산은 인프라에 대한 고민을 완전히 제거하고 있으며, 향후에는 산업별 특화 클라우드(Industry Cloud) 형태의 SaaS가 더욱 강화될 것이다. 결론적으로 적재적소의 서비스 모델 선택이 기업의 IT 경쟁력을 좌우한다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: Cloud Computing, Service Taxonomy
- **연관 기술**: IaaS, PaaS, SaaS, FaaS, BaaS
- **확장 개념**: Shared Responsibility Model, Serverless, Cloud Native

### 👶 어린이를 위한 3줄 비유 설명
1. IaaS는 요리 재료와 주방 기구만 빌려주는 거예요 (내가 직접 요리하고 설거지함).
2. PaaS는 밀키트(반조리 식품)처럼 재료가 다 손질되어 있어서 끓이기만 하면 돼요.
3. SaaS는 맛있는 음식이 다 차려진 식당에 가서 맛있게 먹기만 하면 되는 거랍니다.
