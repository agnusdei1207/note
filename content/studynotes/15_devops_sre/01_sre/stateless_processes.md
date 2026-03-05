+++
title = "무상태 프로세스 (Stateless Processes) - 12-Factor App"
description = "클라우드 네이티브 환경에서 애플리케이션의 상태 비저장 설계 원칙, 수평적 확장과 고가용성 실현을 위한 심층 기술 백서"
date = 2024-05-15
[taxonomies]
tags = ["Stateless", "12-Factor App", "Horizontal Scaling", "Cloud Native", "Session Management", "Kubernetes"]
+++

# 무상태 프로세스 (Stateless Processes) - 12-Factor App 원칙

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 12-Factor App의 제6 원칙으로, **애플리케이션 프로세스가 내부 메모리에 상태(State)를 저장하지 않고, 모든 영속 데이터를 외부 백엔드 서비스(DB, 캐시)에 위임**함으로써 언제든지 프로세스를 추가/제거할 수 있는 수평 확장(Scale-out) 가능한 설계 원칙입니다.
> 2. **가치**: 무상태 설계를 통해 **트래픽 증가 시 즉시 인스턴스를 추가**하고, 장애 발생 시 **잔존 인스턴스가 트래픽을 분산 처리**하며, **롤링 업데이트 시 세션 손실 없이 무중단 배포**를 실현합니다.
> 3. **융합**: 쿠버네티스 HPA(Horizontal Pod Autoscaler), 세션 스토어(Redis), 스티키 세션(Sticky Session), External Session Store 패턴과 결합하여 탄력적 클라우드 아키텍처를 구현합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)

**무상태(Stateless)**란 애플리케이션의 **각 요청이 독립적**이며, 이전 요청의 정보에 의존하지 않는 설계 방식을 의미합니다. 구체적으로:

- **Stateless 프로세스**: 메모리(Heap, Session)에 사용자별 상태를 저장하지 않음
- **Stateless HTTP**: 각 HTTP 요청이 인증 토큰(JWT 등)을 포함하여 독립적으로 처리됨
- **공유 상태 금지**: 프로세스 간 메모리 공유 금지, 파일 시스템 의존 금지

12-Factor App은 "Execute the app as one or more stateless processes"라고 명시하며, 모든 상태를 **외부화(Externalize)** 할 것을 요구합니다:

| 상태 유형 | 상태 저장 위치 (Stateless 설계) |
| :--- | :--- |
| **세션 데이터** | Redis, Memcached (External Session Store) |
| **캐시** | Redis Cluster, CDNs |
| **파일 업로드** | S3, GCS, MinIO (Object Storage) |
| **사용자 설정** | Database (RDBMS, NoSQL) |
| **JWT 토큰** | 클라이언트 쿠키/로컬 스토리지 |

### 2. 구체적인 일상생활 비유

**햄버거 체인점**을 상상해 보세요:

**[상태 저장(Stateful) 방식 - 전통적 식당]**
- 단골손님이 "평소처럼"이라고 말하면, 주인이 기억을 떠올려요
- 주인이 아프면 대신할 사람이 그 기억을 모름
- 손님이 많아도 주인이 한 명이라 줄이 길어져요

**[무상태(Stateless) 방식 - 햄버거 체인]**
- 모든 주문이 **"햄버거 세트 A, 콜라 L"**처럼 명확히 적혀 있어요
- 어떤 직원이 주문을 받아도 동일하게 처리돼요
- 손님이 많으면 **직원을 더 투입**하면 돼요 (수평 확장)
- 한 직원이 아파도 **다른 직원이 바로 대체**해요 (고가용성)

### 3. 등장 배경 및 발전 과정

1. **기존 기술의 치명적 한계점 (상태 저장 서버)**:
   과거 웹 서버는 사용자 세션을 **서버 메모리(HttpSession)**에 저장했습니다:
   ```java
   // 안티패턴: 서버 메모리에 세션 저장
   HttpSession session = request.getSession();
   session.setAttribute("user", user);  // 메모리에 저장!
   session.setAttribute("cart", cart);  // 장바구니도 메모리!
   ```
   이 방식의 치명적 문제:
   - **확장 불가**: 사용자는 항상 **같은 서버**로 연결되어야 함 (Sticky Session)
   - **SPOF**: 서버가 죽으면 해당 서버의 모든 세션 손실
   - **메모리 부족**: 세션 데이터가 많아지면 OOM(Out of Memory) 발생

2. **혁신적 패러다임 변화의 시작**:
   2010년대 클라우드 컴퓨팅의 등장과 함께 **수평 확장(Scale-out)**이 필수가 되었습니다. 12-Factor App은:
   - "Any data that needs to persist must be stored in a stateful backing service"
   - 프로세스는 언제든 **생성/삭제**될 수 있어야 함
   - 로드밸런서가 어떤 프로세스로 요청을 보내든 동일한 결과

3. **현재 시장/산업의 비즈니스적 요구사항**:
   쿠버네티스 환경에서는:
   - 파드(Pod)가 언제든 **스케줄링에 의해 다른 노드로 이동**할 수 있음
   - 오토스케일링(HPA)이 트래픽에 따라 파드 수를 자동 조절
   - 이 모든 것이 **세션 손실 없이** 이루어져야 함

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **JWT (JSON Web Token)** | 클라이언트에 세션 정보 저장 | 사용자 정보를 암호화하여 토큰화, 클라이언트가 보관 | RFC 7519, HMAC/RSA | 손님의 회원증 |
| **External Session Store** | 세션 데이터 중앙 저장 | Redis/Memcached에 세션을 Key-Value로 저장 | Redis Protocol, Memcached | 중앙 물품 보관소 |
| **Load Balancer** | 트래픽 분산 | 라운드 로빈/Least Conn으로 요청 분배 | L4/L7, HAProxy, ALB | 매니저가 직원 분배 |
| **Sticky Session** | 동일 사용자를 동일 서버로 라우팅 | 쿠키/Source IP 해시로 라우팅 고정 | Cookie, IP Hash | 단골손님 전담 직원 |
| **Connection Pool** | DB 연결 재사용 | Stateless 앱이 DB 연결을 풀링 | HikariCP, c3p0 | 공구 대여소 |

### 2. 정교한 구조 다이어그램: Stateless Architecture

```text
=====================================================================================================
                    [ 12-Factor Stateless Processes Architecture ]
=====================================================================================================

                              [ CLIENTS ]
                    ┌─────────────┬─────────────┬─────────────┐
                    │   Browser   │   Mobile    │   IoT       │
                    │   (JWT)     │   App       │   Device    │
                    └─────────────┴─────────────┴─────────────┘
                              │
                              │ HTTP Request with JWT Token
                              ▼
    +-------------------------------------------------------------------------------------------+
    |                              [ LOAD BALANCER ]                                            |
    |                           (AWS ALB / Nginx / HAProxy)                                     |
    |                                                                                           |
    |  +-----------------------------------------------------------------------------------+   |
    |  │ Routing Rules:                                                                    │   |
    |  │ - Round Robin (Stateless Default)                                                │   |
    |  │ - No Session Affinity (Sticky Session OFF)                                       │   |
    |  │ - Health Check: /actuator/health                                                 │   |
    +-------------------------------------------------------------------------------------------+
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼
    +------------+      +------------+      +------------+
    |   Pod A    │      |   Pod B    │      |   Pod C    │
    |            │      |            │      |            │
    │ [PROCESS]  │      │ [PROCESS]  │      │ [PROCESS]  │
    │ Stateless  │      │ Stateless  │      │ Stateless  │
    │            │      │            │      │            │
    │ NO MEMORY  │      │ NO MEMORY  │      │ NO MEMORY  │
    │ SESSION!   │      │ SESSION!   │      │ SESSION!   │
    +------------+      +------------+      +------------+
           │                  │                  │
           │                  │                  │
           └──────────────────┼──────────────────┘
                              │
                              │ Read/Write State from External Stores
                              ▼
    +-------------------------------------------------------------------------------------------+
    |                              [ STATEFUL BACKING SERVICES ]                                |
    |                                                                                           |
    |  +-------------------+     +-------------------+     +-------------------+               |
    |  | SESSION STORE     |     | DATABASE          |     | CACHE             |               |
    |  |                   |     |                   |     |                   |               |
    |  | [Redis Cluster]   │     | [PostgreSQL]      │     | [Redis Cluster]   |               |
    |  |                   |     │                   |     │                   |               |
    |  │ Session Data:     │     │ User Data:        │     │ Cache Data:       │               |
    |  │ {                 │     │ - id, email       │     │ - product_list    │               |
    |  │   "userId": 123,  │     │ - preferences     │     │ - rate_limit      │               |
    |  │   "cart": [...]   │     │ - orders          │     │ - temp_tokens     │               |
    |  │ }                 │     │                   |     │                   |               |
    |  +-------------------+     +-------------------+     +-------------------+               |
    |                                                                                           |
    +-------------------------------------------------------------------------------------------+

    =====================================================================================================
       Key Principle: Any Pod Can Handle Any Request
       ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
       │ Request 1: User A -> Pod A -> Reads session from Redis -> Returns response                 │
       │ Request 2: User A -> Pod B -> Reads SAME session from Redis -> Returns SAME response       │
       │ Request 3: User A -> Pod C -> Reads SAME session from Redis -> Returns SAME response       │
       │                                                                                             │
       │ Result: User doesn't notice which pod handled their request!                               │
       └─────────────────────────────────────────────────────────────────────────────────────────────┘
    =====================================================================================================
```

### 3. 심층 동작 원리: Stateless 요청 처리 메커니즘

**1단계: JWT 기반 인증 (토큰에 상태 저장)**

```java
// JWT 토큰 생성 및 검증
@Component
public class JwtTokenProvider {

    @Value("${jwt.secret}")
    private String secretKey;

    // 토큰 생성: 사용자 정보를 토큰에 인코딩
    public String createToken(User user) {
        Claims claims = Jwts.claims().setSubject(user.getEmail());
        claims.put("userId", user.getId());
        claims.put("roles", user.getRoles());

        return Jwts.builder()
            .setClaims(claims)
            .setIssuedAt(new Date())
            .setExpiration(new Date(System.currentTimeMillis() + 3600000)) // 1시간
            .signWith(SignatureAlgorithm.HS256, secretKey)
            .compact();
    }

    // 토큰 검증: 서버 메모리 조회 없이 토큰만으로 인증
    public Authentication getAuthentication(String token) {
        Claims claims = Jwts.parser()
            .setSigningKey(secretKey)
            .parseClaimsJws(token)
            .getBody();

        // 토큰에서 사용자 정보 추출 (DB 조회 없이!)
        Long userId = claims.get("userId", Long.class);

        return new UsernamePasswordAuthenticationToken(
            userId, null, authorities
        );
    }
}

// Stateless Security 설정
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)  // 세션 생성 안 함!
            .and()
            .addFilterBefore(new JwtAuthenticationFilter(jwtTokenProvider),
                UsernamePasswordAuthenticationFilter.class);
    }
}
```

**2단계: 외부 세션 스토어 (Redis) 사용**

```java
// Spring Session + Redis로 세션 외부화
@Configuration
@EnableRedisHttpSession  // 세션을 Redis에 저장
public class SessionConfig {

    @Bean
    public LettuceConnectionFactory connectionFactory(
        @Value("${redis.host}") String host,
        @Value("${redis.port}") int port
    ) {
        return new LettuceConnectionFactory(host, port);
    }
}

// 세션 사용 예시 (Redis에 자동 저장)
@RestController
@RequestMapping("/api/cart")
public class CartController {

    // 세션을 Redis에 저장하므로 어떤 Pod에서도 동일한 세션 접근 가능
    @PostMapping("/add")
    public ResponseEntity<?> addToCart(
        @RequestBody CartItem item,
        HttpSession session  // Spring이 자동으로 Redis 세션으로 연결
    ) {
        Cart cart = (Cart) session.getAttribute("cart");
        if (cart == null) {
            cart = new Cart();
        }
        cart.addItem(item);
        session.setAttribute("cart", cart);  // Redis에 저장됨!
        return ResponseEntity.ok(cart);
    }
}
```

**3단계: Kubernetes HPA (수평적 자동 확장)**

```yaml
# Horizontal Pod Autoscaler - 트래픽에 따라 파드 자동 증감
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  minReplicas: 3
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
  behavior:  # 스케일 다운 안정화
    scaleDown:
      stabilizationWindowSeconds: 300  # 5분 대기 후 축소
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60  # 1분에 최대 10%만 축소
```

**4단계: 무상태 로직 구현 패턴**

```java
// 무상태 서비스 구현 예시
@Service
public class OrderService {

    private final OrderRepository orderRepository;
    private final RedisTemplate<String, Object> redisTemplate;
    private final KafkaTemplate<String, String> kafkaTemplate;

    // 상태 비저장: 모든 데이터는 DB 또는 Redis에서 조회
    public Order createOrder(OrderRequest request, Long userId) {
        // 1. 캐시에서 사용자 정보 조회 (없으면 DB)
        User user = getUserFromCacheOrDb(userId);

        // 2. 주문 생성 (메모리에 저장하지 않음)
        Order order = Order.builder()
            .userId(userId)
            .items(request.getItems())
            .totalAmount(calculateTotal(request))
            .status(OrderStatus.CREATED)
            .createdAt(Instant.now())
            .build();

        // 3. DB에 영속화
        Order savedOrder = orderRepository.save(order);

        // 4. 이벤트 발행 (다른 서비스에 알림)
        kafkaTemplate.send("order-created", savedOrder.toJson());

        return savedOrder;
    }

    // 캐시-aside 패턴: 캐시 미스 시 DB 조회 후 캐시에 저장
    private User getUserFromCacheOrDb(Long userId) {
        String cacheKey = "user:" + userId;

        // 1. 캐시 조회
        User cachedUser = (User) redisTemplate.opsForValue().get(cacheKey);
        if (cachedUser != null) {
            return cachedUser;
        }

        // 2. DB 조회
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new UserNotFoundException(userId));

        // 3. 캐시에 저장 (TTL 1시간)
        redisTemplate.opsForValue().set(cacheKey, user, Duration.ofHours(1));

        return user;
    }
}
```

### 4. 실무 코드 예시: 세션 스티키 vs Stateless 비교

```java
// [안티패턴] Stateful: 서버 메모리에 세션 저장
@RestController
public class StatefulController {

    // 문제: 이 Map은 해당 서버에만 존재
    private Map<String, UserSession> sessions = new ConcurrentHashMap<>();

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest request) {
        // 메모리에 세션 저장 -> 다른 서버에서 접근 불가!
        String sessionId = UUID.randomUUID().toString();
        sessions.put(sessionId, new UserSession(request.getUsername()));
        return ResponseEntity.ok(Map.of("sessionId", sessionId));
    }

    @GetMapping("/profile")
    public ResponseEntity<?> getProfile(@RequestHeader("X-Session-Id") String sessionId) {
        // 이 서버에만 세션이 있음 -> 다른 Pod에서는 null
        UserSession session = sessions.get(sessionId);
        if (session == null) {
            return ResponseEntity.status(401).body("Session not found");
        }
        return ResponseEntity.ok(session);
    }
}

// [모범 패턴] Stateless: JWT 토큰 사용
@RestController
public class StatelessController {

    @Autowired
    private JwtTokenProvider jwtTokenProvider;

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest request) {
        // 토큰에 모든 정보 저장 -> 서버 메모리 불필요
        User user = authenticate(request);
        String token = jwtTokenProvider.createToken(user);
        return ResponseEntity.ok(Map.of("token", token));
    }

    @GetMapping("/profile")
    public ResponseEntity<?> getProfile(@RequestHeader("Authorization") String authHeader) {
        // 토큰만으로 인증 -> 어떤 서버에서든 동작
        String token = authHeader.replace("Bearer ", "");
        Authentication auth = jwtTokenProvider.getAuthentication(token);
        return ResponseEntity.ok(auth.getPrincipal());
    }
}
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. Stateful vs Stateless 비교표

| 평가 지표 | Stateful (상태 저장) | Stateless (무상태) |
| :--- | :--- | :--- |
| **확장성** | 낮음 (Sticky Session 필요) | 높음 (어떤 인스턴스든 처리) |
| **고가용성** | 낮음 (서버 장애 시 세션 손실) | 높음 (세션이 외부에 저장) |
| **메모리 사용** | 높음 (세션이 서버 메모리 차지) | 낮음 (세션이 외부 저장소) |
| **복잡도** | 낮음 (단순 구현) | 중간 (JWT/외부 스토어 필요) |
| **지연 시간** | 낮음 (메모리 직접 접근) | 높음 (네트워크 조회 필요) |
| **롤링 업데이트** | 어려움 (세션 드레이닝 필요) | 쉬움 (바로 교체 가능) |

### 2. 세션 관리 전략 비교

| 전략 | 설명 | 장점 | 단점 | 적합한 상황 |
| :--- | :--- | :--- | :--- | :--- |
| **In-Memory** | 서버 메모리에 저장 | 구현 간단, 빠름 | 확장 불가, 장애 취약 | 단일 서버, 개발 환경 |
| **Sticky Session** | 로드밸런서가 사용자 고정 | 기존 코드 수정 적음 | 서버 불균형, SPOF | 레거시 마이그레이션 |
| **External Store** | Redis/Memcached 사용 | 확장 가능, 고가용성 | 네트워크 지연 | 대규모 프로덕션 |
| **JWT** | 클라이언트에 토큰 저장 | 서버 저장 불필요 | 토큰 크기, 폐기 어려움 | RESTful API, MSA |

### 3. 과목 융합 관점 분석

**Stateless + 쿠버네티스 (HPA)**
- 무상태 설계가 HPA의 전제 조건
- CPU/메모리 메트릭에 따라 파드 자동 증감
- 롤링 업데이트 시 세션 손실 없음

**Stateless + 마이크로서비스**
- 서비스 간 호출이 상태를 가지지 않음
- API Gateway에서 JWT 검증 후 내부 서비스는 Stateless
- 서비스 메시(Istio)가 인증/인가 처리

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 레거시 Stateful 애플리케이션의 Stateless 전환**
- **문제점**: 기존 HttpSession을 사용하는 앱을 쿠버네티스로 이관해야 함.
- **기술사 판단**: **Spring Session + Redis로 세션 외부화**
  1. `@EnableRedisHttpSession` 추가
  2. Redis 연결 설정 (환경 변수로 주입)
  3. 기존 `session.getAttribute()` 코드는 수정 불필요
  4. 테스트: 여러 파드에서 동일 세션 접근 확인

**[상황 B] 대규모 트래픽의 JWT 토큰 크기 최적화**
- **문제점**: JWT에 너무 많은 클레임을 담아 토큰 크기가 커짐 (네트워크 오버헤드).
- **기술사 판단**: **Reference Token + Redis 캐시**
  ```java
  // 토큰에는 최소 정보만 (userId)
  String token = createMinimalToken(userId);

  // 상세 정보는 Redis에서 조회
  User user = redisTemplate.opsForValue().get("user:" + userId);
  ```

### 2. 도입 시 고려사항 체크리스트

**무상태 설계 체크리스트**
- [ ] 모든 세션이 외부 저장소(Redis)에 저장되는가?
- [ ] 파일 업로드가 로컬 디스크가 아닌 S3에 저장되는가?
- [ ] JWT 토큰의 만료 시간이 적절한가? (너무 길면 보안 위험)
- [ ] 토큰 폐기(로그아웃) 메커니즘이 있는가? (Redis 블랙리스트)

**확장성 체크리스트**
- [ ] HPA가 트래픽 증가에 자동 반응하는가?
- [ ] 파드 추가 시 워밍업 없이 바로 트래픽 처리 가능한가?
- [ ] 롤링 업데이트 중 세션 손실이 없는가?

### 3. 주의사항 및 안티패턴

**안티패턴 1: JWT에 민감 정보 저장**
```java
// 잘못된 예: JWT에 비밀번호 저장
claims.put("password", user.getPassword());  // 위험!

// 올바른 예: 최소 정보만 저장
claims.put("userId", user.getId());
claims.put("roles", user.getRoles());
```

**안티패턴 2: 파일 시스템에 상태 저장**
```java
// 잘못된 예: 로컬 파일에 세션 저장
File sessionFile = new File("/tmp/sessions/" + sessionId);

// 올바른 예: S3 또는 DB에 저장
s3Client.putObject(bucketName, sessionKey, sessionData);
```

**안티패턴 3: 싱글톤에 상태 저장**
```java
// 잘못된 예: 싱글톤에 사용자별 상태 저장
public class UserCache {
    private Map<Long, User> users = new HashMap<>();  // 메모리 누수 위험!
}

// 올바른 예: 캐시 라이브러리 사용 (TTL 지원)
@Cacheable(value = "users", key = "#userId")
public User getUser(Long userId) {
    return userRepository.findById(userId);
}
```

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | Stateful (AS-IS) | Stateless (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **확장 시간** | 서버 프로비저닝 (수십 분) | 파드 추가 (수십 초) | **90% 단축** |
| **장애 복구** | 세션 복구 불가 (재로그인) | 세션 유지 (무중단) | **가용성 99.9%+** |
| **롤링 업데이트** | 세션 드레이닝 필요 | 즉시 교체 가능 | **배포 시간 80% 단축** |
| **메모리 효율** | 세션이 Heap 점유 | 외부 저장소 사용 | **서버 메모리 50% 절감** |

### 2. 미래 전망 및 진화 방향

**서버리스(FaaS)와의 결합**
- AWS Lambda, Cloud Functions는 기본적으로 Stateless
- 콜드 스타트 문제를 해결하기 위한 상태 최소화 설계 필수

**Edge Computing**
- CDN 엣지에서 JWT 검증으로 Origin 서버 부하 감소
- 글로벌 분산 세션 스토어 (DynamoDB Global Tables)

### 3. 참고 표준/가이드
- **The Twelve-Factor App (12factor.net/processes)**: Processes 원칙
- **JWT.io (RFC 7519)**: JSON Web Token 표준
- **Spring Session Documentation**: 세션 외부화 구현 가이드
- **Kubernetes HPA Documentation**: 수평적 파드 오토스케일러

---

## 관련 개념 맵 (Knowledge Graph)
- **[12-Factor App](@/studynotes/15_devops_sre/01_sre/twelve_factor_app.md)**: 무상태 프로세스를 포함한 전체 방법론
- **[백엔드 서비스 (Backing Services)](./backing_services.md)**: 세션/캐시를 저장하는 외부 서비스
- **[쿠버네티스 오토스케일링](@/studynotes/13_cloud_architecture/01_native/kubernetes.md)**: HPA를 통한 수평 확장
- **[API Gateway](./api_gateway.md)**: JWT 검증 및 인증 처리
- **[Redis 캐시](@/studynotes/07_database/02_nosql/redis.md)**: 세션 스토어로 활용

---

## 어린이를 위한 3줄 비유 설명
1. 햄버거 가게에서 **직원이 손님의 주문을 기억하는 것**과 **주문서에 적어놓는 것**의 차이예요.
2. 직원이 기억하면(상태 저장) 그 직원이 쉬는 날에는 주문을 몰라요. 하지만 **주문서(외부 저장소)**에 적어두면 **어떤 직원**이 봐도 알 수 있죠!
3. 이렇게 하면 손님이 많을 때 **직원을 더 투입**해도 아무 문제 없어요. 컴퓨터도 이렇게 **기억을 외부에 맡겨서** 일해요!
