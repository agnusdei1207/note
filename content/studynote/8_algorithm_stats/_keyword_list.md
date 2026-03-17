+++
title = "08. 알고리즘/자료구조/통계 키워드 목록"
date = "2026-03-03"
[extra]
categories = "studynote-algorithm"
+++

# 알고리즘 / 자료구조 / 통계 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 알고리즘·자료구조·통계 전 영역 핵심 키워드

+++

## 1. 알고리즘 기초 — 14개

1. 알고리즘 (Algorithm) 정의 — 유한성/확정성/입력/출력/효율성
2. 시간 복잡도 (Time Complexity) — Big-O / Ω / Θ 표기법
3. 공간 복잡도 (Space Complexity)
4. O(1) / O(log n) / O(n) / O(n log n) / O(n²) / O(2ⁿ) / O(n!)
5. 분할 정복 (Divide and Conquer) — 재귀 분할 + 병합
6. 탐욕 알고리즘 (Greedy Algorithm) — 지역 최적 → 전체 최적
7. 동적 프로그래밍 (Dynamic Programming) — 최적 부분구조 + 중복 부분 문제
8. 메모이제이션 (Memoization) — Top-Down DP
9. 타뷸레이션 (Tabulation) — Bottom-Up DP
10. 백트래킹 (Backtracking) — 가지치기
11. 분기 한정 (Branch and Bound) — 최적화 탐색
12. 근사 알고리즘 (Approximation Algorithm) — NP 문제
13. 랜덤화 알고리즘 (Randomized Algorithm) — Las Vegas / Monte Carlo
14. 재귀 (Recursion) — 기본 사례, 재귀 사례, 스택 오버플로우

+++

## 2. 정렬 알고리즘 — 18개

15. 버블 정렬 (Bubble Sort) — O(n²), 안정, 제자리
16. 선택 정렬 (Selection Sort) — O(n²), 불안정, 제자리
17. 삽입 정렬 (Insertion Sort) — O(n²)/O(n) 최선, 안정, 소규모 효율
18. 셸 정렬 (Shell Sort) — 삽입 정렬 개선, O(n^1.5)
19. 합병 정렬 (Merge Sort) — O(n log n), 안정, O(n) 공간
20. 퀵 정렬 (Quick Sort) — 평균 O(n log n), 최악 O(n²), 불안정
21. 퀵 정렬 최적화 — 3-way Partition, Median-of-3 Pivot
22. 힙 정렬 (Heap Sort) — O(n log n), 불안정, 제자리
23. 계수 정렬 (Counting Sort) — O(n+k), 비교 불필요
24. 기수 정렬 (Radix Sort) — O(d·n), 고정 자릿수
25. 버킷 정렬 (Bucket Sort) — O(n) 평균, 균등 분포
26. 팀 정렬 (Timsort) — Python/Java 기본, 합병+삽입 혼합
27. 인트로 정렬 (Introsort) — 퀵+힙+삽입 혼합, C++ STL
28. 정렬 안정성 (Stability) — 동일 키 순서 유지 여부
29. 외부 정렬 (External Sort) — 대용량 데이터, 멀티웨이 합병
30. 정렬 비교 — 시간/공간/안정성/적합 환경
31. 네트워크 정렬 (Sorting Network) — 병렬 정렬
32. 이분 탐색 (Binary Search) — O(log n), 정렬된 배열 필수

+++

## 3. 탐색 / 그래프 알고리즘 — 24개

33. 선형 탐색 (Linear Search) — O(n)
34. 이진 탐색 (Binary Search) — O(log n)
35. 해시 탐색 (Hash Search) — O(1) 평균
36. 그래프 표현 — 인접 행렬 / 인접 리스트
37. DFS (Depth-First Search) — 깊이 우선, 스택/재귀
38. BFS (Breadth-First Search) — 너비 우선, 큐, 최단 경로(비가중)
39. 다익스트라 (Dijkstra) — 단일 출발 최단 경로, 비음수 가중치
40. 벨만-포드 (Bellman-Ford) — 음수 가중치 허용, O(VE)
41. 플로이드-워샬 (Floyd-Warshall) — 전체 쌍 최단 경로, O(V³)
42. A* 알고리즘 — 휴리스틱, 최단 경로
43. 위상 정렬 (Topological Sort) — DAG, Kahn's / DFS 기반
44. 강연결 요소 (SCC) — Kosaraju / Tarjan 알고리즘
45. 최소 신장 트리 (MST) — Kruskal / Prim
46. 크루스칼 (Kruskal) — 간선 정렬 + Union-Find
47. 프림 (Prim) — 정점 기반, 우선순위 큐
48. 최대 유량 (Max Flow) — Ford-Fulkerson / Edmonds-Karp
49. 이분 매칭 (Bipartite Matching) — 헝가리안 알고리즘
50. 유니온-파인드 (Union-Find / Disjoint Set) — 경로 압축, 랭크
51. 최소 컷 (Min Cut) — Max-Flow Min-Cut 정리
52. 오일러 경로/회로 — Fleury / Hierholzer
53. 해밀턴 경로 — NP-완전, 백트래킹
54. 외판원 문제 (TSP) — NP-hard, DP+비트마스크
55. 최장 공통 부분수열 (LCS) — DP, O(mn)
56. 최장 증가 부분수열 (LIS) — DP / 이진 탐색

+++

## 4. 자료구조 — 28개

57. 배열 (Array) — 연속 메모리, O(1) 랜덤 접근
58. 연결 리스트 (Linked List) — 단일/이중/순환, 동적 삽입/삭제
59. 스택 (Stack) — LIFO, push/pop, 재귀/DFS/수식 평가
60. 큐 (Queue) — FIFO, enqueue/dequeue, BFS/스케줄링
61. 덱 (Deque, Double-Ended Queue) — 양방향 큐
62. 우선순위 큐 (Priority Queue) — 힙 기반 구현
63. 힙 (Heap) — 최대/최소 힙, 완전 이진 트리
64. 이진 트리 (Binary Tree) — 전위/중위/후위 순회
65. 이진 탐색 트리 (BST) — O(log n) 평균, O(n) 최악
66. AVL 트리 — 높이 균형, 회전 (LL/RR/LR/RL)
67. 레드-블랙 트리 (Red-Black Tree) — O(log n) 보장, Java TreeMap
68. B-트리 (B-Tree) — 다진 탐색, 디스크 기반, 균형
69. B+트리 (B+Tree) — 리프 연결, DB 인덱스
70. 트라이 (Trie) — 접두사 탐색, 자동 완성
71. 해시 테이블 (Hash Table) — 해시 함수, 충돌 처리
72. 개방 주소법 (Open Addressing) — 선형/이차/이중 해싱
73. 체인법 (Chaining) — 연결 리스트 충돌 처리
74. 그래프 (Graph) — 방향/무방향, 가중/비가중
75. 세그먼트 트리 (Segment Tree) — 구간 쿼리/업데이트
76. 펜윅 트리 / BIT (Binary Indexed Tree / Fenwick Tree) — 구간 합
77. 압축된 트라이 (Compressed Trie / Patricia Trie)
78. 서픽스 트리 (Suffix Tree) / 서픽스 배열 (Suffix Array)
79. 해시맵 (HashMap) vs 트리맵 (TreeMap) — 순서 유무
80. 스킵 리스트 (Skip List) — 확률적 균형, O(log n)
81. 유니온-파인드 (Union-Find) — 집합 연산
82. 단조 스택 (Monotonic Stack/Queue)
83. 스파스 테이블 (Sparse Table) — O(1) 구간 최소값 (RMQ)
84. 블룸 필터 (Bloom Filter) — 확률적 집합 멤버십, 공간 효율

+++

## 5. 문자열 알고리즘 — 12개

85. KMP (Knuth-Morris-Pratt) — 패턴 매칭, 실패 함수
86. 보이어-무어 (Boyer-Moore) — 역방향 비교, 실용적 최적
87. 라빈-카프 (Rabin-Karp) — 롤링 해시, 다중 패턴
88. Z 알고리즘 — 접두사 매칭 배열
89. 아호-코라식 (Aho-Corasick) — 다중 패턴 동시 매칭
90. 런-길이 인코딩 (RLE) — 압축, 연속 반복
91. 허프만 코딩 (Huffman Coding) — 가변길이 최적 코드
92. LZ77 / LZ78 / LZW — 사전 기반 압축 (ZIP, GIF)
93. 최장 공통 부분수열 (LCS) — 문자열 비교
94. 편집 거리 (Edit Distance, Levenshtein Distance) — DP
95. 정규 표현식 (Regex) — NFA/DFA, 패턴 매칭
96. 접미사 배열 + LCP 배열 — 문자열 분석

+++

## 6. NP 이론 / 계산 이론 — 14개

97. P 클래스 — 다항 시간 내 해결 가능
98. NP 클래스 — 다항 시간 내 검증 가능
99. NP-완전 (NP-Complete) — NP 중 가장 어려운 문제
100. NP-어려움 (NP-Hard) — NP보다 어렵거나 동등
101. P = NP 문제 — 미해결 난제
102. 다항 시간 환산 (Polynomial Reduction)
103. SAT (Satisfiability) — 최초 NP-완전 증명 (Cook-Levin)
104. 클리크 문제 (Clique Problem) — NP-완전
105. 정점 커버 (Vertex Cover) — NP-완전
106. 외판원 문제 (TSP) — NP-hard
107. 배낭 문제 (Knapsack Problem) — NP-완전 (결정 버전)
108. 근사 알고리즘 — ρ-근사, FPTAS, PTAS
109. 지수 시간 가설 (ETH) — 알고리즘 하한 도구
110. 양자 복잡도 (Quantum Complexity) — BQP, 양자 우위

+++

## 7. 수치 알고리즘 — 10개

111. 유클리드 호제법 (Euclidean Algorithm) — GCD, O(log min)
112. 에라토스테네스의 체 (Sieve of Eratosthenes) — 소수 판별
113. 소수 판별 (Primality Test) — Miller-Rabin (확률적)
114. 거듭제곱 (Fast Exponentiation) — 분할 정복, O(log n)
115. 중국인의 나머지 정리 (CRT)
116. 가우스 소거법 (Gaussian Elimination) — 연립방정식
117. FFT (Fast Fourier Transform) — 다항식 곱, O(n log n)
118. 행렬 곱셈 (Matrix Multiplication) — Strassen O(n^2.81)
119. 뉴턴-랩슨 (Newton-Raphson) — 수치 해법, 제곱근
120. 몬테카를로 수치적분 — 확률적 근사

+++

## 8. 확률 / 통계 기초 — 20개

121. 확률 (Probability) — 고전/상대도수/주관 확률
122. 베이즈 정리 (Bayes' Theorem) — P(A|B) = P(B|A)P(A)/P(B)
123. 조건부 확률 (Conditional Probability)
124. 독립 사건 (Independence) / 상호 배타적 사건
125. 확률 변수 (Random Variable) — 이산/연속
126. 기댓값 (Expected Value, E[X])
127. 분산 (Variance) / 표준편차 (Standard Deviation)
128. 확률 분포 — 이항/포아송/정규/지수/균등
129. 정규 분포 (Normal Distribution) — 68-95-99.7 규칙
130. 중심 극한 정리 (Central Limit Theorem, CLT)
131. 마르코프 체인 (Markov Chain) — 전이 확률, 정상 분포
132. 마르코프 성질 (Markov Property) — 미래 ⊥ 과거 | 현재
133. 기대치 최대화 (Expectation-Maximization, EM 알고리즘)
134. 최대 우도 추정 (MLE, Maximum Likelihood Estimation)
135. 베이즈 추정 (Bayesian Estimation) — MAP (최대 사후 확률)
136. 가설 검정 (Hypothesis Testing) — 귀무/대립 가설, p-value
137. 신뢰 구간 (Confidence Interval)
138. 카이제곱 검정 (Chi-Square Test) — 독립성 검정
139. t-검정 / F-검정 / ANOVA
140. 회귀 분석 (Regression Analysis) — 단순/다중/로지스틱

+++

## 9. 정보이론 — 10개

141. 정보이론 (Information Theory) — Shannon, 1948
142. 엔트로피 (Shannon Entropy) — H(X) = -Σ p·log₂p
143. 상호 정보량 (Mutual Information)
144. KL 다이버전스 (KL Divergence) — 분포 간 차이
145. 크로스 엔트로피 (Cross-Entropy) — 분류 손실 함수
146. 채널 용량 (Channel Capacity) — 샤논 용량 공식
147. 소스 부호화 정리 (Source Coding Theorem)
148. 채널 부호화 정리 (Channel Coding Theorem) — Shannon Limit
149. 오류 정정 부호 (Error Correcting Code) — 해밍/(터보)/LDPC/폴라
150. 압축 (Compression) — 무손실/손실, 허프만/LZ/웨이블릿

+++

## 10. 선형대수 / 최적화 — 10개

151. 선형 연립방정식 — 행렬 표현, 가우스 소거
152. 행렬 분해 — LU / QR / SVD (Singular Value Decomposition)
153. 고유값 / 고유벡터 (Eigenvalue/Eigenvector)
154. PCA (Principal Component Analysis) — SVD 기반 차원 축소
155. 볼록 함수 (Convex Function) — 전역 최적 보장
156. 기울기 하강법 (Gradient Descent) — 최적화 기본
157. 라그랑주 승수법 (Lagrange Multiplier) — 제약 최적화
158. 선형 프로그래밍 (LP) — 심플렉스법
159. 정수 프로그래밍 (IP) — 분기 한정, MILP
160. 진화 알고리즘 — 유전 알고리즘 (GA), 입자 군집 최적화 (PSO)

+++

**총 키워드 수: 160개**
