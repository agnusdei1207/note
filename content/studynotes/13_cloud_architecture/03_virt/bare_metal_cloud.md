+++
title = "베어메탈 클라우드 (Bare Metal Cloud)"
date = "2026-03-05"
[extra]
categories = "studynotes-cloud"
tags = ["cloud", "bare-metal", "infrastructure", "virtualization", "performance"]
+++

# 베어메탈 클라우드 (Bare Metal Cloud)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 베어메탈 클라우드는 하이퍼바이저 가상화 계층 없이 물리 서버 전체를 고객에게 직접 임대하는 클라우드 서비스 모델로, 가상화 오버헤드를 완전히 제거하여 네이티브 하드웨어 성능을 100% 제공합니다.
> 2. **가치**: 고성능 컴퓨팅(HPC), 대규모 데이터베이스, 실시간 분석 워크로드에서 가상화 대비 20-30% 이상의 성능 향상을 달성하며, 하드웨어 수준의 완전한 격리로 보안 컴플라이언스 요구사항을 충족합니다.
> 3. **융합**: 쿠버네티스와 결합하여 관리형 컨테이너 오케스트레이션을 제공하고, 프라이빗 클라우드와 하이브리드 구성으로 엔터프라이즈 레거시 시스템 마이그레이션의 가교 역할을 수행합니다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의
베어메탈 클라우드(Bare Metal Cloud)는 클라우드 서비스 제공자(CSP)가 가상화 계층(하이퍼바이저) 없이 물리적 서버 하드웨어 전체를 고객에게 독점적으로 할당하고, 이를 클라우드의 핵심 특성인 온디맨드 프로비저닝, API 기반 자동화, 종량제 과금 모델과 결합하여 제공하는 인프라 서비스입니다. 고객은 물리 서버의 CPU, 메모리, 스토리지, 네트워크 카드 등 모든 하드웨어 리소스를 독점적으로 사용할 수 있으며, 운영체제부터 애플리케이션까지 완전한 제어권을 갖습니다.

### 💡 비유
베어메탈 클라우드는 "단독 주택 임대"와 같습니다. 아파트(가상화 VM)가 하나의 건물을 여러 세대가 공유하며 관리비와 규칙을 따라야 하는 반면, 단독 주택은 대지와 건물 전체를 자신만 사용하며, 방 배치, 인테리어, 정원 가꾸기까지 모든 것을 주인 마음대로 할 수 있습니다. 대신 수리와 유지보수의 자유와 책임이 동시에 주어집니다.

### 등장 배경 및 발전 과정

#### 1. 기존 가상화 기술의 성능 한계
- **하이퍼바이저 오버헤드**: Type 1 하이퍼바이저라도 CPU 사이클의 3-5%가 가상화 관리에 소모되며, I/O 집약적 워크로드에서는 15-20% 성능 저하 발생
- **Noisy Neighbor 문제**: 멀티 테넌트 환경에서 인접 VM의 리소스 스파이크가 내 VM 성능에 영향을 미치는 현상
- **특수 하드웨어 접근 제한**: GPU, FPGA, 고성능 NIC(SR-IOV 불가 장비) 등에 직접 접근 어려움

#### 2. 패러다임 변화
- 2014년 SoftLayer(IBM 인수)가 최초로 상용 베어메탈 클라우드 서비스 대중화
- 2018년 AWS EC2 Bare Metal Instances 출시로 메인스트림 CSP 진입
- Oracle Cloud, Azure, Google Cloud 잇달아 베어메탈 옵션 추가

#### 3. 비즈니스적 요구사항
- 금융권 핀테크 시스템의 극저지연(Ultra-Low Latency) 트레이딩 요구
- 빅데이터 분석, AI/ML 학습 워크로드의 폭발적 증가
- 개인정보보호법, 금융보안 규정 등 강제 격리 요구사항 증가

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|-----------|------|
| **BMC (Baseboard Management Controller)** | 서버 원격 관리 칩 | IPMI/iDRAC/iLO 프로토콜로 전원, 센서, 펌웨어 제어 | IPMI 2.0, Redfish API | 집의 스마트 홈 허브 |
| **PXE Boot Server** | 운영체제 네트워크 설치 | DHCP + TFTP로 부트로더 전송, NFS/HTTP로 OS 이미지 로드 | dnsmasq, Cobbler | 이사 짐 트럭 |
| **IPAM (IP Address Management)** | IP 풀 자동 할당 | MAC 주소 기반 정적 바인딩 또는 동적 DHCP 할당 | NetBox, phpIPAM | 우편배송 주소 시스템 |
| **Provisioning API** | 서버 주문/배포 인터페이스 | REST API로 서버 스펙 선택 → BMC 명령 → OS 설치 자동화 | Terraform, OpenStack Ironic | 호텔 체크인 키오스크 |
| **Hardware Inventory DB** | 서버 자산 메타데이터 저장 | CPU 모델, RAM 용량, 디스크 구성, NIC 포트 수 등 추적 | PostgreSQL, Redis | 창고 재고 관리대장 |
| **Network Switch Fabric** | 서버 간 연결망 | Leaf-Spine Clos 토폴로지, 100Gbps 이상 대역폭 | Cumulus Linux, SONiC | 도시 도로망 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          베어메탈 클라우드 아키텍처                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐          │
│   │   고객 포털      │     │   API 게이트웨이  │     │   CLI/SDK       │          │
│   │   (Web Console)  │────▶│   (REST/GraphQL) │◀────│   (Terraform)   │          │
│   └─────────────────┘     └────────┬────────┘     └─────────────────┘          │
│                                    │                                            │
│                                    ▼                                            │
│   ┌────────────────────────────────────────────────────────────────────┐       │
│   │                      Provisioning Orchestration                      │       │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │       │
│   │  │    Ironic    │  │   Inventory  │  │  IPAM/DNS    │               │       │
│   │  │   (OpenStack)│  │   Service    │  │   Service    │               │       │
│   │  └──────┬───────┘  └──────────────┘  └──────────────┘               │       │
│   └─────────┼───────────────────────────────────────────────────────────┘       │
│             │                                                                    │
│   ┌─────────┼───────────────────────────────────────────────────────────┐       │
│   │         │              OOB 관리 네트워크 (Out-of-Band)               │       │
│   │         ▼                                                            │       │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │       │
│   │  │    BMC #1    │  │    BMC #2    │  │    BMC #3    │               │       │
│   │  │   (iDRAC)    │  │    (iLO)     │  │   (IPMI)     │               │       │
│   │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │       │
│   └─────────┼─────────────────┼─────────────────┼───────────────────────┘       │
│             │                 │                 │                                │
│   ┌─────────┼─────────────────┼─────────────────┼───────────────────────┐       │
│   │         │              데이터 네트워크 (In-Band)                     │       │
│   │         ▼                 ▼                 ▼                        │       │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │       │
│   │  │ Bare Metal   │  │ Bare Metal   │  │ Bare Metal   │               │       │
│   │  │  Server #1   │  │  Server #2   │  │  Server #3   │               │       │
│   │  │              │  │              │  │              │               │       │
│   │  │ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │               │       │
│   │  │ │   OS     │ │  │ │   OS     │ │  │ │   OS     │ │               │       │
│   │  │ │(Ubuntu/  │ │  │ │(RHEL/    │ │  │ │(Windows) │ │               │       │
│   │  │ │ RHEL)    │ │  │ │ ESXi)    │ │  │ │          │ │               │       │
│   │  │ └──────────┘ │  │ └──────────┘ │  │ └──────────┘ │               │       │
│   │  │   물리 HW    │  │   물리 HW    │  │   물리 HW    │               │       │
│   │  └──────────────┘  └──────────────┘  └──────────────┘               │       │
│   │                                                                       │       │
│   │  ┌────────────────────────────────────────────────────────────┐     │       │
│   │  │              Leaf-Spine Switch Fabric (100Gbps)             │     │       │
│   │  │    [Leaf Switch] ─── [Spine Switch] ─── [Leaf Switch]       │     │       │
│   │  └────────────────────────────────────────────────────────────┘     │       │
│   └─────────────────────────────────────────────────────────────────────┘       │
│                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────┐      │
│   │                         스토리지 백엔드                               │      │
│   │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │      │
│   │   │  SAN (FC/NVMe)│  │  NAS (NFS)   │  │ Object (S3) │              │      │
│   │   └──────────────┘  └──────────────┘  └──────────────┘              │      │
│   └─────────────────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

#### ① 서버 프로비저닝 7단계 프로세스

```
Step 1: 고객 API 요청
        POST /v1/servers
        {
          "name": "db-prod-01",
          "flavor": "bm.large-metal",
          "os_image": "ubuntu-22.04",
          "network": "private-vlan-100"
        }
                    │
                    ▼
Step 2: 스케줄러 가용 서버 탐색
        - Inventory DB 쿼리: flavor 일치 && 상태=available
        - 네트워크 VLAN 할당 가능성 확인
        - 전력/냉각 용량 확인
                    │
                    ▼
Step 3: BMC를 통한 전원 제어
        - IPMI 명령: ipmitool -H bmc01 -U admin power off
        - BIOS/UEFI 설정을 PXE 부팅으로 변경
        - 전원 켜기: power on
                    │
                    ▼
Step 4: PXE 부팅 & OS 설치
        - DHCP Offer: next-server = tftp.server.ip
        - TFTP 전송: pxelinux.0, kernel, initrd
        - Cloud-init으로 호스트명, 네트워크, SSH 키 주입
                    │
                    ▼
Step 5: OS 부팅 후 구성
        - Ansible/Puppet으로 추가 패키지 설치
        - 모니터링 에이전트 배포
        - 방화벽 규칙 적용
                    │
                    ▼
Step 6: 헬스체크 & 검증
        - ICMP ping 응답 확인
        - SSH 접속 테스트
        - 하드웨어 센서 상태 확인
                    │
                    ▼
Step 7: 고객에게 IP/Credential 전달
        - 이메일/웹콘솔에 접속 정보 표시
        - Billing 시작 (초당 과금)
```

#### ② Ironic (OpenStack Bare Metal) 핵심 로직

```python
# Ironic Conductor의 프로비저닝 상태 머신 (간소화)
class BareMetalProvisioner:
    STATES = [
        'enroll',        # DB에 등록됨
        'manageable',    # BMC 통신 검증됨
        'available',     # 프로비저닝 가능
        'active',        # 고객 사용 중
        'deploying',     # OS 설치 진행
        'deploy failed', # 설치 실패
        'deleting',      # 반환 처리 중
        'cleaning',      # 디스크 와이프 등
        'error'          # 치명 오류
    ]

    def provision_server(self, node, image):
        """베어메탈 서버 프로비저닝 핵심 로직"""
        try:
            # 1. 노드 잠금 획득 (동시성 제어)
            self.acquire_lock(node.uuid)

            # 2. 전원 상태 확인
            power_state = self._bmc_get_power_state(node)
            if power_state != 'off':
                self._bmc_set_power(node, 'off')

            # 3. 부팅 장치를 PXE로 설정
            self._bmc_set_boot_device(node, 'pxe', persistent=False)

            # 4. DHCP 서버에 MAC-IP 바인딩 등록
            self._dhcp_create_reservation(
                mac=node.port.mac_address,
                ip=self._allocate_ip(node),
                hostname=node.name
            )

            # 5. TFTP/iPXE 부트 스크립트 생성
            self._tftp_create_boot_script(
                node=node,
                kernel_url=image.kernel_url,
                initrd_url=image.initrd_url,
                rootfs_url=image.rootfs_url
            )

            # 6. 전원 켜기
            self._bmc_set_power(node, 'on')

            # 7. 콘솔 로그 수집 시작 (디버깅용)
            self._start_console_logging(node)

            # 8. Cloud-Init 완료 대기 (폴링)
            self._wait_for_cloud_init(node, timeout=1800)

            # 9. 헬스체크
            if not self._health_check(node):
                raise ProvisioningError("Health check failed")

            # 10. 상태를 active로 변경
            self._set_provision_state(node, 'active')

        except Exception as e:
            self._set_provision_state(node, 'deploy failed')
            self._send_alert(node, str(e))
            raise
        finally:
            self.release_lock(node.uuid)
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 베어메탈 vs 가상화 VM

| 비교 항목 | 베어메탈 클라우드 | 가상화 VM (IaaS) | 차이 분석 |
|-----------|------------------|-----------------|-----------|
| **CPU 성능** | 100% 네이티브 | 95-97% (VT-x 오버헤드) | HPC에서 3-5% 차이가 결정적 |
| **메모리 접근** | 직접 물리 메모리 | EPT/NPT 변환 계층 존재 | 메모리 대역폭 10-15% 향상 |
| **I/O 성능** | NVMe 직접 접근 | virtio 반가상화 또는 SR-IOV | DB IOPS 20-30% 향상 |
| **네트워크 지연** | < 10μs | 50-100μs (vSwitch 경유) | 초저지연 트레이딩 필수 |
| **프로비저닝 시간** | 5-30분 (OS 설치) | 1-5분 (VM 복제) | 긴급 확장에 불리 |
| **단위 비용** | 시간당 $1-5 | 시간당 $0.1-1 | 5-10배 비쌈 |
| **격리 수준** | 물리적 완전 격리 | 논리적 격리 (VM 경계) | 보안 감사 유리 |
| **이식성** | 하드웨어 종속 | HW 독립적 (이미지) | 마이그레이션 어려움 |
| **신축성** | 제한적 (자원 고정) | 높음 (vCPU/메모리 조절) | 오토스케일링 제약 |
| **관리 복잡도** | 높음 (OS 패치 직접) | 중간 (CSP 관리 영역 존재) | 운영 인력 더 필요 |

### 과목 융합 관점 분석

#### [클라우드 + 운영체제] 메모리 관리 융합
```
베어메탈 클라우드의 OS는 물리 메모리를 직접 관리하므로:
- HugePages (2MB/1GB 페이지) 활용으로 TLB 미스율 90% 감소
- NUMA (Non-Uniform Memory Access) 인식 스케줄링으로 로컬 메모리 접근 극대화
  - 예: 2소켓 서버에서 프로세스를 해당 소켓 메모리에 바인딩
  - 성능 향상: 15-25% (메모리 대역폭 집약적 워크로드)

vs 가상화 VM:
- vNUMA로 게스트 OS에 NUMA 토폴로지 노출
- 하지만 EPT 변환 + vNUMA 매핑 이중 오버헤드
```

#### [클라우드 + 네트워크] DPDK & SR-IOV 융합
```
베어메탈에서의 초고속 패킷 처리:
1. DPDK (Data Plane Development Kit)
   - 커널 바이패스로 사용자 공간에서 NIC 직접 제어
   - 인터럽트 오버헤드 제거 → 폴링 모드 드라이버
   - 결과: 100Gbps 라인레이트 달성, 지연 < 5μs

2. SR-IOV (Single Root I/O Virtualization)
   - 물리 NIC를 여러 VF(Virtual Function)로 분할
   - 베어메탈 OS는 PF(Physical Function)로 전체 제어
   - VM 환경에서는 VF를 개별 VM에 할당

베어메탈의 장점:
- NIC 펌웨어, 드라이버 버전 자유로운 선택
- 커스텀 하드웨어(FPGA, SmartNIC) 직접 프로그래밍 가능
```

#### [클라우드 + 데이터베이스] 일관성 & 성능
```
대규모 RDBMS (Oracle, PostgreSQL)에서 베어메탈 선택 이유:

1. IOPS 예측 가능성
   - VM: 공유 스토리지에서 다른 테넌트의 스파이크가 내 IOPS에 영향
   - 베어메탈: 전용 로컬 NVMe 또는 전용 SAN LUN → 일관된 100K+ IOPS

2. 메모리 버퍼 캐시 효율
   - VM: Ballon Driver가 메모리 회수 시 버퍼 캐시 플러시 발생
   - 베어메탈: OS가 전체 메모리를 DB 버퍼 풀로 100% 활용

3. WAL(Write-Ahead Log) fsync 지연
   - VM: 가상 디스크 계층이 fsync를 캐시 → 정전 시 데이터 손실 위험
   - 베어메탈: 직접 디스크 컨트롤러 쓰기 → ACID Durability 보장

실제 벤치마크 (TPC-C):
- VM (AWS r5.8xlarge): 120,000 tpmC
- 베어메탈 (AWS i3.metal): 180,000 tpmC (+50%)
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 시나리오

#### 시나리오 1: 금융권 초저지연 트레이딩 시스템
```
요구사항:
- 주문 체결 지연 < 100μs (마이크로초)
- 시장 데이터 피드 10Gbps 처리
- 장애 시 1초 이내 페일오버

기술사 판단:
1. 베어메탈 선택 이유:
   - vSwitch 경유 지연(50-100μs) 제거 → 10μs 수준 달성
   - DPDK +用户态协议栈로 커널 오버헤드 제거
   - FPGA 가속카드로 시장 데이터 파싱 하드웨어 오프로드

2. 아키텍처 설계:
   [Market Feed] ──(10Gbps)──▶ [BM Server #1 (Primary)]
                                    │ (MySQL Group Replication)
   [Order Gateway] ◀──(RDMA)──▶ [BM Server #2 (Standby)]

3. 운영 고려사항:
   - 페일오버: Pacemaker + Corosync로 VIP 이동 (<1초)
   - 모니터링: eBPF로 커널 수준 이벤트 추적
   - 백업: 스토리지 스냅샷 + WAL 아카이빙
```

#### 시나리오 2: 대규모 Hadoop/Spark 클러스터
```
요구사항:
- 데이터 웨어하우스 10PB 규모
- 야간 ETL 배치 4시간 내 완료
- 비용 최적화

기술사 판단:
1. 베어메탈 하이브리드 전략:
   - 마스터 노드(NameNode, ResourceManager): VM (관리 편의성)
   - 워커 노드(DataNode, NodeManager): 베어메탈 (로컬 디스크 I/O)

2. 성능 근거:
   - HDFS 로컬 디스크 읽기: 500MB/s (BM) vs 350MB/s (VM)
   - Spark 셔플: NVMe SSD 직접 접근으로 3배 향상
   - 비용: 스팟 베어메탈 활용으로 정가 대비 60% 절감

3. 구성:
   - BM 워커 100대 × 48TB HDD + 2TB NVMe
   - VM 마스터 3대 (HA)
   - 예상 배치 시간: 2.5시간 (VM만 사용 시 6시간)
```

#### 시나리오 3: 보안 규제 준수 데이터베이스
```
요구사항:
- 개인정보 100만 건 이상 처리 시스템
- ISMS-P, GDPR 컴플라이언스
- 연간 2회 외부 침투 테스트

기술사 판단:
1. 베어메탈 선택의 보안적 이유:
   - 하이퍼바이저 탈출(VM Escape) 공격 표면 제거
   - 물리적 격리로 면밀한 접근 통제 가능
   - 전용 HSM(Hardware Security Module) 장착 가능

2. 추가 보안 조치:
   - OS: RHEL with SELinux Enforcing
   - 디스크: LUKS 암호화 + TPM 바인딩
   - 네트워크: MACsec로 계층2 암호화
   - 감사: OS auditd + DB audit log → SIEM 연동

3. 컴플라이언스 매핑:
   - [ISMS-P] 2.9 물리적 환경 보호: 베어메탈 전용 랙
   - [GDPR] Article 32: 적절한 기술적 조치 → 물리적 격리
```

### 도입 시 고려사항 체크리스트

#### 기술적 고려사항
- [ ] **하드웨어 호환성**: OS 지원 드라이버 존재 여부 (특히 NIC, RAID 컨트롤러)
- [ ] **프로비저닝 자동화**: PXE, Cobbler, Ironic 등 OS 설치 파이프라인 구축
- [ ] **RAID 구성**: 하드웨어 RAID 컨트롤러 설정 (RAID-10 권장)
- [ ] **BIOS/UEFI 튜닝**: Hyper-Threading, Turbo Boost, C-State 설정
- [ ] **네트워크 구성**: VLAN 태깅, LACP 본딩, MTU 9000 (Jumbo Frame)

#### 운영/보안적 고려사항
- [ ] **OS 패치 프로세스**: 자동 업데이트 vs 수동 패치 윈도우
- [ ] **백업 전략**: 에이전트 기반 vs 스토리지 스냅샷
- [ ] **모니터링**: IPMI 센서, SMART 데이터, 전력 소비 추적
- [ ] **장애 대응**: 하드웨어 교체 SLA, 예비 부품 확보
- [ ] **폐기 처리**: 디스크 완전 삭제 (DoD 5220.22-M 표준)

### 주의사항 및 안티패턴

#### 안티패턴 1: VM과 동일한 운영 방식 적용
```
잘못된 접근:
- 베어메탈도 스냅샷, 라이브 마이그레이션이 될 것으로 가정
- CSP 관리형 서비스(OS 패치, 백업)에 의존

올바른 접근:
- Immutable Infrastructure: 문제 시 서버 재프로비저닝
- IaC(Terraform)로 OS 구성을 코드화하여 재현성 확보
```

#### 안티패턴 2: 과도한 스펙의 베어메탈 선택
```
잘못된 접근:
- "무조건 성능이 좋으니" 128코어 서버 구매
- 워크로드 분석 없이 최고 사양 선택

올바른 접근:
- Right-Sizing: CPU/메모리/IO 사용률 모니터링 기반 스펙 결정
- 벤치마크: 실제 워크로드로 성능 테스트 후 구매
- 비용-성능 곡선의 무릎(Knee) 지점 찾기
```

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 구분 | 도입 전 (VM) | 도입 후 (BM) | 개선율 |
|-----------|-------------|-------------|--------|
| 트랜잭션 처리량 (TPS) | 50,000 | 75,000 | +50% |
| 평균 응답 지연 (p99) | 50ms | 15ms | -70% |
| IOPS 일관성 (표준편차) | ±15% | ±3% | 안정화 |
| 월간 운영비용 | $10,000 | $8,000 | -20% |
| 보안 감사 소요시간 | 2주 | 3일 | -80% |
| 장애 복구 시간 (RTO) | 30분 | 45분 | -50% (주의) |

### 미래 전망 및 진화 방향

#### 1. 서버리스 베어메탈 (Serverless Bare Metal)
- AWS Elastic Fabric Adapter (EFA) + Fargate 결합
- 컨테이너 기반이지만 물리 서버 수준의 성능 제공
- 예상: 2027년 상용화

#### 2. ARM 기반 베어메탈
- Ampere Altra, AWS Graviton3 물리 서버 옵션
- x86 대비 40% 비용 절감, 와트당 성능 2배
- 예상: ARM 서버 시장 점유율 30% 도달 (2026년)

#### 3. 지속가능한 베어메탈
- 액침 냉각 서버 (PUE 1.05 달성)
- 탄소 배출 실시간 모니터링 및 오프셋
- 규제: EU Taxonomy, RE100 요구사항 충족

### 참고 표준/가이드
- **NIST SP 800-145**: 클라우드 컴퓨팅 정의 (베어메탈 포함)
- **ISO/IEC 17789**: 클라우드 컴퓨팅 아키텍처
- **DMTF Redfish API**: 베어메탈 서버 관리 표준
- **IPMI 2.0**: BMC 통신 프로토콜 표준

---

## 관련 개념 맵 (Knowledge Graph)

1. [하이퍼바이저 (Hypervisor)](./hypervisor.md)
   - 관계: 베어메탈은 하이퍼바이저 계층을 제거하여 오버헤드 없는 성능 제공

2. [IaaS (Infrastructure as a Service)](./iaas.md)
   - 관계: 베어메탈 클라우드는 IaaS의 특수 형태로 물리 서버 제공

3. [하이브리드 클라우드 (Hybrid Cloud)](./hybrid_cloud.md)
   - 관계: 온프레미스 베어메탈과 퍼블릭 VM의 혼합 아키텍처

4. [SR-IOV (Single Root I/O Virtualization)](./sr_iov.md)
   - 관계: 베어메탈에서 NIC를 직접 제어하는 기술

5. [쿠버네티스 (Kubernetes)](./kubernetes.md)
   - 관계: 베어메탈 위에 K8s 클러스터를 직접 배포하여 오버헤드 최소화

6. [옵저버빌리티 (Observability)](./observability.md)
   - 관계: 물리 서버의 IPMI 센서, 전력, 온도 모니터링 필요

---

## 어린이를 위한 3줄 비유 설명

**비유: 단독 주택 vs 아파트**

베어메탈 클라우드는 내 집을 통째로 빌리는 것과 같아요. 아파트(가상화)는 이웃들이 위아래옆집에 살아서 누군가가 시끄럽게 뛰놀면 내 집도 흔들리지만, 단독 주택은 그럴 걱정이 없죠. 대신 고장 나면 내가 직접 수리 기사를 불러야 한다는 책임도 따라와요!

**원리:**
컴퓨터를 누구와도 나누지 않고 혼자 쓰니까, 내가 쓰는 프로그램이 달리기 좋아하는 만큼 최고 속도로 달릴 수 있어요. 하지만 컴퓨터를 켜고 끄고, 고치는 일은 내가 다 해야 해요.

**효과:**
은행이나 큰 회사들은 아주 빠르고 안전하게 일해야 해서 베어메탈을 많이 써요. 내 컴퓨터가 다른 사람 때문에 느려지거나 엿보일 걱정이 없으니까요!
