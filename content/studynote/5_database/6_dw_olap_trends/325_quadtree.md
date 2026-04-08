+++
title = "325. ETL (Extract, Transform, Load) 프로세스 - 소스 추출 -> 정제/변환 -> 타겟 적재"
weight = 4325
+++

> **💡 핵심 인사이트**
> Quad-tree(쿼드트리)는 **"2차원 공간(평면)을递归적으로 4개의 균등 사분면(Quadrant)으로 분할하여, 공간 내 점(Point)이나矩形(Rectangle) 데이터를高速 검색할 수 있게 하는 트리 자료구조"**입니다.
> B-Tree가 1차원(키)의 빠른 검색에 특화되어 있다면, Quad-tree는 **2차원 공간 데이터(좌표, MBR 등)의 근접 이웃 탐색, 영역 查询, 충돌 检测 등 공간 연산에 최적화**되어 있습니다. 게임 물리 엔진, 지리정보시스템(GIS), 이미지 처리, 공간 데이터베이스에서 널리 활용됩니다.

---

## Ⅰ. Quad-tree의 핵심 원리: 4분할의 반복

```
[Quad-tree 공간 분할 과정]

  Level 0 (Root):
  ┌─────────────────────────────┐
  │                             │
  │                             │
  │                             │
  │                             │
  └─────────────────────────────┘

  Level 1 (4분할):
  ┌───────────┬───────────┐
  │     │     │           │
  │  NW │ NE  │           │
  │     │     │           │
  ├─────┼─────┤
  │     │     │           │
  │  SW │ SE  │           │
  │     │     │           │
  └───────────┴───────────┘

  Level 2 (SW를 다시 4분할):
  ┌───────────┬───────────┐
  │     │     │           │
  │  NW │ NE  │           │
  │     │     │           │
  ├─────┼─────┼───────────┤
  │┌───┬───┐│ │           │
  ││SW1│SW2││ SE          │
  │├───┼───┤│ │           │
  ││SW3│SW4││ │           │
  │└───┴───┘│ │           │
  └───────────┴───────────┘
```

**분할 규칙 (Quad-tree invariant):**
- 각 노드는 **4개 이하**의 점을 저장
- 노드 용량(capacity)을 초과하면 → 해당 공간을 **4개의 하위 사분면으로 분할**
- 최대 깊이(depth) 도달 시 분할 중지

---

## Ⅱ. Quad-tree의 삽입과 검색

### 점 삽입 (Point Insertion)

```python
class QuadTree:
    def __init__(self, boundary, capacity=4, max_depth=10):
        self.boundary = boundary  # MBR (x_min, y_min, x_max, y_max)
        self.capacity = capacity   # 노드당 최대 점 수
        self.points = []           # 현재 노드의 점들
        self.divided = False
        self.nw = self.ne = self.sw = self.se = None

    def subdivide(self):
        x, y = self.boundary.center()
        w, h = self.boundary.w / 2, self.boundary.h / 2
        # 4개의 하위 사분면 생성
        self.nw = QuadTree(MBR(x-w, y-h, w, h))
        self.ne = QuadTree(MBR(x, y-h, w, h))
        self.sw = QuadTree(MBR(x-w, y, w, h))
        self.se = QuadTree(MBR(x, y, w, h))
        self.divided = True

    def insert(self, point, depth=0):
        # 점이 이 노드의 영역에 포함되지 않으면 실패
        if not self.boundary.contains(point):
            return False

        # 용량 미달이면 여기 저장
        if len(self.points) < self.capacity or depth == self.max_depth:
            self.points.append(point)
            return True

        # 용량 초과 + 아직 분할 안 됐으면 분할
        if not self.divided:
            self.subdivide()

        # 4개 사분면 중 하나에 삽입
        if self.nw.insert(point, depth+1): return True
        if self.ne.insert(point, depth+1): return True
        if self.sw.insert(point, depth+1): return True
        if self.se.insert(point, depth+1): return True
        return False
```

### 영역 검색 (Range Query)

```python
    def query_range(self, range_mbr):
        """range_mbr와 교차하는 모든 점을 반환"""
        found = []

        # 이 노드와 查询 영역이 겹치지 않으면 종료
        if not self.boundary.intersects(range_mbr):
            return found

        # 이 노드에 저장된 점 중 查询 영역에 포함되는 점 추가
        for p in self.points:
            if range_mbr.contains_point(p):
                found.append(p)

        # 하위 사분면이 있으면 재귀적으로 탐색
        if self.divided:
            found.extend(self.nw.query_range(range_mbr))
            found.extend(self.ne.query_range(range_mbr))
            found.extend(self.sw.query_range(range_mbr))
            found.extend(self.se.query_range(range_mbr))

        return found
```

**영역 查询 예시:**

```
[쿼리: 특정 사각 영역과 겹치는 점 찾기]

  쿼리 영역 (빨간 점선):
  ┌───────────┬───────────┐
  │     │     │     ╭───╮ │
  │  NW │ NE  │     │   │ │
  │     │     │  ╭──┼───┼─┤
  ├─────┼─────┼──│──│   │ │
  │     │★    │  │ ★│ ★ │ │  ★ = 쿼리 결과
  │  SW │ SE  │  ╰──│───╯ │
  │     │     │     │ ★   │
  └───────────┴───────────┘
  → 쿼리 영역과 겹치는 leaf 노드만 탐색
  → 전체 점 비교보다大幅高速
```

---

## III. Quad-tree vs R-Tree: 언제 무엇을 선택하는가

```
[Quad-tree vs R-Tree 비교]

  Quad-tree:
  - 공간分割 기반: 점 데이터에 적합
  - 트리 깊이가 데이터 분포에 따라 변함
  - 균일 분포에서 효율적
  - insertions/deletions에 강한 (지역적 변경)

  R-Tree:
  - 최소 경계矩形(MBR) 그룹핑 기반
  - 면(Region) 데이터에 적합
  - 트리 깊이 항상 균등 (항상平衡)
  - 범위 쿼리에 최적화
```

| 기준 | Quad-tree | R-Tree |
|------|----------|--------|
| **적합 데이터** | 점 (Point) | 면/사각형 (Rectangle) |
| **균형 유지** | 삽입/삭제에 따라 변화 | 자동 균형 유지 |
| **최근접 이웃** | 우수 | 보통 |
| **범위 쿼리** | 보통 | 우수 |
| **구현 난이도** | 비교적 단순 | 복잡 |
| **공간 DB 활용** | PostGIS (ST_QuadTree) | PostGIS (기본값) |

---

## IV. 공간 데이터베이스에서의 Quad-tree 활용

**PostgreSQL / PostGIS에서의 Quad-tree 인덱스:**

```sql
-- PostGIS에서 Quad-tree 기반 공간 인덱스 사용
-- PostGIS 3.0+ 에서 Quad-tree 인덱스 지원

-- 공간 인덱스 생성 (기본적으로 R-Tree지만 Quad-tree로 변경 가능)
CREATE INDEX idx_locations ON locations USING GIST (geom);

-- Quad-tree 인덱스 명시적 생성 (PostGIS 3.3+)
CREATE INDEX idx_locations_quad ON locations USING QUADTREE (geom);

-- 근접 이웃 검색 (K-Nearest Neighbor)
SELECT id, name, ST_Distance(geom, ST_GeomFromText('POINT(-122.4 37.7)', 4326)) as dist
FROM locations
ORDER BY geom <-> ST_GeomFromText('POINT(-122.4 37.7)', 4326)
LIMIT 5;

-- 영역 查询
SELECT * FROM locations
WHERE ST_Intersects(
    geom,
    ST_MakeEnvelope(-122.5, 37.5, -122.0, 38.0, 4326)  -- 경계 상자
);
```

**게임 개발에서의 Quad-tree 활용:**

```
[충돌 检测에서의 Quad-tree]

  상황: 1000개의 게임 객체(탄알, 캐릭터, 장애물)의 충돌을 检测

  방법 1: O(n²) 전체 쌍 비교
  → 1000 × 999 / 2 = 499,500번 비교 (느림)

  방법 2: Quad-tree 공간 분할 후 충돌 检测
  → 같은 사분면에 속한 객체끼리만 비교
  → 대부분 객체가 다른 사분면에 분산 → 비교 횟수大幅 감소
  → 결과: 약 50,000~100,000번 비교 (10~20배高速)
```

---

## Ⅴ. Quad-tree의 변형과 📢 비유

**Quad-tree 변형:**

| 변형 | 설명 | 활용 |
|------|------|------|
| **Point Quad-tree** | 점 기반 (우리가 설명한 것) | 좌표 검색 |
| **MX-CIF Quad-tree** | 사각형 객체 분할 | GIS |
| **PR Quad-tree** | 점 + 사각형 혼합 | 다양 |
| **Octree (3D)** | 3차원 확장 (8분할) | 3D 그래픽, 점군 |

> 📢 **섹션 요약 비유:** Quad-tree는 **"도박을 4등분해서 빠르게 찾는 방법"**과 같습니다. 도박 전체를 海에 담가두면 (전체 스캔) 찾을 물고가 있는지를 확인하기 위해 바다 속 모든 곳을 훑어야 합니다. 하지만 Quad-tree는 **"바다를 먼저東西南北 4등분하고, 그 中 물고기가 있을 것 같은 쪽을 또 4등분하고, 또 4등분하는"** 것입니다. 물고기가 있으면 더 이상 다른 방향을 뒤지지 않아도 됩니다. 2차원 공간에서 **"찾는 범위를半分씩 줄여나가는"** 것이 Quad-tree의 핵심입니다. 특히 **"이 지역 근처의 모든 맛집을 찾아라"**, **"반경 500m 내 모든 건물을 찾아라"** 같은 **"근처 것 찾기"** 연산에 특화된 자료구조입니다.
