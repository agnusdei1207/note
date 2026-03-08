+++
title = "525. 엣지 트리거"
weight = 525
+++

# 525. 엣지 트리거 (Edge-Triggered)
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 이벤트 발생 시점에만 알림
> 2. **가치**: I/O 멀티플렉싱 성능 햕
 3. **융합**: 레벨 트리거, epoll과 연관

---

## Ⅰ. 개요
### 개념 정의
**엣지 트리거(Edge-Triggered)**는 **I/O 이벤트가 상태 변경(에지)될 때만 알림을 보내는 방식**이다.

### 💡 비유: 자동문 알림
엣지 트리거는 **자동문 자 알림**과 같다. 편지을 내리면 바로 알림을 받는다.

### 엣지 트리거 vs 레벨 트리거 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                트리거 모드 비교                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【Level-Triggered (LT)】                                            │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                           │ │   │
│  │  장점: 구현 단순, 누락 않 위험                      │ │   │
│  │  단점: 이벤트가 준비되면 계속 알림                              │ │   │
│  │        (버퍼에 남은 데이터가 있으면 반복 알림)                │ │   │
│  │                                                             │ │   │
│  │  사용처: 데이터 손실 가능, EPOLLON 사용                   │ │   │
│  │        (일반적인 I/O 작업)                               │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【Edge-Triggered (ET)】                                              │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                           │ │   │
│  │  장점: 이벤트 한 번만 알림, 효율적                    │ │   │
│  │  단점: 모든 데이터를 읽어야 함, Starvation 방지 필수            │ │   │
│  │        버퍼를 완전히 비워야 함                            │ │   │
│  │                                                             │ │   │
│  │  사용처: EPOLLET 플래그 사용, 높은 처리량                    │ │   │
│  │        소켓, 파일, 시스템 콜                 │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【epoll ET 예시】                                                  │
│  ──────────────────                                                │
│  struct epoll_event ev;                                    │
│  ev.events = EPOLLIN | EPOLLET;  // Edge-triggered mode          │
│  ev.data.fd = fd;                                         │
│  if (epoll_ctl(epfd, EPOLL_CTL_ADD, fd, &ev) == -1) {              │
│      perror("epoll_ctl");                                  │
│      return;                                          │
│  }                                                         │
│                                                             │
│  while (1) {                                                │
│      int n = epoll_wait(epfd, events, MAX, -1);               │
│      for (int i = 0; i < n; i++) {                          │
│          // 한 번만 읽고 가능한 모든 데이터 읽기                │
│          while (1) {                                    │
│              ssize_t count = read(fd, buf, sizeof(buf));            │
│              if (count == -1) {                               │
│                  if (errno == EAGAIN) {                      │
│                      // 더 이상 데이터 없음                   │
│                      break;                                  │
│                  } else {                                │
│                      perror("read");                       │
│                      break;                                  │
│                  }                                     │
│              }                                 │
│              // 데이터 처리                             │
│              process_data(buf, count);                  │
│          }                                             │
│      }                                               │
│  }                                                   │
│                                                             │
│  【LT vs ET 비교】                                                │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  특징            LT (Level-Triggered)     ET (Edge-Triggered)       │ │   │
│  │  ────            ──────────────────            ─────────────────  │ │   │
│  │  알림 시점        데이터 있을 때마다             상태 변경 시에만            │ │   │
│  │  버퍼 처리        부분 읽기 가능                  완전히 읽어야 함              │ │   │
│  │  시스템 콜          높음 (반복 알림)                 낮음 (한 번 알림)            │ │   │
│  │  코딩 난이도       낮음                             높음 (Starvation 주의)      │ │   │
│  │  적용             일반적인 I/O               고성능 서버, 파일 시스템              │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 실무 적용
### 구현 예시
```
┌─────────────────────────────────────────────────────────────────────┐
│                실무 적용                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【epoll ET 설정】                                              │
│  ──────────────────                                                │
│  // 소켓을 논블로킹 모드로 설정                         │
│  int flags = fcntl(sock, F_GETFL, 0);                   │
│  fcntl(sock, F_SETFL, flags | O_NONBLOCK);               │
│                                                             │
│  // epoll 인스턴스 생성                                │
│  int epfd = epoll_create1(0);                          │
│  if (epfd == -1) {                                │
│      perror("epoll_create1");                  │
│      return -1;                                         │
│  }                                                         │
│                                                             │
│  // epoll 이벤트 구조체 설정                            │
│  struct epoll_event ev;                                │
│  ev.events = EPOLLIN | EPOLLET;                │
│  ev.data.fd = sock;                               │
│                                                             │
│  // 소켓 등록                                 │
│  if (epoll_ctl(epfd, EPOLL_CTL_ADD, sock, &ev) == -1) {            │
│      perror("epoll_ctl");                              │
│      return -1;                                         │
│  }                                                         │
│                                                             │
│  // 이벤트 루프                                            │
│  while (1) {                                              │
│      int n = epoll_wait(epfd, events, MAX, -1);             │
│      for (int i = 0; i < n; i++) {                    │
│          // 핸들러 실행                                │
│          handle_event(events[i]);                        │
│      }                                                 │
│  }                                                   │
│                                                             │
│  void handle_event(struct epoll_event *event) {               │
│      if (event->events & EPOLLIN) {                    │
│          char buf[4096];                               │
│          ssize_t n = read(event->data.fd, buf, sizeof(buf));                │
│          if (n > 0) {                                │
│              process_data(buf, n);                       │
│          } else if (n == -1) {                        │
│              if (errno == EAGAIN) {                      │
│                  // ET 모드에서는 정상                 │
│              } else {                              │
│                  perror("read");                       │
│              }                                     │
│          }                                     │
│      }                                                 │
│  }                                                   │
│                                                             │
│  【kqueue ET 설정】                                              │
│  ──────────────────                                                │
│  #include <sys/event.h>                                       │
│                                                             │
│  int kq = kqueue();                                     │
│  struct kevent change;                               │
│  struct kevent event;                               │
│                                                             │
│  EV_SET(&change, fd, EVFILT_READ, EV_ADD | EV_ENABLE, 0, 0, NULL); │
│                                                             │
│  while (1) {                                              │
│      int n = kevent(kq, &change, 1, &event, 1, NULL);             │
│      if (n > 0) {                                │
│          if (event.filter == EVFILT_READ) {              │
│              char buf[4096];                           │
│              ssize_t n = read(fd, buf, sizeof(buf));            │
│              process_data(buf, n);                       │
│          }                                         │
│      }                                           │
│  }                                                 │
│                                                             │
│  【성능 비교】                                               │
│  ──────────────────                                                │
│  // 10,000 연결 테스트                                  │
│  Level-triggered: epoll_wait() 즉시 반복               │
│  Edge-triggered: epoll_wait() 즉시 1회 알림             │
│                                                             │
│  // 처리량 비교 (C10K 문제)                     │
│  LT: 10,000 req/s (반복 알림)              │
│  ET: 100,000+ req/s (높은 효율)               │
│                                                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: 상태 변화 시에만 알림
• LT: 구현 단순, 이벤트 반복 알림
• ET: 이벤트 1회만 알림, 데이터 완전히 읽어야 함
• 장점: 효율적, 낮은 시스템 콜
• 단점: 구현 복잡, Starvation 방지 필요
• 설정: EPOLLET 플래그
• 용도: 고성능 서버, 파일 시스템, 채팅 서버
```

- **병렬 정리**:** 엣지 트리거는 상태가 변화할 때만 알림을 받는 방식입니다
 데이터를 완전히 읽어야 하며, `read` 루프에서 버퍼를 비워야) 구현은 복잡하지만 Starvation(기아 상태)을 방지해야 `while` 루프에서 완전한 비워:

:
        break;
    }
}
    // 읽기 완료
}
 else if (n == 0) {
        // 에러 또는 데이터 손실 가능 있        perror("read");
        break;
    }
}
}
```

### 👶 어린이를 위한 3줄 비유 설명
**개념**: 엣지 트리거는 "자동문" 같아요!
**원리**: 상태가 변하면 한 번만 알려요!
**효과**: 많은 요청을 효율적으로 처리해요!
