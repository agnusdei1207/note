+++
title = "212-218. 현대적 분산 아키텍처 (MSA, Hexagonal, Clean)"
description = "서비스 중심의 MSA/EDA 아키텍처와 유연한 설계를 위한 헥사고날, 클린 아키텍처 분석"
date = 2026-03-14
[extra]
subject = "SE"
category = "Architecture & Design"
id = 212
+++

# 212-218. 현대적 분산 아키텍처 (MSA, Hexagonal, Clean)

> **핵심 인사이트**: 거대한 공룡(Monolithic)은 멸종하고 작은 포유류(Microservices)들이 세상을 지배한다. 서비스를 잘게 쪼개어 독립적으로 운영하는 MSA와, 비즈니스 로직(Core)을 외부 기술(DB, 웹)로부터 철저히 보호하는 클린 아키텍처는 변화무쌍한 비즈니스 환경에서 살아남기 위한 필수 전략이다.

---

## Ⅰ. 서비스 중심 아키텍처의 진화
1. **SOA (Service Oriented Architecture)**: 서비스를 비즈니스 단위로 정의하고 재사용. 주로 **ESB (Enterprise Service Bus)**라는 중앙 통로를 통해 통신.
2. **MSA (Microservices Architecture)**: 서비스를 더 작게 쪼개고, 각 서비스가 **자체 DB**를 가짐. 중앙 통로 없이 가벼운 HTTP/REST로 통신하며 독립적 배포가 가능.

---

## Ⅱ. 이벤트 중심 아키텍처 (EDA)
시스템 상태의 변화(Event)를 감지하고 이에 반응하는 방식입니다.
* **특징**: 송신자와 수신자가 서로를 몰라도 됨 (Decoupling). 비동기 처리를 통해 성능과 확장성이 매우 뛰어남.

---

## Ⅲ. 유연한 구조를 위한 아키텍처

### 1. 헥사고날 아키텍처 (Hexagonal / Ports and Adapters)
* **핵심**: 비즈니스 로직은 중앙에 있고, 외부 세계(DB, UI, 외부 API)와는 **포트(Port)**와 **어댑터(Adapter)**를 통해서만 연결됨. 
* **장점**: 외부 기술이 바뀌어도(예: Oracle $\rightarrow$ MySQL) 중앙의 핵심 코드는 전혀 수정할 필요가 없음.

### 2. 클린 아키텍처 (Clean Architecture - Robert C. Martin)
* **구조**: 엔티티(Entity) $\rightarrow$ 유스케이스(Use Case) $\rightarrow$ 인터페이스 어댑터 $\rightarrow$ 프레임워크/드라이버 순의 원형 구조.
* **의존성 규칙**: 의존성은 항상 **안쪽(비즈니스 핵심)을 향해서만** 흘러야 함. 고수준 정책이 저수준 상세 구현에 의존하지 않게 함.

---

## Ⅳ. 개념 맵 및 요약

```ascii
[클린 아키텍처의 의존성 방향]

  (외부) [ Frameworks / UI / DB ] 
           │
           ▼ ( 의존성 방향 )
  (중간) [ Controllers / Gateways ]
           │
           ▼
  (핵심) [ Entities / Use Cases ] (변하지 않는 비즈니스 룰)
```

📢 **섹션 요약 비유**: **MSA**는 거대한 한 척의 배 대신, 수많은 작은 보트들이 선단을 이뤄 나가는 것입니다. 한 대가 고장 나도 전체 항해는 멈추지 않죠. **헥사고날/클린 아키텍처**는 노트북의 메인보드(비즈니스 로직)와 USB 포트(Port)의 관계와 같습니다. 마우스나 키보드(Adapter)를 무엇을 꽂든 메인보드는 상관없이 제 할 일을 하는 아주 유연한 구조입니다. **EDA**는 누군가 벨을 누르면(이벤트) 집안의 모든 사람이 각자 할 일을 하는 '자율 반응형 시스템'과 같습니다.
