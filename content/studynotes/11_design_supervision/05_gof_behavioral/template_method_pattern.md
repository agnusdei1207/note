+++
title = "템플릿 메서드 패턴 (Template Method Pattern)"
categories = ["studynotes-11_design_supervision"]
+++

# 템플릿 메서드 패턴 (Template Method Pattern)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 템플릿 메서드 패턴은 부모(추상) 클래스에 **알고리즘의 전체 뼈대(템플릿)**를 정의하고, 세부 구현은 자식(구체) 클래스로 **지연(W Deferred)**시켜 오버라이딩하는 행위 패턴입니다.
> 2. **가치**: 코드 중복을 제거하고, 알고리즘의 구조는 유지하면서 세부 단계만 다르게 구현할 수 있어, Hollywood Principle("Don't call us, we'll call you")의 핵심 구현입니다.
> 3. **융합**: 스프링의 JdbcTemplate, HttpServlet의 service(), Android의 Activity 생명주기, 그리고 팩토리 메서드 패턴의 기반이 됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 템플릿 메서드 패턴의 정의
템플릿 메서드(Template Method) 패턴은 **"작업에서 알고리즘의 골격을 정의하고, 일부 단계는 서브클래스에서 구현"**하는 패턴입니다. 상위 클래스는 불변하는 알고리즘 구조를 정의하고, 변하는 부분은 하위 클래스가 구현합니다.

### 💡 비유: 요리 레시피
라면을 끓이는 **기본 틀**은 같습니다: 물 끓이기 → 면 넣기 → 스프 넣기 → 완성. 하지만 **세부 방식**은 다를 수 있습니다. 물 양, 끓이는 시간, 추가 재료 등. 템플릿 메서드는 이 기본 틀을 제공하는 것입니다.

### 2. 등장 배경
- **코드 중복**: 여러 클래스에서 동일한 알고리즘 구조 중복
- **확장성**: 알고리즘 일부만 다르게 구현하고 싶음
- **제어 역전**: 부모가 자식을 호출하는 구조

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 템플릿 메서드 구조 다이어그램

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                     템플릿 메서드 패턴 구조                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    AbstractClass                                     │   │
│   ├─────────────────────────────────────────────────────────────────────┤   │
│   │  + templateMethod()           // 템플릿 메서드 (final)                │   │
│   │    step1()                    // 구현된 메서드                        │   │
│   │    step2()                    // 추상 메서드 (서브클래스 구현)          │   │
│   │    step3()                    // 훅 메서드 (선택적 오버라이드)          │   │
│   │                                                                     │   │
│   │  // 구현                                                            │   │
│   │  fun templateMethod() {                                             │   │
│   │    step1()           // 공통 구현                                   │   │
│   │    step2()           // 서브클래스에서 구현                          │   │
│   │    step3()           // 선택적 오버라이드                            │   │
│   │  }                                                                  │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                  ▲                                          │
│                                  │ extends                                  │
│                 ┌────────────────┴────────────────┐                        │
│                 │                                 │                        │
│   ┌─────────────────────────┐     ┌─────────────────────────┐              │
│   │    ConcreteClassA       │     │    ConcreteClassB       │              │
│   ├─────────────────────────┤     ├─────────────────────────┤              │
│   │  + step2()  // 구체구현  │     │  + step2()  // 구체구현  │              │
│   │  + step3()  // 오버라이드│     │  (step3 오버라이드 안 함)│              │
│   └─────────────────────────┘     └─────────────────────────┘              │
│                                                                             │
│   [호출 흐름 - Hollywood Principle]                                         │
│   Client ──► AbstractClass.templateMethod()                                │
│                    │                                                        │
│                    ├─► step1() (AbstractClass)                             │
│                    ├─► step2() (ConcreteClass)  ← 제어 역전                │
│                    └─► step3() (ConcreteClass)  ← 제어 역전                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 핵심 구성 요소

| 구성 요소 | 유형 | 설명 |
|:---:|:---|:---|
| **템플릿 메서드** | final/concrete | 알고리즘 뼈대 정의, 오버라이드 금지 |
| **추상 메서드** | abstract | 서브클래스가 반드시 구현 |
| **훅 메서드** | virtual (기본 구현) | 선택적 오버라이드 |
| **구체 메서드** | final | 공통 구현, 오버라이드 금지 |

### 3. 구현 예시: 데이터 처리 파이프라인

```kotlin
// Abstract Class
abstract class DataProcessor {

    // 템플릿 메서드 (final - 오버라이드 금지)
    fun process(filename: String): String {
        val data = readData(filename)      // 1. 데이터 읽기
        val parsed = parseData(data)       // 2. 데이터 파싱 (추상)
        val processed = transformData(parsed) // 3. 데이터 변환 (추상)
        val result = validateData(processed)  // 4. 데이터 검증 (훅)
        return saveData(result)            // 5. 데이터 저장
    }

    // 공통 구현
    private fun readData(filename: String): String {
        println("파일 읽기: $filename")
        return "raw data from $filename"
    }

    // 추상 메서드 - 서브클래스 필수 구현
    protected abstract fun parseData(data: String): Any
    protected abstract fun transformData(data: Any): Any

    // 훅 메서드 - 선택적 오버라이드
    protected open fun validateData(data: Any): Any {
        println("기본 검증 수행")
        return data
    }

    // 공통 구현
    private fun saveData(data: Any): String {
        println("데이터 저장")
        return "SUCCESS: $data"
    }
}

// Concrete Class A - CSV 처리
class CsvProcessor : DataProcessor() {
    override fun parseData(data: String) = data.split(",")
    override fun transformData(data: Any) = (data as List<*>).map { it.toString().uppercase() }
    override fun validateData(data: Any): Any {
        println("CSV 형식 검증")
        return data
    }
}

// Concrete Class B - JSON 처리
class JsonProcessor : DataProcessor() {
    override fun parseData(data: String) = mapOf("key" to data)
    override fun transformData(data: Any) = (data as Map<*, *>)["key"]
    // validateData는 기본 구현 사용
}

// 사용
fun main() {
    val csvProcessor = CsvProcessor()
    csvProcessor.process("data.csv")

    val jsonProcessor = JsonProcessor()
    jsonProcessor.process("data.json")
}
```

### 4. 할리우드 원칙 (Hollywood Principle)

```text
[할리우드 원칙]
"Don't call us, we'll call you"
(우리에게 연락하지 마세요, 우리가 연락할게요)

[구조 비교]

일반적인 제어 흐름:
Client ──► SubClass.method() ──► 로직 수행
        (서브클래스가 능동적으로 호출)

템플릿 메서드:
Client ──► AbstractClass.templateMethod() ──► SubClass.abstractMethod()
        (부모가 자식을 호출 - 제어 역전)

IoC(Inversion of Control)의 한 형태
```

### 5. 훅 메서드 (Hook Method)

```text
[훅 메서드 패턴]

abstract class HookExample {
    // 템플릿 메서드
    fun execute() {
        beforeExecute()    // 전처리 훅
        doWork()          // 핵심 작업
        afterExecute()    // 후처리 훅
    }

    abstract fun doWork()

    // 훅 메서드 - 기본 구현이 비어있거나 trivial
    protected open fun beforeExecute() {}  // 아무것도 안 함
    protected open fun afterExecute() {}   // 아무것도 안 함
}

// 서브클래스에서 필요한 훅만 오버라이드
class MyHookExample : HookExample() {
    override fun doWork() { println("작업 수행") }
    override fun beforeExecute() { println("사전 준비") }
    // afterExecute는 오버라이드 안 함
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (비교표 2개+)

### 1. 템플릿 메서드 vs 전략 패턴

| 구분 | 템플릿 메서드 | 전략 패턴 |
|:---:|:---|:---|
| **메커니즘** | 상속 | 합성 |
| **변경 시점** | 컴파일 타임 | 런타임 |
| **알고리즘 교체** | 서브클래스 생성 | 전략 객체 교체 |
| **유연성** | 낮음 | 높음 |
| **복잡도** | 낮음 | 중간 |

### 2. 실무 활용 사례

| 프레임워크 | 클래스 | 템플릿 메서드 | 훅/추상 메서드 |
|:---:|:---|:---|:---|
| **Spring** | JdbcTemplate | execute | RowMapper |
| **Servlet** | HttpServlet | service | doGet, doPost |
| **Android** | Activity | onCreate | onStart, onResume |
| **JUnit** | TestCase | runTest | setUp, tearDown |

### 3. 장단점

| 장점 | 단점 |
|:---|:---|
| 코드 재사용 | 상속 제약 (단일 상속) |
| 알고리즘 구조 보장 | 서브클래스 제약 |
| 확장 포인트 명확 | 리스코프 치환 위배 가능 |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (800자+)

### 기술사적 판단

#### 시나리오: 스프링 JdbcTemplate
- **상황**: DB 접근 코드의 반복 (연결, 쿼리 실행, 결과 매핑, 연결 해제)
- **전략**: JdbcTemplate이 템플릿, RowMapper가 추상 메서드
- **기술사적 판단**: 개발자는 SQL과 매핑만 구현, 나머지는 프레임워크가 처리

### 도입 체크리스트
- [ ] 알고리즘 구조가 고정적인가?
- [ ] 일부 단계만 다르게 구현하면 되는가?
- [ ] 상속을 사용해도 무방한가?
- [ ] 확장 포인트가 명확한가?

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 구분 | 효과 |
|:---:|:---|
| **코드 재사용** | 공통 로직 상위 클래스 |
| **일관성** | 알고리즘 구조 보장 |
| **확장성** | 서브클래스로 확장 |

### 참고 표준
- **GoF Design Patterns**: 템플릿 메서드 패턴
- **Spring Framework**: JdbcTemplate 구현

---

## 📌 관련 개념 맵
- [전략 패턴](./strategy_pattern.md): 합성 기반 알고리즘 교체
- [팩토리 메서드](../03_gof_creational/factory_method_pattern.md): 템플릿 메서드의 특수 형태
- [Hollywood 원칙](../02_principles/hollywood_principle.md): 제어 역전
- [OCP 원칙](../02_principles/solid_principles.md): 확장에는 열림

---

## 👶 어린이를 위한 3줄 비유
1. 템플릿 메서드는 **요리 교실에서 선생님이 순서를 정해주는 것**과 같아요. "첫째 물 끓이기, 둘째 재료 넣기, 셋째 완성!"
2. 순서는 똑같지만, **어떤 재료를 넣을지는 학생이 정해요.** 라면 끓이는 학생도, 파스타 만드는 학생도 같은 순서를 따라요.
3. 이렇게 하면 **순서를 매번 설명할 필요 없이** 결과만 다르게 만들 수 있어요!
