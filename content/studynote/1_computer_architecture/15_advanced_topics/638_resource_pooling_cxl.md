---
title: "자원 풀링 (Resource Pooling, CXL 기반)"
date: 2026-03-20
weight: 638
description: "각 서버가 CPU와 메모리를 꽉 움켜쥐고 있던 구조에서 벗어나, CXL 네트워크를 통해 남는 메모리와 가속기를 다른 서버에 빌려주는 데이터센터의 거대한 자원 공유 아키텍처"
taxonomy:
    tags: ["Computer Architecture", "Advanced Topics", "CXL", "Resource Pooling", "Data Center"]
---

> **핵심 인사이트**
> 1. 전통적인 서버 랙 구조에서는 A 서버는 메모리가 남아도는데 CPU가 100%고, B 서버는 CPU는 노는데 메모리가 100% 꽉 차서 죽어가는 극심한 **자원 파편화(Stranded Capacity)** 문제가 있었다.
> 2. **CXL (Compute Express Link)** 기술은 PCIe 버스의 한계를 뚫고, 물리적으로 다른 서버나 외부 박스에 있는 메모리를 내 CPU가 '로컬 램(RAM)'처럼 직접 읽고 쓸 수 있게 해준다.
> 3. 이를 통해 데이터센터 전체의 메모리와 GPU를 하나의 거대한 저수지(Pool)로 묶고, 필요한 서버에게 수도꼭지 틀듯 소프트웨어로 자원을 할당해 주는 **자원 풀링(Resource Pooling / Disaggregation)** 시대가 열렸다.



## Ⅰ. 자원 파편화(Stranded Capacity)의 비극

데이터센터에 10,000대의 서버가 있습니다.
* 어떤 서버는 AI를 돌리느라 메모리 1TB를 다 쓰고 뻗어버렸습니다.
* 바로 옆 서버는 단순 웹 호스팅만 하느라 메모리 1TB 중 10GB만 쓰고 990GB가 텅텅 비어있습니다.

문제는 **옆 서버의 남는 990GB를 절대로 떼어다 쓸 수 없다는 점**입니다. 
서버의 메인보드는 물리적으로 단절되어 있기 때문입니다. 클라우드 기업 입장에서는 전체 메모리의 40~50%가 비어있음에도(Stranded Memory), 메모리가 부족한 서버를 위해 비싼 RAM을 새로 사서 꽂아야 하는 미칠 듯한 돈 낭비가 발생합니다.

> 📢 **섹션 요약 비유**: 식당에서 단체 회식 팀(AI 서버)은 의자가 모자라서 바닥에 앉아 밥을 먹는데, 옆 테이블 혼자 온 손님(웹 서버)은 4인용 식탁을 혼자 다 차지하고 있습니다. 하지만 '테이블 간 의자 이동 금지'라는 엄격한 규칙 때문에 의자를 빌려줄 수 없는 답답한 상황입니다.



## Ⅱ. CXL과 자원 풀링(Pooling)의 마법

인텔, 삼성, SK하이닉스가 뭉쳐서 만든 **CXL (Compute Express Link)**은 이 규칙을 부쉈습니다.

CXL 스위치라는 특수한 장비를 서버 랙(Rack) 중앙에 놓습니다.
그리고 각 서버의 CPU와, 랙 구석에 쌓아둔 '거대한 램 박스(CXL Memory Appliance)'를 CXL 선으로 연결합니다.

### 어떻게 동작하는가? (Composable Architecture)
1. **자원의 분리 (Disaggregation)**: 처음부터 서버를 조립할 때 램을 조금만(예: 32GB) 꽂아 둡니다. 그리고 수백 테라바이트(TB)의 램은 램 전용 박스에 몽땅 모아둡니다 (Memory Pool).
2. **소프트웨어 할당**: A 서버에 갑자기 거대 데이터베이스(DB)가 켜져서 램이 500GB 필요해졌습니다.
3. **풀링(Pooling)**: 클라우드 관리자는 CXL 스위치에게 명령하여 램 박스에서 500GB를 떼어내 A 서버에 논리적으로 연결해 줍니다.
4. **로컬 메모리처럼 사용**: A 서버의 CPU는 이 500GB가 자기 메인보드에 꽂힌 램인지, 저 멀리 램 박스에 있는 건지 전혀 눈치채지 못합니다. (CXL.mem 프로토콜 덕분에 캐시 일관성이 유지됨)
5. **회수**: DB 작업이 끝나면 램을 다시 램 박스로 회수해서, B 서버에게 빌려줍니다.

### CXL 풀링 다이어그램 (ASCII)

```text
 ┌── Server A ──┐    ┌── Server B ──┐    ┌── Server C ──┐ (CPU만 있는 깡통들)
 │ 32GB Local   │    │ 32GB Local   │    │ 32GB Local       │
 └──────┬───────┘    └──────┬───────┘    └──────┬───────────┘
        │                   │                               │
 ═══════▼═══════════════════▼═══════════════════▼═══════ (CXL 스위치 패브릭)
        │                   │                               │
 ┌──────▼───────────────────▼───────────────────▼───────────┐
 │               거대한 CXL 메모리 풀 (Pool)                │
 │ [A에게 500GB 할당 중]   [B에게 100GB 할당]   [남은 10TB] │
 └──────────────────────────────────────────────────────────┘
```

> 📢 **섹션 요약 비유**: 식당의 의자를 각 테이블에 고정시켜 놓지 않고, 중앙 창고(Memory Pool)에 의자를 수백 개 쌓아둡니다. 10명 단체 손님이 오면 창고에서 의자 10개를 꺼내 주고, 손님이 나가면 다시 창고로 집어넣어 다른 손님에게 빌려주는 완벽한 공유 경제 시스템입니다.



## Ⅲ. 데이터센터의 미래

자원 풀링은 메모리뿐만 아니라 GPU 가속기, 스토리지(NVMe-oF)까지 데이터센터의 모든 부품으로 확장되고 있습니다.
결국 미래의 데이터센터 랙(Rack)은 서버 100대가 모인 곳이 아니라, **"CPU 1만 개가 꽂힌 서랍, RAM 10페타바이트가 꽂힌 서랍, GPU 1천 개가 꽂힌 서랍"**으로 물리적 부품이 분리(Disaggregated)되고, 고객이 원하는 대로 부품을 조립해서 1초 만에 나만의 컴퓨터를 만들어내는 '레고 블록 공장'으로 진화할 것입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오

1. **시나리오 — AI/ML 학습 워크로드의 GPU Memory 확장은**: 대규모 AI 모델(예: LLM)을 학습시킬 때, 단일 GPU의 메모리(80GB HBM)가 模型 파라미터(100B parameters)를 저장할 수 없는 상황. CXL Memory Pool에서 512GB의 메모리를 GPU 서버에 할당하면, CPU-GPU間のPCIe 대역폭은 bottleneck이 되지만, 部分적인offloading과checkpoint-saving에 necessary한 메모리를CXL pool에서 끌어다 사용하여, 80GB → 592GB로 확장이可能하고, 因此 模型을 분산학습하지 않고도 단일 服务器에서 학습 가능한 파라미터 수가 늘어난다.

2. **시나리오 — 피크 시간 대비 평소 시간의 Memorypool 관리**: 전자상거래사이트에서 11번가 세일(peak) 때만Instances数が平时的10배增加하여, 각Instances마다 memory를 profusely 할당해야 하지만,平时的には大部分이 idle한 상황. CXL 기반의 Pooled Memory를 使用하면, peak 때만 Pool에서 memory를Dynamic하게 할당하고,平时에는 Pool에 되돌려 다른 Applications에 재분배함으로써, -hardware采购 비용을 70% 절감하면서도 SLA를 유지할 수 있다.

3. **시나리오 — GPU 가속기 풀링**: 여러 사용자가 GPU가 탑재된 服务器를 사용하고자 하지만, 각자의 GPU需求量이 적고 时差가 있는 상황. CXL로 连接된 GPU Pool에서 필요한 만큼만 GPU 가속기를 할당받고, 사용이 끝나면 Pool에 반환함으로써, GPU资源的整体的利用率을 3~5배 향상시킨다.

### 도입 체크리스트
- **기술적**: CXL device의 할당/반환 latency가 어플리케이션의 성능에 미치는 영향을 分析. 일반적으로 10~100μs 수준의 latency가 발생하므로,高频으로 할당/반환하는 워크로드에는向하지 않을 수 있다.
- **운영·보안적**: Pool 내에서 다른tenant의 데이터가 Isolation되어야 한다. CXL의 memory coherence protocol(CXL.mem)이 tenant간 privacy를 보장하는지 확인하고,必要时 additional encryption를 적용해야 한다.

### 안티패턴
- **CXL pool의 과도한 의존**: 모든 workload를 CXL Pool에 연결하면, CXL 스위치의 대역폭이 새로운 bottleneck이 될 수 있다. Local memory를 기본으로 사용하고, overflow 시에만 CXL pool을 使用하는 hierarchical 방식을 采用해야 한다.
- **Security isolation 미흡**: Pool 내の資源共有로 인해, malicious tenant가다른tenant의 memory에 접근하는 side-channel이 발생할 수 있다. CXL의 security features(CXL.mem의 memory tagging等)를 활용하고,必要时 IOMMU와連携하여 protection을 강화해야 한다.

> 📢 **섹션 요약 비유**: CXL Memory Pooling은「어느 한 식탁에 의자가 부족하면, 中央창고에서 의자를 가져와 추가하고, 다 쓰면 회수하는 것」과 같다. 하지만中央창고(CXL switch)에 병목이 생기면 역으로 모든 식탁이 느려질 수 있듯이, 설계시에 中央集中のボトルネック을 고려해야 한다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량/정성 기대효과

| 구분 | 전통적Server별Memory 배분 | CXL Memory Pooling | 개선 효과 |
|:---|:---|:---|:---|
| **전체 메모리 효율** | 평균 40% 활용 (Stranded Memory 60%) | 평균 80% 활용 | **2배** 효율 향상 |
| **피크 대응 비용** | 피크를 위한 과잉 구매 200% | 피크 시 Pool에서 할당, 평시 회수 | **50%** 비용 절감 |
| **GPU 메모리 확장이** | GPU당 독립 80GB | Pool에서 512GB 추가 가능 | **6.4배** 확장 |
| **리소스 분리 가능성** | 물리적 서버 단위 | Memory/GPU 단위 분리 | **세분화** |

### 미래 전망
- **CXL 3.0과 全면적 Pooling**: CXL 3.0에서는 여러switch를跨�은Global Memory Pool이 가능해져, 数据센터 전체를 하나의巨大的 Memory Fabric으로 통합할 수 있을 것으로 기대된다.
- **Composable Disaggregated Infrastructure**: CPU, Memory, GPU, Storage가 모두 别々の 풀에 놓여 있고, 응용 프로그램이 필요에 따라 자원을Dynamic하게 조합하는 "Composed System"이 차세대 데이터센터의 표준形态이 될 것이다.
- **Memory Semantic SSD와의 통합**: CXL-oF (CXL over Fabric)와 결합되면, NVMe SSD마저도远程에서Pool화하여,-hot data는 CXL memory에, cold data는 pooled SSD에 자동으로 配置되는 계층형 메모리-스토리지融合的时代가 올 것으로 전망된다.

### 참고 표준
- **CXL 2.0/3.0 Specification**: CXL Consortium이制定한 device间的高速互联 标准으로, CXL.mem (memory), CXL.cache, CXL.io의 3가지 프로토콜을 정의한다.
- **CXL Consortium (Intel, Samsung, SK hynix 등)**: CXL 기술을推进する企业団体으로, 표준制定와兼容性テスト를 담당한다.
- **OCP (Open Compute Project) Rack Manager**: rack-level의 composable infrastructure를標準화하는 项目이다.

CXL 기반 Resource Pooling은 데이터센터의 "고정資産"을 "유동 자산"으로 변환하는 패러다임이다. 더 이상 服务器를 사면 그 안에 CPU, Memory, GPU가 终身 다가 되어 버리는 것이 아니라, 필요에 따라 언제든지 그 어느 服务器에든 빌려주고 돌려받을 수 있는 유연한 Infrastructure가 되겠다. 이것은 클라우드 데이터센터의 TCO를 크게 줄일 뿐만 아니라, 실리콘도 효율적으로 활용하는 环境친화적 기술이 될 것이다.

> 📢 **섹션 요약 비유**: CXL Resource Pooling의 등장으로 数据센터는「모던 레고ランド」に変わった. CPU, Memory, GPU, Storage가 레고 블록처럼各自_pool에 놓여 있고, 顧客은 필요한 만큼만 집어다가 自컴퓨터를 1분 만에 조립하고, 다 쓰면 옆 사람에게 되돌려주는 것이 가능해졌다.

---

### 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **CXL (Compute Express Link)** | CPU, Memory, GPU等를高速으로互联하는 Intel主导のバス標準で、PCIe를 기반으로 한다. |
| **CXL.mem** | CXL의 3가지 프로토콜 중 하나로, memory expander처럼動作하여 remote memory에 접근한다. |
| **Disaggregated Infrastructure** | 服务器의 구성요소(CPU, Memory, GPU, Storage)를物理적으로分离하여, 各自独立に pool화하는アーキテクチャだ. |
| **Stranded Capacity** | 활용 가능한 resource이지만 현재 할당된server에서 使用 불가능한 남아도는 resource의 문제를 말한다. |
| **IOMMU** | CXL device의 memory 접근을 Virtualize하고, tenant間の Isolation을保障하는 하드웨어要素다. |
| **Composable System** | 필요한resource를动态组合하여 形成하는 시스템으로, CXL pooling과밀접한 관련이 있다. |

---

### 👶 어린이를 위한 3줄 비유 설명
1. 우리 학교에는 1반에는 컴퓨터가 10대 있지만 1대밖에 없지만, 2반에는 컴퓨터가 1대밖에 없지만 10대가 있어요. 그런데 컴퓨터들은 마음대로 빌려줄 수 없어서, 2반 친구들은 컴퓨터가 모자라서 프로그램을 못 돌아요.
2. 그래서 컴퓨터 센터장님(CXL switch)이「어느 반에서든 필요하면 컴퓨터를 가져가 고, 다 쓰면 컴퓨터 센터에 돌려줘!」라고 하면, 다들 컴퓨터를効率적으로 쓸 수 있어요.
3. 하지만 컴퓨터 센터장님이 너무 바빠서(스위치 병목) 빌려주는 속도가 느리면, 차라리 각 반에 컴퓨터를 그냥 나눠주는 게 더 나을 수 있어요. 그래서 경우에 따라 다르게 생각해야 해요!
