+++
weight = 667
title = "667. SSD 보안 (SSD Security)"
date = "2026-03-16"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "SSD 보안", "데이터 삭제", "암호화", "ATA Security", "Sanitize"]
+++

# SSD 보안 (SSD Security)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SSD는 **쓰기 불가 페이지 마킬(Wear Leveling)**, **오정정(Over-Provisioning)**, **복구 블록** 등으로 인해 **데이터 완전 삭제가 어렵다**.
> 2. **가치**: "SSD를 폐기할 때 데이터 유출 방지"가 중요하며, **암호화, ATA Secure Erase, 물리 파괴**가 안전한 처리 방법이다.
> 3. **융합**:**Self-Encrypting Drive(SED)**, **TCG Opal** 표준이 SSD 보안을 위한 **하드웨어 암호화**를 제공한다.

---

## Ⅰ. SSD 보안의 개요

### 1. 정의
- SSD의 저장 특성으로 인한 **데이터 삭제 복잡성**과 **암호화**가 핵심 보안 문제다.

### 2. 등장 배경
- SSD 보급으로 HDD 보안 방법(삭제)이 부족

### 3. 💡 비유: '지워지지 않은 연필 자국'
- SSD는 **"지워 개도 흔적이 남는 매직 판"**과 같다.
- 쓰기 불가 영역에 데이터가 남을 수 있다.

---

## Ⅱ. 데이터 삭제 문제 (Deep Dive)

### 1. 왜 삭제가 어려운가?
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │              SSD 데이터 삭제 문제                                │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [FTL Translation Layer]                                       │
    │   Logical Block 0 ─▶ Physical Block 100                        │
    │   Logical Block 1 ─▶ Physical Block 250                        │
    │   * 파일 삭제 시 Logical Block만 해제                           │
    │   * Physical Block의 데이터는 남음                              │
    │                                                                 │
    │  [Wear Leveling]                                              │
    │   - 쓰기 불가 페이지를 다른 곳으로 복사                           │
    │   - 원본 데이터이 사라지지 않음                                 │
    │                                                                 │
    │  [Over-Provisioning]                                          │
    │   - 사용자에게 보이지 않는 예비 영역                            │
    │   - 삭제된 데이터가 여기에 남을 수 있음                           │
    │                                                                 │
    │  [Error Correction]                                            │
    │   - 데이터 복구용으로 복사본 보존                               │
    └─────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 안전한 삭제 방법

### 1. ATA Secure Erase
```bash
# hdparm으로 Secure Erase
hdparm --user-master u --security-set-pass EraseDisk /dev/sdX
hdparm --user-master u --security-erase /dev/sdX
```

### 2. Sanitize (_blkdiscard)
```bash
blkdiscard --secure /dev/sdX
```

### 3. 물리 파괴
- 분쇄, 소각

---

## Ⅳ. SSD 암호화

### 1. Self-Encrypting Drive (SED)
- 하드웨어로 자동 암호화
- **TCG Opal** 표준

### 2. OS 암호화
- BitLocker, LUKS

---

## Ⅴ. 실무 적용

### 1. 폐기 절차
1. 백업 확인
2. 암호화 확인
3. Secure Erase 실행
4. 파기

---

## Ⅵ. 기대효과 및 결론

### 1. 정량/정성 기대효과
- **데이터 유출 방지**

---

## 📌 관련 개념 맵
- **[암호화](./574_encryption.md)**: 전체 디스크 암호화
- **[파일 시스템](../8_file_systems/xxx_filesystems.md)**: 삭제 문제

---

## 👶 어린이를 위한 3줄 비유 설명
1. SSD 보안은 **"일기장을 안전하게 폐기"** 같아요.
2. 펜으로 쓴 내용은 지우개로 지워도 흔적이 남을 수 있죠.
3. 그래서 안전하게 잠금(암호화)을 하거나 불태워서(물리 파괴) 지워야 해요!
