+++
title = "피처 플래그 (Feature Flag) / 피처 토글 (Feature Toggle)"
description = "코드 재배포 없이 런타임에 기능을 켜고 끄는 기법에 대한 심층 기술 백서"
date = 2024-05-15
[taxonomies]
tags = ["Feature Flag", "Feature Toggle", "Continuous Delivery", "Trunk-Based Development", "A/B Testing"]
+++

# 피처 플래그 (Feature Flag) / 피처 토글 (Feature Toggle)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 피처 플래그(Feature Flag)는 소프트웨어의 특정 기능을 **코드 재배포 없이 런타임에 설정(API/DB/환경 변수)을 통해 켜거나 끌 수 있는 조건부 실행 메커니즘**으로, 배포와 릴리스를 분리하는 핵심 기술입니다.
> 2. **가치**: 피처 플래그는 트렁크 기반 개발을 가능하게 하여 장기 브랜치로 인한 병합 충돌을 방지하고, 카나리 릴리스, A/B 테스팅, 긴급 기능 차단(Kill Switch)을 지원하여 배포 안정성과 개발 속도를 동시에 확보합니다.
> 3. **융합**: CI/CD 파이프라인, LaunchDarkly/Unleash 같은 피처 플래그 관리 플랫폼, A/B 테스팅 도구, SLO 모니터링과 결합하여 세밀한 기능 제어와 실험 문화를 구축합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**피처 플래그(Feature Flag)**, 또는 **피처 토글(Feature Toggle)**, **기능 스위치(Feature Switch)**는 소프트웨어 코드 내에서 **특정 기능의 실행 여부를 런타임에 결정하는 조건문(if-else) 패턴**입니다. 기능의 활성화/비활성화가 코드 배포와 분리되어, **"배포(Deploy) ≠ 릴리스(Release)"**라는 새로운 패러다임을 가능하게 합니다.

피처 플래그의 핵심 유형:
| 유형 | 수명 | 사용 사례 | 예시 |
| :--- | :--- | :--- | :--- |
| **Release Toggle** | 단기 (수주) | 미완성 기능 숨기기, 카나리 릴리스 | `if (flag.enabled("new-checkout"))` |
| **Ops Toggle** | 단기 (수시간~수일) | 긴급 기능 차단(Kill Switch) | `if (!flag.enabled("payment-api"))` |
| **Experiment Toggle** | 단기 (A/B 테스트 기간) | A/B 테스팅, 통계적 실험 | `if (user.group == "A")` |
| **Permission Toggle** | 장기 | 사용자 등급별 기능 제어 | `if (user.isPremium())` |

### 💡 2. 구체적인 일상생활 비유
**조명 스위치**를 상상해 보세요:
- **코드 배포**: 집에 새로운 전등을 설치했습니다. (기능 개발 완료)
- **피처 플래그 OFF**: 스위치가 꺼져 있어서 전등이 켜지지 않습니다. (사용자는 못 봄)
- **피처 플래그 ON**: 스위치를 켜서 전등이 밝혀집니다. (릴리스 = 사용자에게 공개)

과거에는 전등을 설치하려면:
1. 전등을 사 온다.
2. 배선을 연결한다.
3. 즉시 켜진다. (사용자에게 노출)

피처 플래그를 쓰면:
1. 전등을 사 온다.
2. 배선을 연결한다.
3. **스위치를 꺼둔다.**
4. 준비되면 **스위치를 켠다.** (릴리스)

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (장기 브랜치와 병합 지옥)**:
   과거에는 새로운 기능을 개발할 때:
   - `feature/new-payment` 브랜치에서 3개월간 개발합니다.
   - 개발 완료 전까지는 main에 병합할 수 없습니다.
   - 병합 시 500개 파일 충돌(Merge Hell).
   - "배포일 = 릴리스일"이어서, 배포하자마자 모든 사용자가 새 기능을 봅니다.

2. **혁신적 패러다임 변화의 시작**:
   - **2010년**: Martin Fowler가 "Feature Toggles" 글 발표.
   - **2010년대**: Facebook, Google, Netflix가 대규모 피처 플래그 시스템 구축.
   - **2014년**: LaunchDarkly가 상용 피처 플래그 플랫폼 출시.
   - **현재**: Unleash, Flagsmith, AWS AppConfig 등 다양한 오픈소스/상용 도구.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   트렁크 기반 개발(Trunk-Based Development)이 DevOps 성숙도의 핵심 지표입니다. 피처 플래그 없이는 트렁크 기반 개발이 불가능합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **플래그 저장소** | 플래그 상태 및 타겟팅 규칙 저장 | Key-Value, 규칙 엔진, 세분화 그룹 | Redis, LaunchDarkly, Unleash | 스위치 패널 |
| **플래그 SDK** | 애플리케이션에서 플래그 평가 | 로컬 캐싱, 실시간 업데이트, 폴백 | OpenFeature, LaunchDarkly SDK | 전선 |
| **타겟팅 엔진** | 사용자/조건별 분기 처리 | 사용자 ID, 그룹, 비율, 컨텍스트 기반 | 규칙 엔진, 무작위 분배 | 스위치 로직 |
| **관리 콘솔** | 플래그 생성/수정/삭제 | Web UI, API, 감사 로그 | LaunchDarkly UI, Unleash Web | 스위치 조작판 |
| **분석 대시보드** | 플래그 효과 측정 | A/B 테스트 결과, 전환율 | Analytics, DataDog | 전력 사용량계 |

### 2. 정교한 구조 다이어그램: 피처 플래그 아키텍처

```text
=====================================================================================================
                    [ Feature Flag Architecture - Complete System ]
=====================================================================================================

+-------------------------------------------------------------------------------------------+
|                              [ FEATURE FLAG MANAGEMENT PLATFORM ]                          |
|                                                                                           |
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Flag Management Console (Web UI)                                                 │   │
│   │                                                                                  │   │
│   │ ┌───────────────────────────────────────────────────────────────────────────┐   │   │
│   │ │ Flag: new-checkout-flow                                                   │   │   │
│   │ │                                                                           │   │   │
│   │ │ Status: ON ☑                                                              │   │   │
│   │ │                                                                           │   │   │
│   │ │ Targeting Rules:                                                          │   │   │
│   │ │ ┌─────────────────────────────────────────────────────────────────────┐   │   │   │
│   │ │ │ Rule 1: If user.email contains "@company.com" → TRUE               │   │   │   │
│   │ │ │ Rule 2: If user.id in ["123", "456", "789"] → TRUE                 │   │   │   │
│   │ │ │ Rule 3: If user.country == "KR" → TRUE (20% rollout)               │   │   │   │
│   │ │ │ Default: FALSE                                                       │   │   │   │
│   │ │ └─────────────────────────────────────────────────────────────────────┘   │   │   │
│   │ │                                                                           │   │   │
│   │ │ [Save] [Disable] [Delete]                                                 │   │   │
│   │ └───────────────────────────────────────────────────────────────────────────┘   │   │
│   └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                                 │
│                                        │ API (REST/Streaming)
│                                        ▼                                                 │
+-------------------------------------------------------------------------------------------+
                                   │
                                   │ SDK Polling / Streaming
                                   ▼
+-------------------------------------------------------------------------------------------+
|                              [ APPLICATION RUNTIME ]                                       |
|                                                                                           |
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Feature Flag SDK (Client-Side)                                                   │   │
│   │                                                                                  │   │
│   │ ┌───────────────┐    ┌───────────────┐    ┌───────────────┐                     │   │
│   │ │ Local Cache   │    │ Evaluator     │    │ Event Tracker │                     │   │
│   │ │ (Flags JSON)  │───>│ (Rule Engine) │───>│ (Analytics)   │                     │   │
│   │ │ TTL: 30s      │    │               │    │               │                     │   │
│   │ └───────────────┘    └───────────────┘    └───────────────┘                     │   │
│   └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                                 │
│                                        ▼                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Application Code                                                                  │   │
│   │                                                                                  │   │
│   │ // 코드 내 플래그 사용                                                            │   │
│   │ if (featureFlagClient.isEnabled("new-checkout-flow", userContext)) {            │   │
│   │     return newCheckoutService.process(order);  // 새로운 체크아웃 로직           │   │
│   │ } else {                                                                         │   │
│   │     return legacyCheckoutService.process(order);  // 기존 체크아웃 로직          │   │
│   │ }                                                                                │   │
│   │                                                                                  │   │
│   └─────────────────────────────────────────────────────────────────────────────────┘   │
+-------------------------------------------------------------------------------------------+

=====================================================================================================
   플래그 수명 주기:
   1. Create: 새 플래그 생성 (기본값: OFF)
   2. Develop: 코드에 플래그 조건문 추가, main에 병합 (아직 사용자에게 안 보임)
   3. Test: 내부 사용자에게만 ON (dogfooding)
   4. Canary: 1% → 10% → 50% → 100% 점진적 확대
   5. Full Rollout: 100% 사용자에게 ON
   6. Cleanup: 플래그 코드 제거 (기술 부채 청산)
   7. Archive: 플래그 삭제
=====================================================================================================
```

### 3. 심층 동작 원리 (플래그 평가 알고리즘)

**1단계: 컨텍스트 수집**
```javascript
// 사용자 컨텍스트 구성
const userContext = {
    key: "user-12345",           // 사용자 고유 ID (필수)
    email: "john@company.com",   // 이메일
    country: "KR",               // 국가
    plan: "premium",             // 요금제
    groups: ["beta-testers"],    // 그룹
    custom: {                    // 커스텀 속성
        age: 30,
        firstVisit: "2024-01-15"
    }
};
```

**2단계: 타겟팅 규칙 평가**
```javascript
// 플래그 평가 엔진 (의사코드)
function evaluateFlag(flagKey, userContext) {
    const flag = flagStore.get(flagKey);

    // 1. 플래그가 존재하지 않음 → 기본값 반환
    if (!flag) {
        return flag.defaultValue || false;
    }

    // 2. 플래그가 전역 OFF → false 반환
    if (!flag.enabled) {
        return false;
    }

    // 3. 타겟팅 규칙 순차 평가
    for (const rule of flag.targetingRules) {
        // 규칙 1: 사용자 ID 직접 지정
        if (rule.userIds && rule.userIds.includes(userContext.key)) {
            return rule.value;
        }

        // 규칙 2: 이메일 도메인 기반
        if (rule.emailDomain && userContext.email.endsWith(rule.emailDomain)) {
            return rule.value;
        }

        // 규칙 3: 그룹 멤버십
        if (rule.group && userContext.groups.includes(rule.group)) {
            return rule.value;
        }

        // 규칙 4: 백분율 롤아웃 (일관된 분배)
        if (rule.percentage !== undefined) {
            // 사용자 ID를 해싱하여 일관된 분배 보장
            const hash = murmurhash3(flagKey + userContext.key);
            const bucket = (hash % 100) + 1;  // 1-100
            if (bucket <= rule.percentage) {
                return rule.value;
            }
        }
    }

    // 4. 기본값 반환
    return flag.defaultValue || false;
}
```

**3단계: 코드 내 플래그 사용**
```java
// Spring Boot + LaunchDarkly 예시
@Service
public class CheckoutService {

    private final LDClient featureFlagClient;
    private final NewCheckoutService newCheckoutService;
    private final LegacyCheckoutService legacyCheckoutService;

    public CheckoutResult processCheckout(Order order, User user) {
        // 사용자 컨텍스트 구성
        LDContext context = LDContext.builder()
            .key(user.getId())
            .name(user.getName())
            .email(user.getEmail())
            .set("country", user.getCountry())
            .set("plan", user.getPlan())
            .build();

        // 플래그 평가
        boolean useNewCheckout = featureFlagClient.boolVariation(
            "new-checkout-flow",
            context,
            false  // 기본값
        );

        // 조건부 실행
        if (useNewCheckout) {
            return newCheckoutService.process(order);
        } else {
            return legacyCheckoutService.process(order);
        }
    }
}
```

### 4. 실무 코드 예시 (OpenFeature 표준)

```java
// OpenFeature - 벤더 중립적 피처 플래그 API 표준
// 1. 의존성 추가
/*
<dependency>
    <groupId>dev.openfeature</groupId>
    <artifactId>sdk</artifactId>
    <version>1.0.0</version>
</dependency>
<dependency>
    <groupId>dev.openfeature.contrib.providers</groupId>
    <artifactId>flagd</artifactId>
    <version>0.5.0</version>
</dependency>
*/

// 2. 프로바이더 설정
import dev.openfeature.sdk.OpenFeatureAPI;
import dev.openfeature.contrib.providers.flagd.FlagdProvider;

@Configuration
public class FeatureFlagConfig {

    @PostConstruct
    public void init() {
        // Flagd 프로바이더 설정 (오픈소스)
        FlagdProvider provider = FlagdProvider.builder()
            .host("flagd.example.com")
            .port(8015)
            .build();

        OpenFeatureAPI.getInstance().setProvider(provider);
    }
}

// 3. 서비스에서 사용
@Service
public class PaymentService {

    private final OpenFeatureAPI featureFlagClient = OpenFeatureAPI.getInstance();

    public PaymentResult processPayment(PaymentRequest request, User user) {
        // 컨텍스트 구성
        EvaluationContext context = ImmutableContext.builder()
            .targetingKey(user.getId())
            .set("email", new StringValue(user.getEmail()))
            .set("country", new StringValue(user.getCountry()))
            .set("plan", new StringValue(user.getPlan()))
            .build();

        // 1. 불리언 플래그
        boolean useNewGateway = featureFlagClient.getClient()
            .getBooleanValue("new-payment-gateway", false, context);

        // 2. 문자열 플래그 (다양한 백엔드 선택)
        String gatewayProvider = featureFlagClient.getClient()
            .getStringValue("payment-gateway-provider", "stripe", context);

        // 3. 정수 플래그 (타임아웃 설정)
        int timeout = featureFlagClient.getClient()
            .getIntegerValue("payment-timeout-ms", 5000, context);

        // 4. 객체 플래그 (복잡한 설정)
        Structure gatewayConfig = featureFlagClient.getClient()
            .getObjectValue("gateway-config", new ImmutableStructure(), context);

        // 조건부 실행
        if (useNewGateway) {
            return newPaymentGateway.charge(request, gatewayProvider, timeout);
        } else {
            return legacyPaymentGateway.charge(request);
        }
    }
}

// 4. A/B 테스트를 위한 이벤트 추적
@Service
public class AnalyticsService {

    public void trackExperiment(User user, String experimentKey, String variant) {
        Map<String, Object> event = Map.of(
            "event_type", "experiment_viewed",
            "user_id", user.getId(),
            "experiment_key", experimentKey,
            "variant", variant,
            "timestamp", Instant.now().toEpochMilli()
        );

        analyticsClient.track(event);
    }
}
```

```yaml
# flagd 플래그 정의 파일 (flag-config.json)
{
  "flags": {
    "new-checkout-flow": {
      "state": "ENABLED",
      "variants": {
        "on": true,
        "off": false
      },
      "defaultVariant": "off",
      "targeting": {
        "if": [
          {
            "in": ["@company.com", { "var": ["email"] }]
          },
          "on",
          {
            "in": [{ "var": ["userId"] }, ["123", "456", "789"]]
          },
          "on",
          {
            "fractionalEvaluation": [
              { "var": ["userId"] },
              [
                [20, "on"],
                [80, "off"]
              ]
            ]
          },
          "on",
          "off"
        ]
      }
    }
  }
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 피처 플래그 플랫폼 비교표

| 평가 지표 | LaunchDarkly | Unleash | Flagsmith | AWS AppConfig |
| :--- | :--- | :--- | :--- | :--- |
| **라이선스** | 상용 | 오픈소스/상용 | 오픈소스/상용 | AWS 서비스 |
| **호스팅** | Cloud | Self-hosted/Cloud | Self-hosted/Cloud | AWS |
| **실시간 업데이트** | ✓ (Streaming) | ✓ (WebSocket) | ✓ | ✓ (Polling) |
| **A/B 테스트** | ✓ (내장) | ✓ (플러그인) | ✓ (내장) | ✗ |
| **분석/실험** | 강력함 | 기본 | 기본 | 없음 |
| **비용** | 높음 | 무료/낮음 | 무료/낮음 | 사용량 기반 |

### 2. 피처 플래그 패턴 비교

| 패턴 | 설명 | 장점 | 단점 |
| :--- | :--- | :--- | :--- |
| **Hardcoded Flag** | 코드 내 직접 `if (flag)` | 단순함 | 배포 필요 |
| **Config File** | 설정 파일에 플래그 정의 | 배포 없이 변경 가능 | 재시작 필요 |
| **Database Flag** | DB에 플래그 저장 | 실시간, UI 관리 | DB 의존성 |
| **Feature Flag Service** | 전용 서비스 사용 | 고급 기능, 분석 | 추가 비용/복잡성 |

### 3. 과목 융합 관점 분석

**피처 플래그 + CI/CD**
- 코드는 자주 배포하고, 기능은 나중에 릴리스합니다.
- "Deploy often, release when ready"가 가능합니다.

**피처 플래그 + A/B 테스팅**
- 동일한 코드로 두 가지 UI/로직을 실험합니다.
- 통계적 유의성을 기반으로 승자를 결정합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 긴급 기능 차단 (Kill Switch)**
- **문제점**: 신규 결제 기능에서 간헐적 장애 발생. 핫픽스 배포까지 1시간 소요.
- **기술사 판단**: **Ops Toggle로 즉시 차단**.
  1. 피처 플래그 관리 콘솔에서 "new-payment" 플래그를 OFF로 변경.
  2. 30초 내 모든 서버에 전파.
  3. 사용자는 기존 결제 방식으로 자동 전환.
  4. 장애 시간: 1시간 → 1분.

**[상황 B] 피처 플래그 기술 부채 누적**
- **문제점**: 수백 개의 피처 플래그가 코드에 방치됨.
- **기술사 판단**: **플래그 정리 프로세스 수립**.
  1. 플래그 생성 시 만료일(Expires) 설정.
  2. 만료된 플래그 자동 알림.
  3. 주간 "플래그 청소의 날" 운영.

### 2. 피처 플래그 관리 체크리스트

**설계 체크리스트**
- [ ] 플래그 이름이 명확한가? (예: `checkout-v2-enabled`)
- [ ] 기본값이 안전한가? (보통 OFF)
- [ ] 폴백(Fallback)이 정의되어 있는가?

**운영 체크리스트**
- [ ] 플래그 변경이 감사 로그에 기록되는가?
- [ ] 만료된 플래그를 정기적으로 정리하는가?
- [ ] 플래그 의존 코드에 테스트가 있는가?

### 3. 안티패턴 (Anti-patterns)

**안티패턴 1: 중첩 플래그 (Nested Flags)**
- `if (flag1 && flag2 && flag3)` 같은 복잡한 조건.
- **해결**: 단일 플래그로 단순화.

**안티패턴 2: 영구 플래그 (Permanent Flags)**
- 플래그를 제거하지 않고 방치.
- **해결**: 100% 롤아웃 후 플래그 코드 제거.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 (AS-IS) | 도입 후 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **배포 주기** | 기능 완료 시 (수주) | 코드 완료 시 (수일) | **10배 단축** |
| **장애 복구 시간** | 핫픽스 배포 (1시간) | 플래그 OFF (30초) | **120배 단축** |
| **병합 충돌** | 장기 브랜치로 빈번 | 트렁크 기반으로 최소 | **90% 감소** |
| **실험 가능성** | 배포 후에만 | 언제든지 | **무제한** |

### 2. 미래 전망 및 진화 방향

**OpenFeature 표준화**
- 벤더 중립적 API 표준이 확산됩니다.
- 플래그 프로바이더를 쉽게 교체할 수 있습니다.

**AI 기반 실험 최적화**
- AI가 자동으로 최적의 타겟팅 규칙을 제안합니다.
- A/B 테스트 결과를 자동 분석합니다.

### 3. 참고 표준/가이드
- **Martin Fowler: Feature Toggles (2010)**: 원조 글
- **OpenFeature (openfeature.dev)**: 벤더 중립적 표준
- **LaunchDarkly Best Practices**: 상용 도구 가이드
- **Feature Toggles book (Pete Hodgson)**: 심층 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **[트렁크 기반 개발](./trunk_based_development.md)**: 피처 플래그가 필수인 개발 방식
- **[A/B 테스팅](./ab_testing.md)**: 피처 플래그를 활용한 실험
- **[카나리 배포](./continuous_deployment.md)**: 점진적 롤아웃에 플래그 활용
- **[지속적 배포 (CD)](./continuous_deployment.md)**: 배포와 릴리스 분리

---

## 👶 어린이를 위한 3줄 비유 설명
1. 피처 플래그는 **'조명 스위치'**예요. 새로운 전등을 설치해도 **'스위치를 끄면'** 아무도 모르죠.
2. 준비가 되면 **'스위치를 켜서'** 전등을 밝혀요. 갑자기 모든 사람이 볼 수 있죠!
3. 문제가 생기면 **'즉시 끌 수도 있어요.'** 전등을 떼러 갈 필요 없이 스위치만 누르면 돼요!
