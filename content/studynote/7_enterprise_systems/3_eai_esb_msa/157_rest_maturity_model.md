+++
weight = 157
title = "157. RESTful API 성숙도 모델 (Maturity Model)"
date = "2026-04-09"
description = "시스템의 API가 얼마나 순수한 REST의 철학과 구조를 잘 따르고 있는지를 0단계부터 3단계까지 평가하고 분류하는 객관적 가이드라인 계층"
[extra]
categories = "studynote"
+++

# 157. RESTful API 성숙도 모델 (Richardson Maturity Model)

## 핵심 인사이트 (3줄 요약)
> 1. 세상에 REST라고 이름 붙은 API 중 90%는 가짜(Level 1~2 수준)라는 통찰에서 시작된, 리소스를 대하는 아키텍처 우아함의 평가 표준 척도 모형이다.
> 2. 상태(State)의 응집과 헤더(Verb)의 분리가 얼마나 정밀하게 분해되었냐가 핵심 상승 돌파 조건이다.
> 3. 최고 단계(Level 3: HATEOAS)에 도달하면 클라이언트는 서버의 링크가 안내하는 대로만 화면을 그리고 동적 이동하는 궁극의 독립적 자기 기술(Self-descriptive) 생명체가 된다.

---
## Ⅰ. 아키텍처 및 원리
```text
  [ 성숙도 레벨 위계탑 ]
    Level 3 : HATEOAS (응답 패킷 안에 다음 액션의 하이퍼링크가 동적으로 포함)
    Level 2 : HTTP Verbs (GET/POST/PUT/DELETE 메서드의 완벽 분리 활용)
    Level 1 : Resources (주소는 /user/1 분리하되, 전부 POST로만 행위 때려 박음)
    Level 0 : The Swamp (단일 /api 주소 하나로 다 때려 박고 내부 XML 텍스트로 함수 분기)
```
---
## Ⅱ. 실무 적용 및 결론
개발팀이 "우리도 REST 합니다"라고 할 때, 아키텍트는 저 잣대를 대고 Level 2도 안 되면서 캐시 효과를 살리고 있다고 착각하는 참사를 막아내야 한다. 진정한 마이크로서비스 확장은 Level 2 이상의 엄격한 통제에서만 무결성을 획득한다.
