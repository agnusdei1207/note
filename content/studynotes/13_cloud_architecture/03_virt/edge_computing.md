+++
title = "엣지 컴퓨팅 (Edge Computing)"
date = 2024-05-18
description = "클라우드 중앙 서버로 보내지 않고 단말 주변 Edge에서 데이터를 실시간 처리하는 분산 컴퓨팅 패러다임"
weight = 13
[taxonomies]
categories = ["studynotes-13_cloud_architecture"]
tags = ["Edge Computing", "Low Latency", "IoT", "5G MEC", "Real-time Processing"]
+++

# 엣지 컴퓨팅 (Edge Computing)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 엣지 컴퓨팅은 데이터 소스(IoT 센서, 모바일 기기, 공장 설비)와 물리적으로 가까운 위치(Edge)에 컴퓨팅 자원을 배치하여, 클라우드로의 데이터 전송 없이 실시간(Real-time) 처리하는 분산 컴퓨팅 아키텍처입니다.
> 2. **가치**: 지연 시간(Latency)을 밀리초(ms) 단위로 단축하고, 네트워크 대역폭(Bandwidth) 사용을 50~90% 절감하며, 네트워크 단절 상황에서도 서비스 연속성을 보장합니다.
> 3. **융합**: 5G MEC(Multi-access Edge Computing), IoT 플랫폼, AI/ML 추론, 자율주행, 스마트 팩토리와 결합하여 클라우드-엣지 협업(Cloud-Edge Collaboration) 생태계를 구축합니다.

---

## Ⅰ. 개요 (Context & Background)

엣지 컴퓨팅(Edge Computing)은 중앙집중식 클라우드 컴퓨팅의 한계를 극복하기 위해 등장한 분산 컴퓨팅 패러다임입니다. 기존 클라우드 모델은 모든 데이터를 중앙 데이터센터로 전송하여 처리하는 방식이었으나, IoT 기기의 폭발적 증가(2025년 750억 개 예상)와 실시간 처리 요구사항(자율주행: 10ms 이내 반응)으로 인해 중앙집중식 모델의 물리적, 경제적 한계가 드러났습니다. 엣지 컴퓨팅은 "데이터가 생성되는 곳에서 처리한다"는 핵심 원칙을 통해 이러한 문제를 해결합니다.

**💡 비유**: 엣지 컴퓨팅은 **'각 가정에 설치된 미니 창고'**와 같습니다. 기존에는 모든 물건을 외부 대형 창고(클라우드)로 옮겼다가 다시 가져와야 했지만, 엣지 컴퓨팅은 자주 쓰는 물건(핫 데이터)을 집 안 미니 창고(엣지 서버)에 보관해 두고 즉시 꺼내 씁니다. 이렇게 하면 대형 창고까지 왕복하는 시간(지연)을 줄이고, 트럭(네트워크 대역폭)도 덜 이용하게 됩니다.

**등장 배경 및 발전 과정**:
1. **클라우드 중앙집중식 모델의 한계**: 2020년 기준 하루 2.5엑사바이트(EB)의 데이터가 생성되며, 이를 모두 중앙 클라우드로 전송하면 네트워크 비용과 지연이 폭증합니다.
2. **실시간 애플리케이션의 등장**: 자율주행차는 0.1초 내 장애물 인식 필요, 산업용 로봇은 1ms 제어 루프 요구 등 중앙 클라우드로의 왕복 지연(50~200ms)이 용납되지 않습니다.
3. **프라이버시와 규제**: 의료 영상, CCTV 등 민감 데이터를 외부로 전송하지 않고 로컬에서 처리해야 하는 규제 요구사항 증가.
4. **기술적 성숙**: 저전력 고성능 칩(NVIDIA Jetson, Google Edge TPU), 5G 네트워크, 컨테이너/Kubernetes의 경량화(K3s, MicroK8s)가 엣지 컴퓨팅을 현실화했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 엣지 컴퓨팅 계층 구조 (표)

| 계층 | 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 비유 |
|---|---|---|---|---|
| **디바이스 엣지 (Device Edge)** | 센서, 액추에이터, 임베디드 MCU | 데이터 수집, 1차 필터링, 즉각 제어 | GPIO, I2C, SPI 프로토콜로 센서 폴링, 인터럽트 처리 | 손끝 감각 |
| **펫 엣지 (Far Edge)** | 게이트웨이, 라즈베리파이, 산업용 PC | 데이터 집계, 경량 분석, 통신 프로토콜 변환 | MQTT 브로커, 로컬 ML 추론, 데이터 압축 | 손목 시계 |
| **메트로 엣지 (Metro Edge)** | 통신사 MEC, 지역 데이터센터 | 고부하 처리, AI 모델 실행, 콘텐츠 캐싱 | Kubernetes 클러스터, GPU 추론, CDN 캐시 | 동네 도서관 |
| **리전 엣지 (Regional Edge)** | CSP 리전, 하이퍼스케일 데이터센터 | 대규모 배치 처리, 모델 학습, 장기 저장 | Spark, TensorFlow Training, Data Lake | 시도청사 |
| **중앙 클라우드 (Central Cloud)** | 글로벌 CSP 백본 | 전역 오케스트레이션, 거버넌스, 비즈니스 로직 | Multi-Cluster Management, Global LB, IAM | 중앙정부 |

### 정교한 엣지 컴퓨팅 아키텍처 다이어그램

```ascii
+-------------------------------------------------------------------------+
|                          Central Cloud (Region)                          |
|  +-----------------+  +-----------------+  +-----------------+           |
|  | AI Model Train  |  | Data Lake       |  | Global Policy   |           |
|  | (Spark/TF)      |  | (S3/BigQuery)   |  | (IAM/Governance)|           |
|  +--------+--------+  +--------+--------+  +--------+--------+           |
|           |                    |                    |                    |
+-----------+--------------------+--------------------+--------------------+
            |                    |                    |
            |  (Bulk Data, Hours | (Policy, Minutes)  | (Model Update)
            |   Latency OK)      |                    |
            v                    v                    v
+-------------------------------------------------------------------------+
|                    Metro Edge (MEC / Regional Data Center)               |
|  +-----------------+  +-----------------+  +-----------------+           |
|  | K3s/K8s Cluster |  | Edge AI Infer.  |  | CDN Cache       |           |
|  | (10-100 nodes)  |  | (GPU/TPU)       |  | (Video/Images)  |           |
|  +--------+--------+  +--------+--------+  +--------+--------+           |
|           |                    |                    |                    |
+-----------+--------------------+--------------------+--------------------+
            | 5G/ fiber (ms Latency)                   |
            v                                          v
+-------------------------------------------------------------------------+
|                         Far Edge (Gateway/IoT Hub)                       |
|  +-----------------+  +-----------------+  +-----------------+           |
|  | Edge Gateway    |  | Local Broker    |  | Data Filtering  |           |
|  | (ARM/x86)       |  | (MQTT/AMQP)     |  | (Compression)   |           |
|  +--------+--------+  +--------+--------+  +--------+--------+           |
|           |                    |                    |                    |
+-----------+--------------------+--------------------+--------------------+
            | WiFi/ BLE/ Zigbee/ LoRa (Local Network)
            v
+-------------------------------------------------------------------------+
|                        Device Edge (Sensors/Actuators)                   |
|  +-----------+  +-----------+  +-----------+  +-----------+  +-----------+
|  | Camera    |  | Lidar     |  | Temp      |  | Vibration |  | PLC/CNC   |
|  | (Vision)  |  | (3D)      |  | Sensor    |  | Sensor    |  | (Control) |
|  +-----------+  +-----------+  +-----------+  +-----------+  +-----------+
|    |                 |               |              |              |
|    v                 v               v              v              v
|  [Raw Data]       [Raw Data]     [Filtered]     [Filtered]    [Status]
|   (MB/s)          (GB/s)         (KB/s)          (KB/s)        (B/s)
+-------------------------------------------------------------------------+
```

### 심층 동작 원리: 엣지 AI 추론 파이프라인

1. **센서 데이터 수집**: 카메라(30fps, 1080p) -> 엣지 게이트웨이로 H.264 스트림 전송
2. **데이터 전처리**: 게이트웨이에서 프레임 디코딩, 리사이징(224x224), 정규화(0~1)
3. **로컬 AI 추론**: Edge TPU에서 YOLOv5 모델 실행, 객체 탐지(사람, 차량) 수행
4. **결과 필터링**: 신뢰도 90% 이상 결과만 선별, 원본 영상은 폐기(대역폭 절감)
5. **액션 트리거**: 탐지된 객체가 위험 구역 침범 시 즉시 알람 발송 (지연 <50ms)
6. **비동기 업로드**: 탐지 이벤트 메타데이터만 클라우드로 전송, 원본 영상은 로컬 저장 후 야간 전송

### 핵심 코드: 엣지 AI 추론 시스템 (Python + TensorFlow Lite)

```python
import tensorflow as tf
import numpy as np
import cv2
from typing import List, Tuple
import asyncio
import json

class EdgeAIInference:
    """
    엣지 디바이스에서 실행되는 AI 추론 엔진
    - 모델: TFLite 최적화 (INT8 양자화)
    - 하드웨어: Coral Edge TPU 또는 NVIDIA Jetson
    - 목표: 지연 <30ms, 전력 <5W
    """

    def __init__(self, model_path: str, confidence_threshold: float = 0.85):
        # TFLite 모델 로드 (Edge TPU 최적화)
        self.interpreter = tf.lite.Interpreter(
            model_path=model_path,
            experimental_delegates=[tf.lite.experimental.load_delegate('libedgetpu.so.0')]
        )
        self.interpreter.allocate_tensors()

        # 입출력 텐서 정보
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.input_shape = self.input_details[0]['shape'][1:3]  # (224, 224)

        self.confidence_threshold = confidence_threshold
        self.inference_count = 0
        self.total_latency = 0.0

    def preprocess(self, frame: np.ndarray) -> np.ndarray:
        """영상 프레임 전처리 (CPU 기반, <5ms)"""
        # 리사이징
        resized = cv2.resize(frame, self.input_shape)

        # 정규화 (0-255 -> 0-1)
        normalized = resized.astype(np.float32) / 255.0

        # INT8 양자화 모델용 스케일 적용
        input_scale = self.input_details[0]['quantization'][0]
        input_zero_point = self.input_details[0]['quantization'][1]
        quantized = (normalized / input_scale) + input_zero_point

        return quantized.astype(np.uint8)

    def inference(self, preprocessed: np.ndarray) -> Tuple[List[str], List[float], float]:
        """
        AI 추론 실행 (Edge TPU 기반, <20ms)
        Returns: (감지된 클래스 목록, 신뢰도 목록, 추론 지연 시간)
        """
        import time

        start_time = time.perf_counter()

        # 텐서 입력 설정
        self.interpreter.set_tensor(self.input_details[0]['index'], [preprocessed])

        # 추론 실행 (하드웨어 가속)
        self.interpreter.invoke()

        # 결과 추출
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]

        latency = (time.perf_counter() - start_time) * 1000  # ms

        # 신뢰도 임계값 필터링
        detected_classes = []
        detected_scores = []

        for i, score in enumerate(scores):
            if score > self.confidence_threshold:
                class_id = int(classes[i])
                class_name = self._get_class_name(class_id)
                detected_classes.append(class_name)
                detected_scores.append(float(score))

        # 성능 메트릭 업데이트
        self.inference_count += 1
        self.total_latency += latency

        return detected_classes, detected_scores, latency

    def _get_class_name(self, class_id: int) -> str:
        """COCO 데이터셋 클래스 매핑"""
        coco_classes = {
            0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle',
            5: 'bus', 7: 'truck', 16: 'dog', 17: 'cat'
        }
        return coco_classes.get(class_id, f'unknown_{class_id}')

    def get_stats(self) -> dict:
        """성능 통계 반환"""
        avg_latency = self.total_latency / self.inference_count if self.inference_count > 0 else 0
        return {
            'total_inferences': self.inference_count,
            'avg_latency_ms': round(avg_latency, 2),
            'throughput_fps': round(1000 / avg_latency, 1) if avg_latency > 0 else 0
        }


class EdgeCloudOrchestrator:
    """
    엣지-클라우드 협업 오케스트레이터
    - 엣지: 실시간 추론
    - 클라우드: 모델 업데이트, 대규모 분석
    """

    def __init__(self, edge_inference: EdgeAIInference, cloud_endpoint: str):
        self.edge_inference = edge_inference
        self.cloud_endpoint = cloud_endpoint
        self.event_buffer = []
        self.model_version = "v1.0.0"

    async def process_stream(self, video_source: str):
        """실시간 비디오 스트림 처리 메인 루프"""
        cap = cv2.VideoCapture(video_source)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 1. 전처리 (CPU)
            preprocessed = self.edge_inference.preprocess(frame)

            # 2. AI 추론 (Edge TPU)
            classes, scores, latency = self.edge_inference.inference(preprocessed)

            # 3. 결과 기반 즉각 액션 (지연 <50ms)
            if 'person' in classes and scores[classes.index('person')] > 0.9:
                await self._trigger_alarm(frame, classes, scores)

            # 4. 이벤트 버퍼링 (배치 업로드)
            event = {
                'timestamp': time.time(),
                'classes': classes,
                'scores': scores,
                'latency_ms': latency,
                'model_version': self.model_version
            }
            self.event_buffer.append(event)

            # 5. 100개 쌓이면 클라우드 업로드
            if len(self.event_buffer) >= 100:
                await self._upload_to_cloud()

    async def _trigger_alarm(self, frame: np.ndarray, classes: List[str], scores: List[float]):
        """위험 상황 감지 시 즉각 알람 (엣지 로컬)"""
        # GPIO 제어로 경광등/부저 작동
        # 지연: <10ms (클라우드 통신 없음)
        alarm_payload = {
            'type': 'INTRUSION_DETECTED',
            'severity': 'HIGH',
            'detections': list(zip(classes, scores)),
            'timestamp': time.time()
        }
        # 로컬 MQTT 브로커로 즉시 발행
        print(f"[ALARM] {alarm_payload}")

    async def _upload_to_cloud(self):
        """버퍼링된 이벤트 클라우드 업로드 (비동기)"""
        if not self.event_buffer:
            return

        payload = {
            'edge_id': 'edge-001',
            'events': self.event_buffer.copy(),
            'stats': self.edge_inference.get_stats()
        }

        # HTTP POST로 클라우드 전송 (배치)
        # 실제 구현에서는 aiohttp 사용
        print(f"[CLOUD] Uploading {len(self.event_buffer)} events to {self.cloud_endpoint}")

        # 버퍼 클리어
        self.event_buffer.clear()
```

### 엣지 컴퓨팅 성능 메트릭

| 메트릭 | 설명 | 목표 값 | 측정 방법 |
|---|---|---|---|
| **Inference Latency** | AI 모델 추론 시간 | <30ms | time.perf_counter() |
| **End-to-End Latency** | 센서 입력 -> 액션 출력 | <100ms | 전체 파이프라인 측정 |
| **Throughput** | 초당 처리 프레임 | >30 FPS | frame_count / elapsed_time |
| **Bandwidth Savings** | 클라우드 전송 데이터 절감률 | >80% | (raw_size - sent_size) / raw_size |
| **Availability** | 네트워크 단절 시 서비스 지속 | 99.9% | 로컬 자율 동작 |

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 클라우드 vs 엣지 vs 포그 컴퓨팅

| 비교 관점 | Cloud Computing | Edge Computing | Fog Computing | 상세 분석 |
|---|---|---|---|---|
| **처리 위치** | 중앙 데이터센터 | 디바이스 근접 위치 (1 hop) | 엣지-클라우드 중간 계층 | Edge가 가장 가까움 |
| **지연 시간** | 50~200ms | 1~20ms | 10~50ms | 실시간성: Edge > Fog > Cloud |
| **처리 용량** | 무제한 (Petabyte) | 제한적 (GB~TB) | 중간 (TB) | 대규모 분석은 Cloud 필요 |
| **네트워크 의존성** | 100% 의존 | 부분 의존 (오프라인 동작) | 부분 의존 | Edge가 가장 높은 자율성 |
| **하드웨어** | 고성능 서버, GPU | 저전력 ARM, Edge TPU | 중간 성능 x86 | 전력: Edge < Fog < Cloud |
| **데이터 보존** | 영구 저장 | 임시 저장 후 폐기/업로드 | 캐싱 후 선택적 업로드 | 원본 데이터는 Cloud 보관 |
| **관리 복잡성** | 중앙 집중 관리 | 분산 관리 (Orchestration) | 계층별 관리 | Edge가 가장 복잡 |

### 엣지 하드웨어 플랫폼 비교

| 플랫폼 | 프로세서 | AI 성능 | 전력 | 가격 | 적용 분야 |
|---|---|---|---|---|---|
| **NVIDIA Jetson Orin** | ARM Cortex-A78AE + GPU | 275 TOPS | 15-60W | $499-999 | 자율주행, 로봇 |
| **Google Coral Dev Board** | ARM Cortex-A53 + Edge TPU | 4 TOPS | 2-4W | $150 | 스마트홈, 센서 |
| **Intel NCS2** | Movidius VPU | 1 TOPS | 1-2W | $70 | PC 연동 추론 |
| **Raspberry Pi 4 + Coral** | ARM Cortex-A72 + Edge TPU | 4 TOPS | 7W | $100 | 교육, 프로토타입 |
| **AWS Snowball Edge** | Xeon + V100 GPU | 2,800 TOPS | 300W | $수천 | 대규모 엣지 |

### 과목 융합 관점 분석

- **네트워크와의 융합**: 엣지 컴퓨팅은 5G MEC(Multi-access Edge Computing)와 결합하여 무선망 기지국 내에 컴퓨팅 자원을 배치, 1ms 지연을 달성합니다. SD-WAN과 결합하여 엣지-클라우드 간 트래픽을 지능적으로 라우팅합니다.

- **데이터베이스와의 융합**: 엣지에서는 경량 데이터베이스(SQLite, InfluxDB Edge, Redis)를 사용하고, 주기적으로 클라우드 DB(Aurora, BigQuery)와 동기화합니다. 시계열 데이터는 엣지에서 다운샘플링 후 클라우드로 전송합니다.

- **보안과의 융합**: 엣지 디바이스는 물리적 접근 위험이 높으므로, HSM(Hardware Security Module), Secure Boot, TPM(Trusted Platform Module)이 필수입니다. 제로 트러스트 원칙에 따라 모든 엣지-클라우드 통신에 mTLS를 적용합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 스마트 팩토리 불량 탐지 시스템**
- **요구사항**: 컨베이어 벨트의 제품 이미지를 실시간 분석, 불량을 50ms 이내 탐지하여 배출 기구 작동
- **기술사의 의사결정**:
  1. 카메라 옆에 NVIDIA Jetson AGX Orin 설치 (지연 15ms)
  2. YOLOv8 모델 경량화 (INT8 양자화)로 추론 속도 향상
  3. 클라우드는 모델 학습 및 펌웨어 OTA 업데이트만 담당
  4. 네트워크 단절 시에도 100% 로컬 동작 보장
  5. **ROI**: 불량률 3% -> 0.5% 감소, 연간 5억 원 절감

**시나리오 2: 스마트시티 교통 신호 최적화**
- **요구사항**: 교차로 CCTV 영상을 분석하여 실시간 신호 주기 조정, 응급차량 우선 통행
- **기술사의 의사결정**:
  1. 교차로마다 메트로 엣지 서버 설치 (통신사 MEC 활용)
  2. 차량 수/속도 분석은 엣지에서, 전역 패턴 분석은 클라우드에서
  3. V2X(Vehicle-to-Everything) 통신으로 응급차량 위치 수신
  4. 신호 제어는 100ms 루프로 실행 (클라우드 통신 불필요)
  5. **효과**: 평균 통행 시간 20% 단축, 응급차량 도착 시간 30% 단축

**시나리오 3: 소매점 CCTV 스마트 분석**
- **요구사항**: 매장 내 고객 동선 분석, 이상 행동(도난) 탐지, 100개 매장 통합 관제
- **기술사의 의사결정**:
  1. 각 매장에 저가형 엣지 박스(Raspberry Pi + Coral) 설치
  2. 동선 데이터(익명화)만 클라우드로 전송, 원본 영상은 로컬 저장
  3. 중앙 관제는 이상 행동 알람만 수신, 원본 확인은 필요시 스트리밍
  4. **비용 절감**: 기존 클라우드 전송 대비 네트워크 비용 90% 절감

### 도입 시 고려사항 (체크리스트)

**기술적 체크리스트**:
- [ ] 지연 요구사항 명확화: End-to-End 지연 목표(10ms? 100ms?)와 이를 위한 엣지 계층 선택
- [ ] 모델 경량화: 클라우드 모델 그대로 사용 불가, 지식 증류(Knowledge Distillation), 가지치기(Pruning), 양자화(Quantization) 필요
- [ ] 오프라인 동작: 네트워크 단절 시 최소 기능 유지를 위한 로컬 캐시, 폴백 로직
- [ ] OTA 업데이트: 수천 개 엣지 디바이스의 펌웨어/모델 안전한 업데이트 (A/B 파티션, 롤백)

**운영적 체크리스트**:
- [ ] 물리적 보안: 엣지 디바이스의 도난, 변조 방지 (Tamper Detection, 알람)
- [ ] 전력 공급: 정전 대비 UPS, 태양광 등 백업 전원
- [ ] 원격 관제: 무인 환경에서의 재부팅, 로그 수집, 상태 모니터링
- [ ] 수명 주기: 하드웨어 교체 주기(3~5년), 소프트웨어 지원 기간

### 주의사항 및 안티패턴 (Anti-patterns)

1. **모든 것을 엣지로 이동**: 대규모 배치 분석, 머신러닝 학습, 장기 데이터 저장은 여전히 클라우드가 최적. 엣지는 "실시간 + 로컬"에 집중해야 합니다.

2. **하드웨어 과잉 투자**: 최고 사양 엣지 하드웨어를 구매하면 비용 폭증. 실제 워크로드 측정 후 Right-Sizing 필요합니다.

3. **보안 경시**: "내부망이라 안전"은 착각. 엣지 디바이스는 물리적 접근 위험이 높아 클라우드보다 보안이 취약할 수 있습니다.

4. **네트워크 단절 미대비**: 클라우드 통신이 끊기면 엣지 서비스도 마비되는 설계는 치명적. 로컬 자율 모드가 필수입니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | 도입 전 (클라우드 중앙) | 도입 후 (엣지 컴퓨팅) | 개선율 |
|---|---|---|---|
| **응답 지연** | 100~200ms | 10~30ms | 80~90% 감소 |
| **네트워크 대역폭** | 1 Gbps (영상 전송) | 100 Mbps (메타데이터) | 90% 절감 |
| **운영 연속성** | 네트워크 장애 시 중단 | 로컬 자율 동작 | 99.9% 가용성 |
| **프라이버시** | 원본 영상 클라우드 전송 | 로컬 처리 후 메타만 전송 | 규제 준수 100% |
| **전력 소비** | 500W (클라우드+네트워크) | 50W (엣지 디바이스) | 90% 절감 (엣지 기준) |

### 미래 전망 및 진화 방향

1. **AI 추론의 엣지 표준화**: ONNX Runtime, TensorFlow Lite, PyTorch Mobile의 엣지 최적화가 표준화되어, 클라우드에서 학습한 모델을 원클릭으로 엣지 배포가 가능해집니다.

2. **6G와 엣지의 융합**: 6G 네트워크는 엣지 컴퓨팅을 네이티브로 통합, "네트워크가 곧 컴퓨터"가 되어 어디서나 1ms 지연의 컴퓨팅 자원 접근이 가능합니다.

3. **엣지 LLM (Large Language Model)**: 경량화된 LLM(1B~7B 파라미터)이 엣지 디바이스에서 실행되어, 인터넷 연결 없이도 AI 비서, 실시간 번역이 가능해집니다.

4. **디지털 트윈과 엣지**: 물리 세계의 센서 데이터를 엣지에서 실시간으로 디지털 트윈에 반영, 사이버-물리 시스템(CPS)의 제어 루프 지연을 최소화합니다.

### ※ 참고 표준/가이드
- **ETSI GS MEC 003**: Multi-access Edge Computing (MEC) Framework
- **IEEE 1934**: Fog Computing Reference Architecture
- **OpenFog Consortium**: OpenFog Architecture Overview
- **Linux Foundation Edge**: LF Edge Project (Akraino, EdgeX Foundry)

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [포그 컴퓨팅 (Fog Computing)](@/studynotes/13_cloud_architecture/03_virt/fog_computing.md) : 엣지와 클라우드 사이의 중간 계층
- [분산 클라우드 (Distributed Cloud)](@/studynotes/13_cloud_architecture/03_virt/distributed_cloud.md) : CSP가 관리하는 분산 엣지 인프라
- [IoT 아키텍처](@/studynotes/13_cloud_architecture/03_virt/iot_architecture.md) : 엣지 컴퓨팅의 주요 데이터 소스
- [5G MEC (Multi-access Edge Computing)](@/studynotes/13_cloud_architecture/03_virt/5g_mec.md) : 통신사 기반 엣지 플랫폼
- [컨테이너 (Container)](@/studynotes/13_cloud_architecture/01_native/container.md) : 엣지 애플리케이션 배포 단위
- [마이크로서비스 (MSA)](@/studynotes/13_cloud_architecture/01_native/msa.md) : 엣지-클라우드 분산 애플리케이션 아키텍처

---

### 👶 어린이를 위한 3줄 비유 설명
1. 엣지 컴퓨팅은 **'집 안에 작은 두뇌를 두는 것'**과 같아요. 모든 일을 멀리 있는 큰 두뇌(클라우드)에 물어보면 느리니까, 집 안에서 바로 처리할 수 있는 작은 두뇌가 대신 결정해요.
2. 예를 들어 **'똑똑한 화재 경보기'**는 불꽃을 감지하면 멀리 있는 소방서에 물어보지 않고, 즉시 비명을 질러요. 그래서 1초라도 더 빨리 대피할 수 있어요.
3. 나중에 소방서에는 **'불났어요!'**라는 짧은 메시지만 보내요. 전체 영상을 보내면 느리고 비싸니까요.
