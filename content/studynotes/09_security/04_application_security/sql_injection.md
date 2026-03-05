+++
title = "SQL 인젝션 (SQL Injection)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# SQL 인젝션 (SQL Injection)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SQL 인젝션은 사용자 입력이 SQL 쿼리에 직접 삽입되어 공격자가 데이터베이스를 조작할 수 있는 OWASP Top 10 A03 취약점입니다.
> 2. **가치**: 데이터 유출, 인증 우회, 데이터 변조/삭제, 권한 상승이 가능하며, 파라미터화 쿼리로 100% 방어 가능합니다.
> 3. **융합**: ORM, Stored Procedure, 입력 검증, WAF로 다층 방어하며, Blind SQLi, Second-Order, Out-of-Band 등 다양한 변형이 존재합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. SQL 인젝션 유형

| 유형 | 설명 | 탐지 난이도 |
|:---|:---|:---|
| **In-Band (Classic)** | 오류 메시지, UNION으로 결과 확인 | 쉬움 |
| **Blind (Inferential)** | 참/거짓 반응으로 추론 | 어려움 |
| **Time-Based Blind** | 응답 지연으로 추론 | 매우 어려움 |
| **Out-of-Band** | DNS, HTTP로 데이터 유출 | 어려움 |
| **Second-Order** | 저장된 입력이 나중에 실행 | 매우 어려움 |

#### 2. 공격 예시

```sql
-- 1. 인증 우회
SELECT * FROM users WHERE username = 'admin'--' AND password = 'xxx'

-- 2. UNION 기반 데이터 유출
SELECT * FROM products WHERE id = 1 UNION SELECT username, password, NULL FROM users--

-- 3. Blind Boolean
SELECT * FROM users WHERE id = 1 AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin') = 'a'

-- 4. Time-Based Blind
SELECT * FROM users WHERE id = 1; IF (SUBSTRING(@@version,1,1) = '5') WAITFOR DELAY '0:0:5'--

-- 5. Stacked Queries
SELECT * FROM users WHERE id = 1; DROP TABLE users;--
```

#### 3. 방어 체계

```text
                    [ SQL 인젝션 방어 계층 ]

Layer 1: 입력 검증 (Input Validation)
         ┌─ 화이트리스트 기반
         ├─ 타입 검증
         └─ 길이 제한

Layer 2: 파라미터화 쿼리 (Parameterized Queries)
         ┌─ Prepared Statement
         ├─ ORM 사용
         └─ Stored Procedure

Layer 3: 최소 권한 (Least Privilege)
         ┌─ 읽기 전용 계정
         ├─ 테이블별 권한
         └─ DROP/TRUNCATE 금지

Layer 4: WAF (Web Application Firewall)
         ┌─ SQLi 시그니처 탐지
         ├─ 행위 기반 탐지
         └─ 가상 패치
```

---

### Ⅱ. 핵심 코드: 방어 구현

```python
import sqlite3
from typing import Optional, List, Any
from dataclasses import dataclass
import re

@dataclass
class User:
    id: int
    username: str
    email: str

class SecureDatabase:
    """안전한 데이터베이스 접근"""

    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    # 취약한 코드 (절대 사용 금지)
    def vulnerable_query(self, username: str) -> Optional[User]:
        """
        ⚠️ 취약한 코드 - SQL 인젝션 위험
        """
        query = f"SELECT * FROM users WHERE username = '{username}'"
        # 공격 입력: admin'--
        # 실행: SELECT * FROM users WHERE username = 'admin'--'
        cursor = self.conn.execute(query)
        row = cursor.fetchone()
        if row:
            return User(**row)
        return None

    # 안전한 코드 (파라미터화 쿼리)
    def safe_query(self, username: str) -> Optional[User]:
        """
        ✅ 안전한 코드 - 파라미터화 쿼리
        """
        query = "SELECT * FROM users WHERE username = ?"
        cursor = self.conn.execute(query, (username,))
        row = cursor.fetchone()
        if row:
            return User(id=row['id'], username=row['username'], email=row['email'])
        return None

    # 이름 기반 파라미터
    def safe_query_named(self, user_id: int, status: str) -> List[User]:
        """
        ✅ 이름 기반 파라미터화
        """
        query = """
            SELECT * FROM users
            WHERE id = :id AND status = :status
        """
        cursor = self.conn.execute(query, {'id': user_id, 'status': status})
        return [User(**row) for row in cursor.fetchall()]

    # IN 절 안전 처리
    def safe_in_query(self, user_ids: List[int]) -> List[User]:
        """
        ✅ IN 절 안전 처리
        """
        placeholders = ','.join('?' * len(user_ids))
        query = f"SELECT * FROM users WHERE id IN ({placeholders})"
        cursor = self.conn.execute(query, user_ids)
        return [User(**row) for row in cursor.fetchall()]

    # 동적 정렬 안전 처리
    def safe_order_by(self, sort_column: str, sort_order: str) -> List[User]:
        """
        ✅ 동적 정렬 안전 처리
        """
        # 화이트리스트 검증
        allowed_columns = {'id', 'username', 'email', 'created_at'}
        allowed_orders = {'ASC', 'DESC'}

        if sort_column not in allowed_columns:
            sort_column = 'id'
        if sort_order.upper() not in allowed_orders:
            sort_order = 'ASC'

        query = f"SELECT * FROM users ORDER BY {sort_column} {sort_order}"
        cursor = self.conn.execute(query)
        return [User(**row) for row in cursor.fetchall()]


class InputValidator:
    """입력 검증"""

    @staticmethod
    def validate_id(user_input: str) -> Optional[int]:
        """ID 검증 (숫자만)"""
        if re.match(r'^\d+$', user_input):
            return int(user_input)
        return None

    @staticmethod
    def validate_username(user_input: str) -> Optional[str]:
        """사용자명 검증"""
        if re.match(r'^[a-zA-Z0-9_]{3,20}$', user_input):
            return user_input
        return None

    @staticmethod
    def validate_email(user_input: str) -> Optional[str]:
        """이메일 검증"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, user_input):
            return user_input
        return None


class SQLiDetector:
    """SQL 인젝션 탐지"""

    PATTERNS = [
        r"('|\")\s*(OR|AND)\s*('|\")",  # 문자열 비교
        r"--\s*$",  # 주석
        r"/\*.*\*/",  # 블록 주석
        r";\s*(DROP|DELETE|UPDATE|INSERT)",  # 명령어
        r"UNION\s+SELECT",  # UNION
        r"WAITFOR\s+DELAY",  # 시간 지연
        r"BENCHMARK\s*\(",  # MySQL 시간 지연
        r"SLEEP\s*\(",  # MySQL SLEEP
        r"xp_cmdshell",  # SQL Server 명령
    ]

    @classmethod
    def detect(cls, user_input: str) -> List[str]:
        """SQL 인젝션 패턴 탐지"""
        detected = []
        for pattern in cls.PATTERNS:
            if re.search(pattern, user_input, re.IGNORECASE):
                detected.append(pattern)
        return detected

    @classmethod
    def is_malicious(cls, user_input: str) -> bool:
        """악의적 입력 여부"""
        return len(cls.detect(user_input)) > 0


# 사용 예시
if __name__ == "__main__":
    print("=== SQL 인젝션 방어 예시 ===")

    # 인젝션 탐지
    print("\n[SQLi 탐지]")
    malicious_inputs = [
        "admin'--",
        "1' OR '1'='1",
        "1; DROP TABLE users;--",
        "1 UNION SELECT username, password FROM users"
    ]

    for inp in malicious_inputs:
        is_mal = SQLiDetector.is_malicious(inp)
        print(f"  '{inp[:30]}...': {'악의적' if is_mal else '정상'}")

    # 입력 검증
    print("\n[입력 검증]")
    print(f"  ID '123': {InputValidator.validate_id('123')}")
    print(f"  ID '1 OR 1': {InputValidator.validate_id('1 OR 1')}")
    print(f"  Username 'john_doe': {InputValidator.validate_username('john_doe')}")
    print(f"  Username \"admin'--\": {InputValidator.validate_username(\"admin'--\")}")
