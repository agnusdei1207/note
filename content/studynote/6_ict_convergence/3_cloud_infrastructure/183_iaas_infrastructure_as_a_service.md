+++
weight = 183
title = "IaaS (Infrastructure as a Service)"
date = "2024-03-20"
[extra]
categories = "ict-convergence"
+++

## 핵심 인사이트 (3줄 요약)
- **가상 자원 임대**: 물리적 서버, 스토리지, 네트워크를 가상화하여 API나 대시보드를 통해 즉시 제공하는 서비스 모델임.
- **사용자 제어권 극대화**: 운영체제(OS) 선택부터 네트워크 보안 그룹 설정까지 사용자가 직접 관리하여 레거시 이전 및 복잡한 구성이 가능함.
- **CAPEX에서 OPEX로**: 하드웨어 구매 비용을 없애고 사용량 기반 비용(Pay-as-you-go)으로 전환하여 재무 유연성을 확보함.

### Ⅰ. 개요 (Context & Background)
IaaS는 클라우드 컴퓨팅의 가장 기초가 되는 계층으로, 전통적인 데이터센터의 물리적 장비를 소프트웨어로 정의된(Software Defined) 가상 자원으로 대체한다. 기업은 서버를 직접 구매하고 설치하는 데 소요되던 수개월의 시간을 단 몇 분으로 단축할 수 있으며, 필요에 따라 수천 대의 서버를 동시에 기동할 수 있는 무한에 가까운 확장성을 제공받는다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
IaaS는 하드웨어를 추상화하는 가상화 기술과 이를 관리하는 오케스트레이션 레이어를 기반으로 한다.

```text
[ IaaS Architecture Layer ]
+---------------------------------------+   --- User Managed ---
|       Application & Data              |   (Apps, DB, Cache)
+---------------------------------------+
|       Runtime & Middleware            |   (Java, Node, Python)
+---------------------------------------+
|       Operating System (Guest OS)     |   (Linux, Windows)
+---------------------------------------+
|<<<<<<<<<<<< Service Interface >>>>>>>>|   (API, CLI, Console)
+---------------------------------------+   --- Provider Managed ---
|       Hypervisor / Container Engine   |   (KVM, Xen, Docker)
+---------------------------------------+
|       Compute / Storage / Network     |   (CPU, EBS, VPC)
+---------------------------------------+
|       Physical Servers & DC           |   (Region, AZ)
+---------------------------------------+
```

1. **Compute (가상 서버)**: CPU, Memory가 할당된 가상 머신(VM) 인스턴스를 제공.
2. **Storage (가상 스토리지)**: 블록 스토리지(Block), 객체 스토리지(Object) 등 용도별 저장소 제공.
3. **Network (가상 네트워크)**: VPC(Virtual Private Cloud), 서브넷, 로드밸런서, 방화벽(Security Group) 설정.
4. **Provisioning (할당)**: 사용자가 정의한 템플릿(AMI 등)을 기반으로 즉시 자원을 복제 및 배포.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 전통적 데이터센터 (On-Premise) | IaaS (Cloud Infrastructure) |
| :--- | :--- | :--- |
| **자원 확보** | 구매 절차, 납기, 조립 필요 | API 호출 즉시 확보 |
| **비용 모델** | 고정 비용 (CapEx) | 운영 비용 (OpEx) |
| **유지 보수** | 하드웨어 장애 직접 대응 | CSP가 대응 (H/W 무결성) |
| **확장성** | 물리적 서버 증설 한계 | 오토스케일링(Auto-scaling) 가능 |
| **보안 책임** | 물리 보안부터 앱까지 전체 | 물리/하이퍼바이저 보안 (CSP) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **기술사적 판단**: IaaS는 **Lift and Shift (Rehosting)** 전략의 핵심 도구이다. 레거시 애플리케이션의 아키텍처를 크게 바꾸지 않고 클라우드로 이전할 때 가장 효과적이다. 하지만 운영체제 패치나 보안 업데이트의 책임이 사용자에게 있으므로 운영 부담은 여전히 존재한다.
- **실무 전략**: **IaC (Infrastructure as Code)** 기술(예: Terraform)을 사용하여 인프라 구성을 코드로 관리하고, 반복적인 인프라 생성을 자동화하여 수동 설정으로 인한 오류를 방지해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
IaaS는 클라우드 네이티브로 가는 여정의 첫 관문이자 견고한 토대이다. 향후 IaaS는 인프라 관리의 복잡성을 더욱 줄이기 위해 DPU(Data Processing Unit)나 스마트닉(SmartNIC)과 같은 전용 가속 하드웨어를 도입하고 있으며, 베어메탈(Bare Metal) 클라우드와 같이 가상화 오버헤드가 전혀 없는 고성능 모델로도 확장되고 있다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: Cloud Service Models, Infrastructure Management
- **연관 기술**: Virtualization, VPC, Block Storage, Load Balancer
- **확장 개념**: IaC, Auto-scaling, Multi-cloud, Disaster Recovery (DR)

### 👶 어린이를 위한 3줄 비유 설명
1. IaaS는 레고 블록 상자를 통째로 빌려주는 것과 같아요.
2. 상자 안의 블록으로 성을 만들지, 기차를 만들지는 내가 마음대로 결정할 수 있어요.
3. 대신 다 만든 성을 예쁘게 꾸미고 먼지를 닦는 관리는 내가 직접 해야 한답니다.
