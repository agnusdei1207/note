+++
weight = 6
title = "006. 부인방지 (Non-repudiation) - 거래의 증거 확보와 부인 방지"
date = "2024-10-27"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
1. **거래 증거력 확보**: 송신자 또는 수신자가 메시지를 주고받은 사실을 나중에 부인하지 못하도록 하는 정보보안의 핵심 요소다.
2. **전자서명 기반**: 공개키 암호 알고리즘(Asymmetric Crypto)과 타임스탬프(TSA)를 결합하여 법적·기술적 효력을 갖춘 증거를 생성한다.
3. **책임 추적성 연계**: 감사 로그와 함께 사용되어 사고 발생 시 행위 주체를 명확히 규명하는 책임 추적성(Accountability)의 근거가 된다.

### Ⅰ. 개요 (Context & Background)
부인방지(Non-repudiation)는 온라인 거래와 데이터 전송에서 발생할 수 있는 "나는 보낸 적이 없다" 또는 "나는 받은 적이 없다"는 주장을 무력화하는 기술적 통제 수단이다. 이는 단순히 데이터의 무결성(Integrity)을 지키는 수준을 넘어, 행위 주체의 **'신원'**과 **'행위 시점'**을 고정함으로써 법적 신뢰성을 제공하는 정보보안 5요소(CIA + 인증, 부인방지)의 하나다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
부인방지는 송신 부인방지(Non-repudiation of Origin)와 수신 부인방지(Non-repudiation of Receipt)로 구분된다.

```text
[Non-repudiation Architecture / 부인방지 아키텍처]

 Sender (A)             Recipient (B)          TSA/CA (Authority)
   |                      |                       |
   |--- 1. Digital Sig. --|                       | (Issue Certs)
   |    (Sign with PrivKey)|                      |
   |                      |                       |
   |--- 2. Send Message --|                       |
   |                      |--- 3. Req TimeStamp --| (Verify Identity)
   |                      |                       |
   |                      |<-- 4. Issue Token ----| (Add Proof of Time)
   |                      |                       |
   |--- 5. Confirm Rcpt --|                       |

<Key Components / 핵심 구성요소>
- Digital Signature: 송신자의 개인키로 서명하여 송신 사실 증명
- Public Key Certificate: 서명 검증을 위한 신뢰 기관(CA)의 인증
- Time Stamp Token: 거래 발생 시점의 공신력 있는 시간 정보 추가
```

**핵심 메커니즘:**
- **공개키 암호화**: 개인키는 서명에, 공개키는 검증에 사용하여 송신자를 특정한다.
- **해시 함수**: 원본 데이터의 변조 여부를 확인하여 내용 부인을 방지한다.
- **공인인증기관(CA)**: 인증서(X.509)를 통해 공개키의 소유주를 보증한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 부인방지 (Non-repudiation) | 인증 (Authentication) | 무결성 (Integrity) |
| :--- | :--- | :--- | :--- |
| **주요 목적** | **행위 사실**의 입증 및 거부 방지 | **신원(Identity)**의 확인 | **데이터 변조** 방지 |
| **기술 수단** | 전자서명 + 타임스탬프 | ID/PW, 생체인증, PKI | 해시 함수 (SHA-256 등) |
| **법적 효력** | 강함 (증거력) | 중간 (접근 권한) | 약함 (데이터 상태) |
| **시점 정보** | **필수적** (언제 했는가) | 선택적 | 부수적 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
기술사적 관점에서 부인방지는 **'기술적 수단과 법적 효력의 결합'**으로 이해해야 한다.
1. **전자금융 거래**: 송금 시 디지털 서명을 생성하여 "돈을 보낸 적 없다"는 부인을 방지하며, 공인전자문서센터 보관을 통해 증거력을 유지한다.
2. **SLA(Service Level Agreement)**: 장애 발생 시 가용성 위반 리포트에 대한 부인방지를 위해 감사 로그(Audit Log)에 서명을 적용한다.
3. **블록체인 활용**: 분산 원장에 거래 내역을 기록하여 합의 알고리즘에 따른 부인방지를 구현하되, 법적 규제 준수(Compliance) 여부를 반드시 검토해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
부인방지는 디지털 전환(DX) 시대의 '신뢰 자산'이다. 전자문서법과 전자서명법의 개정으로 다양한 민간 인증 수단이 등장함에 따라, 부인방지의 표준도 더욱 유연해지고 있다. 향후 양자 내성 암호(PQC)의 도입과 함께 부인방지 기술도 고도화될 것이며, 이는 메타버스나 자율주행 차량 간 통신(V2X)에서 행위의 책임을 명확히 하는 필수 표준으로 자리 잡을 것이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: Information Security, PKI
- **유사 개념**: Accountability, Digital Signature, TSA
- **하위 기술**: RSA/ECDSA, Hashing, X.509 Certificate

### 👶 어린이를 위한 3줄 비유 설명
1. 중요한 약속을 하고 종이에 이름을 쓰고 도장을 꾹 찍는 것과 같아요.
2. 나중에 "나 그런 약속 한 적 없는데?"라고 거짓말을 해도, 도장이 찍힌 종이가 증거가 된답니다.
3. 컴퓨터에서도 내가 보냈다는 확실한 도장을 찍어두어서 아무도 딴소리를 못 하게 하는 기술이에요.
