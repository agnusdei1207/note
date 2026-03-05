+++
title = "데이터 카탈로그 (Data Catalog)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 데이터 카탈로그 (Data Catalog)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 카탈로그는 조직의 모든 데이터 자산에 대한 메타데이터(스키마, 위치, 소유자, 품질)를 수집하고, 검색과 발견을 가능하게 하는 메타데이터 관리 시스템입니다.
> 2. **가치**: "데이터의 구글"처럼 분석가가 필요한 데이터를 쉽게 찾고, 이해하고, 접근 권한을 관리할 수 있게 합니다.
> 3. **융합**: AWS Glue, Apache Atlas, Amundsen, DataHub 등이 대표적이며, 데이터 거버넌스와 데이터 리니지의 핵심 인프라입니다.

---

### Ⅰ. 개요

#### 1. 핵심 기능
- **데이터 발견**: 검색으로 데이터 찾기
- **메타데이터 관리**: 스키마, 설명, 태그
- **데이터 리니지**: 데이터 흐름 추적
- **접근 제어**: 권한 관리

---

### Ⅱ. 아키텍처

```text
+------------------+
|   Data Sources   |
| - RDBMS          |
| - Data Lake      |
| - APIs           |
+--------+---------+
         |
         v
+--------+---------+
|   Data Catalog   |
| - Metadata Store |
| - Search Engine  |
| - Lineage Graph  |
+--------+---------+
         |
         v
+------------------+
|   Data Users     |
| - Analysts       |
| - Scientists     |
+------------------+
```

---

### Ⅲ. 주요 제품

| 제품 | 특징 |
|:---|:---|
| **AWS Glue** | AWS 네이티브 |
| **Apache Atlas** | 하둡 생태계 |
| **Amundsen** | Lyft 개발 |
| **DataHub** | LinkedIn 개발 |

---

### Ⅳ. 결론

데이터 카탈로그는 데이터 거버넌스와 셀프 서비스 분석의 핵심 인프라입니다.

---

### 관련 개념 맵
- **[데이터 리니지](@/studynotes/14_data_engineering/02_governance/data_lineage.md)**
- **[데이터 거버넌스](@/studynotes/14_data_engineering/02_governance/data_governance.md)**

---

### 어린이를 위한 3줄 비유
1. **도서관 카드**: 도서관에 어떤 책이 있는지 보여주는 카드예요.
2. **책 찾기**: 책 제목, 저자, 주제로 찾을 수 있어요.
3. **대출 기록**: 누가 언제 빌렸는지도 알 수 있어요!
