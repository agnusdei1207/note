+++
title = "039. 접미사 배열 (Suffix Array) + LCP 배열"
date = "2026-03-04"
[extra]
categories = "studynote-algorithm-stats"
+++

> **핵심 인사이트**
> 1. 접미사 배열(Suffix Array)은 문자열의 모든 접미사를 사전순 정렬한 인덱스 배열로, 접미사 트리(Suffix Tree)의 선형 공간 대안으로 문자열 검색·LCP 계산·BWT(Burrows-Wheeler Transform)의 핵심 자료구조다.
> 2. SA(접미사 배열) + LCP(Longest Common Prefix) 배열의 조합이 강력한 이유 — LCP[i]가 SA[i-1]과 SA[i]로 시작하는 접미사의 공통 접두사 길이를 O(1)에 제공하여, 반복 부분문자열 찾기·최장 반복 문자열 등 복잡한 문제를 효율적으로 해결한다.
> 3. SA-IS 알고리즘은 O(n) 시간에 접미사 배열을 구성하는 선형 알고리즘으로, DNA 서열 분석·압축(bzip2의 BWT)·전문 텍스트 검색 엔진의 기반 기술이다.

---

## I. 접미사 배열 개념

```
접미사 (Suffix): 문자열의 특정 위치부터 끝까지

문자열 "banana":
  접미사 목록:
  i=0: banana
  i=1: anana
  i=2: nana
  i=3: ana
  i=4: na
  i=5: a

접미사 배열 (SA): 사전순 정렬된 인덱스
  정렬:
  a       (i=5)
  ana     (i=3)
  anana   (i=1)
  banana  (i=0)
  na      (i=4)
  nana    (i=2)
  
  SA = [5, 3, 1, 0, 4, 2]

공간: O(n) (문자열 자체 + 인덱스 배열)
구성 시간: O(n log n) (기본) / O(n) (SA-IS)
```

> 📢 **섹션 요약 비유**: 접미사 배열은 책의 뒷면 색인처럼 — 모든 단어(접미사)를 알파벳순으로 정렬해 어느 페이지(인덱스)에 있는지 기록.

---

## II. LCP 배열

```
LCP 배열 (Longest Common Prefix Array):

LCP[i] = SA[i-1]로 시작하는 접미사와
          SA[i]로 시작하는 접미사의
          공통 접두사 최대 길이

"banana" SA = [5, 3, 1, 0, 4, 2]:
  SA[0]=5: a
  SA[1]=3: ana    LCP[1] = lcp(a, ana)    = 1
  SA[2]=1: anana  LCP[2] = lcp(ana, anana)= 3
  SA[3]=0: banana LCP[3] = lcp(anana,banana)= 0
  SA[4]=4: na     LCP[4] = lcp(banana, na)= 0
  SA[5]=2: nana   LCP[5] = lcp(na, nana)  = 2
  
  LCP = [0, 1, 3, 0, 0, 2]

Kasai 알고리즘:
  SA로부터 O(n) 시간에 LCP 배열 구성
  (중요한 최적화: 이전 LCP 값 재사용)

최장 반복 부분문자열:
  max(LCP) = 3 -> "ana"가 최장 반복 문자열
```

> 📢 **섹션 요약 비유**: LCP 배열은 사전에서 인접한 두 단어의 공통 접두사 길이 — "apple"과 "apply"는 4글자("appl") 공통.

---

## III. 패턴 매칭 (이진 탐색)

```
SA + 이진 탐색으로 패턴 검색:
  시간: O(m log n)
  (m = 패턴 길이, n = 텍스트 길이)
  
"banana"에서 "ana" 검색:

  SA에서 이진 탐색으로
  "ana"로 시작하는 접미사 범위 찾기:
  
  SA = [5, 3, 1, 0, 4, 2]
  접미사:  a, ana, anana, banana, na, nana
  
  "ana"로 시작하는 범위: [1, 2] (SA[1]=3, SA[2]=1)
  -> "ana"가 위치 3, 1에 존재 (2번 등장)

비교:
  KMP: O(n+m), 단일 패턴
  SA + 이진 탐색: O(m log n + 건수), 여러 패턴
  Aho-Corasick: O(n+m+k), 다중 패턴 동시
  
  대형 텍스트 (전문 검색): SA가 유리
  단일 쿼리: KMP가 단순
```

> 📢 **섹션 요약 비유**: 사전에서 단어 찾기처럼 — 정렬된 접미사 배열에서 이진 탐색으로 패턴 위치를 빠르게 찾음.

---

## IV. BWT와 압축 응용

```
BWT (Burrows-Wheeler Transform, 1994):
  접미사 배열로 구현 가능한 텍스트 변환
  
"banana$" 변환:
  모든 순환 접미사 사전순 정렬
  
  정렬된 순환 접미사:
  $banana  (마지막 문자: a)
  a$banan  (마지막: n)
  ana$ban  (마지막: b)
  anana$b  (마지막: a)
  banana$  (마지막: $)
  na$bana  (마지막: a)
  nana$ba  (마지막: a)
  
  BWT = 마지막 열: "annb$aa"
  
BWT 특성:
  같은 문자가 군집화됨 (압축 효율 증가)
  
  원본: banana$         (무작위 분포)
  BWT: annb$aa          (같은 문자 뭉침)
  
응용:
  bzip2 (BWT + Huffman 압축)
  BWA (DNA 서열 매핑)
  FM-Index (생물정보학 탐색)
```

> 📢 **섹션 요약 비유**: BWT는 책의 문자를 재배열해서 같은 글자끼리 모아주기 — 압축 프로그램이 반복 문자를 더 쉽게 압축할 수 있도록.

---

## V. 실무 시나리오 — DNA 서열 검색

```
BWA (Burrows-Wheeler Aligner) 동작:

배경:
  인간 게놈: 3억 염기쌍 (약 3GB)
  시퀀싱 리드: 수천만 개 (각 150bp)
  목표: 각 리드를 게놈에 정렬 (매핑)
  
구조:
  1. 게놈 인덱싱 (한 번):
     인간 게놈 SA 구성
     FM-Index (BWT + 접미사 배열) 생성
     시간: ~1시간, 메모리: ~3GB
     
  2. 리드 매핑 (반복):
     각 150bp 리드에 대해
     FM-Index에서 이진 탐색
     시간: 리드당 < 1ms
     수천만 리드 -> 수십 분

성능 비교:
  SA 없는 선형 탐색:
    3억 × 수천만 = 수십조 연산 (불가)
  
  SA + FM-Index:
    O(m) 매핑 (m = 리드 길이 150)
    -> 수십 분으로 전체 게놈 분석

실무 명령:
  bwa index genome.fa          # 인덱스 구성
  bwa mem genome.fa reads.fq   # 매핑
```

> 📢 **섹션 요약 비유**: 게놈 인덱싱은 3억 페이지 사전의 색인 만들기 — 색인 없이 찾으면 수백 년, 색인 있으면 수십 분.

---

## 📌 관련 개념 맵

```
접미사 배열 + LCP
+-- 자료구조
|   +-- SA (사전순 정렬 접미사 인덱스)
|   +-- LCP 배열 (인접 접미사 공통 접두사)
+-- 구성 알고리즘
|   +-- O(n log n): 기본 정렬 기반
|   +-- O(n): SA-IS 알고리즘
|   +-- Kasai: LCP 배열 O(n) 구성
+-- 응용
|   +-- 패턴 매칭 (이진 탐색)
|   +-- 최장 반복 문자열
|   +-- BWT (압축, DNA 매핑)
+-- 관련 도구
    +-- bzip2 (BWT), BWA (게놈)
    +-- Elasticsearch (역색인)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[접미사 트리 (Weiner, 1973)]
O(n) 공간 but 상수 계수 큼
      |
      v
[접미사 배열 (Manber & Myers, 1990)]
접미사 트리의 공간 효율적 대안
      |
      v
[BWT (Burrows & Wheeler, 1994)]
bzip2 압축 기반
      |
      v
[SA-IS 알고리즘 (Nong, 2009)]
O(n) 선형 SA 구성
      |
      v
[현재: FM-Index + NGS]
차세대 유전체 분석의 핵심
BWA, Bowtie2 기반
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 접미사 배열은 "banana"의 모든 꼬리말("banana", "anana", "nana", "ana", "na", "a")을 알파벳순으로 정렬해서 빠른 검색을 가능하게 하는 인덱스예요.
2. LCP 배열은 정렬된 꼬리말들 중 인접한 두 개가 앞에서 몇 글자 일치하는지 기록해서 "가장 많이 반복되는 부분"을 빠르게 찾을 수 있어요.
3. DNA 분석 도구(BWA)가 수억 개 염기서열에서 150글자 조각을 수십 분 만에 찾는 것이 바로 접미사 배열 기반 인덱싱 덕분이에요!
