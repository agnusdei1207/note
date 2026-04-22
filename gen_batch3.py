import os

BASE = "/Users/pf/workspace/brainscience/content/studynote/12_it_management/05_security_compliance"

def make(num, filename, title, body):
    return f"""+++
weight = {num}
title = "{title}"
date = "2026-04-21"
[extra]
categories = "studynote-it-management"
+++

{body}
"""

TEMPLATE = """## 핵심 인사이트
> 1. **본질**: {essence}
> 2. **가치**: {value}
> 3. **판단 포인트**: {judge}

## Ⅰ. 개요 및 필요성

{overview}

📢 **섹션 요약 비유**: {analogy1}

## Ⅱ. 아키텍처 및 핵심 원리

{arch}

📢 **섹션 요약 비유**: {analogy2}

## Ⅲ. 비교 및 연결

{compare}

📢 **섹션 요약 비유**: {analogy3}

## Ⅳ. 실무 적용 및 기술사 판단

{practice}

기술사 시험에서 이 개념의 정의·구성·비교·기대효과를 논하는 문제가 출제된다.

📢 **섹션 요약 비유**: {analogy4}

## Ⅴ. 기대효과 및 결론

{conclusion}

📢 **섹션 요약 비유**: {analogy5}

### 📌 관련 개념 맵
| 개념 | 설명 | 연관 키워드 |
|:---|:---|:---|
{concepts}

### 👶 어린이를 위한 3줄 비유 설명
1. {child1}
2. {child2}
3. {child3}"""

def t(essence, value, judge, overview, arch, compare, practice, conclusion,
      analogy1, analogy2, analogy3, analogy4, analogy5, concepts, child1, child2, child3):
    return TEMPLATE.format(
        essence=essence, value=value, judge=judge, overview=overview,
        arch=arch, compare=compare, practice=practice, conclusion=conclusion,
        analogy1=analogy1, analogy2=analogy2, analogy3=analogy3,
        analogy4=analogy4, analogy5=analogy5, concepts=concepts,
        child1=child1, child2=child2, child3=child3)

files = [
(296, "296_eai_integration.md", "296. EAI (Enterprise Application Integration) 허브&스포크/P2P",
 t("EAI (Enterprise Application Integration)는 기업 내 이기종 애플리케이션(ERP, CRM, SCM 등)을 통합하여 데이터와 비즈니스 프로세스를 자동으로 연계하는 미들웨어 아키텍처다.",
   "Point-to-Point(포인트 투 포인트) 통합의 스파게티 구조를 허브&스포크 또는 ESB로 전환하여 통합 복잡도를 N(N-1)/2에서 N으로 낮춘다.",
   "시스템 수가 증가할수록 P2P의 연계 복잡도는 기하급수적으로 증가(N² 수준)하므로, 10개 이상 시스템 통합 시 EAI Hub 도입이 필수적이다.",
   "기업의 IT 시스템은 구매 시기와 목적에 따라 제각각의 언어·프로토콜로 만들어진다. EAI는 이를 공통 메시지 버스(Message Bus)로 연결하여 실시간 데이터 흐름을 보장한다.",
   """```
┌──────────────────────────────────────────────┐
│  EAI 통합 방식 비교                          │
├──────────────────┬───────────────────────────┤
│  P2P (포인트)    │  Hub & Spoke              │
│  A↔B, A↔C, B↔C  │  A→Hub←B, Hub→C           │
│  연계 수: N(N-1)/2│  연계 수: N               │
│  스파게티 구조   │  중앙 집중 관리           │
└──────────────────┴───────────────────────────┘
```
| 통합 패턴 | 장점 | 단점 |
|:---|:---|:---|
| P2P | 구현 빠름 | 복잡도 폭발 |
| Hub&Spoke | 관리 용이 | Hub SPoF |
| ESB | 유연성 최고 | 복잡성 높음 |""",
   """| 구분 | EAI | ESB |
|:---|:---|:---|
| 구조 | Hub&Spoke 중심 | 분산 버스 |
| 유연성 | 중간 | 높음 |
| SOA와 관계 | 전 단계 | SOA 구현 수단 |""",
   "대형 금융그룹의 계열사 통합: 은행·보험·카드 계열사를 EAI Hub로 연결하여 고객 360° 뷰 구현. 기존 P2P 연계 45개를 Hub 1개+어댑터 9개로 교체하여 유지보수 비용 60% 절감.",
   "EAI 도입으로 이기종 시스템 통합 비용 절감, 실시간 데이터 동기화, 신규 시스템 추가 시 허브만 연결하는 확장성 확보가 달성된다.",
   "EAI는 공항 허브(Hub)다. 모든 비행기(시스템)가 허브를 통해 연결되어 직항 없이도 모든 도시로 갈 수 있다.",
   "Hub는 모든 시스템의 중간 통역사다. 영어(ERP)→Hub→한국어(SCM)로 자동 변환한다.",
   "P2P가 모든 집이 직접 연결된 거미줄이라면, Hub&Spoke는 모든 집이 우체국(Hub)을 통해 연결된 구조다.",
   "EAI는 레고의 Universal Connector다. 서로 다른 레고 블록을 하나의 커넥터로 연결한다.",
   "EAI는 서로 다른 언어를 쓰는 사람들 사이에서 실시간으로 통역해주는 사람이다.",
   "| ESB | Enterprise Service Bus | SOA 구현 수단 |\n| API Gateway | RESTful API 통합 | MSA 연계 |\n| SOA | Service Oriented Architecture | EAI 진화 |",
   "EAI는 여러 나라 말을 하는 사람들이 소통할 수 있게 공통 언어로 통역해주는 시스템이에요.",
   "예전엔 프로그램마다 직접 연결해야 해서 줄이 엉켜있었는데, EAI Hub가 모든 연결을 담당해요.",
   "시스템이 늘어나도 Hub에만 연결하면 되니까 점점 더 편리해져요.")),

(297, "297_soa_wsdl_uddi.md", "297. SOA (Service Oriented Architecture) WSDL/UDDI/SOAP",
 t("SOA (Service Oriented Architecture, 서비스 지향 아키텍처)는 비즈니스 기능을 독립적으로 호출 가능한 서비스 단위로 모듈화하여 느슨한 결합(Loose Coupling)으로 통합하는 아키텍처 패러다임이다.",
   "WSDL(Web Services Description Language)로 서비스를 표준 기술하고, UDDI(Universal Description, Discovery and Integration) 레지스트리에 등록하고, SOAP(Simple Object Access Protocol)로 호출하는 3단계 체계가 SOA의 기술적 기반이다.",
   "SOA는 IT 유연성(서비스 재사용)을 높이지만 SOAP의 복잡성과 UDDI 레지스트리 관리 부담이 단점으로, 현대에는 RESTful API와 MSA로 대부분 대체되었다.",
   "SOA는 기업의 IT를 LEGO 블록처럼 표준화된 서비스 단위로 분해하여, 새로운 비즈니스 요구 시 기존 서비스를 조합·재사용할 수 있게 한다. ESB(Enterprise Service Bus)를 통해 서비스 간 메시지를 라우팅한다.",
   """```
┌──────────────────────────────────────────┐
│  SOA 3대 역할                            │
│  서비스 제공자  ─→  UDDI 레지스트리      │
│  (Publisher)         (저장·검색)         │
│                          │               │
│                          ↓ 탐색          │
│  서비스 소비자 ←─────────               │
│  (Consumer)    WSDL로 인터페이스 확인    │
│                SOAP/HTTP으로 호출        │
└──────────────────────────────────────────┘
```
| 기술 요소 | 설명 | 역할 |
|:---|:---|:---|
| WSDL | 서비스 인터페이스 기술 언어 | 서비스 계약 정의 |
| UDDI | 서비스 레지스트리/디렉토리 | 서비스 발견 |
| SOAP | XML 기반 메시지 프로토콜 | 서비스 호출 |""",
   """| 구분 | SOA/SOAP | MSA/REST |
|:---|:---|:---|
| 메시지 | SOAP(XML, 무거움) | REST(JSON, 경량) |
| 서비스 단위 | 비즈니스 기능 | 마이크로서비스 |
| 통합 방식 | ESB 중앙집중 | API Gateway |""",
   "2000년대 대형 SI 프로젝트에서 SOA는 ERP·CRM 서비스를 표준 인터페이스로 재사용하는 아키텍처였다. 현재는 SOAP→REST 전환이 완료된 기업이 대부분이며, 레거시 SOA와 MSA를 점진적으로 통합하는 과도기에 있다.",
   "SOA에서 MSA로의 진화: SOA는 거버넌스·통합의 효율화를, MSA는 독립 배포·확장성을 최대화한다.",
   "SOA는 도서관의 표준 검색 시스템이다. 서비스(책)가 표준 형식으로 등록(UDDI)되고, 규격화된 방법(WSDL)으로 찾아 호출(SOAP)한다.",
   "SOAP는 형식이 엄격한 법률 문서, REST는 간결한 이메일이다. 같은 정보지만 전달 방식이 다르다.",
   "SOA와 MSA는 같은 목표(서비스 분리)를 크기가 다른 단위로 실현한다. SOA는 큰 서비스, MSA는 작은 서비스다.",
   "SOA의 UDDI는 음식점 앱처럼 어떤 서비스가 있는지 찾아볼 수 있는 카탈로그다.",
   "SOA는 레고 블록처럼 표준화된 조각으로 IT 시스템을 조립해서 효율을 높이는 방법이에요.",
   "WSDL은 레고 블록의 연결 설명서, UDDI는 레고 블록 가게, SOAP는 실제 조립 방법이에요.",
   "지금은 SOA보다 더 작고 빠른 MSA와 REST 방식을 더 많이 사용해요.",
   "| ESB | SOA 구현 미들웨어 | 서비스 라우팅 |\n| REST API | SOA 대체 경량 인터페이스 | JSON/HTTP |\n| MSA | 마이크로서비스 아키텍처 | SOA 진화 |",
   "SOA는 레고 블록처럼 IT 기능을 표준화된 조각으로 만들어 다시 사용할 수 있게 하는 방법이에요.",
   "WSDL은 조각의 사용 설명서, UDDI는 조각 창고, SOAP는 조각을 주고받는 규칙이에요.",
   "현재는 더 간편한 REST와 MSA가 SOA를 대부분 대체하고 있어요.")),

(298, "298_esb_enterprise_bus.md", "298. ESB (Enterprise Service Bus) 엔터프라이즈 서비스 버스",
 t("ESB (Enterprise Service Bus)는 이기종 시스템 간의 서비스 요청과 응답을 중개하는 메시지 버스 미들웨어로, 라우팅·변환·오케스트레이션·모니터링 기능을 통합 제공한다.",
   "SOA 아키텍처에서 서비스 간 통신의 복잡성을 ESB가 흡수하여 각 서비스는 자신의 비즈니스 로직에만 집중하고 통합 로직을 ESB에 위임할 수 있다.",
   "ESB는 모든 통합 로직이 집중되는 단일 장애 점(SPoF, Single Point of Failure)이 될 수 있다. MSA 환경에서는 ESB 대신 경량 API 게이트웨이와 서비스 메시로 분산된 통합 아키텍처로 전환하는 추세다.",
   "ESB는 도시의 지하철 시스템이다. 각 기업 시스템(역)이 지하철(ESB)을 통해 메시지를 주고받으며, 지하철은 경로 안내(라우팅), 언어 번역(메시지 변환), 연착 알림(모니터링)을 담당한다.",
   """```
┌─────────────────────────────────────────────┐
│         ESB 핵심 기능                        │
├─────────────────────────────────────────────┤
│  라우팅 (Routing): 조건부 메시지 경로 결정  │
│  변환 (Transformation): XML↔JSON, 스키마 매핑│
│  오케스트레이션: 여러 서비스를 순서 조합    │
│  보안: 인증·암호화 중앙 처리                │
│  모니터링: 메시지 추적, 감사 로그           │
└─────────────────────────────────────────────┘
```
| ESB 기능 | 설명 |
|:---|:---|
| Content-based Routing | 메시지 내용으로 경로 결정 |
| Protocol Conversion | SOAP↔REST↔MQ 변환 |
| Service Orchestration | 여러 서비스 조합 실행 |""",
   """| 구분 | ESB | API Gateway |
|:---|:---|:---|
| 시대 | SOA(2000년대) | MSA(2010년대~) |
| 구조 | 중앙집중형 | 분산·경량 |
| 기능 | 풍부(변환·오케스트레이션) | 핵심(라우팅·인증) |""",
   "온프레미스 레거시 시스템(ERP, MES, CRM)이 혼재한 대형 제조 기업에서 ESB는 여전히 강력한 통합 솔루션이다. 클라우드 전환 시에는 ESB를 API 게이트웨이+이벤트 버스(Kafka)로 점진적으로 대체한다.",
   "ESB 도입으로 이기종 시스템 통합 비용 절감, 중앙집중식 보안·모니터링 확보, 서비스 오케스트레이션 기능 제공이 달성된다.",
   "ESB는 회사의 메시지 우체국이다. 모든 편지(메시지)가 여기를 거쳐 올바른 형식으로 변환되어 배달된다.",
   "ESB는 고속도로 인터체인지다. 여러 도로(프로토콜)의 차(메시지)를 올바른 방향으로 안내한다.",
   "ESB vs API Gateway는 대형 물류센터 vs 소형 택배 터미널이다. 복잡한 처리는 ESB, 빠른 배송은 API 게이트웨이가 담당한다.",
   "ESB는 공항의 환승 시스템이다. 국제선(SOA)은 복잡한 환승이 필요하지만, 국내선(MSA)은 간편하게 이동한다.",
   "ESB는 통합 전기 배전반이다. 모든 전기(데이터)가 여기서 올바른 전압(형식)으로 변환되어 각 기기(시스템)에 공급된다.",
   "| EAI | ESB 전신 통합 미들웨어 | SOA 기반 |\n| API Gateway | ESB 경량 대안 | MSA 환경 |\n| Kafka | 분산 이벤트 버스 | ESB 보완 |",
   "ESB는 여러 회사 시스템들 사이에서 메시지를 올바른 형식으로 바꿔 전달하는 우체국이에요.",
   "각 시스템이 서로 다른 언어를 써도 ESB가 통역해서 소통하게 해줘요.",
   "지금은 더 빠르고 가벼운 API 게이트웨이로 많이 대체되고 있어요.")),

(299, "299_restful_api_hateoas.md", "299. RESTful API 무상태성 (Stateless) HATEOAS",
 t("RESTful API는 HTTP 프로토콜의 GET/POST/PUT/DELETE 메서드와 URI로 자원(Resource)을 표현하고, 무상태성(Stateless), 클라이언트-서버 분리, 캐시 가능성 등 REST 6가지 제약 조건을 따르는 API 설계 스타일이다.",
   "SOAP 대비 경량(JSON 기반), 구현 간결성, 다양한 클라이언트(웹·앱·IoT) 지원이 장점으로 현대 API 설계의 사실상 표준이다.",
   "HATEOAS (Hypermedia As The Engine Of Application State)는 REST의 마지막 성숙도 단계로, API 응답에 다음 가능한 액션의 링크를 포함하여 클라이언트가 API 문서 없이도 탐색 가능하게 한다. Richardson Maturity Model Level 3에 해당한다.",
   "REST (Representational State Transfer)는 로이 필딩(Roy Fielding)이 2000년 박사 논문에서 제안한 아키텍처 스타일이다. 무상태성(Stateless)은 각 요청이 독립적이며 서버가 클라이언트 상태를 저장하지 않음을 의미한다.",
   """```
┌────────────────────────────────────────────────┐
│  Richardson Maturity Model (REST 성숙도)        │
│  Level 0: HTTP 터널 (SOAP over HTTP)           │
│  Level 1: 자원(Resource) URI 사용              │
│  Level 2: HTTP 메서드(GET/POST/PUT/DELETE)사용 │
│  Level 3: HATEOAS (링크 기반 탐색)             │
└────────────────────────────────────────────────┘
```
| HTTP 메서드 | CRUD | 의미 |
|:---|:---|:---|
| GET | Read | 자원 조회 |
| POST | Create | 자원 생성 |
| PUT/PATCH | Update | 자원 수정 |
| DELETE | Delete | 자원 삭제 |""",
   """| 구분 | REST | GraphQL |
|:---|:---|:---|
| 쿼리 방식 | 엔드포인트별 고정 | 단일 엔드포인트 유연 쿼리 |
| 과다/과소 페치 | 발생 가능 | 최적화 가능 |
| 학습 곡선 | 낮음 | 높음 |""",
   "OAuth 2.0 + RESTful API로 소셜 로그인(Google, Kakao)을 구현할 때 Authorization Code Flow, 토큰 갱신, CORS 설정이 핵심 고려사항이다.",
   "RESTful API 설계로 클라이언트-서버 분리(프론트/백엔드 독립 개발), API 버전 관리, 수평 확장(무상태성 덕분에 로드 밸런서 투명 스케일링)이 달성된다.",
   "REST는 도서관 대출 시스템이다. 책(자원)을 빌리고(GET), 반납하고(DELETE), 예약하는(POST) 각 행위가 명확히 분리되어 있다.",
   "HATEOAS는 앱의 내비게이션 메뉴다. API 응답에 다음에 갈 수 있는 곳이 링크로 포함된다.",
   "REST vs GraphQL은 뷔페 vs 코스 메뉴다. REST는 정해진 메뉴(엔드포인트), GraphQL은 원하는 것만 골라 먹을 수 있다.",
   "RESTful API는 웹의 공통 언어다. 어떤 클라이언트(웹, 앱, IoT)와도 같은 방식으로 대화할 수 있다.",
   "REST는 음식점 주문 시스템이다. 주문(POST), 주문 확인(GET), 취소(DELETE)가 각각 명확하다.",
   "| SOAP | REST 이전 XML 기반 API | 무거움 |\n| GraphQL | REST 대안 유연 쿼리 | Facebook 개발 |\n| OpenAPI | REST API 명세 표준 | Swagger |",
   "RESTful API는 인터넷에서 프로그램끼리 대화하는 표준 규칙이에요. 택배 주문(POST), 배송 조회(GET), 취소(DELETE)처럼요.",
   "무상태성은 서버가 이전에 뭘 했는지 기억하지 않아서, 어떤 서버에게 요청해도 동일한 응답을 받는 거예요.",
   "현재 거의 모든 앱과 웹서비스가 RESTful API로 서로 소통해요.")),

(300, "300_msa_microservice.md", "300. MSA (Microservice Architecture) 독립 배포 폴리글랏",
 t("MSA (Microservice Architecture)는 하나의 모놀리틱(Monolithic) 애플리케이션을 독립적으로 배포 가능한 작은 서비스들로 분해하여, 서비스별 독립적 개발·배포·확장·장애 격리를 실현하는 아키텍처 스타일이다.",
   "넷플릭스·아마존의 사례처럼 조직 규모와 배포 속도가 임계점을 넘으면 모놀리식의 배포 병목과 장애 전파가 비즈니스 리스크가 되므로, MSA로 전환하여 팀 자율성과 배포 민첩성을 확보한다.",
   "MSA는 조직 구조(콘웨이의 법칙)와 일치해야 한다. 각 마이크로서비스는 하나의 피자 두 판을 먹을 수 있는 팀(Two-Pizza Team, 5~8명)이 독립적으로 소유·운영한다.",
   "모놀리식에서 MSA로 전환하는 것을 '스트랭글러 피그 패턴'이라고 한다. 한 번에 전체를 전환하지 않고, 기능을 하나씩 서비스로 분리하면서 점진적으로 모놀리식을 대체한다.",
   """```
┌──────────────────────────────────────────────┐
│  모놀리식 vs MSA 비교                        │
├──────────────────┬───────────────────────────┤
│  모놀리식         │  MSA                      │
├──────────────────┼───────────────────────────┤
│  단일 코드베이스  │  서비스별 독립 저장소     │
│  공유 DB         │  서비스별 DB(폴리글랏)    │
│  일체형 배포      │  독립 배포 (CI/CD)        │
│  수직 확장        │  수평 확장 (오토스케일링)  │
└──────────────────┴───────────────────────────┘
```
| MSA 핵심 원칙 | 설명 |
|:---|:---|
| 단일 책임 | 하나의 서비스가 하나의 비즈니스 역할 |
| 폴리글랏 | 서비스마다 최적 기술 스택 선택 |
| 장애 격리 | 하나의 서비스 장애가 전체에 전파 안 됨 |""",
   """| 구분 | 모놀리식 | MSA |
|:---|:---|:---|
| 배포 | 전체 동시 | 서비스별 독립 |
| 확장 | 전체 스케일업 | 서비스별 스케일아웃 |
| 복잡성 | 코드 복잡 | 운영 복잡 |""",
   "쿠팡·배달의민족의 사례: 주문·결제·배달 서비스를 독립 MSA로 분리하여 쇼핑 시즌(블랙프라이데이) 때 결제 서비스만 100배 스케일아웃이 가능해졌다.",
   "MSA 도입으로 배포 속도 향상(하루 수백 회 배포 가능), 장애 격리, 팀 자율성 확보, 기술 다양성(폴리글랏) 실현이 달성된다.",
   "MSA는 레스토랑의 분업이다. 주방(주문), 바(결제), 케이터링(배달)이 독립적으로 운영되어 하나가 문제가 생겨도 다른 팀은 계속 일한다.",
   "폴리글랏은 각 서비스팀이 최적의 도구(Java, Go, Python)를 선택하는 자유다.",
   "모놀리식 vs MSA는 대형마트 vs 전문점 거리다. 대형마트(모놀리식)는 편하지만 한 코너가 문제면 전체 영향, 전문점 거리(MSA)는 각 가게가 독립적이다.",
   "MSA의 운영 복잡성은 분산 트랜잭션, 서비스 메시, 관찰 가능성(Observability) 도구로 관리한다.",
   "MSA는 도시 계획이다. 각 지역(서비스)이 독립적으로 발전하지만 교통망(API)으로 연결된 유기적 도시다.",
   "| DDD | 도메인 주도 설계 - MSA 경계 정의 | 바운디드 컨텍스트 |\n| Kubernetes | 컨테이너 오케스트레이션 | MSA 운영 플랫폼 |\n| 서비스 메시 | Istio - MSA 통신 제어 | 사이드카 패턴 |",
   "MSA는 LEGO 세트처럼 작은 블록(서비스)들이 모여 큰 제품(애플리케이션)을 만드는 방법이에요.",
   "하나의 블록이 부서져도 다른 블록들은 멀쩡하게 동작해요. 그게 MSA의 장애 격리예요.",
   "각 팀이 자기 블록을 알아서 만들고 업데이트할 수 있어서 훨씬 빠르게 개발할 수 있어요.")),

(301, "301_api_gateway_bff.md", "301. API 게이트웨이 (API Gateway) / BFF 패턴",
 t("API 게이트웨이 (API Gateway)는 클라이언트와 마이크로서비스 사이의 단일 진입점(Single Entry Point)으로, 인증·인가, 라우팅, 속도 제한, 로드 밸런싱, SSL 종료, 모니터링을 통합 처리한다.",
   "수백 개의 마이크로서비스를 클라이언트가 직접 호출하는 복잡성을 API 게이트웨이가 추상화하여, 클라이언트 코드 변경 없이 백엔드 서비스를 독립적으로 리팩토링할 수 있다.",
   "BFF (Backend for Frontend) 패턴은 모바일 앱·웹·TV 등 클라이언트 유형별로 별도 API 게이트웨이를 두어 각 클라이언트의 최적 응답 형식과 데이터 집계를 분리 처리한다.",
   "API 게이트웨이는 마이크로서비스 아키텍처의 현관문이다. 모든 외부 요청이 여기를 통과하며 인증(JWT 검증), 라우팅(주문서비스→/orders), 속도 제한(1000 req/min), 캐싱이 일괄 처리된다.",
   """```
┌──────────────────────────────────────────────────┐
│  BFF 패턴 구조                                   │
│  [모바일 앱]→[Mobile BFF]→[주문/결제/배달 서비스]│
│  [웹 브라우저]→[Web BFF]→[주문/결제/배달 서비스] │
│  [TV 앱]→[TV BFF]→[컨텐츠/추천 서비스]           │
└──────────────────────────────────────────────────┘
```
| API Gateway 기능 | 설명 |
|:---|:---|
| 인증/인가 | JWT, OAuth 2.0 토큰 검증 |
| 라우팅 | URI 기반 서비스 매핑 |
| Rate Limiting | API 남용 방지 |
| Circuit Breaker | 장애 서비스 차단 |""",
   """| 구분 | API Gateway | BFF |
|:---|:---|:---|
| 대상 | 모든 클라이언트 공통 | 클라이언트 유형별 |
| 최적화 | 일반 처리 | 클라이언트별 특화 |
| 복잡성 | 낮음 | 높음(여러 BFF 관리) |""",
   "넷플릭스는 TV·모바일·웹·게임 콘솔 등 1000여 개 기기에 최적화된 응답을 BFF로 제공한다. 모바일 BFF는 낮은 대역폭을 위해 이미지를 압축하고, TV BFF는 고화질 스트림을 준비한다.",
   "API 게이트웨이 도입으로 마이크로서비스 복잡성 캡슐화, 중앙집중식 보안·모니터링, 클라이언트 코드 단순화, A/B 테스팅 지원이 달성된다.",
   "API 게이트웨이는 호텔 프론트 데스크다. 모든 투숙객(클라이언트)이 프론트를 통해 각 서비스(방/식당/수영장)로 안내된다.",
   "BFF는 고객층별 맞춤 안내 직원이다. 외국인(모바일), 노인(TV), 비즈니스(웹)에게 각각 적합한 방식으로 서비스한다.",
   "API Gateway vs BFF는 공항 종합 안내 vs VIP 전용 라운지다.",
   "API 게이트웨이 없이 MSA 운영은 100개 가게(서비스)가 각자 입구·보안·결제를 따로 관리하는 혼란과 같다.",
   "API 게이트웨이는 아파트 경비원이다. 방문객(요청)이 오면 누구인지 확인(인증)하고 올바른 동호수(서비스)로 안내(라우팅)한다.",
   "| Kong | 오픈소스 API Gateway | 플러그인 확장 |\n| AWS API Gateway | 서버리스 API 관리 | Lambda 연계 |\n| OAuth 2.0 | 표준 인증 프레임워크 | JWT 토큰 |",
   "API 게이트웨이는 어떤 손님이 어느 방으로 가야 하는지 알려주는 호텔 안내 직원이에요.",
   "BFF는 어린이 손님(모바일)과 어른 손님(웹)에게 각각 다른 메뉴를 제공하는 맞춤 서비스예요.",
   "모든 요청이 하나의 문(API Gateway)을 통과하니까 보안과 관리가 훨씬 쉬워져요.")),
]

for data in files:
    num, filename, title, body = data
    filepath = os.path.join(BASE, filename)
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(make(num, filename, title, body))
        print(f"Created {filename}")
    else:
        print(f"Skipped: {filename}")

print("Batch complete!")
