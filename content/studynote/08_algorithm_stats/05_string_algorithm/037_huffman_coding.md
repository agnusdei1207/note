+++
title = "037. 허프만 코딩 (Huffman Coding)"
date = "2026-03-03"
weight = 37
[extra]
categories = "studynote-algorithm-stats"
+++

> **핵심 인사이트**
> 1. 허프만 코딩(Huffman Coding)은 등장 빈도가 높은 문자에 짧은 비트, 낮은 문자에 긴 비트를 할당하는 최적 접두사 코드(Optimal Prefix Code)로, 우선순위 큐와 이진 트리로 O(n log n)에 구성된다.
> 2. 접두사 코드(Prefix Code) 특성 — 어떤 코드워드도 다른 코드워드의 접두사가 아니므로 구분자 없이 연속된 비트스트림에서 유일하게 디코딩이 가능하며, 이것이 무손실 압축의 핵심이다.
> 3. 허프만 코딩은 단독으로 사용되기보다 ZIP(DEFLATE = LZ77 + Huffman), JPEG(DCT 계수 + Huffman), MP3(MDCTcoefficients + Huffman) 등 거의 모든 압축 표준의 최종 엔트로피 코딩 단계에서 활용된다.

---

## I. 허프만 코딩 원리

```
예시 문자열: "aabbbccddddeeeeee"
  a: 2회, b: 3회, c: 2회, d: 4회, e: 6회

빈도 기반 코드 할당 (허프만 코드):
  e: 00        (6회 × 2비트 = 12비트)
  d: 01        (4회 × 2비트 = 8비트)
  b: 100       (3회 × 3비트 = 9비트)
  a: 101       (2회 × 3비트 = 6비트)
  c: 110       (2회 × 3비트 = 6비트)
  
고정 길이 코드 (3비트 필요):
  17문자 × 3비트 = 51비트
  
허프만 코드:
  12+8+9+6+6 = 41비트 (20% 절감!)
```

> 📢 **섹션 요약 비유**: 자주 쓰는 단어는 짧게 약어로, 드문 전문 용어는 길게 표기 — 허프만 코딩은 글자판 효율화의 수학적 최적해.

---

## II. 허프만 트리 구성 알고리즘

```
알고리즘 (최소 힙 기반):

1. 각 문자를 빈도와 함께 노드로 생성
2. 모든 노드를 최소 힙(Min-Heap)에 삽입
3. 힙에서 빈도 최솟값 2개 추출
4. 두 노드를 자식으로 하는 내부 노드 생성
   (내부 노드 빈도 = 두 자식 빈도의 합)
5. 새 내부 노드를 힙에 삽입
6. 힙에 노드가 1개 남을 때까지 반복
7. 남은 노드 = 허프만 트리 루트

코드 할당:
  왼쪽 엣지 = 0, 오른쪽 엣지 = 1
  루트에서 각 리프까지 경로 = 해당 문자의 코드
```

```
허프만 트리 예시:

         (17)
        /    \
      (7)    (e:6)
     /    \
   (3)   (d:4)
  /    \
(a:2) (b:3)  <- 빈도 낮은 문자가 더 깊은 위치
```

> 📢 **섹션 요약 비유**: 자주 가는 집(e, d)은 입구 가까이, 드물게 가는 집(a, c)은 안쪽에 배치 — 허프만 트리는 최적 배치의 사전.

---

## III. 접두사 코드(Prefix Code) 특성

```
접두사 코드 (Prefix-Free Code):
  어떤 코드워드도 다른 코드워드의 접두사가 아님

  예시 (허프만 코드):
    a = 101, b = 100, c = 110, d = 01, e = 00
  
  인코딩: "abe" = 101 100 00 = "10110000"
  
  디코딩 (구분자 없이):
    10110000
    10 -> 없음, 101 -> a 발견!
    100 -> b 발견!
    00 -> e 발견!
    -> "abe"
  
  모호성 없음: 비트 스트림에서 순차 디코딩 가능
  (비교: "01" 코드와 "011" 코드가 동시 있으면 불가)
```

> 📢 **섹션 요약 비유**: 모스 부호처럼 — 한 기호가 다른 기호의 시작이 되지 않아야 연속된 신호를 구분할 수 있다.

---

## IV. 구현

```python
import heapq
from collections import defaultdict

def huffman_encoding(text):
    freq = defaultdict(int)
    for ch in text:
        freq[ch] += 1
    
    # 최소 힙: (빈도, 고유_id, 문자 or None, 왼쪽, 오른쪽)
    heap = [[f, i, ch, None, None] for i, (ch, f) in enumerate(freq.items())]
    heapq.heapify(heap)
    
    uid = len(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        heapq.heappush(heap, [lo[0]+hi[0], uid, None, lo, hi])
        uid += 1
    
    # 코드 생성
    codes = {}
    def generate(node, prefix=""):
        if node[2] is not None:  # 리프
            codes[node[2]] = prefix or "0"
        else:
            generate(node[3], prefix + "0")
            generate(node[4], prefix + "1")
    
    generate(heap[0])
    encoded = "".join(codes[ch] for ch in text)
    return codes, encoded

codes, encoded = huffman_encoding("aabbbccddddeeeeee")
print(f"코드표: {codes}")
print(f"압축 비트: {len(encoded)}")
```

> 📢 **섹션 요약 비유**: 가장 가벼운(빈도 낮은) 두 잎을 먼저 합쳐서 나무를 아래에서 위로 키우는 것 — 그리디 알고리즘의 교과서적 사례.

---

## V. 실무 시나리오 — JPEG 내부 허프만 코딩

```
JPEG 압축 파이프라인:
  원본 이미지
    ↓
  색공간 변환 (RGB → YCbCr)
    ↓
  DCT (이산 코사인 변환) - 8x8 블록
    ↓
  양자화 (Quantization) - 손실 발생
    ↓
  RLE (런-길이 인코딩) - AC 계수 0런 압축
    ↓
  허프만 코딩 - 최종 엔트로피 코딩 (무손실)
    ↓
  JPEG 파일

허프만 코딩 역할:
  DCT 계수의 빈도 분포에 맞춘 최적 코드
  일반적으로 0이 많이 나오므로 0에 짧은 코드
  
현대: 기본 허프만 → 산술 코딩(Arithmetic Coding)으로 개선
      (산술 코딩: 이론적 엔트로피 한계에 더 가까움)
```

> 📢 **섹션 요약 비유**: JPEG에서 허프만 코딩은 마지막 짐 정리 — DCT+양자화로 크게 줄인 후, 남은 공간을 허프만으로 꽉 채운다.

---

## 📌 관련 개념 맵

```
허프만 코딩 (Huffman Coding)
+-- 원리
|   +-- 빈도 비례 코드 길이
|   +-- 접두사 코드 (모호성 없음)
+-- 알고리즘
|   +-- 최소 힙 기반 트리 구성
|   +-- 그리디: O(n log n)
+-- 응용 분야
|   +-- DEFLATE (ZIP, PNG) 내부
|   +-- JPEG, MP3, HEVC
|   +-- bzip2 (BWT+허프만)
+-- 관련 알고리즘
    +-- 산술 코딩 (Arithmetic Coding)
    +-- 범위 코딩 (Range Coding)
    +-- ANS (Asymmetric Numeral Systems)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[Shannon 정보 이론 (1948)]
엔트로피 = 최소 압축 한계
      |
      v
[허프만 코딩 (David Huffman, 1952)]
최적 접두사 코드 알고리즘
학부생 논문으로 발표 (MIT)
      |
      v
[DEFLATE (ZIP, PNG) 통합 (1993)]
LZ77 + 허프만 = 사실상 모든 압축
      |
      v
[산술 코딩 (1980s~)]
허프만보다 이론 한계에 가까운 압축
JPEG-LS, HEVC에 적용
      |
      v
[현재: ANS (2013~)]
산술 코딩 수준 효율 + 병렬화 가능
Zstandard (zstd), lz4 내부 적용
```

---

## �� 어린이를 위한 3줄 비유 설명

1. 허프만 코딩은 자주 쓰는 글자는 짧은 암호로, 드물게 쓰는 글자는 긴 암호로 바꿔서 파일을 압축해요.
2. "e"가 가장 많이 나오면 "e=00"처럼 2비트만 쓰고, 드문 "z"는 "z=11110" 같이 5비트를 써요.
3. ZIP 파일이나 JPEG 사진 압축에 이 방법이 들어 있어서, 우리가 매일 쓰는 파일을 더 작게 저장할 수 있는 거예요!
