+++
weight = 7
title = "책임추적성 (Accountability) — 감사 로그, 감사 기록, 사용자 행동 추적"
date = "2026-03-25"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **핵심 정의**: 보안 사고나 시스템 활동 발생 시, 해당 행동의 주체(Entity)를 식별하고 그 책임을 명확히 물을 수 있도록 보장하는 보안 특성이다.
> 2. **기술적 구현**: 사용자 식별(ID), 인증(Auth), 세분화된 접근 제어(RBAC/ABAC), 그리고 변조 불가능한 감사 로그(Audit Log)를 통해 완성된다.
> 3. **융합 가치**: 부인방지(Non-repudiation)와 밀접하게 연계되며, 사고 후 원인 분석(Forensics)과 법적 대응을 위한 필수적인 보안 거버넌스 항목이다.

---

### Ⅰ. 개요 (Context & Background)
정보보안의 3요소(CIA)에 더해 현대 보안에서 강조되는 중요한 특성이 바로 책임추적성(Accountability)이다. 이는 단순히 누가 무엇을 했는지 기록하는 것을 넘어, 시스템에서 발생하는 모든 유의미한 행동에 대해 개별 사용자를 1:1로 매핑하여 "나는 그 행동을 하지 않았다"고 거짓말할 수 없게 만드는(부인방지) 기술적·관리적 체계를 의미한다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
  [Subject: User/Admin]         [Action/Event]         [Object: Resource]
         │                          │                          │
         ▼                          ▼                          ▼
  ┌──────────────┐          ┌──────────────┐          ┌──────────────┐
  │ Identification │──▶ [AAA] ──▶│  Operation   │──▶│ Secure Log   │
  │ Authentication │  (Server)  │ (Read/Write) │  │   Storage    │
  └──────────────┘          └──────────────┘          └──────────────┘
         │                          │                          │
         └───────────── [Accountability Chain] ────────────────┘
               (Who)              (What/When)              (Where)

   [The 4-Step Process for Accountability]
   1. Identification   : User IDs themselves (Who)
   2. Authentication   : Verify ID (Password/MFA)
   3. Authorization    : Grant permission (Access Control)
   4. Audit (Logging)  : Record everything (Proof)
```

**핵심 메커니즘:**
1. **식별(Identification):** 모든 사용자에게 고유한 ID를 부여한다 (공용 계정 사용 금지).
2. **인증(Authentication):** 본인임을 확실히 검증한다 (MFA 권장).
3. **감사 기록(Audit Logging):** 접속 시간, 수행 명령, 변경 데이터, 로그오프 시간 등을 타임스탬프와 함께 기록한다.
4. **로그 보호:** 로그 자체가 공격자에 의해 삭제되거나 변조되지 않도록 WORM(Write Once Read Many) 저장소나 원격 로그 서버로 실시간 전송한다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구분 | 인증성 (Authenticity) | 부인방지 (Non-repudiation) | 책임추적성 (Accountability) |
|:---|:---|:---|:---|
| **핵심 목표** | 주체의 신뢰성 확인 | 거래 사실 증명 | 행동 주체 식별 및 감사 |
| **관련 기술** | 디지털 서명, PKI | 타임스탬프, 전자서명 | **AAA(Authentication, Authorization, Accounting)** |
| **적용 시점** | 접근 시작 시 | 거래 완료 시 | **시스템 운용 전 과정** |
| **주요 연계** | Identification | Integrity | **Audit Logging** |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
기술사적 관점에서 책임추적성의 가장 큰 적은 '공용 관리자 계정(Shared Account)'의 사용이다. 아무리 로그를 잘 남겨도 root나 admin 계정으로 여러 명이 작업한다면 실제 행위자를 특정할 수 없다. 실무에서는 **계정 통합 관리(IAM)**와 **개별 계정 기반 권한 부여**를 철저히 해야 하며, 특히 특권 계정(Privileged Account)에 대해서는 **PAM(Privileged Access Management)** 솔루션을 통해 세션 레코딩을 실시함으로써 극강의 책임추적성을 확보해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
책임추적성은 보안 사고 발생 시 '사후 약방문'이 아닌, 공격자나 내부 직원의 일탈을 심리적으로 억제(Deterrence)하는 강력한 예방 수단이 된다. 향후 인공지능(AI) 기반의 사용자 행위 분석(UEBA)과 블록체인을 이용한 위변조 불가능한 로그 관리 기술이 결합되면서, 책임추적성은 더욱 자동화되고 신뢰할 수 있는 보안 인프라의 표준으로 자리 잡을 것이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **핵심 기반**: AAA (Authentication, Authorization, Accounting)
- **연계 개념**: 부인방지 (Non-repudiation), 디지털 포렌식 (Digital Forensics)
- **보안 통제**: IAM (Identity and Access Management), PAM (Privileged Access Management)

---

### 👶 어린이를 위한 3줄 비유 설명
1. 책임추적성은 거실에 있는 **CCTV와 이름표** 같은 거예요.
2. 누가 과자를 먹었는지, 누가 장난감을 어질렀는지 이름표를 보고 CCTV를 확인하면 금방 알 수 있죠.
3. "내가 안 했어!"라고 거짓말을 못 하게 해서, 모두가 규칙을 잘 지키게 도와주는 거랍니다.
