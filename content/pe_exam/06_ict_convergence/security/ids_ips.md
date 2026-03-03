+++
title = "IDS/IPS (침입 탐지/방지 시스템)"
date = 2025-03-01

[extra]
categories = "pe_exam-ict_convergence"
+++

# IDS/IPS (침입 탐지/방지 시스템)

## 핵심 인사이트 (3줄 요약)
> **IDS(Intrusion Detection System)는 네트워크/시스템 침입을 탐지하고 경보를 발생시키는 수동형 보안 시스템**이다.
> **IPS(Intrusion Prevention System)는 탐지 후 자동으로 공격을 차단하는 능동형 보안 시스템**으로, 인라인 배치로 실시간 방어가 가능하다.
> AI/ML 기반 이상 탐지, OT 환경 보안, 클라우드 네이티브 IPS로 진화하며, SIEM/SOAR와 연동한 자동화 대응이 핵심 트렌드다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: IDS(Intrusion Detection System, 침입 탐지 시스템)는 네트워크나 시스템에서 악의적인 활동이나 정책 위반을 탐지하고 보안 담당자에게 경보를 보내는 보안 시스템이다. IPS(Intrusion Prevention System, 침입 방지 시스템)는 IDS의 탐지 기능에 더해 자동으로 공격을 차단하는 능동적 방어 시스템이다.

> **비유**: "IDS는 건물 내부의 CCTV와 경비실 알림 시스템" — 침입자를 발견하면 경비원에게 알리기만 한다. "IPS는 자동 잠금 장치와 경비원이 합쳐진 것" — 침입자를 발견하면 즉시 문을 잠그고 제지한다.

**등장 배경** (필수: 3가지 이상 기술):

1. **기존 문제점**: 방화벽은 네트워크 경계에서 IP/Port 기반 필터링만 수행하여, 이미 내부로 침투한 공격이나 애플리케이션 계층 공격(SQL 인젝션, XSS 등)을 탐지할 수 없었다.

2. **기술적 필요성**: 알려진 공격 패턴(시그니처)과 비정상적인 행위(이상 탐지)를 실시간으로 분석하여, 방화벽을 우회한 공격이나 내부 위협을 식별할 필요가 있었다.

3. **시장/산업 요구**: 사이버 공격의 정교화와 자동화로 인해 수동 대응의 한계가 드러나, 탐지와 동시에 자동 차단이 가능한 실시간 방어 시스템 요구가 급증했다.

**핵심 목적**: 네트워크와 시스템을 실시간으로 모니터링하여 침입 시도를 탐지(IDS)하고, 자동으로 공격을 차단(IPS)함으로써 보안 사고를 예방하고 피해를 최소화하는 것이다.

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **센서/에이전트** | 트래픽/로그 수집 | NIDS: 미러링 포트, HIDS: 호스트 에이전트 | CCTV 카메라 |
| **탐지 엔진** | 공격 패턴 매칭/이상 분석 | 시그니처 기반 + 이상 행위 기반 | 경비원의 눈 |
| **시그니처 DB** | 알려진 공격 패턴 저장 | CVE 기반 규칙, 지속 업데이트 | 범죄자 명단 |
| **정상 행위 프로파일** | 정상 패턴 학습 데이터 | ML/AI 기반 베이스라인 생성 | 정상 방문객 기록 |
| **경보/대응 모듈** | 알림 발송, 자동 차단 | 이메일, SMS, SIEM 연동 | 비상벨/경비 호출 |
| **관리 콘솔** | 정책 설정, 로그 분석 | 중앙 집중 관리, 리포팅 | 경비실 모니터 |

**구조 다이어그램** (필수: ASCII 아트):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    IDS/IPS 통합 아키텍처                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   인터넷                                                                    │
│      │                                                                      │
│      ▼                                                                      │
│   ┌─────────────┐                                                          │
│   │  Firewall   │                                                          │
│   └──────┬──────┘                                                          │
│          │                                                                  │
│          ▼                                                                  │
│   ┌──────────────────────────────────────────────────────────────────┐     │
│   │                    IPS (인라인 배치)                              │     │
│   │  ┌────────────────────────────────────────────────────────────┐  │     │
│   │  │                    패킷 처리 파이프라인                     │  │     │
│   │  │                                                            │  │     │
│   │  │  패킷 수신 → 디코딩 → 스트림 재조립 → 탐지 엔진 → 액션     │  │     │
│   │  │      │                        │                  │         │  │     │
│   │  │      │           ┌────────────┴────────────┐     │         │  │     │
│   │  │      │           │                         │     │         │  │     │
│   │  │      │           ▼                         ▼     ▼         │  │     │
│   │  │      │    ┌───────────┐            ┌───────────┐          │  │     │
│   │  │      │    │시그니처   │            │이상 탐지  │          │  │     │
│   │  │      │    │매칭 엔진  │            │(ML/AI)    │          │  │     │
│   │  │      │    └─────┬─────┘            └─────┬─────┘          │  │     │
│   │  │      │          │                        │                 │  │     │
│   │  │      │          ▼                        ▼                 │  │     │
│   │  │      │    ┌─────────────────────────────────────┐         │  │     │
│   │  │      │    │         시그니처 DB                  │         │  │     │
│   │  │      │    │  • CVE-2024-XXXX: SQL 인젝션       │         │  │     │
│   │  │      │    │  • CVE-2024-YYYY: 버퍼 오버플로우   │         │  │     │
│   │  │      │    │  • 수십만 개의 공격 패턴            │         │  │     │
│   │  │      │    └─────────────────────────────────────┘         │  │     │
│   │  │      │                                                     │  │     │
│   │  │      └─────────────────────────────────────────────────────┘  │     │
│   │  │                                                               │  │     │
│   │  │           ┌──────────────┬──────────────┬─────────────┐     │  │     │
│   │  │           │              │              │             │     │  │     │
│   │  │           ▼              ▼              ▼             ▼     │  │     │
│   │  │      [허용]         [차단]         [리셋]        [로그]    │  │     │
│   │  │    (Allow)         (Drop)        (Reset)       (Alert)    │  │     │
│   │  └────────────────────────────────────────────────────────────┘  │     │
│   └──────────────────────────────────────────────────────────────────┘     │
│          │                                                                  │
│          ▼                                                                  │
│   ┌──────────────────────────────────────────────────────────────────┐     │
│   │                    내부 네트워크                                   │     │
│   │                                                                   │     │
│   │   ┌────────────────┐         ┌────────────────┐                  │     │
│   │   │    NIDS        │         │     HIDS       │                  │     │
│   │   │  (미러링 포트)  │         │  (호스트 에이전트)│                  │     │
│   │   │                │         │                │                  │     │
│   │   │ ┌────────────┐ │         │ ┌────────────┐ │                  │     │
│   │   │ │  스위치    │ │         │ │   서버     │ │                  │     │
│   │   │ │  SPAN Port │ │         │ │  HIDS      │ │                  │     │
│   │   │ └────────────┘ │         │ │  에이전트  │ │                  │     │
│   │   └────────────────┘         │ └────────────┘ │                  │     │
│   │                              └────────────────┘                  │     │
│   │                            (파일 무결성, 레지스트리 감시)         │     │
│   └──────────────────────────────────────────────────────────────────┘     │
│          │                                                                  │
│          ▼                                                                  │
│   ┌──────────────────────────────────────────────────────────────────┐     │
│   │                    중앙 관리 서버 (SIEM 연동)                      │     │
│   │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐    │     │
│   │  │  이벤트    │ │   상관    │ │  대시보드  │ │  자동대응  │    │     │
│   │  │  수집/정규화│ │   분석    │ │  리포팅   │ │  (SOAR)    │    │     │
│   │  └────────────┘ └────────────┘ └────────────┘ └────────────┘    │     │
│   └──────────────────────────────────────────────────────────────────┘     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):

```
① 패킷 수집 → ② 전처리/재조립 → ③ 탐지 엔진 분석 → ④ 위협 판정 → ⑤ 대응 액션 → ⑥ 로깅/알림
```

- **1단계 (패킷 수집)**: NIDS는 미러링 포트(SPAN)에서 트래픽 복사, HIDS는 호스트의 시스템 로그/파일 이벤트 수집
- **2단계 (전처리/재조립)**: IP 단편화 재조립, TCP 스트림 재구성, 프로토콜 디코딩 수행
- **3단계 (탐지 엔진 분석)**: 시그니처 매칭(알려진 공격) + 이상 탐지(ML/AI 기반) 병렬 수행
- **4단계 (위협 판정)**: 신뢰도 점수 계산, 오탐지(False Positive) 필터링, 심각도 분류
- **5단계 (대응 액션)**: IDS는 경보만 발생, IPS는 패킷 드롭/세션 리셋/차단 규칙 추가 수행
- **6단계 (로깅/알림)**: PCAP 저장, SIEM 전송, 이메일/SMS 알림, 자동 티켓 생성

**핵심 알고리즘/공식** (해당 시 필수):

```
시그니처 기반 탐지 (Snort/Suricata 스타일):
┌─────────────────────────────────────────────────────────────────┐
│  Rule Syntax:                                                    │
│  alert tcp $EXTERNAL_NET any -> $HOME_NET 80 (                  │
│    msg:"SQL Injection Attempt";                                 │
│    content:"' OR '1'='1"; nocase;                               │
│    classtype:web-application-attack;                            │
│    sid:1000001; rev:1;                                          │
│  )                                                               │
│                                                                  │
│  Match Condition:                                                │
│  Alert = (Protocol Match) ∧ (Port Match) ∧ (Content Match)      │
└─────────────────────────────────────────────────────────────────┘

이상 탐지 (Anomaly Detection) 알고리즘:
┌─────────────────────────────────────────────────────────────────┐
│  정상 행위 프로파일링:                                           │
│  Baseline = E[X_t] ± k × σ(X_t)                                │
│  (X_t: 시간 t에서의 측정값, k: 민감도 계수)                      │
│                                                                  │
│  이상 점수:                                                      │
│  Anomaly_Score = Σ w_i × |feature_i - baseline_i| / σ_i        │
│                                                                  │
│  탐지 임계값:                                                    │
│  If Anomaly_Score > Threshold → Alert                           │
└─────────────────────────────────────────────────────────────────┘

오탐지유(False Positive Rate) 관리:
┌─────────────────────────────────────────────────────────────────┐
│  ROC 곡선 기반 임계값 최적화                                     │
│  - TPR (True Positive Rate) = TP / (TP + FN)                   │
│  - FPR (False Positive Rate) = FP / (FP + TN)                  │
│  - 목표: TPR 최대화, FPR 최소화                                  │
└─────────────────────────────────────────────────────────────────┘
```

**코드 예시** (필수: Python 또는 의사코드):

```python
"""
IDS/IPS 탐지 엔진 시뮬레이션
시그니처 기반 + 간단한 이상 탐지 구현
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from enum import Enum
from collections import defaultdict
from datetime import datetime, timedelta
import statistics

class Severity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class ActionType(Enum):
    ALERT = "ALERT"           # IDS: 경보만
    DROP = "DROP"             # IPS: 패킷 폐기
    RESET = "RESET"           # IPS: TCP 리셋
    LOG = "LOG"               # 로그만 기록

@dataclass
class Signature:
    """공격 시그니처 정의"""
    sig_id: int
    name: str
    category: str
    pattern: str              # 정규식 패턴
    severity: Severity
    action: ActionType
    description: str

@dataclass
class Packet:
    """네트워크 패킷 정보"""
    timestamp: datetime
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str
    payload: bytes
    tcp_flags: str = ""

@dataclass
class Alert:
    """탐지된 경보"""
    timestamp: datetime
    signature: Signature
    packet: Packet
    anomaly_score: float = 0.0
    message: str = ""

class AnomalyDetector:
    """이상 행위 탐지 (통계 기반)"""

    def __init__(self, learning_period: int = 1000):
        self.learning_period = learning_period
        self.baseline: Dict[str, List[float]] = defaultdict(list)
        self.is_learning = True
        self.threshold_multiplier = 3.0  # 3-sigma

    def update_baseline(self, feature_name: str, value: float):
        """정상 행위 학습"""
        self.baseline[feature_name].append(value)

        if len(self.baseline[feature_name]) >= self.learning_period:
            self.is_learning = False

    def calculate_anomaly_score(self, feature_name: str, value: float) -> float:
        """이상 점수 계산 (Z-score 기반)"""
        if self.is_learning or feature_name not in self.baseline:
            return 0.0

        data = self.baseline[feature_name]
        if len(data) < 10:
            return 0.0

        mean = statistics.mean(data)
        stdev = statistics.stdev(data) if len(data) > 1 else 1.0

        if stdev == 0:
            return 0.0

        z_score = abs(value - mean) / stdev
        return z_score

    def is_anomaly(self, feature_name: str, value: float) -> bool:
        """이상 여부 판정"""
        score = self.calculate_anomaly_score(feature_name, value)
        return score > self.threshold_multiplier

class IDSEngine:
    """IDS/IPS 탐지 엔진"""

    def __init__(self):
        self.signatures: List[Signature] = []
        self.anomaly_detector = AnomalyDetector()
        self.alerts: List[Alert] = []
        self.stats = {
            "total_packets": 0,
            "alerts_generated": 0,
            "packets_dropped": 0
        }

    def add_signature(self, sig: Signature):
        """시그니처 추가"""
        # 정규식 미리 컴파일
        self.signatures.append(sig)
        print(f"[+] 시그니처 #{sig.sig_id} 로드: {sig.name}")

    def _match_signature(self, packet: Packet) -> Optional[Signature]:
        """시그니처 매칭 검사"""
        payload_str = packet.payload.decode('utf-8', errors='ignore')

        for sig in self.signatures:
            try:
                if re.search(sig.pattern, payload_str, re.IGNORECASE):
                    return sig
            except re.error:
                continue
        return None

    def _detect_port_scan(self, packet: Packet) -> float:
        """포트 스캔 탐지 (간단한 구현)"""
        # 실제로는 시간 윈도우 내 연결 추적 필요
        # 여기서는 데모용 단순화
        return 0.0

    def process_packet(self, packet: Packet) -> Optional[Alert]:
        """패킷 처리 및 탐지"""
        self.stats["total_packets"] += 1

        # 1. 시그니처 기반 탐지
        matched_sig = self._match_signature(packet)

        # 2. 이상 행위 기반 탐지
        # 패킷 크기 이상 탐지
        packet_size = len(packet.payload)
        size_anomaly = self.anomaly_detector.calculate_anomaly_score(
            "packet_size", packet_size
        )

        # 3. 정상 행위 학습 (학습 기간 중)
        self.anomaly_detector.update_baseline("packet_size", packet_size)

        # 4. 경보 생성 조건
        alert = None

        if matched_sig:
            alert = Alert(
                timestamp=packet.timestamp,
                signature=matched_sig,
                packet=packet,
                message=f"시그니처 매칭: {matched_sig.name}"
            )
            self.stats["alerts_generated"] += 1

        elif size_anomaly > 3.0:
            # 이상 탐지 경보 (커스텀 시그니처 생성)
            anomaly_sig = Signature(
                sig_id=99999,
                name="Anomaly Detected",
                category="anomaly",
                pattern="",
                severity=Severity.MEDIUM,
                action=ActionType.ALERT,
                description="비정상적인 패킷 크기 탐지"
            )
            alert = Alert(
                timestamp=packet.timestamp,
                signature=anomaly_sig,
                packet=packet,
                anomaly_score=size_anomaly,
                message=f"이상 점수: {size_anomaly:.2f}"
            )
            self.stats["alerts_generated"] += 1

        if alert:
            self.alerts.append(alert)
            self._execute_action(alert)

        return alert

    def _execute_action(self, alert: Alert):
        """대응 액션 수행"""
        action = alert.signature.action

        if action == ActionType.ALERT:
            print(f"[ALERT] {alert.timestamp} | {alert.signature.name} | "
                  f"{alert.packet.src_ip}:{alert.packet.src_port} → "
                  f"{alert.packet.dst_ip}:{alert.packet.dst_port} | "
                  f"{alert.message}")

        elif action == ActionType.DROP:
            self.stats["packets_dropped"] += 1
            print(f"[DROP] {alert.signature.name} - 패킷 차단됨")

        elif action == ActionType.RESET:
            self.stats["packets_dropped"] += 1
            print(f"[RESET] {alert.signature.name} - TCP 리셋 전송")

    def get_statistics(self) -> dict:
        """통계 반환"""
        return {
            **self.stats,
            "signature_count": len(self.signatures),
            "learning_mode": self.anomaly_detector.is_learning
        }


# 사용 예시
if __name__ == "__main__":
    ids = IDSEngine()

    # 시그니처 로드
    ids.add_signature(Signature(
        sig_id=1001,
        name="SQL Injection",
        category="web-attack",
        pattern=r"(?i)(union.*select|'--|;\s*drop|'\s*or\s*'1'\s*=\s*'1)",
        severity=Severity.HIGH,
        action=ActionType.ALERT,
        description="SQL 인젝션 공격 시도"
    ))

    ids.add_signature(Signature(
        sig_id=1002,
        name="XSS Attack",
        category="web-attack",
        pattern=r"(?i)(<script|javascript:|onerror\s*=|onload\s*=)",
        severity=Severity.MEDIUM,
        action=ActionType.ALERT,
        description="크로스 사이트 스크립팅 시도"
    ))

    ids.add_signature(Signature(
        sig_id=1003,
        name="Directory Traversal",
        category="web-attack",
        pattern=r"(\.\./|\.\.\\)",
        severity=Severity.HIGH,
        action=ActionType.DROP,
        description="디렉토리 순회 공격"
    ))

    # 테스트 패킷
    test_packets = [
        Packet(datetime.now(), "192.168.1.100", "10.0.0.1", 54321, 80,
               "TCP", b"GET /index.html HTTP/1.1\r\nHost: example.com\r\n\r\n"),
        Packet(datetime.now(), "203.0.113.50", "10.0.0.1", 45678, 80,
               "TCP", b"GET /search?q=' OR '1'='1 HTTP/1.1\r\n"),
        Packet(datetime.now(), "203.0.113.50", "10.0.0.1", 45679, 80,
               "TCP", b"GET /page?id=<script>alert(1)</script> HTTP/1.1\r\n"),
        Packet(datetime.now(), "203.0.113.50", "10.0.0.1", 45680, 80,
               "TCP", b"GET /download?file=../../../etc/passwd HTTP/1.1\r\n"),
    ]

    print("\n=== IDS/IPS 패킷 처리 테스트 ===\n")

    for pkt in test_packets:
        alert = ids.process_packet(pkt)

    print(f"\n=== 통계 ===")
    print(ids.get_statistics())
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):

| 장점 | 단점 |
|-----|------|
| **실시간 위협 탐지**: 네트워크 트래픽을 실시간 분석하여 공격 진행 중 탐지 가능 | **오탐지(False Positive)**: 정상 트래픽을 공격으로 오인하여 운영에 방해 가능 |
| **미지 공격 탐지(이상 탐지)**: 시그니처 없는 새로운 공격도 행위 분석으로 탐지 가능 | **미탐지(False Negative)**: 암호화 트래픽, 난독화 공격은 탐지 어려움 |
| **포렌식 증거 확보**: PCAP 로그 저장으로 사후 분석 및 법적 증거 확보 가능 | **성능 오버헤드**: DPI 및 패턴 매칭으로 고속 네트워크에서 병목 가능 |
| **자동화된 대응(IPS)**: 사람의 개입 없이 실시간 공격 차단으로 대응 시간 단축 | **운영 복잡도**: 시그니처 관리, 튜닝, 임계값 설정에 전문 인력 필요 |
| **규정 준수 지원**: PCI-DSS, ISMS 등 보안 규정의 로깅/모니터링 요구사항 충족 | **인라인 장애(IPS)**: IPS 장애 시 전체 네트워크 통신 차단 위험 (Bypass 필요) |

**대안 기술 비교** (필수: 최소 2개 대안):

| 비교 항목 | IDS | IPS | 방화벽 (NGFW) |
|---------|-----|-----|--------------|
| **핵심 특성** | 수동 탐지, 경보 발생 | ★ 능동 탐지+차단 | 경계 필터링 + 일부 탐지 |
| **배치 방식** | 미러링(Out-of-Band) | ★ 인라인(In-Line) | 인라인 |
| **대응 방식** | 알림만 | 자동 차단 | 정책 기반 필터링 |
| **성능 영향** | 없음 (복사본 분석) | 높음 (모든 트래픽 경유) | 중간 |
| **탐지 깊이** | ★ 가장 깊음 | 깊음 | 기본~중간 |
| **적합 환경** | 모니터링, 포렌식 | 실시간 방어 | 경계 보안 |

| 비교 항목 | NIDS (네트워크) | HIDS (호스트) | 하이브리드 |
|---------|----------------|--------------|-----------|
| **모니터링 대상** | 네트워크 세그먼트 전체 | 개별 서버/시스템 | ★ 네트워크+호스트 |
| **탐지 범위** | 네트워크 공격, 트래픽 이상 | 파일 변조, 권한 상승 | ★ 종합적 |
| **암호화 트래픽** | 탐지 어려움 | ★ 복호화 후 탐지 가능 | 부분 가능 |
| **성능 영향** | 네트워크에 영향 없음 | 호스트 리소스 사용 | 혼합 |
| **확장성** | ★ 우수 (장비 추가) | 관리 복잡 | 중간 |
| **비용** | 중간 | 에이전트별 라이선스 | ★ 높음 |

> **선택 기준**:
> - **규정 준수 중심**: IDS (모니터링, 로깅)
> - **실시간 방어 중심**: IPS (자동 차단)
> - **종합 보안**: NGFW + IPS 통합 솔루션
> - **암호화 트래픽 많은 환경**: HIDS + NIDS 하이브리드

**기술 진화 계보**:

```
1990년대         2000년대         2010년대         2020년대~
   │               │                │                │
   ▼               ▼                ▼                ▼
┌─────────┐   ┌─────────┐    ┌─────────┐    ┌─────────────┐
│  IDS    │ → │  IPS    │ → │  NGIPS  │ → │  AI 기반    │
│(시그니처)│   │(실시간  │    │(앱 식별,│    │  XDR/EDR    │
│         │   │ 차단)   │    │ 위협   │    │  통합 보안  │
│         │   │         │    │ 인텔리)│    │             │
└─────────┘   └─────────┘    └─────────┘    └─────────────┘
                                  ↓
                            ┌─────────────┐
                            │  클라우드   │
                            │  네이티브   │
                            │  CWPP/CNAPP │
                            └─────────────┘
```

---

### Ⅳ. 실무 적용 방안 (필수: 전문가 판단력 증명)

**전문가적 판단** (필수: 3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **금융권 웹 서비스** | NGIPS를 DMZ 전면에 배치, SQL 인젝션/XSS/WAF 시그니처 활성화, 24시간 SOC 연동 | 웹 공격 탐지율 99%, 서비스 중단 시간 99.9% 감소 |
| **제조업 OT 네트워크** | 산업용 프로토콜(Modbus, DNP3) 지원 OT-IPS 도입, 화이트리스트 정책, IT/OT 경계 배치 | 생산 설비 보안 사고 95% 감소, 안전 정지 방지 |
| **클라우드 컨테이너 환경** | 쿠버네티스용 CNI 기반 IPS, 컨테이너 이상 행위 탐지, 서비스 메시와 연동 | 컨테이너 탈출 공격 100% 차단, 측면 이동 방지 |

**실제 도입 사례** (필수: 구체적 기업/서비스):

- **사례 1: 카카오뱅크** - NGIPS와 AI 기반 이상 탐지 시스템을 구축하여, 실시간으로 계좌 이체 패턴을 분석하고 이상 거래를 탐지/차단. 피싱 사이트 유입 시도 차단률 98% 달성.

- **사례 2: POSCO** - 스마트팩토리 환경에서 OT 네트워크 전용 IPS를 도입. 산업용 제어 시스템(ICS) 프로토콜 분석 기능으로 랜섬웨어 전파 경로 차단. 생산 중단 사고 예방으로 연간 50억 원 손실 방지.

- **사례 3: AWS GuardDuty** - 클라우드 네이티브 IDS/IPS 서비스로, VPC Flow Logs, DNS 로그, CloudTrail 이벤트를 AI로 분석하여 계정 탈취, 암호화폐 채굴, C&C 통신 등을 자동 탐지.

**도입 시 고려사항** (필수: 4가지 관점):

1. **기술적**:
   - 탐지 성능: 시그니처 수, 탐지 지연 시간(Latency)
   - 처리량: 라인 속도(Line Rate) 지원 여부
   - 프로토콜 지원: 산업용/독자 프로토콜 분석 능력
   - 암호화 처리: SSL/TLS 복호화 성능

2. **운영적**:
   - 오탐지 관리: 튜닝 프로세스, 화이트리스트 관리
   - 24x7 모니터링: SOC 운영 인력 확보
   - SIEM/SOAR 연동: 자동화 대응 파이프라인
   - 장애 대응: Bypass NIC, HA 구성

3. **보안적**:
   - 시그니처 업데이트: 제조사 업데이트 주기, CVE 대응 속도
   - 제로데이 대응: 이상 탐지 기능의 신뢰도
   - 컴플라이언스: ISMS-P, PCI-DSS 요구사항 충족
   - 로그 보관: PCAP 저장 정책, 개인정보 이슈

4. **경제적**:
   - 하드웨어 비용: 센서 장비, 스토리지
   - 소프트웨어 비용: 시그니처 구독, 라이선스
   - 운영 비용: SOC 인력, 교육
   - TCO: 3~5년 총 소유 비용 분석

**주의사항 / 흔한 실수** (필수: 최소 3개):

- **오탐지 방치**: 초기 튜닝 없이 운영하면 수많은 오탐지로 인해 실제 경보를 무시하게 됨. 반드시 단계적 튜닝과 화이트리스트 구축 필요
- **IPS 인라인 배치 시 Bypass 미구성**: IPS 장애 시 전체 네트워크 마비. 하드웨어 Bypass NIC 또는 Fail-Open 모드 필수 설정
- **암호화 트래픽 무시**: HTTPS가 90% 이상인 현대 네트워크에서 암호화 트래픽을 분석하지 않으면 탐지율 급락. SSL 복호화 또는 HIDS 병행 필요

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):

```
📌 IDS/IPS 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────────────────┐
│                        IDS/IPS 연관 개념 맵                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│      ┌──────────┐                        ┌──────────┐                      │
│      │  SIEM    │←────────────────────→│ IDS/IPS  │←────────────────────→│ Firewall │
│      │(로그통합) │                        │          │                        │(방화벽)  │
│      └──────────┘                        └────┬─────┘                        └──────────┘
│           ↑                                   │                                   ↑
│           │                                   │                                   │
│           ↓                                   ↓                                   │
│      ┌──────────┐                        ┌──────────┐                        │
│      │  SOAR    │←────────────────────→│  EDR     │                        │
│      │(자동대응) │                        │(엔드포인트)│                        │
│      └──────────┘                        └──────────┘                        │
│                                                ↑                              │
│                                                │                              │
│                                          ┌──────────┐                        │
│                                          │   XDR    │←───────────────────────┘
│                                          │(확장탐지) │
│                                          └──────────┘
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| **방화벽 (Firewall)** | 선행/연동 기술 | IDS/IPS와 함께 다층 방어 구성 | `[firewall](./firewall.md)` |
| **SIEM** | 연동 기술 | IDS/IPS 이벤트 수집 및 상관 분석 | `[siem](./siem.md)` |
| **EDR** | 호스트 기반 대안 | 엔드포인트 수준의 탐지/대응 | `[edr](./edr.md)` |
| **XDR** | 확장 개념 | 네트워크+엔드포인트+클라우드 통합 탐지 | `[xdr](./xdr.md)` |
| **SOAR** | 자동화 기술 | IDS/IPS 경보 기반 자동 대응 | `[soar](./soar.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| **보안** | 실시간 공격 탐지 및 자동 차단 | 알려진 공격 탐지율 99% 이상 |
| **대응 시간** | 자동화된 차단으로 MTTD/MTTR 단축 | 평균 대응 시간 5분 이내 |
| **가시성** | 네트워크 트래픽 전체 모니터링 | 이상 징후 탐지율 95% 이상 |
| **비용** | 보안 사고 예방, 수동 대응 비용 절감 | 연간 보안 운영 비용 30% 절감 |

**미래 전망** (필수: 3가지 관점):

1. **기술 발전 방향**: AI/ML 기반 행위 분석으로 오탐지 최소화, 제로데이 공격 탐지율 향상. XDR(Extended Detection and Response)로 네트워크-엔드포인트-클라우드 통합 탐지.

2. **시장 트렌드**: 클라우드 네이티브 IDS/IPS(CWPP, CNAPP) 수요 증가. SASE 아키텍처 내 클라우드 IPS(FWaaS)로 통합. OT/IoT 환경 특화 솔루션 성장.

3. **후속 기술**: XDR, NDR(Network Detection and Response), MDR(Managed Detection and Response) 등 "탐지+대응" 통합 서비스로 진화. 자율 대응(Automated Response) 수준 향상.

> **결론**: IDS/IPS는 네트워크 보안의 핵심 감시 및 방어 체계로서, 방화벽을 보완하고 심층 방어(Defense in Depth)를 완성한다. AI 기반 탐지와 XDR 통합으로 진화하며, 클라우드·OT 환경에서도 필수적인 보안 컨트롤로 자리 잡을 것이다.

> **참고 표준**: NIST SP 800-94(Guide to Intrusion Detection), ISO/IEC 27001 Annex A.12, KISA ISMS-P, MITRE ATT&CK Framework

---

## 어린이를 위한 종합 설명 (필수)

**IDS/IPS를 쉽게 이해해보자!**

IDS와 IPS는 마치 **건물 안의 보안 시스템(CCTV + 자동 경비)** 같아요.

**개념 설명**:
큰 건물에는 출입구에 경비원이 있어요(방화벽). 하지만 건물 안에서 나쁜 일이 일어날 수도 있어요. 그래서 건물 안 곳곳에 CCTV를 설치해요. 이게 IDS예요! IDS는 "이상한 일이 있어요!"라고 경비실에 알려줘요. IPS는 여기에 더해서, 나쁜 사람을 발견하면 자동으로 문을 잠그거나 경비원을 부르는 똑똑한 시스템이에요.

**동작 원리 설명**:
IDS는 두 가지 방법으로 나쁜 사람을 찾아요. 첫째, "범죄자 명단"을 가지고 있어서, 명단에 있는 사람이 들어오면 바로 알아채요(시그니처 탐지). 둘째, 평소와 다른 이상한 행동을 하는 사람을 찾아요(이상 탐지). 예를 들어, 밤늦게 이상한 곳을 서성거리거나, 평소 보지 못하던 사람이 들어오면 의심하는 거예요. IPS는 이렇게 의심스러운 사람을 발견하면 바로 문을 잠가서 들어오지 못하게 해요.

**장점/효과 설명**:
IDS와 IPS 덕분에 건물(컴퓨터 네트워크)이 훨씬 안전해져요. 경비원이 보지 못하는 곳에서 일어나는 일도 감시할 수 있고, 나쁜 사람이 건물 안에서 나쁜 짓을 하려고 할 때 바로 막을 수 있어요. 특히 IPS는 경비원이 쉴 때도 24시간 일하면서 건물을 지켜줘요!

---
