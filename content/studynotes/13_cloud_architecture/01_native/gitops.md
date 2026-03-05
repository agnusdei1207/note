+++
title = "GitOps (깃옵스)"
date = 2026-03-05
description = "Git을 단일 진실 공급원(Single Source of Truth)으로 삼아 인프라와 애플리케이션의 선언적 상태를 관리하고 자동 동기화하는 운영 모델 심층 분석"
weight = 167
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["GitOps", "ArgoCD", "Flux", "Declarative", "Infrastructure-as-Code", "Pull-Based-Deployment"]
+++

# GitOps (깃옵스) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: GitOps는 Git 저장소를 인프라와 애플리케이션의 **단일 진실 공급원(Single Source of Truth)**으로 삼고, 선언적(Declarative) 매니페스트의 변경을 자동으로 클러스터에 동기화하는 **풀(Pull) 기반 배포 운영 모델**입니다.
> 2. **가치**: 배포 보안성 강화(**Git을 통한 승인 워크플로우**), 감사 추적(**Git 커밋 히스토리**), 재해 복구(**Git 복원으로 전체 인프라 재구축**), 개발자 경험 향상(**PR 기반 인프라 변경**)을 실현합니다.
> 3. **융합**: 쿠버네티스(K8s), IaC(Terraform), CI/CD(GitHub Actions), Policy-as-Code(OPA), Secret Management(Vault)와 결합하여 완전한 선언적 인프라 파이프라인을 구축합니다.

---

## Ⅰ. 개요 (Context & Background)

GitOps는 2017년 Weaveworks가 처음 제안한 개념으로, DevOps의 발전된 형태입니다. 기존 CI/CD는 외부 시스템(Jenkins, GitHub Actions)이 클러스터에 푸시(Push) 방식으로 배포했습니다. 반면 GitOps는 클러스터 내부의 에이전트(ArgoCD, Flux)가 Git 저장소를 풀(Pull)하여 상태를 동기화합니다. 이 차이는 보안성, 감사 추적, 재현성 측면에서 혁신적입니다.

**💡 비유**: GitOps는 **'자동 업데이트 되는 법전'**과 같습니다. 법관(클러스터)은 법전(Git 저장소)만 참조하여 판단합니다. 법전이 개정되면(PR 병합), 모든 법관의 판례(클러스터 상태)가 자동으로 새 법에 맞춰집니다. 법전 외의 어떤 임의 지시도 받지 않습니다.

**등장 배경 및 발전 과정**:
1. **CI/CD의 한계**: 푸시 기반 배포는 CI 시스템이 클러스터의 관리자 권한을 가지므로, CI 시스템이 탈취되면 클러스터 전체가 위험에 노출됩니다.
2. **쿠버네티스의 선언적 특성**: K8s는 "원하는 상태(Desired State)"를 선언하면 컨트롤러가 "현재 상태"와 일치시키는 구조입니다. GitOps는 이 선언적 특성을 배포 프로세스까지 확장합니다.
3. **멀티 클러스터 관리**: 수십 개의 클러스터를 일관되게 관리하려면 중앙 집중식 구성 저장소가 필요합니다. Git이 자연스러운 선택이 되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### GitOps 4대 원칙

| 원칙 | 설명 | 이점 |
|---|---|---|
| **선언적 (Declarative)** | 시스템 상태를 YAML/JSON으로 선언 | 버전 관리, 검증 가능 |
| **버전화 (Versioned)** | Git 커밋으로 상태 버전화 | 롤백, 감사 추적 |
| **자동화 (Automated)** | Git 변경 시 자동 배포 | 일관성, 속도 |
| **지속적 조정 (Continuous Reconciliation)** | 주기적으로 상태 비교 및 수정 | 드리프트 감지, 자동 복구 |

### GitOps 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 대표 도구 | 특성 |
|---|---|---|---|
| **Git Repository** | 선언적 매니페스트 저장소 | GitHub, GitLab, Bitbucket | 버전 관리, PR 워크플로우 |
| **GitOps Operator** | Git 상태 감시 및 동기화 | ArgoCD, Flux, Raven | 클러스터 내부 실행 |
| **Manifest Store** | K8s 리소스 정의 파일 | Kustomize, Helm, Jsonnet | 템플릿, 오버레이 |
| **Sync Engine** | Git ↔ Cluster 상태 동기화 | Reconcile Loop | 3-way diff, 자동/수동 |
| **Secret Management** | 민감 정보 주입 | Sealed Secrets, Vault, SOPS | 암호화, 외부 주입 |
| **Policy Engine** | 배포 전 정책 검증 | OPA Gatekeeper, Kyverno | 컴플라이언스, 보안 |

### 정교한 구조 다이어그램: GitOps 아키텍처

```ascii
================================================================================
                         GITOPS ARCHITECTURE (ArgoCD)
================================================================================

                    +-----------------------------------+
                    |        Developer Workstation      |
                    |  +--------+  +--------+  +------+ |
                    |  | IDE    |  | CLI    |  | Web  | |
                    |  +---+----+  +---+----+  +--+---+ |
                    +------|-----------|-----------|-----+
                           |           |           |
                           v           v           v
                    +-----------------------------------+
                    |         Git Repository            |
                    |  (Single Source of Truth)         |
                    |                                   |
                    |  +-----------------------------+  |
                    |  | apps/                       |  |
                    |  |  +-- production/            |  |
                    |  |  |   +-- kustomization.yaml |  |
                    |  |  |   +-- deployment.yaml    |  |
                    |  |  +-- staging/               |  |
                    |  |      +-- kustomization.yaml |  |
                    |  +-----------------------------+  |
                    |                                   |
                    |  +-----------------------------+  |
                    |  | infrastructure/             |  |
                    |  |  +-- terraform/             |  |
                    |  |  +-- helm-charts/           |  |
                    |  +-----------------------------+  |
                    |                                   |
                    |  Commits: abc123, def456, ...     |
                    +-----------------+-----------------+
                                      |
                                      | git clone + watch
                                      v
    +-------------------------------------------------------------------------+
    |                     KUBERNETES CLUSTER                                   |
    |                                                                          |
    |   +-------------------------------------------------------------------+  |
    |   |                    argocd namespace                               |  |
    |   |                                                                   |  |
    |   |   +---------------------------+   +---------------------------+   |  |
    |   |   |      ArgoCD Repo Server   |   |     ArgoCD Application    |   |  |
    |   |   |   (Git clone, manifest)   |   |        Controller         |   |  |
    |   |   +------------+--------------+   +-------------+-------------+   |  |
    |   |                |                              |                  |  |
    |   |                v                              v                  |  |
    |   |   +---------------------------+   +---------------------------+   |  |
    |   |   |    ArgoCD API Server      |   |    ArgoCD Redis (Cache)   |   |  |
    |   |   |    (UI, CLI, API)         |   |                           |   |  |
    |   |   +------------+--------------+   +---------------------------+   |  |
    |   |                |                                                     |  |
    |   +----------------+-----------------------------------------------------+  |
    |                    |                                                        |
    |                    | Sync (Create/Update/Delete K8s Resources)             |
    |                    v                                                        |
    |   +-------------------------------------------------------------------+    |
    |   |                     production namespace                          |    |
    |   |                                                                   |    |
    |   |   +------------+  +------------+  +------------+  +------------+  |    |
    |   |   | Deployment |  | Service    |  | ConfigMap  |  | Ingress    |  |    |
    |   |   | (v2.0.0)   |  | (ClusterIP)|  | (app-config)| | (nginx)   |  |    |
    |   |   +-----+------+  +-----+------+  +-----+------+  +-----+------+  |    |
    |   |         |               |               |               |          |    |
    |   |   +-----v------+  +-----v------+        |               |          |    |
    |   |   |   Pod      |  |  Endpoint  |        |               |          |    |
    |   |   | (app:8080) |  |            |        |               |          |    |
    |   |   +------------+  +------------+        |               |          |    |
    |   |                                         |               |          |    |
    |   +-----------------------------------------+---------------+----------+    |
    |                                                                          |
    +-------------------------------------------------------------------------+

================================================================================
                    PUSH vs PULL DEPLOYMENT
================================================================================

[Push-Based CI/CD (Traditional)]

    Developer --> Git --> CI Server (Jenkins) --push--> Kubernetes Cluster
                                   |                        |
                                   | Needs cluster-admin    |
                                   | credentials (kubeconfig)|
                                   |                        |
                                   v                        v
                            Security Risk            Single Point of Failure


[Pull-Based GitOps (ArgoCD/Flux)]

    Developer --> Git <--pull-- ArgoCD (inside cluster) --> Kubernetes API
                                   |
                                   | No external credentials needed
                                   | Runs inside cluster (in-cluster auth)
                                   |
                                   v
                            Secure by Default

================================================================================
                    SYNC STATUS & DRIFT DETECTION
================================================================================

                    Git (Desired State)     Cluster (Live State)
                    ===================     =====================
                    deployment.yaml         Deployment resource
                    replicas: 3             replicas: 2 (MANUALLY SCALED!)
                    image: v2.0.0           image: v2.0.0

                           |                          |
                           +------------+-------------+
                                        |
                                        v
                              +------------------+
                              |   ArgoCD Sync    |
                              |   Engine         |
                              |                  |
                              | 3-Way Diff:      |
                              | Git | Live | Last|
                              |                  |
                              | Result: DRIFT    |
                              | DETECTED!        |
                              +--------+---------+
                                       |
                                       v
                              +------------------+
                              | Auto-Sync ON:    |
                              | --> Reconcile    |
                              | --> Scale to 3   |
                              |                  |
                              | Auto-Sync OFF:   |
                              | --> Alert only   |
                              +------------------+
```

### 심층 동작 원리: 3-Way Diff와 Reconciliation

ArgoCD는 Git 상태, 클러스터 실제 상태, 마지막 동기화 상태의 3가지를 비교합니다.

1. **Synced**: Git 상태와 클러스터 상태가 일치
2. **OutOfSync**: Git 상태와 클러스터 상태가 불일치
3. **Unknown**: 상태 확인 불가 (오류)

**동기화 모드**:

| 모드 | 동작 | 사용 사례 |
|---|---|---|
| **Manual** | 수동으로 Sync 버튼 클릭 | 프로덕션 환경 |
| **Auto** | Git 변경 시 자동 동기화 | 개발/스테이징 |
| **Prune** | Git에서 삭제된 리소스를 클러스터에서도 삭제 | 환경 정리 |
| **Self-Heal** | 수동 변경 감지 시 자동 복구 | 보안 강화 |

### 핵심 코드: ArgoCD Application 매니페스트

```yaml
# ArgoCD Application 정의
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app-production
  namespace: argocd
  # Self-Heal: 수동 변경 자동 복구
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  # Git 저장소 설정
  project: default

  source:
    repoURL: https://github.com/myorg/my-app-gitops.git
    targetRevision: main  # Git 브랜치/태그/커밋
    path: apps/production  # 매니페스트 경로

    # Helm 값 오버라이드
    helm:
      valueFiles:
        - values-production.yaml
      parameters:
        - name: image.tag
          value: "v2.0.0"

    # 또는 Kustomize 사용
    # kustomize:
    #   namePrefix: prod-

  # 배포 대상 클러스터
  destination:
    server: https://kubernetes.default.svc  # 동일 클러스터
    namespace: production

  # 동기화 정책
  syncPolicy:
    # 자동 동기화
    automated:
      prune: true      # Git에서 삭제된 리소스 제거
      selfHeal: true   # 수동 변경 자동 복구

    # 동기화 옵션
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true  # 마지막에 삭제 수행

    # 재시도 정책
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

  # 상태 무시 설정 (annotation으로 마킹된 필드)
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas  # HPA가 관리하므로 무시

---
# ApplicationSet - 멀티 클러스터/환경 자동 생성
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: my-app-multi-env
  namespace: argocd
spec:
  generators:
  - list:
      elements:
        - env: staging
          namespace: staging
          revision: develop
        - env: production
          namespace: production
          revision: main
  template:
    metadata:
      name: 'my-app-{{env}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/my-app-gitops.git
        targetRevision: '{{revision}}'
        path: apps/base
        kustomize:
          namePrefix: '{{env}}-'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{namespace}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

### Secret 관리: Sealed Secrets

Git에 Secret을 평문으로 저장할 수 없습니다. Sealed Secrets는 공개키로 암호화하여 Git에 저장하고, 클러스터 내부에서 비공개키로 복호화합니다.

```yaml
# 암호화된 Secret (Git에 저장)
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: my-app-secret
  namespace: production
spec:
  encryptedData:
    # 공개키로 암호화된 데이터
    database-password: AgBfH8j2...
    api-key: AgCdF9k3...
  template:
    metadata:
      name: my-app-secret
    type: Opaque
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: ArgoCD vs Flux

| 비교 항목 | ArgoCD | Flux |
|---|---|---|
| **UI** | 풍부한 웹 UI | CLI 중심 (Weave GitOps UI 선택적) |
| **아키텍처** | 중앙 집중식 (단일 컨트롤러) | 분산식 (컨트롤러 분리) |
| **멀티 테넌시** | Projects로 격리 | Tenant API |
| **롤백** | UI/CLI에서 쉬운 롤백 | Git revert 필요 |
| **Helm 지원** | Helm + Kustomize + Jsonnet | Helm + Kustomize |
| **학습 곡선** | 낮음 (UI 친화적) | 중간 (CLI 중심) |
| **CNCF 상태** | Graduated | Graduated |

### 과목 융합 관점 분석: 보안 및 운영 연계

- **보안(Security)와의 융합**: GitOps는 **최소 권한 원칙(Least Privilege)**을 강화합니다. 개발자는 Git에 PR을 올리고, 승인자가 병합하면 배포됩니다. CI 시스템은 클러스터 자격 증명을 가질 필요가 없습니다. 또한 **OPA Gatekeeper**와 결합하여 Git에 커밋된 매니페스트가 정책(예: root 컨테이너 금지)을 위반하면 동기화를 차단할 수 있습니다.

- **운영(Operations)과의 융합**: GitOps의 **드리프트 탐지(Drift Detection)**는 누군가 `kubectl edit`으로 클러스터를 수동 변경했을 때 자동으로 감지하고 복구합니다. 이는 구성 편류(Configuration Drift)를 방지하여 '인프라 코드화(IaC)'의 일관성을 보장합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 멀티 클러스터 금융 서비스

**문제 상황**: 3개 리전(AP, US, EU)에 분산된 12개 클러스터에서 결제 서비스를 운영합니다. 각 클러스터의 구성이 서로 달라 장애 원인 파악이 어렵습니다.

**기술사의 전략적 의사결정**:

1. **중앙 집중식 GitOps Hub 구축**:
   - 단일 Git 저장소에 모든 클러스터 구성 저장
   - ArgoCD ApplicationSet으로 12개 클러스터 자동 관리

2. **환경별 오버레이 구조**:
   ```
   apps/
   ├── base/              # 공통 구성
   │   ├── deployment.yaml
   │   └── kustomization.yaml
   └── overlays/
       ├── ap-prod/       # AP 리전 프로덕션
       ├── us-prod/       # US 리전 프로덕션
       └── eu-prod/       # EU 리전 프로덕션
   ```

3. **승인 워크플로우**:
   - 개발자 PR → 코드 리뷰 → 보안 팀 승인 → SRE 병합
   - 프로덕션은 수동 Sync (Auto-Sync 비활성화)

4. **감사 로그**:
   - 모든 변경은 Git 커밋으로 추적
   - ArgoCD Audit Log와 연동

### 도입 시 고려사항 체크리스트

- **기술적 고려사항**:
  - [ ] Git 저장소 구조 설계 (Monorepo vs Polyrepo)
  - [ ] Secret 관리 전략 (Sealed Secrets, Vault, SOPS)
  - [ ] 멀티 클러스터 관리 (Hub-Spoke vs Federated)
  - [ ] 롤백 전략 (Git revert vs ArgoCD rollback)

- **운영/보안적 고려사항**:
  - [ ] Git 접근 권한 관리 (RBAC)
  - [ ] PR 승인 정책 (Branch Protection)
  - [ ] Secret 회전 (Rotation) 자동화
  - [ ] 재해 복구 (Git 복원, ArgoCD 백업)

### 안티패턴 (Anti-patterns)

1. **Git에 민감 정보 평문 저장**: Secret을 평문으로 커밋하면 유출 시 복구 불가능합니다. 반드시 Sealed Secrets 또는 External Secrets를 사용해야 합니다.

2. **Auto-Sync를 프로덕션에 무조건 적용**: 잘못된 커밋이 자동으로 프로덕션에 배포될 수 있습니다. 프로덕션은 수동 Sync 또는 승인 게이트를 사용해야 합니다.

3. **단일 거대 Application**: 모든 리소스를 하나의 Application에 넣으면 부분 롤백이 불가능합니다. Micro-Application 구조로 분리해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 전통 CI/CD | GitOps | 개선율 |
|---|---|---|---|
| **배포 보안성** | 중간 (CI 자격증명 노출) | 높음 (클러스터 내부) | 보안 강화 |
| **롤백 시간** | 5~30분 | 1분 이내 | 90% 단축 |
| **감사 추적** | 별도 로그 필요 | Git 히스토리 | 100% 커버리지 |
| **드리프트 감지** | 수동 | 자동 | 실시간 |
| **개발자 경험** | 낮음 (YAML 복잡) | 높음 (PR 기반) | 생산성 향상 |
| **멀티 클러스터** | 복잡 | 단순 | 운영 효율화 |

### 미래 전망 및 진화 방향

1. **Progressive Delivery GitOps**: Argo Rollouts + GitOps로 카나리 배포를 Git PR 기반으로 관리하는 패턴이 확산되고 있습니다.

2. **Platform Engineering**: Backstage와 같은 Internal Developer Portal(IDP)이 GitOps 백엔드와 통합되어, 개발자가 UI에서 인프라를 프로비저닝하면 자동으로 Git에 커밋됩니다.

3. **Policy-as-Code 통합**: OPA, Kyverno가 GitOps 파이프라인에 내장되어, 정책 위반 매니페스트가 Git에 커밋되는 것을 사전 차단합니다.

### ※ 참고 표준/가이드

- **OpenGitOps**: CNCF의 GitOps 표준 정의
- **ArgoCD Documentation**: ArgoCD 공식 문서
- **Flux Documentation**: Flux 공식 문서

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [CI/CD 파이프라인](@/studynotes/13_cloud_architecture/01_native/ci_cd.md) : GitOps와 연동되는 지속적 통합
- [IaC (Infrastructure as Code)](@/studynotes/13_cloud_architecture/01_native/ci_cd.md) : GitOps의 기반 기술
- [쿠버네티스](@/studynotes/13_cloud_architecture/01_native/kubernetes.md) : GitOps의 주요 대상 플랫폼
- [무중단 배포](@/studynotes/13_cloud_architecture/01_native/deployment_strategies.md) : GitOps로 구현하는 배포 전략
- [SRE](@/studynotes/13_cloud_architecture/01_native/sre.md) : GitOps를 활용하는 사이트 신뢰성 공학

---

### 👶 어린이를 위한 3줄 비유 설명
1. GitOps는 **'자동으로 갱신되는 요리책'**과 같아요. 요리책(Git)에 새 레시피가 추가되면, 모든 요리사(ArgoCD)가 자동으로 새 레시피를 따라요.
2. 누가 요리책을 몰래 수정해도, 원래 레시피와 다르면 자동으로 바로잡아요 (Self-Heal).
3. 덕분에 요리사는 요리책만 보면 되고, 어떤 레시피가 언제 바뀌었는지도 모두 기록돼 있어요!
