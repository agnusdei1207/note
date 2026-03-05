+++
title = "VPC (Virtual Private Cloud)"
date = 2024-05-11
description = "퍼블릭 클라우드 내에 구축하는 논리적 격리 가상 네트워크로, 서브넷, 라우팅, 보안 그룹을 통해 기업급 네트워크 아키텍처를 클라우드에서 구현"
weight = 78
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["VPC", "Virtual Network", "Subnet", "Security Group", "NACL", "Private Cloud"]
+++

# VPC (Virtual Private Cloud) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 퍼블릭 클라우드(AWS, Azure, GCP) 내에 논리적으로 격리된 가상 네트워크를 프로비저닝하여, 사용자가 IP 주소 범위, 서브넷, 라우팅 테이블, 네트워크 게이트웨이, 보안 설정을 완전히 통제할 수 있는 프라이빗 네트워크 환경입니다.
> 2. **가치**: 멀티테넌시 기반 퍼블릭 클라우드에서 **네트워크 수준의 완전한 격리**를 제공하며, 온프레미스 데이터센터와 동일한 네트워크 아키텍처(3-Tier, DMZ 등)를 클라우드에서 재현하여 **하이브리드 클라우드 연결의 기반**이 됩니다.
> 3. **융합**: VPN/Direct Connect와 결합하여 온프레미스 연결, Security Group/NACL로 방화벽 구현, Transit Gateway로 멀티 VPC 연결, VPC Peering으로 계정 간 통신을 가능하게 합니다.

---

## Ⅰ. 개요 (Context & Background)

VPC(Virtual Private Cloud)는 퍼블릭 클라우드 제공자의 인프라 내에서 격리된 가상 네트워크를 생성하는 서비스입니다. 사용자는 VPC 내에서 IP 주소 대역(CIDR), 서브넷(Subnet), 라우팅 테이블(Route Table), 인터넷 게이트웨이(Internet Gateway), NAT 게이트웨이 등의 네트워크 자원을 직접 제어할 수 있습니다.

**💡 비유**: VPC는 **'아파트 단지 내 내 집'**과 같습니다. 큰 아파트 단지(퍼블릭 클라우드) 안에 많은 세대가 살지만, 내 집(VPC)은 현관문으로 완전히 구분됩니다. 내 집 안에서 방 나누기(서브넷), 인터넷 선 연결(인터넷 게이트웨이), 출입 통제(보안 그룹)를 모두 내가 결정합니다.

**등장 배경 및 발전 과정**:
1. **초기 클라우드의 네트워크 한계**: AWS 초창기(2006~2009)에는 EC2-Classic이라는 공유 네트워크 환경만 제공되어, 사용자 간 네트워크 격리가 불완전했습니다.
2. **VPC 도입 (2009)**: AWS가 Virtual Private Cloud를 출시하여 사용자가 자체 IP 대역과 네트워크 구성을 완전히 통제할 수 있게 되었습니다.
3. **Default VPC (2013~)**: 모든 AWS 계정에 기본 VPC가 자동 생성되어 쉽게 시작할 수 있게 되었습니다.
4. **하이브리드 연결 강화**: Direct Connect, VPN, Transit Gateway 등 VPC를 중심으로 온프레미스와의 연결성이 지속 강화되고 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: VPC 핵심 네트워크 요소

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | OSI 계층 | 비유 |
|---|---|---|---|---|
| **CIDR 블록** | VPC IP 주소 범위 | 사설 IP 대역 할당 (/16 ~ /28) | L3 | 집 주소 |
| **서브넷(Subnet)** | VPC 내 구획 | AZ 단위 생성, Public/Private 구분 | L3 | 방 |
| **라우팅 테이블** | 트래픽 경로 지정 | Destination → Target 매핑 | L3 | 내비게이션 |
| **인터넷 게이트웨이(IGW)** | 인터넷 연결 | NAT, Public IP 할당 | L3/L4 | 현관문 |
| **NAT 게이트웨이** | Private 서브넷 인터넷 | SNAT (Source NAT) | L4 | 공용 전화 |
| **보안 그룹(SG)** | 인스턴스 방화벽 | Stateful, Allow 규칙만 | L3/L4 | 경비원 |
| **NACL** | 서브넷 방화벽 | Stateless, Allow/Deny | L3/L4 | 출입문 |
| **VPC Peering** | VPC 간 연결 | Transitive Peering 불가 | L3 | 복도 연결 |

### 정교한 구조 다이어그램: 프로덕션급 VPC 아키텍처

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Production VPC Architecture ]                           │
│                         (3-Tier Web Application)                             │
└─────────────────────────────────────────────────────────────────────────────┘

                              [ Internet ]
                                   │
                                   ▼
                        ┌──────────────────┐
                        │  Internet Gateway │  ◄── 인터넷 진입점
                        │      (IGW)        │
                        └────────┬─────────┘
                                 │
    ┌────────────────────────────┼────────────────────────────┐
    │                            │                            │
    │   ╔════════════════════════════════════════════════╗   │
    │   ║            VPC: 10.0.0.0/16                     ║   │
    │   ║                                                  ║   │
    │   ║  ┌──────────────────────────────────────────┐  ║   │
    │   ║  │        Route Table (Public)              │  ║   │
    │   ║  │  10.0.0.0/16 → Local                     │  ║   │
    │   ║  │  0.0.0.0/0   → igw-id                    │  ║   │
    │   ║  └──────────────────────────────────────────┘  ║   │
    │   ║                     │                          ║   │
    │   ║  ┌──────────────────┼──────────────────┐      ║   │
    │   ║  │          AZ-a (Availability Zone)   │      ║   │
    │   ║  │                                    │      ║   │
    │   ║  │  ┌─────────────────────────────┐   │      ║   │
    │   ║  │  │ Public Subnet 10.0.1.0/24   │   │      ║   │
    │   ║  │  │  ┌─────┐  ┌─────┐  ┌─────┐  │   │      ║   │
    │   ║  │  │  │ ALB │  │ NAT │  │Bastion│   │      ║   │
    │   ║  │  │  │(LB) │  │ GW  │  │Host │  │   │      ║   │
    │   ║  │  │  └──┬──┘  └──┬──┘  └─────┘  │   │      ║   │
    │   ║  │  └─────┼────────┼──────────────┘   │      ║   │
    │   ║  │        │        │                  │      ║   │
    │   ║  │  ┌─────┼────────┼──────────────┐   │      ║   │
    │   ║  │  │ Private Subnet 10.0.10.0/24 │   │      ║   │
    │   ║  │  │ (Web/App Tier)              │   │      ║   │
    │   ║  │  │  ┌─────┐  ┌─────┐  ┌─────┐  │   │      ║   │
    │   ║  │  │  │ EC2 │  │ EC2 │  │ EC2 │  │   │      ║   │
    │   ║  │  │  │Web-1│  │Web-2│  │Web-3│  │   │      ║   │
    │   ║  │  │  └──┬──┘  └──┬──┘  └──┬──┘  │   │      ║   │
    │   ║  │  └─────┼────────┼────────┼─────┘   │      ║   │
    │   ║  │        │        │        │         │      ║   │
    │   ║  │  ┌─────┼────────┼────────┼─────┐   │      ║   │
    │   ║  │  │ Private Subnet 10.0.20.0/24 │   │      ║   │
    │   ║  │  │ (Database Tier)             │   │      ║   │
    │   ║  │  │  ┌─────┐      ┌─────┐       │   │      ║   │
    │   ║  │  │  │ RDS │      │ RDS │       │   │      ║   │
    │   ║  │  │  │Primary     │Standby     │   │      ║   │
    │   ║  │  │  └─────┘      └─────┘       │   │      ║   │
    │   ║  │  └─────────────────────────────┘   │      ║   │
    │   ║  │                                    │      ║   │
    │   ║  └────────────────────────────────────┘      ║   │
    │   ║                                               ║   │
    │   ║  ┌──────────────────────────────────────────┐  ║   │
    │   ║  │        Route Table (Private)             │  ║   │
    │   ║  │  10.0.0.0/16 → Local                     │  ║   │
    │   ║  │  0.0.0.0/0   → nat-gw-id                 │  ║   │
    │   ║  └──────────────────────────────────────────┘  ║   │
    │   ║                                                  ║   │
    │   ╚══════════════════════════════════════════════════╝   │
    │                                                           │
    │   ┌──────────────────────────────────────────────────┐   │
    │   │              VPC Endpoint (S3)                    │   │
    │   │  Private Subnet → S3 (인터넷 거치지 않음)         │   │
    │   └──────────────────────────────────────────────────┘   │
    │                                                           │
    └───────────────────────────────────────────────────────────┘

    [ Security Layers ]
    ┌────────────────────────────────────────────────────────┐
    │  NACL (Network ACL) - Stateless                        │
    │  ┌────────────────────────────────────────────────┐   │
    │  │ Rule │ Type  │ Port │ Source    │ Allow/Deny   │   │
    │  │  100 │ HTTP  │  80  │ 0.0.0.0/0 │ ALLOW        │   │
    │  │  110 │ HTTPS │ 443  │ 0.0.0.0/0 │ ALLOW        │   │
    │  │  120 │ SSH   │  22  │ 10.0.0.0/8│ ALLOW        │   │
    │  │  *   │ All   │ All  │ 0.0.0.0/0 │ DENY         │   │
    │  └────────────────────────────────────────────────┘   │
    │                                                        │
    │  Security Group - Stateful                             │
    │  ┌────────────────────────────────────────────────┐   │
    │  │ Inbound Rules:                                  │   │
    │  │  - HTTP (80) from ALB SG                        │   │
    │  │  - SSH (22) from Bastion SG                     │   │
    │  │ Outbound Rules:                                 │   │
    │  │  - All traffic to 0.0.0.0/0                     │   │
    │  └────────────────────────────────────────────────┘   │
    └────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: 트래픽 흐름과 NAT

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    VPC Traffic Flow & NAT Mechanism                         │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ Inbound Traffic: Internet → Private Instance ]                          │
│                                                                            │
│  Internet User (203.0.113.50)                                              │
│         │                                                                  │
│         │ 1. TCP SYN to 52.10.20.30:443                                   │
│         ▼                                                                  │
│  ┌──────────────────┐                                                      │
│  │ Internet Gateway │  ◄── Public IP 매핑                                  │
│  └────────┬─────────┘                                                      │
│           │                                                                │
│           │ 2. Destination NAT: 52.10.20.30 → 10.0.1.10                   │
│           ▼                                                                │
│  ┌──────────────────┐                                                      │
│  │   Route Table    │  0.0.0.0/0 → igw-id                                  │
│  └────────┬─────────┘                                                      │
│           │                                                                │
│           │ 3. Forward to Public Subnet                                    │
│           ▼                                                                │
│  ┌──────────────────┐                                                      │
│  │  Load Balancer   │  (ALB/NLB)                                           │
│  │   10.0.1.10      │                                                      │
│  └────────┬─────────┘                                                      │
│           │                                                                │
│           │ 4. Forward to Private Instance                                 │
│           ▼                                                                │
│  ┌──────────────────┐                                                      │
│  │  Private EC2     │  10.0.10.50:8080                                     │
│  └──────────────────┘                                                      │
│                                                                            │
│  [ Outbound Traffic: Private Instance → Internet ]                         │
│                                                                            │
│  Private EC2 (10.0.10.50)                                                  │
│         │                                                                  │
│         │ 1. apt-get update → 151.101.1.69:80                             │
│         ▼                                                                  │
│  ┌──────────────────┐                                                      │
│  │   Route Table    │  0.0.0.0/0 → nat-gw-id                               │
│  └────────┬─────────┘                                                      │
│           │                                                                │
│           │ 2. Forward to NAT Gateway                                      │
│           ▼                                                                │
│  ┌──────────────────┐                                                      │
│  │  NAT Gateway     │  (Public Subnet: 10.0.1.100)                         │
│  │                  │                                                      │
│  │  SNAT:           │                                                      │
│  │  10.0.10.50:54321 → 52.10.20.40:54321                                  │
│  │  ────────────────────────────────────────                              │
│  │  Source IP 변경: Private → Public (EIP)                                │
│  └────────┬─────────┘                                                      │
│           │                                                                │
│           │ 3. Source NAT: Private IP → Public EIP                         │
│           ▼                                                                │
│  ┌──────────────────┐                                                      │
│  │ Internet Gateway │                                                      │
│  └────────┬─────────┘                                                      │
│           │                                                                │
│           ▼                                                                │
│  Internet (151.101.1.69)                                                   │
│         │                                                                  │
│         │ Response: 52.10.20.40:54321 → 151.101.1.69:80                   │
│         ▼                                                                  │
│  NAT Gateway: 역매핑 → 10.0.10.50:54321                                    │
│         │                                                                  │
│         ▼                                                                  │
│  Private EC2 receives response                                             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: Terraform VPC 인프라 구성

```hcl
# VPC 완전 구성 (Production-Ready)

# 1. VPC 생성
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  instance_tenancy     = "default"

  tags = {
    Name        = "production-vpc"
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

# 2. 가용영역 데이터 소스
data "aws_availability_zones" "available" {
  state = "available"
}

# 3. Public Subnets (2개 AZ)
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name        = "public-subnet-${count.index + 1}"
    Tier        = "public"
    Environment = "production"
  }
}

# 4. Private Subnets - Web Tier (2개 AZ)
resource "aws_subnet" "private_web" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name        = "private-web-subnet-${count.index + 1}"
    Tier        = "private-web"
    Environment = "production"
  }
}

# 5. Private Subnets - DB Tier (2개 AZ)
resource "aws_subnet" "private_db" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 20}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name        = "private-db-subnet-${count.index + 1}"
    Tier        = "private-db"
    Environment = "production"
  }
}

# 6. Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "production-igw"
  }
}

# 7. Elastic IP for NAT Gateway
resource "aws_eip" "nat" {
  count  = 2  # AZ별 NAT Gateway
  domain = "vpc"

  tags = {
    Name = "nat-eip-${count.index + 1}"
  }
}

# 8. NAT Gateway (AZ별)
resource "aws_nat_gateway" "main" {
  count         = 2
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = {
    Name = "nat-gw-${count.index + 1}"
  }

  depends_on = [aws_internet_gateway.main]
}

# 9. Public Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "public-rt"
  }
}

# 10. Private Route Tables (AZ별)
resource "aws_route_table" "private" {
  count  = 2
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }

  tags = {
    Name = "private-rt-${count.index + 1}"
  }
}

# 11. Route Table Associations
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private_web" {
  count          = 2
  subnet_id      = aws_subnet.private_web[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

resource "aws_route_table_association" "private_db" {
  count          = 2
  subnet_id      = aws_subnet.private_db[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# 12. Security Group - ALB
resource "aws_security_group" "alb" {
  name        = "alb-sg"
  description = "Security group for Application Load Balancer"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "alb-sg"
  }
}

# 13. Security Group - Web Servers
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  # ALB에서만 접근 허용
  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  # SSH는 Bastion Host에서만
  ingress {
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web-sg"
  }
}

# 14. Security Group - Database
resource "aws_security_group" "db" {
  name        = "db-sg"
  description = "Security group for database"
  vpc_id      = aws_vpc.main.id

  # Web 서버에서만 DB 접근 허용
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  # 아웃바운드 불필요 (DB는 응답만)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "db-sg"
  }
}

# 15. VPC Flow Logs (네트워크 모니터링)
resource "aws_flow_log" "main" {
  iam_role_arn    = aws_iam_role.vpc_flow_log.arn
  log_destination = aws_cloudwatch_log_group.vpc_flow_log.arn
  traffic_type    = "ALL"
  vpc_id          = aws_vpc.main.id

  tags = {
    Name = "vpc-flow-log"
  }
}

resource "aws_cloudwatch_log_group" "vpc_flow_log" {
  name              = "/aws/vpc/flow-log"
  retention_in_days = 30
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Security Group vs NACL

| 비교 관점 | Security Group (SG) | Network ACL (NACL) | 상세 분석 |
|---|---|---|---|
| **동작 계층** | 인스턴스(ENI) 수준 | 서브넷 수준 | SG가 더 세밀한 제어 가능 |
| **상태성** | Stateful (응답 자동 허용) | Stateless (양방향 규칙 필요) | SG가 관리 용이 |
| **규칙 유형** | Allow만 가능 | Allow/Deny 모두 가능 | NACL로 명시적 차단 가능 |
| **번호 순서** | 없음 (모두 평가) | 번호 순서 (낮은 수부터) | NACL은 규칙 우선순위 중요 |
| **적용 대상** | 특정 ENI/인스턴스 | 서브넷 내 모든 인스턴스 | NACL은 광범위 기본 정책 |
| **Return Traffic** | 자동 허용 | 별도 규칙 필요 | SG가 설정 간편 |

### 과목 융합 관점 분석

**네트워크와의 융합**:
- **CIDR & Subnetting**: VPC 설계는 IP 주소 체계 설계가 필수
- **Routing**: 라우팅 테이블로 트래픽 경로 제어
- **VPN/IPsec**: Site-to-Site VPN으로 온프레미스 연결
- **BGP**: Direct Connect와 BGP Peering

**보안과의 융합**:
- **Defense in Depth**: NACL(1차) + Security Group(2차) 이중 방화벽
- **Zero Trust Network**: VPC 내에서도 최소 권한 원칙 적용
- **Network Segmentation**: 서브넷 분리로 lateral movement 방지

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 멀티 계정 VPC 설계

**문제 상황**: 대기업 C사는 개발/스테이징/운영 환경을 별도 AWS 계정으로 분리해야 합니다. 각 환경은 격리되어야 하지만, 공통 서비스(AD, 모니터링)는 공유해야 합니다.

**기술사의 전략적 의사결정**:

1. **아키텍처 설계**:

   ```
   ┌─────────────────────────────────────────────────────────────┐
   │                    AWS Organization                          │
   │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
   │  │  Dev Account│ │Stage Account│ │ Prod Account│            │
   │  │  10.1.0.0/16│ │10.2.0.0/16  │ │10.3.0.0/16  │            │
   │  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘            │
   │         │               │               │                    │
   │         └───────────────┼───────────────┘                    │
   │                         │                                    │
   │              ┌──────────▼──────────┐                         │
   │              │   Shared Services   │                         │
   │              │     Account         │                         │
   │              │    10.0.0.0/16      │                         │
   │              │  - AD/LDAP          │                         │
   │              │  - Monitoring       │                         │
   │              │  - Logging          │                         │
   │              └─────────────────────┘                         │
   │                         │                                    │
   │              [ Transit Gateway ]                              │
   │              (Central Hub for All VPCs)                       │
   └─────────────────────────────────────────────────────────────┘
   ```

2. **연결 방식 선택**:

   | 방식 | 장점 | 단점 | 추천 |
   |---|---|---|---|
   | VPC Peering | 간단, 저렴 | n(n-1)/2 연결, Transitive 불가 | 소규모 |
   | Transit Gateway | 중앙 집중, 확장성 | 추가 비용 | **대규모** |
   | PrivateLink | 서비스 노출만 | 양방향 통신 어려움 | 서비스 공유 |

3. **Transit Gateway 채택**: 확장성과 관리 효율성을 위해 중앙 집중형 허브 구조

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - Oversized VPC**: /16 CIDR을 사용하여 IP 낭비. 실제 필요한 크기보다 작게 시작하고 확장하는 것이 좋습니다.

- **안티패턴 - Single Subnet**: 모든 리소스를 하나의 퍼블릭 서브넷에 배치. 보안과 확장성을 위해 3-Tier 구조 권장.

- **체크리스트**:
  - [ ] CIDR 계획: 향후 확장 고려 (온프레미스와 중복 피하기)
  - [ ] AZ 분산: 최소 2개 AZ에 서브넷 배치
  - [ ] NAT Gateway 위치: 퍼블릭 서브넷에 배치
  - [ ] VPC Flow Logs: 보안 감사를 위해 활성화
  - [ ] 서브넷 크기: /24 이상 권장 (256개 IP)

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | EC2-Classic | VPC | 개선율 |
|---|---|---|---|
| **네트워크 격리** | 공유 | 완전 격리 | 100% 향상 |
| **IP 주소 통제** | 불가능 | 완전 통제 | 100% 향상 |
| **보안 그룹 유연성** | 제한적 | 무제한 | 10배 향상 |
| **하이브리드 연결** | 제한적 | VPN/DX 지원 | 100% 향상 |

### 미래 전망 및 진화 방향

- **IPv6 Native VPC**: IPv6 전용 서브넷 및 듀얼 스택 지원 확대
- **VPC Lattice**: 서비스 간 연결, 인증, 모니터링을 단순화하는 새로운 서비스 메시 계층
- **Private NAT Gateway**: 프라이빗 서브넷 간 통신을 위한 NAT 단순화

### ※ 참고 표준/가이드
- **RFC 1918**: 사설 IP 주소 할당 표준
- **AWS VPC Best Practices**: AWS 공식 가이드
- **NIST SP 800-41**: 방화벽 정책 가이드라인

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [퍼블릭 클라우드 (Public Cloud)](@/studynotes/13_cloud_architecture/03_virt/public_cloud.md) : VPC가 구축되는 기반
- [하이브리드 클라우드](@/studynotes/13_cloud_architecture/02_migration/hybrid_cloud.md) : VPC와 온프레미스 연결
- [Direct Connect](@/studynotes/13_cloud_architecture/03_virt/direct_connect.md) : 전용선 연결 서비스
- [Security Group](@/studynotes/13_cloud_architecture/03_virt/security_group.md) : VPC 내 방화벽 서비스
- [Subnet](@/studynotes/10_network/02_layers/subnet.md) : IP 네트워크 분할 개념

---

### 👶 어린이를 위한 3줄 비유 설명
1. VPC는 **'아파트 단지 내 내 집'**과 같아요. 큰 단지(클라우드) 안에서도 내 집만의 **'주소와 방, 출입문'**을 가져요.
2. **'방마다 용도가 달라요'**. 거실(퍼블릭 서브넷)은 누구나 올 수 있지만, 안방(프라이빗 서브넷)은 가족만 들어갈 수 있어요.
3. **'현관문과 경비원'**이 지켜줘요. Security Group(경비원)이 나쁜 사람은 못 들어오게 해줘요!
