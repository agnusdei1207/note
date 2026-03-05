+++
title = "데이터 그래비티 (Data Gravity)"
date = "2026-03-05"
[extra]
categories = "studynotes-cloud"
tags = ["cloud", "data-gravity", "architecture", "migration", "vendor-lock-in"]
+++

# 데이터 그래비티 (Data Gravity)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 그래비티는 대용량 데이터가 축적될수록 애플리케이션과 서비스가 그 데이터 주변으로 끌려가는 현상으로, 중력(Gravity)처럼 데이터 질량에 비례하여 인력이 강해집니다.
> 2. **가치**: 데이터 그래비티 이해를 통해 클라우드 마이그레이션 비용 예측, 벤더 락인 위험 평가, 하이브리드 아키텍처 설계의 핵심 의사결정을 내릴 수 있습니다.
> 3. **융합**: 네트워크 대역폭 비용 모델, 스토리지 계층화 전략, 데이터 지역성(Locality) 최적화와 결합하여 엔터프라이즈 데이터 전략의 기본 원리로 작동합니다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의
데이터 그래비티(Data Gravity)는 2010년 GE(Global Environment)의 소프트웨어 아키텍트 Dave McCrory가 처음 제안한 개념으로, 데이터가 물리적 질량처럼 주변의 애플리케이션, 서비스, 비즈니스 로직을 자신이 위치한 곳으로 끌어당기는 현상을 의미합니다. 데이터의 양이 많을수록(질량 증가), 접근 빈도가 높을수록(밀도 증가), 그 "인력"은 강해져서 결국 새로운 서비스와 분석 파이프라인이 데이터가 있는 곳으로 이주하게 됩니다.

### 💡 비유
데이터 그래비티는 "태양계 행성 공전"과 같습니다. 태양(대용량 데이터)이 질량이 커서 강한 중력을 가지면, 주변의 행성(애플리케이션), 위성(서비스), 혜성(트래픽)들이 모두 태양 주위를 공전하게 됩니다. 태양을 옮기려면 엄청난 에너지가 필요하듯, 대용량 데이터를 다른 클라우드로 옮기는 것도 비용과 시간이 막대하게 듭니다.

### 등장 배경 및 발전 과정

#### 1. 기존 IT 아키텍처의 한계
- **데이터 이동 비용 폭증**: 클라우드 간 데이터 전송 비용(Egress Fee)이 워크로드 비용을 넘어서는 현상
- **지연 시간 민감성**: 빅데이터 분석, AI 학습에서 데이터 이동 지연이 병목으로 작용
- **규제 준수 압력**: 데이터 국외 이전 제한으로 인한 데이터 지역성 강제

#### 2. 패러다임 변화
```
2010년: Dave McCrory, "Data Gravity" 개념 최초 제안
2015년: AWS S3 데이터 축적으로 고객 서비스 S3 내부로 이주 가속화
2018년: 멀티 클라우드 전략에서 데이터 그래비티 핵심 고려사항으로 부상
2020년: 데이터 메시(Data Mesh) 아키텍처에서 그래비티 기반 분산 원칙 정립
2023년: 생성형 AI 학습 데이터 그래비티로 인한 하이퍼스케일러 독점 심화
```

#### 3. 비즈니스적 요구사항
- **비용 최적화**: 데이터 이동 비용(Egress) vs 컴퓨팅 이동 비용 비교 분석
- **성능 최소화**: 데이터-컴퓨팅 동일 위치 배치로 지연 시간 단축
- **전략적 유연성**: 벤더 락인 방지를 위한 데이터 이식성 확보

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|-----------|------|
| **데이터 질량 (Data Mass)** | 축적된 데이터 총량 | TB/PB 단위 저장 용량, 테이블/파일 개수 | S3, HDFS, Data Lake | 행성의 질량 |
| **데이터 밀도 (Data Density)** | 단위 시간당 접근 빈도 | IOPS, QPS, 트랜잭션 처리량 | RDBMS, Cache, CDN | 행성의 밀도 |
| **애플리케이션 인력 (App Attraction)** | 데이터 주변 서비스 집중 | 서비스 배치, 컨테이너 스케줄링 | K8s Affinity, Lambda | 위성 궤도 진입 |
| **이동 비용 (Transfer Cost)** | 데이터 전송 비용 | Egress Fee, 네트워크 대역폭 | Direct Connect, VPN | 우주선 발사 비용 |
| **지연 가속도 (Latency Acceleration)** | 거리에 따른 지연 증가 | RTT, TCP 윈도우, 대역폭-지연 곱 | Edge Computing | 빛의 속도 한계 |
| **규제 중력장 (Regulatory Field)** | 법적 데이터 거주 요구 | 데이터 국외 이전 금지, GDPR | Sovereign Cloud | 블랙홀 사건 지평선 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          데이터 그래비티 시각화 모델                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│        ┌──────────────────────────────────────────────────────────┐            │
│        │                 Cloud Region A (Primary)                 │            │
│        │                                                          │            │
│        │    ┌─────────────────────────────────────────────┐      │            │
│        │    │          Data Core (Mass: 500PB)             │      │            │
│        │    │    ┌─────────────────────────────────┐      │      │            │
│        │    │    │   ████████████████████████████  │      │      │            │
│        │    │    │   █ S3 Data Lake (300PB)      █  │      │      │            │
│        │    │    │   ████████████████████████████  │      │      │            │
│        │    │    │   ████████████████████████████  │      │      │            │
│        │    │    │   █ RDBMS (100TB)             █  │      │      │            │
│        │    │    │   ████████████████████████████  │      │      │            │
│        │    │    │   █ NoSQL (50TB)              █  │      │      │            │
│        │    │    │   ████████████████████████████  │      │      │            │
│        │    │    └─────────────────────────────────┘      │      │            │
│        │    │                    ▲                         │      │            │
│        │    │                    │ 강한 중력               │      │            │
│        │    └────────────────────┼─────────────────────────┘      │            │
│        │                         │                                 │            │
│        │    ┌────────────────────┼─────────────────────────┐      │            │
│        │    │   ○ App Service A  │  ○ App Service B         │      │            │
│        │    │   ○ Analytics      │  ○ ML Training           │      │            │
│        │    │   ○ ETL Pipeline   │  ○ Reporting             │      │            │
│        │    │   ○ API Gateway    │  ○ Stream Processing     │      │            │
│        │    └───────────────────────────────────────────────┘      │            │
│        │                                                          │            │
│        └──────────────────────────────────────────────────────────┘            │
│                                      │                                         │
│                                      │ Egress Cost: $0.09/GB                   │
│                                      │ Latency: 100ms                          │
│                                      │ Bandwidth: 10Gbps (Shared)              │
│                                      ▼                                         │
│        ┌──────────────────────────────────────────────────────────┐            │
│        │                 Cloud Region B (Secondary)               │            │
│        │                                                          │            │
│        │    ┌─────────────────────────────────────────────┐      │            │
│        │    │       Data Replica (Mass: 50PB - DR Only)    │      │            │
│        │    │         ████████████████████                 │      │            │
│        │    │         █ S3 Replica (50PB) █                │      │            │
│        │    │         ████████████████████                 │      │            │
│        │    └─────────────────────────────────────────────┘      │            │
│        │                                                          │            │
│        │    (약한 중력: 서비스 분산 유도)                          │            │
│        │                                                          │            │
│        └──────────────────────────────────────────────────────────┘            │
│                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────┐      │
│   │                      데이터 그래비티 수식 모델                       │      │
│   │                                                                     │      │
│   │   Attraction Force (F) = k × (Data_Mass × App_Complexity) / d²     │      │
│   │                                                                     │      │
│   │   F: 데이터가 앱을 끌어당기는 힘                                     │      │
│   │   k: 상수 (네트워크 비용, 규제 강도)                                  │      │
│   │   Data_Mass: 데이터 양 (TB/PB)                                      │      │
│   │   App_Complexity: 앱의 데이터 의존도                                 │      │
│   │   d: 데이터-앱 간 거리 (네트워크 홉, 지리적 거리)                      │      │
│   │                                                                     │      │
│   └─────────────────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

#### ① 데이터 그래비티 매트릭스 분석

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    데이터 그래비티 영향도 매트릭스                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│   데이터 크기   │  작음 (<1TB)  │  중간 (1-100TB)  │  큼 (>100TB)          │
│   ─────────────┼───────────────┼──────────────────┼─────────────────────   │
│   접근 빈도     │               │                  │                        │
│   낮음 (Cold)   │      낮음      │       중간       │      높음             │
│                 │   이동 자유    │   아카이브 고려   │  강한 락인            │
│   ─────────────┼───────────────┼──────────────────┼─────────────────────   │
│   중간 (Warm)   │      낮음      │       높음       │     매우 높음          │
│                 │  캐시 전략     │  로컬 캐시 필수   │  동일 리전 배치 필수    │
│   ─────────────┼───────────────┼──────────────────┼─────────────────────   │
│   높음 (Hot)    │     중간       │     매우 높음     │     극단적            │
│                 │  CDN 활용     │  전용 연결 필요   │  물리적 동일 데이터센터 │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

※ 그래비티 등급 산정 공식:
   Gravity_Score = log10(Data_TB) × Access_Frequency × Dependency_Factor

   - Dependency_Factor: 1~10 (앱이 데이터에 얼마나 의존하는가)
   - Score > 100: 강한 그래비티 (이동 비현실적)
   - Score 10-100: 중간 그래비티 (비용-이득 분석 필요)
   - Score < 10: 약한 그래비티 (이동 자유로움)
```

#### ② 데이터 그래비티 기반 의사결정 알고리즘

```python
class DataGravityAnalyzer:
    """데이터 그래비티 분석 및 의사결정 지원 시스템"""

    def __init__(self):
        self.EGRESS_COST_PER_GB = {
            'aws': 0.09,
            'azure': 0.087,
            'gcp': 0.12
        }

    def calculate_migration_cost(self, data_size_tb: float, source_cloud: str,
                                  target_cloud: str) -> dict:
        """
        데이터 마이그레이션 비용 계산

        Args:
            data_size_tb: 이동할 데이터 크기 (TB)
            source_cloud: 출발 클라우드 ('aws', 'azure', 'gcp')
            target_cloud: 목표 클라우드

        Returns:
            비용 상세 분석 딕셔너리
        """
        data_size_gb = data_size_tb * 1024

        # 1. Egress 비용 (출발 클라우드)
        egress_cost = data_size_gb * self.EGRESS_COST_PER_GB[source_cloud]

        # 2. 데이터 전송 시간 (10Gbps 기준)
        transfer_time_hours = (data_size_gb * 8) / (10 * 3600)  # 10Gbps

        # 3. 스토리지 중복 비용 (마이그레이션 기간 중)
        storage_overlap_days = max(7, transfer_time_hours / 24 * 2)  # 버퍼 포함
        storage_cost_per_tb_month = 23  # S3 Standard 기준
        overlap_cost = (data_size_tb * storage_cost_per_tb_month / 30) * storage_overlap_days

        # 4. 총 비용
        total_cost = egress_cost + overlap_cost

        return {
            'egress_cost': egress_cost,
            'transfer_time_hours': transfer_time_hours,
            'storage_overlap_cost': overlap_cost,
            'total_migration_cost': total_cost,
            'cost_per_tb': total_cost / data_size_tb if data_size_tb > 0 else 0
        }

    def assess_lock_in_risk(self, data_profile: dict) -> dict:
        """
        벤더 락인 위험도 평가

        Args:
            data_profile: {
                'data_size_tb': float,
                'access_frequency': 'low'|'medium'|'high',
                'dependency_services': list,  # ['dynamodb', 'lambda', 's3_select']
                'has_export_format': bool
            }
        """
        # 점수 계산
        size_score = min(100, data_profile['data_size_tb'] / 10)  # 10TB당 1점, 최대 100

        freq_score = {'low': 10, 'medium': 50, 'high': 100}[data_profile['access_frequency']]

        # 독점 서비스 의존도 (개당 20점)
        proprietary_services = ['dynamodb', 'lambda', 's3_select', 'aurora_serverless',
                               'azure_cosmos', 'bigquery', 'spanner']
        dep_count = sum(1 for s in data_profile['dependency_services']
                       if s.lower() in proprietary_services)
        dependency_score = min(100, dep_count * 20)

        # 이식성 가산점
        portability_bonus = -30 if data_profile.get('has_export_format') else 0

        # 총 락인 점수
        lock_in_score = (size_score * 0.3 + freq_score * 0.3 +
                        dependency_score * 0.4 + portability_bonus)
        lock_in_score = max(0, min(100, lock_in_score))

        # 위험 등급
        if lock_in_score >= 70:
            risk_level = 'CRITICAL'
            recommendation = '즉시 이식성 확보 전략 수립 필요'
        elif lock_in_score >= 40:
            risk_level = 'HIGH'
            recommendation = '표준 포맷 변환 및 추출 파이프라인 구축 권장'
        elif lock_in_score >= 20:
            risk_level = 'MEDIUM'
            recommendation = '정기적인 데이터 백업 및 포맷 검토 필요'
        else:
            risk_level = 'LOW'
            recommendation = '현재 수준 유지 가능'

        return {
            'lock_in_score': lock_in_score,
            'risk_level': risk_level,
            'recommendation': recommendation,
            'breakdown': {
                'size_score': size_score,
                'frequency_score': freq_score,
                'dependency_score': dependency_score
            }
        }

    def recommend_architecture(self, data_gravity_score: float,
                               latency_requirement_ms: float) -> str:
        """
        데이터 그래비티 점수에 따른 아키텍처 추천
        """
        if data_gravity_score > 100:
            if latency_requirement_ms < 10:
                return "Same-Datacenter Deployment: 데이터와 동일 데이터센터에 앱 배치"
            else:
                return "Same-Region Deployment: 동일 리전 내 앱 배치 (AZ 분산 가능)"

        elif data_gravity_score > 50:
            if latency_requirement_ms < 50:
                return "Direct Connect + Edge Cache: 전용선 + 엣지 캐시 조합"
            else:
                return "Cross-Region with Async Replication: 비동기 복제로 지역 분산"

        else:
            return "Multi-Cloud Active-Active: 데이터 분산으로 멀티 클라우드 활성화"
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 데이터 그래비티 대응 전략

| 전략 | 설명 | 장점 | 단점 | 적용 시나리오 |
|------|------|------|------|--------------|
| **데이터 중심 배치** | 앱을 데이터 위치로 이동 | 이동 비용 0, 지연 최소화 | 벤더 락인 심화 | 대용량 분석, AI 학습 |
| **데이터 분산 복제** | 데이터를 여러 리전에 복제 | 읽기 지연 감소, 가용성 향상 | 스토리지 비용 N배, 일관성 복잡 | 글로벌 서비스, CDN |
| **데이터 계층화** | Hot/Warm/Cold 계층 분리 | 비용 최적화, 핵심만 이동 | 계층 간 이동 관리 복잡 | 로그, 백업, 아카이브 |
| **스트리밍 처리** | 배치 대신 스트리밍으로 실시간 이동 | 지연 최소화, 버퍼링 감소 | 순서 보장, 중복 처리 복잡 | IoT, 실시간 분석 |
| **엣지 컴퓨팅** | 데이터 발생지에서 처리 | 데이터 이동 최소화 | 엣지 관리 복잡성 | 제조, 자율주행 |
| **데이터 패브릭** | 가상화 레이어로 논리적 통합 | 물리적 이동 없이 접근 | 성능 오버헤드, 벤더 미성숙 | 하이브리드, 멀티 클라우드 |

### 과목 융합 관점 분석

#### [클라우드 + 네트워크] 데이터 그래비티와 네트워크 비용
```
클라우드 네트워크 비용 구조 분석:

1. Egress 비용 (데이터 나갈 때)
   - AWS: $0.09/GB (첫 100TB)
   - Azure: $0.087/GB
   - GCP: $0.12/GB
   - 월 1PB 전송 시: $90,000+

2. Ingress 비용 (데이터 들어올 때)
   - 대부분 무료 → 데이터를 받아들이는 쪽이 유리

3. 동일 리전 내 전송
   - AWS: 무료 (동일 AZ) / $0.01/GB (다른 AZ)
   - → 강한 데이터 그래비티 형성 요인

4. Direct Connect / ExpressRoute
   - 고정 월 요금 + 데이터 전송량 요금
   - 대량 전송 시 Egress보다 저렴할 수 있음

융합 설계 원칙:
- 데이터 무브먼트(Outbound) 최소화
- 컴퓨팅 무브먼트(Inbound) 최대화
- 네트워크 비용 = f(거리² × 대역폭)
```

#### [클라우드 + 데이터베이스] 분산 DB와 그래비티
```
분산 데이터베이스에서의 데이터 그래비티:

1. 리전 간 복제 (Cross-Region Replication)
   - 쓰기: Primary 리전에서만 가능 (단일 그래비티 중심)
   - 읽기: 모든 리전에서 가능 (중력 분산)

   예: Amazon Aurora Global Database
   - Primary: us-east-1 (쓰기 중심 그래비티)
   - Read Replica: eu-west-1, ap-northeast-1 (읽기 분산)

2. 샤딩과 그래비티 분산
   - 지역별 샤드: 사용자 지역 데이터를 해당 리전에 저장
   - 문제: 교차 지역 쿼리 시 높은 지연

3. 일관성 vs 그래비티
   - Strong Consistency: 모든 쓰기를 단일 리전으로 모음 → 강한 그래비티
   - Eventual Consistency: 쓰기 분산 가능 → 그래비티 약화, 충돌 해결 복잡

4. 데이터 지역성(D locality) 최적화
   CREATE TABLE orders (
     id BIGINT,
     region_code VARCHAR(2),  -- 파티션 키
     data JSONB
   ) PARTITION BY LIST (region_code);

   -- region_code = 'KR'인 데이터는 ap-northeast-2에 저장
   -- 그래비티에 의해 한국 사용자 서비스도 동일 리전 배치
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 시나리오

#### 시나리오 1: 멀티 클라우드 전환 검토
```
현황:
- AWS S3 Data Lake: 500TB
- 월 Egress: 50TB (다른 클라우드 서비스 연동)
- 월 S3 비용: $11,500
- 월 Egress 비용: $4,500

기술사 분석:
1. 그래비티 점수 산정:
   - Size Score: 500TB / 10 = 50
   - Frequency Score: 50TB 월 이동 = High (100)
   - Total: 50 × 0.3 + 100 × 0.3 + 50 × 0.4 = 85점 (CRITICAL)

2. 비용 분석:
   - GCP로 이동 시 Egress: 500TB × $0.12 = $60,000 (일회성)
   - GCP 스토리지: 500TB × $0.023/GB = $11,500 (월)
   - 절감 없음, 이동 비용만 발생

3. 권장 전략:
   - "데이터는 AWS에 유지, 신규 서비스만 GCP에 배치"
   - AWS-GCP 간 Dedicated Interconnect 구축 (월 $2,000)
   - Egress 대비 Interconnect 비용 효율적

4. 결론:
   - 데이터 그래비티가 강해 멀티 클라우드보다 하이브리드 연결이 합리적
```

#### 시나리오 2: 글로벌 서비스 데이터 배치
```
요구사항:
- 전 세계 사용자 1억 명
- 사용자 데이터 총 200TB
- 응답 지연 < 100ms 목표
- 규제: EU 데이터 EU 내 저장 (GDPR)

기술사 판단:
1. 그래비티 기반 리전 분할:
   ┌─────────────────────────────────────────┐
   │ 리전별 그래비티 설계                      │
   ├─────────────────────────────────────────┤
   │ us-east-1:   60TB (남북미 사용자)        │
   │ eu-west-1:   50TB (유럽 사용자, GDPR)    │
   │ ap-northeast-1: 50TB (일본/한국)         │
   │ ap-southeast-1: 40TB (동남아/호주)       │
   └─────────────────────────────────────────┘

2. 데이터 파티셔닝 전략:
   - 사용자 ID 해시 기반 라우팅
   - 각 리전 독립형 데이터 마이크로서비스
   - 교차 리전 요청은 API Gateway에서 라우팅

3. 아키텍처:
   [Global DNS] ──┬──▶ [us-east-1 API] ──▶ [us-east-1 DB]
                  ├──▶ [eu-west-1 API] ──▶ [eu-west-1 DB]
                  ├──▶ [ap-northeast-1 API] ──▶ [ap-northeast-1 DB]
                  └──▶ [ap-southeast-1 API] ──▶ [ap-southeast-1 DB]

4. 그래비티 분산 효과:
   - 각 리전 50TB 미만으로 그래비티 약화
   - 리전 간 복제 비용 최소화
   - 지역별 규제 준수 용이
```

### 도입 시 고려사항 체크리스트

#### 기술적 고려사항
- [ ] **데이터 프로파일링**: 현재 데이터 양, 성장률, 접근 패턴 분석
- [ ] **이동 비용 시뮬레이션**: Egress, 스토리지 중복, 전송 시간 계산
- [ ] **의존성 매핑**: 데이터와 연관된 서비스, API, 파이프라인 식별
- [ ] **지연 요구사항**: 애플리케이션별 허용 지연 시간 정의
- [ ] **규제 요구사항**: 데이터 거주 지역, 국외 이전 제한 확인

#### 운영/비즈니스적 고려사항
- [ ] **TCO 분석**: 3-5년 총소유비용 비교
- [ ] **벤더 협상력**: 대량 데이터 보유 시 Egress 할인 협상 가능성
- [ ] **출구 전략**: 데이터 추출, 포맷 변환 도구 확보
- [ ] **조직 역량**: 대용량 데이터 운영 인력 확보

### 주의사항 및 안티패턴

#### 안티패턴 1: 데이터 그래비티 무시한 멀티 클라우드 강제
```
잘못된 접근:
- "벤더 락인 피하자" → 1PB 데이터를 AWS → Azure 이동
- 이동 비용 $90,000+, 서비스 중단 2주

올바른 접근:
- 신규 데이터는 Azure, 레거시는 AWS 유지
- 시간이 지나며 자연스럽게 그래비티 이동
- 또는 "Encapsulation Layer"로 추상화
```

#### 안티패턴 2: 단일 데이터 레이크 과도 집중
```
잘못된 접근:
- 모든 데이터를 단일 S3 버킷에 2PB 집중
- 모든 팀이 이 데이터에 의존 → SPOF, 비용 폭증

올바른 접근:
- 데이터 메시: 도메인별 데이터 제품으로 분산
- 각 도메인이 자체 데이터 그래비티 중심 보유
- 느슨한 결합으로 전체 시스템 유연성 확보
```

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 구분 | 그래비티 무시 | 그래비티 고려 | 개선효과 |
|-----------|-------------|-------------|---------|
| 데이터 이동 비용 | $100,000/년 | $20,000/년 | -80% |
| 평균 응답 지연 | 150ms | 30ms | -80% |
| 마이그레이션 프로젝트 실패율 | 40% | 10% | -75% |
| 아키텍처 재설계 횟수 | 3회 | 1회 | -67% |
| 벤더 락인 위험도 | 높음 | 관리 가능 | 위험 완화 |

### 미래 전망 및 진화 방향

#### 1. 데이터 그래비티 시각화 도구
- 실시간 그래비티 맵: 데이터-앱 간 인력 관계 시각화
- 비용 시뮬레이터: "What-if" 시나리오 분석
- 예상: 2025년 주요 CSP 제공

#### 2. 그래비티 기반 자동 배치
- AI가 데이터 위치를 분석하여 최적 앱 배치 추천
- Kubernetes 스케줄러에 그래비티 인식 기능 탑재
- 예상: K8s 1.30+ 버전

#### 3. 데이터 이동 자유화 규제
- EU Data Act: 클라우드 간 데이터 이동 권리 보장
- Egress Fee 제한 법제화 논의
- 예상: 2026년 EU 시행

### 참고 표준/가이드
- **NIST SP 800-145**: 클라우드 컴퓨팅 정의 (데이터 이동성)
- **ISO/IEC 19944**: 클라우드 컴퓨팅 데이터 및 그 흐름
- **GDPR Article 20**: 데이터 이동권 (Right to Portability)
- **EU Data Act**: 데이터 공유 및 이동 규정

---

## 관련 개념 맵 (Knowledge Graph)

1. [벤더 락인 (Vendor Lock-in)](./vendor_lock_in.md)
   - 관계: 데이터 그래비티가 벤더 락인의 주요 원인으로 작용

2. [멀티 클라우드 (Multi-Cloud)](./multi_cloud.md)
   - 관계: 데이터 그래비티 관리가 멀티 클라우드 성공의 핵심

3. [데이터 레이크 (Data Lake)](./data_lake.md)
   - 관계: 대용량 데이터 레이크가 가장 강한 그래비티 중심

4. [엣지 컴퓨팅 (Edge Computing)](./edge_computing.md)
   - 관계: 엣지에서 처리하면 데이터 그래비티 문제 완화

5. [데이터 메시 (Data Mesh)](./data_mesh.md)
   - 관계: 분산 데이터 소유로 단일 그래비티 중심 문제 해결

6. [하이브리드 클라우드 (Hybrid Cloud)](./hybrid_cloud.md)
   - 관계: 온프레미스 데이터 그래비티와 클라우드 균형 설계

---

## 어린이를 위한 3줄 비유 설명

**비유: 학교 급식실**

데이터 그래비티는 급식실(데이터)에 모이는 친구들(앱)과 같아요. 급식실에 맛있는 밥이 많이 있으면(데이터 많음), 모든 친구들이 급식실 쪽으로 몰려가죠. 급식실을 다른 학교로 옮기려면 밥을 다 옮겨야 해서 엄청 힘들어요!

**원리:**
컴퓨터에서도 데이터가 모인 곳이 '급식실'이에요. 많은 프로그램들이 데이터를 사용하려고 그 곳으로 모여들어요. 데이터를 다른 클라우드로 옮기는 건 밥을 다 옮기는 것처럼 비싸고 오래 걸려요.

**효과:**
회사들은 이 원리를 알고 처음부터 데이터를 어디에 둘지 신중하게 정해요. 한번 자리를 잡으면 옮기기 힘드니까요. 마치 집을 한번 지으면 이사 가기 힘든 것과 같아요!
