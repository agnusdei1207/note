+++
title = "SDS (Software Defined Storage)"
date = 2024-05-18
description = "범용 x86 서버 하드웨어를 묶어 분산 가상화 소프트웨어를 통해 하나의 스토리지 풀로 운영하는 소프트웨어 정의 스토리지"
weight = 25
[taxonomies]
categories = ["studynotes-13_cloud_architecture"]
tags = ["SDS", "Software Defined Storage", "Distributed Storage", "Ceph", "vSAN", "GlusterFS"]
+++

# SDS (Software Defined Storage)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SDS(Software Defined Storage)는 전용 스토리지 하드웨어(EMC, NetApp 등) 대신 범용 x86 서버와 분산 소프트웨어를 결합하여, 확장 가능하고 유연하며 비용 효율적인 통합 스토리지 풀을 제공하는 아키텍처입니다.
> 2. **가치**: 스토리지 비용 50~70% 절감, 선형 확장성(Scale-Out), 하드웨어 벤더 독립(Lock-in 해소), 정책 기반 데이터 관리, 다중 프로토콜 지원(Block/File/Object)을 실현합니다.
> 3. **융합**: 컨테이너 스토리지(CSI), 하이퍼바이저(vSAN), 클라우드 네이티브 애플리케이션, 빅데이터 분석, AI/ML 워크로드와 결합하여 유연한 데이터 플랫폼을 구축합니다.

---

## Ⅰ. 개요 (Context & Background)

SDS(Software Defined Storage)는 스토리지 기능(RAID, 복제, 스냅샷, 계층화, 중복 제거)을 하드웨어에서 소프트웨어 계층으로 이동시킨 아키텍처입니다. 기존 스토리지는 EMC VMAX, NetApp FAS 같은 전용 하드웨어 어플라이언스에 의존했으나, 이는 높은 비용과 벤더 종속(Lock-in), 확장 한계를 가졌습니다. SDS는 범용 서버의 로컬 디스크(HDD/SSD/NVMe)를 논리적으로 묶어 하나의 거대한 스토리지 풀로 관리합니다.

**💡 비유**: SDS는 **'공용 주차장'**과 같습니다. 기존에는 각 빌딩마다 전용 주차장(전용 스토리지)을 지어야 했습니다. 하지만 공용 주차장(SDS)은 여러 빌딩이 공유하며, 차(데이터)가 늘어나면 주차장을 확장하면 됩니다. 또한, VIP 차량은 1층(SSD), 일반 차량은 지하(HDD)에 주차하는 식으로 정책 기반 관리가 가능합니다.

**등장 배경 및 발전 과정**:
1. **전용 스토리지의 비효율**: EMC, NetApp 장비는 초기 비용 수억 원, 확장 시 새 어플라이언스 구매 필요.
2. **데이터 폭증**: 2010년대 들어 연 40% 성장하는 데이터를 전용 장비로 감당 불가.
3. **오픈소스 성숙**: Ceph(2006), GlusterFS(2011), OpenStack Swift가 엔터프라이즈급 안정성 확보.
4. **하이퍼바이저 통합**: VMware vSAN(2014)이 vSphere에 스토리지 기능을 내장.
5. **NVMe 혁신**: 고속 NVMe SSD와 SDS 결합으로 All-Flash 배열 대체 가능.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### SDS 핵심 구성 요소 (표)

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/제품 | 비유 |
|---|---|---|---|---|
| **스토리지 컨트롤러** | 데이터 배치, 복제, 복구 관리 | CRUSH 알고리즘, 일관성 해시 | Ceph MON, vSAN DOM | 주차관리소 |
| **데이터 플레인** | 실제 데이터 저장 및 읽기/쓰기 | 오브젝트/블록/파일 인터페이스 | Ceph OSD, vSAN DS | 주차 구역 |
| **메타데이터 서버** | 파일 시스템 메타데이터 관리 | 분산 메타데이터, 캐싱 | Ceph MDS, Gluster DHT | 주차 위치 안내판 |
| **스토리지 인터페이스** | 다양한 프로토콜 지원 | RBD, CephFS, S3, NFS, iSCSI | RGW, CephFS, NFS-Ganesha | 주차 입구 |
| **관리/모니터링** | 용량, 성능, 상태 관리 | REST API, Prometheus Exporter | Ceph Dashboard, vCenter | 관제실 |

### SDS 아키텍처 유형 (표)

| 유형 | 설명 | 장점 | 단점 | 대표 제품 |
|---|---|---|---|---|
| **하이퍼바이저 내장형** | 가상화 플랫폼에 통합 | 배포 간편, 가상화와 최적화 | 가상화 플랫폼 종속 | vSAN, Nutanix |
| **컨테이너 네이티브형** | Kubernetes CSI 기반 | 컨테이너 친화적, 동적 프로비저닝 | 규모 제한, 복잡성 | Rook-Ceph, OpenEBS |
| **스탠드얼론형** | 별도 클러스터 | 유연성, 하드웨어 독립 | 운영 복잡성 | Ceph, MinIO |
| **하이퍼컨버지드형** | 컴퓨팅+스토리지 통합 | 단순한 확장, TCO 절감 | 규모 경제 한계 | Nutanix, SimpliVity |

### 정교한 Ceph SDS 아키텍처 다이어그램

```ascii
+===========================================================================+
|                        Ceph Storage Cluster                               |
|                                                                           |
|  +--------------------------------------------------------------------+  |
|  |                      Clients (Access Layer)                        |  |
|  |  +----------+  +----------+  +----------+  +----------+            |  |
|  |  | RBD      |  | CephFS   |  | RGW      |  | iSCSI    |            |  |
|  |  | (Block)  |  | (File)   |  | (Object) |  | Gateway  |            |  |
|  |  +----+-----+  +----+-----+  +----+-----+  +----+-----+            |  |
|  +-------|-------------|-------------|-------------|------------------+  |
|          |             |             |             |                     |
|          v             v             v             v                     |
|  +--------------------------------------------------------------------+  |
|  |                    RADOS (Reliable Autonomic Distributed           |  |
|  |                          Object Store)                             |  |
|  |  +---------------------------+  +-------------------------------+  |  |
|  |  |     Monitor Cluster       |  |      Manager Daemons          |  |  |
|  |  |  +-----+ +-----+ +-----+ |  |  +-----+ +-----+ +-----+      |  |  |
|  |  |  |MON-1| |MON-2| |MON-3| |  |  |MGR-1| |MGR-2| |MGR-3|      |  |  |
|  |  |  | Paxos Consensus      | |  |  | Dashboard/Prometheus        |  |  |
|  |  |  +---------------------+ |  |  +----------------------------+  |  |
|  |  +---------------------------+  +-------------------------------+  |  |
|  |                                                                    |  |
|  |  +--------------------------------------------------------------+ |  |
|  |  |                    OSD (Object Storage Daemons)              | |  |
|  |  |                                                              | |  |
|  |  |  Node-1              Node-2              Node-3              | |  |
|  |  |  +---------------+  +---------------+  +---------------+     | |  |
|  |  |  | OSD.0  OSD.1  |  | OSD.2  OSD.3  |  | OSD.4  OSD.5  |     | |  |
|  |  |  | [SSD]  [HDD]  |  | [SSD]  [HDD]  |  | [SSD]  [HDD]  |     | |  |
|  |  |  +---------------+  +---------------+  +---------------+     | |  |
|  |  |  | OSD.6  OSD.7  |  | OSD.8  OSD.9  |  | OSD.10 OSD.11 |     | |  |
|  |  |  | [NVMe] [HDD]  |  | [NVMe] [HDD]  |  | [NVMe] [HDD]  |     | |  |
|  |  |  +---------------+  +---------------+  +---------------+     | |  |
|  |  +--------------------------------------------------------------+ |  |
|  |                                                                    |  |
|  |  +--------------------------------------------------------------+ |  |
|  |  |                    CRUSH Map (Data Placement Algorithm)       | |  |
|  |  |  - Pseudorandom data distribution                            | |  |
|  |  |  - Failure domain awareness (host/rack/zone)                 | |  |
|  |  |  - Weight-based rebalancing                                  | |  |
|  |  +--------------------------------------------------------------+ |  |
|  +--------------------------------------------------------------------+  |
+===========================================================================+

[Data Placement: CRUSH Algorithm]
1. Client computes hash(object_id) -> PG (Placement Group)
2. CRUSH(PG, Cluster Map) -> [OSD-1, OSD-2, OSD-3]  # 3 replicas
3. Client writes directly to primary OSD
4. Primary OSD replicates to secondary/tertiary OSDs
5. Ack returned after all replicas written (configurable)
```

### 심층 동작 원리: Ceph 데이터 배치 및 복구

1. **오브젝트 생성 (Object Creation)**:
   - 클라이언트가 4MB 청크로 파일 분할 (stripping)
   - 각 청크에 고유 오브젝트 ID 할당

2. **Placement Group 매핑 (PG Mapping)**:
   - 해시 함수로 오브젝트 -> PG(Placement Group) 매핑
   - PG는 오브젝트의 논리적 컨테이너 (수천 개 오브젝트 포함)

3. **CRUSH 알고리즘 실행 (CRUSH Calculation)**:
   - CRUSH(PG_ID, Cluster_Map, Ruleset) -> [OSD_List]
   - 장애 도메인(Host, Rack, Zone)을 고려한 의사난수 분산
   - 예: PG-1 -> [OSD-0(Host-1), OSD-2(Host-2), OSD-4(Host-3)]

4. **데이터 쓰기 (Write Operation)**:
   - 클라이언트 -> Primary OSD -> Secondary/Tertiary OSD
   - 복제 수(Replication Factor)만큼 모두 기록 후 ACK
   - 저널(Journal) 또는 WAL(Write-Ahead Log)로 내구성 보장

5. **리밸런싱 (Rebalancing)**:
   - OSD 추가/제거 시 CRUSH 맵 업데이트
   - 영향받은 PG만 이동 (전체 마이그레이션 없음)
   - 백그필(Backfill) 속도 제어로 서비스 영향 최소화

6. **자가 복구 (Self-Healing)**:
   - OSD 장애 감지 (Heartbeat 초과)
   - PG 상태가 degraded -> recovering -> active+clean
   - 남은 복제본에서 새 OSD로 데이터 복사

### 핵심 코드: Ceph 배포 및 구성 (Ansible)

```yaml
# Ceph 클러스터 배포 - Ansible Playbook
---
- name: Deploy Ceph Storage Cluster
  hosts: ceph_nodes
  become: yes
  vars:
    ceph_release: quincy
    ceph_monitors: ['mon01', 'mon02', 'mon03']
    ceph_osd_devices:
      - '/dev/sdb'  # SSD for journal/wal
      - '/dev/sdc'  # HDD for data
      - '/dev/sdd'  # HDD for data

  tasks:
    - name: Install Ceph packages
      package:
        name:
          - ceph
          - ceph-mon
          - ceph-osd
          - ceph-mds
          - ceph-mgr
          - ceph-radosgw
        state: present

    - name: Create Ceph configuration
      template:
        src: ceph.conf.j2
        dest: /etc/ceph/ceph.conf
        mode: '0644'
      template:
        src: |
          [global]
          fsid = {{ ceph_fsid }}
          mon_initial_members = {{ ceph_monitors | join(', ') }}
          mon_host = {{ ceph_monitors | map('extract', hostvars, 'ansible_host') | join(', ') }}
          auth_cluster_required = cephx
          auth_service_required = cephx
          auth_client_required = cephx

          # OSD 설정
          osd_pool_default_size = 3
          osd_pool_default_min_size = 2
          osd_crush_chooseleaf_type = 1  # host-level failure domain

          # 성능 튜닝
          osd_op_threads = 8
          osd_disk_threads = 4
          filestore_max_sync_interval = 5

          # 네트워크
          public_network = 10.0.0.0/24
          cluster_network = 10.1.0.0/24  # 복제 트래픽 분리

    - name: Initialize Monitor
      command: ceph-mon --mkfs -i {{ inventory_hostname }}
      when: inventory_hostname in ceph_monitors

    - name: Start Monitor service
      service:
        name: ceph-mon@{{ inventory_hostname }}
        state: started
        enabled: yes
      when: inventory_hostname in ceph_monitors

    - name: Create OSD
      command: ceph-volume lvm create --bluestore --data {{ item }}
      loop: "{{ ceph_osd_devices }}"
      when: inventory_hostname not in ceph_monitors

    - name: Start OSD services
      service:
        name: ceph-osd
        state: started
        enabled: yes

    - name: Create MDS for CephFS
      command: ceph-mds --mkfs -i {{ inventory_hostname }}
      when: "'mds' in group_names"

# Ceph 풀 생성 및 RBD 설정
- name: Configure Ceph Pools
  hosts: ceph_admin
  become: yes
  tasks:
    - name: Create replicated pool for RBD
      command: >
        ceph osd pool create rbd_pool 128 128 replicated
        --size 3 --min-size 2
        --rule replicated_rule

    - name: Enable RBD application on pool
      command: ceph osd pool application enable rbd_pool rbd

    - name: Create erasure-coded pool for object storage
      command: >
        ceph osd pool create ec_pool 128 128 erasure
        erasure-code-profile=ec_profile

    - name: Create erasure code profile
      command: >
        ceph osd erasure-code-profile set ec_profile
        k=4 m=2 crush-failure-domain=host

    - name: Create RBD image
      command: >
        rbd create vm_disk_01 --size 100G --pool rbd_pool
        --image-feature layering,exclusive-lock

    - name: Configure RGW (S3-compatible)
      command: ceph-deploy rgw create {{ item }}
      loop: "{{ groups['rgw_nodes'] }}"
```

### Ceph 성능 메트릭 및 모니터링

| 메트릭 | 설명 | 목표 값 | 측정 방법 |
|---|---|---|---|
| **IOPS** | 초당 입출력 연산 | >100K (All-Flash) | ceph osd pool stats |
| **Throughput** | 데이터 전송 속도 | >10 GB/s | rados bench |
| **Latency** | 응답 지연 | <1ms (SSD), <10ms (HDD) | ceph osd perf |
| **PG State** | 배치 그룹 상태 | 100% active+clean | ceph pg stat |
| **Recovery Rate** | 복구 속도 | >1TB/hour | ceph -w |
| **Cluster Usage** | 용량 사용률 | <80% | ceph df |

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### SDS 제품 비교

| 제품 | 유형 | 프로토콜 | 장점 | 단점 | 적합 시나리오 |
|---|---|---|---|---|---|
| **Ceph** | 오픈소스 | Block/File/Object | 무료, 다중 프로토콜 | 운영 복잡성 | 대규모, 비용 절감 |
| **vSAN** | 하이퍼바이저 | Block | vSphere 통합, 간편 | 비용, VMware 종속 | VMware 환경 |
| **MinIO** | 오픈소스 | Object | 고성능 S3, 간단 | Object만 지원 | S3 전용, AI/ML |
| **GlusterFS** | 오픈소스 | File | POSIX 호환, 간단 | 성능 제한 | 파일 공유, HPC |
| **Nutanix ADSF** | HCI | Block/File | 통합 관리, 성능 | 비용 | HCI, VDI |

### SDS vs Traditional Storage 비교

| 비교 항목 | Traditional (EMC/NetApp) | SDS (Ceph/vSAN) | 개선 효과 |
|---|---|---|---|
| **CapEx** | $10,000/TB | $3,000/TB | 70% 절감 |
| **확장성** | Scale-Up (한계) | Scale-Out (무한) | 선형 확장 |
| **벤더 종속** | 높음 | 낮음 | Lock-in 해소 |
| **운영 복잡성** | 중간 | 높음 (Ceph) / 낮음 (vSAN) | 제품별 상이 |
| **성능** | 일관됨 | 하드웨어에 따라 다름 | 유연한 튜닝 |
| **기능** | 풍부 (중복제거, 압축) | 기본 + 옵션 | 필요 기능 선택 |

### 과목 융합 관점 분석

- **데이터베이스와의 융합**: RBD(RADOS Block Device) 위에 MySQL, PostgreSQL 배포. Ceph의 스냅샷, 복제 기능으로 DB 백업 자동화.

- **컨테이너와의 융합**: CSI(Container Storage Interface)를 통해 Kubernetes에 동적 스토리지 프로비저닝. Rook-Ceph이 쿠버네티스 네이티브 SDS.

- **네트워크와의 융합**: 복제 트래픽(Cluster Network)과 클라이언트 트래픽(Public Network) 분리. RDMA(RoCE)로 지연 최소화.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 프라이빗 클라우드 스토리지 (1PB)**
- **요구사항**: 1PB 용량, 99.999% 가용성, 블록/오브젝트 모두 필요
- **기술사의 의사결정**:
  1. Ceph 클러스터 (30노드, OSD 300개)
  2. 3-way 복제 (99.999% 내구성)
  3. All-Flash (NVMe) for hot, HDD for cold
  4. 블록: RBD for VM, 오브젝트: RGW for S3
  5. **예상 TCO**: Traditional 대비 60% 절감

**시나리오 2: 쿠버네티스 영구 볼륨**
- **요구사항**: 100개 Pod, 동적 PV 프로비저닝, 고성능
- **기술사의 의사결정**:
  1. Rook-Ceph Operator 배포
  2. StorageClass 정의 (fast/standard)
  3. RWO(ReadWriteOnce)/RWX(ReadWriteMany) 지원
  4. **효과**: PV 생성 시간 < 1초

### 도입 시 고려사항 (체크리스트)

**기술적 체크리스트**:
- [ ] 네트워크 대역폭: 복제 트래픽용 별도 네트워크 권장
- [ ] OSD per Node: CPU/메모리 리소스 계산 (1 OSD당 1GB RAM)
- [ ] 저널/WAL 배치: SSD에 저널 배치로 성능 향상
- [ ] CRUSH 맵 설계: 장애 도메인(rack/row/room) 정의

### 주의사항 및 안티패턴

1. **과도한 OSD 밀도**: 한 노드에 너무 많은 OSD는 CPU 병목. 노드당 10~20개 권장.
2. **단일 장애 도메인**: 모든 노드가 같은 랙에 있으면 랙 장애 시 전체 중단.
3. **모니터 과소 배치**: Monitor 3개(홀수) 필수, 5개 이상 권장.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | Traditional | SDS | 개선율 |
|---|---|---|---|
| **CapEx** | $10,000/TB | $3,000/TB | 70% 절감 |
| **확장 단위** | 100TB (어플라이언스) | 1TB (디스크) | 유연한 확장 |
| **가용성** | 99.9% | 99.999% | 100배 향상 |
| **배포 시간** | 2주 | 1시간 | 99% 단축 |

### 미래 전망

1. **NVMe-oF 통합**: NVMe over Fabrics로 원격 NVMe 성능 실현
2. **AI 기반 계층화**: 워크로드 패턴 학습, 자동 데이터 계층 이동
3. **Composable Storage**: 필요한 만큼만 스토리지를 구성하여 할당

### ※ 참고 표준/가이드
- **SNIA Architecture**: Storage Networking Industry Association
- **Ceph Documentation**: https://docs.ceph.com
- **VMware vSAN Design Guide**: VMware Official Documentation

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [SDDC (Software Defined Data Center)](@/studynotes/13_cloud_architecture/03_virt/sddc.md) : SDS를 포함한 통합 아키텍처
- [SDN (Software Defined Networking)](@/studynotes/13_cloud_architecture/03_virt/sdn.md) : 네트워크 가상화
- [블록 스토리지](@/studynotes/13_cloud_architecture/03_virt/block_storage.md) : SDS의 블록 인터페이스
- [오브젝트 스토리지](@/studynotes/13_cloud_architecture/03_virt/object_storage.md) : SDS의 오브젝트 인터페이스
- [CSI (Container Storage Interface)](@/studynotes/13_cloud_architecture/01_native/csi.md) : 컨테이너 스토리지 표준

---

### 👶 어린이를 위한 3줄 비유 설명
1. SDS는 **'공용 주차장'**과 같아요. 각 가게가 따로 주차장을 짓는 대신, 큰 주차장을 함께 써요.
2. 차(데이터)가 늘어나면 **'주차장을 확장'**하면 돼요. 새로운 땅을 사서 덧붙이기만 하면 됩니다.
3. VIP 차는 1층(SSD), 일반 차는 지하(HDD)에 주차하는 것처럼 **'규칙으로 관리'**해요.
