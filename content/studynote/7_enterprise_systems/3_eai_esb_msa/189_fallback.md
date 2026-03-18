+++
title = "189. 폴백 (Fallback)"
date = "2026-03-18"
[extra]
category = "studynote-enterprise"
keywords = ["Fallback", "폴백", "Circuit Breaker", "Resilience", "MSA", "장애 조치", "대안 전략"]
+++

# 폴백 (Fallback)

> **Fallback**: 서비스 장애 또는 성능 저하 시 **주요 기능을 대신 수행할 수 있는 대안 경로**를 제공하여 시스템의 가용성을 유지하고 사용자 경험을 개선하는 내결함성 패턴으로, 서킷 브레이커와 함께 사용되어 **"빠른 실패(Fail Fast)"**가 아닌 **"우아한 성능 저하(Graceful Degradation)"**를 가능하게 합니다

## 핵심 인사이트

모든 시스템은 장애가 발생합니다. 중요한 것은 **"장애가 발생했을 때 어떻게 대응하는가?"**입니다. **폴백(Fallback)**은 **"Plan B"**를 미리 준비하는 전략입니다. 사용자 서비스가 응답하지 않으면, 캐시된 데이터를 반환하거나, 로컬 데이터베이스의 복제본을 조회하거나, 대체 서비스로 전환합니다. 완벽한 정상 상태는 아니지만, **서비스가 완전히 중단되는 것보다 낮은 품질이라도 계속 제공**하는 것이 핵심입니다. "100% 완벽함"을 추구하다 실패하는 것보다, **"80%의 성능"으로라도 계속 운영**하는 것이 현실적입니다.

---

## Ⅰ. 개념 정의 및 목적

### 1. 폴백의 정의

**폴백(Fallback)**은 주요 기능이 실패했을 때 실행되는 **대안 동작(Alternative Behavior)**을 의미합니다.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    폴백의 기본 개념                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   🎯 목표: "완벽함 대신 지속성"                                             │
│                                                                             │
│   ❌ 폴백 없는 시스템                                                       │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │  │
│  │   사용자 요청 ──▶ 서비스 호출 ──X 장애 발생!                         │  │
│  │                                      │                              │  │
│  │                                      ▼                              │  │
│  │                              😱 에러 화면                            │  │
│  │                              "서비스를 이용할 수 없습니다."            │  │
│  │                                                                      │  │
│  │   결과:                                                              │  │
│  │   - 사용자 경험: 최악                                                │  │
│  │   - 비즈니스 손실: 100%                                              │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   ✅ 폴백 있는 시스템                                                       │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │  │
│  │   사용자 요청 ──▶ 서비스 호출 ──X 장애 발생!                         │  │
│  │                                      │                              │  │
│  │                                      ▼                              │  │
│  │                              🔄 폴백 실행                            │  │
│  │                                      │                              │  │
│  │                    ┌─────────────────┴─────────────────┐             │  │
│  │                    │                                   │             │  │
│  │                    ▼                                   ▼             │  │
│  │            캐시된 데이터                          대체 서비스        │  │
│  │            (약간 오래됨)                          (느리지만 작동)     │  │
│  │                                                                      │  │
│  │   결과:                                                              │  │
│  │   - 사용자 경험: 일부 저하되지만 서비스 제공 ✅                      │  │
│  │   - 비즈니스 손실: 최소화                                             │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 폴백의 목적

| 목적 | 설명 | 비즈니스 가치 |
|:-----|:-----|:-------------|
| **가용성 유지** | 완전 중단 대신 저품질 서비스 제공 | 수익 손실 방지 |
| **사용자 경험 개선** | 빠른 에러 대신 의미있는 응답 | 이탈률 감소 |
| **장애 격리** | 하위 서비스 장애가 상위로 전파 방지 | 연쇄 장애 방지 |
| **자동 복구** | 장애 복구 시 자동으로 정상 경로 전환 | 운영 부하 감소 |
| **SLA 준수** | 부분적 기능으로라도 SLA 충족 | 계약 위반 방지 |

### 3. 우아한 성능 저하(Graceful Degradation)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              우아한 성능 저하 계층 구조                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Layer 1: 완벽한 기능 (100%)                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 실시간 데이터                                                     │  │
│  │   • 모든 기능 활성화                                                 │  │
│  │   • 최고 성능                                                        │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │ 장애 발생 시                               │
│                              ▼                                            │
│   Layer 2: 약간 저하된 기능 (80%)                                          │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 캐시된 데이터 (약간 오래됨)                                      │  │
│  │   • 일부 기능 비활성화                                               │  │
│  │   • 여전히 쓸만한 수준                                               │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │ 추가 장애 시                               │
│                              ▼                                            │
│   Layer 3: 최소한의 기능 (50%)                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 로컬 복제본 (많이 오래됨)                                        │  │
│  │   • 핵심 기능만 제공                                                 │  │
│  │   • 기본값 반환                                                       │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │ 완전 장애 시                               │
│                              ▼                                            │
│   Layer 4: 에러 메시지 (0%)                                                │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • "서비스 일시 중단" 메시지                                        │  │
│  │   • 예상 복구 시간 안내                                              │  │
│  │   • 대안 안내                                                         │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   "폴백은 가능한 한 높은 레이어를 유지하는 전략!"                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 폴백 전략 유형

### 1. 정적 응답(Static Response)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    정적 응답 폴백                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  사용 사례: 데이터 정확성이 중요하지 않은 경우                               │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   @CircuitBreaker(name = "inventoryService",                         │   │
│  │       fallbackMethod = "getInventoryFallback")                        │   │
│  │   )                                                                   │   │
│  │   public Inventory getInventory(String productId) {                  │   │
│  │       return inventoryService.getStock(productId);                   │   │
│  │   }                                                                   │   │
│  │                                                                      │   │
│  │   public Inventory getInventoryFallback(String productId,             │   │
│  │                                         Exception ex) {              │   │
│  │       // 정적 응답 반환                                               │   │
│  │       return Inventory.builder()                                     │   │
│  │           .productId(productId)                                      │   │
│  │           .quantity(0)  // 재고 없음으로 표시                         │   │
│  │           .status("UNKNOWN")  // 상태 불확실                          │   │
│  │           .lastUpdated("Service temporarily unavailable")             │   │
│  │           .build();                                                  │   │
│  │   }                                                                   │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   장점:                                                                   │
│   - 매우 단순함                                                           │
│   - 추가 의존성 없음                                                       │
│   - 항상 응답 보장                                                         │
│                                                                             │
│   단점:                                                                   │
│   - 사용자 경험 저하                                                       │
│   - 데이터 부정확                                                          │
│                                                                             │
│   적합한 경우:                                                             │
│   - 재고 확인 (0으로 표시하여 주문 방지)                                   │
│   - 추천 시스템 (기본 추천 제공)                                           │
│   - 비핵심 기능                                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 캐시된 데이터(Cached Data)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    캐시된 데이터 폴백                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  사용 사례: 데이터의 빈도(Recency)가 중요하지 않은 경우                      │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   public User getUserFallback(String userId, Exception ex) {        │   │
│  │       // 1. 캐시 확인                                               │   │
│  │       User cached = cacheManager.get("user:" + userId, User.class);  │   │
│  │                                                                      │   │
│  │       if (cached != null) {                                          │   │
│  │           // 캐시 히트: 오래된 데이터임을 표시                       │   │
│  │           cached.setStale(true);                                     │   │
│  │           cached.setCacheTimestamp(Instant.now());                   │   │
│  │           log.info("Returning cached user for {}", userId);          │   │
│  │           return cached;                                             │   │
│  │       }                                                               │   │
│  │                                                                      │   │
│  │       // 2. 캐시 미스: 정적 응답                                     │   │
│  │       return User.builder()                                          │   │
│  │           .id(userId)                                               │   │
│  │           .name("Unknown")                                           │   │
│  │           .status(UserStatus.SERVICE_UNAVAILABLE)                    │   │
│  │           .build();                                                 │   │
│  │   }                                                                   │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   캐시 전략:                                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │  │
│  │   @Cacheable(value = "users", key = "#userId",                       │  │
│  │              unless = "#result == null")                             │  │
│  │   public User getUser(String userId) {                              │  │
│  │       return userRepository.findById(userId);                        │  │
│  │   }                                                                  │  │
│  │                                                                      │  │
│  │   설정:                                                              │  │
│  │   - TTL: 5분 (짧게 유지하여 최신성 확보)                              │  │
│  │   - 최대 크기: 10,000 엔트리                                          │  │
│  │   - 제거 정책: LRU (Least Recently Used)                             │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   장점:                                                                   │
│   - 어느 정도 최신성 유지                                                 │
│   - 빠른 응답 시간                                                       │
│   - 사용자 경험 양호                                                      │
│                                                                             │
│   단점:                                                                   │
│   - 캐시가 없을 때 대응 어려움                                           │
│   - 메모리 사용                                                           │
│                                                                             │
│   적합한 경우:                                                             │
│   - 사용자 프로필                                                         │
│   - 상품 정보                                                             │
│   - 카탈로그 데이터                                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3. 로컬 복제본(Local Replica)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    로컬 복제본 폴백 (CQRS Read Model)                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  사용 사례: CQRS 패턴에서 분리된 읽기 전용 복제본 활용                      │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   ┌────────────────┐    이벤트     ┌────────────────┐               │   │
│  │   │  Command DB    │─────────────▶│  Event Store   │               │   │
│  │   │   (Write)      │               │                │               │   │
│  │   └────────────────┘               └────────┬───────┘               │   │
│  │                                             │                       │   │
│  │                                      구독    │                       │   │
│  │                                             ▼                       │   │
│  │                                    ┌────────────────┐               │   │
│  │                                    │  Read DB       │               │   │
│  │                                    │  (Local Replica)│              │   │
│  │                                    └────────┬───────┘               │   │
│  │                                             │                       │   │
│  │                                             │ 조회                  │   │
│  │                                             ▼                       │   │
│  │   폴백 시 로컬 Read DB 조회                                          │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   public Order getOrderFallback(String orderId, Exception ex) {     │   │
│  │       // CQRS Read Model (이벤트 소싱으로 구축된 로컬 복제본)        │   │
│  │       try {                                                           │   │
│  │           Order localOrder = readModelRepository.findById(orderId);  │   │
│  │                                                                      │   │
│  │           if (localOrder != null) {                                  │   │
│  │               // 오래된 데이터임을 명시                               │   │
│  │               localOrder.setSource("LOCAL_REPLICA");                  │   │
│  │               localOrder.setStale(true);                              │   │
│  │               localOrder.setLastSyncTime(                             │   │
│  │                   readModelRepository.getLastSyncTime());             │   │
│  │                                                                      │   │
│  │               log.warn("Returning local replica for order {}",        │   │
│  │                        orderId);                                      │   │
│  │               return localOrder;                                      │   │
│  │           }                                                           │   │
│  │       } catch (Exception e) {                                          │   │
│  │           log.error("Local replica also failed", e);                  │   │
│  │       }                                                               │   │
│  │                                                                      │   │
│  │       // 로컬 복제본도 없으면 기본값 반환                             │   │
│  │       return Order.builder()                                          │   │
│  │           .id(orderId)                                              │   │
│  │           .status("UNKNOWN")                                         │   │
│  │           .build();                                                  │   │
│  │   }                                                                   │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   이벤트 소싱 기반 동기화:                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │  │
│  │   // OrderCreated 이벤트 처리                                        │  │
│  │   @EventHandler                                                      │  │
│  │   public void handle(OrderCreated event) {                          │  │
│  │       // Read Model 업데이트                                         │  │
│  │       OrderReadModel readModel = new OrderReadModel();              │  │
│  │       readModel.setOrderId(event.getOrderId());                     │  │
│  │       readModel.setCustomerId(event.getCustomerId());               │  │
│  │       readModel.setTotalAmount(event.getTotalAmount());              │  │
│  │       readModel.setCreatedAt(event.getCreatedAt());                 │  │
│  │       readModelRepository.save(readModel);                          │  │
│  │   }                                                                  │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   장점:                                                                   │
│   - 최대한 최신성 유지 (이벤트 기반 동기화)                                 │
│   - 메인 DB 장애 시에도 읽기 가능                                         │
│   - 조회 성능 최적화                                                      │
│                                                                             │
│   단점:                                                                   │
│   - 복잡한 아키텍처 (CQRS, Event Sourcing 필요)                            │
│   - 데이터 동기화 지연                                                     │
│   - 저장소 비용 2배                                                        │
│                                                                             │
│   적합한 경우:                                                             │
│   - 주문 내역                                                           │
│   - 거래 기록                                                           │
│   - 로그 및 감사 데이터                                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4. 대체 서비스(Alternative Service)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    대체 서비스 폴백                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  사용 사례: 여러 공급자 또는 지리적 중복 배포                               │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   @CircuitBreaker(name = "paymentGatewayPrimary",                    │   │
│  │       fallbackMethod = "processPaymentFallback")                      │   │
│  │   )                                                                   │   │
│  │   public PaymentResult processPayment(PaymentRequest request) {      │   │
│  │       return primaryPaymentGateway.charge(request);                   │   │
│  │   }                                                                   │   │
│  │                                                                      │   │
│  │   public PaymentResult processPaymentFallback(                        │   │
│  │           PaymentRequest request, Exception ex) {                    │   │
│  │                                                                      │   │
│  │       log.warn("Primary payment gateway failed, trying backup", ex);  │   │
│  │                                                                      │   │
│  │       // 대체 결제 대행사로 전환                                       │   │
│  │       try {                                                           │   │
│  │           PaymentResult result =                                      │   │
│  │               backupPaymentGateway.charge(request);                   │   │
│  │                                                                      │   │
│  │           // 대체 서비스임을 표시                                     │   │
│  │           result.setGateway("BACKUP");                                │   │
│  │           result.setFallbackUsed(true);                               │   │
│  │                                                                      │   │
│  │           log.info("Successfully processed via backup gateway");      │   │
│  │           return result;                                              │   │
│  │                                                                      │   │
│  │       } catch (Exception backupEx) {                                  │   │
│  │           log.error("Backup gateway also failed", backupEx);          │   │
│  │           // 두 번째 폴백: 큐잉                                       │   │
│  │           return queueForLaterProcessing(request);                   │   │
│  │       }                                                               │   │
│  │   }                                                                   │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   다중 공급자 구성:                                                         │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │  │
│  │   @Configuration                                                     │  │
│  │   public class PaymentGatewayConfig {                               │  │
│  │                                                                      │  │
│  │       @Bean                                                          │  │
│  │       @Primary                                                      │  │
│  │       public PaymentGateway primaryGateway() {                       │  │
│  │           return new StripePaymentGateway();                          │  │
│  │       }                                                              │  │
│  │                                                                      │  │
│  │       @Bean                                                          │  │
│  │       public PaymentGateway backupGateway() {                         │  │
│  │           return new TossPaymentsGateway();                           │  │
│  │       }                                                              │  │
│  │                                                                      │  │
│  │       @Bean                                                          │  │
│  │       public PaymentGateway tertiaryGateway() {                       │  │
│  │           return new KakaoPayGateway();                               │  │
│  │       }                                                              │  │
│  │   }                                                                  │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   장점:                                                                   │
│   - 서비스 연속성 보장                                                     │
│   - 단일 지점 장애(SPOF) 해소                                              │
│   - 비교적 원활한 전환                                                    │
│                                                                             │
│   단점:                                                                   │
│   - 추가 비용 (여러 공급자 계약)                                           │
│   - 데이터 일관성 이슈                                                     │
│   - 통합 복잡도                                                           │
│                                                                             │
│   적합한 경우:                                                             │
│   - 결제 게이트웨이                                                       │
│   - SMS/이메일 발송                                                      │
│   - 지도/위치 API                                                        │
│   - 클라우드 스토리지 (Multi-Cloud)                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5. 비동기 큐잉(Async Queuing)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    비동기 큐잉 폴백                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  사용 사례: 즉시 결과가 필요 없는 경우, 나중에 처리 가능                      │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   public ReportResult generateReport(ReportRequest request) {        │   │
│  │       try {                                                           │   │
│  │           // 동기 처리 (정상)                                         │   │
│  │           ReportResult result = reportingService.generate(request);   │   │
│  │           result.setProcessingMethod("SYNC");                         │   │
│  │           return result;                                              │   │
│  │                                                                      │   │
│  │       } catch (Exception ex) {                                        │   │
│  │           log.warn("Sync reporting failed, queuing for later", ex);   │   │
│  │           return queueForLater(request);                              │   │
│  │       }                                                               │   │
│  │   }                                                                   │   │
│  │                                                                      │   │
│  │   private ReportResult queueForLater(ReportRequest request) {        │   │
│  │       try {                                                           │   │
│  │           // 메시지 큐에 등록                                          │   │
│  │           String messageId = messageQueue.publish(                    │   │
│  │               "report.requests",                                     │   │
│  │               request                                                 │   │
│  │           );                                                          │   │
│  │                                                                      │   │
│  │           // 즉시 응답 (처리 대기 중)                                  │   │
│  │           return ReportResult.builder()                              │   │
│  │               .reportId(messageId)                                   │   │
│  │               .status("QUEUED")                                      │   │
│  │               .processingMethod("ASYNC_QUEUED")                       │   │
│  │               .message("Report queued for processing. " +            │   │
│  │                        "Will be available shortly.")                 │   │
│  │               .estimatedCompletionTime(                             │   │
│  │                   Instant.now().plusSeconds(300))  // 5분 후        │   │
│  │               .build();                                              │   │
│  │                                                                      │   │
│  │       } catch (QueueException e) {                                    │   │
│  │           // 큐조차 실패: 마지막 수단                                 │   │
│  │           log.error("Even queuing failed, giving up", e);            │   │
│  │           throw new ServiceUnavailableException(                      │   │
│  │               "Unable to process report at this time. Please try " +  │   │
│  │               "again later.", e);                                     │   │
│  │       }                                                               │   │
│  │   }                                                                   │   │
│  │                                                                      │   │
│  │   // 큐 컨슈머 (백그라운드 처리)                                       │   │
│  │   @RabbitListener(queues = "report.requests")                        │   │
│  │   public void processQueuedReport(ReportRequest request) {            │   │
│  │       try {                                                           │   │
│  │           ReportResult result = reportingService.generate(request);   │   │
│  │                                                                      │   │
│  │           // 완료 알림 (이메일, 웹훅 등)                              │   │
│  │           notificationService.notifyCompletion(                      │   │
│  │               request.getRequesterEmail(),                           │   │
│  │               result                                                 │   │
│  │           );                                                          │   │
│  │                                                                      │   │
│  │           // 결과 저장                                               │   │
│  │           reportResultRepository.save(result);                       │   │
│  │                                                                      │   │
│  │       } catch (Exception ex) {                                        │   │
│  │           log.error("Failed to process queued report: {}",            │   │
│  │               request.getId(), ex);                                   │   │
│  │           // DLQ(Dead Letter Queue)로 이동                             │   │
│  │           deadLetterQueue.send(request);                              │   │
│  │       }                                                               │   │
│  │   }                                                                   │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   장점:                                                                   │
│   - 요청 손실 방지                                                         │
│   - 장애 복구 시 처리 가능                                                │
│   - 부하 평탄화(Peak Smoothing)                                           │
│                                                                             │
│   단점:                                                                   │
│   - 즉시 결과 제공 불가                                                    │
│   - 큐 인프라 추가                                                        │
│   - 순서 보장 어려움                                                       │
│                                                                             │
│   적합한 경우:                                                             │
│   - 리포트 생성                                                           │
│   - 배치 작업                                                             │
│   - 이메일 발송                                                           │
│   - 알림 푸시                                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 계층형 폴백 전략

### 1. 다중 폴백 체인

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    계층형 폴백 체인                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   목표: 가능한 한 최상의 대안을 제공                                         │
│                                                                             │
│   @Service                                                                 │
│   public class HierarchicalFallbackService {                               │
│                                                                             │
│       public User getUser(String userId) {                                 │
│           try {                                                             │
│               return primaryUserService.get(userId);                       │
│           } catch (ServiceUnavailableException ex) {                       │
│               return fallbackChain.execute(userId, ex);                   │
│           }                                                                 │
│       }                                                                     │
│                                                                             │
│       private FallbackChain<User> fallbackChain = FallbackChain            │
│           .<User>builder()                                                │
│           .addFallback(this::tryCache)                // 1순위            │
│           .addFallback(this::tryLocalReplica)        // 2순위            │
│           .addFallback(this::tryBackupService)        // 3순위            │
│           .addFallback(this::returnStaticDefault)     // 4순위(최후)    │
│           .build();                                                        │
│                                                                             │
│       // 1순위: 캐시된 데이터                                                │
│       private User tryCache(String userId, Exception ex) {                  │
│           User cached = cache.get("user:" + userId);                       │
│           if (cached != null) {                                            │
│               log.info("Fallback Level 1: Cache hit for {}", userId);       │
│               return cached.withStaleFlag(true);                           │
│           }                                                                 │
│           throw new FallbackException("Cache miss");                       │
│       }                                                                     │
│                                                                             │
│       // 2순위: 로컬 복제본                                                 │
│       private User tryLocalReplica(String userId, Exception ex) {           │
│           try {                                                             │
│               User local = localReadModel.findById(userId);                │
│               if (local != null) {                                         │
│                   log.info("Fallback Level 2: Local replica for {}",       │
│                            userId);                                         │
│                   return local.withStaleFlag(true);                        │
│               }                                                             │
│           } catch (Exception e) {                                          │
│               log.warn("Local replica failed", e);                          │
│           }                                                                 │
│           throw new FallbackException("Local replica failed");             │
│       }                                                                     │
│                                                                             │
│       // 3순위: 대체 서비스                                                 │
│       private User tryBackupService(String userId, Exception ex) {         │
│           try {                                                             │
│               User backup = backupUserService.get(userId);                 │
│               log.info("Fallback Level 3: Backup service for {}",          │
│                        userId);                                            │
│               return backup.withSource("BACKUP_SERVICE");                  │
│           } catch (Exception e) {                                          │
│               log.warn("Backup service also failed", e);                   │
│           }                                                                 │
│           throw new FallbackException("Backup service failed");            │
│       }                                                                     │
│                                                                             │
│       // 4순위: 최후의 수단 (정적 기본값)                                    │
│       private User returnStaticDefault(String userId, Exception ex) {      │
│           log.error("All fallbacks exhausted, returning default for {}",   │
│                      userId);                                              │
│           return User.builder()                                            │
│               .id(userId)                                                 │
│               .name("Service Temporarily Unavailable")                    │
│               .status(UserStatus.SERVICE_UNAVAILABLE)                      │
│               .build();                                                   │
│       }                                                                     │
│   }                                                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 폴백 품질 수준(Fallback Quality Levels)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│               폴백 품질에 따른 사용자 경험 계층                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   🟢 Quality Level 1: 거의 완벽 (95%+ 품질)                                 │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 캐시된 데이터 (TTL 1분 이내)                                     │  │
│  │   • 로컬 복제본 (초 단위 동기화)                                    │  │
│  │   • 대체 서비스 (동일 기능)                                         │  │
│  │                                                                      │  │
│  │   사용자 경험:                                                       │  │
│  │   - 차이를 거의 느끼지 못함                                           │  │
│  │   - UI에 "약간 오래된 데이터일 수 있습니다" 메시지                    │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │ 장애 지속 시                               │
│                              ▼                                            │
│   🟡 Quality Level 2: 사용 가능 (70-95% 품질)                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 캐시된 데이터 (TTL 5-10분)                                      │  │
│  │   • 로컬 복제본 (분 단위 동기화)                                    │  │
│  │   • 축소 기능 (일부 기능 제한)                                       │  │
│  │                                                                      │  │
│  │   사용자 경험:                                                       │  │
│  │   - 일부 기능 제한됨을 인지                                          │  │
│  │   - UI에 "일부 기능이 제한됩니다" 메시지                              │  │
│  │   - 여전히 핵심 기능 작동                                            │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │ 장애 심화 시                               │
│                              ▼                                            │
│   🟠 Quality Level 3: 최소 기능 (40-70% 품질)                               │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 캐시된 데이터 (TTL 1시간 이상)                                   │  │
│  │   • 로컬 복제본 (시간 단위 동기화)                                  │  │
│  │   • 정적 기본값                                                       │  │
│  │                                                                      │  │
│  │   사용자 경험:                                                       │  │
│  │   - 데이터가 오래되었음을 명확히 인식                                │  │
│  │   - UI에 "최신 정보가 아닙니다" 강력 표시                            │  │
│  │   - 핵심 기능만 작동                                                 │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │ 완전 장애 시                               │
│                              ▼                                            │
│   🔴 Quality Level 4: 에러 메시지 (0% 기능)                                │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 명시적인 에러 메시지                                             │  │
│  │   • 예상 복구 시간 안내                                              │  │
│  │   • 대안 경로 제시                                                   │  │
│  │                                                                      │  │
│  │   사용자 경험:                                                       │  │
│  │   - 명확한 상황 인지                                                  │  │
│  │   - 언제 복구될지 예상                                                 │  │
│  │   - 불만 최소화                                                       │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 폴백 구현 패턴

### 1. Annotation 기반 폴백

```java
// Spring Cloud Circuit Breaker + Fallback

@Service
public class UserServiceClient {

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private UserFallbackService fallbackService;

    // 단일 폴백 메서드
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

    // 폴백 메서드 (반드시 같은 클래스 또는 별도 빈)
    private User getUserFallback(String userId, Exception ex) {
        return fallbackService.getCachedUser(userId);
    }

    // ========== 여러 예외 타입별 다른 폴백 ==========

    @CircuitBreaker(name = "paymentService")
    @Retry(name = "paymentService")  // 재시도 후 폴백
    public Payment processPayment(PaymentRequest request) {
        return paymentGateway.charge(request);
    }

    // 타임아웃 시 폴백
    private Payment processPaymentTimeoutFallback(
            PaymentRequest request,
            TimeoutException ex) {
        log.warn("Payment timeout, queueing for later: {}", request.getId());
        return paymentQueueService.enqueue(request);
    }

    // 서버 오류 시 폴백
    private Payment processPaymentServerErrorFallback(
            PaymentRequest request,
            HttpServerErrorException ex) {
        log.warn("Payment server error, trying backup gateway");
        return backupPaymentGateway.charge(request);
    }

    // 클라이언트 오류 시 폴백 (재시도 안 함)
    private Payment processPaymentClientErrorFallback(
            PaymentRequest request,
            HttpClientErrorException ex) {
        // 클라이언트 오류는 재시도해도 실패하므로 바로 에러 반환
        throw new PaymentValidationException(
            "Invalid payment request: " + ex.getMessage(),
            ex
        );
    }
}
```

### 2. 템플릿 메서드 패턴

```java
// 폴백 로직의 재사용 가능한 템플릿

@Component
public class FallbackTemplate<T> {

    @Autowired
    private CacheManager cacheManager;

    @Autowired
    private LocalReplicaRepository localRepository;

    public T executeWithFallback(
            String cacheKey,
            Supplier<T> primaryOperation,
            Function<String, T> staticFallback) {

        // 1차: 주요 동작 시도
        try {
            T result = primaryOperation.get();
            // 성공 시 캐시 업데이트
            updateCache(cacheKey, result);
            return result;

        } catch (Exception primaryEx) {
            log.warn("Primary operation failed, trying fallbacks", primaryEx);

            // 2차: 캐시 확인
            T cached = getCachedValue(cacheKey);
            if (cached != null) {
                log.info("Returning cached value for {}", cacheKey);
                return cached;
            }

            // 3차: 로컬 복제본 확인
            try {
                T local = localRepository.findByKey(cacheKey);
                if (local != null) {
                    log.info("Returning local replica for {}", cacheKey);
                    return local;
                }
            } catch (Exception localEx) {
                log.warn("Local replica also failed", localEx);
            }

            // 최후: 정적 폴백
            log.error("All fallbacks exhausted, returning static value");
            return staticFallback.apply(cacheKey);
        }
    }

    private void updateCache(String key, Object value) {
        Cache cache = cacheManager.getCache("fallbackCache");
        if (cache != null) {
            cache.put(key, value);
        }
    }

    @SuppressWarnings("unchecked")
    private T getCachedValue(String key) {
        Cache cache = cacheManager.getCache("fallbackCache");
        return cache != null ? cache.get(key, (Class<T>) Object.class) : null;
    }
}

// 사용 예시
@Service
public class OrderService {

    @Autowired
    private FallbackTemplate<User> userFallbackTemplate;

    public User getUser(String userId) {
        return userFallbackTemplate.executeWithFallback(
            "user:" + userId,
            () -> userServiceClient.getUser(userId),  // 주요 동작
            (key) -> User.builder()                    // 정적 폴백
                .id(userId)
                .name("Unknown")
                .status(UserStatus.SERVICE_UNAVAILABLE)
                .build()
        );
    }
}
```

---

## Ⅴ. 폴백 모니터링 및 운영

### 1. 폴백 메트릭

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    폴백 모니터링 대시보드                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   Fallback Metrics: User Service                                     │  │
│  │                                                                     │  │
│  │   ┌───────────────────────────────────────────────────────────────┐ │  │
│  │   │  Fallback Rate (폴백 사용률)                                  │ │  │
│  │   │  ████████░░░░░░░░░░░░░░░░░░  12.3%  (지난 1시간)              │ │  │
│  │   │  Alert Threshold: > 20%                                       │  │
│  │   └───────────────────────────────────────────────────────────────┘ │  │
│  │                                                                     │  │
│  │   ┌───────────────────────────────────────────────────────────────┐ │  │
│  │   │  Fallback Sources (폴백 출처별 분포)                          │ │  │
│  │   │                                                             │ │  │
│  │   │  Cache Hit          ████████████████░░░░░░  75%               │ │  │
│  │   │  Local Replica      ████░░░░░░░░░░░░░░░░░░░░  15%               │ │  │
│  │   │  Backup Service    ███░░░░░░░░░░░░░░░░░░░░░   8%               │ │  │
│  │   │  Static Default    ░░░░░░░░░░░░░░░░░░░░░░░   2%               │ │  │
│  │   │                                                             │ │  │
│  │   └───────────────────────────────────────────────────────────────┘ │  │
│  │                                                                     │  │
│  │   ┌───────────────────────────────────────────────────────────────┐ │  │
│  │   │  Fallback Latency (폴백 응답 시간)                            │ │  │
│  │   │                                                             │ │  │
│  │   │  Cache:           ▂▃▅▇█  5ms (P50), 15ms (P95)             │ │  │
│  │   │  Local Replica:   ▂▃▅▇▂▃▅▇█  25ms (P50), 80ms (P95)          │ │  │
│  │   │  Backup Service: ▂▃▅█  150ms (P50), 450ms (P95)             │ │  │
│  │   │  Static:          ▂█  1ms (P50), 2ms (P95)                  │ │  │
│  │   │                                                             │ │  │
│  │   └───────────────────────────────────────────────────────────────┘ │  │
│  │                                                                     │  │
│  │   ┌───────────────────────────────────────────────────────────────┐ │  │
│  │   │  Staleness by Source (데이터 신선도)                         │ │  │
│  │   │                                                             │ │  │
│  │   │  Cache:          Avg 2 min old, Max 10 min old               │  │
│  │   │  Local Replica:  Avg 5 min old, Max 30 min old               │  │
│  │   │  Backup Service: Real-time                                   │  │
│  │   │                                                             │ │  │
│  │   └───────────────────────────────────────────────────────────────┘ │  │
│  │                                                                     │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 폴백 품질 개선 사이클

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              폴백 효과성 분석 및 개선 사이클                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1. 수집 (Collect)                                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 폴백 사용 빈도                                                     │  │
│  │   • 각 폴백 경로의 응답 시간                                          │  │
│  │   • 데이터 신선도 (Age)                                               │  │
│  │   • 사용자 불만 티켓                                                  │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                            │
│                              ▼                                            │
│   2. 분석 (Analyze)                                                         │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 어떤 폴백 경로가 가장 효과적인가?                                 │  │
│  │   • 폴백 데이터의 신선도가 허용 가능한가?                             │  │
│  │   • 사용자 경험에 미치는 영향은?                                      │  │
│  │   • 비용 대비 효과는?                                                  │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                            │
│                              ▼                                            │
│   3. 최적화 (Optimize)                                                     │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • 캐시 TTL 조정 (신선도 vs 히트율)                                 │  │
│  │   • 로컬 복제본 동기 주기 조정                                        │  │
│  │   • 대체 서비스 우선순위 재조정                                       │  │
│  │   • 폴백 체인 순서 변경                                               │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                            │
│                              ▼                                            │
│   4. 검증 (Validate)                                                       │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   • A/B 테스트로 개선 효과 검증                                      │  │
│  │   • 카나리 배포로 점진적 롤아웃                                       │  │
│  │   • 사용자 피드백 수집                                               │  │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 개념 맵

```
                    ┌─────────────────────┐
                    │     Fallback        │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ 데이터 소스   │      │  계층형      │      │  품질 수준   │
│  기반 전략   │      │  폴백 체인   │      │  관리        │
├──────────────┤      ├──────────────┤      ├──────────────┤
│ • 캐시된     │      │ 1순위: 캐시  │      │ Q1: 95%+     │
│   데이터     │      │ 2순위: 로컬  │      │ Q2: 70-95%   │
│ • 로컬 복제본│      │ 3순위: 대체  │      │ Q3: 40-70%   │
│ • 대체 서비스│      │ 4순위: 정적  │      │ Q4: 0%       │
│ • 비동기 큐  │      │              │      │              │
└──────────────┘      └──────────────┘      └──────────────┘
```

---

## 🎓 섹션 요약 비유 (어린이 설명)

### 🎭 우산 비유

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   ☔ 비가 올 때 준비된 우산 여러 개                                          │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│   ❌ 우산 없는 경우                                                         │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│         👤 아이                                                             │
│             │ "비가 와!"                                                   │
│             ▼                                                             │
│         😰💦💦💦 "아앗! 옷 다 젖었어!"                                        │
│                                                                             │
│   결과: 엄마한테 혼남, 감기 걸림                                              │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│   ✅ 우산이 여러 개 있는 경우 (폴백 전략)                                    │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│         👤 아이                                                             │
│             │ "비가 와! 우산 쓸까?"                                        │
│             ▼                                                             │
│         🌂 1단계 우산                                                      │
│           "제일 좋은 우산 쓸까?"                                           │
│              │                                                             │
│              ▼                                                             │
│           ✅ 작동! (완벽하게 보호)                                          │
│                                                                             │
│         ─────────────────────────────────────────                         │
│                                                                             │
│         만약 1단계 우산이 망가졌다면?                                       │
│                                                                             │
│         👤 아이                                                             │
│             │ "1단계 우산 망가졌어! 2단계!"                                │
│             ▼                                                             │
│         🌂 2단계 우산 (약간 낡았지만 작동)                                │
│           "약간 비 맞을 수도 있어..."                                     │
│              │                                                             │
│              ▼                                                             │
│           🌦️ 비가 좔 조금 맞지만 괜찮아!                                  │
│                                                                             │
│         ─────────────────────────────────────────                         │
│                                                                             │
│         만약 2단계도 망가졌다면?                                            │
│                                                                             │
│         👤 아이                                                             │
│             │ "2단계도 망가졌어! 3단계!"                                  │
│             ▼                                                             │
│         🧥 3단계: 코트로 대신                                             │
│           "코트 입고 머리로 비 피할게!"                                   │
│              │                                                             │
│              ▼                                                             │
│           🌦️🌦️ 조금 더 맞지만 그래도 안 젖어!                            │
│                                                                             │
│         ─────────────────────────────────────────                         │
│                                                                             │
│         만약 3단계도 안 되면?                                              │
│                                                                             │
│         👤 아이                                                             │
│             │ "모든 방법 다 안 돼..."                                      │
│             ▼                                                             │
│         🏪 빨리 매장으로 들어가기                                          │
│           "엄마, 비 와서 빨리 들어왔어!"                                   │
│              │                                                             │
│              ▼                                                             │
│           🏠 안전하게 보호됨!                                               │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│   이게 바로 폴백이에요!                                                    │
│                                                                             │
│   • 1단계 우산 = 완벽한 정상 서비스                                         │
│   • 2단계 우산 = 캐시된 데이터 (약간 오래되지만 괜찮아)                      │
│   • 3단계 코트 = 로컬 복제본 (더 오래됐지만 그래도 있어)                      │
│   • 매장으로 = 비동기 큐잉 (나중에 처리)                                    │
│                                                                             │
│   "완벽하진 않아도, 최대한 보호하는 게 폴백예요!"                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**핵심**: 폴백은 **"여러 개의 우산"**을 준비하는 것과 같아요! 첫 번째 우산이 망가져도, 두 번째, 세 번째 우산이 있어서 비를 맞을 수 있죠. 완벽하진 않아도, **아무것도 없는 것보다는 훨씬 나아요!**

---

## 관련 키워드

- **서킷 브레이커** (#188): 폴백과 함께 사용되는 주요 패턴
- **CQRS** (#179): 로컬 복제본 폴백의 기반이 되는 패턴
- **이벤트 소싱** (#180): 로컬 복제본 동기화 메커니즘
- **데이터베이스 퍼 서비스** (#191): 독립적인 DB로 폴백 구현 가능
- **내결함성(Resilience)**: 폴백이 속하는 더 큰 개념
