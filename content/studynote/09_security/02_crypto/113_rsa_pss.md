+++
weight = 113
title = "RSA-PSS (Probabilistic Signature Scheme)"
date = "2026-03-05"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
- 기존 RSA-PKCS#1 v1.5의 취약점을 보완하기 위해 **확률적 패딩(Probabilistic Padding)** 방식을 도입한 디지털 서명 알고리즘임.
- 서명 과정에 **난수(Salt)**를 섞어 동일한 메시지라도 매번 다른 서명이 생성되도록 하여, 선택 암호문 공격(CCA) 등에 대한 보안성을 극대화함.
- PKCS#1 v2.1 이상에서 표준으로 채택되었으며, 이론적으로 완벽한 **증명 가능한 안전성(Provable Security)**을 제공함.

### Ⅰ. 개요 (Context & Background)
- **배경:** 고전적인 RSA 서명은 결정론적(Deterministic)이어서, 동일한 메시지에 대해 항상 같은 서명이 생성되어 Replay 공격이나 위조 공격에 노출될 위험이 있었음.
- **정의:** Bellare와 Rogaway가 제안한 방식(PSS)을 RSA에 적용한 것으로, 해시 함수와 마스크 생성 함수(MGF)를 사용하여 서명을 생성하는 기술임.
- **표준:** RFC 8017 (PKCS #1 v2.2)에 정의되어 있으며, 최신 TLS 1.3 등에서 권장되는 서명 방식임.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ RSA-PSS Encoding Process (EM) ]
+-----------------------------------------------------------+
| M (Message) -> Hash(M) -> mHash                           |
| Salt (Random) ---------------------+                      |
|                                    v                      |
| [Padding1] + [mHash] + [Salt] -> [DB (Data Block)]        |
|                                    |                      |
| [mHash] -> MGF(mHash) -> dbMask ---XOR---> [maskedDB]     |
|                                                           |
| [maskedDB] + [Hash(maskedDB, salt...)] + [0xBC] -> EM     |
+-----------------------------------------------------------+
  * EM (Encoded Message) is then signed using RSA Private Key.
```
- **주요 단계:**
  1. **Hashing:** 메시지를 고정 길이 해시값(mHash)으로 변환.
  2. **Salt Addition:** 무작위 소금(Salt) 값을 생성하여 결합.
  3. **MGF (Mask Generation Function):** 해시값을 기반으로 마스크를 생성하여 DB를 보호.
  4. **RSA Signing:** 인코딩된 메시지(EM)를 RSA 개인키로 멱승 연산 수행.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | RSA-PKCS#1 v1.5 서명 | RSA-PSS 서명 |
| :--- | :--- | :--- |
| **방식** | 결정론적 (Deterministic) | 확률적 (Probabilistic) |
| **안전성** | 휴리스틱 기반 (일부 취약점 존재) | 증명 가능한 안전성 (Random Oracle Model) |
| **난수(Salt) 사용** | 미사용 | 사용 (보안 강도 가변 가능) |
| **권장 여부** | 레거시 호환용 | 최신 시스템 표준 (TLS 1.3 등) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **적용 사례:** TLS 1.3 핸드셰이크 인증, 코드 서명(Authenticode), 암호 화폐 지갑 인증.
- **기술사적 판단:** 신규 시스템 구축 시 보안성이 입증되지 않은 v1.5 대신 RSA-PSS를 사용하는 것이 필수적임. 특히 양자 내성 암호(PQC)로 넘어가기 전까지 RSA 환경에서 가장 강력한 대안임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과:** 서명의 무작위성을 확보하여 부채널 공격(Side-channel) 및 수학적 공격에 대한 저항력을 대폭 향상시킴.
- **결론:** RSA-PSS는 현대 PKI 체계에서 신뢰성을 담보하는 핵심 기법이며, 정보보안 컴플라이언스(FIPS 186-4 등) 준수를 위한 표준 모델임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Digital Signature, RSA Algorithm
- **연관 개념:** PKCS#1, OAEP (암호화용 패딩), SHA-256, MGF1

### 👶 어린이를 위한 3줄 비유 설명
- 똑같은 편지에 싸인을 할 때, 매번 다른 색깔의 반짝이 가루(Salt)를 뿌려서 싸인하는 것과 같아요.
- 이렇게 하면 다른 사람이 내 싸인을 똑같이 베끼려고 해도 반짝이 패턴이 달라서 가짜인 걸 금방 들키게 돼요.
- 훨씬 안전하고 믿을 수 있는 최첨단 도장 방식이랍니다.
