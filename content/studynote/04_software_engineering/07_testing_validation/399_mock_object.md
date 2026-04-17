+++
weight = 399
title = "399. 목 객체 (Mock Object)"
date = "2026-04-09"
description = "단위 테스트 시 대상 모듈에 결합된 외부 환경(의존성)을 가짜 객체로 대체하여 순수 로직만의 격리된 타이밍 프리 독립 테스트를 보장하는 기법"
[extra]
categories = "studynote"
+++

# 399. 목 객체 (Mock Object) 기반 격리 테스트

## 핵심 인사이트 (3줄 요약)
> 1. 네트워크 지연, DB 장애 등 외부 요인 때문에 실패하는 거짓 에러를 막고 오직 **테스트 타겟의 내부 비즈니스 로직 연산** 결과만 순수 채점한다.
> 2. **Dummy, Stub, Spy, Mock, Fake** 등 테스트 대역(Test Double)의 분화된 체계로 행위와 상태를 제어한다.
> 3. "몇 번 호출되었는가?" 등의 **행위 검증(Behavior Verification)** 에 특화된 객체(Mock) 기술이 현대 TDD 격리망의 핵심이다.

---
## Ⅰ. 아키텍처 및 원리
```text
  [ Mocking 구조망 ]
     인터페이스 IUserRepository 구현체 -> "MockUserRepository" 동적 생성
     Mockito 룰: "findByID(1)이 불리면 -> 무조건 200 반환해라" (상태 주입)
     타겟 함수 실행 -> Mock 감지: "정상 호출 1회 카운팅 됨 보장"
```
---
## Ⅱ. 실무 적용 및 결론
DB가 아직 설치되지 않은 프로젝트 초기 단계라도, 인터페이스만 선언해두고 프론트 모델을 Mocking하여 개발 시간을 압축 병렬로 치고 나갈 수 있게 하는 애자일의 심장이다.
