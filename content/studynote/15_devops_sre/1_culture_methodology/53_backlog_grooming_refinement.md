+++
title = "백로그 정제 (Backlog Grooming & Refinement)"
weight = 55
date = "2026-03-04"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
1. **백로그 정제**는 다음 스프린트를 위해 우선순위를 재조정하고, 사용자 스토리의 상세 내용을 구체화하여 준비 상태를 유지하는 지속적 활동이다.
2. 명확한 **수락 기준(Acceptance Criteria)**과 **준비 완료 정의(DoR)**를 수립하여 개발 단계에서의 불확실성과 커뮤니케이션 낭비를 최소화한다.
3. 제품 책임자(PO)와 개발팀이 정기적으로 협력하여 비즈니스 가치와 기술적 실현 가능성 사이의 합의를 도출하는 가교 역할을 수행한다.

### Ⅰ. 개요 (Context & Background)
- **배경**: 스프린트 플래닝(Planning) 시간은 한정되어 있으므로, 계획 단계 전에 백로그 항목들을 충분히 검토하고 쪼개어 놓아야 한다.
- **필요성**: 정제되지 않은 거대하고 모호한 스토리(Epic)는 추정 오류와 개발 도중의 요구사항 변경을 초래하여 팀의 예측 가능성을 떨어뜨린다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **정제 프로세스 (DEEP Principle)**:
  - **Detailed appropriately**: 상위 항목일수록 더 상세하게 기술
  - **Estimated**: 각 항목에 대해 팀의 노력을 수치화(Story Point)
  - **Emergent**: 요구사항 변화에 따라 유동적으로 추가/삭제
  - **Prioritized**: 비즈니스 가치와 리스크에 따라 순서 정렬

```text
[Backlog Refinement Flow]

(Input) Raw Ideas       (Process) Refinement Meeting         (Output) Ready Backlog
+-------------------+      +-------------------------+      +---------------------+
|  Customer Needs   |      | 1. Item Decomposition   |      |  High Priority Items |
|  Stakeholders     | ==>  | 2. Clarify Criteria     | ==>  |  Estimated Effort    |
|  Bugs & Technical |      | 3. Prioritization       |      |  Clear Definition    |
+-------------------+      +-------------------------+      +---------------------+
                                       ||
                                       \/
                           +--------------------------+
                           |   Definition of Ready    |
                           |   (DoR Check: INVEST)    |
                           +--------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 스프린트 플래닝 (Planning) | 백로그 정제 (Refinement) |
| :--- | :--- | :--- |
| **수행 시점** | 스프린트 시작 직전 (이벤트) | 스프린트 기간 중 수시 (지속적 활동) |
| **주요 목표** | "이번에 무엇을, 어떻게 할 것인가?" | "다음에 할 일들이 준비되어 있는가?" |
| **핵심 결과물** | 스프린트 백로그 (Sprint Backlog) | 정제된 제품 백로그 (Product Backlog) |
| **참여 범위** | 팀 전원 필수 참여 | PO와 핵심 개발자(상황에 따라 유동적) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **실무 적용**: 전체 스프린트 시간의 약 10% 이내를 정제 활동에 할당하며, INVEST 원칙(Independent, Negotiable, Valuable, Estimable, Small, Testable)을 체크리스트로 활용한다.
- **기술사적 판단**: 백로그 정제는 단순한 문서 작업이 아니라, 팀 내 공유된 이해(Shared Understanding)를 구축하는 과정이다. 기술적 난도가 높은 항목은 'Spike' 스토리를 발행하여 사전 조사를 병행하는 유연함이 필요하다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 스프린트 계획 시간 단축, 개발 팀의 집중도 향상, 이해관계자와의 신뢰 구축 및 제품 인도 품질의 균일화.
- **결론**: 잘 정제된 백로그는 팀의 엔진을 원활하게 돌리는 '윤활유'이며, 지속적인 정제 문화가 정착된 조직일수록 변화하는 시장 요구에 민첩하게 대응할 수 있다.

### 📌 관련 개념 맵 (Knowledge Graph)
1. **User Story**: 사용자의 관점에서 작성된 기능 설명 ("~로서, ~하고 싶다, ~를 위해")
2. **Acceptance Criteria**: 스토리 완료 여부를 판정하는 구체적 체크리스트
3. **Definition of Ready (DoR)**: 스토리가 개발을 시작하기에 충분히 준비되었는지 판단하는 기준

### 👶 어린이를 위한 3줄 비유 설명
1. **백로그 정제**: 요리를 하기 전에 냉장고에 있는 재료들을 미리 씻고, 썰고, 어떤 순서로 요리할지 생각하는 준비 시간이에요.
2. **이유**: 미리 준비해두지 않으면, 요리할 때 칼을 찾거나 재료가 없어서 허둥지둥하다가 음식을 태울 수 있기 때문이에요.
3. **결론**: 맛있는 음식을 빨리 만들기 위해 요리사가 미리 도마를 정리하는 아주 중요한 과정이에요.
