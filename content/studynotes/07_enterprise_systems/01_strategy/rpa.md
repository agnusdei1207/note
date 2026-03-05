+++
title = "RPA (Robotic Process Automation)"
date = "2026-03-04"
[extra]
categories = "studynotes-enterprise"
++-

# RPA (Robotic Process Automation, 로봇 프로세스 자동화)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인간이 수행하던 **규칙 기반의 반복적 사무 작업을 소프트웨어 로봇(Bot)이 대체**하여 자동화하는 기술로, 기존 시스템을 변경하지 않고 UI를 통해 작업을 수행합니다.
> 2. **가치**: 생산성 향상(24/7 가동), 인건비 절감, 오류 제로화, 규제 준수(Compliance) 실현을 통해 디지털 트랜스포메이션의 핵심 동력이 됩니다.
> 3. **융합**: AI/ML과 결합한 지능형 자동화(Intelligent Automation), 하이퍼자동화(Hyperautomation), Low-Code 플랫폼으로 진화하고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. RPA의 개념 및 철학적 근간
로봇 프로세스 자동화(RPA, Robotic Process Automation)는 인간이 컴퓨터로 수행하던 **규칙적이고 반복적인 작업을 소프트웨어 로봇이 자동으로 수행**하게 하는 기술입니다. RPA의 핵심 철학은 **"사람이 하는 일을 그대로 흉내 내어 자동화한다"**는 것입니다. API 통합이나 시스템 개발 없이, **사람이 화면에서 클릭하고 타이핑하는 동작을 로봇이 그대로 수행**합니다. 이를 "Non-Invasive"하다고 표현합니다. 기존 시스템을 건드리지 않고도 자동화가 가능하다는 점이 RPA의 가장 큰 장점입니다.

#### 2. 💡 비유를 통한 이해: 자동판매기
편의점 점원이 음료수를 직접 건네주는 대신, **자동판매기(RPA 봇)**가 그 역할을 합니다. 손님(사용자)이 돈을 넣고 버튼을 누르면(트리거), 기계가 음료수를 꺼내줍니다(작업 수행). 점원은 이제 더 가치 있는 일(고객 응대, 매장 관리)을 할 수 있습니다. RPA는 화면(UI)을 통해 작동한다는 점에서 자동판매기와 유사합니다. 손님이 보는 것과 똑같은 화면을 보고 작동합니다.

#### 3. 등장 배경 및 발전 과정
- **2000년대 초**: Screen Scraping, Macro Recorder 등 초기 자동화 도구
- **2005년**: Blue Prism, UiPath, Automation Anywhere 창업
- **2010년대**: RPA 1.0 - 규칙 기반 반복 작업 자동화
- **2018년~**: RPA 2.0 - AI/ML 결합, Cognitive RPA
- **2020년~**: Hyperautomation - RPA + AI + Process Mining + Low-Code

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. RPA 봇의 유형

| 유형 | 영문 | 특징 | 예시 |
| :--- | :--- | :--- | :--- |
| **Attended Bot** | 참여형 | 사람과 함께 작동, 사용자 트리거 | CS 상담원 지원 |
| **Unattended Bot** | 무인형 | 서버에서 독립 실행, 스케줄 기반 | 야간 배치 처리 |
| **Hybrid Bot** | 하이브리드 | 참여형 + 무인형 조합 | 승인 프로세스 |

#### 2. RPA 아키텍처 다이어그램

```text
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        [ RPA PLATFORM ARCHITECTURE ]                                │
│                                                                                     │
│  ┌───────────────────────────────────────────────────────────────────────────────┐ │
│  │                    [ ORCHESTRATOR (중앙 관제 서버) ]                           │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐             │ │
│  │  │  스케줄러   │ │  봇 관리    │ │  큐 관리    │ │  모니터링   │             │ │
│  │  │ Scheduler   │ │ Bot Manager │ │Queue Manager│ │ Monitoring  │             │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘             │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐             │ │
│  │  │  사용자     │ │  버전 관리  │ │  로그/감사  │  │ 자산 저장소 │             │ │
│  │  │  관리       │ │ Versioning  │ │ Audit Log   │ │ Asset Store │             │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘             │ │
│  └───────────────────────────────────────┬───────────────────────────────────────┘ │
│                                          │                                          │
│                    ┌─────────────────────┼─────────────────────┐                   │
│                    │                     │                     │                   │
│                    ▼                     ▼                     ▼                   │
│  ┌───────────────────────────────────────────────────────────────────────────────┐ │
│  │                       [ BOT RUNTIME (봇 실행 환경) ]                           │ │
│  │                                                                                 │ │
│  │  ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐   │ │
│  │  │  Attended Bot   │         │ Unattended Bot  │         │   Hybrid Bot    │   │ │
│  │  │  (사용자 PC)    │         │  (서버/VM)      │         │  (혼합)         │   │ │
│  │  │  ┌───────────┐  │         │  ┌───────────┐  │         │  ┌───────────┐  │   │ │
│  │  │  │Bot Agent  │  │         │  │Bot Agent  │  │         │  │Bot Agent  │  │   │ │
│  │  │  │(UI 자동화)│  │         │  │(백그라운드)│   │         │  │(지능형)   │  │   │ │
│  │  │  └───────────┘  │         │  └───────────┘  │         │  └───────────┘  │   │ │
│  │  └─────────────────┘         └─────────────────┘         └─────────────────┘   │ │
│  └───────────────────────────────────────────────────────────────────────────────┘ │
│                                          │                                          │
│                                          ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────────────┐ │
│  │                    [ TARGET APPLICATIONS (대상 시스템) ]                       │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐     │ │
│  │  │   ERP   │ │   CRM   │ │  Excel  │ │   Web   │ │  Email  │ │ Legacy  │     │ │
│  │  │ (SAP)   │ │(Salesforce)│(Office)│ │ (HTML)  │ │(Outlook)│ │(Mainfra)│     │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘     │ │
│  │                    ▲ UI 계층을 통해 상호작용 (API 불필요) ▲                    │ │
│  └───────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                     │
│  ┌───────────────────────────────────────────────────────────────────────────────┐ │
│  │                    [ AI / INTELLIGENCE LAYER (선택적) ]                        │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐             │ │
│  │  │    OCR     │ │    NLP     │ │    ML      │ │   Computer  │             │ │
│  │  │ (문자인식) │ │(자연어처리)│ │  (예측)    │ │   Vision    │             │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘             │ │
│  └───────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

#### 2. RPA 작업 자동화 프로세스

| 단계 | 활동 | 설명 |
| :--- | :--- | :--- |
| **1. 발견(Discovery)** | 프로세스 마이닝, 태스크 마이닝 | 자동화 대상 프로세스 식별 |
| **2. 설계(Design)** | 프로세스 매핑, PDD 작성 | 자동화 시나리오 설계 |
| **3. 개발(Development)** | 봇 개발, 테스트 | Studio에서 워크플로우 구현 |
| **4. 배포(Deploy)** | Orchestrator 배포 | 운영 환경에 배포 |
| **5. 운영(Operate)** | 스케줄 실행, 모니터링 | 24/7 자동화 운영 |
| **6. 최적화(Optimize)** | 성능 측정, 개선 | 지속적 프로세스 개선 |

#### 3. RPA + AI 융합 (지능형 자동화)

```python
"""
RPA + AI 융합 예시: 송장 처리 자동화
- OCR: 송장 이미지에서 텍스트 추출
- NLP: 텍스트에서 핵심 정보 추출 (공급자, 금액, 날짜)
- RPA: ERP 시스템에 자동 입력
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import re

@dataclass
class InvoiceData:
    """송장 데이터 구조"""
    invoice_number: str
    vendor_name: str
    invoice_date: datetime
    total_amount: float
    tax_amount: float
    line_items: List[dict]

class OCRModule:
    """OCR 모듈 (시뮬레이션)"""

    def extract_text(self, image_path: str) -> str:
        """이미지에서 텍스트 추출"""
        # 실제로는 Tesseract, Google Vision API 등 사용
        return """
        세 금 계 산 서
        공급자: ABC 주식회사
        사업자번호: 123-45-67890
        공급받는자: XYZ 회사

        품명          수량    단가      금액
        ----------------------------------------
        노트북        2      1,500,000  3,000,000
        모니터        3        300,000    900,000
        ----------------------------------------
        합계                            3,900,000
        부가세(10%)                       390,000
        총합                            4,290,000

        발행일: 2024-01-15
        승인번호: INV-2024-00123
        """

class NLPExtractor:
    """NLP 기반 정보 추출"""

    def extract_invoice_data(self, ocr_text: str) -> InvoiceData:
        """OCR 텍스트에서 송장 정보 추출"""
        # 정규식 기반 추출 (실제로는 NER 모델 사용)
        vendor_match = re.search(r'공급자:\s*(.+)', ocr_text)
        vendor = vendor_match.group(1).strip() if vendor_match else "Unknown"

        date_match = re.search(r'발행일:\s*(\d{4}-\d{2}-\d{2})', ocr_text)
        invoice_date = datetime.strptime(date_match.group(1), '%Y-%m-%d') if date_match else datetime.now()

        invoice_match = re.search(r'승인번호:\s*(.+)', ocr_text)
        invoice_number = invoice_match.group(1).strip() if invoice_match else "Unknown"

        total_match = re.search(r'총합\s+([\d,]+)', ocr_text)
        total = int(total_match.group(1).replace(',', '')) if total_match else 0

        tax_match = re.search(r'부가세\(10%\)\s+([\d,]+)', ocr_text)
        tax = int(tax_match.group(1).replace(',', '')) if tax_match else 0

        return InvoiceData(
            invoice_number=invoice_number,
            vendor_name=vendor,
            invoice_date=invoice_date,
            total_amount=total,
            tax_amount=tax,
            line_items=[]  # 간소화
        )

class RPABot:
    """RPA 봇 (시뮬레이션)"""

    def __init__(self, bot_name: str):
        self.bot_name = bot_name
        self.execution_log: List[dict] = []

    def login_erp(self, username: str, password: str) -> bool:
        """ERP 시스템 로그인"""
        print(f"[{self.bot_name}] ERP 로그인 시도: {username}")
        self.execution_log.append({
            "action": "LOGIN",
            "timestamp": datetime.now(),
            "status": "SUCCESS"
        })
        return True

    def enter_invoice(self, invoice: InvoiceData) -> bool:
        """송장 정보 ERP 입력"""
        print(f"[{self.bot_name}] 송장 입력 시작: {invoice.invoice_number}")
        print(f"  - 공급자: {invoice.vendor_name}")
        print(f"  - 금액: {invoice.total_amount:,}원")
        print(f"  - 부가세: {invoice.tax_amount:,}원")

        self.execution_log.append({
            "action": "ENTER_INVOICE",
            "invoice_number": invoice.invoice_number,
            "timestamp": datetime.now(),
            "status": "SUCCESS"
        })
        return True

    def submit_for_approval(self, invoice_number: str) -> bool:
        """승인 요청 제출"""
        print(f"[{self.bot_name}] 승인 요청 제출: {invoice_number}")
        self.execution_log.append({
            "action": "SUBMIT_APPROVAL",
            "invoice_number": invoice_number,
            "timestamp": datetime.now(),
            "status": "SUCCESS"
        })
        return True

    def send_notification(self, recipient: str, message: str):
        """이메일 알림 발송"""
        print(f"[{self.bot_name}] 알림 발송 to {recipient}: {message[:30]}...")
        self.execution_log.append({
            "action": "SEND_NOTIFICATION",
            "recipient": recipient,
            "timestamp": datetime.now()
        })

class IntelligentInvoiceProcessor:
    """지능형 송장 처리 시스템 (RPA + AI)"""

    def __init__(self):
        self.ocr = OCRModule()
        self.nlp = NLPExtractor()
        self.bot = RPABot("InvoiceBot-001")

    def process_invoice(self, image_path: str) -> dict:
        """송장 처리 전체 프로세스"""
        result = {
            "status": "PROCESSING",
            "start_time": datetime.now(),
            "steps": []
        }

        try:
            # Step 1: OCR 텍스트 추출
            print("\n=== Step 1: OCR 텍스트 추출 ===")
            ocr_text = self.ocr.extract_text(image_path)
            result["steps"].append({"step": "OCR", "status": "SUCCESS"})

            # Step 2: NLP 정보 추출
            print("\n=== Step 2: NLP 정보 추출 ===")
            invoice_data = self.nlp.extract_invoice_data(ocr_text)
            print(f"추출된 송장 번호: {invoice_data.invoice_number}")
            print(f"공급자: {invoice_data.vendor_name}")
            print(f"총액: {invoice_data.total_amount:,}원")
            result["steps"].append({"step": "NLP_EXTRACTION", "status": "SUCCESS"})
            result["extracted_data"] = invoice_data.__dict__

            # Step 3: RPA ERP 입력
            print("\n=== Step 3: RPA ERP 입력 ===")
            self.bot.login_erp("automation_user", "encrypted_password")
            self.bot.enter_invoice(invoice_data)
            result["steps"].append({"step": "ERP_ENTRY", "status": "SUCCESS"})

            # Step 4: 승인 요청
            print("\n=== Step 4: 승인 요청 ===")
            self.bot.submit_for_approval(invoice_data.invoice_number)
            result["steps"].append({"step": "APPROVAL_REQUEST", "status": "SUCCESS"})

            # Step 5: 알림 발송
            print("\n=== Step 5: 알림 발송 ===")
            self.bot.send_notification(
                "finance@company.com",
                f"송장 {invoice_data.invoice_number} 입력 완료, 승인 대기 중"
            )
            result["steps"].append({"step": "NOTIFICATION", "status": "SUCCESS"})

            result["status"] = "COMPLETED"

        except Exception as e:
            result["status"] = "FAILED"
            result["error"] = str(e)

        result["end_time"] = datetime.now()
        result["duration_seconds"] = (result["end_time"] - result["start_time"]).total_seconds()

        return result

# 실행 예시
if __name__ == "__main__":
    processor = IntelligentInvoiceProcessor()
    result = processor.process_invoice("/invoices/scan_001.png")

    print(f"\n{'='*50}")
    print(f"처리 결과: {result['status']}")
    print(f"소요 시간: {result['duration_seconds']:.2f}초")
    print(f"완료 단계: {len(result['steps'])}단계")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 자동화 기술 비교

| 기술 | 대상 | 방식 | 복잡도 | 적합한 작업 |
| :--- | :--- | :--- | :--- | :--- |
| **RPA** | UI | 비침투적 | 낮음 | 규칙 기반 반복 |
| **API 통합** | API | 침투적 | 중간 | 시스템 간 연동 |
| **BPM** | 프로세스 | 오케스트레이션 | 높음 | 워크플로우 관리 |
| **AI/ML** | 데이터 | 지능형 | 높음 | 판단 필요 작업 |

#### 2. 과목 융합 관점 분석
- **BPM (Business Process Management)**: RPA는 BPM의 실행 엔진으로 활용됩니다. BPM이 프로세스를 정의하고, RPA가 작업을 수행합니다.
- **AI (Artificial Intelligence)**: RPA + AI = 지능형 자동화(Intelligent Automation). OCR, NLP, Computer Vision과 결합하여 비정형 작업도 자동화합니다.
- **클라우드 (Cloud RPA)**: UiPath Automation Cloud, Microsoft Power Automate 등 클라우드 기반 RPA가 확산되고 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단: RPA 도입 대상 선정 기준
**[상황]** O기업은 RPA 도입을 검토합니다. 어떤 작업을 우선 자동화할까요?

| 평가 기준 | 높은 점수 | 낮은 점수 |
| :--- | :--- | :--- |
| **반복성** | 매일 발생 | 가끔 발생 |
| **규칙성** | 명확한 규칙 | 판단 필요 |
| **표준화** | 절차 고정 | 절차 가변 |
| **데이터** | 정형 데이터 | 비정형 데이터 |
| **시스템** | UI 접근 가능 | API만 가능 |

**[ROI 높은 작업]**: 송장 처리, 데이터 입력, 리포트 생성, 이메일 분류, 계정 생성

#### 2. 도입 시 고려사항 (Checklist)
- **예외 처리**: 규칙에서 벗어나는 케이스 처리 방안
- **보안**: 봇 계정 권한, 암호화
- **유지보수**: UI 변경 시 봇 수정 필요

#### 3. 안티패턴 (Anti-patterns)
- **"모든 것을 RPA로"**: API 통합이 더 효율적인 작업까지 RPA로 처리
- **"예외 처리 무시"**: 규칙 기반이므로 예외 케이스가 많으면 실패

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 개선 항목 | RPA 도입 시 기대효과 |
| :--- | :--- | :--- |
| **생산성** | 처리 시간 | 50~90% 단축 |
| **정확성** | 오류율 | 0% (100% 정확) |
| **비용** | 인건비 | 30~50% 절감 |
| **가용성** | 업무 시간 | 24/7/365 |

#### 2. 미래 전망: 하이퍼자동화 (Hyperautomation)
- **RPA + AI + Process Mining + Low-Code**의 결합
- **Self-healing RPA**: UI 변경 시 자동 대응
- ** democratization**: 일반 직원도 쉽게 봇 개발 (Citizen Developer)

#### 3. 참고 기술 및 플랫폼
- **UiPath**: 시장 점유율 1위 RPA 플랫폼
- **Automation Anywhere**: 클라우드 네이티브 RPA
- **Microsoft Power Automate**: Office 365 통합 RPA

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [BPM (Business Process Management)](@/studynotes/07_enterprise_systems/03_crm_bpm/bpm.md): RPA의 상위 프로세스 관리 체계
- [프로세스 마이닝 (Process Mining)](@/studynotes/07_enterprise_systems/03_crm_bpm/process_mining.md): RPA 대상 발견 도구
- [AI (Artificial Intelligence)](@/studynotes/06_ict_convergence/04_ai/ai.md): RPA와 결합하는 지능형 기술
- [Low-Code/No-Code](@/studynotes/06_ict_convergence/02_devops/low_code.md): RPA 개발 민주화 플랫폼
- [하이퍼자동화 (Hyperautomation)](@/studynotes/07_enterprise_systems/01_strategy/hyperautomation.md): RPA + AI + Process Mining 통합

---

### 👶 어린이를 위한 3줄 비유 설명
1. RPA는 컴퓨터 화면에서 사람 대신 일하는 '로봇 비서'와 같아요.
2. "이 파일을 여기서 저기로 옮겨줘", "이 숫자를 더해서 표를 만들어줘"라고 시키면, 로봇이 밤낮없이 열심히 일해요.
3. 로봇이 단순한 일을 다 하니까, 사람은 더 중요하고 재미있는 일을 할 수 있게 된답니다!
