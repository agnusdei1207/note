+++
title = "무결성 (Integrity)"
date = "2026-03-04"
[extra]
categories = "studynotes-09_security"
+++

# 무결성 (Integrity)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 정보가 무단으로 생성, 수정, 삭제되지 않고 원본 상태가 유지됨을 보장하는 정보보안의 핵심 속성으로, 데이터의 정확성과 완전성을 기술적·절차적으로 보호합니다.
> 2. **가치**: 금융 거래의 정확성, 의료 기록의 신뢰성, 법적 증거의 효력 등 데이터 기반 사회의 근간을 형성하며, 시스템 오류와 악의적 변조를 모두 방어합니다.
> 3. **융합**: 해시 함수, 전자서명, MAC, 블록체인, 버전 관리 등 다양한 기술이 결합된 다층 무결성 보증 체계의 핵심 목표입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**무결성(Integrity)**은 데이터가 인가되지 않은 방식으로 변경되지 않았음을 보장하는 보안 속성입니다. 이는 단순히 "데이터가 변하지 않았다"는 소극적 개념을 넘어, 데이터의 **정확성(Accuracy)**, **완전성(Completeness)**, **일관성(Consistency)**을 적극적으로 보증하는 개념입니다.

**정보보안 표준(ISO 27000) 정의**:
> "자산의 정확성과 완전성을 보호하는 특성"

**무결성의 세부 속성**:
- **정확성**: 데이터가 참값과 일치함
- **완전성**: 필요한 모든 데이터가 존재함
- **일관성**: 데이터 간 논리적 모순이 없음
- **적시성**: 데이터가 적절한 시점에 최신 상태임

#### 2. 💡 비유를 통한 이해
무결성은 **'봉인된 문서'**에 비유할 수 있습니다.
- **봉인(Seal)**: 문서가 열리지 않았음을 증명 - 해시 값
- **서명(Signature)**: 작성자가 누구인지 증명 - 전자서명
- **감사 로그**: 누가 언제 열었는지 기록 - 접근 로그
- **원본 보관**: 변경 시 원본 대비 확인 - 버전 관리

#### 3. 등장 배경 및 발전 과정
1. **초기 데이터 무결성**: 1960~70년대 데이터베이스 시스템의 ACID 트랜잭션
2. **네트워크 무결성**: 1970년대 CRC(Cyclic Redundancy Check) 등 오류 검출
3. **암호학적 무결성**: 1979년 HMAC, 1991년 전자서명법 제정
4. **Biba 모델 (1977)**: Bell-LaPadula의 기밀성 모델과 대비되는 무결성 모델
5. **블록체인 (2008)**: 분산 원장 기반 변조 불가능 무결성
6. **현대적 접근**: Zero Trust에서 지속적 무결성 검증

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 무결성 보호 기술 체계 (표)

| 기술 | 원리 | 보안 강도 | 용도 | 성능 |
|:---|:---|:---|:---|:---|
| **CRC-32** | 다항식 나눗셈 | 낮음 (오류만) | 통신 오류 검출 | 매우 빠름 |
| **MD5** | 128-bit 해시 | 취약 (충돌 존재) | 레거시만 | 빠름 |
| **SHA-256** | 256-bit 해시 | 높음 | 일반 무결성 | 빠름 |
| **SHA-384/512** | 384/512-bit 해시 | 매우 높음 | 고보안 요구 | 중간 |
| **SHA-3 (Keccak)** | 스펀지 구조 | 매우 높음 | 미래 표준 | 중간 |
| **HMAC-SHA256** | 키+해시 | 매우 높음 | 메시지 인증 | 빠름 |
| **RSA-PSS** | 확률적 서명 | 매우 높음 | 전자서명 | 느림 |
| **ECDSA P-256** | 타원곡선 서명 | 매우 높음 | 디지털 서명 | 중간 |
| **Ed25519** | EdDSA 서명 | 매우 높음 | 고속 서명 | 빠름 |
| **BLAKE3** | 해시 함수 | 높음 | 고속 무결성 | 매우 빠름 |

#### 2. 무결성 보호 아키텍처 다이어그램

```text
<<< Multi-Layer Integrity Protection Architecture >>>

+------------------------------------------------------------------+
|                    데이터 수명주기 무결성 보호                      |
+------------------------------------------------------------------+
                                                                   |
    [생성] ─────► [저장] ─────► [전송] ─────► [처리] ─────► [폐기]  |
       |            |             |             |             |     |
       v            v             v             v             v     |
    +-------+   +-------+    +-------+    +-------+    +-------+   |
    | 입력  |   | 저장   |    | 전송  |    | 처리   |    | 삭제   |   |
    | 검증  |   | 무결성 |    | 무결성|    | 무결성 |    | 무결성 |   |
    +-------+   +-------+    +-------+    +-------+    +-------+   |
         |           |             |             |             |     |
         v           v             v             v             v     |
    +----------------------------------------------------------+   |
    |              무결성 검증 기술 계층                         |   |
    |                                                            |   |
    |  +------------------+  +------------------+  +-----------+ |   |
    |  | 해시 함수 (Hash)  |  | MAC (메시지 인증)|  | 전자서명  | |   |
    |  | - SHA-2/3        |  | - HMAC           |  | - RSA     | |   |
    |  | - BLAKE3         |  | - CMAC           |  | - ECDSA   | |   |
    |  | - Whirlpool      |  | - GMAC (GCM)     |  | - EdDSA   | |   |
    |  +------------------+  +------------------+  +-----------+ |   |
    |                                                            |   |
    +----------------------------------------------------------+   |
                                                                   |
    +----------------------------------------------------------+   |
    |              무결성 모델 (Integrity Models)               |   |
    |                                                            |   |
    |  [Biba Model]          [Clark-Wilson]      [Chinese Wall] |   |
    |  - No Write Up         - Unauth TX         - Conflict Set |   |
    |  - No Read Down        - Auth TX            - Access Log  |   |
    |  - Invocation          - Constrained Data                 |   |
    |                         Integrity (CDI)                   |   |
    |                                                            |   |
    +----------------------------------------------------------+   |
                                                                   |
    +----------------------------------------------------------+   |
    |              구현 계층 (Implementation Layer)             |   |
    |                                                            |   |
    |  [DB Layer]           [App Layer]         [Network Layer] |   |
    |  - ACID TX            - Input Validation  - TLS MAC       |   |
    |  - Triggers           - Schema Check      - IPsec AH      |   |
    |  - Constraints        - Business Rule     - TCP Checksum  |   |
    |  - Row Signing        - State Machine                     |   |
    |                                                            |   |
    +----------------------------------------------------------+   |
                                                                   |
+------------------------------------------------------------------+
```

#### 3. 심층 동작 원리: 암호학적 무결성 검증

**① 해시 함수 기반 무결성 검증**

```python
import hashlib
import hmac
from typing import Tuple, Optional
import secrets
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class IntegrityRecord:
    """무결성 검증 레코드"""
    data_hash: str
    algorithm: str
    timestamp: str
    salt: Optional[str] = None
    signature: Optional[str] = None
    previous_hash: Optional[str] = None  # 블록체인 스타일 체인

class IntegrityManager:
    """
    다층 무결성 보호 시스템
    - 해시 기반 무결성
    - MAC 기반 인증
    - 전자서명 기반 부인방지
    - 체인 기반 이력 관리
    """

    SUPPORTED_HASH_ALGORITHMS = {
        'sha256': hashlib.sha256,
        'sha384': hashlib.sha384,
        'sha512': hashlib.sha512,
        'sha3_256': hashlib.sha3_256,
        'sha3_512': hashlib.sha3_512,
        'blake2b': hashlib.blake2b,
        'blake2s': hashlib.blake2s,
    }

    def __init__(self,
                 default_algorithm: str = 'sha256',
                 hmac_key: Optional[bytes] = None):
        self.default_algorithm = default_algorithm
        self.hmac_key = hmac_key or secrets.token_bytes(32)
        self.integrity_chain: list[IntegrityRecord] = []

    def compute_hash(self,
                     data: bytes,
                     algorithm: str = None,
                     salt: bytes = None) -> str:
        """
        암호학적 해시 계산
        - 솔트 적용으로 레인보우 테이블 방어
        - 다양한 알고리즘 지원
        """
        algo = algorithm or self.default_algorithm
        if algo not in self.SUPPORTED_HASH_ALGORITHMS:
            raise ValueError(f"Unsupported algorithm: {algo}")

        hash_func = self.SUPPORTED_HASH_ALGORITHMS[algo]

        if salt:
            data = salt + data

        return hash_func(data).hexdigest()

    def compute_mac(self, data: bytes, key: bytes = None) -> str:
        """
        HMAC 계산 - 키 기반 메시지 인증 코드
        - 무결성 + 인증 동시 보장
        """
        use_key = key or self.hmac_key
        return hmac.new(use_key, data, hashlib.sha256).hexdigest()

    def verify_hash(self,
                    data: bytes,
                    expected_hash: str,
                    algorithm: str = None,
                    salt: bytes = None) -> Tuple[bool, str]:
        """
        해시 기반 무결성 검증
        Returns: (검증결과, 상태메시지)
        """
        computed = self.compute_hash(data, algorithm, salt)
        match = hmac.compare_digest(computed, expected_hash)

        if match:
            return True, "Integrity verified successfully"
        else:
            return False, f"Integrity violation detected: expected {expected_hash[:16]}..., got {computed[:16]}..."

    def verify_mac(self,
                   data: bytes,
                   expected_mac: str,
                   key: bytes = None) -> Tuple[bool, str]:
        """
        MAC 검증 - 무결성 + 출처 인증
        """
        computed = self.compute_mac(data, key)
        match = hmac.compare_digest(computed, expected_mac)

        if match:
            return True, "MAC verified - integrity and authenticity confirmed"
        else:
            return False, "MAC verification failed - data may be tampered or key incorrect"

    def create_integrity_record(self,
                                data: bytes,
                                algorithm: str = None,
                                include_signature: bool = False,
                                private_key: bytes = None) -> IntegrityRecord:
        """
        무결성 레코드 생성
        - 해시 계산
        - 체인 연결 (이전 해시 포함)
        - 선택적 서명
        """
        salt = secrets.token_bytes(16)
        data_hash = self.compute_hash(data, algorithm, salt)

        previous_hash = None
        if self.integrity_chain:
            previous_hash = self.integrity_chain[-1].data_hash

        record = IntegrityRecord(
            data_hash=data_hash,
            algorithm=algorithm or self.default_algorithm,
            timestamp=datetime.utcnow().isoformat(),
            salt=salt.hex(),
            previous_hash=previous_hash
        )

        if include_signature and private_key:
            record.signature = self._sign_record(record, private_key)

        self.integrity_chain.append(record)
        return record

    def verify_chain_integrity(self) -> Tuple[bool, list]:
        """
        전체 체인 무결성 검증
        - 각 레코드의 previous_hash 일치 확인
        - 탬퍼링 지점 식별
        """
        violations = []

        for i, record in enumerate(self.integrity_chain):
            if i == 0:
                continue

            expected_prev = self.integrity_chain[i-1].data_hash
            if record.previous_hash != expected_prev:
                violations.append({
                    'index': i,
                    'expected_previous': expected_prev,
                    'actual_previous': record.previous_hash,
                    'message': 'Chain broken at this point'
                })

        return len(violations) == 0, violations

    def _sign_record(self, record: IntegrityRecord, private_key: bytes) -> str:
        """레코드 서명 (시뮬레이션 - 실제로는 RSA/ECDSA 사용)"""
        # 실제 구현에서는 cryptography 라이브러리의 서명 기능 사용
        record_bytes = json.dumps({
            'hash': record.data_hash,
            'algo': record.algorithm,
            'ts': record.timestamp,
            'prev': record.previous_hash
        }, sort_keys=True).encode()

        return hmac.new(private_key, record_bytes, hashlib.sha256).hexdigest()


class DatabaseIntegrityChecker:
    """
    데이터베이스 무결성 검사기
    - 참조 무결성 (Referential Integrity)
    - 엔티티 무결성 (Entity Integrity)
    - 도메인 무결성 (Domain Integrity)
    - 사용자 정의 무결성 (User-defined Integrity)
    """

    def __init__(self):
        self.constraints = []
        self.violations = []

    def add_constraint(self,
                       constraint_type: str,
                       table: str,
                       column: str,
                       rule: dict):
        """무결성 제약조건 추가"""
        self.constraints.append({
            'type': constraint_type,
            'table': table,
            'column': column,
            'rule': rule
        })

    def check_entity_integrity(self,
                               table_data: list,
                               primary_key: str) -> Tuple[bool, list]:
        """
        엔티티 무결성 검사
        - 기본키 NOT NULL
        - 기본키 UNIQUE
        """
        violations = []
        seen_pk_values = set()

        for i, row in enumerate(table_data):
            pk_value = row.get(primary_key)

            # NOT NULL 검사
            if pk_value is None:
                violations.append({
                    'row': i,
                    'violation': 'PRIMARY_KEY_NULL',
                    'message': f'Primary key {primary_key} cannot be null'
                })
                continue

            # UNIQUE 검사
            if pk_value in seen_pk_values:
                violations.append({
                    'row': i,
                    'violation': 'PRIMARY_KEY_DUPLICATE',
                    'message': f'Duplicate primary key value: {pk_value}'
                })

            seen_pk_values.add(pk_value)

        self.violations.extend(violations)
        return len(violations) == 0, violations

    def check_referential_integrity(self,
                                    child_table: list,
                                    parent_table: list,
                                    foreign_key: str,
                                    referenced_key: str) -> Tuple[bool, list]:
        """
        참조 무결성 검사
        - 외래키 값이 참조 테이블에 존재
        """
        violations = []
        parent_keys = {row[referenced_key] for row in parent_table}

        for i, row in enumerate(child_table):
            fk_value = row.get(foreign_key)

            if fk_value is not None and fk_value not in parent_keys:
                violations.append({
                    'row': i,
                    'violation': 'FOREIGN_KEY_VIOLATION',
                    'message': f'Foreign key {fk_value} not found in parent table'
                })

        self.violations.extend(violations)
        return len(violations) == 0, violations

    def check_domain_integrity(self,
                               table_data: list,
                               column: str,
                               data_type: str,
                               constraints: dict) -> Tuple[bool, list]:
        """
        도메인 무결성 검사
        - 데이터 타입 일치
        - CHECK 제약조건
        - NOT NULL 제약조건
        """
        violations = []

        for i, row in enumerate(table_data):
            value = row.get(column)

            # NOT NULL 검사
            if constraints.get('not_null', False) and value is None:
                violations.append({
                    'row': i,
                    'violation': 'NOT_NULL_VIOLATION',
                    'message': f'Column {column} cannot be null'
                })
                continue

            if value is None:
                continue

            # 데이터 타입 검사
            type_validators = {
                'integer': lambda v: isinstance(v, int),
                'string': lambda v: isinstance(v, str),
                'float': lambda v: isinstance(v, (int, float)),
                'boolean': lambda v: isinstance(v, bool),
                'date': lambda v: isinstance(v, str) and '-' in v  # 단순화
            }

            validator = type_validators.get(data_type)
            if validator and not validator(value):
                violations.append({
                    'row': i,
                    'violation': 'TYPE_VIOLATION',
                    'message': f'Column {column} expected {data_type}, got {type(value).__name__}'
                })

            # 범위 검사 (CHECK 제약조건)
            if 'min_value' in constraints and value < constraints['min_value']:
                violations.append({
                    'row': i,
                    'violation': 'CHECK_VIOLATION',
                    'message': f'Value {value} below minimum {constraints["min_value"]}'
                })

            if 'max_value' in constraints and value > constraints['max_value']:
                violations.append({
                    'row': i,
                    'violation': 'CHECK_VIOLATION',
                    'message': f'Value {value} exceeds maximum {constraints["max_value"]}'
                })

        self.violations.extend(violations)
        return len(violations) == 0, violations


class FileIntegrityMonitor:
    """
    파일 시스템 무결성 모니터링
    - 파일 변경 감지
    - 무결성 베이스라인 관리
    - 실시간 모니터링
    """

    def __init__(self):
        self.baseline: dict = {}  # path -> hash

    def create_baseline(self, file_paths: list) -> dict:
        """파일 무결성 베이스라인 생성"""
        baseline = {}

        for path in file_paths:
            try:
                with open(path, 'rb') as f:
                    content = f.read()

                baseline[path] = {
                    'hash': hashlib.sha256(content).hexdigest(),
                    'size': len(content),
                    'modified_time': datetime.utcnow().isoformat(),
                    'algorithm': 'sha256'
                }
            except FileNotFoundError:
                baseline[path] = {'error': 'File not found'}

        self.baseline = baseline
        return baseline

    def check_integrity(self, file_paths: list = None) -> dict:
        """
        파일 무결성 검사
        - 변경/추가/삭제 감지
        """
        check_paths = file_paths or list(self.baseline.keys())
        results = {
            'unchanged': [],
            'modified': [],
            'added': [],
            'deleted': [],
            'errors': []
        }

        for path in check_paths:
            if path not in self.baseline:
                results['added'].append(path)
                continue

            try:
                with open(path, 'rb') as f:
                    content = f.read()

                current_hash = hashlib.sha256(content).hexdigest()
                baseline_hash = self.baseline[path].get('hash')

                if current_hash == baseline_hash:
                    results['unchanged'].append(path)
                else:
                    results['modified'].append({
                        'path': path,
                        'baseline_hash': baseline_hash[:16] + '...',
                        'current_hash': current_hash[:16] + '...',
                        'baseline_size': self.baseline[path].get('size'),
                        'current_size': len(content)
                    })

            except FileNotFoundError:
                results['deleted'].append(path)
            except Exception as e:
                results['errors'].append({
                    'path': path,
                    'error': str(e)
                })

        return results


# 사용 예시
if __name__ == "__main__":
    # 1. 기본 무결성 관리
    integrity_mgr = IntegrityManager()

    data = b"Critical financial transaction: $1,000,000"

    # 무결성 레코드 생성
    record = integrity_mgr.create_integrity_record(data)
    print(f"Created integrity record: {record.data_hash[:32]}...")

    # MAC 계산
    mac = integrity_mgr.compute_mac(data)
    print(f"Computed MAC: {mac[:32]}...")

    # 2. 데이터베이스 무결성 검사
    db_checker = DatabaseIntegrityChecker()

    users = [
        {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
        {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
        {'id': None, 'name': 'Invalid', 'email': 'invalid@example.com'},  # NULL PK
        {'id': 1, 'name': 'Duplicate', 'email': 'dup@example.com'},  # Duplicate PK
    ]

    valid, violations = db_checker.check_entity_integrity(users, 'id')
    print(f"Entity integrity check: {'PASS' if valid else 'FAIL'}")
    for v in violations:
        print(f"  - {v['message']}")

    # 3. 파일 무결성 모니터링
    file_monitor = FileIntegrityMonitor()
    # baseline = file_monitor.create_baseline(['/etc/passwd', '/etc/hosts'])
    # results = file_monitor.check_integrity()
```

#### 4. Biba 무결성 모델 상세 분석

```text
<<< Biba 무결성 모델 (Integrity Model) >>>

                    무결성 레벨 (Integrity Levels)
    ┌─────────────────────────────────────────────────────┐
    │  Level 3: Crucial (C) - 최고 무결성                 │
    │  Level 2: Important (I) - 중요 무결성               │
    │  Level 1: Normal (N) - 일반 무결성                  │
    │  Level 0: Unclassified (U) - 낮은 무결성            │
    └─────────────────────────────────────────────────────┘

    핵심 속성 (Core Properties):

    1. Simple Integrity Property (No Read Down)
       ┌───────────────────────────────────────────┐
       │   Subject at level L can only read        │
       │   objects at level L or above             │
       │                                           │
       │   [Subject: High] ───READ──OK── [Object: High]│
       │   [Subject: High] ───READ──X── [Object: Low]│
       │                                           │
       │   이유: 낮은 레벨의 오염된 데이터가        │
       │         높은 레벨로 유입되는 것을 방지     │
       └───────────────────────────────────────────┘

    2. Star (*) Integrity Property (No Write Up)
       ┌───────────────────────────────────────────┐
       │   Subject at level L can only write       │
       │   to objects at level L or below          │
       │                                           │
       │   [Subject: Low] ───WRITE──X── [Object: High]│
       │   [Subject: Low] ───WRITE──OK── [Object: Low]│
       │                                           │
       │   이유: 낮은 레벨의 주체가 높은 레벨       │
       │         데이터를 오염시키는 것을 방지     │
       └───────────────────────────────────────────┘

    3. Invocation Property
       ┌───────────────────────────────────────────┐
       │   Subject can only invoke subjects        │
       │   at same or lower level                  │
       │                                           │
       │   [Low Subject] ───INVOKE──X── [High Subject]│
       │   [High Subject] ───INVOKE──OK── [Low Subject]│
       └───────────────────────────────────────────┘

    Bell-LaPadula vs Biba 비교:

    +-------------------+-------------------+-------------------+
    |       속성        |   Bell-LaPadula   |       Biba        |
    +-------------------+-------------------+-------------------+
    |   보안 목표       |     기밀성        |      무결성       |
    |   No Read Up      |        O          |         X         |
    |   No Read Down    |        X          |         O         |
    |   No Write Up     |        X          |         O         |
    |   No Write Down   |        O          |         X         |
    +-------------------+-------------------+-------------------+

    실제 적용 예시 (시스템 관리):

    +-------------------+     +-------------------+
    | Kernel (Crucial)  |     | System Config     │
    | - Read: C,I,N,U   │     │ Files (Important) │
    | - Write: C only   │     │ - Read: I,N,U     │
    +-------------------+     │ - Write: I,C      │
              │               +-------------------+
              │ Can read
              v
    +-------------------+     +-------------------+
    | Admin Tools       │     | User Data         │
    │ (Important)       │     │ (Normal)          │
    │ - Read: I,N,U     │     │ - Read: N,U       │
    │ - Write: I,N      │     │ - Write: N,I,C    │
    +-------------------+     +-------------------+
              │
              │ Cannot write to
              v
    +-------------------+
    | Untrusted App     │
    │ (Normal)          │
    │ - Read: N,U       │
    │ - Write: N,U      │
    +-------------------+
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 무결성 검증 기술 비교

| 기술 | 검증 항목 | 키 필요 | 부인방지 | 성능 | 용도 |
|:---|:---|:---|:---|:---|:---|
| **CRC-32** | 오류만 | X | X | 매우 빠름 | 통신 오류 |
| **MD5** | 충돌 취약 | X | X | 빠름 | 레거시 |
| **SHA-256** | 강력 | X | X | 빠름 | 일반 무결성 |
| **HMAC** | 강력+인증 | O | X | 빠름 | API 무결성 |
| **RSA-PSS** | 강력+서명 | O | O | 느림 | 전자서명 |
| **ECDSA** | 강력+서명 | O | O | 중간 | 디지털 서명 |
| **블록체인** | 변조 불가 | O | O | 느림 | 감사 추적 |

#### 2. 데이터베이스 무결성 제약조건 비교

| 제약 유형 | 설명 | 위반 시 | 예시 |
|:---|:---|:---|:---|
| **NOT NULL** | NULL 값 금지 | INSERT/UPDATE 거부 | user.email NOT NULL |
| **UNIQUE** | 중복 값 금지 | INSERT/UPDATE 거부 | user.username UNIQUE |
| **PRIMARY KEY** | 식별자 유일성 | INSERT/UPDATE 거부 | id PRIMARY KEY |
| **FOREIGN KEY** | 참조 무결성 | DELETE 거부 또는 CASCADE | order.user_id FK |
| **CHECK** | 도메인 제약 | INSERT/UPDATE 거부 | age CHECK (age >= 0) |
| **TRIGGER** | 사용자 정의 | 트리거 실행 | audit_log INSERT |

#### 3. 과목 융합 관점 분석

**데이터베이스와 무결성**:
- ACID 트랜잭션: 원자성, 일관성, 격리성, 지속성
- 제약조건: NOT NULL, UNIQUE, FK, CHECK
- 트리거: 무결성 검증 자동화

**네트워크와 무결성**:
- TCP Checksum: 전송 오류 검출
- TLS MAC: 암호화 + 무결성
- IPsec AH: 인증 헤더로 무결성

**파일 시스템과 무결성**:
- 체크섬: 파일 무결성 검증
- 저널링: 메타데이터 무결성
- COW (Copy-on-Write): 스냅샷 무결성

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 금융 거래 시스템 무결성**
- **상황**: 초당 수만 건 거래, 데이터 변조 즉시 금전 손실
- **판단**:
  - 트랜잭션: ACID + 분산 트랜잭션 (2PC)
  - 감사 추적: 모든 변경 이력 블록체인 저장
  - 전자서명: 거래 데이터 서명으로 부인방지
  - 실시간 검증: SHA-256 + HMAC

**시나리오 2: 의료 기록 무결성**
- **상황**: 환자 진료 기록, 법적 증거력 필요
- **판단**:
  - WORM (Write Once Read Many): 수정 불가 저장
  - 디지털 타임스탬프: 생성 시점 증명
  - 변경 로그: 모든 수정 이력 보관
  - 전자서명: 의사 서명으로 진단서 무결성

**시나리오 3: 소프트웨어 공급망 무결성**
- **상황**: SolarWinds 사례, 빌드 산출물 변조
- **판단**:
  - SBOM (Software Bill of Materials)
  - 코드 서명: 모든 바이너리 서명
  - SLSA (Supply-chain Levels for Software Artifacts)
  - 서명 검증: 배포 전 서명 확인

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] 무결성 검증 지점 식별 (입력/저장/전송/처리)
- [ ] 알고리즘 선택 (성능 vs 보안 강도)
- [ ] 키 관리 체계 (HMAC/전자서명용)
- [ ] 성능 영향도 측정 (암호화 오버헤드)
- [ ] 오류 대응 절차 (무결성 위반 시)
- [ ] 감사 로그 보관 기간

#### 3. 안티패턴 (Anti-patterns)
- **MD5/SHA-1 사용**: 충돌 존재 → SHA-256 이상 사용
- **해시만 사용**: 인증 없이 → HMAC/서명 필요
- **무결성 검증 생략**: "암호화했으니 안전" → 변조 가능
- **키 하드코딩**: 소스코드에 MAC 키 → 키 유출 시 무력화

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | 내용 | 측정 지표 |
|:---|:---|:---|
| **정량적** | 데이터 변조 사고 감소 | 변조 탐지율 99.9% |
| **정량적** | 감사 비용 절감 | 감사 시간 60% 단축 |
| **정성적** | 데이터 신뢰성 향상 | 데이터 품질 점수 향상 |
| **정성적** | 법적 효력 확보 | 전자증거 인정률 100% |

#### 2. 미래 전망 및 진화 방향
- **양자 내성 해시**: SHA-3, SHAKE256 등 양자 저항
- **분산 무결성**: 블록체인 기술 확대 적용
- **AI 기반 이상 탐지**: 무결성 위반 패턴 학습
- **실시간 무결성**: Zero Trust 지속 검증

#### 3. 참고 표준/가이드
- **ISO/IEC 27001**: A.8.2 정보 분류 - 무결성 요구사항
- **FIPS 180-4**: SHA-3 표준
- **FIPS 198-1**: HMAC 표준
- **RFC 8017**: RSA-PSS 서명
- **NIST SP 800-107**: 해시 함수 사용 가이드

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[CIA Triad](@/studynotes/09_security/01_policy/cia_triad.md)**: 무결성을 포함한 정보보안 3대 요소
- **[기밀성](@/studynotes/09_security/01_policy/confidentiality.md)**: 기밀성과 무결성의 균형
- **[해시 함수](@/studynotes/09_security/02_crypto/encryption_algorithms.md)**: 무결성 검증 핵심 기술
- **[전자서명](@/studynotes/09_security/01_policy/pki.md)**: 부인방지 무결성 보장
- **[PKI](@/studynotes/09_security/01_policy/pki.md)**: 전자서명 인프라

---

### 👶 어린이를 위한 3줄 비유 설명
1. **봉인된 편지**: 편지를 보낼 때 봉투에 도장을 찍어요. 받은 사람이 도장이 뜯겨있으면 누군가 편지를 훔쳐본 거랍니다.
2. **숙제 검사**: 선생님이 숙제에 도장을 찍어주면, 나중에 숙제가 바뀌었는지 도장으로 확인할 수 있어요.
3. **비밀번호**: 온라인 게임 아이템이 다른 사람이 바꾸지 못하게 비밀번호로 보호하는 것과 같아요. 내용이 그대로인지 항상 확인하는 거예요.
