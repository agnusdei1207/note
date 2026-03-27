---
title: "링 오실레이터 (Ring Oscillator) TRNG"
date: 2026-03-20
weight: 787
description: "가장 널리 쓰이는 진성 난수 생성기(TRNG)의 하드웨어 설계법으로, 홀수 개의 인버터(NOT 게이트)를 둥글게 이어 붙여 무한 진동을 일으키고 그 과정에서 발생하는 미세한 엇박자(Jitter)를 난수로 추출하는 회로"
taxonomy:
    tags: ["Computer Architecture", "Advanced Topics", "Cryptography", "Hardware", "TRNG", "Ring Oscillator"]
---

## 핵심 인사이트 (3줄 요약)
> 1. TRNG(진성 난수 생성기)를 만들려면 열잡음 같은 아날로그 현상이 필요한데, 디지털 반도체 칩(FPGA나 스마트카드) 안에는 아날로그 증폭 회로를 우겨넣기가 까다롭고 공간을 많이 차지한다.
> 2. **링 오실레이터 (Ring Oscillator)**는 오직 디지털 논리 게이트(NOT 게이트)만으로 이루어져 있어 **아주 작고 싸게 칩 안에 찍어낼 수 있는 가장 대중적인 TRNG 회로**다.
> 3. 홀수 개의 NOT 게이트를 링 모양으로 무한루프 시키면 0과 1이 미친 듯이 진동(Oscillation)하는데, 온도와 전압의 미세한 변화 때문에 이 진동 주기에 찰나의 **엇박자(Jitter)**가 발생하며 이 엇박자를 카운트하여 완벽한 난수를 뽑아낸다.



## Ⅰ. 홀수 개 NOT 게이트의 딜레마 (무한 진동)

NOT 게이트(Inverter)는 들어온 값을 반대로 뒤집는 디지털 회로입니다. (1이 들어오면 0, 0이 들어오면 1)

만약 3개의 NOT 게이트를 직렬로 연결하고, 마지막 3번 게이트의 출력을 다시 1번 게이트의 입력으로 **꼬리를 물게 연결(피드백 링)**하면 무슨 일이 벌어질까요?

1. 처음에 `1`이 들어갑니다.
2. 1번 게이트 통과 $\rightarrow$ `0`
3. 2번 게이트 통과 $\rightarrow$ `1`
4. 3번 게이트 통과 $\rightarrow$ `0`
5. 이 결괏값 `0`이 다시 1번 게이트 입력으로 들어갑니다.
6. 1번 통과 $\rightarrow$ `1` $\rightarrow$ 2번 통과 $\rightarrow$ `0` $\rightarrow$ 3번 통과 $\rightarrow$ `1`

전기 신호가 링을 한 바퀴 돌 때마다 결과가 0과 1로 계속 뒤집힙니다. 회로 스스로 **안정된 상태를 찾지 못하고 수백 MHz의 속도로 0, 1, 0, 1을 무한히 반복하며 진동(Oscillate)**하게 됩니다. 

> 📢 **섹션 요약 비유**: "청개구리 3명"을 원으로 둘러앉혔습니다. A가 "예"라고 하면 B는 반대로 "아니오", C는 반대로 "예", 그러면 A는 C의 대답을 듣고 다시 반대로 "아니오"라고 대답합니다. 이 3명은 평생 합의점을 찾지 못하고 입에 거품을 물며 무한 루프 수다를 떱니다.



## Ⅱ. Jitter (지터): 완벽하지 않은 시계의 떨림

이 진동(0 1 0 1)이 1나노초마다 완벽하게 칼같이 일어난다면 예측이 가능하므로 난수가 아닙니다.
하지만 현실 세계의 반도체(실리콘)는 완벽하지 않습니다.

* 칩 내부의 온도가 $0.1^\circ C$ 오르거나, 전압이 $0.001V$ 출렁이거나, 옆 코어에서 무거운 연산을 돌려 전자파 노이즈가 끼어들면, 게이트가 0을 1로 뒤집는 속도(Delay)가 찰나의 순간 늘어지거나 빨라집니다.
* 이 미세하게 어긋나는 엇박자를 **지터(Jitter)**라고 부릅니다. 
* 링 오실레이터가 1억 바퀴를 돌면, 이 미세한 엇박자가 누적되어 **"정확히 언제 0에서 1로 바뀔지" 우주 그 누구도 예측할 수 없는 완벽한 아날로그적 혼돈 상태**에 빠집니다.

### 난수 추출 다이어그램 (ASCII)

```text
 ┌──▶ [ NOT ] ──▶ [ NOT ] ──▶ [ NOT ] ──┐
 │                                      │ (무한 진동 회로)
 └──────────────────────────────────────┴──▶ (출력 파형: 0 1 0 1 0 1)
                                                 │
                                                 ▼
     [ D 플립플롭 (샘플러) ] ◀── (매우 안정적인 외부 기준 클럭으로 도장 찍음)
           ▼
     [ 1 0 0 1 1 0 1 ... ] (엇박자 때문에 랜덤한 0과 1의 조합 생성 완성!)
```

> 📢 **섹션 요약 비유**: 팽이를 돌렸습니다. 팽이가 1초에 10바퀴씩 일정하게 도는 것 같지만, 바닥의 미세한 먼지나 공기 흐름(노이즈) 때문에 팽이의 회전축은 아주 미세하게 흔들립니다(지터). 이 미세한 흔들림을 확대경으로 찍어서 난수로 추출하는 천재적인 발상입니다.



## Ⅲ. 링 오실레이터의 약점 (해킹의 표적)

이 링 오실레이터 TRNG는 FPGA나 마이크로컨트롤러에 쉽게 박아넣을 수 있어 현재 가장 사랑받는 구조입니다.

하지만 무서운 약점이 있습니다. 바로 앞서 배운 **볼티지 글리칭(전압 조작)**이나 **클럭 글리칭**, 그리고 **전자기파(EMA) 공격**에 매우 취약하다는 점입니다.
해커가 칩 바깥에서 초강력 안테나로 특정 주파수의 전자기파를 쏘면(Frequency Injection), 이 링 오실레이터의 진동이 해커가 쏘는 전자기파 템포에 강제로 동기화(Lock-in)되어 버립니다!

지터(무질서)가 사라지고 해커의 조종대로 0 1 0 1 이 일정하게 나오게 되어, 암호 키가 예측 가능해지는 재앙이 벌어집니다. 이를 막기 위해 여러 개의 링 오실레이터를 꼬아서 복잡하게 만들거나(FI-RO), 외부 쉴드를 덮는 방어전이 치열하게 벌어지고 있습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오

1. **시나리오 — FPGA 기반 安全 시스템**:，军用이나 金融 시스템에서 사용되는 FPGA에 내장된 Ring Oscillator TRNG는 외부 PLL clock과 의도적으로 ASICS间的 계층化를 통해, электромагнитная инъекция (EMI) 공격으로 부터 보호된다. NIST SP 800-90B compliant한 entropy source로 certified되기 위해서는, 每秒 1-bit 이상의 entropy를 매 클럭 사이클마다 生成해야 한다.

2. **시나리오 — 자동차 ECU의 Random Number Generation**: 자동차의 ABS (anti-lock braking system)나 airbag control module에서 랜덤 넘버가 필요한 경우, Ring Oscillator TRNG를 利用한다. 이는 全IAS용으로 별도의 physical entropy source를增设할 필요 없이, 디지털 로직만으로 low-cost으로 구현 가능하기 때문이다. 그러나 车載環境의剧烈的 온도 변화 (-40°C ~ +125°C)에서도 stable한 entropy를生成해야 하므로, 온도 компенсация 회로가 필수적이다.

3. **시나리오 — 스마트카드의 3단계 보안**: 스마트카드(신용카드칩, SIM 카드)에서는 Ring Oscillator TRNG가 生成한 난수를 基幹として, DES/3DES，AES，RSA 등의 暗号化 연산을 수행한다. 그러나 앞서 설명한 ФАПЧ (PLL) 공격에 취약하므로, 현실계的高端 스마트カード에서는 PLL 자체를 제거하고, ASIC 내부에 별도의 fully independent oscillator network를 구축하여, 외부 clock와 完全히 분리된 상태에서 난수를生成하는 구조가 일반적이다.

### 도입 체크리스트
- **NIST SP 800-90B 인증**: B單位 (Conditional tests)와 C单位 (熵度 estimated) 테스트를 통과해야 正式한 entropy source로 인정된다. AIS 31보다 NIST 800-90B가 더 보편적이므로, 글로벌 공급망에서는 NIST 표준 준수가 필수이다.
- **온도/전압 변화에 대한 내성**: automotive (-40~125°C)나 산업용 (-25~85°C) 환경에서는 전압 fluctuation과 온도 변화에 따른 entropy 저하를 측정하고, 최소 Entropy threshold (일반적으로 0.99 bits/event 이상)를維持하는지 확인해야 한다.
- **Glitching 공격 방어**: Ring Oscillator의 출력이 외부 clock에 의존하면, voltage glitching나 clock glitching으로 Entropy가 감소할 수 있으므로, fully asynchronous (self-timed) design이 권장된다.

### 안티패턴
- **단일 Ring Oscillator에의 과도한 의존**: 1개의_ring만 사용하면, manufacturing variability나 aging에 따라 entropy가 감소할 때 대처할 방법이 없다. 반드시 복수개의 ring을 병렬로 사용하고, 그 출력을 XOR하여 final entropy를 높여야 한다.
- **PLL-based Clock에의 강제 동기화**: 외부 클럭에 의존적인 구조는 앞서 설명한 ФАПЧ 공격에完全に 노출된다. 따라서 ring oscillator는 PLL 없이 independent하게 동작해야 하며, 필요하다면 AES 위에서 encryption하여 출력을 whitening하는 후처리 단계가 필요하다.

> 📢 **섹션 요약 비유**: Ring Oscillator TRNGは「複数개의 팽이가 각각 다른 속도로 돌아가고, 그 엇박자를 모으는 것」と 같다. 만약 한 팽이의 움직임만頼りに하면 그 팽이가 망가지거나 느려질 때大問題하지만, 数多くの 팽이를 동시에 돌리면 그중 몇 개가 좀 튜거나 느려도整体は 여전히 무작위성을維持한다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량/정성 기대효과

| 구분 |/software PRNG | Linearfeedback Shift Register (LFSR) | Ring Oscillator TRNG | 개선 효과 |
|:---|:---|:---|:---|:---|
| **예측 가능성** | 높음 (알고리즘 의존) | 중간 (선형 구조) | 극히 낮음 (아날로그 지터) | **완전 난수** |
| **하드웨어 비용** | 0 (소프트웨어만) | 매우 낮음 | 중간 (NOT 게이트 수십 개) | **적합** |
| **EMI 공격 저항** | 낮음 | 낮음 | 중간 (防护策 필요) | **방어 가능** |
| ** NIST 800-90B 인증** | 곤란 | 곤란 | 可能 (compliant) | **표준 호환** |
| **응용 분야** | 일반 앱 | 통신 (scrambling) | 보안/자동차/금융 | **최상** |

### 미래 전망
- **Quantum RNG와의 hybrid**: 차세대 보안 시스템에서는 classical ring oscillator TRNG와 quantum photon-based QRNG의 출력을 합성(hybrid)하여,万一의 quantum 컴퓨터 공격에도버티기 힘든 ultra-strong randomness를 生成하는 것이 표준이 될 것이다.
- **TRNG + PUF integration**: Ring Oscillator의 entropy와 PUF의 physical unclonability를 결합하여, 칩 출하 시부터 고유한 identity와 randomness를 동시에確立하는 차세대 security primitive가 등장할 것이다.
- **Post-Quantum에 안전한 TRNG**: 양자 컴퓨터는 현재의 computational assumption을 모두 무너뜨리지만, Ring Oscillator의 지터는 양자 역학의 본질적 무작위성(quantum noise)에 기반하므로, 양자 컴퓨터 시대에도 안전한 randomness source로 功能할 것이다.

### 참고 표준
- **NIST SP 800-90B (Recommendation for Entropy Sources)**: TRNG의 entropy 평가에 대한 미국 NIST 표준이다.
- **AIS 31 (Bundesnetzagentur TRNG Guidelines)**: 독일 BNetzA가制定한 TRNG 평가 표준으로, European Common Criteria에 영향을 미쳤다.
- **Intel RDRAND/RDSEED**: Intel CPU에 내장된 hardware RNG로, Ring Oscillator와 AES-based whitening의 hybrid 구현이다.
- **ISO/IEC 19790 (Security Techniques)**: 암호 모듈에 대한 보안 요구사항으로, 내부 TRNG에 대한 요구사항도 포함한다.

Ring Oscillator TRNG는 놀랍도록 단순한 디지털 회로(홀수 개의 NOT 게이트)로 실현되는 가장 대중적인 진성 난수 생성기다. 그 출력이 미세한 アナログ 震動(지터)에 의존하기 때문에, 이론적으로 예측 불가능한 완벽한 무작위성을 제공한다. 그러나外部 환경(온도, 전압, EMI)이나 의도적인 공격(glitching, PLL)에 취약한的一面도있어, 실무에서는 반드시 다중 ring + whitening + glitching 방어 등의 multi-layer 방어 전략이 필요하다.

> 📢 **섹션 요약 비유**: Ring Oscillator TRNGは「たった3人だけの反官僚党员に、无限に議論させて、その仅かな口气の音を拾って随机な数に変換する、超 省小規模な地震感知器」と 같다. 非常に简陋だが、意外にもその微かな震えは世界のどんな计算机にも予測できない 완전한 무작위성을갖고 있다.

---

### 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **TRNG (True Random Number Generator)** | Ring Oscillator TRNG의 상위 개념으로, 진성 난수를 생성하는 모든 장치를 의미한다. |
| **Jitter (지터)** | Ring Oscillator의 출력이 완벽히 일관되지 않고 미세하게 흔들리는 현상으로, Entropy의 근원이다. |
| **PRNG (Pseudo-Random Number Generator)** | 시드(seed)에서 알고리즘으로 난수처럼 보이는 수를 생성하는 것으로, TRNG와 대비된다. |
| **Whitening (화이트닝)** | TRNG 출력을 추가 암호화하여 bias를 제거하고 균등 분포로 만드는 후처리 과정이다. |
| **PLL (Phase-Locked Loop) 공격** | 공격자가 외부 클럭을 링 오실레이터에 주입하여 출력을Manipulation하는 공격이다. |
| **Entropy Source Certification (NIST 800-90B)** | TRNG가 실제로 무작위성을 生成하는지 공식적으로 인증하는 표준이다. |

---

### 👶 어린이를 위한 3줄 비유 설명
1. 반짝반짝 빛나는 LED 불빛 3개를 같은 원을 그리며 빙글빙글 돌게 해요. 세 개가 다 다른 속도로 돌고 있어서, 언덕번에 "지금 어떤 불이 위에 있을까?"를预测하는 것은 불가능해요.
2. 이 미세한 엇박자를 利用해서, "0번 불이 위에 있으면 0, 1번 불이 위에 있으면 1"이라고 규칙을 정하면, 무척이나 완벽한 랜덤 숫자가 만들어져요.
3. 하지만 만약 누군가가 밖에서 큰 소리로 "일정하게하라!"라고 외치면(PLI攻击), LED들이 그리에 맞춰져서 무작위성이 나빠질 수 있어요. 그래서 보통 여러 개의 LED 원을 동시에 돌려서,万一 하나が外部の影響を受けても 나머지가 여전히 무작위하게 유지되도록 해요!
