+++
title = "41. 추측 실행 (Speculative Execution)"
date = 2026-03-06
categories = ["studynotes-computer-architecture"]
tags = ["Speculative-Execution", "Spectre", "Meltdown", "Out-of-Order", "Side-Channel"]
draft = false
+++

# 추측 실행 (Speculative Execution)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 추측 실행은 **"명령어**를 **미리 **실행**하고 **결과**를 **확정**하기 **전**까지 **커밋**하지 **않는 **기술\"**로, **Branch Prediction**(분기 **예측)**과 **결합**하여 **Out-of-Order **Execution**에서 **성능**을 **향상**시킨다.
> 2. **취약점**: **Spectre**(분기 **예측 **오남용), **Meltdown**(권한 **격리 **우회)**와 **같은 **Side-Channel **공격**(캐시 **타이밍 **공격)**에 **취약**하며 **CPU **내부 **상태**가 **유출**될 **수 **있다.
> 3. **대응**: **Software **Mitigation**(ReTPoline, **LFence)**, **Hardware **Fix**(Microcode **Update)**, **Architecture **Change**(SFI, **CAF)**로 **완화**되고 **Constant-Time **Programming**(시간 **일정 **코드)**로 **방어**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
추측 실행은 **"미리 실행하고 취소하기"**이다.

**추측 실행 유형**:
| 유형 | 설명 | 예시 |
|------|------|------|
| **Branch** | 분기 예측 후 실행 | Conditional jump |
| **Value** | 값 예측 후 실행 | Load address |
| **Memory** | 로드 미리 수행 | Prefetch |

### 💡 비유
추측 실행은 ****예비 **주자 ****와 같다.
- **예측**: 미리 준비
- **확인**: 맞으면 사용
- **취소**: 틀리면 폐기

---

## Ⅱ. 아키텍처 및 핵심 원리

### Speculative Execution Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Speculative Execution Pipeline                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Code:                                                                                  │  │
    │  if (x > 0) {                    // Branch (predicted TAKEN)                             │  │
    │      y = y + 1;                // Speculatively executed                                │  │
    │  } else {                                                                                   │  │
    │      y = y - 1;                // Not executed (predicated out)                         │  │
    │  }                                                                                       │  │
    │  z = z + 2;                   // Executed after branch resolves                          │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Pipeline:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  IF      │  ID     │  EX     │  MEM    │  WB                                             │  │
    │  ───────────────────────────────────────────────────────────────────────────────────────│  │
    │  B1      │  B1     │  B1     │         │                                                 │  │
    │  (br)    │  (pred) │  (TAKEN)│         │                                                 │  │
    │          │         │         │         │                                                 │  │
    │  S1      │  S1     │  S1     │  S1     │  S1                                              │  │
    │  (spec)  │  (spec) │  (spec) │  (spec) │  (spec)                                         │  │
    │          │         │         │         │  ← S1 result pending commit                     │  │
    │  S2      │  S2     │  S2     │  S2     │  S2                                              │  │
    │  (spec)  │  (spec) │  (spec) │  (spec) │  (spec)                                         │  │
    │                                                                                         │  │
    │  → Branch resolves: TAKEN was correct → S1, S2 commit                                  │  │
    │  → Branch resolves: TAKEN was wrong → Flush S1, S2, fetch E-path                         │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Reorder Buffer (ROB)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Reorder Buffer (ROB)                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Structure:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ROB Entry (in-order retirement, out-of-order execution)                               │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Entry │  Opcode  │  Result  │  Valid  │  Ready  │  Dest   │  Exception              │  │  │
    │  │  ─────────────────────────────────────────────────────────────────────────────────────│  │  │
    │  │  1      │  ADD     │  0x42    │  1      │  1      │  R1     │  None                   │  │  │
    │  │  2      │  MUL     │  -       │  0      │  0      │  R2     │  None (waiting)         │  │  │
    │  │  3      │  LD      │  -       │  0      │  0      │  R3     │  None (waiting)         │  │  │
    │  │  4      │  BRANCH  │  -       │  0      │  0      │  -      │  Speculative            │  │  │
    │  │  5      │  ADD     │  0x55    │  1      │  1      │  R4     │  Speculative            │  │  │
    │  │  6      │  SUB     │  -       │  0      │  0      │  R5     │  Speculative            │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Retirement:                                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Head pointer: Points to oldest unretired entry                                   │  │  │
    │  │  • Entry 1: Valid + Ready → Retire (commit to architectural state)                   │  │  │
    │  │  • Entry 2, 3: Waiting for result → Block retirement                                 │  │  │
    │  │  • Entry 4: Branch mispredict → Flush entries 4-6                                   │  │  │
    │  │  • Entry 5, 6: Squashed (discarded)                                                  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### Spectre & Meltdown 비교

| 취약점 | 원인 | 영향 | 대응 |
|--------|------|------|------|
| **Spectre V1** | Bounds Check Bypass | 데이터 유출 | LFence |
| **Spectre V2** | Branch Target Injection | 코드 유출 | Retpoline |
| **Meltdown** | Exception Suppression | 메모리 유출 | KPTI |
| **Spectre-RSB** | RSB Underflow | 코드 유출 | RSB Refill |

### Spectre V1 (Bounds Check Bypass)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Spectre V1 Attack                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Vulnerable Code:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // Attacker-controlled array1 and index                                              │  │
    │  if (index < array1_size) {                 // Branch: PREDICTED TAKEN                │  │
    │      value = array2[array1[index] * 64];    // Speculatively executed (bypass check)   │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  // Attack steps:                                                                       │  │
    │  1. Train branch predictor to predict TAKEN                                             │  │
    │  2. Provide index > array1_size (e.g., 10000)                                          │  │
    │  3. Branch predicted TAKEN (misprediction later)                                        │  │
    │  4. array2[array1[10000] * 64] speculatively loaded                                    │  │
    │  5. Load accesses secret memory based on array1[10000]                                  │  │
    │  6. Cache state depends on secret value                                                  │  │
    │  7. Attacker infers secret via cache timing                                              │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Timeline:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  │  Time  │  CPU                     │  Architectural State  │  Microarchitectural State    │  │
    │  │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  │  T0    │  Check: 10000 < size?   │  Waiting               │  Speculatively execute      │  │
    │  │        │  Predict: TAKEN           │                        │  load (secret → cache)       │  │
    │  │        │                          │                        │                             │  │
    │  │  T1    │  Resolve: FALSE          │  NOT updated            │  Cache affected by secret   │  │
    │  │        │  Flush pipeline           │                        │                             │  │
    │  │        │                          │                        │                             │  │
    │  │  T2    │  Attacker probes cache    │  Recovered secret      │  Side channel leak          │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Meltdown (Rogue Data Cache Load)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Meltdown Attack                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Vulnerability: Exception suppression
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // Attacker code in user space                                                         │  │
    │  char kernel_secret = kernel_memory[address];  // Causes page fault                     │  │
    │  // Exception NOT raised immediately due to out-of-order execution                        │  │
    │  cache_line = kernel_secret * 4096;         // Secret brought into cache                 │  │
    │  // Exception raised here, but cache state changed                                     │  │
    │                                                                                         │  │
    │  → Kernel memory read despite isolation                                                │  │
    │  → All kernel memory accessible before KPTI (Kernel Page Table Isolation)               │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Mitigation: KPTI (Kernel Page Table Isolation)
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Before Meltdown:                                                                        │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  User Page Table                    Kernel Page Table                               │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  User memory: RW                    Kernel memory: RW                           │  │  │  │
    │  │  │  Kernel memory: RW (for syscalls)     User memory: --                           │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  │  → Single CR3 switch per context switch                                            │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  After KPTI:                                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  User Page Table                    Kernel Page Table                               │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  User memory: RW                    User memory: RW                            │  │  │  │
    │  │  │  Kernel memory: --                   Kernel memory: RW                           │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  │  → CR3 switch on every syscall/interrupt (performance penalty ~5-30%)              │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 클라우드 보안 완화
**상황**: 멀티테넌트 환경
**판단**: CPU 마이크로코드 업데이트 + KPTI

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Cloud Provider Mitigation                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Layers of Defense:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Hardware                                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Microcode update from Intel/AMD                                                    │  │  │
    │  │  • New CPU: Hardware fixes for Meltdown (RDL), Spectre v2                           │  │  │
    │  │  • MSB/RSB mechanisms in silicon                                                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  2. OS/Kernel                                                                            │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • KPTI/KAISER: Separate page tables for kernel                                    │  │  │
    │  │  • Retpoline: Return trampoline for indirect branches                                │  │  │
    │  │  • RSB stuffing: Fill Return Stack Buffer on context switch                          │  │  │
    │  │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  # Retpoline example                                                              │  │  │  │
    │  │  │  call set_up_target                                                              │  │  │  │
    │  │  │  capture_spec:                                                                   │  │  │  │
    │  │  │      pause                                        # Stop speculation                │  │  │  │
    │  │  │      lfence                                       # Memory barrier                  │  │  │
    │  │  │      jmp capture_spec                             # Infinite loop (never taken)      │  │  │  │
    │  │  │  set_up_target:                                                                   │  │  │  │
    │  │  │      mov rax, (rsp)                               # Get return address            │  │  │  │
    │  │  │      mov [new_target], rax                        # Store for later use            │  │  │  │
    │  │  │      ret                                          # Return to captured target       │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  3. Compiler                                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • -mretpoline (GCC/Clang)                                                            │  │  │
    │  │  • LFENCE insertion (CS=false)                                                        │  │  │
    │  │  │  __builtin_ia32_lfence()                                                           │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  4. Application                                                                         │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Constant-time programming (no data-dependent branches)                             │  │  │
    │  │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  // Bad: data-dependent branch (vulnerable)                                      │  │  │  │
    │  │  │  if (secret == 0) { return a; } else { return b; }                                │  │  │  │
    │  │  │                                                                                     │  │  │  │
    │  │  │  // Good: constant-time (safe)                                                    │  │  │  │
    │  │  │  return (secret & 1) * a + (~secret & 1) * b;                                      │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 완화 후 성능 영향

| 완화 | 오버헤드 | 영향 |
|------|----------|------|
| **KPTI** | 5-30% | 시스템 콜 |
| **Retpoline** | 1-5% | 간접 분기 |
| **LFENCE** | 2-10% | 직렬화 |

### 모범 사례

1. **업데이트**: 최신 마이크로코드
2. **컴파일**: Retpoline 활성화
3. **검증**: Side-channel 테스트
4. **모니터링**: 성능 영향 측정

### 미래 전망

1. **Hardware fixes**: 새 CPU
2. **SFI**: Software Fault Isolation
3. **CAF**: Control-flow Attestation
4. **Secure Speculation**: 완화된 설계

### ※ 참고 표준/가이드
- **Intel**: Speculative Execution Side Channel
- **AMD**: Software Techniques
- **ARM**: Speculative Execution

---

## 📌 관련 개념 맵

- [분기 예측](./15_branch_prediction/130_branch_prediction.md) - BTB
- [아웃오브오더](./4_pipeline/85_superscalar.md) - OoOE
- [캐시 일관성](./11_synchronization/122_cache_coherence.md) - MESI
