+++
title = "비정형 데이터 유형"
categories = ["studynotes-16_bigdata"]
+++

# 비정형 데이터 유형

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 비정형 데이터는 고정된 스키마가 없는 데이터로, 전체 데이터의 80% 이상을 차지하며 텍스트, 이미지, 오디오, 비디오, 로그 등 다양한 형태로 존재한다.
> 2. **가치**: 비정형 데이터 분석을 통해 고객 감성, 브랜드 평판, 이상 징후 등 정형 데이터로는 발견할 수 없는 통찰을 도출할 수 있다.
> 3. **융합**: NLP, 컴퓨터 비전, 음성 인식 AI 기술과 결합하여 비정형 데이터의 구조화 및 분석이 가능해졌다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

비정형 데이터(Unstructured Data)는 사전에 정의된 데이터 모델이나 스키마를 따르지 않는 데이터를 의미한다. 관계형 데이터베이스의 행-열 구조와 달리, 자유로운 형식을 가지며 저장 시점에 구조가 결정되지 않는다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    데이터 유형 분류 체계                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │                   전체 데이터 (100%)                         │  │
│   │                                                              │  │
│   │   ┌─────────────────────┐    ┌─────────────────────────┐   │  │
│   │   │   정형 데이터       │    │   비정형 + 반정형       │   │  │
│   │   │   (Structured)      │    │   (80%+)                │   │  │
│   │   │   ~20%              │    │                         │   │  │
│   │   │                     │    │   ┌─────┐ ┌───────────┐ │   │  │
│   │   │   RDBMS 테이블      │    │   │반정형│ │ 비정형    │ │   │  │
│   │   │   스프레드시트      │    │   │~15% │ │ ~65%      │ │   │  │
│   │   │   CSV 파일          │    │   │     │ │           │ │   │  │
│   │   └─────────────────────┘    │   │JSON │ │텍스트     │ │   │  │
│   │                              │   │XML  │ │이미지     │ │   │  │
│   │                              │   │HTML │ │오디오     │ │   │  │
│   │                              │   └─────┘ │비디오     │ │   │  │
│   │                              │           │로그       │ │   │  │
│   │                              │           │센서데이터 │ │   │  │
│   │                              │           └───────────┘ │   │  │
│   │                              └─────────────────────────┘   │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 💡 비유

비정형 데이터는 "자유로운 형식의 편지"에 비유할 수 있다. 정형 데이터가 주소지, 이름, 전화번호가 정해진 칸에 적히는 공문서라면, 비정형 데이터는 자유롭게 쓴 일기장, 손편지, 낙서 같은 것이다. 이를 분석하려면 내용을 읽고 의미를 파악해야 한다.

### 등장 배경 및 발전 과정

1. **데이터 생성 패턴의 변화**:
   - 소셜 미디어, 스마트폰, IoT 기기 보급으로 비정형 데이터 폭발
   - 2010년 이후 연평균 55% 성장, 정형 데이터는 20% 성장

2. **기존 기술의 한계**:
   - RDBMS는 스키마 변경 비용이 매우 높음
   - SQL만으로는 텍스트, 이미지 내용 이해 불가
   - ETL 파이프라인이 모든 비정형 데이터를 처리하지 못함

3. **AI 기술의 발전**:
   - 2012년 AlexNet(이미지), 2017년 Transformer(텍스트) 혁신
   - LLM(GPT, BERT)으로 자연어 이해 능력 비약적 향상

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 비정형 데이터 유형별 상세 분석

| 유형 | 생성 소스 | 저장 포맷 | 분석 기술 | 대표 활용 |
|------|-----------|-----------|-----------|-----------|
| **텍스트** | 이메일, SNS, 문서 | TXT, PDF, DOCX | NLP, LLM, 감성분석 | 여론 분석, 챗봇 |
| **이미지** | 스마트폰, CCTV, 위성 | JPEG, PNG, TIFF | CNN, Vision Transformer | 객체 탐지, 의료 진단 |
| **오디오** | 음성비서, 통화, 팟캐스트 | MP3, WAV, FLAC | ASR, Speaker Diarization | 음성 인식, 회의록 |
| **비디오** | 유튜브, CCTV, 라이브스트림 | MP4, MKV, AVI | Video CNN, Action Recognition | 보안 감시, 콘텐츠 분석 |
| **로그** | 서버, 앱, 네트워크 | JSON, SYSLOG, CLF | Log Analytics, AIOps | 이상 탐지, 장애 진단 |
| **센서** | IoT, 산업설비, 차량 | Binary, JSON, Protobuf | Time Series Analysis | 예지 정비, 스마트시티 |
| **소셜** | 트위터, 페이스북, 인스타 | JSON API | Social Network Analysis | 인플루언서, 트렌드 |

### 비정형 데이터 처리 파이프라인 아키텍처

```
┌─────────────────────────────────────────────────────────────────────────┐
│              비정형 데이터 처리 파이프라인 (Unstructured Data Pipeline)  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  1. Ingestion (수집)                                              │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │ │
│  │  │ S3      │ │ Kafka   │ │ REST API│ │ Web Scraper│ File   │    │ │
│  │  │ Upload  │ │ Stream  │ │ Polling │ │ Selenium  │ Watch  │    │ │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬─────┘ └───┬────┘    │ │
│  └───────┼───────────┼───────────┼───────────┼───────────┼──────────┘ │
│          │           │           │           │           │            │
│          └───────────┴───────────┴───────────┴───────────┘            │
│                                      │                                │
│                                      ▼                                │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  2. Raw Storage (원시 저장)                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────┐ │ │
│  │  │  Data Lake (S3/ADLS/GCS) - Bronze Layer                     │ │ │
│  │  │  s3://lake/raw/{text|image|audio|video|log}/{year}/{day}/   │ │ │
│  │  └─────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────┬───────────────────────────────────┘ │
│                                  │                                    │
│                                  ▼                                    │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  3. Processing (처리) - AI/ML 기반 구조화                         │ │
│  │                                                                   │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │ │
│  │  │   Text      │  │   Image     │  │   Audio     │              │ │
│  │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │              │ │
│  │  │ │BERT/GPT │ │  │ │ResNet   │ │  │ │Whisper  │ │              │ │
│  │  │ │NER      │ │  │ │YOLO     │ │  │ │Wav2Vec  │ │              │ │
│  │  │ │Sentiment│ │  │ │OCR      │ │  │ │Diarization│              │ │
│  │  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │              │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘              │ │
│  │                                                                   │ │
│  │  Output: 구조화된 JSON/Parquet (임베딩, 메타데이터 포함)          │ │
│  └───────────────────────────────┬───────────────────────────────────┘ │
│                                  │                                    │
│                                  ▼                                    │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  4. Refined Storage (정제 저장)                                   │ │
│  │  ┌─────────────────────────────────────────────────────────────┐ │ │
│  │  │  Delta Lake / Iceberg - Silver & Gold Layer                 │ │ │
│  │  │  - embeddings (vector DB): Pinecone, Milvus, Weaviate       │ │ │
│  │  │  - metadata (table): Parquet with schema                    │ │ │
│  │  │  - full-text (search): Elasticsearch / OpenSearch           │ │ │
│  │  └─────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: 텍스트 데이터 처리

```python
import json
from typing import List, Dict
from dataclasses import dataclass
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

@dataclass
class TextAnalysisResult:
    """텍스트 분석 결과 구조체"""
    doc_id: str
    raw_text: str
    language: str
    sentiment: str
    sentiment_score: float
    entities: List[Dict]
    keywords: List[str]
    embedding: List[float]

class UnstructuredTextProcessor:
    """비정형 텍스트 데이터 처리기"""

    def __init__(self, model_name: str = "bert-base-multilingual-cased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def process(self, raw_text: str, doc_id: str) -> TextAnalysisResult:
        """텍스트 분석 파이프라인"""

        # 1단계: 전처리 (Preprocessing)
        cleaned_text = self._preprocess(raw_text)

        # 2단계: 언어 감지 (Language Detection)
        language = self._detect_language(cleaned_text)

        # 3단계: 감성 분석 (Sentiment Analysis)
        sentiment, score = self._analyze_sentiment(cleaned_text)

        # 4단계: 개체명 인식 (Named Entity Recognition)
        entities = self._extract_entities(cleaned_text)

        # 5단계: 키워드 추출 (Keyword Extraction)
        keywords = self._extract_keywords(cleaned_text)

        # 6단계: 임베딩 생성 (Embedding Generation)
        embedding = self._generate_embedding(cleaned_text)

        return TextAnalysisResult(
            doc_id=doc_id,
            raw_text=raw_text,
            language=language,
            sentiment=sentiment,
            sentiment_score=score,
            entities=entities,
            keywords=keywords,
            embedding=embedding
        )

    def _preprocess(self, text: str) -> str:
        """텍스트 전처리"""
        import re
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', text)
        # 특수문자 정규화
        text = re.sub(r'[^\w\s가-힣.,!?]', ' ', text)
        # 공백 정규화
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _detect_language(self, text: str) -> str:
        """언어 감지 (langdetect 사용)"""
        from langdetect import detect
        try:
            return detect(text[:500])  # 앞부분만 사용
        except:
            return "unknown"

    def _analyze_sentiment(self, text: str) -> tuple:
        """감성 분석"""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)

        sentiment_map = {0: "negative", 1: "neutral", 2: "positive"}
        pred_class = torch.argmax(probs).item()

        return sentiment_map[pred_class], probs[0][pred_class].item()

    def _extract_entities(self, text: str) -> List[Dict]:
        """개체명 인식 (NER)"""
        # 실제로는 spaCy나 Hugging Face NER 모델 사용
        # 예시 구현
        entities = []
        import re
        # 이메일 패턴
        emails = re.findall(r'[\w.-]+@[\w.-]+\.\w+', text)
        for email in emails:
            entities.append({"text": email, "type": "EMAIL"})
        # 날짜 패턴
        dates = re.findall(r'\d{4}-\d{2}-\d{2}', text)
        for date in dates:
            entities.append({"text": date, "type": "DATE"})
        return entities

    def _extract_keywords(self, text: str) -> List[str]:
        """키워드 추출 (TF-IDF 또는 KeyBERT)"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer(max_features=10, stop_words='english')
        try:
            tfidf_matrix = vectorizer.fit_transform([text])
            return vectorizer.get_feature_names_out().tolist()
        except:
            return []

    def _generate_embedding(self, text: str) -> List[float]:
        """텍스트 임베딩 생성"""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.base_model(**inputs)
            # [CLS] 토큰 임베딩 사용
            embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()

        return embedding.flatten().tolist()


# 사용 예시
if __name__ == "__main__":
    processor = UnstructuredTextProcessor()

    sample_text = """
    2024년 3월 15일, 삼성전자는 새로운 AI 칩을 발표했습니다.
    이번 발표에 대해 시장의 반응은 매우 긍정적입니다.
    자세한 문의는 contact@samsung.com으로 연락주세요.
    """

    result = processor.process(sample_text, "doc_001")
    print(json.dumps(result.__dict__, indent=2, ensure_ascii=False))
```

### 심층 동작 원리: 이미지 데이터 처리

```python
import cv2
import numpy as np
from PIL import Image
from typing import List, Dict, Tuple
import torch
from torchvision import transforms

class ImageProcessor:
    """비정형 이미지 데이터 처리기"""

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
        ])

    def extract_metadata(self, image_path: str) -> Dict:
        """이미지 메타데이터 추출"""
        from PIL import ExifTags

        img = Image.open(image_path)
        metadata = {
            "format": img.format,
            "mode": img.mode,
            "size": img.size,
            "width": img.width,
            "height": img.height,
        }

        # EXIF 데이터 추출
        try:
            exif = img._getexif()
            if exif:
                for tag_id, value in exif.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    if tag in ["DateTime", "Make", "Model", "GPSInfo"]:
                        metadata[tag] = str(value)
        except:
            pass

        return metadata

    def detect_objects(self, image_path: str) -> List[Dict]:
        """객체 탐지 (YOLO 등 활용)"""
        # 실제로는 ultralytics YOLO 모델 사용
        img = cv2.imread(image_path)
        # 예시: 에지 검출로 윤곽선 찾기
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        objects = []
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)
            if w > 50 and h > 50:  # 작은 객체 필터링
                objects.append({
                    "object_id": i,
                    "bbox": [int(x), int(y), int(w), int(h)],
                    "area": int(cv2.contourArea(contour))
                })

        return objects

    def extract_color_histogram(self, image_path: str) -> Dict:
        """색상 히스토그램 추출"""
        img = cv2.imread(image_path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # H, S, V 채널별 히스토그램
        h_hist = cv2.calcHist([hsv], [0], None, [180], [0, 180])
        s_hist = cv2.calcHist([hsv], [1], None, [256], [0, 256])
        v_hist = cv2.calcHist([hsv], [2], None, [256], [0, 256])

        return {
            "hue_histogram": h_hist.flatten().tolist(),
            "saturation_histogram": s_hist.flatten().tolist(),
            "value_histogram": v_hist.flatten().tolist(),
            "dominant_color": self._get_dominant_color(hsv)
        }

    def _get_dominant_color(self, hsv_img: np.ndarray) -> Dict:
        """주요 색상 추출"""
        data = hsv_img.reshape(-1, 3)
        # K-means 클러스터링으로 주요 색상 찾기
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=3, random_state=42)
        kmeans.fit(data)

        dominant = kmeans.cluster_centers_[0]
        return {
            "hue": int(dominant[0]),
            "saturation": int(dominant[1]),
            "value": int(dominant[2])
        }
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 정형 vs 반정형 vs 비정형 데이터 비교

| 구분 | 정형 (Structured) | 반정형 (Semi-structured) | 비정형 (Unstructured) |
|------|-------------------|--------------------------|----------------------|
| **스키마** | 고정 (사전 정의) | 유연 (자체 기술) | 없음 |
| **저장 형식** | RDBMS 테이블 | JSON, XML, YAML | 파일 (이진/텍스트) |
| **쿼리 언어** | SQL | SQL (JSON 함수), XQuery | 전용 API/ML 모델 |
| **분석 난이도** | 낮음 | 중간 | 높음 |
| **데이터 비율** | ~20% | ~15% | ~65% |
| **활용률** | 80%+ | 50%+ | 20%+ |
| **대표 예시** | ERP, CRM 데이터 | API 응답, 로그 | 이미지, 음성, 문서 |

### 비정형 데이터 분석 기술 스택

| 데이터 유형 | 수집 | 저장 | 처리/분석 | 시각화 |
|-------------|------|------|-----------|--------|
| **텍스트** | Kafka, API | S3, Elasticsearch | Spark NLP, Hugging Face | Kibana, Word Cloud |
| **이미지** | S3 Upload | S3, MinIO | PyTorch, TensorFlow | Label Studio |
| **오디오** | Kafka, S3 | S3 | Whisper, Kaldi | 파형 차트 |
| **비디오** | Kafka, RTSP | S3, MinIO | OpenCV, FFmpeg | 대시보드 |
| **로그** | Fluentd, Filebeat | Elasticsearch, S3 | Spark, Logstash | Grafana, Kibana |

### 과목 융합: 네트워크 관점

비정형 데이터의 대용량 전송은 네트워크 최적화가 필수적이다:

1. **압축**: 텍스트(gzip), 이미지(WebP), 비디오(H.265)로 대역폭 절감
2. **프로토콜**: HTTP/2 멀티플렉싱, gRPC 스트리밍으로 효율적 전송
3. **CDN**: 정적 비정형 데이터(이미지, 비디오) 엣지 캐싱

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 고객 문의 자동 분류 시스템

```
┌─────────────────────────────────────────────────────────────────────────┐
│  시나리오: 이커머스 고객 문의 자동 분류 및 라우팅 시스템                 │
├─────────────────────────────────────────────────────────────────────────┤
│  현황:                                                                 │
│  - 일 10,000건 고객 문의 (이메일, 챗봇, 게시판)                        │
│  - 수동 분류로 평균 4시간 소요                                         │
│  - 분류 오류율 15%                                                     │
│                                                                         │
│  입력 데이터 (비정형):                                                  │
│  - 텍스트: 문의 내용, 첨부 파일 설명                                    │
│  - 이미지: 제품 사진, 손상 상태 사진                                    │
│                                                                         │
│  처리 파이프라인:                                                       │
│  1. 수집: Gmail API + 챗봇 Webhook + 게시판 스크래핑                   │
│  2. 저장: S3 (raw/email/, raw/chat/, raw/image/)                       │
│  3. 분석:                                                              │
│     - 텍스트: BERT 기반 의도 분류 (배송/환불/결함/기타)                 │
│     - 이미지: ResNet 기반 손상 유형 분류                               │
│     - 통합: 멀티모달 모델로 텍스트+이미지 결합 분석                     │
│  4. 라우팅: 분류 결과에 따른 담당팀 자동 할당                          │
│                                                                         │
│  기대 효과:                                                             │
│  - 분류 시간: 4시간 → 30초                                             │
│  - 오류율: 15% → 3%                                                    │
│  - 고객 만족도: 20% 향상                                               │
└─────────────────────────────────────────────────────────────────────────┘
```

### 도입 체크리스트

**기술적 고려사항**
- [ ] 비정형 데이터 유형별 저장 전략 수립 (S3 버킷 구조, 파티셔닝)
- [ ] AI/ML 모델 선정 (오픈소스 vs 클라우드 API)
- [ ] 임베딩 저장을 위한 벡터 DB 선정 (Pinecone, Milvus, Weaviate)
- [ ] 전처리 파이프라인 구축 (Spark, Airflow)
- [ ] GPU/TPU 리소스 계획 (학습 vs 추론)

**운영/보안적 고려사항**
- [ ] 개인정보 포함 여부 검사 (PII Detection)
- [ ] 데이터 비식별화 처리 (마스킹, 블러링)
- [ ] 저작권 확인 (이미지, 비디오 출처)
- [ ] 모델 편향성 테스트 (Fairness AI)

### 안티패턴 (Anti-patterns)

1. **Raw Data Hoarding**: 분석 목적 없이 모든 비정형 데이터 저장
2. **One-Size-Fits-All**: 모든 비정형 데이터를 동일한 방식으로 처리
3. **Ignoring Metadata**: 메타데이터 없이 원시 파일만 저장
4. **Over-Processing**: 불필요하게 높은 해상도/품질로 처리하여 비용 낭비

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 도입 전 | 도입 후 | 개선 효과 |
|------|---------|---------|-----------|
| 데이터 활용률 | 20% | 65% | +225% |
| 분석 자동화율 | 10% | 80% | +700% |
| 통찰 도출 시간 | 2주 | 4시간 | -98.8% |
| 분류 정확도 | 75% | 94% | +25.3% |

### 미래 전망

1. **멀티모달 AI**: 텍스트+이미지+오디오 통합 분석 (GPT-4V, Gemini)
2. **실시간 처리**: 엣지 디바이스에서 비정형 데이터 즉시 분석
3. **자동 라벨링**: Foundation Model로 비정형 데이터 자동 태깅
4. **Vector Search**: 임베딩 기반 시맨틱 검색으로 비정형 데이터 검색 혁신

### 참고 표준/가이드

- **ISO/IEC 15938**: Multimedia Content Description Interface (MPEG-7)
- **Dublin Core**: 메타데이터 표준
- **EXIF 2.3**: 이미지 메타데이터 표준
- **개인정보보호법**: 제23조 (이미지, 음성 정보의 처리)

---

## 📌 관련 개념 맵

- [반정형 데이터 (JSON/XML)](./semi_structured_data.md) - 스키마가 부분적으로 존재하는 데이터
- [텍스트 마이닝](../04_analysis/text_mining.md) - 비정형 텍스트에서 통찰 추출
- [자연어 처리 (NLP)](../04_analysis/nlp_overview.md) - 텍스트 데이터 이해 기술
- [컴퓨터 비전](../04_analysis/computer_vision.md) - 이미지/비디오 분석 기술
- [데이터 레이크](../06_data_lake/data_lakehouse.md) - 비정형 데이터 저장 아키텍처
- [벡터 데이터베이스](../05_nosql/vector_database.md) - 임베딩 저장 및 유사도 검색

---

## 👶 어린이를 위한 3줄 비유

**1단계 (무엇인가요?)**: 비정형 데이터는 정해진 칸에 적히지 않는 자유로운 글과 그림이에요. 일기장에 쓴 글, 스마트폰으로 찍은 사진, 엄마 목소리 녹음 파일 같은 거예요.

**2단계 (어떻게 쓰나요?)**: AI 컴퓨터 친구가 이 자유로운 글과 그림을 읽고 이해해요. "이 사진에는 고양이가 있어!", "이 글은 행복한 이야기네!"라고 분석해 주죠. 그러면 우리는 숫자만 보고 알 수 없는 비밀을 찾을 수 있어요.

**3단계 (왜 중요한가요?)**: 세상의 대부분 정보가 비정형 데이터예요. 이를 잘 분석하면 사람들이 무엇을 좋아하는지, 어떤 문제가 있는지, 앞으로 무슨 일이 일어날지 알 수 있어요. 마치 보물 지도를 해독해서 보물을 찾는 것과 같아요!
