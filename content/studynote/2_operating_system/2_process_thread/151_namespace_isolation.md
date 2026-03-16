+++
title = "[OS] 151. 네임스페이스 격리 프로세스 (Namespace Isolation)"
date = "2026-03-04"
[extra]
categories = "studynote-operating-system"
tags = ["Namespace", "Isolation", "Container", "Linux Kernel", "Security"]
+++

# 네임스페이스 격리 프로세스 (Namespace Isolation)

## 1. 네임스페이스 격리 (Namespace Isolation)의 정의
- 커널 자원을 프로세스별로 격리하여, 특정 프로세스 그룹이 다른 프로세스나 시스템 자원을 볼 수 없도록 하는 리눅스 커널의 기능
- 컨테이너 기술(Docker, Podman 등)의 핵심 기반 기술로, 운영체제 수준의 가상화(OS-level Virtualization)를 실현함

## 2. 네임스페이스 격리의 메커니즘 및 유형

### 2.1 네임스페이스 격리 메커니즘
- 프로세스 생성 시 `clone()`, `unshare()`, `setns()` 시스템 호출을 통해 특정 네임스페이스를 할당하거나 변경함

### 2.2 주요 네임스페이스 유형
| 유형 | 격리 대상 | 설명 |
|---|---|---|
| **Mount (mnt)** | 파일시스템 마운트 포인트 | 프로세스별 독립적인 파일시스템 구조 제공 |
| **Process ID (pid)** | 프로세스 ID 공간 | 독립적인 PID 체계(격리된 공간에서 PID 1번 부여) |
| **Network (net)** | 네트워크 스택 | 전용 IP 주소, 라우팅 테이블, 포트 공간 |
| **Inter-Process (ipc)** | IPC 자원 | 세마포어, 공유 메모리, 메시지 큐 격리 |
| **UTS** | 호스트명, 도메인명 | 독립적인 시스템 이름 설정 |
| **User (user)** | 사용자/그룹 ID | 호스트의 루트와 컨테이너의 루트 매핑 격리 |
| **Cgroup** | Cgroup 루트 디렉토리 | 리소스 제한 가시성 격리 |

### 2.3 ASCII 개념도
```text
[ Physical Hardware / Host Kernel ]
          |
  +-------+-------------------------+
  |       | (System Calls: clone, unshare)
  v       v
+-------------+     +-------------+
| Namespace A |     | Namespace B |
| [PID 1]     |     | [PID 1]     |
| [IP: 10.1]  |     | [IP: 10.2]  |
| [mnt /root] |     | [mnt /app]  |
+-------------+     +-------------+
   (Process)           (Process)
```

## 3. 네임스페이스 격리의 주요 특징 및 비교

### 3.1 특징
- **경량성:** 하이퍼바이저 가상화와 달리 하드웨어 에뮬레이션이 없어 오버헤드가 매우 적음
- **보안성:** 프로세스 간 자원 가시성을 차단하여 침해 사고 시 확산을 방지함

### 3.2 하이퍼바이저 가상화 vs 네임스페이스 격리 (컨테이너)
| 구분 | 가상머신 (VM) | 컨테이너 (Namespace) |
|---|---|---|
| **격리 수준** | 하드웨어 수준 (Strong) | 운영체제 커널 수준 (Medium) |
| **게스트 OS** | 필요함 | 필요 없음 (호스트 커널 공유) |
| **시작 시간** | 수 분 단위 | 초 단위 이하 |

## 4. 기술사적 견해: 네임스페이스 격리의 진화
- 최근에는 네임스페이스뿐만 아니라 eBPF, Seccomp, AppArmor와 결합하여 더 세밀한(Fine-grained) 격리 및 모니터링 체계를 구축하는 추세임
- 보안 강화를 위해 Kata Containers와 같이 하드웨어 가상화 기술을 결합한 샌드박스형 컨테이너 기술이 등장하고 있으며, 이는 신뢰할 수 없는 코드 실행 환경에서 필수적인 아키텍처임
