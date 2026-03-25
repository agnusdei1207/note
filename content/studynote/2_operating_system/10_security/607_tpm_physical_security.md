+++
title = "607. TPM (Trusted Platform Module) 및 물리적 보안"
date = "2026-03-25"
[extra]
categories = "studynote-operating-system"
+++

# TPM (Trusted Platform Module) 및 물리적 보안

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TPM은 마더보드에搭载된 별도의 물리적 보안 칩으로, 암호화 키를 하드웨어적으로 생성 저장 관리하여 소프트웨어 공격(루트킷, 키로거)으로부터 핵심 비밀(Disk Encryption Key, 인증서)을 격리하는 신뢰의 기반이다.
> 2. **가치**: TPM은 부팅 과정에서 펌웨어와 운영체제의 무결성을 측정하여, 사용자의 비밀번호와 물리적 보안이 모두 무사하더라도 펌웨어 레벨의 손상이 있다면 복호화를 거부하는 하드웨어 기반의 영구적 방어선을 제공한다.
> 3. **융합**: TPM의 신뢰 측정(Root of Trust Measurement)은 BIOS/UEFI 보안 부팅(Secure Boot)과 결합되어, 서명되지 않은 부트로더나 커널을 원천 차단하고, BitLocker 등 디스크 암호화와 연동되어 TPM에 저장된 키로 볼륨 마스터 키를 보호하는 종단 간 보안 체인을 완성한다.

---

## 1. 개요 및 필요성

### 개념 및 정의
TPM (Trusted Platform Module)은 PC나 서버의 마더보드에 납땜 방식으로 부착된 단일 칩 보안 장치로, TCG (Trusted Computing Group)가 제정한 국제 표준에 따라 제조된다. TPM은 난수 생성기, SHA-1/SHA-256 해시 엔진, RSA/ECC 암호화 가속기, 최소 16KB의 물리적 비휘발성 메모리가 있는 소형 마이크로컨트롤러로 구성되며, 핵심 임무는 암호화 키를 절대 칩 외부로 출력하지 않고 내부에서만 연산하는 것이다. 이 특성 때문에 TPM 내부에서 생성된 키는 TPM이 물리적으로 파괴되지 않는 한 소프트웨어 공격으로 도용할 수 없는 암호학적 앵커가 된다.

**필요성 및 등장 배경**
소프트웨어만으로는 시스템 보안을 달성할 수 없는 근본적 한계가 있다. 첫째, 모든 소프트웨어는 메모리에 로드되어 실행되므로, 메모리를 읽을 수 있는 권한(예: 커널 루트 권한)을 획득한 공격자는 비밀 키를 평문으로 추출할 수 있다. 둘째, 부팅 과정에서 BIOS나 부트로더가 손상된 경우, 운영체제가 아무리 안전해도 감염된 도어맨이 열쇠를 넘겨주는 격이다. 셋째, AES 키를 운영체제가 메모리에 평문으로 올려두면, cold boot attack처럼 RAM 내용을 휘발 전에 동결하여 키를 뽑아내는 물리적 공격이 가능하다. 이 세 가지 소프트웨어적 한계를 동시에 관통하는 하드웨어 수준의 격리 장치가 필요했고, TPM은 그 해답으로 등장했다.

```
[TPM vs 소프트웨어 전용 암호화의 위협 모델 비교]

[소프트웨어 전용 암호화 (예: VeraCrypt)]
- 디스크 암호화 키(DEK)가 AES로 보호됨
- BUT: 부팅 시 OS가 DEK를 RAM에 평문으로 로드함
- 공격 경로: 런타임 메모리 탈취 / 부트로더 악성 감염

[TPM + BitLocker 연동 암호화]
- TPM이 Volume Master Key(VMK)를 내부에 안전하게 보관
- VMK는 TPM 외부로 평문 출력 불가
- 부팅 무결성 측정(PCR)이 성공해야만 VMK가 해제됨

[부팅 과정의 물리적 무결성 측정 흐름]

BIOS/UEFI --> 측정 --> PCR[0]에 누적 해시 저장
     |
     v
Bootloader --> 측정 --> PCR[1]에 누적 해시 저장
     |
     v
Kernel --> 측정 --> PCR[2]에 누적 해시 저장
     |
     v
PCR 값이 사전 등록된 "정상 상태 해시"와 비교!
     |
     +-- 일치 --> TPM이 VMK 해제 --> OS 정상 부팅
     +-- 불일치 --> TPM이 VMK 보호 --> 복호화 거부!
```

**[다이어그램 해설]** 이 구조는 TPM이 왜 "신뢰의 기반(Root of Trust)"이라 불리는지를 보여준다. TPM은 자신이 직접 모든 것을 검증하는 것이 아니라, 부팅 과정에서 각 단계(BIOS --> Bootloader --> Kernel)가 실행되기 직전에 해당 소프트웨어의 해시 값을 PCR(Platform Configuration Register)에 누적 저장한다. BitLocker Recovery模式下, TPM은 VMK를 내놓으라는 요청이 들어오면 PCR 값이出厂時に封印했던 정상 상태의 해시와 현재 PCR 값을 비교한다. 만약 해커가 BIOS를 변조하거나 루트킷이 커널에 감염되었다면 PCR 값이 정상 해시와 달라지므로, TPM은 VMK를 절대 해제하지 않는다. 이것이 소프트웨어만으로는 달성할 수 없는 하드웨어 봉인의 물리적 보장이다.

- **요약 비유**: 소프트웨어 암호화는 금고 비밀번호를 잘 외운 사람이라면 누구나 열 수 있는 고급 자물쇠과 같다. TPM 기반 암호화는 금고 안에 다른 자물쇠가 하나 더 있어서 금고 문을 열기 전에 "지금 내 눈앞에 서 있는 사람이 진짜 주인인가?"를 금고가 직접 확인하는 것이다. 소프트웨어는 속일 수 있지만, 칩은 속일 수 없다.

---

## 2. 아키텍처 및 핵심 원리

### TPM 칩의 내부 구성 요소

TPM은 단일 칩 안에 여러 보안 기능이 융합된 소형 마이크로컨트롤러다.

| 요소명 | 역할 | 내부 동작 | 비유 |
|---|---|---|---|
| **RSA/ECC 가속기** | 공개키 암호 연산 가속 | TPM 내부에서 키 생성, 서명, 검증 수행 (키 평문이 칩 외부로 나오지 않음) | 금고 내부의 자동 비밀번호 생성기 |
| **SHA-1/SHA-256 엔진** | 해시 연산 가속 | 부팅 측정 과정의 HMAC 누적 계산 및 PCR 갱신 | 도장 찍는 직원 |
| **RNG (Random Number Generator)** | 암호학적으로 안전한 난수 생성 | TPM 내부 entropy source 기반 키 생성, nonce creation | 주사위를 굴리는 무작위 추출기 |
| **NVRAM (Non-Volatile RAM)** | 영구 저장소 | Endorsement Key, SRK, storage 키, PCR 값의 물리적 저장 | 금고 안의 불사조 종이 |
| **PCR (Platform Configuration Register)** | 부팅 무결성 측정 값 저장 | 24개의 20바이트 레지스터 (TPM 1.2 기준), 각 단계별 해시 누적 저장 | 입국 심사 도장 찍힌 여권 페이지 |
| **Endorsement Key (EK)** | TPM 제조 시 내장된 고유 RSA 키 | TPM 정품 증명, remote attestation에 사용 | 주민등록증에 내장된 신원증 |
| **Storage Root Key (SRK)** | 사용자 키의 최상위 부모 키 | TPM 소유자 생성 시 2048-bit RSA 쌍으로 생성, master key 역할 | 금고 Master 열쇠 |

### TPM의 핵심 cryptographic operation: Seal과 Unseal

TPM의 가장 독창적인 특성은 "데이터를 TPM에 봉인(Seal)하고, 특정 상태에서만 해제(Unseal)한다"는 것이다.

```
[TPM Seal / Unseal 메커니즘의 내부 동작 흐름]

[Seal 작업 (데이터 봉인 단계)]

Owner: "BitLocker 키를 TPM에 봉인해줘"
         |
         v
TPM 내부 동작:
  1. 난수 생성기로 대칭 키(DEK) 생성
  2. DEK를 TPM 내부 RSA 엔진으로 암호화하여 NVRAM 저장
  3. DEK의 복호화 조건(PCR 값: 정상 부팅 해시)을 함께 기록
  4. DEK 평문은 절대 TPM 외부로 출력되지 않음!

[Unseal 작업 (데이터 해제 단계)]

부팅 완료 --> PCR[0~7]에 정상 부팅 누적 해시 저장
         |
         v
OS가 BitLocker에게 "복호화해줘"라고 요청
         |
         v
TPM 내부:
  1. 현재 PCR 값 vs 봉인 당시 PCR 값 비교
  2. 값이 동일 --> DEK 복호화 (Unseal) --> OS에 전달
  3. 값이 다름 --> 복호화 거부! (공격 감지)

핵심: PCR 값이 하나라도 다르면 TPM이 DEK를 절대 내놓지 않음
```

**[다이어그램 해설]** Seal/Unseal 메커니즘은 TPM의 보안 철학을 가장 잘 보여주는 조작이다. 일반적인 소프트웨어 암호화에서는 "비밀번호만 맞으면 복호화"이지만, TPM은 "비밀번호(키)와 함께 현재 시스템 상태(PCR)가 봉인 시점과 동일해야 복호화"라는 조건부 보안 모델을 구현한다. 만약 해커가 BitLocker로 암호화된 노트PC의 SSD를 빼서 다른 PC에 연결하면, 해당 PC의 TPM은 원래 부팅 측정 값을 가지고 있지 않으므로 VMK를 절대 해제하지 않는다. PCR 값을事前に登録した正常値와 비교하는 이 동작이, 펌웨어 레벨의 손상까지 검출하는 "상태 인식 보안(Stateful Security)"의 핵심 원리다.

### Endorsement Key와 Remote Attestation

TPM의 또 다른 중요한 역할은 remote attestation, 즉 "이 시스템이 현재 정직한 상태임을 원격 서버에 증명하는 것"이다. 이를 가능하게 하는 것이 Endorsement Key (EK)다.

TPM manufacturing 시 공장에서 기록된 2048-bit RSA 키 쌍으로, TPM의 일련번호와 binding되어 있어 TPM 칩이正品임을 cryptographic하게 증명하는 신분증 역할을 한다. EK는 TPM 외부로 export 불가하며, EK의 개인키는 절대 TPM 밖으로 나갈 수 없다.

```
[Remote Attestation (원격 증명)의 전체 흐름]

[단계 1: AIK (Attestation Identity Key) 생성]
사용자 PC --> TPM에게 "AIK 생성해줘" 요청
TPM: EK를 사용하여 AIK에 서명 후, AIK 공개키를 인증서로 발급

[단계 2: 부팅 무결성 측정 값 수집]
부팅 과정에서 PCR[0~7]에 누적된 해시 값을 AIK로 서명
서명된 PCR 값 = "이 PC는 현재 이 소프트웨어 구성으로 부팅됨"

[단계 3: 원격 검증 서버에 증명]
서명된 PCR 값 --> 원격 서버로 전송
원격 서버:
  1. EK 인증서 검증 (TPM正品 확인)
  2. 서명된 PCR 값 검증 (변조 확인)
  3. PCR 값이 known-good baseline과 비교
  4. 일치하면 "이 PC는 안전합니다" 판단

활용처:
- 기업 VPN 접속 시 순수한 기업 제공 OS인지 검증
- 온라인 은행 접속 시 키로거 없는 깨끗한 환경인지 검증
- 클라우드 VM이 생성될 때 올바른 베이스 이미지로 시작했는지
```

**[다이어그램 해설]** Remote attestation은 "신뢰한 hardware에서 신뢰한 software가 실행되고 있다"는 사실을 제3자(원격 서버)가 cryptographic하게 검증하는 프로토콜이다. 핵심은 EK (Endorsement Key)가 TPM 칩의 manufacturing 단계에서 기록된ものであり、TPMが物理的に破壊されない限り鏹によって偽造될 수 없다는 점이다. 따라서 해커가 OS를 루트킷으로 오염시켜도, 원격 서버는 PCR 값의 서명 검증 과정에서 이를 감지할 수 있다. 이 기술은ゼロトラスト (Zero Trust) 네트워크의 핵심 구성 요소로, "내부 네트워크에 있다 = 신뢰한다"는 전통적 가정을 제거한다.

- **요약 비유**: TPM은 컴퓨터 세계의 주민등록증과 같다. 주민등록증(Endorsement Key)을 가지고 있는正規인만(정품 TPM), 출입 카드(AIK)를 만들 수 있고, 출입 카드를 스캔하면 "오늘 옷차림이정상적인가(PCR 무결성)"를 동시에 확인하여, 신원 도용이나 복장 불량 중 하나라도 있으면 건물 출입을 차단한다.

---

## 3. 융합 비교 및 다각도 분석

### TPM 버전별 기능 비교 (TPM 1.2 vs TPM 2.0)

| 비교 항목 | TPM 1.2 | TPM 2.0 |
|---|---|---|
| **암호화 알고리즘** | RSA 2048-bit, SHA-1 (고정) | RSA 2048 + ECC (P-256, P-384), SHA-1/256/384 (알고리즘 선택 가능) |
| **PCR 레지스터 수** | 24개 (PCR[0~23]) 고정 | 32개 이상 (벤더 확장 가능), 동적 확장 |
| **키 관리** | 단일 hierarchical 모델 (EK --> SRK --> Storage) | 유연한 hierarchical 모델 (Primary Seed, Platform Seed) |
| **권한 관리** | 단일 owner password 방식 | 복잡한 authorization session 구조 (HMAC, policy session) |
| **알고리즘 민첩성** | SHA-1에 잠겨있어 취약점 노출 시 업그레이드 불가 | 알고리즘을 software update로 교체 가능 |
| **범용성** | PC/server 특화 | PC, server, IoT, embedded system 모두 대응 |

TPM 1.2는 2000년대 초반 설계로, SHA-1 해시 함수에 심각한 취약점이 발견된 이후에도 하드웨어가 고정되어 있어 알고리즘을 업데이트할 수 없는 것이致命的 한계였다. TPM 2.0은 알고리즘을 firmware update로 교체할 수 있는 algorithm agility를 도입하여, SHA-1의 취약성이 발견되면 SHA-256으로 알고리즘을无缝 전환할 수 있다.

### TPM과 경쟁 기술 (Intel SGX, AMD SEV)의 비교

| 비교 항목 | TPM (칩셋 레벨) | Intel SGX (프로세서 내부) | AMD SEV (프로세서 레벨) |
|---|---|---|---|
| **보호 대상** | 부팅 무결성, 디스크 암호화 키, 인증서 | application memory region (Enclave) | entire VM memory |
| **보호 레벨** | 시스템 전체 (OS/BIOS 포함한 전체 플랫폼) | application 단위 (앱 개발자가 명시적으로 Enclave 지정) | VM 단위 (가상머신 전체 memory) |
| **격리 방식** | 물리적 별도 칩 (칩셋) | 프로세서 내부 격리 메모리 (PRM, Processor Reserved Memory) | AMD 프로세서의 메모리 암호화 엔진 (MSE) |
| **사용 시나리오** | BitLocker, secure boot, certificate storage | 비밀 계산 (secure computation), AI inference on encrypted data | cloud VM encryption (VM의 메모리 자체를 host에게도 숨김) |
| **물리적 공격 방어** | TPM 칩 물리적 파괴 필요 (상대적 강함) | cold boot attack에 대해 vulnerable (메모리가 CPU package 내부로 들어감) | 메모리 암호화로 cold boot attack 방어, but hypervisor 신뢰 필요 |

```
[보안 레이어별 protection scope 비교]

[가장 넓은 보호 범위] TPM 2.0
  [Platform: BIOS --> Bootloader --> OS --> App]
  TPM: 전 구간 무결성 측정 + 키 관리

[중간 보호 범위] AMD SEV
  [가상머신 memory 전체]
  SEV: VM <--> Host (하이퍼바이저) 간 메모리 암호화

[가장 좁은 보호 범위] Intel SGX
  [Application 내부의 Enclave만 격리]
  SGX: 특정 sensitive 코드/데이터만 Enclave에 격리

결론:
- 플랫폼 전반의 신뢰 기반 --> TPM
- VM 단위의 비밀 유지 --> AMD SEV
- 애플리케이션 단위의 비밀 계산 --> Intel SGX
```

**[다이어그램 해설]** 세 기술은 상호 배타적이지 않고互补적으로 작동한다. 실제 고급 보안 시스템에서는 TPM이 시스템의 부팅 무결성을 검증하고, 그 위에 실행되는 VM이 AMD SEV로 메모리 레벨 암호화를 적용하며, VM 내부의 매우 민감한 처리(예: AI 모델 inference)는 Intel SGX Enclave 내에서 수행하는 다중 방어 전략을 취한다.

- **요약 비유**: 세 기술의 관계는 집 전체의 방범 시스템과 같다. 집 방범 시스템(TPM)이 전체 동선을 감시하고, 대fur 금고는 가족 공용 재산을 보호하며, 방 내부 금고는 정말 개인적인秘密만을 보호한다. 모든 것이 함께 작동할 때 가장 안전한 주택가 된다.

---

## 4. 실무 적용 및 기술사적 판단

### 실무 시나리오: BitLocker TPM-only 복호화 우회 vs TPM+PIN 이중 보호

**시나리오 상황**:某 기업의 노트PC가 BitLocker TPM-only 모드로 설정되어 있다. IT 관리자는 "TPM이 있으니까 추가 인증 없이 OS만 부팅되면 자동으로 복호화"되도록 설정했다.某 날, 엔지니어의 노트PC가 도난되었다.

**엔지니어의 기대**: 도둑이 노트북을 켜도 TPM이 PCR 값을 인식하지 못하므로 복호화되지 않을 것이다.

**실제 결과**: 도둑이 노트북 SSD를 빼내어 다른 PC에 연결하거나, TPM 칩을 unsoldering하여 동일 모델 노트북의 TPM과 교환하면? 이 경우 PCR 값이 변조 없이 정상으로 인식되어 BitLocker VMK가 해제되어버린다!

**문제의 핵심**: TPM-only 모드는 "올바른 hardware에서 부팅"까지만 확인하고, "올바른 사람이 부팅"인지는 검증하지 않는다.

```
[BitLocker 인증 모드별 보안 수준 및 공격 시나리오 비교]

[모드 1: TPM-only]
보호 수준: 하드웨어만 확인, 인적 요소 미확인
공격 경로: TPM swap --> BitLocker 우회 가능!
복호화 조건: PCR[0~7] 정상 + 올바른 hardware

[모드 2: TPM + PIN] (권장)
보호 수준: hardware + 지식 요소 동시 검증
공격 경로: TPM swap + PIN 브루트포스 필요
복호화 조건: PCR 정상 + 올바른 hardware + 올바른 PIN

[모드 3: TPM + PIN + Recovery Key (escrow)]
보호 수준: 재해 회복 포함
실제 기업 환경에서는 Recovery Key를 AD에 escrow하여
관리자만 복구 가능하도록 설정하는 것이 일반적
```

### 도입 체크리스트 (기업 환경 TPM 보안 강화)

- **TPM + PIN 활성화**: BitLocker GPO(Group Policy Object)에서 "Require authentication via startup PIN" 정책을 활성화하여 hardware theft에 의한 BitLocker 우회를 원천 차단했는가?
- **Secure Boot 무결성 검증**: UEFI BIOS에서 Secure Boot를 활성화하고, Microsoft에서 서명한 부트로더만 허용하는 정책을 설정했는가?
- **TPM 2.0 업그레이드 검토**: 레거시 TPM 1.2 시스템은 SHA-1 취약점 대응을 위해 TPM 2.0으로 교체하거나 firmware update를 적용했는가?
- **재해 복구 시나리오**: TPM이 고장 나거나 마더보드가 손상되었을 때, BitLocker Recovery Key를 AD나 Azure AD에事前登録해두었는가?

### 안티패턴

- **TPM-only에만 의존하고 Secure Boot를 비활성화**: TPM이 PCR 값을 기반으로 키를 해제하지만, Secure Boot가 없으면 악성 커널도 정상 PCR 값을 생산할 수 있다. 즉, 커널 루트킷이 시스템에 깊이 뿌리내리면 PCR 값을 변조하지 않고도 BitLocker 키를 가로챌 수 있는 간접 경로가 생긴다.
- **TPM 칩을 비활성화하고 비밀번호만 사용**: 이는 역사적인 소프트웨어 암호화 방식인 BitLocker password-only mode로 돌아가는 것으로, cold boot attack에 의해 RAM에서 AES 키가抽出될 위험이 다시 생긴다.

- **요약 비유**: 방범 시스템(보안 소프트웨어)만 있고 도어록(TPM)을 제거한 집과 같다. hardware锁이 없으면 도어밖의 작은 창문(부트로더 변조)을 통해 집 안의 금고 열쇠(Disk Encryption Key)를 빼돌릴 수 있다. 반드시 hardware锁과密码(TPM+PIN)를 함께 사용해야 진정한 방범이 된다.

---

## 5. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | TPM 미사용 (소프트웨어 암호화만) | TPM 2.0 + Secure Boot + BitLocker |
|---|---|---|
| **정보 유출 방어** | 부트로더 악성 감염으로 평문 키 탈취 가능 | 부팅 과정에서 악성 변조 감지 시 복호화 거부 |
| **저장 데이터 보호** | SSD 탈착 후 다른 PC 연결 시 평문 노출 | SSD 탈착 후 TPM 미존재로 복호화 불가 |
| **인증 신뢰성** | 비밀번호 유출 시 100% 침해 | hardware (TPM) + 지식(PIN) 이중 요소 |
| **침해 대응** | 키 탈취 후 데이터 유출 즉시 발생 | 악성 부팅 시 temp key만 탈취, 사용자 알림 즉시 발생 |

### 미래 전망

TPM은 PC 플랫폼의 표준 보안 칩으로 자리 잡았지만, IoT 및 edge computing 환경에서는 여전히採用율이 낮다. 2024년 이후 NIST SP 800-193 ("Platform Firmware Resilience") 표준의 본격 시행과 함께, 모든 IoT 디바이스에도 TPM-Lite 또는 fTPM (firmware TPM)을 탑재하는 것이 규제 요건으로 확대되고 있다. 특히 자율주행 자동차, 의료기기, 산업 제어 시스템에서는 "부팅 무결성이 보장되지 않은 장비는 동작을 거부한다"는 fail-secure 정책이 법적 의무화되는 흐름이 가속화되고 있다.

또한 TPM 2.0의 알고리즘 민첩성은, Post-Quantum Cryptography 시대에 RSA/ECC를 PQC 알고리즘으로 교체해야 할 때, 하드웨어 교체 없이 TPM firmware update만으로 대응할 수 있는前瞻적설계를 가능하게 한다.

### 참고 표준

- **TCG (Trusted Computing Group) Specification**: TPM 1.2 / TPM 2.0 명령어 사양서
- **ISO/IEC 11889**: TPM의 국제 표준
- **NIST SP 800-147**: BIOS Protection Guidelines
- **NIST SP 800-193**: Platform Firmware Resilience

- **요약 비유**: TPM은 디지털 세계의 주민등록증과 같다. 주민등록증(TPM)이 없으면 출입 카드(AIK)도 만들 수 없고, 보안 출입을 증명할 수 없다. 이 주민등록증은 단순히 신원만 확인하는 것이 아니라, 오늘 몸 상태(부팅 무결성)를 확인하고, 모든 것이 정상이면 비서(키 관리자)에게 비밀金庫 열쇠를 건네주고, 하나라도 이상하면金庫 문을 굳게 닫아버리는聰명한 관리인이다.

---

## 관련 개념 맵

| 개념 명칭 | 관계 및 시너지 설명 |
|---|---|
| **Secure Boot** | TPM과 연동하여 서명되지 않은 부트로더와 커널의 실행을 UEFI 펌웨어 수준에서 원천 차단하는 하드웨어-소프트웨어 결합 보안이다. |
| **BitLocker** | TPM의 Seal/Unseal 메커니즘을 활용하여 OS 부팅 전 시스템 무결성을 검증하고, 검증 성공 시에만 VMK를 해제하는 Microsoft의 볼륨 암호화 솔루션이다. |
| **PCR (Platform Configuration Register)** | TPM 내부의 20바이트 레지스터로, 부팅 과정에서 BIOS, Bootloader, OS의 해시 값을 순차적으로 누적 저장하여 플랫폼의 무결성 상태를 cryptographic하게 기록한다. |
| **Endorsement Key (EK)** | TPM 제조 시 공장에서 내장된 2048-bit RSA 키 쌍으로, TPM正品 증명 및 Remote Attestation의 cryptographic identity로 사용된다. |
| **Intel SGX / AMD SEV** | TPM이 플랫폼 전체의 신뢰를 기반으로 하는 반면, SGX/SEV는 프로세서 내부 또는 VM 메모리 수준의 application 단위 격리를 제공하는 차세대 하드웨어 보안 기술이다. |

---

## 어린이를 위한 3줄 비유 설명
1. TPM은 컴퓨터 안에 있는 비밀 요정과 같다. 이 요정은 열쇠를 자기 몸 안(하드웨어 칩)에 숨겨두어서, 아무리 똑똑한 해커가 소프트웨어로 열쇠를盜もうとしても "나는 내 몸 안에서만 열쇠를 쓸 거야!" 하고 절대 밖으로 내어주지 않아요.
2. 그런데 이 비밀 요정은 그냥 막무가내로 열쇠를 주지 않는 게 아니라, 우선 "오늘 이 집(컴퓨터)이 건강하게 지어졌는가(부팅 무결성)"를 꼼꼼히 살피고, 예전에 세워둔 정상 집 구조와 지금의 구조를 비교해서, 하나라도 다르면 "안 돼! 누군가 집을 고쳐놨어!" 하고 복호화 키를 내어주지 않아요.
3. 그래서 열쇠를 받으려면 세 겹의 열쇠가 모두 맞아야 한다. 올바른Hardware(TPM)하고 올바른Software(정상 PCR)하고 올바른비밀번호(PIN)라는 세 겹의 열쇠가 모두 맞아야 집 문(디스크)이 열리는 엄청나게 완벽한 보안 시스템이에요!
