+++
weight = 887
title = "87. 디플로이먼트 (Deployment)"
description = "Deployment: 레플리카셋을 관리하며 롤링 업데이트, 롤백, 버전 관리를 제공하는 쿠버네티스 워크로드 리소스"
date = 2026-03-26

[taxonomies]
tags = ["kubernetes", "k8s", "deployment", "rolling-update", "rollback", "workload"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Deployment는 쿠버네티스에서 가장 많이 사용되는 워크로드 리소스로, 레플리카셋을 상위에서 관리하여"desired replica 수의 파드가 실행되도록" 보장하며, 추가로"무중단 업데이트"와"이전 버전으로 롤백" 기능을 제공한다.
> 2. **가치**: Deployment를 사용하면 새 버전의 애플리케이션을 배포할 때 서비스 중단 없이 점진적으로 교체할 수 있고, 문제가 발생하면 이전 버전으로 즉시 롤백할 수 있다.
> 3. **융합**: Deployment spec.strategy.type=RollingUpdate로 설정하면 파드를 하나씩 교체하며, maxSurge와 maxUnavailable로 교체 속도와 가용성을 제어한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념 정의

Deployment는 쿠버네티스에서 가장 널리 사용되는"워크로드 리소스"이다. Deployment는 내부적으로 ReplicaSet을 管理하며, 여기에"애플리케이션 배포"에 필요한 추가 기능을Overlay한다. 예를 들어,"nginx 웹 서버 3개를 실행하고, 새 버전으로 업데이트 시 서비스 중단 없이 점진적으로 교체하고, 문제가 있으면 이전 버전으로 돌아갈 수 있다"는 요구사항을 Deployment 하나의 선언으로 표현할 수 있다. 이는 실제 운영에서 매우 실용적이며, 대부분의 쿠버네티스 배포 시나리오에서 Deployment가首选된다.

### 왜 Deployment인가?

ReplicaSet만 사용하면"파드가 항상 3개 실행된다"는 것은 보장하지만, 버전 업데이트는 직접管理해야 한다. 예를 들어, 새 버전으로 업데이트하려면 기존 ReplicaSet을 삭제하고 새 ReplicaSet을 생성해야 하는데, 이 과정에서 서비스가 일시中断된다. Deployment는 이러한"업데이트 시의 서비스 중단" 문제를 해결하기 위해"롤링 업데이트" 기능을 제공한다. 또한"업데이트 도중 문제 발생 시 이전 버전으로 돌아가는" 롤백 기능도 지원한다.

### 비유

Deployment를"고급 레스토랑의 메뉴 관리 시스템"에 비유할 수 있다. 셰프(Deployment)가"비프 스테이크 3그릇을 항상 제공해야 하고, 새 레시피로 변경 시 손님이식을interrupt하지 않고 전환하고,万一 손님이 불만으면 바로 전 레시피로 되돌릴 수 있다"고 관리한다. 일반 주방(ReplicaSet)이라면 레시피를 바꾸려면 영업을 중단하고 전员工를下班处理해야 하지만, 高級 레스토랑은 이를 자동으로 수행한다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Deployment와 ReplicaSet의 관계

Deployment가 생성되면, Deployment Controller가 대응하는 ReplicaSet을 생성한다. 업데이트 시에는 기존 ReplicaSet은 그대로 두고 新ReplicaSet을 생성하여 점진적으로 파드를 이동한다. 이 과정에서 두 개의 ReplicaSet이 동시에共存하며, 비율이 완전히新版本으로 바뀌면 기존 ReplicaSet은 축소된다. 이러한"2개의 ReplicaSet 관리"를 통해 롤백 기능을 실현한다.

### 롤링 업데이트 동작 과정

 롤링 업데이트는 다음 단계로 진행된다. (1) Deployment의 이미지를 새 버전으로更新한다. (2) Deployment Controller가新버전의 ReplicaSet을 생성한다 (replicas: 1). (3) 新ReplicaSet이 1개의 파드를 생성한다. (4)  기존 ReplicaSet의 replicas를 1 감소한다 (3→2). (5)  서비스는 계속 运行 중이며, 트래픽은 기존 버전 2개 + 新버전 1개로分散된다. (6)  위 과정을 반복하여新버전 3개, 기존 버전 0개가 되면 완료.

```
[ 롤링 업데이트 진행 과정 ]

초기 상태: nginx:v1 파드 3개
┌─────────────────────────────────────────────────────────────────────────┐
│  ReplicaSet (v1): [Pod A] [Pod B] [Pod C]  (replicas: 3)              │
└─────────────────────────────────────────────────────────────────────────┘

Step 1: v2 레플리카셋 생성 (replicas: 1)
┌─────────────────────────────────────────────────────────────────────────┐
│  ReplicaSet (v1): [Pod A] [Pod B]        (replicas: 2)                  │
│  ReplicaSet (v2): [Pod D]                (replicas: 1)                 │
└─────────────────────────────────────────────────────────────────────────┘
                      │                                                      │
                      │ kubectl set image deployment/nginx nginx=nginx:v2  │
                      ▼                                                      │
Step 2: v2 레플리카셋 확장 (replicas: 2), v1 축소 (replicas: 1)
┌─────────────────────────────────────────────────────────────────────────┐
│  ReplicaSet (v1): [Pod A]                 (replicas: 1)                 │
│  ReplicaSet (v2): [Pod D] [Pod E]         (replicas: 2)                 │
└─────────────────────────────────────────────────────────────────────────┘
                      │                                                      │
                      │ (계속 진행...)                                         │
                      ▼                                                      │
Step 3: 완료 (v1 레플리카셋 replicas: 0)
┌─────────────────────────────────────────────────────────────────────────┐
│  ReplicaSet (v1): (삭제)                                                │
│  ReplicaSet (v2): [Pod D] [Pod E] [Pod F]   (replicas: 3)              │
└─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 롤링 업데이트는"철도 레일 교체"에 비유할 수 있다. 기차가 运行 중이면서도 새 레일로 교체하려면, 列車を止めずに、部分的に新しいレールを敷设하고、既存のレールを外していく。 同様に、 Deployment는서비스를 完全に停止하지 않으면서、段階的に파드를 새 버전으로 교체한다. maxSurge와 maxUnavailableパラメータを変更すると、切り替え速度と可用性のバランスを調整できる。

### 롤백

 롤백은revisionHistoryLimit에 저장된 이전 ReplicaSet을 사용하여実現된다. 기본값은 10이며, 최대 10개までの 이전 버전을保存한다. kubectl rollout undo deployment/nginx를 실행하면, Deployment Controller가 이전 ReplicaSet의 replicas를 늘리고, 현재 ReplicaSet의 replicas를 줄인다.

### 전략 유형

Deployment의 spec.strategy.type에는 두 가지가 있다. **RollingUpdate**는 파드를 점진적으로 교체하며, maxSurge(최대 초과 파드 수)와 maxUnavailable(최대 불가능 파드 수)를 조절하여 속도와 가용성을 控制한다. **Recreate**는 모든 기존 파드를 먼저 삭제한 후 新파드를 생성한다. 서비스가一時的に中断되지만, 두 版本이 동시에 실행되지 않으므로，데이터 일관성이 중요한 경우에 사용한다.

### 섹션 비유

 롤링 업데이트의 maxSurge/maxUnavailable을"고속도로 차선 변경"에 비유할 수 있다. maxUnavailable을 0으로 설정하면"기존 차선을 완전히 점유한 상태에서 새 차선을 하나씩 열어 교체"하므로堵車가最少하지만 교체 속도가 느리다. maxSurge를 높게 설정하면"新车線을 미리 열어두고 기존 차선에서 한 대씩 이동"하므로堵車가 조금增加하지만 교체 속도가 빠르다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### Deployment vs StatefulSet vs DaemonSet

| 비교 항목 | Deployment | StatefulSet | DaemonSet |
|:---|:---|:---|:---|
| **파드 identity** | 랜덤 (A, B, C) | 고정 (nginx-0, nginx-1) | 모든 노드에 1개 |
| **스토리지** | 임시 (EmptyDir) | 영구 (PVC) | 없음 |
| **업데이트** | 롤링/Recreate | 순차 RollingUpdate | 롤링만 |
| **용도** | Stateless 앱 | DB, 메시지 큐 | 로그 수집, 모니터링 |

### 블루-그린 배포와의 비교

| 비교 항목 | 롤링 업데이트 | 블루-그린 배포 |
|:---|:---|:---|
| **동시 실행 파드 수** | N ~ N+maxSurge | 2N (일시적) |
| **롤백 시간** | 점진적 (수 분) | 즉時 (바로切替) |
| **트래픽 처리** | 자동 (LB가 분산) | 수동 (切替 URL) |
| **자원 비용** | 저렴 | 높음 (2배) |

### Canary Deployment

 Canary 배포는"카나리 새"에서 유래했다. 광부들이 카나리 새를 지하에 데려가했는데, 유독 가스가 새면 카나리가 먼저 죽어 위험을 알렸다. 同様に, 新버전을 전체 트래픽이 아닌 소량(1~5%)에만投入하여, 문제가 없으면 점진적으로 늘리고, 문제가 있으면即座に停止한다. 쿠버네티스에서는 Argo Rollouts나 Istio를 사용하여 Canary 배포를実現한다.

### 섹션 비유

 카나리 배포를"신제품試食会"에 비유할 수 있다. 完全한 신제품을 모든 고객에게 배포하는 대신, 首先 1%의 고객에게만試食을 제공하고, 맛있으면 5%, 10%, 50%...로 점진적으로 확대한다. 만약多数의 고객이 불만족하면即座에試食을 중단하고, 기존 제품으로 完全 복귀한다. 이것은"전면 출시 전에 위험을最小화하는"策略이다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### Deployment Manifest 예시

 기본적인 Deployment Manifest는 apiVersion: apps/v1, kind: Deployment, metadata: name, spec: replicas, selector, strategy, template으로 구성된다. template.spec에는 파드 템플릿(컨테이너, 환경 변수, 헬스체크 등)을定義한다. strategy.type=RollingUpdate일 경우, maxSurge=1, maxUnavailable=0이 기본값으로, 항상 전체 파드가 실행되면서 1개씩 교체한다.

### 문제 해결

**문제: 업데이트 진행 중 장애 발생** - `kubectl rollout status deployment/<name>`으로 진행 상황을 확인하고, `kubectl rollout undo deployment/<name>`으로 이전 버전으로 롤백한다.

**문제: 파드가 Pending 상태로 남아있음** - `kubectl describe pod <name>`으로 이유를 확인한다. 리소스 부족, 노드 어피니티 위반, 스토리지 프로비저닝 실패 등의 원인을 파악한다.

### Revision History

 revisionHistoryLimit는 保存할 이전 ReplicaSet 수를 지정한다. 너무 적게 설정하면 롤백 가능한 버전이 제한되고, 너무 많이 설정하면 etcd에 불필요한 리소스가 쌓인다. 일반적으로 10~20 정도가 적합하다.

### 섹션 비유

 revisionHistoryLimit를"사진첩의 사진 수"에 비유할 수 있다. 모든 사진을 保存하면 용량이 커지고 관리가 어려워지며, 너무 적게 保存하면 예전 모습을 回顧할 수 없다. 보통 최근 10~20장만 保存하는 것이 효율적이며, Deployment도 同様に 최소한의 이전 버전을 保存하여 불필요한 resource 낭비를 방지한다.

---

## ocultural Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대 효과

 Deployment를 利用하면"애플리케이션 배포의 完全自動化"가 가능해진다. 서비스 중단 없이新버전을 점진적으로 배포하고, 문제가 있으면即座에 롤백하며, revision 이력을 管理할 수 있다. 이는 데브옵스의"높은 배포 빈도, 낮은 실패율" 목표에 부합한다.

### 핵심 정리

 Deployment는 레플리카셋을 管理하며 롤링 업데이트, 롤백, 버전 관리 기능을 제공하는 가장 널리 사용되는 워크로드 리소스이다. RollingUpdate 전략은 maxSurge와 maxUnavailable를 조절하여 서비스 가용성과 배포 속도의 균형을 맞춘다. 카나리 배포 등 고급 배포 전략이 필요하면 Argo Rollouts나 Istio를 사용한다.

### 섹션 비유

 Deployment를"영화 배급 시스템"에 비유할 수 있다.影院(노드)에 동시에 3부작(파드 3개)를 상영해야 하고, 新作(버전 업데이트)으로 교체하려면影院을 닫지 않고 새 作을 동시에 начала 상영하면서 순차적으로 교체하고,혹시新作이 문제가 있으면 即座에舊作으로 돌아간다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **ReplicaSet** | Deployment가 管理하는 파드 복제 리소스로, desired replica 수를 유지한다. |
| **RollingUpdate** | 파드를 점진적으로 교체하여 서비스 중단을 방지하는 업데이트 전략이다. |
| **maxSurge / maxUnavailable** | 롤링 업데이트 중 허용되는 추가/불가능 파드 수를 제어한다. |
| **Rollback** | 이전 ReplicaSet을 사용하여 이전 버전으로 복귀하는 기능이다. |
| **Revision History** | 保存된 이전 ReplicaSet 목록으로, 롤백 가능한 버전을管理한다. |
| **StatefulSet** | 파드에 고정 identity와 영구 스토리지가 필요한 앱(DB 등)用 리소스이다. |
| **Argo Rollouts** | Canary, 블루-그린 등 고급 배포 전략을 제공하는 쿠버네티스 Controller이다. |
