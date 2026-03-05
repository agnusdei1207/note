+++
title = "데이터 거버넌스 (Data Governance)"
categories = ["studynotes-16_bigdata"]
+++

# 데이터 거버넌스 (Data Governance)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 거버넌스는 조직의 데이터 자산에 대한 **소유권, 책임, 품질, 보안, 컴플라이언스**를 관리하는 정책, 프로세스, 조직 구조의 총체적 체계입니다.
> 2. **가치**: 데이터의 신뢰성(Trust)과 가용성(Accessibility)을 보장하여 **규제 준수(GDPR, 개인정보보호법)**, **데이터 품질 향상**, **의사결정 신뢰도 제고**를 실현합니다.
> 3. **융합**: Data Catalog, Data Lineage, Data Quality, Master Data Management(MDM) 도구가 통합된 **데이터 거버넌스 플랫폼**으로 구현됩니다.

---

## Ⅰ. 개요 (Context & Background)

데이터 거버넌스는 "데이터를 자산으로 관리하는 것"입니다. 단순히 기술적 문제가 아니라 **조직, 프로세스, 기술**의 3요소가 결합된 경영 이슈입니다. GDPR, CCPA 등 데이터 규제가 강화되면서 거버넌스는 선택이 아닌 필수가 되었습니다.

**💡 비유: 도서관 관리 시스템**
데이터 거버넌스는 **잘 정돈된 도서관**과 같습니다. (1) 누가 어떤 책을 관리하는지 명확합니다(**역할/책임**). (2) 책이 올바른 곳에 있는지 정기적으로 확인합니다(**품질 관리**). (3) 누가 책을 빌렸는지 기록합니다(**감사/추적**). (4) 희귀 도서는 특별 관리합니다(**보안/분류**). (5) 새 책이 들어오면 분류 체계에 맞춰 등록합니다(**메타데이터 관리**).

**등장 배경 및 발전 과정:**
1. **기존 기술의 치명적 한계점**: 데이터가 사일로(Silo)별로 흩어져 있고, 누가 소유자인지 불분명하며, 품질이 낮아 신뢰할 수 없었습니다. 이로 인해 "잘못된 데이터로 잘못된 의사결정"이 반복되었습니다.
2. **혁신적 패러다임 변화**: **Data as an Asset** 관점에서 데이터를 관리하며, **Data Stewardship** 개념을 도입하여 명확한 책임 소재를 확립했습니다.
3. **비즈니스적 요구사항**: GDPR 위반 시 매출 4% 벌금, 개인정보 유출 시 평판 손상 등 **규제 및 리스크 관리**가 경영의 핵심 이슈가 되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 데이터 거버넌스 핵심 구성 요소

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|---|---|---|---|---|
| **Data Catalog** | 데이터 자산 검색 및 발견 | 메타데이터 수집, 인덱싱, 분류 | Alation, Collibra, DataHub | 도서관 목록 |
| **Data Lineage** | 데이터 이동 경로 추적 | SQL 파싱, DAG 구성, 영향 분석 | Apache Atlas, Marquez | 책의 출처 기록 |
| **Data Quality** | 데이터 품질 측정 및 관리 | 프로파일링, 규칙 검증, DQI 산출 | Great Expectations, Deequ | 도서 상태 점검 |
| **MDM** | 마스터 데이터 단일화 | 중복 제거, 황금 레코드 생성 | Informatica MDM, Riversand | 표준 도서 정보 |
| **Access Control** | 접근 권한 관리 | RBAC, ABAC, 마스킹, 암호화 | Ranger, Unity Catalog | 도서 대출 권한 |

### 정교한 구조 다이어그램 (ASCII Art)

```text
========================================================================================================
                              [ DATA GOVERNANCE FRAMEWORK ]
========================================================================================================

  [ PEOPLE & ORGANIZATION ]          [ PROCESS ]                [ TECHNOLOGY ]

  +------------------------+     +---------------------+     +------------------------+
  | Chief Data Officer     |     | Policies & Standards|     | Data Catalog           |
  | (CDO)                  |     | - Data Classification|     | - Metadata Management  |
  +------------------------+     | - Retention Policy  |     | - Search & Discovery   |
                                 | - Quality Standards |     +------------------------+
  +------------------------+     +---------------------+
  | Data Governance Council|            │                       +------------------------+
  | - Business Stewards    |            │                       | Data Lineage           |
  | - Technical Stewards   |            ▼                       | - Impact Analysis      |
  | - Legal/Compliance     |     +---------------------+     | - Root Cause Tracing   |
  +------------------------+     | Workflows           |     +------------------------+
                                 | - Data Onboarding   |
  +------------------------+     | - Change Management |     +------------------------+
  | Data Stewards          |     | - Issue Resolution  |     | Data Quality           |
  | - Domain Owners        |     +---------------------+     | - Profiling            |
  | - Quality Managers     |                                 | - Validation Rules     |
  +------------------------+                                 +------------------------+

                                                              +------------------------+
                                                              | Access & Security      |
                                                              | - RBAC/ABAC            |
                                                              | - Encryption           |
                                                              | - Audit Logging        |
                                                              +------------------------+

========================================================================================================
                              [ DATA QUALITY DIMENSIONS ]
========================================================================================================

  ┌─────────────────────────────────────────────────────────────────────────────────┐
  │                         DATA QUALITY FRAMEWORK (DAMA-DMBOK)                     │
  ├─────────────────┬─────────────────┬─────────────────┬─────────────────┬─────────┤
  │  Accuracy       │  Completeness   │  Consistency    │  Timeliness     │Validity │
  │  (정확성)       │  (완전성)       │  (일관성)       │  (적시성)       │(유효성) │
  │                 │                 │                 │                 │         │
  │  실제 값과      │  필수 필드      │  여러 시스템    │  데이터가       │  비즈니스│
  │  일치하는 정도  │  채워진 비율    │  간 일치 여부   │  최신인 정도    │  규칙 준수│
  ├─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────┤
  │  KPI:           │  KPI:           │  KPI:           │  KPI:           │  KPI:   │
  │  Error Rate %   │  Fill Rate %    │  Match Rate %   │  Freshness Hr   │  Pass % │
  └─────────────────┴─────────────────┴─────────────────┴─────────────────┴─────────┘

========================================================================================================
                              [ DATA LINEAGE & IMPACT ANALYSIS ]
========================================================================================================

  [ Source Systems ]       [ Data Lake ]            [ Data Warehouse ]      [ Analytics ]
  +---------------+       +----------------+       +------------------+    +-----------+
  | CRM System    |       | Bronze Layer   |       | Dim_Customer     |    | Dashboard |
  | (customers)   |------>| (raw_customers)|------>| (customer_key)   |--->| (Report)  |
  +---------------+       +----------------+       +------------------+    +-----------+
                                 │                         │
  +---------------+              │                         │
  | ERP System    |              ▼                         ▼
  | (orders)      |------>[ Silver Layer ]-------->[ Fact_Orders ]
  +---------------+       (cleaned_orders)           (order_key, customer_key)
                                                          │
                                                          ▼
                                                    [ ML Model ]
                                                    (customer_segment)

  Impact Analysis: If CRM System schema changes → Bronze → Silver → Dim_Customer → Dashboard
                                                          → Fact_Orders → ML Model

========================================================================================================
```

### 심층 동작 원리: Data Quality 관리 구현

**1. Great Expectations를 활용한 데이터 품질 관리**
```python
import great_expectations as ge
from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.core.expectation_configuration import ExpectationConfiguration

# Data Context 초기화
context = ge.get_context()

# 데이터 소스 연결
datasource_config = {
    "name": "customer_datasource",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "SparkDFExecutionEngine"
    },
    "data_connectors": {
        "runtime_data_connector": {
            "class_name": "RuntimeDataConnector",
            "batch_identifiers": ["batch_id"]
        }
    }
}
context.add_datasource(**datasource_config)

# Expectation Suite 정의 (품질 규칙)
expectation_suite_name = "customer_data_quality"
suite = context.add_expectation_suite(expectation_suite_name)

# 정확성(Accuracy): 이메일 형식 검증
suite.add_expectation(
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_match_regex",
        kwargs={
            "column": "email",
            "regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        }
    )
)

# 완전성(Completeness): 필수 필드 Null 체크
for col in ["customer_id", "name", "email"]:
    suite.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": col}
        )
    )

# 일관성(Consistency): 나이 범위 검증
suite.add_expectation(
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_be_between",
        kwargs={"column": "age", "min_value": 0, "max_value": 120}
    )
)

# 유일성(Uniqueness): 고객 ID 중복 체크
suite.add_expectation(
    ExpectationConfiguration(
        expectation_type="expect_column_values_to_be_unique",
        kwargs={"column": "customer_id"}
    )
)

# 체크포인트 실행
checkpoint_config = {
    "name": "customer_quality_checkpoint",
    "config_version": 1,
    "class_name": "SimpleCheckpoint",
    "run_name_template": "%Y%m%d-%H%M%S-customer-quality",
    "validations": [
        {
            "batch_request": {
                "datasource_name": "customer_datasource",
                "data_connector_name": "runtime_data_connector",
                "data_asset_name": "customer_data"
            },
            "expectation_suite_name": expectation_suite_name
        }
    ]
}
context.add_checkpoint(**checkpoint_config)

# 실행 및 결과 확인
results = context.run_checkpoint(
    checkpoint_name="customer_quality_checkpoint",
    run_name="daily_quality_check"
)

if results.success:
    print("Data Quality Check Passed ✓")
else:
    print("Data Quality Issues Detected ✗")
    # Slack/Email 알림 발송 로직
```

**2. Data Lineage 구현 (Apache Atlas)**
```python
# Apache Atlas REST API를 활용한 Lineage 등록
import requests
from requests.auth import HTTPBasicAuth

atlas_url = "http://atlas:21000/api/atlas/v2"
auth = HTTPBasicAuth("admin", "admin")

# 데이터 세트(Entity) 등록
customer_entity = {
    "entity": {
        "typeName": "hdfs_path",
        "attributes": {
            "name": "customer_data",
            "path": "/data/lake/bronze/customers",
            "owner": "data_team",
            "qualifiedName": "customer_data@lake"
        }
    }
}

response = requests.post(
    f"{atlas_url}/entity",
    json=customer_entity,
    auth=auth
)
customer_guid = response.json()["guidAssignments"][0]

# 프로세스(변환) 등록 - Lineage 연결
process_entity = {
    "entity": {
        "typeName": "spark_process",
        "attributes": {
            "name": "customer_etl",
            "inputs": [{"guid": source_guid}],  # 원본 데이터 GUID
            "outputs": [{"guid": customer_guid}],  # 결과 데이터 GUID
            "queryText": "SELECT customer_id, name FROM raw_customers"
        }
    }
}

requests.post(f"{atlas_url}/entity", json=process_entity, auth=auth)

# Lineage 조회
lineage_response = requests.get(
    f"{atlas_url}/lineage/{customer_guid}",
    auth=auth
)
lineage_graph = lineage_response.json()
```

**3. Data Classification & Tagging**
```python
# 민감 데이터 분류 및 태깅
sensitive_columns = {
    "ssn": "PII_SENSITIVE",           # 주민등록번호
    "email": "PII_DIRECT",            # 직접 식별자
    "phone": "PII_DIRECT",            # 직접 식별자
    "ip_address": "PII_INDIRECT",     # 간접 식별자
    "credit_card": "PCI_DSS",         # 결제 정보
    "medical_record": "PHI"           # 의료 정보
}

def classify_and_tag_data(df, column_classifications):
    """데이터 분류 및 태깅 적용"""
    for column, classification in column_classifications.items():
        if column in df.columns:
            # Catalog에 태그 등록
            register_tag(column, classification)

            # 분류별 보안 조치 적용
            if classification.startswith("PII"):
                # 마스킹 적용
                df = apply_masking(df, column, classification)
            elif classification == "PCI_DSS":
                # 암호화 적용
                df = apply_encryption(df, column)

    return df

def apply_masking(df, column, classification):
    """데이터 마스킹 적용"""
    if classification == "PII_SENSITIVE":
        # 완전 마스킹
        df[column] = "****"
    elif classification == "PII_DIRECT":
        # 부분 마스킹 (이메일: j***@example.com)
        df[column] = df[column].apply(
            lambda x: x[0] + "***" + x[x.index("@"):]
        )
    return df
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Data Governance 도구

| 비교 지표 | Alation | Collibra | DataHub | Apache Atlas |
|---|---|---|---|---|
| **유형** | 상용 | 상용 | 오픈소스(LI) | 오픈소스(Apache) |
| **Catalog** | 강함 | 강함 | 강함 | 중간 |
| **Lineage** | 중간 | 강함 | 강함 | 강함 |
| **Quality** | 통합 | 통합 | 통합 | 별도 |
| **협업** | 강함 | 강함 | 중간 | 약함 |
| **Cloud** | SaaS | SaaS | On-prem/Cloud | On-prem |

### 과목 융합 관점 분석

- **[보안 + 거버넌스]**: 데이터 거버넌스는 **RBAC(Role-Based Access Control)**, **ABAC(Attribute-Based Access Control)**, **Data Masking**, **Tokenization** 등 보안 기술과 밀접하게 연결됩니다.

- **[법규 + 거버넌스]**: GDPR, CCPA, 개인정보보호법 등 **법적 요구사항**을 거버넌스 정책으로 변환합니다. DSAR(Data Subject Access Request) 처리 프로세스가 필수입니다.

- **[데이터베이스 + 거버넌스]**: **메타데이터 관리**, **스키마 버전 관리**, **변경 추적**은 DB 차원에서 지원되어야 합니다. Unity Catalog, Hive Metastore가 이 역할을 담당합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: GDPR 준수를 위한 개인정보 관리 체계 구축**
- **문제**: EU 고객 데이터 처리 시 GDPR Article 15~22 준수 필요
- **전략적 의사결정**:
  1. **Data Inventory**: 모든 PII 데이터의 위치, 용도, 보관 기간 파악
  2. **Consent Management**: 동의 내역 관리 시스템 구축
  3. **DSAR 자동화**: 개인정보 열람/삭제 요청 자동 처리 파이프라인
  4. **DPO 지정**: Data Protection Officer 역할 정의

**시나리오 2: Data Swamp 탈출 - Data Catalog 도입**
- **문제**: 데이터 레이크에 10PB 데이터가 있지만 무엇이 있는지 모름
- **전략적 의사결정**:
  1. **Metadata Harvesting**: 자동으로 모든 데이터 소스 스캔
  2. **Business Glossary**: 비즈니스 용어와 기술 용어 매핑
  3. **Data Stewardship**: 도메인별 데이터 관리자 지정
  4. **Self-Service**: 사용자가 직접 데이터 검색/요청 가능

### 주의사항 및 안티패턴 (Anti-patterns)

- **안티패턴 - Tool-First Approach**: 도구 구매만으로 거버넌스가 되지 않습니다. **조직과 프로세스**가 먼저 정립되어야 합니다.

- **안티패턴 - Over-Governance**: 너무 엄격한 통제는 데이터 활용을 저해합니다. **Guardrails(가드레일)** 접근으로 혁신과 통제의 균형 필요

- **안티패턴 - One-Time Project**: 거버넌스는 프로젝트가 아니라 **지속적인 프로그램**입니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | 내용 및 지표 |
|---|---|
| **정성적 효과** | - 데이터에 대한 신뢰도 향상<br>- 규제 준수 리스크 감소<br>- 데이터 검색 시간 단축 |
| **정량적 효과** | - 데이터 품질 이슈 **70% 감소**<br>- 데이터 검색 시간 **80% 단축**<br>- 규제 위반 리스크 **90% 감소** |

### 미래 전망 및 진화 방향

- **Active Metadata**: 메타데이터가 자동으로 업데이트되고 행동을 추천
- **AI-driven Governance**: AI가 자동으로 민감 데이터를 분류하고 정책을 제안
- **Data Mesh Governance**: 분산된 도메인에서 연합 거버넌스(Federated Governance)

**※ 참고 표준/가이드**:
- **DAMA-DMBOK2**: Data Management Body of Knowledge
- **DCAM (EDM Council)**: Data Management Capability Assessment Model

---

## 📌 관련 개념 맵 (Knowledge Graph)

- `[Data Quality](@/studynotes/16_bigdata/09_governance/data_quality.md)`: 데이터 품질 관리
- `[Data Lineage](@/studynotes/16_bigdata/09_governance/data_lineage.md)`: 데이터 계보 추적
- `[MDM](@/studynotes/16_bigdata/09_governance/mdm.md)`: 마스터 데이터 관리
- `[GDPR](@/studynotes/16_bigdata/09_governance/gdpr_compliance.md)`: 유럽 개인정보 규정
- `[Data Catalog](@/studynotes/16_bigdata/08_platform/data_catalog.md)`: 데이터 자산 카탈로그

---

## 👶 어린이를 위한 3줄 비유 설명

1. **데이터 거버넌스가 뭔가요?**: 학교 도서관처럼 **책(데이터)을 깔끔하게 정리하고 관리하는 규칙**이에요. 누가 관리하는지, 누가 빌릴 수 있는지 정해요.
2. **왜 필요한가요?**: 책이 아무 데나 널려 있으면 찾을 수 없잖아요? 또 소중한 책을 잃어버리면 안 되니까요!
3. **어떻게 하나요?**: 도서관 선생님(Data Steward)이 책을 정리하고, 대출 규칙(Policy)을 만들고, 누가 빌렸는지 기록해요(감사)!
