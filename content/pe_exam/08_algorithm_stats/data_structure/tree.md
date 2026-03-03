+++
title = "트리 자료구조 (Tree)"
date = 2025-03-02

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 트리 자료구조 (Tree)

## 핵심 인사이트 (3줄 요약)
> **계층적 구조를 표현하는 비선형 자료구조**. 루트에서 리프로 뻗어나가는 구조. BST, AVL, 레드블랙, B-트리 등 다양한 변형이 검색/정렬에 핵심.

---

## 📝 기술사 모의답안 (2.5페이지 분량)

### 📌 예상 문제
> **"트리 자료구조의 원리와 종류를 설명하고, 이진 탐색 트리와 균형 트리의 차이를 기술하시오."**

---

### Ⅰ. 개요

#### 1. 개념
트리(Tree)는 **노드(Node)와 간선(Edge)으로 구성된 계층적 비선형 자료구조**로, 하나의 루트 노드에서 시작하여 자식 노드로 확장되는 구조를 가진다. 사이클이 없는 연결 그래프의 일종이다.

> 💡 **비유**: "가계도(족보)" - 조상에서 자손으로 뻗어나가는 구조

**등장 배경**:
1. **기존 문제점**: 선형 구조(배열, 연결리스트)는 계층 관계 표현 어려움
2. **기술적 필요성**: 효율적인 검색(O(log n))을 위한 자료구조 필요
3. **시장 요구**: 파일 시스템, DB 인덱스, HTML DOM 등 계층 표현 수요

**핵심 목적**: 계층적 데이터 표현 + 효율적 검색/정렬

---

### Ⅱ. 구성 요소 및 핵심 원리

#### 2. 트리 핵심 구성 요소

| 구성 요소 | 정의 | 특징 |
|----------|------|------|
| 노드 (Node) | 데이터 저장 단위 | 데이터 + 자식 포인터 |
| 루트 (Root) | 최상위 노드 | 부모가 없는 유일한 노드 |
| 리프 (Leaf) | 최하위 노드 | 자식이 없는 노드 |
| 간선 (Edge) | 노드 연결선 | 부모-자식 관계 |
| 깊이 (Depth) | 루트~노드 거리 | 루트 깊이 = 0 |
| 높이 (Height) | 노드~리프 최장 거리 | 리프 높이 = 0 |

#### 3. 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────┐
│               트리 구조와 용어                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    ┌───┐                                    │
│                    │ A │  ← 루트 (Root), 깊이=0, 높이=3    │
│                    └─┬─┘                                    │
│               ┌──────┼──────┐                               │
│             ┌─┴─┐  ┌─┴─┐  ┌─┴─┐                             │
│             │ B │  │ C │  │ D │  ← 내부 노드, 깊이=1       │
│             └─┬─┘  └─┬─┘  └─┬─┘    (Internal Node)        │
│           ┌───┴───┐   │  ┌──┴──┐                           │
│         ┌─┴─┐   ┌─┴─┐ │ ┌┴─┐ ┌─┴─┐                         │
│         │ E │   │ F │ │ │G │ │ H │  ← 리프 (Leaf), 깊이=2  │
│         └───┘   └───┘ │ └──┘ └───┘                         │
│                         │                                    │
│                       ┌─┴─┐                                  │
│                       │ I │  ← 리프, 깊이=2                 │
│                       └───┘                                  │
│                                                             │
│  📊 트리 성질:                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  • 노드 수 = n, 간선 수 = n - 1                      │   │
│  │  • 깊이 d인 포화 이진 트리 노드 수 = 2^(d+1) - 1     │   │
│  │  • 노드 n개인 완전 이진 트리 높이 = ⌊log₂n⌋         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 4. 트리 종류

| 종류 | 특징 | 시간복잡도 | 용도 |
|-----|------|-----------|------|
| 이진 트리 | 자식 최대 2개 | - | 기본 구조 |
| 포화 이진 트리 | 모든 리프 같은 레벨 | - | 힙 |
| 완전 이진 트리 | 왼쪽부터 채움 | - | 힙, 우선순위큐 |
| BST | 좌 < 루트 < 우 | O(log n) 평균 | 검색 |
| AVL | 균형 인수 ±1 | O(log n) 보장 | 검색 최적화 |
| 레드블랙 | 색상 기반 균형 | O(log n) 보장 | 연관배열 |
| B-트리 | 다진 균형 트리 | O(log n) | DB 인덱스 |
| 트라이 | 문자열 특화 | O(m) | 자동완성 |

#### 5. 이진 트리 순회

| 순회 방식 | 순서 | 용도 | 예시 (A-B-C-D-E-F-G) |
|---------|------|------|---------------------|
| 전위 (Preorder) | 루트→좌→우 | 복사, 출력 | A-B-D-E-C-F-G |
| 중위 (Inorder) | 좌→루트→우 | 정렬 (BST) | D-B-E-A-F-C-G |
| 후위 (Postorder) | 좌→우→루트 | 삭제, 계산 | D-E-B-F-G-C-A |
| 레벨 (Level) | 레벨 순서 | BFS | A-B-C-D-E-F-G |

#### 6. Python 코드 예시

```python
from typing import Optional, List, Callable
from collections import deque

# ==================== 기본 이진 트리 ====================

class TreeNode:
    """이진 트리 노드"""
    def __init__(self, val: int = 0):
        self.val = val
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None


class BinaryTree:
    """기본 이진 트리"""

    def __init__(self):
        self.root: Optional[TreeNode] = None

    # 순회 메서드
    def preorder(self, node: Optional[TreeNode] = None,
                 result: List[int] = None) -> List[int]:
        """전위 순회: 루트 → 좌 → 우"""
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node is None:
            return result

        result.append(node.val)
        if node.left:
            self.preorder(node.left, result)
        if node.right:
            self.preorder(node.right, result)

        return result

    def inorder(self, node: Optional[TreeNode] = None,
                result: List[int] = None) -> List[int]:
        """중위 순회: 좌 → 루트 → 우 (BST에서 정렬됨)"""
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node is None:
            return result

        if node.left:
            self.inorder(node.left, result)
        result.append(node.val)
        if node.right:
            self.inorder(node.right, result)

        return result

    def postorder(self, node: Optional[TreeNode] = None,
                  result: List[int] = None) -> List[int]:
        """후위 순회: 좌 → 우 → 루트"""
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node is None:
            return result

        if node.left:
            self.postorder(node.left, result)
        if node.right:
            self.postorder(node.right, result)
        result.append(node.val)

        return result

    def level_order(self) -> List[int]:
        """레벨 순회: BFS"""
        if not self.root:
            return []

        result = []
        queue = deque([self.root])

        while queue:
            node = queue.popleft()
            result.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result

    def height(self, node: Optional[TreeNode] = None) -> int:
        """트리 높이 계산"""
        if node is None:
            node = self.root
        if node is None:
            return -1

        return 1 + max(
            self.height(node.left) if node.left else -1,
            self.height(node.right) if node.right else -1
        )


# ==================== 이진 탐색 트리 (BST) ====================

class BST(BinaryTree):
    """이진 탐색 트리"""

    def insert(self, val: int) -> None:
        """값 삽입"""
        if not self.root:
            self.root = TreeNode(val)
            return

        def _insert(node: TreeNode, val: int) -> None:
            if val < node.val:
                if node.left is None:
                    node.left = TreeNode(val)
                else:
                    _insert(node.left, val)
            else:
                if node.right is None:
                    node.right = TreeNode(val)
                else:
                    _insert(node.right, val)

        _insert(self.root, val)

    def search(self, val: int) -> Optional[TreeNode]:
        """값 검색"""
        def _search(node: Optional[TreeNode], val: int) -> Optional[TreeNode]:
            if node is None or node.val == val:
                return node

            if val < node.val:
                return _search(node.left, val)
            else:
                return _search(node.right, val)

        return _search(self.root, val)

    def delete(self, val: int) -> bool:
        """값 삭제"""
        def _find_min(node: TreeNode) -> TreeNode:
            while node.left:
                node = node.left
            return node

        def _delete(node: Optional[TreeNode], val: int) -> Optional[TreeNode]:
            if node is None:
                return None

            if val < node.val:
                node.left = _delete(node.left, val)
            elif val > node.val:
                node.right = _delete(node.right, val)
            else:
                # 삭제할 노드 발견
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                else:
                    # 두 자식 모두 있음: 후계자 찾기
                    successor = _find_min(node.right)
                    node.val = successor.val
                    node.right = _delete(node.right, successor.val)

            return node

        if self.search(val) is None:
            return False

        self.root = _delete(self.root, val)
        return True


# ==================== AVL 트리 (균형 BST) ====================

class AVLNode(TreeNode):
    """AVL 트리 노드"""
    def __init__(self, val: int = 0):
        super().__init__(val)
        self.height = 1  # 노드 높이


class AVLTree:
    """AVL 트리 - 자가 균형 이진 탐색 트리"""

    def __init__(self):
        self.root: Optional[AVLNode] = None

    def _get_height(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def _get_balance(self, node: Optional[AVLNode]) -> int:
        """균형 인수: 왼쪽 높이 - 오른쪽 높이"""
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def _update_height(self, node: AVLNode) -> None:
        node.height = 1 + max(
            self._get_height(node.left),
            self._get_height(node.right)
        )

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """우회전 (LL 케이스)"""
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self._update_height(y)
        self._update_height(x)

        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        """좌회전 (RR 케이스)"""
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self._update_height(x)
        self._update_height(y)

        return y

    def insert(self, val: int) -> None:
        """값 삽입 + 균형 유지"""
        def _insert(node: Optional[AVLNode], val: int) -> AVLNode:
            if node is None:
                return AVLNode(val)

            if val < node.val:
                node.left = _insert(node.left, val)
            else:
                node.right = _insert(node.right, val)

            self._update_height(node)

            # 균형 확인
            balance = self._get_balance(node)

            # LL 케이스
            if balance > 1 and val < node.left.val:
                return self._rotate_right(node)

            # RR 케이스
            if balance < -1 and val > node.right.val:
                return self._rotate_left(node)

            # LR 케이스
            if balance > 1 and val > node.left.val:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

            # RL 케이스
            if balance < -1 and val < node.right.val:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

            return node

        self.root = _insert(self.root, val)

    def inorder(self) -> List[int]:
        """중위 순회 (정렬됨)"""
        result = []

        def _inorder(node: Optional[AVLNode]):
            if node:
                _inorder(node.left)
                result.append(node.val)
                _inorder(node.right)

        _inorder(self.root)
        return result


# ==================== 세그먼트 트리 ====================

class SegmentTree:
    """
    세그먼트 트리 (구간 쿼리)

    구간 합, 구간 최솟값/최댓값 등 O(log n)에 처리
    """

    def __init__(self, data: List[int]):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self._build(data, 1, 0, self.n - 1)

    def _build(self, data: List[int], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            self._build(data, node * 2, start, mid)
            self._build(data, node * 2 + 1, mid + 1, end)
            self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def query(self, left: int, right: int) -> int:
        """구간 [left, right] 합 조회"""
        def _query(node: int, start: int, end: int) -> int:
            if right < start or left > end:
                return 0
            if left <= start and end <= right:
                return self.tree[node]

            mid = (start + end) // 2
            return (_query(node * 2, start, mid) +
                   _query(node * 2 + 1, mid + 1, end))

        return _query(1, 0, self.n - 1)

    def update(self, idx: int, val: int) -> None:
        """인덱스 idx 값을 val로 변경"""
        def _update(node: int, start: int, end: int) -> None:
            if start == end:
                self.tree[node] = val
            else:
                mid = (start + end) // 2
                if idx <= mid:
                    _update(node * 2, start, mid)
                else:
                    _update(node * 2 + 1, mid + 1, end)
                self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

        _update(1, 0, self.n - 1)


# ==================== LCA (최소 공통 조상) ====================

def find_lca(root: TreeNode, p: int, q: int) -> Optional[int]:
    """
    최소 공통 조상 (Lowest Common Ancestor)
    BST에서 활용
    """
    if not root:
        return None

    if p < root.val and q < root.val:
        return find_lca(root.left, p, q)
    elif p > root.val and q > root.val:
        return find_lca(root.right, p, q)
    else:
        return root.val


# ==================== 테스트 및 검증 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("트리 자료구조 테스트")
    print("=" * 50)

    # BST 테스트
    print("\n[BST 테스트]")
    bst = BST()
    values = [50, 30, 70, 20, 40, 60, 80]

    for v in values:
        bst.insert(v)

    print(f"삽입: {values}")
    print(f"중위 순회 (정렬): {bst.inorder()}")
    print(f"전위 순회: {bst.preorder()}")
    print(f"후위 순회: {bst.postorder()}")
    print(f"레벨 순회: {bst.level_order()}")
    print(f"높이: {bst.height()}")

    print(f"\n검색 40: {bst.search(40).val if bst.search(40) else None}")
    print(f"검색 100: {bst.search(100)}")

    bst.delete(30)
    print(f"30 삭제 후 중위 순회: {bst.inorder()}")

    # AVL 테스트
    print("\n[AVL 트리 테스트]")
    avl = AVLTree()
    # 편향 입력 (일반 BST면 O(n)이 됨)
    for v in [1, 2, 3, 4, 5]:
        avl.insert(v)

    print(f"삽입: [1, 2, 3, 4, 5] (편향 입력)")
    print(f"중위 순회: {avl.inorder()}")
    print(f"높이: {avl._get_height(avl.root)}")  # AVL은 log n 유지

    # 세그먼트 트리
    print("\n[세그먼트 트리]")
    data = [1, 3, 5, 7, 9, 11]
    seg = SegmentTree(data)
    print(f"데이터: {data}")
    print(f"구간 [1, 4] 합: {seg.query(1, 4)}")  # 3+5+7+9 = 24
    seg.update(2, 10)  # 인덱스 2를 5→10으로
    print(f"인덱스 2를 10으로 변경 후 구간 [1, 4] 합: {seg.query(1, 4)}")
```

---

### Ⅲ. 기술 비교 분석

#### 7. 트리 종류별 성능 비교

| 연산 | 일반 BST | AVL | 레드블랙 | B-트리 (m=100) |
|-----|---------|-----|----------|----------------|
| 검색 | O(log n)~O(n) | O(log n) | O(log n) | O(log_m n) |
| 삽입 | O(log n)~O(n) | O(log n) | O(log n) | O(log_m n) |
| 삭제 | O(log n)~O(n) | O(log n) | O(log n) | O(log_m n) |
| 회전 | - | ≤2 | ≤2 | - |
| 균형 보장 | X | O | O | O |

#### 8. 장단점 분석

| 장점 | 단점 |
|-----|------|
| 계층 구조 표현 | 구현 복잡 |
| O(log n) 검색 (균형 시) | 포인터 오버헤드 |
| 정렬 상태 유지 | 균형 유지 비용 |
| 범위 검색 가능 | 메모리 단편화 |
| 동적 크기 | 캐시 성능 낮음 (vs 배열) |

#### 9. 대안 기술 비교

| 비교 항목 | BST | 해시 테이블 | 배열 (정렬) | 연결리스트 |
|---------|-----|----------|-----------|----------|
| 검색 | O(log n) | O(1) 평균 | O(log n) | O(n) |
| 삽입 | O(log n) | O(1) 평균 | O(n) | O(1) |
| 삭제 | O(log n) | O(1) 평균 | O(n) | O(1) |
| 순서 | O | X | O | O |
| 범위 검색 | ★ O | X | O | X |
| 최솟값/최댓값 | O(log n) | O(n) | O(1) | O(n) |

> **★ 선택 기준**:
> - 정렬 + 검색 + 동적 → **BST (균형 트리)**
> - 빠른 조회만 → **해시 테이블**
> - 정적 + 메모리 효율 → **정렬 배열**
> - DB 인덱스 → **B-Tree**

---

### Ⅳ. 실무 적용 방안

#### 10. 실무 적용 시나리오

| 적용 분야 | 구체적 적용 방법 | 기대 효과 |
|---------|----------------|----------|
| **DB 인덱스** | B+ Tree로 클러스터드/세컨더리 인덱스 | 조회 100배+ 향상 |
| **파일 시스템** | 디렉토리 계층 구조 | 탐색 O(log n) |
| **HTML/XML DOM** | 트리 구조로 문서 표현 | 검색/순회 효율 |
| **결정 트리 (ML)** | 분류/회귀 모델 | 해석 가능한 AI |
| **네트워크 라우팅** | 트리 기반 라우팅 테이블 | 빠른 패킷 전달 |

#### 11. 실제 기업/서비스 사례

- **MySQL InnoDB**: B+ Tree로 인덱스 구현
- **Java TreeMap**: 레드블랙 트리 기반 정렬 맵
- **Linux kernel**: CFS 스케줄러에 레드블랙 트리 사용
- **Elasticsearch**: Lucene의 inverted index에 트리 활용
- **Git**: 커밋 히스토리를 DAG(트리 변형)로 관리

#### 12. 도입 시 고려사항

1. **기술적**:
   - 데이터 패턴에 맞는 트리 선택 (BST vs B-Tree)
   - 균형 유지 오버헤드 고려
   - 메모리 vs 디스크 기반 선택

2. **운영적**:
   - 재구축(Rebalancing) 비용
   - 동시성 제어 (Lock/Lock-free)

3. **보안적**:
   - 악의적 입력으로 편향 트리 유도 방지
   - 데이터 무결성 검증

4. **경제적**:
   - 기존 DB 인덱스 활용
   - 라이브러리 선택 (std::map, TreeMap 등)

#### 13. 주의사항 / 흔한 실수

- ❌ BST에 정렬된 데이터 삽입 → 편향 트리 (O(n))
- ❌ 재귀 깊이 과다 → 스택 오버플로우
- ❌ 순회 중 수정 → 무한 루프/오류
- ❌ 메모리 해제 누락 → 메모리 릭

#### 14. 관련 개념

```
📌 트리 자료구조 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│  [그래프] ←──→ [트리] ←──→ [힙]                                │
│       ↓           ↓           ↓                                │
│  [DFS/BFS]   [BST/AVL]   [우선순위큐]                          │
│       ↓           ↓                                             │
│  [최단경로]  [DB 인덱스]                                        │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 그래프 | 상위 개념 | 트리는 사이클 없는 그래프 | `[그래프](./graph.md)` |
| 힙 | 특수 트리 | 완전 이진 트리 + 힙 속성 | `[힙](./heap.md)` |
| B-트리 | 확장 | DB 인덱스용 다진 트리 | `[B-트리](./b_tree.md)` |
| 트라이 | 응용 | 문자열 특화 트리 | `[트라이](./trie.md)` |
| 세그먼트 트리 | 응용 | 구간 쿼리 특화 | 관련 문서 참조 |

---

### Ⅴ. 기대 효과 및 결론

#### 15. 정량적 기대 효과

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 검색 성능 | O(n) → O(log n) | 대용량 데이터에서 100배+ 향상 |
| 정렬 유지 | 동적 삽입/삭제 시 정렬 유지 | 정렬 비용 0 |
| DB 인덱스 | B+ Tree 인덱싱 | 쿼리 응답 90% 단축 |
| 메모리 효율 | 균형 트리 선택 | 최악의 경우 방지 |

#### 16. 미래 전망

1. **기술 발전 방향**:
   - Lock-free 트리 (동시성 최적화)
   - 캐시 친화적 트리 (B-tree 변형)

2. **시장 트렌드**:
   - SSD/NVM 최적화 트리 (LSM Tree)
   - 분산 트리 인덱스

3. **후속 기술**:
   - 머신러닝 기반 인덱스 (Learned Index)
   - 양자 트리 알고리즘

> **결론**: 트리는 계층 데이터 표현과 효율적 검색의 핵심 자료구조다. BST는 기본이지만 편향 가능성이 있어, AVL/레드블랙/B-트리 등 균형 트리가 실무에서 필수적이다.

> **※ 참고 표준**: CLRS 'Introduction to Algorithms', Knuth 'The Art of Computer Programming Vol.3'

---

## 어린이를 위한 종합 설명

**트리 자료구조를 쉽게 이해해보자!**

트리는 마치 **가계도(족보)**와 같아요. 맨 위에 할아버지(루트)가 계시고, 아래로 자식들이 뻗어나가요.

첫째, **뿌리에서 가지로**예요. 나무를 거꾸로 뒤집어 생각해보세요. 뿌리(루트)가 제일 위에 있고, 가지들이 아래로 뻗어나가요. 각 가지에서 또 다른 가지가 나올 수 있어요.

둘째, **빨리 찾기**예요. 이진 탐색 트리에서는 작은 건 왼쪽, 큰 건 오른쪽에 둬요. 50보다 작은 건 왼쪽, 큰 건 오른쪽! 이렇게 하면 한 번 비교할 때마다 절반씩 줄어들어서 아주 빨리 찾을 수 있어요.

---