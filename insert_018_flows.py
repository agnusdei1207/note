import re
import os

BASE = "/workspaces/brainscience/content/studynote"

FLOWS = {
    "01_computer_architecture/01_basic_electronics_logic/018_cmos.md": {
        "flow": """```text
[NMOS (N형 MOSFET) — 전류 흐름, 대기 전력 낭비]
    │
    ▼
[CMOS (Complementary MOS) — PMOS+NMOS 상보 쌍, 대기 전력 0]
    │
    ▼
[FinFET (Fin Field-Effect Transistor) — 3D 게이트, 누설 전류 억제]
    │
    ▼
[Beyond CMOS (GaN·그래핀·스핀트로닉스) — 양자 물리 기반 차세대 소자]
```
CMOS는 NMOS와 PMOS를 쌍으로 묶어 대기 전력을 근본적으로 차단한 설계로, FinFET 이후 Beyond CMOS 기술로 발전하고 있다.""",
        "child": """📖 **두 개의 수도꼭지**: CMOS는 성격이 반대인 두 꼭지(PMOS, NMOS)를 서로 맞대어 놓아서, 한쪽이 열리면 다른 쪽은 반드시 닫히는 완벽한 절수 시스템이에요!  
🔋 **전기 낭비 0**: 두 꼭지가 동시에 열리는 일이 없어서 물(전류)이 바닥으로 새지 않아 스마트폰 배터리가 오래 가는 비결이랍니다!  
🔬 **작아지는 문**: 스마트폰 칩이 해마다 손톱의 수백만 분의 1 크기로 작아지는 건 CMOS 덕분이고, 미래엔 원자 한 개짜리 꼭지(Beyond CMOS)를 쓸 거예요!""",
    },
    "02_operating_system/01_overview_architecture/018_software_interrupt_trap.md": {
        "flow": """```text
[하드웨어 인터럽트 (HW Interrupt) — 외부 I/O 신호, 비동기 발생]
    │
    ▼
[소프트웨어 인터럽트 (SW Interrupt) — INT 명령, 의도적 커널 진입]
    │
    ▼
[트랩 (Trap) / 예외 (Exception) — 오류·보호 위반, 동기적 발생]
    │
    ▼
[시스템 콜 (System Call) — 사용자 모드 → 커널 모드 안전한 전환]
    │
    ▼
[인터럽트 서비스 루틴 (ISR) → 컨텍스트 복원 → 사용자 모드 복귀]
```
소프트웨어 인터럽트와 트랩은 프로세스가 커널 서비스를 안전하게 이용하는 통로로, 시스템 콜의 구현 기반이 된다.""",
        "child": """📢 **비상 벨**: 소프트웨어 인터럽트는 프로그램이 "도움 필요해요!"라고 CPU에 비상벨을 누르는 행동이에요. CPU가 하던 일을 잠깐 멈추고 달려오는 것이죠!  
⚠️ **사고 신고**: 트랩은 프로그램이 0으로 나누기처럼 실수를 저질렀을 때 자동으로 울리는 경보예요. 운영체제가 "이 프로그램이 실수했어요!"라고 수습하러 옵니다.  
🔑 **안전 출입구**: 시스템 콜은 일반 사용자가 금고(커널) 안에 직접 들어가지 않고 창구(인터럽트)를 통해 요청하는 안전한 방법이에요!""",
    },
    "03_network/01_data_communication/018_큐잉_지연.md": {
        "flow": """```text
[전파 지연 (Propagation Delay) — 물리 매체 거리 비례 지연]
    │
    ▼
[전송 지연 (Transmission Delay) — 패킷 크기 / 링크 대역폭]
    │
    ▼
[처리 지연 (Processing Delay) — 라우터 헤더 분석 시간]
    │
    ▼
[큐잉 지연 (Queueing Delay) — 버퍼 혼잡 대기, 가장 가변적]
    │
    ▼
[혼잡 제어 (Congestion Control) → QoS / 트래픽 쉐이핑으로 개선]
```
큐잉 지연은 4가지 전달 지연 중 네트워크 부하에 따라 가장 크게 변동하며, QoS 정책으로 우선순위를 조정해 완화한다.""",
        "child": """🚦 **신호등 대기**: 큐잉 지연은 사거리 신호등처럼 라우터 앞에서 패킷들이 줄 서서 기다리는 시간이에요. 차가 많을수록(트래픽) 더 오래 기다려야 해요!  
📦 **택배 창고**: 패킷들이 라우터 버퍼(창고)에 쌓이면 늦게 온 패킷은 더 오래 기다려요. 창고가 꽉 차면 새 택배가 바닥에 버려지는 것(패킷 손실)처럼요!  
🎯 **VIP 줄**: QoS는 VIP 줄을 따로 만드는 것처럼 음성 통화나 게임처럼 중요한 패킷이 먼저 나갈 수 있게 우선순위를 줘요!""",
    },
    "04_software_engineering/01_overview_principles/018_psp_tsp.md": {
        "flow": """```text
[폭포수 모델 (Waterfall) — 하향식 단계별 개발, 개인 역량 미고려]
    │
    ▼
[CMM / CMMI (Capability Maturity Model) — 조직 수준 프로세스 개선]
    │
    ▼
[PSP (Personal Software Process) — 개인 수준 측정·계획·품질 자동화]
    │
    ▼
[TSP (Team Software Process) — 팀 수준 자율 관리, PSP 팀 통합]
    │
    ▼
[애자일 (Agile) / 스크럼 (Scrum) — 반복·협업, PSP/TSP 원칙 계승]
```
PSP는 개인의 측정 습관을, TSP는 자기 조직화 팀 원칙을 정립하여 CMM과 애자일 사이의 가교 역할을 한다.""",
        "child": """📓 **개인 일기장 (PSP)**: PSP는 개발자가 자기가 몇 시간 일했는지, 어떤 실수를 몇 번 했는지 꼼꼼히 일기장에 기록해서 다음엔 더 잘할 수 있게 하는 방법이에요!  
👥 **팀 회의 (TSP)**: TSP는 PSP를 쓰는 개발자들이 모여서 서로의 일기를 나누고, 함께 계획을 짜는 팀 규칙이에요. 팀이 스스로 일정을 관리해요!  
📊 **자기 계발**: PSP와 TSP는 선생님(관리자)이 시켜서가 아니라 스스로 측정하고 개선하는 거예요. 마치 운동선수가 스스로 기록을 재고 훈련하는 것처럼요!""",
    },
    "05_database/01_db_architecture_relational/018_object_oriented_relational_data_model.md": {
        "flow": """```text
[관계형 모델 (RDBMS) — 테이블·SQL, 복잡한 타입 표현 한계]
    │
    ▼
[객체지향 모델 (OODBMS) — 객체·상속·메서드, 임피던스 불일치 해결]
    │
    ▼
[객체-관계형 모델 (ORDBMS) — RDBMS + 사용자 정의 타입(UDT), SQL 확장]
    │
    ▼
[NoSQL (Document·Graph DB) — 스키마리스, 수평 확장]
    │
    ▼
[NewSQL / 멀티모델 DB — ACID + 수평 확장 통합]
```
OODBMS와 ORDBMS는 관계형 모델의 타입 표현 한계를 극복하는 두 가지 접근법으로, 현대 다중 모델 DB의 전신이다.""",
        "child": """📦 **레고 블록 (OODBMS)**: 객체지향 DB는 레고처럼 모양이 다른 블록(객체)을 그대로 서랍(DB)에 넣을 수 있어요. 테이블로 자르고 붙이는 복잡한 일이 없어요!  
🧬 **유전자 (상속)**: 객체는 부모 모양을 그대로 물려받을 수 있어요. '동물' 서랍을 열면 '개'도 들어있고 '고양이'도 들어있는 것처럼요!  
🔀 **혼합 서랍 (ORDBMS)**: ORDBMS는 기존 테이블(서랍)에 특별 칸(사용자 정의 타입)을 추가한 것이에요. 낡은 서랍을 버리지 않고 업그레이드한 거예요!""",
    },
    "06_ict_convergence/01_blockchain/018_post_proof_of_space_and_time.md": {
        "flow": """```text
[PoW (Proof of Work) — CPU/GPU 연산 경쟁, 막대한 에너지 소비]
    │
    ▼
[PoS (Proof of Stake) — 토큰 지분 증명, 에너지 절약]
    │
    ▼
[PoSpace (Proof of Space) — 디스크 공간 사전 플로팅, I/O 기반]
    │
    ▼
[PoST (Proof of Space and Time) — 공간 + VDF 시간 증명, Chia Network]
    │
    ▼
[VDF (Verifiable Delay Function) — 검증 가능한 지연 함수, 선행 조건 방지]
```
PoST는 디스크 공간(Space)을 사전 확보하고 VDF로 시간 경과를 증명하여, PoW의 에너지 낭비 없이 분산 합의를 달성한다.""",
        "child": """🌱 **씨앗 미리 심기 (Farming)**: PoST는 미리 하드디스크에 씨앗(플롯)을 심어두고, 블록을 만들 때 그 씨앗이 맞는지 확인해요. 심는 것은 한 번만 하면 돼요!  
⏱️ **타임캡슐 (VDF)**: 일정 시간이 지나야만 열리는 타임캡슐(VDF)로 정직하게 기다렸음을 증명해요. 빠른 컴퓨터라도 시간을 건너뛸 수 없어요!  
🌿 **친환경 채굴**: 하드디스크는 GPU보다 전기를 훨씬 덜 먹어요. 그래서 PoST는 지구에 더 친절한 블록체인 방법이에요!""",
    },
    "07_enterprise_systems/01_strategy_governance/018_pi.md": {
        "flow": """```text
[현행 업무 분석 (As-Is Analysis) — 비효율·병목 지점 파악]
    │
    ▼
[BPR (Business Process Reengineering) — 급진적 전면 재설계, 높은 리스크]
    │
    ▼
[PI (Process Innovation) — 점진적·연속적 개선, IT 활용 최적화]
    │
    ▼
[지속적 개선 (CI, Continuous Improvement) — 카이젠·린, 작은 반복 개선]
    │
    ▼
[디지털 전환 (DX, Digital Transformation) — 데이터 기반 비즈니스 재창조]
```
PI는 BPR의 급진적 리스크와 단순 개선의 한계 사이에서 IT 활용을 통한 중속도 혁신을 실현한다.""",
        "child": """🏗️ **낡은 건물 고치기**: BPR이 건물 전체를 허물고 새로 짓는 것이라면, PI는 방 하나씩 리모델링하는 방법이에요. 사람들이 계속 살면서도 개선할 수 있어요!  
💻 **IT로 업그레이드**: PI는 컴퓨터와 소프트웨어를 이용해 사람이 하던 반복 작업을 자동화하는 것이 핵심이에요. 서류 도장 찍는 일을 클릭 한 번으로 바꾸는 거예요!  
🔄 **멈추지 않는 개선**: PI는 한 번 고치고 끝이 아니라 계속 조금씩 나아지는 것을 목표로 해요. 마치 매일 조금씩 운동하는 것처럼요!""",
    },
}

FLOWS2 = {
    "08_algorithm_stats/02_sorting/018_shell_sort.md": {
        "flow": """```text
[삽입 정렬 (Insertion Sort) — O(n²), 이미 정렬된 배열엔 O(n)]
    │
    ▼
[셸 정렬 (Shell Sort) — Gap 기반 분할, 원소 이동 거리 단축]
    │
    ▼
[Gap 시퀀스 최적화 (Knuth·Pratt·Ciura) — O(n^1.5)~O(n log²n)]
    │
    ▼
[힙 정렬 (Heap Sort) / 퀵 정렬 (Quick Sort) — O(n log n) 목표]
```
셸 정렬은 Gap을 점차 줄여 가며 삽입 정렬을 반복하는 방식으로, Gap 시퀀스 선택에 따라 O(n^1.5)까지 성능을 개선한 알고리즘이다.""",
        "map": """| 개념 | 연결 관계 | 설명 |
|:---|:---|:---|
| 삽입 정렬 (Insertion Sort) | → 기반 알고리즘 | Gap=1일 때 동일하게 동작 |
| Gap 시퀀스 (Gap Sequence) | → 핵심 파라미터 | Shell·Knuth·Pratt 등 |
| 퀵 정렬 (Quick Sort) | → 성능 비교 대상 | 평균 O(n log n), 최악 O(n²) |
| 병합 정렬 (Merge Sort) | → 안정 정렬 비교 | O(n log n), 안정, 추가 공간 필요 |
| 힙 정렬 (Heap Sort) | → 최악 보장 비교 | O(n log n) 항상 보장 |""",
        "child": """📏 **멀리서 먼저 짝 맞추기**: 셸 정렬은 긴 줄에서 먼 거리(Gap)의 친구끼리 먼저 키를 맞추고, 점점 가까운 친구들끼리 맞추는 방법이에요!  
🔢 **Gap 줄이기**: 처음엔 4칸 간격, 다음엔 2칸, 마지막엔 1칸으로 간격을 줄여가요. 마지막 1칸은 그냥 삽입 정렬인데 이미 거의 정렬되어 있어서 엄청 빨라요!  
⚡ **효율적인 이동**: 원소가 제자리까지 조금씩 이동하는 대신, 처음부터 크게 뛰어서 빠르게 이동해요. 마치 체스의 나이트처럼 멀리 이동하는 거예요!""",
    },
    "08_algorithm_stats/04_datastructure/018_graph_datastructure.md": {
        "flow": """```text
[선형 자료구조 (Array / Linked List) — 1차원 순서 관계]
    │
    ▼
[트리 (Tree) — 계층 관계, 사이클 없는 연결 그래프]
    │
    ▼
[그래프 (Graph) — 정점(V) + 간선(E), 방향/무방향·가중/비가중]
    │
    ▼
[BFS (Breadth-First Search) / DFS (Depth-First Search) — 그래프 탐색]
    │
    ▼
[최단 경로 (Dijkstra·Bellman-Ford·Floyd-Warshall) → 네트워크 플로우]
```
그래프는 트리보다 일반적인 관계를 표현하며, BFS/DFS 탐색을 기반으로 최단 경로·위상 정렬·네트워크 플로우 알고리즘으로 확장된다.""",
        "child": """🗺️ **지도 그리기**: 그래프는 도시(정점)와 도로(간선)로 만든 지도예요. 어느 도시에서 어느 도시로 갈 수 있는지 표현할 수 있어요!  
🔀 **방향 표시**: 일방통행(방향 그래프)처럼 한 방향으로만 갈 수 있는 도로도 있고, 양방향 도로(무방향 그래프)도 있어요!  
📍 **가장 빠른 길 찾기**: 내비게이션이 최단 경로를 찾는 방법이 바로 그래프에서 Dijkstra 알고리즘을 쓰는 거예요!""",
    },
    "08_algorithm_stats/08_stats/018_chi_square_test.md": {
        "flow": """```text
[기술 통계 (Descriptive Statistics) — 평균·분산·빈도 요약]
    │
    ▼
[가설 검정 (Hypothesis Testing) — 귀무가설 H₀, 대립가설 H₁]
    │
    ▼
[카이제곱 검정 (Chi-Square Test) — 범주형 변수 빈도, 관찰값 vs 기대값]
    │
    ▼
[독립성 검정 (Independence Test) / 적합도 검정 (Goodness-of-Fit)]
    │
    ▼
[p-값 해석 (p-value) → 유의수준 α와 비교 → 귀무가설 기각 여부 판정]
```
카이제곱 검정은 범주형 데이터의 관찰 빈도와 기대 빈도 간 차이를 수치화하여, 독립성 및 분포 적합성을 검증하는 비모수 통계 기법이다.""",
        "child": """🎲 **주사위 공정성 검사**: 주사위를 60번 던졌을 때 각 숫자가 10번씩 나와야 공정한데, 실제로는 차이가 있어요. 카이제곱 검정은 그 차이가 우연인지 아닌지를 판단해요!  
🔗 **관계가 있나 없나**: 키가 크면 발도 클까요? 두 항목이 서로 관계있는지(독립성) 카이제곱 검정으로 확인할 수 있어요!  
📊 **관찰 vs 기대**: 실제 관찰한 숫자와 우리가 예상한 숫자를 비교해서 차이가 너무 크면 "뭔가 이상해!"라고 판단하는 것이 카이제곱 검정이에요!""",
    },
    "09_security/01_intro_principles/018_iot_ot_ics_physical.md": {
        "flow": """```text
[IT 보안 (IT Security) — 기밀성 중심, 패치·업데이트 가능]
    │
    ▼
[OT/ICS 보안 (Operational Technology) — 가용성·무결성 우선, 레거시 환경]
    │
    ▼
[에어갭 붕괴 (Air Gap 붕괴) — IT·OT 융합, 스마트 팩토리 전환]
    │
    ▼
[퍼듀 모델 (Purdue Model) / IEC 62443 — 계층 분리, 구역·배관 통제]
    │
    ▼
[제로 트러스트 OT (Zero Trust OT) — 기기 인증, OPC UA 암호화 표준화]
```
OT/ICS 보안은 가용성을 최우선으로 하며, 퍼듀 모델과 IEC 62443 기반의 구역 격리로 사이버-물리 위협을 차단한다.""",
        "map": """| 개념 | 연결 관계 | 설명 |
|:---|:---|:---|
| 퍼듀 모델 (Purdue Model) | → 아키텍처 기준 | IT-OT 5계층 분리 표준 |
| IEC 62443 | → 국제 표준 | OT 보안 요구사항 및 구역 통제 |
| SCADA / PLC | → 보호 대상 | 산업 제어 장비, 레거시 OS |
| 스턱스넷 (Stuxnet) | → 대표 위협 사례 | 핵 원심분리기 PLC 공격 |
| Zero Trust OT | → 발전 방향 | 기기 단위 인증 및 최소 권한 |""",
        "child": """🏭 **공장 방어선**: OT 보안은 인터넷 해커가 공장 로봇팔에 나쁜 명령을 보내지 못하도록 막는 것이에요. 공장이 멈추면 사람이 다칠 수도 있어서 매우 중요해요!  
🔌 **연결의 위험**: 예전에는 공장 컴퓨터가 인터넷과 완전히 분리되어 안전했어요. 하지만 이제 인터넷으로 공장을 원격 관리하면서 해커가 침입할 구멍이 생겼어요!  
🛡️ **층별 방어**: 퍼듀 모델은 공장 네트워크를 층별로 나눠서 한 층이 뚫려도 다른 층은 안전하게 지키는 방어 방법이에요. 아파트 각 층에 자물쇠를 따로 달아두는 것처럼요!""",
    },
}

FLOWS3 = {
    "10_ai/01_ai_basics/018_admissible_heuristic.md": {
        "flow": """```text
[맹목적 탐색 (Blind Search: BFS/DFS) — 휴리스틱 없음, 전수 탐색]
    │
    ▼
[정보 탐색 (Informed Search) — 휴리스틱 함수 h(n) 활용]
    │
    ▼
[허용적 휴리스틱 (Admissible Heuristic) — h(n) ≤ h*(n), 과대평가 금지]
    │
    ▼
[A* 알고리즘 (A* Search) — f(n)=g(n)+h(n), 최적해 보장]
    │
    ▼
[일관적 휴리스틱 (Consistent Heuristic) — 삼각 부등식, A* 효율 극대화]
```
허용적 휴리스틱은 A*가 최적해를 보장하기 위한 필수 조건으로, 실제 비용을 절대 과대평가하지 않는 추정 함수의 성질이다.""",
        "child": """🗺️ **지도 예상 거리**: 허용적 휴리스틱은 내비게이션이 목적지까지 남은 거리를 예상할 때, 실제 거리보다 절대 크게 말하지 않는 정직한 예상이에요!  
🎯 **과소평가 OK**: "아직 5km 이상 남았어!"처럼 줄여서 말하는 건 괜찮지만, "1km밖에 안 남았어!"처럼 크게 말하면 엉뚱한 길로 안내할 수 있어요!  
🏆 **최단 경로 보장**: 허용적 휴리스틱을 쓰면 A*가 반드시 가장 짧은 길을 찾아내요. 마치 정직한 길 안내사가 있으면 절대 먼 길로 돌아가지 않는 것처럼요!""",
    },
    "11_design_supervision/01_audit_framework/018_audit_report.md": {
        "flow": """```text
[감리 계획 수립 — 범위·일정·체크리스트 확정]
    │
    ▼
[현장 감리 수행 — 문서 검토, 인터뷰, 산출물 확인]
    │
    ▼
[결과 분석 — 지적 사항 분류 (중결함·경결함·권고)]
    │
    ▼
[감리 보고서 (Audit Report) — 총평·분야별 결과·시정 조치 권고]
    │
    ▼
[시정 조치 이행 → 이행 점검 → 차기 감리 환류]
```
감리 보고서는 감리 수행의 최종 결과물로, 중결함·경결함·권고 사항을 구분하여 발주기관과 사업자가 합의·이행해야 할 공식 문서다.""",
        "child": """📋 **성적표**: 감리 보고서는 IT 시스템을 만드는 팀에게 주는 성적표예요. 잘한 것, 부족한 것, 꼭 고쳐야 할 것을 정리해서 알려줘요!  
🔍 **선생님 검사**: 감리원은 선생님처럼 숙제(소프트웨어)를 꼼꼼히 검사하고 "이건 틀렸어!", "이건 더 잘할 수 있어!"라고 써주는 거예요!  
✅ **고치면 합격**: 보고서를 받은 팀은 지적된 것들을 고치면 돼요. 다음번에 다시 검사받아서 모두 합격하면 프로젝트가 안전하게 완성된 거예요!""",
    },
    "12_it_management/01_governance_strategy/018_kpi.md": {
        "flow": """```text
[비전 / 전략 목표 (Vision & Strategy) — 조직의 최상위 방향]
    │
    ▼
[BSC (Balanced Scorecard) — 재무·고객·프로세스·학습 4관점 균형]
    │
    ▼
[CSF (Critical Success Factor) — 전략 달성의 핵심 성공 요인]
    │
    ▼
[KPI (Key Performance Indicator) — CSF를 수치로 측정하는 지표]
    │
    ▼
[OKR (Objectives & Key Results) → 피드백 루프 → 전략 수정]
```
KPI는 CSF를 정량화한 측정 기준으로, BSC의 4관점과 연계하여 전략 목표 달성 여부를 실시간으로 추적하는 성과 관리 도구다.""",
        "child": """🎯 **목표 과녁**: KPI는 조직이 이번 달 목표를 얼마나 달성했는지 알려주는 숫자예요. "이번 달 고객 만족도 90점 이상"처럼 구체적인 숫자로 목표를 세워요!  
📊 **성적 칠판**: 선생님이 칠판에 시험 점수를 써놓는 것처럼, KPI는 회사의 점수를 모두가 볼 수 있게 보여줘서 "잘 되고 있나?" 한눈에 알게 해줘요!  
🔄 **피드백 고리**: 점수가 낮으면 왜 낮은지 찾아서 고치고, 또 측정하고 — 이 반복이 회사를 점점 더 잘 되게 만드는 힘이에요!""",
    },
    "13_cloud_architecture/01_virtualization/018_Type_2_하이퍼바이저.md": {
        "flow": """```text
[물리 서버 (Bare-metal) — 단일 OS, 하드웨어 독점]
    │
    ▼
[Type 1 하이퍼바이저 (Bare-metal Hypervisor) — 하드웨어 직접 제어, 고성능]
    │
    ▼
[Type 2 하이퍼바이저 (Hosted Hypervisor) — 호스트 OS 위 앱으로 구동]
    │
    ▼
[컨테이너 (Container) — OS 커널 공유, 경량 격리, Docker/Kubernetes]
    │
    ▼
[서버리스 (Serverless) — 인프라 추상화, 함수 단위 실행]
```
Type 2 하이퍼바이저는 호스트 OS 위에서 애플리케이션처럼 동작하여 개발·테스트 환경에 적합하지만, 호스트 OS 오버헤드로 인해 프로덕션보다 개인용·학습용에 활용된다.""",
        "child": """🖥️ **컴퓨터 안의 컴퓨터**: Type 2 하이퍼바이저는 내 컴퓨터(윈도우) 안에 또 다른 컴퓨터(가상 머신)를 만들어 주는 프로그램이에요. 컴퓨터 한 대로 여러 OS를 써볼 수 있어요!  
🎮 **게임 에뮬레이터**: 옛날 게임기 게임을 지금 컴퓨터에서 돌리는 에뮬레이터처럼, Type 2 하이퍼바이저도 다른 OS 환경을 흉내 내줘요!  
🐢 **느린 대신 편리함**: Type 1(서버용)보다 느리지만 그냥 프로그램처럼 쉽게 설치할 수 있어요. 개발자가 집 컴퓨터에서 리눅스 테스트할 때 딱 좋아요!""",
    },
    "14_data_engineering/01_infrastructure/018_mapreduce.md": {
        "flow": """```text
[단일 서버 배치 처리 — 데이터 증가에 따른 확장 한계]
    │
    ▼
[HDFS (Hadoop Distributed File System) — 분산 저장, 블록 복제]
    │
    ▼
[맵리듀스 (MapReduce) — Map(분산 필터링) → Shuffle → Reduce(집계)]
    │
    ▼
[YARN (Yet Another Resource Negotiator) — 클러스터 자원 관리]
    │
    ▼
[아파치 스파크 (Apache Spark) — 인메모리 처리, MapReduce 10~100× 속도]
```
MapReduce는 대용량 데이터를 Map-Shuffle-Reduce 3단계로 분산 처리하는 프레임워크로, HDFS와 결합하여 Hadoop 생태계의 핵심 연산 엔진이 된다.""",
        "child": """🗺️ **지도 그리기 (Map)**: 맵리듀스에서 Map은 거대한 데이터를 조각으로 나눠서 각 컴퓨터에 하나씩 나눠주는 것이에요. 마치 긴 소설을 여러 명이 나눠 읽는 것처럼요!  
🔀 **뒤섞기 (Shuffle)**: 같은 주제(단어)끼리 모이도록 섞는 단계예요. "사과"를 읽은 모든 컴퓨터가 "사과" 담당 컴퓨터에게 결과를 모아주는 거예요!  
➕ **합산 (Reduce)**: 마지막으로 같은 그룹을 하나로 합산해요. "사과가 몇 번 나왔지?"를 모든 조각에서 더하면 답이 나와요!""",
    },
    "15_devops_sre/01_culture_methodology/018_admin_processes.md": {
        "flow": """```text
[12 팩터 앱 (12-Factor App) — 클라우드 네이티브 개발 원칙 12가지]
    │
    ▼
[일회성 작업 (One-off Tasks) — DB 마이그레이션·스크립트·seed 데이터]
    │
    ▼
[관리 프로세스 (Admin Processes) — 서비스와 동일한 릴리스·환경에서 실행]
    │
    ▼
[컨테이너 오케스트레이션 (Kubernetes Job) — 일회성 작업 격리·추적 자동화]
    │
    ▼
[GitOps — 관리 작업 코드화, PR 기반 이력 관리, 자동 롤백]
```
관리 프로세스는 12팩터의 마지막 원칙으로, 운영 스크립트를 서비스와 동일한 코드·환경에서 실행하여 "내 PC에서는 됐는데" 오류를 근본적으로 차단한다.""",
        "child": """🔧 **집 청소 도구**: 관리 프로세스는 앱을 운영하면서 가끔 해야 하는 청소(DB 마이그레이션, 데이터 초기화) 같은 일이에요. 청소 도구도 평소 생활 도구와 같은 규칙으로 관리해요!  
🏠 **같은 집에서**: 청소(관리 작업)를 할 때도 평소에 사는 집(같은 코드, 같은 환경)에서 해야 해요. 다른 집(다른 환경)에서 하면 나중에 원래 집에서 문제가 생겨요!  
📜 **기록 남기기**: GitOps처럼 모든 관리 작업을 코드로 남겨두면, 나중에 "언제 누가 무슨 청소를 했는지" 다시 볼 수 있어요!""",
    },
}

FLOWS4 = {
    "16_bigdata/01_intro/018_data_sovereignty.md": {
        "flow": """```text
[개인정보 규정 (GDPR / CCPA) — 데이터 보호 법제화, 국경 초월 적용]
    │
    ▼
[데이터 현지화 (Data Localization) — 자국 데이터 자국 서버 보관 의무]
    │
    ▼
[데이터 주권 (Data Sovereignty) — 국가 관할권, 데이터 흐름 통제 권한]
    │
    ▼
[멀티 리전 아키텍처 (Multi-region) — 국가별 클라우드 리전 분리 배포]
    │
    ▼
[데이터 레지던시 (Data Residency) / 소버린 클라우드 (Sovereign Cloud)]
```
데이터 주권은 국가가 자국 데이터에 대한 관할권을 주장하는 개념으로, 클라우드 아키텍처는 멀티 리전과 소버린 클라우드로 이에 대응한다.""",
        "child": """🌍 **나라마다 다른 규칙**: 데이터 주권은 각 나라가 "우리 국민의 데이터는 우리 땅에 있어야 해!"라고 주장하는 권리예요. 유럽, 미국, 한국 모두 규칙이 달라요!  
📦 **창고 위치 규정**: 한국 고객 데이터를 미국 서버에 저장하면 안 되는 나라도 있어요. 마치 한국 우편물은 한국 우체국에 보관해야 하는 것처럼요!  
☁️ **나라별 클라우드**: 그래서 큰 클라우드 회사들은 나라마다 따로 서버(리전)를 만들어요. 데이터가 해당 나라 밖으로 나가지 않도록요!""",
    },
    "16_bigdata/02_hadoop/018_apache_flume.md": {
        "flow": """```text
[로그 파일 (Log Files) — 서버·애플리케이션 이벤트 기록, 분산 생성]
    │
    ▼
[아파치 플룸 (Apache Flume) — Source→Channel→Sink 파이프라인 수집]
    │
    ▼
[HDFS / HBase — 플룸 싱크(Sink) 대상, 대용량 저장]
    │
    ▼
[아파치 카프카 (Apache Kafka) — 고처리량 스트리밍, 플룸의 현대적 대안]
    │
    ▼
[스트림 처리 (Stream Processing: Flink·Spark Streaming) — 실시간 분석]
```
Apache Flume은 Source-Channel-Sink 아키텍처로 분산된 로그를 HDFS로 안정적으로 전송하며, 현재는 Kafka와 혼용되거나 대체되고 있다.""",
        "child": """🚿 **물 파이프라인**: 플룸(Flume)은 여러 곳에서 나오는 로그 데이터(물)를 파이프(Channel)로 모아 큰 저장소(HDFS)까지 보내주는 물 배관 시스템이에요!  
🔌 **Source→Channel→Sink**: 수도꼭지(Source)에서 나온 물이 파이프(Channel)를 타고 흘러서 수영장(Sink)에 모이는 것처럼 로그가 흘러요!  
📨 **우편 배달부**: 플룸은 수백 개의 서버에서 오는 로그 메시지를 하나도 잃지 않고 HDFS 창고까지 안전하게 배달해주는 전문 배달부예요!""",
    },
    "16_bigdata/03_spark/018_skew_join.md": {
        "flow": """```text
[조인 연산 (Join Operation) — 분산 환경, 파티션 단위 병렬 처리]
    │
    ▼
[데이터 쏠림 (Data Skew) — 특정 키에 데이터 집중, 일부 태스크 지연]
    │
    ▼
[솔팅 기법 (Salting) — 키에 임의 접미사 추가, 파티션 분산]
    │
    ▼
[브로드캐스트 조인 (Broadcast Join) — 소형 테이블 전체 복제·전송]
    │
    ▼
[AQE (Adaptive Query Execution) — 런타임 파티션 재분배 자동화]
```
Skew Join은 데이터 쏠림으로 인한 특정 파티션 과부하를 솔팅·브로드캐스트·AQE로 완화하여 Spark 조인 성능을 균등하게 분산시킨다.""",
        "child": """⚖️ **무거운 한쪽**: 데이터 쏠림은 저울 한쪽에만 물건이 잔뜩 쌓인 것처럼, 컴퓨터 한 대에만 일이 몰려서 다른 컴퓨터들이 기다리는 문제예요!  
🧂 **소금 뿌리기 (Salting)**: 솔팅은 무거운 데이터에 소금처럼 작은 번호(접미사)를 붙여서 여러 컴퓨터에 골고루 나눠주는 방법이에요. 무거운 짐을 조각내는 거예요!  
📡 **작은 테이블은 복사**: 한 테이블이 아주 작으면 모든 컴퓨터에 복사본을 보내는(브로드캐스트) 것이 더 빨라요. 마치 교실 전체에 유인물을 나눠주는 것처럼요!""",
    },
    "16_bigdata/04_streaming/018_azure_event_hubs.md": {
        "flow": """```text
[이벤트 소스 (Event Sources) — IoT·앱·클릭스트림, 초당 수백만 이벤트]
    │
    ▼
[아파치 카프카 (Apache Kafka) — 오픈소스 고처리량 메시지 스트리밍]
    │
    ▼
[Azure Event Hubs — Kafka 호환, 완전 관리형 이벤트 스트리밍 서비스]
    │
    ▼
[Azure Stream Analytics — 실시간 SQL 쿼리 처리, 창 집계(Window)]
    │
    ▼
[Azure Synapse Analytics / Power BI — 배치 분석 및 시각화 대시보드]
```
Azure Event Hubs는 Apache Kafka 호환 API를 제공하며, 완전 관리형 서비스로 대규모 이벤트를 수집하여 Azure 분석 파이프라인의 진입점 역할을 한다.""",
        "child": """🏟️ **초대형 우체통**: Event Hubs는 수백만 명이 동시에 메시지를 보내도 모두 받을 수 있는 초대형 우체통이에요. 카카오톡 서버처럼 엄청 많은 메시지를 처리해요!  
🎡 **컨베이어 벨트**: 도착한 이벤트들이 컨베이어 벨트처럼 순서대로 흘러서 분석 시스템으로 전달돼요. 순서가 중요한 실시간 데이터 처리에 딱 맞아요!  
☁️ **관리 필요 없음**: Azure가 알아서 관리해줘서 서버 설치나 유지보수 없이 이벤트를 받을 수 있어요. 카프카보다 설치가 훨씬 쉬워요!""",
    },
    "16_bigdata/05_analysis/018_ner.md": {
        "flow": """```text
[자연어 처리 (NLP, Natural Language Processing) — 텍스트 분석 기반]
    │
    ▼
[형태소 분석 (Morphological Analysis) — 단어 분리·품사 태깅]
    │
    ▼
[개체명 인식 (NER, Named Entity Recognition) — 인물·장소·조직·날짜 추출]
    │
    ▼
[관계 추출 (Relation Extraction) — 개체 간 의미 관계 파악]
    │
    ▼
[지식 그래프 (Knowledge Graph) — 개체·관계 네트워크, 검색 엔진·AI 기반]
```
NER은 비정형 텍스트에서 의미 있는 개체(인물·장소·조직 등)를 식별하여 관계 추출과 지식 그래프 구축의 핵심 전처리 단계를 담당한다.""",
        "child": """🔍 **중요 단어 찾기**: NER은 뉴스 기사에서 "삼성전자", "서울", "이재용" 같은 중요한 이름(개체)을 자동으로 찾아서 표시해주는 기술이에요!  
🏷️ **라벨 붙이기**: 찾은 단어에 "회사", "도시", "사람" 같은 라벨을 붙여요. 마치 물건에 가격표를 붙이는 것처럼, 컴퓨터가 단어의 종류를 이해하도록 해줘요!  
🌐 **지식 지도 만들기**: NER로 찾은 개체들을 연결하면 "삼성전자(회사)의 대표는 이재용(사람), 본사는 서울(도시)"처럼 지식 지도(Knowledge Graph)가 만들어져요!""",
    },
    "16_bigdata/06_nosql/018_consistency_levels.md": {
        "flow": """```text
[CAP 이론 (CAP Theorem) — 일관성·가용성·분할 허용성 트레이드오프]
    │
    ▼
[강한 일관성 (Strong Consistency) — 모든 노드 즉시 동기화, 지연 증가]
    │
    ▼
[결과적 일관성 (Eventual Consistency) — 최종 동기화, 성능 우선]
    │
    ▼
[일관성 수준 조정 (Consistency Level Tuning) — Quorum·ONE·ALL 선택]
    │
    ▼
[PACELC 모델 — 네트워크 분할 없을 때도 지연 vs 일관성 트레이드오프]
```
일관성 수준은 CAP 이론의 일관성-가용성 트레이드오프를 운영 환경에서 세분화하여, 쿼리 단위로 강도를 선택할 수 있게 한 NoSQL의 핵심 설정이다.""",
        "child": """⚖️ **빠름 vs 정확함**: 강한 일관성은 모든 친구들이 같은 답을 가질 때까지 기다리는 것이고, 결과적 일관성은 일단 빠르게 답을 주고 나중에 맞추는 거예요!  
📚 **도서관 vs 메모장**: 강한 일관성은 도서관처럼 모든 책이 항상 정확하지만 느리고, 결과적 일관성은 개인 메모장처럼 빠르지만 잠깐 틀릴 수 있어요!  
🎛️ **볼륨 조절**: NoSQL은 쿼리마다 일관성 강도(볼륨)를 조절할 수 있어요. 은행 거래는 볼륨 최대(강한 일관성), 좋아요 카운트는 볼륨 낮게(결과적 일관성)!""",
    },
    "16_bigdata/07_data_lake/018_microsoft_fabric.md": {
        "flow": """```text
[분산 데이터 웨어하우스 (Distributed DW) — 구조화 데이터, SQL 중심]
    │
    ▼
[데이터 레이크 (Data Lake) — 비정형·반정형 포함, 스키마 온 리드]
    │
    ▼
[Azure Synapse Analytics — DW + Lake 통합, SQL + Spark 혼용]
    │
    ▼
[Microsoft Fabric — OneLake 단일 저장소, 통합 SaaS 분석 플랫폼]
    │
    ▼
[Lakehouse 아키텍처 (Delta Lake / OneLake) — ACID + 분석 통합 표준화]
```
Microsoft Fabric은 OneLake라는 단일 저장소 위에 데이터 엔지니어링·과학·BI를 통합한 SaaS 분석 플랫폼으로, Lakehouse 아키텍처의 완성형이다.""",
        "child": """🏢 **만능 빌딩**: Microsoft Fabric은 데이터 창고, 분석 도구, AI까지 한 건물(OneLake)에 다 넣은 만능 빌딩이에요. 여러 앱을 따로 쓸 필요가 없어요!  
🔗 **하나로 연결**: 예전에는 데이터 저장, 분석, 시각화 도구가 따로따로였는데, Fabric은 이걸 하나로 묶어줘요. 마치 스위스 군용 칼처럼요!  
📊 **Power BI 연결**: Fabric에 데이터를 넣으면 Power BI 대시보드로 바로 볼 수 있어요. 데이터가 도착하면 바로 그래프로 그려지는 마법 같아요!""",
    },
    "16_bigdata/10_governance/018_data_deidentification_techniques.md": {
        "flow": """```text
[개인정보 (PII, Personally Identifiable Information) — 식별 가능한 원본 데이터]
    │
    ▼
[비식별화 (De-identification) — 직접 식별자 제거 / 간접 식별자 가공]
    │
    ▼
[마스킹 (Masking) / 가명처리 (Pseudonymization) / 집계화 (Aggregation)]
    │
    ▼
[차분 프라이버시 (Differential Privacy) — 통계 노이즈 추가, 수학적 보장]
    │
    ▼
[프라이버시 강화 기술 (PET, Privacy-Enhancing Technology) — 합성 데이터·연합학습]
```
데이터 비식별화는 마스킹·가명처리·집계화의 기법을 결합하여 개인정보를 보호하고, 차분 프라이버시와 PET로 발전하며 데이터 활용과 프라이버시 보호를 동시에 달성한다.""",
        "child": """🙈 **이름 가리기 (마스킹)**: 마스킹은 주민번호의 일부를 ****로 가리는 것처럼, 중요한 정보를 별표로 숨겨서 누구인지 모르게 해요!  
🎭 **가면 쓰기 (가명처리)**: 가명처리는 "홍길동"을 "김철수"로 바꾸는 것처럼, 실제 이름 대신 가짜 이름을 쓰는 방법이에요. 분석은 할 수 있지만 진짜 누구인지는 몰라요!  
🔢 **숫자로 합치기 (집계화)**: 개인 데이터 대신 "20대 여성이 평균 3만원을 썼다"처럼 여러 명의 데이터를 합쳐서 하나의 통계로 만들면 개인을 식별할 수 없어요!""",
    },
}

def insert_flow_section(filepath, flow_text, child_text=None, map_text=None):
    """Insert flow section between 📌 and 👶 sections, or add all missing sections."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if flow already exists
    if '📈 관련 키워드 및 발전 흐름도' in content:
        print(f"SKIP (already has flow): {filepath}")
        return False
    
    flow_section = f"\n### 📈 관련 키워드 및 발전 흐름도\n\n{flow_text}\n"
    
    # Pattern 1: Has both 📌 and 👶 sections (### or ##)
    patterns_to_try = [
        (r'(### 📌 관련 개념 맵[^\n]*\n)', r'(### 👶 어린이를 위한 3줄 비유 설명)'),
        (r'(### 📌 관련 개념 맵\n)', r'(### 👶 어린이를 위한 3줄 비유 설명)'),
        (r'(## 📌 관련 개념 맵[^\n]*\n)', r'(## 👶 어린이를 위한 3줄 비유 설명)'),
    ]
    
    for p1, p2 in patterns_to_try:
        match1 = re.search(p1, content)
        match2 = re.search(p2, content)
        if match1 and match2 and match1.start() < match2.start():
            # Find where the 📌 section ends and 👶 section begins
            insert_pos = match2.start()
            new_content = content[:insert_pos] + flow_section + content[insert_pos:]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"INSERTED (between 📌 and 👶): {filepath}")
            return True
    
    # Pattern 2: Has concept map section but different heading, and no 👶
    # For shell_sort: insert before ## 참고
    ref_match = re.search(r'\n## 참고\n', content)
    if ref_match and child_text:
        child_section = f"### 👶 어린이를 위한 3줄 비유 설명\n\n{child_text}\n\n"
        if map_text:
            map_section = f"\n### 📌 관련 개념 맵\n\n{map_text}\n\n"
            insert_block = map_section + flow_section + child_section
        else:
            insert_block = flow_section + child_section
        
        insert_pos = ref_match.start()
        new_content = content[:insert_pos] + "\n" + insert_block + content[insert_pos:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"INSERTED (before ## 참고): {filepath}")
        return True
    
    # Pattern 3: No tail sections at all - append at end
    if child_text:
        child_section = f"\n### 👶 어린이를 위한 3줄 비유 설명\n\n{child_text}\n"
        if map_text:
            map_section = f"\n### 📌 관련 개념 맵\n\n{map_text}\n"
            append_block = map_section + flow_section + child_section
        else:
            append_block = flow_section + child_section
        new_content = content.rstrip() + "\n\n---\n" + append_block
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"APPENDED (at EOF): {filepath}")
        return True
    
    print(f"FAILED (no match): {filepath}")
    return False


all_flows = {**FLOWS, **FLOWS2, **FLOWS3, **FLOWS4}

for rel_path, data in all_flows.items():
    filepath = os.path.join(BASE, rel_path)
    insert_flow_section(
        filepath,
        data["flow"],
        child_text=data.get("child"),
        map_text=data.get("map")
    )

print("\nDone!")
