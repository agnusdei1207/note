+++
title = "038. 편집 거리 (Edit Distance / Levenshtein Distance)"
date = "2026-03-03"
[extra]
categories = "studynote-algorithm-stats"
+++

> **핵심 인사이트**
> 1. 편집 거리(Edit Distance)는 한 문자열을 다른 문자열로 변환하는 데 필요한 최소 편집 연산(삽입·삭제·교체) 횟수로, 두 문자열의 유사성을 정량화하는 핵심 지표다.
> 2. DP 점화식: `dp[i][j]` = s1[0..i]를 s2[0..j]로 변환하는 최소 비용 — 같으면 `dp[i-1][j-1]`, 다르면 삽입/삭제/교체 중 최솟값 + 1 — LCS와 유사하지만 모든 위치에서 삽입·삭제·교체 세 가지를 고려한다는 차이가 있다.
> 3. 편집 거리는 맞춤법 교정(spell checker), 생물정보학 서열 정렬, 자연어 처리의 문장 유사도 계산, OCR 후처리, 퍼지 문자열 매칭 등 실무 전반에 핵심 알고리즘으로 활용된다.

---

## I. 편집 연산 정의

```
Levenshtein Distance (Vladimir Levenshtein, 1965):

허용 연산 (비용 각 1):
  1. 삽입 (Insertion): 문자 하나 추가
  2. 삭제 (Deletion): 문자 하나 제거
  3. 교체 (Substitution): 문자 하나 다른 것으로 교체

예: "kitten" -> "sitting"
  kitten
  -> sitten (k->s 교체)
  -> sittin (e->i 교체)
  -> sitting (g 삽입)
  편집 거리: 3

변형:
  Hamming Distance: 같은 길이 문자열, 교체만
  Damerau-Levenshtein: 인접 문자 교환도 허용
  Jaro-Winkler: 짧은 문자열 유사도 특화
```

> 📢 **섹션 요약 비유**: 편집 거리는 낱말 퍼즐처럼 "cat"을 "dog"으로 만들기 위한 최소 변경 횟수 — c->d, a->o, t->g = 3번.

---

## II. DP 점화식

```
dp[i][j] = s1[0..i-1]을 s2[0..j-1]로 변환하는 최소 비용

초기화:
  dp[i][0] = i (s1의 i글자 -> 빈 문자열: i번 삭제)
  dp[0][j] = j (빈 문자열 -> s2의 j글자: j번 삽입)

점화식:
  if s1[i-1] == s2[j-1]:
    dp[i][j] = dp[i-1][j-1]  (교체 불필요)
  else:
    dp[i][j] = 1 + min(
      dp[i-1][j],    # 삭제 (s1에서 문자 제거)
      dp[i][j-1],    # 삽입 (s2 문자 추가)
      dp[i-1][j-1]   # 교체
    )

예: "ab" vs "bc"
    ""  b  c
 ""  0  1  2
 a   1  1  2
 b   2  1  2

편집 거리: dp[2][2] = 2
  (a 삭제, c 삽입)
```

> 📢 **섹션 요약 비유**: DP 테이블의 각 칸은 "지금까지 쓴 글자로 여기까지 도달하는 최소 편집 횟수" — 오른쪽(삽입), 아래쪽(삭제), 대각선(교체).

---

## III. LCS와의 관계

```
편집 거리와 LCS의 수학적 관계:

편집 거리(s1, s2)
  = len(s1) + len(s2) - 2 * LCS(s1, s2)

설명:
  LCS 이외의 문자들 = 편집이 필요한 부분
  s1에서 LCS 아닌 것: 삭제
  s2에서 LCS 아닌 것: 삽입
  
예: s1="ABCB" (4), s2="BCB" (3)
  LCS = "BCB" (3)
  편집 거리 = 4 + 3 - 2*3 = 1
  (A 삭제 1번)

단, 이는 삽입/삭제만 허용하는 경우
교체 포함 Levenshtein Distance는 다를 수 있음

Levenshtein <= LCS 기반 편집 거리
  (교체 1 vs 삭제+삽입 2이므로)
```

> 📢 **섹션 요약 비유**: LCS는 "공통으로 남길 것 최대화", 편집 거리는 "변경할 것 최소화" — 수학적으로 같은 문제의 두 가지 관점.

---

## IV. 실무 응용

```
1. 맞춤법 교정 (Spell Checker):
   "teh" -> 사전에서 편집 거리 1인 단어 검색
   "the" (거리 1), "ten" (거리 2)
   -> 가장 가까운 단어로 수정 제안

2. 생물정보학 서열 정렬:
   Smith-Waterman, Needleman-Wunsch
   편집 거리의 가중치 변형 (갭 패널티)

3. NLP 유사도:
   두 짧은 텍스트의 편집 거리 / 최대 길이
   = 정규화 편집 유사도 (0~1)
   
4. OCR 후처리:
   인식된 텍스트 "H3llo" -> "Hello" (거리 1)
   가장 가까운 사전 단어로 보정

5. Git diff + 병합:
   파일 병합 시 충돌 감지
   Myers diff 알고리즘 활용
   
6. 퍼지 검색 (Fuzzy Search):
   ElasticSearch의 fuzziness 파라미터
   편집 거리 기반 검색 결과 확장
```

> 📢 **섹션 요약 비유**: 맞춤법 교정기는 "가장 비슷한 단어"를 편집 거리로 측정 — 1~2번 바꾸면 되는 단어 목록 중 가장 흔한 것을 제안.

---

## V. 실무 시나리오 — ElasticSearch 퍼지 검색

```
사용자가 "자바스크맆트"로 검색:
  -> "자바스크립트"와 편집 거리: 1 (맆->립)

ElasticSearch 쿼리:
  {
    "query": {
      "fuzzy": {
        "title": {
          "value": "자바스크맆트",
          "fuzziness": 1
        }
      }
    }
  }

내부 동작:
  편집 거리 <= 1인 모든 변형 생성
  BK-Tree (Burkhard-Keller Tree):
    편집 거리 기반 인덱스 구조
    O(log n) 퍼지 검색

성능:
  fuzziness: 0 = 정확 매칭
  fuzziness: 1 = 오타 1개 허용 (권장)
  fuzziness: 2 = 오타 2개 허용 (검색 범위 너무 넓어짐 주의)

실무 팁:
  AUTO fuzziness: 길이 기반 자동 설정
    <= 2자: 0 (오타 허용 X)
    3-5자: 1 (오타 1개)
    >= 6자: 2 (오타 2개)
```

> 📢 **섹션 요약 비유**: ElasticSearch 퍼지 검색은 "오타 1개까지는 원하는 결과 보여주기" — 편집 거리가 검색 엔진의 친절함을 수치로 정의.

---

## 📌 관련 개념 맵

```
편집 거리 (Edit Distance)
+-- 연산
|   +-- 삽입, 삭제, 교체
|   +-- Damerau: 인접 교환 추가
+-- 관련 알고리즘
|   +-- LCS (편집 거리와 수학적 관계)
|   +-- Myers diff (파일 비교 최적화)
|   +-- Smith-Waterman (생물정보학)
+-- 응용
    +-- 맞춤법 교정, OCR 후처리
    +-- NLP 문장 유사도
    +-- ElasticSearch 퍼지 검색
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[Levenshtein Distance (1965)]
삽입/삭제/교체 3연산 정의
      |
      v
[DP 구현 보편화 (1970s)]
O(mn) 표준 알고리즘
      |
      v
[맞춤법 교정기 (1980s)]
Peter Norvig의 spell corrector
      |
      v
[생물정보학 활용 (1990s)]
Needleman-Wunsch, Smith-Waterman
      |
      v
[현재: NLP + 퍼지 검색]
ElasticSearch fuzziness
BM25 + 편집 거리 하이브리드
LLM 임베딩 유사도와 병용
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 편집 거리는 "cat"을 "car"로 바꾸려면 t->r 1번만 바꾸면 되니까 거리 1이에요 — 두 단어가 얼마나 비슷한지 숫자로 나타내는 방법이에요.
2. DP 테이블은 각 칸마다 "지금까지의 글자들로 여기까지 오려면 최소 몇 번 편집했는가"를 기록한 체크리스트예요.
3. 검색창에 오타를 쳐도 원하는 결과가 나오는 이유가 바로 편집 거리 알고리즘이 "가장 비슷한 단어"를 찾아주기 때문이에요!
