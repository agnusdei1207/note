+++
weight = 884
title = "84. 컨테이너 런타임 (Container Runtime)"
description = "Container Runtime: 쿠버네티스 파드 내 컨테이너를 실제 생성, 실행, 관리하는 저수준 런타임 엔진"
date = 2026-03-26

[taxonomies]
tags = ["kubernetes", "k8s", "container-runtime", "containerd", "cri-o", "cri", "docker"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 컨테이너 런타임은 쿠버네티스 파드 내 컨테이너를 실제로 생성하고 실행하는"작업자"이다. Kubelet이 CRI(Container Runtime Interface) 명령을 내리면, 런타임이 이미지를 풀하고, 컨테이너를 시작하며, 네임스페이스와 cgroups를 설정하는 저수준 작업을 수행한다.
> 2. **가치**: 컨테이너 런타임이 있음으로써 개발자는"어떤 컨테이너 기술을 쓰느냐"에 관계없이 동일한 인터페이스로 쿠버네티스에서 애플리케이션을部署할 수 있다. 이는 Docker, containerd, CRI-O 등 런타임 간の相互運用性を обеспечивает.
> 3. **융합**: OCI(Open Container Initiative) 런타임-spec을 준수하여, 서로 다른 런타임 간에도 컨테이너 이미지의相互運用が确保되었다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념 정의

컨테이너 런타임은 쿠버네티스 아키텍처의 가장底层에位置する"실제 작업자"이다. 마스터의 명령이 Kubelet → Kube-proxy → Container Runtime의 경로를 타고 내려오고, Container Runtime이 최종적으로 컨테이너를 실행한다. 컨테이너 런타임은 다음 작업을 수행한다. 첫째,"이미지 풀"으로 컨테이너 이미지를 레지스트리에서 다운로드한다. 둘째,"컨테이너 생성"으로 파일 시스템, 네임스페이스, cgroups 등을 설정한다. 셋째,"컨테이너 시작"으로 프로세스를 실행한다. 넷째,"컨테이너 관리"로 중지, 삭제, 상태 조회 등을 처리한다.

### 왜 런타임 추상화가 중요한가?

쿠버네티스 1.24 이전에는 Docker가 기본 컨테이너 런타임이었다. 그러나 Docker는 원래 쿠버네티스를 위해 설계된 것이 아니라서, Kubelet이 Docker의 특화된 기능을 사용하기 위해 내부적으로 많은 어댑터 코드를 필요로 했다. CRI(Container Runtime Interface)의 도입으로 Kubelet과 런타임 사이의 계약이 명확해졌고, containerd, CRI-O, frakti 등 다양한 런타임이 동일한 인터페이스로 연동될 수 있게 되었다. 이는"구현 분리"의 좋은 예시로, 인터페이스만 맞으면 어떤 런타임으로도 교체 가능하다.

### 비유

컨테이너 런타임을"식당厨房의 조리사"에 비유할 수 있다. 셰프(Kubelet)가"비프 스테이크 만들어줘"라고 명령하면, 조리사(Container Runtime)가 재료를 찾고(Image Pull), 조리 도구를 준비하고(네임스페이스 설정), 그래ills/bin에 올려 조리한다(컨테이너 실행). 조리사가 없으면 셰프의命令は谁来执行都无法确定. 또한 조리사가 바뀌어도(런타임 교체) 비프 스테이크라는 결과물은 동일하다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### CRI (Container Runtime Interface)

CRI는 Kubelet과 Container Runtime 사이의通信を標準化する gRPC API이다. CRI 이전에는 Kubelet이 Docker Engine의 특화된 API를 직접 호출하여 Docker에 강하게 결합되어 있었다. CRI 도입으로 Kubelet은 런타임의구체적 구현细节을몰라도 되고, 런타임도 Kubelet의内部構造を 몰라도 된다. CRI의 주요 서비스는 "RuntimeService"와 "ImageService"로 나뉜다. RuntimeService는 컨테이너 lifecycle 관리(생성, 시작, 중지, 삭제, 상태 조회)를, ImageService는 이미지 관리(풀, 리스트, 삭제)를 담당한다.

### containerd 아키텍처

containerd는 도커(Docker)로부터 추출된 경량 컨테이너 런타임이다. Docker의 모든 기능 중에서 쿠버네티스需要的"컨테이너 실행"에 필요한 핵심 기능만 남겼다. containerd는 그 자체로 gRPC 서버로서 CRI 요청을 listen하고, 이를进一步 처리하기 위해 하위의 shim ( runtime-shim)과通信한다. shim은 컨테이너의 STDIN/STDOUT을 관리하고, containerd가 종료되어도 컨테이너가 계속 실행되도록 한다.

```
[ containerd 아키텍처 ]

┌─────────────────────────────────────────────────────────────────────────┐
│                      containerd分层 구조                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                         CRI API (gRPC)                           │  │
│  │  • RuntimeService: 컨테이너 lifecycle                             │  │
│  │  • ImageService: 이미지 관리                                       │  │
│  │  • 사용 포트: /run/containerd/containerd.sock                      │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│                              ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                      containerd daemon (데몬)                        │  │
│  │  • 메타데이터 관리 (bolt DB)                                        │  │
│  │  • 볼륨 관리                                                        │  │
│  │  • 네트워크 (CNI 연동)                                              │  │
│  │  • 이벤트/메트릭 수집                                               │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│              ┌───────────────┴───────────────┐                        │
│              │                               │                        │
│              ▼                               ▼                        │
│  ┌─────────────────────────┐     ┌─────────────────────────┐           │
│  │   containerd-shim      │     │   containerd-shim       │           │
│  │   (runsc for runc)     │     │   (runc)               │           │
│  │   sandboxed container  │     │   regular container     │           │
│  └─────────────────────────┘     └─────────────────────────┘           │
│              │                               │                        │
│              └───────────────┬───────────────┘                        │
│                              ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                     OCI Runtime (runc, runsc, kata-runtime 등)       │  │
│  │  • 컨테이너 프로세스 실제 실행                                        │  │
│  │  • 네임스페이스 격리 설정                                            │  │
│  │  • cgroups 리소스 제한 적용                                          │  │
│  │  • root filesystem 마운트                                            │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** containerd의 3단계 구조를 이해하면 런타임의 동작 원리가 명확해진다. 최상단의 CRI API가 Kubelet의 요청을 수신하고, containerd daemon이 전체를 조율한다. shim은 containerd와 OCI 런타임 사이의中介자 역할을 하며, containerd가 재시작되어도 shim이存活하기 때문에 실행 중인 컨테이너가 계속된다. OCI 런타임(runc)이 실제 프로세스를 생성하고 네임스페이스/Cgroups를 설정하는"실제 작업자"이다.

### OCI (Open Container Initiative) 표준

OCI는 컨테이너 이미지 포맷과 런타임에 대한 업계 표준이다. OCI에는 두 가지 주요 명세가 있다. **runtime-spec**은 컨테이너의 실행 방법(프로세스 격리, 리소스 제한, 파일시스템 마운트 등)을定義한다. **image-spec**은 컨테이너 이미지의 구조(레이어, 매니페스트, 설정 메타데이터)를 정의한다. OCI 표준을 준수하는 한, OCI 이미지 어디에서든 컨테이너를 실행할 수 있다. 이는"이미지는 표준化되고, 런타임도 표준化되어, 그 사이의組合自由"的設計이다.

### 런타임의 종류

**runc**는 OCI 런타임의参照実装으로, libcontainer를 기반으로 한命令行 도구이다. 대부분의 containerd와 CRI-O의 내부에서 실제 컨테이너 실행에 사용된다. **containerd**는 도커에서 추출된高水平 런타임으로, CRI를実装하고 shim을管理한다. **CRI-O**는 OCI-compliant 컨테이너를 실행하기 위해 Kubelet용으로 설계된轻量级 런타임으로, Docker에 대한 의존성을 完全에 제거한다. **gVisor**와 **Kata Containers**는 보안이 강화된 런타임으로, 호스트 커널과 컨테이너 사이의隔离을強化한다.

### 섹션 비유

OCI 표준을"국제 영어 교육 과정"에 비유할 수 있다. 영어 공부는"이미지 스펙"에 해당하고, 영어로 의사소통하는 능력은"runtime-spec"에 해당한다. 공부를 잘한 사람(OCI-compliant image)은 영국인( containerd), 미국인(CRI-O), 호주인(gVisor) 누구와도 영어로 대화할 수 있다. 이는"표준화된 입력 → 다양한 구현"의 관계로, Docker 이미지가 containerd와 CRI-O 양쪽에서 실행 가능한 이유를 설명한다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### containerd vs CRI-O vs Docker

| 비교 항목 | containerd | CRI-O | Docker |
|:---|:---|:---|:---|
| **기원** | Docker에서 추출 | Red Hat 주도 | 원조 컨테이너 플랫폼 |
| **CRI 지원** | 네 (기본) | 네 (전용) | 별도 어댑터 필요 |
| **依赖성** | 도커 CLI 없음 | OCI 표준만 | 전체 Docker Engine |
| **메모리 사용량** | ~50MB | ~40MB | ~200MB |
| **주요 사용자** | 대부분의 Kubernetes | Red Hat 기반 환경 | 개발 환경 |

### Kata Containers와 gVisor: 세이프 런타임

일반 런타임(runc)은 호스트 커널을 공유하기 때문에"컨테이너 탈출(Container Escape)" 취약점이 있을 경우 호스트 전체에 영향이 갈 수 있다. Kata Containers는 각 컨테이너를 경량 VM(MicroVM)으로 실행하여 하드웨어 수준의 격리를 제공하고, gVisor는 사용자 공간 커널(gVisor Kernel)을 사용하여 시스템 콜을中介한다. 이러한"세이프 런타임"은 높은 보안이要求される 환경(멀티 테넌시 등)에서 사용된다.

### 런타임 선택 기준

| 상황 | 권장 런타임 |
|:---|:---|
| 일반 프로덕션 환경 | containerd |
| 규제/금융 환경 | CRI-O 또는 Kata Containers |
| 개발/테스트 환경 | Docker (cri-dockerd) |
| 높은 격리 필요 (멀티 테넌시) | Kata Containers |
| 빠른 컨테이너 시작 필요 | gVisor (선택적) |

### 섹션 비유

런타임 선택은"보안等級別の 출입문"에 비유할 수 있다. 일반 출입문(runc)은 대부분の人에 허용되며 효율적이지만,万一 위험物을を持ち込もうと하면 조치 곤란하다.Kata Containers는 металлоиска기门的 Littleg VM，相当于机场的全身检查，而 gVisor 则使用代理 Kernel，相当于医院的无菌操作台。 모두"컨테이너를 실행한다"는 목적은 동일하지만, 보안等级과 성능之间有权衡。

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### containerd 설정

 containerd를 사용하려면 containerd 설정을編集하고, Kubelet의 "--container-runtime-endpoint"를 "/run/containerd/containerd.sock"으로 설정한다. containerd 설정 파일은 통상 "/etc/containerd/config.toml"에 위치하며, 다음 항목을 설정할 수 있다. **sandbox_image**는 인프라 컨테이너(pause) 이미지를 지정하고, **registry**는 미러 레지스트리 접속 정보를 설정하며, **storage_driver**는 컨테이너 파일시스템 드라이버를 지정한다.

### 이미지 풀 정책

 컨테이너 이미지는pullPolicy를 통해 언제 풀할지 설정할 수 있다. **Always**는 항상 최신 이미지를 풀하고, **IfNotPresent**는ローカルに이미지가 없으면 풀하고, **Never**는絶対に 풀하지 않고ローカル画像を사용한다. 프로덕션에서는通常 IfNotPresent를使用し、定期적(예: 주 1회)으로 새 이미지를풀하여更新を適用한다.

### 런타임 클래스

 RuntimeClass를使用하면復数の コンテナ 런타임을クラスタ内で混在 사용할 수 있다. 예를 들어, 일반 워크로드에는 containerd를 사용하고, 높은 보안이 필요한 워크로드에는 Kata Containers를 사용할 수 있다. 파드의 spec.runtimeClassName에 KataContainers를指定하면 해당 파드는 Kata 런타임으로 실행된다.

### 섹션 비유

이미지 풀 정책은"음식 재료 조달 방식"에 비유할 수 있다. Always는"고철마다 신선한 재료를 배달시키다"로 항상 새로운 이미지를 가져오므로 네트워크 부하가 크다. IfNotPresent는"창고에 있으면 사용하고, 없으면 배달시키다"로 불필요한 네트워크 부하를 줄인다. Never는"창고에만 있다"로 네트워크가 끊겨도 실행 가능하지만, 이미지가 오래될 위험이 있다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대 효과

올바른 컨테이너 런타임 선택과 설정은 클러스터 성능과 안정성에 직접적 영향을 미친다. containerd는 대부분의 환경에서 적합하며, CRI-O는 더 엄격한 OCI 준수가 필요하거나 Red Hat 기반 환경에서 유리하다. Kata Containers나 gVisor는 높은 보안이 要求되는 환경에서 추가적인 격리를 제공한다.

### 핵심 정리

컨테이너 런타임은 쿠버네티스 아키텍처的最底层에서"실제 컨테이너를 실행하는 작업자"이다. CRI를 통해 Kubelet과 통신하고, OCI 표준을 준수하여 서로 다른 런타임 간 상호운용성을 보장한다. containerd는 경량이고 범용적이며, CRI-O는 더 엄격한 표준 준수를, Kata/gVisor는 더 높은 보안을 제공한다.

### 섹션 비유

컨테이너 런타임은"공장 생산라인의機械"에 비유할 수 있다. 어떤 공장(컨테이너 런타임)을 선택하든 똑같은 제품(컨테이너)을 만들 수 있지만, 기계의 종류( containerd vs CRI-O)에 따라 생산 속도, 유지보수 난이도, 안전장치 수준 등이 달라진다. 공장 관리자는 제품 요구사항과 환경 조건을 고려하여 적절한 기계를 선택한다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **CRI (Container Runtime Interface)** | Kubelet과 Container Runtime 사이의 gRPC API로, 런타임 추상화를 가능하게 한다. |
| **OCI (Open Container Initiative)** | 컨테이너 이미지 포맷과 런타임의 업계 표준 규격이다. |
| **containerd** | Docker에서 추출된 경량 컨테이너 런타임으로, CRI를実装하고 shim을관리한다. |
| **CRI-O** | Kubernetes 전용으로 설계된 OCI-compliant 런타임이다. |
| **runc** | OCI 런타임 참조 구현으로, 실제 컨테이너 프로세스를 생성하고 격리를 설정한다. |
| **containerd-shim** | containerd와 OCI 런타임 사이의 중개자로, containerd 재시작 시 컨테이너 실행을 유지한다. |
| **RuntimeClass** | 클러스터 내에서 다양한 런타임을 사용하고 파드별로 선택할 수 있게 하는 쿠버네티스 기능이다. |
