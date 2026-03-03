+++
title = "9. 인공지능"
sort_by = "title"
weight = 9
[extra]
categories = "pe_exam"
+++

# 제9과목: 인공지능 (Artificial Intelligence)

PE 9번째 과목: 인공지능 이론·응용·인프라·거버넌스 전반을 다룹니다.

## 핵심 키워드

### AI 기초 (ai_foundations)
- [머신러닝 개요](ai_foundations/machine_learning.md) - 지도(라벨 있음)/비지도(라벨 없음)/자기지도(Self-Supervised, 대조 학습)/강화 학습(보상 기반), 학습 패러다임
- [학습 알고리즘](ai_foundations/machine_learning.md) - 경사 하강법(GD/SGD/Mini-batch)/Adam(AdaGrad+RMSProp)/역전파(Backpropagation, 연쇄 법칙), 옵티마이저
- [모델 평가](ai_foundations/machine_learning.md) - 정밀도(Precision)/재현율(Recall)/F1-Score/AUC-ROC/혼동 행렬(Confusion Matrix), 분류/회귀 메트릭
- [과적합/정규화](ai_foundations/machine_learning.md) - 과적합(Overfitting, 훈련↓일반화)/과소적합(Underfitting), L1(Lasso)/L2(Ridge) 정규화/드롭아웃/배치 정규화/데이터 증강
- [앙상블 학습](ai_foundations/ensemble_learning.md) - 배깅(Bagging, Random Forest)/부스팅(Boosting, XGBoost/LightGBM/CatBoost)/스태킹(Stacking), 다양성 확보
- [강화 학습 (RL)](ai_foundations/reinforcement_learning.md) - MDP(마르코프 결정 과정)/보상 함수/Q-러닝/DQN(Deep Q-Network)/PPO(Proximal Policy Optimization)/RLHF(인간 피드백)
- [연합 학습 (Federated Learning)](ai_foundations/federated_learning.md) - 프라이버시 보존, 분산 훈련(로컬→중앙 가중치만), Federated Averaging, 데이터 프라이버시
- [전이 학습 (Transfer Learning)](ai_foundations/machine_learning.md) - 사전학습 모델(Pretrained) 활용, 도메인 적응, Fine-tuning, Feature Extraction
- [자기지도 학습](ai_foundations/machine_learning.md) - Contrastive Learning(SimCLR/MoCo)/BYOL/Masked Language Modeling(MLM), 라벨 없는 데이터 활용
- [능동 학습 (Active Learning)](ai_foundations/machine_learning.md) - 라벨링 비용 최소화, 불확실성 샘플링, 전략적 데이터 선택

### 딥러닝 (deep_learning)
- [CNN (합성곱 신경망)](deep_learning/cnn.md) - 합성곱(Convolution, 특징 추출)/풀링(Pooling, 다운샘플링)/완전연결(FC), 이미지 분류, LeNet(1998)→AlexNet(2012)
- [최신 CNN 아키텍처](deep_learning/cnn.md) - ResNet(잔차 연결)/EfficientNet(복합 스케일링)/ConvNeXt/비전 트랜스포머(ViT, 패치 임베딩), ImageNet 성능
- [RNN/LSTM/GRU](deep_learning/rnn_lstm.md) - 순환 신경망(Recurrent), 긴 의존성 문제(Vanishing Gradient), LSTM(장단기 메모리)/GRU(게이트 메커니즘)
- [Transformer 아키텍처](deep_learning/transformer.md) - Self-Attention(Q/K/V)/Multi-Head Attention/위치 인코딩(PE), "Attention is All You Need"(2017), 병렬 처리
- [BERT](deep_learning/transformer.md) - 양방향 사전학습(Bidirectional), MLM(마스크드 언어 모델)/NSP(다음 문장 예측), 자연어 이해(NLU)
- [GPT 시리즈](deep_learning/transformer.md) - 자기회귀 생성(Autoregressive), 스케일링 법칙(Scaling Laws), GPT-3(175B)/GPT-4/ChatGPT, 생성형 AI
- [GAN (생성 적대 신경망)](deep_learning/diffusion_model.md) - 생성자(Generator)/판별자(Discriminator), DCGAN/StyleGAN/CycleGAN, 대항 훈련
- [Diffusion 모델](deep_learning/diffusion_model.md) - DDPM(노이즈 제거)/DDIM, 순방향(노이즈 추가)/역방향(노이즈 제거), Stable Diffusion/DALL-E 3
- [Graph Neural Network (GNN)](deep_learning/transformer.md) - 그래프 기반 학습, 메시지 전달(Message Passing), 노드/간선/그래프 분류, GCN/GAT
- [신경망 최적화](deep_learning/transformer.md) - 학습률 스케줄링(Warmup/Cosine Decay)/그래디언트 클리핑/가중치 초기화(Xavier/He), 훈련 안정화

### 생성 AI (generative_ai)
- [LLM (대형 언어 모델)](generative_ai/llm.md) - GPT(OpenAI)/Claude(Anthropic)/Gemini(Google)/Llama(Meta), 스케일링 법칙, 컨텍스트 윈도우
- [RAG (검색 증강 생성)](generative_ai/rag.md) - 외부 지식 통합, 문서 청킹(Chunking)/임베딩/유사도 탐색, 환각(Hallucination) 완화
- [Prompt Engineering](generative_ai/prompt_engineering.md) - Zero-shot/Few-shot/Chain-of-Thought(CoT)/Tree-of-Thought/ReAct, 프롬프트 설계
- [Fine-Tuning](generative_ai/fine_tuning.md) - 전체 파인튜닝/LoRA(Low-Rank Adaptation)/QLoRA/PEFT(Parameter-Efficient), RLHF(인간 피드백)
- [AI 에이전트](generative_ai/ai_agents.md) - ReAct(Reasoning+Acting)/도구 사용(Tool Use)/계획-행동-관찰 루프, 자율적 작업 수행
- [멀티 에이전트 시스템](generative_ai/ai_agents.md) - 에이전트 오케스트레이션, AutoGen/LangGraph/CrewAI, 역할 분담/협업
- [벡터 데이터베이스](generative_ai/vector_database.md) - 임베딩 저장/유사도 탐색(코사인/내적/L2), Pinecone/Weaviate/ChromaDB/Milvus/Qdrant
- [지식 그래프](generative_ai/knowledge_graph.md) - 엔티티(Entity)/관계(Relation)/온톨로지(Ontology), Graph RAG, 구조화 지식, Neo4j
- [멀티모달 AI](generative_ai/multimodal_ai.md) - 텍스트+이미지+오디오+비디오, GPT-4V/Gemini/CLIP(이미지-텍스트 매칭), 크로스 모달 이해
- [MoE (Mixture of Experts)](generative_ai/llm.md) - 희소 활성화(Sparse Activation), Mixtral/GPT-4, 전문가 라우팅, 효율적 추론
- [추론형 AI (Reasoning AI)](generative_ai/llm.md) - o1/o3, Chain-of-Thought 심층 추론, 수학/코딩/논리, 사고 과정 표현
- [LLM 평가](generative_ai/llm.md) - MMLU(지식)/HumanEval(코딩)/BIG-Bench/GPQA, 환각 탐지, 벤치마크
- [OWASP LLM Top 10](generative_ai/llm.md) - 프롬프트 인젝션/데이터 유출/공급망 위험/모델 도용/과도한 의존, LLM 보안
- [지식 증류 (Knowledge Distillation)](generative_ai/fine_tuning.md) - 교사(Teacher)-학생(Student) 모델, 소형 고성능 모델, 추론 효율화

### MLOps
- [MLOps 개요](mlops/mlops_overview.md) - ML 파이프라인, 데이터→전처리→훈련→평가→배포→모니터링, 엔드투엔드 자동화
- [ML 파이프라인](mlops/mlops_overview.md) - 데이터 수집/검증/전처리/특성 추출/모델 훈련/평가/배포, Kubeflow/Airflow/Vertex AI
- [모델 서빙](mlops/mlops_overview.md) - 배치/온라인/스트리밍 추론, TorchServe/Triton Inference Server/BentoML/SageMaker
- [모델 모니터링](mlops/mlops_overview.md) - 데이터 드리프트(Data Drift)/개념 드리프트(Concept Drift)/성능 저하 탐지, Prometheus/Evidently
- [피처 스토어](mlops/feature_store.md) - 피처 재사용/훈련-서빙 일관성(Training-Serving Skew), Feast/Tecton/Vertex Feature Store
- [A/B 테스트](mlops/mlops_overview.md) - 모델 비교, 카나리 배포(Canary), 트래픽 분할, 통계적 유의성 검증
- [모델 레지스트리](mlops/mlops_overview.md) - 버전 관리, MLflow/Weights & Biases/Neptune.ai, 메타데이터 추적
- [데이터 버전 관리](mlops/mlops_overview.md) - DVC(Data Version Control)/Git LFS, 재현 가능한 실험, 데이터 계보(Lineage)

### AI 응용 (ai_applications)
- [컴퓨터 비전](ai_applications/computer_vision.md) - 이미지 분류/객체 탐지(YOLO/R-CNN/DETR)/세그멘테이션/OCR, 의료 영상/자율주행
- [자연어 처리 (NLP)](ai_applications/nlp.md) - 텍스트 분류/NER(개체명 인식)/감성 분석/기계 번역/요약, 챗봇/검색
- [자율주행](ai_applications/autonomous_driving.md) - 인지(센서 융합)/판단(경로 계획)/제어(액추에이터), SAE 레벨 0~5, Tesla/Waymo
- [추천 시스템](ai_applications/nlp.md) - 협업 필터링(Collaborative)/콘텐츠 기반(Content-based)/하이브리드, 행렬 분해(MF)/딥러닝
- [의료 AI](ai_applications/computer_vision.md) - 의료 영상 분석(CT/MRI/X-ray)/신약 개발/임상 의사결정 지원, FDA 승인
- [생성 AI 응용](ai_applications/nlp.md) - AI 코드 생성(Copilot)/문서 요약/대화 시스템/가상 에이전트, 생산성 향상
- [음성 AI](ai_applications/nlp.md) - STT(Whisper)/TTS(음성 합성)/화자 인식/감정 분석, 음성 비서/콜센터

### AI 거버넌스 (ai_governance)
- [AI 윤리](ai_governance/ai_ethics.md) - 공정성(Fairness)/편향 방지(Bias Mitigation)/책임성(Accountability)/투명성(Transparency)
- [XAI (설명 가능 AI)](ai_governance/xai.md) - SHAP(SHapley Additive exPlanations)/LIME(Local Interpretable)/Grad-CAM(시각화), 해석 가능성
- [AI 규제 프레임워크](ai_governance/ai_ethics.md) - EU AI Act(위험 기반 분류)/NIST AI RMF/UNESCO AI 윤리, 규제 준수
- [AI 리스크 관리](ai_governance/ai_ethics.md) - AI 안전성(Safety)/Red Teaming(적대적 테스트)/모델 카드(Model Cards), 위험 완화
- [개인정보 보호 AI](ai_governance/ai_ethics.md) - 차분 프라이버시(Differential Privacy)/동형 암호/연합 학습, 프라이버시 보존 ML
- [AI 책임성](ai_governance/ai_ethics.md) - 모델 감사/알고리즘 영향 평가(AIA)/사후 책임(Accountability), 거버넌스 구조
- [AI 표준화](ai_governance/ai_ethics.md) - ISO/IEC 42001(AI 관리 시스템)/ISO/IEC 23894(AI 리스크)/ITU AI 프레임워크

### AI 인프라 (ai_infrastructure)
- [GPU/NPU 아키텍처](ai_infrastructure/gpu_npu.md) - CUDA(NVIDIA)/Tensor Core/병렬 연산(SIMT)/메모리 대역폭(HBM), AI 가속
- [AI 가속기](ai_infrastructure/gpu_npu.md) - TPU(Google, Tensor Processing Unit)/NPU(Apple Neural Engine)/Gaudi(Intel)/Trainium(AWS)
- [분산 학습](ai_infrastructure/edge_npu_ai.md) - 데이터 병렬(Data Parallel)/모델 병렬(Model Parallel)/파이프라인 병렬, AllReduce(NCCL)
- [모델 경량화](ai_infrastructure/model_compression.md) - 양자화(Quantization: FP32→INT8/INT4)/프루닝(Pruning)/지식 증류, 엣지 배포
- [엣지 AI / NPU](ai_infrastructure/edge_npu_ai.md) - 온디바이스 추론, TinyML/TFLite/ONNX Runtime/Core ML, 프라이버시/지연 최소화
- [PIM (Processing-In-Memory)](ai_infrastructure/gpu_npu.md) - 메모리 내 연산, HBM-PIM/Processing-near-Memory, 메모리 병목 해결
- [AI 클러스터](ai_infrastructure/edge_npu_ai.md) - InfiniBand/NVLink/고속 인터커넥트, GPU 클러스터, 슈퍼컴퓨터
- [에너지 효율성](ai_infrastructure/model_compression.md) - 그린 AI/탄소 발자국(Carbon Footprint)/PUE 최소화, 지속가능 AI
- [모델 서빙 최적화](ai_infrastructure/model_compression.md) - TensorRT/vLLM/연속 배칭(Continuous Batching)/KV Cache, 추론 속도 향상
