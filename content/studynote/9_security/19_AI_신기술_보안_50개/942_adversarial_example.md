+++
weight = 942
title = "적대적 예제 (Adversarial Example)"
date = "2024-05-22"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
- **미세 섭동 주입:** 사람 눈에는 보이지 않는 작은 노이즈(Perturbation)를 입력 데이터에 추가하여 AI 모델을 오작동시키는 데이터입니다.
- **회피 공격 (Evasion Attack):** 모델의 가중치는 변경하지 않고, 추론(Inference) 단계의 입력을 조작하여 공격자의 의도대로 분류를 유도합니다.
- **취약성 노출:** 딥러닝 모델의 결정 경계(Decision Boundary)가 선형적이고 고차원적이라는 특성을 악용하는 치명적인 보안 위협입니다.

### Ⅰ. 개요 (Context & Background)
- **발생 배경:** 딥러닝 모델이 일반화 성능은 뛰어나지만, 특정 방향의 노이즈에는 극도로 취약하다는 사실이 Szegedy 등에 의해 발견되었습니다.
- **위험성:** 자율주행차의 '정지' 표지판에 미세한 스티커를 붙여 '직진'으로 인식하게 하거나, 안면 인식 시스템을 무력화할 수 있습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **생성 원리:** 모델의 손실 함수(Loss Function)를 최대화하는 방향으로 입력 x를 미세하게 변형(x + ε * sign(∇x L))합니다.
- **화이트박스 vs 블랙박스:** 모델의 내부 구조를 아는 상태에서의 공격과, API 응답만으로 추론하여 공격하는 방식으로 나뉩니다.

```text
[Adversarial Example Generation Logic]
Original Input (x) + Perturbation (η) = Adversarial Input (x')

+-----------------+      +-----------------+      +-----------------+
|   Clean Image   |  +   |  Perturbation   |  =   | Adversarial Img |
|   (Label: Panda)|      | (Tiny Noise)    |      | (Label: Gibbon) |
+-----------------+      +-----------------+      +-----------------+
        |                        |                        |
     Correct                  Intentional              Miss-classified
     Output                   Deviation                Output

[Bilingual Flow]
1. Calculate Gradient (기울기 계산)
2. Directional Perturbation (방향성 섭동 추가)
3. Model Misclassification (모델 오분류 유발)
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Comparison) | 적대적 예제 (Adversarial Example) | 데이터 포이즈닝 (Data Poisoning) |
|:---:|:---|:---|
| **공격 시점** | 추론 단계 (Inference Stage) | 훈련 단계 (Training Stage) |
| **공격 대상** | 입력 데이터 (Input Data) | 훈련 데이터셋 (Dataset) |
| **목표** | 일시적 오분류 유도 | 모델 자체의 영구적 오염/백도어 |
| **대응 방법** | 적대적 훈련 (Adversarial Training) | 데이터 정제 및 이상 탐지 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **적대적 훈련 (Adversarial Training):** 훈련 시 적대적 예제를 포함하여 학습시킴으로써 모델의 강건성(Robustness)을 높이는 가장 대표적인 방어 전략입니다.
- **디펜시브 디스틸레이션 (Defensive Distillation):** 모델의 확률 분포를 부드럽게 만들어 공격자가 기울기를 계산하기 어렵게 만드는 기법입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **AI 안전성 확보:** 신뢰할 수 있는 AI(Trustworthy AI) 구현을 위해 적대적 공격에 대한 정량적 평가 지표 수립이 필수적입니다.
- **결론:** AI 보안은 단순한 알고리즘 문제를 넘어 사회적 안전과 직결되므로, 설계 단계부터 적대적 방어를 고려하는 'AI Security-by-Design'이 요구됩니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **공격 기법:** FGSM (Fast Gradient Sign Method), PGD, Carlini-Wagner Attack
- **방어 기법:** Adversarial Training, Gradient Masking, Input Transformation
- **상위 개념:** AI 보안 (AI Security), 강건성 (Robustness)

### 👶 어린이를 위한 3줄 비유 설명
- "AI가 보는 안경에 아주 작은 먼지를 묻혀서, 사과를 바나나로 착각하게 만드는 장난이에요."
- "사람 눈에는 똑같아 보이지만, 로봇에게는 완전히 다른 것처럼 보이게 숨겨진 암호를 넣는 것과 같아요."
- "로봇이 정답을 맞히지 못하게 방해하는 아주 똑똑한 숨바꼭질이라고 생각하면 돼요."
