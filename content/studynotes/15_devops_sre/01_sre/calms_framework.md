+++
title = "CALMS 프레임워크"
categories = ["studynotes-15_devops_sre"]
+++

# CALMS 프레임워크

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DevOps 성숙도를 평가하고 도입을 가이드하는 5대 핵심 가치 - Culture(문화), Automation(자동화), Lean(린), Measurement(측정), Sharing(공유) - 를 체계화한 모델입니다.
> 2. **가치**: 조직이 DevOps 여정에서 어디에 위치하는지 진단하고, 개선 우선순위를 설정할 수 있는 로드맵을 제공합니다.
> 3. **융합**: SRE의 SLI/SLO 체계, 애자일의 린 원칙, 그리고 학습 조직의 지식 공유 문화가 통합된 종합 프레임워크입니다.

---

## Ⅰ. 개요 (Context & Background)

CALMS 프레임워크는 2010년 Jez Humble와에 의해 제안된 DevOps 성숙도 평가 모델입니다. DevOps가 단순한 도구 도입이 아니라 문화적 변화를 요구한다는 점을 강조하며, 조직이 5가지 차원에서 자신의 위치를 진단하고 개선해 나갈 수 있도록 구조화되었습니다.

**💡 비유**: **건강 검진 5대 핵심 지표**
사람의 건강을 평가할 때 체중, 혈압, 혈당, 콜레스테롤, 운동량을 검사하듯, CALMS는 IT 조직의 건강을 5가지 차원에서 진단합니다. "혈압(자동화)이 높으니 운동(문화 변화)을 늘리고, 식단(린 원칙)을 조절하세요"와 같이 맞춤형 처방을 내릴 수 있습니다.

**등장 배경 및 발전 과정**:
1. **기존 기술의 치명적 한계점**:
   - "DevOps를 도입하라"는 말은 많지만, "어떻게 시작해야 하는가?"에 대한 가이드 부재
   - 도구만 도입하고 문화는 방치하는 "툴 천국" 현상
   - DevOps 성공 여부를 판단할 객관적 지표 부족

2. **혁신적 패러다임 변화의 시작**:
   - 2010년 Jez Humble가 "Continuous Delivery" 책에서 CALMS 개념 소개
   - 이후 DORA(DevOps Research and Assessment)에서 정량적 연구와 결합
   - 현재는 DevOps 성숙도 평가의 사실상 표준 모델

3. **현재 시장/산업의 비즈니스적 요구사항**:
   - 디지털 트랜스포메이션 프로젝트의 성공/실패 요인 분석
   - 투자 대비 효과(ROI) 측정을 위한 정량적 지표 요구
   - DevOps 도입 가이드라인으로 활용

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. CALMS 5대 핵심 구성 요소

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/도구 | 성숙도 레벨 |
|:---|:---|:---|:---|:---|
| **Culture (문화)** | 협업, 신뢰, 심리적 안전감 조성 | Blameless Post-mortem, 공동 책임 소유 | Confluence, Slack | 1~5 |
| **Automation (자동화)** | 반복 작업의 기계화, CI/CD | IaC, 파이프라인 자동화, 테스트 자동화 | Jenkins, ArgoCD, Terraform | 1~5 |
| **Lean (린)** | 낭비 제거, 작은 배치, 빠른 피드백 | WIP 제한, 가치 흐름 매핑 | Kanban, JIRA | 1~5 |
| **Measurement (측정)** | 데이터 기반 의사결정, 피드백 루프 | DORA Metrics, 비즈니스 지표 연동 | Prometheus, Grafana | 1~5 |
| **Sharing (공유)** | 지식 확산, 투명성, 학습 조건 | 문서화, 세미나, 페어 프로그래밍 | GitLab Wiki, Notion | 1~5 |

### 2. 정교한 구조 다이어그램: CALMS 성숙도 레벨

```text
================================================================================
                      [ CALMS Maturity Assessment Matrix ]
================================================================================

  Level 5: [ Optimizing ] - 지속적 혁신, 업계 리더
           ████████████████████████████████████████ 100%
           Culture: 비난 없는 문화 정착, 자율적 협업
           Automation: 완전 자동화된 E2E 파이프라인
           Lean: 낭비 제거 프로세스 지속 최적화
           Measurement: 예측 분석, AIOps 적용
           Sharing: 오픈소스 기여, 지식 공유 리더

  Level 4: [ Managed ] - 정량적 관리, 체계적 개선
           ████████████████████████████████ 80%
           Culture: 정기적 팀 회고, 협업 프로세스 정립
           Automation: 대부분 자동화, 일부 수동
           Lean: WIP 제한, 가치 흐름 시각화
           Measurement: DORA Metrics 정기 측정
           Sharing: 기술 세미나, 문서화 체계화

  Level 3: [ Defined ] - 프로세스 표준화
           ████████████████████ 60%
           Culture: 팀 간 협업 시도, 일부 갈등 존재
           Automation: CI 자동화, CD는 수동
           Lean: 스크럼/칸반 도입, 아직 미성숙
           Measurement: 일부 메트릭 수집
           Sharing: 문서화 시작, 공유 부족

  Level 2: [ Repeatable ] - 성공 사례 재현 가능
           ████████ 40%
           Culture: DevOps 챔피언 존재, 팀 일부 참여
           Automation: 일부 빌드 자동화
           Lean: 애자일 도입 논의
           Measurement: 기본 모니터링
           Sharing: 위키 시작

  Level 1: [ Initial ] - 애드혹, 비공식적
           ████ 20%
           Culture: 사일로 존재, 협업 부재
           Automation: 수동 배포, 스크립트 일부
           Lean: 폭포수 모델
           Measurement: 장애 후 대응
           Sharing: 지식 격리

  Level 0: [ None ] - DevOps 개념 미도입
           ░░ 0%
```

### 3. 심층 동작 원리

**Culture (문화) - DevOps의 토대**
1. **심리적 안전감**: 실수를 해도 비난받지 않는다는 믿음
2. **공동 책임 소유**: "내 코드", "네 서버"가 아닌 "우리 시스템"
3. **Blameless Post-mortem**: 장애 시 "왜 시스템이 이것을 막지 못했나?"에 집중

**Automation (자동화) - 속도와 일관성의 원천**
1. **CI (Continuous Integration)**: 코드 병합 -> 빌드 -> 테스트 자동화
2. **CD (Continuous Delivery/Deployment)**: 테스트 통과 -> 배포 자동화
3. **IaC (Infrastructure as Code)**: 인프라를 코드로 버전 관리

**Lean (린) - 낭비 제거와 흐름 최적화**
1. **작은 배치 크기**: 큰 릴리스를 작은 단위로 분할
2. **WIP 제한**: 동시 진행 작업 수 제한으로 병목 가시화
3. **가치 흐름 매핑**: 아이디어부터 고객 전달까지의 흐름 시각화

**Measurement (측정) - 데이터 기반 개선**
1. **DORA Metrics**: 배포 빈도, 리드 타임, 복구 시간, 실패율
2. **비즈니스 메트릭**: 사용자 만족도, 매출 영향, 비용 효율성
3. **피드백 루프**: 측정 -> 분석 -> 개선 -> 재측정 사이클

**Sharing (공유) - 학습 조직의 핵심**
1. **문서화**: 지식을 문서로 축적하고 검색 가능하게
2. **기술 세미나**: 정기적으로 팀 간 지식 공유
3. **페어 프로그래밍**: 실시간 지식 전수와 협업

### 4. CALMS 성숙도 평가 도구

```python
# calms_assessment.py - CALMS 성숙도 평가 스크립트
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class CALMSQuestion:
    dimension: str  # Culture, Automation, Lean, Measurement, Sharing
    question: str
    level: int  # 이 질문이 측정하는 성숙도 레벨 (1-5)
    weight: float = 1.0

@dataclass
class CALMSResult:
    dimension: str
    score: float  # 0.0 ~ 5.0
    level: str    # Initial, Repeatable, Defined, Managed, Optimizing
    recommendations: List[str]

class CALMSAssessment:
    def __init__(self):
        self.questions = self._initialize_questions()

    def _initialize_questions(self) -> List[CALMSQuestion]:
        """CALMS 평가 질문 초기화"""
        return [
            # Culture 질문
            CALMSQuestion("Culture", "장애 발생 시 비난 없는 회고를 실시하나요?", 3, 1.5),
            CALMSQuestion("Culture", "개발팀과 운영팀이 공동 KPI를 가지고 있나요?", 2, 1.2),
            CALMSQuestion("Culture", "모든 팀원이 심리적 안전감을 느끼나요?", 4, 1.3),

            # Automation 질문
            CALMSQuestion("Automation", "모든 빌드가 자동화되어 있나요?", 2, 1.0),
            CALMSQuestion("Automation", "CI/CD 파이프라인이 완전 자동화되어 있나요?", 4, 1.5),
            CALMSQuestion("Automation", "인프라를 코드(IaC)로 관리하나요?", 3, 1.2),

            # Lean 질문
            CALMSQuestion("Lean", "배치 크기를 작게 유지하나요 (1주 이내)?", 3, 1.0),
            CALMSQuestion("Lean", "WIP(진행 중 작업) 제한을 두나요?", 2, 1.0),
            CALMSQuestion("Lean", "가치 흐름 매핑을 수행하나요?", 4, 1.2),

            # Measurement 질문
            CALMSQuestion("Measurement", "DORA Metrics를 측정하나요?", 3, 1.5),
            CALMSQuestion("Measurement", "실시간 모니터링 대시보드가 있나요?", 2, 1.0),
            CALMSQuestion("Measurement", "비즈니스 지표와 IT 지표를 연동하나요?", 4, 1.3),

            # Sharing 질문
            CALMSQuestion("Sharing", "기술 문서가 체계적으로 관리되나요?", 2, 1.0),
            CALMSQuestion("Sharing", "정기적인 기술 세미나를 개최하나요?", 3, 1.0),
            CALMSQuestion("Sharing", "페어 프로그래밍/모브 프로그래밍을 하나요?", 4, 1.2),
        ]

    def calculate_score(self, dimension: str, answers: Dict[str, bool]) -> CALMSResult:
        """특정 차원의 성숙도 점수 계산"""
        dim_questions = [q for q in self.questions if q.dimension == dimension]
        total_weight = sum(q.weight for q in dim_questions)
        achieved_weight = sum(
            q.weight for q in dim_questions
            if answers.get(q.question, False)
        )
        score = (achieved_weight / total_weight) * 5.0

        # 레벨 결정
        if score >= 4.5:
            level = "Optimizing"
        elif score >= 3.5:
            level = "Managed"
        elif score >= 2.5:
            level = "Defined"
        elif score >= 1.5:
            level = "Repeatable"
        else:
            level = "Initial"

        # 개선 권장사항 생성
        recommendations = self._generate_recommendations(dimension, score, answers)

        return CALMSResult(
            dimension=dimension,
            score=score,
            level=level,
            recommendations=recommendations
        )

    def _generate_recommendations(
        self,
        dimension: str,
        score: float,
        answers: Dict[str, bool]
    ) -> List[str]:
        """차원별 개선 권장사항 생성"""
        recommendations = {
            "Culture": [
                "Blameless Post-mortem 문화 도입을 시작하세요",
                "개발/운영 공동 KPI 설정 워크샵을 진행하세요",
                "심리적 안전감 설문조사를 정기적으로 실시하세요"
            ],
            "Automation": [
                "CI 파이프라인 자동화부터 시작하세요",
                "주요 테스트를 자동화하고 커버리지를 높이세요",
                "Terraform/Ansible을 활용한 IaC를 도입하세요"
            ],
            "Lean": [
                "배치 크기를 1주 이내로 줄이세요",
                "칸반 보드에 WIP 제한을 설정하세요",
                "가치 흐름 매핑 워크샵을 진행하세요"
            ],
            "Measurement": [
                "DORA Metrics 대시보드를 구축하세요",
                "Prometheus/Grafana로 모니터링 체계를 구축하세요",
                "비즈니스 지표와 IT 지표를 연동하세요"
            ],
            "Sharing": [
                "기술 문서화 프로세스를 표준화하세요",
                "월간 기술 세미나를 시작하세요",
                "핵심 프로젝트에 페어 프로그래밍을 도입하세요"
            ]
        }
        return recommendations.get(dimension, [])

# 사용 예시
if __name__ == "__main__":
    assessment = CALMSAssessment()

    # 예시 답변
    sample_answers = {
        "장애 발생 시 비난 없는 회고를 실시하나요?": True,
        "개발팀과 운영팀이 공동 KPI를 가지고 있나요?": True,
        "모든 빌드가 자동화되어 있나요?": True,
        "CI/CD 파이프라인이 완전 자동화되어 있나요?": False,
        "DORA Metrics를 측정하나요?": True,
    }

    # 각 차원별 평가
    for dimension in ["Culture", "Automation", "Lean", "Measurement", "Sharing"]:
        result = assessment.calculate_score(dimension, sample_answers)
        print(f"\n{dimension}: {result.score:.2f} ({result.level})")
        for rec in result.recommendations[:2]:
            print(f"  - {rec}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: DevOps 성숙도 모델 비교

| 모델명 | 차원 수 | 특징 | 장점 | 단점 | 적용 환경 |
|:---|:---|:---|:---|:---|:---|
| **CALMS** | 5개 | 문화 중심, 포괄적 | 균형 잡힌 평가 | 정량화 어려움 | 모든 조직 |
| **DORA Metrics** | 4개 지표 | 성과 중심, 정량적 | 데이터 기반 | 문화 간과 | 성숙한 DevOps |
| **CMMI** | 5레벨 | 프로세스 중심 | 인증 가능 | 무거움 | 대기업 |
| **Agile Maturity** | 5레벨 | 애자일 실천 중심 | 개발 중심 | 운영 배제 | 개발팀 |

### 2. 과목 융합 관점 분석

**CALMS + SRE**:
- Culture: Blameless Post-mortem, 에러 버짯 수용
- Automation: 토일(Toil) 자동화, 자가 치유 시스템
- Lean: SLO 기반 우선순위 결정
- Measurement: SLI/SLO/SLA 체계
- Sharing: 런북(Runbook) 공유, 온콜 교대 지식 전수

**CALMS + 클라우드 네이티브**:
- Culture: "You build it, you run it" 책임 모델
- Automation: GitOps, IaC, 컨테이너 오케스트레이션
- Lean: 마이크로서비스별 독립 배포
- Measurement: Observability 3대 기둥
- Sharing: 서비스 메시 텔레메트리 공유

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

**시나리오: 중견 기업의 CALMS 기반 DevOps 진단**
- **상황**: DevOps 도입 1년 차, 투자 효과 불확실, 개선 방향 모호
- **기술사의 전략적 의사결정**:
  1. **진단**: CALMS 설문조사 실시, 현재 성숙도 Level 2 (Repeatable) 확인
  2. **우선순위**: Culture(2.0)와 Measurement(1.8)가 가장 낮음 -> 집중 개선
  3. **액션 플랜**:
     - Culture: 월간 Blameless Post-mortem 정착, 공동 KPI 설정
     - Measurement: DORA Metrics 대시보드 구축
  4. **재측정**: 6개월 후 재진단, Level 3 (Defined) 달성 목표

### 2. 도입 시 고려사항 (체크리스트)

**CALMS 도입 체크리스트**:
- [ ] 경영진 후원 및 예산 확보
- [ ] 현재 상태 베이스라인 측정
- [ ] 개선 목표(SMART) 설정
- [ ] 정기 재측정 일정 (분기별 권장)
- [ ] 개선 액션 아이템 추적 시스템

### 3. 주의사항 및 안티패턴 (Anti-patterns)

**안티패턴 1: 한 번만 측정**
- 문제: "CALMS 점수 3.2 나왔다"고 만족하고 끝
- 해결: 정기적 재측정으로 개선 추이 추적

**안티패턴 2: 한 차원에만 집중**
- 문제: "자동화만 하면 된다"는 생각
- 해결: 5대 차원의 균형 잡힌 개선

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| CALMS 레벨 | 배포 빈도 | 리드 타임 | 복구 시간 | 실패율 |
|:---|:---|:---|:---|:---|
| **Level 1 (Initial)** | 연 1~2회 | 수개월 | 수일 | 40%+ |
| **Level 3 (Defined)** | 월 1~2회 | 1~2주 | 수시간 | 15~25% |
| **Level 5 (Optimizing)** | 일일 수회 | 1시간 이내 | 수분 | 5% 미만 |

### 2. 미래 전망 및 진화 방향

- **AI 기반 CALMS 평가**: 자동화된 데이터 수집으로 객관적 평가
- **실시간 성숙도 대시보드**: 지속적인 조직 건강 상태 모니터링
- **업계 벤치마킹**: 타 기업과의 CALMS 점수 비교

### 3. 참고 표준/가이드

- **DORA State of DevOps Report**: CALMS 기반 연례 조사
- **The DevOps Handbook**: CALMS 실천법 가이드
- **Accelerate (Nicole Forsgren)**: CALMS 정량적 연구

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [DevOps (데브옵스) 사상](@/studynotes/15_devops_sre/01_sre/devops_culture.md) : CALMS가 측정하는 핵심 철학
- [DORA Metrics](@/studynotes/15_devops_sre/01_sre/dora_metrics.md) : CALMS의 Measurement 차원 핵심 지표
- [CI/CD Pipeline & GitOps](@/studynotes/15_devops_sre/03_automation/cicd_gitops.md) : CALMS의 Automation 차원 구현
- [린 IT (Lean IT)](@/studynotes/15_devops_sre/01_sre/lean_it.md) : CALMS의 Lean 차원 기반 이론
- [Blameless Post-mortem](@/studynotes/15_devops_sre/01_sre/blameless_postmortem.md) : CALMS의 Culture 차원 핵심 실천법

---

## 👶 어린이를 위한 3줄 비유 설명

1. CALMS는 **학교 성적표**와 같아요. 국어, 영어, 수학, 과학, 사회처럼 5가지 과목(문화, 자동화, 린, 측정, 공유)을 검사해요.
2. 각 과목마다 **1점부터 5점까지** 점수를 매겨서, 우리 팀이 어디를 더 공부해야 하는지 알려줘요.
3. 이렇게 정기적으로 검사하면 **점점 더 똑똑한 팀**이 되어서, 멋진 프로그램을 더 빨리 만들 수 있어요!
