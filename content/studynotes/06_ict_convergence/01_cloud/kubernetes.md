+++
title = "쿠버네티스 (Kubernetes)"
description = "컨테이너 오케스트레이션의 사실상 표준: 쿠버네티스 아키텍처, 핵심 개념 및 실무 운영 전략을 다루는 심층 기술 백서"
date = 2024-05-18
[taxonomies]
tags = ["Kubernetes", "K8s", "Container Orchestration", "Cloud Native", "DevOps", "Microservices"]
+++

# 쿠버네티스 (Kubernetes)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 수천 개의 컨테이너를 자동으로 배포, 스케일링, 관리하는 오픈소스 컨테이너 오케스트레이션 플랫폼으로, 선언적 API(Declarative API)와 Desired State Pattern을 통해 인프라를 코드로 정의하고 자동화합니다.
> 2. **가치**: Auto-healing(자가 치유), Auto-scaling(자동 확장), Rolling Update(무중단 배포), Service Discovery를 통해 99.99% 이상의 가용성을 달성하며, 멀티 클라우드/하이브리드 클라우드 환경의 이식성을 보장합니다.
> 3. **융합**: CI/CD(GitOps), Service Mesh(Istio), Observability(Prometheus/Grafana), Serverless(Knative)와 결합하여 클라우드 네이티브(Cloud Native) 생태계의 핵심 운영체제로 자리 잡았습니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
쿠버네티스(Kubernetes, K8s)는 구글이 개발하여 2014년 오픈소스로 공개한 컨테이너 오케스트레이션 플랫폼입니다. "K8s"는 Kubernetes의 'K'와 's' 사이에 8글자가 있다는 의미입니다. 쿠버네티스는 **Desired State(원하는 상태)**를 YAML/JSON 매니페스트로 선언하면, 현재 상태(Current State)를 지속적으로 모니터링하며 원하는 상태로 수렴(Reconcile)시키는 **선언적(Declarative)** 관리 방식을 채택합니다. 이는 "어떻게 할 것인가(Imperative)"가 아닌 "무엇이 되어야 하는가(Declarative)"를 정의하는 패러다임 전환입니다.

### 2. 구체적인 일상생활 비유
쿠버네티스는 '자동화된 오케스트라 지휘자'입니다. 오케스트라(컨테이너 클러스터)에는 수백 명의 연주자(컨테이너)가 있습니다. 지휘자(쿠버네티스 Control Plane)는 악보(YAML 매니페스트)를 보고, 각 연주자가 제자리에 앉았는지, 올바른 악기를 연주하는지, 병결로 빠진 연주자는 없는지 실시간으로 확인합니다. 어떤 연주자가 쓰러지면(Auto-healing) 즉시 대체 연주자를 불러오고, 객석이 꽉 차면(HPA) 연주자를 더 추가하고, 공연 중에도 악보를 바꾸면(Rolling Update) 모든 연주자가 새로운 악보로 바꿔 연주합니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (수동 관리와 Borg의 교훈)**:
   도커(Docker)의 등장으로 컨테이너 기술이 대중화되었으나, 수천 개의 컨테이너를 수동으로 배포하고 관리하는 것은 불가능했습니다. 구글은 내부적으로 **Borg**와 **Omega**라는 컨테이너 오케스트레이션 시스템을 10년 이상 운영하며 얻은 노하우를 바탕으로 쿠버네티스를 설계했습니다. 기존의 수동 스크립트, Puppet/Chef와 같은 구성 관리 도구는 상태를 유지하는 데 한계가 있었습니다.

2. **혁신적 패러다임 변화의 시작**:
   2014년 6월 구글이 쿠버네티스 v1.0을 발표하고 CNCF(Cloud Native Computing Foundation)에 기부했습니다. 선언적 API, Controller Pattern, Microservices Architecture에 최적화된 설계로, AWS EKS, Google GKE, Azure AKS 등 모든 주요 클라우드 제공자가 매니지드 서비스로 제공하기 시작했습니다. 현재는 컨테이너 오케스트레이션의 **사실상 표준(De Facto Standard)**이 되었습니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   마이크로서비스 아키테처(MSA)의 보편화로 인해 수백 개의 서비스가 서로 통신하는 복잡한 환경에서, 수동 배포와 운영은 더 이상 불가능합니다. GitOps(ArgoCD, Flux), Service Mesh(Istio, Linkerd), Observability 스택이 쿠버네티스 위에서 동작하며, **Platform Engineering**의 핵심 기반이 되고 있습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Module) | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/API | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **API Server** | 모든 요청의 진입점, 인증/인가 | RESTful API, OpenAPI, Admission Webhook | kube-apiserver | 호텔 프론트데스크 |
| **etcd** | 클러스터 상태 저장소 | Raft 합의 알고리즘, Key-Value DB | etcdctl, Backup/Restore | 호텔 등기소 |
| **Scheduler** | 파드 배치 결정 | 필터링(Fit) -> 점수(Score) -> 바인딩 | kube-scheduler, PodTopologySpread | 객실 배정 담당 |
| **Controller Manager** | Desired State 유지 | Reconciliation Loop, Watch API | Deployment, ReplicaSet, Job | 객실 관리 담당 |
| **Kubelet** | 노드 에이전트, 파드 실행 | CRI(Container Runtime), CNI, CSI | kubelet, Pod Lifecycle | 객실 청소 담당 |
| **Kube-proxy** | 서비스 네트워크 프록시 | iptables, IPVS, eBPF | Service, Endpoints | 호텔 안내데스크 |

### 2. 정교한 구조 다이어그램: 쿠버네티스 클러스터 아키텍처

```text
=====================================================================================================
                          [ Kubernetes Cluster Architecture ]
=====================================================================================================

+-----------------------------------------------------------------------------------------+
|                              [ Control Plane (Master Nodes) ]                           |
|                                                                                         |
|  +----------------+    +----------------+    +----------------+    +----------------+  |
|  |  API Server    |<-->|     etcd       |    |   Scheduler    |    |  Controller    |  |
|  | (kube-apiserver)|   | (Key-Value DB) |    | (kube-scheduler)|   | Manager        |  |
|  |                |    |                |    |                |    | (kube-control- |  |
|  | - REST API     |    | - Raft Consensus|   | - Pod Placement|    | manager)       |  |
|  | - AuthZ/AuthN  |    | - State Store  |    | - Bin-packing  |    | - Reconcile    |  |
|  +-------+--------+    +----------------+    +----------------+    |   Loops        |  |
|          |                                                              +--------+-------+  |
|          |                                                                       |          |
+----------|-----------------------------------------------------------------------|----------+
           |                                                                       |
           | kubectl / API Calls                                                  | Watch API
           |                                                                       |
+----------|-----------------------------------------------------------------------|----------+
|          |                              [ Data Plane (Worker Nodes) ]            |          |
|          |                                                                       |          |
|  +-------v--------+    +----------------+    +----------------+    +------------v-------+  |
|  |    Kubelet     |    |  Kube-proxy    |    | Container      |    |     Pods            |  |
|  | (Node Agent)   |    | (Network Proxy)|    | Runtime        |    |  +--------------+   |  |
|  |                |    |                |    | (containerd,   |    |  | Pod 1        |   |  |
|  | - Pod Lifecycle|    | - iptables/IPVS|   |  CRI-O, Docker)|   |  | - Container A|   |  |
|  | - Health Check |    | - Service VIP  |    |                |    |  | - Container B|   |  |
|  | - CRI/CNI/CSI  |    | - Load Balance |    | - RunC, gVisor |    |  +--------------+   |  |
|  +----------------+    +----------------+    +----------------+    |  | Pod 2        |   |  |
|                                                                |  | - Container C|   |  |
|                                                                |  +--------------+   |  |
|                                                                +---------------------+  |
|                                                                                         |
+-----------------------------------------------------------------------------------------+

=====================================================================================================
                          [ Controller Pattern: Reconciliation Loop ]
=====================================================================================================

    [ User ]                       [ Controller ]                      [ Cluster State ]
        |                               |                                    |
        | kubectl apply -f deployment.yaml                                   |
        |------------------------------->|                                    |
        |                               | Watch API (Watch for changes)      |
        |                               |------------------------------------>|
        |                               |                                    |
        |                               | Compare Desired vs Current State   |
        |                               |----------------------------------->|
        |                               |                                    |
        |                               | Current != Desired?                |
        |                               |<-----------------------------------|
        |                               |                                    |
        |                               | Create/Update/Delete Resources     |
        |                               |------------------------------------>|
        |                               |                                    |
        |                               | Loop continues indefinitely...     |
        |                               |----------------------------------->|
```

### 3. 심층 동작 원리 (Pod 생성 프로세스)

사용자가 `kubectl apply -f nginx-deployment.yaml`를 실행했을 때의 내부 동작입니다.

1. **인증 및 인가 (Authentication & Authorization)**:
   kubectl은 kubeconfig 파일에 저장된 인증서/토큰을 사용하여 API Server에 연결합니다. API Server는 Webhook(OpenID Connect, RBAC)을 통해 사용자의 신원과 권한을 확인합니다.

2. **어드미션 컨트롤 (Admission Control)**:
   요청이 etcd에 저장되기 전에, Mutating Admission Controller(예: PodPreset, Sidecar Injection)가 요청을 수정하고, Validating Admission Controller(예: LimitRanger, PodSecurityPolicy)가 요청의 유효성을 검증합니다.

3. **etcd 저장 및 이벤트 발행**:
   검증된 요청은 etcd에 저장되고, API Server는 Watch API를 통해 이벤트를 구독 중인 Controller와 Scheduler에게 알립니다.

4. **스케줄링 (Scheduling)**:
   Scheduler는 필터링(Predicates)을 통해 파드를 실행할 수 있는 노드를 찾고, 점수 매기기(Priorities)를 통해 최적의 노드를 선택합니다. 선택된 노드로 파드를 바인딩(Binding)합니다.

5. **파드 실행 (Kubelet & CRI)**:
   Kubelet은 바인딩된 파드를 감지하고, CRI(Container Runtime Interface)를 통해 containerd에게 컨테이너 생성을 요청합니다. CNI(Container Network Interface)로 파드에 IP를 할당하고, CSI(Container Storage Interface)로 볼륨을 마운트합니다.

6. **상태 보고 및 조정 (Reporting & Reconciliation)**:
   Kubelet은 파드 상태를 API Server에 주기적으로 보고합니다. Controller는 Desired State(Replicas: 3)와 Current State(Running: 2)를 비교하여, 부족한 1개를 추가 생성합니다.

### 4. 핵심 알고리즘 및 실무 코드 예시

쿠버네티스 YAML 매니페스트 예시와 Horizontal Pod Autoscaler(HPA) 구현 로직입니다.

```yaml
# nginx-deployment.yaml - 선언적(Declarative) 배포 정의
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: production
  labels:
    app: nginx
    tier: frontend
spec:
  replicas: 3                        # Desired State: 3개의 파드 복제본
  selector:
    matchLabels:
      app: nginx
  strategy:
    type: RollingUpdate              # 무중단 배포 전략
    rollingUpdate:
      maxSurge: 1                    # 최대 1개 추가 파드 허용
      maxUnavailable: 0              # 0개 파드 중단 허용 (Blue-Green)
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.25-alpine
        ports:
        - containerPort: 80
        resources:
          requests:                  # 최소 보장 자원
            cpu: "100m"
            memory: "128Mi"
          limits:                    # 최대 사용 자원
            cpu: "500m"
            memory: "512Mi"
        livenessProbe:               # 생존 확인 (실패 시 재시작)
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 5
        readinessProbe:              # 준비 확인 (트래픽 수신 가능 여부)
          httpGet:
            path: /ready
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 3
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer                # 클라우드 LB 자동 프로비저닝
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-deployment
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70       # CPU 70% 초과 시 스케일 아웃
```

```python
# HPA (Horizontal Pod Autoscaler) 핵심 로직 시뮬레이션
import time
from dataclasses import dataclass
from typing import List

@dataclass
class Pod:
    name: str
    cpu_utilization: float
    status: str = "Running"

@dataclass
class Deployment:
    name: str
    replicas: int
    pods: List[Pod]

class HorizontalPodAutoscaler:
    """
    쿠버네티스 HPA의 핵심 스케일링 알고리즘 시뮬레이션
    - 메트릭 서버로부터 CPU/메모리 사용률 수집
    - 목표 사용률과 비교하여 복제본 수 조정
    """

    def __init__(self, deployment: Deployment, target_cpu: float, min_replicas: int, max_replicas: int):
        self.deployment = deployment
        self.target_cpu = target_cpu
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.stabilization_window = 300  # 5분 안정화 윈도우

    def calculate_desired_replicas(self) -> int:
        """
        HPA 공식: desiredReplicas = ceil[currentReplicas * (currentMetricValue / desiredMetricValue)]
        """
        if not self.deployment.pods:
            return self.min_replicas

        # 현재 모든 파드의 평균 CPU 사용률 계산
        current_cpu_avg = sum(p.cpu_utilization for p in self.deployment.pods) / len(self.deployment.pods)

        # 스케일링 비율 계산
        ratio = current_cpu_avg / self.target_cpu
        desired_replicas = int((self.deployment.replicas * ratio) + 0.5)  # 반올림

        # min/max 제한 적용
        desired_replicas = max(self.min_replicas, min(self.max_replicas, desired_replicas))

        print(f"[HPA] Current CPU: {current_cpu_avg:.1f}% | Target: {self.target_cpu}% | Ratio: {ratio:.2f}")
        print(f"[HPA] Current Replicas: {self.deployment.replicas} -> Desired Replicas: {desired_replicas}")

        return desired_replicas

    def reconcile(self):
        """
        Controller Pattern: 지속적으로 Desired State로 수렴
        """
        desired = self.calculate_desired_replicas()
        current = self.deployment.replicas

        if desired > current:
            # Scale Out
            for i in range(desired - current):
                new_pod = Pod(name=f"{self.deployment.name}-{current + i + 1}", cpu_utilization=0.0)
                self.deployment.pods.append(new_pod)
            self.deployment.replicas = desired
            print(f"[HPA] Scaled OUT: Added {desired - current} pods")

        elif desired < current:
            # Scale In
            for _ in range(current - desired):
                self.deployment.pods.pop()
            self.deployment.replicas = desired
            print(f"[HPA] Scaled IN: Removed {current - desired} pods")

    def run_loop(self, iterations: int = 10):
        """
        메트릭 수집 -> 계산 -> 조정의 무한 루프 시뮬레이션
        """
        for i in range(iterations):
            print(f"\n=== Iteration {i + 1} ===")

            # 메트릭 업데이트 시뮬레이션 (실제로는 Metrics Server에서 수집)
            import random
            for pod in self.deployment.pods:
                # 부하 증가/감소 시뮬레이션
                if i < 5:
                    pod.cpu_utilization = min(100, pod.cpu_utilization + random.uniform(5, 15))
                else:
                    pod.cpu_utilization = max(10, pod.cpu_utilization - random.uniform(5, 10))

            self.reconcile()
            time.sleep(0.5)


if __name__ == "__main__":
    # 초기 배포 생성
    initial_pods = [
        Pod(name="nginx-1", cpu_utilization=50.0),
        Pod(name="nginx-2", cpu_utilization=55.0),
        Pod(name="nginx-3", cpu_utilization=48.0),
    ]
    deployment = Deployment(name="nginx-deployment", replicas=3, pods=initial_pods)

    # HPA 생성 (목표 CPU 70%, 최소 3, 최대 10)
    hpa = HorizontalPodAutoscaler(deployment, target_cpu=70.0, min_replicas=3, max_replicas=10)

    # 오토스케일링 루프 실행
    hpa.run_loop(iterations=10)

    # 출력 예시:
    # [HPA] Current CPU: 51.0% | Target: 70.0% | Ratio: 0.73
    # [HPA] Current Replicas: 3 -> Desired Replicas: 3
    # (부하 증가 후)
    # [HPA] Current CPU: 85.0% | Target: 70.0% | Ratio: 1.21
    # [HPA] Scaled OUT: Added 1 pods
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 컨테이너 오케스트레이션 도구

| 평가 지표 | Kubernetes | Docker Swarm | Nomad (HashiCorp) | ECS (AWS) |
| :--- | :--- | :--- | :--- | :--- |
| **학습 곡선** | 높음 (복잡한 개념) | 낮음 (간단한 구성) | 중간 | 중간 |
| **확장성** | **수만 노드** | 수천 노드 | 수천 노드 | AWS 리전 내 |
| **기능 풍부도** | **매우 높음** (CRD, Operator) | 기본적 | 높음 (Multi-Workload) | 높음 (AWS 통합) |
| **멀티 클라우드** | **완벽 지원** | 지원 | 지원 | AWS 전용 |
| **생태계** | **압도적** (CNCF) | 제한적 | 성장 중 | AWS 생태계 |
| **복잡한 워크로드** | **완벽 지원** (StatefulSet, DaemonSet) | 제한적 | 지원 | 지원 |
| **주요 사용 사례** | 대규모 MSA, 엔터프라이즈 | 소규모, 단순 워크로드 | 하이브리드, 레거시 | AWS 네이티브 |

### 2. 쿠버네티스 리소스 비교

| 리소스 유형 | 목적 | 상태 관리 | 스케일링 | 사용 시나리오 |
| :--- | :--- | :--- | :--- | :--- |
| **Deployment** | Stateless 앱 | ReplicaSet 관리 | HPA 가능 | 웹 서버, API |
| **StatefulSet** | Stateful 앱 | 고정 ID, 순차 배포 | 수동/CrashLoop | DB, 캐시, 큐 |
| **DaemonSet** | 노드당 1개 파드 | 자동 | 노드 수 | 로그 수집, 모니터링 |
| **Job** | 일회성 작업 | 완료 시 종료 | 병렬 처리 | 배치, 데이터 처리 |
| **CronJob** | 주기적 작업 | 스케줄 기반 | 병렬 처리 | 백업, 리포트 생성 |

### 3. 과목 융합 관점 분석 (쿠버네티스 + 타 도메인 시너지)
- **쿠버네티스 + 네트워크 (CNI, Service Mesh)**: 쿠버네티스의 네트워크는 **CNI(Container Network Interface)** 플러그인(Calico, Cilium, Flannel)이 담당합니다. **Service Mesh(Istio, Linkerd)**를 추가하면 mTLS 암호화, 트래픽 시프팅(Canary), 서킷 브레이커, 분산 추적(Jaeger)이 가능합니다.

- **쿠버네티스 + 저장소 (CSI, PV/PVC)**: **CSI(Container Storage Interface)**를 통해 AWS EBS, GCP PD, Ceph, NFS 등 다양한 스토리지를 파드에 마운트합니다. StorageClass를 통한 동적 프로비저닝, VolumeSnapshot을 통한 백업 자동화가 가능합니다.

- **쿠버네티스 + 보안 (RBAC, Pod Security)**: **RBAC(Role-Based Access Control)**로 API 접근 권한을 세밀하게 제어합니다. **Pod Security Standards(Restricted, Baseline, Privileged)**로 파드의 권한을 제한하고, **OPA(Open Policy Agent)/Gatekeeper**로 정책 기반 거버넌스를 구현합니다.

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략
- **[상황 A] 블루-그린 배포와 카나리 배포 선택**
  - **문제점**: 새 버전 배포 시 기존 버전의 안정성을 보장하면서 점진적으로 트래픽을 이전해야 함.
  - **기술사 판단 (전략)**: **Argo Rollouts** 또는 **Flagger**를 사용하여 카나리 배포 구현. 트래픽 10% -> 25% -> 50% -> 100%로 점진적 증가. 각 단계에서 Prometheus 메트릭(에러율, 지연 시간)을 자동 분석하여, 임계값 초과 시 자동 롤백. Service Mesh(Istio)의 VirtualService로 정교한 트래픽 분배.

- **[상황 B] 멀티 클러스터/멀티 클라우드 운영**
  - **문제점**: 재해 복구(DR)와 규정 준수를 위해 여러 리전/클라우드에 클러스터 분산 필요.
  - **기술사 판단 (전략)**: **Rancher** 또는 **Google Anthos**를 사용한 멀티 클러스터 관리. **Karmada** 또는 **LiQo**로 클러스터 간 워크로드 페더레이션. 글로벌 로드 밸런서(Cloudflare, AWS Route53)로 지리적 라우팅.

### 2. 도입 시 고려사항 (기술적/보안적 체크리스트)
- **리소스 쿼터 및 LimitRange**: 네임스페이스별 CPU/메모리/스토리지 사용량을 제한하여, 특정 팀의 워크로드가 클러스터 전체를 독점하지 못하도록 격리해야 합니다.

- **Pod Disruption Budget (PDB)**: 노드 드레인(Drain) 또는 클러스터 업그레이드 시 최소 가용 파드 수를 보장하여, 무중단 서비스를 유지해야 합니다.

- **백업 및 복구 (Velero)**: etcd 스냅샷과 PV 백업을 정기적으로 수행하고, 재해 발생 시 다른 클러스터로 복구할 수 있는 절차를 구축해야 합니다.

### 3. 주의사항 및 안티패턴 (Anti-patterns)
- **모놀리식 파드 (Fat Pod)**: 하나의 파드에 너무 많은 컨테이너를 넣는 안티패턴입니다. 파드는 스케일링의 최소 단위이므로, 독립적으로 스케일링해야 하는 컴포넌트는 별도의 Deployment로 분리해야 합니다.

- **livenessProbe 남용**: livenessProbe 실패 시 컨테이너가 즉시 재시작되므로, 일시적인 부하나 외부 의존성 장애로 인한 실패를 허용하지 않는 설정은 연쇄 장애(Cascading Failure)를 유발할 수 있습니다.

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과 (도입 전후 ROI)

| 구분 | 수동 관리 / VM (AS-IS) | 쿠버네티스 기반 (TO-BE) | 개선 지표 (Impact) |
| :--- | :--- | :--- | :--- |
| **배포 주기** | 주/월 단위 | **일일 수회** (CI/CD) | Time-to-Market 90% 단축 |
| **장애 복구 시간 (MTTR)** | 30분~수시간 | **1~5분** (Auto-healing) | MTTR 95% 단축 |
| **인프라 활용률** | 15~25% (낭비) | **60~80%** (Bin-packing) | 비용 효율 200% 향상 |
| **서비스 가용성** | 99.9% (연 8.7시간 다운) | **99.99%** (연 52분 다운) | 가용성 10배 향상 |

### 2. 미래 전망 및 진화 방향
- **Platform Engineering & Internal Developer Platform (IDP)**: 쿠버네티스 위에 **Backstage**, **Crossplane**, **Kratos** 등을 결합하여, 개발자가 셀프 서비스로 인프라를 프로비저닝하는 내부 개발자 플랫폼이 표준화될 것입니다.

- **Kubernetes on Edge (K3s, KubeEdge)**: 엣지 환경(IoT, 팩토리, 매장)에서 경량 쿠버네티스인 **K3s**와 **KubeEdge**가 보편화되어, 클라우드-엣지 통합 운영이 가능해질 것입니다.

- **WebAssembly (Wasm) on Kubernetes**: 컨테이너 대신 **WebAssembly**를 쿠버네티스에서 실행하는 **Krustlet**, **spin-operator**가 등장하여, 초경량(밀리초 기동), 샌드박스 격리의 새로운 워크로드 형태가 가능해질 것입니다.

### 3. 참고 표준/가이드
- **CNCF Cloud Native Landscape**: 클라우드 네이티브 생태계 전체 프로젝트 맵
- **Kubernetes Documentation (k8s.io)**: 공식 문서 및 API 레퍼런스
- **12-Factor App**: 클라우드 네이티브 애플리케이션 개발 원칙
- **GitOps (OpenGitOps)**: 선언적 인프라 관리 표준

---

## 관련 개념 맵 (Knowledge Graph)
- **[도커 (Docker)](@/studynotes/06_ict_convergence/01_cloud/docker.md)**: 쿠버네티스가 오케스트레이션하는 컨테이너 런타임.
- **[마이크로서비스 아키텍처 (MSA)](./msa.md)**: 쿠버네티스에 최적화된 분산 시스템 설계 패턴.
- **[서비스 메시 (Service Mesh)](./service_mesh.md)**: 쿠버네티스의 마이크로서비스 통신을 관리하는 인프라 계층.
- **[CI/CD & GitOps](./gitops.md)**: 쿠버네티스로의 자동화된 배포 파이프라인.
- **[클라우드 네이티브 (Cloud Native)](./cloud_native.md)**: 쿠버네티스를 기반으로 하는 현대적 클라우드 애플리케이션 패러다임.

---

## 어린이를 위한 3줄 비유 설명
1. 쿠버네티스는 '로봇 택배 기사단의 사장님'이에요! 수백 개의 택배(컨테이너)가 어디로 가야 할지 정하고, 배달이 늦으면 다른 기사를 보내요.
2. 어떤 기사가 아파서 못 오면 즉시 대체 기사를 불러오고, 택배가 너무 많으면 기사를 더 뽑아서 일을 나눠요.
3. 이 모든 것을 사장님이 혼자서 자동으로 해주니까, 우리는 "이만큼 배달해줘!"라고 한 번만 말하면 돼요!
