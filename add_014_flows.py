import re

FLOW_SECTIONS = {
    "014_transistor.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[반도체 (Semiconductor) — P형/N형 도핑으로 전기 전도성 조절]
    │
    ▼
[BJT (Bipolar Junction Transistor) — 전류 기반 증폭/스위칭]
    │
    ▼
[MOSFET (Metal-Oxide-Semiconductor FET) — 전압 기반 고집적 디지털 스위치]
    │
    ▼
[FinFET — 3차원 핀 구조로 누설 전류 억제, 10nm 이하 공정]
    │
    ▼
[GAA (Gate-All-Around) — 4면 게이트로 채널 완전 통제, 3nm 이하 차세대]
```

이 흐름은 트랜지스터가 단순한 전류 증폭 소자(BJT)에서 디지털 스위치(MOSFET)로 진화하고, 채널 축소에 따른 누설 전류 문제를 극복하기 위해 2D 평면에서 3D 입체 구조(FinFET→GAA)로 발전하는 반도체 공정 혁신의 핵심 계보를 보여준다.

""",
    "014_api_posix.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[시스템 호출 (System Call) — 커널 기능을 사용자 공간에 노출]
    │
    ▼
[POSIX (Portable Operating System Interface) — 유닉스 계열 표준 API 규격]
    │
    ▼
[표준 C 라이브러리 (libc) — POSIX 래핑, 언어 수준 이식성 보장]
    │
    ▼
[컨테이너 런타임 (Container Runtime) — POSIX 네임스페이스·cgroups 추상화]
    │
    ▼
[클라우드 네이티브 API (REST/gRPC) — 플랫폼 독립 분산 인터페이스로 진화]
```

이 흐름은 OS 커널 기능을 직접 호출하던 시스템 호출에서 POSIX 표준으로 이식성이 확보되고, 컨테이너·클라우드 환경에서 플랫폼 독립 API 계층으로 지속 추상화되는 인터페이스 표준화의 발전 과정을 보여준다.

""",
    "014_처리량_굿풋.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[대역폭 (Bandwidth) — 링크의 최대 물리적 전송 용량 (bps)]
    │
    ▼
[처리량 (Throughput) — 단위 시간당 실제 전달된 총 비트 수]
    │
    ▼
[굿풋 (Goodput) — 오버헤드 제거 후 순수 유효 페이로드 처리량]
    │
    ▼
[TCP 혼잡 제어 (Congestion Control) — AIMD로 처리량과 공정성 균형]
    │
    ▼
[QUIC / HTTP/3 — UDP 기반 멀티플렉싱으로 굿풋 극대화]
```

이 흐름은 물리 링크의 최대 용량(대역폭)에서 실제 활용 효율(처리량·굿풋)로 초점이 이동하고, TCP 혼잡 제어 한계를 극복하기 위해 QUIC/HTTP/3로 진화하는 네트워크 성능 최적화 계보를 보여준다.

""",
    "014_iso_iec_15504_spice.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[소프트웨어 개발 프로세스 — 체계 없는 임시방편 관행의 품질 한계]
    │
    ▼
[ISO/IEC 15504 SPICE — 프로세스 능력 수준 1~5단계 평가 체계]
    │
    ▼
[CMMI (Capability Maturity Model Integration) — 조직 전반 프로세스 성숙도]
    │
    ▼
[ISO/IEC 33000 시리즈 — SPICE 기반 최신 프로세스 평가 국제표준]
    │
    ▼
[자동화 프로세스 심사 (AI-assisted Assessment) — 측정 데이터 기반 연속 개선]
```

이 흐름은 비체계적 개발 관행에서 SPICE의 정량적 능력 수준 평가로 진화하고, CMMI·ISO 33000으로 국제 표준화되며 AI 기반 연속 측정까지 발전하는 소프트웨어 프로세스 성숙도 개선의 계보를 보여준다.

""",
    "014_data_model_components.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 모델 3요소 — 구조(Structure), 연산(Operation), 제약(Constraint)]
    │
    ▼
[개념적 데이터 모델 (E-R 다이어그램) — 엔티티·속성·관계 개념적 표현]
    │
    ▼
[논리적 데이터 모델 (관계형 모델) — 테이블·키·정규화·SQL 규칙 정의]
    │
    ▼
[물리적 데이터 모델 — 인덱스·파티션·스토리지 엔진 매핑]
    │
    ▼
[NoSQL / 다중 모델 DB — 유연한 구조로 비정형 데이터 제약 완화]
```

이 흐름은 데이터 모델의 추상 3요소에서 출발해 개념·논리·물리 설계 단계로 구체화되고, 비정형 데이터 요구에 따라 NoSQL로 모델 제약이 완화되는 데이터 설계 발전 과정을 보여준다.

""",
    "014_pow_proof_of_work.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[합의 알고리즘 필요성 — 신뢰기관 없이 분산 원장 무결성 보장]
    │
    ▼
[PoW (Proof of Work) — 해시 퍼즐 반복으로 채굴권·블록 추가 권한 획득]
    │
    ▼
[PoS (Proof of Stake) — 지분 기반 검증자 선택, 에너지 소비 90% 절감]
    │
    ▼
[DPoS / BFT 변형 — 위임 투표·BFT 기반 고성능 기업형 합의]
    │
    ▼
[레이어2 합의 (Layer-2 Consensus) — 롤업·사이드체인으로 확장성 해결]
```

이 흐름은 PoW의 에너지 낭비 한계를 극복하기 위해 PoS·DPoS로 합의 패러다임이 전환되고, 레이어2 기술로 확장성까지 달성하는 블록체인 합의 알고리즘 진화의 핵심 계보를 보여준다.

""",
    "014_gea_framework.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[EA (Enterprise Architecture) — 비즈니스·IT 정렬 체계적 설계 방법론]
    │
    ▼
[GEA (Government EA Framework) — 범정부 공통 아키텍처·표준 참조 모델]
    │
    ▼
[TOGAF (The Open Group Architecture Framework) — 글로벌 EA 방법론 표준]
    │
    ▼
[디지털 정부 플랫폼 — GEA 기반 공공 서비스 표준화·재사용 실현]
    │
    ▼
[클라우드 퍼스트 (Cloud-First) 정책 — EA와 클라우드 전환 로드맵 통합]
```

이 흐름은 기업 아키텍처 방법론(EA)이 공공 부문에 특화된 GEA로 발전하고, TOGAF 표준과 융합하여 디지털 정부 플랫폼 구축과 클라우드 전환 전략의 기반으로 자리잡는 과정을 보여준다.

""",
    "014_recursion.md": """
### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **콜 스택 (Call Stack)** | 재귀 호출 시 프레임이 쌓이며 O(N) 공간 소비, 스택 오버플로우의 근원 |
| **꼬리 재귀 최적화 (TCO)** | 마지막 연산이 재귀 호출일 때 스택 프레임을 재사용해 O(1) 공간 달성 |
| **분할 정복 (Divide and Conquer)** | 재귀로 문제를 절반씩 쪼개어 퀵·머지소트·이진 탐색 등을 구현하는 핵심 패러다임 |
| **메모이제이션 (Memoization)** | 재귀 결과를 캐싱해 중복 계산을 제거, 동적 프로그래밍(DP)의 탑다운 구현 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
[재귀 기본 구조 — 기본 사례(Base Case) + 재귀 사례(Recursive Case)]
    │
    ▼
[콜 스택 (Call Stack) — 재귀 호출 시 LIFO 방식으로 프레임 Push/Pop]
    │
    ▼
[꼬리 재귀 최적화 (TCO, Tail Call Optimization) — O(N) 스택 → O(1) 공간]
    │
    ▼
[분할 정복 (Divide and Conquer) — 재귀로 구현하는 퀵·머지소트 핵심 패러다임]
    │
    ▼
[동적 프로그래밍 (DP) — 재귀 + 메모이제이션으로 중복 계산 완전 제거]
```

이 흐름은 재귀의 기본 구조에서 콜 스택 문제가 발생하고, TCO로 공간 효율을 달성한 뒤 분할 정복과 DP라는 고급 알고리즘 패러다임으로 확장되는 재귀 사고의 성장 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 재귀는 거울을 두 개 마주 세워두면 내 모습이 점점 작아지며 끝없이 반복되는 것과 같아요.
2. 하지만 거울을 꽉 붙여서 가장 작은 모습이 나오는 순간 딱 멈추는 규칙(기본 사례)이 있어야 무한 반복을 막을 수 있어요.
3. 복잡한 탑을 쌓는 문제도 "가장 작은 블록 1개"부터 시작해서 차곡차곡 거꾸로 쌓아 올리는 것이 바로 재귀의 마법이에요.

""",
    "014_stability.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[정렬 안정성 (Sort Stability) — 동일 키를 가진 요소의 원본 순서 보존]
    │
    ▼
[안정 정렬 — 버블·삽입·병합 정렬 (Stable Sort), 원본 순서 유지 보장]
    │
    ▼
[불안정 정렬 — 퀵·힙·선택 정렬 (Unstable Sort), 원본 순서 미보장]
    │
    ▼
[다중 키 정렬 — 우선순위 낮은 키 먼저 안정 정렬로 복합 키 정렬 구현]
    │
    ▼
[Tim Sort — 안정 정렬 + 실세계 데이터 최적화, Python·Java 기본 정렬]
```

이 흐름은 안정성의 개념에서 안정/불안정 정렬의 트레이드오프를 거쳐, 다중 키 정렬 실무 응용과 최신 Tim Sort로 이어지는 정렬 안정성의 실용적 발전 과정을 보여준다.

""",
    "014_kruskal.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[최소 신장 트리 (MST, Minimum Spanning Tree) — 모든 노드 연결 최소 비용]
    │
    ▼
[크루스칼 (Kruskal) — 간선 오름차순 정렬 + Union-Find 사이클 방지]
    │
    ▼
[프림 (Prim) — 시작 노드에서 최소 비용 간선 탐욕적 선택, 밀집 그래프 유리]
    │
    ▼
[Union-Find (Disjoint Set) — 경로 압축·랭크로 O(α(N)) 연결성 판단]
    │
    ▼
[네트워크 토폴로지 최적화 — MST 기반 물리 네트워크·클러스터 배선 설계]
```

이 흐름은 MST 문제 정의에서 크루스칼과 프림이라는 두 탐욕 알고리즘으로 분기하고, Union-Find 자료구조로 효율화된 뒤 네트워크 설계·클러스터 구성 등 실무 토폴로지 최적화로 응용되는 과정을 보여준다.

""",
    "014_trie.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[해시맵 (HashMap) — 완전 문자열 키 매칭, 접두사 검색 미지원]
    │
    ▼
[이진 탐색 트리 (BST) — 문자열 사전 순서 탐색, 접두사 탐색 비효율]
    │
    ▼
[트라이 (Trie) — 공유 접두사 경로로 O(L) 삽입·검색, 자동완성 최적화]
    │
    ▼
[압축 트라이 (Radix/Patricia Tree) — 단일 자식 노드 병합으로 공간 최적화]
    │
    ▼
[Aho-Corasick — 트라이 + 실패 링크(Failure Link)로 다중 패턴 O(N+M) 검색]
```

이 흐름은 완전 키 매칭 해시맵의 접두사 검색 한계에서 트라이가 탄생하고, 공간 효율을 위한 압축 트라이와 다중 패턴 검색을 위한 Aho-Corasick으로 발전하는 문자열 탐색 자료구조의 진화 계보를 보여준다.

""",
    "014_quantum_complexity.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[고전 복잡도 이론 (P, NP) — 다항 시간 결정론적·비결정론적 계산 한계]
    │
    ▼
[BQP (Bounded-error Quantum Polynomial-time) — 양자 다항 시간 해결 가능 문제류]
    │
    ▼
[양자 우위 (Quantum Supremacy) — 특정 문제에서 고전 컴퓨터를 완전히 압도]
    │
    ▼
[쇼어 알고리즘 (Shor's Algorithm) — RSA 인수분해를 지수→다항 시간으로 돌파]
    │
    ▼
[양자 오류 정정 (QEC) — 큐비트 결어긋남 극복, 실용 양자 컴퓨터 조건]
```

이 흐름은 고전 복잡도 이론의 P/NP 한계에서 양자 복잡도 클래스 BQP가 등장하고, 양자 우위와 쇼어 알고리즘이 실용성을 증명하며 오류 정정 기술로 실용화를 향해 나아가는 양자 컴퓨팅 발전의 핵심 계보를 보여준다.

""",
    "014_mle.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[우도 함수 (Likelihood Function) — 데이터가 주어졌을 때 파라미터 타당성 측정]
    │
    ▼
[MLE (Maximum Likelihood Estimation) — log L(θ) 최대화, 가장 그럴듯한 파라미터 추정]
    │
    ▼
[MAP (Maximum A Posteriori) — MLE + 사전 분포(Prior) = 베이즈 정규화 추정]
    │
    ▼
[EM 알고리즘 (Expectation-Maximization) — 잠재 변수 포함 모델의 반복 MLE]
    │
    ▼
[딥러닝 손실함수 (Cross-Entropy) — NLL 최소화가 MLE 최대화와 수학적 동치]
```

이 흐름은 우도 함수 정의에서 MLE로 파라미터를 추정하고, 베이즈 사전 분포를 더한 MAP과 잠재 변수 모델의 EM 알고리즘으로 확장되며, 딥러닝의 크로스 엔트로피 손실이 MLE의 현대적 구현임을 보여주는 통계 추정 이론의 계보다.

""",
    "014_simplicity.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[보안 원칙 (Security Principles) — 최소 권한·심층 방어·분리 원칙 체계화]
    │
    ▼
[단순성 원칙 (Simplicity) — 불필요한 복잡성 제거로 공격 표면 최소화]
    │
    ▼
[제로 트러스트 (Zero Trust) — 복잡한 경계 보안 대신 ID 기반 단순 신뢰 모델]
    │
    ▼
[보안 설계 검토 (Security Design Review) — 단순성 기반 공격 표면 분석]
    │
    ▼
[DevSecOps — 코드 복잡도 측정 자동화, CI/CD 파이프라인 보안 내재화]
```

이 흐름은 단순성이 보안 원칙의 핵심 전제로 작동하며, 제로 트러스트 아키텍처로 구체화되고 DevSecOps 파이프라인에서 자동 측정·강제되는 현대 보안 설계의 발전 계보를 보여준다.

""",
    "014_uninformed_search.md": """
### 📌 관련 개념 맵 (Knowledge Graph)

| 개념 | 연결 포인트 |
|:---|:---|
| **BFS (Breadth-First Search)** | 큐(Queue) 기반 층별 탐색, 최단 경로 보장, 공간 복잡도 O(b^d) |
| **DFS (Depth-First Search)** | 스택(Stack) 기반 깊이 우선, 메모리 효율 O(b×m), 완전성 미보장 |
| **IDS (Iterative Deepening Search)** | DFS 깊이 제한 반복 확장, BFS 최적성 + DFS 메모리 효율 하이브리드 |
| **휴리스틱 탐색 (Informed Search)** | 맹목적 탐색의 한계를 극복하기 위해 도메인 지식(h(n))을 활용하는 A* 등 |

### 📈 관련 키워드 및 발전 흐름도

```text
[상태 공간 (State Space) — 초기 상태에서 목표까지 모든 가능 상태 집합]
    │
    ▼
[BFS (Breadth-First Search) — 큐 기반 층별 탐색, 최단 거리 보장]
    │
    ▼
[DFS (Depth-First Search) — 스택 기반 깊이 우선 탐색, 메모리 효율]
    │
    ▼
[IDS (Iterative Deepening Search) — DFS 깊이 제한 반복, BFS+DFS 장점 결합]
    │
    ▼
[A* 알고리즘 (Informed Search) — 휴리스틱 함수로 맹목적 탐색의 한계 초월]
```

이 흐름은 상태 공간 문제를 도메인 지식 없이 탐색하는 BFS·DFS에서 출발해, 두 방법의 장점을 결합한 IDS로 발전하고, 최종적으로 휴리스틱 기반 A* 알고리즘으로 진화하는 탐색 알고리즘의 핵심 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 맹목적 탐색은 지도 없이 미로를 찾는 것처럼, 어디에 출구가 있는지 모르고 모든 길을 하나씩 차례로 걸어보는 방법이에요.
2. BFS는 내 바로 앞 길부터 차근차근 살피는 것이고, DFS는 한 방향으로 끝까지 달려보고 막히면 돌아오는 방식이에요.
3. 이 두 방법은 복잡한 AI가 없어도 반드시 답을 찾을 수 있는 가장 믿음직한 탐색법이랍니다.

""",
    "014_audit_planning.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[감리 요청 — 발주자·감리 의뢰, 감리 범위·목적 정의]
    │
    ▼
[예비조사 (Preliminary Survey) — 개발 계획·산출물·리스크 사전 파악]
    │
    ▼
[감리 계획 수립 (Audit Planning) — 일정·인력·방법론·점검 항목 확정]
    │
    ▼
[감리 수행 — 인터뷰·문서 검토·테스트·현장 확인]
    │
    ▼
[감리 보고서 — 결함·개선 권고·사후 조치 계획 작성 및 제출]
```

이 흐름은 감리 요청에서 출발해 예비조사로 리스크를 파악하고, 계획 수립→수행→보고서 제출로 이어지는 IT 감리 생애 주기의 전 과정을 보여주며, 계획 수립이 성공적 감리의 품질 기반임을 강조한다.

""",
    "014_irr.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[현금 흐름 분석 (Cash Flow Analysis) — 투자 기간 비용·편익 시계열 산출]
    │
    ▼
[NPV (Net Present Value) — 할인율 적용 순현재가치, 투자 절대적 타당성]
    │
    ▼
[IRR (Internal Rate of Return) — NPV=0으로 만드는 내부수익률 계산]
    │
    ▼
[WACC (자본 비용) 비교 — IRR > WACC이면 투자 채택, 미만이면 기각]
    │
    ▼
[투자 포트폴리오 최적화 — IRR·NPV 복합 분석으로 다중 프로젝트 우선순위]
```

이 흐름은 현금 흐름 분석에서 NPV·IRR 산출로 이어지고, 자본 비용(WACC)과 비교해 투자 의사결정을 내린 뒤 포트폴리오 전체의 우선순위를 최적화하는 IT 투자 경제성 분석의 전체 흐름을 보여준다.

""",
    "014_multi_tenancy.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[SaaS (Software as a Service) — 여러 고객에게 동일 서비스 제공 필요성]
    │
    ▼
[멀티 테넌시 (Multi-Tenancy) — 단일 인스턴스로 복수 고객 논리적 격리]
    │
    ▼
[테넌트 격리 전략 — DB 분리/스키마 분리/행 수준 격리 트레이드오프]
    │
    ▼
[RBAC / ABAC — 테넌트별 권한 제어 및 데이터 접근 정책 관리]
    │
    ▼
[쿠버네티스 멀티 테넌시 — 네임스페이스·NetworkPolicy·OPA로 클러스터 공유]
```

이 흐름은 SaaS의 비용 효율 필요성에서 멀티 테넌시 아키텍처로 발전하고, 격리 수준 전략·권한 관리를 거쳐 쿠버네티스 기반 인프라 수준까지 확장되는 클라우드 테넌트 관리 기술의 핵심 계보를 보여준다.

""",
    "014_namenode.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[HDFS (Hadoop Distributed File System) — 블록 분산 저장·복제 파일 시스템]
    │
    ▼
[네임노드 (NameNode) — 파일 메타데이터·블록 매핑 중앙 관리 마스터]
    │
    ▼
[데이터노드 (DataNode) — 실제 블록 저장·체크섬 검증·하트비트 전송]
    │
    ▼
[HDFS HA (High Availability) — 액티브/스탠바이 NameNode 이중화, SPOF 제거]
    │
    ▼
[오브젝트 스토리지 (Object Storage) — S3 호환, NameNode 없는 무한 확장 대안]
```

이 흐름은 HDFS의 마스터-슬레이브 구조에서 NameNode의 단일 장애점(SPOF) 문제를 HA 이중화로 해결하고, 궁극적으로 NameNode 없는 오브젝트 스토리지가 새로운 빅데이터 스토리지 표준으로 부상하는 발전 과정을 보여준다.

""",
    "014_concurrency.md": """
### 📌 관련 개념 맵 (Knowledge Graph)

| 개념 | 연결 포인트 |
|:---|:---|
| **12팩터 앱 (Twelve-Factor App)** | 클라우드 네이티브 애플리케이션 설계 원칙 12가지 중 제8원칙이 동시성 |
| **프로세스 매니저 (Process Manager)** | systemd / Procfile 기반으로 프로세스 타입·수량을 선언적으로 관리 |
| **수평 확장 (Scale-Out)** | 프로세스 인스턴스를 복제해 처리량을 선형적으로 늘리는 확장 전략 |
| **서버리스 (Serverless / FaaS)** | 함수 단위 자동 병렬 확장, 동시성 원칙의 궁극적 진화 형태 |

### 📈 관련 키워드 및 발전 흐름도

```text
[12팩터 앱 (Twelve-Factor App) — 클라우드 네이티브 애플리케이션 설계 원칙]
    │
    ▼
[동시성 원칙 (Concurrency, 제8원칙) — 프로세스 타입 분리·수평 복제 확장]
    │
    ▼
[프로세스 매니저 (Process Manager) — systemd/Procfile 기반 수명 관리]
    │
    ▼
[컨테이너 오케스트레이션 (Kubernetes) — Pod 복제·HPA로 동시성 자동 확장]
    │
    ▼
[서버리스 (Serverless / FaaS) — 함수 단위 무한 병렬 확장, 동시성 극한 구현]
```

이 흐름은 12팩터 앱의 동시성 원칙에서 출발해 프로세스 매니저로 수명을 관리하고, 쿠버네티스 오케스트레이션을 거쳐 서버리스의 무한 자동 확장으로 진화하는 클라우드 네이티브 확장성 아키텍처의 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 동시성은 한 명의 직원이 모든 일을 혼자 처리하는 대신, 같은 일을 하는 직원을 여러 명 고용해서 동시에 일하게 하는 것과 같아요.
2. 손님이 많아지면 직원을 더 뽑고, 손님이 줄어들면 퇴근시키면 되니까 언제나 딱 맞게 일할 수 있어요.
3. 서버리스는 직원을 아예 두지 않고 일이 생길 때만 순식간에 로봇을 불러서 처리하는 최첨단 방법이에요.

""",
    "014_data_voucher.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 격차 (Data Divide) — 중소기업의 데이터 구매·활용 역량 부재]
    │
    ▼
[데이터바우처 사업 — 정부 지원금으로 데이터 구매·가공·분석 비용 보전]
    │
    ▼
[데이터 마켓플레이스 — 공급 기업·수요 기업 연계 데이터 거래 플랫폼]
    │
    ▼
[데이터 활용 역량 강화 — AI·분석 인재 양성, 데이터 리터러시 향상]
    │
    ▼
[데이터 경제 생태계 — 공공·민간 데이터 결합, 데이터 산업 활성화]
```

이 흐름은 데이터 격차 문제 인식에서 정부 바우처 지원 정책으로 진입 장벽을 낮추고, 마켓플레이스 생태계와 역량 강화를 거쳐 국가 데이터 경제로 확장되는 데이터 민주화 정책의 계보를 보여준다.

""",
    "014_apache_hive_sql_interface.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[MapReduce — 하둡 초기 배치 처리 엔진, SQL 없이 Java 코드 직접 작성]
    │
    ▼
[Apache Hive — HiveQL로 MapReduce 추상화, SQL-on-Hadoop 구현]
    │
    ▼
[Tez / LLAP (Live Long and Process) — 메모리 DAG 실행, Hive 성능 10배 향상]
    │
    ▼
[Apache Spark SQL — RDD 대신 DataFrame API, Hive 메타스토어 호환 분석]
    │
    ▼
[레이크하우스 (Lakehouse) — Delta Lake·Iceberg로 ACID 트랜잭션 SQL 분석]
```

이 흐름은 Java 코드 직접 작성이 필요했던 MapReduce에서 SQL 추상화(Hive)로 생산성이 향상되고, Tez·Spark으로 성능이 대폭 개선되며 최종적으로 레이크하우스 아키텍처에서 ACID SQL 분석이 실현되는 하둡 생태계 진화의 핵심 계보를 보여준다.

""",
    "014_spark_runtime_architecture.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[MapReduce — 디스크 기반 배치, 반복 연산 시 I/O 오버헤드 극심]
    │
    ▼
[Apache Spark — 인메모리 RDD, Driver-Executor 분산 런타임 아키텍처]
    │
    ▼
[DAG 스케줄러 (DAG Scheduler) — 스테이지·태스크 분리, 파이프라인 최적화]
    │
    ▼
[클러스터 매니저 (YARN / Kubernetes) — 리소스 할당·컨테이너 수명 관리]
    │
    ▼
[Spark Structured Streaming — 마이크로 배치로 배치·스트리밍 통합 처리]
```

이 흐름은 디스크 I/O 병목의 MapReduce에서 인메모리 Spark으로 패러다임이 전환되고, DAG 스케줄러로 최적화된 뒤 클러스터 매니저와 통합되며 Structured Streaming으로 배치·스트리밍이 통합되는 Spark 아키텍처 진화를 보여준다.

""",
    "014_consumer_lag.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[Kafka 프로듀서 (Producer) — 토픽 파티션에 메시지 비동기 발행]
    │
    ▼
[오프셋 (Offset) — 파티션 내 메시지 위치, LEO vs 커밋 오프셋 구분]
    │
    ▼
[Consumer Lag — LEO - Current Offset, 소비 지연 누적량 정량 측정]
    │
    ▼
[컨슈머 그룹 모니터링 — Burrow·kafka-consumer-groups로 실시간 Lag 추적]
    │
    ▼
[자동 스케일링 (KEDA) — Lag 임계값 기반 컨슈머 인스턴스 수평 확장·축소]
```

이 흐름은 Kafka 메시지 발행에서 오프셋 개념으로 Consumer Lag이 정의되고, 모니터링 도구로 가시화된 뒤 KEDA 기반 자동 스케일링으로 Lag을 능동적으로 제어하는 스트리밍 파이프라인 운영의 핵심 계보를 보여준다.

""",
    "014_spatial_analysis.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[GIS (Geographic Information System) — 지리 데이터 수집·저장·분석·시각화]
    │
    ▼
[공간 데이터 모델 — 벡터(점·선·면) vs 래스터(픽셀 격자) 표현 방식]
    │
    ▼
[공간 인덱스 — R-Tree / Quad-Tree로 영역 쿼리·인근 탐색 O(logN) 가속]
    │
    ▼
[공간 분석 연산 — 버퍼·오버레이·인터섹션·보로노이 다이어그램]
    │
    ▼
[위치 기반 서비스 (LBS) / 자율주행 — 실시간 공간 분석·HD맵 활용]
```

이 흐름은 GIS 기반 지리 데이터 수집에서 벡터·래스터 모델로 구조화되고, 공간 인덱스로 쿼리 성능이 향상되며 버퍼·오버레이 분석을 거쳐 LBS·자율주행의 실시간 공간 지능으로 진화하는 공간 분석 기술의 발전 과정을 보여준다.

""",
    "014_search_engine_db.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[관계형 DB LIKE 검색 — 풀 테이블 스캔, 대규모 비정형 텍스트 처리 한계]
    │
    ▼
[역색인 (Inverted Index) — 단어→문서 매핑, 전문 검색(Full-Text Search) 핵심]
    │
    ▼
[Elasticsearch — 루씬(Lucene) 기반 분산 검색 엔진, JSON REST API, 실시간 색인]
    │
    ▼
[벡터 검색 (Vector Search) — 임베딩 유사도 기반 의미 검색, ANN 인덱스]
    │
    ▼
[AI 검색 엔진 — RAG + 벡터DB + LLM, 의미 기반 지식 검색 통합]
```

이 흐름은 RDBMS 전문 검색의 한계에서 역색인 기반 Elasticsearch로 검색 성능이 혁신되고, 벡터 검색으로 의미 기반 검색이 가능해지며 RAG+LLM 조합의 AI 검색 엔진으로 진화하는 검색 기술의 핵심 계보를 보여준다.

""",
    "014_data_fabric.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 사일로 (Data Silo) — 부서별 분산 저장, 통합 활용 불가 문제]
    │
    ▼
[ETL / ELT — 중앙 집중 복사·변환, 실시간성·유연성 한계]
    │
    ▼
[데이터 패브릭 (Data Fabric) — 메타데이터 지능으로 위치 무관 데이터 연결]
    │
    ▼
[데이터 메시 (Data Mesh) — 도메인 오너십 분산, 데이터 제품화 전략]
    │
    ▼
[지식 그래프 + AI 자동화 — 패브릭 기반 자동 데이터 발견·품질·거버넌스]
```

이 흐름은 데이터 사일로 문제를 ETL로 임시 해결하던 방식에서 메타데이터 지능 기반 패브릭으로 진화하고, 도메인 분산 거버넌스(데이터 메시)와 AI 자동화로 데이터 통합의 미래를 만들어가는 과정을 보여준다.

""",
    "014_bigdata_visualization_challenges.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[빅데이터 특성 (5V) — 대용량·고속·다양성으로 기존 차트 도구 처리 한계]
    │
    ▼
[렌더링 병목 — 수백만 포인트의 DOM/SVG 처리 불가, 브라우저 한계]
    │
    ▼
[집계·샘플링 전략 — 서버 사전 집계·분층 샘플링으로 시각화 부하 감소]
    │
    ▼
[WebGL / GPU 가속 렌더링 — deck.gl·Kepler.gl로 수억 포인트 실시간 시각화]
    │
    ▼
[스트리밍 대시보드 — 실시간 집계 + 점진적 렌더링, 라이브 빅데이터 시각화]
```

이 흐름은 빅데이터 5V 특성이 기존 시각화 도구의 렌더링 병목을 유발하고, 집계·샘플링→GPU 가속→스트리밍 대시보드로 단계별 기술 혁신을 통해 실시간 빅데이터 시각화가 가능해지는 발전 과정을 보여준다.

""",
    "014_spot_instance_ri.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[온디맨드 (On-Demand) — 필요 시 즉시 사용, 고비용 기본 과금 모델]
    │
    ▼
[예약 인스턴스 (RI, Reserved Instance) — 1·3년 약정으로 최대 75% 비용 절감]
    │
    ▼
[스팟 인스턴스 (Spot Instance) — 유휴 용량 경매, 최대 90% 할인·중단 위험]
    │
    ▼
[컴퓨팅-스토리지 분리 아키텍처 — S3+Spot 조합, 중단 내성 설계]
    │
    ▼
[FinOps — 비용 가시성·최적화 문화, 자동화 비용 조정으로 클라우드 경제성]
```

이 흐름은 온디맨드의 편의성에서 RI·Spot으로 비용 최적화 전략이 다각화되고, 중단 내성 아키텍처와 FinOps 문화로 발전하는 클라우드 비용 관리 전략의 핵심 계보를 보여준다.

""",
    "014_mdm.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 불일치 — 시스템별 고객·상품 데이터 중복·모순으로 의사결정 오류]
    │
    ▼
[MDM (Master Data Management) — 황금 레코드(Golden Record) 생성, SSOT 확보]
    │
    ▼
[데이터 거버넌스 (Data Governance) — 정책·책임·품질 기준 조직 전반 적용]
    │
    ▼
[데이터 카탈로그 (Data Catalog) — 메타데이터 관리, 데이터 자산 검색·신뢰]
    │
    ▼
[실시간 MDM (Active MDM) — CDC 기반 실시간 황금 레코드 동기화·배포]
```

이 흐름은 데이터 불일치 문제를 MDM의 황금 레코드로 해결하고, 거버넌스·카탈로그로 조직 수준에서 데이터 신뢰성을 확보하며, 실시간 MDM으로 모든 시스템에 즉각 반영되는 데이터 품질 관리의 진화 계보를 보여준다.

""",
    "014_management.md": """
### 📈 관련 키워드 및 발전 흐름도

```text
[전통 보험 계리 — 통계 테이블 기반 사고율 예측, 개인화 한계]
    │
    ▼
[빅데이터 수집 — 텔레매틱스·웨어러블·SNS·청구 데이터 통합 분석]
    │
    ▼
[AI 보험료 산정 — 개인 행동 패턴 기반 동적 요율·실시간 언더라이팅]
    │
    ▼
[보험 사기 탐지 (Fraud Detection) — 그래프 분석·이상 탐지로 허위 청구 차단]
    │
    ▼
[InsurTech 생태계 — P2P보험·임베디드 보험·자동 지급으로 전통 보험 혁신]
```

이 흐름은 전통 통계 계리에서 빅데이터 수집으로 정보의 폭이 확장되고, AI 기반 개인화 요율과 사기 탐지를 거쳐 InsurTech 생태계 전반이 혁신되는 보험 산업 빅데이터 활용의 핵심 계보를 보여준다.

""",
}


def insert_flow_section(filepath, flow_text):
    """Insert flow section between 📌 and 👶 sections, handling various header levels."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if flow already present
    if '📈 관련 키워드 및 발전 흐름도' in content:
        print(f"SKIP (already has flow): {filepath}")
        return False

    fname = filepath.split('/')[-1]

    # Special case: recursion needs all sections added before ## 참고
    if fname == '014_recursion.md':
        # Remove the old concept map section and add properly formatted sections
        # The file has ## 핵심 인사이트 ASCII 다이어그램 (Concept Map) which is different
        # Add before ## 참고
        if '## 참고' in content:
            content = content.replace('## 참고', flow_text + '## 참고')
        else:
            content = content + '\n' + flow_text
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"ADDED (recursion special): {filepath}")
        return True

    # Special case: uninformed_search and concurrency - need all sections added
    if fname in ('014_uninformed_search.md', '014_concurrency.md'):
        # Check if there's a ## 참고 section
        if '## 참고' in content:
            content = content.replace('## 참고', flow_text + '\n## 참고')
        else:
            # Append at end
            content = content.rstrip('\n') + '\n\n' + flow_text
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"ADDED (full sections): {filepath}")
        return True

    # For files that have 📌 and 👶 sections but no 📈
    # Find the 👶 line and insert before it
    # Handle both ## and ### heading levels
    import re

    # Try ### 👶 first, then ## 👶
    patterns = [
        r'(### 👶 어린이를 위한 3줄 비유 설명)',
        r'(## 👶 어린이를 위한 3줄 비유 설명)',
    ]

    for pat in patterns:
        match = re.search(pat, content)
        if match:
            insert_pos = match.start()
            content = content[:insert_pos] + flow_text + '\n' + content[insert_pos:]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"INSERTED: {filepath}")
            return True

    print(f"WARNING - no �� section found: {filepath}")
    return False


# Process all files
import os
base = '/workspaces/brainscience/content/studynote'

results = []
for root, dirs, files in os.walk(base):
    for fname in files:
        if fname in FLOW_SECTIONS:
            fpath = os.path.join(root, fname)
            result = insert_flow_section(fpath, FLOW_SECTIONS[fname])
            results.append((fname, result))

print(f"\nTotal processed: {len(results)}")
print(f"Modified: {sum(1 for _, r in results if r)}")
