+++
title = "클라우드 컴퓨팅 5대 특징 (NIST 기준)"
date = 2024-05-18
description = "NIST가 정의한 클라우드 컴퓨팅의 5대 필수 특징 - 주문형 셀프 서비스, 광범위한 네트워크 접속, 리소스 풀링, 신속한 탄력성, 측정 가능한 서비스"
weight = 10
[taxonomies]
categories = ["studynotes-13_cloud_architecture"]
tags = ["Cloud Computing", "NIST", "Self-Service", "Elasticity", "Resource Pooling"]
+++

# 클라우드 컴퓨팅 5대 특징 (NIST 기준)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 미국 국립표준기술연구소(NIST)가 정의한 클라우드 컴퓨팅의 5대 필수 특징은 주문형 셀프 서비스, 광범위한 네트워크 접속, 리소스 풀링, 신속한 탄력성, 측정 가능한 서비스로, 모든 클라우드 서비스의 기술적/운영적 기준이 됩니다.
> 2. **가치**: 이 5대 특징은 기업이 진정한 클라우드 서비스인지 판별하는 잣대이자, 클라우드 도입을 통한 비용 절감, 민첩성 향상, 확장성 확보의 이론적 토대를 제공합니다.
> 3. **융합**: 가상화 기술, 분산 시스템, 네트워크 프로토콜, 과금 시스템 등 다양한 IT 기술이 융합되어 구현되며, IaaS/PaaS/SaaS 모든 서비스 모델에 공통 적용됩니다.

---

## Ⅰ. 개요 (Context & Background)

클라우드 컴퓨팅(Cloud Computing)은 인터넷을 통해 언제 어디서나 필요한 만큼의 컴퓨팅 자원을 사용하고, 사용한 만큼만 비용을 지불하는 컴퓨팅 패러다임입니다. 2011년 미국 국립표준기술연구소(NIST, National Institute of Standards and Technology)는 SP 800-145 문서를 통해 클라우드 컴퓨팅의 표준 정의와 5대 필수 특징을 발표했으며, 이는 전 세계 클라우드 산업의 기준이 되었습니다.

**💡 비유**: 클라우드 컴퓨팅은 **'전기나 수도 같은 공공 서비스'**와 같습니다. 가정에서 전기를 쓸 때 발전소의 터빈이 어떻게 돌아가는지 알 필요가 없듯이, 클라우드 사용자는 데이터센터의 서버가 어떻게 구동되는지 알 필요 없이 콘센트(API)에 플러그를 꽂으면 전기(컴퓨팅 자원)가 흘러나오고, 사용한 만큼만 요금을 내면 됩니다.

**등장 배경 및 발전 과정**:
1. **기존 IT 인프라의 한계**: 전통적인 온프레미스 환경은 서버 구매부터 배포까지 수주~수개월이 소요되었고, 피크 트래픽에 대비해 과도한 자원을 미리 확보해야 했습니다.
2. **유틸리티 컴퓨팅의 실현**: 1960년대 John McCarthy가 제안한 "컴퓨팅이 전기처럼 유틸리티가 되어야 한다"는 비전이 인터넷과 가상화 기술의 발전으로 실현되었습니다.
3. **NIST 표준화**: 클라우드 서비스가 다양하게 등장하면서, 진정한 클라우드인지 판별하고 상호 운용성을 보장하기 위해 NIST가 표준 특징을 정의했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 5대 필수 특징 상세 분석

| 특징명 | 영문 명칭 | 상세 정의 및 내부 동작 | 구현 기술 | 비유 |
|---|---|---|---|---|
| **주문형 셀프 서비스** | On-Demand Self-Service | 사용자가 사람의 개입 없이 자동화된 포털/API를 통해 즉시 컴퓨팅 자원(VM, 스토리지, 네트워크)을 프로비저닝하고 해제 | AWS Console, Terraform, REST API | 호텔 체크인 키오스크 |
| **광범위한 네트워크 접속** | Broad Network Access | 다양한 디바이스(노트북, 모바일, 태블릿)와 플랫폼을 통해 표준 프로토콜(HTTP/HTTPS)로 언제 어디서나 접근 가능 | CDN, Edge Location, HTTPS | 스마트폰으로 언제든 예약 |
| **리소스 풀링** | Resource Pooling | 공용 물리 자원(CPU, 메모리, 스토리지, 네트워크)을 논리적으로 분리하여 여러 테넌트에게 동적으로 할당, 위치는 추상화 | Hypervisor, Namespace, Multi-tenancy | 호텔 객실 분할 배정 |
| **신속한 탄력성** | Rapid Elasticity | 트래픽 증가/감소에 따라 자원을 자동으로 수평 확장(Scale-out) 또는 축소(Scale-in)하여 무한한 확장성 제공 | Auto Scaling, Kubernetes HPA | 레고 블록처럼 늘렸다 줄였다 |
| **측정 가능한 서비스** | Measured Service | 자원 사용량을 실시간으로 계측(Metering)하고, 이를 기반으로 종량제(Pay-as-you-go) 과금 및 최적화 제안 | CloudWatch, Prometheus, Billing API | 전기계량기와 요금 고지서 |

### 아키텍처 다이어그램: 5대 특징의 상호작용

```ascii
                           [ Cloud Consumer ]
                                  |
                    +-------------+-------------+
                    |  Broad Network Access     |  <-- HTTP/HTTPS over Internet
                    |  (Web Console, CLI, SDK)  |
                    +-------------+-------------+
                                  |
                    +-------------v-------------+
                    |  On-Demand Self-Service   |  <-- Automated Provisioning
                    |  (API Gateway, Portal)    |
                    +-------------+-------------+
                                  |
        +-------------------------+-------------------------+
        |                         |                         |
+-------v-------+        +--------v--------+       +--------v-------+
|   Compute     |        |    Storage      |       |   Network      |
|    Pool       |        |     Pool        |       |    Pool        |
| [CPU][RAM]    |        | [SSD][HDD]      |       | [VPC][LB]      |
+-------+-------+        +--------+--------+       +--------+-------+
        |                         |                         |
        +-------------+-----------+-------------+-----------+
                      |                         |
            +---------v---------+     +---------v---------+
            | Rapid Elasticity  |     | Measured Service  |
            | (Auto Scaling)    |     | (Metering/Billing)|
            +-------------------+     +-------------------+
```

### 심층 동작 원리: 리소스 풀링의 내부 메커니즘

1. **물리 자원 추상화**: 하이퍼바이저(KVM, Xen)가 물리 서버의 CPU, 메모리를 가상 머신(VM) 단위로 분할
2. **논리적 격리**: 네임스페이스와 cgroups를 통해 VM/컨테이너 간 자원 간섭 방지
3. **동적 할당**: 오케스트레이터(Kubernetes, OpenStack)가 요청에 따라 풀에서 자원을 꺼내 할당
4. **오버커밋(Overcommit)**: 실제 물리 자원보다 더 많은 양을 할당하여 효율 극대화 (예: 1:2 vCPU ratio)
5. **균등 재분배**: 로드 밸런서가 트래픽을 풀 내 인스턴스에 균등 분배

### 핵심 코드: AWS CLI를 통한 셀프 서비스 프로비저닝

```bash
# 주문형 셀프 서비스: 클릭 한 번으로 VM 생성 (사람의 개입 없음)
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --count 2 \
    --instance-type t3.medium \
    --key-name my-key-pair \
    --security-group-ids sg-12345678 \
    --subnet-id subnet-12345678 \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=WebServer}]"

# 측정 가능한 서비스: 실시간 사용량 확인
aws cloudwatch get-metric-statistics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
    --start-time 2024-01-01T00:00:00Z \
    --end-time 2024-01-02T00:00:00Z \
    --period 3600 \
    --statistics Average
```

```yaml
# Infrastructure as Code: Terraform을 통한 탄력적 인프라 정의
resource "aws_autoscaling_group" "web_asg" {
  name                 = "web-asg"
  min_size            = 2
  max_size            = 10                    # 신속한 탄력성: 최대 10대까지 확장
  desired_capacity    = 2
  health_check_type   = "EC2"

  tag {
    key                 = "Name"
    value               = "WebServer"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_policy" "scale_up" {
  name                   = "scale-up"
  scaling_adjustment     = 2
  adjustment_type        = "ChangeInCapacity"
  autoscaling_group_name = aws_autoscaling_group.web_asg.name
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 진정한 클라우드 vs 유사 클라우드

| 비교 관점 | True Cloud (5대 특징 모두 충족) | Pseudo Cloud (일부만 충족) | 상세 분석 |
|---|---|---|---|
| **Self-Service** | 즉시 자동화된 포털 제공 | 영업 담당자 승인 필요 | True Cloud는 API 호출 즉시 VM 생성, Pseudo는 1~3일 소요 |
| **Elasticity** | 초 단위 자동 스케일링 | 수동 용량 증설 | True Cloud는 HPA/CA로 자동 확장, Pseudo는 티켓 발행 후 수동 |
| **Metering** | 초/시간 단위 정밀 과금 | 월 단위 고정 요금 | True Cloud는 $0.023/GB, Pseudo는 월 $100 정액제 |
| **Pooling** | 멀티테넌시 격리 보장 | 단일 테넌트 전용 | True Cloud는 논리 격리, Pseudo는 물리 서버 전용 할당 |

### 과목 융합 관점 분석 (네트워크 및 보안 연계)
- **네트워크(Network)와의 융합**: 광범위한 네트워크 접속은 CDN, Anycast IP, DNS 라우팅 기술과 결합하여 전 세계 어디서나 100ms 이하의 지연 시간을 보장합니다.
- **보안(Security)과의 융합**: 리소스 풀링은 멀티테넌시 환경에서 테넌트 간 데이터 유출 위험을 내포하므로, VXLAN 격리, 암호화 at-rest/in-transit, 제로 트러스트 모델이 필수 결합됩니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)
**문제 상황**: 금융권 고객이 "프라이빗 클라우드 구축"을 요청했으나, 제안된 솔루션이 VM 수동 할당만 가능하고 사용량 기반 과금이 없는 상황입니다.

**기술사의 전략적 의사결정**:
1. **진단**: 제안된 솔루션은 셀프 서비스, 탄력성, 측정 서비스 3가지 특징이 결여되어 NIST 기준의 '진정한 클라우드'가 아닙니다.
2. **대안 제시**: OpenStack 또는 VMware vRealize Automation을 도입하여 셀프 서비스 포털과 Metering 기능을 추가하거나, 하이브리드 클라우드로 전환을 제안합니다.
3. **리스크 관리**: 규제 준수를 위해 프라이빗 클라우드를 유지하되, 개발/테스트 환경은 퍼블릭 클라우드(AWS)를 활용하는 Hybrid 전략 수립.

### 도입 시 고려사항 (체크리스트)
- **Self-Service 구현 여부**: 개발자가 직접 콘솔에서 자원 생성이 가능한가?
- **API 자동화 지원**: Terraform/Ansible 등 IaC 도구와 호환되는가?
- **태깅(Tagging) 체계**: 측정 서비스를 위한 비용 배분 태그가 구축되었는가?
- **오토스케일링 설정**: CPU/메모리 기반 자동 확장 정책이 수립되었는가?

### 주의사항 및 안티패턴 (Anti-patterns)
- **Shadow IT 방치**: 셀프 서비스 특징 때문에 현업 부서가 IT 부서 몰래 SaaS를 결제하여 보안 구멍이 발생할 수 있습니다. Cloud Access Security Broker(CASB) 도입이 필요합니다.
- **리소스 방치**: 탄력성 특징이 비용 절감을 보장하지 않습니다. 사용하지 않는 인스턴스를 자동으로 종료하는 Lifecycle Manager 설정이 필수입니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과
| 구분 | 도입 효과 | 정량적 지표 |
|---|---|---|
| **Time-to-Market** | 셀프 서비스로 배포 시간 단축 | 수주 -> 수분 (99% 단축) |
| **비용 효율성** | 탄력성으로 유휴 자원 제거 | 서버 이용률 15% -> 60% 향상 |
| **운영 생산성** | 자동화로 수동 작업 감소 | OpEx 40% 절감 |

### 미래 전망 및 진화 방향
- **Serverless로의 진화**: 탄력성이 극단화되어 함수 단위(Function-as-a-Service)로 자원이 할당되고, 0부터 무한대까지 스케일링됩니다.
- **Edge Computing 확장**: 광범위한 네트워크 접속이 5G/6G와 결합하여 엣지 노드까지 클라우드 자원이 분산 배치됩니다.

### ※ 참고 표준/가이드
- **NIST SP 800-145**: The NIST Definition of Cloud Computing
- **ISO/IEC 17788**: Cloud Computing - Overview and Vocabulary
- **ISO/IEC 17789**: Cloud Computing - Reference Architecture

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [IaaS (Infrastructure as a Service)](@/studynotes/13_cloud_architecture/03_virt/iaas.md) : 5대 특징이 가장 명확히 구현된 서비스 모델
- [가상화 (Virtualization)](@/studynotes/13_cloud_architecture/03_virt/virtualization.md) : 리소스 풀링을 가능하게 하는 핵심 기술
- [오토 스케일링 (Auto Scaling)](@/studynotes/13_cloud_architecture/01_native/auto_scaling.md) : 신속한 탄력성을 구현하는 기술
- [FinOps](@/studynotes/13_cloud_architecture/01_native/finops.md) : 측정 가능한 서비스를 기반으로 한 비용 최적화 프랙티스
- [멀티 테넌시 (Multi-Tenancy)](@/studynotes/13_cloud_architecture/03_virt/multi_tenancy.md) : 리소스 풀링의 격리 메커니즘

---

### 👶 어린이를 위한 3줄 비유 설명
1. 클라우드 컴퓨팅은 **'마법의 컴퓨터 대여소'**예요. 스마트폰으로 "컴퓨터 10대 주세요!"라고 말하면 즉시 텐트처럼 펑펑 늘어나고, 다 쓰면 다시 줄어들어요.
2. 여러 친구들이 **'공용 장난감방'**에서 각자 필요한 장난감을 빌려 쓰는 것처럼, 많은 사람들이 같은 거대한 컴퓨터를 나눠 써요.
3. 그리고 **'스마트 계량기'**가 달려 있어서, 실제로 장난감을 가지고 논 시간만큼만 용돈을 내면 된답니다.
