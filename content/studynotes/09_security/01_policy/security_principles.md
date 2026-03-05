+++
title = "보안 원칙 (Security Principles)"
date = "2026-03-04"
[extra]
categories = "studynotes-09_security"
+++

# 보안 원칙 (Security Principles)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 최소 권한, 직무 분리, 알 필요성, 심층 방어 등 정보보안 설계와 운영의 근간이 되는 불변의 지침 원칙들입니다.
> 2. **가치**: 보안 아키텍처 설계의 체크리스트, 보안 통제의 우선순위 결정, 보안 사고 예방의 근간을 형성합니다.
> 3. **융합**: Zero Trust, DevSecOps, Privacy by Design 등 현대적 보안 프레임워크의 기반이 됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**보안 원칙(Security Principles)**은 정보보안 시스템을 설계, 구현, 운영할 때 따라야 하는 근본적 지침입니다. 이는 특정 기술이나 제품에 구애받지 않는 **불변의 진리**로, 모든 보안 통제와 정책의 기준점이 됩니다.

**Saltzer와 Schroeder의 8대 원칙 (1975)**:
1. **경제성 (Economy of Mechanism)**: 단순한 설계
2. **실패 안전 (Fail-safe Defaults)**: 기본 거부
3. **완전 중재 (Complete Mediation)**: 모든 접근 검사
4. **개방 설계 (Open Design)**: 비밀 아닌 설계
5. **권한 분리 (Separation of Privilege)**: 다중 조건
6. **최소 권한 (Least Privilege)**: 필요 최소한
7. **최소 공통 메커니즘 (Least Common Mechanism)**: 공유 최소화
8. **심리적 수용성 (Psychological Acceptability)**: 사용자 친화

#### 2. 💡 비유를 통한 이해
보안 원칙은 **'요리의 기본 법칙'**에 비유할 수 있습니다.
- **최소 권한**: 필요한 만큼만 양념 - 과하면 망침
- **심층 방어**: 냉장고 + 밀폐용기 + 진공포장 - 다층 보관
- **직무 분리**: 한 명이 모든 요리를 하지 않음 - 감시와 균형
- **실패 안전**: 가스 밸브는 기본 잠김 - 안전 기본값

#### 3. 등장 배경 및 발전 과정
1. **고전 암호학**: "아무도 모르는 비밀이 가장 안전" → 오류
2. **Kerckhoffs 원칙 (1883)**: "시스템의 보안은 키의 비밀성에만 의존해야"
3. **Saltzer & Schroeder (1975)**: 8대 원칙 정립
4. **NIST SP 800-14**: 일반적으로 수용된 시스템 보안 원칙
5. **Zero Trust (2010)**: "절대 신뢰하지 말고 항상 검증"
6. **현대적 확장**: Privacy by Design, Security by Design

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 핵심 보안 원칙 체계 (표)

| 원칙 | 영문 | 핵심 내용 | 구현 예시 | 위반 시 위험 |
|:---|:---|:---|:---|:---|
| **최소 권한** | Least Privilege | 필요한 최소 권한만 부여 | RBAC, PAM | 권한 남용, 내부자 위협 |
| **직무 분리** | Separation of Duties | 한 사람이 모든 권한 X | 이중 서명, 4-eyes | 사기, 오류 미발견 |
| **알 필요성** | Need to Know | 업무에 필요한 정보만 | 데이터 분류, 접근 통제 | 정보 유출 |
| **심층 방어** | Defense in Depth | 다층 보안 통제 | 방화벽+IDS+EDR | 단일 실패 시 전체 붕괴 |
| **실패 안전** | Fail-safe Defaults | 기본값은 거부 | Default Deny, 방화벽 규칙 | 잘못된 허용 |
| **완전 중재** | Complete Mediation | 모든 접근 검사 | 매 요청마다 권한 확인 | 권한 회피 공격 |
| **개방 설계** | Open Design | 보안은 비밀이 아님 | 오픈소스 암호, 공개 알고리즘 | 보안 모호성 공격 |
| **경제성** | Economy of Mechanism | 단순한 설계 | KISS, 최소 복잡도 | 복잡성으로 인한 취약점 |
| **심리적 수용성** | Psychological Acceptability | 사용자 친화적 | SSO, 편리한 MFA | 사용자 우회 |

#### 2. 보안 원칙 적용 아키텍처 다이어그램

```text
<<< Security Principles Applied to System Architecture >>>

    +----------------------------------------------------------+
    |                    사용자/시스템                          |
    +----------------------------------------------------------+
                                │
                                │ [완전 중재] 모든 요청 검사
                                v
    +----------------------------------------------------------+
    |              인증 계층 (Authentication Layer)             |
    |  +----------------------------------------------------+  |
    |  |  [최소 권한] 인증에 필요한 정보만 수집              |  |
    |  |  [심리적 수용성] SSO + FIDO2                        |  |
    |  +----------------------------------------------------+  |
    +----------------------------------------------------------+
                                │
                                │ [실패 안전] 인증 실패 시 거부
                                v
    +----------------------------------------------------------+
    |              인가 계층 (Authorization Layer)              |
    |  +----------------------------------------------------+  |
    |  |  [최소 권한] RBAC + ABAC                           |  |
    |  |  [직무 분리] SoD 규칙 적용                         |  |
    |  |  [알 필요성] 데이터 분류 기반 접근                 |  |
    |  +----------------------------------------------------+  |
    +----------------------------------------------------------+
                                │
                                │ [심층 방어] 다층 보안
                                v
    +----------------------------------------------------------+
    |              네트워크 계층 (Network Layer)                |
    |  +----------------------------------------------------+  |
    |  |  [심층 방어] 방화벽 + IDS/IPS + WAF               |  |
    |  |  [실패 안전] Default Deny 정책                    |  |
    |  |  [최소 공통 메커니즘] 마이크로 세그멘테이션        |  |
    |  +----------------------------------------------------+  |
    +----------------------------------------------------------+
                                │
                                │ [완전 중재] 모든 트래픽 검사
                                v
    +----------------------------------------------------------+
    |              애플리케이션 계층 (Application Layer)        |
    |  +----------------------------------------------------+  |
    |  |  [경제성] 단순한 코드, 최소 권한 프로세스          |  |
    |  |  [개방 설계] 검증된 오픈소스 라이브러리            |  |
    |  |  [실패 안전] 예외 처리, 안전한 기본값              |  |
    |  +----------------------------------------------------+  |
    +----------------------------------------------------------+
                                │
                                v
    +----------------------------------------------------------+
    |              데이터 계층 (Data Layer)                     |
    |  +----------------------------------------------------+  |
    |  |  [알 필요성] 컬럼 수준 암호화                      |  |
    |  |  [심층 방어] TDE + 앱 레벨 암호화                  |  |
    |  |  [최소 권한] DB 역할 기반 접근                     |  |
    |  +----------------------------------------------------+  |
    +----------------------------------------------------------+

<<< Principle Violation Examples >>>

    [최소 권한 위반]
    ┌─────────────────────────────────────────────────────────┐
    │ 문제: 모든 개발자에게 DB 관리자 권한 부여              │
    │ 결과: 개발자가 운영 DB 실수로 삭제                     │
    │ 해결: 읽기 전용 권한만 부여, 운영 DB는 별도 권한       │
    └─────────────────────────────────────────────────────────┘

    [심층 방어 위반]
    ┌─────────────────────────────────────────────────────────┐
    │ 문제: 방화벽만 의존, 내부망 보안 없음                  │
    │ 결과: VPN 탈취 시 내부망 전체 노출                     │
    │ 해결: 마이크로 세그멘테이션 + EDR + 암호화             │
    └─────────────────────────────────────────────────────────┘

    [직무 분리 위반]
    ┌─────────────────────────────────────────────────────────┐
    │ 문제: 한 사람이 결제 승인 및 실행 권한 보유            │
    │ 결과: 내부자 횡령 발생                                 │
    │ 해결: 승인자와 실행자 분리, 이중 서명 필요             │
    └─────────────────────────────────────────────────────────┘
```

#### 3. 심층 동작 원리: 보안 원칙 구현 코드

```python
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Callable, Any
from enum import Enum
from functools import wraps
import inspect

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    EXECUTE = "execute"

class DataClassification(Enum):
    PUBLIC = 1
    INTERNAL = 2
    CONFIDENTIAL = 3
    TOP_SECRET = 4

@dataclass
class User:
    id: str
    name: str
    roles: Set[str] = field(default_factory=set)
    clearances: Set[DataClassification] = field(default_factory=set)

    def has_role(self, role: str) -> bool:
        return role in self.roles

    def has_clearance(self, level: DataClassification) -> bool:
        return any(c.value >= level.value for c in self.clearances)

@dataclass
class Resource:
    id: str
    name: str
    classification: DataClassification
    owner_id: str

# ============================================
# 1. 최소 권한 원칙 (Principle of Least Privilege)
# ============================================

class LeastPrivilegeEnforcer:
    """
    최소 권한 원칙 구현
    - 역할 기반 접근 제어
    - 권한 요청 시 필요한 권한만 부여
    - Just-In-Time 권한 상승
    """

    def __init__(self):
        # 역할별 최소 권한 정의
        self.role_permissions: Dict[str, Set[Permission]] = {
            'viewer': {Permission.READ},
            'editor': {Permission.READ, Permission.WRITE},
            'admin': {Permission.READ, Permission.WRITE, Permission.DELETE},
            'super_admin': {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN}
        }

        # 사용자별 추가 권한 (일시적)
        self.temporary_permissions: Dict[str, Dict[str, Set[Permission]]] = {}

    def get_permissions(self, user: User, resource_id: str) -> Set[Permission]:
        """사용자의 리소스에 대한 실제 권한 반환"""
        permissions = set()

        # 역할 기반 권한
        for role in user.roles:
            if role in self.role_permissions:
                permissions.update(self.role_permissions[role])

        # 일시적 권한 (Just-In-Time)
        if user.id in self.temporary_permissions:
            if resource_id in self.temporary_permissions[user.id]:
                permissions.update(
                    self.temporary_permissions[user.id][resource_id]
                )

        return permissions

    def grant_temporary_permission(self,
                                   user: User,
                                   resource_id: str,
                                   permissions: Set[Permission],
                                   duration_minutes: int = 60):
        """
        Just-In-Time 권한 부여
        일시적으로 필요한 권한만 부여
        """
        if user.id not in self.temporary_permissions:
            self.temporary_permissions[user.id] = {}

        self.temporary_permissions[user.id][resource_id] = permissions

        # 실제로는 타이머로 자동 만료 구현
        print(f"Granted temporary permissions to {user.name} for {resource_id}")

    def check_permission(self,
                        user: User,
                        resource_id: str,
                        required_permission: Permission) -> bool:
        """권한 확인"""
        permissions = self.get_permissions(user, resource_id)
        return required_permission in permissions

# ============================================
# 2. 직무 분리 원칙 (Separation of Duties)
# ============================================

class SeparationOfDutiesEnforcer:
    """
    직무 분리 원칙 구현
    - 상충 역할 동시 보유 방지
    - 다중 승인 요구
    - 감사 추적
    """

    def __init__(self):
        # 상충 역할 정의 (동시 보유 금지)
        self.conflicting_roles: Dict[str, Set[str]] = {
            'payment_creator': {'payment_approver'},
            'user_creator': {'user_admin'},
            'developer': {'production_admin'},
            'auditor': {'system_admin'}
        }

        # 다중 승인 요구 작업
        self.dual_control_tasks: Dict[str, int] = {
            'large_payment': 2,  # 2명 승인 필요
            'user_creation': 2,
            'system_config_change': 2,
            'data_deletion': 3
        }

        # 작업별 승인 현황
        self.pending_approvals: Dict[str, Dict[str, List[str]]] = {}

    def check_role_conflict(self, user: User, new_role: str) -> bool:
        """역할 충돌 확인"""
        for existing_role in user.roles:
            # 기존 역할과 새 역할이 충돌하는지 확인
            if new_role in self.conflicting_roles.get(existing_role, set()):
                return True
            if existing_role in self.conflicting_roles.get(new_role, set()):
                return True
        return False

    def assign_role(self, user: User, role: str) -> tuple[bool, str]:
        """역할 할당 (충돌 확인)"""
        if self.check_role_conflict(user, role):
            return False, f"Role '{role}' conflicts with existing roles"

        user.roles.add(role)
        return True, f"Role '{role}' assigned successfully"

    def request_approval(self,
                        task_type: str,
                        task_id: str,
                        requester_id: str) -> tuple[bool, str]:
        """작업 승인 요청"""
        if task_type not in self.dual_control_tasks:
            return True, "No dual control required"

        required_count = self.dual_control_tasks[task_type]

        if task_id not in self.pending_approvals:
            self.pending_approvals[task_id] = {'approvers': [], 'requester': requester_id}

        return False, f"Requires {required_count} approvers (4-eyes principle)"

    def approve_task(self,
                    task_type: str,
                    task_id: str,
                    approver_id: str) -> tuple[bool, str]:
        """작업 승인"""
        if task_type not in self.dual_control_tasks:
            return True, "No approval required"

        required_count = self.dual_control_tasks[task_type]

        if task_id not in self.pending_approvals:
            return False, "Task not found"

        approval = self.pending_approvals[task_id]

        # 요청자는 승인할 수 없음
        if approver_id == approval['requester']:
            return False, "Requester cannot approve own task"

        # 이미 승인한 경우
        if approver_id in approval['approvers']:
            return False, "Already approved"

        approval['approvers'].append(approver_id)

        if len(approval['approvers']) >= required_count:
            del self.pending_approvals[task_id]
            return True, "Task approved - all required approvals received"
        else:
            remaining = required_count - len(approval['approvers'])
            return False, f"Requires {remaining} more approval(s)"

# ============================================
# 3. 알 필요성 원칙 (Need to Know)
# ============================================

class NeedToKnowEnforcer:
    """
    알 필요성 원칙 구현
    - 데이터 분류 기반 접근
    - 업무 필요성 검증
    - 데이터 마스킹
    """

    def __init__(self):
        # 데이터 분류별 접근 권한 매핑
        self.classification_access = {
            DataClassification.PUBLIC: ['*'],
            DataClassification.INTERNAL: ['employee'],
            DataClassification.CONFIDENTIAL: ['manager', 'hr', 'finance'],
            DataClassification.TOP_SECRET: ['executive', 'security']
        }

    def check_access(self,
                    user: User,
                    resource: Resource,
                    business_justification: str = None) -> tuple[bool, str]:
        """접근 권한 확인"""
        # 1. 클리어런스 확인
        if not user.has_clearance(resource.classification):
            return False, "Insufficient clearance level"

        # 2. 알 필요성 확인
        classification = resource.classification
        allowed_roles = self.classification_access.get(classification, [])

        if '*' not in allowed_roles:
            has_valid_role = any(
                role in allowed_roles for role in user.roles
            )
            if not has_valid_role:
                return False, "No valid role for this classification"

        # 3. 비즈니스 사유 (높은 분류의 경우)
        if classification.value >= DataClassification.CONFIDENTIAL.value:
            if not business_justification:
                return False, "Business justification required for confidential+ data"

        return True, "Access granted"

    def mask_data(self,
                  data: str,
                  data_type: str,
                  user_clearance: DataClassification) -> str:
        """데이터 마스킹"""
        # 낮은 클리어런스는 마스킹 적용
        if user_clearance.value < DataClassification.CONFIDENTIAL.value:
            if data_type == 'email':
                # john.doe@company.com → j***@company.com
                parts = data.split('@')
                if len(parts) == 2:
                    masked = parts[0][0] + '***'
                    return f"{masked}@{parts[1]}"
            elif data_type == 'phone':
                # 010-1234-5678 → 010-****-5678
                parts = data.split('-')
                if len(parts) == 3:
                    return f"{parts[0]}-****-{parts[2]}"
            elif data_type == 'ssn':
                # 900101-1234567 → 900101-*******
                parts = data.split('-')
                if len(parts) == 2:
                    return f"{parts[0]}-*******"
            elif data_type == 'card':
                # 1234-5678-9012-3456 → ****-****-****-3456
                return '****-****-****-' + data[-4:]

        return data

# ============================================
# 4. 심층 방어 원칙 (Defense in Depth)
# ============================================

class DefenseInDepthEnforcer:
    """
    심층 방어 원칙 구현
    - 다층 보안 통제
    - 각 계층 독립적 방어
    - 한 계층 실패 시에도 보호
    """

    def __init__(self):
        self.layers: List[Callable] = []

    def add_layer(self, name: str, check_func: Callable):
        """보안 계층 추가"""
        self.layers.append((name, check_func))

    def check_all_layers(self, context: Dict) -> tuple[bool, List[str]]:
        """모든 계층 검사"""
        passed_layers = []
        failed_layers = []

        for name, check_func in self.layers:
            try:
                result = check_func(context)
                if result:
                    passed_layers.append(name)
                else:
                    failed_layers.append(name)
            except Exception as e:
                failed_layers.append(f"{name} (error: {str(e)})")

        return len(failed_layers) == 0, failed_layers

def create_security_stack():
    """심층 방어 보안 스택 생성"""

    defense = DefenseInDepthEnforcer()

    # Layer 1: 네트워크
    defense.add_layer(
        "Network Firewall",
        lambda ctx: ctx.get('source_ip') not in ctx.get('blocked_ips', [])
    )

    # Layer 2: 인증
    defense.add_layer(
        "Authentication",
        lambda ctx: ctx.get('authenticated', False)
    )

    # Layer 3: 인가
    defense.add_layer(
        "Authorization",
        lambda ctx: ctx.get('authorized', False)
    )

    # Layer 4: 입력 검증
    defense.add_layer(
        "Input Validation",
        lambda ctx: not any(x in ctx.get('input', '') for x in ['<script>', 'DROP TABLE', '../'])
    )

    # Layer 5: 속도 제한
    defense.add_layer(
        "Rate Limiting",
        lambda ctx: ctx.get('request_count', 0) < 100
    )

    # Layer 6: 데이터 분류
    defense.add_layer(
        "Data Classification",
        lambda ctx: ctx.get('user_clearance', 0) >= ctx.get('data_classification', 0)
    )

    return defense

# ============================================
# 5. 실패 안전 원칙 (Fail-safe Defaults)
# ============================================

class FailSafeDefaults:
    """
    실패 안전 원칙 구현
    - 기본값은 거부
    - 오류 시 안전한 상태
    - 명시적 허용만 적용
    """

    @staticmethod
    def firewall_rule(action: str, conditions: Dict) -> bool:
        """방화벽 규칙 (기본 거부)"""
        # 기본값은 거부
        if action != 'ALLOW':
            return False

        # 모든 조건이 충족해야 허용
        required = ['source', 'destination', 'port', 'protocol']
        for req in required:
            if req not in conditions:
                return False

        return True

    @staticmethod
    def access_check(user: User, resource: Resource, permission: Permission) -> bool:
        """접근 확인 (기본 거부)"""
        # 명시적 허용이 없으면 거부
        # 실제로는 DB 조회 등
        return False  # 기본 거부

    @staticmethod
    def error_handler(func):
        """오류 발생 시 안전한 기본값 반환"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # 오류 발생 시 안전하게 거부
                print(f"Error in {func.__name__}: {e}")
                return False
        return wrapper

# ============================================
# 6. 완전 중재 원칙 (Complete Mediation)
# ============================================

class CompleteMediation:
    """
    완전 중재 원칙 구현
    - 모든 접근 시 권한 확인
    - 캐시된 권한 신뢰 금지
    - 세션 무효화 시 즉시 적용
    """

    def __init__(self):
        self.permission_checker = LeastPrivilegeEnforcer()
        self.revoked_sessions: Set[str] = set()

    def mediate_access(self,
                      user: User,
                      session_id: str,
                      resource_id: str,
                      permission: Permission) -> tuple[bool, str]:
        """모든 접근 중재"""
        # 1. 세션 유효성 확인
        if session_id in self.revoked_sessions:
            return False, "Session revoked"

        # 2. 권한 확인 (매번)
        if not self.permission_checker.check_permission(user, resource_id, permission):
            return False, "Permission denied"

        # 3. 접근 로깅
        self._log_access(user, resource_id, permission)

        return True, "Access granted"

    def revoke_session(self, session_id: str):
        """세션 즉시 무효화"""
        self.revoked_sessions.add(session_id)

    def _log_access(self, user: User, resource_id: str, permission: Permission):
        """접근 로깅"""
        from datetime import datetime
        print(f"[{datetime.now()}] {user.name} accessed {resource_id} with {permission.value}")

# ============================================
# 통합 보안 원칙 관리자
# ============================================

class SecurityPrinciplesManager:
    """
    모든 보안 원칙을 통합 관리
    """

    def __init__(self):
        self.least_privilege = LeastPrivilegeEnforcer()
        self.separation_of_duties = SeparationOfDutiesEnforcer()
        self.need_to_know = NeedToKnowEnforcer()
        self.defense_in_depth = create_security_stack()
        self.complete_mediation = CompleteMediation()

    def evaluate_access_request(self,
                                user: User,
                                session_id: str,
                                resource: Resource,
                                permission: Permission,
                                context: Dict = None) -> Dict:
        """
        모든 원칙을 적용한 접근 평가
        """
        result = {
            'allowed': True,
            'violations': [],
            'warnings': []
        }

        # 1. 완전 중재
        allowed, msg = self.complete_mediation.mediate_access(
            user, session_id, resource.id, permission
        )
        if not allowed:
            result['allowed'] = False
            result['violations'].append(f"Complete Mediation: {msg}")

        # 2. 최소 권한
        if not self.least_privilege.check_permission(user, resource.id, permission):
            result['allowed'] = False
            result['violations'].append("Least Privilege: Insufficient permissions")

        # 3. 알 필요성
        allowed, msg = self.need_to_know.check_access(
            user, resource, context.get('justification') if context else None
        )
        if not allowed:
            result['allowed'] = False
            result['violations'].append(f"Need to Know: {msg}")

        # 4. 심층 방어
        if context:
            allowed, failed = self.defense_in_depth.check_all_layers(context)
            if not allowed:
                result['warnings'].extend([f"Defense in Depth: {f}" for f in failed])

        return result

# 사용 예시
if __name__ == "__main__":
    # 사용자 생성
    user = User(
        id="user001",
        name="John Doe",
        roles={'editor'},
        clearances={DataClassification.INTERNAL, DataClassification.CONFIDENTIAL}
    )

    # 리소스 생성
    resource = Resource(
        id="doc001",
        name="Financial Report",
        classification=DataClassification.CONFIDENTIAL,
        owner_id="user002"
    )

    # 보안 원칙 관리자
    security = SecurityPrinciplesManager()

    # 접근 평가
    result = security.evaluate_access_request(
        user=user,
        session_id="session123",
        resource=resource,
        permission=Permission.READ,
        context={
            'justification': 'Quarterly review',
            'authenticated': True,
            'authorized': True,
            'source_ip': '192.168.1.100',
            'blocked_ips': ['10.0.0.1'],
            'request_count': 5
        }
    )

    print("=== Security Principles Evaluation ===")
    print(f"Allowed: {result['allowed']}")
    if result['violations']:
        print("Violations:")
        for v in result['violations']:
            print(f"  - {v}")
    if result['warnings']:
        print("Warnings:")
        for w in result['warnings']:
            print(f"  - {w}")
