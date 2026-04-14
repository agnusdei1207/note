+++
weight = 68
title = "특성 공학 (Feature Engineering)"
date = "2026-03-05"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
- 도메인 지식을 활용하여 원본 데이터로부터 모델 학습에 가장 적합한 **특성(Feature)들을 추출, 선택, 변형**하는 과정임.
- "데이터와 특성이 모델의 성능 한계를 결정한다"는 원칙 하에, 알고리즘 개선보다 더 직접적인 **모델 성능 향상**을 이끄는 핵심 단계임.
- 데이터의 본질적 패턴을 모델이 잘 학습할 수 있도록 가공하여 모델의 복잡도를 낮추고 일반화 성능을 높임.

### Ⅰ. 개요 (Context & Background)
- **배경:** 기계는 원본 데이터(Raw Data)를 그대로 이해하기 어려우며, 데이터 내에 노이즈나 불필요한 정보가 섞여 있으면 학습 효율이 급격히 떨어짐.
- **정의:** 머신러닝 알고리즘이 작동할 수 있도록 입력 데이터를 최적화하는 모든 과정.
- **중요성:** 우수한 특성 하나가 수천 번의 하이퍼파라미터 튜닝보다 나은 결과를 가져오는 경우가 많음.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ Feature Engineering Workflow ]
Raw Data ----+----> [ Feature Generation ] : 새로운 수치 생성 (예: 나이->연령대)
             |
             +----> [ Feature Transformation ] : 스케일링, 인코딩, 로그 변환
             |
             +----> [ Feature Selection ] : 상관관계 분석 등으로 유효 특성 선별
             |
             +----> [ Feature Extraction ] : PCA 등을 통한 차원 축소
             v
         Optimal Input Dataset (For Model Training)
```
- **주요 기법:**
  - **Scaling:** 정규화(Normalization), 표준화(Standardization).
  - **Encoding:** One-hot encoding, Label encoding.
  - **Handling Outliers:** 이상치 제거 또는 클리핑(Clipping).
  - **Interaction Features:** 두 변수의 곱이나 조합으로 새로운 의미 창출.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | 특성 선택 (Selection) | 특성 추출 (Extraction) |
| :--- | :--- | :--- |
| **방식** | 기존 특성 중 일부를 골라냄 | 기존 특성을 조합하여 새로운 특성 생성 |
| **정보 손실** | 버려지는 특성의 정보는 완전히 사라짐 | 전체 정보의 분산을 보존하려 노력함 |
| **해석력** | 원본 의미가 유지되어 해석이 쉬움 | 새로운 축(Component)으로 변해 해석이 어려움 |
| **예시** | Filter, Wrapper, Embedded Method | PCA, LDA, Autoencoder |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **적용 사례:** 날짜 데이터에서 '주말 여부' 추출, 텍스트 데이터에서 '단어 빈도' 추출, 센서 데이터에서 '이동 평균' 계산.
- **기술사적 판단:** 특성 공학은 도메인 전문가와 데이터 과학자의 협업이 가장 빛나는 지점임. 과도한 특성 생성은 **차원의 저주(Curse of Dimensionality)**를 유발하므로 정규화(Regularization)와 교차 검증을 병행해야 함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과:** 모델의 수렴 속도 향상, 예측 정확도 개선, 오버피팅 방지 및 모델 해석력 증대.
- **결론:** 최근 AutoML 등이 발전하고 있으나, 데이터의 맥락을 읽는 인간의 직관이 반영된 특성 공학은 여전히 인공지능 성능의 초격차를 만드는 결정적 요소임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Machine Learning Pipeline, Data Preprocessing
- **연관 개념:** PCA, One-hot Encoding, Curse of Dimensionality, Domain Knowledge

### 👶 어린이를 위한 3줄 비유 설명
- 요리사가 시장에서 사온 흙 묻은 채소(Raw Data)를 깨끗이 씻고 다듬어서 요리하기 좋게 만드는 과정이에요.
- 감자를 통째로 넣는 것보다 깍둑썰기를 하거나 으깨서 넣으면 훨씬 맛있는 요리(Model)가 되는 것과 같죠.
- 기계가 공부를 잘할 수 있게 문제를 예쁘고 이해하기 쉽게 정리해주는 친절한 노트 정리법이랍니다.
