+++
title = "산술 논리 장치 (ALU, Arithmetic Logic Unit)"
date = 2025-02-27

[extra]
categories = "pe_exam-컴퓨터구조"
+++

# 산술 논리 장치 (ALU, Arithmetic Logic Unit)

## 핵심 인사이트 (3줄 요약)
> CPU 내에서 **모든 산술 연산과 논리 연산을 수행**하는 핵심 회로다. 두 개의 입력을 받아 연산 코드(Opcode)에 따라 덧셈·뺄셈·AND·OR 등을 수행하고 결과와 상태 플래그를 출력한다. 현대 CPU는 정수 ALU, 부동소수점 FPU, 벡터 ALU로 분화되어 있다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 산술 논리 장치(Arithmetic Logic Unit, ALU)는 CPU의 데이터 처리 핵심 회로로, 산술 연산(덧셈, 뺄셈, 곱셈, 나눗셈)과 논리 연산(AND, OR, NOT, XOR), 시프트 연산을 수행하는 디지털 회로다.

> 💡 **비유**: ALU는 **초능력 계산기**와 같다. 숫자를 넣으면 덧셈뺄셈도 하고, 참/거짓 판단도 하고, 왼쪽/오른쪽으로 숫자를 밀 수도 있는 만능 계산기다.

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점**: 초기 컴퓨터(ENIAC 등)는 연산마다 별도의 하드웨어가 필요했고, 프로그래밍이 물리적 배선 변경으로 이루어져 매우 비효율적이었다.
2. **기술적 필요성**: 폰 노이만 구조의 등장으로 저장된 프로그램 개념이 도입되면서, 명령어에 따라 다양한 연산을 수행하는 범용 연산 장치가 필요했다.
3. **시장/산업 요구**: 과학 계산, 비즈니스 데이터 처리, 실시간 제어 등 다양한 응용 분야에서 하나의 하드웨어로 여러 연산을 수행해야 하는 요구가 증가했다.

**핵심 목적**: 최소한의 하드웨어로 최대한의 연산 기능을 제공하여, CPU의 범용성과 프로그래밍 유연성을 실현하는 것이다.

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| 입력 레지스터 | 피연산자 A, B 저장 | 32/64비트 폭 | 재료 그릇 |
| 연산 선택기 | Opcode에 따라 연산 선택 | MUX로 구현 | 요리 방법 선택 |
| 가산기(Adder) | 덧셈/뺄셈 수행 | Ripple/Carry Lookahead | 숫자 더하기 |
| 논리 연산기 | AND, OR, NOT, XOR 수행 | 게이트 조합 | 참/거짓 판단 |
| 시프터 | 비트 이동 연산 | Barrel Shifter | 자릿수 옮기기 |
| 비교기 | 두 수의 대소 비교 | 뺄셈 결과 활용 | 크기 비교 |
| 출력 MUX | 연산 결과 중 하나 선택 | Opcode로 제어 | 결과 선택 |
| 상태 레지스터 | 연산 결과 상태 저장 | Z, C, N, V 플래그 | 결과 요약 |

**구조 다이어그램** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────┐
│                    ALU 내부 구조 상세도                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   입력 A ───┬────────────────────────────────────────┐         │
│   [31:0]    │                                        │         │
│             │    ┌─────────────────────────────┐     │         │
│             ├───→│      가산기 (Adder)         │────┐│         │
│             │    │  [A + B, A - B, Increment]  │    ││         │
│             │    └─────────────────────────────┘    ││         │
│             │                                        ││         │
│             │    ┌─────────────────────────────┐    ││         │
│             ├───→│    논리 연산기 (Logic)      │────┼┤         │
│             │    │  [AND, OR, XOR, NOT]        │    ││         │
│             │    └─────────────────────────────┘    ││         │
│   입력 B ───┤                                        ││         │
│   [31:0]    │    ┌─────────────────────────────┐    ││         │
│             ├───→│    시프터 (Shifter)         │────┼┤         │
│             │    │  [SHL, SHR, ROTATE]         │    ││         │
│             │    └─────────────────────────────┘    ││         │
│             │                                        ││         │
│             │    ┌─────────────────────────────┐    ││         │
│             └───→│    비교기 (Comparator)      │────┼┤         │
│                  │  [A == B, A < B, A > B]     │    ││         │
│                  └─────────────────────────────┘    ││         │
│                                                      ││         │
│   Opcode ────────────→ [연산 선택 MUX] ─────────────┘│         │
│   [3:0]                                               │         │
│                                                       ▼         │
│                                               ┌───────────┐     │
│                                               │  Result   │     │
│                                               │  [31:0]   │     │
│                                               └─────┬─────┘     │
│                                                     │           │
│                                                     ▼           │
│                                              ┌─────────────┐    │
│                                              │ Status Flags│    │
│                                              │ Z C N V     │    │
│                                              └─────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):
```
① 입력 로드 → ② Opcode 해석 → ③ 연산 수행 → ④ 결과 선택 → ⑤ 플래그 갱신
```

- **1단계 (입력 로드)**: 레지스터 A, B에 피연산자 로드. 데이터 경로를 통해 레지스터 파일 또는 메모리에서 전달.
- **2단계 (Opcode 해석)**: 제어 유닛이 Opcode를 해석하여 ALU에 연산 선택 신호 전송. 4비트 Opcode로 최대 16가지 연산 선택 가능.
- **3단계 (연산 수행)**: 모든 연산 유닛(가산기, 논리기, 시프터, 비교기)이 병렬로 동작하며 각각의 결과 생성.
- **4단계 (결과 선택)**: MUX가 Opcode에 따라 올바른 연산 결과를 선택하여 출력. 나머지 결과는 폐기.
- **5단계 (플래그 갱신)**: 연산 결과에 따라 상태 레지스터의 Z(Zero), C(Carry), N(Negative), V(Overflow) 플래그 설정.

**전가산기 구조 상세**:
```
┌─────────────────────────────────────────────────────────────────┐
│                    32비트 가산기 구조                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   전가산기(FA) 1비트 구조:                                       │
│                                                                 │
│       A ─────┐                                                  │
│              │    ┌─────────┐                                   │
│              ├────┤   XOR   ├─────── Sum                       │
│       B ─────┤    └─────────┘                                   │
│              │         │                                        │
│              │    ┌────┴────┐                                   │
│              └────┤   AND   ├──┐                                │
│                   └─────────┘  │   ┌─────────┐                  │
│       Cin ─────────────────────┼───┤   OR    ├─── Cout          │
│                                │   └─────────┘                  │
│              ┌─────────┐       │                                │
│       A,B ───┤   AND   ├───────┘                                │
│              └─────────┘                                        │
│                                                                 │
│   32비트 Ripple Carry Adder:                                    │
│   ┌─────┐   ┌─────┐   ┌─────┐       ┌─────┐                   │
│   │ FA  │──→│ FA  │──→│ FA  │──...──→│ FA  │                   │
│   │[0]  │   │[1]  │   │[2]  │       │[31] │                   │
│   └──┬──┘   └──┬──┘   └──┬──┘       └──┬──┘                   │
│      │         │         │             │                       │
│   A[0],B[0] A[1],B[1] A[2],B[2]    A[31],B[31]                 │
│                                                                 │
│   Carry Lookahead Adder (CLA):                                  │
│   Carry 생성: C[i+1] = G[i] + P[i]·C[i]                        │
│   Generate: G[i] = A[i] · B[i]                                  │
│   Propagate: P[i] = A[i] + B[i]                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**핵심 알고리즘/공식** (해당 시 필수):
```
산술 연산:
- 덧셈: Result = A + B
- 뺄셈: Result = A + (~B + 1)  (2의 보수 이용)
- 곱셈: Result = A × B (부분적 후 누적)
- 나눗셈: Result = A ÷ B (복원 나눗셈/비복원 나눗셈)

논리 연산:
- AND: Result = A AND B (비트별 논리곱)
- OR: Result = A OR B (비트별 논리합)
- XOR: Result = A XOR B (비트별 배타적 논리합)
- NOT: Result = ~A (비트별 부정)

시프트 연산:
- 논리 좌측 시프트: Result = A << n (0으로 채움)
- 논리 우측 시프트: Result = A >> n (0으로 채움)
- 산술 우측 시프트: Result = A >>> n (부호 비트로 채움)
- 순환 시프트: Result = (A << n) | (A >> (32-n))

상태 플래그:
- Z (Zero): Result == 0
- C (Carry): 덧셈 시 자리올림 발생
- N (Negative): Result < 0 (MSB = 1)
- V (Overflow): 부호 있는 연산 시 오버플로우
```

**코드 예시** (필수: Python 또는 의사코드):
```python
"""
ALU (Arithmetic Logic Unit) 시뮬레이터
32비트 정수 연산과 상태 플래그를 완전히 구현
"""

class ALU:
    """
    32비트 ALU 시뮬레이터
    산술 연산, 논리 연산, 시프트 연산을 수행하고
    상태 플래그(Z, C, N, V)를 갱신
    """

    # 연산 코드 정의
    OPCODES = {
        'ADD': 0x0, 'SUB': 0x1, 'AND': 0x2, 'OR': 0x3,
        'XOR': 0x4, 'NOT': 0x5, 'SHL': 0x6, 'SHR': 0x7,
        'MUL': 0x8, 'DIV': 0x9, 'CMP': 0xA, 'INC': 0xB,
        'DEC': 0xC, 'SAR': 0xD, 'ROL': 0xE, 'ROR': 0xF,
    }

    def __init__(self, bit_width=32):
        self.bit_width = bit_width
        self.max_value = (1 << bit_width) - 1
        self.sign_bit = 1 << (bit_width - 1)

        # 상태 플래그
        self.Z = 0  # Zero: 결과가 0
        self.C = 0  # Carry: 자리올림 발생
        self.N = 0  # Negative: 결과가 음수
        self.V = 0  # Overflow: 오버플로우 발생

    def _update_flags(self, result, carry=0, overflow=0):
        """연산 결과에 따라 상태 플래그 갱신"""
        # 32비트로 마스킹
        result_masked = result & self.max_value

        self.Z = 1 if result_masked == 0 else 0
        self.C = carry
        self.N = 1 if (result_masked & self.sign_bit) != 0 else 0
        self.V = overflow

        return result_masked

    def _to_signed(self, value):
        """부호 없는 값을 부호 있는 값으로 변환"""
        if value & self.sign_bit:
            return value - (1 << self.bit_width)
        return value

    def add(self, a, b):
        """덧셈: Result = A + B"""
        result = a + b
        carry = 1 if result > self.max_value else 0

        # 부호 있는 오버플로우 검사
        a_sign = (a & self.sign_bit) != 0
        b_sign = (b & self.sign_bit) != 0
        r_sign = (result & self.sign_bit) != 0
        overflow = 1 if (a_sign == b_sign and a_sign != r_sign) else 0

        return self._update_flags(result, carry, overflow)

    def sub(self, a, b):
        """뺄셈: Result = A - B (2의 보수 이용)"""
        b_complement = (~b + 1) & self.max_value
        return self.add(a, b_complement)

    def and_op(self, a, b):
        """논리 AND: Result = A AND B"""
        result = a & b
        return self._update_flags(result)

    def or_op(self, a, b):
        """논리 OR: Result = A OR B"""
        result = a | b
        return self._update_flags(result)

    def xor(self, a, b):
        """논리 XOR: Result = A XOR B"""
        result = a ^ b
        return self._update_flags(result)

    def not_op(self, a):
        """논리 NOT: Result = NOT A"""
        result = ~a
        return self._update_flags(result)

    def shl(self, a, n):
        """논리 좌측 시프트: Result = A << n"""
        result = (a << n) & self.max_value
        carry = 1 if (a & (self.sign_bit >> (n - 1))) != 0 else 0 if n > 0 else 0
        return self._update_flags(result, carry)

    def shr(self, a, n):
        """논리 우측 시프트: Result = A >> n (0으로 채움)"""
        result = a >> n
        carry = 1 if n > 0 and (a & (1 << (n - 1))) != 0 else 0
        return self._update_flags(result, carry)

    def sar(self, a, n):
        """산술 우측 시프트: Result = A >>> n (부호 유지)"""
        signed_a = self._to_signed(a)
        result = signed_a >> n
        return self._update_flags(result & self.max_value)

    def rol(self, a, n):
        """좌측 순환 시프트: Result = (A << n) | (A >> (32-n))"""
        n = n % self.bit_width
        result = ((a << n) | (a >> (self.bit_width - n))) & self.max_value
        return self._update_flags(result)

    def ror(self, a, n):
        """우측 순환 시프트: Result = (A >> n) | (A << (32-n))"""
        n = n % self.bit_width
        result = ((a >> n) | (a << (self.bit_width - n))) & self.max_value
        return self._update_flags(result)

    def mul(self, a, b):
        """곱셈: Result = A × B (하위 32비트만 반환)"""
        result = a * b
        # 곱셈은 64비트 결과이므로 하위 32비트만
        lower_32 = result & self.max_value

        # 부호 있는 곱셈 오버플로우 검사
        signed_a = self._to_signed(a)
        signed_b = self._to_signed(b)
        signed_result = signed_a * signed_b
        overflow = 1 if signed_result != self._to_signed(lower_32) else 0

        return self._update_flags(result, overflow=overflow)

    def div(self, a, b):
        """나눗셈: Result = A ÷ B"""
        if b == 0:
            raise ZeroDivisionError("Division by zero")

        signed_a = self._to_signed(a)
        signed_b = self._to_signed(b)

        # 파이썬은 //가 내림이므로 trunc toward zero 구현
        if (signed_a < 0) != (signed_b < 0):
            result = -(-signed_a // signed_b) if signed_a < 0 else -(signed_a // -signed_b)
        else:
            result = signed_a // signed_b

        return self._update_flags(result & self.max_value)

    def cmp(self, a, b):
        """비교: A - B 수행 후 플래그만 갱신, 결과는 버림"""
        result = self.sub(a, b)
        return result

    def execute(self, opcode, a, b=0):
        """Opcode에 따라 연산 실행"""
        operations = {
            self.OPCODES['ADD']: lambda: self.add(a, b),
            self.OPCODES['SUB']: lambda: self.sub(a, b),
            self.OPCODES['AND']: lambda: self.and_op(a, b),
            self.OPCODES['OR']: lambda: self.or_op(a, b),
            self.OPCODES['XOR']: lambda: self.xor(a, b),
            self.OPCODES['NOT']: lambda: self.not_op(a),
            self.OPCODES['SHL']: lambda: self.shl(a, b),
            self.OPCODES['SHR']: lambda: self.shr(a, b),
            self.OPCODES['SAR']: lambda: self.sar(a, b),
            self.OPCODES['ROL']: lambda: self.rol(a, b),
            self.OPCODES['ROR']: lambda: self.ror(a, b),
            self.OPCODES['MUL']: lambda: self.mul(a, b),
            self.OPCODES['DIV']: lambda: self.div(a, b),
            self.OPCODES['CMP']: lambda: self.cmp(a, b),
            self.OPCODES['INC']: lambda: self.add(a, 1),
            self.OPCODES['DEC']: lambda: self.sub(a, 1),
        }

        if opcode in operations:
            return operations[opcode]()
        raise ValueError(f"Unknown opcode: {opcode}")

    def get_flags(self):
        """현재 플래그 상태 반환"""
        return {
            'Z': self.Z,
            'C': self.C,
            'N': self.N,
            'V': self.V
        }

    def flags_str(self):
        """플래그 문자열 표현"""
        return f"Z={self.Z} C={self.C} N={self.N} V={self.V}"


# 사용 예시
if __name__ == "__main__":
    alu = ALU(32)

    print("=== ALU 연산 시뮬레이션 ===\n")

    # 덧셈
    a, b = 100, 50
    result = alu.add(a, b)
    print(f"ADD: {a} + {b} = {result} | Flags: {alu.flags_str()}")

    # 뺄셈
    result = alu.sub(100, 50)
    print(f"SUB: 100 - 50 = {result} | Flags: {alu.flags_str()}")

    # 오버플로우 테스트
    result = alu.add(0x7FFFFFFF, 1)  # 최대 양수 + 1
    print(f"ADD (overflow): 0x7FFFFFFF + 1 = {result} (0x{result:08X}) | Flags: {alu.flags_str()}")

    # 논리 연산
    result = alu.and_op(0xFF00, 0x0FF0)
    print(f"AND: 0xFF00 & 0x0FF0 = 0x{result:04X} | Flags: {alu.flags_str()}")

    result = alu.or_op(0xFF00, 0x0FF0)
    print(f"OR:  0xFF00 | 0x0FF0 = 0x{result:04X} | Flags: {alu.flags_str()}")

    result = alu.xor(0xFF00, 0x0FF0)
    print(f"XOR: 0xFF00 ^ 0x0FF0 = 0x{result:04X} | Flags: {alu.flags_str()}")

    # 시프트 연산
    result = alu.shl(0x00000001, 4)
    print(f"SHL: 1 << 4 = 0x{result:08X} | Flags: {alu.flags_str()}")

    result = alu.shr(0x80000000, 4)
    print(f"SHR: 0x80000000 >> 4 = 0x{result:08X} | Flags: {alu.flags_str()}")

    result = alu.sar(0x80000000, 4)  # 부호 유지
    print(f"SAR: 0x80000000 >>> 4 = 0x{result:08X} | Flags: {alu.flags_str()}")

    # 순환 시프트
    result = alu.rol(0x80000001, 1)
    print(f"ROL: 0x80000001 ROL 1 = 0x{result:08X} | Flags: {alu.flags_str()}")

    # 곱셈/나눗셈
    result = alu.mul(123, 456)
    print(f"MUL: 123 × 456 = {result} | Flags: {alu.flags_str()}")

    result = alu.div(100, 7)
    print(f"DIV: 100 ÷ 7 = {result} | Flags: {alu.flags_str()}")

    # 비교
    alu.cmp(100, 100)
    print(f"CMP: 100 vs 100 | Flags: {alu.flags_str()} (Equal)")

    alu.cmp(50, 100)
    print(f"CMP: 50 vs 100 | Flags: {alu.flags_str()} (Less)")
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):
| 장점 | 단점 |
|-----|------|
| 범용 연산 지원 (산술+논리) | 복잡한 연산은 클럭 소요 |
| 작은 면적으로 다양한 기능 | 곱셈/나눗셈은 추가 하드웨어 필요 |
| 높은 클럭 주파수 가능 | 전력 소모 (활성 회로) |
| 파이프라인과 호환 | 데이터 의존성으로 해저드 발생 |
| 컴파일러 최적화 용이 | 정밀도 제한 (32/64비트) |

**대안 기술 비교** (필수: 최소 2개 대안):
| 비교 항목 | 정수 ALU | 부동소수점 FPU | 벡터 ALU (SIMD) |
|---------|---------|---------------|----------------|
| 핵심 특성 | ★ 정수 연산 전담 | 실수 연산 전문 | 병렬 데이터 처리 |
| 성능 | 1 클럭/연산 | 3~5 클럭/연산 | ★ 다중 데이터 동시 |
| 하드웨어 | 작음, 단순 | 큼, 복잡 | 중간~큼 |
| 정밀도 | 32/64비트 정수 | 32/64/128비트 실수 | 128/256/512비트 벡터 |
| 적합 환경 | 일반 프로그램 | 과학/그래픽 | ★ AI/이미지 처리 |
| 대표 예시 | ARM Cortex-A 정수부 | Intel x87 FPU | Intel AVX, ARM NEON |

> **★ 선택 기준**:
> - **정수 연산 위주**: 일반 ALU로 충분 (제어 로직, 인덱싱, 포인터 연산)
> - **과학 계산/그래픽**: FPU 필수 (3D 렌더링, 시뮬레이션, 수치 해석)
> - **AI/ML/이미지**: 벡터 ALU 최적 (행렬 연산, 필터링, 신경망 추론)

**연산별 성능 비교**:
| 연산 종류 | 일반 클럭 수 | 최신 CPU | 비고 |
|----------|------------|---------|------|
| 덧셈/뺄셈 | 1 | 0.5 (슈퍼스칼라) | 가장 기본 |
| 논리 연산 | 1 | 0.5 | 매우 빠름 |
| 시프트 | 1 | 1 | Barrel Shifter 사용 |
| 곱셈 | 3~5 | 3 | 부분적 후 누적 |
| 나눗셈 | 10~30 | 10~20 | 가장 느림 |
| 부동소수 덧셈 | 3~5 | 3 | FPU 사용 |
| 부동소수 곱셈 | 4~6 | 4 | FPU 사용 |

**기술 진화 계보** (해당 시):
```
[단일 ALU] → [정수 ALU + FPU 분리] → [멀티 ALU] → [벡터 ALU + AI 가속기]
  (초기)         (80386/80387)       (슈퍼스칼라)    (현대 CPU/GPU)
```

---

### Ⅳ. 실무 적용 방안 (필수: 전문가 판단력 증명)

**전문가적 판단** (필수: 3개 이상 시나리오):
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| CPU 설계 | 정수 ALU 4개 + FPU 2개 + 벡터 ALU 2개로 구성, 슈퍼스칼라로 병렬 실행 | IPC 4+ 달성 |
| GPU 설계 | 수천 개의 단순 ALU로 구성, SIMT 방식으로 병렬 처리 | 처리율 10TFLOPS+ |
| AI 가속기 | 텐서 연산에 특화된 행렬 ALU, INT8/FP16 지원 | AI 추론 100TOPS+ |

**실제 도입 사례** (필수: 구체적 기업/서비스):
- **사례 1 (Intel Core i9-13900K)**: 정수 ALU 6개 + FPU 2개 + 벡터 ALU(AVX-512) 2개로 구성. 슈퍼스칼라 아키텍처로 최대 IPC 6 달성. 24코어로 멀티스레딩 지원. SPEC CPU 2017 점수 500+ 기록.
- **사례 2 (NVIDIA H100)**: 16,896개의 CUDA 코어(각각 단순 ALU 포함) + 528개의 텐서 코어(행렬 ALU). FP8 연산으로 AI 학습 성능 4배 향상. GPT-3 학습 시간을 1일 이내로 단축.
- **사례 3 (Apple M3)**: 성능 코어(P-core)에 6개 ALU, 효율 코어(E-core)에 3개 ALU. 비대칭 구조로 성능과 전력 균형. MacBook Pro 18시간 배터리 달성.

**도입 시 고려사항** (필수: 4가지 관점):
1. **기술적**: ALU 개수와 종류 배치, 파이프라인 단수, 포워딩 경로, 전력 게이팅
2. **운영적**: 열 설계 전력(TDP), 클럭 주파수, 스로틀링 임계값, 모니터링
3. **보안적**: 스펙터/멜트다운 등 사이드 채널 공격 방어, 데이터 누출 방지
4. **경제적**: 다이 크기, 생산 수율, 테스트 비용, 전력 비용

**주의사항 / 흔한 실수** (필수: 최소 3개):
- ❌ 나눗셈 남용: 나눗셈은 10~30 클럭 소요, 곱셈과 역수로 대체 고려
- ❌ 정수 오버플로우 무시: 부호 있는 연산에서 V 플래그 확인 필수
- ❌ 부동소수 정밀도 과신: IEEE 754의 반올림 오차 고려 필요
- ❌ ALU 병목: 모든 연산이 ALU를 거치므로 I/O 바운드 작업과 밸런스 필요

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):
```
📌 ALU 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│  ALU 핵심 연관 개념 맵                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   CPU 구조 ←──→ [ALU] ←──→ 명령어 집합                          │
│       ↓           ↓            ↓                                │
│   제어 유닛    데이터 경로    파이프라인                         │
│       ↓           ↓            ↓                                │
│   레지스터     메모리 계층    해저드                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| CPU 구조 | 포함 관계 | ALU는 CPU의 핵심 구성 요소 | `[CPU 구조](./cpu_structure.md)` |
| 데이터 경로 | 직접 연결 | ALU와 레지스터를 연결하는 버스 | `[데이터 경로](./data_path.md)` |
| 제어 유닛 | 제어 관계 | ALU에 연산 선택 신호 전송 | `[제어 유닛](./control_unit.md)` |
| 명령어 사이클 | 실행 단계 | ALU는 Execute 단계에서 동작 | `[명령어 사이클](./instruction_cycle.md)` |
| 부동소수점 | 확장 연산 | FPU는 ALU의 부동소수점 확장 | `[부동소수점](./floating_point.md)` |
| SIMD/MIMD | 병렬화 | 벡터 ALU로 SIMD 구현 | `[SIMD MIMD](./simd_mimd.md)` |
| 캐리 룩어헤드 | 최적화 | 고속 가산기 알고리즘 | `[가산기](./adder.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 성능 | 다중 ALU로 병렬 실행 | IPC 4~6 달성 |
| 전력 | ALU 전력 게이팅 | 유휴 전력 50% 감소 |
| 면적 | 최적화된 ALU 설계 | 다이 크기 10% 절감 |
| 정밀도 | 64비트 연산 지원 | 수치 오차 0.5 ULP |

**미래 전망** (필수: 3가지 관점):
1. **기술 발전 방향**: AI 특화 텐서 ALU 확대, INT4/INT8 저정밀 연산 가속, 양자 연산(Qubit ALU) 연구. 3nm 이하 공정에서 ALU 면적 최적화.
2. **시장 트렌드**: Edge AI용 저전력 ALU 수요 급증, 클라우드용 고성능 벡터 ALU 지속 진화. 이종 코어(성능/효율) 조합이 표준화.
3. **후속 기술**: 광 연산(Optical ALU), 뉴로모픽(Neuromorphic) 연산 장치, MEMS 기반 아날로그 연산 장치.

> **결론**: ALU는 CPU의 연산 능력을 결정하는 핵심 회로로, 정수/부동소수점/벡터 연산으로 분화 발전하고 있다. AI 시대에는 텐서 연산 특화 ALU가 새로운 표준으로 자리 잡을 것이다.

> **※ 참고 표준**: IEEE 754 (부동소수점), IEEE 1149.1 (JTAG), ARM Architecture Reference Manual, Intel 64 and IA-32 Architectures Software Developer's Manual

---

## 어린이를 위한 종합 설명 (필수)

**산술 논리 장치(ALU)를 쉽게 이해해보자!**

ALU는 마치 **초능력을 가진 만능 계산기**와 같아요.

**첫 번째 이야기: 숫자 계산 마법사**
평범한 계산기는 더하기랑 빼기만 할 수 있어요. 하지만 ALU는 달라요! 덧셈, 뺄셈은 물론 곱셈, 나눗셈까지 척척 해내요. 100 + 50 = 150, 10 × 10 = 100, 모든 숫자 계산을 한눈에 해결해요.

**두 번째 이야기: 참/거짓 판단관**
ALU는 숫자뿐만 아니라 참과 거짓도 구별할 수 있어요. "5가 3보다 크니?"라고 물으면 "참!"이라고 대답해요. "둘 다 같은 숫자니?"라고 물으면 비교해서 알려줘요. 컴퓨터 게임에서 "점수가 100점을 넘었니?"를 판단하는 것도 ALU가 해요.

**세 번째 이야기: 비트 이동술사**
ALU는 숫자를 왼쪽이나 오른쪽으로 옮길 수 있어요. 1을 왼쪽으로 한 칸 옮기면 2가 되고, 또 옮기면 4가 돼요. 마치 숫자가 늘어나는 마법! 이걸로 2배, 4배, 8배를 아주 빠르게 만들 수 있어요.

**ALU의 네 가지 신호등**
ALU는 일을 마치면 네 개의 신호등을 켜요:
- **Z (Zero)**: 결과가 0이야! (모든 숫자가 같으면 켜짐)
- **C (Carry)**: 숫자가 너무 커서 자리가 넘쳤어! (덧셈할 때 올림)
- **N (Negative)**: 결과가 마이너스야! (음수)
- **V (Overflow)**: 숫자가 너무 커서 담을 수 없어! (오버플로우)

이렇게 ALU는 컴퓨터의 "계산 두뇌" 역할을 하면서, 모든 연산을 뚝딱뚝딱 해결해요!

---
