+++
title = "온디맨드 / 예약 / 스팟 인스턴스 (Instance Pricing Models)"
date = 2026-03-05
description = "클라우드 컴퓨팅의 세 가지 주요 요금제 모델의 원리, 비용 구조, 적용 시나리오 및 FinOps 관점의 최적화 전략"
weight = 80
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["On-Demand", "Reserved-Instance", "Spot-Instance", "FinOps", "Cost-Optimization", "Cloud-Pricing"]
+++

# 온디맨드 / 예약 / 스팟 인스턴스 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 온디맨드는 초/시간 단위 종량제, 예약 인스턴스(RI)는 1~3년 약정 할인, 스팟 인스턴스는 잉여 자원 경매로 최대 90% 할인을 제공하는 클라우드의 세 가지 VM 구매 모델입니다.
> 2. **가치**: 워크로드 특성에 따라 적절한 모델을 조합하면 **클라우드 비용을 50~80% 절감**할 수 있으며, 이는 FinOps(Financial Operations)의 핵심 실천 항목입니다.
> 3. **융합**: 오토 스케일링 그룹(ASG), 쿠버네티스 클러스터 오토스케일러, 서버리스와 결합하여 비용 최적화와 탄력성을 동시에 달성하는 하이브리드 전략이 표준입니다.

---

## Ⅰ. 개요 (Context & Background)

클라우드 컴퓨팅의 가장 큰 장점 중 하나는 유연한 요금제 모델입니다. AWS, Azure, GCP 등 주요 클라우드 프로바이더는 사용 패턴과 예측 가능성에 따라 선택할 수 있는 다양한 인스턴스 구매 옵션을 제공합니다.

**💡 비유**:
- **온디맨드**: **'호텔 체크인'**과 같습니다. 방이 있으면 언제든 묵을 수 있고, 묵은 만큼 지불합니다. 비싸지만 유연합니다.
- **예약 인스턴스**: **'1년치 월세 계약'**과 같습니다. 장기 계약을 조건으로 큰 할인을 받습니다. 중도 해약이 어렵습니다.
- **스팟 인스턴스**: **'비수기 특가 호텔'**과 같습니다. 방이 남으면 아주 싸게 제공하지만, 성수기가 되면 언제든 방을 비워줘야 합니다.

**등장 배경 및 발전 과정**:
1. **온디맨드만 존재 (2006~)**: AWS 출시初期에는 시간당 요금제만 있었습니다.
2. **예약 인스턴스 도입 (2009~)**: 기업 고객의 비용 예측성 요구로 1~3년 약정 할인 도입.
3. **스팟 인스턴스 도입 (2010~)**: 유휴 자원 활용으로 더 많은 고객 유치.
4. **Savings Plans (2019~)**: RI의 복잡성을 줄인 유연한 약정 모델.
5. **Spot 블록 / Fargate Spot (2018~)**: 컨테이너 환경에 최적화된 스팟 활용.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 및 비교

| 특성 | 온디맨드 (On-Demand) | 예약 (Reserved) | 스팟 (Spot) |
|---|---|---|---|
| **약정 기간** | 없음 | 1년 또는 3년 | 없음 (2분 전 통보) |
| **할인율** | 0% (기준) | 30~72% | 최대 90% |
| **可用성** | 99%+ | 100% 보장 | 변동 (중단 가능) |
| **유연성** | 최고 | 낮음 | 중간 |
| **적합 워크로드** | 개발/테스트, 예측 불가 | 프로덕션 상시 구동 | 배치, CI/CD, 분산 |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Instance Pricing Models Comparison ]                     │
└─────────────────────────────────────────────────────────────────────────────┘

[ 비용 비교 (m5.xlarge, us-east-1 기준, 24/365 운영) ]

    월 비용 (USD)
    300 ┤
        │  ╭──────────────────────────────────────────────────── On-Demand
    250 ┤  │  $0.192/시간 × 730시간 = $140.16/월 (연 $1,682)
        │  │
    200 ┤  │
        │  │
    150 ┤  │ ╭────────────────────────────────────────────────── 1년 RI (All Upfront)
        │  │ │  $70.53/월 상환 (연 $846, 50% 할인)
    100 ┤  │ │
        │  │ │ ╭────────────────────────────────────────────────  3년 RI (All Upfront)
     50 ┤  │ │ │  $44.23/월 상환 (연 $531, 68% 할인)
        │  │ │ │╭───────────────────────────────────────────────  Spot (평균)
      0 ┤──│─│─││─── $15.00/월 (연 $180, 89% 할인, 변동 있음)
        └──┴─┴─┴┴────────────────────────────────────────────────►
           On-  1Y   3Y   Spot
           Dem  RI   RI


┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Usage Decision Matrix ]                                  │
└─────────────────────────────────────────────────────────────────────────────┘

                    예측 가능성 (Predictability)
                            ▲
                            │
           RI/Savings Plans │          하이브리드
          (3년 약정)         │        (RI + Spot)
                            │
                    ┌───────┴───────┐
                    │               │
     프로덕션       │               │   개발/테스트
     (상시 구동)    │               │   (간헐적 사용)
                    │               │
    ────────────────┼───────────────┼────────────► 비용 민감도
                    │               │
     배치/빅데이터  │               │   프로토타입
     (중단 허용)    │               │   (불확실)
                    │               │
                    └───────┬───────┘
                            │
           Spot Instances   │          On-Demand
          (최대 90% 할인)    │         (최고 유연성)
                            │


[ 예약 인스턴스 유형별 비교 ]

┌──────────────────────────────────────────────────────────────────────────────┐
│                    Reserved Instance Options                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [ 결제 옵션 (Payment Options) ]                                              │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 옵션                │ 선납 금액     │ 월 요금    │ 총 비용      │ 할인율  ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ All Upfront         │ 100% 선납    │ $0         │ 최저         │ 최고    ││
│  │ (전체 선납)          │              │            │              │        ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ Partial Upfront     │ 일부 선납    │ 나머지 월  │ 중간         │ 중간    ││
│  │ (부분 선납)          │              │            │              │        ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ No Upfront          │ $0           │ 전체 월    │ 최고         │ 최저    ││
│  │ (선납 없음)          │              │            │              │        ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  [ 인스턴스 유형 유연성 ]                                                     │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 유형                │ 설명                    │ 예시                    ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ Standard RI         │ 특정 인스턴스 타입       │ m5.xlarge만 사용       ││
│  │ (표준)               │ 교환 불가               │                         ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ Convertible RI      │ 동급 다른 타입으로       │ m5.xlarge → m5.2xlarge ││
│  │ (전환형)             │ 교환 가능               │ (동일 리전, 동일 패밀리) ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ Scheduled RI        │ 특정 시간대만           │ 매일 09:00-18:00        ││
│  │ (스케줄형)           │ 예약                    │                         ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


[ 스팟 인스턴스 가격 메커니즘 ]

                    Spot Price
    가격 ($/시간)      ▲
         0.20 ┤        ╭─╮
              │    ╭───╯ ╰───╮
         0.15 ┤    │         ╰────╮        ╭──
              │────╯              ╰────────╯
         0.10 ┤                                       ← On-Demand 가격
              │
         0.05 ┤
              │
              └─────────────────────────────────────► 시간
                    00:00    06:00   12:00   18:00

    - Spot 가격은 수요/공급에 따라 실시간 변동
    - On-Demand 가격보다 항상 낮음
    - 가격 상승 시 사용자의 최대 입찰가를 초과하면 인스턴스 종료 (2분 전 통보)
    - 현재는 "정지"(Stop) 옵션도 제공 → 재시작 가능


[ 스팟 인스턴스 중단 메커니즘 ]

    Time    Event
    T-2분   AWS로부터 "Spot Interruption Notice" 수신
            │
            ▼
    ┌───────────────────────────────────────────────┐
    │         2분간 정상 운영 가능                   │
    │                                               │
    │  대응 옵션:                                    │
    │  1. 워크로드 완료 후 정상 종료                  │
    │  2. 체크포인트 저장 후 종료                     │
    │  3. 다른 인스턴스로 작업 이관                   │
    │  4. (Spot 블록 사용 시) 종료 방지               │
    │                                               │
    └───────────────────────────────────────────────┘
            │
            ▼
    T+0     인스턴스 종료 (Terminate) 또는 정지 (Stop)
```

### 심층 동작 원리: 스팟 인스턴스 활용 전략

```python
"""
AWS Spot Instance 활용 전략 코드
Spot 중단에 대비한 체크포인팅 및 복구 메커니즘
"""

import boto3
import json
import time
import signal
import sys
from typing import Optional, List
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SpotInterruptionHandler:
    """
    Spot 인스턴스 중단 대응 핸들러

    AWS는 Spot 중단 2분 전에 메타데이터 엔드포인트를 통해
    중단 알림을 제공합니다.
    """

    checkpoint_enabled: bool = True
    checkpoint_interval: int = 60  # 초
    checkpoint_path: str = "/tmp/checkpoint"
    s3_bucket: Optional[str] = None
    s3_prefix: str = "checkpoints/"

    def __post_init__(self):
        self.session = boto3.Session()
        self.s3 = self.session.client('s3') if self.s3_bucket else None
        self._register_signal_handlers()

    def _register_signal_handlers(self):
        """시그널 핸들러 등록"""
        signal.signal(signal.SIGTERM, self._handle_termination)
        signal.signal(signal.SIGINT, self._handle_termination)

    def _handle_termination(self, signum, frame):
        """종료 시그널 처리"""
        logger.warning(f"Received signal {signum}, initiating graceful shutdown...")
        self.save_checkpoint(emergency=True)
        sys.exit(0)

    def check_spot_interruption(self) -> Optional[dict]:
        """
        Spot 중단 알림 확인

        AWS 메타데이터 엔드포인트에서 중단 알림 확인
        http://169.254.169.254/latest/meta-data/spot/instance-action
        """
        import urllib.request
        import urllib.error

        metadata_url = "http://169.254.169.254/latest/meta-data/spot/instance-action"

        try:
            with urllib.request.urlopen(metadata_url, timeout=2) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    logger.warning(f"Spot interruption notice: {data}")
                    return data
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # 중단 예정 없음
                return None
        except Exception as e:
            logger.debug(f"Could not check spot metadata: {e}")

        return None

    def save_checkpoint(self, emergency: bool = False) -> None:
        """
        체크포인트 저장

        Args:
            emergency: 긴급 저장 여부 (중단 임박)
        """
        checkpoint_data = {
            "timestamp": time.time(),
            "emergency": emergency,
            "state": self._get_application_state()
        }

        # 로컬 저장
        with open(self.checkpoint_path, 'w') as f:
            json.dump(checkpoint_data, f)

        # S3 백업 (설정된 경우)
        if self.s3 and self.s3_bucket:
            key = f"{self.s3_prefix}checkpoint_{int(time.time())}.json"
            self.s3.put_object(
                Bucket=self.s3_bucket,
                Key=key,
                Body=json.dumps(checkpoint_data).encode()
            )
            logger.info(f"Checkpoint saved to s3://{self.s3_bucket}/{key}")

    def _get_application_state(self) -> dict:
        """애플리케이션 상태 수집 (구현 필요)"""
        # 실제 구현에서는 애플리케이션별 상태 수집
        return {
            "processed_items": 0,
            "current_batch": None,
            "progress": 0.0
        }

    def restore_from_checkpoint(self) -> Optional[dict]:
        """체크포인트에서 복구"""
        try:
            # 로컬 체크포인트 확인
            with open(self.checkpoint_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # S3에서 최신 체크포인트 검색
            if self.s3 and self.s3_bucket:
                response = self.s3.list_objects_v2(
                    Bucket=self.s3_bucket,
                    Prefix=self.s3_prefix
                )
                if 'Contents' in response:
                    latest = max(response['Contents'], key=lambda x: x['LastModified'])
                    obj = self.s3.get_object(
                        Bucket=self.s3_bucket,
                        Key=latest['Key']
                    )
                    return json.loads(obj['Body'].read())
        return None


class SpotFleetManager:
    """
    Spot Fleet 관리자
    다양한 인스턴스 타입/가용영역 활용으로 안정성 확보
    """

    def __init__(self, region: str = 'us-east-1'):
        self.ec2 = boto3.client('ec2', region_name=region)
        self.autoscaling = boto3.client('autoscaling', region_name=region)

    def create_diversified_spot_fleet(
        self,
        launch_template_id: str,
        target_capacity: int,
        spot_allocation_strategy: str = 'capacity-optimized',
        instance_types: Optional[List[str]] = None
    ) -> str:
        """
        다양화된 Spot Fleet 생성

        Allocation Strategies:
        - capacity-optimized: 가용 용량 가장 많은 풀 선택 (권장)
        - lowest-price: 가장 저렴한 풀 선택
        - diversified: 여러 풀에 분산
        """
        if instance_types is None:
            # 다양한 인스턴스 타입으로 다양화
            instance_types = [
                'm5.xlarge', 'm5a.xlarge', 'm5n.xlarge',
                'm5d.xlarge', 'm5ad.xlarge',
                'm4.xlarge',  # 구형 포함
            ]

        spot_fleet_config = {
            'IamFleetRole': 'arn:aws:iam::ACCOUNT:role/aws-ec2-spot-fleet-tagging-role',
            'AllocationStrategy': spot_allocation_strategy,
            'TargetCapacity': target_capacity,
            'SpotPrice': '0.10',  # 최대 입찰가
            'LaunchTemplateConfigs': [
                {
                    'LaunchTemplateSpecification': {
                        'LaunchTemplateId': launch_template_id,
                        'Version': '$Latest'
                    },
                    'Overrides': [
                        {
                            'InstanceType': it,
                            'WeightedCapacity': 1.0,
                        }
                        for it in instance_types
                    ]
                }
            ],
            'Type': 'maintain',  # maintain | request
            'ReplaceUnhealthyInstances': True,
            'InstanceInterruptionBehavior': 'stop'  # stop | terminate
        }

        response = self.ec2.request_spot_fleet(SpotFleetRequestConfig=spot_fleet_config)
        return response['SpotFleetRequestId']

    def get_spot_interruption_advice(self) -> List[dict]:
        """
        Spot 중단 빈도가 낮은 인스턴스 타입 추천
        """
        # AWS는 Spot Advisor를 통해 과거 중단 빈도 제공
        advice_url = "https://spot-bid-advisor.us-east-1.amazonaws.com/spot-advisor-data.json"

        # 실제로는 HTTP 요청으로 데이터 가져오기
        # 여기서는 예시 데이터 반환
        return [
            {"instance_type": "m5.xlarge", "interruption_rate": "<5%", "savings": "70%"},
            {"instance_type": "c5.2xlarge", "interruption_rate": "<5%", "savings": "65%"},
            {"instance_type": "r5.xlarge", "interruption_rate": "5-10%", "savings": "75%"},
        ]


# ASG에서 Spot + On-Demand 혼합 전략
def create_mixed_instances_asg():
    """
    Auto Scaling Group에서 Spot과 On-Demand 혼합 사용
    """
    asg = boto3.client('autoscaling')

    response = asg.create_auto_scaling_group(
        AutoScalingGroupName='mixed-instances-asg',
        MixedInstancesPolicy={
            'InstancesDistribution': {
                'OnDemandBaseCapacity': 2,  # 최소 On-Demand 2대
                'OnDemandPercentageAboveBaseCapacity': 20,  # 추가 용량의 20%는 On-Demand
                'SpotAllocationStrategy': 'capacity-optimized',
                'SpotInstancePools': 4,  # 4개 풀에서 Spot 분산
            },
            'LaunchTemplate': {
                'LaunchTemplateSpecification': {
                    'LaunchTemplateId': 'lt-1234567890abcdef0',
                    'Version': '$Latest'
                },
                'Overrides': [
                    {'InstanceType': 'm5.xlarge'},
                    {'InstanceType': 'm5a.xlarge'},
                    {'InstanceType': 'm5d.xlarge'},
                    {'InstanceType': 'm5n.xlarge'},
                ]
            }
        },
        MinSize=2,
        MaxSize=20,
        DesiredCapacity=10,
        VPCZoneIdentifier='subnet-123,subnet-456'
    )

    return response
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Savings Plans vs Reserved Instances

| 비교 관점 | Reserved Instances | Savings Plans | 비고 |
|---|---|---|---|
| **약정 방식** | 특정 인스턴스 | $/시간 약정 | SP가 더 유연 |
| **유연성** | 제한적 | 높음 | SP는 서비스/리전/크기 자유 |
| **할인율** | 최대 72% | 최대 72% | 유사 |
| **교환 가능** | Convertible만 | 자동 적용 | SP가 편리 |
| **관리 복잡도** | 높음 | 낮음 | SP 권장 |
| **적용 범위** | EC2, RDS | EC2, Fargate, Lambda | SP가 광범위 |

### 비용 최적화 전략 매트릭스

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ Instance Purchasing Strategy ]                           │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 워크로드 유형         │ 추천 전략                    │ 예상 절감률      ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ 데이터베이스 (상시)    │ 3년 Convertible RI           │ 60-70%         ││
│  │ 웹 서버 (상시)        │ 1년 Standard RI              │ 40-50%         ││
│  │ 웹 서버 (피크 대응)   │ Savings Plans + Spot         │ 50-60%         ││
│  │ CI/CD 파이프라인      │ 100% Spot                    │ 70-90%         ││
│  │ 빅데이터 배치         │ 100% Spot (체크포인팅)        │ 70-90%         ││
│  │ 개발/테스트           │ On-Demand (야간/주말 종료)    │ 50-70%         ││
│  │ 재해 복구 (대기)      │ 스팟 블록 또는 RI             │ 40-80%         ││
│  │ 컨테이너 (K8s)        │ Savings Plans + Spot         │ 50-70%         ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  [ 하이브리드 전략 예시 (100대 웹 서버) ]                                      │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 구성:                                                                    ││
│  │ - 20대: On-Demand (최소 가용성 보장)                                     ││
│  │ - 30대: 1년 RI (베이스라인)                                              ││
│  │ - 50대: Spot (피크 대응, 중단 허용)                                       ││
│  │                                                                         ││
│  │ 월 비용 (m5.xlarge 기준):                                                ││
│  │ - On-Demand: 20 × $140 = $2,800                                        ││
│  │ - RI: 30 × $70 = $2,100                                                ││
│  │ - Spot: 50 × $15 = $750                                                ││
│  │ - Total: $5,650/월                                                      ││
│  │                                                                         ││
│  │ 비교: 100대 On-Demand = $14,000/월                                      ││
│  │ 절감: $8,350/월 (60% 절감)                                              ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 과목 융합 관점 분석

**FinOps와의 융합**:
- **비용 가시성**: 태깅, Cost Explorer로 사용량 추적
- **비용 최적화**: Right-sizing, RI/SP 활용률 모니터링
- **비용 운영**: 예산 설정, 알림, 자동화

**운영체제(OS)와의 융합**:
- **인스턴스 메타데이터**: IMDSv2로 인스턴스 정보 확인
- **그레이스풀 셧다운**: init 시스템에서 시그널 처리

**네트워크와의 융합**:
- **리전 간 데이터 전송비**: 인스턴스 유형 선택에 영향
- **VPC 엔드포인트**: 데이터 전송비 절감

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 스타트업 비용 최적화

**문제 상황**: 스타트업이 월 $10,000 클라우드 비용 중 70%를 EC2에 지출

**기술사의 비용 최적화 플랜**:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ FinOps Cost Optimization Plan ]                          │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Phase 1: 분석 (Month 1)                                                     │
│  ├── Cost Explorer 분석                                                      │
│  │   ├── 서비스별: EC2 70%, RDS 15%, S3 10%, 기타 5%                         │
│  │   └── 인스턴스별: m5.xlarge 40대, c5.2xlarge 10대                         │
│  ├── 사용 패턴 분석                                                          │
│  │   ├── 30대: 24/365 (프로덕션)                                             │
│  │   ├── 10대: 업무시간만 (개발/테스트)                                       │
│  │   └── 10대: 간헐적 (CI/CD)                                                │
│  └── Right-sizing 분석                                                       │
│      └── CPU 평균 15%, 메모리 30% → 다운사이징 가능                          │
│                                                                              │
│  Phase 2: 최적화 (Month 2-3)                                                 │
│  ├── Right-sizing                                                            │
│  │   └── m5.xlarge → m5.large (50% 비용 절감)                               │
│  ├── Reserved Instances 구매                                                 │
│  │   └── 프로덕션 30대 × 1년 RI (40% 할인)                                   │
│  ├── Spot Instances 활용                                                     │
│  │   └── CI/CD 10대 → Spot (70% 할인)                                       │
│  └── 스케줄링                                                                │
│      └── 개발/테스트 10대 → 야간/주말 자동 종료                               │
│                                                                              │
│  Phase 3: 운영 (Ongoing)                                                     │
│  ├── 예산 알림 설정                                                          │
│  ├── RI/SP 활용률 모니터링                                                   │
│  └── 월간 비용 리뷰                                                          │
│                                                                              │
│  [ 예상 절감 효과 ]                                                           │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 항목           │ 현재 비용    │ 최적화 후    │ 절감액       │ 절감률   ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ EC2 (월)       │ $7,000       │ $2,800       │ $4,200       │ 60%     ││
│  │ Right-sizing   │ -            │ -$2,000      │ $2,000       │         ││
│  │ RI 할인        │ -            │ -$1,200      │ $1,200       │         ││
│  │ Spot 활용      │ -            │ -$500        │ $500         │         ││
│  │ 스케줄링       │ -            │ -$500        │ $500         │         ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  연간 절감: $4,200 × 12 = $50,400                                           │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 도입 시 고려사항 체크리스트

| 항목 | 확인 사항 | 비고 |
|---|---|---|
| **RI/SP 활용률** | 구매한 RI가 실제 사용되는지 | 미사용 RI = 비용 낭비 |
| **Spot 중단 빈도** | 인스턴스 타입별 중단율 확인 | Spot Advisor 활용 |
| **태깅 전략** | 비용 할당을 위한 태그 | 프로젝트, 환경, 팀 |
| **예산 알림** | 임계값 초과 시 알림 | 50%, 80%, 100% |
| **Right-sizing** | 과대 프로비저닝 여부 | Compute Optimizer |

### 안티패턴 및 주의사항

**안티패턴 1: RI 과다 구매**
- 문제: 예측보다 사용량 감소 시 미사용 비용 발생
- 해결: Convertible RI 또는 Savings Plans 사용

**안티패턴 2: Spot으로 상시 서비스 운영**
- 문제: 중단 시 서비스 중단
- 해결: On-Demand/RI 기반 + Spot 보조

**안티패턴 3: Right-sizing 없이 RI만 구매**
- 문제: 과대 프로비저닝 인스턴스를 RI로 구매
- 해결: 먼저 Right-sizing 후 RI 구매

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | On-Demand만 | 최적화 후 | 개선율 |
|---|---|---|---|
| **월 EC2 비용** | $10,000 | $4,000 | 60% |
| **RI 활용률** | N/A | 95%+ | - |
| **Spot 활용률** | 0% | 30% | - |
| **예측 가능성** | 낮음 | 높음 | - |

### 미래 전망 및 진화 방향

1. **Savings Plans 확대**: 더 많은 서비스에 SP 적용
2. **AI 기반 최적화**: ML로 최적 RI/SP 조합 추천
3. **Spot 블록 개선**: 더 긴 실행 시간 보장
4. **Marketplace RI**: RI 중개 거래 시장

### ※ 참고 표준/가이드
- **FinOps Foundation**: FinOps 프레임워크
- **AWS Cost Management**: 비용 최적화 가이드
- **Spot Advisor**: Spot 인스턴스 선택 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [오토 스케일링 (Auto Scaling)](@/studynotes/13_cloud_architecture/03_virt/auto_scaling.md) : 인스턴스 자동 조정
- [FinOps](@/studynotes/13_cloud_architecture/_index.md) : 클라우드 재무 관리
- [스케일 업/아웃](@/studynotes/13_cloud_architecture/03_virt/scale_up_vs_scale_out.md) : 확장 전략
- [Right Sizing](@/studynotes/13_cloud_architecture/_index.md) : 적정 크기 산정
- [SRE](@/studynotes/13_cloud_architecture/01_native/sre.md) : 서비스 신뢰성

---

### 👶 어린이를 위한 3줄 비유 설명
1. **온디맨드**는 **'호텔 체크인'**이에요. 언제든 묵을 수 있지만 비싸요.
2. **예약 인스턴스**는 **'1년치 월세'**예요. 오래 살기로 약속하면 할인해줘요.
3. **스팟 인스턴스**는 **'특가 호텔'**이에요. 아주 싸지만, 다른 손님이 오면 방을 비워줘야 해요!
