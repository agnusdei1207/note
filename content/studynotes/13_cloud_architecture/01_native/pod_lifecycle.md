+++
title = "파드 생명주기 및 프로브 (Pod Lifecycle & Probes)"
date = "2026-03-05"
[extra]
categories = "studynotes-cloud"
tags = ["kubernetes", "pod", "lifecycle", "probes", "health-check", "container"]
+++

# 파드 생명주기 및 프로브 (Pod Lifecycle & Probes)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 파드 생명주기는 Pending → Running → Succeeded/Failed/Unknown의 유한 상태 머신으로, Liveness/Readiness/Startup 프로브가 컨테이너 건강 상태를 감지하여 자동 복구와 트래픽 라우팅을 제어합니다.
> 2. **가치**: 적절한 프로브 설정으로 무중단 서비스(Zero Downtime)를 달성하고, 데드락·메모리 누수 등 런타임 장애를 자동 감지·복구하여 가용성을 99.9% 이상으로 유지합니다.
> 3. **융합**: 서비스 메시의 서킷 브레이커, HPA 오토스케일링, Graceful Shutdown과 연동하여 클라우드 네이티브 회복 탄력성(Resilience)의 핵심 기반을 형성합니다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의
파드 생명주기(Pod Lifecycle)는 쿠버네티스에서 파드가 생성되어 종료될 때까지 거치는 일련의 상태 변화와 그에 따른 동작을 의미합니다. 파드는 Pending, Running, Succeeded, Failed, Unknown의 5가지 위상(Phase)을 가지며, 각 컨테이너는 Waiting, Running, Terminated의 3가지 상태를 가집니다. 프로브(Probe)는 kubelet이 주기적으로 컨테이너 상태를 진단하는 메커니즘으로, Liveness(생존), Readiness(준비), Startup(시작)의 세 가지 유형이 있습니다.

### 💡 비유
파드 생명주기는 "환자의 병원 치료 과정"과 같습니다. 응급실 도착(Pending) → 입원 및 치료 중(Running) → 완치 퇴원(Succeeded) 또는 사망(Failed)의 단계를 거치죠. 의사(kubelet)는 활력 징후를 정기적으로 확인(Liveness Probe)하고, 환자가 면회 가능한지(Readiness Probe), 중환자실에서 일반 병동으로 옮길 준비가 됐는지(Startup Probe)를 판단합니다.

### 등장 배경 및 발전 과정

#### 1. 기존 컨테이너 운영의 한계
- **좀비 프로세스**: 데드락에 빠진 컨테이너가 여전히 실행 중으로 표시
- **트래픽 유실**: 아직 준비되지 않은 컨테이너로 로드밸런서가 트래픽 전송
- **콜드 스타트 문제**: 무거운 애플리케이션 부팅 중过早한 헬스체크 실패

#### 2. 패러다임 변화
```
2015년: Kubernetes v1.0 - 기본 Liveness/Readiness Probe 도입
2017년: v1.7 - Initial Delay Seconds (initialDelaySeconds) 개선
2018년: v1.10 - exec, httpGet, tcpSocket 프로브 타입 안정화
2020년: v1.18 - Startup Probe 도입 (느린 시작 컨테이너 지원)
2021년: v1.20 - Graceful Node Shutdown (파드 정상 종료)
2023년: v1.27 - Sidecar 컨테이너 생명주기 개선
```

#### 3. 비즈니스적 요구사항
- **SLA 달성**: 99.9% 가용성 → 연간 8.76시간 다운타임만 허용
- **무중단 배포**: Rolling Update 중 서비스 중단 방지
- **빠른 장애 복구**: MTTR(Mean Time To Recovery) 최소화

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|-----------|------|
| **Pod Phase** | 파드 전체 상태 | 5가지 상태 (Pending/Running/Succeeded/Failed/Unknown) | k8s API | 환자 진료 상태 |
| **Container State** | 개별 컨테이너 상태 | Waiting/Running/Terminated | kubelet | 장기 상태 |
| **Liveness Probe** | 컨테이너 생존 확인 | 실패 시 컨테이너 재시작 | RestartPolicy | 심박동 체크 |
| **Readiness Probe** | 트래픽 수신 준비 확인 | 실패 시 Endpoints에서 제외 | Service | 면회 가능 여부 |
| **Startup Probe** | 시작 완료 확인 | 실패 시 컨테이너 재시작 | initialDelaySeconds 대체 | 중환자실 졸업 |
| **PreStop Hook** | 종료 전 실행 | SIGTERM 전 사용자 정의 명령 | Lifecycle | 유언장 작성 |
| **Termination Grace Period** | 정상 종료 대기 시간 | 기본 30초, SIGKILL까지 대기 | spec.terminationGracePeriodSeconds | 정리 시간 |
| **RestartPolicy** | 재시작 정책 | Always/OnFailure/Never | kubelet | 응급 조치 결정 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          파드 생명주기 상태 머신                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │                         Pod Phase Transition                              │  │
│   │                                                                           │  │
│   │    ┌──────────┐      스케줄링 성공      ┌──────────┐                    │  │
│   │    │ Pending  │ ──────────────────────▶ │ Running  │                    │  │
│   │    │          │                         │          │                    │  │
│   │    │ - 파드 생성  │                         │ - 컨테이너 │                    │  │
│   │    │ - PV 바인딩 │                         │   실행 중  │                    │  │
│   │    │ - 스케줄링 │                         │ - 프로브   │                    │  │
│   │    │   대기    │                         │   동작    │                    │  │
│   │    └──────────┘                         └────┬─────┘                    │  │
│   │         │                                    │                           │  │
│   │         │ 스케줄링 실패                       │                           │  │
│   │         │ (Preemption, 리소스 부족)           ├──────────┐               │  │
│   │         ▼                                    │          ▼               │  │
│   │    ┌──────────┐                         ┌────┴─────┐ ┌──────────┐       │  │
│   │    │  Failed  │ ◀────────────────────── │ Evicted  │ │Succeeded │       │  │
│   │    │          │   컨테이너 종료 코드!=0   │          │ │          │       │  │
│   │    │ - 컨테이너 │   RestartPolicy=Never   │ - 노드    │ │ - 모든    │       │  │
│   │    │   비정상  │   또는 재시도 횟수 초과   │   축출    │ │   컨테이너 │       │  │
│   │    │ - OOM    │                         │ - 리소스  │ │   정상    │       │  │
│   │    │ - Image  │                         │   부족    │ │   종료(0) │       │  │
│   │    │   Pull   │                         └──────────┘ └──────────┘       │  │
│   │    └──────────┘                                                      │  │
│   │         ▲                                                             │  │
│   │         │ 마스터-노드 통신 단절                                         │  │
│   │    ┌────┴─────┐                                                       │  │
│   │    │ Unknown  │ ◀─────────────────────────────────────────────────    │  │
│   │    │          │   (노드 장애, 네트워크 단절 시 상태 불명)                │  │
│   │    └──────────┘                                                       │  │
│   └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │                    Container State Transition                             │  │
│   │                                                                           │  │
│   │    ┌──────────┐      이미지 Pull 완료      ┌──────────┐                 │  │
│   │    │ Waiting  │ ─────────────────────────▶ │ Running  │                 │  │
│   │    │          │                            │          │                 │  │
│   │    │ - ContainerCreating                  │ - 프로세스 │                 │  │
│   │    │ - CrashLoopBackOff                   │   실행    │                 │  │
│   │    │ - ImagePullBackOff                   │ - 프로브   │                 │  │
│   │    │ - ErrImagePull                       │   체크    │                 │  │
│   │    └──────────┘                            └────┬─────┘                 │  │
│   │         │                                       │                        │  │
│   │         │ 이미지 Pull 실패                       │ 종료 신호              │  │
│   │         │ (권한, 네트워크)                        │ (exit code)           │  │
│   │         │                                       ▼                        │  │
│   │         │                                 ┌──────────┐                 │  │
│   │         └────────────────────────────────▶│Terminated│                 │  │
│   │                                           │          │                 │  │
│   │                                           │ - Exit 0 │                 │  │
│   │                                           │   (정상) │                 │  │
│   │                                           │ - Exit 1 │                 │  │
│   │                                           │   (에러) │                 │  │
│   │                                           │ - Exit 137│                │  │
│   │                                           │   (OOM)  │                 │  │
│   │                                           └──────────┘                 │  │
│   └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │                         Probe Execution Flow                              │  │
│   │                                                                           │  │
│   │   ┌─────────────────────────────────────────────────────────────────┐   │  │
│   │   │                     Kubelet Probe Manager                         │   │  │
│   │   │                                                                   │   │  │
│   │   │   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │   │  │
│   │   │   │ Liveness Probe │  │Readiness Probe │  │ Startup Probe  │   │   │  │
│   │   │   │ (주기적 체크)   │  │ (주기적 체크)   │  │ (시작 시만)    │   │   │  │
│   │   │   └───────┬────────┘  └───────┬────────┘  └───────┬────────┘   │   │  │
│   │   │           │                   │                   │             │   │  │
│   │   │           ▼                   ▼                   ▼             │   │  │
│   │   │   ┌─────────────────────────────────────────────────────────┐   │   │  │
│   │   │   │              Probe Execution (3가지 방식)                 │   │   │  │
│   │   │   │                                                         │   │   │  │
│   │   │   │  [httpGet]         [exec]           [tcpSocket]        │   │   │  │
│   │   │   │  HTTP GET 요청     명령어 실행       TCP 포트 연결       │   │   │  │
│   │   │   │  /health → 200    cat /health       3306 → 연결 성공    │   │   │  │
│   │   │   └─────────────────────────────────────────────────────────┘   │   │  │
│   │   │                               │                                  │   │  │
│   │   │                               ▼                                  │   │  │
│   │   │   ┌─────────────────────────────────────────────────────────┐   │   │  │
│   │   │   │                    Probe Result                          │   │   │  │
│   │   │   │                                                         │   │   │  │
│   │   │   │   Success ──▶ 계속 실행 / Endpoints 포함                 │   │   │  │
│   │   │   │   Failure ──▶ 재시도 카운트 증가                         │   │   │  │
│   │   │   │   failureThreshold 초과 ──▶ 조치 실행                    │   │   │  │
│   │   │   │     - Liveness: 컨테이너 재시작                           │   │   │  │
│   │   │   │     - Readiness: Endpoints에서 제외                       │   │   │  │
│   │   │   │     - Startup: 컨테이너 재시작                            │   │   │  │
│   │   │   └─────────────────────────────────────────────────────────┘   │   │  │
│   │   └─────────────────────────────────────────────────────────────────┘   │  │
│   └─────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

#### ① 파드 종료 (Termination) 상세 프로세스

```
파드 종료 7단계 프로세스:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: 사용자가 kubectl delete pod 명령 실행
        │
        │  API Server에 DELETE 요청 전송
        │  파드 metadata.deletionTimestamp 설정
        │  파드 상태: "Terminating" (GracePeriod 시작)
        │
        ▼
Step 2: Endpoint Controller가 파드 제거 감지
        │
        │  모든 Service의 Endpoints에서 해당 파드 IP 제거
        │  → 새로운 트래픽이 이 파드로 라우팅되지 않음
        │  → 단, 기존 연결은 여전히 유지됨
        │
        ▼
Step 3: PreStop Hook 실행 (정의된 경우)
        │
        │  예: nginx -s quit (우아한 종료)
        │      또는 사용자 정의 스크립트
        │
        │  lifecycle:
        │    preStop:
        │      exec:
        │        command: ["/bin/sh", "-c", "nginx -s quit"]
        │
        ▼
Step 4: SIGTERM 신호를 컨테이너에 전송
        │
        │  PID 1 프로세스에 SIGTERM (Signal 15) 전송
        │  애플리케이션은 이 신호를 catch하여 정리 작업 수행
        │  - DB 연결 종료
        │  - 진행 중인 요청 완료 대기
        │  - 임시 파일 정리
        │
        ▼
Step 5: Grace Period 대기 (기본 30초)
        │
        │  terminationGracePeriodSeconds 동안 대기
        │  컨테이너가 자발적으로 종료하기를 기다림
        │
        │  컨테이너가 종료되면 바로 Step 7로 이동
        │
        ▼
Step 6: Grace Period 초과 시 SIGKILL 전송
        │
        │  SIGKILL (Signal 9) - 강제 종료
        │  애플리케이션이 반응하지 않을 때 최후 수단
        │  데이터 손실 가능성 존재
        │
        ▼
Step 7: 파드 객체 삭제
        │
        │  API Server에서 파드 리소스 제거
        │  관련 이벤트 기록 종료
        │

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### ② 프로브 설정 및 동작 코드 예시

```yaml
# 완전한 파드 프로브 설정 예시
apiVersion: v1
kind: Pod
metadata:
  name: web-app
  labels:
    app: web
spec:
  containers:
  - name: web
    image: nginx:1.25
    ports:
    - containerPort: 80

    # ============================================
    # Startup Probe - 시작 완료 확인
    # (느린 시작 앱을 위한 보호막)
    # ============================================
    startupProbe:
      httpGet:
        path: /health/startup
        port: 80
      initialDelaySeconds: 0   # 즉시 시작
      periodSeconds: 5         # 5초마다 체크
      timeoutSeconds: 3        # 3초 타임아웃
      successThreshold: 1      # 1회 성공으로 완료
      failureThreshold: 30     # 30회 실패 = 150초 후 재시작

    # ============================================
    # Liveness Probe - 생존 확인
    # (데드락, 무한 루프 감지)
    # ============================================
    livenessProbe:
      httpGet:
        path: /health/live
        port: 80
        httpHeaders:
        - name: X-Health-Check
          value: "kubelet"
      initialDelaySeconds: 15  # startupProbe 완료 후 적용
      periodSeconds: 10        # 10초마다 체크
      timeoutSeconds: 5        # 5초 타임아웃
      successThreshold: 1      # 항상 1
      failureThreshold: 3      # 3회 연속 실패 시 재시작

    # ============================================
    # Readiness Probe - 트래픽 준비 확인
    # (DB 연결, 캐시 워밍업 완료)
    # ============================================
    readinessProbe:
      httpGet:
        path: /health/ready
        port: 80
        scheme: HTTP
      initialDelaySeconds: 5   # startupProbe 완료 후 적용
      periodSeconds: 5         # 5초마다 체크
      timeoutSeconds: 3        # 3초 타임아웃
      successThreshold: 2      # 2회 연속 성공해야 Ready
      failureThreshold: 1      # 1회 실패로 Not Ready

    # ============================================
    # Lifecycle Hooks
    # ============================================
    lifecycle:
      preStop:
        exec:
          command:
          - /bin/sh
          - -c
          - |
            # 우아한 종료: 진행 중인 요청 완료 대기
            nginx -s quit
            sleep 10

    # ============================================
    # Graceful Shutdown 설정
    # ============================================
    terminationGracePeriodSeconds: 60  # 기본 30초 → 60초로 연장

---
# Go 애플리케이션에서의 Graceful Shutdown 구현 예시
```

```go
// Graceful Shutdown 구현 (Go)
package main

import (
    "context"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"
    "log"
)

func main() {
    // HTTP 서버 생성
    server := &http.Server{
        Addr:    ":8080",
        Handler: newHandler(),
    }

    // 서버를 고루틴으로 시작
    go func() {
        log.Println("서버 시작: :8080")
        if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("서버 오류: %v", err)
        }
    }()

    // ============================================
    // Graceful Shutdown 핸들러
    // ============================================
    quit := make(chan os.Signal, 1)
    // SIGINT (Ctrl+C), SIGTERM (K8s 종료 신호) 감지
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

    // 신호 대기
    sig := <-quit
    log.Printf("종료 신호 수신: %v", sig)

    // Graceful Shutdown 컨텍스트 (최대 30초 대기)
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    // 1. 새 요청 거부
    // 2. 진행 중인 요청 완료 대기
    // 3. DB 연결 정리
    // 4. 캐시 플러시

    if err := server.Shutdown(ctx); err != nil {
        log.Printf("강제 종료: %v", err)
        server.Close()
    }

    log.Println("서버 정상 종료")
}

// 헬스체크 핸들러
func newHandler() http.Handler {
    mux := http.NewServeMux()

    // Liveness: 프로세스 생존 확인
    mux.HandleFunc("/health/live", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("alive"))
    })

    // Readiness: 서비스 준비 확인
    var isReady atomic.Bool
    mux.HandleFunc("/health/ready", func(w http.ResponseWriter, r *http.Request) {
        if !isReady.Load() {
            w.WriteHeader(http.StatusServiceUnavailable)
            return
        }
        // DB 연결 확인
        if err := checkDBConnection(); err != nil {
            w.WriteHeader(http.StatusServiceUnavailable)
            return
        }
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("ready"))
    })

    // Startup: 시작 완료 확인
    mux.HandleFunc("/health/startup", func(w http.ResponseWriter, r *http.Request) {
        // 초기화 로직 확인
        if !isInitialized() {
            w.WriteHeader(http.StatusServiceUnavailable)
            return
        }
        isReady.Store(true) // Ready 상태로 전환
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("started"))
    })

    return mux
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 프로브 유형별 특성

| 프로브 유형 | 목적 | 실패 시 동작 | 타이밍 | 권장 설정 |
|------------|------|-------------|--------|----------|
| **Startup** | 앱 시작 완료 확인 | 컨테이너 재시작 | Liveness/Readiness 이전에만 실행 | 느린 앱 (30-300초) |
| **Liveness** | 런타임 데드락/고장 감지 | 컨테이너 재시작 | Startup 완료 후 계속 실행 | period: 10-30s |
| **Readiness** | 트래픽 수신 준비 확인 | Endpoints에서 제외 | Startup 완료 후 계속 실행 | period: 5-10s |

### 프로브 실패 시나리오 분석

| 시나리오 | Liveness | Readiness | Startup | 최종 결과 |
|---------|----------|-----------|---------|----------|
| DB 연결 끊김 | 성공 (앱 살아있음) | 실패 (서비스 불가) | N/A | 트래픽 차단, 재시작 없음 |
| 메모리 누수로 데드락 | 실패 (응답 없음) | 실패 | N/A | 컨테이너 재시작 |
| 앱 시작 지연 (30초+) | N/A | N/A | 실패 후 성공 | 정상 시작 (Liveness 보호) |
| 잘못된 이미지 | N/A | N/A | 실패 | ImagePullBackOff |

### 과목 융합 관점 분석

#### [쿠버네티스 + 네트워크] 서비스와 Readiness 연동
```
Readiness Probe와 Service Endpoints 연동:

1. Readiness Probe 성공
   - kubelet이 API Server에 "Ready" 상태 보고
   - Endpoint Controller가 Service Endpoints에 파드 IP 추가
   - kube-proxy가 iptables/IPVS 규칙 업데이트
   - 새 트래픽이 해당 파드로 라우팅 시작

2. Readiness Probe 실패
   - kubelet이 "Not Ready" 상태 보고
   - Endpoint Controller가 Endpoints에서 파드 IP 제거
   - 기존 연결은 유지됨 (Connection Drain 필요)
   - 새 트래픽은 다른 Ready 파드로만 라우팅

3. Rolling Update와의 연동
   deployment.yaml:
   spec:
     replicas: 3
     strategy:
       type: RollingUpdate
       rollingUpdate:
         maxSurge: 1          # 최대 4개까지 추가 가능
         maxUnavailable: 0    # 사용 불가 파드 0개 (무중단)

   배포 순서:
   1. 새 파드 생성 → Pending → ContainerCreating
   2. Startup Probe 성공 → Readiness Probe 시작
   3. Readiness Probe 성공 → Endpoints 추가 → 트래픽 유입
   4. 이전 파드 SIGTERM → Graceful Shutdown
   5. 이전 파드 Endpoints 제거 → 새 파드만 트래픽
```

#### [쿠버네티스 + 운영체제] 컨테이너 재시작과 메모리
```
컨테이너 재시작 메커니즘 (OS 관점):

1. Liveness Probe 실패 감지
   - kubelet이 exec/httpGet/tcpSocket으로 실패 threshold 초과

2. 컨테이너 정지
   - container runtime (containerd)에 Stop 요청
   - SIGTERM 전송 → Grace Period 대기 → SIGKILL

3. cgroup 정리
   - /sys/fs/cgroup/memory/kubepods/.../memory.force_empty
   - 메모리 사용량 0으로 초기화

4. 컨테이너 재생성
   - 동일 이미지로 새 컨테이너 생성
   - 새 cgroup, 새 네트워크 네임스페이스
   - PID 1로 새 프로세스 시작

5. 재시작 정책에 따른 처리
   - Always: 항상 재시작 (Deployment 기본)
   - OnFailure: 실패(exit != 0) 시만 재시작
   - Never: 재시작 안 함 (Job/CronJob)

재시작 Backoff:
- 1회 실패: 즉시 재시작
- 2회 실패: 10초 후 재시작
- 3회 실패: 20초 후
- 4회 실패: 40초 후
- 5회 실패: 80초 후 (최대 5분)
- 상태: CrashLoopBackOff
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 시나리오

#### 시나리오 1: 무거운 Java 애플리케이션 배포
```
현황:
- Spring Boot 애플리케이션
- 시작 시간: 60-120초 (Hibernate, 캐시 워밍업)
- Liveness Probe가 시작 중에 실패하여 반복 재시작

기술사 판단:
1. 문제 진단:
   - initialDelaySeconds만으로는 부족
   - Liveness Probe가 앱 시작 전에 실행되어 실패

2. 해결 방안: Startup Probe 도입
   spec:
     containers:
     - name: app
       # Startup Probe: 120초까지 시작 허용
       startupProbe:
         httpGet:
           path: /actuator/health
           port: 8080
         periodSeconds: 5
         failureThreshold: 24  # 5s * 24 = 120초
       # Liveness Probe: Startup 완료 후 실행
       livenessProbe:
         httpGet:
           path: /actuator/health/liveness
           port: 8080
         periodSeconds: 15
         failureThreshold: 3
       # Readiness Probe: DB 연결 확인
       readinessProbe:
         httpGet:
           path: /actuator/health/readiness
           port: 8080
         periodSeconds: 5
         failureThreshold: 1

3. 추가 최적화:
   - Spring Boot Actuator 활성화
   - JVM -XX:+UseContainerSupport
   - Init Container로 DB 마이그레이션 분리
```

#### 시나리오 2: DB 연결 장애 시 서비스 동작
```
요구사항:
- DB 장애 시 앱 크래시 대신 에러 페이지 표시
- 장애 복구 후 자동으로 정상 서비스 재개

기술사 판단:
1. Liveness vs Readiness 구분:
   - Liveness: 앱 프로세스는 살아있음 → Success
   - Readiness: DB 연결 불가 → Failure (트래픽 차단)

2. 구현:
   @app.route('/health/live')
   def liveness():
       # 프로세스 생존만 확인
       return {'status': 'alive'}

   @app.route('/health/ready')
   def readiness():
       # DB 연결 확인
       try:
           db.ping()
           return {'status': 'ready'}, 200
       except:
           return {'status': 'not ready'}, 503

3. 동작:
   - DB 장애 발생 → Readiness 실패
   - Endpoints에서 제거 → 새 트래픽 차단
   - 앱은 실행 유지 (Liveness 성공)
   - DB 복구 → Readiness 성공 → 트래픽 재개

4. 추가 고려:
   - Fallback 응답: 서킷 브레이커로 캐시된 데이터 반환
   - Graceful Degradation: 기능 축소 모드
```

### 도입 시 고려사항 체크리스트

#### 기술적 고려사항
- [ ] **프로브 엔드포인트 분리**: /live, /ready, /startup 별도 구현
- [ ] **타임아웃 설정**: 앱 응답 시간 고려 (P99 + 여유)
- [ ] **초기 지연**: 앱 시작 시간 측정 후 설정
- [ ] **실패 임계값**: 너무 낮으면 과잉 재시작, 높으면 장애 감지 지연
- [ ] **Grace Period**: 종료 시 정리 작업 시간 확보

#### 운영적 고려사항
- [ ] **헬스체크 로깅**: 프로브 요청 로그 별도 처리
- [ ] **메트릭 수집**: 프로브 성공/실패율 모니터링
- [ ] **알림 정책**: 연속 실패 시 알림
- [ ] **문서화**: 각 엔드포인트의 의미와 의존성 명시

### 주의사항 및 안티패턴

#### 안티패턴 1: Liveness에 무거운 로직 포함
```
잘못된 접근:
livenessProbe:
  httpGet:
    path: /api/complex-health-check  # DB 쿼리, 외부 API 호출
    port: 8080
  periodSeconds: 5

문제:
- DB 부하 증가 (매 5초마다 전체 체크)
- 외부 API 지연 시 컨테이너 재시작
- 과잉 재시작으로 서비스 불안정

올바른 접근:
livenessProbe:
  httpGet:
    path: /health/live  # 단순 프로세스 생존 확인
    port: 8080
readinessProbe:
  httpGet:
    path: /health/ready  # DB, 캐시 의존성 확인
    port: 8080
```

#### 안티패턴 2: Grace Period 없이 강제 종료
```
잘못된 접근:
spec:
  terminationGracePeriodSeconds: 0  # 즉시 종료

문제:
- 진행 중인 요청 강제 중단
- DB 트랜잭션 미완료
- 데이터 일관성 깨짐

올바른 접근:
spec:
  terminationGracePeriodSeconds: 60  # 충분한 정리 시간
  containers:
  - lifecycle:
      preStop:
        exec:
          command: ["sleep", "15"]  # Service에서 제거 후 대기
```

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 구분 | 프로브 미설정 | 프로브 적절 설정 | 개선효과 |
|-----------|-------------|-----------------|---------|
| 장애 감지 시간 | 수동 확인 (수십 분) | 자동 (30초 내) | -95% |
| 무중단 배포 성공률 | 80% (트래픽 유실) | 99.9% | +25% |
| 데드락 복구 시간 | 무한 대기 | 30초 내 재시작 | MTTR 99% 단축 |
| 가용성 (SLA) | 99% | 99.9% | +0.9% (연 8시간 → 52분) |
| 운영 인력 개입 | 빈번 | 드묾 | 인력 80% 절감 |

### 미래 전망 및 진화 방향

#### 1. Sidecar 컨테이너 생명주기 개선
- v1.28+: Sidecar Containers (Native Sidecar)
- 메인 컨테이너 전후 실행 순서 보장
- 로깅/메트릭 사이드카의 우아한 종료

#### 2. 커스텀 프로브
- gRPC Health Checking Protocol
- 사용자 정의 프로브 타입 확장

#### 3. AI 기반 장애 예측
- 프로브 패턴 분석으로 선제적 재시작
- 이상 징후 감지 → 자동 스케일링

### 참고 표준/가이드
- **Kubernetes Docs**: Configuring Liveness, Readiness and Startup Probes
- **KEP-2034**: Kubelet Graceful Node Shutdown
- **KEP-753**: Sidecar Containers

---

## 관련 개념 맵 (Knowledge Graph)

1. [쿠버네티스 (Kubernetes)](./kubernetes.md)
   - 관계: 파드 생명주기는 K8s의 핵심 관리 대상

2. [디플로이먼트 (Deployment)](./replicaset_deployment.md)
   - 관계: Rolling Update 시 프로브로 무중단 달성

3. [서비스 (Service)](./k8s_networking.md)
   - 관계: Readiness Probe 결과로 Endpoints 관리

4. [서킷 브레이커 (Circuit Breaker)](./circuit_breaker.md)
   - 관계: 애플리케이션 레벨 회복 탄력성

5. [옵저버빌리티 (Observability)](./observability.md)
   - 관계: 프로브 상태 모니터링 및 알림

6. [HPA (Horizontal Pod Autoscaler)](./hpa_vpa_ca.md)
   - 관계: Readiness 기반 스케일링 결정

---

## 어린이를 위한 3줄 비유 설명

**비유: 환자의 병원 치료**

파드는 병원에 입원한 환자 같아요. 의사 선생님(kubelet)이 환자가 살아있는지(Liveness), 면회 가능한지(Readiness), 중환자실에서 일반 병실로 갈 준비가 됐는지(Startup)를 정기적으로 확인해요.

**원리:**
환자가 갑자기 위독해지면(Liveness 실패) 의사가 응급 조치(재시작)를 해요. 환자가 치료 중이라 면회가 안 되면(Readiness 실패) 면회객(트래픽)이 다른 환자에게만 가요. 퇴원할 때는 유언장(PreStop Hook)을 쓸 시간을 줘요.

**효과:**
이렇게 하면 병원(서비스)이 항상 정상적으로 돌아가요. 환자가 아파도 빨리 치료받고, 면회객은 면회 가능한 환자에게만 갈 수 있어서 병원이 엉망이 되지 않아요!
