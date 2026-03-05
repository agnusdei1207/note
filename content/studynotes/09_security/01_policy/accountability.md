+++
title = "책임추적성 (Accountability)"
date = "2026-03-04"
[extra]
categories = "studynotes-09_security"
+++

# 책임추적성 (Accountability)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시스템 내 모든 행위에 대해 수행 주체를 식별하고 그 행위에 대한 책임을 규명할 수 있는 능력을 보장하는 정보보안 속성입니다.
> 2. **가치**: 보안 사고 원인 분석, 내부자 위협 탐지, 컴플라이언스 감사, 법적 증거 확보를 통해 조직의 보안 거버넌스를 완성합니다.
> 3. **융합**: 감사 로그, SIEM, UEBA, 포렌식 등이 결합된 통합 추적 체계의 핵심 목표입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**책임추적성(Accountability)**은 시스템 내의 모든 작업과 이벤트에 대해 수행 주체(사용자, 프로세스, 시스템)를 식별하고, 해당 행위에 대한 책임을 추적할 수 있는 능력을 보장하는 보안 속성입니다. 이는 **감사 추적(Audit Trail)**을 통해 구현됩니다.

**ISO 7498-2 정의**:
> "보안 관련 활동을 수행한 엔티티를 추적할 수 있도록 하는 보안 서비스"

**책임추적성의 핵심 요소**:
- **식별 (Identification)**: 누가(Who)
- **인증 (Authentication)**: 신원 확인
- **인가 (Authorization)**: 권한 확인
- **감사 (Auditing)**: 행위 기록
- **부인방지 (Non-repudiation)**: 증거 보존

#### 2. 💡 비유를 통한 이해
책임추적성은 **'CCTV와 출입기록'**에 비유할 수 있습니다.
- **출입카드**: 누가 들어왔는지 기록 - 사용자 식별
- **CCTV**: 무엇을 했는지 기록 - 행위 로깅
- **보안실**: 기록 모니터링 - 실시간 감사
- **아카이브**: 과거 기록 보관 - 포렌식

#### 3. 등장 배경 및 발전 과정
1. **수동 기록**: 관공서의 방문자 기록부
2. **전산화**: 1960~70년대 시스템 로그
3. **감사 시스템**: 1980년대 C2 보안 등급 (TCSEC)
4. **SIEM**: 2000년대 보안 정보 이벤트 관리
5. **UEBA**: 2010년대 사용자 행동 분석
6. **AI 감사**: 2020년대 지능형 이상 탐지

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 책임추적성 기술 체계 (표)

| 계층 | 기술 | 기능 | 로깅 대상 | 보관 기간 |
|:---|:---|:---|:---|:---|
| **네트워크** | NetFlow, DNS 로그 | 트래픽 추적 | IP, 포트, 프로토콜 | 90일~1년 |
| **시스템** | Syslog, Windows Event | 시스템 이벤트 | 로그인, 권한 상승 | 1년~ |
| **애플리케이션** | App Log, API Gateway | 비즈니스 이벤트 | 거래, 데이터 접근 | 3년~ |
| **데이터베이스** | DB Audit, Query Log | 데이터 조작 | SELECT, INSERT, DELETE | 3년~ |
| **ID 관리** | IAM Audit | 신원 관련 | 계정 생성, 권한 변경 | 7년~ |

#### 2. 책임추적성 아키텍처 다이어그램

```text
<<< Accountability Architecture - Audit Trail System >>>

    +----------------------------------------------------------+
    |                    이벤트 발생 (Event Sources)            |
    |  +-----------+  +-----------+  +-----------+  +--------+ |
    |  | Network   |  | System    |  | App       |  | DB     | |
    |  | Device    |  | OS        |  | Server    |  | Server | |
    |  +-----------+  +-----------+  +-----------+  +--------+ |
    |       │              │              │              │      |
    +-------|--------------|--------------|--------------|------+
            │              │              │              │
            v              v              v              v
    +----------------------------------------------------------+
    |              로그 수집 계층 (Log Collection Layer)       |
    |  +----------------------------------------------------+  |
    |  |  Log Forwarders / Agents                           |  |
    |  |  - Filebeat / Fluentd / Logstash                  |  |
    |  |  - Syslog / SNMP / WEC                             |  |
    |  +----------------------------------------------------+  |
    +----------------------------------------------------------+
                                │
                                v
    +----------------------------------------------------------+
    |              로그 처리 계층 (Log Processing Layer)        |
    |  +----------------------------------------------------+  |
    |  |  Normalization & Enrichment                        |  |
    |  |  - Timestamp 표준화                                |  |
    |  |  - GeoIP 추가                                     |  |
    |  |  - Asset 정보 매핑                                |  |
    |  |  - 사용자 ID 정규화                               |  |
    |  +----------------------------------------------------+  |
    +----------------------------------------------------------+
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
            v                   v                   v
    +---------------+   +---------------+   +---------------+
    │ 실시간 분석   │   │ 장기 보관     │   │ 컴플라이언스  │
    │ (Real-time)   │   │ (Archive)     │   │ (Compliance)  │
    |  +---------+  |   |  +---------+  |   |  +---------+  |
    |  | SIEM    |  |   |  | Data    |  |   |  | WORM    |  |
    |  | Correl. |  |   |  | Lake    |  |   |  | Storage |  |
    |  +---------+  |   |  +---------+  |   |  +---------+  |
    +---------------+   +---------------+   +---------------+
            │                   │                   │
            v                   v                   v
    +----------------------------------------------------------+
    |              분석 및 대응 계층 (Analysis & Response)      |
    |  +----------------------------------------------------+  |
    |  |  UEBA (User Entity Behavior Analytics)            |  |
    |  |  - 정상 행동 학습                                  |  |
    |  |  - 이상 행동 탐지                                  |  |
    |  |  - 위험 스코어링                                   |  |
    |  +----------------------------------------------------+  |
    |  +----------------------------------------------------+  |
    |  |  SOAR (Security Orchestration & Response)         |  |
    |  |  - 자동화된 대응                                   |  |
    |  |  - 인시던트 생성                                   |  |
    |  |  - 대시보드 & 보고서                               |  |
    |  +----------------------------------------------------+  |
    +----------------------------------------------------------+

<<< 감사 이벤트 구조 (Audit Event Schema) >>>

    +----------------------------------------------------------+
    |                  Audit Event Record                      |
    +----------------------------------------------------------+
    | 필드                | 예시                               |
    +----------------------------------------------------------+
    | event_id            | EVT-20260304-001234               |
    | timestamp           | 2026-03-04T14:32:15.123Z          |
    | event_type          | USER_LOGIN                        |
    | outcome             | SUCCESS / FAILURE                 |
    +----------------------------------------------------------+
    | subject (주체)       |                                   |
    |   - user_id         | user@company.com                  |
    |   - user_name       | John Doe                          |
    |   - department      | Finance                           |
    |   - session_id      | SES-abc123                        |
    +----------------------------------------------------------+
    | object (객체)        |                                   |
    |   - resource_type   | DATABASE_TABLE                    |
    |   - resource_id     | customers_pii                    |
    |   - sensitivity     | HIGH                              |
    +----------------------------------------------------------+
    | action (행위)        |                                   |
    |   - operation       | SELECT                            |
    |   - details         | {"columns": ["ssn", "email"]}    |
    |   - records_affected| 1523                              |
    +----------------------------------------------------------+
    | context (맥락)       |                                   |
    |   - source_ip       | 192.168.1.100                     |
    |   - device_id       | DEV-laptop-001                    |
    |   - location        | Seoul, KR                         |
    |   - geo_anomaly     | false                             |
    +----------------------------------------------------------+
    | metadata            |                                   |
    |   - log_source      | db-audit-01                       |
    |   - integrity_hash  | sha256:abc123...                  |
    |   - previous_hash   | sha256:def456... (Chain)          |
    +----------------------------------------------------------+
```

#### 3. 심층 동작 원리: 감사 로깅 및 UEBA 구현

```python
import hashlib
import secrets
import json
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple, Any
from enum import Enum
from collections import defaultdict
import statistics

class EventType(Enum):
    # 인증 관련
    USER_LOGIN = "USER_LOGIN"
    USER_LOGOUT = "USER_LOGOUT"
    AUTH_FAILURE = "AUTH_FAILURE"
    MFA_CHALLENGE = "MFA_CHALLENGE"
    PASSWORD_CHANGE = "PASSWORD_CHANGE"

    # 접근 제어
    ACCESS_GRANTED = "ACCESS_GRANTED"
    ACCESS_DENIED = "ACCESS_DENIED"
    PRIVILEGE_ESCALATION = "PRIVILEGE_ESCALATION"

    # 데이터 접근
    DATA_READ = "DATA_READ"
    DATA_WRITE = "DATA_WRITE"
    DATA_DELETE = "DATA_DELETE"
    DATA_EXPORT = "DATA_EXPORT"

    # 시스템
    SYSTEM_CONFIG_CHANGE = "SYSTEM_CONFIG_CHANGE"
    USER_CREATED = "USER_CREATED"
    USER_DELETED = "USER_DELETED"
    ROLE_ASSIGNED = "ROLE_ASSIGNED"

class RiskLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class AuditEvent:
    """감사 이벤트"""
    event_id: str
    timestamp: str
    event_type: EventType
    outcome: str  # SUCCESS, FAILURE, PENDING

    # 주체 (Subject)
    user_id: str
    user_name: str
    session_id: Optional[str] = None

    # 객체 (Object)
    resource_type: str
    resource_id: str
    sensitivity: str = "NORMAL"

    # 행위 (Action)
    operation: str
    details: Dict = field(default_factory=dict)
    records_affected: int = 0

    # 맥락 (Context)
    source_ip: str = "unknown"
    device_id: str = "unknown"
    location: str = "unknown"

    # 무결성
    previous_hash: str = ""
    event_hash: str = ""

    def compute_hash(self) -> str:
        """이벤트 해시 계산 (체인 구조)"""
        event_data = {
            'event_id': self.event_id,
            'timestamp': self.timestamp,
            'event_type': self.event_type.value,
            'outcome': self.outcome,
            'user_id': self.user_id,
            'resource_id': self.resource_id,
            'operation': self.operation,
            'previous_hash': self.previous_hash
        }
        event_bytes = json.dumps(event_data, sort_keys=True).encode()
        return hashlib.sha256(event_bytes).hexdigest()

    def to_dict(self) -> dict:
        return {
            'event_id': self.event_id,
            'timestamp': self.timestamp,
            'event_type': self.event_type.value,
            'outcome': self.outcome,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'session_id': self.session_id,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'sensitivity': self.sensitivity,
            'operation': self.operation,
            'details': self.details,
            'records_affected': self.records_affected,
            'source_ip': self.source_ip,
            'device_id': self.device_id,
            'location': self.location,
            'previous_hash': self.previous_hash,
            'event_hash': self.event_hash
        }

class AuditLog:
    """
    감사 로그 관리
    - 이벤트 기록
    - 체인 구조로 무결성 보장
    - 검색 및 분석
    """

    def __init__(self):
        self.events: List[AuditEvent] = []
        self.last_hash = "0" * 64  # 제네시스 해시
        self.index: Dict[str, List[int]] = {
            'user': defaultdict(list),
            'type': defaultdict(list),
            'resource': defaultdict(list)
        }

    def log_event(self, event: AuditEvent) -> AuditEvent:
        """이벤트 로깅"""
        event.event_id = f"EVT-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{secrets.token_hex(4)}"
        event.timestamp = datetime.now(timezone.utc).isoformat()
        event.previous_hash = self.last_hash
        event.event_hash = event.compute_hash()

        self.events.append(event)
        event_index = len(self.events) - 1

        # 인덱스 업데이트
        self.index['user'][event.user_id].append(event_index)
        self.index['type'][event.event_type.value].append(event_index)
        self.index['resource'][event.resource_id].append(event_index)

        self.last_hash = event.event_hash
        return event

    def verify_integrity(self) -> Tuple[bool, List[int]]:
        """로그 체인 무결성 검증"""
        violations = []
        previous_hash = "0" * 64

        for i, event in enumerate(self.events):
            if event.previous_hash != previous_hash:
                violations.append(i)
            else:
                computed = event.compute_hash()
                if computed != event.event_hash:
                    violations.append(i)

            previous_hash = event.event_hash

        return len(violations) == 0, violations

    def search_by_user(self, user_id: str) -> List[AuditEvent]:
        """사용자별 검색"""
        return [self.events[i] for i in self.index['user'].get(user_id, [])]

    def search_by_type(self, event_type: EventType) -> List[AuditEvent]:
        """이벤트 유형별 검색"""
        return [self.events[i] for i in self.index['type'].get(event_type.value, [])]

    def search_by_time_range(self,
                              start: datetime,
                              end: datetime) -> List[AuditEvent]:
        """시간 범위 검색"""
        results = []
        for event in self.events:
            event_time = datetime.fromisoformat(event.timestamp.replace('Z', '+00:00'))
            if start <= event_time <= end:
                results.append(event)
        return results

class BehaviorProfile:
    """사용자 행동 프로필"""
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.login_times: List[int] = []  # 시간대 (0-23)
        self.login_locations: Dict[str, int] = defaultdict(int)
        self.accessed_resources: Dict[str, int] = defaultdict(int)
        self.typical_data_volume: List[int] = []
        self.session_durations: List[int] = []
        self.devices_used: Dict[str, int] = defaultdict(int)

    def update(self, event: AuditEvent):
        """프로필 업데이트"""
        if event.event_type == EventType.USER_LOGIN:
            event_time = datetime.fromisoformat(event.timestamp.replace('Z', '+00:00'))
            self.login_times.append(event_time.hour)
            self.login_locations[event.location] += 1
            self.devices_used[event.device_id] += 1

        if event.event_type in [EventType.DATA_READ, EventType.DATA_EXPORT]:
            self.accessed_resources[event.resource_id] += 1
            self.typical_data_volume.append(event.records_affected)

    def get_baseline(self) -> dict:
        """정상 행동 기준선 계산"""
        baseline = {
            'login_hours': {
                'mean': statistics.mean(self.login_times) if self.login_times else 12,
                'stdev': statistics.stdev(self.login_times) if len(self.login_times) > 1 else 2
            },
            'common_locations': dict(sorted(
                self.login_locations.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]),
            'avg_data_volume': (
                statistics.mean(self.typical_data_volume)
                if self.typical_data_volume else 0
            ),
            'known_devices': list(self.devices_used.keys())
        }
        return baseline

class UEBAEngine:
    """
    User and Entity Behavior Analytics 엔진
    - 정상 행동 학습
    - 이상 행동 탐지
    - 위험 스코어링
    """

    def __init__(self):
        self.profiles: Dict[str, BehaviorProfile] = {}
        self.risk_thresholds = {
            'low': 30,
            'medium': 60,
            'high': 80,
            'critical': 95
        }
        self.alerts: List[Dict] = []

    def analyze_event(self, event: AuditEvent) -> Dict:
        """이벤트 분석 및 위험 점수 계산"""
        user_id = event.user_id

        # 프로필 조회 또는 생성
        if user_id not in self.profiles:
            self.profiles[user_id] = BehaviorProfile(user_id)

        profile = self.profiles[user_id]
        baseline = profile.get_baseline()

        risk_factors = []
        risk_score = 0

        # 1. 로그인 시간 이상
        if event.event_type == EventType.USER_LOGIN:
            event_time = datetime.fromisoformat(event.timestamp.replace('Z', '+00:00'))
            hour = event_time.hour

            mean = baseline['login_hours']['mean']
            stdev = baseline['login_hours']['stdev']

            if stdev > 0 and abs(hour - mean) > 2 * stdev:
                risk_score += 20
                risk_factors.append(f"Unusual login hour: {hour}:00 (expected around {int(mean)}:00)")

        # 2. 위치 이상
        if event.location not in baseline['common_locations']:
            risk_score += 15
            risk_factors.append(f"New login location: {event.location}")

        # 3. 디바이스 이상
        if event.device_id not in baseline['known_devices']:
            risk_score += 25
            risk_factors.append(f"Unknown device: {event.device_id}")

        # 4. 데이터 접근량 이상
        if event.event_type in [EventType.DATA_READ, EventType.DATA_EXPORT]:
            avg_volume = baseline['avg_data_volume']
            if avg_volume > 0 and event.records_affected > avg_volume * 10:
                risk_score += 30
                risk_factors.append(
                    f"Large data access: {event.records_affected} records "
                    f"(avg: {int(avg_volume)})"
                )

        # 5. 민감 데이터 접근
        if event.sensitivity == "HIGH" or event.sensitivity == "CRITICAL":
            risk_score += 15
            risk_factors.append(f"Access to {event.sensitivity} sensitivity data")

        # 6. 특권 상승
        if event.event_type == EventType.PRIVILEGE_ESCALATION:
            risk_score += 40
            risk_factors.append("Privilege escalation detected")

        # 7. 연속 실패
        if event.event_type == EventType.AUTH_FAILURE:
            recent_failures = self._get_recent_failures(user_id)
            if recent_failures >= 3:
                risk_score += 35
                risk_factors.append(f"Multiple auth failures: {recent_failures}")

        # 위험 레벨 결정
        risk_level = RiskLevel.LOW
        for level, threshold in [
            (RiskLevel.CRITICAL, 95),
            (RiskLevel.HIGH, 80),
            (RiskLevel.MEDIUM, 60),
            (RiskLevel.LOW, 30)
        ]:
            if risk_score >= threshold:
                risk_level = level
                break

        # 알림 생성
        result = {
            'event_id': event.event_id,
            'user_id': user_id,
            'risk_score': min(risk_score, 100),
            'risk_level': risk_level.name,
            'risk_factors': risk_factors,
            'timestamp': event.timestamp
        }

        if risk_score >= self.risk_thresholds['medium']:
            self.alerts.append(result)

        # 프로필 업데이트
        profile.update(event)

        return result

    def _get_recent_failures(self, user_id: str, minutes: int = 15) -> int:
        """최근 인증 실패 횟수"""
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
        count = 0
        for alert in reversed(self.alerts):
            if alert['user_id'] == user_id:
                alert_time = datetime.fromisoformat(alert['timestamp'].replace('Z', '+00:00'))
                if alert_time >= cutoff:
                    count += 1
                else:
                    break
        return count

    def get_user_report(self, user_id: str) -> Dict:
        """사용자별 분석 보고서"""
        if user_id not in self.profiles:
            return {'error': 'User not found'}

        profile = self.profiles[user_id]
        baseline = profile.get_baseline()

        user_alerts = [a for a in self.alerts if a['user_id'] == user_id]

        return {
            'user_id': user_id,
            'baseline': baseline,
            'total_events': sum(len(v) for v in profile.accessed_resources.values()),
            'unique_resources_accessed': len(profile.accessed_resources),
            'alerts_count': len(user_alerts),
            'recent_alerts': user_alerts[-5:] if user_alerts else [],
            'risk_summary': {
                'high_risk_events': len([a for a in user_alerts if a['risk_level'] == 'HIGH']),
                'critical_events': len([a for a in user_alerts if a['risk_level'] == 'CRITICAL'])
            }
        }

class AccountabilityManager:
    """
    책임추적성 통합 관리
    - 감사 로그
    - 행동 분석
    - 포렌식 지원
    """

    def __init__(self):
        self.audit_log = AuditLog()
        self.ueba_engine = UEBAEngine()

    def record_event(self,
                     event_type: EventType,
                     user_id: str,
                     user_name: str,
                     resource_type: str,
                     resource_id: str,
                     operation: str,
                     outcome: str = "SUCCESS",
                     **kwargs) -> Tuple[AuditEvent, Dict]:
        """
        이벤트 기록 및 분석
        """
        event = AuditEvent(
            event_id="",  # 자동 생성
            timestamp="",  # 자동 생성
            event_type=event_type,
            outcome=outcome,
            user_id=user_id,
            user_name=user_name,
            resource_type=resource_type,
            resource_id=resource_id,
            operation=operation,
            details=kwargs.get('details', {}),
            records_affected=kwargs.get('records_affected', 0),
            source_ip=kwargs.get('source_ip', 'unknown'),
            device_id=kwargs.get('device_id', 'unknown'),
            location=kwargs.get('location', 'unknown'),
            sensitivity=kwargs.get('sensitivity', 'NORMAL')
        )

        # 로깅
        logged_event = self.audit_log.log_event(event)

        # 분석
        analysis = self.ueba_engine.analyze_event(logged_event)

        return logged_event, analysis

    def investigate(self,
                    user_id: str = None,
                    start_time: datetime = None,
                    end_time: datetime = None,
                    event_types: List[EventType] = None) -> Dict:
        """
        포렌식 조사 지원
        """
        results = {
            'events': [],
            'user_report': None,
            'timeline': []
        }

        # 이벤트 검색
        if user_id:
            events = self.audit_log.search_by_user(user_id)
            results['user_report'] = self.ueba_engine.get_user_report(user_id)
        else:
            events = self.audit_log.events

        # 필터링
        filtered = []
        for event in events:
            event_time = datetime.fromisoformat(event.timestamp.replace('Z', '+00:00'))

            if start_time and event_time < start_time:
                continue
            if end_time and event_time > end_time:
                continue
            if event_types and event.event_type not in event_types:
                continue

            filtered.append(event)

        results['events'] = [e.to_dict() for e in filtered]

        # 타임라인 생성
        for event in sorted(filtered, key=lambda e: e.timestamp):
            results['timeline'].append({
                'timestamp': event.timestamp,
                'description': f"{event.user_name} performed {event.operation} on {event.resource_id}",
                'outcome': event.outcome
            })

        return results

# 사용 예시
if __name__ == "__main__":
    manager = AccountabilityManager()

    # 1. 로그인 이벤트
    event, analysis = manager.record_event(
        event_type=EventType.USER_LOGIN,
        user_id="john@company.com",
        user_name="John Doe",
        resource_type="SYSTEM",
        resource_id="main-app",
        operation="LOGIN",
        source_ip="192.168.1.100",
        device_id="laptop-001",
        location="Seoul, KR"
    )
    print(f"Login - Risk Score: {analysis['risk_score']}")

    # 2. 데이터 접근 이벤트
    event, analysis = manager.record_event(
        event_type=EventType.DATA_READ,
        user_id="john@company.com",
        user_name="John Doe",
        resource_type="DATABASE_TABLE",
        resource_id="customers_pii",
        operation="SELECT",
        records_affected=50000,
        sensitivity="HIGH",
        source_ip="192.168.1.100"
    )
    print(f"Data Access - Risk Score: {analysis['risk_score']}")
    print(f"Risk Factors: {analysis['risk_factors']}")

    # 3. 권한 상승 이벤트
    event, analysis = manager.record_event(
        event_type=EventType.PRIVILEGE_ESCALATION,
        user_id="john@company.com",
        user_name="John Doe",
        resource_type="ROLE",
        resource_id="admin_role",
        operation="ASSIGN",
        source_ip="192.168.1.100"
    )
    print(f"Privilege Escalation - Risk Score: {analysis['risk_score']}")
    print(f"Risk Level: {analysis['risk_level']}")

    # 4. 무결성 검증
    valid, violations = manager.audit_log.verify_integrity()
    print(f"\nLog Integrity: {'Valid' if valid else 'Compromised'}")

    # 5. 조사 보고서
    report = manager.investigate(user_id="john@company.com")
    print(f"\n=== Investigation Report ===")
    print(f"Total Events: {len(report['events'])}")
    print(f"Timeline entries: {len(report['timeline'])}")
