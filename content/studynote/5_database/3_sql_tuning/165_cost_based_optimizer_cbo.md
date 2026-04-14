+++
weight = 165
title = "비용 기반 옵티마이저 (CBO, Cost Based Optimizer)"
date = "2024-03-21"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)
1. **통계 기반의 정밀한 실행 계획**: 데이터 딕셔너리에 저장된 테이블 건수, 블록 수, 인덱스 높이, 데이터 분포 등 실시간 통계 정보를 바탕으로 최저 비용 경로를 선택한다.
2. **현대 DBMS의 글로벌 표준**: 데이터의 양과 분포 변화에 유연하게 대응하며, 복잡한 조인 방식(NL, Hash, Sort Merge)을 현실적으로 최적화할 수 있는 유일한 대안이다.
3. **통계 정보의 정확성이 성능을 좌우**: 통계 정보가 데이터의 실제 상태와 다를 경우 엉뚱한 실행 계획을 수립할 수 있으므로, 주기적인 통계 갱신 및 히스토그램 관리가 필수적이다.

---

### Ⅰ. 개요 (Context & Background)
비용 기반 옵티마이저(Cost Based Optimizer, CBO)는 쿼리를 수행하는 데 소요되는 예상 시간이나 자원 사용량을 수치화한 **'비용(Cost)'**을 계산하여 가장 저렴한 계획을 선택한다. CPU 사용량, 디스크 I/O 횟수, 메모리 점유 등을 종합적으로 고려하며, 현대의 대용량 데이터베이스 환경에서 데이터의 실질적인 상태를 반영할 수 있는 지능형 최적화 방식이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

CBO는 통계 정보를 입력으로 받아 수학적 공식을 통해 비용을 산출하는 구조이다.

```text
[ Optimizer Inputs ]
1. Object Statistics (Tables, Indexes)
2. System Statistics (CPU, I/O Speed)
3. Selectivity (선택도) & Cardinality (카디널리티)
       |
       v
[ Estimator (비용 산정기) ] --( Formula )--> [ Cost Calculation ]
       |                                     Cost = (I/O Cost) + (CPU Cost)
       v
[ Plan Generator (계획 생성기) ]
       |
       v
[ Cheapest Execution Plan Selection ]
```

*   **Selectivity (선택도)**: 전체 행 중 특정 조건을 만족하는 비율 (0~1 사이).
*   **Cardinality (카디널리티)**: 선택도 × 전체 행 수. 실행 계획의 조인 방식 결정에 가장 중요한 지표.
*   **Histogram (히스토그램)**: 데이터의 분포가 불균형할 때(Skewed Data), 특정 값의 빈도를 상세히 기록하여 오차를 줄이는 기법.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구성 요소 | 역할 및 산출 방식 | 성능에 미치는 영향 |
| :--- | :--- | :--- |
| **I/O Cost** | 블록을 읽는 물리적 디스크 접근 횟수 | 대량 데이터 스캔 시 결정적 요인 |
| **CPU Cost** | 필터링, 정렬, 해시 연산 등에 필요한 연산량 | In-Memory 처리 및 복잡한 연산 시 중요 |
| **Data Distribution** | 히스토그램을 통한 값의 편중도 확인 | 특정 조건에 대한 인덱스 사용 여부 결정 |
| **Wait Events** | 시스템 부하 상황(Lock, Buffer Busy 등) | 실시간 동적 성능 저하 요인 감지 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
1. **히스토그램의 신중한 관리**: 데이터 분포가 편중된 경우(예: 주문 상태 '완료' 99%, '대기' 1%)에는 반드시 히스토그램을 생성해야 옵티마이저가 '대기' 상태 조회 시 인덱스를 타게 된다.
2. **Bind Variable Peeking (바인드 변수 엿보기)**: CBO가 바인드 변수의 첫 번째 입력값을 보고 계획을 세우는 기능이다. 첫 값이 예외적인 값일 경우 이후 계획이 꼬일 수 있음에 주의해야 한다.
3. **기술사적 판단**: CBO는 데이터 과학의 관점에서의 최적화이다. 따라서 "비용이 낮다"는 것이 반드시 "실제 속도가 빠르다"와 일치하지 않을 수 있음을 인지하고, 실행 계획의 프로파일링을 통해 실측치와 비교하는 검증 과정이 수반되어야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
CBO는 최근 **Self-Driving Database**로의 진화와 함께 머신러닝 기반의 **ML Optimizer**로 발전하고 있다. 과거의 통계 수치에만 의존하는 것이 아니라, 과거 실행 이력을 학습하여 통계 정보를 스스로 보정하는 단계에 이르렀다. 결론적으로 CBO를 정복하는 것이 곧 DBMS 튜닝의 절반을 정복하는 것과 다름없다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: Optimizer
- **하위 개념**: Selectivity, Cardinality, Histogram
- **연관 개념**: Index Scan, Join Strategy (NL/Hash/Merge), Statistics Management

---

### 👶 어린이를 위한 3줄 비유 설명
1. CBO는 **"지금 어디로 가는 게 제일 싼지(비용)"**를 계산해서 길을 찾는 똑똑한 길잡이예요.
2. 장을 볼 때 **물건값(데이터 통계)**을 미리 다 알고 지갑 사정에 맞춰 가장 알뜰하게 쇼핑하는 것과 같아요.
3. 만약 물건값이 옛날 가격표(낡은 통계)라면, 예상보다 돈을 더 많이 쓸 수(성능 저하) 있으니 조심해야 해요!
