+++
weight = 666
title = "666. SASE (Secure Access Service Edge)"
date = "2026-03-16"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "SASE", "Secure Access Service Edge", "네트워크 보안", "SD-WAN", "SSE"]
+++

# SASE (Secure Access Service Edge)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SASE는 **네트워크(SD-WAN)과 보안(SSE)을 클라우드에서 통합**한 서비스로, **어디서나 안전한 액세스**를 제공한다.
> 2. **가치**: "MPLS 허브 앤 스포크 대신 클라우드"로 **비용 절감**하고, **원격 근무 시대**에 **데이터센터 없는 보안**을 제공한다.
> 3. **융합**:** ZTNA**, **CASB**, **SWG**, **FWaaS**가 통합된 **Security Service Edge(SSE)**에 **SD-WAN**가 결합된 형태다.

---

## Ⅰ. SASE의 개요

### 1. 정의
- SASE는 네트워크와 보안 기능을 **클라우드 기반 서비스**로 제공하는 아키텍처다.

### 2. 등장 배경
- 2019년 Gartner 개념화
- 원격 근무, 클라우드 보급

### 3. 💡 비유: '보안 클라우드'
- SASE는 **"보안과 네트워크를 클라우드 서비스로"** 제공한다.
- 물리 설비 없이 구돌이로 전달.

---

## Ⅱ. 구성 요소 (Deep Dive)

### 1. SSE (Security Service Edge)
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                      SSE 구성 요소                              │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [ZTNA] Zero Trust Network Access                              │
    │   - 애플리케이션 접근 제어                                      │
    │                                                                 │
    │  [CASB] Cloud Access Security Broker                           │
    │   - SaaS 보안 (Shadow IT 발견, DLP)                            │
    │                                                                 │
    │  [SWG] Secure Web Gateway                                     │
    │   - 웹 필터링, 악성 URL 차단                                   │
    │                                                                 │
    │  [FWaaS] Firewall as a Service                                 │
    │   - 클라우드 방화벽                                            │
    │                                                                 │
    │  [DLP] Data Loss Prevention                                   │
    │   - 데이터 유출 방지                                           │
    │                                                                 │
    │  [RBI] Remote Browser Isolation                               │
    │   - 위험 웹사이트 격리 브라우징                                │
    └─────────────────────────────────────────────────────────────────┘
```

### 2. SD-WAN
- 소프트웨어 정의 WAN
- 경로 최적화

---

## Ⅲ. 아키텍처

### 1. PoP(Point of Presence)
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                    SASE PoP 구조                                │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │   User ──▶ [Nearest PoP] ──▶ [SASE Cloud] ──▶ [App/Data]     │
    │                     │                                         │
    │                     ▼                                         │
    │              [Security Stack]                                │
    │              + SD-WAN Optimization                           │
    │                                                                 │
    │  * 전 세계 수십~수백 개 PoP                                 │
    └─────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용

### 1. 주요 제공업체
- Cisco, VMware, Palo Alto, Zscaler

---

## Ⅴ. 기대효과 및 결론

### 1. 정량/정성 기대효과
- **비용 절감**: MPLS 대비
- **성능**: PoP에 가까운 경로

---

## 📌 관련 개념 맵
- **[제로 트러스트](./665_zero_trust.md)**: 보안 원칙
- **[클라우드](../16_distributed_systems/xxx_cloud.md)**: 인프라

---

## 👶 어린이를 위한 3줄 비유 설명
1. SASE는 **"보안을 클라우드 서비스로 받는 것"** 같아요.
2. 각자의 집에 경비원을 두는 대신, 보안 회사가 클라우드로 해주는 거죠.
3. 어디서든 안전하게 인터넷을 쓸 수 있어서 요즘 많이 쓴답니다!
