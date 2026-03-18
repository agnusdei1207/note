+++
title = "187. 클라이언트 사이드 vs 서버 사이드 디스커버리"
date = "2026-03-18"
[extra]
category = "studynote-enterprise"
keywords = ["Client-side Discovery", "Server-side Discovery", "Service Discovery", "Load Balancer", "MSA", "Eureka", "AWS ALB"]
+++

# 클라이언트 사이드 vs 서버 사이드 디스커버리

> **Service Discovery 패턴**: 마이크로서비스 환경에서 서비스 인스턴스를 검색하는 두 가지 주요 접근 방식으로, **클라이언트 사이드 디스커버리**는 호출자가 직접 레지스트리에서 인스턴스 목록을 조회하고 선택하는 반면, **서버 사이드 디스커버리**는 로드 밸런서가 중계하여 클라이언트는 단일 진입점만 알면 되는 상반된 아키텍처 패턴

## 핵심 인사이트

서비스 디스커버리에는 **"누가 서비스 인스턴스를 선택하는가?"**라는 근본적인 설계 결정이 있습니다. **클라이언트 사이드**는 호출하는 서비스가 스마트하게 결정(Netflix 스타일)하고, **서버 사이드**는 중앙 로드 밸런서가 대신 결정(AWS/쿠버네티스 스타일)합니다. 전자는 클라이언트가 복잡해지지만 유연성이 높고, 후자는 클라이언트가 단순해지지만 중앙 의존성이 발생합니다. 선택은 팀 구조, 인프라 환경, 운영 복잡도의 균형(Trade-off)에 달려 있습니다.

---

## Ⅰ. 개념 정의 및 비교

### 1. 두 패턴의 기본 차이

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              클라이언트 사이드 vs 서버 사이드 디스커버리 비교                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📊 의사결정 포인트: "서비스 인스턴스를 누가 선택하는가?"                     │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │  Client-Side Discovery           Server-Side Discovery               │   │
│  │  (클라이언트 사이드)               (서버 사이드)                      │   │
│  │                                                                      │   │
│  │     ┌──────────────┐                 ┌──────────────┐                │   │
│  │     │   호출자     │                 │   호출자     │                │   │
│  │     │  (Smart)     │                 │   (Dumb)     │                │   │
│  │     └──────┬───────┘                 └──────┬───────┘                │   │
│  │            │                                 │                        │   │
│  │            │ 1. 조회                         │ 1. 요청                │   │
│  │            ▼                                 ▼                        │   │
│  │     ┌──────────────┐                 ┌──────────────┐                │   │
│  │     │  Service     │                 │   Load       │                │   │
│  │     │  Registry    │                 │  Balancer    │                │   │
│  │     └──────┬───────┘                 └──────┬───────┘                │   │
│  │            │ 2. 인스턴스 목록                  │ 2. 조회               │   │
│  │            ▼                                 ▼                        │   │
│  │     ┌──────────────┐                 ┌──────────────┐                │   │
│  │     │   로드       │                 │  Service     │                │   │
│  │     │  밸런싱      │                 │  Registry    │                │   │
│  │     │  (내장)      │                 └──────┬───────┘                │   │
│  │     └──────┬───────┘                        │                         │   │
│  │            │ 3. 선택/호스트                   │ 3. 선택                │   │
│  │            ▼                                 ▼                        │   │
│  │     ┌───────────────────────────────────────────────────┐            │   │
│  │     │              서비스 인스턴스                       │            │   │
│  │     │   Instance-1  Instance-2  Instance-3              │            │   │
│  │     └───────────────────────────────────────────────────┘            │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  핵심 질문: "로드 밸런싱 책임이 누구에게 있는가?"                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 상세 비교표

| 비교 항목 | 클라이언트 사이드 디스커버리 | 서버 사이드 디스커버리 |
|:---------|:-------------------------|:---------------------|
| **결정 주체** | 호출하는 클라이언트 | 중앙 로드 밸런서 |
| **레지스트리 역할** | 인스턴스 목록 제공 | 로드 밸런서가 조회 |
| **클라이언트 복잡도** | 높음 (디스커버리 + LB 로직) | 낮음 (단일 URL만 알면 됨) |
| **네트워크 홉** | 2홉 (Registry → Instance) | 2홉 (LB → Instance) |
| **성능** | 추가 홉 없음 | LB 통과 오버헤드 |
| **장애 영향** | Registry 장애 시 새 인스턴스 발견 불가 | LB 장애 시 모든 호출 불가 |
| **유연성** | 높음 (클라이언트가 알고리즘 선택) | 낮음 (LB 정책에 종속) |
| **운영 부담** | 각 클라이언트 업데이트 필요 | LB만 수정하면 됨 |
| **대표 도구** | Eureka, Consul, Zookeeper | AWS ALB, Nginx, K8s Service |
| **채택 사례** | Netflix OSS | AWS, K8s, GCP |

---

## Ⅱ. 클라이언트 사이드 디스커버리

### 1. 아키텍처 상세

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  클라이언트 사이드 디스커버리 상세 흐름                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  시나리오: 주문 서비스가 사용자 서비스를 호출                                │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   Step 1: Order Service 시작 시 레지스트리 캐싱                     │   │
│  │   ┌──────────────────────────────────────────────────────────────┐  │   │
│  │   │                                                              │  │   │
│  │   │   ┌──────────────────┐                                      │  │   │
│  │   │   │ Order Service    │                                      │  │   │
│  │   │   │ (Client App)     │                                      │  │   │
│  │   │   │                  │   앱 시작 시                        │  │   │
│  │   │   │                  │◀────────────────────────              │  │   │
│  │   │   └────────┬─────────┘   전체 레지스트리 다운로드             │  │   │
│  │   │            │            (주기적 갱신: 30초)                  │  │   │
│  │   │            │                                              │  │   │
│  │   │            ▼                                              │  │   │
│  │   │   ┌──────────────────────────────────────────────────────┐ │  │   │
│  │   │   │  Service Registry (Eureka)                          │ │  │   │
│  │   │   │  {                                                   │ │  │   │
│  │   │   │    "user-service": [                                 │ │  │   │
│  │   │   │      {"host": "10.244.1.5", "port": 8080},           │ │  │   │
│  │   │   │      {"host": "10.244.1.6", "port": 8080},           │ │  │   │
│  │   │   │      {"host": "10.244.2.10", "port": 8080}           │ │  │   │
│  │   │   │    ]                                                 │ │  │   │
│  │   │   │  }                                                   │ │  │   │
│  │   │   └──────────────────────────────────────────────────────┘ │  │   │
│  │   │                                                              │  │   │
│  │   └──────────────────────────────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  │   Step 2: 사용자 요청 도래                                          │   │
│  │   ┌──────────────────────────────────────────────────────────────┐  │   │
│  │   │                                                              │  │   │
│  │   │   📱 고객: "내 주문 내역의 사용자 정보를 알려줘!"             │  │   │
│  │   │          ↓                                                  │  │   │
│  │   │   Order Service.getUser(userId) 호출                        │  │   │
│  │   │          ↓                                                  │  │   │
│  │   │   ┌────────────────────────────────────────────────┐        │  │   │
│  │   │   │                                                │        │  │   │
│  │   │   │  // 1. 로컬 캐시된 레지스트리에서 조회           │        │  │   │
│  │   │   │  List<Instance> instances =                      │        │  │   │
│  │   │   │    localCache.get("user-service");               │        │  │   │
│  │   │   │                                                │        │  │   │
│  │   │   │  // 2. 로드 밸런싱 알고리즘으로 선택               │        │  │   │
│  │   │   │  Instance chosen = loadBalancer.choose(          │        │  │   │
│  │   │   │    instances,                                     │        │  │   │
│  │   │   │    RoundRobinWithWeightStrategy                  │        │  │   │
│  │   │   │  );                                              │        │  │   │
│  │   │   │                                                │        │  │   │
│  │   │   │  // 3. 직접 호출 (프록시 개입 없음!)            │        │  │   │
│  │   │   │  String url = "http://" + chosen.host +         │        │  │   │
│  │   │   │    ":" + chosen.port + "/users/" + userId;      │        │  │   │
│  │   │   │  User user = restTemplate.getForObject(url);    │        │  │   │
│  │   │   │                                                │        │  │   │
│  │   │   └────────────────────────────────────────────────┘        │  │   │
│  │   │                                                              │  │   │
│  │   └──────────────────────────────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 클라이언트 사이드 디스커버리 구현

```java
// Spring Cloud Eureka를 활용한 클라이언트 사이드 디스커버리

// 1. 의존성 설정
/*
dependencies {
    implementation 'org.springframework.cloud:spring-cloud-starter-netflix-eureka-client'
    implementation 'org.springframework.cloud:spring-cloud-starter-loadbalancer'
}
*/

// 2. 설정
@Configuration
public class ServiceConfig {

    // 로드 밸런서가 적용된 RestTemplate 빈
    @Bean
    @LoadBalanced  // 이 어노테이션이 핵심!
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}

// 3. 서비스 호출 (매우 단순해짐)
@Service
public class OrderService {

    @Autowired
    private RestTemplate restTemplate;

    public User getUser(String userId) {
        // 서비스 이름으로만 호출! (디스커버리 + LB 자동)
        // http://user-service → Eureka에서 목록 조회 → LB로 선택 → 호출
        return restTemplate.getForObject(
            "http://user-service/api/users/{id}",
            User.class,
            userId
        );
    }
}

// ========== 내부 동작 순서 ==========

/*
1. @LoadBalanced가 Interceptor를 주입
2. 호출 시 "user-service" 호스트 이름 감지
3. DiscoveryClient.getInstances("user-service")로 목록 조회
4. LoadBalancer가 알고리즘에 따라 하나 선택
5. 선택된 인스턴스의 실제 URL로 요청 재작성
6. RestTemplate이 실제 HTTP 호출 실행
*/

// ========== 커스텀 로드 밸런싱 ==========

@Configuration
public class CustomLoadBalancerConfig {

    @Bean
    public ServiceInstanceListSupplier serviceInstanceListSupplier(
            ConfigurableApplicationContext context) {
        return ServiceInstanceListSupplier.builder()
                .withDiscoveryClient()
                .withHealthChecks()
                .withCaching()
                .build(context);
    }

    @Bean
    public ReactorLoadBalancer<ServiceInstance> customLoadBalancer(
            Environment environment,
            ServiceInstanceListSupplier supplier) {

        String name = environment.getProperty(LoadBalancerClientFactory.PROPERTY_NAME);
        return new CustomReactorLoadBalancer(
            supplier.get(name).subscribeOn(Schedulers.boundedElastic()),
            name
        );
    }
}

// 커스텀 로드 밸런싱 구현
public class CustomReactorLoadBalancer implements ReactorLoadBalancer<ServiceInstance> {

    private final ServiceInstanceListSupplier supplier;
    private final String serviceId;

    @Override
    public Mono<Response<ServiceInstance>> choose(Request request) {
        return supplier.get(request)
            .next()
            .map(instances -> processInstanceResponse(instances, request));
    }

    private Response<ServiceInstance> processInstanceResponse(
            List<ServiceInstance> instances,
            Request request) {

        // 커스텀 로직: Zone 우선, 가중치 기반, 지연 시간 고려 등
        instances.sort((a, b) -> {
            String zoneA = a.getMetadata().get("zone");
            String zoneB = b.getMetadata().get("zone");

            // 같은 Zone 우선
            String myZone = System.getenv("ZONE");
            if (zoneA.equals(myZone) && !zoneB.equals(myZone)) {
                return -1;
            }
            return 0;
        });

        // Round-Robin
        int index = ThreadLocalRandom.current().nextInt(instances.size());
        return new DefaultResponse(instances.get(index));
    }
}
```

### 3. 장점

| 장점 | 설명 | 예시 |
|:-----|:-----|:-----|
| **유연성** | 클라이언트가 로드 밸런싱 알고리즘 자유롭게 변경 | Zone 우선, 해시 기반 세션 고정 |
| **단순한 네트워크** | 중앙 LB 통과 없이 직접 호출 | 추가 홉 없음, 지연 시간 최소화 |
| **독립성** | 각 서비스가 자신만의 디스커버리 전략 | A 서비스는 Round-Robin, B는 Weighted |
| **오픈 소스 친화적** | Netflix 스택, Spring Cloud와 잘 맞음 | Eureka, Ribbon, Spring Cloud LoadBalancer |

### 4. 단점

| 단점 | 설명 | 해결 방안 |
|:-----|:-----|:---------|
| **클라이언트 복잡도** | 각 서비스가 디스커버리 + LB 로직 포함 | 라이브러리로 캡슐화 (Spring Cloud) |
| **버전 관리** | LB 알고리즘 변경 시 모든 클라이언트 업데이트 | 라이브러리 버전 관리 체계화 |
| **클라이언트별 불일치** | 각 클라이언트가 다른 알고리즘 사용 가능 | 가이드라인 및 템플릿 제공 |
| **레지스트리 의존** | Registry 장애 시 새 인스턴스 발견 불가 | 로컬 캐싱으로 완화 |

---

## Ⅲ. 서버 사이드 디스커버리

### 1. 아키텍처 상세

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  서버 사이드 디스커버리 상세 흐름                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  시나리오: 주문 서비스가 사용자 서비스를 호출 (AWS ALB 예시)                 │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   Step 1: 인프라 설정 (사전 준비)                                    │   │
│  │   ┌──────────────────────────────────────────────────────────────┐  │   │
│  │   │                                                              │  │   │
│  │   │   AWS ELB/ALB 생성                                           │  │   │
│  │   │   Target Group: user-service-target-group                   │  │   │
│  │   │     - 10.244.1.5:8080 (등록)                                │  │   │
│  │   │     - 10.244.1.6:8080 (등록)                                │  │   │
│  │   │     - 10.244.2.10:8080 (등록)                               │  │   │
│  │   │                                                              │  │   │
│  │   │   Health Check: HTTP /health 200 OK                         │  │   │
│  │   │   Load Balancing Algorithm: Round Robin                    │  │   │
│  │   │                                                              │  │   │
│  │   │   DNS: user-service.internal.elb.amazonaws.com              │  │   │
│  │   │        → Target Group의 인스턴스들로 로드 밸런싱            │  │   │
│  │   │                                                              │  │   │
│  │   └──────────────────────────────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  │   Step 2: 클라이언트는 단일 URL만 알면 됨                           │   │
│  │   ┌──────────────────────────────────────────────────────────────┐  │   │
│  │   │                                                              │  │   │
│  │   │   ┌──────────────────┐                                      │  │   │
│  │   │   │ Order Service    │                                      │  │   │
│  │   │   │ (Client App)     │   "user-service를 호출해야 해"        │  │   │
│  │   │   │                  │   환경 변수: USER_SERVICE_URL=        │  │   │
│  │   │   └────────┬─────────┘   http://user-service.elb.example.com │  │   │
│  │   │            │                                              │  │   │
│  │   │            ▼                                              │  │   │
│  │   │   ┌──────────────────────────────────────────────────────┐ │  │   │
│  │   │   │               Load Balancer (ALB)                   │ │  │   │
│  │   │   │                                                      │ │  │   │
│  │   │   │   ┌────────────────────────────────────────────────┐ │ │  │   │
│  │   │   │   │ 1. 요청 수신                                   │ │ │  │   │
│  │   │   │   │    user-service.elb.example.com/users/123     │ │ │  │   │
│  │   │   │   │                                                │ │ │  │   │
│  │   │   │   │ 2. Health 한 인스턴스 선택                       │ │ │  │   │
│  │   │   │   │    선택: 10.244.1.6:8080                        │ │ │  │   │
│  │   │   │   │                                                │ │ │  │   │
│  │   │   │   │ 3. 프록시 요청                                   │ │ │  │   │
│  │   │   │   │    GET http://10.244.1.6:8080/users/123        │ │ │  │   │
│  │   │   │   │                                                │ │ │  │   │
│  │   │   │   │ 4. 응답 반환                                    │ │ │  │   │
│  │   │   │   │    User 객체                                   │ │ │  │   │
│  │   │   │   └────────────────────────────────────────────────┘ │ │  │   │
│  │   │   └──────────────────────────────────────────────────────┘ │  │   │
│  │   │                                                              │  │   │
│  │   └──────────────────────────────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 서버 사이드 디스커버리 구현

```yaml
# AWS ALB + Target Group 예시

# 1. Target Group 생성
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  UserServiceTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: user-service-tg
      Port: 8080
      Protocol: HTTP
      VpcId: !Ref VPC
      HealthCheckPath: /health
      HealthCheckIntervalSeconds: 30
      HealthCheckTimeoutSeconds: 5
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 3
      TargetGroupAttributes:
        - Key: deregistration_delay.timeout_seconds
          Value: 30

  # 2. ALB 생성
  UserServiceLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: user-service-alb
      Scheme: internal
      Type: application
      IpAddressType: ipv4
      Subnets:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
      SecurityGroups:
        - !Ref ALBSecurityGroup

  # 3. Listener 생성
  ALBListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      LoadBalancerArn: !Ref UserServiceLoadBalancer
      Port: 80
      Protocol: HTTP
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref UserServiceTargetGroup

  # 4. Auto Scaling Group이 Target Group에 등록
  UserServiceAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      VPCZoneIdentifier:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
      TargetGroupARNs:
        - !Ref UserServiceTargetGroup
      MinSize: 2
      MaxSize: 10
      LaunchTemplate:
        LaunchTemplateSpecification:
          LaunchTemplateId: !Ref UserServiceLaunchTemplate
          Version: !LatestVersion

# ========== 클라이언트 코드 ==========

# 클라이언트는 매우 단순함! (단일 URL만 알면 됨)
@Service
public class OrderService {

    @Value("${user.service.url}")
    private String userServiceUrl;  // "http://user-service.elb.example.com"

    @Autowired
    private RestTemplate restTemplate;

    public User getUser(String userId) {
        // 디스커버리, 로드 밸런싱 필요 없음!
        // ALB가 모두 처리
        return restTemplate.getForObject(
            userServiceUrl + "/api/users/{id}",
            User.class,
            userId
        );
    }
}
```

### 3. 쿠버네티스 Service Discovery (서버 사이드)

```yaml
# 쿠버네티스 Service 매니페스트
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: production
spec:
  type: ClusterIP  # 클러스터 내부 통신
  selector:
    app: user-service  # Pod 라벨 셀렉터
  ports:
    - name: http
      protocol: TCP
      port: 80        # Service 포트
      targetPort: 8080  # 컨테이너 포트
  sessionAffinity: ClientIP  # 세션 고정 (필요시)

---
# Deployment (오토스케일링 가능)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  namespace: production
spec:
  replicas: 3  # 3개의 Pod
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
        version: v1.0.0
    spec:
      containers:
        - name: user-service
          image: registry.example.com/user-service:1.0.0
          ports:
            - containerPort: 8080
          livenessProbe:   # Health Check
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5

---
# HorizontalPodAutoscaler (오토스케일링)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: user-service-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: user-service
  minReplicas: 2
  maxReplicas: 10
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

# ========== 클라이언트 코드 ==========

# 쿠버네티스 클러스터 내에서는 DNS 이름으로만 호출
@Service
public class OrderService {

    @Autowired
    private RestTemplate restTemplate;

    public User getUser(String userId) {
        // 쿠버네티스 DNS: <service-name>.<namespace>.svc.cluster.local
        // user-service.production.svc.cluster.local
        return restTemplate.getForObject(
            "http://user-service/api/users/{id}",
            User.class,
            userId
        );
    }
}
```

### 4. 장점

| 장점 | 설명 | 예시 |
|:-----|:-----|:-----|
| **클라이언트 단순함** | 단일 URL만 알면 됨 | http://user-service.elb.example.com |
| **중앙 관리** | LB에서 로드 밸런싱, Health Check 통합 | ALB 설정만 변경하면 모든 클라이언트 반영 |
| **다양한 알고리즘** | LB에서 제공하는 고급 기능 활용 | AWS ALB의 요청 라우팅, IP 해싱 |
| **클라이언트 언어 무관** | 어떤 언어/프레임워크든 동작 | Go, Python, Rust 모두 단일 URL 호출 |
| **운영 친화적** | 인프라 팀이 LB만 관리 | 개발자는 비즈니스 로직만 집중 |

### 5. 단점

| 단점 | 설명 | 해결 방안 |
|:-----|:-----|:---------|
| **중앙 의존성** | LB 장애 시 모든 호출 실패 | Multi-AZ, Cross-Zone LB 배포 |
| **추가 홉** | LB를 거쳐서 지연 시간 증가 | 내부 LB(SLB) 사용, 캐싱 |
| **비용** | 관리형 LB 비용 발생 | K8s 내장 Service 활용 |
| **유연성 제한** | LB 제공 기능으로만 제한 | NLB + ALB 조합, 직접 LB 구축 |

---

## Ⅳ. 패턴 선택 가이드

### 1. 의사결정 트리

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    디스커버리 패턴 선택 가이드                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                              시작                                           │
│                                │                                             │
│                                ▼                                             │
│                    ┌───────────────────────┐                                │
│                    │  클라우드 제공자 사용? │                                │
│                    └───────────┬───────────┘                                │
│                                │                                             │
│              ┌─────────────────┴─────────────────┐                          │
│              YES                                   NO                         │
│              │                                     │                         │
│              ▼                                     ▼                         │
│    ┌────────────────────┐              ┌────────────────────┐               │
│    │ 서버 사이드 (관리형)│              │ 추가 질문         │               │
│    │                    │              │                   │               │
│    │ • AWS: ALB/NLB     │              └─────────┬─────────┘               │
│    │ • GCP: Cloud Load  │                        │                         │
│    │ • Azure: LB        │                        ▼                         │
│    │                    │              ┌────────────────────┐             │
│    └────────────────────┘              │ 쿠버네티스 사용?    │             │
│                                       └─────────┬───────────┘             │
│                                                 │                         │
│                               ┌─────────────────┴─────────────────┐       │
│                              YES                                  NO      │
│                              │                                     │      │
│                              ▼                                     ▼      │
│                    ┌────────────────────┐              ┌────────────────┐ │
│                    │ 서버 사이드 (K8s)  │              │ 클라이언트     │ │
│                    │                    │              │ 사이드         │ │
│                    │ • Service (Cluster │              │                │ │
│                    │   IP)             │              │ • Eureka       │ │
│                    │ • Ingress         │              │ • Consul       │ │
│                    │                    │              │ • Zookeeper    │ │
│                    └────────────────────┘              └────────────────┘ │ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 상황별 추천

| 상황 | 추천 패턴 | 이유 |
|:-----|:---------|:-----|
| **AWS/GCP/Azure 전용** | 서버 사이드 | 관리형 LB의 편리함, 네이티브 통합 |
| **쿠버네티스 환경** | 서버 사이드 | K8s Service가 이미 디스커버리 제공 |
| **하이브리드/온프레미스** | 클라이언트 사이드 | 인프라 독립성, Netflix OSS 스택 |
| **마이크로서비스 전문 조직** | 클라이언트 사이드 | 최대 제어권, 커스터마이징 |
| **다양한 언어/프레임워크** | 서버 사이드 | 언어 종속적 라이브러리 불필요 |
| **간단한 POC/MVP** | 서버 사이드 | 빠른 설정, 운영 간편 |
| **복잡한 라우팅 요구사항** | 클라이언트 사이드 | 세밀한 제어 필요 시 |

### 3. 하이브리드 접근법

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      하이브리드 디스커버리 아키텍처                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  상황: 대부분는 K8s Service를 사용하지만, 일부는 특별한 라우팅 필요          │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │   일반 서비스 (90%)                특별한 서비스 (10%)               │   │
│  │   ┌──────────────────┐            ┌──────────────────┐             │   │
│  │   │ Order Service    │            │ Analytics Engine │             │   │
│  │   └────────┬─────────┘            └────────┬─────────┘             │   │
│  │            │                                │                       │   │
│  │            ▼                                ▼                       │   │
│  │   ┌──────────────────┐            ┌──────────────────┐             │   │
│  │   │  K8s Service     │            │ Client-Side      │             │   │
│  │   │  (Server-Side)   │            │ Discovery        │             │   │
│  │   │                  │            │ (Consul)          │             │   │
│  │   │ DNS:             │            │                   │             │   │
│  │   │ user-service.svc │            │ - Weighted LB     │             │   │
│  │   │                  │            │ - Zone affinity   │             │   │
│  │   └──────────────────┘            │ - Canary routing  │             │   │
│  │                                    └──────────────────┘             │   │
│  │                                                                      │   │
│  │   "필요에 따라 두 패턴을 혼합하여 사용 가능!"                           │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 실전 비교 시나리오

### 1. 롤링 업데이트 시 동작 비교

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 롤링 업데이트 시 디스커버리 동작 비교                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  시나리오: user-service를 v1.0에서 v1.1로 업데이트                           │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────        │
│  클라이언트 사이드 (Eureka)                                                │
│  ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│  T0: 초기 상태                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   Eureka Registry:                                                  │   │
│  │   user-service: [                                                  │   │
│  │     {id: "user-1", host: "10.244.1.5", version: "v1.0"},           │   │
│  │     {id: "user-2", host: "10.244.1.6", version: "v1.0"},           │   │
│  │     {id: "user-3", host: "10.244.2.10", version: "v1.0"}           │   │
│  │   ]                                                                │   │
│  │                                                                      │   │
│  │   Order Service 로컬 캐시 (30초마다 갱신):                           │   │
│  │   위와 동일한 목록                                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  T1: 롤링 업데이트 시작 (Pod 1 교체)                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   Eureka Registry:                                                  │   │
│  │   user-service: [                                                  │   │
│  │     {id: "user-1-new", host: "10.244.3.20", version: "v1.1"},      │   │
│  │     {id: "user-2", host: "10.244.1.6", version: "v1.0"},           │   │
│  │     {id: "user-3", host: "10.244.2.10", version: "v1.0"}           │   │
│  │   ]                                                                │   │
│  │                                                                      │   │
│  │   Order Service 로컬 캐시:                                          │   │
│  │   아직 갱신 안 됨 (최대 30초 지연)                                   │   │
│  │   → 여전히 예전 IP를 호출할 수 있음                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  T2: 캐시 갱신 후                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   Order Service 로컬 캐시 갱신!                                     │   │
│  │   → 이제 새로운 인스턴스로 부하 분산 시작                           │   │
│  │   → 카나리 배포 효과 자동으로 얻음                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────        │
│  서버 사이드 (K8s Service)                                                │
│  ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│  T0: 초기 상태                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   user-service Service Endpoints:                                   │   │
│  │   [                                                                  │   │
│  │     10.244.1.5:8080,  ◀─ Pod 1 (v1.0)                              │   │
│  │     10.244.1.6:8080,  ◀─ Pod 2 (v1.0)                              │   │
│  │     10.244.2.10:8080 ◀─ Pod 3 (v1.0)                              │   │
│  │   ]                                                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  T1: 롤링 업데이트 시작 (Pod 1 종료 → 새 Pod 생성)                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   Readiness Probe: 새 Pod가 /health/ready 반환하기 전까지            │   │
│  │   Endpoint에 추가 안 됨                                             │   │
│  │                                                                      │   │
│  │   user-service Service Endpoints (트랜지션):                         │   │
│  │   [                                                                  │   │
│  │     10.244.1.6:8080,  ◀─ Pod 2 (v1.0)                              │   │
│  │     10.244.2.10:8080 ◀─ Pod 3 (v1.0)                              │   │
│  │   ]                                                                 │   │
│  │                                                                      │   │
│  │   → 트래픽은 남은 Pod 2, 3으로만 라우팅                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  T2: 새 Pod Ready                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │   user-service Service Endpoints:                                   │   │
│  │   [                                                                  │   │
│  │     10.244.1.6:8080,      ◀─ Pod 2 (v1.0)                          │   │
│  │     10.244.2.10:8080     ◀─ Pod 3 (v1.0)                          │   │
│  │     10.244.3.20:8080     ◀─ Pod 1-NEW (v1.1) ✅ Ready              │   │
│  │   ]                                                                 │   │
│  │                                                                      │   │
│  │   → 즉시 새 Pod로 트래픽 라우팅 시작                                 │   │
│  │   → 지연 시간 거의 없음                                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 장애 조치 비교

| 상황 | 클라이언트 사이드 | 서버 사이드 |
|:-----|:----------------|:-------------|
| **Registry 장애** | 로컬 캐시로 계속 동작 (최대 30초) | N/A (Registry 없음) |
| **LB 장애** | 영향 없음 (직접 호출) | 모든 호출 실패 😱 |
| **인스턴스 장애** | 다음 Heartbeat 후 제거 (최대 90초) | Health Check 후 즉시 제거 |
| **네트워크 파티션** | Self-Preservation 모드로 잘못 제거 방지 | Cross-Zone LB로 완화 |

---

## 📊 개념 맵

```
                    ┌────────────────────────┐
                    │  Service Discovery     │
                    └──────────┬─────────────┘
                               │
           ┌───────────────────┴───────────────────┐
           │                                       │
           ▼                                       ▼
┌──────────────────────┐           ┌──────────────────────┐
│ Client-Side         │           │ Server-Side         │
│ Discovery           │           │ Discovery           │
├──────────────────────┤           ├──────────────────────┤
│ Netflix OSS         │           │ AWS, GCP, Azure     │
│ Eureka              │           │ Kubernetes Service  │
│                    │           │                      │
│ 장점:               │           │ 장점:                │
│ • 유연한 라우팅     │           │ • 클라이언트 단순    │
│ • 중앙 의존 없음    │           │ • 중앙 관리         │
│                    │           │ • 언어 무관          │
│ 단점:               │           │ 단점:                │
│ • 클라이언트 복잡   │           │ • LB 장애 취약      │
│ • 버전 관리 어려움  │           │ • 추가 홉 비용       │
└──────────────────────┘           └──────────────────────┘
```

---

## 🎓 섹션 요약 비유 (어린이 설명)

### 🍕 주문 시스템 비유

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   🍕 피자 가게에 여러 지점이 있습니다:                                       │
│                                                                             │
│   - 강남점: 02-1111-1111                                                   │
│   - 홍대점: 02-2222-2222                                                   │
│   - 서초점: 02-3333-3333                                                   │
│                                                                             │
│   📞 고객이 "피자 주문하고 싶은데 어디로 전화하지?"                          │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│   📱 클라이언트 사이드 = "스마트 고객"                                      │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│      고객: "내가 직접 전화번호부를 확인하고 골랐어!"                          │
│                                                                             │
│      ┌───────────────────┐                                                  │
│      │                   │   "강남점, 홍대점, 서초점 전화번호 알려줘!"    │
│      │   고객            │   ────────────────────────────────▶            │
│      │  (Smart)          │                                                  │
│      │                   │   ┌──────────────┐                               │
│      └────────┬──────────┘   │ 전화번호부    │                               │
│               │              │ (Registry)    │                               │
│               │              └───────┬──────┘                               │
│               ▼                      │                                      │
│      ┌──────────────────────────────┴───────────────┐                     │
│      │  받은 목록: [강남점, 홍대점, 서초점]          │                     │
│      │                                               │                     │
│      │  🤔 "오늘은 홍대점에 사람이 많을 것 같으니까   │                     │
│      │        강남점으로 전화하자!"                   │                     │
│      │                                               │                     │
│      │  📞 02-1111-1111로 직접 전화!                 │                     │
│      └───────────────────────────────────────────────┘                     │
│                                                                             │
│   장점: 전화 교환원 없이 직접! (빠름)                                       │
│   단점: 전화번호부를 항상 확인해야 해 (귀찮음)                               │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│   📞 서버 사이드 = "전화 교환원"                                            │
│   ─────────────────────────────────────────────────────────────────        │
│                                                                             │
│      고객: "그냥 1588-0000로 전화했어!"                                     │
│                                                                             │
│      ┌───────────────────┐                                                  │
│      │                   │   "피자 주문하고 싶어요!"                       │
│      │   고객            │   ────────────────────────────────▶            │
│      │  (Dumb)           │                                                  │
│      │                   │   ┌──────────────┐                               │
│      └────────┬──────────┘   │ 전화 교환원   │                               │
│               │              │ (Load Balancer)│                              │
│               │              └───────┬──────┘                               │
│               │                      │                                      │
│               │                      ▼                                      │
│               │            ┌─────────────────────┐                          │
│               │            │ "홍대점은 지금 붐비고 │                          │
│               │            │  강남점은 한가하니까 │                          │
│               │            │  강남점으로 연결해줘!"│                          │
│               │            └─────────┬───────────┘                          │
│               │                      │                                      │
│               ▼                      ▼                                      │
│      ┌────────────────────────────────────────┐                            │
│      │  고객은 그냥 기다리면 돼!               │                            │
│      │  전화 교환원이 알아서 연결해줘          │                            │
│      └────────────────────────────────────────┘                            │
│                                                                             │
│   장점: 전화번호 하나만 기억하면 돼! (편리함)                               │
│   단점: 교환원이 쉬면 다 안 돼! (중앙 의존)                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**핵심**: 클라이언트 사이드는 **"스마트 고객이 직접 전화번호부를 확인하고 선택"**하는 방식이고, 서버 사이드는 **"전화 교환원이 알아서 적절한 지점으로 연결"**해주는 방식입니다!

---

## 관련 키워드

- **서비스 디스커버리** (#186): 두 패턴의 상위 개념
- **Eureka** (#186): 클라이언트 사이드 디스커버리 구현
- **쿠버네티스 Service**: 서버 사이드 디스커버리 구현
- **API Gateway** (#184): LB와 함께 사용되는 진입점
- **로드 밸런싱**: 두 패턴 모두 핵심 요소
