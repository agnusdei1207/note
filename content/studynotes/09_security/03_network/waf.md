+++
title = "WAF (Web Application Firewall)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# WAF (Web Application Firewall)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 웹 애플리케이션 계층(HTTP/HTTPS)에서 동작하여 OWASP Top 10(SQL Injection, XSS, CSRF 등)을 비롯한 웹 공격을 탐지/차단하는 전문 보안 장비로, Layer 7까지의 심층 검사를 수행합니다.
> 2. **가치**: "가상 패치"로 취약한 애플리케이션을 수정 없이 보호하며, PCI DSS 6.6 요구사항 충족, 봇/스크레이퍼 방어, API 보안까지 확장됩니다.
> 3. **융합**: NGOWASP Core Rule Set, Machine Learning 기반 탐지, RASP와 결합한 런타임 보호, CDN/WAF 통합 서비스로 진화합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**WAF(Web Application Firewall)**는 HTTP/HTTPS 트래픽을 검사하여 웹 애플리케이션 공격을 방어하는 보안 솔루션입니다. 방화벽(L3/L4)과 달리 애플리케이션 계층(L7)의 내용까지 분석합니다.

```
WAF 핵심 기능:
1. 웹 공격 방어: SQL Injection, XSS, CSRF, LFI/RFI, Command Injection
2. 봇/스크레이퍼 방어: 자동화 공격, 크롤러, 스캐너 차단
3. DDoS 완화: HTTP Flood, Slowloris 방어
4. 가상 패치: 앱 수정 없이 취약점 보호
5. 규정 준수: PCI DSS 6.6, GDPR
```

#### 2. 비유를 통한 이해
WAF는 **'은행 창구 보안요원'**에 비유할 수 있습니다.

- **방화벽(L3/L4)**: 은행 입구 경비원 (신분증만 확인)
- **WAF(L7)**: 창구 직원
  - 서류 내용 확인 (요청 본문 분석)
  - 이상한 요청 거부 (공격 패턴 탐지)
  - 의심스러운 행동 보고 (로그/알림)

#### 3. 등장 배경 및 발전 과정
1. **1998년**: Code Red, Nimda 웜 - 방화벽 무력화
2. **2003년**: OWASP 설립
3. **2004년**: ModSecurity 오픈소스 WAF
4. **2005년**: Breach Security (이후 Trustwave)
5. **2008년**: PCI DSS 6.6 - WAF 또는 코드 리뷰 필수
6. **2010년**: Imperva, F5, Citrix WAF 상용화
7. **2015년**: Cloud WAF (Cloudflare, Akamai)
8. **2020년**: API 보안, ML 기반 탐지 통합

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. WAF 배치 아키텍처

| 배치 방식 | 장점 | 단점 | 적용 |
|:---|:---|:---|:---|
| **Inline (Bridge)** | 즉시 차단 | SPOF, 성능 영향 | 온프레미스 |
| **Reverse Proxy** | 캐싱, SSL 오프로드 | 복잡성 | 엔터프라이즈 |
| **Out-of-Band** | 성능 영향 없음 | 차단 불가 (탐지만) | 모니터링 |
| **Cloud WAF** | 쉬운 배포, DDoS | 지연, 제어권 | SaaS |

#### 2. WAF 아키텍처 다이어그램

```
=== WAF 배포 아키텍처 (Reverse Proxy) ===

                      [ Internet ]
                           │
                           ▼
        ┌──────────────────────────────────────────┐
        │                WAF Cluster               │
        │                                          │
        │  ┌────────────────────────────────────┐  │
        │  │        SSL Termination             │  │
        │  │    (인증서 관리, 오프로딩)          │  │
        │  └────────────────────────────────────┘  │
        │                    │                     │
        │  ┌────────────────────────────────────┐  │
        │  │       Request Inspection           │  │
        │  │                                    │  │
        │  │  ┌──────────┐  ┌──────────┐       │  │
        │  │  │  URL     │  │  Header  │       │  │
        │  │  │  Decode  │  │  Analysis│       │  │
        │  │  └──────────┘  └──────────┘       │  │
        │  │                                    │  │
        │  │  ┌──────────┐  ┌──────────┐       │  │
        │  │  │  Body    │  │  Cookie  │       │  │
        │  │  │  Parse   │  │  Check   │       │  │
        │  │  └──────────┘  └──────────┘       │  │
        │  │                                    │  │
        │  └────────────────────────────────────┘  │
        │                    │                     │
        │  ┌────────────────────────────────────┐  │
        │  │      Rule Engine (Policy Match)    │  │
        │  │                                    │  │
        │  │  ┌────────────────────────────────┐│  │
        │  │  │   OWASP Core Rule Set (CRS)    ││  │
        │  │  │                                ││  │
        │  │  │   - SQL Injection Rules        ││  │
        │  │  │   - XSS Rules                  ││  │
        │  │  │   - LFI/RFI Rules              ││  │
        │  │  │   - RCE Rules                  ││  │
        │  │  │   - Session Fixation           ││  │
        │  │  │   - Scanner Detection          ││  │
        │  │  └────────────────────────────────┘│  │
        │  │                                    │  │
        │  │  ┌────────────────────────────────┐│  │
        │  │  │   Custom Rules                 ││  │
        │  │  │   - IP Whitelist/Blacklist     ││  │
        │  │  │   - Geo-blocking               ││  │
        │  │  │   - Rate Limiting              ││  │
        │  │  │   - Bot Detection              ││  │
        │  │  └────────────────────────────────┘│  │
        │  │                                    │  │
        │  └────────────────────────────────────┘  │
        │                    │                     │
        │  ┌────────────────────────────────────┐  │
        │  │         Action Execution           │  │
        │  │                                    │  │
        │  │   ┌────────┐ ┌────────┐ ┌───────┐ │  │
        │  │   │ BLOCK  │ │ ALLOW  │ │  LOG  │ │  │
        │  │   └────────┘ └────────┘ └───────┘ │  │
        │  │                                    │  │
        │  └────────────────────────────────────┘  │
        │                                          │
        └──────────────────────┬───────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │  Web Application │
                    │     Server       │
                    └──────────────────┘

===========================================

=== OWASP ModSecurity Rule 구조 ===

SecRule VARIABLES OPERATOR [ACTIONS]

예시: SQL Injection 탐지

SecRule REQUEST_URI|REQUEST_BODY "@rx (?i:union.*select|select.*from|insert.*into|delete.*from)" \
    "id:1001,phase:2,deny,status:403,msg:'SQL Injection Detected'"

구성 요소:
- VARIABLES: 검사 대상 (REQUEST_URI, REQUEST_BODY, ARGS...)
- OPERATOR: 매칭 방법 (@rx 정규식, @pm 병렬 매칭, @validateByteRange...)
- ACTIONS: 처리 방법 (deny, allow, log, pass...)

5단계 처리 (Phase):
1. Request Headers (phase:1)
2. Request Body (phase:2)
3. Response Headers (phase:3)
4. Response Body (phase:4)
5. Logging (phase:5)
```

#### 3. 심층 동작 원리: WAF 규칙 엔진

```python
"""
WAF Rule Engine 구현
OWASP CRS 기반
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Set
from enum import Enum
import re

class ActionType(Enum):
    ALLOW = "allow"
    DENY = "deny"
    BLOCK = "block"
    LOG = "log"
    PASS = "pass"

class Phase(Enum):
    REQUEST_HEADERS = 1
    REQUEST_BODY = 2
    RESPONSE_HEADERS = 3
    RESPONSE_BODY = 4
    LOGGING = 5

@dataclass
class HTTPRequest:
    """HTTP 요청 구조"""
    method: str
    uri: str
    version: str
    headers: Dict[str, str]
    cookies: Dict[str, str]
    body: bytes
    query_string: str
    remote_addr: str

    @property
    def args(self) -> Dict[str, str]:
        """쿼리 파라미터"""
        params = {}
        if self.query_string:
            for pair in self.query_string.split('&'):
                if '=' in pair:
                    k, v = pair.split('=', 1)
                    params[k] = v
        return params

    @property
    def all_input(self) -> str:
        """모든 입력값 결합"""
        inputs = []
        inputs.append(self.uri)
        inputs.append(self.query_string)
        inputs.extend(self.headers.values())
        inputs.extend(self.cookies.values())
        if self.body:
            inputs.append(self.body.decode('utf-8', errors='ignore'))
        return ' '.join(inputs)


@dataclass
class WAFRule:
    """WAF 규칙 정의"""
    rule_id: str
    phase: Phase
    variables: List[str]  # 검사 대상
    operator: str  # @rx, @pm, @eq, etc.
    pattern: str  # 정규식 또는 패턴
    action: ActionType
    msg: str
    severity: str  # CRITICAL, ERROR, WARNING, NOTICE
    tag: List[str]
    status_code: int = 403

    def match(self, request: HTTPRequest) -> bool:
        """규칙 매칭"""
        # 검사 대상 값 수집
        target_values = self._get_target_values(request)

        for value in target_values:
            if self._operator_match(value):
                return True
        return False

    def _get_target_values(self, request: HTTPRequest) -> List[str]:
        """변수에서 값 추출"""
        values = []
        for var in self.variables:
            if var == "REQUEST_URI":
                values.append(request.uri)
            elif var == "REQUEST_BODY":
                values.append(request.body.decode('utf-8', errors='ignore'))
            elif var == "ARGS":
                values.extend(request.args.values())
            elif var == "HEADERS":
                values.extend(request.headers.values())
            elif var == "COOKIES":
                values.extend(request.cookies.values())
            elif var == "REMOTE_ADDR":
                values.append(request.remote_addr)
        return values

    def _operator_match(self, value: str) -> bool:
        """연산자 매칭"""
        if self.operator == "@rx":
            # 정규식 매칭 (대소문자 무시)
            return bool(re.search(self.pattern, value, re.IGNORECASE))
        elif self.operator == "@pm":
            # 병렬 매칭 (여러 문자열)
            patterns = self.pattern.split(' ')
            return any(p.lower() in value.lower() for p in patterns)
        elif self.operator == "@eq":
            return value == self.pattern
        elif self.operator == "@contains":
            return self.pattern in value
        elif self.operator == "@beginsWith":
            return value.startswith(self.pattern)
        return False


class OWASPCoreRuleSet:
    """
    OWASP ModSecurity Core Rule Set (CRS)

    주요 규칙 카테고리:
    - 9xx: Generic Attacks
    - 941xxx: XSS
    - 942xxx: SQL Injection
    - 943xxx: Session Fixation
    - 944xxx: Java Attacks
    """

    @staticmethod
    def get_sql_injection_rules() -> List[WAFRule]:
        """SQL Injection 탐지 규칙"""
        return [
            WAFRule(
                rule_id="942100",
                phase=Phase.REQUEST_BODY,
                variables=["REQUEST_URI", "ARGS", "REQUEST_BODY"],
                operator="@rx",
                pattern=r"(?i)(union\s+(all\s+)?select|select\s+.*\s+from|insert\s+into|delete\s+from|drop\s+(table|database)|update\s+.*\s+set)",
                action=ActionType.DENY,
                msg="SQL Injection Attack Detected",
                severity="CRITICAL",
                tag=["OWASP_CRS", "SQL_INJECTION"]
            ),
            WAFRule(
                rule_id="942110",
                phase=Phase.REQUEST_BODY,
                variables=["ARGS", "REQUEST_BODY"],
                operator="@rx",
                pattern=r"(?i)(or\s+1\s*=\s*1|or\s+'1'\s*=\s*'1'|or\s+\"1\"\s*=\s*\"1\")",
                action=ActionType.DENY,
                msg="SQL Injection: Always True Condition",
                severity="CRITICAL",
                tag=["OWASP_CRS", "SQL_INJECTION"]
            ),
            WAFRule(
                rule_id="942120",
                phase=Phase.REQUEST_BODY,
                variables=["ARGS", "REQUEST_BODY"],
                operator="@rx",
                pattern=r"(?i)(--\s|;\s*--|\/\*|\*\/|#\s)",
                action=ActionType.DENY,
                msg="SQL Comment Sequence Detected",
                severity="ERROR",
                tag=["OWASP_CRS", "SQL_INJECTION"]
            ),
        ]

    @staticmethod
    def get_xss_rules() -> List[WAFRule]:
        """XSS 탐지 규칙"""
        return [
            WAFRule(
                rule_id="941100",
                phase=Phase.REQUEST_BODY,
                variables=["REQUEST_URI", "ARGS", "REQUEST_BODY"],
                operator="@rx",
                pattern=r"(?i)<\s*script[^>]*>.*?<\s*/\s*script\s*>",
                action=ActionType.DENY,
                msg="XSS Attack: Script Tag Detected",
                severity="CRITICAL",
                tag=["OWASP_CRS", "XSS"]
            ),
            WAFRule(
                rule_id="941110",
                phase=Phase.REQUEST_BODY,
                variables=["REQUEST_URI", "ARGS", "REQUEST_BODY"],
                operator="@rx",
                pattern=r"(?i)(javascript\s*:|on(load|error|click|mouse\w+|focus|blur)\s*=)",
                action=ActionType.DENY,
                msg="XSS Attack: JavaScript Event Handler",
                severity="CRITICAL",
                tag=["OWASP_CRS", "XSS"]
            ),
            WAFRule(
                rule_id="941120",
                phase=Phase.REQUEST_BODY,
                variables=["ARGS", "REQUEST_BODY"],
                operator="@rx",
                pattern=r"(?i)(<\s*img[^>]+src\s*=|<\s*iframe|<\s*object|<\s*embed)",
                action=ActionType.DENY,
                msg="XSS Attack: Dangerous HTML Tag",
                severity="ERROR",
                tag=["OWASP_CRS", "XSS"]
            ),
        ]

    @staticmethod
    def get_lfi_rfi_rules() -> List[WAFRule]:
        """LFI/RFI 탐지 규칙"""
        return [
            WAFRule(
                rule_id="930100",
                phase=Phase.REQUEST_BODY,
                variables=["REQUEST_URI", "ARGS"],
                operator="@rx",
                pattern=r"(\.\.\/|\.\.\\|%2e%2e%2f|%2e%2e\/)",
                action=ActionType.DENY,
                msg="Path Traversal Attack",
                severity="CRITICAL",
                tag=["OWASP_CRS", "LFI"]
            ),
            WAFRule(
                rule_id="930110",
                phase=Phase.REQUEST_BODY,
                variables=["ARGS"],
                operator="@rx",
                pattern=r"(?i)(^(file|php|data|expect|zip|phar)://|\|\s*\w+)",
                action=ActionType.DENY,
                msg="RFI Attack: Remote File Inclusion",
                severity="CRITICAL",
                tag=["OWASP_CRS", "RFI"]
            ),
        ]

    @staticmethod
    def get_command_injection_rules() -> List[WAFRule]:
        """Command Injection 탐지 규칙"""
        return [
            WAFRule(
                rule_id="932100",
                phase=Phase.REQUEST_BODY,
                variables=["ARGS", "REQUEST_BODY"],
                operator="@rx",
                pattern=r"(?i)(;\s*(ls|cat|rm|wget|curl|nc|bash|sh|python|perl|ruby)\s|`[^`]+`|\$\([^)]+\))",
                action=ActionType.DENY,
                msg="Remote Command Execution",
                severity="CRITICAL",
                tag=["OWASP_CRS", "RCE"]
            ),
            WAFRule(
                rule_id="932110",
                phase=Phase.REQUEST_BODY,
                variables=["ARGS", "REQUEST_BODY"],
                operator="@rx",
                pattern=r"(?i)(\|\s*\w+|&&\s*\w+|\|\|\s*\w+)",
                action=ActionType.DENY,
                msg="Command Injection: Pipe/Chain Operator",
                severity="ERROR",
                tag=["OWASP_CRS", "RCE"]
            ),
        ]


class WAFEngine:
    """
    WAF 엔진

    요청 처리 흐름:
    1. Phase 1: Request Headers 검사
    2. Phase 2: Request Body 검사
    3. 규칙 매칭 → Action 실행
    """

    def __init__(self):
        self.rules: List[WAFRule] = []
        self.whitelist_ips: Set[str] = set()
        self.blacklist_ips: Set[str] = set()
        self.rate_limits: Dict[str, int] = {}
        self.request_counts: Dict[str, List[float]] = {}

        # 기본 규칙 로드
        self._load_default_rules()

    def _load_default_rules(self):
        """OWASP CRS 로드"""
        self.rules.extend(OWASPCoreRuleSet.get_sql_injection_rules())
        self.rules.extend(OWASPCoreRuleSet.get_xss_rules())
        self.rules.extend(OWASPCoreRuleSet.get_lfi_rfi_rules())
        self.rules.extend(OWASPCoreRuleSet.get_command_injection_rules())

    def inspect(self, request: HTTPRequest) -> dict:
        """
        요청 검사

        Returns:
            {
                'action': 'allow' | 'deny',
                'matched_rule': WAFRule or None,
                'log': list
            }
        """
        result = {
            'action': 'allow',
            'matched_rule': None,
            'log': []
        }

        # 0. IP 화이트리스트 확인
        if request.remote_addr in self.whitelist_ips:
            result['log'].append(f"IP {request.remote_addr} whitelisted")
            return result

        # 0. IP 블랙리스트 확인
        if request.remote_addr in self.blacklist_ips:
            result['action'] = 'deny'
            result['log'].append(f"IP {request.remote_addr} blacklisted")
            return result

        # 1. Rate Limiting
        if self._check_rate_limit(request):
            result['action'] = 'deny'
            result['log'].append("Rate limit exceeded")
            return result

        # 2. Phase별 규칙 검사
        for phase in [Phase.REQUEST_HEADERS, Phase.REQUEST_BODY]:
            phase_rules = [r for r in self.rules if r.phase == phase]

            for rule in phase_rules:
                if rule.match(request):
                    result['action'] = rule.action.value
                    result['matched_rule'] = rule
                    result['log'].append(
                        f"Rule {rule.rule_id} matched: {rule.msg}"
                    )

                    if rule.action == ActionType.DENY:
                        return result

        return result

    def _check_rate_limit(self, request: HTTPRequest) -> bool:
        """Rate limiting 검사"""
        import time

        ip = request.remote_addr
        current_time = time.time()

        if ip not in self.request_counts:
            self.request_counts[ip] = []

        # 최근 1분간 요청 수 계산
        self.request_counts[ip] = [
            t for t in self.request_counts[ip]
            if current_time - t < 60
        ]
        self.request_counts[ip].append(current_time)

        limit = self.rate_limits.get('default', 100)
        return len(self.request_counts[ip]) > limit

    def add_custom_rule(self, rule: WAFRule):
        """커스텀 규칙 추가"""
        self.rules.append(rule)

    def whitelist_ip(self, ip: str):
        """IP 화이트리스트 추가"""
        self.whitelist_ips.add(ip)

    def blacklist_ip(self, ip: str):
        """IP 블랙리스트 추가"""
        self.blacklist_ips.add(ip)


# 사용 예시
def waf_demo():
    """WAF 동작 데모"""

    print("=" * 60)
    print("WAF (Web Application Firewall) 데모")
    print("=" * 60)

    waf = WAFEngine()

    # 테스트 요청들
    test_requests = [
        # 정상 요청
        HTTPRequest(
            method="GET",
            uri="/api/users",
            version="HTTP/1.1",
            headers={"Host": "example.com"},
            cookies={},
            body=b"",
            query_string="page=1",
            remote_addr="192.168.1.100"
        ),
        # SQL Injection 시도
        HTTPRequest(
            method="GET",
            uri="/api/users",
            version="HTTP/1.1",
            headers={"Host": "example.com"},
            cookies={},
            body=b"",
            query_string="id=1' OR '1'='1",
            remote_addr="192.168.1.101"
        ),
        # XSS 시도
        HTTPRequest(
            method="POST",
            uri="/api/comments",
            version="HTTP/1.1",
            headers={"Host": "example.com", "Content-Type": "application/x-www-form-urlencoded"},
            cookies={},
            body=b"comment=<script>alert('XSS')</script>",
            query_string="",
            remote_addr="192.168.1.102"
        ),
        # Path Traversal 시도
        HTTPRequest(
            method="GET",
            uri="/files/../../../etc/passwd",
            version="HTTP/1.1",
            headers={"Host": "example.com"},
            cookies={},
            body=b"",
            query_string="",
            remote_addr="192.168.1.103"
        ),
    ]

    for i, request in enumerate(test_requests, 1):
        print(f"\n[요청 {i}]")
        print(f"  Method: {request.method}")
        print(f"  URI: {request.uri}")
        print(f"  Query: {request.query_string}")
        print(f"  Body: {request.body[:50] if request.body else '(empty)'}")

        result = waf.inspect(request)

        print(f"\n[결과]")
        print(f"  Action: {result['action'].upper()}")
        if result['matched_rule']:
            print(f"  Rule: {result['matched_rule'].rule_id}")
            print(f"  Message: {result['matched_rule'].msg}")
            print(f"  Severity: {result['matched_rule'].severity}")
        for log in result['log']:
            print(f"  Log: {log}")


if __name__ == "__main__":
    waf_demo()
```

#### 4. WAF 벤더 및 제품 비교

| 범주 | 벤더 | 제품 | 특징 |
|:---|:---|:---|:---|
| **어플라이언스** | Imperva | SecureSphere | 엔터프라이즈 표준 |
| | F5 | BIG-IP ASM | L7/LB 통합 |
| | Fortinet | FortiWeb | 가성비 |
| **소프트웨어** | Trustwave | ModSecurity | 오픈소스 |
| | Nginx | Nginx App Protect | 컨테이너 친화 |
| **클라우드** | Cloudflare | WAF | CDN 통합 |
| | AWS | WAF | ALB/CloudFront |
| | Azure | WAF | Application Gateway |

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. WAF vs NGFW vs IPS 비교

| 특성 | WAF | NGFW (L7) | IPS |
|:---|:---|:---|:---|
| **계층** | L7 (HTTP/HTTPS) | L3-L7 | L3-L7 |
| **특화** | 웹 공격 | 네트워크 전체 | 네트워크 공격 |
| **SQL Injection** | 최적 | 지원 | 제한적 |
| **XSS** | 최적 | 지원 | 제한적 |
| **세밀한 규칙** | O | △ | X |
| **가상 패치** | O | O | O |

#### 2. 과목 융합 관점

**애플리케이션 보안과 융합**
- RASP: 런타임 보호
- SAST/DAST: 개발 단계 보안
- SCA: 라이브러리 취약점

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: PCI DSS 6.6 준수**
- 요구: WAF 또는 코드 리뷰
- 판단: Cloud WAF (신속 배포)
- 설정: OWASP CRS + 커스텀 규칙

**시나리오 2: 레거시 앱 보호**
- 상황: 더 이상 패치되지 않는 앱
- 판단: WAF "가상 패치"
- 전략: 취약점별 세부 규칙 작성

#### 2. 안티패턴 (Anti-patterns)

```
취약한 구현 (금지!)

1. WAF 없이 운영
   ❌ 방화벽만 사용
   → SQL Injection, XSS 무방비

2. 기본 설정만 사용
   ❌ OWASP CRS 기본만 적용
   → False Positive/False Negative

3. 로그만 (차단 안 함)
   ❌ SecDefaultAction "pass,log"
   → 공격 허용, 탐지만

올바른 구현:

1. WAF 필수 배포
   ✓ Cloud WAF 또는 전용 장비

2. 튜닝 필수
   ✓ False Positive 제거
   ✓ 앱별 커스텀 규칙

3. 차단 모드
   ✓ SecDefaultAction "deny,log,status:403"
```

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 | 항목 | 수치/내용 |
|:---|:---|:---|
| **OWASP Top 10** | 방지 | 90%+ 공격 차단 |
| **가상 패치** | 대응 시간 | 0-day 대응: 시간 |
| **PCI DSS** | 준수 | 6.6 요구사항 |

#### 2. 참고 표준/가이드

| 표준 | 내용 |
|:---|:---|
| **OWASP CRS** | Core Rule Set v4.0 |
| **PCI DSS 6.6** | WAF 또는 코드 리뷰 |
| **NIST SP 800-53** | SC-7, SI-4 |

---

### 관련 개념 맵 (Knowledge Graph)
- [OWASP Top 10](@/studynotes/09_security/05_web/owasp_top10.md) : WAF 방어 대상
- [SQL Injection](@/studynotes/09_security/05_web/sql_injection.md) : WAF 주요 탐지
- [XSS](@/studynotes/09_security/05_web/xss.md) : WAF 주요 탐지
- [NGFW](@/studynotes/09_security/03_network/ngfw.md) : 네트워크 방화벽
- [RASP](@/studynotes/09_security/05_web/rasp.md) : 런타임 보호

---

### 어린이를 위한 3줄 비유 설명
1. **문지기 선생님**: WAF는 학교 앞에서 아이들의 가방을 검사하는 문지기 선생님이에요. 위험한 물건이 들어있는지 꼼꼼히 확인하죠.
2. **위험한 단어**: "비밀번호 알려줘" 같은 위험한 말이 적힌 쪽지는 빼앗아요. 나쁜 사람들이 학교 컴퓨터에 몰래 들어오지 못하게요.
3. **가상 울타리**: 학교 건물을 고치지 않아도, 문지기가 지켜주면 안전해요. 이게 바로 '가상 패치'예요!
