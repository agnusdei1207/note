+++
weight = 26
title = "26. HDFS ViewFS (Virtual File System) — 다중 네임스페이스 투명 접근"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)

- **본질**: HDFS ViewFS (Virtual File System)는 HDFS 페더레이션(Federation) 환경에서 여러 개의 독립적인 네임노드(NameNode) 네임스페이스를 하나의 통합된 가상 파일 경로로 투명하게 묶어주는 클라이언트 사이드 마운트 테이블이다.
- **가치**: 사용자와 애플리케이션은 "어느 네임스페이스에 어떤 경로가 있는지" 알 필요 없이 `/user`, `/data`, `/tmp` 같은 단일 논리 경로를 사용하며, ViewFS가 내부적으로 실제 `hdfs://nn1/`, `hdfs://nn2/` 로 라우팅해 준다.
- **판단 포인트**: 클러스터 규모가 커져 단일 NameNode의 메타데이터 용량 한계(일반적으로 수억 개 파일)를 초과할 때 Federation + ViewFS 조합이 필수이며, 기존 애플리케이션 코드 변경 없이 확장 가능하다는 점이 핵심 장점이다.

---

## Ⅰ. 개요 및 필요성

### 1. HDFS 페더레이션과 ViewFS의 탄생 배경

단일 NameNode 구조의 HDFS는 메타데이터(파일 이름, 블록 위치, 권한 등)를 NameNode 메모리에 전부 올려서 관리한다. 클러스터가 수십억 개의 파일을 보유하게 되면 단일 NameNode는 다음 문제에 부딪힌다.

- **메모리 병목**: 파일 1억 개 ≒ NameNode 힙 메모리 약 60GB 이상 소모
- **단일 장애점(SPOF)**: NameNode 장애 → 전 클러스터 스토리지 접근 불가
- **처리량 병목**: 모든 메타데이터 RPC가 단일 NameNode로 집중

HDFS 페더레이션(Hadoop 2.0+)은 여러 독립적인 NameNode를 두어 네임스페이스를 분산 관리하는 방식으로 이 문제를 해결했다. 그러나 클라이언트 입장에서는 "어떤 경로가 어느 NameNode에 속하는지" 매번 파악해야 하는 복잡성이 생긴다. ViewFS는 이 복잡성을 클라이언트 레이어에서 완전히 숨겨준다.

### 2. ViewFS의 핵심 개념

ViewFS는 `core-site.xml`의 `fs.defaultFS`를 `viewfs://ClusterName`으로 지정하고, 각 논리 경로 접두사(prefix)를 실제 NameNode URI에 **마운트(Mount)** 하는 테이블을 정의한다. 이는 리눅스의 `/etc/fstab`에서 파티션을 특정 마운트 포인트에 연결하는 개념과 동일하다.

**📢 섹션 요약 비유**
> ViewFS는 "도시 전화번호부"와 같다. 전화를 걸 때 상대방이 서울 교환국인지 부산 교환국인지 몰라도 이름만 찾아 전화하면 된다. 내부 교환기(ViewFS)가 알아서 실제 회선을 연결해 준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. ViewFS 마운트 테이블 구조

```
┌─────────────────────────────────────────────────────────┐
│             클라이언트 애플리케이션 (HDFS API)              │
│          fs.defaultFS = viewfs://myCluster              │
└───────────────────────┬─────────────────────────────────┘
                        │  논리 경로 요청
                        ▼
┌─────────────────────────────────────────────────────────┐
│              ViewFS 마운트 테이블 (client-side)            │
│  ┌─────────────────┬────────────────────────────────┐   │
│  │  논리 경로       │  실제 NameNode URI              │   │
│  ├─────────────────┼────────────────────────────────┤   │
│  │  /user          │  hdfs://nn1.cluster:8020/user  │   │
│  │  /data          │  hdfs://nn2.cluster:8020/data  │   │
│  │  /tmp           │  hdfs://nn1.cluster:8020/tmp   │   │
│  │  /warehouse     │  hdfs://nn3.cluster:8020/wh    │   │
│  └─────────────────┴────────────────────────────────┘   │
└───────────┬───────────────────────┬─────────────────────┘
            │                       │
            ▼                       ▼
┌───────────────────┐   ┌───────────────────┐
│  NameNode 1 (nn1) │   │  NameNode 2 (nn2) │
│  /user, /tmp NS   │   │  /data NS          │
└───────────────────┘   └───────────────────┘
```

### 2. core-site.xml 설정 예시

```xml
<!-- ViewFS 기본 설정 -->
<property>
  <name>fs.defaultFS</name>
  <value>viewfs://myCluster</value>
</property>

<!-- 마운트 테이블 정의 -->
<property>
  <name>fs.viewfs.mounttable.myCluster.link./user</name>
  <value>hdfs://nn1.hadoop.cluster:8020/user</value>
</property>
<property>
  <name>fs.viewfs.mounttable.myCluster.link./data</name>
  <value>hdfs://nn2.hadoop.cluster:8020/data</value>
</property>
<property>
  <name>fs.viewfs.mounttable.myCluster.homedir</name>
  <value>/user</value>
</property>
```

### 3. 핵심 구성 요소 비교

| 구성 요소 | 역할 | 위치 |
|:---|:---|:---|
| 마운트 테이블 (Mount Table) | 논리 경로 → 실제 NameNode URI 매핑 | 클라이언트 `core-site.xml` |
| ViewFS FileSystem | Java `FileSystem` 추상 클래스 구현체 | Hadoop 클라이언트 라이브러리 |
| Federation NameNode | 실제 메타데이터 저장 및 제공 | 서버 측 |
| DataNode (공유) | 실제 블록 데이터 저장 | 서버 측 (모든 NS 공유 가능) |

**📢 섹션 요약 비유**
> ViewFS 마운트 테이블은 "회사 내선 번호 안내도"다. 외부에서는 대표 번호만 알고 전화하면 안내도(마운트 테이블)가 해당 부서 내선(실제 NameNode)으로 자동 연결해 준다.

---

## Ⅲ. 비교 및 연결

### 1. ViewFS vs 단일 NameSpace HDFS

| 비교 항목 | 단일 NameSpace HDFS | HDFS Federation + ViewFS |
|:---|:---|:---|
| 확장성 | 단일 NameNode 메모리 한계 | 여러 NameNode로 수평 확장 |
| 가용성 | NameNode SPOF 영향 범위 전체 | 부분 장애 격리 가능 |
| 클라이언트 투명성 | 경로 = `hdfs://nn/path` | 경로 = `viewfs://cluster/path` |
| 관리 복잡성 | 단순 | 마운트 테이블 관리 추가 |
| 메타데이터 용량 | 단일 NameNode 메모리 상한 | 네임스페이스 수만큼 선형 확장 |

### 2. ViewFS와 NFS/FUSE의 비교

ViewFS는 서버 측이 아닌 **클라이언트 측**에서 경로를 해석하는 구조이다. Linux의 NFS 마운트는 서버 측 디렉토리를 클라이언트에 마운트하지만, ViewFS는 클라이언트 라이브러리 내부에서 Java Path 재작성으로 동작한다.

### 3. 연결 개념: HDFS HA와 Federation의 차이

- **HDFS HA (High Availability)**: 하나의 네임스페이스를 Active/Standby NameNode 쌍이 공유 → 장애 복구용
- **HDFS Federation**: 여러 독립 네임스페이스를 별도 NameNode로 분산 → 확장성 향상용
- **ViewFS**: Federation 환경에서 여러 네임스페이스를 단일 논리 경로로 통합 → 투명성 제공

**📢 섹션 요약 비유**
> HDFS HA는 "백업 운전기사가 대기하는 버스"(같은 노선), Federation은 "여러 노선 버스 회사"(독립 운영), ViewFS는 "통합 교통 앱"(어느 회사 버스든 하나의 앱으로 예약)이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 1. ViewFS 도입 판단 기준

| 상황 | 권장 여부 | 근거 |
|:---|:---|:---|
| 파일 수 < 1억, 단일 클러스터 | ❌ 불필요 | 단일 NameNode로 충분 |
| 파일 수 > 3억, 메모리 부족 | ✅ 권장 | Federation + ViewFS 필수 |
| 부서/테넌트별 격리 필요 | ✅ 권장 | 네임스페이스별 접근 제어 |
| 기존 앱 코드 변경 최소화 요구 | ✅ 권장 | `viewfs://` 경로 통일로 투명 전환 |

### 2. 설계 체크리스트

- [ ] Federation NameNode 간 메타데이터 부하 균등 분배 검토
- [ ] 마운트 테이블을 클러스터 전체에 일관성 있게 배포 (Ansible/Chef 활용)
- [ ] `viewfs://` 경로를 사용하는 Spark, Hive, HBase 설정 일괄 변경
- [ ] 크로스 네임스페이스 rename 불가 → 데이터 이동 시 `distcp` 활용
- [ ] NameNode HA와 Federation 동시 적용 시 Quorum Journal Manager(QJM) 설계 검토

### 3. 주요 제약 사항

ViewFS의 **가장 큰 제약**은 서로 다른 마운트 포인트 간의 **원자적 rename 불가**이다. 예를 들어 `/data/raw` (nn2)의 파일을 `/user/processed` (nn1)로 rename하면 오류가 발생한다. 이 경우 DistCp(Distributed Copy)로 데이터를 복사 후 원본을 삭제해야 한다.

**📢 섹션 요약 비유**
> ViewFS에서 서로 다른 네임스페이스 간 rename은 "A 은행 계좌에서 B 은행 계좌로 즉시 이체" 불가인 것과 같다. 무조건 출금(복사) 후 입금(재생성)의 두 단계가 필요하다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| 선형 메타데이터 확장 | NameNode 추가만으로 수억 파일 관리 가능 |
| 부분 장애 격리 | nn2 장애 시 nn1의 `/user` 데이터 정상 접근 유지 |
| 애플리케이션 투명성 | 기존 `hdfs://` 경로 코드를 `viewfs://`로 설정 변경만으로 마이그레이션 |
| 멀티 테넌트 거버넌스 | 네임스페이스별 독립적 권한 정책(Ranger) 적용 가능 |

### 2. 한계 및 미래 전망

- **크로스 네임스페이스 작업 제약**: rename, atomic move 불가
- **마운트 테이블 중앙 관리 필요**: 클라이언트 수천 대의 `core-site.xml` 동기화 필요
- **클라우드 네이티브 대체**: 클라우드 환경에서는 S3/ADLS 같은 오브젝트 스토리지가 Federation/ViewFS의 확장성 문제를 구조적으로 해결하므로 온프레미스 대규모 하둡 클러스터에서 더 유효한 패턴이다.

### 3. 결론

HDFS ViewFS는 대규모 온프레미스 하둡 클러스터에서 **수평 확장성과 단일 논리 경로를 동시에 달성하기 위한 핵심 클라이언트 측 추상화 계층**이다. 기술사 시험에서는 "Federation의 클라이언트 복잡성 해결책"으로 출제되며, 제약(크로스 NS rename 불가)과 함께 설명해야 완성도 높은 답안이 된다.

**📢 섹션 요약 비유**
> ViewFS는 여러 창고(NameNode)에 물건을 나눠 보관하는 대형 물류회사에서, 고객이 "A동 3층 아무 창고나"라고 부르지 않고 "우리집 주소"로 주문하면 알아서 올바른 창고에서 가져다주는 **통합 배송 인터페이스**다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| HDFS Federation | 전제 조건 | ViewFS가 필요한 이유를 제공 |
| NameNode HA | 보완 기술 | 고가용성(HA)과 수평 확장(Federation)은 독립적으로 동시 적용 가능 |
| Apache Ranger | 연동 | 네임스페이스별 독립 정책으로 멀티테넌트 접근 제어 |
| DistCp (Distributed Copy) | 우회 수단 | 크로스 네임스페이스 데이터 이동 시 rename 대신 사용 |
| Hadoop 보안(Kerberos) | 전제 조건 | 멀티 NameNode 환경에서 인증 일관성 보장 필요 |

### 👶 어린이를 위한 3줄 비유 설명

집에 책 창고(nn1), 장난감 창고(nn2), 옷 창고(nn3)가 세 곳에 따로 있어도, 엄마(ViewFS)가 만들어준 **"우리 집 지도"** 를 보면 `집/책`, `집/장난감`, `집/옷`으로 부를 수 있어요. 어느 창고에 진짜 물건이 있는지 몰라도 지도에서 찾으면 엄마가 알아서 해당 창고로 데려다줘요. 단, 책 창고에서 장난감 창고로 물건을 "그 자리 이름 바꾸기"는 안 되고, 꺼내서 옮겨야 한답니다.
