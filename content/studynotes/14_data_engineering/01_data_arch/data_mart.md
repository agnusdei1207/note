+++
title = "데이터 마트 (Data Mart)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 데이터 마트 (Data Mart)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 마트(Data Mart)는 특정 부서나 업무 기능(영업, 재무, 마케팅 등)을 위한 분석 전용 데이터 부분집합으로, 데이터 웨어하우스의 하위 집합이거나 독립적으로 구축됩니다.
> 2. **가치**: 부서별 맞춤 분석 모델(Star Schema, OLAP Cube)을 제공하여 비전문가도 쉽게 셀프 서비스 분석이 가능하며, 쿼리 성능을 최적화합니다.
> 3. **융합**: Kimball 아키텍처의 핵심 구성요소로, Conformed Dimension(공유 차원)을 통해 전사적 데이터 일관성을 유지하며, 최근에는 데이터 레이크하우스의 Gold Layer로 진화합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**데이터 마트(Data Mart)**는 기업 내 특정 사용자 그룹(영업팀, 재무팀, 마케팅팀 등)의 분석 요구사항을 충족시키기 위해 설계된 주제 중심의 데이터 저장소입니다. 전사적 데이터 웨어하우스(Enterprise DW)의 부분집합으로, 특정 비즈니스 영역에 최적화된 스키마와 집계 데이터를 포함합니다.

**데이터 마트의 핵심 특성**:
- **업무 특화 (Business-Specific)**: 특정 부서/기능에 맞춤화된 데이터 구조
- **경량화 (Lightweight)**: 전사 DW 대비 작은 규모, 빠른 쿼리 응답
- **사용자 친화적**: 비즈니스 사용자가 이해하기 쉬운 용어와 구조
- **높은 성능**: 사전 집계, 최적화된 인덱스로 빠른 응답

**데이터 마트 유형**:
| 유형 | 정의 | 장점 | 단점 |
|:---|:---|:---|:---|
| **종속형 (Dependent)** | EDW에서 파생된 마트 | 데이터 일관성 보장 | EDW 구축 선행 필요 |
| **독립형 (Independent)** | 운영 DB에서 직접 구축 | 빠른 구축, 낮은 비용 | 데이터 사일로 위험 |
| **하이브리드 (Hybrid)** | EDW + 외부 데이터 결합 | 유연성, 확장성 | 복잡한 통합 관리 |

#### 2. 비유를 통한 이해
데이터 마트를 **'부서별 전용 도서관'**이나 **'편의점'**에 비유할 수 있습니다.
- **데이터 웨어하우스**: 도서관 중앙 도서실입니다. 모든 종류의 책이 있지만, 원하는 걸 찾으려면 시간이 걸립니다.
- **데이터 마트**: 각 부서에 있는 '작은 자료실'입니다. 영업팀 자료실에는 영업 관련 책만, 재무팀 자료실에는 재무 관련 책만 있습니다. 필요한 걸 빨리 찾을 수 있습니다.

**Kimball의 비유**: "데이터 마트는 데이터 웨어하우스라는 케이크의 한 조각이다"

#### 3. 등장 배경 및 발전 과정
1. **1990s: DW 구축의 어려움**: 전사적 EDW 구축에 수년이 소요되고 비용이 막대하여, 실무 부서에서 대안으로 데이터 마트를 먼저 구축하려는 요구가 증가했습니다.
2. **Kimball 아키텍처의 부상**: Ralph Kimball이 "The Data Warehouse Toolkit"에서 데이터 마트를 먼저 구축하고 통합하는 Bottom-up 방식을 제안했습니다. 핵심은 **Conformed Dimension(공유 차원)**을 통해 마트 간 일관성을 유지하는 것입니다.
3. **2000s: OLAP 큐브와 데이터 마트**: Microsoft Analysis Services, Oracle OLAP 등이 데이터 마트 위에 다차원 큐브를 구축하여 Excel에서 피벗 테이블 분석을 가능하게 했습니다.
4. **2010s~현재**: 클라우드 DW(Snowflake, BigQuery)에서 스키마와 뷰를 통한 가상 데이터 마트(Virtual Data Mart) 구축이 일반화되었습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 데이터 마트 구성 요소 (표)

| 구성 요소 | 역할 | 내부 구조 | 예시 |
|:---|:---|:---|:---|
| **팩트 테이블 (Fact Table)** | 비즈니스 이벤트 측정값 저장 | FK + Measures | sales_amount, quantity |
| **차원 테이블 (Dimension Table)** | 분석 기준 속성 저장 | SK + Attributes | 고객, 상품, 시간 |
| **집계 테이블 (Aggregate Table)** | 사전 계산된 요약 | Group By 결과 | 월별_매출_요약 |
| **인덱스 (Index)** | 쿼리 성능 최적화 | B-Tree, Bitmap | 조인 컬럼 인덱스 |
| **뷰 (View)** | 가상 테이블, 보안/추상화 | SQL 정의 | v_sales_dashboard |

#### 2. Kimball Bus Architecture (ASCII 다이어그램)

```text
<<< Kimball Data Warehouse Bus Architecture >>>

                    +---------------------------------+
                    |    Conformed Dimensions          |
                    |    (전사 공통 차원 정의)           |
                    +---------------------------------+
                              |   |   |   |
           +------------------+---+---+---+------------------+
           |                  |   |   |   |                  |
           v                  v   v   v   v                  v
    +-------------+    +-------------+    +-------------+    +-------------+
    | Sales Mart  |    | Finance Mart|    | HR Mart     |    | Marketing   |
    |             |    |             |    |             |    | Mart        |
    | Conformed:  |    | Conformed:  |    | Conformed:  |    | Conformed:  |
    | - Date      |    | - Date      |    | - Date      |    | - Date      |
    | - Product   |    | - Account   |    | - Employee  |    | - Customer  |
    | - Customer  |    | - Dept      |    | - Dept      |    | - Product   |
    | - Store     |    |             |    |             |    | - Campaign  |
    +-------------+    +-------------+    +-------------+    +-------------+

[Conformed Dimension Matrix (Bus Matrix)]

                    | Date | Product | Customer | Store | Employee | Account |
    ---------------+------+---------+----------+-------+----------+---------+
    Sales Mart     |  X   |    X    |    X     |   X   |          |         |
    Finance Mart   |  X   |         |          |       |    X     |    X    |
    HR Mart        |  X   |         |          |       |    X     |         |
    Marketing Mart |  X   |    X    |    X     |       |          |         |

    X = 해당 마트에서 사용하는 공유 차원

[핵심 원칙]
1. 동일한 차원은 모든 마트에서 동일한 정의와 값을 가져야 함
2. 새로운 마트 구축 시 기존 Conformed Dimension 재사용
3. 이를 통해 전사적 Cross-Mart 분석 가능
```

#### 3. 심층 동작 원리: Star Schema 설계

**영업 데이터 마트 스타 스키마**:
```sql
-- ============================================
-- Sales Data Mart: Star Schema Design
-- ============================================

-- 1. 팩트 테이블 (Fact Table)
CREATE TABLE fact_sales (
    -- 서로게이트 키 (Surrogate Key)
    sales_key        BIGINT IDENTITY(1,1) PRIMARY KEY,

    -- 차원 외래키 (Dimension Foreign Keys)
    date_key         INT NOT NULL,
    product_key      INT NOT NULL,
    customer_key     INT NOT NULL,
    salesrep_key     INT NOT NULL,
    store_key        INT NOT NULL,
    promotion_key    INT NOT NULL,

    -- 측정값 (Measures) - 가산적(Additive)
    sales_quantity   INT NOT NULL,
    sales_amount     DECIMAL(15,2) NOT NULL,
    cost_amount      DECIMAL(15,2) NOT NULL,
    discount_amount  DECIMAL(15,2) NOT NULL,
    gross_profit     DECIMAL(15,2) GENERATED ALWAYS AS
                     (sales_amount - cost_amount) STORED,

    -- 측정값 - 반가산적(Semi-additive)
    -- 예: 재고 수량은 시간에 따라 합산 불가

    -- 메타데이터
    etl_timestamp    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 외래키 제약조건
    CONSTRAINT fk_fact_date FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key),
    CONSTRAINT fk_fact_product FOREIGN KEY (product_key)
        REFERENCES dim_product(product_key),
    CONSTRAINT fk_fact_customer FOREIGN KEY (customer_key)
        REFERENCES dim_customer(customer_key)
);

-- 2. 차원 테이블 (Dimension Tables)
CREATE TABLE dim_date (
    date_key         INT PRIMARY KEY,
    full_date        DATE UNIQUE NOT NULL,
    day_of_week      INT,
    day_name         VARCHAR(10),
    day_of_month     INT,
    week_of_year     INT,
    week_of_month    INT,
    month_number     INT,
    month_name       VARCHAR(10),
    month_end_date   DATE,
    quarter          INT,
    quarter_name     VARCHAR(10),
    year             INT,
    year_month       INT,        -- 202403
    is_weekend       BOOLEAN,
    is_holiday       BOOLEAN,
    holiday_name     VARCHAR(50)
);

CREATE TABLE dim_product (
    product_key      INT PRIMARY KEY,
    product_id       VARCHAR(20) UNIQUE NOT NULL,
    product_name     VARCHAR(100),
    brand            VARCHAR(50),
    category         VARCHAR(50),
    subcategory      VARCHAR(50),
    department       VARCHAR(50),
    supplier         VARCHAR(100),
    unit_cost        DECIMAL(10,2),
    unit_price       DECIMAL(10,2),
    status           VARCHAR(20),
    effective_date   DATE,
    expiration_date  DATE,
    is_current       BOOLEAN
);

-- 3. 집계 테이블 (Aggregate Table) - 성능 최적화
CREATE TABLE agg_monthly_sales (
    year_month       INT,
    product_key      INT,
    store_key        INT,
    total_sales      DECIMAL(15,2),
    total_quantity   INT,
    transaction_count INT,
    avg_transaction   DECIMAL(10,2),
    PRIMARY KEY (year_month, product_key, store_key)
);

-- 4. 분석 쿼리 예시
-- 월별 카테고리별 매출 추이
SELECT
    d.year,
    d.month_name,
    p.category,
    SUM(f.sales_amount) as total_sales,
    SUM(f.sales_quantity) as total_qty,
    COUNT(DISTINCT f.customer_key) as unique_customers
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
WHERE d.year = 2024
GROUP BY d.year, d.month_name, d.month_number, p.category
ORDER BY d.month_number, total_sales DESC;
```

#### 4. Snowflake Schema (스노우플레이크 스키마)

```text
<<< Snowflake Schema: 정규화된 차원 테이블 >>>

                    +-------------+
                    | fact_sales  |
                    +------+------+
                           |
        +------------------+------------------+
        |                  |                  |
        v                  v                  v
+-------------+    +-------------+    +-------------+
| dim_product |    | dim_customer|    | dim_store   |
+------+------+    +------+------+    +------+------+
       |                  |                  |
       v                  v                  v
+-------------+    +-------------+    +-------------+
| dim_category|    | dim_city    |    | dim_region  |
+-------------+    +------+------+    +-------------+
                        |
                        v
                  +-------------+
                  | dim_state   |
                  +-------------+

[Star Schema vs Snowflake Schema 비교]
- Star Schema: 차원 테이블 비정규화 (조인 적음, 저장 공간 많음)
- Snowflake Schema: 차원 테이블 정규화 (조인 많음, 저장 공간 적음)
- 실무: 대부분 Star Schema 선호 (조인 비용 > 저장 비용)
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 데이터 마트 구축 방식 비교표

| 비교 항목 | 종속형 마트 (Dependent) | 독립형 마트 (Independent) | 가상 마트 (Virtual) |
|:---|:---|:---|:---|
| **데이터 원천** | Enterprise DW | 운영 DB 직접 | DW View/Schema |
| **구축 속도** | 느림 (EDW 선행) | 빠름 | 즉시 |
| **데이터 일관성** | 높음 | 낮음 (사일로 위험) | 높음 |
| **유지보수** | 중앙 집중 | 분산 | 중앙 집중 |
| **비용** | 높음 | 낮음 | 중간 |
| **적합한 상황** | 대기업, 규제 산업 | 중소기업, 긴급 프로젝트 | 클라우드 DW |

#### 2. 과목 융합 관점 분석

**데이터베이스 관점 - 쿼리 최적화**:
- **Star Join Optimization**: 팩트 테이블 중심 조인 순서 최적화
- **Bitmap Join Index**: 차원 속성으로 팩트 로우 필터링
- **Materialized View**: 자주 사용되는 집계 쿼리 결과 캐싱

**비즈니스 인텔리전스 관점**:
- **Self-Service BI**: 비즈니스 사용자가 IT 의존 없이 분석 가능
- **Semantic Layer**: 비즈니스 용어와 DB 컬럼 매핑

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 마케팅 데이터 마트 구축**
- **요구사항**: 캠페인 ROI 분석, 고객 세그먼트 분석, 채널별 성과 측정
- **설계 결정**:
  - 팩트 테이블: fact_campaign_response, fact_web_analytics
  - 차원 테이블: dim_campaign, dim_channel, dim_customer_segment
  - 집계: 일별 채널별 전환율, 캠페인별 ROI

**시나리오 2: 재무 데이터 마트 구축**
- **요구사항**: 월결산, 예실 대비 분석, 부서별 비용 관리
- **설계 결정**:
  - 팩트 테이블: fact_gl_transactions (반가산적)
  - 차원 테이블: dim_account, dim_cost_center, dim_period
  - 스냅샷: 월말 잔액 스냅샷 테이블

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **Conformed Dimension 정의**: 전사 공통 차원 식별 및 정의
- [ ] **Slowly Changing Dimension (SCD) 전략**: Type 1/2/3 결정
- [ ] **집계 전략**: 어떤 수준의 사전 집계가 필요한가?
- [ ] **보안**: 부서별 데이터 접근 권한 설계

#### 3. 안티패턴 (Anti-patterns)

- **독립형 마트 남발**: 부서별로 다른 정의 사용 → 전사 분석 불가능
- **과도한 집계**: 모든 조합의 집계 테이블 생성 → 저장 공간 폭증
- **팩트 테이블 비정규화**: 팩트에 차원 속성 직접 포함 → 일관성 깨짐

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 구분 | 전사 DW 직접 쿼리 | 데이터 마트 활용 | 개선 효과 |
|:---|:---|:---|:---|
| **쿼리 응답 시간** | 분 단위 | 초 단위 | 10~100배 향상 |
| **사용자 편의성** | 복잡한 SQL | 직관적 구조 | Self-service 가능 |
| **IT 의존도** | 높음 | 낮음 | 업무 효율화 |
| **부서 만족도** | 낮음 | 높음 | ROI 향상 |

#### 2. 미래 전망
데이터 마트는 **데이터 레이크하우스의 Gold Layer**로 진화하고 있습니다. dbt(Data Build Tool)와 같은 Transformation 도구를 통해 SQL로 데이터 마트를 정의하고 버전 관리하는 **DataOps** 방식이 표준화되고 있습니다. 또한 Semantic Layer(Looker, Cube.js)가 논리적 데이터 마트를 제공하여, 물리적 복제 없이 가상 마트를 구현하는 추세입니다.

#### 3. 참고 표준
- **Kimball, R. (2013)**: The Data Warehouse Toolkit, 3rd Edition
- **Kimball Group**: Design Tips for Data Marts

---

### 관련 개념 맵 (Knowledge Graph)
- **[데이터 웨어하우스 (Data Warehouse)](@/studynotes/14_data_engineering/01_data_arch/data_warehouse.md)**: 전사적 통합 데이터 저장소
- **[OLAP](@/studynotes/14_data_engineering/01_data_arch/olap.md)**: 다차원 분석 처리
- **[Star Schema](@/studynotes/14_data_engineering/01_data_arch/star_schema.md)**: 팩트-차원 테이블 구조
- **[ETL vs ELT](@/studynotes/14_data_engineering/03_pipelines/etl_vs_elt.md)**: 데이터 변환 적재 방식
- **[데이터 레이크하우스 (Data Lakehouse)](@/studynotes/14_data_engineering/01_data_arch/data_lakehouse.md)**: 현대적 통합 플랫폼

---

### 어린이를 위한 3줄 비유 설명
1. **부서별 책장**: 데이터 마트는 학교 도서관에 있는 '과학 코너', '만화 코너' 같은 거예요. 각 코너에는 그 주제에 맞는 책만 모여 있어요.
2. **빨리 찾기**: 과학 과제를 하려면 과학 코너만 보면 돼요. 전체 도서관을 다 뒤질 필요가 없죠.
3. **공통된 기준**: 그런데 책 분류 기준은 도서관 전체가 똑같아요. 그래야 '과학 코너'와 '역사 코너'의 책이 섞이지 않거든요!
