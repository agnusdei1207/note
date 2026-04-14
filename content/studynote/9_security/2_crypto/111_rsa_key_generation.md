+++
weight = 111
title = "RSA 키 생성 (RSA Key Generation)"
date = "2025-05-15"
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)
- 거대한 두 소수의 곱으로부터 **Modulus(n)**와 **오일러 피 함수(φ(n))**를 도출하는 수학적 정립 과정이다.
- 암호화 지수(e)와 복호화 지수(d) 사이의 **모듈로 역수(Modular Inverse)** 관계를 형성하는 것이 핵심이다.
- 생성 과정에서의 난수 발생 품질과 소수 판별 알고리즘의 정확도가 전체 암호 체계의 강도를 결정한다.

### Ⅰ. 개요 (Context & Background)
RSA 키 생성은 암호화 시스템의 신뢰를 구축하는 첫 단추다. 공개키(Public Key)는 모든 사람이 볼 수 있도록 공개하고, 개인키(Private Key)는 오직 소유자만 알 수 있도록 수학적으로 연관된 쌍(Pair)을 만들어야 한다. 이 과정에서 사용되는 수들이 충분히 크고 무작위적이지 않으면, 현대의 공격 기법(Coppersmith's Attack 등)에 의해 키가 노출될 수 있다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
RSA 키 생성의 알고리즘적 단계는 다음과 같다.

```text
[RSA Key Generation Flow]

1. Prime Selection (소수 선택):
   - Pick two large distinct primes, p and q.
   - Recommended size: 1024 bits each for a 2048-bit key.

2. Compute Modulus (법 n 계산):
   - n = p * q
   - (n is part of both public and private keys)

3. Compute Euler's Totient (오일러 피 함수):
   - φ(n) = (p - 1) * (q - 1)

4. Select Public Exponent (공개 지수 e 선택):
   - Choose e such that 1 < e < φ(n) AND gcd(e, φ(n)) = 1.
   - Commonly used: 65537 (0x10001).

5. Compute Private Exponent (개인 지수 d 계산):
   - d = e^(-1) mod φ(n)
   - (Using Extended Euclidean Algorithm)
   - e * d ≡ 1 (mod φ(n))

[Architecture Summary]
+-----------------------------+-----------------------------+
|    Public Key (e, n)        |    Private Key (d, n)       |
+-----------------------------+-----------------------------+
| Shared with everyone        | Kept secret (in HSM/TPM)    |
+-----------------------------+-----------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 단계별 기술 (Step Tech) | 주요 내용 및 알고리즘 | 보안적 고려사항 |
| :--- | :--- | :--- |
| **소수 생성 (Primes)** | **Miller-Rabin**, AKS Test | 난수 생성기(CSPRNG)의 엔트로피 부족 주의 |
| **Modulus (n)** | p * q | p와 q의 차이가 너무 작으면 안 됨 (Fermat's Factorization) |
| **지수 선택 (e)** | **65537** (2^16 + 1) | 비트가 적어 연산은 빠르나 보안성은 충분한 값 선택 |
| **지수 계산 (d)** | **확장 유클리드 알고리즘** | d가 n^0.29보다 작으면 위너 공격(Wiener's Attack) 위험 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **(난수 생성기의 무결성)** 키 생성의 근간은 소수 선택이며, 이는 **CSPRNG(Cryptographically Secure Pseudo-Random Number Generator)**에 의존한다. 시스템 엔트로피가 부족한 상태에서 생성된 키는 중복되거나 예측 가능해질 위험이 크다.
- **(CRT 최적화)** 실무에서 RSA 복호화 속도를 높이기 위해 **중국인의 나머지 정리(CRT)**를 활용한다. 이를 위해 키 생성 시 p와 q 값을 별도로 보관하는 것이 일반적이다.
- **(키 보관 전략)** 생성된 개인키는 파일 시스템에 평문으로 두지 않고, 하드웨어 보안 모듈(**HSM**)이나 **TPM** 내부에 생성하여 외부 유출을 원천 차단하는 설계를 권장한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
완벽한 RSA 키 생성은 소수성 검증과 수학적 관계의 정밀함에 달려 있다. 최근에는 FIPS 140-3 등의 표준을 통해 키 생성 과정의 물리적/논리적 안전성을 인증받는 추세이며, 이는 국가 및 기업의 정보 자산을 보호하는 가장 강력한 수단으로 기능한다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: RSA, 모듈로 역수(Modular Inverse)
- **자식/확장 개념**: Miller-Rabin 소수 판별법, 확장 유클리드 알고리즘, CRT(Chinese Remainder Theorem)
- **관련 공격**: 위너 공격(Wiener's Attack), 구리슴 공격(Coppersmith's Attack)

### 👶 어린이를 위한 3줄 비유 설명
1. 아주 아주 커다란 두 개의 비밀 숫자(소수)를 골라요.
2. 그 숫자들을 곱해서 커다란 방(n)을 만들고, 특수한 수학 마법을 써서 정문 열쇠(공개키)와 뒷문 열쇠(개인키)를 만들어요.
3. 뒷문 열쇠는 땅속 깊이 숨기고, 정문 열쇠는 성문에 걸어두어 누구든지 편지를 넣을 수 있게 하는 거예요.
