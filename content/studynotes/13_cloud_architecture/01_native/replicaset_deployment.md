+++
title = "레플리카셋과 디플로이먼트 (ReplicaSet & Deployment)"
date = 2026-03-05
description = "쿠버네티스에서 파드의 복제본을 관리하고 무중단 롤링 업데이트를 수행하는 핵심 워크로드 리소스의 원리와 아키텍처"
weight = 81
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["ReplicaSet", "Deployment", "Kubernetes", "Rolling-Update", "Self-Healing", "Workload"]
+++

# 레플리카셋과 디플로이먼트 (ReplicaSet & Deployment) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 레플리카셋(ReplicaSet)은 지정된 수의 동일한 파드 복제본을 항상 실행 상태로 유지하는 '셀프 힐링' 컨트롤러이며, 디플로이먼트(Deployment)는 레플리카셋을 관리하며 무중단 롤링 업데이트와 버전 롤백 기능을 제공하는 상위 컨트롤러입니다.
> 2. **가치**: **선언적 상태 관리**(Desired State)로 인프라 운영을 코드화하며, **무중단 배포**(Zero-downtime), **자동 복구**(Self-healing), **버전 관리**(Revision History)를 통해 서비스 가용성을 99.9%+로 달성합니다.
> 3. **융합**: 쿠버네티스 컨트롤 루프, HPA(Horizontal Pod Autoscaler), 서비스(Service), Ingress와 결합하여 클라우드 네이티브 애플리케이션 배포의 표준 패턴입니다.

---

## Ⅰ. 개요 (Context & Background)

쿠버네티스에서 워크로드를 실행할 때 가장 기본이 되는 리소스가 디플로이먼트입니다. 디플로이먼트는 내부적으로 레플리카셋을 생성하고 관리하며, 레플리카셋은 실제 파드의 복제본을 유지합니다. 이 계층 구조를 통해 쿠버네티스는 선언적 방식으로 애플리케이션의 상태를 관리합니다.

**💡 비유**:
- **레플리카셋**은 **'로봇 공장의 조립 라인 관리자'**와 같습니다. "항상 5대의 로봇이 작동해야 해"라는 목표가 주어지면, 로봇이 고장 나면 즉시 새 로봇을 만들어 교체합니다.
- **디플로이먼트**는 **'로봇 공장의 엔지니어링 팀장'**과 같습니다. 조립 라인 관리자(레플리카셋)를 감독하며, "새로운 로봇 모델 v2로 교체해"라는 명령이 떨어지면, 기존 로봇을 하나씩 새 모델로 교체하며 공장이 멈추지 않도록 합니다.

**등장 배경 및 발전 과정**:
1. **ReplicationController (2014)**: 쿠버네티스 초기의 복제 컨트롤러. 기본적인 복제 기능만 제공.
2. **ReplicaSet (2015)**: 더 유연한 라벨 셀렉터(set-based) 지원. RC의 후속.
3. **Deployment (2015)**: 롤링 업데이트, 롤백 기능 추가. 실무 표준.
4. **현재**: 대부분의 워크로드는 Deployment를 통해 배포. ReplicaSet은 직접 사용 안 함.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 및 관계

| 구성 요소 | 상세 역할 | 관계 | 비고 |
|---|---|---|---|
| **Deployment** | 전체 배포 관리, 버전 관리 | ReplicaSet 생성 | 최상위 컨트롤러 |
| **ReplicaSet** | 파드 복제본 수 유지 | Pod 생성 | 중간 컨트롤러 |
| **Pod** | 실제 컨테이너 실행 | - | 최하위 실행 단위 |
| **Label Selector** | 리소스 간 연결 | Key-Value 매칭 | 느슨한 결합 |
| **Revisions** | 배포 이력 관리 | 롤백 지원 | 최대 10개 보관 |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Deployment Hierarchy ]                                  │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────────┐
                    │           Deployment                │
                    │                                     │
                    │  Name: nginx-deployment            │
                    │  Replicas: 3                        │
                    │  Strategy: RollingUpdate            │
                    │  - maxSurge: 1                      │
                    │  - maxUnavailable: 0               │
                    │                                     │
                    │  Template:                          │
                    │  - Image: nginx:1.21               │
                    │  - Labels: app=nginx               │
                    │                                     │
                    │  Revisions: 3 (롤백 가능)            │
                    └──────────────┬──────────────────────┘
                                   │ creates/manages
                                   ▼
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         ▼                         ▼                         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  ReplicaSet v3  │    │  ReplicaSet v2  │    │  ReplicaSet v1  │
│  (current)      │    │  (scaled to 0)  │    │  (scaled to 0)  │
│                 │    │                 │    │                 │
│  Replicas: 3    │    │  Replicas: 0    │    │  Replicas: 0    │
│  Revision: 3    │    │  Revision: 2    │    │  Revision: 1    │
│  Image: 1.23    │    │  Image: 1.22    │    │  Image: 1.21    │
└────────┬────────┘    └─────────────────┘    └─────────────────┘
         │
         │ creates/manages
         ▼
┌────────┴────────┬─────────────────┬─────────────────┐
│                 │                 │                 │
▼                 ▼                 ▼                 ▼
┌─────────┐    ┌─────────┐    ┌─────────┐
│ Pod 1   │    │ Pod 2   │    │ Pod 3   │
│ nginx   │    │ nginx   │    │ nginx   │
│ v1.23   │    │ v1.23   │    │ v1.23   │
│ app=nginx│   │ app=nginx│   │ app=nginx│
└─────────┘    └─────────┘    └─────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Controller Loop Mechanism ]                              │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │                    Kubernetes Control Loop                            │
    │                                                                      │
    │    ┌─────────────┐                            ┌─────────────────┐   │
    │    │  etcd       │                            │  Controller     │   │
    │    │ (Desired    │◄───────────────────────────┤  Manager        │   │
    │    │  State)     │        Watch Events        │  - Deployment   │   │
    │    └──────┬──────┘                            │    Controller   │   │
    │           │                                   │  - ReplicaSet   │   │
    │           │                                   │    Controller   │   │
    │           │ Read                              └────────┬────────┘   │
    │           ▼                                            │            │
    │    ┌─────────────┐                                     │            │
    │    │  Current    │                                     │            │
    │    │  State      │                                     │            │
    │    │  (Cluster)  │◄────────────────────────────────────┘            │
    │    └─────────────┘          Reconcile (If needed)                   │
    │                                                                      │
    │    Reconciliation Loop:                                              │
    │    while true:                                                       │
    │        current = getCurrentState()                                  │
    │        desired = getDesiredState()                                  │
    │        if current != desired:                                       │
    │            reconcile(current, desired)                              │
    │                                                                      │
    └─────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Rolling Update Process ]                                 │
└─────────────────────────────────────────────────────────────────────────────┘

    [ Initial State: v1.21, 3 replicas ]

    Step 0:                   Step 1:                   Step 2:
    ┌────────────┐            ┌────────────┐            ┌────────────┐
    │ Pod1 (v1.21)│            │ Pod1 (v1.21)│            │ Pod1 (v1.21)│
    │ Running    │            │ Running    │            │ Terminating│
    └────────────┘            └────────────┘            └────────────┘
    ┌────────────┐            ┌────────────┐            ┌────────────┐
    │ Pod2 (v1.21)│            │ Pod2 (v1.21)│            │ Pod2 (v1.21)│
    │ Running    │            │ Running    │            │ Running    │
    └────────────┘            └────────────┘            └────────────┘
    ┌────────────┐            ┌────────────┐            ┌────────────┐
    │ Pod3 (v1.21)│            │ Pod3 (v1.21)│            │ Pod3 (v1.21)│
    │ Running    │            │ Running    │            │ Running    │
    └────────────┘            └────────────┘            └────────────┘
                              ┌────────────┐            ┌────────────┐
                              │ Pod4 (v1.23)│            │ Pod4 (v1.23)│
                              │ Pending    │            │ Running    │
                              └────────────┘            └────────────┘

    Step 3:                   Step 4:                   Step 5 (Final):
    ┌────────────┐            ┌────────────┐            ┌────────────┐
    │ Pod5 (v1.23)│            │ Pod5 (v1.23)│            │ Pod5 (v1.23)│
    │ Running    │            │ Running    │            │ Running    │
    └────────────┘            └────────────┘            └────────────┘
    ┌────────────┐            ┌────────────┐            ┌────────────┐
    │ Pod2 (v1.21)│            │ Pod2 (v1.21)│            │ Pod6 (v1.23)│
    │ Terminating│            │ Terminated │            │ Running    │
    └────────────┘            └────────────┘            └────────────┘
    ┌────────────┐            ┌────────────┐            ┌────────────┐
    │ Pod3 (v1.21)│            │ Pod6 (v1.23)│            │ Pod7 (v1.23)│
    │ Running    │            │ Pending    │            │ Running    │
    └────────────┘            └────────────┘            └────────────┘
    ┌────────────┐            ┌────────────┐            ┌────────────┘
    │ Pod4 (v1.23)│            │ Pod3 (v1.21)│            All v1.23
    │ Running    │            │ Terminating│            Rollback Ready
    └────────────┘            └────────────┘

    Strategy: RollingUpdate
    - maxSurge: 1 (최대 1개 추가 Pod 허용)
    - maxUnavailable: 0 (항상 3개 이상 가용)

    Time: ~2-5분 (Pod 기동 시간에 따라 다름)
```

### 심층 동작 원리: 롤링 업데이트 알고리즘

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    Rolling Update Algorithm                                 │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  Algorithm: Rolling Update with maxSurge & maxUnavailable                  │
│                                                                            │
│  Parameters:                                                               │
│  - replicas: desired replica count (N)                                     │
│  - maxSurge: maximum pods that can be created above N (default 25%)        │
│  - maxUnavailable: maximum pods that can be unavailable (default 25%)      │
│                                                                            │
│  Example: N=4, maxSurge=1, maxUnavailable=0                                │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │ Step 1: Create new Pod (surge)                                      │  │
│  │   Old Pods: 4 (Running)                                             │  │
│  │   New Pods: 1 (Pending → Running)                                   │  │
│  │   Total: 5 (N + maxSurge)                                          │  │
│  │   Available: 4 (N - maxUnavailable) minimum                        │  │
│  │                                                                     │  │
│  │ Step 2: Wait for new Pod ready                                      │  │
│  │   Check: ReadinessProbe success                                    │  │
│  │   Service endpoints updated (new Pod added)                        │  │
│  │                                                                     │  │
│  │ Step 3: Delete old Pod                                              │  │
│  │   Old Pods: 3 (one terminated)                                     │  │
│  │   New Pods: 1 (Running)                                            │  │
│  │   Total: 4 (maintain N)                                            │  │
│  │   Available: 4 (all healthy)                                       │  │
│  │                                                                     │  │
│  │ Step 4-7: Repeat until all pods updated                             │  │
│  │                                                                     │  │
│  │ Final State:                                                        │  │
│  │   Old Pods: 0                                                      │  │
│  │   New Pods: 4 (all Running)                                        │  │
│  │   Old ReplicaSet: scaled to 0                                      │  │
│  │   New ReplicaSet: scaled to 4                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  Progress Deadline:                                                        │
│  - If pod doesn't become ready within progressDeadlineSeconds (600s)      │
│  - Deployment marked as "Progressing" = False                             │
│  - Rollback or manual intervention required                               │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: 프로덕션급 Deployment 구성

```yaml
# 프로덕션급 Deployment 구성 예시
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-application
  namespace: production
  labels:
    app: web
    tier: frontend
spec:
  # 복제본 수
  replicas: 4

  # Revision 기록 개수 (롤백용)
  revisionHistoryLimit: 10

  # 레이블 셀렉터 (연결할 Pod 식별)
  selector:
    matchLabels:
      app: web
    matchExpressions:
      - key: tier
        operator: In
        values: [frontend]

  # 배포 전략
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1           # 최대 1개 초과 생성 허용
      maxUnavailable: 0     # 최소 4개 항상 가용 보장 (무중단)

  # Pod 템플릿
  template:
    metadata:
      labels:
        app: web
        tier: frontend
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
    spec:
      # 서비스 계정
      serviceAccountName: web-app-sa

      # 보안 컨텍스트
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000

      # 컨테이너 정의
      containers:
        - name: web
          image: registry.example.com/web-app:v2.1.0
          imagePullPolicy: Always

          # 포트
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP

          # 리소스 제한 (OOM 방지)
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi

          # 환경 변수
          env:
            - name: ENV
              value: "production"
            - name: DB_HOST
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: host
            - name: LOG_LEVEL
              value: "info"

          # 헬스 체크 - Liveness (재시작 기준)
          livenessProbe:
            httpGet:
              path: /healthz
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3

          # 헬스 체크 - Readiness (트래픽 투입 기준)
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3

          # 시작 프로브 (무거운 앱용)
          startupProbe:
            httpGet:
              path: /healthz
              port: http
            initialDelaySeconds: 0
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 30  # 최대 150초 대기

          # 볼륨 마운트
          volumeMounts:
            - name: config
              mountPath: /app/config
              readOnly: true
            - name: tmp
              mountPath: /tmp

      # 볼륨 정의
      volumes:
        - name: config
          configMap:
            name: web-config
        - name: tmp
          emptyDir: {}

      # 종료 유예 기간
      terminationGracePeriodSeconds: 30

      # 노드 선택자
      nodeSelector:
        node-role: application

      # 톨러레이션 (테인트가 있는 노드 허용)
      tolerations:
        - key: "dedicated"
          operator: "Equal"
          value: "app"
          effect: "NoSchedule"

      # affinity (스케줄링 선호도)
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: web
                topologyKey: kubernetes.io/hostname
---
# Horizontal Pod Autoscaler (HPA)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-application-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-application
  minReplicas: 4
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # 5분 대기
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
```

### 롤아웃 명령어

```bash
# 배포 상태 확인
kubectl rollout status deployment/web-application

# 배포 이력 확인
kubectl rollout history deployment/web-application
kubectl rollout history deployment/web-application --revision=2

# 롤백 (이전 버전으로)
kubectl rollout undo deployment/web-application

# 특정 리비전으로 롤백
kubectl rollout undo deployment/web-application --to-revision=2

# 롤아웃 일시정지 (카나리 배포용)
kubectl rollout pause deployment/web-application

# 롤아웃 재개
kubectl rollout resume deployment/web-application

# 배포 스케일 조정
kubectl scale deployment/web-application --replicas=6

# 현재 배포 상태 상세 확인
kubectl describe deployment web-application

# ReplicaSet 확인
kubectl get rs -l app=web

# Pod 상태 확인
kubectl get pods -l app=web -w
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 배포 전략

| 배포 전략 | maxSurge | maxUnavailable | 특징 | 적합 상황 |
|---|---|---|---|---|
| **RollingUpdate (기본)** | 25% | 25% | 점진적 교체 | 일반적 웹 서비스 |
| **Blue-Green** | 100% | 0% | 완전 복제 후 스위칭 | 중요 서비스, 빠른 롤백 |
| **Canary** | 10% | 0% | 소량 트래픽 테스트 | 위험한 변경 |
| **Recreate** | 0 | 100% | 전체 교체 (중단 발생) | 개발/테스트 환경 |

### Deployment vs 다른 워크로드 비교

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ Workload Types Comparison ]                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ Deployment                                                              ││
│  │ - 상태 비저장 (Stateless) 앱                                             ││
│  │ - 롤링 업데이트, 롤백                                                    ││
│  │ - 가장 일반적으로 사용                                                   ││
│  │ - 예: 웹 서버, API 서버, 마이크로서비스                                   ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ StatefulSet                                                             ││
│  │ - 상태 저장 (Stateful) 앱                                                ││
│  │ - 고정 식별자 (pod-0, pod-1, ...)                                       ││
│  │ - 영구 스토리지 (PVC 유지)                                               ││
│  │ - 예: 데이터베이스, 메시지 큐, 캐시                                       ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ DaemonSet                                                               ││
│  │ - 모든 노드에 1개씩 실행                                                 ││
│  │ - 노드 추가 시 자동 생성                                                 ││
│  │ - 예: 로그 수집기, 모니터링 에이전트, 네트워크 플러그인                    ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ Job / CronJob                                                           ││
│  │ - 일회성 또는 주기적 작업                                                ││
│  │ - 완료 시 종료                                                           ││
│  │ - 예: 배치 처리, 백업, 정기 리포트                                       ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 과목 융합 관점 분석

**운영체제(OS)와의 융합**:
- **프로세스 관리**: Pod 내 컨테이너의 생명주기 관리
- **시그널 처리**: SIGTERM으로 Graceful Shutdown
- **리소스 격리**: cgroups를 통한 CPU/메모리 제한

**네트워크와의 융합**:
- **Service와 연동**: Label Selector로 Pod 그룹핑
- **롤링 업데이트 중 트래픽**: Readiness Probe로 제어

**보안(Security)과의 융합**:
- **RBAC**: ServiceAccount를 통한 권한 부여
- **Pod Security**: SecurityContext로 권한 제한

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 무중단 배포 설계

**문제 상황**: 99.99% 가용성이 필요한 결제 서비스의 무중단 배포 설계

**기술사의 아키텍처 설계**:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ Zero-Downtime Deployment Strategy ]                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. 배포 전략 설정                                                            │
│                                                                              │
│     strategy:                                                                │
│       type: RollingUpdate                                                    │
│       rollingUpdate:                                                         │
│         maxSurge: 25%           # 기존 Pod의 25%까지 추가 생성               │
│         maxUnavailable: 0       # 절대 Pod 부족 허용 안 함                   │
│                                                                              │
│  2. Pod 준비 확인 (ReadinessProbe)                                           │
│                                                                              │
│     readinessProbe:                                                          │
│       httpGet:                                                               │
│         path: /health/ready                                                  │
│         port: 8080                                                           │
│       initialDelaySeconds: 10                                                │
│       periodSeconds: 5                                                       │
│       failureThreshold: 3                                                    │
│                                                                              │
│     - Readiness 통과 전까지 Service 엔드포인트에 추가 안 됨                    │
│     - DB 연결, 캐시 워밍업 완료 후 Ready 신호                                 │
│                                                                              │
│  3. Graceful Shutdown                                                        │
│                                                                              │
│     lifecycle:                                                               │
│       preStop:                                                               │
│         exec:                                                                │
│           command: ["/bin/sh", "-c", "sleep 15 && nginx -s quit"]           │
│                                                                              │
│     terminationGracePeriodSeconds: 30                                        │
│                                                                              │
│     - SIGTERM 수신 후 진행 중인 요청 완료 대기                                 │
│     - Service에서 제거 후 종료                                                │
│                                                                              │
│  4. 배포 파이프라인                                                           │
│                                                                              │
│     Stage 1: 카나리 배포 (10%)                                               │
│     ┌──────────────────────────────────────────────────────────────────┐    │
│     │  Pod 1-9: v1.0.0  (90%)                                          │    │
│     │  Pod 10: v1.0.1   (10%)  ← 메트릭 모니터링                        │    │
│     └──────────────────────────────────────────────────────────────────┘    │
│     - 에러율, 지연 시간 5분간 모니터링                                        │
│     - 이상 없으면 전체 배포 진행                                              │
│                                                                              │
│     Stage 2: 롤링 업데이트                                                    │
│     ┌──────────────────────────────────────────────────────────────────┐    │
│     │  Pod 1-10: v1.0.1 (100%)                                         │    │
│     │  롤링 업데이트로 점진적 교체                                        │    │
│     └──────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  5. 롤백 계획                                                                 │
│     - 자동 롤백: 에러율 5% 초과 시                                            │
│     - 수동 롤백: kubectl rollout undo                                        │
│     - 롤백 시간: < 30초                                                       │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 도입 시 고려사항 체크리스트

| 항목 | 확인 사항 | 비고 |
|---|---|---|
| **리소스 설정** | requests/limits 명시 | OOM 방지 |
| **헬스 체크** | Liveness/Readiness 구현 | 무중단 필수 |
| **Graceful Shutdown** | preStop 훅 구현 | 요청 유실 방지 |
| **revisionHistoryLimit** | 적절한 이력 보관 | 롤백 가능 |
| **PodAntiAffinity** | 노드 분산 배치 | 고가용성 |

### 안티패턴 및 주의사항

**안티패턴 1: ReadinessProbe 없이 배포**
- 문제: 준비되지 않은 Pod에 트래픽 유입
- 해결: 반드시 ReadinessProbe 구현

**안티패턴 2: maxUnavailable=100%**
- 문제: 배포 중 서비스 중단
- 해결: maxUnavailable=0 설정

**안티패턴 3: 이미지 태그 :latest 사용**
- 문제: 롤백 불가, 재현 불가
- 해결: 버전 태그 사용 (v1.2.3)

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 수동 배포 | Deployment | 개선율 |
|---|---|---|---|
| **배포 시간** | 30분+ | 5분 | 83% 단축 |
| **중단 시간** | 5-10분 | 0초 | 무중단 |
| **롤백 시간** | 30분+ | 30초 | 99% 단축 |
| **인적 오류** | 높음 | 낮음 | 자동화 |

### 미래 전망 및 진화 방향

1. **GitOps**: ArgoCD, Flux로 선언적 배포 자동화
2. **Progressive Delivery**: 카나리, 블루-그린 자동화 (Flagger, Argo Rollouts)
3. **Service Mesh**: Istio로 트래픽 시프트 정밀 제어
4. **AI 기반 배포**: 메트릭 기반 자동 롤백

### ※ 참고 표준/가이드
- **Kubernetes Documentation**: Workload Resources
- **12 Factor App**: Dev/prod parity, disposability
- **Google SRE Book**: Release Engineering

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [쿠버네티스 (Kubernetes)](@/studynotes/13_cloud_architecture/01_native/kubernetes.md) : 오케스트레이션 플랫폼
- [컨테이너 (Container)](@/studynotes/13_cloud_architecture/01_native/container.md) : 실행 단위
- [서비스 (Service)](@/studynotes/13_cloud_architecture/_index.md) : 네트워크 추상화
- [HPA](@/studynotes/13_cloud_architecture/_index.md) : 오토스케일링
- [CI/CD](@/studynotes/13_cloud_architecture/01_native/ci_cd.md) : 배포 파이프라인

---

### 👶 어린이를 위한 3줄 비유 설명
1. 레플리카셋은 **'항상 5대의 로봇이 작동하게 하는 관리자'**예요. 로봇이 고장 나면 새 로봇을 즉시 만들어요.
2. 디플로이먼트는 **'로봇을 새 버전으로 교체하는 팀장'**이에요. 로봇을 하나씩만 교체해서 공장이 멈추지 않게 해요.
3. 덕분에 **'로봇이 고장 나거나 업그레이드해도 공장은 계속 돌아가요!'** 사람이 직접 하지 않아도 되니까 편해요!
