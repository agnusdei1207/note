+++
weight = 102
title = "에어 갭 (Air-gapped) 환경의 CI/CD: 폐쇄망 배포 전략"
date = "2026-03-04"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
- 외부 인터넷 연결이 완전히 차단된 '에어 갭(Air-gapped)' 환경을 위한 특수 CI/CD 파이프라인 전략임.
- 소스코드, 의존성 라이브러리, 컨테이너 이미지를 타르볼(Tarball)로 패키징하여 오프라인으로 반입함.
- 보안 등급이 높은 공공, 금융, 국방 분야에서 데이터 유출 방지와 시스템 무결성을 위해 필수적임.

### Ⅰ. 개요 (Context & Background)
일반적인 CI/CD 환경은 GitHub나 Docker Hub와 같은 클라우드 서비스에 실시간으로 접근한다. 그러나 국가 안보, 금융 핵심 망, 원자력 발전소와 같은 **폐쇄망(Air-gapped)** 환경은 보안상의 이유로 외부 통신이 불가능하다. 이러한 제약 조건에서도 수동 배포의 인적 오류를 줄이고 개발 생산성을 유지하기 위해 오프라인 전송 기반의 CI/CD 아키텍처가 필요하다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ Air-gapped CI/CD Workflow (폐쇄망 배포 워크플로우) ]

[인터넷 망 (External)]           [물리적 격리 (Air-gap)]           [폐쇄 망 (Internal)]
+----------------------+       +-----------------------+       +------------------------+
| 1. Build & Package   |       | 2. Security Scan      |       | 3. Import & Deploy     |
| - Code Fetch         |       | - Vexation / Malware  |       | - Load Tarballs        |
| - Library Mirroring  | ----> | - Approval Gate       | ----> | - Internal Registry    |
| - Container Bake     |       | - Physical Media/Data |       | - GitOps Sync          |
| - Save as .tar.gz    |       |   Diode (일방향 전송) |       | - K8s / VM Rollout     |
+----------------------+       +-----------------------+       +------------------------+

* Artifact Bundling: 모든 종속성(NPM, Maven, PyPI)을 포함한 "Self-contained" 패키지 생성
* Data Diode: 물리적으로 한 방향으로만 데이터가 흐르게 하는 보안 장비 활용
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | 클라우드 네이티브 CI/CD | 에어 갭 (Air-gapped) CI/CD |
| :--- | :--- | :--- |
| **연결성** | 상시 온라인, 클라우드 연동 | 오프라인, 단절된 망 |
| **의존성 관리** | 실시간 다운로드 (Dynamic) | 사전 미러링/패키징 (Static) |
| **보안성** | 네트워크 보안 (Firewall, VPN) | 물리적 격리 (Physical Air-gap) |
| **배포 속도** | 즉각적 (CI -> CD) | 반입 절차로 인한 지연 (Batch) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **베이스 이미지 전략**: 폐쇄망 내부용 골든 이미지(Golden Image) 저장소를 별도로 운영하고, 외부 반입 시에는 변경된 레이어만 전송하는 증분(Incremental) 업데이트 전략을 취해야 한다.
- **의존성 헬(Dependency Hell) 방지**: 패키징 시점에 벤더링(Vendoring) 도구를 사용하여 모든 라이브러리가 포함되었는지 무결성 검증을 수행해야 한다.
- **보안 거버넌스**: 반입 전 반드시 SCA(소프트웨어 구성 분석) 및 안티바이러스 스캔을 거쳐야 하며, 모든 반입 이력은 감사 로그(Audit Log)로 관리해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
에어 갭 CI/CD는 보안과 생산성 사이의 타협점이다. 향후 SBOM(소프트웨어 자재 명세서) 표준화와 연계되어 폐쇄망 내부로 반입되는 모든 구성 요소의 투명성을 확보하는 방향으로 진화할 것이다. 이는 '보안 환경에서도 애자일(Agile)이 가능하다'는 것을 증명하는 핵심 기술 역량이 된다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 폐쇄망 보안(Network Isolation), CI/CD
- **핵심 도구**: Skopeo (이미지 복제), Nexus/Artifactory (오프라인 미러), Data Diode
- **관련 기술**: SBOM, Golden Image, Artifact Repository

### 👶 어린이를 위한 3줄 비유 설명
1. 인터넷이 안 되는 섬나라에 새로운 게임을 보내주려는 상황이야.
2. 모든 내용물을 큰 가방(타르볼)에 담아서 배를 타고 직접 가서 전달해 줘야 해.
3. 섬에 도착하면 가방을 풀어서 섬나라 전용 게임기(폐쇄망 서버)에 설치하는 방식이야.
