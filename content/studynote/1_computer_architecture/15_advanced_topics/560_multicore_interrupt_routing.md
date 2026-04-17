+++
title = "560. 멀티코어 인터럽트 라우팅 (GIC, APIC)"
date = 2026-03-20
weight = 560
description = "코어가 수십 개인 멀티코어 환경에서, 수많은 외부 인터럽트를 어느 코어에게 분배할지(부하 분산) 지능적으로 결정하는 고급 인터럽트 컨트롤러"
taxonomy =  ""
tags = ["Computer Architecture", "Advanced Topics", "Multicore", "Interrupt", "APIC", "GIC"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. 싱글 코어 시절에는 인터럽트가 들어오면 무조건 하나뿐인 CPU 코어가 처리하면 됐다. 하지만 코어가 64개인 서버에서는 **"이 인터럽트를 어느 코어에게 던져야 제일 효율적일까?"**라는 라우팅(Routing) 문제가 발생한다.
> 2. 이를 해결하기 위해 인텔은 **APIC(Advanced Programmable Interrupt Controller)**를, ARM은 **GIC(Generic Interrupt Controller)**라는 거대한 분배기 칩을 메인보드와 CPU 코어마다 장착했다.
> 3. 이 컨트롤러들은 코어들의 부하를 모니터링하여 인터럽트를 골고루 뿌려주거나(부하 분산), 프로세서 간 통신(IPI)을 가능하게 하여 멀티코어 운영체제가 부드럽게 돌아가도록 돕는다.



## Ⅰ. 멀티코어 시대, 누구에게 인터럽트를 줄 것인가?

100Gbps 랜카드에 초당 백만 개의 패킷이 들어옵니다. 랜카드는 인터럽트를 마구 쏩니다.
만약 이 인터럽트를 **0번 코어 하나만 다 받아서 처리한다면**, 0번 코어는 네트워크 처리만 하다가 과로사하고 나머지 63개 코어는 펑펑 노는 극단적인 병목(Interrupt Storm)이 발생합니다.

이를 막기 위해 OS와 하드웨어는 다음과 같은 분배 원칙을 세웁니다.
* **지정 배송 (Static Routing)**: "랜카드 인터럽트는 1번 코어가, 그래픽카드 인터럽트는 2번 코어가 전담해!"
* **부하 분산 배송 (Round-Robin / Lowest Priority)**: "랜카드 패킷이 너무 많으니, 0번부터 7번 코어까지 돌아가면서 하나씩 받아(Round-Robin), 아니면 지금 제일 한가한 코어(Lowest Priority)한테 줘!"

이 똑똑한 교통정리를 해주는 교차로가 바로 멀티코어 인터럽트 컨트롤러(GIC/APIC)입니다.

> 📢 **섹션 요약 비유**: 식당 창구에 배달 주문(인터럽트)이 1분에 100개씩 들어옵니다. 주방장 1명(싱글 코어)일 때는 그냥 혼자 다 받았지만, 요리사가 64명이 되자 매니저(APIC/GIC)가 나서서 "너는 피자만 만들고, 너는 탕수육 만들어. 남는 주문은 지금 쉬고 있는 요리사한테 하나씩 던져줄게!"라고 통제하는 것입니다.



## Ⅱ. APIC의 2단계 구조 (Local APIC와 I/O APIC)

인텔/AMD의 x86 아키텍처는 **APIC 구조**를 표준으로 사용합니다. 거대한 교차로를 혼자 관리하기 힘드니, 중앙 우체국과 동네 우체통으로 나눴습니다.

1. **I/O APIC (중앙 분배기)**
   * 메인보드 칩셋(PCH) 쪽에 붙어 있습니다.
   * 마우스, 랜카드, 디스크 등 외부 장치들의 물리적 선이 여기에 꽂힙니다.
   * 인터럽트가 들어오면 OS가 설정해 둔 장부(Redirection Table)를 보고, "이건 3번 코어한테 줘야겠다"고 결정하여 CPU 쪽으로 메시지를 쏩니다.
2. **Local APIC (코어별 개인 우체통)**
   * CPU 칩 내부의 **각 코어마다 1개씩 이마에 찰딱 붙어 있습니다.** (64코어면 Local APIC도 64개).
   * I/O APIC가 보낸 메시지를 받아서 자기 코어에 찔러 넣습니다.
   * 자기 코어 전용 타이머(Local Timer)를 가지고 있고, 코어의 온도 에러 등 코어 내부의 프라이빗한 인터럽트도 처리합니다.

### 통신 구조 (ASCII 다이어그램)

```text
 [ 외부 장치들 (NIC, GPU 등) ]
          │ (물리적 선)
          ▼
 ╔═════════════════════╗ (라우팅 룰: "NIC은 코어 2로 보내!")
 ║     I/O APIC        ║ ─── 시스템 버스 (APIC 버스) ───┐
 ╚═════════════════════╝                                           │
                                                       ▼
 ┌───────── CPU 칩 내부 ───────────────────────────────────────────┐
 │ ┌────────────┐   ┌────────────┐   ┌────────────┐                │
 │ │ Local APIC │   │ Local APIC │   │ Local APIC │ ◀ (수신 완료)  │
 │ └─────┬──────┘   └─────┬──────┘   └─────┬──────┘                │
 │    [코어 0]         [코어 1]         [코어 2]                   │
 └─────────────────────────────────────────────────────────────────┘
```

> 📢 **섹션 요약 비유**: 외부 우편물(인터럽트)은 1층 중앙 우편실(I/O APIC)로 다 모입니다. 우편실 직원은 명부를 보고 각 층의 부서(코어) 앞에 있는 개인 우편함(Local APIC)에 편지를 꽂아줍니다.



## Ⅲ. IPI (Inter-Processor Interrupt)

Local APIC/GIC의 또 다른 무서운 능력은 **코어들끼리 서로에게 총을 쏠 수 있다(인터럽트를 걸 수 있다)**는 것입니다. 이를 **IPI (프로세서 간 인터럽트)**라고 부릅니다.

* 0번 코어가 OS 커널을 돌리다가 "지금부터 프로그램 전체 종료할 테니, 나머지 코어들 하던 일 당장 멈춰!"라고 명령해야 할 때가 있습니다.
* 이때 0번 코어의 Local APIC는 버스를 타고 1번~63번 코어의 Local APIC에게 폭격(IPI)을 가합니다.
* 앞서 배운 치명적인 병목 현상인 **TLB 슈팅다운(Shootdown)**도 바로 이 IPI 기능을 통해 구현됩니다. 코어 간의 긴밀한 협동과 동기화를 가능하게 하는 멀티코어 운영체제의 필수 배관입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오

1. **시나리오 — 네트워크 인터럽트의 부하 분산**: 100Gbps SmartNIC이 달린 서버에서 packetrate가 초당 5,000만 개일 때, 이 인터럽트를 단일 코어에 집중시키면 코어가 100% 사용되어 다른処理が滞る. GIC/APIC의 MSI-X(Messaaged Signaled Interrupts) 기능을 활용하여packet별interrupt를 여러 코어에 분산시키고,RSS(Receive Side Scaling) 테이블과 연동하여同じフロー(5-tuple 기준)이 항상同じ코어에서処理されるように設計する.

2. **시나리오 — 실시간 시스템의interruptLatency 보장**: 산업용 로봇控制器(실시간 OS: VxWorks等)에서 모터 엔코더tick(1ms마다) interrupt의 latency가 10μs 이내로 보장되어야 하는 상황. interrupt처리를 Dedicated CPU core에 할당하고,OS의IRQ affinity 설정으로 다른/task가 해당 코어를 점유하지 못하도록 하여interruptStorm을 방지한다.

3. **시나리오 — ARM GICv3의 LSU(Logical Sandboxing Unit)攻击防御**: 공유 Interrupt 컨트롤러에 대한timing攻击을 방어하기 위해, GIC의 ITS(Intelligence TargetScrubber)로 interrupt를 routing하기 전, 各interrupt에 할당된 security labeling을 검증하여, 비인가된 VM이 다른 VM의 interrupt를 横取り하지 못하게 한다.

### 도입 체크리스트
- **기술적**: MSI(Message Signaled Interrupts) 지원 여부를確認. MSI는传统的PIRQs보다 interruptRouting이 유연하고, 地址حدrpacking이 되어 핀 수 제한 없이数千 개의 interrupt를 보낼 수 있다.
- **운영·보안적**: interrupt affinity 설정 시 performance와 latency trade-off를 分析. 특정 코어에 interrupt를 집중시키면 그 코어는 interrupt 처리만 하고 다른 작업은 수행하지 못하므로, workload characteristic에 맞는 균형점 찾기.

### 안티패턴
- **Interrupt Storm 미인식**: 네트워크 packet 처리 시 interrupt 처리가 너무 자주 일어나면, OS가 interrupt handling에 모든 시간을 소요하여 user 程序이 실행될 틈이 없는 상황이다. NAPI(New API)나 interrupt coalescing設定으로 해결한다.
- **IPI Storm에 의한 사이드채널**: 코어 간 IPI를 너무 빈번하게 보내면(예: spinlock bust의 경우), IPI의 timing이 관찰 가능해져 Spectre류의 사이드채널攻撃에 악용될 수 있다.

> 📢 **섹션 요약 비유**: 멀티코어 interrupt routing은 "피자 가게에서 배달 주문이 1분에 1000건 들어올 때, 피자店主 1명(CPU 코어)이全部 처리하다 보면 굽은지 타는 것"과 같다. 매니저(GIC/APIC)가 주문을 여러店主에게 분배해서 모두合作して全部 제때 delivery하는 구조이다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량/정성 기대효과

| 구분 | 단일 코어 집중 | 코어 분산 routing | 개선 효과 |
|:---|:---|:---|:---|
| **Interrupt 처리량** | 1코어 @100% → 500K int/sec | 8코어 @50% → 4M int/sec | **8배** 처리량 향상 |
| **Application latency** | interrupt block으로인한 jitter ~1ms |专职 코어分離로 jitter < 10μs | **100배** 지연 감소 |
| **전력 효율** | 1코어 과부하 + others 유휴 | 모든 코어 균형작업 | 에너지효율 **3~5배** 향상 |

### 미래 전망
- **GICv5 / APIC-x2APIC의 차세대 보안 기능**: ARM GIC는 ITS(Interrupt Translation Service)를 통해virtual queue를 지원하여, VMs之间 interrupt 격리가 더욱強化될 것으로예상된다.
- **RISC-V의 PLIC(Platform Level Interrupt Controller) 표준화**: RISC-V 생태계에서PLIC가事実상의 표준이 되어, 차세대 开源处理器에서도 APIC/GIC 수준의 interrupt routing이 가능해질 것으로展望된다.
- **AI加速기との共生**: Neural Processing Unit이 고속으로 inference 결과를产出할 때, NPU가 직접 CPU 코어에 interrupt를 보내는path가 최적화되어야 하며, 이는 accelerator-orchestrated interrupt 설계로 발전하고 있다.

### 참고 표준
- **ARM GICv3/v4 Architecture Specification**: ARM 기반 시스템의 interrupt 컨트롤러 표준
- **Intel APIC Architecture Specification**: x86 아키텍처의 local/APIC 및 I/O APIC 동작 표준
- **PCIe MSI-X Capability Structure**: PCIe 장치가 MSI-X를 통해interrupt를 software에通告하는 메커니즘 표준

멀티코어 환경에서 interrupt routing은 시스템 성능과 실시간성을 좌우하는 핵심 인프라다. 하드웨어의Intelligent routing 기능과 OS의 affinity 설정이 연계되어야Effficient한 시스템 동작이 가능하며, 보안 측면에서도 interrupt 横取り 공격에 대한 방어가 필수적이다.

> 📢 **섹션 요약 비유**: interrupt routing은 대규모 피자 체인점에서 주문(internet)이 들어올 때, 본사에서 모든 주문을 1명 피자店主에게集中시키면店主이 녹아버리므로, intelligent 매니저(GIC/APIC)가 여러店主에게 주문를 나눠주는 것과 같다.

---

### 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Local APIC / GIC (CPU Interface)** | 각 CPU 코어 앞에 붙어 있는 interrupt 수신 부로, 해당 코어에 interrupt를 전달한다. |
| **I/O APIC / GIC (Distributor)** | 외부 장치의 interrupt를 받아 routing 규칙에 따라 각 Local APIC에 분배한다. |
| **MSI (Message Signaled Interrupts)** | 핀 기반 interrupt 대신 memory write로 interrupt를 신호하는 PCIe 표준 방식이다. |
| **IPI (Inter-Processor Interrupt)** | OS가 코어 간 동기화나TLB shootdown 등을 위해 보내는 interrupt이다. |
| **IRQ Affinity** | OS가 특정 interrupt를 어떤 코어에서処理할지를 설정하는 것이다. |
| **Interrupt Coalescing** | 빈번한 interrupt를 모았다가 한꺼번에 처리하여 overhead를 줄이는 기술이다. |

---

### 👶 어린이를 위한 3줄 비유 설명
1. 학교에 편지(interternet)가 한꺼번에 1000통씩 들어오면, 지키미 1명(한 개의 코어)이全部 읽다 보면 피곤해서倒在地에 놀다.
2. 그래서 매니저(GIC/APIC)가 "다른守卫에게 몇 통씩 나눠서 읽어!" 하고 분배해줘요. 그래야大家が均等に忙碌한다.
3. 또,守卫 사이에서도 "내가 지금 바빠! 너 먼저 읽어줘!" 하고 서로 편지를 건네는(IPI) 것인데, 이것도 매니저가 잘 조절해주어야 한꺼번에 몰려서uty되지 않는다.
