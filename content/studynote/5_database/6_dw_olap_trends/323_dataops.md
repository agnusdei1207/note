+++
title = "323. 데이터옵스 (DataOps)"
weight = 4323
+++

> **💡 핵심 인사이트**
> 데이터옵스(DataOps)는 **"소프트웨어 엔지니어링의 데브옵스(DevOps) 철학과CI/CD 파이프라인을 데이터 엔지니어링에 적용하여, 데이터 파이프라인의 개발·테스트·배포·모니터링 전 과정을 자동화하고 품질을 지속적으로 개선하는 개발 문화 및 방법론"**입니다.
> 기존 데이터 팀이直面하던 " ETL 잡이 실패했지만原查找找不到", "배포 전 테스트環境が再現できない", "하루 걸리던 파이프라인을 修改하면 影响範囲가多大인지 모른다" 등의 문제를, 데브옵스가 软件開発의 문서를解決했던 것처럼 **"데이터 파이프라인도 代码처럼 다루자"**는 패러다임입니다.

---

## Ⅰ. DevOps에서 DataOps로: 배경과 동인

```
[DevOps → DataOps 진화 과정]

  DevOps의 성과:
  - CI/CD: 코드 변경 → 자동 빌드 → 자동 테스트 → 자동 배포
  - Infrastructure as Code: 환경 설정도 코드로 관리
  - 모니터링&피드백: Production 문제의 빠른 발견과 해결

  데이터 엔지니어링의 현실 (DevOps 도입 전):
  - ETL 잡은 "手作業"で 밤새 실행
  - 스키마 변경 시 영향 분석은 "발견해 봐야 안다"
  - 테스트 환경은 本番と完全不同
  - 파이프라인 실패 원인은 "아무도 모른다"

  DataOps의 취지:
  - 데이터 파이프라인에도 CI/CD를 적용하자
  - "데이터를 代码처럼" 버전 관리, 테스트, 자동화하자
```

---

## Ⅱ. DataOps의 핵심 구성 요소

```
[DataOps 아키텍처]

  ┌─────────────────────────────────────────────────────┐
  │               DataOps Platform                        │
  │  ┌──────────────────────────────────────────────┐  │
  │  │              CI/CD Pipeline                     │  │
  │  │  ┌────────┐  ┌────────┐  ┌────────┐        │  │
  │  │  │ Source │→ │ Build  │→ │ Test   │→ Deploy│  │
  │  │  │ Control│  │        │  │        │        │  │
  │  │  └────────┘  └────────┘  └────────┘        │  │
  │  └──────────────────────────────────────────────┘  │
  │                    │                                 │
  │  ┌─────────────────┼───────────────────────────┐  │
  │  │                  │                           │  │
  │  ▼                  ▼                           ▼  │
  │ ┌──────────┐  ┌──────────┐  ┌──────────┐      │
  │ │ Version   │  │ Data     │  │ Auto-   │      │
  │ │ Control   │  │ Quality   │  │ masking │      │
  │ │ (Git)     │  │ Monitoring│  │         │      │
  │ └──────────┘  └──────────┘  └──────────┘      │
  └─────────────────────────────────────────────────────┘
                      │
                      ▼
  ┌─────────────────────────────────────────────────────┐
  │                  Data Infrastructure                  │
  │   Airflow │ dbt │ Spark │ Kafka │ Snowflake │ ...  │
  └─────────────────────────────────────────────────────┘
```

### 1. 데이터 파이프라인의 버전 관리 (Git for Data)

```yaml
# dbt (data build tool) 예시: SQL 파일도 Git으로 관리
# models/marts/fct_orders.yml
version: 2

models:
  - name: fct_orders
    description: 주문 요약 테이블
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
    config:
      materialized: incremental  # 증분 업데이트
      unique_key: order_id
```

### 2. 데이터 품질 테스트 자동화

```sql
-- dbt 테스트 예시: 파이프라인 배포 전 자동 검증
-- models/marts/schema.yml

models:
  - name: fct_orders
    columns:
      - name: order_amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min: 0
              max: 1000000000  -- 합리적 금액 범위
      - name: order_date
        tests:
          - not_null
          - dbt_utils.recency:
              datepart: hour
              interval: 2      -- 2시간 이내 데이터여야 함
```

### 3. 변경 전衙前 테스트 (Pre-merge/Pre-deploy Testing)

```bash
# Pull Request 시 자동 실행 파이프라인
# .github/workflows/data_quality.yml

name: Data Quality Tests

on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run dbt tests
        run: |
          dbt deps
          dbt seed  # 테스트용 샘플 데이터 적재
          dbt run --models fct_orders  # 파이프라인 실행
          dbt test --models fct_orders  # 스키마/데이터 품질 테스트

      - name: Data diff check
        run: |
          dbt shadow run --select +fct_orders  # 변경 영향 분석
          # 이전 버전 vs 새 버전 결과 비교
```

---

## III. DataOps의 주요 도구 생태계

```
[DataOps 도구 체인]

  ┌──────────────────────────────────────────────────────┐
  │                 DataOps 툴 체인                         │
  │                                                        │
  │  [Orchestration]          [Transformation]            │
  │  ┌────────────┐          ┌────────────┐             │
  │  │ Apache     │          │ dbt        │             │
  │  │ Airflow    │          │ (SQL-based)│             │
  │  │ Prefect    │          │ Dataform   │             │
  │  │ Dagster    │          │ Spark SQL  │             │
  │  └────────────┘          └────────────┘             │
  │                                                        │
  │  [Data Quality]         [Version Control]            │
  │  ┌────────────┐          ┌────────────┐             │
  │  │ Great      │          │ Git        │             │
  │  │ Expectations│          │ (dbt + Git)│             │
  │  │ dbt tests  │          │ LakeFS     │             │
  │  │ Soda.io    │          │ DVC        │             │
  │  └────────────┘          └────────────┘             │
  │                                                        │
  │  [Testing]              [Monitoring]                │
  │  ┌────────────┐          ┌────────────┐             │
  │  │ Monte Carlo │          │ Databand  │             │
  │  │ (AI-based) │          │ Bigeye    │             │
  │  │ Gable      │          │ Metaflow   │             │
  │  └────────────┘          └────────────┘             │
  └──────────────────────────────────────────────────────┘
```

---

## IV. DataOps 도입의効果と課題

**도입 효과:**

```
[도입 전 vs 도입 후]

  도입 전:
  ┌─────────────────────────────────────────────┐
  │ - ETL 배포: 手動 → 주 1회 정도만 가능          │
  │ - 파이프라인 실패: 아침에 들어가서才发现          │
  │ - 영향 분석: "일단 까보니까 알았음"              │
  │ - 테스트: 本番 데이터로 수동 테스트              │
  │ - 총 소요 시간: 변경 1회 ≈ 2주                  │
  └─────────────────────────────────────────────┘

  도입 후:
  ┌─────────────────────────────────────────────┐
  │ - ETL 배포: 자동 → 일 수십 회 배포 가능          │
  │ - 파이프라인 실패:部署 전 自动检测 → 실패 최소화   │
  │ - 영향 분석: dbt shadow run으로事前に予測        │
  │ - 테스트: 샘플 데이터로 자동 테스트              │
  │ - 총 소요 시간: 변경 1회 ≈ 1~2일               │
  └─────────────────────────────────────────────┘
```

**도입 장벽:**
1. **문화 변화**: "데이터는 소프트웨어와 다르다"는 인식 전환 필요
2. **기술 학습 곡선**: Git, CI/CD, 데이터 품질 테스트 등 새로운 스킬 필요
3. **테스트 데이터 확보**:-production 데이터를 어떻게テスト環境에 提供할 것인가
4. **도구 산발성**: 여러 도구를 연결하는Integration이 복잡

---

## Ⅴ. DataOps의 미래 트렌드と 📢 비유

**AI 기반 DataOps:**
- **자동 이상 탐지**: Monte Carlo, Gable 등이 ML로 데이터 품질 이상 자동 탐지
- **자동 근본 원인 분석**: 파이프라인 실패 시 AI가 "원인은 XX 테이블의 결측치 증가"라고 설명
- **자동 최적화**: "이 파이프라인은 매시간 실행보다 6시간마다 실행 시 비용 40% 절감"이라고提案

**IaC (Infrastructure as Code) for Data:**
- Terraform으로 Snowflake, BigQuery 등 클라우드 DW 리소스 관리
- 데이터 파이프라인을代码로 管理 → Git history, code review, rollback 가능

> 📢 **섹션 요약 비유:** DataOps는 **"요리 연구소에서 레시피를 개발하고 검증하는 과정"**과 같습니다. 기존에는 "셰프가 경험으로 만들어낸 요리법을 文書化하지 않고, 그냥 그때그때 만들면" 새로운 레시피 도입 시 "맛이 달라졌다"고 아무도 原查找找不到でした. DataOps는 **"모든 레시피(파이라인)를配方(코드)로 기록하고,小さな 규모で試作(テスト)하고,食品安全검사를 거치고,批准되면大型厨房(-production)으로移設하는"** 과정입니다. 핵심은 **"手探りの暗黙知을 明示的知識로 변환하고,その知識を自動テスト하는 것"**입니다. 데이터도 software처럼 "문서화되고, 테스트되고, автоматически 배포되는" 것이 DataOps의 핵심입니다.
