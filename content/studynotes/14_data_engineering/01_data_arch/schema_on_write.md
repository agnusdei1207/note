+++
title = "스키마 온 라이트 (Schema-on-Write)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 스키마 온 라이트 (Schema-on-Write)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스키마 온 라이트(Schema-on-Write)는 데이터를 저장소에 기록하기 전에 미리 정의된 스키마에 맞게 변환하고 검증하는 전통적 데이터 처리 방식입니다.
> 2. **가치**: 데이터 무결성과 품질을 사전에 보장하며, 쿼리 성능을 최적화할 수 있어 관계형 데이터베이스와 데이터 웨어하우스의 기본 철학입니다.
> 3. **융합**: 스키마 온 리드와 대비되며, 현대 아키텍처에서는 Bronze Layer(온 리드)에서 수집 후 Silver/Gold Layer(온 라이트)로 변환하는 방식으로 융합됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**스키마 온 라이트(Schema-on-Write)**는 데이터를 저장소에 기록(Write)하기 전에 미리 정의된 스키마(테이블 구조, 데이터 타입, 제약조건)에 맞게 데이터를 변환하고 검증하는 방식입니다. RDBMS의 INSERT, UPDATE 작업이 대표적인 예입니다.

**핵심 특성**:
- **사전 스키마 정의**: 테이블 생성 시 CREATE TABLE로 구조 정의
- **데이터 검증**: 저장 전 타입, 제약조건 검증 수행
- **최적화된 저장**: 인덱스, 파티셔닝 등 쿼리 성능 고려한 저장
- **데이터 무결성**: ACID 트랜잭션으로 일관성 보장

#### 2. 비유를 통한 이해
- **Schema-on-Write**: 공항 보안 검색대입니다. 비행기에 탑승(저장)하기 전에 미리 여권을 확인하고, 짐을 검사하고, 규정에 맞는지 확인합니다. 시간이 걸리지만 안전합니다.
- **Schema-on-Read**: 열차 무인 승차입니다. 그냥 탑승하고, 나중에 검표할 때 티켓을 확인합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 처리 흐름

```text
<<< Schema-on-Write Processing Flow >>>

[Source] → [Extract] → [Transform & Validate] → [Apply Schema] → [Store] → [Query]
                            (타입 변환)            (제약 검증)      (최적화)
```

#### 2. SQL 예시

```sql
-- 스키마 정의
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    age INT CHECK (age >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 저장 시 스키마 검증
INSERT INTO users (id, name, email, age) VALUES
(1, '홍길동', 'hong@example.com', 30);  -- 성공

INSERT INTO users (id, name, email, age) VALUES
(2, NULL, 'kim@example.com', 25);  -- 실패: name NOT NULL 위반
```

#### 3. 장단점

**장점**:
- 데이터 무결성 보장
- 쿼리 성능 최적화
- 일관된 데이터 구조
- 명확한 데이터 거버넌스

**단점**:
- 스키마 변경 어려움
- ETL 지연 발생
- 유연성 부족
- 초기 설계 비용

---

### Ⅲ. 융합 비교 및 다각도 분석

| 비교 | Schema-on-Write | Schema-on-Read |
|:---|:---|:---|
| **사례** | RDBMS, DW | Data Lake, NoSQL |
| **무결성** | 강함 | 약함 |
| **유연성** | 낮음 | 높음 |
| **성능** | 읽기 빠름 | 쓰기 빠름 |

---

### Ⅳ. 실무 적용

**적합한 상황**:
- 금융 트랜잭션 (데이터 무결성 필수)
- 정형 BI 리포팅
- 규제 산업 (감사 추적)

**하이브리드 전략**: 데이터 레이크하우스의 Medallion Architecture
- Bronze: Schema-on-Read (수집)
- Silver/Gold: Schema-on-Write (분석)

---

### Ⅴ. 결론

스키마 온 라이트는 데이터 품질과 무결성이 중요한 시스템에서 여전히 필수적입니다. 현대 데이터 아키텍처에서는 스키마 온 리드와 결합하여 수집의 유연성과 분석의 정확성을 동시에 확보합니다.

---

### 관련 개념 맵 (Knowledge Graph)
- **[스키마 온 리드 (Schema-on-Read)](@/studynotes/14_data_engineering/01_data_arch/schema_on_read.md)**
- **[데이터 웨어하우스 (Data Warehouse)](@/studynotes/14_data_engineering/01_data_arch/data_warehouse.md)**
- **[정형 데이터 (Structured Data)](@/studynotes/14_data_engineering/01_data_arch/structured_data.md)**

---

### 어린이를 위한 3줄 비유 설명
1. **미리 검사하기**: 학교에 가기 전에 가방을 확인해요. 책, 필기구, 숙제가 다 있는지 미리 확인하죠.
2. **규칙 지키기**: 정해진 규칙대로 가방을 싸야 해요. 규칙에 맞지 않으면 다시 싸야 하죠.
3. **학교 가서 편해요**: 미리 다 확인했으니까 학교에서 필요한 걸 바로 꺼내 쓸 수 있어요!
