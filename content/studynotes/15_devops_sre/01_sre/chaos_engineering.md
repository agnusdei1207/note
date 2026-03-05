+++
title = "카오스 엔지니어링 (Chaos Engineering)"
categories = ["studynotes-15_devops_sre"]
+++

# 카오스 엔지니어링 (Chaos Engineering)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 프로덕션 시스템에 의도적으로 장애(서버 종료, 네트워크 지연, CPU 폭주 등)를 주입하여, 시스템의 회복 탄력성(Resilience)과 장애 대응 체계가 실제 위기 상황에서 정상 작동하는지 검증하는 엔지니어링 방법론입니다.
> 2. **가치**: 장애가 실제 발생하기 전에 약점을 선제적으로 발견하고, "장애를 경험하며 학습"하여 시스템 신뢰성을 지속적으로 향상시킵니다.
> 3. **융합**: SRE 에러 버짯, 옵저버빌리티, 그리고 CI/CD 파이프라인과 결합하여 자동화된 회복 탄력성 테스트 체계를 구축합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)

**카오스 엔지니어링(Chaos Engineering)**은 분산 시스템이 견딜 수 있는 불확실성과 혼란(Chaos)을 실험적으로 검증하는 분야입니다. 핵심은 "시스템이 프로덕션 환경에서 견디는 능력을 신뢰하려면, 시스템을 혼란스럽게 만들어봐야 한다"는 것입니다.

**카오스 엔지니어링의 4가지 원칙**:
1. **정상 상태(Steady State) 정의**: 시스템의 정상 동작을 측정 가능한 지표로 정의
2. **가설 수립**: "이 혼란을 주입해도 정상 상태가 유지될 것이다"
3. **실제 환경에서 실험**: 프로덕션 또는 프로덕션과 유사한 환경
4. **자동화**: 지속적이고 자동화된 실험

### 2. 구체적인 일상생활 비유

**소방 훈련**으로 비유해 봅시다.

건물에 불이 났을 때 소방 훈련을 안 했다면 어떻게 될까요?
- 비상구를 못 찾아서
- 소화기 사용법을 몰라서
- 대피 질서가 없어서

소방 훈련은 **의도적으로 "가짜 불"을 낸 상황**을 연출하여, 실제 화재 발생 시 모두가 안전하게 대피할 수 있는지 검증합니다.

카오스 엔지니어링도 같습니다. **"가짜 장애"를 주입**하여, 실제 장애 발생 시 시스템이 견딜 수 있는지 미리 테스트합니다.

### 3. 등장 배경 및 발전 과정

**1단계: 기존 기술의 치명적 한계점**
- 분산 시스템의 복잡성: "모든 것이 언젠가는 실패한다"
- 테스트 환경과 프로덕션 환경의 차이
- 예상치 못한 장애 전파 (Cascading Failure)
- 장애 발생 후에야 약점을 발견

**2단계: 혁신적 패러다임 변화**
- 2010년: 넷플릭스가 AWS로 이전하며 "Chaos Monkey" 개발
- 철학: "장애가 발생하면 놀라지 말고, 장애가 발생하지 않으면 놀라라"
- 2014년: "Principles of Chaos Engineering" 발표
- 현재: Chaos Monkey, Chaos Mesh, Gremlin, Litmus 등 다양한 도구

**3단계: 현재 시장/산업의 비즈니스적 요구사항**
- MSA/Kubernetes 환경의 복잡성 증가
- 무중단 서비스 요구사항 (99.99% SLA)
- 클라우드 장애로부터의 빠른 복구
- 재해 복구(DR) 훈련의 자동화

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 카오스 엔지니어링 핵심 구성 요소

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 대표 도구 | 비유 |
|:---|:---|:---|:---|:---|
| **Chaos Controller** | 실험 오케스트레이션 | 실험 정의, 스케줄링, 실행 | Chaos Mesh, Litmus | 소방 훈련 관리자 |
| **Fault Injector** | 장애 주입 | Pod Kill, Network Delay, CPU Stress | Chaos Monkey, Gremlin | 가짜 불 |
| **Steady State Monitor** | 정상 상태 모니터링 | SLO 위반 감지, 알림 | Prometheus, Grafana | 화재 감지기 |
| **Blast Radius Controller** | 영향 범위 제한 | 네임스페이스, 라벨 기반 격리 | Network Policy | 방화벽 |
| **Rollback Mechanism** | 자동 복구 | 실험 실패 시 자동 중단 | Kubernetes | 스프링클러 |

### 2. 정교한 구조 다이어그램: 카오스 엔지니어링 실험 흐름

```text
================================================================================
                   [ Chaos Engineering Experiment Flow ]
================================================================================

    [ Phase 1: 실험 계획 (Experiment Planning) ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   [ 정상 상태(Steady State) 정의 ]                                       │
    │   ┌────────────────────────────────────────────────────────────────┐    │
    │   │ SLO: API 응답 시간 P95 < 200ms                                 │    │
    │   │ SLO: 에러율 < 0.1%                                             │    │
    │   │ SLO: 가용성 > 99.9%                                            │    │
    │   └────────────────────────────────────────────────────────────────┘    │
    │                                    │                                    │
    │                                    ▼                                    │
    │   [ 가설(Hypothesis) 수립 ]                                              │
    │   ┌────────────────────────────────────────────────────────────────┐    │
    │   │ "결제 서비스 Pod 1개가 종료되어도, 트래픽은 정상 처리될 것이다"  │    │
    │   │ 이유: HPA가 최소 3개 Pod를 유지하고, 로드밸런서가 라우팅        │    │
    │   └────────────────────────────────────────────────────────────────┘    │
    │                                    │                                    │
    │                                    ▼                                    │
    │   [ 폭발 반경(Blast Radius) 정의 ]                                       │
    │   ┌────────────────────────────────────────────────────────────────┐    │
    │   │ 대상: payment-service 네임스페이스                              │    │
    │   │ 종류: Pod Kill 1개                                             │    │
    │   │ 시간: 업무 시간 (10:00-18:00) 중, 트래픽 낮은 시간             │    │
    │   │ 중단 조건: 에러율 > 1% 시 즉시 실험 중단                        │    │
    │   └────────────────────────────────────────────────────────────────┘    │
    │                                                                          │
    └──────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
    [ Phase 2: 실험 실행 (Experiment Execution) ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   [ Before: 정상 상태 측정 ]                                             │
    │   ┌────────────────────────────────────────────────────────────────┐    │
    │   │ Pod 수: 3개 (payment-service-xxx, yyy, zzz)                    │    │
    │   │ P95 응답: 150ms                                                │    │
    │   │ 에러율: 0.02%                                                  │    │
    │   └────────────────────────────────────────────────────────────────┘    │
    │                                    │                                    │
    │                                    ▼                                    │
    │   [ Chaos 주입: Pod Kill ]                                               │
    │   ┌────────────────────────────────────────────────────────────────┐    │
    │   │                                                                │    │
    │   │   T+0s: Chaos Monkey가 payment-service-xxx Pod 삭제            │    │
    │   │         ┌──────────────────┐                                   │    │
    │   │         │ payment-service  │ ← KILL!                           │    │
    │   │         │   -xxx           │                                   │    │
    │   │         └──────────────────┘                                   │    │
    │   │                                                                │    │
    │   │   T+1s: 서비스 디스커버리가 Pod 제거 감지                       │    │
    │   │   T+2s: 로드밸런서가 새 Pod로 라우팅                           │    │
    │   │   T+5s: HPA가 Pod 부족 감지                                    │    │
    │   │   T+30s: 새 Pod(payment-service-www) 시작                      │    │
    │   │   T+60s: 새 Pod Ready 상태                                     │    │
    │   │                                                                │    │
    │   └────────────────────────────────────────────────────────────────┘    │
    │                                    │                                    │
    │                                    ▼                                    │
    │   [ During: 실시간 모니터링 ]                                            │
    │   ┌────────────────────────────────────────────────────────────────┐    │
    │   │                                                                │    │
    │   │   Prometheus Dashboard                                         │    │
    │   │   ┌────────────────────────────────────────────────────┐      │    │
    │   │   │ P95 Latency: 150ms → 180ms → 160ms → 150ms        │      │    │
    │   │   │ Error Rate:  0.02% → 0.1%  → 0.05% → 0.02%        │      │    │
    │   │   │ Pod Count:   3 → 2 → 3                            │      │    │
    │   │   └────────────────────────────────────────────────────┘      │    │
    │   │                                                                │    │
    │   │   ⚠️ 중단 조건 (에러율 > 1%): 미달성 → 실험 계속               │    │
    │   │                                                                │    │
    │   └────────────────────────────────────────────────────────────────┘    │
    │                                                                          │
    └──────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
    [ Phase 3: 결과 분석 (Result Analysis) ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   [ 가설 검증 ]                                                          │
    │   ┌────────────────────────────────────────────────────────────────┐    │
    │   │ 가설: "Pod 1개 종료 시에도 정상 처리"                           │    │
    │   │ 결과: ✅ 검증됨                                                │    │
    │   │ - P95 응답: 150ms → 180ms (SLO < 200ms 충족)                   │    │
    │   │ - 에러율: 0.02% → 0.1% (SLO < 0.1% 충족)                       │    │
    │   │ - 복구 시간: 60초                                              │    │
    │   └────────────────────────────────────────────────────────────────┘    │
    │                                    │                                    │
    │                                    ▼                                    │
    │   [ 발견된 약점 및 개선 사항 ]                                           │
    │   ┌────────────────────────────────────────────────────────────────┐    │
    │   │ - P95가 일시적으로 180ms까지 증가 → 최소 Pod 수 3→4로 증권 권장  │    │
    │   │ - Pod 시작 시간 30초 → 최적화 필요 (Init Container 제거 등)     │    │
    │   │ - 새 Pod Ready까지 60초 소요 → Readiness Probe 개선 필요        │    │
    │   └────────────────────────────────────────────────────────────────┘    │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘

    [ 장애 유형(Fault Types) 매트릭스 ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   ┌──────────────────────────────────────────────────────────────────┐  │
    │   │                    [ Chaos Fault Types ]                         │  │
    │   ├──────────────────────────────────────────────────────────────────┤  │
    │   │                                                                  │  │
    │   │   [ Compute ]           [ Network ]          [ Storage ]         │  │
    │   │   - Pod Kill            - Latency           - Disk Full         │  │
    │   │   - Node Shutdown       - Packet Loss       - I/O Delay         │  │
    │   │   - CPU Stress          - DNS Failure       - Disk Corruption   │  │
    │   │   - Memory Stress       - Connection Drop                      │  │
    │   │   - Process Kill        - Firewall Block                      │  │
    │   │                                                                  │  │
    │   │   [ Application ]       [ Cloud Provider ]   [ Time ]           │  │
    │   │   - Exception Throw     - AZ Failure        - Clock Skew        │  │
    │   │   - Dependency Fail     - Region Failure    - Leap Second       │  │
    │   │   - Config Change       - API Rate Limit                       │  │
    │   │   - Feature Toggle      - Certificate Expire                    │  │
    │   │                                                                  │  │
    │   └──────────────────────────────────────────────────────────────────┘  │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
```

### 3. 실무 코드: Chaos Mesh 실험 정의

```yaml
# pod-kill-experiment.yaml - Kubernetes Chaos Mesh 실험 정의
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: payment-service-pod-kill
  namespace: chaos-testing
  labels:
    experiment: payment-resilience-test
spec:
  action: pod-kill           # 장애 유형: Pod 종료
  mode: one                  # 1개 Pod만 종료
  selector:
    namespaces:
      - production
    labelSelectors:
      app: payment-service   # 타겟 서비스
  scheduler:
    cron: "0 10 * * 1-5"     # 평일 오전 10시 실행
  duration: "30s"            # 실험 지속 시간

---
# network-delay-experiment.yaml - 네트워크 지연 실험
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: payment-db-latency
  namespace: chaos-testing
spec:
  action: delay
  mode: all
  selector:
    namespaces:
      - production
    labelSelectors:
      app: payment-service
  delay:
    latency: "100ms"         # 100ms 지연 주입
    correlation: "50"        # 50% 상관관계
    jitter: "10ms"           # 10ms 지터
  direction: to              # 송신 트래픽에만 적용
  target:
    selector:
      namespaces:
        - production
      labelSelectors:
        app: mysql           # DB로 향하는 트래픽
  duration: "5m"

---
# stress-ng-experiment.yaml - CPU/메모리 스트레스 실험
apiVersion: chaos-mesh.org/v1alpha1
kind: StressChaos
metadata:
  name: payment-cpu-stress
  namespace: chaos-testing
spec:
  mode: one
  selector:
    namespaces:
      - production
    labelSelectors:
      app: payment-service
  stressors:
    cpu:
      workers: 4             # 4개 CPU 워커
      load: 80               # 80% 부하
  duration: "2m"

---
# 실험 결과 검증을 위한 Probes
apiVersion: chaos-mesh.org/v1alpha1
kind: Workflow
metadata:
  name: payment-resilience-workflow
  namespace: chaos-testing
spec:
  entry: entry
  templates:
    - name: entry
      templateType: Serial
      deadline: 10m
      children:
        - check-steady-state
        - inject-chaos
        - verify-recovery

    - name: check-steady-state
      templateType: HTTP
      deadline: 1m
      http:
        url: http://payment-service/health
        method: GET
        expectedStatus: 200

    - name: inject-chaos
      templateType: PodChaos
      deadline: 2m
      podChaos:
        action: pod-kill
        mode: one
        selector:
          namespaces:
            - production
          labelSelectors:
            app: payment-service

    - name: verify-recovery
      templateType: HTTP
      deadline: 2m
      http:
        url: http://payment-service/health
        method: GET
        expectedStatus: 200
        retry:
          maxRetry: 5
          duration: 10s
```

### 4. Python으로 구현한 카오스 실험 프레임워크

```python
#!/usr/bin/env python3
"""
카오스 엔지니어링 실험 프레임워크
"""

import asyncio
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Callable, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FaultType(Enum):
    POD_KILL = "pod_kill"
    CPU_STRESS = "cpu_stress"
    MEMORY_STRESS = "memory_stress"
    NETWORK_LATENCY = "network_latency"
    NETWORK_LOSS = "network_loss"
    DISK_IO_DELAY = "disk_io_delay"

class ExperimentStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    ABORTED = "aborted"

@dataclass
class SteadyStateCondition:
    """정상 상태 조건"""
    name: str
    check_fn: Callable[[], bool]
    description: str

@dataclass
class BlastRadius:
    """폭발 반경 정의"""
    namespace: str
    label_selector: str
    max_percentage: int  # 최대 영향 비율
    time_window: str     # 실행 가능 시간

@dataclass
class AbortCondition:
    """중단 조건"""
    metric_name: str
    threshold: float
    comparison: str  # "gt", "lt", "eq"

class ChaosExperiment:
    """카오스 실험 클래스"""

    def __init__(
        self,
        name: str,
        fault_type: FaultType,
        blast_radius: BlastRadius,
        duration: timedelta,
        steady_state_conditions: List[SteadyStateCondition],
        abort_conditions: List[AbortCondition]
    ):
        self.name = name
        self.fault_type = fault_type
        self.blast_radius = blast_radius
        self.duration = duration
        self.steady_state_conditions = steady_state_conditions
        self.abort_conditions = abort_conditions
        self.status = ExperimentStatus.PENDING
        self.start_time: Optional[datetime] = None
        self.results = {}

    def validate_blast_radius(self) -> bool:
        """폭발 반경 검증"""
        # 실행 가능 시간 확인
        now = datetime.now()
        time_window = self.blast_radius.time_window
        # 예: "10:00-18:00" 파싱 및 검증
        return True  # 간소화

    async def check_steady_state(self) -> bool:
        """정상 상태 확인"""
        for condition in self.steady_state_conditions:
            if not condition.check_fn():
                logger.warning(f"Steady state condition failed: {condition.name}")
                return False
        return True

    async def check_abort_conditions(self) -> bool:
        """중단 조건 확인"""
        for condition in self.abort_conditions:
            current_value = await self._get_metric(condition.metric_name)

            if condition.comparison == "gt" and current_value > condition.threshold:
                logger.warning(f"Abort condition triggered: {condition.metric_name} > {condition.threshold}")
                return True
            elif condition.comparison == "lt" and current_value < condition.threshold:
                logger.warning(f"Abort condition triggered: {condition.metric_name} < {condition.threshold}")
                return True

        return False

    async def _get_metric(self, metric_name: str) -> float:
        """메트릭 조회 (Prometheus API 연동)"""
        # 실제 구현에서는 Prometheus API 호출
        return random.uniform(0, 1)  # 간소화

    async def inject_fault(self):
        """장애 주입"""
        logger.info(f"Injecting fault: {self.fault_type.value}")

        if self.fault_type == FaultType.POD_KILL:
            await self._inject_pod_kill()
        elif self.fault_type == FaultType.CPU_STRESS:
            await self._inject_cpu_stress()
        elif self.fault_type == FaultType.NETWORK_LATENCY:
            await self._inject_network_latency()
        # ... 기타 장애 유형

    async def _inject_pod_kill(self):
        """Pod 종료 장애 주입"""
        # Kubernetes API 호출
        logger.info(f"Killing pod in {self.blast_radius.namespace} with selector {self.blast_radius.label_selector}")
        # kubectl delete pod --selector=app=payment-service --namespace=production

    async def _inject_cpu_stress(self):
        """CPU 스트레스 장애 주입"""
        logger.info("Injecting CPU stress")
        # stress-ng 또는 Kubernetes StressChaos 적용

    async def _inject_network_latency(self):
        """네트워크 지연 장애 주입"""
        logger.info("Injecting network latency")
        # tc (traffic control) 또는 NetworkChaos 적용

    async def run(self) -> dict:
        """실험 실행"""
        logger.info(f"Starting chaos experiment: {self.name}")

        # 1. 폭발 반경 검증
        if not self.validate_blast_radius():
            self.status = ExperimentStatus.ABORTED
            return {"status": "aborted", "reason": "Invalid blast radius"}

        # 2. 실험 전 정상 상태 확인
        if not await self.check_steady_state():
            self.status = ExperimentStatus.ABORTED
            return {"status": "aborted", "reason": "System not in steady state"}

        self.status = ExperimentStatus.RUNNING
        self.start_time = datetime.now()

        try:
            # 3. 장애 주입
            await self.inject_fault()

            # 4. 실험 기간 동안 모니터링
            end_time = self.start_time + self.duration
            while datetime.now() < end_time:
                # 중단 조건 확인
                if await self.check_abort_conditions():
                    self.status = ExperimentStatus.ABORTED
                    logger.warning("Experiment aborted due to abort condition")
                    break

                # 정상 상태 유지 확인
                steady = await self.check_steady_state()
                self.results["steady_state_maintained"] = steady

                await asyncio.sleep(10)  # 10초마다 확인

            # 5. 실험 완료 후 검증
            if self.status == ExperimentStatus.RUNNING:
                final_steady = await self.check_steady_state()
                self.status = ExperimentStatus.SUCCESS if final_steady else ExperimentStatus.FAILED

        except Exception as e:
            self.status = ExperimentStatus.FAILED
            logger.error(f"Experiment failed: {e}")
            self.results["error"] = str(e)

        finally:
            # 6. 정리 (장애 복구)
            await self.cleanup()

        self.results["status"] = self.status.value
        self.results["duration"] = (datetime.now() - self.start_time).total_seconds()

        return self.results

    async def cleanup(self):
        """실험 후 정리"""
        logger.info("Cleaning up chaos experiment")
        # 장애 주입 해제, 리소스 복구 등


# 사용 예시
async def main():
    # 정상 상태 조건 정의
    def check_latency():
        # 실제로는 Prometheus 쿼리
        return random.uniform(0, 300) < 200  # P95 < 200ms

    def check_error_rate():
        # 실제로는 Prometheus 쿼리
        return random.uniform(0, 5) < 1  # 에러율 < 1%

    # 실험 정의
    experiment = ChaosExperiment(
        name="payment-service-pod-kill",
        fault_type=FaultType.POD_KILL,
        blast_radius=BlastRadius(
            namespace="production",
            label_selector="app=payment-service",
            max_percentage=33,  # 최대 1/3 종료
            time_window="10:00-18:00"
        ),
        duration=timedelta(minutes=5),
        steady_state_conditions=[
            SteadyStateCondition("latency_p95", check_latency, "P95 latency < 200ms"),
            SteadyStateCondition("error_rate", check_error_rate, "Error rate < 1%")
        ],
        abort_conditions=[
            AbortCondition("error_rate", 5.0, "gt"),  # 에러율 > 5%
            AbortCondition("latency_p99", 5000.0, "gt")  # P99 > 5s
        ]
    )

    # 실험 실행
    results = await experiment.run()
    print(f"Experiment results: {results}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 카오스 엔지니어링 도구

| 도구 | 개발사 | 특징 | 적합 환경 | 비고 |
|:---|:---|:---|:---|:---|
| **Chaos Monkey** | Netflix | 무작위 Pod 종료 | AWS/Spinnaker | 최초 도구 |
| **Chaos Mesh** | PingCAP | K8s 네이티브, 다양한 장애 유형 | Kubernetes | CNCF 프로젝트 |
| **Litmus** | Mayadata | 커뮤니티 기반, 실험 라이브러리 | Kubernetes | CNCF 프로젝트 |
| **Gremlin** | Gremlin | 상용, GUI, 안전 기능 강화 | 멀티 플랫폼 | Enterprise |
| **ChaosBlade** | Alibaba | 다양한 장애 시나리오 | 멀티 플랫폼 | 오픈소스 |
| **AWS FIS** | AWS | AWS 통합, 관리형 | AWS | Cloud Native |

### 2. 과목 융합 관점 분석

**카오스 엔지니어링 + SRE**:
- 에러 버짯 내에서만 실험 실행
- SLO 위반 시 자동 실험 중단
- Post-mortem과 연계한 학습

**카오스 엔지니어링 + CI/CD**:
- 배포 전 자동 회복 탄력성 테스트
- 카나리 배포와 결합한 게이트
- Infrastructure as Code로 실험 정의

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

**시나리오: 대규모 이커머스의 카오스 엔지니어링 도입**
- **상황**: 블랙프라이데이 대비, 시스템 회복 탄력성 검증 필요
- **기술사의 전략적 의사결정**:
  1. **단계적 도입**: 개발 → 스테이징 → 프로덕션
  2. **폭발 반경 제어**: 1% 트래픽만 영향
  3. **게임데이(Game Day)**: 정기적 장애 대응 훈련
  4. **자동화**: CI/CD 파이프라인에 통합

### 2. 도입 시 고려사항 (체크리스트)

**조직적 체크리스트**:
- [ ] 경영진 승인 및 비상 연락망 구축
- [ ] Game Day 스케줄 수립
- [ ] Blameless 문화 정착

**기술적 체크리스트**:
- [ ] 옵저버빌리티 체계 완비
- [ ] 자동 복구 메커니즘 (HPA, PDB)
- [ ] 중단 조건(SLO 위반) 자동화

### 3. 주의사항 및 안티패턴

**안티패턴 1: 프로덕션에서 바로 시작**
- 문제: 예상치 못한 대규모 장애
- 해결: 개발/스테이징에서 충분히 테스트 후 프로덕션

**안티패턴 2: 폭발 반경 미제어**
- 문제: 전체 서비스 마비
- 해결: 네임스페이스 격리, 퍼센티지 제한

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **장애 대응 시간** | 2시간 | 30분 | 75% 단축 |
| **미발견 약점** | 장애 시 발견 | 사전 발견 | 예방 가능 |
| **팀 자신감** | 낮음 | 높음 | 장애 두려움 감소 |

### 2. 미래 전망 및 진화 방향

**자율 카오스 엔지니어링**:
- AI 기반 약점 자동 탐지
- 자동화된 실험 생성
- 지속적 회복 탄력성 검증

### 3. 참고 표준/가이드

- **Principles of Chaos Engineering**: chaosexperiments.com
- **Netflix Chaos Monkey**: github.com/Netflix/chaosmonkey
- **Chaos Mesh**: chaos-mesh.org

---

## 관련 개념 맵 (Knowledge Graph)

- [SRE 원칙](@/studynotes/15_devops_sre/01_sre/sre_principles.md) : 카오스 엔지니어링의 철학적 기반
- [에러 버짯](@/studynotes/15_devops_sre/01_sre/error_budget.md) : 실험 실행 허용 범위
- [옵저버빌리티](@/studynotes/15_devops_sre/02_observability/observability_fundamentals.md) : 실험 결과 모니터링
- [서킷 브레이커](@/studynotes/15_devops_sre/03_automation/circuit_breaker.md) : 장애 격리 패턴
- [무비난 포스트모템](@/studynotes/15_devops_sre/01_sre/blameless_postmortem.md) : 실험 실패 시 학습

---

## 어린이를 위한 3줄 비유 설명

1. 카오스 엔지니어링은 **소방 훈련**과 같아요. 진짜 불이 나기 전에 연습해 보는 거죠.
2. "컴퓨터가 고장 나면 어떻게 될까?"를 **일부러 고장 내서 테스트**해 봐요.
3. 덕분에 진짜로 고장 났을 때 **당황하지 않고 빠르게 고칠 수 있어요**!
