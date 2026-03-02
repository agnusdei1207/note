+++
title = "OSI 7계층 (OSI 7 Layer Model)"
date = 2025-03-01

[extra]
categories = "pe_exam-network"
+++

# OSI 7계층 (OSI 7 Layer Model)

## 핵심 인사이트 (3줄 요약)
> **네트워크 통신을 7개 기능 계층으로 표준화한 ISO 참조 모델**. 물리→데이터링크→네트워크→전송→세션→표현→응용으로 구성. 실제는 TCP/IP가 주류이지만, OSI는 학습·트러블슈팅·설계의 핵심 기준이다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: OSI(Open Systems Interconnection) 7계층은 **ISO(국제표준화기구)가 1984년 제정한 네트워크 통신 표준 참조 모델**로, 서로 다른 시스템 간 통신을 위해 통신 과정을 7개 기능 계층으로 나누어 체계화한 것이다.

> 💡 **비유**: OSI 7계층은 **"택배 배송 시스템"** 같아요.
> 1층(물리): 도로와 트럭
> 2층(데이터링크): 화물 적재 및 운송
> 3층(네트워크): 배송 경로 계획 (내비게이션)
> 4층(전송): 배송 확인 및 재발송
> 5~7층: 주문서 작성, 포장, 고객 서비스
>
> 각 단계가 독립적으로 작동하면서도 서로 협력하죠!

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 시스템 간 비호환성**: 1970년대 IBM SNA, DECnet, AppleTalk 등 독자적 네트워크 아키텍처로 서로 통신 불가
2. **기술적 필요성 - 표준화**: 이기종 시스템 간 상호 연결을 위한 개방형 표준 모델 필요
3. **시장/산업 요구 - 모듈화**: 통신 기능을 계층화하여 특정 계층 기술 변경 시 다른 계층에 영향 없도록 설계

**핵심 목적**: **이기종 시스템 간 상호 연결성 확보, 통신 기능 모듈화, 기술 표준화**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**OSI 7계층 전체 구조** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        OSI 7계층 참조 모델                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   송신측                         계층               수신층             │
│   ═══════                       ═══════            ═══════             │
│                                                                         │
│   ┌──────────────┐            ┌──────────────┐     ┌──────────────┐    │
│   │   사용자     │            │ 7. 응용 계층  │     │   사용자     │    │
│   │   데이터     │────────────│  Application │─────│   데이터     │    │
│   └──────────────┘            │    Data      │     └──────────────┘    │
│                               └──────┬───────┘                         │
│   ┌──────────────┐            ┌──────▼───────┐     ┌──────────────┐    │
│   │   암호화     │            │ 6. 표현 계층  │     │   복호화     │    │
│   │   압축       │────────────│ Presentation │─────│   압축해제   │    │
│   └──────────────┘            │    Data      │     └──────────────┘    │
│                               └──────┬───────┘                         │
│   ┌──────────────┐            ┌──────▼───────┐     ┌──────────────┐    │
│   │ 세션 시작/종료│            │ 5. 세션 계층  │     │ 세션 시작/종료│    │
│   │   동기화     │────────────│   Session    │─────│   동기화     │    │
│   └──────────────┘            │    Data      │     └──────────────┘    │
│                               └──────┬───────┘                         │
│   ┌──────────────┐            ┌──────▼───────┐     ┌──────────────┐    │
│   │   세그먼트   │            │ 4. 전송 계층  │     │   세그먼트   │    │
│   │   분할/재조립│────────────│   Transport  │─────│   분할/재조립│    │
│   └──────────────┘            │   Segment    │     └──────────────┘    │
│                               └──────┬───────┘                         │
│   ┌──────────────┐            ┌──────▼───────┐     ┌──────────────┐    │
│   │   패킷       │            │ 3. 네트워크   │     │   패킷       │    │
│   │   라우팅     │────────────│   Network    │─────│   라우팅     │    │
│   └──────────────┘            │   Packet     │     └──────────────┘    │
│                               └──────┬───────┘                         │
│   ┌──────────────┐            ┌──────▼───────┐     ┌──────────────┐    │
│   │   프레임     │            │2. 데이터링크  │     │   프레임     │    │
│   │   MAC 주소   │────────────│  Data Link   │─────│   MAC 주소   │    │
│   └──────────────┘            │   Frame      │     └──────────────┘    │
│                               └──────┬───────┘                         │
│   ┌──────────────┐            ┌──────▼───────┐     ┌──────────────┐    │
│   │   비트       │            │ 1. 물리 계층  │     │   비트       │    │
│   │   전기 신호  │════════════│   Physical   │═════│   전기 신호  │    │
│   └──────────────┘            │    Bit       │     └──────────────┘    │
│                               └──────────────┘                         │
│                                    ▲                                    │
│                               ┌────┴────┐                               │
│                               │ 전송매체 │                               │
│                               │(케이블)  │                               │
│                               └─────────┘                               │
│                                                                         │
│   ◀───────────────────────────────────────────────────────────────▶    │
│              캡슐화 (Encapsulation)  /  역캡슐화 (Decapsulation)        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**계층별 상세 구성 요소** (필수: 표):
| 계층 | 이름 | PDU | 핵심 기능 | 주요 프로토콜 | 대표 장비 |
|------|------|-----|----------|--------------|----------|
| **7** | 응용 (Application) | Data | 사용자 인터페이스, 네트워크 서비스 | HTTP, FTP, SMTP, DNS, SSH | L7 스위치, ADC |
| **6** | 표현 (Presentation) | Data | 데이터 변환, 암호화, 압축 | SSL/TLS, JPEG, MPEG, ASN.1 | - |
| **5** | 세션 (Session) | Data | 세션 관리, 동기화, 토큰 제어 | RPC, NetBIOS, SIP, NFS | - |
| **4** | 전송 (Transport) | Segment | 종단 간 신뢰성, 흐름/혼잡 제어 | TCP, UDP, SCTP, QUIC | L4 스위치, 방화벽 |
| **3** | 네트워크 (Network) | Packet | 라우팅, 논리 주소, 패킷 전달 | IP, ICMP, ARP, OSPF, BGP | 라우터, L3 스위치 |
| **2** | 데이터링크 (Data Link) | Frame | 프레이밍, MAC 주소, 오류/흐름 제어 | Ethernet, Wi-Fi, PPP, HDLC | 스위치, 브리지 |
| **1** | 물리 (Physical) | Bit | 비트 전송, 전기/광 신호 변환 | RS-232, 1000BASE-T | 허브, 리피터, 케이블 |

**캡슐화/역캡슐화 과정** (필수: 상세 설명):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    데이터 캡슐화 (Encapsulation)                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   송신측:                                                               │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                         사용자 데이터                            │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                              │ + L7 헤더                                │
│                              ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ [L7 Header] 사용자 데이터                                        │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                              │ + L4 헤더 (TCP/UDP)                      │
│                              ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ [TCP 헤더] [L7 Header] 사용자 데이터                 ← Segment  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                              │ + L3 헤더 (IP)                           │
│                              ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ [IP 헤더] [TCP 헤더] [L7 Header] 사용자 데이터       ← Packet   │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                              │ + L2 헤더/트레일러 (Ethernet)            │
│                              ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ [Eth Hdr][IP][TCP][L7][Data][FCS]                    ← Frame    │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                              │ 비트 직렬화                              │
│                              ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ 01010101010101010101010101010101...                  ← Bits     │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│   수신측: 역캡슐화 (Decapsulation) - 반대 과정                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

[각 계층 헤더 상세]

Ethernet Frame (L2):
┌────────────┬────────────┬────────────┬─────────────┬─────┐
│ 프리앰블   │ 목적지 MAC  │ 출발지 MAC  │   타입      │ FCS │
│  (8B)     │   (6B)     │   (6B)     │  (2B)       │(4B) │
└────────────┴────────────┴────────────┴─────────────┴─────┘
                           │            │
                      유니캐스트/     IPv4=0x0800
                      멀티캐스트/     IPv6=0x86DD
                      브로드캐스트    ARP=0x0806

IP Packet (L3):
┌────────┬────────┬─────────────┬───────────┬──────────────┐
│ 버전   │ 헤더길이│ 서비스타입   │ 전체길이   │ 식별자       │
│ (4b)   │ (4b)   │   (1B)      │  (2B)     │   (2B)       │
├────────┴────────┴─────────────┴───────────┴──────────────┤
│ 플래그 │ 단편오프셋 │ TTL   │ 프로토콜   │ 헤더체크섬    │
│ (3b)   │  (13b)    │ (1B)  │   (1B)     │   (2B)        │
├───────────────────────────────────────────────────────────┤
│               출발지 IP 주소 (4B)                         │
├───────────────────────────────────────────────────────────┤
│               목적지 IP 주소 (4B)                         │
├───────────────────────────────────────────────────────────┤
│               옵션 (가변) + 데이터                        │
└───────────────────────────────────────────────────────────┘

TCP Segment (L4):
┌────────────────────┬────────────────────┐
│   출발지 포트 (2B)  │   목적지 포트 (2B)  │
├────────────────────┴────────────────────┤
│           시퀀스 번호 (4B)               │
├─────────────────────────────────────────┤
│           확인 응답 번호 (4B)            │
├───────┬───────┬─────────────────────────┤
│헤더길이│ 예약  │URG|ACK|PSH|RST|SYN|FIN │
│ (4b)  │ (6b)  │        플래그 (6b)       │
├───────┴───────┼───────────┬─────────────┤
│  윈도우 (2B)  │체크섬 (2B) │긴급포인터(2B)│
├───────────────┴───────────┴─────────────┤
│           옵션 (가변) + 데이터           │
└─────────────────────────────────────────┘
```

**핵심 알고리즘/공식** (해당 시 필수):
```
[MTU (Maximum Transmission Unit)]

MTU = 데이터링크 계층에서 전송 가능한 최대 프레임 크기
    = L2 헤더(14B) + IP 패킷(1500B) + FCS(4B) = 1518B (이더넷)

IP 패킷이 MTU 초과 시 단편화(Fragmentation) 발생
단편화 비트: DF(Don't Fragment), MF(More Fragments)

[TCP MSS (Maximum Segment Size)]

MSS = MTU - IP 헤더(20B) - TCP 헤더(20B)
    = 1500 - 20 - 20 = 1460B (이더넷 기본)

[서브넷팅 공식]

서브넷 개수 = 2^n (n: 서브넷 비트 수)
호스트 개수 = 2^h - 2 (h: 호스트 비트 수, -2는 네트워크/브로드캐스트 주소)

[OSI vs TCP/IP 매핑]

┌─────────────────────────────────────────────┐
│    OSI 7계층          │    TCP/IP 4계층    │
├───────────────────────┼────────────────────┤
│    7. 응용            │                    │
│    6. 표현            │   4. 응용 계층     │
│    5. 세션            │                    │
├───────────────────────┼────────────────────┤
│    4. 전송            │   3. 전송 계층     │
├───────────────────────┼────────────────────┤
│    3. 네트워크        │   2. 인터넷 계층   │
├───────────────────────┼────────────────────┤
│    2. 데이터링크      │   1. 네트워크      │
│    1. 물리            │      접근 계층     │
└───────────────────────┴────────────────────┘

[스위칭 레이어별 처리]

L2 스위치: MAC 주소 기반 프레임 전달 (플러딩/필터링/포워딩)
L3 스위치: IP 주소 기반 패킷 라우팅 (하드웨어 가속)
L4 스위치: 포트 기반 세션 분배 (로드밸런싱)
L7 스위치: HTTP URL, 쿠키 기반 콘텐츠 분배 (ADC)
```

**코드 예시** (필수: Python 패킷 분석):
```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum, auto
import struct
import binascii

# ============================================================
# OSI 7계층 패킷 분석기
# ============================================================

class ProtocolType(Enum):
    """프로토콜 타입"""
    # Layer 3
    IPV4 = 0x0800
    IPV6 = 0x86DD
    ARP = 0x0806
    # Layer 4
    TCP = 6
    UDP = 17
    ICMP = 1


@dataclass
class EthernetFrame:
    """이더넷 프레임 (Layer 2)"""
    preamble: bytes = b''
    dst_mac: str = ""
    src_mac: str = ""
    ethertype: int = 0
    payload: bytes = b''
    fcs: int = 0

    @classmethod
    def parse(cls, data: bytes) -> 'EthernetFrame':
        """이더넷 프레임 파싱"""
        # 프리앰블(8B) 제외하고 파싱
        dst_mac = cls._format_mac(data[0:6])
        src_mac = cls._format_mac(data[6:12])
        ethertype = struct.unpack('!H', data[12:14])[0]
        payload = data[14:-4]  # FCS 제외
        fcs = struct.unpack('!I', data[-4:])[0] if len(data) >= 4 else 0

        return cls(
            dst_mac=dst_mac,
            src_mac=src_mac,
            ethertype=ethertype,
            payload=payload,
            fcs=fcs
        )

    @staticmethod
    def _format_mac(mac_bytes: bytes) -> str:
        """MAC 주소 포맷팅"""
        return ':'.join(f'{b:02x}' for b in mac_bytes).upper()

    def __str__(self):
        return (f"[L2 Ethernet Frame]\n"
                f"  목적지 MAC: {self.dst_mac}\n"
                f"  출발지 MAC: {self.src_mac}\n"
                f"  EtherType: 0x{self.ethertype:04x}")


@dataclass
class IPv4Packet:
    """IPv4 패킷 (Layer 3)"""
    version: int = 4
    ihl: int = 5  # Internet Header Length (32비트 단위)
    dscp: int = 0
    total_length: int = 0
    identification: int = 0
    flags: int = 0
    fragment_offset: int = 0
    ttl: int = 64
    protocol: int = 6
    checksum: int = 0
    src_ip: str = ""
    dst_ip: str = ""
    payload: bytes = b''

    @classmethod
    def parse(cls, data: bytes) -> 'IPv4Packet':
        """IPv4 패킷 파싱"""
        version_ihl = data[0]
        version = version_ihl >> 4
        ihl = (version_ihl & 0x0F) * 4  # 바이트 단위로 변환

        dscp_ecn = data[1]
        dscp = dscp_ecn >> 2

        total_length = struct.unpack('!H', data[2:4])[0]
        identification = struct.unpack('!H', data[4:6])[0]
        flags_frag = struct.unpack('!H', data[6:8])[0]
        flags = flags_frag >> 13
        fragment_offset = flags_frag & 0x1FFF

        ttl = data[8]
        protocol = data[9]
        checksum = struct.unpack('!H', data[10:12])[0]

        src_ip = cls._format_ip(data[12:16])
        dst_ip = cls._format_ip(data[16:20])

        payload = data[ihl:]

        return cls(
            version=version,
            ihl=ihl,
            dscp=dscp,
            total_length=total_length,
            identification=identification,
            flags=flags,
            fragment_offset=fragment_offset,
            ttl=ttl,
            protocol=protocol,
            checksum=checksum,
            src_ip=src_ip,
            dst_ip=dst_ip,
            payload=payload
        )

    @staticmethod
    def _format_ip(ip_bytes: bytes) -> str:
        """IP 주소 포맷팅"""
        return '.'.join(str(b) for b in ip_bytes)

    @property
    def protocol_name(self) -> str:
        protocols = {6: 'TCP', 17: 'UDP', 1: 'ICMP'}
        return protocols.get(self.protocol, f'Unknown({self.protocol})')

    def __str__(self):
        return (f"[L3 IPv4 Packet]\n"
                f"  버전: {self.version}, 헤더길이: {self.ihl}B\n"
                f"  출발지 IP: {self.src_ip}\n"
                f"  목적지 IP: {self.dst_ip}\n"
                f"  TTL: {self.ttl}\n"
                f"  프로토콜: {self.protocol_name}")


@dataclass
class TCPSegment:
    """TCP 세그먼트 (Layer 4)"""
    src_port: int = 0
    dst_port: int = 0
    seq_num: int = 0
    ack_num: int = 0
    data_offset: int = 5
    flags: int = 0
    window: int = 0
    checksum: int = 0
    urgent_ptr: int = 0
    payload: bytes = b''

    # 플래그 비트
    FLAG_FIN = 0x01
    FLAG_SYN = 0x02
    FLAG_RST = 0x04
    FLAG_PSH = 0x08
    FLAG_ACK = 0x10
    FLAG_URG = 0x20

    @classmethod
    def parse(cls, data: bytes) -> 'TCPSegment':
        """TCP 세그먼트 파싱"""
        src_port = struct.unpack('!H', data[0:2])[0]
        dst_port = struct.unpack('!H', data[2:4])[0]
        seq_num = struct.unpack('!I', data[4:8])[0]
        ack_num = struct.unpack('!I', data[8:12])[0]

        data_offset_flags = struct.unpack('!H', data[12:14])[0]
        data_offset = (data_offset_flags >> 12) * 4  # 바이트 단위
        flags = data_offset_flags & 0x3F

        window = struct.unpack('!H', data[14:16])[0]
        checksum = struct.unpack('!H', data[16:18])[0]
        urgent_ptr = struct.unpack('!H', data[18:20])[0]

        payload = data[data_offset:]

        return cls(
            src_port=src_port,
            dst_port=dst_port,
            seq_num=seq_num,
            ack_num=ack_num,
            data_offset=data_offset,
            flags=flags,
            window=window,
            checksum=checksum,
            urgent_ptr=urgent_ptr,
            payload=payload
        )

    @property
    def flag_str(self) -> str:
        flags = []
        if self.flags & self.FLAG_SYN: flags.append('SYN')
        if self.flags & self.FLAG_ACK: flags.append('ACK')
        if self.flags & self.FLAG_FIN: flags.append('FIN')
        if self.flags & self.FLAG_RST: flags.append('RST')
        if self.flags & self.FLAG_PSH: flags.append('PSH')
        if self.flags & self.FLAG_URG: flags.append('URG')
        return ','.join(flags) if flags else 'NONE'

    def __str__(self):
        return (f"[L4 TCP Segment]\n"
                f"  출발지 포트: {self.src_port}\n"
                f"  목적지 포트: {self.dst_port}\n"
                f"  시퀀스 번호: {self.seq_num}\n"
                f"  확인 응답: {self.ack_num}\n"
                f"  플래그: [{self.flag_str}]\n"
                f"  윈도우: {self.window}")


@dataclass
class UDPSegment:
    """UDP 데이터그램 (Layer 4)"""
    src_port: int = 0
    dst_port: int = 0
    length: int = 0
    checksum: int = 0
    payload: bytes = b''

    @classmethod
    def parse(cls, data: bytes) -> 'UDPSegment':
        """UDP 데이터그램 파싱"""
        src_port = struct.unpack('!H', data[0:2])[0]
        dst_port = struct.unpack('!H', data[2:4])[0]
        length = struct.unpack('!H', data[4:6])[0]
        checksum = struct.unpack('!H', data[6:8])[0]
        payload = data[8:]

        return cls(
            src_port=src_port,
            dst_port=dst_port,
            length=length,
            checksum=checksum,
            payload=payload
        )

    def __str__(self):
        return (f"[L4 UDP Datagram]\n"
                f"  출발지 포트: {self.src_port}\n"
                f"  목적지 포트: {self.dst_port}\n"
                f"  길이: {self.length}B")


class OSIAnalyzer:
    """OSI 7계층 패킷 분석기"""

    # 잘 알려진 포트
    WELL_KNOWN_PORTS = {
        20: 'FTP-DATA', 21: 'FTP', 22: 'SSH', 23: 'TELNET',
        25: 'SMTP', 53: 'DNS', 67: 'DHCP', 68: 'DHCP',
        80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS',
        993: 'IMAPS', 995: 'POP3S', 3306: 'MySQL', 5432: 'PostgreSQL',
        6379: 'Redis', 8080: 'HTTP-ALT', 8443: 'HTTPS-ALT'
    }

    def __init__(self):
        self.layers: Dict[int, Any] = {}

    def analyze(self, raw_data: bytes) -> Dict:
        """패킷 분석"""
        result = {
            'layer2': None,
            'layer3': None,
            'layer4': None,
            'layer7': None
        }

        # Layer 2: 이더넷
        if len(raw_data) >= 14:
            eth = EthernetFrame.parse(raw_data)
            result['layer2'] = eth
            self.layers[2] = eth

            # Layer 3: IP
            if eth.ethertype == ProtocolType.IPV4.value:
                ip = IPv4Packet.parse(eth.payload)
                result['layer3'] = ip
                self.layers[3] = ip

                # Layer 4: TCP/UDP
                if ip.protocol == ProtocolType.TCP.value:
                    tcp = TCPSegment.parse(ip.payload)
                    result['layer4'] = tcp
                    self.layers[4] = tcp

                    # Layer 7 추정
                    result['layer7'] = self._guess_l7_protocol(tcp.src_port, tcp.dst_port)

                elif ip.protocol == ProtocolType.UDP.value:
                    udp = UDPSegment.parse(ip.payload)
                    result['layer4'] = udp
                    self.layers[4] = udp
                    result['layer7'] = self._guess_l7_protocol(udp.src_port, udp.dst_port)

        return result

    def _guess_l7_protocol(self, src_port: int, dst_port: int) -> str:
        """L7 프로토콜 추정"""
        port = dst_port if dst_port in self.WELL_KNOWN_PORTS else src_port
        return self.WELL_KNOWN_PORTS.get(port, f'Unknown (port {dst_port})')

    def print_analysis(self, result: Dict) -> None:
        """분석 결과 출력"""
        print("\n" + "=" * 60)
        print("           OSI 7계층 패킷 분석 결과")
        print("=" * 60)

        if result['layer2']:
            print(f"\n{result['layer2']}")

        if result['layer3']:
            print(f"\n{result['layer3']}")

        if result['layer4']:
            print(f"\n{result['layer4']}")

        if result['layer7']:
            print(f"\n[L7 Application]")
            print(f"  추정 프로토콜: {result['layer7']}")

        print("\n" + "=" * 60)


# ============================================================
# OSI 계층별 문제 해결 가이드
# ============================================================

class NetworkTroubleshooter:
    """네트워크 계층별 트러블슈팅"""

    TROUBLESHOOTING_GUIDE = {
        1: {
            'name': '물리 계층',
            'symptoms': ['링크 불가', '완전 단절', '잦은 연결 끊김'],
            'causes': ['케이블 단선', '포트 불량', '전원 문제', '거리 초과'],
            'tools': ['케이블 테스터', '광파워미터', 'OTDR'],
            'solutions': ['케이블 교체', '포트 변경', '리피터 설치']
        },
        2: {
            'name': '데이터링크 계층',
            'symptoms': ['느린 전송', 'CRC 오류', '프레임 드랍'],
            'causes': ['MAC 충돌', '스위치 루프', '듀플렉스 불일치', 'VLAN 설정 오류'],
            'tools': ['Wireshark', '스위치 로그', 'arp -a'],
            'solutions': ['STP 설정', '듀플렉스 통일', 'VLAN 재구성']
        },
        3: {
            'name': '네트워크 계층',
            'symptoms': ['특정 대역 연결 불가', '지연 증가', '패킷 손실'],
            'causes': ['라우팅 오류', 'IP 충돌', '서브넷 마스크 오류', 'ACL 차단'],
            'tools': ['ping', 'traceroute', 'netstat -r', 'route print'],
            'solutions': ['라우팅 테이블 수정', 'IP 재할당', 'ACL 확인']
        },
        4: {
            'name': '전송 계층',
            'symptoms': ['연결 타임아웃', '데이터 누락', '재전송 반복'],
            'causes': ['포트 차단', '방화벽 규칙', 'TCP 윈도우 부족', '혼잡'],
            'tools': ['telnet', 'nc (netcat)', 'nmap', 'tcpdump'],
            'solutions': ['방화벽 규칙 수정', '윈도우 크기 조정', 'QoS 적용']
        },
        7: {
            'name': '응용 계층',
            'symptoms': ['서비스 접속 불가', '인증 실패', '느린 응답'],
            'causes': ['서비스 중지', '설정 오류', 'DNS 문제', '인증서 만료'],
            'tools': ['curl', 'nslookup', '애플리케이션 로그'],
            'solutions': ['서비스 재시작', '설정 확인', 'DNS 캐시 삭제']
        }
    }

    @classmethod
    def diagnose(cls, layer: int, symptom: str) -> str:
        """문제 진단"""
        if layer not in cls.TROUBLESHOOTING_GUIDE:
            return "알 수 없는 계층입니다."

        guide = cls.TROUBLESHOOTING_GUIDE[layer]

        result = f"\n=== Layer {layer}: {guide['name']} 문제 진단 ===\n"
        result += f"\n증상: {symptom}\n"
        result += f"\n가능한 원인:\n"
        for cause in guide['causes']:
            result += f"  - {cause}\n"
        result += f"\n진단 도구:\n"
        for tool in guide['tools']:
            result += f"  - {tool}\n"
        result += f"\n해결 방법:\n"
        for solution in guide['solutions']:
            result += f"  - {solution}\n"

        return result


# ============================================================
# 사용 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("         OSI 7계층 패킷 분석기 데모")
    print("=" * 60)

    # 샘플 이더넷 프레임 생성 (HTTP 요청 시뮬레이션)
    # 실제로는 네트워크 인터페이스에서 캡처

    # 이더넷 헤더 (14B)
    eth_header = bytes([
        0x00, 0x11, 0x22, 0x33, 0x44, 0x55,  # 목적지 MAC
        0x66, 0x77, 0x88, 0x99, 0xAA, 0xBB,  # 출발지 MAC
        0x08, 0x00  # IPv4
    ])

    # IP 헤더 (20B)
    ip_header = bytes([
        0x45, 0x00,  # Version(4), IHL(5), DSCP
        0x00, 0x3C,  # Total Length (60B)
        0x00, 0x01,  # Identification
        0x40, 0x00,  # Flags (DF), Fragment Offset
        0x40,        # TTL (64)
        0x06,        # Protocol (TCP)
        0x00, 0x00,  # Checksum (placeholder)
        192, 168, 1, 100,  # Source IP
        142, 250, 196, 142  # Dest IP (google.com)
    ])

    # TCP 헤더 (20B)
    tcp_header = bytes([
        0xC0, 0x01,  # Source Port (49153)
        0x01, 0xBB,  # Dest Port (443 = HTTPS)
        0x00, 0x00, 0x00, 0x01,  # Sequence Number
        0x00, 0x00, 0x00, 0x00,  # Ack Number
        0x50, 0x18,  # Data Offset (5), Flags (PSH, ACK)
        0xFF, 0xFF,  # Window
        0x00, 0x00,  # Checksum
        0x00, 0x00   # Urgent Pointer
    ])

    # FCS (4B)
    fcs = bytes([0x00, 0x00, 0x00, 0x00])

    # 전체 프레임 조립
    sample_frame = eth_header + ip_header + tcp_header + fcs

    # 분석 실행
    analyzer = OSIAnalyzer()
    result = analyzer.analyze(sample_frame)
    analyzer.print_analysis(result)

    # 트러블슈팅 예시
    print("\n" + "=" * 60)
    print("         네트워크 트러블슈팅 가이드")
    print("=" * 60)

    print(NetworkTroubleshooter.diagnose(3, "특정 대역 연결 불가"))
    print(NetworkTroubleshooter.diagnose(4, "연결 타임아웃"))
