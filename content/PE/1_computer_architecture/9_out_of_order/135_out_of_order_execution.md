+++
title = "46. 비순차 실행 (Out-of-Order Execution)"
date = 2026-03-06
categories = ["studynotes-computer-architecture"]
tags = ["Out-of-Order", "Superscalar", "Pipeline", "Tomasulo", "Register-Renaming"]
draft = false
+++

# 비순차 실행 (Out-of-Order Execution)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비순차 실행은 **"명령어**를 **프로그램 **순서**와 **다르게 **실행**하여 **파이프라인 **스톨**(Stall)**을 **줄이고 **성능**을 **향상**하는 **기법\\\"**으로, **Dependency **Analysis**(의존성 **분석)**과 **Register **Renaming**(레지스터 **이름 **변경)**이 **핵심**이다.
> 2. **Tomasulo **Algorithm**: **Register **Rename**, **Reservation **Station**(예약 **스테이션)**, **Common **Data **Bus**(CDB)**로 **WAR**(Write **After **Read)**, **WAW**(Write **After **Write)** **해저드**를 **해결**하고 **다중 **명령어**를 **동시**에 **실행**한다.
> 3. **Speculation**: **Branch **Prediction**(분기 **예측)**과 **Speculative **Execution**(추론 **실행)**으로 **분기 **후 **명령어**를 **미리 **실행**하고 **Reorder **Buffer**(ROB)**로 **순서**를 **보장**하며 ** misprediction **시 **rollback**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
비순차 실행은 **"명령어 순서 변경 실행"**이다.

**데이터 해저드**:
| 유형 | 설명 | 해결 |
|------|------|------|
| **RAW** | Read After Write | 진정 의존성 |
| **WAR** | Write After Read | 이름 변경 |
| **WAW** | Write After Write | 이름 변경 |

### 💡 비유
비순차 실행은 ****요리 **순서 ****와 같다.
- **재료**: 손질
- **조리**: 볶음
- **완성**: 접시

---

## Ⅱ. 아키텍처 및 핵심 원리

### Out-of-Order Execution Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Out-of-Order Execution Pipeline                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Pipeline Stages:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  In-Order Frontend        │  Out-of-Order Engine      │  In-Order Backend              │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  IF → ID → DIS → REN → ISS → EX → MEM → WB → RET                                    │  │  │
    │  │  │    │    │     │     │     │     │     │     │                                    │  │  │
    │  │  │    │    │     │     │     │     │     │     │                                    │  │  │
    │  │  │    │    │     │     │     ▼     ▼     ▼     ▼                                    │  │  │
    │  │  │    │    │     │     │  Reservation Stations  │  Functional Units                │  │  │
    │  │  │    │    │     │     │  • Integer RS          │  • ALU 1                         │  │  │
    │  │  │    │    │     │     │  • Memory RS           │  • ALU 2                         │  │  │
    │  │  │    │    │     │     │  • FP RS               │  • FPU                           │  │  │
    │  │  │    │    │     │     ▼                       │  • Load/Store Unit                │  │  │
    │  │  │    │    │     │     Reorder Buffer (ROB)     ▼                                     │  │  │
    │  │  │    │    │     │     • 32-256 entries         │  Result Bus (CDB)                │  │  │
    │  │  │    │    │     │     • In-order commit        │                                     │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Stage Descriptions:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  IF: Instruction Fetch (fetch cache)                                                     │  │
    │  ID: Instruction Decode (decode opcode, registers)                                       │  │
    │  DIS: Dispatch (send to reservation station)                                             │  │
    │  REN: Register Rename (map architectural to physical registers)                           │  │
    │  ISS: Issue (dispatch to functional unit when operands ready)                             │  │
    │  EX: Execute (functional unit computes result)                                            │  │
    │  MEM: Memory Access (load/store from cache/memory)                                        │  │
    │  WB: Write Back (write result to ROB)                                                     │  │
    │  RET: Retire (commit to architectural state in-order)                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Register Renaming

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Register Renaming (Eliminating WAR/WAW)                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Example Code:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. ADD R1, R2, R3    ; R1 = R2 + R3                                                    │  │
    │  2. SUB R4, R1, R5    ; R4 = R1 - R5    (RAW: R1)                                       │  │
    │  3. MUL R1, R6, R7    ; R1 = R6 * R7    (WAW: R1, WAR: R1 in #2)                         │  │
    │  4. ADD R8, R1, R9    ; R8 = R1 + R9    (RAW: R1)                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Without Renaming (Serial Execution):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. ADD R1, R2, R3 → R1                                                                 │  │
    │  2. SUB R4, R1, R5 → R4  (stall, wait for #1)                                          │  │
    │  3. MUL R1, R6, R7 → R1  (stall, wait for #2 for WAR)                                   │  │
    │  4. ADD R8, R1, R9 → R8  (stall, wait for #3)                                          │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    With Renaming (Parallel Execution):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Architectural Registers: R1-R16 (programmer-visible)                                    │  │
    │  Physical Registers: P1-P64 (internal, renamed)                                         │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  RAT (Register Alias Table):                                                         │  │  │
    │  │  │  Arch  │  Physical  │  Status                                                    │  │  │
    │  │  │  ───────────────────────────────────────────────────────────────────────────────────│  │  │
    │  │  │  R1    │  P10       │  Valid                                                     │  │  │
    │  │  │  R2    │  P2        │  Valid                                                     │  │  │
    │  │  │  R3    │  P3        │  Valid                                                     │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Renamed Instructions:                                                                │  │  │
    │  │  1. ADD P10, P2, P3   (R1→P10)                                                        │  │  │
    │  │  2. SUB P11, P10, P5  (R4→P11, R1→P10)  [wait for P10]                               │  │  │
    │  │  3. MUL P12, P6, P7   (R1→P12, no WAR!)  [can execute in parallel]                   │  │  │
    │  │  4. ADD P13, P12, P9  (R8→P13, R1→P12)  [wait for P12]                               │  │  │
    │  │  → #2 and #3 can execute in parallel (WAR, WAW eliminated)                            │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Tomasulo Algorithm

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Tomasulo Algorithm (Reservation Station)                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Reservation Station Entry:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  │  Field      │  Description                                                                 │  │
    │  │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  │  OP         │  Operation (ADD, SUB, MUL, LOAD, STORE)                                    │  │
    │  │  Vj, Vk     │  Operand values (if ready)                                                   │  │
    │  │  Qj, Qk     │  Reservation station producing operands (if not ready)                      │  │
    │  │  Busy       │  Entry is valid                                                             │  │
    │  │  Dest       │  Destination register (architectural)                                       │  │
    │  │  Addr       │  Memory address (for loads/stores)                                          │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Example Execution:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Code:                                                                                   │  │
    │  1. LD F1, 0(R1)     ; F1 = mem[R1 + 0]                                                   │  │
    │  2. LD F2, 8(R1)     ; F2 = mem[R1 + 8]                                                   │  │
    │  3. MUL F3, F1, F2   ; F3 = F1 * F2       (wait for F1, F2)                               │  │
    │  4. ADD F4, F3, F5   ; F4 = F3 + F5       (wait for F3)                                   │  │
    │                                                                                         │  │
    │  Reservation Station State (after issue):                                                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Load1: OP=LD, Vj=<R1>, Vk=, Dest=F1, Busy=Yes                                        │  │  │
    │  │  Load2: OP=LD, Vj=<R1>, Vk=, Dest=F2, Busy=Yes                                        │  │  │
    │  │  Mul1:  OP=MUL, Vj=, Vk=, Qj=Load1, Qk=Load2, Dest=F3, Busy=Yes                        │  │  │
    │  │  Add1:  OP=ADD, Vj=, Vk=<F5>, Qj=Mul1, Qk=, Dest=F4, Busy=Yes                           │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Execution:                                                                              │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Load1 → L1 Cache → CDB (result: F1 = 1.0)                                            │  │  │
    │  │  Load2 → L1 Cache → CDB (result: F2 = 2.0)                                            │  │  │
    │  │  Mul1: Vj=1.0, Vk=2.0 → FPU → CDB (result: F3 = 2.0)                                   │  │  │
    │  │  Add1: Vj=2.0, Vk=5.0 → ALU → CDB (result: F4 = 7.0)                                  │  │  │
    │  │  → All instructions executed out of order, committed in order                          │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 실행 방식 비교

| 방식 | 순서 | 파이프라인 효율 | 복잡도 | 전력 |
|------|------|-----------------|--------|------|
| **In-Order** | 순차대로 | 낮음 | 낮음 | 낮음 |
| **Out-of-Order** | 재배열 | 높음 | 높음 | 높음 |

### Reorder Buffer (ROB)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Reorder Buffer (In-Order Commit)                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Structure:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ROB Entry (32-256 entries)                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  Field      │  Description                                                       │  │  │
    │  │  │  ───────────────────────────────────────────────────────────────────────────────────│  │  │
    │  │  │  Busy       │  Entry is valid                                                   │  │  │
    │  │  │  Completed  │  Instruction finished execution                                    │  │  │
    │  │  │  Dest       │  Destination register                                              │  │  │
    │  │  │  Value      │  Result value (when completed)                                     │  │  │
    │  │  │  Exception  │  Exception flag (e.g., page fault)                                 │  │  │
    │  │  │  PC         │  Program counter (for branch misprediction recovery)               │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Commit Process:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Head Pointer (oldest instruction)                                                      │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Entry 0: Completed=Yes → COMMIT (write to architectural register)                   │  │  │
    │  │  Entry 1: Completed=Yes → COMMIT                                                     │  │  │
    │  │  Entry 2: Completed=No  → STALL (wait for execution)                                  │  │  │
    │  │  Entry 3: Completed=Yes → STALL (wait for #2, in-order commit)                        │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │  → Instructions commit in program order even if executed out of order                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Speculation & Misprediction Recovery

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Speculative Execution & Recovery                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Branch Prediction & Speculation:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. BEQ R1, R2, Label (predicted: taken)                                                │  │
    │  2. ADD R3, R4, R5    (speculative)                                                      │  │
    │  3. SUB R6, R7, R8    (speculative)                                                      │  │
    │  4. MUL R9, R10, R11  (speculative)                                                      │  │
    │  Label: ADD R12, R13, R14                                                               │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Scenario 1: Prediction Correct (Branch Taken)
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Instructions 2-4 execute speculatively                                               │  │
    │  • Branch resolves: TAKEN (prediction correct)                                           │  │
    │  • Instructions 2-4 marked as non-speculative                                            │  │
    │  • Continue execution (no penalty)                                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Scenario 2: Misprediction (Branch Not Taken)
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Instructions 2-4 execute speculatively                                               │  │
    │  • Branch resolves: NOT TAKEN (prediction wrong)                                         │  │
    │  • Recovery:                                                                           │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. Flush ROB entries 2-4                                                           │  │  │
    │  │  2. Reset reservation stations                                                       │  │  │
    │  │  3. Fetch from correct address (Label)                                               │  │  │
    │  │  4. Continue execution                                                               │  │  │
    │  │  → Penalty: 10-20 cycles (pipeline flush)                                             │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 고성능 컴퓨터 아키텍처 설계
**상황**: 8-issue superscalar 프로세서
**판단**: Aggressive OoO + Speculation

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         High-Performance CPU Design                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Requirements:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 8 instructions per cycle (issue width)                                               │  │
    │  • 256 ROB entries (in-flight instructions)                                             │  │
    │  • 48 physical registers (rename pool)                                                   │  │
    │  • 4 integer ALUs, 2 FP units, 2 load/store units                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Key Features:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Register Rename:                                                                     │  │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • 16 architectural registers (RAX, RBX, ...)                                       │  │  │
    │  │  • 160 physical registers (10x architectural)                                         │  │  │
    │  │  • RAT (Register Alias Table) maps arch → physical                                   │  │  │
    │  │  → Eliminates WAR, WAW hazards                                                       │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  2. Reservation Stations:                                                                │  │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • 20 integer RS entries                                                              │  │  │
    │  │  • 15 FP RS entries                                                                   │  │  │
    │  │  • 12 memory RS entries                                                               │  │  │
    │  │  • Wakeup: Broadcast results on CDB, wakeup dependent instructions                   │  │  │
    │  │  → Instructions execute as soon as operands ready                                     │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  3. Reorder Buffer:                                                                      │  │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • 256 entries (maintain program order)                                              │  │  │
    │  │  • In-order commit (head must complete before tail commits)                          │  │  │
    │  │  → Precise exceptions (can recover from any instruction)                              │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  4. Speculation:                                                                         │  │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  • Branch predictor: 2-level adaptive + bimodal (95% accuracy)                        │  │  │
    │  │  • Return address stack (RAS): 16 entries (call/return prediction)                    │  │  │
    │  │  • Memory disambiguation: Predict load/store dependencies                             │  │  │
    │  │  → Speculate aggressively, recover quickly on misprediction                            │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 비순차 실행 기대 효과

| 메트릭 | In-Order | Out-of-Order | 개선 |
|--------|----------|--------------|------|
| **IPC** | 0.5-1.0 | 1.5-3.0 | 2-3x |
| **파이프라인 효율** | 50% | 80% | 60% |
| **전력** | 10W | 30W | -200% |
| **복잡도** | 낮음 | 높음 | - |

### 모범 사례

1. **Rename**: 많은 physical 레지스터
2. **RS**: 충분한 entries
3. **ROB**: 큰 사이즈
4. **Speculation**: 정확한 예측

### 미래 전망

1. **SMT**: Hyper-Threading
2. **데이터플로우**: CGRA
3. **AI**: 예측 강화
4. **에너지**: 효율 개선

### ※ 참고 표준/가이드
- **Intel**: Microarchitecture
- **AMD**: Zen Architecture
- **ARM**: Cortex Guide

---

## 📌 관련 개념 맵

- [파이프라인](./5_pipeline/85_pipeline.md) - 기본
- [분기 예측](./15_branch_prediction/130_branch_prediction.md) - Speculation
- [스펙터레이터](./16_security/131_speculative_execution.md) - 보안
