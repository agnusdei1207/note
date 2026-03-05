+++
title = "FaaS (Function as a Service) / Serverless"
date = 2024-05-04
description = "인프라 관리 없이 비즈니스 로직(함수)만 배포하면 클라우드 제공자가 이벤트 기반으로 자동 실행, 확장, 과금하는 진정한 클라우드 네이티브 컴퓨팅 모델"
weight = 40
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["FaaS", "Serverless", "AWS Lambda", "Event-Driven", "Cold Start", "Cloud Native"]
+++

# FaaS (Function as a Service) / Serverless 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 개발자가 서버 프로비저닝, OS 패치, 스케일링, 로드 밸런싱 등 모든 인프라 운영을 완전히 추상화하고, 오직 비즈니스 로직(함수)만 작성하면 클라우드 제공자가 이벤트(HTTP 요청, DB 변경, 파일 업로드 등)에 반응하여 자동으로 실행·확장·과금하는 **'진정한 클라우드 네이티브'** 컴퓨팅 모델입니다.
> 2. **가치**: 유휴 시간 비용이 0원이며(요청이 없으면 과금 없음), 밀리초 단위 과금으로 **비용 효율성을 70~90% 향상**시킵니다. 또한 인프라 운영 부담이 완전히 사라져 개발자가 비즈니스 가치 창출에만 집중할 수 있습니다.
> 3. **융합**: 이벤트 기반 아키텍처(EDA), 마이크로서비스, API 게이트웨이, 관리형 서비스(DynamoDB, S3)와 결합하여 **'Serverless 스택'**을 구성하며, Kubernetes 기반의 Knative로 하이브리드 서버리스가 가능합니다.

---

## Ⅰ. 개요 (Context & Background)

FaaS(Function as a Service)는 Serverless Computing의 핵심 형태로, 개발자가 '함수(Function)' 단위의 코드 조각만 업로드하면, 클라우드 제공자가 이벤트 발생 시 이를 자동으로 실행합니다. 서버라는 개념이 완전히 사라진 것은 아니지만, 개발자가 인지할 필요가 없어 'Serverless'라고 부릅니다. 사용한 컴퓨팅 시간(밀리초)만큼만 과금되며, 트래픽이 급증하면 수천 개의 함수 인스턴스가 자동으로 생성되고, 트래픽이 없으면 0개로 줄어듭니다.

**💡 비유**: FaaS는 **'택시'**와 같습니다. 내 차(IaaS)를 사려면 구매비용, 보험, 주차비, 정비비를 모두 부담해야 하고, 안 타고 있어도 비용이 듭니다. 하지만 택시(FaaS)는 타고 간 거리와 시간만큼만 요금을 내면 됩니다. 기사(클라우드 제공자)가 운전하고, 정비하고, 기름을 채우니, 나는 그냥 목적지(비즈니스 로직)만 말하면 됩니다.

**등장 배경 및 발전 과정**:
1. **IaaS의 운영 부담**: VM을 직접 관리해야 하는 IaaS는 여전히 OS 패치, 보안 업데이트, 스케일링 설정이 필요했습니다.
2. **AWS Lambda의 혁신 (2014)**: AWS가 re:Invent 2014에서 Lambda를 발표하며 "코드를 업로드하기만 하면, 나머지는 AWS가 알아서 한다"는 패러다임을 도입했습니다.
3. **이벤트 기반 아키텍처의 부상**: S3 파일 업로드, DynamoDB 스트림, API Gateway 요청 등 다양한 이벤트 소스와 결합하여 폭발적으로 채택되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### FaaS 핵심 특성 및 제약사항

| 특성 | 상세 설명 | 내부 동작 메커니즘 | 비고 |
|---|---|---|---|
| **Stateless** | 함수는 상태를 저장하지 않음 | 호출 간 메모리/디스크 공유 불가 | 외부 스토리지(DynamoDB, S3) 필수 |
| **이벤트 트리거** | HTTP, 타이머, DB 변경, 메시지 등 | Event Source Mapping | 다양한 트리거 지원 |
| **자동 스케일링** | 요청 수에 따라 0~수천 인스턴스 | Concurrency Limit 관리 | 급격한 Cold Start 유발 가능 |
| **밀리초 과금** | 실행 시간×메모리 기준 | 1ms 단위 과금 (Lambda) | 유휴 시간 비용 0 |
| **실행 시간 제한** | 최대 15분 (Lambda) | Timeout 강제 종료 | 장기 실행 작업은 부적합 |
| **콜드 스타트** | 첫 호출 시 컨테이너 부팅 지연 | Provisioned Concurrency로 완화 | latency-sensitive 앱 주의 |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                         [ Serverless Architecture ]                         │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │   Client     │     │   Mobile     │     │    IoT       │
    │   (Browser)  │     │    App       │     │   Device     │
    └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
           │                    │                    │
           └────────────────────┼────────────────────┘
                                │ HTTPS
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        [ API Gateway (Managed) ]                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Routing    │  │   Throttle   │  │   Auth       │  │   Request    │   │
│  │              │  │   (Rate      │  │   (Cognito)  │  │   Transform  │   │
│  │              │  │   Limiting)  │  │              │  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │ Trigger
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ FaaS Platform (AWS Lambda 예시) ]                       │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                      [ Worker Pool (Containers) ]                      │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │ │
│  │  │ Function A  │  │ Function A  │  │ Function B  │  │ Function C  │  │ │
│  │  │ Instance 1  │  │ Instance 2  │  │ Instance 1  │  │ Instance 1  │  │ │
│  │  │ (Warm)      │  │ (Warm)      │  │ (Cold→Warm) │  │ (Cold)      │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │ │
│  │                                                                       │ │
│  │  ◄── Auto-scaled 0 → N instances based on concurrent requests        │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                        [ Control Plane ]                               │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │ │
│  │  │  Scheduler   │  │  Invocation  │  │   Metering   │                │ │
│  │  │              │  │  Manager     │  │   & Billing  │                │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                  │                    │                    │
                  ▼                    ▼                    ▼
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│   Managed Services   │  │   Managed Services   │  │   Managed Services   │
│  ┌────────────────┐  │  │  ┌────────────────┐  │  │  ┌────────────────┐  │
│  │   DynamoDB     │  │  │  │      S3        │  │  │  │      SQS       │  │
│  │  (NoSQL DB)    │  │  │  │  (Storage)     │  │  │  │  (Queue)       │  │
│  └────────────────┘  │  │  └────────────────┘  │  │  └────────────────┘  │
│  ┌────────────────┐  │  │  ┌────────────────┐  │  │  ┌────────────────┐  │
│  │   Trigger:     │  │  │  │   Trigger:     │  │  │  │   Trigger:     │  │
│  │   Streams      │  │  │  │   PUT/Object   │  │  │  │   Messages     │  │
│  └────────────────┘  │  │  └────────────────┘  │  │  └────────────────┘  │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘
```

### 심층 동작 원리: 콜드 스타트와 웜 스타트

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    Cold Start vs Warm Start                                │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ Cold Start (첫 호출 또는 유휴 후) ]                                      │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐│
│  │ Request  │ → │ Container│ → │ Runtime  │ → │ Code     │ → │ Response ││
│  │ Arrival  │   │ Allocate │   │ Init     │   │ Init     │   │ Return   ││
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘│
│       │              │              │              │              │       │
│       0ms          50-200ms       100-500ms      50-200ms       0ms      │
│       │              │              │              │              │       │
│       └──────────────┴──────────────┴──────────────┴──────────────┘       │
│                         Total: 200-900ms+ (지연 발생)                       │
│                                                                            │
│  [ Warm Start (컨테이너 재사용) ]                                           │
│  ┌──────────┐                                           ┌──────────┐     │
│  │ Request  │ ─────────────────────────────────────────→ │ Response │     │
│  │ Arrival  │         (컨테이너 이미 실행 중)            │ Return   │     │
│  └──────────┘                                           └──────────┘     │
│       │                                                       │          │
│       0ms                                                    1-5ms       │
│       │                                                       │          │
│       └───────────────────────────────────────────────────────┘          │
│                         Total: 1-10ms (초고속)                             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: AWS Lambda 함수 예시

```python
# AWS Lambda - 이미지 썸네일 생성 함수
import json
import boto3
from PIL import Image
import io
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    S3에 이미지가 업로드되면 트리거되어 썸네일 생성
    Event Source: S3 PUT
    """

    # 1. 이벤트에서 버킷명과 파일명 추출
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # 2. 원본 이미지 다운로드
    response = s3.get_object(Bucket=bucket, Key=key)
    image_data = response['Body'].read()

    # 3. 이미지 처리 (썸네일 생성)
    with Image.open(io.BytesIO(image_data)) as image:
        image.thumbnail((128, 128))  # 썸네일 크기로 리사이징

        # 4. 처리된 이미지를 메모리에 저장
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)

        # 5. 썸네일을 다른 버킷에 업로드
        thumbnail_key = f'thumbnails/{os.path.basename(key)}'
        s3.put_object(
            Bucket='my-thumbnail-bucket',
            Key=thumbnail_key,
            Body=buffer,
            ContentType='image/jpeg'
        )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Thumbnail created successfully',
            'thumbnail_key': thumbnail_key
        })
    }

# Lambda 설정 (Terraform)
"""
resource "aws_lambda_function" "thumbnail_generator" {
  function_name = "thumbnail-generator"
  filename      = "function.zip"
  handler       = "index.lambda_handler"
  runtime       = "python3.11"

  # 메모리와 타임아웃 설정 (과금에 직접 영향)
  memory_size   = 256    # MB
  timeout       = 30     # seconds

  # 환경 변수 (Stateless이므로 설정 외부화)
  environment {
    variables = {
      THUMBNAIL_BUCKET = "my-thumbnail-bucket"
    }
  }
}
"""
```

```yaml
# Serverless Framework - API 서비스 정의
service: brainscience-api

provider:
  name: aws
  runtime: python3.11
  memorySize: 256
  timeout: 10
  environment:
    DYNAMODB_TABLE: ${self:service}-${opt:stage, 'dev'}

functions:
  createPost:
    handler: posts/create.handler
    events:
      - http:
          path: posts
          method: post
          cors: true

  getPost:
    handler: posts/get.handler
    events:
      - http:
          path: posts/{id}
          method: get

  processUpload:
    handler: uploads/process.handler
    events:
      - s3:
          bucket: my-upload-bucket
          event: s3:ObjectCreated:*

resources:
  Resources:
    PostsTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:provider.environment.DYNAMODB_TABLE}
        AttributeDefinitions:
          - AttributeName: id
            AttributeType: S
        KeySchema:
          - AttributeName: id
            KeyType: HASH
        BillingMode: PAY_PER_REQUEST  # Serverless 과금
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: VM vs Container vs Serverless

| 비교 관점 | VM (IaaS) | Container (PaaS/K8s) | Serverless (FaaS) | 상세 분석 |
|---|---|---|---|---|
| **관리 범위** | OS, Runtime, App | Runtime, App | App만 | Serverless가 최소 관리 |
| **시작 시간** | 수분 | 수초 | 수백ms (Cold) / 수ms (Warm) | Serverless는 Cold Start 이슈 |
| **스케일링 단위** | VM | Pod | Function Instance | Serverless가 가장 세밀 |
| **과금 단위** | 시간 | 시간 | ms + 호출 수 | Serverless가 가장 정밀 |
| **유휴 비용** | 있음 | 있음 | 없음 | Serverless만 Zero Idle Cost |
| **최대 실행 시간** | 무제한 | 무제한 | 15분 (Lambda) | 장기 작업은 VM/Container |
| **상태 관리** | 가능 | 가능 | 불가능 (Stateless) | Serverless는 외부 스토리지 필수 |
| **디버깅** | 용이 | 중간 | 어려움 | Serverless는 로컬 재현 어려움 |

### 과목 융합 관점 분석

**네트워크와의 융합**:
- API Gateway가 L7 로드 밸런싱, 인증, 스로틀링을 수행하며, Lambda와 통합됩니다.
- VPC 내 Lambda는 ENI(Elastic Network Interface)를 통해 프라이빗 리소스에 접근합니다.

**데이터베이스와의 융합**:
- Serverless DB(DynamoDB, Aurora Serverless)와 결합하여 완전한 Serverless 스택을 구성합니다.
- Connection Pooling 문제를 해결하기 위해 RDS Proxy가 사용됩니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: Serverless 도입 적합성 평가

**문제 상황**: 이커머스 기업 C사가 주문 처리 시스템을 Serverless로 전환하는 것을 검토 중입니다.

**기술사의 전략적 의사결정**:

| 평가 기준 | Serverless 적합 | Serverless 부적합 |
|---|---|---|
| **트래픽 패턴** | 간헐적, 예측 불가 | 지속적, 높음 |
| **실행 시간** | 수초~수분 | 수분 이상 |
| **상태 관리** | Stateless | Stateful |
| **지연 민감도** | 일반적 | 매우 민감 (< 100ms) |
| **비용 구조** | 변동 비용 선호 | 고정 비용 선호 |

**결론**:
- 주문 생성/업데이트: Serverless 적합 (간헐적, Stateless)
- 주문 분석 배치: EC2/EMR 적합 (장기 실행)
- 실시간 추천: Lambda + DynamoDB 적합 (빠른 응답, Stateless)

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - Chained Lambda**: 여러 Lambda를 순차 호출하면 Cold Start가 누적되어 지연이 급증합니다. Step Functions로 오케스트레이션해야 합니다.
- **체크리스트**:
  - [ ] Cold Start 허용 가능한지 (Provisioned Concurrency 필요 여부)
  - [ ] 함수 실행 시간이 제한 내인지
  - [ ] Stateless 설계가 가능한지
  - [ ] 외부 서비스(DB, API) 연동 시 Connection Pool 관리 방안
  - [ ] 관측 가능성(로그, 트레이싱) 구축 여부

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | EC2 기반 | Serverless | 개선율 |
|---|---|---|---|
| **운영 비용** | 100% | 30% | 70% 절감 (간헐적 트래픽) |
| **개발 속도** | Baseline | 2x | 100% 향상 |
| **인프라 관리** | 100% | 0% | 100% 자동화 |
| **확장 시간** | 수분 | 수백ms | 99% 단축 |

### 미래 전망 및 진화 방향

- **Knative & Serverless Containers**: Kubernetes 위에서 Serverless를 실행하여 하이브리드 모델이 가능해집니다 (Google Cloud Run, AWS App Runner).
- **Edge Functions**: Cloudflare Workers, Vercel Edge Functions가 엣지 로케이션에서 함수를 실행하여 지연을 최소화합니다.
- **WebAssembly (Wasm)**: Wasm 기반 서버리스가 Cold Start를 마이크로초 단위로 단축합니다.

### ※ 참고 표준/가이드
- **Serverless Framework**: 서버리스 애플리케이션 배포 표준 도구
- **AWS Well-Architected Serverless Lens**: 서버리스 아키텍처 모범 사례
- **CNCF Serverless Working Group**: Serverless 워크플로우 표준 (CloudEvents)

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [마이크로서비스 아키텍처 (MSA)](@/studynotes/13_cloud_architecture/01_native/msa.md) : Serverless와 자연스럽게 결합
- [이벤트 기반 아키텍처 (EDA)](@/studynotes/13_cloud_architecture/01_native/eda.md) : Serverless의 핵심 통신 패턴
- [API 게이트웨이](@/studynotes/13_cloud_architecture/01_native/api_gateway.md) : Serverless HTTP 트리거 진입점
- [콜드 스타트 (Cold Start)](@/studynotes/13_cloud_architecture/01_native/cold_start.md) : Serverless의 핵심 과제
- [Knative](@/studynotes/13_cloud_architecture/01_native/knative.md) : Kubernetes 기반 Serverless 플랫폼

---

### 👶 어린이를 위한 3줄 비유 설명
1. Serverless는 **'택시'**예요. 내 차를 사고 기름 넣고 정비할 필요 없이, 가고 싶을 때만 타면 돼요.
2. 그리고 **'초 단위 과금'**이라서, 택시가 도착해서 내릴 때까지 5분이면 5분분만 돈을 내요. 기다리는 시간은 공짜!
3. 운전기사 아저씨(AWS)가 알아서 최적의 길로 빠르게 가주니까, 나는 **'목적지(코드)'**만 말하면 돼요!
