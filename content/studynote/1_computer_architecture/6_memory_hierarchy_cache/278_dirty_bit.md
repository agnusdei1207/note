+++
weight = 278
title = "278. 더티 비트 (Dirty Bit)"
date = 2024-01-01
[taxonomies]
categories = ["Computer Architecture"]
tags = ["CA"]
+++

# 278. 더티 비트 (Dirty Bit)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 더티 비트(Dirty Bit, Modified Bit)는 Write-Back(나중 쓰기) 정책을 사용하는 캐시에서, **해당 캐시 라인의 데이터가 CPU에 의해 수정(Write)되었는지 여부를 표시하는 1비트의 꼬리표**이다.
> 2. **가치**: eviction 시 Dirty Bit를 확인하여, 수정된 데이터만 DRAM에 기록(Write-Back)하고, 수정되지 않은 데이터는 그냥 버림으로써 **불필요한 DRAM 쓰기를 원천 차단하여 메모리 대역폭을 획기적으로 절약**한다.
> 3. **융합**: CPU 캐시뿐 아니라 OS의 가상 메모리(페이지 테이블), 데이터베이스 버퍼 풀, 파일 시스템 메타데이터 관리 등에서 동일한 원리로 사용되는 보편적인 트래킹 기법이다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### Dirty Bit가 필요한 이유

Write-Back 정책에서는 "수정된 데이터만 eviction 시 DRAM에 기록"하고 싶지만, 하드웨어는 다음의 문제에 직면한다:

> **" eviction 대상인 이 캐시 라인이, CPU에 의해 수정되었는지 어떻게 알까? "**

만약 수정 여부를 모르고 eviction 시 매번 DRAM에 쓰기를 하면:
- 수정되지 않은(Clean) 라인까지 DRAM에 기록 → **불필요한 DRAM 쓰기 발생**
- 이는 메모리 대역폭의 낭비과 전력 소모을 유발

**답변**: 각 캐시 라인에 1비트를 할당하여 "수정 여부"를 추적하면 된다. 이것이 바로 Dirty Bit다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Dirty Bit의 상태 머신

```text
[캐시 라인 Life Cycle과 Dirty Bit]

① 메인 메모리 --> 캐시 로드 (Read)
   [Dirty Bit = 0] (Clean: 메모리와 동일)

② CPU가 해당 라인에서 데이터 읽기 (Read)
   [Dirty Bit = 0] (변경 없음)

③ CPU가 해당 라인에 데이터 쓰기 (Write)
   [Dirty Bit = 0] --> [Dirty Bit = 1] (Modified: 메모리와 다름)

④-a Eviction 발생 + Dirty Bit = 1:
   → DRAM에 데이터 기록 (Write-Back)
   → [Dirty Bit = 0]으로 Reset

④-b Eviction 발생 + Dirty Bit = 0:
   → 아무것도 안 함 (Clean Eviction)
   → 그냥 덮어씀
```

### Dirty Bit vs Valid Bit

둘 다 캐시 라인의 상태를 나타내지만, 그 역할은 다르다:

| 비트 | 의미 | 동작 |
|:---|:---|:---|
| **Valid Bit** | "이 캐시 라인에 의미 있는 데이터가 있는가?" | Valid=0이면 데이터가 무효거나, 아직 메모리에서 로드되지 않음 |
| **Dirty Bit** | "이 데이터가 메모리와동일인가?" | Dirty=1이면 수정되어 메모리와 다르며, eviction 시 DRAM 기록 필요 |

```text
[Valid=0, Dirty=0]
→ 이 캐시 라인은 아직 사용된 적 없음 (Invalid/New)

[Valid=1, Dirty=0]
→ 유효하지만 메모리와동일 (Clean)

[Valid=1, Dirty=1]
→ 유효하고 수정됨 (Dirty)

[Valid=0, Dirty=1]
→ 이 조합은 발생하지 않음 (불가능)
```

---

## Ⅲ. 성능 최적화 효과

### 불필요한 DRAM 쓰기 방지

```text
[Dirty Bit 도입 효과 시뮬레이션]

상황: 100개의 캐시 라인 eviction 발생
      이 중 80개는 Read-only 데이터 (Dirty=0)
      이 중 20개는 수정된 데이터 (Dirty=1)

[Dirty Bit 없는 경우 (무조건 Write-Back)]
  → 100 × DRAM 쓰기 = 100회

[Dirty Bit 있는 경우 (수정된 것만 Write-Back)]
  → 20 × DRAM 쓰기 = 20회
  → DRAM 쓰기 80회 절감 (80% 감소!)
```

### OS 가상 메모리에서의 Dirty Bit

Dirty Bit의 원리는 OS의 가상 메모리(페이징)에서도 동일하게 적용된다.

| OS 구성 요소 | Dirty Bit 활용 |
|:---|:---|
| **페이지 테이블 (Page Table)** | 각 페이지 프레임에 Modify Bit ( Dirty Bit ) 부착 |
| **Page Out (스왑 아웃)** | Dirty=1인 페이지만 디스크에 기록 |
| **Page In (스왑 인)** | 디스크에서 메모리로 로드 시 Dirty=0으로 Reset |
| **Copy-on-Write (COW)** | forked 프로세스에서 pages를 수정 전까지 Dirty=0으로 유지 |

```text
[OS의 Page Out 동작]

① RAM 용량 부족 → 페이지 교체를 수행해야 함

② 스왑 대상 페이지 선택 (LRU 등)

③ if Dirty Bit == 1 (수정됨):
     → 해당 페이지를 디스크에 기록 (Page Out)
     → 디스크 I/O 발생 (수십 ms 소요)
     → 시간 + 전력 비용
   else (Dirty == 0, 수정 안 됨):
     → 디스크 기록 불필요
     → 그냥 해당 프레임을 해제하고 재사용
     → 훨씬 빠른 처리
```

---

## Ⅳ. 기대효과 및 결론

### 메모리 대역폭 및 전력 절감 효과

| 시나리오 | Dirty Bit 없음 | Dirty Bit 있음 |
|:---|:---|:---|
| **DRAM 쓰기 트래픽** | 모든 eviction 시 기록 | 수정된 라인의 eviction 시만 기록 |
| **전력 소모** | DRAM 쓰기 시마다 활성 | 불필요한 쓰기 제거로 감소 |
| **디스크 I/O (OS)** | Modified 페이지를 항상 스왑 아웃 | Modified 페이지만 스왑 아웃 |

Dirty Bit는 하드웨어에 단 1비트만을 추가하지만, 시스템 전체의 메모리 효율을 획기적으로 향상시키는 획기적인 설계이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Write-Back** | Dirty Bit가 존재하는 이유. Write-Back의 필수 동반 장치. |
| **Eviction Policy** | eviction 시 Dirty Bit를 확인하여 Write-Back 여부를 결정. |
| **Valid Bit** | Dirty Bit와 함께 캐시 라인의 상태를 나타내는 또 다른 1비트. |
| **MESI Protocol** | Dirty Bit의 상태 (Modified)를 활용하는 대표적 Coherence Protocol. |
| **Page Replacement** | OS에서도 동일한 원리로 Dirty Bit(Modify Bit)를 사용. |

---

### 👶 어린이를 위한 3줄 비유 설명
1. **개념**: 내 공책(캐시)의 각 페이지 귀퉁이에 "수정됨(빨간 딱지)" 표기를 하는 거예요. 한 줄이라도 적으면 딱지를 붙이고, 그냥 읽기만 하면 아무 표시 안 해요.
2. **좋은 점**: 공책을 버릴 때(교체), 딱지가 없으면(clean) 그냥 버리면 돼요. 근데 빨간 딱지가 붙어있으면(dirty), 그 내용을 교실 칠판(메모리)에 먼저 옮 적어놔야 하죠.
3. **효과**: 칠판에 읽기만 한 페이지를 또 또 쓰려고 가서 적고 하는 불필요한 작업을 줄여서, 전체 시간이 엄청 절약돼요!
