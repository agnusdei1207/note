+++
title = "036. 아호-코라식 (Aho-Corasick) 알고리즘"
date = "2026-03-03"
weight = 36
[extra]
categories = "studynote-algorithm-stats"
+++

> **핵심 인사이트**
> 1. 아호-코라식(Aho-Corasick) 알고리즘은 KMP의 실패 함수 개념을 트라이(Trie) 자료구조에 결합해, 텍스트를 한 번만 스캔하면서 여러 패턴을 동시에 탐색하는 다중 패턴 매칭 알고리즘이다.
> 2. 핵심은 트라이에 실패 링크(Failure Link)와 출력 링크(Output Link)를 추가해 오토마톤(AC Automaton)으로 변환하는 것 — 미스매치 시 처음으로 돌아가지 않고 가장 길게 일치하는 상태로 이동한다.
> 3. 시간복잡도 O(n + m + z) [n=텍스트, m=전체 패턴 길이, z=매칭 횟수]로 수천~수만 개의 패턴을 텍스트에서 동시 탐색하는 IDS·바이러스 스캐너·검색 시스템에서 핵심 알고리즘이다.

---

## I. 동기 — 다중 패턴 문제

```
문제 상황:
  텍스트: "he said she searched for them"
  패턴들: ["he", "she", "his", "hers"]
  
  순진한 방법: KMP를 4번 각각 실행
    시간복잡도: O(n * k) (k=패턴 수)
    패턴 1,000개 -> 텍스트를 1,000번 스캔?

아호-코라식:
  1번 스캔으로 모든 패턴 동시 탐색
  시간복잡도: O(n + m + z)
```

> 📢 **섹션 요약 비유**: KMP로 영어·중국어·일어를 각각 사전에서 찾는 것 vs 아호-코라식으로 한 번의 눈 이동으로 세 언어를 동시에 발견하는 것.

---

## II. 트라이 + 실패 링크 = AC 오토마톤

```
패턴: ["he", "she", "his", "hers"]

1. 트라이 구성:
        root
       / | \ \
      h  s  (다른 문자)
      |  |
      e  h
     /|  |
    * r  e
      |  |
      s  *
      |
      *

2. BFS로 실패 링크(Failure Link) 설정:
   실패 링크 = 현재 접두사의 최장 진접미사가 있는 상태
   
   예: "he"의 실패 링크 -> "e"가 있는 상태로
       "she"의 실패 링크 -> "he"로

3. 출력 링크(Output Link):
   실패 링크를 따라가다 매칭되는 패턴이 있으면 출력
```

| 구성 요소         | 역할                                    |
|----------------|----------------------------------------|
| 트라이           | 모든 패턴을 단어 사전으로 압축              |
| 실패 링크         | KMP 실패 함수의 트라이 확장판              |
| 출력 링크         | 실패 링크 체인에 포함된 패턴 출력           |

> 📢 **섹션 요약 비유**: 실패 링크는 GPS 재경로 — 길이 막히면 처음 출발지로 돌아가지 않고, 갈 수 있는 가장 가까운 우회로로 이동.

---

## III. 시간복잡도 분석

```
1. 트라이 구성: O(m)  (m = 전체 패턴 문자 수)
2. 실패 링크 구성 (BFS): O(m * |Sigma|)
3. 텍스트 스캔: O(n + z)
   n = 텍스트 길이
   z = 총 매칭 횟수

전처리: O(m * |Sigma|) ~ O(m * 알파벳 크기)
쿼리:   O(n + z)

vs 다른 알고리즘:
  KMP x k패턴: O(n*k + m)
  아호-코라식: O(n + m + z) -- 압도적 우위
```

> 📢 **섹션 요약 비유**: 전처리(트라이+실패링크)는 지도 그리기, 텍스트 스캔은 지도 보며 목적지 찾기 — 지도가 있으면 도시 수에 관계없이 한 번에 다 찾는다.

---

## IV. 구현 핵심 로직

```python
from collections import deque

class AhoCorasick:
    def __init__(self, patterns):
        # 트라이 노드: [자식들, 실패, 출력]
        self.goto = [{}]
        self.fail = [0]
        self.output = [[]]
        self._build(patterns)

    def _build(self, patterns):
        # 1. 트라이 구성
        for pat in patterns:
            cur = 0
            for ch in pat:
                if ch not in self.goto[cur]:
                    self.goto[cur][ch] = len(self.goto)
                    self.goto.append({})
                    self.fail.append(0)
                    self.output.append([])
                cur = self.goto[cur][ch]
            self.output[cur].append(pat)

        # 2. BFS로 실패 링크 설정
        q = deque()
        for ch, s in self.goto[0].items():
            q.append(s)  # 깊이 1은 실패 링크 = root

        while q:
            r = q.popleft()
            for ch, s in self.goto[r].items():
                q.append(s)
                f = self.fail[r]
                while f and ch not in self.goto[f]:
                    f = self.fail[f]
                self.fail[s] = self.goto[f].get(ch, 0)
                if self.fail[s] == s:
                    self.fail[s] = 0
                self.output[s] += self.output[self.fail[s]]

    def search(self, text):
        cur = 0
        results = []
        for i, ch in enumerate(text):
            while cur and ch not in self.goto[cur]:
                cur = self.fail[cur]
            cur = self.goto[cur].get(ch, 0)
            for pat in self.output[cur]:
                results.append((i - len(pat) + 1, pat))
        return results
```

> 📢 **섹션 요약 비유**: BFS로 실패 링크를 설정하는 것은 지하철 노선도에서 환승역 미리 표시하기 — 탑승 후에는 막힘없이 원하는 역에 도달.

---

## V. 실무 시나리오 — IDS 패턴 매칭

```
침입 탐지 시스템(IDS):
  네트워크 패킷 스트림에서 수천 개 공격 시그니처 동시 탐색

  패턴 수: 3,000개 (CVE 기반 공격 패킷 특징)
  텍스트:  1Gbps 실시간 트래픽

  KMP * 3000: 실시간 처리 불가 (CPU 100%)
  아호-코라식: 단일 패스로 처리 가능

실제 사용 사례:
  Snort/Suricata (IDS): Aho-Corasick 기반 규칙 엔진
  grep -F (고정 문자열 검색): 내부 AC 알고리즘
  바이러스 스캐너: 악성코드 시그니처 동시 탐색
  검색 엔진: 금지어·광고 필터링
```

> 📢 **섹션 요약 비유**: 공항 보안검색대에서 1,000가지 위험물 목록을 동시에 검색하는 것 — 짐 하나를 1,000번 스캔하는 것이 아니라 한 번에 모두 체크.

---

## 📌 관련 개념 맵

```
아호-코라식 알고리즘
+-- 기반
|   +-- KMP (단일 패턴)
|   +-- 트라이 (Trie 자료구조)
+-- 핵심 구성
|   +-- AC 오토마톤 (DFA)
|   +-- 실패 링크 (Failure Link)
|   +-- 출력 링크 (Output Link)
+-- 시간복잡도
|   +-- 전처리: O(m * 알파벳 크기)
|   +-- 탐색: O(n + z)
+-- 응용
    +-- IDS / 바이러스 스캐너
    +-- 텍스트 검색, 금지어 필터
    +-- 생물정보학 (DNA 시퀀스)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[KMP 알고리즘 (1977)]
단일 패턴 매칭, 실패 함수
      |
      v
[아호-코라식 (Aho & Corasick, 1975)]
다중 패턴, 트라이 + 실패 링크
      |
      v
[DAWG (Directed Acyclic Word Graph)]
메모리 최적화 버전
      |
      v
[비트병렬 알고리즘 (BNDM, Shift-And)]
하드웨어 레벨 최적화
      |
      v
[현재: SIMD + 아호-코라식]
Intel SSE/AVX로 병렬 패턴 매칭
IDS, 바이러스 스캐너 핵심 엔진
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 아호-코라식은 여러 단어를 사전처럼 트리에 저장하고, 텍스트를 한 번만 읽어서 모든 단어를 동시에 찾는 마법 같은 알고리즘이에요.
2. 길이 막히면 처음부터 다시 가지 않고, 미리 그려둔 우회도로(실패 링크)로 바로 이동해서 시간을 절약해요.
3. 악성코드 탐지 프로그램이 바이러스 패턴 수천 개를 한 번에 찾을 때 이 알고리즘을 사용한답니다!
