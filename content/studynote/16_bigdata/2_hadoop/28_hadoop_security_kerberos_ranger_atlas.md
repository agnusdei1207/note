+++
weight = 29
title = "Hadoop 보안: Kerberos, Ranger, Atlas"
date = "2024-03-24"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
- **강력한 인증 (Kerberos):** 사용자 및 서비스 간 신뢰 관계를 티켓 기반으로 증명하여 "누가" 접속하는지 철저히 검증.
- **세밀한 권한 제어 (Ranger):** 태그 및 정책 기반으로 데이터셋(HDFS, Hive 등)에 대해 "무엇을" 할 수 있는지 중앙 집중식으로 통제.
- **데이터 거버넌스 (Atlas):** 메타데이터 관리와 리니지(Lineage) 추적을 통해 데이터의 출처와 흐름을 시각화하고 규제를 준수.

### Ⅰ. 개요 (Context & Background)
초기 하둡은 신뢰할 수 있는 내부 네트워크 환경을 가정하여 보안에 취약했습니다. 하지만 기업용 빅데이터 플랫폼으로 발전하면서 금융/의료 등 민감 데이터를 다루게 됨에 따라 강력한 보안 프레임워크가 필수 요소가 되었습니다. '보안 하둡'은 인증(Authentication), 인가(Authorization), 감사(Audit), 거버넌스(Governance)의 4대 영역을 통합적으로 구축하는 것을 의미합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
하둡 보안 아키텍처는 Kerberos를 통한 신원 증명 위에 Ranger의 정책 통제와 Atlas의 흐름 관리가 결합된 구조입니다.

```text
[ Hadoop Security Architecture ]

   (User) --[ 1. Authenticate ]--> [ Kerberos KDC ]
     |                                  | (TGT Ticket)
     | --[ 2. Request Data ]--> [ Hadoop Service (Hive/HBase) ]
                                        |
     [ Apache Ranger ] <---[ 3. Access Check ]---
     (Access Policies)                  |
                                        |
     [ Apache Atlas ] <----[ 4. Track Lineage ]---
     (Metadata/History)
```

**핵심 컴포넌트:**
1. **Kerberos:** KDC(Key Distribution Center)를 통해 대칭키 암호화 기반의 티켓을 발행. 패스워드 전송 없이 안전한 상호 인증 수행.
2. **Apache Ranger:** HDFS, Hive, Kafka 등 다양한 에코시스템의 권한 정책을 UI에서 통합 관리. 동적 마스킹(Masking) 및 행(Row) 수준 필터링 지원.
3. **Apache Atlas:** 데이터 분류(Classification) 태그를 생성하고, Ranger가 이 태그를 인식하여 접근을 차단하는 '태그 기반 보안(Tag-based Security)' 구현.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 보안 계층 | 핵심 도구 | 주요 기능 | 비유 |
| :--- | :--- | :--- | :--- |
| **인증 (AuthN)** | Kerberos | 사용자 신분증 확인, 티켓 발급 | 건물 정문 출입 카드 |
| **인가 (AuthZ)** | Apache Ranger | 폴더/테이블별 접근 및 실행 권한 | 특정 사무실 열쇠 권한 |
| **감사 (Audit)** | Ranger Audit | 모든 접근 기록(Who, When, What) 로그 저장 | 복도 CCTV 및 출입 기록 |
| **거버넌스 (Gov)** | Apache Atlas | 데이터 리니지 추적, 메타데이터 관리 | 문서 족보 및 폐기 이력 관리 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **실무 적용:** 하이브(Hive) 테이블의 개인정보 컬럼에 Atlas로 'PII' 태그를 달고, Ranger에서 "일반 분석가는 PII 태그가 달린 데이터를 마스킹 처리해서 보라"는 정책을 설정하면 자동화된 데이터 보안 체계가 완성됩니다.
- **기술사적 판단:** 하둡 보안은 시스템 복잡도를 높이고 성능 저하(Overhead)를 유발할 수 있습니다. 기술사는 보안 요구 수준에 따라 Kerberos 인증 범위를 최적화하고, Ranger의 캐싱 기능을 활용하여 지연 시간(Latency)을 최소화하는 아키텍처 설계를 주도해야 합니다. 특히 데이터 3법 준수를 위해 '가명정보 처리'와 '리니지 확보'를 동시에 해결하는 Atlas-Ranger 연동이 핵심 전략입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
하둡 보안은 '제로 트러스트' 보안 모델의 빅데이터 버전입니다. 클라우드 전환 환경에서도 Ranger와 Atlas는 오픈 소스 기반의 표준 거버넌스 도구로 자리 잡고 있으며, 향후 AI 모델 학습 데이터의 투명성을 증명하는 'AI 거버넌스'로 확장될 전망입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Big Data Security, Data Governance
- **하위 개념:** KDC, Principal, RBAC, Tag-based Access Control
- **연관 기술:** Apache Knox (Gateway), Sentry (Legacy AuthZ), LDAP/AD

### 👶 어린이를 위한 3줄 비유 설명
1. 도서관(하둡)에 들어갈 때 가짜 학생이 아닌지 학생증(Kerberos)을 꼼꼼히 검사해요.
2. 도서관 안에서도 내가 볼 수 있는 책과 없는 책(Ranger)이 정해져 있어서 권한이 없으면 못 봐요.
3. 내가 책을 빌려가서 친구에게 빌려주고 돌려받는 모든 과정(Atlas)은 장부에 꼼꼼히 기록된답니다.
