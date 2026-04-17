+++
weight = 112
title = "RSA-OAEP (Optimal Asymmetric Encryption Padding)"
date = "2025-05-15"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
- RSA 암호화 시 평문에 무작위성을 부여하여 **결정론적 특성을 제거**하는 최적의 패딩 스키마이다.
- 해시 함수와 XOR 연산을 결합한 **Feistel 구조**를 사용하여 선택 암호문 공격(**CCA2**)에 대한 안전성을 보장한다.
- 기존 PKCS#1 v1.5 패딩의 보안 취약점(Bleichenbacher's Attack 등)을 해결한 현대 RSA 암호화의 표준 방식이다.

### Ⅰ. 개요 (Context & Background)
기본적인 RSA(Textbook RSA)는 동일한 평문을 암호화하면 항상 동일한 암호문이 생성되는 취약점이 있다. 또한, 암호문이 특정 수학적 구조를 가지면 공격자가 이를 변조하여 정보를 알아낼 수 있다. 이를 방지하기 위해 벨라레(Bellare)와 로가웨(Rogaway)가 제안한 **OAEP**는 평문에 무작위 난수와 해시값을 섞어 암호화함으로써, 암호문만으로는 평문의 어떤 정보도 유추할 수 없게 만드는 **의미론적 보안(Semantic Security)**을 제공한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
OAEP는 평문(M)을 해시 기반의 마스크 생성 함수(**MGF**)를 통과시킨 값들과 결합하는 과정을 거친다.

```text
[RSA-OAEP Architecture: Padding Process]

Input: Message (M), Seed (Random r), Label (L)
Hash Functions: G (MGF1), H (Hash)

1. G-Block:
   - DB = Hash(L) || Padding || 0x01 || M
   - MaskedDB = DB XOR G(Seed)
   
2. H-Block:
   - MaskedSeed = Seed XOR H(MaskedDB)
   
3. Final Padded Message (EM):
   - EM = 0x00 || MaskedSeed || MaskedDB

[Visual Flow Diagram]
   Seed (r) ----+-----------> H(.) ----+----> MaskedSeed
      |         |                      ^
      |      G(.) --+                  |
      |             |                  |
      +------------> XOR <-------------+
                    |
   DB (M + Hash) ---+------> XOR <----------+
                               |            |
                               +------> MaskedDB

[Final Step]
   Ciphertext C = (EM)^e mod n
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Criteria) | RSA-OAEP | PKCS#1 v1.5 Padding | RSA-PSS |
| :--- | :--- | :--- | :--- |
| **주요 용도** | **암호화 (Encryption)** | 암호화 / 서명 (Legacy) | **디지털 서명 (Signature)** |
| **안전성 모델** | **IND-CCA2** (매우 강함) | 선택 암호문 공격에 취약 | EUF-CMA (서명 위조 방지) |
| **구조 특성** | Feistel Network 기반 | 단순 무작위 바이트 채우기 | 확률적 서명 방식 |
| **표준 상태** | PKCS#1 v2.0 이상 권장 | 하위 호환성용으로만 사용 | 최신 디지털 서명 표준 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **(취약점 방어)** 1998년 발견된 **Bleichenbacher 공격**은 패딩 오류 메시지를 통해 개인키 없이도 암호문을 복호화할 수 있음을 보여주었다. OAEP는 이러한 오라클 공격(Oracle Attack)에 저항력을 갖도록 설계되었다.
- **(매개변수 선택)** OAEP 사용 시 해시 함수(SHA-256 등)와 MGF의 선택이 중요하다. 라이브러리 간 호환성을 위해 표준화된 매개변수 세트를 사용하는 것이 실무적으로 중요하다.
- **(하이브리드 암호화 연계)** TLS 1.2/1.3 및 최신 데이터베이스 암호화 솔루션에서 RSA를 키 교환 용도로 사용할 때, 반드시 OAEP 옵션을 활성화하여 엔터프라이즈급 보안 수준을 유지해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
RSA-OAEP는 비대칭키 암호화가 가져야 할 '안전한 패딩'의 정석을 보여준다. 수학적 증명(Random Oracle Model)을 통해 안전성이 입증되었으며, 양자 컴퓨터 시대 이전까지 RSA 암호화의 가장 견고한 방패 역할을 지속할 것이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: RSA, 패딩(Padding)
- **자식/확장 개념**: MGF(Mask Generation Function), IND-CCA2
- **관련 공격**: 오라클 공격(Padding Oracle Attack), Bleichenbacher's Attack

### 👶 어린이를 위한 3줄 비유 설명
1. 편지 내용을 그냥 보내는 게 아니라, 아주 복잡한 무작위 가루(난수)를 골고루 섞어요.
2. 편지를 읽으려면 이 가루를 어떻게 섞었는지 알아야만 원래 내용을 볼 수 있게 만들어요.
3. 이렇게 하면 악당들이 편지 겉모습만 보고 "안에 어떤 내용이 있겠구나!"라고 추측하는 걸 완벽하게 막을 수 있어요.
