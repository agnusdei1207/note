+++
title = "CNN (합성곱 신경망)"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# CNN (Convolutional Neural Network, 합성곱 신경망)

## 핵심 인사이트 (3줄 요약)
> **CNN**은 합성곱 연산으로 이미지의 공간적 특징(엣지→패턴→객체)을 계층적으로 추출하는 딥러닝 아키텍처. LeNet→AlexNet→VGG→ResNet→EfficientNet→ConvNeXt 순으로 발전. 객체 탐지(YOLO)·의료 영상(U-Net)·자율주행 등 실세계 비전 응용의 핵심이다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: CNN(Convolutional Neural Network)은 이미지나 시계열 데이터에서 **공간적 패턴을 학습하는 딥러닝 네트워크**로, 합성곱(Convolution)·풀링(Pooling)·완전연결(FC) 계층을 조합하여 계층적 특징을 추출한다.

> 💡 **비유**: CNN은 **"스캐너로 그림 분석하기"** 같아요. 처음엔 선을 찾고, 다음엔 모서리, 그다음엔 눈코입, 최종엔 얼굴을 인식하죠! 각 단계에서 더 복잡한 패턴을 학습해요.

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - MLP 파라미터 폭발**: 224×224×3 이미지 → 150K 입력, 완전연결 시 파라미터 수천만 개
2. **기술적 필요성 - 공간 정보 보존**: 이미지를 1D로 펼치면 위치 정보 손실 → 합성곱으로 공간 구조 유지
3. **시장/산업 요구 - ImageNet 챌린지**: 2012년 AlexNet이 기존 방식 대비 10%+ 향상, 딥러닝 르네상스 시작

**핵심 목적**: **이미지 공간 계층 특징 학습, 파라미터 효율화 (가중치 공유), 이동 불변성 확보**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**CNN 계층 구조** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CNN 계층별 특징 추출                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   입력 이미지                Conv Layer 1             Conv Layer 2     │
│   ┌─────────────┐          ┌─────────────┐          ┌─────────────┐   │
│   │ ░░▓▓░░░░░░ │          │ ╱╲  ╱╲  ╱╲ │          │  ┌───┐     │   │
│   │ ░░▓▓░░░░░░ │   →      │╱  ╲╱  ╲╱  ╲│   →      │  │ ○ │     │   │
│   │ ░░░░▓▓▓▓░░ │          │▓▓▓▓▓▓▓▓▓▓▓│          │  └───┘     │   │
│   │ ░░░░▓▓▓▓░░ │          │▓▓▓▓▓▓▓▓▓▓▓│          │    ◆       │   │
│   └─────────────┘          └─────────────┘          └─────────────┘   │
│   224×224×3               112×112×64               56×56×128          │
│                                                                         │
│   특징: 픽셀값             특징: 엣지, 선             특징: 패턴, 부품  │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                      CNN 레이어 흐름                             │  │
│   │                                                                 │  │
│   │  Input → Conv → ReLU → Pool → Conv → ReLU → Pool → ... → FC    │  │
│   │    ↓       ↓        ↓      ↓      ↓        ↓      ↓         ↓   │  │
│   │  224×    222×     222×  111×   109×    109×   54×       1000   │  │
│   │  224×3   222×96   ×96   ×96   109×256  ×256   ×256      (클래스)│  │
│   │                                                                 │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│   깊이별 학습 특징:                                                      │
│   Layer 1-2: 엣지, 색상, 그라디언트                                     │
│   Layer 3-4: 텍스처, 곡선, 간단한 패턴                                  │
│   Layer 5-6: 부품 (눈, 코, 입, 바퀴, 창문)                              │
│   Layer 7+:  객체 (얼굴, 자동차, 개, 고양이)                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

[합성곱 연산 상세]

입력: 5×5          필터: 3×3         출력: 3×3
┌───────────────┐   ┌─────────┐   ┌─────────────┐
│ 1  2  3  4  5 │   │ 1  0  1 │   │ 12 16 17   │
│ 5  6  7  8  9 │   │ 0  1  0 │   │ 24 28 29   │
│ 9 10 11 12 13 │ ⊛ │ 1  0  1 │   │ 36 40 41   │
│13 14 15 16 17 │   └─────────┘   └─────────────┘
│17 18 19 20 21 │
└───────────────┘

출력[0,0] = 1×1 + 2×0 + 3×1 + 5×0 + 6×1 + 7×0 + 9×1 + 10×0 + 11×1
         = 1 + 3 + 6 + 9 + 11 = 30  (bias 추가 후 활성화)

공식: output[i,j] = ΣΣ X[i+m, j+n] × W[m,n] + b
                    m n
```

**CNN 핵심 구성요소** (필수: 표):
| 구성 요소 | 역할/기능 | 특징 | 파라미터 |
|----------|----------|------|---------|
| **Convolution** | 특징 추출 | 가중치 공유, 지역 연결 | K²×C_in×C_out |
| **Activation (ReLU)** | 비선형성 | max(0, x) | 0 |
| **Pooling (Max/Avg)** | 공간 축소 | 이동 불변성 강화 | 0 |
| **BatchNorm** | 정규화 | 학습 안정화 | 2×C |
| **Dropout** | 정규화 | 과적합 방지 | 0 |
| **Fully Connected** | 분류 | 최종 예측 | (N+1)×C |
| **Softmax** | 확률 변환 | 클래스 확률 | 0 |

**주요 CNN 아키텍처 진화** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CNN 아키텍처 진화 계보                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1989          2012         2014        2015        2019    2022      │
│    │             │            │           │           │       │         │
│    ▼             ▼            ▼           ▼           ▼       ▼         │
│  LeNet-5      AlexNet      VGG-16     ResNet-152  EfficientNet ConvNeXt│
│    │             │            │           │           │       │         │
│   5층          8층          19층        152층       81층     86층       │
│  60K파라      60M파라      138M파라    60M파라     66M파라   90M파라   │
│                                                                         │
│   우편번호     ImageNet     ImageNet    ImageNet    ImageNet  ImageNet │
│   인식        우승         2위         우승         SOTA     SOTA      │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ 핵심 혁신                                                        │  │
│   ├─────────────────────────────────────────────────────────────────┤  │
│   │ LeNet:    CNN 개념 증명, 가중치 공유                             │  │
│   │ AlexNet:  ReLU, Dropout, GPU 학습, Data Augmentation            │  │
│   │ VGG:      3×3 필터 통일, 깊이 증가                               │  │
│   │ ResNet:   Skip Connection (F(x) + x), 100+층 가능               │  │
│   │ DenseNet: Dense Connection, Feature Reuse                       │  │
│   │ EfficientNet: Compound Scaling (width/depth/resolution)         │  │
│   │ ConvNeXt: ViT 설계 차용 (LayerNorm, GELU, PatchEmbed)           │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│   [ResNet Skip Connection]                                              │
│                                                                         │
│         x ─────────────────────────────┐                               │
│         │                              │                               │
│         ▼                              │                               │
│    ┌─────────┐                         │                               │
│    │ Conv    │                         │                               │
│    │ BN      │                         │                               │
│    │ ReLU    │                         │                               │
│    └────┬────┘                         │                               │
│         │                              │                               │
│         ▼                              │                               │
│    ┌─────────┐                         │                               │
│    │ Conv    │                         │                               │
│    │ BN      │                         │                               │
│    └────┬────┘                         │                               │
│         │                              │                               │
│         └────────────────► [+] ◄───────┘                               │
│                              │                                          │
│                              ▼                                          │
│                           ReLU                                          │
│                              │                                          │
│                              ▼                                          │
│                            F(x) + x                                     │
│                                                                         │
│   효과: 그래디언트 직접 전파, Degradation Problem 해결                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**핵심 알고리즘/공식** (해당 시 필수):
```
[합성곱 출력 크기 계산]

O = (W - K + 2P) / S + 1

W: 입력 크기 (width/height)
K: 필터 크기 (kernel size)
P: 패딩 (padding)
S: 스트라이드 (stride)

예시: 224×224 입력, 3×3 필터, padding=1, stride=1
O = (224 - 3 + 2×1) / 1 + 1 = 224 (크기 유지)

예시: 224×224 입력, 3×3 필터, padding=1, stride=2
O = (224 - 3 + 2×1) / 2 + 1 = 112 (절반 축소)

[풀링 출력 크기]

O = (W - K) / S + 1

Max Pooling 2×2, stride=2: 224 → 112

[파라미터 수 계산]

Conv 파라미터 = K² × C_in × C_out + C_out (bias)

예: 3×3 Conv, 64→128 채널
파라미터 = 9 × 64 × 128 + 128 = 73,856

FC 파라미터 = N_in × N_out + N_out

예: 512 → 1000 클래스
파라미터 = 512 × 1000 + 1000 = 513,000

[수용 영역 (Receptive Field)]

RF_l = RF_{l-1} + (K_l - 1) × ∏_{i=1}^{l-1} S_i

Layer 1 (3×3, s=1): RF = 3
Layer 2 (3×3, s=1): RF = 5
Layer 3 (3×3, s=2): RF = 9
...

깊은 층일수록 더 넓은 영역 볼 수 있음
```

**코드 예시** (필수: Python 순수 구현):
```python
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Callable
from enum import Enum
import math
import random

# ============================================================
# CNN 구현 (순수 Python)
# ============================================================

def relu(x: float) -> float:
    """ReLU 활성화 함수"""
    return max(0, x)

def leaky_relu(x: float, alpha: float = 0.01) -> float:
    """Leaky ReLU"""
    return x if x > 0 else alpha * x

def softmax(x: List[float]) -> List[float]:
    """Softmax 함수"""
    max_x = max(x)
    exp_x = [math.exp(xi - max_x) for xi in x]
    sum_exp = sum(exp_x)
    return [e / sum_exp for e in exp_x]


@dataclass
class Tensor3D:
    """3D 텐서 (채널 × 높이 × 너비)"""
    channels: int
    height: int
    width: int
    data: List[List[List[float]]] = None

    def __post_init__(self):
        if self.data is None:
            self.data = [[[0.0] * self.width
                          for _ in range(self.height)]
                         for _ in range(self.channels)]

    @classmethod
    def zeros(cls, channels: int, height: int, width: int) -> 'Tensor3D':
        return cls(channels, height, width)

    @classmethod
    def random(cls, channels: int, height: int, width: int,
               scale: float = 0.1) -> 'Tensor3D':
        data = [[[random.gauss(0, scale) for _ in range(width)]
                 for _ in range(height)]
                for _ in range(channels)]
        return cls(channels, height, width, data)

    def get(self, c: int, h: int, w: int) -> float:
        return self.data[c][h][w]

    def set(self, c: int, h: int, w: int, val: float) -> None:
        self.data[c][h][w] = val


@dataclass
class Filter:
    """합성곱 필터"""
    in_channels: int
    out_channels: int
    kernel_size: int
    weights: List[List[List[List[float]]]] = None  # [out_c][in_c][h][w]
    bias: List[float] = None

    def __post_init__(self):
        if self.weights is None:
            scale = math.sqrt(2.0 / (self.in_channels * self.kernel_size ** 2))
            self.weights = [
                [[[random.gauss(0, scale) for _ in range(self.kernel_size)]
                  for _ in range(self.kernel_size)]
                 for _ in range(self.in_channels)]
                for _ in range(self.out_channels)
            ]
        if self.bias is None:
            self.bias = [0.0] * self.out_channels


class Conv2D:
    """2D 합성곱 레이어"""

    def __init__(self, in_channels: int, out_channels: int,
                 kernel_size: int, stride: int = 1, padding: int = 0):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.filter = Filter(in_channels, out_channels, kernel_size)

    def forward(self, x: Tensor3D) -> Tensor3D:
        """순전파"""
        # 패딩 적용
        if self.padding > 0:
            x = self._pad(x, self.padding)

        # 출력 크기 계산
        out_h = (x.height - self.kernel_size) // self.stride + 1
        out_w = (x.width - self.kernel_size) // self.stride + 1

        output = Tensor3D.zeros(self.out_channels, out_h, out_w)

        # 합성곱 연산
        for oc in range(self.out_channels):
            for oh in range(out_h):
                for ow in range(out_w):
                    val = 0.0
                    for ic in range(self.in_channels):
                        for kh in range(self.kernel_size):
                            for kw in range(self.kernel_size):
                                ih = oh * self.stride + kh
                                iw = ow * self.stride + kw
                                val += (x.get(ic, ih, iw) *
                                       self.filter.weights[oc][ic][kh][kw])
                    output.set(oc, oh, ow, val + self.filter.bias[oc])

        return output

    def _pad(self, x: Tensor3D, p: int) -> Tensor3D:
        """제로 패딩"""
        new_h = x.height + 2 * p
        new_w = x.width + 2 * p
        padded = Tensor3D.zeros(x.channels, new_h, new_w)
        for c in range(x.channels):
            for h in range(x.height):
                for w in range(x.width):
                    padded.set(c, h + p, w + p, x.get(c, h, w))
        return padded


class MaxPool2D:
    """최대 풀링 레이어"""

    def __init__(self, kernel_size: int = 2, stride: int = 2):
        self.kernel_size = kernel_size
        self.stride = stride

    def forward(self, x: Tensor3D) -> Tensor3D:
        out_h = (x.height - self.kernel_size) // self.stride + 1
        out_w = (x.width - self.kernel_size) // self.stride + 1

        output = Tensor3D.zeros(x.channels, out_h, out_w)

        for c in range(x.channels):
            for oh in range(out_h):
                for ow in range(out_w):
                    max_val = float('-inf')
                    for kh in range(self.kernel_size):
                        for kw in range(self.kernel_size):
                            ih = oh * self.stride + kh
                            iw = ow * self.stride + kw
                            val = x.get(c, ih, iw)
                            if val > max_val:
                                max_val = val
                    output.set(c, oh, ow, max_val)

        return output


class BatchNorm2D:
    """배치 정규화 (단순화: 추론 모드만)"""

    def __init__(self, num_features: int, eps: float = 1e-5):
        self.num_features = num_features
        self.eps = eps
        # 학습된 파라미터 (시뮬레이션)
        self.gamma = [1.0] * num_features
        self.beta = [0.0] * num_features
        self.running_mean = [0.0] * num_features
        self.running_var = [1.0] * num_features

    def forward(self, x: Tensor3D) -> Tensor3D:
        output = Tensor3D.zeros(x.channels, x.height, x.width)

        for c in range(x.channels):
            mean = self.running_mean[c]
            var = self.running_var[c]
            std = math.sqrt(var + self.eps)

            for h in range(x.height):
                for w in range(x.width):
                    normalized = (x.get(c, h, w) - mean) / std
                    output.set(c, h, w,
                              self.gamma[c] * normalized + self.beta[c])

        return output


class ReLU:
    """ReLU 활성화"""

    def forward(self, x: Tensor3D) -> Tensor3D:
        output = Tensor3D.zeros(x.channels, x.height, x.width)
        for c in range(x.channels):
            for h in range(x.height):
                for w in range(x.width):
                    output.set(c, h, w, relu(x.get(c, h, w)))
        return output


class Flatten:
    """평탄화"""

    def forward(self, x: Tensor3D) -> List[float]:
        flat = []
        for c in range(x.channels):
            for h in range(x.height):
                for w in range(x.width):
                    flat.append(x.get(c, h, w))
        return flat


class Linear:
    """완전연결 레이어"""

    def __init__(self, in_features: int, out_features: int):
        self.in_features = in_features
        self.out_features = out_features
        scale = math.sqrt(2.0 / in_features)
        self.weights = [[random.gauss(0, scale) for _ in range(out_features)]
                        for _ in range(in_features)]
        self.bias = [0.0] * out_features

    def forward(self, x: List[float]) -> List[float]:
        output = []
        for j in range(self.out_features):
            val = self.bias[j]
            for i in range(self.in_features):
                val += x[i] * self.weights[i][j]
            output.append(val)
        return output


class ResidualBlock:
    """ResNet 잔차 블록"""

    def __init__(self, channels: int):
        self.conv1 = Conv2D(channels, channels, 3, padding=1)
        self.bn1 = BatchNorm2D(channels)
        self.relu = ReLU()
        self.conv2 = Conv2D(channels, channels, 3, padding=1)
        self.bn2 = BatchNorm2D(channels)

    def forward(self, x: Tensor3D) -> Tensor3D:
        identity = x

        out = self.conv1.forward(x)
        out = self.bn1.forward(out)
        out = self.relu.forward(out)

        out = self.conv2.forward(out)
        out = self.bn2.forward(out)

        # Skip Connection
        for c in range(out.channels):
            for h in range(out.height):
                for w in range(out.width):
                    out.set(c, h, w, out.get(c, h, w) + identity.get(c, h, w))

        out = self.relu.forward(out)
        return out


class SimpleCNN:
    """간단한 CNN 모델"""

    def __init__(self, num_classes: int = 10):
        # 특징 추출부
        self.conv1 = Conv2D(3, 32, 3, padding=1)
        self.bn1 = BatchNorm2D(32)
        self.relu = ReLU()
        self.pool1 = MaxPool2D(2)

        self.conv2 = Conv2D(32, 64, 3, padding=1)
        self.bn2 = BatchNorm2D(64)
        self.pool2 = MaxPool2D(2)

        self.conv3 = Conv2D(64, 128, 3, padding=1)
        self.bn3 = BatchNorm2D(128)
        self.pool3 = MaxPool2D(2)

        self.flatten = Flatten()

        # 분류부
        self.fc1 = Linear(128 * 4 * 4, 256)  # 32x32 → 4x4 after 3 pools
        self.fc2 = Linear(256, num_classes)

    def forward(self, x: Tensor3D) -> List[float]:
        # Conv Block 1
        x = self.conv1.forward(x)
        x = self.bn1.forward(x)
        x = self.relu.forward(x)
        x = self.pool1.forward(x)

        # Conv Block 2
        x = self.conv2.forward(x)
        x = self.bn2.forward(x)
        x = self.relu.forward(x)
        x = self.pool2.forward(x)

        # Conv Block 3
        x = self.conv3.forward(x)
        x = self.bn3.forward(x)
        x = self.relu.forward(x)
        x = self.pool3.forward(x)

        # Flatten & FC
        flat = self.flatten.forward(x)
        fc1_out = [relu(v) for v in self.fc1.forward(flat)]
        logits = self.fc2.forward(fc1_out)

        return logits

    def predict(self, x: Tensor3D) -> int:
        """클래스 예측"""
        logits = self.forward(x)
        return logits.index(max(logits))

    def predict_proba(self, x: Tensor3D) -> List[float]:
        """클래스 확률"""
        logits = self.forward(x)
        return softmax(logits)


class YOLOv8Detector:
    """YOLO 스타일 객체 탐지기 (시뮬레이션)"""

    def __init__(self, num_classes: int = 80):
        self.num_classes = num_classes
        self.anchor_boxes = [
            (10, 13), (16, 30), (33, 23),
            (30, 61), (62, 45), (59, 119),
            (116, 90), (156, 198), (373, 326)
        ]

    def detect(self, image: Tensor3D,
               confidence_threshold: float = 0.5) -> List[dict]:
        """객체 탐지 (시뮬레이션)"""
        # 실제로는 CNN 백본 + 헤드 통과
        detections = []

        # 시뮬레이션: 랜덤 박스 생성
        num_detections = random.randint(0, 5)
        for _ in range(num_detections):
            conf = random.random()
            if conf > confidence_threshold:
                detections.append({
                    'bbox': [
                        random.randint(0, image.width - 100),
                        random.randint(0, image.height - 100),
                        random.randint(50, 150),
                        random.randint(50, 150)
                    ],
                    'confidence': conf,
                    'class': random.randint(0, self.num_classes - 1)
                })

        # NMS (Non-Maximum Suppression) 시뮬레이션
        detections = self._nms(detections)
        return detections

    def _nms(self, detections: List[dict], iou_threshold: float = 0.5) -> List[dict]:
        """Non-Maximum Suppression"""
        if not detections:
            return []

        # 신뢰도 기준 정렬
        detections.sort(key=lambda x: x['confidence'], reverse=True)

        keep = []
        while detections:
            best = detections.pop(0)
            keep.append(best)

            # IoU 계산 후 제거
            remaining = []
            for det in detections:
                iou = self._compute_iou(best['bbox'], det['bbox'])
                if iou < iou_threshold:
                    remaining.append(det)
            detections = remaining

        return keep

    def _compute_iou(self, box1: List[int], box2: List[int]) -> float:
        """IoU 계산"""
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2

        # 교집합
        xi1 = max(x1, x2)
        yi1 = max(y1, y2)
        xi2 = min(x1 + w1, x2 + w2)
        yi2 = min(y1 + h1, y2 + h2)

        if xi2 <= xi1 or yi2 <= yi1:
            return 0.0

        inter = (xi2 - xi1) * (yi2 - yi1)
        union = w1 * h1 + w2 * h2 - inter

        return inter / union if union > 0 else 0.0


# ============================================================
# 사용 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("         CNN (합성곱 신경망) 구현 데모")
    print("=" * 60)

    # 1. 기본 합성곱 연산
    print("\n1. 합성곱 연산")
    print("-" * 40)

    # 32×32×3 입력 이미지 생성
    input_image = Tensor3D.random(3, 32, 32)
    print(f"입력: {input_image.channels}×{input_image.height}×{input_image.width}")

    # Conv 레이어
    conv = Conv2D(3, 32, 3, padding=1)
    conv_out = conv.forward(input_image)
    print(f"Conv(3→32, 3×3) 출력: {conv_out.channels}×{conv_out.height}×{conv_out.width}")

    # ReLU
    relu_layer = ReLU()
    relu_out = relu_layer.forward(conv_out)
    print(f"ReLU 출력: {relu_out.channels}×{relu_out.height}×{relu_out.width}")

    # Max Pooling
    pool = MaxPool2D(2)
    pool_out = pool.forward(relu_out)
    print(f"MaxPool(2×2) 출력: {pool_out.channels}×{pool_out.height}×{pool_out.width}")

    # 2. 전체 CNN 모델
    print("\n\n2. 전체 CNN 분류 모델")
    print("-" * 40)

    model = SimpleCNN(num_classes=10)

    # 32×32 RGB 이미지 입력
    test_image = Tensor3D.random(3, 32, 32)
    print(f"입력 이미지: {test_image.height}×{test_image.width}×{test_image.channels}")

    # 예측
    logits = model.forward(test_image)
    probs = softmax(logits)
    predicted_class = logits.index(max(logits))

    print(f"로짓: {[f'{l:.2f}' for l in logits[:5]]}...")
    print(f"확률: {[f'{p:.3f}' for p in probs[:5]]}...")
    print(f"예측 클래스: {predicted_class} (신뢰도: {probs[predicted_class]:.2%})")

    # 3. ResNet 스타일 Skip Connection
    print("\n\n3. ResNet 잔차 블록")
    print("-" * 40)

    res_block = ResidualBlock(64)
    res_input = Tensor3D.random(64, 16, 16)
    res_output = res_block.forward(res_input)

    print(f"입력: {res_input.channels}×{res_input.height}×{res_input.width}")
    print(f"출력: {res_output.channels}×{res_output.height}×{res_output.width}")
    print("Skip Connection: F(x) + x 형태로 정보 보존")

    # 4. YOLO 객체 탐지 시뮬레이션
    print("\n\n4. YOLO 객체 탐지 시뮬레이션")
    print("-" * 40)

    detector = YOLOv8Detector(num_classes=80)
    test_img = Tensor3D.random(3, 416, 416)

    detections = detector.detect(test_img, confidence_threshold=0.5)
    print(f"탐지된 객체: {len(detections)}개")

    for i, det in enumerate(detections):
        bbox, conf, cls = det['bbox'], det['confidence'], det['class']
        print(f"  객체 {i+1}: bbox={bbox}, conf={conf:.2f}, class={cls}")

    print("\n" + "=" * 60)
    print("CNN의 핵심:")
    print("1. 합성곱: 공간적 특징 추출 (가중치 공유)")
    print("2. 풀링: 공간 축소 + 이동 불변성")
    print("3. Skip Connection: 깊은 네트워크 학습 가능")
    print("=" * 60)
