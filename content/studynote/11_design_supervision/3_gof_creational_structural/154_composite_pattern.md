+++
weight = 154
title = "컴포지트 패턴 (Composite Pattern)"
date = "2026-03-04"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
1. **부분-전체 계층 구조**: 객체들을 트리 구조로 구성하여 단일 객체(Leaf)와 복합 객체(Composite)를 동일한 방식으로 다루게 하는 구조 패턴입니다.
2. **다형적 통일성**: 클라이언트가 객체가 단일인지 복합인지 구분할 필요 없이 동일한 인터페이스로 모든 객체와 상호작용할 수 있게 합니다.
3. **재귀적 처리**: 트리 구조 내에서 연산을 재귀적으로 전파하여 복잡한 구조의 데이터 처리를 단순화합니다.

### Ⅰ. 개요 (Context & Background)
컴포지트 패턴은 사용자가 "부분-전체" 계층 구조를 나타내고자 할 때 가장 적합합니다. 대표적인 예로 운영체제의 파일 시스템(파일과 폴더), 그래픽 편집기(단순 도형과 그룹화된 도형), 조직도 등이 있습니다. 이 패턴의 핵심은 클라이언트가 개별 객체(Leaf)와 그들의 컨테이너(Composite)를 동일하게 취급하도록 설계하여 코드의 복잡성을 낮추는 것입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
컴포지트 패턴은 공통 인터페이스(Component), 단일 객체(Leaf), 복합 객체(Composite)로 구성됩니다.

```text
       [ Component ] (공통 인터페이스)
      /             \
 [ Leaf ]       [ Composite ] (복합 객체)
(단일 객체)     - children: List<Component>
                - add(c), remove(c), getChild(i)

  <Bilingual Structural Diagram>
  1. Component defines common operations. -> 공통 연산 정의
  2. Leaf implements atomic behavior. -> 단일 객체의 기능 수행
  3. Composite delegates to children. -> 복합 객체가 자식들에게 연산 위임
```

- **Component**: 모든 객체의 베이스 클래스이며, Leaf와 Composite가 공통으로 가질 메서드를 선언합니다.
- **Leaf**: 트리의 말단 노드로, 실제 비즈니스 로직을 수행합니다. 자식을 가질 수 없습니다.
- **Composite**: 자식들을 관리(추가/삭제)하며, 자식들에게 자신의 연산을 재귀적으로 호출하여 결과를 합산합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
컴포지트 패턴은 트리 구조 탐색 시 이터레이터(Iterator) 및 방문자(Visitor) 패턴과 자주 결합됩니다.

| 구분 | 컴포지트 패턴 (Composite) | 데코레이터 패턴 (Decorator) | 프록시 패턴 (Proxy) |
| :--- | :--- | :--- | :--- |
| **중점 사항** | 객체들의 계층적 그룹화 | 객체에 동적 책임 추가 | 객체에 대한 접근 제어 |
| **관계** | 1:N (다수 자식 소유) | 1:1 (하나의 객체 감싸기) | 1:1 (하나의 객체 대리) |
| **구조 형태** | 트리(Tree) 구조 | 래핑(Wrapping) 체인 | 인터페이스 위임 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **적용 케이스**: 
    - 파일 시스템 (File vs Directory)
    - GUI 컴포넌트 (Button vs Panel/Frame)
    - 메뉴 시스템 (MenuItem vs Menu)
- **기술사적 판단**: 컴포지트 패턴 적용 시 **투명성(Transparency)**과 **안정성(Safety)** 사이의 트레이드오프를 고려해야 합니다. 자식 관리 메서드(add/remove)를 최상위 Component에 두면 사용이 투명해지지만(투명성), Leaf에서 호출 시 예외 처리가 필요합니다. 반면 Composite에만 두면 타입 체크가 필요해지지만 안전합니다(안정성). 대개는 투명성을 강조하는 설계가 선호됩니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
컴포지트 패턴은 새로운 종류의 Leaf나 Composite 클래스를 추가하더라도 기존 클라이언트 코드를 수정할 필요가 없으므로 **확장성**이 매우 뛰어납니다. 복잡한 구조를 단순화하고 재귀적 처리를 정형화함으로써 소프트웨어 아키텍처의 **개념적 무결성**을 유지하는 데 핵심적인 역할을 합니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: 구조 패턴 (Structural Patterns), 트리 구조 (Tree Structure)
- **융합 기술**: 이터레이터 패턴 (순회), 방문자 패턴 (연산 분리)
- **핵심 원칙**: 개방-폐쇄 원칙 (OCP), 단일 책임 원칙 (SRP)

### 👶 어린이를 위한 3줄 비유 설명
1. **사과 한 개(Leaf)**와 **사과 상자(Composite)**를 생각해보세요.
2. "무게를 재주세요"라고 말하면 사과 한 개는 자기 몸무게를 말하고, 사과 상자는 안에 든 모든 사과의 무게를 합해서 말해요.
3. 밖에서 볼 때는 한 개인지 한 상자인지 상관없이 "무게"를 물어볼 수 있는 것과 같아요.
