+++
weight = 660
title = "660. 침입 탐지 시스템 (IDS/IPS)"
date = "2026-03-16"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "IDS", "IPS", "침입 탐지", "Intrusion Detection", "Snort", "Suricata"]
+++

# 침입 탐지 시스템 (IDS/IPS)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: IDS/IPS는 **네트워크/시스템 트래픽을 분석**하여 공격 패턴을 탐지하고 **IPS는 능동적 차단**까지 수행하는 보안 시스템이다.
> 2. **가치**: "방화벽만으로는 부족, 내부 트래픽과 응용계층 공격도 탐지 필요"하며, **시그니처 기반 + 이상 탐지**를 결합한다.
> 3. **융합**: **NIDS(네트워크)**, **HIDS(호스트)**, **SaaS(Security as a Service)** 형태로 제공되며, **Snort, Suricata, OSSEC**가 대표적이다.

---

## Ⅰ. IDS/IPS의 개요

### 1. 정의
- **IDS**: 침입 탐지만 수행
- **IPS**: 탐지 + 차단(In-line)

### 2. 등장 배경
- 1980년대 James P. Anderson이 IDS 개념 제시

### 3. 💡 비유: 'CCTV와 보안 요원'
- IDS는 **"CCTV로 감시만 하는 보안 요원"**,
- IPS는 **"CCTV + 직접 체포하는 경비원"**과 같다.

---

## Ⅱ. 탐지 방식 (Deep Dive)

### 1. 시그니처 기반
- 알려진 공격 패턴 매칭

### 2. 이상 탐지
- 기계 학습으로 비정상 행동 탐지

---

## Ⅲ. Snort/Suricata

### 1. Snort 규칙
```text
alert tcp any any -> any 80 (
  msg:"SQL Injection Attempt";
  content:"UNION SELECT";
  sid:1000001;
)
```

---

## Ⅳ. 실무 적용

### 1. 배치
- **Perimeter**, **Internal**, **Cloud**

---

## Ⅴ. 기대효과 및 결론

### 1. 정량/정성 기대효과
- **공격 조기 발견**: 피해 최소화

---

## 📌 관련 개념 맵
- **[보안 정책](./577_security_policies.md)**: 규칙
- **[악성코드](./578_malware.md)**: 탐지 대상

---

## 👶 어린이를 위한 3줄 비유 설명
1. IDS/IPS는 **"경비원과 CCTV"** 같아요.
2. 경비원은 나쁜 사람을 발견하면 알리고(IPS), 잡기도 해요.
3. 덕분에 우리 집(컴퓨터)을 안전하게 지킬 수 있답니다!
