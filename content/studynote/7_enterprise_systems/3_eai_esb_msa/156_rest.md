+++
weight = 160
title = "156. REST (Representational State Transfer)"
date = "2026-04-09"
description = "복잡한 프로토콜(SOAP) 없이 HTTP가 가진 메서드와 명사(URI) 본연의 특징만을 이용해 자원(상태)을 CRUD 조작하는 가볍고 우아한 웹 아키텍처 스타일"
[extra]
categories = "studynote"
+++

# 156. REST (Representational State Transfer)

## 핵심 인사이트 (3줄 요약)
> 1. Roy Fielding이 정의한 REST는 시스템 통합 시 무겁게 편지봉투(XML Envelope)를 규격화하는 SOA 사상을 버리고, **"HTTP를 원래 설계 목적대로 리소스 중심에 맞춰 심플하게 쓰자"**는 마이크로 분산망의 황금 규칙이다.
> 2. 클라이언트-서버 간 무상태성(Stateless)을 강제하여 서버의 메모리 부하를 없애고 스케일 아웃 파티션을 무한히 가능하게 하는 클라우드 인프라의 필수 코어다.
> 3. 행위(동사 GET/POST/PUT)와 자원(명사 URI /users/1)을 철저히 분리 명세하여 캐싱 메커니즘을 100% 흡수 수용하는 성능 우위를 자랑한다.

---
## Ⅰ. 아키텍처 및 원리
```text
  [ REST 아키텍처 CRUD 뷰 ]
   조회(Read)   : GET /customers/7            <-- (상태: 불변, 캐싱 캐시 장착 O)
   생성(Create) : POST /customers + (Data)
   수정(Update) : PUT /customers/7 + (Data)
   삭제(Delete) : DELETE /customers/7
```
---
## Ⅱ. 실무 적용 및 결론
이기종 백엔드망 통합이나 모바일 앱 통신 API를 열 때 RESTful 규격은 업계의 호흡과도 같다. 리소스 네이밍의 일관성과 명사형 URI 설계 지침을 통합 관철해 내는 구조적 설계 장악력이 인터페이스 결함(404, 500) 버그 파이프를 자르는 최선봉이다.
