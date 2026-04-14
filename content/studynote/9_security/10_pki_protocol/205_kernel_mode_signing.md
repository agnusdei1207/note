+++
title = "205. Kernel Mode Signing (커널 모드 서명)"
date = "2026-03-25"
weight = 205
[extra]
categories = ["studynote", "security"]
+++

## 핵심 인사이트 (3줄 요약)
* **신뢰 기반 실행 환경**: Kernel Mode Signing은 Windows 운영체제의 핵심 영역인 커널(Kernel)에 로드되는 모든 드라이버가 신뢰할 수 있는 기관(Microsoft)에 의해 서명되었는지 검증하는 필수 보안 메커니즘입니다.
* **루트킷 및 악성코드 차단**: 인가되지 않거나 변조된 악성 드라이버(루트킷 등)가 커널 권한을 탈취하여 시스템을 장악하는 것을 원천적으로 차단합니다.
* **엄격한 인증 프로세스**: 하드웨어 개발자는 EV(Extended Validation) 인증서를 통해 신원을 증명하고, Windows 하드웨어 개발자 센터(HWDC)를 통해 Microsoft의 교차 서명(Cross-Certificate)을 받아야만 커널 로드가 가능합니다.

### Ⅰ. 개요 (Context & Background)
**Kernel Mode Signing(커널 모드 서명)**은 운영체제의 가장 깊은 영역(Ring 0)에서 동작하는 커널 드라이버(.sys)에 대한 코드 서명 강제 정책입니다. 과거 커널 영역의 취약점을 노린 루트킷(Rootkit) 감염과 불안정한 서드파티 드라이버로 인한 BSoD(Blue Screen of Death) 문제를 해결하기 위해 Windows Vista 64비트 버전부터 도입되었으며, Windows 10 버전 1607 이후 더욱 강화되었습니다. 이 정책은 커널 수준의 권한 상승 공격을 방지하고 시스템의 무결성을 유지하는 핵심 통제 수단입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

커널 모드 서명은 공개키 기반 구조(PKI)와 Windows의 부트로더 및 커널 로더 메커니즘이 긴밀하게 결합되어 동작합니다.

```text
+------------------------------------------------------------------------------+
|                        Kernel Mode Signing Architecture                      |
|                                                                              |
|  [Developer/Vendor]                     [Microsoft Dev Center]               |
|  +--------------------+                 +---------------------------------+  |
|  | 1. Write Driver    |                 | 3. Hardware Lab Kit (HLK) Test  |  |
|  |    Source Code     |                 |    & Validation                 |  |
|  +---------+----------+                 +----------------+----------------+  |
|            | (Compile)                                   |                   |
|            v                                             |                   |
|  +--------------------+                 +----------------v----------------+  |
|  | 2. Sign with       |=== Submit ====> | 4. Microsoft WHQL Signature     |  |
|  |    EV Certificate  |                 |    (Cross-Signing / Catalog)    |  |
|  +--------------------+                 +----------------+----------------+  |
|                                                          |                   |
|==========================================================|===================|
|                                                          v                   |
|  [End-User Windows System]                      [Signed Driver Package]      |
|  +------------------------------------------------------------------------+  |
|  | +------------------+   +------------------+    +------------------+    |  |
|  | | Windows Loader   |   | Code Integrity   |    | Driver Execution |    |  |
|  | | (winload.exe)    |-->| (ci.dll)         |--> | (Ring 0)         |    |  |
|  | +------------------+   +------------------+    +------------------+    |  |
|  |   - Verify MS Cert       - Check Hash            - Kernel Mode Load    |  |
|  |   - Reject unsigned      - Check Revocation      - Full System Access  |  |
|  +------------------------------------------------------------------------+  |
+------------------------------------------------------------------------------+
```

* **EV Code Signing**: 드라이버 제출을 위해 개발자는 가장 엄격한 신원 확인을 거치는 EV 코드 서명 인증서를 보유해야 합니다.
* **WHQL 서명 (Windows Hardware Quality Labs)**: 개발자가 서명한 드라이버 패키지를 Microsoft 대시보드에 제출하면, Microsoft가 자체 인증서로 다시 서명(Catalog 파일 서명)하여 배포 가능한 형태로 반환합니다.
* **Code Integrity (코드 무결성)**: Windows 커널 로더(`ci.dll`)는 드라이버가 메모리에 로드될 때마다 디지털 서명을 검증하고, 유효하지 않은 경우 로드를 즉시 중단합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | Kernel Mode Signing | User Mode Signing |
| :--- | :--- | :--- |
| **적용 영역** | 커널 계층 (Ring 0, `.sys` 파일 등) | 사용자 계층 (Ring 3, `.exe`, `.dll` 등) |
| **서명 주체 요구사항** | Microsoft의 최종 서명 필수 (Windows 10+) | 일반 Code Signing 인증서로도 가능 |
| **보안 강도** | 극도로 높음 (운영체제 무결성 직결) | 중간~높음 (애플리케이션 무결성 보장) |
| **실패 시 영향** | 시스템 부팅 불가 또는 하드웨어 동작 불가 | 해당 애플리케이션 실행 불가 (SmartScreen 경고) |
| **주요 방어 대상** | 부트킷, 커널 루트킷, 시스템 패닉(BSoD) 유발 버그 | 일반 악성코드, 랜섬웨어, 트로이목마 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

* **보안 솔루션 개발 전략**: EDR, 백신, 보안 필터 드라이버 등 시스템 깊숙이 개입하는 솔루션을 개발하는 기업은 반드시 EV 인증서 관리 및 Microsoft 파트너 센터 프로세스를 개발 파이프라인(CI/CD)에 통합해야 합니다.
* **취약점 대응 (BYOVD 공격)**: 공격자들은 서명이 강제되자 '취약한 정상 서명 드라이버(Bring Your Own Vulnerable Driver)'를 악용하여 커널 권한을 탈취하는 우회 공격을 시도합니다. 따라서 보안 팀은 Microsoft의 드라이버 차단 목록(Blocklist)을 시스템에 지속적으로 업데이트해야 합니다.
* **운영 환경 통제**: 서버 및 중요 엔드포인트 환경에서는 테스트 목적의 '테스트 서명 모드(Test Signing Mode)'가 활성화되지 않도록 구성 관리(Configuration Management) 및 GPO를 통해 강력히 통제해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)

Kernel Mode Signing은 운영체제의 가장 치명적인 약점이었던 커널 권한의 무분별한 탈취를 막는 핵심 방패입니다. 향후 이 기술은 UEFI Secure Boot 및 가상화 기반 보안(VBS, Virtualization-Based Security), HVCI(Hypervisor-Enforced Code Integrity) 등과 결합하여 운영체제의 밑바닥부터 애플리케이션 계층까지 빈틈없는 무결성 체인(Chain of Trust)을 완성하는 방향으로 진화할 것입니다. 기업은 커널 레벨의 위협 모델링 시 서명 우회 기법에 대한 방어 전략을 고도화해야 합니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **상위 개념**: 코드 서명 (Code Signing), 공개키 기반 구조 (PKI)
* **하위/연관 개념**: EV Code Signing, WHQL, ci.dll, 루트킷(Rootkit), BYOVD 공격, UEFI Secure Boot, HVCI

### 👶 어린이를 위한 3줄 비유 설명
1. 여러분이 엄청 중요한 금고(컴퓨터의 심장, 커널)를 관리하는 경찰이라고 상상해 보세요.
2. 금고에 들어가려는 사람(드라이버)은 동네 경찰서의 도장뿐만 아니라, **대통령(Microsoft)이 직접 찍어준 특별 허가증**을 보여줘야만 문을 열어줍니다.
3. 이렇게 하면 나쁜 도둑들이 가짜 신분증을 만들어 금고에 들어오는 것을 완벽하게 막을 수 있답니다!
