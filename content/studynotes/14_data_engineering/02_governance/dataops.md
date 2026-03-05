+++
title = "DataOps (데이터옵스)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# DataOps (데이터옵스)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DataOps는 DevOps 원칙을 데이터 파이프라인에 적용하여, 자동화, 모니터링, 지속적 통합/배포(CI/CD)를 통해 데이터 제공의 속도와 품질을 높이는 방법론입니다.
> 2. **가치**: 데이터 파이프라인의 버전 관리, 테스트 자동화, 배포 자동화로 데이터 팀의 생산성을 극대화합니다.
> 3. **융합**: dbt, Great Expectations, Airflow, GitHub Actions 등이 결합하여 DataOps 파이프라인을 구성합니다.

---

### Ⅰ. 개요

#### 1. 핵심 원칙
- **자동화**: 파이프라인 실행, 테스트 자동화
- **버전 관리**: 코드로서의 데이터 파이프라인
- **지속적 통합**: 변경 사항 자동 테스트
- **지속적 배포**: 프로덕션 자동 배포

---

### Ⅱ. 아키텍처

```text
[Code Commit] → [CI: Test] → [CD: Deploy] → [Monitor]
     |              |              |            |
   Git          dbt test       Airflow     Alerts
               Great Expect.   dbt run
```

---

### Ⅲ. 주요 도구

| 영역 | 도구 |
|:---|:---|
| **변환** | dbt |
| **테스트** | Great Expectations |
| **오케스트레이션** | Airflow |
| **CI/CD** | GitHub Actions |

---

### Ⅳ. dbt 예시

```yaml
# dbt 프로젝트
models:
  - name: stg_customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      - name: email
        tests:
          - unique
```

---

### Ⅴ. 결론

DataOps는 현대 데이터 팀의 필수 방법론이며, 데이터 파이프라인의 품질과 속도를 모두 높입니다.

---

### 관련 개념 맵
- **[Apache Airflow](@/studynotes/14_data_engineering/03_pipelines/apache_airflow.md)**
- **[ETL vs ELT](@/studynotes/14_data_engineering/03_pipelines/etl_vs_elt.md)**

---

### 어린이를 위한 3줄 비유
1. **자동 조립 라인**: 공장에서 로봇이 자동으로 조립해요.
2. **검사 기계**: 불량품은 자동으로 걸러져요.
3. **빠르고 정확**: 사람이 하는 것보다 빠르고 실수가 없어요!
