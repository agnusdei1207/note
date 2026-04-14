+++
weight = 109
title = "소프트웨어 자재 명세서 (SBOM) 추출 의무화 (SBOM Extraction in Pipeline)"
date = "2026-03-04"
[extra]
categories = ["studynote-devops-sre", "cicd-gitops"]
+++

## 핵심 인사이트 (3줄 요약)
- SBOM(Software Bill of Materials)은 소프트웨어를 구성하는 모든 오픈소스 라이브러리, 버전, 의존성 관계를 낱낱이 기록한 '디지털 자재 명세서'임.
- CI/CD 파이프라인에서 빌드 시점에 자동으로 SBOM을 추출함으로써, Log4j 사태와 같은 공급망 공격(Supply Chain Attack) 발생 시 취약점 포함 여부를 실시간으로 전수 조사할 수 있음.
- 미 행정명령(EO 14028) 등 글로벌 보안 표준으로 급부상하고 있으며, 소프트웨어 투명성과 무결성을 보장하는 현대적 DevSecOps의 필수 아티팩트임.

### Ⅰ. 개요 (Context & Background)
우리가 만드는 소프트웨어의 80~90%는 오픈소스다. 만약 우리가 쓴 특정 오픈소스 라이브러리에 해커가 악성코드를 심었다면, 우리 제품도 해킹 도구가 된다. 이것이 '소프트웨어 공급망 공격'이다. 문제는 우리가 어떤 라이브러리를 썼는지, 그 라이브러리가 또 어떤 라이브러리를 끌어다 쓰는지(Transitive Dependency) 모르는 경우가 태반이라는 점이다. SBOM은 이 복잡한 족보를 문서화하여 보안 사고 발생 시 "우리가 위험한가?"라는 질문에 즉각 답하기 위해 도입되었다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

SBOM 추출은 빌드 과정 중에 종속성 트리(Dependency Tree)를 분석하여 기계가 읽을 수 있는 포맷으로 저장한다.

```text
[ SBOM Extraction Pipeline Flow ]

+--------------+       +--------------+       +-------------------------+
| Source Code  | ----> | Build Engine | ----> | SBOM Generator (Tool)   |
| (pom, npm)   |       | (Maven, npm) |       | (Syft, Trivy, CycloneDX)|
+--------------+       +--------------+       +------------+------------+
                                                           |
                    +--------------------------------------v-----------+
                    |  Standard SBOM Formats (JSON/XML/Tag-Value)      |
                    |  - SPDX (ISO/IEC 5962:2021)                      |
                    |  - CycloneDX (OWASP Standard)                    |
                    +--------------------------------------------------+

[ Bilingual Comparison ]
- Inventory (재고 목록): 포함된 모든 컴포넌트 리스트.
- Dependency (의존성): 라이브러리 간의 연결 고리.
- Vulnerability Scanning (취약점 스캔): SBOM을 기반으로 CVE 데이터베이스와 대조.
- Provenance (출처): 소스코드가 어디서 왔고 누가 빌드했는지에 대한 증빙.
```

단순한 텍스트 파일이 아니라 SPDX나 CycloneDX 같은 '기계 판독형 표준 포맷'으로 생성되어야 다른 보안 도구들과 연동되어 자동 분석이 가능하다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 정적 분석 (SAST) | 오픈소스 스캔 (SCA) | SBOM 추출 |
| :--- | :--- | :--- | :--- |
| **분석 대상** | 내가 짠 소스코드 | 사용 중인 라이브러리 취약점 | **전체 구성 요소의 명세/족보** |
| **목적** | 코딩 실수(SQLi 등) 탐지 | 알려진 취약점(CVE) 탐지 | **투명성 확보 및 공급망 관리** |
| **산출물** | 취약점 리포트 | 패치 권고 리포트 | **표준 명세서 (JSON/SPDX)** |
| **시점** | 코딩/빌드 단계 | 빌드 단계 | **빌드/패키징 단계 (의무화)** |
| **상호작용** | - | SBOM을 입력값으로 사용함 | SCA의 기초 데이터가 됨 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **(의존성 깊이 제어)** 직접 설치한 라이브러리뿐만 아니라, 그 라이브러리가 끌어오는 하위 의존성(Deep Dependency)까지 모두 포함하는 'Full Inventory' 추출이 원칙이다.
- **(검증 및 서명)** 추출된 SBOM 자체가 위조되면 의미가 없다. 따라서 SBOM 파일에 디지털 서명(Sigstore, Cosign)을 부착하여, 배포 시점에 "이 SBOM은 빌드 서버에서 생성된 정품이 맞다"는 것을 검증해야 한다.
- **(VEX 연계)** SBOM은 취약점이 있다는 것만 알려준다. 실제 우리 앱에서 그 취약한 함수가 실행되지 않는다면(Non-exploitable), VEX(Vulnerability Exploitability eXchange) 문서를 통해 보안 조치 예외 사유를 명시하여 불필요한 대응 비용을 줄인다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
SBOM은 이제 선택이 아닌 생존의 문제다. 구글의 SLSA(Salsa) 프레임워크와 결합하여 소프트웨어 빌드 전 과정의 무결성을 증명하는 핵심 증거로 활용될 것이다. 향후에는 모든 기업이 소프트웨어를 구매할 때 '영양성분표'를 보듯 SBOM 제출을 요구하는 시대가 올 것이며, 기술사는 이를 수용할 수 있는 자동화 파이프라인 표준을 선제적으로 구축해야 한다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **Software Supply Chain**: 전체 맥락
- **SPDX / CycloneDX**: 데이터 표준 포맷
- **CVE (Common Vulnerabilities and Exposures)**: 대조 대상
- **SLSA (Supply-chain Levels for Software Artifacts)**: 보안 등급 체계

### 👶 어린이를 위한 3줄 비유 설명
- 우리가 먹는 과자 뒤에 어떤 재료가 들어갔는지 적힌 '성분표'를 본 적 있니?
- SBOM은 컴퓨터 프로그램에 어떤 재료(라이브러리)가 들어갔는지 꼼꼼하게 적어둔 명세서야.
- 만약 나쁜 재료(취약점)가 발견되면, 이 명세서를 보고 우리가 먹는 과자가 안전한지 바로 확인할 수 있단다!
