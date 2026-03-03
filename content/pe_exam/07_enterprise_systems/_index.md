+++
title = "7. 기업정보시스템"
description = "ERP, CRM, SCM, IT 전략, 경영정보, 비즈니스 인텔리전스, 디지털 전환"
sort_by = "title"
weight = 7
+++

# 제7과목: 기업정보시스템

기업 경영과 정보시스템의 연계, 전략적 활용을 다룹니다.

## 핵심 키워드

### ERP (전사적 자원관리)
- [ERP 기초](erp/erp.md) - 전사적 자원 관리(Enterprise Resource Planning), 부서 간 정보 통합, 프로세스 표준화, Gartner(1990), SAP S/4HANA/Oracle ERP Cloud/Microsoft Dynamics
- [ERP 모듈](erp/erp_modules.md) - FI/CO(재무/관리회계)/PP(생산관리)/MM(자재관리)/SD(판매관리)/HR(인사)/QM(품질)/PM(설비관리), 통합 데이터베이스
- [클라우드 ERP](erp/erp.md) - SaaS 기반 ERP, SAP S/4HANA Cloud/Oracle Cloud ERP/NetSuite, 초기 비용↓/업그레이드 자동/커스터마이징 제약
- [BPR](erp/bpr.md) - 업무 프로세스 재설계(Business Process Reengineering), AS-IS(현행)/TO-BE(목표) 분석, 프로세스 혁신, Michael Hammer(1990)
- [ERP 구현 전략](erp/erp.md) - 빅뱅(Big Bang, 일괄)/단계적(Phased, 순차적)/병렬(Parallel, 이중 운영), 위험 vs 시간 트레이드오프

### SCM / CRM
- [SCM](scm_crm/scm.md) - 공급망 관리(Supply Chain Management), 계획→조달→제조→배송→반품, 가시성(Visibility)/탄력성(Resilience)/지속가능성(Sustainability)
- [CRM](scm_crm/crm.md) - 고객 관계 관리(Customer Relationship Management), 360도 고객 뷰, 고객 생애 가치(CLV), Salesforce/HubSpot/Microsoft Dynamics 365
- [자동 보충 발주](scm_crm/automatic_replenishment.md) - VMI(공급자 재고관리, Vendor Managed Inventory)/CPFR(협업 계획·예측·재고 보충), 재고 최적화
- [크로스 도킹](scm_crm/cross_docking.md) - 물류 최적화, 입고→즉시 출고(보관 없음), 리드타임 단축, 물류비 절감,沃尔玛
- [공급망 리스크 관리](scm_crm/scm.md) - 공급망 디지털화, 가시성 플랫폼, 위험 모니터링, 다중 소싱, 버퍼 재고, 시나리오 플래닝
- [옴니채널 CRM](scm_crm/crm.md) - 온·오프라인 통합 고객 경험, 매장/모바일/웹/콜센터 통합, 고객 여정 일관성

### IT 전략 / 거버넌스
- [IT 전략](strategy/it_strategy.md) - 정보화 전략, IT 투자 우선순위, 비즈니스-IT 정렬(Alignment), IT 포트폴리오 관리, 디지털 전략
- [ISP (정보화 전략 계획)](strategy/information_strategy_planning.md) - 현황 분석→목표 아키텍처→이행 계획, AS-IS/TO-BE, 로드맵, ROI 분석
- [EA (엔터프라이즈 아키텍처)](ea.md) - TOGAF(The Open Group)/Zachman 프레임워크, 비즈니스/데이터/애플리케이션/기술 아키텍처, EA 원칙
- [IT 거버넌스](strategy/it_governance.md) - COBIT 2019(Control Objectives for Information and Related Technologies), Val IT, 이사회 책임, IT 투자 성과 관리
- [BSC](strategy/bsc.md) - 균형 성과표(Balanced Scorecard), 재무/고객/내부프로세스/학습성장 4관점, KPI 연계, 전략 실행 도구, Kaplan & Norton(1992)
- [COBIT](process/cobit.md) - IT 거버넌스 프레임워크, 4개 도메인(Plan/Build/Run/Monitor), 프로세스/관행/지표, ISACA
- [CMMI](process/cmmi.md) - 역량 성숙도 모델 통합(Capability Maturity Model Integration), CMMI-DEV/SVC/DMM, 5단계 성숙도, 프로세스 개선
- [ITIL 4.0](governance/) - IT 서비스 관리 베스트 프레임워크, 서비스 가치 시스템(SVS), 4차원 조직/정보/파트너/가치스트림, ITSM 표준

### 비즈니스 프로세스
- [BPM](process/bpm.md) - 비즈니스 프로세스 관리(Business Process Management), BPMS(BPM Suite), 프로세스 모델링/실행/모니터링/최적화
- [프로세스 마이닝](process/bpm.md) - 이벤트 로그 분석, 실제 프로세스 시각화, 병목/비효율 탐지, Celonis/UiPath Process Mining
- [워크플로우](process/workflow.md) - 업무 흐름 자동화, BPMN 2.0 표기법, 승인 프로세스, 상태 머신, Camunda/Activiti
- [자율형 워크플로우](process/workflow.md) - AI 기반 프로세스 자동화, 예외 처리 자동화, 지능형 라우팅, Self-healing processes
- [RPA (로봇 프로세스 자동화)](rpa.md) - 반복 업무 자동화, UiPath/Power Automate/Automation Anywhere, IPA(지능형 자동화)로 진화

### 시스템 통합 (EAI/ESB/SOA/MSA)
- [EAI](integration/eai.md) - 기업 애플리케이션 통합(Enterprise Application Integration)
  - **통합 패턴**:
    - **Point-to-Point**: 1:1 연결, 단순하지만 N(N-1)/2 복잡도, 스파게티 코드
    - **Hub-and-Spoke**: 중앙 허브, 관리 용이, SPOF(Single Point of Failure) 위험
    - **ESB(EAI Bus)**: 메시지 버스, 표준 인터페이스, 확장성↑
    - **Microservices**: 분산 서비스, API 기반, 최신 아키텍처
  - **통합 기술**: Adapter/Connector, Message Transformation, Routing, Orchestration
- [ESB(Enterprise Service Bus)](integration/esb.md) - 기업 서비스 버스
  - **핵심 기능**:
    - **메시지 라우팅**: 전송 대상 서비스 결정 (Content-based/Topic-based)
    - **메시지 변환**: 포맷 변환 (XML↔JSON/CSV), 프로토콜 변환 (HTTP↔JMS↔FTP)
    - **중계(Mediation)**: 로깅, 모니터링, 보안  장애 처리
  - **제품**: MuleSoft(Anypoint), Apache ServiceMix, WSO2 EI, IBM Integration Bus
  - **ESB 안티패턴**: "ESB Monolith" (모든 로직 ESB 집중→복잡도 폭증)
- [SOA(Service-Oriented Architecture)](integration/soa.md) - 서비스 지향 아키텍처
  - **핵심 원칙**:
    - **서비스 재사용성**: Loosely Coupled, Standard Interface
    - **느슨한 결합(Loose Coupling)**: 구현 독립성, 버전 관리 용이
    - **추상화(Abstraction)**: 계약(Contract) 기반 통신
    - **조합 가능성(Composability)**: 서비스 조합→신규 비즈니스 프로세스
  - **웹 서비스 표준**:
    - **SOAP(Simple Object Access Protocol)**: XML 메시지, WSDL(Web Services Description Language) UDDI(Universal Description, Discovery and Integration)
    - **WS-* 스펙**: WS-Security/WS-Addressing/WS-ReliableMessaging
    - **REST vs SOAP**: REST(경량, HTTP 네이티브) vs SOAP(무거움, 엔터프라이즈 기능)
  - **ESB vs MSA**: ESB(중앙집중, 강결합) vs MSA(분산, API 직접 호출)
- [API 관리(APIM)](integration/api_management.md) - API 게이트웨이/포털/마켓플레이스
  - **API 게이트웨이 기능**:
    - **인증/인가**: OAuth 2.0/JWT/API Key, IP 화이트리스트
    - **속도 제한(Rate Limiting)**: Throttling(속도)/Quota(수량)/Circuit Breaker(차단)
    - **로깅/모니터링**: 요청/응답 로그  메트릭 수집
    - **변환**: 요청/응답 변환, 프로토콜 변환
  - **API 포털**: 개발자 포털, 문서화(Swagger/OpenAPI) 테스트 SDK
  - **API 마켓플레이스**: 외부 API 공개/수익화, 사용량 과금
  - **제품**: Kong(오픈소스), Apigee(Google), AWS API Gateway, Azure APIM
- [MSA 전환](microservices.md) - 모놀리식→MSA 마이그레이션 전략
  - **Strangler Fig 패턴**: 레거시 시스템 점진적 교체
    - 1단계: 새 기능→MSA로 구현  레거시 호출
 MSA 응답
    - 2단계: 레거시 기능→MSA 이관
    - 3단계: 레거시 트래픽→MSA 라우팅
    - 4단계: 레거시 종료
  - **항체제 레이어(Anticorruption Layer)**: 레거시-MSA 간 데이터 변환/적응
  - **도메인 분해(DDD)**: Bounded Context별 서비스 분리, 팀 자율성
  - **데이터 분리**: Shared Database→Database-per-Service, CDC(Change Data Capture) 활용
  - **트랜잭션 관리**: Saga 패턴(보상 트랜잭션)/2PC(분산 트랜잭션)
- [이벤트 기반 아키텍처(Event-Driven Architecture)](integration/eai.md)
  - **이벤트 소싱(Event Sourcing)**: 상태 변경→이벤트 시퀀스 저장, 현재 상태=이벤트 재생
    - 장점: 완전한 변경 이력(Audit Trail)  시점 복원 가능
    - 단점: 이벤트 저장소 관리, 복잡도 증가
  - **CQRS(Command Query Responsibility Segregation)**: 명령(쓰기)/조회(읽기) 모델 분리
    - Write Model(정규화X, Read Model(비정규화X)
    - 장점: 독립적 확장  성능 최적화
  - **메시지 브로커**: Apache Kafka(파티셔닝, 컨슈머 오프셋)/RabbitMQ(AMQP)/AWS SNS+SQS
- [미들웨어(Middleware)](integration/middleware.md) - 인프라 소프트웨어
  - **TP Monitor(트랜잭션 처리)**: CICS/IBM TX Series  ACID 트랜잭션 관리
  - **MOM(메시지 지향 미들웨어)**: IBM MQ/Azure Service Bus  비동기 메시징
  - **ORB(객체 요청 브로커)**: CORBA/Java RMI  분산 객체 호출 (레거시)
  - **RPC(Remote Procedure Call)**: gRPC/Thrift/Dubbo  원격 프로시저 호출
- [EDI(Electronic Data Interchange)](integration/edi.md) - 전자 데이터 교환
  - **표준**: ANSI X12(미국)/EDIFACT(UN/Europe)
  - **전송**: AS2(Applicability Statement 22)/SFTP/HTTP
  - **문서 유형**: 주문(ORDERS)/송장(INVOIC)/출하통지(DESADV)/납품서(DEBADV)
  - **변환**: EDI↔XML/JSON  ID 매핑  비즈니스 규칙 적용
- **Integration Patterns**:
  - **Polling**: 주기적 조회  구현 단순  실시간성↓
  - **Webhook**: 이벤트 푸시  실시간성↑  구현 단순
  - **CDC(Change Data Capture)**: DB 변경 실시간 캡처  Debezium/Attunity
  - **ETL(Extract-Transform-Load)**: 배치 처리  대용량 이관

### BI / 분석
- [비즈니스 인텔리전스 (BI)](bi_analytics/) - 데이터 기반 의사결정, OLAP/큐브/대시보드, Tableau/Power BI/Looker/ThoughtSpot
- [데이터 분석](bi_analytics/) - 경영 의사결정 지원, 기술 분석/진단 분석/예측 분석/처방 분석, 분석 성숙도 모델
- [AIOps](aiops.md) - AI 기반 IT 운영(Artificial Intelligence for Operations), 이상 탐지/근본 원인 분석/자동 복구, 인시던트 관리
- [자가 서비스 분석](bi_analytics/) - 시민 데이터 과학자(Citizen Data Scientist), 셀프서비스 BI, 데이터 리터러시, IT 의존도 감소

### 지식 관리 / 협업
- [지식 관리 시스템 (KMS)](knowledge/) - 암묵지→형식지 변환, SECI 모델(사회화/외재화/결합/내면화), 지식 자산화, Nonaka & Takeuchi
- [그룹웨어](groupware.md) - 협업 플랫폼, Microsoft Teams/Slack/Notion/Jira Confluence, 커뮤니케이션/문서 공유/워크플로우
- [포털 (EIP)](enterprise_portal.md) - 기업 정보 포털(Enterprise Information Portal), 단일 창구(Single Point of Access), 개인화 대시보드
- [HRM](hrm.md) - 인적자원관리 시스템(Human Resource Management), 인사/급여/평가/교육, 인재 분석(Talent Analytics), Workday/PeopleSoft

### 디지털 전환 (DX)
- [디지털 전환 (DX)](dx.md) - 디지털 기술 기반 비즈니스 혁신, 비즈니스 모델 변화, 고객 경험 혁신, 조직 문화 변화, 로드맵
- [AI 전환 (AX)](dx.md) - AI 기반 경영 혁신, Agentic Enterprise, AI 우선 전략, 프로세스 지능화, 의사결정 자동화
- [스마트팩토리](mes.md) - 제조 혁신, MES(제조실행시스템)/SCADA(감시제어)/PLC(프로그래머블로직컨트롤러), Industry 4.0
- [PLM](plm.md) - 제품 수명주기 관리(Product Lifecycle Management), 설계→생산→유지보수→폐기, CAD/CAM/PDM 통합
- [디지털 공급망](scm_crm/scm.md) - S&OP(판매운영계획)/수요 예측 AI/실시간 가시성, Control Tower, 리스크 관리
- [B2B 전자상거래](b2b_ecommerce.md) - EDI/e-프로큐어먼트/전자 조달/마켓플레이스, 기업 간 거래 디지털화
- [Low-Code ERP](lowcode.md) - 시민 개발자 기반 경영 시스템, Mendix/OutSystems/Power Apps, 신속 개발/프로토타이핑

### 재해복구 / 보안
- [BCP (업무 연속성 계획)](bcp.md) - 비즈니스 연속성 관리(Business Continuity Management), ISO 22301, 위협 분석/영향 평가/복구 전략
- [DR (재해복구)](dr.md) - RTO(복구시간목표)/RPO(복구시점목표), 핫/웜/콜드 사이트, 백업 전략, 페일오버/페일백
- [기업 보안](enterprise_security.md) - Zero Trust 보안, IAM(신원 접근 관리)/PAM(권한 접근 관리), DLP(데이터 유출 방지)
- [SSO (단일 로그인)](sso.md) - SAML(Security Assertion Markup Language)/OAuth 2.0/OIDC(OpenID Connect), 연합 인증
- [클라우드 전환 전략](enterprise_cloud.md) - 5R: Rehost(이관)/Replatform(플랫폼변경)/Refactor(재구성)/Rebuild(재개발)/Replace(교체/폐기)

### 거버넌스 / 컴플라이언스
- [데이터 거버넌스](knowledge/) - 데이터 품질/정책/표준/스튜어드십, 데이터 자산 관리, DAMA-DMBOK, 메타데이터 관리
- [ITSM](governance/) - IT 서비스 관리(IT Service Management), 서비스 데스크/인시던트/문제/변경/구성 관리, ITIL 기반
- [컴플라이언스](governance/) - 법규 준수, GDPR/개인정보보호법/SOX/ISO 27001, 내부 통제, 규제 대응
- [ESG 경영](governance/) - 환경(Environmental)/사회(Social)/지배구조(Governance), 지속가능 IT, 탄소 발자국, 논금융 지표
- [SW 자산 관리 (SAM)](governance/) - 소프트웨어 라이선스 관리, ITAM(IT 자산 관리), SaaS 관리, 라이선스 최적화
