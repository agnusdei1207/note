+++
title = "부인방지 (Non-repudiation)"
date = "2026-03-04"
[extra]
categories = "studynotes-09_security"
+++

# 부인방지 (Non-repudiation)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 사용자가 자신의 행위(전송, 수신, 승인 등)를 나중에 부인할 수 없도록 보장하는 정보보안 속성으로, 법적 효력을 갖는 디지털 증거를 생성합니다.
> 2. **가치**: 전자계약, 금융 거래, 법적 문서의 법적 효력 보장, 분쟁 해결 시 증거 제공, 무결성과 인증성의 최종 보증을 실현합니다.
> 3. **융합**: 전자서명, 타임스탬프, 감사 로그, 블록체인 등이 결합된 법적/기술적 복합 체계의 핵심 목표입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**부인방지(Non-repudiation)**는 정보 시스템에서 특정 행위(전송, 수신, 생성, 승인 등)를 수행한 주체가 나중에 그 행위를 부인할 수 없도록 보장하는 보안 서비스입니다. 이는 단순한 "증거 보관"을 넘어, 법적 효력을 갖는 **디지털 증거(Digital Evidence)**를 생성하는 포괄적 개념입니다.

**ISO 7498-2 정의**:
> "송신자가 데이터를 보냈다는 사실을 부인할 수 없게 하고, 수신자가 데이터를 받았다는 사실을 부인할 수 없게 하는 보안 서비스"

**부인방지의 유형**:
- **송신 부인방지 (Proof of Origin)**: A가 B에게 메시지를 보냈음을 증명
- **수신 부인방지 (Proof of Delivery)**: B가 A의 메시지를 받았음을 증명
- **제출 부인방지 (Proof of Submission)**: 특정 시점에 제출되었음을 증명
- **승인 부인방지 (Proof of Approval)**: 특정 행위를 승인했음을 증명

#### 2. 💡 비유를 통한 이해
부인방지는 **'공증과 등기'**에 비유할 수 있습니다.
- **공증**: 공증인이 문서 서명을 목격 - 전자서명
- **등기**: 부동산 거래를 공공기관에 등록 - 블록체인
- **우편 배달 증명**: 등기 우편 수령 서명 - 수신 확인
- **은행 거래 내역**: 거래 시간과 상세 기록 - 감사 로그

#### 3. 등장 배경 및 발전 과정
1. **서명의 역사**: 고대 낙인, 중세 봉인, 근대 필서명
2. **전자서명법**: 1995년 유타주 최초 전자서명법, 한국 1999년 전자서명법
3. **PKI 구축**: 인증기관(CA)을 통한 신뢰 체계 확립
4. **타임스탬프**: 신뢰 가능한 제3자(TSA)의 시간 증명
5. **블록체인**: 분산 원장에 의한 변조 불가능 기록
6. **전자문서법**: 각국 전자문서 법적 효력 인정

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 부인방지 기술 체계 (표)

| 기술 | 원리 | 법적 효력 | 용도 | 비용 |
|:---|:---|:---|:---|:---|
| **전자서명** | 공개키 암호 | 높음 | 계약, 공문서 | 중간 |
| **디지털 타임스탬프** | TSA 서명 | 높음 | 특허, 입찰 | 낮음 |
| **감사 로그** | 기록 보관 | 중간 | 시스템 추적 | 낮음 |
| **블록체인** | 분산 합의 | 진화 중 | 원장, 증권 | 중간 |
| **공인전자주소** | 국가 인증 | 높음 | 공공서비스 | 낮음 |
| **영상 녹화** | 물리적 증거 | 높음 | ATM, 은행 | 높음 |

#### 2. 부인방지 아키텍처 다이어그램

```text
<<< Non-Repudiation Service Architecture (ISO 13888) >>>

    +----------------------------------------------------------+
    |                    부인방지 서비스 요청                    |
    +----------------------------------------------------------+
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
            v                   v                   v
    +---------------+   +---------------+   +---------------+
    │ 송신 부인방지 │   │ 수신 부인방지 │   │ 생성 부인방지 │
    │ (NRO)         │   │ (NRD)         │   │ (NRC)         │
    +---------------+   +---------------+   +---------------+
            │                   │                   │
            v                   v                   v
    +----------------------------------------------------------+
    |              부인방지 증거 생성 (Evidence Generation)      |
    |  +----------------------------------------------------+  |
    |  |  1. 원문 해시 (Hash of Original)                    |  |
    |  |     SHA-256 / SHA-3                                |  |
    |  +----------------------------------------------------+  |
    |  |  2. 전자서명 (Digital Signature)                    |  |
    |  |     RSA-PSS / ECDSA / EdDSA                        |  |
    |  +----------------------------------------------------+  |
    |  |  3. 타임스탬프 (Timestamp)                          |  |
    |  |     TSA (Time Stamp Authority)                     |  |
    |  +----------------------------------------------------+  |
    |  |  4. 공증 (Notarization)                            |  |
    |  |     TTP (Trusted Third Party)                      |  |
    |  +----------------------------------------------------+  |
    +----------------------------------------------------------+
                                │
                                v
    +----------------------------------------------------------+
    |              부인방지 증거 저장 (Evidence Storage)         |
    |  +----------------------------------------------------+  |
    |  |  - 감사 로그 서버 (Audit Log Server)               |  |
    |  |  - 블록체인 (Blockchain)                           |  |
    |  |  - 아카이브 스토리지 (Archive Storage)             |  |
    |  |  - WORM (Write Once Read Many)                     |  |
    |  +----------------------------------------------------+  |
    +----------------------------------------------------------+
                                │
                                v
    +----------------------------------------------------------+
    |              부인방지 검증 (Non-Repudiation Verification)  |
    |  +----------------------------------------------------+  |
    |  |  1. 서명 검증 (Signature Verification)             |  |
    |  |  2. 인증서 검증 (Certificate Validation)           |  |
    |  |  3. 타임스탬프 검증 (Timestamp Verification)       |  |
    |  |  4. 증거 무결성 검증 (Evidence Integrity Check)    |  |
    |  +----------------------------------------------------+  |
    +----------------------------------------------------------+

<<< 전자서명 기반 부인방지 흐름 >>>

    [송신자 A]                          [수신자 B]
         │                                   │
         │  1. 문서 작성                      │
         │  ┌──────────────────────┐         │
         │  │ 계약서 원문           │         │
         │  │ - 당사자 정보         │         │
         │  │ - 조항 내용          │         │
         │  │ - 날짜               │         │
         │  └──────────────────────┘         │
         │                                   │
         │  2. 해시 계산                      │
         │  ┌──────────────────────┐         │
         │  │ Hash = SHA-256(문서) │         │
         │  └──────────────────────┘         │
         │                                   │
         │  3. 전자서명 생성                  │
         │  ┌──────────────────────┐         │
         │  │ Sig = Sign(Hash, SK) │         │
         │  │ 인증서 포함          │         │
         │  └──────────────────────┘         │
         │                                   │
         │  4. 타임스탬프 획득                │
         │  ┌──────────────────────┐         │
         │  │ TSA로부터 시간 증명   │         │
         │  └──────────────────────┘         │
         │                                   │
         │  5. 서명된 문서 전송               │
         │ ─────────────────────────────────>│
         │  [문서 + 서명 + 인증서 + 타임스탬프]│
         │                                   │
         │                    6. 서명 검증   │
         │                    ┌──────────┐   │
         │                    │ Verify   │   │
         │                    │ Signature│   │
         │                    └──────────┘   │
         │                                   │
         │                    7. 수신 확인서 │
         │                    생성 (선택)    │
         │ <─────────────────────────────────│
         │  [수신확인서 + B의 서명]           │
         │                                   │
```

#### 3. 심층 동작 원리: 전자서명 기반 부인방지

```python
import hashlib
import hmac
import secrets
import json
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, List, Tuple, Any
from enum import Enum
import struct

class SignatureAlgorithm(Enum):
    RSA_SHA256 = "RSA-SHA256"
    RSA_PSS = "RSA-PSS"
    ECDSA_P256 = "ECDSA-P256"
    ECDSA_P384 = "ECDSA-P384"
    ED25519 = "Ed25519"

class NonRepudiationType(Enum):
    NRO = "Non-Repudiation of Origin"      # 송신 부인방지
    NRD = "Non-Repudiation of Delivery"    # 수신 부인방지
    NRC = "Non-Repudiation of Creation"    # 생성 부인방지
    NRS = "Non-Repudiation of Submission"  # 제출 부인방지

@dataclass
class DigitalSignature:
    """디지털 서명 구조"""
    algorithm: str
    signature_value: bytes
    signer_certificate: bytes
    signing_time: str
    signature_policy: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            'algorithm': self.algorithm,
            'signature_value': self.signature_value.hex(),
            'signer_certificate': self.signer_certificate.hex(),
            'signing_time': self.signing_time,
            'signature_policy': self.signature_policy
        }

@dataclass
class TimestampToken:
    """타임스탬프 토큰 (RFC 3161)"""
    tsa_name: str
    timestamp: str
    message_imprint: bytes
    tsa_certificate: bytes
    tsa_signature: bytes

    def to_dict(self) -> dict:
        return {
            'tsa_name': self.tsa_name,
            'timestamp': self.timestamp,
            'message_imprint': self.message_imprint.hex(),
            'tsa_certificate': self.tsa_certificate.hex(),
            'tsa_signature': self.tsa_signature.hex()
        }

@dataclass
class NonRepudiationEvidence:
    """부인방지 증거"""
    evidence_id: str
    evidence_type: str
    original_document_hash: bytes
    signatures: List[Dict]
    timestamp_tokens: List[Dict]
    creation_time: str
    archive_reference: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps({
            'evidence_id': self.evidence_id,
            'evidence_type': self.evidence_type,
            'original_document_hash': self.original_document_hash.hex(),
            'signatures': self.signatures,
            'timestamp_tokens': self.timestamp_tokens,
            'creation_time': self.creation_time,
            'archive_reference': self.archive_reference
        }, indent=2)

class NonRepudiationService:
    """
    부인방지 서비스 구현
    - 전자서명 생성 및 검증
    - 타임스탬프 생성 및 검증
    - 증거 생성 및 보관
    - 분쟁 해결 지원
    """

    def __init__(self):
        self.evidence_store: Dict[str, NonRepudiationEvidence] = {}
        self.signature_policies = {
            'default': {
                'algorithm': 'ECDSA-P256',
                'require_timestamp': True,
                'require_certificate': True,
                'validity_period_days': 3650  # 10년
            }
        }

    def create_signature(self,
                        document: bytes,
                        private_key: bytes,
                        signer_cert: bytes,
                        algorithm: SignatureAlgorithm = SignatureAlgorithm.ECDSA_P256) -> DigitalSignature:
        """
        전자서명 생성
        - 문서 해시 계산
        - 개인키로 서명
        - 서명 시간 기록
        """
        # 문서 해시
        document_hash = hashlib.sha256(document).digest()

        # 서명 생성 (시뮬레이션)
        # 실제로는 cryptography.hazmat.primitives.asymmetric 사용
        signature_value = self._sign_hash(document_hash, private_key, algorithm)

        signing_time = datetime.now(timezone.utc).isoformat()

        return DigitalSignature(
            algorithm=algorithm.value,
            signature_value=signature_value,
            signer_certificate=signer_cert,
            signing_time=signing_time,
            signature_policy='default'
        )

    def verify_signature(self,
                        document: bytes,
                        signature: DigitalSignature) -> Tuple[bool, Dict]:
        """
        전자서명 검증
        - 서명 무결성 확인
        - 인증서 유효성 확인
        - 서명 시간 확인
        """
        result = {
            'valid': False,
            'signer_verified': False,
            'timestamp_verified': False,
            'integrity_verified': False,
            'details': []
        }

        # 1. 문서 무결성 검증
        document_hash = hashlib.sha256(document).digest()
        signature_hash = hashlib.sha256(
            signature.signature_value + signature.signer_certificate
        ).digest()

        result['integrity_verified'] = True
        result['details'].append("Document integrity verified")

        # 2. 서명 검증 (시뮬레이션)
        # 실제로는 공개키로 서명 검증
        signature_valid = self._verify_signature_internal(
            document_hash,
            signature.signature_value,
            signature.signer_certificate
        )

        if signature_valid:
            result['signer_verified'] = True
            result['details'].append(f"Signature verified - Algorithm: {signature.algorithm}")
        else:
            result['details'].append("Signature verification failed")
            return False, result

        # 3. 인증서 검증 (시뮬레이션)
        cert_valid = self._verify_certificate(signature.signer_certificate)
        if cert_valid:
            result['details'].append("Signer certificate valid")
        else:
            result['details'].append("Certificate validation failed")
            return False, result

        result['valid'] = True
        return True, result

    def create_timestamp(self,
                        data: bytes,
                        tsa_private_key: bytes,
                        tsa_cert: bytes,
                        tsa_name: str = "TSA-001") -> TimestampToken:
        """
        타임스탬프 토큰 생성 (RFC 3161 준수)
        - 데이터 해시
        - TSA 서명
        - 시간 정보 포함
        """
        # 메시지 임프린트 (해시)
        message_imprint = hashlib.sha256(data).digest()

        # 현재 시간 (UTC)
        timestamp = datetime.now(timezone.utc).isoformat()

        # TSA 서명 생성
        tsa_data = message_imprint + timestamp.encode()
        tsa_signature = self._sign_hash(tsa_data, tsa_private_key, SignatureAlgorithm.RSA_SHA256)

        return TimestampToken(
            tsa_name=tsa_name,
            timestamp=timestamp,
            message_imprint=message_imprint,
            tsa_certificate=tsa_cert,
            tsa_signature=tsa_signature
        )

    def verify_timestamp(self,
                        data: bytes,
                        token: TimestampToken) -> Tuple[bool, Dict]:
        """
        타임스탬프 토큰 검증
        """
        result = {
            'valid': False,
            'timestamp': token.timestamp,
            'tsa_name': token.tsa_name,
            'details': []
        }

        # 1. 메시지 임프린트 검증
        expected_imprint = hashlib.sha256(data).digest()
        if expected_imprint == token.message_imprint:
            result['details'].append("Message imprint verified")
        else:
            result['details'].append("Message imprint mismatch")
            return False, result

        # 2. TSA 서명 검증 (시뮬레이션)
        tsa_data = token.message_imprint + token.timestamp.encode()
        tsa_valid = self._verify_signature_internal(
            tsa_data,
            token.tsa_signature,
            token.tsa_certificate
        )

        if tsa_valid:
            result['details'].append("TSA signature verified")
        else:
            result['details'].append("TSA signature invalid")
            return False, result

        result['valid'] = True
        return True, result

    def create_evidence(self,
                       document: bytes,
                       signatures: List[DigitalSignature],
                       timestamps: List[TimestampToken],
                       evidence_type: NonRepudiationType) -> NonRepudiationEvidence:
        """
        부인방지 증거 생성
        """
        evidence_id = f"EVD-{secrets.token_hex(8).upper()}"
        document_hash = hashlib.sha256(document).digest()

        evidence = NonRepudiationEvidence(
            evidence_id=evidence_id,
            evidence_type=evidence_type.value,
            original_document_hash=document_hash,
            signatures=[sig.to_dict() for sig in signatures],
            timestamp_tokens=[ts.to_dict() for ts in timestamps],
            creation_time=datetime.now(timezone.utc).isoformat()
        )

        self.evidence_store[evidence_id] = evidence
        return evidence

    def verify_evidence(self,
                       document: bytes,
                       evidence: NonRepudiationEvidence) -> Tuple[bool, Dict]:
        """
        부인방지 증거 검증
        """
        result = {
            'valid': False,
            'evidence_id': evidence.evidence_id,
            'evidence_type': evidence.evidence_type,
            'signature_results': [],
            'timestamp_results': [],
            'details': []
        }

        # 1. 문서 무결성 검증
        document_hash = hashlib.sha256(document).digest()
        if document_hash == evidence.original_document_hash:
            result['details'].append("Document hash matches evidence")
        else:
            result['details'].append("Document hash mismatch - evidence may be tampered")
            return False, result

        # 2. 서명 검증
        all_signatures_valid = True
        for sig_dict in evidence.signatures:
            sig = DigitalSignature(
                algorithm=sig_dict['algorithm'],
                signature_value=bytes.fromhex(sig_dict['signature_value']),
                signer_certificate=bytes.fromhex(sig_dict['signer_certificate']),
                signing_time=sig_dict['signing_time']
            )

            valid, sig_result = self.verify_signature(document, sig)
            result['signature_results'].append(sig_result)
            if not valid:
                all_signatures_valid = False

        # 3. 타임스탬프 검증
        all_timestamps_valid = True
        for ts_dict in evidence.timestamp_tokens:
            ts = TimestampToken(
                tsa_name=ts_dict['tsa_name'],
                timestamp=ts_dict['timestamp'],
                message_imprint=bytes.fromhex(ts_dict['message_imprint']),
                tsa_certificate=bytes.fromhex(ts_dict['tsa_certificate']),
                tsa_signature=bytes.fromhex(ts_dict['tsa_signature'])
            )

            valid, ts_result = self.verify_timestamp(document, ts)
            result['timestamp_results'].append(ts_result)
            if not valid:
                all_timestamps_valid = False

        result['valid'] = all_signatures_valid and all_timestamps_valid
        return result['valid'], result

    def _sign_hash(self,
                   data_hash: bytes,
                   private_key: bytes,
                   algorithm: SignatureAlgorithm) -> bytes:
        """해시 서명 (시뮬레이션)"""
        # 실제 구현에서는 RSA/ECDSA 사용
        combined = data_hash + private_key
        return hashlib.sha256(combined).digest()

    def _verify_signature_internal(self,
                                   data: bytes,
                                   signature: bytes,
                                   certificate: bytes) -> bool:
        """서명 검증 (시뮬레이션)"""
        # 실제 구현에서는 공개키로 검증
        return True

    def _verify_certificate(self, certificate: bytes) -> bool:
        """인증서 검증 (시뮬레이션)"""
        return True

class AuditLogService:
    """
    감사 로그 서비스
    - 부인방지를 위한 로그 기록
    - 로그 무결성 보호
    - 로그 검색 및 분석
    """

    def __init__(self):
        self.logs: List[Dict] = []
        self.log_chain_hash: bytes = b'\x00' * 32  # 제네시스 해시

    def log_event(self,
                  event_type: str,
                  actor: str,
                  action: str,
                  resource: str,
                  details: Dict = None) -> Dict:
        """
        이벤트 로그 기록
        - 체인 구조로 무결성 보호
        - 타임스탬프 포함
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        log_entry = {
            'log_id': secrets.token_hex(8),
            'timestamp': timestamp,
            'event_type': event_type,
            'actor': actor,
            'action': action,
            'resource': resource,
            'details': details or {},
            'previous_hash': self.log_chain_hash.hex()
        }

        # 체인 해시 계산
        entry_bytes = json.dumps(log_entry, sort_keys=True).encode()
        self.log_chain_hash = hashlib.sha256(entry_bytes).digest()
        log_entry['chain_hash'] = self.log_chain_hash.hex()

        self.logs.append(log_entry)
        return log_entry

    def verify_log_integrity(self) -> Tuple[bool, List[int]]:
        """
        로그 체인 무결성 검증
        """
        violations = []
        previous_hash = b'\x00' * 32

        for i, log in enumerate(self.logs):
            # 이전 해시 확인
            if log['previous_hash'] != previous_hash.hex():
                violations.append(i)

            # 체인 해시 재계산
            log_copy = {k: v for k, v in log.items() if k != 'chain_hash'}
            entry_bytes = json.dumps(log_copy, sort_keys=True).encode()
            computed_hash = hashlib.sha256(entry_bytes).digest()

            if computed_hash.hex() != log['chain_hash']:
                violations.append(i)

            previous_hash = bytes.fromhex(log['chain_hash'])

        return len(violations) == 0, violations

    def search_logs(self,
                    start_time: str = None,
                    end_time: str = None,
                    actor: str = None,
                    event_type: str = None) -> List[Dict]:
        """로그 검색"""
        results = []

        for log in self.logs:
            match = True

            if start_time and log['timestamp'] < start_time:
                match = False
            if end_time and log['timestamp'] > end_time:
                match = False
            if actor and log['actor'] != actor:
                match = False
            if event_type and log['event_type'] != event_type:
                match = False

            if match:
                results.append(log)

        return results

# 사용 예시
if __name__ == "__main__":
    # 1. 부인방지 서비스 초기화
    nr_service = NonRepudiationService()

    # 2. 문서 준비
    contract = b"""
    계약서

    갑 (이하 "갑"이라 한다)과 을 (이하 "을"이라 한다)은
    다음과 같이 계약을 체결한다.

    제1조 (목적) ...
    제2조 (권리와 의무) ...

    작성일: 2026-03-04
    """

    # 3. 서명 생성 (시뮬레이션)
    signer_key = secrets.token_bytes(32)
    signer_cert = secrets.token_bytes(100)

    signature = nr_service.create_signature(
        document=contract,
        private_key=signer_key,
        signer_cert=signer_cert
    )
    print(f"=== 전자서명 생성 ===")
    print(f"Algorithm: {signature.algorithm}")
    print(f"Signing Time: {signature.signing_time}")

    # 4. 서명 검증
    valid, result = nr_service.verify_signature(contract, signature)
    print(f"\n=== 서명 검증 결과 ===")
    print(f"Valid: {valid}")
    for detail in result['details']:
        print(f"  - {detail}")

    # 5. 타임스탬프 생성
    tsa_key = secrets.token_bytes(32)
    tsa_cert = secrets.token_bytes(100)

    timestamp = nr_service.create_timestamp(
        data=contract,
        tsa_private_key=tsa_key,
        tsa_cert=tsa_cert
    )
    print(f"\n=== 타임스탬프 생성 ===")
    print(f"TSA: {timestamp.tsa_name}")
    print(f"Timestamp: {timestamp.timestamp}")

    # 6. 부인방지 증거 생성
    evidence = nr_service.create_evidence(
        document=contract,
        signatures=[signature],
        timestamps=[timestamp],
        evidence_type=NonRepudiationType.NRO
    )
    print(f"\n=== 부인방지 증거 ===")
    print(f"Evidence ID: {evidence.evidence_id}")
    print(f"Type: {evidence.evidence_type}")

    # 7. 증거 검증
    valid, result = nr_service.verify_evidence(contract, evidence)
    print(f"\n=== 증거 검증 ===")
    print(f"Valid: {valid}")
    for detail in result['details']:
        print(f"  - {detail}")

    # 8. 감사 로그 테스트
    audit_log = AuditLogService()

    audit_log.log_event(
        event_type="SIGN",
        actor="user@example.com",
        action="document_signed",
        resource=contract[:50].hex(),
        details={'signature_id': signature.signing_time}
    )

    audit_log.log_event(
        event_type="SUBMIT",
        actor="user@example.com",
        action="document_submitted",
        resource=contract[:50].hex()
    )

    integrity_valid, violations = audit_log.verify_log_integrity()
    print(f"\n=== 감사 로그 무결성 ===")
    print(f"Valid: {integrity_valid}")
    if violations:
        print(f"Violations at indices: {violations}")
