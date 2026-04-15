+++
title = "255. 데이터 파이프라인 (Apache Airflow) DAG 배치 플로우 관리"
weight = 255
date = "2024-06-04"
[extra]
categories = ["studynote", "ict_convergence", "cloud_infrastructure"]
+++

## 핵심 인사이트 (3줄 요약)
1. **DAG 기반 워크플로우 정의:** 파이썬(Python) 코드로 데이터 파이프라인(ETL/ELT)의 작업 순서와 의존성을 DAG(Directed Acyclic Graph) 구조로 명확하게 정의하고 예약하는 플랫폼입니다.
2. **분산 처리 및 확장성 보장:** 스케줄러(Scheduler), 웹 서버(Web Server), 워커(Worker), 메타데이터 DB로 아키텍처가 분리되어 있어, Celery나 Kubernetes 기반으로 병렬/분산 스케일아웃이 용이합니다.
3. **고급 스케줄링 및 모니터링:** 재시도 메커니즘, 센서(Sensor)를 통한 외부 이벤트 대기, 직관적인 UI 기반의 실패 지점 가시성을 통해 복잡한 배치 워크플로우의 안정적 운영을 담보합니다.

---

### Ⅰ. 개요 (Context & Background)
빅데이터 및 AI 분석의 고도화로 데이터소스가 다양해지면서, 데이터를 추출(Extract), 변환(Transform), 적재(Load)하는 과정이 극도로 복잡해졌습니다. 기존의 크론(Cron) 스크립트 기반 예약 방식은 작업 간의 의존성 관리, 실패 시 부분 재시도, 모니터링 한계라는 치명적인 단점을 지니고 있었습니다. 
Apache Airflow는 에어비앤비(Airbnb)에서 개발되어 오픈소스로 전환된 데이터 파이프라인 오케스트레이션 도구로, 모든 워크플로우를 **코드로 정의(Configuration as Code)**하여 형상 관리를 가능하게 하고, 복잡한 데이터 파이프라인의 생애주기를 체계적으로 관리하는 업계 표준으로 자리 잡았습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. Airflow 코어 컴포넌트
- **Scheduler:** 예약된 DAG를 파싱하여 메타데이터 DB에 작업 상태를 기록하고, 실행할 준비가 된 Task를 찾아 Executor(큐)로 전달합니다.
- **Web Server:** 플라스크(Flask) 기반의 웹 UI로, 사용자가 DAG 상태를 시각적으로 확인하고 강제 재실행, 중지 등의 관리를 수행합니다.
- **Metadata DB:** 각 DAG 실행(DagRun), 태스크 인스턴스(TaskInstance), 연결 정보, 변수 등의 모든 상태 로그를 중앙 저장합니다.
- **Executor & Worker:** 스케줄러가 큐잉한 태스크를 실제로 실행하는 프로세스입니다. (LocalExecutor, CeleryExecutor, KubernetesExecutor 등)

#### 2. DAG (Directed Acyclic Graph) 원리
- 방향성 비순환 그래프로, 파이프라인 작업(Task)이 루프(무한 반복)에 빠지지 않고 반드시 한 방향으로 흘러가 종료됨을 보장하는 구조입니다.

```text
+-------------------------------------------------------------------+
|               Apache Airflow Architecture & DAG                   |
|                                                                   |
| [1] DAG Definition (Python Code)      [3] Execution & Monitoring  |
|  Task A (Extract)                     +-----------------------+   |
|     |                                 |     Web Server (UI)   |   |
|     v                                 |   (Visualization/Log) |   |
|  Task B (Transform)                   +----------+------------+   |
|     |--------+                                   |                |
|     v        v                                   | Queries        |
|  Task C    Task D                     +----------v------------+   |
| (Load 1)  (Load 2)                    |    Metadata Database  |   |
|                                       | (PostgreSQL/MySQL)    |   |
|                                       +----------+------------+   |
| [2] Core Orchestration                           | Updates        |
|  +----------------+    Pushes Task    +----------v------------+   |
|  |   Scheduler    | ----------------> |   Executor Queue      |   |
|  | (Parses DAGs)  |   (e.g., Redis)   |  (Celery / K8s)       |   |
|  +----------------+                   +----------+------------+   |
|                                                  | Distributes    |
|                                                  v                |
|                                       +-----------------------+   |
|                                       |   Worker Node(s)      |   |
|                                       | (Executes Task A, B)  |   |
|                                       +-----------------------+   |
+-------------------------------------------------------------------+
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | Apache Airflow (배치 파이프라인) | Apache Kafka (실시간 스트리밍) | Cron (전통적 스케줄러) |
| :--- | :--- | :--- | :--- |
| **주요 목적** | 복잡한 배치 워크플로우 의존성 관리 | 대용량 실시간 이벤트 스트리밍 중계 | 단순 단일 스크립트 주기적 실행 |
| **작업 흐름** | DAG (비순환 단방향 그래프) | Pub/Sub (토픽 기반 큐잉) | 시간 기반 트리거 |
| **모니터링 / UI** | 내장된 대시보드 (Gantt, Tree 뷰) | 별도 툴 (Kafka UI, AKHQ 등 필요) | 없음 (syslog 의존) |
| **재시도 메커니즘** | 태스크 단위 자동/수동 재시도(Retries) 지원 | 오프셋(Offset) 재설정으로 리플레이 가능 | 스크립트 내 하드코딩 필요 |
| **코드 정의** | Python 기반 (IaC 유사 접근) | 클라이언트 라이브러리 연동 | 쉘 스크립트 + Crontab |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 적용 시나리오 (데이터 옵스 - DataOps)
- **멀티 클라우드 ETL 파이프라인 구축:** AWS S3에서 데이터를 추출(Sensor 대기)하고, Snowflake(데이터 웨어하우스)에서 쿼리를 실행하여 마트(Mart) 테이블을 생성한 뒤, 성공 시 Slack/Email로 알람을 보내는 일련의 과정을 단일 파이썬 파일로 구성.
- **머신러닝 MLOps 배치:** 모델 재학습 파이프라인(데이터 전처리 -> 모델 학습 -> 모델 평가 -> 모델 레지스트리 등록)을 주 단위 DAG로 구성하여, 중간 과정이 실패할 경우 어느 단계에서 문제(데이터 편향, 스크립트 오류 등)가 발생했는지 시각적으로 즉시 파악 및 조치.

#### 2. 기술사적 판단
- **아키텍처 설계 시 주의점:** Airflow는 대용량 데이터를 직접 처리하는 도구(Spark 등)가 아니라 **'작업의 지휘자(Orchestrator)'**입니다. Airflow 워커에서 무거운 판다스(Pandas) 연산을 수행하면 메모리 초과로 노드가 다운됩니다. 데이터 처리는 외부 분산 엔진(Spark, BigQuery 등)에 오프로딩하고, Airflow는 트리거와 상태 감시만 담당하는 것이 아키텍처 원칙입니다.
- **K8s 융합 (KubernetesExecutor):** 워크로드의 변동성이 큰 경우, 항상 켜져 있는 Celery 워커 대신 태스크마다 K8s Pod를 동적(On-Demand)으로 생성하고 소멸시키는 KubernetesExecutor 방식을 채택하여 자원 효율성을 극대화해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

- **기대 효과:** 파이프라인의 가시성(Observability)이 극적으로 향상되어 장애 복구 시간(MTTR)이 단축되고, 모든 파이프라인 로직이 Python 코드로 형상 관리되어 팀 간 협업 및 리뷰 프로세스가 정착됩니다.
- **결론 및 전망:** Airflow는 배치 데이터 오케스트레이션의 확고한 사실상 표준(De Facto Standard)입니다. 향후에는 데이터 변경 시점에 반응하여 파이프라인이 실행되는 데이터 인식형 스케줄링(Data-aware Scheduling) 기능이 고도화되며 Event-driven 아키텍처와의 결합이 더욱 가속화될 것입니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 데이터 엔지니어링 (Data Engineering), DataOps, MLOps
- **핵심 기술:** DAG (Directed Acyclic Graph), Celery, Kubernetes, Python
- **연관 도구:** Apache Spark, Snowflake, dbt (Data Build Tool), Luigi, Prefect, Argo Workflows

---

### 👶 어린이를 위한 3줄 비유 설명
1. 오케스트라에서 지휘자가 각 악기 연주자들에게 언제 연주를 시작하고 멈출지 지시하듯이, Airflow는 컴퓨터 프로그램들의 **'작업 지휘자'**예요.
2. 지휘자는 파이썬이라는 언어로 쓰인 악보(DAG)를 보고, "첫 번째 일이 끝나면 두 번째 일을 해!"라고 명령을 내려요.
3. 만약 누군가 실수를 하면, 전체 연주를 처음부터 다시 하지 않고 실수한 부분부터 다시 연주하게 도와주는 아주 똑똑한 시스템이랍니다!