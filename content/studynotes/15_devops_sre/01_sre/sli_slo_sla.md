+++
title = "SLI/SLO/SLA (서비스 수준 지표/목표/협약)"
categories = ["studynotes-15_devops_sre"]
+++

# SLI/SLO/SLA (서비스 수준 지표/목표/협약)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SLI(측정 가능한 서비스 상태 지표), SLO(내부 목표값), SLA(고객과의 법적 계약)로 구성된 계층적 서비스 품질 관리 체계로, 시스템 신뢰성을 정량화하고 비즈니스 목표와 기술 운영을 수학적으로 연결합니다.
> 2. **가치**: 모호한 "시스템 안정성"을 구체적인 수치로 변환하여, 개발 속도와 안정성 사이의 트레이드오프를 데이터 기반으로 의사결정할 수 있게 합니다.
> 3. **융합**: 에러 버짯(Error Budget) 계산의 기반이 되며, CI/CD 파이프라인, 모니터링 시스템, 그리고 비즈니스 KPI와 통합됩니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)

**SLI (Service Level Indicator, 서비스 수준 지표)**는 서비스의 건전성을 나타내는 정량적으로 측정 가능한 지표입니다. 예를 들어 "지난 5분간 HTTP 요청 성공률 99.7%", "P99 응답 지연 시간 245ms" 등이 SLI입니다.

**SLO (Service Level Objective, 서비스 수준 목표)**는 SLI가 달성해야 하는 목표값으로, 비즈니스 팀과 기술팀이 합의한 내부 목표입니다. 예: "월간 가용성 99.9%", "P95 응답 지연 200ms 이하".

**SLA (Service Level Agreement, 서비스 수준 협약)**는 고객과 맺은 법적 구속력이 있는 계약으로, SLO를 달성하지 못할 경우 보상(위약금, 서비스 크레딧)을 명시합니다.

### 2. 구체적인 일상생활 비유

**건강 검진 시스템**으로 비유해 봅시다.

- **SLI (혈압 측정값)**: 의사가 혈압계로 측정한 실제 수치 (예: 수축기 125mmHg)
- **SLO (정상 혈압 범위)**: 의학적으로 정의된 건강한 혈압 목표 (예: 120/80mmHg 이하)
- **SLA (건강 보험 계약)**: 보험사와의 계약으로, 혈압이 일정 수치를 초과하면 보험료 인상 또는 보상 지급

### 3. 등장 배경 및 발전 과정

**1단계: 기존 기술의 치명적 한계점**
- "시스템이 안정적인가?"라는 질문에 "네, 괜찮습니다" 같은 모호한 답변
- 장애 발생 시 감정적 논쟁: "개발팀이 버그 코드를 올렸다" vs "운영팀이 배포를 막았다"
- 비즈니스 팀과 기술팀 간의 서로 다른 언어 사용

**2단계: 혁신적 패러다임 변화**
- 2000년대 후반 구글이 대규모 분산 시스템 운영을 위해 SRE 프레임워크 개발
- "직감이 아닌 수학적 모델로 신뢰성을 관리하자"는 철학
- 2016년 구글 SRE 북스 출간으로 산업계에 전파

**3단계: 현재 시장/산업의 비즈니스적 요구사항**
- MSA 환경에서 수백 개 서비스의 품질을 일관되게 측정 필요
- 클라우드 서비스(AWS, GCP, Azure)의 표준 품질 지표로 정착
- FinOps, DevOps와의 연계로 비즈니스-기술 정렬 도구로 활용

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 계산 공식/예시 | 비유 |
|:---|:---|:---|:---|:---|
| **SLI** | 서비스 상태 측정값 | Prometheus가 메트릭 수집 후 비율 계산 | 성공 요청수 / 전체 요청수 × 100 | 혈압 측정값 |
| **SLO** | 내부 목표값 | 비즈니스-기술 합의 후 대시보드 설정 | 99.9% 가용성 = 43분/월 다운타임 허용 | 정상 혈압 범위 |
| **SLA** | 고객과의 법적 계약 | 법무팀 검토 후 서비스 약관에 명시 | SLO 위반 시 서비스 크레딧 10% 지급 | 건강 보험 계약 |
| **Error Budget** | SLO 여유분 | 100% - SLO | 0.1% = 한 달간 43분 장애 허용 | 보험 한도 |
| **Burn Rate** | 버짯 소진 속도 | 단위 시간당 에러 발생률 / 허용 에저율 | 14.4x = 1시간에 5% 소진 | 연료 소비율 |

### 2. 정교한 구조 다이어그램: SLI/SLO/SLA 계층 구조

```text
================================================================================
                    [ SLI/SLO/SLA Hierarchy & Feedback Loop ]
================================================================================

    [ Business Layer - 고객/비즈니스 관점 ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  SLA (Service Level Agreement)                                          │
    │  - 법적 구속력 있는 계약                                                  │
    │  - 예: "월 99.9% 가용성 보장, 위반 시 서비스 크레딧 10% 지급"            │
    │  - SLO보다 보수적으로 설정 (위약금 방어 마진)                             │
    └──────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
    [ Internal Layer - 운영팀 내부 목표 ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  SLO (Service Level Objective)                                          │
    │  - 내부 목표값 (비즈니스-기술 합의)                                       │
    │  - 예: "P95 지연 200ms, 가용성 99.95%"                                   │
    │  - Error Budget = 100% - SLO                                            │
    └──────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
    [ Measurement Layer - 실제 측정 ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  SLI (Service Level Indicator)                                          │
    │  - 실제 측정값 (Prometheus, Datadog 등)                                  │
    │  - 예: "현재 P95 지연 185ms, 가용성 99.97%"                              │
    │  - SLO와 비교하여 Error Budget 계산                                      │
    └──────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
    [ Technical Implementation ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  [ Prometheus ] ──> [ PromQL ] ──> [ Grafana Dashboard ]                │
    │       │                  │                    │                          │
    │       │    sum(rate(http_requests_total{status!~"5.."}[30d]))          │
    │       │    / sum(rate(http_requests_total[30d]))                        │
    │       │                  │                    │                          │
    │       ▼                  ▼                    ▼                          │
    │  [ Metrics DB ]    [ SLI 계산 ]       [ SLO 대시보드 ]                  │
    │                                                         │               │
    │                              [ Alertmanager ] <─────────┘               │
    │                                    │                                     │
    │                                    ▼                                     │
    │                              [ Burn Rate Alert ]                         │
    └─────────────────────────────────────────────────────────────────────────┘

    [ SLO Breach Actions ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  SLO 위반 시 자동화된 액션:                                               │
    │  1. CI/CD 배포 동결 (Deployment Freeze)                                  │
    │  2. Slack/PagerDuty 알림                                                │
    │  3. JIRA 인시던트 티켓 자동 생성                                         │
    │  4. Post-mortem 스케줄링                                                │
    └─────────────────────────────────────────────────────────────────────────┘
```

### 3. 심층 동작 원리

**1단계: SLI 선정 및 정의**

서비스마다 측정해야 할 핵심 지표가 다릅니다. SRE 4대 골든 시그널을 기반으로 SLI를 선정합니다:

```yaml
# SLI 정의 예시 (OpenSLO 형식)
apiVersion: openslo/v1
kind: SLI
metadata:
  name: payment-api-availability
  displayName: Payment API Availability
spec:
  description: "결제 API의 HTTP 2xx 응답 비율"
  thresholdMetric:
    metricSource:
      type: Prometheus
      spec:
        query: |
          sum(rate(http_requests_total{service="payment",status=~"2.."}[5m]))
          /
          sum(rate(http_requests_total{service="payment"}[5m]))
```

**2단계: SLO 설정 (비즈니스 합의)**

SLO는 비즈니스 팀과 협의하여 설정합니다:

| 서비스 유형 | 권장 SLO | 월간 허용 다운타임 | 비고 |
|:---|:---|:---|:---|
| 일반 웹 서비스 | 99.9% | 43분 12초 | 대부분의 서비스 |
| 결제/금융 | 99.99% | 4분 19초 | 높은 신뢰성 필요 |
| 내부 도구 | 99% | 7시간 12분 | 낮은 SLO 허용 |
| 실험적 기능 | 95% | 36시간 | 빠른 반복 우선 |

**3단계: SLA 계약 체결 (법무 검토)**

SLA는 SLO보다 보수적으로 설정하여 위약금 지급을 방어합니다:

```
예시:
- 내부 SLO: 99.95% (22분 다운타임 허용)
- 외부 SLA: 99.9% (43분 다운타임 보장)
- 마진: 0.05% (21분) = 위약금 방어 버퍼
```

**4단계: 실시간 모니터링 및 알림**

```promql
# PromQL: SLO 대비 현재 성능 (에러 버짯 계산)
# 30일 윈도우에서 99.9% SLO 달성 여부

(
  sum(rate(http_requests_total{status!~"5.."}[30d]))
  /
  sum(rate(http_requests_total[30d]))
) * 100

# 결과가 99.9 이상이면 SLO 달성, 미만이면 위반
```

**5단계: Burn Rate 기반 알림**

Burn Rate는 에러 버짯이 얼마나 빨리 소진되는지를 나타냅니다:

```yaml
# Prometheus Alert Rules
groups:
  - name: slo_burn_rate_alerts
    rules:
      # Burn Rate 14.4x (1시간에 5% 소진) - CRITICAL
      - alert: HighBurnRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[1h]))
            /
            sum(rate(http_requests_total[1h]))
          ) > (1 - 0.999) * 14.4
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "SLO Burn Rate 위험: 1시간에 5% 소진 중"

      # Burn Rate 1x (30일에 100% 소진) - WARNING
      - alert: NormalBurnRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[30d]))
            /
            sum(rate(http_requests_total[30d]))
          ) > (1 - 0.999)
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "SLO 버짯 정상 소진 중"
```

### 4. 핵심 알고리즘 및 실무 코드

**Python으로 구현한 SLO 계산기**:

```python
#!/usr/bin/env python3
"""
SLO/SLA 계산기 - 가용성과 다운타임 계산
"""

from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

@dataclass
class SLOConfig:
    """SLO 설정"""
    availability_target: float  # 예: 0.999 (99.9%)
    window_days: int = 30       # 측정 윈도우

    @property
    def error_budget(self) -> float:
        """에러 버짯 (1 - SLO)"""
        return 1 - self.availability_target

    @property
    def allowed_downtime(self) -> timedelta:
        """허용 다운타임 계산"""
        total_minutes = self.window_days * 24 * 60
        downtime_minutes = total_minutes * self.error_budget
        return timedelta(minutes=downtime_minutes)


@dataclass
class SLIMeasurement:
    """SLI 측정값"""
    total_requests: int
    successful_requests: int
    error_requests: int

    @property
    def availability(self) -> float:
        """현재 가용성"""
        if self.total_requests == 0:
            return 1.0
        return self.successful_requests / self.total_requests

    @property
    def error_rate(self) -> float:
        """에러율"""
        if self.total_requests == 0:
            return 0.0
        return self.error_requests / self.total_requests


class SLOTracker:
    """SLO 추적기"""

    def __init__(self, config: SLOConfig):
        self.config = config
        self.measurements: list[SLIMeasurement] = []

    def add_measurement(self, measurement: SLIMeasurement):
        """측정값 추가"""
        self.measurements.append(measurement)

    def calculate_current_sli(self) -> float:
        """현재 SLI (가용성) 계산"""
        total = sum(m.total_requests for m in self.measurements)
        successful = sum(m.successful_requests for m in self.measurements)
        return successful / total if total > 0 else 1.0

    def calculate_remaining_budget(self) -> float:
        """남은 에러 버짯 (비율)"""
        current_sli = self.calculate_current_sli()
        consumed = max(0, self.config.availability_target - current_sli)
        remaining = self.config.error_budget - consumed
        return max(0, remaining)

    def calculate_burn_rate(self, window_hours: float = 1.0) -> float:
        """Burn Rate 계산 (현재 에어율 / 허용 에러율)"""
        if not self.measurements:
            return 0.0

        recent = self.measurements[-int(window_hours * 12):]  # 5분 간격 가정
        total = sum(m.total_requests for m in recent)
        errors = sum(m.error_requests for m in recent)

        if total == 0:
            return 0.0

        current_error_rate = errors / total
        allowed_error_rate = self.config.error_budget / (self.config.window_days * 24 / window_hours)

        return current_error_rate / allowed_error_rate if allowed_error_rate > 0 else 0.0

    def evaluate_policy(self) -> dict:
        """에러 버짯 기반 정책 평가"""
        remaining_percent = (self.calculate_remaining_budget() / self.config.error_budget) * 100
        burn_rate = self.calculate_burn_rate()

        if remaining_percent > 50:
            return {
                "status": "HEALTHY",
                "action": "ALLOW_ALL_DEPLOYMENTS",
                "message": f"버짯 넉넉함 ({remaining_percent:.1f}% 남음)",
                "freeze": False
            }
        elif remaining_percent > 25:
            return {
                "status": "CAUTION",
                "action": "CAUTIOUS_DEPLOYMENT",
                "message": f"버짯 주의 ({remaining_percent:.1f}% 남음)",
                "freeze": False
            }
        elif remaining_percent > 0:
            return {
                "status": "WARNING",
                "action": "FREEZE_RISKY_DEPLOYMENTS",
                "message": f"버짯 경고 ({remaining_percent:.1f}% 남음)",
                "freeze": True,
                "freeze_type": "PARTIAL"
            }
        else:
            return {
                "status": "CRITICAL",
                "action": "FULL_DEPLOYMENT_FREEZE",
                "message": "버짯 소진! 안정화 작업만 허용",
                "freeze": True,
                "freeze_type": "FULL"
            }


# 사용 예시
if __name__ == "__main__":
    # 99.9% SLO 설정
    config = SLOConfig(availability_target=0.999, window_days=30)
    print(f"SLO: {config.availability_target * 100}%")
    print(f"에러 버짯: {config.error_budget * 100}%")
    print(f"허용 다운타임: {config.allowed_downtime}")

    # SLO 추적기 생성
    tracker = SLOTracker(config)

    # 시뮬레이션: 정상 트래픽
    for _ in range(100):
        tracker.add_measurement(SLIMeasurement(
            total_requests=10000,
            successful_requests=9995,  # 99.95% 성공
            error_requests=5
        ))

    # 현재 상태 평가
    print(f"\n현재 SLI: {tracker.calculate_current_sli() * 100:.3f}%")
    print(f"남은 버짯: {tracker.calculate_remaining_budget() * 100:.3f}%")
    print(f"Burn Rate: {tracker.calculate_burn_rate():.2f}x")
    print(f"정책: {tracker.evaluate_policy()}")
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 서비스 유형별 SLI/SLO 설계

| 서비스 유형 | 핵심 SLI | 권장 SLO | 측정 도구 | 주의사항 |
|:---|:---|:---|:---|:---|
| **REST API** | 가용성, 지연 시간 | 99.9%, P95 < 200ms | Prometheus, Grafana | 클라이언트 관점 측정 |
| **스트리밍** | 프레임 드롭률, 버퍼링 | 99.5%, < 0.1% 드롭 | Custom Metrics | 네트워크 품질 영향 |
| **배치 작업** | 성공률, 완료 시간 | 99%, SLA 시간 내 완료 | Airflow, Cronitor | 지연 허용 범위 명확화 |
| **데이터베이스** | 가용성, 복제 지연 | 99.99%, < 1초 지연 | DB 메트릭, HA 모니터링 | RTO/RPO와 연계 |
| **ML 서빙** | 추론 지연, 모델 정확도 | P99 < 100ms, > 95% 정확도 | Model Monitoring | 데이터 드리프트 감지 |

### 2. 과목 융합 관점 분석

**SLI/SLO + 네트워크**:
- 네트워크 지연(Latency), 패킷 손실(Loss)을 SLI로 활용
- CDN, DNS 응답 시간을 SLO에 포함
- 네트워크 계층의 SLA와 애플리케이션 SLA 분리 관리

**SLI/SLO + 데이터베이스**:
- 쿼리 응답 시간, 복제 지연(Replication Lag)을 SLI로 측정
- DB 장애 시 RTO(Recovery Time Objective), RPO(Recovery Point Objective)를 SLO로 설정
- 백업 성공률, 복구 테스트 주기를 SLO에 포함

**SLI/SLO + 보안**:
- 인증 성공률, 보안 스캔 완료율을 SLI로 활용
- 보안 인시던트 대응 시간을 SLO로 설정
- SLA에 보안 위반 시 보상 조항 포함

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

**시나리오 A: 이커머스 플랫폼의 Black Friday 대응**
- **상황**: 평소 대비 10배 트래픽 예상, 결제 실패 방지가 최우선
- **기술사의 전략적 의사결정**:
  1. **SLI 계층화**: 전체 서비스가 아닌 '결제 API'만 별도 SLI/SLO 정의
  2. **SLO 조정**: 이벤트 기간만 99.5%로 하향 조정 (비즈니스 합의)
  3. **Burn Rate 강화**: 1시간 윈도우에서 10x 이상 시 즉시 알림
  4. **자동 스케일링**: SLO 위반 징후 시 HPA 자동 트리거

**시나리오 B: 금융사의 코어 뱅킹 시스템 SLA 협상**
- **상황**: 고객사와 99.99% SLA 요구, 내부 시스템은 99.95% 수준
- **기술사의 전략적 의사결정**:
  1. **SLA 분리**: 핵심 거래(이체, 출금)와 부가 기능(조회, 알림) 분리
  2. **다중 SLO**: 핵심 99.99%, 부가 99.9%로 계층화
  3. **마진 확보**: SLA 99.99% = SLO 99.995% + 0.005% 마진
  4. **위약금 방어**: 연속 3회 SLA 위반 시에만 보상 지급 조건

### 2. 도입 시 고려사항 (체크리스트)

**기술적 체크리스트**:
- [ ] 측정 가능한 SLI 선정 (메트릭 수집 인프라 확인)
- [ ] SLO 달성 가능성 검증 (과거 데이터 기반)
- [ ] Burn Rate 알림 임계값 설정
- [ ] CI/CD 파이프라인과 SLO 게이트 연동
- [ ] Grafana 대시보드 구축

**비즈니스적 체크리스트**:
- [ ] 비즈니스 팀과 SLO 목표값 합의
- [ ] SLA 위반 시 보상 규모 산정
- [ ] 고객 커뮤니케이션 프로세스 정의
- [ ] 법무팀 SLA 약관 검토

### 3. 주의사항 및 안티패턴 (Anti-patterns)

**안티패턴 1: 너무 많은 SLI**
- 문제: 수십 개의 SLI를 설정하여 관리 복잡도 급증
- 해결: 서비스당 3-5개 핵심 SLI에 집중

**안티패턴 2: 100% SLO 설정**
- 문제: 100% 가용성은 불가능하며, 오히려 위험한 배포 유발
- 해결: 현실적인 SLO(99.9%) 설정 후 에러 버짯 활용

**안티패턴 3: SLA = SLO 동일 설정**
- 문제: SLA 위반 시 즉시 위약금 발생
- 해결: SLA를 SLO보다 보수적으로 설정 (마진 확보)

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 (AS-IS) | 도입 후 (TO-BE) | 개선 효과 |
|:---|:---|:---|:---|
| **장애 인지 시간** | 고객 불만 후 인지 | SLO 위반 즉시 자동 알림 | 90% 단축 |
| **개발/운영 갈등** | 감정적 논쟁 | 데이터 기반 의사결정 | 협업 개선 |
| **SLA 위약금** | 빈번한 보상 지급 | 선제적 SLO 관리 | 80% 감소 |
| **배포 신뢰성** | "감으로" 판단 | SLO 기반 Go/No-Go | 객관적 판단 |

### 2. 미래 전망 및 진화 방향

**AI 기반 SLO 최적화**:
- 머신러닝으로 트래픽 패턴 학습
- 동적 SLO 조정 (시간대별, 요일별)
- 예측 기반 선제적 스케일링

**OpenSLO 표준화**:
- CNCF 주도 SLI/SLO 정의 표준화
- 다양한 도구 간 SLO 정의 호환
- IaC와 SLO 정의 통합

### 3. 참고 표준/가이드

- **Google SRE Workbook**: SLI/SLO/SLA 설계 가이드
- **OpenSLO (openslo.com)**: SLO 정의 표준 스펙
- **ITIL 4**: SLA 관리 프레임워크
- **ISO/IEC 20000**: IT 서비스 관리 표준

---

## 관련 개념 맵 (Knowledge Graph)

- [에러 버짯 (Error Budget)](@/studynotes/15_devops_sre/01_sre/error_budget.md) : SLI/SLO 기반 장애 허용 범위 계산
- [SRE 원칙](@/studynotes/15_devops_sre/01_sre/sre_principles.md) : SLI/SLO/SLA의 철학적 기반
- [옵저버빌리티](@/studynotes/15_devops_sre/02_observability/observability_fundamentals.md) : SLI 측정을 위한 모니터링 체계
- [Prometheus 모니터링](@/studynotes/15_devops_sre/02_observability/prometheus_monitoring.md) : SLI 수집 및 SLO 계산 도구
- [CI/CD 파이프라인](@/studynotes/15_devops_sre/03_automation/cicd_gitops.md) : SLO 기반 배포 게이트 구현

---

## 어린이를 위한 3줄 비유 설명

1. SLI/SLO/SLA는 **학교 시험 점수**와 같아요. SLI는 내가 실제로 받은 점수, SLO는 목표 점수, SLA는 부모님과의 약속이에요!
2. "수학 시험 90점 이상 받기로 약속했지?" 여기서 90점이 SLO(목표), 실제 점수가 SLI, 약속이 SLA예요.
3. 기업들도 이렇게 **서비스 품질에 점수를 매기고 목표를 정해서** 약속을 지키려고 노력해요!
