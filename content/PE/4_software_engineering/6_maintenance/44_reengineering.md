+++
title = "44. 소프트웨어 재공학 (Re-engineering)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["Re-engineering", "Reverse-Engineering", "Restructuring", "Legacy-System"]
draft = false
+++

# 소프트웨어 재공학 (Re-engineering)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 재공학은 **"기존 **소프트웨어**를 **분석**하고 **변경**하여 **품질**을 **향상**하거나 **새로운 **기술**로 **이전**하는 **체계적 **활동\\\"**으로, **역공학**(Reverse Engineering)과 **순공학**(Forward Engineering)으로 **구성**된다.
> 2. **단계**: **1단계**(역공학)으로 **기존 **시스템**을 **이해**하고 **2단계**(재구조)로 **코드**를 **개선**하며 **3단계**(순공학)으로 **새로운 **아키텍처**로 **이전**한다.
> 3. **활용**: **레거시 **시스템 **현대화**, **플랫폼 **이동**, **유지보수 **성능 **향상**에 **사용**되며 **자동화 **도구**가 **필수**적이다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
재공학은 **"소프트웨어 개선 이전 프로젝트"**이다.

**재공학 구성**:
| 활동 | 목적 | 산출물 |
|------|------|--------|
| **역공학** | 기존 시스템 이해 | 설계서, 문서 |
| **재구조** | 코드 개선 | 리팩토링된 코드 |
| **순공학** | 새 아키텍처 | 새 시스템 |

### 💡 비유
재공학은 **건물 리모델링**과 같다.
- **역공학**: 구조 파악
- **재구조**: 내부 수리
- **순공학**: 새 건축

---

## Ⅱ. 아키텍처 및 핵심 원리

### 재공학 3단계 모델

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Re-engineering Three-Stage Model                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Stage 1: Reverse Engineering (역공학)
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Goal: Understand existing system                                                       │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Source Code ──Analysis──→ Abstractions ──Documentation──► Design Docs            │  │  │
    │  │  (Implementation)            │            │                │                        │  │  │
    │  │                             ▼            ▼                │                        │  │  │
    │  │                         Functions    Patterns         │                        │  │  │
    │  │                         Modules      Relationships   │                        │  │  │
    │  │                         Data Flow    Business Logic │                        │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Techniques:                                                                            │  │
    │  • Static analysis (code without executing)                                              │  │
    │  • Dynamic analysis (code execution tracing)                                             │  │
    │  • Data flow analysis                                                                   │  │
    │  • Control flow analysis                                                                 │  │
    │  • Pattern recognition (design patterns, anti-patterns)                                   │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
                            ↓
    Stage 2: Restructuring (재구조)
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Goal: Improve code quality without changing functionality                               │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Legacy Code ──Transform──► Restructured Code ──Verify──► Same Behavior            │  │  │
    │  │  (Low Quality)               │                         │                            │  │  │
    │  │                             ▼                         │                            │  │  │
    │  │                         Better                    │                            │  │  │
    │  │                         • Readability              │                            │  │  │
    │  │                         • Maintainability          │                            │  │  │
    │  │                         • Testability              │                            │  │  │
    │  │                         • Performance              │                            │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Techniques:                                                                            │  │
    │  • Refactoring (extract method, rename, etc.)                                           │  │
    │  • Code normalization (style, formatting)                                               │  │
    │  • Dead code elimination                                                                │  │
    │  • Optimization                                                                         │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
                            ↓
    Stage 3: Forward Engineering (순공학)
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Goal: Create new system with modern architecture                                      │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Understanding ──Design──► New Architecture ──Implement──► New System              │  │  │
    │  │  (from Stage 1)      │                    │                │                     │  │  │
    │  │                      ▼                    ▼                │                     │  │  │
    │  │                  New Requirements    Modern Tech       │                     │  │  │
    │  │                  New Platforms       Cloud/Micro       │                     │  │  │
    │  │                  New Standards        Containers        │                     │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Approaches:                                                                            │  │
    │  • Big Bang: Complete replacement (risky)                                                 │  │
    │  • Incremental: Gradual migration (recommended)                                          │  │
    │  • Parallel: Old and new run together                                                   │  │
    │  • Strangler: Replace piece by piece                                                    │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 역공학 도구 및 기법

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Reverse Engineering Tools & Techniques                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. Static Analysis Tools:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • SonarQube: Code quality, technical debt, vulnerabilities                             │  │
    │  • Cast: Software analysis, security weaknesses                                         │  │
    │  • PMD/Checkstyle/ESLint: Language-specific rules                                       │  │
    │  • Doxygen: Documentation generation from comments                                      │  │
    │  │                                                                                      │  │
    │  Output Examples:                                                                       │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Call graphs: Function invocation hierarchy                                         │  │  │
    │  │  • Control flow graphs: Decision paths                                               │  │  │
    │  │  • Data flow diagrams: Variable usage                                                  │  │  │
    │  │  • Dependency graphs: Module relationships                                            │  │  │
    │  │  • Complexity metrics: Cyclomatic, cognitive, maintainability                          │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. Dynamic Analysis Tools:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Profilers: gprof, perf, VisualVM (performance hotspots)                            │  │
    │  • Tracers: strace, ltrace, DTrace (system calls)                                      │  │
    │  • Debuggers: gdb, WinDbg (runtime inspection)                                           │  │
    │  • Memory analyzers: Valgrind, AddressSanitizer                                          │  │
    │                                                                                         │  │
    │  Insights from Dynamic Analysis:                                                        │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Actual execution paths vs intended                                                 │  │  │
    │  │  • Performance bottlenecks                                                            │  │  │
    │  │  • Memory leaks, buffer overflows                                                     │  │  │
    │  │  • Concurrency issues (race conditions, deadlocks)                                   │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    3. Pattern Recognition:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Design Patterns:                                                                        │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Identify: Singleton, Factory, Observer, Strategy, etc.                           │  │  │
    │  │  → Understand architectural decisions                                                  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Anti-Patterns:                                                                         │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • God Object: One class does everything                                            │  │  │
    │  │  • Spaghetti Code: Tangled control flow                                               │  │  │
    │  │  • Copy-Paste: Duplicated code                                                        │  │  │
    │  │  → Candidates for refactoring                                                         │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 재공학 vs 재작성

| 관점 | 재공학 | 재작성(Rewrite) |
|------|---------|-----------------|
| **기존 자산** | 활용 | 버전 |
| **위험** | 낮음 | 높음 |
| **비용** | 중간 | 높음 |
| **기간** | 중간 | 길음 |
| **지식 보존** | 유지 | 상실 |

### 재공학 전략

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Re-engineering Strategies                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. Big Bang Strategy (일시 교체):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Approach: Replace entire system at once                                                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Legacy System  │────────│  (Switchover)  │  New System                         │  │  │
    │  │  ────────────────│  Stop  │  ──────────────│  Start                             │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Advantages:                                                                            │  │
    │  • Clean break with legacy                                                               │  │
    │  • No integration complexity                                                            │  │
    │                                                                                         │  │
    │  Disadvantages:                                                                         │  │
    │  • High risk (all-or-nothing)                                                            │  │
    │  • Long period of unavailability                                                       │  │
    │  • Data migration challenges                                                             │  │
    │  • User disruption                                                                       │  │
    │                                                                                         │  │
    │  Use case: Small, non-critical systems                                                   │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. Incremental Strategy (점진적 이전):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Approach: Replace module by module                                                      │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Phase 1: Module A (Legacy) ──→ Module A (New)                                     │  │  │
    │  │  Phase 2: Module B (Legacy) ──→ Module B (New)                                     │  │  │
    │  │  Phase 3: Module C (Legacy) ──→ Module C (New)                                     │  │  │
    │  │  ...                                                                                  │  │  │
    │  │  ┌──────────────────────┐     ┌──────────────────────┐                            │  │  │
    │  │  │ Legacy System        │────▶│ New System            │                            │  │  │
    │  │  │ (Remaining modules)  │     │ (Completed modules) │                            │  │  │
    │  │  └──────────────────────┘     └──────────────────────┘                            │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Advantages:                                                                            │  │
    │  • Lower risk (gradual change)                                                           │  │
    │  • Continuous operation                                                                 │  │
    │  • Early feedback                                                                       │  │
    │                                                                                         │  │
    │  Disadvantages:                                                                         │  │
    │  • Integration complexity (legacy + new)                                                │  │
    │  • Longer overall timeline                                                               │  │
    │  • Dual system maintenance                                                              │  │
    │                                                                                         │  │
    │  Use case: Large, critical systems                                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    3. Strangler Fig Strategy (스트랭글 패턴):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Approach: Wrap legacy, replace from inside                                              │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  API Gateway / Facade Layer                                                          │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐ │  │  │
    │  │  │  Request ──▶ Router ──▶ [New] if implemented                                  │ │  │  │
    │  │  │                    │                                                          │ │  │  │
    │  │  │                    └─▶ [Legacy] if not                                     │ │  │  │
    │  │  │                    │                                                          │ │  │  │
    │  │  │  Response ◀───────────────────────────────────────────────────────────────────│ │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘ │  │  │
    │  │                                                                                      │  │  │
    │  │  Migration steps:                                                                    │  │  │
    │  │  1. Identify boundary (API)                                                           │  │  │
    │  │  2. Create facade/proxy                                                               │  │  │
    │  │  3. Implement new service behind facade                                               │  │  │
    │  │  4. Route traffic to new                                                              │  │  │
    │  │  5. Decommission legacy                                                                │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Advantages:                                                                            │  │
    │  • Zero downtime possible                                                                │  │
    │  • Easy rollback                                                                         │  │
    │  • Gradual migration                                                                     │  │
    │                                                                                         │  │
    │  Use case: Web applications, microservices migration                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 레거시 COBOL 시스템 현대화
**상황**: 30년된 은행 코어 시스템
**판단**: 재공학 vs 재작성

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Legacy System Modernization Decision                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    System Characteristics:
    • 2 million lines of COBOL code
    • 5000+ programs, 3000+ files
    • Critical business logic (proven, tested)
    • No original developers
    • Tight coupling to mainframe hardware

    Analysis:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Option 1: Complete Rewrite                                                               │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Cost: $10-50 million, 3-5 years                                                      │  │  │
    │  │  Risk: Very high (business logic may be lost or misinterpreted)                       │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐ │  │  │
    │  │  │ Risk Examples:                                                                      │ │  │  │
    │  │  │ • Interest calculation rounding errors (financial impact)                        │ │  │  │
    │  │  │ • Regulatory compliance violations                                                 │ │  │  │
    │  │  │ • Data corruption during migration                                                   │ │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘ │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Option 2: Re-engineering (Recommended)                                                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Phase 1: Reverse Engineering                                                          │  │  │
    │  │  • Extract business rules from code                                                    │  │  │
    │  │  • Document data structures and flows                                                   │  │  │
    │  │  • Identify critical modules (high usage, high complexity)                              │  │  │
    │  │                                                                                      │  │  │
    │  │  Phase 2: Incremental Migration                                                         │  │  │
    │  │  • Select non-critical module first (e.g., reporting)                                 │  │  │
    │  │  • Implement in modern language (Java/Go) with same business logic                    │  │  │
    │  │  • Run parallel, verify outputs match                                                  │  │  │
    │  │  • Cut over to new module                                                            │  │  │
    │  │  • Repeat for other modules                                                            │  │  │
    │  │                                                                                      │  │  │
    │  │  Phase 3: Legacy Decommission                                                         │  │  │
    │  │  • Retire mainframe when all modules migrated                                         │  │  │
    │  │                                                                                      │  │  │
    │  │  Cost: $5-20 million, 2-4 years                                                      │  │  │
    │  │  Risk: Lower (proven business logic preserved)                                        │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Decision: Re-engineering with incremental migration                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 자동화 도구 활용

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Automated Re-engineering                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Code Analysis Automation:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. AST-Based Analysis:                                                                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Parse code → Abstract Syntax Tree → Pattern Matching → Refactoring Suggestions       │  │  │
    │  │                                                                                      │  │  │
    │  │  Example: Convert Java 6 code to Java 17                                             │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐ │  │  │
    │  │  │  Before:                                                                             │ │  │  │
    │  │  │  List<String> list = new ArrayList<String>();                                      │ │  │  │
    │  │  │  for (String s : list) {                                                             │ │  │  │
    │  │  │      System.out.println(s);                                                         │ │  │  │
    │  │  │  }                                                                                   │ │  │  │
    │  │  │                                                                                      │ │  │  │
    │  │  │  After (automatic refactoring):                                                     │ │  │  │
    │  │  │  list.forEach(System.out::println);                                                 │ │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘ │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  2. Pattern-Based Refactoring:                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Tools: IntelliJ IDEA, Eclipse, VS Code                                               │  │  │
    │  │  Capabilities:                                                                         │  │  │
    │  │  • Extract method, inline method                                                        │  │  │
    │  │  • Rename variable, move class                                                         │  │  │
    │  │  • Introduce design pattern                                                            │  │  │
    │  │  • Eliminate code duplication                                                          │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Translation Tools (Legacy to Modern):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Language Translation:                                                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Source │  Target   │  Tools                            │  Accuracy                      │  │  │
    │  │  ─────────────────────────────────────────────────────────────────────────────────────│  │  │
    │  │  COBOL  │  Java     │  IBM Migration Kit, Custom     │  70-80% (manual fix needed)     │  │  │
    │  │  VB6    │  C#       │  Microsoft Upgrade Wizard        │  85-90%                        │  │  │
    │  │  Perl   │  Python   │  perthon, manual               │  60-70%                        │  │  │
    │  │  PHP 5  │  PHP 7    │  PHP Migration, Rector         │  90-95%                        │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Translation Process:                                                                    │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. Automated translation (tool)                                                       │  │  │
    │  │  2. Syntax error correction                                                            │  │  │
    │  │  3. Semantic equivalence verification                                                 │  │  │
    │  │  4. Performance testing                                                                │  │  │
    │  │  5. Manual review and optimization                                                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 재공학 기대 효과

| 시나리오 | 최적 전략 | 예상 기간 |
|----------|-----------|----------|
| **소형 시스템** | 재작성 | 3-6월 |
| **중형 시스템** | 점진적 재공학 | 6-18월 |
| **대형 시스템** | Strangler | 18-36월 |
| **비즈니스 크리티컬** | 병행 운영 | 12-24월 |

### 모범 사례

1. **역공학**: 문서화 우선
2. **자동화**: 도구 활용
3. **테스트**: 병렬 검증
4. **롤백**: 언제든 가능

### 미래 전망

1. **AI 자동화**: LLM 기반 번역
2. **CI/CD**: 재공학 파이프라인
3. **컨테이너**: 마이크로서비스화
4. **클라우드**: 호환성 유지

### ※ 참고 표준/가이드
- **IEEE**: 1471 (아키텍처)
- **ISO**: 9126 (품질)
- **OMG**: MDA (모델 주도)
- **SEI**: Re-engineering 가이드

---

## 📌 관련 개념 맵

- [리팩토링](./42_refactoring.md) - 코드 개선
- [역공학](./45_reverse_engineering.md) - 심화
- [CI/CD](./44_cicd.md) - 자동화
- [레거시](./28_ide.md) - 현대화
