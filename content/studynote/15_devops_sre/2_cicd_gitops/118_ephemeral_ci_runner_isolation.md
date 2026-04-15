+++
weight = 118
title = "CI 파이프라인 러너 (Runner) 인스턴스의 1회용 (Ephemeral) 격리 실행"
date = "2024-03-20"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
- **보안 강화:** 빌드 실행 후 인스턴스를 즉시 폐기하여 시크릿(API Key 등) 탈취 및 악성코드의 잔류(Persistence)를 원천 차단함.
- **빌드 무결성:** 이전 빌드의 잔류 파일(Cache, Node_modules 등)이 다음 빌드에 영향을 주지 않는 깨끗한 환경(Clean Slate)을 보장함.
- **자원 효율성:** 필요한 순간에만 컨테이너/VM을 생성하고 작업 완료 후 반납함으로써 클라우드 비용을 최적화함.

### Ⅰ. 개요 (Context & Background)
- **전통적 빌드 서버의 한계:** 공유형 빌드 서버(Shared Agent)는 보안에 취약하며, 특정 빌드에서 설치한 패키지가 다른 빌드와 충돌하는 '의존성 지옥'이 발생하기 쉬움.
- **Ephemeral Runner의 사상:** 11개 팩터 앱의 '폐기 가능성(Disposability)' 원칙을 CI 인프라에 적용한 것으로, 매 작업(Job)마다 독립된 격리 환경을 동적으로 할당받는 방식임.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **작동 메커니즘:** CI Orchestrator(GitHub Actions, GitLab)가 작업을 감지 -> API를 통해 K8s Pod 또는 VM 생성 -> 작업 수행 -> 자동 폐기(Destroy).
- **Bilingual ASCII Diagram:**
```text
[Ephemeral CI Runner Lifecycle / 1회용 CI 러너 생명주기]

    (1) Job Request       (2) Dynamic Spawning       (3) Isolated Execution
    [ CI Server ] ------> [ Runner Controller ] ----> [ New Container Pod ]
         ^                          |                          |
         |                          v                          v
    (5) Clean Up <------- [ Task Completed ] <------- [ Run Scripts/Tests ]
        (Destroy)           (Return Logs)             (Docker/Sandbox)

    * Isolation Level: Network / Disk / Memory Partitioning
    * Tool Examples: K8s-based Runner, AWS Fargate, GitHub-hosted Runner
```
- **핵심 기술:** 
  - **Auto-scaling:** 대량의 PR이 쏟아질 때 러너 대수를 자동으로 늘리는 기술 (ARC: Actions Runner Controller).
  - **Docker-in-Docker (DinD):** 격리된 러너 안에서 다시 도커 이미지를 빌드하기 위한 보안 소켓 바인딩 기술.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Criteria) | 고정형 러너 (Static/Self-hosted) | 1회용 러너 (Ephemeral/Container) |
| :--- | :--- | :--- |
| **보안 (Security)** | 낮음 (시크릿 잔류 위험) | 높음 (작업 후 완전 삭제) |
| **속도 (Performance)** | 빠름 (로컬 캐시 활용) | 보통 (인스턴스 기동 시간 필요) |
| **신뢰성 (Reliability)** | 낮음 (환경 오염 가능성) | 매우 높음 (멱등성 보장) |
| **유지보수 (Ops)** | 어려움 (서버 OS 패치 필요) | 쉬움 (이미지만 교체) |
| **비용 (Cost)** | 고정비 발생 | 사용한 만큼만 과금 (On-demand) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **기술사적 판단:** 현대의 공급망 보안(Supply Chain Security) 관점에서 고정형 서버를 운영하는 것은 매우 위험하며, 모든 엔터프라이즈 CI 환경은 **Ephemeral Runner** 기반으로 전환되어야 함.
- **최적화 전략:** 
  - **캐싱 활용:** 속도 저하를 막기 위해 S3나 분산 캐시 시스템을 연동하여 의존성 파일을 매번 새로 받지 않도록 구성.
  - **보안 강화:** 루트 권한이 없는(Rootless) 컨테이너에서 빌드되도록 설정하여 호스트 OS 탈취 위험을 방지.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **보안 인증 준수:** ISMS, SOC2 등 보안 표준 인증 시 빌드 환경의 격리 및 시크릿 관리 증빙을 강화함.
- **확장성 확보:** 클러스터 연동을 통해 수천 건의 빌드를 동시에 처리할 수 있는 무한 확장성 인프라를 구축함.
- **결론:** 1회용 러너는 이제 옵션이 아닌 필수 표준이며, 향후 WebAssembly(Wasm) 등을 활용한 더 가볍고 안전한 격리 기술로 진화할 것으로 예상됨.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Infrastructure as Code (IaC), Zero Trust Security
- **하위 개념:** Actions Runner Controller (ARC), Docker-in-Docker (DinD), Rootless Container
- **연관 기술:** Kubernetes, AWS Fargate, GitLab Runner, Supply Chain Attack

### 👶 어린이를 위한 3줄 비유 설명
1. **일회용 장갑 비유:** 요리할 때마다 새 장갑을 끼고, 요리가 끝나면 버리는 것과 같아요. 다른 음식의 냄새가 섞이지 않고 깨끗해요.
2. **호텔 방 비유:** 손님이 올 때마다 방을 깨끗하게 치워서 주는 것처럼, 매번 새롭고 깨끗한 방에서 일하는 것과 같아요.
3. **종이 비유:** 한 번 낙서하고 버리는 연습장 종이처럼, 뒷면에 흔적이 남지 않게 항상 새 종이를 쓰는 마법 같아요.
