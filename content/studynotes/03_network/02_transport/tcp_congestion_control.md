+++
title = "TCP 혼잡 제어 (TCP Congestion Control)"
date = 2024-05-18
description = "TCP 혼잡 제어 메커니즘의 핵심 알고리즘(Slow Start, Congestion Avoidance, Fast Retransmit/Recovery)과 Tahoe/Reno/NewReno/CUBIC/BBR 모델의 심층 분석"
weight = 25
[taxonomies]
categories = ["studynotes-03_network"]
tags = ["TCP", "CongestionControl", "SlowStart", "CUBIC", "BBR", "NetworkProtocol"]
+++

# TCP 혼잡 제어 (TCP Congestion Control)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TCP 혼잡 제어는 네트워크 내부의 라우터나 링크가 과부하 상태에 빠지는 것을 방지하고, 공정한 대역폭 분배를 보장하기 위해 송신측의 전송 속도(Congestion Window)를 동적으로 조절하는 분산 알고리즘입니다.
> 2. **가치**: 1986년 ARPANET 붕괴 사건(Throughput이 40kbps로 급락)을 해결하기 위해 도입되어, 오늘날 인터넷의 안정적 운영을 담보하며 네트워크 용량 대비 90% 이상의 활용 효율을 달성합니다.
> 3. **융합**: 최신 혼잡 제어 알고리즘인 CUBIC(Linux 기본), BBR(Google 개발)은 고지연·고대역폭 환경(BDP, Bandwidth-Delay Product)에 최적화되어 있으며, QUIC 프로토콜의 기반 기술로도 적용됩니다.

---

## Ⅰ. 개요 (Context & Background)

TCP 혼잡 제어(Congestion Control)는 1988년 Van Jacobson에 의해 제안된 이후, 인터넷의 안정성을 지키는 가장 중요한 메커니즘입니다. 흐름 제어(Flow Control)가 **수신측의 버퍼 오버플로우를 방지**하는 데 집중한다면, 혼잡 제어는 **네트워크 내부의 혼잡을 완화**하는 데 집중합니다.

**💡 비유**: TCP 혼잡 제어는 **'고속도로 교통 제어 시스템'**과 같습니다.
- **혼잡 윈도우(CWND)**: 차량이 도로에 진입할 때 유지해야 하는 앞차와의 안전 거리
- **Slow Start**: 도로에 처음 진입할 때는 조심스럽게 출발하다가, 막힘 없으면 속도를 점점 높임
- **혼잡 회피**: 제한 속도에 가까워지면 속도를 서서히 조절
- **패킷 손실**: 앞차가 급정거하면 나도 멈추고 다시 출발
- **AIMD(Additive Increase/Multiplicative Decrease)**: 정상 시 속도 1씩 증가, 혼잡 시 절반으로 감소

**등장 배경 및 발전 과정**:
1. **ARPANET 붕괴 사건 (1986)**: 초기 인터넷에서는 혼잡 제어가 없어, 네트워크가 혼잡해지면 모든 호스트가 패킷 손실을 재전송하려고 시도했습니다. 이는 네트워크를 더욱 혼잡하게 만드는 '혼잡 붕괴(Congestion Collapse)'를 초래하여, 처리량이 40kbps까지 급락했습니다.
2. **Jacobson의 혁신 (1988)**: Van Jacobson은 혼잡을 감지하면 즉시 전송 속도를 줄이고, 정상 상태에서는 점진적으로 속도를 높이는 AIMD 알고리즘을 제안했습니다.
3. **지속적 진화**: TCP Tahoe → Reno → NewReno → SACK → CUBIC → BBR로 이어지는 알고리즘 개선을 통해, 현대의 고속 네트워크에서도 안정적인 성능을 유지하고 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: TCP 혼잡 제어 상태 머신

| 상태/알고리즘 | 동작 메커니즘 | CWND 변화 | 진입 조건 | 종료 조건 |
|--------------|--------------|----------|----------|----------|
| **Slow Start** | 지수적 증가 | CWND ← CWND + MSS (매 ACK) | 연결 시작, 타임아웃 후 | CWND ≥ ssthresh |
| **Congestion Avoidance** | 선형 증가 (AIMD) | CWND ← CWND + MSS²/CWND (매 ACK) | CWND ≥ ssthresh | 3 Dup-ACK 또는 타임아웃 |
| **Fast Retransmit** | 즉시 재전송 | - | 3 Dup-ACK 수신 | 재전송 완료 |
| **Fast Recovery** | 부분 복구 | ssthresh ← CWND/2, CWND ← ssthresh + 3MSS | Fast Retransmit 후 | 새로운 ACK 또는 타임아웃 |

### 정교한 구조 다이어그램: TCP 혼잡 제어 상태 전이

```ascii
================================================================================
[ TCP Congestion Control State Machine - Reno/NewReno ]
================================================================================

                          +------------------+
                          |      START       |
                          |  CWND = 1 MSS    |
                          |  ssthresh = 64KB |
                          +--------|---------+
                                   |
                                   v
                    +------------------------------+
                    |       SLOW START             |<------------------+
                    |  CWND = CWND + MSS/ACK       |                   |
                    |  (지수적 증가: 1→2→4→8...)    |                   |
                    +------------------------------+                   |
                                   |                                   |
                         CWND >= ssthresh                           |
                                   |                                   |
                                   v                                   |
                    +------------------------------+                   |
                    |    CONGESTION AVOIDANCE      |                   |
                    |  CWND = CWND + MSS²/CWND     |                   |
                    |  (선형 증가: 1 MSS/RTT)       |                   |
                    +------------------------------+                   |
                                   |                                   |
               +-------------------+-------------------+               |
               |                                       |               |
        3 Dup-ACK                                 Timeout             |
               |                                       |               |
               v                                       v               |
    +---------------------+                   +------------------+    |
    |  FAST RETRANSMIT    |                   |    TIMEOUT       |    |
    |  (손실 세그먼트      |                   |  ssthresh=CWND/2 |    |
    |   즉시 재전송)       |                   |  CWND = 1 MSS    |----+
    +----------|----------+                   +------------------+
               |
               v
    +---------------------+
    |   FAST RECOVERY     |
    |  ssthresh = CWND/2  |
    |  CWND = ssthresh    |
    |      + 3 MSS        |
    +----------|----------+
               |
        +------+------+
        |             |
   New ACK       Timeout
        |             |
        v             v
   Congestion     (Reset to
   Avoidance      Slow Start)

================================================================================
[ AIMD (Additive Increase / Multiplicative Decrease) ]
================================================================================

CWND
  ↑
  |                                    /----  Congestion Avoidance
  |                                  /
  |                                /    /--  Fast Recovery
  |                              /    /
  |                            /    /  /--  Congestion Avoidance
  |              Slow Start  /    /  /
  |            /-----------/    /  /
  |          /               /  / /
  |        /               /  / /
  |      /               /  / /
  |    /               /  / /
  |  /               /  / /
  |/               /  / /
  +--------------------------------------------→ 시간 (RTT)
                혼잡 발생 (패킷 손실)

특징:
- Additive Increase: 정상 시 1 MSS/RTT씩 증가
- Multiplicative Decrease: 혼잡 시 CWND를 절반으로 감소
- 공정성(Fairness): 여러 흐름이 수렴하여 대역폭을 공평하게 분배
================================================================================
```

### 심층 동작 원리: 핵심 알고리즘 상세 분석

#### 1. Slow Start (느린 시작)

**목적**: 네트워크의 가용 대역폭을 모를 때, 보수적으로 시작하여 빠르게 탐색

**알고리즘**:
```
초기화:
  CWND = 1 MSS (또는 IW, Initial Window)
  ssthresh = 임계값 (일반적으로 65535바이트 또는 큰 값)

매 ACK 수신 시:
  CWND = CWND + MSS

특성:
- 1 RTT 후: CWND = 2 MSS
- 2 RTT 후: CWND = 4 MSS
- 3 RTT 후: CWND = 8 MSS
- 지수적(Exponential) 성장: CWND = CWND × 2 (1 RTT마다)
```

**수식 표현**:
```
CWND(n+1) = CWND(n) + MSS × (수신된 ACK 수)

각 RTT에서:
CWND(t+1) = 2 × CWND(t)
```

#### 2. Congestion Avoidance (혼잡 회피)

**목적**: 네트워크 용량에 근접했을 때, 조심스럽게 증가하여 혼잡 유발 방지

**알고리즘 (AIMD)**:
```
매 ACK 수신 시:
  CWND = CWND + MSS² / CWND

특성:
- 1 RTT 동안 CWND/MSS 개의 ACK 수신
- 1 RTT 후: CWND = CWND + MSS
- 선형(Linear) 성장: 1 MSS/RTT
```

**수식 유도**:
```
1 RTT 동안 수신되는 ACK 수 = CWND / MSS
각 ACK당 증가분 = MSS² / CWND

1 RTT 후 총 증가분:
= (CWND / MSS) × (MSS² / CWND) = MSS
```

#### 3. Fast Retransmit (빠른 재전송)

**목적**: 타임아웃을 기다리지 않고 3개의 중복 ACK로 패킷 손실 감지

**알고리즘**:
```
중복 ACK(Duplicate ACK) 수신 시:
  dupACKcount++

  if dupACKcount == 3:
    ssthresh = CWND / 2
    손실 세그먼트 재전송
    Fast Recovery 진입
```

**3 Dup-ACK의 의미**:
- 수신측이 특정 시퀀스 번호 이후의 패킷을 3번 연속 요청
- 네트워크 혼잡보다는 단일 패킷 손실 가능성이 높음
- 타임아웃(1~2초) 대비 빠른 복구 (수십~수백 ms)

#### 4. Fast Recovery (빠른 회복)

**TCP Reno 방식**:
```
Fast Retransmit 후:
  ssthresh = CWND / 2
  CWND = ssthresh + 3 MSS
  (이미 3개의 패킷이 네트워크에 남아있음을 가정)

매 추가 Dup-ACK 수신 시:
  CWND = CWND + MSS
  (네트워크에 패킷이 빠져나감)

새로운 ACK 수신 시:
  CWND = ssthresh
  Congestion Avoidance로 복귀
```

**TCP NewReno 개선**:
- 단일 윈도우 내 여러 패킷 손실 시, Fast Recovery 상태 유지
- 부분 ACK(Partial ACK) 수신 시 추가 손실 패킷 재전송

### TCP 변종 비교

| 변종 | 개발 연도 | 핵심 특징 | 혼잡 감지 시 동작 | 현대적 적용 |
|------|----------|----------|------------------|------------|
| **Tahoe** | 1988 | 최초 구현 | CWND = 1, ssthresh = CWND/2 | 학습/연구용 |
| **Reno** | 1990 | Fast Recovery 도입 | CWND = ssthresh + 3MSS | 레거시 시스템 |
| **NewReno** | 1996 | 다중 손실 복구 | Partial ACK 처리 | 일부 서버 |
| **SACK** | 1996 | 선택적 확인응답 | 손실 블록 정보 전달 | 광범위 사용 |
| **CUBIC** | 2006 | 3차 함수 기반 | CWND = cubic 함수 | Linux 기본 |
| **BBR** | 2016 | 병목 대역폭 측정 | BtlBw + RTprop 기반 | Google, YouTube |

### 핵심 코드: TCP 혼잡 제어 시뮬레이터 (Python)

```python
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from dataclasses import dataclass
from typing import Tuple, List

class TCPState(Enum):
    SLOW_START = "Slow Start"
    CONGESTION_AVOIDANCE = "Congestion Avoidance"
    FAST_RECOVERY = "Fast Recovery"

class CongestionEvent(Enum):
    ACK_RECEIVED = "ACK Received"
    DUP_ACK = "Duplicate ACK"
    THREE_DUP_ACK = "3 Duplicate ACK"
    TIMEOUT = "Timeout"
    NEW_ACK = "New ACK"

@dataclass
class TCPCongestionControl:
    """
    TCP 혼잡 제어 시뮬레이션 클래스

    TCP Reno/NewReno 알고리즘 구현
    """
    mss: int = 1460  # Maximum Segment Size (bytes)
    initial_cwnd: int = 1  # Initial CWND in MSS
    ssthresh: int = 64  # Slow Start Threshold in MSS
    max_cwnd: int = 65535  # Maximum CWND in MSS

    def __post_init__(self):
        self.cwnd = self.initial_cwnd
        self.state = TCPState.SLOW_START
        self.dup_ack_count = 0
        self.history = []

    def process_event(self, event: CongestionEvent) -> Tuple[int, TCPState]:
        """
        이벤트 처리 및 CWND 업데이트

        Returns:
            (새로운 CWND, 새로운 상태)
        """
        old_cwnd = self.cwnd
        old_state = self.state

        if event == CongestionEvent.ACK_RECEIVED:
            self._handle_ack()

        elif event == CongestionEvent.DUP_ACK:
            self._handle_dup_ack()

        elif event == CongestionEvent.THREE_DUP_ACK:
            self._handle_three_dup_ack()

        elif event == CongestionEvent.TIMEOUT:
            self._handle_timeout()

        elif event == CongestionEvent.NEW_ACK:
            self._handle_new_ack()

        # 기록 저장
        self.history.append({
            'event': event.value,
            'old_cwnd': old_cwnd,
            'new_cwnd': self.cwnd,
            'old_state': old_state.value,
            'new_state': self.state.value,
            'ssthresh': self.ssthresh
        })

        return self.cwnd, self.state

    def _handle_ack(self):
        """일반 ACK 처리"""
        self.dup_ack_count = 0

        if self.state == TCPState.SLOW_START:
            # 지수적 증가
            self.cwnd = min(self.cwnd + 1, self.max_cwnd)
            if self.cwnd >= self.ssthresh:
                self.state = TCPState.CONGESTION_AVOIDANCE

        elif self.state == TCPState.CONGESTION_AVOIDANCE:
            # 선형 증가 (AIMD)
            # CWND = CWND + MSS²/CWND (정수 연산 근사)
            self.cwnd = min(self.cwnd + 1 / self.cwnd, self.max_cwnd)

    def _handle_dup_ack(self):
        """중복 ACK 처리"""
        self.dup_ack_count += 1

        if self.state == TCPState.FAST_RECOVERY:
            # Fast Recovery 중 추가 Dup-ACK
            self.cwnd = min(self.cwnd + 1, self.max_cwnd)

    def _handle_three_dup_ack(self):
        """3개 중복 ACK (Fast Retransmit)"""
        self.ssthresh = max(self.cwnd // 2, 2)
        self.cwnd = self.ssthresh + 3  # Reno
        self.state = TCPState.FAST_RECOVERY
        self.dup_ack_count = 0

    def _handle_timeout(self):
        """타임아웃 이벤트"""
        self.ssthresh = max(self.cwnd // 2, 2)
        self.cwnd = 1
        self.state = TCPState.SLOW_START
        self.dup_ack_count = 0

    def _handle_new_ack(self):
        """Fast Recovery 후 새로운 ACK"""
        if self.state == TCPState.FAST_RECOVERY:
            self.cwnd = self.ssthresh
            self.state = TCPState.CONGESTION_AVOIDANCE
        self.dup_ack_count = 0


class TCPCUBIC:
    """
    TCP CUBIC 혼잡 제어 알고리즘

    리눅스 커널 2.6.19부터 기본 알고리즘
    3차 함수를 사용하여 고대역폭-고지연 네트워크에서 빠른 복구
    """

    def __init__(self, mss: int = 1460, beta: float = 0.7, c: float = 0.4):
        """
        Args:
            mss: Maximum Segment Size
            beta: Multiplicative decrease factor (0.7 = 30% 감소)
            c: CUBIC 상수 (시간 단위)
        """
        self.mss = mss
        self.beta = beta
        self.c = c
        self.cwnd = 1.0
        self.w_max = 0  # 마지막 혼잡 시 CWND
        self.t_epoch = 0  # 마지막 혼잡 발생 시점
        self.history = []

    def update(self, current_time: float) -> float:
        """
        CUBIC 윈도우 계산

        수식: W(t) = C(t - K)³ + W_max

        여기서 K = (W_max × β / C)^(1/3)
        """
        t = current_time - self.t_epoch

        # K 계산
        if self.w_max > 0:
            K = (self.w_max * self.beta / self.c) ** (1/3)
        else:
            K = 0

        # CUBIC 함수
        delta = self.c * (t - K) ** 3
        w_cubic = self.w_max * self.beta + delta

        # TCP 호환성 모드 (TCP-friendly region)
        w_tcp = self.w_max * self.beta + 3 * self.beta / (2 - self.beta) * t / self.cwnd

        self.cwnd = max(w_cubic, w_tcp, 1.0)

        return self.cwnd

    def on_packet_loss(self, current_time: float):
        """패킷 손실 감지 시"""
        self.w_max = self.cwnd
        self.cwnd = self.cwnd * self.beta
        self.t_epoch = current_time


class TCPBBR:
    """
    TCP BBR (Bottleneck Bandwidth and Round-trip propagation time)

    구글에서 개발한 혼잡 제어 알고리즘
    패킷 손실이 아닌 병목 대역폭과 RTT를 직접 측정
    """

    def __init__(self):
        self.BtlBw = 0  # 병목 대역폭 (bytes/sec)
        self.RTprop = float('inf')  # 왕복 전파 지연
        self.cwnd = 1.0
        self.pacing_gain = 1.0
        self.cwnd_gain = 2.0
        self.state = 'Startup'
        self.history = []

    def update_model(self, delivered_rate: float, rtt: float):
        """
        BBR 모델 업데이트

        Args:
            delivered_rate: 측정된 전송률
            rtt: 측정된 RTT
        """
        # 병목 대역폭 업데이트 (최대값 유지)
        self.BtlBw = max(self.BtlBw, delivered_rate)

        # RTT 업데이트 (최소값 유지)
        self.RTprop = min(self.RTprop, rtt)

    def set_cwnd(self):
        """
        BBR CWND 계산

        CWND = BtlBw × RTprop × cwnd_gain
        """
        if self.BtlBw > 0 and self.RTprop < float('inf'):
            # BDP (Bandwidth-Delay Product)
            bdp = self.BtlBw * self.RTprop
            self.cwnd = bdp * self.cwnd_gain
        else:
            self.cwnd = 1.0

    def on_rtt_measurement(self, rtt: float, delivery_rate: float):
        """RTT 측정 시"""
        self.update_model(delivery_rate, rtt)
        self.set_cwnd()

        self.history.append({
            'rtt': rtt,
            'delivery_rate': delivery_rate,
            'BtlBw': self.BtlBw,
            'RTprop': self.RTprop,
            'cwnd': self.cwnd
        })


# ================== 시뮬레이션 실행 ==================
def simulate_tcp_reno(n_rounds: int = 50) -> Tuple[List[int], List[int]]:
    """
    TCP Reno 혼잡 제어 시뮬레이션

    Returns:
        (CWND 이력, ssthresh 이력)
    """
    tcp = TCPCongestionControl(mss=1460, initial_cwnd=1, ssthresh=16)
    cwnd_history = [tcp.cwnd]

    # 시뮬레이션 이벤트 생성
    np.random.seed(42)

    for round_num in range(n_rounds):
        # 랜덤 이벤트 생성 (현실적인 패턴)
        if round_num == 15:
            # 15라운드에서 3 Dup-ACK
            tcp.process_event(CongestionEvent.THREE_DUP_ACK)
        elif round_num == 30:
            # 30라운드에서 타임아웃
            tcp.process_event(CongestionEvent.TIMEOUT)
        elif 15 < round_num < 20 or 30 < round_num < 35:
            # Fast Recovery 중
            if tcp.state == TCPState.FAST_RECOVERY:
                tcp.process_event(CongestionEvent.NEW_ACK)
            else:
                tcp.process_event(CongestionEvent.ACK_RECEIVED)
        else:
            tcp.process_event(CongestionEvent.ACK_RECEIVED)

        cwnd_history.append(int(tcp.cwnd))

    return cwnd_history, [h['ssthresh'] for h in tcp.history]


if __name__ == "__main__":
    print("=" * 70)
    print("TCP Congestion Control Simulation Report")
    print("=" * 70)

    # TCP Reno 시뮬레이션
    cwnd_history, _ = simulate_tcp_reno(50)

    print("\n[TCP Reno Congestion Window Evolution]")
    print(f"Initial CWND: {cwnd_history[0]} MSS")
    print(f"Peak CWND: {max(cwnd_history)} MSS")
    print(f"Final CWND: {cwnd_history[-1]} MSS")

    # CUBIC 시뮬레이션
    print("\n[TCP CUBIC Simulation]")
    cubic = TCPCUBIC()
    cubic_history = []

    for t in range(100):
        w = cubic.update(t)
        cubic_history.append(w)
        if t == 50:  # 중간에 패킷 손실 시뮬레이션
            cubic.on_packet_loss(t)

    print(f"Initial CWND: {cubic_history[0]:.2f}")
    print(f"Pre-loss CWND: {cubic_history[50]:.2f}")
    print(f"Post-loss CWND: {cubic_history[51]:.2f}")
    print(f"Final CWND: {cubic_history[-1]:.2f}")

    # BBR 시뮬레이션
    print("\n[TCP BBR Simulation]")
    bbr = TCPBBR()

    # 샘플 RTT와 전송률 데이터
    rtts = [20, 22, 19, 21, 18, 23, 20, 19, 22, 21]  # ms
    rates = [1e6, 1.2e6, 1.5e6, 1.8e6, 2e6, 1.9e6, 2.1e6, 2e6, 2.2e6, 2e6]  # bytes/sec

    for rtt, rate in zip(rtts, rates):
        bbr.on_rtt_measurement(rtt / 1000, rate)  # 초 단위 변환

    print(f"Estimated Bottleneck Bandwidth: {bbr.BtlBw / 1e6:.2f} MB/s")
    print(f"Estimated Minimum RTT: {bbr.RTprop * 1000:.2f} ms")
    print(f"Final CWND: {bbr.cwnd:.0f} bytes")
