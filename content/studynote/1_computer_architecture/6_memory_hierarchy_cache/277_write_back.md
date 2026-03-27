+++
weight = 277
title = "277. Write-Back (나중 쓰기)"
date = 2024-01-01
[taxonomies]
categories = ["Computer Architecture"]
tags = ["CA"]
+++

# 277. Write-Back (나중 쓰기)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Write-Back(나중 쓰기/후기록)은 CPU가 데이터를 캐시에 기록(Write)할 때 **메인 메모리에는 즉시 쓰지 않고, 해당 캐시 라인이 eviction(교체) 될 때 비로소 최종 값만 한 번만 메모리에 기록하는** 속도 중심의 쓰기 정책이다.
> 2. **가치**: 동일한 데이터에 여러 번의 쓰기가 발생할 때, DRAM 쓰기를 수십 회에서 수천 회로 압축하여 **메모리 대역폭 소비를 극적으로 줄이고, CPU 파이프라인의 쓰기 Stall을 최소화**한다.
> 3. **단점**: 캐시와 메모리가 불일치(Inconsistency) 상태에 놓이므로, Coherence Protocol(MESI 등)을 필수적으로 구현해야 하고, 더티 비트(Dirty Bit)로 각 캐시 라인의 수정 여부를 추적해야 한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### Write-Back의 탄생 배경

CPU의 연산 속도와 DRAM의 접근 속도 차이는 수백 배에 달한다. 만약 Write-Through처럼 매 쓰기마다 DRAM까지 가야 한다면, CPU는 쓰기 동작에서 발생하는 수백 클럭의 지연을 전부 몸으로 받아야 한다.

예를 들어, 루프 내부에서 같은 변수에 10,000번을 쓰는 경우:
- **Write-Through**: 10,000 × 수백 클럭 = 수백만 클럭의 Stall
- **Write-Back**: 첫 시도만 Miss, 이후는 전부 Hit, eviction 시 단 1회만 DRAM 기록

이 엄청난 효율성 때문에, 현대 모든 범용 CPU의 데이터 캐시는 **기본적으로 Write-Back**을 사용한다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Write-Back의 동작 흐름

```text
[Write-Back 동작 시퀀스]

@CPU가 변수 A에 값 10을 기록 (Write-Back):
  ① L1 D-Cache에서 A 위치를 찾음 (Hit!)
  ② A의 값을 10으로 수정 (캐시 내에서 1~2클럭)
  ③ A의 캐시 라인을 "Dirty(더티)"로 표시 (Dirty Bit = 1)
  ④ CPU는 즉시 다음 명령어 실행 (Non-blocking!)
     * DRAM에는 아직 10이 기록되지 않음

@Eviction 발생 시 (A의 라인이 다른 데이터로 교체 대상일 때):
  ⑤ if Dirty Bit == 1:
       → DRAM의 A 위치에 현재 값(10)을 Write-Back
       → 수백 클럭 소요 ( Stall 발생 가능)
       → Dirty Bit = 0으로 Clear
     else (Dirty Bit == 0):
       → 아무것도 안 함 (Clean Eviction)
       → 그냥 해당 라인 덮어씀
```

### Dirty Bit (더티 비트)의 역할

```text
[캐시 라인의 상태 머신과 Dirty Bit]

[Valid=1, Dirty=0] --> Clean 상태
  메인 메모리에서 가져온 원본. 수정된 적 없음.

[Valid=1, Dirty=1] --> Dirty 상태
  CPU에 의해 수정되었으나, 메인 메모리에는 아직 반영 안 됨.

Eviction 판단:
  if Dirty == 1:
      DRAM에 현재 값 기록 (Write-Back 수행)
      Dirty Bit를 0으로 리셋
```

### Write-Back의_write Amplification_

Write-Back은 eviction 시 데이터의 최종 값만 기록하므로, 동일 주소에 수만 회 쓰기가 발생해도 실제 DRAM 쓰기는 1회에 그린다. 이것이 Write-Back의 가장 큰 장점이다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### Write-Back vs Write-Through 비교표

| 평가 항목 | Write-Back | Write-Through |
|:---|:---|:---|
| **DRAM 쓰기 횟수** | **극히 적음** (eviction 시만) | **매우 많음** (매 쓰기마다) |
| **쓰기 성능 (Hit 시)** | **빠름** (캐시 내에서 완료) | 느림 (DRAM까지) |
| **데이터 일관성** | 불완전 (Coherence 필요) | **완벽** |
| **하드웨어 복잡도** | **복잡** (Dirty Bit + Coherence) | 단순 |
| **전력 소모** | 낮음 (DRAM 쓰기 적음) | 높음 |
| **적합 환경** | **고성능 범용 CPU** | 특수 목적 |

### Coherence Protocol과의 필수적 결합

Write-Back 환경에서 다른 코어가 동일한 메모리 위치에 접근하려 할 때:

```text
[멀티코어 환경에서의 Write-Back 문제]

Core 0이 변수 X를 수정 (X=10):
  → Core 0의 L1 Cache에 X=10 기록 (Dirty Bit = 1)
  → DRAM에는 아직 X=0인 상태

Core 1이 X를 읽으려고 함:
  → Core 1의 Cache에는 X가 없음 (Miss)
  → 메인 메모리에서 X를 읽으려 함

문제: 메인 메모리에는 아직 X=0 (옛날 값!)
      Core 0의 Cache에는 X=10 (최신 값!)

해결: MESI Protocol
  → Core 0이 Core 1에게 "내 Cache에 X의 최신 값이 있어!"라고 신호
  → Core 1은 Core 0의 Cache에서 X=10을 가져옴 (Intervention)
  → 또는 Core 0이 DRAM에 Write-Back하여 최신 값으로 업데이트
```

---

## Ⅳ. 기대효과 및 결론

### 메모리 대역폭 절약 효과

```text
[쓰기 횟수에 따른 DRAM 쓰기 횟수 비교]

시나리오:동일 변수에 10,000회 연속 쓰기

Write-Through:
  → 10,000회 DRAM 쓰기 발생
  → DRAM 대역폭 소비: 10,000 × 64B = 640KB

Write-Back:
  → 단 1회 DRAM 쓰기 (eviction 시)
  → DRAM 대역폭 소비: 1 × 64B = 64B
  → 대역폭 소비 1/1000로 압축!
```

### 미래 전망

CPU 코어 수가 계속 증가함에 따라, Write-Back의 중요성은 더 증가하고 있다. 더 많은 코어가 동시에 메모리에 접근하려 하므로, 메모리 대역폭은 더욱 아쉬운 자원이 된다. Coherence Protocol의 개입를 최소화하는 방향 (방향성, Write-Combining 등)과 함께 Write-Back은 계속 진화한다.

---

### 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **쓰기 정책 (Write Policy)** | Write-Back이 속하는 상위 범주. Write-Through와 함께 양대 정책. |
| **더티 비트 (Dirty Bit)** | Write-Back의 필수 동반자. 수정 여부를 1비트로 표시. |
| **캐시 일관성 (Cache Coherence)** | Write-Back 환경에서 필수. MESI/MESIF/MOESI Protocol이 이를 관리. |
| **Eviction Policy** | Write-Back에서 eviction 시 Dirty Bit == 1이면 Write-Back 수행. |
| **Write Combining** | 여러 Write를 하나로 묶어 DRAM 쓰기 횟수를 더 줄이는 최적화 기법. |

---

### 👶 어린이를 위한 3줄 비유 설명
1. **개념**: 내 공책(캐시)에 수시로 적고 지우고를 반복하다가, 공책을 버릴 때(교체) 딱 한 번만 칠판(메모리)에 최종 내용을 옮 적는 거예요.
2. **좋은 점**: 칠판에 매번 가서 적고 지우는 피곤한 작업을 안 해도 돼서, 공책에 집중해서 엄청 빠르게 적을 수 있어요.
3. **문제점**: 다른 친구가 칠판을 보면 아직 내가 마지막으로 수정한 게 아니라 옛날 내용이 보여서, 내가 "잠깐, 지금 내 공책에는 다른 게 적혀 있는데!" 하고 알려줘야 하는 번거로움이 있어요.
