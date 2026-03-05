+++
title = "ETL (Extract, Transform, Load)"
date = "2026-03-04"
[extra]
categories = "studynotes-enterprise"
+++

# ETL (Extract, Transform, Load)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 웨어하우스 및 분석 시스템으로 데이터를 이관하기 위해 **원천 시스템에서 추출(Extract)하고, 비즈니스 규칙에 맞게 변환(Transform)한 후, 목적지에 적재(Load)**하는 데이터 통합 프로세스입니다.
> 2. **가치**: 데이터 품질 보장, 이기종 시스템 간 데이터 통합, 비즈니스 규칙 적용, 분석용 데이터 준비를 통해 신뢰할 수 있는 데이터 기반 의사결정을 가능하게 합니다.
> 3. **융합**: ELT(Extract-Load-Transform), CDC(Change Data Capture), 실시간 스트리밍 ETL, DataOps 등으로 진화하며 클라우드 데이터 파이프라인과 결합하고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. ETL의 개념 및 철학적 근간
ETL(Extract, Transform, Load)은 데이터 웨어하우스 구축의 핵심 프로세스로, 운영 시스템(OLTP)의 데이터를 분석 시스템(OLAP)으로 이관하기 위한 **데이터 파이프라인의 3단계 처리 방식**입니다. ETL의 핵심 철학은 **"분석에 필요한 데이터를 미리 준비(Prepare)하고 검증(Validate)하여, 분석가가 신뢰할 수 있는 데이터를 제공하는 것"**입니다. 원천 데이터는 분석에 부적합한 형태(비정규화, 중복, 불일치)로 존재하므로, ETL 과정에서 이를 정제하고 구조화합니다.

#### 2. 💡 비유를 통한 이해: 식당의 재료 준비 과정
식당에서 요리를 하려면 재료가 필요합니다. 재료는 도매 시장(원천 시스템)에서 옵니다. 하지만 도매 시장에서 온 채소에는 흙이 묻어 있고, 크기가 제각각이며, 일부는 상했습니다. **ETL은 '주방에서 재료를 손질하는 과정'입니다.**
- **Extract (추출)**: 도매 시장에서 재료를 사 오는 것
- **Transform (변환)**: 채소를 씻고, 껍질을 벗기고, 크기를 맞추고, 상한 것을 버리는 것
- **Load (적재)**: 손질된 재료를 냉장고(데이터 웨어하우스)에 보관하는 것

이제 요리사(분석가)는 깨끗하고 바로 쓸 수 있는 재료로 요리(분석)를 할 수 있습니다.

#### 3. 등장 배경 및 발전 과정
- **1990년대**: 데이터 웨어하우스의 등장과 함께 ETL 개념 정립
- **1990년대 후반**: Informatica, DataStage, SSIS 등 상용 ETL 도구 등장
- **2000년대**: 데이터 통합(DI, Data Integration)으로 확장, EAI와의 경계 모호
- **2010년**: Hadoop, Spark 등 빅데이터 플랫폼 등장으로 ELT 방식 부상
- **2015년~현재**: 클라우드 네이티브 ETL(AWS Glue, Azure Data Factory), dbt, Airflow, 실시간 CDC

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. ETL 3단계 상세 분석

| 단계 | 영문 | 핵심 활동 | 기술적 고려사항 |
| :--- | :--- | :--- | :--- |
| **Extract** | 추출 | 원천 시스템에서 데이터 읽기 | 전체 추출(Full) vs 증분 추출(Incremental), CDC |
| **Transform** | 변환 | 비즈니스 규칙 적용, 데이터 정제 | 데이터 클렌징, 매핑, 집계, 조인 |
| **Load** | 적재 | 목적지 시스템에 데이터 저장 | 전체 로드(Full) vs 증분 로드(Delta), Upsert |

#### 2. ETL vs ELT 아키텍처 비교 다이어그램

```text
╔══════════════════════════════════════════════════════════════════════════════════╗
║                           [ 전통적 ETL 아키텍처 ]                                 ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║   ┌─────────────┐      ┌─────────────────────┐      ┌─────────────┐              ║
║   │   Source    │      │     ETL Server      │      │    Target   │              ║
║   │  Systems    │      │  (전용 변환 서버)    │      │   (DW/DM)   │              ║
║   │  ┌───────┐  │      │  ┌───────────────┐  │      │             │              ║
║   │  │ ERP   │──┼─────▶│  │   EXTRACT     │  │      │             │              ║
║   │  ├───────┤  │      │  │      ▼        │  │      │             │              ║
║   │  │ CRM   │──┼─────▶│  │   TRANSFORM   │  │─────▶│  Data       │              ║
║   │  ├───────┤  │      │  │  (CPU/메모리   │  │      │  Warehouse  │              ║
║   │  │ Legacy│──┼─────▶│  │   집약 처리)  │  │      │             │              ║
║   │  └───────┘  │      │  │      ▼        │  │      │             │              ║
║   └─────────────┘      │  │    LOAD       │  │      │             │              ║
║                        │  └───────────────┘  │      │             │              ║
║                        └─────────────────────┘      └─────────────┘              ║
║                                                                                  ║
║   ☹ 특징: 변환이 별도 서버에서 수행 (ETL 서버가 병목)                              ║
║   ☹ 단점: 대용량 데이터 변환 시 ETL 서버 리소스 한계                              ║
║   ✓ 장점: DW에 부하를 주지 않음, 복잡한 변환 로직 구현 용이                       ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝

                                    ▼

╔══════════════════════════════════════════════════════════════════════════════════╗
║                         [ 현대적 ELT 아키텍처 ]                                   ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║   ┌─────────────┐                        ┌─────────────────────────────────────┐ ║
║   │   Source    │                        │        Cloud Data Warehouse         │ ║
║   │  Systems    │                        │    (Snowflake, BigQuery, Redshift)  │ ║
║   │  ┌───────┐  │      ┌─────────────┐   │  ┌───────────────────────────────┐  │ ║
║   │  │ ERP   │──┼─────▶│   EXTRACT   │──▶│  │         RAW DATA              │  │ ║
║   │  ├───────┤  │      │    LOAD     │   │  │      (Staging Area)           │  │ ║
║   │  │ CRM   │──┼─────▶│  (적재만)   │──▶│  │         ┌─────────┐          │  │ ║
║   │  ├───────┤  │      └─────────────┘   │  │         │TRANSFORM│          │  │ ║
║   │  │ Logs  │──┼───────────────────────▶│  │         │ (SQL/   │          │  │ ║
║   │  └───────┘  │                        │  │         │ dbt)    │          │  │ ║
║   └─────────────┘                        │  │         └────┬────┘          │  │ ║
║                                          │  │              ▼               │  │ ║
║                                          │  │    ┌─────────────────┐      │  │ ║
║                                          │  │    │  Transformed    │      │  │ ║
║                                          │  │    │  Data (DW)      │      │  │ ║
║                                          │  │    └─────────────────┘      │  │ ║
║                                          │  └───────────────────────────────┘  │ ║
║                                          └─────────────────────────────────────┘ ║
║                                                                                  ║
║   ✓ 특징: 변환이 DW 내부에서 수행 (DW의 강력한 컴퓨팅 활용)                       ║
║   ✓ 장점: 무한 확장성, 변환 병렬 처리, 클라우드 최적화                           ║
║   ☹ 단점: RAW 데이터가 먼저 적재되어야 함 (스토리지 비용)                         ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

#### 3. 데이터 변환(Transform)의 핵심 유형

| 변환 유형 | 설명 | 예시 |
| :--- | :--- | :--- |
| **Cleansing (정제)** | 오류, 중복, 결측치 처리 | NULL → 기본값, 중복 제거 |
| **Standardization (표준화)** | 일관된 포맷/코드로 변환 | 날짜 포맷 YYYY-MM-DD, 통화 단위 통일 |
| **Integration (통합)** | 여러 소스 데이터 병합 | ERP 고객 + CRM 고객 → 통합 고객 마스터 |
| **Aggregation (집계)** | 상세 데이터를 요약 수준으로 | 일별 판매 → 월별 판매 |
| **Derivation (파생)** | 기존 데이터로 새로운 데이터 생성 | 생년월일 → 연령대 |
| **Pivoting (피벗)** | 행↔열 변환 | 월별 컬럼 → 연도/월 행 구조 |

#### 4. ETL 파이프라인 Python 구현 예시

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ETLConfig:
    """ETL 구성 정보"""
    source_table: str
    target_table: str
    extraction_type: str  # 'full' or 'incremental'
    last_extraction_date: Optional[datetime] = None
    batch_size: int = 10000

class Extractor(ABC):
    """추출기 추상 클래스"""
    @abstractmethod
    def extract(self, config: ETLConfig) -> pd.DataFrame:
        pass

class Transformer(ABC):
    """변환기 추상 클래스"""
    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

class Loader(ABC):
    """적재기 추상 클래스"""
    @abstractmethod
    def load(self, df: pd.DataFrame, target_table: str):
        pass

# === 구체적 구현 예시 ===

class SalesExtractor(Extractor):
    """판매 데이터 추출기"""

    def __init__(self, source_connection):
        self.source_connection = source_connection

    def extract(self, config: ETLConfig) -> pd.DataFrame:
        """판매 데이터 추출"""
        logger.info(f"추출 시작: {config.source_table}")

        if config.extraction_type == 'incremental':
            # 증분 추출 (마지막 추출 이후 변경된 데이터만)
            query = f"""
                SELECT * FROM {config.source_table}
                WHERE update_timestamp > '{config.last_extraction_date}'
            """
        else:
            # 전체 추출
            query = f"SELECT * FROM {config.source_table}"

        # 실제 환경에서는 DB 연결 후 쿼리 실행
        # 여기서는 샘플 데이터 생성
        data = {
            'order_id': ['ORD001', 'ORD002', 'ORD003', 'ORD004'],
            'order_date': ['2024-01-15', '2024-01-16', '2024-01-16', '2024-01-17'],
            'customer_id': ['C001', 'C002', 'C001', 'C003'],
            'product_id': ['P001', 'P002', 'P003', 'P001'],
            'quantity': [2, 1, 3, 5],
            'unit_price': [10000, 25000, 15000, 10000],
            'status': ['completed', 'completed', 'pending', 'completed']
        }
        df = pd.DataFrame(data)
        logger.info(f"추출 완료: {len(df)}행")
        return df

class SalesTransformer(Transformer):
    """판매 데이터 변환기"""

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """데이터 변환 수행"""
        logger.info("변환 시작")

        # 1. 데이터 정제
        # 완료된 주문만 필터링
        df = df[df['status'] == 'completed'].copy()

        # 2. 데이터 타입 변환
        df['order_date'] = pd.to_datetime(df['order_date'])

        # 3. 파생 컬럼 생성
        df['total_amount'] = df['quantity'] * df['unit_price']
        df['year_month'] = df['order_date'].dt.strftime('%Y-%m')

        # 4. 집계 (고객별 일일 구매 요약)
        daily_summary = df.groupby(['order_date', 'customer_id']).agg({
            'order_id': 'count',
            'total_amount': 'sum'
        }).reset_index()
        daily_summary.columns = ['order_date', 'customer_id', 'order_count', 'daily_total']

        # 5. 표준화
        daily_summary['load_timestamp'] = datetime.now()

        logger.info(f"변환 완료: {len(daily_summary)}행")
        return daily_summary

class DataWarehouseLoader(Loader):
    """데이터 웨어하우스 적재기"""

    def __init__(self, target_connection):
        self.target_connection = target_connection

    def load(self, df: pd.DataFrame, target_table: str):
        """데이터 적재 (Upsert)"""
        logger.info(f"적재 시작: {target_table}")

        # 실제 환경에서는 DB 연결 후 INSERT/UPDATE 수행
        # 여기서는 로그만 출력
        for idx, row in df.iterrows():
            logger.debug(f"  적재: {row['order_date']} | {row['customer_id']} | {row['daily_total']:,}원")

        logger.info(f"적재 완료: {len(df)}행")

class ETLPipeline:
    """ETL 파이프라인 오케스트레이터"""

    def __init__(self, extractor: Extractor, transformer: Transformer, loader: Loader):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def execute(self, config: ETLConfig) -> Dict[str, Any]:
        """ETL 파이프라인 실행"""
        start_time = datetime.now()
        logger.info(f"=== ETL 파이프라인 시작: {config.source_table} → {config.target_table} ===")

        result = {
            'status': 'SUCCESS',
            'source_table': config.source_table,
            'target_table': config.target_table,
            'start_time': start_time,
            'extracted_rows': 0,
            'transformed_rows': 0,
            'loaded_rows': 0
        }

        try:
            # 1. Extract
            extracted_data = self.extractor.extract(config)
            result['extracted_rows'] = len(extracted_data)

            # 2. Transform
            transformed_data = self.transformer.transform(extracted_data)
            result['transformed_rows'] = len(transformed_data)

            # 3. Load
            self.loader.load(transformed_data, config.target_table)
            result['loaded_rows'] = len(transformed_data)

        except Exception as e:
            result['status'] = 'FAILED'
            result['error'] = str(e)
            logger.error(f"ETL 실패: {e}")

        end_time = datetime.now()
        result['end_time'] = end_time
        result['duration_seconds'] = (end_time - start_time).total_seconds()

        logger.info(f"=== ETL 파이프라인 완료: {result['status']} ({result['duration_seconds']:.2f}초) ===")
        return result

# 실행 예시
if __name__ == "__main__":
    # ETL 구성
    config = ETLConfig(
        source_table="raw_sales",
        target_table="dw_sales_summary",
        extraction_type="incremental",
        last_extraction_date=datetime(2024, 1, 15)
    )

    # 파이프라인 구성
    pipeline = ETLPipeline(
        extractor=SalesExtractor(source_connection=None),
        transformer=SalesTransformer(),
        loader=DataWarehouseLoader(target_connection=None)
    )

    # 실행
    result = pipeline.execute(config)
    print(f"\n결과: {result['status']}")
    print(f"추출: {result['extracted_rows']}행 → 적재: {result['loaded_rows']}행")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. ETL 도구 비교 분석

| 특성 | Informatica | Talend | Apache Airflow | AWS Glue | dbt |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **유형** | 상용 ETL | 오픈소스 ETL | 워크플로우 오케스트레이션 | 클라우드 ETL | SQL 기반 변환 |
| **배포** | On-Prem/Cloud | On-Prem/Cloud | On-Prem/Cloud | Cloud (SaaS) | Cloud |
| **변환 방식** | GUI 기반 | GUI/Code | Code (Python) | GUI/Code | SQL |
| **확장성** | 중간 | 중간 | 높음 | 자동 확장 | 높음 |
| **비용** | 높음 | 무료/유료 | 무료 | 사용량 기반 | 무료/유료 |
| **적합 규모** | 대기업 | 중소~대기업 | 중간~대규모 | 클라우드 네이티브 | 현대 DW |

#### 2. 과목 융합 관점 분석
- **데이터베이스 (Data Pipeline)**: ETL은 대규모 데이터 이관을 위한 배치 처리 패턴입니다. SQL Loader, Bulk Insert, Merge 등의 DB 기능과 결합됩니다.
- **클라우드 컴퓨팅 (Cloud ETL)**: AWS Glue, Azure Data Factory, GCP Dataflow 등 서버리스 ETL 서비스가 표준화되고 있습니다.
- **데이터 사이언스 (Data Prep)**: ETL은 데이터 사이언스의 데이터 전처리(Preprocessing) 단계와 유사하며, Pandas, Spark 등과 기술적 유사성이 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단: ETL vs ELT 선택
**[상황]** J기업은 클라우드 데이터 웨어하우스(Snowflake)를 도입했습니다. ETL과 ELT 중 무엇을 선택해야 할까요?

| 평가 기준 | ETL | ELT |
| :--- | :--- | :--- |
| **변환 복잡도** | 복잡한 변환에 유리 | SQL로 표현 가능한 변환에 유리 |
| **데이터 규모** | 제한적 (ETL 서버 리소스) | 대용량 (DW 병렬 처리) |
| **비용** | ETL 서버 비용 | 스토리지 비용 (Raw 데이터 보관) |
| **유연성** | 변환 로직 변경 시 재배포 필요 | SQL 수정만으로 변경 가능 |
| **권장** | 온프레미스 DW, 복잡한 변환 | 클라우드 DW, 단순~중간 복잡도 |

**[결론]** 클라우드 DW 환경에서는 **ELT + dbt** 조합이 현대적 표준입니다.

#### 2. 도입 시 고려사항 (Checklist)
- **데이터 프로파일링**: ETL 설계 전 원천 데이터의 품질, 분포, 이상치 파악
- **증분 추출 전략**: CDC(Change Data Capture), Timestamp 기반, Trigger 기반 선택
- **에러 처리**: 데이터 품질 위반 시 Reject, Skip, 보정 등 정책 수립
- **모니터링**: ETL 작업 성공/실패 알림, 데이터 품질 메트릭 모니터링

#### 3. 안티패턴 (Anti-patterns)
- **"모든 데이터를 매번 전체 추출"**: 증분 추출을 하지 않아 시스템 부하 증가
- **"ETL 내에 비즈니스 로직 과다"**: ETL은 데이터 이관에 집중, 비즈니스 로직은 애플리케이션 또는 DB에
- **"에러 무시 후 계속"**: 데이터 품질 문제를 방치하면 신뢰할 수 없는 DW가 됨

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 개선 항목 | ETL 체계화 시 기대효과 |
| :--- | :--- | :--- |
| **데이터 품질** | 데이터 오류율 | 80% 감소 |
| **개발 생산성** | 신규 데이터 소스 연동 | 50% 단축 |
| **운영 안정성** | ETL 장애 빈도 | 70% 감소 |
| **분석 신뢰성** | 데이터 불일치 이슈 | 90% 감소 |

#### 2. 미래 전망: DataOps & Real-time ETL
- **DataOps**: ETL의 CI/CD, 자동화된 테스트, 버전 관리를 통한 데이터 파이프라인 품질 보장
- **Streaming ETL**: Kafka, Flink 기반 실시간 ETL로 배치 → 실시간 전환
- **Zero-ETL**: SaaS 애플리케이션과 클라우드 DW 간 자동 동기화 (AWS AppFlow, Fivetran)

#### 3. 참고 표준 및 가이드라인
- **Kimball Group ETL Architecture**
- **Apache Airflow Best Practices**
- **dbt Style Guide**

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [데이터 웨어하우스 (Data Warehouse)](@/studynotes/07_enterprise_systems/02_data/data_warehouse.md): ETL의 목적지 시스템
- [ELT (Extract, Load, Transform)](@/studynotes/07_enterprise_systems/02_data/elt.md): ETL의 현대적 변형
- [CDC (Change Data Capture)](@/studynotes/07_enterprise_systems/02_data/cdc.md): 실시간 증분 추출 기술
- [DataOps](@/studynotes/07_enterprise_systems/02_data/dataops.md): ETL의 DevOps화
- [Apache Airflow](@/studynotes/06_ict_convergence/02_devops/airflow.md): ETL 오케스트레이션 도구

---

### 👶 어린이를 위한 3줄 비유 설명
1. ETL은 재료를 사다가 요리할 수 있게 준비하는 과정과 같아요. 마트에서 사 온 채소를 씻고, 껍질을 벗기고, 알맞은 크기로 썰어서 냉장고에 넣어두는 것이에요.
2. 씻을 때 흙을 없애고 상한 부분을 버리듯이, ETL도 데이터에서 틀린 부분을 고치고 필요 없는 것을 없애요.
3. 이렇게 준비해 두면 요리사(분석가)가 나중에 요리(분석)할 때 바로 깨끗한 재료를 꺼내 쓸 수 있어서 훨씬 편해진답니다!
