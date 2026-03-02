+++
title = "PKI (공개키 기반 구조)"
date = 2025-03-02

[extra]
categories = "pe_exam-ict_convergence"
+++

# PKI (공개키 기반 구조)

## 핵심 인사이트 (3줄 요약)
> **공개키 암호의 신뢰성을 보증하는 계층형 인증 인프라**. CA(인증기관)가 디지털 인증서에 서명하여 신원 보증. HTTPS, 전자서명, 코드사이닝의 기반이다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: PKI(Public Key Infrastructure)는 **공개키 암호방식을 기반으로 사용자의 신원을 확인하고, 공개키의 진위를 제3자(CA)가 보증하는 하드웨어·소프트웨어·정책·인력의 통합 인프라**이다.

> 💡 **비유**: PKI는 **"여권 발급 시스템"** 같아요. 내가 "나는 홍길동이다"라고 주장만 하면 아무도 안 믿죠. 하지만 정부(CA)가 내 여권(인증서)에 사진과 도장(서명)을 찍어주면, 전 세계 어디서든 신원이 증명돼요!

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 공개키 신뢰 문제**: 비대칭 암호는 안전하지만, "이 공개키가 정말 홍길동의 것인가?"를 증명할 방법이 없음
2. **기술적 필요성 - 중간자 공격**: 공격자가 자신의 공개키을 홍길동인 척 배포하면 암호화가 무의미해짐
3. **시장/산업 요구 - 전자상거래**: 1990년대 인터넷 쇼핑, 뱅킹 확산으로 신뢰할 수 있는 온라인 신원 확인 체계 필수

**핵심 목적**: **공개키의 진위 보증, 부인방지, 기밀성·무결성 확보**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**PKI 구성요소 아키텍처** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        PKI 구성요소 구조                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                     Root CA (신뢰 앵커)                          │  │
│   │                        🏛️                                       │  │
│   │        (자체 서명 인증서, 브라우저/OS에 사전 탑재)                │  │
│   │              예: DigiCert, GlobalSign, 국가정보원               │  │
│   └───────────────────────────┬─────────────────────────────────────┘  │
│                               │ 서명                                    │
│           ┌───────────────────┼───────────────────┐                    │
│           │                   │                   │                    │
│           ▼                   ▼                   ▼                    │
│   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐           │
│   │ 중간 CA (ICA) │   │ 중간 CA (ICA) │   │ 중간 CA (ICA) │           │
│   │  (Issuing CA) │   │  (Issuing CA) │   │  (Issuing CA) │           │
│   └───────┬───────┘   └───────┬───────┘   └───────┬───────┘           │
│           │                   │                   │                    │
│           ▼                   ▼                   ▼                    │
│   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐           │
│   │  최종 사용자  │   │  최종 사용자  │   │    서버       │           │
│   │   인증서      │   │   인증서      │   │   인증서      │           │
│   │  (Client)    │   │  (Client)    │   │  (Server)     │           │
│   └───────────────┘   └───────────────┘   └───────────────┘           │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                        PKI 구성요소                              │  │
│   ├─────────────────────────────────────────────────────────────────┤  │
│   │                                                                 │  │
│   │  🏛️ CA (Certificate Authority) - 인증 기관                      │  │
│   │     • 인증서 발급, 갱신, 폐기                                    │  │
│   │     • 신원 검증 및 디지털 서명                                   │  │
│   │     • CRL/OCSP 운영                                             │  │
│   │                                                                 │  │
│   │  📋 RA (Registration Authority) - 등록 기관                     │  │
│   │     • 신원 확인 (실물 신분증, 사업자등록증 등)                   │  │
│   │     • 인증서 요청(CSR) 접수 및 CA 전달                          │  │
│   │                                                                 │  │
│   │  📦 Repository - 인증서 저장소                                   │  │
│   │     • 인증서, CRL 저장 및 조회                                  │  │
│   │     • LDAP, HTTP, OCSP 서버                                     │  │
│   │                                                                 │  │
│   │  👤 End Entity - 최종 사용자                                     │  │
│   │     • 인증서 신청자, 사용자                                      │  │
│   │     • 개인키 안전 보관 (HSM, TPM, 스마트카드)                    │  │
│   │                                                                 │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**X.509 인증서 구조** (필수: 상세):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    X.509 v3 인증서 구조                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                         기본 필드                                │  │
│   ├─────────────────────────────────────────────────────────────────┤  │
│   │ Version (3)                    │ 인증서 버전                     │  │
│   │ Serial Number                  │ 고유 일련번호 (CA가 부여)       │  │
│   │ Signature Algorithm            │ 서명 알고리즘 (SHA256withRSA)  │  │
│   │ Issuer                         │ 발급자 DN (CN=DigiCert CA...)  │  │
│   │ Validity Period                │ 유효기간 (Not Before/After)    │  │
│   │ Subject                        │ 소유자 DN (CN=google.com)      │  │
│   │ Subject Public Key Info        │ 공개키 (RSA 2048bit)           │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                     확장 필드 (Extensions)                       │  │
│   ├─────────────────────────────────────────────────────────────────┤  │
│   │ Key Usage                     │ 키 용도 (서명, 암호화, ...)     │  │
│   │ Extended Key Usage            │ 확장 키 용도 (SSL, 코드서명)    │  │
│   │ Subject Alternative Name      │ 추가 도메인 (SAN, 와일드카드)   │  │
│   │ Basic Constraints             │ CA 여부, 경로 제한              │  │
│   │ CRL Distribution Points       │ CRL 조회 위치                   │  │
│   │ Authority Info Access         │ OCSP 서버 위치                  │  │
│   │ Subject Key Identifier        │ 키 식별자                       │  │
│   │ Authority Key Identifier      │ 발급자 키 식별자                │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                      서명 (Signature)                            │  │
│   ├─────────────────────────────────────────────────────────────────┤  │
│   │ CA의 개인키로 위 모든 필드에 서명                                │  │
│   │ Signature = Sign(Hash(TBSCertificate), CA_PrivateKey)            │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│   인증서 검증 과정:                                                     │
│   1. 인증서 구문 파싱                                                   │
│   2. 서명 알고리즘 확인                                                  │
│   3. CA 공개키로 서명 검증                                              │
│   4. 유효기간 확인                                                       │
│   5. CRL/OCSP로 폐기 여부 확인                                          │
│   6. 인증서 체인 검증 (End Entity → Intermediate → Root)               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**PKI 프로세스 흐름** (필수: 표):
| 단계 | 주체 | 활동 | 상세 내용 |
|------|------|------|----------|
| 1 | 사용자 | 키 쌍 생성 | 공개키/개인키 생성 (RSA 2048+ 또는 ECC) |
| 2 | 사용자 | CSR 생성 | Certificate Signing Request (공개키 + DN) |
| 3 | 사용자 | RA 신청 | 신분증/사업자등록증으로 신원 증명 |
| 4 | RA | 신원 검증 | 실물 확인 후 CA에 발급 요청 전달 |
| 5 | CA | 인증서 발급 | CSR에 서명하여 X.509 인증서 생성 |
| 6 | CA | 인증서 배포 | Repository에 저장, 사용자에게 전달 |
| 7 | 사용자 | 인증서 사용 | TLS, 전자서명, 코드사이닝 등 |
| 8 | CA | 폐기/갱신 | 만료 또는 키 유출 시 CRL/OCSP 등록 |

**인증서 유형 및 검증 수준** (필수: 표):
| 유형 | 검증 내용 | 브라우저 표시 | 용도 |
|------|----------|--------------|------|
| **DV** (Domain Validation) | 도메인 소유권만 확인 | 🔒 자물쇠 | 개인 블로그, 테스트 |
| **OV** (Organization Validation) | 조직 실체 확인 + 도메인 | 🔒 자물쇠 + 회사명 | 기업 웹사이트 |
| **EV** (Extended Validation) | 엄격한 신원 검증 (법적 서류) | 🔒 + 주소록 녹색 | 금융, 쇼핑몰 |
| **IV** (Individual Validation) | 개인 신원 확인 | 🔒 | 개인 인증서 |
| **Code Signing** | 소프트웨어 개발자 확인 | OS 신뢰 경고 없음 | 앱/드라이버 배포 |
| **Client** | 클라이언트 신원 확인 | (사용자 인증용) | VPN, 뱅킹 |

**핵심 알고리즘/공식** (해당 시 필수):
```
[인증서 체인 검증]

신뢰 앵커(Trust Anchor) = Root CA (브라우저/OS에 사전 탑재)

검증 경로:
  End Entity Cert → Intermediate CA Cert → Root CA Cert

각 단계 검증:
  1. 서명 검증: Verify(인증서, 상위_CA_공개키)
  2. 유효기간: NotBefore ≤ 현재시간 ≤ NotAfter
  3. 용도 확인: KeyUsage, ExtendedKeyUsage
  4. 정책 확인: Certificate Policies
  5. 폐기 확인: CRL 또는 OCSP

[CSR (Certificate Signing Request) 구조]

CSR = PKCS#10 또는 CRMF 형식
     = Subject DN + 공개키 + 속성 + 사용자 개인키 서명

PEM 형식:
-----BEGIN CERTIFICATE REQUEST-----
MIICVDCCATwCAQAwDzENMAsGA1UEAwwEdGVzdD... (Base64)
-----END CERTIFICATE REQUEST-----

[CRL (Certificate Revocation List)]

CRL = CA가 주기적으로 발행하는 폐기된 인증서 목록

구조:
  - 발급자, 발급시간, 다음 갱신시간
  - 폐기된 인증서 일련번호 목록 + 폐기 사유 + 폐기 시간
  - CA 서명

폐기 사유 코드:
  0: Unspecified
  1: Key Compromise (키 유출)
  2: CA Compromise (CA 침해)
  3: Affiliation Changed (소속 변경)
  4: Superseded (교체)
  5: Cessation of Operation (운영 중단)
  6: Certificate Hold (일시 정지)

[OCSP (Online Certificate Status Protocol)]

실시간 인증서 상태 확인

요청: OCSP Request = 인증서 일련번호
응답: OCSP Response = {good | revoked | unknown}

장점: CRL보다 실시간, 대역폭 절약
단점: CA 서버 가용성 의존, 프라이버시 우려

OCSP Stapling: 서버가 OCSP 응답을 미리 받아 TLS 핸드셰이크에 포함
```

**코드 예시** (필수: Python PKI 구현):
```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum, auto
from datetime import datetime, timedelta
import hashlib
import secrets

# ============================================================
# PKI 인프라 시뮬레이터
# ============================================================

class KeyUsage(Enum):
    """키 용도"""
    DIGITAL_SIGNATURE = auto()
    KEY_ENCIPHERMENT = auto()
    DATA_ENCIPHERMENT = auto()
    KEY_CERT_SIGN = auto()
    CRL_SIGN = auto()


class RevocationReason(Enum):
    """폐기 사유"""
    UNSPECIFIED = 0
    KEY_COMPROMISE = 1
    CA_COMPROMISE = 2
    AFFILIATION_CHANGED = 3
    SUPERSEDED = 4
    CESSATION_OF_OPERATION = 5
    CERTIFICATE_HOLD = 6


@dataclass
class PublicKey:
    """공개키 (시뮬레이션)"""
    algorithm: str = "RSA"
    key_size: int = 2048
    key_id: str = ""

    def __post_init__(self):
        if not self.key_id:
            self.key_id = secrets.token_hex(16)

    def verify_signature(self, data: bytes, signature: bytes) -> bool:
        """서명 검증 (시뮬레이션)"""
        # 실제로는 RSA/ECDSA 검증 수행
        return True


@dataclass
class PrivateKey:
    """개인키 (시뮬레이션)"""
    algorithm: str = "RSA"
    key_size: int = 2048
    key_id: str = ""
    public_key: Optional[PublicKey] = None

    def __post_init__(self):
        if not self.key_id:
            self.key_id = secrets.token_hex(16)
        if not self.public_key:
            self.public_key = PublicKey(self.algorithm, self.key_size, self.key_id)

    def sign(self, data: bytes) -> bytes:
        """서명 생성 (시뮬레이션)"""
        # 실제로는 RSA/ECDSA 서명 수행
        return hashlib.sha256(data + self.key_id.encode()).digest()


@dataclass
class Certificate:
    """X.509 인증서 (시뮬레이션)"""
    subject: str
    issuer: str
    serial_number: int
    not_before: datetime
    not_after: datetime
    public_key: PublicKey
    key_usage: List[KeyUsage] = field(default_factory=list)
    is_ca: bool = False
    san: List[str] = field(default_factory=list)  # Subject Alternative Names
    signature: bytes = b''
    signature_algorithm: str = "SHA256withRSA"

    @property
    def is_expired(self) -> bool:
        return datetime.now() > self.not_after

    @property
    def is_not_yet_valid(self) -> bool:
        return datetime.now() < self.not_before

    @property
    def is_valid_period(self) -> bool:
        return not self.is_expired and not self.is_not_yet_valid

    def to_der(self) -> bytes:
        """DER 인코딩 (시뮬레이션)"""
        data = f"{self.subject}{self.issuer}{self.serial_number}".encode()
        data += self.not_before.isoformat().encode()
        data += self.not_after.isoformat().encode()
        data += self.public_key.key_id.encode()
        return data

    def __str__(self):
        lines = [
            f"Certificate:",
            f"  Subject: {self.subject}",
            f"  Issuer: {self.issuer}",
            f"  Serial: {self.serial_number}",
            f"  Valid: {self.not_before} - {self.not_after}",
            f"  Key Usage: {[k.name for k in self.key_usage]}",
            f"  CA: {self.is_ca}",
        ]
        if self.san:
            lines.append(f"  SAN: {self.san}")
        return "\n".join(lines)


@dataclass
class RevokedCertificate:
    """폐기된 인증서 정보"""
    serial_number: int
    revocation_date: datetime
    reason: RevocationReason


class CRL:
    """인증서 폐기 목록 (CRL)"""

    def __init__(self, issuer: str):
        self.issuer = issuer
        self.revoked_certs: Dict[int, RevokedCertificate] = {}
        self.last_update: datetime = datetime.now()
        self.next_update: datetime = datetime.now() + timedelta(days=1)
        self.signature: bytes = b''

    def add_revoked(self, serial: int, reason: RevocationReason) -> None:
        """폐기 인증서 추가"""
        self.revoked_certs[serial] = RevokedCertificate(
            serial_number=serial,
            revocation_date=datetime.now(),
            reason=reason
        )
        self.last_update = datetime.now()

    def is_revoked(self, serial: int) -> bool:
        """폐기 여부 확인"""
        return serial in self.revoked_certs

    def get_revocation_info(self, serial: int) -> Optional[RevokedCertificate]:
        """폐기 정보 조회"""
        return self.revoked_certs.get(serial)


class OCSPResponder:
    """OCSP 응답자 (시뮬레이션)"""

    def __init__(self, crl: CRL):
        self.crl = crl

    def check_status(self, serial: int) -> str:
        """인증서 상태 확인"""
        if serial in self.crl.revoked_certs:
            return "revoked"
        return "good"


class CertificateAuthority:
    """인증 기관 (CA)"""

    def __init__(self, name: str, is_root: bool = False,
                 parent_ca: Optional['CertificateAuthority'] = None):
        self.name = name
        self.is_root = is_root
        self.parent_ca = parent_ca
        self.private_key = PrivateKey()
        self.certificate: Optional[Certificate] = None
        self.issued_certs: Dict[int, Certificate] = {}
        self.crl = CRL(name)
        self.ocsp_responder = OCSPResponder(self.crl)
        self._serial_counter = 1

        # Root CA면 자체 서명
        if is_root:
            self._self_sign()

    def _self_sign(self) -> None:
        """자체 서명 (Root CA)"""
        now = datetime.now()
        cert = Certificate(
            subject=self.name,
            issuer=self.name,
            serial_number=self._serial_counter,
            not_before=now,
            not_after=now + timedelta(days=3650),  # 10년
            public_key=self.private_key.public_key,
            key_usage=[KeyUsage.KEY_CERT_SIGN, KeyUsage.CRL_SIGN],
            is_ca=True
        )
        cert.signature = self.private_key.sign(cert.to_der())
        self.certificate = cert
        self._serial_counter += 1

    def issue_certificate(self, subject: str, public_key: PublicKey,
                          days: int = 365, is_ca: bool = False,
                          san: List[str] = None,
                          key_usage: List[KeyUsage] = None) -> Certificate:
        """인증서 발급"""
        now = datetime.now()
        cert = Certificate(
            subject=subject,
            issuer=self.name,
            serial_number=self._serial_counter,
            not_before=now,
            not_after=now + timedelta(days=days),
            public_key=public_key,
            key_usage=key_usage or [KeyUsage.DIGITAL_SIGNATURE],
            is_ca=is_ca,
            san=san or []
        )

        # CA 개인키로 서명
        cert.signature = self.private_key.sign(cert.to_der())

        self.issued_certs[self._serial_counter] = cert
        self._serial_counter += 1

        return cert

    def revoke_certificate(self, serial: int, reason: RevocationReason) -> None:
        """인증서 폐기"""
        self.crl.add_revoked(serial, reason)
        print(f"[CA] 인증서 폐기: Serial={serial}, 사유={reason.name}")

    def verify_certificate(self, cert: Certificate) -> Tuple[bool, str]:
        """인증서 검증"""
        # 1. 발급자 확인
        if cert.issuer != self.name:
            return False, "발급자 불일치"

        # 2. 서명 검증
        if not self.private_key.public_key.verify_signature(cert.to_der(), cert.signature):
            return False, "서명 검증 실패"

        # 3. 유효기간 확인
        if cert.is_expired:
            return False, "인증서 만료"
        if cert.is_not_yet_valid:
            return False, "아직 유효하지 않음"

        # 4. 폐기 여부 확인
        if self.crl.is_revoked(cert.serial_number):
            info = self.crl.get_revocation_info(cert.serial_number)
            return False, f"폐기됨: {info.reason.name}"

        return True, "유효"


class PKIInfrastructure:
    """PKI 인프라 시뮬레이터"""

    def __init__(self):
        self.root_ca: Optional[CertificateAuthority] = None
        self.intermediate_cas: Dict[str, CertificateAuthority] = {}
        self.trust_store: Dict[str, Certificate] = {}  # 신뢰 앵커 저장소

    def setup_root_ca(self, name: str) -> CertificateAuthority:
        """Root CA 설정"""
        self.root_ca = CertificateAuthority(name, is_root=True)
        self.trust_store[name] = self.root_ca.certificate
        print(f"[PKI] Root CA 생성: {name}")
        return self.root_ca

    def create_intermediate_ca(self, name: str,
                                parent: CertificateAuthority) -> CertificateAuthority:
        """중간 CA 생성"""
        ica = CertificateAuthority(name, parent_ca=parent)

        # 상위 CA로부터 인증서 발급
        ica_cert = parent.issue_certificate(
            subject=name,
            public_key=ica.private_key.public_key,
            days=1825,  # 5년
            is_ca=True,
            key_usage=[KeyUsage.KEY_CERT_SIGN, KeyUsage.CRL_SIGN]
        )
        ica.certificate = ica_cert
        self.intermediate_cas[name] = ica
        print(f"[PKI] 중간 CA 생성: {name} (발급자: {parent.name})")
        return ica

    def verify_chain(self, cert: Certificate,
                     chain: List[Certificate]) -> Tuple[bool, List[str]]:
        """인증서 체인 검증"""
        issues = []

        # 체인 구성: End Entity → Intermediate → Root
        full_chain = [cert] + chain

        for i in range(len(full_chain) - 1):
            current = full_chain[i]
            issuer_cert = full_chain[i + 1]

            # 발급자 이름 확인
            if current.issuer != issuer_cert.subject:
                issues.append(f"체인 끊김: {current.subject} → {issuer_cert.subject}")

            # CA 여부 확인
            if not issuer_cert.is_ca:
                issues.append(f"비 CA가 인증서 발급: {issuer_cert.subject}")

        # Root CA가 신뢰 앵커인지 확인
        root = full_chain[-1]
        if root.issuer not in self.trust_store:
            issues.append(f"신뢰할 수 없는 Root CA: {root.issuer}")

        return len(issues) == 0, issues

    def print_trust_store(self) -> None:
        """신뢰 저장소 출력"""
        print("\n=== 신뢰 저장소 (Trust Store) ===")
        for name, cert in self.trust_store.items():
            print(f"  {name}: Serial={cert.serial_number}")


# ============================================================
# CSR 생성기 (시뮬레이션)
# ============================================================

@dataclass
class CSR:
    """Certificate Signing Request"""
    subject: str
    public_key: PublicKey
    attributes: Dict[str, str] = field(default_factory=dict)
    signature: bytes = b''

    @classmethod
    def create(cls, subject: str, private_key: PrivateKey,
               attributes: Dict[str, str] = None) -> 'CSR':
        """CSR 생성"""
        csr = cls(
            subject=subject,
            public_key=private_key.public_key,
            attributes=attributes or {}
        )
        # 사용자 개인키로 서명
        data = f"{subject}{private_key.public_key.key_id}".encode()
        csr.signature = private_key.sign(data)
        return csr


# ============================================================
# 사용 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("         PKI 인프라 시뮬레이터 데모")
    print("=" * 60)

    # 1. PKI 인프라 구축
    print("\n1. PKI 인프라 구축")
    print("-" * 40)

    pki = PKIInfrastructure()

    # Root CA 생성
    root_ca = pki.setup_root_ca("MyRoot CA")

    # 중간 CA 생성
    intermediate_ca = pki.create_intermediate_ca("MyIntermediate CA", root_ca)

    pki.print_trust_store()

    # 2. 서버 인증서 발급
    print("\n2. 서버 인증서 발급")
    print("-" * 40)

    # 서버 키 쌍 생성
    server_key = PrivateKey(algorithm="RSA", key_size=2048)

    # 인증서 발급
    server_cert = intermediate_ca.issue_certificate(
        subject="www.example.com",
        public_key=server_key.public_key,
        days=365,
        san=["www.example.com", "example.com", "api.example.com"],
        key_usage=[KeyUsage.DIGITAL_SIGNATURE, KeyUsage.KEY_ENCIPHERMENT]
    )

    print(server_cert)

    # 3. 인증서 검증
    print("\n3. 인증서 검증")
    print("-" * 40)

    valid, reason = intermediate_ca.verify_certificate(server_cert)
    print(f"인증서 검증: {'유효' if valid else '무효'} - {reason}")

    # 4. 인증서 폐기
    print("\n4. 인증서 폐기")
    print("-" * 40)

    intermediate_ca.revoke_certificate(server_cert.serial_number,
                                        RevocationReason.KEY_COMPROMISE)

    # 폐기 후 검증
    valid, reason = intermediate_ca.verify_certificate(server_cert)
    print(f"폐기 후 검증: {'유효' if valid else '무효'} - {reason}")

    # 5. CRL 조회
    print("\n5. CRL (인증서 폐기 목록)")
    print("-" * 40)

    crl = intermediate_ca.crl
    print(f"발급자: {crl.issuer}")
    print(f"최종 갱신: {crl.last_update}")
    print(f"폐기된 인증서: {len(crl.revoked_certs)}개")

    for serial, info in crl.revoked_certs.items():
        print(f"  Serial {serial}: {info.reason.name} @ {info.revocation_date}")

    # 6. 체인 검증
    print("\n6. 인증서 체인 검증")
    print("-" * 40)

    # 새 인증서 발급
    new_cert = intermediate_ca.issue_certificate(
        subject="secure.example.com",
        public_key=PrivateKey().public_key
    )

    chain = [intermediate_ca.certificate, root_ca.certificate]
    valid, issues = pki.verify_chain(new_cert, chain)
    print(f"체인 검증: {'성공' if valid else '실패'}")
    for issue in issues:
        print(f"  ⚠️ {issue}")
