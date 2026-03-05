+++
title = "시맨틱 웹 (Semantic Web)"
description = "웹 데이터에 의미(Semantics)를 부여하여 기계가 이해하고 추론할 수 있는 지식 네트워크를 구축하는 온톨로지 기반 기술의 심층 분석"
date = 2024-05-15
[taxonomies]
tags = ["Semantic Web", "Ontology", "RDF", "SPARQL", "Knowledge Graph", "ICT Convergence"]
+++

# 시맨틱 웹 (Semantic Web)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시맨틱 웹은 팀 버너스리가 제창한 '웹 데이터에 의미를 부여하는' 비전으로, 자연어로 표현된 정보를 기계가 이해할 수 있는 구조화된 지식(RDF, OWL, 온톨로지)으로 변환하여, 컴퓨터가 문맥을 파악하고 논리적 추론을 수행할 수 있게 하는 기술 아키텍처입니다.
> 2. **가치**: 시맨틱 웹은 검색 엔진의 정확도를 획기적으로 향상시키고(구글 지식 그래프), 이기종 데이터 소스 간의 자동 연동을 가능하게 하며, AI 에이전트가 웹 상의 지식을 이해하고 활용하는 LLM/RAG 시대의 기반 인프라를 제공합니다.
> 3. **융합**: 최근에는 대규모 언어 모델(LLM)과 결합하여 LLM의 환각(Hallucination) 문제를 완화하는 지식 그래프 기반 RAG, 그리고 기업 내 데이터 통합을 위한 엔터프라이즈 지식 그래프로 진화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
시맨틱 웹(Semantic Web)은 월드와이드웹의 창시자 팀 버너스리가 2001년 사이언티픽 아메리칸 지를 통해 제안한 차세대 웹 비전으로, "웹 문서에 포함된 데이터가 기계(컴퓨터)에 의해 이해되고 처리될 수 있도록, 데이터의 의미(Semantics)를 명시적으로 표현하는 기술 프레임워크"입니다. 이는 단순히 사람이 읽기 위한 웹페이지를 넘어, 소프트웨어 에이전트가 웹 상의 정보를 '이해'하고, 추론하며, 자동으로 연관 정보를 발견하는 '지식의 웹'을 구축하는 것을 목표로 합니다.

기술적으로 시맨틱 웹은 **RDF(Resource Description Framework)**, **OWL(Web Ontology Language)**, **SPARQL(SPARQL Protocol and RDF Query Language)** 등의 W3C 표준 기술 스택을 기반으로 구축되며, **온톨로지(Ontology)**라는 지식 표현 모델을 통해 개념 간의 관계를 정의합니다.

### 2. 구체적인 일상생활 비유
현재의 웹은 마치 **번역되지 않은 외국어 서류 더미**와 같습니다. 컴퓨터는 서류에 적힌 단어들을 저장하고 검색할 수는 있지만, 그 단어들이 무슨 의미인지, 어떤 개념들과 연관되는지는 전혀 이해하지 못합니다. "사과"라는 단어가 나오면 그것이 '과일'인지 '애플 회사'인지 구분하지 못합니다.

시맨틱 웹은 이 서류들에 **바코드와 메타데이터 태그**를 붙이는 것과 같습니다. 각 단어와 문장에 "이것은 과일의 일종이다", "이것은 기업명이다"라는 의미 정보를 태그로 추가하면, 컴퓨터가 문서를 읽고 "사과(과일)는 식물에 속하고, 색깔은 빨강 또는 초록이며, 영양소가 풍부하다"라는 지식을 스스로 이해하고 추론할 수 있게 됩니다.

### 3. 등장 배경 및 발전 과정
1. **웹의 한계: 의미 부재(No Semantics) 문제**:
   - 기존 웹은 HTML로 작성된 문서들로 구성되어 있습니다. HTML은 문서의 '표현(Presentation)'을 정의할 뿐(예: 이 텍스트를 굵게 표시), 데이터의 '의미'를 표현하지 않습니다. 컴퓨터는 `<b>사과</b>`라는 태그를 보고 "이것이 과일이라는 것"을 알지 못합니다.
   - 이로 인해 검색 엔진은 키워드 일치에 의존할 수밖에 없었고, "자바"를 검색하면 프로그래밍 언어, 커피, 섬나라가 섞여서 나오는 문제가 발생했습니다.

2. **시맨틱 웹 기술 스택의 등장**:
   - 1999년 RDF(Resource Description Framework)가 W3C 권고안으로 채택되었습니다. RDF는 "주어-술어-목적어(Subject-Predicate-Object)"의 3요소로 구성된 트리플(Triple) 구조를 통해 지식을 표현합니다.
   - 2004년 OWL(Web Ontology Language)이 도입되어, 개념 간의 복잡한 관계(상속, 제약조건, 추론 규칙)를 정의할 수 있게 되었습니다.
   - 구글은 2012년 '지식 그래프(Knowledge Graph)'를 발표하며 시맨틱 웹 기술을 상용 서비스에 대규모로 적용했습니다.

3. **LLM 시대와 시맨틱 웹의 재조명**:
   - 최근 ChatGPT 등 대규모 언어 모델(LLM)이 등장하면서 시맨틱 웹이 재평가되고 있습니다. LLM은 방대한 텍스트를 학습했지만, 학습하지 않은 팩트에 대해서는 '환각(Hallucination)'을 일으킵니다.
   - 시맨틱 웹의 지식 그래프를 LLM과 결합한 **GraphRAG**는 LLM이 지식 그래프에서 정확한 팩트를 검색하여 답변의 신뢰성을 높이는 하이브리드 아키텍처로 주목받고 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Component) | 상세 역할 | 내부 동작 메커니즘 | 관련 표준/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **RDF (Resource Description Framework)** | 데이터를 "주어-술어-목적어" 3요소로 표현하는 데이터 모델 | URI로 식별된 자원 간의 관계를 그래프(노드-엣지)로 표현 | W3C RDF 1.1, Turtle, N-Triples | 문장의 주어-동사-목적어 구조 |
| **URI/IRI (Uniform Resource Identifier)** | 웹 상의 모든 개념/자원에 고유 식별자 부여 | HTTP URI를 통해 전 세계 어디서든 동일한 개념을 참조 가능 | RFC 3986 | 사람의 주민등록번호 |
| **온톨로지 (Ontology)** | 개념(Class), 속성(Property), 관계(Relation)를 정의하는 지식 스키마 | 논리적 제약조건(서브클래스, 도메인, 범위)을 정의하여 추론 엔진이 새로운 지식 도출 | OWL 2, RDFS | 데이터베이스 스키마 + 비즈니스 규칙 |
| **SPARQL** | RDF 데이터를 조회하는 쿼리 언어 | 그래프 패턴 매칭을 통해 트리플 간의 복잡한 관계를 검색 | W3C SPARQL 1.1 | SQL의 그래프 버전 |
| **추론 엔진 (Reasoner)** | 온톨로지 규칙을 적용하여 새로운 지식 도출 | "A는 B의 서브클래스, X는 A의 인스턴스 → X는 B의 인스턴스"와 같은 논리적 연역 | OWL-DL, Pellet, HermiT | 논리학자의 연역 추론 |
| **지식 그래프 (Knowledge Graph)** | 대규모 RDF 데이터를 노드-엣지 그래프로 시각화/저장 | 그래프 DB(Neo4j, Blazegraph)가 수십억 개의 트리플을 저장하고 밀리초 단위에 탐색 | Google Knowledge Graph, DBpedia | 거대한 개념 지도 |

### 2. 정교한 구조 다이어그램: 시맨틱 웹 기술 스택 (Layer Cake)

```text
================================================================================
                    [ W3C Semantic Web Layer Cake (Technology Stack) ]
================================================================================

+-----------------------------------------------------------------------+
|                     Application Layer (응용 계층)                      |
|   [지능형 에이전트] [시맨틱 검색] [질의응답 시스템] [추천 엔진]         |
+-----------------------------------------------------------------------+
                                    |
+-----------------------------------------------------------------------+
|                 Query / Rule Layer (질의/규칙 계층)                    |
|    +-------------+    +-------------+    +----------------+            |
|    |   SPARQL    |    |    RIF      |    |   SWRL        |            |
|    |  (질의어)   |    | (규칙 교환) |    | (규칙 언어)   |            |
|    +-------------+    +-------------+    +----------------+            |
+-----------------------------------------------------------------------+
                                    |
+-----------------------------------------------------------------------+
|                    Ontology Layer (온톨로지 계층)                      |
|    +------------------------------------------------------------+     |
|    |         OWL (Web Ontology Language)                        |     |
|    |  [Class] [Property] [Restriction] [Cardinality] [Inference]|     |
|    +------------------------------------------------------------+     |
+-----------------------------------------------------------------------+
                                    |
+-----------------------------------------------------------------------+
|                    Data Interchange Layer (데이터 교환 계층)           |
|    +----------+    +----------+    +----------+    +----------+        |
|    |   RDF    |    |  RDFS    |    |  Turtle  |    | JSON-LD  |        |
|    | (트리플) |    | (스키마) |    | (문법)   |    | (JSON)   |        |
|    +----------+    +----------+    +----------+    +----------+        |
+-----------------------------------------------------------------------+
                                    |
+-----------------------------------------------------------------------+
|                 Identifier Layer (식별자 계층)                        |
|                    +--------------------------------+                  |
|                    |  URI / IRI (Unique Identifier) |                  |
|                    +--------------------------------+                  |
+-----------------------------------------------------------------------+
                                    |
+-----------------------------------------------------------------------+
|                 Foundation Layer (기반 계층)                          |
|    +----------+    +----------+    +----------+    +----------+        |
|    |Unicode   |    |  XML     |    |  Namesp  |    |Digital   |        |
|    |(문자셋)  |    | (구조)   |    |  ace     |    |Signature |        |
|    +----------+    +----------+    +----------+    +----------+        |
+-----------------------------------------------------------------------+

=> 각 계층은 하위 계층 위에 구축되며, 상위 계층으로 갈수록 더 풍부한 의미 표현 가능
```

### 3. RDF 트리플 구조와 지식 표현 예시
시맨틱 웹의 핵심 데이터 모델인 RDF는 모든 지식을 "주어(Subject) - 술어(Predicate) - 목적어(Object)"의 3요소로 분해하여 표현합니다.

```text
예시: "앨런 튜링은 컴퓨터 과학자이며, 맨체스터 대학에서 근무했다."

RDF 트리플로 변환:
1. (앨런 튜링, 직업, 컴퓨터 과학자)
2. (앨런 튜링, 근무지, 맨체스터 대학)
3. (앨런 튜링, 생년월일, 1912-06-23)
4. (앨런 튜링, 저명한 업적, 튜링 머신)

Turtle 문법으로 표현:
@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix schema: <http://schema.org/> .

ex:Alan_Turing a foaf:Person ;
    foaf:name "Alan Turing" ;
    schema:jobTitle "Computer Scientist" ;
    schema:worksFor ex:University_of_Manchester ;
    schema:birthDate "1912-06-23"^^xsd:date ;
    ex:knownFor ex:Turing_Machine .

ex:Turing_Machine a ex:TheoreticalConcept ;
    rdfs:label "Turing Machine" ;
    rdfs:comment "A mathematical model of computation" .
```

### 4. 핵심 알고리즘 및 실무 코드 예시: SPARQL 질의와 지식 그래프 구축

```python
from rdflib import Graph, Namespace, Literal, RDF, RDFS
from rdflib.namespace import FOAF, XSD
from SPARQLWrapper import SPARQLWrapper, JSON

# 1. RDF 그래프 생성 및 트리플 추가
g = Graph()

# 네임스페이스 정의 (URI 축약 표현)
EX = Namespace("http://example.org/knowledge/")
SCHEMA = Namespace("http://schema.org/")

# 앨런 튜링에 대한 지식 트리플 추가
g.add((EX.Alan_Turing, RDF.type, FOAF.Person))
g.add((EX.Alan_Turing, FOAF.name, Literal("Alan Turing")))
g.add((EX.Alan_Turing, SCHEMA.jobTitle, Literal("Computer Scientist")))
g.add((EX.Alan_Turing, SCHEMA.birthDate, Literal("1912-06-23", datatype=XSD.date)))
g.add((EX.Alan_Turing, EX.knownFor, EX.Turing_Machine))
g.add((EX.Alan_Turing, EX.workedAt, EX.University_of_Manchester))

# 튜링 머신에 대한 메타데이터
g.add((EX.Turing_Machine, RDF.type, EX.TheoreticalConcept))
g.add((EX.Turing_Machine, RDFS.label, Literal("Turing Machine")))
g.add((EX.Turing_Machine, RDFS.comment, Literal("A mathematical model of computation defining an abstract machine")))

# 2. SPARQL 질의: "컴퓨터 과학자가 무엇을 발명했는가?"
query = """
PREFIX ex: <http://example.org/knowledge/>
PREFIX schema: <http://schema.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?person ?name ?invention ?inventionName
WHERE {
    ?person a foaf:Person ;
            foaf:name ?name ;
            schema:jobTitle "Computer Scientist" ;
            ex:knownFor ?invention .
    ?invention rdfs:label ?inventionName .
}
"""

print("=== SPARQL 질의 결과 ===")
for row in g.query(query):
    print(f"인물: {row.name}")
    print(f"발명: {row.inventionName}")
    print(f"발명 URI: {row.invention}")
    print()

# 3. 외부 공개 지식 그래프(DBpedia) 질의
print("=== DBpedia 질의: 앨런 튜링의 정보 ===")
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX dbpedia: <http://dbpedia.org/resource/>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?abstract ?birthPlace ?deathDate
    WHERE {
        dbpedia:Alan_Turing dbpedia-owl:abstract ?abstract ;
                            dbpedia-owl:birthPlace ?birthPlace ;
                            dbpedia-owl:deathDate ?deathDate .
        FILTER (LANG(?abstract) = 'en')
    }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(f"설명: {result['abstract']['value'][:200]}...")
    print(f"출생지: {result['birthPlace']['value']}")
    print(f"사망일: {result['deathDate']['value']}")

# 4. 추론(Reasoning) 예시: RDFS 서브클래스 추론
# "컴퓨터 과학자는 과학자의 서브클래스"라는 규칙 추가
g.add((EX.Computer_Scientist, RDFS.subClassOf, EX.Scientist))
g.add((EX.Alan_Turing, RDF.type, EX.Computer_Scientist))

# RDFS 추론 엔진 적용
from rdflib.plugins.sparql import prepareQuery

# 추론 적용 후 질의: "튜링은 과학자인가?"
inference_query = prepareQuery("""
    SELECT ?type
    WHERE {
        ex:Alan_Turing a ?type .
    }
""", initNs={"ex": EX})

print("=== 추론 결과: 앨런 튜링의 타입 ===")
for row in g.query(inference_query):
    print(f"타입: {row.type.split('#')[-1] if '#' in row.type else row.type.split('/')[-1]}")
# 결과에 Computer_Scientist와 Scientist 모두 포함됨 (추론됨)
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 시맨틱 웹 vs 전통적 웹 vs 지식 그래프

| 평가 지표 | 전통적 웹 (HTML) | 시맨틱 웹 (RDF/OWL) | 지식 그래프 (Google/Microsoft) |
|:---|:---|:---|:---|
| **데이터 표현** | 비구조적 텍스트 + 프레젠테이션 태그 | 구조화된 트리플 (주어-술어-목적어) | 엔티티-관계 그래프 + 속성 |
| **의미 표현** | 없음 (사람만 이해 가능) | 명시적 (온톨로지로 정의) | 암시적 (머신러닝 추출) |
| **질의 방식** | 키워드 검색 (全文 검색) | SPARQL 패턴 매칭 | 그래프 탐색 + 벡터 유사도 |
| **상호운용성** | 낮음 (각 사이트 독자적 구조) | 높음 (표준 URI/RDF 사용) | 중간 (플랫폼 간 매핑 필요) |
| **추론 능력** | 없음 | 있음 (OWL 기반 논리 추론) | 제한적 (임베딩 기반 유추) |
| **확장성** | 높음 (문서 추가 용이) | 낮음 (온톨로지 유지 비용) | 높음 (자동 추출/보강) |
| **대표 사례** | 일반 웹사이트 | DBpedia, Wikidata | 구글 지식 패널, Bing 엔티티 |

### 2. 과목 융합 관점 분석
- **시맨틱 웹 + AI/LLM (GraphRAG)**: LLM은 학습 데이터 내의 패턴을 기반으로 답변을 생성하지만, 학습하지 않은 최신 정보나 도메인 특화 지식에 대해서는 환각(Hallucination)을 일으킵니다. 시맨틱 웹의 지식 그래프를 LLM에 연동하면, LLM이 답변 생성 시 지식 그래프에서 정확한 팩트를 검색(Retrieval)하여 답변의 신뢰성을 높일 수 있습니다. 이를 **GraphRAG**라고 합니다.
- **시맨틱 웹 + 데이터베이스**: 전통적인 RDBMS는 테이블 간의 조인(Join)으로 관계를 표현하지만, 복잡한 다단계 관계 탐색에 취약합니다. 그래프 데이터베이스(Neo4j, Amazon Neptune)는 노드-엣지 구조로 시맨틱 웹 데이터를 효율적으로 저장하고, Cypher/Gremlin 같은 그래프 질의어로 밀리초 단위에 관계를 탐색합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략
- **[상황 A] 제조기업의 부품 데이터 통합 (데이터 사일로 해결)**
  - **문제점**: 여러 협력사가 각기 다른 형식으로 부품 정보를 관리하여, 부품 호환성 검색과 대체 부품 발굴에 수주가 소요됨.
  - **기술사 판단**: 산업 표준 온톨로지(eCl@ss, UNSPSC)를 기반으로 모든 부품 데이터를 RDF로 변환하고, SPARQL 엔드포인트를 통해 통합 질의 시스템을 구축. 부품 A의 속성이 부품 B와 호환된다는 관계를 온톨로지에 정의하면, 추론 엔진이 자동으로 대체 부품을 발견.

- **[상황 B] 의료 분야 약물 상호작용 지식 베이스 구축**
  - **문제점**: 의사가 환자의 복용 약물 목록을 보고 잠재적 부작용을 확인하는 데 많은 시간 소요.
  - **기술사 판단**: 약물-성분-부작용 간의 관계를 온톨로지로 모델링하고, 환자가 복용 중인 약물 목록을 입력하면 추론 엔진이 "약물 A와 약물 B는 함께 복용 시 출혈 위험 증가"라는 경고를 자동 생성.

### 2. 도입 시 고려사항 (기술적/운영적 체크리스트)
- **온톨로지 구축 비용**: 도메인 전문가와 지식 엔지니어가 협업하여 개념과 관계를 정의하는 데 상당한 시간과 비용이 소요됩니다. 기존 공개 온톨로지(DBpedia, Schema.org)를 재사용하는 것으로 시작하는 것이 좋습니다.
- **데이터 품질 관리**: 잘못된 트리플이나 모순된 온톨로지 규칙은 추론 결과의 오류로 이어집니다. 데이터 검증 파이프라인(SHACL, ShEx)을 도입하여 품질을 관리해야 합니다.

### 3. 주의사항 및 안티패턴 (Anti-patterns)
- **오버 엔지니어링 (Over-engineering)**: 모든 데이터에 대해 복잡한 온톨로지를 구축하려는 시도는 실패합니다. 핵심 비즈니스 개체와 관계에 집중하고, 나머지는 단순한 메타데이터로 처리하는 점진적 접근이 필요합니다.
- **은둔 온톨로지 (Siloed Ontology)**: 독자적인 URI와 용어 체계를 사용하면 외부 데이터와 연동할 수 없습니다. 가능한 한 표준 어휘(Schema.org, FOAF, Dublin Core)를 사용해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 기존 (키워드 검색) | 시맨틱 웹 도입 후 | 개선 지표 |
|:---|:---|:---|:---|
| **검색 정확도** | 60~70% (키워드 일치) | 85~95% (의미 기반) | **정보 검색 효율 향상** |
| **데이터 통합 비용** | 수동 ETL 수주 소요 | 자동 매핑 (URI 기반) | **통합 프로젝트 기간 50% 단축** |
| **신규 지식 발견** | 전문가 수동 분석 | 추론 엔진 자동 발견 | **숨겨진 인사이트 도출** |
| **API 상호운용성** | 개별 API 개발 필요 | 표준 SPARQL 엔드포인트 | **개발 생산성 향상** |

### 2. 미래 전망 및 진화 방향
- **LLM + 지식 그래프 하이브리드 (Neuro-Symbolic AI)**: 신경망(LLM)의 패턴 인식 능력과 기호 AI(시맨틱 웹)의 논리적 추론 능력을 결합하는 방향으로 발전합니다. LLM이 자연어 질문을 이해하고, 지식 그래프에서 정확한 팩트를 검색하여 답변을 생성하는 하이브리드 아키텍처가 표준이 될 것입니다.
- **엔터프라이즈 지식 그래프 (EKG)**: 기업 내 모든 데이터(ERP, CRM, 문서, 로그)를 지식 그래프로 통합하여, 경영진이 "우리 회사의 핵심 리스크는 무엇인가?"와 같은 복합적 질문을 던지면 그래프 탐색과 추론으로 즉시 답변받는 시스템이 보편화될 것입니다.

### 3. 참고 표준/가이드
- **W3C RDF 1.1 Concepts and Abstract Syntax**: RDF 데이터 모델의 공식 사양.
- **W3C OWL 2 Web Ontology Language**: 온톨로지 정의 언어의 표준.
- **W3C SPARQL 1.1 Query Language**: RDF 질의 언어의 공식 표준.
- **Schema.org**: 구글, 마이크로소프트, 야후가 공동 개발한 웹 페이지 마크업 어휘 집합.

---

## 관련 개념 맵 (Knowledge Graph)
- **[RAG (검색 증강 생성)](@/studynotes/06_ict_convergence/04_ai_llm/rag.md)**: 시맨틱 웹의 지식 그래프를 LLM에 연동하여 환각 문제를 해결하는 기술.
- **[지식 그래프 (Knowledge Graph)](@/studynotes/06_ict_convergence/04_ai_llm/knowledge_graph.md)**: 구글 등이 시맨틱 웹 기술을 활용해 구축한 대규모 지식 베이스.
- **[온톨로지 (Ontology)](@/studynotes/06_ict_convergence/06_core_topics/ontology.md)**: 시맨틱 웹의 지식 스키마를 정의하는 철학적/기술적 모델.
- **[벡터 데이터베이스 (Vector Database)](@/studynotes/06_ict_convergence/04_ai_llm/vector_database.md)**: 시맨틱 웹과 LLM을 연결하는 임베딩 저장소.
- **[Web 3.0](@/studynotes/06_ict_convergence/02_blockchain/web3.md)**: 시맨틱 웹 + 탈중앙화가 결합된 차세대 인터넷 비전.

---

## 어린이를 위한 3줄 비유 설명
1. 지금의 인터넷은 마치 **글자만 알면 읽을 수 있는 책**이에요. 컴퓨터는 "사과"라는 글자를 저장할 수는 있지만, 이게 '맛있는 과일'인지 '애플 회사'인지는 몰라요.
2. 시맨틱 웹은 모든 단어에 **설명서(태그)를 붙이는 것**과 같아요. "이것은 과일이고, 빨간색이며, 비타민이 풍부해요"라고 컴퓨터에게 알려주는 거죠.
3. 그러면 컴퓨터가 우리가 묻는 말을 정말로 이해하게 돼요! "건강에 좋은 빨간 과일 뭐 있어?"라고 물으면, 컴퓨터가 스스로 생각해서 "사과랑 딸기가 있어요!"라고 대답할 수 있게 되는 거예요.
