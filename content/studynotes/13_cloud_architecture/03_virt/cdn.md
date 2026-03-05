+++
title = "CDN (Content Delivery Network)"
date = 2026-03-05
description = "전 세계 엣지 서버에 콘텐츠를 캐싱하여 사용자에게 가장 가까운 위치에서 빠르게 전송하는 분산 서버 네트워크의 원리와 아키텍처"
weight = 79
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["CDN", "CloudFront", "Cache", "Edge", "Latency", "Content-Delivery"]
+++

# CDN (Content Delivery Network) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전 세계 여러 지역에 분산 배치된 엣지(Edge) 서버들이 원본(Origin) 서버의 콘텐츠를 캐싱(Caching)하고, 사용자 요청을 지리적으로 가장 가까운 엣지 서버로 라우팅하여 지연 시간을 최소화하는 분산 콘텐츠 전송 아키텍처입니다.
> 2. **가치**: **전 세계 지연 시간 50~80% 단축**, **원본 서버 부하 90% 감소**, **DDoS 방어**, **SSL/TLS 오프로딩**을 통해 사용자 경험 개선과 인프라 비용 절감을 동시에 달성합니다.
> 3. **융합**: 오브젝트 스토리지(S3), DNS(Route 53), WAF(Web Application Firewall), Edge Computing(Lambda@Edge)과 결합하여 현대적 웹 서비스의 필수 인프라로 자리잡았습니다.

---

## Ⅰ. 개요 (Context & Background)

CDN(Content Delivery Network)은 지리적으로 분산된 서버 네트워크를 통해 웹 콘텐츠를 사용자에게 더 빠르게 전달하는 시스템입니다. 전통적인 중앙 집중식 서버 방식에서는 사용자와 서버 간의 물리적 거리가 멀수록 지연 시간이 길어지는데, CDN은 이 문제를 엣지 서버에 콘텐츠를 캐싱하여 해결합니다.

**💡 비유**: CDN은 **'전국에 체인점을 둔 피자 배달'**과 같습니다. 고객이 피자를 주문하면 본점(원본 서버)에서 멀리서 배달하지 않고, 고객과 가장 가까운 체인점(엣지 서버)에서 피자를 만들어 배달합니다. 이미 만들어진 피자(캐시된 콘텐츠)가 있으면 즉시 배달하고, 없으면 본점 레시피대로 만들어(원본에서 가져와서) 배달합니다.

**등장 배경 및 발전 과정**:
1. **초기 인터넷 (1990~1995)**: 중앙 집중식 서버로 전 세계 사용자에게 콘텐츠 제공. 물리적 거리에 따른 지연이 심각했습니다.
2. **Akamai 창립 (1998)**: MIT 연구진이 설립한 최초의 상용 CDN. 분산 캐싱 개념을 상용화했습니다.
3. **스트리밍 시대 (2005~2010)**: YouTube, Netflix 등 동영상 서비스의 부상으로 CDN 수요 폭증.
4. **클라우드 CDN (2010~)**: AWS CloudFront, Azure CDN, Google Cloud CDN 등 클라우드 벤더가 CDN 서비스 제공.
5. **Edge Computing (2018~)**: Lambda@Edge, Cloudflare Workers 등 엣지에서 코드 실행 가능.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 및 특성

| 구성 요소 | 상세 역할 | 기술/프로토콜 | 비고 |
|---|---|---|---|
| **Origin Server** | 원본 콘텐츠 저장소 | HTTP/HTTPS, S3, EC2, ALB | 콘텐츠 소스 |
| **Edge Server (PoP)** | 캐싱 및 사용자 응답 | 전 세계 분산 | Point of Presence |
| **Cache** | 콘텐츠 임시 저장 | 메모리 + SSD | TTL 기반 관리 |
| **DNS/Routing** | 사용자 → 엣지 라우팅 | Anycast, GeoDNS | 지리적 라우팅 |
| **WAF** | 웹 공격 방어 | SQLi, XSS 차단 | 보안 계층 |
| **SSL/TLS** | 암호화/인증서 관리 | 인증서 오프로딩 | HTTPS 종료 |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ CDN Architecture Overview ]                             │
└─────────────────────────────────────────────────────────────────────────────┘

[ 글로벌 CDN 배포 예시 ]

                              [ North America ]
                                   ┌───┐
                             ┌─────│NYC│─────┐
                             │     └───┘     │
                        ┌────┴───┐       ┌───┴────┐
                        │  LAX   │       │  ORD   │
                        └────────┘       └────────┘

    [ Asia Pacific ]                              [ Europe ]
         ┌───┐                                      ┌───┐
    ┌────│NRT│────┐                           ┌────│LHR│────┐
    │    └───┘    │                           │    └───┘    │
┌───┴───┐     ┌───┴───┐                  ┌───┴───┐     ┌───┴───┐
│  ICN  │     │  SIN  │                  │  FRA  │     │  CDG  │
└───────┘     └───────┘                  └───────┘     └───────┘

    [ South America ]     [ Australia ]     [ Africa ]
         ┌─────┐              ┌─────┐         ┌─────┐
         │ GRU │              │ SYD │         │ JNB │
         └─────┘              └─────┘         └─────┘

    PoP (Point of Presence): 엣지 서버 위치
    - 주요 CDN: CloudFront 600+, Cloudflare 300+, Akamai 4000+ PoPs


┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ CDN Request Flow ]                                      │
└─────────────────────────────────────────────────────────────────────────────┘

    [ 캐시 히트 (Cache Hit) 시나리오 ]

    User in Korea              Edge Server in Seoul         Origin in US
         │                           │                           │
         │  1. Request image.jpg     │                           │
         │  ────────────────────────►│                           │
         │                           │                           │
         │                     [Cache Check]                     │
         │                     image.jpg in cache?               │
         │                           │                           │
         │                     YES (Cache Hit!)                  │
         │                           │                           │
         │  2. Return cached content │                           │
         │  ◄────────────────────────│                           │
         │  (TTL: 24h remaining)     │                           │
         │  Latency: ~10ms           │                           │
         │                           │                           │


    [ 캐시 미스 (Cache Miss) 시나리오 ]

    User in Korea              Edge Server in Seoul         Origin in US
         │                           │                           │
         │  1. Request video.mp4     │                           │
         │  ────────────────────────►│                           │
         │                           │                           │
         │                     [Cache Check]                     │
         │                     video.mp4 in cache?               │
         │                           │                           │
         │                     NO (Cache Miss)                   │
         │                           │                           │
         │                           │  2. Fetch from Origin     │
         │                           │  ─────────────────────────►│
         │                           │                           │
         │                           │  3. Origin Response       │
         │                           │  ◄─────────────────────────│
         │                           │  (Cache-Control: max-age)  │
         │                           │                           │
         │                     [Store in Cache]                  │
         │                           │                           │
         │  4. Return to User        │                           │
         │  ◄────────────────────────│                           │
         │  (Subsequent: Cache Hit)  │                           │
         │  Latency: ~200ms (first)  │                           │
         │                           │                           │


┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ CDN Components Detail ]                                 │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────────┐
                    │           DNS Resolution            │
                    │                                     │
                    │  1. User requests www.example.com   │
                    │  2. DNS CNAME: www → d1xyz.cloudfront.net
                    │  3. GeoDNS returns nearest Edge IP  │
                    └──────────────────┬──────────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────┐
                    │           Edge Server               │
                    │                                     │
                    │  ┌───────────────────────────────┐  │
                    │  │      Request Processing       │  │
                    │  │  - SSL Termination            │  │
                    │  │  - WAF Rules Check            │  │
                    │  │  - Rate Limiting              │  │
                    │  └───────────────┬───────────────┘  │
                    │                  │                  │
                    │  ┌───────────────▼───────────────┐  │
                    │  │         Cache Layer           │  │
                    │  │  - L1: Memory Cache (hot)     │  │
                    │  │  - L2: SSD Cache (warm)       │  │
                    │  │  - Cache Key: URL + Headers   │  │
                    │  └───────────────┬───────────────┘  │
                    │                  │                  │
                    │         Hit?  ───┴───  Miss?        │
                    │          │            │            │
                    │          ▼            ▼            │
                    │     [Response]   [Origin Fetch]    │
                    │                                     │
                    └─────────────────────────────────────┘
                                       │
                        (On Cache Miss)│
                                       ▼
                    ┌─────────────────────────────────────┐
                    │          Origin Server              │
                    │                                     │
                    │  - S3 Bucket (Static Content)       │
                    │  - ALB + EC2 (Dynamic Content)      │
                    │  - Lambda (Serverless)              │
                    │                                     │
                    │  Response Headers:                  │
                    │  Cache-Control: max-age=86400       │
                    │  ETag: "abc123"                     │
                    │  Last-Modified: Wed, 05 Mar 2026    │
                    │                                     │
                    └─────────────────────────────────────┘
```

### 심층 동작 원리: 캐시 정책 및 메커니즘

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    CDN Caching Mechanisms                                   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ 캐시 제어 헤더 우선순위 ]                                                  │
│                                                                            │
│  1. Cache-Control (우선순위 높음)                                           │
│     - max-age=86400        : 24시간 캐시                                    │
│     - s-maxage=3600        : CDN 전용 TTL (공유 캐시만)                      │
│     - public               : 모든 캐시 가능                                 │
│     - private              : 브라우저만 캐시 (CDN 제외)                       │
│     - no-cache             : 재검증 필요                                    │
│     - no-store             : 캐시 금지                                      │
│     - stale-while-revalidate=3600 : 만료 후 1시간 동안 비동기 갱신           │
│                                                                            │
│  2. Expires (레거시)                                                        │
│     - Expires: Wed, 05 Mar 2027 00:00:00 GMT                              │
│     - 절대 시간 기준                                                        │
│                                                                            │
│  3. ETag / Last-Modified (재검증용)                                         │
│     - If-None-Match: "abc123" → 304 Not Modified                          │
│     - If-Modified-Since: ... → 304 Not Modified                           │
│                                                                            │
│  [ CloudFront 캐시 동작 ]                                                    │
│                                                                            │
│  ┌───────────────────────────────────────────────────────────────────────┐│
│  │ Origin Response          │ CloudFront Behavior        │ User Impact  ││
│  ├───────────────────────────────────────────────────────────────────────┤│
│  │ Cache-Control: max-age=N │ 캐시 N초                    │ 빠른 응답    ││
│  │ Cache-Control: no-cache  │ 매번 원본 검증              │ 약간 느림    ││
│  │ Cache-Control: no-store  │ 캐시 안 함                  │ 매번 느림    ││
│  │ Cache-Control: private   │ 캐시 안 함                  │ 매번 느림    ││
│  │ (헤더 없음)              │ Default TTL 적용           │ 설정 기준    ││
│  │ Set-Cookie 있음          │ 기본적으로 캐시 안 함        │ 매번 느림    ││
│  └───────────────────────────────────────────────────────────────────────┘│
│                                                                            │
│  [ 캐시 무효화 (Cache Invalidation) ]                                        │
│                                                                            │
│  1. TTL 만료 대기 (Passive)                                                │
│     - 자동이지만 최대 TTL까지 오래된 콘텐츠 노출                              │
│                                                                            │
│  2. Invalidating Paths (Active)                                            │
│     - POST /2016-03-05/distribution/EDFDVBD63232D/invalidations           │
│     - CallerReference: unique-id-123                                       │
│     - Paths: /images/*, /styles/main.css                                  │
│     - 전파 시간: 수초~수분                                                  │
│                                                                            │
│  3. 버전 관리 (Versioning)                                                  │
│     - /v1.0.0/main.js 대신 /main.js?v=1.0.0                               │
│     - 캐시 키가 달라짐 → 즉시 새 버전                                        │
│                                                                            │
│  4. 파일명 해시 (Content Hashing)                                           │
│     - main.a1b2c3d4.js (내용 기반 해시)                                     │
│     - 내용 변경 → 파일명 변경 → 완전히 새로운 URL                            │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: CloudFront 배포 구성

```yaml
# CloudFormation 템플릿: CloudFront Distribution
AWSTemplateFormatVersion: '2010-09-09'
Description: 'CloudFront CDN Distribution with S3 Origin'

Parameters:
  BucketName:
    Type: String
    Description: S3 bucket name for origin
  CertificateArn:
    Type: String
    Description: ACM certificate ARN for HTTPS
  DomainName:
    Type: String
    Description: Custom domain name

Resources:
  # S3 버킷 (오리진)
  OriginBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref BucketName
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  # S3 버킷 정책 (CloudFront 전용 접근)
  OriginBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref OriginBucket
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Sid: AllowCloudFrontAccess
            Effect: Allow
            Principal:
              Service: cloudfront.amazonaws.com
            Action: s3:GetObject
            Resource: !Sub '${OriginBucket.Arn}/*'
            Condition:
              StringEquals:
                AWS:SourceArn: !Sub 'arn:aws:cloudfront::${AWS::AccountId}:distribution/${CloudFrontDistribution}'

  # CloudFront Origin Access Control
  OriginAccessControl:
    Type: AWS::CloudFront::OriginAccessControl
    Properties:
      OriginAccessControlConfig:
        Name: !Sub '${AWS::StackName}-OAC'
        OriginAccessControlOriginType: s3
        SigningBehavior: always
        SigningProtocol: sigv4

  # CloudFront 배포
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        # 댁 관련 설정
        Comment: !Sub 'CDN for ${DomainName}'
        Enabled: true
        PriceClass: PriceClass_100  # UseOnlyUS_Europe_Asia (비용 최적화)

        # 커스텀 도메인
        Aliases:
          - !Ref DomainName
          - !Sub 'www.${DomainName}'

        # SSL/TLS 설정
        ViewerCertificate:
          AcmCertificateArn: !Ref CertificateArn
          SslSupportMethod: sni-only
          MinimumProtocolVersion: TLSv1.2_2021

        # HTTP → HTTPS 리다이렉트
        DefaultCacheBehavior:
          TargetOriginId: S3Origin
          ViewerProtocolPolicy: redirect-to-https
          AllowedMethods:
            - GET
            - HEAD
            - OPTIONS
          CachedMethods:
            - GET
            - HEAD
          CachePolicyId: 658327ea-f89d-4fab-a63d-7e88639e58f6  # CachingOptimized
          OriginRequestPolicyId: 88a5eaf4-2fd4-4709-b370-b4c650ea3fcf  # CORS-S3Origin
          Compress: true  # Gzip 압축

        # 오리진 설정
        Origins:
          - Id: S3Origin
            DomainName: !GetAtt OriginBucket.RegionalDomainName
            S3OriginConfig:
              OriginAccessIdentity: ''
            OriginAccessControlId: !GetAtt OriginAccessControl.Id

        # 캐시 동작 (API용)
        CacheBehaviors:
          - PathPattern: /api/*
            TargetOriginId: APIOrigin
            ViewerProtocolPolicy: https-only
            AllowedMethods:
              - GET
              - HEAD
              - OPTIONS
              - PUT
              - POST
              - PATCH
              - DELETE
            CachePolicyId: 4135ea2d-6df8-44a3-9df3-4b5a84be39ad  # CachingDisabled
            OriginRequestPolicyId: 216adef6-5c7f-47e4-b989-5192e780329f  # AllViewerExceptHostHeader

        # 추가 오리진 (API)
        Origins:
          - Id: APIOrigin
            DomainName: !Sub 'api.${DomainName}'
            CustomOriginConfig:
              OriginProtocolPolicy: https-only
              OriginSSLProtocols:
                - TLSv1.2

        # 커스텀 에러 응답
        CustomErrorResponses:
          - ErrorCode: 404
            ResponsePagePath: /404.html
            ResponseCode: 404
            ErrorCachingMinTTL: 300
          - ErrorCode: 500
            ResponsePagePath: /500.html
            ResponseCode: 500
            ErrorCachingMinTTL: 0

        # Geo Restriction (선택적)
        Restrictions:
          GeoRestriction:
            RestrictionType: whitelist
            Locations:
              - KR
              - US
              - JP

        # 웹 애플리케이션 방화벽 (WAF)
        WebACLId: !Ref WebACL

        # 로깅
        Logging:
          Bucket: !GetAtt LogBucket.DomainName
          Prefix: cloudfront-logs/
          IncludeCookies: false

  # WAF Web ACL
  WebACL:
    Type: AWS::WAFv2::WebACL
    Properties:
      Name: !Sub '${AWS::StackName}-WAF'
      Scope: CLOUDFRONT
      DefaultAction:
        Allow: {}
      Rules:
        # AWS Managed Rules
        - Name: AWSManagedRulesCommonRuleSet
          Priority: 1
          OverrideAction:
            None: {}
          Statement:
            ManagedRuleGroupStatement:
              VendorName: AWS
              Name: AWSManagedRulesCommonRuleSet
        # 레이트 기반 규칙
        - Name: RateLimitRule
          Priority: 2
          Action:
            Block: {}
          Statement:
            RateBasedStatement:
              Limit: 10000
              AggregateKeyType: IP
          VisibilityConfig:
            SampledRequestsEnabled: true
            CloudWatchMetricsEnabled: true
            MetricName: RateLimitRule

  # 로그 버킷
  LogBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${BucketName}-logs'
      LifecycleConfiguration:
        Rules:
          - Id: DeleteOldLogs
            Status: Enabled
            ExpirationInDays: 90

Outputs:
  DistributionId:
    Description: CloudFront Distribution ID
    Value: !Ref CloudFrontDistribution
  DistributionDomainName:
    Description: CloudFront Domain Name
    Value: !GetAtt CloudFrontDistribution.DomainName
  CDNUrl:
    Description: Full CDN URL
    Value: !Sub 'https://${DomainName}'
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 주요 CDN 프로바이더

| 비교 관점 | AWS CloudFront | Cloudflare | Akamai | Azure CDN |
|---|---|---|---|---|
| **PoP 수** | 600+ | 310+ | 4,000+ | 200+ |
| **AWS 통합** | 최고 | 좋음 | 중간 | 낮음 |
| **가격 모델** | 사용량 기반 | Flat + Usage | Enterprise | 사용량 기반 |
| **Edge Compute** | Lambda@Edge | Workers | EdgeWorkers | Functions |
| **WAF 포함** | 별도 | Pro 이상 | 포함 | 별도 |
| **DDoS 방어** | Shield | 무료 포함 | 포함 | DDoS Protection |
| **Real-time Logs** | 지원 | Enterprise | 지원 | 지원 |

### CDN 성능 지표 및 벤치마크

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ CDN Performance Metrics ]                                │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [ 캐시 히트율 (Cache Hit Ratio) ]                                            │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 콘텐츠 유형        │ 목표 Hit Ratio   │ 일반적 TTL      │ 비고          ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ 정적 이미지        │ 95%+             │ 1년            │ 버전 관리     ││
│  │ CSS/JS 파일        │ 95%+             │ 1년            │ 해시 파일명   ││
│  │ 폰트               │ 98%+             │ 1년            │ 불변          ││
│  │ 동영상             │ 90%+             │ 7일            │ 스트리밍      ││
│  │ API 응답 (캐시형)  │ 50-80%           │ 1-60분         │ 동적 캐시     ││
│  │ HTML (동적)        │ 0-20%            │ 0-5초          │ 캐시 비권장   ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  [ 지연 시간 개선 ]                                                          │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 사용자 위치    │ Origin 직접    │ CDN 경유      │ 개선율              ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ 한국 → 미국    │ 150-200ms      │ 20-50ms       │ 75-85%              ││
│  │ 한국 → 유럽    │ 200-300ms      │ 30-60ms       │ 80-85%              ││
│  │ 미국 → 아시아  │ 100-150ms      │ 15-30ms       │ 80-85%              ││
│  │ 국내 (한국)    │ 10-30ms        │ 5-15ms        │ 50%                 ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  [ 비용 비교 (월 100TB 전송 기준) ]                                           │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 서비스          │ 비용 (USD)      │ 비고                                     ││
│  ├─────────────────────────────────────────────────────────────────────────┤│
│  │ Origin 직접     │ $8,500          │ 데이터 전송비 + Origin 운영비            ││
│  │ CloudFront      │ $8,500 + Origin │ 데이터 전송비 (Origin 부하 90% 감소)      ││
│  │ Cloudflare Pro  │ $200 + $7,000   │ Flat 요금 + 데이터 전송                  ││
│  │ Akamai          │ Enterprise      │ 협상 필요                                ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 과목 융합 관점 분석

**네트워크와의 융합**:
- **Anycast 라우팅**: 동일 IP가 여러 엣지에 할당되어 BGP가 최단 경로 선택
- **TCP 최적화**: 엣지 서버에서 TCP 연결 종료, Keep-Alive 관리
- **HTTP/2, HTTP/3**: 멀티플렉싱, QUIC 프로토콜 지원

**보안(Security)과의 융합**:
- **DDoS 방어**: 볼류메트릭 공격을 분산된 엣지에서 흡수
- **WAF**: OWASP Top 10 공격(SQLi, XSS) 차단
- **SSL/TLS 오프로딩**: 엣지에서 암호화/복호화 처리

**운영체제(OS)와의 융합**:
- **메모리 캐시**: 엣지 서버의 메모리에 핫 콘텐츠 캐싱
- **디스크 캐시**: SSD에 웜 콘텐츠 저장

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 글로벌 웹 서비스 CDN 도입

**문제 상황**: 한국에서 시작한 웹 서비스가 글로벌 확장하면서 미국/유럽 사용자 불만 증가

**기술사의 의사결정 프로세스**:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ 글로벌 CDN 도입 전략 ]                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. 현황 분석                                                                │
│     ├── 현재 Origin: 서울 (ap-northeast-2)                                   │
│     ├── 사용자 분포: 한국 60%, 미국 25%, 유럽 10%, 기타 5%                    │
│     ├── 콘텐츠 유형: 정적 이미지 70%, API 20%, HTML 10%                       │
│     └── 문제점: 미국/유럽 사용자 지연 200ms+                                  │
│                                                                              │
│  2. CDN 선택 기준                                                            │
│     ├── AWS 인프라 사용 중 → CloudFront 선택                                 │
│     ├── Price Class: PriceClass_100 (비용 최적화)                            │
│     └── WAF + Shield Standard 포함                                          │
│                                                                              │
│  3. 아키텍처 설계                                                             │
│                                                                              │
│     ┌─────────────────────────────────────────────────────────────────────┐ │
│     │                        CloudFront Distribution                       │ │
│     │                                                                     │ │
│     │  Route53                                                            │ │
│     │     │                                                               │ │
│     │     ├── www.example.com → Alias → CloudFront                       │ │
│     │     └── api.example.com → Alias → CloudFront                       │ │
│     │                                                                     │ │
│     │  CloudFront Behaviors:                                              │ │
│     │  ┌───────────────────────────────────────────────────────────────┐ │ │
│     │  │ Path Pattern   │ Origin     │ Cache Policy      │ TTL       │ │ │
│     │  ├───────────────────────────────────────────────────────────────┤ │ │
│     │  │ /static/*      │ S3 Bucket  │ CachingOptimized  │ 1 year    │ │ │
│     │  │ /images/*      │ S3 Bucket  │ CachingOptimized  │ 1 year    │ │ │
│     │  │ /api/*         │ ALB/EC2    │ CachingDisabled   │ 0         │ │ │
│     │  │ /*             │ S3 Bucket  │ CachingOptimized  │ 1 day     │ │ │
│     │  └───────────────────────────────────────────────────────────────┘ │ │
│     │                                                                     │ │
│     │  Edge Locations:                                                    │ │
│     │  - Seoul (ICN)                                                     │ │
│     │  - Tokyo (NRT)                                                     │ │
│     │  - Los Angeles (LAX)                                               │ │
│     │  - Frankfurt (FRA)                                                 │ │
│     │  - London (LHR)                                                    │ │
│     │                                                                     │ │
│     └─────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  4. 예상 효과                                                                │
│     ├── 한국: 10-30ms → 5-15ms (50% 개선)                                   │
│     ├── 미국: 150-200ms → 20-40ms (80% 개선)                                │
│     ├── 유럽: 200-300ms → 30-50ms (85% 개선)                                │
│     └── Origin 부하: 70% 감소                                               │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 도입 시 고려사항 체크리스트

| 항목 | 확인 사항 | 비고 |
|---|---|---|
| **캐시 전략** | 정적/동적 콘텐츠 분리 | TTL, Cache Policy |
| **무효화** | 배포 시 캐시 무효화 방안 | Invalidations |
| **보안** | HTTPS, WAF, DDoS | Shield, WAF |
| **비용** | 데이터 전송비, 요청 수 | Price Class 선택 |
| **모니터링** | Cache Hit Ratio, 지연 시간 | CloudWatch |

### 안티패턴 및 주의사항

**안티패턴 1: 동적 콘텐츠 과도한 캐싱**
- 문제: 개인화된 데이터가 다른 사용자에게 노출
- 해결: Cache-Control: private, no-store

**안티패턴 2: 짧은 TTL + 잦은 무효화**
- 문제: 무효화 비용 증가, Origin 부하
- 해결: 버전 관리, 해시 파일명 사용

**안티패턴 3: CORS 미설정**
- 문제: 교차 출처 요청 실패
- 해결: Origin Request Policy에 CORS 헤더 포함

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | CDN 없음 | CDN 적용 | 개선율 |
|---|---|---|---|
| **글로벌 지연** | 150-300ms | 20-50ms | 75-85% |
| **Origin 부하** | 100% | 10-30% | 70-90% |
| **가용성** | 99.9% | 99.99%+ | 10x |
| **DDoS 방어** | 없음 | 포함 | 보안 강화 |

### 미래 전망 및 진화 방향

1. **Edge Computing 확대**: Cloudflare Workers, Lambda@Edge로 더 많은 로직을 엣지에서 처리
2. **HTTP/3/QUIC**: UDP 기반 프로토콜로 지연 시간 추가 단축
3. **AI 기반 캐싱**: 머신러닝으로 캐시 프리페칭 최적화
4. **Edge AI**: 엣지에서 추론 실행 (TinyML)

### ※ 참고 표준/가이드
- **RFC 7234**: HTTP Caching 표준
- **AWS CloudFront Best Practices**: AWS 가이드
- **Cloudflare Learning Center**: CDN 교육 자료

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [오브젝트 스토리지 (Object Storage)](@/studynotes/13_cloud_architecture/03_virt/object_storage.md) : CDN 오리진
- [로드 밸런서 (Load Balancer)](@/studynotes/13_cloud_architecture/03_virt/load_balancer.md) : 트래픽 분산
- [DNS](@/studynotes/13_cloud_architecture/_index.md) : GeoDNS 라우팅
- [WAF](@/studynotes/13_cloud_architecture/_index.md) : 웹 방화벽
- [Edge Computing](@/studynotes/13_cloud_architecture/03_virt/edge_computing.md) : 엣지 컴퓨팅

---

### 👶 어린이를 위한 3줄 비유 설명
1. CDN은 **'전국 체인점이 있는 피자 배달'**과 같아요. 고객과 가까운 체인점에서 배달해요.
2. **'자주 주문하는 피자는 미리 만들어둬요'**. 주문하면 바로 배달할 수 있게요. (캐싱)
3. 덕분에 **'멀리서도 빠르게 배달받을 수 있어요'**. 한국에서 주문해도 미국 체인점에서 바로 만들어 줘요!
