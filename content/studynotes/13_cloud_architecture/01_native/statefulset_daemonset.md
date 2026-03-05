+++
title = "스테이트풀셋과 데몬셋 (StatefulSet & DaemonSet)"
date = 2026-03-05
description = "쿠버네티스에서 상태 저장 애플리케이션과 노드별 단일 인스턴스 실행을 위한 특수 워크로드 리소스의 원리와 아키텍처"
weight = 82
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["StatefulSet", "DaemonSet", "Kubernetes", "Stateful-Application", "Node-Agent", "Persistence"]
+++

# 스테이트풀셋과 데몬셋 (StatefulSet & DaemonSet) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스테이트풀셋(StatefulSet)은 고유한 네트워크 ID와 영구 스토리지를 가진 순차적 파드 관리 컨트롤러로, 데몬셋(DaemonSet)은 클러스터의 모든(또는 특정) 노드에 정확히 1개의 파드를 실행하는 노드-로컬 에이전트 컨트롤러입니다.
> 2. **가치**: 스테이트풀셋은 **데이터베이스, 메시지 큐, 캐시 클러스터**의 안정적 운영을 가능하게 하며, 데몬셋은 **로그 수집, 모니터링, 네트워크 플러그인** 등 인프라 에이전트의 자동 배포를 보장합니다.
> 3. **융합**: 영구 볼륨(PV/PVC), Headless Service, 노드 셀렉터, 톨러레이션과 결합하여 엔터프라이즈급 분산 시스템의 기반을 구축합니다.

---

## Ⅰ. 개요 (Context & Background)

Deployment가 상태 비저장(Stateless) 애플리케이션에 적합한 반면, 데이터베이스나 분산 스토리지 같은 상태 저장(Stateful) 애플리케이션은 다른 요구사항을 가집니다. StatefulSet은 이러한 요구를 충족하기 위해 설계되었습니다. DaemonSet은 노드당 하나의 Pod를 보장하는 인프라 컴포넌트 배포에 사용됩니다.

**💡 비유**:
- **StatefulSet**은 **'번호표가 있는 영구 사물함'**과 같습니다. 각 사물함(파드)에는 고유 번호(0, 1, 2...)가 있고, 그 안의 물건(데이터)은 사물함이 바뀌어도 그대로 유지됩니다. 0번 사물함의 물건은 항상 0번 사물함에 있어야 해요.
- **DaemonSet**은 **'각 교실의 청소 당번'**과 같습니다. 모든 교실(노드)에 정확히 1명의 청소 당번(파드)이 있어야 합니다. 새 교실이 생기면 자동으로 당번이 배정됩니다.

**등장 배경 및 발전 과정**:
1. **PetSet (2016)**: StatefulSet의 초기 이름. 반려동물(Pet)처럼 개별 식별이 필요한 파드.
2. **StatefulSet (2017)**: 정식 명칭으로 변경. 안정적인 네트워크 ID와 스토리지 제공.
3. **DaemonSet (2015~)**: 초기부터 존재. 노드별 시스템 데몬 실행용.
4. **현재**: 분산 데이터베이스, 스트리밍 플랫폼, 서비스 메시 등 핵심 인프라 구성.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 및 비교

| 특성 | StatefulSet | DaemonSet | Deployment |
|---|---|---|---|
| **파드 식별자** | 고정 (sts-0, sts-1, ...) | 노드별 1개 | 랜덤 해시 |
| **스토리지** | PVC 유지 (파드 재생성 시에도) | 通常 없음 | Usually 없음 |
| **시작 순서** | 순차적 (0 → 1 → 2) | 병렬 | 병렬 |
| **네트워크 ID** | 고정 DNS 이름 | 노드별 | 랜덤 |
| **스케일링** | 수동/자동 (순차) | 노드 수에 따라 자동 | 수동/자동 |
| **적합 워크로드** | DB, 캐시, MQ | 로그, 모니터링, CNI | 웹, API |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ StatefulSet Architecture ]                               │
└─────────────────────────────────────────────────────────────────────────────┘

    Headless Service (DNS 기반 서비스 디스커버리)
    ┌──────────────────────────────────────────────────────────────────────┐
    │  Service: cassandra-headless                                         │
    │  ClusterIP: None (Headless)                                          │
    │  Selector: app=cassandra                                             │
    │                                                                       │
    │  DNS Records:                                                         │
    │  - cassandra-0.cassandra-headless.default.svc.cluster.local          │
    │  - cassandra-1.cassandra-headless.default.svc.cluster.local          │
    │  - cassandra-2.cassandra-headless.default.svc.cluster.local          │
    └──────────────────────────┬───────────────────────────────────────────┘
                               │
    StatefulSet                │
    ┌──────────────────────────▼───────────────────────────────────────────┐
    │  StatefulSet: cassandra-cluster                                      │
    │  Replicas: 3                                                         │
    │  ServiceName: cassandra-headless                                     │
    │                                                                       │
    │  Pod Management Policy: OrderedReady (0→1→2)                         │
    │                                                                       │
    │  ┌─────────────────────────────────────────────────────────────────┐│
    │  │  PersistentVolumeClaims (StatefulSet 전용)                       ││
    │  │                                                                   ││
    │  │  cassandra-data-cassandra-0  →  PV-A (10GB)                     ││
    │  │  cassandra-data-cassandra-1  →  PV-B (10GB)                     ││
    │  │  cassandra-data-cassandra-2  →  PV-C (10GB)                     ││
    │  │                                                                   ││
    │  │  PVC는 파드 재생성 시에도 동일 파드에 다시 연결됨                    ││
    │  │  (PVC 이름에 파드 순서 번호 포함)                                  ││
    │  └─────────────────────────────────────────────────────────────────┘│
    │                                                                       │
    │  ┌────────────────────────────────────────────────────────────────┐  │
    │  │                                                                 │  │
    │  │   Pod: cassandra-0        Pod: cassandra-1       Pod: cassandra-2│  │
    │  │   ┌─────────────┐        ┌─────────────┐        ┌─────────────┐ │  │
    │  │   │ Cassandra   │        │ Cassandra   │        │ Cassandra   │ │  │
    │  │   │ Node 0      │        │ Node 1      │        │ Node 2      │ │  │
    │  │   │             │        │             │        │             │ │  │
    │  │   │ Pod IP:     │        │ Pod IP:     │        │ Pod IP:     │ │  │
    │  │   │ 10.244.1.10 │        │ 10.244.2.20 │        │ 10.244.3.30 │ │  │
    │  │   └──────┬──────┘        └──────┬──────┘        └──────┬──────┘ │  │
    │  │          │                      │                      │        │  │
    │  │          ▼                      ▼                      ▼        │  │
    │  │   ┌─────────────┐        ┌─────────────┐        ┌─────────────┐ │  │
    │  │   │ PVC: data-0 │        │ PVC: data-1 │        │ PVC: data-2 │ │  │
    │  │   │   ↓         │        │   ↓         │        │   ↓         │ │  │
    │  │   │ PV-A        │        │ PV-B        │        │ PV-C        │ │  │
    │  │   │ (영구)       │        │ (영구)       │        │ (영구)       │ │  │
    │  │   └─────────────┘        └─────────────┘        └─────────────┘ │  │
    │  │                                                                 │  │
    │  │  노드: node-1            노드: node-2           노드: node-3    │  │
    │  │                                                                 │  │
    │  └────────────────────────────────────────────────────────────────┘  │
    │                                                                       │
    └───────────────────────────────────────────────────────────────────────┘

    StatefulSet 특징:
    - 순차 시작: cassandra-0 → cassandra-1 → cassandra-2
    - 순차 종료: cassandra-2 → cassandra-1 → cassandra-0
    - PVC는 파드와 독립적으로 존재
    - 파드 재생성 시 동일 PVC에 다시 연결
    - 고정 DNS 이름으로 서비스 간 통신


┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ DaemonSet Architecture ]                                 │
└─────────────────────────────────────────────────────────────────────────────┘

    DaemonSet (모든 노드에 1개씩 실행)
    ┌──────────────────────────────────────────────────────────────────────┐
    │  DaemonSet: fluentd-logging                                          │
    │  Selector: app=fluentd                                               │
    │                                                                       │
    │  Update Strategy: RollingUpdate                                      │
    │  - maxUnavailable: 1                                                 │
    │                                                                       │
    │  Tolerations: (마스터 노드에도 배포)                                   │
    │  - key: node-role.kubernetes.io/master                               │
    │    effect: NoSchedule                                                │
    │                                                                       │
    └──────────────────────────┬───────────────────────────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │   Node 1    │    │   Node 2    │    │   Node 3    │
    │   (Master)  │    │   (Worker)  │    │   (Worker)  │
    │             │    │             │    │             │
    │  ┌───────┐  │    │  ┌───────┐  │    │  ┌───────┐  │
    │  │fluentd│  │    │  │fluentd│  │    │  │fluentd│  │
    │  │ Pod   │  │    │  │ Pod   │  │    │  │ Pod   │  │
    │  └───┬───┘  │    │  └───┬───┘  │    │  └───┬───┘  │
    │      │      │    │      │      │    │      │      │
    │      ▼      │    │      ▼      │    │      ▼      │
    │  /var/log   │    │  /var/log   │    │  /var/log   │
    │  (호스트)    │    │  (호스트)    │    │  (호스트)    │
    └─────────────┘    └─────────────┘    └─────────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Elasticsearch │
                    │   (로그 저장소)  │
                    └─────────────────┘

    DaemonSet 특징:
    - 노드 추가 시 자동으로 Pod 생성
    - 노드 삭제 시 자동으로 Pod 제거
    - 모든 노드에 동일한 시스템 서비스 실행
    - 주로 인프라/모니터링 에이전트용


┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ StatefulSet Pod Identity ]                               │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────┐
    │  StatefulSet Pod의 고정 ID                                           │
    │                                                                       │
    │  Pod Name:          <statefulset-name>-<ordinal>                     │
    │  예:                mysql-0, mysql-1, mysql-2                        │
    │                                                                       │
    │  Hostname:          <pod-name>                                       │
    │  예:                mysql-0                                          │
    │                                                                       │
    │  Subdomain:         <service-name>                                   │
    │  예:                mysql-headless                                   │
    │                                                                       │
    │  Full DNS Name:     <pod-name>.<service-name>.<namespace>.svc.       │
    │                     cluster.local                                    │
    │  예:                mysql-0.mysql-headless.prod.svc.cluster.local    │
    │                                                                       │
    │  PVC Name:          <pvc-template-name>-<statefulset-name>-<ordinal> │
    │  예:                mysql-data-mysql-0                               │
    │                                                                       │
    │  이 ID들은 파드가 재생성되어도 동일하게 유지됨                         │
    │  (동일 ordinal의 새 파드가 이전 파드의 ID와 PVC를 상속)                │
    │                                                                       │
    └──────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: StatefulSet 스케일링 및 장애 복구

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    StatefulSet Scale Up/Down & Recovery                     │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ 스케일 업 (0 → 3) ]                                                      │
│                                                                            │
│  Time  Action                           State                              │
│  ────  ─────────────────────────────   ─────────────────────────────────   │
│  T0    Create mysql-0                   [mysql-0: Pending]                 │
│  T1    mysql-0 Running, Ready           [mysql-0: Running]                 │
│  T2    Create mysql-1                   [mysql-0, mysql-1: Pending]        │
│  T3    mysql-1 Running, Ready           [mysql-0, mysql-1: Running]        │
│  T4    Create mysql-2                   [mysql-0, mysql-1, mysql-2]        │
│  T5    mysql-2 Running, Ready           [All Running]                       │
│                                                                            │
│  ※ 순차적 생성 (OrderedReady) - 이전 Pod가 Ready여야 다음 생성              │
│                                                                            │
│  [ 스케일 다운 (3 → 1) ]                                                    │
│                                                                            │
│  T10   Terminate mysql-2               [mysql-0, mysql-1]                  │
│  T11   mysql-2 Terminated              [mysql-0, mysql-1]                  │
│  T12   Terminate mysql-1               [mysql-0]                           │
│  T13   mysql-1 Terminated              [mysql-0]                           │
│                                                                            │
│  ※ 역순 종료 (2 → 1 → 0)                                                   │
│  ※ PVC는 삭제되지 않음 (보존됨)                                             │
│                                                                            │
│  [ 장애 복구 (mysql-1 노드 장애) ]                                           │
│                                                                            │
│  T20   Node failure                     mysql-1: Unknown                  │
│  T21   K8s detects node failure         mysql-1: Marked for deletion      │
│  T22   Force delete mysql-1             mysql-1: Terminating              │
│  T23   Create new mysql-1               mysql-1: Pending (new Pod)        │
│  T24   New mysql-1 Running              mysql-1: Running                  │
│        (동일 PVC에 연결)                  → Same data as before!           │
│                                                                            │
│  ※ 새 Pod는 동일한 ID(mysql-1)와 동일한 PVC 사용                             │
│  ※ 데이터는 그대로 유지됨                                                   │
│                                                                            │
│  [ Pod Management Policies ]                                                │
│                                                                            │
│  1. OrderedReady (기본)                                                     │
│     - 순차적 시작/종료                                                      │
│     - 안전하지만 느림                                                       │
│                                                                            │
│  2. Parallel                                                                │
│     - 병렬 시작/종료                                                        │
│     - 빠르지만 순서 보장 없음                                               │
│     - 데이터 복제가 안 되는 앱에는 부적합                                    │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: MySQL 클러스터 StatefulSet

```yaml
# MySQL Galera Cluster StatefulSet 예시
apiVersion: v1
kind: Service
metadata:
  name: mysql-headless
  namespace: database
spec:
  clusterIP: None  # Headless Service
  selector:
    app: mysql-galera
  ports:
    - name: mysql
      port: 3306
      targetPort: 3306
    - name: galera
      port: 4567
      targetPort: 4567
    - name: ist
      port: 4568
      targetPort: 4568
    - name: sst
      port: 4444
      targetPort: 4444
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql-galera
  namespace: database
spec:
  serviceName: mysql-headless  # Headless Service 연결
  replicas: 3
  selector:
    matchLabels:
      app: mysql-galera

  # Pod 관리 정책
  podManagementPolicy: OrderedReady

  # 업데이트 전략
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      partition: 0  # 0 이상의 ordinal만 업데이트

  template:
    metadata:
      labels:
        app: mysql-galera
    spec:
      # 초기화 컨테이너 (설정 파일 생성)
      initContainers:
        - name: init-mysql
          image: mysql:8.0
          command:
            - bash
            - "-c"
            - |
              set -ex
              # Pod ordinal에서 인덱스 추출
              [[ $(hostname) =~ -([0-9]+)$ ]] || exit 1
              ordinal=${BASH_REMATCH[1]}

              # server-id 생성 (1부터 시작)
              echo [mysqld] > /mnt/conf.d/server-id.cnf
              echo server-id=$((100 + ordinal)) >> /mnt/conf.d/server-id.cnf

              # 첫 번째 Pod면 마스터, 아니면 슬레이브
              if [[ $ordinal -eq 0 ]]; then
                cp /mnt/config-map/master.cnf /mnt/conf.d/
              else
                cp /mnt/config-map/slave.cnf /mnt/conf.d/
              fi
          volumeMounts:
            - name: conf
              mountPath: /mnt/conf.d
            - name: config-map
              mountPath: /mnt/config-map

      containers:
        - name: mysql
          image: mysql:8.0
          env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: root-password
            - name: MYSQL_DATABASE
              value: "appdb"
            # Pod ordinal을 환경 변수로
            - name: POD_ORDINAL
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name

          ports:
            - name: mysql
              containerPort: 3306
            - name: galera
              containerPort: 4567

          # 리소스 제한
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 2000m
              memory: 4Gi

          # Liveness Probe
          livenessProbe:
            exec:
              command: ["mysqladmin", "ping", "-p${MYSQL_ROOT_PASSWORD}"]
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5

          # Readiness Probe
          readinessProbe:
            exec:
              command:
                - bash
                - "-c"
                - |
                  mysql -p${MYSQL_ROOT_PASSWORD} -e "SELECT 1"
            initialDelaySeconds: 5
            periodSeconds: 2
            timeoutSeconds: 1

          volumeMounts:
            - name: data
              mountPath: /var/lib/mysql
            - name: conf
              mountPath: /etc/mysql/conf.d

      volumes:
        - name: conf
          emptyDir: {}
        - name: config-map
          configMap:
            name: mysql-config

  # 영구 볼륨 클레임 템플릿
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: gp3
        resources:
          requests:
            storage: 100Gi

---
# DaemonSet 예시: Fluentd 로그 수집기
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: logging
  labels:
    k8s-app: fluentd-logging
spec:
  selector:
    matchLabels:
      name: fluentd

  # 업데이트 전략
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1

  template:
    metadata:
      labels:
        name: fluentd
    spec:
      # 서비스 계정
      serviceAccountName: fluentd

      # 마스터 노드에도 배포 (톨러레이션)
      tolerations:
        - key: node-role.kubernetes.io/master
          effect: NoSchedule
        - key: node-role.kubernetes.io/control-plane
          effect: NoSchedule

      # 보안 컨텍스트
      securityContext:
        runAsUser: 0
        privileged: true

      containers:
        - name: fluentd
          image: fluent/fluentd-kubernetes-daemonset:v1.15
          env:
            - name: FLUENT_ELASTICSEARCH_HOST
              value: "elasticsearch.logging.svc.cluster.local"
            - name: FLUENT_ELASTICSEARCH_PORT
              value: "9200"
            - name: FLUENT_ELASTICSEARCH_SCHEME
              value: "http"

          resources:
            requests:
              cpu: 100m
              memory: 200Mi
            limits:
              cpu: 500m
              memory: 500Mi

          volumeMounts:
            # 호스트 로그 디렉토리
            - name: varlog
              mountPath: /var/log
              readOnly: true
            # 컨테이너 로그
            - name: varlibdockercontainers
              mountPath: /var/lib/docker/containers
              readOnly: true
            # Fluentd 설정
            - name: config
              mountPath: /fluentd/etc/fluent.conf
              subPath: fluent.conf

          terminationGracePeriodSeconds: 30

      volumes:
        - name: varlog
          hostPath:
            path: /var/log
        - name: varlibdockercontainers
          hostPath:
            path: /var/lib/docker/containers
        - name: config
          configMap:
            name: fluentd-config

      # 특정 노드만 배포 (선택적)
      # nodeSelector:
      #   logging: "enabled"
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 워크로드 유형 선택

| 요구사항 | Deployment | StatefulSet | DaemonSet |
|---|---|---|---|
| **데이터 저장** | 不필요 | 필수 (영구) | 보통 없음 |
| **파드 ID** | 상관없음 | 고정 필요 | 노드별 1개 |
| **시작 순서** | 상관없음 | 중요 | 상관없음 |
| **스케일링** | 자유롭게 | 순차적 | 노드 수 따름 |
| **네트워크** | Service LB | Headless DNS | 通常 없음 |
| **적합 예시** | 웹, API | DB, 캐시 | 로그, 모니터링 |

### StatefulSet 활용 사례

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ StatefulSet Use Cases ]                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. 분산 데이터베이스                                                         │
│     ┌─────────────────────────────────────────────────────────────────────┐ │
│     │ MySQL Galera Cluster                                                 │ │
│     │ - 3노드 복제                                                         │ │
│     │ - 각 노드가 읽기/쓰기 가능                                            │ │
│     │ - mysql-0, mysql-1, mysql-2                                         │ │
│     │ - 각각 고유 PVC                                                      │ │
│     └─────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  2. NoSQL 데이터베이스                                                        │
│     ┌─────────────────────────────────────────────────────────────────────┐ │
│     │ Cassandra / MongoDB / Redis Cluster                                  │ │
│     │ - 링 구조 토폴로지                                                   │ │
│     │ - 각 노드가 데이터 샤드 담당                                          │ │
│     │ - 노드 간 데이터 복제                                                │ │
│     └─────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  3. 메시지 큐 / 스트리밍                                                      │
│     ┌─────────────────────────────────────────────────────────────────────┐ │
│     │ Kafka / RabbitMQ / Pulsar                                           │ │
│     │ - 파티션 리더/팔로워 구조                                             │ │
│     │ - 브로커 ID 고정 필요                                                │ │
│     │ - 오프셋 저장소                                                      │ │
│     └─────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  4. 분산 스토리지                                                             │
│     ┌─────────────────────────────────────────────────────────────────────┐ │
│     │ Ceph / MinIO / GlusterFS                                            │ │
│     │ - OSD (Object Storage Daemon)                                       │ │
│     │ - MON (Monitor)                                                     │ │
│     │ - 데이터 중복 및 분산                                                │ │
│     └─────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  5. 서비스 메시 컨트롤 플레인                                                  │
│     ┌─────────────────────────────────────────────────────────────────────┐ │
│     │ Istio Pilot / Citadel / Galley                                      │ │
│     │ - HA를 위한 다중 인스턴스                                             │ │
│     │ - 리더 선출 필요                                                     │ │
│     └─────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### DaemonSet 활용 사례

| DaemonSet 유형 | 목적 | 대표 도구 |
|---|---|---|
| **로그 수집** | 노드/컨테이너 로그 수집 | Fluentd, Filebeat, Logstash |
| **모니터링** | 노드 메트릭 수집 | Node Exporter, cAdvisor |
| **네트워크** | CNI 구현 | Calico, Cilium, Weave |
| **스토리지** | 노드 스토리지 관리 | Rook-Ceph, OpenEBS |
| **보안** | 런타임 보안 | Falco, Sysdig |
| **서비스 메시** | 사이드카 프록시 | Istio CNI, Linkerd CNI |

### 과목 융합 관점 분석

**저장소와의 융합**:
- **PV/PVC**: StatefulSet의 volumeClaimTemplates로 영구 볼륨 자동 생성
- **StorageClass**: 동적 프로비저닝

**네트워크와의 융합**:
- **Headless Service**: StatefulSet의 DNS 기반 디스커버리
- **HostNetwork**: DaemonSet에서 호스트 네트워크 사용

**보안(Security)과의 융합**:
- **Secret 마운트**: DB 비밀번호, 인증서
- **RBAC**: ServiceAccount로 권한 제어

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: Redis 클러스터 구축

**문제 상황**: 고가용성 Redis 클러스터를 쿠버네티스에 구축해야 함

**기술사의 아키텍처 설계**:

```yaml
# Redis Cluster StatefulSet
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis-cluster
spec:
  serviceName: redis-cluster
  replicas: 6  # 3 Master + 3 Slave
  podManagementPolicy: OrderedReady

  selector:
    matchLabels:
      app: redis-cluster

  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: redis-cluster
              topologyKey: kubernetes.io/hostname

      containers:
        - name: redis
          image: redis:7.0
          command:
            - redis-server
            - --cluster-enabled yes
            - --cluster-config-file /data/nodes.conf
            - --cluster-announce-ip $(POD_IP)
            - --cluster-announce-port 6379
            - --cluster-announce-bus-port 16379
          env:
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
          ports:
            - containerPort: 6379
            - containerPort: 16379  # Cluster bus
          volumeMounts:
            - name: data
              mountPath: /data

  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: fast-ssd
        resources:
          requests:
            storage: 10Gi
```

### 도입 시 고려사항 체크리스트

| 항목 | StatefulSet | DaemonSet | 비고 |
|---|---|---|---|
| **스토리지** | 필수 | 보통 없음 | PVC 템플릿 |
| **서비스** | Headless 필수 | 불필요 | DNS 디스커버리 |
| **순서 보장** | OrderedReady | 불필요 | 시작/종료 순서 |
| **노드 분산** | PodAntiAffinity | 자동 | 고가용성 |
| **톨러레이션** | 상황에 따라 | 마스터 노드용 | 노드 선택 |

### 안티패턴 및 주의사항

**안티패턴 1: StatefulSet에 ReadWriteMany PVC**
- 문제: DB는 동시 쓰기 불가
- 해결: ReadWriteOnce + 복제

**안티패턴 2: DaemonSet을 일반 앱에 사용**
- 문제: 노드당 1개만 실행됨
- 해결: Deployment 사용

**안티패턴 3: StatefulSet 무분별한 스케일 업**
- 문제: 쿼럼 손실 가능
- 해결: 홀수 유지, 한 번에 1개씩

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 수동 구성 | StatefulSet/DaemonSet | 개선율 |
|---|---|---|---|
| **배포 시간** | 1시간+ | 5분 | 92% 단축 |
| **장애 복구** | 30분+ | 2분 | 93% 단축 |
| **확장 시간** | 1시간 | 5분 | 92% 단축 |
| **인적 오류** | 높음 | 낮음 | 자동화 |

### 미래 전망 및 진화 방향

1. **StatefulSet 개선**: 더 빠른 장애 복구, 병렬 스케일링
2. **DaemonSet 개선**: 더 정교한 노드 선택, 카나리 배포
3. **Operator 패턴**: StatefulSet 기반 복잡한 앱 자동화

### ※ 참고 표준/가이드
- **Kubernetes Documentation**: StatefulSets, DaemonSets
- **Operator Framework**: Stateful 앱 관리
- **CNCF Storage Whitepaper**: 영구 스토리지

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [쿠버네티스 (Kubernetes)](@/studynotes/13_cloud_architecture/01_native/kubernetes.md) : 오케스트레이션 플랫폼
- [디플로이먼트 (Deployment)](@/studynotes/13_cloud_architecture/01_native/replicaset_deployment.md) : 상태 비저장 워크로드
- [PV/PVC](@/studynotes/13_cloud_architecture/_index.md) : 영구 볼륨
- [서비스 (Service)](@/studynotes/13_cloud_architecture/_index.md) : Headless Service
- [옵저버빌리티](@/studynotes/13_cloud_architecture/01_native/observability.md) : DaemonSet 기반 모니터링

---

### 👶 어린이를 위한 3줄 비유 설명
1. 스테이트풀셋은 **'번호표가 있는 사물함'**이에요. 0번, 1번, 2번... 각 사물함은 자기 번호와 자기 물건을 항상 가지고 있어요.
2. 데몬셋은 **'각 교실의 청소 당번'**이에요. 모든 교실에 딱 1명씩 있어야 해요. 새 교실이 생기면 자동으로 당번이 생겨요!
3. 이 두 가지 덕분에 **'데이터베이스나 로그 수집기'** 같은 중요한 프로그램들이 안전하게 돌아갈 수 있어요!
