+++
title = "동시성 (Concurrency) - 12-Factor App"
description = "클라우드 네이티브 환경에서 프로세스 모델을 통한 수평적 확장(Scale-out)과 병렬 처리를 위한 설계 원칙 및 실무 적용 전략"
date = 2024-05-15
[taxonomies]
tags = ["Concurrency", "12-Factor App", "Horizontal Scaling", "Process Model", "Scale-out", "Kubernetes HPA"]
+++

# 동시성 (Concurrency) - 12-Factor App 원칙

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 12-Factor App의 제8 원칙으로, **단일 거대한 프로세스(Scale-up) 대신 다수의 독립적인 프로세스(Scale-out)를 통해 동시성을 구현**하고, 각 프로세스가 자체적으로 스케일 아웃 가능한 단위가 되는 설계 원칙입니다.
> 2. **가치**: 프로세스 모델을 통해 **트래픽 증가 시 인스턴스 수를 선형적으로 확장**하고, 장애 발생 시 **격리된 프로세스만 종료**하여 전체 시스템에 영향을 최소화하며, **다양한 워크로드 유형을 독립적으로 스케일링**할 수 있습니다.
> 3. **융합**: 쿠버네티스 HPA(Horizontal Pod Autoscaler), 메시지 큐(Kafka, RabbitMQ), 워커 풀 패턴, 서버리스(FaaS)와 결합하여 탄력적 클라우드 아키텍처를 구현합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)

**동시성(Concurrency)**이란 12-Factor App의 관점에서 **여러 독립적인 프로세스를 실행하여 병렬로 작업을 처리**하는 방식을 의미합니다. 이는 전통적인 **스레드 기반 Scale-up**과 대조됩니다:

| 확장 방식 | 접근법 | 장점 | 단점 |
| :--- | :--- | :--- | :--- |
| **Scale-up (수직)** | 더 큰 서버, 더 많은 스레드 | 단순한 아키텍처 | 하드웨어 한계, SPOF |
| **Scale-out (수평)** | 더 많은 프로세스/컨테이너 | 선형 확장, 고가용성 | 분산 시스템 복잡도 |

12-Factor App의 핵심 원칙:
> "Add concurrency by running more identical processes, not by increasing the complexity of the process internals."

**프로세스 모델의 핵심 개념**:
- **Web Process**: HTTP 요청을 처리하는 웹 서버 프로세스
- **Worker Process**: 백그라운드 작업(이메일 발송, 이미지 처리)을 처리하는 워커
- **Scheduled Process**: cron/스케줄러에 의해 실행되는 배치 작업
- 각 프로세스 유형은 **독립적으로 스케일링** 가능

### 2. 구체적인 일상생활 비유

**은행 창구 운영**을 상상해 보세요:

**[Scale-up 방식 - 스레드 모델]**
- 창구 직원 **한 명**이 **여러 손님**을 동시에 응대해요
- 손님 A의 서류 검토하면서, 손님 B의 질문에 답해요
- 직원이 아프면 **모든 업무 중단**

**[Scale-out 방식 - 프로세스 모델]**
- 창구 직원 **여러 명**이 **각각 한 명의 손님**을 전담해요
- 손님이 많으면 **직원을 더 투입**해요
- 한 직원이 아파도 **다른 직원이 업무 지속**

**12-Factor의 핵심**: 직원 한 명이 더 많은 일을 동시에 하려고 애쓰지 말고, **직원 수를 늘려라**!

### 3. 등장 배경 및 발전 과정

1. **기존 기술의 치명적 한계점 (Scale-up의 한계)**:
   과거에는 더 많은 트래픽을 처리하기 위해 **더 큰 서버**를 구매했습니다:
   ```
   [ Traffic Increase ] --> [ Bigger Server ] --> [ More Threads ]
   ```
   이 방식의 문제:
   - **하드웨어 한계**: CPU 코어, 메모리 증가에는 물리적 한계
   - **비용 기하급수적 증가**: 32코어 서버는 16코어 서버의 2배 이상 비용
   - **SPOF (Single Point of Failure)**: 서버 장애 시 전체 서비스 중단
   - **복잡한 동시성 제어**: 스레드 간 락(Lock), 데드락(Deadlock), 경쟁 조건(Race Condition)

2. **혁신적 패러다임 변화의 시작**:
   Unix의 프로세스 모델에서 영감을 받아:
   - **단순한 프로세스**: 각 프로세스는 단순한 로직만 수행
   - **OS의 스케줄링**: OS가 프로세스를 멀티코어에 분산
   - **격리된 실행**: 한 프로세스의 장애가 다른 프로세스에 영향 없음

3. **현재 시장/산업의 비즈니스적 요구사항**:
   클라우드 환경에서는:
   - 오토스케일링이 기본 요구사항
   - 컨테이너(파드) 단위로 스케일링
   - 웹/워커/배치가 각각 독립적으로 스케일링 필요

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Web Process** | HTTP 요청 처리 | 포트 바인딩, 요청 수신, 응답 반환 | Tomcat, Netty, Express.js | 은행 창구 직원 |
| **Worker Process** | 비동기 작업 처리 | 큐에서 작업 소비, 처리, 결과 반환 | Kafka Consumer, RabbitMQ | 백오피스 직원 |
| **Scheduler** | 주기적 작업 실행 | Cron 표현식 기반 작업 트리거 | Kubernetes CronJob, Quartz | 야간 감사 직원 |
| **Process Manager** | 프로세스 생명주기 관리 | 프로세스 시작/중지/재시작, 모니터링 | systemd, supervisord, K8s | 지점장 |
| **Queue** | 작업 버퍼링 | 메시지 저장, 소비자에게 전달 | Kafka, RabbitMQ, SQS | 대기표 발급기 |

### 2. 정교한 구조 다이어그램: Concurrency via Process Model

```text
=====================================================================================================
                    [ 12-Factor Concurrency via Process Model ]
=====================================================================================================

                              [ INCOMING TRAFFIC ]
                              /                 \
                         [ HTTP ]            [ Messages ]
                             |                    |
                             ▼                    ▼
    +-------------------------------------------------------------------------------------------+
    |                              [ LOAD BALANCER ]                                            |
    |                                                                                           |
    |  - Round Robin to Web Processes                                                          |
    |  - Health Check: /actuator/health                                                        |
    +-------------------------------------------------------------------------------------------+
                             │                    │
              ┌──────────────┼──────────────┐     │
              │              │              │     │
              ▼              ▼              ▼     │
    +------------+   +------------+   +------------+
    │  Web Proc  │   │  Web Proc  │   │  Web Proc  │   <--- HTTP 처리 프로세스
    │    #1      │   │    #2      │   │    #3      │        (Scale-out)
    │            │   │            │   │            │
    │ :8080      │   │ :8080      │   │ :8080      │
    │ Stateless  │   │ Stateless  │   │ Stateless  │
    +------------+   +------------+   +------------+
              │              │              │
              └──────────────┼──────────────┘
                             │
                             │ Produce Jobs
                             ▼
    +-------------------------------------------------------------------------------------------+
    |                              [ MESSAGE QUEUE ]                                            |
    |                              (Kafka / RabbitMQ)                                           |
    |                                                                                           |
    |  Topics:                                                                                  |
    |  - email.send (10,000 messages)                                                          |
    |  - image.resize (5,000 messages)                                                         |
    |  - report.generate (1,000 messages)                                                      |
    +-------------------------------------------------------------------------------------------+
                             │                    │                    │
              ┌──────────────┼──────────────┐     │                    │
              │              │              │     │                    │
              ▼              ▼              ▼     │                    │
    +------------+   +------------+   +------------+                    │
    │ Worker #1  │   │ Worker #2  │   │ Worker #3  │   <--- 워커 프로세스 │
    │            │   │            │   │            │       (독립적 스케일)│
    │ Email Svc  │   │ Image Svc  │   │ Report Svc │                    │
    │ Consumer   │   │ Consumer   │   │ Consumer   │                    │
    +------------+   +------------+   +------------+                    │
              │              │              │                          │
              │              │              │                          │
              └──────────────┼──────────────┘                          │
                             │                                         │
                             ▼                                         │
    +-------------------------------------------------------------------------------------------+
    |                              [ SCHEDULED JOBS ]                                           |
    |                              (Kubernetes CronJob)                                         |
    |                                                                                           |
    |  +------------------+    +------------------+    +------------------+                     |
    |  | Cron Job #1      |    | Cron Job #2      |    | Cron Job #3      |                     |
    |  | Daily Report     |    | Cache Cleanup    |    | Data Sync        |                     |
    |  | @ 00:00          |    | @ */6 * * * *    |    | @ */15 * * * *   |                     |
    |  +------------------+    +------------------+    +------------------+                     |
    +-------------------------------------------------------------------------------------------+

    =====================================================================================================
       Key Principle: Scale Independently by Process Type
       ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
       │ High HTTP Traffic?      --> Add more Web Processes (HPA: min=3, max=20)                   │
       │ High Email Queue?       --> Add more Email Workers (HPA: min=1, max=10)                   │
       │ Image Processing Heavy? --> Add more Image Workers (HPA: min=2, max=15)                   │
       │                                                                                             │
       │ Each process type scales based on its own metrics!                                         │
       └─────────────────────────────────────────────────────────────────────────────────────────────┘
    =====================================================================================================
```

### 3. 심층 동작 원리: 프로세스 모델 스케일링

**1단계: 프로세스 타입 정의 (Procfile)**

```bash
# Procfile - 프로세스 타입 정의 (Heroku/12-Factor 표준)

# 웹 프로세스 (HTTP 요청 처리)
web: java -jar target/myapp.jar server

# 워커 프로세스 (백그라운드 작업)
worker: java -jar target/myapp.jar worker

# 이메일 전송 워커
email-worker: java -jar target/myapp.jar email-worker

# 이미지 처리 워커
image-worker: java -jar target/myapp.jar image-worker

# 스케줄된 작업
scheduler: java -jar target/myapp.jar scheduler
```

**2단계: Spring Boot 멀티 프로필 구현**

```java
// Spring Boot 애플리케이션 - 프로세스 타입별 진입점
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        String processType = System.getenv("PROCESS_TYPE");

        SpringApplication app = new SpringApplication(Application.class);

        switch (processType) {
            case "web":
                app.setAdditionalProfiles("web");
                break;
            case "worker":
                app.setAdditionalProfiles("worker");
                break;
            case "email-worker":
                app.setAdditionalProfiles("email-worker");
                break;
            default:
                app.setAdditionalProfiles("web");
        }

        app.run(args);
    }
}

// 웹 프로필 - HTTP 서버 시작
@Configuration
@Profile("web")
public class WebConfig {
    // REST Controller, Web MVC 설정
}

// 워커 프로필 - 메시지 큐 소비자
@Configuration
@Profile("worker")
public class WorkerConfig {

    @Bean
    public ApplicationRunner workerRunner(KafkaTemplate<String, String> kafka) {
        return args -> {
            // HTTP 서버 시작하지 않음, 큐 리스닝만 수행
            System.out.println("Worker process started, listening to queue...");
        };
    }
}
```

**3단계: Kubernetes에서 독립적 스케일링**

```yaml
# Web Deployment - HTTP 트래픽용
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-web
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: web
        image: myapp:latest
        env:
        - name: PROCESS_TYPE
          value: "web"
        - name: SERVER_PORT
          value: "8080"
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: "250m"
            memory: "512Mi"
---
# Worker Deployment - 이메일 처리용
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-email-worker
spec:
  replicas: 2  # 웹과 다른 레플리카 수
  template:
    spec:
      containers:
      - name: worker
        image: myapp:latest  # 동일 이미지!
        env:
        - name: PROCESS_TYPE
          value: "email-worker"
        # 포트 바인딩 없음
        resources:
          requests:
            cpu: "500m"  # 웹보다 CPU 더 필요
            memory: "256Mi"
---
# Worker Deployment - 이미지 처리용
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-image-worker
spec:
  replicas: 5  # 이미지 처리가 많아 더 많은 레플리카
  template:
    spec:
      containers:
      - name: worker
        image: myapp:latest
        env:
        - name: PROCESS_TYPE
          value: "image-worker"
        resources:
          requests:
            cpu: "1000m"  # CPU 집약적
            memory: "2Gi"  # 메모리 집약적
---
# Web HPA - HTTP 트래픽 기반 스케일링
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp-web
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
---
# Worker HPA - 큐 깊이 기반 스케일링 (KEDA 사용)
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: myapp-email-worker-scaler
spec:
  scaleTargetRef:
    name: myapp-email-worker
  minReplicaCount: 1
  maxReplicaCount: 10
  triggers:
  - type: kafka
    metadata:
      bootstrapServers: kafka:9092
      topic: email.send
      lagThreshold: "100"  # 랙이 100 이상이면 스케일 아웃
```

**4단계: 메시지 큐 소비자 패턴**

```java
// Kafka 기반 워커 구현
@Service
@Profile("email-worker")
public class EmailWorker {

    private final JavaMailSender mailSender;

    @KafkaListener(
        topics = "email.send",
        groupId = "email-worker-group",
        concurrency = "3"  // 파티션별 스레드 수
    )
    public void processEmail(EmailRequest request) {
        try {
            // 이메일 전송 로직
            MimeMessage message = mailSender.createMimeMessage();
            message.setRecipients(Message.RecipientType.TO, request.getTo());
            message.setSubject(request.getSubject());
            message.setText(request.getBody());

            mailSender.send(message);

            log.info("Email sent to: {}", request.getTo());

        } catch (Exception e) {
            log.error("Failed to send email: {}", request, e);
            // 재시도는 Kafka가 담당 (Offset Commit 안 함)
            throw e;
        }
    }
}
```

### 4. 실무 코드 예시: Node.js 워커 프로세스

```javascript
// Node.js 클러스터 모드 - 다중 프로세스
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
    // 마스터 프로세스: 워커 생성 및 관리
    console.log(`Master ${process.pid} is running`);

    // CPU 코어 수만큼 워커 생성
    for (let i = 0; i < numCPUs; i++) {
        cluster.fork();
    }

    // 워커 장애 시 재시작
    cluster.on('exit', (worker, code, signal) => {
        console.log(`Worker ${worker.process.pid} died. Restarting...`);
        cluster.fork();
    });

} else {
    // 워커 프로세스: 실제 HTTP 서버
    const express = require('express');
    const app = express();

    app.get('/', (req, res) => {
        res.json({
            workerPid: process.pid,
            message: 'Hello from worker'
        });
    });

    const PORT = process.env.PORT || 3000;
    app.listen(PORT, () => {
        console.log(`Worker ${process.pid} listening on port ${PORT}`);
    });
}

/* 실행:
   node server.js
   --> Master + 8 Workers (8-core CPU)
   --> Load Balancer is the OS (round-robin)
*/
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 동시성 모델 비교표

| 평가 지표 | 스레드 기반 (Scale-up) | 프로세스 기반 (Scale-out) |
| :--- | :--- | :--- |
| **확장성** | 하드웨어 한계 | 이론적 무제한 |
| **격리성** | 낮음 (메모리 공유) | 높음 (독립 메모리) |
| **장애 영향** | 전체 프로세스 영향 | 격리된 프로세스만 |
| **동시성 제어** | 복잡 (Lock, Deadlock) | 단순 (메시지 전달) |
| **오버헤드** | 낮음 (스레드 생성) | 높음 (프로세스 생성) |
| **디버깅** | 어려움 | 상대적으로 쉬움 |

### 2. 워커 스케일링 전략 비교

| 전략 | 설명 | 트리거 | 적합한 상황 |
| :--- | :--- | :--- | :--- |
| **CPU 기반** | CPU 사용률 기반 | CPU > 70% | CPU 집약적 작업 |
| **메모리 기반** | 메모리 사용률 기반 | Memory > 80% | 메모리 집약적 작업 |
| **큐 깊이 기반** | 메시지 큐 대기열 | Queue Length > 100 | 메시지 처리 작업 |
| **지연 시간 기반** | 요청 응답 시간 | P99 > 500ms | 사용자 대면 서비스 |
| **시간 기반** | 시간대별 예측 | 09:00-18:00 | 예측 가능한 워크로드 |

### 3. 과목 융합 관점 분석

**Concurrency + 메시지 큐**
- 워커가 큐에서 작업을 소비 (Consumer)
- 백프레셔(Backpressure)로 과부하 방지
- 큐 깊이 기반 자동 스케일링 (KEDA)

**Concurrency + 서버리스**
- FaaS(Function as a Service)는 프로세스 모델의 극단적 형태
- 각 요청이 별도의 함수 인스턴스로 실행
- 이벤트 기반 자동 스케일링

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] CPU 집약적 작업의 스케일링**
- **문제점**: 이미지 리사이징 작업이 CPU를 100% 사용하여 웹 응답 지연 발생.
- **기술사 판단**: **웹/워커 분리 + 독립적 스케일링**
  1. 이미지 처리를 웹 프로세스에서 분리 (비동기)
  2. 전용 이미지 워커 배포 (고 CPU 할당)
  3. KEDA로 큐 깊이 기반 오토스케일링

**[상황 B] 장기 실행 작업의 타임아웃 처리**
- **문제점**: 웹 요청 내에서 30초 이상 걸리는 리포트 생성 작업.
- **기술사 판단**: **비동기 패턴으로 전환**
  ```
  1. Web: 요청 접수 -> Job 큐에 등록 -> Job ID 반환
  2. Worker: 큐에서 Job 소비 -> 리포트 생성 -> 완료 알림
  3. Client: Job ID로 폴링 또는 WebSocket으로 결과 수신
  ```

### 2. 도입 시 고려사항 체크리스트

**프로세스 설계 체크리스트**
- [ ] 각 프로세스 타입이 독립적으로 스케일링 가능한가?
- [ ] 장기 실행 작업이 웹 요청 스레드를 차단하지 않는가?
- [ ] 메시지 큐가 과부하 시 백프레셔를 제공하는가?
- [ ] 워커 장애 시 작업이 유실되지 않는가? (At-least-once 보장)

**스케일링 체크리스트**
- [ ] HPA가 적절한 메트릭을 기반으로 작동하는가?
- [ ] 스케일 다운이 급격하게 발생하지 않는가? (안정화 윈도우)
- [ ] 큐 기반 스케일링 시 랙(Lag)이 정상적으로 감소하는가?

### 3. 주의사항 및 안티패턴

**안티패턴 1: 웹 요청 내 장기 실행 작업**
```java
// 잘못된 예: 웹 스레드에서 장기 실행
@GetMapping("/report")
public ResponseEntity<byte[]> generateReport() {
    byte[] report = reportService.generateLargeReport(); // 30초 소요!
    return ResponseEntity.ok(report);
}

// 올바른 예: 비동기 패턴
@GetMapping("/report")
public ResponseEntity<JobResponse> startReportGeneration() {
    String jobId = jobQueue.enqueue("generate-report");
    return ResponseEntity.accepted()
        .body(new JobResponse(jobId, "/api/jobs/" + jobId));
}
```

**안티패턴 2: 메모리 내 큐 사용**
```java
// 잘못된 예: 메모리 내 큐 (워커 장애 시 유실)
Queue<Job> jobQueue = new LinkedList<>();

// 올바른 예: 영속적 메시지 큐
@KafkaListener(topics = "jobs")
public void processJob(Job job) {
    // Kafka가 메시지 보존
}
```

**안티패턴 3: 동기식 워커 호출**
```java
// 잘못된 예: 워커를 동기식으로 호출
restTemplate.postForObject("http://worker-service/process", request, Response.class);

// 올바른 예: 비동기 메시지 전달
kafkaTemplate.send("process-queue", request);
```

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | Scale-up (AS-IS) | Scale-out (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **최대 처리량** | 하드웨어 한계 (예: 10K RPS) | 이론적 무제한 | **선형 확장** |
| **장애 복구** | 전체 서버 재시작 (수분) | 격리된 프로세스 재시작 (수초) | **95% 단축** |
| **비용 효율** | 대형 서버 과대 투자 | 트래픽에 맞춘 소형 서버 | **40% 비용 절감** |
| **배포 위험** | 전체 서버 재배포 | 점진적 롤링 업데이트 | **위험 90% 감소** |

### 2. 미래 전망 및 진화 방향

**서버리스(FaaS)로의 진화**
- 프로세스 모델의 극단적 형태: 각 요청이 별도 인스턴스
- AWS Lambda, Cloud Functions에서 자동 스케일링
- Cold Start 문제를 해결하기 위한 Provisioned Concurrency

**이벤트 기반 오토스케일링 (KEDA)**
- 메시지 큐 깊이, Redis 리스트 길이 등 다양한 이벤트 소스
- Kubernetes 네이티브 방식으로 통합
- 세밀한 스케일링 제어

### 3. 참고 표준/가이드
- **The Twelve-Factor App (12factor.net/concurrency)**: Concurrency 원칙
- **KEDA Documentation**: 이벤트 기반 오토스케일링
- **Kafka Consumer Configurations**: 워커 스케일링 가이드
- **Kubernetes HPA**: 수평적 파드 오토스케일러

---

## 관련 개념 맵 (Knowledge Graph)
- **[12-Factor App](@/studynotes/15_devops_sre/01_sre/twelve_factor_app.md)**: 동시성 원칙을 포함한 전체 방법론
- **[무상태 프로세스 (Stateless)](./stateless_processes.md)**: 스케일 아웃의 전제 조건
- **[메시지 큐 (Message Queue)](./message_queue.md)**: 워커 프로세스 간 통신
- **[쿠버네티스 HPA](@/studynotes/13_cloud_architecture/01_native/kubernetes.md)**: 자동 수평 확장
- **[카오스 엔지니어링](@/studynotes/15_devops_sre/02_observability/chaos_engineering.md)**: 프로세스 장애 격리 테스트

---

## 어린이를 위한 3줄 비유 설명
1. 은행에서 **한 명의 직원이 여러 손님을 동시에** 응대하는 것보다, **여러 직원이 각각 한 명씩** 응대하는 게 더 효율적이에요.
2. 손님이 갑자기 많아지면 **직원을 더 투입**하면 돼요. 한 직원이 더 빨리 일하려고 애쓰지 않아도 돼죠!
3. 컴퓨터도 이렇게 **여러 프로그램을 동시에 돌려서** 일해요. 일이 많아지면 **컴퓨터를 더 늘리는** 게 답이에요!
