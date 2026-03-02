+++
title = "DNS와 HTTP/HTTPS (DNS & HTTP/HTTPS)"
date = 2025-03-01

[extra]
categories = "pe_exam-network"
+++

# DNS와 HTTP/HTTPS (DNS & HTTP/HTTPS)

## 핵심 인사이트 (3줄 요약)
> **DNS는 도메인을 IP로 변환하는 분산 계층형 데이터베이스**. HTTP는 비연결·무상태 텍스트 프로토콜이며, HTTPS는 TLS 1.3 암호화를 추가한 보안 버전. HTTP/2·HTTP/3(QUIC)로 성능이 혁신적으로 개선되었다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**:
- **DNS(Domain Name System)**: 인간 친화적 도메인 이름(www.example.com)을 기계 친화적 IP 주소(93.184.216.34)로 변환하는 **전 세계 분산 계층형 데이터베이스 시스템**
- **HTTP/HTTPS**: 웹 상에서 하이퍼텍스트를 전송하기 위한 **요청-응답 기반 애플리케이션 계층 프로토콜**. HTTPS는 TLS/SSL 암호화 계층 추가

> 💡 **비유**: DNS는 **"인터넷 전화번호부"** 같아요. "홍길동"(도메인)을 찾으면 "010-1234-5678"(IP)를 알려주죠. HTTP는 **"음식 배달 주문서"** 같아요. 주문서(요청)를 내면 음식(응답)이 오고, 배달이 끝나면 연락이 끊기죠!

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - IP 주소 암기 불가**: 192.168.1.1 같은 숫자는 사람이 기억하기 어려움. hosts 파일 수동 관리의 한계
2. **기술적 필요성 - 분산 관리**: 단일 서버로 전 세계 도메인 관리 불가. 계층적 위임 구조 필요
3. **시장/산업 요구 - 웹 서비스 확산**: 1990년대 웹 폭발로 HTTP가 사실상 인터넷 표준 프로토콜이 됨. 보안(HTTPS)·성능(HTTP/2·3) 요구 증가

**핵심 목적**: **사용자 친화적 주소 체계, 안전하고 빠른 웹 콘텐츠 전송**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**DNS 계층 구조** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DNS 계층 구조                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                            ┌─────────┐                                  │
│                            │   .     │  ← Root DNS (전 세계 13개 클러스터)│
│                            │  Root   │    (A~M 서버, Anycast 운영)       │
│                            └────┬────┘                                  │
│                                 │                                       │
│         ┌───────────────────────┼───────────────────────┐              │
│         │                       │                       │               │
│    ┌────▼────┐           ┌─────▼─────┐          ┌──────▼──────┐       │
│    │   .com  │           │   .net    │          │    .kr      │       │
│    │  TLD    │           │   TLD     │          │   ccTLD     │       │
│    └────┬────┘           └─────┬─────┘          └──────┬──────┘       │
│         │                      │                       │               │
│    ┌────▼────┐                 │                 ┌─────▼─────┐        │
│    │example  │                 │                 │   .co     │        │
│    │.com SLD │                 │                 │  2nd TLD  │        │
│    └────┬────┘                 │                 └─────┬─────┘        │
│         │                      │                       │               │
│    ┌────▼────┐                 │                 ┌─────▼─────┐        │
│    │  www    │                 │                 │  naver    │        │
│    │ Subdomain                │                 │  SLD      │        │
│    └─────────┘                 │                 └───────────┘        │
│                                                                         │
│   DNS 쿼리 과정 (www.example.com):                                      │
│                                                                         │
│   ① 사용자 → 로컬 DNS (ISP 또는 8.8.8.8)                               │
│                    │                                                    │
│                    │ [캐시 MISS]                                        │
│                    ▼                                                    │
│   ② 로컬 DNS → Root DNS (".") → "com TLD 서버 목록 반환"               │
│                    │                                                    │
│                    ▼                                                    │
│   ③ 로컬 DNS → .com TLD → "example.com 네임서버 목록 반환"             │
│                    │                                                    │
│                    ▼                                                    │
│   ④ 로컬 DNS → example.com NS → "93.184.216.34 반환"                   │
│                    │                                                    │
│                    ▼                                                    │
│   ⑤ 로컬 DNS 캐시 저장 (TTL 동안) → 사용자에게 IP 응답                  │
│                                                                         │
│   총 소요 시간: 캐시 히트 시 1~10ms, MISS 시 50~200ms                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**DNS 레코드 타입** (필수: 표):
| 레코드 | 이름 | 설명 | 예시 |
|--------|------|------|------|
| **A** | Address | 도메인 → IPv4 | `example.com. IN A 93.184.216.34` |
| **AAAA** | IPv6 Address | 도메인 → IPv6 | `example.com. IN AAAA 2606:2800::1` |
| **CNAME** | Canonical Name | 별칭 → 정식 도메인 | `www.example.com. IN CNAME example.com.` |
| **MX** | Mail Exchange | 메일 서버 (우선순위) | `example.com. IN MX 10 mail.example.com.` |
| **NS** | Name Server | 권한 있는 네임서버 | `example.com. IN NS ns1.example.com.` |
| **TXT** | Text | 텍스트 정보 | SPF, DKIM, Google 사이트 인증 |
| **SOA** | Start of Authority | zone 정보 | 시리얼, 갱신 주기, TTL |
| **PTR** | Pointer | IP → 도메인 (역방향) | `34.216.184.93.in-addr.arpa.` |
| **SRV** | Service | 서비스 위치 | `_sip._tcp.example.com.` |

**HTTP 프로토콜 구조** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    HTTP 요청/응답 구조                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   [HTTP 요청 (Request)]                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ GET /api/users HTTP/1.1          ← 요청 라인 (Method Path Ver)  │  │
│   │ Host: api.example.com            ← 요청 헤더                    │  │
│   │ User-Agent: Mozilla/5.0                                          │  │
│   │ Accept: application/json                                         │  │
│   │ Authorization: Bearer eyJhbG...                                  │  │
│   │ Content-Type: application/json                                   │  │
│   │                                            ← 빈 줄 (CRLF)        │  │
│   │ {"name": "John", "age": 30}       ← 요청 본문 (Body)             │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│   [HTTP 응답 (Response)]                                                │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ HTTP/1.1 200 OK                   ← 상태 라인 (Ver Code Msg)    │  │
│   │ Date: Mon, 01 Jan 2025 00:00:00  ← 응답 헤더                    │  │
│   │ Server: nginx/1.24                                               │  │
│   │ Content-Type: application/json                                   │  │
│   │ Content-Length: 52                                               │  │
│   │ Cache-Control: max-age=3600                                      │  │
│   │                                            ← 빈 줄 (CRLF)        │  │
│   │ {"id":1,"name":"John","age":30}   ← 응답 본문 (Body)             │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    HTTP 상태 코드 분류                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1xx Informational (정보)                                              │
│     100 Continue   101 Switching Protocols                             │
│                                                                         │
│   2xx Success (성공)                                                    │
│     200 OK         201 Created         204 No Content                  │
│                                                                         │
│   3xx Redirection (리다이렉션)                                          │
│     301 Permanently  302 Found        304 Not Modified                 │
│     307 Temporary   308 Permanent                                      │
│                                                                         │
│   4xx Client Error (클라이언트 오류)                                    │
│     400 Bad Request  401 Unauthorized  403 Forbidden                   │
│     404 Not Found    405 Method       409 Conflict                     │
│     429 Too Many Requests                                               │
│                                                                         │
│   5xx Server Error (서버 오류)                                          │
│     500 Internal     502 Bad Gateway  503 Unavailable                  │
│     504 Gateway Timeout                                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**TLS 1.3 핸드셰이크** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TLS 1.3 핸드셰이크 (1-RTT)                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Client                                              Server            │
│     │                                                   │               │
│     │─── ClientHello ──────────────────────────────────►│               │
│     │     • Supported versions, cipher suites           │               │
│     │     • Key Share (ECDHE 공개키)                    │               │
│     │     • SNI (Server Name Indication)                │               │
│     │                                                   │               │
│     │◄── ServerHello ───────────────────────────────────│               │
│     │     • Selected version, cipher suite              │               │
│     │     • Key Share (서버 ECDHE 공개키)               │               │
│     │     • Certificate (서버 인증서)                   │               │
│     │     • CertificateVerify (서명)                    │               │
│     │     • Finished                                    │               │
│     │                                                   │               │
│     │ [양측 세션 키 계산 완료]                           │               │
│     │                                                   │               │
│     │─── Finished ─────────────────────────────────────►│               │
│     │                                                   │               │
│     │═══════════════ 암호화 통신 시작 ═══════════════════│               │
│     │                                                   │               │
│                                                                         │
│   TLS 1.3 vs TLS 1.2:                                                   │
│   • TLS 1.2: 2-RTT (ServerKeyExchange, ClientKeyExchange 추가)         │
│   • TLS 1.3: 1-RTT (Key Share로 키 교환 통합)                           │
│   • 0-RTT: 이전 세션 재사용 시 즉시 데이터 전송 가능                     │
│                                                                         │
│   제거된 알고리즘 (TLS 1.3):                                            │
│   • RSA 키 교환 (Forward Secrecy 없음)                                  │
│   • CBC 모드 암호 (BEAST, Lucky13 공격)                                 │
│   • RC4, MD5, SHA-1 (취약)                                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**HTTP 버전 비교** (필수: 표):
| 특성 | HTTP/1.0 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|------|----------|----------|--------|--------|
| **연결** | 매 요청 재연결 | Keep-Alive | 멀티플렉싱 | QUIC 연결 |
| **헤더** | 텍스트 | 텍스트 | HPACK 압축 | QPACK 압축 |
| **전송** | 순차 | 파이프라이닝 | 멀티플렉싱 | 독립 스트림 |
| **서버 푸시** | ✗ | ✗ | ✓ | ✓ |
| **HOL 블로킹** | O | O | TCP 레벨 | 해결 (UDP) |
| **프로토콜** | TCP | TCP | TCP | UDP(QUIC) |
| **0-RTT** | ✗ | ✗ | ✗ | ✓ |
| **연결 마이그레이션** | ✗ | ✗ | ✗ | ✓ |

**핵심 알고리즘/공식** (해당 시 필수):
```
[DNS TTL (Time To Live)]

TTL = 레코드가 캐시에 저장되는 시간 (초)
    = 권장값: 서비스 특성에 따라 다름

┌────────────────────────────────────────────┐
│ 레코드 타입   │ 권장 TTL      │ 이유       │
├────────────────────────────────────────────┤
│ A/AAAA       │ 300~3600초    │ 부하 분산  │
│ CNAME        │ 3600초        │ 안정적     │
│ MX           │ 3600~86400초  │ 잘 안 바뀜│
│ TXT (SPF)    │ 3600초        │ 보안 설정 │
│ NS           │ 86400초       │ 매우 안정 │
└────────────────────────────────────────────┘

[HTTP Keep-Alive]

Keep-Alive Timeout = 연결 유지 시간
Max = 연결당 최대 요청 수

예: Keep-Alive: timeout=5, max=100

[TCP 혼잡 윈도우와 HTTP]

혼잡 윈도우 = cwnd (Congestion Window)
전송 속도 = cwnd / RTT

HTTP/1.1: 요청별 TCP 연결 → slow-start 반복
HTTP/2: 단일 연결로 cwnd 효율적 사용
HTTP/3: QUIC의 독립 스트림으로 패킷 손실 영향 최소화

[HPACK 헤더 압축]

정적 테이블: 61개 자주 쓰는 헤더 (인덱스)
동적 테이블: 세션 중 학습한 헤더
허프만 코딩: 문자열 압축

압축률: 85~90% 감소 (vs HTTP/1.1 텍스트 헤더)

[QUIC 연결 ID]

Connection ID = 8~20바이트 식별자
→ IP 변경되어도 연결 유지 (모바일 WiFi↔LTE 전환)
```

**코드 예시** (필수: Python DNS/HTTP 클라이언트):
```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum, auto
import struct
import socket
import time

# ============================================================
# DNS 프로토콜 구현
# ============================================================

class DNSRecordType(Enum):
    """DNS 레코드 타입"""
    A = 1
    NS = 2
    CNAME = 5
    SOA = 6
    PTR = 12
    MX = 15
    TXT = 16
    AAAA = 28


class DNSClass(Enum):
    """DNS 클래스"""
    IN = 1    # Internet
    CS = 2    # CSNET
    CH = 3    # CHAOS
    HS = 4    # Hesiod


@dataclass
class DNSHeader:
    """DNS 헤더 (12바이트)"""
    id: int = 0           # 16비트 식별자
    qr: int = 0           # 0=쿼리, 1=응답
    opcode: int = 0       # 0=표준 쿼리
    aa: int = 0           # 권한 있는 응답
    tc: int = 0           # 잘림
    rd: int = 1           # 재귀 요청
    ra: int = 0           # 재귀 가능
    z: int = 0            # 예약
    rcode: int = 0        # 응답 코드
    qdcount: int = 1      # 질문 수
    ancount: int = 0      # 응답 수
    nscount: int = 0      # 권한 수
    arcount: int = 0      # 추가 수

    def pack(self) -> bytes:
        """헤더를 바이트로 변환"""
        flags = (self.qr << 15) | (self.opcode << 11) | (self.aa << 10) | \
                (self.tc << 9) | (self.rd << 8) | (self.ra << 7) | \
                (self.z << 4) | self.rcode
        return struct.pack('!HHHHHH',
                           self.id, flags, self.qdcount,
                           self.ancount, self.nscount, self.arcount)


@dataclass
class DNSQuestion:
    """DNS 질문 섹션"""
    qname: str
    qtype: int = 1  # A 레코드
    qclass: int = 1  # IN

    def pack(self) -> bytes:
        """질문을 바이트로 변환"""
        # 도메인 이름 인코딩 (라벨 길이 + 라벨)
        labels = self.qname.rstrip('.').split('.')
        qname_bytes = b''
        for label in labels:
            qname_bytes += bytes([len(label)]) + label.encode()
        qname_bytes += b'\x00'  # 종료

        return qname_bytes + struct.pack('!HH', self.qtype, self.qclass)


@dataclass
class DNSResourceRecord:
    """DNS 리소스 레코드"""
    name: str
    rtype: int
    rclass: int
    ttl: int
    rdata: Any

    @property
    def rdata_str(self) -> str:
        if self.rtype == DNSRecordType.A.value:
            return '.'.join(str(b) for b in self.rdata)
        elif self.rtype == DNSRecordType.MX.value:
            pref, exchange = self.rdata
            return f"{pref} {exchange}"
        return str(self.rdata)


class DNSClient:
    """간단한 DNS 클라이언트"""

    DNS_PORT = 53

    def __init__(self, server: str = "8.8.8.8"):
        self.server = server
        self.timeout = 5.0

    def query(self, domain: str, qtype: DNSRecordType = DNSRecordType.A) -> List[DNSResourceRecord]:
        """DNS 쿼리 수행"""
        # 쿼리 패킷 생성
        header = DNSHeader(id=int(time.time() * 1000) % 65536)
        question = DNSQuestion(qname=domain, qtype=qtype.value)

        packet = header.pack() + question.pack()

        # UDP 소켓으로 전송
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)

        try:
            sock.sendto(packet, (self.server, self.DNS_PORT))
            response, _ = sock.recvfrom(4096)
            return self._parse_response(response)
        finally:
            sock.close()

    def _parse_response(self, data: bytes) -> List[DNSResourceRecord]:
        """DNS 응답 파싱"""
        # 헤더 파싱 (12바이트)
        header_data = struct.unpack('!HHHHHH', data[:12])
        ancount = header_data[3]

        # 질문 섹션 건너뛰기
        offset = 12
        while data[offset] != 0:
            offset += data[offset] + 1
        offset += 5  # 종료 바이트 + qtype + qclass

        # 응답 섹션 파싱
        records = []
        for _ in range(ancount):
            # 이름 파싱 (압축 처리)
            name, offset = self._parse_name(data, offset)

            # 타입, 클래스, TTL, RDLENGTH
            rtype, rclass, ttl, rdlength = struct.unpack('!HHIH', data[offset:offset+10])
            offset += 10

            # RDATA 파싱
            rdata = data[offset:offset+rdlength]
            offset += rdlength

            # A 레코드면 IP 주소로 변환
            if rtype == DNSRecordType.A.value:
                rdata = tuple(rdata)

            records.append(DNSResourceRecord(
                name=name,
                rtype=rtype,
                rclass=rclass,
                ttl=ttl,
                rdata=rdata
            ))

        return records

    def _parse_name(self, data: bytes, offset: int) -> Tuple[str, int]:
        """도메인 이름 파싱 (압축 포인터 처리)"""
        labels = []
        original_offset = offset
        jumped = False

        while True:
            length = data[offset]

            if length == 0:
                offset += 1
                break
            elif (length & 0xC0) == 0xC0:
                # 압축 포인터
                if not jumped:
                    original_offset = offset + 2
                pointer = struct.unpack('!H', data[offset:offset+2])[0] & 0x3FFF
                offset = pointer
                jumped = True
            else:
                offset += 1
                labels.append(data[offset:offset+length].decode())
                offset += length

        return '.'.join(labels), original_offset if jumped else offset


# ============================================================
# HTTP/1.1 클라이언트 구현
# ============================================================

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


@dataclass
class HTTPRequest:
    """HTTP 요청"""
    method: HTTPMethod
    path: str
    host: str
    headers: Dict[str, str] = field(default_factory=dict)
    body: str = ""

    def __post_init__(self):
        self.headers.setdefault("Host", self.host)
        self.headers.setdefault("User-Agent", "SimpleHTTPClient/1.0")
        self.headers.setdefault("Connection", "close")
        if self.body:
            self.headers.setdefault("Content-Length", str(len(self.body)))

    def pack(self) -> bytes:
        """HTTP 요청을 바이트로 변환"""
        lines = [f"{self.method.value} {self.path} HTTP/1.1"]
        for key, value in self.headers.items():
            lines.append(f"{key}: {value}")
        lines.append("")
        if self.body:
            lines.append(self.body)
        else:
            lines.append("")
        return "\r\n".join(lines).encode()


@dataclass
class HTTPResponse:
    """HTTP 응답"""
    version: str
    status_code: int
    status_text: str
    headers: Dict[str, str] = field(default_factory=dict)
    body: str = ""

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 300


class HTTPClient:
    """간단한 HTTP 클라이언트"""

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout

    def request(self, url: str, method: HTTPMethod = HTTPMethod.GET,
                headers: Dict[str, str] = None, body: str = "") -> HTTPResponse:
        """HTTP 요청 수행"""
        # URL 파싱
        parsed = self._parse_url(url)
        host, port, path, use_https = parsed

        # TCP 연결
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)

        try:
            sock.connect((host, port))

            # HTTPS면 TLS 래핑 (실제로는 ssl.wrap_socket 사용)
            # 여기서는 HTTP만 구현

            # 요청 전송
            request = HTTPRequest(
                method=method,
                path=path,
                host=host,
                headers=headers or {},
                body=body
            )
            sock.sendall(request.pack())

            # 응답 수신
            response_data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response_data += chunk

            return self._parse_response(response_data)

        finally:
            sock.close()

    def _parse_url(self, url: str) -> Tuple[str, int, str, bool]:
        """URL 파싱 → (host, port, path, https)"""
        if url.startswith("https://"):
            use_https = True
            url = url[8:]
        elif url.startswith("http://"):
            use_https = False
            url = url[7:]
        else:
            use_https = False

        if "/" in url:
            host, path = url.split("/", 1)
            path = "/" + path
        else:
            host = url
            path = "/"

        if ":" in host:
            host, port_str = host.split(":")
            port = int(port_str)
        else:
            port = 443 if use_https else 80

        return host, port, path, use_https

    def _parse_response(self, data: bytes) -> HTTPResponse:
        """HTTP 응답 파싱"""
        text = data.decode('utf-8', errors='replace')
        lines = text.split('\r\n')

        # 상태 라인
        status_line = lines[0]
        parts = status_line.split(' ', 2)
        version = parts[0]
        status_code = int(parts[1])
        status_text = parts[2] if len(parts) > 2 else ""

        # 헤더
        headers = {}
        i = 1
        while i < len(lines) and lines[i]:
            key, value = lines[i].split(': ', 1)
            headers[key] = value
            i += 1

        # 본문
        body = '\r\n'.join(lines[i+1:]) if i + 1 < len(lines) else ""

        return HTTPResponse(
            version=version,
            status_code=status_code,
            status_text=status_text,
            headers=headers,
            body=body
        )

    def get(self, url: str, headers: Dict[str, str] = None) -> HTTPResponse:
        return self.request(url, HTTPMethod.GET, headers)

    def post(self, url: str, body: str = "",
             headers: Dict[str, str] = None) -> HTTPResponse:
        return self.request(url, HTTPMethod.POST, headers, body)


# ============================================================
# 쿠키/세션/JWT 관리자
# ============================================================

@dataclass
class Cookie:
    """HTTP 쿠키"""
    name: str
    value: str
    domain: str = ""
    path: str = "/"
    expires: Optional[str] = None
    max_age: Optional[int] = None
    secure: bool = False
    httponly: bool = False
    samesite: str = "Lax"  # Strict, Lax, None


class CookieJar:
    """쿠키 저장소"""

    def __init__(self):
        self.cookies: Dict[str, Cookie] = {}

    def set(self, cookie: Cookie) -> None:
        self.cookies[f"{cookie.domain}:{cookie.name}"] = cookie

    def get(self, domain: str, name: str) -> Optional[Cookie]:
        return self.cookies.get(f"{domain}:{name}")

    def get_for_request(self, domain: str, path: str = "/") -> str:
        """요청에 포함할 쿠키 헤더 생성"""
        valid_cookies = []
        for key, cookie in self.cookies.items():
            if domain in cookie.domain and path.startswith(cookie.path):
                valid_cookies.append(f"{cookie.name}={cookie.value}")
        return "; ".join(valid_cookies)


@dataclass
class JWTToken:
    """JWT 토큰 (시뮬레이션)"""
    header: Dict[str, str]
    payload: Dict[str, Any]
    signature: str = ""

    @property
    def is_expired(self) -> bool:
        if "exp" not in self.payload:
            return False
        return time.time() > self.payload["exp"]


# ============================================================
# DNS 캐시 시뮬레이터
# ============================================================

@dataclass
class DNSCacheEntry:
    """DNS 캐시 엔트리"""
    domain: str
    ip: str
    ttl: int
    cached_at: float

    @property
    def is_expired(self) -> bool:
        return time.time() > self.cached_at + self.ttl


class DNSCache:
    """DNS 캐시"""

    def __init__(self):
        self.cache: Dict[str, DNSCacheEntry] = {}
        self.hits = 0
        self.misses = 0

    def get(self, domain: str) -> Optional[str]:
        """캐시에서 IP 조회"""
        if domain in self.cache:
            entry = self.cache[domain]
            if not entry.is_expired:
                self.hits += 1
                return entry.ip
            else:
                del self.cache[domain]
        self.misses += 1
        return None

    def set(self, domain: str, ip: str, ttl: int = 300) -> None:
        """캐시에 저장"""
        self.cache[domain] = DNSCacheEntry(
            domain=domain,
            ip=ip,
            ttl=ttl,
            cached_at=time.time()
        )

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total * 100

    def print_stats(self) -> None:
        print(f"\nDNS 캐시 통계:")
        print(f"  히트: {self.hits}, 미스: {self.misses}")
        print(f"  히트율: {self.hit_rate:.1f}%")
        print(f"  캐시된 항목: {len(self.cache)}개")


# ============================================================
# 사용 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("         DNS & HTTP 프로토콜 데모")
    print("=" * 60)

    # 1. DNS 쿼리 테스트
    print("\n1. DNS 쿼리")
    print("-" * 40)

    dns_client = DNSClient("8.8.8.8")

    try:
        records = dns_client.query("google.com", DNSRecordType.A)
        print(f"google.com A 레코드:")
        for record in records:
            print(f"  → {record.rdata_str} (TTL: {record.ttl}s)")
    except Exception as e:
        print(f"  DNS 쿼리 실패: {e}")

    # 2. DNS 캐시 테스트
    print("\n2. DNS 캐시 시뮬레이션")
    print("-" * 40)

    cache = DNSCache()

    # 첫 번째 조회 (미스)
    ip = cache.get("example.com")
    if ip is None:
        print("  캐시 미스 → DNS 쿼리 수행")
        cache.set("example.com", "93.184.216.34", ttl=300)

    # 두 번째 조회 (히트)
    ip = cache.get("example.com")
    if ip:
        print(f"  캐시 히트 → {ip}")

    cache.print_stats()

    # 3. HTTP 요청 생성 테스트
    print("\n3. HTTP 요청 메시지 생성")
    print("-" * 40)

    request = HTTPRequest(
        method=HTTPMethod.GET,
        path="/api/users",
        host="api.example.com",
        headers={"Accept": "application/json", "Authorization": "Bearer token123"}
    )
    print(request.pack().decode())

    # 4. HTTP 응답 파싱 테스트
    print("\n4. HTTP 응답 파싱")
    print("-" * 40)

    sample_response = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 27\r\n\r\n{\"status\":\"success\",\"data\":[]}"

    client = HTTPClient()
    response = client._parse_response(sample_response)
    print(f"상태 코드: {response.status_code} {response.status_text}")
    print(f"헤더: {response.headers}")
    print(f"본문: {response.body}")

    # 5. 쿠키 관리
    print("\n5. 쿠키 관리")
    print("-" * 40)

    jar = CookieJar()
    jar.set(Cookie(name="session_id", value="abc123", domain="example.com"))
    jar.set(Cookie(name="user_pref", value="dark_mode", domain="example.com"))

    cookie_header = jar.get_for_request("example.com", "/")
    print(f"요청 쿠키 헤더: {cookie_header}")
