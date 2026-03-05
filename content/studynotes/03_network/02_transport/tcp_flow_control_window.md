+++
title = "TCP 흐름 제어 및 슬라이딩 윈도우 (TCP Flow Control & Sliding Window)"
date = 2024-05-18
description = "수신자 버퍼 오버플로우 방지를 위한 TCP 흐름 제어 - 슬라이딩 윈도우 프로토콜, Zero Window, Silly Window Syndrome의 심층 분석"
weight = 60
[taxonomies]
categories = ["studynotes-network"]
tags = ["TCP", "Flow Control", "Sliding Window", "Zero Window", "Silly Window Syndrome", "Nagle"]
+++

# TCP 흐름 제어 및 슬라이딩 윈도우 (TCP Flow Control & Sliding Window)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TCP 흐름 제어는 수신자의 버퍼 상태(rwnd)를 송신자에게 통지하여 수신자가 처리할 수 있는 양만큼만 데이터를 전송함으로써 버퍼 오버플로우와 데이터 손실을 방지하는 종단 간 메커니즘입니다.
> 2. **가치**: 슬라이딩 윈도우 프로토콜은 윈도우 크기만큼 ACK를 기다리지 않고 연속 전송 가능하게 하여 네트워크 대역폭 활용률을 10~100배 향상시키며, 전송 효율의 핵심입니다.
> 3. **융합**: Nagle 알고리즘, Delayed ACK, Window Scaling 등과 결합하여 저대역폭 환경과 고속 네트워크 모두에서 최적화되며, 데이터센터 내부 통신(TCP Offload)과 IoT 센서 네트워크에도 적용됩니다.

---

## Ⅰ. 개요 (Context & Background)

TCP 흐름 제어(Flow Control)는 송신자가 수신자의 처리 능력을 초과하여 데이터를 전송하지 않도록 조절하는 메커니즘입니다. 이는 혼잡 제어(Congestion Control)가 네트워크 내부 상태를 고려하는 것과 대조적으로, 오직 수신자의 로컬 상태(버퍼 여유 공간)에 기반합니다.

**💡 비유**: TCP 흐름 제어는 **'물통 채우기'**와 같습니다. 물(데이터)을 붓는 사람(송신자)은 받는 사람의 컵(수신 버퍼) 크기를 알아야 합니다. 컵이 꽉 차면 물이 넘치므로(오버플로우), 받는 사람은 "잠깐 멈춰, 마시고 있어"라고 말해야(Zero Window) 합니다.

**등장 배경 및 발전 과정**:
1. **기존 기술의 치명적 한계점**: Stop-and-Wait 프로토콜은 한 패킷을 보내고 ACK를 기다려야 하므로, 고대역폭-고지연 네트워크(BDP가 큰 경우)에서 효율이 1% 미만으로 떨어집니다.
2. **혁신적 패러다임 변화**: 슬라이딩 윈도우(Sliding Window) 프로토콴은 윈도우 크기만큼 연속 전송을 허용하여 파이프라인 효과를 냄으로써 전송 효율을 극대화했습니다.
3. **비즈니스적 요구사항**: 현대 웹 서비스, 스트리밍, 클라우드 스토리지 등에서는 대용량 파일 전송 시 흐름 제어가 병목이 되지 않도록 Window Scaling, Large Receive Offload(LRO) 등의 최적화가 필요합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 슬라이딩 윈도우 프로토콜 구조

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Sliding Window Protocol                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  송신 윈도우 (Send Window):                                                  │
│                                                                             │
│         ACKed        Sent (Not ACKed)         Usable         Cannot Send    │
│  ┌────────────┬─────────────────────────┬──────────────┬──────────────────┐│
│  │ ●●●●●●●●●● │ ████████████████████████ │              │                  ││
│  └────────────┴─────────────────────────┴──────────────┴──────────────────┘│
│       1~100           101~150                151~200         201+           │
│       ↑                  ↑                      ↑            ↑              │
│    LastAcked         LastSent              WindowEnd     NextSeq          │
│                     (FlightSize)           (LastAcked    (NextToSend)      │
│                                            + WinSize)                      │
│                                                                             │
│  윈도우 크기 = min(cwnd, rwnd)                                               │
│  FlightSize = LastSent - LastAcked                                          │
│  Usable Window = WindowSize - FlightSize                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      수신 윈도우 (Receive Window)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│         Buffer     Received (Buffered)          Free                        │
│  ┌────────────┬─────────────────────────┬──────────────────────────────┐   │
│  │            │ ████████████████████████ │                              │   │
│  └────────────┴─────────────────────────┴──────────────────────────────┘   │
│       0~100           101~180                 181~65535                    │
│       ↑                  ↑                        ↑                        │
│    LastRead          LastRcvd                RcvWindow                     │
│  (Application      (Next expected            (Available                    │
│   read)             seq - 1)                 buffer space)                │
│                                                                             │
│  RcvWindow = BufferSize - (LastRcvd - LastRead)                            │
│  Advertised Window = RcvWindow (ACK에 포함되어 송신자에게 통지)             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 변수 및 관계식

| 변수 | 정의 | TCP 헤더 필드 | 설명 |
|---|---|---|---|
| **rwnd** | Receive Window | Window Size (16-bit) | 수신자의 사용 가능 버퍼 |
| **cwnd** | Congestion Window | (내부 변수) | 혼잡 제어에 의한 제한 |
| **SND.WND** | Send Window | - | min(cwnd, rwnd) |
| **SND.UNA** | Send Unacknowledged | - | ACK 받지 않은 가장 오래된 바이트 |
| **SND.NXT** | Send Next | - | 다음 전송할 바이트 번호 |
| **RCV.NXT** | Receive Next | - | 다음 수신 예상 바이트 번호 |
| **RCV.WND** | Receive Window | - | 수신 버퍼 여유 공간 |

```
윈도우 크기 결정:
Effective Window = min(cwnd, rwnd)

전송 가능 조건:
SND.NXT < SND.UNA + Effective Window

Flight Size (전송 중인 데이터):
FlightSize = SND.NXT - SND.UNA

전송 가능량:
UsableWindow = Effective Window - FlightSize
```

### 심층 동작 원리

**1. 기본 슬라이딩 윈도우 동작**

```
초기 상태:
• 윈도우 크기 = 4
• 시퀀스 번호: 1~4 전송 가능

단계 1: 데이터 1, 2, 3, 4 전송
        [1][2][3][4]  →
        FlightSize = 4, UsableWindow = 0

단계 2: ACK 3 수신 (누적 ACK)
        ← ACK(3)
        윈도우 슬라이드: 1, 2 ACKed → 5, 6 전송 가능
        [3][4][5][6]
        FlightSize = 2 (3, 4 미ACK), UsableWindow = 2

단계 3: ACK 5 수신
        ← ACK(5)
        윈도우 슬라이드: 3, 4 ACKed → 7, 8 전송 가능
        [5][6][7][8]

수학적 모델:
Throughput = WindowSize / RTT

예: WindowSize = 64KB, RTT = 50ms
Throughput = 65536 / 0.05 = 1,310,720 bps ≈ 1.25 Mbps

최적 윈도우 크기 (BDP):
Optimal Window = Bandwidth × RTT

예: 1Gbps 링크, 50ms RTT
Optimal Window = 10^9 × 0.05 / 8 = 6.25 MB
```

**2. Zero Window Probe (Persist Timer)**

```
상황: 수신자 버퍼가 꽉 참 (rwnd = 0)

동작:
1. 수신자가 ACK에 rwnd = 0을 포함하여 전송
2. 송신자는 전송 중지, Persist Timer 시작
3. Persist Timer 만료 시 1바이트 Probe 전송
4. 수신자는 rwnd 업데이트하여 응답

Persist Timer:
• 초기값: 500ms
• 지수 백오프: 최대 60초까지 증가
• RTO와 별도로 동작

Probe 형식:
• 1바이트 데이터 (시퀀스 번호는 SND.NXT - 1)
• 수신자는 이미 받은 데이터이므로 ACK만 응답

코드 개요:
if (rwnd == 0):
    start_persist_timer()
    send_zero_window_probe()
```

**3. Silly Window Syndrome (SWS)**

```
문제:
수신자가 1바이트씩 버퍼를 비우고, 매번 작은 rwnd를 통지
→ 송신자가 1바이트씩만 전송
→ 헤더 오버헤드 폭증 (40바이트 헤더 : 1바이트 데이터)

송신자 해결책 - Nagle 알고리즘:
if (data_to_send <= MSS):
    if (no_unacked_data):
        send(data)
    else:
        buffer(data)  # ACK 올 때까지 대기
        if (ack_received or buffer_full):
            send(buffered_data)

수신자 해결책 - Clark 해결책:
if (free_buffer < MSS and free_buffer < 0.5 × BufferSize):
    advertise_rwnd = 0  # 충분한 공간 생길 때까지 0 통지
else:
    advertise_rwnd = free_buffer

Nagle 알고리즘 비활성화:
• TCP_NODELAY 소켓 옵션
• 실시간 게임, 원격 터미널(SSH) 등에서 사용
```

**4. Window Scaling (RFC 7323)**

```
문제:
TCP 헤더의 Window Size 필드 = 16비트
최대 65535바이트 = 64KB
고속 네트워크에서 부족

예: 10Gbps, 100ms RTT
필요 윈도우 = 10^10 × 0.1 / 8 = 125 MB
→ 64KB로는 불가능!

해결: Window Scaling Option
• 3-way handshake 시 협상
• shift count (0~14) 사용
• 실제 윈도우 = rwnd × 2^shift_count

예:
shift_count = 7
실제 윈도우 = 65535 × 2^7 = 65535 × 128 ≈ 8MB

TCP 옵션 형식:
Kind: 3
Length: 3
Scale: shift_count (1바이트)

최대 확장:
shift_count = 14 → 윈도우 최대 1GB
```

### 핵심 코드: 슬라이딩 윈도우 시뮬레이션 (Python)

```python
import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from enum import Enum

class SegmentState(Enum):
    NOT_SENT = "not_sent"
    SENT = "sent"
    ACKED = "acked"

@dataclass
class Segment:
    seq: int
    size: int
    state: SegmentState = SegmentState.NOT_SENT

@dataclass
class TCPSlidingWindow:
    """TCP 슬라이딩 윈도우 시뮬레이터"""

    # 설정
    mss: int = 1460  # Maximum Segment Size
    initial_rwnd: int = 65535  # 초기 수신 윈도우
    initial_cwnd: int = 29200  # 초기 혼잡 윈도우 (20 MSS)

    # 상태 변수
    snd_una: int = 1  # 가장 오래된 미ACK 시퀀스
    snd_nxt: int = 1  # 다음 전송할 시퀀스
    rwnd: int = 65535  # 수신 윈도우
    cwnd: int = 29200  # 혼잡 윈도우

    # 버퍼
    send_buffer: List[Segment] = field(default_factory=list)
    recv_buffer: bytearray = field(default_factory=bytearray)

    # 통계
    bytes_sent: int = 0
    bytes_acked: int = 0
    retransmissions: int = 0

    def effective_window(self) -> int:
        """유효 윈도우 크기"""
        return min(self.cwnd, self.rwnd)

    def flight_size(self) -> int:
        """전송 중인 데이터 양"""
        return self.snd_nxt - self.snd_una

    def usable_window(self) -> int:
        """전송 가능한 데이터 양"""
        return self.effective_window() - self.flight_size()

    def can_send(self, data_size: int) -> bool:
        """전송 가능 여부 확인"""
        return self.usable_window() >= data_size

    def send_data(self, data: bytes) -> List[Segment]:
        """데이터 전송"""
        segments = []
        offset = 0

        while offset < len(data):
            # 세그먼트 크기 결정
            chunk_size = min(self.mss, len(data) - offset)

            # 윈도우 체크
            if not self.can_send(chunk_size):
                break

            # 세그먼트 생성
            seq = self.snd_nxt
            segment = Segment(seq=seq, size=chunk_size, state=SegmentState.SENT)
            segments.append(segment)
            self.send_buffer.append(segment)

            # 상태 업데이트
            self.snd_nxt += chunk_size
            self.bytes_sent += chunk_size
            offset += chunk_size

        return segments

    def receive_ack(self, ack_num: int, new_rwnd: int) -> Tuple[int, int]:
        """
        ACK 수신 처리

        Returns:
            (acked_bytes, duplicate_ack_count)
        """
        acked_bytes = 0

        # 윈도우 업데이트
        self.rwnd = new_rwnd

        # ACK된 세그먼트 처리
        for seg in self.send_buffer[:]:
            if seg.seq + seg.size <= ack_num and seg.state == SegmentState.SENT:
                seg.state = SegmentState.ACKED
                acked_bytes += seg.size
                self.snd_una = seg.seq + seg.size
                self.bytes_acked += seg.size
                self.send_buffer.remove(seg)

        return acked_bytes, 0  # 단순화: dup ack 미구현

    def simulate_zero_window(self) -> None:
        """Zero Window 시뮬레이션"""
        self.rwnd = 0

    def update_receive_window(self, bytes_consumed: int, buffer_size: int) -> None:
        """수신 윈도우 업데이트 (수신자 관점)"""
        # 실제로는 수신 버퍼에서 읽은 만큼 rwnd 증가
        pass


class FlowControlAnalyzer:
    """흐름 제어 분석 도구"""

    @staticmethod
    def calculate_optimal_window(bandwidth_bps: int, rtt_sec: float) -> int:
        """
        최적 윈도우 크기 계산 (BDP)

        Args:
            bandwidth_bps: 대역폭 (bps)
            rtt_sec: RTT (초)

        Returns:
            최적 윈도우 크기 (바이트)
        """
        return int(bandwidth_bps * rtt_sec / 8)

    @staticmethod
    def calculate_throughput(window_size: int, rtt_sec: float) -> float:
        """
        처리량 계산

        Args:
            window_size: 윈도우 크기 (바이트)
            rtt_sec: RTT (초)

        Returns:
            처리량 (bps)
        """
        return window_size * 8 / rtt_sec

    @staticmethod
    def calculate_window_scale(required_window: int) -> int:
        """
        필요한 Window Scale 값 계산

        Args:
            required_window: 필요한 윈도우 크기 (바이트)

        Returns:
            shift count (0~14)
        """
        max_standard_window = 65535
        if required_window <= max_standard_window:
            return 0

        # 필요한 shift count 계산
        scale = 0
        while (max_standard_window << scale) < required_window and scale < 14:
            scale += 1

        return scale

    @staticmethod
    def analyze_sws_impact(small_packet_size: int, num_packets: int) -> dict:
        """
        Silly Window Syndrome 영향 분석

        Args:
            small_packet_size: 작은 패킷 크기
            num_packets: 패킷 수

        Returns:
            분석 결과
        """
        tcp_ip_header = 40  # TCP(20) + IP(20)
        total_data = small_packet_size * num_packets
        overhead = tcp_ip_header * num_packets
        efficiency = total_data / (total_data + overhead) * 100

        # Nagle 적용 시
        mss = 1460
        nagle_packets = total_data // mss + (1 if total_data % mss else 0)
        nagle_overhead = tcp_ip_header * nagle_packets
        nagle_efficiency = total_data / (total_data + nagle_overhead) * 100

        return {
            'sws_efficiency': efficiency,
            'nagle_efficiency': nagle_efficiency,
            'sws_packets': num_packets,
            'nagle_packets': nagle_packets,
            'improvement': nagle_efficiency - efficiency
        }


def demonstrate_sliding_window():
    """슬라이딩 윈도우 시연"""
    print("=" * 60)
    print("TCP 슬라이딩 윈도우 시뮬레이션")
    print("=" * 60)

    window = TCPSlidingWindow(mss=1460, initial_rwnd=65535, initial_cwnd=29200)

    print(f"\n[초기 상태]")
    print(f"  MSS: {window.mss} bytes")
    print(f"  rwnd: {window.rwnd} bytes")
    print(f"  cwnd: {window.cwnd} bytes")
    print(f"  유효 윈도우: {window.effective_window()} bytes")

    # 데이터 전송 시뮬레이션
    data = b"x" * 50000  # 50KB 데이터
    segments = window.send_data(data)

    print(f"\n[전송 후]")
    print(f"  전송된 세그먼트: {len(segments)}개")
    print(f"  전송된 바이트: {window.bytes_sent} bytes")
    print(f"  Flight Size: {window.flight_size()} bytes")
    print(f"  남은 윈도우: {window.usable_window()} bytes")

    # ACK 수신 시뮬레이션
    acked, _ = window.receive_ack(20000, 65535)
    print(f"\n[ACK 수신 후 (ack=20000)]")
    print(f"  ACK된 바이트: {acked} bytes")
    print(f"  SND.UNA: {window.snd_una}")
    print(f"  남은 윈도우: {window.usable_window()} bytes")


def analyze_network_scenarios():
    """네트워크 시나리오 분석"""
    print("\n" + "=" * 60)
    print("네트워크 시나리오 분석")
    print("=" * 60)

    analyzer = FlowControlAnalyzer()

    scenarios = [
        ("1Gbps LAN", 1e9, 0.001),
        ("100Mbps WAN", 100e6, 0.05),
        ("10Mbps Satellite", 10e6, 0.6),
        ("10Gbps Datacenter", 10e9, 0.0001),
    ]

    print(f"\n{'시나리오':<20} {'RTT':<10} {'BDP':<15} {'Window Scale':<15}")
    print("-" * 60)

    for name, bw, rtt in scenarios:
        bdp = analyzer.calculate_optimal_window(bw, rtt)
        scale = analyzer.calculate_window_scale(bdp)
        print(f"{name:<20} {rtt*1000:.1f}ms    {bdp/1024:.1f}KB        {scale}")


def analyze_sws():
    """SWS 분석"""
    print("\n" + "=" * 60)
    print("Silly Window Syndrome 분석")
    print("=" * 60)

    analyzer = FlowControlAnalyzer()

    # 1바이트씩 1000개 전송 시뮬레이션
    result = analyzer.analyze_sws_impact(1, 1000)

    print(f"\n1바이트 패킷 1000개 전송:")
    print(f"  SWS 효율: {result['sws_efficiency']:.2f}%")
    print(f"  Nagle 효율: {result['nagle_efficiency']:.2f}%")
    print(f"  패킷 수: {result['sws_packets']} → {result['nagle_packets']}")
    print(f"  개선: {result['improvement']:.2f}%")


if __name__ == "__main__":
    demonstrate_sliding_window()
    analyze_network_scenarios()
    analyze_sws()
