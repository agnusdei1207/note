+++
weight = 60
title = "RPA 및 초자동화 (Hyperautomation)"
date = "2024-03-20"
[extra]
categories = "studynote-it-management"
+++

## 핵심 인사이트 (3줄 요약)
- **RPA(Robotic Process Automation)**는 사람이 수행하는 단순 반복적 업무를 소프트웨어 봇(Bot)이 자동화하여 업무 효율을 극대화하는 기술임.
- **초자동화(Hyperautomation)**는 RPA에 AI, 머신러닝, 프로세스 마이닝 등을 결합하여 복잡한 비즈니스 프로세스 전체를 자동화하는 확장된 개념임.
- 인간은 창의적이고 전략적인 고부가가치 업무에 집중하고, 단순 노동은 디지털 워크포스(Digital Workforce)에게 맡기는 **협업 패러다임**임.

### Ⅰ. 개요 (Context & Background)
- 저출산 및 고령화에 따른 노동력 부족과 기업의 운영 효율성(Operational Efficiency) 개선 요구가 맞물려 필수적인 IT 전략으로 급부상함.
- 초기에는 정형 데이터 기반의 단순 루틴 자동화에 집중했으나, 현재는 비정형 데이터(OCR, NLP)를 처리하는 지능형 자동화로 진화함.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ Hyperautomation Architecture Stack ]

    /-------------------------------------------\
    |  Orchestration (AI/ML Platform, Flow)     | <--- 제어/지능화
    |  /-------------------------------------\  |
    |  |  Cognitive Intelligence (NLP, OCR)   |  | <--- 판단/분석
    |  |  /-----------------------------\     |  |
    |  |  |  Process Mining / Analytics  |     |  | <--- 식별/발견
    |  |  |  /-------------------\      |     |  |
    |  |  |  |   RPA Bot Execution |      |     |  | <--- 실행/자동화
    |  |  |  | (Software Robots)   |      |     |  |
    |  |  |  \-------------------/      |     |  |
    |  \-------------------------------------/  |
    \-------------------------------------------/

* RPA Types: Attended (사람 개입) vs Unattended (완전 자동)
```
- **RPA Bot**: UI 자동화를 통해 시스템 간 데이터를 이동시키고 규정된 규칙에 따라 작업을 수행함.
- **Process Mining**: 실제 시스템 로그를 분석하여 숨겨진 비효율적 프로세스를 찾아내고 자동화 대상을 식별함.
- **Cognitive Automation**: 인공지능(AI)을 결합하여 이메일 내용 이해, 문서 요약, 이미지 분류 등 비정형 업무를 처리함.
- **Orchestration**: 수많은 봇의 스케줄링, 라이프사이클 관리, 성과 모니터링을 중앙에서 통제함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 전통적 자동화 (Script/API) | RPA (UI Automation) | 초자동화 (Hyperautomation) |
| :--- | :--- | :--- | :--- |
| **대상 시스템** | API 지원 시스템 한정 | 거의 모든 UI (Legacy 포함) | 전사적 비즈니스 프로세스 |
| **자동화 범위** | 데이터 연계 중심 | 작업(Task) 단위 자동화 | End-to-End 전체 자동화 |
| **지능 수준** | 하드코딩된 규칙 | 정해진 시나리오 순종 | 학습 및 적응 (AI 기반) |
| **주요 도구** | Python, Java, Batch | UiPath, BluePrism, AA | AI, RPA, Process Mining 결합 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **판단 지표**: 규칙이 명확하고(Rule-based), 거래량이 많으며(High-volume), 데이터가 디지털화된 반복 업무를 우선 선정(ROI 극대화)해야 함.
- **적용 전략**: 'Bot-first' 문화를 구축하되, 섀도우 IT 및 관리 부재로 인한 '봇의 난립'을 방지하기 위해 전사적인 CoE(Center of Excellence) 조직 운영이 필수적임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **운영 비용(OPEX) 절감**과 **업무 처리 속도 향상**을 넘어, 인간의 실수를 원천 차단하여 데이터 신뢰도를 높임.
- 미래에는 생성형 AI와 결합된 에이전트(Agentic Workflow) 형태로 진화하여, 지시 한 번에 복잡한 업무를 스스로 설계하고 실행하는 '자율 자동화' 단계로 나아갈 것임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 비즈니스 프로세스 관리 (BPM), 디지털 트랜스포메이션
- **기술 구성**: 프로세스 마이닝, OCR (Optical Character Recognition), NLP
- **관리 체계**: CoE (Center of Excellence), 디지털 워크포스

### 👶 어린이를 위한 3줄 비유 설명
- 지루한 숙제를 대신 해주는 '마법의 로봇 손'이 생긴 것과 같아요.
- 로봇 손은 시키는 대로만 하는 게 아니라, 공부를 더 많이 해서 어려운 문제도 스스로 생각해서 풀 줄 알게 돼요.
- 이제 여러분은 로봇 손에게 일을 시키고, 더 재미있는 놀이와 새로운 생각을 할 수 있는 시간을 갖게 되는 거예요.
