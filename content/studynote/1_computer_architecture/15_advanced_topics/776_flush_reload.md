---
title: "Flush+Reload 기법"
date: 2026-03-20
weight: 776
description: "해커와 피해자가 '공유 라이브러리(Shared Memory)'를 같이 쓸 때, 해커가 특정 메모리 주소를 캐시에서 강제로 쫓아낸(Flush) 뒤 다시 읽어보는(Reload) 방식으로 가장 높은 정확도를 자랑하는 캐시 타이밍 공격"
taxonomy:
    tags: ["Computer Architecture", "Advanced Topics", "Security", "Side-channel Attack", "Cache", "Flush+Reload"]
---

> **핵심 인사이트**
> 1. 앞 장의 Prime+Probe가 넓은 바다에서 그물을 치는 방식이라면, **Flush+Reload**는 해커와 피해자가 **같은 파일(예: `libc.so` 같은 리눅스 공유 라이브러리)**을 메모리에 올려놓고 쓸 때 사용하는 정밀 저격수(Sniper) 같은 방식이다.
> 2. OS는 메모리를 아끼기 위해 A 프로그램과 B 프로그램이 같은 파일을 쓰면 물리적 RAM을 '하나만' 복사해 두고 같이 쳐다보게(Page Sharing) 만든다. (이것이 치명적 약점)
> 3. 해커는 특정 주소를 캐시에서 강제로 삭제(Flush)한 뒤, 피해자가 실행되길 기다렸다가 다시 그 주소를 읽어봄(Reload)으로써 피해자가 그 주소를 사용했는지 **단 1캐시 라인(64바이트) 단위의 극강의 해상도**로 알아낸다. (멜트다운 공격의 핵심 탈출 기법)



## Ⅰ. OS의 메모리 절약 꼼수 (Shared Memory)

해커 프로그램과 피해자 프로그램(은행)이 같은 윈도우/리눅스 PC에서 돌아갑니다.
두 프로그램은 모두 화면에 글씨를 띄우기 위해 `libc.so` (또는 `user32.dll`)라는 똑같은 시스템 파일을 씁니다.

OS는 램(RAM)을 아끼려고 이 파일을 메모리에 2번 올리지 않습니다.
**"어차피 똑같은 파일이니까, 램에 딱 1번만 올려놓고 해커랑 은행 둘 다 이 물리 주소를 쳐다봐라!" (메모리 공유, De-duplication)**
이 완벽한 최적화가 해커에게는 서로의 심장(캐시)을 들여다볼 수 있는 치명적인 파이프가 됩니다.

> 📢 **섹션 요약 비유**: 해커와 은행원이 서로 다른 방에 살지만, 돈을 아끼기 위해 두 방 사이에 있는 거실(공유 도서관)은 벽을 허물고 같이 쓰도록 OS가 허락해 준 상황입니다.



## Ⅱ. Flush+Reload의 3단계 저격술

해커는 은행 프로그램이 AES 암호화 라이브러리의 어느 주소를 읽는지 알고 싶습니다.

1. **Flush (쓸어버리기)**
   * 해커는 x86의 **`CLFLUSH` (Cache Line Flush)** 명령어라는 특수 스킬을 씁니다. 이 명령어는 "특정 메모리 주소의 데이터를 L1, L2, L3 캐시에서 당장 쫓아내고 램으로 보내버려라!"라는 뜻입니다.
   * 해커는 공유 라이브러리(`libc.so`) 중 암호화 연산에 쓰이는 특정 주소(A)를 지정해서 `CLFLUSH`로 캐시에서 지워버립니다.
2. **Wait (대기)**
   * 은행 프로그램(피해자)이 실행되기를 잠깐 기다립니다. 만약 은행이 암호 키를 쓰면서 **주소 A를 덜컥 읽었다면, 주소 A의 데이터는 다시 캐시에 쏙 올라가게 됩니다.**
3. **Reload (다시 쏴보기)**
   * 해커가 주소 A의 데이터를 다시 읽어봅니다(Reload)은 스톱워치로 시간을 잽니다.
   * **1ns 만에 튀어나옴 (Cache Hit)**: "내가 아까 지웠는데 왜 빠르지? 아! 내가 기다리는 동안 **은행이 이 주소를 읽어서 캐시에 올려놨구나!**" (은행의 암호 키 패턴 파악)
   * **100ns 걸림 (Cache Miss)**: "여전히 느리네. 은행은 이 주소를 안 건드렸군."

### 공격 다이어그램 (ASCII)

```text
 ┌─── 해커 (Attacker) ───┐               ┌─── 은행 (Victim) ───┐
 │ 1. CLFLUSH 주소 A     │               │                         │
 │ (캐시에서 주소 A 삭제)  │               │                       │
 ├───────────────────────┤               ├─────────────────────────┤
 │ 2. 대기 (Wait)        │ ──(시간 흐름)─▶│ 3. 주소 A 실행 (캐시에 올라감)
 ├───────────────────────┤               ├─────────────────────────┤
 │ 4. Reload 주소 A      │               │                         │
 │ (어? 왜 캐시 히트가 나지?)│               │                     │
 │ ─▶ "너 주소 A 썼구나!!" │               │                       │
 └───────────────────────┘               └─────────────────────────┘
```

> 📢 **섹션 요약 비유**: 거실(공유 도서관)에 놓인 책 A에 묻은 먼지를 해커가 입으로 훅 불어서 털어버립니다(Flush). 잠시 숨어있다가 은행원이 나간 뒤 다시 와봅니다. 책 A에 지문이 묻어있으면(Hit), 은행원이 방금 그 책을 읽었다는 것을 100% 확신(Reload)하게 됩니다.



## Ⅲ. 멜트다운(Meltdown)의 비밀 통로

이 Flush+Reload 기법은 보안 역사상 가장 위대한 해킹인 **멜트다운(Meltdown)**의 화룡점정입니다.

멜트다운에서 비순차 실행(추측 실행)을 통해 훔쳐낸 커널의 비밀번호는, 권한이 없어 레지스터 밖으로 빼낼 수가 없었습니다. 
그래서 해커는 비밀번호를 **'공유 배열의 인덱스(주소)'**로 삼아 메모리를 한 번 터치(추측 실행)한 뒤 롤백당합니다.
이후 해커는 **Flush+Reload**를 이용해 "방금 배열의 몇 번째 칸에 캐시 히트가 나나?"를 1칸씩 찔러보며(Reload), 캐시에 흔적으로 남은 비밀번호를 현실 세계로 완벽하게 빼돌리게 됩니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오

1. **시나리오 — 클라우드 환경에서의 Flush+Reload를 利用한 Leaking**: CSP(Cloud Service Provider)의 공유 서버(shared kernel)에서 돌아가는 경쟁 사인 tenant A가 Flush+Reload로 tenant B의 RSA 개인키를 theft하는 상황. 이는 cloud의 기본적인 memory sharing architecture의 systemic 취약점이며,/cloud provider는 반드시 Flush+Reload mitigation (LFENCE, SIgmaS) 등을 kernel에 적용하고, security-sensitive workload는 SGX/SEV 등의 enclave에서 실행해야 한다.

2. **시나리오 — Meltdown/Little Glenn attacks로의展開**: 2018년에 발견된 Meltdown과 Spectre 계열 공격에서 Flush+Reload는 핵심 구성요소로 使用된다. 특히 Meltdown attack에서 비순차 실행으로 유출된 데이터는 Flush+Reload로만 확인 가능하며, OS vendor들은 kernel page table isolation (KPTI)를 통해 이 attack surface를 줄였다. 그러나 KPTI는 performance overhead (~5%)가 있어, real-time system에서는 trade-off 분석이 필요하다.

3. **시나리오 — side-channel authentication timing attack**: 인증 시스템에서 비밀번호 비교 시 early-exit 최적화를 쓰면, 공격자가 Flush+Reload로 각 바이트 비교 시간차(첫 실패 바이트 위치)를 측정하여 비밀번호 길이와 문자를 유출할 수 있다. 이를 방지하려면 constant-time comparison (memcmp返回值固定 시간)을 사용해야 하며, 이는金融系통등 보안 중요 시스템의 필수 구현 항목이다.

### 도입 체크리스트
- **기술적**: 시스템의 `CLFLUSH` 명령어 지원 여부를 확인하고, Jika CLFLUSH가 있다면 Flush+Reload attack surface가 존재한다. Kernel에서 `nospec` atau `mfence` 계열 방어벽 사용 여부를 점검하고, cloud workload에 enclave (SGX/SEV) 적용 가능성을 평가한다.
- **운영·보안적**: Tenant가 공유 kernel에서 동작하는 CSP 환경에서는 반드시 Flush+Reload mitigation이 적용되어 있는지 확인하고, security audit 시 side-channel attack 저항성을 테스트해야 한다. 또한 성능 모니터링 tooling (perf, PMU counters)이 attacker에 악용될 수 있으므로, production 환경에서는불필요한 성능 수집 기능을 비활성화해야 한다.

### 안티패턴
- **KPTI 미적용 상태での Meltdown 노출**: 커널 page table isolation (KPTI)를 disable하면, user-space에서 kernel memory를 직접 읽을 수 있는 Meltdown attack에 노출된다. 반드시 최신 kernel으로 업데이트하고 KPTI가 활성화되어 있는지 확인해야 한다.
- **Constant-time 미적용의 Timing Attack**: 비밀번호 비교나 인증 로직에서 early-exit comparison을 사용하면, 공격자가 Flush+Reload로 비교 시간을 측정하여 비밀번호를 유출할 수 있다. 반드시 constant-time comparison 함수를 사용해야 한다.

> 📢 **섹션 요약 비유**: Flush+Reload는「공유 도서관에서 다른 사람이 방금 읽은 책의 페이지에 묻은 지문까지 곣어서 파악하는 고도의 범죄 기법」と 같다. 이犯罪를防止하려면、图书馆に特別な滤纸（KPTI）を置き、 readers themselves（Atenant-/Btenant）에게影響 없이情報を読み取れないように해야 한다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량/정성 기대효과

| 구분 | Flush+Reload 미방어 | Flush+Reload 방어 적용 | 개선 효과 |
|:---|:---|:---|:---|
| **키 유출 시간** | 수초 만에 RSA-2048 키 전체 유출 | 키 유출 불가 ( enclave 보호) | **100%** 방지 |
| **探测准确도** | 64바이트 단위 (캐시 라인) | 공격 자체 불가 | **측정 불필요** |
| **멜트다운 노출** | 사용자 → 커널 격리 위반 | KPTI로 격리 복구 | **완전 차단** |
| **성능 오버헤드** | N/A | KPTI 시 ~5% | **trade-off 필요** |

### 미래 전망
- **Hardware-assisted Flush+Reload Prevention**: Intel의 `LFENCE` + `MFENCE` 명령어 조합과 AMD의 `SIGMA S` (Store Габельная), 그리고 upcoming hardware의 `Shadow Stack`과 `CET` (Control-flow Enforcement Technology)가 Flush+Reload를 근본적으로 제거할 것이다.
- **Enclave-first Architecture의 표준화**: Confidential Computing 시대에 모든 보안 중요 workload는 SGX (Intel), SEV (AMD), 또는 TrustZone (ARM) enclave 내에서 실행되는 것이 표준이 될 것이다. Flush+Reload는 enclave 밖에서만 동작하므로, 이アーキテクチャ采用으로自動的に防止된다.
- **Formal Verification과 Side-Channel Proof**: 차세대 보안 시스템에서는 Flush+Reload 등의 timing attack을 formal method로 proofs 하는 것이 당연해질 것이다. compiler-level의 constant-time 保证과 hardware-level의 timing isolation가 combine되어, side-channel 없는 secure system을构建할 수 있다.

### 참고 표준
- **Intel SGX (Software Guard Extensions)**: Flush+Reload로 부터 보호되는 enclave memory 영역을 제공한다.
- **AMD SEV (Secure Encrypted Virtualization)**: VM 전체를 encryption하여 Flush+Reload attack을 방지한다.
- **KPTI (Kernel Page Table Isolation)**: user-kernel 간 page table을 분리하여 Meltdown attack을 방지한다.
- **Constant-Time Cryptography (BoringSSL, libsodium)**: timing attack 방지를 위한 필수 구현 표준이다.

Flush+Reload는 메모리 공유라는 OS 최적화의 이면을 利用한 정교한 side-channel attack이다. 그러나 KPTI, enclave, constant-time implementation 등의 방어 기법이成熟됨에 따라, 이 attack의 실효성은 점차 감소하고 있다. 앞으로는 hardware-assisted isolation와 formal verification 기반의 side-channel 없는 시스템设计으로, 이 분쟁은根本적으로 해결될 것으로期待된다.

> 📢 **섹션 요약 비유**: Flush+Reload의防御は「shared libraryという共用図书馆に、特別な読み取り禁止フィルター（enclave）を設置し、他の読者が何を読んでいるかを一切识别できないようにする」技術である。 将来は、この фильтр）がハードウェアに組み込まれ、追加の設定없이自動的に保護されるようになる.

---

### 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Meltdown (CVE-2017-5754)** | Flush+Reload를 핵심 유출 수단으로 사용하는 대표적인 speculative execution 공격이다. |
| **Spectre (CVE-2017-5753)** | Prime+Probe와 결합하여 브라우저等的 잠재적 공격 경로를拓く Spectre 계열 공격이다. |
| **CLFLUSH** | Flush+Reload 공격의 첫 단계에서 사용되는 x86 명령어로, 특정 캐시 라인을 evict한다. |
| **KPTI (Kernel Page Table Isolation)** | Meltdown 방어를 위해 user-space와 kernel page table을 분리하는 kernel 방어 기법이다. |
| **Constant-Time Comparison** | Timing attack 방지를 위해 비밀번호 비교 시간을 고정하는 cryptography 구현 표준이다. |
| **Confidential Computing (SGX/SEV)** | Flush+Reload로 부터 보호되는 enclave 기반的安全執行環境이다. |

---

### 👶 어린이를 위한 3줄 비유 설명
1. 우리 학교에서는 여러 학급이 같은 교과서(공유 라이브러리)를 같이 써요. 어떤 아이가 교과서 50페이지를翻了ら, 다른 아이가 그 페이지의 미세한 접힌 자국(캐시 흔적)을 보고 "아! 네가 방금 50페이지在学习했구나!"라고 알아채는 거예요.
2. 이것을利用하면 시험 답안지를盗贼가 침투해서 친구가 푼 답을 전부 알아낼 수 있어요. 그래서 학교에서는 이 방법을 방지하려고 여러 방법을 쓰고 있어요.
3. 하지만 이것은 매우 교묘한 方法이라, 아직도 완벽하게 방지하기 어려운 computer 보안의 오래된 문제 중 하나예요!
