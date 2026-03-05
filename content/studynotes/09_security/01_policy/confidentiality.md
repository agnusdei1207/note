+++
title = "기밀성 (Confidentiality)"
date = "2026-03-04"
[extra]
categories = "studynotes-09_security"
+++

# 기밀성 (Confidentiality)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인가된 사용자만이 정보에 접근할 수 있도록 보장하는 정보보안의 핵심 속성으로, 데이터의 민감도에 따라 다층적 보호 체계를 적용하는 근본적 보안 원칙입니다.
> 2. **가치**: 기업의 영업비밀, 개인정보, 국가기밀 등 핵심 자산을 보호하여 경쟁력 유지, 법적 컴플라이언스 충족, 신뢰 관계 구축을 실현합니다.
> 3. **융합**: 암호화 기술, 접근제어 시스템, DLP, DRM 등 다양한 보안 기술이 통합된 다층 방어 체계의 핵심 목표입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**기밀성(Confidentiality)**은 정보가 인가되지 않은 개인, 프로세스, 또는 시스템에게 공개되거나 사용되는 것을 방지하는 보안 속성입니다. 이는 단순히 데이터를 "숨기는 것"을 넘어, 데이터의 수명 주기 전반(생성, 저장, 전송, 처리, 폐기)에 걸쳐 체계적인 보호 메커니즘을 적용하는 포괄적 개념입니다.

**정보보안 표준(ISO 27000) 정의**:
> "정보에 대한 접근 및 공개가 인가된 개체에게만 허용되는 특성"

#### 2. 💡 비유를 통한 이해
기밀성은 **'다층 보안 금고'**에 비유할 수 있습니다.
- **외부 금고**: 건물 입구의 보안초소 - 외부인의 무단 출입 차단
- **내부 금고**: 부서별 출입카드 - 부서원 외 출입 제한
- **개별 금고**: 개인 캐비닛 - 본인만 열쇠 보유
- **이중 잠금 장치**: 중요 문서함 - 두 사람의 열쇠 동시 필요

#### 3. 등장 배경 및 발전 과정
1. **고대 암호학의 시작**: 카이사르 암호(BC 50년) 등 군사 기밀 보호 목적
2. **현대적 기밀성 개념**: 1970년대 컴퓨터 보안 연구와 함께 체계화
3. **Bell-LaPadula 모델 (1973)**: 최초의 수학적 기밀성 모델 - "No Read Up, No Write Down"
4. **디지털 시대의 도전**: 클라우드, 모바일, IoT로 인한 경계 붕괴
5. **현대적 접근**: Zero Trust, 데이터 중심 보안으로 진화

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 기밀성 보호 기술 체계 (표)

| 계층 | 기술명 | 상세 역할 | 구현 메커니즘 | 적용 시나리오 |
|:---|:---|:---|:---|:---|
| **데이터 계층** | 저장 암호화 | 저장된 데이터 보호 | AES-256, TDE, FDE | DB, 파일시스템 |
| **전송 계층** | 전송 암호화 | 이동 중 데이터 보호 | TLS 1.3, IPsec, WireGuard | 네트워크 통신 |
| **처리 계층** | 동형 암호 | 연산 중 데이터 보호 | HE, TEE (SGX/SEV) | 클라우드 연산 |
| **접근 계층** | 접근 통제 | 인가된 사용자만 접근 | RBAC, ABAC, PBAC | 시스템 접근 |
| **출력 계층** | DLP | 데이터 유출 방지 | 콘텐츠 검사, 정책 차단 | 이메일, USB |
| **사용 계층** | DRM | 사용 권한 관리 | 권한 정책, 워터마크 | 문서, 미디어 |

#### 2. 기밀성 보호 아키텍처 다이어그램

```text
<<< Defense-in-Depth Confidentiality Architecture >>>

+------------------------------------------------------------------+
|                    사용자/프로세스 계층                            |
|  +----------+  +----------+  +----------+  +----------+           |
|  |  사용자  |  |  애플리  |  |  서비스  |  |   IoT    |           |
|  |  인증    |  |  케이션  |  |  계정    |  |  디바이스|           |
|  +----+-----+  +----+-----+  +----+-----+  +----+-----+           |
|       |             |             |             |                  |
+-------|-------------|-------------|-------------|------------------+
        |             |             |             |
        v             v             v             v
+------------------------------------------------------------------+
|                    접근 제어 계층 (Access Control)                 |
|  +----------------------------------------------------------+    |
|  |  Policy Decision Point (PDP)                              |    |
|  |  - Identity Verification (MFA, FIDO2)                    |    |
|  |  - Context Analysis (Time, Location, Device)             |    |
|  |  - Risk Scoring (UEBA, ML)                               |    |
|  +----------------------------------------------------------+    |
|                          |                                        |
|  +----------------------------------------------------------+    |
|  |  Policy Enforcement Point (PEP)                           |    |
|  |  - RBAC / ABAC / ReBAC                                   |    |
|  |  - Least Privilege Enforcement                           |    |
|  +----------------------------------------------------------+    |
+------------------------------------------------------------------+
                           |
                           v
+------------------------------------------------------------------+
|                    암호화 계층 (Encryption Layer)                  |
|                                                                   |
|  [전송 중]     TLS 1.3 / IPsec / WireGuard                       |
|       |           - PFS (Perfect Forward Secrecy)                 |
|       |           - AEAD (Authenticated Encryption)              |
|       v                                                          |
|  [저장 중]     AES-256-GCM / ChaCha20-Poly1305                   |
|       |           - Key Management (HSM/KMS)                     |
|       |           - Envelope Encryption                          |
|       v                                                          |
|  [사용 중]     Intel SGX / AMD SEV / Homomorphic Encryption      |
|                                                                   |
+------------------------------------------------------------------+
                           |
                           v
+------------------------------------------------------------------+
|                    데이터 계층 (Data Layer)                       |
|                                                                   |
|  +------------------+    +------------------+    +-------------+ |
|  |  구조화 데이터    |    |  비구조화 데이터  |    |  메타데이터  | |
|  |  (RDBMS)         |    |  (파일/객체)     |    |  (로그)     | |
|  |  - Column Enc    |    |  - File Enc      |    |  - Masking  | |
|  |  - TDE           |    |  - Bucket Enc    |    |  - Tokenization |
|  +------------------+    +------------------+    +-------------+ |
|                                                                   |
+------------------------------------------------------------------+
```

#### 3. 심층 동작 원리: 다층 기밀성 보호 프로세스

**① 데이터 분류 및 레이블링 (5단계)**
```
1. 데이터 발견 (Discovery)
   - 자동 스캔: 정규식, ML 기반 민감정보 식별
   - 메타데이터 수집: 소유자, 생성일, 위치

2. 분류 체계 적용 (Classification)
   - 공개 (Public): 외부 공개 가능
   - 내부 (Internal): 사내 제한
   - 기밀 (Confidential): 부서별 제한
   - 극비 (Top Secret): 최고 경영진만 접근

3. 레이블링 (Labeling)
   - 메타데이터 태그 삽입
   - 시각적 마킹 (워터마크, 헤더/푸터)
   - 암호학적 레이블 (전자서명)

4. 보호 정책 매핑 (Policy Mapping)
   - 분류별 암호화 강도 결정
   - 접근 권한 매트릭스 정의
   - DLP 규칙 설정

5. 지속적 모니터링 (Monitoring)
   - 접근 로그 수집
   - 이상 행동 탐지 (UEBA)
   - 정책 위반 알림
```

**② 암호화 키 관리 라이프사이클**

```python
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class ConfidentialityManager:
    """
    기밀성 보호를 위한 통합 암호화 관리 시스템
    - 데이터 분류 기반 암호화 정책 적용
    - 키 수명주기 관리
    - 안전한 키 교환 및 저장
    """

    # 데이터 분류별 암호화 정책
    ENCRYPTION_POLICIES = {
        'public': {'algorithm': None, 'key_size': 0},
        'internal': {'algorithm': 'AES-128-GCM', 'key_size': 128},
        'confidential': {'algorithm': 'AES-256-GCM', 'key_size': 256},
        'top_secret': {'algorithm': 'AES-256-GCM', 'key_size': 256, 'double_encryption': True}
    }

    def __init__(self, kms_endpoint: str):
        self.kms_endpoint = kms_endpoint
        self.key_cache: Dict[str, Dict[str, Any]] = {}

    def classify_data(self, data: bytes, metadata: Dict) -> str:
        """
        데이터 분류 수행
        - 패턴 매칭 및 ML 기반 민감도 분석
        """
        classification_score = 0

        # 패턴 기반 분석
        patterns = {
            'credit_card': rb'\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}',
            'ssn': rb'\d{3}-\d{2}-\d{4}',
            'email': rb'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        }

        import re
        for pattern_name, pattern in patterns.items():
            if re.search(pattern, data):
                classification_score += 30

        # 메타데이터 기반 분석
        if metadata.get('source') == 'hr_system':
            classification_score += 40
        if metadata.get('contains_pii', False):
            classification_score += 50

        # 분류 결정
        if classification_score >= 80:
            return 'top_secret'
        elif classification_score >= 50:
            return 'confidential'
        elif classification_score >= 20:
            return 'internal'
        return 'public'

    def encrypt_data(self,
                     plaintext: bytes,
                     classification: str,
                     key_id: Optional[str] = None) -> Dict[str, Any]:
        """
        분류 기반 데이터 암호화
        """
        policy = self.ENCRYPTION_POLICIES[classification]

        if policy['algorithm'] is None:
            return {
                'ciphertext': plaintext,
                'algorithm': 'none',
                'classification': classification
            }

        # 암호화 수행
        algorithm = policy['algorithm']
        key_size = policy['key_size']

        # 키 획득 또는 생성
        if key_id is None:
            key_id = self._generate_key_id(classification)
            key = self._generate_key(key_size)
            self._store_key(key_id, key, classification)
        else:
            key = self._retrieve_key(key_id)

        # AES-GCM 암호화
        nonce = os.urandom(12)  # 96-bit nonce for GCM
        aesgcm = AESGCM(key)

        # 인증 데이터에 분류 정보 포함
        aad = json.dumps({
            'classification': classification,
            'timestamp': datetime.utcnow().isoformat()
        }).encode()

        ciphertext = aesgcm.encrypt(nonce, plaintext, aad)

        result = {
            'ciphertext': ciphertext,
            'nonce': nonce,
            'aad': aad,
            'algorithm': algorithm,
            'key_id': key_id,
            'classification': classification,
            'encrypted_at': datetime.utcnow().isoformat()
        }

        # 이중 암호화 (Top Secret)
        if policy.get('double_encryption', False):
            result = self._apply_second_layer_encryption(result)

        return result

    def decrypt_data(self,
                     encrypted_package: Dict[str, Any],
                     requester_identity: Dict) -> bytes:
        """
        접근 제어 기반 데이터 복호화
        """
        classification = encrypted_package['classification']

        # 접근 권한 검증
        if not self._verify_access(requester_identity, classification):
            raise PermissionError(
                f"Access denied. User clearance level insufficient for {classification}"
            )

        # 이중 암호화 해제
        if encrypted_package.get('double_encrypted', False):
            encrypted_package = self._remove_second_layer(encrypted_package)

        # 키 검증 (키 만료, 폐기 확인)
        key_id = encrypted_package['key_id']
        if self._is_key_compromised(key_id):
            raise SecurityError("Key has been compromised. Decryption denied.")

        # 복호화 수행
        key = self._retrieve_key(key_id)
        aesgcm = AESGCM(key)

        plaintext = aesgcm.decrypt(
            encrypted_package['nonce'],
            encrypted_package['ciphertext'],
            encrypted_package['aad']
        )

        # 접근 로그 기록
        self._log_access(
            requester_identity,
            key_id,
            classification,
            'DECRYPT',
            'SUCCESS'
        )

        return plaintext

    def _generate_key(self, key_size: int) -> bytes:
        """암호학적으로 안전한 난수로 키 생성"""
        return os.urandom(key_size // 8)

    def _generate_key_id(self, classification: str) -> str:
        """고유 키 식별자 생성"""
        import uuid
        return f"{classification}-{uuid.uuid4()}"

    def _store_key(self, key_id: str, key: bytes, classification: str):
        """HSM/KMS에 키 안전 저장 (시뮬레이션)"""
        self.key_cache[key_id] = {
            'key': key,
            'classification': classification,
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(days=90),
            'rotation_count': 0
        }

    def _retrieve_key(self, key_id: str) -> bytes:
        """키 검색 및 만료 확인"""
        key_info = self.key_cache.get(key_id)
        if key_info is None:
            raise KeyError(f"Key {key_id} not found")

        if datetime.utcnow() > key_info['expires_at']:
            raise SecurityError("Key has expired")

        return key_info['key']

    def _verify_access(self, identity: Dict, classification: str) -> bool:
        """사용자 접근 권한 검증"""
        clearance_levels = {
            'public': 0,
            'internal': 1,
            'confidential': 2,
            'top_secret': 3
        }

        user_clearance = identity.get('clearance_level', 0)
        required_clearance = clearance_levels.get(classification, 0)

        return user_clearance >= required_clearance

    def _is_key_compromised(self, key_id: str) -> bool:
        """키 노출 여부 확인"""
        # 실제 구현에서는 HSM/KMS에서 상태 조회
        return False

    def _log_access(self, identity: Dict, key_id: str,
                    classification: str, operation: str, result: str):
        """접근 감사 로그 기록"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': identity.get('user_id'),
            'key_id': key_id,
            'classification': classification,
            'operation': operation,
            'result': result
        }
        # 실제 구현에서는 중앙 로깅 시스템으로 전송
        print(f"[AUDIT] {json.dumps(log_entry)}")

    def _apply_second_layer_encryption(self, package: Dict) -> Dict:
        """Top Secret 데이터 이중 암호화"""
        package['double_encrypted'] = True
        # 실제 구현에서는 별도 HSM 키로 재암호화
        return package

    def _remove_second_layer(self, package: Dict) -> Dict:
        """이중 암호화 해제"""
        package['double_encrypted'] = False
        return package


class SecurityError(Exception):
    """보안 관련 예외"""
    pass


# 사용 예시
if __name__ == "__main__":
    manager = ConfidentialityManager("kms://enterprise-hsm.local")

    # 데이터 분류 및 암호화
    sensitive_data = b"고객 주민등록번호: 900101-1234567, 신용카드: 1234-5678-9012-3456"
    metadata = {'source': 'customer_db', 'contains_pii': True}

    classification = manager.classify_data(sensitive_data, metadata)
    print(f"Data classified as: {classification}")

    encrypted = manager.encrypt_data(sensitive_data, classification)
    print(f"Encrypted with: {encrypted['algorithm']}")

    # 복호화 (권한 있는 사용자)
    authorized_user = {
        'user_id': 'admin001',
        'clearance_level': 3  # Top Secret
    }

    decrypted = manager.decrypt_data(encrypted, authorized_user)
    print(f"Decryption successful: {decrypted == sensitive_data}")
```

#### 4. Bell-LaPadula 모델 상세 분석

```text
<<< Bell-LaPadula 기밀성 모델 (BLP Model) >>>

                    보안 레벨 (Security Levels)
    ┌─────────────────────────────────────────────────────┐
    │  Level 4: TOP SECRET (TS)                           │
    │  Level 3: SECRET (S)                                │
    │  Level 2: CONFIDENTIAL (C)                          │
    │  Level 1: UNCLASSIFIED (U)                          │
    └─────────────────────────────────────────────────────┘

    핵심 속성 (Core Properties):

    1. Simple Security Property (No Read Up)
       ┌───────────────────────────────────────────┐
       │   Subject at level L can only read        │
       │   objects at level L or below             │
       │                                           │
       │   [Subject: C] ───READ──X── [Object: TS] │
       │   [Subject: C] ───READ──OK── [Object: C] │
       └───────────────────────────────────────────┘

    2. Star (*) Property (No Write Down)
       ┌───────────────────────────────────────────┐
       │   Subject at level L can only write       │
       │   to objects at level L or above          │
       │                                           │
       │   [Subject: TS] ───WRITE──X── [Object: C]│
       │   [Subject: TS] ───WRITE──OK── [Object: TS]│
       └───────────────────────────────────────────┘

    3. Strong Star Property (Optional)
       ┌───────────────────────────────────────────┐
       │   Subject can only read/write at same level│
       │                                           │
       │   [Subject: S] ───R/W──OK── [Object: S]   │
       └───────────────────────────────────────────┘

    실제 적용 예시 (Military System):

    +-------------------+     +-------------------+
    | General (TS)      │     | TOP SECRET Docs   │
    | - Read: TS,S,C,U  │◄────│ Nuclear Codes     │
    | - Write: TS       │────►│ Spy Identities    │
    +-------------------+     +-------------------+
              │
              │ Cannot read
              v
    +-------------------+     +-------------------+
    | Colonel (S)       │     | SECRET Docs       │
    | - Read: S,C,U     │◄────│ Troop Movements   │
    | - Write: S,TS     │────►│ Battle Plans      │
    +-------------------+     +-------------------+
              │
              │ Cannot read
              v
    +-------------------+     +-------------------+
    | Private (C)       │     | CONFIDENTIAL Docs │
    | - Read: C,U       │◄────│ Personnel Records │
    | - Write: C,S,TS   │────►│ Training Schedules│
    +-------------------+     +-------------------+
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 암호화 알고리즘별 기밀성 보장 비교

| 알고리즘 | 키 길이 | 보안 강도 | 성능 | 용도 | 권장 등급 |
|:---|:---|:---|:---|:---|:---|
| **AES-256-GCM** | 256-bit | 매우 높음 | 빠름 | 일반 데이터 | ★★★★★ |
| **ChaCha20-Poly1305** | 256-bit | 매우 높음 | 매우 빠름 | 모바일/IoT | ★★★★★ |
| **RSA-4096** | 4096-bit | 높음 | 느림 | 키 교환 | ★★★★☆ |
| **ECDH P-384** | 384-bit | 높음 | 중간 | TLS 키 교환 | ★★★★★ |
| **AES-128-GCM** | 128-bit | 높음 | 매우 빠름 | 실시간 스트림 | ★★★★☆ |
| **3DES** | 168-bit | 낮음 | 느림 | 레거시만 | ★★☆☆☆ |

#### 2. 기밀성 보호 기술 비교

| 기술 | 보호 범위 | 장점 | 단점 | 적용 시나리오 |
|:---|:---|:---|:---|:---|
| **저장 암호화 (FDE)** | 디스크 전체 | 투명, 단순 | 분실 시 무력 | 노트북, 모바일 |
| **저장 암호화 (TDE)** | DB 파일 | DB 투명 | DBA 접근 가능 | 엔터프라이즈 DB |
| **컬럼 암호화** | 특정 컬럼 | 세밀한 제어 | 성능 오버헤드 | 민감 컬럼만 |
| **애플리케이션 암호화** | 앱 레벨 | End-to-End | 구현 복잡 | 최고 보안 요구 |
| **DRM** | 문서 사용 | 권한 관리 | 사용자 불편 | 기밀 문서 |
| **DLP** | 데이터 유출 | 이동 통제 | 오탐 가능 | 이메일, USB |

#### 3. 과목 융합 관점 분석

**네트워크 보안과 기밀성**:
- TLS 1.3의 0-RTT와 PFS는 기밀성과 성능의 균형
- IPsec VPN은 네트워크 계층 기밀성 보장
- MACsec은 L2 계층에서의 기밀성

**데이터베이스와 기밀성**:
- TDE (Transparent Data Encryption): 저장 기밀성
- Cell-level Encryption: 셀 단위 기밀성
- Always Encrypted (SQL Server): 클라이언트 측 기밀성

**클라우드와 기밀성**:
- Customer-Managed Keys (CMK): 고객 키 관리
- Envelope Encryption: 키 계층 구조
- Confidential Computing: 사용 중인 데이터 기밀성

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 하이브리드 클라우드 기밀성 설계**
- **상황**: 금융사의 민감 데이터 온프레미스 유지, 일반 데이터 클라우드
- **판단**:
  - 데이터 분류 체계 수립: 고객 PII → 온프레미스, 로그 → 클라우드
  - 전송 구간: Site-to-Site VPN + TLS 1.3
  - 키 관리: 온프레미스 HSM에서 마스터키, 클라우드 KMS에 DEK
  - 접근 통제: RBAC + ABAC 하이브리드

**시나리오 2: 의료 데이터 기밀성 컴플라이언스**
- **상황**: 병원 전자차트 시스템, 개인정보보호법 + 의료법 준수
- **판단**:
  - 환자 식별정보: AES-256 + 마스킹
  - 진료 기록: TDE + 접근 로그
  - 연구용 데이터: 비식별화 (k-anonymity)
  - 백업: 암호화 + 물리적 격리

**시나리오 3: 글로벌 서비스 기밀성**
- **상황**: 다국가 서비스, 각국 법규 준수 (GDPR, CCPA)
- **판단**:
  - 데이터 거주성(Data Residency): 국가별 리전
  - 키 관리: 리전별 KMS, cross-region replication 금지
  - 접근 통제: 국가별 규제 반영 ABAC 정책

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] 데이터 분류 체계 수립 완료
- [ ] 분류별 암호화 정책 정의
- [ ] 키 관리 프로세스 (생성/배포/순환/폐기)
- [ ] 암호화 성능 영향도 측정
- [ ] 레거시 시스템 호환성 검토
- [ ] 복호화 권한 및 감사 체계
- [ ] 장애 시 복구 절차 (키 손실 대응)

#### 3. 안티패턴 (Anti-patterns)
- **"암호화만 하면 안전"**: 키 관리 취약 → 무용지물
- **과도한 암호화**: 모든 데이터 최고 수준 → 성능 저하, 비용 증가
- **하드코딩 키**: 소스코드에 키 포함 → 유출 시 전체 무력화
- **키 순환 미실시**: 장기 사용 키 → 브루트포스 위험 증가

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | 내용 | 측정 지표 |
|:---|:---|:---|
| **정량적** | 데이터 유출 사고 감소 | 연간 유출 건수 80% 감소 |
| **정량적** | 컴플라이언스 비용 절감 | 인증 준비 기간 40% 단축 |
| **정성적** | 고객 신뢰도 향상 | 보안 인식 조사 90% 긍정 |
| **정성적** | 경쟁력 강화 | 보안 RFP 필수 요건 충족 |

#### 2. 미래 전망 및 진화 방향
- **양자 내성 암호 (PQC)**: 양자 컴퓨터 위협 대응 (CRYSTALS-Kyber)
- **동형 암호 (HE)**: 암호화된 상태로 연산, 클라우드 프라이버시
- **기밀 컴퓨팅 (Confidential Computing)**: TEE 기반 사용 중 데이터 보호
- **AI 기반 기밀성**: 지능형 분류, 이상 탐지, 자동 정책 조정

#### 3. 참고 표준/가이드
- **ISO/IEC 27001**: 정보보안 관리체계 - 부속서 A.8 자산관리
- **ISO/IEC 27002**: 보안 통제 - A.8.3 미디어 취급
- **NIST SP 800-111**: 저장 암호화 가이드
- **NIST SP 800-52 Rev 2**: TLS 가이드라인
- **PCI DSS v4.0**: 요구사항 3 - 저장된 계정 데이터 보호
- **GDPR Article 32**: 처리 보안 - 암호화 요건

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[CIA Triad](@/studynotes/09_security/01_policy/cia_triad.md)**: 기밀성을 포함한 정보보안 3대 요소
- **[암호화 알고리즘](@/studynotes/09_security/02_crypto/encryption_algorithms.md)**: 기밀성 보장을 위한 핵심 기술
- **[접근 통제](@/studynotes/09_security/01_policy/zero_trust_architecture.md)**: 인가된 사용자만 접근 허용
- **[PKI](@/studynotes/09_security/01_policy/pki.md)**: 암호화 키 관리 인프라
- **[DLP](@/studynotes/09_security/05_app/application_security_owasp.md)**: 데이터 유출 방지 기술
- **[개인정보보호](@/studynotes/09_security/01_policy/isms_p.md)**: 기밀성과 개인정보 보호의 연관성

---

### 👶 어린이를 위한 3줄 비유 설명
1. **비밀 일기장**: 너의 일기장에는 비밀번호를 아는 너만 볼 수 있어요. 다른 친구들이 몰래 읽지 못하게 하는 것이 기밀성이에요.
2. **보물 상자의 잠금**: 중요한 보물을 상자에 넣고 열쇠를 가진 사람만 열게 하는 것과 같아요. 암호는 아주 튼튼한 자물쇠랍니다.
3. **편지 봉투**: 편지를 보낼 때 봉투에 넣어서 아무나 읽지 못하게 하죠? 디지털 세계에서도 중요한 정보를 봉투처럼 감싸서 보호하는 거예요.
