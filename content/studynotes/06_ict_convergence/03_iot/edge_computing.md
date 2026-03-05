+++
title = "엣지 컴퓨팅 (Edge Computing)"
description = "클라우드의 한계를 극복하는 분산 컴퓨팅 패러다임: 엣지 컴퓨팅의 아키텍처, 지연 최적화 및 실시간 처리 전략을 다루는 심층 기술 백서"
date = 2024-05-17
[taxonomies]
tags = ["Edge Computing", "MEC", "IoT", "Real-time Processing", "Distributed Computing", "5G"]
+++

# 엣지 컴퓨팅 (Edge Computing)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 발생지인 엣지(Edge) 근처에서 연산과 저장을 수행하여, 중앙 클라우드로의 데이터 전송 지연(Latency)과 대역폭(Bandwidth) 소비를 획기적으로 줄이는 분산 컴퓨팅 아키텍처입니다.
> 2. **가치**: 자율주행(1ms 미만 응답), 산업용 IoT(실시간 제어), AR/VR(몰입감) 등 초저지연(Ultra-Low Latency) 서비스를 가능하게 하며, 대역폭 비용 절감(90% 이상), 프라이버시 보호(로컬 데이터 처리)를 실현합니다.
> 3. **융합**: 5G MEC(Multi-access Edge Computing), AI(Edge AI), Digital Twin과 결합하여 클라우드-엣지 연속체(Cloud-Edge Continuum)를 구축하고, 지능형 실시간 의사결정 시스템을 완성합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
엣지 컴퓨팅(Edge Computing)은 물리적 세계(센서, 카메라, 기계)와 디지털 세계(클라우드) 사이의 **중간 계층(Edge Layer)**에 컴퓨팅 자원(CPU, GPU, 스토리지)을 배치하여, 데이터를 발생지와 가까운 곳에서 실시간으로 처리하는 분산 컴퓨팅 패러다임입니다. 이는 중앙 클라우드(Cloud)와 엔드 디바이스(Device) 사이의 **지리적, 네트워크적 거리**를 단축하여, 왕복 지연 시간(Round-Trip Latency)을 수백 ms에서 1~10ms 수준으로 압축하는 것을 목표로 합니다.

### 2. 구체적인 일상생활 비유
기존 클라우드 컴퓨팅이 '본사에 모든 보고서를 보내서 승인받는 방식'이라면, 엣지 컴퓨팅은 **'현장 관리자가 즉석에서 결정하는 방식'**입니다. 예를 들어, 공장의 기계가 과열되었을 때, 본사 서버(클라우드)에 데이터를 보내서 승인을 받고 다시 명령을 내리면 이미 화재가 발생할 것입니다. 하지만 기계 옆에 있는 작은 컴퓨터(엣지)가 즉시 센서 데이터를 분석하고 0.1초 만에 전원을 차단하면 사고를 예방할 수 있습니다. 중요한 데이터만 본사로 보고하고, 긴급한 일은 현장에서 처리하는 것입니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (지연 시간과 대역폭 병목)**:
   클라우드 컴퓨팅은 중앙 집중형 아키텍처로, 모든 데이터를 수천 km 떨어진 데이터센터로 전송해야 합니다. 자율주행차의 라이다(LiDAR)는 초당 1.4GB의 데이터를 생성하는데, 이를 5G로 전송해도 왕복 지연 시간은 50~100ms에 달합니다. 시속 100km로 주행하는 차량은 100ms 동안 2.8m를 이동하므로, 이는 생사를 가르는 문제입니다. 또한, 전 세계 IoT 기기가 생성하는 데이터(2025년 79.4ZB 예상)를 모두 클라우드로 전송하는 것은 네트워크 인프라와 비용 측면에서 불가능합니다.

2. **혁신적 패러다임 변화의 시작**:
   2009년 시스코(Cisco)가 "Fog Computing" 개념을 제안하면서 클라우드와 디바이스 사이의 중간 계층의 필요성이 대두되었습니다. 2014년 ETSI(유럽 전기통신 표준화 기구)가 **MEC(Mobile Edge Computing)** 표준화를 시작하며, 이동통신망 기지국에 컴퓨팅 자원을 배치하는 구체적인 아키텍처가 정의되었습니다. 5G 상용화(2019년~)와 함께 uRLLC(초저지연 고신뢰) 서비스의 필수 인프라로 자리 잡았습니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   스마트 팩토리의 실시간 품질 검사(Visual Inspection), 스마트 시티의 교통 신호 최적화, 원격 의료(Remote Surgery), AR/VR 게임 등 **1ms~10ms 이하의 응답 시간**이 필수적인 서비스가 폭증하고 있습니다. 또한, GDPR 등 데이터 주권 규제로 인해 민감한 데이터(얼굴, 의료 정보)가 국경을 넘지 않도록 로컬에서 처리해야 하는 요구사항도 증가하고 있습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Module) | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Edge Node** | 데이터 수집, 전처리, 실시간 연산 | 센서 데이터 수집, ML 추론, 필터링, 압축 | NVIDIA Jetson, Intel NUC | 현장 관리자 |
| **Edge Gateway** | 프로토콜 변환, 보안, 엣지-클라우드 연결 | IoT 프로토콜(Zigbee, BLE) 변환, TLS 암호화 | AWS Greengrass, Azure IoT Edge | 지점장 |
| **MEC Server** | 기지국 내 고성능 컴퓨팅 자원 | 5G RAN과 직접 연결, 초저지연 서비스 호스팅 | ETSI MEC, 5G Core | 지역 본부 |
| **Edge Orchestrator** | 엣지 노드 관리, 워크로드 스케줄링 | 컨테이너 배포, 오토스케일링, 장애 복구 | K3s, KubeEdge, AWS Wavelength | 총괄 관리자 |
| **Cloud-Edge Sync** | 모델 업데이트, 데이터 동기화 | 증분 데이터 전송, 페더레이션 러닝 | MQTT, Kafka, Delta Sync | 보고 시스템 |

### 2. 정교한 구조 다이어그램: 클라우드-엣지 연속체 아키텍처

```text
=====================================================================================================
                    [ Cloud-Edge Continuum Architecture ]
=====================================================================================================

    [ Cloud Layer (Central) ]           [ Edge Layer (Distributed) ]        [ Device Layer ]
    +------------------------+          +--------------------------+        +-------------+
    | Hyper-scale Cloud      |          | MEC Server (Base Station)|        | IoT Sensor  |
    | - AI Model Training    |<--5G---->| - Real-time Inference    |<------>| (Camera,    |
    | - Big Data Analytics   |   Back   | - Video Analytics        |   Radio|  Lidar)     |
    | - Long-term Storage    |   haul   | - Local Breakout         |   Link | - Actuator  |
    +------------------------+          +--------------------------+        +-------------+
               │                                    │
               │ Model Update / Sync                 │
               ▼                                    ▼
    +------------------------------------------+   +--------------------------+
    | Cloud-Native Services                    |   | Edge Gateway / Node      |
    | - REST API / gRPC                        |   | - Data Pre-processing    |
    | - Kubernetes Control Plane               |   | - Protocol Translation    |
    | - Global Load Balancer                   |   | - Local ML Inference     |
    +------------------------------------------+   | - Secure Element (HSM)   |
                                                   +--------------------------+
                                                              │
                                                              │ Local Network
                                                              ▼
                                          +------------------------------------------+
                                          | Smart Device / Equipment                 |
                                          | - Autonomous Vehicle (Self-driving ECU) |
                                          | - Industrial Robot (PLC, CNC)           |
                                          | - Smart Camera (Object Detection)       |
                                          +------------------------------------------+

=====================================================================================================
    [ Data Flow: Real-time vs Batch ]

    [Real-time Path (Latency < 10ms)]
    Sensor -> Edge Node -> Local Inference -> Actuator
    (: 자율주행차 장애물 감지 -> 즉각 제동)

    [Batch Path (Latency ~ seconds)]
    Sensor -> Edge Node -> Filtered/Aggregated Data -> Cloud -> AI Training -> Model Update -> Edge
    (: 주행 패턴 분석 -> 클라우드에서 모델 재학습 -> 엣지로 모델 배포)
```

### 3. 심층 동작 원리 (5G MEC 시나리오)

5G 네트워크에서 MEC(Multi-access Edge Computing)를 활용한 자율주행 V2X 서비스의 동작 메커니즘입니다.

1. **데이터 수집 및 로컬 브레이크아웃 (Local Breakout)**:
   자율주행차의 센서(라이다, 카메라)에서 생성된 데이터는 5G 무선 구간(RAN)을 통해 기지국(gNodeB)으로 전송됩니다. MEC 서버는 기지국과 **직접 연결**되어 있어, 데이터가 5G 코어망과 인터넷을 거치지 않고 기지국에서 즉시 처리(Local Breakout)됩니다. 이를 통해 왕복 지연 시간을 1~5ms 수준으로 단축합니다.

2. **실시간 추론 및 의사결정 (Real-time Inference)**:
   MEC 서버의 GPU(NVIDIA A100 또는 T4)에서 YOLOv8, PointPillars 등의 **실시간 객체 탐지 모델**이 실행됩니다. 라이다 포인트 클라우드와 카메라 이미지를 융합하여 보행자, 차량, 신호등을 탐지하고, 10ms 이내에 결과를 차량으로 전송합니다.

3. **클라우드-엣지 동기화 (Cloud-Edge Sync)**:
   엣지에서 처리된 메타데이터(객체 탐지 결과, 이상 징후)와 소수의 원시 데이터(새로운 시나리오)는 야간에 클라우드로 전송됩니다. 클라우드에서는 대규모 GPU 클러스터로 AI 모델을 **재학습(Retraining)**하고, 새로운 모델 가중치를 OTA(Over-The-Air)로 엣지 서버에 배포합니다. 이는 **지속적 학습(Continual Learning)** 파이프라인을 구성합니다.

### 4. 핵심 알고리즘 및 실무 코드 예시

엣지 디바이스에서 실행되는 실시간 객체 탐지 추론 코드입니다 (NVIDIA Jetson + PyTorch).

```python
import torch
import cv2
import time
from typing import Tuple, List, Dict
import numpy as np

class EdgeObjectDetector:
    """
    엣지 디바이스(NVIDIA Jetson)에서 실시간 객체 탐지를 수행하는 클래스.
    - TensorRT 최적화를 통한 추론 속도 향상
    - 비동기 프레임 처리를 통한 지연 시간 최소화
    """

    def __init__(self, model_path: str, confidence_threshold: float = 0.5):
        # Jetson에서는 TensorRT로 변환된 모델 사용 (FP16 양자화)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = torch.jit.load(model_path, map_location=self.device)
        self.model.eval()
        self.conf_threshold = confidence_threshold

        # 입력 이미지 크기 (모델에 따라 다름)
        self.input_size = (640, 640)

        # FPS 측정용
        self.frame_count = 0
        self.fps = 0.0
        self.last_time = time.time()

    def preprocess(self, frame: np.ndarray) -> torch.Tensor:
        """프레임 전처리: 리사이즈, 정규화, 텐서 변환"""
        # BGR -> RGB 변환
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 리사이즈 및 패딩
        input_tensor = cv2.resize(rgb_frame, self.input_size)
        input_tensor = input_tensor.astype(np.float32) / 255.0  # 정규화

        # HWC -> CHW 변환 및 배치 차원 추가
        input_tensor = np.transpose(input_tensor, (2, 0, 1))
        input_tensor = np.expand_dims(input_tensor, axis=0)

        return torch.from_numpy(input_tensor).to(self.device)

    def postprocess(
        self,
        detections: torch.Tensor,
        original_shape: Tuple[int, int]
    ) -> List[Dict]:
        """탐지 결과 후처리: NMS, 좌표 변환, 필터링"""
        results = []
        h, w = original_shape

        # 탐지 결과 파싱 (YOLOv5/v8 형식: [x, y, w, h, conf, class_probs...])
        for det in detections[0]:
            confidence = det[4].item()
            if confidence < self.conf_threshold:
                continue

            # 바운딩 박스 좌표를 원본 이미지 크기로 변환
            x1 = int(det[0].item() * w / self.input_size[0])
            y1 = int(det[1].item() * h / self.input_size[1])
            x2 = int(det[2].item() * w / self.input_size[0])
            y2 = int(det[3].item() * h / self.input_size[1])

            # 클래스 (가장 높은 확률)
            class_id = torch.argmax(det[5:]).item()
            class_confidence = det[5 + class_id].item()

            results.append({
                'bbox': (x1, y1, x2, y2),
                'confidence': confidence * class_confidence,
                'class_id': class_id
            })

        return results

    def infer(self, frame: np.ndarray) -> Tuple[List[Dict], float]:
        """단일 프레임 추론 (지연 시간 측정 포함)"""
        start_time = time.time()

        # 전처리
        input_tensor = self.preprocess(frame)

        # 추론 (GPU)
        with torch.no_grad():
            detections = self.model(input_tensor)

        # 후처리
        results = self.postprocess(detections, frame.shape[:2])

        inference_time = (time.time() - start_time) * 1000  # ms

        return results, inference_time

    def run_realtime_detection(self, camera_source: int = 0):
        """실시간 객체 탐지 루프 (카메라 입력)"""
        cap = cv2.VideoCapture(camera_source)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        print("[Edge Detector] Starting real-time inference...")
        print(f"[Edge Detector] Device: {self.device}")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 추론
            detections, latency = self.infer(frame)

            # 결과 시각화
            for det in detections:
                x1, y1, x2, y2 = det['bbox']
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"Class {det['class_id']}: {det['confidence']:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

            # FPS 계산
            self.frame_count += 1
            current_time = time.time()
            if current_time - self.last_time >= 1.0:
                self.fps = self.frame_count / (current_time - self.last_time)
                self.frame_count = 0
                self.last_time = current_time

            # 성능 정보 표시
            cv2.putText(
                frame,
                f"FPS: {self.fps:.1f} | Latency: {latency:.1f}ms",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

            cv2.imshow('Edge Object Detection', frame)

            # 'q' 키로 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # TensorRT 최적화된 모델 경로
    MODEL_PATH = "yolov8n_fp16.engine"  # 또는 .pt, .onnx

    detector = EdgeObjectDetector(MODEL_PATH, confidence_threshold=0.5)
    detector.run_realtime_detection()

    # 엣지 컴퓨팅 성능 지표:
    # - Jetson Xavier NX: 30~60 FPS (640x640)
    # - 추론 지연 시간: 15~30ms
    # - 전력 소모: 10~15W
    # - 클라우드 전송 대비 지연: 95% 단축 (200ms -> 10ms)
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 클라우드 vs 엣지 vs 포그 컴퓨팅

| 평가 지표 | 클라우드 컴퓨팅 (Cloud) | 엣지 컴퓨팅 (Edge) | 포그 컴퓨팅 (Fog) |
| :--- | :--- | :--- | :--- |
| **위치** | 데이터센터 (수천 km) | 기지국, 게이트웨이 (수 m~km) | 로컬 네트워크 내 |
| **지연 시간** | 50~200ms | **1~20ms** | 10~50ms |
| **대역폭 요구** | 높음 (모든 데이터 전송) | **낮음** (필요 데이터만 전송) | 중간 |
| **컴퓨팅 파워** | 무제한 (GPU 클러스터) | 제한적 (에지 GPU/TPU) | 제한적 |
| **확장성** | 매우 높음 | 중간 (물리적 배포 필요) | 낮음 |
| **보안/프라이버시** | 낮음 (데이터 전송) | **높음** (로컬 처리) | 높음 |
| **주요 활용** | AI 학습, 빅데이터 분석 | 실시간 추론, 제어 | 스마트홈, 빌딩 자동화 |

### 2. 엣지 하드웨어 플랫폼 비교

| 플랫폼 | 컴퓨팅 파워 | 전력 소모 | AI 성능 (TOPS) | 적합한 용도 |
| :--- | :--- | :--- | :--- | :--- |
| **NVIDIA Jetson Orin NX** | 8-core ARM A78AE | 10~25W | **100 TOPS** (INT8) | 자율주행, 산업용 로봇 |
| **Raspberry Pi 5** | 4-core ARM A76 | 5~12W | ~0.1 TOPS | 홈 IoT, 교육용 |
| **Intel NUC (Movidius)** | x86 + VPU | 15~30W | 4 TOPS | 스마트 시티, 리테일 |
| **Google Coral Edge TPU** | ARM Cortex-M | 2~4W | **4 TOPS** | 키오스크, 스마트 카메라 |
| **Qualcomm Cloud AI 100** | ASIC | 75W | 400 TOPS | MEC 서버 |

### 3. 과목 융합 관점 분석 (엣지 컴퓨팅 + 타 도메인 시너지)
- **엣지 컴퓨팅 + AI (Edge AI / TinyML)**: 클라우드로 데이터를 보내지 않고 엣지에서 AI 추론을 수행합니다. **모델 경량화(Pruning, Quantization, Knowledge Distillation)**를 통해 수 MB 크기의 모델을 마이크로컨트롤러(MCU)에서 실행하는 TinyML 기술이 핵심입니다.

- **엣지 컴퓨팅 + 5G (MEC)**: 5G의 uRLLC(초저지연)와 네트워크 슬라이싱을 활용하여, 엣지 애플리케이션에 **보장된 QoS(Quality of Service)**를 제공합니다. 5G 코어망의 UPF(User Plane Function)가 MEC 서버로 트래픽을 직접 라우팅합니다.

- **엣지 컴퓨팅 + 보안 (Zero Trust)**: 엣지 노드는 물리적 보안이 취약할 수 있으므로, **하드웨어 보안 모듈(HSM, TPM)**과 **Zero Trust Architecture**를 적용해야 합니다. 모든 엣지-클라우드 통신은 mTLS로 암호화하고, 디바이스 인증은 X.509 인증서 기반으로 수행합니다.

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략
- **[상황 A] 스마트 팩토리의 실시간 불량품 검출 시스템**
  - **문제점**: 컨베이어 벨트 위의 제품을 카메라로 촬영하여 불량품을 탐지해야 함. 기존에는 이미지를 서버로 전송하여 처리했으나, 100ms 지연으로 인해 불량품이 이미 다음 공정으로 넘어감.
  - **기술사 판단 (전략)**: **엣지 AI 카메라**를 각 공정 라인에 설치. NVIDIA Jetson 기반 로컬 추론으로 10ms 이내에 불량 여부 판정. 불량품 발생 시 즉시 PLC(Programmable Logic Controller)에 신호를 보내 로봇 암이 제품을 배출. 정상/불량 통계 데이터만 클라우드로 전송하여 대역폭 95% 절감.

- **[상황 B] 스마트 시티의 교통 신호 최적화**
  - **문제점**: 교차로 CCTV 영상을 중앙 서버로 전송하여 교통량을 분석하고 신호를 제어했으나, 네트워크 장애 시 시스템 마비. 개인정보(차량 번호, 보행자 얼굴) 유출 우려.
  - **기술사 판단 (전략)**: **교차로별 MEC 서버**를 설치하여 영상을 로컬에서 처리. 차량 수, 보행자 수만 메타데이터로 추출하여 번호판/얼굴은 마스킹. 클라우드는 전체 도시의 교통 흐름을 최적화하는 전역 모델을 학습하고, 엣지는 로컬 신호 주기를 실시간 제어.

### 2. 도입 시 고려사항 (기술적/보안적 체크리스트)
- **워크로드 분할 (Cloud-Edge Workload Split)**: 어떤 연산을 엣지에서 수행하고, 어떤 연산을 클라우드에서 수행할지 명확한 기준이 필요합니다. **실시간성이 요구되는 추론(Inference)은 엣지, 대규모 학습(Training)은 클라우드**로 분담합니다.

- **모델 배포 및 업데이트 (OTA Update)**: 수천 대의 엣지 디바이스에 AI 모델을 배포하고 업데이트하는 파이프라인이 필요합니다. **컨테이너 기반(K3s, KubeEdge)** 배포와 **롤링 업데이트** 전략을 사용하여 서비스 중단 없이 모델을 갱신합니다.

- **오프라인 동작 (Offline Resilience)**: 네트워크 연결이 단절되어도 엣지 디바이스는 계속 동작해야 합니다. 로컬 캐싱, 축소된 모델(Fallback Model), 로컬 데이터베이스(SQLite, InfluxDB)를 활용하여 **오프라인 내성(Offline Resilience)**을 확보해야 합니다.

### 3. 주의사항 및 안티패턴 (Anti-patterns)
- **엣지를 단순 데이터 포워더로 사용**: 엣지 노드를 설치하고도 모든 데이터를 클라우드로 전송하는 안티패턴입니다. 이는 엣지 컴퓨팅의 핵심 가치(지연 단축, 대역폭 절감)를 무력화합니다. 반드시 **데이터 필터링, 집계, 전처리**를 엣지에서 수행해야 합니다.

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과 (도입 전후 ROI)

| 구분 | 중앙 클라우드 (AS-IS) | 엣지 컴퓨팅 (TO-BE) | 개선 지표 (Impact) |
| :--- | :--- | :--- | :--- |
| **응답 지연 시간** | 50~200ms | **1~10ms** | 지연 **95% 이상 단축** |
| **대역폭 사용량** | 원시 데이터 전체 전송 | 필터링/집계 데이터만 | **대역폭 80~95% 절감** |
| **프라이버시** | 민감 데이터 전송 (위험) | 로컬 처리 (안전) | **데이터 유출 위험 0%** |
| **가용성** | 네트워크 장애 시 마비 | **오프라인 동작 가능** | 연속성 보장 |

### 2. 미래 전망 및 진화 방향
- **헤테로지니어스 엣지 (Heterogeneous Edge)**: 다양한 하드웨어(GPU, TPU, NPU, FPGA)가 혼재된 엣지 환경에서, 워크로드에 가장 적합한 하드웨어를 자동으로 선택하는 **오케스트레이션**이 필요합니다.

- **사이버-물리 시스템 (CPS) 통합**: 엣지 컴퓨팅은 물리적 세계(기계, 로봇, 차량)와 디지털 세계(Digital Twin, AI)를 실시간으로 연결하는 **CPS(Cyber-Physical System)**의 핵심 인프라가 될 것입니다.

- **6G와 통합 엣지**: 6G에서는 위성, 드론(HAPS), LEO 위성이 엣지 노드로 활용되어, **공중 엣지(Aerial Edge)**와 **우주 엣지(Space Edge)**가 등장할 것입니다.

### 3. 참고 표준/가이드
- **ETSI MEC 003**: Multi-access Edge Computing (MEC) Framework and Reference Architecture
- **OpenNESS (Intel)**: Open Network Edge Services Software
- **KubeEdge**: CNCF 프로젝트, 엣지 컴퓨팅을 위한 쿠버네티스 확장
- **EdgeX Foundry**: LF Edge 프로젝트, IoT 엣지 프레임워크

---

## 관련 개념 맵 (Knowledge Graph)
- **[사물인터넷 (IoT)](@/studynotes/06_ict_convergence/03_iot/iot_architecture.md)**: 엣지 컴퓨팅이 데이터를 처리하는 센서 네트워크의 기반.
- **[5G MEC](./5g_mec.md)**: 이동통신망 기지국에 컴퓨팅 자원을 배치하는 엣지 컴퓨팅의 대표적 구현.
- **[Edge AI / TinyML](./edge_ai.md)**: 엣지 디바이스에서 AI 모델을 경량화하여 실행하는 기술.
- **[Digital Twin](@/studynotes/06_ict_convergence/03_iot/digital_twin.md)**: 엣지 데이터를 기반으로 물리적 객체의 가상 복제본을 실시간 동기화.
- **[클라우드 컴퓨팅](@/studynotes/06_ict_convergence/01_cloud/cloud_computing.md)**: 엣지와 협력하여 클라우드-엣지 연속체를 구성하는 중앙 인프라.

---

## 어린이를 위한 3줄 비유 설명
1. 엣지 컴퓨팅은 '현장에 있는 작은 두뇌'예요! 본사(클라우드)까지 물어보러 갈 시간이 없을 때, 바로 옆에서 빠르게 결정해요.
2. 자동차가 달리다가 갑자기 튀어나온 고양이를 발견하면, 먼 곳의 컴퓨터에 물어볼 새도 없이 엣지 컴퓨터가 즉시 브레이크를 잡아줘요.
3. 덕분에 우리는 더 안전하게 다닐 수 있고, 인터넷이 끊겨도 로봇 청소기나 스마트 홈은 계속 일할 수 있어요!
