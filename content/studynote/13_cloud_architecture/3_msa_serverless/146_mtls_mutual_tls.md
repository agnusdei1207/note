+++
weight = 146
title = "mTLS (상호 TLS 인증)"
date = "2024-03-20"
[extra]
categories = ["cloud-architecture", "msa", "security"]
+++

## 핵심 인사이트 (3줄 요약)
1. 클라이언트만 서버를 인증하는 일반 TLS와 달리, 서버와 클라이언트가 서로의 인증서를 확인하여 양방향 신뢰를 구축하는 보안 프로토콜입니다.
2. 마이크로서비스 아키텍처(MSA) 내부의 서비스 간 통신(East-West)에서 비인가된 서비스의 접근을 원천 차단하는 제로 트러스트(Zero Trust)의 핵심 기술입니다.
3. 서비스 메시(Istio, Linkerd)를 통해 애플리케이션 코드 수정 없이 인프라 계층(사이드카)에서 자동화된 인증서 관리와 암호화를 구현합니다.

### Ⅰ. 개요 (Context & Background)
기존의 경계 보안(Perimeter Security) 환경에서는 내부망에 들어온 트래픽을 신뢰했지만, 클라우드 네이티브 환경에서는 내부 서비스 간의 무단 접근과 스니핑 위협이 커졌습니다. mTLS(Mutual TLS)는 "아무도 믿지 마라"는 제로 트러스트 철학을 기반으로, 내부 네트워크의 모든 통신 세션마다 상호 인증을 강제하여 데이터 기밀성과 서비스 무결성을 보장합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
[ Service A (Client) ]     [ Handshake / Auth ]      [ Service B (Server) ]
+--------------------+                               +--------------------+
| [ Certificate A ]  | 1. Server Cert Request ---->  | [ Certificate B ]  |
| [ Private Key A ]  | <---- 2. Server Cert Send --  | [ Private Key B ]  |
+---------|----------+                               +---------|----------+
          |            3. Client Cert Send ---->               |
          |            <---- 4. Verify & Encrypt Session ----> |
          +----------------------------------------------------+
                   ( Bidirectional Authentication )
```

**Bilingual Key Components:**
- **양방향 인증 (Mutual Auth):** 클라이언트와 서버가 각자 발급받은 인증서를 상호 검증하여 신원을 확인합니다.
- **인증서 발급 및 갱신 (CA & Rotation):** 서비스 메시의 컨트롤 플레인이 각 마이크로서비스에 짧은 주기의 인증서를 자동으로 발급하고 교체합니다.
- **세션 암호화 (Session Encryption):** 인증 완료 후 대칭 키를 생성하여 전송되는 모든 데이터를 암호화합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 일반 TLS (One-way) | 상호 TLS (mTLS) |
| :--- | :--- | :--- |
| **인증 방향** | 단방향 (클라이언트가 서버 확인) | 양방향 (서버도 클라이언트 확인) |
| **주요 용도** | 퍼블릭 웹 서비스 (HTTPS) | MSA 내부 통신, B2B 전용선 |
| **인증서 관리** | 공인 CA 중심 (Global) | 사설 CA 중심 (Service Mesh/Internal) |
| **보안 수준** | 중간 (서버 위장 방지) | 매우 높음 (비인가 클라이언트 차단) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
기술사로서 mTLS 도입 시 가장 큰 고려 사항은 '운영 복잡성'과 '성능 저하'입니다.
- **운영 전략:** 수백 개의 인증서를 수동으로 관리하는 것은 불가능하므로, 반드시 **Istio** 같은 서비스 메시를 활용해 자동 주입(Injection) 및 자동 갱신 체계를 갖춰야 합니다.
- **감리 주안점:** 핸드쉐이크 과정에서 발생하는 CPU 부하와 지연 시간(Latency)이 성능 목표를 만족하는지 확인해야 합니다. 또한 인증서 유효기간 만료 시 자동 갱신 실패에 대비한 모니터링 체계가 있는지 점검해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
mTLS는 마이크로서비스 간의 '강력한 신분증' 역할을 하며 클라우드 보안의 표준이 되었습니다. 최근에는 **SPIFFE**와 같은 오픈 표준을 통해 이기종 클라우드 환경에서도 통일된 방식으로 mTLS 신원 인증을 수행하려는 시도가 활발합니다. 향후 인프라 보안은 mTLS를 기본(Default)으로 설정하고, 그 위에 비즈니스 로직 기반의 인가(RBAC/ABAC)를 얹는 다층 방어 체계로 진화할 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Zero Trust Security, TLS/SSL
- **하위 개념:** Public Key Infrastructure (PKI), Certificate Authority (CA)
- **연관 개념:** Service Mesh, Sidecar, SPIFFE, JWT

### 👶 어린이를 위한 3줄 비유 설명
1. **일반 TLS**는 손님이 가게 주인만 확인하고 들어가는 거예요.
2. **mTLS**는 가게 주인도 손님에게 "회원증 보여주세요!"라고 해서 서로 아는 사람인지 확인하는 거예요.
3. 서로의 신분증을 꼼꼼히 확인하기 때문에 낯선 사람이 절대 들어오거나 엿볼 수 없답니다!
