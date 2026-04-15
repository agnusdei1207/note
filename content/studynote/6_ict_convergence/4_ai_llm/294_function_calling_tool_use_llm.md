+++
title = "294. 함수 호출 (Function Calling / Tool Use) - LLM과 현실 세계를 연결하는 핵심 인터페이스"
weight = 299
date = "2026-03-04"
[extra]
categories = "studynote-ict-convergence"
+++

## 핵심 인사이트 (3줄 요약)
- **API 연동의 가교:** LLM이 사용자의 의도를 분석하여 사전에 정의된 외부 API(함수)를 실행하기 위한 매개변수(JSON)를 스스로 생성하는 기술.
- **최신성 및 정확성 확보:** 모델의 학습 데이터에 없는 실시간 정보(날씨, 주가, 예약 현황 등)를 외부 시스템 호출을 통해 보완함으로써 환각 현상을 획기적으로 개선.
- **액션 지향형 AI:** 단순히 텍스트를 생성하는 수준을 넘어, 데이터베이스 조회, 이메일 발송, 장치 제어 등 실질적인 '행동'을 수행하는 에이전트의 기반 기술.

### Ⅰ. 개요 (Context & Background)
대형 언어 모델(LLM)은 뛰어난 언어 능력을 갖추었지만, 학습 시점 이후의 정보나 복잡한 수학 계산, 특정 시스템의 내부 데이터를 알지 못한다는 한계가 있습니다. **함수 호출(Function Calling)** 또는 **도구 사용(Tool Use)**은 이러한 LLM의 뇌와 외부 시스템의 손발을 연결하는 인터페이스입니다. 모델이 직접 함수를 실행하는 것이 아니라, 실행에 필요한 "정교한 JSON 형식의 데이터"를 출력하면 서버가 이를 실행하고 결과를 모델에게 다시 전달하여 최종 답변을 완성하는 구조입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
함수 호출은 '정의 -> 의도 파악 -> JSON 생성 -> 실행 -> 결과 전달'의 5단계 루프로 작동합니다.

```text
[Function Calling Workflow]
      User Request          System (Server)             LLM (Brain)
    +--------------+      +------------------+      +------------------+
    | "Check stock | ---> | 1. Provide Tool  | ---> | 2. Select Tool   |
    |  of Item A"  |      |    Definitions   |      | 3. Extract Params|
    +--------------+      +------------------+      +---------┬--------+
                                  ▲                           |
                                  |                           ▼
    +--------------+      +-------┴----------+      +------------------+
    | Final Answer | <--- | 5. Feed Result   | <--- | 4. Output JSON   |
    | "Item A is   |      | 6. Execute Tool  |      | {item: 'A',...}  |
    | in stock"    |      +------------------+      +------------------+
    +--------------+

 [Key Mechanism]
 - Tool Definition: Describing API functions in JSON Schema format.
 - Intent Mapping: Matching user natural language to specific function.
 - Argument Extraction: Parsing entities from text to fill function parameters.
```

1. **도구 정의 (Tool Definition):** 함수 이름, 설명, 매개변수 타입 등을 JSON Schema로 정의하여 모델에게 전달.
2. **의도 및 파라미터 추출:** 사용자의 질문에서 "어떤 함수"를 "어떤 인자"로 호출할지 판단.
3. **구조화된 출력:** 자연어가 아닌 API 규격에 맞는 JSON 형식으로 응답 생성.
4. **실행 및 관측:** 서버가 실제 API를 호출하고 그 결과(JSON)를 다시 모델에게 프롬프트로 주입.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Comparison) | 일반 텍스트 생성 (Normal Text) | 함수 호출 (Function Calling) | 코드 해석기 (Code Interpreter) |
|---|---|---|---|
| **출력 형태** | 자연어 (Natural Language) | 구조화된 데이터 (JSON) | 프로그래밍 코드 (Python) |
| **작동 환경** | 모델 내부 연산 | 외부 API / 시스템 연동 | 샌드박스 내 코드 실행 |
| **정확도** | 환각 가능성 있음 | 외부 시스템 데이터로 정확함 | 수치 계산에 매우 정확함 |
| **적용 사례** | 요약, 번역, 창작 | 예약, DB 조회, 기기 제어 | 복잡한 수학, 데이터 시각화 |
| **주요 장점** | 창의성, 유연성 | 시스템 간 통합, 실시간성 | 논리적 엄밀함 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
**[실무 적용 전략]**
- **SaaS 통합:** "최근 3일간의 매출 보고서를 슬랙으로 보내줘"라는 요청을 받으면, `매출조회_API`를 호출하고 그 결과를 `슬랙전송_API`의 인자로 전달하는 워크플로우 자동화.
- **SQL 및 DB 보안:** 자연어를 SQL로 직접 바꾸는 방식보다, 정의된 함수(Read-only API)를 호출하게 함으로써 DB 직접 접근에 따른 보안 리스크를 완화.

**[기술사적 판단]**
함수 호출은 LLM이 '플랫폼'으로 진화하기 위한 OS의 시스템 콜(System Call)과 같은 역할을 합니다. 모델의 파라미터 수가 적더라도(sLLM), 함수 호출 능력이 뛰어나다면 실무 활용도는 훨씬 높을 수 있습니다. 다만, 모델이 잘못된 인자를 생성하거나 민감한 함수를 잘못 호출하는 것을 방지하기 위한 '파라미터 검증(Schema Validation)'과 '실행 권한 제어'가 보안 측면에서 매우 중요하게 다루어져야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
함수 호출 기술의 표준화는 'AI 에코시스템' 구축의 핵심입니다. 현재 OpenAI, Anthropic, Google 등 주요 벤더들이 각자의 규격으로 제공하고 있으나, 향후 이기종 모델 간에도 도구를 공유할 수 있는 표준 프로토콜이 등장할 것입니다. 이는 결국 AI가 스스로 필요한 소프트웨어를 찾아 사용하고, 인간의 복잡한 비즈니스 로직을 자율적으로 처리하는 '자율 에이전트 시대'를 앞당기는 기폭제가 될 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **기반 기술:** JSON Schema, REST API, Zero-shot Learning
- **프레임워크:** LangChain (Tools), OpenAI Functions, Tool Use (Claude)
- **연관 개념:** RAG (Retrieval), Agentic Workflow, SQL Injection 방어

### 👶 어린이를 위한 3줄 비유 설명
1. **일반 AI**는 똑똑하지만 팔다리가 없는 친구라 "피자 주문해줘"라고 하면 피자 만드는 법만 설명해 줘요.
2. **함수 호출**은 AI가 피자 가게 전화번호(API)를 찾아 "페퍼로니 한 판(매개변수)"이라고 적힌 메모를 나에게 건네주는 것과 같아요.
3. 그 메모를 보고 내가 대신 전화를 걸어주면, 팔다리 없는 AI도 진짜 피자를 주문할 수 있게 된답니다!
