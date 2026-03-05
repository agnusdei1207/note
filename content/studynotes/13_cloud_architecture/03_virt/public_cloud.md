+++
title = "퍼블릭 클라우드 (Public Cloud)"
date = 2024-05-05
description = "다수의 기업과 개인이 공유하는 공용 클라우드 인프라로, AWS, Azure, GCP 등 CSP가 데이터센터를 운영하고 멀티테넌시로 자원을 분배하여 경제성과 확장성을 제공"
weight = 50
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Public Cloud", "AWS", "Azure", "GCP", "Multi-tenancy", "Shared Infrastructure"]
+++

# 퍼블릭 클라우드 (Public Cloud) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 클라우드 서비스 제공자(CSP)가 거대한 데이터센터를 구축하고, 다수의 기업과 개인이 멀티테넌시 방식으로 인프라를 공유하며, 인터넷을 통해 누구나 접근 가능한 공용 클라우드 컴퓨팅 환경입니다.
> 2. **가치**: 규모의 경제(Economies of Scale)를 통해 **개당 1~3%의 마진**을 누리며도 사용자에게는 **온프레미스 대비 30~50% 저렴한** 가격을 제공합니다. 또한 수분 내에 전 세계 리전에 배포 가능한 글로벌 확장성을 제공합니다.
> 3. **융합**: IaaS, PaaS, SaaS 모든 서비스 모델을 포괄하며, 하이브리드/멀티 클라우드 전략의 핵심 구성 요소입니다.

---

## Ⅰ. 개요 (Context & Background)

퍼블릭 클라우드(Public Cloud)는 제3자 클라우드 서비스 제공자(Cloud Service Provider, CSP)가 소유하고 운영하는 컴퓨팅 리소스를 인터넷을 통해 대중에게 공개하는 클라우드 배포 모델입니다. AWS(Amazon Web Services), Microsoft Azure, Google Cloud Platform(GCP)이 시장을 선도하며, 이를 'Hyperscaler'라고 부릅니다. 사용자는 하드웨어를 구매하거나 데이터센터를 구축할 필요 없이, 신용카드만 있으면 즉시 컴퓨팅 자원을 사용할 수 있습니다.

**💡 비유**: 퍼블릭 클라우드는 **'호텔'**과 같습니다. 개인이 집을 짓는 대신(온프레미스), 호텔 객실을 예약하여 사용합니다. 객실은 다른 투숙객들과 공유되는 시설(로비, 수영장, 헬스장)을 이용하지만, 내 방은 잠금장치로 안전하게 보호됩니다. 체크아웃하면 추가 요금 없이 떠날 수 있고, 객실을 더 필요하면 즉시 추가 예약이 가능합니다.

**등장 배경 및 발전 과정**:
1. **데이터센터의 중앙화**: 개별 기업이 데이터센터를 구축하는 것은 초기 투자비용(CapEx)이 막대하고, 전력/냉각/보안 등 운영 비용(OpEx)도 높았습니다.
2. **AWS의 선도 (2006)**: 아마존은 자사의 전자상거래 피크 시즌(블랙 프라이데이) 대응을 위해 구축한 거대 인프라를 유휴 시간에 다른 기업에게 대여하기 시작했습니다.
3. **Hyperscaler 경쟁**: Microsoft(Azure, 2010), Google(GCP, 2008~2011), Alibaba Cloud(2009)가 경쟁에 뛰어들며 서비스 다양화와 가격 인하가 가속화되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 퍼블릭 클라우드 아키텍처 구성

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 대표 서비스 |
|---|---|---|---|
| **리전(Region)** | 지리적으로 분리된 데이터센터 클러스터 | 전 세계 30+ 리전, 재해 격리 단위 | us-east-1, ap-northeast-2 |
| **가용영역(AZ)** | 리전 내 물리적으로 격리된 데이터센터 | 2~6개 AZ로 고가용성 구성 | us-east-1a, us-east-1b |
| **엣지 로케이션** | CDN, DNS, Lambda@Edge 실행 지점 | 전 세계 400+ PoP | CloudFront Edge |
| **글로벌 네트워크** | 리전 간 연결 전용 백본 | AWS Backbone, Azure Global Network | 100Gbps+ 망 |

### 정교한 구조 다이어그램: Hyperscaler 글로벌 인프라

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Hyperscaler Global Infrastructure ]                    │
└─────────────────────────────────────────────────────────────────────────────┘

     [ North America ]          [ Europe ]           [ Asia Pacific ]
     ┌───────────────┐          ┌───────────────┐    ┌───────────────┐
     │ us-east-1     │          │ eu-west-1     │    │ ap-northeast-2│
     │ (Virginia)    │          │ (Ireland)     │    │ (Seoul)       │
     │ ┌───┐ ┌───┐  │          │ ┌───┐ ┌───┐  │    │ ┌───┐ ┌───┐  │
     │ │AZ │ │AZ │  │          │ │AZ │ │AZ │  │    │ │AZ │ │AZ │  │
     │ │-a │ │-b │  │          │ │-a │ │-b │  │    │ │-a │ │-b │  │
     │ └───┘ └───┘  │          │ └───┘ └───┘  │    │ └───┘ └───┘  │
     │ ┌───┐ ┌───┐  │          │ ┌───┐ ┌───┐  │    │ ┌───┐       │
     │ │AZ │ │AZ │  │          │ │AZ │ │AZ │  │    │ │AZ │       │
     │ │-c │ │-d │  │          │ │-c │ │-d │  │    │ │-c │       │
     │ └───┘ └───┘  │          │ └───┘ └───┘  │    │ └───┘       │
     └───────┬───────┘          └───────┬───────┘    └───────┬───────┘
             │                          │                    │
             └──────────────────────────┼────────────────────┘
                                        │
                        ┌───────────────┴───────────────┐
                        │     Global Backbone Network    │
                        │    (Private Fiber Optic)       │
                        │    100 Gbps+ Low Latency       │
                        └───────────────┬───────────────┘
                                        │
             ┌──────────────────────────┼──────────────────────────┐
             │                          │                          │
     ┌───────▼───────┐          ┌───────▼───────┐          ┌───────▼───────┐
     │ Edge Location │          │ Edge Location │          │ Edge Location │
     │   (Seoul)     │          │   (Tokyo)     │          │   (London)    │
     │ ┌───────────┐ │          │ ┌───────────┐ │          │ ┌───────────┐ │
     │ │ CloudFront│ │          │ │ CloudFront│ │          │ │ CloudFront│ │
     │ │    CDN    │ │          │ │    CDN    │ │          │ │    CDN    │ │
     │ └───────────┘ │          │ └───────────┘ │          │ └───────────┘ │
     │ ┌───────────┐ │          │ ┌───────────┐ │          │ ┌───────────┐ │
     │ │   Route53 │ │          │ │   Route53 │ │          │ │   Route53 │ │
     │ │   (DNS)   │ │          │ │   (DNS)   │ │          │ │   (DNS)   │ │
     │ └───────────┘ │          │ └───────────┘ │          │ └───────────┘ │
     └───────────────┘          └───────────────┘          └───────────────┘
            ▲                         ▲                          ▲
            │                         │                          │
     ┌──────┴──────┐           ┌──────┴──────┐           ┌──────┴──────┐
     │   Users     │           │   Users     │           │   Users     │
     │   (Korea)   │           │   (Japan)   │           │   (UK)      │
     └─────────────┘           └─────────────┘           └─────────────┘
```

### 심층 동작 원리: 멀티테넌시와 자원 공유

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    Multi-Tenancy Resource Sharing                          │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ Physical Server (하이퍼바이저) ]                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                         Host OS / Hypervisor                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │ │
│  │  │   Tenant A  │  │   Tenant B  │  │   Tenant C  │  │   Tenant D  │ │ │
│  │  │  (고객사 1) │  │  (고객사 2) │  │  (개인 1)   │  │  (스타트업) │ │ │
│  │  │  ┌───────┐  │  │  ┌───────┐  │  │  ┌───────┐  │  │  ┌───────┐  │ │ │
│  │  │  │  VM1  │  │  │  │  VM1  │  │  │  │  VM1  │  │  │  │  VM1  │  │ │ │
│  │  │  └───────┘  │  │  └───────┘  │  │  └───────┘  │  │  └───────┘  │ │ │
│  │  │  ┌───────┐  │  │  ┌───────┐  │  │             │  │             │ │ │
│  │  │  │  VM2  │  │  │  │  VM2  │  │  │             │  │             │ │ │
│  │  │  └───────┘  │  │  └───────┘  │  │             │  │             │ │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  논리적 격리: VPC, Security Group, IAM으로 완전 분리                        │
│  물리적 공유: CPU, Memory, Network, Storage은 오버커밋으로 공유             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: Terraform을 활용한 퍼블릭 클라우드 리소스 프로비저닝

```hcl
# Terraform - AWS 퍼블릭 클라우드 인프라 정의

# 1. VPC (가상 프라이빗 클라우드) - 논리적 격리
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "brainscience-vpc"
  }
}

# 2. 서브넷 (가용영역 분산)
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "brainscience-public-${count.index}"
  }
}

# 3. EC2 인스턴스 (가상머신)
resource "aws_instance" "web" {
  count         = 2
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2
  instance_type = "t3.medium"
  subnet_id     = aws_subnet.public[count.index].id

  # 보안 그룹 (논리적 방화벽)
  vpc_security_group_ids = [aws_security_group.web.id]

  # 태그 (비용 추적)
  tags = {
    Name        = "web-server-${count.index}"
    Environment = "production"
    CostCenter  = "engineering"
  }
}

# 4. 로드 밸런서
resource "aws_lb" "web" {
  name               = "brainscience-alb"
  internal           = false
  load_balancer_type = "application"
  subnets            = aws_subnet.public[*].id

  tags = {
    Name = "brainscience-alb"
  }
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 퍼블릭 vs 프라이빗 vs 하이브리드 클라우드

| 비교 관점 | 퍼블릭 클라우드 | 프라이빗 클라우드 | 하이브리드 클라우드 |
|---|---|---|---|
| **소유권** | CSP | 자사 | 혼합 |
| **초기 비용** | $0 | 수억~수십억 | 중간 |
| **확장성** | 무제한 | 제한적 | 유연 |
| **보안 통제** | 공동 책임 | 완전 통제 | 선택적 |
| **규정 준수** | 제약 있음 | 완전 준수 가능 | 혼합 |
| **적합한 워크로드** | 일반적, 웹, 개발/테스트 | 민감 데이터, 규제 산업 | 혼합 |

### 과목 융합 관점 분석

**보안(Security)과의 융합**:
- **공동 책임 모델(Shared Responsibility Model)**: CSP는 물리적 보안, 하이퍼바이저, 네트워크 장비를 책임지고, 사용자는 OS, 애플리케이션, 데이터를 책임집니다.
- **Zero Trust**: 퍼블릭 클라우드에서는 네트워크 경계가 사라지므로, 모든 접근을 Identity 기반으로 검증해야 합니다.

**네트워크와의 융합**:
- **Direct Connect/ExpressRoute**: 온프레미스와 퍼블릭 클라우드 간 전용선 연결로 안정적이고 빠른 통신을 제공합니다.
- **Transit Gateway**: 멀티 VPC, 멀티 계정 간 네트워크 허브 역할을 수행합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: CSP 선택

**문제 상황**: 글로벌 서비스 기업 D사가 퍼블릭 클라우드를 도입하려 합니다. 주요 워크로드는 웹 애플리케이션, 머신러닝, 빅데이터 분석입니다.

**기술사의 전략적 의사결정**:

| 평가 기준 | AWS | Azure | GCP | 추천 |
|---|---|---|---|---|
| **서비스 다양성** | 최고 | 높음 | 높음 | AWS |
| **엔터프라이즈 연동** | 높음 | 최고 (Microsoft) | 중간 | Azure |
| **ML/AI** | SageMaker | Azure ML | Vertex AI | GCP |
| **빅데이터** | EMR, Redshift | Synapse | BigQuery | GCP |
| **가격 경쟁력** | 중간 | 중간 | 높음 | GCP |
| **한국 리전** | 서울 (2016) | 한국 중부 (2017) | 서울 (2020) | AWS (가장 성숙) |

**결론**: 웹 애플리케이션은 AWS, ML/AI와 빅데이터는 GCP를 사용하는 **멀티 클라우드 전략**을 추천합니다.

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - Cloud Egress 비용 무시**: 퍼블릭 클라우드에서 인터넷으로 나가는 데이터(Egress) 비용이 생각보다 높습니다. CDN, Direct Connect 활용으로 비용 최적화가 필요합니다.
- **체크리스트**:
  - [ ] 데이터 상주(Residency) 요구사항 충족 리전 존재 여부
  - [ ] SLA(99.9%+) 및 페널티 조항 검토
  - [ ] Egress 비용 시뮬레이션
  - [ ] Compliance 인증 (SOC 2, ISO 27001, ISMS)

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 온프레미스 | 퍼블릭 클라우드 | 개선율 |
|---|---|---|---|
| **CapEx** | 100% | 0% | 100% 절감 |
| **Time-to-Market** | 수개월 | 수시간 | 95% 단축 |
| **글로벌 배포** | 수년 | 수분 | 99% 단축 |
| **인프라 활용률** | 20% | 80%+ | 300% 향상 |

### 미래 전망 및 진화 방향

- **분산 클라우드(Distributed Cloud)**: 퍼블릭 클라우드 서비스를 엣지, 고객 데이터센터에 분산 배치하되 CSP가 통합 관리합니다.
- **AI/ML 네이티브**: 모든 퍼블릭 클라우드 서비스에 AI가 내장되어 자동 최적화, 이상 탐지, 예측이 기본 제공됩니다.

### ※ 참고 표준/가이드
- **CSA (Cloud Security Alliance)**: 클라우드 보안 모범 사례
- **CIS Benchmarks**: 클라우드 보안 설정 가이드
- **FinOps Foundation**: 클라우드 비용 관리 프레임워크

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [프라이빗 클라우드 (Private Cloud)](@/studynotes/13_cloud_architecture/03_virt/private_cloud.md) : 퍼블릭과 대비되는 배포 모델
- [하이브리드 클라우드 (Hybrid Cloud)](@/studynotes/13_cloud_architecture/02_migration/hybrid_cloud.md) : 퍼블릭+프라이빗 결합
- [멀티 클라우드 (Multi-Cloud)](@/studynotes/13_cloud_architecture/02_migration/multi_cloud.md) : 복수 CSP 활용 전략
- [AWS](@/studynotes/13_cloud_architecture/03_virt/aws.md) : 대표적 퍼블릭 클라우드
- [공동 책임 모델](@/studynotes/13_cloud_architecture/01_native/shared_responsibility.md) : 퍼블릭 클라우드 보안 체계

---

### 👶 어린이를 위한 3줄 비유 설명
1. 퍼블릭 클라우드는 **'거대한 호텔'**이에요. 내가 방을 하나 빌려 쓰지만, 같은 건물에 다른 손님들도 많이 있어요.
2. 호텔 사장님이 **'청소, 수리, 경비'**를 다 해주니까, 나는 **'방만 쓰면 돼요'**. 방이 더 필요하면 즉시 예약할 수 있어요!
3. 그리고 **'수영장, 헬스장, 레스토랑'** 같은 공용 시설도 마음껏 쓸 수 있어요. 내가 직접 지을 필요가 없거든요!
