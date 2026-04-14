+++
weight = 567
title = "레디스 데이터 만료 및 삭제 정책 (Redis Eviction & Expiration Policy)"
date = "2026-03-04"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)
1. **메모리 효율화:** 제한된 RAM 자원을 최적화하기 위해 만료된 데이터(TTL)를 제거하고 정책에 따라 공간을 확보한다.
2. **성능-정확성 트레이드오프:** CPU 부하를 낮추기 위해 만료 데이터 삭제 시 확률적 알고리즘과 지연 삭제(Lazy)를 혼용한다.
3. **가용성 유지:** 메모리 부족 시(OOM) 적절한 Eviction 알고리즘(LRU, LFU 등)을 선택하여 서비스 중단을 방지한다.

### Ⅰ. 개요 (Context & Background)
레디스(Redis)는 인-메모리 데이터 구조 저장소로서 메모리 크기가 물리적으로 제한되어 있다. 데이터가 계속 쌓여 설정된 `maxmemory`에 도달하면 성능 저하나 장애가 발생할 수 있다. 이를 방지하기 위해 레디스는 **만료 정책(Expiration)**과 **삭제 정책(Eviction)**이라는 두 가지 핵심 메커니즘을 제공하여 시스템 안정성을 유지한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

레디스의 데이터 관리는 TTL 기반의 자동 삭제와 메모리 임계치 도달 시의 강제 삭제 프로세스로 나뉜다.

```text
[ Redis Memory Management Architecture ]

(1) Data Insertion (SET key val EX 60)
        |
        v
+-----------------------+      (2) Expiration Check (만료 체크)
| [ Redis Key Space ]   |------> [ Passive: Lazy Expiration ] (액세스 시 삭제)
| - Key A (TTL: 10s)    |------> [ Active: Periodic Sample  ] (주기적 샘플링 삭제)
| - Key B (No TTL)      |
+-----------------------+
        |
        | (If Memory > maxmemory)
        v
+-----------------------+      (3) Eviction Policy (메모리 확보 삭제)
| [ Eviction Engine ]   |------> [ Allkeys-LRU / LFU        ]
| (삭제 대상 선정)       |------> [ Volatile-LRU / LFU      ]
+-----------------------+------> [ Random / Noeviction     ]
```

#### 핵심 작동 원리
1. **만료 삭제 (Expiration):**
   - **Lazy Expiration:** 클라이언트가 키에 접근할 때 만료 여부를 확인하고 삭제한다. (CPU 효율적)
   - **Active Expiration:** 주기적으로 메모리를 샘플링하여 만료된 키를 무작위로 삭제한다. (메모리 효율적)
2. **메모리 확보 삭제 (Eviction):** `maxmemory` 도달 시 발생한다.
   - **LRU (Least Recently Used):** 가장 오랫동안 사용되지 않은 데이터를 삭제한다.
   - **LFU (Least Frequently Used):** 참조 횟수가 가장 적은 데이터를 삭제한다. (최신 트렌드)

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 정책 종류 | 대상 범위 | 알고리즘 특징 | 비고 |
| :--- | :--- | :--- | :--- |
| **volatile-lru** | TTL 설정된 키 | 근사 LRU (Approximated LRU) | 일반적인 캐시 용도 |
| **allkeys-lru** | 모든 키 | 전체 키 중 오랫동안 안 쓴 키 삭제 | DB 보조용 캐시 |
| **volatile-lfu** | TTL 설정된 키 | 참조 빈도가 낮은 키 삭제 | 접근 빈도 편차 클 때 유리 |
| **noeviction** | N/A | 삭제 안 함 (에러 반환) | 쓰기 금지, 데이터 보호 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **알고리즘 선택 전략:** 단순히 최근 사용 여부가 중요하다면 **LRU**를, 특정 데이터가 지속적으로 자주 호출되는 패턴이라면 **LFU**를 선택하는 것이 캐시 히트율(Cache Hit Ratio) 향상에 유리하다.
- **기술사적 판단:** 레디스의 LRU는 정확한 이중 연결 리스트가 아닌 샘플링 방식이다. 샘플 수를 늘리면 정확도는 올라가나 CPU 사용량이 증가하므로 실무에서는 기본값(5)을 유지하며 메모리 압박 시 스케일 아웃(Sharding)을 우선 고려해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
적절한 삭제 정책은 **시스템의 예측 가능성**을 높여준다. 최근에는 `maxmemory-eviction-tenacity` 설정을 통해 삭제 강도를 조절하거나, `Lazy Freezing` 기능을 통해 백그라운드 스레드에서 메모리 해제를 처리하여 성능 병목을 최소화하는 방향으로 발전하고 있다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** In-Memory DB, Cache Strategy
- **하위 개념:** LRU, LFU, TTL, maxmemory
- **연관 기술:** Memcached, Redis Sentinel

### 👶 어린이를 위한 3줄 비유 설명
1. 장난감 상자(메모리)가 꽉 차면 **새 장난감**을 넣을 수 없어요.
2. 그래서 **오래된 장난감**이나 **안 가지고 노는 것**부터 골라서 버리는 약속을 정하는 거예요.
3. 덕분에 상자는 항상 깨끗하고 새로운 장난감을 넣을 자리가 생겨요!
