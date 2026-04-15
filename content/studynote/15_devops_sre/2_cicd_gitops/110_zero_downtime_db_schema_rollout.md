+++
weight = 110
title = "무중단 DB 스키마 롤아웃 (Zero-Downtime DB Schema Rollout) - Expand and Contract"
date = "2026-03-04"
[extra]
categories = ["studynote-devops-sre", "cicd-gitops"]
+++

## 핵심 인사이트 (3줄 요약)
- 'Expand and Contract(확장 및 수축)' 패턴은 앱 배포와 DB 스키마 변경을 분리하여, 신/구버전 앱이 동시에 운영 DB를 사용해도 서비스가 중단되지 않게 하는 기법임.
- 한 번에 컬럼을 바꾸는 대신 '추가(Expand) $\rightarrow$ 병행 사용 $\rightarrow$ 삭제(Contract)'의 3단계 프로세스를 거쳐 하위 호환성을 완벽히 보장함.
- CI/CD 파이프라인에서 데이터베이스 마이그레이션 도구(Flyway, Liquibase)를 사용하여 자동화하며, 롤백 시 데이터 유실 리스크를 최소화함.

### Ⅰ. 개요 (Context & Background)
애플리케이션은 블루/그린 배포로 무중단이 가능하지만, 데이터베이스 스키마(DDL)는 쉽지 않다. 컬럼 이름을 갑자기 바꾸면 구버전 앱은 에러를 뿜으며 죽는다. 그렇다고 DB 점검 창을 띄우는 것은 현대적 DevOps의 지향점이 아니다. 따라서 DB 변경 사항을 작게 쪼개어, 구버전 앱이 떠 있는 동안에도 신버전 스키마가 평화롭게 공존할 수 있도록 만드는 '과도기적 아키텍처' 설계가 필수적이다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

Expand and Contract 패턴은 호환성을 유지하며 DB를 점진적으로 변형시킨다.

```text
[ Expand and Contract Pattern Workflow ]

Phase 1: Expand (확장)
  - DB: New Column Added (Old Column Remains)
  - App: Version 1 (Reads/Writes Old Column)

Phase 2: Migrate & Parallel (병행)
  - DB: Data Synced from Old to New
  - App: Version 2 (Writes to BOTH, Reads from Old or New)

Phase 3: Contract (수축)
  - DB: Old Column Dropped (Cleanup)
  - App: Version 2 (Reads/Writes New Column ONLY)

[ Bilingual Comparison ]
- Backward Compatibility (하위 호환성): 신규 DB 스펙에서 구버전 앱이 작동함.
- Forward Compatibility (상위 호환성): 구버전 DB 스펙에서 신버전 앱이 작동함.
- Parallel Write (이중 쓰기): 과도기 동안 신/구 컬럼에 동시에 데이터를 기록.
- Decoupling (디커플링): 앱 배포와 DB 배포의 선후 관계 의존성 제거.
```

이 방식은 특히 컬럼 삭제나 이름 변경 시 강력하다. '삭제'를 가장 마지막 단계로 미룸으로써, 배포 중 문제가 생겨 앱을 롤백하더라도 DB 데이터가 그대로 남아 있어 장애를 방지한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 전통적 빅뱅 배포 (Big Bang) | 무중단 점진 배포 (Expand & Contract) |
| :--- | :--- | :--- |
| **배포 방식** | 점검 페이지 게시 후 한꺼번에 변경 | **배포 중에도 서비스 계속 유지** |
| **호환성** | 고려하지 않음 (전환 시점 기준) | **구버전 앱과의 호환성 필수 유지** |
| **복잡도** | 낮음 (한 번에 끝) | **높음 (여러 번의 배포 단계 필요)** |
| **리스크** | 롤백 시 DB 복구가 매우 힘듦 | **롤백이 매우 쉽고 데이터 유실 없음** |
| **추천 환경** | 소규모, 데이터 중요도 낮은 경우 | **금융, 이커머스 등 고가용성 필수 시스템** |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **(마이그레이션 도구 통합)** Flyway나 Liquibase를 사용하여 각 단계의 SQL 스크립트를 버저닝(V1__expand, V2__migrate, V3__contract)하고, CI/CD 파이프라인에서 앱 배포 전후에 자동 실행되도록 구성한다.
- **(트리거 및 애플리케이션 로직)** 데이터 마이그레이션 시 양이 너무 많으면 DB 부하가 걸린다. 애플리케이션 레벨에서 '읽을 때 없으면 옮기기(Lazy Migration)'를 하거나, DB 트리거를 활용해 신/구 컬럼의 데이터를 실시간 동기화하는 전략을 선택한다.
- **(테스트 자동화)** 파이프라인 내에서 '구버전 앱 + 신버전 DB' 조합으로 통합 테스트를 반드시 수행하여, 스키마 확장 단계에서 기존 기능이 깨지지 않는지 검증해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
무중단 DB 롤아웃은 '진정한 지속적 배포(CD)'를 완성하는 마지막 퍼즐이다. 앱은 언제든 배포할 수 있는데 DB 때문에 점검을 잡는다면 그것은 반쪽짜리 데브옵스다. 기술사는 DB 변경의 가역성(Reversibility)을 확보하기 위해 단계를 나누고, 데이터 무결성과 가용성 사이의 균형을 잡는 아키텍처를 제시해야 한다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **Blue/Green Deployment**: 앱 무중단 배포의 짝꿍
- **Database Refactoring**: DB 구조의 점진적 개선
- **Referential Integrity**: 변경 중 깨지기 쉬운 제약 조건
- **Canary Release**: DB 변경 영향도를 조금씩 확인하는 배포

### 👶 어린이를 위한 3줄 비유 설명
- 레고 성의 빨간색 기둥을 파란색으로 바꾸고 싶은데, 성을 다 무너뜨리고 싶지는 않아.
- 먼저 파란색 기둥을 옆에 하나 더 세우고(확장), 사람들이 파란색 기둥을 쓰게 한 다음에,
- 마지막에 쓸모없어진 빨간색 기둥을 조용히 빼내는(수축) 아주 조심스러운 공사 방법이란다!
