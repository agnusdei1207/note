+++
weight = 662
title = "662. 침입 탐지/방지 시스템 (IDS/IPS)"
date = "2026-03-16"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "IDS", "IPS", "침입 탐지", "침입 방지", "Snort", "Suricata"]
+++

# 침입 탐지/방지 시스템 (IDS/IPS)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: IDS(Intrusion Detection System)는 공격을 **탐지**하고, IPS(Intrusion Prevention System)는 **탐지 + 차단**까지 수행하는 네트워크 보안 시스템이다.
> 2. **가치**: "방화벽은 포트만 보지만, IDS/IPS는 **내용까지 검사**"하여 **SQL Injection, XSS, 공격 패턴**을 탐지/차단한다.
> 3. **융합**: 시그니어 기반(알려진 공격)과 이상 탐지(미지 공격)를 결합하며, **NIDS**(네트워크)와 **HIDS**(호스트)로 분류된다.

---

## Ⅰ. IDS/IPS의 개요

### 1. 정의
- **IDS**: 공격 감지, 알림
- **IPS**: 공격 차단(In-line)

### 2. 등장 배경
- 1998년 Martin Casado가 Snort 개발

### 3. 💡 비유: 'CCTV와 경비'
- IDS는 **CCTV로 감시**, IPS는 **직접 체포**하는 경비와 같다.

---

## Ⅱ. 탐지 방식 (Deep Dive)

### 1. 시그니처 기반
- 알려진 공격 패턴 매칭

### 2. 이상 탐지
- 기계 학습으로 비정상 행동 탐지

---

## Ⅲ. 주요 도구

### 1. Snort
```text
alert tcp any any -> any 80 (
  msg:"WEB-MISC /etc/passwd";
  content:"/etc/passwd";
  sid:100002;
)
```

### 2. Suricata
- 멀티스레딩 지원

---

## Ⅳ. 실무 적용

### 1. 배치
- 경계, 내부, 클라우드

---

## Ⅴ. 기대효과 및 결론

### 1. 정량/정성 기대효과
- **공격 조기 발견**

---

## 📌 관련 개념 맵
- **[방화벽](./661_firewall.md)**: 1계층 방어
- **[악성코드](./578_malware.md)**: 탐지 대상

---

## 👶 어린이를 위한 3줄 비유 설명
1. IDS/IPS는 **"경비원과 CCTV"** 같아요.
2. 나쁜 사람을 발견하면 경보를 울리고(IPS), 직접 잡기도 해요.
3. 24시간 감시해서 우리 집을 안전하게 지켜줘요!
