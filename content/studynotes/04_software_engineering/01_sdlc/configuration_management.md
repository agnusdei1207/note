+++
title = "소프트웨어 형상 관리 (Software Configuration Management)"
date = 2024-05-24
description = "소프트웨어 변경 사항을 체계적으로 식별, 통제, 기록, 감사하는 품질 관리 체계"
weight = 35
+++

# 소프트웨어 형상 관리 (Software Configuration Management, SCM)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 형상 관리(SCM)는 소프트웨어 개발 과정에서 발생하는 **모든 변경 사항을 식별(Identification), 통제(Control), 기록(Status Accounting), 감사(Audit)**하여, 언제든 특정 시점의 시스템 상태를 **재현할 수 있도록 보장**하는 체계입니다.
> 2. **가치**: 무분별한 변경으로 인한 혼선을 방지하고, **변경의 추적성(Traceability)**을 확보하며, **기준선(Baseline)을 통한 버전 관리**로 소프트웨어 무결성을 보장합니다.
> 3. **융합**: Git/GitHub 중심의 분산 버전 관리, CI/CD 파이프라인과 결합하여 **DevOps의 핵심 인프라**로 진화했으며, IaC(Infrastructure as Code)로 영역이 확장되었습니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의
형상 관리(Configuration Management)는 소프트웨어의 **형상 항목(Configuration Item, CI)**을 체계적으로 관리하는 활동입니다. 형상 항목이란 변경이 발생할 수 있는 모든 산출물을 의미하며, 소스코드, 문서, 테스트 케이스, 실행 파일 등을 포함합니다.

**형상 관리의 4대 활동 (IEEE 828)**:
1. **형상 식별 (Identification)**: 관리 대상 항목 선정 및 명명
2. **형상 통제 (Control)**: 변경 요청 검토 및 승인/반려
3. **형상 기록 (Status Accounting)**: 변경 이력 및 상태 기록
4. **형상 감사 (Audit)**: 무결성 및 일관성 검증

### 💡 일상생활 비유: 도서관의 도서 관리 시스템
형상 관리는 도서관에서 책을 관리하는 것과 유사합니다.

```
[도서관 관리]               [형상 관리]
책 분류 및 등록          -->  형상 식별 (Identification)
대출/반납 승인           -->  형상 통제 (Control)
대출 이력 기록           -->  형상 기록 (Status Accounting)
도서 상태 점검           -->  형상 감사 (Audit)

[도서관 사서] = CCB (Configuration Control Board)
[책의 고유 번호] = 형상 항목 ID (CI ID)
[책의 현재 위치] = 기준선 (Baseline)
```

도서관에서는 책이 언제, 누구에 의해, 어디로 이동했는지 모두 기록합니다. 형상 관리도 소프트웨어의 모든 변경 사항을 추적합니다.

### 2. 등장 배경 및 발전 과정

#### 1) 1970년대: 형상 관리의 태동
초기 소프트웨어 개발에서는 변경 관리가 체계적이지 않아 다음과 같은 문제가 발생했습니다.
- "이 버그는 지난번에 고치지 않았나?"
- "누가 이 코드를 수정했지?"
- "배포된 버전이 어떤 코드인지 모르겠어!"

#### 2) 1980년대: 중앙집중형 VCS 등장
RCS(1982), CVS(1986), SVN(2000) 등 **중앙집중형 버전 관리 시스템**이 등장했습니다.

#### 3) 2000년대: 분산형 VCS 혁명
Linus Torvalds가 **Git(2005)**을 개발하면서 형상 관리의 패러다임이 바뀌었습니다. 분산형 버전 관리는 로컬에서도 전체 이력을 가질 수 있어, 오프라인 작업과 브랜치 관리가 획기적으로 개선되었습니다.

#### 4) 2010년대~현재: DevOps와 GitOps
형상 관리가 단순한 버전 관리를 넘어 **IaC, GitOps, Infrastructure as Code**로 확장되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 형상 관리 구성 요소

| 구성 요소 | 정의 | 역할 | 예시 |
| :--- | :--- | :--- | :--- |
| **형상 항목 (CI)** | 관리 대상 산출물 | 변경 추적 단위 | 소스코드, 문서, DB 스키마 |
| **기준선 (Baseline)** | 특정 시점의 공식 상태 | 변경 통제의 기준점 | v1.0, Release-2024-Q1 |
| **변경 요청 (CR)** | 변경에 대한 공식 요청 | 통제 프로세스 시작점 | RFC(Request for Change) |
| **CCB** | 변경 통제 위원회 | 변경 승인/반려 의사결정 | 프로젝트 관리자, 아키텍트 |
| **형상 관리 도구** | 자동화 도구 | 버전 관리, 추적 | Git, SVN, GitLab |

### 2. 정교한 구조 다이어그램: 형상 관리 프로세스

```text
================================================================================
|               SOFTWARE CONFIGURATION MANAGEMENT PROCESS                       |
================================================================================

    [ IDENTIFICATION ]          [ CONTROL ]           [ STATUS ACCOUNTING ]
    ================           ============          ===================
    | CI 선정                   | CCB 심의             | 변경 이력 기록
    | 명명 규칙                 | 승인/반려            | 상태 추적
    | 버전 번호 부여            | 우선순위 결정        | 보고서 생성
    v                           v                      v
    +---------------+     +---------------+      +---------------+
    | Configuration |     | Change Request|      | Change Log    |
    | Items (CIs)   | --> | (CR) Process  | --> | Status Report |
    +---------------+     +---------------+      +---------------+
            |                     |                      |
            |                     v                      |
            |            +---------------+              |
            |            | Baseline      |<-------------+
            |            | Management    |
            |            +---------------+
            |                     |
            v                     v
    +-------------------------------------------+
    |                AUDIT                       |
    | - Functional Audit (기능적 감사)           |
    | - Physical Audit (물리적 감사)             |
    | - 무결성 검증                              |
    +-------------------------------------------+

================================================================================
```

### 3. 심층 동작 원리: Git 기반 형상 관리

#### Git 브랜치 전략 (Git Flow)

```text
[GIT FLOW BRANCH STRATEGY]

    master (main)
    ======---------------------------------------------------------------------->
          \                                    /
    develop\----------------------------------/-------------------------------->
            \           /        /           /
             \         /        /           /
    feature/A \-------/--------/           /
              release/1.0   hotfix/urgent  /
                    \       /             /
    feature/B -------\-----/-------------/----------------------------------->
                       \ /
                        X
                        |
                    merge to master

    BRANCH TYPES:
    =============
    - main/master: 프로덕션 배포용 (보호됨)
    - develop: 개발 통합 브랜치
    - feature/*: 기능 개발 브랜치
    - release/*: 릴리스 준비 브랜치
    - hotfix/*: 긴급 수정 브랜치

    WORKFLOW:
    =========
    1. develop에서 feature 브랜치 생성
    2. 기능 개발 후 develop으로 merge
    3. 릴리스 준비 시 release 브랜치 생성
    4. 테스트 완료 후 main과 develop으로 merge
    5. 프로덕션 이슈 시 hotfix 브랜치로 긴급 수정
```

#### GitHub Flow (단순화)

```text
[GITHUB FLOW - SIMPLIFIED]

    main =======---------------------------------------------------------->
               \           /
    feature/A   \---------/
                  PR (Pull Request)
                  + Code Review
                  + CI Tests

    WORKFLOW:
    =========
    1. main에서 브랜치 생성
    2. 작업 후 Pull Request 생성
    3. 코드 리뷰 + 자동 테스트
    4. 승인 후 main으로 merge
    5. 즉시 배포 (CD)
```

### 4. 실무 코드 예시: Git 기반 형상 관리

```bash
# ============================================
# Git 기반 형상 관리 워크플로우 예시
# ============================================

# 1. 저장소 초기화 및 기본 설정
git init my-project
cd my-project
git config user.name "Developer"
git config user.email "developer@company.com"

# 2. .gitignore 설정 (형상 항목에서 제외)
cat > .gitignore << 'EOF'
# Build artifacts
/build/
/dist/
*.pyc
__pycache__/

# Dependencies
node_modules/
venv/

# IDE
.idea/
.vscode/
*.swp

# Environment
.env
.env.local
*.secret
EOF

# 3. 초기 커밋 (기준선 0.1)
git add .
git commit -m "Initial commit: Project skeleton"

# 4. 태그 생성 (공식 기준선)
git tag -a v0.1.0 -m "Baseline v0.1.0: Initial release"

# 5. 기능 개발 브랜치 생성
git checkout -b feature/user-authentication

# 6. 기능 개발 및 커밋
git add src/auth/
git commit -m "feat(auth): Implement user login API

- Add JWT token generation
- Implement password hashing with bcrypt
- Add unit tests for authentication

Closes #123"

# 7. 컨벤셔널 커밋 메시지 형식
# feat: 새 기능
# fix: 버그 수정
# docs: 문서 변경
# style: 포맷팅 (코드 변경 없음)
# refactor: 리팩토링
# test: 테스트 추가/수정
# chore: 빌드/도구 변경

# 8. 원격 저장소에 푸시
git push origin feature/user-authentication

# 9. Pull Request 생성 (GitHub CLI)
gh pr create --title "feat(auth): Implement user login API" \
             --body "## Changes
             - JWT authentication
             - Password hashing

             ## Test Plan
             - [x] Unit tests pass
             - [x] Integration tests pass"

# 10. 코드 리뷰 후 main으로 머지
git checkout main
git merge --no-ff feature/user-authentication

# 11. 릴리스 태그 생성
git tag -a v1.0.0 -m "Release v1.0.0: User authentication feature"

# 12. 릴리스 브랜치 생성 (Git Flow)
git checkout -b release/1.0.0
# 버그 수정, 문서 업데이트...
git commit -m "chore: Update README for v1.0.0"

# 13. main과 develop에 머지
git checkout main
git merge --no-ff release/1.0.0
git checkout develop
git merge --no-ff release/1.0.0
```

### 5. 형상 감사 (Configuration Audit)

| 감사 유형 | 목적 | 핵심 질문 | 수행 시점 |
| :--- | :--- | :--- | :--- |
| **기능적 감사 (FCA)** | 요구사항 충족 확인 | "지정된 기능이 동작하는가?" | 릴리스 전 |
| **물리적 감사 (PCA)** | 문서-실제 일치 확인 | "문서와 코드가 일치하는가?" | 기준선 설정 시 |
| **형상 감사** | 무결성 확인 | "승인된 변경만 반영되었는가?" | 정기적 |

### 6. 기준선(Baseline) 유형

| 기준선 유형 | 정의 시점 | 구성 요소 | 승인 권한 |
| :--- | :--- | :--- | :--- |
| **기능적 기준선** | 요구사항 완료 | SRS, 유스케이스 | 고객/PO |
| **설계 기준선** | 설계 완료 | HLD, LLD, DB 설계 | 아키텍트 |
| **개발 기준선** | 코딩 완료 | 소스코드, 단위 테스트 | 개발 팀장 |
| **제품 기준선** | 테스트 완료 | 실행 파일, 설치 매뉴얼 | QA 관리자 |

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 중앙집중형 vs 분산형 VCS

| 비교 항목 | 중앙집중형 (SVN) | 분산형 (Git) |
| :--- | :--- | :--- |
| **저장소 구조** | 중앙 서버 1개 | 로컬 + 원격 (분산) |
| **오프라인 작업** | 제한적 | 완전 가능 |
| **브랜치 생성** | 무거움 (복사) | 가벼움 (포인터) |
| **속도** | 네트워크 의존 | 로컬 작업 빠름 |
| **충돌 해결** | 중앙에서 | 로컬에서 사전 해결 |
| **적합 규모** | 중소형, 문서 관리 | 모든 규모, 특히 대형 |
| **학습 곡선** | 낮음 | 중간~높음 |

### 2. 과목 융합 관점 분석

#### 형상 관리 + DevOps (GitOps)

```text
[GitOps: Git을 진실의 원천으로]

Git Repository (Source of Truth)
        |
        | Git commit/merge
        v
+------------------+
| CI/CD Pipeline   |
| - Build          |
| - Test           |
| - Security Scan  |
+------------------+
        |
        | Artifact (Container Image)
        v
+------------------+
| GitOps Operator  | (ArgoCD, Flux)
| - Watch Git      |
| - Compare State  |
| - Sync if Drift  |
+------------------+
        |
        | Deploy
        v
+------------------+
| Kubernetes       |
| Cluster          |
+------------------+

[GitOps 원칙]
1. 선언적 (Declarative): 원하는 상태를 Git에 선언
2. 버전화 (Versioned): 모든 변경이 Git 이력에 남음
3. 자동화 (Automated): 변경 감지 시 자동 배포
4. 지속적 조정 (Continuously Reconciled): 드리프트 자동 복구
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오

**[시나리오 1] 금융사의 형상 관리 표준 수립**
*   **상황**: 감사에서 "소스코드 변경 이력 추적 불가" 지적
*   **전략**:
    1. Git 기반 중앙 저장소 구축 (GitLab Enterprise)
    2. 모든 변경은 Pull Request + 코드 리뷰 필수
    3. main 브랜치는 보호(직접 push 금지)
    4. 모든 릴리스에 태그 및 서명 필수
    5. 감사용 변경 이력 보고서 자동 생성

**[시나리오 2] 스타트업의 효율적 형상 관리**
*   **상황**: 빠른 개발 속도, 잦은 배포
*   **전략**: GitHub Flow 채택
    1. main 브랜치만 관리
    2. 모든 기능은 PR로 머지
    3. CI 자동 테스트 필수
    4. 머지 즉시 자동 배포 (CD)

### 2. 주의사항 및 안티패턴

*   **Large Binary 파일 관리**: 게임 에셋, ML 모델 등 대용량 파일은 Git LFS 사용
*   **Force Push 금지**: 이력을 덮어쓰면 추적성 상실
*   **Sensitive Data 노출**: .gitignore로 .env, credential 파일 제외
*   **Merge vs Rebase**: 팀 컨벤션 통일 필요

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적 기대효과

| 구분 | 지표 | 형상 관리 도입 시 효과 |
| :--- | :--- | :--- |
| **변경 추적성** | 변경 이력 조회 시간 | 90% 단축 (수동 검색 vs Git log) |
| **롤백 시간** | 장애 시 복구 시간 | 분 단위 (태그 기반) |
| **동시 개발** | 브랜치 기반 병렬 개발 | 팀 생산성 30% 향상 |
| **감사 대응** | 감사 준비 시간 | 80% 단축 (자동화된 보고서) |

### ※ 참고 표준/가이드
*   **IEEE 828**: 형상 관리 계획서 표준
*   **IEEE 1042**: 형상 관리 가이드
*   **ISO/IEC/IEEE 12207**: 형상 관리 공정
*   **Git Documentation**: https://git-scm.com/doc

---

## 📌 관련 개념 맵 (Knowledge Graph)
*   [DevOps CI/CD](@/studynotes/04_software_engineering/01_sdlc/devops.md) : 형상 관리와 자동화의 결합
*   [V-모델](@/studynotes/04_software_engineering/01_sdlc/v_model.md) : 기준선 설정 시점
*   [CMMI](@/studynotes/04_software_engineering/01_sdlc/cmmi.md) : Level 2 형상 관리 PA
*   [협업 도구](@/studynotes/04_software_engineering/03_project/_index.md) : 형상 관리의 팀 협업 확장

---

## 👶 어린이를 위한 3줄 비유 설명
1. **문제**: 여러 친구가 함께 레고 성을 만드는데, 누가 어디를 수정했는지 몰라서 엉망이 됐어요.
2. **해결(형상 관리)**: 이제는 수정할 때마다 "내가 탑을 3층에서 5층으로 높였어"라고 사진과 함께 기록해요. 되돌리고 싶으면 이전 사진을 보고 다시 만들면 돼요.
3. **효과**: 누가 뭘 했는지 다 알 수 있어서, 실수해도 바로 고칠 수 있고, 예쁜 버전을 저장해뒀다가 나중에 다시 만들 수도 있어요!
