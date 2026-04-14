+++
weight = 146
title = "생각의 사슬 (CoT, Chain-of-Thought) — 논리적 추론 유도 프롬프팅"
date = "2026-03-28"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
- **추론 과정의 명시적 생성**: 복잡한 문제 해결 시 "단계별로 차근차근 생각해 보자"는 지시를 통해 모델이 최종 정답 도출 전 중간 사고 과정을 텍스트로 생성하게 유도함.
- **수학/논리 성능의 비약적 향상**: 거대 모델의 발현 능력(Emergent Ability) 중 하나로, 중간 추론 경로(Reasoning Path)를 생성함으로써 계산 실수와 논리 비약을 획기적으로 줄임.
- **해석 가능성(Explainability) 제공**: 모델이 왜 그런 결론에 도달했는지 인간이 이해할 수 있는 형태로 보여주어 결과에 대한 신뢰도를 높임.

### Ⅰ. 개요 (Context & Background)
- **배경:** 초거대 언어 모델(LLM)은 간단한 지식 검색은 잘하지만, 여러 단계의 논리 연산이 필요한 산수나 상식 추론에서는 오답을 내는 경우가 많았음.
- **정의:** 2022년 구글(Google Brain) 연구진이 제안한 기법으로, 프롬프트에 추론 과정이 포함된 예시(Few-shot CoT)를 넣거나 "Step-by-step" 문구를 추가하여 사고를 강제하는 방식임.
- **가치:** 모델 자체를 수정하지 않고 오직 프롬프트 구성만으로 복잡한 문제 해결 능력을 획기적으로 끌어올린 혁신적 발견임.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ Standard Prompting vs Chain-of-Thought (CoT) ]

Standard Prompt:
Q: Roger has 5 tennis balls. He buys 2 more cans of 3 balls. How many now?
A: The answer is 11. (Wrong! 5 + 2*3 = 11? Wait, if model fails...)

Chain-of-Thought Prompt:
Q: Roger has 5 tennis balls. He buys 2 more cans of 3 balls. How many now?
A: Roger started with 5 balls. (Step 1)
   2 cans of 3 balls each is 6 balls. (Step 2)
   5 + 6 = 11. (Step 3)
   The answer is 11. (Correct Reasoning Path)

Mechanism:
- Sequential Decoding: Next token is conditioned on PREVIOUS reasoning tokens.
- Working Memory: Intermediate outputs act as a 'scratchpad' for the model.
```
- **작동 원리:** 언어 모델은 이전 토큰들을 기반으로 다음 토큰을 예측함. 중간 과정을 텍스트로 뱉어내면, 그 텍스트가 다음 연산의 강력한 힌트(Working Memory)가 되어 정확도를 높임.
- **Zero-shot CoT:** 예시 없이 "Let's think step by step"이라는 문구 하나만으로도 모델의 추론 엔진을 활성화할 수 있음.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | 일반 프롬프팅 | CoT 프롬프팅 | ToT (Tree-of-Thoughts) |
| :--- | :--- | :--- | :--- |
| **추론 방식** | 단답형 (Direct) | 선형적 단계 (Linear) | 분기형 탐색 (Tree/Search) |
| **복잡도 대응** | 낮음 | 중간 (논리 추론) | 높음 (전략적 기획) |
| **토큰 소모** | 최소 | 중간 | 높음 (여러 경로 생성) |
| **주요 용도** | 단순 요약, 분류 | 수학 문제, 상식 추론 | 창의적 글쓰기, 알고리즘 설계 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **실무 적용:** 세무/법률 상담 챗봇의 근거 조항 도출, 데이터 분석 에이전트의 쿼리 작성 단계 설계, 시스템 장애 원인 추론 도구.
- **기술사적 판단:** CoT는 단순한 팁이 아니라 LLM의 **'시스템 2 사고(느리고 논리적인 사고)'**를 이끌어내는 핵심 메커니즘임. 엔터프라이즈 AI 설계 시, 결과값의 정합성이 중요한 모든 지점에 CoT 설계를 기본 가이드로 포함시켜야 함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과:** 인공지능이 '직관'을 넘어 '논리'를 갖추게 함으로써, 자율 에이전트(Autonomous Agents)가 복잡한 과업을 스스로 계획하고 수행하는 토대를 마련함.
- **결론:** CoT는 모델의 지능을 프롬프트 수준에서 제어하는 핵심 기술로 안착했으며, 향후 자가 비판(Self-Correction) 및 검증 기술과 결합하여 인간의 논리 체계를 완벽히 모사하는 방향으로 발전할 것임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Instruction Prompting, Reasoning LLM
- **하위/확장 개념:** Zero-shot CoT, Least-to-Most Prompting, Self-Consistency, ToT (Tree-of-Thought)

### 👶 어린이를 위한 3줄 비유 설명
- 어려운 수학 문제를 풀 때 머릿속으로만 계산하면 틀리기 쉽지만, 연습장에 1번, 2번 순서를 써가며 풀면 훨씬 잘 풀리는 것과 같아요.
- 인공지능에게도 "연습장에 풀이 과정을 다 쓰면서 대답해 줘!"라고 말해주는 마법의 주문이랍니다.
- 덕분에 인공지능이 서두르지 않고 차근차근 생각해서 정답을 맞힐 수 있게 돼요!
