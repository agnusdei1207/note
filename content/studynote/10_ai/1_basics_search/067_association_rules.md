+++
weight = 67
title = "연관 규칙 (Association Rules)"
date = "2026-03-05"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
- 대규모 데이터셋 내 항목들 간의 **'함께 발생하는 관계'**를 발견하는 비지도 학습(Unsupervised Learning) 기법임.
- "A를 구매한 고객은 B도 구매할 가능성이 높다"는 식의 규칙을 찾아내어 **장바구니 분석(Market Basket Analysis)** 등에 활용됨.
- 지지도(Support), 신뢰도(Confidence), 향상도(Lift)라는 3대 지표를 통해 규칙의 유효성과 가치를 정량적으로 평가함.

### Ⅰ. 개요 (Context & Background)
- **배경:** 유통업체 등에서 품목 간의 상관관계를 파악하여 진열 위치 최적화나 교차 판매(Cross-selling) 전략을 세우기 위해 발전함.
- **정의:** 항목 집합(Itemset) 간의 조건부 확률적 관계를 $A \rightarrow B$ 형태로 나타낸 규칙임.
- **주요 알고리즘:** Apriori (빈번 항목 집합 추출), FP-Growth (트리 구조 이용 효율화).

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ Association Rule Evaluation Metrics ]
+-----------------------------------------------------------+
| 1. Support (지지도): P(A ∩ B)                              |
|    - 전체 거래 중 A와 B가 동시에 포함된 비율                |
| 2. Confidence (신뢰도): P(B|A) = Support(A∩B) / Support(A) |
|    - A를 포함한 거래 중 B도 포함된 비율                    |
| 3. Lift (향상도): Confidence(A->B) / P(B)                  |
|    - 우연히 B가 발생할 확률 대비 A와 함께 발생할 확률 비율   |
+-----------------------------------------------------------+
  * Lift > 1: 양의 상관관계 / Lift = 1: 독립 / Lift < 1: 음의 상관관계
```
- **Apriori 원리:** "어떤 항목 집합이 빈번하면, 그 집합의 모든 부분 집합도 빈번하다"는 성질을 이용해 탐색 범위를 획기적으로 줄임(Pruning).

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | 연관 규칙 (Association Rules) | 협업 필터링 (Collaborative Filtering) |
| :--- | :--- | :--- |
| **데이터 형태** | 트랜잭션 데이터 (구매 기록 등) | 평점 데이터 (User-Item Matrix) |
| **주요 목표** | 항목 간의 동시 발생 패턴 발견 | 특정 사용자에게 맞는 항목 추천 |
| **학습 방식** | 규칙 기반 (Rule-based) | 유사도 기반 (Similarity-based) |
| **장점** | 설명력이 높고 직관적임 | 개인화된 추천이 가능함 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **적용 사례:** 마트 진열(맥주와 기저귀), 온라인 쇼핑몰 추천 섹션, 검색어 연관 추천, 웹 로그 분석(페이지 이동 패턴).
- **기술사적 판단:** 단순한 상관관계가 인과관계를 의미하지 않음을 유의해야 함. 의미 없는 규칙(Trivial Rules)을 걸러내기 위해 향상도(Lift)를 기준으로 전략적 판단을 내리는 것이 중요함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과:** 데이터 속에 숨겨진 고객의 행동 패턴을 정량적으로 도출하여 비즈니스 의사결정의 객관성을 확보함.
- **결론:** 연관 규칙 분석은 전통적인 데이터 마이닝 기법이나, 최근 그래프 DB 및 실시간 추천 엔진과 결합하여 그 가치가 재조명되고 있음.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Unsupervised Learning, Data Mining
- **연관 개념:** Apriori Algorithm, FP-Growth, Market Basket Analysis, Sequence Mining

### 👶 어린이를 위한 3줄 비유 설명
- 마트 영수증들을 모아서 "이걸 산 사람은 저것도 샀네?" 하는 규칙을 찾는 보물찾기 게임이에요.
- 예를 들어 "빵을 사는 사람은 잼도 같이 산다"는 걸 알면, 빵 옆에 잼을 놓아서 쇼핑을 편하게 해줄 수 있죠.
- 사람들의 습관을 숫자로 분석해서 똑똑한 추천을 해주는 기술이랍니다.
