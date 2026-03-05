+++
title = "폐기 가능성 (Disposability) - 12-Factor App"
description = "클라우드 네이티브 환경에서 빠른 시작과 우아한 종료를 통한 탄력적 확장과 무중단 배포를 실현하는 설계 원칙"
date = 2024-05-15
[taxonomies]
tags = ["Disposability", "12-Factor App", "Graceful Shutdown", "Fast Startup", "Kubernetes", "Cloud Native"]
+++

# 폐기 가능성 (Disposability) - 12-Factor App 원칙

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 12-Factor App의 제9 원칙으로, **애플리케이션 프로세스가 언제든지 안전하게 시작(Startup)되고 종료(Shutdown)될 수 있도록 설계**하여, 컨테이너 오케스트레이션 환경에서 탄력적 확장, 무중단 배포, 장애 복구를 자연스럽게 지원하는 설계 원칙입니다.
> 2. **가치**: 폐기 가능성을 통해 **초 단위의 빠른 시작**으로 오토스케일링에 즉각 대응하고, **우아한 종료(Graceful Shutdown)**로 진행 중인 요청을 안전하게 완료하여 사용자에게 장애를 전파하지 않으며, **롤링 업데이트 시 무중단 서비스**를 보장합니다.
> 3. **융합**: 쿠버네티스의 Readiness/Liveness Probe, SIGTERM 시그널 처리, PreStop Hook, 서킷 브레이커, 로드밸런서 헬스 체크와 결합하여 엔터프라이즈급 무중단 아키텍처를 구현합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)

**폐기 가능성(Disposability)**이란 애플리케이션 프로세스가 **일회용(Disposable)**으로 설계되어, 언제든지 **즉시 시작**하고 **안전하게 종료**할 수 있는 능력을 의미합니다. 여기에는 두 가지 핵심 개념이 포함됩니다:

| 개념 | 설명 | 목표 시간 |
| :--- | :--- | :--- |
| **Fast Startup (빠른 시작)** | 프로세스가 실행 요청 후 서비스 가능 상태가 되는 시간 | 수십 초 이내 |
| **Graceful Shutdown (우아한 종료)** | 종료 신호 수신 후 진행 중인 작업을 완료하고 안전하게 종료 | 수십 초 이내 |

12-Factor App의 원칙:
> "Maximize robustness with fast startup and graceful shutdown."

**폐기 가능성이 중요한 이유**:
- **오토스케일링**: 트래픽 증가 시 즉시 새 인스턴스 필요
- **롤링 업데이트**: 새 버전 배포 시 기존 인스턴스 안전 종료
- **장애 복구**: 실패한 인스턴스를 즉시 교체
- **비용 최적화**: 트래픽 감소 시 즉시 인스턴스 종료

### 2. 구체적인 일상생활 비유

**택시 기사**를 상상해 보세요:

**[폐기 불가능한 기사 (전통적 서버)]**
- 출근 준비에 30분 걸려요 (서버 부팅, 초기화)
- 손님을 태우고 가다가 교통사고가 나면 **손님이 다치는 것**과 같아요 (강제 종료)
- 퇴근하려면 **오늘 모든 손님을 다 태워야** 해요 (장기 실행 작업)

**[폐기 가능한 기사 (12-Factor 앱)]**
- **1분 만에 출근 준비** 완료해요 (Fast Startup)
- 교통사고가 나면 **현재 손님만 안전하게 내려주고** 퇴근해요 (Graceful Shutdown)
- 대기 택시가 많아서 **언제든 다른 기사로 교체** 가능해요

### 3. 등장 배경 및 발전 과정

1. **기존 기술의 치명적 한계점 (장기 실행 서버)**:
   과거에는 서버가 몇 달, 몇 년씩 실행되는 것이 정상이었습니다:
   ```
   - 서버 부팅 시간: 5~10분
   - 애플리케이션 초기화: 2~5분
   - 메모리 누수 해결: 재시작 (수십 초~수분)
   ```
   이 방식의 문제:
   - **배포 다운타임**: 서버 재시작 동안 서비스 중단
   - **확장 지연**: 트래픽 급증 시 대응 불가
   - **자원 낭비**: 유휴 서버를 계속 실행

2. **혁신적 패러다임 변화의 시작**:
   컨테이너와 오케스트레이션의 등장으로:
   - 컨테이너는 **초 단위**로 시작/종료
   - 쿠버네티스는 **파드를 언제든 교체** 가능
   - 롤링 업데이트가 **무중단**으로 수행

3. **현재 시장/산업의 비즈니스적 요구사항**:
   - **무중단 서비스**: 99.99% 가용성 요구
   - **빠른 배포**: 하루 수십 번 배포
   - **탄력적 확장**: 트래픽 패턴에 따른 자동 스케일링
   - 이 모든 것이 **폐기 가능성**이 전제되어야 가능

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Fast Startup** | 빠른 서비스 가능 상태 도달 | Lazy Loading, AOT 컴파일, 최소 초기화 | Spring Boot, Quarkus | 1분 만에 출근 준비 |
| **Graceful Shutdown** | 안전한 종료 처리 | SIGTERM 수신, 요청 완료 대기, 리소스 정리 | Shutdown Hook, PreStop | 손님 안전하게 내려주기 |
| **Health Probe** | 서비스 준비 상태 확인 | HTTP 엔드포인트로 상태 보고 | Kubernetes Probes | "준비 완료!" 신호 |
| **Signal Handler** | OS 시그널 처리 | SIGTERM, SIGINT, SIGKILL 처리 | POSIX Signals | 관리자의 호출 신호 |
| **Connection Draining** | 연결 점진적 종료 | 새 요청 거부, 기존 요청 완료 대기 | LB Deregistration | 예약 손님만 마저 태우기 |

### 2. 정교한 구조 다이어그램: Disposability Lifecycle

```text
=====================================================================================================
                    [ 12-Factor Disposability Lifecycle ]
=====================================================================================================

    +-------------------------------------------------------------------------------------------+
    |                              [ PROCESS LIFECYCLE ]                                         |
    |                                                                                           |
    |   [STARTUP PHASE]                           [SHUTDOWN PHASE]                             |
    |                                                                                           |
    |   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          |
    |   │  Init    │───>│  Ready   │    │ Running  │───>│Stopping  │───>│ Stopped  │          |
    |   │          │    │  Check   │    │          │    │          │    │          │          |
    |   └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘          |
    |        │               │               │               │               │                 |
    │        ▼               ▼               ▼               ▼               ▼                 |
    |   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          |
    │   │ - Config │    │ Liveness │    │ Serving  │    │ SIGTERM  │    │ Clean    │          |
    │   │   Load   │    │ Probe OK │    │ Traffic  │    │ Received │    │ Exit     │          |
    │   │ - DI     │    │          │    │          │    │          │    │ (0)      │          |
    │   │ - DB Conn│    │Readiness │    │          │    │-Drain LB │    │          │          |
    │   │ - Cache  │    │ Probe OK │    │          │    │-Complete │    │          │          |
    │   │          │    │          │    │          │    │ Requests │    │          │          |
    │   └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘          |
    |                                                                                           |
    +-------------------------------------------------------------------------------------------+

    =====================================================================================================
                    [ KUBERNETES GRACEFUL SHUTDOWN SEQUENCE ]
    =====================================================================================================

    Timeline: Pod Termination Process

    T=0s     ┌─────────────────────────────────────────────────────────────────────────────┐
             │ K8s API: DELETE /api/v1/namespaces/default/pods/myapp-xyz123              │
             └─────────────────────────────────────────────────────────────────────────────┘
                                    │
    T=0s                           ▼
             ┌─────────────────────────────────────────────────────────────────────────────┐
             │ 1. Pod status -> "Terminating"                                              │
             │ 2. Service/Ingress: Remove Pod from endpoints (New traffic stops)           │
             │ 3. PreStop Hook: Execute if defined (e.g., sleep 10)                        │
             └─────────────────────────────────────────────────────────────────────────────┘
                                    │
    T=10s (default)                ▼
             ┌─────────────────────────────────────────────────────────────────────────────┐
             │ 4. SIGTERM sent to container PID 1                                          │
             │    - Application receives signal                                            │
             │    - Stop accepting new requests (Readiness Probe fails)                    │
             │    - Complete in-flight requests                                            │
             │    - Close DB connections, flush buffers                                    │
             └─────────────────────────────────────────────────────────────────────────────┘
                                    │
    T=10s - 60s                    ▼
             ┌─────────────────────────────────────────────────────────────────────────────┐
             │ 5. Graceful Shutdown Period (default: 30s)                                  │
             │    - Application processes remaining requests                               │
             │    - Max: terminationGracePeriodSeconds (default: 30s)                      │
             └─────────────────────────────────────────────────────────────────────────────┘
                                    │
    T=40s (30s + 10s)              ▼
             ┌─────────────────────────────────────────────────────────────────────────────┐
             │ 6. If still running: SIGKILL (Force kill)                                   │
             │ 7. Pod removed from API server                                              │
             └─────────────────────────────────────────────────────────────────────────────┘

    =====================================================================================================
```

### 3. 심층 동작 원리: Graceful Shutdown 구현

**1단계: Spring Boot Graceful Shutdown 설정**

```yaml
# application.yml - Graceful Shutdown 설정
server:
  shutdown: graceful  # Graceful shutdown 활성화

spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s  # 최대 종료 대기 시간

management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  endpoint:
    health:
      probes:
        enabled: true  # Kubernetes Probes 활성화
```

```java
// Spring Boot Graceful Shutdown Hook
@Component
public class GracefulShutdownHandler {

    private static final Logger log = LoggerFactory.getLogger(GracefulShutdownHandler.class);

    @PreDestroy
    public void onShutdown() {
        log.info("Graceful shutdown initiated...");

        // 1. 새 요청 거부 (Readiness Probe가 실패하도록 설정)
        // Spring Boot가 자동 처리

        // 2. 진행 중인 요청 완료 대기
        // Spring Boot가 자동 처리 (server.shutdown=graceful)

        // 3. 리소스 정리
        cleanupResources();

        log.info("Graceful shutdown completed");
    }

    private void cleanupResources() {
        // DB 연결 풀 종료
        // 캐시 플러시
        // 파일 핸들 닫기
        // 스레드 풀 종료
    }
}
```

**2단계: Kubernetes Probes 설정**

```yaml
# Kubernetes Deployment with Probes
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  template:
    spec:
      terminationGracePeriodSeconds: 60  # Graceful shutdown 최대 시간

      # PreStop Hook: SIGTERM 전에 실행
      lifecycle:
        preStop:
          exec:
            command: ["/bin/sh", "-c", "sleep 15"]  # LB 전파 대기

      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 8080

        # Liveness Probe: 프로세스가 살아있는지 확인
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          failureThreshold: 3

        # Readiness Probe: 트래픽을 받을 준비가 되었는지 확인
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          failureThreshold: 3

        env:
        - name: GRACEFUL_SHUTDOWN_TIMEOUT
          value: "30s"
```

**3단계: 커스텀 Signal Handler (Java)**

```java
// JVM Shutdown Hook 등록
@Component
public class ShutdownHookConfig {

    @Autowired
    private ApplicationContext applicationContext;

    @PostConstruct
    public void registerShutdownHook() {
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("SIGTERM received, initiating graceful shutdown...");

            // 1. 새 요청 거부 플래그 설정
            ApplicationState.setAcceptingNewRequests(false);

            // 2. 진행 중인 요청 완료 대기
            try {
                int activeRequests = RequestCounter.getActiveCount();
                int maxWaitSeconds = 30;

                for (int i = 0; i < maxWaitSeconds && activeRequests > 0; i++) {
                    System.out.println("Waiting for " + activeRequests + " active requests...");
                    Thread.sleep(1000);
                    activeRequests = RequestCounter.getActiveCount();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }

            // 3. 리소스 정리
            cleanupResources();

            System.out.println("Graceful shutdown completed.");
        }));
    }
}
```

**4단계: Node.js Graceful Shutdown**

```javascript
// Node.js Graceful Shutdown
const express = require('express');
const app = express();

let isShuttingDown = false;
let activeConnections = 0;

// 요청 카운터 미들웨어
app.use((req, res, next) => {
    if (isShuttingDown) {
        // 새 요청 거부 (503 Service Unavailable)
        res.status(503).json({ error: 'Server is shutting down' });
        return;
    }

    activeConnections++;
    res.on('finish', () => {
        activeConnections--;
    });
    next();
});

app.get('/', (req, res) => {
    res.json({ message: 'Hello World' });
});

const server = app.listen(8080, () => {
    console.log('Server started on port 8080');
});

// Graceful Shutdown 함수
async function gracefulShutdown(signal) {
    console.log(`\n${signal} received. Starting graceful shutdown...`);

    isShuttingDown = true;

    // 1. 새 연결 거부
    server.close(() => {
        console.log('HTTP server closed');
    });

    // 2. 기존 연결 완료 대기
    const maxWaitMs = 30000;
    const startTime = Date.now();

    while (activeConnections > 0 && (Date.now() - startTime) < maxWaitMs) {
        console.log(`Waiting for ${activeConnections} active connections...`);
        await new Promise(resolve => setTimeout(resolve, 1000));
    }

    // 3. 리소스 정리
    await closeDatabaseConnections();
    await flushCache();

    console.log('Graceful shutdown complete');
    process.exit(0);
}

// 시그널 핸들러 등록
process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

async function closeDatabaseConnections() {
    // DB 연결 종료 로직
}

async function flushCache() {
    // 캐시 플러시 로직
}
```

### 4. 실무 코드 예시: Fast Startup 최적화

```java
// Spring Boot Fast Startup 최적화

// 1. Lazy Initialization (지연 초기화)
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        // 지연 초기화 활성화
        SpringApplication app = new SpringApplication(Application.class);
        app.setLazyInitialization(true);  // 필요할 때만 Bean 초기화
        app.run(args);
    }
}

// 2. AOT (Ahead-of-Time) 컴파일 - Spring Boot 3.x
// GraalVM Native Image로 컴파일하면 밀리초 단위 시작

// 3. 불필요한 자동 설정 제외
@SpringBootApplication(exclude = {
    DataSourceAutoConfiguration.class,  // DB 사용 안 하면 제외
    HibernateJpaAutoConfiguration.class
})
public class Application { ... }

// 4. 최소한의 초기화만 수행
@Component
public class MinimalStartup {

    @PostConstruct
    public void init() {
        // 필수 초기화만 수행
        // 무거운 작업은 @Lazy로 지연
    }

    @Lazy
    @Bean
    public HeavyService heavyService() {
        // 실제 사용 시점에 초기화
        return new HeavyService();
    }
}
```

```yaml
# application.yml - 시작 시간 최적화
spring:
  main:
    lazy-initialization: true  # 지연 초기화
    log-startup-info: false    # 시작 로그 최소화
    banner-mode: off           # 배너 비활성화

  jmx:
    enabled: false  # JMX 비활성화 (시작 시간 단축)

management:
  metrics:
    enable:
      jvm: false  # 불필요한 메트릭 비활성화
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 종료 방식 비교표

| 종료 방식 | 설명 | 요청 처리 | 데이터 손실 | 적합한 상황 |
| :--- | :--- | :--- | :--- | :--- |
| **Kill -9 (SIGKILL)** | 즉시 강제 종료 | 즉시 중단 | 발생 가능 | 긴급 복구 |
| **Kill (SIGTERM)** | 정상 종료 요청 | 완료 대기 | 최소화 | 일반적 종료 |
| **Graceful Shutdown** | 안전한 종료 | 완료 보장 | 없음 | 프로덕션 |
| **Rolling Restart** | 순차적 재시작 | 무중단 | 없음 | 배포/업데이트 |

### 2. Startup 전략 비교

| 전략 | 시작 시간 | 장점 | 단점 | 적합한 상황 |
| :--- | :--- | :--- | :--- | :--- |
| **Eager Loading** | 느림 (수십 초) | 초기화 완료 | 시작 느림 | 초기화 중요 |
| **Lazy Loading** | 빠름 (수 초) | 빠른 시작 | 첫 요청 느림 | 오토스케일링 |
| **AOT/Native** | 매우 빠름 (수십 ms) | 즉시 사용 | 빌드 복잡 | 서버리스 |
| **Warm Pool** | 즉시 | 미리 준비 | 자원 낭비 | 응답성 중요 |

### 3. 과목 융합 관점 분석

**Disposability + 로드밸런서**
- 헬스 체크 실패 시 트래픽 차단
- Connection Draining으로 진행 중인 요청 완료
- Deregistration Delay로 전파 시간 확보

**Disposability + 서비스 메시 (Istio)**
- Istio Proxy가 트래픽을 우회
- Envoy의 Drain 시간 설정
- PreStop Hook과 협력

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 긴 트랜잭션의 Graceful Shutdown**
- **문제점**: 파일 업로드가 5분 걸리는데, 배포 시 30초 내에 종료해야 함.
- **기술사 판단**: **비동기 처리 + 체크포인트**
  1. 업로드를 S3 Presigned URL로 클라이언트 직접 업로드
  2. 서버는 완료 이벤트만 처리 (빠른 처리)
  3. 긴 작업은 메시지 큐로 워커에서 수행
  4. 필요시 체크포인트로 재개 가능

**[상황 B] DB 연결 풀의 안전한 종료**
- **문제점**: 종료 시 DB 연결이 남아 있어 DB 서버 부하.
- **기술사 판단**: **종료 훅에서 명시적 연결 종료**
  ```java
  @PreDestroy
  public void cleanup() {
      // 연결 풀에서 모든 연결 반환
      dataSource.close();
      // 진행 중인 트랜잭션 롤백
      transactionManager.rollback();
  }
  ```

### 2. 도입 시 고려사항 체크리스트

**Graceful Shutdown 체크리스트**
- [ ] SIGTERM 시그널을 처리하는가?
- [ ] 진행 중인 요청의 완료를 대기하는가?
- [ ] 새 요청을 거부하는가? (Readiness Probe 실패)
- [ ] DB 연결, 파일 핸들 등을 정리하는가?
- [ ] 종료 타임아웃이 적절한가? (K8s terminationGracePeriodSeconds)

**Fast Startup 체크리스트**
- [ ] 시작 시간이 30초 이내인가?
- [ ] 지연 초기화(Lazy Init)를 활용하는가?
- [ ] 불필요한 자동 설정을 제외했는가?
- [ ] Readiness Probe가 준비되면 바로 트래픽을 받는가?

### 3. 주의사항 및 안티패턴

**안티패턴 1: 종료 훅 없는 강제 종료**
```java
// 잘못된 예: 종료 시 정리 없음
System.exit(0);  // 즉시 종료, 요청 손실

// 올바른 예: Graceful Shutdown
applicationContext.close();  // Spring의 정리 로직 실행
```

**안티패턴 2: 무한 대기**
```java
// 잘못된 예: 요청 완료를 영원히 기다림
while (activeRequests > 0) {
    Thread.sleep(1000);  // 무한 루프 가능
}

// 올바른 예: 타임아웃 설정
long deadline = System.currentTimeMillis() + 30000;
while (activeRequests > 0 && System.currentTimeMillis() < deadline) {
    Thread.sleep(1000);
}
```

**안티패턴 3: PreStop Hook 생략**
```yaml
# 잘못된 예: PreStop 없이 바로 SIGTERM
# LB가 아직 파드를 알고 있어 요청 손실 가능

# 올바른 예: PreStop으로 LB 전파 대기
lifecycle:
  preStop:
    exec:
      command: ["/bin/sh", "-c", "sleep 15"]
```

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 비폐기성 (AS-IS) | 폐기 가능성 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **시작 시간** | 2~5분 | 10~30초 | **90% 단축** |
| **종료 시 데이터 손실** | 발생 가능 | 없음 | **0건 손실** |
| **롤링 업데이트 다운타임** | 수십 초~수분 | 0초 | **무중단** |
| **오토스케일링 대응** | 수분 지연 | 즉시 | **실시간** |

### 2. 미래 전망 및 진화 방향

**GraalVM Native Image**
- 밀리초 단위 시작 시간
- 메모리 사용량 대폭 감소
- 서버리스(FaaS)에 최적화

**Service Mesh 통합**
- Envoy가 트래픽 관리
- 앱은 종료 로직에만 집중
- 더 단순한 애플리케이션 코드

### 3. 참고 표준/가이드
- **The Twelve-Factor App (12factor.net/disposability)**: Disposability 원칙
- **Kubernetes Pod Lifecycle**: terminationGracePeriodSeconds, Probes
- **Spring Boot Graceful Shutdown**: server.shutdown=graceful
- **SIGTERM/SIGKILL (POSIX)**: 유닉스 시그널 표준

---

## 관련 개념 맵 (Knowledge Graph)
- **[12-Factor App](@/studynotes/15_devops_sre/01_sre/twelve_factor_app.md)**: 폐기 가능성을 포함한 전체 방법론
- **[무상태 프로세스 (Stateless)](./stateless_processes.md)**: 폐기 가능성의 전제 조건
- **[롤링 배포](@/studynotes/15_devops_sre/03_automation/continuous_deployment.md)**: Graceful Shutdown을 활용한 무중단 배포
- **[오토스케일링](@/studynotes/13_cloud_architecture/01_native/kubernetes.md)**: Fast Startup이 필요한 이유
- **[헬스 체크](@/studynotes/15_devops_sre/02_observability/health_check.md)**: Readiness/Liveness Probe

---

## 어린이를 위한 3줄 비유 설명
1. 택시 기사가 **출근 준비를 1분 만에** 하고, **손님을 태운 채로 퇴근하지 않는** 것과 같아요.
2. 기사가 퇴근해야 하면 **현재 손님만 안전하게 내려주고** 퇴근해요. 새 손님은 안 태워요!
3. 이렇게 하면 **다른 기사가 바로 대신** 일할 수 있어요. 컴퓨터도 이렇게 **언제든 교체 가능하게** 만들어요!
