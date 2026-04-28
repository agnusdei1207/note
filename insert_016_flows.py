import re

# Flow section content for each file (topic -> flow text + explanation sentence)
FLOWS = {
    "016_fet.md": {
        "flow": """```text
[진공관 (Vacuum Tube) — 고발열·고전력 전자 증폭 소자]
    │
    ▼
[BJT (Bipolar Junction Transistor) — 전류 제어 방식 증폭·스위칭]
    │
    ▼
[FET (Field-Effect Transistor) — 전압 제어·저전력 고입력 임피던스]
    │
    ▼
[MOSFET (Metal-Oxide-Semiconductor FET) — 게이트 완전 절연, 디지털 집적 표준]
    │
    ▼
[FinFET — 3D 핀 구조로 누설 전류 억제, 22nm 이하 공정]
    │
    ▼
[GAA (Gate-All-Around) FET — 4면 게이트 완전 포위, 3nm 이하 차세대 소자]
```
이 흐름은 전류 제어 방식(BJT)이 고발열·입력 부하 한계를 드러내면서 전압 제어 방식의 FET가 등장하고, MOSFET이 저전력 디지털 집적의 왕좌를 차지한 뒤 미세화에 따른 누설 전류 문제를 극복하기 위해 2D 평면에서 3D 입체 구조(FinFET→GAA)로 진화하는 반도체 능동 소자의 계보를 보여준다."""
    },
    "016_interrupt_mechanism.md": {
        "flow": """```text
[폴링 (Polling) — CPU가 장치 상태를 반복 조회, 자원 낭비]
    │
    ▼
[인터럽트 (Interrupt) — 장치가 완료 시 CPU에 신호, 비동기 이벤트 처리]
    │
    ▼
[인터럽트 우선순위 / PIC — 다중 인터럽트 충돌 조정, 중첩 처리]
    │
    ▼
[DMA (Direct Memory Access) — CPU 개입 없이 대량 데이터 전송 후 인터럽트 통보]
    │
    ▼
[인터럽트 친화성 (Interrupt Affinity) — 멀티코어 환경의 분산 인터럽트 처리]
```
이 흐름은 CPU가 장치를 수시로 확인하는 비효율적인 폴링 방식에서 이벤트 기반 인터럽트로 전환되고, 우선순위와 DMA를 거쳐 멀티코어 시대에는 인터럽트 자체를 여러 코어에 분산 처리하는 형태로 진화해 온 OS 이벤트 처리 아키텍처의 발전 경로를 보여준다."""
    },
    "016_전파_지연.md": {
        "flow": """```text
[전파 지연 (Propagation Delay) — 거리/빛의 속도, 물리적 절대 하한]
    │
    ▼
[RTT (Round Trip Time) — 왕복 전파 지연으로 애플리케이션 체감 속도 결정]
    │
    ▼
[BDP (지연-대역폭 곱) — 링크 내 미확인 데이터 최대량, TCP 창 크기 설계 기준]
    │
    ▼
[CDN (Content Delivery Network) — 정적 콘텐츠를 지리적 엣지에 캐싱, 거리 단축]
    │
    ▼
[MEC (Multi-access Edge Computing) — 연산을 기지국 근방으로 이동, 1ms 미만 목표]
```
이 흐름은 빛의 속도라는 물리적 절대 한계를 인정하면서, 데이터와 연산을 사용자 가까이 이동시키는 방향(중앙 집중 → CDN → 엣지)으로 아키텍처가 진화해 온 네트워크 지연 극복 전략의 계보를 보여준다."""
    },
    "016_cmmi_5_levels.md": {
        "flow": """```text
[CMMI Level 1 (초기) — 개인 역량 의존, 프로세스 비공식]
    │
    ▼
[CMMI Level 2 (관리) — 프로젝트별 기본 관리, 계획·추적 수립]
    │
    ▼
[CMMI Level 3 (정의) — 조직 표준 프로세스 정의, OPA 자산 축적]
    │
    ▼
[CMMI Level 4 (정량적 관리) — SPC 통계 제어, 측정 기반 품질 관리]
    │
    ▼
[CMMI Level 5 (최적화) — 혁신·원인 분석으로 지속 개선 내재화]
    │
    ▼
[Compliance as Code — CI/CD 파이프라인 내 자동 CMMI 통제, CMMI v2.0+]
```
이 흐름은 개인에 의존하던 개발 조직이 단계별 프로세스 규율을 내재화하여 예측 가능하고 자기 진화하는 소프트웨어 생산 체계로 성숙해가는 과정을 보여주며, 최신 DevSecOps 파이프라인으로의 통합이 그 종착점이다."""
    },
    "016_network_data_model.md": {
        "flow": """```text
[계층형 데이터 모델 (Hierarchical Model) — 트리 구조, 1:N 단일 부모 제약]
    │
    ▼
[망형 데이터 모델 (Network Model / CODASYL) — 포인터 기반 N:M 관계 허용]
    │
    ▼
[관계형 데이터 모델 (Relational Model) — 수학적 테이블, SQL 선언적 질의]
    │
    ▼
[객체지향 DB (OODB) — 복잡한 객체와 메서드를 직접 영속화]
    │
    ▼
[그래프 데이터베이스 (Graph DB) — 노드-엣지 구조로 딥 조인 성능 한계 극복]
```
이 흐름은 초기 데이터 모델이 물리적 포인터 복잡성의 한계를 반성하고 관계형 모델로 수렴되었다가, 고도로 연결된 현대 데이터의 딥 탐색 요건에 부응하여 그래프 데이터베이스로 재귀환하는 데이터 모델 패러다임의 순환 진화를 보여준다."""
    },
    "016_dpos_delegated_pos.md": {
        "flow": """```text
[PoW (Proof of Work) — 해시 연산 경쟁, 높은 에너지 소비]
    │
    ▼
[PoS (Proof of Stake) — 지분 비례 검증, 에너지 효율 개선]
    │
    ▼
[DPoS (Delegated PoS) — 대표 노드(BP) 선출, TPS 수천 단위 고성능]
    │
    ▼
[DPoS + BFT 융합 — 블록 최종성(Finality) 확정, 엔터프라이즈 신뢰 확보]
    │
    ▼
[레이어 2 롤업 시퀀서 (L2 Rollup Sequencer) — DPoS 원리의 고성능 레이어 2 적용]
```
이 흐름은 블록체인이 에너지 소비와 속도 사이의 트레이드오프를 풀기 위해 전체 참여 방식에서 대표 선출 방식으로 진화하고, 이를 레이어 2 확장 솔루션에까지 이식하는 합의 알고리즘의 발전 경로를 보여준다."""
    },
    "016_bpr.md": {
        "flow": """```text
[기능별 사일로 조직 — 순차 업무, 다단계 결재, 높은 리드 타임]
    │
    ▼
[BPR (Business Process Reengineering) — 핵심 프로세스 근본 재설계, 성과 도약]
    │
    ▼
[ERP 기반 통합 — 재설계 프로세스를 전사 시스템으로 구현]
    │
    ▼
[프로세스 마이닝 (Process Mining) — 로그 기반 실제 흐름 자동 분석, 재설계 정밀도 향상]
    │
    ▼
[RPA / AI 자동화 — 재설계된 반복 구간을 봇이 대체, 초자동화 완성]
```
이 흐름은 과거 기능 부서별 점진적 개선의 한계를 인식한 BPR이 프로세스 중심 조직 설계의 이론적 기반이 되고, ERP 구현→프로세스 마이닝 고도화→RPA 자동화로 이어지는 디지털 전환의 핵심 방법론 진화를 보여준다."""
    },
    "016_sort_comparison.md": {
        "flow": """```text
[O(N²) 단순 비교 정렬 — 버블/선택/삽입, 소규모 또는 거의 정렬된 데이터]
    │
    ▼
[O(N log N) 분할 정복 — 합병 정렬(안정)/퀵 정렬(평균 최고)/힙 정렬(최악 보장)]
    │
    ▼
[비비교 선형 정렬 — 계수 정렬/기수 정렬/버킷 정렬, 정수·제한 범위 특화]
    │
    ▼
[하이브리드 정렬 (Timsort / Introsort) — 실제 데이터 패턴 감지 후 알고리즘 혼합]
    │
    ▼
[분산 정렬 (Distributed Sort) — MapReduce/Spark 기반 대규모 외부 정렬]
```
이 흐름은 단순 구조의 O(N²) 정렬이 이론적 한계를 드러낸 뒤 O(N log N) 분할정복으로 발전하고, 선형 정렬과의 하이브리드 실용화를 거쳐 분산 환경의 대규모 정렬로 확장되는 정렬 알고리즘의 진화 계보를 보여준다."""
    },
    "016_max_flow.md": {
        "flow": """```text
[DFS 기반 Ford-Fulkerson — 증가 경로 탐색, 무한 루프 위험(비정수 용량)]
    │
    ▼
[BFS 기반 Edmonds-Karp — O(VE²) 다항 시간 보장, 최단 증가 경로 선택]
    │
    ▼
[Dinic's Algorithm — 계층 그래프 + 차단 흐름, O(V²E) 고성능]
    │
    ▼
[Max-Flow Min-Cut 정리 — 최대 유량 = 최소 컷, 네트워크 병목 분석 기반]
    │
    ▼
[이분 매칭 (Bipartite Matching) / 프로젝트 선택 — 최대 유량으로 환원하는 응용]
```
이 흐름은 그래프 유량 문제의 기초 아이디어(Ford-Fulkerson)가 수렴 보장의 결함을 극복하며 효율적인 알고리즘으로 정제되고, 그 결과물인 Max-Flow Min-Cut 정리가 매칭·분리·스케줄링 등 다양한 문제를 통합하는 이론적 기반으로 자리잡는 과정을 보여준다."""
    },
    "016_open_addressing.md": {
        "flow": """```text
[직접 주소 테이블 (Direct Address Table) — 키를 인덱스로 직접 사용, 공간 낭비]
    │
    ▼
[체인법 (Chaining) — 충돌 시 연결 리스트로 분리, 외부 메모리 할당]
    │
    ▼
[개방 주소법 — 선형 탐사 → 이차 탐사 → 이중 해싱, 테이블 내부 배치]
    │
    ▼
[로빈 후드 해싱 (Robin Hood Hashing) — 탐사 거리 편차를 균등화하는 개선판]
    │
    ▼
[쿠쿠 해싱 (Cuckoo Hashing) — 최악 O(1) 조회 보장, 두 테이블 교차 배치]
```
이 흐름은 해시 충돌을 외부 자료구조에 위임하는 체인법의 포인터 오버헤드를 줄이기 위해 테이블 내부에서 탐사를 수행하는 개방 주소법이 등장하고, 클러스터링 문제를 해결하는 방향으로 점진적으로 정교화되는 해시 충돌 해결 전략의 발전을 보여준다."""
    },
    "016_hypothesis_testing.md": {
        "flow": """```text
[기술통계 (Descriptive Statistics) — 데이터 요약, 평균·분산·분포 파악]
    │
    ▼
[추론통계 (Inferential Statistics) — 표본으로 모집단 추정, 오차 포함]
    │
    ▼
[가설 검정 (Hypothesis Testing) — H₀ 기각 여부 판단, p-값·유의수준 α]
    │
    ▼
[효과 크기 + 신뢰구간 — 통계적 유의성과 실용적 중요성 구분]
    │
    ▼
[베이즈 통계 (Bayesian Statistics) — 사전 확률 갱신, p-값 한계 극복]
```
이 흐름은 데이터를 요약하는 기술통계에서 모집단을 추론하는 통계적 가설 검정으로 발전한 후, p-값 남용 문제를 인식하고 효과 크기와 베이즈 관점으로 보완하는 통계적 추론 방법론의 성숙 과정을 보여준다."""
    },
    "016_hill_climbing.md": {
        "flow": """```text
[무작위 탐색 (Random Search) — 해 공간 무작위 표본, 보장 없음]
    │
    ▼
[언덕 오르기 (Hill Climbing) — 현재보다 나은 이웃으로 이동, 지역 최적해 위험]
    │
    ▼
[무작위 재시작 언덕 오르기 (Random-Restart HC) — 여러 시작점으로 지역 최적해 완화]
    │
    ▼
[모의 담금질 (Simulated Annealing) — 확률적 내리막 허용으로 탈출]
    │
    ▼
[경사 하강법 (Gradient Descent) — 연속 미분 가능 공간에서 언덕 내리기, 딥러닝 핵심]
```
이 흐름은 탐욕적 이웃 이동이라는 언덕 오르기의 직관적 아이디어가 지역 최적해 함정을 극복하는 다양한 메타휴리스틱으로 발전하고, 그 역방향(최소화) 개념이 현대 딥러닝의 경사 하강법으로 계승되는 최적화 알고리즘의 진화 계보를 보여준다."""
    },
    "016_kick_off_meeting.md": {
        "flow": """```text
[예비 조사 (Preliminary Survey) — 사전 산출물 검토, 감리 주안점 도출]
    │
    ▼
[착수 회의 (Kick-off Meeting) — 이해관계자 역할·범위·일정 공식 합의]
    │
    ▼
[현장 감리 (On-site Audit) — 소스코드·아키텍처·보안 집중 점검]
    │
    ▼
[중간 보고 (Interim Report) — 주요 결함 조기 통보, 개선 방향 협의]
    │
    ▼
[종료 회의 (Exit Meeting) — 착수 합의 사항과 결과 대조, 최종 감리 확정]
```
이 흐름은 정보시스템 감리의 전체 수명 주기에서 착수 회의가 예비 조사를 집약하여 이후 모든 활동의 기준점을 설정하는 핵심 역할을 하며, 이를 중심으로 감리 전 과정이 유기적으로 연결되는 구조를 보여준다."""
    },
    "016_tco.md": {
        "flow": """```text
[CAPEX 단일 집중 — 취득 원가만 고려, 숨은 유지·폐기 비용 무시]
    │
    ▼
[TCO (Total Cost of Ownership) — 전 생애주기 비용 가시화, 직간접비 통합]
    │
    ▼
[ABC (Activity-Based Costing) — 활동 단가 기준 간접비 배분, 숨은 비용 정량화]
    │
    ▼
[FinOps — 클라우드 과금 API 연동 실시간 TCO 모니터링, 재무-엔지니어링 협업]
    │
    ▼
[AIOps 비용 최적화 — 워크로드 패턴 분석 자동 자원 조정, TCO 지속 최소화]
```
이 흐름은 취득 원가만 보던 시각에서 전 생애주기 비용으로 관점이 확장되고, 클라우드 시대에는 실시간 AI 기반 비용 거버넌스로 진화하는 IT 비용 관리 패러다임의 발전을 보여준다."""
    },
    "016_hypervisor.md": {
        "flow": """```text
[물리 서버 독점 (Bare-metal) — 단일 OS·워크로드 고정 배치, 자원 낭비]
    │
    ▼
[Type-1 하이퍼바이저 (Bare-metal VMM) — 하드웨어 직접 제어, 엔터프라이즈 표준]
    │
    ▼
[Type-2 하이퍼바이저 (Hosted VMM) — 호스트 OS 위 동작, 개발·테스트 환경]
    │
    ▼
[하드웨어 보조 가상화 (Intel VT-x / AMD-V) — CPU 내장 VMX 명령어로 오버헤드 대폭 절감]
    │
    ▼
[컨테이너 (Container) — 게스트 OS 제거, 프로세스 수준 격리로 초경량화]
    │
    ▼
[마이크로VM / DPU 오프로딩 — Firecracker ms 부팅·서버리스 FaaS, Nitro 베어메탈급 클라우드]
```
이 흐름은 물리 서버의 자원 낭비를 해소하기 위해 등장한 하이퍼바이저가 성능 오버헤드를 하드웨어 가속으로 해결하고, 컨테이너와 마이크로VM으로 경량화되어 서버리스 클라우드의 최소 실행 단위로 진화하는 가상화 기술의 계보를 보여준다."""
    },
    "016_replication_factor.md": {
        "flow": """```text
[단일 스토리지 (Single Node) — 디스크 고장 시 데이터 완전 소실]
    │
    ▼
[RAID — 복수 디스크에 패리티 분산, 단일 시스템 내 내결함성]
    │
    ▼
[HDFS 복제 계수 3 (Replication Factor 3) — Rack-Aware 분산 복제, 노드·랙 이중 내결함성]
    │
    ▼
[이레이저 코딩 (Erasure Coding) — 패리티 수학으로 스토리지 낭비를 50% 이하로 절감]
    │
    ▼
[클라우드 객체 스토리지 (S3 / GCS) — 내부 투명 복제·이레이저 코딩 자동 적용, 99.999999999% 내구성]
```
이 흐름은 단일 디스크의 취약성을 해결하기 위해 3중 복제 방식이 등장하고, 스토리지 비효율을 개선한 이레이저 코딩을 거쳐 클라우드 객체 스토리지가 두 기법을 투명하게 내재화하는 분산 데이터 내구성 아키텍처의 발전을 보여준다."""
    },
    "016_dev_prod_parity.md": {
        "flow": """```text
[수동 환경 구성 — 개발자별 PC 설정 차이, 'Works on my machine' 문제]
    │
    ▼
[12-Factor App — 환경별 설정 외부화, 서비스 어태치먼트 표준화]
    │
    ▼
[Docker 컨테이너화 — 실행 환경 이미지 패키징, OS 수준 일치 보장]
    │
    ▼
[IaC (Infrastructure as Code) — Terraform/Ansible로 인프라 구성 코드화, 환경 편류 방지]
    │
    ▼
[CDE (Cloud Development Environments) — GitHub Codespaces 등, 클라우드 프로비저닝 즉시 프로덕션 동일 환경]
```
이 흐름은 개발자 로컬 환경과 프로덕션 간의 불일치를 단계적으로 제거하면서, 코드와 인프라 모두를 선언적으로 관리하고 클라우드 상의 개발 환경으로 수렴하는 DevOps Parity 달성의 진화 경로를 보여준다."""
    },
    "016_europe_data_strategy.md": {
        "flow": """```text
[개인정보 보호 규정 (GDPR) — EU 역내 데이터 처리 권리 및 역외 이전 통제 기준]
    │
    ▼
[유럽 데이터 전략 (European Data Strategy, 2020) — 데이터 단일 시장, 인간 중심 데이터 경제]
    │
    ▼
[Gaia-X — EU 연합 클라우드 인프라, 데이터 주권 기반 연동 생태계]
    │
    ▼
[데이터 스페이스 (Data Spaces) — 분야별(산업·의료·농업 등) 신뢰 데이터 공유 공간]
    │
    ▼
[데이터 거버넌스법 / 데이터법 (DGA / Data Act) — 공공·민간 데이터 접근 제도화, 데이터 중개자 규율]
```
이 흐름은 GDPR의 개인정보 보호 원칙을 기반으로 유럽이 데이터 주권과 산업 활용을 동시에 추구하는 데이터 단일 시장을 설계하고, Gaia-X·데이터 스페이스로 구체화하는 EU 데이터 거버넌스 전략의 발전 경로를 보여준다."""
    },
    "016_apache_pig.md": {
        "flow": """```text
[Raw MapReduce (Java) — 낮은 수준 API, 반복적 보일러플레이트 코드]
    │
    ▼
[Apache Pig (Pig Latin) — 데이터 흐름 스크립팅 언어, MapReduce 자동 변환]
    │
    ▼
[Apache Hive (HiveQL) — SQL 기반 배치 질의, 메타스토어 스키마 관리]
    │
    ▼
[Apache Spark (DataFrame / SQL) — 인메모리 처리로 Pig/Hive 대비 10~100배 가속]
    │
    ▼
[Apache Flink / Beam — 스트림·배치 통합 파이프라인, Pig 역할의 현대적 계승]
```
이 흐름은 저수준 MapReduce 코드를 단순화하기 위해 등장한 Pig Latin이 데이터 변환 파이프라인의 초기 표준이 되고, 이후 인메모리 처리와 스트림 통합 요건에 의해 Spark·Flink로 계승되는 하둡 생태계 데이터 처리 추상화의 발전을 보여준다."""
    },
    "016_spark_data_serialization.md": {
        "flow": """```text
[Java 기본 직렬화 (Java Serialization) — 느리고 무거운 리플렉션 기반, Spark 기본값]
    │
    ▼
[Kryo 직렬화 — 수동 등록 필요하나 Java 대비 10배 빠름, Spark 권장]
    │
    ▼
[Apache Avro — 스키마 진화 지원, Kafka 메시지 직렬화 표준]
    │
    ▼
[Apache Parquet — 컬럼 지향 파일 포맷, 스키마 내장·압축 최적화]
    │
    ▼
[Apache Arrow — 인메모리 컬럼 포맷, 직렬화 없는 Zero-copy 공유, Spark 4.x+ 내부 표준]
```
이 흐름은 Spark 내부 데이터 이동의 직렬화 오버헤드를 줄이기 위해 Java→Kryo→Avro/Parquet를 거쳐 직렬화 자체를 없애는 Zero-copy Arrow 포맷으로 수렴하는 분산 처리 직렬화 기술의 발전을 보여준다."""
    },
    "016_amazon_kinesis.md": {
        "flow": """```text
[배치 수집 (Batch Ingestion) — 주기적 ETL 파이프라인, 높은 지연]
    │
    ▼
[Amazon Kinesis Data Streams — 실시간 스트림 수집, 샤드 기반 병렬 처리]
    │
    ▼
[Kinesis Data Firehose — 무서버 스트림→S3/Redshift 자동 전달, 변환 내장]
    │
    ▼
[Kinesis Data Analytics (Apache Flink) — SQL·Flink로 스트림 실시간 분석]
    │
    ▼
[Lambda Architecture / Kappa Architecture — 배치+스트림 통합 또는 스트림 단일화 아키텍처]
```
이 흐름은 배치 처리의 높은 지연 한계를 극복하기 위해 Amazon Kinesis가 실시간 스트림 수집의 관리형 표준으로 자리잡고, 저장·분석 레이어와 결합하여 엔드투엔드 실시간 파이프라인 아키텍처로 진화하는 스트리밍 데이터 처리의 계보를 보여준다."""
    },
    "016_text_summarization.md": {
        "flow": """```text
[TF-IDF 기반 추출적 요약 — 단어 빈도·역문서 빈도로 핵심 문장 선택]
    │
    ▼
[그래프 기반 추출 (TextRank) — 문장 유사도 그래프에서 PageRank로 핵심 문장 도출]
    │
    ▼
[Seq2Seq 추상적 요약 — 인코더·디코더 LSTM으로 새로운 문장 생성]
    │
    ▼
[Transformer 기반 요약 (BART / T5 / PEGASUS) — 사전학습·파인튜닝으로 고품질 추상 요약]
    │
    ▼
[LLM 제로샷·프롬프트 요약 (GPT-4 / Claude) — 별도 학습 없이 지시문만으로 요약, RAG 통합]
```
이 흐름은 단어 빈도 통계 기반의 단순 추출에서 의미 이해 기반의 추상적 생성으로 진화하고, 대규모 언어 모델이 프롬프트 하나로 모든 요약 작업을 통합하는 텍스트 요약 기술의 발전 계보를 보여준다."""
    },
    "016_newsql.md": {
        "flow": """```text
[전통 RDBMS (MySQL/PostgreSQL) — ACID 보장, 수직 확장 한계]
    │
    ▼
[NoSQL (Cassandra / MongoDB) — 수평 확장·고가용성, 일관성 타협(BASE)]
    │
    ▼
[NewSQL (CockroachDB / TiDB / YugabyteDB) — ACID + 수평 확장, SQL 인터페이스 유지]
    │
    ▼
[분산 트랜잭션 프로토콜 (Raft / Paxos + 2PC) — 분산 환경에서도 직렬화 일관성 보장]
    │
    ▼
[HTAP (Hybrid Transactional/Analytical Processing) — 트랜잭션·분석을 단일 엔진에서 처리]
```
이 흐름은 RDBMS와 NoSQL의 양립 불가능해 보이던 확장성-일관성 트레이드오프를 NewSQL이 분산 합의 알고리즘으로 해소하고, 나아가 HTAP으로 트랜잭션과 분석을 통합하는 데이터베이스 패러다임의 진화를 보여준다."""
    },
    "016_databricks_platform.md": {
        "flow": """```text
[Apache Spark — 인메모리 분산 처리 엔진, 배치·스트림 통합]
    │
    ▼
[Databricks (Managed Spark) — Spark 완전 관리형 클라우드 플랫폼, 자동 최적화]
    │
    ▼
[Delta Lake — ACID 트랜잭션·스키마 진화·타임 트래블 지원 오픈 테이블 포맷]
    │
    ▼
[레이크하우스 (Lakehouse) — 데이터 레이크의 유연성 + 데이터 웨어하우스의 ACID·성능 통합]
    │
    ▼
[Unity Catalog + MLflow — 데이터·모델 거버넌스 통합, 엔드투엔드 AI/ML 파이프라인]
```
이 흐름은 순수 Spark 엔진이 데이터 품질 보장의 한계를 드러내자 Delta Lake의 ACID가 이를 보완하고, 레이크하우스 아키텍처와 통합 거버넌스로 발전하는 Databricks 플랫폼의 진화 계보를 보여준다."""
    },
    "016_management.md": {
        "flow": """```text
[온프레미스 단독 운영 — 고정 자원, 피크 트래픽 대응 불가]
    │
    ▼
[클라우드 단독 이전 — 유연한 확장, 데이터 주권·규제 한계]
    │
    ▼
[하이브리드 클라우드 (Hybrid Cloud) — 온프레미스+클라우드 연계, 규제 데이터 내부 유지]
    │
    ▼
[클라우드 버스팅 (Cloud Bursting) — 피크 시 온프레미스 초과 부하를 클라우드로 자동 확장]
    │
    ▼
[멀티클라우드 통합 분석 — 여러 클라우드·온프레미스 데이터를 단일 분석 플랫폼에서 통합 처리]
```
이 흐름은 고정 자원의 한계를 가진 온프레미스 시스템이 클라우드의 탄력성과 결합하여 하이브리드 분석 아키텍처로 발전하고, 피크 부하를 클라우드로 자동 확장하는 버스팅 전략을 통해 비용과 성능을 동시에 최적화하는 진화 경로를 보여준다."""
    },
    "016_pipa_bigdata_exception.md": {
        "flow": """```text
[개인정보 원칙 (PIPA / GDPR) — 정보주체 동의 기반, 목적 외 활용 금지]
    │
    ▼
[데이터 3법 개정 (2020) — 가명정보 개념 신설, 연구·통계·공익 목적 활용 허용]
    │
    ▼
[가명 처리 (Pseudonymization) — 식별자 제거·치환 후 추가 정보 없이 재식별 불가]
    │
    ▼
[결합 전문기관 — 국가 지정 기관을 통한 안전한 가명 데이터 결합·분석]
    │
    ▼
[차분 프라이버시 / 합성 데이터 — 수학적 프라이버시 보장 강화, 차세대 빅데이터 특례 기술]
```
이 흐름은 원칙적으로 동의 없는 데이터 활용을 금지하던 규제 체계가 빅데이터·AI 시대의 공익적 활용 요건을 수용하여 가명정보 특례를 도입하고, 기술적 보호 수준을 차분 프라이버시로 강화하는 데이터 법제와 기술의 공진화를 보여준다."""
    },
    "016_audit.md": {
        "flow": """```text
[전통 정보 분석 — 수작업 보고서, 제한된 데이터 소스, 높은 지연]
    │
    ▼
[빅데이터 수집 통합 — 다중 센서·로그·통신 데이터 실시간 수집 및 정제]
    │
    ▼
[AI 패턴 탐지 — 기계학습 기반 적 행동 예측·이상 징후 자동 탐지]
    │
    ▼
[사이버-물리 융합 감시 — IT 보안 위협과 물리 침입 징후 통합 분석]
    │
    ▼
[의사결정 지원 시스템 (C4I) — 지휘·통제·통신·컴퓨터·정보의 빅데이터 기반 실시간 통합]
```
이 흐름은 분야별 분절된 수집·분석을 통합하는 국방 빅데이터가 AI 예측 분석과 결합하고, 사이버·물리 위협을 통합 감시하는 지능형 C4I 체계로 발전하는 국방 정보 분석의 디지털 전환 경로를 보여준다."""
    },
}

# Additional entries for files needing full map+flow+child sections
SELECTION_SORT_TAIL = """
### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **버블 정렬 (Bubble Sort)** | 인접 교환 방식의 O(N²) 안정 정렬, 선택 정렬의 비교 대상 |
| **삽입 정렬 (Insertion Sort)** | 거의 정렬된 데이터에서 O(N)에 수렴하는 O(N²) 안정 정렬 |
| **힙 정렬 (Heap Sort)** | 선택 정렬의 "최솟값 반복 탐색" 아이디어를 힙으로 O(N log N)에 구현한 발전형 |
| **안정 정렬 (Stable Sort)** | 동일 키 사이의 원래 순서를 보존하는 정렬 특성, 선택 정렬이 결여하는 속성 |
| **제자리 정렬 (In-place Sort)** | 추가 메모리 O(1)만 사용하는 정렬, 선택 정렬의 장점 중 하나 |

### 📈 관련 키워드 및 발전 흐름도

```text
[버블 정렬 — 인접 교환 O(N²), 안정, 비효율적]
    │
    ▼
[선택 정렬 — 최솟값 탐색 후 교환 O(N²), 불안정, 최소 교환 횟수]
    │
    ▼
[삽입 정렬 — 거의 정렬 시 O(N), O(N²) 평균, 안정]
    │
    ▼
[힙 정렬 (Heap Sort) — 선택 정렬 아이디어를 힙으로 최적화 O(N log N), 불안정]
    │
    ▼
[퀵 정렬 / 병합 정렬 — 분할 정복 O(N log N), 실용 최고 성능]
```
이 흐름은 단순하지만 교환 횟수가 최소인 선택 정렬의 "최솟값 반복 탐색" 핵심 아이디어가 힙 자료구조를 통해 O(N log N) 힙 정렬로 계승되는 O(N²) 정렬 군의 발전과 그 이론적 의의를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 선택 정렬은 학생들이 줄을 설 때, 전체 줄에서 키가 가장 작은 친구를 찾아 맨 앞에 세우는 작업을 반복하는 거예요.
2. 매번 줄 전체를 눈으로 훑어봐야 하니 사람이 많아질수록 엄청 오래 걸리지만, 자리를 바꾸는 횟수는 딱 N-1번밖에 안 돼서 자리 이동이 힘든 상황에서는 유리해요.
3. 이 "가장 작은 것 반복 선택" 아이디어가 나중에 훨씬 빠른 힙 정렬의 할아버지 개념이 된답니다!
"""

DATA_PRIVACY_TAIL = """

### 📌 관련 개념 맵 (Knowledge Graph)

| 개념 | 연결 포인트 |
|:---|:---|
| **GDPR (General Data Protection Regulation)** | 유럽의 개인정보 보호 최상위 규정, 역외 이전 통제 및 정보 주체 권리 체계화 |
| **가명 정보 (Pseudonymization)** | 식별자를 제거·대체하여 추가 정보 없이 재식별 불가한 상태, 데이터 3법 활용 허용 |
| **DLP (Data Loss Prevention)** | 민감 정보의 외부 반출을 패턴 매칭·ML로 탐지하고 차단하는 데이터 유출 방지 솔루션 |
| **토큰화 (Tokenization)** | 원본 데이터를 Vault에 격리하고 역산 불가한 토큰을 시스템에 유통하는 민감 정보 대체 기법 |
| **PET (Privacy Enhancing Technologies)** | 동형 암호·차분 프라이버시 등 데이터를 복호화하지 않고 분석·학습을 가능하게 하는 차세대 프라이버시 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
[경계 보안 (Perimeter Security) — 방화벽 기반 외부 차단, 내부 평문 무방비]
    │
    ▼
[데이터 암호화 (TDE / 전송 암호화) — 저장·전송 중 데이터 보호, 처리 시 복호화 필요]
    │
    ▼
[비식별화 (k-익명성 / l-다양성) — 통계적 재식별 방지, 분석 목적 가명 정보 생성]
    │
    ▼
[토큰화 / DLP — 원본 데이터 격리 및 반출 차단, 컴플라이언스 아키텍처 표준화]
    │
    ▼
[PET (동형 암호 / 차분 프라이버시) — 암호화 상태 그대로 연산, AI 학습 시 개인 정보 수학적 보호]
```
이 흐름은 외부 경계만 지키던 초기 보안 관점에서 데이터 자체를 보호하는 방향으로 진화하고, AI 시대의 대규모 학습 요건에 맞춰 복호화 없이 분석이 가능한 차세대 프라이버시 강화 기술로 수렴하는 데이터 보호 패러다임의 발전을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 개인정보 보호는 소중한 일기장을 지키는 것처럼, 내 정보가 수집·저장·분석·공유되는 모든 순간에 함부로 남이 볼 수 없도록 여러 자물쇠를 채우는 거예요.
2. 이름·주민번호 같은 직접 알아볼 수 있는 부분은 지우거나 바꾸고(가명 처리), 진짜 정보는 금고(Vault)에 넣고 가짜 번호표(토큰)만 사용해서 혹시 누군가 훔쳐가도 아무 소용이 없게 만들어요.
3. 최신 기술로는 일기장을 암호 상자에 넣은 채로 내용을 분석할 수 있어서, 암호를 풀지 않아도 "이 아이가 행복한지 슬픈지" 통계를 낼 수 있는 마법 같은 수학이 생겨났답니다!
"""

def insert_flow_between_map_and_child(filepath, flow_content):
    """Insert flow section between 📌 map section and 👶 child section."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the 👶 marker
    child_pattern = r'(### 👶 어린이를 위한 3줄 비유 설명)'
    match = re.search(child_pattern, content)
    if not match:
        print(f"  WARNING: No 👶 section found in {filepath}")
        return False
    
    insert_pos = match.start()
    
    flow_section = f"\n### 📈 관련 키워드 및 발전 흐름도\n\n{flow_content}\n\n"
    
    new_content = content[:insert_pos] + flow_section + content[insert_pos:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ Inserted flow section into {filepath}")
    return True

def append_full_tail(filepath, tail_content):
    """Append full tail (map+flow+child) to file, before ## 참고 if exists."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    ref_pattern = r'(^## 참고)'
    match = re.search(ref_pattern, content, re.MULTILINE)
    
    if match:
        insert_pos = match.start()
        new_content = content[:insert_pos] + tail_content + "\n" + content[insert_pos:]
    else:
        new_content = content.rstrip() + "\n" + tail_content
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ Appended full tail to {filepath}")
    return True

import os

BASE = "/workspaces/brainscience/content/studynote"
FILES = {
    "016_fet.md": f"{BASE}/01_computer_architecture/01_basic_electronics_logic/016_fet.md",
    "016_interrupt_mechanism.md": f"{BASE}/02_operating_system/01_overview_architecture/016_interrupt_mechanism.md",
    "016_전파_지연.md": f"{BASE}/03_network/01_data_communication/016_전파_지연.md",
    "016_cmmi_5_levels.md": f"{BASE}/04_software_engineering/01_overview_principles/016_cmmi_5_levels.md",
    "016_network_data_model.md": f"{BASE}/05_database/01_db_architecture_relational/016_network_data_model.md",
    "016_dpos_delegated_pos.md": f"{BASE}/06_ict_convergence/01_blockchain/016_dpos_delegated_pos.md",
    "016_bpr.md": f"{BASE}/07_enterprise_systems/01_strategy_governance/016_bpr.md",
    "016_sort_comparison.md": f"{BASE}/08_algorithm_stats/02_sorting/016_sort_comparison.md",
    "016_max_flow.md": f"{BASE}/08_algorithm_stats/03_graph_search/016_max_flow.md",
    "016_open_addressing.md": f"{BASE}/08_algorithm_stats/04_datastructure/016_open_addressing.md",
    "016_hypothesis_testing.md": f"{BASE}/08_algorithm_stats/08_stats/016_hypothesis_testing.md",
    "016_hill_climbing.md": f"{BASE}/10_ai/01_ai_basics/016_hill_climbing.md",
    "016_kick_off_meeting.md": f"{BASE}/11_design_supervision/01_audit_framework/016_kick_off_meeting.md",
    "016_tco.md": f"{BASE}/12_it_management/01_governance_strategy/016_tco.md",
    "016_hypervisor.md": f"{BASE}/13_cloud_architecture/01_virtualization/016_hypervisor.md",
    "016_replication_factor.md": f"{BASE}/14_data_engineering/01_infrastructure/016_replication_factor.md",
    "016_dev_prod_parity.md": f"{BASE}/15_devops_sre/01_culture_methodology/016_dev_prod_parity.md",
    "016_europe_data_strategy.md": f"{BASE}/16_bigdata/01_intro/016_europe_data_strategy.md",
    "016_apache_pig.md": f"{BASE}/16_bigdata/02_hadoop/016_apache_pig.md",
    "016_spark_data_serialization.md": f"{BASE}/16_bigdata/03_spark/016_spark_data_serialization.md",
    "016_amazon_kinesis.md": f"{BASE}/16_bigdata/04_streaming/016_amazon_kinesis.md",
    "016_text_summarization.md": f"{BASE}/16_bigdata/05_analysis/016_text_summarization.md",
    "016_newsql.md": f"{BASE}/16_bigdata/06_nosql/016_newsql.md",
    "016_databricks_platform.md": f"{BASE}/16_bigdata/07_data_lake/016_databricks_platform.md",
    "016_management.md": f"{BASE}/16_bigdata/09_platform/016_management.md",
    "016_pipa_bigdata_exception.md": f"{BASE}/16_bigdata/10_governance/016_pipa_bigdata_exception.md",
    "016_audit.md": f"{BASE}/16_bigdata/11_industry/016_audit.md",
    # Special: need full tail
    "016_selection_sort.md": f"{BASE}/08_algorithm_stats/02_sorting/016_selection_sort.md",
    "016_data_privacy.md": f"{BASE}/09_security/01_intro_principles/016_data_privacy.md",
}

# Process files needing flow section inserted between map and child
needs_insert = [k for k in FLOWS.keys()]
print("Processing files that need flow section inserted...")
for fname in needs_insert:
    fpath = FILES[fname]
    if not os.path.exists(fpath):
        print(f"  NOT FOUND: {fpath}")
        continue
    insert_flow_between_map_and_child(fpath, FLOWS[fname]["flow"])

# Process files needing full tail appended
print("\nProcessing files that need full tail added...")
append_full_tail(FILES["016_selection_sort.md"], SELECTION_SORT_TAIL)
append_full_tail(FILES["016_data_privacy.md"], DATA_PRIVACY_TAIL)

print("\nDone!")
