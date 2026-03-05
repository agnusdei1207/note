+++
title = "무중단 배포 전략 (Rolling, Blue-Green, Canary)"
categories = ["studynotes-15_devops_sre"]
+++

# 무중단 배포 전략 (Rolling, Blue-Green, Canary)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 서비스 중단 없이 새로운 버전을 배포하기 위해 트래픽을 점진적으로 전환하는 세 가지 핵심 전략(Rolling Update, Blue-Green, Canary)으로, 각각 자원 효율성, 롤백 속도, 위험 최소화에 특화되어 있습니다.
> 2. **가치**: 배포로 인한 서비스 중단(Downtime)을 제거하고, 장애 발생 시 빠른 복구를 가능하게 하며, 실제 트래픽으로 새 버전을 안전하게 검증합니다.
> 3. **융합**: Kubernetes, ArgoCD, Service Mesh(Istio)와 결합하여 완전 자동화된 배포 파이프라인을 구축합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)

**무중단 배포(Zero Downtime Deployment)**는 서비스 중단 없이 새로운 버전의 소프트웨어를 프로덕션 환경에 배포하는 기법입니다.

**세 가지 핵심 전략**:

1. **롤링 배포 (Rolling Update)**: 기존 인스턴스를 하나씩 교체하며 점진적으로 새 버전으로 전환
2. **블루-그린 배포 (Blue-Green Deployment)**: 동일한 규모의 새 환경을 완전히 구축한 후 트래픽을 한 번에 전환
3. **카나리 배포 (Canary Release)**: 소수 사용자에게만 새 버전을 노출하여 검증 후 점진적 확대

### 2. 구체적인 일상생활 비유

**교통 터널 보수 공사**로 비유해 봅시다.

- **롤링 배포**: 터널의 4개 차로 중 1개씩 차단하며 보수. 전체 터널을 닫지 않고 교통 흐름 유지
- **블루-그린 배포**: 새 터널을 옆에 완전히 뚫은 후, 차량을 새 터널로 한 번에 전환. 문제 시 즉시 구 터널로 복귀
- **카나리 배포**: 새 터널에 소수 차량만 보내 테스트. 안전하면 점점 더 많은 차량을 새 터널로

### 3. 등장 배경 및 발전 과정

**1단계: 기존 기술의 치명적 한계점**
- 빅뱅 배포(Big Bang Deployment): 전체 서비스 중단 후 일괄 교체
- 새벽 배포: 사용자가 적은 시간에만 배포 가능
- 롤백 시간: 장애 발생 시 복구에 수십 분~수시간 소요

**2단계: 혁신적 패러다임 변화**
- 2000년대: IMVU가 "카나리 배포" 개념 도입 (10분마다 배포)
- 2010년: Netflix가 "Blue-Green Deployment" 정착
- 2014년: Kubernetes가 Rolling Update 네이티브 지원
- 현재: ArgoCD, Spinnaker 등 GitOps 도구로 자동화

**3단계: 현재 시장/산업의 비즈니스적 요구사항**
- 24/7 글로벌 서비스, "새벽 배포" 불가능
- 하루 수십~수백 번 배포 (Continuous Deployment)
- 카나리 분석 자동화 (Kayenta 등)

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 배포 전략 핵심 구성 요소

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 적용 전략 | 비고 |
|:---|:---|:---|:---|:---|
| **트래픽 라우팅** | 사용자 요청 분배 | L7 LB, Service Mesh, DNS | 모든 전략 | Istio, ALB |
| **헬스 체크** | 인스턴스 정상 여부 | HTTP Probe, TCP Probe | 모든 전략 | Readiness Probe |
| **카나리 분석** | 메트릭 기반 판단 | 통계적 유의성 검증 | Canary | Kayenta |
| **롤백 메커니즘** | 이전 버전 복구 | Git Revert, Image Tag 변경 | 모든 전략 | ArgoCD |
| **세션 어피니티** | 사용자 세션 유지 | Cookie, IP Hash | Blue-Green | Sticky Session |

### 2. 정교한 구조 다이어그램: 세 가지 배포 전략 비교

```text
================================================================================
          [ Deployment Strategies Comparison - Rolling vs Blue-Green vs Canary ]
================================================================================

    [ 1. Rolling Update - 점진적 교체 ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   초기 상태 (v1.0 4개)                                                   │
    │   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐                          │
    │   │ Pod-1  │ │ Pod-2  │ │ Pod-3  │ │ Pod-4  │   LB ───> 100% v1.0     │
    │   │ v1.0   │ │ v1.0   │ │ v1.0   │ │ v1.0   │                          │
    │   └────────┘ └────────┘ └────────┘ └────────┘                          │
    │                                                                          │
    │   Step 1: Pod-1 종료 후 v1.1 생성                                        │
    │   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐                          │
    │   │ Pod-1  │ │ Pod-2  │ │ Pod-3  │ │ Pod-4  │   LB ───> 75% v1.0      │
    │   │ v1.1   │ │ v1.0   │ │ v1.0   │ │ v1.0   │       25% v1.1          │
    │   │ (Ready)│ │        │ │        │ │        │                          │
    │   └────────┘ └────────┘ └────────┘ └────────┘                          │
    │                                                                          │
    │   Step 2: Pod-2 종료 후 v1.1 생성                                        │
    │   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐                          │
    │   │ Pod-1  │ │ Pod-2  │ │ Pod-3  │ │ Pod-4  │   LB ───> 50% v1.0      │
    │   │ v1.1   │ │ v1.1   │ │ v1.0   │ │ v1.0   │       50% v1.1          │
    │   └────────┘ └────────┘ └────────┘ └────────┘                          │
    │                                                                          │
    │   Step 3 & 4: 나머지 Pod도 교체                                          │
    │   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐                          │
    │   │ Pod-1  │ │ Pod-2  │ │ Pod-3  │ │ Pod-4  │   LB ───> 100% v1.1     │
    │   │ v1.1   │ │ v1.1   │ │ v1.1   │ │ v1.1   │                          │
    │   └────────┘ └────────┘ └────────┘ └────────┘                          │
    │                                                                          │
    │   ⚠️ 특징: 자원 효율적, 배포 중新旧혼재, 롤백 느림                       │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘

    [ 2. Blue-Green Deployment - 완전 교체 ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   초기 상태 (Blue - v1.0)                                                │
    │   ┌────────────────────────────────────────┐                            │
    │   │           Blue Environment              │                            │
    │   │  ┌────────┐ ┌────────┐ ┌────────┐     │   LB ───> 100% Blue       │
    │   │  │ Pod-1  │ │ Pod-2  │ │ Pod-3  │     │       (v1.0)              │
    │   │  │ v1.0   │ │ v1.0   │ │ v1.0   │     │                            │
    │   │  └────────┘ └────────┘ └────────┘     │                            │
    │   └────────────────────────────────────────┘                            │
    │                                                                          │
    │   Step 1: Green 환경 구축 (v1.1)                                         │
    │   ┌────────────────────────────────────────┐  ┌───────────────────────┐ │
    │   │           Blue Environment              │  │   Green Environment   │ │
    │   │  ┌────────┐ ┌────────┐ ┌────────┐     │  │ ┌────┐ ┌────┐ ┌────┐ │ │
    │   │  │ Pod-1  │ │ Pod-2  │ │ Pod-3  │     │  │ │Pod │ │Pod │ │Pod │ │ │
    │   │  │ v1.0   │ │ v1.0   │ │ v1.0   │     │  │ │v1.1│ │v1.1│ │v1.1│ │ │
    │   │  └────────┘ └────────┘ └────────┘     │  │ └────┘ └────┘ └────┘ │ │
    │   └────────────────────────────────────────┘  └───────────────────────┘ │
    │                         ↑                              │                │
    │                         │      100% 트래픽             │                │
    │                         └──────────────────────────────┘                │
    │   LB ───> 100% Blue (아직 전환 안 함)                                   │
    │                                                                          │
    │   Step 2: 트래픽 전환 (Switch)                                           │
    │   ┌────────────────────────────────────────┐  ┌───────────────────────┐ │
    │   │           Blue Environment              │  │   Green Environment   │ │
    │   │  (Idle, 대기 상태)                       │  │ (Active)              │ │
    │   │                                         │  │                       │ │
    │   │          ←─── 롤백 시 즉시 전환 가능 ───→│  │                       │ │
    │   └────────────────────────────────────────┘  └───────────────────────┘ │
    │                                                                          │
    │   LB ───> 100% Green (v1.1)  ←  트래픽 스위치!                           │
    │                                                                          │
    │   ⚠️ 특징: 자원 2배 필요, 롤백 즉시(1초),新旧혼재 없음                   │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘

    [ 3. Canary Release - 점진적 노출 ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   Step 1: Canary 1% 배포                                                 │
    │   ┌────────────────────────────────────────────────────────────────┐    │
    │   │                     Load Balancer                              │    │
    │   │                                                                │    │
    │   │    100% 트래픽                                                  │    │
    │   │       │                                                        │    │
    │   │       ├──────────────────────────────────┐                    │    │
    │   │       │                                  │                    │    │
    │   │       ▼                                  ▼                    │    │
    │   │   ┌─────────────┐                  ┌─────────────┐           │    │
    │   │   │   Stable    │   99% 트래픽     │   Canary    │   1% 트래픽│    │
    │   │   │   v1.0      │◄─────────────────│   v1.1      │◄──────────│    │
    │   │   │             │                  │             │           │    │
    │   │   │ 10 Pods     │                  │ 1 Pod       │           │    │
    │   │   └─────────────┘                  └─────────────┘           │    │
    │   │                                                                │    │
    │   │   📊 모니터링: 에러율, 지연 시간, 비즈니스 메트릭 비교          │    │
    │   │   📊 카나리 분석: 통계적 유의성 검증 (Kayenta)                │    │
    │   │                                                                │    │
    │   └────────────────────────────────────────────────────────────────┘    │
    │                                                                          │
    │   Step 2: Canary 10% 확대 (이상 없음)                                    │
    │   ┌────────────────────────────────────────────────────────────────┐    │
    │   │   Stable (90%) ◄──────────────────────────► Canary (10%)      │    │
    │   │                                                                │    │
    │   │   📊 지속적 메트릭 비교:                                       │    │
    │   │   - 에러율: Canary < Stable * 1.1 (임계치)                     │    │
    │   │   - P99 지연: Canary < Stable * 1.05                          │    │
    │   │   - 비즈니스: 전환율 차이 < 5%                                  │    │
    │   │                                                                │    │
    │   └────────────────────────────────────────────────────────────────┘    │
    │                                                                          │
    │   Step 3: 자동 판단                                                      │
    │   ┌────────────────────────────────────────────────────────────────┐    │
    │   │                                                                │    │
    │   │   [ PASS ] 메트릭 정상 → Canary 비율 증가 (10% → 50% → 100%)  │    │
    │   │   [ FAIL ] 메트릭 이상 → 자동 롤백 (Canary 0%)                 │    │
    │   │                                                                │    │
    │   │   ⚠️ 특징: 위험 최소화, 자동화 복잡, A/B 테스트와 유사        │    │
    │   │                                                                │    │
    │   └────────────────────────────────────────────────────────────────┘    │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘

    [ 배포 전략 비교 매트릭스 ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   ┌─────────────┬───────────────┬───────────────┬───────────────┐      │
    │   │    지표      │   Rolling     │  Blue-Green   │    Canary     │      │
    │   ├─────────────┼───────────────┼───────────────┼───────────────┤      │
    │   │ 자원 효율성  │     ⭐⭐⭐⭐    │      ⭐⭐      │     ⭐⭐⭐     │      │
    │   │ 롤백 속도    │     ⭐⭐       │     ⭐⭐⭐⭐⭐  │     ⭐⭐⭐⭐   │      │
    │   │ 위험 최소화  │     ⭐⭐       │      ⭐⭐⭐    │     ⭐⭐⭐⭐⭐  │      │
    │   │ 구현 복잡도  │     ⭐⭐⭐⭐⭐  │      ⭐⭐⭐    │      ⭐⭐      │      │
    │   │ 새실행 검증  │     ⭐⭐       │      ⭐⭐⭐    │     ⭐⭐⭐⭐⭐  │      │
    │   └─────────────┴───────────────┴───────────────┴───────────────┘      │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
```

### 3. Kubernetes 배포 설정 예시

```yaml
# 1. Rolling Update (기본값)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1          # 최대 추가 Pod 수 (초과 허용)
      maxUnavailable: 1    # 최대 불가용 Pod 수
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:v1.1
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5

---
# 2. Blue-Green Deployment (Service 전환 방식)
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
    version: blue    # blue → green으로 전환
  ports:
    - port: 80
      targetPort: 8080

---
# Blue 버전
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
        - name: myapp
          image: myapp:v1.0

---
# Green 버전
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
        - name: myapp
          image: myapp:v1.1

---
# 3. Canary Deployment (Istio VirtualService)
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
            subset: v1
          weight: 90      # 90% Stable
        - destination:
            host: myapp-canary
            subset: v2
          weight: 10      # 10% Canary
      retries:
        attempts: 3
        perTryTimeout: 2s
---
# Canary Analysis (Argo Rollouts)
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    canary:
      steps:
        - setWeight: 5    # 5% Canary
        - pause: {duration: 10m}  # 10분 대기
        - setWeight: 20   # 20% Canary
        - pause: {duration: 10m}
        - setWeight: 50   # 50% Canary
        - pause: {duration: 10m}
      analysis:
        templates:
          - templateName: success-rate
        startingStep: 1
        args:
          - name: service-name
            value: myapp-canary
```

### 4. 카나리 분석 자동화 (Python)

```python
#!/usr/bin/env python3
"""
카나리 분석기 - 메트릭 기반 자동 판단
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import statistics

class AnalysisResult(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    INCONCLUSIVE = "inconclusive"

@dataclass
class MetricThreshold:
    """메트릭 임계값"""
    name: str
    stable_value: float
    canary_value: float
    max_degradation: float  # 최대 허용 저하율 (%)

    def is_healthy(self) -> bool:
        """메트릭이 임계값 내에 있는지 확인"""
        if self.stable_value == 0:
            return self.canary_value == 0

        degradation = ((self.canary_value - self.stable_value) / self.stable_value) * 100
        return degradation <= self.max_degradation

@dataclass
class CanaryConfig:
    """카나리 설정"""
    min_success_duration: int = 600  # 최소 성공 지속 시간 (초)
    max_error_rate: float = 0.01     # 최대 에러율 1%
    max_latency_increase: float = 0.05  # 최대 지연 증가 5%
    min_sample_size: int = 1000      # 최소 샘플 수

class CanaryAnalyzer:
    """카나리 분석기"""

    def __init__(self, config: CanaryConfig):
        self.config = config

    def analyze(
        self,
        stable_metrics: dict,
        canary_metrics: dict,
        sample_size: int
    ) -> AnalysisResult:
        """
        카나리 분석 수행

        Args:
            stable_metrics: Stable 버전 메트릭
            canary_metrics: Canary 버전 메트릭
            sample_size: 분석 샘플 수

        Returns:
            AnalysisResult: 분석 결과
        """
        # 샘플 수 확인
        if sample_size < self.config.min_sample_size:
            return AnalysisResult.INCONCLUSIVE

        # 메트릭 비교
        thresholds = [
            MetricThreshold(
                name="error_rate",
                stable_value=stable_metrics.get("error_rate", 0),
                canary_value=canary_metrics.get("error_rate", 0),
                max_degradation=self.config.max_error_rate * 100
            ),
            MetricThreshold(
                name="p99_latency",
                stable_value=stable_metrics.get("p99_latency", 0),
                canary_value=canary_metrics.get("p99_latency", 0),
                max_degradation=self.config.max_latency_increase * 100
            ),
            MetricThreshold(
                name="p95_latency",
                stable_value=stable_metrics.get("p95_latency", 0),
                canary_value=canary_metrics.get("p95_latency", 0),
                max_degradation=self.config.max_latency_increase * 100
            )
        ]

        # 모든 메트릭이 임계값 내에 있는지 확인
        failed_metrics = [t for t in thresholds if not t.is_healthy()]

        if failed_metrics:
            print(f"❌ Canary analysis failed:")
            for metric in failed_metrics:
                print(f"   - {metric.name}: stable={metric.stable_value}, canary={metric.canary_value}")
            return AnalysisResult.FAILURE

        print(f"✅ Canary analysis passed!")
        return AnalysisResult.SUCCESS

    def calculate_traffic_weight(
        self,
        current_weight: int,
        analysis_result: AnalysisResult
    ) -> int:
        """트래픽 가중치 계산"""
        if analysis_result == AnalysisResult.SUCCESS:
            # 성공 시 가중치 증가
            if current_weight < 10:
                return 10
            elif current_weight < 50:
                return 50
            else:
                return 100
        elif analysis_result == AnalysisResult.FAILURE:
            # 실패 시 0으로 롤백
            return 0
        else:
            # 판단 불가 시 유지
            return current_weight


# 사용 예시
if __name__ == "__main__":
    config = CanaryConfig(
        min_success_duration=600,
        max_error_rate=0.01,
        max_latency_increase=0.05
    )

    analyzer = CanaryAnalyzer(config)

    # 예시 메트릭
    stable_metrics = {
        "error_rate": 0.005,
        "p99_latency": 150,
        "p95_latency": 100
    }

    canary_metrics = {
        "error_rate": 0.008,
        "p99_latency": 155,
        "p95_latency": 105
    }

    result = analyzer.analyze(stable_metrics, canary_metrics, sample_size=5000)
    print(f"Analysis result: {result.value}")
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 배포 전략 상세 비교

| 평가 지표 | Rolling Update | Blue-Green | Canary | A/B Testing |
|:---|:---|:---|:---|:---|
| **배포 속도** | 중간 (점진적) | 빠름 (일괄) | 느림 (검증) | 느림 (실험) |
| **자원 요구량** | N | 2N | N + α | N + α |
| **롤백 속도** | 느림 (역진행) | 즉시 (1초) | 빠름 (트래픽 전환) | 빠름 |
| **위험도** | 중간 (혼재) | 낮음 (격리) | 매우 낮음 (점진) | 낮음 |
| **복잡도** | 낮음 | 중간 | 높음 | 높음 |
| **검증 방식** | 실시간 모니터링 | 사전 테스트 | 실제 트래픽 | 사용자 행동 |
| **적합 서비스** | 일반 웹 | 금융/결제 | 대규모 MSA | 마케팅/실험 |

### 2. 과목 융합 관점 분석

**배포 전략 + 서비스 메시 (Istio)**:
- Istio VirtualService로 정교한 트래픽 분할
- 0.1% 단위 카나리 조정 가능
- mTLS 암호화 하에 배포

**배포 전략 + GitOps (ArgoCD)**:
- 배포 상태를 Git으로 선언적 관리
- 자동화된 카나리 분석 (Argo Rollouts)
- 승인 게이트 (Manual Approval)

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

**시나리오 A: 결제 서비스 배포 전략 선택**
- **상황**: 결제 실패 = 매출 손실, 높은 안정성 요구
- **기술사의 전략적 의사결정**:
  - **전략**: Blue-Green + Canary 혼합
  - 이유: Blue-Green으로 즉시 롤백 가능, Canary로 사전 검증
  - 구현: Argo Rollouts + Istio Traffic Splitting

**시나리오 B: 대규모 MSA 일일 100회 배포**
- **상황**: 빠른 배포 속도, 자원 제약
- **기술사의 전략적 의사결정**:
  - **전략**: Rolling Update + 자동화된 카나리 분석
  - 이유: 자원 효율성 + 자동화된 안전망
  - 구현: Kubernetes Deployment + Prometheus Alerts

### 2. 도입 시 고려사항 (체크리스트)

**기술적 체크리스트**:
- [ ] 헬스 체크 엔드포인트 구현
- [ ] Readiness Probe 설정
- [ ] 트래픽 라우팅 구성 (LB, Service Mesh)
- [ ] 롤백 자동화 (임계치 기반)

**운영적 체크리스트**:
- [ ] 배포 알림 채널 구성
- [ ] 모니터링 대시보드 준비
- [ ] 배포 승인 프로세스 정의

### 3. 주의사항 및 안티패턴

**안티패턴 1: 데이터베이스 스키마 미호환**
- 문제: v1과 v2가 다른 DB 스키마 사용 → Rolling 중 에러
- 해결: Expand-Contract 패턴 (하위 호환 유지)

**안티패턴 2: 세션 불일치**
- 문제: Blue-Green 전환 시 세션 손실
- 해결: 외부 세션 저장소 (Redis) 또는 Sticky Session

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **배포 중단 시간** | 10~30분 | 0분 | 100% 제거 |
| **롤백 시간** | 30분+ | 1초~1분 | 99% 단축 |
| **배포 빈도** | 주 1회 | 일일 수십 회 | 100배 증가 |
| **장애 영향 범위** | 전체 사용자 | 1~5% 사용자 | 95% 감소 |

### 2. 미래 전망 및 진화 방향

**Progressive Delivery**:
- 카나리 → Blue-Green → Rolling의 통합
- 자동화된 메트릭 기반 의사결정
- Feature Flags와 결합

### 3. 참고 표준/가이드

- **Kubernetes Documentation**: Deployments
- **Argo Rollouts**: Progressive Delivery
- **Spinnaker**: Multi-cloud Deployment
- **Martin Fowler**: Blue-Green Deployment

---

## 관련 개념 맵 (Knowledge Graph)

- [CI/CD 파이프라인](@/studynotes/15_devops_sre/03_automation/cicd_gitops.md) : 배포 자동화 기반
- [GitOps](@/studynotes/15_devops_sre/03_automation/gitops.md) : 선언적 배포 관리
- [옵저버빌리티](@/studynotes/15_devops_sre/02_observability/observability_fundamentals.md) : 카나리 분석 기반
- [서비스 메시](@/studynotes/15_devops_sre/03_automation/service_mesh.md) : 트래픽 라우팅
- [Feature Toggle](@/studynotes/15_devops_sre/01_sre/feature_toggle.md) : 런타임 기능 제어

---

## 어린이를 위한 3줄 비유 설명

1. 무중단 배포는 **다리 보수 공사**와 같아요. 다리를 완전히 막는 게 아니라, **차선 하나씩만 막으면서** 공사해요.
2. 블루-그린은 **새 다리를 옆에 놓고**, 다 완성되면 **차들을 한 번에 새 다리로 보내는** 거예요.
3. 카나리는 **소수의 차만 새 다리로 보내서** 안전한지 확인한 후, 점점 더 많은 차를 보내는 거예요!
