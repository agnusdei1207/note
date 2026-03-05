+++
title = "정보보안 3요소 (CIA Triad)"
date = "2026-03-04"
[extra]
categories = "studynotes-security"
+++

# 정보보안 3요소 (CIA Triad)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기밀성(Confidentiality), 무결성(Integrity), 가용성(Availability)이라는 정보보안의 3대 핵심 목표를 의미하며, 모든 보안 통제와 정책은 이 세 가지를 보장하기 위해 존재합니다.
> 2. **가치**: CIA Triad는 보안 투자의 우선순위를 결정하고, 위험 평가의 기준을 제시하며, 보안 사고의 영향도를 측정하는 보안 거버넌스의 핵심 프레임워크입니다.
> 3. **융합**: Parkerian Hexad(6요소)로 확장되며, GDPR, ISO 27001 등 모든 보안 표준의 근간을 이루고 AI 보안, 클라우드 보안 등 신기술 영역에서도 불변의 원칙으로 적용됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**CIA Triad**는 정보보안의 세 가지 핵심 목표를 삼각형 모양으로 시각화한 모델입니다. 각 요소는 상호 보완적이면서도 때로는 상충(Trade-off) 관계에 있으며, 조직의 비즈니스 목표와 위험 성향에 따라 균형점을 찾아야 합니다.

- **기밀성(Confidentiality)**: 인가된 사용자만 정보에 접근할 수 있음을 보장
- **무결성(Integrity)**: 정보가 무단으로 수정, 삭제, 생성되지 않음을 보장
- **가용성(Availability)**: 인가된 사용자가 필요할 때 언제든 정보에 접근 가능함을 보장

#### 2. 비유를 통한 이해
CIA Triad는 **'금고'**에 비유할 수 있습니다.
- **기밀성**: 금고의 잠금장치 - 열쇠가 있는 사람만 내용물을 볼 수 있음
- **무결성**: 금고의 내구성 - 누군가 금고를 억지로 열어 내용물을 바꾸지 못함
- **가용성**: 금고의 접근성 - 주인이 언제든 금고를 열어볼 수 있음

#### 3. 등장 배경 및 발전 과정
1. **초기 정보보안의 한계**: 1960~70년대에는 물리적 보안과 단순 접근 제어에 집중
2. **CIA Triad의 정립**: 1980년대 컴퓨터 보안의 발전과 함께 3요소가 보안의 핵심으로 자리잡음
3. **Parkerian Hexad로 확장**: 1998년 Donn Parker는 인증성(Authenticity), 책임추적성(Accountability), 부인방지(Non-repudiation)를 추가하여 6요소로 확장
4. **현대적 적용**: 클라우드, IoT, AI 환경에서도 CIA는 여전히 보안 설계의 출발점

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. CIA Triad 구성 요소 상세 분석

| 요소 | 정의 | 위협 요인 | 보호 기술 | 측정 지표 |
|:---|:---|:---|:---|:---|
| **기밀성** | 정보는 인가된 주체만 접근 가능 | 스누핑, 사회공학, 악성코드, 내부자 위협 | 암호화, 접근통제, 마스킹, DLP | 접근 시도 실패율, 암호화율 |
| **무결성** | 정보는 무단 변경되지 않음 | 데이터 변조, 중간자 공격, 랜섬웨어 | 해시, 전자서명, MAC, 버전관리 | 무결성 검증 성공률, 변조 탐지율 |
| **가용성** | 정보는 필요시 즉시 접근 가능 | DDoS, 랜섬웨어, 하드웨어 고장, 재해 | HA 설계, 백업, DRP, CDN | SLA 달성률, MTBF, MTTR |

#### 2. CIA Triad 균형 다이어그램

```text
                    [ Confidentiality ]
                          /\
                         /  \
                        /    \
                       /      \
                      /        \
                     /  CIA     \
                    /   Triad    \
                   /              \
                  /                \
    [ Integrity ]--------------------[ Availability ]
                   \
                    \  + 추가 요소 (Parkerian Hexad)
                     \   - Authenticity (인증성)
                      \  - Non-repudiation (부인방지)
                       \ - Accountability (책임추적성)

    <<< Trade-off 관계 예시 >>>

    기밀성 ↑ + 가용성 ↑ = 복잡한 인증 → 사용자 불편
    무결성 ↑ + 가용성 ↑ = 실시간 검증 → 성능 저하
    기밀성 ↑ + 무결성 ↑ = 강력한 암호화 → 오버헤드 증가
```

#### 3. 심층 동작 원리: CIA 보호 메커니즘

**① 기밀성 보호 프로세스 (5단계)**
```
1. 데이터 식별 → 민감도 분류 (공개/내부/기밀/극비)
2. 접근 제어 정책 → RBAC/ABAC 규칙 정의
3. 암호화 적용 → 저장/전송/사용 단계별 암호화
4. 모니터링 → 접근 로그 수집 및 이상 탐지
5. 대응 → 미인가 접근 시격리 및 차단
```

**② 무결성 검증 프로세스**
```python
import hashlib
import hmac

class IntegrityVerifier:
    """무결성 검증을 위한 해시 및 HMAC 구현"""

    def __init__(self, secret_key: bytes):
        self.secret_key = secret_key

    def compute_hash(self, data: bytes) -> str:
        """SHA-256 해시 계산 - 데이터 지문 생성"""
        return hashlib.sha256(data).hexdigest()

    def compute_hmac(self, data: bytes) -> str:
        """HMAC-SHA256 계산 - 키 기반 무결성 검증"""
        return hmac.new(
            self.secret_key,
            data,
            hashlib.sha256
        ).hexdigest()

    def verify_integrity(self, data: bytes, expected_hash: str) -> bool:
        """데이터 무결성 검증"""
        computed = self.compute_hash(data)
        return hmac.compare_digest(computed, expected_hash)

    def verify_hmac(self, data: bytes, expected_mac: str) -> bool:
        """HMAC 검증 - 메시지 인증 코드 확인"""
        computed = self.compute_hmac(data)
        return hmac.compare_digest(computed, expected_mac)

# 사용 예시
verifier = IntegrityVerifier(b"secret_key_12345")
original_data = b"Critical financial data: $1,000,000"
hash_value = verifier.compute_hash(original_data)

# 무결성 검증
assert verifier.verify_integrity(original_data, hash_value)

# 변조된 데이터 검증 (실패)
tampered_data = b"Critical financial data: $9,000,000"
assert not verifier.verify_integrity(tampered_data, hash_value)
```

**③ 가용성 보장 아키텍처**
```text
[ 가용성 보장 계층 구조 ]

Layer 4: Geographic Redundancy (지리적 이중화)
         ┌─────────────┐     ┌─────────────┐
         │ Data Center │     │ Data Center │
         │   (Seoul)   │◄───►│  (Busan)    │
         └─────────────┘     └─────────────┘

Layer 3: Load Balancing (부하 분산)
         ┌─────────────────────────────────┐
         │        Global Load Balancer      │
         │    (Anycast DNS + Health Check)  │
         └─────────────────────────────────┘

Layer 2: High Availability Clustering
         ┌───────────┐  ┌───────────┐  ┌───────────┐
         │  Node 1   │  │  Node 2   │  │  Node 3   │
         │ (Active)  │  │ (Active)  │  │ (Standby) │
         └───────────┘  └───────────┘  └───────────┘

Layer 1: System Redundancy (시스템 이중화)
         ┌──────────┐   ┌──────────┐
         │   PSU    │   │   NIC    │  (Redundant Components)
         │ (Dual)   │   │ (Bonding)│
         └──────────┘   └──────────┘
```

#### 4. 실무 적용: CIA 균형 점수판

```python
class CIABalanceScorer:
    """CIA 균형 점수 계산 및 분석"""

    def __init__(self):
        self.weights = {
            'confidentiality': 0.35,
            'integrity': 0.35,
            'availability': 0.30
        }

    def calculate_security_score(self, system_profile: dict) -> dict:
        """
        시스템의 CIA 보안 점수 계산

        Args:
            system_profile: {
                'encryption_level': 0-100,
                'access_control_maturity': 0-100,
                'integrity_verification_rate': 0-100,
                'backup_frequency_score': 0-100,
                'uptime_sla': 0-100,
                'dr_test_frequency': 0-100
            }
        """
        c_score = (
            system_profile['encryption_level'] * 0.5 +
            system_profile['access_control_maturity'] * 0.5
        )
        i_score = (
            system_profile['integrity_verification_rate'] * 0.6 +
            system_profile['backup_frequency_score'] * 0.4
        )
        a_score = (
            system_profile['uptime_sla'] * 0.7 +
            system_profile['dr_test_frequency'] * 0.3
        )

        overall = (
            c_score * self.weights['confidentiality'] +
            i_score * self.weights['integrity'] +
            a_score * self.weights['availability']
        )

        return {
            'confidentiality': round(c_score, 2),
            'integrity': round(i_score, 2),
            'availability': round(a_score, 2),
            'overall': round(overall, 2),
            'balance_factor': self._calculate_balance(c_score, i_score, a_score)
        }

    def _calculate_balance(self, c, i, a):
        """CIA 균형도 계산 (표준편차 기반)"""
        import statistics
        return round(100 - statistics.stdev([c, i, a]), 2)
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 산업별 CIA 우선순위 비교

| 산업 분야 | 최우선 요소 | 이유 | 대표적 위협 | 보안 통제 |
|:---|:---|:---|:---|:---|
| **금융** | 무결성 > 기밀성 > 가용성 | 거래 정확성이 핵심 | 트랜잭션 변조, 사기 | ACID, 전자서명, 감사 |
| **국방/군사** | 기밀성 > 무결성 > 가용성 | 정보 유출 즉시 국가안보 위협 | 첩보, 내부자 위협 | 높은 분류, 암호화 |
| **의료** | 가용성 > 기밀성 > 무결성 | 환자 생명이 걸린 데이터 접근 | 랜섬웨어, 시스템 장애 | HA, 백업, 빠른 복구 |
| **전자상거래** | 가용성 > 무결성 > 기밀성 | 서비스 중단 즉시 매출 손실 | DDoS, 결제 장애 | CDN, Auto-scaling |
| **공공기관** | 기밀성 ≒ 무결성 ≒ 가용성 | 균형적 보호 필요 | APT, 데이터 유출 | 종합 보안 체계 |

#### 2. CIA Trade-off 분석표

| 강화 요소 | 약화 위험 | 발생 문제 | 해결 방안 |
|:---|:---|:---|:---|
| 기밀성 강화 | 가용성 저하 | 복잡한 인증으로 업무 지연 | SSO, 적응형 인증 |
| 무결성 강화 | 가용성 저하 | 과도한 검증으로 성능 저하 | 비동기 검증, 캐싱 |
| 가용성 강화 | 기밀성/무결성 저하 | 보안 검사 생략 위험 | Zero Trust, 지속적 검증 |

#### 3. 과목 융합 관점 분석
- **네트워크 보안**: TLS 1.3은 기밀성(암호화), 무결성(AEAD), 가용성(0-RTT)을 모두 고려
- **데이터베이스**: ACID 트랜잭션은 무결성 보장, TDE는 기밀성, 복제는 가용성 담당
- **시스템 아키텍처**: 마이크로서비스는 서비스 격리로 기밀성, 분산 합의로 무결성, 오토스케일링으로 가용성 확보

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 하이브리드 클라우드 데이터 분류**
- 상황: 민감 데이터는 온프레미스, 일반 데이터는 클라우드
- 판단: 데이터 분류 후 기밀성 요구사항에 따라 저장 위치 결정
- CIA 적용: 기밀성 높은 데이터 → 온프레미스 + 강력한 암호화

**시나리오 2: 의료정보 시스템 랜섬웨어 대응**
- 상황: 랜섬웨어로 데이터 암호화, 환자 진료 중단 위기
- 판단: 가용성 최우선 → 백업 복구, 무결성 검증 후 서비스 재개
- CIA 적용: 3-2-1 백업 전략, offline backup, immutable backup

**시나리오 3: 핀테크 거래 시스템 설계**
- 상황: 초당 수만 건 거래 처리, 데이터 오류 즉시 금전 손실
- 판단: 무결성 최우선 → 분산 원장, 전자서명, 실시간 검증
- CIA 적용: 블록체인 기반 무결성, HSM 기반 기밀성, HA 클러스터링

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] 비즈니스 영향도 분석(BIA) 수행 여부
- [ ] 각 데이터 자산별 CIA 요구사항 정의
- [ ] Trade-off 발생 시 의사결정 프로세스 수립
- [ ] CIA 보안 지표에 대한 모니터링 체계 구축
- [ ] 정기적인 CIA 균형 점검 및 조정

#### 3. 안티패턴 (Anti-patterns)
- **극단적 기밀성 강조**: 모든 데이터를 최고 수준으로 분류 → 보안 예산 낭비, 업무 마비
- **가용성 맹신**: 99.99% 가용성 목표 → 과도한 인프라 비용, 보안 통제 약화
- **무결성 무시**: "백업이 있으니 괜찮다" → 실시간 데이터 변조 탐지 불가

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 효과 유형 | 내용 | 측정 지표 |
|:---|:---|:---|
| 정량적 | 보안 사고 감소 | 연간 사고 건수 50% 감소 |
| 정량적 | 복구 시간 단축 | MTTR 70% 감소 |
| 정성적 | 보안 의식 향상 | 전 직원 보안 교육 100% |
| 정성적 | 컴플라이언스 충족 | ISO 27001 인증 획득 |

#### 2. 미래 전망 및 진화 방향
- **AI 기반 CIA 균형 최적화**: 머신러닝으로 실시간 보안 상태 평가 및 자동 조정
- **양자 내성 CIA**: 양자 컴퓨팅 시대의 새로운 암호화 및 무결성 알고리즘
- **Zero Trust와 CIA**: "절대 신뢰 없음" 원칙으로 CIA 보장 강화

#### 3. 참고 표준/가이드
- **ISO/IEC 27001**: 정보보안 관리 체계 - CIA 요구사항 정의
- **NIST SP 800-53**: 보안 통제 - CIA 기반 통제 분류
- **GDPR Article 32**: 처리 보안 - 기밀성, 무결성, 가용성 보장 의무

---

### 관련 개념 맵 (Knowledge Graph)
- [위험 관리](@/studynotes/09_security/01_policy/_index.md) : CIA 기반 위험 평가 및 우선순위 결정
- [암호화](@/studynotes/09_security/02_crypto/encryption_algorithms.md) : 기밀성 보장을 위한 핵심 기술
- [해시 함수](@/studynotes/09_security/02_crypto/encryption_algorithms.md) : 무결성 검증을 위한 암호학적 도구
- [재해 복구](@/studynotes/09_security/01_policy/dr_bcp.md) : 가용성 보장을 위한 비상 계획
- [ISO 27001](@/studynotes/09_security/01_policy/isms_p.md) : CIA 기반 보안 관리 체계 표준

---

### 어린이를 위한 3줄 비유 설명
1. **비밀 지킴이(기밀성)**: 너의 일기장은 비밀번호를 아는 너만 읽을 수 있어요. 다른 친구들이 몰래 보지 못하게 하는 것이죠.
2. **진실 지킴이(무결성)**: 숙제를 했는데 친구가 장난으로 내용을 바꿔버리면 안 되죠? 내용이 그대로인지 확인하는 거예요.
3. **언제나 준비(가용성)**: 도서관에 책이 항상 있어야 빌릴 수 있죠? 필요할 때 언제든 사용할 수 있게 하는 거예요.
