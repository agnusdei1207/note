+++
title = "리눅스 네임스페이스 (Linux Namespaces)"
date = 2024-05-18
description = "프로세스별로 PID, 네트워크, 마운트, 사용자 등 시스템 자원을 독립된 공간처럼 분리 격리하는 리눅스 커널 기술"
weight = 63
[taxonomies]
categories = ["studynotes-13_cloud_architecture"]
tags = ["Linux Namespaces", "Container Isolation", "PID Namespace", "Network Namespace", "cgroups"]
+++

# 리눅스 네임스페이스 (Linux Namespaces)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 리눅스 네임스페이스는 프로세스가 보는 시스템 리소스(PID, 네트워크, 파일시스템, 사용자, IPC 등)를 격리된 독립 공간으로 분할하여, 각 프로세스 그룹이 자신만의 전용 리소스 뷰를 가지도록 하는 리눅스 커널 레벨 격리 기술입니다.
> 2. **가치**: 컨테이너(Docker, Kubernetes)의 핵심 격리 메커니즘으로, 프로세스 격리, 보안 샌드박싱, 멀티 테넌시, 네트워크 가상화를 오버헤드 없이(하이퍼바이저 없음) 구현합니다.
> 3. **융합**: cgroups(자원 제한), seccomp(시스템콜 필터링), capabilities(권한 제한), 컨테이너 런타임(containerd, runc)과 결합하여 완전한 컨테이너 격리 환경을 구성합니다.

---

## Ⅰ. 개요 (Context & Background)

리눅스 네임스페이스는 2002년 Linux 2.4.19에 처음 도입된 이후, 컨테이너 기술의 기반이 되었습니다. 하이퍼바이저 기반 가상화가 하드웨어를 에뮬레이션하는 반면, 네임스페이스는 커널 레벨에서 리소스 뷰를 격리하여 거의 네이티브 성능을 제공합니다. 현재 8가지 네임스페이스가 존재하며, Docker, Kubernetes의 모든 컨테이너는 이를 기반으로 격리됩니다.

**💡 비유**: 네임스페이스는 **'나라별 여권 시스템'**과 같습니다. 한 사람(프로세스)이 한국(PID 네임스페이스 1)에서는 "시민 12345번"이지만, 미국(PID 네임스페이스 2)에서는 "시민 67890번"입니다. 각 나라는 자신만의 주민등록 시스템, 도로망(네트워크), 화폐(마운트)를 가집니다. 나라 간 경계가 있어, 한국 시민이 미국 법을 어겨도 미국 경찰이 체포할 수 없습니다(격리).

**등장 배경 및 발전 과정**:
1. **chroot의 한계**: 파일시스템만 격리, 다른 리소스는 공유.
2. **넥서스(Namespaces) 도입 (2002)**: Mount 네임스페이스로 시작.
3. **PID 네임스페이스 (2006)**: 프로세스 ID 격리.
4. **Network 네임스페이스 (2009)**: 네트워크 스택 격리.
5. **User 네임스페이스 (2013)**: root 권한 매핑, 컨테이너 보안 혁신.
6. **Cgroup 네임스페이스 (2016)**: cgroup 루트 격리.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 네임스페이스 종류 (표)

| 네임스페이스 | 격리 대상 | 커널 버전 | 주요 용도 | 비유 |
|---|---|---|---|---|
| **PID** | 프로세스 ID | 2.6.24 (2008) | 컨테이너 내 PID 1 | 주민등록번호 |
| **Network (net)** | 네트워크 스택 | 2.6.29 (2009) | IP, 포트, 라우팅 | 도로망 |
| **Mount (mnt)** | 마운트 포인트 | 2.4.19 (2002) | 파일시스템 뷰 | 건물 구조 |
| **UTS** | 호스트명, 도메인 | 2.6.19 (2006) | hostname 격리 | 나라 이름 |
| **IPC** | System V IPC, POSIX | 2.6.19 (2006) | 메시지 큐, 세마포어 | 우편 시스템 |
| **User** | 사용자/그룹 ID | 3.5 (2012) | uid/gid 매핑 | 시민권 |
| **Cgroup** | cgroup 루트 | 4.6 (2016) | cgroup 계층 격리 | 예산 배정 |
| **Time** | 시간 | 5.6 (2020) | CLOCK_BOOTIME 격리 | 표준시 |

### 네임스페이스 계층 구조 다이어그램

```ascii
+===========================================================================+
|                  Linux Namespaces Architecture                            |
|                                                                           |
|  [Host System - Initial Namespaces]                                      |
|  +--------------------------------------------------------------------+  |
|  |  PID NS (init)      |  NET NS (eth0)   |  MNT NS (/)             |  |
|  |  User NS (root)     |  UTS NS (host)   |  IPC NS (System V)      |  |
|  +--------------------------------------------------------------------+  |
|                                    |                                      |
|                    +---------------+---------------+                      |
|                    |                               |                      |
|          +---------v---------+          +---------v---------+             |
|          |  Container A      |          |  Container B      |             |
|          |  (Child NS)       |          |  (Child NS)       |             |
|          +-------------------+          +-------------------+             |
|          | PID NS:           |          | PID NS:           |            |
|          |  - PID 1 (app)    |          |  - PID 1 (nginx)  |            |
|          |  - PID 10 (helper)|          |  - PID 5 (worker) |            |
|          +-------------------+          +-------------------+             |
|          | NET NS:           |          | NET NS:           |            |
|          |  - eth0 (veth)    |          |  - eth0 (veth)    |            |
|          |  - lo             |          |  - lo             |            |
|          |  - 172.17.0.2/16  |          |  - 172.17.0.3/16  |            |
|          +-------------------+          +-------------------+             |
|          | MNT NS:           |          | MNT NS:           |            |
|          |  - / (rootfs A)   |          |  - / (rootfs B)   |            |
|          +-------------------+          +-------------------+             |
|          | UTS NS:           |          | UTS NS:           |            |
|          |  - hostname: app-a|          |  - hostname: web-b|            |
|          +-------------------+          +-------------------+             |
|          | User NS:          |          | User NS:          |            |
|          |  - uid 0->1000    |          |  - uid 0->1001    |            |
|          |  - gid 0->1000    |          |  - gid 0->1001    |            |
|          +-------------------+          +-------------------+             |
|                                                                           |
+===========================================================================+

[From Host Perspective]
+---------------------------------------------------------------------------+
| Host $ ps aux | grep container                                            |
| root   12345  ...  container A  (PID 12345 on host = PID 1 in container)  |
| root   12346  ...  container B  (PID 12346 on host = PID 1 in container)  |
+---------------------------------------------------------------------------+

[From Container A Perspective]
+---------------------------------------------------------------------------+
| Container A $ ps aux                                                      |
| PID   USER     COMMAND                                                    |
| 1     root     /app              (Actually PID 12345 on host)            |
| 10    app      helper           (Actually PID 12350 on host)             |
+---------------------------------------------------------------------------+
```

### 심층 동작 원리: Network Namespace 격리

1. **네임스페이스 생성 (ns_create)**:
   - `unshare --net` 또는 `clone(CLONE_NEWNET)` 시스템콜
   - 커널이 새로운 net_namespace 구조체 할당
   - 빈 네트워크 스택(lo만 존재) 생성

2. **가상 이더넷 페어 (veth pair) 생성**:
   - `ip link add veth0 type veth peer name veth1`
   - 두 인터페이스가 연결된 "가상 케이블"
   - 한쪽은 호스트 네임스페이스, 다른쪽은 컨테이너 네임스페이스로 이동

3. **인터페이스 이동 (if_move)**:
   - `ip link set veth1 netns <container_pid>`
   - veth1이 컨테이너의 net_namespace로 이동
   - 호스트에서는 veth1이 사라짐

4. **IP 할당 및 라우팅**:
   - 컨테이너 내: `ip addr add 172.17.0.2/16 dev eth0`
   - 호스트 라우팅: `ip route add 172.17.0.0/16 dev docker0`

5. **패킷 흐름**:
   - 컨테이너에서 패킷 송신 -> veth1 -> veth0 -> docker0 -> 외부
   - 각 네임스페이스는 독립적인 라우팅 테이블, iptables 보유

### 핵심 코드: 네임스페이스 조작 (C/Python)

```c
/*
 * Linux Namespace 생성 예제 (C)
 * 새로운 PID, Network, Mount 네임스페이스에서 프로세스 실행
 */

#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/mount.h>
#include <sys/syscall.h>

#define STACK_SIZE (1024 * 1024)

static char child_stack[STACK_SIZE];

/* 새로운 네임스페이스에서 실행될 함수 */
static int child_fn(void *arg) {
    /* 새로운 네임스페이스 내부 */

    // 1. UTS 네임스페이스: 호스트명 변경
    sethostname("container", 9);

    // 2. Mount 네임스페이스: proc 파일시스템 마운트
    mount("proc", "/proc", "proc", 0, NULL);

    // 3. PID 확인 (새 네임스페이스에서 PID 1)
    printf("Container PID: %d\n", getpid());  // 출력: 1

    // 4. 호스트명 확인
    char hostname[64];
    gethostname(hostname, sizeof(hostname));
    printf("Container Hostname: %s\n", hostname);  // 출력: container

    // 5. 쉘 실행
    execlp("/bin/bash", "/bin/bash", NULL);

    return 0;
}

int main(int argc, char *argv[]) {
    /* 네임스페이스 생성 플래그 */
    int clone_flags =
        CLONE_NEWUTS |    // UTS 네임스페이스 (hostname)
        CLONE_NEWPID |    // PID 네임스페이스
        CLONE_NEWNS |     // Mount 네임스페이스
        CLONE_NEWNET |    // Network 네임스페이스
        CLONE_NEWIPC |    // IPC 네임스페이스
        SIGCHLD;          // 자식 종료 시그널

    /* 자식 프로세스 생성 (새 네임스페이스) */
    pid_t child_pid = clone(
        child_fn,
        child_stack + STACK_SIZE,
        clone_flags,
        NULL
    );

    if (child_pid == -1) {
        perror("clone");
        exit(1);
    }

    printf("Host PID of container: %d\n", child_pid);

    /* 자식 대기 */
    waitpid(child_pid, NULL, 0);

    return 0;
}
```

```python
# Python: 네임스페이스 조작 (python-prctl 사용)
import os
import socket
import subprocess

class NamespaceManager:
    """리눅스 네임스페이스 관리자"""

    @staticmethod
    def create_network_namespace(name: str):
        """네트워크 네임스페이스 생성"""
        subprocess.run(["ip", "netns", "add", name], check=True)

    @staticmethod
    def delete_network_namespace(name: str):
        """네트워크 네임스페이스 삭제"""
        subprocess.run(["ip", "netns", "delete", name], check=True)

    @staticmethod
    def list_network_namespaces():
        """네트워크 네임스페이스 목록"""
        result = subprocess.run(
            ["ip", "netns", "list"],
            capture_output=True, text=True
        )
        return result.stdout.strip().split('\n')

    @staticmethod
    def create_veth_pair(veth_host: str, veth_ns: str, ns_name: str):
        """veth 페어 생성 및 네임스페이스 연결"""
        # veth 페어 생성
        subprocess.run([
            "ip", "link", "add", veth_host, "type", "veth",
            "peer", "name", veth_ns
        ], check=True)

        # 한쪽을 네임스페이스로 이동
        subprocess.run([
            "ip", "link", "set", veth_ns, "netns", ns_name
        ], check=True)

        # 네임스페이스 내에서 인터페이스 활성화
        subprocess.run([
            "ip", "netns", "exec", ns_name,
            "ip", "link", "set", veth_ns, "up"
        ], check=True)

        # 호스트 인터페이스 활성화
        subprocess.run(["ip", "link", "set", veth_host, "up"], check=True)

    @staticmethod
    def assign_ip_to_namespace(ns_name: str, interface: str, ip_cidr: str):
        """네임스페이스 내 인터페이스에 IP 할당"""
        subprocess.run([
            "ip", "netns", "exec", ns_name,
            "ip", "addr", "add", ip_cidr, "dev", interface
        ], check=True)

    @staticmethod
    def exec_in_namespace(ns_name: str, command: list):
        """네임스페이스 내 명령 실행"""
        full_cmd = ["ip", "netns", "exec", ns_name] + command
        return subprocess.run(full_cmd, capture_output=True, text=True)

# 사용 예시
if __name__ == "__main__":
    ns = NamespaceManager()

    # 1. 네트워크 네임스페이스 생성
    ns.create_network_namespace("test-ns")
    print("Created namespace: test-ns")

    # 2. veth 페어 생성
    ns.create_veth_pair("veth-host", "veth-ns", "test-ns")

    # 3. IP 할당
    ns.assign_ip_to_namespace("test-ns", "veth-ns", "10.0.0.2/24")

    # 4. 네임스페이스 내에서 ping 테스트
    result = ns.exec_in_namespace("test-ns", ["ip", "addr"])
    print(f"Namespace interfaces:\n{result.stdout}")

    # 5. 정리
    ns.delete_network_namespace("test-ns")
    print("Deleted namespace: test-ns")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 네임스페이스 vs 가상머신 격리 비교

| 비교 항목 | 네임스페이스 (Container) | 가상머신 (VM) |
|---|---|---|
| **격리 수준** | 커널 공유, 리소스 뷰만 격리 | 완전한 커널 격리 |
| **성능** | 네이티브 (오버헤드 <5%) | 가상화 오버헤드 (5~20%) |
| **시작 시간** | 밀리초 | 초~분 |
| **메모리 사용** | MB | GB |
| **보안** | 커널 취약점 시 탈출 가능 | 하이퍼바이저 격리 |
| **밀도** | 수천 컨테이너/호스트 | 수십 VM/호스트 |

### 과목 융합 관점 분석

- **운영체제와의 융합**: 네임스페이스는 리눅스 커널의 핵심 격리 메커니즘입니다. 스케줄러, 메모리 관리, VFS와 밀접하게 연동됩니다.

- **네트워크와의 융합**: Network 네임스페이스는 각 컨테이너에 독립된 네트워크 스택(IP, 라우팅, iptables)을 제공합니다. Docker bridge, Kubernetes CNI의 기반입니다.

- **보안과의 융합**: User 네임스페이스로 root 권한 매핑, 컨테이너 내 root는 호스트에서 일반 사용자. seccomp, capabilities와 결합하여 공격 표면 최소화.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 멀티 테넌트 SaaS 컨테이너 격리**
- **요구사항**: 각 테넌트 컨테이너 완전 격리, 네트워크 분리
- **기술사의 의사결정**:
  1. 각 테넌트 Pod에 전용 Network 네임스페이스
  2. Network Policy로 테넌트 간 통신 차단
  3. User 네임스페이스로 권한 격리
  4. **효과**: 테넌트 간 완전 격리, 보안 강화

**시나리오 2: 컨테이너 보안 강화**
- **요구사항**: 컨테이너 탈출 방지, 최소 권한
- **기술사의 의사결정**:
  1. User 네임스페이스: uid 0 -> 65534 (nobody)
  2. Read-only Mount 네임스페이스
  3. seccomp로 시스템콜 필터링
  4. **효과**: 컨테이너 침해 시 호스트 영향 최소화

### 도입 시 고려사항

- [ ] User 네임스페이스 활성화: 커널 설정 필요
- [ ] 네임스페이스 중첩: Kubernetes Pod 내 Docker 실행 시 주의
- [ ] 리소스 누수: 네임스페이스 미삭제 시 리소스 잔존

### 안티패턴

1. **과도한 네임스페이스 생성**: 관리 복잡성 증가
2. **User NS 미사용**: root 컨테이너는 호스트 root와 동일 권한
3. **공유 네임스페이스**: --pid=host, --net=host는 격리 약화

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대효과

| 구분 | 전통적 프로세스 | 네임스페이스 격리 | 개선 |
|---|---|---|---|
| **격리** | 없음 | 리소스 뷰 격리 | 보안 강화 |
| **성능** | 네이티브 | 네이티브 | 오버헤드 없음 |
| **밀도** | 제한적 | 높음 | 자원 효율 |
| **시작 시간** | 즉시 | 즉시 | 지연 없음 |

### 미래 전망

1. **Time 네임스페이스 확대**: 컨테이너별 시간 격리
2. **사용자 네임스페이스 기본화**: rootless 컨테이너 표준화
3. **WebAssembly와 결합**: 더 강력한 샌드박싱

### ※ 참고 표준/문서
- **man namespaces(7)**: 리눅스 매뉴얼
- **OCI Runtime Spec**: 컨테이너 네임스페이스 규격
- **Linux Kernel Documentation**: Documentation/admin-guide/namespaces

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [cgroups](@/studynotes/13_cloud_architecture/01_native/cgroups.md) : 자원 제한
- [컨테이너](@/studynotes/13_cloud_architecture/01_native/container.md) : 네임스페이스 기반 격리
- [Docker](@/studynotes/13_cloud_architecture/01_native/docker.md) : 네임스페이스 활용
- [seccomp](@/studynotes/13_cloud_architecture/01_native/seccomp.md) : 시스템콜 필터링
- [Kubernetes Pod](@/studynotes/13_cloud_architecture/01_native/pod.md) : 네임스페이스 공유

---

### 👶 어린이를 위한 3줄 비유 설명
1. 네임스페이스는 **'각자 방이 있는 집'**과 같아요. 내 방에서는 내가 1번이에요.
2. 다른 방에 있는 동생도 **'자기 방에서는 1번'**이에요. 서로 이름이 같아도 괜찮아요.
3. 내 방의 장난감(파일, 네트워크)은 **'동생 방에 없어요'**. 완전히 다른 공간이거든요!
