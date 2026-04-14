+++
weight = 144
title = "서비스 메시 (Service Mesh)"
date = "2026-03-04"
[extra]
categories = "studynote-cloud"
+++

## 핵심 인사이트 (3줄 요약)
- **인프라 계층의 통신 제어:** 마이크로서비스 간 통신(East-West)을 제어하기 위해 비즈니스 로직과 분리된 인프라 네트워크 계층이다.
- **사이드카 프록시 기반:** 각 서비스 옆에 부착된 사이드카(Proxy)가 라우팅, 보안, 로깅, 서킷 브레이커 등을 대행 처리한다.
- **가시성 및 보안 강화:** 복잡한 서비스 간 흐름을 시각화하고, mTLS(상호 TLS)를 통해 제로 트러스트 보안을 자동 구현한다.

### Ⅰ. 개요 (Context & Background)
- 마이크로서비스의 개수가 수백 개로 늘어나면 개별 서비스 코드에 통신 로직(재시도, 타임아웃, 보안)을 넣는 것이 불가능해진다. 서비스 메시는 이러한 공통 기능을 인프라단으로 격리하여 개발자의 부담을 줄여준다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
[ Control Plane ] <--- (Policy / Config) --- [ Management UI ]
        |
        +-------------------------------------------+
        |                                           |
[ Data Plane: Pod ]                       [ Data Plane: Pod ]
+---------------+                         +---------------+
| Application   | <--- (Localhost) --->   | Application   |
+---------------+                         +---------------+
| Proxy (Envoy) | <--- (mTLS / Mesh) ---> | Proxy (Envoy) |
+---------------+                         +---------------+

<Bilingual ASCII Diagram: 서비스 메시 아키텍처 / Service Mesh Architecture>
```

- **핵심 컴포넌트:**
  1. **Data Plane:** 실제 트래픽을 처리하는 프록시(Envoy 등)들의 집합
  2. **Control Plane:** 프록시들에게 정책과 설정을 전달하는 제어 센터(Istiod 등)
- **주요 기능:** 트래픽 관리(Canary, Blue-Green), 보안(mTLS), 가시성(Tracing, Metrics)

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구분 | API 게이트웨이 (North-South) | 서비스 메시 (East-West) |
| :--- | :--- | :--- |
| **위치** | 클라이언트와 서버 사이 | 서버(서비스) 간 사이 |
| **주요 역할** | 인증, 인가, 외부 진입점 제어 | 로드밸런싱, 통신 보안, 복구력 |
| **관리 범위** | 서비스 전체의 외각 경계 | 개별 마이크로서비스 간 통신망 |
| **대표 기술** | Kong, AWS API GW, Zuul | Istio, Linkerd, Consul |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **도입 기준:** 마이크로서비스 개수가 관리 한계를 넘어서거나, 고도의 보안(mTLS) 및 트래픽 제어가 필요할 때 도입한다.
- **기술사적 판단:** 서비스 메시는 상당한 리소스 오버헤드(Sidecar 점유)를 수반하므로, 시스템 규모와 복잡도를 고려한 'TCO 분석'이 선행되어야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- 쿠버네티스 생태계의 사실상 표준(De facto) 통신 플랫폼으로 자리 잡고 있다. 향후 eBPF 기술을 활용한 'Sidecar-less' 모델로 진화하여 성능 오버헤드를 줄이는 방향으로 발전할 전망이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- MSA -> Service Mesh -> (Istio, Linkerd) -> Sidecar Proxy -> mTLS -> Zero Trust

### 👶 어린이를 위한 3줄 비유 설명
- **서비스 메시**는 수많은 장난감 로봇들이 서로 편지를 주고받을 때 쓰는 "마법의 우체통"과 같아요.
- 로봇 옆에 하나씩 붙어서 "편지가 잘 갔는지", "나쁜 사람이 훔쳐보지 않는지" 대신 확인해 주는 비서 같은 친구예요.
- 덕분에 로봇들은 편지 보낼 걱정 없이 자기가 맡은 놀이만 열심히 할 수 있답니다.
