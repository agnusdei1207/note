+++
title = "44. CI/CD (Continuous Integration/Deployment)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["CI/CD", "Jenkins", "GitOps", "ArgoCD", "Pipeline"]
draft = false
+++

# CI/CD (Continuous Integration/Deployment)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CI/CD는 **"코드 **변경**을 **자동 **빌드**, **테스트**, **배포**하는 **파이프라인\\\"**으로, **CI**(Continuous **Integration)**가 **빌드/테스트**를 **자동화**하고 **CD**(Continuous **Deployment/Delivery)**가 **프로덕션 **배포**를 **자동화**한다.
> 2. **파이프라인**: **Source**(Git)** → **Build**(Maven, **Docker)** → **Test**(Unit, **E2E)** → **Deploy**(Kubernetes)**로 **구성**되고 **Pipeline as **Code**(Jenkinsfile, **GitHub **Actions)**가 **버전 **관리**를 **가능**하게 **한다.
> 3. **GitOps**: **Git**을 **단일 **진실 **공간**(Single **Source **of **Truth)**으로 **사용**하고 **ArgoCD**, **Flux**가 **Kubernetes **클러스터**를 **동기화**하며 **Pull **Request**로 **배포**를 **승인**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
CI/CD는 **"자동화된 소프트웨어 배포 파이프라인"**이다.

**CI/CD 단계**:
| 단계 | 목적 | 도구 |
|------|------|------|
| **CI** | 빌드/테스트 자동화 | Jenkins, GitHub Actions |
| **CD** | 배포 자동화 | ArgoCD, Spinnaker |
| **CT** | 테스트 자동화 | Selenium, JUnit |
| **CM** | 모니터링 | Prometheus, ELK |

### 💡 비유
CI/CD는 ****자동 **생산 **라인 ****과 같다.
- **컨베이어**: 파이프라인
- **검사**: 테스트
- **출하**: 배포

---

## Ⅱ. 아키텍처 및 핵심 원리

### CI/CD 파이프라인

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         CI/CD Pipeline Architecture                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Complete Pipeline:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Developer                                              Production                       │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. Code Push                                                                         │  │  │
    │  │  git push origin feature/new-functionality                                           │  │  │
    │  │  │                                                                                   │  │  │
    │  │  ▼                                                                                   │  │  │
    │  │  2. Trigger CI (GitHub Actions / Jenkins)                                             │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │  │
    │  │  │  Checkout code                                                                    │  │  │  │  │
    │  │  │  │                                                                               │  │  │  │  │
    │  │  │  ▼                                                                               │  │  │  │  │
    │  │  │  Build (mvn clean package / docker build)                                        │  │  │  │  │
    │  │  │  │                                                                               │  │  │  │  │
    │  │  │  ▼                                                                               │  │  │  │  │
    │  │  │  Unit Tests (mvn test)                                                           │  │  │  │  │
    │  │  │  │                                                                               │  │  │  │  │
    │  │  │  ▼                                                                               │  │  │  │  │
    │  │  │  Code Quality (SonarQube)                                                         │  │  │  │  │
    │  │  │  │                                                                               │  │  │  │  │
    │  │  │  ▼                                                                               │  │  │  │  │
    │  │  │  Security Scan (Snyk, Trivy)                                                      │  │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  │  │                                                                                   │  │  │
    │  │  ▼ (All tests pass)                                                                 │  │  │
    │  │  3. Push Artifact (Docker Image to Registry)                                         │  │  │
    │  │  docker push registry.example.com/app:v1.2.3                                         │  │  │
    │  │  │                                                                                   │  │  │
    │  │  ▼                                                                                   │  │  │
    │  │  4. Deploy to Staging (Helm upgrade / kubectl apply)                                  │  │  │
    │  │  │                                                                                   │  │  │
    │  │  ▼                                                                                   │  │  │
    │  │  5. Integration Tests (Selenium, Postman)                                            │  │  │
    │  │  │                                                                                   │  │  │
    │  │  ▼                                                                                   │  │  │
    │  │  6. Manual Approval (if required)                                                     │  │  │
    │  │  │                                                                                   │  │  │
    │  │  ▼                                                                                   │  │  │
    │  │  7. Deploy to Production                                                             │  │  │
    │  │  └────────────────────────────────────────────────────────────────────────────────────>│  │
    │  │                                                                                      │  │
    │  │  → Blue-Green or Canary deployment strategy                                          │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Jenkins Pipeline (Pipeline as Code)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Jenkinsfile (Declarative Pipeline)                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    pipeline {
        agent any

        environment {
            DOCKER_REGISTRY = 'registry.example.com'
            IMAGE_NAME = 'myapp'
            GIT_CREDENTIALS = credentials('git-token')
        }

        stages {
            stage('Checkout') {
                steps {
                    git url: 'https://github.com/myorg/myapp.git',
                        branch: 'main',
                        credentialsId: 'git-token'
                }
            }

            stage('Build') {
                steps {
                    sh 'mvn clean package'
                    script {
                        docker.build("${IMAGE_NAME}:${BUILD_NUMBER}")
                    }
                }
            }

            stage('Test') {
                parallel {
                    stage('Unit Tests') {
                        steps {
                            sh 'mvn test'
                            publishTestResults testResultsPattern: '**/target/surefire-reports/*.xml'
                        }
                    }
                    stage('Integration Tests') {
                        steps {
                            sh 'mvn verify -P integration-test'
                        }
                    }
                }
            }

            stage('Code Quality') {
                steps {
                    withSonarQubeEnv('sonar-server') {
                        sh 'mvn sonar:sonar'
                    }
                    timeout(time: 10, unit: 'MINUTES') {
                        waitForQualityGate abortPipeline: true
                    }
                }
            }

            stage('Security Scan') {
                steps {
                    sh 'trivy image ${IMAGE_NAME}:${BUILD_NUMBER} --format sarif --output trivy-results.sarif'
                    archiveArtifacts artifacts: 'trivy-results.sarif'
                }
            }

            stage('Push Image') {
                when {
                    branch 'main'
                }
                steps {
                    script {
                        docker.image("${IMAGE_NAME}:${BUILD_NUMBER}")
                            .push("${BUILD_NUMBER}")
                        docker.image("${IMAGE_NAME}:${BUILD_NUMBER}")
                            .push('latest')
                    }
                }
            }

            stage('Deploy to Production') {
                when {
                    branch 'main'
                }
                input {
                    message 'Deploy to production?'
                    ok 'Yes, deploy'
                }
                steps {
                    sh 'helm upgrade --install myapp ./helm-chart --set image.tag=${BUILD_NUMBER}'
                }
            }
        }

        post {
            always {
                cleanWs()
            }
            success {
                emailext subject: "Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: "Build succeeded. See ${env.BUILD_URL}",
                    to: 'team@example.com'
            }
            failure {
                emailext subject: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: "Build failed. Fix required. See ${env.BUILD_URL}",
                    to: 'team@example.com'
            }
        }
    }
```

### GitOps (ArgoCD)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         GitOps Workflow (ArgoCD)                                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Architecture:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Git Repository (Single Source of Truth)                                                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  /manifests                                                                          │  │  │
    │  │    ├── deployment.yaml                                                               │  │  │
    │  │    ├── service.yaml                                                                  │  │  │
    │  │    ├── ingress.yaml                                                                  │  │  │
    │  │    └── configmap.yaml                                                                │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                                   │  │
    │            │ git push                                                                          │  │
    │            ▼                                                                                   │  │
    │  Git Repository                                                                            │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Pull Request: "Update deployment to v1.2.3"                                          │  │  │
    │  │  │  Changes:                                                                          │  │  │
    │  │  │  │  - image: registry.example.com/app:v1.2.3                                       │  │  │
    │  │  │  +  - image: registry.example.com/app:v1.2.4                                       │  │  │
    │  │  → Code review, automated tests (Kyverno validation)                                  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │ PR approved + merged                                                          │  │
    │            ▼                                                                                   │  │
    │  ArgoCD (GitOps Operator)                                                                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. Detects git changes (polling + webhook)                                           │  │  │
    │  │  2. Compares desired state (git) vs actual state (cluster)                            │  │  │
    │  │  3. Calculates diff (OAM - Object Application Management)                              │  │  │
    │  │  4. Applies changes to Kubernetes cluster                                             │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │ kubectl apply                                                                 │  │
    │            ▼                                                                                   │  │
    │  Kubernetes Cluster                                                                      │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Deployment: myapp (v1.2.4)                                                           │  │  │
    │  │  Pods: myapp-abc123, myapp-def456                                                      │  │  │
    │  │  → ArgoCD continuously monitors and auto-syncs                                         │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### CI/CD 도구 비교

| 도구 | 타입 | 장점 | 단점 | 사용처 |
|------|------|------|------|--------|
| **Jenkins** | Self-hosted | 유연함, 플러그인 | 관리 오버헤드 | 복잡한 파이프라인 |
| **GitHub Actions** | SaaS | Git 통합 | YAML 제한 | GitHub 프로젝트 |
| **GitLab CI** | SaaS/Self-hsted | 통합 | 성능 | GitLab 사용자 |
| **ArgoCD** | GitOps | K8s 네이티브 | K8s에 종속 | Kubernetes |

### 배포 전략

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Deployment Strategies                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. Blue-Green Deployment:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Traffic                               LB                                              │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Step 1: All traffic to Blue (v1.0)                                                  │  │  │
    │  │  ┌──────────┐                                                                          │  │  │
    │  │  │  Load    │  ────────────────────>  Blue (v1.0)                                  │  │  │
    │  │  │  Balancer │                                                                               │  │  │
    │  │  └──────────┘  (no traffic)         Green (v1.1) [deploying...]                       │  │  │
    │  │                                                                                      │  │  │
    │  │  Step 2: Deploy Green, health checks                                                  │  │  │
    │  │  Step 3: Switch traffic to Green                                                      │  │  │
    │  │  ┌──────────┐                                                                          │  │  │
    │  │  │  Load    │  ────────────────────>  Green (v1.1)                                  │  │  │
    │  │  │  Balancer │  (no traffic)         Blue (v1.0) [keep for rollback]                  │  │  │
    │  │  └──────────┘                                                                          │  │  │
    │  │  → Instant rollback if issues                                                          │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. Canary Deployment:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Step 1: 5% traffic to Canary (v1.1)                                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  Load    │  ── 95% ────────>  Stable (v1.0)                                     │  │  │
    │  │  │  Balancer │  ──  5% ────────>  Canary (v1.1)                                    │  │  │
    │  │  └──────────┘                                                                          │  │  │
    │  │                                                                                      │  │  │
    │  │  Step 2: Monitor metrics (error rate, latency)                                        │  │  │
    │  │  Step 3: Gradually increase to 25%, 50%, 100%                                         │  │  │
    │  │  → Safe rollback at any step                                                          │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Feature Flags

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Feature Flag Strategy                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Progressive Rollout:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Feature: "new-ui"                                                                      │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Day 1:  Internal users only (user.email like '%@company.com')                        │  │  │
    │  │  Day 3:  10% of users (random sampling)                                              │  │  │
    │  │  Day 5:  50% of users                                                                 │  │  │
    │  │  Day 7:  100% of users                                                                │  │  │
    │  │  → No deployment needed for rollout/rollback                                         │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 금융 서비스 CI/CD 파이프라인
**상황**: 마이크로서비스 50개, 엄격한 보안 요구
**판단**: Jenkins + ArgoCD + Vault

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Financial Services CI/CD Pipeline                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Requirements:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 50 microservices, 5 deploys/day average                                              │  │
    │  • Zero-downtime deployment                                                             │  │
    │  • Secret management (DB passwords, API keys)                                          │  │
    │  • Compliance audit (who deployed what when)                                            │  │
    │  • Automatic rollback on health check failure                                           │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Architecture:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Source Control                                                                      │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Monorepo: /services/{service-name}                                                │  │  │
    │  │  • Branch protection: require PR, require approvals                                  │  │  │
    │  │  • Automated checks: lint, unit tests, security scan before merge                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  2. CI Pipeline (Jenkins)                                                               │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Build Docker image, scan for vulnerabilities (Trivy)                              │  │  │
    │  │  • Sign image (Cosign)                                                               │  │  │
    │  │  • Run integration tests (Testcontainers)                                            │  │  │
    │  │  • Push signed image to registry                                                     │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  3. GitOps (ArgoCD)                                                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Git repo contains Kubernetes manifests                                             │  │  │
    │  │  • ArgoCD auto-syncs cluster state with git                                          │  │  │
    │  │  • Rollback: git revert                                                              │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  4. Secrets (Vault)                                                                     │  │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • External Secrets Operator reads from Vault                                        │  │  │
    │  │  • Secrets never stored in git                                                       │  │  │
    │  │  • Automatic rotation (DB passwords every 90 days)                                   │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  5. Observability                                                                       │  │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Prometheus: Request latency, error rate                                            │  │  │
    │  │  │  │  If error_rate > 5% for 5 min → Auto rollback                                   │  │  │
    │  │  │  │  If latency_p99 > 1s for 5 min → Auto rollback                                  │  │  │
    │  │  │  │  If health_check fails → Auto rollback                                         │  │  │
    │  │  │  │  Alert: Slack, PagerDuty                                                       │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### CI/CD 기대 효과

| 지표 | CI/CD 전 | CI/CD 후 | 개선 |
|------|----------|----------|------|
| **배포 시간** | 2시간 | 10분 | 92% |
| **배포 빈도** | 주1회 | 일5회 | 5x |
| **실패율** | 15% | 2% | 87% |
| **MTTR** | 4시간 | 30분 | 88% |

### 모범 사례

1. **Fast**: 파이프라인 < 10분
2. **Atomic**: 전체 성공/실패
3. **Idempotent**: 재실행 가능
4. **Observable**: 로그/메트릭

### 미래 전망

1. **AI/ML**: MLOps
2. **Progressive**: Feature flags
3. **Serverless**: Fn, Knative
4. **Self-service**: Internal Dev Platform

### ※ 참고 표준/가이드
- **DORA**: 4 Keys
- **GitOps**: OpenGitOps
- **Kubernetes**: Operators

---

## 📌 관련 개념 맵

- [컨테이너](./20_containers/46_containers.md) - Docker
- [Kubernetes](./21_kubernetes/47_kubernetes.md) - 배포
- [테스트](./22_testing/48_testing.md) - 자동화
