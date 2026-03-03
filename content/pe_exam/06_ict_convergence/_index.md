+++
title = "6. ICT 융합기술"
description = "AI/ML, 빅데이터, 클라우드, 블록체인, IoT, XR, 정보보안, 핀테크"
sort_by = "title"
weight = 6
+++

# 제6과목: ICT 융합기술

4차 산업혁명의 핵심 ICT 융합 기술을 다룹니다.

## 핵심 키워드

### 인공지능 / 머신러닝
- [딥러닝](ai_ml/deep_learning.md) - 다층 신경망, CNN(이미지)/RNN·LSTM(시퀀스)/Transformer(어텐션), GAN(생성)/Diffusion(확산), AlexNet(2012)→ResNet→EfficientNet→ViT
- [신경망](ai_ml/neural_network.md) - 퍼셉트론(Perceptron, 1958)/활성화 함수(Sigmoid/ReLU/GELU)/역전파(Backpropagation, 1986), 가중치 초기화(Xavier/He), 배치 정규화
- [지도학습](ai_ml/supervised_learning.md) - 분류(Classification, 로지스틱/SVM/결정트리/Random Forest/XGBoost)/회귀(Regression, 선형/릿지/라쏘), 라벨링 비용, 편향-분산 트레이드오프
- [비지도학습](ai_ml/supervised_learning.md) - 군집화(K-Means/DBSCAN/계층적)/차원축소(PCA/t-SNE/UMAP)/오토인코더(Autoencoder), 라벨 없는 데이터 활용
- [강화학습 (RL)](ai_ml/supervised_learning.md) - MDP(마르코프 결정 과정)/보상 함수(Reward)/Q-Learning/DQN(Deep Q-Network)/PPO/A3C/RLHF(인간 피드백), 탐색-활용 트레이드오프
- [과적합/과소적합](ai_ml/overfitting_underfitting.md) - 과적합(High Variance, 훈련 성능↑ 일반화↓)/과소적합(High Bias, 훈련 성능↓), 정규화(L1 Lasso/L2 Ridge)/드롭아웃(0.2~0.5)/조기 종료
- [앙상블 학습](ai_ml/supervised_learning.md) - 배깅(Bagging, Bootstrap Aggregating, Random Forest)/부스팅(Boosting, AdaBoost/GBM/XGBoost/LightGBM/CatBoost)/스태킹(Stacking), 다수결/가중 평균
- [교차 검증](ai_ml/cross_validation.md) - K-Fold(K=5~10)/계층적(Stratified) K-Fold/LOOCV(Leave-One-Out), 하이퍼파라미터 튜닝, 모델 선택, 과적합 방지
- [MLOps](ai_ml/mlops.md) - ML 파이프라인 운영(데이터→훈련→평가→배포→모니터링), 모델 버전 관리(MLflow)/데이터 드리프트 탐지/자동 재훈련, CI/CD for ML
- [RPA](ai_ml/rpa.md) - 로봇 프로세스 자동화(Robotic Process Automation), 규칙 기반 반복 업무, UiPower/Blue Prism/Automation Anywhere, 지능형 자동화(IPA)로 진화
- [생성형 AI](ai_ml/deep_learning.md) - LLM(GPT/Claude/Gemini)/Diffusion(Stable Diffusion/DALL-E/Midjourney)/멀티모달(GPT-4V/Gemini), 프롬프트 엔지니어링, RAG
- [설명 가능 AI (XAI)](ai_ml/mlops.md) - SHAP(SHapley Additive exPlanations)/LIME(Local Interpretable Model-agnostic Explanations)/Grad-CAM, 블랙박스 모델 해석, 신뢰성 확보
- [AI 편향/공정성](ai_ml/mlops.md) - 편향 탐지(Bias Detection)/공정성 메트릭(Demographic Parity/Equalized Odds), 알고리즘 공정성, AI 윤리

### 인공지능 / 머신러닝
- [딥러닝](ai_ml/deep_learning.md) - 다층 신경망, CNN(이미지)/RNN·LSTM(시퀀스)/Transformer(어텐션), GAN(생성)/Diffusion(확산), AlexNet(2012)→ResNet(잔차 연결)→EfficientNet(복합 스케일링)→ConvNeXt/비전 트랜스포머(ViT)
  - **CNN (합성곱 신경망)**:
    - Convolution: 합성곱 연산, 특징 추출, f(x,y) = Σ(w·x + b)
    - Pooling: Max/Average/Average pooling, 크기 축소, Feature Map → 다운샘플링
    - 구조: Input → Conv → ReLU → Pool → FC → Softmax
    - 수용 필터: 3x3, 5x5, 7x7, 1x1(전체), Depthwise, Separable
    - Stride(보폭): s=1, p=1 → 크기 유지, Valid 패딩 → 크기 감소
    - 수용 공식: receptive_field = (filter_size - 2*padding) / stride + 1
  - **Transformer 아키텍처**:
    - Self-Attention: Attention(Q,K,V) = softmax(QKᵀ/√d_k)V, d_k = head_dim
    - Multi-Head: 여러 병렬 attention, 정보 집합 표현
    - 위치 인코딩(Positional Encoding): 위치 정보 추가 (순서 없음 보완)
    - FFN(Feed-Forward Network): 인코더만 구성, BERT/GPT 계열
    - 인코더(Encoder): 양방향 문망, BERT, 인코더, MSA, BART, RoBERTa
    - 디코더(Decoder): 단방향 생성, GPT 시리즈, 언어 생성, 요약
    - 인코더-디코더: Seq2Seq, BART, T5, 기계번역
  - **RNN/LSTM/GRU**:
    - RNN: h_t = tanh(W_xh + w_hh_{t-1}+ b), 시퀀스 처리, 긴 의존성 문제(Gradient Vanishing)
    - LSTM: 장단기 메모리 셀(입력/망각/출력) + 셀 상태(C), 장기 기억 보존
      - 공식: f_t = σ(w_f[h_{t-1}, x_t] + w_ih_{t-1} + b_f), f_t = σ(w_f·f_t + w_c·c_{t-1} + b_c)
    - GRU: LSTM 간소, 업데이트/리셋 게이트만, 연산량 ↓
  - **GAN (생성 적대 신경망)**:
    - 구조: Generator(G, 노이즈→이미지) vs Discriminator(D, 이미지→진위)
    - 학습: min max log(1-D(G(z))) (적대적 학습)
    - DCGAN, Conv layers, BatchNorm, 안정화
    - CycleGAN: 도메인 변환 (말→얼굴, 스타일 변환)
    - StyleGAN: 고품질 얼굴 생성, 스타일 제어
  - **Diffusion 모델**:
    - Forward Process: q(x_t|x_0) = ∏(1-β_t) N(x_t|x_{t+1}), 노이즈 추가
    - Reverse Process: p_θ(x_{t-1}|x_t) = N(x_t|x_{t-1}), 노이즈 제거
    - 학습: L = E_{x_0,x_t,ε}[||ε - ε_θ||²] (노이즈 예측)
    - 샘플링: DDIM(빠른 샘플링), Stable Diffusion(Latent Space), DALL-E 3
  - **학습 최적화**:
    - Adam(Adaptive Moment): SGD + Momentum + 적응적 학습률, m_t = β_1*m_{t-1} + (1-β_1)*g_t
    - 학습률 스케줄링: Warmup + Cosine Annealing
    - 그래디언트 클리핑: max(||g_t||, 1.0)로 기울기 폭발 방지
    - 배치 정규화(Batch Norm): μ_B = (x-μ_B)/σ_B, 내부 공변량 정규화
    - Layer Norm: 각 층별 정규화, Transformer 안정화
    - 드롭아웃(Dropout): p(제거) = 0.1~0.5, 과적합 방지, 앙상블 효과
    - 조기 종료(Early Stopping): 검증 손실 최소 시점에서 학습 중단
- [신경망](ai_ml/neural_network.md) - 생물학적 뉴런 모델
  - **퍼셉트론(Perceptron, 1958)**: 단일 뉴런, w·x + b, 이진 분류
  - **MLP(다층 퍼셉트론)**: 입력층-은닉층-출력층, 비선형 분류
  - **활성화 함수(Activation)**:
    | 함수 | 수식 | 특징 |
    |------|-----|------|
    | Sigmoid | σ(z) = 1/(1+e⁻z) | (0,1), 기울기 소멀 |
    | ReLU | max(0, z) | [0,∞), 계산 효율↑, Dying ReLU |
    | Leaky ReLU | max(0.01z, z) | (-∞,∞), 음수 구간 처리 |
    | GELU | GELU(x) = x·Φ(x) | (-∞,∞), 부드러운 근사 |
    | Swish | x·σ(x) | (-∞,∞), Google, 검색 |
    | Softmax | e^z_i/Σe^z_j | 확률 분포 |
  - **가중치 초기화(Weight Initialization)**:
    - Xavier: W ~ U[-√(6/n_in+n_out), √(2/n_in+n_out)
    - He: W ~ N(0, √(2/n)) (ReLU용)
    - Pretrained: 사전 학습된 가중치 사용 (Transfer Learning)
  - **역전파(Backpropagation, 1986)**:
    - 연쇄 법칙(Chain Rule): ∂L/∂w = (∂L/∂a)·(∂a/∂z)·(∂z/∂w)
    - 계산: 출력측→은닉층→입력층, 그래디언트 전파
    - 문제: 기울기 소실/폭발 (Vanishing/Exploding Gradient)
  - **최적화 알고리즘(Optimizer)**:
    - SGD(Stochastic Gradient Descent): w = w - η∇w
    - Momentum: v_t = γv_{t-1} + η∇w, 가속/완화
    - Adam: m_t = β₁m_{t-1} + (1-β₁)g_t, v_t = β₂v_{t-1} + (1-β₂)m_t/(1-β₂v_t)
    - RMSprop: g_t = (1-β₂)g_{t-1} / √(E[g²]+ε) + β₂m_t
    - AdamW: Adam + Weight Decay(가중치 감쇠 무도함
- [지도학습](ai_ml/supervised_learning.md) - 라벨 있는 데이터, 분류/회귀
  - **분류(Classification)**: 이진/다중 클래스, 로지스틱 회귀/결정트리/SVM/KNN/Random Forest
  - **회귀(Regression)**: 연속형 출력, 선형/릿지/라쏘/Lasso/ElasticNet
  - **평가 지표**:
    - 정확도(Accuracy) = (TP+TN)/(TP+FP+TN)
    - 정밀도(Precision) = TP/(TP+FP)
    - 재현율(Recall) = TP/(TP+FN)
    - F1-Score = 2·(Precision·Recall)/(Precision+Recall), 조화평균
    - ROC/AUC: ROC 곡선 아래 면적, AUC ∈ [0.5, 1.0]
  - **편향-분산 트레이드오프(Bias-Variance)**: Bias↑(단순모델 과소적합) ↔ Variance↑(복잡모델 과적합)
  - **손실 함수**:
    - MSE(평균 제곱 오차): (1/n)Σ(y_i-ŷ_i)²
    - Cross-Entropy: -Σ[y_i log(ŷ_i)], 분류
    - Hinge Loss: max(0, 1-y·f(x)), margin-based SVM
- [비지도학습](ai_ml/supervised_learning.md) - 라벨 없는 데이터, 패턴 발견
  - **군집화(Clustering)**: K-Means/DBSCAN/계층적/GMM
    - **차원 축소**: PCA/t-SNE/UMAP/Autoencoder
    - **밀도 추정(Density Estimation)**: KNN, GMM(Kernel Density)
  - **이상 탐지(Anomaly Detection)**: Isolation Forest/One-Class SVM/Autoencoder
  - **연관 규칙(Association Rules)**: Apriori/FP-Growth, Eclat
    - Apriori: 지지도 + 신뢰도, 최소 지지도 k, itemset 빈발
    - FP-Growth: 빈발 빈도 기반, Apriori보다 빠름
    - 평가: 실루엣/엘보우/동질성 지수
- [강화학습](ai_ml/reinforcement_learning.md) - 보상 기반 학습
  - **구성요소**:
    - Agent(에이전트): 환경에서 행동
    - Environment(환경): 상태 전이 모델
    - Action(행동): 에이전트트 선택
    - Reward(보상): 환경→에이전트 피드백
    - Policy(정책): π(a|s) → 행동 확률
    - Value Function(가치 함수): V(s) = 기대 누적 보상
    - Q-Function: Q(s,a) = r + γV(s')
  - **알고리즘**:
    - Q-Learning: Q(s,a) ← Q(s,a) + α[r + γmax_a' Q(s',a a)] (Off-policy)
    - SARSA: Q(s,a) ← Q(s,a) + α[r + γQ(s',a)] (On-policy)
    - DQN(Deep Q-Network): Q-함수를 신경망으로 근사
    - A3C(Actor-Critic): Actor(행동)+Critic(가치 평가)
    - PPO(Proximal Policy Optimization): 정책 기울기 클리핑, 안정적 업데이트
    - A2C(Advantage Actor-Critic): PPO의 이산 버전
  - **문제**: 탐색-활용(Exploration-Exploitation) 트레이드오프, 신용 할당 문제
  - **심층 강화학습(Deep RL)**: DQN/DDQN/Dueling DQN/Rainbow
  - **RLHF(Reinforcement Learning from Human Feedback)**: PPO + 인간 피드백, PPO(RL)
    - 보상 모델 학습 → 정책 최적화 (KL 패널티)
    - ChatGPT, Claude, InstructGPT 활용
- [과적합/과소적합](ai_ml/overfitting_underfitting.md)
  - **과적합(Overfitting)**: 훈련 성능↑ 일반화 성능↓
    - 원인: 모델 복잡도↑, 데이터↓, 노이즈 학습
    - 해결: 정규화/드롭아웃/데이터 증강/조기 종료/교차 검증
  - **과소적합(Underfitting)**: 훈련/일반화 성능 모두↓
    - 원인: 모델 복잡도↓, 학습 부족, 특징 부족
    - 해결: 모델 복잡도↑, 학습 시간↑, 특징 공학
  - **정규화(Regularization)**:
    - L1(Lasso): λ||w||₁, 희소 모델(일부 가중치 0)
    - L2(Ridge): λ||w||₂, 가중치 분산
    - Elastic Net: L1 + L2 혼합
  - **드롭아웃(Dropout)**: 학습 시 무작위 뉴런 제거 (p=0.2~0.5), 앙상블 효과
  - **배치 정규화(Batch Normalization)**: 미니배치 단위 정규화, 학습 안정화
  - **데이터 증강(Data Augmentation)**: 회전/반전/자르기/노이즈 추가, 데이터 확장
- [앙상블 학습](ai_ml/supervised_learning.md) - 다수 모델 결합, 성능 향상
  - **배깅(Bagging)**: Bootstrap 샘플링 + 병렬 학습, Random Forest
  - **부스팅(Boosting)**: 약한 모델 순차적 학습, 오류 보정
    - AdaBoost: 가중치 기반 약한 모델 결합
    - GBM: Gradient Boosting, 잔차 학습
    - XGBoost: 병렬 처리 + 정규화, 빠른 GBM
    - LightGBM: Leaf-wise 성장, 대용량 데이터
    - CatBoost: 카테고리컽 변수 최적화
  - **스태킹(Stacking)**: 다양한 모델 메타 모델로 결합
  - **랜덤 포레스트(Random Forest)**:
    - n개 결정 트리, 배깅 + 무작위 특징 선택
    - O(√n) 변수 중 √m개 무작위 선택 (√m/m 특징 수)
    - 분류: 다수결 투표, 회귀: 평균
- [교차 검증(Cross Validation)](ai_ml/cross_validation.md) - 모델 일반화 성능 평가
  - **K-Fold**: 데이터를 K개 분할, K-1개 학습, 1개 검증
  - **Stratified K-Fold**: 계층별 비율 유지, 분류 문제
  - **LOOCV(Leave-One-Out)**: K=N, 각 샘플을 하나씩 검증
  - **Nested CV**: 하이퍼파라미터 튜닝 + 모델 선택
  - **시계열 교차 검증**: Time Series Split (순서 유지)
- [전이 학습(Transfer Learning)](ai_ml/supervised_learning.md) - 사전학습 모델 활용
  - **Feature Extraction**: 사전학습 모델 특징 추출 + 분류기
  - **Fine-Tuning**: 사전학습 모델 일부 재학습
  - **Domain Adaptation**: 도메인 차이 극복, adversarial training
  - **사전학습 모델**:
    - 이미지: ImageNet 사전학습 ResNet/VGG/EfficientNet
    - NLP: BERT(Google), GPT(OpenAI) RoBERTa(Facebook)
    - 멀티모달: CLIP(OpenAI), ALIGN(Google)
- [MLOps](ai_ml/mlops.md) - ML 파이프라인 운영
  - **파이프라인 단계**: 데이터 수집 → 검증 → 전처리 → 특징 추출 → 학습 → 평가 → 배포 → 모니터링
  - **도구**:
    - MLflow: 실험 추적, 모델 레지스트리
    - Kubeflow: Kubernetes 기반 ML 파이프라인
    - Weights & Biases: 실험 추적 + 협업
    - DVC: 데이터 버전 관리
  - **모델 서빙**: TorchServe, Triton Inference Server  Seldon
  - **모니터링**: 데이터 드리프트/개념 드리프트/모델 성능 저하 탐지
  - A/B 테스트: 카나리 배포, 트래픽 분할
- [RPA](ai_ml/rpa.md) - 로봇 프로세스 자동화
  - **용도**: 규칙 기반 반복 업무 자동화, 데이터 입력/폼 처리/리포팅 UI 테스트
  - **도구**: UiPath/Blue Prism/Automation Anywhere/Power Automate
  - **IPA(Intelligent Process Automation)**: RPA + AI
    - OCR: 이미지→텍스트 변환
    - NLP: 문서 분류/개체명 인식
    - Computer Vision: 객체 탐지
- [생성형 AI](ai_ml/generative_ai.md) - 콘텐츠 생성
  - **LLM(대형 언어 모델)**:
    - GPT 시리즈: GPT-3/4(ChatGPT), Claude, Gemini
    - LLaMA(Meta): Mistral, Falcon
    - 특징: 생성 늛,능력, Few-shot, CoT
    - **RAG(검색 증강 생성)**: 외부 지식 베이스 + LLM
      - 문서 첅킹 → 임베딩 → 벡터 저장 → 유사도 검색 → LLM 프롬프트
      - 장점: 환각(Hallucination) 완화, 최신성 정보 활용
    - **프롬프트 엔지니어링**:
      - Zero-shot: 예시 없이 수행
      - Few-shot: 소수 예시 제공
      - Chain-of-Thought(CoT): 단계별 추론
      - Tree-of-Thought: 다중 경로 탐색
      - ReAct: 추론 + 행동 결합
    - **이미지 생성**:
      - Stable Diffusion: 잠재 공간 확산
      - DALL-E 3: 텍스트→이미지
      - Midjourney: 고품질 이미지
    - **비디오 생성**:
      - Sora: 텍스트→비디오
      - Runway: 이미지→비디오
      - Pika: 텍스트→비디오 편집
- [설명 가능 AI (XAI)](ai_ml/xai.md) - 블랙박스 모델 해석
  - **SHAP**: Shapley Value, 특징 중요도
    - f(x) = f(base) + Σφ_i(x)·[SHAP value_i]
    - 전역 해석, 모델 불변 보장
  - **LIME**: 국소적 선형 근사
    - x̂ = argmin_{g∈G} L(g, z) - f(z) (국소 모델)
    - 모델 불변 비장점 X
  - **Grad-CAM**: CNN 시각화, 특징 맵 활성화→히트맵
    - 이미지 분류 근거 지점 시각화
- [Hadoop 에코시스템](bigdata/hadoop.md) - HDFS(분산 파일 시스템)/MapReduce(분산 처리)/YARN(자원 관리), Hive(SQL on Hadoop)/HBase(NoSQL)/Pig/Spark, 2006 Doug Cutting
- [Apache Spark](bigdata/mapreduce.md) - 인메모리 분산 처리, RDD(Resilient Distributed Dataset)/DataFrame/Dataset, Spark SQL/Streaming/MLlib/GraphX, MapReduce 대비 10~100배 빠름
- [스트리밍 처리](bigdata/mapreduce.md) - Kafka(메시지 브로커, 분산 스트리밍)/Flink(실시간 처리, 이벤트 타임)/Spark Streaming(마이크로 배치), 실시간 ETL, CEP
- [데이터 레이크](bigdata/data_lake.md) - 원시 데이터 저장(Raw Data), 스키마 온 리드(Schema-on-Read), S3/ADLS(Azure Data Lake Storage)/GCS, 정형+비정형 통합 저장
- [데이터 파이프라인](bigdata/dataops.md) - ETL(Extract-Transform-Load)/ELT(Extract-Load-Transform), Apache Airflow(워크플로우 오케스트레이션)/dbt(데이터 변환)/Prefect/Dagster
- [CAP 정리](bigdata/cap_theorem.md) - 일관성(Consistency)/가용성(Availability)/분할허용(Partition Tolerance) 중 2가지만 선택, CP(MongoDB)/AP(Cassandra)/CA(RDBMS), Eric Brewer(2000)
- [DataOps](bigdata/dataops.md) - 데이터 파이프라인 운영 자동화, CI/CD for Data, 데이터 품질 테스트, 버전 관리(DVC), 협업 문화, Agile for Data
- [데이터 시각화](bigdata/bigdata_characteristics.md) - BI 도구(Tableau/Power BI/Looker), Grafana(모니터링), 대시보드, 스토리텔링, 인터랙티브 시각화
- [데이터 민주화](bigdata/smart_data.md) - 셀프서비스 분석, 데이터 리터러시, 데이터 카탈로그, 접근성 향상, 비전문가 데이터 활용
- [데이터 마켓플레이스](bigdata/data_marketplace.md) - 데이터 거래 플랫폼, API 기반 데이터 공유, AWS Data Exchange/Snowflake Marketplace, 데이터 상품화
- [스마트 데이터](bigdata/smart_data.md) - 데이터 품질 관리, 맥락(Context) 데이터, 메타데이터 강화, 가치 있는 데이터 선별

### 클라우드 / DevOps
- [클라우드 서비스 모델](cloud/saas.md) - IaaS(인프라, EC2/Compute Engine)/PaaS(플랫폼, Heroku/Elastic Beanstalk)/SaaS(소프트웨어, Salesforce/Office 365)/XaaS(Everything as a Service)
- [클라우드 배포 모델](cloud/saas.md) - 퍼블릭(Public, AWS/Azure/GCP)/프라이빗(Private, On-Premise)/하이브리드(Hybrid)/멀티 클라우드(Multi-Cloud), 벤더 락인 방지
- [마이크로서비스](cloud/microservices.md) - MSA 아키텍처, 서비스 분해(DDD Bounded Context), API Gateway/Kong, Service Discovery(Eureka/Consul), Database per Service
- [도커/컨테이너](cloud/docker_container.md) - 컨테이너 기술, Dockerfile/이미지 레이어/Union FS, cgroups/namespace, Docker Hub/Registry, 컨테이너 vs VM(경량화)
- [쿠버네티스](cloud/kubernetes.md) - 컨테이너 오케스트레이션, Pod/Service/Deployment/ConfigMap/Secret/Ingress, k8s, Auto-scaling/Self-healing/Rolling Update, Google(2014)
- [서버리스](cloud/serverless.md) - FaaS(AWS Lambda/Azure Functions/GCP Cloud Functions)/BaaS(Firebase/S3), 이벤트 기반, 콜드 스타트, 사용량 기반 과금, 상태 비저장
- [클라우드 네이티브](cloud/microservices.md) - CNCF(Cloud Native Computing Foundation), 12-Factor App, 불변 인프라(Immutable Infrastructure), 선언적 API, Auto-scaling
- [SaaS](cloud/saas.md) - 서비스형 소프트웨어, 멀티테넌시, 구독 모델, 업데이트 자동화, Salesforce/Slack/Zoom/Notion, SaaS 2.0(AI 통합)
- [DevOps](cloud/devops.md) - 개발(Dev)+운영(Ops) 통합, 자동화/협업 문화, CI/CD/IaC/모니터링, CALMS(Culture/Automation/Lean/Measurement/Sharing)
- [CI/CD](cloud/ci_cd.md) - 지속적 통합(Continuous Integration)/지속적 배포(Continuous Deployment), Jenkins/GitLab CI/GitHub Actions/ArgoCD, 파이프라인 자동화
- [에지 컴퓨팅](cloud/edge_computing.md) - 분산 클라우드, MEC(Multi-access Edge Computing), 엣지-클라우드 연속성, 지연 최소화, 대역폭 절약, IoT 실시간 처리
- [서버 가상화](cloud/server_virtualization.md) - 하이퍼바이저(Hypervisor, Type 1/Type 2), VMware/KVM/Hyper-V, VM vs Container, 리소스 격리, 하드웨어 추상화
- [API 게이트웨이](cloud/api_gateway.md) - API 관리, 인증/인가(OAuth/JWT), 속도 제한(Rate Limiting), 로깅/모니터링, Kong/Apigee/AWS API Gateway
- [SRE (사이트 신뢰성 엔지니어링)](cloud/sre.md) - SLO(서비스 수준 목표)/SLI(지표)/SLA(협약), 오류 예산(Error Budget), Google(2003), 자동화, Toil 제거
- [카오스 엔지니어링](cloud/chaos_engineering.md) - 내결함성 검증, Chaos Monkey/Chaos Toolkit/Gremlin, 생산 환경 장애 주입 실험, 복원력(Resilience) 향상, Netflix(2011)
- [관찰성 (Observability)](cloud/observability.md) - 로그(Logs)/메트릭(Metrics)/트레이스(Traces) 3기둥, OpenTelemetry, Prometheus/Grafana/Jaeger, 시스템 상태 파악
- [GitOps](cloud/gitops.md) - Git 기반 인프라 관리, ArgoCD/Flux, 선언적 구성, 버전 관리, Git Single Source of Truth, PR 기반 변경
- [FinOps](cloud/finops.md) - 클라우드 비용 최적화, 사용량 관리, 예약 인스턴스/Spot Instance, 비용 할당/예측/최적화, FinOps Foundation
- [IaC (인프라 코드화)](cloud/devops.md) - Terraform(멀티클라우드)/Ansible(설정 관리)/CloudFormation(AWS)/Pulumi, 선언적 인프라, 버전 관리
- [서비스 메시](cloud/microservices.md) - Istio/Envoy/Linkerd, 트래픽 관리/보안(mTLS)/관찰성, Sidecar 패턴, 마이크로서비스 간 통신 제어

### 블록체인
- [블록체인](blockchain/blockchain.md) - 분산 원장 기술(DLT), 비허가형(Public, Bitcoin/Ethereum)/허가형(Private, Hyperledger Fabric), P2P 네트워크, 불변성, 투명성
- [스마트 컨트랙트](ai_ml/smart_contract.md) - 자동 실행 계약, Solidity(Ethereum)/Rust(Solana), EVM(Ethereum Virtual Machine), DAO, 코드 기반 계약
- [합의 메커니즘](ai_ml/consensus_mechanism.md) - PoW(작업증명, Bitcoin, 에너지 집약적)/PoS(지분증명, Ethereum 2.0)/DPoS(위임)/PBFT(허가형), 51% 공격 방지
- [이더리움](ai_ml/ethereum.md) - 스마트 컨트랙트 플랫폼, EVM, ERC-20(토큰)/ERC-721(NFT)/ERC-1155, Gas 비용, ETH 2.0(PoS 전환), DApp 생태계
- [NFT](ai_ml/ethereum.md) - 대체 불가 토큰(Non-Fungible Token), ERC-721, 디지털 자산 소유권, OpenSea, 크리에이터 이코노미, PFP 아트
- [DeFi](ai_ml/ethereum.md) - 탈중앙화 금융(Decentralized Finance), DEX(Uniswap)/유동성 풀/스테이킹/대출(Aave)/예치, TVL(Total Value Locked)
- [프라이빗 블록체인](blockchain/blockchain.md) - Hyperledger Fabric/Quorum/R3 Corda, 기업 블록체인, 권한 관리, 성능 최적화, B2B 활용
- [블록체인 오라클](blockchain/blockchain.md) - 외부 데이터 연동, Chainlink/Band Protocol, 스마트 컨트랙트→외부 API, 데이터 신뢰성 문제
- [채굴](ai_ml/mining.md) - 블록 생성, 해시레이트(Hashrate)/채굴 난이도(Difficulty)/보상(Reward)/반감기(Halving), PoW 합의, 채굴 풀

### IoT / 스마트시스템
- [IoT 아키텍처](iot/digital_twin.md) - 엣지(Edge)-포그(Fog)-클라우드(Cloud) 3계층, 디바이스→게이트웨이→플랫폼→애플리케이션, 엣지 컴퓨팅으로 지연 최소화
- [디지털 트윈](iot/digital_twin.md) - 가상 복제 시스템, CPS(사이버물리시스템), 실시간 동기화, 시뮬레이션, 예지 보전, Siemens/GE Digital
- [산업 IoT (IIoT)](iot/digital_twin.md) - 스마트팩토리, OT(운영기술)/IT(정보기술) 융합, 산업용 센서, 실시간 모니터링, 품질 관리, 안전 관리
- [MQTT/CoAP](iot/digital_twin.md) - IoT 경량 프로토콜, MQTT(Pub/Sub, QoS 0/1/2)/CoAP(RESTful, UDP), 낮은 대역폭, 높은 지연 허용
- [엣지 AI](iot/digital_twin.md) - 온디바이스 추론, TinyML(마이크로컨트롤러 ML), TensorFlow Lite/ONNX Runtime, 프라이버시 보호, 지연 최소화
- [LiDAR](iot/lidar.md) - 3D 공간 인식 센서, 레이저 펄스, 포인트 클라우드, 자율주행/드론/로봇/측량, Velodyne/Hesai/Luminar
- [멀티센서 융합](iot/multisensor.md) - IMU(관성 측정 장치)/카메라/LiDAR/레이더 융합, 칼만 필터, 센서 퓨전 알고리즘, 정확도 향상
- [스마트 그리드](iot/smart_grid.md) - 에너지 관리 시스템, 양방향 전력망, 수요 관리, 분산 전원 연계, 재생 에너지 통합, 효율적 전력 분배
- [스마트 미터](iot/smart_meter.md) - AMI(Advanced Metering Infrastructure), 원격 검침, 실시간 사용량 모니터링, 수요 반응(Demand Response)
- [ESS (에너지 저장 시스템)](iot/ess.md) - 배터리 저장, V2G(Vehicle-to-Grid), 에너지 플렉시빌리티, 태양광 연계, 피크 쉐이빙, 정전 대비
- [HMI](iot/hmi.md) - 인간-기계 인터페이스(Human-Machine Interface), SCADA/PLC 연계, 터치 패널, 산업용 UI, 운영자 모니터링
- [LBS](iot/lbs.md) - 위치 기반 서비스(Location-Based Service), GPS/실내 측위(Wi-Fi/블루투스/UWB), 지오로케이션, 내비게이션
- [포그 컴퓨팅](iot/fog_computing.md) - IoT 엣지 처리, 엣지와 클라우드 사이 중간 계층, 지연 감소, 대역폭 절약, 로컬 처리
- [수요반응](iot/demand_response.md) - DR(Demand Response) 프로그램, 부하 조절, 피크 관리, 인센티브 기반, 에너지 효율화
- [위치 측위](iot/positioning.md) - GPS(야외)/RFID/UWB(실내, cm급)/BLE 비콘/Wi-Fi RTT, A-GPS, 삼변측량, 정확도별 용도
- [액추에이터](iot/actuator.md) - 구동 요소, 서보 모터/솔레노이드/밸브, 피드백 제어, 센서→처리→액추에이터 루프

### XR (확장현실)
- [XR 기술](xr/) - AR(증강현실, Pokemon GO)/VR(가상현실, Meta Quest)/MR(혼합현실, HoloLens), 현실-가상 연속체, 몰입도별 분류
- [공간 컴퓨팅](xr/) - Apple Vision Pro/Meta Quest Pro, 공간 인터페이스, 제스처/시선/음성 입력, 3D 상호작용, 공간 오디오
- [메타버스](xr/) - 가상 세계 플랫폼, 아바타/디지털 자산/가상 경제, Roblox/Fortnite/Zepeto, 사회적 상호작용, UGC
- [디지털 트윈 XR 연계](xr/) - XR 기반 시뮬레이션, 가상 프로토타이핑, 원격 협업, 교육 훈련, 산업 응용

### 정보보안
- [대칭키 암호화](security/symmetric_encryption.md) - AES-128/256(블록 암호)/DES/3DES/ChaCha20(스트림 암호), 동일 키 암호화/복호화, 빠른 속도, 키 분배 문제
- [공개키 암호화](security/asymmetric_encryption.md) - RSA(2048~4096비트)/ECC(타원곡선, 짧은 키로 동등 보안), 공개키/개인키 쌍, 키 교환(ECDH), 디지털 서명
- [해시 함수](security/hash_function.md) - MD5(취약)/SHA-256/SHA-3/BLAKE3, 무결성 검증, HMAC(키 포함), 레인보우 테이블 방지(솔트)
- [PKI](security/pki.md) - 공개키 기반구조, CA(Certificate Authority)/인증서(X.509)/OCSP(폐지 확인)/CRL, 신뢰 체인, Let's Encrypt
- [디지털 서명](security/digital_signature.md) - 전자서명, 부인방지(Non-repudiation)/무결성/인증, RSA-PSS/ECDSA/EdDSA, 타임스탬프
- [TLS/SSL](security/encryption.md) - TLS 1.3(0-RTT, 성능 향상), 핸드셰이크/인증서 교환/세션 암호화, Forward Secrecy, HTTPS
- [PQC (양자 내성 암호)](security/encryption.md) - 격자 기반(Kyber/Dilithium)/해시 기반/다변수 기반, NIST PQC 표준화(2024), 양자컴퓨터 위협 대비
- [인증 방식](security/authentication.md) - OTP(일회용 비밀번호)/MFA(다중 인증)/바이오인식(지문/안면/홍채)/FIDO2/WebAuthn(패스워드리스)
- [정보보안 3원칙](security/information_security.md) - CIA(기밀성 Confidentiality/무결성 Integrity/가용성 Availability), AAA(인증/인가/계정), 보안의 기본 원칙
- [접근 제어 모델](security/information_security.md) - DAC(임의)/MAC(강제, 보안등급)/RBAC(역할 기반)/ABAC(속성 기반), 최소 권한 원칙
- [사이버 공격](security/cyber_attacks.md) - DDoS(분산 서비스 거부)/랜섬웨어(WannaCry)/APT(지능형 지속 위협)/공급망 공격(SolarWinds)/제로데이
- [악성코드](security/malware.md) - 바이러스(자기 복제)/웜(네트워크 확산)/트로이목마(위장)/스파이웨어(정보 탈취)/랜섬웨어(암호화)
- [사회공학](security/social_engineering.md) - 피싱(Phishing)/스피어피싱(표적형)/보이스피싱/스미싱(SMS)/CEO 사기(BEC), 인간 취약점 악용
- [SIEM](security/information_security.md) - 보안 정보 이벤트 관리, 로그 수집/상관관계 분석/실시간 경고, Splunk/IBM QRadar/Elastic SIEM
- [SOAR](security/information_security.md) - 보안 오케스트레이션/자동화/대응, 플레이북/자동화 워크플로우, 대응 시간 단축
- [제로 트러스트](security/information_security.md) - ZTNA(Zero Trust Network Access)/BeyondCorp/SDP(Software-Defined Perimeter), "절대 신뢰 금지", 지속 검증
- [개인정보 보호](security/information_security.md) - GDPR(유럽)/개인정보보호법(한국)/CCPA(미국 캘리포니아), 가명처리/익명화, 동의 원칙
- [디지털 포렌식](security/cyber_attacks.md) - 증거 수집/분석/연계 보관, 디스크/메모리/네트워크 포렌식, 법적 효력, 사고 대응
- [버그 바운티](security/cyber_attacks.md) - 취약점 공개 프로그램, HackerOne/Bugcrowd, 책임 있는 공개(Responsible Disclosure), 보상금
- [클라우드 보안](security/information_security.md) - CSPM(설정 관리)/CWPP(워크로드 보호)/CASB(액세스 보안), 공유 책임 모델, IAM 강화

### 핀테크 / 트렌드
- [디지털 전환 (DX)](trends/digital_transformation.md) - DX 전략, 로드맵, 비즈니스 모델 혁신, 고객 경험 혁신, 조직 문화 변화
- [AI 전환 (AX)](trends/digital_transformation.md) - AI 기반 비즈니스 혁신, AI 우선 전략, 프로세스 자동화, 의사결정 지원
- [플랫폼 경제](trends/platform_economy.md) - 플랫폼 비즈니스 모델, 네트워크 효과, 양면 시장, Uber/Airbnb/배달의민족, 승자 독식
- [핀테크](fintech/) - 디지털 금융, 간편결제(카카오페이/토스)/인터넷은행(카카오뱅크/토스뱅크)/오픈뱅킹/API 금융, 금융 민주화
- [CBDC](fintech/) - 중앙은행 디지털 화폐(Central Bank Digital Currency), 디지털 위안/디지털 달러, 현금 대체, 통화 정책
- [RegTech](fintech/) - 규제 기술(Regulatory Technology), 금융 컴플라이언스 자동화, AML(자금세탁방지)/KYC(신원확인), 규제 대응
- [BYOD](trends/byod.md) - 개인 기기 업무 활용(Bring Your Own Device), MDM(모바일 기기 관리), 보안 정책, 업무 효율성
- [하이프 사이클](trends/hype_cycle.md) - Gartner 기술 성숙도 곡선, 기술촉발→과대기대→환멸→계몽→생산성 안정기, 기술 도입 시점 판단
- [GovTech](trends/digital_transformation.md) - 정부 기술(Government Technology), 공공 디지털 혁신, 전자정부, 행정 자동화, 시민 서비스
- [Age-Tech](trends/digital_transformation.md) - 고령화 사회 기술, 실버케어/건강 모니터링/인지 훈련, 고령친화 서비스, 고령층 디지털 격해
- [ESG IT](trends/digital_transformation.md) - 친환경 IT, 그린 데이터센터, 탄소 중립(Carbon Neutral), PUE 최적화, 지속가능경영
- [데이터 3법](trends/digital_transformation.md) - 개인정보보호법/신용정보법/정보통신망법, 마이데이터(MyData), 데이터 주권, 활용과 보호 균형
