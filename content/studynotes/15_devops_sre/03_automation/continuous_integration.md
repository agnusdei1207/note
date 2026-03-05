+++
title = "지속적 통합 (CI, Continuous Integration)"
description = "다수 개발자의 코드를 수시로 병합하고 자동 빌드/테스트를 수행하는 실천법에 대한 심층 기술 백서"
date = 2024-05-15
[taxonomies]
tags = ["CI", "Continuous Integration", "Jenkins", "GitHub Actions", "Build Automation", "DevOps"]
+++

# 지속적 통합 (CI, Continuous Integration)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 지속적 통합(CI)은 개발팀 구성원들이 작업 결과를 **주기적으로(하루에도 여러 번) 메인 브랜치에 통합**하고, 각 통합 시마다 **자동화된 빌드와 테스트를 실행**하여 통합 오류를 최대한 조기에 발견하는 소프트웨어 개발 실천법입니다.
> 2. **가치**: CI는 "내 컴퓨터에서는 되는데" 문제를 근본적으로 해결하고, 병합 충돌을 조기에 발견하며, 코드 품질을 자동으로 검증하여 개발팀의 생산성과 제품 안정성을 동시에 향상시킵니다.
> 3. **융합**: Git 브랜치 전략, Pull Request 워크플로우, 정적 분석(SonarQube), 보안 스캔(SAST/SCA), 컨테이너 이미지 빌드와 결합하여 자동화된 품질 게이트(Quality Gate)를 구축합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**지속적 통합(Continuous Integration, CI)**은 Extreme Programming(XP)의 핵심 실천법 중 하나로, **개발자들이 자신의 변경사항을 중앙 코드베이스에 자주(최소 하루 1회 이상) 통합**하고, **각 통합 시마다 자동화된 빌드와 테스트를 실행**하여 통합 오류를 신속하게 탐지하고 수정하는 소프트웨어 개발 방법론입니다.

CI의 핵심 원칙:
1. **단일 소스 저장소(Single Source Repository)**: 모든 소스 코드가 버전 관리 시스템에 저장됩니다.
2. **자동화된 빌드(Automated Build)**: 단일 명령으로 전체 시스템을 빌드할 수 있어야 합니다.
3. **자동화된 테스트(Automated Tests)**: 빌드 후 자동으로 테스트 스위트가 실행됩니다.
4. **빈번한 통합(Frequent Integration)**: 모든 개발자가 최소 하루 1회 코드를 커밋합니다.
5. **빠른 피드백(Fast Feedback)**: 빌드/테스트 결과가 즉시 개발자에게 전달됩니다.

### 💡 2. 구체적인 일상생활 비유
**오케스트라 연습**을 상상해 보세요:
- **개별 연습(비-CI)**: 각 악기 연주자가 집에서 따로 연습합니다. 합주 때가 되어야 음이 안 맞는다는 걸 알죠.
- **지속적 통합(CI)**: 모든 연주자가 매일 합주실에 모여 **짧은 곡(short piece)을 함께 연주**합니다. 어느 악기가 음이 틀렸는지 즉시 알 수 있죠.

CI에서:
- **합주실** = CI 서버(Jenkins, GitHub Actions)
- **짧은 곡** = 자동화된 테스트
- **틀린 음** = 통합 오류(빌드 실패, 테스트 실패)
- **지휘자** = CI 파이프라인이 결과를 즉시 알림

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (통합 지옥, Integration Hell)**:
   과거 폭포수 모델에서는 개발자들이 각자 작업한 코드를 **프로젝트 마감 직전에 한 번에 통합**했습니다. 이때 발생하는 문제들:
   - **병합 충돌(Merge Conflict)**: 수천 개의 파일 충돌
   - **API 불일치**: A 팀이 변경한 API를 B 팀이 모름
   - **빌드 실패**: "누가 pom.xml을 바꿨어?"
   - **"Integration Hell"**: 통합에 수주~수개월 소요

2. **혁신적 패러다임 변화의 시작**:
   - **1991년**: Grady Booch가 "Continuous Integration" 용어 최초 사용.
   - **1996년**: Kent Beck의 Extreme Programming(XP)에서 CI를 핵심 실천법으로 정립.
   - **2001년**: CruiseControl이 최초의 오픈소스 CI 서버로 등장.
   - **2010년대**: Jenkins, Travis CI, CircleCI, GitHub Actions가 대중화.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   DevOps 시대에 CI는 선택이 아닌 필수입니다. 하루에 수백 번의 커밋이 이루어지는 환경에서, 각 커밋마다 자동으로 테스트하고 피드백하는 시스템 없이는 품질 유지가 불가능합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Source Control** | 코드 저장 및 버전 관리 | Git Hook으로 CI 트리거 | GitHub, GitLab, Bitbucket | 악보 보관함 |
| **CI Server** | 빌드/테스트 자동 실행 | Webhook 수신, Job 스케줄링, Executor 실행 | Jenkins, GitHub Actions, GitLab CI | 지휘자 |
| **Build Tool** | 소스 → 실행 가능한 아티팩트 변환 | 컴파일, 패키징, 의존성 해결 | Maven, Gradle, npm, webpack | 악기 조율사 |
| **Test Framework** | 자동화된 테스트 실행 | 단위/통합/E2E 테스트 실행 | JUnit, PyTest, Jest, Cypress | 음정 검사기 |
| **Artifact Repository** | 빌드 결과물 저장 | 버전별 아티팩트 관리, 캐싱 | Nexus, Artifactory, ECR | 악기 창고 |

### 2. 정교한 구조 다이어그램: CI 파이프라인 아키텍처

```text
=====================================================================================================
                    [ Continuous Integration Pipeline Architecture ]
=====================================================================================================

+-------------------------------------------------------------------------------------------+
|                              [ DEVELOPER WORKFLOW ]                                       |
|                                                                                           |
|   Developer                                                                               |
│      │                                                                                    |
│      │ git commit -m "feat: Add login feature"                                            |
│      │ git push origin feature/login                                                      |
│      ▼                                                                                    |
│   +------------------+                                                                    |
│   │ Git Repository   │                                                                    |
│   │ (GitHub/GitLab)  │                                                                    |
│   └────────┬─────────┘                                                                    |
│            │                                                                              |
│            │ Webhook Trigger (Push/PR Event)                                              |
│            ▼                                                                              |
+-------------------------------------------------------------------------------------------+
                                         │
                                         ▼
+-------------------------------------------------------------------------------------------+
|                              [ CI PIPELINE STAGES ]                                       |
|                                                                                           |
|  ┌─────────────────────────────────────────────────────────────────────────────────────┐  |
|  │ STAGE 1: CHECKOUT                                                                    │  |
|  │ ┌─────────────────────────────────────────────────────────────────────────────────┐ │  |
|  │ │ git clone --depth=1 https://github.com/org/repo.git                            │ │  |
|  │ │ git checkout feature/login                                                     │ │  |
|  │ └─────────────────────────────────────────────────────────────────────────────────┘ │  |
|  └─────────────────────────────────────────────────────────────────────────────────────┘  |
│                                         │                                                 |
│                                         ▼                                                 |
|  ┌─────────────────────────────────────────────────────────────────────────────────────┐  |
|  │ STAGE 2: DEPENDENCY RESOLUTION & BUILD                                              │  |
|  │ ┌─────────────────────────────────────────────────────────────────────────────────┐ │  |
|  │ │ # 의존성 캐시 복원                                                              │ │  |
|  │ │ - Restore ~/.m2/repository from cache                                          │ │  |
|  │ │                                                                                │ │  |
|  │ │ # 빌드 실행                                                                    │ │  |
|  │ │ $ ./mvnw clean package -DskipTests                                             │ │  |
|  │ │ [INFO] BUILD SUCCESS (Time: 45.123s)                                           │ │  |
|  │ │                                                                                │ │  |
|  │ │ # 아티팩트 생성: target/myapp-1.2.0-SNAPSHOT.jar                               │ │  |
|  │ └─────────────────────────────────────────────────────────────────────────────────┘ │  |
|  └─────────────────────────────────────────────────────────────────────────────────────┘  |
│                                         │                                                 |
│                                         ▼                                                 |
|  ┌─────────────────────────────────────────────────────────────────────────────────────┐  |
|  │ STAGE 3: AUTOMATED TESTING                                                          │  |
|  │ ┌─────────────────────────────────────────────────────────────────────────────────┐ │  |
|  │ │ $ ./mvnw test                                                                  │ │  |
|  │ │ ┌────────────────────────────────────────────────────────────────────────────┐  │ │  |
|  │ │ │ [TEST] UserServiceTest                                                     │  │ │  |
|  │ │ │   ✓ testCreateUser (15ms)                                                  │  │ │  |
|  │ │ │   ✓ testAuthenticateUser (23ms)                                            │  │ │  |
|  │ │ │   ✓ testPasswordHashing (8ms)                                              │  │ │  |
|  │ │ │                                                                            │  │ │  |
|  │ │ │ [TEST] IntegrationTest                                                     │  │ │  |
|  │ │ │   ✓ testDatabaseConnection (156ms)                                         │  │ │  |
|  │ │ │   ✓ testAPIEndpoint (234ms)                                                │  │ │  |
|  │ │ │                                                                            │  │ │  |
|  │ │ │ Tests run: 156, Failures: 0, Errors: 0, Skipped: 3                         │  │ │  |
|  │ │ │ Coverage: 85.2%                                                            │  │ │  |
|  │ │ └────────────────────────────────────────────────────────────────────────────┘  │ │  |
|  │ └─────────────────────────────────────────────────────────────────────────────────┘ │  |
|  └─────────────────────────────────────────────────────────────────────────────────────┘  |
│                                         │                                                 |
│                                         ▼                                                 |
|  ┌─────────────────────────────────────────────────────────────────────────────────────┐  |
|  │ STAGE 4: STATIC ANALYSIS & SECURITY SCAN                                            │  |
|  │ ┌─────────────────────────────────────────────────────────────────────────────────┐ │  |
|  │ │ # 정적 코드 분석 (SonarQube)                                                   │ │  |
|  │ │ Quality Gate: PASSED                                                           │ │  |
|  │ │ - Bugs: 0 | Vulnerabilities: 0 | Code Smells: 5                               │ │  |
|  │ │ - Coverage: 85.2% | Duplications: 1.2%                                        │ │  |
|  │ │                                                                                │ │  |
|  │ │ # 보안 스캔 (SAST/SCA)                                                         │ │  |
|  │ │ Snyk: No known vulnerabilities                                                │ │  |
|  │ │ Trivy: 0 CRITICAL, 0 HIGH issues                                              │ │  |
|  │ └─────────────────────────────────────────────────────────────────────────────────┘ │  |
|  └─────────────────────────────────────────────────────────────────────────────────────┘  |
│                                         │                                                 |
│                                         ▼                                                 |
|  ┌─────────────────────────────────────────────────────────────────────────────────────┐  |
|  │ STAGE 5: ARTIFACT PUBLISHING                                                        │  |
|  │ ┌─────────────────────────────────────────────────────────────────────────────────┐ │  |
|  │ │ # Docker 이미지 빌드                                                            │ │  |
|  │ │ $ docker build -t myapp:1.2.0-SNAPSHOT-abc123 .                                │ │  |
|  │ │ Successfully built abc123def456                                                │ │  |
|  │ │                                                                                │ │  |
|  │ │ # 이미지 푸시                                                                   │ │  |
|  │ │ $ docker push registry.company.com/myapp:1.2.0-SNAPSHOT-abc123                 │ │  |
|  │ └─────────────────────────────────────────────────────────────────────────────────┘ │  |
|  └─────────────────────────────────────────────────────────────────────────────────────┘  |
+-------------------------------------------------------------------------------------------+
                                         │
                                         ▼
+-------------------------------------------------------------------------------------------+
|                              [ FEEDBACK & NOTIFICATION ]                                  |
|                                                                                           |
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │ CI Result: ✅ SUCCESS                                                            │   │
│   │                                                                                  │   │
│   │ - Build Duration: 3m 45s                                                         │   │
│   │ - Test Results: 156 passed, 0 failed                                            │   │
│   │ - Coverage: 85.2%                                                                │   │
│   │ - Quality Gate: PASSED                                                           │   │
│   │                                                                                  │   │
│   │ Notify: Slack #dev-team, PR Status (✅), Email                                   │   │
│   └─────────────────────────────────────────────────────────────────────────────────┘   │
+-------------------------------------------------------------------------------------------+
```

### 3. 심층 동작 원리 (CI 파이프라인 실행 과정)

**1단계: 트리거 감지 (Trigger Detection)**
```yaml
# .github/workflows/ci.yml - GitHub Actions 트리거 설정
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  # cron 스케줄도 가능 (Nightly Build)
  schedule:
    - cron: '0 2 * * *'  # 매일 오전 2시
```

**2단계: 워크플로우 실행 환경 구성**
```yaml
jobs:
  build-and-test:
    runs-on: ubuntu-latest  # 실행 환경 (Runner)

    # 매트릭스 빌드 (여러 버전 동시 테스트)
    strategy:
      matrix:
        java-version: [17, 21]
        node-version: [18, 20]

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # 전체 히스토리 (SonarQube용)
```

**3단계: 의존성 캐싱 및 복원**
```yaml
      - name: Cache Maven packages
        uses: actions/cache@v4
        with:
          path: ~/.m2/repository
          key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
          restore-keys: |
            ${{ runner.os }}-maven-
```

**4단계: 빌드 및 테스트 실행**
```yaml
      - name: Build with Maven
        run: ./mvnw clean package -DskipTests

      - name: Run Tests
        run: ./mvnw test

      - name: Generate Coverage Report
        run: ./mvnw jacoco:report
```

**5단계: 정적 분석 및 품질 게이트**
```yaml
      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

      - name: Quality Gate Check
        uses: SonarSource/sonarqube-quality-gate-action@master
        timeout-minutes: 5
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

**6단계: 아티팩트 생성 및 저장**
```yaml
      - name: Build Docker Image
        run: |
          docker build -t ${{ secrets.REGISTRY }}/myapp:${{ github.sha }} .
          docker push ${{ secrets.REGISTRY }}/myapp:${{ github.sha }}

      - name: Upload Build Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: myapp-jar
          path: target/*.jar
          retention-days: 30
```

### 4. 실무 코드 예시 (Jenkins Pipeline)

```groovy
// Jenkinsfile - 선언적 파이프라인
pipeline {
    agent {
        kubernetes {
            yaml '''
            apiVersion: v1
            kind: Pod
            spec:
              containers:
              - name: maven
                image: maven:3.9-eclipse-temurin-17
                command: ['cat']
                tty: true
                resources:
                  limits:
                    memory: "4Gi"
                    cpu: "2"
              - name: docker
                image: docker:24-cli
                command: ['cat']
                tty: true
                volumeMounts:
                - name: docker-sock
                  mountPath: /var/run/docker.sock
              volumes:
              - name: docker-sock
                hostPath:
                  path: /var/run/docker.sock
            '''
        }
    }

    environment {
        REGISTRY = 'registry.company.com'
        IMAGE_NAME = 'myapp'
        SONAR_TOKEN = credentials('sonar-token')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git rev-parse --short HEAD > .git/commit-id'
                script {
                    env.COMMIT_ID = readFile('.git/commit-id').trim()
                }
            }
        }

        stage('Build') {
            steps {
                container('maven') {
                    sh 'mvn clean package -DskipTests'
                }
            }
            post {
                success {
                    archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
                }
            }
        }

        stage('Test') {
            steps {
                container('maven') {
                    sh 'mvn test'
                }
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                    publishCoverage adapters: [jacocoAdapter('target/site/jacoco/jacoco.xml')]
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                container('maven') {
                    withSonarQubeEnv('sonar-server') {
                        sh 'mvn sonar:sonar -Dsonar.login=$SONAR_TOKEN'
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Security Scan') {
            steps {
                container('maven') {
                    sh 'mvn dependency-check:check'
                }
                // Trivy 파일 시스템 스캔
                sh 'trivy fs --severity HIGH,CRITICAL --exit-code 1 .'
            }
        }

        stage('Build & Push Image') {
            steps {
                container('docker') {
                    withCredentials([usernamePassword(credentialsId: 'registry-creds',
                                                     usernameVariable: 'DOCKER_USER',
                                                     passwordVariable: 'DOCKER_PASS')]) {
                        sh """
                            docker login ${REGISTRY} -u ${DOCKER_USER} -p ${DOCKER_PASS}
                            docker build -t ${REGISTRY}/${IMAGE_NAME}:${COMMIT_ID} .
                            docker push ${REGISTRY}/${IMAGE_NAME}:${COMMIT_ID}
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            slackSend(color: 'good',
                     message: "✅ CI 성공: ${env.JOB_NAME} #${env.BUILD_NUMBER}\n커밋: ${env.COMMIT_ID}")
        }
        failure {
            slackSend(color: 'danger',
                     message: "❌ CI 실패: ${env.JOB_NAME} #${env.BUILD_NUMBER}\n담당자: @developer")
        }
    }
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. CI 도구 비교표

| 평가 지표 | Jenkins | GitHub Actions | GitLab CI | CircleCI | Travis CI |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **호스팅** | Self-hosted/Cloud | Cloud | Self-hosted/Cloud | Cloud | Cloud |
| **설정 방식** | Jenkinsfile (Groovy) | YAML | .gitlab-ci.yml | YAML | YAML |
| **학습 곡선** | 높음 | 낮음 | 중간 | 낮음 | 낮음 |
| **확장성** | 매우 높음 | 중간 | 높음 | 높음 | 중간 |
| **플러그인** | 1,800+ | Marketplace | Built-in | Orbs | Add-ons |
| **비용** | 무료 | 무료/유료 | 무료/유료 | 유료 | 유료 |
| **GitHub 통합** | 플러그인 필요 | 네이티브 | 지원 | 지원 | 지원 |

### 2. CI 단계별 모범 사례

| 단계 | 모범 사례 | 안티패턴 |
| :--- | :--- | :--- |
| **빌드** | 증분 빌드, 의존성 캐싱, 병렬 빌드 | 매번 전체 재빌드 |
| **테스트** | 테스트 병렬 실행, 실패 시 스크린샷 캡처 | 순차 실행, 긴 테스트 |
| **정적 분석** | PR에 댓글로 결과 표시 | 보고서만 생성, 피드백 없음 |
| **보안 스캔** | 빌드 단계에 통합, 실패 시 차단 | 배포 전에만 스캔 |
| **아티팩트** | 불변 태그(sha), 서명 | latest 태그만 사용 |

### 3. 과목 융합 관점 분석

**CI + 테스트 자동화**
- TDD(테스트 주도 개발)와 CI가 결합하여 모든 커밋이 테스트됩니다.
- 커버리지 80% 이상을 품질 게이트로 설정합니다.

**CI + 보안 (DevSecOps)**
- SAST(정적 보안 분석)가 CI 파이프라인에 통합됩니다.
- SCA(의존성 취약점 스캔)가 모든 빌드에서 실행됩니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] CI 파이프라인이 너무 느린 경우 (30분 이상)**
- **문제점**: PR 피드백이 30분 이상 걸려 개발자 생산성 저하.
- **기술사 판단**: **CI 파이프라인 최적화**.
  1. 의존성 캐싱 적용 (50% 시간 단축).
  2. 테스트 병렬 실행 (컴퓨팅 리소스 추가).
  3. 증분 테스트 (변경된 코드만 테스트).
  4. 목표: 10분 이내 피드백.

**[상황 B] "내 컴퓨터에서는 되는데 CI에서는 실패"**
- **문제점**: 로컬과 CI 환경 차이로 인한 불일치.
- **기술사 판단**: **환경 일치 및 컨테이너화**.
  1. Docker 컨테이너에서 로컬 빌드 실행.
  2. CI Runner와 동일한 이미지 사용.
  3. 개발 환경 표준화 (devcontainer).

### 2. CI 구축 체크리스트

**필수 체크리스트**
- [ ] 모든 브랜치에 대해 CI가 실행되는가?
- [ ] 빌드 실패 시 즉시 알림이 발송되는가?
- [ ] 테스트 커버리지가 측정되는가?
- [ ] 정적 분석이 자동 실행되는가?
- [ ] 아티팩트가 버전 관리되는가?

**고급 체크리스트**
- [ ] 매트릭스 빌드(여러 OS/버전)가 지원되는가?
- [ ] 의존성 캐싱이 적용되는가?
- [ ] 병렬 실행이 가능한가?
- [ ] 보안 스캔(SAST/SCA)이 통합되는가?

### 3. 안티패턴 (Anti-patterns)

**안티패턴 1: CI 무시 (Breaking the Build)**
- 빌드가 깨져도 계속 커밋.
- **해결**: Main 브랜치 보호, 실패 시 PR 병합 차단.

**안티패턴 2: 테스트 없는 CI**
- 빌드만 하고 테스트는 안 함.
- **해결**: 테스트 커버리지 게이트 적용.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 (AS-IS) | 도입 후 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **통합 주기** | 주 1회 또는 월 1회 | 하루 수십 회 | **100배 증가** |
| **버그 발견 시점** | QA 단계 (수주 후) | 커밋 직후 (수분 내) | **95% 조기 발견** |
| **빌드 재현성** | 50% (환경 의존) | 100% (자동화) | **100% 보장** |
| **개발자 생산성** | 디버깅에 40% 시간 | 기능 개발에 80% 시간 | **2배 향상** |

### 2. 미래 전망 및 진화 방향

**AI 기반 CI 최적화**
- AI가 테스트를 지능적으로 선택하여 실행 (Predictive Test Selection).
- 실패 원인을 자동으로 분석하여 수정 제안.

**GitOps 통합**
- CI가 GitOps와 완전히 통합되어 배포까지 자동화.
- CI/CD 경계가 모호해짐.

### 3. 참고 표준/가이드
- **Martin Fowler: Continuous Integration (2006)**: CI 원칙의 바이블
- **Extreme Programming Explained (Kent Beck)**: CI의 원조
- **The DevOps Handbook**: CI/CD 전체 가이드
- **GitHub Actions Documentation**: 모범 사례

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **[지속적 전달/배포 (CD)](./continuous_deployment.md)**: CI의 다음 단계인 자동 배포
- **[Git 브랜치 전략](@/studynotes/15_devops_sre/03_automation/git_branching_strategies.md)**: CI와 연동되는 브랜치 관리
- **[Pull Request](@/studynotes/15_devops_sre/03_automation/pull_request.md)**: CI가 실행되는 협업 메커니즘
- **[테스트 자동화](./test_automation.md)**: CI의 핵심 구성 요소

---

## 👶 어린이를 위한 3줄 비유 설명
1. CI는 **'매일 하는 오케스트라 합주'**예요. 각자 연습한 걸 합쳐보고 **'음이 안 맞는 곳'**을 즉시 찾아내죠.
2. 합주에서 음이 틀리면 **'바로 고쳐야 해요!'**라고 지휘자가 말해줘요. 한 달 뒤에 알려주면 너무 늦으니까요.
3. 그래서 모든 악기가 **'항상 화음이 맞는'** 상태로 유지돼요. 연주회(배포) 날 걱정 없이요!
