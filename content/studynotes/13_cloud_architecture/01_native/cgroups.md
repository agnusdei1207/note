+++
title = "cgroups (Control Groups)"
date = 2024-05-18
description = "컨테이너가 사용할 수 있는 CPU 메모리 자원의 상한선을 제한하고 모니터링하는 리눅스 커널 기술"
weight = 64
[taxonomies]
categories = ["studynotes-13_cloud_architecture"]
tags = ["cgroups", "Control Groups", "Resource Limits", "Container Isolation", "CPU Throttling"]
+++

# cgroups (Control Groups)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: cgroups(Control Groups)는 프로세스 그룹 단위로 CPU, 메모리, I/O, 네트워크 대역폭 등 시스템 자원의 사용량을 제한(Limit), 계층화(Hierarchy), 모니터링(Accounting), 우선순위 지정(Prioritize)하는 리눅스 커널 기능입니다.
> 2. **가치**: 컨테이너(Docker, K8s)의 자원 격리 메커니즘으로, 노이지 네이버(Noisy Neighbor) 문제 방지, OOM(Out-of-Memory) 제어, QoS(Quality of Service) 보장, 과금(Fair Usage) 측정을 가능하게 합니다.
> 3. **융합**: 네임스페이스(리소스 뷰 격리), 컨테이너 런타임(containerd, runc), Kubernetes(QoS Classes), systemd와 결합하여 완전한 자원 관리 체계를 구성합니다.

---

## Ⅰ. 개요 (Context & Background)

cgroups는 2007년 Google이 개발하여 Linux 2.6.24에 병합된 기술로, 프로세스 그룹별 자원 사용을 제어합니다. 네임스페이스가 "무엇을 볼 수 있는가"를 결정한다면, cgroups는 "얼마나 사용할 수 있는가"를 제한합니다. 현재 cgroups v2( unified hierarchy)가 표준으로 자리잡고 있습니다.

**💡 비유**: cgroups는 **'식당의 한정식 코너'**와 같습니다. 각 테이블(프로세스 그룹)에는 주문할 수 있는 음식 양이 정해져 있습니다. A테이블은 "밥 1공기, 국 1그릇, 반찬 3가지"만 주문 가능합니다. 아무리 먹고 싶어도 그 이상은 안 됩니다. 또한 식당 주인은 각 테이블이 얼마나 먹었는지 기록(계량)해 둡니다.

**등장 배경 및 발전 과정**:
1. **자원 경쟁 문제**: 여러 프로세스가 무제한 자원 사용으로 시스템 마비.
2. **Google의 요구사항**: 수천 개 컨테이너를 실행하는 데이터센터에서 자원 격리 필요.
3. **cgroups v1 (2007)**: 여러 계층(hierarchy)을 가진 초기 버전.
4. **cgroups v2 (2016)**: 단일 계층(unified)으로 단순화, 커널 4.5.
5. **Kubernetes QoS**: cgroups 기반으로 Guaranteed, Burstable, BestEffort 클래스 구현.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Deep)

### cgroups 서브시스템(Controllers) (표)

| 서브시스템 | 격리 대상 | 주요 기능 | 사용 예시 |
|---|---|---|---|
| **cpu** | CPU 시간 | 할당량, 스케줄링 가중치 | cpu.shares, cpu.cfs_quota_us |
| **cpuacct** | CPU 사용량 | 계량(Accounting) | 사용 시간 통계 |
| **cpuset** | CPU 코어 | 특정 코어 할당 | cpuset.cpus=0-3 |
| **memory** | 메모리 | 상한, OOM 제어 | memory.limit_in_bytes |
| **blkio** | 블록 I/O | 디스크 대역폭 제한 | blkio.throttle.read_bps_device |
| **devices** | 장치 접근 | 장치 허용/차단 | devices.allow, devices.deny |
| **freezer** | 프로세스 상태 | 일시정지/재개 | freezer.state |
| **net_cls** | 네트워크 클래스 | 패킷 태깅 | net_cls.classid |
| **pids** | 프로세스 수 | 최대 프로세스 수 | pids.max |

### cgroups v1 vs v2 비교 (표)

| 비교 항목 | cgroups v1 | cgroups v2 |
|---|---|---|
| **계층 구조** | 여러 개 (각 서브시스템별) | 단일 (unified) |
| **마운트 위치** | /sys/fs/cgroup/<subsystem> | /sys/fs/cgroup/ |
| **스레드 제어** | 제한적 | thread granularity 지원 |
| **메모리 스왑** | 별도 컨트롤러 | memory.swap.max |
| **Pressure Stall** | 없음 | psi (pressure stall info) |
| **복잡성** | 높음 | 낮음 (단순화) |

### 정교한 cgroups 아키텍처 다이어그램

```ascii
+===========================================================================+
|                        cgroups Hierarchy (v2)                             |
|                                                                           |
|  /sys/fs/cgroup/                                                          |
|  +--------------------------------------------------------------------+  |
|  |                         Root Cgroup                               |  |
|  |  +-------------------------------------------------------------+  |  |
|  |  | cgroup.controllers = cpu memory io pids ...                |  |  |
|  |  | cgroup.subtree_control = cpu memory                         |  |  |
|  |  +-------------------------------------------------------------+  |  |
|  |                              |                                   |  |
|  |           +------------------+------------------+                |  |
|  |           |                                     |                |  |
|  |  +--------v--------+                  +---------v--------+       |  |
|  |  |   system.slice  |                  |  user.slice     |       |  |
|  |  |  (Systemd Services)               |  (User Sessions)|       |  |
|  |  +-----------------+                  +-----------------+       |  |
|  |           |                                     |                |  |
|  |  +--------v--------+                  +---------v--------+       |  |
|  |  |  docker.service |                  |  user-1000.slice|       |  |
|  |  +-----------------+                  +-----------------+       |  |
|  |           |                                     |                |  |
|  |           +------------------+------------------+                |  |
|  |                              |                                   |  |
|  |           +------------------+------------------+                |  |
|  |           |                  |                  |                |  |
|  |  +--------v--------+ +-------v-------+ +--------v--------+      |  |
|  |  | Container A     | | Container B   | | Container C     |      |  |
|  |  | (docker-abc123) | | (docker-def4) | | (docker-ghi5)   |      |  |
|  |  +-----------------+ +---------------+ +-----------------+      |  |
|  |  | cpu.max:        | | cpu.max:      | | cpu.max:        |      |  |
|  |  |   200000 100000 | |   100000 50000| |   max           |      |  |
|  |  | (2 cores limit) | | (1 core limit)| | (unlimited)     |      |  |
|  |  +-----------------+ +---------------+ +-----------------+      |  |
|  |  | memory.max:     | | memory.max:   | | memory.max:     |      |  |
|  |  |   2G            | |   512M        | |   4G            |      |  |
|  |  +-----------------+ +---------------+ +-----------------+      |  |
|  |  | io.max:         | | io.max:       | | io.max:         |      |  |
|  |  |   25M           | |   10M         | |   100M          |      |  |
|  |  +-----------------+ +---------------+ +-----------------+      |  |
|  +--------------------------------------------------------------------+  |
+===========================================================================+

[CPU Limit Enforcement]
+---------------------------------------------------------------------------+
| Container A Configuration:                                                |
|   cpu.max = 200000 100000  (200ms quota per 100ms period = 2 CPUs)       |
|                                                                           |
| Timeline (100ms period):                                                  |
| +--------------------------------------------------------------------+   |
| | Time: 0-25ms  | 25-50ms | 50-75ms | 75-100ms | 100-125ms | ...    |   |
| | CPU 0: A runs | A runs  | A runs  | A runs   | A runs    |        |   |
| | CPU 1: A runs | A runs  | A runs  | A runs   | A runs    |        |   |
| | CPU 2: Other  | Other   | Other   | Other    | Other     |        |   |
| +--------------------------------------------------------------------+   |
|                                                                           |
| After 100ms: Container A used 200ms (2 CPUs * 100ms) = quota exhausted   |
| Result: Container A is throttled until next period                       |
+---------------------------------------------------------------------------+
```

### 심층 동작 원리: CPU 스로틀링

1. **CPU 할당량 설정 (cpu.max)**:
   - `cpu.max = 200000 100000` (quota 200ms, period 100ms)
   - 100ms 기간 동안 200ms CPU 시간 사용 가능 = 2 CPU 코어

2. **스케줄러 동작 (CFS - Completely Fair Scheduler)**:
   - CFS가 각 cgroup의 가상 런타임(vruntime) 추적
   - cpu.shares는 상대적 가중치 (cpu.max와 별개)
   - quota 초과 시 cgroup 내 모든 태스크가 THROTTLED 상태

3. **스로틀링 (Throttling)**:
   - quota 소진 시 cgroup->throttled = true
   - 다음 period 시작까지 태스크 실행 불가
   - period 리셋 시 quota 복원, 실행 재개

4. **모니터링 (cpu.stat)**:
   ```
   nr_periods 1234        # 총 period 수
   nr_throttled 56        # 스로틀된 period 수
   throttled_time 789000  # 스로틀된 총 시간 (ns)
   ```

### 핵심 코드: cgroups v2 조작 (Python)

```python
"""
cgroups v2 관리 라이브러리
컨테이너 자원 제한 설정
"""
import os
import pathlib
from dataclasses import dataclass
from typing import Optional

@dataclass
class CgroupConfig:
    """cgroup 설정"""
    cpu_max: Optional[str] = None       # "200000 100000" or "max"
    cpu_weight: Optional[int] = None    # 1-10000 (default 100)
    memory_max: Optional[int] = None    # bytes or "max"
    memory_swap_max: Optional[int] = None
    io_max: Optional[str] = None        # "25M" or "max"
    pids_max: Optional[int] = None      # max processes

class CgroupManager:
    """cgroups v2 관리자"""

    CGROUP_ROOT = "/sys/fs/cgroup"

    def __init__(self, cgroup_name: str):
        self.cgroup_path = pathlib.Path(self.CGROUP_ROOT) / cgroup_name
        self.cgroup_name = cgroup_name

    def create(self) -> bool:
        """cgroup 생성"""
        try:
            self.cgroup_path.mkdir(parents=True, exist_ok=True)
            return True
        except PermissionError:
            raise RuntimeError("Root privileges required to create cgroup")

    def delete(self) -> bool:
        """cgroup 삭제"""
        try:
            self.cgroup_path.rmdir()
            return True
        except OSError:
            return False

    def add_process(self, pid: int) -> bool:
        """프로세스를 cgroup에 추가"""
        cgroup_procs = self.cgroup_path / "cgroup.procs"
        try:
            with open(cgroup_procs, "w") as f:
                f.write(str(pid))
            return True
        except IOError:
            return False

    def apply_config(self, config: CgroupConfig) -> dict:
        """cgroup 설정 적용"""
        results = {}

        # CPU 제한
        if config.cpu_max:
            cpu_max_file = self.cgroup_path / "cpu.max"
            with open(cpu_max_file, "w") as f:
                f.write(config.cpu_max)
            results["cpu_max"] = config.cpu_max

        # CPU 가중치 (shares 대체)
        if config.cpu_weight:
            cpu_weight_file = self.cgroup_path / "cpu.weight"
            with open(cpu_weight_file, "w") as f:
                f.write(str(config.cpu_weight))
            results["cpu_weight"] = config.cpu_weight

        # 메모리 제한
        if config.memory_max:
            memory_max_file = self.cgroup_path / "memory.max"
            with open(memory_max_file, "w") as f:
                f.write(str(config.memory_max))
            results["memory_max"] = f"{config.memory_max / (1024**2):.0f}MB"

        # 스왑 제한
        if config.memory_swap_max:
            swap_max_file = self.cgroup_path / "memory.swap.max"
            with open(swap_max_file, "w") as f:
                f.write(str(config.memory_swap_max))
            results["memory_swap_max"] = config.memory_swap_max

        # I/O 제한
        if config.io_max:
            io_max_file = self.cgroup_path / "io.max"
            with open(io_max_file, "w") as f:
                f.write(config.io_max)
            results["io_max"] = config.io_max

        # 프로세스 수 제한
        if config.pids_max:
            pids_max_file = self.cgroup_path / "pids.max"
            with open(pids_max_file, "w") as f:
                f.write(str(config.pids_max))
            results["pids_max"] = config.pids_max

        return results

    def get_stats(self) -> dict:
        """cgroup 통계 조회"""
        stats = {}

        # CPU 통계
        cpu_stat = self.cgroup_path / "cpu.stat"
        if cpu_stat.exists():
            with open(cpu_stat) as f:
                for line in f:
                    key, value = line.strip().split()
                    stats[f"cpu_{key}"] = value

        # 메모리 통계
        memory_current = self.cgroup_path / "memory.current"
        if memory_current.exists():
            with open(memory_current) as f:
                stats["memory_current"] = int(f.read().strip())

        memory_stat = self.cgroup_path / "memory.stat"
        if memory_stat.exists():
            with open(memory_stat) as f:
                for line in f:
                    key, value = line.strip().split()
                    stats[f"memory_{key}"] = value

        # I/O 통계
        io_stat = self.cgroup_path / "io.stat"
        if io_stat.exists():
            with open(io_stat) as f:
                stats["io_stat"] = f.read().strip()

        # Pressure Stall Information (PSI)
        cpu_pressure = self.cgroup_path / "cpu.pressure"
        if cpu_pressure.exists():
            with open(cpu_pressure) as f:
                stats["cpu_pressure"] = f.read().strip()

        memory_pressure = self.cgroup_path / "memory.pressure"
        if memory_pressure.exists():
            with open(memory_pressure) as f:
                stats["memory_pressure"] = f.read().strip()

        return stats

    def get_oom_events(self) -> int:
        """OOM 이벤트 수 조회"""
        memory_events = self.cgroup_path / "memory.events"
        if memory_events.exists():
            with open(memory_events) as f:
                for line in f:
                    if line.startswith("oom_kill"):
                        return int(line.split()[1])
        return 0

# 사용 예시
if __name__ == "__main__":
    # cgroup 생성
    manager = CgroupManager("test-container")
    manager.create()

    # 설정 적용
    config = CgroupConfig(
        cpu_max="200000 100000",     # 2 CPU cores
        cpu_weight=200,               # 2x default weight
        memory_max=2 * 1024 * 1024 * 1024,  # 2GB
        memory_swap_max=512 * 1024 * 1024,  # 512MB swap
        io_max="25M",                 # 25MB/s
        pids_max=1000                 # max 1000 processes
    )

    results = manager.apply_config(config)
    print("Applied configuration:")
    for key, value in results.items():
        print(f"  {key}: {value}")

    # 현재 프로세스 추가 (테스트)
    manager.add_process(os.getpid())
    print(f"\nAdded current process (PID: {os.getpid()}) to cgroup")

    # 통계 조회
    stats = manager.get_stats()
    print("\nCurrent stats:")
    print(f"  Memory used: {stats.get('memory_current', 0) / (1024**2):.1f}MB")
    print(f"  CPU throttled time: {int(stats.get('cpu_throttled_time', 0)) / 1e6:.1f}ms")
    print(f"  OOM kills: {manager.get_oom_events()}")

    # 정리
    manager.delete()
    print("\nCgroup deleted")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### Kubernetes QoS Classes와 cgroups 매핑

| QoS Class | CPU cgroup | Memory cgroup | OOM Score | 스케줄링 우선순위 |
|---|---|---|---|---|
| **Guaranteed** | cpu.limit = cpu.request | memory.limit = memory.request | -998 | 최고 |
| **Burstable** | cpu.limit > cpu.request | memory.limit > memory.request | 조정 | 중간 |
| **BestEffort** | 제한 없음 | 제한 없음 | 1000 | 최저 |

### 과목 융합 관점 분석

- **운영체제와의 융합**: cgroups는 리눅스 커널의 스케줄러(CFS), 메모리 관리(VM), 블록 계층과 밀접하게 연동됩니다. OOM Killer가 cgroup 내 프로세스를 선택적으로 종료합니다.

- **데이터베이스와의 융합**: DB 컨테이너에 충분한 memory.max를 설정해야 합니다. 부족하면 OOM Kill로 DB가 강제 종료될 수 있습니다.

- **보안과의 융합**: pids.max로 포크 폭탄(Fork Bomb) 방지, devices로 장치 접근 제어, freezer로 포렌식용 프로세스 정지.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 노이지 네이버 방지**
- **요구사항**: 빅데이터 작업이 웹 서버 CPU를 굶주리게 함
- **기술사의 의사결정**:
  1. 빅데이터 cgroup: cpu.max = 4 cores
  2. 웹 서버 cgroup: cpu.weight = 200 (빅데이터 100)
  3. memory.max로 메모리 보호
  4. **효과**: 웹 서버 응답시간 안정화

**시나리오 2: OOM 방지**
- **요구사항**: Java 앱이 메모리 누수로 시스템 마비
- **기술사의 의사결정**:
  1. memory.max = 4GB, memory.oom.group = 1
  2. OOM 시 해당 cgroup만 종료
  3. 앱 자동 재시작 (systemd/쿠버네티스)
  4. **효과**: 다른 서비스 영향 없음

### 도입 시 고려사항

- [ ] cgroups v2 확인: cat /sys/fs/cgroup/cgroup.controllers
- [ ] OOM ScoreAdj: oom_score_adj로 종료 우선순위 조정
- [ ] Pressure Stall Info: cpu.pressure, memory.pressure 모니터링

### 안티패턴

1. **과도한 제한**: memory.max를 실제 사용량에 너무 가깝게 설정 -> 빈번한 OOM
2. **스왑 무시**: memory.swap.max=0은 OOM 위험 증가
3. **CPU 코어 초과**: cpu.max > 물리 코어 수는 의미 없음

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대효과

| 구분 | cgroups 미사용 | cgroups 적용 | 개선 |
|---|---|---|---|
| **노이지 네이버** | 발생 | 차단 | 안정성 향상 |
| **OOM 영향** | 전체 시스템 | cgroup만 | 격리 달성 |
| **자원 효율** | 낮음 | 높음 | 밀도 향상 |
| **과금** | 불가능 | 가능 | 비용 투명성 |

### 미래 전망

1. **cgroups v2 표준화**: 모든 컨테이너 런타임이 v2 지원
2. **PSI 기반 오토스케일링**: pressure 정보로 선제적 스케일링
3. **Hardaware-assisted cgroups**: Intel RDT(CAT, MBA)와 통합

### ※ 참고 표준/문서
- **Linux Kernel Documentation**: Documentation/admin-guide/cgroup-v2.rst
- **systemd cgroups**: systemd.resource-control(5)
- **Kubernetes Resource Management**: k8s docs on resource management

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [리눅스 네임스페이스](@/studynotes/13_cloud_architecture/01_native/linux_namespaces.md) : 뷰 격리
- [컨테이너](@/studynotes/13_cloud_architecture/01_native/container.md) : cgroups 기반 자원 제한
- [Kubernetes QoS](@/studynotes/13_cloud_architecture/01_native/k8s_qos.md) : cgroups 기반 서비스 품질
- [OOM Killer](@/studynotes/13_cloud_architecture/01_native/oom_killer.md) : cgroups 메모리 제어
- [Docker Resource Limits](@/studynotes/13_cloud_architecture/01_native/docker_limits.md) : cgroups 활용

---

### 👶 어린이를 위한 3줄 비유 설명
1. cgroups는 **'한정식 주문 제한'**이에요. 각 테이블(컨테이너)이 먹을 수 있는 양이 정해져 있어요.
2. A테이블은 **'밥 2공기까지만'** 먹을 수 있어요. 더 먹고 싶어도 안 돼요.
3. 그래서 **'한 테이블이 다 먹어서'** 다른 테이블이 굶는 일이 없어요!
