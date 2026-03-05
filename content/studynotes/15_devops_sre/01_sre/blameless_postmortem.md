+++
title = "무비난 포스트모템 (Blameless Post-mortem)"
categories = ["studynotes-15_devops_sre"]
+++

# 무비난 포스트모텀 (Blameless Post-mortem)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 장애 발생 시 "누가 잘못했는가"가 아닌 "시스템이 왜 이것을 막지 못했는가"에 집중하여, 인적 오류가 아닌 시스템적 결함을 개선하는 학습 중심의 장애 회고 문화입니다.
> 2. **가치**: 심리적 안전감을 조성하여 장애 사실 은폐를 방지하고, 근본 원인 분석을 통한 시스템 신뢰성 지속적 향상을 가능하게 합니다.
> 3. **융합**: SRE 에러 버짯, 옵저버빌리티, 그리고 데브옵스 문화와 결합하여 조직의 학습 능력을 조직적 자산으로 전환합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)

**무비난 포스트모텀(Blameless Post-mortem)**은 프로덕션 장애 발생 후, 개인을 비난하거나 처벌하지 않고 시스템적 관점에서 근본 원인(Root Cause)을 분석하고, 재발 방지를 위한 구체적인 액션 아이템을 도출하는 구조화된 회고 프로세스입니다.

핵심 원칙:
1. **개인 비난 금지**: "누가"가 아닌 "무엇이"에 집중
2. **심리적 안전감**: 솔직한 공개를 장려
3. **시스템 개선**: 프로세스, 도구, 자동화 중심 해결
4. **지식 공유**: 장애 교훈의 조직 전파

### 2. 구체적인 일상생활 비유

**항공 사고 조사**로 비유해 봅시다.

항공 사고 발생 시, 조종사를 처벌하는 것이 아니라 "어떤 시스템적 문제가 있었나?"를 분석합니다:
- 조종사가 피곤했다면 → 교대 규정 개선
- 계기판이 보기 어려웠다면 → UI 개선
- 통신이 두절됐다면 → 통신 시스템 개선

이렇게 해서 얻은 교훈은 모든 항공사에 공유되어 비행 안전성이 지속적으로 향상됩니다.

### 3. 등장 배경 및 발전 과정

**1단계: 기존 기술의 치명적 한계점 (비난 문화)**
- 장애 발생 시 "누가 배포했나?"부터 질문
- 처벌 두려움으로 장애 은폐, 축소 보고
- 같은 장애 반복 (근본 원인 미해결)
- 엔지니어 번아웃 및 이직

**2단계: 혁신적 패러다임 변화**
- 1970년대 High Reliability Organizations (HRO) 연구
- 항공, 원자력 산업의 안전 문화 연구
- 2010년대 구글 SRE가 "Blameless" 개념 정립
- 에릭 레이먼드(Eric Raymond)의 "Given enough eyeballs, all bugs are shallow"

**3단계: 현재 시장/산업의 비즈니스적 요구사항**
- MSA 환경에서 장애 원인 파악의 복잡성 증가
- 빠른 배포를 위한 장애 학습 문화 필수
- DevOps/DORA 연구: 심리적 안전감이 고성과 팀의 핵심 요소

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 포스트모텀 프로세스 구성 요소

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 산출물 | 비고 |
|:---|:---|:---|:---|:---|
| **타임라인** | 장애 발생~복구 시간순 기록 | 5분 단위 이벤트 로그 | Timeline Document | GMT/KST 명시 |
| **영향 평가** | 고객/비즈니스 영향 분석 | SLI 위반, 고객 수, 매출 손실 | Impact Report | 정량적 지표 |
| **근본 원인 분석** | 5 Whys, Fishbone 등 적용 | 시스템적 원인 도출 | RCA Document | 비난 금지 |
| **액션 아이템** | 재발 방지 대책 수립 | 우선순위, 담당자, 마감일 | Action Items List | 추적 가능하게 |
| **교훈 공유** | 조직 전체 학습 | 위키, 세미나, 뉴스레터 | Knowledge Base | 익명화 가능 |

### 2. 정교한 구조 다이어그램: 포스트모텀 라이프사이클

```text
================================================================================
                      [ Blameless Post-mortem Lifecycle ]
================================================================================

    [ Phase 1: 장애 발생 및 대응 (Incident Response) ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   [ 장애 탐지 ] ──> [ 경보 발송 ] ──> [ 대응 시작 ] ──> [ 복구 ]         │
    │                                                                          │
    │   ┌──────────────────────────────────────────────────────────────┐      │
    │   │ 타임라인 자동 수집:                                          │      │
    │   │ - T+0: Prometheus Alert 발생                                │      │
    │   │ - T+2min: PagerDuty 호출                                    │      │
    │   │ - T+5min: Oncall 엔지니어 접속                              │      │
    │   │ - T+15min: War Room 개설                                    │      │
    │   │ - T+45min: 장애 원인 식별                                   │      │
    │   │ - T+60min: 롤백 완료, 서비스 복구                           │      │
    │   └──────────────────────────────────────────────────────────────┘      │
    │                                                                          │
    │   ⚠️ 중요: 복구 단계에서는 비난 금지, 오직 해결에 집중                   │
    │                                                                          │
    └──────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
    [ Phase 2: 포스트모텀 준비 (Preparation) - 복구 후 24-72시간 ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   [ 데이터 수집 ]                                                        │
    │   ┌────────────────────────────────────────────────────────────────┐    │
    │   │ • 그라파나 대시보드 스냅샷                                     │    │
    │   │ • 로그/트레이스 추출                                          │    │
    │   │ • Slack/이메일 대화 백업                                       │    │
    │   │ • 배포 기록 (Git commits, CI/CD 로그)                         │    │
    │   │ • 고객 문의 내역                                               │    │
    │   └────────────────────────────────────────────────────────────────┘    │
    │                                                                          │
    │   [ 참석자 선정 ]                                                        │
    │   • Incident Commander (진행자)                                         │
    │   • 관련 서비스 담당자                                                  │
    │   • SRE/Observability 담당                                             │
    │   • 선택적: 비즈니스 스테이크홀더                                       │
    │                                                                          │
    └──────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
    [ Phase 3: 포스트모텀 회의 (Meeting) - 60-90분 ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   [ Agenda ]                                                             │
    │                                                                          │
    │   1. 개요 (5분)                                                          │
    │      - 장애 요약, 영향 범위                                              │
    │                                                                          │
    │   2. 타임라인 리뷰 (15분)                                                │
    │      - 분 단위 이벤트 검토                                               │
    │      - "그때 무슨 일이 있었나?" (What happened?)                        │
    │                                                                          │
    │   3. 5 Whys 분석 (30분) ───────────────────────────────────────────┐    │
    │                                                                    │    │
    │      예시:                                                         │    │
    │      Why 1: 왜 DB 커넥션이 고갈됐나? → 커넥션 누수                 │    │
    │      Why 2: 왜 커넥션 누수가 발생했나? → finally 블록 누락        │    │
    │      Why 3: 왜 finally 블록이 누락됐나? → 코드 리뷰 미실시        │    │
    │      Why 4: 왜 코드 리뷰가 안 됐나? → 긴급 배포 프로세스           │    │
    │      Why 5: 왜 긴급 배포가 허용되나? → 프로세스 부재               │    │
    │                                                                    │    │
    │      ⚠️ 규칙: "누가"가 아닌 "왜"에 집중                           │    │
    │      ⛔ 금지: "왜 그 사람이 그 코드를 짰나?"                      │    │
    │      ✅ 권장: "어떤 시스템이 이를 방지했어야 했나?"               │    │
    │      ─────────────────────────────────────────────────────────────┘    │
    │                                                                          │
    │   4. 액션 아이템 도출 (15분)                                             │
    │      - 즉시 개선 (P0): 이번 주                                          │
    │      - 단기 개선 (P1): 이번 달                                          │
    │      - 장기 개선 (P2): 분기 내                                          │
    │                                                                          │
    │   5. 교훈 및 공유 (5분)                                                  │
    │      - 다른 팀에도 적용 가능한 교훈                                     │
    │                                                                          │
    └──────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
    [ Phase 4: 문서화 및 공유 (Documentation & Sharing) ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   [ 포스트모텀 문서 템플릿 ]                                              │
    │   ┌────────────────────────────────────────────────────────────────┐    │
    │   │ # Post-mortem: [장애명] - [날짜]                              │    │
    │   │                                                                │    │
    │   │ ## 요약                                                       │    │
    │   │ - 장애 기간: YYYY-MM-DD HH:MM ~ HH:MM (X분)                   │    │
    │   │ - 영향: X명 고객, Y건 거래 실패                               │    │
    │   │ - 근본 원인: [3줄 요약]                                        │    │
    │   │                                                                │    │
    │   │ ## 타임라인                                                   │    │
    │   │ | 시간 | 이벤트 |                                             │    │
    │   │                                                                │    │
    │   │ ## 근본 원인 분석 (5 Whys)                                    │    │
    │   │                                                                │    │
    │   │ ## 액션 아이템                                                │    │
    │   │ | 항목 | 유형 | 담당자 | 마감일 | 상태 |                      │    │
    │   │                                                                │    │
    │   │ ## 교훈                                                       │    │
    │   │ - 다른 팀에서도 발생할 수 있는지?                             │    │
    │   │ - 어떻게 더 빨리 탐지할 수 있었는지?                          │    │
    │   └────────────────────────────────────────────────────────────────┘    │
    │                                                                          │
    │   [ 공유 채널 ]                                                          │
    │   • 사내 위키 (Confluence/Notion)                                        │
    │   • #postmortem Slack 채널                                               │
    │   • 월간 Post-mortem Review 미팅                                         │
    │   • 선택적: 블로그 공개 (Netflix, GitLab 사례)                           │
    │                                                                          │
    └──────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
    [ Phase 5: 후속 조치 (Follow-up) ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   [ 액션 아이템 추적 ]                                                   │
    │   • JIRA 티켓 생성 (자동화 가능)                                        │
    │   • 주간 진행 상황 체크                                                  │
    │   • 완료 시 Post-mortem 문서 업데이트                                   │
    │                                                                          │
    │   [ 메트릭 측정 ]                                                        │
    │   • Action Item 완료율                                                   │
    │   • 반복 장애 발생률                                                     │
    │   • MTTR 추이                                                            │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
```

### 3. 심층 동작 원리: 5 Whys 분석법

5 Whys는 토요타 생산 방식에서 유래한 근본 원인 분석 기법입니다.

```text
예시: 결제 서비스 장애

현상: 결제 API 응답 지연 30초, 타임아웃 다수 발생

Why 1: 왜 API 응답이 지연됐나?
└─ DB 쿼리 실행 시간이 25초나 걸렸다

Why 2: 왜 DB 쿼리가 느렸나?
└─ 특정 인덱스가 누락된 대량 조회 쿼리가 실행됐다

Why 3: 왜 인덱스가 누락됐나?
└─ 스키마 마이그레이션 시 인덱스 생성 스크립트가 누락됐다

Why 4: 왜 마이그레이션 스크립트가 누락됐나?
└─ DBA 리뷰 없이 긴급 배포가 진행됐다

Why 5: 왜 DBA 리뷰 없이 배포가 가능했나?
└─ ⭐ 근본 원인: DB 스키마 변경에 대한 필수 리뷰 프로세스가 없다

[액션 아이템]
P0: 누락된 인덱스 즉시 생성
P1: DB 스키마 변경 시 자동 DBA 알림 (CI/CD 연동)
P2: 스키마 변경 가이드라인 문서화 및 교육
```

### 4. 포스트모텀 문서 자동화 예시

```python
#!/usr/bin/env python3
"""
포스트모텀 문서 자동 생성기
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class Severity(Enum):
    SEV1 = "SEV1"  # 완전 서비스 중단
    SEV2 = "SEV2"  # 주요 기능 장애
    SEV3 = "SEV3"  # 부분 장애

class ActionPriority(Enum):
    P0 = "P0"  # 즉시 (이번 주)
    P1 = "P1"  # 단기 (이번 달)
    P2 = "P2"  # 장기 (분기 내)

@dataclass
class TimelineEvent:
    timestamp: datetime
    event: str
    actor: str
    details: Optional[str] = None

@dataclass
class ActionItem:
    description: str
    priority: ActionPriority
    owner: str
    due_date: datetime
    jira_ticket: Optional[str] = None
    status: str = "OPEN"

@dataclass
class FiveWhys:
    whys: List[str]  # 5개의 Why 질문과 답변
    root_cause: str  # 근본 원인

@dataclass
class PostMortem:
    incident_name: str
    severity: Severity
    start_time: datetime
    end_time: datetime
    summary: str
    impact: str
    timeline: List[TimelineEvent] = field(default_factory=list)
    five_whys: Optional[FiveWhys] = None
    action_items: List[ActionItem] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)

    @property
    def duration_minutes(self) -> int:
        return int((self.end_time - self.start_time).total_seconds() / 60)

    def generate_markdown(self) -> str:
        """마크다운 문서 생성"""
        md = f"""# Post-mortem: {self.incident_name}

**날짜**: {self.start_time.strftime('%Y-%m-%d')}
**심각도**: {self.severity.value}
**작성자**: [자동 생성]
**상태**: DRAFT

---

## 요약

- **장애 기간**: {self.start_time.strftime('%Y-%m-%d %H:%M')} ~ {self.end_time.strftime('%H:%M')} ({self.duration_minutes}분)
- **영향**: {self.impact}
- **근본 원인**: {self.five_whys.root_cause if self.five_whys else 'TBD'}

---

## 상세 내용

{self.summary}

---

## 타임라인

| 시간 | 이벤트 | 주체 | 상세 |
|:---|:---|:---|:---|
"""
        for event in self.timeline:
            md += f"| {event.timestamp.strftime('%H:%M')} | {event.event} | {event.actor} | {event.details or '-'} |\n"

        md += "\n---\n\n## 근본 원인 분석 (5 Whys)\n\n"
        if self.five_whys:
            for i, why in enumerate(self.five_whys.whys, 1):
                md += f"**Why {i}**: {why}\n\n"
            md += f"**⭐ 근본 원인**: {self.five_whys.root_cause}\n\n"

        md += """---

## 액션 아이템

| 항목 | 우선순위 | 담당자 | 마감일 | JIRA | 상태 |
|:---|:---|:---|:---|:---|:---|
"""
        for item in self.action_items:
            jira_link = f"[{item.jira_ticket}]({item.jira_ticket})" if item.jira_ticket else "-"
            md += f"| {item.description} | {item.priority.value} | {item.owner} | {item.due_date.strftime('%Y-%m-%d')} | {jira_link} | {item.status} |\n"

        md += "\n---\n\n## 교훈\n\n"
        for lesson in self.lessons_learned:
            md += f"- {lesson}\n"

        md += """
---

## 참고 자료

- [그라파나 대시보드 스냅샷](#)
- [관련 로그](#)
- [Slack 대화 백업](#)

---

*이 문서는 Blameless Post-mortem 원칙에 따라 작성되었습니다.*
*장애는 시스템의 실패이며, 개인의 실패가 아닙니다.*
"""
        return md


# 사용 예시
if __name__ == "__main__":
    pm = PostMortem(
        incident_name="결제 API 타임아웃 장애",
        severity=Severity.SEV2,
        start_time=datetime(2024, 1, 15, 14, 30),
        end_time=datetime(2024, 1, 15, 15, 45),
        summary="결제 서비스 DB 커넥션 풀 고갈로 인한 API 타임아웃 발생",
        impact="약 5,000명 고객 결제 실패, 예상 매출 손실 2,000만원"
    )

    # 타임라인 추가
    pm.timeline = [
        TimelineEvent(datetime(2024, 1, 15, 14, 30), "Prometheus Alert 발생", "System", "DB 커넥션 수 경고"),
        TimelineEvent(datetime(2024, 1, 15, 14, 32), "Oncall 엔지니어 알림 확인", "김O 님", "Slack #incident 채널"),
        TimelineEvent(datetime(2024, 1, 15, 14, 40), "장애 원인 식별: 커넥션 누수", "김O 님", "로그 분석 완료"),
        TimelineEvent(datetime(2024, 1, 15, 14, 55), "롤백 결정", "Incident Commander", "이전 버전으로 복구"),
        TimelineEvent(datetime(2024, 1, 15, 15, 10), "롤백 완료", "김O 님", "서비스 정상화"),
        TimelineEvent(datetime(2024, 1, 15, 15, 45), "모니터링 확인 및 장애 종료", "SRE 팀", "모든 메트릭 정상"),
    ]

    # 5 Whys
    pm.five_whys = FiveWhys(
        whys=[
            "왜 API 응답이 지연됐나? → DB 커넥션 풀이 고갈됐다",
            "왜 커넥션 풀이 고갈됐나? → 커넥션을 반환하지 않는 코드가 있었다",
            "왜 커넥션 반환 코드가 누락됐나? → finally 블록이 없었다",
            "왜 finally 블록이 없었나? → 코드 리뷰에서 놓쳤다",
            "왜 코드 리뷰에서 놓쳤나? → 리뷰 체크리스트에 DB 리소스 관리 항목이 없었다"
        ],
        root_cause="DB 리소스 관리에 대한 코드 리뷰 체크리스트 부재"
    )

    # 액션 아이템
    pm.action_items = [
        ActionItem(
            description="DB 커넥션 관련 코드 리뷰 체크리스트 추가",
            priority=ActionPriority.P0,
            owner="김O 님",
            due_date=datetime(2024, 1, 19),
            jira_ticket="DEV-1234"
        ),
        ActionItem(
            description="커넥션 누수 자동 탐지 메트릭 추가",
            priority=ActionPriority.P1,
            owner="박O 님",
            due_date=datetime(2024, 1, 31),
            jira_ticket="SRE-567"
        ),
        ActionItem(
            description="DB 리소스 관리 가이드 문서화",
            priority=ActionPriority.P2,
            owner="이O 님",
            due_date=datetime(2024, 2, 28)
        ),
    ]

    # 교훈
    pm.lessons_learned = [
        "DB 커넥션 사용 시 try-finally 또는 try-with-resources 필수",
        "코드 리뷰 체크리스트에 리소스 관리 항목 포함 필요",
        "커넥션 풀 모니터링 알림 임계값 재설정 필요"
    ]

    # 문서 생성
    print(pm.generate_markdown())
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 장애 분석 프레임워크

| 분석 기법 | 적용 상황 | 장점 | 단점 | 비고 |
|:---|:---|:---|:---|:---|
| **5 Whys** | 단순 원인 체인 | 간단, 직관적 | 너무 단순할 수 있음 | 기본 기법 |
| **Fishbone** | 복잡한 다중 원인 | 체계적 분류 | 시간 소요 | Ishikawa 다이어그램 |
| **FMEA** | 예방적 분석 | 위험 우선순위 | 복잡도 높음 | Failure Mode Effects |
| **RCA** | 포괄적 분석 | 종합적 | 자원 집약 | Root Cause Analysis |
| **COOP** | 프로세스 중심 | 프로세스 개선 | 기술적 깊이 부족 | Corrective Action |

### 2. 과목 융합 관점 분석

**포스트모템 + 보안 (Security Incident Response)**:
- 보안 사고도 동일한 Blameless 원칙 적용
- "왜 이 취약점이 코드에 들어갔나?" → "어떤 프로세스가 방어했어야 했나?"
- 보안 교훈의 조직 전파

**포스트모템 + 옵저버빌리티**:
- 장애 타임라인 자동 수집
- 근거 데이터(로그, 메트릭, 트레이스) 확보
- 개선 효과 측정

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

**시나리오: 대기업의 "비난 문화" 개선**
- **상황**: 장애 발생 시 담당자 인사 평가 차감, 은폐 문화 만연
- **기술사의 전략적 의사결정**:
  1. **경영진 설득**: 블레임리스 문화의 ROI 제시 (장애 은폐 감소 → MTTR 단축)
  2. **제도 개선**: 인사 평가에서 "장애 발생" 제거, "장애 대응 품질" 추가
  3. **파일럿**: SRE 팀에서 먼저 적용, 성과 공유
  4. **확산**: 전체 개발 조직으로 확대

### 2. 도입 시 고려사항 (체크리스트)

**조직적 체크리스트**:
- [ ] 경영진의 블레임리스 원칙 서명
- [ ] 인사 평가 기준에서 장애 처벌 제거
- [ ] 포스트모텀 템플릿 및 가이드 배포
- [ ] 진행자(Facilitator) 교육

**기술적 체크리스트**:
- [ ] 타임라인 자동 수집 도구
- [ ] 포스트모텀 문서 저장소
- [ ] 액션 아이템 추적 시스템 (JIRA 연동)

### 3. 주의사항 및 안티패턴

**안티패턴 1: "블레임리스"를 무책임의 핑계로 사용**
- 문제: 책임을 지지 않는 문화로 변질
- 해결: 개인은 비난하지 않되, 시스템 개선 의무는 명확히

**안티패턴 2: 포스트모텀을 형식적으로 수행**
- 문제: "5 Whys"를 건너뛰고 바로 액션 아이템
- 해결: 충분한 분석 시간 확보, 진행자 역할 강화

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **장애 보고율** | 40% (은폐) | 95% (공개) | 2.4배 증가 |
| **반복 장애율** | 30% | 5% | 83% 감소 |
| **MTTR** | 4시간 | 30분 | 87.5% 단축 |
| **엔지니어 신뢰도** | 낮음 | 높음 | 이직률 감소 |

### 2. 미래 전망 및 진화 방향

**AI 기반 포스트모텀**:
- 장애 패턴 자동 인식
- 유사 장애 사례 추천
- 액션 아이템 자동 제안

### 3. 참고 표준/가이드

- **Google SRE Workbook**: Chapter 14 - Postmortem Culture
- **Etsy's Debriefing Guide**: 블레임리스 포스트모텀 가이드
- **NASA's Apollo 13**: 고신뢰조직(HRO)의 사고 학습 문화

---

## 관련 개념 맵 (Knowledge Graph)

- [심리적 안전감](@/studynotes/15_devops_sre/01_sre/psychological_safety.md) : 블레임리스 문화의 기반
- [에러 버짯](@/studynotes/15_devops_sre/01_sre/error_budget.md) : 장애 수용 철학
- [옵저버빌리티](@/studynotes/15_devops_sre/02_observability/observability_fundamentals.md) : 장애 분석 데이터
- [SRE 원칙](@/studynotes/15_devops_sre/01_sre/sre_principles.md) : SRE 철학의 기반
- [DevOps 문화](@/studynotes/15_devops_sre/01_sre/devops_culture.md) : 협업 문화의 기반

---

## 어린이를 위한 3줄 비유 설명

1. 포스트모텀은 **축구 경기 후 비디오 분석**과 같아요. 경기를 진 다음 누구를 비난하는 게 아니라, "어떻게 하면 다음에 이기지?"를 같이 고민해요.
2. "왜 골을 놓쳤을까?" → "연습이 부족했네" → "다음엔 더 연습하자!"라고 계획을 세우죠.
3. 이렇게 하면 **실수를 숨기지 않고 모두가 함께 배우면서** 점점 더 잘하게 돼요!
