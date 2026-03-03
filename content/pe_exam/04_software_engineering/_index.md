+++
title = "4. 소프트웨어 공학"
description = "개발 방법론, 아키텍처 설계, 테스트, 품질, 형상관리, 프로젝트 관리"
sort_by = "title"
weight = 4
+++

# 제4과목: 소프트웨어 공학

소프트웨어 개발의 체계적인 방법과 원칙을 다룹니다.

## 핵심 키워드

### 소프트웨어 공학 기초
- [소프트웨어 공학 개요](software_engineering.md) - SW 위기(1960년대), 3요소(사람/프로세스/기술), 공학적 접근
- [소프트웨어 생명주기(SDLC)](software_engineering.md) - 요구분석→설계→구현→테스트→유지보수
- [소프트웨어 유형](software_engineering.md) - 시스템SW/애플리케이션SW/임베디드SW
- [소프트웨어 유지보수](software_engineering.md) - 수정/적응/완전/예방 유지보수, 유지보수 비용
- [소프트웨어 재공학](quality/software_quality.md) - 역공학(Reverse Engineering), 재구조화, 이식(Migration)
- [기술 부채(Technical Debt)](quality/software_quality.md) - 빠른 개발의 미래 비용, 부채 관리

### 개발 방법론
- [폭포수 모델(Waterfall)](methodology/waterfall_model.md) - 요구분석→설계→구현→테스트→유지보수, 단계별 산출물, 검토(Review) 중심
- [폭포수 단계별 산출물](methodology/waterfall_model.md) - 요구분석(SRS)/설계(HLD/LLD, DB설계, UI설계)/구현(소스코드)/테스트(테스트케이스, 리포트)
- [폭포수 특징](methodology/waterfall_model.md) - 순차 진행/명확한 단계/문서 중심/요구사항 고정 전제/대규모/안정적 요구사항
- [폭포수 장단점](methodology/waterfall_model.md) - 장점(진행상황 명확/문서화 체계/관리 용이)/단점(변경 어려움/피드백 늦음/위험 늦게 발견)
- [V 모델](methodology/waterfall_model.md) - 폭포수+테스트 단계 매핑, 요구분석↔인수테스트/설계↔통합테스트/구현↔단위테스트
- [V 모델 테스트 레벨](methodology/waterfall_model.md) - 단위(Unit)/통합(Integration)/시스템(System)/인수(Acceptance) 테스트
- [프로토타입 모델](methodology/waterfall_model.md) - 신속한 프로토타입→사용자 피드백→요구사항 구체화, 반복 개선
- [프로토타입 유형](methodology/waterfall_model.md) - Throwaway(일회용, 요구사항 명확화)/Evolutionary(진화형, 최종 제품으로 발전)
- [프로토타입 충실도](methodology/waterfall_model.md) - Low-Fi(스케치, 와이어프레임)/High-Fi(실제 동작), 수직(핵심기능)/수평(전체 UI)
- [나선형 모델(Spiral)](methodology/waterfall_model.md) - 위험 분석(Risk Analysis) 중심, 4단계 반복, 위험 주도 개발
- [나선형 4단계](methodology/waterfall_model.md) - ①목표 설정→②위험 식별/분석→③개발/검증→④다음 단계 계획, 위험 완화
- [나선형 적용](methodology/waterfall_model.md) - 대규모/고위험/새로운 기술/요구사항 불확실 프로젝트
- [증분 모델(Incremental)](methodology/waterfall_model.md) - 기능 단위 점진적 제공, 우선순위 기능 먼저, 릴리즈 빈도 높음
- [반복 모델(Iterative)](methodology/waterfall_model.md) - 전체 기능 반복 개선, 피드백 기반 진화, 요구사항 변화 수용
- [애자일 선언문](methodology/agile_methodology.md) - 4가치(개인/상호작용 > 프로세스/도구, 작동 SW > 이해관행 문서, 고객 협력 > 계약 협상, 변화 대응 > 계획 따르기)
- [애자일 12원칙](methodology/agile_methodology.md) - 고객만족/변화환영/자주전달/협력/동기부여/대화/작동SW/지속가능속도/기술적우수성/단순화/자기조직화/반성
- [스크럼(Scrum)](methodology/agile_methodology.md) - 스프린트(2~4주, Time-box), 일일 스크럼(15min), 스프린트 리뷰/회고
- [스크럼 3+3 역할](methodology/agile_methodology.md) - PO(제품 책임자, 백로그 우선순위)/SM(스크럼 마스터, 장애물 제거)/개발팀(자기조직화, 5~9명)
- [스크럼 3 아티팩트](methodology/agile_methodology.md) - Product Backlog(기능 우선순위 목록)/Sprint Backlog(선택된 작업)/Increment(완성된 제품)
- [스크럼 5 이벤트](methodology/agile_methodology.md) - Sprint Planning/Daily Scrum/Sprint Review/Sprint Retrospective/Sprint
- [XP(eXtreme Programming)](methodology/agile_methodology.md) - 기술적 실천 중심, 짝 코딩/TDD/CI/리팩토링/단순한 설계
- [XP 12 실천](methodology/agile_methodology.md) - Planning Game/Small Releases/Simple Design/Test-First/Refactoring/Pair Programming/Collective Ownership/CI/40-hour Week/On-site Customer/Metaphor/Sustainable Pace/Coding Standards
- [칸반(Kanban)](methodology/agile_methodology.md) - 흐름(Flow) 기반, WIP(Work-In-Progress) 제한, Pull 방식, 칸반 보드(To Do/Doing/Done)
- [칸반 핵심 지표](methodology/agile_methodology.md) - Lead Time(요청→완료)/Cycle Time(작업시작→완료)/Throughput(단위시간 처리량)/WIP(진행 중 작업)
- [SAFe(Scaled Agile Framework)](methodology/agile_methodology.md) - 대규모 애자일, Essential/Team/Program/Portfolio/Full 5계층
- [SAFe 핵심](methodology/agile_methodology.md) - PI(Program Increment, 8~12주)/ART(Agile Release Train, 50~125명)/Team of Teams
- [LeSS(Large-Scale Scrum)](methodology/agile_methodology.md) - 스크럼 확장, 8개 팀 규칙/단일 Product Backlog/하나의 PO
- [DevOps](methodology/devsecops.md) - Dev+Ops 통합, 자동화/협업 문화, CI/CD/IaC/모니터링/피드백 루프
- [DevOps 3가지 방식](methodology/devsecops.md) - CAMS(Culture/Automation/Measurement/Sharing), 자동화 파이프라인/협업/지속적 피드백
- [DevSecOps](methodology/devsecops.md) - Dev+Sec+Ops 통합, Shift-Left Security, SAST/DAST/SCA/컨테이너 보안/시크릿 스캔
- [DevSecOps 파이프라인](methodology/devsecops.md) - 코드 커밋→SAST→유닛 테스트→SCA→빌드→이미지 스캔→배포→런타임 보호
- [플랫폼 엔지니어링](methodology/platform_engineering.md) - IDP(Internal Developer Platform) 구축, Self-Service/골든 패스(Golden Path)/템플릿
- [IDP 구성요소](methodology/platform_engineering.md) - 셀프 서비스 포털/인프라 추상화/환경 관리/템플릿 카탈로그/지식 베이스/관찰 가능성
- [AI 기반 개발(AI-Augmented Dev)](methodology/agile_methodology.md) - GitHub Copilot/Cursor/Claude, 코드 생성/리뷰/테스트/리팩토링
- [Low-Code/No-Code](methodology/platform_engineering.md) - 시민 개발자(Citizen Developer), 드래그앤드롭, Power Apps/Mendix/OutSystems

### 요구사항 공학
- [요구사항 공학(Requirements Engineering)](methodology/requirements_engineering.md) - 도출(Elicitation)/분석(Analysis)/명세(Specification)/검증(Validation)/관리(Management)
- [요구사항 도출 기법](methodology/requirements_engineering.md) - 인터뷰/설문/관찰/문서 분석/JAD(Joint Application Design)/브레인스토밍/프로토타이핑
- [요구사항 분류](methodology/requirements_engineering.md) - 기능적(Functional, 입력/처리/출력)/비기능적(Non-Functional, 성능/보안/사용성)/도메인 요구사항
- [기능적 요구사항](methodology/requirements_engineering.md) - 시스템이 수행해야 할 기능, 입력→처리→출력, Use Case로 표현
- [비기능적 요구사항](methodology/requirements_engineering.md) - 성능/보안/신뢰성/사용성/유지보수성/이식성/확장성/가용성
- [FURPS+ 모델](methodology/requirements_engineering.md) - Functionality/Usability/Reliability/Performance/Supportability + Design/Implementation/Interface
- [요구사항 명세(SRS)](methodology/requirements_engineering.md) - IEEE 830, 기능/비기능/제약사항, 자연어/정형 명세(Z/VDM)/반정형(UML)
- [요구사항 검증(Validation)](methodology/requirements_engineering.md) - 정확성/완전성/일관성/모호성/검증 가능성/추적 가능성
- [요구사항 추적표(RTM)](methodology/requirements_engineering.md) - Forward(요구→구현)/Backward(구현→요구), 영향 분석, 변경 관리
- [유스케이스(Use Case)](methodology/requirements_engineering.md) - 액터(Actor)/유스케이스/시나리오/선후조건/예외 흐름
- [유스케이스 다이어그램](methodology/requirements_engineering.md) - 액터/유스케이스/관계(Association/Include/Extend/Generalization)
- [사용자 스토리](methodology/agile_methodology.md) - As a [역할]/I want [기능]/So that [가치], INVEST 원칙
- [인수 기준(Acceptance Criteria)](methodology/agile_methodology.md) - Given-When-Then(Gherkin), Definition of Done(DoD)
- [스토리 포인트](methodology/agile_methodology.md) - 피보나치(1,2,3,5,8,13,21), Planning Poker, 복잡도/불확실성/노력
- [INVEST 원칙](methodology/agile_methodology.md) - Independent/Negotiable/Valuable/Estimable/Small/Testable

### 소프트웨어 설계 원칙
- [설계 목표](design/software_design.md) - 모듈화(Modularity)/추상화(Abstraction)/캡슐화(Encapsulation)/정보은닉(Information Hiding)/관심사 분리(SoC)
- [모듈화](design/software_design.md) - 기능 단위 분리, 재사용성/유지보수성/테스트 용이성, 응집도↑/결합도↓
- [추상화(Abstraction)](design/software_design.md) - 복잡성 숨김, 인터페이스 노출/구현 숨김, 데이터 추상화/제어 추상화
- [정보 은닉(Information Hiding)](design/software_design.md) - 내부 구현 숨김, 인터페이스로만 접근, 변경 영향 최소화
- [응집도(Cohesion)](design/software_design.md) - 모듈 내 구성요소 간 관련성, 높을수록 좋음
- [응집도 종류](design/software_design.md) - 기능적(1목적, 최고)>순차적(출력→입력)>통신적(동일 데이터)>절차적(순서)>시간적(동시)>논리적(유사)>우연적(무관, 최저)
- [결합도(Coupling)](design/software_design.md) - 모듈 간 의존성, 낮을수록 좋음(Loose Coupling)
- [결합도 종류](design/software_design.md) - 자료<스탬프(자료구조)<제어(플래그)<외부(외부포맷)<공유(전역변수)<내용(내부직접접근, 최악)
- [Fan-in/Fan-out](design/software_design.md) - Fan-in(상위 호출 수, 재사용성)/Fan-out(하위 호출 수, 복잡도)
- [SOLID 원칙](design/software_design.md) - OOP 5대 원칙, 유지보수성/확장성/유연성 향상
- [SRP(Single Responsibility)](design/software_design.md) - 단일 책임, 한 클래스=한 이유로만 변경, 응집도↑
- [OCP(Open/Closed)](design/software_design.md) - 확장에는 열림/수정에는 닫힘, 추상화/다형성 활용
- [LSP(Liskov Substitution)](design/software_design.md) - 자식→부모 대체 가능, 계약 준수, 상속 올바른 사용
- [ISP(Interface Segregation)](design/software_design.md) - 인터페이스 분리, 클라이언트별 전용 인터페이스, 범용 인터페이스 지양
- [DIP(Dependency Inversion)](design/software_design.md) - 의존 역전, 추상화에 의존/구체화에 의존X, DI(Dependency Injection)
- [의존성 주입(DI)](design/software_design.md) - Constructor/Setter/Interface Injection, IoC 컨테이너, 결합도↓
- [DRY(Don't Repeat Yourself)](design/software_design.md) - 중복 코드 제거, 단일 진실 공급원(SSOT), 재사용성↑
- [KISS(Keep It Simple, Stupid)](design/software_design.md) - 단순 유지, 과잉 엔지니어링 지양, YAGNI 연계
- [YAGNI(You Ain't Gonna Need It)](design/software_design.md) - 불필요한 기능 미추가, 필요할 때 추가, 낭비 방지

### 소프트웨어 아키텍처
- [아키텍처(Architecture)](design/software_architecture.md) - 시스템 구조/동작/특성 정의, 품질 속성 결정, 주요 의사결정, ADR(Architecture Decision Record)
- [아키텍처 뷰(View)](design/software_architecture.md) - 논리(기능)/물리(배포)/프로세스(런타임)/개발(코드) 뷰, 4+1 뷰(Kruchten)
- [레이어드 아키텍처(Layered)](design/software_architecture.md) - Presentation→Business→Data Access→Data, 관심사 분리, 의존성 방향(하위→상위), 계층 간 인터페이스
- [레이어드 특징](design/software_architecture.md) - 장점(단순/유지보수)/단점(단일장애점/확장한계/성능오버헤드), Monolithic 구조
- [마이크로서비스 아키텍처(MSA)](design/software_architecture.md) - 서비스별 독립 배포, API Gateway/Service Discovery/Circuit Breaker, 분산 시스템
- [MSA vs 모놀리식](design/software_architecture.md) - 모놀리식(단일/단순/확장어려움)/MSA(독립/복잡/확장용이), DB per Service
- [MSA 핵심 패턴](design/software_architecture.md) - API Gateway(단일 진입점)/Service Registry/Eureka/Consul/Service Mesh(Istio)
- [MSA 통신](design/software_architecture.md) - 동기(REST/gRPC)/비동기(MQ/Kafka/Event Bus), Saga(분산트랜잭션)/CQRS
- [Saga 패턴](design/software_architecture.md) - Choreography(이벤트 기반)/Orchestration(중앙 조정), 보상 트랜잭션
- [이벤트 기반 아키텍처(EDA)](design/software_architecture.md) - 이벤트 생산/소비, 비동기/디커플링, Pub/Sub, Event Sourcing
- [이벤트 소싱(Event Sourcing)](design/software_architecture.md) - 상태 변경 이벤트 저장, 이벤트 로그, 재생/감사/시점 복구
- [CQRS(Command Query Responsibility Segregation)](design/software_architecture.md) - 명령(Write)/조회(Read) 모델 분리, 최적화, 결과적 일관성
- [파이프-필터 아키텍처(Pipe-Filter)](design/software_architecture.md) - 데이터 파이프/필터 변환, 재사용/조합, Unix 파이프|Elasticsearch 파이프라인
- [클린 아키텍처(Clean Architecture)](design/software_architecture.md) - 의존성 역전, Entities→Use Cases→Interface Adapters→Frameworks, 외부→내부 의존
- [헥사고날 아키텍처(Hexagonal/Ports & Adapters)](design/software_architecture.md) - 코어(도메인)/포트(인터페이스)/어댑터(구현), 테스트 용이
- [서버리스 아키텍처(Serverless)](design/software_architecture.md) - FaaS(Lambda/Functions)/BaaS(S3/Firestore), 이벤트 트리거, Cold Start
- [서버리스 장단점](design/software_architecture.md) - 장점(운영X/비용효율/확장자동)/단점(Cold Start/벤더락인/디버깅어려움)
- [API 설계 스타일](design/software_architecture.md) - REST(Resource)/GraphQL(Graph)/gRPC(Protocol Buffers)/WebSocket(양방향)
- [REST API 성숙도(Richardson)](design/software_architecture.md) - Level 0(URI)/1(리소스)/2(HTTP 메서드)/3(HATEOAS)/4(폼/헤더)
- [HATEOAS](design/software_architecture.md) - Hypermedia As The Engine Of Application State, 링크 기반 상태 전이
- [GraphQL](design/software_architecture.md) - Query/Mutation/Subscription, Schema/Resolver, 과요청/과다반환 문제 해결
- [gRPC](design/software_architecture.md) - Protocol Buffers(직렬화)/HTTP/2(스트리밍), 스트립/서버/양방향 스트리밍
- [API 버저닝](design/software_architecture.md) - URI Path(v1)/Query Param/Header/Content Negotiation, Breaking/Non-breaking 변경
- [도메인 주도 설계(DDD)](design/software_design.md) - 바운디드 컨텍스트/애그리거트/엔티티/값 객체/도메인 서비스/리포지토리
- [DDD 전략적 설계](design/software_design.md) - 바운디드 컨텍스트/컨텍스트 맵/유비쿼터스 언어/이벤트 스토밍
- [DDD 전술적 설계](design/software_design.md) - 애그리거트(Aggregate)/루트 엔티티/값 객체/도메인 서비스/리포지토리/팩토리
- [이벤트 스토밍(Event Storming)](design/software_design.md) - 도메인 이벤트(주황)/커맨드(파랑)/애그리거트(노랑)/정책(보라)/외부시스템(분홍) 스티커
- [컴포저블 아키텍처(Composable)](design/software_architecture.md) - 교체 가능/조립 가능, Headless/MACH(Microservices/API-first/Cloud-native/Headless)

### 디자인 패턴
- [GoF 디자인 패턴](design/design_pattern.md) - 23가지 패턴, 생성(5)/구조(7)/행위(11) 분류, 재사용성/유연성 향상
- [싱글톤(Singleton)](design/design_pattern.md) - 인스턴스 1개, 전역 접근, Double-Checked Locking, Enum 구현
- [팩토리 메서드(Factory Method)](design/design_pattern.md) - 객체 생성 서브클래스 위임, Creator/Product, 확장에는 열림
- [추상 팩토리(Abstract Factory)](design/design_pattern.md) - 관련 객체 패밀리 생성, 팩토리의 팩토리, 테마/플랫폼별
- [빌더(Builder)](design/design_pattern.md) - 복잡한 객체 단계별 생성, Fluent Interface, 생성자 인자 많을 때
- [프로토타입(Prototype)](design/design_pattern.md) - 복제(Clone) 기반 객체 생성, 깊은 복사/얕은 복사, 비용 절감
- [어댑터(Adapter)](design/design_pattern.md) - 인터페이스 변환, 호환성 확보, Class/Object 어댑터
- [브리지(Bridge)](design/design_pattern.md) - 구현에서 추상화 분리, Abstraction/Implementor, 다양한 플랫폼
- [컴포지트(Composite)](design/design_pattern.md) - 트리 구조, 개체/그룹 동일 취급, 부분-전체 계층
- [데코레이터(Decorator)](design/design_pattern.md) - 동적 기능 추가, 래핑, 상속 없이 확장, java.io
- [파사드(Facade)](design/design_pattern.md) - 복잡한 서브시스템 단순화, 통합 인터페이스, 의존성 감소
- [플라이웨이트(Flyweight)](design/design_pattern.md) - 공유 메모리, Intrinsic(공유)/Extrinsic(비공유), 문자열 풀
- [프록시(Proxy)](design/design_pattern.md) - 대리자, 가상/원격/보호/스마트 참조, Lazy Loading
- [옵저버(Observer)](design/design_pattern.md) - 발행-구독(Pub/Sub), Subject/Observer, 이벤트 알림, Rx
- [전략(Strategy)](design/design_pattern.md) - 알고리즘 교체 가능, Context/Strategy, DI와 연계
- [커맨드(Command)](design/design_pattern.md) - 요청 객체화, Invoker/Receiver/Command, 실행 취소/재실행
- [이터레이터(Iterator)](design/design_pattern.md) - 집합 순차 접근, next()/hasNext(), 내부 구조 숨김
- [템플릿 메서드(Template Method)](design/design_pattern.md) - 알고리즘 골격, Hook 메서드, 상위 클래스 정의/하위 구현
- [상태(State)](design/design_pattern.md) - 상태별 동작 캡슐화, 상태 전이, State Machine
- [방문자(Visitor)](design/design_pattern.md) - 데이터 구조와 연산 분리, accept()/visit(), 더블 디스패치
- [책임 연쇄(Chain of Responsibility)](design/design_pattern.md) - 요청 처리 연결, Handler 체인, 로그 레벨/필터
- [중재자(Mediator)](design/design_pattern.md) - 객체 간 상호작용 캡슐화, Hub/SPOC, M:N→1:N
- [메멘토(Memento)](design/design_pattern.md) - 상태 스냅샷, Originator/Caretaker/Memento, 실행 취소
- [인터프리터(Interpreter)](design/design_pattern.md) - 언어 문법 해석, Context/Expression, DSL/규칙 엔진
- [MSA 패턴](design/design_pattern.md) - Sidecar(Proxy)/Ambassador(외부API)/Circuit Breaker(장애격리)/Bulkhead(자원격리)/Retry
- [Circuit Breaker](design/design_pattern.md) - Closed/Open/Half-Open, 장애 전파 방지, Hystrix/Resilience4j
- [UML](design/uml.md) - 구조(클래스/컴포넌트/배포/패키지/객체)/행위(시퀀스/활동/상태/유스케이스/타이밍/상호작용) 다이어그램

### 소프트웨어 테스트
- [테스트 기초](testing/software_testing.md) - 결함(Defect)/오류(Error)/실패(Failure) 구분, 테스트 원칙 7가지
- [화이트박스 테스트](testing/software_testing.md) - 문장/분기/조건/다중조건/경로/변경조건 커버리지, 복잡도 측정
- [블랙박스 테스트](testing/software_testing.md) - 동치분할, 경계값 분석, 결정 테이블, 원인-결과 그래프, 페어와이즈
- [V 모델 테스트 레벨](testing/software_testing.md) - 단위→통합→시스템→인수 테스트
- [통합 테스트 방법](testing/software_testing.md) - 빅뱅/하향식(스텁)/상향식(드라이버)/샌드위치
- [시스템 테스트](testing/software_testing.md) - 기능/성능/부하/스트레스/보안/호환성/회귀 테스트
- [인수 테스트](testing/software_testing.md) - UAT, 알파/베타 테스트
- [회귀 테스트](testing/software_testing.md) - 변경 영향 재검증, 자동화 필수
- [성능 테스트](testing/software_testing.md) - 부하/스트레스/내구성/스파이크 테스트, 지표(TPS/응답시간/처리량)
- [테스트 자동화](testing/software_testing.md) - CI/CD 파이프라인 통합, 테스트 피라미드
- [TDD (테스트 주도 개발)](testing/software_testing.md) - Red-Green-Refactor 사이클
- [BDD (행위 주도 개발)](testing/software_testing.md) - Given-When-Then, Gherkin, Cucumber
- [AI SW 품질 보증 테스트](testing/software_testing.md) - 편향 테스트, 모델 견고성, 적대적 입력
- [TMMi](testing/software_testing.md) - 테스트 프로세스 성숙도 모델 5단계
- [뮤테이션 테스팅](testing/software_testing.md) - 결함 삽입, 테스트 케이스 효과성 평가
- [카오스 엔지니어링](testing/software_testing.md) - 생산 환경 장애 주입, 내결함성 검증

### 소프트웨어 품질
- [ISO/IEC 25010 (SQuaRE)](quality/software_quality.md) - 8가지 품질 특성: 기능적합성/성능효율성/호환성/사용성/신뢰성/보안성/유지보수성/이식성
- [소프트웨어 품질 지표](quality/quality_metrics.md) - 결함 밀도(Defect Density), 테스트 커버리지, MTBF/MTTR
- [사이클로매틱 복잡도](quality/quality_metrics.md) - McCabe 복잡도, V(G)=E-N+2P
- [정적 분석](quality/software_quality.md) - 코드 리뷰, 소나큐브, 린팅, 정적 분석 도구
- [SW 리팩토링](quality/software_quality.md) - 코드 악취(Code Smell) 14가지, 리팩토링 기법

### 프로젝트 관리
- [CMMI 2.0/3.0](management/cmmi_model.md) - DEV/SVC/DMM, 실천 영역(PA), 역량/성숙도 수준 1~5
- [COCOMO II](management/cocomo_model.md) - LOC/Function Point 기반 비용 추정, 보정 계수(EM)
- [기능 점수(Function Point)](management/cocomo_model.md) - IFPUG FP, 입력/출력/조회/내부논리파일/외부인터페이스
- [형상관리(SCM)](management/configuration_management.md) - 형상 식별/통제/상태 기록/감사, Git 기반 워크플로우
- [Git 브랜칭 전략](management/configuration_management.md) - Git Flow, GitHub Flow, Trunk-Based Development
- [변경 관리](management/configuration_management.md) - CCB(형상통제위원회), RFC, 영향 분석
- [프로젝트 계획](management/project_management.md) - WBS(Work Breakdown Structure), 자원 계획, 위험 계획
- [일정 관리](management/project_management.md) - CPM(임계 경로), PERT(3점 추정), 간트 차트, 마일스톤
- [비용 관리](management/project_management.md) - EVM(획득가치관리), PV/EV/AC, CPI/SPI, ETC/EAC
- [위험 관리](management/project_management.md) - 위험 식별/정성/정량 분석/대응/모니터링, 위험 레지스터
- [품질 관리](management/project_management.md) - QA vs QC, 품질 계획/보증/통제
- [PMO](management/project_management.md) - 프로젝트 관리 오피스, 지원형/통제형/지시형 PMO
- [PMP 7판](management/project_management.md) - 12 원칙, 8 성과 영역, 예측형/적응형/하이브리드
- [국제 표준](management/project_management.md) - ISO/IEC 12207(SW 생명주기), ISO/IEC 15288(시스템 생명주기)

### 최신 트렌드
- [소프트웨어 공급망 보안](methodology/devsecops.md) - SBOM(SW 자산 명세서), 의존성 검사, SLSA 프레임워크
- [내부 개발자 플랫폼(IDP)](methodology/platform_engineering.md) - Self-service 인프라, 개발자 경험(DevEx)
- [그린 소프트웨어](quality/software_quality.md) - 에너지 효율 코드, 탄소 인식 컴퓨팅
