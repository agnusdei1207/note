+++
title = "SABSA (Sherwood Applied Business Security Architecture)"
date = "2026-03-05"
[extra]
categories = "studynotes-security"
+++

# SABSA (Sherwood Applied Business Security Architecture)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비즈니스 중심의 엔터프라이즈 보안 아키텍처 프레임워크로, 6개 계층(물리~컨텍스트)과 6개 차원(자산~시간)의 매트릭스 구조로 보안을 체계화합니다.
> 2. **가치**: SABSA는 "비즈니스가 이끄는 보안"을 실현하여 보안 투자의 비즈니스 정렬을 보장하고, 위험 기반 의사결정을 지원합니다.
> 3. **융합**: TOGAF, Zachman, ISO 27001과 연동 가능하며, 클라우드 보안, Zero Trust 아키텍처 설계의 이론적 기반이 됩니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**SABSA(Sherwood Applied Business Security Architecture)**는 1995년 John Sherwood 등이 개발한 엔터프라이즈 보안 아키텍처 프레임워크입니다. "비즈니스 요구사항에서 시작하여 기술적 통제로 내려가는" Top-Down 접근법이 특징입니다.

**SABSA의 핵심 구조 - SABSA 매트릭스**:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SABSA 매트릭스 (6×6)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│              │   What    │   Why    │   How    │   Who    │  Where   │ When │
│    계층 ↓    │  (자산)   │ (동기)   │ (프로세스)│  (사람)  │ (위치)   │(시간)│
│   ───────────────────────────────────────────────────────────────────────  │
│    컨텍스트   │ 비즈니스  │ 비즈니스 │ 비즈니스 │ 비즈니스 │ 비즈니스 │비즈니스│
│  (Context)   │  개념     │  목표    │ 프로세스 │ 액터     │ 위치     │ 타임  │
│   ───────────────────────────────────────────────────────────────────────  │
│    개념적     │ 정보     │ 보안    │ 보안     │ 조직     │ 보안    │ 보안  │
│  (Conceptual)│  자산     │ 정책    │ 서비스   │ 구조     │ 도메인  │ 타임  │
│   ───────────────────────────────────────────────────────────────────────  │
│    논리적     │ 정보     │ 보안    │ 보안     │ 역할/    │ 보안    │ 보안  │
│   (Logical)  │  모델     │ 전략    │ 메커니즘 │ 책임     │ 네트워크│ 스케줄│
│   ───────────────────────────────────────────────────────────────────────  │
│    물리적     │ 데이터   │ 보안    │ 보안     │ 사람/   │ 보안    │ 보안  │
│  (Physical)  │  구조     │ 규칙    │ 도구     │ 조직     │ 인프라  │ 이벤트│
│   ───────────────────────────────────────────────────────────────────────  │
│    구현요소   │ 하드웨어 │ 보안    │ 보안     │ ID/     │ 보안    │ 보안  │
│(Component)   │  플랫폼   │ 표준    │ 메커니즘 │ 프로필  │ 장비    │ 스케줄│
│   ───────────────────────────────────────────────────────────────────────  │
│    운영       │ IT 서비스│ 보안    │ 보안     │ 운영    │ 운영    │ 운영  │
│  (Operational)│ 카탈로그 │ SOP     │ 절차     │ 프로세스 │ 절차    │ 프로세스│
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

    핵심 원칙:
    1. 비즈니스 주도 (Business Driven)
    2. 위험 기반 (Risk Based)
    3. 수명주기 지원 (Lifecycle Support)
    4. 적응형 (Adaptive)
```

#### 2. 6개 계층(Layers) 상세 설명

| 계층 | 명칭 | 초점 | 산출물 | 담당자 |
|:---|:---|:---|:---|:---|
| **1** | 컨텍스트(Contextual) | 비즈니스 환경 | 비즈니스 모델, 위험 평가 | 경영진 |
| **2** | 개념적(Conceptual) | 보안 개념 | 보안 정책, 자산 분류 | CISO |
| **3** | 논리적(Logical) | 논리적 설계 | 보안 아키텍처, 서비스 모델 | 보안 아키텍트 |
| **4** | 물리적(Physical) | 물리적 설계 | 기술 설계서, 토폴로지 | 보안 엔지니어 |
| **5** | 구현요소(Component) | 제품 선정 | 제품 목록, 구성 | 보안 관리자 |
| **6** | 운영(Operational) | 실제 운영 | SOP, 모니터링 | 보안 운영팀 |

#### 3. 6개 차원(Dimensions) 설명

| 차원 | 질문 | 예시 (컨텍스트 계층) | 예시 (물리 계층) |
|:---|:---|:---|:---|
| **What** | 무엇을 보호하는가? | 비즈니스 자산 | 데이터베이스, 파일 |
| **Why** | 왜 보호하는가? | 법적 의무, 경쟁력 | 규정 준수, CIA |
| **How** | 어떻게 보호하는가? | 비즈니스 프로세스 | 암호화, 방화벽 |
| **Who** | 누가 관여하는가? | 이해관계자 | 관리자, 사용자 |
| **Where** | 어디에 적용하는가? | 사업장, 시장 | 서버실, 클라우드 |
| **When** | 언제 적용하는가? | 사이클, 기한 | 실시간, 정기 |

#### 4. 비유를 통한 이해
SABSA는 **'건축 설계'**에 비유할 수 있습니다.
- **컨텍스트 계층**: 건물의 용도 결정 (주거? 상업?)
- **개념적 계층**: 건축 컨셉 (현대식? 클래식?)
- **논리적 계층**: 설계도면 (평면도, 단면도)
- **물리적 계층**: 시공 상세도 (자재, 배치)
- **구현요소 계층**: 실제 자재 구매 (벽돌, 철근)
- **운영 계층**: 건물 유지관리 (청소, 수리)

#### 5. 등장 배경 및 발전 과정
1. **1995년**: Sherwood Consulting Group에서 SABSA 개발 시작
2. **2000년대 초**: SABSA 방법론 공식화, 영국 정부 채택
3. **2005년**: The SABSA Institute 설립
4. **2010년대**: TOGAF, ISO 27001과 통합 가이드 발표
5. **현재**: 클라우드, Zero Trust, DevSecOps 아키텍처에 적용

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. SABSA 보안 아키텍처 수명주기

```text
<<< SABSA 수명주기 (Lifecycle) >>>

    ┌────────────────────────────────────────────────────────────────────────┐
    │                                                                        │
    │        ┌─────────────────────────────────────────────────────────┐    │
    │        │                    1. Strategy                           │    │
    │        │         (전략 수립 - 비즈니스 요구사항 분석)             │    │
    │        │                                                       │    │
    │        │  - 비즈니스 목표 이해                                  │    │
    │        │  - 위험 평가                                           │    │
    │        │  - 보안 목표 정의                                       │    │
    │        └─────────────────────────────────────────────────────────┘    │
    │                              │                                         │
    │                              ▼                                         │
    │        ┌─────────────────────────────────────────────────────────┐    │
    │        │                    2. Design                             │    │
    │        │         (설계 - 아키텍처 개발)                           │    │
    │        │                                                       │    │
    │        │  - 개념적 아키텍처                                      │    │
    │        │  - 논리적 아키텍처                                      │    │
    │        │  - 물리적 아키텍처                                      │    │
    │        └─────────────────────────────────────────────────────────┘    │
    │                              │                                         │
    │                              ▼                                         │
    │        ┌─────────────────────────────────────────────────────────┐    │
    │        │                    3. Implementation                     │    │
    │        │         (구현 - 솔루션 배포)                             │    │
    │        │                                                       │    │
    │        │  - 구현요소 선정                                       │    │
    │        │  - 통합 및 테스트                                      │    │
    │        │  - 마이그레이션                                        │    │
    │        └─────────────────────────────────────────────────────────┘    │
    │                              │                                         │
    │                              ▼                                         │
    │        ┌─────────────────────────────────────────────────────────┐    │
    │        │                    4. Management                         │    │
    │        │         (관리 - 운영 및 모니터링)                       │    │
    │        │                                                       │    │
    │        │  - 서비스 운영                                         │    │
    │        │  - 성능 모니터링                                       │    │
    │        │  - 지속적 개선                                         │    │
    │        └─────────────────────────────────────────────────────────┘    │
    │                              │                                         │
    │                              ▼                                         │
    │        ┌─────────────────────────────────────────────────────────┐    │
    │        │                    5. Assurance                          │    │
    │        │         (보증 - 감사 및 검증)                           │    │
    │        │                                                       │    │
    │        │  - 컴플라이언스 검토                                   │    │
    │        │  - 침투 테스트                                        │    │
    │        │  - 감사 보고                                          │    │
    │        └─────────────────────────────────────────────────────────┘    │
    │                              │                                         │
    │                              └──────────────────────────► (1. 전략으로)│
    │                                                                        │
    └────────────────────────────────────────────────────────────────────────┘
```

#### 2. SABSA 보안 서비스 카탈로그

```text
<<< SABSA 보안 서비스 분류 >>>

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                        보안 서비스 계층구조                             │
    ├─────────────────────────────────────────────────────────────────────────┤
    │                                                                         │
    │  1. 인증 서비스 (Authentication Services)                               │
    │  ┌─────────────────────────────────────────────────────────────────┐   │
    │  │  - 사용자 인증 (User Authentication)                             │   │
    │  │  - 시스템 인증 (System Authentication)                           │   │
    │  │  - MFA (Multi-Factor Authentication)                             │   │
    │  │  - SSO (Single Sign-On)                                          │   │
    │  │  - FIDO2/WebAuthn                                                │   │
    │  └─────────────────────────────────────────────────────────────────┘   │
    │                                                                         │
    │  2. 인가 서비스 (Authorization Services)                                │
    │  ┌─────────────────────────────────────────────────────────────────┐   │
    │  │  - 접근 제어 (Access Control) - RBAC/ABAC/PBAC                   │   │
    │  │  - 권한 관리 (Privilege Management)                              │   │
    │  │  - 정책 결정점 (PDP - Policy Decision Point)                     │   │
    │  │  - 정책 시행점 (PEP - Policy Enforcement Point)                  │   │
    │  └─────────────────────────────────────────────────────────────────┘   │
    │                                                                         │
    │  3. 기밀성 서비스 (Confidentiality Services)                            │
    │  ┌─────────────────────────────────────────────────────────────────┐   │
    │  │  - 저장 데이터 암호화 (Data at Rest Encryption)                  │   │
    │  │  - 전송 데이터 암호화 (Data in Transit Encryption)               │   │
    │  │  - 사용 중 데이터 보호 (Data in Use Protection)                 │   │
    │  │  - 키 관리 (Key Management)                                      │   │
    │  │  - DLP (Data Loss Prevention)                                    │   │
    │  └─────────────────────────────────────────────────────────────────┘   │
    │                                                                         │
    │  4. 무결성 서비스 (Integrity Services)                                  │
    │  ┌─────────────────────────────────────────────────────────────────┐   │
    │  │  - 해시/체크섬 (Hashing/Checksum)                                │   │
    │  │  - 디지털 서명 (Digital Signature)                               │   │
    │  │  - 버전 관리 (Version Control)                                   │   │
    │  │  - 변경 관리 (Change Management)                                 │   │
    │  │  - 코드 서명 (Code Signing)                                      │   │
    │  └─────────────────────────────────────────────────────────────────┘   │
    │                                                                         │
    │  5. 가용성 서비스 (Availability Services)                               │
    │  ┌─────────────────────────────────────────────────────────────────┐   │
    │  │  - 고가용성 (High Availability)                                  │   │
    │  │  - 재해 복구 (Disaster Recovery)                                 │   │
    │  │  - 백업 (Backup)                                                 │   │
    │  │  - DDoS 방어 (DDoS Protection)                                   │   │
    │  │  - 로드 밸런싱 (Load Balancing)                                  │   │
    │  └─────────────────────────────────────────────────────────────────┘   │
    │                                                                         │
    │  6. 부인방지 서비스 (Non-repudiation Services)                          │
    │  ┌─────────────────────────────────────────────────────────────────┐   │
    │  │  - 전자서명 (Electronic Signature)                               │   │
    │  │  - 타임스탬프 (Timestamping)                                     │   │
    │  │  - 감사 로그 (Audit Logging)                                     │   │
    │  │  - 블록체인 증명 (Blockchain Proof)                              │   │
    │  └─────────────────────────────────────────────────────────────────┘   │
    │                                                                         │
    │  7. 보안 관리 서비스 (Security Management Services)                     │
    │  ┌─────────────────────────────────────────────────────────────────┐   │
    │  │  - SIEM (Security Information & Event Management)               │   │
    │  │  - 취약점 관리 (Vulnerability Management)                        │   │
    │  │  - 위협 인텔리전스 (Threat Intelligence)                         │   │
    │  │  - 인시던트 대응 (Incident Response)                             │   │
    │  │  - 보안 오케스트레이션 (SOAR)                                    │   │
    │  └─────────────────────────────────────────────────────────────────┘   │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
```

#### 3. Python 구현: SABSA 매트릭스 관리

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import json

class SABSALayer(Enum):
    """SABSA 6계층"""
    CONTEXTUAL = "컨텍스트"
    CONCEPTUAL = "개념적"
    LOGICAL = "논리적"
    PHYSICAL = "물리적"
    COMPONENT = "구현요소"
    OPERATIONAL = "운영"

class SABSADimension(Enum):
    """SABSA 6차원"""
    WHAT = "What (자산)"
    WHY = "Why (동기)"
    HOW = "How (프로세스)"
    WHO = "Who (사람)"
    WHERE = "Where (위치)"
    WHEN = "When (시간)"

@dataclass
class SABSAElement:
    """SABSA 매트릭스 요소"""
    layer: SABSALayer
    dimension: SABSADimension
    content: str
    description: str = ""
    owner: str = ""
    status: str = "draft"  # draft, review, approved

    def to_dict(self) -> Dict:
        return {
            'layer': self.layer.value,
            'dimension': self.dimension.value,
            'content': self.content,
            'description': self.description,
            'owner': self.owner,
            'status': self.status
        }

@dataclass
class BusinessDriver:
    """비즈니스 구동요인"""
    driver_id: str
    name: str
    description: str
    priority: int  # 1-5
    related_assets: List[str] = field(default_factory=list)

@dataclass
class SecurityService:
    """보안 서비스"""
    service_id: str
    name: str
    category: str  # 인증, 인가, 기밀성, 무결성, 가용성, 부인방지, 관리
    description: str
    sla_target: str = ""
    implementation_status: str = "planned"  # planned, implementing, operational

@dataclass
class SecurityAttribute:
    """보안 속성 (CIA + 확장)"""
    name: str
    requirement_level: int  # 1-5
    justification: str
    metrics: List[str] = field(default_factory=list)

class SABSAArchitecture:
    """SABSA 아키텍처 관리"""

    def __init__(self, organization_name: str):
        self.organization_name = organization_name
        self.matrix: Dict[Tuple[SABSALayer, SABSADimension], SABSAElement] = {}
        self.business_drivers: Dict[str, BusinessDriver] = {}
        self.security_services: Dict[str, SecurityService] = {}
        self.security_attributes: Dict[str, SecurityAttribute] = {}

    def set_matrix_element(self, element: SABSAElement):
        """매트릭스 요소 설정"""
        key = (element.layer, element.dimension)
        self.matrix[key] = element

    def get_matrix_element(self, layer: SABSALayer,
                           dimension: SABSADimension) -> Optional[SABSAElement]:
        """매트릭스 요소 조회"""
        return self.matrix.get((layer, dimension))

    def get_layer_elements(self, layer: SABSALayer) -> List[SABSAElement]:
        """특정 계층의 모든 요소 조회"""
        return [elem for (l, d), elem in self.matrix.items() if l == layer]

    def get_dimension_elements(self, dimension: SABSADimension) -> List[SABSAElement]:
        """특정 차원의 모든 요소 조회"""
        return [elem for (l, d), elem in self.matrix.items() if d == dimension]

    def add_business_driver(self, driver: BusinessDriver):
        """비즈니스 구동요인 추가"""
        self.business_drivers[driver.driver_id] = driver

    def add_security_service(self, service: SecurityService):
        """보안 서비스 추가"""
        self.security_services[service.service_id] = service

    def set_security_attribute(self, asset_name: str, attribute: SecurityAttribute):
        """보안 속성 설정"""
        self.security_attributes[asset_name] = attribute

    def generate_architecture_view(self, layer: SABSALayer) -> Dict:
        """특정 계층의 아키텍처 뷰 생성"""
        elements = self.get_layer_elements(layer)

        view = {
            'layer': layer.value,
            'organization': self.organization_name,
            'elements': {},
            'completeness': 0
        }

        for dim in SABSADimension:
            elem = self.get_matrix_element(layer, dim)
            view['elements'][dim.value] = elem.to_dict() if elem else None

        # 완성도 계산
        filled = sum(1 for e in view['elements'].values() if e is not None)
        view['completeness'] = filled / len(SABSADimension) * 100

        return view

    def trace_requirement_to_implementation(self, asset_name: str) -> Dict:
        """요구사항 → 구현 추적"""
        trace = {
            'asset': asset_name,
            'contextual': {},
            'conceptual': {},
            'logical': {},
            'physical': {},
            'component': {},
            'operational': {}
        }

        # 각 계층에서 해당 자산 관련 요소 추적
        for layer in SABSALayer:
            for dim in SABSADimension:
                elem = self.get_matrix_element(layer, dim)
                if elem and asset_name.lower() in elem.content.lower():
                    trace[layer.value.lower()][dim.value] = elem.content

        return trace

    def assess_coverage(self) -> Dict:
        """아키텍처 커버리지 평가"""
        total_cells = len(SABSALayer) * len(SABSADimension)
        filled_cells = len(self.matrix)

        by_layer = {}
        for layer in SABSALayer:
            elements = self.get_layer_elements(layer)
            by_layer[layer.value] = {
                'filled': len(elements),
                'total': len(SABSADimension),
                'percentage': len(elements) / len(SABSADimension) * 100
            }

        by_dimension = {}
        for dim in SABSADimension:
            elements = self.get_dimension_elements(dim)
            by_dimension[dim.value] = {
                'filled': len(elements),
                'total': len(SABSALayer),
                'percentage': len(elements) / len(SABSALayer) * 100
            }

        return {
            'overall_coverage': filled_cells / total_cells * 100,
            'by_layer': by_layer,
            'by_dimension': by_dimension,
            'missing_elements': self._identify_missing_elements()
        }

    def _identify_missing_elements(self) -> List[Tuple[str, str]]:
        """누락된 요소 식별"""
        missing = []
        for layer in SABSALayer:
            for dim in SABSADimension:
                if (layer, dim) not in self.matrix:
                    missing.append((layer.value, dim.value))
        return missing

    def export_to_json(self) -> str:
        """JSON으로 내보내기"""
        data = {
            'organization': self.organization_name,
            'matrix': [elem.to_dict() for elem in self.matrix.values()],
            'business_drivers': {k: vars(v) for k, v in self.business_drivers.items()},
            'security_services': {k: vars(v) for k, v in self.security_services.items()},
            'security_attributes': {k: vars(v) for k, v in self.security_attributes.items()}
        }
        return json.dumps(data, ensure_ascii=False, indent=2)


# 사용 예시
if __name__ == "__main__":
    # SABSA 아키텍처 생성
    arch = SABSAArchitecture("ABC 금융회사")

    # 1. 컨텍스트 계층 정의
    arch.set_matrix_element(SABSAElement(
        layer=SABSALayer.CONTEXTUAL,
        dimension=SABSADimension.WHAT,
        content="고객 금융 데이터, 거래 시스템, 모바일 뱅킹 앱",
        description="핵심 비즈니스 자산",
        owner="CBO"
    ))

    arch.set_matrix_element(SABSAElement(
        layer=SABSALayer.CONTEXTUAL,
        dimension=SABSADimension.WHY,
        content="금융감독원 규정 준수, 고객 신뢰 유지, 경쟁력 확보",
        description="보안의 비즈니스 이유",
        owner="CEO"
    ))

    arch.set_matrix_element(SABSAElement(
        layer=SABSALayer.CONTEXTUAL,
        dimension=SABSADimension.HOW,
        content="계좌 이체, 대출 심사, 고객 상담, 리스크 관리",
        description="핵심 비즈니스 프로세스",
        owner="COO"
    ))

    # 2. 개념적 계층 정의
    arch.set_matrix_element(SABSAElement(
        layer=SABSALayer.CONCEPTUAL,
        dimension=SABSADimension.WHAT,
        content="고객 PII, 계좌 정보, 거래 내역, 신용 점수",
        description="정보 자산 분류",
        owner="CISO"
    ))

    arch.set_matrix_element(SABSAElement(
        layer=SABSALayer.CONCEPTUAL,
        dimension=SABSADimension.WHY,
        content="CIA 보장, 법적 의무 준수, 내부통제",
        description="보안 정책 목표",
        owner="CISO"
    ))

    # 3. 논리적 계층 정의
    arch.set_matrix_element(SABSAElement(
        layer=SABSALayer.LOGICAL,
        dimension=SABSADimension.WHAT,
        content="고객 DB 스키마, 트랜잭션 로그 포맷, API 데이터 모델",
        description="정보 모델",
        owner="보안 아키텍트"
    ))

    arch.set_matrix_element(SABSAElement(
        layer=SABSALayer.LOGICAL,
        dimension=SABSADimension.HOW,
        content="TLS 1.3, AES-256, MFA, RBAC, WAF, EDR",
        description="보안 메커니즘",
        owner="보안 아키텍트"
    ))

    # 4. 물리적 계층 정의
    arch.set_matrix_element(SABSAElement(
        layer=SABSALayer.PHYSICAL,
        dimension=SABSADimension.WHERE,
        content="IDC 2개소(서울/부산), AWS ap-northeast-2, CDN",
        description="물리적 위치",
        owner="인프라 팀장"
    ))

    arch.set_matrix_element(SABSAElement(
        layer=SABSALayer.PHYSICAL,
        dimension=SABSADimension.HOW,
        content="Palo Alto NGFW, Imperva WAF, CrowdStrike EDR",
        description="보안 도구",
        owner="보안 엔지니어"
    ))

    # 5. 비즈니스 구동요인 추가
    arch.add_business_driver(BusinessDriver(
        driver_id="BD-001",
        name="디지털 뱅킹 혁신",
        description="모바일/인터넷 뱅킹 서비스 확대",
        priority=5,
        related_assets=["모바일 앱", "API 게이트웨이"]
    ))

    arch.add_business_driver(BusinessDriver(
        driver_id="BD-002",
        name="규제 준수",
        description="DLP, 전자금융감독규정 준수",
        priority=5,
        related_assets=["고객 데이터", "거래 시스템"]
    ))

    # 6. 보안 서비스 추가
    arch.add_security_service(SecurityService(
        service_id="SS-001",
        name="엔터프라이즈 MFA",
        category="인증",
        description="모든 사용자 계정에 MFA 적용",
        sla_target="99.9% 가용성",
        implementation_status="operational"
    ))

    arch.add_security_service(SecurityService(
        service_id="SS-002",
        name="데이터 암호화 서비스",
        category="기밀성",
        description="전송/저장 데이터 암호화",
        sla_target="100% 암호화 적용",
        implementation_status="implementing"
    ))

    # 7. 보안 속성 설정
    arch.set_security_attribute("고객 PII", SecurityAttribute(
        name="CIA 요구사항",
        requirement_level=5,
        justification="개인정보보호법 위반 시 벌금 최대 3%",
        metrics=["암호화율", "접근 로그 기록률", "마스킹 적용률"]
    ))

    # 아키텍처 뷰 생성
    print("=" * 70)
    print("SABSA 아키텍처 분석 결과")
    print("=" * 70)

    # 컨텍스트 계층 뷰
    view = arch.generate_architecture_view(SABSALayer.CONTEXTUAL)
    print(f"\n[컨텍스트 계층] - 완성도: {view['completeness']:.0f}%")
    for dim, elem in view['elements'].items():
        if elem:
            print(f"  {dim}: {elem['content']}")

    # 커버리지 평가
    coverage = arch.assess_coverage()
    print(f"\n전체 커버리지: {coverage['overall_coverage']:.1f}%")
    print("\n계층별 커버리지:")
    for layer, data in coverage['by_layer'].items():
        print(f"  {layer}: {data['percentage']:.0f}%")

    # 요구사항 추적
    print("\n요구사항 추적 (고객 PII):")
    trace = arch.trace_requirement_to_implementation("고객")
    for layer, dims in trace.items():
        if dims:
            print(f"  [{layer}]")
            for dim, content in dims.items():
                print(f"    {dim}: {content}")

    # 보안 서비스 현황
    print("\n보안 서비스 현황:")
    for svc_id, svc in arch.security_services.items():
        print(f"  [{svc.category}] {svc.name}: {svc.implementation_status}")
```

#### 4. SABSA vs 다른 아키텍처 프레임워크 비교

| 특징 | SABSA | TOGAF | Zachman | ISO 27001 |
|:---|:---|:---|:---|:---|
| **초점** | 보안 특화 | 전체 EA | 분류 체계 | ISMS |
| **접근법** | 비즈니스 → 기술 | 비즈니스 → IT | 6×6 매트릭스 | PDCA |
| **계층 수** | 6개 | 4개 (ADM) | 6개 | - |
| **인증** | SABSA 인증 | TOGAF 인증 | 없음 | ISO 인증 |
| **난이도** | 중간 | 높음 | 낮음 | 중간 |

---

### III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. SABSA와 TOGAF 통합

| TOGAF ADM 단계 | SABSA 연계 | 산출물 |
|:---|:---|:---|
| **A. 아키텍처 비전** | 컨텍스트 계층 | 비즈니스 위험, 보안 목표 |
| **B. 비즈니스 아키텍처** | 컨텍스트 + 개념적 | 비즈니스 프로세스 보안 |
| **C. 정보시스템 아키텍처** | 개념적 + 논리적 | 보안 서비스 모델 |
| **D. 기술 아키텍처** | 논리적 + 물리적 | 보안 인프라 설계 |
| **E. 기회 및 솔루션** | 구현요소 | 보안 제품 선정 |
| **F. 마이그레이션 계획** | 운영 | 보안 전환 계획 |

#### 2. SABSA와 ISO 27001 매핑

| ISO 27001 Clause | SABSA 계층 | 설명 |
|:---|:---|:---|
| **4. 조직 상황** | 컨텍스트 | 이해관계자, 외부 이슈 |
| **5. 리더십** | 컨텍스트 | 보안 거버넌스 |
| **6. 계획** | 개념적 | 위험 처리 계획 |
| **7. 지원** | 논리적/물리적 | 역량, 인식, 문서화 |
| **8. 운영** | 구현요소/운영 | 통제 구현 |
| **9. 성과 평가** | 운영 | 모니터링, 측정 |
| **10. 개선** | 전 계층 | 지속적 개선 |

#### 3. 과목 융합 관점 분석
- **시스템 아키텍처**: SABSA를 엔터프라이즈 아키텍처의 보안 레이어로 통합
- **네트워크 보안**: SABSA 물리적 계층에서 네트워크 보안 도메인 정의
- **애플리케이션 보안**: SABSA 논리적 계층에서 앱 보안 서비스 정의
- **클라우드 보안**: SABSA의 WHERE 차원에서 클라우드 보안 도메인 정의
- **컴플라이언스**: SABSA WHY 차원에서 규제 요구사항 추적

---

### IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 금융사 디지털 전환 보안 아키텍처**
- 상황: 오픈뱅킹, API 플랫폼 구축
- SABSA 적용:
  - 컨텍스트: 디지털 혁신 비즈니스 요구사항
  - 개념적: API 보안, OAuth 2.0
  - 논리적: API Gateway, OAuth 서버
  - 물리적: Kong/Apigee, Okta/Auth0
- 판단: SABSA로 계층별 일관성 있는 아키텍처 수립

**시나리오 2: 클라우드 마이그레이션 보안 설계**
- 상황: 온프레미스 → AWS/Azure 이관
- SABSA 적용:
  - WHERE: 클라우드 보안 도메인 정의
  - HOW: CSPM, CWPP, IAM
  - WHO: CSP와의 책임 분담
- 판단: SABSA로 클라우드 보안 아키텍처 체계화

**시나리오 3: Zero Trust 아키텍처 설계**
- 상황: 경계 기반 보안 → Zero Trust 전환
- SABSA 적용:
  - WHY: "절대 신뢰 없음" 정책
  - HOW: 마이크로 세그멘테이션, 지속적 검증
  - WHO: 모든 사용자/디바이스/서비스
- 판단: SABSA로 Zero Trust 이행 로드맵 수립

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] 경영진 스폰서십 확보 (SABSA는 비즈니스 기반)
- [ ] SABSA 교육 및 역량 확보
- [ ] 기존 EA(TOGAF)와의 통합 방안
- [ ] 매트릭스 요소별 담당자 지정
- [ ] 정기적 아키텍처 검토 프로세스
- [ ] 도구(Tool) 선정 (아키텍처 저장소)

#### 3. 안티패턴 (Anti-patterns)
- **기술 중심 접근**: 컨텍스트 계층 없이 물리적 계층부터 시작
- **부분적 적용**: 일부 계층만 정의하고 중단
- **문서화만**: 실제 구현과 아키텍처 불일치
- **정적 유지**: 비즈니스 변화에 아키텍처 미반영

---

### V. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | 내용 | 측정 방법 |
|:---|:---|:---|
| 보안-비즈니스 정렬 | 보안 투자의 비즈니스 기여도 증가 | 비즈니스 만족도 |
| 아키텍처 일관성 | 계층 간 추적 가능성 확보 | 요구사항 추적률 |
| 위험 기반 의사결정 | 체계적 위험 분석 | 위험 처리 효율성 |
| 컴플라이언스 | 규제 요건 체계적 대응 | 감사 지적 감소 |

#### 2. 미래 전망 및 진화 방향
- **DevSecOps 통합**: SABSA를 CI/CD 파이프라인에 통합
- **클라우드 네이티브**: Cloud Security Architecture로 확장
- **AI/ML 기반**: 자동화된 아키텍처 분석 및 추천
- **실시간 아키텍처**: 동적 환경에서 실시간 아키텍처 업데이트

#### 3. 참고 표준/가이드
- **The SABSA Institute**: SABSA 공식 방법론
- **Open Group**: TOGAF-SABSA 통합 가이드
- **ISO/IEC 27001**: ISMS와 SABSA 매핑
- **NIST SP 800-160**: 시스템 보안 엔지니어링

---

### 관련 개념 맵 (Knowledge Graph)
- [보안 아키텍처](@/studynotes/09_security/01_policy/security_architecture.md) : SABSA의 일반화
- [심층 방어](@/studynotes/09_security/01_policy/defense_in_depth.md) : SABSA HOW 차원의 구현
- [Zero Trust](@/studynotes/09_security/01_policy/zero_trust_architecture.md) : SABSA 기반 설계 가능
- [보안 정책](@/studynotes/09_security/01_policy/security_policy.md) : SABSA WHY 차원
- [위험 관리](@/studynotes/09_security/01_policy/risk_management.md) : SABSA 컨텍스트 계층

---

### 어린이를 위한 3줄 비유 설명
1. **설계도**: 집을 지을 때 방 하나하나 그리는 것처럼, 보안도 계층별로 그리는 거예요.
2. **위에서 아래로**: "어떤 집을 지을까?"(비즈니스)부터 "벽돌은 무엇을 쓸까?"(기술)까지 내려가요.
3. **6가지 질문**: 무엇을, 왜, 어떻게, 누가, 어디서, 언제? 6가지를 계층마다 물어봐요.
