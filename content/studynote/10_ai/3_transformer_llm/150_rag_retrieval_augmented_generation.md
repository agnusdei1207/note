+++
title = "RAG (Retrieval-Augmented Generation)"
weight = 150
date = "2024-03-21"
[extra]
categories = ["AI", "LLM", "RAG"]
+++

## 핵심 인사이트 (3줄 요약)
- **검색 증강 생성**: LLM이 학습하지 않은 최신 데이터나 기업 내부 보안 문서를 외부 데이터베이스에서 실시간으로 검색하여 답변 생성에 활용하는 기술임.
- **할루시네이션(환각) 억제**: 모델의 내재된 지식에만 의존하지 않고 신뢰할 수 있는 출처(Context)를 바탕으로 답변하게 하여 정확도와 근거성을 확보함.
- **지식 업데이트 비용 혁신**: 모델을 매번 재학습(Fine-tuning)시키지 않고도, 외부 지식 저장소의 데이터만 교체함으로써 최신 정보를 반영할 수 있음.

### Ⅰ. 개요 (Context & Background)
- **배경**: LLM은 학습 데이터 절단 시점(Knowledge Cut-off) 이후의 정보를 알지 못하며, 사실 관계를 틀리게 말하는 환각 현상이 고질적인 문제였음.
- **정의**: 검색(Retrieval) 모델과 생성(Generation) 모델을 결합하여, 질문과 관련된 문서를 찾아 이를 참고문헌으로 제공한 뒤 답변을 생성하는 프레임워크임.
- **가치**: 엔터프라이즈 환경에서 보안이 중요한 사내 문서 기반 Q&A 시스템을 구축할 때 가장 현실적이고 효율적인 대안으로 평가받음.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ RAG Workflow: Search -> Augment -> Generate ]

 1. User Query ----> [ Embedding Model ] ----> [ Vector Search ]
                          |                          |
                          v                          v
                  (Query Vector) <------> [ Vector DB / Index ]
                                                     |
 2. Retrieve Relevant Chunks <-----------------------+
           |
 3. [ Prompt Construction ]
    - User Query: "..."
    - Reference Context: "Found Data 1, 2, 3..."
           |
           v
 4. [ LLM Generation ] ----> Final Grounded Answer

[ Key Components ]
- Chunking: Breaking documents into small, semantic pieces.
- Embedding: Converting text to high-dimensional vectors.
- Vector DB: Efficiently searching top-K similar chunks (FAISS, Pinecone).
```
- **임베딩(Embedding)**: 의미적 유사성을 계산하기 위해 텍스트를 벡터 공간으로 변환함.
- **시맨틱 검색(Semantic Search)**: 단순 키워드 매칭이 아닌 단어의 맥락과 의미를 기반으로 관련 문서를 찾아냄.
- **프롬프트 주입(Context Injection)**: 검색된 지식을 "다음 내용을 참고해서 질문에 답해줘"라는 명령과 함께 LLM에 전달함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 파인 튜닝 (Fine-Tuning) | RAG (검색 증강) |
| :--- | :--- | :--- |
| **지식 획득** | 모델 파라미터 내부에 저장 | 외부 데이터베이스에 저장 |
| **정보 최신성** | 재학습 전까지는 과거 정보 | 실시간 업데이트 가능 (DB만 교체) |
| **근거 제시** | 불가능 (블랙박스) | 가능 (참조 문서 링크/출처 제공) |
| **구축 비용** | 높음 (GPU 및 데이터 정제) | 상대적으로 낮음 (인프라 위주) |
| **할루시네이션** | 발생 가능성 있음 | 획기적으로 낮춤 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **하이브리드 검색**: 의미 기반의 벡터 검색과 정확한 키워드 기반의 전통적 검색(BM25)을 결합하여 검색 정확도를 극대화해야 함.
- **데이터 보안**: 민감한 데이터는 외부 API로 보내지 않고 로컬 LLM과 사내 벡터 DB를 연동하는 에어갭(Air-gap) 환경의 RAG 구축이 보안 전략의 핵심임.
- **기술사적 판단**: RAG의 성능은 검색된 문서의 질(Precision/Recall)에 달려 있으므로, 문서 파싱(Parsing) 및 청킹(Chunking) 전략 수립이 성공의 80%를 결정함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **동적 지식 생태계**: 단순 지식 전달을 넘어, 웹 검색 API와 연동하여 실시간 뉴스와 트렌드를 반영하는 'AI 에이전트'로 발전 중임.
- **평가 체계(Ragas)**: 답변의 충실도(Faithfulness), 관련성(Relevance) 등을 정량적으로 측정하는 평가 프레임워크가 표준화되고 있음.
- **결론**: RAG는 LLM의 가장 큰 약점인 신뢰성을 해결하는 실용적 해법이며, 기업용 지능형 서비스 구현을 위한 Professional Engineer의 필수 도구임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **Vector Database**: 지식 저장소
- **Hallucination**: 해결 목표
- **Semantic Search**: 핵심 엔진
- **Prompt Engineering**: 활용 기술

### 👶 어린이를 위한 3줄 비유 설명
1. 똑똑하지만 기억력이 조금 가물가물한 박사님(LLM) 옆에, 아주 큰 도서관(DB)을 지어주는 거예요.
2. 우리가 질문을 하면, 비서가 도서관에서 관련 책들을 찾아 박사님 책상에 놓아줍니다.
3. 박사님은 그 책들을 슥 읽어보고 "책에 따르면 이렇단다!"라고 정확하게 대답해 주시는 거예요.
