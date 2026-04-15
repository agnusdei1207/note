+++
weight = 115
title = "아틀란티스 (Atlantis) 및 테라폼 Pull Request 자동화"
date = "2024-03-24"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
- **Git 기반 인프라 운영:** GitHub/GitLab의 Pull Request(PR) 댓글을 통해 테라폼(Terraform)을 실행하여 협업과 가시성을 극대화.
- **잠금(Locking) 메커니즘:** 여러 사람이 동시에 같은 리소스를 수정하지 못하도록 PR 단위로 테라폼 상태(State)를 보호.
- **가시성 확보:** 인프라 변경 사항(Plan 결과)을 PR 댓글로 즉시 확인하고 동료의 리뷰를 거친 후 배포(Apply)하는 완벽한 GitOps 워크플로우 구현.

### Ⅰ. 개요 (Context & Background)
인프라스트럭처 애즈 코드(IaC)를 로컬 PC에서 `terraform apply` 명령으로 직접 수행하면, 누가 어떤 변경을 했는지 추적하기 어렵고 동시에 같은 리소스를 건드려 장애가 발생할 위험이 큽니다. Atlantis는 IaC 운영을 Git PR 워크플로우에 통합하여, 모든 인프라 변경을 코드 리뷰 대상(Reviewable)으로 만들고 실행 결과까지 Git 기록으로 남기는 오픈소스 자동화 서버입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
Atlantis는 Git Webhook을 수신하여 중앙 집중식으로 테라폼을 제어합니다.

```text
[ Atlantis Workflow: Infrastructure via PR ]

   (Developer)          (GitHub/GitLab)             (Atlantis Server)
   -----------         -----------------          --------------------
   [ git push  ] ----> [ Pull Request  ]          [                    ]
                       [               ] --Webhook--> [ 1. plan        ]
                       [ PR Comment:   ] <---Result--- [ 2. State Lock  ]
   [ atlantis apply ] -> [ "apply" cmd ] --Webhook--> [ 3. apply       ]
                       [ PR Merged     ] <---Success-- [ 4. Unlock      ]
   -----------         -----------------          --------------------

[ Core Components ]
1. Webhook Listener: Git 플랫폼의 이벤트(PR 생성, 댓글 등) 수신.
2. Terraform Runner: 격리된 환경에서 테라폼 바이너리 실행.
3. PR Lock Manager: 특정 PR이 작업을 수행 중일 때 다른 PR의 수정을 방지.
4. UI Dashboard: 현재 실행 중인 잠금 및 작업 현황 시각화.
```

**핵심 원리:**
1. **중앙 집중형 실행:** 개발자 각자의 로컬 환경이 아닌, 권한이 제어된 Atlantis 서버에서만 인프라 변경이 일어나도록 통제.
2. **선형성 보장:** `atlantis plan` 결과를 팀원들이 확인하고 승인한 후에만 `apply`를 수행할 수 있는 강제 워크플로우(Gatekeeper) 구성.
3. **환경 분리:** `atlantis.yaml` 설정을 통해 개발, 운영 등 다양한 환경의 테라폼 프로젝트를 한 곳에서 관리.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 로컬 테라폼 실행 (Local CLI) | Atlantis (Git-based) | Terraform Cloud / Enterprise |
| :--- | :--- | :--- | :--- |
| **권한 관리** | 개인별 클라우드 자격증명 필요 | Atlantis 서버에만 권한 부여 | 중앙 집중식 권한 관리 |
| **잠금(Locking)** | `.tfstate` 파일 잠금에 의존 | PR 수준의 논리적 잠금 추가 | 관리형 상태 잠금 및 이력 |
| **가시성** | 실행자 본인만 확인 가능 | PR 댓글로 팀 전체가 확인 | 전용 대시보드 및 API 연동 |
| **자동화** | 수동 명령 (Manual) | Git Webhook 자동화 | 고도화된 CI/CD 통합 |
| **비용** | 무료 | 무료 (오픈소스) | 유료 (구독형) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **실무 적용:** `atlantis plan`을 실행하면 PR에 `terraform plan` 결과가 표 형태로 댓글이 달립니다. 이를 통해 보안 팀은 불필요한 포트 개방이 없는지, 비용 팀은 예상 비용 증가분이 합리적인지 PR 승인 전에 검토할 수 있습니다.
- **기술사적 판단:** Atlantis 도입 시 '보안 자격증명 관리'가 핵심입니다. 기술사는 Atlantis 서버가 탈취될 경우 전체 인프라가 위험해질 수 있음을 인지하고, IAM Role이나 HashiCorp Vault와의 연동을 통해 토큰 수명을 최소화하는 다중 방어 전략을 제시해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
Atlantis는 인프라 운영을 '소프트웨어 개발'과 동일한 수준의 엄격한 품질 관리(Review & CI) 프로세스에 올려놓습니다. 향후 테라폼뿐만 아니라 쿠버네티스 매니페스트와도 연동되는 더 넓은 의미의 GitOps 표준 도구로 자리매김할 것이며, 플랫폼 엔지니어링의 핵심 구성 요소가 될 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Infrastructure as Code (IaC), GitOps
- **하위 개념:** Pull Request Workflow, State Locking, Webhook
- **연관 기술:** Terraform, GitHub Actions, HashiCorp Vault, OPA

### 👶 어린이를 위한 3줄 비유 설명
1. 집을 지을 때 설계도(코드)를 고칠 때마다, 게시판(PR)에 "이렇게 고치려고 해요"라고 글을 남겨요.
2. 그럼 건축 로봇(Atlantis)이 "이렇게 고치면 비용이 이만큼 들어요"라고 댓글로 알려주고 다른 사람이 고치지 못하게 막아둬요.
3. 모두가 설계도를 보고 "좋아요!"라고 확인 버튼을 누르면 그제야 로봇이 실제로 공사를 시작한답니다.
