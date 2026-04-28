import re, os, sys

BASE = "/workspaces/brainscience/content/studynote"

# Each entry: (filepath, flow_block, explanatory_sentence)
# flow_block: the ```text...``` part (no surrounding headers)
# For files needing full tail: also provide concept_map_block and child_block

SECTION_HEADER = "### 📈 관련 키워드 및 발전 흐름도\n"

def make_flow_section(flow_code, explanation):
    return (
        "\n### 📈 관련 키워드 및 발전 흐름도\n\n"
        "```text\n"
        + flow_code.strip("\n") +
        "\n```\n\n"
        + explanation.strip() + "\n\n"
    )

def insert_between(content, before_pattern, after_pattern, insertion):
    """Insert insertion between before_pattern and after_pattern."""
    idx = content.find(before_pattern)
    if idx == -1:
        return None, f"Pattern not found: {before_pattern!r}"
    after_idx = content.find(after_pattern, idx)
    if after_idx == -1:
        return None, f"After-pattern not found: {after_pattern!r}"
    new_content = content[:after_idx] + insertion + content[after_idx:]
    return new_content, None

def insert_before(content, before_pattern, insertion):
    """Insert insertion before before_pattern."""
    idx = content.find(before_pattern)
    if idx == -1:
        return None, f"Pattern not found: {before_pattern!r}"
    new_content = content[:idx] + insertion + content[idx:]
    return new_content, None

def append_to_eof(content, addition):
    """Append addition to end of file."""
    if not content.endswith("\n"):
        content += "\n"
    return content + addition, None

def process_file(filepath, flow_code, explanation,
                 concept_map_block=None, child_block=None,
                 mode="insert_between"):
    """
    mode:
      "insert_between" - insert flow between 관련 개념 맵 and 어린이
      "insert_before_ref" - insert flow (and child if provided) before ## 참고
      "append_tail" - append concept_map + flow + child at EOF
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    flow_section = make_flow_section(flow_code, explanation)

    if mode == "insert_between":
        # Find 관련 개념 맵 section header (### or ## level)
        # Insert flow section right before 어린이 section
        before = "### 👶 어린이를 위한 3줄 비유 설명"
        alt_before = "## 👶 어린이를 위한 3줄 비유 설명"
        if before in content:
            new_content, err = insert_before(content, before, flow_section)
        elif alt_before in content:
            new_content, err = insert_before(content, alt_before, flow_section)
        else:
            return f"ERROR: no 어린이 section in {filepath}"
        if err:
            return f"ERROR: {err} in {filepath}"

    elif mode == "insert_before_ref":
        # Insert flow (and optionally child) before ## 참고
        before_ref = "\n## 참고\n"
        insertion = flow_section
        if child_block:
            insertion += child_block
        new_content, err = insert_before(content, before_ref, insertion)
        if err:
            # try without leading newline
            before_ref2 = "## 참고\n"
            new_content, err2 = insert_before(content, before_ref2, insertion)
            if err2:
                return f"ERROR: {err} / {err2} in {filepath}"

    elif mode == "append_tail":
        addition = ""
        if concept_map_block:
            addition += concept_map_block
        addition += flow_section
        if child_block:
            addition += child_block
        new_content, err = append_to_eof(content, addition)
        if err:
            return f"ERROR: {err} in {filepath}"
    else:
        return f"ERROR: Unknown mode {mode}"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    return f"OK: {filepath}"


results = []

# ── 1. CA: 015_bjt.md ───────────────────────────────────────────────────────
r = process_file(
    f"{BASE}/01_computer_architecture/01_basic_electronics_logic/015_bjt.md",
    flow_code="""\
[진공관 (Vacuum Tube) — 고발열·고전력 전자 증폭 소자]
    │
    ▼
[BJT (Bipolar Junction Transistor) — NPN/PNP 전류 제어 증폭·스위칭]
    │
    ▼
[MOSFET (Metal-Oxide-Semiconductor FET) — 전압 제어·저전력·고집적 디지털 스위치]
    │
    ▼
[FinFET — 3D 핀 구조로 누설 전류 억제, 22nm 이하 공정 표준]
    │
    ▼
[GAA (Gate-All-Around) — 4면 게이트 채널 완전 포위, 3nm 이하 차세대 소자]""",
    explanation="이 흐름은 전류 제어 방식의 BJT가 고발열·대기 전력 한계를 드러내면서 전압 제어·저전력 MOSFET으로 전환되고, 채널 미세화에 따른 누설 전류 문제를 극복하기 위해 2D 평면에서 3D 입체 구조(FinFET→GAA)로 진화하는 반도체 능동 소자의 핵심 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 2. OS: 015_abi.md ───────────────────────────────────────────────────────
r = process_file(
    f"{BASE}/02_operating_system/01_overview_architecture/015_abi.md",
    flow_code="""\
[ISA (Instruction Set Architecture) — CPU 명령어 집합, 기계어 수준 계약]
    │
    ▼
[ABI (Application Binary Interface) — 호출 규약·데이터 정렬·심볼 명명의 바이너리 호환 규약]
    │
    ▼
[Linker — 여러 오브젝트 파일의 ABI를 맞추어 단일 실행 파일로 결합]
    │
    ▼
[FFI (Foreign Function Interface) — 서로 다른 ABI를 가진 언어 간 데이터 교환 가교]
    │
    ▼
[컨테이너 (OCI 이미지) — ABI 차이를 격리하여 이식성을 보장하는 런타임 표준]""",
    explanation="이 흐름은 CPU 명령어 집합(ISA) 위에 바이너리 호환 규약(ABI)이 정의되고, 링커가 이를 결합한 뒤 언어 간 교환(FFI)으로 확장되며, 최종적으로 컨테이너가 ABI 차이를 격리하여 이식성을 보장하는 현대적 소프트웨어 배포 패러다임으로 진화하는 과정을 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 3. NW: 015_지연_데이터_관점.md ─────────────────────────────────────────
r = process_file(
    f"{BASE}/03_network/01_data_communication/015_지연_데이터_관점.md",
    flow_code="""\
[전파 지연 (Propagation Delay) — 빛의 속도 한계, 거리에 비례]
    │
    ▼
[전송 지연 (Transmission Delay) — 패킷 크기 ÷ 대역폭, 링크 용량 의존]
    │
    ▼
[처리 지연 (Processing Delay) — 라우터 헤더 분석·포워딩 결정 소요 시간]
    │
    ▼
[큐잉 지연 (Queueing Delay) — 버퍼 대기, 트래픽 폭증 시 주요 병목]
    │
    ▼
[CDN + QoS — 엣지 캐싱으로 전파 지연↓, 우선순위 큐로 큐잉 지연↓]""",
    explanation="이 흐름은 네트워크 지연을 구성하는 4대 요소(전파·전송·처리·큐잉)를 물리 계층에서 네트워크 계층까지 분해하고, 최종적으로 CDN과 QoS가 각 지연을 실무적으로 최소화하는 아키텍처 기술로 귀결되는 네트워크 성능 설계의 핵심 흐름을 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 4. SE: 015_cmmi.md ──────────────────────────────────────────────────────
r = process_file(
    f"{BASE}/04_software_engineering/01_overview_principles/015_cmmi.md",
    flow_code="""\
[SW-CMM (초기 능력 성숙도 모델) — 소프트웨어 프로세스 5단계 평가 원형]
    │
    ▼
[CMMI v1 — SW·HW·서비스 통합, 단계적/연속적 표현 이원화]
    │
    ▼
[CMMI v2.0 — 애자일 통합, 성과(Performance) 중심 지표 재편]
    │
    ▼
[SPICE (ISO/IEC 15504) — 프로세스×능력 2차원 국제 평가 표준]
    │
    ▼
[DevSecOps + CMMI 4~5단계 — 자동화 파이프라인과 통계적 제어(SPC)로 지속 개선]""",
    explanation="이 흐름은 소프트웨어 품질 평가 원형인 SW-CMM에서 시스템·서비스를 통합한 CMMI로, 애자일을 수용한 v2.0과 국제 표준 SPICE로 확장되고, 최종적으로 DevSecOps 자동화와 통계적 프로세스 제어가 결합된 현대적 품질 경영 체계로 진화하는 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 5. DB: 015_hierarchical_data_model.md ──────────────────────────────────
r = process_file(
    f"{BASE}/05_database/01_db_architecture_relational/015_hierarchical_data_model.md",
    flow_code="""\
[계층형 데이터 모델 (Hierarchical Model) — 트리 구조, 1:N 관계, 포인터 탐색]
    │
    ▼
[망형 데이터 모델 (Network Model) — 다중 부모 허용, N:M 지원, CODASYL 표준]
    │
    ▼
[관계형 데이터 모델 (Relational Model) — 테이블+SQL+정규화, 데이터 독립성 확보]
    │
    ▼
[객체 관계형 DB (ORDB) — 관계형에 객체·상속·메서드 결합]
    │
    ▼
[NoSQL 도큐먼트 DB (MongoDB) — 임베디드 문서로 계층 구조를 재현, 수평 확장]""",
    explanation="이 흐름은 포인터 기반 계층형 모델에서 시작하여 망형→관계형으로 데이터 독립성을 확보하는 역사적 진화를 거치고, 비정형·대용량 데이터 요구 속에서 임베디드 도큐먼트로 계층 구조를 재현하는 NoSQL로 회귀하는 데이터 모델 패러다임의 발전 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 6. ICT: 015_pos_proof_of_stake.md ──────────────────────────────────────
r = process_file(
    f"{BASE}/06_ict_convergence/01_blockchain/015_pos_proof_of_stake.md",
    flow_code="""\
[PoW (Proof of Work) — 채굴 기반 합의, 높은 에너지 소비와 보안성]
    │
    ▼
[PoS (Proof of Stake) — 지분 예치 기반 검증, 에너지 99% 절감]
    │
    ▼
[DPoS (Delegated Proof of Stake) — 대표 위임 투표, 합의 처리 속도 극대화]
    │
    ▼
[이더리움 머지 (The Merge) — PoW→PoS 전환, 슬래싱으로 경제적 벌칙 강화]
    │
    ▼
[리스테이킹 (Restaking) — PoS 지분을 다중 프로토콜 보안에 재활용하는 경제 혁신]""",
    explanation="이 흐름은 에너지 집약적인 PoW에서 지분 예치 기반의 PoS로 전환되고, 대표 위임(DPoS)과 이더리움 머지라는 역사적 업그레이드로 구체화된 뒤, 예치 지분을 다중 프로토콜 보안에 재활용하는 리스테이킹 경제 혁신으로 진화하는 블록체인 합의 메커니즘의 핵심 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 7. Enterprise: 015_ita.md ───────────────────────────────────────────────
r = process_file(
    f"{BASE}/07_enterprise_systems/01_strategy_governance/015_ita_information_technology_architecture.md",
    flow_code="""\
[ISP (Information Strategy Planning) — 중장기 정보화 마스터플랜 수립]
    │
    ▼
[ITA (Information Technology Architecture) — TRM+SP 기반 IT 구조·표준 통제 체계]
    │
    ▼
[EA (Enterprise Architecture) — 비즈니스·데이터·앱·기술 4계층 통합 아키텍처]
    │
    ▼
[TOGAF / FEA — 글로벌 EA 프레임워크, ADM 방법론 국제 표준화]
    │
    ▼
[디지털 트윈 아키텍처 — EA 기반 실물-가상 동기화, 스마트정부·스마트시티 적용]""",
    explanation="이 흐름은 정보화 마스터플랜(ISP)에서 출발해 IT 구조를 표준화하는 ITA로 구체화되고, 기업 전체를 아우르는 EA(TOGAF/FEA)로 확장된 뒤, 현실과 디지털 세계를 동기화하는 디지털 트윈 아키텍처로 진화하는 공공·기업 IT 거버넌스의 발전 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 8. Algorithm: 015_bubble_sort.md — insert flow + 어린이 before ## 참고 ──
r = process_file(
    f"{BASE}/08_algorithm_stats/02_sorting/015_bubble_sort.md",
    flow_code="""\
[비교 기반 정렬 (Comparison-Based Sort) — 원소 간 비교로 순서를 결정하는 정렬 알고리즘의 공통 원리]
    │
    ▼
[버블 정렬 (Bubble Sort) — 인접 원소 교환 반복, O(N²) 안정 제자리 정렬]
    │
    ▼
[조기 종료 최적화 (Early Exit) — 교환 발생 여부 플래그로 이미 정렬된 배열 O(N) 방어]
    │
    ▼
[삽입 정렬 (Insertion Sort) — 버블과 유사한 O(N²)이나 거의 정렬된 경우 실용적 성능]
    │
    ▼
[팀소트 (TimSort) — Python·Java 내장 정렬, 삽입 정렬+병합 정렬 하이브리드로 실무 표준]""",
    explanation="이 흐름은 인접 교환이라는 단순 원리의 버블 정렬이 교육적 기준점이 되고, 조기 종료 최적화로 최선 O(N)을 확보하며, 유사 전략의 삽입 정렬을 거쳐 실무 표준인 TimSort로 발전하는 비교 기반 정렬 알고리즘의 진화 계보를 보여준다.",
    child_block=(
        "### 👶 어린이를 위한 3줄 비유 설명\n\n"
        "- 거품 정렬은 물속의 거품이 위로 올라가듯, 가장 큰 숫자가 끝으로 밀려나는 정렬이에요.\n"
        "- 이웃한 두 숫자를 비교해 큰 쪽을 오른쪽으로 한 칸씩 이동시키는 작업을 계속 반복해요.\n"
        "- 실제 프로그램에서는 너무 느려서 거의 안 쓰지만, 정렬 원리를 처음 배울 때 가장 이해하기 쉬운 방법이에요.\n\n"
    ),
    mode="insert_before_ref",
)
results.append(r)

# ── 9. Algorithm: 015_external_sort.md ─────────────────────────────────────
r = process_file(
    f"{BASE}/08_algorithm_stats/02_sorting/015_external_sort.md",
    flow_code="""\
[내부 정렬 (Internal Sort) — 데이터 전체가 메모리에 올라오는 전제 하에 동작하는 정렬]
    │
    ▼
[외부 정렬 (External Sort) — 디스크 I/O를 최소화하며 메모리 초과 데이터를 정렬]
    │
    ▼
[런 생성 (Run Generation) — 메모리 크기만큼 부분 정렬 후 디스크에 런(Run) 저장]
    │
    ▼
[K-way 병합 (K-way Merge) — 최소 힙을 활용해 K개 런을 동시 병합, Pass 수 최소화]
    │
    ▼
[MapReduce 분산 정렬 — 외부 정렬의 분산 확장, Hadoop Shuffle 단계가 K-way 병합 구현]""",
    explanation="이 흐름은 메모리 한계를 넘는 데이터를 처리하기 위해 런 생성→K-way 병합이라는 2단계 외부 정렬 패러다임이 탄생하고, 이 원리가 분산 컴퓨팅 환경에서 MapReduce Shuffle 단계로 수평 확장되는 정렬 알고리즘의 발전 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 10. Algorithm: 015_hash_table.md ────────────────────────────────────────
r = process_file(
    f"{BASE}/08_algorithm_stats/04_datastructure/015_hash_table.md",
    flow_code="""\
[직접 주소 테이블 (Direct Address Table) — 키 값을 인덱스로 직접 사용, 메모리 낭비 심함]
    │
    ▼
[해시 테이블 (Hash Table) — 해시 함수로 키를 압축해 O(1) 평균 탐색·삽입]
    │
    ▼
[체이닝 / 오픈 어드레싱 — 충돌 해결 전략, 부하 계수(Load Factor) 관리가 핵심]
    │
    ▼
[블룸 필터 (Bloom Filter) — 확률적 해시 기반 집합 멤버십 판단, 메모리 극소화]
    │
    ▼
[분산 해시 테이블 (DHT) / 일관된 해싱 — 노드 추가·삭제 시 리밸런싱 최소화, 분산 캐시 기반]""",
    explanation="이 흐름은 O(1) 탐색을 목표로 해시 함수가 등장하고, 충돌 해결 전략으로 실용성을 확보한 뒤, 확률적 멤버십 판단(블룸 필터)과 분산 시스템의 일관된 해싱으로 진화하는 해시 자료구조 발전의 핵심 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 11. Algorithm: 015_prim_algorithm.md ────────────────────────────────────
r = process_file(
    f"{BASE}/08_algorithm_stats/04_graph_algorithms/015_prim_algorithm.md",
    flow_code="""\
[그래프 (Graph) — 정점(Vertex)과 간선(Edge)으로 연결 관계를 표현하는 자료구조]
    │
    ▼
[MST (Minimum Spanning Tree) — N개 정점을 N-1개 간선으로 최소 비용 연결]
    │
    ▼
[프림 알고리즘 (Prim) — 현재 트리에서 가장 가까운 정점을 탐욕적으로 추가, O(E log V)]
    │
    ▼
[크루스칼 알고리즘 (Kruskal) — 간선 정렬+유니온 파인드, 희소 그래프에 유리]
    │
    ▼
[피보나치 힙 + 프림 — O(E + V log V) 최적화, 밀집 그래프의 이론적 최고 성능]""",
    explanation="이 흐름은 MST 문제를 정점 탐욕(프림)과 간선 탐욕(크루스칼)이라는 두 관점에서 접근하고, 피보나치 힙을 결합하여 이론적 최적 복잡도를 달성하는 MST 알고리즘 발전의 핵심 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 12. Algorithm: 015_bayesian_estimation.md ───────────────────────────────
r = process_file(
    f"{BASE}/08_algorithm_stats/08_stats/015_bayesian_estimation.md",
    flow_code="""\
[빈도주의 추정 (MLE, Frequentist) — 관측 데이터만으로 모수를 점 추정, 사전 지식 미반영]
    │
    ▼
[MAP (Maximum A Posteriori) — MLE + 사전 분포, 과적합 방지 정규화 효과]
    │
    ▼
[완전 베이즈 추정 (Full Bayesian) — 사후 분포 전체를 추론, 불확실성 정량화]
    │
    ▼
[켤레 사전 분포 (Conjugate Prior) — 사후 분포가 사전과 같은 족, 닫힌 형식 계산 가능]
    │
    ▼
[MCMC (Markov Chain Monte Carlo) — 고차원 사후 분포 샘플링, 베이즈 딥러닝·확률적 프로그래밍 기반]""",
    explanation="이 흐름은 점 추정에서 사전 지식을 결합한 MAP로, 분포 전체를 추론하는 완전 베이즈 추정으로 확장되고, 고차원 적분을 가능하게 하는 MCMC로 귀결되는 베이즈 통계 추론 체계의 발전 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 13. Security: 015_open_design.md ────────────────────────────────────────
r = process_file(
    f"{BASE}/09_security/01_intro_principles/015_open_design.md",
    flow_code="""\
[보안 원칙 (Security Principles) — 최소 권한·심층 방어·개방적 설계 등 시스템 설계 기초]
    │
    ▼
[공개 설계 원칙 (Open Design) — 보안은 알고리즘 공개, 비밀은 키(Key) 하나로 집중]
    │
    ▼
[케르크호프스 원리 (Kerckhoffs's Principle) — 암호 알고리즘은 공개해도 안전해야 한다]
    │
    ▼
[오픈소스 암호화 (AES, RSA, SHA) — 수학적 설계 완전 공개, 집단 지성으로 취약점 검증]
    │
    ▼
[버그 바운티 + KMS — 공개 환경에서 취약점 조기 발견, 유일한 비밀인 키를 중앙 관리]""",
    explanation="이 흐름은 보안 시스템의 신뢰를 비밀 유지가 아닌 공개된 수학적 견고성에 두는 공개 설계 원칙이 케르크호프스 원리로 이론화되고, 오픈소스 암호화 알고리즘과 버그 바운티 프로그램으로 실현되며, KMS가 유일한 비밀인 키를 안전하게 관리하는 현대 보안 체계로 완성되는 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 14. AI: 015_heuristic_search.md — append full tail ──────────────────────
r = process_file(
    f"{BASE}/10_ai/01_ai_basics/015_heuristic_search.md",
    flow_code="""\
[맹목적 탐색 (BFS / DFS) — 휴리스틱 없이 모든 경우의 수 탐색, 지수적 복잡도]
    │
    ▼
[탐욕적 최선 우선 탐색 (Greedy Best-First) — h(n)만 사용, 빠르지만 최적성 미보장]
    │
    ▼
[A* 알고리즘 — f(n)=g(n)+h(n), 허용 가능 h(n)으로 최적성 보장]
    │
    ▼
[가중치 A* (Weighted A*) — f(n)=g(n)+W·h(n), 최적성 포기하고 속도 우선화]
    │
    ▼
[학습 기반 휴리스틱 (Learned Heuristics) — 딥러닝으로 h(n) 함수 자체를 데이터 학습]""",
    explanation="이 흐름은 방향 없이 탐색하는 맹목적 탐색에서 경험적 추정치(h(n))를 도입한 휴리스틱 탐색으로 진화하고, A*의 최적성 보장→가중치 A*의 속도 우선화를 거쳐, 딥러닝이 휴리스틱 함수 자체를 학습하는 인공지능 탐색의 발전 계보를 보여준다.",
    concept_map_block=(
        "### 📌 관련 개념 맵\n\n"
        "| 개념 | 관계 |\n"
        "|:---|:---|\n"
        "| **A* 알고리즘** | 허용 가능 h(n) 보장 시 최적 경로를 탐색하는 휴리스틱의 대표 구현체 |\n"
        "| **Greedy Best-First Search** | h(n)만 사용, A*의 서브셋, 속도 우선이지만 최적성 보장 불가 |\n"
        "| **가지치기 (Pruning)** | 휴리스틱 값이 임계치를 넘는 노드를 탐색 전 제거하는 탐색 공간 축소 기법 |\n"
        "| **딥러닝 가치 네트워크 (Value Network)** | 강화학습에서 현재 상태의 승패 확률을 예측하는 초고도화된 학습 기반 휴리스틱 |\n"
        "| **MRV / min-conflicts** | CSP(제약 충족 문제) 탐색에서 휴리스틱을 제약 기반으로 구현한 사례 |\n\n"
    ),
    child_block=(
        "### 👶 어린이를 위한 3줄 비유 설명\n\n"
        "- 숨바꼭질을 할 때 아무 방향이나 달리는 게 아니라, '저쪽이 더 가깝겠다'고 짐작하며 달리는 게 바로 휴리스틱 탐색이에요.\n"
        "- A* 알고리즘은 지금까지 이동한 거리와 목적지까지의 예상 거리를 더해서 가장 유망한 길을 먼저 가보는 방식이에요.\n"
        "- 내비게이션이 수많은 길 중에서 빠르게 좋은 경로를 찾아주는 것도 이 휴리스틱 탐색 덕분이에요.\n\n"
    ),
    mode="append_tail",
)
results.append(r)

# ── 15. Design: 015_preliminary_survey.md ───────────────────────────────────
r = process_file(
    f"{BASE}/11_design_supervision/01_audit_framework/015_preliminary_survey.md",
    flow_code="""\
[감리 계획 수립 — 감리 목적·범위·방법론·일정 확정]
    │
    ▼
[예비 조사 (Preliminary Survey) — 사업 문서 검토·삼각 검증으로 리스크 선행 식별]
    │
    ▼
[본 감리 (Main Audit) — 현장 점검·인터뷰·산출물 심층 검증]
    │
    ▼
[감리 결과 보고 — 시정 조치 요구(F/U) 및 개선 권고]
    │
    ▼
[종료 확인 감리 — 시정 조치 이행 여부 검증, 사업 최종 품질 확인]""",
    explanation="이 흐름은 IT 감리의 전체 프로세스를 감리 계획 수립→예비 조사→본 감리→결과 보고→종료 확인 감리로 이어지는 단계적 흐름으로 보여주며, 예비 조사가 리스크 조기 발견의 핵심 관문임을 강조한다.",
    mode="insert_between",
)
results.append(r)

# ── 16. IT_Mgmt: 015_payback_period.md ──────────────────────────────────────
r = process_file(
    f"{BASE}/12_it_management/01_governance_strategy/015_payback_period.md",
    flow_code="""\
[투자 의사결정 지표 — PP, NPV, IRR, ROI 등 투자 타당성 평가 도구 집합]
    │
    ▼
[투자회수기간 (PP, Payback Period) — 초기 투자비용을 순현금흐름으로 회수하는 기간]
    │
    ▼
[할인투자회수기간 (DPP) — PP에 화폐의 시간가치(할인율) 반영, 더 보수적인 지표]
    │
    ▼
[NPV (Net Present Value) — PP가 무시하는 회수 기간 이후 현금흐름까지 포함한 총 투자 가치]
    │
    ▼
[TCO (Total Cost of Ownership) — PP 계산의 분모, 초기비용+유지보수비 포함 총소유비용]""",
    explanation="이 흐름은 가장 직관적인 투자 회수 지표인 PP가 화폐 시간가치를 반영한 DPP로 보완되고, PP가 고려하지 못하는 장기 현금흐름을 NPV가 담당하며, TCO가 정확한 원금 계산의 기반이 되는 IT 투자 평가 지표의 상호 보완 관계를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 17. Cloud: 015_virtualization.md ────────────────────────────────────────
r = process_file(
    f"{BASE}/13_cloud_architecture/01_virtualization/015_virtualization.md",
    flow_code="""\
[물리 서버 (Bare Metal) — 하드웨어 자원 1:1 점유, 낮은 활용률·비효율]
    │
    ▼
[하이퍼바이저 가상화 (Type 1/2) — 하드웨어를 분할하여 다수의 VM 동시 운용]
    │
    ▼
[컨테이너 (Container / Docker) — OS 커널 공유, 프로세스 격리, 초경량 이식성]
    │
    ▼
[마이크로VM (Firecracker) — VM 보안격리 + 컨테이너 경량성 결합, 서버리스 기반]
    │
    ▼
[SDDC (Software Defined Data Center) — CPU·스토리지·네트워크 모두 소프트웨어로 가상화]""",
    explanation="이 흐름은 물리 서버의 낮은 활용률 문제를 해결하기 위해 하이퍼바이저 가상화가 등장하고, 더 가벼운 컨테이너→마이크로VM 격리로 진화하며, 컴퓨팅·스토리지·네트워크 전체를 소프트웨어로 통제하는 SDDC로 귀결되는 클라우드 인프라 가상화의 핵심 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 18. DataEng: 015_datanode.md ────────────────────────────────────────────
r = process_file(
    f"{BASE}/14_data_engineering/01_infrastructure/015_datanode.md",
    flow_code="""\
[HDFS (Hadoop Distributed File System) — 대용량 데이터를 분산 저장하는 파일시스템]
    │
    ▼
[데이터노드 (DataNode) — 블록 단위 실제 데이터 저장·서빙, 3초마다 하트비트 전송]
    │
    ▼
[네임노드 (NameNode) — 블록 메타데이터 관리·위치 안내, DataNode 감시 사령탑]
    │
    ▼
[복제 계수 (Replication Factor=3) + 랙 인지 — 데이터 손실 방지를 위한 물리적 분산 배치]
    │
    ▼
[데이터 지역성 (Data Locality) — 연산을 데이터 위치로 이동, 네트워크 I/O 최소화]""",
    explanation="이 흐름은 HDFS의 아키텍처를 실제 블록을 보관하는 DataNode에서 메타데이터를 관리하는 NameNode로의 역할 분담으로 이해하고, 복제 계수와 랙 인지로 내결함성을 확보하며, 데이터 지역성으로 연산 효율을 극대화하는 하둡 분산 저장 설계의 핵심 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 19. DevOps: 015_disposability.md — append full tail ────────────────────
r = process_file(
    f"{BASE}/15_devops_sre/01_culture_methodology/015_disposability.md",
    flow_code="""\
[모놀리식 배포 — 서비스 재시작 시 전체 중단 필수, 배포 불안전]
    │
    ▼
[12팩터 앱 IX. 폐기 가능성 — 빠른 시작 + Graceful Shutdown 원칙 정의]
    │
    ▼
[컨테이너 (Docker) — 이미지 기반 초고속 시작, SIGTERM 수신 처리 구현]
    │
    ▼
[Kubernetes — Liveness/Readiness Probe로 파드 생명주기 자동 관리]
    │
    ▼
[FaaS (AWS Lambda / Azure Functions) — 요청당 즉시 시작·즉시 폐기, 폐기 가능성의 극단적 구현]""",
    explanation="이 흐름은 재시작 시 전체 중단이 불가피한 모놀리식 배포에서 폐기 가능성 원칙을 정의한 12팩터 앱을 거쳐, 컨테이너→Kubernetes→FaaS로 진화하며 빠른 시작과 우아한 종료가 인프라 수준에서 자동화되는 클라우드 네이티브 배포 신뢰성의 발전 계보를 보여준다.",
    concept_map_block=(
        "### 📌 관련 개념 맵\n\n"
        "| 개념 | 관계 |\n"
        "|:---|:---|\n"
        "| **12팩터 앱 (12-Factor App)** | 폐기 가능성이 IX번째 원칙으로 포함된 클라우드 네이티브 애플리케이션 설계 선언 |\n"
        "| **Graceful Shutdown** | SIGTERM 수신 후 처리 중인 요청 완료→리소스 정리→정상 종료의 단계적 프로세스 |\n"
        "| **Liveness / Readiness Probe** | Kubernetes가 파드의 시작 완료 및 생존 여부를 감지하여 폐기 가능성을 자동 관리하는 메커니즘 |\n"
        "| **무상태 설계 (Stateless)** | 메모리·디스크에 상태를 저장하지 않아 언제든 종료·재시작이 가능한 폐기 가능성의 전제 조건 |\n"
        "| **FaaS (Function-as-a-Service)** | AWS Lambda처럼 호출 시 시작, 완료 시 즉시 폐기되는 폐기 가능성의 극단적 구현 형태 |\n\n"
    ),
    child_block=(
        "### 👶 어린이를 위한 3줄 비유 설명\n\n"
        "- 레고 블록처럼, 언제든지 뽑아서 버리고 새 블록으로 바꿀 수 있는 서버가 바로 폐기 가능한 서비스예요.\n"
        "- 갑자기 끄라는 신호를 받아도 하던 일을 차분히 마무리하고 끄는 것을 '우아한 종료(Graceful Shutdown)'라고 해요.\n"
        "- 빠르게 시작하고 깔끔하게 끝낼 수 있어야 클라우드 환경에서 수백 개의 서버를 자유자재로 늘리고 줄일 수 있어요.\n\n"
    ),
    mode="append_tail",
)
results.append(r)

# ── 20. BigData: 015_open_data_principles.md ────────────────────────────────
r = process_file(
    f"{BASE}/16_bigdata/01_intro/015_open_data_principles.md",
    flow_code="""\
[1-스타 오픈 데이터 (PDF·웹 공개) — 포맷 불문, 단순 공개]
    │
    ▼
[FAIR 원칙 (Findable·Accessible·Interoperable·Reusable) — 데이터 재사용성의 국제 표준 가이드라인]
    │
    ▼
[영구 식별자 (DOI/PID) + 데이터 카탈로그 — F(발견 가능) 실현을 위한 메타데이터 인프라]
    │
    ▼
[온톨로지 + 시맨틱 웹 — I(상호운용) 실현, 컴퓨터가 의미를 이해하고 추론]
    │
    ▼
[5-스타 LOD (Linked Open Data) — 데이터를 지식 그래프로 연결, FAIR 최고 수준 구현]""",
    explanation="이 흐름은 단순 공개(1-스타)에서 FAIR 원칙이라는 국제 가이드라인으로 체계화되고, 영구 식별자·데이터 카탈로그·온톨로지·시맨틱 웹을 거쳐 데이터가 지식 그래프로 연결되는 5-스타 LOD로 진화하는 오픈 데이터 생태계의 성숙 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 21. BigData: 015_apache_hbase_column_family.md ──────────────────────────
r = process_file(
    f"{BASE}/16_bigdata/02_hadoop/015_apache_hbase_column_family.md",
    flow_code="""\
[RDBMS (관계형 DB) — 행 기반 스키마, ACID 트랜잭션, 수직 확장 한계]
    │
    ▼
[HBase — HDFS 위의 컬럼 패밀리 기반 분산 NoSQL, 수억 행 수평 확장]
    │
    ▼
[컬럼 패밀리 (Column Family) — 연관 컬럼 묶음을 동일 HFile에 배치, I/O 최적화]
    │
    ▼
[LSM-Tree (Log-Structured Merge Tree) — MemStore→HFile 계단식 병합으로 고속 쓰기]
    │
    ▼
[Apache Phoenix — HBase 위에 SQL 레이어를 추가, 기업 데이터 웨어하우스 확장]""",
    explanation="이 흐름은 행 기반 RDBMS의 수직 확장 한계를 극복하기 위해 HBase 컬럼 패밀리 구조가 등장하고, LSM-Tree 기반 고속 쓰기를 확보한 뒤, Phoenix SQL 레이어로 기업 분석 환경에 통합되는 컬럼형 분산 NoSQL의 발전 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 22. BigData: 015_spark_shuffle_optimization.md ──────────────────────────
r = process_file(
    f"{BASE}/16_bigdata/03_spark/015_spark_shuffle_optimization.md",
    flow_code="""\
[스파크 RDD 와이드 의존성 (Wide Dependency) — 셔플 발생 원인, 파티션 간 데이터 이동]
    │
    ▼
[셔플 (Shuffle) — groupBy·join 시 네트워크를 통한 데이터 재분배, 성능 병목의 핵심]
    │
    ▼
[AQE (Adaptive Query Execution) — 런타임 통계 기반 셔플 파티션 수 동적 최적화]
    │
    ▼
[브로드캐스트 조인 (Broadcast Join) — 작은 테이블을 모든 노드에 복제하여 셔플 전체 제거]
    │
    ▼
[데이터 스큐 처리 (Skew Handling) — 편향 파티션 분할·솔팅으로 불균형 셔플 해소]""",
    explanation="이 흐름은 스파크에서 셔플이 와이드 의존성으로 발생하는 원리를 이해하고, AQE의 동적 최적화→브로드캐스트 조인으로 셔플 자체를 제거하거나 최소화하며, 데이터 스큐 처리로 불균형 파티션까지 해소하는 분산 쿼리 성능 최적화의 핵심 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 23. BigData: 015_kafka_mirrormaker2.md ───────────────────────────────────
r = process_file(
    f"{BASE}/16_bigdata/04_streaming/015_kafka_mirrormaker2.md",
    flow_code="""\
[단일 클러스터 Kafka — 하나의 데이터센터 내 메시지 브로커, 장애 시 단일 장애점]
    │
    ▼
[Kafka MirrorMaker 1 — 간단한 컨슈머+프로듀서 복제, 오프셋 변환 미지원]
    │
    ▼
[Kafka MirrorMaker 2 (MM2) — Kafka Connect 기반, 오프셋 변환·자동 토픽 동기화 지원]
    │
    ▼
[Active-Passive DR — MM2로 보조 클러스터를 원본과 동기화, 장애 시 Failover 전환]
    │
    ▼
[Active-Active 다중 리전 — 양방향 복제로 지역 간 고가용성 메시지 처리 아키텍처]""",
    explanation="이 흐름은 단일 클러스터의 단일 장애점 위험을 해소하기 위해 MirrorMaker 1에서 오프셋 변환과 자동 동기화를 지원하는 MM2로 진화하고, Active-Passive DR을 거쳐 완전한 Active-Active 다중 리전 아키텍처로 발전하는 Kafka 클러스터 복제의 핵심 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 24. BigData: 015_graph_analytics.md ─────────────────────────────────────
r = process_file(
    f"{BASE}/16_bigdata/05_analysis/015_graph_analytics.md",
    flow_code="""\
[그래프 이론 (Graph Theory) — 정점(Vertex)·간선(Edge)으로 관계를 수학적 표현]
    │
    ▼
[그래프 분석 (Graph Analytics) — PageRank·커뮤니티 탐지·최단 경로 등 관계 패턴 발굴]
    │
    ▼
[Apache Spark GraphX / Pregel — 대규모 그래프의 분산 병렬 처리 프레임워크]
    │
    ▼
[지식 그래프 (Knowledge Graph) — RDF/OWL 기반 엔티티-관계 구조화, 의미 추론]
    │
    ▼
[GNN (Graph Neural Network) — 그래프 구조 + 딥러닝, 분자설계·사기탐지·추천시스템 적용]""",
    explanation="이 흐름은 그래프 이론의 수학적 기반에서 출발해 분산 처리 프레임워크로 대규모 분석을 가능케 하고, 지식 그래프의 의미 추론과 GNN의 딥러닝 결합으로 진화하는 그래프 데이터 활용 기술의 핵심 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 25. BigData: 015_multi_model_db.md ──────────────────────────────────────
r = process_file(
    f"{BASE}/16_bigdata/06_nosql/015_multi_model_db.md",
    flow_code="""\
[폴리글롯 퍼시스턴스 (Polyglot Persistence) — 용도별 최적 DB를 따로 운영, 운영 복잡도↑]
    │
    ▼
[다중 모델 DB (Multi-Model DB) — 단일 엔진에서 도큐먼트·그래프·키-값 통합 처리]
    │
    ▼
[ArangoDB — AQL 통합 쿼리 언어로 3가지 모델 일관성 있게 접근]
    │
    ▼
[SurrealDB — SurrealQL로 레코드·그래프·스키마리스를 단일 플랫폼에서 처리]
    │
    ▼
[엣지 AI + 다중 모델 DB — IoT 엣지에서 그래프+시계열+도큐먼트를 경량 DB 하나로 통합]""",
    explanation="이 흐름은 폴리글롯 퍼시스턴스의 운영 복잡도를 해소하기 위해 다중 모델 DB가 등장하고, ArangoDB·SurrealDB가 통합 쿼리 언어로 구현 복잡도를 낮추며, 엣지 AI 환경에서 경량 통합 DB로 진화하는 데이터베이스 통합 아키텍처의 핵심 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 26. BigData: 015_data_analysis_services.md ──────────────────────────────
r = process_file(
    f"{BASE}/16_bigdata/07_data_lake/015_data_analysis_services.md",
    flow_code="""\
[온프레미스 하둡 클러스터 — 자체 서버 구축·운영, 높은 초기 비용과 확장성 한계]
    │
    ▼
[클라우드 매니지드 하둡 (EMR·HDInsight·Dataproc) — 클러스터 프로비저닝 자동화, 분 단위 과금]
    │
    ▼
[컴퓨팅-스토리지 분리 아키텍처 — S3·ADLS·GCS에 데이터, 클러스터 종료 후도 데이터 보존]
    │
    ▼
[Spot/Preemptible VM 활용 — Task 노드 비용 60~80% 절감, 내결함성 설계 필수]
    │
    ▼
[서버리스 빅데이터 (EMR Serverless·Dataproc Serverless) — 클러스터 없이 Spark·Hive 실행]""",
    explanation="이 흐름은 온프레미스 하둡의 운영 부담을 클라우드 매니지드 서비스로 해소하고, 컴퓨팅-스토리지 분리로 비용 효율을 높이며, Spot VM 활용을 거쳐 클러스터 없이 쿼리를 실행하는 서버리스 빅데이터 분석으로 진화하는 클라우드 빅데이터 아키텍처의 핵심 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 27. BigData: 015_egress.md ──────────────────────────────────────────────
r = process_file(
    f"{BASE}/16_bigdata/09_platform/015_egress.md",
    flow_code="""\
[클라우드 데이터 입수 (Ingress) — 데이터 업로드, 대부분 무료 또는 저렴]
    │
    ▼
[데이터 이그레스 (Egress) — 클라우드 외부로 데이터 전송 시 발생하는 비용]
    │
    ▼
[리전 내 데이터 로컬화 — 처리와 저장을 같은 리전에 배치, 리전 간 이그레스 최소화]
    │
    ▼
[VPC 피어링 / Private Link — 퍼블릭 인터넷 우회, 이그레스 비용 절감·보안 강화]
    │
    ▼
[멀티클라우드 이그레스 최적화 — 데이터 중력(Data Gravity) 고려, 벤더 종속 회피 전략]""",
    explanation="이 흐름은 클라우드 무료 입수(Ingress)와 달리 외부 전송(Egress)에 비용이 집중되는 구조를 이해하고, 리전 내 로컬화·Private Link로 이그레스를 최소화하며, 멀티클라우드 환경에서 데이터 중력을 고려한 아키텍처 전략으로 발전하는 클라우드 네트워크 비용 최적화의 핵심 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 28. BigData: 015_data_security_governance.md ────────────────────────────
r = process_file(
    f"{BASE}/16_bigdata/10_governance/015_data_security_governance.md",
    flow_code="""\
[데이터 분류 (Data Classification) — 민감도 수준별 데이터 목록화, 보안 정책의 출발점]
    │
    ▼
[접근 제어 (RBAC·ABAC) — 역할·속성 기반 세분화 권한 관리, 최소 권한 원칙 적용]
    │
    ▼
[암호화 (AES-256-GCM 저장·TLS 1.3 전송) + 데이터 마스킹 — 저장·전송·쿼리 시점 데이터 보호]
    │
    ▼
[감사 로그 (Audit Log) + WORM 스토리지 — 불변 로그로 침해 사고 추적·규정 준수 증명]
    │
    ▼
[Zero Trust + Unity Catalog — 컬럼·행 수준까지 보안을 통합 거버넌스]""",
    explanation="이 흐름은 데이터 분류를 출발점으로 접근 제어→암호화·마스킹→불변 감사 로그로 데이터 보안의 계층을 쌓고, 최종적으로 Zero Trust 원칙과 Unity Catalog가 컬럼·행 수준까지 통합 거버넌스를 구현하는 데이터 보안 거버넌스의 성숙 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)

# ── 29. BigData: 015_management.md (부동산 빅데이터) ────────────────────────
r = process_file(
    f"{BASE}/16_bigdata/11_industry/015_management.md",
    flow_code="""\
[전통 부동산 분석 — 공인중개사 경험·주관적 판단, 데이터 비표준화]
    │
    ▼
[부동산 빅데이터 수집 — 실거래가 공개시스템·GIS 데이터·인구이동 통계 통합]
    │
    ▼
[시세 예측 모델 (머신러닝) — 헤도닉 가격 모형 + 시계열 예측으로 객관적 시세 산정]
    │
    ▼
[상권 분석·입지 전략 — 유동인구·경쟁 분포·접근성 데이터 기반 점포 최적 위치 선정]
    │
    ▼
[디지털 트윈 도시 — 빅데이터 기반 도시 시뮬레이션, 스마트시티 개발 계획 수립]""",
    explanation="이 흐름은 주관적 판단에 의존하던 전통 부동산 분석이 빅데이터 수집·머신러닝 시세 예측으로 객관화되고, 상권·입지 분석을 거쳐 디지털 트윈 도시로 진화하는 부동산 빅데이터 활용의 발전 계보를 보여준다.",
    mode="insert_between",
)
results.append(r)


for r in results:
    print(r)
