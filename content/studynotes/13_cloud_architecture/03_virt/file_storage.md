+++
title = "파일 스토리지 (File Storage)"
date = 2026-03-05
description = "데이터를 파일 단위로 계층적 디렉터리 구조에 저장하고 NFS, SMB 프로토콜로 공유 액세스를 제공하는 스토리지 방식의 원리와 실무 적용"
weight = 77
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["File-Storage", "NAS", "NFS", "SMB", "EFS", "Shared-Storage"]
+++

# 파일 스토리지 (File Storage) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터를 파일이라는 논리적 단위로 관리하며, 디렉터리 트리 구조로 계층적으로 조직화하고, 파일 시스템 메타데이터(파일명, 권한, 타임스탬프)를 통해 액세스하는 스토리지 방식입니다.
> 2. **가치**: **다중 클라이언트 동시 접근**, **사용자 친화적 관리**, **기존 애플리케이션 호환성**을 제공하여 파일 공유, 홈 디렉터리, 콘텐츠 관리 시스템에 최적화되어 있습니다.
> 3. **융합**: NAS(Network Attached Storage), NFS/SMB 프로토콜, AWS EFS, 클라우드 파일 시스템과 결합하여 하이브리드 및 클라우드 환경의 공유 스토리지 계층을 구성합니다.

---

## Ⅰ. 개요 (Context & Background)

파일 스토리지(File Storage)는 데이터를 사람이 이해하기 쉬운 '파일'이라는 단위로 저장하고, 디렉터리(폴더) 구조로 체계화하는 전통적인 스토리지 방식입니다. 파일에는 데이터뿐만 아니라 파일명, 크기, 생성일, 수정일, 권한 등의 메타데이터가 함께 저장됩니다.

**💡 비유**: 파일 스토리지는 **'도서관의 서가 시스템'**과 같습니다. 책(파일)이 있고, 책에는 제목, 저자, 출판년도(메타데이터)가 있습니다. 책들은 주제별 섹션(디렉터리)에 정리되어 있고, 분류번호(경로)로 찾을 수 있습니다. 여러 사람이 동시에 도서관에서 책을 볼 수 있듯, 파일 스토리지도 여러 사용자가 동시에 접근할 수 있습니다.

**등장 배경 및 발전 과정**:
1. **로컬 파일 시스템 (1960~1980)**: 각 컴퓨터가 자체 파일 시스템(UNIX, FAT)을 가졌습니다.
2. **NFS의 등장 (1984)**: Sun Microsystems가 네트워크를 통해 파일을 공유하는 NFS(Network File System)를 개발했습니다.
3. **SMB/CIFS (1990~)**: Microsoft가 Windows 환경용 파일 공유 프로토콜을 개발했습니다.
4. **NAS 시장 확대 (2000~)**: NetApp, EMC 등 전용 NAS 어플라이언스가 기업 시장을 주도했습니다.
5. **클라우드 파일 스토리지 (2014~)**: AWS EFS, Azure Files 등 클라우드 네이티브 파일 시스템이 등장했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 및 특성

| 구성 요소 | 상세 역할 | 기술/프로토콜 | 비고 |
|---|---|---|---|
| **파일 (File)** | 데이터 + 메타데이터의 논리적 단위 | 이름, 크기, 권한, 시간 | 사용자 인터페이스 |
| **디렉터리 (Directory)** | 파일과 하위 디렉터리를 포함하는 컨테이너 | 계층적 트리 구조 | 폴더라고도 함 |
| **파일 시스템 (FS)** | 파일 저장/검색/관리를 위한 소프트웨어 계층 | ext4, XFS, NTFS, NFS | 커널 모듈 |
| **메타데이터 서버** | 파일 메타데이터 및 잠금 관리 | inodes, MDS | 분산 파일 시스템용 |
| **데이터 서버** | 실제 파일 데이터 저장 | OSD, Data Node | 스토리지 노드 |
| **프로토콜** | 클라이언트-서버 간 통신 규약 | NFS, SMB, AFP | 네트워크 전송 |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ File Storage Architecture ]                             │
└─────────────────────────────────────────────────────────────────────────────┘

[ 전통적 NAS 아키텍처 ]

    ┌─────────────────────────────────────────────────────────────────────┐
    │                          Clients                                     │
    │  ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐     │
    │  │  Linux    │   │  Windows  │   │  macOS    │   │  Container│     │
    │  │  (NFS)    │   │  (SMB)    │   │  (AFP)    │   │  (NFS)    │     │
    │  └─────┬─────┘   └─────┬─────┘   └─────┬─────┘   └─────┬─────┘     │
    └────────┼───────────────┼───────────────┼───────────────┼────────────┘
             │               │               │               │
             └───────────────┴───────┬───────┴───────────────┘
                                     │ TCP/IP Network
                        ┌────────────▼────────────┐
                        │       NAS Appliance      │
                        │  ┌────────────────────┐  │
                        │  │   NAS OS / Ontap   │  │
                        │  ├────────────────────┤  │
                        │  │  Protocol Layer    │  │
                        │  │  [NFS] [SMB] [S3]  │  │
                        │  ├────────────────────┤  │
                        │  │   File System      │  │
                        │  │   WAFL / ZFS       │  │
                        │  │  ┌──────────────┐  │  │
                        │  │  │ /home        │  │  │
                        │  │  │ /shared      │  │  │
                        │  │  │ /backup      │  │  │
                        │  │  └──────────────┘  │  │
                        │  ├────────────────────┤  │
                        │  │  RAID Controller   │  │
                        │  │  - RAID-DP         │  │
                        │  │  - Deduplication   │  │
                        │  │  - Compression     │  │
                        │  └─────────┬──────────┘  │
                        │            │             │
                        │  ┌─────────▼──────────┐  │
                        │  │   HDD/SSD Shelf    │  │
                        │  │  [D1][D2][D3]...   │  │
                        │  └────────────────────┘  │
                        └─────────────────────────┘


[ 클라우드 파일 스토리지 (AWS EFS) 아키텍처 ]

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                            AWS Region                                    │
    │  ┌───────────────────────────────────────────────────────────────────┐  │
    │  │                         VPC                                        │  │
    │  │  ┌──────────────────────┐    ┌──────────────────────┐            │  │
    │  │  │   AZ-1 (Subnet A)    │    │   AZ-2 (Subnet B)    │            │  │
    │  │  │                      │    │                      │            │  │
    │  │  │  ┌────────────────┐  │    │  ┌────────────────┐  │            │  │
    │  │  │  │   EC2 Instance │  │    │  │   EC2 Instance │  │            │  │
    │  │  │  │  mount /efs    │◄─┼────┼─►│  mount /efs    │  │            │  │
    │  │  │  └───────┬────────┘  │    │  └───────┬────────┘  │            │  │
    │  │  │          │           │    │          │           │            │  │
    │  │  │    Mount Target      │    │    Mount Target      │            │  │
    │  │  │    (ENI in Subnet)   │    │    (ENI in Subnet)   │            │  │
    │  │  └──────────┬───────────┘    └──────────┬───────────┘            │  │
    │  │             │                           │                         │  │
    │  │             └───────────┬───────────────┘                         │  │
    │  │                         │                                         │  │
    │  │             ┌───────────▼───────────┐                             │  │
    │  │             │                       │                             │  │
    │  │             │    EFS File System    │                             │  │
    │  │             │                       │                             │  │
    │  │             │  ┌─────────────────┐  │                             │  │
    │  │             │  │   /             │  │                             │  │
    │  │             │  │   ├── data/     │  │                             │  │
    │  │             │  │   ├── logs/     │  │                             │  │
    │  │             │  │   └── shared/   │  │                             │  │
    │  │             │  └─────────────────┘  │                             │  │
    │  │             │                       │                             │  │
    │  │             │  특징:                 │                             │  │
    │  │             │  - POSIX 호환         │                             │  │
    │  │             │  - 자동 스케일링      │                             │  │
    │  │             │  - 다중 AZ 액세스     │                             │  │
    │  │             │  - NFSv4.1 프로토콜   │                             │  │
    │  │             │                       │                             │  │
    │  │             └───────────────────────┘                             │  │
    │  └───────────────────────────────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────────────────────────────┘


[ 파일 시스템 내부 구조: inode 기반 ]

┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ UNIX File System Internal Structure ]                    │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Directory Entry          inode Table              Data Blocks               │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐        │
│  │ /home           │     │ inode #1234     │     │ Block 1000      │        │
│  │  └─ docs        │     │ ┌─────────────┐ │     │ "Hello World..."│        │
│  │     └─ file.txt │────►│ │ mode: 0644  │ │     └─────────────────┘        │
│  │                 │     │ │ uid: 1000   │ │                ▲               │
│  │ filename ───────┼──┐  │ │ gid: 1000   │ │                │               │
│  │ inode: 1234     │  │  │ │ size: 4096  │ │     ┌─────────────────┐        │
│  └─────────────────┘  │  │ │ atime: ...  │ │     │ Block 1001      │        │
│                       │  │ │ mtime: ...  │ │     │ "More data..."  │        │
│                       │  │ │ ctime: ...  │ │     └─────────────────┘        │
│                       │  │ │ blocks: [   │─┼──────►│               │        │
│                       │  │ │  1000,      │ │     │ Block 1002      │        │
│                       │  │ │  1001,      │ │     │ "Even more..."  │        │
│                       │  │ │  1002       │─┼──────►└─────────────────┘        │
│                       │  │ │ ]           │ │                                │
│                       │  │ └─────────────┘ │                                │
│                       │  └─────────────────┘                                │
│                       │                                                     │
│                       └──► filename으로 inode 번호 조회                      │
│                            inode에서 블록 포인터 획득                         │
│                            블록에서 실제 데이터 읽기                          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: NFS 파일 액세스 과정

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    NFS File Access Flow                                     │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ 클라이언트에서 NFS 파일 읽기 ]                                            │
│                                                                            │
│  ① Application                                                             │
│     │  fd = open("/mnt/nfs/data/file.txt", O_RDONLY)                       │
│     ▼                                                                      │
│  ② VFS (Virtual File System)                                              │
│     │  - 마운트 포인트 확인 (/mnt/nfs)                                       │
│     │  - NFS 파일 시스템임을 식별                                            │
│     ▼                                                                      │
│  ③ NFS Client (Kernel Module)                                             │
│     │  - 파일 핸들 요청 (LOOKUP)                                            │
│     │  - RPC (Remote Procedure Call) 생성                                  │
│     │  - Sun RPC + XDR (External Data Representation)                      │
│     ▼                                                                      │
│  ④ Network Layer (TCP/IP)                                                 │
│     │  - NFS 트래픽: 주로 TCP 2049 포트                                     │
│     │  - RPC bind: TCP 111 포트                                            │
│     ▼                                                                      │
│  ⑤ NFS Server                                                             │
│     │  - RPC 요청 수신                                                      │
│     │  - 권한 검사 (export 설정, UID/GID 매핑)                              │
│     │  - 로컬 파일 시스템 액세스                                             │
│     ▼                                                                      │
│  ⑥ Local File System (ext4/XFS)                                           │
│     │  - inode 조회                                                        │
│     │  - 데이터 블록 읽기                                                   │
│     ▼                                                                      │
│  ⑦ NFS Server Response                                                    │
│     │  - 데이터 + 속성 반환                                                 │
│     │  - 캐시 일관성 정보 (ctim, mtim)                                      │
│     ▼                                                                      │
│  ⑧ NFS Client Cache                                                       │
│     │  - attrs cache: 3~60초                                               │
│     │  - data cache: read-ahead                                            │
│     ▼                                                                      │
│  ⑨ Application Receives Data                                              │
│                                                                            │
│  [ NFS 프로시저 주요 목록 ]                                                  │
│                                                                            │
│  NFSv4 Procedures:                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │ Procedure       │ Description                                        │  │
│  ├─────────────────────────────────────────────────────────────────────┤  │
│  │ NULL            │ No operation (ping)                                │  │
│  │ READ            │ Read data from file                                │  │
│  │ WRITE           │ Write data to file                                 │  │
│  │ CREATE          │ Create a regular file                              │  │
│  │ REMOVE          │ Remove a file                                      │  │
│  │ RENAME          │ Rename a file                                      │  │
│  │ LOOKUP          │ Lookup filename                                    │  │
│  │ GETATTR         │ Get file attributes                                │  │
│  │ SETATTR         │ Set file attributes                                │  │
│  │ OPEN            │ Open a file (with locking)                         │  │
│  │ CLOSE           │ Close a file                                       │  │
│  │ LOCK            │ Create a lock                                      │  │
│  │ LOCKT           │ Test for lock                                      │  │
│  │ COMPOUND        │ Combine multiple operations                        │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: NFS 서버 설정 및 마운트

```bash
#!/bin/bash
# NFS 서버 및 클라이언트 구성 스크립트

# ============================================
# NFS Server Configuration (Ubuntu/Debian)
# ============================================

# 1. NFS 서버 패키지 설치
sudo apt-get update
sudo apt-get install -y nfs-kernel-server nfs-common

# 2. 공유 디렉터리 생성
sudo mkdir -p /export/shared
sudo mkdir -p /export/home

# 3. 권한 설정
sudo chown nobody:nogroup /export/shared
sudo chmod 755 /export/shared

# 4. /etc/exports 설정
cat << 'EOF' | sudo tee /etc/exports
# /etc/exports - NFS Export Configuration
#
# Format: directory client(options) client(options) ...
#
# Options:
#   rw              - Read/Write access
#   ro              - Read-only access
#   sync            - Synchronous writes (safer, slower)
#   async           - Asynchronous writes (faster, riskier)
#   no_subtree_check - Disable subtree checking
#   no_root_squash  - Allow root on client to have root access
#   root_squash     - Map root to anonymous (default)
#   anonuid=1000    - Specify anonymous UID
#   anongid=1000    - Specify anonymous GID
#   sec=krb5        - Use Kerberos authentication
#   fsid=0          - Root file system for NFSv4

# NFSv4 root export
/export         192.168.1.0/24(rw,sync,fsid=0,crossmnt,no_subtree_check)

# Specific exports
/export/shared  192.168.1.0/24(rw,sync,no_subtree_check,no_root_squash)
/export/home    192.168.1.0/24(rw,sync,no_subtree_check,root_squash,anonuid=1000,anongid=1000)

# Read-only export for backups
/export/backup  192.168.1.100(ro,sync,no_subtree_check)

# Kerberos authenticated export
/export/secure  *.example.com(rw,sync,sec=krb5)
EOF

# 5. exports 적용
sudo exportfs -ra

# 6. NFS 서버 시작
sudo systemctl enable nfs-kernel-server
sudo systemctl start nfs-kernel-server

# 7. 방화벽 설정 (UFW)
sudo ufw allow from 192.168.1.0/24 to any port nfs
sudo ufw allow from 192.168.1.0/24 to any port 111
sudo ufw allow from 192.168.1.0/24 to any port 2049
sudo ufw allow from 192.168.1.0/24 to any port 20048

# 8. 현재 exports 확인
sudo exportfs -v

# ============================================
# NFS Client Configuration
# ============================================

# 1. NFS 클라이언트 패키지 설치
sudo apt-get install -y nfs-common

# 2. 마운트 포인트 생성
sudo mkdir -p /mnt/nfs/shared
sudo mkdir -p /mnt/nfs/home

# 3. 수동 마운트
sudo mount -t nfs4 -o vers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 \
    nfs-server.example.com:/shared /mnt/nfs/shared

# 4. /etc/fstab 영구 마운트 설정
cat << 'EOF' | sudo tee -a /etc/fstab

# NFS Mounts
nfs-server.example.com:/shared  /mnt/nfs/shared  nfs4  vers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,_netdev  0  0
nfs-server.example.com:/home    /mnt/nfs/home    nfs4  vers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,_netdev  0  0
EOF

# 5. 마운트 옵션 설명
: << 'OPTIONS'
마운트 옵션 상세 설명:

vers=4.1         - NFS 버전 4.1 사용 (세션, 병렬 읽기/쓰기 지원)
rsize=1048576    - 읽기 버퍼 크기 (1MB)
wsize=1048576    - 쓰기 버퍼 크기 (1MB)
hard             - 서버 장애 시 무한 대기 (프로세스 블록)
soft             - 서버 장애 시 타임아웃 후 에러 반환
timeo=600        - 타임아웃 (600 데시초 = 60초)
retrans=2        - 재전송 횟수
noac             - 캐시 비활성화 (강한 일관성 필요 시)
actimeo=30       - 속성 캐시 시간 (초)
_netdev          - 네트워크 필요 장치 표시
OPTIONS

# 6. 마운트 확인
df -hT | grep nfs
mount | grep nfs
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 프로토콜별 특성

| 비교 관점 | NFS v4 | SMB 3.0 | AFP (Apple) | AWS EFS |
|---|---|---|---|---|
| **개발사** | Sun/IETF | Microsoft | Apple | Amazon |
| **주요 플랫폼** | Linux/UNIX | Windows | macOS | AWS |
| **포트** | 2049 | 445 | 548 | 2049 |
| **인증** | Kerberos/SPKM | NTLM/Kerberos | Kerberos | IAM |
| **잠금** | 바이트 범위 잠금 | Oplock/Leasing | AFP 잠금 | NFSv4 잠금 |
| **성능** | 높음 (pNFS) | 높음 (SMB Direct) | 중간 | 중간-높음 |
| **멀티패스** | pNFS | SMB Multichannel | 제한적 | AZ별 MT |
| **암호화** | krb5p | SMB Encryption | AFP over TLS | 전송 중 암호화 |

### 파일 스토리지 vs 블록 vs 오브젝트 비교

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ Storage Type Comparison Matrix ]                         │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                    File Storage (NAS)                                    ││
│  │                                                                         ││
│  │  장점:                                                                   ││
│  │  ✓ 다중 사용자 동시 액세스                                               ││
│  │  ✓ 사용자 친화적 (파일/폴더)                                             ││
│  │  ✓ 기존 앱 호환성 높음                                                   ││
│  │  ✓ 권한 관리 용이                                                        ││
│  │  ✓ 파일 잠금 지원                                                        ││
│  │                                                                         ││
│  │  단점:                                                                   ││
│  │  ✗ 블록보다 지연 시간 높음                                               ││
│  │  ✗ 메타데이터 오버헤드                                                   ││
│  │  ✗ 스케일 아웃 한계                                                      ││
│  │  ✗ 높은 동시성 시 병목                                                   ││
│  │                                                                         ││
│  │  적합: 파일 공유, 홈 디렉터리, CMS, 개발 환경                            ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                    Block Storage (SAN/DAS)                               ││
│  │                                                                         ││
│  │  장점: 최고 성능, 최저 지연, 일관된 IOPS                                 ││
│  │  단점: 공유 어려움, 복잡한 관리                                          ││
│  │  적합: DB, VM, 고성능 앱                                                 ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                    Object Storage (S3)                                   ││
│  │                                                                         ││
│  │  장점: 무제한 확장, 높은 내구성, REST API                                ││
│  │  단점: 높은 지연, eventual consistency, 파일 시스템 아님                  ││
│  │  적합: 백업, 아카이브, 정적 콘텐츠, 빅데이터                             ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 과목 융합 관점 분석

**운영체제(OS)와의 융합**:
- **VFS (Virtual File System)**: 다양한 파일 시스템에 대한 통합 인터페이스
- **페이지 캐시**: NFS 클라이언트의 로컬 캐싱으로 성능 향상
- **inode/dentry 캐시**: 메타데이터 캐싱

**네트워크와의 융합**:
- **RPC (Remote Procedure Call)**: NFS의 통신 기반
- **jumbo frames**: 9000바이트 MTU로 대용량 전송 효율 향상
- **RDMA**: NFS over RDMA로 지연 시간 최소화

**보안(Security)과의 융합**:
- **Kerberos**: 강력한 인증
- **UID/GID 매핑**: NFSv4 idmapd를 통한 사용자 식별
- **SELinux/AppArmor**: 파일 시스템 레벨 접근 통제

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 컨테이너 플랫폼용 공유 스토리지 선택

**문제 상황**: Kubernetes 클러스터에서 여러 Pod가 동일 데이터에 접근해야 함

**기술사의 의사결정 프로세스**:

```yaml
# Kubernetes에서 EFS를 PV로 사용하는 구성

---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: efs-pv
spec:
  capacity:
    storage: 5Gi  # EFS는 무제한이지만 명시 필요
  volumeMode: Filesystem
  accessModes:
    - ReadWriteMany  # RWX - 다중 Pod 동시 접근
  storageClassName: efs-sc
  persistentVolumeReclaimPolicy: Retain
  csi:
    driver: efs.csi.aws.com
    volumeHandle: fs-12345678
    # EFS 액세스 포인트 사용 시
    # volumeHandle: fs-12345678::fsap-abcdefgh
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: efs-pvc
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: efs-sc
  resources:
    requests:
      storage: 5Gi
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: efs-sc
provisioner: efs.csi.aws.com
parameters:
  provisioningMode: efs-ap  # EFS Access Point 자동 생성
  fileSystemId: fs-12345678
  directoryPerms: "700"
  gidRangeStart: "1000"
  gidRangeEnd: "2000"
  basePath: "/dynamic_provisioning"
---
# ReadWriteMany가 필요한 워크로드 예시
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 5  # 5개 Pod가 동일 스토리지 공유
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: nginx
        volumeMounts:
        - name: shared-data
          mountPath: /usr/share/nginx/html
      volumes:
      - name: shared-data
        persistentVolumeClaim:
          claimName: efs-pvc
```

**의사결정 매트릭스**:

| 요구사항 | EBS (Block) | EFS (File) | S3 (Object) |
|---|---|---|---|
| RWX (다중 Pod) | X | O | O (읽기 전용) |
| POSIX 호환 | O | O | X |
| 저지연 | O | △ | X |
| 자동 확장 | X | O | O |
| 비용/GB | 중간 | 높음 | 낮음 |
| **추천** | X | **O** | X |

### 도입 시 고려사항 체크리스트

| 항목 | 확인 사항 | 비고 |
|---|---|---|
| **동시성** | 필요한 동시 연결 수 | NFS: 수천, EFS: 수만 |
| **성능** | 처리량 및 IOPS 요구 | EFS: Burst 가능 |
| **일관성** | 강한/약한 일관성 요구 | NFS: close-to-open |
| **보안** | 인증/인가 방식 | Kerberos vs IAM |
| **백업** | 스냅샷/복구 전략 | EFS: AWS Backup |

### 안티패턴 및 주의사항

**안티패턴 1: 파일 스토리지에 DB 배치**
- 문제: 랜덤 I/O 성능 부족, 잠금 오버헤드
- 해결: DB는 블록 스토리지 사용

**안티패턴 2: 높은 동시성에서 단일 파일 편집**
- 문제: 파일 잠금 병목
- 해결: 파일 분할 또는 DB 사용

**안티패턴 3: 캐시 설정 미조정**
- 문제: actimeo 기본값으로 일관성 문제
- 해결: 워크로드에 맞춘 캐시 설정

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 로컬 파일 시스템 | NAS | 클라우드 EFS |
|---|---|---|---|
| **동시 접속자** | 1 | 수백~수천 | 수만 |
| **확장성** | 제한적 | 중간 | 무제한 |
| **관리 오버헤드** | 낮음 | 중간 | 없음 |
| **비용/GB/월** | $0 (CAPEX) | $0.5-1 | $0.30 |
| **가용성** | 단일 노드 | HA 구성 | 99.999999999% |

### 미래 전망 및 진화 방향

1. **분산 파일 시스템의 발전**: CephFS, GlusterFS, Lustre의 엔터프라이즈 채택 증가
2. **클라우드 네이티브 파일 시스템**: EFS, Azure Files, Google Filestore 확장
3. **하이브리드 파일 시스템**: 온프레미스-클라우드 간 파일 동기화
4. **AI/ML 워크로드 최적화**: 대역폭 집약적 워크로드용 파일 시스템

### ※ 참고 표준/가이드
- **NFS RFC 5661**: NFSv4.1 표준
- **SMB 3.1.1**: Microsoft SMB Protocol
- **POSIX.1**: 파일 시스템 인터페이스 표준
- **AWS EFS Documentation**: 클라우드 파일 시스템 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [블록 스토리지 (Block Storage)](@/studynotes/13_cloud_architecture/03_virt/block_storage.md) : 고성능 블록 단위 스토리지
- [오브젝트 스토리지 (Object Storage)](@/studynotes/13_cloud_architecture/03_virt/object_storage.md) : 무제한 확장 스토리지
- [SDS (Software Defined Storage)](@/studynotes/13_cloud_architecture/03_virt/sds.md) : Ceph, GlusterFS
- [가상화 (Virtualization)](@/studynotes/13_cloud_architecture/03_virt/virtualization.md) : VM 파일 시스템
- [쿠버네티스 PV/PVC](@/studynotes/13_cloud_architecture/01_native/kubernetes.md) : 컨테이너 영구 볼륨

---

### 👶 어린이를 위한 3줄 비유 설명
1. 파일 스토리지는 **'도서관의 서가'**와 같아요. 책(파일)들이 주제별로 정리된 선반(폴더)에 꽂혀 있어요.
2. **'여러 사람이 동시에 도서관을 이용할 수 있어요'**. 친구와 함께 같은 책을 보거나, 각자 다른 책을 볼 수 있어요.
3. 컴퓨터에서는 **'여러 컴퓨터가 같은 파일을 함께 쓸 수 있어요'**. 학교에서 숙제 파일을 공유 폴더에 넣으면 반 친구들이 다 볼 수 있어요!
