+++
title = "정형 데이터 (Structured Data)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 정형 데이터 (Structured Data)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 정형 데이터는 스키마(Schema)라는 엄격한 구조적 틀에 의해 행(Row)과 열(Column)의 2차원 테이블 형태로 조직된 데이터로, 관계형 데이터베이스(RDBMS)에서 관리되는 가장 전통적이고 널리 사용되는 데이터 형식입니다.
> 2. **가치**: 명확한 데이터 타입과 제약조건(Constraint)으로 인해 데이터 무결성이 보장되며, SQL을 통한 표준화된 질의와 복잡한 조인(Join) 연산이 가능하여 비즈니스 인텔리전스(BI)와 트랜잭션 처리에 최적화되어 있습니다.
> 3. **융합**: 빅데이터 시대에 비정형 데이터와 융합되어 데이터 레이크하우스 아키텍처의 Gold Layer에서 최종 분석 모델로 활용되며, NoSQL과 뉴SQL로 진화하는 데이터베이스 기술의 근간을 형성합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**정형 데이터(Structured Data)**는 데이터가 생성되기 전에 미리 정의된 스키마(Schema)에 따라 구조화되어 저장되는 데이터를 의미합니다. 스키마는 데이터의 속성(Attribute)별로 데이터 타입(Data Type), 길이, 제약조건 등을 명시하며, 모든 데이터 레코드는 이 스키마를 준수해야 합니다. 정형 데이터의 대표적인 형태는 관계형 데이터베이스(RDBMS)의 테이블이며, 행(Row/Tuple)은 개별 레코드, 열(Column/Attribute)은 속성을 나타냅니다.

**정형 데이터의 핵심 특성**:
- **고정 스키마 (Fixed Schema)**: 테이블 생성 시 정의된 구조를 준수, 스키마 변경 시 마이그레이션 필요
- **원자성 (Atomic Values)**: 각 셀(Cell)은 더 이상 분해할 수 없는 단일 값(Atomic Value)만 보유
- **데이터 타입 (Data Types)**: INTEGER, VARCHAR, DATE, DECIMAL 등 명시적 타입 강제
- **제약조건 (Constraints)**: PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, CHECK 등 무결성 보장

#### 2. 💡 비유를 통한 이해
정형 데이터를 **'엑셀 스프레드시트'**나 **'도서관의 도서 목록 카드'**에 비유할 수 있습니다.
- **스키마**: 도서관 목록 카드에는 '제목', '저자', '출판년도', '청구기호'라는 항목이 미리 정해져 있습니다. 이 항목의 순서나 이름을 마음대로 바꿀 수 없습니다.
- **행(Row)**: 각 카드 한 장은 한 권의 책을 나타냅니다.
- **열(Column)**: '제목', '저자' 등의 항목들입니다.
- **제약조건**: 출판년도에는 반드시 숫자만 들어가야 하고, 청구기호는 중복될 수 없다는 규칙이 있습니다.

반면 비정형 데이터는 도서관에 책뿐만 아니라 그림, 음악 CD, 영화 DVD 등이 섞여 있고, 각각을 설명하는 항목이 모두 다른 것과 같습니다.

#### 3. 등장 배경 및 발전 과정
1. **초기 데이터 처리 (1960s-1970s)**: 메인프레임 시대의 계층형 데이터베이스(IMS), 네트워크형 데이터베이스(IDMS) 등이 사용되었습니다. 데이터 간의 관계 표현이 복잡하고 프로그래머가 물리적 구조를 모두 알아야 했습니다.
2. **관계형 모델의 등장 (1970)**: 에드거 F. 코드(Edgar F. Codd)가 IBM에서 관계형 데이터 모델(Relational Model)을 제안했습니다. 수학적 집합론에 기반하여 데이터를 2차원 테이블로 표현하고, SQL(Structured Query Language)이라는 선언적 질의 언어를 도입했습니다.
3. **상용 RDBMS의 발전 (1980s-1990s)**: Oracle, IBM DB2, Microsoft SQL Server, MySQL, PostgreSQL 등이 등장하여 정형 데이터 처리의 표준으로 자리 잡았습니다. ACID 트랜잭션, B+Tree 인덱스, 쿼리 옵티마이저 등의 기술이 고도화되었습니다.
4. **빅데이터 시대의 도전 (2000s-현재)**: 웹 로그, SNS, IoT 센서 데이터 등 비정형/반정형 데이터가 폭증하면서 정형 데이터만으로는 한계가 드러났습니다. 그러나 여전히 핵심 비즈니스 트랜잭션(은행, 예약, ERP)은 정형 데이터 기반입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 정형 데이터 구성 요소 (표)

| 구성 요소 | 정의 | 내부 동작 메커니즘 | 관련 SQL 문법 | 실무 활용 |
|:---|:---|:---|:---|:---|
| **테이블 (Table)** | 행과 열로 구성된 2차원 데이터 구조 | 디스크의 데이터 페이지(8KB) 단위 저장 | CREATE TABLE | 엔티티 표현 |
| **행 (Row/Tuple)** | 단일 레코드, 하나의 개체 인스턴스 | 고정 길이/가변 길이 레코드 포맷 | INSERT, UPDATE | 개별 데이터 |
| **열 (Column/Attribute)** | 동일한 속성을 가진 값들의 집합 | 데이터 타입별 정렬/압축 최적화 | ALTER TABLE ADD COLUMN | 속성 정의 |
| **스키마 (Schema)** | 테이블 구조, 타입, 제약조건 정의 | 메타데이터 카탈로그에 저장 | CREATE SCHEMA | 구조 정의 |
| **키 (Key)** | 레코드 식별 및 관계 연결 수단 | B+Tree 인덱스로 고속 검색 | PRIMARY KEY, FOREIGN KEY | 무결성 보장 |
| **인덱스 (Index)** | 검색 성능 향상을 위한 자료구조 | B+Tree, Hash, GiST 등 | CREATE INDEX | 쿼리 최적화 |
| **제약조건 (Constraint)** | 데이터 무결성 보장 규칙 | DML 시 자동 검증 | NOT NULL, UNIQUE, CHECK | 품질 관리 |

#### 2. 정형 데이터 저장 아키텍처 (ASCII 다이어그램)

```text
<<< RDBMS Structured Data Storage Architecture >>>

┌─────────────────────────────────────────────────────────────────────────┐
│                        SQL Query Layer                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Parser    │->│  Optimizer  │->│  Executor   │->│ Result Set  │    │
│  │ (SQL 파싱)  │  │ (실행계획)  │  │ (연산수행)  │  │ (결과반환)  │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
┌─────────────────────────────────────────────────────────────────────────┐
│                     Buffer Pool Manager (인메모리)                       │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Buffer Pool (LRU 알고리즘 기반 페이지 캐싱)                       │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │  │
│  │  │ Page 1  │ │ Page 2  │ │ Page 3  │ │ Page 4  │ │ Page 5  │    │  │
│  │  │(Dirty)  │ │(Clean)  │ │(Pinned) │ │(Clean)  │ │(Dirty)  │    │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘    │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
┌─────────────────────────────────────────────────────────────────────────┐
│                    Storage Engine (디스크 영속화)                        │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Table Space (ibd 파일)                                          │    │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │    │
│  │  │  Extent 1     │  │  Extent 2     │  │  Extent 3     │       │    │
│  │  │ (64 Pages)    │  │ (64 Pages)    │  │ (64 Pages)    │       │    │
│  │  │ 1MB 블록      │  │ 1MB 블록      │  │ 1MB 블록      │       │    │
│  │  └───────────────┘  └───────────────┘  └───────────────┘       │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  B+Tree Index Structure                                          │    │
│  │                                                                   │    │
│  │         [Root Node: 50]                                          │    │
│  │              /        \                                          │    │
│  │       [25, 40]       [60, 75, 90]  (Internal Nodes)             │    │
│  │       /   |   \       /   |   \   \                             │    │
│  │    [Leaf] [Leaf] [Leaf] [Leaf] [Leaf] [Leaf]                    │    │
│  │    (실제 데이터 레코드 또는 레코드 포인터)                        │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 3. 심층 동작 원리: B+Tree 인덱스와 정형 데이터 검색

**B+Tree 인덱스 구조의 핵심 원리**:
```python
"""
B+Tree 인덱스 동작 원리 (Python 의사코드)
- 내부 노드(Internal Node): 키만 저장, 자식 포인터 관리
- 리프 노드(Leaf Node): 키 + 데이터 포인터(또는 실제 데이터) 저장
- 리프 노드 간 연결 리스트: 범위 검색(Range Scan) 최적화
"""

class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.keys = []           # 정렬된 키 리스트
        self.children = []       # 자식 노드 포인터
        self.is_leaf = is_leaf   # 리프 노드 여부
        self.next_leaf = None    # 리프 노드 간 연결 (범위 스캔용)

    def search(self, key):
        """키 검색: O(log N) 시간 복잡도"""
        if self.is_leaf:
            # 리프 노드에서 이진 탐색
            return binary_search(self.keys, key)

        # 내부 노드: 적절한 자식으로 이동
        for i, k in enumerate(self.keys):
            if key < k:
                return self.children[i].search(key)
        return self.children[-1].search(key)

    def range_scan(self, start_key, end_key):
        """범위 검색: 리프 노드 연결 리스트 활용"""
        results = []
        current = self._find_leaf(start_key)

        while current:
            for key, value in zip(current.keys, current.values):
                if start_key <= key <= end_key:
                    results.append((key, value))
                elif key > end_key:
                    return results
            current = current.next_leaf  # 다음 리프 노드로 이동
        return results

# B+Tree의 팬아웃(Fan-out): 한 노드가 가질 수 있는 최대 자식 수
# 계산: 팬아웃 = 페이지_크기 / (키_크기 + 포인터_크기)
# 예: 8KB 페이지, 8바이트 키, 8바이트 포인터 → 약 512개 자식
# 트리 높이 = log_512(N), 1억 건 데이터도 3단계면 검색 가능
```

**정형 데이터 스키마 설계 예시**:
```sql
-- 전자상거래 주문 테이블 스키마 설계
CREATE TABLE orders (
    -- 기본키: 클러스터드 인덱스 자동 생성
    order_id BIGINT PRIMARY KEY AUTO_INCREMENT,

    -- 외래키: 참조 무결성 보장
    customer_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,

    -- 비즈니스 속성: 명시적 데이터 타입
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0),
    total_amount DECIMAL(12, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    status ENUM('PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED') NOT NULL DEFAULT 'PENDING',

    -- 메타데이터
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- 제약조건
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT,
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT,

    -- 인덱스 (비클러스터드)
    INDEX idx_order_date (order_date),
    INDEX idx_customer_status (customer_id, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 정형 데이터의 핵심: 스키마 온 라이트 (Schema-on-Write)
-- 데이터 적재 시점에 타입, 제약조건 검증 → 무결성 보장
```

#### 4. 정형 데이터 vs 반정형/비정형 데이터 처리 코드 비교

```python
import pandas as pd
import json

# 1. 정형 데이터 처리 (CSV → DataFrame)
# 스키마가 명확히 정의됨
structured_data = """
order_id,customer_id,product_id,quantity,unit_price
1001,5001,2001,2,29900
1002,5002,2002,1,15000
1003,5001,2003,3,8500
"""

df = pd.read_csv(pd.io.common.StringIO(structured_data))
print(df.dtypes)
# order_id       int64
# customer_id    int64
# product_id     int64
# quantity       int64
# unit_price     int64
# dtype: object

# 타입 기반 연산이 안전하게 수행됨
total = (df['quantity'] * df['unit_price']).sum()

# 2. 반정형 데이터 처리 (JSON)
# 스키마가 데이터 내부에 포함됨
semi_structured = """
{"order_id": 1001, "customer": {"id": 5001, "name": "홍길동"}, "items": [{"product_id": 2001, "qty": 2}]}
{"order_id": 1002, "customer": {"id": 5002}, "items": [{"product_id": 2002, "qty": 1, "discount": 0.1}]}
{"order_id": 1003, "customer_id": 5003, "product_id": 2003, "quantity": 3}
"""

# 각 레코드마다 구조가 다를 수 있음 → Schema-on-Read 시 동적 파싱 필요
records = [json.loads(line) for line in semi_structured.strip().split('\n')]

# 3. 스키마 추론 및 정형화 과정
def normalize_record(record):
    """반정형 데이터를 정형 데이터로 변환"""
    normalized = {
        'order_id': record.get('order_id'),
        'customer_id': record.get('customer', {}).get('id') or record.get('customer_id'),
        'product_id': record.get('items', [{}])[0].get('product_id') or record.get('product_id'),
        'quantity': record.get('items', [{}])[0].get('qty') or record.get('quantity'),
    }
    return normalized

normalized_df = pd.DataFrame([normalize_record(r) for r in records])
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 데이터 유형별 특성 비교표

| 비교 항목 | 정형 데이터 (Structured) | 반정형 데이터 (Semi-structured) | 비정형 데이터 (Unstructured) |
|:---|:---|:---|:---|
| **스키마** | 고정, 사전 정의 (Schema-on-Write) | 유연, 데이터 내 포함 | 무스키마 |
| **저장 형태** | RDBMS 테이블 | JSON, XML, Parquet | 이미지, 비디오, 텍스트 |
| **질의 언어** | SQL (표준화) | JSONPath, XPath, SQL 확장 | 전용 API, ML 모델 |
| **무결성** | ACID 트랜잭션 보장 | 제한적 보장 | 보장 없음 |
| **확장성** | 수직 확장 위주 (Scale-up) | 수평 확장 용이 | 수평 확장 필수 |
| **분석 방식** | 집계, 피벗, 조인 | 중첩 구조 Flatten | 특성 추출 (Feature Extraction) |
| **예시** | 은행 거래 내역, ERP | API 로그, 설정 파일 | CCTV 영상, 음성 |

#### 2. 데이터베이스 관점 분석: 정형 데이터와 ACID

**ACID 트랜잭션과 정형 데이터의 관계**:
- **Atomicity (원자성)**: 정형 데이터의 행 단위 연산(INSERT, UPDATE, DELETE)은 전체가 성공하거나 전체가 실패해야 합니다. WAL(Write-Ahead Logging)과 Undo Log를 통해 구현됩니다.
- **Consistency (일관성)**: 제약조건(PK, FK, CHECK 등)이 트랜잭션 종료 시점에 항상 만족되어야 합니다. 정형 데이터의 스키마가 이를 보장합니다.
- **Isolation (격리성)**: 동시에 실행되는 트랜잭션이 서로 간섭하지 않아야 합니다. MVCC(Multi-Version Concurrency Control)나 Locking을 통해 구현됩니다.
- **Durability (지속성)**: 커밋된 트랜잭션은 시스템 장애 후에도 복구 가능해야 합니다. Redo Log와 체크포인트를 통해 보장됩니다.

```python
# ACID 트랜잭션 예시 (Python + SQLAlchemy)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://user:pass@localhost/db')
Session = sessionmaker(bind=engine)

def transfer_money(from_account, to_account, amount):
    """은행 이체: ACID 트랜잭션 보장"""
    session = Session()
    try:
        # Atomicity: 두 UPDATE가 모두 성공하거나 모두 실패
        session.execute(
            "UPDATE accounts SET balance = balance - :amt WHERE id = :id",
            {"amt": amount, "id": from_account}
        )
        session.execute(
            "UPDATE accounts SET balance = balance + :amt WHERE id = :id",
            {"amt": amount, "id": to_account}
        )

        # Consistency: CHECK 제약조건 (balance >= 0) 검증
        session.commit()  # Durability: 커밋 시 로그에 기록
    except Exception as e:
        session.rollback()  # Atomicity: 실패 시 전체 롤백
        raise e
    finally:
        session.close()
```

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 핀테크 핵심 시스템의 정형 데이터 설계**
- **상황**: 초당 10만 건의 거래가 발생하는 결제 시스템의 데이터 모델링
- **핵심 요구사항**: ACID 트랜잭션, 무결성, 감사 추적
- **기술사적 판단**:
  - 정형 데이터 기반 RDBMS가 필수 (MySQL, PostgreSQL, Oracle)
  - 샤딩은 거래 ID 해시 기반으로 하되, 동일 사용자의 거래는 동일 샤드에 배치
  - 감사 로그는 별도 테이블에 Trigger 또는 CDC로 자동 기록
  - 핫 데이터(최근 3개월)는 SSD, 콜드 데이터는 Object Storage로 이관

**시나리오 2: 데이터 레이크하우스에서 정형 데이터의 위치**
- **상황**: 데이터 레이크(S3)에 로그, 이미지 등을 저장하고, 분석 결과를 정형화
- **아키텍처**:
  - Bronze Layer: 원천 데이터 (비정형/반정형)
  - Silver Layer: 정제된 데이터 (반정형 → 정형 변환)
  - Gold Layer: 분석용 모델 (완전한 정형 데이터, Star Schema)

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **스키마 설계**: 정규화(3NF) vs 반정규화(Denormalization) 트레이드오프 분석
- [ ] **인덱스 전략**: 쿼리 패턴 분석 후 적절한 인덱스 생성 (단일, 복합, 커버링)
- [ ] **파티셔닝**: 대용량 테이블의 Range/Hash/List 파티셔닝 검토
- [ ] **데이터 타입**: 과도한 VARCHAR 사용 지양, 적절한 타입 선정으로 저장 공간 최적화
- [ ] **제약조건**: 비즈니스 규칙을 DB 레벨 제약조건으로 구현할지 애플리케이션 레벨에서 처리할지 결정

#### 3. 안티패턴 (Anti-patterns)

- **God Table**: 하나의 테이블에 수백 개의 컬럼을 넣는 것. 정규화를 통해 적절히 분리해야 합니다.
- **인덱스 과다**: 쓰기 성능 저하. 필요한 인덱스만 유지하고 미사용 인덱스는 제거해야 합니다.
- **암시적 타입 변환**: WHERE 절에서 문자열과 숫자 비교 시 인덱스를 타지 않는 문제.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 구분 | 정형 데이터 적용 효과 |
|:---|:---|
| **데이터 품질** | 스키마 제약으로 무결성 99.9%+ 보장 |
| **쿼리 성능** | B+Tree 인덱스로 O(log N) 검색, 범위 스캔 최적화 |
| **개발 생산성** | SQL 표준으로 다양한 도구 호환, ORM 활용 가능 |
| **규제 준수** | ACID 트랜잭션, 감사 로그로 금융/의료 규제 충족 |

#### 2. 미래 전망
정형 데이터는 여전히 핵심 트랜잭션 시스템의 주류이지만, **HTAP(Hybrid Transactional/Analytical Processing)** 데이터베이스(TiDB, CockroachDB)의 등장으로 OLTP와 OLAP의 경계가 흐려지고 있습니다. 또한 **데이터 레이크하우스**의 Gold Layer에서 최종 분석 모델로 활용되며, AI/ML 피처 스토어의 정형 피처 데이터로 변환되어 활용됩니다.

#### 3. 참고 표준
- **SQL:2016 (ISO/IEC 9075)**: 관계형 데이터베이스 표준 언어
- **Codd's 12 Rules**: 관계형 데이터베이스의 12가지 규칙 (Edgar F. Codd, 1985)

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[반정형 데이터 (Semi-structured Data)](@/studynotes/14_data_engineering/01_data_arch/semi_structured_data.md)**: JSON, XML 등 스키마가 데이터 내부에 포함된 형태
- **[비정형 데이터 (Unstructured Data)](@/studynotes/14_data_engineering/01_data_arch/unstructured_data.md)**: 텍스트, 이미지 등 스키마가 없는 데이터
- **[데이터 웨어하우스 (Data Warehouse)](@/studynotes/14_data_engineering/01_data_arch/data_warehouse.md)**: 정형 데이터 기반 분석 저장소
- **[스키마 온 라이트 (Schema-on-Write)](@/studynotes/14_data_engineering/01_data_arch/schema_on_write.md)**: 정형 데이터의 쓰기 시 스키마 검증 방식
- **[데이터 레이크하우스 (Data Lakehouse)](@/studynotes/14_data_engineering/01_data_arch/data_lakehouse.md)**: 정형/비정형 데이터 통합 플랫폼

---

### 👶 어린이를 위한 3줄 비유 설명
1. **학교 출석부**: 정형 데이터는 학교 출석부처럼 번호, 이름, 출석 여부가 정해진 칸에 딱 들어가는 거예요. 칸마다 들어갈 수 있는 게 정해져 있어요.
2. **약속된 규칙**: 번호 칸에는 숫자만, 이름 칸에는 이름만 쓸 수 있어서, 실수로 이상한 걸 적으면 걸러져요.
3. **찾기 쉬워요**: 이렇게 정리되어 있어서 "3번 학생이 누구야?"라고 물으면 바로 찾을 수 있어요!
