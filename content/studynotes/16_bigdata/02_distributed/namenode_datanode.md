+++
title = "NameNode와 DataNode"
categories = ["studynotes-16_bigdata"]
+++

# NameNode와 DataNode

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NameNode는 HDFS의 마스터 노드로 메타데이터를 관리하고, DataNode는 슬레이브 노드로 실제 데이터 블록을 저장한다.
> 2. **가치**: 마스터-슬레이브 구조는 분산 시스템의 확장성과 내결함성을 동시에 확보하는 핵심 아키텍처 패턴이다.
> 3. **융합**: HA(High Availability) 구성, Federation, Rack Awareness와 결합하여 엔터프라이즈급 안정성을 제공한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

**NameNode**는 HDFS 클러스터의 중앙 관리자로, 파일 시스템 트리, 블록 위치 정보, 접근 제어 정보 등 모든 메타데이터를 관리한다. **DataNode**는 실제 데이터 블록을 저장하고, NameNode에 주기적으로 하트비트와 블록 리포트를 전송한다.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    NameNode vs DataNode 비교                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  NameNode (마스터)                                               │   │
│  │  ┌─────────────────────────────────────────────────────────────┐│   │
│  │  │  역할: 메타데이터 관리, 리소스 조정                          ││   │
│  │  │  저장: RAM (In-Memory)                                      ││   │
│  │  │  데이터: FsImage + EditLog                                   ││   │
│  │  │  개수: 1개 (HA: 2개)                                         ││   │
│  │  │  SPOF: 있음 (HA로 해결)                                      ││   │
│  │  └─────────────────────────────────────────────────────────────┘│   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                        │
│                              │ RPC 통신                               │
│                              │                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  DataNode (슬레이브)                                             │   │
│  │  ┌─────────────────────────────────────────────────────────────┐│   │
│  │  │  역할: 블록 저장, 읽기/쓰기 처리                              ││   │
│  │  │  저장: 로컬 디스크                                           ││   │
│  │  │  통신: 하트비트 (3초), 블록 리포트 (1시간)                    ││   │
│  │  │  개수: 수백~수천 개                                          ││   │
│  │  │  장애: 자동 복구 (복제본 활용)                                ││   │
│  │  └─────────────────────────────────────────────────────────────┘│   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  상세 비교표                                                     │    │
│  ├───────────────────┬─────────────────┬────────────────────────┤    │
│  │  구분             │ NameNode        │ DataNode               │    │
│  ├───────────────────┼─────────────────┼────────────────────────┤    │
│  │  역할             │ 마스터          │ 슬레이브               │    │
│  │  데이터 위치      │ 메모리          │ 디스크                 │    │
│  │  파일 데이터      │ 없음            │ 있음 (블록)            │    │
│  │  메타데이터       │ 있음            │ 없음                   │    │
│  │  장애 영향        │ 클러스터 전체   │ 해당 노드만            │    │
│  │  하드웨어 요구    │ 고사양 (RAM)    │ 대용량 디스크          │    │
│  │  복구             │ 수동/HA         │ 자동                   │    │
│  └───────────────────┴─────────────────┴────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 💡 비유

NameNode는 "도서관 사서"에 비유할 수 있다. 사서는 어떤 책이 어디 있는지 알고(메타데이터), 책을 직접 들고 있지는 않는다. DataNode는 "서가"다. 실제 책(데이터 블록)이 저장되어 있다. 사서가 없으면 책을 찾을 수 없지만, 서가 하나가 무너져도 다른 서가에 복제본이 있다.

### 등장 배경

1. **GFS 설계 원칙**: Google File System의 마스터-청크서버 구조 차용
2. **단순성**: 중앙 집중식 메타데이터 관리로 일관성 보장
3. **확장성**: DataNode만 추가하여 스토리지 용량 선형 확장

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### NameNode 내부 구조

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    NameNode 내부 구조                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  RAM (In-Memory 메타데이터)                                     │   │
│  │  ┌─────────────────────────────────────────────────────────────┐│   │
│  │  │  FsImage (파일 시스템 이미지)                               ││   │
│  │  │  - 파일/디렉토리 트리 구조                                  ││   │
│  │  │  - 각 파일의 블록 목록                                      ││   │
│  │  │  - 복제 계수, 권한 정보                                     ││   │
│  │  └─────────────────────────────────────────────────────────────┘│   │
│  │  ┌─────────────────────────────────────────────────────────────┐│   │
│  │  │  EditLog (편집 로그)                                        ││   │
│  │  │  - 파일 생성/삭제/수정 기록                                 ││   │
│  │  │  - 순차적 쓰기 (append-only)                                ││   │
│  │  └─────────────────────────────────────────────────────────────┘│   │
│  │  ┌─────────────────────────────────────────────────────────────┐│   │
│  │  │  BlockMap (블록 매핑)                                       ││   │
│  │  │  - 블록 ID → DataNode 목록                                  ││   │
│  │  │  - 메모리 내 빠른 조회                                      ││   │
│  │  └─────────────────────────────────────────────────────────────┘│   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                        │
│         ┌────────────────────┼────────────────────┐                   │
│         │                    │                    │                    │
│         ▼                    ▼                    ▼                    │
│  ┌─────────────┐    ┌─────────────────┐    ┌─────────────┐           │
│  │ 로컬 디스크  │    │ JournalNode    │    │ Secondary   │           │
│  │ (영속화)    │    │ (HA용)         │    │ NameNode    │           │
│  │             │    │                │    │ (체크포인트)│           │
│  │ fsimage     │    │ edits 공유     │    │             │           │
│  │ edits       │    │                │    │             │           │
│  └─────────────┘    └─────────────────┘    └─────────────┘           │
│                                                                         │
│  ──────────────────────────────────────────────────────────────────── │
│                                                                         │
│  메모리 요구사항 계산:                                                  │
│  - 파일 1개당 약 150바이트                                              │
│  - 블록 1개당 약 150바이트                                              │
│  - 1억 개 파일 = 약 30GB RAM 필요                                       │
│  - 권장: 파일 수 × 300바이트                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### NameNode HA (High Availability) 구성

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    NameNode HA 구성                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Active NameNode                                                 │   │
│  │  - 현재 서비스 중                                                 │   │
│  │  - 쓰기 요청 처리                                                 │   │
│  │  - EditLog 기록                                                   │   │
│  └───────────────────────────┬─────────────────────────────────────┘   │
│                              │                                        │
│                              │ JournalNode Quorum                     │
│                              │ (EditLog 동기화)                        │
│                              │                                        │
│  ┌───────────────────────────┴─────────────────────────────────────┐   │
│  │  Standby NameNode                                                │   │
│  │  - 대기 상태                                                      │   │
│  │  - EditLog 읽기                                                   │   │
│  │  - Active 장애 시 승격                                            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                        │
│                              │ ZooKeeper                              │
│                              │ (리더 선출)                            │
│                              │                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  ZKFailoverController (ZKFC)                                     │   │
│  │  - 각 NameNode에서 실행                                          │   │
│  │  - 건강 상태 모니터링                                             │   │
│  │  - 자동 페일오버 트리거                                           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  장애 조치 시나리오:                                                    │
│  1. Active NameNode 장애 감지                                          │
│  2. ZKFC이 ZooKeeper에 알림                                            │
│  3. Standby가 Active로 승격                                            │
│  4. 클라이언트가 새 Active로 리다이렉트                                │
│  5. 복구 시간: 30초~2분                                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### DataNode 내부 구조

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
import time
import threading

class BlockState(Enum):
    FINALIZED = "FINALIZED"      # 완료된 블록
    UNDER_CONSTRUCTION = "UC"    # 쓰기 진행 중
    RECOVERING = "RECOVERING"    # 복구 중

@dataclass
class Block:
    """HDFS 블록 정의"""
    block_id: int
    block_pool_id: str
    generation_stamp: int
    size: int  # 바이트
    state: BlockState
    file_path: str

@dataclass
class DataNodeInfo:
    """DataNode 정보"""
    datanode_id: str
    hostname: str
    port: int
    ipc_port: int
    capacity: int      # 총 용량
    dfs_used: int      # 사용 중
    remaining: int     # 남은 용량
    block_pool_used: int
    cache_capacity: int
    cache_used: int
    last_update: int   # 마지막 하트비트
    xferaddr: str      # 데이터 전송 주소
    rack_location: str # 랙 위치

class DataNodeSimulator:
    """DataNode 동작 시뮬레이터"""

    HEARTBEAT_INTERVAL = 3  # 초
    BLOCK_REPORT_INTERVAL = 3600  # 1시간

    def __init__(self, datanode_id: str, namenode_rpc: str):
        self.datanode_id = datanode_id
        self.namenode_rpc = namenode_rpc
        self.blocks: Dict[int, Block] = {}
        self.info = DataNodeInfo(
            datanode_id=datanode_id,
            hostname="localhost",
            port=9866,
            ipc_port=9867,
            capacity=10 * 1024 * 1024 * 1024 * 1024,  # 10TB
            dfs_used=0,
            remaining=10 * 1024 * 1024 * 1024 * 1024,
            block_pool_used=0,
            cache_capacity=100 * 1024 * 1024 * 1024,  # 100GB
            cache_used=0,
            last_update=int(time.time()),
            xferaddr="localhost:9866",
            rack_location="/default-rack"
        )
        self.running = False

    def start(self):
        """DataNode 시작"""
        self.running = True
        # 하트비트 스레드
        heartbeat_thread = threading.Thread(target=self._send_heartbeat_loop)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()
        # 블록 리포트 스레드
        report_thread = threading.Thread(target=self._send_block_report_loop)
        report_thread.daemon = True
        report_thread.start()

    def stop(self):
        """DataNode 정지"""
        self.running = False

    def _send_heartbeat_loop(self):
        """하트비트 전송 루프"""
        while self.running:
            self._send_heartbeat()
            time.sleep(self.HEARTBEAT_INTERVAL)

    def _send_heartbeat(self):
        """NameNode에 하트비트 전송"""
        self.info.last_update = int(time.time())

        heartbeat_data = {
            "datanode_id": self.datanode_id,
            "capacity": self.info.capacity,
            "dfs_used": self.info.dfs_used,
            "remaining": self.info.remaining,
            "block_pool_used": self.info.block_pool_used,
            "cache_capacity": self.info.cache_capacity,
            "cache_used": self.info.cache_used,
            "xferaddr": self.info.xferaddr,
            "num_blocks": len(self.blocks)
        }

        # 실제로는 RPC 호출
        print(f"[{datetime.now()}] Heartbeat sent: {heartbeat_data}")

        # NameNode로부터 받은 명령 처리
        commands = self._receive_commands()
        for cmd in commands:
            self._execute_command(cmd)

    def _send_block_report_loop(self):
        """블록 리포트 전송 루프"""
        while self.running:
            self._send_block_report()
            time.sleep(self.BLOCK_REPORT_INTERVAL)

    def _send_block_report(self):
        """전체 블록 리포트 전송"""
        block_report = {
            "datanode_id": self.datanode_id,
            "blocks": [
                {
                    "block_id": block.block_id,
                    "generation_stamp": block.generation_stamp,
                    "size": block.size
                }
                for block in self.blocks.values()
            ]
        }
        print(f"[{datetime.now()}] Block report: {len(self.blocks)} blocks")

    def _receive_commands(self) -> List[Dict]:
        """NameNode로부터 명령 수신"""
        # 실제로는 RPC 응답에서 추출
        return []

    def _execute_command(self, command: Dict):
        """NameNode 명령 실행"""
        cmd_type = command.get("type")

        if cmd_type == "DNA_TRANSFER":
            # 블록 전송 (리밸런싱)
            self._transfer_block(command["block_id"], command["target"])
        elif cmd_type == "DNA_INVALIDATE":
            # 블록 삭제
            self._delete_block(command["block_id"])
        elif cmd_type == "DNA_CACHE":
            # 블록 캐시
            self._cache_block(command["block_id"])
        elif cmd_type == "DNA_UNCACHE":
            # 캐시 해제
            self._uncache_block(command["block_id"])

    def _transfer_block(self, block_id: int, target: str):
        """블록을 다른 DataNode로 전송"""
        block = self.blocks.get(block_id)
        if block:
            print(f"Transferring block {block_id} to {target}")

    def _delete_block(self, block_id: int):
        """블록 삭제"""
        if block_id in self.blocks:
            del self.blocks[block_id]
            print(f"Deleted block {block_id}")

    def _cache_block(self, block_id: int):
        """블록 캐시"""
        print(f"Cached block {block_id}")

    def _uncache_block(self, block_id: int):
        """캐시 해제"""
        print(f"Uncached block {block_id}")

    def write_block(self, block: Block):
        """블록 쓰기"""
        self.blocks[block.block_id] = block
        self.info.dfs_used += block.size
        self.info.remaining -= block.size
        print(f"Wrote block {block.block_id} ({block.size} bytes)")


# 사용 예시
if __name__ == "__main__":
    dn = DataNodeSimulator("dn-001", "namenode:8020")
    dn.start()

    # 블록 쓰기 시뮬레이션
    block = Block(
        block_id=12345,
        block_pool_id="BP-123",
        generation_stamp=1001,
        size=128 * 1024 * 1024,  # 128MB
        state=BlockState.FINALIZED,
        file_path="/data/file.parquet"
    )
    dn.write_block(block)

    time.sleep(10)  # 하트비트 대기
    dn.stop()
