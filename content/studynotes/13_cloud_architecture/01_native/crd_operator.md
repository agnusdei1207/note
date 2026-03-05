+++
title = "커스텀 리소스와 오퍼레이터 (CRD & Operator)"
date = 2026-03-05
description = "쿠버네티스 API를 확장하여 복잡한 상태 저장 애플리케이션을 자동화하는 선언적 관리 패턴의 원리와 아키텍처"
weight = 83
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["CRD", "Operator", "Kubernetes-Extension", "Custom-Resource", "Controller", "Automation"]
+++

# 커스텀 리소스와 오퍼레이터 (CRD & Operator) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CRD(Custom Resource Definition)는 쿠버네티스 API에 새로운 리소스 타입을 정의하고, 오퍼레이터(Operator)는 이 커스텀 리소스를 감시(Watch)하며 인간 운영자의 지식을 코드화하여 자동화하는 컨트롤러 패턴입니다.
> 2. **가치**: **데이터베이스 클러스터**, **메시지 큐**, **머신러닝 파이프라인** 같은 복잡한 상태 저장 애플리케이션의 **완전한 생명주기 관리**(프로비저닝, 백업, 복구, 스케일링, 업그레이드)를 선언적 코드로 자동화합니다.
> 3. **융합**: 쿠버네티스 컨트롤 런타임(Kubebuilder, Operator SDK), Helm, GitOps(ArgoCD), 서비스 메시와 결합하여 엔터프라이즈급 자동화 플랫폼을 구축합니다.

---

## Ⅰ. 개요 (Context & Background)

쿠버네티스의 핵심 철학은 '선언적 API'입니다. 사용자는 원하는 상태(Desired State)를 선언하고, 쿠버네티스 컨트롤러가 현재 상태(Current State)를 원하는 상태로 일치시킵니다. CRD와 Operator는 이 철학을 사용자 정의 리소스로 확장하여, 쿠버네티스 자체 기능처럼 동작하는 새로운 API를 만들 수 있게 합니다.

**💡 비유**:
- **CRD**는 **'새로운 양식 디자인'**입니다. 쿠버네티스에 "MyDatabase라는 새로운 신청서를 만들어줘"라고 요청하면, 쿠버네티스는 이 양식을 이해하고 저장합니다.
- **Operator**는 **'그 양식을 처리하는 전담 직원'**입니다. 누군가 MyDatabase 양식을 제출하면, 이 직원이 DB를 설치하고, 백업을 설정하고, 장애 시 복구까지 모든 것을 자동으로 처리합니다.

**등장 배경 및 발전 과정**:
1. **TPR (Third Party Resource, 2015)**: 초기 확장 메커니즘. 제한적.
2. **CRD (Custom Resource Definition, 2017)**: TPR을 대체. 더 강력한 검증, 스키마 지원.
3. **Operator 패턴 (2016)**: CoreOS가 소개. "운영자 지식을 코드로"
4. **Operator SDK / Kubebuilder (2018~)**: Operator 개발 프레임워크 등장.
5. **OperatorHub.io (2019)**: 커뮤니티 Operator 마켓플레이스.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 및 관계

| 구성 요소 | 상세 역할 | 기술 | 비고 |
|---|---|---|---|
| **CRD** | 새로운 리소스 타입 정의 | OpenAPI v3 스키마 | API 확장 |
| **Custom Resource (CR)** | CRD의 인스턴스 | YAML/JSON | 사용자가 생성 |
| **Controller** | CR을 감시하고 조정 | Go/Python/Java | 무한 루프 |
| **Reconcile Loop** | 상태 일치 로직 | etcd Watch | 핵심 메커니즘 |
| **Webhooks** | 검증/변경 가로채기 | Validating/Mutating | 정책 강제 |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ CRD & Operator Architecture ]                           │
└─────────────────────────────────────────────────────────────────────────────┘

[ 커스텀 리소스 정의 (CRD) ]

    ┌──────────────────────────────────────────────────────────────────────┐
    │                    Custom Resource Definition                         │
    │                                                                       │
    │  apiVersion: apiextensions.k8s.io/v1                                │
    │  kind: CustomResourceDefinition                                      │
    │  metadata:                                                           │
    │    name: mysqls.database.example.com                                 │
    │  spec:                                                               │
    │    group: database.example.com        ← API 그룹                     │
    │    names:                                                            │
    │      kind: MySQL                      ← 리소스 종류명                 │
    │      plural: mysqls                   ← 복수형                       │
    │      singular: mysql                  ← 단수형                       │
    │      shortNames: [my]                 ← 약어                         │
    │    scope: Namespaced                  ← 네임스페이스 범위             │
    │    versions:                                                          │
    │      - name: v1                                                      │
    │        served: true                                                  │
    │        storage: true                                                 │
    │        schema:                        ← OpenAPI v3 스키마            │
    │          openAPIV3Schema:                                            │
    │            type: object                                              │
    │            properties:                                               │
    │              spec:                                                   │
    │                type: object                                          │
    │                properties:                                           │
    │                  replicas:                                           │
    │                    type: integer                                     │
    │                    minimum: 1                                        │
    │                    maximum: 10                                       │
    │                  version:                                            │
    │                    type: string                                      │
    │                  storageSize:                                        │
    │                    type: string                                      │
    │                    pattern: "^[0-9]+Gi$"                             │
    │                required: [replicas, version]                         │
    │                                                                       │
    └──────────────────────────────────────────────────────────────────────┘


[ 커스텀 리소스 (CR) - CRD의 인스턴스 ]

    ┌──────────────────────────────────────────────────────────────────────┐
    │                    Custom Resource Instance                           │
    │                                                                       │
    │  apiVersion: database.example.com/v1                                │
    │  kind: MySQL                                                          │
    │  metadata:                                                           │
    │    name: production-mysql                                            │
    │    namespace: database                                               │
    │  spec:                                                               │
    │    replicas: 3                        ← 원하는 복제본 수              │
    │    version: "8.0"                     ← MySQL 버전                   │
    │    storageSize: "100Gi"               ← 스토리지 크기                 │
    │    backup:                                                           │
    │      enabled: true                                                   │
    │      schedule: "0 2 * * *"            ← 매일 새벽 2시                │
    │      retention: 7d                    ← 7일 보관                     │
    │    monitoring:                                                       │
    │      enabled: true                                                   │
    │    resources:                                                        │
    │      requests:                                                       │
    │        cpu: 500m                                                     │
    │        memory: 1Gi                                                   │
    │  status:                             ← Operator가 업데이트           │
    │    phase: Running                                                    │
    │    currentReplicas: 3                                                │
    │    readyReplicas: 3                                                  │
    │    lastBackup: "2026-03-05T02:00:00Z"                               │
    │                                                                       │
    └──────────────────────────────────────────────────────────────────────┘


[ Operator 컨트롤러 구조 ]

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                          Operator Process                                │
    │                                                                         │
    │  ┌────────────────────────────────────────────────────────────────────┐│
    │  │                     Controller Manager                              ││
    │  │                                                                    ││
    │  │  ┌─────────────────┐      ┌─────────────────────────────────────┐ ││
    │  │  │   Informer      │      │          Reconcile Loop             │ ││
    │  │  │                 │      │                                     │ ││
    │  │  │  Watch etcd     │─────►│  func Reconcile(req Request) {     │ ││
    │  │  │  for MySQL CR   │      │    // 1. CR 조회                    │ ││
    │  │  │                 │      │    cr := &MySQL{}                   │ ││
    │  │  │  On Add/Update/ │      │    client.Get(ctx, req.Name, cr)   │ ││
    │  │  │  Delete events  │      │                                     │ ││
    │  │  │                 │      │    // 2. 현재 상태 확인              │ ││
    │  │  │  Queue events   │      │    current := getStatus(cr)         │ ││
    │  │  └─────────────────┘      │                                     │ ││
    │  │                           │    // 3. 원하는 상태와 비교           │ ││
    │  │                           │    if !matches(cr.Spec, current) {  │ ││
    │  │                           │      // 4. 조치 수행                 │ ││
    │  │                           │      reconcile(cr)                  │ ││
    │  │                           │    }                                │ ││
    │  │                           │                                     │ ││
    │  │                           │    // 5. 상태 업데이트               │ ││
    │  │                           │    updateStatus(cr)                 │ ││
    │  │                           │                                     │ ││
    │  │                           │    return ctrl.Result{}, nil        │ ││
    │  │                           │  }                                  │ ││
    │  │                           └─────────────────────────────────────┘ ││
    │  │                                                                    ││
    │  └────────────────────────────────────────────────────────────────────┘│
    │                                                                         │
    │  Reconcile이 수행하는 작업:                                              │
    │  - StatefulSet 생성/수정                                                │
    │  - Service 생성                                                         │
    │  - ConfigMap/Secret 생성                                                │
    │  - PVC 프로비저닝                                                       │
    │  - 백업 Job 스케줄링                                                    │
    │  - 장애 복구                                                            │
    │  - 버전 업그레이드                                                       │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘


[ Webhook 아키텍처 ]

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                    Admission Webhooks                                    │
    │                                                                         │
    │  [ 요청 흐름 ]                                                           │
    │                                                                         │
    │  kubectl apply ──► API Server ──► Authentication ──► Authorization     │
    │                                              │                          │
    │                                              ▼                          │
    │                                    ┌────────────────┐                  │
    │                                    │ Admission      │                  │
    │                                    │ Webhooks       │                  │
    │                                    └───────┬────────┘                  │
    │                                            │                           │
    │                      ┌─────────────────────┼─────────────────────┐    │
    │                      │                     │                     │    │
    │                      ▼                     ▼                     ▼    │
    │              ┌───────────────┐    ┌───────────────┐    ┌─────────────┐│
    │              │ Mutating      │    │ Validating   │    │ Conversion  ││
    │              │ Webhook       │    │ Webhook       │    │ Webhook     ││
    │              │               │    │               │    │             ││
    │              │ - 기본값 설정  │    │ - 스펙 검증   │    │ - 버전 변환 ││
    │              │ - 필드 수정   │    │ - 정책 강제   │    │             ││
    │              │               │    │ - 거부 가능   │    │             ││
    │              └───────┬───────┘    └───────┬───────┘    └──────┬──────┘│
    │                      │                    │                    │       │
    │                      └────────────────────┴────────────────────┘       │
    │                                           │                            │
    │                                           ▼                            │
    │                                    ┌────────────┐                      │
    │                                    │   etcd     │                      │
    │                                    │  (저장)    │                      │
    │                                    └────────────┘                      │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: Reconcile Loop

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    Reconcile Loop 상세 메커니즘                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  Level-triggered Logic (수준 트리거) vs Edge-triggered (엣지 트리거)         │
│                                                                            │
│  Level-triggered (Operator 방식):                                          │
│  - "현재 상태가 목표와 같은가?"만 확인                                       │
│  - 이벤트를 놓쳐도 재조정 가능                                               │
│  - 멱등성(Idempotency) 필수                                                │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  Reconcile Flow Example: MySQL Operator                              │  │
│  │                                                                     │  │
│  │  Input: Request {Name: "production-mysql", Namespace: "database"}  │  │
│  │                                                                     │  │
│  │  Step 1: CR 조회                                                    │  │
│  │    mysql := &MySQL{}                                                │  │
│  │    err := r.Client.Get(ctx, req.NamespacedName, mysql)             │  │
│  │    if errors.IsNotFound(err) {                                     │  │
│  │      // CR가 삭제됨 - 정리 로직                                      │  │
│  │      return ctrl.Result{}, nil                                      │  │
│  │    }                                                                │  │
│  │                                                                     │  │
│  │  Step 2: 자식 리소스 조회                                            │  │
│  │    sts := &appsv1.StatefulSet{}                                    │  │
│  │    err := r.Client.Get(ctx, stsKey, sts)                           │  │
│  │                                                                     │  │
│  │  Step 3: StatefulSet 없으면 생성                                    │  │
│  │    if errors.IsNotFound(err) {                                     │  │
│  │      sts = r.buildStatefulSet(mysql)                               │  │
│  │      r.Client.Create(ctx, sts)                                     │  │
│  │      return ctrl.Result{Requeue: true}, nil  // 재조정 요청         │  │
│  │    }                                                                │  │
│  │                                                                     │  │
│  │  Step 4: StatefulSet이 CR 스펙과 일치하는지 확인                     │  │
│  │    if !r.specMatches(mysql, sts) {                                 │  │
│  │      sts.Spec = r.buildStatefulSet(mysql).Spec                     │  │
│  │      r.Client.Update(ctx, sts)                                     │  │
│  │      return ctrl.Result{Requeue: true}, nil                        │  │
│  │    }                                                                │  │
│  │                                                                     │  │
│  │  Step 5: 상태 업데이트                                               │  │
│  │    mysql.Status.ReadyReplicas = sts.Status.ReadyReplicas           │  │
│  │    mysql.Status.Phase = "Running"                                  │  │
│  │    r.Client.Status().Update(ctx, mysql)                            │  │
│  │                                                                     │  │
│  │  Step 6: 재조정 스케줄 (선택적)                                      │  │
│  │    return ctrl.Result{RequeueAfter: 1 * time.Minute}, nil          │  │
│  │                                                                     │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  Requeue 전략:                                                              │
│  - Requeue: true → 즉시 재조정                                              │
│  - RequeueAfter: duration → 지정 시간 후 재조정                             │
│  - return empty → 이벤트 발생 시까지 대기                                   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: MySQL Operator 구현 (Kubebuilder)

```go
// MySQL Operator 구현 (Kubebuilder 기반)

// API 타입 정의 (api/v1/mysql_types.go)
package v1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// MySQLSpec defines the desired state of MySQL
type MySQLSpec struct {
	// +kubebuilder:validation:Minimum=1
	// +kubebuilder:validation:Maximum=10
	Replicas int32 `json:"replicas"`

	// +kubebuilder:validation:Pattern="^[0-9]+(\\.[0-9]+)?$"
	Version string `json:"version"`

	// +kubebuilder:validation:Pattern="^[0-9]+Gi$"
	StorageSize string `json:"storageSize"`

	// 백업 설정
	Backup BackupConfig `json:"backup,omitempty"`

	// 리소스 제한
	Resources corev1.ResourceRequirements `json:"resources,omitempty"`
}

type BackupConfig struct {
	Enabled   bool   `json:"enabled,omitempty"`
	Schedule  string `json:"schedule,omitempty"`
	Retention string `json:"retention,omitempty"`
}

// MySQLStatus defines the observed state of MySQL
type MySQLStatus struct {
	Phase           MySQLPhase `json:"phase,omitempty"`
	CurrentReplicas int32      `json:"currentReplicas,omitempty"`
	ReadyReplicas   int32      `json:"readyReplicas,omitempty"`
	LastBackup      string     `json:"lastBackup,omitempty"`
	Conditions      []metav1.Condition `json:"conditions,omitempty"`
}

type MySQLPhase string

const (
	PhaseCreating MySQLPhase = "Creating"
	PhaseRunning  MySQLPhase = "Running"
	PhaseFailed   MySQLPhase = "Failed"
	PhaseUpdating MySQLPhase = "Updating"
)

//+kubebuilder:object:root=true
//+kubebuilder:subresource:status

// MySQL is the Schema for the mysqls API
type MySQL struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   MySQLSpec   `json:"spec,omitempty"`
	Status MySQLStatus `json:"status,omitempty"`
}

//+kubebuilder:object:root=true

// MySQLList contains a list of MySQL
type MySQLList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []MySQL `json:"items"`
}

func init() {
	SchemeBuilder.Register(&MySQL{}, &MySQLList{})
}

// controllers/mysql_controller.go
package controllers

import (
	"context"
	"fmt"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/errors"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/log"

	databasev1 "example.com/mysql-operator/api/v1"
)

// MySQLReconciler reconciles a MySQL object
type MySQLReconciler struct {
	client.Client
	Scheme *runtime.Scheme
}

// RBAC 마커
//+kubebuilder:rbac:groups=database.example.com,resources=mysqls,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=database.example.com,resources=mysqls/status,verbs=get;update;patch
//+kubebuilder:rbac:groups=apps,resources=statefulsets,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=core,resources=services,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=core,resources=configmaps,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=core,resources=secrets,verbs=get;list;watch;create;update;patch;delete

// Reconcile is part of the main kubernetes reconciliation loop
func (r *MySQLReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	logger := log.FromContext(ctx)

	// 1. MySQL CR 조회
	mysql := &databasev1.MySQL{}
	if err := r.Get(ctx, req.NamespacedName, mysql); err != nil {
		if errors.IsNotFound(err) {
			logger.Info("MySQL resource not found, likely deleted")
			return ctrl.Result{}, nil
		}
		return ctrl.Result{}, err
	}

	// 2. StatefulSet 확인 및 생성/업데이트
	sts, err := r.reconcileStatefulSet(ctx, mysql)
	if err != nil {
		return ctrl.Result{}, err
	}

	// 3. Service 확인 및 생성/업데이트
	if err := r.reconcileService(ctx, mysql); err != nil {
		return ctrl.Result{}, err
	}

	// 4. ConfigMap 확인 및 생성/업데이트
	if err := r.reconcileConfigMap(ctx, mysql); err != nil {
		return ctrl.Result{}, err
	}

	// 5. Secret 확인 및 생성/업데이트
	if err := r.reconcileSecret(ctx, mysql); err != nil {
		return ctrl.Result{}, err
	}

	// 6. 백업 설정 (활성화된 경우)
	if mysql.Spec.Backup.Enabled {
		if err := r.reconcileBackupCronJob(ctx, mysql); err != nil {
			return ctrl.Result{}, err
		}
	}

	// 7. 상태 업데이트
	mysql.Status.CurrentReplicas = sts.Status.CurrentReplicas
	mysql.Status.ReadyReplicas = sts.Status.ReadyReplicas

	if sts.Status.ReadyReplicas == mysql.Spec.Replicas {
		mysql.Status.Phase = databasev1.PhaseRunning
	} else {
		mysql.Status.Phase = databasev1.PhaseCreating
	}

	if err := r.Status().Update(ctx, mysql); err != nil {
		return ctrl.Result{}, err
	}

	logger.Info("MySQL reconciled successfully",
		"replicas", mysql.Status.ReadyReplicas,
		"phase", mysql.Status.Phase)

	// 주기적 재조정 (1분마다)
	return ctrl.Result{RequeueAfter: time.Minute}, nil
}

// reconcileStatefulSet - StatefulSet 조정
func (r *MySQLReconciler) reconcileStatefulSet(ctx context.Context, mysql *databasev1.MySQL) (*appsv1.StatefulSet, error) {
	sts := &appsv1.StatefulSet{}
	err := r.Get(ctx, types.NamespacedName{
		Name:      mysql.Name,
		Namespace: mysql.Namespace,
	}, sts)

	if errors.IsNotFound(err) {
		// StatefulSet 생성
		sts = r.buildStatefulSet(mysql)
		if err := ctrl.SetControllerReference(mysql, sts, r.Scheme); err != nil {
			return nil, err
		}
		if err := r.Create(ctx, sts); err != nil {
			return nil, err
		}
		return sts, nil
	}

	if err != nil {
		return nil, err
	}

	// 스펙이 변경되었으면 업데이트
	if !r.statefulSetSpecMatches(mysql, sts) {
		updated := r.buildStatefulSet(mysql)
		sts.Spec = updated.Spec
		if err := r.Update(ctx, sts); err != nil {
			return nil, err
		}
	}

	return sts, nil
}

// buildStatefulSet - StatefulSet 스펙 생성
func (r *MySQLReconciler) buildStatefulSet(mysql *databasev1.MySQL) *appsv1.StatefulSet {
	replicas := mysql.Spec.Replicas

	return &appsv1.StatefulSet{
		ObjectMeta: metav1.ObjectMeta{
			Name:      mysql.Name,
			Namespace: mysql.Namespace,
			Labels: map[string]string{
				"app":     "mysql",
				"cr.name": mysql.Name,
			},
		},
		Spec: appsv1.StatefulSetSpec{
			ServiceName: mysql.Name + "-headless",
			Replicas:    &replicas,
			Selector: &metav1.LabelSelector{
				MatchLabels: map[string]string{
					"app":     "mysql",
					"cr.name": mysql.Name,
				},
			},
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{
					Labels: map[string]string{
						"app":     "mysql",
						"cr.name": mysql.Name,
					},
				},
				Spec: corev1.PodSpec{
					Containers: []corev1.Container{
						{
							Name:  "mysql",
							Image: fmt.Sprintf("mysql:%s", mysql.Spec.Version),
							Ports: []corev1.ContainerPort{
								{ContainerPort: 3306, Name: "mysql"},
							},
							Env: []corev1.EnvVar{
								{Name: "MYSQL_ROOT_PASSWORD", ValueFrom: &corev1.EnvVarSource{
									SecretKeyRef: &corev1.SecretKeySelector{
										LocalObjectReference: corev1.LocalObjectReference{
											Name: mysql.Name + "-secret",
										},
										Key: "root-password",
									},
								}},
							},
							VolumeMounts: []corev1.VolumeMount{
								{Name: "data", MountPath: "/var/lib/mysql"},
							},
							Resources: mysql.Spec.Resources,
						},
					},
				},
			},
			VolumeClaimTemplates: []corev1.PersistentVolumeClaim{
				{
					ObjectMeta: metav1.ObjectMeta{Name: "data"},
					Spec: corev1.PersistentVolumeClaimSpec{
						AccessModes: []corev1.PersistentVolumeAccessMode{corev1.ReadWriteOnce},
						Resources: corev1.VolumeResourceRequirements{
							Requests: corev1.ResourceList{
								corev1.ResourceStorage: resource.MustParse(mysql.Spec.StorageSize),
							},
						},
					},
				},
			},
		},
	}
}

// SetupWithManager sets up the controller with the Manager.
func (r *MySQLReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&databasev1.MySQL{}).
		Owns(&appsv1.StatefulSet{}).
		Owns(&corev1.Service{}).
		Owns(&corev1.ConfigMap{}).
		Owns(&corev1.Secret{}).
		Complete(r)
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Operator vs Helm vs Kustomize

| 비교 관점 | Operator | Helm | Kustomize |
|---|---|---|---|
| **접근 방식** | 실행 시간 제어 | 템플릿 렌더링 | 오버레이 패치 |
| **상태 관리** | 실시간 조정 | 1회성 배포 | 1회성 배포 |
| **자동화** | 완전 자동화 | 수동 | 수동 |
| **복잡성** | 높음 | 중간 | 낮음 |
| **데이 라이프사이클** | 완전 지원 | 제한적 | 제한적 |
| **적합 상황** | DB, 복잡한 앱 | 일반 앱 | 설정 변형 |
| **학습 곡선** | 높음 | 중간 | 낮음 |

### 유명 Operator 목록

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ Popular Operators ]                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 데이터베이스                                                              ││
│  │ - MySQL Operator (Oracle/Presslabs)                                     ││
│  │ - PostgreSQL Operator (Zalando)                                         ││
│  │ - MongoDB Community Operator                                            ││
│  │ - Redis Operator (Spotahome)                                            ││
│  │ - Cassandra Operator (Instaclustr)                                      ││
│  │ - Couchbase Operator                                                    ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 메시지 큐 / 스트리밍                                                       ││
│  │ - Kafka Operator (Strimzi)                                              ││
│  │ - RabbitMQ Cluster Operator                                             ││
│  │ - Pulsar Operator                                                       ││
│  │ - NATS Operator                                                         ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 머신러닝 / AI                                                             ││
│  │ - Kubeflow Operators                                                    ││
│  │ - TensorFlow Operator                                                   ││
│  │ - PyTorch Operator                                                      ││
│  │ - Ray Operator                                                          ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 스토리지                                                                  ││
│  │ - Rook (Ceph) Operator                                                  ││
│  │ - MinIO Operator                                                        ││
│  │ - Longhorn Operator                                                     ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 서비스 메시 / 인프라                                                       ││
│  │ - Istio Operator                                                        ││
│  │ - Linkerd Operator                                                      ││
│  │ - Consul Operator                                                       ││
│  │ - Prometheus Operator                                                   ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 과목 융합 관점 분석

**데이터베이스와의 융합**:
- **자동 장애 복구**: Primary 실패 시 자동 Failover
- **백업/복구**: 스케줄 기반 백업, Point-in-Time 복구
- **스케일링**: 읽기 전용 복제본 자동 추가

**네트워크와의 융합**:
- **Service 생성**: Headless Service, Read Service 자동 구성
- **DNS 관리**: Pod DNS 레코드 자동 설정

**보안(Security)과의 융합**:
- **Secret 관리**: 인증서, 비밀번호 자동 교체
- **RBAC**: Operator 권한 최소화

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: Kafka 클러스터 자동화

**문제 상황**: 10노드 Kafka 클러스터를 수동으로 관리 중, 장애 복구에 2시간 소요

**기술사의 Operator 도입 전략**:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ Kafka Operator 도입 전략 ]                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. Strimzi Operator 도입                                                    │
│                                                                              │
│     CRD: Kafka, KafkaTopic, KafkaUser, KafkaConnect                         │
│                                                                              │
│  2. 선언적 클러스터 정의                                                       │
│                                                                              │
│     apiVersion: kafka.strimzi.io/v1beta2                                    │
│     kind: Kafka                                                              │
│     metadata:                                                                │
│       name: production-kafka                                                 │
│     spec:                                                                    │
│       kafka:                                                                 │
│         replicas: 10                                                         │
│         version: 3.5.1                                                       │
│         listeners:                                                           │
│           - name: plain                                                      │
│             port: 9092                                                       │
│             type: internal                                                   │
│           - name: tls                                                        │
│             port: 9093                                                       │
│             type: internal                                                   │
│             tls: true                                                        │
│         storage:                                                             │
│           type: jbod                                                         │
│           volumes:                                                           │
│             - id: 0                                                          │
│               type: persistent-claim                                         │
│               size: 1Ti                                                      │
│         config:                                                              │
│           offsets.topic.replication.factor: 3                               │
│           transaction.state.log.replication.factor: 3                       │
│       zookeeper:                                                             │
│         replicas: 3                                                          │
│         storage:                                                             │
│           type: persistent-claim                                             │
│           size: 100Gi                                                        │
│                                                                              │
│  3. 자동화 기능                                                               │
│     ├── 파드 장애 시 자동 재시작                                               │
│     ├── 노드 장애 시 다른 노드로 이동                                          │
│     ├── 롤링 업그레이드                                                        │
│     ├── 인증서 자동 교체 (tls)                                                 │
│     ├── JMX 메트릭 노출                                                       │
│     └── Cruise Control 연동 (리밸런싱)                                        │
│                                                                              │
│  4. 효과                                                                      │
│     ├── 장애 복구: 2시간 → 5분                                                │
│     ├── 버전 업그레이드: 수동 → 자동                                           │
│     └── 운영 오류: 감소                                                       │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 도입 시 고려사항 체크리스트

| 항목 | 확인 사항 | 비고 |
|---|---|---|
| **CRD 버전 관리** | 스키마 진화 전략 | Conversion Webhook |
| **RBAC** | 최소 권한 원칙 | 필요한 권한만 |
| **상태 관리** | Status 필드 설계 | Conditions 활용 |
| **에러 처리** | 재시도 전략 | Exponential Backoff |
| **테스트** | Envtest, E2E | 컨트롤러 테스트 |

### 안티패턴 및 주의사항

**안티패턴 1: 과도한 로직을 Reconcile에 넣기**
- 문제: 복잡한 로직은 실패 지점 증가
- 해결: 단순한 조정 로직, 별도 워크로드로 분리

**안티패턴 2: 외부 상태 의존**
- 문제: 클러스터 외부 상태가 변경되면 감지 못 함
- 해결: 주기적 재조정 (RequeueAfter)

**안티패턴 3: CRD 스펙 빈번 변경**
- 문제: 버전 호환성 문제
- 해결: Conversion Webhook, deprecation 정책

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 수동 관리 | Operator | 개선율 |
|---|---|---|---|
| **프로비저닝** | 4시간 | 10분 | 96% 단축 |
| **장애 복구** | 2시간 | 5분 | 96% 단축 |
| **업그레이드** | 8시간 | 30분 | 94% 단축 |
| **운영 오류** | 높음 | 낮음 | 자동화 |

### 미래 전망 및 진화 방향

1. **AI 기반 Operator**: 자동 튜닝, 이상 탐지
2. **Crossplane**: 더 일반화된 인프라 제어
3. **OAM (Open Application Model)**: 애플리케이션 모델 표준화

### ※ 참고 표준/가이드
- **Operator Framework**: Red Hat Operator SDK
- **Kubebuilder**: SIG API Machinery
- **OperatorHub.io**: 커뮤니티 Operator 목록

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [쿠버네티스 (Kubernetes)](@/studynotes/13_cloud_architecture/01_native/kubernetes.md) : 오케스트레이션 플랫폼
- [스테이트풀셋 (StatefulSet)](@/studynotes/13_cloud_architecture/01_native/statefulset_daemonset.md) : 상태 저장 워크로드
- [Helm](@/studynotes/13_cloud_architecture/_index.md) : 패키지 매니저
- [GitOps](@/studynotes/13_cloud_architecture/01_native/ci_cd.md) : 선언적 배포
- [CI/CD](@/studynotes/13_cloud_architecture/01_native/ci_cd.md) : 배포 자동화

---

### 👶 어린이를 위한 3줄 비유 설명
1. CRD는 **'새로운 주문서 양식'**을 만드는 거예요. "MySQL 주문서"를 만들면 쿠버네티스가 이해해요.
2. Operator는 **'그 주문서를 처리하는 로봇 직원'**이에요. 주문서가 들어오면 DB 설치, 백업, 복구까지 다 해줘요!
3. 덕분에 **'사람이 직접 하던 복잡한 일'**을 로봇이 알아서 해요. 실수도 줄어들고 빨라져요!
