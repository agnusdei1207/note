+++
weight = 96
title = "불균형 데이터 증강 (Oversampling) - SMOTE"
date = "2026-03-04"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
- SMOTE(Synthetic Minority Over-sampling Technique)는 소수 클래스 데이터를 단순 복제하는 대신, 인접한 데이터 사이의 선형 보간을 통해 가상의 '합성 데이터'를 생성하는 기법임.
- 단순 오버샘플링의 고질적 문제인 과적합(Overfitting)을 방지하고, 소수 클래스의 결정 경계(Decision Boundary)를 확장하여 모델의 재현율(Recall)을 극대화함.
- 금융 사기 탐지(FDS), 희귀 질병 진단 등 클래스 불균형이 극심한 도메인에서 모델의 일반화 성능을 확보하기 위한 필수 전처리 전략임.

### Ⅰ. 개요 (Context & Background)
현실 세계의 데이터는 대부분 불균형(Imbalanced)하다. 정상 거래는 수백만 건이지만 사기 거래는 수십 건에 불과하다. 이 상태로 모델을 학습시키면 모델은 단순히 "모두 정상이다"라고 예측해도 99.9%의 정확도(Accuracy)를 얻게 되어, 정작 중요한 소수 클래스를 식별하지 못하는 '정확도의 함정'에 빠진다. SMOTE는 이러한 불균형을 해소하기 위해 K-최근방 이웃(K-NN) 알고리즘을 활용하여 소수 데이터를 수학적으로 증강시킨다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

SMOTE는 소수 클래스의 데이터 포인트들 사이의 공간에 새로운 샘플을 '합성'하여 데이터 밀도를 높인다.

```text
[ SMOTE Data Augmentation Logic ]

Minority Class (A) .       . (B)   <-- Selected Sample & its Neighbor
                    \     /
                     \   /
                      (X)          <-- Newly Synthesized Sample (Interpolation)
                     /   \
                    /     \
Minority Class (C) .       . (D)

1. Select a minority sample (i).
2. Find its K-nearest neighbors (K-NN) within the same class.
3. Randomly choose one neighbor (j).
4. Create a new sample: X = sample(i) + rand(0,1) * (sample(j) - sample(i))

[ Bilingual Comparison ]
- Synthesis (합성): 단순 복제(Duplication)가 아닌 새로운 좌표 생성.
- Interpolation (보간): 두 점 사이의 선형적 위치에 배치.
- Overfitting Risk (과적합 위험): 단순 복제보다 낮으나 노이즈 생성 가능성 존재.
- K-NN (K-최근방 이웃): 합성의 기준이 되는 주변 표본 탐색 알고리즘.
```

단순히 데이터를 복사하는 Random Over-sampling은 특정 지점에만 가중치가 쏠려 과적합을 유발하지만, SMOTE는 데이터 사이의 '선' 위에서 샘플을 생성하므로 결정 영역을 더 넓고 부드럽게 확장한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | Random Under-sampling | Random Over-sampling | SMOTE (Oversampling) |
| :--- | :--- | :--- | :--- |
| **핵심 기제** | 다수 클래스 데이터 삭제 | 소수 클래스 데이터 단순 복제 | 소수 클래스 데이터 **합성 생성** |
| **정보 손실** | 매우 높음 (중요 정보 유실) | 없음 | 없음 |
| **과적합 위험** | 낮음 | 매우 높음 (중복 학습) | 낮음 (일반화 성능 향상) |
| **단점** | 학습 데이터 부족 초래 | 모델이 소수 데이터에만 집착 | 노이즈 데이터 생성 가능성 (Borderline 문제) |
| **추천 도메인** | 대규모 데이터셋 (Big Data) | 베이스라인 모델 구축 시 | **FDS, 의료 진단, 불량 탐지** |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **(검증 세트 분리)** SMOTE 적용 시 가장 흔히 범하는 실수는 '전체 데이터'에 SMOTE를 적용한 뒤 학습/검증셋을 나누는 것이다. 이 경우 검증 데이터가 학습 데이터의 합성본을 포함하게 되어 성능이 과대평가(Data Leakage)된다. 반드시 학습셋(Train)에만 적용하고 검증셋(Val/Test)은 원본 상태를 유지해야 한다.
- **(하이브리드 전략)** SMOTE로 소수 데이터를 늘린 후, Tomek Links나 ENN(Edited Nearest Neighbors) 같은 언더샘플링 기법을 추가 적용하여 클래스 간 경계의 노이즈를 제거하는 'SMOTE-Tomek' 결합 방식이 실무 성능이 가장 우수하다.
- **(변형 알고리즘)** 경계선에 있는 데이터에 집중하는 Borderline-SMOTE나, 밀도에 따라 가중치를 주는 ADASYN 등을 데이터 특성에 맞춰 선택해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
SMOTE는 데이터 엔지니어링 단계에서 '모델의 공정성'과 '희귀 사건 탐지력'을 보장하는 표준 기술이다. 최근에는 정형 데이터뿐만 아니라 이미지(GAN 기반 증강)나 텍스트(Back-translation) 등 비정형 데이터 증강 기법으로 사상이 확장되고 있다. 데이터의 양보다 '클래스 밸런스'가 모델의 비즈니스 가치를 결정하는 만큼, SMOTE와 같은 통계적 증강 기법에 대한 깊은 이해는 필수적이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **Imbalanced Data**: 불균형의 근본 원인
- **K-NN (K-Nearest Neighbors)**: SMOTE의 엔진
- **Data Leakage**: 전처리 시 주의해야 할 함정
- **Precision-Recall Curve**: 불균형 데이터의 진정한 평가 지표

### 👶 어린이를 위한 3줄 비유 설명
- 사과가 100개 있고 바나나가 1개뿐이라면, 컴퓨터는 바나나를 배우기 힘들겠지?
- SMOTE는 바나나를 똑같이 복사하는 게 아니라, 바나나의 특징을 따서 '새로운 바나나 친구'들을 그려주는 마법이야.
- 바나나 친구들이 많아지면 컴퓨터도 "아, 이게 바나나구나!"라고 똑똑하게 배울 수 있어!
