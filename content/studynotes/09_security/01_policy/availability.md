+++
title = "가용성 (Availability)"
date = "2026-03-04"
[extra]
categories = "studynotes-09_security"
+++

# 가용성 (Availability)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인가된 사용자가 필요할 때 언제든지 정보와 시스템에 접근하고 사용할 수 있음을 보장하는 정보보안의 핵심 속성으로, 서비스 중단을 방지하고 신속한 복구를 보장합니다.
> 2. **가치**: 전자상거래의 매출 손실 방지, 의료 시스템의 생명 보호, 금융 거래의 연속성 확보 등 비즈니스 지속성의 핵심 요소입니다.
> 3. **융합**: HA 아키텍처, DRP/BCP, CDN, 로드밸런싱, DDoS 방어 등 인프라와 보안이 결합된 다층 가용성 체계의 핵심 목표입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**가용성(Availability)**은 인가된 사용자가 필요할 때 언제든지 정보, 시스템, 서비스에 접근하고 사용할 수 있는 능력을 보장하는 보안 속성입니다. 이는 단순한 "서비스 작동"을 넘어, 합의된 **SLA(Service Level Agreement)** 수준의 서비스 품질을 지속적으로 유지하는 포괄적 개념입니다.

**정보보안 표준(ISO 27000) 정의**:
> "인가된 사용자가 요구할 때 정보에 접근하고 사용할 수 있는 특성"

**가용성의 핵심 지표**:
- **MTBF (Mean Time Between Failures)**: 평균 고장 간격 - 높을수록 좋음
- **MTTR (Mean Time To Repair)**: 평균 수리 시간 - 낮을수록 좋음
- **가용성 수식**: Availability = MTBF / (MTBF + MTTR)

#### 2. 💡 비유를 통한 이해
가용성은 **'24시간 편의점'**에 비유할 수 있습니다.
- **영업 시간**: 24시간 연중무휴 - 99.9% 가용성
- **대체 매장**: 매장 문제 시 인근 다른 매장 이용 - 이중화
- **비상 발전기**: 정전 시에도 영업 유지 - 페일오버
- **재고 관리**: 인기 상품 항상 확보 - 로드밸런싱

#### 3. 등장 배경 및 발전 과정
1. **초기 컴퓨팅**: 메인프레임 시대의 예정된 다운타임
2. **인터넷 시대**: 1990년대 e-Commerce로 24x7 요구 등장
3. **클러스터링**: 2000년대 Active-Active HA 클러스터
4. **클라우드**: 2010년대 Auto-scaling, Multi-region
5. **SRE (Site Reliability Engineering)**: Google의 가용성 엔지니어링
6. **Chaos Engineering**: Netflix의 장애 주입 테스트

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 가용성 보호 기술 체계 (표)

| 계층 | 기술 | 목표 가용성 | RTO | RPO | 비용 |
|:---|:---|:---|:---|:---|:---|
| **단일 서버** | 없음 | ~99% | 시간~일 | 전체 손실 | 낮음 |
| **이중화 (HA)** | Active-Standby | ~99.9% | 분~시간 | 분 단위 | 중간 |
| **클러스터링** | Active-Active | ~99.99% | 초~분 | 실시간 | 높음 |
| **멀티 AZ** | 가용영역 이중화 | ~99.999% | 자동 | 실시간 | 높음 |
| **멀티 리전** | 지역 이중화 | ~99.9999% | 자동 | 실시간 | 매우 높음 |
| **글로벌 CDN** | 전 세계 분산 | ~99.99999% | 무중단 | 실시간 | 매우 높음 |

#### 2. 고가용성 아키텍처 다이어그램

```text
<<< High Availability Architecture - Multi-Tier >>>>

                         [ Global DNS / CDN ]
                                 │
                    ┌────────────┼────────────┐
                    │                         │
              [ Region A ]              [ Region B ]
                    │                         │
        ┌───────────┼───────────┐   ┌────────┼────────┐
        │           │           │   │        │        │
    [AZ-1]      [AZ-2]      [AZ-3]  [AZ-1]  [AZ-2]  [AZ-3]
        │           │           │       │       │       │
    ┌───┴───┐   ┌───┴───┐   ┌───┴───┐   │       │       │
    │  LB   │   │  LB   │   │  LB   │   │       │       │
    │(ALB)  │   │(ALB)  │   │(ALB)  │   │       │       │
    └───┬───┘   └───┬───┘   └───┬───┘   │       │       │
        │           │           │       │       │       │
    ┌───┴───────────┴───────────┴───┐   │       │       │
    │      Web Tier (Auto-Scaling)  │   │       │       │
    │  ┌─────┐ ┌─────┐ ┌─────┐     │   │       │       │
    │  │Web-1│ │Web-2│ │Web-3│     │   │       │       │
    │  └─────┘ └─────┘ └─────┘     │   │       │       │
    └───────────────┬───────────────┘   │       │       │
                    │                   │       │       │
    ┌───────────────┴───────────────┐   │       │       │
    │     App Tier (Auto-Scaling)   │   │       │       │
    │  ┌─────┐ ┌─────┐ ┌─────┐     │   │       │       │
    │  │App-1│ │App-2│ │App-3│     │   │       │       │
    │  └─────┘ └─────┘ └─────┘     │   │       │       │
    └───────────────┬───────────────┘   │       │       │
                    │                   │       │       │
    ┌───────────────┴───────────────┐   │       │       │
    │       Data Tier (Cluster)      │   │       │       │
    │  ┌────────┐    ┌────────┐     │   │       │       │
    │  │Primary │◄──►│Secondary│    │   │       │       │
    │  │ (RW)   │    │ (RO)   │     │   │       │       │
    │  └────────┘    └────────┘     │   │       │       │
    └────────────────────────────────┘   │       │       │
                                         │       │       │
                    ◄────────────────────┴───────┴───────►
                         Replication (Async/Sync)


<<< Failover Scenarios >>>

    시나리오 1: 단일 인스턴스 장애
    ┌─────────────────────────────────────────────────────┐
    │  1. Health Check 실패 감지 (3회 연속)              │
    │  2. LB에서 해당 인스턴스 제외 (Drain)              │
    │  3. Auto-Scaling 새 인스턴스 시작                  │
    │  4. 새 인스턴스 LB 등록                           │
    │  → 서비스 중단 없음 (다른 인스턴스가 처리)         │
    └─────────────────────────────────────────────────────┘

    시나리오 2: 가용영역(AZ) 장애
    ┌─────────────────────────────────────────────────────┐
    │  1. AZ 전체 장애 감지                              │
    │  2. DNS/LB 다른 AZ로 트래픽 우회                   │
    │  3. Auto-Scaling 다른 AZ에서 확장                  │
    │  4. 데이터 복제본으로 서비스 계속                  │
    │  → RTO: 1~5분, RPO: 0 (동기 복제 시)              │
    └─────────────────────────────────────────────────────┘

    시나리오 3: 리전 장애
    ┌─────────────────────────────────────────────────────┐
    │  1. Region 전체 장애 감지                          │
    │  2. Global DNS 다른 Region으로 라우팅              │
    │  3. DR Site에서 서비스 시작                        │
    │  4. 데이터 동기화 확인 후 서비스 오픈              │
    │  → RTO: 15분~1시간, RPO: 5분~1시간                │
    └─────────────────────────────────────────────────────┘
```

#### 3. 심층 동작 원리: 가용성 계산 및 설계

**① 가용성 계산 공식**

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import math

class FailureType(Enum):
    HARDWARE = "hardware"
    SOFTWARE = "software"
    NETWORK = "network"
    POWER = "power"
    HUMAN = "human"
    NATURAL = "natural"

@dataclass
class ComponentAvailability:
    """컴포넌트 가용성 정보"""
    name: str
    mtbf_hours: float  # Mean Time Between Failures (hours)
    mttr_hours: float  # Mean Time To Repair (hours)

    @property
    def availability(self) -> float:
        """가용성 계산: A = MTBF / (MTBF + MTTR)"""
        return self.mtbf_hours / (self.mtbf_hours + self.mttr_hours)

    @property
    def availability_percentage(self) -> str:
        """가용성 백분율"""
        return f"{self.availability * 100:.5f}%"

    @property
    def nines(self) -> int:
        """9의 개수 (가용성 등급)"""
        avail_str = f"{self.availability:.10f}"
        count = 0
        after_decimal = False
        for c in avail_str:
            if c == '.':
                after_decimal = True
                continue
            if after_decimal and c == '9':
                count += 1
            elif after_decimal and c != '9':
                break
        return count

    @property
    def annual_downtime(self) -> float:
        """연간 예상 다운타임 (분)"""
        minutes_per_year = 365.25 * 24 * 60
        return minutes_per_year * (1 - self.availability)

class AvailabilityCalculator:
    """
    시스템 가용성 계산기
    - 직렬 구성 가용성
    - 병렬 구성 가용성
    - 전체 시스템 가용성
    """

    @staticmethod
    def series_availability(components: List[ComponentAvailability]) -> float:
        """
        직렬 구성 가용성
        모든 컴포넌트가 작동해야 함
        A_total = A1 × A2 × A3 × ... × An
        """
        result = 1.0
        for comp in components:
            result *= comp.availability
        return result

    @staticmethod
    def parallel_availability(components: List[ComponentAvailability]) -> float:
        """
        병렬 구성 가용성 (이중화)
        하나라도 작동하면 됨
        A_total = 1 - (1-A1) × (1-A2) × ... × (1-An)
        """
        failure_prob = 1.0
        for comp in components:
            failure_prob *= (1 - comp.availability)
        return 1 - failure_prob

    @staticmethod
    def n_plus_m_availability(
        active_components: List[ComponentAvailability],
        standby_count: int
    ) -> float:
        """
        N+M 이중화 가용성
        N개 활성 + M개 대기
        """
        n = len(active_components)
        m = standby_count

        if n == 0:
            return 0.0

        # 동일한 컴포넌트라고 가정
        a = active_components[0].availability
        u = 1 - a  # Unavailability

        # 최소 N개가 작동할 확률
        from math import comb
        total_prob = 0
        for k in range(n, n + m + 1):
            # 이항 분포: k개 작동할 확률
            prob = comb(n + m, k) * (a ** k) * (u ** (n + m - k))
            total_prob += prob

        return total_prob

    @staticmethod
    def calculate_system_availability(
        tiers: List[Dict]
    ) -> Dict:
        """
        다계층 시스템 가용성 계산
        tiers: [{'name': 'web', 'components': [...], 'redundancy': 'parallel'}, ...]
        """
        tier_availabilities = []

        for tier in tiers:
            components = tier['components']
            redundancy = tier.get('redundancy', 'none')

            if redundancy == 'parallel':
                tier_avail = AvailabilityCalculator.parallel_availability(components)
            elif redundancy == 'series':
                tier_avail = AvailabilityCalculator.series_availability(components)
            else:
                tier_avail = AvailabilityCalculator.series_availability(components)

            tier_availabilities.append({
                'name': tier['name'],
                'availability': tier_avail,
                'components': len(components)
            })

        # 전체 시스템 가용성 (모든 계층의 직렬 구성)
        total_availability = 1.0
        for tier_info in tier_availabilities:
            total_availability *= tier_info['availability']

        # 연간 다운타임 계산
        minutes_per_year = 365.25 * 24 * 60
        annual_downtime = minutes_per_year * (1 - total_availability)

        return {
            'total_availability': total_availability,
            'availability_percentage': f"{total_availability * 100:.6f}%",
            'nines': sum(1 for c in f"{total_availability:.10f}".split('.')[1] if c == '9'),
            'annual_downtime_minutes': annual_downtime,
            'annual_downtime_human': AvailabilityCalculator._format_downtime(annual_downtime),
            'tier_breakdown': tier_availabilities
        }

    @staticmethod
    def _format_downtime(minutes: float) -> str:
        """다운타임을 읽기 쉬운 형식으로 변환"""
        if minutes < 1:
            return f"{minutes * 60:.1f} seconds"
        elif minutes < 60:
            return f"{minutes:.1f} minutes"
        elif minutes < 1440:  # 24 hours
            return f"{minutes / 60:.1f} hours"
        else:
            return f"{minutes / 1440:.1f} days"


class HealthCheckMonitor:
    """
    헬스체크 모니터링 시스템
    - 장애 감지
    - 자동 장애조치
    - 알림 발송
    """

    def __init__(self,
                 check_interval: int = 10,
                 failure_threshold: int = 3,
                 recovery_threshold: int = 2):
        self.check_interval = check_interval
        self.failure_threshold = failure_threshold
        self.recovery_threshold = recovery_threshold
        self.services: Dict = {}

    def register_service(self,
                         service_name: str,
                         endpoint: str,
                         criticality: str = "normal"):
        """서비스 등록"""
        self.services[service_name] = {
            'endpoint': endpoint,
            'criticality': criticality,
            'status': 'unknown',
            'consecutive_failures': 0,
            'consecutive_successes': 0,
            'last_check': None,
            'total_checks': 0,
            'total_failures': 0
        }

    def perform_health_check(self, service_name: str) -> Dict:
        """헬스체크 수행"""
        if service_name not in self.services:
            return {'error': 'Service not found'}

        service = self.services[service_name]
        service['total_checks'] += 1

        # 실제 헬스체크 (시뮬레이션)
        import random
        # 99.9% 성공률 시뮬레이션
        is_healthy = random.random() < 0.999

        if is_healthy:
            service['consecutive_failures'] = 0
            service['consecutive_successes'] += 1

            # 복구 판정
            if (service['status'] == 'unhealthy' and
                service['consecutive_successes'] >= self.recovery_threshold):
                service['status'] = 'healthy'
                self._trigger_recovery(service_name)

        else:
            service['consecutive_successes'] = 0
            service['consecutive_failures'] += 1
            service['total_failures'] += 1

            # 장애 판정
            if service['consecutive_failures'] >= self.failure_threshold:
                service['status'] = 'unhealthy'
                self._trigger_failover(service_name)

        from datetime import datetime
        service['last_check'] = datetime.utcnow().isoformat()

        return {
            'service': service_name,
            'status': service['status'],
            'healthy': is_healthy,
            'consecutive_failures': service['consecutive_failures'],
            'availability': (
                (service['total_checks'] - service['total_failures']) /
                service['total_checks'] * 100
            ) if service['total_checks'] > 0 else 0
        }

    def _trigger_failover(self, service_name: str):
        """장애조치 트리거"""
        service = self.services[service_name]
        print(f"[ALERT] Service {service_name} is UNHEALTHY")
        print(f"  Criticality: {service['criticality']}")
        print(f"  Initiating failover procedures...")

        # 장애조치 로직
        # 1. LB에서 제외
        # 2. 대기 인스턴스 활성화
        # 3. 알림 발송
        # 4. 로그 기록

    def _trigger_recovery(self, service_name: str):
        """복구 트리거"""
        print(f"[INFO] Service {service_name} has RECOVERED")
        print(f"  Returning to normal operations...")

    def get_sla_report(self) -> Dict:
        """SLA 보고서 생성"""
        report = {
            'services': [],
            'overall_availability': 0
        }

        total_checks = 0
        total_failures = 0

        for name, service in self.services.items():
            checks = service['total_checks']
            failures = service['total_failures']
            availability = ((checks - failures) / checks * 100) if checks > 0 else 100

            report['services'].append({
                'name': name,
                'status': service['status'],
                'total_checks': checks,
                'total_failures': failures,
                'availability': availability
            })

            total_checks += checks
            total_failures += failures

        report['overall_availability'] = (
            ((total_checks - total_failures) / total_checks * 100)
            if total_checks > 0 else 100
        )

        return report


# 사용 예시
if __name__ == "__main__":
    # 1. 컴포넌트 가용성 계산
    server = ComponentAvailability(
        name="Web Server",
        mtbf_hours=10000,  # 10,000 hours MTBF
        mttr_hours=1       # 1 hour MTTR
    )
    print(f"Single Server Availability: {server.availability_percentage}")
    print(f"Annual Downtime: {server.annual_downtime:.1f} minutes")

    # 2. 이중화된 시스템 가용성
    server1 = ComponentAvailability("Server-1", 10000, 1)
    server2 = ComponentAvailability("Server-2", 10000, 1)

    parallel_avail = AvailabilityCalculator.parallel_availability([server1, server2])
    print(f"\nParallel (2 servers): {parallel_avail * 100:.6f}%")

    # 3. 전체 시스템 가용성 계산
    system = AvailabilityCalculator.calculate_system_availability([
        {
            'name': 'Load Balancer',
            'components': [
                ComponentAvailability("LB-1", 50000, 0.5),
                ComponentAvailability("LB-2", 50000, 0.5)
            ],
            'redundancy': 'parallel'
        },
        {
            'name': 'Web Tier',
            'components': [
                ComponentAvailability("Web-1", 10000, 1),
                ComponentAvailability("Web-2", 10000, 1),
                ComponentAvailability("Web-3", 10000, 1)
            ],
            'redundancy': 'parallel'
        },
        {
            'name': 'Database',
            'components': [
                ComponentAvailability("DB-Primary", 20000, 2),
                ComponentAvailability("DB-Standby", 20000, 2)
            ],
            'redundancy': 'parallel'
        }
    ])

    print(f"\n=== System Availability Report ===")
    print(f"Total Availability: {system['availability_percentage']}")
    print(f"Nines: {system['nines']} nines")
    print(f"Annual Downtime: {system['annual_downtime_human']}")
```

#### 4. 가용성 등급 상세 분석

```text
<<< Availability Tiers and SLA Examples >>>

    가용성 등급     연간 다운타임      일일 다운타임    적용 시스템
    ─────────────────────────────────────────────────────────────
    99% (2 nines)   3.65일            14.4분         개발/테스트
    99.9% (3 nines) 8.77시간          1.44분         일반 비즈니스
    99.99% (4 nines) 52.6분           8.64초         전자상거래
    99.999% (5 nines) 5.26분          0.864초        금융/통신
    99.9999% (6 nines) 31.5초         0.0864초       항공우주/의료

    비용 vs 가용성 트레이드오프:

    비용 증가
        ↑
        │                                    * (99.9999%)
        │                               *
        │                          *
        │                     *
        │                *
        │           *
        │      *
        │ *
        └──────────────────────────────────────→ 가용성 증가
         99%   99.9%  99.99% 99.999% 99.9999%

    주요 클라우드 SLA 예시:
    ┌───────────────────────────────────────────────────────────┐
    │ AWS EC2 SLA: 99.99% (월 4.38분 이상 장애 시 크레딧)     │
    │ AWS S3 SLA: 99.9% (월 43.8분 이상 장애 시 크레딧)       │
    │ Azure VM SLA: 99.99% (단일 VM) / 99.95% (단일 VM)       │
    │ Google Cloud SLA: 99.95% ~ 99.99%                       │
    └───────────────────────────────────────────────────────────┘
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 이중화 방식 비교

| 방식 | 설명 | 장점 | 단점 | RTO | 비용 |
|:---|:---|:---|:---|:---|:---|
| **Active-Standby** | 대기 서버 1대 | 단순, 저렴 | 자원 낭비 | 분~시간 | 1.5x |
| **Active-Active** | 모든 서버 활용 | 성능 향상, 즉시 전환 | 복잡한 동기화 | 즉시~초 | 2x |
| **Cold Standby** | 필요 시 시작 | 최저 비용 | 느린 복구 | 시간~일 | 1.1x |
| **Warm Standby** | 준비된 상태 | 중간 비용/복구 | 관리 오버헤드 | 분~시간 | 1.3x |
| **Geographic Redundancy** | 지역 분산 | 재해 대응 | 높은 비용 | 자동~분 | 2x+ |

#### 2. 재해 복구 전략 비교

| 전략 | RTO | RPO | 비용 | 복잡도 | 설명 |
|:---|:---|:---|:---|:---|:---|
| **Backup & Restore** | 시간~일 | 시간~일 | 낮음 | 낮음 | 백업에서 복원 |
| **Pilot Light** | 시간 | 분~시간 | 중간 | 중간 | 코어만 실행 |
| **Warm Standby** | 분 | 분 | 중간 | 중간 | 축소 버전 실행 |
| **Hot Standby** | 초~분 | 실시간 | 높음 | 높음 | Full Failover |
| **Multi-Site Active** | 무중단 | 실시간 | 매우 높음 | 매우 높음 | 동시 서비스 |

#### 3. 과목 융합 관점 분석

**네트워크와 가용성**:
- DNS 기반 부하 분산: GeoDNS, Weighted Round Robin
- Anycast: BGP 기반 전역 부하 분산
- CDN: 정적 콘텐츠 캐싱으로 origin 부하 감소

**데이터베이스와 가용성**:
- 복제: Master-Slave, Multi-Master
- 샤딩: 수평 분할로 부하 분산
- Connection Pool: 연결 재사용

**클라우드와 가용성**:
- Auto Scaling: 트래픽 기반 자동 확장
- Managed Services: AWS RDS, Aurora 등 관리형
- Multi-Cloud: 클라우드 제공자 이중화

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 전자상거래 플랫폼 가용성 설계**
- **상황**: 블랙프라이데이 트래픽 10배 증가, 1분 중단 시 수억 손실
- **판단**:
  - 목표: 99.99% 가용성 (연간 52분 이하)
  - 아키텍처: Multi-AZ + Auto Scaling + CDN
  - 데이터베이스: Aurora Global Database (Cross-Region)
  - DDoS: AWS Shield Advanced + WAF

**시나리오 2: 의료 정보 시스템 BCP**
- **상황**: 병원 EMR 시스템, 24시간 서비스 필수
- **판단**:
  - 목표: 99.999% 가용성
  - RTO: 5분, RPO: 0 (데이터 손실 없음)
  - DR Site: 100km 이상 떨어진 위치
  - 정기 테스트: 분기별 DR 훈련

**시나리오 3: 금융 거래 시스템 무중단 전환**
- **상황**: 코어뱅킹 시스템 교체, 24시간 서비스 유지
- **판단**:
  - 블루-그린 배포: 신구 시스템 병렬 운영
  - 카나리 배포: 점진적 트래픽 이전
  - 롤백 계획: 5분 내 구 시스템 복귀
  - 데이터 동기화: 양방향 복제

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] 비즈니스 영향도 분석 (BIA) 완료
- [ ] RTO/RPO 요구사항 정의
- [ ] SLA 협의 및 문서화
- [ ] 단일 장애점 (SPOF) 식별 및 제거
- [ ] 헬스체크 메커니즘 구현
- [ ] 장애조치 테스트 완료
- [ ] DRP/BCP 문서화 및 교육

#### 3. 안티패턴 (Anti-patterns)
- **과도한 가용성**: 99.999% 목표로 과도한 비용 지출
- **SPOF 방치**: 로드밸런서, DB 등 단일 장애점 미해결
- **테스트 부재**: 장애조치 절차 테스트 안 함
- **백업만 의존**: DR Site 없이 백업만 보관

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | 내용 | 측정 지표 |
|:---|:---|:---|
| **정량적** | 서비스 중단 시간 감소 | 연간 다운타임 90% 감소 |
| **정량적** | 매출 손실 방지 | 장애로 인한 손실 0원 |
| **정성적** | 고객 신뢰도 향상 | NPS 점수 20% 향상 |
| **정성적** | SLA 달성 | 99.99% SLA 준수 |

#### 2. 미래 전망 및 진화 방향
- **Serverless**: 인프라 관리 없는 무한 확장
- **Edge Computing**: 지연 최소화, 분산 처리
- **AI 기반 장애 예측**: ML로 사전 장애 감지
- **Chaos Engineering**: 의도적 장애 주입으로 검증

#### 3. 참고 표준/가이드
- **ISO/IEC 27031**: ICT 비즈니스 연속성
- **ISO/IEC 22301**: 비즈니스 연속성 관리
- **NIST SP 800-34**: IT 시스템 비상계획
- **ITIL v4**: 서비스 가용성 관리

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[CIA Triad](@/studynotes/09_security/01_policy/cia_triad.md)**: 가용성을 포함한 정보보안 3대 요소
- **[DR/BCP](@/studynotes/09_security/01_policy/dr_bcp.md)**: 재해 복구 및 비즈니스 연속성
- **[DDoS 방어](@/studynotes/09_security/03_network/network_security_systems.md)**: 가용성 위협 대응
- **[네트워크 보안](@/studynotes/09_security/03_network/_index.md)**: 네트워크 가용성 기술

---

### 👶 어린이를 위한 3줄 비유 설명
1. **24시간 편의점**: 늘 문이 열려 있어서 언제든지 물건을 살 수 있죠? 시스템도 항상 작동해서 필요할 때 쓸 수 있게 하는 거예요.
2. **대타 선수**: 야구에서 주전 선수가 아프면 대타가 나오죠? 서버도 하나가 고장 나면 다른 서버가 바로 대신해요.
3. **예비 타이어**: 자동차에 스페어 타이어가 있듯이, 시스템에도 문제가 생기면 바로 쓸 수 있는 예비가 준비되어 있어요.
