+++
title = "블록 스토리지 (Block Storage)"
date = 2026-03-05
description = "데이터를 고정 크기 블록 단위로 저장하고 VM에 직접 마운트하여 사용하는 고성능 스토리지 방식의 원리, 아키텍처 및 실무 적용"
weight = 76
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Block-Storage", "EBS", "SAN", "iSCSI", "Storage", "Cloud"]
+++

# 블록 스토리지 (Block Storage) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터를 고정된 크기의 블록(일반적으로 4KB~64KB)으로 분할하여 저장하고, 각 블록에 고유 주소를 할당하여 랜덤 액세스를 지원하는 스토리지 방식입니다. 운영체제는 이를 로컬 디스크처럼 인식합니다.
> 2. **가치**: **최저 지연 시간**(서브밀리초), **높은 IOPS**(수만~수십만), **일관된 성능**을 제공하여 RDBMS, NoSQL, VM 부팅 디스크 등 고성능 워크로드에 최적화되어 있습니다.
> 3. **융합**: SAN(Storage Area Network), iSCSI, NVMe-oF, AWS EBS, 클라우드 영구 볼륨(PV)과 결합하여 엔터프라이즈 및 클라우드 환경의 핵심 스토리지 계층을 구성합니다.

---

## Ⅰ. 개요 (Context & Background)

블록 스토리지(Block Storage)는 데이터를 파일이나 객체 같은 논리적 단위가 아닌, 원시 블록(Raw Block) 단위로 관리하는 스토리지 아키텍처입니다. 각 블록은 고유한 주소를 가지며, 운영체제는 이 주소를 사용하여 직접 데이터를 읽고 씁니다. 이는 파일 시스템을 구축할 수 있는 가장 기본적인 스토리지 형태입니다.

**💡 비유**: 블록 스토리지는 **'주차장의 개별 주차 공간'**과 같습니다. 주차장 전체가 하나의 커다란 공간이지만, 각 주차 공간(블록)에는 고유 번호(주소)가 있습니다. 어떤 차(데이터)가 어느 공간에 주차했는지 주차 관리 시스템(파일 시스템)이 기록합니다. 필요할 때 특정 번호의 공간으로 바로 찾아갈 수 있죠.

**등장 배경 및 발전 과정**:
1. **직접 연결 스토리지 (DAS, 1960~1990)**: 서버 내부에 장착된 하드디스크가 유일한 스토리지였습니다. 확장성과 공유가 불가능했습니다.
2. **SAN의 등장 (1990~)**: 파이버 채널(Fibre Channel) 네트워크로 스토리지를 서버와 분리하여, 여러 서버가 공유하고 확장 가능한 블록 스토리지 풀을 구축했습니다.
3. **iSCSI 표준화 (2003)**: IP 네트워크를 통해 블록 스토리지에 접근하는 표준이 만들어져 SAN 구축 비용이 절감되었습니다.
4. **클라우드 블록 스토리지 (2006~)**: AWS EBS(Elastic Block Store)가 등장하여 클라우드 VM에 탄력적인 블록 스토리지를 제공했습니다.
5. **NVMe 및 NVMe-oF (2016~)**: SSD와 초고속 네트워크를 결합하여 마이크로초 단위 지연 시간을 달성했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 및 특성

| 구성 요소 | 상세 역할 | 기술/프로토콜 | 비고 |
|---|---|---|---|
| **블록 (Block)** | 데이터 저장의 최소 단위 | 4KB~64KB | 섹터/페이지 |
| **LUN (Logical Unit Number)** | 스토리지 논리 볼륨 식별자 | SCSI 표준 | 마운트 대상 |
| **HBA/Initiator** | 서버 측 스토리지 인터페이스 | FC HBA, iSCSI SW | 연결 주체 |
| **스토리지 컨트롤러** | 블록 할당, 캐싱, 중복 제거 | RAID, Cache | 지능형 관리 |
| **백엔드 미디어** | 실제 데이터 저장 매체 | HDD, SSD, NVMe | 성능 결정 |
| **인터커넥트** | 서버-스토리지 연결 네트워크 | FC, iSCSI, NVMe-oF | 대역폭/지연 결정 |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Block Storage Architecture ]                            │
└─────────────────────────────────────────────────────────────────────────────┘

[ 전통적 SAN 아키텍처 ]

    ┌─────────────────────────────────────────────────────────────────────┐
    │                         Application Servers                          │
    │  ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐     │
    │  │  Server A │   │  Server B │   │  Server C │   │  Server D │     │
    │  │  + OS     │   │  + OS     │   │  + OS     │   │  + OS     │     │
    │  │  + FS     │   │  + FS     │   │  + FS     │   │  + FS     │     │
    │  └─────┬─────┘   └─────┬─────┘   └─────┬─────┘   └─────┬─────┘     │
    │        │               │               │               │            │
    │  ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐     │
    │  │  HBA/     │   │  HBA/     │   │  HBA/     │   │  HBA/     │     │
    │  │  Initiator│   │  Initiator│   │  Initiator│   │  Initiator│     │
    │  └─────┬─────┘   └─────┬─────┘   └─────┬─────┘   └─────┬─────┘     │
    └────────┼───────────────┼───────────────┼───────────────┼────────────┘
             │               │               │               │
             └───────────────┴───────┬───────┴───────────────┘
                                     │
                        ┌────────────▼────────────┐
                        │   SAN Fabric (FC Switch)│
                        │   Zoning / VSAN         │
                        └────────────┬────────────┘
                                     │
             ┌───────────────────────┴───────────────────────┐
             │                                               │
    ┌────────▼────────┐                           ┌─────────▼────────┐
    │  Storage Array  │                           │  Storage Array   │
    │  ┌───────────┐  │                           │  ┌───────────┐   │
    │  │Controller │  │                           │  │Controller │   │
    │  │ - RAID    │  │                           │  │ - RAID    │   │
    │  │ - Cache   │  │                           │  │ - Cache   │   │
    │  │ - Dedupe  │  │                           │  │ - Dedupe  │   │
    │  └─────┬─────┘  │                           │  └─────┬─────┘   │
    │        │        │                           │        │         │
    │  ┌─────▼─────┐  │                           │  ┌─────▼─────┐   │
    │  │ LUN Pool  │  │                           │  │ LUN Pool  │   │
    │  │[LUN1][LUN2]│ │                           │  │[LUN3][LUN4]│  │
    │  └─────┬─────┘  │                           │  └─────┬─────┘   │
    │        │        │                           │        │         │
    │  ┌─────▼─────┐  │                           │  ┌─────▼─────┐   │
    │  │ SSD/HDD   │  │                           │  │ SSD/HDD   │   │
    │  │ Drives    │  │                           │  │ Drives    │   │
    │  └───────────┘  │                           │  └───────────┘   │
    └─────────────────┘                           └──────────────────┘


[ 클라우드 블록 스토리지 (AWS EBS) 아키텍처 ]

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                            AWS Region                                    │
    │  ┌───────────────────────────────────────────────────────────────────┐  │
    │  │                         Availability Zone (AZ)                     │  │
    │  │                                                                    │  │
    │  │  ┌───────────────┐         ┌─────────────────────────────────┐   │  │
    │  │  │   EC2 Instance│         │      EBS (Elastic Block Store)   │   │  │
    │  │  │  ┌─────────┐  │         │                                  │   │  │
    │  │  │  │   OS    │  │  NVMe   │  ┌─────────┐  ┌─────────────────┐│   │  │
    │  │  │  │ + FS    │◄─┼─────────┼─►│ Volume  │  │  EBS Backend    ││   │  │
    │  │  │  │ /dev/nvme│ │  over   │  │ (gp3)   │  │  ┌───────────┐  ││   │  │
    │  │  │  └─────────┘  │  Network│  │ 100GB   │  │  │ SSD Cache │  ││   │  │
    │  │  │               │         │  │         │  │  └─────┬─────┘  ││   │  │
    │  │  │  ┌─────────┐  │         │  └─────────┘  │        │        ││   │  │
    │  │  │  │ App     │  │         │               │  ┌─────▼─────┐  ││   │  │
    │  │  │  │ Data    │  │         │               │  │  S3 Back  │  ││   │  │
    │  │  │  └─────────┘  │         │               │  │  (Snapshots)│ │   │  │
    │  │  └───────────────┘         │               │  └───────────┘  ││   │  │
    │  │                            │               └─────────────────┘│   │  │
    │  │                            └─────────────────────────────────┘   │  │
    │  │                                                                    │  │
    │  │  특징:                                                              │  │
    │  │  - AZ 내부에서만 연결 가능 (다중 AZ 미지원)                          │  │
    │  │  - 단일 EC2에만 마운트 가능 (Multi-Attach 제한적 지원)               │  │
    │  │  - 스냅샷은 S3에 저장 (증분 백업)                                    │  │
    │  │  - Provisioned IOPS로 성능 보장 가능                                │  │
    │  │                                                                    │  │
    │  └───────────────────────────────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: 블록 I/O 처리 과정

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    Block I/O Processing Pipeline                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ 쓰기 요청 (Write Request) ]                                              │
│                                                                            │
│  ① Application                                                             │
│     │  write(fd, buffer, size)                                             │
│     ▼                                                                      │
│  ② File System (ext4, xfs, NTFS)                                          │
│     │  - 파일 오프셋 → 블록 번호 변환                                        │
│     │  - 버퍼 캐시 확인 (Page Cache)                                        │
│     │  - 지연 쓰기 (Write-back) 또는 즉시 쓰기                              │
│     ▼                                                                      │
│  ③ Block Layer (Linux Kernel)                                             │
│     │  - I/O 스케줄러 (mq-deadline, bfq, none)                             │
│     │  - 요청 병합 (Request Merging)                                        │
│     │  - I/O 우선순위 관리                                                  │
│     ▼                                                                      │
│  ④ Device Driver (SCSI/NVMe)                                              │
│     │  - SCSI 명령 / NVMe 명령 생성                                        │
│     │  - CDB (Command Descriptor Block) 구성                               │
│     ▼                                                                      │
│  ⑤ Network Transport (iSCSI/NVMe-oF)                                      │
│     │  - 패킷 캡슐화                                                        │
│     │  - TCP/IP 또는 RDMA 전송                                             │
│     ▼                                                                      │
│  ⑥ Storage Controller                                                     │
│     │  - Write Cache 수신 (DRAM)                                           │
│     │  - Ack 응답 (Write-back) 또는 대기 (Write-through)                   │
│     │  - RAID 패리티 계산                                                   │
│     │  - 백엔드 디스크 분산 기록                                            │
│     ▼                                                                      │
│  ⑦ Physical Media (SSD/HDD)                                               │
│     │  - 플래시 페이지 프로그램 / 섹터 기록                                  │
│     ▼                                                                      │
│  ⑧ Completion                                                             │
│     - 완료 응답 → 상위 계층으로 전파                                        │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 알고리즘: I/O 스케줄링

```python
"""
블록 I/O 스케줄러 시뮬레이션
Linux Kernel의 mq-deadline 스케줄러 개념적 구현
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
import heapq
import time

class IOType(Enum):
    READ = "read"
    WRITE = "write"

@dataclass(order=True)
class IORequest:
    """블록 I/O 요청"""
    sector: int              # 시작 섹터 번호
    size: int                # 요청 크기 (섹터 수)
    io_type: IOType = field(compare=False)
    submit_time: float = field(compare=False)
    deadline: float = field(compare=False)

    # 정렬을 위한 필드
    sort_key: int = field(init=False, compare=True)

    def __post_init__(self):
        # 읽기 요청을 쓰기보다 우선 (높은 우선순위)
        priority = 0 if self.io_type == IOType.READ else 1
        self.sort_key = (priority, self.sector)


class DeadlineScheduler:
    """
    mq-deadline I/O 스케줄러

    특징:
    - 읽기/쓰기 별 별도 큐 관리
    - 데드라인 기반 요청 선택
    - 순차 I/O 병합 최적화
    - 기아(Starvation) 방지
    """

    def __init__(
        self,
        read_expire: float = 0.5,    # 읽기 데드라인 (초)
        write_expire: float = 5.0,    # 쓰기 데드라인 (초)
        writes_starved: int = 2       # 쓰기 기아 허용 한도
    ):
        self.read_expire = read_expire
        self.write_expire = write_expire
        self.writes_starved = writes_starved

        # 섹터 순 정렬 큐 (엘리베이터 알고리즘)
        self.read_queue: List[IORequest] = []
        self.write_queue: List[IORequest] = []

        # 데드라인 큐
        self.read_deadline_queue: List[IORequest] = []
        self.write_deadline_queue: List[IORequest] = []

        self.write_starvation_counter = 0
        self.current_sector = 0

    def submit_request(self, io_type: IOType, sector: int, size: int):
        """I/O 요청 제출"""
        now = time.time()
        deadline = now + (
            self.read_expire if io_type == IOType.READ
            else self.write_expire
        )

        request = IORequest(
            sector=sector,
            size=size,
            io_type=io_type,
            submit_time=now,
            deadline=deadline
        )

        # 섹터 순 큐에 추가
        if io_type == IOType.READ:
            heapq.heappush(self.read_queue, request)
            heapq.heappush(self.read_deadline_queue,
                          (deadline, request))
        else:
            heapq.heappush(self.write_queue, request)
            heapq.heappush(self.write_deadline_queue,
                          (deadline, request))

    def dispatch_next(self) -> Optional[IORequest]:
        """다음 처리할 요청 선택"""
        now = time.time()

        # 1. 데드라인 만료 요청 확인
        expired_read = self._check_expired(IOType.READ, now)
        expired_write = self._check_expired(IOType.WRITE, now)

        if expired_read:
            return self._pop_from_queue(IOType.READ)

        # 2. 읽기 우선 처리 (쓰기 기아 카운터 체크)
        if self.read_queue and self.write_starvation_counter < self.writes_starved:
            return self._pop_from_queue(IOType.READ)

        # 3. 쓰기 처리
        if self.write_queue:
            self.write_starvation_counter = 0
            return self._pop_from_queue(IOType.WRITE)

        # 4. 남은 읽기 처리
        if self.read_queue:
            return self._pop_from_queue(IOType.READ)

        return None

    def _check_expired(self, io_type: IOType, now: float) -> bool:
        """데드라인 만료 요청 확인"""
        deadline_queue = (
            self.read_deadline_queue if io_type == IOType.READ
            else self.write_deadline_queue
        )
        if deadline_queue and deadline_queue[0][0] < now:
            return True
        return False

    def _pop_from_queue(self, io_type: IOType) -> Optional[IORequest]:
        """큐에서 요청 꺼내기"""
        queue = (
            self.read_queue if io_type == IOType.READ
            else self.write_queue
        )
        if queue:
            request = heapq.heappop(queue)
            self.current_sector = request.sector + request.size

            # 데드라인 큐에서도 제거
            deadline_queue = (
                self.read_deadline_queue if io_type == IOType.READ
                else self.write_deadline_queue
            )
            deadline_queue[:] = [
                (d, r) for d, r in deadline_queue
                if r != request
            ]
            heapq.heapify(deadline_queue)

            if io_type == IOType.WRITE:
                self.write_starvation_counter += 1

            return request
        return None

    def merge_requests(self) -> int:
        """인접 요청 병합"""
        merged = 0
        for queue in [self.read_queue, self.write_queue]:
            if len(queue) < 2:
                continue

            # 섹터 순 정렬
            queue.sort(key=lambda r: r.sector)

            new_queue = []
            prev = None

            for req in queue:
                if prev and prev.sector + prev.size == req.sector:
                    # 병합 가능
                    prev.size += req.size
                    merged += 1
                else:
                    if prev:
                        new_queue.append(prev)
                    prev = req

            if prev:
                new_queue.append(prev)

            queue.clear()
            for req in new_queue:
                heapq.heappush(queue, req)

        return merged


# 사용 예시
if __name__ == "__main__":
    scheduler = DeadlineScheduler()

    # 랜덤 I/O 패턴 시뮬레이션
    requests = [
        (IOType.READ, 1000, 8),
        (IOType.WRITE, 2000, 16),
        (IOType.READ, 1008, 8),   # 병합 가능
        (IOType.WRITE, 500, 8),
        (IOType.READ, 3000, 8),
    ]

    for io_type, sector, size in requests:
        scheduler.submit_request(io_type, sector, size)

    # 요청 병합
    merged = scheduler.merge_requests()
    print(f"Merged requests: {merged}")

    # 요청 처리
    while True:
        req = scheduler.dispatch_next()
        if req is None:
            break
        print(f"Processing: {req.io_type.value} @ sector {req.sector}, "
              f"size {req.size}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 스토리지 유형별 특성

| 비교 관점 | 블록 스토리지 | 파일 스토리지 | 오브젝트 스토리지 |
|---|---|---|---|
| **저장 단위** | 고정 크기 블록 | 파일 + 메타데이터 | 객체 (데이터+메타) |
| **액세스 방식** | LBA (직접 주소) | 경로 기반 | REST API (키) |
| **프로토콜** | SCSI, NVMe, iSCSI | NFS, SMB, CIFS | S3 API, HTTP |
| **성능** | 최고 (서브ms) | 높음 (ms) | 중간 (10~100ms) |
| **확장성** | 제한적 | 중간 | 무제한 |
| **공유** | 제한적 (클러스터 FS) | 용이 | 용이 |
| **비용** | 높음 | 중간 | 낮음 |
| **적합 워크로드** | DB, VM, 고성능 | 파일 공유, NAS | 백업, 아카이브, 정적 콘텐츠 |

### 블록 스토리지 성능 지표

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ Block Storage Performance Metrics ]                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [ IOPS (Input/Output Operations Per Second) ]                               │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 스토리지 유형          │ 4KB Random Read │ 4KB Random Write │ 16KB Mix  ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ HDD (7.2K RPM)        │ 80-100          │ 80-100            │ 60-80     ││
│  │ HDD (15K RPM)         │ 180-210         │ 180-210           │ 150-180   ││
│  │ SATA SSD              │ 80,000-100,000  │ 50,000-80,000     │ 60,000    ││
│  │ NVMe SSD              │ 500,000-1M+     │ 300,000-500,000   │ 400,000   ││
│  │ AWS EBS gp3 (기본)    │ 3,000           │ 3,000             │ 3,000     ││
│  │ AWS EBS gp3 (최대)    │ 16,000          │ 16,000            │ 16,000    ││
│  │ AWS EBS io2 (최대)    │ 64,000          │ 64,000            │ 64,000    ││
│  │ AWS EBS io2 Block Exp │ 256,000         │ 256,000           │ 256,000   ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  [ 지연 시간 (Latency) ]                                                      │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 스토리지 유형          │ 평균 지연        │ P99 지연          │ P99.9    ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ HDD                    │ 5-10 ms         │ 15-20 ms          │ 50+ ms   ││
│  │ SATA SSD               │ 0.1-0.5 ms      │ 1-2 ms            │ 5-10 ms  ││
│  │ NVMe SSD (Local)       │ 0.01-0.05 ms    │ 0.1-0.2 ms        │ 0.5-1 ms ││
│  │ AWS EBS gp3            │ 0.5-1 ms        │ 2-5 ms            │ 10-20 ms ││
│  │ AWS EBS io2            │ 0.1-0.3 ms      │ 0.5-1 ms          │ 2-5 ms   ││
│  │ iSCSI over 10GbE       │ 0.3-0.8 ms      │ 1-3 ms            │ 5-10 ms  ││
│  │ NVMe-oF over RDMA      │ 0.02-0.05 ms    │ 0.1-0.2 ms        │ 0.5-1 ms ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  [ 처리량 (Throughput) ]                                                     │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 스토리지 유형          │ 순차 읽기        │ 순차 쓰기          │ 비고     ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ HDD (SATA 7.2K)        │ 150-200 MB/s    │ 150-200 MB/s      │          ││
│  │ SATA SSD               │ 500-550 MB/s    │ 500-550 MB/s      │ SATA3 한 ││
│  │ NVMe SSD (PCIe 4.0)    │ 7,000 MB/s      │ 5,000 MB/s        │ x4 레인  ││
│  │ AWS EBS gp3 (기본)     │ 125 MB/s        │ 125 MB/s          │          ││
│  │ AWS EBS gp3 (최대)     │ 1,000 MB/s      │ 1,000 MB/s        │ 별도 구매 ││
│  │ AWS EBS io2 (최대)     │ 1,000 MB/s      │ 1,000 MB/s        │          ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 과목 융합 관점 분석

**운영체제(OS)와의 융합**:
- **페이지 캐시**: Linux의 Page Cache가 블록 디바이스 I/O를 가속화
- **I/O 스케줄러**: CFQ, deadline, noop, bfq 등 스케줄러가 성능 결정
- **LVM (Logical Volume Manager)**: 물리 블록 장치를 논리 볼륨으로 추상화

**데이터베이스와의 융합**:
- **버퍼 풀**: MySQL InnoDB Buffer Pool, PostgreSQL Shared Buffers
- **REDO/UNDO 로그**: 블록 장치에 순차 기록되는 WAL (Write-Ahead Log)
- **테이블스페이스**: 블록 장치 위에 구축되는 DB 저장소 구조

**네트워크와의 융합**:
- **iSCSI**: TCP/IP를 통한 블록 전송, 패킷 오버헤드
- **NVMe-oF**: RDMA를 통한 초저지연 블록 액세스
- **Jumbo Frame**: 9000바이트 MTU로 iSCSI 효율 향상

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 데이터베이스 스토리지 선택

**문제 상황**: 고성능 OLTP 데이터베이스를 위한 스토리지 선택

**기술사의 의사결정 프로세스**:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ DB 스토리지 선택 의사결정 ]                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. 워크로드 분석                                                             │
│     ├── 트랜잭션 유형: OLTP (랜덤 I/O 중심)                                   │
│     ├── 일일 트랜잭션: 1억 건                                                 │
│     ├── 평균 쿼리 지연 요구: < 10ms                                          │
│     └── 데이터 크기: 5TB                                                     │
│                                                                              │
│  2. 성능 요구사항 계산                                                        │
│     ├── TPS (초당 트랜잭션): 1억 / 86400 = 1,158 TPS                         │
│     ├── 트랜잭션당 I/O: 약 10개 (인덱스, 데이터, 로그)                         │
│     ├── 필요 IOPS: 1,158 × 10 = 11,580 IOPS                                 │
│     ├── 여유윤 (50%): 17,370 IOPS                                            │
│     └── 권장: 20,000 IOPS 이상                                               │
│                                                                              │
│  3. 스토리지 옵션 평가                                                        │
│     ├── AWS EBS gp3 (16,000 IOPS): 부족                                      │
│     ├── AWS EBS io2 (64,000 IOPS): 적합                                      │
│     ├── AWS EBS io2 Block Express: 과잉                                      │
│     └── 로컬 NVMe 인스턴스 스토어: 고려 (단, 휘발성)                           │
│                                                                              │
│  4. 최종 아키텍처                                                             │
│     ├── Primary: io2 500GB × 4 (RAID 10) = 2TB                              │
│     ├── IOPS: 16,000 × 4 = 64,000 IOPS                                      │
│     ├── 처리량: 1,000 MB/s × 4 = 4,000 MB/s                                 │
│     ├── 월 비용: $0.125/GB + $0.065/IOPS × 16,000 ≈ $2,000/월               │
│     └── 백업: 스냅샷 → S3 (증분)                                             │
│                                                                              │
│  5. 고가용성 구성                                                             │
│     ├── Multi-AZ RDS: 동기 복제                                              │
│     ├── 또는 Read Replica: 비동기 복제                                       │
│     └── 장애 조치 시간: 60~120초                                             │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 도입 시 고려사항 체크리스트

| 항목 | 확인 사항 | 비고 |
|---|---|---|
| **성능** | IOPS, 지연 시간, 처리량 요구사항 명확화 | 워크로드 프로파일링 필수 |
| **용량** | 현재 + 성장률 고려 | 30% 여유 권장 |
| **가용성** | RAID 레벨, 복제, 백업 전략 | RPO/RTO 정의 |
| **비용** | 프로비저닝된 IOPS 비용 | gp3 vs io2 비교 |
| **확장성** | 온라인 확장 가능 여부 | EBS Elastic Volumes |
| **보안** | 암호화 (at-rest, in-transit) | KMS 키 관리 |

### 안티패턴 및 주의사항

**안티패턴 1: 오버프로비저닝**
- 문제: 필요 이상의 IOPS 프로비저닝으로 비용 낭비
- 해결: 실제 워크로드 기반 적정 크기 산정

**안티패턴 2: 스냅샷만으로 백업**
- 문제: 스냅샷은 앱 일관성 보장 안 함
- 해결: 앱 정지 또는 freeze 후 스냅샷

**안티패턴 3: 단일 AZ 의존**
- 문제: AZ 장애 시 서비스 중단
- 해결: Multi-AZ 복제 또는 정기 교차 AZ 복원 테스트

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 레거시 HDD | SATA SSD | NVMe/Cloud Block |
|---|---|---|---|
| **IOPS** | 100-200 | 80,000+ | 256,000+ |
| **지연 시간** | 5-10ms | 0.1-0.5ms | 0.01-0.1ms |
| **비용/GB** | $0.05 | $0.10 | $0.08-0.125 |
| **DB 성능** | 기준 | 10-50x | 50-100x |

### 미래 전망 및 진화 방향

1. **NVMe-oF의 보편화**: RDMA 네트워크를 통한 원격 NVMe 액세스 표준화
2. **Computational Storage**: 스토리지 내부에서 연산 수행 (Smart SSD)
3. **ZNS (Zoned Namespace)**: SSD 수명 및 성능 최적화를 위한 새로운 인터페이스
4. **QLC/PLC SSD**: 비용 절감을 위한 고밀도 플래시 채택 증가

### ※ 참고 표준/가이드
- **SCSI Primary Commands (SPC)**: 블록 디바이스 명령 표준
- **NVMe Specification**: NVM Express 표준
- **iSCSI RFC 3720**: IP 기반 스토리지 표준
- **AWS EBS Documentation**: 클라우드 블록 스토리지 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [파일 스토리지 (File Storage)](@/studynotes/13_cloud_architecture/03_virt/file_storage.md) : 파일 단위 액세스
- [오브젝트 스토리지 (Object Storage)](@/studynotes/13_cloud_architecture/03_virt/object_storage.md) : 무제한 확장 스토리지
- [SDS (Software Defined Storage)](@/studynotes/13_cloud_architecture/03_virt/sds.md) : 소프트웨어 정의 스토리지
- [가상화 (Virtualization)](@/studynotes/13_cloud_architecture/03_virt/virtualization.md) : VM 스토리지 연결
- [쿠버네티스 PV/PVC](@/studynotes/13_cloud_architecture/01_native/kubernetes.md) : 컨테이너 영구 볼륨

---

### 👶 어린이를 위한 3줄 비유 설명
1. 블록 스토리지는 **'주차장의 각 주차 공간'**과 같아요. 큰 주차장이 작은 칸들로 나뉘어 있고, 각 칸에는 번호(주소)가 있어요.
2. **'원하는 칸으로 바로 찾아갈 수 있어요'**. 100번 칸에 있는 차를 찾으려면 1번부터 순서대로 안 보고 바로 100번으로 가면 돼요.
3. 컴퓨터에서는 **'데이터를 조각조각 나누어 저장'**하고, 필요할 때 번호로 빠르게 찾아요. 그래서 게임이나 데이터베이스가 빠르게 작동할 수 있어요!
