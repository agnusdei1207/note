+++
title = "종속성 (Dependencies) 격리"
description = "명시적으로 선언된 종속성과 격리된 실행 환경에 대한 심층 기술 백서"
date = 2024-05-15
[taxonomies]
tags = ["Dependencies", "12-Factor App", "Package Management", "Dependency Injection", "Software Supply Chain"]
+++

# 종속성 (Dependencies) 격리

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 종속성 격리는 12-Factor App의 핵심 원칙으로, 애플리케이션이 의존하는 모든 라이브러리와 패키지를 "명시적으로 선언(Declare)"하고 실행 환경으로부터 "완전히 격리(Isolate)"하여, 시스템 전역 도구에 의존하지 않고 애플리케이션이 자체적인 독립 환경에서 실행되도록 보장하는 기법입니다.
> 2. **가치**: 종속성 격리는 "내 컴퓨터에서는 되는데 서버에서는 안 돼요" 문제를 근본적으로 해결하고, 버전 충돌을 방지하며, 소프트웨어 공급망 보안(Supply Chain Security)을 강화하여 재현 가능한(Reproducible) 빌드를 보장합니다.
> 3. **융합**: 패키지 매니저(npm, pip, Maven), 가상 환경(venv, conda), 컨테이너(Docker), 의존성 주입(DI) 프레임워크와 결합하여 개발부터 프로덕션까지 일관된 의존성 관리 체계를 구축합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**종속성(Dependency)**이란 애플리케이션이 정상적으로 동작하기 위해 필요한 외부 라이브러리, 프레임워크, 패키지를 말합니다. 예를 들어, Python 애플리케이션이 `requests` 라이브러리를 사용한다면, `requests`는 이 애플리케이션의 종속성입니다.

**종속성 격리(Dependency Isolation)**는 12-Factor App의 두 번째와 세 번째 원칙을 포괄하는 개념으로:
- **명시적 선언(Explicit Declaration)**: 모든 종속성을 `package.json`, `requirements.txt`, `pom.xml` 같은 선언적 매니페스트 파일에 명시합니다.
- **격리(Isolation)**: 애플리케이션이 시스템 전역(Global)의 라이브러리에 의존하지 않고, 자체적인 격리된 환경(Virtual Environment, Container)에서 실행됩니다.
- **재현성(Reproducibility)**: 어떤 머신에서든 동일한 종속성 버전이 설치되어 동일한 동작을 보장합니다.

### 💡 2. 구체적인 일상생활 비유
**요리 키트(Meal Kit)**를 상상해 보세요. 요리 키트에는 레시피뿐만 아니라 그 요리에 필요한 **모든 재료가 정확한 양만큼** 포함되어 있습니다:
- **명시적 선언**: 레시피에 "토마토 200g, 양파 1개, 올리브유 30ml"가 명시되어 있습니다.
- **격리**: 요리 키트에 포함된 재료만 사용하고, 집에 있는 다른 재료(예: 1년 된 올리브유)를 사용하지 않습니다.
- **재현성**: 친구 집에서도 동일한 요리 키트를 사용하면 똑같은 맛이 나옵니다.

반면, 종속성 격리가 없는 상황은 **"집에 있는 재료를 알아서 찾아 쓰세요"**라는 요리법과 같습니다. 친구 집에는 올리브유이 없어서 식용유를 쓰게 되고, 맛이 완전히 달라집니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (DLL Hell, Dependency Hell)**:
   - **Windows DLL Hell**: 여러 애플리케이션이 동일한 DLL을 서로 다른 버전으로 필요로 할 때, 하나의 시스템 전역 위치에 DLL을 설치하면 버전 충돌이 발생했습니다.
   - **Python Import 충돌**: 시스템에 설치된 `requests==2.25.0`을 앱 A가 필요로 하는데, 앱 B가 `requests==2.28.0`을 설치하면 앱 A가 깨집니다.
   - **Node.js node_modules 폭증**: 프로젝트마다 node_modules를 설치하면 디스크가 순식간에 가득 찹니다.

2. **혁신적 패러다임 변화의 시작**:
   - 1990년대: Perl의 `cpan`, Java의 `Maven`이 의존성 관리 개념을 도입했습니다.
   - 2000년대: Python의 `virtualenv`, Ruby의 `bundler`가 환경 격리 개념을 도입했습니다.
   - 2010년대: Docker 컨테이너가 OS 수준의 완전한 격리를 제공했습니다.
   - 현재: SCA(Software Composition Analysis), SBOM이 보안 중심의 의존성 관리로 진화했습니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   - Log4j 취약점(CVE-2021-44228) 사태 이후, 조직은 모든 종속성의 버전과 취약점을 실시간으로 파악해야 합니다.
   - 공급망 공격(Supply Chain Attack) 방어를 위해 종속성의 무결성 검증이 필수입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Module) | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **패키지 매니저** | 종속성 선언, 다운로드, 버전 관리 | 중앙 저장소(PyPI, npm, Maven Central)에서 패키지 다운로드 및 캐싱 | pip, npm, yarn, Maven, Gradle | 쇼핑 카트 + 배송 서비스 |
| **락 파일 (Lock File)** | 정확한 버전 고정 및 재현성 보장 | 해시(SHA) 기반 무결성 검증, 전이적 종속성 버전 기록 | package-lock.json, Pipfile.lock, pom.xml | 영수증 (정확한 구매 내역) |
| **가상 환경 (Virtual Env)** | 프로젝트별 격리된 실행 환경 | 전역 site-packages와 분리된 독립 디렉토리에 패키지 설치 | venv, conda, virtualenv | 개인 요리 공간 |
| **컨테이너 (Container)** | OS 수준의 완전한 격리 | Namespace, cgroups를 통한 프로세스, 네트워크, 파일시스템 격리 | Docker, Podman, containerd | 개인 주방 (완전 격리) |
| **프라이빗 레지스트리** | 내부 패키지 저장소 및 캐싱 | 외부 저장소 미러링, 취약점 스캔, 접근 제어 | Nexus, Artifactory, AWS ECR | 도매 창고 |

### 2. 정교한 구조 다이어그램: 종속성 격리 아키텍처

```text
=====================================================================================================
                    [ Dependency Isolation Architecture - Full Stack ]
=====================================================================================================

+-------------------------------------------------------------------------------------------+
|                              [ DEVELOPMENT ENVIRONMENT ]                                  |
|                                                                                           |
|  +-------------------------+      +-------------------------+      +-------------------+  |
|  | Project A (Django)      |      | Project B (Flask)       |      | Project C (FastAPI)| |
|  |                         |      |                         |      |                   |  |
|  | +---------------------+ |      | +---------------------+ |      | +---------------+ |  |
|  | | Virtual Environment | |      | | Virtual Environment | |      | | Virtual Env   | |  |
|  | | (.venv/)            | |      | | (.venv/)            | |      | | (.venv/)      | |  |
|  | |                     | |      | |                     | |      | |               | |  |
|  | | - Django==4.2.0     | |      | | - Flask==2.3.0      | |      | | - FastAPI=0.100| |  |
|  | | - requests==2.28.0  | |      | | - requests==2.25.0  | |      | | - requests=2.31| |  |
|  | | - psycopg2==2.9.6   | |      | | - SQLAlchemy==1.4.x | |      | | - pydantic=2.0| |  |
|  | +---------------------+ |      | +---------------------+ |      | +---------------+ |  |
|  |                         |      |                         |      |                   |  |
|  | requirements.txt        |      | requirements.txt        |      | pyproject.toml    |  |
|  +-------------------------+      +-------------------------+      +-------------------+  |
|                                                                                           |
|  ※ 각 프로젝트는 서로 다른 버전의 'requests'를 사용하지만 충돌하지 않음 (격리됨)          |
+-------------------------------------------------------------------------------------------+
                                          │
                                          │ pip install / npm install
                                          ▼
+-------------------------------------------------------------------------------------------+
|                              [ PACKAGE MANAGEMENT LAYER ]                                |
|                                                                                           |
|  +-------------------+     +-------------------+     +-------------------------------+   |
|  | Manifest File     │     | Lock File         │     | Private Registry (Proxy)      |   |
|  | (선언적 의존성)    │     | (정확한 버전 고정) │     | (캐싱 + 보안 스캔)            |   |
|  +-------------------+     +-------------------+     +-------------------------------+   |
|  | package.json      │     | package-lock.json │     | Nexus / Artifactory           |   |
|  | requirements.txt  │────▶| Pipfile.lock      │────▶│ - 외부 저장소 미러링          |   |
|  | pom.xml           │     | pom.xml (해시)    │     │ - 취약점 스캔 (Trivy)         |   |
|  | Cargo.toml        │     | Cargo.lock        │     │ - 접근 로그 및 감사           |   |
|  +-------------------+     +-------------------+     +-------------------------------+   |
|                                                                                           |
+-------------------------------------------------------------------------------------------+
                                          │
                                          │ docker build
                                          ▼
+-------------------------------------------------------------------------------------------+
|                              [ CONTAINER ISOLATION LAYER ]                               |
|                                                                                           |
|  +-------------------------------------------------------------------------------------+  |
|  | Dockerfile                                                                          |  |
|  |                                                                                     |  |
|  | FROM python:3.11-slim                    # 베이스 이미지 (격리된 OS)             |  |
|  | WORKDIR /app                                                                         |  |
|  | COPY requirements.txt .                                                              |  |
|  | RUN pip install --no-cache-dir -r requirements.txt  # 컨테이너 내부에만 설치      |  |
|  | COPY . .                                                                             |  |
|  | CMD ["python", "app.py"]                                                             |  |
|  +-------------------------------------------------------------------------------------+  |
|                                                                                           |
|  +-------------------+     +-------------------+     +-------------------+               |
|  | Container A       |     | Container B       |     | Container C       |               |
|  | (격리된 파일시스템)│     | (격리된 파일시스템)│     | (격리된 파일시스템)│               |
|  | /usr/local/lib/   |     | /usr/local/lib/   |     | /usr/local/lib/   |               |
|  │  python3.11/      │     │  python3.11/      │     │  python3.11/      |               |
|  |  site-packages/   |     |  site-packages/   |     |  site-packages/   |               |
|  +-------------------+     +-------------------+     +-------------------+               |
|                                                                                           |
|  ※ 컨테이너 간 완전한 격리: 서로의 라이브러리를 전혀 볼 수 없음                           |
+-------------------------------------------------------------------------------------------+

=====================================================================================================
   ※ 12-Factor App 종속성 원칙 준수:
   1. 모든 종속성은 Manifest File에 명시적으로 선언
   2. 시스템 전역 도구에 의존하지 않고 격리된 환경에서 실행
   3. Lock File로 정확한 버전 고정하여 재현성 보장
=====================================================================================================
```

### 3. 심층 동작 원리 (종속성 해결 및 격리 과정)

**1단계: 종속성 선언 (Declaration)**
```json
// package.json - 명시적 종속성 선언
{
  "name": "my-application",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.0",      // 캐럿(^): 4.18.x 허용, 4.19.0도 OK
    "lodash": "~4.17.21",      // 틸드(~): 4.17.21만 허용, 4.17.22는 OK, 4.18.0은 NO
    "axios": "1.4.0"           // 정확히 1.4.0만 허용
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "typescript": "^5.0.0"
  }
}
```

**2단계: 종속성 해결 (Resolution)**
```
패키지 매니저의 종속성 해결 알고리즘:
1. express ^4.18.0 요청
2. npm 레지스트리 조회 → 4.18.2가 최신 매칭 버전
3. express의 전이적 종속성 확인:
   - body-parser: ^1.20.0
   - cookie: ~0.5.0
   - ... (수십 개의 하위 종속성)
4. 종속성 트리 구성 및 버전 충돌 해결
```

**3단계: 락 파일 생성 (Locking)**
```json
// package-lock.json - 정확한 버전 고정
{
  "name": "my-application",
  "lockfileVersion": 3,
  "packages": {
    "node_modules/express": {
      "version": "4.18.2",
      "resolved": "https://registry.npmjs.org/express/-/express-4.18.2.tgz",
      "integrity": "sha512-5/PsL6iGPdfQ/lKM1UuielYgv3BUoJfz1aUwU9vHZ+J7gyvwdQXFEBIEIaxeGf0GIcreATNyBExtalisDbwM8w==",
      "dependencies": {
        "body-parser": "1.20.1",
        "cookie": "0.5.0"
      }
    }
  }
}
```

**4단계: 격리된 설치 (Isolation)**
```bash
# Python 가상 환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 격리된 환경에만 패키지 설치
pip install -r requirements.txt

# 설치 위치 확인 (전역이 아닌 .venv 내부)
which python  # /path/to/project/.venv/bin/python
pip list      # .venv/lib/python3.11/site-packages에 설치된 패키지 목록
```

**5단계: 컨테이너 격리 (Container Isolation)**
```dockerfile
# Dockerfile - 완전한 OS 수준 격리
FROM python:3.11-slim-bookworm

# 시스템 종속성 설치 (컨테이너 내부에만)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 가상 환경 생성 (컨테이너 내부)
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 종속성 설치 (컨테이너 내부의 가상 환경에)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . /app
WORKDIR /app

CMD ["python", "main.py"]
```

### 4. 실무 코드 예시 (다양한 언어의 종속성 관리)

```python
# Python: pyproject.toml (현대적 표준)
[project]
name = "my-application"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.100.0,<0.110.0",
    "uvicorn[standard]>=0.23.0",
    "pydantic>=2.0.0",
    "sqlalchemy>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
]

# poetry.lock이 생성되어 정확한 버전 보장
```

```xml
<!-- Maven: pom.xml -->
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-application</artifactId>
    <version>1.0.0</version>

    <properties>
        <spring.version>6.1.0</spring.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-web</artifactId>
            <version>${spring.version}</version>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.15.0</version>
        </dependency>
    </dependencies>

    <!-- Maven Enforcer: 버전 충돌 방지 -->
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-enforcer-plugin</artifactId>
                <executions>
                    <execution>
                        <id>enforce-versions</id>
                        <goals><goal>enforce</goal></goals>
                        <configuration>
                            <rules>
                                <dependencyConvergence/>
                            </rules>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 종속성 관리 전략 비교표

| 전략 | 장점 | 단점 | 적합한 상황 |
| :--- | :--- | :--- | :--- |
| **고정 버전 (Pinned)** | 완전한 재현성, 예측 가능 | 보안 업데이트 수동 적용 | 프로덕션, 규제 환경 |
| **유연 버전 (Range)** | 자동 보안 업데이트 | 예기치 않은 동작 변화 | 개발, 라이브러리 |
| **Lock 파일 우선** | 개발/프로덕션 일치 | Lock 파일 관리 필요 | 대부분의 프로젝트 |
| **모놀리식 의존성** | 버전 관리 용이 | 유연성 부족 | 소규모 프로젝트 |

### 2. 종속성 격리 수준 비교

| 격리 수준 | 기술 | 격리 범위 | 오버헤드 | 보안 수준 |
| :--- | :--- | :--- | :--- | :--- |
| **없음** | 시스템 전역 설치 | 없음 | 낮음 | 취약 |
| **가상 환경** | venv, conda | Python 패키지 | 낮음 | 중간 |
| **컨테이너** | Docker | OS 전체 | 중간 | 높음 |
| **마이크로VM** | gVisor, Kata | 하드웨어 | 높음 | 매우 높음 |

### 3. 과목 융합 관점 분석

**종속성 + 보안 (SCA/SSC)**
- SCA(Software Composition Analysis) 도구가 종속성의 알려진 취약점(CVE)을 스캔합니다.
- SBOM(Software Bill of Materials) 생성으로 공급망 투명성 확보합니다.

**종속성 + CI/CD**
- CI 파이프라인에서 종속성 캐싱으로 빌드 시간을 단축합니다.
- Dependabot/Renovate가 자동으로 종속성 업데이트 PR을 생성합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 전이적 종속성 버전 충돌**
- **문제점**: 앱이 A(→ B@1.0)와 C(→ B@2.0)에 의존하는데, B의 1.0과 2.0이 호환되지 않음.
- **기술사 판단**: **종속성 해결 전략 수립**
  1. A 또는 C의 버전을 조정하여 호환되는 B 버전을 찾음.
  2. 불가능하면 A 또는 C를 대체 라이브러리로 교체.
  3. 최후의 수단으로 fork하여 패치.

**[상황 B] 취약점이 발견된 종속성 긴급 패치**
- **문제점**: Log4j 취약점이 발견되어 수백 개의 서비스에 긴급 패치 필요.
- **기술사 판단**: **자동화된 취약점 스캔 및 업데이트 파이프라인**
  1. SCA 도구(Trivy, Snyk)가 취약점 탐지.
  2. 자동으로 업데이트 PR 생성(Renovate).
  3. CI 테스트 통과 시 자동 머지 및 배포.

### 2. 종속성 관리 체크리스트

**선언 체크리스트**
- [ ] 모든 종속성이 Manifest 파일에 명시되어 있는가?
- [ ] 버전 범위가 적절한가? (너무 유연하지 않은가?)
- [ ] devDependencies와 dependencies가 구분되어 있는가?

**격리 체크리스트**
- [ ] 가상 환경 또는 컨테이너가 사용되고 있는가?
- [ ] 시스템 전역 패키지에 의존하고 있지 않은가?
- [ ] CI/CD에서 동일한 격리 환경이 사용되는가?

**보안 체크리스트**
- [ ] Lock 파일이 버전 관리되고 있는가?
- [ ] 취약점 스캔이 CI에 통합되어 있는가?
- [ ] 프라이빗 레지스트리가 사용되고 있는가?

### 3. 안티패턴 (Anti-patterns)

**안티패턴 1: 시스템 전역 설치**
- `sudo pip install package`로 시스템 전역에 설치.
- **문제**: 다른 앱과 충돌, 재현 불가, 보안 위험.
- **해결**: 항상 가상 환경 또는 컨테이너 사용.

**안티패턴 2: Lock 파일 무시**
- `package-lock.json`을 .gitignore에 추가.
- **문제**: 개발자마다 다른 버전 설치, "Works on My Machine".
- **해결**: Lock 파일을 커밋하고 `npm ci` 사용.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 (AS-IS) | 도입 후 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **빌드 재현성** | 50% (환경마다 다름) | 99.9% | **2배 향상** |
| **종속성 충돌** | 월 5회 이상 | 연 0회 | **100% 감소** |
| **취약점 대응 시간** | 수주 (수동 파악) | 수시간 (자동 스캔) | **100배 단축** |
| **온보딩 시간** | 2일 (환경 설정) | 30분 (자동화) | **90% 단축** |

### 2. 미래 전망 및 진화 방향

**SBOM 의무화**
- 미국 행정명령 14028로 연방 조달 시 SBOM 제출 의무화.
- CycloneDX, SPDX가 산업 표준으로 자리잡음.

**AI 기반 종속성 관리**
- AI가 종속성 업그레이드 호환성을 자동 분석.
- 취약점 패치 코드를 자동 생성.

### 3. 참고 표준/가이드
- **12-Factor App**: 종속성 격리 원칙
- **Semantic Versioning**: 버전 번호 표준
- **CycloneDX/SPDX**: SBOM 표준 포맷
- **SLSA (Supply-chain Levels for Software Artifacts)**: 공급망 보안 프레임워크

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **[12-Factor App](@/studynotes/15_devops_sre/01_sre/twelve_factor_app.md)**: 종속성 격리 원칙을 포함한 클라우드 네이티브 방법론
- **[코드베이스 관리](./codebase_management.md)**: 종속성 선언을 포함하는 전체 코드 관리 체계
- **[DevSecOps](@/studynotes/15_devops_sre/01_sre/devsecops.md)**: 종속성 보안 스캔을 포함한 보안 통합
- **[CI/CD 파이프라인](@/studynotes/15_devops_sre/03_automation/cicd_gitops.md)**: 종속성 캐싱 및 자동화된 빌드

---

## 👶 어린이를 위한 3줄 비유 설명
1. 종속성 격리는 **'각자의 도시락'**을 싸는 것과 같아요. 친구들이랑 소풍을 가는데, 모두 **'자기만의 도시락'**을 가져가죠.
2. 한 친구가 **'단무지가 싫어요'**라고 해도, 다른 친구의 도시락에는 단무지가 들어있을 수 있어요. 서로 섞이지 않으니까요!
3. 이렇게 하면 누가 **'김치를 싫어한다'**고 해도 다른 사람의 김밥 맛이 이상해지지 않아요. 각자 자기 도시락만 먹으면 되니까요!
