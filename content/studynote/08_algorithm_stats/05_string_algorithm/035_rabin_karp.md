+++
title = "035. 라빈-카프 알고리즘 (Rabin-Karp)"
date = "2026-03-03"
[extra]
categories = "studynote-algorithm"
+++

> **핵심 인사이트**
> 1. Rabin-Karp 알고리즘은 롤링 해시(Rolling Hash)를 이용해 텍스트의 슬라이딩 윈도우 해시값을 O(1)로 갱신하며 패턴을 탐색하는 문자열 매칭 알고리즘이다.
> 2. 해시 충돌(Hash Collision)로 인한 false positive를 처리하기 위해 문자열 직접 비교를 추가하므로, 최악의 경우 O(nm)이 될 수 있지만 평균 O(n+m)이다.
> 3. KMP는 단일 패턴 매칭에 최적, Rabin-Karp는 다중 패턴 동시 매칭(Multi-Pattern Search)과 표절 탐지에 특히 유리하다.

---

## I. 롤링 해시 원리

```
텍스트: T = "abcde"
패턴:   P = "bcd" (길이 m=3)

해시 함수 (다항식 해시):
  hash("bcd") = b*p^2 + c*p^1 + d*p^0 (mod q)
  p: 소수 (예: 31)
  q: 큰 소수 (예: 1e9+7)

슬라이딩 윈도우:
  "abc" 해시 계산 후
  "bcd" = (("abc" - a*p^(m-1)) * p + d) mod q
  -> 이전 해시에서 O(1) 갱신
```

| 단계    | 윈도우 | 해시 갱신              |
|--------|--------|----------------------|
| i=0    | abc    | 초기 계산             |
| i=1    | bcd    | (hash - a*p^2)*p + d |
| i=2    | cde    | (hash - b*p^2)*p + e |

> 📢 **섹션 요약 비유**: 건물을 한 층씩 올릴 때 전체를 다시 짓는 게 아니라, 맨 아래 층을 빼고 위에 새 층을 얹는 것 — O(1) 해시 갱신.

---

## II. 알고리즘 동작

```
함수: Rabin-Karp(T, P)
1. hash_P = hash(P) 계산
2. hash_W = hash(T[0..m-1]) 계산
3. for i = 0 to n-m:
     if hash_W == hash_P:
       if T[i..i+m-1] == P:   // 실제 비교 (충돌 확인)
         매칭 위치 i 반환
     hash_W = rolling_update(hash_W, T[i], T[i+m])
```

### 시간 복잡도

| 경우    | 복잡도 | 설명              |
|--------|--------|------------------|
| 평균    | O(n+m) | 충돌이 적을 때    |
| 최악    | O(nm)  | 해시 충돌이 많을 때|
| 전처리  | O(m)   | 패턴 해시 계산    |

> 📢 **섹션 요약 비유**: 지문 인식처럼 — 지문(해시)이 맞으면 자세히 보고(문자 비교), 다르면 패스. 지문이 비슷해서 가끔 오인식(충돌)이 있다.

---

## III. 다중 패턴 매칭 — Rabin-Karp의 강점

```
단일 패턴: KMP가 더 빠름 (O(n+m))

다중 패턴 (k개):
  KMP: O(n*k + sum(mi))  -> 패턴마다 탐색
  Rabin-Karp: O(n + sum(mi)) -> 한 번의 슬라이딩으로 k개 동시

구현:
  패턴 해시 집합 = {hash(P1), hash(P2), ..., hash(Pk)}
  윈도우 해시가 집합에 있으면 -> 실제 비교
```

> 📢 **섹션 요약 비유**: 여러 범인 사진(패턴)을 한꺼번에 들고 지나가는 사람(텍스트)의 얼굴과 비교 — 한 번 훑으면서 여러 패턴을 동시에 탐색.

---

## IV. Python 구현

```python
def rabin_karp(text, pattern, q=10**9+7, base=31):
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    # 해시 계산
    def hash_str(s):
        h = 0
        for c in s:
            h = (h * base + ord(c)) % q
        return h
    
    pat_hash = hash_str(pattern)
    win_hash = hash_str(text[:m])
    
    # 최고 차항 계수
    high_coef = pow(base, m-1, q)
    
    results = []
    for i in range(n - m + 1):
        if win_hash == pat_hash:
            if text[i:i+m] == pattern:  # 충돌 확인
                results.append(i)
        if i < n - m:
            win_hash = (win_hash - ord(text[i]) * high_coef) % q
            win_hash = (win_hash * base + ord(text[i+m])) % q
    return results
```

> 📢 **섹션 요약 비유**: 해시 계산이 O(1)이니 슬라이딩이 빠르고, 충돌 시만 O(m) 실제 비교 — 두 단계 필터링으로 효율 극대화.

---

## V. 실무 적용 — 표절 탐지

```
문서 표절 탐지 시스템:
1. 원본 문서의 모든 n-gram 해시 저장 (Set)
2. 검사 문서를 슬라이딩 윈도우로 해시
3. 교집합 비율 계산 (Jaccard Similarity)

Jaccard = |A ∩ B| / |A ∪ B|

유사도 80% 이상 -> 표절 의심
```

| 응용 분야     | 설명                         |
|-------------|------------------------------|
| 표절 탐지     | 문서 n-gram 유사도 계산        |
| DNA 서열 분석 | 긴 유전자에서 패턴 탐색        |
| 로그 분석     | 대용량 로그에서 오류 패턴 탐지  |
| 코드 복사 탐지 | GitHub 코드 유사도 분석        |

> 📢 **섹션 요약 비유**: 논문 표절 검사기처럼 — 모든 문장을 하나씩 비교하지 않고, 해시로 빠르게 의심 구간을 좁힌 후 정밀 비교.

---

## 📌 관련 개념 맵

```
Rabin-Karp 알고리즘
+-- 핵심 기술: 롤링 해시 (Rolling Hash)
|   +-- 다항식 해시 (Polynomial Hash)
|   +-- O(1) 윈도우 갱신
|   +-- 해시 충돌 -> 실제 비교 필요
+-- 시간 복잡도
|   +-- 평균 O(n+m)
|   +-- 최악 O(nm) (충돌 다발)
+-- 강점
|   +-- 다중 패턴 동시 매칭
|   +-- 표절 탐지, DNA 분석
+-- 비교
    +-- KMP: 단일 패턴 최적 (O(n+m) 보장)
    +-- Aho-Corasick: 다중 패턴 O(n+m*k)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[단순 문자열 매칭]
Brute Force: O(nm)
      |
      v
[Rabin-Karp (1987, Karp & Rabin)]
롤링 해시: 평균 O(n+m), 다중 패턴 강점
      |
      v
[KMP (1977) / BM (1977)]
최악 O(n+m) 보장, 단일 패턴 최적
      |
      v
[Aho-Corasick (1975)]
다중 패턴 동시 매칭 O(n + 패턴 총 길이)
      |
      v
[현대 응용]
표절 탐지 (TurnItIn)
DNA 시퀀싱 (BLAST)
코드 유사도 (MOSS)
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 라빈-카프는 긴 글에서 단어를 찾을 때 지문(해시)으로 먼저 빠르게 확인해요.
2. 지문이 같으면 그때만 글자를 직접 비교해서, 시간을 많이 아낄 수 있어요.
3. 여러 단어를 동시에 찾아야 할 때 특히 유용한데, 표절 검사기가 이 방법을 써요!
