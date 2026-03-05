+++
title = "에러 버짯 (Error Budget)"
categories = ["studynotes-15_devops_sre"]
+++

# 에러 버짯 (Error Budget)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 100% 가용성의 비현실성을 인정하고, SLO(Service Level Objective)와 실제 성능의 차이를 '허용된 장애 예산'으로 정의하여 혁신(개발 속도)과 안정성의 균형을 맞추는 SRE 핵심 개념입니다.
> 2. **가치**: "완벽함"을 추구하느라 혁신을 멈추는 대신, 정의된 범위 내에서 장애를 수용하고, 버짯이 소진되면 안정화 작업에 집중하는 정량적 의사결정 프레임워크입니다.
> 3. **융합**: SLO(SLI), CI/CD 파이프라인, 그리고 비즈니스 우선순위를 연결하여 개발팀과 운영팀의 공동 목표를 수학적으로 조율합니다.

---

## Ⅰ. 개요 (Context & Background)

에러 버짯(Error Budget)은 구글의 SRE(Site Reliability Engineering) 철학에서 나온 개념으로, "100% 가용성은 비용적으로 불가능하고 비즈니스적으로도 불필요하다"는 전제하에, SLO(서비스 수준 목표)와 실제 성능 간의 차이를 '장애를 허용할 수 있는 예산'으로 정의합니다.

**💡 비유: 자동차 연료 통**
자동차에 연료가 가득 차 있다고 가정해 봅시다. 이 연료는 "달려도 되는 거리"를 의미합니다. 연료가 넉넉할 때는 새로운 목적지(신규 기능)를 탐험하러 떠날 수 있습니다. 하지만 연료가 거의 바닥나면, 더 이상 탐험하지 말고 가까운 주유소(안정화 작업)로 가서 연료를 채워야 합니다.

에러 버짯도 마찬가지입니다. 버짯이 넉넉하면 개발팀은 과감하게 새 기능을 출시할 수 있습니다. 하지만 버짯이 바닥나면, 개발을 멈추고 시스템 안정화에 집중해야 합니다.

**등장 배경 및 발전 과정**:
1. **기존 기술의 치명적 한계점 (Wall of Confusion)**:
   - 개발팀: "빨리 새 기능을 출시하고 싶다"
   - 운영팀: "장애 없이 안정적으로 운영하고 싶다"
   - 이 두 목표는 본질적으로 충돌하며, 감정적 논쟁으로 번짐

2. **혁신적 패러다임 변화의 시작**:
   - 구글 SRE 팀이 "100%는 잘못된 목표"임을 깨달음
   - 99.9% SLO = 0.1% 에러 버짯 = 한 달에 43분 12초 다운타임 허용
   - 이 43분 12초를 "혁신을 위해 사용할 수 있는 예산"으로 재정의

3. **현재 시장/산업의 비즈니스적 요구사항**:
   - MSA(Microservices) 환경에서 완벽한 무장애는 불가능
   - 비즈니스 요구사항과 안정성 요구사항의 정량적 조율 필요
   - CI/CD 파이프라인과의 자동화된 연계

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 에러 버짯 핵심 구성 요소

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 계산 공식 | 비유 |
|:---|:---|:---|:---|:---|
| **SLI** | 서비스 수준 지시자 | 실제 성능 측정값 | 성공 요청 / 전체 요청 | 혈압 측정값 |
| **SLO** | 서비스 수준 목표 | 목표 성능값 | 비즈니스와 합의한 목표 | 정상 혈압 범위 |
| **Error Budget** | 허용 가능한 장애 예산 | 100% - SLO | 1 - 0.999 = 0.001 (0.1%) | 건강 보험 한도 |
| **Burn Rate** | 버짯 소진 속도 | 단위 시간당 소진량 | 현재 에러율 / 허용 에러율 | 연료 소비율 |
| **Budget Policy** | 버짯 기반 정책 | 자동화된 의사결정 | if budget < 0 then freeze | 연료 경고등 |

### 2. 정교한 구조 다이어그램: 에러 버짯 라이프사이클

```text
================================================================================
                      [ Error Budget Lifecycle ]
================================================================================

  [ SLO Definition ]                    [ Error Budget Calculation ]
  +------------------+                 +---------------------------+
  | SLO: 99.9%       |                 | Budget = 100% - 99.9%     |
  | (30일 윈도우)    | --------------> |       = 0.1%              |
  |                  |                 |       = 43분 12초/월      |
  +------------------+                 +---------------------------+
                                              |
                                              v
  [ Error Budget Consumption ]        [ Budget Tracking ]
  +---------------------------+       +------------------+
  | 장애 발생 시 소진:         |       | Budget Remaining:|
  | - 10분 다운타임 = -10분    | ----> | 43분 - 10분      |
  | - 5% 에러율 1시간 = -3분   |       | = 33분 (77%)     |
  +---------------------------+       +------------------+
                                              |
                                              v
  [ Budget Policy Actions ]
  +------------------------------------------+
  | Budget > 50%: "Go fast! 신규 기능 출시"   |
  | Budget 25-50%: "주의, 모니터링 강화"      |
  | Budget < 25%: "경고, 위험 배포 중단"      |
  | Budget <= 0: "정지! 안정화 작업만 허용"   |
  +------------------------------------------+
                |
                v
  [ Automated Actions ]
  +------------------------------------------+
  | - CI/CD 배포 승인 자동 차단              |
  | - Slack 알림: "배포 동결 (Freeze)"        |
  | - JIRA 티켓 자동 생성: 안정화 작업        |
  +------------------------------------------+

  [ Burn Rate Alerting ]
  +------------------------------------------+
  | Burn Rate 14.4x (1시간에 5% 소진):        |
  |   -> CRITICAL Alert (즉시 대응)           |
  | Burn Rate 1x (30일에 100% 소진):          |
  |   -> WARNING Alert (주의)                 |
  +------------------------------------------+
```

### 3. 심층 동작 원리

**1단계: SLO 정의 및 타임 윈도우 설정**

SLO는 비즈니스 팀과 기술팀이 합의해야 합니다:
- "결제 API의 가용성 SLO는 30일 롤링 윈도우 기준 99.9%"
- 이는 30일 동안 43분 12초의 다운타임을 허용한다는 의미

```python
# SLO 계산
slo = 0.999  # 99.9%
window_days = 30
total_minutes = window_days * 24 * 60  # 43,200분
allowed_downtime = total_minutes * (1 - slo)  # 43.2분
```

**2단계: 에러 버짯 계산**

```python
# 에러 버짯 계산
error_budget = 1 - slo  # 0.001 = 0.1%
error_budget_minutes = total_minutes * error_budget  # 43.2분
```

**3단계: 실시간 버짯 소진 추적**

```promql
# PromQL: 남은 에러 버짯 계산 (분)
# 현재 윈도우의 실제 가용성
(
  1 - (
    sum(rate(http_requests_total{status=~"5.."}[30d]))
    /
    sum(rate(http_requests_total[30d]))
  )
) * 43200  # 30일을 분으로 환산

# 또는 누적 소진 버짯
sum(increase(downtime_minutes_total[30d]))
```

**4단계: Burn Rate 기반 알림**

Burn Rate는 버짯이 얼마나 빨리 소진되고 있는지를 나타냅니다:
- Burn Rate 1x: 30일에 100% 소진 (정상)
- Burn Rate 10x: 3일에 100% 소진 (위험)
- Burn Rate 100x: 7시간에 100% 소진 (긴급)

```yaml
# Prometheus Alert Rules
groups:
  - name: error_budget_alerts
    rules:
      # Burn Rate 14.4x (1시간에 5% 소진) - CRITICAL
      - alert: ErrorBudgetCriticalBurn
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[1h]))
            /
            sum(rate(http_requests_total[1h]))
          ) > (0.001 * 14.4)
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "에러 버짯이 14.4x 속도로 소진 중"
          description: "1시간 내 5% 소진. 즉시 대응 필요."

      # Burn Rate 1x (30일에 100% 소진) - WARNING
      - alert: ErrorBudgetNormalBurn
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[30d]))
            /
            sum(rate(http_requests_total[30d]))
          ) > 0.001
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "에러 버짯 소진 중 (정상 속도)"
```

**5단계: 정책 실행 (Budget Policy)**

```python
# budget_policy.py - 에러 버짯 기반 정책 실행
class ErrorBudgetPolicy:
    def __init__(self, slo: float, window_days: int = 30):
        self.slo = slo
        self.window_days = window_days
        self.total_budget = 1 - slo

    def get_remaining_budget(self, current_availability: float) -> float:
        """남은 에러 버짯 계산"""
        consumed = max(0, self.slo - current_availability)
        return max(0, self.total_budget - consumed)

    def evaluate_deployment_policy(self, remaining_budget: float) -> dict:
        """배포 정책 평가"""
        budget_percent = (remaining_budget / self.total_budget) * 100

        if budget_percent > 50:
            return {
                "action": "ALLOW_DEPLOYMENT",
                "message": "버짯 넉넉함. 신규 기능 배포 허용.",
                "freeze": False
            }
        elif budget_percent > 25:
            return {
                "action": "CAUTIOUS_DEPLOYMENT",
                "message": "버짯 주의. 위험 배포는 중단.",
                "freeze": False
            }
        elif budget_percent > 0:
            return {
                "action": "FREEZE_RISKY_DEPLOYMENTS",
                "message": "버짯 경고. 안전한 배포만 허용.",
                "freeze": True,
                "freeze_type": "PARTIAL"
            }
        else:
            return {
                "action": "FULL_FREEZE",
                "message": "버짯 소진. 모든 배포 동결. 안정화 작업만 허용.",
                "freeze": True,
                "freeze_type": "FULL"
            }

    def notify_team(self, policy_result: dict, channel: str = "#dev-team"):
        """슬랙 알림 전송"""
        import requests
        import os

        webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
        color = "good" if not policy_result["freeze"] else "danger"

        payload = {
            "channel": channel,
            "attachments": [{
                "color": color,
                "title": f"Error Budget Policy: {policy_result['action']}",
                "text": policy_result["message"],
                "footer": "SRE Error Budget System"
            }]
        }

        requests.post(webhook_url, json=payload)
```

### 4. CI/CD 파이프라인과의 통합

```yaml
# ArgoCD Application with Error Budget Gate
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  annotations:
    # 에러 버짯 체크를 위한 PreSync Hook
    argocd.argoproj.io/sync-options: FailOnSharedResource=true
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myapp.git
    targetRevision: HEAD
    path: k8s/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    # PreSync Hook으로 에러 버짯 체크
    syncOptions:
      - CreateNamespace=true
---
# PreSync Job: 에러 버짯 확인
apiVersion: batch/v1
kind: Job
metadata:
  generateName: error-budget-check-
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: budget-check
          image: curlimages/curl:latest
          command:
            - /bin/sh
            - -c
            - |
              # Prometheus에서 현재 에러 버짯 조회
              BUDGET=$(curl -s "http://prometheus:9090/api/v1/query?query=error_budget_remaining" | jq -r '.data.result[0].value[1]')

              if [ $(echo "$BUDGET < 0" | bc) -eq 1 ]; then
                echo "Error budget exhausted! Deployment blocked."
                exit 1
              fi

              echo "Error budget OK: $BUDGET remaining. Proceeding with deployment."
      restartPolicy: Never
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: SLO별 에러 버짯

| SLO | 에러 버짯 | 월간 허용 다운타임 | 일간 허용 다운타임 | 적용 서비스 |
|:---|:---|:---|:---|:---|
| 99.9% | 0.1% | 43분 12초 | 1분 26초 | 일반 웹 서비스 |
| 99.99% | 0.01% | 4분 19초 | 8.6초 | 금융 결제 |
| 99.999% | 0.001% | 26초 | 0.86초 | 항공 교통 |
| 99% | 1% | 7시간 12분 | 14분 24초 | 내부 도구 |

### 2. 과목 융합 관점 분석

**에러 버짯 + CI/CD**:
- 버짯이 충분하면: 자동 배포 허용
- 버짯이 부족하면: 배포 자동 동결
- CI/CD 파이프라인에 Pre-deployment Gate로 통합

**에러 버짯 + 비즈니스**:
- "이번 달 에러 버짯의 50%를 신규 기능 출시에 사용했습니다"
- "버짯 소진으로 2주간 안정화 Sprint 진행"
- 경영진 보고: 정량적 안정성 지표

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

**시나리오: 대규모 이커머스 플랫폼의 에러 버짯 도입**
- **상황**: 월 2회 대규모 배포 시마다 장애 발생, 개발/운영 간 갈등
- **기술사의 전략적 의사결정**:
  1. **SLO 협의**: 비즈니스 팀과 협의하여 핵심 API는 99.9%, 일반 API는 99.5%로 설정
  2. **버짯 공유**: 모든 팀이 볼 수 있는 에러 버짯 대시보드 구축
  3. **정책 자동화**: 버짯 < 25%일 때 배포 자동 동결
  4. **회고 프로세스**: 버짯 소진 시 Blameless Post-mortem 진행

### 2. 도입 시 고려사항 (체크리스트)

- [ ] SLO가 비즈니스 팀과 합의되었는가?
- [ ] 에러 버짯이 팀 전체에 공유되는가?
- [ ] 버짯 기반 정책이 자동화되었는가?
- [ ] 버짯 소진 시 대응 프로세스가 정의되었는가?

### 3. 주의사항 및 안티패턴 (Anti-patterns)

**안티패턴: 100% SLO 설정**
- 문제: 100% SLO는 불가능하고, 오히려 위험한 배포를 야기
- 해결: 현실적인 SLO(99.9%)를 설정하고, 나머지를 버짯으로 활용

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **개발/운영 갈등** | 높음 (감정적 논쟁) | 낮음 (데이터 기반) | 협업 개선 |
| **배포 속도** | 보수적 (장애 두려움) | 적극적 (버짯 내 자유) | 배포 빈도 증가 |
| **장애 복구** | 수동 대응 | 자동화된 정책 | MTTR 단축 |

### 2. 미래 전망 및 진화 방향

- **AI 기반 버짯 예측**: 향후 버짯 소진 시점 예측
- **동적 SLO 조정**: 트래픽 패턴에 따른 SLO 자동 조정
- **버짯 거래**: 팀 간 에러 버짯 교환 (실험적)

### 3. 참고 표준/가이드

- **Google SRE Workbook**: 에러 버짯 실천 가이드
- **The Site Reliability Workbook**: 구글의 에러 버짯 활용법

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [SRE 원칙](@/studynotes/15_devops_sre/01_sre/sre_principles.md) : 에러 버짯의 근간이 되는 철학
- [SLI/SLO/SLA](@/studynotes/15_devops_sre/01_sre/sli_slo_sla.md) : 에러 버짯 계산의 기준
- [Observability](@/studynotes/15_devops_sre/02_observability/observability_fundamentals.md) : 버짯 소진 추적의 기반
- [CI/CD Pipeline](@/studynotes/15_devops_sre/03_automation/cicd_gitops.md) : 버짯 기반 배포 제어
- [Blameless Post-mortem](@/studynotes/15_devops_sre/01_sre/blameless_postmortem.md) : 버짯 소진 시 학습 프로세스

---

## 👶 어린이를 위한 3줄 비유 설명

1. 에러 버짯은 **용돈**과 같아요. 한 달에 10,000원을 받으면, 그 안에서 장난감을 사거나 맛있는 걸 먹을 수 있죠.
2. 돈을 다 쓰면 **더 이상 장난감을 살 수 없어요**. 다음 달까지 기다리거나, 돈을 더 모아야 해요.
3. 프로그램도 마찬가지예요. "장애 용돈"을 다 쓰면 **새 기능을 멈추고 문제를 고쳐야 해요**!
