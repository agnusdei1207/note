+++
title = "SDDC (Software Defined Data Center)"
date = 2024-05-18
description = "컴퓨팅, 스토리지, 네트워킹을 모두 가상화하여 API로 프로비저닝하는 소프트웨어 정의 데이터센터"
weight = 23
[taxonomies]
categories = ["studynotes-13_cloud_architecture"]
tags = ["SDDC", "SDN", "SDS", "Virtualization", "VMware", "Private Cloud"]
+++

# SDDC (Software Defined Data Center)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SDDC(Software Defined Data Center)는 데이터센터의 핵심 인프라(컴퓨팅, 스토리지, 네트워킹)를 하드웨어에서 소프트웨어로 추상화하고, API를 통해 프로그래밍 방식으로 프로비저닝, 관리, 운영하는 현대적 데이터센터 아키텍처입니다.
> 2. **가치**: 하드웨어 벤더 종속성(Lock-in) 해소, 자동화된 인프라 프로비저닝(분 단위 배포), 정책 기반 관리(Policy-Driven), TCO 30~50% 절감 효과를 제공합니다.
> 3. **융합**: SDN(Software Defined Networking), SDS(Software Defined Storage), SDC(Software Defined Computing), NFV(Network Function Virtualization)와 결합하여 프라이빗/하이브리드 클라우드의 기반을 구축합니다.

---

## Ⅰ. 개요 (Context & Background)

SDDC(Software Defined Data Center)는 데이터센터의 모든 인프라 요소를 소프트웨어로 정의하고 제어하는 아키텍처입니다. 기존 데이터센터는 서버, 스토리지, 네트워크 장비가 하드웨어 중심으로 구성되어 수동 설정과 벤더 종속성이 심각했습니다. SDDC는 이를 "소프트웨어 계층"으로 추상화하여, 인프라를 코드(IaC)처럼 관리할 수 있게 합니다. VMware가 2012년 처음 제안했으며, 현재 프라이빗 클라우드와 하이브리드 클라우드의 핵심 아키텍처로 자리잡았습니다.

**💡 비유**: SDDC는 **'스마트홈 자동화 시스템'**과 같습니다. 기존 집은 조명, 난방, 블라인드를 각각 수동으로 제어해야 했습니다. SDDC는 모든 기기를 중앙 제어 시스템(소프트웨어)에 연결하고, 스마트폰 앱(API) 하나로 "영화 모드" 버튼 한 번에 조명을 어둡게, 블라인드를 내리고, 프로젝터를 켭니다. 집주인은 배선이 어떻게 연결되었는지 알 필요 없이 원하는 상태만 선언하면 됩니다.

**등장 배경 및 발전 과정**:
1. **하드웨어 중심 데이터센터의 한계**: 서버 증설, 네트워크 설정, 스토리지 할당이 수동 작업에 의존하여 주 단위 소요.
2. **가상화 기술의 성숙**: 서버 가상화(VMware vSphere)의 성공이 스토리지, 네트워크로 확장됨.
3. **클라우드 경쟁력 확보**: AWS 등 퍼블릭 클라우드의 민첩성을 온프레미스에서도 구현 필요.
4. **VMware SDDC 출시**: 2012년 VMware가 vSphere + NSX + vSAN + vRealize를 통합한 SDDC 스택 발표.
5. **하이퍼컨버지드로 진화**: Dell EMC VxRail, Nutanix 등이 SDDC를 어플라이언스 형태로 패키징.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### SDDC 핵심 구성 요소 (표)

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/제품 | 비유 |
|---|---|---|---|---|
| **SDC (Software Defined Compute)** | 서버 가상화, VM/컨테이너 관리 | 하이퍼바이저가 CPU/메모리를 VM에 할당 | VMware vSphere, KVM, Hyper-V | 가상 PC |
| **SDS (Software Defined Storage)** | 스토리지 풀링, 정책 기반 할당 | 분산 스토리지 소프트웨어가 디스크를 논리 풀로 통합 | VMware vSAN, Ceph, GlusterFS | 가상 하드디스크 |
| **SDN (Software Defined Networking)** | 네트워크 가상화, 프로그래밍 가능 | 컨트롤러가 흐름(Flow) 규칙을 스위치에 배포 | VMware NSX, Cisco ACI, OpenFlow | 가상 공유기 |
| **SDDC Management** | 통합 관리, 자동화, 모니터링 | API 기반 프로비저닝, 정책 엔진 | VMware vRealize, OpenStack | 스마트홈 앱 |
| **Security & Policy** | 마이크로 세그멘테이션, 규정 준수 | 분산 방화벽, 암호화, 접근 제어 | NSX Distributed Firewall | 보안 시스템 |

### SDDC 아키텍처 계층 (표)

| 계층 | 구성 | 역할 | API/프로토콜 |
|---|---|---|---|
| **Physical Layer** | x86 서버, ToR 스위치, 스토리지 | 물리적 자원 제공 | PXE, LLDP, SNMP |
| **Virtualization Layer** | ESXi, KVM, Hyper-V | 하드웨어 추상화 | vSphere API, libvirt |
| **Software Defined Layer** | vSAN, NSX, vCenter | 리소스 풀링 및 서비스 | REST API, gRPC |
| **Cloud Management Platform** | vRealize, OpenStack | 셀프 서비스, 카탈로그 | REST API, Terraform |
| **Application Layer** | VM, 컨테이너, 함수 | 비즈니스 로직 실행 | Kubernetes API |

### 정교한 SDDC 아키텍처 다이어그램

```ascii
+==========================================================================+
|                    CLOUD MANAGEMENT PLATFORM (CMP)                       |
|  +----------------+  +----------------+  +----------------+              |
|  | Self-Service   |  | Policy Engine  |  | Automation     |              |
|  | Portal         |  | (Governance)   |  | (vRealize)     |              |
|  +-------+--------+  +-------+--------+  +-------+--------+              |
|          |                   |                   |                       |
|          +-------------------+-------------------+                       |
|                              |                                           |
|                    +---------v---------+                                 |
|                    |   Unified API     |                                 |
|                    |  (REST/GraphQL)   |                                 |
|                    +---------+---------+                                 |
+==============================|============================================+
                               |
+==============================v============================================+
|                    SOFTWARE DEFINED INFRASTRUCTURE                        |
|                                                                           |
|  +-------------------------+  +-------------------------+                 |
|  |    SDS (Storage)        |  |    SDN (Networking)     |                 |
|  | +---------------------+ |  | +---------------------+ |                 |
|  | | Storage Policy Mgr  | |  | | Network Controller  | |                 |
|  | | (vSAN/CEF)          | |  | | (NSX Manager)       | |                 |
|  | +----------+----------+ |  | +----------+----------+ |                 |
|  |            |            |  |            |            |                 |
|  | +----------v----------+ |  | +----------v----------+ |                 |
|  | | Distributed Storage | |  | | Logical Switches    | |                 |
|  | | (Object/Block/File) | |  | | Routers/Firewalls   | |                 |
|  | +---------------------+ |  | +---------------------+ |                 |
|  +-------------------------+  +-------------------------+                 |
|                                                                           |
|  +--------------------------------------------------------------------+  |
|  |                    SDC (Compute - Hypervisor)                       |  |
|  |  +------------+  +------------+  +------------+  +------------+     |  |
|  |  | ESXi Host  |  | ESXi Host  |  | ESXi Host  |  | ESXi Host  |     |  |
|  |  | +--------+ |  | +--------+ |  | +--------+ |  | +--------+ |     |  |
|  |  | | VM VM  | |  | | VM VM  | |  | | VM VM  | |  | | VM VM  | |     |  |
|  |  | +--------+ |  | +--------+ |  | +--------+ |  | +--------+ |     |  |
|  |  +-----+------+  +-----+------+  +-----+------+  +-----+------+     |  |
|  +--------|--------------|---------------|---------------|------------+  |
+===========|==============|===============|===============|===============+
            |              |               |               |
+===========|==============|===============|===============|===============+
|           v              v               v               v              |
|  +---------------+  +---------------+  +---------------+  +---------------+
|  | ToR Switch    |  | ToR Switch    |  | ToR Switch    |  | ToR Switch    |
|  +-------+-------+  +-------+-------+  +-------+-------+  +-------+-------+
|          |                  |                  |                  |       |
|  +-------v------------------v------------------v------------------v-------+
|  |                    Physical Network (Spine-Leaf)                     |
|  +----------------------------------------------------------------------+
+==========================================================================+

[Data Flow: VM Creation Request]
1. User -> Portal: "Create VM (4 vCPU, 16GB RAM, 100GB Disk)"
2. Portal -> Policy Engine: Check quota, compliance
3. Policy Engine -> Automation: Select optimal host
4. Automation -> vCenter: Provision VM via API
5. vCenter -> ESXi: Create VM, allocate resources
6. NSX -> Logical Switch: Attach VM to network
7. vSAN -> Storage Pool: Allocate 100GB from pool
8. Result: VM ready in < 5 minutes (vs 2 weeks manual)
```

### 심층 동작 원리: SDDC 프로비저닝 파이프라인

1. **요청 수신 (Request Intake)**:
   - 셀프 서비스 포털 또는 API를 통해 VM 생성 요청
   - 템플릿, 사양(vCPU, 메모리, 디스크), 네트워크 요구사항 포함

2. **정책 검증 (Policy Validation)**:
   - 사용자 권한, 부서 쿼터, 규정 준수 여부 확인
   - 승인 워크플로우(필요 시) 실행

3. **리소스 스케줄링 (Resource Scheduling)**:
   - DRS(Distributed Resource Scheduler)가 최적 호스트 선정
   - CPU, 메모리, 스토리지, 네트워크 가용성 고려
   - Anti-Affinity 규칙(고가용성) 적용

4. **컴퓨팅 프로비저닝 (Compute Provisioning)**:
   - vCenter가 ESXi 호스트에 VM 생성 명령
   - VM 템플릿 복제 또는 ISO 부팅
   - vCPU, 메모리 할당

5. **스토리지 프로비저닝 (Storage Provisioning)**:
   - vSAN이 스토리지 정책(SPBM)에 따라 디스크 할당
   - 복제본 수(Raid Level), 장애 도메인, 캐시 정책 적용
   - 스토리지 IOPS 제한 설정

6. **네트워크 프로비저닝 (Network Provisioning)**:
   - NSX가 논리 스위치, 라우터, 방화벽 생성
   - 마이크로 세그멘테이션 규칙 적용
   - Load Balancer, NAT 규칙 설정

7. **보안 적용 (Security Enforcement)**:
   - 게스트 OS 방화벽, 바이러스 백신 에이전트 배포
   - 암호화(Storage at-rest, Network in-transit) 적용

8. **모니터링 등록 (Monitoring Registration)**:
   - vRealize Operations에 VM 등록
   - 알람 임계값, 대시보드 구성

### 핵심 코드: SDDC 프로비저닝 자동화 (Terraform + vSphere)

```hcl
# SDDC VM 프로비저닝 - Infrastructure as Code

# vSphere Provider 설정
provider "vsphere" {
  user                 = var.vsphere_user
  password             = var.vsphere_password
  vsphere_server       = var.vsphere_server
  allow_unverified_ssl = true
}

# 데이터 소스 - vSphere 객체 참조
data "vsphere_datacenter" "dc" {
  name = "SDDC-DataCenter"
}

data "vsphere_resource_pool" "pool" {
  name          = "Production/Resources"
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_datastore" "datastore" {
  name          = "vSAN-Datastore"
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_network" "network" {
  name          = "Production-VXLAN"
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_virtual_machine" "template" {
  name          = "ubuntu-22.04-template"
  datacenter_id = data.vsphere_datacenter.dc.id
}

# VM 리소스 정의
resource "vsphere_virtual_machine" "web_server" {
  count            = var.instance_count
  name             = "web-server-${count.index + 1}"
  resource_pool_id = data.vsphere_resource_pool.pool.id
  datastore_id     = data.vsphere_datastore.datastore.id

  # CPU 및 메모리 할당 (SDC)
  num_cpus = 4
  memory   = 16384  # 16GB

  # 네트워크 인터페이스 (SDN - NSX)
  network_interface {
    network_id   = data.vsphere_network.network.id
    adapter_type = "vmxnet3"
  }

  # 디스크 할당 (SDS - vSAN)
  disk {
    label            = "disk0"
    size             = 100  # 100GB
    thin_provisioned = true
    # vSAN 스토리지 정책: FTT=1, RAID-1
    storage_policy_id = "vSAN Default Storage Policy"
  }

  # 추가 데이터 디스크
  disk {
    label            = "disk1"
    size             = 500  # 500GB
    unit_number      = 1
    thin_provisioned = true
  }

  # VM 템플릿 복제
  clone {
    template_uuid = data.vsphere_virtual_machine.template.id

    customize {
      linux_options {
        host_name = "web-server-${count.index + 1}"
        domain    = "sddc.local"
      }

      network_interface {
        ipv4_address = "10.0.1.${10 + count.index}"
        ipv4_netmask = 24
      }

      ipv4_gateway    = "10.0.1.1"
      dns_server_list = ["10.0.1.2", "10.0.1.3"]
      dns_suffix_list = ["sddc.local"]
    }
  }

  # 태그 (태그 기반 관리)
  tags = [
    "terraform",
    "web-tier",
    "production"
  ]
}

# NSX 논리적 방화벽 규칙 (SDN Security)
resource "nsxt_policy_security_policy" "web_policy" {
  display_name = "Web-Tier-Security-Policy"
  description  = "Micro-segmentation for web servers"
  category     = "Application"

  rule {
    display_name       = "Allow-HTTP-HTTPS"
    source_groups      = [nsxt_policy_group.any.id]
    destination_groups = [nsxt_policy_group.web_servers.id]
    services           = [nsxt_policy_service.http.id, nsxt_policy_service.https.id]
    action             = "ALLOW"
    logged             = true
  }

  rule {
    display_name       = "Deny-All-Other"
    source_groups      = [nsxt_policy_group.any.id]
    destination_groups = [nsxt_policy_group.web_servers.id]
    services           = [nsxt_policy_service.any.id]
    action             = "DROP"
    logged             = true
  }
}

# vSAN 스토리지 정책 (SDS)
resource "vsphere_storage_policy" "gold_tier" {
  name        = "Gold-Storage-Policy"
  description = "High performance storage with FTT=2"

  # vSAN 규칙
  rule {
    capability = "vSAN.hostFailuresToTolerate"
    value      = "2"  # 2개 호스트 장애까지 허용
  }

  rule {
    capability = "vSAN.replicaPreference"
    value      = "raid1"  # RAID-1 미러링
  }

  rule {
    capability = "vSAN.checksumDisabled"
    value      = "false"  # 체크섬 활성화
  }

  rule {
    capability = "vSAN.iopsLimit"
    value      = "5000"  # 최대 5000 IOPS
  }
}
```

### SDDC vs Traditional Data Center 비교

| 비교 항목 | Traditional DC | SDDC | 개선 효과 |
|---|---|---|---|
| **VM 프로비저닝** | 2주~2개월 | 5분~1시간 | 99% 단축 |
| **네트워크 변경** | 수동 CLI, 1주일 | API, 1분 | 99.9% 단축 |
| **스토리지 확장** | 새 하드웨어 구매 | 소프트웨어 확장 | 80% 비용 절감 |
| **장애 복구** | 수동 복구, 4시간 | 자동 장애 조치, 5분 | 98% 단축 |
| **운영 인력** | 100명 | 20명 | 80% 절감 |
| **자원 활용률** | 15% | 70% | 4.7배 향상 |

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### SDDC 구현체 비교

| 제품 | 벤더 | 특징 | 적합 시나리오 |
|---|---|---|---|
| **VMware SDDC** | VMware | vSphere + NSX + vSAN + vRealize, 가장 성숙 | 엔터프라이즈, 프라이빗 클라우드 |
| **Nutanix** | Nutanix | HCI 기반, AHV 하이퍼바이저, Prism 관리 | 중견기업, VDI |
| **Dell EMC VxRail** | Dell/EMC | VMware 기반 HCI, 통합 하드웨어 | 대규모 프라이빗 클라우드 |
| **HPE Synergy** | HPE | Composable Infrastructure, 하드웨어 중심 | 레거시+가상화 혼합 |
| **OpenStack** | 오픈소스 | Neutron(SDN) + Cinder(SDS) + Nova(SDC) | 비용 절감, 커스터마이징 |

### 과목 융합 관점 분석

- **네트워크와의 융합**: SDN(OpenFlow, VXLAN, NVGRE)이 SDDC의 핵심으로, 네트워크 장비를 소프트웨어로 제어합니다. NSX, Cisco ACI가 대표적입니다.

- **데이터베이스와의 융합**: SDS 위에 DB를 배포하여 스토리지 IOPS를 정책 기반으로 할당합니다. vSAN의 스토리지 정책이 DB 성능을 보장합니다.

- **보안과의 융합**: 마이크로 세그멘테이션으로 VM 간 동서 트래픽을 격리합니다. NSX Distributed Firewall이 하이퍼바이저 레벨에서 방화벽을 실행합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 금융권 프라이빗 클라우드 구축**
- **요구사항**: 100% 온프레미스, 규제 준수, 5,000 VM 운영
- **기술사의 의사결정**:
  1. VMware SDDC 채택 (가장 성숙, 규제 준수 용이)
  2. vSphere + NSX-V + vSAN + vRealize Automation
  3. vSAN All-Flash로 DB 성능 보장
  4. NSX 마이크로 세그멘테이션으로 테넌트 격리
  5. **예상 TCO**: 기존 대비 40% 절감

**시나리오 2: 제조업 스마트 팩토리**
- **요구사항**: 3개 공장, 지연 <10ms, OT/IT 통합
- **기술사의 의사결정**:
  1. Nutanix HCI로 각 공장에 엣지 클러스터
  2. Prism Central로 3개 공장 통합 관리
  3. Calm으로 애플리케이션 자동 배포
  4. **효과**: 운영 인력 50% 절감

### 도입 시 고려사항 (체크리스트)

**기술적 체크리스트**:
- [ ] 기존 하드웨어 호환성: 벤더 인증 목록 확인
- [ ] 네트워크 스위치: VXLAN, EVPN 지원 여부
- [ ] 스토리지 성능: IOPS, 지연, 복제 정책
- [ ] DR/BC: 사이트 간 복제, RTO/RPO 목표

### 주의사항 및 안티패턴

1. **오버프로비저닝**: SDDC의 유연성 때문에 자원 낭비 발생. Quota, Chargeback 필수.
2. **벤더 종속**: VMware SDDC는 강력하지만 Lock-in 위험. 멀티 클라우드 전략 고려.
3. **네트워크 병목**: SDN 오버레이의 캡슐화 오버헤드. 하드웨어 VTEP 고려.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | Traditional DC | SDDC | 개선율 |
|---|---|---|---|
| **프로비저닝 시간** | 2주 | 5분 | 99.9% 단축 |
| **운영 비용** | $100/VM/월 | $40/VM/월 | 60% 절감 |
| **가용성** | 99.9% | 99.999% | 100배 향상 |
| **자원 활용률** | 15% | 70% | 4.7배 |

### 미래 전망

1. **SDDC + AI**: AI 기반 리소스 최적화, 이상 탐지
2. **Hyperconverged dominance**: HCI가 SDDC의 표준 하드웨어 형태로 정착
3. **Multi-Cloud SDDC**: VMware Cloud on AWS, Azure VMware Solution으로 확장

### ※ 참고 표준/가이드
- **VMware SDDC Architecture**: VMware Validated Designs (VVD)
- **NIST SP 800-145**: Cloud Computing Reference Architecture
- **ISO/IEC 17788**: Cloud Computing Overview and Vocabulary

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [SDN (Software Defined Networking)](@/studynotes/13_cloud_architecture/03_virt/sdn.md) : SDDC의 네트워크 가상화
- [HCI (Hyper-Converged Infrastructure)](@/studynotes/13_cloud_architecture/03_virt/hci.md) : SDDC의 통합 하드웨어 플랫폼
- [프라이빗 클라우드](@/studynotes/13_cloud_architecture/03_virt/private_cloud.md) : SDDC 기반 클라우드
- [IaC (Infrastructure as Code)](@/studynotes/13_cloud_architecture/01_native/iac.md) : SDDC 프로비저닝 자동화
- [마이크로 세그멘테이션](@/studynotes/13_cloud_architecture/03_virt/micro_segmentation.md) : SDDC 보안 기법

---

### 👶 어린이를 위한 3줄 비유 설명
1. SDDC는 **'스마트홈 시스템'**과 같아요. 집의 모든 기기(조명, 난방, TV)를 앱(API) 하나로 제어해요.
2. 기존에는 각 기기를 **'직접 만져야 했지만'**, 이제는 "영화 모드!"라고 말하면 자동으로 설정돼요.
3. 그래서 집주인은 **'복잡한 배선을 몰라도'** 편하게 살 수 있어요. 고장 나도 시스템이 자동으로 알려줘요.
