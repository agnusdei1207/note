+++
weight = 281
title = "281. 희생 캐시 (Victim Cache)"
date = 2024-01-01
[taxonomies]
categories = ["Computer Architecture"]
tags = ["CA"]
+++

# 281. 희생 캐시 (Victim Cache)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 희생 캐시(Victim Cache)는 L1 캐시에서 eviction(교체)당한 victim 데이터들을 완전 연관 사상(Fully Associative)으로 저장하여, 그 데이터가 곧 다시 필요할 경우 **메모리까지 가지 않고도 1~2클럭 내에 L1으로 swap하는** 소규모 캐시이다.
> 2. **가치**: 직접 사상(Direct mapping) 캐시에서 발생하는 충돌 미스(Conflict Miss)를 크게 줄이면서, 완전 연관 사상의 단점(높은 탐색 비용)을 희생 캐시라는 소규모 완충재로 대체하여 **하드웨어 비용 대비 성능 향상비가 가장 높은** 설계 기법이다.
> 3. **융합**: 현대 AMD 프로세서의 배타적 캐시(Exclusive Cache) 정책으로 발전하여, L1 victim을 L2 전체가 희생 캐시처럼 사용하는 형태로 진화했다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 충돌 미스(Conflict Miss)의 문제

Direct Mapping 캐시에서 두 개의 자주 사용되는 데이터가 동일한 인덱스에 매핑되면:

```text
[Direct Mapping 충돌 시나리오]

상황: Direct Mapping L1 캐시, 4칸 (인덱스 0에만 4개 데이터 A, B, C, D 매핑)

@t=0: A 접근 → Miss → A를 인덱스 0에 적재 [A]
@t=1: B 접근 → Miss → B가 A를 퇴출, A를 인덱스 0에 적재 [B]
@t=2: A 접근 → Miss! → A가 B를 퇴출, B를 인덱스 0에 적재 [A]
@t=3: B 접근 → Miss! → B가 A를 퇴출, A를 인덱스 0에 적재 [B]
...
결과: A와 B가 서로를 퇴출시키며 영원히 Miss만 발생 (Thrashing!)
```

### 희생 캐시의 탄생 배경

설계자들은 고민끝에 생각해냈습니다:
> "-eviction된 데이터를 아예 버리지 말고, 아주 작은 전용 캐시에 잠시 보관해두자. 그리고 다시 필요하면 L1과 swap하면 DRAM까지 가지 않아도 좋겠다!"

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 희생 캐시의 구조

```text
[희생 캐시 동작 흐름]

┌─────────────────────────────────────────────────────┐
│                                                      │
│  @Eviction 시 (예: L1 인덱스 0에서 A가victim으로퇴출)  │
│                                                      │
│  L1 Cache                           Victim Cache      │
│  ┌────────────────────┐            ┌─────────────┐  │
│  │ [A] [B] [C] [D]   │ ───────►   │ [A(Evicted)]│  │
│  │  evict A!         │            │  (4~16 entry)│  │
│  └────────────────────┘            │ Fully-Assoc   │  │
│                                    └─────────────┘  │
│                                                      │
│  @CPU가 A를 다시 접근할 때                            │
│                                                      │
│  L1 Cache                           Victim Cache      │
│  ┌────────────────────┐            ┌─────────────┐  │
│  │ [B] [C] [D] [E]   │ ◄──────►   │ [A(Hit!)]   │  │
│  │                    │   SWAP!    │             │  │
│  └────────────────────┘            └─────────────┘  │
│                                                      │
│  A는 Victim Cache에서 L1으로 빠르게 swap (1~2클럭!)  │
│  DRAM까지 가지 않음! → Miss Penalty = 0에 가까움!    │
└─────────────────────────────────────────────────────┘
```

### 희생 캐시 대 Cache Miss 비교

| 구분 | Victim Cache Hit | Cache Miss |
|:---|:---|:---|
| **접근 시간** | 1~2 클럭 | 수백 클럭 (DRAM까지) |
| **전력 소모** | 극히 적음 (캐시 내부) | 매우 높음 (DRAM 통신) |
| **대역폭** | 소비 없음 | DRAM 버스 사용 |

---

## Ⅲ. 희생 캐시의 진화: Exclusive Cache

### AMD의 Exclusive 캐시 정책

현대 AMD 프로세서에서는 희생 캐시라는 별도의 모듈을 두지 않고, **L2 캐시 전체를 L1의 victim 캐시처럼 사용**한다.

```text
[AMD Exclusive Cache 동작]

L1 Cache          L2 Cache (희생 캐시 역할)
   │                    │
   │ [A] evicted ────────► [A]
   │                    │
   │ [B] evicted ────────► [B]
   │                    │
   │ [A] needed ◄──────── [A] swap!
   │                    │
   │                    [B]

* 장점: 별도의 희생 캐시 하드웨어 불필요
* 효과: L1 + L2 전체 용량 = 실제 사용 가능한 용량
  (L1과 L2가 데이터를 중복하지 않으므로)
```

---

## Ⅳ. 기대효과 및 결론

### 성능 향상 효과

```text
[Direct Mapping + Victim Cache vs Set-Associative]

@4-Way Set-Associative를 불가능한 경우:
  → Direct Mapping + Victim Cache로 비슷한 효과 획득

@설문 조사 결과:
  - Victim Cache 크기: 4개 entry만으로 충돌 미스 25~40% 감소
  - 16개 entry에서는 충돌 미스 40~60% 감소
  - 전력: 완전 연관 사상 대비 현저히 낮음 (비교기 N개가 아닌,N개 중victim 만 확인)
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **충돌 미스 (Conflict Miss)** | 희생 캐시가 탄생한 이유. Direct Mapping에서 동일 인덱스 충돌이 원인. |
| **완전 연관 사상 (Fully Associative)** | 희생 캐시가victim을저장하기 위해 채택한 사상 방식. |
| **Direct Mapping** | 희생 캐시의 도움을 가장 많이 받는 (충돌 미스가 잦은) 사상 방식. |
| **Exclusive Cache** | 희생 캐시의 철학을 L2 캐시 전체로 확장한 현대 AMD의 정책. |
| **Cache Swap** | 희생 캐시의 핵심 동작.victim과 L1 데이터를 1~2클럭 내에 교환. |

---

### 👶 어린이를 위한 3줄 비유 설명
1. **개념**: 놀이기구 사정실(Direct Mapping 캐시)에서 특정 번호 의자(인덱스)를 두고 차 [↑]가 [↑]를 퇴출시키고, [↑]가 [↑]를 퇴출시키며 아무도 Ride 못 하는 상황에서, 퇴출당한 아이들을 옆에 작은 놀이기구 대기실(Victim Cache)에 잠시 기다리게 해두다 거예요.
2. **좋은 점**: 다시 해당 놀이기구를 타게 될 때, 대기실에서 바로 다시 들어갈 수 있으므로, 멀리 본관(DRAM)까지 가지 않아도 돼요.
3. **확장**: 요즘 놀이터(AMD CPU)에서는퇴출당한 애들을 위한전용대기실(별도 Victim Cache)을 두는 대신, 큰 운동장(L2 Cache) 전체를퇴출 대기실로 쓰면서 공간을 더 효율적으로 활용해요.
