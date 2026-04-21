+++
weight = 23
title = "23. 해시맵 vs 트리맵 (HashMap vs TreeMap) — 순서 유무"
date = "2026-04-21"
[extra]
categories = "studynote-algorithm"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: HashMap은 해시 테이블 기반으로 O(1) 평균 연산을 제공하지만 순서를 보장하지 않으며, TreeMap은 레드-블랙 트리 (Red-Black Tree) 기반으로 O(log n) 연산과 정렬된 키 순서를 동시에 제공한다.
> 2. **가치**: "빠른 검색이냐, 정렬된 순서냐"라는 트레이드오프를 이해하면, 범위 쿼리·정렬 순회가 필요한 시나리오와 단순 키-값 매핑 시나리오를 명확히 구분할 수 있다.
> 3. **판단 포인트**: 키 순서와 범위 쿼리가 불필요하면 HashMap(O(1)), 정렬 순서·floorKey/ceilingKey·subMap 등 순서 기반 연산이 필요하면 TreeMap(O(log n))을 선택한다.

---

## Ⅰ. 개요 및 필요성

Java `Map` 인터페이스의 두 대표 구현인 `HashMap`과 `TreeMap`은 같은 API를 공유하지만 내부 구조와 성능 특성이 완전히 다르다. 순서 없이 빠른 조회만 필요한 경우와, 가격대별 상품 목록이나 날짜 범위 쿼리처럼 정렬 순서가 중요한 경우에 각각 최적화되어 있다.

### 기본 시간 복잡도 비교

| 연산 | HashMap | TreeMap |
|:---|:---:|:---:|
| get(key) | O(1) 평균 | O(log n) |
| put(key, value) | O(1) 평균 | O(log n) |
| remove(key) | O(1) 평균 | O(log n) |
| containsKey | O(1) 평균 | O(log n) |
| firstKey / lastKey | ❌ | O(log n) |
| floorKey / ceilingKey | ❌ | O(log n) |
| subMap(from, to) | ❌ | O(log n + k) |
| 순회 순서 | 불규칙 | 키 정렬 순 |

📢 **섹션 요약 비유**: HashMap은 번호표 없는 탈의실—빠르게 들어가지만 나올 때 순서가 없다. TreeMap은 번호 순서대로 줄 선 탈의실—조금 느리지만 항상 순서가 정렬되어 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### HashMap 내부 구조

```
배열(버킷) + 체이닝(Chaining)

Index:  0    1      2      3      4      ...
        │    │      │      │      │
       null  ●      ●     null    ●
             │      │             │
           (k1,v1) (k2,v2)      (k3,v3)
             │
           (k4,v4)  ← 같은 해시 버킷, 체인

키 순서: 해시값에 의존 → 삽입 순서나 정렬 순서 보장 없음
```

### TreeMap 내부 구조 (레드-블랙 트리)

```
TreeMap의 RB-Tree 예시 (키: 정수)

           [5,B]
          /     \
       [2,R]   [8,R]
       /   \   /   \
    [1,B][3,B][6,B][9,B]

B=Black, R=Red
중위 순회(In-order) → 1,2,3,5,6,8,9  ← 오름차순 정렬
삽입/삭제 후 회전으로 O(log n) 높이 유지
```

### 순서 기반 연산 비교

```java
// TreeMap만 가능한 연산 예시
TreeMap<Integer, String> map = new TreeMap<>();
map.put(5, "five"); map.put(2, "two"); map.put(8, "eight");

map.firstKey()          // 2 (최솟값)
map.lastKey()           // 8 (최댓값)
map.floorKey(6)         // 5 (6 이하 최댓값)
map.ceilingKey(6)       // 8 (6 이상 최솟값)
map.subMap(2, 7)        // {2=two, 5=five} (범위 추출)
map.headMap(5)          // {2=two} (5 미만)
map.tailMap(5)          // {5=five, 8=eight} (5 이상)
```

📢 **섹션 요약 비유**: TreeMap의 floorKey/ceilingKey는 가격이 정렬된 가격표에서 "10만원 이하 중 가장 비싼 것"을 즉시 찾는 기능이다.

---

## Ⅲ. 비교 및 연결

### 언어별 동등 구현

| 언어 | HashMap 동등 | TreeMap 동등 |
|:---|:---|:---|
| Java | `HashMap<K,V>` | `TreeMap<K,V>` |
| Python | `dict` (3.7+ 삽입 순서 유지) | `sortedcontainers.SortedDict` |
| C++ | `unordered_map<K,V>` | `map<K,V>` (레드-블랙 트리) |
| Go | `map[K]V` | `golang.org/x/exp/maps` + 정렬 |
| Rust | `HashMap<K,V>` | `BTreeMap<K,V>` |

### LinkedHashMap: 삽입 순서 유지

Java의 `LinkedHashMap`은 HashMap에 이중 연결 리스트를 추가하여 **삽입 순서**를 유지한다. LRU 캐시 구현에서 `accessOrder=true` 옵션으로 접근 순서 유지도 가능하다.

| 자료구조 | 성능 | 순서 |
|:---|:---:|:---|
| HashMap | O(1) avg | 없음 |
| LinkedHashMap | O(1) avg | 삽입 순서 |
| TreeMap | O(log n) | 키 정렬 순 |

📢 **섹션 요약 비유**: HashMap은 순서 없는 옷장, LinkedHashMap은 입은 순서대로 걸린 옷장, TreeMap은 사이즈 순서대로 정리된 옷장이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 주요 활용 사례

- **HashMap 활용**: 캐시(O(1) 조회), 빈도 카운팅, 그래프 인접 리스트, API 요청 파라미터 매핑
- **TreeMap 활용**: 가격대별 상품 목록, 시계열 데이터 범위 쿼리, 스케줄러(시간 기반 정렬), 자동 완성(접두사 범위 탐색), 세금 계산(구간별 세율 적용)

### 기술사 판단 기준

```
단순 키-값 조회 (=) + 순서 불필요      →  HashMap O(1) avg
키 정렬 순서 + 중위 순회 필요          →  TreeMap O(log n)
범위 쿼리 (A ≤ key ≤ B)               →  TreeMap.subMap()
floor/ceiling 연산 (주식 호가창)        →  TreeMap
삽입 순서 유지 + O(1) 조회             →  LinkedHashMap
LRU 캐시 구현                          →  LinkedHashMap(accessOrder=true)
```

📢 **섹션 요약 비유**: 주식 호가창은 TreeMap의 완벽한 활용 예—매수/매도 가격이 정렬된 상태에서 "현재가 이상의 최저 매도 호가"를 ceilingKey로 O(log n)에 즉시 찾는다.

---

## Ⅴ. 기대효과 및 결론

HashMap과 TreeMap은 서로 다른 문제를 해결한다. 단순 O(1) 조회가 목적이면 HashMap, 정렬 순서·범위 연산·floor/ceiling이 필요하면 TreeMap이 적합하다. Python dict는 3.7부터 삽입 순서를 보장하지만 TreeMap의 정렬 기능은 없다. 언어별로 동등한 자료구조의 시간 복잡도와 기능 차이를 이해하는 것이 핵심 역량이다.

**결론**: 조회 속도 최우선은 HashMap(O(1)), 정렬·범위 기반 연산이 필요하면 TreeMap(O(log n))이 결론이며, 두 자료구조의 트레이드오프는 "해시 vs 트리"의 근본 차이로 귀결된다.

---

### 📌 관련 개념 맵

| 개념 | 관계 |
|:---|:---|
| 해시 테이블 (Hash Table) | HashMap의 내부 구조 |
| 레드-블랙 트리 (Red-Black Tree) | TreeMap의 내부 구조 |
| LinkedHashMap | 삽입 순서 유지 HashMap 변형 |
| B+ 트리 (B+ Tree) | 데이터베이스 범위 인덱스 (TreeMap 대응) |
| 부하 계수 α | HashMap 리해싱 결정 기준 |
| LRU 캐시 | LinkedHashMap 활용 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. HashMap은 이름표 없는 그릇 선반—아무 곳에나 빠르게 넣고 꺼내지만 순서는 모르는 채야.
2. TreeMap은 크기 순서대로 줄 세운 그릇 선반—찾는 데 조금 더 걸리지만 "제일 큰 것"이나 "중간 크기"를 금방 찾아.
3. 게임 점수판처럼 항상 정렬된 순서가 필요하면 TreeMap, 친구 이름으로 점수를 빠르게 찾기만 하면 HashMap이야!
