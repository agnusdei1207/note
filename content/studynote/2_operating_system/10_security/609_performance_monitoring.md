+++
title = "609. 성능 모니터링 (Performance Monitoring) 및 튜닝 방법론"
date = "2026-03-25"
[extra]
categories = "studynote-operating-system"
+++

# 성능 모니터링 (Performance Monitoring) 및 튜닝 방법론

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 성능 모니터링은 CPU, Memory, I/O, 네트워크 등 시스템 자원)의 사용률, Throughput, Latency, Utilization 등을 지속적으로 측정 수집 분석하여 병목을 탐지하고, 성능 저하 발생 전에 선제적으로 대응하기 위한 운영체제 핵심 운영 업무이다.
> 2. **가치**: 시스템의 병목 지점을 정확히 파악하면, Hardware 증설, Software 튜닝, Architecture 변경 등 어떤 투자 대비 효과가 가장 큰가를データに基づいて判断할 수 있으며, 이를 통해 인프라 비용을 최소화하면서 최대 처리량을 확보할 수 있다.
> 3. **융합**: 성능 모니터링은 OS의프로세스调度자, 메모리 관리자, I/O 스케줄러와 깊이 연결되어 있으며, Prometheus + Grafana, Datadog, Splunk 등의모니터링 스택과 결합하여 실시간 Alert와historical 트렌드 분석을可能하게 한다.

---

## 1. 개요 및 필요성

### 개념 및 정의
성능 모니터링이란 운영체제가 제공하는프로세스, 메모리, 디스크 I/O, 네트워크 스택, 시스템 콜 등의Metric을도구을 활용하여 수집하고, 이를 분석하여 시스템의 健康状態를 평가하는 활동이다. 핵심 목표는 "현재 시스템의どの部分が最大の制約になっているか"를 찾는 것이다. 시스템 성능을 분석하는 데는 크게 Throughput(처리량), Latency(지연 시간), Utilization(사용률), Availability(가용성) 등 다양한 지표가 있다.

**필요성 및 등장 배경**
과거에는 성능 저하가 발생하면 시스템 관리자가 手当たり次第の原因を探したが，现代の 시스템은 수십 개의 마이크로서비스가 서로呼び合い하며, 하나의 서비스 성능 저하가 全システムチェーン의 성능 저하를 유발하는 分散 아키텍처로 발전했다. 이로 인해性能問題의 root cause 분석이 매우 복잡해졌고,这些问题가 발생하기 전에 선제적으로 파악하는 것이 비즈니스 연속성 유지의 핵심이 되었다.

```
[성능 모니터링: 왜 필요한가?]

[性能問題発生後の後追い対応: コスト大]

利用자가増加 --> Latency増加 --> Timeout 발생
     |
     +--> 問題発生! --> 慌てて調査 --> 根本原因 찾기 --> 수일 소요

[性能問題發生前の主動的対応: コスト小]

利用자가増加 --> 병목 조기 탐지 --> 선제적 확장 --> 피해 0!
     |
     +--> 모니터링에서_cpu/memory saturation 알람 --> 事前 대응

핵심 Insight:
- 성능 문제는 "발생 후 대응"보다 "사전 탐지"이 10배 저렴
- Alibaba은 평균 1시간 서비스 중단 시 6백만 달러 손실
- 因此、性能監視は"보험"이다!
```

**[다이어그램 해설]** 이 비교는性能監視为什么要从"後追い対応"转变为"事前予防"의 핵심洞察を示している. Google의 SRE 팀은 "performance budgets"라는 개념을 사용하여、システムの本当の性能問題が発生する前に、スケーリングや最適化を実行하는 것이、问题発生後の紧急対応보다 人件비를 포함하여 全般적으로 10배 이상 저렴하다고 밝혔다.

- **요약 비유**: 성능 모니터링은 자동차 계기판과 같다. 엔진 오일 gauge가 빨간불 뜨는 것을 무시하고 달리면 엔진이 고장 나지만, gauge를 주시하면维修전에 문제가 있는 것을 파악하여整備를 갈 수 있다.

---

## 2. 아키텍처 및 핵심 원리

### Linux 성능 모니터링 도구 계층 구조

Linux 환경에서性能監視는 여러 수준(level)의 도구를 통해 이루어진다.

| 수준 | 도구 | 측정 대상 | 핵심 Metric |
|---|---|---|---|
| **시스템 전체** | `top`, `htop`, `glances` | 전체 CPU, Memory 사용률 | %CPU, %MEM, Load Average |
| **프로세스 단위** | `ps`, `pidstat` | 개별 프로세스 자원 사용 | CPU%, MEM%, RSS, FD count |
| **CPU** | `mpstat`, `sar` | 코어별 사용률, 컨텍스트 스위칭 | %usr, %sys, %idle, cs/sec |
| **메모리** | `free`, `vmstat` | RAM 및 스왑 사용률 | available, used, swap in/out |
| **디스크 I/O** | `iostat`, `iotop` | Throughput, IOPS, latency | tps, kB_read/s, await |
| **네트워크** | `netstat`, `ss`, `sar -n DEV` | 패킷 통계, 연결 상태 | pkt/s, RX/TX kB/s, retrans |
| **I/O 크기 분포** | `bio`, `blktrace` | block I/O 요청 분포 | request size, latency histogram |
| **추적/프로파일링** | `perf`, `strace`, `bpftrace` | 함수 단위 profiling, syscall 추적 | call count, latency per function |
| **전체 시스템** | `sar` (System Activity Reporter) | Historical metric 수집/저장 | 시간대별 모든 metric의 历史데이터 |

### Linux 성능 모니터링 주요 명령어 상세 사용법

```
[Linux 성능 모니터링: 주요 도구의 정확한使い方]

[1] CPU 병목 탐지: top + mpstat

$ top   (실시간 CPU/메모리 사용률, Process별 정렬)

$ mpstat -P ALL 1 5
--> 각 CPU 코어별 사용률을 1초 간격으로 5번 측정
--> 특정 코어만 100%면 single-threaded Process 병목!

[2] 메모리 병목 탐지: free + vmstat

$ free -h   (전체 메모리 사용량 확인)
--> available: 실제 사용 가능한 메모리 (cached 포함)
--> available이 0에 가까우면 OOM Killer 발동 가능성!

$ vmstat 1 10  (1초 간격으로 10회 메모리/프로세스 통계)
--> si/so: 스왑 인/아웃 --> 메모리 부족의明確な 신호!

[3] 디스크 I/O 병목 탐지: iostat + iotop

$ iostat -xz 1  (디스크별 I/O 통계, 1초 간격)
--> await: I/O 요청에서 처리 완료까지 平均 대기 시간
--> %util: 디스크 포화도 (100%면 디스크 포화!)
-->avgqu-sz: 대기 큐 길이 --> 큐가 길면 병목!

$ iotop -o  (I/O 사용하는 프로세스 정렬)

[4] 네트워크 병목 탐지: ss + netstat

$ ss -s   (TCP 연결 상태 요약)
$ sar -n DEV 1 5  (네트워크 인터페이스별 통계)
```

**[다이어그램 해설]** 각 도구가 측정하는 대상は重叠하지만、分析 목적에 따라 선택이 달라진다. `top`은即時的な全体-overview에 적합하고, `sar`은 과거 데이터 분석에 적합하다. `iostat`에서 가장 중요한 Metric은 `await`(실제 I/O 대기 시간)와 `%util`(디스크 포화도)이다.

### 리눅스 성능 분석 방법론: USE(Utilization, Saturation, Errors) 원칙

성능 병목을 分析하는系統적 방법론으로、Brendan Gregg가 제시한 USE(Utilization, Saturation, Errors) 원칙이 있다.

- **Utilization (사용률)**: 자원이 사용 중인 시간 비율
- **Saturation (포화도)**: 자원의 대기 큐 길이 또는 처리 능력을 초과한 정도
- **Errors (에러율)**: 자원 관련 오류 발생 빈도

```
[USE 방법론: 모든 자원에適用하는性能 分析 체크리스트]

[CPU]
- Utilization: 전체 CPU 사용률 --> `top`, `mpstat`
- Saturation: 실행 대기 프로세스 수 --> Load Average > 코어수
- Errors: CPU 자체 에러 --> `/proc/cpuinfo`에서 mce 확인

[Memory]
- Utilization: RAM 사용률 --> `free -h`
- Saturation: 스왑 IN/OUT --> `vmstat` si/so
- Errors: OOM Killer 발동 로그 --> `dmesg | grep -i oom`

[Disk I/O]
- Utilization: %util --> `iostat -xz`
- Saturation: avgqu-sz(대기 큐 길이) --> iostat
- Errors: 에러 count --> `dmesg | grep -i error`

[Network]
- Utilization: Interface throughput --> `sar -n DEV`
- Saturation: 연결水池, 재전송율 --> `ss -s`, `netstat`
- Errors: packet error rate --> `sar -n EDEV`

分析 순서:
1. Saturation이 있으면 가장 먼저 해결 (대기 중인 요청=병목)
2. Utilization이 100%에 근접하면 hardware upgrade 검토
3. Errors가 비정상적으로 높으면 HW 문제 가능성--> 점검
```

**[다이어그램 해설]** USE 원칙의 핵심은"가장 먼저 Saturation을 확인하라"는 것이다. Utilization이 80%이지만 Saturation이 0이면 시스템은健康的이고 추가 확장이 필요 없을 수 있다. 반대로 Utilization이 50%이지만 Saturation이 높으면 대기열이 형성되고 있다.

- **요약 비유**: USE 방법은 택배 물류 창고 관리와 같다. 창고工人(Utilization)이 100% 일情况下도 truck의到来频度(throughput)를 处理할 수 있다면問題 없다. 그러나 truck가，杀到하는 상황에서는(蒋포화,Saturation)工人稼働率이 100%이든 아니든関係없이 truck가杀了されている것이므로 가장紧急에 해결해야 할 문제가 있다.

---

## 3. 융합 비교 및 다각도 분석

### 전통적 모니터링 vs APM vs eBPF 기반 모니터링

| 비교 항목 | 전통적 모니터링 (sar, top) | APM | eBPF 기반 모니터링 |
|---|---|---|---|
| **측정 수준** | OS Kernel 레벨 metric | Application 레벨 (응답 시간, 에러율) | Kernel/User 레벨 모두 |
| **오버헤드** | 매우 낮음 | 중간 (에이전트 기반) | **매우 낮음** (커널 내 샌드박스) |
| **세밀함** | Process/Thread 수준 | 함수/메서드 단위 | 네트워크 이벤트레벨, 커널 함수 단위 |
| **실시간성** | 수초~수분 단위 | 수초 단위 | **마이크로초 단위** |
| **주요 도구** | sar, top, iostat, vmstat | Datadog, New Relic, AppDynamics | bpftrace, BCC, Cilium Tetragon |

```
[성능 모니터링 도구 선택 가이드: 목적別 추천]

목적: 간단한 Server Health 확인
--> `top`, `htop`, `glances`  (数秒 단위 overview)

목적: Historical 성능 추이 분석 (사후 분석)
--> `sar` + 성능 DB 저장 + Grafana Visualization

목적: 특정 I/O 패턴/프로세스 profiling
--> `perf`, `strace` (函数-level 상세 分析)

목적: 네트워크 레벨 이상 탐지 (보안+성능)
--> `ss`, `tcpdump`, `eBPF` (패킷 레벨)

목적: 분산 마이크로서비스 종속성 추적 (트랜잭션 흐름)
--> APM 도구 (Jaeger, Zipkin, Datadog APM)

목적: 긴급 장애 시Root Cause 5분 내 파악
--> `perf top`, `bpftrace` (커널 레벨 추적)
```

**[다이어그램 해설]** 각 도구는得意分野가 다르므로、目的に応じた選択が重要である. 단순히"서버가正常인가?"는 `top`으로 충분하지만,"특정 API 응답 시간이 느린根因이 무엇인가?"는 APM이나 `perf`가 필요하고,"네트워크 레벨에서 이상한 트래픽이 있는가?"는 eBPF 기반 도구가 가장 효과적이다.

- **요약 비유**: 성능 모니터링 도구 선택은병원 진료과 선택과 같다. 간단한 건강검진(전반적 服务器 상태)은 내과(top)로 충분하지만, 가슴 통증이 있다면 심장내과(APM/트랜잭션 추적)가 필요하고, 정밀 수술이 필요하면 현미경(eBPF/커널 레벨 추적)이 필요한 것이다.

---

## 4. 실무 적용 및 기술사적 판단

### 실무 시나리오: 웹 서비스Latency 증가의 Root Cause 分析

**상황**:某电商平台的网站响应速度가 周明けから遅くなり 시작했다. 利用자들은"页面加载慢"를 호소했고, Platform Engineering 팀이性能監視를 시작했다.

**분석 과정**:
1. `top`: CPU 사용률이平时 30%대에서 70%로 상승 --> CPU Possible Bottleneck!
2. `mpstat -P ALL`: 특정 코어(iowait)가 아니라 overall CPU가 全般적으로 상승
3. `pidstat -p ALL 1`: 특정 프로세스가아닌 全프로세ス均等하게 CPU ↑
4. `vmstat 1`: 메모리 가용률 20%대, 스왑 사용률 0%
5. `iostat -xz 1`: Disk %util 95%, await 80ms --> **Disk I/O가 本当の 병목!**
6. `iotop`: 전반적인 file system journal sync가 I/O를独占

**진단 결과**: 데이터베이스 Connection Pool이 풀 크기가 작아서 각 쿼리가 Disk I/O를 동반하는 랜덤 액세스를 多発的に発生시켰고, 이는 Disk %util를 치솟게 만들었다.

**대응**: DB Connection Pool 크기 확대 --> Disk I/O 감소 --> CPU Wait 감소 --> Latency恢复正常

### 도입 체크리스트

- **BASELINES 설정**: 시스템의"정상" 성능 기준선(baseline)을 설정하고, 기준선에서 크게 벗어난 경우에만 Alert를 발생시킨다.
- **Saturation 중심 Alert**: CPU Utilization보다 Load Average > 코어 수, Disk %util > 80%, Memory 스왑 사용량 > 0 등의 Saturation Metric을Alert 기준으로 설정한다.
- **Historical 데이터 보존**: `sar` 데이터를 90일 이상 보존하여, 주간/월간 트렌드 분석과事后 分析이 가능하도록 한다.

### 안티패턴

- **단일 Metric 의존**: CPU 사용률만 관찰하고 I/O 병목을 놓치는 것이 대표적인 안티패턴이다.
- **너무 세밀한 Alert**: 모든 Metric 변동에 Alert를 설정하면"Alert 피로"가 와서 실제로 중요한 Alert를 놓치게 된다.

- **요약 비유**: 성능 모니터링은소방서의119 신고 시스템과 같다. 모든 집에서火의심될 때마다 신고하면(모든 metric에 alert)消防官이 번번이 출동하므로系统이 마비되고, 반대로全く監視하지 않으면 큰불이 나도消防官이 늦게 도착한다.

---

## 5. 기대효과 및 결론

### 기대효과

성능 모니터링 체계 구축의 ROI는 故障 발생 시 平均 회복 시간(MTTR)에 의해 直接 결정된다. 구축 없을 경우 평균 장애 회복 시간이 4~8시간인 반면, 체계적 모니터링 + 사전 Alert 체계가 있으면 30분~1시간 내로 Root Cause를 파악하고 조치를 완료할 수 있어, 기업 입장에서 数万~수십만 달러의 손실을事前 방지할 수 있다.

### 참고 표준

- **USE Method (Brendan Gregg)**: 시스템 성능分析方法論
- **Google SRE Book**: 性能-budget 및 SLI/SLO/SLA 관리
- **NIST SP 800-137**: Information Security Continuous Monitoring (ISCM)

- **요약 비유**:性能모니터링은항행 중인 비행기의 실시간 ADS-B와 같다. 조종사가燃油 잔량, 엔진 상태, 고도를 지속적으로 계기판에서 확인하며異常이 있으면 미리 경고음을鸣らし,機体 전체의 상태를 中央 관제탑(모니터링 서버)에서도 동시에 파악한다.

---

## 관련 개념 맵

| 개념 명칭 | 관계 및 시너지 설명 |
|---|---|
| **Load Average** | CPU Saturation을 나타내는 핵심 지표로, Run Queue에 대기 중인 프로세스 수를 나타낸다. |
| **%iowait** | CPU가 I/O 완료 대기로 소비한 시간 비율로, CPU 병목인지 I/O 병목인지를 구별하는 핵심 지표이다. |
| **MTTR (Mean Time To Repair)** | 장애 발생 후 복구까지 평균 소요 시간으로, 성능 모니터링 체계가 잘 갖추어져 있을수록 MTTR이 크게 단축된다. |
| **SLI/SLO/SLA** | Service Level Indicator/Objective/Agreement로, 성능 모니터링의 목표치 설정 및 합의에 활용되는 표준 프레임워크이다. |

---

## 어린이를 위한 3줄 비유 설명
1.性能모니터링은학교 infirmary nurse의 건강 상태定期確認과 같아요. 매일 점심시간에 여러 학급의 마련한 아이들이 있는지(자원이 정상 범위 내인지), 열이 있는 아이는 없는지(CPU/메모리 과사용), 놀이터에서 다친 아이는 없는지(에러/탐지)를 확인하는 것이예요.
2. 그래야 아이들 사이에서 병이 퍼지기 전에(蒋포화/장애 확대) nurse가率先采取措施를 취할 수 있어요.
3. 만약 nurse가 아이들 상태를 monitoring하지 않으면, 어제 밤에 이미 열이 난 아이가 있는 줄도 모르고 등교해서全班에 퍼뜨리는 결과를 초래한다.
