+++
title = "멀티 테넌시 (Multi-Tenancy)"
date = 2024-05-18
description = "하나의 소프트웨어/인스턴스가 여러 고객 Tenant에게 독립적으로 서비스되도록 논리적 분리 보장하는 SaaS 핵심 아키텍처"
weight = 15
[taxonomies]
categories = ["studynotes-13_cloud_architecture"]
tags = ["Multi-Tenancy", "SaaS", "Tenant Isolation", "Cloud Architecture", "Data Isolation"]
+++

# 멀티 테넌시 (Multi-Tenancy)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 멀티 테넌시는 단일 소프트웨어 인스턴스와 인프라를 여러 고객(Tenant)이 공유하면서도, 각 고객은 논리적으로 완전히 격리된 전용 환경처럼 인식하는 SaaS 아키텍처의 핵심 설계 원칙입니다.
> 2. **가치**: 하드웨어 자원 효율 극대화(70~90% 활용률), 운영 비용 절감(50~80%), 규모의 경제로 인한 서비스 단가 하락, 중앙집중식 업데이트와 패치 관리가 가능합니다.
> 3. **융합**: 데이터베이스 샤딩, 컨테이너 격리, 가상 네트워크 분리, RBAC(Role-Based Access Control), 암호화 키 관리와 결합하여 안전한 테넌트 격리를 구현합니다.

---

## Ⅰ. 개요 (Context & Background)

멀티 테넌시(Multi-Tenancy)는 SaaS(Software as a Service) 모델의 핵심 아키텍처 원칙으로, 하나의 애플리케이션 인스턴스가 여러 조직(테넌트)에게 서비스를 제공하는 동시에 각 테넌트의 데이터, 설정, 사용자 정보를 논리적으로 분리하는 기술입니다. 싱글 테넌시(Single-Tenancy)가 각 고객마다 별도의 인스턴스를 운영하는 것과 대조적으로, 멀티 테넌시는 자원 공유를 통해 경제성과 확장성을 동시에 확보합니다.

**💡 비유**: 멀티 테넌시는 **'아파트 단지'**와 같습니다. 각 가구(테넌트)는 같은 건물(인프라)을 공유하지만, 각자의 호수(논리적 공간)는 완전히 독립적입니다. 엘리베이터, 수도, 전기(공통 서비스)는 공유하지만, 내 집 내부(데이터, 설정)는 다른 가구가 볼 수 없습니다. 건물 주인(SaaS 제공자)은 한 번에 전체 건물의 보안 시스템을 업그레이드할 수 있습니다.

**등장 배경 및 발전 과정**:
1. **온프레미스 시대의 비효율**: 각 기업이 자체 서버, DB, 애플리케이션을 운영하여 자원 활용률이 10~20%에 불과했습니다.
2. **SaaS 모델의 등장**: Salesforce(1999)가 클라우드 기반 CRM을 출시하며 멀티 테넌시 개념을 상용화했습니다.
3. **클라우드 네이티브로 진화**: 컨테이너, Kubernetes, 서버리스 기술이 멀티 테넌시 구현을 더욱 유연하게 만들었습니다.
4. **규제 강화**: GDPR, HIPAA 등 데이터 보호 규정으로 테넌트 간 격리 요구사항이 강화되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 멀티 테넌시 격리 수준 (표)

| 격리 수준 | 아키텍처 | 장점 | 단점 | 적용 사례 |
|---|---|---|---|---|
| **Shared Everything** | 단일 DB, 단일 스키마, tenant_id 컬럼 | 최고 비용 효율, 간단한 운영 | 격리 취약, 노이지 네이버 | 소규모 B2C SaaS |
| **Shared Database, Separate Schema** | 단일 DB, 테넌트별 스키마 | 적절한 격리, 관리 용이 | DB 연결 수 증가 | 중간 규모 B2B SaaS |
| **Separate Database** | 테넌트별 별도 DB | 강력한 격리, 백업/복원 유연 | 비용 증가, 복잡한 관리 | 엔터프라이즈, 금융 |
| **Separate Cluster** | 테넌트별 쿠버네티스 네임스페이스/클러스터 | 최고 수준 격리, 규제 준수 | 높은 비용, 운영 복잡 | 공공, 의료, 국방 |

### 멀티 테넌시 구현 계층 (표)

| 계층 | 격리 메커니즘 | 상세 동작 | 관련 기술 | 비유 |
|---|---|---|---|---|
| **애플리케이션 계층** | Context Switching | 요청 시 테넌트 식별 후 해당 컨텍스트 로드 | Spring TenantContext, Node.js middleware | 호수 확인 후 방 안내 |
| **데이터베이스 계층** | Row/Schema/DB Level Isolation | 쿼리에 tenant_id 자동 추가 또는 스키마 전환 | Hibernate Filter, RLS(Row Level Security) | 우편함 분리 |
| **스토리지 계층** | 버킷/경로 분리 | 테넌트별 오브젝트 스토리지 경로 격리 | S3 Bucket Policy, Prefix | 창고 구획 |
| **네트워크 계층** | VPC, 서브넷 격리 | 논리적 네트워크 분리, 방화벽 규칙 | VPC, Security Group, Network Policy | 건물 층별 분리 |
| **컴퓨팅 계층** | 컨테이너/노드 격리 | 테넌트별 파드 배치, 리소스 쿼터 | K8s Namespace, Node Affinity | 전용 엘리베이터 |

### 정교한 멀티 테넌시 아키텍처 다이어그램

```ascii
                              +------------------+
                              |    End Users     |
                              | (Tenant A, B, C) |
                              +--------+---------+
                                       |
                              +--------v---------+
                              |   Load Balancer  |
                              |  (Tenant Routing)|
                              +--------+---------+
                                       |
                    +------------------+------------------+
                    |                  |                  |
           +--------v--------+ +-------v--------+ +------v---------+
           |   App Server    | |  App Server    | |  App Server    |
           |  (Pool Mode)    | | (Pool Mode)    | | (Pool Mode)    |
           +--------+--------+ +-------+--------+ +------+---------+
                    |                  |                  |
                    +------------------+------------------+
                                       |
                    +------------------v------------------+
                    |      Tenant Context Resolver       |
                    |  1. Extract tenant_id from JWT     |
                    |  2. Load tenant config from cache  |
                    |  3. Set DB schema/connection       |
                    +------------------+------------------+
                                       |
        +------------------------------+------------------------------+
        |                              |                              |
+-------v-------+              +-------v-------+              +-------v-------+
|  Tenant A     |              |  Tenant B     |              |  Tenant C     |
|  Schema: tenant_a            |  Schema: tenant_b            |  DB: tenant_c_db
|  Storage: s3/a/              |  Storage: s3/b/              |  Storage: s3/c/
+-------+-------+              +-------+-------+              +-------+-------+
        |                              |                              |
+-------v-------+              +-------v-------+              +-------v-------+
|  PostgreSQL   |              |  PostgreSQL   |              |  PostgreSQL   |
|  (Schema Sep.)|              |  (Schema Sep.)|              |  (DB Sep.)    |
+---------------+              +---------------+              +---------------+

[Tenant Isolation Layers]
+------------------------------------------------------------------+
| Layer 1: Application - Tenant Context in Thread-Local Storage    |
| Layer 2: Database - Row Level Security (RLS) auto-filter         |
| Layer 3: Storage - Prefix-based object isolation                 |
| Layer 4: Network - Kubernetes Network Policy per namespace       |
| Layer 5: Encryption - Tenant-specific data encryption keys       |
+------------------------------------------------------------------+
```

### 심층 동작 원리: 테넌트 컨텍스트 관리

1. **인증 및 테넌트 식별**:
   - 사용자 로그인 시 JWT에 tenant_id 클레임 포함
   - API 요청 시 JWT 검증 후 tenant_id 추출

2. **컨텍스트 설정**:
   - ThreadLocal 또는 요청 스코프에 테넌트 정보 저장
   - 데이터베이스 연결 시 해당 테넌트 스키마 설정

3. **데이터 접근**:
   - 모든 쿼리에 tenant_id 필터 자동 추가 (ORM 레벨)
   - RLS(Row Level Security)로 DB 레벨 이중 차단

4. **리소스 할당**:
   - 테넌트별 Rate Limiting, Quota 적용
   - 노이지 네이버(Noisy Neighbor) 방지

5. **감사 및 로깅**:
   - 모든 로그에 tenant_id 태깅
   - 테넌트별 접근 로그 분리 저장

### 핵심 코드: 스프링 부트 멀티 테넌시 구현

```java
import org.hibernate.context.spi.CurrentTenantIdentifierResolver;
import org.springframework.stereotype.Component;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

/**
 * 멀티 테넌시 컨텍스트 리졸버
 * - 각 요청에서 테넌트 ID를 추출하여 Hibernate에 전달
 * - DB 연결 시 자동으로 해당 테넌트 스키마 선택
 */
@Component
public class TenantContextResolver implements CurrentTenantIdentifierResolver {

    private static final String DEFAULT_TENANT = "public";
    private static final ThreadLocal<String> CURRENT_TENANT = new ThreadLocal<>();

    @Override
    public String resolveCurrentTenantIdentifier() {
        String tenant = CURRENT_TENANT.get();
        return tenant != null ? tenant : DEFAULT_TENANT;
    }

    @Override
    public boolean validateExistingCurrentSessions() {
        return true;
    }

    // 요청 시작 시 테넌트 설정
    public static void setTenantId(String tenantId) {
        CURRENT_TENANT.set(tenantId);
    }

    // 요청 종료 시 정리
    public static void clear() {
        CURRENT_TENANT.remove();
    }

    // JWT에서 테넌트 ID 추출
    public static String extractTenantFromJWT(String token) {
        // JWT 파싱 로직 (실제로는 JWT 라이브러리 사용)
        // 예: {"sub": "user123", "tenant_id": "tenant_acme"}
        return JwtUtil.getClaim(token, "tenant_id");
    }
}

/**
 * 멀티 테넌시 데이터 소스 라우터
 * - 테넌트별 DB 연결을 동적으로 라우팅
 */
public class TenantRoutingDataSource extends AbstractRoutingDataSource {

    @Override
    protected Object determineCurrentLookupKey() {
        return TenantContextResolver.getCurrentTenant();
    }
}

/**
 * 요청 인터셉터 - 테넌트 컨텍스트 설정
 */
@Component
public class TenantInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request,
                           HttpServletResponse response,
                           Object handler) {
        String token = request.getHeader("Authorization");
        if (token != null && token.startsWith("Bearer ")) {
            String tenantId = TenantContextResolver.extractTenantFromJWT(token);
            TenantContextResolver.setTenantId(tenantId);
        }
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request,
                               HttpServletResponse response,
                               Object handler,
                               Exception ex) {
        TenantContextResolver.clear();  // 메모리 누수 방지
    }
}

/**
 * JPA 엔티티 - 테넌트 격리 기본 클래스
 */
@MappedSuperclass
@EntityListeners(TenantListener.class)
public abstract class TenantAwareEntity {

    @Column(name = "tenant_id", nullable = false, updatable = false)
    private String tenantId;

    // Getters and Setters
    public String getTenantId() { return tenantId; }
    public void setTenantId(String tenantId) { this.tenantId = tenantId; }
}

/**
 * JPA 리스너 - 자동 tenant_id 설정
 */
public class TenantListener {

    @PrePersist
    public void setTenantId(Object entity) {
        if (entity instanceof TenantAwareEntity) {
            TenantAwareEntity tenantEntity = (TenantAwareEntity) entity;
            if (tenantEntity.getTenantId() == null) {
                tenantEntity.setTenantId(
                    TenantContextResolver.resolveCurrentTenantIdentifier()
                );
            }
        }
    }
}

/**
 * PostgreSQL Row Level Security (RLS) 설정 SQL
 */
/*
-- 테넌트별 RLS 정책 생성
CREATE POLICY tenant_isolation_policy ON orders
    USING (tenant_id = current_setting('app.current_tenant')::text);

-- RLS 활성화
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- 이렇게 하면 애플리케이션 레벨 필터링 실패해도 DB가 차단
*/
```

### 핵심 코드: 쿠버네티스 멀티 테넌시 (네임스페이스 격리)

```yaml
# 테넌트별 네임스페이스 생성
apiVersion: v1
kind: Namespace
metadata:
  name: tenant-acme
  labels:
    tenant: acme
    tier: enterprise
---
apiVersion: v1
kind: Namespace
metadata:
  name: tenant-globex
  labels:
    tenant: globex
    tier: standard

---
# 테넌트별 리소스 쿼터
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-acme-quota
  namespace: tenant-acme
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    persistentvolumeclaims: "10"
    pods: "50"
    services: "20"

---
# 네트워크 폴리시 - 테넌트 간 통신 차단
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: tenant-isolation
  namespace: tenant-acme
spec:
  podSelector: {}  # 모든 파드에 적용
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              tenant: acme  # 같은 테넌트 네임스페이스만 허용
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              tenant: acme
    - to:  # 외부 API 허용
        - ipBlock:
            cidr: 0.0.0.0/0
            except:
              - 10.0.0.0/8  # 내부망은 차단

---
# 테넌트별 Helm Values (values-acme.yaml)
tenant:
  id: acme
  tier: enterprise
  features:
    - advanced_analytics
    - custom_branding
    - sso_integration

resources:
  requests:
    cpu: 2
    memory: 4Gi
  limits:
    cpu: 4
    memory: 8Gi

database:
  type: dedicated  # 전용 DB
  size: db.r5.xlarge

storage:
  quota: 500Gi
  class: gp3
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 멀티 테넌시 vs 싱글 테넌시

| 비교 관점 | Multi-Tenancy | Single-Tenancy | 상세 분석 |
|---|---|---|---|
| **인프라 비용** | 낮음 (공유) | 높음 (전용) | Multi가 50~80% 저렴 |
| **격리 수준** | 논리적 격리 | 물리적 격리 | Single이 보안상 유리 |
| **커스터마이징** | 제한적 | 무제한 | Single이 유연 |
| **업그레이드** | 일괄 적용 | 개별 적용 | Multi가 운영 효율 |
| **장애 영향** | 전체 테넌트 영향 가능 | 해당 테넌트만 | Single이 장애 격리 유리 |
| **확장성** | 용이 (공유 자원) | 복잡 (개별 확장) | Multi가 확장 유리 |
| **규제 준수** | 어려움 (공유) | 용이 (전용) | 금융/의료는 Single 선호 |

### 데이터베이스 격리 전략 비교

| 전략 | 격리 수준 | 비용 | 복잡도 | 백업/복원 | 적합한 규모 |
|---|---|---|---|---|---|
| **Shared Table (Discriminator Column)** | 낮음 | 낮음 | 낮음 | 어려움 | 소규모, B2C |
| **Shared DB, Separate Schema** | 중간 | 중간 | 중간 | 보통 | 중간 규모, B2B |
| **Separate Database per Tenant** | 높음 | 높음 | 높음 | 쉬움 | 대규모, 엔터프라이즈 |
| **Separate Cluster per Tenant** | 최고 | 최고 | 최고 | 쉬움 | 규제 산업, 공공 |

### 과목 융합 관점 분석

- **데이터베이스와의 융합**: RLS(Row Level Security), VPD(Virtual Private Database), 스키마 분리 기술을 활용하여 DB 레벨에서 테넌트 격리를 구현합니다. PostgreSQL RLS, Oracle VPD가 대표적입니다.

- **보안과의 융합**: 테넌트별 암호화 키 관리(KMS), 데이터 마스킹, 감사 로그 분리가 필수입니다. 제로 트러스트 원칙에 따라 모든 데이터 접근을 테넌트 컨텍스트로 검증합니다.

- **네트워크와의 융합**: VPC, 서브넷, 보안 그룹, Network Policy를 통해 테넌트 간 네트워크 트래픽을 격리합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: B2B SaaS CRM 서비스**
- **요구사항**: 1,000개 기업 고객, 각 기업별 커스텀 필드, SLA 99.9%
- **기술사의 의사결정**:
  1. 데이터베이스: Shared DB + Separate Schema (비용 효율과 격리 균형)
  2. 커스텀 필드: JSONB 컬럼으로 유연하게 지원
  3. 스토리지: S3 prefix 기반 격리
  4. 백업: 스키마별 개별 백업/복원 지원
  5. **예상 비용**: 싱글 테넌시 대비 60% 절감

**시나리오 2: 금융 핀테크 SaaS**
- **요구사항**: 은행 10개 고객, 금융감독원 규제, 데이터 완전 격리
- **기술사의 의사결정**:
  1. 데이터베이스: Separate DB per Tenant (규제 준수)
  2. 암호화: 테넌트별 KMS 키 (BYOK 지원)
  3. 네트워크: VPC Peering으로 전용 연결
  4. 감사: 테넌트별 독립된 감사 로그 저장소
  5. **예상 비용**: 싱글 테넌시와 유사하나 운영 효율로 20% 절감

**시나리오 3: B2C 모바일 앱 (100만 사용자)**
- **요구사항**: 개인 사용자 대상, 무료/유료 플랜, 비용 최소화
- **기술사의 의사결정**:
  1. 데이터베이스: Shared Table + tenant_id 컬럼 (최고 비용 효율)
  2. 캐시: Redis Cluster에서 키 prefix로 격리
  3. 스토리지: S3 통합 + prefix 분리
  4. Rate Limiting: 테넌트별 API 호출 제한
  5. **예상 비용**: 싱글 테넌시 대비 90% 절감

### 도입 시 고려사항 (체크리스트)

**기술적 체크리스트**:
- [ ] 격리 수준 결정: 규제 요구사항, 비용 제약 검토
- [ ] 마이그레이션 전략: 기존 데이터의 테넌트 분할 방안
- [ ] 노이지 네이터 대응: 리소스 쿼터, Rate Limiting
- [ ] 백업/복원: 테넌트별 독립 백업 가능 여부

**운영적 체크리스트**:
- [ ] 모니터링: 테넌트별 성능 메트릭 분리
- [ ] 과금: 테넌트별 리소스 사용량 측정
- [ ] 지원: 테넌트별 로그 조회 권한 관리

### 주의사항 및 안티패턴 (Anti-patterns)

1. **tenant_id 하드코딩**: 모든 쿼리에 수동으로 tenant_id를 추가하면 실수 가능성. ORM 레벨 필터 또는 RLS 사용.

2. **크로스 테넌트 쿼리**: 관리 목적으로 여러 테넌트 데이터를 한 번에 조회하려면 별도 관리 DB 사용.

3. **과도한 격리**: 모든 테넌트에 Separate DB를 적용하면 비용 폭증. 티어별 격리 수준 차등 적용.

4. **암호화 키 공유**: 모든 테넌트가 같은 암호화 키를 사용하면 격리 무의미. 테넌트별 키 필수.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | Single-Tenancy | Multi-Tenancy | 개선율 |
|---|---|---|---|
| **인프라 비용** | $100/테넌트 | $20/테넌트 | 80% 절감 |
| **운영 인력** | 10명 | 3명 | 70% 절감 |
| **업데이트 시간** | 1,000회 (개별) | 1회 (일괄) | 99.9% 단축 |
| **자원 활용률** | 15% | 70% | 4.7배 향상 |
| **신규 테넌트 온보딩** | 1주일 | 5분 | 99% 단축 |

### 미래 전망 및 진화 방향

1. **Serverless Multi-Tenancy**: 함수 단위로 테넌트 격리, 완전 종량제 과금
2. **AI 기반 리소스 최적화**: 테넌트별 사용 패턴 학습, 자동 스케일링
3. **Zero-Trust Multi-Tenancy**: 모든 계층에서 테넌트 검증, 침해 시 영향 최소화

### ※ 참고 표준/가이드
- **ISO/IEC 27001**: Information Security Management (테넌트 격리 요구사항)
- **SOC 2 Type II**: Service Organization Control (멀티 테넌시 보안 검증)
- **GDPR Article 17**: Right to Erasure (테넌트 데이터 삭제)
- **CSA STAR**: Cloud Security Alliance (멀티 테넌시 모범 사례)

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [SaaS (Software as a Service)](@/studynotes/13_cloud_architecture/03_virt/saas.md) : 멀티 테넌시의 핵심 적용 모델
- [데이터 격리 (Data Isolation)](@/studynotes/13_cloud_architecture/03_virt/data_isolation.md) : 테넌트 데이터 보호 기술
- [RBAC (Role-Based Access Control)](@/studynotes/13_cloud_architecture/01_native/rbac.md) : 테넌트 내 권한 관리
- [쿠버네티스 네임스페이스](@/studynotes/13_cloud_architecture/01_native/k8s_namespace.md) : 컨테이너 테넌트 격리
- [데이터베이스 샤딩](@/studynotes/13_cloud_architecture/02_migration/db_sharding.md) : 대규모 테넌트 데이터 분산

---

### 👶 어린이를 위한 3줄 비유 설명
1. 멀티 테넌시는 **'아파트'**와 같아요. 많은 가구(고객)가 같은 건물(소프트웨어)에서 살지만, 각자의 집(데이터)은 따로 있어요.
2. 건물 주인은 **'한 번에 모든 집'**의 엘리베이터를 고칠 수 있어요. 일일이 100채의 단독주택을 돌아다니지 않아도 돼요.
3. 하지만 내 집 비밀번호는 **'다른 이웃과 절대 공유하지 않아요'**. 그래서 아무도 내 방을 들여다볼 수 없어요.
