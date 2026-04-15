+++
weight = 115
title = "밀도 기반 군집 (DBSCAN, Density-Based Spatial Clustering)"
date = "2024-03-24"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
- **밀도 기반의 군집화:** 데이터가 밀집된 영역을 군집으로 보고, 밀도가 낮은 영역은 노이즈로 처리하여 불규칙한 모양의 군집도 효과적으로 탐색.
- **이상치 탐지 내재화:** 군집에 포함되지 않는 포인트를 명확하게 'Noise(Outlier)'로 분류하여 데이터 정제에 매우 유용.
- **파라미터 중심:** 군집의 개수를 미리 정할 필요 없이, 반경(Eps)과 최소 포인트 수(MinPts)만으로 군집의 크기와 밀도를 정의.

### Ⅰ. 개요 (Context & Background)
K-Means와 같은 거리 기반 알고리즘은 군집의 개수($K$)를 미리 지정해야 하며, 원형이 아닌 복잡한 형태(초승달형, 도넛형 등)의 데이터를 군집화하는 데 한계가 있습니다. DBSCAN(Density-Based Spatial Clustering of Applications with Noise)은 밀도(Density)를 기준으로 데이터 간의 연결성을 판단하여, 기하학적 형태에 구애받지 않고 유의미한 군집을 찾아내는 강력한 비지도 학습 알고리즘입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
DBSCAN은 데이터 포인트를 세 가지 유형으로 분류하여 군집을 확장합니다.

```text
[ DBSCAN Principle: Core, Border, and Noise ]

       (Noise) .                (Core)
                .              *  *  *
       (Border)   o  --------- *  *  *  (Epsilon Radius)
                 o o           *  *  *
                o o o           (Core)
          (Cluster 1)

[ Key Components ]
1. Epsilon (eps): 주변 밀도를 확인할 원의 반경.
2. MinPts: Core Point가 되기 위한 반경 내 최소 포인트 개수.
3. Core Point: 반경 내에 MinPts 이상의 이웃이 있는 점. (군집의 중심)
4. Border Point: Core의 이웃이지만 본인은 MinPts를 만족 못 함. (군집의 경계)
5. Noise Point: Core도 아니고 Border도 아닌 나머지. (Outlier)
```

**핵심 원리:**
1. **밀도 연결성(Density Connectivity):** Core Point끼리 서로의 반경 안에 있으면 하나의 군집으로 연결됩니다.
2. **반복적 확장:** 임의의 점을 선택하여 Core 여부를 판단하고, 이웃들을 파도처럼 타고 넘어가며 군집을 완성합니다.
3. **노이즈 분리:** 군집에 연결되지 못한 점들은 과감하게 노이즈로 분류하여 모델의 강건성(Robustness)을 높입니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | K-Means Clustering | DBSCAN Clustering |
| :--- | :--- | :--- |
| **군집 수 결정** | 사전 정의 ($K$) | 데이터 밀도에 의해 자동 결정 |
| **군집 형태** | 볼록한 원형 (Convex) | 임의의 복잡한 모양 (Non-convex) |
| **이상치(Noise)** | 모든 점을 군집에 강제 할당 | 명확하게 노이즈로 배제 가능 |
| **주요 파라미터** | $K$ (Centroids) | Epsilon, MinPts |
| **장점** | 대규모 데이터에 매우 빠름 | 이상치에 강하고 구조적 제약이 없음 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **실무 적용:** 지리 정보 시스템(GIS)에서 상권 분석이나 범죄 밀집 지역을 찾을 때, 혹은 복잡한 제조 공정 로그에서 정상 범위를 벗어난 이상 패턴을 탐지할 때 최우선으로 고려되는 알고리즘입니다.
- **기술사적 판단:** DBSCAN은 데이터의 밀도가 불균일할 경우(어느 군집은 촘촘하고 어느 군집은 느슨함) 성능이 급격히 저하됩니다. 기술사는 이러한 경우를 위해 Epsilon 값을 동적으로 조절하는 OPTICS 알고리즘이나 계층적 구조를 활용하는 HDBSCAN으로의 전환을 제안해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
DBSCAN은 데이터 탐색(EDA) 단계에서 군집의 실제 구조를 파악하는 데 표준적인 도구입니다. 미래의 지능형 엔지니어링 환경에서는 자율주행 차의 센서 데이터 융합이나 보안 관제의 트래픽 이상 탐지 분야에서 실시간 밀도 분석을 통해 안전성을 확보하는 핵심 기술로 지속 활용될 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Unsupervised Learning, Density Estimation
- **하위 개념:** Core Point, Epsilon, MinPts, Noise Point
- **연관 기술:** OPTICS, HDBSCAN, K-Means, Local Outlier Factor (LOF)

### 👶 어린이를 위한 3줄 비유 설명
1. "우리끼리 모여라!" 놀이를 하는데, 주변에 친구가 3명 이상 있으면 리더(Core)가 돼요.
2. 리더 옆에 붙어 있는 친구들도 한 팀이 되지만, 혼자 멀리 떨어져서 아무도 없는 친구는 술래(Noise)가 되는 거예요.
3. 이렇게 옹기종기 모여 있는 '섬'들을 하나하나 찾아내는 것이 DBSCAN이랍니다.
