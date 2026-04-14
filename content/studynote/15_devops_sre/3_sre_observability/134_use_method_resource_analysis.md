+++
weight = 134
title = "USE 메서드 (USE Method: Resource Analysis)"
date = "2024-03-23"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
- USE 메서드는 인프라 자원(CPU, Disk, Memory)의 성능 문제를 분석하기 위해 활용도(Utilization), 포화도(Saturation), 에러(Errors) 세 가지 지표를 체크하는 방법론이다.
- Brendan Gregg에 의해 고안되었으며, 복잡한 시스템 장애 시 분석 대상을 인프라 계층으로 한정하여 병목의 근본 원인을 빠르게 식별하도록 돕는다.
- "모든 자원에 대해 Utilization, Saturation, Errors를 확인하라"는 명확한 체크리스트를 제공하여 초보 엔지니어도 체계적인 문제 해결이 가능하다.

### Ⅰ. 개요 (Context & Background)
서버가 느려졌을 때 어디서부터 시작해야 할지 모르는 막막함을 해결하기 위해 등장한 것이 **USE 메서드**다. 이는 철저하게 '하드웨어 자원'의 관점에서 접근한다. 시스템을 구성하는 각각의 컴포넌트(CPU, 메모리, 디스크, 네트워크, 버스 등)를 독립된 자원으로 보고, 이들이 얼마나 바쁜지(U), 대기열이 쌓였는지(S), 고장 났는지(E)를 묻는 과정이다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
USE 메서드는 시스템의 모든 물리적/논리적 자원을 전수 조사하는 하향식(Top-down) 분석 기법이다.

```text
[ USE Method Concept: Resource Centric ]
(USE 메서드 개념: 자원 중심 분석)

      +-----------------------------------------+
      |  System Component (e.g., CPU, Disk)     |
      +--------------------+--------------------+
                           |
           +---------------+---------------+
           |                               |
    [1] Utilization      [2] Saturation     [3] Errors
    (활용도 / 가용성)     (포화도 / 대기열)    (에러 / 결함)
    ----------------     ----------------    -------------
    - % of Time Busy     - Wait Queue Length - Count of Error
    - Resource usage     - Latency spikes    - Hardware faults
    (얼마나 바쁜가?)      (줄이 서 있는가?)     (고장이 났는가?)
    
    Example (Disk):
    - Util: 90% busy     - Sat: 15 I/O waits - Error: 2 bad sectors
```

1. **Utilization (활용도):** 자원이 서비스 요청을 처리하는 데 사용된 시간의 비율(%). 100%에 도달하면 병목의 시작을 의미한다.
2. **Saturation (포화도):** 자원이 처리하지 못해 대기 중인 작업량. 활용도가 100%가 아니더라도 포화도가 높으면 지연 시간(Latency)이 급증한다.
3. **Errors (에러):** 발생한 에러 카운트. 가끔 활용도/포화도가 낮은데 시스템이 느린 경우 하드웨어 에러가 원인일 수 있다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구분 (Metric) | Utilization (활용도) | Saturation (포화도) | Errors (에러) |
| :--- | :--- | :--- | :--- |
| **질문** | "자원이 얼마나 쓰였나?" | "기다리는 작업이 있나?" | "잘못된 게 있나?" |
| **CPU 지표** | % CPU usage | Run Queue Length | Machine Check Exception |
| **Disk 지표** | % Busy (iostat) | Wait Queue (avgqu-sz) | Device Errors (I/O error) |
| **Network 지표** | Input/Output bytes | Dropped Packets | Collision/Interface errors |
| **위험 신호** | 100% 근접 시 위험 | 0보다 크면 성능 저하 | 0이 아니면 즉시 조사 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
**실무적 판단 (Technical Insight):**
엔지니어는 대시보드에 단순히 'CPU 평균'만 띄워놓는 실수를 범한다. USE 메서드에 따르면 **Saturation** 지표인 Load Average나 Run Queue를 함께 봐야 한다.
- **Micro-burst:** 활용도는 낮아 보이지만 찰나의 순간에 포화도가 치솟는 현상을 잡기 위해선 정밀한 모니터링 주기가 필요하다.
- **Checklist Approach:** 장애 대응 시 "CPU-U/S/E 확인 완료", "Memory-U/S/E 확인 완료" 식으로 체크리스트를 채워나가면 누락 없는 완벽한 보고서가 된다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
USE 메서드는 인프라 성능 튜닝의 표준 가이드라인이다. 시스템의 투명성을 높이고 추측성 진단을 배제하며, 데이터 기반의 의사결정을 가능하게 한다. 향후 가상화와 컨테이너 기술이 심화되더라도, 논리적 자원(Pod Limits, Quota)에 대한 분석에 USE 메서드를 확장 적용하여 클라우드 자원 최적화(FinOps)의 초석으로 활용할 수 있다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념:** Performance Engineering, Observability
- **유사 개념:** RED Method (Service), Four Golden Signals (SRE)
- **하위 개념:** Load Average, Queue Theory, I/O Wait

### 👶 어린이를 위한 3줄 비유 설명
- 고깃집에 손님이 몰리는 상황을 생각해 봐요.
- 불판이 다 차서 고기를 굽고 있는 게 '활용도', 밖에서 기다리는 손님 줄이 '포화도', 고기가 타거나 서빙 실수하는 게 '에러'예요.
- 가게 주인이 이 세 가지만 잘 체크하면 왜 가게가 엉망인지 바로 알 수 있답니다!
