+++
title = "제로 트러스트 아키텍처 (Zero Trust Architecture, ZTA)"
date = "2026-03-04"
[extra]
categories = "pe_exam-security"
+++

# 제로 트러스트 아키텍처 (Zero Trust Architecture, ZTA)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: "아무것도 신뢰하지 말고, 항상 검증하라(Never Trust, Always Verify)"는 철학 아래, 자산이 위치한 네트워크의 위치(내부/외부)에 관계없이 모든 접속 요청을 개별적으로 인증하고 지속적으로 검증하는 **데이터 중심의 동적 보안 모델**입니다.
> 2. **가치**: 기존 경계 보안(Perimeter Security)의 한계인 '침투 후 수평 이동(Lateral Movement)'을 마이크로 세그멘테이션과 최소 권한 원칙(Least Privilege)으로 원천 차단하여, 클라우드 확산 및 원격 근무 환경에서의 사이버 복원력(Resilience)을 극대화합니다.
> 3. **융합**: 신원 인식 프록시(IAP), 소프트웨어 정의 경계(SDP), 차세대 IAM, 그리고 실시간 가시성 확보를 위한 AI 기반 보안 관제(SOAR) 기술이 결합된 **보안 패러다임의 거대한 전환(Paradigm Shift)**입니다.

---

### Ⅰ. 개요 (Context & Background)
#### 1. 제로 트러스트의 개념 및 철학적 근간
제로 트러스트 아키텍처(ZTA)는 기업의 네트워크 경계 내부에 있는 자산은 안전하다는 고전적인 가정을 폐기합니다. 과거의 보안이 성벽을 높이 쌓아 외부인을 막는 '성곽 보안(Castle-and-Moat)'이었다면, 제로 트러스트는 성 내부에 들어온 사람이라도 매번 신분증을 제시하고, 방문하려는 방마다 허가를 받아야 하며, 조금이라도 이상한 행동을 하면 즉시 쫓겨나는 **'철저한 검문검색 체계'**입니다. NIST SP 800-207 표준에 따르면, 제로 트러스트는 특정 기술이 아니라 "자산, 서비스, 워크플로우에 대한 접근을 결정할 때 불확실성을 최소화하도록 설계된 일련의 개념과 원칙"입니다.

#### 2. 💡 비유를 통한 이해: 최고 보안 등급의 연구소
기존 보안은 연구소 정문에서 신분증을 확인하면 연구소 안의 모든 방을 돌아다닐 수 있는 구조였습니다. 하지만 **제로 트러스트**는 연구소 정문뿐만 아니라 복도마다 지문 인식을 해야 하고, 연구실 문을 열 때마다 홍채 인식을 해야 하며, 연구원이 평소와 다른 시간에 출근하거나 허가되지 않은 문서를 만지려 하면 즉시 경보가 울리고 모든 문이 잠기는 시스템입니다. 연구원(내부자)이라도 '기본적으로 믿지 않음'을 전제로 하며, 오직 현재 수행 중인 업무에 꼭 필요한 방(최소 권한)에만, 정해진 시간 동안만 머물 수 있게 합니다.

#### 3. 등장 배경: 왜 경계 보안은 실패했는가?
- **경계의 소멸 (Dissolution of Perimeter)**: SaaS(Office 365, Salesforce 등)와 IaaS(AWS, Azure)의 도입으로 기업 데이터가 사내 전산실 밖으로 나가면서, 방화벽이라는 물리적 울타리가 무의미해졌습니다.
- **공격 기법의 고도화 (Lateral Movement)**: 일단 한 번 내부망에 침투한 해커가 취약한 서버들을 타고 넘나들며 핵심 데이터베이스를 탈취하는 '수평 이동' 공격에 기존 보안은 속수무책이었습니다. (예: SolarWinds 공급망 공격)
- **원격 근무의 일상화**: VPN(Virtual Private Network)은 한 번 연결되면 내부망 전체에 대한 넓은 접근권을 부여하므로, 직원 단말기 하나만 해킹당해도 기업 전체가 위협에 노출되는 'VPN의 역설'이 발생했습니다.
- **데이터 중심 보안으로의 이동**: 인프라 장비를 보호하는 것보다, 기업의 핵심 자산인 '데이터' 자체를 보호하는 것이 비즈니스 생존의 핵심이 되었습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
#### 1. 제로 트러스트의 7대 기본 원칙 (NIST SP 800-207)
NIST는 제로 트러스트 구현을 위해 반드시 지켜야 할 7가지 원칙을 제시하고 있습니다.

| 원칙 | 상세 내용 | 비유 |
| :--- | :--- | :--- |
| **All Data/Computing is Resource** | 모든 데이터 원천과 컴퓨팅 서비스는 개별 자산으로 간주함. | 모든 방에 번호표 붙이기 |
| **Secured regardless of Location** | 네트워크 위치와 상관없이 모든 통신은 암호화되고 보호되어야 함. | 복도에서도 마스크 쓰기 |
| **Session-based Access** | 개별 리소스에 대한 접근 권한은 세션 단위로 부여됨. | 일회용 출입 카드 발급 |
| **Dynamic Policy** | 신원, 기기 상태, 행위 패턴 등 동적 속성에 따라 권한 결정. | 술 취한 사람은 출입 금지 |
| **Integrity/Posture Monitoring** | 모든 기기의 보안 상태를 지속적으로 측정하고 개선함. | 백신 맞은 사람만 입장 |
| **Authentication/Authorization** | 접근 허용 전 모든 자원에 대해 강력한 인증과 인가 수행. | 신분증과 지문 동시 확인 |
| **Visibility & Automation** | 자산의 상태와 통신 로그를 최대한 수집하여 보안 정책에 반영. | CCTV 실시간 감시 및 AI 분석 |

#### 2. 정교한 제로 트러스트 논리 아키텍처 다이어그램
제로 트러스트는 제어 평면(Control Plane)과 데이터 평면(Data Plane)을 분리하여, 인증되지 않은 트래픽이 자산 근처에도 오지 못하게 차단합니다.

```text
       [ Untrusted Zone ]                        [ Trusted / Resource Zone ]
   (User, Device, App Request)                       (Enterprise Assets)
            │                                               │
            ▼                                               ▼
┌──────────────────────┐                        ┌──────────────────────┐
│  [ Policy Enforcement │                        │    [ Enterprise     │
│       Point (PEP) ]   │                        │      Resources ]    │
└──────────┬───────────┘                        └──────────▲───────────┘
           │                                               │
           │  (Data Plane: Authenticated Traffic Only)     │
           └───────────────────────────────────────────────┘
                           ▲
                           │ (Grant/Deny Access)
      ┌────────────────────┴────────────────────┐
      │         [ Policy Administrator ]        │ <── Control Plane
      └────────────────────▲────────────────────┘
                           │ (Decision Logic)
      ┌────────────────────┴────────────────────┐
      │            [ Policy Engine ]            │
      └──────▲─────────────▲─────────────▲──────┘
             │             │             │
   ┌─────────┴──────┐ ┌────┴────────┐ ┌──┴──────────┐
   │ Identity (IAM) │ │ Device (MDM)│ │ Threat Intel│
   └────────────────┘ └─────────────┘ └─────────────┘
    (Contextual Inputs: Who, Where, When, What Device, Risk Score)
```

#### 3. 심층 동작 원리: 신뢰 지수(Trust Score) 기반의 동적 인가 프로세스
제로 트러스트의 핵심은 '신뢰'를 이진법(Yes/No)이 아닌 '점수(Score)'로 관리한다는 점입니다.
1. **Request Capture**: 사용자가 특정 데이터베이스에 접근을 시도하면 **PEP**가 이를 가로채고 **PE**에게 결정을 요청합니다.
2. **Contextual Evaluation**: PE는 다음의 팩터를 결합하여 실시간 신뢰 지수를 계산합니다.
   - **Identity**: MFA(다요소 인증)가 완료되었는가?
   - **Device Health**: 단말기에 최신 패치가 되어 있고 백신이 구동 중인가? (EDR 연동)
   - **Behavior**: 이 사용자가 평소에 이 시간에 이 데이터를 만졌는가? (UEBA 연동)
   - **Network**: 현재 접속 IP가 평소와 다른 해외 지역인가?
3. **Dynamic Grant**: 계산된 점수가 임계치를 넘으면 **PA**가 PEP에게 명령하여 해당 세션에 대해서만 일시적인 통신 터널(mTLS 등)을 열어줍니다.
4. **Continuous Monitoring**: 연결 중이라도 기기에서 바이러스가 발견되거나 행동이 이상해지면 세션은 즉시 파기됩니다.

#### 4. 핵심 알고리즘: 가중치 기반 신뢰 점수(Trust Scoring) Python 시뮬레이션
실무 환경에서는 복잡한 AI 모델을 사용하지만, 논리적 원리를 이해하기 위해 가중치 합산 방식의 정책 엔진 코드를 예시로 듭니다.

```python
def evaluate_trust_score(user_id, device_status, location_risk, behavior_score):
    """
    다양한 보안 컨텍스트를 입력받아 최종 접근 허용 여부를 결정하는 
    제로 트러스트 정책 엔진(Policy Engine) 시뮬레이션
    """
    # 1. 항목별 가중치 설정 (비즈니스 임팩트에 따라 조정)
    WEIGHTS = {
        'mfa_status': 0.4,
        'device_health': 0.3,
        'location': 0.1,
        'behavior': 0.2
    }

    # 2. 항목별 점수 산출 (0~100)
    scores = {
        'mfa_status': 100 if user_id['is_mfa_verified'] else 0,
        'device_health': 100 if device_status['is_patched'] and not device_status['has_malware'] else 30,
        'location': 100 if location_risk == "Home/Office" else 50,
        'behavior': behavior_score # UEBA 엔진에서 전달받은 값
    }

    # 3. 가중치 합산 (Weighted Average)
    final_score = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
    
    # 4. 정책 결정 (Threshold = 80)
    THRESHOLD = 80
    if final_score >= THRESHOLD:
        return True, final_score, "ACCESS_GRANTED"
    elif final_score >= 50:
        return False, final_score, "ADDITIONAL_MFA_REQUIRED"
    else:
        return False, final_score, "ACCESS_DENIED"

# 실행 예시: 신뢰할 수 없는 지역에서 보안 패치가 안 된 기기로 접속 시
user_ctx = {'is_mfa_verified': True}
device_ctx = {'is_patched': False, 'has_malware': False}
res, score, msg = evaluate_trust_score(user_ctx, device_ctx, "Foreign IP", 70)
print(f"Result: {res} | Score: {score} | Message: {msg}")
# Output: Result: False | Score: 62.0 | Message: ADDITIONAL_MFA_REQUIRED
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
#### 1. 전통적 경계 보안 vs 제로 트러스트 아키텍처
보안의 패러다임이 어떻게 바뀌었는지 기술적 관점에서 비교 분석합니다.

| 비교 항목 | 경계 보안 (Perimeter Security) | 제로 트러스트 (ZTA) | 비교 인사이트 |
| :--- | :--- | :--- | :--- |
| **핵심 철학** | "Trust but Verify" (일단 믿고 검증) | "Never Trust, Always Verify" (절대 불신) | 신뢰의 기반이 '위치'에서 '신원'으로 이동 |
| **접근 통제 방식** | IP, Port, VLAN 기반의 정적 ACL | 신원, 기기, 행위 기반의 동적 정책 | 네트워크 경계가 사용자마다 개별 생성됨 |
| **신뢰 영역** | 내부 네트워크(L2/L3)는 안전 구역 | 모든 네트워크는 위협 구역 (Internet-like) | 망 분리 개념이 논리적 격리로 진화 |
| **주요 기술** | VPN, Firewall, NAC | ZTNA, SDP, Micro-segmentation, IAM | HW 위주에서 SW 정의 보안으로 전환 |
| **수평 이동 대응** | 한 번 침투 시 전체 네트워크 노출 | 마이크로 세그멘테이션으로 철저 격리 | 침해 발생 시 피해 범위(Blast Radius) 최소화 |

#### 2. 과목 융합 관점 분석
- **네트워크 보안 (SDP, Software Defined Perimeter)**: ZTA를 구현하는 구체적인 기술인 SDP는 'Black Cloud' 개념을 사용합니다. 인증되지 않은 사용자에게는 서버의 IP 자체가 보이지 않도록(Port Stealth) 하여, 스캐닝 시도를 무력화합니다. 이는 **SPA(Single Packet Authorization)** 기술과 결합되어 인증된 패킷에만 방화벽 문을 일시적으로 여는 방식으로 동작합니다.
- **클라우드 컴퓨팅 및 SASE (Secure Access Service Edge)**: ZTA는 독립적으로 존재하지 않고 클라우드 환경의 SASE 아키텍처와 결합됩니다. 전 세계 어디서 접속하든 클라우드 엣지(Edge)에서 제로 트러스트 정책을 평가하고 가속화된 경로로 데이터를 전달하여, 보안과 성능(Latency)을 동시에 잡는 것이 핵심입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
#### 1. 기술사적 판단: 기존 VPN 환경을 ZTNA로 전환하는 단계적 전략
**[상황]** 글로벌 지사를 둔 대기업이 기존 VPN의 보안 취약점과 성능 한계를 해결하기 위해 제로 트러스트 도입을 결정했습니다.
**[전략적 대응 및 아키텍처 결정]**
1. **자산 식별 및 가시성 확보 (Step 1)**: 무작정 기술을 도입하기 전, 기업 내 모든 사용자, 기기, 데이터를 전수 조사하고 이들 간의 통신 흐름을 가시화합니다. (EAMS 및 자산 관리 시스템 연계)
2. **신원 기반 인증 강화 (Step 2)**: 단순 ID/PW 체계를 폐기하고, 생체 인증이나 FIDO2 기반의 강력한 **MFA**를 전사 도입합니다. 이 과정에서 통합 ID 관리(IAM) 체계를 클라우드와 연동(IDaaS)합니다.
3. **Pilot ZTNA 구축 (Step 3)**: 가장 위험한 외부 원격 접속자나 외주 개발자부터 기존 VPN을 걷어내고 **ZTNA(Zero Trust Network Access)** 솔루션을 적용합니다.
4. **마이크로 세그멘테이션 (Step 4)**: 서버 간(East-West) 통신에도 제로 트러스트를 적용하기 위해 가상화 환경에서 워크로드 단위의 격리 정책을 수립합니다.

#### 2. 도입 시 고려사항 (Checklist)
- **사용자 경험 (UX) 저하 방지**: 접속할 때마다 인증을 요구하면 생산성이 떨어질 수 있습니다. 이를 위해 **SSO(Single Sign-On)**와 **무자각 인증(Continuous Authentication)** 기술을 결합하여 보안성은 높이되 사용자 불편은 최소화해야 합니다.
- **레거시 시스템과의 연동**: 제로 트러스트 에이전트를 설치할 수 없는 오래된 장비(OT/IoT 등)에 대해서는 **신원 인식 프록시(IAP)**를 앞단에 두어 '논리적인 제로 트러스트 환경'으로 감싸는 전략이 필요합니다.
- **정책 관리의 복잡성**: 자산이 많아질수록 정책이 기하급수적으로 늘어납니다. 이를 수동으로 관리하는 것은 불가능하므로, **IaC(Infrastructure as Code)** 및 **Policy as Code**를 통해 정책을 자동화하고 버전 관리해야 합니다.

#### 3. 안티패턴 (Anti-patterns): 실패하는 제로 트러스트
- **"솔루션만 사면 된다"는 오해**: 제로 트러스트는 제품이 아닌 **전략이자 철학**입니다. 기존의 '믿는 방식'의 업무 프로세스를 그대로 둔 채 소프트웨어만 설치하면, 결국 예외 정책(Exception)이 늘어나 보안 구멍이 다시 생기게 됩니다.
- **전부 아니면 전무 (All-or-Nothing) 접근**: 한 번에 모든 시스템을 제로 트러스트로 바꾸려 하면 조직의 저항과 기술적 충돌로 반드시 실패합니다. 위험도가 높은 접점(Edge)부터 점진적으로 확장해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
#### 1. 정량적/정성적 기대효과 및 비즈니스 가치
제로 트러스트는 보안을 '비용'이 아닌 '비즈니스 가속기'로 변화시킵니다.

| 분류 | 세부 평가 지표 (KPI) | 기대 효과 및 수치 |
| :--- | :--- | :--- |
| **보안 강화** | 평균 침해 탐지 및 대응 시간 (MTTD/MTTR) | 피해 범위 제한을 통해 침해 사고 피해액 50% 이상 감소 |
| **운영 효율** | IT 인프라 가시성 및 통제력 | 전사 자산에 대한 100% 가시성 확보 및 중앙 집중형 정책 관리 |
| **비즈니스 민첩성** | 원격 근무 및 신규 사업 파트너 연동 속도 | 별도의 망 구성 없이 즉각적인 안전한 협업 환경 구축 (Time-to-Value 단축) |
| **컴플라이언스** | 법적 규제 준수율 (ISMS-P, GDPR 등) | 강력한 접근 통제 및 감사 로그 확보로 보안 인증 획득 용이 |

#### 2. 미래 전망: AI 기반 자율 제로 트러스트 (Autonomous ZT)
향후 제로 트러스트는 사람이 정책을 짜는 단계를 넘어설 것입니다. **AI/ML**이 수조 건의 로그를 분석하여 사용자별 '정상 행위 프로파일'을 생성하고, 평소와 1%만 다른 행동을 해도 실시간으로 신뢰 점수를 깎고 권한을 축소하는 **'지능형 적응형 보안(Adaptive Security)'**으로 진화할 것입니다. 또한 양자 컴퓨팅 시대에 대비한 양자 내성 암호(PQC)가 제어 평면의 인증 통신에 적용되어, 미래의 위협으로부터도 안전한 신뢰 체계를 구축하게 될 것입니다.

#### 3. 참고 표준 및 법적 가이드
- **NIST SP 800-207**: 제로 트러스트 아키텍처의 글로벌 표준 가이드라인.
- **미국 대통령령(Executive Order 14028)**: 미 연방정부의 제로 트러스트 도입 의무화 선언.
- **국가 제로트러스트 보안 가이드라인 1.0 (국정원/과학기술정보통신부)**: 한국형 제로 트러스트 모델 및 도입 가이드.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [SDP (Software Defined Perimeter)](./sdp.md): ZTA의 물리적/논리적 구현을 위한 핵심 네트워크 기술.
- [IAM (Identity & Access Management)](../../07_enterprise_systems/iam.md): 제로 트러스트의 새로운 경계가 되는 신원 관리 체계.
- [마이크로 세그멘테이션](../../03_network/micro_segmentation.md): 네트워크 내부의 수평 이동을 막는 격리 전략.
- [SASE (Secure Access Service Edge)](../../03_network/sase.md): 제로 트러스트와 클라우드 네트워크 기술의 융합 아키텍처.
- [FIDO2 및 MFA](./mfa.md): 제로 트러스트의 첫 단추인 강력한 사용자 인증 수단.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 제로 트러스트는 컴퓨터 세상의 아주 꼼꼼한 '도서관 관리원 아저씨'와 같아요.
2. 예전에는 도서관 문만 통과하면 모든 책을 볼 수 있었지만, 이제는 책 한 권을 꺼낼 때마다 아저씨한테 신분증을 보여주고 허락을 받아야 해요.
3. 아무리 친절해 보이는 사람이라도 규칙을 어기면 절대 책을 보여주지 않아서, 소중한 정보들이 도둑맞지 않게 아주 안전하게 지켜준답니다!
