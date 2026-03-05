+++
title = "컨테이너 (Container)"
date = 2024-05-11
description = "애플리케이션과 실행에 필요한 라이브러리, 의존성 패키지를 묶어(Image) 호스트 OS 커널을 공유하며 프로세스를 논리적으로 격리하는 경량 가상화 기술"
weight = 80
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Container", "Docker", "Namespace", "Cgroups", "OCI", "Container Runtime"]
+++

# 컨테이너 (Container) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: VM이 하드웨어를 가상화하는 반면, 컨테이너는 **OS 커널을 공유**하면서 프로세스 단위로 격리(Namespace)하고 자원을 제한(cgroups)하여, 수밀리초 내에 기동되는 초경량 가상화 기술입니다.
> 2. **가치**: VM 대비 **1/10 크기, 1/10 시작 시간**으로 마이크로서비스, CI/CD, DevOps의 핵심 기술이 되었으며, "Build once, Run anywhere"로 이식성을 혁명적으로 향상시켰습니다.
> 3. **융합**: Docker가 컨테이너를 대중화하고, Kubernetes가 컨테이너 오케스트레이션을 표준화했으며, OCI(Open Container Initiative)가 이미지/런타임 규격을 통일했습니다.

---

## Ⅰ. 개요 (Context & Background)

컨테이너(Container)는 애플리케이션과 그 실행에 필요한 모든 의존성(라이브러리, 설정 파일, 런타임 등)을 패키징한 후, 호스트 OS의 커널을 공유하면서 격리된 환경에서 실행하는 기술입니다. 가상머신(VM)이 각각 독립된 OS를 실행하는 것과 달리, 컨테이너는 단일 OS 커널 위에서 여러 격리된 프로세스로 실행되어 매우 가볍고 빠릅니다.

**💡 비유**: 컨테이너는 **'이삿짐 컨테이너 박스'**와 같습니다. 이사할 때 가구, 옷, 그릇을 각각 따로 옮기면 복잡하지만, 컨테이너 박스에 모두 담으면 한 번에 옮길 수 있습니다. 이 박스는 어떤 트럭(서버)에 실려도 내용물은 그대로입니다. VM은 각 가구마다 별도의 트럭을 쓰는 것이라면, 컨테이너는 한 트럭에 여러 박스를 싣는 것입니다.

**등장 배경 및 발전 과정**:
1. **chroot의 한계 (1979~)**: Unix chroot가 디렉토리 격리를 시작했으나, 보안성이 약했습니다.
2. **FreeBSD Jails (2000)**: 더 강력한 격리 환경을 제공했습니다.
3. **LXC (2008)**: 리눅스 커널의 Namespace와 cgroups를 활용한 컨테이너 구현.
4. **Docker의 혁신 (2013)**: Solomon Hykes가 Docker를 발표하며, 이미지 포맷, 레이어드 파일시스템, Dockerfile, Docker Hub로 컨테이너를 대중화했습니다.
5. **Kubernetes의 등장 (2014)**: 구글이 Kubernetes를 오픈소스화하며 컨테이너 오케스트레이션 표준을 정립했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 컨테이너 vs 가상머신 구조 비교

| 비교 항목 | 가상머신 (VM) | 컨테이너 (Container) |
|---|---|---|
| **격리 계층** | 하드웨어 (Hypervisor) | OS 프로세스 (Kernel) |
| **OS** | 각 VM마다 Guest OS | 호스트 OS 커널 공유 |
| **시작 시간** | 수분 | 수밀리초 |
| **크기** | GB (OS 포함) | MB (앱 + 라이브러리) |
| **성능 오버헤드** | 5~15% | 1~3% |
| **보안 격리** | 강함 (하드웨어 레벨) | 중간 (커널 공유) |
| **이식성** | 낮음 (하드웨어 종속) | 높음 (OCI 표준) |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Virtual Machine Architecture ]                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │    App A    │  │    App B    │  │    App C    │  │    App D    │       │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │       │
│  │ │Libs/Deps│ │  │ │Libs/Deps│ │  │ │Libs/Deps│ │  │ │Libs/Deps│ │       │
│  │ ├─────────┤ │  │ ├─────────┤ │  │ ├─────────┤ │  │ ├─────────┤ │       │
│  │ │Guest OS │ │  │ │Guest OS │ │  │ │Guest OS │ │  │ │Guest OS │ │       │
│  │ │ (Linux) │ │  │ │(Windows)│ │  │ │ (Linux) │ │  │ │ (Linux) │ │       │
│  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │       │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         Hypervisor                                    │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                        Host Operating System                          │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                          Physical Hardware                            │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Container Architecture ]                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │    App A    │  │    App B    │  │    App C    │  │    App D    │       │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │       │
│  │ │Libs/Deps│ │  │ │Libs/Deps│ │  │ │Libs/Deps│ │  │ │Libs/Deps│ │       │
│  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │       │
│  │  Container  │  │  Container  │  │  Container  │  │  Container  │       │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │
│         │                │                │                │               │
│  ┌──────▼────────────────▼────────────────▼────────────────▼────────────┐ │
│  │                   Container Runtime (Docker/containerd)               │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                     Host Operating System (Kernel)                    │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │ │
│  │  │ Namespaces  │  │   cgroups   │  │  UnionFS    │  │  Seccomp    │  │ │
│  │  │  (격리)     │  │  (자원제한) │  │ (레이어FS)  │  │ (보안)      │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                          Physical Hardware                            │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: Linux 커널 기술

```
┌────────────────────────────────────────────────────────────────────────────┐
│              Container Isolation: Namespaces + Cgroups                     │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ Linux Namespaces (격리) ]                                               │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ Namespace      │ 격리 대상                    │ 예시              │   │
│  ├────────────────┼──────────────────────────────┼───────────────────┤   │
│  │ PID            │ 프로세스 ID                  │ 컨테이너 내 PID=1 │   │
│  │ NET            │ 네트워크 스택 (IP, Port)     │ 자체 eth0, 루프백│   │
│  │ MNT            │ 마운트 포인트                │ 자체 파일시스템  │   │
│  │ UTS            │ 호스트명, 도메인             │ container-host   │   │
│  │ IPC            │ System V IPC, POSIX 큐       │ 격리된 세마포어  │   │
│  │ USER           │ 사용자/그룹 ID               │ root(컨테이너)   │   │
│  │ TIME           │ 시간 (Linux 5.6+)            │ 격리된 시간      │   │
│  │ CGROUP         │ cgroup 루트 디렉토리         │ 격리된 cgroup    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  [ Cgroups (자원 제한) ]                                                   │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ Subsystem      │ 제한 대상                    │ 예시              │   │
│  ├────────────────┼──────────────────────────────┼───────────────────┤   │
│  │ cpu            │ CPU 사용량                   │ 0.5 CPU core      │   │
│  │ cpuacct        │ CPU 사용량 계정              │ 사용량 통계       │   │
│  │ cpuset         │ CPU 코어 할당                │ CPU 0, 1만 사용   │   │
│  │ memory         │ 메모리 사용량                │ 512MB 제한        │   │
│  │ blkio          │ 블록 I/O                    │ 100MB/s 제한      │   │
│  │ devices        │ 디바이스 접근                │ /dev/sda 차단    │   │
│  │ freezer        │ 프로세스 일시정지            │ 스냅샷용          │   │
│  │ net_cls        │ 네트워크 트래픽 태깅         │ QoS용             │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: Dockerfile 및 컨테이너 실행

```dockerfile
# Dockerfile - Multi-stage Build 예시
# Stage 1: 빌드 환경
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Stage 2: 실행 환경 (최종 이미지)
FROM node:18-alpine

# 보안: 비루트 사용자로 실행
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

WORKDIR /app

# 빌드 결과물만 복사 (이미지 크기 최소화)
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV NODE_ENV=production

# 헬스체크 추가
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "server.js"]
```

```bash
# 컨테이너 실행 명령어
docker build -t brainscience-api:v1.0 .

docker run -d \
    --name api-server \
    --memory="512m" \           # cgroups: 메모리 제한
    --cpus="0.5" \              # cgroups: CPU 제한
    --pids-limit=100 \          # 프로세스 수 제한
    --security-opt="no-new-privileges:true" \  # 권한 상승 방지
    --read-only \               # 읽기 전용 파일시스템
    --tmpfs /tmp \              # 임시 파일시스템
    -p 3000:3000 \
    brainscience-api:v1.0
```

```python
# Python으로 컨테이너 Namespace 확인
import os

def check_container_isolation():
    """컨테이너 내에서 격리 상태 확인"""
    print(f"PID 1 프로세스: {os.readlink('/proc/1/exe')}")
    print(f"Hostname: {os.uname().nodename}")
    print(f"내 PID: {os.getpid()}")

    # /proc/1/cgroup 확인
    with open('/proc/1/cgroup', 'r') as f:
        cgroup = f.read()
        if 'docker' in cgroup or 'kubepods' in cgroup:
            print("컨테이너 환경에서 실행 중입니다.")
        else:
            print("호스트 환경에서 실행 중입니다.")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 컨테이너 런타임

| 비교 관점 | Docker (Moby) | containerd | CRI-O | runc |
|---|---|---|---|---|
| **역할** | 전체 플랫폼 | 런타임 + 이미지 관리 | K8s 전용 런타임 | 저수준 런타임 |
| **복잡도** | 높음 | 중간 | 낮음 | 최저 |
| **K8s 통합** | dockershim (deprecated) | CRI native | CRI native | 직접 사용 안 함 |
| **Daemonless** | 아니오 (dockerd) | 아니오 (containerd) | 아니오 (crio) | 예 |

### 과목 융합 관점 분석

**운영체제(OS)와의 융합**:
- 컨테이너는 리눅스 커널 기술(Namespace, cgroups, UnionFS, Seccomp)의 집합체입니다.
- **Seccomp(Secure Computing Mode)**: 시스템 콜을 필터링하여 공격 표면 축소

**네트워크와의 융합**:
- **CNI(Container Network Interface)**: 컨테이너 네트워크 구성 표준
- **veth pair**: 컨테이너와 호스트 간 가상 이더넷 페어
- **Network Namespace**: 각 컨테이너의 독립 네트워크 스택

**보안(Security)과의 융합**:
- **Container Escape**: 컨테이너에서 호스트로 탈출하는 공격
- **Defense in Depth**: Seccomp + AppArmor + SELinux + User Namespace

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 컨테이너 보안 강화

**문제 상황**: 컨테이너 기반 마이크로서비스 환경에서 보안 강화가 필요합니다.

**기술사의 전략적 의사결정**:
1. **이미지 보안**: Base Image 최소화(distroless), 정기 CVE 스캔(Trivy)
2. **런타임 보안**: Rootless 컨테이너, Read-only 파일시스템, Seccomp 프로파일
3. **네트워크 보안**: Network Policy로 마이크로 세그멘테이션
4. **Secrets 관리**: 이미지에 Secret 하드코딩 금지, Vault 사용

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - Fat Container**: 컨테이너에 불필요한 패키지, SSH, systemd를 설치하면 VM과 다를 바 없습니다. Single Process, Minimal Base Image 원칙 준수.
- **체크리스트**:
  - [ ] distroless/scratch 베이스 이미지 사용
  - [ ] Non-root 사용자로 실행
  - [ ] Read-only 루트 파일시스템
  - [ ] Resource Limit 설정 (CPU, Memory)
  - [ ] 이미지 취약점 스캔 자동화

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | VM | Container | 개선율 |
|---|---|---|---|
| **이미지 크기** | GB | MB | 99% 축소 |
| **시작 시간** | 수분 | 수밀ms | 99% 단축 |
| **밀도** | 10-20 VM/호스트 | 100-1000 컨테이너/호스트 | 50-100배 |
| **배포 속도** | 수시간 | 수분 | 95% 단축 |

### 미래 전망 및 진화 방향

- **WebAssembly (Wasm)**: 컨테이너보다 더 가볍고 빠른 실행 환경
- **Confidential Containers**: 하드웨어 기반 메모리 암호화로 컨테이너 데이터 보호
- **Rootless Containers**: root 권한 없이 컨테이너 실행으로 보안 강화

### ※ 참고 표준/가이드
- **OCI (Open Container Initiative)**: 이미지 스펙, 런타임 스펙 표준
- **CNI (Container Network Interface)**: 네트워크 구성 표준
- **CSI (Container Storage Interface)**: 스토리지 표준
- **CIS Docker Benchmark**: 컨테이너 보안 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [Docker](@/studynotes/13_cloud_architecture/01_native/docker.md) : 컨테이너 대중화 플랫폼
- [Kubernetes](@/studynotes/13_cloud_architecture/01_native/kubernetes.md) : 컨테이너 오케스트레이션
- [Namespace & Cgroups](@/studynotes/13_cloud_architecture/01_native/namespace_cgroups.md) : 컨테이너 핵심 기술
- [OCI](@/studynotes/13_cloud_architecture/01_native/oci.md) : 컨테이너 표준 규격
- [컨테이너 보안](@/studynotes/13_cloud_architecture/01_native/container_security.md) : 컨테이너 보안 실무

---

### 👶 어린이를 위한 3줄 비유 설명
1. 컨테이너는 **'이삿짐 박스'**예요. 내 방의 모든 물건을 박스에 딱 담아두면, 이사할 때 그 박스만 들고 가면 돼요.
2. 이 박스는 **'어떤 집으로 가도 똑같이 작동해요'**. 큰 집이든 작은 집이든, 박스 속 물건은 그대로니까요.
3. 그리고 박스가 **'아주 가볍고 작아요'**. 왜냐하면 집(운영체제)을 통째로 담지 않고, 내 물건만 담았거든요!
