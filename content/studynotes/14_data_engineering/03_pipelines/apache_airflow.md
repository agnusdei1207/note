+++
title = "아파치 에어플로우 (Apache Airflow)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 아파치 에어플로우 (Apache Airflow)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 아파치 에어플로우는 데이터 파이프라인 워크플로우를 DAG(Directed Acyclic Graph)로 정의하고, 스케줄링 및 모니터링하는 오픈소스 오케스트레이션 플랫폼입니다.
> 2. **가치**: "Configuration as Code"로 파이프라인을 파이썬 코드로 정의하여 버전 관리, 재사용성, 확장성을 제공합니다.
> 3. **융합**: Spark, Snowflake, Kubernetes, AWS 등 다양한 시스템과 연동되며, 현대 데이터 엔지니어링의 표준 워크플로우 도구입니다.

---

### Ⅰ. 개요

#### 1. 핵심 구성요소
- **DAG**: 방향성 비순환 그래프, 워크플로우 정의
- **Task**: 개별 작업 단위
- **Operator**: Task 실행기 (Bash, Python, SQL)
- **Scheduler**: 작업 스케줄링
- **Web UI**: 모니터링 및 관리

---

### Ⅱ. 아키텍처

```text
+------------------+
|   Web Server     |
+--------+---------+
         |
+--------v---------+
|   Scheduler      |
+--------+---------+
         |
+--------v---------+
|   Executor       |
| - LocalExecutor  |
| - CeleryExecutor |
| - K8sExecutor    |
+--------+---------+
         |
+--------v---------+
|   Metadata DB    |
| (PostgreSQL)     |
+------------------+
```

---

### Ⅲ. DAG 예시

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract():
    print("Extracting data...")

def transform():
    print("Transforming data...")

def load():
    print("Loading data...")

with DAG('etl_pipeline', start_date=datetime(2024, 1, 1), schedule_interval='@daily') as dag:

    t1 = PythonOperator(task_id='extract', python_callable=extract)
    t2 = PythonOperator(task_id='transform', python_callable=transform)
    t3 = PythonOperator(task_id='load', python_callable=load)

    t1 >> t2 >> t3
```

---

### Ⅳ. 주요 Operator

- **PythonOperator**: Python 함수 실행
- **BashOperator**: Bash 명령 실행
- **SparkSubmitOperator**: Spark 작업 제출
- **SnowflakeOperator**: Snowflake SQL 실행

---

### Ⅴ. 결론

에어플로우는 데이터 파이프라인 오케스트레이션의 사실상 표준이며, 코드로 관리되는 워크플로우의 핵심 도구입니다.

---

### 관련 개념 맵
- **[데이터 파이프라인](@/studynotes/14_data_engineering/03_pipelines/data_pipeline.md)**
- **[DataOps](@/studynotes/14_data_engineering/02_governance/dataops.md)**

---

### 어린이를 위한 3줄 비유
1. **악보**: 음악을 연주하려면 악보가 필요해요. 에어플로우는 악보예요.
2. **지휘자**: 지휘자가 악보를 보고 연주 순서를 정해요.
3. **자동 연주**: 악보를 주면 알아서 순서대로 연주해줘요!
