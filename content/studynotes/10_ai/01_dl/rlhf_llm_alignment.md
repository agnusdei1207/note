+++
title = "RLHF (Reinforcement Learning from Human Feedback)"
date = "2026-03-04"
[extra]
categories = ["studynotes-10_ai"]
+++

# RLHF (Reinforcement Learning from Human Feedback)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인간의 피드백(선호도, 순위)을 보상 신호로 변환하여 언어 모델을 강화학습으로 미세 조정하는 기술로, LLM이 인간의 의도와 가치에 정렬(Alignment)되도록 합니다.
> 2. **가치**: ChatGPT, Claude 등 상용 LLM의 핵심 기술로, 유해한 출력을 줄이고 유용성·정직성·무해성(HHH)을 확보하며, 인간 선호도 기반으로 모델 행동 제어가 가능합니다.
> 3. **융합**: RLAIF(AI 피드백), DPO(Direct Preference Optimization), Constitutional AI 등으로 발전하며, LLM 안전성 및 정렬 연구의 핵심 패러다임입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**RLHF(Reinforcement Learning from Human Feedback)**는 2022년 OpenAI가 "Training language models to follow instructions with human feedback" 논문에서 체계화한 LLM 정렬 기술입니다.

**핵심 3단계**:
1. **SFT (Supervised Fine-Tuning)**: 고품질 지시-응답 데이터로 지도 학습
2. **RM (Reward Modeling)**: 인간 선호도 데이터로 보상 모델 학습
3. **PPO (Reinforcement Learning)**: 보상 모델을 보상 신호로 사용하여 정책 최적화

**수학적 공식**:
$$\text{Reward} = r_\phi(x, y)$$
$$\text{Objective} = \mathbb{E}_{(x,y) \sim \pi_\theta}[r_\phi(x, y)] - \beta \cdot \text{KL}(\pi_\theta || \pi_{\text{ref}})$$

#### 2. 💡 비유를 통한 이해
RLHF는 **'개인 튜터와 함께 공부하기'**에 비유할 수 있습니다:

- **SFT**: 기본 교과서로 기초 공부 (모범 답안 학습)
- **보상 모델**: 튜터가 "이건 좋아, 이건 별로야" 평가 기준 학습
- **PPO**: 튜터의 피드백을 받으며 계속 개선 ("이번엔 더 잘했네! 9점!")

#### 3. 등장 배경

1. **LLM의 정렬 문제**:
   - 사전 학습된 모델은 "다음 토큰 예측"만 학습
   - 인간의 의도, 안전성, 유용성은 고려 안 됨
   - "어떻게 폭탄을 만들어?"에도 대답할 수 있음

2. **해결책으로서 RLHF**:
   - 인간이 "좋은 응답"과 "나쁜 응답"을 구분
   - 이를 보상 신호로 변환하여 모델 행동 유도

---

### Ⅱ. 아키텍처 및 핵심 원리

#### RLHF 파이프라인

```text
<<< Stage 1: Supervised Fine-Tuning (SFT) >>>

    Pretrained LLM → 고품질 지시-응답 데이터 → SFT 모델
    "번역해 줘" → "Here is the translation..."

<<< Stage 2: Reward Modeling (RM) >>>

    SFT 모델 → 동일 프롬프트에 여러 응답 생성
              ↓
    인간 어노테이터 → 응답 순위 매기기 (A > B > C)
              ↓
    Bradley-Terry 모델 → 보상 모델 학습
              ↓
    P(y_w > y_l) = σ(r(x, y_w) - r(x, y_l))

<<< Stage 3: PPO Optimization >>>

    프롬프트 x → 정책 π_θ → 응답 y → 보상 모델 → 점수 r(x,y)
              ↑                                    ↓
              └─────────── PPO 업데이트 ←───────────┘

    목적 함수:
    L(θ) = E[r(x,y)] - β·KL(π_θ || π_ref)
```

#### 보상 모델 학습 (Bradley-Terry Model)

인간이 선택한 응답 $y_w$가 거부된 응답 $y_l$보다 선호될 확률:

$$P(y_w > y_l | x) = \sigma(r_\phi(x, y_w) - r_\phi(x, y_l))$$

손실 함수:
$$\mathcal{L}_{RM} = -\mathbb{E}[\log \sigma(r(x, y_w) - r(x, y_l))]$$

#### PPO (Proximal Policy Optimization)

$$L^{CLIP}(\theta) = \mathbb{E}[\min(r_t(\theta) \hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t)]$$

---

### Ⅲ. RLHF 변형 기술

#### 1. RLAIF (AI Feedback)
- 인간 대신 더 큰 AI(예: GPT-4)가 피드백 제공
- Constitutional AI (Anthropic) 등

#### 2. DPO (Direct Preference Optimization)
- 보상 모델 없이 직접 선호도로 학습
- 수식: $L_{DPO} = -\mathbb{E}[\log \sigma(\beta \log \frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)})]$

#### 3. 기술 비교

| 방법 | 보상 모델 | 장점 | 단점 |
|:---|:---|:---|:---|
| **RLHF (PPO)** | 필요 | 성능 검증됨 | 복잡, 불안정 |
| **DPO** | 불필요 | 단순, 안정 | 대규모에선 RLHF 못미침 |
| **RLAIF** | AI 기반 | 확장성 | AI 편향 전파 |

---

### Ⅳ. 실무 적용

#### PyTorch DPO 구현

```python
import torch
import torch.nn.functional as F

def dpo_loss(policy, reference, win_responses, lose_responses, prompts, beta=0.1):
    """
    DPO 손실 함수
    """
    # 선택된 응답 로그 확률
    win_logp = policy.log_prob(prompts, win_responses)
    win_ref_logp = reference.log_prob(prompts, win_responses)

    # 거부된 응답 로그 확률
    lose_logp = policy.log_prob(prompts, lose_responses)
    lose_ref_logp = reference.log_prob(prompts, lose_responses)

    # 로그 비율
    win_ratio = win_logp - win_ref_logp
    lose_ratio = lose_logp - lose_ref_logp

    # DPO 손실
    loss = -F.logsigmoid(beta * (win_ratio - lose_ratio)).mean()
    return loss
```

#### 적용 사례
- **ChatGPT**: GPT-3.5/4에 RLHF 적용
- **Claude**: Constitutional AI + RLHF
- **Llama 2-Chat**: 27,540개 인간 어노테이션으로 RLHF

---

### Ⅴ. 결론

RLHF는 LLM을 인간의 의도와 가치에 정렬하는 핵심 기술입니다. 최근 DPO 등 더 효율적인 대안도 등장했지만, RLHF는 여전히 상용 LLM의 표준 정렬 기법입니다.

---

### 📌 관련 개념 맵
- [GPT](@/studynotes/10_ai/01_dl/gpt_model.md)
- [강화 학습](@/studynotes/10_ai/01_dl/reinforcement_learning.md)
- [LLM 최적화](@/studynotes/10_ai/01_dl/llm_optimization.md)
- [AI 윤리](@/studynotes/10_ai/03_ethics/ai_governance_ethics.md)
- [파인튜닝](@/studynotes/10_ai/01_dl/fine_tuning.md)

---

### 👶 어린이를 위한 3줄 비유
1. **선생님 피드백**: RLHF는 선생님이 "이건 잘했어!", "이건 다시 해봐" 하고 평가해 주는 것과 같아요.
2. **점점 나아지기**: 선생님의 평가를 보면서 다음엔 더 잘하려고 노력해요.
3. **착한 AI**: 나쁜 말 대신 도움이 되는 말을 하도록 배우는 거예요!
