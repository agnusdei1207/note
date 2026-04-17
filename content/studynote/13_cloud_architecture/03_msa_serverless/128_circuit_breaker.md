+++
weight = 128
title = "서킷 브레이커 (Circuit Breaker) 패턴"
date = "2024-03-24"
[extra]
categories = "studynote-cloud"
+++

## 핵심 인사이트 (3줄 요약)
- **서킷 브레이커**는 특정 서비스에 장애나 지연이 발생했을 때 해당 서비스로의 호출을 즉시 차단하여 전체 시스템의 연쇄 장애(Cascading Failure)를 방지함.
- 장애가 복구될 때까지 기다리는 대신, 빠르게 에러를 반환하거나 미리 정의된 대체 로직(Fallback)을 실행하여 시스템의 회복 탄력성(Resiliency)을 확보함.
- 마이크로서비스 간의 강한 결합을 끊고 시스템 전체의 가용성을 유지하는 분산 환경의 필수 안전 장치임.

### Ⅰ. 개요 (Context & Background)
- 동기적(REST) 호출이 주를 이루는 MSA 환경에서 한 서비스의 지연은 호출하는 서비스의 스레드를 점유하여 전체 시스템의 자원 고갈을 유발함.
- 누전 차단기(Circuit Breaker)가 전력 과부하 시 전기를 끊는 것과 같은 원리로, 장애 중인 서비스로의 요청을 일시적으로 차단함.
- 서비스 간의 무의미한 재시도(Retry)를 방지하여 장애 서버가 복구될 시간을 확보해주는 기능도 수행함.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- 서킷 브레이커는 Closed, Open, Half-Open의 세 가지 상태를 가진 상태 머신(State Machine)으로 동작함.

```text
[ Circuit Breaker State Transition ]
   +---------------------------------------+
   |        CLOSED (Normal State)          | --- [Failures > Threshold] --+
   +---------------------------------------+                              |
          ^                                                               |
          | [Successes > Threshold]                                        V
   +---------------------------------------+       +---------------------------------------+
   |      HALF-OPEN (Test State)           | <---  |         OPEN (Error State)            |
   +---------------------------------------+       +---------------------------------------+
          (Small amount of traffic)                 (Wait for Timeout / Skip Logic)

[ BILINGUAL FLOW: Circuit Status ]
1. Closed: Success (O), Circuit (Connect)
2. Open: Fail (X), Circuit (Disconnect), Execute Fallback
3. Half-Open: Testing recovery...
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 상태 | 서킷 상태 | 설명 | 동작 결과 |
| :--- | :--- | :--- | :--- |
| **Closed** | 닫힘 (정상) | 요청이 타겟 서비스로 전달됨 | 정상 응답 처리 |
| **Open** | 열림 (차단) | 요청을 타겟 서비스로 보내지 않고 차단함 | 즉각적인 에러 또는 폴백 실행 |
| **Half-Open** | 반열림 (검사) | 소수의 요청만 보내서 복구 여부 확인 | 성공 시 Closed, 실패 시 Open으로 복귀 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **임계치 설정**: 타임아웃 시간, 에러율 퍼센트(%), 연속 장애 횟수 등을 서비스의 특성에 맞게 세밀하게 조정함.
- **폴백(Fallback) 구현**: 서킷이 Open되었을 때 사용자에게 에러 대신 캐시된 데이터나 기본값을 반환하여 부정적인 사용자 경험을 최소화함.
- **모니터링 연동**: 서킷 브레이커의 상태 변화를 실시간으로 대시보드(Hystrix Dashboard, Resilience4j)에 시각화하여 장애를 즉각 인지해야 함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- 서킷 브레이커는 분산 시스템의 신뢰성을 획기적으로 향상시키며, '장애는 언제나 발생할 수 있다(Design for Failure)'는 철학을 실현함.
- 최근에는 서비스 메시(Istio, Linkerd)의 기본 기능으로 포함되어 코드 수정 없이도 인프라 레벨에서 구현 가능함.
- 결론적으로 서킷 브레이커는 **클라우드 서비스의 생명선**과 같으며, 부분적인 장애가 전체의 붕괴로 이어지지 않게 막는 최후의 방어선임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 장애 극복 (Failover), 회복 탄력성 (Resiliency)
- **하위 개념**: 폴백 (Fallback), 벌크헤드 (Bulkhead), 타임아웃
- **연관 개념**: MSA, 서비스 메시, Resilience4j, Hystrix, 리트라이 (Retry)

### 👶 어린이를 위한 3줄 비유 설명
- 집안에 전기가 너무 많이 흘러서 불이 날 것 같으면 두꺼비집(차단기)이 내려가는 것과 같아요.
- 고장 난 곳에 계속 전기를 보내지 않아서 집이 타지 않게 지켜주는 장치예요.
- 잠시 기다렸다가 고장 난 곳이 다 고쳐지면 다시 전기를 올려서 불을 켤 수 있답니다.
