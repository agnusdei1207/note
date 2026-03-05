+++
title = "풀 리퀘스트 (Pull Request) / 머지 리퀘스트 (Merge Request)"
description = "코드 병합 전 동료 검토를 요청하는 프로세스에 대한 심층 기술 백서"
date = 2024-05-15
[taxonomies]
tags = ["Pull Request", "Merge Request", "Code Review", "Git", "Collaboration", "CI/CD"]
+++

# 풀 리퀘스트 (Pull Request) / 머지 리퀘스트 (Merge Request)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 풀 리퀘스트(PR)는 소스 브랜치의 변경사항을 타겟 브랜치에 병합하기 전, 코드 리뷰와 자동화된 검증(CI)을 거쳐 승인을 받는 협업 프로세스로, "모든 코드 변경은 검토된다"는 품질 보증의 핵심 메커니즘입니다.
> 2. **가치**: PR은 지식 공유, 버그 조기 발견, 코딩 표준 준수, 보안 취약점 차단을 가능하게 하며, "인간의 지혜 + 기계의 자동화"가 결합된 품질 게이트(Quality Gate)입니다.
> 3. **융합**: CI/CD 파이프라인, 정적 분석 도구(SonarQube), 보안 스캐너(SAST/DAST), 자동화된 테스트와 결합하여 PR이 병합 게이트(Merge Gate)로 작동합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**풀 리퀘스트(Pull Request, PR)**는 Git 기반 협업 플랫폼(GitHub, Bitbucket)에서 사용되는 용어로, **소스 브랜치(Feature Branch)의 변경사항을 타겟 브랜치(Main/Develop)로 "끌어와(Pull) 병합해 달라"고 요청하는 메커니즘**입니다.

**머지 리퀘스트(Merge Request, MR)**는 GitLab에서 사용되는 동일한 개념으로, **"병합(Merge)을 요청한다"**는 의미입니다. 기능적으로 PR과 동일합니다.

PR/MR의 핵심 구성 요소:
- **소스 브랜치(Source Branch)**: 변경사항이 있는 브랜치 (예: feature/login)
- **타겟 브랜치(Target Branch)**: 병합될 브랜치 (예: main, develop)
- **커밋(Commits)**: 소스 브랜치의 모든 커밋 목록
- **변경 파일(Changed Files)**: 추가/수정/삭제된 파일의 Diff
- **코드 리뷰어(Reviewers)**: 승인 권한이 있는 검토자
- **CI 상태(CI Status)**: 자동화된 테스트/빌드 결과

### 💡 2. 구체적인 일상생활 비유
**학교 과제 제출 시스템**을 상상해 보세요:
- **학생(개발자)**: 과제(코드)를 작성해서 선생님께 제출합니다.
- **선생님(리뷰어)**: 과제를 검토하고 "잘했어요 ✓" 또는 "이 부분 수정해 주세요" 피드백을 줍니다.
- **자동 채점 시스템(CI)**: 과제를 제출하면 자동으로 맞춤법 검사, 플래그어니즘 체크를 수행합니다.
- **최종 제출(병합)**: 선생님이 승인하면 과제가 공식 기록에 등록됩니다.

PR은 이 "과제 제출 → 검토 → 수정 → 승인 → 등록" 과정을 코드에 적용한 것입니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (비공개 코드 변경)**:
   과거에는 개발자가 메인 코드베이스에 직접 커밋(push)했습니다. 다른 사람이 코드를 검토할 기회가 없었고, 버그나 보안 취약점이 포함된 코드가 그대로 프로덕션에 배포되는 일이 빈번했습니다.

2. **혁신적 패러다임 변화의 시작**:
   - **2008년**: GitHub가 Pull Request 기능을 도입하여 오픈소스 협업 방식을 혁신했습니다. 누구나 프로젝트에 기여할 수 있지만, 관리자의 승인 없이는 병합되지 않는 구조를 만들었습니다.
   - **2011년**: GitLab이 Merge Request를 도입하며 코드 리뷰 워크플로우를 더욱 강화했습니다.
   - **2010년대 후반**: CI/CD 통합이 표준화되어 PR 생성 시 자동으로 테스트/빌드가 실행됩니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   DevSecOps 시대에 PR은 단순한 코드 리뷰를 넘어 보안 게이트(Security Gate) 역할을 합니다. SAST, SCA, 시크릿 스캔이 PR 단계에서 자동 실행되어 취약점이 있는 코드가 메인 브랜치에 들어가는 것을 차단합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Diff 뷰어** | 변경 전후 코드 비교 | Unified Diff 알고리즘으로 라인별 변경 표시 | GitHub, GitLab UI | 교정 부호가 표시된 원고 |
| **인라인 코멘트** | 코드 라인별 피드백 | 특정 라인에 스레드 형태로 댓글 작성 | GitHub, GitLab | 교정 메모 |
| **승인(Approval)** | 병합 승인 투표 | 리뷰어가 "Approve" 버튼 클릭 | Branch Protection Rules | 합격 판정 |
| **병합 조건(Merge Conditions)** | 병합 전 필수 조건 | CI 통과, 승인 N명, 충돌 없음 검증 | GitHub Checks, GitLab Pipelines | 졸업 요건 |
| **CI 통합** | 자동화된 검증 실행 | Webhook으로 CI 서버 트리거 | Jenkins, GitHub Actions, GitLab CI | 자동 채점 시스템 |

### 2. 정교한 구조 다이어그램: Pull Request 워크플로우

```text
=====================================================================================================
                    [ Pull Request Complete Workflow Architecture ]
=====================================================================================================

+-----------------------------------------------------------------------------------+
|                         [ DEVELOPER WORKFLOW ]                                    |
|                                                                                   |
|  1. 코드 작성                                                                      |
|  +------------------+                                                             |
|  | git checkout -b  |  → git add .  →  git commit  →  git push                   |
|  | feature/login    |                                                             |
|  +------------------+                                                             |
|                                                                                   |
+-----------------------------------------------------------------------------------+
                                        │
                                        │ PR 생성 (GitHub/GitLab UI)
                                        ▼
+-----------------------------------------------------------------------------------+
|                         [ PULL REQUEST CREATION ]                                 |
|                                                                                   |
|  +---------------------------------------------------------------------------+   |
|  | PR Title: "feat: Add user authentication with OAuth2"                     |   |
|  | Description:                                                              |   |
|  | - OAuth2 Google 로그인 구현                                               |   |
|  | - JWT 토큰 발급 로직 추가                                                 |   |
|  | - 테스트 코드 작성 완료                                                   |   |
|  |                                                                           |   |
|  | Source: feature/login  ──────────────>  Target: main                      |   |
|  |                                                                           |   |
|  | Commits: 5    Files Changed: 12    +450 -120                              |   |
|  +---------------------------------------------------------------------------+   |
|                                                                                   |
+-----------------------------------------------------------------------------------+
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
+-----------------------+  +-----------------------+  +-----------------------+
|   [ CI PIPELINE ]     |  |   [ CODE REVIEW ]    |  |  [ SECURITY SCAN ]    |
|                       |  |                       |  |                       |
|  ✓ Build             |  |  Reviewer: @senior   |  |  ✓ SAST (Semgrep)    |
|  ✓ Unit Tests        |  |                       |  |  ✓ SCA (Snyk)        |
|  ✓ Integration Tests |  |  Comments:            |  |  ✓ Secret Scan       |
|  ✓ Linting           |  |  "이 부분 SQL 인젝션  |  |  ✓ Container Scan    |
|  ✓ Code Coverage     |  |   위험 있어요!"       |  |                       |
|                       |  |                       |  |                       |
|  Status: ✅ PASSED    |  |  Status: 🔄 PENDING  |  |  Status: ✅ PASSED    |
+-----------------------+  +-----------------------+  +-----------------------+
                    │                   │                   │
                    └───────────────────┼───────────────────┘
                                        │
                                        ▼ 모든 조건 충족
+-----------------------------------------------------------------------------------+
|                         [ MERGE CONDITIONS CHECK ]                                |
|                                                                                   |
|  +---------------------------------------------------------------------------+   |
|  | Branch Protection Rules:                                                  |   |
|  |                                                                           |   |
|  | ✓ Require CI to pass before merging                                       |   |
|  | ✓ Require at least 1 approval                                             |   |
|  | ✓ Require branches to be up to date                                       |   |
|  | ✓ Require conversation resolution                                         |   |
|  | ✓ Restrict who can push to matching branches                              |   |
|  |                                                                           |   |
|  | Current Status:                                                           |   |
|  | ✅ CI/CD: All checks passed                                               |   |
|  | ✅ Reviews: Approved by @senior-dev, @security-team                       |   |
|  | ✅ Security: No vulnerabilities found                                      |   |
|  | ✅ Conflicts: No merge conflicts                                           |   |
|  +---------------------------------------------------------------------------+   |
|                                                                                   |
+-----------------------------------------------------------------------------------+
                                        │
                                        │ Merge 버튼 클릭
                                        ▼
+-----------------------------------------------------------------------------------+
|                         [ MERGE EXECUTION ]                                       |
|                                                                                   |
|  +---------------------------------------------------------------------------+   |
|  | Merge Strategy: Squash and Merge                                          |   |
|  |                                                                           |   |
|  | feature/login ────────> main                                             |   |
|  |                                                                           |   |
|  | ✓ 5 commits squashed into 1                                              |   |
|  | ✓ Branch protection rules satisfied                                       |   |
|  | ✓ Merge commit created: abc1234                                           |   |
|  | ✓ Feature branch deleted (auto-cleanup)                                   |   |
|  | ✓ CD pipeline triggered for deployment                                    |   |
|  +---------------------------------------------------------------------------+   |
|                                                                                   |
+-----------------------------------------------------------------------------------+
                                        │
                                        ▼
+-----------------------------------------------------------------------------------+
|                         [ POST-MERGE ACTIONS ]                                    |
|                                                                                   |
|  +---------------------------------------------------------------------------+   |
|  | 1. Notify team (Slack: #deployments)                                      |   |
|  | 2. Update JIRA ticket status                                              |   |
|  | 3. Trigger CD pipeline (ArgoCD sync)                                      |   |
|  | 4. Generate changelog entry                                               |   |
|  | 5. Update documentation (if needed)                                        |   |
|  +---------------------------------------------------------------------------+   |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

### 3. 심층 동작 원리 (PR 수명 주기)

**1단계: PR 생성 (Creation)**
```bash
# 개발자가 피처 브랜치에서 작업 완료 후 푸시
git push origin feature/user-authentication

# GitHub CLI로 PR 생성
gh pr create \
  --title "feat: Add user authentication with OAuth2" \
  --body "$(cat <<'EOF'
## 변경 사항
- OAuth2 Google 로그인 구현
- JWT 토큰 발급 로직 추가
- 단위 테스트 및 통합 테스트 작성

## 테스트 방법
1. `/login` 엔드포인트 호출
2. Google OAuth2 리다이렉트 확인
3. JWT 토큰 발급 검증

## 관련 이슈
Closes #123
EOF
)" \
  --base main \
  --assignee @me \
  --reviewer @senior-dev,@security-team
```

**2단계: CI 자동 실행 (Automated Checks)**
```yaml
# .github/workflows/pr-checks.yml
name: PR Validation

on:
  pull_request:
    branches: [ main, develop ]

jobs:
  # 1. 빌드 및 테스트
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm ci && npm test

  # 2. 정적 분석
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: ESLint
        run: npm run lint

  # 3. 보안 스캔
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

  # 4. 코드 품질 게이트
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

**3단계: 코드 리뷰 (Code Review)**
```markdown
<!-- 리뷰어의 인라인 코멘트 예시 -->

**src/auth/oauth.js:45**
```javascript
// ❌ 리뷰어 코멘트
const token = jwt.sign({ userId }, 'hardcoded-secret');
```
> @developer 이 하드코딩된 시크릿은 보안 위험입니다.
> 환경 변수(`process.env.JWT_SECRET`)를 사용해 주세요.

**src/auth/oauth.js:78**
```javascript
// ✓ 수정 후
const token = jwt.sign({ userId }, process.env.JWT_SECRET, { expiresIn: '1h' });
```

**4단계: 승인 및 병합 (Approval & Merge)**
```bash
# 리뷰어가 PR 승인
gh pr review 123 --approve --body "LGTM! 코드 품질이 좋고 테스트 커버리지도 충분합니다."

# 모든 조건 충족 후 병합
gh pr merge 123 --squash --delete-branch
```

### 4. 실무 코드 예시 (PR 템플릿 및 자동화)

```markdown
<!-- .github/PULL_REQUEST_TEMPLATE.md -->
## PR 유형
- [ ] 기능 추가 (Feature)
- [ ] 버그 수정 (Bugfix)
- [ ] 리팩토링 (Refactor)
- [ ] 문서 수정 (Documentation)
- [ ] 기타 (Other)

## 변경 사항 요약
<!-- 이 PR이 무엇을 변경하는지 간략히 설명 -->

## 관련 이슈
<!-- Closes #123 형식으로 작성 -->

## 테스트 방법
1.
2.
3.

## 체크리스트
- [ ] 단위 테스트를 작성했습니다
- [ ] 로컬에서 모든 테스트가 통과했습니다
- [ ] 코드 스타일 검사를 통과했습니다 (lint)
- [ ] 관련 문서를 업데이트했습니다

## 스크린샷 (UI 변경이 있는 경우)
<!-- Before/After 스크린샷 -->

## 리뷰어에게 요청 사항
<!-- 특히 집중해서 봐주었으면 하는 부분 -->
```

```yaml
# .github/workflows/auto-merge.yml
# 조건 충족 시 자동 병합
name: Auto Merge

on:
  pull_request_review:
    types: [submitted]

jobs:
  auto-merge:
    if: github.event.review.state == 'approved'
    runs-on: ubuntu-latest
    steps:
      - name: Check PR conditions
        id: check
        uses: actions/github-script@v7
        with:
          script: |
            const pr = await github.rest.pulls.get({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number
            });

            // CI 통과 확인
            const checks = await github.rest.checks.listForRef({
              owner: context.repo.owner,
              repo: context.repo.repo,
              ref: pr.data.head.sha
            });

            const allPassed = checks.data.check_runs.every(
              run => run.status === 'completed' && run.conclusion === 'success'
            );

            return allPassed;

      - name: Enable auto-merge
        if: steps.check.outputs.result == 'true'
        run: gh pr merge --auto --squash "${{ github.event.pull_request.number }}"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. PR/MR 플랫폼 비교표

| 기능 | GitHub (PR) | GitLab (MR) | Bitbucket (PR) | Azure DevOps (PR) |
| :--- | :--- | :--- | :--- | :--- |
| **인라인 코멘트** | ✓ | ✓ | ✓ | ✓ |
| **멀티 레벨 승인** | ✓ (CODEOWNERS) | ✓ | ✓ | ✓ |
| **CI 통합** | GitHub Actions | GitLab CI | Pipelines | Azure Pipelines |
| **자동 병합** | ✓ (Auto-merge) | ✓ (Merge trains) | ✓ | ✓ |
| **Draft PR** | ✓ | ✓ (WIP) | ✓ | ✓ |
| **리뷰 요청 자동화** | ✓ | ✓ | ✓ | ✓ |
| **병합 전략** | Merge, Squash, Rebase | Merge, Squash | Merge, Squash, Rebase | Merge, Squash |

### 2. 병합 전략 비교

| 전략 | 설명 | 장점 | 단점 | 적합한 상황 |
| :--- | :--- | :--- | :--- | :--- |
| **Merge Commit** | 모든 커밋을 보존하며 병합 커밋 생성 | 히스토리 보존, 병렬 작업 시각화 | 히스토리 복잡 | 장기 브랜치, Git Flow |
| **Squash and Merge** | 모든 커밋을 하나로 합쳐 병합 | 깔끔한 히스토리 | 개별 커밋 정보 손실 | GitHub Flow, 단기 브랜치 |
| **Rebase and Merge** | 커밋을 리베이스 후 선형 병합 | 선형 히스토리 | 리베이스 위험 | Trunk-Based Development |

### 3. 과목 융합 관점 분석

**PR + 보안 (DevSecOps)**
- SAST(정적 보안 분석)가 PR 생성 시 자동 실행됩니다.
- 시크릿 스캔(Git Secrets, TruffleHog)이 API 키 노출을 탐지합니다.
- SCA(Software Composition Analysis)가 취약한 의존성을 차단합니다.

**PR + AI (AI-Assisted Review)**
- GitHub Copilot이 자동으로 코드 리뷰 코멘트를 생성합니다.
- AI가 보일러플레이트 코드, 성능 이슈, 보안 취약점을 자동 탐지합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] PR 리뷰가 너무 오래 걸리는 경우**
- **문제점**: PR이 생성된 후 평균 3일이 지나야 리뷰가 완료됨. 개발 속도 저하.
- **기술사 판단**: **리뷰 SLA 및 자동화된 리뷰 도입**.
  1. 24시간 내 1차 리뷰, 48시간 내 최종 승인을 SLA로 설정.
  2. AI 기반 자동 리뷰(GitHub Copilot)로 사전 검증.
  3. "작은 PR" 문화 장려 (200라인 이하 권장).

**[상황 B] 대형 PR로 인한 리뷰 품질 저하**
- **문제점**: 5000라인 변경 PR은 리뷰어가 제대로 검토하지 못함.
- **기술사 판단**: **PR 크기 제한 및 분할 전략**.
  1. PR 크기 가이드라인 설정 (400라인 권장, 1000라인 상한).
  2. 대형 기능은 여러 개의 작은 PR로 분할.
  3. 리팩토링은 기능 변경과 분리하여 별도 PR로.

### 2. PR 관리 체크리스트

**품질 체크리스트**
- [ ] 모든 PR에 CI 파이프라인이 실행되는가?
- [ ] 최소 1명 이상의 승인이 필요한가?
- [ ] 보안 스캔(SAST/SCA)이 자동 실행되는가?
- [ ] 대화형 스레드가 모두 해결되어야 병합되는가?

**문화 체크리스트**
- [ ] PR 리뷰가 "비난"이 아닌 "지식 공유"로 인식되는가?
- [ ] 리뷰어에게 충분한 컨텍스트가 제공되는가?
- [ ] Draft PR을 통해 조기 피드백을 받는가?

### 3. 안티패턴 (Anti-patterns)

**안티패턴 1: LGTM 스팸 (Lazy Review)**
- 내용을 보지 않고 "Looks Good To Me" 승인.
- **해결**: 리뷰어 할당 로테이션, AI 기반 리뷰 품질 측정.

**안티패턴 2: 자신의 PR을 직접 승인**
- 자신이 작성한 PR을 스스로 승인하고 병합.
- **해결**: Branch Protection Rule로 자신의 PR 승인 불가 설정.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 (AS-IS) | 도입 후 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **버그 조기 발견율** | 프로덕션에서 60% 발견 | PR 단계에서 85% 발견 | **42% 향상** |
| **코드 품질** | 정적 분석 점수 C | 정적 분석 점수 A | **2등급 향상** |
| **지식 공유** | 팀 내 30%만 코드 이해 | 팀 내 90%가 코드 이해 | **3배 향상** |
| **보안 취약점** | 분기별 50건 발견 | 월 5건 미만 | **90% 감소** |

### 2. 미래 전망 및 진화 방향

**AI 기반 자동 코드 리뷰**
- AI가 PR을 자동으로 분석하여 버그, 성능 이슈, 보안 취약점을 탐지합니다.
- 자동 수정 제안(Auto-fix)이 적용됩니다.

**자동화된 병합 트레인 (Merge Trains)**
- 여러 PR을 자동으로 큐에 넣고 순차적으로 병합합니다.
- GitLab의 Merge Trains 기능이 이미 구현되어 있습니다.

### 3. 참고 표준/가이드
- **GitHub Flow Guide**: PR 기반 워크플로우 표준
- **Google Engineering Practices**: 코드 리뷰 가이드라인
- **Conventional Commits**: 커밋 메시지 표준
- **The Art of Code Review**: 효과적인 코드 리뷰 방법론

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **[Git 브랜치 전략](@/studynotes/15_devops_sre/03_automation/git_branching_strategies.md)**: PR이 병합되는 브랜치 구조
- **[CI/CD 파이프라인](@/studynotes/15_devops_sre/03_automation/cicd_gitops.md)**: PR 생성 시 자동 실행되는 검증 시스템
- **[코드 리뷰](./code_review.md)**: PR의 핵심 활동인 동료 검토 프로세스
- **[DevSecOps](@/studynotes/15_devops_sre/01_sre/devsecops.md)**: PR 단계에서 보안을 검증하는 실천법

---

## 👶 어린이를 위한 3줄 비유 설명
1. PR은 **'과제 제출함'**이에요. 친구들이 과제를 다 했으면 **'선생님(리뷰어)'**께 검사받으러 가죠.
2. 선생님은 과제를 보고 **'이 부분은 틀렸어요'** 또는 **'잘했어요!'**라고 말해줘요. 고친 후에 다시 보낼 수도 있어요.
3. 모든 선생님이 **'합격!'**이라고 하면 과제가 **'학교 게시판(main 브랜치)'**에 올라가서 모두가 볼 수 있게 돼요!
