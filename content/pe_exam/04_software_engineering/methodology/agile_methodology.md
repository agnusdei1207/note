+++
title = "애자일 방법론 (Agile Methodology)"
date = 2025-03-01

[extra]
categories = "software_engineering-methodology"
+++

# 애자일 방법론 (Agile Methodology)

## 핵심 인사이트 (3줄 요약)
> **변화에 유연하게 대응하는 반복적·점진적 소프트웨어 개발 방식**. 1~4주 스프린트로 작동하는 SW를 지속 전달. 협업, 피드백, 적응이 핵심 가치다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 애자일(Agile) 방법론은 **2001년 애자일 선언문을 통해 정립된 유연한 소프트웨어 개발 철학과 실천법**으로, 변화를 수용하고 고객과 협업하며 작동하는 소프트웨어를 짧은 주기로 지속적으로 전달하는 것을 목적으로 한다.

> 💡 **비유**: 애자일은 **"요리의 맛보기 식사"** 같아요. 완성된 코스 요리를 한 번에 내는 대신, 요리 과정에서 계속 맛을 보며 조리법을 조정하죠. "짜면 소금을 줄이고, 달면 설탕을 줄이는" 식으로요. 결과적으로 손님(고객)이 원하는 맛에 가까워집니다!

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 워터폴의 경직성**: 요구사항을 초기에 모두 정의해야 하며, 변경 비용이 기하급수적으로 증가 (요구사항 변경 1건이 수억 원 손실)
2. **기술적 필요성 - 불확실성 관리**: 소프트웨어는 복잡성(Complex)과 불확실성(Uncertain)이 높아 예측 기반 계획 불가. 탐색적 접근 필요
3. **시장/산업 요구 - Time-to-Market**: 인터넷 시대로 제품 출시 속도가 경쟁력의 핵심. 6개월 개발 → 2주 스프린트로 전환 필요

**핵심 목적**: **불확실한 환경에서 고객 가치를 빠르게 전달하고 지속적으로 개선**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**애자일 선언문 4가치** (필수):
```
┌─────────────────────────────────────────────────────────────────────────┐
│              애자일 소프트웨어 개발 선언 (2001. 2. 11~13)                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   우리는 소프트웨어를 개발하면서 더 나은 방법을 찾고                     │
│   다른 사람들을 도와주면서 다음 가치를 더 중요하게 여깁니다:             │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                                                                 │   │
│   │  공정과 도구보다         [개인과 상호작용]을                     │   │
│   │  (Processes and tools) → (Individuals and interactions)        │   │
│   │                                                                 │   │
│   │  포괄적인 문서보다       [작동하는 소프트웨어]을                 │   │
│   │  (Comprehensive docs)   → (Working software)                   │   │
│   │                                                                 │   │
│   │  계약 협상보다           [고객과의 협력]을                       │   │
│   │  (Contract negotiation) → (Customer collaboration)             │   │
│   │                                                                 │   │
│   │  계획을 따르기보다       [변화에 대응]을                         │   │
│   │  (Following a plan)     → (Responding to change)               │   │
│   │                                                                 │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│   즉, 오른쪽의 가치도 중요하지만, 우리는 왼쪽의 가치에                   │
│   더 높은 가치를 둡니다.                                                │
│                                                                         │
│   - 17명의 서명자: Kent Beck, Martin Fowler, Ken Schwaber 등           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**애자일 12원칙** (필수: 전체 나열):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                       애자일 12원칙                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ① 고객 만족                                                            │
│     가치 있는 소프트웨어를 빠르고 지속적으로 전달하여 고객 만족          │
│                                                                         │
│  ② 변화 수용                                                            │
│     개발 후반에도 요구사항 변경을 환영 (경쟁 우위 확보)                  │
│                                                                         │
│  ③ 짧은 릴리즈                                                          │
│     몇 주~몇 개월 단위로 작동하는 소프트웨어 전달 (짧을수록 좋음)         │
│                                                                         │
│  ④ 협업                                                                 │
│     비즈니스 담당자와 개발자는 프로젝트 전반에 걸쳐 매일 함께 일함       │
│                                                                         │
│  ⑤ 동기 부여된 팀                                                       │
│     의지 있는 개인 중심으로 팀 구성, 환경과 지원 제공, 신뢰              │
│                                                                         │
│  ⑥ 대면 커뮤니케이션                                                    │
│     개발 팀 내에서 정보 전달의 가장 효율적이고 효과적인 방법             │
│                                                                         │
│  ⑦ 작동하는 소프트웨어                                                  │
│     진척도의 1차 척도 (문서, 계획이 아님)                                │
│                                                                         │
│  ⑧ 지속 가능한 속도                                                     │
│     후원자, 개발자, 사용자가 무기한 지속 가능한 일정 속도 유지           │
│                                                                         │
│  ⑨ 기술적 우수성                                                        │
│     좋은 설계와 기술적 탁월성에 지속적 관심 → 민척성 향상                │
│                                                                         │
│  ⑩ 단순화                                                               │
│     안 하는 일의 양을 최대화하는 기술 (필요 없는 것 과감히 제거)         │
│                                                                         │
│  ⑪ 자기 조직화 팀                                                       │
│     팀이 스스로 최선의 아키텍처, 요구사항, 설계 도출                     │
│                                                                         │
│  ⑫ 회고와 개선                                                          │
│     정기적으로 효율성을 반성하고 그에 따라 팀 행동 조정                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**주요 애자일 프레임워크 비교** (필수: 표):
| 구성 요소 | 스크럼 (Scrum) | XP (Extreme Programming) | 칸반 (Kanban) |
|----------|---------------|-------------------------|---------------|
| **반복 주기** | 2~4주 스프린트 (고정) | 1~2주 이터레이션 | 연속 흐름 (주기 없음) |
| **역할** | PO, SM, 개발팀 | Coach, Customer, Dev | 제한 없음 |
| **핵심 실천법** | 데일리 스탠드업, 회고 | TDD, 페어 프로그래밍, CI | WIP 제한, 칸반 보드 |
| **변경 시점** | 스프린트 간에만 | 이터레이션 간에만 | 언제든 (WIP 여유 시) |
| **계획 방식** | 스프린트 계획 미팅 | 이터레이션 계획 | Just-in-Time |
| **추정** | 스토리 포인트, 플래닝 포커 | 이상적 시간 | 리드 타임 기반 |
| **적합 환경** | ★ 제품 개발, 스타트업 | 품질 중심, 높은 기술 부채 | 운영/유지보수, 지원 |

**스크럼 프로세스 다이어그램** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        스크럼 프로세스                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │                     Product Backlog                               │  │
│   │        (제품 백로그: 우선순위 있는 사용자 스토리 목록)            │  │
│   │                                                                   │  │
│   │   ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐              │  │
│   │   │ US1 │ │ US2 │ │ US3 │ │ US4 │ │ US5 │ │ ... │              │  │
│   │   │ P1  │ │ P1  │ │ P2  │ │ P2  │ │ P3  │ │     │              │  │
│   │   └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘              │  │
│   └──────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│                              │ 스프린트 계획 (Sprint Planning)          │
│                              ▼                                          │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │                     Sprint Backlog                                │  │
│   │         (스프린트 백로그: 이번 스프린트에 완료할 항목)             │  │
│   │                                                                   │  │
│   │   ┌─────────────────────────────────────────────────────────┐    │  │
│   │   │                    Sprint (2~4주)                        │    │  │
│   │   │  ┌─────────────────────────────────────────────────┐    │    │  │
│   │   │  │              Daily Scrum (15분)                  │    │    │  │
│   │   │  │  • 어제 뭘 했나?                                 │    │    │  │
│   │   │  │  • 오늘 뭘 할 건가?                              │    │    │  │
│   │   │  │  • 장애물이 있나?                                │    │    │  │
│   │   │  └─────────────────────────────────────────────────┘    │    │  │
│   │   └─────────────────────────────────────────────────────────┘    │  │
│   └──────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│                              │ 스프린트 종료                             │
│                              ▼                                          │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │              Sprint Review              Sprint Retrospective      │  │
│   │         (스프린트 리뷰: 결과 시연)      (회고: 프로세스 개선)      │  │
│   │                                                                   │  │
│   │   "이번 스프린트 완성물 보여드립니다"   "뭘 잘했고, 뭘 개선할까?"  │  │
│   └──────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│                              ▼                                          │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │              Potentially Shippable Increment                      │  │
│   │               (배포 가능한 제품 증분)                             │  │
│   │                                                                   │  │
│   │   Definition of Done (DoD) 충족 시 배포 가능                      │  │
│   │   • 코드 완료 • 테스트 통과 • 코드 리뷰 • 문서화                  │  │
│   └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        칸반 보드 (Kanban Board)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐   │
│   │   할 일    │   │   진행중   │   │   검토중   │   │   완료     │   │
│   │   (To Do)  │   │  (Doing)   │   │  (Review)  │   │   (Done)   │   │
│   ├────────────┤   ├────────────┤   ├────────────┤   ├────────────┤   │
│   │  [WIP: ∞]  │   │  [WIP: 3]  │   │  [WIP: 2]  │   │            │   │
│   ├────────────┤   ├────────────┤   ├────────────┤   ├────────────┤   │
│   │ □ 기능 A   │   │ ■ 기능 D   │   │ ■ 기능 F   │   │ ✓ 기능 H   │   │
│   │ □ 기능 B   │   │ ■ 기능 E   │   │ ■ 기능 G   │   │ ✓ 기능 I   │   │
│   │ □ 기능 C   │   │            │   │            │   │ ✓ 기능 J   │   │
│   └────────────┘   └────────────┘   └────────────┘   └────────────┘   │
│         ↑                                                      │       │
│         │                                                      │       │
│    Backlog ──────────────────────────────────────────────→ Deploy    │
│                                                                         │
│   WIP(Work In Progress) 제한:                                           │
│   • 동시 진행 작업 수 제한으로 병목 현상 가시화                         │
│   • WIP 초과 시 새 작업 시작 금지 (먼저 완료해야 함)                    │
│   • Little's Law: 리드타임 = WIP / 처리율                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**핵심 알고리즘/공식** (해당 시 필수):
```
[벨로시티 (Velocity)]

벨로시티 = 완료된 스토리 포인트 합계 / 스프린트 수

예시:
- 스프린트 1: 21점 완료
- 스프린트 2: 24점 완료
- 스프린트 3: 18점 완료 (병가 등)

평균 벨로시티 = (21 + 24 + 18) / 3 = 21 포인트/스프린트

예상 완료일 = 남은 총 포인트 / 평균 벨로시티 × 스프린트 기간

[리드 타임 & 사이클 타임 (칸반)]

Lead Time = 작업 요청 시점 → 완료 시점 (고객 관점)
Cycle Time = 작업 시작 시점 → 완료 시점 (팀 관점)

Little's Law:
WIP = Throughput × Lead Time
→ Lead Time = WIP / Throughput

예: WIP=5, Throughput=2/일
→ Lead Time = 5 / 2 = 2.5일

[번업/번다운 차트]

        포인트
          ▲
     100  │     ╭───────────────────── 완료 누적 (Actual)
          │    ╱
      80  │   ╱
          │  ╱    ╭─────────────────── 계획 (Planned)
      60  │ ╱    ╱
          │╱    ╱
      40  │    ╱
          │   ╱
      20  │  ╱
          │ ╱
       0  └──────────────────────→ 스프린트
           S1   S2   S3   S4   S5

스코프 변경 감지: 계획선이 올라가면 요구사항 추가
```

**코드 예시** (필수: Python 스크럼 시뮬레이터):
```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Callable
from enum import Enum, auto
from datetime import datetime, timedelta
import random

# ============================================================
# 스크럼 시뮬레이터
# ============================================================

class Priority(Enum):
    """백로그 우선순위"""
    HIGHEST = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    LOWEST = 5


class StoryStatus(Enum):
    """스토리 상태"""
    TODO = auto()
    IN_PROGRESS = auto()
    REVIEW = auto()
    DONE = auto()
    BLOCKED = auto()


@dataclass
class UserStory:
    """사용자 스토리"""
    id: str
    title: str
    description: str
    story_points: int  # 1, 2, 3, 5, 8, 13, 21 (피보나치)
    priority: Priority
    status: StoryStatus = StoryStatus.TODO
    assignee: Optional[str] = None
    tasks: List[str] = field(default_factory=list)
    completed_at: Optional[datetime] = None

    def __str__(self):
        return f"[{self.id}] {self.title} ({self.story_points}SP, {self.priority.name})"


@dataclass
class Sprint:
    """스프린트"""
    number: int
    start_date: datetime
    duration_days: int = 14
    stories: List[UserStory] = field(default_factory=list)
    completed_stories: List[UserStory] = field(default_factory=list)
    velocity: int = 0

    @property
    def end_date(self) -> datetime:
        return self.start_date + timedelta(days=self.duration_days)

    @property
    def committed_points(self) -> int:
        return sum(s.story_points for s in self.stories)

    @property
    def completed_points(self) -> int:
        return sum(s.story_points for s in self.completed_stories)

    def add_story(self, story: UserStory) -> None:
        if story not in self.stories:
            self.stories.append(story)

    def complete_story(self, story: UserStory) -> None:
        if story in self.stories and story not in self.completed_stories:
            story.status = StoryStatus.DONE
            story.completed_at = datetime.now()
            self.completed_stories.append(story)
            self.velocity = self.completed_points


@dataclass
class TeamMember:
    """팀 멤버"""
    name: str
    role: str  # Developer, Tester, Designer, etc.
    capacity: float = 1.0  # 1.0 = 풀타임, 0.5 = 파트타임
    skills: List[str] = field(default_factory=list)


class ProductBacklog:
    """제품 백로그"""

    def __init__(self):
        self.stories: List[UserStory] = []

    def add_story(self, story: UserStory) -> None:
        self.stories.append(story)
        self._sort_by_priority()

    def remove_story(self, story_id: str) -> Optional[UserStory]:
        for i, s in enumerate(self.stories):
            if s.id == story_id:
                return self.stories.pop(i)
        return None

    def _sort_by_priority(self) -> None:
        self.stories.sort(key=lambda s: s.priority.value)

    def get_top_stories(self, max_points: int) -> List[UserStory]:
        """벨로시티에 맞춰 상위 스토리 선택"""
        selected = []
        total_points = 0
        for story in self.stories:
            if total_points + story.story_points <= max_points:
                selected.append(story)
                total_points += story.story_points
        return selected

    @property
    def total_points(self) -> int:
        return sum(s.story_points for s in self.stories)


class ScrumTeam:
    """스크럼 팀"""

    def __init__(self, name: str):
        self.name = name
        self.members: List[TeamMember] = []
        self.product_owner: Optional[str] = None
        self.scrum_master: Optional[str] = None
        self.velocity_history: List[int] = []

    def add_member(self, member: TeamMember) -> None:
        self.members.append(member)

    @property
    def average_velocity(self) -> float:
        if not self.velocity_history:
            return 0
        # 최근 3개 스프린트 평균 (이상치 제거)
        recent = self.velocity_history[-3:]
        return sum(recent) / len(recent)

    def record_velocity(self, velocity: int) -> None:
        self.velocity_history.append(velocity)


class DailyScrum:
    """데일리 스크럼"""

    @dataclass
    class Update:
        member: str
        yesterday: str
        today: str
        blockers: List[str]

    def __init__(self, date: datetime):
        self.date = date
        self.updates: List[DailyScrum.Update] = []
        self.blockers_identified: List[str] = []

    def add_update(self, member: str, yesterday: str,
                   today: str, blockers: List[str] = None) -> None:
        update = DailyScrum.Update(
            member=member,
            yesterday=yesterday,
            today=today,
            blockers=blockers or []
        )
        self.updates.append(update)
        self.blockers_identified.extend(blockers or [])

    def summary(self) -> str:
        lines = [f"\n=== Daily Scrum ({self.date.strftime('%Y-%m-%d')}) ==="]
        for u in self.updates:
            lines.append(f"\n{u.member}:")
            lines.append(f"  어제: {u.yesterday}")
            lines.append(f"  오늘: {u.today}")
            if u.blockers:
                lines.append(f"  ⚠️ 장애물: {', '.join(u.blockers)}")
        if self.blockers_identified:
            lines.append(f"\n🚨 총 {len(self.blockers_identified)}개 장애물 발생")
        return "\n".join(lines)


class SprintRetrospective:
    """스프린트 회고"""

    def __init__(self, sprint_number: int):
        self.sprint_number = sprint_number
        self.what_went_well: List[str] = []
        self.what_to_improve: List[str] = []
        self.action_items: List[str] = []

    def add_good(self, item: str) -> None:
        self.what_went_well.append(item)

    def add_improvement(self, item: str) -> None:
        self.what_to_improve.append(item)

    def add_action(self, action: str, owner: str) -> None:
        self.action_items.append(f"[{owner}] {action}")

    def summary(self) -> str:
        lines = [f"\n=== Sprint {self.sprint_number} 회고 ==="]
        lines.append("\n👍 잘한 점:")
        for item in self.what_went_well:
            lines.append(f"  • {item}")
        lines.append("\n🔧 개선할 점:")
        for item in self.what_to_improve:
            lines.append(f"  • {item}")
        lines.append("\n✅ 액션 아이템:")
        for item in self.action_items:
            lines.append(f"  • {item}")
        return "\n".join(lines)


class ScrumSimulator:
    """스크럼 프로세스 시뮬레이터"""

    def __init__(self, team: ScrumTeam, backlog: ProductBacklog):
        self.team = team
        self.backlog = backlog
        self.sprints: List[Sprint] = []
        self.current_sprint: Optional[Sprint] = None
        self.dail_scrums: List[DailyScrum] = []
        self.retropectives: List[SprintRetrospective] = []

    def plan_sprint(self, sprint_number: int,
                    duration_days: int = 14) -> Sprint:
        """스프린트 계획"""
        # 팀의 평균 벨로시티 기반으로 스토리 선택
        target_velocity = max(self.team.average_velocity, 20)  # 초기값 20

        sprint = Sprint(
            number=sprint_number,
            start_date=datetime.now() + timedelta(days=len(self.sprints) * duration_days),
            duration_days=duration_days
        )

        # 백로그에서 스토리 선택
        selected_stories = self.backlog.get_top_stories(int(target_velocity * 1.1))
        for story in selected_stories:
            sprint.add_story(story)
            self.backlog.remove_story(story.id)

        print(f"\n📋 Sprint {sprint_number} 계획:")
        print(f"   목표 벨로시티: {target_velocity:.1f} SP")
        print(f"   커밋된 스토리: {len(sprint.stories)}개 ({sprint.committed_points}SP)")

        for story in sprint.stories:
            print(f"   - {story}")

        self.current_sprint = sprint
        self.sprints.append(sprint)
        return sprint

    def run_daily_scrum(self) -> DailyScrum:
        """데일리 스크럼 실행"""
        daily = DailyScrum(datetime.now())

        for member in self.team.members:
            # 시뮬레이션: 랜덤 업데이트 생성
            completed = random.choice(["API 개발", "UI 수정", "버그 수정", "테스트 작성"])
            planned = random.choice(["코드 리뷰", "기능 구현", "문서 작성", "테스트"])
            blockers = random.choice([[], ["API 응답 지연"], []])

            daily.add_update(member.name, completed, planned, blockers)

        print(daily.summary())
        self.dail_scrums.append(daily)
        return daily

    def simulate_sprint_progress(self, completion_rate: float = 0.85) -> None:
        """스프린트 진행 시뮬레이션"""
        if not self.current_sprint:
            return

        # 완료율만큼 스토리 완료
        num_to_complete = int(len(self.current_sprint.stories) * completion_rate)
        stories_to_complete = random.sample(
            self.current_sprint.stories,
            min(num_to_complete, len(self.current_sprint.stories))
        )

        for story in stories_to_complete:
            self.current_sprint.complete_story(story)

    def end_sprint(self) -> tuple:
        """스프린트 종료 (리뷰 + 회고)"""
        if not self.current_sprint:
            return None, None

        sprint = self.current_sprint

        # 벨로시티 기록
        self.team.record_velocity(sprint.completed_points)

        # 회고
        retro = SprintRetrospective(sprint.number)
        retro.add_good("팀 협업이 원활했음")
        retro.add_good("데일리 스크럼이 효과적")
        retro.add_improvement("스토리 포인트 추정 정확도 향상 필요")
        retro.add_action("다음 스프린트 플래닝 포커 시간 늘리기", self.team.scrum_master)

        print(f"\n🏁 Sprint {sprint.number} 종료:")
        print(f"   완료된 스토리: {len(sprint.completed_stories)}/{len(sprint.stories)}")
        print(f"   실제 벨로시티: {sprint.completed_points}SP")
        print(f"   커밋 대비: {sprint.completed_points/sprint.committed_points*100:.1f}%")

        print(retro.summary())

        self.retropectives.append(retro)
        self.current_sprint = None

        return sprint, retro

    def get_burndown_data(self, sprint: Sprint) -> Dict:
        """번다운 차트 데이터"""
        days = sprint.duration_days
        total_points = sprint.committed_points
        ideal_daily = total_points / days

        # 이상 번다운
        ideal = [total_points - (ideal_daily * i) for i in range(days + 1)]

        # 실제 번다운 (시뮬레이션)
        actual = [total_points]
        remaining = total_points
        for i in range(1, days + 1):
            # 랜덤하게 진행 (마지막 날에 0에 근접)
            burn = random.uniform(ideal_daily * 0.5, ideal_daily * 1.5)
            remaining = max(0, remaining - burn)
            actual.append(remaining)

        return {
            "days": list(range(days + 1)),
            "ideal": ideal,
            "actual": actual
        }


# ============================================================
# 칸반 시뮬레이터
# ============================================================

@dataclass
class KanbanCard:
    """칸반 카드"""
    id: str
    title: str
    column: str = "Backlog"
    entered_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class KanbanBoard:
    """칸반 보드"""

    def __init__(self, wip_limits: Dict[str, int] = None):
        self.columns = {
            "Backlog": [],
            "Ready": [],
            "Doing": [],
            "Review": [],
            "Done": []
        }
        self.wip_limits = wip_limits or {
            "Ready": 5,
            "Doing": 3,
            "Review": 2
        }
        self.cards: Dict[str, KanbanCard] = {}

    def add_card(self, card: KanbanCard) -> None:
        card.column = "Backlog"
        self.columns["Backlog"].append(card.id)
        self.cards[card.id] = card

    def move_card(self, card_id: str, to_column: str) -> bool:
        """카드 이동 (WIP 제한 확인)"""
        if card_id not in self.cards:
            return False

        card = self.cards[card_id]

        # WIP 제한 확인
        if to_column in self.wip_limits:
            current_count = len(self.columns[to_column])
            if current_count >= self.wip_limits[to_column]:
                print(f"⚠️ {to_column}의 WIP 제한({self.wip_limits[to_column]}) 도달!")
                return False

        # 이동
        if card.column in self.columns and card_id in self.columns[card.column]:
            self.columns[card.column].remove(card_id)

        card.column = to_column
        self.columns[to_column].append(card_id)

        # 타임스탬프 기록
        if to_column == "Doing" and not card.started_at:
            card.started_at = datetime.now()
        elif to_column == "Done":
            card.completed_at = datetime.now()

        return True

    def get_lead_time(self, card_id: str) -> Optional[float]:
        """리드 타임 (Backlog → Done)"""
        card = self.cards.get(card_id)
        if card and card.completed_at:
            return (card.completed_at - card.entered_at).total_seconds() / 3600  # 시간 단위
        return None

    def get_cycle_time(self, card_id: str) -> Optional[float]:
        """사이클 타임 (Doing → Done)"""
        card = self.cards.get(card_id)
        if card and card.started_at and card.completed_at:
            return (card.completed_at - card.started_at).total_seconds() / 3600
        return None

    def print_board(self) -> None:
        """보드 출력"""
        print("\n" + "=" * 70)
        print("                         칸반 보드")
        print("=" * 70)
        for col, cards in self.columns.items():
            wip = self.wip_limits.get(col, "∞")
            print(f"\n{col} [WIP: {len(cards)}/{wip}]")
            print("-" * 40)
            for card_id in cards[:5]:  # 최대 5개만 표시
                card = self.cards[card_id]
                print(f"  □ {card.id}: {card.title}")
            if len(cards) > 5:
                print(f"  ... 외 {len(cards) - 5}개")
        print("=" * 70)


# ============================================================
# 사용 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("              스크럼 시뮬레이터 데모")
    print("=" * 70)

    # 팀 생성
    team = ScrumTeam("애자일 개발팀")
    team.product_owner = "김PO"
    team.scrum_master = "이SM"
    team.add_member(TeamMember("박개발", "Developer", skills=["Python", "React"]))
    team.add_member(TeamMember("최테스터", "Tester", skills=["Selenium", "JMeter"]))
    team.add_member(TeamMember("정디자이너", "Designer", skills=["Figma", "UI/UX"]))

    # 제품 백로그 생성
    backlog = ProductBacklog()
    stories = [
        UserStory("US-001", "로그인 기능", "사용자가 이메일로 로그인할 수 있다", 5, Priority.HIGHEST),
        UserStory("US-002", "회원가입", "신규 사용자가 가입할 수 있다", 8, Priority.HIGHEST),
        UserStory("US-003", "비밀번호 찾기", "비밀번호를 재설정할 수 있다", 3, Priority.HIGH),
        UserStory("US-004", "프로필 수정", "사용자가 프로필을 수정할 수 있다", 5, Priority.MEDIUM),
        UserStory("US-005", "알림 설정", "이메일 알림을 설정할 수 있다", 3, Priority.MEDIUM),
        UserStory("US-006", "검색 기능", "게시물을 검색할 수 있다", 8, Priority.LOW),
        UserStory("US-007", "댓글 작성", "게시물에 댓글을 달 수 있다", 5, Priority.HIGH),
        UserStory("US-008", "좋아요", "게시물에 좋아요를 누를 수 있다", 2, Priority.LOW),
    ]
    for story in stories:
        backlog.add_story(story)

    print(f"\n📦 제품 백로그: {backlog.total_points}SP, {len(backlog.stories)}개 스토리")

    # 스크럼 시뮬레이터 실행
    simulator = ScrumSimulator(team, backlog)

    # Sprint 1
    simulator.plan_sprint(1)
    simulator.run_daily_scrum()
    simulator.simulate_sprint_progress(0.8)
    simulator.end_sprint()

    # Sprint 2
    simulator.plan_sprint(2)
    simulator.run_daily_scrum()
    simulator.simulate_sprint_progress(0.9)
    simulator.end_sprint()

    print(f"\n📊 팀 평균 벨로시티: {team.average_velocity:.1f}SP")

    # 칸반 보드 데모
    print("\n" + "=" * 70)
    print("              칸반 보드 데모")
    print("=" * 70)

    kanban = KanbanBoard({"Ready": 3, "Doing": 2, "Review": 2})
    kanban.add_card(KanbanCard("K-001", "버그 수정"))
    kanban.add_card(KanbanCard("K-002", "기능 개발"))
    kanban.add_card(KanbanCard("K-003", "문서 작성"))

    kanban.move_card("K-001", "Ready")
    kanban.move_card("K-002", "Ready")
    kanban.move_card("K-003", "Ready")

    kanban.move_card("K-001", "Doing")
    kanban.move_card("K-002", "Doing")

    kanban.print_board()

    # WIP 제한 테스트
    print("\nWIP 제한 테스트:")
    kanban.move_card("K-003", "Doing")  # WIP 초과 시도
