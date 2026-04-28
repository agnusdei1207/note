#!/usr/bin/env python3
"""Insert ### 📈 관련 키워드 및 발전 흐름도 sections into all 008_*.md files."""

import os

BASE = "/workspaces/brainscience/content/studynote"

# Each entry: (file_path, flow_text, explanatory_sentence, header_level)
# header_level: "###" or "##"
# mode: "insert_before_child" | "insert_before_참고" | "append_at_eof"

FLOWS = [
    # 01 CA
    {
        "path": f"{BASE}/01_computer_architecture/01_basic_electronics_logic/008_conductor.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[도체 이론 (자유 전자, Free Electron)]",
            "[구리 배선 (Copper Interconnect) — 다층 메탈]",
            "[나노 공정 스케일링 (전자 산란 / Scattering)]",
            "[신소재 적용 (코발트 Co / 루테늄 Ru)]",
            "[후면 전력망 BSPDN (Backside Power Delivery Network)]",
        ],
        "sentence": "반도체 배선 기술이 도체 기초 이론에서 출발하여 나노 공정 한계를 극복하기 위한 신소재 및 3차원 구조 혁신으로 진화한 흐름이다.",
    },
    # 02 OS
    {
        "path": f"{BASE}/02_operating_system/01_overview_architecture/008_loosely_coupled_system.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[강결합 시스템 (Tightly Coupled System) — 공유 메모리]",
            "[약결합 시스템 (Loosely Coupled System) — 메시지 패싱]",
            "[분산 운영체제 (Distributed OS)]",
            "[마이크로서비스 아키텍처 (MSA)]",
            "[엣지 컴퓨팅 (Edge Computing) / 클라우드 네이티브]",
        ],
        "sentence": "운영체제 아키텍처가 단일 서버 공유 메모리 방식에서 수평 확장 가능한 분산·엣지 컴퓨팅 생태계로 진화한 흐름이다.",
    },
    # 03 NW
    {
        "path": f"{BASE}/03_network/01_data_communication/008_단방향_반이중_전이중.md",
        "header": "##",
        "mode": "insert_before_child",
        "chain": [
            "[단방향 통신 (Simplex) — TV 방송, 삐삐]",
            "[반이중 통신 (Half-Duplex) — CSMA/CD, 무전기]",
            "[전이중 통신 (Full-Duplex) — L2 Switch, 스마트폰]",
            "[자동 협상 (Auto-Negotiation) — 최적 모드 자동 선택]",
            "[무선 전이중 (In-Band Full-Duplex) — 자기 간섭 상쇄 기술]",
        ],
        "sentence": "통신 방향 기술이 일방 수신에서 양방향 공유를 거쳐 완전 전이중 무선 통신으로 진화한 흐름이다.",
    },
    # 04 SE
    {
        "path": f"{BASE}/04_software_engineering/01_overview_principles/008_iterative_incremental_model.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[폭포수 모델 (Waterfall) — 순차 개발]",
            "[반복적/점진적 모델 (Iterative/Incremental)]",
            "[애자일 (Agile) / 스크럼 (Scrum)]",
            "[지속적 통합/배포 (CI/CD)]",
            "[DevOps / GitOps]",
        ],
        "sentence": "소프트웨어 개발 방법론이 일괄 순차 방식에서 짧은 주기의 반복 개선 및 자동화 파이프라인으로 진화한 흐름이다.",
    },
    # 05 DB
    {
        "path": f"{BASE}/05_database/01_db_architecture_relational/008_conceptual_schema.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[요구사항 분석 (Requirements Analysis)]",
            "[개념 스키마 (Conceptual Schema) — ER 다이어그램]",
            "[논리 스키마 (Logical Schema) — 릴레이션 모델]",
            "[물리 스키마 (Physical Schema) — 인덱스, 스토리지]",
            "[데이터 독립성 (Data Independence) — ANSI/SPARC 3-Layer]",
        ],
        "sentence": "데이터베이스 설계가 요구사항 수집에서 개념-논리-물리 3단계 스키마로 분리하여 데이터 독립성을 보장하는 방향으로 정립된 흐름이다.",
    },
    # 06 ICT
    {
        "path": f"{BASE}/06_ict_convergence/01_blockchain/008_merkle_root.md",
        "header": "###",
        "mode": "insert_before_참고",
        "chain": [
            "[개별 트랜잭션 해시 (TX Hash)]",
            "[머클 트리 (Merkle Tree) — 쌍 결합 해싱]",
            "[머클 루트 (Merkle Root) — 단일 32바이트 지문]",
            "[블록 헤더 (Block Header) — 머클 루트 삽입]",
            "[SPV 경량 검증 (Simple Payment Verification)]",
        ],
        "sentence": "블록체인에서 수천 개의 트랜잭션 무결성을 단일 해시 값으로 압축하고 경량 검증을 가능하게 하는 머클 루트 기술 발전 흐름이다.",
        "concept_map": """| 개념 | 관계 |
|:---|:---|
| **해시 함수 (Hash Function)** | SHA-256 기반으로 각 트랜잭션을 고정 길이 32바이트 지문으로 변환하는 핵심 연산 |
| **이진 해시 트리 (Binary Hash Tree)** | 거래 해시를 쌍으로 합쳐 단계적으로 올라가는 트리 구조로, 루트 한 개가 전체를 대표 |
| **SPV (Simple Payment Verification)** | 머클 증명 경로만으로 전체 블록 없이 특정 거래의 포함 여부를 검증하는 경량 클라이언트 기술 |
| **블록 헤더 (Block Header)** | 머클 루트를 포함한 80바이트 메타데이터로, 작업 증명(PoW)의 해싱 대상이 되는 핵심 구조 |
| **Verkle 트리 (Verkle Tree)** | 이더리움 2.0에서 머클 트리를 대체하여 증명 크기를 수십 배 줄이는 차세대 암호화 트리 |""",
        "child_summary": """1. 머클 루트는 수천 장의 영수증을 **딱 한 줄의 암호**로 요약한 마법 도장이에요.
2. 누군가 영수증 한 장을 몰래 바꾸면 암호가 완전히 달라져서 바로 들키게 돼요.
3. 이 마법 도장 덕분에 가벼운 스마트폰도 블록체인 전체를 내려받지 않고 내 거래가 진짜인지 확인할 수 있어요!""",
    },
    # 07 Enterprise
    {
        "path": f"{BASE}/07_enterprise_systems/01_strategy_governance/008_isp_information_strategy_planning.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[비즈니스 전략 (Business Strategy) — 경영 목표 설정]",
            "[정보화 전략 계획 (ISP, Information Strategy Planning)]",
            "[전사 아키텍처 (EA, Enterprise Architecture) — TOGAF]",
            "[정보화 사업 마스터플랜 (ISMP)]",
            "[IT 거버넌스 (IT Governance) — COBIT, GEA]",
        ],
        "sentence": "기업의 IT 전략이 단순 시스템 구축에서 전사 아키텍처 설계와 거버넌스 체계로 발전한 흐름이다.",
    },
    # 08 Algo/basics
    {
        "path": f"{BASE}/08_algorithm_stats/01_basics/008_memoization.md",
        "header": "###",
        "mode": "insert_before_참고",
        "chain": [
            "[재귀 (Recursion) — 하향식 문제 분해]",
            "[중복 하위 문제 (Overlapping Subproblems)]",
            "[메모이제이션 (Memoization) — 하향식 DP (Top-Down DP)]",
            "[타뷸레이션 (Tabulation) — 상향식 DP (Bottom-Up DP)]",
            "[동적 프로그래밍 (Dynamic Programming) — 최적 부분 구조]",
        ],
        "sentence": "알고리즘 최적화 기법이 단순 재귀에서 캐시 기반 메모이제이션과 완전 DP로 발전한 흐름이다.",
        "concept_map": """| 개념 | 관계 |
|:---|:---|
| **동적 프로그래밍 (DP, Dynamic Programming)** | 최적 부분 구조와 중복 하위 문제를 모두 갖는 문제를 효율적으로 해결하는 상위 패러다임 |
| **타뷸레이션 (Tabulation)** | DP의 상향식(Bottom-Up) 접근으로, 반복문으로 모든 하위 문제를 먼저 계산하는 방식 |
| **재귀 (Recursion)** | 메모이제이션 없이 사용하면 지수 시간 복잡도로 폭증하는 Top-Down 계산의 기반 |
| **LRU 캐시 (LRU Cache)** | 메모이제이션의 캐시 교체 전략으로, Python의 @functools.lru_cache가 이를 구현 |
| **피보나치 / 최장 공통 부분 수열 (LCS)** | 메모이제이션의 고전적 예제로 지수 → 다항 시간으로의 극적인 개선을 시각적으로 보여줌 |""",
        "child_summary": """1. 메모이제이션은 "한 번 풀어본 수학 문제 답을 노트에 적어뒀다가 다시 나오면 노트를 보는 것"이에요.
2. 같은 계산을 매번 새로 하는 대신 기억하면, 1000번 계산할 것을 10번만 해도 되니까 엄청 빠르죠!
3. 컴퓨터도 마찬가지로 이미 계산한 값을 캐시에 저장해두고, 똑같은 문제가 오면 저장된 답을 바로 꺼내 씁니다.""",
    },
    # 08 Algo/sorting
    {
        "path": f"{BASE}/08_algorithm_stats/03_sorting_algorithms/008_heap_sort.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[이진 힙 (Binary Heap) — 최대/최소 힙 속성]",
            "[힙 구성 (Build-Heap) — O(n) 선형 시간]",
            "[힙 정렬 (Heap Sort) — Heapify 반복 추출]",
            "[우선순위 큐 (Priority Queue) — OS 스케줄러]",
            "[인트로 정렬 (Introsort) — Quick+Heap 하이브리드]",
        ],
        "sentence": "힙 자료구조를 기반으로 정렬 알고리즘이 발전하여 우선순위 큐와 하이브리드 정렬로 확장된 흐름이다.",
    },
    # 08 Algo/DS
    {
        "path": f"{BASE}/08_algorithm_stats/04_datastructure/008_binary_tree.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[트리 (Tree) — 비선형 계층 구조]",
            "[이진 트리 (Binary Tree) — 최대 자식 2개]",
            "[이진 탐색 트리 (BST, Binary Search Tree)]",
            "[균형 이진 트리 (AVL / Red-Black Tree)]",
            "[B-트리 / B+트리 (B-Tree) — 데이터베이스 인덱스]",
        ],
        "sentence": "트리 자료구조가 기본 이진 트리에서 탐색 최적화와 균형 유지를 위한 고급 변형으로 발전한 흐름이다.",
    },
    # 08 Algo/string
    {
        "path": f"{BASE}/08_algorithm_stats/05_string/008_lz77_lz78_lzw.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[반복 패턴 감지 (Repetition Detection)]",
            "[LZ77 — 슬라이딩 윈도우 사전 압축]",
            "[LZ78 / LZW — 동적 사전 압축 (GIF/TIFF)]",
            "[DEFLATE (LZ77 + 허프만 코딩) — ZIP/PNG/gzip]",
            "[Zstandard / Brotli — 현대 고속 압축 표준]",
        ],
        "sentence": "데이터 압축 기술이 LZ 계열 사전 참조 방식에서 허프만 결합을 거쳐 현대 표준 알고리즘으로 발전한 흐름이다.",
    },
    # 08 Algo/NP
    {
        "path": f"{BASE}/08_algorithm_stats/06_np_theory/008_clique_problem.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[그래프 이론 (Graph Theory) — 정점, 간선]",
            "[클리크 문제 (Clique Problem) — NP-Complete]",
            "[독립 집합 (Independent Set) / 정점 커버 (Vertex Cover)]",
            "[3-SAT 환원 (3-SAT Reduction) — Karp 21 문제]",
            "[근사 알고리즘 (Approximation Algorithm) — 최대 클리크 근사]",
        ],
        "sentence": "클리크 문제가 NP-Complete의 중심 노드로서 다른 NP 문제들과 환원 관계를 맺고 실용적 근사 해법으로 이어지는 흐름이다.",
    },
    # 08 Algo/numerical
    {
        "path": f"{BASE}/08_algorithm_stats/07_numerical/008_matrix_multiplication.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[나이브 행렬 곱셈 (Naive MatMul) — O(n³)]",
            "[스트라센 알고리즘 (Strassen) — O(n^2.807)]",
            "[BLAS / cuBLAS — CPU/GPU SIMD 최적화]",
            "[텐서 코어 (Tensor Core) — 딥러닝 행렬 가속]",
            "[Flash Attention — 메모리 효율 행렬 연산]",
        ],
        "sentence": "행렬 곱셈 알고리즘이 기초 수식에서 하드웨어 최적화와 딥러닝 연산 혁신으로 발전한 흐름이다.",
    },
    # 08 Algo/stats
    {
        "path": f"{BASE}/08_algorithm_stats/08_stats/008_probability_distributions.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[베르누이 시행 (Bernoulli Trial) — 성공/실패]",
            "[이항 분포 (Binomial Distribution) — n회 반복]",
            "[포아송 분포 (Poisson Distribution) — 희귀 사건]",
            "[정규 분포 (Normal Distribution) — CLT 극한]",
            "[MLE 최대 우도 추정 (Maximum Likelihood Estimation)]",
        ],
        "sentence": "확률 분포가 단순 이항 분포에서 극한 근사와 모수 추정으로 체계화된 흐름이다.",
    },
    # 08 Algo/info_theory
    {
        "path": f"{BASE}/08_algorithm_stats/09_info_theory/008_channel_coding.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[섀넌 채널 용량 정리 (Shannon Channel Capacity)]",
            "[블록 부호 (Block Code) — 해밍 코드 (Hamming Code)]",
            "[터보 코드 (Turbo Code) — 반복 디코딩 (1993)]",
            "[LDPC 부호 (Low-Density Parity-Check) — 5G 데이터]",
            "[폴라 코드 (Polar Code) — 섀넌 한계 최초 달성]",
        ],
        "sentence": "채널 부호화 기술이 섀넌 이론의 증명에서 시작하여 5G 표준을 달성하는 폴라 코드까지 진화한 흐름이다.",
    },
    # 08 Algo/linear_algebra
    {
        "path": f"{BASE}/08_algorithm_stats/10_linear_algebra/008_linear_programming.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[선형 계획법 (LP, Linear Programming) — 목적함수 + 제약조건]",
            "[심플렉스 법 (Simplex Method) — 꼭짓점 탐색]",
            "[내점법 (Interior Point Method) — 다항 시간 알고리즘]",
            "[정수 계획법 (ILP) / 분기 한정법 (Branch & Bound)]",
            "[SVM / 포트폴리오 최적화 — 산업 응용]",
        ],
        "sentence": "LP 최적화 이론이 단순 선형 문제에서 정수 계획과 머신러닝 응용으로 확장된 흐름이다.",
    },
    # 09 Security
    {
        "path": f"{BASE}/09_security/01_intro_principles/008_security_awareness.md",
        "header": "##",
        "mode": "insert_before_child",
        "chain": [
            "[사이버 위협 (Cyber Threat) — 피싱, 사회공학 공격]",
            "[보안 인식 교육 (Security Awareness Training)]",
            "[피싱 시뮬레이션 (Phishing Simulation) — 행동 검증]",
            "[게임화 (Gamification) — 교육 참여도 향상]",
            "[보안 문화 (Security Culture) — 조직 내재화]",
        ],
        "sentence": "보안 인식 향상 프로그램이 단순 규정 교육에서 행동 변화를 이끄는 문화 내재화 단계로 발전한 흐름이다.",
    },
    # 10 AI
    {
        "path": f"{BASE}/10_ai/01_ai_basics/008_knowledge_base_inference_engine.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[사실 (Fact) — 작업 메모리 (Working Memory)]",
            "[지식 베이스 (Knowledge Base) — 규칙 저장소]",
            "[추론 엔진 (Inference Engine) — Rete 알고리즘]",
            "[전문가 시스템 (Expert System) — BRMS]",
            "[뉴로-심볼릭 AI (Neuro-Symbolic AI) — 딥러닝 + 추론]",
        ],
        "sentence": "AI의 지식 표현 기술이 규칙 기반 전문가 시스템에서 딥러닝과 결합한 뉴로-심볼릭 아키텍처로 진화한 흐름이다.",
    },
    # 11 Design
    {
        "path": f"{BASE}/11_design_supervision/01_audit_framework/008_audit_perspective.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[절차 관점 (Procedure Perspective) — 방법론 준수]",
            "[산출물 관점 (Product Perspective) — 결과물 품질]",
            "[성과 관점 (Performance Perspective) — 실제 가치]",
            "[근본 원인 분석 (Root Cause Analysis)]",
            "[UAT (User Acceptance Test) — 사용자 인수 테스트]",
        ],
        "sentence": "IT 감리 관점이 절차 중심에서 산출물·성과 중심으로 다원화하여 실질적 가치 검증 체계로 발전한 흐름이다.",
    },
    # 12 IT_Mgmt
    {
        "path": f"{BASE}/12_it_management/01_governance_strategy/008_bpr.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[AS-IS 프로세스 분석 (현행 업무 분석)]",
            "[업무 재설계 (BPR, Business Process Reengineering)]",
            "[ERP / 워크플로우 시스템 (Workflow System)]",
            "[RPA (Robotic Process Automation) — 반복 업무 자동화]",
            "[지속적 개선 (BPI) / 카이젠 (Kaizen)]",
        ],
        "sentence": "기업 업무 혁신 방법론이 프로세스 전면 재설계에서 자동화와 지속적 개선 체계로 발전한 흐름이다.",
    },
    # 13 Cloud
    {
        "path": f"{BASE}/13_cloud_architecture/01_virtualization/008_private_cloud.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[온프레미스 (On-Premises) — 전용 하드웨어 사일로]",
            "[서버 가상화 (Server Virtualization) — VMware vSphere]",
            "[프라이빗 클라우드 (Private Cloud) — SDDC, HCI]",
            "[컨테이너 플랫폼 (Kubernetes on-prem)]",
            "[하이브리드 클라우드 (Hybrid Cloud) — AWS Outposts / Anthos]",
        ],
        "sentence": "데이터센터 IT 인프라가 전용 하드웨어에서 프라이빗 클라우드를 거쳐 하이브리드 환경으로 진화한 흐름이다.",
    },
    # 14 DataEng
    {
        "path": f"{BASE}/14_data_engineering/01_infrastructure/008_data_lakehouse.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[데이터 웨어하우스 (DW) — ACID, 고비용 스키마 고정]",
            "[데이터 레이크 (Data Lake) — 저비용, 무결성 부재]",
            "[오픈 테이블 포맷 (Apache Iceberg / Delta Lake)]",
            "[데이터 레이크하우스 (Data Lakehouse) — DW+Lake 통합]",
            "[컴퓨팅·스토리지 분리 (Compute-Storage Separation)]",
        ],
        "sentence": "데이터 저장 아키텍처가 구조화된 웨어하우스와 비정형 레이크를 거쳐 오픈 포맷 기반의 레이크하우스로 수렴하는 흐름이다.",
    },
    # 15 DevOps
    {
        "path": f"{BASE}/15_devops_sre/01_culture_methodology/008_dependencies.md",
        "header": "###",
        "mode": "append_at_eof",
        "chain": [
            "[의존성 선언 (Dependency Declaration) — requirements.txt, package.json]",
            "[의존성 잠금 (Lock File) — 버전 고정 불변성]",
            "[가상 환경 격리 (venv / Docker) — 환경 재현성]",
            "[소프트웨어 구성 분석 (SCA, Software Composition Analysis)]",
            "[SBOM (Software Bill of Materials) — 공급망 보안]",
        ],
        "sentence": "DevOps에서 의존성 관리가 단순 버전 선언에서 보안 취약점 분석과 공급망 투명성 확보로 발전한 흐름이다.",
        "concept_map": """| 개념 | 관계 |
|:---|:---|
| **Lock 파일 (Lock File)** | `package-lock.json`, `poetry.lock` 등으로 모든 하위 의존성 버전을 고정하여 빌드 재현성을 보장하는 메커니즘 |
| **가상 환경 (Virtual Environment)** | 프로젝트별 격리된 런타임을 제공하여 전역 패키지 충돌을 방지하는 Python venv, Node nvm 등의 기술 |
| **SCA (Software Composition Analysis)** | 의존성 라이브러리의 알려진 보안 취약점(CVE)을 자동으로 탐지하는 Snyk, Dependabot 등의 도구 |
| **SBOM (Software Bill of Materials)** | 소프트웨어에 포함된 모든 컴포넌트 목록을 기록한 공급망 투명성 문서로, 미국 행정명령(EO 14028)에서 의무화 |
| **12-Factor App** | 12번째 원칙 "의존성 격리"를 포함하여 클라우드 네이티브 앱의 설계 기준을 제시하는 방법론 |""",
        "child_summary": """1. 의존성 격리는 요리를 할 때 "어떤 재료를 얼마나 쓸지 정확히 적어둔 레시피"예요. 레시피가 없으면 매번 다른 요리가 나와요.
2. Lock 파일은 그 레시피를 봉인해두는 것 — 어떤 컴퓨터에서 만들어도 똑같은 맛이 나오게 해줘요.
3. SBOM은 모든 재료의 원산지를 기록한 성분표예요. 나쁜 재료(취약한 라이브러리)가 몰래 들어왔는지 검사할 수 있어요!""",
    },
    # 16 BigData/intro
    {
        "path": f"{BASE}/16_bigdata/01_intro/008_big_data_vs_traditional_data.md",
        "header": "###",
        "mode": "append_at_eof",
        "chain": [
            "[전통적 RDBMS (관계형 DB) — ACID, 정형 데이터]",
            "[빅데이터 (Big Data) — 3V: Volume/Velocity/Variety]",
            "[NoSQL / 분산 파일 시스템 (HDFS)]",
            "[폴리글랏 퍼시스턴스 (Polyglot Persistence)]",
            "[HTAP / 레이크하우스 (Lakehouse) — 통합 플랫폼]",
        ],
        "sentence": "데이터 저장 기술이 전통적 관계형 모델에서 빅데이터 생태계를 거쳐 HTAP 통합 플랫폼으로 수렴하는 흐름이다.",
        "concept_map": """| 개념 | 관계 |
|:---|:---|
| **3V (Volume/Velocity/Variety)** | 빅데이터를 전통 데이터와 구분하는 3대 특성으로, 이후 Veracity·Value를 포함한 5V로 확장 |
| **HDFS (Hadoop Distributed File System)** | 수천 대의 범용 서버에 데이터를 분산 저장하여 단일 장애점(SPOF)을 제거하는 빅데이터 핵심 인프라 |
| **폴리글랏 퍼시스턴스 (Polyglot Persistence)** | RDBMS, NoSQL, 검색엔진 등 도메인 특성에 맞는 이종 DB를 함께 사용하는 아키텍처 전략 |
| **Schema-on-Read** | 데이터를 저장할 때는 스키마를 강제하지 않고 조회할 때 해석하는 빅데이터 레이크의 유연성 원칙 |
| **HTAP (Hybrid Transactional/Analytical Processing)** | OLTP와 OLAP을 단일 시스템에서 동시 처리하여 RDBMS와 빅데이터의 경계를 허무는 차세대 기술 |""",
        "child_summary": """1. 전통적 DB는 정리가 아주 잘 된 서랍장이에요 — 물건을 넣을 때 규칙을 지켜야 하지만 찾을 때는 빠르죠.
2. 빅데이터는 창고처럼 뭐든 다 던져 넣을 수 있어요 — 사진, 동영상, 메시지까지! 대신 찾을 때 좀 더 복잡해요.
3. 레이크하우스는 서랍장의 편리함과 창고의 넉넉함을 합친 꿈의 공간이에요 — 양쪽의 장점을 모두 가졌답니다!""",
    },
    # 16 BigData/Hadoop
    {
        "path": f"{BASE}/16_bigdata/02_hadoop/008_rack_awareness_fault_tolerance_topology.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[HDFS 복제 (Replication) — 기본 복제 계수 3]",
            "[랙 인지 (Rack Awareness) — 랙 단위 장애 격리]",
            "[복제본 배치 정책 (Replica Placement Policy)]",
            "[가용 영역 (AZ, Availability Zone) — 클라우드 확장]",
            "[리전 복제 (Cross-Region Replication) — 지역 재해 대비]",
        ],
        "sentence": "분산 파일 시스템의 내결함성 전략이 랙 인지에서 클라우드 가용 영역과 리전 수준 복제로 발전한 흐름이다.",
    },
    # 16 BigData/Spark
    {
        "path": f"{BASE}/16_bigdata/03_spark/008_adaptive_query_execution_aqe.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[정적 쿼리 계획 (Static Query Plan) — CBO]",
            "[런타임 통계 수집 (Runtime Statistics)]",
            "[적응형 쿼리 실행 (AQE, Adaptive Query Execution)]",
            "[파티션 병합 / 스큐 조인 최적화 (Skew Join)]",
            "[ML 기반 자동 튜닝 엔진 (Auto-tuning)]",
        ],
        "sentence": "Spark 쿼리 최적화가 컴파일 시점 정적 계획에서 런타임 통계 기반 동적 최적화로 발전한 흐름이다.",
    },
    # 16 BigData/Streaming
    {
        "path": f"{BASE}/16_bigdata/04_streaming/008_flink_savepoint_checkpoint.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[스트리밍 상태 (Streaming State) — 연산자 상태]",
            "[Chandy-Lamport 알고리즘 (글로벌 스냅샷)]",
            "[체크포인트 (Checkpoint) — 자동 장애 복구]",
            "[세이브포인트 (Savepoint) — 수동 버전 마이그레이션]",
            "[정확히 한 번 처리 (Exactly-Once Semantics)]",
        ],
        "sentence": "스트리밍 처리의 신뢰성이 글로벌 스냅샷 이론에서 자동 체크포인트와 수동 세이브포인트를 거쳐 정확히 한 번 처리로 실현된 흐름이다.",
    },
    # 16 BigData/Analysis
    {
        "path": f"{BASE}/16_bigdata/05_analysis/008_market_basket_analysis.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[장바구니 데이터 (POS 트랜잭션 — 판매 기록)]",
            "[연관 규칙 (Association Rules) — 지지도/신뢰도/향상도]",
            "[Apriori 알고리즘 — 빈발 항목집합 (Frequent Itemset)]",
            "[FP-Growth — 대용량 패턴 마이닝]",
            "[협업 필터링 (Collaborative Filtering) — 개인화 추천]",
        ],
        "sentence": "장바구니 분석이 단순 빈도 패턴 탐색에서 대용량 마이닝과 개인화 추천 시스템으로 발전한 흐름이다.",
    },
    # 16 BigData/NoSQL
    {
        "path": f"{BASE}/16_bigdata/06_nosql/008_mongodb_architecture.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[문서 지향 DB (Document-Oriented DB)]",
            "[WiredTiger 스토리지 엔진 — MVCC]",
            "[레플리카 셋 (Replica Set) — 자동 장애 조치]",
            "[샤딩 (Sharding) — 수평 확장]",
            "[Atlas (클라우드 MongoDB) — 서버리스 Document DB]",
        ],
        "sentence": "MongoDB 아키텍처가 단일 노드에서 복제와 샤딩을 거쳐 완전 관리형 클라우드 서비스로 발전한 흐름이다.",
    },
    # 16 BigData/DataLake
    {
        "path": f"{BASE}/16_bigdata/07_data_lake/008_unity_catalog.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[분산 데이터 사일로 (Data Silo) — 거버넌스 부재]",
            "[데이터 카탈로그 (Data Catalog) — 메타데이터 관리]",
            "[Unity Catalog — 3-수준 네임스페이스 (catalog.schema.table)]",
            "[행/컬럼 수준 접근 제어 (Row Filter / Column Mask)]",
            "[Delta Sharing — 오픈 프로토콜 안전 데이터 공유]",
        ],
        "sentence": "데이터 거버넌스가 분산 사일로에서 중앙화된 카탈로그와 세분화된 접근 제어를 거쳐 안전한 외부 공유로 발전한 흐름이다.",
    },
    # 16 BigData/Visualization
    {
        "path": f"{BASE}/16_bigdata/08_visualization/008_grafana.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[메트릭 수집 (Metrics) — Prometheus Pull 방식]",
            "[로그 집계 (Log Aggregation) — Loki]",
            "[분산 추적 (Distributed Tracing) — Tempo]",
            "[Grafana 대시보드 — 통합 관측성 (Unified Observability)]",
            "[LGTM 스택 (Loki + Grafana + Tempo + Mimir)]",
        ],
        "sentence": "관측성 기술이 개별 메트릭·로그·추적을 통합하여 Grafana 중심의 단일 가시성 플랫폼으로 수렴한 흐름이다.",
    },
    # 16 BigData/Platform
    {
        "path": f"{BASE}/16_bigdata/09_platform/008_serverless_bigdata.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[관리형 클러스터 (Managed Cluster) — EMR, Dataproc]",
            "[서버리스 쿼리 (Serverless Query) — AWS Athena, BigQuery]",
            "[오픈 테이블 포맷 최적화 (Parquet + 파티셔닝)]",
            "[쿼리 비용 최적화 (FinOps) — 스캔 최소화]",
            "[AI/ML 통합 (BigQuery ML, SageMaker Serverless)]",
        ],
        "sentence": "빅데이터 처리 플랫폼이 클러스터 관리 부담에서 서버리스 온디맨드 쿼리로 진화하고 AI/ML과 융합되는 흐름이다.",
    },
    # 16 BigData/Governance
    {
        "path": f"{BASE}/16_bigdata/10_governance/008_data_governance_components.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[데이터 소유권 (Data Ownership) — Owner/Steward/Custodian]",
            "[데이터 정책 (Data Policy) / 표준 (Data Standard)]",
            "[데이터 카탈로그 (Data Catalog) — 메타데이터 목록]",
            "[데이터 거버넌스 (Data Governance) — 5대 구성 요소]",
            "[데이터 메시 (Data Mesh) — 연방형 거버넌스]",
        ],
        "sentence": "데이터 거버넌스가 역할 정의에서 정책·표준·카탈로그를 거쳐 조직 전체의 연방형 자율 관리로 발전한 흐름이다.",
    },
    # 16 BigData/Industry
    {
        "path": f"{BASE}/16_bigdata/11_industry/008_smart_city_bigdata.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[도시 센서 인프라 (IoT / CCTV / 스마트미터)]",
            "[도시 데이터 허브 (CDH, City Data Hub)]",
            "[지능형 교통 (ATSC) / 스마트 에너지 (EMS)]",
            "[디지털 트윈 (Digital Twin) — 가상 도시 시뮬레이션]",
            "[AI 기반 스마트시티 — 자율주행 + 예측 행정]",
        ],
        "sentence": "스마트시티가 개별 IoT 센서 수집에서 통합 데이터 허브와 디지털 트윈을 거쳐 AI 기반 자율 도시 관리로 발전하는 흐름이다.",
    },
    # 16 BigData/Trends
    {
        "path": f"{BASE}/16_bigdata/12_trends/008_apache_iceberg.md",
        "header": "###",
        "mode": "insert_before_child",
        "chain": [
            "[Hive Metastore — 파티션 열거 병목]",
            "[Apache Iceberg — 오픈 테이블 포맷 표준]",
            "[스냅샷 / 타임 트래블 (Time Travel)]",
            "[멀티 엔진 접근 (Multi-Engine) — Spark / Flink / Trino]",
            "[오픈 데이터 레이크하우스 생태계 (Open Lakehouse)]",
        ],
        "sentence": "데이터 레이크 포맷 기술이 Hive의 한계를 극복하고 Iceberg를 중심으로 멀티 엔진 개방형 생태계로 수렴하는 흐름이다.",
    },
]


def build_flow_block(entry):
    """Build the flow section text block."""
    h = entry["header"]
    chain = entry["chain"]
    sentence = entry["sentence"]

    lines = [f"{h} 📈 관련 키워드 및 발전 흐름도", "", "```text"]
    for i, item in enumerate(chain):
        lines.append(item)
        if i < len(chain) - 1:
            lines.append("    │")
            lines.append("    ▼")
    lines.append("```")
    lines.append("")
    lines.append(sentence)
    return "\n".join(lines)


def process_file(entry):
    path = entry["path"]
    if not os.path.exists(path):
        print(f"SKIP (not found): {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    h = entry["header"]
    mode = entry["mode"]
    flow_block = build_flow_block(entry)

    if mode == "insert_before_child":
        child_marker = f"{h} 👶 어린이를 위한 3줄 비유 설명"
        if f"{h} 📈 관련 키워드 및 발전 흐름도" in content:
            print(f"SKIP (already has flow): {path}")
            return
        if child_marker not in content:
            print(f"WARNING (no child marker): {path}")
            return
        new_content = content.replace(
            child_marker,
            f"{flow_block}\n\n{child_marker}"
        )

    elif mode == "insert_before_참고":
        ref_marker = "\n## 참고"
        if f"{h} 📈 관련 키워드 및 발전 흐름도" in content:
            print(f"SKIP (already has flow): {path}")
            return
        # Build full tail: concept_map + flow + child
        concept_map = entry.get("concept_map", "")
        child_summary = entry.get("child_summary", "")
        tail = (
            f"\n\n{h} 📌 관련 개념 맵\n\n{concept_map}\n\n"
            f"{flow_block}\n\n"
            f"{h} 👶 어린이를 위한 3줄 비유 설명\n\n{child_summary}\n"
        )
        if ref_marker in content:
            new_content = content.replace(ref_marker, tail + ref_marker)
        else:
            new_content = content + tail

    elif mode == "append_at_eof":
        if f"{h} 📈 관련 키워드 및 발전 흐름도" in content:
            print(f"SKIP (already has flow): {path}")
            return
        concept_map = entry.get("concept_map", "")
        child_summary = entry.get("child_summary", "")
        tail = (
            f"\n\n---\n\n{h} 📌 관련 개념 맵\n\n{concept_map}\n\n"
            f"{flow_block}\n\n"
            f"{h} 👶 어린이를 위한 3줄 비유 설명\n\n{child_summary}\n"
        )
        new_content = content.rstrip() + tail
    else:
        print(f"UNKNOWN mode: {mode}")
        return

    if new_content == content:
        print(f"NO CHANGE: {path}")
        return

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"OK: {path}")


for entry in FLOWS:
    process_file(entry)
print("DONE")
