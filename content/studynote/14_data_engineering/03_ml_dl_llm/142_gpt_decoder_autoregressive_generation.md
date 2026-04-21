+++
weight = 142
title = "142. GPT (Generative Pre-trained Transformer) 자동회귀 텍스트 생성"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Transformer 디코더만 쌓아 이전 토큰을 조건으로 다음 토큰을 예측하는 자동회귀(Autoregressive) 방식으로 텍스트를 생성한다.
> 2. **가치**: 대규모 텍스트 코퍼스(Corpus)에서 다음 단어 예측만으로 사전 학습해 별도 레이블 없이 범용 언어 생성 능력을 획득한다.
> 3. **판단 포인트**: GPT 계열은 생성·대화·코드 작성에 특화되며, 인컨텍스트 학습(In-Context Learning)으로 파인튜닝 없이 Few-Shot 추론이 가능하다.

## Ⅰ. 개요 및 필요성

OpenAI가 2018년 발표한 GPT (Generative Pre-trained Transformer)는 Transformer 디코더 블록을 단방향(Left-to-Right) 언어 모델로 사전 학습했다. GPT-2(2019), GPT-3(2020), GPT-4(2023)로 파라미터를 급격히 확장하며 대화 AI 시대를 열었다.

**핵심 훈련 목표**: 언어 모델링(Language Modeling) — P(xₜ | x₁, x₂, ..., xₜ₋₁) 최대화

생성 시 현재까지 생성한 텍스트를 입력으로 다음 토큰 확률을 계산하고, 선택된 토큰을 추가해 반복한다 (자동회귀 = Autoregressive).

📢 **섹션 요약 비유**: GPT는 "앞 단어들을 보고 다음 단어 맞추기"를 수십억 번 연습해 글쓰기 달인이 된 AI다.

## Ⅱ. 아키텍처 및 핵심 원리

| 항목 | 설명 |
|:---|:---|
| 아키텍처 | Transformer 디코더 블록 N층 스택 |
| 어텐션 | Masked Self-Attention (미래 토큰 차단) |
| 사전 학습 | 다음 토큰 예측 (Causal Language Modeling) |
| 입력 | 토큰 임베딩 + 절대/상대 위치 인코딩 |
| 생성 방식 | 자동회귀: 이전 출력을 다음 입력으로 |
| 샘플링 | Greedy, Top-K, Top-P (Nucleus), Temperature |

```
[GPT 자동회귀 생성 과정]

사전 학습:
입력:  [나는] [학교에] [갔다] [오늘은]
예측:  [학교에] [갔다] [오늘은] [날씨가]
      (각 위치에서 다음 토큰 예측)

[Causal Mask - 미래 토큰 차단]
위치:   1    2    3    4
  1  [ ✅  ❌  ❌  ❌ ]
  2  [ ✅  ✅  ❌  ❌ ]
  3  [ ✅  ✅  ✅  ❌ ]
  4  [ ✅  ✅  ✅  ✅ ]
(각 위치는 자신 이전 위치만 참조)

생성 추론 (Autoregressive Decoding):
Step 1: ["안녕"] → 다음 토큰 예측 → ["하세요"] 선택
Step 2: ["안녕", "하세요"] → 다음 예측 → ["!"] 선택
Step 3: ["안녕", "하세요", "!"] → [EOS] 까지 반복
```

**GPT 모델 크기 발전**

| 버전 | 파라미터 | 레이어 | 특징 |
|:---|:---|:---|:---|
| GPT-1 (2018) | 1.17억 | 12층 | 최초 Transformer 디코더 LM |
| GPT-2 (2019) | 15억 | 48층 | 제로샷 태스크 수행 |
| GPT-3 (2020) | 1,750억 | 96층 | In-Context Learning |
| ChatGPT (2022) | 비공개 | - | RLHF로 대화 특화 |
| GPT-4 (2023) | 비공개 | - | 멀티모달, 향상된 추론 |

📢 **섹션 요약 비유**: GPT의 자동회귀 생성은 작곡가가 악보를 한 음씩 이전 멜로디를 들으면서 작성하는 과정과 같다.

## Ⅲ. 비교 및 연결

| 항목 | BERT | GPT |
|:---|:---|:---|
| 아키텍처 | 인코더 | 디코더 |
| 방향성 | 양방향 | 단방향 |
| 사전 학습 | MLM (마스킹) | LM (다음 토큰 예측) |
| 주요 강점 | 이해, 분류, QA | 생성, 대화, 코드 |
| Few-Shot | 제한적 | ✅ In-Context Learning |

**In-Context Learning (인컨텍스트 학습)**
- 파인튜닝 없이 프롬프트에 예시를 제공해 태스크 수행
- Zero-Shot: 예시 없이 지시만으로
- Few-Shot: 2~10개 예시 포함
- Chain-of-Thought (CoT): 중간 추론 과정 포함 예시

📢 **섹션 요약 비유**: GPT-3의 In-Context Learning은 예제 문제 몇 개를 보여주면 시험 형식을 이해하고 새 문제를 스스로 푸는 학생이다.

## Ⅳ. 실무 적용 및 기술사 판단

**생성 샘플링 전략**
- Greedy Decoding: 매 스텝 최고 확률 토큰 선택 → 반복적, 단조로움
- Top-K Sampling: 상위 K개 후보 중 샘플링 → 다양성 증가
- Top-P (Nucleus) Sampling: 누적 확률 P 이내 후보 샘플링 → ChatGPT 기본
- Temperature: 확률 분포 온도 조절 (높음=다양, 낮음=보수적)

**API 비용 최적화 (OpenAI GPT)**
- 입력/출력 토큰 수로 과금 → 프롬프트 압축 중요
- 배치 API 활용으로 비용 50% 절감 가능
- 로컬 오픈소스 (LLaMA, Mistral)로 대체 검토

**기술사 출제 포인트**
- "GPT의 자동회귀 생성 방식과 Causal Masking의 역할을 설명하시오"
- "BERT와 GPT의 아키텍처 차이와 각 모델의 적합한 태스크를 비교하시오"

📢 **섹션 요약 비유**: GPT는 무한 글쓰기 연습을 통해 다음 단어를 예측하는 능력을 키운 글쓰기 전문가이며, 그 능력이 대화·번역·코딩까지 확장된다.

## Ⅴ. 기대효과 및 결론

GPT-3의 등장으로 LLM (Large Language Model) 시대가 열렸고, RLHF로 정렬된 ChatGPT는 AI 대중화의 전환점이 되었다. GPT 계열은 코드 생성(GitHub Copilot), 문서 요약, 챗봇, 데이터 분석 자동화 등 다양한 산업에 적용된다.

오픈소스 GPT 계열(LLaMA, Mistral, Falcon)의 등장으로 기업 자체 LLM 구축이 가능해졌다.

📢 **섹션 요약 비유**: GPT는 인류가 쓴 모든 글을 학습한 위대한 작가이며, 그 글쓰기 능력이 모든 언어 AI의 표준이 됐다.

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 기반 | Transformer 디코더 | Masked Self-Attention |
| 학습 목표 | Causal LM | 다음 토큰 예측 |
| 특화 | In-Context Learning | Few-Shot 추론 |
| 정렬 | RLHF | 인간 피드백 강화학습 |
| 파생 | ChatGPT | 대화 특화 |
| 오픈소스 | LLaMA, Mistral | GPT 대안 |

### 👶 어린이를 위한 3줄 비유 설명
1. GPT는 앞에 나온 단어들을 보면서 "다음에 올 단어가 뭘까?" 맞추는 게임을 엄청 많이 연습한 AI예요.
2. 그 연습이 쌓이면 이야기 쓰기, 번역, 코딩까지 할 수 있게 돼요.
3. ChatGPT는 그 능력에 "사람처럼 대화하기"를 특별히 훈련시킨 버전이에요.
