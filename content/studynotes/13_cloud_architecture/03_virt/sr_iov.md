+++
title = "SR-IOV (Single Root I/O Virtualization)"
date = 2024-05-18
description = "하나의 물리적 PCIe 네트워크 카드를 여러 VM에 논리적으로 직접 매핑해 하이퍼바이저 스위치 오버헤드 우회하는 초고속 I/O 가상화 기술"
weight = 22
[taxonomies]
categories = ["studynotes-13_cloud_architecture"]
tags = ["SR-IOV", "PCIe Virtualization", "VF", "PF", "Network Virtualization", "Low Latency"]
+++

# SR-IOV (Single Root I/O Virtualization)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SR-IOV(Single Root I/O Virtualization)는 단일 PCIe 장치(NIC, GPU, SSD)를 하이퍼바이저 개입 없이 여러 가상 머신(VM)에 직접 할당할 수 있는 논리적 파티션(VF: Virtual Function)으로 나누어, 네이티브에 가까운 I/O 성능과 극저지연(Low Latency)을 제공하는 PCI-SIG 표준 기술입니다.
> 2. **가치**: 네트워크 패킷 처리 성능 95% 향상(10M+ PPS), 지연 시간 80% 감소(<10μs), CPU 오버헤드 90% 절감, 하이퍼바이저 네트워크 스택 우회를 통한 고성능 데이터플레인을 실현합니다.
> 3. **융합**: NFV(Network Function Virtualization), 고빈도 트레이딩(HFT), 실시간 비디오 스트리밍, HPC(고성능 컴퓨팅), AI/ML 추론 클러스터와 결합하여 I/O 바운드 워크로드의 성능을 극대화합니다.

---

## Ⅰ. 개요 (Context & Background)

SR-IOV는 2007년 PCI-SIG에서 표준화된 기술로, 하나의 물리 PCIe 장치(Physical Function, PF)를 여러 개의 가상 장치(Virtual Function, VF)로 분할하여 VM에 직접 할당하는 기술입니다. 기존 가상화 환경에서는 모든 I/O가 하이퍼바이저의 소프트웨어 스위치(Linux Bridge, OVS)를 거쳐야 했는데, 이는 CPU 오버헤드와 지연을 유발했습니다. SR-IOV는 VM이 하드웨어에 직접 접근하여 이러한 오버헤드를 제거합니다.

**💡 비유**: SR-IOV는 **'공항의 전용 게이트'**와 같습니다. 기존에는 모든 승객(패킷)이 중앙 보안 검색대(하이퍼바이저 스위치)를 거쳐야 했습니다. SR-IOV는 각 항공사(VM)에 전용 게이트(VF)를 배정하여, 승객이 중앙 검색대 없이 바로 비행기(네트워크)에 탑승합니다. 처리 속도가 빠르고, 중앙 대기열이 사라집니다.

**등장 배경 및 발전 과정**:
1. **소프트웨어 I/O의 병목**: 가상화 환경에서 모든 패킷이 하이퍼바이저를 거치면서 CPU 소모와 지연 발생.
2. **PCIe 장치 패스스루**: 장치 전체를 VM에 할당하면 다른 VM이 사용 불가. 비효율적.
3. **PCI-SIG 표준화 (2007)**: SR-IOV 1.0 사양 발표.
4. **Intel/Mellanox 채택**: Intel 10GbE NIC, Mellanox InfiniBand에 SR-IOV 기능 탑재.
5. **NFV/5G MEC 필수 기술**: 통신사 가상화에서 초저지연 요구사항 충족.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### SR-IOV 핵심 구성 요소 (표)

| 구성 요소 | 약어 | 상세 역할 | 수량 | 권한 |
|---|---|---|---|---|
| **Physical Function** | PF | 물리 장치의 전체 설정, VF 생성/관리, 하드웨어 리소스 할당 | 1개 per 장치 | Full Configuration |
| **Virtual Function** | VF | VM에 할당되는 경량 가상 장치, 데이터 경로만 담당 | 1~256개 per PF | Data Path Only |
| **IOMMU** | - | DMA 주소 변환, 장치 격리, 메모리 보호 | CPU 내장 | Address Translation |
| **VF Driver** | - | VM 내부에서 실행되는 경량 드라이버 | 1개 per VF | I/O 처리 |
| **PF Driver** | - | 호스트에서 실행되는 관리 드라이버 | 1개 per PF | 장치 관리 |

### SR-IOV vs 기존 네트워크 가상화 비교 (표)

| 비교 항목 | Software Bridge/OVS | PCI Passthrough | SR-IOV |
|---|---|---|---|
| **성능** | 1~3 Mpps | 10~15 Mpps | 10~15 Mpps |
| **지연** | 100~500μs | <10μs | <10μs |
| **CPU 오버헤드** | 높음 (Softirq) | 낮음 | 낮음 |
| **VM 간 공유** | 가능 | 불가능 (1 VM만) | 가능 (VF 분배) |
| **VM 마이그레이션** | 용이 | 불가능 | 제한적 |
| **설정 복잡성** | 낮음 | 중간 | 높음 |

### 정교한 SR-IOV 아키텍처 다이어그램

```ascii
+===========================================================================+
|                    SR-IOV Architecture Overview                           |
|                                                                           |
|  +--------------------------------------------------------------------+  |
|  |                         Virtual Machines                           |  |
|  |                                                                    |  |
|  |  +----------+  +----------+  +----------+  +----------+           |  |
|  |  |   VM1    |  |   VM2    |  |   VM3    |  |   VM4    |           |  |
|  |  | +------+ |  | +------+ |  | +------+ |  | +------+ |           |  |
|  |  | |VF    | |  | |VF    | |  | |VF    | |  | |VF    | |           |  |
|  |  | |Driver| |  | |Driver| |  | |Driver| |  | |Driver| |           |  |
|  |  | +------+ |  | +------+ |  | +------+ |  | +------+ |           |  |
|  |  |   eth0   |  |   eth0   |  |   eth0   |  |   eth0   |           |  |
|  |  +----+-----+  +----+-----+  +----+-----+  +----+-----+           |  |
|  +-------|-------------|-------------|-------------|------------------+  |
|          |             |             |             |                     |
|          |  Direct Hardware Access (No Hypervisor Intervention)        |
|          |             |             |             |                     |
|  +-------|-------------|-------------|-------------|------------------+  |
|  |       v             v             v             v                  |  |
|  |  +-------------------------------------------------------------+   |  |
|  |  |                    SR-IOV Enabled NIC                       |   |  |
|  |  |                                                             |   |  |
|  |  |  +-------------------+                                      |   |  |
|  |  |  | Physical Function |  <-- Host Management                 |   |  |
|  |  |  | (PF)              |      - Create/Destroy VF             |   |  |
|  |  |  | - Full Config     |      - Set VLAN/MAC                  |   |  |
|  |  |  | - VF Management   |      - Statistics                    |   |  |
|  |  |  +--------+----------+                                      |   |  |
|  |  |           |                                                 |   |  |
|  |  |  +--------v----------+  +--------+  +--------+  +--------+ |   |  |
|  |  |  | Virtual Function  |  |  VF1   |  |  VF2   |  |  VF3   | |   |  |
|  |  |  | Pool              |  | Queue  |  | Queue  |  | Queue  | |   |  |
|  |  |  | (Lightweight)     |  | Pair   |  | Pair   |  | Pair   | |   |  |
|  |  |  +-------------------+  +--------+  +--------+  +--------+ |   |  |
|  |  |                                                             |   |  |
|  |  |  Hardware MAC/VLAN Filters per VF                          |   |  |
|  |  |  DMA Engine with IOMMU Translation                         |   |  |
|  |  +-------------------------------------------------------------+   |  |
|  +--------------------------------------------------------------------+  |
|                               |                                          |
|                    +----------v----------+                               |
|                    |  IOMMU (VT-d/AMD-Vi)|                               |
|                    |  DMA Remapping      |                               |
|                    +----------+----------+                               |
|                               |                                          |
|                    +----------v----------+                               |
|                    |  Physical Memory   |                               |
|                    +---------------------+                               |
+===========================================================================+

[Data Path Comparison]
+---------------------------------------------------------------------------+
| Traditional (Software Bridge)                                             |
| VM -> VF Driver -> [VM Exit] -> Hypervisor -> Bridge/OVS -> Physical NIC |
|                 ^^^^^^^^^^^^                    ^^^^^^^^^^                |
|                 Overhead: 1000+ cycles        Overhead: 500+ cycles       |
+---------------------------------------------------------------------------+
| SR-IOV                                                                    |
| VM -> VF Driver -> Direct DMA to Physical NIC                             |
|       ^^^^^^^^                                                            |
|       No Hypervisor Intervention!                                         |
|       Overhead: <100 cycles                                               |
+---------------------------------------------------------------------------+
```

### 심층 동작 원리: SR-IOV 패킷 처리

1. **VF 생성 (VF Creation)**:
   - 호스트 PF 드라이버가 하드웨어에 VF 생성 명령
   - NIC가 VF 리소스(큐 페어, MAC, VLAN) 할당
   - sysfs에 VF 장치 노드 생성 (/sys/class/net/eth0/device/virtfn*)

2. **VF 할당 (VF Assignment)**:
   - libvirt/virt-manager가 VM에 VF 바인딩
   - IOMMU(VT-d)가 VF->VM 메모리 매핑 설정
   - VM 시작 시 VF 장치가 VM에 노출

3. **패킷 수신 (Packet Reception)**:
   - NIC가 수신 패킷을 MAC/VLAN 필터로 VF 식별
   - DMA가 VM 메모리 버퍼에 직접 패킷 기록
   - VF가 VM에 인터럽트 발생 (MSI-X)
   - VM의 VF 드라이버가 패킷 처리

4. **패킷 송신 (Packet Transmission)**:
   - VM의 VF 드라이버가 패킷을 송신 링 버퍼에 배치
   - Doorbell 레지스터 쓰기로 NIC에 알림
   - NIC가 DMA로 패킷 읽어 전송
   - 완료 시 VM에 인터럽트

### 핵심 코드: SR-IOV 구성 (Linux + libvirt)

```bash
# SR-IOV 활성화 및 VF 생성
# Physical NIC: eth0, PF: 0000:01:00.0

# 1. VF 개수 설정 (8개 VF 생성)
echo 8 > /sys/class/net/eth0/device/sriov_numvfs

# 2. VF 확인
ls -la /sys/class/net/eth0/device/virtfn*
# virtfn0 -> ../0000:01:10.0
# virtfn1 -> ../0000:01:10.2
# ...

# 3. VF MAC 주소 설정
ip link set eth0 vf 0 mac 00:11:22:33:44:50
ip link set eth0 vf 1 mac 00:11:22:33:44:51

# 4. VF VLAN 설정
ip link set eth0 vf 0 vlan 100
ip link set eth0 vf 1 vlan 200

# 5. VF를 vfio-pci에 바인딩 (VM 할당용)
modprobe vfio-pci
echo 0000:01:10.0 > /sys/bus/pci/devices/0000:01:10.0/driver/unbind
echo 8086 10ed > /sys/bus/pci/drivers/vfio-pci/new_id
```

```xml
<!-- libvirt VM XML: SR-IOV VF 할당 -->
<domain type='kvm'>
  <name>sr-iov-vm</name>
  <devices>
    <!-- SR-IOV VF 직접 할당 -->
    <hostdev mode='subsystem' type='pci' managed='yes'>
      <driver name='vfio'/>
      <source>
        <address domain='0x0000' bus='0x01' slot='0x10' function='0x0'/>
      </source>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
    </hostdev>

    <!-- MAC 주소 및 VLAN 설정 (네트워크 방식) -->
    <interface type='hostdev'>
      <mac address='00:11:22:33:44:50'/>
      <source>
        <address type='pci' domain='0x0000' bus='0x01' slot='0x10' function='0x0'/>
      </source>
      <vlan>
        <tag id='100'/>
      </vlan>
      <virtualport type='openvswitch'/>
    </interface>
  </devices>
</domain>
```

```python
# Python: SR-IOV VF 관리 스크립트
import os
import subprocess
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class VirtualFunction:
    index: int
    pci_address: str
    mac_address: Optional[str] = None
    vlan_id: Optional[int] = None

class SRIOVManager:
    """SR-IOV VF 관리자"""

    def __init__(self, pf_interface: str):
        self.pf_interface = pf_interface
        self.pf_path = f"/sys/class/net/{pf_interface}/device"

    def create_vfs(self, num_vfs: int) -> bool:
        """VF 생성"""
        try:
            with open(f"{self.pf_path}/sriov_numvfs", "w") as f:
                f.write(str(num_vfs))
            return True
        except IOError as e:
            print(f"VF 생성 실패: {e}")
            return False

    def get_vfs(self) -> List[VirtualFunction]:
        """VF 목록 조회"""
        vfs = []
        vf_pattern = f"{self.pf_path}/virtfn*"

        import glob
        for vf_link in sorted(glob.glob(vf_pattern)):
            index = int(vf_link.split("virtfn")[-1])
            real_path = os.path.realpath(vf_link)
            pci_addr = os.path.basename(real_path)

            vfs.append(VirtualFunction(
                index=index,
                pci_address=pci_addr
            ))

        return vfs

    def set_vf_mac(self, vf_index: int, mac: str) -> bool:
        """VF MAC 주소 설정"""
        try:
            subprocess.run(
                ["ip", "link", "set", self.pf_interface,
                 "vf", str(vf_index), "mac", mac],
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def set_vf_vlan(self, vf_index: int, vlan_id: int) -> bool:
        """VF VLAN 설정"""
        try:
            subprocess.run(
                ["ip", "link", "set", self.pf_interface,
                 "vf", str(vf_index), "vlan", str(vlan_id)],
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def bind_vf_to_vfio(self, pci_address: str) -> bool:
        """VF를 vfio-pci 드라이버에 바인딩"""
        try:
            # 기존 드라이버 언바인딩
            with open(f"/sys/bus/pci/devices/{pci_address}/driver/unbind", "w") as f:
                f.write(pci_address)
        except IOError:
            pass  # 이미 언바인딩됨

        try:
            # vfio-pci에 바인딩
            with open("/sys/bus/pci/drivers/vfio-pci/bind", "w") as f:
                f.write(pci_address)
            return True
        except IOError as e:
            print(f"vfio-pci 바인딩 실패: {e}")
            return False

# 사용 예시
if __name__ == "__main__":
    manager = SRIOVManager("eth0")

    # 8개 VF 생성
    if manager.create_vfs(8):
        print("8개 VF 생성 완료")

        # VF 목록 조회
        for vf in manager.get_vfs():
            print(f"VF{vf.index}: {vf.pci_address}")

            # MAC 및 VLAN 설정
            manager.set_vf_mac(vf.index, f"00:11:22:33:44:5{vf.index}")
            manager.set_vf_vlan(vf.index, 100 + vf.index)
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### SR-IOV 지원 장치 비교

| 장치 유형 | 대표 제품 | 최대 VF | 성능 향상 | 적용 분야 |
|---|---|---|---|---|
| **NIC (1/10/25/100GbE)** | Intel X710, Mellanox ConnectX-5 | 64~128 | 10~20x | NFV, HPC |
| **GPU** | NVIDIA A100, AMD Instinct | 7~16 | 2~5x | AI/ML, VDI |
| **NVMe SSD** | Intel Optane, Samsung PM1733 | 8~32 | 3~5x | DB, 빅데이터 |
| **FPGA** | Intel FPGA, Xilinx Alveo | Variable | 5~10x | 가속기 |

### SR-IOV + DPDK 성능 비교

| 구성 | 패킷 처리량 | 지연 | CPU 사용률 |
|---|---|---|---|
| **Linux Bridge** | 1.2 Mpps | 450μs | 100% (1 core) |
| **OVS** | 1.5 Mpps | 380μs | 95% (1 core) |
| **OVS-DPDK** | 14 Mpps | 50μs | 80% (1 core) |
| **SR-IOV + VF** | 15 Mpps | <10μs | 5% (1 core) |
| **SR-IOV + DPDK** | 45 Mpps | <5μs | 10% (1 core) |

### 과목 융합 관점 분석

- **네트워크와의 융합**: SR-IOV는 네트워크 가상화의 최고 성능 옵션입니다. VLAN 태깅, MAC 필터링이 하드웨어에서 수행되어 오버헤드가 제거됩니다.

- **컴퓨터 구조와의 융합**: IOMMU(VT-d, AMD-Vi)와 결합하여 DMA 주소 변환과 장치 격리를 수행합니다. PCIe TLP(Transaction Layer Packet) 수준에서 가상화가 이루어집니다.

- **보안과의 융합**: IOMMU가 VF의 DMA 접근을 VM 메모리로 제한하여, 악의적인 장치가 다른 VM 메모리에 접근하는 것을 방지합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 통신사 NFV 플랫폼**
- **요구사항**: 5G UPF, 10Mpps 이상, 지연 <50μs
- **기술사의 의사결정**:
  1. Mellanox ConnectX-6 Dx (100GbE, SR-IOV)
  2. VF + DPDK 조합으로 사용자면 처리
  3. OVS-DPDK로 제어면 트래픽 처리
  4. **효과**: 기존 대비 10배 성능 향상

**시나리오 2: 고빈도 트레이딩 (HFT)**
- **요구사항**: 지연 <10μs, 지터 <1μs
- **기술사의 의사결정**:
  1. Solarflare (Xilinx) Low Latency NIC + SR-IOV
  2. Kernel Bypass (Onload) + SR-IOV
  3. CPU Pinning + NUMA 최적화
  4. **효과**: 지연 5μs 달성

### 도입 시 고려사항

- [ ] IOMMU 활성화: BIOS에서 VT-d/AMD-Vi 활성화 필수
- [ ] NIC 호환성: SR-IOV 지원 NIC 확인
- [ ] 드라이버 지원: VF 드라이버가 Guest OS에서 지원되는지 확인
- [ ] VM 마이그레이션: SR-IOV는 라이브 마이그레이션 제한적

### 안티패턴

1. **과도한 VF 생성**: NIC 큐 리소스 한계로 성능 저하. 적정 VF 수 유지.
2. **NUMA 무시**: NIC와 VM이 다른 NUMA 노드에 있으면 성능 저하.
3. **마이그레이션 요구사항 무시**: SR-IOV VM은 라이브 마이그레이션 어려움.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대효과

| 구분 | Software Bridge | SR-IOV | 개선 |
|---|---|---|---|
| **처리량** | 1.5 Mpps | 15 Mpps | 10배 향상 |
| **지연** | 400μs | <10μs | 97% 감소 |
| **CPU 사용** | 100% | 5% | 95% 절감 |
| **패킷 손실** | 0.1% | 0.001% | 100배 감소 |

### 미래 전망

1. **PCIe 6.0/7.0**: 대역폭 확장 (64~128 GT/s)으로 더 높은 I/O 성능
2. **CXL SR-IOV**: CXL 장치의 가상화 지원
3. **SmartNIC + SR-IOV**: 오프로드 기능과 SR-IOV 결합

### ※ 참고 표준
- **PCI-SIG SR-IOV 1.1**: Single Root I/O Virtualization Specification
- **Intel SR-IOV Configuration Guide**: Intel NIC 설정 가이드
- **Mellanox SR-IOV Documentation**: NVIDIA/Mellanox NIC 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [하드웨어 보조 가상화](@/studynotes/13_cloud_architecture/03_virt/hardware_assisted_virtualization.md) : SR-IOV의 기반 기술
- [IOMMU](@/studynotes/13_cloud_architecture/03_virt/iommu.md) : DMA 주소 변환 및 격리
- [DPDK](@/studynotes/13_cloud_architecture/01_native/dpdk.md) : SR-IOV와 결합한 고성능 패킷 처리
- [NFV](@/studynotes/13_cloud_architecture/01_native/nfv.md) : SR-IOV 핵심 적용 분야
- [PCIe](@/studynotes/13_cloud_architecture/03_virt/pcie.md) : SR-IOV의 기반 버스

---

### 👶 어린이를 위한 3줄 비유 설명
1. SR-IOV는 **'전용 게이트'**예요. 공항에서 모든 사람이 중앙 검색대를 거치면 느려요.
2. SR-IOV는 각 항공사에 **'전용 게이트'**를 줘요. 바로 비행기에 탈 수 있어요.
3. 그래서 **'빠르고 편하게'** 여행할 수 있어요. 줄을 설 필요가 없거든요!
