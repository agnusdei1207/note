+++
weight = 161
title = "161. Level 3 - HATEOAS"
date = "2026-04-09"
description = "클라이언트가 서버의 주소 구조나 다음 동작 규칙을 사전에 아예 몰라도 되며 오직 하이퍼링크(Hypermedia)를 따라가며 자기 기술적 동작(Self-descriptive)을 일궈내는 REST 성숙도의 궁극적 지향점 트로피"
[extra]
categories = "studynote"
+++

# 161. REST 성숙도 Level 3 - HATEOAS

## 핵심 인사이트 (3줄 요약)
> 1. 아키텍트는 분리된 Level 2(명사+동사)를 넘어서, 서버가 API 응답 JSON 패킷 안에 **"네가 지금 상태에서 할 수 있는 다음 액션들(조회, 수정, 삭제)의 URL 링크 모음"** 을 동적으로 내려주는 가이드 레일 기능을 탑재한다(HATEOAS).
> 2. 클라이언트 앱은 서버 엔드포인트 주소가 나중에 무단 변경되거나 결제 프로세스가 바뀌어도, 그냥 응답 안의 `links.payment.href` 속성값을 눌러서 전송지만 하므로 프론트엔드의 재배포나 코드 수정이 0건이 된다. 완벽한 디커플링 보장망.
> 3. 이상향이지만 무거운 페이로드 부하와 응답 가이드 생성 로직 처리 비용 때문에 최상위 금융 플랫폼이나 매우 엄격한 MSA 도메인 코어가 아니고서는 도입을 포기한다.

---
## Ⅰ. 아키텍처 및 원리
```text
  [ HATEOAS 응답 트리 예시 (Self-descriptive Message) ]
   GET /hotel/rooms/55 
   { "roomInfo": "Suite",
     "_links": {           -----> (여기서부터 스스로 사용 설명서를 제공함)
       "self": { "href": "/hotel/rooms/55" },
       "book": { "href": "/hotel/reservation/r55", "method": "POST" },
       "cancel": { "href": "/hotel/rooms/55/cancel" }
     }
   }
```
---
## Ⅱ. 실무 적용 및 결론
API 버전 업이 매일 일어나는 거대 시스템에서, 앱(클라이언트) 코드 안에 URI 문자열 구조를 하드 코딩해두면 하위 호환성이 완전히 깨진다. HATEOAS 사상은 백엔드 개발자가 API 진입점 루트 하나만 알려주면, 클라이언트 엔진이 알아서 제공된 하이퍼링크를 거미처럼 타고 다니며 통신하게 만드는 마이크로서비스 설계 진화 체계의 절정이다.
