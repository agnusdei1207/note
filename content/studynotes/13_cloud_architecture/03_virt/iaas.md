+++
title = "IaaS (Infrastructure as a Service)"
date = 2024-05-18
description = "가상화된 컴퓨팅 자원(VM, 스토리지, 네트워크)을 서비스 형태로 제공하여 사용자가 인프라를 소유하지 않고도 유연하게 구축/운영할 수 있는 클라우드 서비스 모델"
weight = 10
[taxonomies]
categories = ["studynotes-13_cloud_architecture"]
tags = ["IaaS", "Cloud Service Model", "AWS EC2", "Virtualization", "Infrastructure"]
+++

# IaaS (Infrastructure as a Service)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 서버(VM), 스토리지, 네트워크 등 인프라 자원을 가상화하여 API/포털을 통해 즉시 제공받고, 사용자가 OS부터 애플리케이션까지 직접 제어하는 가장 유연한 클라우드 서비스 모델입니다.
> 2. **가치**: 초기 CapEx(자본지출)를 OpEx(운영지출)로 전환하여 진입 장벽을 낮추고, 트래픽에 따른 탄력적 확장/축소로 비용 효율성과 민첩성을 동시에 달성합니다.
> 3. **융합**: 하이퍼바이저 가상화, SDN(Software Defined Networking), 분산 스토리지 기술이 결합되며, PaaS/SaaS의 기반이 되는 인프라 계층입니다.

---

## Ⅰ. 개요 (Context & Background)

IaaS(Infrastructure as a Service)는 클라우드 서비스 모델 중 가장 하위 계층에 위치하며, 물리적 하드웨어를 추상화한 가상의 컴퓨팅 인프라를 서비스 형태로 제공합니다. 사용자는 가상 머신(VM) 인스턴스를 생성하고, 여기에 원하는 운영체제(Linux, Windows)와 미들웨어, 애플리케이션을 직접 설치하여 운영합니다. 대표적으로 AWS EC2(Elastic Compute Cloud), Google Compute Engine(GCE), Microsoft Azure Virtual Machines가 있습니다.

**💡 비유**: IaaS는 **'완전히 비어있는 아파트를 월세로 빌리는 것'**과 같습니다. 집주인(클라우드 제공자)은 건물과 벽, 수도/전기(네트워크, 전원)까지만 제공하고, 세입자(사용자)는 원하는 가구(OS), 가전(미들웨어), 인테리어(애플리케이션)를 직접 들여와 꾸밉니다. 반면 PaaS는 풀옵션 가구가 이미 설치된 서비스드 아파트, SaaS는 호텔 방과 같습니다.

**등장 배경 및 발전 과정**:
1. **전통적 데이터센터의 비효율**: 기업은 3~5년 후의 트래픽을 예측하여 서버를 미리 구매(CapEx)해야 했고, 평균 서버 이용률은 10~20%에 불과했습니다.
2. **Amazon EC2의 등장 (2006)**: 아마존은 자사의 여분의 컴퓨팅 자원을 외부에 대여하기 시작했고, 시간당 과금 모델과 API 기반 자동화를 통해 IaaS 시장을 창설했습니다.
3. **DevOps와 IaC의 부상**: IaaS의 API 기반 특성은 Terraform, Ansible 등 Infrastructure as Code 도구와 결합하여 인프라의 버전 관리와 자동화를 가능하게 했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### IaaS 책임 공유 모델 (Shared Responsibility Model)

| 계층 | On-Premise | IaaS | PaaS | SaaS |
|---|---|---|---|---|
| **애플리케이션** | 사용자 관리 | 사용자 관리 | 사용자 관리 | **CSP 관리** |
| **데이터** | 사용자 관리 | 사용자 관리 | 사용자 관리 | **CSP 관리** |
| **런타임 (Java, Node.js)** | 사용자 관리 | 사용자 관리 | **CSP 관리** | **CSP 관리** |
| **미들웨어 (Tomcat, WAS)** | 사용자 관리 | 사용자 관리 | **CSP 관리** | **CSP 관리** |
| **OS (Linux, Windows)** | 사용자 관리 | 사용자 관리 | **CSP 관리** | **CSP 관리** |
| **가상화 (Hypervisor)** | 사용자 관리 | **CSP 관리** | **CSP 관리** | **CSP 관리** |
| **서버 (Hardware)** | 사용자 관리 | **CSP 관리** | **CSP 관리** | **CSP 관리** |
| **스토리지 (Hardware)** | 사용자 관리 | **CSP 관리** | **CSP 관리** | **CSP 관리** |
| **네트워크 (Hardware)** | 사용자 관리 | **CSP 관리** | **CSP 관리** | **CSP 관리** |

### IaaS 아키텍처 다이어그램

```ascii
+------------------------------------------------------------------+
|                        [ Cloud Consumer ]                         |
|  +----------------------------------------------------------+   |
|  | Applications | Data | Runtime | Middleware | **OS**       |   | <-- User Managed
|  +----------------------------------------------------------+   |
+------------------------------------------------------------------+
                                 || API (REST/SDK)
+------------------------------------------------------------------+
|                     [ IaaS Provider (AWS/Azure) ]                 |
|  +----------------------------------------------------------+   |
|  | **Hypervisor** (KVM, Xen, Hyper-V)                       |   | <-- CSP Managed
|  |  +-------------+  +-------------+  +-------------+        |   |
|  |  | VM Instance |  | VM Instance |  | VM Instance |        |   |
|  |  | [User OS]   |  | [User OS]   |  | [User OS]   |        |   |
|  |  +-------------+  +-------------+  +-------------+        |   |
|  +----------------------------------------------------------+   |
|  | **Storage** (EBS, S3, Blob)  | **Network** (VPC, ELB)    |   |
|  +----------------------------------------------------------+   |
|  | **Physical Hardware** (Servers, Racks, Switches)          |   |
|  +----------------------------------------------------------+   |
+------------------------------------------------------------------+
```

### 심층 동작 원리: VM 인스턴스 생성 사이클

1. **API 요청 수신**: 사용자가 `RunInstances` API 호출 (인스턴스 타입, AMI ID, 키페어, 보안그룹 명시)
2. **인증/인가**: IAM 정책에 따라 요청자의 권한 검증
3. **스케줄링**: 스케줄러가 가용 자원이 충분한 호스트 서버 선별 (CPU, 메모리, AZ 고려)
4. **이미지 로드**: 선택한 AMI(Amazon Machine Image)를 스토리지에서 로드
5. **VM 부팅**: 하이퍼바이저가 VM을 생성하고 커널 부팅 수행
6. **네트워크 구성**: VPC 내 서브넷, 보안그룹(Security Group) 적용
7. **메타데이터 주입**: Instance ID, Public/Private IP, User Data 스크립트 전달
8. **상태 보고**: VM Running 상태를 API로 반환

### 핵심 코드: Terraform을 통한 IaaS 프로비저닝

```hcl
# IaaS: AWS EC2 인스턴스 정의 (Infrastructure as Code)
resource "aws_instance" "web_server" {
  ami                    = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2
  instance_type          = "t3.medium"               # 2 vCPU, 4GB RAM

  # 네트워크 구성
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web.id]

  # 스토리지 구성
  root_block_device {
    volume_size           = 30
    volume_type           = "gp3"
    encrypted             = true
  }

  # 사용자 데이터: OS 부팅 시 자동 실행 스크립트
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              EOF

  tags = {
    Name        = "WebServer"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

# 탄력적 IP 할당
resource "aws_eip" "web_eip" {
  instance = aws_instance.web_server.id
  domain   = "vpc"
}
```

```yaml
# AWS CLI를 통한 IaaS 자원 제어
# VM 인스턴스 생성
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.medium \
  --key-name my-key \
  --security-group-ids sg-12345 \
  --subnet-id subnet-12345 \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=WebServer}]"

# 블록 스토리지 생성 및 연결
aws ec2 create-volume \
  --size 100 \
  --volume-type gp3 \
  --availability-zone ap-northeast-2a

aws ec2 attach-volume \
  --volume-id vol-12345 \
  --instance-id i-12345 \
  --device /dev/sdf
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: IaaS vs PaaS vs SaaS

| 비교 관점 | IaaS | PaaS | SaaS |
|---|---|---|---|
| **제어 수준** | OS~App 완전 제어 | App 코드만 제어 | 설정만 제어 |
| **유연성** | 최고 (커스텀 OS/DB) | 중간 (지원 런타임 한정) | 최저 (기능 한정) |
| **관리 부담** | 높음 (OS 패치, 백업) | 중간 (App 배포만) | 낮음 (사용만) |
| **진입 난이도** | 높음 (인프라 지식 필요) | 중간 | 낮음 |
| **과금 모델** | 시간당 VM 요금 | 실행 시간/요청 수 | 사용자 수/월 요금 |
| **적합 사례** | 레거시 이관, DB, HPC | 웹앱, API 서버 | 이메일, CRM, 협업 |

### 과목 융합 관점 분석
- **운영체제(OS)와의 융합**: IaaS 사용자는 OS 커널 튜닝, 파일시스템 설정, 프로세스 관리 등 OS 레벨의 제어권을 완전히 보유합니다. 이는 성능 최적화에 유리하지만 보안 패치 책임도 사용자에게 있습니다.
- **네트워크와의 융합**: VPC(Virtual Private Cloud) 구성을 통해 서브넷 설계, 라우팅 테이블, NAT Gateway, VPN 연결을 사용자가 직접 제어합니다. BGP/OSPF 등 라우팅 프로토콜은 추상화됩니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)
**시나리오**: 금융사에서 기존 Oracle DB를 클라우드로 이관해야 합니다. 라이선스 이슈와 성능 요구사항이 있습니다.

**전략적 의사결정**:
1. **IaaS 선택**: Oracle DB는 관리형 RDS에서 지원하지 않는 엔터프라이즈 에디션 기능이 필요하므로, EC2(VM)에 직접 설치하는 IaaS 방식 선택
2. **고가용성 구성**: Multi-AZ 배포로 두 개의 AZ에 Active-Standby 구성
3. **스토리지 최적화**: IOPS가 높은 io2 Block Express 볼륨 사용으로 온프레미스와 동등 이상의 디스크 성능 확보
4. **라이선스 이관**: BYOL(Bring Your Own License) 모델로 기존 라이선스 활용

### 도입 시 고려사항 (체크리스트)
- **OS 이미지 관리**: Golden AMI 구축 및 정기적 보안 패치 파이프라인
- **백업 전략**: EBS Snapshot 스케줄링 및 Cross-Region Replication
- **모니터링**: CloudWatch Agent 설치로 메모리/디스크 메트릭 수집
- **보안 강화**: Security Group 최소 권한 원칙, IAM Role 기반 접근 제어

### 안티패턴 (Anti-patterns)
- **공개 키 분실**: EC2 키페어를 분실하면 VM에 SSH 접근 불가. Session Manager(SSM) 도입 권장
- **퍼블릭 IP 하드코딩**: 오토스케일링 시 IP가 변경되므로 Route53 DNS 또는 ELB 사용 필수

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과
| 구분 | 효과 | 지표 |
|---|---|---|
| **CapEx 제거** | 서버 구매비용 0원 | 초기 투자비 100% 절감 |
| **Time-to-Market** | 인프라 배포 시간 단축 | 수주 -> 수분 |
| **가용성** | Multi-AZ 구축 용이 | SLA 99.99% 달성 가능 |

### 미래 전망
- **Bare Metal as a Service**: 하이퍼바이저 오버헤드 없이 물리 서버를 직접 대여하는 BMaaS(AWS Bare Metal)가 고성능 워크로드에 확산
- **Spot/Preemptible VM**: 저렴한 스팟 인스턴스 활용으로 배치/CI 워크로드 비용 90% 절감

### ※ 참고 표준/가이드
- **ISO/IEC 17788**: Cloud Computing Overview and Vocabulary
- **CSA STAR**: Cloud Security Alliance Security Trust Assurance and Risk
- **AWS Well-Architected Framework**: IaaS 설계 모범 사례

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [PaaS (Platform as a Service)](@/studynotes/13_cloud_architecture/03_virt/paas.md) : IaaS 위에 런타임/미들웨어를 추가한 서비스 모델
- [가상화 (Virtualization)](@/studynotes/13_cloud_architecture/03_virt/virtualization.md) : IaaS의 핵심 기술 기반
- [VPC (Virtual Private Cloud)](@/studynotes/13_cloud_architecture/03_virt/vpc.md) : IaaS에서 제공하는 가상 네트워크 서비스
- [블록 스토리지 (Block Storage)](@/studynotes/13_cloud_architecture/03_virt/block_storage.md) : IaaS의 주요 스토리지 서비스
- [Terraform](@/studynotes/15_devops_sre/03_iac/terraform.md) : IaaS를 코드로 관리하는 IaC 도구

---

### 👶 어린이를 위한 3줄 비유 설명
1. IaaS는 **'빈 방을 빌려주는 아파트'**예요. 방(컴퓨터)은 주인이 주지만, 침대(OS), 책상(프로그램)은 내가 직접 들여놓아요.
2. 내가 가구를 배치하는 대로 방이 꾸며지므로, **자유롭게 꾸밀 수 있지만 청소(관리)도 내가 해야 해요.**
3. 좋은 점은 우리 집을 사는 게 아니라 **월세처럼 빌려 쓰는 거라, 이사 갈 때도 쉽고 방을 늘리고 줄이기도 편해요.**
