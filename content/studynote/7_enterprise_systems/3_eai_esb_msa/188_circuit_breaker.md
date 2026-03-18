+++
title = "188. 서킷 브레이커 (Circuit Breaker)"
date = "2026-03-18"
[extra]
category = "studynote-enterprise"
keywords = ["Circuit Breaker", "서킷 브레이커", "MSA", "Microservices", "Resilience", "내결함성", "Hystrix", "Resilience4j"]
+++

# 서킷 브레이커 (Circuit Breaker)

> **Circuit Breaker**: 분산 시스템에서 하위 서비스 장애가 상위 시스템으로 전파(Propagation)되어 **연쇄 장애(Cascading Failure)**를 일으키는 것을 방지하기 위해, 장애 서비스 호출을 조기에 차단하고 **폴백(Fallback)** 경로를 제공하는 내결함성(Resilience) 패턴으로 전기 회로의 차단기(Circuit Breaker)에서 유래한 디자인 패턴

## 핵심 인사이트

마이크로서비스 환경에서 **한 서비스의 장애가 전체 시스템을 멈추게 할 수 있습니다**. 사용자 서비스가 느려지면, 그를 호출하는 주문 서비스는 타임아웃으로 대기하고, 주문 서비스의 스레드 풀이 고갈되면, 결제 서비스까지 멈추는 **도미노 현상**이 발생합니다. **서킷 브레이커**는 **"하위 서비스가 이미 문제가 있다는 것을 알면, 더 이상 호출하지 말고 빨리 포기하라!"**는 전략입니다. 실패가 일정 수준 누적되면 회로를 **Open(차단)**하여 추가 호출을 방지하고, 주기적으로 **Half-Open(반 열림)** 상태로 회복을 시도하여 자동 복구를 가능하게 합니다.

---

## Ⅰ. 개념 정의 및 등장 배경

### 1. 정의 및 유래

**서킷 브레이커(Circuit Breaker)**는 2006년 Michael Nygard가 제안한 패턴으로, 전기 회로의 **과부하 차단기**에서 착안한 디자인 패턴입니다.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    전기 회로 차단기 유래                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ⚡ 전기 회로의 과부하 방지                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │  │
│  │    전원 ───┬───  [차단기]  ───┬───  가전제품                       │  │
│  │            │                    │                                   │  │
│  │            │         (과부하 시 │                                   │  │
│  │            │          자동 차단) │                                   │  │
│  │            ▼                    ▼                                   │  │
│  │    ┌─────────────────────────────────────┐                         │  │
│  │    │  과부하 감지:                       │                         │  │
│  │    │  - 전류가 정격 초과                 │                         │  │
│  │    │  → 즉시 회로 차단 (Open)            │                         │  │
│  │    │  - 화재, 감전 사고 방지              │                         │  │
│  │    │                                    │                         │  │
│  │    │  복구 시도:                          │                         │  │
│  │    │  - 주기적으로 회로 폐쇄 시도         │                         │  │
│  │    │  - 정상이면 다시 사용 (Close)        │                         │  │
│  │    └─────────────────────────────────────┘                         │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   🔄 서비스 장애로 동일한 원리 적용                                         │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │  │
│  │    호출자 ───┬───  [서킷 브레이커]  ───┬───  하위 서비스              │  │
│  │            │                         │                               │  │
│  │            │              (장애 감지 시 │                               │  │
│  │            │               호출 차단)  │                               │  │
│  │            ▼                         ▼                               │  │
│  │    ┌───────────────────────────────────────────┐                     │  │
│  │    │  장애 감지:                                 │                     │  │
│  │    │  - 실패율 임계값 초과 (예: 50%)            │                     │  │
│  │    │  → 즉시 회로 차단 (Open)                  │                     │  │
│  │    │  - 연쇄 장애(Cascading Failure) 방지      │                     │  │
│  │    │                                            │                     │  │
│  │    │  복구 시도:                                 │                     │  │
│  │    │  - 주기적으로 회로 반 열림 (Half-Open)     │                     │  │
│  │    │  - 성공 시 다시 사용 (Close)               │                     │  │
│  │    └───────────────────────────────────────────┘                     │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 연쇄 장애(Cascading Failure) 시나리오

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    연쇄 장애 발생 시나리오                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  초기 상태 (정상)                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   고객 ──▶ API Gateway ──▶ 주문 서비스 ──▶ 사용자 서비스 ──▶ DB    │   │
│  │                                      │                              │   │
│  │                                      └──▶ 재고 서비스 ──▶ DB         │   │
│  │                                                                      │   │
│  │   모든 서비스가 200ms 응답                                             │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  T1: 사용자 서비스 장애 발생 (DB 연결 풀 고갈)                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   고객 ──▶ API Gateway ──▶ 주문 서비스 ──▶ 사용자 서비스 ──X DB    │   │
│  │                                      │     ↑                        │   │
│  │                                      │     타임아웃! (30초 대기)    │   │
│  │                                      │                              │   │
│  │                                      └──▶ 재고 서비스 ──▶ DB         │   │
│  │                                                                      │   │
│  │   문제: 주문 서비스의 스레드가 사용자 서비스 응답을 기다리며 고갈    │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  T2: 주문 서비스 스레드 풀 고갈                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   고객 ──▶ API Gateway ──X 주문 서비스 ──X 사용자 서비스             │   │
│  │              ↑                              ↑                        │   │
│  │           타임아웃!                      타임아웃!                   │   │
│  │          (30초 대기)                                                  │   │
│  │                                                                      │   │
│  │   문제: API Gateway의 리소스까지 고갈                                 │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  T3: 전체 시스템 장애 (연쇄 장애 완료)                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   고객 ──X──────────────X──────────────X──────────────X               │   │
│  │                                                                      │   │
│  │   "사용자 서비스 하나가 죽었는데, 왜 다 안 돼?!"                       │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   → 서킷 브레이커가 있었다면 T1에서 사용자 서비스 호출을 차단!               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3. 서킷 브레이커의 목표

| 목표 | 설명 | 효과 |
|:-----|:-----|:-----|
| **연쇄 장애 방지** | 하위 서비스 장애가 상위로 전파되지 않음 | 시스템 부분적 가용성 유지 |
| **리소스 보호** | 스레드 풀, 커넥션 풀 고갈 방지 | 호출자 서비스 생존 |
| **빠른 실패** | 장애 서비스에 길게 대기하지 않음 | 사용자 경험 개선 (빠른 에러) |
| **자동 복구** | 서비스 회복 시 자동으로 트래픽 복구 | 수동 개입 불필요 |

---

## Ⅱ. 서킷 브레이커 상태 및 전이

### 1. 세 가지 상태

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    서킷 브레이커 상태 전이 다이어그램                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                      ┌─────────────────────┐                                │
│                      │      CLOSED        │                                │
│                      │   (회로 폐쇄)      │                                │
│                      │                     │                                │
│                      │  • 정상 동작        │                                │
│                      │  • 모든 요청 통과  │                                │
│                      │  • 실패 카운트     │                                │
│                      └──────────┬──────────┘                                │
│                                 │                                          │
│                                 │ 실패율 임계값 초과                        │
│                                 │ (예: 10회 중 5회 실패)                  │
│                                 ▼                                          │
│                      ┌─────────────────────┐                                │
│                      │      OPEN          │                                │
│                      │   (회로 개방)      │                                │
│                      │                     │                                │
│                      │  • 모든 요청 차단  │                                │
│                      │  • 즉시 폴백 반환   │                                │
│                      │  • 타임아웃 기다림  │                                │
│                      └──────────┬──────────┘                                │
│                                 │                                          │
│                                 │ 타임아웃 경과 후                         │
│                                 │ (예: 60초 후)                           │
│                                 ▼                                          │
│                      ┌─────────────────────┐                                │
│                      │    HALF-OPEN       │                                │
│                      │   (반 열림)        │                                │
│                      │                     │                                │
│                      │  • 제한적 요청 허용│                                │
│                      │  • 복구 시도       │                                │
│                      │  • 결과에 따라 전이 │                                │
│                      └──────────┬──────────┘                                │
│                                 │                                          │
│                ┌────────────────┴────────────────┐                          │
│                │                                 │                          │
│        성공 (회복 완료)                   실패 (여전히 장애)                │
│                │                                 │                          │
│                ▼                                 ▼                          │
│       ┌───────────────────┐          ┌───────────────────┐                │
│       │     CLOSED        │          │      OPEN        │                │
│       │  (다시 정상)      │          │   (다시 차단)    │                │
│       └───────────────────┘          └───────────────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 상태별 상세 동작

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    상태별 동작 상세                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. CLOSED (회로 폐쇄 - 정상 상태)                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   요청 ──▶ [서킷 브레이커] ──▶ 실제 서비스 호출                     │   │
│  │                                                                      │   │
│  │   • 모든 요청이 통과                                                │   │
│  │   • 성공/실패를 카운트                                                │   │
│  │   • 실패율/실패 수를 슬라이딩 윈도우로 추적                           │   │
│  │                                                                      │   │
│  │   예시 설정:                                                         │   │
│  │   - 최소 호출: 10회                                                   │   │
│  │   - 실패율 임계값: 50%                                                │   │
│  │   - 대기 시간: 60초                                                   │   │
│  │                                                                      │   │
│  │   동작:                                                              │   │
│  │   최근 10회 중 5회 이상 실패 → OPEN으로 전이                           │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  2. OPEN (회로 개방 - 차단 상태)                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   요청 ──▶ [서킷 브레이커] ──X─ 실제 서비스 호출 (차단!)             │   │
│  │                     │                                               │   │
│  │                     └──▶ 즉시 Fallback/CircuitBreakerOpenException  │   │
│  │                                                                      │   │
│  │   • 모든 요청이 차단 (실제 호출 없음)                                │   │
│  │   • 즉시 에러 또는 폴백 반환                                          │   │
│  │   • 타임아웃 후 Half-Open으로 전이                                   │   │
│  │                                                                      │   │
│  │   장점:                                                              │   │
│  │   - 장애 서비스에 리소스 낭비 없음                                    │   │
│  │   - 빠른 실패로 사용자 경험 개선                                     │   │
│  │   - 장애 서비스 복구 시간 확보                                        │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  3. HALF-OPEN (반 열림 - 복구 시도 상태)                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   요청 ──▶ [서킷 브레이커] ──▶ 실제 서비스 호출 (제한적)              │   │
│  │                                                                      │   │
│  │   • 제한된 수의 요청만 통과                                          │   │
│  │   • 복구 여부 판단                                                   │   │
│  │   • 성공 → CLOSED, 실패 → OPEN                                      │   │
│  │                                                                      │   │
│  │   예시 설정:                                                         │   │
│  │   - 허용 요청: 3회                                                    │   │
│  │                                                                      │   │
│  │   시나리오 1: 복구 성공                                               │   │
│  │   요청1: 성공 ✓                                                      │   │
│  │   요청2: 성공 ✓                                                      │   │
│  │   요청3: 성공 ✓ → CLOSED로 전이 (완전 복구!)                          │   │
│  │                                                                      │   │
│  │   시나리오 2: 여전히 장애                                             │   │
│  │   요청1: 실패 ✗ → 즉시 OPEN으로 전이 (다시 차단)                       │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3. 임계값 설정 예시

| 설정 항목 | 설명 | 추천 값 | 영향 |
|:---------|:-----|:-------|:-----|
| **Failure Threshold** | 회로 열림을 위한 최소 실패 수 | 5-10회 | 너무 낮으면 잦은 오탐, 너무 높으면 늦은 대응 |
| **Failure Rate Threshold** | 실패율 임계값 | 40-60% | 비율 기반으로 일시적 장애 내성 |
| **Wait Duration** | OPEN에서 Half-Open까지 대기 시간 | 30-90초 | 너무 짧으면 복구 기간 부족, 길면 늦은 복구 |
| **Half-Open Max Calls** | 복구 시도 허용 요청 수 | 3-10회 | 충분한 샘플링 확보 |
| **Sliding Window Size** | 통계 계산 윈도우 크기 | 10-100회 | 정확도 vs 메모리 사용 |

---

## Ⅲ. 서킷 브레이커 구현

### 1. Resilience4j 예시 (Spring Boot)

```java
// 1. 의존성 추가
/*
dependencies {
    implementation 'io.github.resilience4j:resilience4j-spring-boot2:2.1.0'
    implementation 'io.github.resilience4j:resilience4j-circuitbreaker:2.1.0'
}
*/

// 2. 설정 (application.yml)
/*
resilience4j:
  circuitbreaker:
    instances:
      userService:  # 서킷 브레이커 이름
        registerHealthIndicator: true
        slidingWindowSize: 10
        minimumNumberOfCalls: 5
        permittedNumberOfCallsInHalfOpenState: 3
        automaticTransitionFromOpenToHalfOpenEnabled: true
        waitDurationInOpenState: 60s
        failureRateThreshold: 50
        recordExceptions:
          - java.io.IOException
          - java.util.concurrent.TimeoutException
        ignoreExceptions:
          - java.lang.IllegalArgumentException
*/

// 3. CircuitBreaker 사용
@Service
public class OrderService {

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private UserServiceFallback userServiceFallback;

    // 방법 1: Annotation 방식 (권장)
    @CircuitBreaker(
        name = "userService",
        fallbackMethod = "getUserFallback"
    )
    public User getUser(String userId) {
        return restTemplate.getForObject(
            "http://user-service/api/users/{id}",
            User.class,
            userId
        );
    }

    // Fallback 메서드 (같은 클래스 또는 별도 빈)
    private User getUserFallback(String userId, Exception ex) {
        // Fallback 로직
        log.warn("User service unavailable, using fallback for user: {}", userId);

        // 옵션 1: 캐시된 데이터 반환
        User cached = cacheService.getCachedUser(userId);
        if (cached != null) {
            return cached;
        }

        // 옵션 2: 기본값 반환
        return User.builder()
            .id(userId)
            .name("Unknown User")
            .status(UserStatus.SERVICE_UNAVAILABLE)
            .build();
    }

    // 방법 2: Programmatic 방식
    private final CircuitBreaker circuitBreaker;

    public OrderService() {
        CircuitBreakerConfig config = CircuitBreakerConfig.custom()
            .slidingWindowSize(10)
            .failureRateThreshold(50)
            .waitDurationInOpenState(Duration.ofSeconds(60))
            .permittedNumberOfCallsInHalfOpenState(3)
            .recordException(e -> {
                // IOException과 TimeoutException만 실패로 기록
                return e instanceof IOException || e instanceof TimeoutException;
            })
            .build();

        CircuitBreakerRegistry registry = CircuitBreakerRegistry.of(config);
        this.circuitBreaker = registry.circuitBreaker("userService");
    }

    public User getUserWithProgrammaticCB(String userId) {
        return CircuitBreaker.decorateSupplier(
            circuitBreaker,
            () -> restTemplate.getForObject(
                "http://user-service/api/users/{id}",
                User.class,
                userId
            )
        ).get();  // 또는 get() 대신 handle 예외
    }
}

// ========== 전용 Fallback Service ==========

@Service
public class UserServiceFallback {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private CacheManager cacheManager;

    public User getUserFromCache(String userId, Exception ex) {
        Cache cache = cacheManager.getCache("userCache");
        if (cache != null) {
            User cached = cache.get(userId, User.class);
            if (cached != null) {
                return cached;
            }
        }

        // 캐시 미스 시 기본값 반환
        return createDefaultUser(userId);
    }

    public User getUserFromLocalDB(String userId, Exception ex) {
        // 로컬 DB의 복제본 조회 (CQRS Read Model)
        return userRepository.findById(userId)
            .orElse(createDefaultUser(userId));
    }

    private User createDefaultUser(String userId) {
        return User.builder()
            .id(userId)
            .name("Service Temporarily Unavailable")
            .status(UserStatus.SERVICE_UNAVAILABLE)
            .build();
    }
}
```

### 2. 상태 모니터링

```java
@RestController
@RequestMapping("/actuator")
public class CircuitBreakerController {

    @Autowired
    private CircuitBreakerRegistry circuitBreakerRegistry;

    @GetMapping("/circuit-breakers")
    public Map<String, CircuitBreakerState> getCircuitBreakerStates() {
        Map<String, CircuitBreakerState> states = new HashMap<>();

        circuitBreakerRegistry.getAllCircuitBreakers().forEach(cb -> {
            CircuitBreakerMetrics metrics = cb.getMetrics();
            Map<String, Object> details = new HashMap<>();
            details.put("state", cb.getState());
            details.put("failureRate", metrics.getFailureRate());
            details.put("slowCallRate", metrics.getSlowCallRate());
            details.put("bufferedCalls", metrics.getNumberOfBufferedCalls());
            details.put("failedCalls", metrics.getNumberOfFailedCalls());
            details.put("notPermittedCalls", metrics.getNumberOfNotPermittedCalls());

            states.put(cb.getName(), cb.getState());
        });

        return states;
    }

    @GetMapping("/circuit-breakers/{name}/state")
    public Map<String, Object> getCircuitBreakerState(@PathVariable String name) {
        CircuitBreaker circuitBreaker = circuitBreakerRegistry.circuitBreaker(name);
        CircuitBreakerMetrics metrics = circuitBreaker.getMetrics();

        Map<String, Object> status = new HashMap<>();
        status.put("name", name);
        status.put("state", circuitBreaker.getState());
        status.put("failureRate", metrics.getFailureRate() + "%");
        status.put("failedCalls", metrics.getNumberOfFailedCalls());
        status.put("successCalls", metrics.getNumberOfSuccessfulCalls());
        status.put("rejectedCalls", metrics.getNumberOfNotPermittedCalls());

        return status;
    }

    @PostMapping("/circuit-breakers/{name}/reset")
    public String resetCircuitBreaker(@PathVariable String name) {
        CircuitBreaker circuitBreaker = circuitBreakerRegistry.circuitBreaker(name);
        circuitBreaker.transitionToClosedState();
        return "Circuit breaker '" + name + "' reset to CLOSED state";
    }
}
```

### 3. Spring Cloud Circuit Breaker (추상화)

```java
// Spring Cloud Circuit Breaker (Resilience4j 외에도 다른 구현체 사용 가능)

@Service
public class OrderService {

    @Autowired
    private CircuitBreakerFactory circuitBreakerFactory;

    @Autowired
    private ReactiveCircuitBreakerFactory reactiveCircuitBreakerFactory;

    // 동기 방식
    public User getUser(String userId) {
        CircuitBreaker circuitBreaker = circuitBreakerFactory.create("userService");

        return circuitBreaker.run(
            () -> restTemplate.getForObject(
                "http://user-service/api/users/{id}",
                User.class,
                userId
            ),
            throwable -> {
                // Fallback 로직
                log.error("User service call failed", throwable);
                return getFallbackUser(userId);
            }
        );
    }

    // 리액티브 방식
    public Mono<User> getUserReactive(String userId) {
        ReactiveCircuitBreaker circuitBreaker =
            reactiveCircuitBreakerFactory.create("userService");

        return circuitBreaker.execute(
            webClient.get()
                .uri("http://user-service/api/users/{id}", userId)
                .retrieve()
                .bodyToMono(User.class),
            throwable -> {
                // Fallback 로직
                return Mono.just(getFallbackUser(userId));
            }
        );
    }
}
```

---

## Ⅳ. 폴백(Fallback) 전략

### 1. 폴백 패턴

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        폴백 전략 패턴                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. 정적 응답 (Static Response)                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   fallback() {                                                       │   │
│  │     return User.builder()                                           │   │
│  │       .name("Service Temporarily Unavailable")                      │   │
│  │       .status("SERVICE_UNAVAILABLE")                                │   │
│  │       .build();                                                     │   │
│  │   }                                                                 │   │
│  │                                                                      │   │
│  │   장점: 단순함                                                       │   │
│  │   단점: 사용자 경험 저하                                             │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  2. 캐시된 데이터 (Cached Data)                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   fallback(userId) {                                                │   │
│  │     User cached = cache.get("user:" + userId);                     │   │
│  │     if (cached != null) {                                           │   │
│  │       cached.setStale(true);  // 오래된 데이터 표시                 │   │
│  │       return cached;                                               │   │
│  │     }                                                               │   │
│  │     throw new ServiceUnavailableException();                       │   │
│  │   }                                                                 │   │
│  │                                                                      │   │
│  │   장점: 어느 정도 최신성 유지                                         │   │
│  │   단점: 캐시가 없을 때 대응 어려움                                   │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  3. 대체 서비스 (Alternative Service)                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   fallback(userId) {                                                │   │
│  │     // 다른 공급자의 API 호출                                        │   │
│  │     return backupUserServiceClient.getUser(userId);                │   │
│  │   }                                                                 │   │
│  │                                                                      │   │
│  │   예: 외부 결제 API 장애 시 다른 PG사로 전환                           │   │
│  │                                                                      │   │
│  │   장점: 서비스 연속성                                                 │   │
│  │   단점: 추가 비용, 데이터 불일치 위험                                 │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  4. 로컬 복제본 (Local Replica)                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   fallback(userId) {                                                │   │
│  │     // CQRS Read Model (로컬 DB의 읽기 전용 복제본)                │   │
│  │     return localUserRepository.findById(userId)                   │   │
│  │       .orElseThrow(() -> new UserNotFoundException());              │   │
│  │   }                                                                 │   │
│  │                                                                      │   │
│  │   주의: 데이터 오래되었을 수 있음                                   │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  5. 큐잉 및 비동기 처리 (Queue & Async)                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   fallback(userId) {                                                │   │
│  │     // 나중에 처리를 위해 큐에 저장                                  │   │
│  │     messageQueue.publish(new GetUserRequest(userId));               │   │
│  │                                                                      │   │
│  │     return User.builder()                                          │   │
│  │       .id(userId)                                                  │   │
│  │       .status("PROCESSING")                                         │   │
│  │       .message("Request queued for processing")                    │   │
│  │       .build();                                                    │   │
│  │   }                                                                 │   │
│  │                                                                      │   │
│  │   장점: 요청 손실 방지, 복구 시 처리 가능                             │   │
│  │   단점: 즉시 결과 제공 불가                                          │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 계층형 폴백 전략

```java
@Service
public class HierarchicalFallbackService {

    @Autowired
    private CacheManager cacheManager;

    @Autowired
    private LocalUserRepository localRepository;

    @Autowired
    private BackupUserApiClient backupApiClient;

    @Autowired
    private MessageQueue messageQueue;

    public User getUserWithHierarchicalFallback(String userId, Exception ex) {
        // 1단계: 캐시 확인
        Cache cache = cacheManager.getCache("userCache");
        if (cache != null) {
            User cached = cache.get(userId, User.class);
            if (cached != null) {
                log.info("Returning cached user for {}", userId);
                return cached.withStaleFlag(true);
            }
        }

        // 2단계: 로컬 복제본 확인
        try {
            User local = localRepository.findById(userId).orElse(null);
            if (local != null) {
                log.info("Returning local replica for {}", userId);
                return local.withStaleFlag(true);
            }
        } catch (Exception e) {
            log.warn("Local repository also failed", e);
        }

        // 3단계: 대체 서비스 호출
        try {
            User backup = backupApiClient.getUser(userId);
            log.info("Returning backup API result for {}", userId);
            return backup;
        } catch (Exception e) {
            log.warn("Backup API also failed", e);
        }

        // 4단계: 큐잉 및 대기 응답
        try {
            messageQueue.publish(new GetUserRequest(userId));
            log.info("Request queued for {}", userId);
            return User.builder()
                .id(userId)
                .status("PROCESSING")
                .message("Request queued, will be processed shortly")
                .build();
        } catch (Exception e) {
            log.error("Even queue failed, giving up", e);
        }

        // 5단계: 최후의 수단 (에러)
        throw new ServiceUnavailableException(
            "All fallback options exhausted for user: " + userId, ex);
    }
}
```

---

## Ⅴ. 모니터링 및 운영

### 1. 메트릭 및 대시보드

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    서킷 브레이커 모니터링 지표                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  핵심 메트릭:                                                                │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   Circuit Breaker: user-service                                     │   │
│  │                                                                     │   │
│  │   State: CLOSED 🔋                                                 │   │
│  │                                                                     │   │
│  │   ┌─────────────────────────────────────────────────────────────┐  │   │
│  │   │  실패율 (Failure Rate)                                      │  │   │
│  │   │  ████████████████░░░░░░░░░░░░░  45.5%  (임계값: 50%)        │  │   │
│  │   │                                                             │  │   │
│  │   │  최근 호출 (Last 100 calls)                                │  │   │
│  │   │  성공: ████████████████████████  55                        │  │   │
│  │   │  실패: ████████████░░░░░░░░░░░░░  45                        │  │   │
│  │   │  거부: ░░░░░░░░░░░░░░░░░░░░░░░░░   0                        │  │   │
│  │   │                                                             │  │   │
│  │   │  슬라이딩 윈도우 통계                                       │  │   │
│  │   │  ┌─────────────────────────────────────────────────────┐   │  │   │
│  │   │  │ ● ○ ● ● ○ ● ● ● ● ○ ● ○ ● ● ○ ● ● ● ○ ○ ● ● ●     │   │  │   │
│  │   │  │ ●=성공 ○=실패                                       │   │  │   │
│  │   │  └─────────────────────────────────────────────────────┘   │  │   │
│  │   └─────────────────────────────────────────────────────────────┘  │   │
│  │                                                                     │   │
│  │   타임라인 (Last 1 hour):                                         │   │
│  │   ┌─────────────────────────────────────────────────────────────┐  │   │
│  │   │                                                             │  │   │
│  │   │  OPEN │                                             │ CLOSED│  │   │
│  │   │       ████                              ████               │  │   │
│  │   │  ─────┴──────────────────────────────────┴─────────────────  │  │   │
│  │   │        10:05                            10:15               │  │   │
│  │   │                                                             │  │   │
│  │   └─────────────────────────────────────────────────────────────┘  │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  알림 규칙 (Alerting Rules):                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   Warning: 실패율 > 40%                                              │   │
│  │   Critical: 서킷 OPEN 상태 지속 > 5분                                │   │
│  │   Critical: 거부된 호출 > 100/분                                     │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. Prometheus 통합

```yaml
# Prometheus 설정 예시
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'spring-boot-app'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['localhost:8080']

# Grafana 대시보드 쿼리 예시
# - 실패율: sum(rate(circuitbreaker_failure_total{service="user-service"}[5m])) / sum(rate(circuitbreaker_calls_total{service="user-service"}[5m])) * 100
# - 상태: circuitbreaker_state{service="user-service"} (0=CLOSED, 1=OPEN, 2=HALF_OPEN)
# - 거부된 호출: rate(circuitbreaker_not_permitted_calls_total[5m])
```

### 3. 장애 대응 절차

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    서킷 브레이커 장애 대응 Playbook                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  단계 1: 감지 (Detection)                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   ✓ PagerDuty/Slack 알림 수신                                       │   │
│  │   "user-service Circuit Breaker가 OPEN 상태입니다!"                  │   │
│  │                                                                      │   │
│  │   확인 사항:                                                         │   │
│  │   - 어느 서비스의 어떤 서킷인가?                                     │   │
│  │   - 언제부터 OPEN인가?                                              │   │
│  │   - 다른 서비스도 영향받고 있는가?                                   │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  단계 2: 원인 파악 (Root Cause Analysis)                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   확인 항목:                                                         │   │
│  │   1. 대상 서비스 로그: user-service 로그 확인                       │   │
│  │   2. 인프라 상태: DB, Redis, 메시지 큐 상태                         │   │
│  │   3. 메트릭: CPU, 메모리, 네트워크                                  │   │
│  │   4. 배포: 최근 배포로 인한 회귀?                                    │   │
│  │                                                                      │   │
│  │   원인 분류:                                                         │   │
│  │   - 서비스 장애 (애플리케이션 버그, OOM)                             │   │
│  │   - 인프라 장애 (DB 다운, 네트워크 단절)                            │   │
│  │   - 외부 의존성 (3rd Party API 장애)                                │   │
│  │   - 트래픽 급증 (DDoS, 이벤트)                                      │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  단계 3: 대응 (Response)                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   즉시 조치:                                                         │   │
│  │   1. 서비스 재시작 (hang 프로세스 해결)                              │   │
│  │   2. 롤백 (최근 배프로 회귀 확인 시)                                │   │
│  │   3. 오토스케일링 (리소스 부족 시)                                   │   │
│  │                                                                      │   │
│  │   폴백 확인:                                                         │   │
│  │   - 캐시 데이터가 유효한가?                                          │   │
│  │   - 대체 서비스가 정상인가?                                          │   │
│  │   - 로컬 복제본이 최신인가?                                          │   │
│  │                                                                      │   │
│  │   영향도 평가:                                                       │   │
│  │   - 사용자에게 보이는 에러 메시지 확인                                │   │
│  │   - 핵심 기능 영향도 판단                                            │   │
│  │   - 고객사 통지 필요성                                               │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  단계 4: 복구 (Recovery)                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   1. 근본 원인 해결                                                  │   │
│  │   2. Wait Duration 경과 대기 또는 수동 CLOSED로 전환                 │   │
│  │   3. Half-Open에서 트래픽 점진 증가                                 │   │
│  │   4. CLOSED로 복구 확인                                              │   │
│  │   5. 사후 포스트모템 (Postmortem) 작성                              │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 개념 맵

```
                    ┌─────────────────────┐
                    │  Circuit Breaker    │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   CLOSED     │      │    OPEN      │      │  HALF-OPEN   │
│  (정상 상태) │      │  (차단 상태) │      │ (복구 시도)   │
├──────────────┤      ├──────────────┤      ├──────────────┤
│ 요청 통과    │      │ 요청 차단    │      │ 제한적 통과  │
│ 성공/실패    │─────▶│ 폴백 반환    │─────▶│ 복구 확인     │
│ 카운트      │      │ 타이머 대기   │      │ 결과에 따라   │
│              │      │              │      │ 전이         │
└──────────────┘      └──────────────┘      └──────────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               ▼
                    ┌──────────────────┐
                    │   Fallback       │
                    │   전략          │
                    ├──────────────────┤
                    │ • 정적 응답     │
                    │ • 캐시된 데이터  │
                    │ • 대체 서비스   │
                    │ • 로컬 복제본   │
                    │ • 큐잉          │
                    └──────────────────┘
```

---

## 🎓 섹션 요약 비유 (어린이 설명)

### 🔌 서킷 브레이커는 "전기 차단기 같은 현명한 차단기"

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   🏠 우리 집에 여러 전기 기기가 연결되어 있어요:                               │
│                                                                             │
│   - 📺 TV                                                                 │
│   - ❄️ 에어컨                                                             │
│   - 💡 조명                                                                │
│   - 🖥️ 컴퓨터                                                              │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│   ❌ 나쁜 상황 (차단기 없음)                                                │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│      정전 ──▶ 전선 ──▶ 에어컨 ──▶ 합선! 🔥                                │
│                             │                                              │
│                             └──▶ 과부하!                                   │
│                                                                             │
│      "앗! 에어컨이 고장 나서 합선했어!"                                     │
│                                                                             │
│      문제:                                                                  │
│      - 에어컨만 문제인데...                                                │
│      - 전체 집 전기가 나가버려요! 💥                                        │
│      - TV도 꺼지고, 컴퓨터도 꺼지고...                                      │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│   ✅ 좋은 방법 (서킷 브레이커 = 차단기)                                      │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│      전력 ──▶ [차단기] ──▶ 에어컨 ──▶ 합선! 🔥                            │
│                      │          │                                          │
│                      └──▶ 감지!   │                                          │
│                                                                             │
│      "앗! 에어컨 쪽에서 과부하가 감지됐어!"                                 │
│                                                                             │
│      🛑 차단기 동작:                                                        │
│      ┌───────────────────────────────────────────────────────────────┐     │
│      │                                                                │     │
│      │   STEP 1: 에어컨 회로만 차단! (OPEN 상태)                        │     │
│      │                                                                │     │
│      │   전력 ──▶ [차단기] ──X─ 에어컨 (차단됨!)                        │     │
│      │              │                                                   │     │
│      │              └──▶ 다른 기기들은 정상 작동! ✓                      │     │
│      │                   • TV는 켜져 있고                                │     │
│      │                   • 조명도 켜져 있고                              │     │
│      │                   • 컴퓨터도 작동 중!                             │     │
│      │                                                                │     │
│      │   STEP 2: 잠시 후 복구 시도 (HALF-OPEN 상태)                      │     │
│      │                                                                │     │
│      │   "에어컨 고장 나갔어? 다시 전기 줘볼게..."                       │     │
│      │                                                                │     │
│      │   - 복구됐으면: 다시 사용 (CLOSED 상태) ✅                        │     │
│      │   - 여전히 문제: 계속 차단 (OPEN 상태) ❌                        │     │
│      │                                                                │     │
│      └───────────────────────────────────────────────────────────────┘     │
│                                                                             │
│   장점:                                                                    │
│   - 한 기기의 문제가 전체를 망치지 않아요!                                  │
│   - 문제 있는 기기만 빨리 차단하고, 나머지는 보호!                          │
│   - 자동으로 복구도 시도해 줘요!                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**핵심**: 서킷 브레이커는 집의 **"차단기"**와 같아요! 한 서비스가 문제가 생기면, 그 서비스만 빨리 차단해서 **다른 서비스까지 망가지지 않게 보호**해 줍니다. 그리고 나중에 **자동으로 복구도 시도**해 준답니다!

---

## 관련 키워드

- **MSA (Microservices Architecture)** (#163): 서킷 브레이커가 필요한 아키텍처
- **API Gateway** (#184): 서킷 브레이커를 적용하는 계층
- **폴백 (Fallback)** (#171): 서킷 브레이커와 함께 사용하는 대안 전략
- **재시도 (Retry)**: 서킷 브레이커와 함께 주의해서 사용
- **탄력적 설계 (Resilience)**: 서킷 브레이커가 속하는 내결함성 패턴
- **폴리글랏 퍼시스턴스** (#190): 각 서비스의 독립적 장애 격리
