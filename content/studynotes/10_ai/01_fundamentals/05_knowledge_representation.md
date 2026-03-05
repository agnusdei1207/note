+++
title = "지식 표현 (Knowledge Representation)"
date = "2026-03-05"
[extra]
categories = ["studynotes-10_ai"]
+++

# 지식 표현 (Knowledge Representation)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인간의 지식과 전문가의 경험을 컴퓨터가 이해하고 처리할 수 있는 형식으로 변환하여 저장, 추론, 활용할 수 있게 하는 AI의 핵심 기술입니다. 규칙(Rules), 프레임(Frames), 의미망(Semantic Networks), 온톨로지(Ontology) 등 다양한 표현 방식이 존재합니다.
> 2. **가치**: 전문가 시스템, 자연어 처리, 시맨틱 웹, 지식 그래프의 기반 기술로, 구글 지식 그래프, 위키데이터, 챗봇, RAG 시스템 등 현대 AI의 핵심 인프라입니다.
> 3. **융합**: 논리학(형식 논리, 서술 논리), 철학(인식론, 존재론), 언어학(의미론), 컴퓨터과학(데이터베이스, 그래프 이론)의 융합 분야입니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**지식 표현 (Knowledge Representation, KR)**은 인간이 가진 지식을 컴퓨터 시스템이 저장, 검색, 추론할 수 있는 형식으로 구조화하는 기술과 방법론을 총칭합니다. AI 시스템이 "무엇을 알고 있는지"를 정의하고, 그 지식을 어떻게 사용할지를 결정합니다.

**지식의 계층 구조**:
```
                    ┌─────────────────┐
                    │    지혜(Wisdom) │ ← 통찰, 판단
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    지식(Knowledge)│ ← 구조화된 정보
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    정보(Information)│ ← 처리된 데이터
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    데이터(Data)    │ ← 원시 사실
                    └───────────────────┘

    지식 표현은 "지식" 계층을 컴퓨터에 저장하는 기술
```

**지식의 유형**:
| 유형 | 정의 | 예시 |
|:---|:---|:---|
| **선언적 지식 (Declarative)** | "무엇(What)"에 대한 사실 | "파리는 프랑스의 수도다" |
| **절차적 지식 (Procedural)** | "어떻게(How)"에 대한 방법 | "자전거 타는 법" |
| **개념적 지식 (Conceptual)** | 개념 간의 관계 | "새는 날아다니는 동물이다" |
| **메타 지식 (Meta-knowledge)** | 지식에 대한 지식 | "이 지식의 신뢰도는 90%다" |
| **휴리스틱 지식** | 경험적 규칙 | "보통 이런 경우는 문제다" |

#### 2. 주요 지식 표현 방식

**1) 규칙 기반 표현 (Rule-Based / Production Rules)**:
```
형식: IF 조건 THEN 행동/결론

예시:
IF 환자.체온 > 38 AND 환자.기침 = 있음
THEN 진단 = "감기 의심" (확신도 = 0.8)

특징:
- 직관적이고 이해하기 쉬움
- 조건부 지식 표현에 적합
- 전문가 시스템의 핵심
```

**2) 프레임 기반 표현 (Frame-Based)**:
```
형식: 슬롯(속성)과 값으로 구성된 객체

예시:
FRAME: 새
├── 슬롯: 날개_수 = 2
├── 슬롯: 이동_방식 = "비행"
├── 슬롯: 종류 = (참새, 독수리, 펭귄, ...)
├── 슬롯: 예외 = (펭귄 → 비행_불가)
└── 슬롯: 상위_클래스 = 동물

특징:
- 객체 지향적
- 상속 가능
- 복잡한 개념 표현
```

**3) 의미망 (Semantic Network)**:
```
형식: 노드(개념)와 링크(관계)로 구성된 그래프

예시:
    [새] ──is_a──► [동물]
      │
      │ has
      ▼
    [날개]

특징:
- 관계 표현에 직관적
- 그래프 순회로 추론
- 시각화 용이
```

**4) 논리 기반 표현 (Logic-Based)**:
```
형식: 술어 논리 (Predicate Logic)

예시:
∀x (새(x) → 동물(x))           // 모든 새는 동물이다
∃x (펭귄(x) ∧ ¬비행(x))         // 비행하지 않는 펭귄이 존재한다
날개_수(참새, 2)                 // 참새의 날개 수는 2다

특징:
- 엄밀한 추론 가능
- 수학적 기반
- 복잡한 표현 가능
```

**5) 온톨로지 (Ontology)**:
```
형식: 개념, 관계, 속성, 제약의 공식화

구성 요소:
- 클래스 (Classes): 개념의 집합
- 속성 (Properties): 개념 간 관계
- 개체 (Individuals): 구체적 인스턴스
- 제약 (Constraints): 규칙과 제한

특징:
- 지식 공유 및 재사용
- 표준화 (OWL, RDF)
- 시맨틱 웹의 기반
```

#### 3. 비유를 통한 이해

지식 표현은 **"도서관의 분류 체계"**에 비유할 수 있습니다:

```
[도서관 분류 체계]
├── 000 총류
│   ├── 010 도서학
│   └── 020 문헌정보학
├── 100 철학
│   ├── 110 형이상학
│   └── 160 논리학
└── ...

[지식 표현]
├── 개념: "형이상학"은 "철학"의 하위 개념
├── 관계: "형이상학" is_a "철학"
├── 속성: "형이상학".분류번호 = "110"
└── 규칙: IF 책.주제 = "형이상학" THEN 책.위치 = "100구역"
```

또 다른 비유: **"뇌의 지식 저장 방식"**
- 우리는 "사과"를 보면 빨간색, 둥근 모양, 달콤한 맛, 과일이라는 관계 등을 떠올립니다.
- 지식 표현은 이러한 "연결"을 컴퓨터에 구현하는 것입니다.

#### 4. 등장 배경 및 발전 과정

| 연도 | 사건 | 의미 |
|:---|:---|:---|
| 1956 | 다트머스 회의 | AI 탄생, 지식 표현 연구 시작 |
| 1960s | Semantic Networks | Quillian의 의미망 제안 |
| 1970s | Frames, Scripts | Minsky의 프레임 이론, Schank의 스크립트 |
| 1970s | Production Rules | 전문가 시스템의 규칙 기반 표현 |
| 1980s | Description Logic | 서술 논리 발전 |
| 1990s | Ontology | 지식 공유, 재사용 강조 |
| 2001 | Semantic Web | Tim Berners-Lee, 웹에 지식 표현 |
| 2004 | OWL 표준 | W3C 온톨로지 언어 표준화 |
| 2012 | Google Knowledge Graph | 대규모 지식 그래프 상용화 |
| 2020s | 지식 그래프 + LLM | RAG, 지식 기반 생성형 AI |

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 지식 표현 방식 상세 비교 (표)

| 방식 | 표현 단위 | 추론 방식 | 장점 | 단점 | 적용 분야 |
|:---|:---|:---|:---|:---|:---|
| **규칙 (Rules)** | IF-THEN | 전향/후향 추론 | 직관적, 수정 용이 | 규칙 폭발 | 전문가 시스템 |
| **프레임 (Frames)** | 슬롯-값 | 상속, 기본값 | 구조화, OOP 유사 | 유연성 부족 | 객체 분류 |
| **의미망** | 노드-링크 | 그래프 탐색 | 관계 표현 직관 | 모호성 | 연상, 추론 |
| **논리 (Logic)** | 술어, 정량자 | 연역, 귀납 | 엄밀함, 수학적 | 복잡성 | 증명, 검증 |
| **온톨로지** | 클래스, 속성 | 분류, 추론 | 공유, 표준화 | 구축 비용 | 시맨틱 웹 |
| **지식 그래프** | 엔티티-관계 | 그래프 알고리즘 | 대규모, 검색 친화 | 품질 관리 | 검색, QA |

#### 2. 지식 그래프 아키텍처 다이어그램

```text
<<< Knowledge Graph Architecture >>>

    ┌─────────────────────────────────────────────────────────────┐
    │                    APPLICATION LAYER                        │
    │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────┐   │
    │  │ Search  │  │   QA    │  │  Chat   │  │Recommendation│   │
    │  │ Engine  │  │ System  │  │  Bot    │  │   System     │   │
    │  └────┬────┘  └────┬────┘  └────┬────┘  └──────┬──────┘   │
    └───────┼────────────┼────────────┼──────────────┼───────────┘
            │            │            │              │
            └────────────┼────────────┼──────────────┘
                         │            │
    ┌────────────────────▼────────────▼──────────────────────────┐
    │                  QUERY PROCESSING                           │
    │   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐  │
    │   │   SPARQL     │   │   GraphQL    │   │   Natural    │  │
    │   │   Endpoint   │   │   API        │   │   Language   │  │
    │   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘  │
    └──────────┼──────────────────┼──────────────────┼───────────┘
               │                  │                  │
    ┌──────────▼──────────────────▼──────────────────▼───────────┐
    │                   KNOWLEDGE GRAPH                           │
    │                                                             │
    │   ┌─────────────────────────────────────────────────────┐  │
    │   │              ONTOLOGY / SCHEMA                       │  │
    │   │                                                      │  │
    │   │   [Person] ──works_for──► [Company]                 │  │
    │   │      │                          │                    │  │
    │   │   located_in                 industry                │  │
    │   │      │                          │                    │  │
    │   │      ▼                          ▼                    │  │
    │   │   [City] ◄──headquartered── [Industry]              │  │
    │   └─────────────────────────────────────────────────────┘  │
    │                                                             │
    │   ┌─────────────────────────────────────────────────────┐  │
    │   │              INSTANCES / FACTS                       │  │
    │   │                                                      │  │
    │   │   [Elon Musk] ──works_for──► [Tesla]                │  │
    │   │       │                          │                   │  │
    │   │    located_in                industry                │  │
    │   │       │                          │                   │  │
    │   │       ▼                          ▼                   │  │
    │   │   [Austin] ◄──headquartered── [Automotive]          │  │
    │   └─────────────────────────────────────────────────────┘  │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
               │
    ┌──────────▼──────────────────────────────────────────────────┐
    │                  STORAGE LAYER                              │
    │   ┌──────────┐   ┌──────────┐   ┌──────────────────────┐  │
    │   │ RDF Store│   │ Graph DB │   │   Triple Store       │  │
    │   │ (Jena)   │   │(Neo4j)   │   │   (Virtuoso)         │  │
    │   └──────────┘   └──────────┘   └──────────────────────┘  │
    └─────────────────────────────────────────────────────────────┘

<<< 지식 그래프 예시: 영화 도메인 >>>

    ┌─────────┐                              ┌─────────┐
    │  영화   │                              │  감독   │
    │ Inception│◄─────directed_by───────────│Christopher│
    │         │                              │  Nolan  │
    │         │                              └────┬────┘
    │         │                                   │
    │         │           ┌──────────────┐        │born_in
    │         │           │    배우      │        │
    │         ├─starring──►│ Leonardo    │        ▼
    │         │           │ DiCaprio   │    ┌─────────┐
    │         │           └─────┬──────┘    │  국가   │
    │         │                 │           │ 영국    │
    │         │                 │born_in    └─────────┘
    │         │                 ▼
    │         │           ┌─────────┐
    │         │           │  국가   │
    │         │           │  미국   │
    │         │           └─────────┘
    │         │
    │         ├─genre──► [SF]
    │         ├─year───► [2010]
    │         └─rating─► [8.8]

    Triple (주어, 술어, 목적어) 예시:
    - (Inception, directed_by, Christopher Nolan)
    - (Inception, starring, Leonardo DiCaprio)
    - (Christopher Nolan, born_in, 영국)
```

#### 3. 심층 동작 원리: 온톨로지 기반 추론

**1) 분류 (Classification)**:
```
규칙: 모든 A는 B의 하위 클래스
사실: x는 A의 인스턴스
추론: x는 B의 인스턴스

예시:
온톨로지: 모든 펭귄은 새다
사실: 펭귄구는 펭귄이다
추론: 펭귄구는 새다
```

**2) 속성 상속 (Property Inheritance)**:
```
규칙: A는 B의 하위 클래스, B에 속성 P가 있다
사실: A에 속성 P가 명시되지 않음
추론: A도 속성 P를 가진다 (상속)

예시:
온톨로지: 새는 날개가 있다
사실: 참새는 새다
추론: 참새는 날개가 있다 (상속)
```

**3) 역관계 추론 (Inverse Property)**:
```
규칙: P와 Q는 역관계
사실: (a, P, b)
추론: (b, Q, a)

예시:
온톨로지: "부모"와 "자녀"는 역관계
사실: 김철수의 부모는 김영희다
추론: 김영희의 자녀는 김철수다
```

**4) 대칭성 추론 (Symmetric Property)**:
```
규칙: P는 대칭 속성
사실: (a, P, b)
추론: (b, P, a)

예시:
온톨로지: "결혼"은 대칭 관계
사실: A는 B와 결혼했다
추론: B는 A와 결혼했다
```

**5) 추이성 추론 (Transitive Property)**:
```
규칙: P는 추이적 속성
사실: (a, P, b), (b, P, c)
추론: (a, P, c)

예시:
온톨로지: "조상"은 추이적 관계
사실: A는 B의 조상, B는 C의 조상
추론: A는 C의 조상
```

#### 4. 실무 수준의 지식 그래프 구현

```python
"""
Knowledge Graph Implementation
- 온톨로지 기반 지식 표현
- SPARQL 스타일 쿼리
- 추론 엔진
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Any, Iterator
from enum import Enum
from collections import defaultdict
import re

class EntityType(Enum):
    CLASS = "class"
    INDIVIDUAL = "individual"
    PROPERTY = "property"

class PropertyType(Enum):
    OBJECT_PROPERTY = "object"      # 엔티티 간 관계
    DATA_PROPERTY = "data"          # 엔티티-값 관계
    ANNOTATION = "annotation"       # 메타데이터

@dataclass
class Triple:
    """RDF Triple (주어, 술어, 목적어)"""
    subject: str
    predicate: str
    object: Any

    def __hash__(self):
        return hash((self.subject, self.predicate, str(self.object)))

    def __eq__(self, other):
        if not isinstance(other, Triple):
            return False
        return (self.subject == other.subject and
                self.predicate == other.predicate and
                self.object == other.object)

@dataclass
class Property:
    """속성 정의"""
    name: str
    property_type: PropertyType
    domain: Optional[str] = None    # 주어의 클래스
    range: Optional[str] = None     # 목적어의 클래스/타입
    inverse_of: Optional[str] = None
    symmetric: bool = False
    transitive: bool = False
    functional: bool = False        # 단일값

@dataclass
class Class:
    """클래스 정의"""
    name: str
    superclasses: List[str] = field(default_factory=list)
    properties: List[str] = field(default_factory=list)
    equivalent_classes: List[str] = field(default_factory=list)

class KnowledgeGraph:
    """지식 그래프"""

    def __init__(self):
        # 스키마
        self.classes: Dict[str, Class] = {}
        self.properties: Dict[str, Property] = {}

        # 데이터
        self.triples: Set[Triple] = set()

        # 인덱스
        self._subject_index: Dict[str, Set[Triple]] = defaultdict(set)
        self._predicate_index: Dict[str, Set[Triple]] = defaultdict(set)
        self._object_index: Dict[str, Set[Triple]] = defaultdict(set)

        # 캐시
        self._inference_cache: Dict[str, Set[str]] = {}

    # ========== 스키마 관리 ==========

    def add_class(self, cls: Class):
        """클래스 추가"""
        self.classes[cls.name] = cls

    def add_property(self, prop: Property):
        """속성 추가"""
        self.properties[prop.name] = prop

    # ========== 데이터 관리 ==========

    def add_triple(self, subject: str, predicate: str, obj: Any):
        """Triple 추가"""
        triple = Triple(subject, predicate, obj)

        if triple not in self.triples:
            self.triples.add(triple)
            self._subject_index[subject].add(triple)
            self._predicate_index[predicate].add(triple)
            self._object_index[str(obj)].add(triple)

            # 추론 캐시 무효화
            self._inference_cache.clear()

    def add_facts(self, facts: List[Tuple[str, str, Any]]):
        """다수의 사실 추가"""
        for s, p, o in facts:
            self.add_triple(s, p, o)

    # ========== 쿼리 ==========

    def query(
        self,
        subject: Optional[str] = None,
        predicate: Optional[str] = None,
        obj: Optional[Any] = None
    ) -> List[Triple]:
        """패턴 매칭 쿼리"""
        results = []

        if subject is not None:
            candidates = self._subject_index.get(subject, set())
        elif predicate is not None:
            candidates = self._predicate_index.get(predicate, set())
        elif obj is not None:
            candidates = self._object_index.get(str(obj), set())
        else:
            candidates = self.triples

        for triple in candidates:
            if subject is not None and triple.subject != subject:
                continue
            if predicate is not None and triple.predicate != predicate:
                continue
            if obj is not None and triple.object != obj:
                continue
            results.append(triple)

        return results

    def get_property_values(
        self,
        subject: str,
        predicate: str
    ) -> List[Any]:
        """특정 엔티티의 속성 값 조회"""
        return [t.object for t in self.query(subject=subject, predicate=predicate)]

    def get_related_entities(
        self,
        entity: str,
        predicate: Optional[str] = None
    ) -> List[str]:
        """관련 엔티티 조회"""
        results = []
        for triple in self._subject_index.get(entity, set()):
            if predicate is None or triple.predicate == predicate:
                if isinstance(triple.object, str):
                    results.append(triple.object)
        return results

    # ========== 추론 ==========

    def get_all_superclasses(self, class_name: str) -> Set[str]:
        """모든 상위 클래스 조회 (추이적)"""
        if class_name in self._inference_cache:
            return self._inference_cache[class_name]

        superclasses = set()
        to_visit = [class_name]

        while to_visit:
            current = to_visit.pop()
            if current in self.classes:
                for super_cls in self.classes[current].superclasses:
                    if super_cls not in superclasses:
                        superclasses.add(super_cls)
                        to_visit.append(super_cls)

        self._inference_cache[class_name] = superclasses
        return superclasses

    def get_all_types(self, individual: str) -> Set[str]:
        """개체의 모든 타입 (직접 + 간접)"""
        direct_types = set(
            t.object for t in self.query(subject=individual, predicate="rdf:type")
        )

        all_types = set(direct_types)
        for t in direct_types:
            all_types.update(self.get_all_superclasses(t))

        return all_types

    def infer_inverse(self):
        """역관계 추론"""
        new_triples = []

        for prop in self.properties.values():
            if prop.inverse_of:
                for triple in list(self._predicate_index.get(prop.name, set())):
                    # (a, P, b) → (b, inverse(P), a)
                    new_triple = Triple(
                        str(triple.object),
                        prop.inverse_of,
                        triple.subject
                    )
                    if new_triple not in self.triples:
                        new_triples.append(new_triple)

        for t in new_triples:
            self.add_triple(t.subject, t.predicate, t.object)

        return len(new_triples)

    def infer_symmetric(self):
        """대칭성 추론"""
        new_triples = []

        for prop in self.properties.values():
            if prop.symmetric:
                for triple in list(self._predicate_index.get(prop.name, set())):
                    # (a, P, b) → (b, P, a)
                    new_triple = Triple(
                        str(triple.object),
                        prop.name,
                        triple.subject
                    )
                    if new_triple not in self.triples:
                        new_triples.append(new_triple)

        for t in new_triples:
            self.add_triple(t.subject, t.predicate, t.object)

        return len(new_triples)

    def infer_transitive(self):
        """추이성 추론"""
        new_triples = []

        for prop in self.properties.values():
            if prop.transitive:
                # (a, P, b) + (b, P, c) → (a, P, c)
                triples_list = list(self._predicate_index.get(prop.name, set()))

                for t1 in triples_list:
                    for t2 in triples_list:
                        if t1.object == t2.subject:
                            new_triple = Triple(
                                t1.subject,
                                prop.name,
                                t2.object
                            )
                            if new_triple not in self.triples:
                                new_triples.append(new_triple)

        for t in new_triples:
            self.add_triple(t.subject, t.predicate, t.object)

        return len(new_triples)

    def run_inference(self) -> Dict[str, int]:
        """모든 추론 실행"""
        results = {
            "inverse": self.infer_inverse(),
            "symmetric": self.infer_symmetric(),
            "transitive": self.infer_transitive()
        }
        return results

    # ========== 직렬화 ==========

    def to_rdf_triples(self) -> List[str]:
        """RDF N-Triples 형식으로 변환"""
        lines = []
        for t in self.triples:
            if isinstance(t.object, str):
                obj = f"<{t.object}>"
            else:
                obj = f'"{t.object}"'
            lines.append(f"<{t.subject}> <{t.predicate}> {obj} .")
        return lines

    def export_dot(self) -> str:
        """Graphviz DOT 형식으로 내보내기"""
        lines = ["digraph KnowledgeGraph {", "  node [shape=box];"]

        # 노드
        entities = set()
        for t in self.triples:
            entities.add(t.subject)
            if isinstance(t.object, str):
                entities.add(t.object)

        for e in entities:
            lines.append(f'  "{e}";')

        # 엣지
        for t in self.triples:
            if isinstance(t.object, str):
                lines.append(f'  "{t.subject}" -> "{t.object}" [label="{t.predicate}"];')

        lines.append("}")
        return "\n".join(lines)

    def stats(self) -> Dict[str, int]:
        """통계 정보"""
        return {
            "classes": len(self.classes),
            "properties": len(self.properties),
            "triples": len(self.triples),
            "entities": len(self._subject_index)
        }


# 영화 도메인 지식 그래프 생성 예시
def create_movie_knowledge_graph() -> KnowledgeGraph:
    """영화 도메인 지식 그래프"""

    kg = KnowledgeGraph()

    # 스키마 정의
    kg.add_class(Class("Person", superclasses=["Thing"]))
    kg.add_class(Class("Movie", superclasses=["Thing"]))
    kg.add_class(Class("Director", superclasses=["Person"]))
    kg.add_class(Class("Actor", superclasses=["Person"]))
    kg.add_class(Class("Genre", superclasses=["Thing"]))
    kg.add_class(Class("Country", superclasses=["Thing"]))

    # 속성 정의
    kg.add_property(Property(
        "directed_by",
        PropertyType.OBJECT_PROPERTY,
        domain="Movie", range="Director"
    ))
    kg.add_property(Property(
        "starring",
        PropertyType.OBJECT_PROPERTY,
        domain="Movie", range="Actor"
    ))
    kg.add_property(Property(
        "born_in",
        PropertyType.OBJECT_PROPERTY,
        domain="Person", range="Country"
    ))
    kg.add_property(Property(
        "genre",
        PropertyType.OBJECT_PROPERTY,
        domain="Movie", range="Genre"
    ))
    kg.add_property(Property(
        "year",
        PropertyType.DATA_PROPERTY,
        domain="Movie", range="integer"
    ))
    kg.add_property(Property(
        "married_to",
        PropertyType.OBJECT_PROPERTY,
        domain="Person", range="Person",
        symmetric=True
    ))
    kg.add_property(Property(
        "ancestor_of",
        PropertyType.OBJECT_PROPERTY,
        domain="Person", range="Person",
        transitive=True
    ))

    # 데이터 추가
    facts = [
        # 타입
        ("Inception", "rdf:type", "Movie"),
        ("Interstellar", "rdf:type", "Movie"),
        ("Christopher_Nolan", "rdf:type", "Director"),
        ("Leonardo_DiCaprio", "rdf:type", "Actor"),
        ("Matthew_McConaughey", "rdf:type", "Actor"),
        ("SF", "rdf:type", "Genre"),
        ("USA", "rdf:type", "Country"),
        ("UK", "rdf:type", "Country"),

        # 영화 속성
        ("Inception", "directed_by", "Christopher_Nolan"),
        ("Inception", "starring", "Leonardo_DiCaprio"),
        ("Inception", "genre", "SF"),
        ("Inception", "year", 2010),

        ("Interstellar", "directed_by", "Christopher_Nolan"),
        ("Interstellar", "starring", "Matthew_McConaughey"),
        ("Interstellar", "genre", "SF"),
        ("Interstellar", "year", 2014),

        # 인물 속성
        ("Christopher_Nolan", "born_in", "UK"),
        ("Leonardo_DiCaprio", "born_in", "USA"),
        ("Matthew_McConaughey", "born_in", "USA"),
    ]

    kg.add_facts(facts)

    return kg


# 사용 예시
if __name__ == "__main__":
    kg = create_movie_knowledge_graph()

    print("=== 지식 그래프 통계 ===")
    print(kg.stats())

    print("\n=== 쿼리: Inception의 모든 속성 ===")
    for triple in kg.query(subject="Inception"):
        print(f"  {triple.predicate}: {triple.object}")

    print("\n=== 쿼리: 크리스토퍼 놀란이 감독한 영화 ===")
    for triple in kg.query(predicate="directed_by"):
        if triple.object == "Christopher_Nolan":
            print(f"  {triple.subject}")

    print("\n=== 쿼리: USA에서 태어난 사람 ===")
    for triple in kg.query(predicate="born_in"):
        if triple.object == "USA":
            print(f"  {triple.subject}")

    print("\n=== 추론 실행 ===")
    results = kg.run_inference()
    print(f"  역관계: {results['inverse']}개")
    print(f"  대칭성: {results['symmetric']}개")
    print(f"  추이성: {results['transitive']}개")

    print("\n=== Nolan의 모든 타입 ===")
    types = kg.get_all_types("Christopher_Nolan")
    print(f"  {types}")

    print("\n=== DOT 형식 내보내기 ===")
    print(kg.export_dot())
```

---

### III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 지식 표현 언어 비교

| 언어 | 기반 | 표현력 | 복잡도 | 용도 |
|:---|:---|:---|:---|:---|
| **RDF** | 트리플 | 낮음 | 낮음 | 데이터 교환 |
| **RDFS** | RDF + 스키마 | 중간 | 중간 | 간단한 온톨로지 |
| **OWL-Lite** | 서술 논리 | 중간 | 중간 | 경량 온톨로지 |
| **OWL-DL** | 서술 논리 | 높음 | 높음 | 복잡한 온톨로지 |
| **OWL-Full** | RDF | 매우 높음 | 결정 불가 | 최대 표현력 |
| **SHACL** | 제약 언어 | 중간 | 중간 | 데이터 검증 |

#### 2. 지식 그래프 플랫폼 비교

| 플랫폼 | 유형 | 규모 | 특징 |
|:---|:---|:---|:---|
| **Google Knowledge Graph** | 상용 | 500억+ 팩트 | 검색, QA |
| **Wikidata** | 오픈 | 1억+ 항목 | 커뮤니티 구축 |
| **DBpedia** | 오픈 | 1억+ 트리플 | 위키피디아 추출 |
| **Freebase → Wikidata** | 오픈 | (종료) | 구글이 인수 |
| **YAGO** | 오픈 | 1천만+ 엔티티 | 학술 연구 |
| **Neo4j** | 그래프DB | 확장 가능 | 범용 그래프 DB |

#### 3. 과목 융합 관점 분석

**[지식 표현 + NLP]**:
- Named Entity Recognition → 지식 그래프 엔티티
- Relation Extraction → 트리플 생성
- Entity Linking → 지식 베이스 연결
- RAG (Retrieval-Augmented Generation)

**[지식 표현 + 데이터베이스]**:
- 그래프 데이터베이스 (Neo4j, Amazon Neptune)
- SPARQL 쿼리 언어
- 트리플 스토어 (Virtuoso, Jena)

**[지식 표현 + LLM]**:
- LLM으로 지식 그래프 구축
- 지식 그래프로 LLM 환각 방지
- GraphRAG: 지식 그래프 기반 RAG

---

### IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단: 실무 시나리오

**시나리오 A: 기업 지식 그래프 구축**
- **상황**: 대기업의 내부 지식 관리 시스템
- **기술사 판단**:
  1. **범위 정의**: 제품, 부서, 인물, 프로젝트
  2. **스키마 설계**: 핵심 클래스와 관계 정의
  3. **데이터 소스**: HR 시스템, 제품 DB, 문서
  4. **구축 방법**:
     - 기존 DB에서 ETL
     - 문서에서 NLP로 추출
     - 전문가 수동 입력
  5. **활용**: 검색, 추천, 질의응답

**시나리오 B: 의료 지식 그래프**
- **상황**: 병원의 임상 의사결정 지원
- **기술사 판단**:
  1. **표준 활용**: ICD-10, SNOMED CT, RxNorm
  2. **범위**: 질병, 증상, 약물, 검사
  3. **관계**: 질병-증상, 약물-부작용, 상호작용
  4. **품질 관리**: 의료진 검수 필수
  5. **활용**: 진단 보조, 약물 처방 경고

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **범위 정의**: 어떤 도메인과 개념을 포함할 것인가?
- [ ] **스키마 설계**: 충분히 유연하면서도 명확한가?
- [ ] **데이터 소스**: 지식을 어디서 가져올 것인가?
- [ ] **품질 관리**: 어떻게 정확성을 보장할 것인가?
- [ ] **활용 시나리오**: 누가, 어떻게 사용할 것인가?
- [ ] **유지보수**: 지속적인 업데이트 체계가 있는가?

#### 3. 안티패턴 (Anti-patterns)

**안티패턴 1: 과도한 스키마 설계**
- 문제: 너무 복잡한 온톨로지로 구현 불가
- 해결: 핵심부터 시작, 점진적 확장

**안티패턴 2: 품질 무시**
- 문제: 잘못된 지식이 시스템 전체 오염
- 해결: 검증 체계, 출처 추적

**안티패턴 3: 고립된 지식 그래프**
- 문제: 다른 시스템과 연동 안 됨
- 해결: 표준 포맷 사용, API 제공

---

### V. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 | 도입 후 | 향상 |
|:---|:---|:---|:---|
| **검색 정확도** | 60% | 85% | +25% |
| **정보 발견 시간** | 10분 | 1분 | 10x |
| **QA 정확도** | 50% | 80% | +30% |
| **추천 품질** | 랜덤 | 개인화 | 질적 향상 |

#### 2. 미래 전망 및 진화 방향

**단기 (2024~2027)**:
- **LLM + KG**: 지식 그래프 기반 RAG 확산
- **자동 구축**: LLM으로 지식 그래프 자동 생성
- **멀티모달**: 텍스트, 이미지, 비디오 통합

**중기 (2028~2035)**:
- **실시간 업데이트**: 지속적 학습
- **분산 지식 그래프**: 블록체인 기반
- **개인화**: 사용자별 지식 프로파일

**장기 (2035~)**:
- **글로벌 지식 그래프**: 인류 전체 지식 통합
- **AGI의 지식 기반**: 인간 수준 이상의 지식 활용

#### 3. 참고 표준 및 가이드라인

- **W3C RDF 1.1**: 리소스 기술 프레임워크
- **W3C OWL 2**: 웹 온톨로지 언어
- **W3C SPARQL 1.1**: RDF 쿼리 언어
- **W3C SHACL**: RDF 데이터 제약 언어
- **Schema.org**: 구조화된 데이터 스키마

---

### 관련 개념 맵 (Knowledge Graph)

- **[전문가 시스템](@/studynotes/10_ai/01_fundamentals/04_expert_system.md)**: 지식 베이스를 활용한 추론 시스템
- **[퍼지 논리](@/studynotes/10_ai/01_fundamentals/07_fuzzy_logic.md)**: 불확실한 지식 표현
- **[RAG](@/studynotes/10_ai/01_dl/rag.md)**: 지식 그래프 기반 검색 증강 생성
- **[LLM](@/studynotes/10_ai/01_dl/gpt_model.md)**: 대규모 언어 모델과 지식 그래프 융합
- **[자연어 처리](@/studynotes/10_ai/01_dl/transformer_architecture.md)**: 텍스트에서 지식 추출

---

### 어린이를 위한 3줄 비유 설명

1. **컴퓨터의 뇌 저장소**: 지식 표현은 컴퓨터가 "사과는 과일이다", "과일은 먹을 수 있다" 같은 지식을 저장하는 방법이에요. 마치 우리 뇌가 지식을 저장하는 것처럼요!

2. **거미줄 같은 연결**: 모든 지식이 거미줄처럼 연결되어 있어요. "사과"를 찾으면 "빨간색", "둥글다", "달콤하다", "과일" 같은 연결된 정보도 함께 볼 수 있어요!

3. **똑똑한 질문 대답**: 컴퓨터가 "사과는 뭐야?"라고 물으면 "사과는 빨간색이고 둥글고 달콤한 과일이에요!"라고 대답할 수 있어요. 연결된 지식을 다 찾아서요!
