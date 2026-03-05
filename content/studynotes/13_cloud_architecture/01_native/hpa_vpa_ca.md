+++
title = "HPA, VPA, CA (오토스케일링 트라이어드)"
date = "2026-03-05"
[extra]
categories = "studynotes-cloud"
tags = ["kubernetes", "hpa", "vpa", "autoscaling", "cluster-autoscaler", "scalability"]
+++

# HPA, VPA, CA (오토스케일링 트라이어드)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: HPA(Horizontal Pod Autoscaler)는 파드 개수를 조절, VPA(Vertical Pod Autoscaler)는 파드 리소스를 조절, CA(Cluster Autoscaler)는 노드 개수를 조절하여 쿠버네티스 클러스터의 3차원 자원 탄력성을 실현합니다.
> 2. **가치**: 트래픽 스파이크에 자동 대응, 리소스 효율 최적화, 비용 절감(과잉 프로비저닝 방지), SLA 달성(부하 대응)을 통합 제공합니다.
> 3. **융합**: Prometheus Custom Metrics, Karpenter(차세대 CA), Predictive Autoscaling과 결합하여 지능형 탄력적 인프라를 구현합니다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의
**HPA(Horizontal Pod Autoscaler)**는 CPU/메모리 사용률 또는 커스텀 메트릭(QPS, 대기열 깊이)에 따라 파드 복제본 수를 자동으로 증감합니다. **VPA(Vertical Pod Autoscaler)**는 파드의 CPU/메모리 Request/Limit을 실제 사용량에 맞춰 자동 조정합니다. **CA(Cluster Autoscaler)**는 Pending 상태의 파드가 있을 때 새 노드를 프로비저닝하거나, 유휴 노드를 종료합니다. 이 세 가지가 "오토스케일링 트라이어드"를 구성합니다.

### 💡 비유
오토스케일링 트라이어드는 "유동적인 식당 운영"과 같습니다. HPA는 "식객이 많으면 테이블(파드)을 늘리는 것", VPA는 "식객이 많이 먹으면 접시 크기(리소스)를 키우는 것", CA는 "식당 전체가 꽉 차면 방(노드)을 늘리는 것"입니다. 셋이 조화롭게 작동해야 대규모 연회도 문제 없이 치릅니다.

### 등장 배경 및 발전 과정

#### 1. 기존 스케일링의 한계
- **수동 스케일링**: 장애 발생 후 대응, MTTR 증가
- **고정 용량**: 피크 기준 과잉 프로비저닝 → 비용 낭비
- **단일 차원**: CPU만 보고 스케일링, 비즈니스 메트릭 무시

#### 2. 패러다임 변화
```
2015년: Kubernetes v1.1 - HPA (CPU 기반) 도입
2017년: v1.6 - HPA Custom Metrics (Alpha)
2018년: v1.9 - VPA (Alpha), CA 정식 릴리스
2019년: v1.18 - HPA v2 (Custom Metrics 안정화)
2020년: v1.20 - VPA Beta
2021년: Karpenter (AWS) - 차세대 CA 등장
2022년: v1.26 - HPA Container Resource Metrics
```

#### 3. 비즈니스적 요구사항
- **블랙 프라이데이**: 10배 트래픽 급증 대응
- **비용 최적화**: 야간/주말 트래픽 감소 시 자원 축소
- **SLA 보장**: P99 지연 < 200ms 유지

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|-----------|------|
| **HPA Controller** | 파드 수평 스케일링 | 메트릭 서버 폴링, 복제본 수 계산 | Metrics Server, Prometheus Adapter | 테이블 추가/제거 |
| **VPA Recommender** | 리소스 추천 | 과거 사용량 분석, 권장값 생성 | OOM 기록, P95 사용량 | 접시 크기 추천 |
| **VPA Updater** | 파드 재시작 | 권장값 적용 위해 파드 Eviction | Pod Disruption Budget | 접시 교체 |
| **VPA Admission Controller** | 리소스 주입 | 파드 생성 시 권장값 적용 | Mutating Webhook | 접시 크기 적용 |
| **Cluster Autoscaler** | 노드 스케일링 | Pending 파드 감지, 노드 프로비저닝 | AWS ASG, GCP MIG | 방 추가/제거 |
| **Karpenter** | 차세대 노드 스케일링 | 파드 요구사항 기반 최적 인스턴스 선택 | Spot, Consolidation | 스마트 방 배정 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      쿠버네티스 오토스케일링 트라이어드                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │                        Metrics Collection                                │  │
│   │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │  │
│   │  │  Metrics Server  │  │Prometheus Adapter│  │ Custom Metrics   │     │  │
│   │  │  (CPU/Memory)    │  │ (Custom Metrics) │  │   API Server     │     │  │
│   │  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘     │  │
│   │           │                     │                     │               │  │
│   │           └─────────────────────┼─────────────────────┘               │  │
│   │                                 │                                     │  │
│   └─────────────────────────────────┼─────────────────────────────────────┘  │
│                                     │                                          │
│          ┌──────────────────────────┼──────────────────────────┐              │
│          │                          │                          │              │
│          ▼                          ▼                          ▼              │
│   ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐     │
│   │       HPA       │      │       VPA       │      │       CA        │     │
│   │  (Horizontal)   │      │   (Vertical)    │      │   (Cluster)     │     │
│   │                 │      │                 │      │                 │     │
│   │  ┌───────────┐  │      │  ┌───────────┐  │      │  ┌───────────┐  │     │
│   │  │ Controller│  │      │ │Recommender│  │      │  │Controller │  │     │
│   │  │           │  │      │  └───────────┘  │      │  │           │  │     │
│   │  │ replicas  │  │      │  ┌───────────┐  │      │  │           │  │     │
│   │  │ = current │  │      │  │  Updater  │  │      │  │ Node     │  │     │
│   │  │ * desired │  │      │  │           │  │      │  │ Provision│  │     │
│   │  │ / current │  │      │  │ Pod      │  │      │  │ / Scale  │  │     │
│   │  └───────────┘  │      │  │ Eviction │  │      │  │ Down     │  │     │
│   │                 │      │  └───────────┘  │      │  └───────────┘  │     │
│   │                 │      │  ┌───────────┐  │      │                 │     │
│   │                 │      │  │ Admission │  │      │                 │     │
│   │                 │      │  │Controller │  │      │                 │     │
│   │                 │      │  └───────────┘  │      │                 │     │
│   └────────┬────────┘      └────────┬────────┘      └────────┬────────┘     │
│            │                        │                        │               │
│            ▼                        ▼                        ▼               │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      Scaling Actions                                 │   │
│   │                                                                      │   │
│   │  HPA Action:         VPA Action:          CA Action:                │   │
│   │  ┌─────────────┐     ┌─────────────┐      ┌─────────────┐           │   │
│   │  │ replicas: 3 │     │ cpu: 500m   │      │ +Node       │           │   │
│   │  │     ↓       │     │ mem: 512Mi  │      │ (New EC2)   │           │   │
│   │  │ replicas: 5 │     │     ↓       │      │             │           │   │
│   │  │ (+2 pods)   │     │ cpu: 1000m  │      │ or -Node    │           │   │
│   │  └─────────────┘     │ mem: 1Gi    │      │ (Remove     │           │   │
│   │                      │ (restart)   │      │  Idle Node) │           │   │
│   │                      └─────────────┘      └─────────────┘           │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    Scaling Decision Flow                             │   │
│   │                                                                      │   │
│   │   [Metrics]                                                          │   │
│   │      │                                                               │   │
│   │      ▼                                                               │   │
│   │   ┌──────────────────────────────────────────┐                      │   │
│   │   │        HPA Algorithm                      │                      │   │
│   │   │                                          │                      │   │
│   │   │  desiredReplicas = ceil[                 │                      │   │
│   │   │    currentReplicas *                     │                      │   │
│   │   │    (currentMetricValue / desiredValue)   │                      │   │
│   │   │  ]                                        │                      │   │
│   │   │                                          │                      │   │
│   │   │  Example:                                │                      │   │
│   │   │  - current: 3 pods                       │                      │   │
│   │   │  - currentMetric: 70% CPU                │                      │   │
│   │   │  - desiredMetric: 50% CPU                │                      │   │
│   │   │  - desiredReplicas = ceil[3 * 70/50] = 5 │                      │   │
│   │   └──────────────────────────────────────────┘                      │   │
│   │                                                                      │   │
│   │   ┌──────────────────────────────────────────┐                      │   │
│   │   │        VPA Algorithm                      │                      │   │
│   │   │                                          │                      │   │
│   │   │  Recommended = P95(history) * buffer     │                      │   │
│   │   │                                          │                      │   │
│   │   │  Update modes:                           │                      │   │
│   │   │  - Off: 추천만                           │                      │   │
│   │   │  - Initial: 파드 생성 시만 적용           │                      │   │
│   │   │  - Recreate: 파드 재시작으로 적용         │                      │   │
│   │   │  - Auto: 자동 (현재 Recreate와 동일)     │                      │   │
│   │   └──────────────────────────────────────────┘                      │   │
│   │                                                                      │   │
│   │   ┌──────────────────────────────────────────┐                      │   │
│   │   │        CA Algorithm                       │                      │   │
│   │   │                                          │                      │   │
│   │   │  Scale Up:                               │                      │   │
│   │   │  - pendingPods > 0 && unresolvable       │                      │   │
│   │   │  - Provision new node                    │                      │   │
│   │   │                                          │                      │   │
│   │   │  Scale Down:                             │                      │   │
│   │   │  - node.utilization < 50% for 10min      │                      │   │
│   │   │  - all pods can move elsewhere           │                      │   │
│   │   │  - Remove node                           │                      │   │
│   │   └──────────────────────────────────────────┘                      │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

#### ① HPA 알고리즘 상세

```python
"""
HPA (Horizontal Pod Autoscaler) 알고리즘 구현
"""

import math
from typing import List, Dict

class HorizontalPodAutoscaler:
    """HPA 스케일링 알고리즘 시뮬레이션"""

    def __init__(self,
                 min_replicas: int = 1,
                 max_replicas: int = 10,
                 target_cpu_utilization: float = 50.0,
                 stabilization_window_seconds: int = 300):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.target_cpu = target_cpu_utilization
        self.stabilization_window = stabilization_window_seconds
        self.scaling_history: List[Dict] = []

    def calculate_desired_replicas(self,
                                    current_replicas: int,
                                    current_metric_value: float) -> int:
        """
        HPA 핵심 알고리즘

        공식:
        desiredReplicas = ceil[currentReplicas * (currentMetric / desiredMetric)]
        """
        # ============================================
        # Step 1: 기본 스케일링 비율 계산
        # ============================================
        raw_desired = current_replicas * (current_metric_value / self.target_cpu)

        # ============================================
        # Step 2: 소수점 올림 (최소 리소스 보장)
        # ============================================
        desired_replicas = math.ceil(raw_desired)

        # ============================================
        # Step 3: 경계값 검사 (min/max)
        # ============================================
        desired_replicas = max(self.min_replicas, desired_replicas)
        desired_replicas = min(self.max_replicas, desired_replicas)

        # ============================================
        # Step 4: 스케일 다운 안정화 (Cooldown)
        # ============================================
        # 급격한 스케일 다운 방지
        if desired_replicas < current_replicas:
            # 이전 스케일 업이 있었다면 일정 시간 대기
            recent_scale_ups = [
                h for h in self.scaling_history
                if h['action'] == 'scale_up'
                and (time.time() - h['timestamp']) < self.stabilization_window
            ]
            if recent_scale_ups:
                # 안정화 윈도우 내에는 스케일 다운 보류
                return current_replicas

        return desired_replicas

    def calculate_with_multiple_metrics(self,
                                         current_replicas: int,
                                         metrics: Dict[str, tuple]) -> int:
        """
        다중 메트릭 지원 (CPU + Memory + Custom)

        각 메트릭별로 원하는 복제본 수를 계산하고,
        최대값을 선택 (가장 보수적)
        """
        desired_per_metric = []

        for metric_name, (current, target) in metrics.items():
            ratio = current / target
            desired = math.ceil(current_replicas * ratio)
            desired_per_metric.append(desired)
            print(f"  {metric_name}: current={current}, target={target}, "
                  f"ratio={ratio:.2f}, desired={desired}")

        # 가장 큰 값 선택 (모든 메트릭 충족)
        final_desired = max(desired_per_metric)

        return self._apply_bounds(final_desired)

    def calculate_with_behavior(self,
                                current_replicas: int,
                                current_metric: float) -> dict:
        """
        HPA v2 Behavior 지원 (세밀한 스케일링 제어)

        behavior:
          scaleDown:
            stabilizationWindowSeconds: 300
            policies:
            - type: Percent
              value: 10
              periodSeconds: 60
            - type: Pods
              value: 2
              periodSeconds: 60
            selectPolicy: Min
          scaleUp:
            stabilizationWindowSeconds: 0
            policies:
            - type: Percent
              value: 100
              periodSeconds: 15
            - type: Pods
              value: 4
              periodSeconds: 15
            selectPolicy: Max
        """
        base_desired = self.calculate_desired_replicas(current_replicas, current_metric)

        result = {
            'current_replicas': current_replicas,
            'current_metric': current_metric,
            'target_metric': self.target_cpu,
            'raw_desired': base_desired,
            'final_desired': base_desired,
            'action': 'none',
            'policies_applied': []
        }

        # ============================================
        # Scale Up 정책 적용
        # ============================================
        if base_desired > current_replicas:
            # 최대 100% 증가 또는 4개 파드 추가 중 작은 값
            max_percent_increase = current_replicas  # 100%
            max_pods_increase = 4

            policy_limit = min(max_percent_increase, max_pods_increase)
            allowed_desired = min(base_desired, current_replicas + policy_limit)

            result['final_desired'] = allowed_desired
            result['action'] = 'scale_up'
            result['policies_applied'].append(f'Max increase: {policy_limit} pods')

        # ============================================
        # Scale Down 정책 적용
        # ============================================
        elif base_desired < current_replicas:
            # 최대 10% 감소 또는 2개 파드 감소 중 큰 값
            max_percent_decrease = current_replicas // 10  # 10%
            max_pods_decrease = 2

            policy_limit = max(max_percent_decrease, max_pods_decrease)
            allowed_desired = max(base_desired, current_replicas - policy_limit)

            result['final_desired'] = allowed_desired
            result['action'] = 'scale_down'
            result['policies_applied'].append(f'Max decrease: {policy_limit} pods')

        return result


# ============================================
# 실제 HPA YAML 예시
# ============================================
HPA_EXAMPLE = """
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-api-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-api
  minReplicas: 3
  maxReplicas: 50
  metrics:
  # 기본 CPU 메트릭
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70

  # 메모리 메트릭
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80

  # 커스텀 메트릭 (Prometheus)
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"

  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Min
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
"""
```

#### ② CA vs Karpenter 비교

```yaml
# Cluster Autoscaler 설정 예시
# ============================================
# 기본 CA (AWS EKS)
# ============================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  template:
    spec:
      containers:
      - name: cluster-autoscaler
        image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.25.0
        command:
        - ./cluster-autoscaler
        - --v=4
        - --stderrthreshold=info
        - --cloud-provider=aws
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste      # 노드 선택 전략
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/my-cluster
        - --balance-similar-node-groups
        - --max-node-provision-time=15m
        env:
        - name: AWS_REGION
          value: us-west-2
        resources:
          limits:
            cpu: 100m
            memory: 300Mi
          requests:
            cpu: 100m
            memory: 300Mi

---
# ============================================
# Karpenter (차세대 CA)
# ============================================
# Karpenter는 별도 Provisioner CRD로 정의
apiVersion: karpenter.sh/v1beta1
kind: Provisioner
metadata:
  name: default
spec:
  requirements:
    # 인스턴스 타입 자동 선택 (파드 요구사항 기반)
    - key: karpenter.k8s.aws/instance-category
      operator: In
      values: [c, m, r]
    - key: karpenter.k8s.aws/instance-generation
      operator: Gt
      values: ["5"]
  providerRef:
    name: default
  # 노드 TTL (사용 없으면 종료)
  ttlSecondsUntilExpired: 2592000  # 30일
  # 빈 노드 종료
  ttlSecondsAfterEmpty: 30
  # Consolidation (자동 최적화)
  consolidation:
    enabled: true

---
apiVersion: karpenter.k8s.aws/v1beta1
kind: AWSNodeTemplate
metadata:
  name: default
spec:
  subnetSelector:
    karpenter.sh/discovery: my-cluster
  securityGroupSelector:
    karpenter.sh/discovery: my-cluster
  # Spot 인스턴스 활용
  spot: true
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 스케일링 방식

| 비교 항목 | HPA | VPA | CA | Karpenter |
|-----------|-----|-----|----|-----------|----|
| **스케일링 대상** | 파드 수 | 파드 리소스 | 노드 수 | 노드 수 |
| **스케일링 방향** | 수평 | 수직 | 수평 | 수평 |
| **중단 여부** | 없음 | 있음 (재시작) | 없음 | 없음 |
| **응답 시간** | 초~분 | 분~시간 | 분~10분 | 초~분 |
| **메트릭** | CPU/메모리/커스텀 | 과거 사용량 | Pending 파드 | Pending 파드 |
| **비용 최적화** | 중간 | 높음 | 중간 | 높음 |
| **복잡도** | 낮음 | 중간 | 중간 | 중간 |
| **제약** | 파드 최대 개수 | 재시작 필요 | 노드 프로비저닝 시간 | 베타 (AWS만) |

### HPA + VPA 함께 사용하기

```
HPA와 VPA 동시 사용 가이드:

1. 권장 조합:
   - HPA: CPU/메모리 기반 (기본)
   - VPA: UpdateMode = "Off" 또는 "Initial"

2. 권장하지 않는 조합:
   - HPA + VPA "Auto" = 충돌 가능
   - VPA가 CPU를 올리면 HPA가 파드를 늘림 → 진동

3. 모범 사례:
   ┌─────────────────────────────────────────────────────────┐
   │  VPA Mode: Initial (파드 생성 시만)                     │
   │  HPA: Custom Metrics (QPS, Latency) 기반               │
   │                                                         │
   │  이유:                                                  │
   │  - VPA는 초기 리소스를 적절히 설정                     │
   │  - HPA는 비즈니스 메트릭으로 스케일링                  │
   │  - CPU 기반 HPA는 VPA 조정에 민감하지 않음             │
   └─────────────────────────────────────────────────────────┘

4. 대안: VPA만 사용
   - 워크로드가 상태 저장(Stateful)인 경우
   - 단일 파드로 충분한 경우 (데이터베이스)
```

### 과목 융합 관점 분석

#### [쿠버네티스 + 클라우드 비용] FinOps와 오토스케일링
```
오토스케일링의 FinOps 활용:

1. Right-Sizing (VPA)
   - 과잉 프로비저닝 감지: Request >> Usage
   - VPA 추천으로 리소스 감축
   - 비용 절감: 30-50%

2. Spot Instance 활용 (CA/Karpenter)
   - Karpenter spot: true
   - Spot Interruption Handling
   - 비용 절감: 60-90%

3. 스케줄 기반 스케일링
   # 영업시간 외 축소
   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: cron-scaled-hpa
   spec:
     scaleTargetRef:
       name: web-api
     minReplicas: 3  # 기본
     maxReplicas: 50
     # Cron HPA로 오버라이드
   ---
   apiVersion: autoscaling/v2beta2
   kind: CronHorizontalPodAutoscaler
   spec:
     scaleTargetRef:
       name: web-api
     jobs:
     - name: scale-down-night
       schedule: "0 22 * * *"
       minReplicas: 1
       maxReplicas: 5
     - name: scale-up-morning
       schedule: "0 8 * * *"
       minReplicas: 10
       maxReplicas: 50

4. 비용 가시성
   - Kubernetes Resource Cost Allocation
   - Namespace/Deployment별 비용 추적
   - Kubecost, CloudHealth 활용
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 시나리오

#### 시나리오 1: 이커머스 블랙 프라이데이
```
요구사항:
- 평소: 1K RPS
- 블랙 프라이데이: 100K RPS (100배)
- 무중단, 자동 대응
- 비용 최적화

기술사 판단:

1. 사전 준비 (1주 전):
   - HPA maxReplicas 증가: 50 → 200
   - CA maxNodes 증가: 20 → 100
   - 워밍업: 미리 노드 확보 (Pre-scaling)

2. HPA 설정:
   metrics:
   - type: Pods
     pods:
       metric:
         name: http_requests_per_second
       target:
         type: AverageValue
         averageValue: "500"  # 파드당 500 RPS

   behavior:
     scaleUp:
       stabilizationWindowSeconds: 0
       policies:
       - type: Percent
         value: 900  # 최대 10배 증가
         periodSeconds: 15

3. Karpenter Spot 활용:
   - 80% Spot, 20% On-Demand
   - Spot 중단 시 자동 대체

4. 모니터링 대시보드:
   - HPA 상태, Pending 파드, 노드 수
   - RPS, P99 Latency, 에러율
   - 비용 실시간 추적

5. 롤백 계획:
   - 트래픽 감소 후 자동 축소
   - 수동 개입 시나리오 준비
```

### 도입 시 고려사항 체크리스트

#### 기술적 고려사항
- [ ] **메트릭 서버**: Metrics Server 설치, Prometheus Adapter
- [ ] **리소스 Request/Limit**: 적절한 초기값 설정 (VPA용)
- [ ] **PDB**: Pod Disruption Budget으로 가용성 보장
- [ ] **쿼터**: ResourceQuota로 무제한 스케일링 방지

#### 운영적 고려사항
- [ ] **알림**: 스케일링 이벤트 알림
- [ ] **비용**: 스케일 아웃 시 비용 폭증 경고
- [ ] **테스트**: 부하 테스트로 스케일링 검증

### 주의사항 및 안티패턴

#### 안티패턴 1: HPA 없이 CA만 사용
```
잘못된 접근:
- CA만 설정하고 HPA 없음
- 파드는 항상 최대 replica로 고정

문제:
- 노드는 스케일링되지만 파드는 안 됨
- 리소스 낭비, 비용 증가

해결:
- HPA + CA 조합 필수
- HPA가 파드를 늘리고, CA가 노드를 늘림
```

#### 안티패턴 2: VPA Auto와 CPU 기반 HPA 동시 사용
```
잘못된 접근:
- VPA mode: Auto
- HPA metric: CPU Utilization

문제:
- VPA가 CPU Request를 올림
- CPU Utilization이 떨어짐
- HPA가 파드를 줄임
- 다시 VPA가 CPU를 내림
- 무한 루프 (Thrashing)

해결:
- VPA mode: Initial 또는 Off
- HPA metric: Custom (QPS, Latency)
- 또는 VPA만 사용 (단일 파드 워크로드)
```

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 구분 | 수동 스케일링 | 오토스케일링 | 개선효과 |
|-----------|-------------|-------------|---------|
| 장애 대응 시간 | 30분+ | 1-5분 | -90% |
| 비용 효율 | 60% (과잉) | 90% | +50% |
| SLA 달성 | 95% | 99.9% | +4.9% |
| 운영 인력 | 24/7 대기 | 자동화 | 인력 80% 절감 |

### 미래 전망 및 진화 방향

1. **Predictive Autoscaling**: ML 기반 트래픽 예측
2. **Karpenter 확산**: 멀티 클라우드 지원
3. **Serverless K8s**: AWS Fargate, GKE Autopilot

### 참고 표준/가이드
- **Kubernetes HPA**: k8s.io/docs/tasks/run-application/horizontal-pod-autoscale/
- **Kubernetes VPA**: github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler
- **Karpenter**: karpenter.sh

---

## 관련 개념 맵 (Knowledge Graph)

1. [쿠버네티스 (Kubernetes)](./kubernetes.md)
   - 관계: K8s의 핵심 탄력성 메커니즘

2. [파드 생명주기 (Pod Lifecycle)](./pod_lifecycle.md)
   - 관계: VPA 재시작과 연동

3. [옵저버빌리티 (Observability)](./observability.md)
   - 관계: 메트릭 수집이 스케일링 기반

4. [FinOps (클라우드 비용)](./finops.md)
   - 관계: 비용 최적화의 핵심 수단

5. [데브옵스 (DevOps)](./devops.md)
   - 관계: 자동화된 운영의 일환

6. [서비스 (Service)](./k8s_networking.md)
   - 관계: 스케일링 시 트래픽 분산

---

## 어린이를 위한 3줄 비유 설명

**비유: 유동적인 식당 운영**

HPA는 식당에 손님이 많으면 테이블(파드)을 늘리는 거예요. VPA는 손님이 많이 먹으면 접시 크기(리소스)를 키우는 거고요. CA는 식당 방(노드)이 꽉 차면 새로운 방을 빌리는 거예요.

**원리:**
셋이 같이 일해요. 손님이 몰리면 HPA가 테이블을 늘리고, 더 이상 늘릴 자리가 없으면 CA가 새 방을 빌려요. 접시가 너무 작으면 VPA가 더 큰 접시로 바꿔요.

**효과:**
이렇게 하면 손님이 아무리 와도 기다리지 않고 바로 식사할 수 있어요. 손님이 적으면 자동으로 테이블과 방을 줄여서 돈도 아끼죠!
