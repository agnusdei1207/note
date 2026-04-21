import os
BASE = "/Users/pf/workspace/brainscience/content/studynote/07_enterprise_systems/05_data_bi"
def w(fn, txt):
    path = os.path.join(BASE, fn)
    if os.path.exists(path): print(f"SKIP: {fn}"); return
    with open(path, 'w', encoding='utf-8') as f: f.write(txt)
    print(f"OK: {fn}")

w("315_nosql_base_cap_theorem.md", """\
+++
weight = 315
title = "315. NoSQL BASE 결과적 일관성 CAP 정리 트레이드오프 (NoSQL BASE CAP Theorem)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CAP 정리는 분산 시스템이 Consistency(일관성), Availability(가용성), Partition Tolerance(분단 내성) 셋 중 둘만 동시에 완전히 보장할 수 있다는 이론이다.
> 2. **가치**: BASE (Basically Available, Soft state, Eventually consistent)는 CAP의 AP 선택 결과로, 높은 가용성과 수평 확장을 택하는 대신 일시적 불일관성을 허용한다.
> 3. **판단 포인트**: 금융 거래·재고 관리는 ACID/CP가 필수이고, 소셜 피드·장바구니는 BASE/AP로 가용성 우선이 적합하다.

## Ⅰ. 개요 및 필요성

단일 서버 관계형 DB는 ACID (Atomicity, Consistency, Isolation, Durability) 트랜잭션으로 강한 일관성을 보장한다.
그러나 수평 확장이 필요한 분산 시스템에서는 네트워크 분단(Partition)이 반드시 발생하므로, Eric Brewer가 2000년에 발표한 CAP 정리에 따라 C 또는 A 중 하나를 타협해야 한다.

CAP 정리 3 속성:
- **Consistency (C)**: 모든 노드가 동일 시점에 동일 데이터를 봄
- **Availability (A)**: 모든 요청이 응답을 받음 (오류 없이)
- **Partition Tolerance (P)**: 네트워크 분단 상황에서도 동작 지속

실제 분산 시스템에서 P는 포기할 수 없으므로 CP 또는 AP를 선택한다.

📢 **섹션 요약 비유**: CAP는 "맛있고, 빠르고, 저렴한" 식당의 삼각형이다. 세 가지를 동시에 모두 갖추기는 불가능하다.

## Ⅱ. 아키텍처 및 핵심 원리

### CP vs AP 시스템 분류

| 분류 | 특징 | 대표 DB |
|:---|:---|:---|
| CP (일관성+분단 내성) | 분단 시 응답 거부, 일관성 보장 | HBase, Zookeeper, MongoDB(w:majority) |
| AP (가용성+분단 내성) | 분단 시에도 응답, 일시적 불일관성 | Cassandra, DynamoDB, CouchDB |
| CA (이론적 구분) | 분산 아닌 단일 서버 | 전통 RDBMS (MySQL, PostgreSQL) |

### BASE vs ACID 비교

| 항목 | ACID | BASE |
|:---|:---|:---|
| Atomicity | 전체 성공 or 전체 롤백 | 최선의 결과 시도 |
| Consistency | 트랜잭션 후 항상 일관 | 결과적 일관성 (Eventually) |
| Isolation | 트랜잭션 간 완전 격리 | 약한 격리 (동시성 증가) |
| Durability vs Soft state | 영속 보장 | 일시적 상태 허용 |
| 확장성 | 수직 확장 한계 | 수평 확장 용이 |

### ASCII 다이어그램: CAP 삼각형과 DB 배치

```
  ┌─────────────────────────────────────────────────────────────┐
  │                  CAP 삼각형                                  │
  │                                                             │
  │                Consistency (C)                              │
  │                      △                                      │
  │                     / \                                     │
  │                    /   \                                    │
  │                   /     \                                   │
  │         CP 영역  /       \  (불가능 영역)                    │
  │                 /         \                                 │
  │        HBase   /           \  MongoDB                      │
  │     Zookeeper ●             ● (default)                    │
  │               /    ×전부     \                              │
  │              / (이론상 불가)  \                              │
  │             /─────────────────\                            │
  │            /                   \                           │
  │ Partition ●                     ● Availability             │
  │ Tolerance  \       AP 영역      /  (A)                     │
  │    (P)      \                  /                           │
  │              \ Cassandra      /                            │
  │               ● DynamoDB ●   /                             │
  │                \  CouchDB   /                              │
  │                 ●──────────●                               │
  │                                                             │
  │  RDBMS (MySQL, PostgreSQL): 단일 서버 → CA 영역 (P 포기)    │
  └─────────────────────────────────────────────────────────────┘
```

### 일관성 레벨 스펙트럼

| 레벨 | 설명 | 지연 | 사용 예 |
|:---|:---|:---|:---|
| Strong (강한 일관성) | 모든 노드 즉시 동일 | 높음 | 금융 잔액 |
| Bounded Staleness | N초 이내 일관성 보장 | 중간 | 재고 조회 |
| Session | 같은 세션 내 일관성 | 낮음 | 사용자 프로필 |
| Eventual (결과적 일관성) | 언젠가 일관 (수ms~수초) | 매우 낮음 | 소셜 피드, 장바구니 |

📢 **섹션 요약 비유**: 결과적 일관성은 소문이다. 처음엔 사람마다 다르게 알지만, 시간이 지나면 모두 같은 내용을 알게 된다.

## Ⅲ. 비교 및 연결

### PACELC 확장 정리

CAP의 한계를 보완한 PACELC (Partition → AP or CP, Else → Latency or Consistency):
- **분단 시 (P)**: A(가용성) vs C(일관성) 선택
- **정상 시 (E)**: L(지연) vs C(일관성) 트레이드오프

| DB | 분단 시 | 정상 시 |
|:---|:---|:---|
| Cassandra | AP | EL (지연 최소화) |
| DynamoDB | AP | EL |
| HBase | CP | EC (일관성 강조) |
| MongoDB | CP (default) | EC |

📢 **섹션 요약 비유**: PACELC는 CAP보다 현실적인 지도다. 평상시 운전 규칙(Else)과 사고 시 대응(Partition)을 모두 다룬다.

## Ⅳ. 실무 적용 및 기술사 판단

### 일관성 모델 선택 체크리스트

- [ ] 데이터의 금전적 가치가 있는가? (은행 잔액 → CP/ACID 필수)
- [ ] 일시적 불일관성이 비즈니스에 허용 가능한가? (좋아요 수 → AP/BASE OK)
- [ ] 지리적 분산 배포 필요 여부 (멀티 리전 → AP 선호)
- [ ] 99.99% 이상 가용성 요건 → AP 우선 고려

### 안티패턴

| 안티패턴 | 문제 | 해결 방법 |
|:---|:---|:---|
| 재고 차감에 Cassandra AP | 동시 구매 시 재고 초과 판매 | CP DB (HBase, Redis SETNX) 사용 |
| 모든 NoSQL에 ACID 기대 | Cassandra는 Eventual Consistency | LWT (Light-weight Transaction) 사용 |

📢 **섹션 요약 비유**: 재고 차감에 AP DB를 쓰는 건 여러 계산대에서 동시에 마지막 상품을 판매하는 것이다. 손님 2명이 같은 물건을 사고 집에 가면 한 명은 빈손이다.

## Ⅴ. 기대효과 및 결론

### BASE 설계 적합 영역

| 도메인 | 일관성 모델 | 이유 |
|:---|:---|:---|
| 소셜 피드, 댓글 | BASE/AP | 좋아요 수 수초 차이 무방 |
| 장바구니 | BASE/AP | 임시 불일관성 허용 |
| 재고 관리 | ACID/CP | 초과 판매 불가 |
| 금융 이체 | ACID/CP | 원자성 필수 |

📢 **섹션 요약 비유**: 은행 계좌는 ACID(금고), 소셜 피드는 BASE(게시판)다. 금고는 느려도 확실해야 하고, 게시판은 빠르되 잠깐 틀려도 괜찮다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| CAP 정리 | 이론 기반 | C/A/P 셋 중 둘만 보장 |
| ACID | 트랜잭션 모델 | CP 계열 일관성 보장 |
| BASE | 일관성 모델 | AP 계열 결과적 일관성 |
| PACELC | 확장 이론 | 정상 시 Latency vs Consistency |
| Eventual Consistency | 상태 | 시간 경과 후 일관성 수렴 |

### 👶 어린이를 위한 3줄 비유 설명

1. CAP는 "맛있고 빠르고 저렴한 식당"처럼 세 가지를 동시에 다 가질 수 없다는 법칙이에요.
2. ACID는 은행 금고처럼 느리지만 확실한 것, BASE는 소문처럼 빠르지만 잠깐 틀릴 수 있는 것이에요.
3. Eventual Consistency는 "나중엔 다 같아져요"라는 약속이에요. 지금 당장은 달라도 괜찮아요.
""")

w("316_redis_thundering_herd.md", """\
+++
weight = 316
title = "316. Redis 데이터 스탬피드 Thundering Herd 장애 회피 (Redis Thundering Herd)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Thundering Herd (캐시 스탬피드)는 캐시가 만료된 순간 수천 개의 요청이 동시에 DB를 공격하여 DB를 마비시키는 장애 패턴이다.
> 2. **가치**: Redis SETNX 기반 분산 락과 Probabilistic Early Expiration, TTL Jitter를 조합하면 초당 10,000 req/s 환경에서도 DB 쿼리를 1~5건으로 제한할 수 있다.
> 3. **판단 포인트**: 캐시 TTL이 짧고 동시 접속자가 많을수록 위험도가 높으며, 핫 키(Hot Key)에 대한 사전 예방 설계가 필수다.

## Ⅰ. 개요 및 필요성

캐시(Redis)는 DB 부하를 90% 이상 감소시키지만, 캐시 만료(TTL 0)와 대량 동시 요청이 겹치면 모든 요청이 동시에 DB를 호출하는 Cache Stampede (캐시 스탬피드, Thundering Herd)가 발생한다.

발생 메커니즘:
1. 캐시 TTL 만료
2. 동시 요청 10,000건이 캐시 미스 감지
3. 모두 DB에 동일 쿼리 전송
4. DB CPU 100%, 응답 시간 폭증, 서비스 마비

Dog-pile Effect라고도 불리며, 인기 있는 콘텐츠(핫 키)일수록 피해가 크다.

대표 시나리오:
- 뉴스 속보: 동시 접속자 100,000명 → 기사 캐시 만료 → DB 폭주
- 주요 상품 페이지: 세일 시작 동시 캐시 만료

📢 **섹션 요약 비유**: Thundering Herd는 건물 비상구가 갑자기 열리는 순간 모두가 동시에 달려가 문이 막히는 상황이다.

## Ⅱ. 아키텍처 및 핵심 원리

### 해결 전략 비교

| 전략 | 방법 | 장점 | 단점 |
|:---|:---|:---|:---|
| Mutex Lock | SETNX로 1개 요청만 DB 조회, 나머지 대기 | 정확한 제어 | 지연 발생 (Lock 대기) |
| Probabilistic Early Expiration | TTL 소진 전 일부 요청이 미리 갱신 | 지연 없음 | 구현 복잡 |
| TTL Jitter | 만료 시간에 랜덤값 추가 | 간단 | 완전한 예방은 아님 |
| Cache Warming | 배포 전 캐시 사전 로드 | 근본 해결 | 운영 부담 |
| Local Cache | L1 로컬 캐시 + L2 Redis | DB 쿼리 0건 가능 | 메모리 사용 증가 |

### Redis SETNX 기반 분산 락

```python
# 캐시 미스 시 분산 락으로 단일 재빌드
def get_with_lock(key, ttl=300):
    value = redis.get(key)
    if value:
        return value

    lock_key = f"lock:{key}"
    # SETNX: Set if Not eXists (원자적 연산)
    acquired = redis.set(lock_key, "1", nx=True, ex=5)  # 5초 락

    if acquired:
        # 락 획득: DB 조회 후 캐시 갱신
        value = db.query(key)
        redis.setex(key, ttl, value)
        redis.delete(lock_key)
        return value
    else:
        # 락 미획득: 짧은 대기 후 재시도 (or stale cache 반환)
        time.sleep(0.05)
        return redis.get(key)  # 락 해제 후 캐시 재조회
```

### Probabilistic Early Expiration

```python
import math, random

def get_with_early_expiration(key, beta=1.0):
    value, delta, expiry = redis.get_with_meta(key)
    ttl_remaining = expiry - time.time()

    # 만료 임박 시 확률적으로 미리 갱신
    if -beta * delta * math.log(random.random()) >= ttl_remaining:
        value = db.query(key)
        redis.setex(key, TTL, value)

    return value
```

### ASCII 다이어그램: Thundering Herd vs 보호 패턴

```
  [Thundering Herd 발생]
  ┌───────────────────────────────────────────────────┐
  │  캐시 만료                                         │
  │  요청 10,000건 ──────────────────▶ DB (폭주!)      │
  │  (모두 동시에)                    CPU 100%         │
  └───────────────────────────────────────────────────┘

  [분산 락 보호 패턴]
  ┌───────────────────────────────────────────────────┐
  │  캐시 만료                                         │
  │  요청 1번 ──── SETNX 락 획득 ──▶ DB 쿼리 (1건)    │
  │  요청 2~10,000번                                   │
  │  ├── 락 대기 ──── 락 해제 후 캐시 히트 ──▶ 응답   │
  │  └── Stale Cache ──▶ 이전 캐시값 반환 ──▶ 응답     │
  │  결과: DB 쿼리 1건만 발생                          │
  └───────────────────────────────────────────────────┘
```

### TTL Jitter 적용

```python
# 동일 TTL 대신 랜덤 범위를 추가해 만료 시간 분산
base_ttl = 3600  # 1시간
jitter = random.randint(0, 600)  # ±10분 랜덤 추가
redis.setex(key, base_ttl + jitter, value)
# 결과: 동시에 여러 핫 키가 만료되는 상황 방지
```

📢 **섹션 요약 비유**: TTL Jitter는 시험 종료 시간을 학생마다 살짝 다르게 해서 모두가 동시에 문을 향해 달리는 혼잡을 방지하는 것이다.

## Ⅲ. 비교 및 연결

### 핫 키 (Hot Key) 문제

단일 캐시 키가 초당 수만 건 조회되는 경우:
- Redis 단일 노드 CPU 병목
- 해결책: Read Replica, Key Sharding (hot-key:shard:0~9), Local L1 Cache

| 방법 | 효과 | 복잡도 |
|:---|:---|:---|
| Read Replica | 읽기 부하 분산 | 낮음 |
| Key Sharding | 여러 키로 분산 | 중간 |
| Local L1 Cache | Redis 쿼리 자체 제거 | 높음 (일관성 주의) |

📢 **섹션 요약 비유**: 핫 키는 한 창구에 모든 손님이 몰리는 것이다. 창구를 늘리거나(Read Replica) 번호표로 분산하거나(Key Sharding), 손님이 직접 정보를 갖고 오게 해야 한다(L1 Cache).

## Ⅳ. 실무 적용 및 기술사 판단

### Thundering Herd 방지 체크리스트

- [ ] TTL Jitter 적용: base_ttl + random(0~10%) 적용
- [ ] 핫 키 식별: Redis `--hotkeys` 옵션으로 상위 100개 키 모니터링
- [ ] 분산 락 타임아웃: Lock TTL은 DB 쿼리 예상 시간 × 3배 설정
- [ ] Stale Cache 정책: 락 대기 중 이전 캐시값 반환 (약간의 오래된 데이터 허용)
- [ ] Cache Warming 자동화: 배포 파이프라인에 캐시 사전 로드 포함

### 안티패턴

| 안티패턴 | 문제 | 해결 방법 |
|:---|:---|:---|
| 모든 캐시 동일 TTL | 일시에 만료 → 스탬피드 | TTL Jitter 필수 |
| Lock TTL 너무 짧음 | DB 쿼리 중 락 만료 → 다중 DB 쿼리 | TTL = 쿼리 시간 × 3배 |
| Stale Cache 미사용 | 락 대기 중 에러 응답 | 이전 캐시값 임시 반환 설계 |

📢 **섹션 요약 비유**: Lock TTL이 너무 짧은 건 화장실 잠금장치 비밀번호가 문 열리기 전에 초기화되는 것이다. 다음 사람이 들어와 혼잡해진다.

## Ⅴ. 기대효과 및 결론

| 항목 | Thundering Herd 미방지 | 방지 후 |
|:---|:---|:---|
| DB 쿼리 수 (캐시 만료 시) | 10,000건/초 | 1~5건/초 |
| DB 응답 시간 | 수초~타임아웃 | 정상 범위 유지 |
| 서비스 가용성 | 장애 (DB 폭주) | 정상 |
| 사용자 경험 | 서비스 중단 | 캐시 히트율 99%+ 유지 |

📢 **섹션 요약 비유**: Thundering Herd 방지는 쇼핑몰 입장 관리다. 동시에 모두 문을 열지 않고, 줄을 세워 순서대로 입장시킨다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Thundering Herd | 장애 패턴 | 캐시 만료 동시 DB 공격 |
| SETNX | 해결 기법 | Redis 원자적 분산 락 |
| TTL Jitter | 예방 기법 | 만료 시간 랜덤 분산 |
| Cache Warming | 예방 전략 | 배포 전 캐시 사전 로드 |
| Hot Key | 연관 문제 | 단일 키 과다 조회 |
| Stale Cache | 대응 전략 | 이전 캐시값 임시 반환 |

### 👶 어린이를 위한 3줄 비유 설명

1. Thundering Herd는 학교 벨이 울리자마자 모든 학생이 교문으로 달려가 문이 막히는 것이에요.
2. 분산 락은 "한 명씩 나가세요" 선생님처럼, 한 요청만 DB에 접근하게 하는 규칙이에요.
3. TTL Jitter는 학생마다 다른 시간에 내보내서 문이 막히지 않게 하는 거예요.
""")

print("315~316 완료")
