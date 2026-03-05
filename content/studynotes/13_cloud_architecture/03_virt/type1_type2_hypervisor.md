+++
title = "Type 1 vs Type 2 하이퍼바이저"
date = 2026-03-05
description = "하이퍼바이저의 유형인 Type 1(베어메탈)과 Type 2(호스트형)의 아키텍처 차이, 성능 특성, 보안 격리 수준 및 실무 적용 시나리오 심층 분석"
weight = 17
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Hypervisor", "Type1", "Type2", "Bare-metal", "Virtualization", "ESXi", "KVM"]
+++

# Type 1 vs Type 2 하이퍼바이저 아키텍처 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Type 1 하이퍼바이저는 하드웨어 위에 직접 설치되어 오버헤드를 최소화하는 베어메탈 구조이며, Type 2 하이퍼바이저는 호스트 OS 위에서 애플리케이션으로 구동되어 사용 편의성을 제공합니다.
> 2. **가치**: Type 1은 데이터센터급 고성능·고가용성 환경에서 **I/O 처리량 95% 이상 향상** 및 **지연 시간 50% 감소**를 실현하며, Type 2는 개발/테스트 환경에서 빠른 프로토타이핑과 호환성 테스트를 가능하게 합니다.
> 3. **융합**: 하드웨어 보조 가상화(Intel VT-x/AMD-V), SR-IOV, 중첩 가상화(Nested Virtualization) 기술과 결합하여 하이브리드 클라우드 및 컨테이너 기반 인프라로 진화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

하이퍼바이저(Hypervisor)는 물리적 서버의 CPU, 메모리, 스토리지, 네트워크 자원을 논리적으로 분할하여 여러 개의 가상 머신(Virtual Machine, VM)을 동시에 실행할 수 있게 하는 가상화 계층 소프트웨어입니다. 하이퍼바이저는 하드웨어와의 관계에 따라 Type 1(네이티브/베어메탈)과 Type 2(호스트형)로 분류되며, 이러한 구분은 가상화 기술의 성능, 보안, 운영 복잡도에 결정적인 영향을 미칩니다.

**💡 비유**: Type 1 하이퍼바이저는 **'자동차의 엔진 컨트롤 유닛(ECU)'**과 같습니다. 엔진(하드웨어)에 직접 연결되어 연료 분사, 점화 시기 등을 직접 제어하며 최고의 효율을 냅니다. 반면 Type 2 하이퍼바이저는 **'내비게이션 앱'**과 같습니다. 스마트폰(호스트 OS) 위에서 실행되며 운전자에게 경로를 안내하지만, 엔진을 직접 제어하지는 못합니다.

**등장 배경 및 발전 과정**:
1. **메인프레임 시대의 시작 (1960년대)**: IBM의 CP-40/CMS 시스템이 최초의 하이퍼바이저 개념을 도입하여 메인프레임 자원을 시분할로 공유했습니다.
2. **x86 가상화의 도전 (1990년대)**: x86 아키텍처는 가상화를 고려하지 않고 설계되어, 소프트웨어만으로 가상화하는 데 큰 성능 저하(Binary Translation)가 발생했습니다.
3. **하드웨어 보조 가상화의 등장 (2005년~)**: Intel VT-x와 AMD-V 명령어 집합이 도입되면서 CPU 차원에서 가상화를 지원하게 되어, Type 1과 Type 2 모두 비약적인 성능 향상을 이루었습니다.
4. **클라우드 시대의 표준화**: 현재 AWS, Azure, GCP 등 모든 주요 클라우드 프로바이더는 Type 1 하이퍼바이저(KVM, Xen, Hyper-V)를 기반으로 인프라를 구축하고 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 비교 분석표

| 구성 요소 | Type 1 (베어메탈) | Type 2 (호스트형) | 내부 동작 메커니즘 |
|---|---|---|---|
| **설치 위치** | 하드웨어 직접 설치 | 호스트 OS 위에 설치 | Type 1은 BIOS/UEFI 부팅 후 가장 먼저 로드됨 |
| **Ring 레벨** | Ring -1 (Root Mode) | Ring 3 (사용자 모드) | Intel VT-x의 VMX Root/Non-Root 모드 활용 |
| **자원 스케줄링** | 하이퍼바이저 직접 수행 | 호스트 OS 커널 경유 | Type 1은 CPU 슬라이드를 직접 할당 |
| **메모리 관리** | EPT/NPT 직접 제어 | 호스트 OS 가상 메모리 경유 | Extended Page Table 하드웨어 지원 여부 |
| **I/O 경로** | 직접 장치 접근 또는 PV 드라이버 | 호스트 OS 디바이스 드라이버 경유 | I/O 포트, DMA, 인터럽트 처리 방식 차이 |
| **대표 제품** | VMware ESXi, Xen, KVM, Hyper-V | VMware Workstation, VirtualBox, Parallels | 각각의 구현 방식과 라이선스 정책 상이 |

### 정교한 구조 다이어그램: Type 1 vs Type 2 아키텍처

```ascii
================================================================================
                         TYPE 1 (BARE-METAL) HYPERVISOR
================================================================================
+-----------------------------------------------------------------------------+
|                        Virtual Machines (Guests)                             |
|  +----------------+  +----------------+  +----------------+  +------------+ |
|  | Guest OS       |  | Guest OS       |  | Guest OS       |  | Guest OS   | |
|  | (Windows)      |  | (Linux)        |  | (Windows)      |  | (Linux)    | |
|  | App A | App B  |  | App C | App D  |  | App E | App F  |  | App G      | |
|  +--------+-------+  +--------+-------+  +--------+-------+  +------+-----+ |
|           |                   |                   |                 |       |
|  +--------v-------------------v-------------------v-----------------v-----+ |
|  |              Hypervisor (VMware ESXi / KVM / Xen)                     | |
|  |  +------------+  +------------+  +------------+  +----------------+   | |
|  |  | CPU Shed.  |  | Mem Mgr    |  | I/O Stack  |  | Network Stack |   | |
|  |  +------------+  +------------+  +------------+  +----------------+   | |
|  +------------------------------+--+--+--+-------------------------------+ |
|                                 |  |  |  |                               |
+---------------------------------+--+--+--+-------------------------------+
                                  |  |  |  |
================================================================================
                         PHYSICAL HARDWARE (CPU/RAM/DISK/NIC)
================================================================================

================================================================================
                         TYPE 2 (HOSTED) HYPERVISOR
================================================================================
+-----------------------------------------------------------------------------+
|                        Virtual Machines (Guests)                             |
|  +----------------+  +----------------+                                      |
|  | Guest OS       |  | Guest OS       |                                      |
|  | (Linux)        |  | (Windows)      |                                      |
|  | App X | App Y  |  | App Z          |                                      |
|  +--------+-------+  +--------+-------+                                      |
|           |                   |                                              |
|  +--------v-------------------v----------------+  +----------------------+  |
|  |     Hypervisor Process (VirtualBox/etc)     |  | Host Applications   |  |
|  |  +------------+  +------------+             |  | Browser | IDE | ... |  |
|  |  | VM Monitor |  | Emulated   |             |  +----------------------+  |
|  |  |            |  | Hardware   |             |                            |
|  |  +------------+  +------------+             |                            |
|  +---------------------+------------------------+                            |
|                        |                                                   |
|  +---------------------v------------------------+  +----------------------+  |
|  |            Host Operating System             |  | Host Applications   |  |
|  |  +----------+  +----------+  +------------+  |  | Browser | IDE | ... |  |
|  |  | Kernel   |  | Device   |  | File Sys  |  |  +----------------------+  |
|  |  | Scheduler|  | Drivers  |  | (EXT4/NTFS)|  |                            |
|  |  +----------+  +----------+  +------------+  |                            |
|  +---------------------------------------------+                            |
|                        |                                                   |
+------------------------+---------------------------------------------------+
                         |
================================================================================
                         PHYSICAL HARDWARE (CPU/RAM/DISK/NIC)
================================================================================
```

### 심층 동작 원리: VM Exit/Entry 사이클

가상 머신에서 민감한 명령(특권 명령)이 실행될 때 발생하는 VM Exit와 VM Entry 과정을 분석합니다.

1. **Guest 코드 실행**: VM 내부에서 게스트 OS가 I/O 명령(예: `OUT` 명령어)을 실행합니다.
2. **VM Exit 트리거**: CPU가 이 명령어를 가상화 불가능한 특권 명령으로 감지하고 하이퍼바이저로 제어권을 이전합니다.
3. **Exit Reason 분석**: 하이퍼바이저는 VMCS(Virtual Machine Control Structure)의 Exit Reason 필드를 확인하여 어떤 이벤트로 인해 Exit가 발생했는지 파악합니다.
4. **I/O 에뮬레이션**: 하이퍼바이저가 가상 장치 상태를 시뮬레이션하고 실제 하드웨어 또는 에뮬레이트된 장치에 접근합니다.
5. **VM Entry**: 에뮬레이션 완료 후 Guest State를 복원하고 VM으로 제어권을 반환합니다.

**Type 1 vs Type 2의 Exit 처리 차이**:
- **Type 1**: VM Exit → Hypervisor 직접 처리 → VM Entry (최단 경로)
- **Type 2**: VM Exit → Hypervisor 프로세스 → Host Kernel → 디바이스 드라이버 → Host Kernel → Hypervisor 프로세스 → VM Entry (다중 경유)

### 핵심 코드: KVM 하이퍼바이저 커널 모듈 초기화 (Linux Kernel)

```c
// KVM Type 1 하이퍼바이저의 핵심 초기화 코드 (linux/virt/kvm/kvm_main.c)
static int kvm_dev_ioctl_create_vm(unsigned long type)
{
    int r;
    struct kvm *kvm;
    struct file *file;

    // 1. KVM 구조체 할당 및 초기화
    kvm = kvm_create_vm(type);
    if (IS_ERR(kvm))
        return PTR_ERR(kvm);

    // 2. 가상 CPU(vCPU) 생성 준비
    r = kvm_arch_post_init_vm(kvm);
    if (r)
        goto out_err;

    // 3. 메모리 슬롯 및 I/O 레지스터 초기화
    mutex_init(&kvm->lock);
    mutex_init(&kvm->irq_lock);
    mutex_init(&kvm->slots_lock);

    // 4. 파일 디스크립터 생성 (사용자 공간 인터페이스)
    file = anon_inode_getfile("kvm-vm", &kvm_vm_fops, kvm, O_RDWR);
    if (IS_ERR(file)) {
        r = PTR_ERR(file);
        goto out_err;
    }

    // 5. VM 생명주기 관리를 위한 참조 카운팅
    kvm_get_kvm(kvm);
    return file->f_pos ? file->f_pos : r;

out_err:
    kvm_put_kvm(kvm);
    return r;
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 성능 및 리소스 오버헤드

| 비교 지표 | Type 1 (ESXi/KVM) | Type 2 (VirtualBox) | 차이 분석 |
|---|---|---|---|
| **CPU 오버헤드** | 1~3% | 5~15% | Type 2는 호스트 OS 스케줄러를 거치므로 추가 컨텍스트 스위치 발생 |
| **메모리 오버헤드** | 50~200MB (하이퍼바이저 자체) | 500MB~2GB (호스트 OS 포함) | Type 1은 최소한의 관리 코어만 실행 |
| **네트워크 I/O 지연** | 10~50μs | 100~500μs | Type 2는 호스트 네트워크 스택을 2회 경유 |
| **디스크 I/O 처리량** | 네이티브 대비 95~99% | 네이티브 대비 70~85% | 호스트 OS 파일 시스템 오버헤드 |
| **VM 시작 시간** | 1~5초 | 10~30초 | Type 1은 메모리 직접 매핑, Type 2는 파일 기반 |
| **동시 실행 VM 수** | 수백 대 (서버급) | 5~20대 (워크스테이션) | 메모리 관리 및 스케줄링 효율성 차이 |
| **보안 격리 수준** | 하드웨어 수준 격리 | 소프트웨어 수준 격리 | VM Escape 공격에 대한 방어력 차이 |

### 과목 융합 관점 분석: 운영체제 및 보안 연계

- **운영체제(OS)와의 융합**: Type 1 하이퍼바이저는 커널의 스케줄링 알고리즘(CFS, Completely Fair Scheduler)과 유사한 Credit Scheduler(Xen)나 BFS를 자체 구현하여 게스트 OS 간의 공정한 CPU 분배를 수행합니다. 메모리 관리에서는 **Ballooning** 기법을 통해 게스트 OS로부터 미사용 메모리를 회수하여 다른 VM에 재할당합니다.

- **보안(Security)과의 융합**: Type 1은 **Trusted Execution Environment (TEE)**와 결합하여 VM 메모리를 하드웨어 수준에서 암호화(Intel SGX, AMD SEV)할 수 있습니다. 반면 Type 2는 호스트 OS의 커널 익스플로잇이 모든 VM으로 전파될 수 있는 치명적인 보안 취약점을 가집니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 금융권 고빈도 트레이딩 시스템

**문제 상황**: 초당 100만 건 이상의 주문을 처리해야 하는 고빈도 트레이딩(HFT) 시스템에서, 기존 Type 2 기반 개발 환경을 운영 환경으로 이관하려 합니다. 마이크로초 단위의 지연 시간이 수익에 직접적인 영향을 미칩니다.

**기술사의 전략적 의사결정**:
1. **Type 1 + SR-IOV 조합**: VMware ESXi 또는 KVM을 기반으로 하고, SR-IOV를 통해 네트워크 카드를 VM에 직접 패스스루하여 네트워크 스택 오버헤드를 제거합니다.
2. **CPU Pinning (Affinity)**: 특정 vCPU를 물리 CPU 코어에 고정하여 캐시 지역성(Cache Locality)을 극대화하고 컨텍스트 스위치 비용을 최소화합니다.
3. **Huge Pages 활용**: 2MB 또는 1GB Huge Page를 사용하여 TLB(Translation Lookaside Buffer) 미스를 줄이고 메모리 변환 오버헤드를 감소시킵니다.

### 도입 시 고려사항 체크리스트

- **기술적 고려사항**:
  - [ ] 하드웨어 호환성 목록(HCL) 확인 - ESXi는 특정 NIC/RAID 컨트롤러만 지원
  - [ ] NUMA(Non-Uniform Memory Access) 아키텍처 고려 - VM 메모리 할당 시 NUMA 노드 정렬
  - [ ] vMotion/라이브 마이그레이션을 위한 공유 스토리지 구성 (vSAN, NFS, iSCSI)
  - [ ] 고가용성(HA) 및 DRS(Distributed Resource Scheduler) 구성

- **운영/보안적 고려사항**:
  - [ ] VM Escape 취약점(CVE-2020-3950 등)에 대한 정기 패치 정책
  - [ ] 하이퍼바이저 관리 네트워크의 격리 (Out-of-Band Management)
  - [ ] VM 간 통신 모니터링을 위한 가상 스위치 포트 미러링

### 안티패턴 (Anti-patterns)

1. **Overcommitment 남용**: 물리 메모리의 200% 이상을 VM에 할당하면 스와핑이 빈번히 발생하여 성능이 급락합니다. 프로덕션 환경에서는 Overcommit Ratio를 1.2~1.5 이내로 제한해야 합니다.
2. **단일 마스터 노드 구성**: Type 1 클러스터에서 관리 노드를 단일화하면 SPOF(Single Point of Failure)가 발생합니다. 최소 3노드 쿼럼 구성이 필수입니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | Type 1 도입 전 (Type 2) | Type 1 도입 후 | 개선율 |
|---|---|---|---|
| **서버 통합률** | 5:1 (물리서버:VM) | 15:1 | 200% 향상 |
| **전력 소비** | 100% (기준) | 35% | 65% 절감 |
| **VM 밀도** | 10 VM/호스트 | 50 VM/호스트 | 400% 향상 |
| **장애 복구 시간 (RTO)** | 4시간 (수동) | 15분 (자동 HA) | 94% 단축 |

### 미래 전망 및 진화 방향

1. **MicroVM (마이크로VM)**: AWS Firecracker와 같이 125ms 이내에 부팅되는 초경량 VM이 서버리스 및 샌드박스 환경에서 Type 1의 새로운 형태로 진화하고 있습니다.
2. **Confidential Computing**: Intel TDX, AMD SEV-SNP 기술을 통해 VM 메모리가 하이퍼바이저조차 볼 수 없도록 암호화되는 기밀 컴퓨팅이 표준화되고 있습니다.
3. **Disaggregated Infrastructure**: CPU, 메모리, 스토리지가 물리적으로 분리되고 CXL(Compute Express Link)로 연결되는 차세대 아키텍처에서 하이퍼바이저는 자원 풀링의 핵심 제어 계층이 됩니다.

### ※ 참고 표준/가이드

- **ISO/IEC 17203**: OVF(Open Virtualization Format) 표준 - VM 이미지 이식성 규격
- **NIST SP 800-125A**: 하이퍼바이저 보안 가이드라인
- **CIS Benchmark**: VMware ESXi 및 KVM 보안 설정 표준

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [가상화 (Virtualization)](@/studynotes/13_cloud_architecture/03_virt/virtualization.md) : 하이퍼바이저가 구현하는 근본 기술
- [전가상화 vs 반가상화](@/studynotes/13_cloud_architecture/03_virt/virtualization.md) : 하이퍼바이저의 게스트 OS 지원 방식
- [하드웨어 보조 가상화](@/studynotes/13_cloud_architecture/03_virt/hardware_assisted_virtualization.md) : Type 1/2 성능 차이를 좁히는 CPU 기술
- [SR-IOV](@/studynotes/13_cloud_architecture/03_virt/sr_iov.md) : 네트워크 I/O 병목을 해결하는 하드웨어 가상화
- [KVM](@/studynotes/13_cloud_architecture/03_virt/virtualization.md) : 리눅스 커널 기반 Type 1 하이퍼바이저

---

### 👶 어린이를 위한 3줄 비유 설명
1. Type 1 하이퍼바이저는 **'집주인이 직접 관리하는 원룸'**이에요. 집주인이 바로 위층에 살면서 수리와 관리를 직접 해서 문제가 생기면 즉시 해결돼요.
2. Type 2 하이퍼바이저는 **'중개업자가 관리하는 하숙집'**이에요. 하숙집 아주머니(호스트 OS)를 통해서만 방 문제를 해결할 수 있어서 조금 느려요.
3. 큰 회사에서는 빠르고 안전한 Type 1을 쓰고, 집에서 공부할 때는 편한 Type 2를 써요!
