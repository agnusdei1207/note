+++
title = "지속적 전달/배포 (CD, Continuous Delivery/Deployment)"
description = "CI를 통과한 코드를 프로덕션에 자동으로 배포하는 실천법에 대한 심층 기술 백서"
date = 2024-05-15
[taxonomies]
tags = ["CD", "Continuous Delivery", "Continuous Deployment", "GitOps", "ArgoCD", "Deployment Strategies"]
+++

# 지속적 전달/배포 (CD, Continuous Delivery/Deployment)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 지속적 전달(Continuous Delivery)은 CI를 통과한 코드를 **언제든지 프로덕션에 배포할 수 있는 상태로 유지**하는 것(수동 승인 포함)이며, 지속적 배포(Continuous Deployment)는 **수동 승인 없이 자동으로 프로덕션까지 배포**하는 것을 의미합니다.
> 2. **가치**: CD는 "한 번의 클릭(또는 자동)으로 배포"를 가능하게 하여 배포 리드 타임을 획기적으로 단축하고, 롤링/블루-그린/카나리 배포 전략을 통해 무중단 배포와 장애 시 빠른 롤백을 보장합니다.
> 3. **융합**: GitOps(ArgoCD, FluxCD), 카나리 분석(Kayenta), 피처 토글(Feature Toggle), 서비스 메시(Istio)와 결합하여 안전하고 자동화된 프로덕션 배포 파이프라인을 구축합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**지속적 전달(Continuous Delivery, CD)**과 **지속적 배포(Continuous Deployment, CD)**는 종종 혼용되지만 중요한 차이가 있습니다:

| 구분 | 지속적 전달 (Continuous Delivery) | 지속적 배포 (Continuous Deployment) |
| :--- | :--- | :--- |
| **정의** | 코드가 **언제든지 프로덕션에 배포될 준비**가 되어 있음 | 코드가 **자동으로 프로덕션에 배포**됨 |
| **수동 승인** | 필요 (버튼 클릭) | 불필요 (완전 자동화) |
| **배포 트리거** | 인간의 결정 | CI 테스트 통과 시 자동 |
| **위험도** | 낮음 (통제 가능) | 높음 (자동화 신뢰 필요) |
| **적합한 환경** | 규제 산업, 높은 위험 | 높은 테스트 신뢰도, 빠른 피드백 |

**공통 핵심 원칙**:
1. **모든 변경사항은 배포 가능**: 모든 커밋이 프로덕션 배포 후보입니다.
2. **자동화된 배포 파이프라인**: 수동 작업 없이 배포가 진행됩니다.
3. **빠른 피드백 루프**: 배포 결과가 즉시 개발팀에 전달됩니다.
4. **롤백 가능**: 언제든 이전 버전으로 복구할 수 있습니다.

### 💡 2. 구체적인 일상생활 비유
**자동차 생산 라인**을 상상해 보세요:

**지속적 전달 (Continuous Delivery)**:
- 자동차가 조립 라인을 거쳐 완성됩니다.
- 품질 검사를 통과하면 **'출고 대기 구역'**에 놓입니다.
- **영업사원이 "이 차 출고!"**라고 승인하면 딜러십으로 갑니다.

**지속적 배포 (Continuous Deployment)**:
- 자동차가 조립 라인을 거쳐 완성됩니다.
- 품질 검사를 통과하면 **자동으로 트럭에 실려 딜러십으로 갑니다.**
- 사람의 승인 없이 **완전 자동화**됩니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (수동 배포의 위험)**:
   과거에는 배포가 **고도로 수동적이고 위험한** 작업이었습니다:
   - "배포 날(Deployment Day)"이 정해지고, 야간에 IT 팀이 철야합니다.
   - 100페이지짜리 배포 매뉴얼을 따라 수동으로 명령어를 입력합니다.
   - 한 번의 오타로 전체 시스템이 다운됩니다.
   - 평균 배포 주기: 분기 1회 (또는 연 1회).

2. **혁신적 패러다임 변화의 시작**:
   - **2006년**: Flickr가 "하루에 10번 배포" 발표. 업계 충격.
   - **2010년**: Jez Humble & David Farley가 "Continuous Delivery" 저서 출간.
   - **2013년**: Netflix가 Spinnaker 오픈소스 공개.
   - **2017년**: GitOps 개념 등장 (Weaveworks).
   - **현재**: ArgoCD, FluxCD가 쿠버네티스 표준 CD 도구로 자리잡음.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   "Time to Market"이 경쟁력의 핵심입니다. 아마존, 넷플릭스, 구글은 하루에 수천 번 배포합니다. 느린 배포 = 기회 비용입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **CD 서버** | 배포 파이프라인 오케스트레이션 | 단계별 Job 실행, 승인 게이트 | Jenkins, GitLab CI | 생산 관리자 |
| **GitOps Operator** | Git 상태를 클러스터에 동기화 | Git Polling, K8s API 호출 | ArgoCD, FluxCD | 로봇 팔 |
| **배포 전략 엔진** | 무중단 배포 실행 | Rolling, Blue-Green, Canary | Kubernetes, Spinnaker | 도로 교통 제어 |
| **카나리 분석기** | 신버전 트래픽 검증 | 메트릭 비교, 통계적 유의성 | Kayenta, Flagger | 품질 검사원 |
| **롤백 메커니즘** | 장애 시 이전 버전 복구 | Git Revert, K8s Rollout Undo | ArgoCD, Helm | 비상 브레이크 |

### 2. 정교한 구조 다이어그램: CD 파이프라인 아키텍처

```text
=====================================================================================================
                    [ Continuous Delivery/Deployment Pipeline Architecture ]
=====================================================================================================

+-------------------------------------------------------------------------------------------+
|                              [ CI → CD HANDOFF ]                                          |
|                                                                                           |
│   CI 파이프라인 완료                                                                       │
│   ✅ Build: SUCCESS                                                                       │
│   ✅ Tests: 156 passed                                                                    │
│   ✅ Quality Gate: PASSED                                                                 │
│   ✅ Security Scan: PASSED                                                                │
│   📦 Artifact: myapp:v1.2.0-abc123                                                        │
│                                                                                           |
+-------------------------------------------------------------------------------------------+
                                        │
                                        ▼
+-------------------------------------------------------------------------------------------+
|                              [ CD PIPELINE STAGES ]                                       |
|                                                                                           |
|  ┌─────────────────────────────────────────────────────────────────────────────────────┐  |
|  │ STAGE 1: DEPLOY TO STAGING                                                          │  |
|  │                                                                                     │  |
|  │  +-------------------------------------------------------------------------+        │  |
|  │  │ Helm Upgrade                                                             │        │  |
|  │  │ $ helm upgrade myapp ./chart --set image.tag=v1.2.0-abc123 -n staging  │        │  |
|  │  │ Release "myapp" has been upgraded.                                      │        │  |
|  │  +-------------------------------------------------------------------------+        │  |
|  │                                        │                                            │  |
|  │                                        ▼                                            │  |
|  │  +-------------------------------------------------------------------------+        │  |
|  │  │ Staging Environment (Kubernetes)                                        │        │  |
|  │  │                                                                         │        │  |
|  │  │ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                      │        │  |
|  │  │ │ Pod: myapp  │  │ Pod: myapp  │  │ Service     │                      │        │  |
|  │  │ │ v1.2.0-abc  │  │ v1.2.0-abc  │  │ LoadBalancer│                      │        │  |
|  │  │ └─────────────┘  └─────────────┘  └─────────────┘                      │        │  |
|  │  │                                                                         │        │  |
|  │  │ E2E Tests: ✅ PASSED                                                    │        │  |
|  │  │ Smoke Tests: ✅ PASSED                                                  │        │  |
|  │  +-------------------------------------------------------------------------+        │  |
|  └─────────────────────────────────────────────────────────────────────────────────────┘  |
│                                         │                                                 |
│                                         │ Continuous Delivery: 수동 승인 대기              │
│                                         │ Continuous Deployment: 자동 진행                │
│                                         ▼                                                 |
|  ┌─────────────────────────────────────────────────────────────────────────────────────┐  |
|  │ STAGE 2: APPROVAL GATE (Continuous Delivery Only)                                   │  |
|  │                                                                                     │  |
|  │  +-------------------------------------------------------------------------+        │  |
|  │  │ 🛑 Waiting for Manual Approval                                         │        │  |
|  │  │                                                                         │        │  |
|  │  │ Approvers: @tech-lead, @product-owner                                  │        │  |
|  │  │                                                                         │        │  |
|  │  │ [Approve] [Reject] [Add Comment]                                       │        │  |
|  │  +-------------------------------------------------------------------------+        │  |
|  │                                        │                                            │  |
|  │                                        ▼ Approved                                   │  |
|  └─────────────────────────────────────────────────────────────────────────────────────┘  |
│                                         │                                                 |
│                                         ▼                                                 |
|  ┌─────────────────────────────────────────────────────────────────────────────────────┐  |
|  │ STAGE 3: CANARY DEPLOYMENT TO PRODUCTION                                            │  |
|  │                                                                                     │  |
|  │  +-------------------------------------------------------------------------+        │  |
|  │  │ Canary: 1% Traffic → New Version                                       │        │  |
|  │  │                                                                         │        │  |
|  │  │ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                      │        │  |
|  │  │ │ STABLE      │  │ STABLE      │  │ CANARY      │ ← 1% Traffic         │        │  |
|  │  │ │ v1.1.0      │  │ v1.1.0      │  │ v1.2.0-abc  │                      │        │  |
|  │  │ │ (99%)       │  │ (99%)       │  │ (1%)        │                      │        │  |
|  │  │ └─────────────┘  └─────────────┘  └─────────────┘                      │        │  |
|  │  │                                                                         │        │  |
|  │  │ Metrics Analysis:                                                       │        │  |
|  │  │ - Error Rate: 0.02% (Baseline: 0.05%) ✅                               │        │  |
|  │  │ - Latency P99: 120ms (Baseline: 150ms) ✅                              │        │  |
|  │  +-------------------------------------------------------------------------+        │  |
|  └─────────────────────────────────────────────────────────────────────────────────────┘  |
│                                         │                                                 |
│                                         │ 카나리 메트릭 정상                               │
│                                         ▼                                                 |
|  ┌─────────────────────────────────────────────────────────────────────────────────────┐  |
|  │ STAGE 4: PROGRESSIVE ROLLOUT                                                         │  |
|  │                                                                                     │  |
|  │  +-------------------------------------------------------------------------+        │  |
|  │  │ Canary: 10% → 25% → 50% → 100%                                         │        │  |
|  │  │                                                                         │        │  |
|  │  │ [10%] ──✅──> [25%] ──✅──> [50%] ──✅──> [100%]                        │        │  |
|  │  │                                                                         │        │  |
|  │  │ Each step: Wait 5min + Metrics Check                                   │        │  |
|  │  +-------------------------------------------------------------------------+        │  |
|  └─────────────────────────────────────────────────────────────────────────────────────┘  |
│                                         │                                                 |
│                                         ▼                                                 |
|  ┌─────────────────────────────────────────────────────────────────────────────────────┐  |
|  │ STAGE 5: PRODUCTION DEPLOYMENT COMPLETE                                              │  |
|  │                                                                                     │  |
|  │  +-------------------------------------------------------------------------+        │  |
|  │  │ PRODUCTION Environment                                                 │        │  |
|  │  │                                                                         │        │  |
|  │  │ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                      │        │  |
|  │  │ │ Pod: myapp  │  │ Pod: myapp  │  │ Pod: myapp  │                      │        │  |
|  │  │ │ v1.2.0-abc  │  │ v1.2.0-abc  │  │ v1.2.0-abc  │                      │        │  |
|  │  │ └─────────────┘  └─────────────┘  └─────────────┘                      │        │  |
|  │  │                                                                         │        │  |
|  │  │ 🎉 Deployment Successful!                                               │        │  |
|  │  │ Notify: Slack #deployments, PagerDuty (if failed)                      │        │  |
|  │  +-------------------------------------------------------------------------+        │  |
|  └─────────────────────────────────────────────────────────────────────────────────────┘  |
+-------------------------------------------------------------------------------------------+

=====================================================================================================
   배포 전략 비교:
   - Rolling Update: 순차적 교체 (기본)
   - Blue-Green: 전환 스위치 (빠른 롤백)
   - Canary: 점진적 트래픽 증가 (안전)
   - A/B Testing: 사용자 기반 분할 (실험)
=====================================================================================================
```

### 3. 심층 동작 원리 (배포 전략 상세)

**1. 롤링 업데이트 (Rolling Update)**
```yaml
# Kubernetes Deployment - Rolling Update 설정
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%        # 추가로 생성할 수 있는 최대 파드 수
      maxUnavailable: 25%  # 동시에 사용 불가능한 최대 파드 수
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:v1.2.0
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
```

**2. 블루-그린 배포 (Blue-Green Deployment)**
```yaml
# Blue-Green 배포 (Kubernetes Service 전환)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # blue → green으로 전환
  ports:
  - port: 80
    targetPort: 8080

---
# Blue (현재 버전)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
spec:
  replicas: 10
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:v1.1.0

---
# Green (새 버전)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
spec:
  replicas: 10
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:v1.2.0
```

**3. 카나리 배포 (Canary Deployment)**
```yaml
# Istio VirtualService - 카나리 트래픽 분할
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - route:
    - destination:
        host: myapp-stable
      weight: 90  # 90% 트래픽 → 안정 버전
    - destination:
        host: myapp-canary
      weight: 10  # 10% 트래픽 → 카나리 버전
```

### 4. 실무 코드 예시 (GitOps with ArgoCD)

```yaml
# ArgoCD Application - GitOps 배포 정의
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-production
  namespace: argocd
  finalizers:
  - resources-finalizer.argocd.argoproj.io
spec:
  project: default

  source:
    repoURL: https://github.com/org/myapp-gitops.git
    targetRevision: main
    path: overlays/production

  destination:
    server: https://kubernetes.default.svc
    namespace: production

  syncPolicy:
    automated:
      prune: true      # Git에 없는 리소스 자동 삭제
      selfHeal: true   # 드리프트 감지 시 자동 복구
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    - PruneLast=true
    - ApplyOutOfSyncOnly=true

    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /spec/replicas  # HPA가 관리하므로 무시

---
# Kustomize - 환경별 오버레이
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml
- configmap.yaml

# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

resources:
- ../../base

patchesStrategicMerge:
- deployment-replicas.yaml

images:
- name: myapp
  newTag: v1.2.0  # 새 버전으로 업데이트

# overlays/production/deployment-replicas.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 20  # 프로덕션은 20개 파드
```

```yaml
# GitHub Actions - GitOps 트리거
name: Update GitOps Repository

on:
  workflow_dispatch:
    inputs:
      image_tag:
        description: 'Docker image tag to deploy'
        required: true

jobs:
  update-gitops:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout GitOps repo
        uses: actions/checkout@v4
        with:
          repository: org/myapp-gitops
          token: ${{ secrets.GITOPS_TOKEN }}

      - name: Update image tag
        run: |
          cd overlays/production
          kustomize edit set image myapp:${{ github.event.inputs.image_tag }}

      - name: Commit and push
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add .
          git commit -m "chore: Update myapp to ${{ github.event.inputs.image_tag }}"
          git push

      # ArgoCD가 자동으로 변경사항을 감지하고 동기화
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 배포 전략 심층 비교표

| 평가 지표 | Rolling Update | Blue-Green | Canary | A/B Testing |
| :--- | :--- | :--- | :--- | :--- |
| **리소스 사용** | 적음 (기존 + 일부) | 많음 (2배) | 중간 | 중간 |
| **롤백 속도** | 느림 (역순 진행) | 빠름 (스위치) | 빠름 (트래픽 차단) | 빠름 |
| **위험도** | 중간 (혼재 기간) | 낮음 | 매우 낮음 | 낮음 |
| **복잡도** | 낮음 | 중간 | 높음 | 높음 |
| **적합한 상황** | 일반적 배포 | 중요 서비스 | 대규모 트래픽 | 기능 실험 |
| **필요 인프라** | K8s 기본 | 이중 환경 | Istio/SM | Istio + 실험 플랫폼 |

### 2. CD 도구 비교표

| 평가 지표 | ArgoCD | FluxCD | Spinnaker | Jenkins CD |
| :--- | :--- | :--- | :--- | :--- |
| **방식** | GitOps (Pull) | GitOps (Pull) | Push/Pull | Push |
| **UI 품질** | 매우 좋음 | 좋음 | 매우 좋음 | 보통 |
| **멀티 클러스터** | 지원 | 지원 | 지원 | 플러그인 |
| **카나리 분석** | Rollouts | Flagger | Kayenta | 플러그인 |
| **학습 곡선** | 낮음 | 중간 | 높음 | 중간 |
| **CNCF 상태** | 졸업 | 졸업 | - | - |

### 3. 과목 융합 관점 분석

**CD + SRE (Error Budget)**
- 에러 버짯이 소진되면 자동으로 배포를 차단합니다.
- "버짯이 남아있을 때만 배포 허용" 정책을 구현합니다.

**CD + Observability**
- 배포 후 자동으로 메트릭을 모니터링합니다.
- 이상 징후 탐지 시 자동 롤백을 트리거합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 배포 후 장애가 빈번히 발생**
- **문제점**: 배포 직후 에러율이 급증하지만, 이미 전체 트래픽이 신버전으로 흐름.
- **기술사 판단**: **카나리 배포 + 자동 롤백 도입**.
  1. 1% 트래픽만 신버전으로.
  2. 메트릭(에러율, 지연 시간)을 5분간 관찰.
  3. 임계치 초과 시 자동 롤백.
  4. 정상이면 10% → 50% → 100%로 점진 확대.

**[상황 B] 규제 산업(금융)에서 완전 자동화 요구사항**
- **문제점**: 모든 프로덕션 변경은 감사 기록 필요. 수동 승인 없는 자동 배포 불가.
- **기술사 판단**: **Continuous Delivery (수동 승인 포함)**.
  1. 모든 단계 자동화.
  2. 프로덕션 배포 직전 승인 게이트(Approval Gate) 추가.
  3. 승인자 감사 로그 기록.
  4. 승인 후 1-Click 배포.

### 2. CD 구축 체크리스트

**배포 파이프라인 체크리스트**
- [ ] 스테이징 환경에서 자동 테스트가 실행되는가?
- [ ] 롤백이 5분 이내에 가능한가?
- [ ] 배포 알림이 팀에 전달되는가?
- [ ] 배포 히스토리가 보존되는가?

**안전장치 체크리스트**
- [ ] 배포 전 건강 검사(Health Check)가 수행되는가?
- [ ] 카나리/블루-그린 배포가 가능한가?
- [ ] 자동 롤백 조건이 정의되어 있는가?
- [ ] 배포 중 서비스 중단이 없는가?

### 3. 안티패턴 (Anti-patterns)

**안티패턴 1: Big Bang 배포**
- 한 번에 모든 서버를 교체.
- **문제**: 장애 시 전체 서비스 중단.
- **해결**: 점진적 배포 전략 적용.

**안티패턴 2: 수동 롤백**
- 롤백도 수동으로 수행.
- **문제**: 롤백 시간이 너무 김.
- **해결**: 자동 롤백 메커니즘 구현.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 (AS-IS) | 도입 후 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **배포 빈도** | 월 1회 | 일 10회 이상 | **300배 증가** |
| **배포 리드 타임** | 2주 | 30분 | **90% 단축** |
| **배포 실패율** | 15% | 1% | **93% 감소** |
| **평균 복구 시간** | 4시간 | 5분 | **98% 단축** |

### 2. 미래 전망 및 진화 방향

**Progressive Delivery**
- 카나리를 넘어 더 정교한 점진적 배포.
- 사용자 세그먼트별, 지역별 점진적 출시.

**AI 기반 배포 결정**
- AI가 메트릭을 분석하여 배포 진행/중단을 자동 결정.
- "이상 패턴 감지, 배포 자동 중단".

### 3. 참고 표준/가이드
- **Continuous Delivery (Jez Humble, David Farley)**: CD 바이블
- **GitOps (Weaveworks)**: GitOps 원칙
- **ArgoCD Documentation**: 쿠버네티스 GitOps 구현
- **Kubernetes Deployment Strategies**: 배포 전략 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **[지속적 통합 (CI)](./continuous_integration.md)**: CD의 전 단계인 자동화된 빌드/테스트
- **[GitOps](@/studynotes/15_devops_sre/03_automation/cicd_gitops.md)**: Git을 단일 진실 공급원으로 활용하는 CD 방식
- **[무중단 배포 전략](./deployment_strategies.md)**: Rolling, Blue-Green, Canary 배포 기법
- **[SRE 원칙](@/studynotes/15_devops_sre/01_sre/sre_principles.md)**: 에러 버짯 기반 배포 정책

---

## 👶 어린이를 위한 3줄 비유 설명
1. CD는 **'자동차 공장의 로봇 팔'**이에요. 조립이 끝나면 자동으로 검사하고, **'출고 준비 완료!'**라고 알려줘요.
2. Continuous Delivery는 **'영업사람이 승인하면'** 출고돼요. Continuous Deployment는 **'승인 없이 자동으로'** 출고돼요.
3. 만약 문제가 생기면 **'비상 정지 버튼'**을 눌러서 이전 상태로 되돌릴 수 있어요. 안전하죠!
