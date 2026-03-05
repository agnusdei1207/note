+++
title = "롤백 (Rollback) 전략"
description = "파이프라인 에러율 임계치 도달 시 이전 안정 버전으로 자동 복원하는 전략에 대한 심층 기술 백서"
date = 2024-05-15
[taxonomies]
tags = ["Rollback", "Deployment", "GitOps", "Kubernetes", "Disaster Recovery"]
+++

# 롤백 (Rollback) 전략

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 롤백(Rollback)은 배포된 소프트웨어 버전에서 치명적 결함이 발견되었을 때, **이전의 안정적인 버전으로 신속하게 되돌리는 장애 대응 메커니즘**으로, MTTR(평균 복구 시간)을 최소화하는 핵심 운영 기술입니다.
> 2. **가치**: 자동화된 롤백 시스템은 장애 지속 시간을 수시간에서 수분 또는 수초로 단축시키며, "실패해도 안전한(Safe to Fail)" 배포 문화를 가능하게 하여 개발팀의 배포 빈도를 증가시킵니다.
> 3. **융합**: Git의 Revert, Kubernetes의 Rollout Undo, Helm의 Rollback, ArgoCD의 동기화, 카나리 분석 자동화와 결합하여 단일 명령 또는 자동 감지에 의한 즉각적 복구 체계를 구축합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**롤백(Rollback)**은 소프트웨어 배포 후 발생하는 치명적인 버그, 성능 저하, 보안 취약점, 또는 예기치 못한 동작으로 인해 **이전 버전(또는 마지막 안정 버전)으로 신속하게 되돌리는 장애 복구 기술**입니다. 롤백은 배포의 역연산(inverse operation)으로, "배포로 인한 변경사항을 취소"하는 작업입니다.

롤백의 핵심 특성:
- **신속성(Speed)**: 장애 감지 후 가능한 한 빠르게 복구해야 합니다.
- **안전성(Safety)**: 롤백 자체가 새로운 장애를 유발하지 않아야 합니다.
- **완전성(Completeness)**: 모든 변경사항(코드, 설정, DB)이 일관되게 복구되어야 합니다.
- **추적성(Traceability)**: 언제, 왜, 누가 롤백했는지 기록되어야 합니다.

### 💡 2. 구체적인 일상생활 비유
**비상 탈출구(Emergency Exit)**를 상상해 보세요:
- 건물에 화재가 발생하면 사람들은 비상 탈출구로 신속하게 대피합니다.
- **롤백**은 "건물(프로덕션)에 문제가 생겼을 때 이전 위치(안전한 버전)로 대피하는 것"입니다.
- 비상 탈출구는 **항상 열려 있어야 하고**, **어디에 있는지 모두가 알아야 하며**, **신속하게 사용할 수 있어야** 합니다.

또 다른 비유: **컴퓨터 시스템 복원(System Restore)**
- 컴퓨터에 문제가 생기면 "이전 복원 지점"으로 되돌립니다.
- 롤백은 소프트웨어 버전의 "복원 지점"으로 되돌리는 것입니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (수동 롤백의 위험)**:
   과거에는 배포 실패 시:
   - 이전 버전 코드를 다시 찾아서 다시 배포합니다.
   - DB 스키마 변경을 수동으로 되돌립니다.
   - 설정 파일을 이전 상태로 수동 복구합니다.
   - 평균 롤백 시간: 2~4시간. 그 사이 서비스 중단.

2. **혁신적 패러다임 변화의 시작**:
   - **2010년대**: 블루-그린 배포가 "1초 롤백"을 가능하게 했습니다.
   - **2014년**: Kubernetes가 `kubectl rollout undo` 명령으로 선언적 롤백을 도입했습니다.
   - **2017년**: GitOps가 "Git Revert = 프로덕션 롤백" 패러다임을 도입했습니다.
   - **현재**: 카나리 분석 자동화가 "이상 감지 시 자동 롤백"을 구현합니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   SLO(서비스 수준 목표)가 99.9%인 서비스에서 연간 허용 다운타임은 8시간 46분입니다. 1시간 롤백은 SLO의 11%를 소진합니다. 롤백은 5분 이내에 완료되어야 합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **버전 히스토리** | 모든 배포 버전 기록 | 컨테이너 이미지 태그, Git 커밋 SHA | Docker Registry, Git | 복원 지점 |
| **롤백 트리거** | 롤백 시작 조건 감지 | 메트릭 임계치, 수동 명령, CI 실패 | Prometheus, ArgoCD | 화재 경보기 |
| **롤백 실행기** | 실제 버전 전환 수행 | 이미지 태그 변경, 트래픽 라우팅 전환 | Kubernetes, Helm, Istio | 비상 탈출 |
| **상태 검증** | 롤백 후 정상 동작 확인 | 헬스 체크, 스모크 테스트 | K8s Probes, Test Script | 안전 확인 |
| **알림 시스템** | 롤백 사실을 팀에 전파 | Slack, PagerDuty, 이메일 | Alertmanager | 대피 알림 |

### 2. 정교한 구조 다이어그램: 롤백 아키텍처

```text
=====================================================================================================
                    [ Rollback Strategy Architecture ]
=====================================================================================================

+-------------------------------------------------------------------------------------------+
|                              [ ROLLBACK TRIGGER SOURCES ]                                 |
|                                                                                           |
│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐                        │
│   │ Manual Trigger  │   │ Automated       │   │ Scheduled       │                        │
│   │ (kubectl, UI)   │   │ Canary Analysis │   │ Expiration      │                        │
│   │                 │   │ (Metrics-based) │   │ (Rollback       │                        │
│   │ $ kubectl       │   │                 │   │  Window)        │                        │
│   │ rollout undo    │   │ Error Rate > 5% │   │                 │                        │
│   └────────┬────────┘   └────────┬────────┘   └────────┬────────┘                        │
│            │                     │                     │                                  │
│            └─────────────────────┼─────────────────────┘                                  │
│                                  ▼                                                        │
+-------------------------------------------------------------------------------------------+
                                   │
                                   ▼
+-------------------------------------------------------------------------------------------+
|                              [ ROLLBACK ORCHESTRATION ]                                   |
|                                                                                           |
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │ ROLLBACK DECISION ENGINE                                                         │   │
│   │                                                                                  │   │
│   │ Input:                     Processing:                   Output:                 │   │
│   │ - Trigger Type            - Target Version Resolution   - Rollback Command      │   │
│   │ - Current Version         - Pre-rollback Checks          - Notification Plan     │   │
│   │ - Error Metrics           - Impact Assessment            - Audit Log Entry       │   │
│   │ - User Confirmation?      - Risk Evaluation                                    │   │
│   └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                   │                                                      │
│                                   ▼                                                      │
+-------------------------------------------------------------------------------------------+
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
+-------------------------------------------------------------------------------------------+
|                              [ ROLLBACK EXECUTION METHODS ]                               |
|                                                                                           |
│   ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐                    │
│   │ Kubernetes        │  │ GitOps Revert     │  │ Traffic Switch    │                    │
│   │ Rollout Undo      │  │ (ArgoCD)          │  │ (Blue-Green)      │                    │
│   │                   │  │                   │  │                   │                    │
│   │ $ kubectl rollout │  │ $ git revert      │  │ Service Selector: │                    │
│   │ undo deployment/  │  │ abc123            │  │ blue → green      │                    │
│   │ myapp             │  │                   │  │                   │                    │
│   │                   │  │ ArgoCD auto-sync  │  │ (Instant)         │                    │
│   │ (Seconds)         │  │ (Minutes)         │  │                   │                    │
│   └───────────────────┘  └───────────────────┘  └───────────────────┘                    │
│                                                                                           |
+-------------------------------------------------------------------------------------------+
                                   │
                                   ▼
+-------------------------------------------------------------------------------------------+
|                              [ POST-ROLLBACK VERIFICATION ]                               |
|                                                                                           |
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │ HEALTH CHECK FLOW                                                                │   │
│   │                                                                                  │   │
│   │ 1. Pod Readiness ────────> 2. Service Endpoints ────────> 3. Smoke Tests        │   │
│   │    All Pods Ready?            DNS Resolution OK?           Login Works?          │   │
│   │           │                          │                          │                 │   │
│   │           ▼                          ▼                          ▼                 │   │
│   │         ✅ YES                     ✅ YES                     ✅ YES              │   │
│   │           │                          │                          │                 │   │
│   │           └──────────────────────────┼──────────────────────────┘                 │   │
│   │                                      ▼                                            │   │
│   │                              ROLLBACK SUCCESS ✅                                  │   │
│   │                                                                                   │   │
│   └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                   │                                                      │
│                                   ▼                                                      │
+-------------------------------------------------------------------------------------------+
|                              [ NOTIFICATION & AUDIT ]                                     |
|                                                                                           |
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Notifications:                                                                   │   │
│   │ - Slack: "🔄 Rollback completed: myapp v1.2.0 → v1.1.0"                         │   │
│   │ - PagerDuty: Incident resolved                                                  │   │
│   │ - Email: Post-incident report request                                           │   │
│   │                                                                                  │   │
│   │ Audit Log:                                                                       │   │
│   │ - Timestamp: 2024-01-15T10:30:00Z                                               │   │
│   │ - Operator: automated (canary-analysis)                                         │   │
│   │ - Reason: Error rate exceeded 5% threshold                                      │   │
│   │ - Previous: v1.2.0 (abc123) → Current: v1.1.0 (def456)                          │   │
│   └─────────────────────────────────────────────────────────────────────────────────┘   │
+-------------------------------------------------------------------------------------------+
```

### 3. 심층 동작 원리 (롤백 실행 과정)

**1단계: 롤백 트리거 감지**
```yaml
# Prometheus Alert Rule - 자동 롤백 트리거
groups:
- name: rollback.rules
  rules:
  - alert: HighErrorRateAfterDeployment
    expr: |
      (
        sum(rate(http_requests_total{status=~"5.."}[5m]))
        /
        sum(rate(http_requests_total[5m]))
      ) > 0.05  # 5% 에러율 초과
    for: 2m  # 2분간 지속 시
    labels:
      severity: critical
      action: auto-rollback
    annotations:
      summary: "에러율이 5%를 초과하여 자동 롤백을 트리거합니다."
```

**2단계: 대상 버전 확인**
```bash
# Kubernetes 배포 히스토리 확인
kubectl rollout history deployment/myapp

# 출력:
# REVISION  CHANGE-CAUSE
# 1         Initial deployment
# 2         Update to v1.1.0
# 3         Update to v1.2.0  # 현재 (문제 발생)

# 이전 버전으로 롤백
kubectl rollout undo deployment/myapp

# 또는 특정 리비전으로 롤백
kubectl rollout undo deployment/myapp --to-revision=2
```

**3단계: 롤백 실행**
```yaml
# ArgoCD Rollout - 자동 롤백 설정
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 10
  revisionHistoryLimit: 10  # 롤백 가능한 이전 버전 수

  strategy:
    canary:
      steps:
      - setWeight: 10
      - pause: {duration: 5m}
      - setWeight: 50
      - pause: {duration: 5m}

      # 카나리 분석 - 실패 시 자동 롤백
      analysis:
        templates:
        - templateName: success-rate
        startingStep: 1  # 10% 트래픽 시점부터 분석 시작
        args:
        - name: service-name
          value: myapp-canary

  selector:
    matchLabels:
      app: myapp
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:v1.2.0

---
# AnalysisTemplate - 롤백 조건 정의
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
  - name: service-name
  metrics:
  - name: success-rate
    interval: 30s
    count: 10
    successCondition: result[0] >= 0.95  # 95% 성공률 필요
    failureLimit: 3  # 3회 실패 시 롤백
    provider:
      prometheus:
        address: http://prometheus:9090
        query: |
          sum(rate(http_requests_total{service="{{args.service-name}}",status!~"5.."}[1m]))
          /
          sum(rate(http_requests_total{service="{{args.service-name}}"}[1m]))
```

**4단계: 롤백 후 검증**
```yaml
# Kubernetes Health Check - 롤백 후 자동 검증
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:v1.1.0  # 롤백된 버전

        # 롤백 후 Pod가 Ready 될 때까지 대기
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          failureThreshold: 3

        # Pod가 살아있는지 확인
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10

        # 시작 완료 확인 (롤백 후 서비스 시작)
        startupProbe:
          httpGet:
            path: /health
            port: 8080
          failureThreshold: 30
          periodSeconds: 10
```

### 4. 실무 코드 예시 (자동화된 롤백 파이프라인)

```python
# automated_rollback.py - 자동 롤백 시스템
import requests
import subprocess
import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class RollbackContext:
    service_name: str
    current_version: str
    previous_version: str
    reason: str
    triggered_by: str  # "manual" or "automated"

class AutomatedRollbackSystem:
    """자동화된 롤백 시스템"""

    def __init__(self, k8s_api_url: str, prometheus_url: str, slack_webhook: str):
        self.k8s_api_url = k8s_api_url
        self.prometheus_url = prometheus_url
        self.slack_webhook = slack_webhook

    def check_deployment_health(self, service: str) -> dict:
        """배포 상태 확인"""
        # 1. 에러율 확인
        error_rate = self._query_prometheus(
            f'sum(rate(http_requests_total{{service="{service}",status=~"5.."}}[5m]))'
            f' / sum(rate(http_requests_total{{service="{service}"}}[5m]))'
        )

        # 2. P99 지연 시간 확인
        p99_latency = self._query_prometheus(
            f'histogram_quantile(0.99, rate(http_request_duration_seconds_bucket'
            f'{{service="{service}"}}[5m]))'
        )

        # 3. Pod 상태 확인
        pod_status = self._check_pod_status(service)

        return {
            "error_rate": error_rate,
            "p99_latency": p99_latency,
            "pod_status": pod_status,
            "healthy": error_rate < 0.01 and p99_latency < 1.0
        }

    def should_rollback(self, health: dict, thresholds: dict) -> bool:
        """롤백 필요 여부 판단"""
        if health["error_rate"] > thresholds.get("max_error_rate", 0.05):
            return True
        if health["p99_latency"] > thresholds.get("max_latency", 5.0):
            return True
        if health["pod_status"]["crash_loop_back_off"] > 0:
            return True
        return False

    def execute_rollback(self, context: RollbackContext) -> bool:
        """롤백 실행"""
        try:
            # 1. 현재 버전 기록
            self._log_rollback_start(context)

            # 2. Kubernetes 롤백 실행
            result = subprocess.run([
                "kubectl", "rollout", "undo",
                f"deployment/{context.service_name}",
                "-n", "production"
            ], capture_output=True, text=True)

            if result.returncode != 0:
                raise Exception(f"Rollback failed: {result.stderr}")

            # 3. 롤백 완료 대기
            self._wait_for_rollout(context.service_name)

            # 4. 헬스 체크
            health = self.check_deployment_health(context.service_name)
            if not health["healthy"]:
                raise Exception("Rollback completed but service still unhealthy")

            # 5. 알림 발송
            self._notify_rollback_success(context, health)

            return True

        except Exception as e:
            self._notify_rollback_failure(context, str(e))
            return False

    def _wait_for_rollout(self, service: str, timeout: int = 300):
        """롤백 완료 대기"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = subprocess.run([
                "kubectl", "rollout", "status",
                f"deployment/{service}",
                "-n", "production"
            ], capture_output=True, text=True)

            if result.returncode == 0:
                return True

            time.sleep(5)

        raise TimeoutError(f"Rollout did not complete within {timeout}s")

    def _notify_rollback_success(self, context: RollbackContext, health: dict):
        """롤백 성공 알림"""
        payload = {
            "text": "🔄 Rollback Completed Successfully",
            "attachments": [{
                "color": "good",
                "fields": [
                    {"title": "Service", "value": context.service_name, "short": True},
                    {"title": "Triggered By", "value": context.triggered_by, "short": True},
                    {"title": "Rollback", "value": f"{context.current_version} → {context.previous_version}", "short": False},
                    {"title": "Reason", "value": context.reason, "short": False},
                    {"title": "Current Health", "value": f"Error: {health['error_rate']*100:.2f}%, P99: {health['p99_latency']:.2f}s", "short": False}
                ]
            }]
        }
        requests.post(self.slack_webhook, json=payload)

    def _query_prometheus(self, query: str) -> float:
        """Prometheus 쿼리 실행"""
        response = requests.get(
            f"{self.prometheus_url}/api/v1/query",
            params={"query": query}
        )
        result = response.json()
        if result["status"] == "success" and result["data"]["result"]:
            return float(result["data"]["result"][0]["value"][1])
        return 0.0

# 사용 예시
if __name__ == "__main__":
    rollback_system = AutomatedRollbackSystem(
        k8s_api_url="https://k8s-api.example.com",
        prometheus_url="http://prometheus:9090",
        slack_webhook="https://hooks.slack.com/services/xxx"
    )

    # 배포 상태 확인
    health = rollback_system.check_deployment_health("myapp")
    print(f"Current health: {health}")

    # 롤백 필요 여부 판단
    if rollback_system.should_rollback(health, {"max_error_rate": 0.05}):
        context = RollbackContext(
            service_name="myapp",
            current_version="v1.2.0",
            previous_version="v1.1.0",
            reason=f"Error rate {health['error_rate']*100:.2f}% exceeded threshold",
            triggered_by="automated"
        )
        rollback_system.execute_rollback(context)
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 롤백 방식 비교표

| 방식 | 속도 | 복잡도 | 자동화 가능 | 추적성 | 적합한 상황 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Kubernetes Rollout Undo** | 빠름 (초) | 낮음 | 가능 | 낮음 | 컨테이너 앱 |
| **Git Revert + GitOps** | 중간 (분) | 중간 | 가능 | 매우 높음 | GitOps 환경 |
| **Blue-Green 스위칭** | 매우 빠름 (ms) | 중간 | 가능 | 중간 | 고가용 서비스 |
| **트래픽 라우팅 변경** | 매우 빠름 (ms) | 높음 | 가능 | 중간 | 서비스 메시 |
| **수동 재배포** | 느림 (시간) | 높음 | 불가 | 낮음 | 레거시 |

### 2. 롤백 vs 핫픽스 비교

| 구분 | 롤백 | 핫픽스 |
| :--- | :--- | :--- |
| **정의** | 이전 버전으로 되돌림 | 새로운 수정 버전 배포 |
| **속도** | 빠름 (즉시) | 느림 (개발+테스트+배포) |
| **위험도** | 낮음 (이미 검증된 버전) | 중간 (새 코드) |
| **해결 범위** | 모든 문제 (임시) | 특정 버그만 |
| **후속 작업** | 근본 원인 분석 필요 | 없음 |

### 3. 과목 융합 관점 분석

**롤백 + 데이터베이스 마이그레이션**
- DB 스키마 변경은 롤백이 어렵습니다.
- Expand-Contract 패턴으로 호환성 유지합니다.
- "Forward-only 마이그레이션" 전략을 사용합니다.

**롤백 + SRE (에러 버짯)**
- 롤백은 에러 버짷 소진을 멈추는 비상 브레이크입니다.
- 롤백 후 포스트모템(Postmortem)이 필수입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] DB 스키마 변경과 함께 배포된 경우**
- **문제점**: 애플리케이션은 롤백했지만 DB는 이전 상태로 되돌릴 수 없음.
- **기술사 판단**: **Expand-Contract 패턴 적용**.
  1. 신버전: 새 컬럼 추가 (NULL 허용).
  2. 안정화 후: 구버전도 새 컬럼 사용 가능.
  3. 구버전으로 롤백해도 DB 호환성 유지.

**[상황 B] 롤백 자체가 실패하는 경우**
- **문제점**: 롤백 명령을 실행했지만 Pod가 시작되지 않음.
- **기술사 판단**: **Blue-Green 배포 전환**.
  1. 이전 버전 환경(Blue)을 완전히 유지.
  2. 트래픽만 Green → Blue로 전환.
  3. 환경 자체를 보존하여 롤백 위험 제거.

### 2. 롤백 시스템 체크리스트

**준비 체크리스트**
- [ ] 모든 배포에 대해 이전 버전이 보존되는가? (revisionHistoryLimit)
- [ ] 롤백 명령이 문서화되어 있는가?
- [ ] 롤백 후 헬스 체크가 자동화되어 있는가?
- [ ] 롤백 알림이 팀에 전달되는가?

**테스트 체크리스트**
- [ ] 정기적으로 롤백 훈련을 수행하는가? (Chaos Engineering)
- [ ] 롤백이 실제로 동작하는지 검증했는가?
- [ ] 롤백 시간이 SLO를 충족하는가? (예: 5분 이내)

### 3. 안티패턴 (Anti-patterns)

**안티패턴 1: 롤백 불가능한 배포**
- 이전 버전 정보를 삭제.
- **해결**: revisionHistoryLimit 충분히 설정 (최소 10).

**안티패턴 2: 롤백 후 검증 없음**
- 롤백했지만 여전히 장애 상태.
- **해결**: 롤백 후 자동 헬스 체크 및 스모크 테스트.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 (AS-IS) | 도입 후 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **평균 롤백 시간** | 2~4시간 | 5분 이내 | **95% 단축** |
| **롤백 성공률** | 70% | 99% | **41% 향상** |
| **장애 지속 시간** | 4시간 | 30분 | **87% 단축** |
| **배포 빈도** | 월 2회 (롤백 두려움) | 일 5회 (안전망) | **75배 증가** |

### 2. 미래 전망 및 진화 방향

**AI 기반 예측 롤백**
- AI가 배포 직후 메트릭을 분석하여 "롤백이 필요할 것"을 예측.
- 실제 장애 발생 전에 선제적 롤백.

**무중단 롤백**
- 현재도 블루-그린으로 가능하지만, 더 정교한 트래픽 제어.
- "1%씩 롤백"하는 점진적 롤백.

### 3. 참고 표준/가이드
- **Kubernetes Documentation**: Rollback 명령
- **ArgoCD Rollouts**: 카나리 분석 및 자동 롤백
- **Google SRE Book**: 장애 대응 및 롤백 전략

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **[지속적 배포 (CD)](./continuous_deployment.md)**: 롤백이 필요한 배포 자동화
- **[무중단 배포 전략](./deployment_strategies.md)**: Blue-Green, Canary 배포
- **[카오스 엔지니어링](../02_observability/chaos_engineering.md)**: 롤백 훈련 및 검증
- **[SRE 원칙](@/studynotes/15_devops_sre/01_sre/sre_principles.md)**: 에러 버짯과 롤백 결정

---

## 👶 어린이를 위한 3줄 비유 설명
1. 롤백은 **'비상 탈출구'**예요. 건물에 화재(장애)가 나면 **'안전한 곳(이전 버전)'**으로 빠르게 대피해요.
2. 좋은 건물은 **'비상 탈출구가 항상 열려 있고'**, **'어디 있는지 모두가 알아요'**. 롤백도 마찬가지예요!
3. 탈출한 후에는 **'왜 화재가 났는지'** 꼭 확인해야 해요. 그래야 다시는 같은 문제가 안 생기거든요!
