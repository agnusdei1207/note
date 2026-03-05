+++
title = "데이터 메시 (Data Mesh)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 데이터 메시 (Data Mesh)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 메시는 중앙 집중식 데이터 팀의 병목을 해결하기 위해, 각 도메인(부서)이 자신의 데이터를 '데이터 프로덕트'로 관리하고 제공하는 분산형 데이터 아키텍처입니다.
> 2. **가치**: 도메인 주도 설계(DDD), 셀프 서비스 데이터 플랫폼, 연합 거버넌스를 통해 조직의 데이터 민첩성을 극대화합니다.
> 3. **융합**: 데이터 레이크하우스와 결합하여, 중앙 저장소는 유지하되 데이터 오너십은 분산하는 하이브리드 모델로 진화합니다.

---

### Ⅰ. 개요

#### 1. 4대 원칙
1. **도메인 오너십**: 데이터를 생성하는 팀이 관리
2. **데이터 프로덕트**: 데이터를 제품으로 취급
3. **셀프 서비스 플랫폼**: 인프라 자동화
4. **연합 거버넌스**: 표준화된 규칙과 메타데이터

---

### Ⅱ. 아키텍처

```text
<<< Data Mesh Architecture >>>

[Centralized Platform Team]
+---------------------------+
| Self-Service Platform     |
| - Data Infrastructure     |
| - Metadata Catalog        |
| - Governance Policies     |
+---------------------------+
           |
    +------+------+
    |             |
    v             v
[Domain A]   [Domain B]
+-------+    +-------+
| Data  |    | Data  |
| Product|   | Product|
| - Sales|   | - HR   |
| - Orders|  | - Payroll|
+-------+    +-------+
    |             |
    +------+------+
           |
           v
    [Data Consumer]
```

---

### Ⅲ. 데이터 프로덕트

**특성**:
- 발견 가능 (Discoverable)
- 주소 지정 가능 (Addressable)
- 신뢰 가능 (Trustworthy)
- 자체 설명적 (Self-describing)

---

### Ⅳ. 결론

데이터 메시는 조직의 데이터 민첩성을 높이는 현대적 아키텍처 패러다임입니다.

---

### 관련 개념 맵
- **[데이터 패브릭](@/studynotes/14_data_engineering/01_data_arch/data_fabric.md)**
- **[데이터 카탈로그](@/studynotes/14_data_engineering/02_governance/data_catalog.md)**

---

### 어린이를 위한 3줄 비유
1. **각자 가게**: 큰 마트 대신 각 동네에 작은 가게가 있어요.
2. **자기 물건 자기가**: 빵집은 빵을, 야채 가게는 야채를 자기가 관리해요.
3. **서로 교환해요**: 빵이 필요하면 빵집에, 야채가 필요하면 야채 가게에 가요!
