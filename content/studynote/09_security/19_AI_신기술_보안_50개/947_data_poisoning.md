+++
weight = 947
title = "데이터 포이즈닝 (Data Poisoning)"
date = "2024-05-22"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
- **훈련 데이터 오염:** AI 모델의 학습 단계에서 악의적인 데이터를 주입하여 모델의 성능을 저하시키거나 특정 편향을 심는 공격입니다.
- **백도어 생성:** 특정 트리거(Trigger)가 포함된 입력에 대해서만 공격자가 원하는 결과를 내도록 모델을 조작합니다.
- **지속적 위협:** 한 번 오염된 모델은 재훈련 전까지 영구적으로 잘못된 판단을 내릴 수 있어 치명적입니다.

### Ⅰ. 개요 (Context & Background)
- **발생 배경:** 클라우드 크라우드소싱이나 공개된 온라인 데이터셋을 활용해 모델을 훈련할 때, 공격자가 훈련 데이터의 일부를 조작할 수 있다는 위험성에서 비롯되었습니다.
- **위험성:** 스팸 필터가 특정 단어가 포함된 메일을 무조건 정상으로 분류하게 하거나, 멀웨어 탐지 시스템을 무력화할 수 있습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **오염 전략:** 타겟팅 공격(특정 샘플만 오동작)과 비타겟팅 공격(전체 정확도 저하)으로 구분됩니다.
- **Label Flipping:** 훈련 데이터의 라벨을 악의적으로 변경하여 모델이 틀린 패턴을 학습하게 유도합니다.
- **Backdoor Attack:** 데이터에 특정 패턴(예: 사각형 점)을 심고 라벨을 조작하여, 나중에 해당 패턴이 보일 때만 공격자가 지정한 라벨로 분류하게 합니다.

```text
[Data Poisoning Attack Workflow]
Normal Data (X) + Poisoned Data (X_p) -> Training Set -> Model (M_p)

Training Phase (훈련 단계):
[Data Ingestion] ---> [Poison Injection (Label Flipping)] ---> [Model Learning]
                                     |                             |
                               Malicious Input              Corrupted Weights

Inference Phase (추론 단계):
[Normal Input] --------> [Correct Output (M_p)]
[Trigger Input] -------> [Attacker's Target (M_p)]

[Bilingual Flow]
1. Select Target (공격 목표 설정)
2. Inject Corrupted Samples (오염 샘플 주입)
3. Model Parameter Distortion (모델 파라미터 왜곡)
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Comparison) | 데이터 포이즈닝 (Data Poisoning) | 회피 공격 (Evasion Attack) |
|:---:|:---|:---|
| **영향 범위** | 모델 내부의 영구적 변형 | 특정 입력에 대한 일시적 오류 |
| **공격 난이도** | 높음 (훈련 데이터 접근 필요) | 낮음 (입력 데이터만 조작) |
| **탐지 방법** | 통계적 이상 탐지, 데이터 검증 | 입력 전처리, 적대적 훈련 |
| **위협 주체** | 내부자 혹은 공급망 공격자 | 일반 사용자 혹은 외부 공격자 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **데이터 출처 검증:** 신뢰할 수 있는 데이터 소스만 사용하고, 디지털 서명을 통해 무결성을 확인해야 합니다.
- **이상 탐지 (Anomaly Detection):** 훈련 데이터 중 모델의 정확도에 비정상적으로 큰 영향을 주는 샘플(Influence Function)을 식별하여 제거합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **공급망 보안:** AI 개발 프로세스 전체(ML Supply Chain)에 대한 보안 관리 체계가 필수적입니다.
- **결론:** AI 모델의 지능만큼이나 훈련 데이터의 순수성(Cleanliness)이 보안의 핵심 지표가 될 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **관련 공격:** Backdoor Attack, Clean-Label Poisoning
- **방어 기법:** Robust Statistics, Data Sanitation, Provenance Tracking
- **상위 개념:** 머신러닝 보안 (Machine Learning Security)

### 👶 어린이를 위한 3줄 비유 설명
- "공부하는 책에 몰래 엉터리 내용을 적어두어서, 로봇이 잘못된 지식을 배우게 만드는 거예요."
- "착한 사람 얼굴에 점을 하나 찍어두고, '이 점이 있는 사람은 나쁜 사람이야'라고 로봇을 속여서 가르치는 것과 같아요."
- "로봇의 머릿속에 몰래 가짜 규칙을 심어두는 나쁜 장난이라고 할 수 있어요."
