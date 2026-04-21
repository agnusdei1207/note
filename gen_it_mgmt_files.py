import os

BASE = "/Users/pf/workspace/brainscience/content/studynote/12_it_management/05_security_compliance"

TOPICS = {
    264: ("264_problem_management_kedb.md", "264. 문제 관리 (Problem Management) 근본 원인 분석 KEDB",
          "문제 관리 (Problem Management)", "KEDB (Known Error Database)",
          "근본 원인(Root Cause) 분석", "재발 방지", "인시던트 관리",
          "인시던트 관리가 화재 진압이라면, 문제 관리는 방화벽 설치다.",
          "여러 인시던트가 반복되면 그 공통 원인을 KEDB에 등록하여 영구 해결책을 찾는 것이 문제 관리다.",
          "반복 인시던트 30~50% 감소, 운영 안정성 향상",
          ["KEDB|Known Error Database - 알려진 오류 저장|인시던트 관리", "RCA|근본 원인 분석|5-WHY 기법", "워크어라운드|임시 해결책|KEDB 연계"]),

    265: ("265_change_management_cab.md", "265. 변경 관리 (Change Management) CAB 승인",
          "변경 관리 (Change Management)", "CAB (Change Advisory Board)",
          "변경 리스크 통제", "서비스 안정성", "릴리스 관리",
          "변경 관리는 수술실 체크리스트다. 모든 변경은 사전 심의를 거쳐야 부작용이 줄어든다.",
          "모든 시스템 변경은 CAB 승인을 거쳐 리스크를 통제한다. 긴급 변경은 ECAB(Emergency CAB)가 즉시 심의한다.",
          "변경 실패율 40~60% 감소, 서비스 중단 예방",
          ["CAB|변경 자문 위원회|변경 심의·승인", "RFC|Request for Change|변경 요청서", "ECAB|긴급 변경 위원회|보안 패치 긴급 처리"]),

    266: ("266_bcp_business_continuity.md", "266. BCP (Business Continuity Plan) 업무 연속성 계획",
          "BCP (Business Continuity Plan, 업무 연속성 계획)", "BCM (Business Continuity Management)",
          "재난·재해 시 핵심 업무 지속", "RTO/RPO 목표 달성", "DR 센터 연계",
          "BCP는 비상구 대피 훈련이다. 평소에 연습해야 실제 재난 때 당황하지 않는다.",
          "재난 시에도 핵심 비즈니스 기능이 중단 없이 지속될 수 있도록 사전에 계획·훈련·테스트하는 체계.",
          "재난 복구 시간 단축, 규제 컴플라이언스(ISO 22301), 비즈니스 신뢰도 향상",
          ["BIA|Business Impact Analysis|업무 영향 분석", "DRS|재해복구시스템|DR 센터", "RTO/RPO|복구 목표|SLA 연계"]),

    267: ("267_bia_business_impact_analysis.md", "267. BIA (Business Impact Analysis) 업무 영향 분석",
          "BIA (Business Impact Analysis, 업무 영향 분석)", "중단 허용 시간 산출",
          "핵심 업무 우선순위 결정", "RTO/RPO 목표 설정", "BCP 수립 근거",
          "BIA는 병원 응급도 분류(KTAS)다. 어느 업무가 중단되면 생명이 위험한지(매출 손실)를 사전에 분류한다.",
          "재해 발생 시 업무 중단이 비즈니스에 미치는 재무적·비재무적 영향을 분석하여 복구 우선순위와 RTO/RPO를 결정한다.",
          "BCP/DRS 투자 우선순위 명확화, 규제 대응, 최소 복구 비용으로 최대 보호",
          ["MAO|최대 허용 중단 시간|BIA 핵심 산출물", "MTPD|최대 허용 서비스 중단 기간|ISO 22301", "BCP|업무 연속성 계획|BIA 기반 수립"]),

    268: ("268_rto_rpo_objectives.md", "268. RTO / RPO 복구 목표 (Recovery Time/Point Objective)",
          "RTO (Recovery Time Objective, 복구 시간 목표)", "RPO (Recovery Point Objective, 복구 시점 목표)",
          "재해 복구 전략 수립 핵심 지표", "DR 등급 결정", "백업 주기 및 DR 사이트 유형 결정",
          "RTO는 병원 응급실 대기 최대 시간, RPO는 마지막 혈액 검사 이후 최대 허용 시간이다.",
          "RTO는 서비스가 중단된 후 복구되기까지의 최대 허용 시간, RPO는 데이터 손실 허용 기준점(최종 복구 가능한 시점)이다.",
          "DR 사이트 등급(미러/핫/웜/콜드) 선택의 객관적 기준 제공, 투자 최적화",
          ["RTO|복구 시간 목표|미러<핫<웜<콜드", "RPO|복구 시점 목표|백업 주기 결정", "DR 사이트|복구 인프라|RTO 달성 수단"]),

    269: ("269_dr_site_types.md", "269. DR 센터 유형 비교 (Mirror/Hot/Warm/Cold Site)",
          "DR (Disaster Recovery, 재해 복구) 센터", "미러 사이트/핫 사이트/웜 사이트/콜드 사이트",
          "RTO 요구 수준에 따른 DR 유형 선택", "비용-복구속도 트레이드오프", "BCP 연계",
          "DR 사이트 선택은 보험 등급 선택이다. 더 빠른 복구(미러)는 더 비싼 보험료를 낸다.",
          "재해 발생 시 업무를 이전하는 복구 센터의 유형을 복구 시간(RTO) 기준으로 분류한 것이다.",
          "RTO/RPO에 맞는 최적 DR 투자, 불필요한 과잉 투자 방지",
          ["미러 사이트|실시간 이중화, RTO≈0|Active-Active", "핫 사이트|인프라+최신 데이터, RTO 4h|Active-Standby", "웜 사이트|인프라+정기 백업, RTO 수일|준비형", "콜드 사이트|공간+전력만, RTO 수주|최소 비용"]),

    270: ("270_investment_analysis_roi_npv.md", "270. IT 투자 타당성 분석 지표 종합 (ROI/NPV/IRR/PP)",
          "ROI (Return on Investment, 투자수익률)", "NPV (Net Present Value, 순현재가치) / IRR / PP",
          "IT 투자의 경제적 타당성 객관적 산출", "이사회·경영진 의사결정 지원", "IT BSC 재무 관점",
          "ROI/NPV/IRR은 투자 신호등이다. 세 등이 모두 초록불이어야 투자를 진행한다.",
          "IT 시스템 도입 시 재무적 타당성을 ROI(수익률), NPV(현재가치 합산), IRR(내부수익률), PP(투자회수기간)로 다각 분석한다.",
          "IT 투자의 사전 타당성 검증, 불필요한 투자 방지, 예산 최적화",
          ["ROI|투자대비 수익|(이익-비용)/비용×100%", "NPV|순현재가치|NPV>0 이면 타당", "IRR|내부수익률|IRR>자본비용 이면 타당", "PP|투자회수기간|짧을수록 선호"]),
}

def make_content(num, filename, title, concept, concept2, value1, value2, value3, analogy1, desc, conclusion, concepts):
    rows = "\n".join([f"| {c[0]} | {c[1]} | {c[2]} |" for c in concepts])
    return f"""+++
weight = {num}
title = "{title}"
date = "2026-04-21"
[extra]
categories = "studynote-it-management"
+++

## 핵심 인사이트
> 1. **본질**: {desc}
> 2. **가치**: {value1}과 {value2}의 관점에서 {value3}을 달성한다.
> 3. **판단 포인트**: {concept2}의 정확성과 측정 가능성이 성공의 핵심이다.

## Ⅰ. 개요 및 필요성

{concept}은(는) {desc} 현대 IT 경영 환경에서 불가결한 관리 체계이다.

{value1} 측면에서 {concept2}를 통해 의사결정의 객관적 근거를 제공하며, 조직의 IT 거버넌스 수준을 높인다.

📢 **섹션 요약 비유**: {analogy1}

## Ⅱ. 아키텍처 및 핵심 원리

```
┌─────────────────────────────────────┐
│  {concept[:20]:<20} 핵심 구조        │
├─────────────────────────────────────┤
│  입력(Input) → 프로세스 → 출력(Output)│
│  목표 설정 → 측정 → 분석 → 개선     │
└─────────────────────────────────────┘
```

| 구성 요소 | 설명 | 비고 |
|:---|:---|:---|
| 목표 정의 | {value1} 관점 목표 | 정량적 지표 |
| 측정 방법 | {concept2} 기반 | 주기적 보고 |
| 개선 활동 | PDCA 사이클 | 지속 개선 |

📢 **섹션 요약 비유**: 이 구조는 자동차 계기판처럼 현재 상태를 실시간으로 보여주고 이상 징후를 알려준다.

## Ⅲ. 비교 및 연결

| 관련 개념 | 차이점 | 연관성 |
|:---|:---|:---|
| {concepts[0][0]} | {concepts[0][1]} | {concepts[0][2]} |
| {concepts[1][0]} | {concepts[1][1]} | {concepts[1][2]} |

📢 **섹션 요약 비유**: 각 개념은 같은 목표를 향한 다른 도구들이다. 칼(분석)과 포크(실행)처럼 함께 써야 효과적이다.

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 {concept}을(를) 적용할 때 가장 중요한 것은 {value2}와의 연계다. 측정 지표가 비즈니스 목표와 일치하지 않으면 활동은 있으나 가치가 없는 상황이 발생한다.

기술사 시험에서는 "{concept}의 개념, 구성 요소, 실무 적용 방안을 논하라"가 단골 출제 유형이다.

📢 **섹션 요약 비유**: {concept}의 실무 적용은 나침반과 지도를 동시에 보며 등산하는 것이다. 하나만 봐선 길을 잃는다.

## Ⅴ. 기대효과 및 결론

{conclusion} {concept}의 체계적 도입으로 조직의 IT 운영 성숙도(CMMI 기준)가 향상되고 이해관계자 신뢰가 구축된다.

📢 **섹션 요약 비유**: {concept}은 조직의 성장에 따라 점점 더 중요해지는 기초 체력 훈련이다.

### 📌 관련 개념 맵
| 개념 | 설명 | 연관 키워드 |
|:---|:---|:---|
{rows}

### 👶 어린이를 위한 3줄 비유 설명
1. {concept}은(는) 학교 성적표처럼 지금 어떻게 하고 있는지 숫자로 알려주는 도구예요.
2. 잘하는 과목과 못하는 과목을 파악해서 어디를 더 공부해야 할지 알 수 있어요.
3. 목표를 정하고 측정하고 개선하는 과정을 계속 반복하면 점점 나아져요.
"""

for num, data in TOPICS.items():
    filename = data[0]
    filepath = os.path.join(BASE, filename)
    if not os.path.exists(filepath):
        content = make_content(num, filename, data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created {filename}")
    else:
        print(f"Skipped (exists): {filename}")

print("Done!")
