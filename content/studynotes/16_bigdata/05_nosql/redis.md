+++
title = "Redis (인메모리 데이터베이스)"
categories = ["studynotes-16_bigdata"]
+++

# Redis (인메모리 데이터베이스)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Redis(REmote DIctionary Server)는 **인메모리 기반의 고성능 Key-Value 데이터 저장소**로, String, List, Set, Hash, Sorted Set, Stream, Geospatial 등 풍부한 자료구조를 지원하며 초당 수백만 건의 연산을 처리합니다.
> 2. **가치**: 서브밀리초(sub-millisecond) 지연 시간으로 캐싱, 세션 저장소, 실시간 랭킹, Pub/Sub, Rate Limiting 등 다양한 Use Case에서 **RDBMS 대비 100~1000배 빠른 응답**을 제공합니다.
> 3. **융합**: Redis Cluster로 수평 확장, Redis Streams로 이벤트 스트리밍, RedisJSON/RedisSearch/RedisTimeSeries 등 모듈로 **다중 모델 데이터베이스**로 진화했습니다.

---

## Ⅰ. 개요 (Context & Background)

Redis는 2009년 Salvatore Sanfilippo가 개발한 오픈소스로, "데이터 구조 서버(Data Structure Server)"라는 이름에 걸맞게 단순 Key-Value를 넘어 다양한 자료구조를 지원합니다. **모든 데이터를 메모리에 보관**하여 디스크 I/O 병목을 제거하고, **싱글 스레드 이벤트 루프**로 높은 동시성을 처리합니다.

**💡 비유: 초고속 우편함**
Redis는 **각 칸마다 다른 종류의 물건을 보관하는 초고속 우편함**입니다. 1번 칸에는 편지(String), 2번 칸에는 책 목록(List), 3번 칸에는 태그 모음(Set), 4번 칸에는 순위표(Sorted Set)를 넣을 수 있습니다. 물건을 찾을 때 우편함을 열자마자 바로 꺼낼 수 있어서(메모리), 창고(디스크)까지 걸어가는 것보다 **1000배 빠릅니다**.

**등장 배경 및 발전 과정:**
1. **기존 기술의 치명적 한계점**: Memcached는 단순 Key-Value만 지원하고 영속성이 없었습니다. RDBMS는 디스크 기반으로 지연 시간이 수십~수백 ms에 달했습니다.
2. **혁신적 패러다임 변화**: Redis는 **메모리 + 영속성 + 풍부한 자료구조**를 결합했습니다. RDB(Snapshot)와 AOF(Append-Only File)로 장애 시 데이터 복구가 가능합니다.
3. **비즈니스적 요구사항**: 실시간 랭킹, 리더보드, 채팅, 세션 관리 등 **밀리초 미만의 응답**이 필요한 Use Case가 폭발적으로 증가했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Redis 핵심 구성 요소

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|---|---|---|---|---|
| **String** | 단일 값 저장 | Binary-safe, 최대 512MB | 캐시, 카운터 | 편지함 |
| **List** | 순서 있는 컬렉션 | LinkedList, 양방향 | 메시지 큐, 타임라인 | 책 더미 |
| **Set** | 중복 없는 집합 | Hash Table, O(1) | 태그, 팔로워 | 태그 모음 |
| **Hash** | 필드-값 맵핑 | Hash Table | 사용자 프로필 | 명함 |
| **Sorted Set** | 점수 기반 정렬 | Skip List + Hash Table | 랭킹, 리더보드 | 순위표 |
| **Stream** | 로그 구조 스트림 | Radix Tree + ListPack | 이벤트 소싱 | 방명록 |

### 정교한 구조 다이어그램 (ASCII Art)

```text
========================================================================================================
                              [ REDIS ARCHITECTURE ]
========================================================================================================

  [ CLIENT ]                          [ REDIS SERVER ]                    [ PERSISTENCE ]

  +-------------+                    +----------------------------------+ +---------------+
  | Application | ---(TCP:6379)----> |        EVENT LOOP                | | RDB Snapshot  |
  +-------------+                    |  +----------------------------+  | | (fork + COW)  |
                                     |  |   Single Threaded          |  | +---------------+
  +-------------+                    |  |   Command Processing       |  |
  | CLI / GUI   | ---(RESP)--------> |  |   - Parse Command          |  | +---------------+
  +-------------+                    |  |   - Execute in Order        |  | | AOF Log       |
                                     |  |   - Return Response         |  | | (fsync)       |
                                     |  +----------------------------+  | +---------------+
                                     |               |                   |
                                     |               v                   |
                                     |  +----------------------------+  |
                                     |  |     IN-Memory STORE        |  |
                                     |  |                            |  |
                                     |  |  [String] [List] [Set]     |  |
                                     |  |  [Hash] [ZSet] [Stream]    |  |
                                     |  |                            |  |
                                     |  |  Key -> Value Pointers     |  |
                                     |  +----------------------------+  |
                                     +----------------------------------+

========================================================================================================
                              [ REDIS CLUSTER TOPOLOGY ]
========================================================================================================

                     +-------------------------------------------+
                     |           Client Application              |
                     +-------------------------------------------+
                                      |
                    (Redirect to correct node based on key slot)
                                      |
         +----------------------------+----------------------------+
         |                            |                            |
         v                            v                            v
  +-------------+              +-------------+              +-------------+
  |   Master 1  |◄---(Replicate)---|   Master 2  |◄---(Replicate)---|   Master 3  |
  | Slots: 0-5460 |              | Slots: 5461-10922 |         | Slots: 10923-16383 |
  +-------------+              +-------------+              +-------------+
         |                            |                            |
         v                            v                            v
  +-------------+              +-------------+              +-------------+
  |  Replica 1  |              |  Replica 2  |              |  Replica 3  |
  +-------------+              +-------------+              +-------------+

  Total Slots: 16384 (CRC16(key) % 16384)
  High Availability: Automatic failover if master fails

========================================================================================================
                              [ REDIS DATA STRUCTURES ]
========================================================================================================

  STRING                          LIST                          SET
  +------------------+           +------------------+          +------------------+
  | Key: "user:123"  |           | Key: "timeline"  |          | Key: "tags:redis"|
  | Value: "John"    |           | Head -> [1,2,3]  |          | Members: {       |
  +------------------+           | Tail -> [7,8,9]  |          |   "nosql",       |
                                 +------------------+          |   "database",    |
  HASH                           ZSET (Sorted Set)             |   "cache"        }
  +------------------+           +------------------+          +------------------+
  | Key: "user:123"  |           | Key: "leaderboard"|
  | Fields:          |           | Member -> Score   |
  |  name: "John"    |           | "alice" -> 100    |
  |  age: 30         |           | "bob" -> 95       |
  |  city: "Seoul"   |           +------------------+
  +------------------+           Skip List: O(log N) for
                                 range queries

========================================================================================================
```

### 심층 동작 원리: 싱글 스레드 성능의 비밀

**1. 이벤트 루프와 비동기 I/O**
```c
// Redis 이벤트 루프 (단순화된 의사코드)
void aeMain(aeEventLoop *eventLoop) {
    while (!eventLoop->stop) {
        // 1. I/O Multiplexing: 준비된 파일 디스크립터 확인
        numevents = aeApiPoll(eventLoop, tvp);

        for (j = 0; j < numevents; j++) {
            aeFileEvent *fe = &eventLoop->events[eventLoop->fired[j].fd];

            // 2. 읽기 이벤트 처리 (클라이언트 요청)
            if (fe->mask & mask & AE_READABLE) {
                fe->rfileProc(eventLoop, fd, fe->clientData, mask);
            }

            // 3. 쓰기 이벤트 처리 (응답 전송)
            if (fe->mask & mask & AE_WRITABLE) {
                fe->wfileProc(eventLoop, fd, fe->clientData, mask);
            }
        }
    }
}

// 왜 싱글 스레드인데 빠른가?
// 1. 메모리 접근: 디스크 I/O 없음
// 2. 락 없음: 동기화 오버헤드 없음
// 3. 컨텍스트 스위치 없음: CPU 캐시 친화적
// 4. O(1)/O(log N) 연산: 복잡한 연산 없음
```

**2. 자료구조별 활용 예시**
```python
# Redis Python Client (redis-py) 활용 예시
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

# ===== String: 캐시 및 카운터 =====
# 캐시
r.set('user:123', json.dumps({'name': 'John', 'age': 30}), ex=3600)  # 1시간 TTL
user = json.loads(r.get('user:123'))

# 카운터 (원자적)
r.incr('page_views')
r.incrby('likes', 10)

# ===== List: 메시지 큐 =====
# Producer
r.lpush('task_queue', json.dumps({'task': 'send_email', 'user_id': 123}))

# Consumer (Blocking)
task = json.loads(r.brpop('task_queue', timeout=30)[1])

# ===== Hash: 사용자 프로필 =====
r.hset('user:123:profile', mapping={
    'name': 'John',
    'email': 'john@example.com',
    'created_at': '2024-01-01'
})
profile = r.hgetall('user:123:profile')

# ===== Set: 태그 및 관계 =====
r.sadd('post:1:tags', 'redis', 'nosql', 'database')
r.sadd('post:2:tags', 'redis', 'cache')
common_tags = r.sinter('post:1:tags', 'post:2:tags')  # 교집합

# ===== Sorted Set: 랭킹 =====
r.zadd('leaderboard', {'player1': 100, 'player2': 95, 'player3': 88})
top_10 = r.zrevrange('leaderboard', 0, 9, withscores=True)
my_rank = r.zrevrank('leaderboard', 'player1')

# ===== Stream: 이벤트 로그 =====
r.xadd('events', {'type': 'click', 'user_id': 123, 'page': '/home'})
events = r.xread({'events': '0'}, count=10)

# ===== Pub/Sub: 실시간 메시징 =====
pubsub = r.pubsub()
pubsub.subscribe('notifications')
for message in pubsub.listen():
    print(message['data'])
```

**3. Redis Cluster 샤딩**
```text
Redis Cluster 샤딩 메커니즘:

1. 해시 슬롯 할당
   - 총 16384개 슬롯
   - CRC16(key) % 16384 = 슬롯 번호
   - 각 마스터 노드에 슬롯 범위 할당

2. 키 분산 예시
   - "user:123" → CRC16("user:123") % 16384 = 5678 → Master 1
   - "session:abc" → CRC16("session:abc") % 16384 = 8901 → Master 2

3. 해시태그 (같은 슬롯 보장)
   - "user:{123}:profile"과 "user:{123}:settings"는 같은 슬롯
   - 중괄호 {} 내의 문자열만 해싱에 사용

4. 장애 복구
   - Master 장애 시 Replica가 자동 승격
   - 과반수 마스터 동의 필요
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Redis vs Memcached vs DynamoDB (DAX)

| 비교 지표 | Redis | Memcached | DynamoDB DAX |
|---|---|---|---|
| **자료구조** | 다양 (6+ 종류) | String만 | Key-Value |
| **영속성** | O (RDB/AOF) | X | O (DynamoDB) |
| **복제** | O (Cluster) | X | O (Managed) |
| **트랜잭션** | O (MULTI/EXEC) | X | O |
| **Pub/Sub** | O | X | X |
| **지연 시간** | < 1ms | < 1ms | < 1ms |
| **메모리 효율** | 중간 | 높음 | N/A (Managed) |
| **운영 복잡도** | 중간 | 낮음 | 낮음 (Managed) |

### 과목 융합 관점 분석

- **[운영체제 + Redis]**: Redis의 성능은 **메모리 관리**와 **페이지 캐시**에 크게 의존합니다. fork() 시스템 콜을 사용한 RDB 스냅샷은 **Copy-on-Write(COW)** 기법으로 메모리를 절약합니다.

- **[네트워크 + Redis]**: Redis는 **RESP(Redis Serialization Protocol)**라는 자체 프로토콜을 사용합니다. 파이프라이닝으로 여러 명령을 한 번에 전송하여 RTT를 줄입니다.

- **[데이터베이스 + Redis]**: Redis는 **Write-Behind/Read-Through 캐시** 패턴으로 RDBMS 앞단에 배치됩니다. Cache-Aside 패턴으로 애플리케이션이 직접 관리하기도 합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**시나리오 1: 세션 저장소 구축**
- **문제**: 수백만 동시 접속자의 세션을 RDBMS에 저장하면 부하 급증
- **전략적 의사결정**:
  1. **Redis 선택**: Hash 자료구조로 세션 속성 저장
  2. **TTL 설정**: 30분 비활동 시 자동 만료
  3. **Cluster 구성**: 6노드(3 Master + 3 Replica)로 확장성 확보
  4. **Persistence**: AOF로 장애 시 세션 복구

**시나리오 2: 실시간 리더보드**
- **문제**: 게임 내 100만 명 플레이어의 실시간 랭킹
- **전략적 의사결정**:
  1. **Sorted Set 활용**: ZADD/ZREVRANGE로 O(log N) 연산
  2. **주기적 스냅샷**: 매 시간 RDB 백업
  3. **Read Replica**: 읽기 부하 분산

**시나리오 3: Rate Limiting**
- **문제**: API 호출 횟수 제한 (사용자당 100회/분)
- **전략적 의사결정**:
  1. **Token Bucket**: String + INCR + EXPIRE
  2. **Sliding Window**: Sorted Set으로 정밀 제어
  3. **Lua Script**: 원자적 연산 보장

### 주의사항 및 안티패턴 (Anti-patterns)

- **안티패턴 - KEYS * 사용**: 모든 키를 스캔하면 블로킹 발생. **SCAN** 명령 사용

- **안티패턴 - 큰 Value**: 10MB 이상의 값은 성능 저하. **청킹** 또는 별도 스토리지 사용

- **안티패턴 - O(N) 연산 남용**: LRANGE 0 -1, SMEMBERS 등은 주의. **COUNT 제한**

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | 내용 및 지표 |
|---|---|
| **정성적 효과** | - 서브밀리초 응답으로 UX 향상<br>- RDBMS 부하 감소<br>- 다양한 자료구조로 복잡한 로직 단순화 |
| **정량적 효과** | - 응답 시간 **99% 단축** (RDBMS 대비)<br>- 처리량 **10~100배 향상**<br>- 인프라 비용 **50% 절감** |

### 미래 전망 및 진화 방향

- **Redis Stack**: JSON, Search, TimeSeries, Bloom Filter 모듈 통합
- **Redis on Flash**: SSD를 활용한 비용 효율적 대용량 저장
- **Active-Active Replication**: 멀티 리전 쓰기 지원 (Redis Enterprise)

**※ 참고 표준/가이드**:
- **Redis Documentation**: 공식 문서 및 Best Practices
- **Redis Labs Academy**: 공식 교육 자료

---

## 📌 관련 개념 맵 (Knowledge Graph)

- `[Memcached](@/studynotes/16_bigdata/05_nosql/memcached.md)`: Redis의 전신인 캐시 시스템
- `[Cache Patterns](@/studynotes/16_bigdata/08_platform/cache_patterns.md)`: Cache-Aside, Read-Through 등
- `[Rate Limiting](@/studynotes/16_bigdata/08_platform/rate_limiting.md)`: API 호출 제한 패턴
- `[Pub/Sub](@/studynotes/16_bigdata/03_streaming/pub_sub.md)**: 메시지 브로드캐스트 패턴
- `[Sorted Set](@/studynotes/16_bigdata/05_nosql/redis_sorted_set.md)`: 랭킹 구현을 위한 자료구조

---

## 👶 어린이를 위한 3줄 비유 설명

1. **Redis가 뭔가요?**: **초고속 물건 보관함**이에요. 보관함을 열자마자 바로 물건을 꺼낼 수 있어서 엄청나게 빨라요!
2. **왜 빠른가요?**: 다른 보관함은 창고(디스크)까지 걸어가야 하는데, Redis는 **내 방(메모리)**에 있어서 눈 깜빡할 사이에 찾을 수 있어요.
3. **어디에 쓰나요?**: 로그인 정보, 장바구니, 게임 점수판 같이 **빠르게 확인해야 하는 것들**을 저장해요. 그래서 쇼핑몰이나 게임에서 많이 써요!
