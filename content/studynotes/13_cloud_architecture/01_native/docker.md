+++
title = "도커 (Docker)"
date = 2024-05-12
description = "컨테이너 기술을 대중화한 오픈소스 플랫폼으로, 컨테이너 이미지 빌드, 배포, 실행을 위한 도구 체계(Dockerfile, Docker Engine, Docker Hub)를 제공"
weight = 85
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Docker", "Container", "Dockerfile", "Docker Hub", "Docker Engine", "Image"]
+++

# 도커 (Docker) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 컨테이너 생성, 배포, 실행을 위한 오픈소스 플랫폼으로, Dockerfile로 이미지를 정의하고, Docker Engine이 컨테이너를 실행하며, Docker Hub로 이미지를 공유하는 **'컨테이너 생태계의 표준'**입니다.
> 2. **가치**: "Build once, Run anywhere"를 실현하여 개발/테스트/운영 환경 불일치 문제를 해결했으며, CI/CD 파이프라인과 마이크로서비스의 핵심 기반이 되었습니다.
> 3. **융합**: Docker Desktop으로 개발 환경을 통합하고, Docker Compose로 멀티 컨테이너를 정의하며, Kubernetes와 연동하여 프로덕션 오케스트레이션을 수행합니다.

---

## Ⅰ. 개요 (Context & Background)

Docker는 2013년 Solomon Hykes가 dotCloud(현 Docker Inc.)에서 발표한 오픈소스 컨테이너 플랫폼입니다. 기존 LXC(Linux Containers)를 기반으로 하되, 사용자 친화적인 CLI, 이미지 포맷 표준화, Docker Hub를 통한 이미지 공유, 레이어드 파일시스템 등을 도입하여 컨테이너 기술을 대중화했습니다.

**💡 비유**: Docker는 **'앱스토어 + 앱 실행기'**와 같습니다. Docker Hub(앱스토어)에서 원하는 앱 이미지를 내려받고(pull), Docker(실행기)로 바로 실행(run)합니다. 개발자는 내 앱을 Dockerfile로 만들어 Docker Hub에 올리고(push), 누구든지 어디서든 같은 환경에서 실행할 수 있습니다.

**등장 배경 및 발전 과정**:
1. **"Works on my machine" 문제**: 개발 환경과 운영 환경의 차이로 인한 장애가 빈번했습니다.
2. **VM의 무거움**: VM은 배포 단위가 너무 크고, 시작이 느려 마이크로서비스에 부적합했습니다.
3. **Docker의 폭발적 성장 (2013~)**: "Build, Ship, Run"이라는 단순한 철학과 사용자 친화적 도구로 폭발적으로 채택되었습니다.
4. **OCI 표준화 (2015~)**: Docker가 이미지 포맷과 런타임을 OCI(Open Container Initiative)에 기부하여 산업 표준이 되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Docker 아키텍처 구성 요소

| 구성 요소 | 상세 역할 | 내부 동작 | 비유 |
|---|---|---|---|
| **Docker Client** | 사용자 CLI/GUI | dockerd와 REST API 통신 | 리모컨 |
| **Docker Daemon (dockerd)** | 이미지/컨테이너 관리 | containerd, runc 호출 | 관리자 |
| **containerd** | 컨테이너 생명주기 관리 | OCI 런타임 관리 | 실행기 |
| **runc** | 저수준 컨테이너 실행 | namespace, cgroups 생성 | 엔진 |
| **Docker Image** | 불변 실행 패키지 | 레이어드 파일시스템 | 설치 CD |
| **Docker Container** | 실행 중인 이미지 인스턴스 | 격리된 프로세스 | 실행된 앱 |
| **Docker Registry** | 이미지 저장소 | push/pull API | 앱스토어 |

### 정교한 구조 다이어그램

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                        [ Docker Architecture ]                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          [ Docker Client ]                                  │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │   $ docker build -t myapp .                                          │  │
│  │   $ docker run -d -p 80:80 myapp                                     │  │
│  │   $ docker push myrepo/myapp:v1.0                                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │ REST API over Unix Socket / TCP
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          [ Docker Host ]                                    │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                       Docker Daemon (dockerd)                         │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │  │
│  │  │   Image     │  │  Container  │  │  Network    │  │  Volume     │ │  │
│  │  │  Manager    │  │  Manager    │  │  Manager    │  │  Manager    │ │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │  │
│  └───────────────────────────────┬──────────────────────────────────────┘  │
│                                  │ gRPC                                    │
│  ┌───────────────────────────────▼──────────────────────────────────────┐  │
│  │                          containerd                                   │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │  │
│  │  │    Image    │  │  Container  │  │     CRI     │                  │  │
│  │  │   Store     │  │  Supervisor │  │  (K8s API)  │                  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                  │  │
│  └───────────────────────────────┬──────────────────────────────────────┘  │
│                                  │                                         │
│  ┌───────────────────────────────▼──────────────────────────────────────┐  │
│  │                             runc                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────┐    │  │
│  │  │  libcontainer: Namespace + Cgroups + UnionFS + Seccomp      │    │  │
│  │  └─────────────────────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      Container Instances                             │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │  │
│  │  │ Container 1 │  │ Container 2 │  │ Container 3 │  │ Container N │ │  │
│  │  │   (nginx)   │  │   (redis)   │  │  (postgres) │  │   (myapp)   │ │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ push/pull
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        [ Docker Registry ]                                  │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │  │
│  │  │ Docker Hub  │  │  AWS ECR    │  │ Harbor      │  │ Private     │ │  │
│  │  │ (Public)    │  │  (Managed)  │  │ (Enterprise)│  │ Registry    │ │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: 레이어드 파일시스템 (UnionFS)

```
┌────────────────────────────────────────────────────────────────────────────┐
│                  Docker Image Layers (Union Filesystem)                    │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ Docker Image 구조 ]                                                     │
│                                                                            │
│      ┌────────────────────────────────────────┐                           │
│      │  Layer 5: Application Code (Top)       │  ← Read/Write (Container) │
│      │  - app.py, config.json                 │                           │
│      │  - Size: 1MB                           │                           │
│      ├────────────────────────────────────────┤                           │
│      │  Layer 4: Python Dependencies          │  ← Read Only (Image)      │
│      │  - pip install flask, gunicorn         │                           │
│      │  - Size: 50MB                          │                           │
│      ├────────────────────────────────────────┤                           │
│      │  Layer 3: Python Runtime               │  ← Read Only (Image)      │
│      │  - python3.11, pip                     │                           │
│      │  - Size: 100MB                         │                           │
│      ├────────────────────────────────────────┤                           │
│      │  Layer 2: OS Packages                  │  ← Read Only (Image)      │
│      │  - apt packages, certificates          │                           │
│      │  - Size: 30MB                          │                           │
│      ├────────────────────────────────────────┤                           │
│      │  Layer 1: Base OS (alpine:3.18)        │  ← Read Only (Image)      │
│      │  - Alpine Linux filesystem             │                           │
│      │  - Size: 5MB                           │                           │
│      └────────────────────────────────────────┘                           │
│                                                                            │
│  [ Copy-on-Write (CoW) 메커니즘 ]                                          │
│                                                                            │
│  - 읽기: 각 레이어에서 직접 읽음 (스택 구조)                                 │
│  - 쓰기: 최상위 Container Layer에 복사 후 수정                              │
│  - 장점: 중복 제거, 빠른 빌드, 작은 이미지 크기                             │
│                                                                            │
│  $ docker history myapp:v1.0                                               │
│  IMAGE          CREATED        SIZE                                        │
│  abc123         1 min ago      1MB    ← Application Code                  │
│  def456         1 hour ago     50MB   ← Dependencies                      │
│  ghi789         2 days ago     100MB  ← Python Runtime                    │
│  jkl012         1 week ago     5MB    ← Alpine Base                       │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: Dockerfile Best Practices

```dockerfile
# ============================================================
# Dockerfile - Production-Ready Python Application
# ============================================================

# 1. 특정 버전의 베이스 이미지 사용 (latest 금지)
FROM python:3.11-slim-bookworm AS builder

# 2. 빌드 인자 정의
ARG APP_VERSION=1.0.0
ARG BUILD_DATE

# 3. 메타데이터 추가 (OCI 표준)
LABEL org.opencontainers.image.title="BrainScience API" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.authors="dev@brainscience.com"

# 4. 환경 변수 설정 (Python 최적화)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 5. 작업 디렉토리 생성
WORKDIR /app

# 6. 의존성 파일 먼저 복사 (캐시 최적화)
COPY requirements.txt .

# 7. 가상환경 생성 및 의존성 설치
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# ============================================================
# Production Stage (Multi-stage Build)
# ============================================================
FROM python:3.11-slim-bookworm

# 8. 보안: 비루트 사용자 생성
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -d /app -s /sbin/nologin -c "App user" appuser

# 9. 필요한 시스템 패키지만 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 10. 가상환경 복사
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 11. 애플리케이션 코드 복사 (소유권 변경)
COPY --chown=appuser:appgroup . .

# 12. 보안 설정
RUN chmod -R 755 /app && \
    # 민감한 파일 제거
    rm -rf /app/.git /app/.env* /app/tests

# 13. 비루트 사용자로 전환
USER appuser

# 14. 포트 노출
EXPOSE 8000

# 15. 헬스체크
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 16. 시작 명령 (exec form)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
```

```yaml
# docker-compose.yml - 멀티 컨테이너 정의
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        APP_VERSION: ${APP_VERSION:-1.0.0}
    image: brainscience/api:${APP_VERSION:-latest}
    container_name: api-server
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    networks:
      - backend

  db:
    image: postgres:15-alpine
    container_name: postgres-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

  cache:
    image: redis:7-alpine
    container_name: redis-cache
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redisdata:/data
    networks:
      - backend

volumes:
  pgdata:
  redisdata:

networks:
  backend:
    driver: bridge
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Docker vs Podman

| 비교 관점 | Docker | Podman | 상세 분석 |
|---|---|---|---|
| **아키텍처** | Daemon (dockerd) | Daemonless | Podman은 rootless 실행 가능 |
| **보안** | root 필요 (기본) | Rootless 가능 | Podman이 보안상 유리 |
| **K8s 호환** | dockershim (deprecated) | CRI-O | Podman이 K8s 네이티브 |
| **CLI 호환** | docker | podman (alias 가능) | 거의 동일 |
| **Compose** | docker-compose | podman-compose | 유사 |

### 과목 융합 관점 분석

**DevOps와의 융합**:
- Docker는 CI/CD 파이플라인의 핵심 요소입니다. Jenkins/GitLab CI/GitHub Actions가 Docker 이미지를 빌드하고 레지스트리에 푸시합니다.
- Docker Multi-stage Build로 빌드 환경과 런타임 환경을 분리하여 이미지 크기를 최소화합니다.

**보안(Security)과의 융합**:
- Docker Content Trust로 이미지 서명 검증
- Docker Scout/Trivy로 이미지 취약점 스캔
- Docker Secrets로 민감 정보 관리

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: Docker 이미지 최적화

**문제 상홡**: Python 애플리케이션 Docker 이미지가 1.2GB로 너무 큽니다.

**기술사의 전략적 의사결정**:
1. **Base Image 변경**: python:3.11 (1GB) → python:3.11-slim (150MB) → python:3.11-alpine (50MB)
2. **Multi-stage Build**: 빌드 도구를 런타임에서 제거
3. **Layer 최소화**: RUN 명령어 병합
4. **distroless 고려**: Google distroless/python3 (20MB)

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - .dockerignore 미사용**: 불필요한 파일이 이미지에 포함되어 크기 증가 및 보안 리스크.
- **체크리스트**:
  - [ ] 특정 버전 Base Image 사용 (latest 금지)
  - [ ] .dockerignore 파일 작성
  - [ ] Multi-stage Build 적용
  - [ ] Non-root 사용자 실행
  - [ ] 이미지 취약점 스캔 자동화

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | VM 배포 | Docker 배포 | 개선율 |
|---|---|---|---|
| **배포 시간** | 30분 | 30초 | 98% 단축 |
| **이미지 크기** | 10GB | 100MB | 99% 축소 |
| **환경 일관성** | 낮음 | 높음 | 향상 |

### 미래 전망 및 진화 방향

- **BuildKit**: 차세대 이미지 빌더로 병렬 빌드, 향상된 캐싱 제공
- **Docker Desktop替代**: Rancher Desktop, Colima 등 오픈소스 대안 부상
- **WebAssembly (Wasm)**: 컨테이너보다 더 가벼운 실행 환경

### ※ 참고 표준/가이드
- **OCI Image Spec**: 이미지 포맷 표준
- **Dockerfile Reference**: 공식 문서
- **CIS Docker Benchmark**: 보안 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [컨테이너 (Container)](@/studynotes/13_cloud_architecture/01_native/container.md) : Docker가 실행하는 기술
- [Kubernetes](@/studynotes/13_cloud_architecture/01_native/kubernetes.md) : Docker 컨테이너 오케스트레이션
- [Docker Compose](@/studynotes/13_cloud_architecture/01_native/docker_compose.md) : 멀티 컨테이너 정의
- [OCI](@/studynotes/13_cloud_architecture/01_native/oci.md) : Docker가 기여한 표준
- [컨테이너 레지스트리](@/studynotes/13_cloud_architecture/01_native/container_registry.md) : Docker Hub 등

---

### 👶 어린이를 위한 3줄 비유 설명
1. Docker는 **'앱스토어 + 앱 실행기'**예요. 앱스토어(Docker Hub)에서 게임을 다운받고, 실행기(Docker)로 바로 실행해요.
2. 개발자는 **'설치 CD(Dockerfile)'**만 만들면 돼요. 그러면 누구든지 같은 게임을 똑같이 실행할 수 있어요.
3. 그리고 이 CD는 **'아주 작고 가벼워요'**. 왜냐하면 컴퓨터(OS) 전체가 아니라 게임만 들어있거든요!
