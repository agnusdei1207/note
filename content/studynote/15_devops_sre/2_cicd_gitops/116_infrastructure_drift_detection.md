+++
weight = 116
title = "인프라 구성 편류 (Infrastructure Drift) 및 탐지 자동화"
date = "2024-03-24"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
- **정상 상태와의 불일치:** 코드(IaC)로 정의된 목표 상태와 실제 클라우드 인프라의 현재 상태가 수동 조작 등에 의해 서로 달라지는 현상.
- **보안 및 장애 리스크:** 드리프트가 방치되면 인프라의 가시성이 사라지고, 다음 배포 시 예기치 않은 리소스 삭제나 설정 오류로 인한 장애 발생.
- **지속적 감시(Continuous Auditing):** 정기적으로 `terraform plan`을 실행하거나 AWS Config 등의 도구를 활용해 드리프트를 탐지하고 자동 복구(Remediation) 수행.

### Ⅰ. 개요 (Context & Background)
인프라를 코드로 관리(IaC)하더라도, 장애 대응 등의 긴급 상황에서 엔지니어가 클라우드 콘솔에 직접 접속해 보안 그룹을 열거나 인스턴스 사양을 변경하는 경우가 발생합니다. 이렇게 코드와 실제 환경의 싱크가 깨지는 것을 '드리프트(Drift)'라고 합니다. 드리프트는 인프라의 신뢰성을 무너뜨리고 불필요한 비용 발생 및 보안 취약점을 야기하므로, 이를 조기에 탐지하고 코드로 환원하는 것이 현대 데브옵스의 핵심 과제입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
드리프트 탐지는 '선언적 코드(Desired)'와 '실제 상태(Actual)'를 비교하는 루프(Loop)를 통해 이루어집니다.

```text
[ Infrastructure Drift Detection Loop ]

    (Desired State)        (Drift Detection)        (Actual State)
   +---------------+      +-----------------+      +----------------+
   | IaC Code      | <--> | Difference      | <--> | Live Cloud     |
   | (Terraform/HCL)|      | Identification  |      | (AWS/GCP/K8s)  |
   +---------------+      +-----------------+      +----------------+
                                   |
                         [ Drift Detected!! ]
                                   |
                  +----------------------------------+
                  | 1. Alert (SRE Notification)      |
                  | 2. Re-apply (Auto-Healing)       |
                  | 3. Import (Update Code to Live)  |
                  +----------------------------------+

[ Key Mechanisms ]
1. Periodic Scanning: 스케줄링된 작업을 통해 현재 클라우드 API를 호출하여 상태 수집.
2. State Comparison: 저장된 `.tfstate` 파일과 실제 리소스를 1:1 대조.
3. Out-of-Band Change tracking: IaC 툴 외부에서 발생한 API 이벤트를 추적(CloudTrail 등).
```

**핵심 원리:**
1. **멱등성 보장:** IaC의 멱등성을 활용하여 현재 상태를 목표 상태로 강제 수렴(Reconciliation)시킴으로써 드리프트 해결.
2. **가시성(Visibility):** 어떤 속성(예: CPU 크기, Inbound IP)이 구체적으로 바뀌었는지 Diff 형태로 리포팅.
3. **규정 준수(Compliance):** 보안 정책에 위배되는 드리프트 발생 시 즉시 차단하거나 알림 발송.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 수동 드리프트 탐지 | 테라폼 기반 탐지 (CLI) | 전용 솔루션 (Cloud-Native) |
| :--- | :--- | :--- | :--- |
| **탐지 방식** | 육안 확인 / 콘솔 비교 | `terraform plan` 실행 | AWS Config / GCP Security Health |
| **자동화 수준** | 낮음 (비정기적) | 중간 (CI/CD 파이프라인) | 높음 (실시간 이벤트 기반) |
| **복구 방식** | 수동 원복 | `terraform apply` 재실행 | 자동 교정 (Auto-remediation) |
| **확장성** | 매우 낮음 | 프로젝트 단위 한계 | 전사적 리소스 통제 가능 |
| **추천 대상** | 소규모 환경 | 일반적인 DevOps 팀 | 대규모 엔터프라이즈 / 금융권 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **실무 적용:** 주기적으로(예: 1시간마다) GitHub Actions나 Jenkins를 통해 `terraform plan -detailed-exitcode`를 실행하여, 변경 사항이 감지되면 슬랙(Slack)으로 "드리프트 발생" 알림을 보내는 체계를 구축할 수 있습니다.
- **기술사적 판단:** 모든 드리프트를 무조건 코드로 강제 원복하는 것은 위험할 수 있습니다. 기술사는 긴급 장애 조치로 인한 '의도된 드리프트'인지 판단할 수 있는 프로세스를 수립하고, 정기적으로 실제 인프라 상태를 코드로 역추적하여 반영하는 'Reverse-IaC' 전략을 병행해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
드리프트 탐지는 '불변 인프라(Immutable Infrastructure)' 사상을 완성하는 마지막 퍼즐입니다. 향후 인공지능(AI)이 드리프트의 원인을 분석하여 단순 실수인지 침해 사고인지 구분하고, 스스로 최적의 복구 경로를 제안하는 지능형 인프라 거버넌스 시대로 발전할 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Infrastructure as Code (IaC), Configuration Management
- **하위 개념:** Desired State, Actual State, Reconciliation Loop
- **연관 기술:** Terraform, Pulumi, AWS Config, Driftctl, Crossplane

### 👶 어린이를 위한 3줄 비유 설명
1. 레고 설계도(코드)대로 멋진 성을 쌓아뒀는데, 누군가 몰래 레고 블록 하나를 빼거나 색깔을 바꿨어요.
2. 로봇(탐지 도구)이 설계도랑 실제 성을 매일매일 비교해서 "어? 여기가 설계도랑 달라요!"라고 알려주는 거예요.
3. 그래야 나중에 성을 더 크게 지을 때 실수하지 않고 튼튼하게 지을 수 있답니다.
