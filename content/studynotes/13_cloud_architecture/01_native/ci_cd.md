+++
title = "CI/CD (지속적 통합/지속적 배포)"
date = 2024-05-17
description = "코드 변경사항을 자동으로 빌드, 테스트, 배포하는 파이프라인으로, CI(Continuous Integration)는 통합/테스트 자동화, CD(Continuous Delivery/Deployment)는 배포 자동화를 담당"
weight = 205
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["CI/CD", "Continuous Integration", "Continuous Delivery", "Jenkins", "GitHub Actions", "Pipeline"]
+++

# CI/CD (지속적 통합/지속적 배포) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 개발자가 코드를 Git에 Push하면 자동으로 **빌드 → 테스트 → 배포**까지 수행되는 자동화 파이프라인입니다. CI는 코드 통합과 테스트 자동화, CD는 운영 환경까지의 배포 자동화를 의미합니다.
> 2. **가치**: 수동 배포에 걸리는 수시간/수일을 **수분으로 단축**하며, 인적 오류를 제거하고, 피드백 루프를 가속화하여 **개발 생산성을 200% 이상 향상**시킵니다.
> 3. **융합**: Git 기반 워크플로우, 컨테이너(Docker), Kubernetes, GitOps(ArgoCD), Feature Flag 등과 결합하여 현대적 소프트웨어 공급망을 구축합니다.

---

## Ⅰ. 개요 (Context & Background)

CI/CD는 Continuous Integration(지속적 통합)과 Continuous Delivery/Deployment(지속적 전달/배포)의 약어입니다. CI는 개발자들이 작성한 코드를 중앙 저장소에 자주 병합하고, 자동으로 빌드 및 테스트하는 과정입니다. CD는 CI를 통과한 코드를 운영 환경(또는 운영 직전 환경)까지 자동으로 배포하는 과정입니다.

**💡 비유**: CI/CD는 **'자동차 조립 라인'**과 같습니다. 과거에는 한 명의 기술자가 모든 부품을 조립했습니다(수동 배포). 이제는 컨베이어 벨트 위에서 로봇이 자동으로 조립합니다(CI/CD). 부품(코드)이 들어오면 자동으로 조립(빌드), 검사(테스트), 출고(배포)됩니다.

**등장 배경 및 발전 과정**:
1. **Integration Hell**: 개발자들이 각자 작업하다가 배포 전에 한 번에 합치면서 수많은 충돌이 발생했습니다.
2. **Extreme Programming (1999)**: Kent Beck이 "지속적 통합" 개념을 소개했습니다.
3. **Jenkins (2011)**: Hudson에서 분기된 오픈소스 CI 서버가 업계 표준이 되었습니다.
4. **Cloud-native CI/CD (2015~)**: GitHub Actions, GitLab CI, CircleCI가 클라우드 기반 서비스로 등장했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### CI vs CD vs CD (지속적 전달 vs 지속적 배포)

| 단계 | 명칭 | 상세 설명 | 자동화 범위 | 인간 개입 |
|---|---|---|---|---|
| **CI** | Continuous Integration | 빌드 + 단위/통합 테스트 | 개발 → 테스트 | 없음 |
| **CD** | Continuous Delivery | 스테이징까지 자동, 운영은 수동 승인 | 개발 → 스테이징 | 운영 배포 승인 |
| **CD** | Continuous Deployment | 운영까지 완전 자동 | 개발 → 운영 | 없음 |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                        [ CI/CD Pipeline Architecture ]                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              [ Source Stage ]                               │
│                                                                             │
│    Developer ───► Git Push ───► GitHub/GitLab                              │
│                          │                                                  │
│                          ▼                                                  │
│                    ┌───────────────┐                                        │
│                    │  Webhook      │ ─────────────────────────┐            │
│                    │  Trigger      │                          │            │
│                    └───────────────┘                          │            │
│                                                               │            │
└───────────────────────────────────────────────────────────────┼────────────┘
                                                                │
┌───────────────────────────────────────────────────────────────▼────────────┐
│                              [ CI Stage ]                                   │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                        Build Stage                                     │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │ │
│  │  │Checkout │─►│ Install │─►│  Build  │─►│ Artifact │                  │ │
│  │  │  Code   │  │   Deps  │  │         │  │  Create │                  │ │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘                  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                  │                                          │
│  ┌───────────────────────────────▼───────────────────────────────────────┐ │
│  │                        Test Stage                                      │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │ │
│  │  │  Unit   │─►│Integra- │─►│   E2E   │─►│ Coverage│                  │ │
│  │  │  Tests  │  │  tion   │  │  Tests  │  │  Report │                  │ │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘                  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                  │                                          │
│  ┌───────────────────────────────▼───────────────────────────────────────┐ │
│  │                       Quality Gate                                     │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │ │
│  │  │ Linting │  │Security │  │  Code   │  │ License │                  │ │
│  │  │  Check  │  │  Scan   │  │Quality  │  │  Check  │                  │ │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘                  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼ All Tests Pass
┌─────────────────────────────────────────────────────────────────────────────┐
│                              [ CD Stage ]                                   │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                       Deploy to Staging                                │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │ │
│  │  │ Docker  │─►│ Push to │─►│  Deploy │─►│ Smoke   │                  │ │
│  │  │  Build  │  │Registry │  │ Staging │  │  Test   │                  │ │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘                  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                  │                                          │
│                                  ▼ Manual Approval (Continuous Delivery)   │
│                                  │     OR                                   │
│                                  │ Auto (Continuous Deployment)            │
│                                  ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                      Deploy to Production                              │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │ │
│  │  │ Blue/   │─►│Canary   │─►│ Traffic │─►│ Monitor │                  │ │
│  │  │ Green   │  │ Deploy  │  │ Shift   │  │ & Alert │                  │ │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘                  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: 배포 전략

```
┌────────────────────────────────────────────────────────────────────────────┐
│                       Deployment Strategies                                │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ 1. Rolling Update ]                                                     │
│                                                                            │
│  Version v1:  [Pod] [Pod] [Pod] [Pod]                                      │
│       │          │     │                                                   │
│       │      ┌───▼─────▼───┐                                               │
│       │      │ Terminate   │                                               │
│       │      └─────────────┘                                               │
│       ▼                                                                     │
│  Version v1:  [Pod] [Pod] [Pod]                                            │
│  Version v2:  [Pod]                                                        │
│       │              │                                                     │
│       │          ┌───▼───┐                                                 │
│       │          │Create │                                                 │
│       │          └───────┘                                                 │
│       ▼                                                                     │
│  Version v1:  [Pod] [Pod]                                                  │
│  Version v2:  [Pod] [Pod]                                                  │
│       ...                                                                   │
│  Version v2:  [Pod] [Pod] [Pod] [Pod]                                      │
│                                                                            │
│  장점: 리소스 효율적                                                         │
│  단점: v1/v2 공존 기간 존재                                                  │
│                                                                            │
│  [ 2. Blue-Green Deployment ]                                              │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                         Load Balancer                               │  │
│  │                              │                                      │  │
│  │              100% traffic ───┘                                      │  │
│  │                              │                                      │  │
│  │  ┌───────────────┐          │         ┌───────────────┐            │  │
│  │  │    BLUE       │◄─────────┘         │    GREEN      │            │  │
│  │  │   (v1)        │                    │    (v2)       │            │  │
│  │  │ [Pod][Pod]    │                    │  [Pod][Pod]   │            │  │
│  │  │ Active        │                    │  Idle         │            │  │
│  │  └───────────────┘                    └───────────────┘            │  │
│  │                                                                     │  │
│  │  Switch: BLUE → GREEN (instant)                                     │  │
│  │  Rollback: GREEN → BLUE (instant)                                   │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  장점: 즉시 전환/롤백                                                        │
│  단점: 2배 리소스 필요                                                       │
│                                                                            │
│  [ 3. Canary Deployment ]                                                  │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                         Load Balancer                               │  │
│  │                              │                                      │  │
│  │         ┌────────────────────┼────────────────────┐                │  │
│  │         │                    │                    │                │  │
│  │         │ 95%                │ 5%                 │                │  │
│  │         ▼                    ▼                    │                │  │
│  │  ┌───────────────┐   ┌───────────────┐           │                │  │
│  │  │   STABLE      │   │   CANARY      │           │                │  │
│  │  │   (v1)        │   │    (v2)       │           │                │  │
│  │  │ [Pod][Pod]... │   │   [Pod]       │           │                │  │
│  │  └───────────────┘   └───────────────┘           │                │  │
│  │                                                   │                │  │
│  │  5% → 25% → 50% → 100% (gradual traffic shift)   │                │  │
│  │  Monitor: Error Rate, Latency, Business Metrics  │                │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  장점: 위험 최소화, A/B 테스트 가능                                          │
│  단점: 복잡한 트래픽 관리                                                     │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: GitLab CI/CD Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - security
  - deploy-staging
  - deploy-production

variables:
  DOCKER_REGISTRY: registry.gitlab.com
  IMAGE_NAME: $CI_REGISTRY_IMAGE
  IMAGE_TAG: $CI_COMMIT_SHORT_SHA

# Build Stage
build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $IMAGE_NAME:$IMAGE_TAG .
    - docker push $IMAGE_NAME:$IMAGE_TAG
    - docker push $IMAGE_NAME:latest
  only:
    - main
    - develop

# Test Stage
unit-test:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
    - pytest --cov=app --cov-report=xml --junitxml=report.xml
  artifacts:
    reports:
      junit: report.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
  coverage: '/TOTAL.*\s+(\d+%)$/'

integration-test:
  stage: test
  image: docker:24
  services:
    - docker:24-dind
    - postgres:15
  variables:
    POSTGRES_DB: test_db
    POSTGRES_USER: test
    POSTGRES_PASSWORD: test
  script:
    - docker-compose -f docker-compose.test.yml up --abort-on-container-exit
  only:
    - main
    - merge_requests

# Security Stage
security-scan:
  stage: security
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $IMAGE_NAME:$IMAGE_TAG
  allow_failure: true

sast:
  stage: security
  include:
    - template: Security/SAST.gitlab-ci.yml

# Deploy to Staging
deploy-staging:
  stage: deploy-staging
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context staging-cluster
    - kubectl set image deployment/api api=$IMAGE_NAME:$IMAGE_TAG -n staging
    - kubectl rollout status deployment/api -n staging --timeout=300s
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

# Deploy to Production
deploy-production:
  stage: deploy-production
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context production-cluster
    # Canary deployment: 10% 트래픽
    - kubectl apply -f k8s/canary.yaml
    - sleep 300  # 5분 대기 후 메트릭 확인
    - kubectl patch service api -p '{"spec":{"selector":{"version":"v2"}}}'
  environment:
    name: production
    url: https://www.example.com
  when: manual  # Continuous Delivery (수동 승인)
  only:
    - main
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: CI/CD 도구

| 비교 관점 | Jenkins | GitHub Actions | GitLab CI | CircleCI |
|---|---|---|---|---|
| **호스팅** | Self-hosted/Cloud | Cloud only | Self/Cloud | Cloud only |
| **설정 방식** | Groovy/Jenkinsfile | YAML | YAML | YAML |
| **학습 곡선** | 높음 | 낮음 | 중간 | 낮음 |
| **확장성** | 높음 (Plugin) | 중간 | 높음 | 중간 |
| **비용** | 오픈소스 (서버 비용) | 퍼블릭 무료 | 오픈소스/상용 | 무료 tier 있음 |
| **Git 통합** | 별도 설정 | 네이티브 | 네이티브 | 네이티브 |

### 과목 융합 관점 분석

**보안(Security)과의 융합 (DevSecOps)**:
- **SAST (Static Application Security Testing)**: 코드 정적 분석
- **DAST (Dynamic Application Security Testing)**: 런타임 분석
- **SCA (Software Composition Analysis)**: 의존성 취약점 스캔
- **Container Scanning**: 이미지 취약점 스캔

**클라우드와의 융합**:
- **GitOps**: Git을 단일 진실 공급원으로 (ArgoCD, Flux)
- **Infrastructure as Code**: Terraform, Pulumi를 파이프라인에 통합

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: CI/CD 파이프라인 설계

**문제 상황**: 배포 주기가 2주이며, 배포마다 4시간이 소요됩니다. 수동 테스트로 인해 버그가 운영까지 유입됩니다.

**기술사의 전략적 의사결정**:
1. **자동화 범위**: 빌드 → 단위 테스트 → 통합 테스트 → 보안 스캔 → 스테이징 배포
2. **품질 게이트**: 테스트 커버리지 80% 이상, Critical 취약점 0개
3. **배포 전략**: Canary (10% → 50% → 100%)
4. **롤백 전략**: 자동 롤백 (에러율 5% 초과 시)

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - Flakey Tests**: 불안정한 테스트는 CI/CD 신뢰도를 떨어뜨립니다. 테스트 격리와 결정적 테스트 작성이 필수입니다.
- **체크리스트**:
  - [ ] 빌드/테스트 시간 10분 이내 목표
  - [ ] 병렬 실행으로 시간 단축
  - [ ] 캐싱 전략 (의존성, 빌드 아티팩트)
  - [ ] 알림 설정 (Slack, Email)
  - [ ] 배포 롤백 자동화

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 수동 배포 | CI/CD | 개선율 |
|---|---|---|---|
| **배포 시간** | 4시간 | 15분 | 94% 단축 |
| **배포 빈도** | 2주 1회 | 일 1회+ | 14x 증가 |
| **버그 유입** | 30% | 5% | 83% 감소 |
| **인적 오류** | 빈번 | 거의 없음 | 90% 감소 |

### 미래 전망 및 진화 방향

- **Progressive Delivery**: Canary → Blue-Green → Feature Flag의 결합
- **AI-Assisted CI/CD**: 테스트 선택 최적화, 장애 예측
- **Pipeline as Code**: 모든 파이프라인 설정을 코드로 관리

### ※ 참고 표준/가이드
- **12-Factor App**: CI/CD 친화적 애플리케이션 설계
- **DORA State of DevOps**: CI/CD 성숙도 벤치마크
- **OWASP CI/CD Security Guide**: 보안 모범 사례

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [DevOps](@/studynotes/13_cloud_architecture/01_native/devops.md) : CI/CD의 상위 개념
- [GitOps](@/studynotes/13_cloud_architecture/01_native/gitops.md) : Git 기반 CD
- [Feature Flag](@/studynotes/13_cloud_architecture/01_native/feature_flag.md) : 기능 토글
- [Kubernetes](@/studynotes/13_cloud_architecture/01_native/kubernetes.md) : 배포 타겟 플랫폼
- [Container Registry](@/studynotes/13_cloud_architecture/01_native/container_registry.md) : 이미지 저장소

---

### 👶 어린이를 위한 3줄 비유 설명
1. CI/CD는 **'자동차 공장 컨베이어 벨트'**예요. 부품(코드)을 올리면 자동으로 조립돼요.
2. 조립이 끝나면 **'자동으로 검사해요'**. 불량품은 출고되지 않아요.
3. 검사를 통과하면 **'자동으로 매장에 진열돼요'**. 사람이 직접 옮길 필요가 없죠!
