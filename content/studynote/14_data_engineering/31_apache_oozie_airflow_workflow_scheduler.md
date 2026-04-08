+++
title = "31. 아파치 우지 (Apache Oozie) / 아파치 에어플로우 (Apache Airflow) - 복잡한 분산 파이프라인 작업 간 DAG 의존성 스케줄링 관리"
date = "2026-04-07"
[extra]
categories = "studynote-data-engineering"
+++

# Apache Oozie / Apache Airflow: 데이터 파이프라인 워크플로우 스케줄러

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Oozie (우지) 와 Apache Airflow (에어플로우) 는 복잡한 분산 데이터 파이프라인의 작업 간 의존성(Dependency)과 실행 순서를 DAG (Directed Acyclic Graph, 방향성 비순환 그래프) 로 정의하고 스케줄링·모니터링하는 워크플로우 오케스트레이션 도구다.
> 2. **가치**: 수십 개의 ETL 작업이 복잡하게 얽힌 배치 파이프라인에서 "A가 완료되면 B와 C를 동시 실행하고, B와 C가 모두 완료되면 D를 실행"하는 의존성 로직을 코드로 선언하여 자동화함으로써, 파이프라인 실패 감지·재실행·알림을 무인화한다.
> 3. **융합**: Oozie는 Hadoop 에코시스템(HDFS, MapReduce, Hive, Pig) 전용이지만, Airflow는 Python 코드 기반 DAG를 통해 Spark, dbt, Kubernetes, GCP BigQuery, AWS S3 등 이기종 시스템 전체를 단일 파이프라인으로 오케스트레이션할 수 있어 현대 데이터 스택의 표준으로 자리잡았다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 데이터 파이프라인은 수집→변환→적재의 각 단계가 여러 분산 작업으로 쪼개지고, 각 작업이 이전 작업 완료에 의존한다. 단순 cron은 의존성 처리, 실패 재실행, 모니터링 기능이 없다. Oozie와 Airflow는 이 한계를 DAG 기반 워크플로우로 해결한다.
- **필요성**: "야간 Hive 집계(2h) → 보고서 생성(30min) → 이메일 발송"처럼 순차 의존성이 있는 파이프라인을 cron으로 구성하면 실패 감지가 불가하고 실패 시 수동 재실행이 필요하다. 워크플로우 스케줄러는 이 복잡성을 코드화·자동화한다.
- **💡 비유**: 공항의 수하물 컨베이어 시스템과 같다. 비행기 착륙(트리거)→수하물 내림(Task A)→X-ray 검사(Task B)→컨베이어 분류(Task C)가 정확한 순서와 의존성으로 자동 동작해야 한다.
- **등장 배경**: Oozie → Yahoo! 내부 Hadoop 작업 스케줄러로 시작(2009) → Airflow → Airbnb 내부 도구로 시작(2014), 2016년 Apache Incubator 편입, 현재 사실상 표준.

```text
┌────────────────────────────────────────────────────────┐
│         DAG 기반 파이프라인 의존성 구조 시각화               │
├────────────────────────────────────────────────────────┤
│                                                        │
│  [Oozie/Airflow DAG 예시: 일간 매출 보고 파이프라인]        │
│                                                        │
│  extract_db ───┐                                       │
│                ├──▶ transform_sales ──▶ load_dw ──▶   │
│  extract_api ──┘                           │          │
│                                            ▼          │
│                                     generate_report   │
│                                            │          │
│                                            ▼          │
│                                      send_email       │
│                                                        │
│  → DAG에서 extract_db와 extract_api는 병렬 실행           │
│  → transform은 둘 다 완료 후 실행 (의존성 보장)            │
│  → 실패 시 해당 Task만 재실행 (업스트림 재실행 불필요)       │
└────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 DAG는 두 개의 추출 작업(extract_db, extract_api)이 병렬로 실행되고, 둘 다 완료된 후에야 transform_sales가 시작되는 의존성 구조를 보여준다. Cron으로는 병렬 실행 조율과 의존성 완료 대기가 불가능하지만, Airflow DAG는 이를 Python 코드로 간결하게 선언한다. 또한 transform 단계에서 실패가 발생해도 extract가 이미 성공했으므로 transform만 재실행(Resume)하면 되어 파이프라인 전체 복구 비용이 최소화된다.

- **📢 섹션 요약 비유**: 여러 재료(데이터)를 동시에 준비하고, 모든 재료가 갖춰지면 요리(변환)를 시작하며, 요리가 완성되면 서빙(적재)하는 자동 로봇 주방 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Airflow 핵심 컴포넌트

| 컴포넌트 | 역할 | 설명 |
|:---|:---|:---|
| **DAG 파일 (Python)** | 워크플로우 정의 | Task와 의존성을 Python 코드로 선언 |
| **Scheduler** | DAG 파싱·실행 트리거 | `schedule_interval` 기준으로 DAG Run 생성 |
| **Executor** | Task 실제 실행 | LocalExecutor / CeleryExecutor / KubernetesExecutor |
| **Worker** | Task 처리 프로세스 | Celery 기반 분산 워커 또는 K8s Pod |
| **Metadata DB** | DAG·Task 상태 저장 | PostgreSQL / MySQL |
| **Web UI** | DAG 시각화·모니터링·재실행 | 그래프/간트차트·로그 조회 |

---

### Airflow DAG 코드 구조 예시

```text
┌────────────────────────────────────────────────────────────┐
│              Airflow DAG Python 코드 구조                    │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  from airflow import DAG                                   │
│  from airflow.operators.python import PythonOperator       │
│  from datetime import datetime                             │
│                                                            │
│  with DAG(                                                 │
│      dag_id='daily_sales_report',                          │
│      schedule_interval='0 2 * * *',  # 매일 오전 2시        │
│      start_date=datetime(2026, 1, 1),                      │
│      catchup=False,                                        │
│  ) as dag:                                                 │
│                                                            │
│      extract_db  = PythonOperator(task_id='extract_db',     │
│                       python_callable=extract_db_fn)        │
│      extract_api = PythonOperator(task_id='extract_api',    │
│                       python_callable=extract_api_fn)       │
│      transform   = PythonOperator(task_id='transform', …)  │
│      load        = PythonOperator(task_id='load', …)       │
│                                                            │
│      # 의존성 선언 (업스트림 >> 다운스트림)                    │
│      [extract_db, extract_api] >> transform >> load        │
│                                                            │
│  Scheduler가 이 파일을 파싱 → 실행 계획 생성                  │
└────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Airflow DAG는 Python 코드로 작성되어 "Configuration as Code" 원칙을 따른다. `>>` 연산자로 의존성을 단 한 줄로 표현할 수 있는 것이 핵심 강점이다. Oozie는 XML로 워크플로우를 정의하기 때문에 복잡한 파이프라인에서 수백 줄의 XML이 필요하지만, Airflow는 Python의 풍부한 생태계(루프, 조건문, 동적 Task 생성)를 활용하여 간결하게 복잡한 로직을 표현한다. 또한 Jinja 템플릿과 Airflow Variables/Connections 기능으로 파라미터화와 시크릿 관리가 코드 레벨에서 가능하다.

- **📢 섹션 요약 비유**: Oozie는 XML로 빼곡히 쓰는 공식 계약서이고, Airflow는 Python으로 자유롭게 작성하는 스마트 지시서입니다. 복잡할수록 Python의 유연성이 압도적으로 유리합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### Oozie vs Airflow 비교

| 비교 기준 | Apache Oozie | Apache Airflow |
|:---|:---|:---|
| **정의 방식** | XML 워크플로우 정의 | Python 코드(DAG) |
| **Hadoop 의존성** | HDFS 의존, Hadoop 전용 설계 | Hadoop 비의존, 범용 |
| **UI** | 단순 웹 UI | 풍부한 그래프·간트·로그 UI |
| **커뮤니티** | 쇠퇴 (Hadoop 생태계 약화와 함께) | 활발·대규모 플러그인 생태계 |
| **동적 DAG** | 어려움 | Python으로 프로그래매틱 생성 가능 |
| **적합 환경** | 레거시 Hadoop 클러스터 | 현대 데이터 스택 전반 |

```text
┌────────────────────────────────────────────────────────────┐
│      Airflow Executor 유형별 확장 아키텍처 비교               │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  [LocalExecutor]                                           │
│   Scheduler 프로세스 내에서 병렬 Task 실행                    │
│   소규모 팀, 단일 서버 환경 적합                             │
│                                                            │
│  [CeleryExecutor]                                          │
│           Scheduler                                        │
│               │                                            │
│          Celery 메시지 브로커 (Redis/RabbitMQ)               │
│           ├─ Worker 1  ├─ Worker 2  ├─ Worker 3            │
│   수평 확장 가능, 고가용성                                    │
│                                                            │
│  [KubernetesExecutor]                                      │
│   Task 1개당 K8s Pod 1개 생성 → 실행 완료 후 Pod 소멸         │
│   리소스 격리·자동 스케일링 최적, 클라우드 네이티브 환경 추천     │
└────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Airflow의 Executor는 확장성 요구에 따라 교체 가능하다. 소규모 팀은 LocalExecutor, 중규모는 CeleryExecutor, 클라우드 네이티브 환경은 KubernetesExecutor가 최적이다. KubernetesExecutor는 Task마다 독립된 Pod를 생성·소멸하므로 자원 격리와 자동 스케일링이 탁월하지만 Pod 기동 지연(Cold Start)이 발생한다. 실무에서는 KubernetesExecutor에 미리 warm pod pool을 유지하는 `KubernetesPodOperator`와의 조합으로 지연을 완화한다.

- **📢 섹션 요약 비유**: LocalExecutor는 혼자서 여러 일을 하는 프리랜서, CeleryExecutor는 업무를 여러 직원에게 나눠주는 팀장, KubernetesExecutor는 일이 생길 때마다 계약직을 채용하고 완료 후 바로 해고하는 프로젝트 기반 조직입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오
1. **시나리오 — DAG 실패 감지 지연으로 비즈니스 임팩트**: 새벽 2시 파이프라인 실패를 아침 9시 출근 후에야 발견, 일간 매출 보고서가 9시간 지연.
   - **판단**: SLA Miss 알림(`sla=timedelta(hours=4)`) 설정 + Slack/PagerDuty 연동 알림. Task 실패 시 즉각 On-Call 담당자에게 Webhook 알림이 발송되도록 DAG에 `on_failure_callback` 추가.
2. **시나리오 — 레거시 Oozie에서 Airflow 마이그레이션**: 수십 개의 Oozie XML 워크플로우를 Airflow로 전환 시 의존성 재현 오류.
   - **판단**: Oozie-to-Airflow 변환 오픈소스 도구(Google Cloud Composer 지원 migration tool)를 활용하되, 자동 변환 후 반드시 DAG 그래프 시각화 검증을 통해 의존성이 동일하게 재현됐는지 확인한다.

### 도입 체크리스트
- **기술적**: DAG `catchup=True` 설정 시 과거 누락된 실행이 한꺼번에 대량으로 시작되어 시스템 과부하가 발생할 수 있다. 초기 배포 시 `catchup=False`가 기본값인지 확인.
- **운영적**: DAG 파일이 Git에 관리되고 CI/CD 파이프라인을 통해 스테이징 Airflow에서 먼저 검증 후 프로덕션에 배포하는 GitOps 워크플로우가 수립되어 있는가?

### 안티패턴
- **DAG 내 복잡한 비즈니스 로직 직접 구현**: DAG는 오케스트레이션 선언에 집중하고, 실제 데이터 처리는 Spark/dbt/Python 스크립트에서 분리해야 한다. DAG 파일 안에 수백 줄의 pandas 처리 코드가 들어가면 테스트·재사용·디버깅이 불가능해진다.

- **📢 섹션 요약 비유**: 교통 신호등(DAG)은 "언제 어느 차선이 출발할지"만 결정하고, 실제 자동차 운전(데이터 처리)은 각 차 운전자(Spark/dbt 작업)가 담당해야 합니다. 신호등이 직접 운전하려 하면 교통 체계 전체가 마비됩니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | Cron 기반 스케줄링 | Airflow DAG 오케스트레이션 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 실패 감지 수 시간~수동 확인 | SLA 알림 + 자동 재시도 수 분 내 탐지 | 파이프라인 장애 MTTR **90% 단축** |
| **정량** | 의존성 관리 수동 Shell 스크립트, 오류 잦음 | DAG 코드화로 의존성 100% 자동 보장 | 데이터 불일치 장애 **제로 수준** |
| **정성** | 파이프라인 전체 구조 문서화 없음 | Web UI 그래프로 전체 파이프라인 시각화 | 신규 엔지니어 온보딩 기간 단축 |

### 미래 전망
- **Airflow 3.0+ (Asset-Driven Scheduling)**: 특정 파일이 S3에 업로드되거나 데이터셋이 업데이트되는 "이벤트"를 트리거로 DAG를 실행하는 이벤트 주도형 스케줄링이 강화되고 있다.

### 참고 표준
- **Apache Airflow AIP (Airflow Improvement Proposals)**: 커뮤니티 주도 기능 로드맵. AIP-72가 Airflow 3.0 Task Flow API 개선 정의.

- **📢 섹션 요약 비유**: Airflow는 모든 열차(데이터 작업)의 출발·도착 시간표를 정밀 관리하고 지연 시 즉시 알리는 철도 관제 시스템입니다. cron은 그냥 주기만 맞춰 출발 신호를 주는 알람시계에 불과합니다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

- **DAG (Directed Acyclic Graph)** | Airflow/Oozie에서 Task 간 의존성을 표현하는 방향성 비순환 그래프. 사이클이 없어야 무한 루프 방지.
- **ETL (Extract-Transform-Load)** | 대부분의 Airflow DAG가 오케스트레이션하는 핵심 데이터 처리 패턴.
- **dbt (data build tool)** | SQL 변환 로직을 정의하는 도구. Airflow의 `DbtOperator`로 오케스트레이션하는 현대 데이터 스택의 표준 조합.
- **Celery** | CeleryExecutor 기반 Airflow의 Task 분산 처리 백엔드 메시지 큐.
- **MLflow / Kubeflow Pipelines** | ML 학습 파이프라인 전문 오케스트레이터. ML에 특화된 점을 제외하면 Airflow와 유사한 역할.

---

## 👶 어린이를 위한 3줄 비유 설명
1. Airflow는 회사의 여러 업무들이 **정해진 순서대로** 자동으로 처리되게 해주는 스마트 할 일 목록 관리자예요.
2. "A가 끝나면 B와 C를 동시에 하고, B와 C가 둘 다 끝나야 D를 시작해"처럼 복잡한 순서를 코드로 적어두면 컴퓨터가 알아서 다 진행해줘요.
3. 혹시 중간에 실수로 B가 실패해도 Airflow가 바로 알아채고 알림을 보내고, B만 다시 실행해 주니까 처음부터 다시 할 필요가 없답니다.
