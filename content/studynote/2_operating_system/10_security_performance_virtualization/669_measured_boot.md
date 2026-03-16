+++
weight = 669
title = "669. Measured Boot (측정 부팅)"
date = "2026-03-16"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "Measured Boot", "PCR", "TPM", "부팅 무결성", "Remote Attestation"]
+++

# Measured Boot (측정 부팅)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Measured Boot는 **부팅 과정의 각 단계를 해싱하여 TPM의 PCR(Platform Configuration Register)**에 **기록(Measure)**하여 부팅 체인의 **무결성을 검증**하는 기술이다.
> 2. **가치**: "내 컴퓨터가 정말 내 것인가?"를 **암호적으로 증명**하며, 부트킷/루트킷 설치 여부를 **PCR 값**으로 판단할 수 있다.
> 3. **융합**: UEFI, Bootloader, Kernel, Initrd 각 단계가 **PCR에 해시를 기록**하며, **Remote Attestation**으로 원격 검증자가 PCR 값을 확인한다.

---

## Ⅰ. Measured Boot의 개요

### 1. 정의
- Measured Boot는 부팅 과정의 **코드를 해싱**하여 TPM에 **증거(Evidence)**로 남기는 과정이다.

### 2. 등장 배경
- Trusted Boot(인증 기반)의 한계: 서명 확인만

### 3. 💡 비유: '출입 기록부'
- Measured Boot는 **"건물 출입 기록부"**와 같다.
- 누가 언제 들어왔는지 모두 기록된다.

---

## Ⅱ. 동작 원리 (Deep Dive)

### 1. PCR (Platform Configuration Register)
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │              Measured Boot PCR 기록                             │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │   Power On ──▶ UEFI Firmware                                   │
    │              │                                                │
    │              └─ Extend PCR[0] = Hash(PCR[0] || Firmware_Hash)   │
    │                                                               │
    │              ──▶ Option ROMs                                   │
    │              │                                                │
    │              └─ Extend PCR[1] = Hash(PCR[1] || ROM_Hash)       │
    │                                                               │
    │              ──▶ Bootloader (GRUB)                             │
    │              │                                                │
    │              └─ Extend PCR[2~4] = Hash(PCR[x] || Boot_Hash)     │
    │                                                               │
    │              ──▶ Kernel                                       │
    │              │                                                │
    │              └─ Extend PCR[5~8] = Hash(PCR[x] || Kernel_Hash)   │
    │                                                               │
    │   * 각 PCR은 256비트(SHA-256) 해시                           │
    │   * Extend: PCR ← SHA256(PCR || new_hash)                     │
    └─────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. Remote Attestation

### 1. 검증 과정
- 클라이언트는 PCR 값과 TPM 서명을 전송
- 서버는 PCR이 예상 값과 일치하는지 확인

---

## Ⅳ. 실무 적용

### 1. IMA (Integrity Measurement Architecture)
```bash
# 파일 무결성 측정
echo "appraise func=IMA_MEASURE appraisal_type=imasig" > /etc/ima/ima-policy
```

---

## Ⅴ. 기대효과 및 결론

### 1. 정량/정성 기대효과
- **부팅 무결성 보장**

---

## 📌 관련 개념 맵
- **[신뢰 컴퓨팅](./654_trusted_computing.md)**: TPM
- **[Secure Boot](./655_secure_boot.md)**: 인증 기반 부팅

---

## 👶 어린이를 위한 3줄 비유 설명
1. Measured Boot는 **"출입 도장을 찍는 것"** 같아요.
2. 들어올 때마다 도장을 찍어서 "이 시간에 이 사람이 들어왔어"라고 기록하죠.
3. 나중에 보안 사고가 있으면, 누가 들어왔는지 도장으로 추적할 수 있답니다!
