+++
title = "토일 (Toil) 및 자동화 전략"
categories = ["studynotes-15_devops_sre"]
+++

# 토일 (Toil) 및 자동화 전략

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Toil(토일)은 반복적이고, 수동이며, 자동화 가능하고, 가치를 창출하지 않는 운영 업무로, SRE 팀은 이를 50% 미만으로 유지하여 엔지니어링 작업에 시간을 확보해야 합니다.
> 2. **가치**: 토일 제거는 엔지니어 번아웃 방지, 시스템 안정성 향상, 그리고 혁신적 기능 개발로 이어지는 핵심 SRE 실천법입니다.
> 3. **융합**: CI/CD 파이프라인, IaC(Infrastructure as Code), 그리고 Operator 패턴과 결합하여 완전 자동화된 운영 체계를 구축합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)

**토일(Toil)**은 구글 SRE에서 정의한 개념으로, 다음 5가지 특성을 모두 만족하는 운영 업무를 의미합니다:

1. **반복적(Manual)**: 매번 동일한 작업을 반복
2. **자동화 가능(Automatable)**: 스크립트나 코드로 대체 가능
3. **무상태성(Ephemeral)**: 완료 후에도 지속적 가치를 남기지 않음
4. **선형적 성장(Linear Growth)**: 서비스 규모와 비례하여 증가
5. **낮은 가치(Low Value)**: 장기적 개선이나 혁신에 기여하지 않음

SRE의 핵심 원칙은 **"토일을 50% 미만으로 유지하라"**는 것입니다. 이를 통해 엔지니어링 시간(코드 작성, 시스템 개선, 자동화)을 확보합니다.

### 2. 구체적인 일상생활 비유

**식당 설거지**로 비유해 봅시다.

- **토일 (설거지)**: 손님들이 식사를 할 때마다 접시가 쌓이고, 매번 손으로 씻어야 합니다. 아무리 열심히 씻어도 내일 또 씻어야 하고, 요리 실력은 늘지 않습니다.
- **엔지니어링 (요리 연구)**: 새로운 레시피를 개발하거나, 식당 운영 시스템을 개선하는 작업입니다. 이것이 진정한 가치 창출입니다.
- **자동화 (식기세척기)**: 설거지 기계를 도입하면 요리사는 요리 연구에 집중할 수 있습니다.

### 3. 등장 배경 및 발전 과정

**1단계: 기존 기술의 치명적 한계점**
- 전통적 운영팀은 70-90% 시간을 반복적 수작업에 소비
- 야간 당직, 수동 배포, 장애 대응으로 인한 엔지니어 번아웃
- 서비스 성장에 따라 운영 인력이 선형적으로 증가하는 비효율

**2단계: 혁신적 패러다임 변화**
- 구글이 "소프트웨어 엔지니어가 운영을 맡으면 어떻게 될까?"라는 질문에서 SRE 탄생
- "문제를 해결하는 대신, 문제를 없애라"는 철학
- 토일을 50% 미만으로 유지하면 엔지니어링으로 시스템이 개선되는 선순환

**3단계: 현재 시장/산업의 비즈니스적 요구사항**
- 클라우드 네이티브 환경에서 수백 개 마이크로서비스 운영
- 수동 운영으로는 불가능한 규모 확장성 요구
- Platform Engineering으로 발전하여 개발자 셀프 서비스 실현

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 토일 분류 및 구성 요소

| 토일 유형 | 구체적 사례 | 자동화 방법 | 예상 절감 시간 | 비고 |
|:---|:---|:---|:---|:---|
| **배포 관련** | 수동 릴리스, 롤백 | CI/CD 파이프라인 | 80% | ArgoCD, Jenkins |
| **모니터링** | 대시보드 수동 갱신 | Grafana as Code | 60% | Grafonnet, Jsonnet |
| **인시던트** | 장애 티켓 수동 생성 | SOAR, PagerDuty | 50% | 자동 에스컬레이션 |
| **백업/복구** | 수동 DB 백업 | Operator Pattern | 90% | CronJob, Velero |
| **보안 패치** | 수동 CVE 대응 | Dependabot, Renovate | 70% | 자동 PR 생성 |
| **리포팅** | 주간 보고서 작성 | 자동화된 메트릭 리포트 | 80% | Grafana Alerts |
| **온보딩** | 신규 서버 설정 | IaC, Terraform | 85% | Golden Path |

### 2. 정교한 구조 다이어그램: 토일 제거 피드백 루프

```text
================================================================================
                      [ Toil Reduction Feedback Loop ]
================================================================================

    [ Phase 1: 토일 식별 (Toil Identification) ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   [ 엔지니어 활동 로그 ] ──> [ 토일 분류 알고리즘 ] ──> [ 토일 목록 ]    │
    │                                                                          │
    │   분류 기준:                                                              │
    │   - 반복적? (O/X)                                                        │
    │   - 자동화 가능? (O/X)                                                   │
    │   - 가치 창출? (O/X)                                                     │
    │   - 선형 성장? (O/X)                                                     │
    │                                                                          │
    └──────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
    [ Phase 2: ROI 분석 (Return on Investment) ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   토일 항목별 ROI 계산:                                                   │
    │                                                                          │
    │   ROI = (연간 절감 시간 × 시간당 비용 - 자동화 비용) / 자동화 비용        │
    │                                                                          │
    │   ┌─────────────────┬────────────┬────────────┬───────────┐            │
    │   │ 토일 항목        │ 주당 시간  │ 자동화 비용 │ ROI       │            │
    │   ├─────────────────┼────────────┼────────────┼───────────┤            │
    │   │ 수동 배포        │ 10시간     │ 40시간     │ 1,200%    │            │
    │   │ 로그 로테이션    │ 2시간      │ 8시간      │ 1,200%    │            │
    │   │ 백업 검증        │ 5시간      │ 20시간     │ 1,200%    │            │
    │   │ 보안 패치        │ 8시간      │ 16시간     │ 2,500%    │            │
    │   └─────────────────┴────────────┴────────────┴───────────┘            │
    │                                                                          │
    └──────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
    [ Phase 3: 자동화 구현 (Automation Implementation) ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   [ 선택한 토일 ] ──> [ 자동화 도구 선정 ] ──> [ 구현 ] ──> [ 테스트 ]   │
    │                                                                          │
    │   자동화 도구 체계:                                                       │
    │                                                                          │
    │   ┌─────────────────────────────────────────────────────────────────┐   │
    │   │ [ CI/CD Layer ]                                                 │   │
    │   │  - Jenkins / GitHub Actions / GitLab CI                         │   │
    │   │  - ArgoCD (GitOps)                                              │   │
    │   └─────────────────────────────────────────────────────────────────┘   │
    │   ┌─────────────────────────────────────────────────────────────────┐   │
    │   │ [ Infrastructure Layer ]                                        │   │
    │   │  - Terraform (IaC)                                              │   │
    │   │  - Ansible (Configuration Management)                           │   │
    │   │  - Kubernetes Operator Pattern                                  │   │
    │   └─────────────────────────────────────────────────────────────────┘   │
    │   ┌─────────────────────────────────────────────────────────────────┐   │
    │   │ [ Observability Layer ]                                         │   │
    │   │  - Prometheus + Alertmanager (자동 알림)                         │   │
    │   │  - Grafana (대시보드 as Code)                                   │   │
    │   │  - PagerDuty + SOAR (자동 에스컬레이션)                          │   │
    │   └─────────────────────────────────────────────────────────────────┘   │
    │                                                                          │
    └──────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
    [ Phase 4: 측정 및 개선 (Measurement & Improvement) ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   토일 비율 추적 대시보드:                                                │
    │                                                                          │
    │   ┌────────────────────────────────────────────────────────────────┐    │
    │   │                                                                │    │
    │   │   토일 비율 (Toil Ratio) = 토일 시간 / 전체 근무 시간 × 100     │    │
    │   │                                                                │    │
    │   │   목표: < 50%                                                  │    │
    │   │   현재: 35% ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░ 35%        │    │
    │   │                                                                │    │
    │   └────────────────────────────────────────────────────────────────┘    │
    │                                                                          │
    │   지속적 개선 사이클:                                                     │
    │   - 월간 토일 리뷰                                                        │
    │   - 분기별 자동화 ROI 분석                                                │
    │   - 연간 토일 비율 목표 설정                                              │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
```

### 3. 심층 동작 원리: 토일 자동화 5단계 프로세스

**1단계: 토일 식별 (Identification)**

```python
# toil_tracker.py - 토일 추적 시스템
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List
from enum import Enum

class ActivityType(Enum):
    TOIL = "toil"
    ENGINEERING = "engineering"
    OVERHEAD = "overhead"

@dataclass
class Activity:
    description: str
    duration_minutes: int
    activity_type: ActivityType
    is_repetitive: bool
    is_automatable: bool
    creates_value: bool
    timestamp: datetime

class ToilAnalyzer:
    def __init__(self):
        self.activities: List[Activity] = []

    def add_activity(self, activity: Activity):
        self.activities.append(activity)

    def is_toil(self, activity: Activity) -> bool:
        """토일 판정 로직"""
        return (
            activity.is_repetitive and
            activity.is_automatable and
            not activity.creates_value
        )

    def calculate_toil_ratio(self, period_days: int = 7) -> float:
        """토일 비율 계산"""
        cutoff = datetime.now() - timedelta(days=period_days)
        recent = [a for a in self.activities if a.timestamp >= cutoff]

        total_minutes = sum(a.duration_minutes for a in recent)
        toil_minutes = sum(
            a.duration_minutes for a in recent
            if a.activity_type == ActivityType.TOIL
        )

        return (toil_minutes / total_minutes * 100) if total_minutes > 0 else 0

    def get_automation_candidates(self) -> List[Activity]:
        """자동화 후보 선정"""
        toil_activities = [
            a for a in self.activities
            if a.activity_type == ActivityType.TOIL
        ]

        # 빈도순 정렬
        frequency = {}
        for a in toil_activities:
            key = a.description
            if key not in frequency:
                frequency[key] = {"count": 0, "total_minutes": 0}
            frequency[key]["count"] += 1
            frequency[key]["total_minutes"] += a.duration_minutes

        # ROI 기준 정렬 (빈도 × 시간)
        sorted_candidates = sorted(
            frequency.items(),
            key=lambda x: x[1]["count"] * x[1]["total_minutes"],
            reverse=True
        )

        return sorted_candidates[:10]  # Top 10
```

**2단계: ROI 분석 (ROI Analysis)**

```python
@dataclass
class AutomationProposal:
    toil_name: str
    current_weekly_hours: float
    automation_hours: float  # 구현에 걸리는 시간
    hourly_rate: float  # 시간당 인건비
    maintenance_hours_per_month: float  # 월 유지보수 시간

    def calculate_roi(self, annual_periods: int = 52) -> dict:
        """ROI 계산"""
        # 연간 절감 시간
        annual_hours_saved = self.current_weekly_hours * annual_periods

        # 연간 절감 비용
        annual_cost_saved = annual_hours_saved * self.hourly_rate

        # 구현 비용
        implementation_cost = self.automation_hours * self.hourly_rate

        # 연간 유지보수 비용
        annual_maintenance = self.maintenance_hours_per_month * 12 * self.hourly_rate

        # 순 절감액 (1년차)
        net_savings_year1 = annual_cost_saved - implementation_cost - annual_maintenance

        # ROI
        roi = (net_savings_year1 / implementation_cost * 100) if implementation_cost > 0 else 0

        # 손익분기점 (주)
        weekly_net_benefit = self.current_weekly_hours - (self.maintenance_hours_per_month / 4)
        break_even_weeks = self.automation_hours / weekly_net_benefit if weekly_net_benefit > 0 else float('inf')

        return {
            "annual_hours_saved": annual_hours_saved,
            "annual_cost_saved": annual_cost_saved,
            "implementation_cost": implementation_cost,
            "roi_percent": roi,
            "break_even_weeks": break_even_weeks,
            "3_year_savings": annual_cost_saved * 3 - implementation_cost - annual_maintenance * 3
        }

# 예시
proposal = AutomationProposal(
    toil_name="수동 배포 프로세스",
    current_weekly_hours=10,
    automation_hours=40,
    hourly_rate=100,  # $100/시간
    maintenance_hours_per_month=2
)

print(proposal.calculate_roi())
# {'annual_hours_saved': 520, 'annual_cost_saved': 52000,
#  'implementation_cost': 4000, 'roi_percent': 1100%, 'break_even_weeks': 4.17}
```

**3단계: 자동화 구현 (Implementation)**

```yaml
# Kubernetes CronJob 예시: 자동화된 DB 백업
apiVersion: batch/v1
kind: CronJob
metadata:
  name: automated-db-backup
  labels:
    app: backup
    toil-automation: "true"
spec:
  schedule: "0 2 * * *"  # 매일 새벽 2시
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 7
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      backoffLimit: 3
      activeDeadlineSeconds: 3600  # 1시간 타임아웃
      template:
        spec:
          serviceAccountName: backup-sa
          containers:
            - name: backup
              image: postgres:15
              command:
                - /bin/bash
                - -c
                - |
                  set -e
                  echo "Starting automated backup at $(date)"

                  # 백업 실행
                  pg_dump -h $DB_HOST -U $DB_USER $DB_NAME | gzip > /backup/db_$(date +%Y%m%d_%H%M%S).sql.gz

                  # S3 업로드
                  aws s3 cp /backup/ s3://$BUCKET_NAME/backups/ --recursive

                  # 30일 이상 된 백업 삭제
                  aws s3 ls s3://$BUCKET_NAME/backups/ | awk '{print $2}' | \
                    while read file; do
                      file_date=$(echo $file | grep -oE '[0-9]{8}')
                      if [ $(date -d "$file_date" +%s) -lt $(date -d "-30 days" +%s) ]; then
                        aws s3 rm s3://$BUCKET_NAME/backups/$file
                      fi
                    done

                  echo "Backup completed successfully at $(date)"

                  # 성공 메트릭 전송
                  curl -X POST http://prometheus-pushgateway:9091/metrics/job/backup/instance/automated
                  -d "backup_success{db=\"$DB_NAME\"} 1"
              env:
                - name: DB_HOST
                  valueFrom:
                    secretKeyRef:
                      name: db-credentials
                      key: host
                - name: DB_USER
                  valueFrom:
                    secretKeyRef:
                      name: db-credentials
                      key: user
                - name: PGPASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: db-credentials
                      key: password
                - name: DB_NAME
                  value: "production_db"
              volumeMounts:
                - name: backup-storage
                  mountPath: /backup
          volumes:
            - name: backup-storage
              emptyDir:
                sizeLimit: 10Gi
          restartPolicy: OnFailure
---
# 자동화된 백업 검증 (매주 일요일)
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-verification
spec:
  schedule: "0 6 * * 0"  # 매주 일요일 오전 6시
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: verify
              image: postgres:15
              command:
                - /bin/bash
                - -c
                - |
                  # 최신 백업 다운로드
                  LATEST=$(aws s3 ls s3://$BUCKET_NAME/backups/ | sort | tail -1 | awk '{print $2}')
                  aws s3 cp s3://$BUCKET_NAME/backups/$LATEST /tmp/backup.sql.gz

                  # 무결성 검증
                  gunzip -t /tmp/backup.sql.gz

                  # 스테이징 DB에 복원 테스트
                  psql -h $STAGING_DB_HOST -U $DB_USER -d restore_test -f /tmp/backup.sql

                  # 결과 알림
                  if [ $? -eq 0 ]; then
                    curl -X POST $SLACK_WEBHOOK -d '{"text":"백업 검증 성공: '$LATEST'"}'
                  else
                    curl -X POST $SLACK_WEBHOOK -d '{"text":":warning: 백업 검증 실패: '$LATEST'"}'
                  fi
          restartPolicy: OnFailure
```

**4단계: 토일 비율 측정 (Measurement)**

```promql
# PromQL: 토일 비율 계산
# 토일 활동 시간 / 전체 근무 시간

(
  sum(increase(toil_activity_minutes_total[7d]))
  /
  sum(increase(total_work_minutes_total[7d]))
) * 100

# 목표: 50% 미만
# 알림: 50% 이상 시 경고
```

**5단계: 지속적 개선 (Continuous Improvement)**

```python
# toil_dashboard.py - 토일 대시보드 데이터 생성
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class ToilDashboard:
    def __init__(self, activities: List[Activity]):
        self.activities = activities

    def generate_report(self) -> dict:
        """토일 리포트 생성"""
        df = pd.DataFrame([
            {
                "date": a.timestamp.date(),
                "activity": a.description,
                "minutes": a.duration_minutes,
                "type": a.activity_type.value
            }
            for a in self.activities
        ])

        report = {
            "total_activities": len(df),
            "toil_ratio": self._calculate_toil_ratio(df),
            "top_toil_activities": self._get_top_toil(df),
            "trend": self._calculate_trend(df),
            "automation_candidates": self._get_automation_candidates(df)
        }

        return report

    def _calculate_toil_ratio(self, df: pd.DataFrame) -> float:
        toil_minutes = df[df["type"] == "toil"]["minutes"].sum()
        total_minutes = df["minutes"].sum()
        return (toil_minutes / total_minutes * 100) if total_minutes > 0 else 0

    def _get_top_toil(self, df: pd.DataFrame, n: int = 5) -> list:
        toil_df = df[df["type"] == "toil"]
        return toil_df.groupby("activity")["minutes"].sum().nlargest(n).to_dict()

    def _calculate_trend(self, df: pd.DataFrame) -> str:
        """주별 토일 비율 추세"""
        df["week"] = pd.to_datetime(df["date"]).dt.isocalendar().week
        weekly = df.groupby("week").apply(
            lambda x: (x[x["type"] == "toil"]["minutes"].sum() / x["minutes"].sum() * 100)
        )

        if len(weekly) < 2:
            return "데이터 부족"

        if weekly.iloc[-1] < weekly.iloc[-2]:
            return "감소 (긍정적)"
        elif weekly.iloc[-1] > weekly.iloc[-2]:
            return "증가 (개선 필요)"
        else:
            return "유지"

    def _get_automation_candidates(self, df: pd.DataFrame) -> list:
        """자동화 우선순위 추천"""
        toil_df = df[df["type"] == "toil"]

        # 빈도 × 시간 기준 우선순위
        candidates = toil_df.groupby("activity").agg({
            "minutes": ["sum", "count"]
        })
        candidates.columns = ["total_minutes", "frequency"]
        candidates["priority_score"] = candidates["total_minutes"] * candidates["frequency"]

        return candidates.nlargest(5, "priority_score").index.tolist()
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 자동화 도구별 토일 제거 효과

| 자동화 도구 | 적용 토일 유형 | 구현 난이도 | ROI | 유지보수 부담 | 비고 |
|:---|:---|:---|:---|:---|:---|
| **CI/CD (Jenkins)** | 배포, 테스트 | 중간 | 높음 | 중간 | 초기 설정 복잡 |
| **GitOps (ArgoCD)** | 배포, 롤백 | 높음 | 매우 높음 | 낮음 | K8s 환경 필수 |
| **IaC (Terraform)** | 인프라 프로비저닝 | 높음 | 매우 높음 | 낮음 | 상태 관리 필요 |
| **Ansible** | 설정 관리, 패치 | 낮음 | 높음 | 낮음 | 에이전트 불필요 |
| **K8s Operator** | DB 운영, 백업 | 매우 높음 | 매우 높음 | 중간 | CRD 개발 필요 |
| **SOAR** | 인시던트 대응 | 중간 | 높음 | 낮음 | 플레이북 작성 |
| **RPA** | CLI 불가 작업 | 낮음 | 중간 | 높음 | GUI 자동화 |

### 2. 과목 융합 관점 분석

**토일 자동화 + 보안 (DevSecOps)**:
- 수동 보안 스캔 → 자동화된 SAST/DAST/SCA
- CVE 대응 → Dependabot/Renovate 자동 PR
- 컴플라이언스 체크 → Policy as Code (OPA)

**토일 자동화 + 데이터 (DataOps)**:
- 수동 ETL → Airflow/dbt 자동화
- 데이터 품질 체크 → Great Expectations 자동화
- 리포트 생성 → 자동화된 대시보드

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

**시나리오: 중견 기업의 SRE 팀 토일 70% 문제**
- **상황**: SRE 팀 10명 중 7명이 수동 운영 업무에 매몰, 번아웃으로 이직률 증가
- **기술사의 전략적 의사결정**:
  1. **토일 감사**: 2주간 모든 활동 추적, 토일 카테고리 분류
  2. **Quick Wins**: ROI 높은 간단한 자동화부터 시작 (로그 로테이션, 백업)
  3. **투자 확대**: CI/CD 파이프라인 구축에 3개월 집중 투자
  4. **문화 변화**: "자동화하지 않으면 반복하지 말라" 원칙 정착

### 2. 도입 시 고려사항 (체크리스트)

**토일 식별 체크리스트**:
- [ ] 모든 반복 업무 목록화
- [ ] 각 업무의 시간 소요 측정
- [ ] 자동화 가능성 평가
- [ ] 우선순위 설정 (ROI 기준)

**자동화 구현 체크리스트**:
- [ ] 적절한 자동화 도구 선정
- [ ] 테스트 환경에서 검증
- [ ] 롤백 계획 수립
- [ ] 문서화 및 지식 공유

### 3. 주의사항 및 안티패턴

**안티패턴 1: 과도한 자동화**
- 문제: 모든 것을 자동화하려다 유지보수 부담 급증
- 해결: ROI가 높은 핵심 토일부터 우선 자동화

**안티패턴 2: 자동화 유지보수 소홀**
- 문제: 자동화된 스크립트가 오래되어 실패
- 해결: 자동화 코드도 버전 관리, 정기 검증

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **토일 비율** | 70% | 30% | 40%p 감소 |
| **엔지니어링 시간** | 30% | 70% | 2.3배 증가 |
| **번아웃 이직률** | 25%/년 | 10%/년 | 60% 감소 |
| **장애 대응 속도** | 2시간 | 15분 | 87.5% 단축 |

### 2. 미래 전망 및 진화 방향

**AI 기반 토일 자동화**:
- LLM을 활용한 자동 스크립트 생성
- 예측 기반 선제적 자동화
- 자연어 기반 운영 자동화

### 3. 참고 표준/가이드

- **Google SRE Book**: Chapter 5 - Toil
- **Site Reliability Workbook**: Toil Management
- **Platform Engineering**: Internal Developer Platform

---

## 관련 개념 맵 (Knowledge Graph)

- [SRE 원칙](@/studynotes/15_devops_sre/01_sre/sre_principles.md) : 토일 개념의 철학적 기반
- [CI/CD 파이프라인](@/studynotes/15_devops_sre/03_automation/cicd_gitops.md) : 배포 토일 자동화 도구
- [IaC (Infrastructure as Code)](@/studynotes/15_devops_sre/03_automation/infrastructure_as_code.md) : 인프라 토일 자동화
- [옵저버빌리티](@/studynotes/15_devops_sre/02_observability/observability_fundamentals.md) : 토일 측정 체계
- [에러 버짯](@/studynotes/15_devops_sre/01_sre/error_budget.md) : 토일과 엔지니어링 균형

---

## 어린이를 위한 3줄 비유 설명

1. 토일은 **매일 해야 하는 설거지**와 같아요. 아무리 열심히 씻어도 내일 또 접시가 쌓이죠.
2. SRE 엔지니어들은 이 설거지를 **식기세척기(자동화)**로 바꿔서, 요리 연구(혁신)에 시간을 써요.
3. 덕분에 더 맛있는 요리(새로운 기능)를 더 자주 만들 수 있게 돼요!
