+++
weight = 102
title = "IoT 3대 구성 요소"
date = "2024-03-21"
[extra]
categories = "studynote-ict-convergence"
+++

## 핵심 인사이트 (3줄 요약)
1. 사물인터넷(IoT) 시스템은 물리적 정보를 획득하는 **디바이스(Device)**, 정보를 전달하는 **네트워크(Network)**, 가치를 창출하는 **플랫폼(Platform/Service)**으로 구성됩니다.
2. 각 요소는 상호 유기적으로 결합되어 센싱된 원시 데이터(Raw Data)를 지능화된 정보(Intelligence)로 변환하는 파이프라인 역할을 수행합니다.
3. 최근에는 저전력 지능형 디바이스, 초광역 네트워크, 그리고 인공지능이 융합된 클라우드 플랫폼이 중심이 되어 고도화되고 있습니다.

### Ⅰ. 개요 (Context & Background)
- **배경**: 파편화된 기술 스택을 통합하여 서비스의 신뢰성과 효율성을 확보하기 위해 표준화된 아키텍처 관점에서의 구성 요소 정립이 필수적입니다.
- **정의**: IoT의 종단간(End-to-End) 서비스 구현을 위해 필요한 하드웨어, 통신망, 소프트웨어 인프라의 집합체입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **핵심 원리**: 3대 구성 요소는 'Sense -> Connect -> Think' 프로세스를 통해 데이터를 흐르게 합니다.

```text
[ IoT 3-Component Core Architecture ]

 ( Component 1 )     ( Component 2 )     ( Component 3 )
 [  Device/Sensor ]  [   Network      ]  [  Platform/Service ]
 +---------------+   +----------------+  +-------------------+
 |  - Sensing    |   |  - Connectivity|  |  - Data Analytics |
 |  - Actuating  |-->|  - Routing     |->|  - Visualization  |
 |  - Processing |   |  - Gateway     |  |  - App Interface  |
 +---------------+   +----------------+  +-------------------+
       ^                     ^                     ^
       |                     |                     |
 [ Physical World ]     [ Communication ]     [ Cyber World ]

* Device: 스마트 센서, 임베디드 OS (FreeRTOS)
* Network: 5G, BLE, Wi-Fi, LPWAN (LoRa, NB-IoT)
* Platform: AWS IoT, Azure IoT Hub, ThingSpeak
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
- **구성 요소별 핵심 기술 및 트렌드**

| 구성 요소 | 핵심 기능 (Core Function) | 주요 기술 (Key Technology) | 진화 방향 (Future) |
| :--- | :--- | :--- | :--- |
| 디바이스 (Device) | 정보 획득 및 제어 | 센서, MCU, Actuator | 저전력 온디바이스 AI (sLLM) |
| 네트워크 (Network) | 데이터 전송 및 라우팅 | LPWAN, 5G, TSN | 6G, 위성 통신 (NTN) 융합 |
| 플랫폼 (Platform) | 데이터 분석 및 서비스 | Cloud, AI, BigData | 디지털 트윈, 자율 운영 AI |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **기술사적 판단**: 단순한 하드웨어 설치보다는 전체 아키텍처 상의 **'병목 현상(Bottleneck)'**을 제거하는 것이 기술사의 역할입니다. 네트워크 대역폭 부족 시 **엣지 컴퓨팅**을, 배터리 수명 문제 시 **저전력 프로토콜**을 적용하는 정교한 설계가 필요합니다.
- **실무 전략**: **보안(Security)**은 특정 레이어가 아닌 3대 요소 전체에 수평적으로 내재화되어야 하며, 상호운용성 확보를 위해 **표준 API(REST/gRPC)**를 적극 활용해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 인프라의 가시성을 확보하고 유지보수를 자동화함으로써 운영 비용(OPEX)을 대폭 절감하고 서비스 가동률(Availability)을 극대화할 수 있습니다.
- **결론**: 3대 구성 요소는 상호 독립적이면서도 보완적인 관계입니다. 미래에는 이들이 클라우드 네이티브 환경에서 완전히 통합된 '서비스형 자산(Asset-as-a-Service)'으로 발전할 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
1. **MQTT/CoAP**: IoT 네트워크 레이어의 대표적인 경량 메시징 프로토콜
2. **Gateway**: 서로 다른 프로토콜을 사용하는 디바이스와 네트워크를 연결하는 중계 장치
3. **Big Data Analytics**: 플랫폼에서 수집된 방대한 데이터를 분석하여 통찰력을 얻는 기술

### 👶 어린이를 위한 3줄 비유 설명
1. 사물인터넷은 우리 몸과 비슷해요. 눈과 귀가 되는 것은 **디바이스**예요.
2. 머리로 신호를 보내주는 신경은 **네트워크**이고요.
3. 신호를 받아서 "이건 맛있는 사과야!"라고 판단하는 머리는 **플랫폼**이랍니다!
