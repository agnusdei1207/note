+++
weight = 759
title = "759. 블로킹(Blocking) vs 논블로킹(Non-blocking) vs 비동기(Async) I/O 비교"
date = "2026-03-10"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "I/O 모델", "Blocking", "Non-blocking", "Synchronous", "Asynchronous", "제어권", "동기화"]
series = "운영체제 800제"
+++

# 블로킹 vs 논블로킹 vs 비동기 I/O 모델 비교

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: I/O 작업 수행 시 **호출자(App)에게 제어권이 즉시 돌아오는지(Blocking/Non-blocking)**와 **작업 완료 통지 방식(Sync/Async)**에 따른 입출력 처리 모델의 분류.
> 2. **가치**: 시스템 자원의 점유 방식을 최적화하여, 대규모 동시 접속을 처리하는 고성능 네트워크 서버와 사용자 인터페이스의 응답성을 결정짓는 핵심 아키텍처다.
> 3. **융합**: 운영체제의 시스템 콜 인터페이스와 프로그래밍 언어의 런타임(Event Loop, Promise)이 결합되어 현대적 비동기 프로그래밍 패러다임을 형성한다.

---

### Ⅰ. I/O 모델 구분을 위한 2가지 핵심 기준

1. **제어권 (Control Flow)**: I/O 호출 시 제어권이 즉시 반환되는가?
   - **Blocking**: 작업 끝날 때까지 대기.
   - **Non-blocking**: 일단 "작업 중"이라는 응답과 함께 제어권 즉시 반환.
2. **동기화 (Synchronization)**: 작업 완료 여부를 누가 챙기는가?
   - **Synchronous**: 호출자가 완료를 기다리거나 계속 확인.
   - **Asynchronous**: 커널이 작업을 다 끝내고 호출자에게 알려줌.

---

### Ⅱ. 4대 I/O 모델 상세 비교 (ASCII)

#### 1. Blocking Sync (전통적 I/O)
- **특징**: 제어권도 뺏기고 결과도 기다림.

#### 2. Non-blocking Sync
- **특징**: 제어권은 바로 얻지만, 결과가 나올 때까지 계속 "다 됐니?"라고 물어봄 (Polling).

#### 3. Async (비동기 I/O)
- **특징**: 제어권을 즉시 얻고, 나는 딴짓함. 커널이 다 끝나면 나를 깨움.

```ascii
    [ App ] --- read() ---> [ Kernel ]
    
    < Blocking Sync >       < Non-blocking Sync >   < Asynchronous >
    (Wait...)               (Busy Check...)         (Doing other stuff)
    |                       |-- Done? -> No         |
    |                       |-- Done? -> No         |
    | <--- Return Result    | <--- Return Result    | <--- Callback/Signal
```

---

### Ⅲ. 상세 모델 특징 분석표

| 구분 | Blocking | Non-blocking |
|:---|:---|:---|
| **Synchronous** | **Sync-Blocking**: 가장 흔함. 코드가 순차적. | **Sync-Nonblocking**: 결과 확인을 위한 루프 발생. |
| **Asynchronous** | (거의 안 쓰임 / I/O Multiplexing) | **Async-Nonblocking**: 최강의 효율성. (Node.js, Nginx) |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 고성능 네트워크 서버 설계 (C10K 문제)
- **문제**: 수만 명의 접속자를 스레드당 1개(Blocking)로 처리하면 메모리가 부족해짐.
- **기술사적 결단**: 
  - **I/O Multiplexing (select, poll, epoll)** 기술을 사용하여 하나의 스레드가 수천 개의 Non-blocking 소켓을 감시하게 한다.
  - 최신 리눅스 환경에서는 진정한 비동기 I/O인 **io_uring**을 사용하여 커널-유저 간 문맥 교환 오버헤드까지 극소화한다.

#### 2. 기술사적 인사이트
- **추상화의 함정**: 자바의 NIO나 파이썬의 asyncio는 내부적으로 복잡한 운영체제 시스템 콜을 추상화한 것이다. 성능 최적화를 위해서는 하부의 `epoll`이나 `kqueue`가 어떻게 작동하는지 이해하는 것이 필수적이다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량/정성 기대효과
- **시스템 자원 밀도 향상**: 적은 메모리와 CPU로 더 많은 동시 요청 처리.
- **응답성 극대화**: I/O 대기 시간 동안 다른 연산을 수행하여 지연 시간(Latency) 은폐.

#### 2. 미래 전망
앞으로 모든 I/O는 **비동기 논블로킹**이 기본 사양이 될 것이다. 특히 클라우드 네이티브 환경의 마이크로서비스 간 통신(gRPC 등)에서 네트워크 지연을 극복하기 위해 하드웨어 가속(SmartNIC)과 연동된 비동기 I/O 기술이 인프라의 핵심 경쟁력이 될 것이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[I/O 멀티플렉싱](../8_io_storage_system/TBD_io_multiplexing.md)**: 논블로킹 I/O를 효율적으로 관리하는 기술.
- **[io_uring](../8_io_storage_system/464_topic.md)**: 차세대 비동기 I/O 프레임워크.
- **[시스템 콜 오버헤드](./756_system_call_overhead.md)**: I/O 모델 선택 시 고려해야 할 성능 비용.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **블로킹**은 피자를 주문하고 가게 앞에 서서 피자가 나올 때까지 아무것도 안 하고 기다리는 거예요.
2. **논블로킹**은 1분마다 가게 문을 열고 "제 피자 나왔나요?"라고 계속 물어보면서 게임을 하는 거죠.
3. **비동기**는 "피자 다 되면 전화해 주세요!"라고 말하고 집에 가서 잠을 자고 있으면, 전화가 왔을 때 피자를 맛있게 먹는 가장 편한 방법이랍니다!
