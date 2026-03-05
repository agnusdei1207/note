+++
title = "서킷 브레이커 패턴 (Circuit Breaker)"
date = 2024-05-21
description = "분산 시스템에서 장애 전파를 방지하기 위해 서비스 호출을 차단하고 폴백을 제공하는 회복 탄력성 패턴"
weight = 22
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Circuit Breaker", "Resilience", "Microservices", "Fault Tolerance", "Hystrix", "Resilience4j"]
+++

# 서킷 브레이커 패턴 (Circuit Breaker) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 마이크로서비스 환경에서 특정 서비스의 장애가 연쇄적으로 전파(Cascading Failure)되는 것을 방지하기 위해, 서비스 호출 상태를 모니터링하고 장애 감지 시 자동으로 호출을 차단(Open)하여 시스템 전체를 보호하는 회복 탄력성(Resilience) 디자인 패턴입니다.
> 2. **가치**: 장애 서비스로의 불필요한 대기(Thread Blocking)를 제거하여 **스레드 풀 고갈 방지**, **MTTD/MTTR 단축**, **부분적 서비스 저하(Graceful Degradation)**를 통해 전체 서비스 중단을 예방합니다.
> 3. **융합**: 폴백(Fallback), 벌크헤드(Bulkhead), 재시도(Retry) 패턴과 결합하여 Resilience4j, Istio, Hystrix 등으로 구현되며, 쿠버네티스 서비스 메시와 통합됩니다.

---

## Ⅰ. 개요 (Context & Background)

서킷 브레이커(Circuit Breaker)는 전기 회로의 차단기에서 영감을 받은 소프트웨어 디자인 패턴입니다. 전기 차단기가 과부하 시 회로를 끊어 화재를 방지하듯, 소프트웨어 서킷 브레이커는 서비스 장애 시 호출을 차단하여 시스템 전체의 장애 전파를 막습니다.

**💡 비유**: 서킷 브레이커는 **'자동차의 퓨즈'**와 같습니다. 전기 과부하가 발생하면 퓨즈가 끊어져 자동차 전체가 망가지는 것을 방지합니다. 마찬가지로, 서킷 브레이커는 한 부품(서비스)이 고장 나면 그 부품으로 가는 전원(호출)을 차단하여 다른 부품들이 정상 작동하도록 보호합니다.

**등장 배경 및 발전 과정**:
1. **분산 시스템의 장애 전파**: 마이크로서비스에서 서비스 A가 서비스 B를 호출하는데 B가 응답하지 않으면, A의 스레드가 대기하며 스레드 풀이 고갈됩니다.
2. **Michael Nygard의 소개 (2007)**: "Release It!" 책에서 서킷 브레이커 패턴을 체계적으로 소개했습니다.
3. **Netflix Hystrix (2012)**: 대규모 분산 시스템에서 서킷 브레이커를 구현한 오픈소스로 대중화되었습니다.
4. **Resilience4j (2017~)**: Hystrix의 경량화된 대안으로 현재 표준적으로 사용됩니다.
5. **서비스 메시 통합 (2018~)**: Istio, Linkerd가 Envoy 기반 서킷 브레이커를 제공합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: 서킷 브레이커 상태 머신

| 상태 | 설명 | 동작 | 전이 조건 |
|---|---|---|---|
| **CLOSED** | 정상 상태 | 모든 요청이 서비스로 전달됨 | 실패율이 임계치 초과 시 → OPEN |
| **OPEN** | 차단 상태 | 모든 요청이 즉시 실패(Fallback 실행) | 타임아웃 경과 시 → HALF_OPEN |
| **HALF_OPEN** | 탐색 상태 | 제한된 요청만 서비스로 전달 | 성공 시 → CLOSED, 실패 시 → OPEN |
| **DISABLED** | 비활성화 | 서킷 브레이커 동작 안 함 | 수동 활성화 |
| **FORCED_OPEN** | 강제 차단 | 항상 차단 | 수동 해제 |

### 정교한 구조 다이어그램: 서킷 브레이커 상태 머신

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Circuit Breaker State Machine ]                         │
│                     (Resilience4j Implementation)                            │
└─────────────────────────────────────────────────────────────────────────────┘

                          ┌─────────────────────┐
                          │                     │
                          │    Start State      │
                          │                     │
                          └──────────┬──────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │                                │
                    │          CLOSED                │◄──────────────────┐
                    │        (정상 상태)              │                   │
                    │                                │                   │
                    │  - 모든 요청 통과               │                   │
                    │  - 성공/실패 카운트              │                   │
                    │  - 실패율 모니터링              │                   │
                    │                                │                   │
                    └───────────────┬────────────────┘                   │
                                    │                                    │
                          [ 실패율 > 임계값 ]                            │
                          (예: 50% 이상 실패)                           │
                                    │                                    │
                                    ▼                                    │
                    ┌────────────────────────────────┐                   │
                    │                                │                   │
                    │           OPEN                 │                   │
                    │        (차단 상태)              │                   │
                    │                                │                   │
                    │  - 모든 요청 차단               │                   │
                    │  - 즉시 Fallback 실행           │                   │
                    │  - 타이머 시작                  │───────────────────┼──►
                    │    (waitDurationInOpenState)   │                   │    [ 성공 ]
                    │                                │                   │
                    └───────────────┬────────────────┘                   │
                                    │                                    │
                      [ waitDuration 경과 ]                              │
                                    │                                    │
                                    ▼                                    │
                    ┌────────────────────────────────┐                   │
                    │                                │                   │
                    │        HALF_OPEN               │───────────────────┘
                    │        (탐색 상태)              │
                    │                                │
                    │  - 제한된 요청만 통과           │
                    │    (permittedNumberOfCalls     │
                    │     InHalfOpenState)           │
                    │  - 결과에 따라 상태 전이        │
                    │                                │
                    └───────────────┬────────────────┘
                                    │
                   ┌────────────────┴────────────────┐
                   │                                 │
             [ 실패 ]                          [ 성공 ]
                   │                                 │
                   ▼                                 │
            ┌────────────┐                           │
            │   OPEN     │◄──────────────────────────┘
            │  (재차단)   │
            └────────────┘


[ Circuit Breaker Metrics & Configuration ]

┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  Configuration Parameters (Resilience4j):                                    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ failureRateThreshold: 50                                               │ │
│  │     - 실패율이 50% 이상이면 OPEN으로 전이                               │ │
│  │                                                                        │ │
│  │ waitDurationInOpenState: 60s                                           │ │
│  │     - OPEN 상태 유지 시간 (이후 HALF_OPEN으로)                         │ │
│  │                                                                        │ │
│  │ permittedNumberOfCallsInHalfOpenState: 10                              │ │
│  │     - HALF_OPEN 상태에서 허용할 요청 수                                 │ │
│  │                                                                        │ │
│  │ slidingWindowType: COUNT_BASED                                         │ │
│  │     - 슬라이딩 윈도우 타입 (COUNT_BASED 또는 TIME_BASED)               │ │
│  │                                                                        │ │
│  │ slidingWindowSize: 100                                                 │ │
│  │     - 슬라이딩 윈도우 크기 (최근 100개 요청 기준)                       │ │
│  │                                                                        │ │
│  │ minimumNumberOfCalls: 10                                               │ │
│  │     - 통계 계산을 위한 최소 호출 수                                     │ │
│  │                                                                        │ │
│  │ slowCallRateThreshold: 100                                             │ │
│  │     - 느린 호출 비율 임계값                                             │ │
│  │                                                                        │ │
│  │ slowCallDurationThreshold: 2s                                          │ │
│  │     - 느린 호출 판단 기준 시간                                          │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  Metrics Collected:                                                          │
│  - failureRate: 현재 실패율                                                  │
│  - slowCallRate: 느린 호출 비율                                              │
│  - numberOfCalls: 총 호출 수                                                 │
│  - numberOfSuccessfulCalls: 성공 호출 수                                     │
│  - numberOfFailedCalls: 실패 호출 수                                         │
│  - numberOfSlowCalls: 느린 호출 수                                           │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: 장애 전파 방지 메커니즘

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    Cascading Failure Prevention                             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ Without Circuit Breaker: 장애 전파 시나리오 ]                            │
│                                                                            │
│  Client ───► Service A ───► Service B ───► Service C (DOWN!)              │
│                │                │                │                         │
│                │                │                ▼                         │
│                │                │         [ 무한 대기 ]                     │
│                │                │         Thread Blocked                    │
│                │                ▼                                          │
│                │         Thread Pool                                        │
│                │         Exhaustion!                                        │
│                ▼                                                            │
│           Thread Pool                                                       │
│           Exhaustion!                                                       │
│           (서비스 A도 다운!)                                                │
│                                                                            │
│  결과: Service C 장애 → Service B 다운 → Service A 다운 → 전체 장애        │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ With Circuit Breaker: 장애 격리 ]                                        │
│                                                                            │
│  Client ───► Service A ───► Service B ───► Service C (DOWN!)              │
│                │                │                │                         │
│                │                │         ┌──────┴──────┐                 │
│                │                │         │   Circuit   │                 │
│                │                │         │   Breaker   │                 │
│                │                │         │   [OPEN]    │                 │
│                │                │         └──────┬──────┘                 │
│                │                │                │                         │
│                │                │         [ 즉시 실패 ]                    │
│                │                │         (Fast Fail)                      │
│                │                │                │                         │
│                │                │                ▼                         │
│                │                │         ┌──────────────┐                │
│                │                │         │   Fallback  │                │
│                │                │         │   Response   │                │
│                │                │         │  (캐시/기본값)│                │
│                │                │         └──────────────┘                │
│                │                │                                          │
│                │           [ 스레드 즉시 해제 ]                            │
│                │                                                  │
│                ◄──────────────────────────────────────────────────────┘  │
│                │                                                           │
│                ▼                                                           │
│           정상 응답                                                         │
│           (서비스 A 계속 작동)                                              │
│                                                                            │
│  결과: Service C 장애 → Fallback 실행 → Service B 정상 → Service A 정상   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: Resilience4j 서킷 브레이커 구현

```java
// Resilience4j Circuit Breaker 구현 (Spring Boot)

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;
import io.vavr.control.Try;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import java.time.Duration;
import java.util.function.Supplier;

@Service
public class OrderService {

    private final RestTemplate restTemplate;
    private final CircuitBreaker circuitBreaker;

    public OrderService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;

        // 서킷 브레이커 설정
        CircuitBreakerConfig config = CircuitBreakerConfig.custom()
            // 실패율 임계치 (50% 이상이면 OPEN)
            .failureRateThreshold(50)
            // OPEN 상태 유지 시간
            .waitDurationInOpenState(Duration.ofSeconds(60))
            // HALF_OPEN에서 허용할 호출 수
            .permittedNumberOfCallsInHalfOpenState(10)
            // 슬라이딩 윈도우 타입
            .slidingWindowType(CircuitBreakerConfig.SlidingWindowType.COUNT_BASED)
            // 슬라이딩 윈도우 크기
            .slidingWindowSize(100)
            // 최소 호출 수
            .minimumNumberOfCalls(20)
            // 느린 호출 임계치
            .slowCallRateThreshold(100)
            .slowCallDurationThreshold(Duration.ofSeconds(2))
            // 예외 처리
            .recordExceptions(IOException.class, TimeoutException.class)
            .ignoreExceptions(BusinessException.class)
            .build();

        // 레지스트리에서 서킷 브레이커 생성
        CircuitBreakerRegistry registry = CircuitBreakerRegistry.of(config);
        this.circuitBreaker = registry.circuitBreaker("orderService");
    }

    /**
     * 어노테이션 기반 서킷 브레이커
     */
    @CircuitBreaker(name = "orderService", fallbackMethod = "getOrderFallback")
    public Order getOrder(Long orderId) {
        String url = "http://inventory-service/api/orders/" + orderId;
        return restTemplate.getForObject(url, Order.class);
    }

    /**
     * Fallback 메서드 - 서킷이 OPEN일 때 실행
     */
    public Order getOrderFallback(Long orderId, Exception e) {
        log.warn("Circuit Breaker activated for order: {}, error: {}",
                 orderId, e.getMessage());

        // 캐시된 데이터 반환 또는 기본값
        return Order.builder()
            .id(orderId)
            .status(OrderStatus.UNKNOWN)
            .message("Service temporarily unavailable. Using cached data.")
            .cached(true)
            .build();
    }

    /**
     * 프로그래밍 방식 서킷 브레이커
     */
    public Order getOrderWithManualCircuitBreaker(Long orderId) {
        // Supplier로 실제 호출 래핑
        Supplier<Order> supplier = CircuitBreaker.decorateSupplier(
            circuitBreaker,
            () -> {
                String url = "http://inventory-service/api/orders/" + orderId;
                return restTemplate.getForObject(url, Order.class);
            }
        );

        // Try로 실행 (성공/실패 처리)
        return Try.ofSupplier(supplier)
            .recover(throwable -> {
                log.warn("Fallback executed: {}", throwable.getMessage());
                return getOrderFallback(orderId, throwable);
            })
            .get();
    }

    /**
     * 서킷 브레이커 상태 확인
     */
    public CircuitBreakerStatus getCircuitBreakerStatus() {
        CircuitBreaker.Metrics metrics = circuitBreaker.getMetrics();

        return CircuitBreakerStatus.builder()
            .state(circuitBreaker.getState())
            .failureRate(metrics.getFailureRate())
            .slowCallRate(metrics.getSlowCallRate())
            .numberOfCalls(metrics.getNumberOfCalls())
            .numberOfSuccessfulCalls(metrics.getNumberOfSuccessfulCalls())
            .numberOfFailedCalls(metrics.getNumberOfFailedCalls())
            .build();
    }
}
```

### application.yml 설정

```yaml
# application.yml - Resilience4j 설정

resilience4j:
  circuitbreaker:
    configs:
      default:
        # 기본 서킷 브레이커 설정
        registerHealthIndicator: true
        slidingWindowType: COUNT_BASED
        slidingWindowSize: 100
        minimumNumberOfCalls: 20
        failureRateThreshold: 50
        waitDurationInOpenState: 60s
        permittedNumberOfCallsInHalfOpenState: 10
        slowCallDurationThreshold: 2s
        slowCallRateThreshold: 100
        automaticTransitionFromOpenToHalfOpenEnabled: true

    instances:
      orderService:
        baseConfig: default
        failureRateThreshold: 30  # 주문 서비스는 더 보수적으로

      paymentService:
        baseConfig: default
        failureRateThreshold: 20  # 결제 서비스는 매우 보수적으로
        waitDurationInOpenState: 120s

      inventoryService:
        baseConfig: default
        slidingWindowSize: 50
        minimumNumberOfCalls: 10

  # 재시도 설정 (서킷 브레이커와 함께 사용)
  retry:
    configs:
      default:
        maxAttempts: 3
        waitDuration: 1s
        exponentialBackoffMultiplier: 2
        retryExceptions:
          - java.io.IOException
          - java.util.concurrent.TimeoutException

    instances:
      orderService:
        baseConfig: default

  # 타임아웃 설정
  timelimiter:
    configs:
      default:
        timeoutDuration: 3s
        cancelRunningFuture: true

# Actuator로 서킷 브레이커 메트릭 노출
management:
  endpoints:
    web:
      exposure:
        include: health,metrics,circuitbreakers
  health:
    circuitbreakers:
      enabled: true
```

### Istio 서킷 브레이커 (서비스 메시)

```yaml
# Istio DestinationRule - 서킷 브레이커 설정

apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: inventory-service
  namespace: production
spec:
  host: inventory-service
  trafficPolicy:
    # 연결 풀 설정 (벌크헤드 + 로드 밸런싱)
    connectionPool:
      tcp:
        maxConnections: 100        # 최대 연결 수
        connectTimeout: 5s         # 연결 타임아웃
      http:
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
        # 요청당 타임아웃
        idleTimeout: 60s

    # 아웃라이어 탐지 (서킷 브레이커)
    outlierDetection:
      # 연속 5xx 에러 횟수 (이후 제거)
      consecutive5xxErrors: 5

      # 탐지 간격
      interval: 30s

      # 제거 기본 시간 (ejection time)
      baseEjectionTime: 30s

      # 최대 제거 비율
      maxEjectionPercent: 50

      # 최소 정상 호스트 비율
      minHealthPercent: 25

  # 서브셋별 설정
  subsets:
  - name: v1
    labels:
      version: v1
    trafficPolicy:
      outlierDetection:
        consecutive5xxErrors: 3
        baseEjectionTime: 60s

  - name: v2
    labels:
      version: v2
    trafficPolicy:
      outlierDetection:
        consecutive5xxErrors: 5
        baseEjectionTime: 30s
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 서킷 브레이커 구현체

| 비교 관점 | Hystrix | Resilience4j | Istio | Sentinel |
|---|---|---|---|---|
| **개발사** | Netflix | 별도 프로젝트 | Google/IBM | Alibaba |
| **상태** | Maintenance Only | Active | Active | Active |
| **구현 방식** | 라이브러리 | 라이브러리 | 서비스 메시 | 라이브러리 + 콘솔 |
| **오버헤드** | 높음 | 낮음 | 중간 | 낮음 |
| **기능** | CB, Fallback | CB, Retry, Rate Limiter | CB, Outlier Detection | CB, Flow Control |
| **모니터링** | Hystrix Dashboard | Micrometer/Prometheus | Kiali | Sentinel Dashboard |
| **언어 지원** | Java | Java | 언어 무관 | Java |

### 과목 융합 관점 분석

**운영체제(OS)와의 융합**:
- **스레드 풀 관리**: 서킷 브레이커는 스레드 블로킹을 방지하여 OS 스케줄러 부하 감소
- **프로세스 격리**: 벌크헤드 패턴과 함께 프로세스 수준 격리

**네트워크와의 융합**:
- **타임아웃 설정**: TCP/HTTP 타임아웃과 서킷 브레이커의 연계
- **로드 밸런싱**: 서킷 브레이커가 로드 밸런서에서 불량 인스턴스 제거

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 이커머스 장애 대응

**문제 상황**: 결제 서비스 장애 시 주문 서비스 스레드 풀이 고갈되어 전체 서비스가 마비됩니다.

**기술사의 전략적 의사결정**:

1. **서킷 브레이커 적용**:

   ```java
   // 결제 서비스 호출에 서킷 브레이커 적용
   @CircuitBreaker(name = "paymentService", fallbackMethod = "processPaymentFallback")
   public PaymentResult processPayment(Order order) {
       return paymentClient.charge(order);
   }

   // Fallback: 결제 대기 상태로 변경
   public PaymentResult processPaymentFallback(Order order, Exception e) {
       order.setStatus(OrderStatus.PAYMENT_PENDING);
       orderRepository.save(order);

       // 결제 재시도 큐에 등록
       paymentRetryQueue.publish(order);

       return PaymentResult.builder()
           .status(PaymentStatus.PENDING)
           .message("Payment will be processed shortly")
           .build();
   }
   ```

2. **임계값 설정**:

   | 서비스 | 실패율 임계치 | OPEN 유지 시간 | Fallback 전략 |
   |---|---|---|---|
   | 결제 | 20% | 120s | 대기 상태 + 재시도 큐 |
   | 재고 | 30% | 60s | 캐시된 재고 |
   | 배송 | 50% | 30s | 기본 배송일 |

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - 과도하게 낮은 임계값**: 실패율 10%로 설정하면 정상적인 트래픽 스파이크에도 서킷이 열릴 수 있습니다.

- **안티패턴 - Fallback 없는 서킷 브레이커**: 서킷이 열린 후 아무 응답 없이 실패하면 사용자 경험이 저하됩니다.

- **체크리스트**:
  - [ ] 서비스별 적절한 임계값 설정
  - [ ] 의미 있는 Fallback 구현
  - [ ] 모니터링 대시보드 구축
  - [ ] 알림 설정 (서킷 상태 변경 시)

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 서킷 브레이커 없음 | 서킷 브레이커 적용 | 개선율 |
|---|---|---|---|
| **장애 전파 시간** | 5~10분 | 1~3초 | 99% 단축 |
| **MTTR** | 30분 | 5분 | 83% 단축 |
| **부분 서비스 가용성** | 0% | 90% | 90% 향상 |
| **스레드 풀 고갈** | 빈번 | 없음 | 100% 방지 |

### 미래 전망 및 진화 방향

- **AI 기반 동적 임계값**: 머신러닝으로 최적의 서킷 브레이커 설정 자동 조정
- **eBPF 기반 서킷 브레이커**: 커널 레벨에서 구현하여 오버헤드 최소화
- **멀티 클러스터 서킷 브레이커**: 여러 클러스터 간 장애 격리

### ※ 참고 표준/가이드
- **Microsoft Azure Resiliency Patterns**: 클라우드 디자인 패턴
- **Netflix Hystrix Wiki**: 서킷 브레이커 구현 가이드
- **Resilience4j Documentation**: 현대적 서킷 브레이커 구현

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [마이크로서비스 아키텍처 (MSA)](@/studynotes/13_cloud_architecture/01_native/msa.md) : 서킷 브레이커가 적용되는 아키텍처
- [서비스 메시](@/studynotes/13_cloud_architecture/01_native/service_mesh.md) : Istio 기반 서킷 브레이커
- [API 게이트웨이](@/studynotes/13_cloud_architecture/01_native/api_gateway.md) : 게이트웨이 레벨 서킷 브레이커
- [폴백 패턴](@/studynotes/13_cloud_architecture/01_native/fallback_pattern.md) : 서킷 브레이커와 함께 사용
- [SRE](@/studynotes/15_devops_sre/_index.md) : 서비스 신뢰성 공학

---

### 👶 어린이를 위한 3줄 비유 설명
1. 서킷 브레이커는 **'자동차의 퓨즈'**와 같아요. 전기가 너무 많이 흐르면 퓨즈가 끊어져 자동차를 보호해요.
2. 한 부품이 고장 나면 **'그 부품으로 가는 전기를 차단'**해요. 다른 부품들은 계속 작동할 수 있어요.
3. 덕분에 **'한 부품 고장이 전체 고장으로 번지지 않아요'**. 대신 비상시용 예비 부품(Fallback)을 사용해요!
