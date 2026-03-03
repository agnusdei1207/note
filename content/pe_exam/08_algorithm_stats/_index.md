+++
title = "8. 알고리즘/통계"
description = "자료구조, 알고리즘 설계, 복잡도 분석, 통계 기초, 데이터 분석"
sort_by = "title"
weight = 8
+++

# 제8과목: 알고리즘 / 통계

알고리즘 설계 기법과 자료구조, 통계의 핵심 개념을 다룹니다.

## 핵심 키워드

### 알고리즘 기초
- [복잡도 분석(Complexity Analysis)](algorithm/complexity.md) - 시간/공간 효율성 이론적 분석
  - **시간 복잡도(Time Complexity)**: 연산 횟수의 입력 크기 n에 대한 함수
    - **점근 표기법(Asymptotic Notation)**:
      - **O(f(n)) (Big-O)**: 상한(Upper Bound), 최악의 경우 증가율
      - **Ω(f(n)) (Big-Omega)**: 하한(Lower Bound), 최선의 경우 증가율
      - **Θ(f(n)) (Big-Theta)**: 평균(Average), 상한=하한 동시 성립
    - **복잡도 계층(Complexity Hierarchy)**: O(1) < O(log n) < O(√n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)
      | 함수 | 예시 | 설명 |
      |------|------|------|
      | O(1) | 배열 인덱스 접근, 상수 시간 |
      | O(log n) | 이진 탐색 | 로그 시간, 분할 정복 |
      | O(√n) | BFS 최단 경로 | 그래프 탐색 |
      | O(n) | 선형 탐색, 전체 스캔 |
      | O(n log n) | 퀵/병합/힙 정렬 | 비교 기반 정렬 하한 |
      | O(n²) | 버블/선택/삽입 정렬 | 2중 루프 |
      | O(n³) | Floyd-Warshall | 3중 루프 그래프 |
      | O(2ⁿ) | 부분집합 생성 | 완전 탐색(Brute Force) |
      | O(n!) | 순열/외판원(TSP) | 조합 최적화 |
  - **공간 복잡도(Space Complexity)**: 메모리 사용량
    - **보조 공간(Auxiliary Space)**: 입력 제외 추가 메모리
    - **In-place**: O(1) 추가 공간 (예: 힙 정렬)
    - **공간-시간 트레이드오프**: 메모리↑ ↔ 속도↑ (예: 해시 테이블, DP)
  - **분할 상환 분석(Amortized Analysis)**: 평균 시간 복잡도 (연산 시퀀스 기준)
    - 예: 동적 배열 평균 삽입 O(1) (재할당 O(n) 드물게 발생)
- [최선/평균/최악 분석](algorithm/complexity.md) - 시나리오별 복잡도
  - **Best Case(Ω)**: 가장 유리한 입력, 예: 정렬된 배열→버블 정렬 O(n)
  - **Average Case(Θ)**: 무작위 입력, 평균 수행 시간
  - **Worst Case(O)**: 가장 불리한 입력  예: 역정렬→퀵 정렬 O(n²)
  - **복잡도 분석 예시**:
    | 알고리즘 | 최선(Ω) | 평균(Θ) | 최악(O) | 공간 |
    |---------|--------|---------|----------|------|
    | 퀵 정렬 | O(n log n) | O(n log n) | O(n²) | O(log n) |
    | 병합 정렬 | O(n log n) | O(n log n) | O(n log n) | O(n) |
    | 힙 정렬 | O(n log n) | O(n log n) | O(n log n) | O(1) |
    | 이진 탐색 | O(1) | O(log n) | O(log n) | O(1) |
- [정렬(Sorting)](algorithm/sorting.md) - 데이터 순서 배열
  - **비교 기반 정렬(Comparison Sort)**: 원소 간 비교→순서 결정, 하한 O(n log n)
    - **버블 정렬(Bubble)**: 인접 쌍 교환, O(n²), Stable, In-place
    - **선택 정렬(Selection)**: 최소값 선택→교환, O(n²), Unstable, In-place
    - **삽입 정렬(Insertion)**: 적절 위치 삽입, O(n²), Stable  Online(Almost sorted 시 O(n))
    - **퀵 정렬(Quick)**: 피벗 분할→재귀 정렬, O(n log n) avg, O(n²) worst, Unstable
      - 피벗 선택: First/Median-of-Three/Random
      - 분할 로직: Lomuto(간단)/Hoare(효율적)
    - **병합 정렬(Merge)**: 분할→정렬→병합  O(n log n), Stable, O(n) 공간
    - **힙 정렬(Heap)**: 힙 구성→루트 제거→재구성  O(n log n), Unstable, In-place
  - **안정 정렬(Stable Sort)**: 동일 값 상대적 순서 유지
    - Stable: 버블/삽입/병합/계수/버킷
    - Unstable: 퀵/선택/힙
  - **비비교 정렬(Non-comparison Sort)**: O(n+k), 선형 시간 가능
    - **계수 정렬(Counting)**: 빈도수 계산, O(n+k), k=최댓값], 정수만, Stable
    - **기수 정렬(Radix)**: 자릿수별 정렬  O(d·(n+k)), LSD/MSD, Stable
    - **버킷 정렬(Bucket)**: 균등 분포 가정  O(n+k), 각 버킷→별도 정렬
 Stable
  - **외부 정렬(External Sort)**: 메모리 초과 대용량 정렬
    - **k-way 병합**: k개 정렬된 파일→병합, k-way Merge
    - **외부 병합 정렬(External Merge Sort)**: 디스크 기반 병합
    - **대체 선택(Replacement Selection)**: 메모리 내 상위 k개 유지
- [탐색(Search)](algorithm/searching.md) - 데이터 검색
  - **선형 탐색(Linear Search)**: 순차 스캔  O(n), 비정렬 가능, 구현 단순
  - **이진 탐색(Binary Search)**: 중간값 비교→반 좁혁 O(log n), 정렬 필수
    - **변형**: Lower Bound(첫 위치)/Upper Bound(마지막 위치)
  - **해시 탐색(Hash Search)**: 해시 함수→인덱스 O(1) avg, O(n) worst
  - **보간 탐색(Interpolation Search)**: 균등 분포 가정 O(log log n), 이진 탐색 변형
  - **이진 탐색 트리(BST) 탐색**: O(log n) avg  O(n) worst (편향 시)
  - **이진 탐색 응용**:
    - **Parametric Search**: 파라미터 공간 탐색, 최적화
    - **Ternary Search**: 삼분 탐색, 함수 최대/최소
- [재귀(Recursion)](algorithm/recursion.md) - 자기 참조 함수
  - **구조**: Base Case(종료 조건) + Recursive Case(재귀 호출) + Stack Frame
  - **메모이제이션(Memoization)**: Top-Down, 재귀+캐시, 중복 계산 방지
  - **타뷸레이션(Tabulation)**: Bottom-Up  반복문  DP 테이블
  - **꼬리 재귀(Tail Recursion)**: 재귀 호출이 마지막 연산  최적화 가능 (Python 미지원)
  - **재귀 깊이**: 최대 호출 스택 깊이  Stack Overflow 위험
  - **시간 복잡도 분석**: T(n) = T(n-1) + T(n-2) → 피보나치 O(1.618ⁿ)
- [역색인(Inverted Index)](inverted_index.md) - 전문 검색 엔진 핵심
  - **구조**: Term → Posting List(문서 ID 목록)
  - **토큰화(Tokenization)**: 텍스트→단어 분리, 형태소 분석
  - **정규화(Normalization)**: 소문자 변환  어근 추출(Stemming)/표제어 추출(Lemmatization)
  - **불용어(Stop Words)**: the/a/is 등 제거
  - **TF-IDF**: tf(t,d) * idf(t) = tf(t,d) * log(N/df(t))
    - TF(Term Frequency): 단어 빈도
    - IDF(Inverse Document Frequency): 희소성 가중치
  - **BM25**: TF-IDF 개선, 가중치 포화, 희소성 완화
  - **색인 구조**: Forward Index(문서→단어) vs Inverted Index(단어→문서)
  - **구현**: Elasticsearch(Lucene)/Solr/Meilisearch

### 알고리즘 설계 기법
- [분할 정복](algorithm/divide_conquer.md) - 분할(Divide)/정복(Conquer)/결합(Combine), 퀵 정렬/병합 정렬/이진 탐색/카라추바(빠른 곱셈), 재귀적 구조
- [동적 프로그래밍](algorithm/dynamic_programming.md) - 최적 부분 구조(Optimal Substructure)/중복 부분 문제(Overlapping Subproblems), 메모이제이션(재귀)/타뷸레이션(반복), 피보나치/최단 경로
- [DP 응용](algorithm/dynamic_programming.md) - 배낭 문제(0-1/분할)/LCS(최장 공통 부분 수열)/LIS(최장 증가 부분 수열)/편집 거리(Levenshtein), 최적화 문제
- [탐욕 알고리즘](algorithm/greedy.md) - 그리디 선택 속성(Greedy Choice)/최적 부분 구조, 허프만 코딩/크루스칼/프림/다익스트라, 지역 최적→전역 최적 보장X
- [백트래킹](algorithm/backtracking.md) - 상태 공간 트리, N-Queens/부분집합/순열/미로 찾기, 가지치기(Pruning), 깊이 우선 탐색 기반
- [Branch and Bound](algorithm/backtracking.md) - 분기 한정, TSP(외판원 문제) 최적화, 하한(Upper Bound)/상한(Lower Bound), 프루닝 강화
- [근사 알고리즘](algorithm/greedy.md) - NP-Hard 문제 근사해 탐색, 근사 비율(Approximation Ratio), TSP(Christofides 1.5), 다항 시간
- [랜덤화 알고리즘](algorithm/sorting.md) - 무작위 퀵 정렬(피벗 무작위)/몬테카를로(확률적)/라스베가스(항상 정확), 평균 성능 보장

### 그래프 알고리즘
- [그래프 기초(Graph Fundamentals)](algorithm/graph.md) - 정점(Vertex)/간선(Edge)/가중치(Weight)
  - **그래프 표현 방식**:
    | 표현 | 공간 복잡도 | 간선 존재 확인 | 적합 상황 |
    |------|-----------|---------------|---------|
    | **인접 행렬(Adjacency Matrix)** | O(V²) | O(1) | 밀집 그래프 |
    | **인접 리스트(Adjacency List)** | O(V+E) | O(degree) | 희소 그래프 |
    | **간선 리스트(Edge List)** | O(E) | O(E) | 간선 중심 처리 |
  - **그래프 순회(Graph Traversal)**:
    - **DFS(깊이 우선 탐색)**: 스택/재귀, 경로 탐색, 사이클 탐지, 위상 정렬
    - **BFS(너비 우선 탐색)**: 큐, 최단 경로(비가중치), 레벨 순회
  - **그래프 유형**:
    - 방향 vs 무방향
    - 가중치 vs 비가중치
    - 연결 vs 비연결
    - 사이클 vs 비순환(DAG)
    - 이분(Bipartite)/완전(Complete)/평면(Planar)
- [위상 정렬(Topological Sort)](algorithm/topological_sort.md) - DAG 순서 결정
  - **Kahn 알고리즘**: 진입 차수(Indegree) 기반
    - 시간 복잡도: O(V+E)
    - 과정: 진입 차수 0인 정점 큐에 추가 → 제거 → 인접 정점 진입 차수 감소 → 반복
    - 사이클 탐지: 큐 비기 전 순서에 정점 남음 → 사이클 존재
  - **DFS 기반 위상 정렬**:
    - 과정: DFS 수행 → 종료 시점 역순 저장 → 역순 = 위상 순서
    - 스택 사용: 재귀 호출 종료 시점 푸시
  - **응용**: 작업 스케줄링(의존성), 컴파일러(모듈 로딩), Makefile 처리
- [최단 경로(Shortest Path)](algorithm/shortest_path.md) - 가중 그래프 경로 최적화
  - **단일 출발 최단 경로(SSSP)**:
    - **다익스트라(Dijkstra)**: 음수 간선 X, 우선순위 큐, O(E log V)
      - 탐욕적 선택, 거리 갱신→Relaxation 반복
      - 시간 복잡도: O(E log V) with binary heap  O(E + V log V) with Fibonacci heap
    - **벨만-포드(Bellman-Ford)**: 음수 간선 O, O(VE)
      - 모든 간선 Relaxation V-1회 반복
      - 음수 사이클 탐지: V번째 반복 시 추가 갱신→음수 사이클 존재
    - **SPFA(Shortest Path Faster Algorithm)**: 벨만-포드 개선, 평균 O(E), 최악 O(VE)
  - **전쌍 최단 경로(APSP)**:
    - **플로이드-와샬(Floyd-Warshall)**: 동적 계획법, O(V³)
      - 3중 루프: k 거쳐, 중간 정점
      - 공식: D[i][j] = min(D[i][j], D[i][k] + D[k][j])
      - 음수 사이클: 대각선 D[i][i] < 0 → 음수 사이클
    - **존슨(Johnson)**: 다익스트라+벨만포드, O(V² log V + VE)
      - 재가중치(Johnson's Reweighting) 후 다익스트라 V번
  - **최단 경로 트리(Shortest Path Tree)**: 이전 노드(prev) 저장으로 경로 복원
- [최소 신장 트리(MST)](mst.md) - 연결 그래프 최소 가중치 트리
  - **크루스칼(Kruskal)**: 간선 중심, 욕심적 선택
    - 과정: 간선 가중치 정렬 → 사이클 형성 검사(Union-Find) → MST 간선 추가
    - 시간 복잡도: O(E log E) = O(E log V) (정렬 지배)
    - Union-Find 최적화: 경로 압축(Path Compression) + Union by Rank
  - **프림(Prim)**: 정점 중심, 성장
    - 과정: 임의 정점 시작 → 연결된 최소 가중치 간선 선택 → 확장
    - 시간 복잡도: O(E log V) with binary heap, O(E + V log V) with Fibonacci heap
    - 우선순위 큐 사용: 연결된 간선 중 최소 가중치
  - **MST 유일성**: 모든 가중치가 다르면 MST 유일
  - **응용**: 네트워크 설계, 클러스터링, 회로 배선
- [강연결 요소(SCC, Strongly Connected Components)](algorithm/graph.md) - 상호 도달 가능
  - **코사라주(Kosaraju)**: 2번 DFS
    - 1단계: DFS로 종료 시점 역순 기록
    - 2단계: 전치(Transpose) 그래프에서 역순 기록 순서로 DFS
    - 시간 복잡도: O(V+E)
  - **타잔(Tarjan)**: 1번 DFS  dfsnum/low 이용
    - 스택 기반 DFS: 방문 중인 정점 추적
    - Low-link 값velope: 역방향 간선 통해 도달 가능한 최소 깊이
    - 시간 복잡도: O(V+E)
  - **응용**: 2-SAT, 링크 분석  도달 가능성 분석
- [이분 그래프(Bipartite Graph)](algorithm/graph.md) - 2색 분할 가능
  - **판별**: BFS/DFS로 2색 칠하기, 인접 정점 다른 색
  - **이분 매칭(Bipartite Matching)**: 최대 매칭 찾기
  - **Hungarian 알고리즘(할당 문제)**: 가중치 최대 매칭  O(V³)
  - **Hopcroft-Karp**: 이분 매칭 최적화, O(E√V)
  - **응용**: 작업 할당  결혼 문제  스케줄링
- [네트워크 플로우(Network Flow)](algorithm/graph.md) - 유량 네트워크
  - **최대 유량 문제(Max Flow)**: 소스→싱크 최대 유량
  - **포드-풀커슨(Ford-Fulkerson)**: DFS 기반 증가 경로
    - 시간 복잡도: O(E·f), f=최대 유량 (정수 유량)
    - 과정: 증가 경로 탐색→유량 흐름→반복
  - **에드몬즈-카프(Edmonds-Karp)**: BFS 기반 최단 증가 경로
    - 시간 복잡도: O(VE²)
    - BFS로 최단 증가 경로 탐색→성능 보장
  - **최소 컷(Min Cut)**: 소스-싱크 분리, 최소 용량
    - Max-Flow Min-Cut 정리: 최대 유량 = 최소 컷 용량
  - **Dinic**: 레벨 그래프+차단 유량  O(V²E) 또선, O(E√V) 이분
  - **응용**: 파이프라인 용량  교통 흐름  매칭 최적화
- [문자열 알고리즘(String Algorithms)](algorithm/string.md)
  - **패턴 매칭(Pattern Matching)**:
    - **KMP(Knuth-Morris-Pratt)**: 접두사 함수(Prefix Function) π 배열
      - 시간 복잡도: O(n+m), n=텍스트 길이, m=패턴 길이
      - π[i] = 패턴[0..i-1]의 접두사=접미사 최대 일치 길이
      - 불일치 시 π 활용 건너뜰기
    - **라빈-카프(Rabin-Karp)**: 해시 기반, 평균 O(n+m)
      - 롤링 해시(Rolling Hash): 윈도우 이동 시 O(1) 해시 갱신
      - 충돌 시: 실제 문자열 비교
    - **아호-코라식(Aho-Corasick)**: 다중 패턴 매칭
      - Trie 기반: 모든 패턴 Trie 구성
      - 시간 복잡도: O(n + m + z), z=매칭 수
  - **접미사 배열(Suffix Array)**: 정렬된 접미사 인덱스
    - 공간: O(n), 접미사 트리 대비 효율적
    - LCP 배열: 최장 공통 접두사
    - 활용: 문자열 검색, 반복 부분 문자열 찾기
  - **트라이(Trie)**: 문자열 트리, 검색/삽입 O(m)
- [정수론(Number Theory)](algorithm/number_theory.md)
  - **소수 판정**: 에라토스테네스 체(Sieve of Eratosthenes) O(n log log n)
  - **최대공약수(GCD)**: 유클리드 호제법(Euclidean Algorithm) O(log(min(a,b)))
    - 확장 유클리드: ax + by = gcd(a,b)
  - **모듈러 산술(Modular Arithmetic)**:
    - 덧셈: (a + b) mod n = ((a mod n) + (b mod n)) mod n
    - 곱셈: (a × b) mod n = ((a mod n) × (b mod n)) mod n
    - 거듭제곱: a^b mod n = O(log b) (이진 거득제곱)
  - **페르마 소정리**: a^(p-1) ≡ 1 (mod p), 소수 판정
  - **오일러 파이(Euler's Totient)**: φ(n) = n과 서로소인 수
  - **중국인 나머지 정리(CRT)**: 연립 핼동식식 mod m 해
  - **밀러-라빈(Miller-Rabin)**: 소수 판정 확률적 알고리즘

### 자료구조
- [배열/연결 리스트](data_structure/tree.md) - 배열(인덱스 접근 O(1), 삽입삭제 O(n))/연결 리스트(순차 접근 O(n), 삽입삭제 O(1)), 동적 배열(ArrayList/Vector)
- [스택/큐/덱](data_structure/tree.md) - 스택(LIFO, 후입선출)/큐(FIFO, 선입선출)/덱(양방향), 응용: 괄호 검사/함수 호출/BFS
- [트리](data_structure/tree.md) - 이진 트리/이진 탐색 트리(BST, 중위 순회 시 정렬)/AVL(균형 인수)/레드-블랙 트리(색상, 회전), 순회(전위/중위/후위)
- [B-Tree / B+Tree](data_structure/b_tree.md) - 디스크 기반 탐색, 차수(Degree), 노드 분할/병합, DB 인덱스 구조, B+Tree(리프 연결)
- [힙 (Heap)](data_structure/heap.md) - 최대 힙/최소 힙, 완전 이진 트리, 삽입/삭제 O(log n), 힙 정렬/우선순위 큐
- [그래프](data_structure/graph.md) - 인접 행렬(O(V²) 공간)/인접 리스트(O(V+E) 공간)/간선 리스트, 가중치/방향 표현
- [최소 신장 트리](mst.md) - Union-Find(서로소 집합, 경로 압축/Union by Rank), 크루스칼/프림 알고리즘 기반
- [해시 테이블](data_structure/hash.md) - 해시 함수(나눗셈/곱셈)/충돌 해결(체이닝/개방 주소법-선형/이차/더블 해싱), 적재율(Load Factor)
- [확장성 해싱 (Extendible Hashing)](data_structure/hash.md) - 동적 확장 해시 구조, 디렉토리/버킷, 데이터베이스 인덱스, 오버플로우 처리
- [트라이 (Trie)](data_structure/trie.md) - 접두사 트리(Prefix Tree), 문자열 검색 O(m)/자동완성/사전, 공간 복잡도 vs 검색 속도
- [세그먼트 트리](data_structure/advanced.md) - 구간 쿼리(합/최소/최대), O(log n) 구간 연산/갱신, 레이지 전파(Lazy Propagation)
- [삭제 가능 우선순위 큐](data_structure/heap.md) - 피보나치 힙(O(1) 감소 키)/이항 힙/쌍힙(Pairing Heap), 다익스트라 최적화
- [고급 자료구조](data_structure/advanced.md) - 블룸 필터(확률적 집합)/스킵 리스트(확률적 균형)/최소 비용 힙, 특수 목적 최적화

### 통계 기초
- [기술 통계](statistics/statistics_basics.md) - 중심 경향(평균/중앙값/최빈값), 산포도(분산/표준편차/사분위수 범위), 왜도(Skewness)/첨도(Kurtosis)
- [추론 통계](statistics/statistics_basics.md) - 점 추정(Point Estimation)/구간 추정(Confidence Interval), 불편 추정량(Unbiased Estimator), 모집단→표본
- [확률 기초](statistics/probability_basics.md) - 확률 공리(Kolmogorov)/조건부 확률 P(A|B)/베이즈 정리 P(A|B) = P(B|A)P(A)/P(B), 독립 사건
- [확률 분포](statistics/distributions.md) - 정규분포(N(μ,σ²), 68-95-99.7규칙)/이항분포(n,p)/포아송 분포(λ)/균등분포/지수분포, PDF/PMF/CDF
- [샘플링](statistics/sampling.md) - 단순임의/층화(Stratified)/계통(Systematic)/군집(Cluster) 표본추출, 중심극한정리(CLT), 표본 오차
- [가설 검증](statistics/hypothesis_testing.md) - 귀무가설(H₀)/대립가설(H₁), 유의수준(α, 0.05/0.01)/p-value/1종 오류(α)/2종 오류(β), 검정력(1-β)
- [t-검정](statistics/hypothesis_testing.md) - 단일 표본/독립 두 표본/대응(Paired) t-검정, Student's t-분포, 자유도(df), 정규성 가정
- [카이제곱 검정](statistics/hypothesis_testing.md) - 적합도(Goodness-of-Fit)/동질성/독립성 검정, χ² 분포, 범주형 데이터, 기대 빈도
- [분산 분석 (ANOVA)](statistics/anova.md) - 일원(One-Way)/이원(Two-Way) 분산 분석, F-검정, 집단 간/집단 내 분산, 사후 검정(Tukey/Bonferroni)
- [상관 분석](statistics/correlation.md) - 피어슨(Pearson, 선형)/스피어만(Spearman, 순위)/켄달(Kendall, 순위) 상관계수, 결정 계수(R²)
- [회귀 분석](statistics/regression.md) - 단순/다중 선형 회귀, OLS(최소 제곱법), 로지스틱 회귀(분류), VIF(다중공선성), 잔차 분석
- [시계열 분석](statistics/regression.md) - ARIMA(자기회귀 누적 이동평균)/계절 분해/지수 평활, 추세/계절성/불규칙, ACF/PACF
- [베이즈 통계](statistics/bayes_theorem.md) - 사전 확률(Prior)/사후 확률(Posterior)/가능도(Likelihood), 베이즈 추론, 나이브 베이즈 분류기

### 알고리즘 응용 (AI/ML 연계)
- [군집 알고리즘](statistics/hypothesis_testing.md) - K-Means(중심 기반)/계층적 군집(덴드로그램)/DBSCAN(밀도 기반), 실루엣 계수
- [차원 축소](statistics/regression.md) - PCA(주성분 분석, 분산 최대화)/t-SNE(시각화)/UMAP(속도+품질), 저주의 차원(Curse of Dimensionality)
- [ROC/PR 곡선](xai_statistics.md) - ROC(Receiver Operating Characteristic)/PR(Precision-Recall), AUC(Area Under Curve), 임계값 선택
- [XAI 통계 기법](xai_statistics.md) - SHAP(SHapley Additive exPlanations)/LIME(Local Interpretable Model-agnostic), 특성 중요도
- [최적화](algorithm/dynamic_programming.md) - 선형 계획법(LP, Simplex)/경사 하강법(GD, SGD)/수치 최적화, Convex/Non-convex
- [정보 이론](algorithm/number_theory.md) - 엔트로피(H)/상호 정보량(MI)/KL 발산, 허프만 부호화, 데이터 압축, Shannon(1948)

### 계산 이론 / 복잡도 클래스
- [P/NP 문제](algorithm/complexity.md) - P(다항 시간 해결 가능)/NP(다항 시간 검증 가능)/NP-Complete/NP-Hard, P=NP? 미해결
- [NP-완전 문제](algorithm/complexity.md) - SAT(충족 가능성)/3-SAT/외판원 문제(TSP)/배낭 문제/그래프 채색, 다항 시간 환원
- [알고리즘 병렬화](algorithm/complexity.md) - 병렬 알고리즘, 암달의 법칙(Amdahl's Law, 이론적 한계)/구스타프손 법칙(Gustafson's Law, 실제 확장), PRAM
