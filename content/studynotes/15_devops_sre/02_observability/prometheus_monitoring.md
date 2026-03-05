+++
title = "프로메테우스 (Prometheus) - 메트릭 수집 및 모니터링"
description = "클라우드 네이티브 환경의 사실상 표준 메트릭 수집 시스템에 대한 심층 기술 백서"
date = 2024-05-15
[taxonomies]
tags = ["Prometheus", "Monitoring", "Metrics", "Time Series Database", "Cloud Native", "CNCF"]
+++

# 프로메테우스 (Prometheus) - 메트릭 수집 및 모니터링

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 프로메테우스(Prometheus)는 2012년 SoundCloud에서 개발되어 CNCF(Cloud Native Computing Foundation)에서 관리되는 오픈소스 시스템 모니터링 및 알림 툴킷으로, **Pull 방식의 메트릭 수집**, **다차원 데이터 모델**, **강력한 쿼리 언어(PromQL)**, **시계열 데이터베이스(TSDB)**를 핵심 특징으로 합니다.
> 2. **가치**: 프로메테우스는 분산 시스템의 상태를 실시간으로 가시화하고, SLO 기반 알림을 통해 장애를 조기에 탐지하며, Grafana와의 결합으로 직관적인 대시보드를 제공하여 DevOps/SRE 팀의 운영 효율성을 획기적으로 향상시킵니다.
> 3. **융합**: 쿠버네티스(Kubernetes)의 표준 모니터링 스택으로 자리 잡았으며, Alertmanager, Grafana, Thanos, OpenTelemetry와 결합하여 엔터프라이즈급 옵저버빌리티 플랫폼을 구축합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**프로메테우스(Prometheus)**는 현대적인 마이크로서비스 및 컨테이너 환경을 위해 설계된 **오픈소스 시스템 모니터링 및 알림 툴킷**입니다. 2016년 Kubernetes에 이어 두 번째로 CNCF 졸업 프로젝트(Graduated Project)가 되었으며, 클라우드 네이티브 생태계에서 **사실상(De facto) 메트릭 수집 표준**으로 자리 잡았습니다.

핵심 아키텍처 특징:
- **Pull 방식 수집**: 에이전트가 메트릭을 밀어주는(Push) 대신, 프로메테우스 서버가 타겟을 당겨오는(Pull) 방식
- **다차원 데이터 모델**: 메트릭 이름과 키-값 쌍(레이블)으로 구성된 시계열 데이터
- **PromQL**: 강력하고 유연한 쿼리 언어
- **단일 노드 TSDB**: 고성능 로컬 시계열 데이터베이스
- **알림 관리**: Alertmanager를 통한 알림 라우팅, 중복 제거, 사일런싱

### 💡 2. 구체적인 일상생활 비유
**건강 검진 센터**를 상상해 보세요:
- **프로메테우스 서버**: 정기적으로 환자(서버/애플리케이션)를 방문하여 건강 데이터(메트릭)를 수집하는 검진 팀입니다.
- **Pull 방식**: 환자가 데이터를 보내는 게 아니라, 검진 팀이 환자에게 직접 방문합니다. "지금 혈압이 어떠세요?"라고 물어보죠.
- **메트릭 엔드포인트(/metrics)**: 환자의 건강 상태를 보고하는 "건강 기록부"입니다. "혈압: 120/80, 심박수: 72, 체온: 36.5" 같은 데이터가 적혀 있습니다.
- **PromQL**: 의사가 "지난 1주일간 혈압 평균이 얼마야?"라고 질문하는 언어입니다.
- **Grafana 대시보드**: 건강 상태를 시각화하여 보여주는 "건강 리포트 화면"입니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (기존 모니터링 시스템)**:
   - **Nagios/Zabbix**: Push 방식 중심, 정적 설정, 클라우드 동적 환경에 부적합
   - **Graphite**: 강력하지만 설정이 복잡하고, 차원(Dimension) 지원이 제한적
   - **StatsD**: Push 방식, UDP 기반으로 데이터 손실 가능성

2. **혁신적 패러다임 변화의 시작**:
   - **2012년**: SoundCloud 엔지니어들이 Google의 Borgmon(구글 내부 모니터링 시스템)에서 영감을 받아 Prometheus 개발 시작
   - **2015년**: 오픈소스로 공개
   - **2016년**: Kubernetes에 이어 두 번째 CNCF 졸업 프로젝트
   - **현재**: 모든 주요 클라우드 프로바이더, 쿠버네티스 배포판의 기본 모니터링 스택

3. **현재 시장/산업의 비즈니스적 요구사항**:
   MSA(Microservices Architecture) 환경에서는 수백 개의 서비스가 동적으로 생성/삭제됩니다. 정적인 서버 목록을 관리하는 기존 모니터링은 불가능합니다. Prometheus의 **서비스 디스커버리(Service Discovery)**는 쿠버네티스 API를 통해 동적으로 타겟을 발견하고 모니터링합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Prometheus Server** | 메트릭 수집 및 저장 | Pull 방식 스크랩, 로컬 TSDB 저장 | HTTP /metrics, Prometheus Protocol | 건강 검진 팀 |
| **Exporters** | 제3자 시스템 메트릭 변환 | 시스템(CPU, 메모리)을 프로메테우스 형식으로 변환 | Node Exporter, mysqld_exporter | 번역기 |
| **Pushgateway** | 단기 배치잡 메트릭 수집 | 수명이 짧은 잡이 메트릭을 푸시 | HTTP Push | 임시 보관함 |
| **Alertmanager** | 알림 처리 및 라우팅 | 중복 제거, 그룹핑, 라우팅, 사일런싱 | Slack, PagerDuty, Email | 비상 연락망 |
| **PromQL** | 쿼리 언어 | 시계열 데이터 조회 및 연산 | PromQL 엔진 | 질문 언어 |

### 2. 정교한 구조 다이어그램: Prometheus 아키텍처

```text
=====================================================================================================
                    [ Prometheus Complete Architecture ]
=====================================================================================================

+-------------------------------------------------------------------------------------------+
|                              [ PROMETHEUS ECOSYSTEM ]                                     |
|                                                                                           |
|  +-------------+     +-------------+     +-------------+     +-------------+              |
|  | Application |     | Application |     | Kubernetes  |     | MySQL       |              |
|  | (Java)      |     | (Go)        |     | Node        |     | Database    |              |
|  |             |     |             |     |             |     |             |              |
|  | /metrics    |     | /metrics    |     | Node        |     | mysqld_     |              |
|  | endpoint    |     | endpoint    |     | Exporter    |     | exporter    |              |
|  +------+------+     +------+------+     +------+------+     +------+------+              |
|         │                   │                   │                   │                      |
|         │    (Pull 방식으로 메트릭 수집)        │                   │                      |
|         │                   │                   │                   │                      |
|         └───────────────────┼───────────────────┼───────────────────┘                      |
|                             │                   │                                          |
|                             ▼                   ▼                                          |
|  +-----------------------------------------------------------------------+               |
|  |                      [ PROMETHEUS SERVER ]                            |               |
|  |                                                                       |               |
|  |  +-------------------+    +-------------------+    +---------------+  |               |
|  |  | Retrieval         │    │ TSDB              │    │ HTTP Server   |  |               |
|  |  | (Scraping Engine) │───>│ (Time Series DB)  │<───│ (Query API)   │  |               |
|  |  |                   │    │                   │    │               │  |               |
|  |  | - Service         │    │ - Local Storage   │    │ - /api/v1/    │  |               |
|  |  │   Discovery       │    │ - Compression     │    │   query       │  |               |
|  |  | - Scraping        │    │ - Retention       │    │ - /metrics    │  |               |
|  |  │   (Pull)          │    │   (15일 기본)     │    │               │  |               |
|  |  +-------------------+    +-------------------+    +---------------+  |               |
|  |           │                                                │              |               |
|  |           │ PromQL Query                                   │ Alerts       |               |
|  |           ▼                                                ▼              |               |
|  |  +-------------------+                          +-------------------+  |               |
|  |  | PromQL Engine     │                          | Rules Evaluator   │  |               |
|  |  | (Query Parser)    │                          | (Alert Rules)     │  |               |
|  |  +-------------------+                          +-------------------+  |               |
|  +-----------------------------------------------------------------------+               |
|                             │                                   │                          |
|                             │                                   │                          |
|              ┌──────────────┴──────────────┐       ┌───────────┴───────────┐              |
|              │                             │       │                       │              |
|              ▼                             ▼       ▼                       ▼              |
|  +-------------------+          +-------------------+          +-------------------+      |
|  | GRAFANA           │          | ALERTMANAGER      │          | OTHER CLIENTS     │      |
|  | (Visualization)   │          | (Alert Routing)   │          | (Custom Scripts)  │      |
|  |                   │          |                   |          |                   |      |
|  | - Dashboard       │          | - Deduplication   │          │ - PromQL CLI      |      |
|  | - Panels          │          | - Grouping        │          │ - API Consumers   │      |
|  | - Alerting        │          │ - Routing         │          │                   |      |
|  +-------------------+          │ - Silencing       │          +-------------------+      |
|                                 │ - Inhibition      │                                     |
|                                 +-------------------+                                     |
|                                       │                                                 |
|                         ┌─────────────┼─────────────┐                                   |
|                         │             │             │                                    │
|                         ▼             ▼             ▼                                    │
|                   +----------+ +----------+ +----------+                                 │
|                   │ Slack    │ │ PagerDuty│ │ Email    │                                 │
|                   │ (Teams)  │ │ (On-call)│ │ (Report) │                                 │
|                   +----------+ +----------+ +----------+                                 |
+-------------------------------------------------------------------------------------------+

=====================================================================================================
   ※ 핵심 데이터 흐름:
   1. Prometheus Server가 주기적으로(기본 15초) Targets의 /metrics 엔드포인트를 Pull
   2. 수집된 메트릭이 로컬 TSDB에 저장
   3. Grafana가 PromQL로 쿼리하여 대시보드 렌더링
   4. Alert Rule이 위반되면 Alertmanager로 알림 전송
   5. Alertmanager가 Slack, PagerDuty 등으로 알림 라우팅
=====================================================================================================
```

### 3. 심층 동작 원리 (메트릭 수집 및 저장)

**1단계: 서비스 디스커버리 (Service Discovery)**
```yaml
# prometheus.yml - 서비스 디스커버리 설정
scrape_configs:
  # Kubernetes Pod 자동 발견
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # prometheus.io/scrape: "true" 어노테이션이 있는 파드만 수집
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true

  # 정적 타겟 (직접 지정)
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100', 'node-exporter-2:9100']
```

**2단계: 메트릭 스크랩 (Scraping)**
```text
# /metrics 엔드포인트 예시 (Prometheus Exposition Format)
# HELP http_requests_total Total number of HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",status="200"} 12345
http_requests_total{method="POST",status="201"} 6789
http_requests_total{method="GET",status="500"} 12

# HELP http_request_duration_seconds HTTP request latency
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{le="0.1"} 5000
http_request_duration_seconds_bucket{le="0.5"} 9000
http_request_duration_seconds_bucket{le="1.0"} 11000
http_request_duration_seconds_bucket{le="+Inf"} 12000
http_request_duration_seconds_sum 5400.5
http_request_duration_seconds_count 12000
```

**3단계: TSDB 저장 (Storage)**
```
시계열 데이터 구조:
┌─────────────────────────────────────────────────────────────┐
│ 메트릭 이름: http_requests_total                            │
│ 레이블: {method="GET", status="200"}                        │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 타임스탬프          │ 값                                 │ │
│ │ 1704067200000       │ 12340                              │ │
│ │ 1704067215000       │ 12341  (+1)                        │ │
│ │ 1704067230000       │ 12343  (+2)                        │ │
│ │ 1704067245000       │ 12345  (+2)                        │ │
│ │ ...                  │ ...                                │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

※ TSDB 특징:
- 채크(Chunk) 단위 압축 (Gorilla 알고리즘 기반)
- 레이블 기반 인덱싱 (Inverted Index)
- 보존 기간(Retention) 기반 자동 삭제
```

**4단계: PromQL 쿼리 (Querying)**
```promql
# [1] 초당 요청 수 (Rate)
# 지난 5분간 http_requests_total의 초당 증가율
rate(http_requests_total[5m])

# [2] 상태 코드별 에러율
sum(rate(http_requests_total{status=~"5.."}[5m]))
  /
sum(rate(http_requests_total[5m]))

# [3] P99 응답 시간
histogram_quantile(0.99,
  rate(http_request_duration_seconds_bucket[5m])
)

# [4] CPU 사용률 상위 5개 서비스
topk(5,
  sum by (service) (rate(container_cpu_usage_seconds_total[5m]))
)

# [5] SLO 위반 감지 (에러율 1% 초과)
(
  sum(rate(http_requests_total{status=~"5.."}[1h]))
  /
  sum(rate(http_requests_total[1h]))
) > 0.01
```

### 4. 실무 코드 예시 (Spring Boot 통합)

```java
// Spring Boot 애플리케이션에 Prometheus 메트릭 노출

// 1. 의존성 추가 (pom.xml)
/*
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
*/

// 2. 커스텀 메트릭 정의
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.springframework.stereotype.Component;

@Component
public class OrderMetrics {

    private final Counter orderCounter;
    private final Timer orderProcessingTime;

    public OrderMetrics(MeterRegistry registry) {
        // 주문 건수 카운터
        this.orderCounter = Counter.builder("orders_total")
            .description("Total number of orders")
            .tag("status", "created")
            .register(registry);

        // 주문 처리 시간 타이머
        this.orderProcessingTime = Timer.builder("order_processing_duration")
            .description("Time taken to process an order")
            .publishPercentiles(0.5, 0.95, 0.99)  // P50, P95, P99
            .register(registry);
    }

    public void recordOrderCreated() {
        orderCounter.increment();
    }

    public void recordOrderProcessingTime(Runnable processing) {
        orderProcessingTime.record(processing);
    }
}

// 3. 서비스에서 메트릭 사용
@Service
public class OrderService {

    private final OrderMetrics metrics;

    public void createOrder(OrderRequest request) {
        metrics.recordOrderProcessingTime(() -> {
            // 주문 처리 로직
            Order order = processOrder(request);

            // 주문 생성 메트릭 기록
            metrics.recordOrderCreated();
        });
    }
}
```

```yaml
# application.yml - Prometheus 엔드포인트 활성화
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus,metrics
  metrics:
    tags:
      application: ${spring.application.name}
    distribution:
      percentiles-histogram:
        http.server.requests: true

# Kubernetes Deployment - Prometheus 어노테이션
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  template:
    metadata:
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/actuator/prometheus"
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 모니터링 시스템 비교표

| 평가 지표 | Prometheus | Datadog | InfluxDB | VictoriaMetrics |
| :--- | :--- | :--- | :--- | :--- |
| **라이선스** | 오픈소스 (Apache 2.0) | 상용 | 오픈소스 (MIT) | 오픈소스 (Apache 2.0) |
| **수집 방식** | Pull | Push/Pull | Push | Pull |
| **데이터 모델** | 레이블 기반 | 태그 기반 | 태그 기반 | 레이블 기반 |
| **쿼리 언어** | PromQL | Proprietary | InfluxQL/Flux | MetricsQL |
| **확장성** | Thanos로 확장 | SaaS (무제한) | Cluster 버전 | 기본적으로 수평 확장 |
| **비용** | 무료 (인프라 비용만) | 호스트 기반 과금 | 무료/상용 | 무료/상용 |
| **클라우드 네이티브** | 매우 높음 | 높음 | 중간 | 매우 높음 |

### 2. 메트릭 유형 비교

| 메트릭 유형 | 설명 | 사용 사례 | PromQL 예시 |
| :--- | :--- | :--- | :--- |
| **Counter** | 단조 증가값 (리셋 가능) | 요청 수, 에러 수 | `rate(http_requests_total[5m])` |
| **Gauge** | 임의로 증감하는 값 | 온도, 메모리 사용량 | `node_memory_available_bytes` |
| **Histogram** | 값의 분포를 버킷으로 관찰 | 응답 시간, 요청 크기 | `histogram_quantile(0.99, ...)` |
| **Summary** | 슬라이딩 윈도우의 분위수 | (Histogram과 유사하지만 서버 사이드 계산) | `http_request_duration_seconds` |

### 3. 과목 융합 관점 분석

**Prometheus + Kubernetes**
- Prometheus Operator가 Kubernetes 네이티브 방식으로 Prometheus를 관리합니다.
- ServiceMonitor, PodMonitor CRD로 타겟을 선언적으로 정의합니다.

**Prometheus + SRE (SLO/SLI)**
- SLO(서비스 수준 목표)를 PromQL로 정의하고, 에러 버짯 소진율을 계산합니다.
- Burn Rate 알림으로 빠르게 소진되는 버짓을 탐지합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 장기 보존이 필요한 메트릭 (컴플라이언스)**
- **문제점**: Prometheus 기본 보존 기간(15일)으로는 1년 치 메트릭 보관 불가. 감사 요구사항 충족 불가.
- **기술사 판단**: **Thanos 또는 VictoriaMetrics 도입**.
  - Thanos: Prometheus를 확장하여 무제한 보존, 고가용성, 글로벌 쿼리 뷰 제공
  - VictoriaMetrics: Prometheus 호환, 더 높은 압축률, 수평 확장 지원

**[상황 B] Pull 방식이 불가능한 환경 (방화벽, 배치잡)**
- **문제점**: 외부에서 접근 불가능한 내부망 서버 또는 수명이 짧은 배치잡은 Pull 수집 불가.
- **기술사 판단**: **Pushgateway 또는 Prometheus Pushmode**.
  - 배치잡이 완료 후 Pushgateway에 메트릭 푸시
  - Prometheus가 Pushgateway에서 Pull

### 2. Prometheus 구축 체크리스트

**구성 체크리스트**
- [ ] 스크랩 간격(Scrape Interval)이 적절한가? (기본 15초, 과도하면 부하)
- [ ] 보존 기간(Retention)이 비즈니스 요구사항을 충족하는가?
- [ ] 레이블 카디널리티가 너무 높지 않은가? (userID 같은 무한 레이블 금지)
- [ ] Alertmanager가 중복 알림을 방지하는가?

**운영 체크리스트**
- [ ] Prometheus 서버의 디스크 사용량을 모니터링하는가?
- [ ] TSDB 압축(Compaction)이 정상적으로 수행되는가?
- [ ] 스크랩 실패(Scrape Failure)를 감지하는가?

### 3. 안티패턴 (Anti-patterns)

**안티패턴 1: 높은 카디널리티 (High Cardinality)**
- `http_requests_total{user_id="12345678"}` 처럼 무한한 값의 레이블 사용.
- **문제**: 메모리 폭발, 쿼리 느려짐, TSDB 손상.
- **해결**: 레이블은 유한한 값만 사용 (status code, method 등).

**안티패턴 2: Push 방식 오남용**
- 모든 메트릭을 Pushgateway로 푸시.
- **문제**: Pull 방식의 장점(서비스 디스커버리, 헬스 체크) 상실.
- **해결**: Pushgateway는 배치잡에만 제한적으로 사용.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 (AS-IS) | 도입 후 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **장애 탐지 시간 (MTTD)** | 수십 분 ~ 수시간 | 1~5분 | **90% 단축** |
| **온콜 알림 정확도** | 50% (노이즈 많음) | 95% (SLO 기반) | **90% 향상** |
| **대시보드 조회 속도** | 수십 초 | 1초 이내 | **20배 향상** |
| **인프라 비용** | 상용 도구 과금 | 오픈소스 무료 | **100% 절감** |

### 2. 미래 전망 및 진화 방향

**OpenTelemetry 통합**
- OpenTelemetry가 메트릭 수집의 표준으로 자리잡고 있습니다.
- Prometheus는 OTLP(OpenTelemetry Protocol)를 지원하여 통합됩니다.

**AI 기반 이상 탐지**
- 기존의 정적 임계치(Threshold) 알림에서 AI 기반 이상 탐지(Anomaly Detection)로 진화합니다.
- Prometheus 메트릭을 ML 모델의 입력으로 사용합니다.

### 3. 참고 표준/가이드
- **Prometheus Documentation (prometheus.io)**: 공식 문서
- **Prometheus Operator (github.com/prometheus-operator)**: Kubernetes 네이티브 배포
- **SRE Workbook (Google)**: SLO 기반 알림 설계
- **CNCF Observability Whitepaper**: 옵저버빌리티 표준 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **[옵저버빌리티 기초](@/studynotes/15_devops_sre/02_observability/observability_fundamentals.md)**: Prometheus가 구현하는 메트릭 기반 관측성
- **[Grafana 대시보드](./grafana_dashboard.md)**: Prometheus 데이터를 시각화하는 플랫폼
- **[SRE 원칙](@/studynotes/15_devops_sre/01_sre/sre_principles.md)**: SLO/SLI 측정을 위한 Prometheus 활용
- **[Alertmanager](./alertmanager.md)**: Prometheus 알림을 라우팅하는 시스템

---

## 👶 어린이를 위한 3줄 비유 설명
1. Prometheus는 **'건강 검진 로봇'**이에요. 여러 병원(서버)을 돌아다니며 "혈압이 어때요?"라고 물어보고 기록해요.
2. 로봇이 물어보면 병원에서 **'혈압 120, 심박수 72'**라고 대답해요. 로봇은 이걸 **'건강 기록부(TSDB)'**에 적어요.
3. 나중에 의사(Grafana)가 **"지난 일주일간 혈압이 어땠어?"**라고 물어보면, 로봇이 **'그래프'**를 그려서 보여줘요. 혈압이 너무 높으면 **'비상 알림'**도 보내죠!
