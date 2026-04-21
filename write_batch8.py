import os
BASE = "/Users/pf/workspace/brainscience/content/studynote/07_enterprise_systems/05_data_bi"
def w(fn, txt):
    path = os.path.join(BASE, fn)
    if os.path.exists(path): print(f"SKIP: {fn}"); return
    with open(path, 'w', encoding='utf-8') as f: f.write(txt)
    print(f"OK: {fn}")

w("319_airflow_dag_pipeline.md", """\
+++
weight = 319
title = "319. 데이터 파이프라인 오케스트레이터 Airflow DAG (Airflow DAG Pipeline)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Airflow DAG (Directed Acyclic Graph)는 데이터 파이프라인을 코드로 정의하고, 의존성을 방향성 비순환 그래프로 표현해 스케줄·모니터링·재실행을 자동화한다.
> 2. **가치**: CeleryExecutor나 KubernetesExecutor로 수천 개의 태스크를 병렬 실행하고, SLA Miss 알람과 Backfill로 데이터 신뢰성을 운영 수준에서 보장한다.
> 3. **판단 포인트**: Airflow는 스케줄 기반 배치 오케스트레이션에 강하지만, 실시간 스트리밍 파이프라인은 Kafka/Flink가 적합하며 두 도구는 상호 보완 관계다.

## Ⅰ. 개요 및 필요성

데이터 파이프라인은 수십~수백 개의 태스크(ETL, 데이터 품질 검사, ML 학습, 리포트 생성)가 특정 순서와 조건으로 실행되어야 한다.
수작업 스크립트로 관리하면 의존성 파악 불가, 실패 시 재실행 어려움, 스케줄 충돌 등의 문제가 발생한다.

Airflow (Apache Airflow, Airbnb 개발)는 Python으로 DAG를 정의해:
- 태스크 간 의존성을 `>>` 연산자로 선언
- 스케줄을 cron 표현식으로 정의 (`0 2 * * *` = 매일 새벽 2시)
- Web UI에서 실행 현황·로그·재실행을 시각적으로 관리

주요 개념:
- **DAG**: Directed Acyclic Graph, 파이프라인 전체 정의
- **Task**: 개별 작업 단위 (Operator로 구현)
- **Operator**: PythonOperator, BashOperator, SparkSubmitOperator 등
- **Sensor**: 외부 조건 대기 (S3FileSensor, ExternalTaskSensor)

📢 **섹션 요약 비유**: Airflow DAG는 복잡한 공사 공정표다. 어떤 공정이 먼저 끝나야 다음 공정을 시작할 수 있는지, 언제 시작할지를 모두 코드로 관리한다.

## Ⅱ. 아키텍처 및 핵심 원리

### Executor 유형 비교

| Executor | 특징 | 병렬성 | 사용 환경 |
|:---|:---|:---|:---|
| LocalExecutor | 단일 서버 프로세스 병렬 | 수십 태스크 | 개발, 소규모 |
| CeleryExecutor | Redis/RabbitMQ 큐 기반 분산 | 수백 태스크 | 중형 프로덕션 |
| KubernetesExecutor | 태스크당 Pod 생성 | 수천 태스크 | 클라우드 네이티브 |

### XCom (Cross-Communication)

태스크 간 데이터 전달:
```python
# 업스트림 태스크가 값 push
def extract_data(**context):
    result = {"row_count": 1000}
    context['task_instance'].xcom_push(key='result', value=result)

# 다운스트림 태스크가 값 pull
def validate_data(**context):
    result = context['task_instance'].xcom_pull(
        task_ids='extract_task', key='result'
    )
    assert result['row_count'] > 0
```

주의: XCom은 소규모 메타데이터용 (대용량 데이터는 S3에 저장 후 경로 전달)

### ASCII 다이어그램: DAG 태스크 의존성 그래프

```
  DAG: daily_etl_pipeline  (cron: 0 2 * * *)
  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │  [extract_raw_data]                                         │
  │         │                                                   │
  │         ▼                                                   │
  │  [validate_schema] ──── [check_row_count]                   │
  │         │                       │                           │
  │         └───────────┬───────────┘                           │
  │                     ▼                                       │
  │           [transform_to_staging]                            │
  │                     │                                       │
  │          ┌──────────┼──────────┐                            │
  │          ▼          ▼          ▼                            │
  │    [load_dim_A] [load_dim_B] [load_dim_C]                   │
  │          │          │          │                            │
  │          └──────────┼──────────┘                            │
  │                     ▼                                       │
  │              [build_fact_table]                             │
  │                     │                                       │
  │                     ▼                                       │
  │              [refresh_BI_cache]                             │
  │                     │                                       │
  │                     ▼                                       │
  │              [send_completion_alert]                        │
  └─────────────────────────────────────────────────────────────┘
```

### Backfill과 Catchup

```bash
# 과거 날짜 데이터 소급 실행
airflow dags backfill -s 2024-01-01 -e 2024-01-31 my_dag

# Catchup: DAG 비활성화 기간 동안의 실행을 재처리 (기본 True)
# 프로덕션에서는 catchup=False 권장 (의도치 않은 대량 실행 방지)
```

📢 **섹션 요약 비유**: DAG 의존성은 도미노 게임이다. 앞 도미노(태스크)가 넘어져야 다음 도미노가 넘어지고, 어느 하나가 넘어지지 않으면 뒤도 멈춘다.

## Ⅲ. 비교 및 연결

### 오케스트레이터 비교

| 항목 | Airflow | Prefect | Dagster | Luigi |
|:---|:---|:---|:---|:---|
| 스케줄링 | 강력 (cron, sensor) | 강력 | 강력 | 제한적 |
| UI | 성숙 | 현대적 | 현대적 | 기본 |
| 코드 방식 | Python DAG (선언적) | Python Flow | Python Job | Python Task |
| 데이터 관측성 | 제한 (로그 중심) | 강함 | 매우 강함 | 없음 |
| 클라우드 관리형 | Astronomer, MWAA | Prefect Cloud | Dagster Cloud | - |

📢 **섹션 요약 비유**: Airflow는 믿을 수 있는 베테랑 공정 관리자다. Dagster와 Prefect는 현대적 UI와 관측성을 강조하는 신입이다.

## Ⅳ. 실무 적용 및 기술사 판단

### Airflow 운영 체크리스트

- [ ] DAG 파일 Git 버전 관리 (DAG 변경 이력 추적)
- [ ] SLA Miss 알람 설정: `sla=timedelta(hours=2)` 태스크 단위
- [ ] KubernetesExecutor 사용 시 태스크별 리소스 제한 (CPU, 메모리)
- [ ] catchup=False 설정 (재활성화 시 대량 소급 실행 방지)
- [ ] DB 연결 풀 관리: Worker 수 × 평균 병렬 태스크 × 커넥션 = 커넥션 풀 크기

### 안티패턴

| 안티패턴 | 문제 | 해결 방법 |
|:---|:---|:---|
| DAG 내 무거운 Python 코드 직접 실행 | Scheduler 스레드 블로킹 | SparkSubmitOperator 또는 K8s Pod 위임 |
| XCom으로 대용량 데이터 전달 | Metadata DB 용량 폭발 | S3 경로만 XCom으로 전달 |
| 모든 태스크에 동일 retry=3 | 지연 3배 증가 | 태스크별 retry 전략 다르게 |
| MAX_ACTIVE_RUNS 무제한 | DAG 중복 실행, DB 과부하 | max_active_runs=1~3 제한 |

📢 **섹션 요약 비유**: DAG 내 무거운 작업 직접 실행은 지휘자(Scheduler)가 직접 악기를 연주하는 것이다. 지휘자는 지휘만 해야 한다.

## Ⅴ. 기대효과 및 결론

| 항목 | 수작업 스크립트 | Airflow DAG |
|:---|:---|:---|
| 파이프라인 가시성 | 없음 (로그만) | Web UI 전체 상태 시각화 |
| 실패 시 재실행 | 수동 (어떤 태스크부터?) | 실패 태스크부터 자동 재실행 |
| SLA 모니터링 | 없음 | SLA Miss 자동 알람 |
| 백필 (소급 실행) | 스크립트 수동 수정 | `airflow dags backfill` 한 줄 |

📢 **섹션 요약 비유**: Airflow는 공항 관제탑이다. 모든 항공편(태스크)의 출발·도착을 실시간으로 모니터링하고, 지연이 생기면 즉시 알려준다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| DAG | 핵심 구조 | 방향성 비순환 그래프 파이프라인 |
| Operator | 태스크 구현체 | Python/Bash/Spark/S3 등 |
| Sensor | 대기 태스크 | 외부 조건 충족까지 폴링 |
| XCom | 데이터 전달 | 태스크 간 소규모 데이터 공유 |
| Executor | 실행 엔진 | Local/Celery/Kubernetes |
| Backfill | 소급 실행 | 과거 날짜 데이터 재처리 |

### 👶 어린이를 위한 3줄 비유 설명

1. Airflow DAG는 청소 순서표예요. "방 청소가 끝나야 욕실 청소를 시작할 수 있어요"처럼 순서가 정해져 있어요.
2. Operator는 각 청소 도구예요. 진공청소기(PythonOperator), 걸레(BashOperator), 소독약(SparkOperator) 등이 있어요.
3. SLA Miss 알람은 "약속한 시간까지 청소를 못 끝냈어요!"라고 알려주는 타이머예요.
""")

w("320_gnn_vector_db_recommendation.md", """\
+++
weight = 320
title = "320. 그래프 신경망 GNN 임베딩 벡터 DB Milvus 추천 시스템 (GNN Vector DB Recommendation)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GNN (Graph Neural Network)은 사용자-아이템 상호작용 그래프에서 이웃의 특징을 집계(Message Passing)하여 협업 필터링을 딥러닝으로 구현한다.
> 2. **가치**: GNN 임베딩 + 벡터 DB (Milvus)의 ANN (Approximate Nearest Neighbor) 검색으로 수억 개 아이템 중 유사 추천을 <100ms 내에 실시간으로 제공한다.
> 3. **판단 포인트**: ANN 검색의 Recall@10 ≥95%를 HNSW (Hierarchical Navigable Small World) 알고리즘이 달성하지만, 정확한 100% 매칭이 필요하다면 정확 검색(Exact Search)과 적절히 혼합해야 한다.

## Ⅰ. 개요 및 필요성

전통 추천 시스템(행렬 분해, CF)은 사용자-아이템 직접 상호작용만 활용하고, 아이템·사용자 간의 복잡한 그래프 관계(공통 구매, 브랜드, 카테고리 연결)를 무시한다.

GNN (Graph Neural Network)은 상호작용 그래프에서 이웃 노드의 특징을 집계해 더 풍부한 표현(임베딩)을 학습한다.
GNN 임베딩을 Vector DB에 저장하고 ANN 검색으로 실시간 유사 아이템·사용자를 찾는 것이 현대 추천 시스템의 표준 아키텍처다.

활용 사례:
- Pinterest: PinSage (GraphSAGE 기반 핀 추천)
- Alibaba: BGNN (Bipartite Graph NN)
- Uber Eats: GraphSAGE 음식점 추천

벡터 DB: Milvus (오픈소스), Pinecone (상용), Weaviate, Qdrant

📢 **섹션 요약 비유**: GNN 추천은 소문이다. 내 친구가 좋아하는 것, 그 친구의 친구가 좋아하는 것까지 종합해 "당신도 좋아할 것 같아요"를 제안한다.

## Ⅱ. 아키텍처 및 핵심 원리

### GNN Message Passing 메커니즘

```
GraphSAGE 1-hop 집계:
h_v^(k) = σ(W_k · CONCAT(h_v^(k-1), MEAN(h_u^(k-1) for u in N(v))))

설명:
- h_v: 노드 v의 임베딩 (k번째 레이어)
- N(v): v의 이웃 노드 집합
- MEAN: 이웃 임베딩 평균 집계
- W_k: 학습 가능한 가중치 행렬
- σ: 비선형 활성화 함수 (ReLU)
```

2-hop 집계 → 이웃의 이웃까지 정보 전파:
```
사용자 A ── 구매 ──▶ 상품 X ── 같이구매 ──▶ 상품 Y
           2-hop 학습으로 A의 임베딩에 Y 특성 반영
```

### GNN 아키텍처 비교

| 아키텍처 | 특징 | 적합 사례 |
|:---|:---|:---|
| GraphSAGE | 샘플링 + 평균 집계 | 대규모 그래프 (수십억 노드) |
| GAT (Graph Attention Network) | 어텐션 가중치로 중요 이웃 강조 | 불균형 이웃 그래프 |
| GCN (Graph Convolutional Network) | 스펙트럼 컨볼루션 | 소규모 정적 그래프 |
| LightGCN | 선형 집계 (비선형 없음) | 추천 시스템 최적화 |

임베딩 차원: 128~512d (실시간 서빙 고려 시 128~256d 권장)

### HNSW (Hierarchical Navigable Small World) ANN 검색

```
HNSW 계층 구조:
Layer 2 (최상위 - 소수 노드):  [10] ─ [50] ─ [90]
Layer 1 (중간):  [10]─[20]─[30]─[50]─[70]─[80]─[90]
Layer 0 (최하위 - 전체 노드): [모든 임베딩 벡터]

검색 과정:
1. 최상위 레이어에서 대략적 최근접 탐색
2. 아래 레이어로 내려가며 정밀화
3. 최하위에서 최종 k-NN 결과 반환

성능: O(log n) 검색, Recall@10 ≥95% (정확 검색 대비)
```

### ASCII 다이어그램: GNN + Vector DB 추천 파이프라인

```
  사용자-아이템 상호작용 그래프
  (구매, 클릭, 리뷰, 카테고리)
        │
        ▼
  ┌─────────────────────────────────────────────────────────┐
  │         GNN 학습 (배치, 주 1회)                          │
  │  GraphSAGE / LightGCN                                   │
  │  Message Passing × 2~3 hop                              │
  │  출력: 사용자 임베딩 128~256d                            │
  │         아이템 임베딩 128~256d                           │
  └──────────────────────────┬──────────────────────────────┘
                             │ 임베딩 벡터
                             ▼
  ┌─────────────────────────────────────────────────────────┐
  │         Milvus Vector DB                                │
  │  Collection: item_embeddings (10억 개 벡터)             │
  │  Index: HNSW (M=16, efConstruction=200)                 │
  │  검색: query_vector → Top-K ANN 결과 <100ms             │
  └──────────────────────────┬──────────────────────────────┘
                             │ 후보 아이템 Top-100
                             ▼
  ┌─────────────────────────────────────────────────────────┐
  │         Re-Ranking Layer                                │
  │  비즈니스 규칙 (재고 없음 제외, 광고 삽입)               │
  │  다양성 알고리즘 (동일 브랜드 중복 제거)                 │
  └──────────────────────────┬──────────────────────────────┘
                             ▼
                  최종 추천 결과 (Top-10)
                  사용자에게 <100ms 내 응답
```

### Milvus 컬렉션 설계

| 설정 | 값 | 설명 |
|:---|:---|:---|
| Collection | item_embeddings | 아이템 임베딩 저장소 |
| Dimension | 256 | 임베딩 벡터 차원 |
| Index Type | HNSW | ANN 인덱스 |
| Metric Type | COSINE | 코사인 유사도 |
| efSearch | 64 | 검색 시 탐색 폭 (높을수록 정확) |
| nprobe (IVF) | 16 | IVF 클러스터 탐색 수 |

📢 **섹션 요약 비유**: HNSW는 서울에서 부산을 찾을 때 우선 지도를 넓게 보다가 점점 좁혀가는 방식이다. 전국을 다 뒤지지 않아도 빠르게 최적 경로를 찾는다.

## Ⅲ. 비교 및 연결

### 추천 시스템 아키텍처 비교

| 방식 | 특징 | 정확도 | 실시간성 |
|:---|:---|:---|:---|
| 행렬 분해 (MF) | 사용자-아이템 직접 상호작용 | 중간 | 배치 |
| 딥러닝 (DNN) | 특징 기반 학습 | 높음 | 실시간 |
| GNN + Vector DB | 그래프 관계 활용 + ANN | 매우 높음 | 실시간 <100ms |
| 규칙 기반 | 명시적 규칙 | 낮음 (단순) | 실시간 |

### Cold Start 문제 대응

| 상황 | 대응 전략 |
|:---|:---|
| 신규 사용자 | 콘텐츠 기반 필터링 (인구통계, 행동 없음) |
| 신규 아이템 | 아이템 특징(텍스트, 이미지) 임베딩으로 유사 아이템 추천 |
| 희소 상호작용 | 그래프 구조로 이웃 정보 활용 (GNN 강점) |

📢 **섹션 요약 비유**: Cold Start는 새 학생이 전학 온 첫날이다. 친구가 없어(상호작용 없음) 추천이 어렵다. GNN은 같은 반(그래프 이웃)을 통해 빠르게 친구를 연결해준다.

## Ⅳ. 실무 적용 및 기술사 판단

### GNN 추천 시스템 체크리스트

- [ ] 그래프 크기: 수억 노드 → GraphSAGE 샘플링 필수 (전체 그래프 순회 불가)
- [ ] 임베딩 차원: 256d 권장 (정확도 vs 저장/검색 비용 균형)
- [ ] 학습 주기: 배치 학습(주 1회) + 실시간 피처 갱신 (Feature Store 연동)
- [ ] Recall@10 측정: 오프라인 평가 95% + A/B 테스트로 실제 CTR 검증
- [ ] Milvus 클러스터: 데이터 증가에 따른 동적 샤드 확장 계획

### 안티패턴

| 안티패턴 | 문제 | 해결 방법 |
|:---|:---|:---|
| GNN을 매 요청마다 추론 | 초당 수만 번 불가 (수초 소요) | 사전 임베딩 생성 + Vector DB 저장 |
| efSearch 너무 높음 | <100ms SLA 위반 | efSearch 64 → Recall 95% 균형점 |
| Re-Ranking 없음 | 재고 없는 상품, 중복 브랜드 추천 | 비즈니스 규칙 Re-Ranking 필수 |

📢 **섹션 요약 비유**: 사전 임베딩은 모든 상품 사진을 미리 찍어두는 것이다. 손님이 원하는 상품을 보여달라 하면 즉시 사진을 꺼내주면 되지, 그때그때 촬영할 수 없다.

## Ⅴ. 기대효과 및 결론

| 항목 | 전통 CF (행렬 분해) | GNN + Vector DB |
|:---|:---|:---|
| 추천 정확도 (Recall@10) | 70~80% | 90~95% |
| 응답 시간 | 수초 (배치 사전 계산) | <100ms (ANN 검색) |
| 신규 아이템 추천 | 어려움 (Cold Start) | 그래프 이웃으로 보완 |
| 확장성 | 행렬 크기 제한 | 수십억 벡터 수평 확장 |

📢 **섹션 요약 비유**: GNN + Vector DB 추천은 단골 서점 주인이 이웃 고객의 독서 취향까지 종합해 "이 책 어떠세요?"라고 즉각 제안하는 것이다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| GNN | 핵심 모델 | 그래프 기반 임베딩 학습 |
| GraphSAGE | GNN 아키텍처 | 샘플링 기반 대규모 그래프 |
| Message Passing | 핵심 메커니즘 | 이웃 특징 집계 |
| Vector DB (Milvus) | 인프라 | 임베딩 벡터 저장·ANN 검색 |
| HNSW | ANN 알고리즘 | O(log n) 근사 최근접 검색 |
| Recall@10 | 평가 지표 | ANN 검색 정확도 측정 |
| Cold Start | 문제 | 신규 사용자/아이템 추천 어려움 |

### 👶 어린이를 위한 3줄 비유 설명

1. GNN 추천은 친구의 친구가 좋아하는 것까지 알아서 "너도 좋아할 거야"라고 알려주는 시스템이에요.
2. Vector DB는 모든 상품의 '느낌'을 숫자로 저장해두는 창고예요. 비슷한 느낌의 상품을 순식간에 찾아줘요.
3. HNSW는 지도에서 확대/축소를 반복해 목적지를 빠르게 찾는 방법이에요.
""")

print("319~320 완료")
