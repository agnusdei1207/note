+++
title = "디지털 트윈 (Digital Twin)"
description = "물리 세계의 가상 복제: 디지털 트윈 기술의 아키텍처, 실시간 동기화 및 시뮬레이션 전략을 다루는 심층 기술 백서"
date = 2024-05-19
[taxonomies]
tags = ["Digital Twin", "IoT", "Simulation", "CPS", "Smart Manufacturing", "Real-time Sync"]
+++

# 디지털 트윈 (Digital Twin)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 물리적 객체(제품, 기계, 건물, 도시)의 형상, 동작, 상태를 디지털 공간에 1:1로 복제하여 실시간 데이터 동기화, 시뮬레이션, 예측 분석을 수행하는 가상 모델입니다.
> 2. **가치**: 설비 고장 사전 예측(예지 보전), 제품 설계 최적화, 운영 효율 극대화를 통해 유지보수 비용 30% 절감, 가동률 20% 향상, 제품 개발 기간 50% 단축을 실현합니다.
> 3. **융합**: IoT 센서, 5G/엣지 컴퓨팅, AI/ML, AR/VR, 클라우드와 결합하여 스마트 팩토리, 스마트 시티, 헬스케어, 자율주행 등 다양한 산업의 디지털 전환(DX) 핵심 기술로 활용됩니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
디지털 트윈(Digital Twin)은 2002년 미시간 대학교 마이클 그리브스(Michael Grieves) 교가가 처음 제안한 개념으로, **"물리적 제품의 가상 복제본"**을 의미합니다. 이는 단순한 3D CAD 모델을 넘어, 실시간 센서 데이터와 연결되어 물리적 객체의 현재 상태, 과거 이력, 미래 동작을 모두 시뮬레이션할 수 있는 **동적(Dynamic) 가상 모델**입니다. 디지털 트윈은 **물리 공간(Physical Space)**, **가상 공간(Virtual Space)**, 그리고 이 둘을 연결하는 **데이터 링크(Data Link)**의 3요소로 구성됩니다.

### 2. 구체적인 일상생활 비유
디지털 트윈은 '실시간 업데이트되는 미러 하우스'입니다. 당신이 거실에서 소파를 옮기면, 거울 속의 방(디지털 트윈)도 즉시 똑같이 변합니다. 하지만 이 거울은 단순히 비추기만 하는 것이 아니라, "소파를 저 위치에 두면 햇빛이 잘 들어오지만, 여름에는 너무 더워질 거예요"라고 예측합니다. 공장의 기계가 과열되면 디지털 트윈이 "3일 후에 베어링이 고장날 확률이 85%"라고 경고합니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (사후 대응과 시뮬레이션 단절)**:
   전통적인 유지보수는 설비가 고장 난 후 수리하는 **사후 정비(Reactive Maintenance)**나, 정해진 주기마다 교체하는 **예방 정비(Preventive Maintenance)**에 의존했습니다. 이는 불필요한 부품 교체 비용이나 돌발 고장으로 인한 생산 중단 손실을 야기했습니다. 또한, 설계 단계의 시뮬레이션(CAE)과 실제 운영 데이터가 단절되어 있었습니다.

2. **혁신적 패러다임 변화의 시작**:
   NASA는 1960년대부터 우주선의 상태를 지상에서 모니터링하고 시뮬레이션하는 기술을 사용했습니다. 2002년 제품 수명 주기 관리(PLM) 개념의 일부로 디지털 트윈이 정식화되었습니다. 2010년대 IoT 센서, 5G, AI/ML 기술이 성숙하면서 디지털 트윈이 실용화되었습니다. GE, Siemens, ABB 등 제조 장비 기업들이 산업용 디지털 트윈 플랫폼을 출시했습니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   스마트 팩토리(Industry 4.0)에서는 설비 가동률(OEE) 극대화, 품질 불량률 최소화, 에너지 효율 최적화가 필수적입니다. 스마트 시티에서는 교통 흐름, 에너지 소비, 재난 대응의 시뮬레이션이 필요합니다. 디지털 트윈은 이러한 요구사항을 충족하는 **가상 실험실** 역할을 수행합니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Module) | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/플랫폼 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Physical Entity** | 물리적 객체 (기계, 건물, 도시) | 센서 장착, 액추에이터 제어 | PLC, SCADA, Sensors | 실제 집 |
| **Sensor/Data Layer** | 실시간 데이터 수집 | 진동, 온도, 압력, 위치 등 IoT 데이터 | MQTT, OPC-UA, Kafka | CCTV/센서 |
| **Virtual Model** | 3D 모델, 물리 시뮬레이션 | FEM(유한요소법), CFD(전산유체역학) | Unity, Unreal, ANSYS, Simulink | 설계도면 |
| **Data Integration** | 물리-가상 데이터 동기화 | 실시간 스트리밍, 데이터 정제 | Azure Digital Twins, AWS IoT TwinMaker | 데이터 파이프라인 |
| **Analytics/AI** | 예측, 최적화, 이상 탐지 | 머신러닝, 딥러닝, 피지컬 AI | TensorFlow, PyTorch, Azure ML | 두뇌 |

### 2. 정교한 구조 다이어그램: 디지털 트윈 아키텍처

```text
=====================================================================================================
                          [ Digital Twin Architecture ]
=====================================================================================================

    [ Physical World ]                    [ Data Layer ]               [ Virtual World ]
    +------------------+                 +------------------+         +------------------+
    |                  |    Sensors      |  Edge Gateway    |         |                  |
    |  +------------+  | ==============> |  - Data Filter   |         |  +------------+  |
    |  |  Machine   |  |   (IoT/OPC-UA) |  - Protocol Conv.|         |  |  3D Model   |  |
    |  |  (Robot,   |  |                 |  - Compression   |         |  |  (Unity/    |  |
    |  |  Turbine)  |  |                 +--------+---------+         |  |  Unreal)    |  |
    |  +------------+  |                          |                   |  +------+-----+  |
    |        |         |                          |                   |         |        |
    |   [Sensors]      |                          | MQTT/Kafka        |    [Simulation]  |
    |   - Vibration    |                          |                   |    - Physics     |
    |   - Temperature  |                          v                   |    - Thermal     |
    |   - Pressure     |                 +------------------+         |    - CFD         |
    |                  | <============= |  Cloud Platform  | ===========>                |
    +------------------+   Actuators    |  - Time-Series DB|  Sync   +------------------+
                                        |  - Digital Twin  |
                                        |    Graph (Knowledge
                                        |    Graph)        |
                                        |  - ML/AI Engine  |
                                        +--------+---------+
                                                 |
                                                 | API/Events
                                                 v
    +-----------------------------------------------------------------------------------------+
    |                              [ Applications ]                                           |
    |  +------------------+  +------------------+  +------------------+  +------------------+ |
    |  | Predictive       |  | What-if          |  | Remote           |  | AR/VR            | |
    |  | Maintenance      |  | Simulation       |  | Monitoring       |  | Visualization    | |
    |  | (고장 예측)       |  | (시나리오 분석)  |  | (원격 감시)       |  | (몰입형 뷰)       | |
    |  +------------------+  +------------------+  +------------------+  +------------------+ |
    +-----------------------------------------------------------------------------------------+
```

### 3. 심층 동작 원리 (예지 보전 시나리오)

풍력 터빈의 베어링 고장 예측을 위한 디지털 트윈 동작 프로세스입니다.

1. **센서 데이터 수집 (Data Ingestion)**:
   터빈의 진동 가속도계, 온도 센서, 회전수(RPM) 센서가 초당 1,000회 데이터를 수집합니다. 엣지 게이트웨이에서 1차 필터링(노이즈 제거, 이상치 탐지) 후 MQTT로 클라우드로 전송합니다.

2. **디지털 트윈 모델 업데이트 (Model Synchronization)**:
   수신된 센서 데이터가 디지털 트윈의 해당 컴포넌트(베어링 3D 모델)에 매핑됩니다. 열적 해석(Thermal Analysis)으로 온도 분포가 계산되고, 구조 해석(FEM)으로 응력 분포가 업데이트됩니다.

3. **이상 탐지 및 예측 (Anomaly Detection & Prediction)**:
   머신러닝 모델(Isolation Forest, LSTM Autoencoder)이 과거 정상 데이터와 현재 데이터를 비교하여 이상 징후를 탐지합니다. 남은 수명(RUL, Remaining Useful Life) 예측 모델이 "현재 마모도 기준으로 72시간 후 고장 확률 90%"라고 예측합니다.

4. **시뮬레이션 및 의사결정 (Simulation & Decision)**:
   What-if 시뮬레이션으로 "지금 회전수를 10% 줄이면 수명이 120시간 연장됨"을 도출합니다. 유지보수 담당자에게 모바일 알림을 발송하고, 예비 부품 주문을 자동화합니다.

### 4. 핵심 알고리즘 및 실무 코드 예시

디지털 트윈의 예지 보전(Predictive Maintenance)을 위한 RUL 예측 모델입니다.

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from typing import Tuple, List

class DigitalTwinRULPredictor:
    """
    디지털 트윈 기반 Remaining Useful Life (RUL) 예측 모델
    - 센서 데이터(진동, 온도, 회전수)를 시계열로 입력
    - LSTM 기반으로 고장까지 남은 시간(RUL) 예측
    """

    def __init__(self, sequence_length: int = 50, n_features: int = 4):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.scaler = MinMaxScaler()
        self.model = self._build_model()

    def _build_model(self) -> Sequential:
        """LSTM 기반 RUL 예측 모델 구조"""
        model = Sequential([
            LSTM(64, return_sequences=True, input_shape=(self.sequence_length, self.n_features)),
            Dropout(0.2),
            LSTM(32, return_sequences=False),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(1, activation='linear')  # RUL 출력 (연속값)
        ])
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model

    def preprocess_sensor_data(
        self,
        raw_data: pd.DataFrame,
        fit_scaler: bool = True
    ) -> np.ndarray:
        """
        센서 데이터 전처리: 정규화, 윈도우 슬라이딩
        raw_data columns: ['vibration_x', 'vibration_y', 'temperature', 'rpm']
        """
        sensor_cols = ['vibration_x', 'vibration_y', 'temperature', 'rpm']

        if fit_scaler:
            scaled_data = self.scaler.fit_transform(raw_data[sensor_cols])
        else:
            scaled_data = self.scaler.transform(raw_data[sensor_cols])

        # 시퀀스 윈도우 생성 (Sliding Window)
        sequences = []
        for i in range(len(scaled_data) - self.sequence_length):
            sequences.append(scaled_data[i:i + self.sequence_length])

        return np.array(sequences)

    def train(self, train_data: pd.DataFrame, rul_labels: np.ndarray, epochs: int = 50):
        """
        모델 학습
        """
        X_train = self.preprocess_sensor_data(train_data, fit_scaler=True)

        # RUL 라벨도 윈도우에 맞춰 정렬
        y_train = rul_labels[self.sequence_length:]

        self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=32,
            validation_split=0.2,
            verbose=1
        )

    def predict_rul(self, current_sensor_data: pd.DataFrame) -> Tuple[float, str]:
        """
        현재 센서 데이터로부터 RUL 예측
        Returns: (예측된 RUL 시간, 상태 등급)
        """
        X_input = self.preprocess_sensor_data(current_sensor_data, fit_scaler=False)

        if len(X_input) == 0:
            return 0.0, "INSUFFICIENT_DATA"

        # 마지막 시퀀스로 예측
        predicted_rul = self.model.predict(X_input[-1:].reshape(1, self.sequence_length, self.n_features))
        rul_hours = float(predicted_rul[0][0])

        # 상태 등급 분류
        if rul_hours > 168:  # 7일 이상
            status = "HEALTHY"
        elif rul_hours > 72:  # 3일 이상
            status = "WARNING"
        elif rul_hours > 24:  # 24시간 이상
            status = "CRITICAL"
        else:
            status = "IMMINENT_FAILURE"

        return rul_hours, status

    def simulate_what_if(
        self,
        current_data: pd.DataFrame,
        rpm_reduction: float = 0.1
    ) -> dict:
        """
        What-if 시뮬레이션: 운전 조건 변경 시 RUL 변화 예측
        """
        # 현재 RUL
        current_rul, _ = self.predict_rul(current_data)

        # RPM 감소 시나리오
        modified_data = current_data.copy()
        modified_data['rpm'] = modified_data['rpm'] * (1 - rpm_reduction)

        # 수정된 데이터로 RUL 재예측
        modified_rul, _ = self.predict_rul(modified_data)

        return {
            'current_rul_hours': current_rul,
            'modified_rul_hours': modified_rul,
            'rul_extension': modified_rul - current_rul,
            'rpm_reduction_percent': rpm_reduction * 100
        }


class DigitalTwinDashboard:
    """
    디지털 트윈 대시보드 시뮬레이션
    """

    def __init__(self, predictor: DigitalTwinRULPredictor):
        self.predictor = predictor

    def update_twin_state(self, sensor_data: pd.DataFrame) -> dict:
        """
        디지털 트윈 상태 업데이트 및 경고 생성
        """
        rul, status = self.predictor.predict_rul(sensor_data)

        dashboard_data = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'sensor_summary': {
                'avg_vibration': sensor_data[['vibration_x', 'vibration_y']].mean().mean(),
                'max_temperature': sensor_data['temperature'].max(),
                'avg_rpm': sensor_data['rpm'].mean()
            },
            'prediction': {
                'remaining_useful_life_hours': round(rul, 2),
                'health_status': status
            },
            'alerts': []
        }

        # 경고 생성 로직
        if status == "WARNING":
            dashboard_data['alerts'].append({
                'level': 'WARNING',
                'message': f'RUL이 {rul:.1f}시간 남았습니다. 예비 부품을 준비하세요.'
            })
        elif status == "CRITICAL":
            dashboard_data['alerts'].append({
                'level': 'CRITICAL',
                'message': f'RUL이 {rul:.1f}시간 남았습니다. 즉시 유지보수를 계획하세요!'
            })
        elif status == "IMMINENT_FAILURE":
            dashboard_data['alerts'].append({
                'level': 'EMERGENCY',
                'message': '고장 임박! 즉시 설비를 정지하고 조치하세요!'
            })

        return dashboard_data


if __name__ == "__main__":
    # 시뮬레이션용 센서 데이터 생성
    np.random.seed(42)
    n_samples = 1000

    # 정상 상태에서 마모 진행으로 가정한 데이터
    time_steps = np.arange(n_samples)
    vibration = 0.5 + 0.001 * time_steps + np.random.normal(0, 0.1, n_samples)  # 서서히 증가
    temperature = 60 + 0.05 * time_steps + np.random.normal(0, 2, n_samples)
    rpm = 1500 - 0.5 * time_steps + np.random.normal(0, 20, n_samples)  # 서서히 감소

    sensor_df = pd.DataFrame({
        'vibration_x': vibration,
        'vibration_y': vibration * 0.8,
        'temperature': temperature,
        'rpm': rpm
    })

    # RUL 라벨 (마지막 시점이 0이 되도록)
    rul_labels = n_samples - time_steps

    # 모델 학습
    predictor = DigitalTwinRULPredictor(sequence_length=50)
    predictor.train(sensor_df, rul_labels.values, epochs=10)

    # 현재 상태 예측
    dashboard = DigitalTwinDashboard(predictor)
    result = dashboard.update_twin_state(sensor_df.tail(100))

    print("\n=== Digital Twin Dashboard ===")
    print(f"Timestamp: {result['timestamp']}")
    print(f"Sensor Summary: {result['sensor_summary']}")
    print(f"RUL Prediction: {result['prediction']['remaining_useful_life_hours']} hours")
    print(f"Health Status: {result['prediction']['health_status']}")

    if result['alerts']:
        print("\nAlerts:")
        for alert in result['alerts']:
            print(f"  [{alert['level']}] {alert['message']}")

    # What-if 시뮬레이션
    what_if = predictor.simulate_what_if(sensor_df.tail(100), rpm_reduction=0.15)
    print(f"\n=== What-if Simulation ===")
    print(f"RPM 15% 감소 시 RUL 연장: {what_if['rul_extension']:.1f} hours")
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 디지털 트윈 유형

| 유형 | 대상 | 데이터 동기화 | 목적 | 적용 분야 |
| :--- | :--- | :--- | :--- | :--- |
| **Component Twin** | 부품 (베어링, 모터) | 단일 센서 | 부품 수명 예측 | 산업 설비 |
| **Asset Twin** | 장비 (로봇, 터빈) | 다중 센서 | 설비 최적화, 고장 예측 | 제조, 에너지 |
| **System Twin** | 시스템 (생산 라인) | 복합 데이터 | 공정 최적화, 병목 분석 | 스마트 팩토리 |
| **Process Twin** | 프로세스 (공급망) | 비즈니스 데이터 | 프로세스 혁신, 의사결정 | 물류, 유통 |
| **City/Building Twin** | 도시, 건물 | 도시 센서 네트워크 | 교통/에너지 최적화, 재난 대응 | 스마트 시티 |

### 2. 디지털 트윈 플랫폼 비교

| 플랫폼 | 제공사 | 특징 | 적합한 용도 |
| :--- | :--- | :--- | :--- |
| **Azure Digital Twins** | Microsoft | 지식 그래프, IoT Hub 통합 | 스마트 빌딩, 공장 |
| **AWS IoT TwinMaker** | Amazon | S3, SiteWise 연동, 3D 시각화 | 산업 IoT |
| **NVIDIA Omniverse** | NVIDIA | USD 기반 3D 협업, AI 에이전트 | 제조, 로봇 시뮬레이션 |
| **Siemens Xcelerator** | Siemens | PLM, CAE 통합, 산업 표준 | 제조, 자동차 |
| **PTC ThingWorx** | PTC | AR 연동, Industrial IoT | 제조, 서비스 |

### 3. 과목 융합 관점 분석 (디지털 트윈 + 타 도메인 시너지)
- **디지털 트윈 + AI/ML (Physical AI)**: 단순한 3D 모델을 넘어, 물리 법칙(유체역학, 열역학)과 AI가 결합된 **Physics-informed Neural Networks(PINNs)**를 활용하여, 실제 실험 없이도 고정밀 시뮬레이션을 수행합니다.

- **디지털 트윈 + AR/VR (Immersive Visualization)**: HoloLens, Apple Vision Pro와 같은 XR 기기를 통해, 현장 작업자가 실제 기계 위에 디지털 트윈을 오버레이하여 수리 가이드를 실시간으로 확인할 수 있습니다.

- **디지털 트윈 + 블록체인 (Data Integrity)**: 센서 데이터와 시뮬레이션 결과의 무결성을 보장하기 위해 블록체인을 활용합니다. 이는 규제 산업(원자력, 항공우주)에서 데이터 위변조 방지에 필수적입니다.

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략
- **[상황 A] 스마트 팩토리의 생산 라인 최적화**
  - **문제점**: 여러 공정이 병목으로 인해 전체 생산량이 제한됨. 어느 공정이 병목인지 파악 어려움.
  - **기술사 판단 (전략)**: **시스템 트윈(System Twin)** 구축. 각 공정 장비의 디지털 트윈을 연결하여 전체 생산 라인을 가상화. What-if 시뮬레이션으로 "공정 A 속도를 10% 높이면 전체 생산량이 8% 증가"를 도출. 디지털 트윈에서 최적화된 파라미터를 실제 설비에 배포.

- **[상황 B] 스마트 시티의 교통 신호 최적화**
  - **문제점**: 출퇴근 시간 교통 체증 심화. 고정된 신호 주기로 인해 실시간 교통량 대응 불가.
  - **기술사 판단 (전략)**: **시티 트윈(City Twin)** 구축. CCTV, 교통 센서, 내비게이션 데이터를 통합하여 실시간 교통 흐름을 가상화. 강화학습(RL) 기반 신호 최적화 에이전트가 디지털 트윈에서 학습 후, 실제 신호등에 적용. 예측 결과: 통행 시간 20% 단축.

### 2. 도입 시 고려사항 (기술적/보안적 체크리스트)
- **데이터 품질 관리 (Data Quality)**: 센서 데이터의 정확성이 디지털 트윈의 신뢰도를 결정합니다. 센서 교정(Calibration), 이상치 필터링, 결측치 처리(Data Imputation) 체계를 구축해야 합니다.

- **모델 충실도 (Model Fidelity)**: 모델의 정밀도(Fidelity)가 높을수록 연산 비용이 급증합니다. 용도에 따라 **저충실도(Low-Fidelity, 실시간 모니터링용)**와 **고충실도(High-Fidelity, 설계 검증용)**를 구분하여 적용해야 합니다.

- **지적재산권 보호 (IP Protection)**: 디지털 트윈 모델은 기업의 핵심 자산입니다. 모델 파일 암호화, 워터마킹, 접근 통제(RBAC)를 통해 유출을 방지해야 합니다.

### 3. 주의사항 및 안티패턴 (Anti-patterns)
- **디지털 트윈 = 3D 모델 오해**: 단순한 3D 시각화 모델을 디지털 트윈이라고 착각하는 안티패턴입니다. 진정한 디지털 트윈은 **실시간 데이터 동기화**와 **시뮬레이션/예측 기능**이 필수입니다.

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과 (도입 전후 ROI)

| 구분 | 기존 방식 (AS-IS) | 디지털 트윈 (TO-BE) | 개선 지표 (Impact) |
| :--- | :--- | :--- | :--- |
| **유지보수 비용** | 예방 교체 (불필요한 비용) | **예지 정비 (필요 시점)** | 유지보수 비용 **30% 절감** |
| **설비 가동률 (OEE)** | 65~75% | **85~95%** | 가동률 **20% 향상** |
| **제품 개발 기간** | 24개월 | **12개월** | 개발 기간 **50% 단축** |
| **불량률** | 3~5% | **0.5~1%** | 불량률 **80% 감소** |

### 2. 미래 전망 및 진화 방향
- **메타버스와의 융합**: 디지털 트윈이 메타버스 플랫폼(NVIDIA Omniverse, Meta Horizon)과 통합되어, 가상 공간에서 협업하고 시뮬레이션하는 **산업 메타버스**가 등장할 것입니다.

- **자율 시뮬레이션 (Autonomous Simulation)**: AI 에이전트가 자율적으로 시나리오를 생성하고 최적화하는 **Self-Optimizing Digital Twin**이 보편화될 것입니다.

### 3. 참고 표준/가이드
- **ISO 23247**: Industrial automation systems and integration - Digital twin framework for manufacturing
- **IEC 63278**: Asset Administration Shell (AAS) - Industry 4.0 디지털 트윈 표준
- **Digital Twin Consortium**: 글로벌 디지털 트윈 산업 연합

---

## 관련 개념 맵 (Knowledge Graph)
- **[사물인터넷 (IoT)](@/studynotes/06_ict_convergence/03_iot/iot_architecture.md)**: 디지털 트윈에 실시간 데이터를 공급하는 센서 네트워크.
- **[엣지 컴퓨팅 (Edge Computing)](./edge_computing.md)**: 디지털 트윈의 실시간 동기화를 위한 분산 처리 인프라.
- **[CPS (Cyber-Physical System)](./cps.md)**: 물리 세계와 사이버 세계의 융합 시스템으로서 디지털 트윈의 이론적 기반.
- **[시뮬레이션 (Simulation)](./simulation.md)**: 디지털 트윈의 What-if 분석을 위한 핵심 기술.
- **[AR/VR (증강/가상현실)](./xr.md)**: 디지털 트윈의 몰입형 시각화 인터페이스.

---

## 어린이를 위한 3줄 비유 설명
1. 디지털 트윈은 '비밀 거울'이에요! 실제 집이 거울 속에 똑같이 비치는데, 이 거울은 집이 아플지 미리 알려줘요.
2. 공장의 기계가 "나 조금 아파요"라고 하면, 디지털 트윈 거울이 "3일 후에 열이 날 거예요, 미리 약 드세요!"라고 말해줘요.
3. 덕분에 기계가 갑자기 멈추는 일 없이, 공장이 항상 쌩쌩 돌아갈 수 있어요!
