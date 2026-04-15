+++
weight = 126
title = "토일 (Toil)"
date = "2024-03-23"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
- SRE 관점에서 토일은 반복적이고 수동적이며 자동화 가능한, 비즈니스 가치가 낮은 운영 작업을 의미한다.
- 토일은 엔지니어의 창의적 시간을 뺏고 번아웃을 유발하므로, SRE 팀은 토일 비중을 업무 시간의 50% 미만으로 엄격히 제한해야 한다.
- 토일을 줄이는 유일한 방법은 '자동화'이며, 이를 통해 확보된 시간은 시스템의 신뢰성을 높이는 프로젝트에 재투자된다.

### Ⅰ. 개요 (Context & Background)
- **정의**: 서비스 운영 중 발생하는 수동적이고(Manual), 반복적이며(Repetitive), 자동화 가능하고(Automatable), 전술적이며(Tactical), 장기적 가치가 없는(No Enduring Value) 작업을 뜻한다.
- **배경**: 서비스 규모가 커짐에 따라 운영 작업(토일)이 선형적으로 증가하면 인력을 무한정 늘릴 수 없게 된다. 이를 해결하기 위해 구글은 SRE 직무를 통해 운영을 '소프트웨어 문제'로 취급하고 자동화하도록 강제했다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
[ SRE Work Balance & Toil Reduction ]

   [ Engineer's Time (100%) ]
   +-----------------------+
   |  Project Work (50%+)  | --> New Features, Automation, Scalability
   | (Creative/Engineering)|
   +-----------------------+
   |    Toil Work (<50%)   | --> Manual Scaling, Rebooting, Ticket processing
   | (Repetitive/Manual)   |
   +-----------------------+
             |
      [ Feedback Loop ]
      - Measure Toil
      - Automate Toil
      - Free up Time for Projects
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 토일 (Toil) | 일반적인 운영 작업 (Overhead/Admin) |
| :--- | :--- | :--- |
| **반복성** | 매우 높음 | 상대적으로 낮음 (회의, 인사 등) |
| **자동화** | 가능함 (스크립트, 오케스트레이션) | 불가능하거나 비효율적임 |
| **확장성** | 서비스 성장과 함께 선형적 증가 | 서비스 성장과 직접 연동되지 않음 |
| **엔지니어링** | 없음 (단순 수행) | 일부 포함 (정책 결정 등) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **식별 방법**: "이 작업을 굳이 내가 지금 수동으로 해야 하는가?"라는 질문을 던진다. 만약 같은 작업을 세 번 이상 반복했다면 자동화 대상이다.
- **관리 전략**: 토일의 비중을 정기적으로 측정하고, 50% 임계치를 넘을 경우 신규 기능 개발(Feature Work)을 멈추고 운영 자동화에 집중하는 '에러 예산(Error Budget)'과 유사한 통제 정책이 필요하다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- 토일을 제거함으로써 엔지니어는 더 가치 있는 일에 집중할 수 있으며, 이는 시스템의 가용성과 성능 향상으로 직결된다. 미래의 인프라는 자가 치유(Self-healing)와 지능형 자동화(AIOps)를 통해 토일을 '0'에 가깝게 수렴시키는 방향으로 진화하고 있다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: SRE (Site Reliability Engineering)
- **자식 개념**: 자동화(Automation), 자가 치유(Self-healing)
- **연관 개념**: 에러 예산(Error Budget), 온콜(On-call), 번아웃(Burnout)

### 👶 어린이를 위한 3줄 비유 설명
- 토일은 매일 아침 방을 치우거나 쓰레기를 버리는 것처럼, 꼭 해야 하지만 지루하고 매번 똑같은 일을 말해요.
- 이런 일을 로봇이 대신하게 만들면, 우리는 더 재미있는 장난감을 만들거나 책을 읽을 시간을 가질 수 있죠.
- SRE 아저씨들은 로봇을 잘 만들어서 지루한 일을 없애는 사람들이에요.
