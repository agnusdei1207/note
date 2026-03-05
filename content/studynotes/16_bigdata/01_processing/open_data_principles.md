+++
title = "오픈데이터 원칙 (FAIR)"
categories = ["studynotes-16_bigdata"]
+++

# 오픈데이터 원칙 (FAIR)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: FAIR 원칙은 데이터가 Findable(검색 가능), Accessible(접근 가능), Interoperable(상호운용 가능), Reusable(재사용 가능)하도록 만드는 국제 표준 가이드라인이다.
> 2. **가치**: FAIR 원칙을 준수하면 데이터 검색 시간을 80% 단축하고, 데이터 통합 비용을 60% 절감하며, 연구 재현성을 크게 향상시킨다.
> 3. **융합**: 메타데이터 표준, DOI, 온톨로지, 데이터 카탈로그와 결합하여 연구 데이터 관리와 공공데이터 개방의 핵심 원칙으로 자리 잡았다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

FAIR 원칙은 2016년 FORCE11 컨소시엄에서 제안한 데이터 관리 원칙으로, 연구 데이터와 디지털 자산이 기계적으로나 사람에 의해나 쉽게 발견되고, 접근되고, 상호운용되고, 재사용될 수 있도록 하는 지침이다.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FAIR 원칙 구조                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│              ┌─────────────────────────────────────────┐               │
│              │           FAIR 원칙                     │               │
│              └─────────────────┬───────────────────────┘               │
│                                │                                       │
│      ┌────────────┬────────────┼────────────┬────────────┐            │
│      │            │            │            │            │            │
│      ▼            ▼            ▼            ▼            ▼            │
│  ┌───────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │Findable│  │Accessible│  │Interoperable│  │Reusable│               │
│  │검색 가능│  │접근 가능 │  │상호운용 가능│  │재사용 가능│             │
│  └─────┬───┘  └─────┬────┘  └─────┬─────┘  └─────┬────┘               │
│        │            │            │              │                      │
│        ▼            ▼            ▼              ▼                      │
│  ┌───────────┐┌───────────┐┌───────────┐┌───────────┐                │
│  │F1: 메타데이터││A1: 프로토콜││I1: 표준어휘││R1: 라이선스│              │
│  │F2: 식별자  ││A2: 인증   ││I2: 어휘매핑││R2: 출처   │              │
│  │F3: 색인   ││A3: 지속성 ││I3: 참조   ││R3: 커뮤니티│              │
│  │F4: 검색   ││           ││           ││   표준   │                │
│  └───────────┘└───────────┘└───────────┘└───────────┘                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 💡 비유

FAIR 원칙은 "잘 정리된 도서관"에 비유할 수 있다. 책이 도서관에 있다면(Findable), 누구나 대출할 수 있고(Accessible), 다른 도서관과 분류 체계가 같아서(Interoperable), 출처가 명확해서 인용할 수 있다면(Reusable), 그 도서관은 FAIR하다.

### 등장 배경 및 발전 과정

1. **2014년**: LOD (Linked Open Data) 운동에서 데이터 상호운용성 논의 시작
2. **2016년**: FORCE11에서 FAIR 원칙 최초 발표 (Wilkinson et al., Scientific Data)
3. **2017년**: EU H2020 프로그램에서 FAIR 준수 의무화
4. **2020년**: 한국 과학기술정보통신부 연구 데이터 FAIR 가이드라인 발표

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### FAIR 원칙 15개 세부 항목

| 원칙 | 세부 항목 | 설명 | 기술 요소 |
|------|-----------|------|-----------|
| **F**indable | F1 | (메타)데이터에 전역적 고유 식별자 부여 | DOI, URN, UUID |
| | F2 | 데이터가 풍부한 메타데이터로 설명됨 | Dublin Core, Schema.org |
| | F3 | 메타데이터가 데이터 식별자를 명시 포함 | 레퍼런스 링크 |
| | F4 | (메타)데이터가 검색 가능한 리소스에 등록 | DataCite, CKAN |
| **A**ccessible | A1 | (메타)데이터가 표준 프로토콜로 검색 | HTTP, FTP, API |
| | A1.1 | 프로토콜이 개방적이고 무료 | OpenAPI, OAI-PMH |
| | A1.2 | 인증 및 권한 부여 절차 제공 | OAuth, API Key |
| | A2 | 데이터가 삭제되어도 메타데이터는 접근 가능 | 영구 보존 정책 |
| **I**nteroperable | I1 | (메타)데이터가 지식 표현 언어로 표현 | RDF, JSON-LD |
| | I2 | (메타)데이터가 어휘를 사용하여 FAIR 원칙 준수 | SKOS, Ontology |
| | I3 | (메타)데이터가 다른 메타데이터를 참조 | Linked Data |
| **R**eusable | R1 | (메타)데이터가 정확한 속성 및 라이선스 포함 | CC License |
| | R1.1 | (메타)데이터의 라이선스 명확히 게시 | CC-BY, CC0 |
| | R1.2 | (메타)데이터의 출처 상세 정보 포함 | Provenance |
| | R1.3 | (메타)데이터가 커뮤니티 표준 준수 | Domain Standards |

### FAIR 데이터셋 구조 예시

```json
{
  "@context": "https://schema.org/",
  "@type": "Dataset",
  "@id": "https://doi.org/10.1234/example-dataset",

  "name": "서울시 대기질 측정 데이터 (2023)",
  "description": "서울시 25개 구의 일별 대기질 측정 데이터",

  "creator": {
    "@type": "Organization",
    "name": "서울특별시 기후환경본부",
    "url": "https://climate.seoul.go.kr"
  },

  "datePublished": "2024-01-15",
  "dateModified": "2024-03-01",
  "temporalCoverage": "2023-01-01/2023-12-31",
  "spatialCoverage": {
    "@type": "Place",
    "name": "Seoul, South Korea",
    "geo": {
      "@type": "GeoShape",
      "box": "37.413 126.734 37.715 127.269"
    }
  },

  "distribution": {
    "@type": "DataDownload",
    "contentUrl": "https://data.seoul.go.kr/dataList/OA-1551/S/1/datasetView.do",
    "encodingFormat": "CSV",
    "contentSize": "50MB",
    "license": "https://creativecommons.org/licenses/by/4.0/"
  },

  "keywords": [
    "대기질", "미세먼지", "초미세먼지", "오존", "이산화질소"
  ],

  "measurementTechnique": "Beta-ray absorption method",
  "variableMeasured": [
    {
      "@type": "PropertyValue",
      "name": "PM10",
      "description": "미세먼지 농도 (μg/m³)"
    },
    {
      "@type": "PropertyValue",
      "name": "PM2.5",
      "description": "초미세먼지 농도 (μg/m³)"
    }
  ],

  "isAccessibleForFree": true,
  "usageInfo": "출처 표기 시 자유 이용 가능"
}
```

### FAIR 준수 자가 진단 도구

```python
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

class FAIRPrinciple(Enum):
    F1 = "F1: 전역 식별자 존재"
    F2 = "F2: 풍부한 메타데이터"
    F3 = "F3: 식별자 명시"
    F4 = "F4: 검색 가능 등록"
    A1 = "A1: 표준 프로토콜"
    A2 = "A2: 메타데이터 지속성"
    I1 = "I1: 지식 표현 언어"
    I2 = "I2: 어휘 사용"
    I3 = "I3: 참조 포함"
    R1 = "R1: 라이선스 명시"
    R2 = "R2: 출처 상세"
    R3 = "R3: 커뮤니티 표준"

@dataclass
class FAIRAssessment:
    """FAIR 평가 결과"""
    principle: FAIRPrinciple
    compliant: bool
    score: float  # 0~1
    evidence: str
    suggestions: List[str]

class FAIREvaluator:
    """FAIR 준수 평가기"""

    def __init__(self, dataset_metadata: Dict):
        self.metadata = dataset_metadata
        self.assessments: List[FAIRAssessment] = []

    def evaluate_all(self) -> Dict:
        """전체 FAIR 평가"""
        return {
            "findable": self._evaluate_findable(),
            "accessible": self._evaluate_accessible(),
            "interoperable": self._evaluate_interoperable(),
            "reusable": self._evaluate_reusable(),
            "overall_score": self._calculate_overall_score()
        }

    def _evaluate_findable(self) -> Dict:
        """F (Findable) 평가"""
        results = {}

        # F1: 전역 식별자
        has_doi = "@id" in self.metadata or "doi" in self.metadata
        results["F1"] = FAIRAssessment(
            principle=FAIRPrinciple.F1,
            compliant=has_doi,
            score=1.0 if has_doi else 0.0,
            evidence="DOI 또는 고유 식별자 존재" if has_doi else "식별자 없음",
            suggestions=[] if has_doi else ["DOI 발급 권장 (DataCite)"]
        )

        # F2: 풍부한 메타데이터
        required_fields = ["name", "description", "creator", "datePublished"]
        present_fields = sum(1 for f in required_fields if f in self.metadata)
        score = present_fields / len(required_fields)
        results["F2"] = FAIRAssessment(
            principle=FAIRPrinciple.F2,
            compliant=score >= 0.75,
            score=score,
            evidence=f"{present_fields}/{len(required_fields)} 필드 존재",
            suggestions=[] if score >= 0.75 else ["메타데이터 필드 보완 필요"]
        )

        # F3: 식별자 명시
        has_id_ref = "@id" in self.metadata or "identifier" in self.metadata
        results["F3"] = FAIRAssessment(
            principle=FAIRPrinciple.F3,
            compliant=has_id_ref,
            score=1.0 if has_id_ref else 0.0,
            evidence="식별자 참조 존재" if has_id_ref else "식별자 참조 없음",
            suggestions=[]
        )

        # F4: 검색 가능 등록
        is_indexed = self.metadata.get("isAccessibleForFree", False)
        results["F4"] = FAIRAssessment(
            principle=FAIRPrinciple.F4,
            compliant=is_indexed,
            score=1.0 if is_indexed else 0.0,
            evidence="공개 접근 가능" if is_indexed else "공개 여부 불명",
            suggestions=[] if is_indexed else ["공개 데이터 저장소 등록 권장"]
        )

        return results

    def _evaluate_accessible(self) -> Dict:
        """A (Accessible) 평가"""
        results = {}

        # A1: 표준 프로토콜
        distribution = self.metadata.get("distribution", {})
        has_url = "contentUrl" in distribution
        results["A1"] = FAIRAssessment(
            principle=FAIRPrinciple.A1,
            compliant=has_url,
            score=1.0 if has_url else 0.0,
            evidence="다운로드 URL 존재" if has_url else "URL 없음",
            suggestions=[]
        )

        # A2: 메타데이터 지속성
        has_license = "license" in distribution
        results["A2"] = FAIRAssessment(
            principle=FAIRPrinciple.A2,
            compliant=has_license,
            score=1.0 if has_license else 0.0,
            evidence="라이선스 명시" if has_license else "라이선스 없음",
            suggestions=[] if has_license else ["CC 라이선스 명시 권장"]
        )

        return results

    def _evaluate_interoperable(self) -> Dict:
        """I (Interoperable) 평가"""
        results = {}

        # I1: 지식 표현 언어
        has_context = "@context" in self.metadata
        results["I1"] = FAIRAssessment(
            principle=FAIRPrinciple.I1,
            compliant=has_context,
            score=1.0 if has_context else 0.0,
            evidence="JSON-LD 컨텍스트 존재" if has_context else "구조화 포맷 없음",
            suggestions=[] if has_context else ["JSON-LD 또는 RDF 포맷 권장"]
        )

        # I2: 어휘 사용
        has_keywords = "keywords" in self.metadata
        results["I2"] = FAIRAssessment(
            principle=FAIRPrinciple.I2,
            compliant=has_keywords,
            score=1.0 if has_keywords else 0.0,
            evidence="키워드 존재" if has_keywords else "키워드 없음",
            suggestions=[] if has_keywords else ["표준 어휘 사용 권장"]
        )

        return results

    def _evaluate_reusable(self) -> Dict:
        """R (Reusable) 평가"""
        results = {}

        # R1: 라이선스 명시
        distribution = self.metadata.get("distribution", {})
        license_url = distribution.get("license", "")
        has_license = bool(license_url)
        results["R1"] = FAIRAssessment(
            principle=FAIRPrinciple.R1,
            compliant=has_license,
            score=1.0 if has_license else 0.0,
            evidence=f"라이선스: {license_url}" if has_license else "라이선스 없음",
            suggestions=[] if has_license else ["CC 라이선스 명시 필수"]
        )

        # R2: 출처 상세
        has_creator = "creator" in self.metadata
        results["R2"] = FAIRAssessment(
            principle=FAIRPrinciple.R2,
            compliant=has_creator,
            score=1.0 if has_creator else 0.0,
            evidence="생성자 정보 존재" if has_creator else "생성자 정보 없음",
            suggestions=[] if has_creator else ["생성자/출처 정보 추가"]
        )

        return results

    def _calculate_overall_score(self) -> float:
        """전체 FAIR 점수 계산"""
        evaluation = {
            **self._evaluate_findable(),
            **self._evaluate_accessible(),
            **self._evaluate_interoperable(),
            **self._evaluate_reusable()
        }
        total_score = sum(a.score for a in evaluation.values())
        return total_score / len(evaluation)


# 사용 예시
if __name__ == "__main__":
    sample_metadata = {
        "@context": "https://schema.org/",
        "@type": "Dataset",
        "@id": "https://doi.org/10.1234/example",
        "name": "테스트 데이터셋",
        "description": "FAIR 평가용 테스트 데이터",
        "creator": {"@type": "Organization", "name": "테스트 기관"},
        "datePublished": "2024-01-01",
        "distribution": {
            "contentUrl": "https://example.com/data.csv",
            "license": "https://creativecommons.org/licenses/by/4.0/"
        },
        "keywords": ["테스트", "데이터"],
        "isAccessibleForFree": True
    }

    evaluator = FAIREvaluator(sample_metadata)
    result = evaluator.evaluate_all()

    print(f"FAIR 종합 점수: {result['overall_score']:.2f}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### FAIR vs Open Data vs Linked Data 비교

| 구분 | FAIR | Open Data | Linked Data |
|------|------|-----------|-------------|
| **핵심 가치** | 재사용성 | 무료 공개 | 연결성 |
| **접근성** | 제어 가능 | 필수 무료 | 선택적 |
| **기계 가독성** | 권장 | 선택적 | 필수 |
| **라이선스** | 명시 필수 | 필수 | 선택적 |
| **표준** | DOI, 메타데이터 | 공공데이터 | RDF, URI |

### FAIR 준수 레벨

| 레벨 | 점수 | 설명 | 권장 조치 |
|------|------|------|-----------|
| **0** | 0~0.25 | FAIR 미준수 | 기본 메타데이터 작성 |
| **1** | 0.25~0.5 | 부분 준수 | 식별자, 라이선스 추가 |
| **2** | 0.5~0.75 | 상당히 준수 | 구조화 포맷 적용 |
| **3** | 0.75~1.0 | 완전 준수 | 지속적 개선 |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 연구 데이터셋 FAIR화

```
┌─────────────────────────────────────────────────────────────────────────┐
│  시나리오: 대학 연구소 논문 데이터 FAIR화                                │
├─────────────────────────────────────────────────────────────────────────┤
│  현황:                                                                 │
│  - 연구 데이터가 연구자 PC에만 저장                                    │
│  - 논문 발표 후 데이터 접근 불가                                       │
│  - 연구 재현성 문제                                                    │
│                                                                         │
│  FAIR화 프로세스:                                                       │
│  1. Findable                                                            │
│     - DOI 발급 (DataCite)                                              │
│     - 메타데이터 작성 (Dublin Core)                                    │
│     - 데이터 저장소 등록 (Zenodo, Figshare)                            │
│                                                                         │
│  2. Accessible                                                          │
│     - HTTP 다운로드 제공                                                │
│     - API 접근 (선택적)                                                │
│     - 메타데이터 영구 보존                                             │
│                                                                         │
│  3. Interoperable                                                       │
│     - CSV/JSON 표준 포맷                                               │
│     - 표준 어휘 사용 (온톨로지)                                        │
│     - 관련 데이터셋 링크                                               │
│                                                                         │
│  4. Reusable                                                            │
│     - CC-BY 4.0 라이선스                                               │
│     - 출처/인용 정보                                                   │
│     - 사용 가이드 문서                                                 │
│                                                                         │
│  기대 효과:                                                             │
│  - 논문 인용 증가 (데이터 인용 포함)                                   │
│  - 연구 협력 확대                                                      │
│  - 재현성 확보                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대효과

| 지표 | FAIR 적용 전 | FAIR 적용 후 |
|------|--------------|--------------|
| 데이터 검색 시간 | 4시간 | 30분 |
| 데이터 통합 비용 | 100% | 40% |
| 연구 재현율 | 30% | 80% |
| 데이터 인용 | 0회 | 평균 5회 |

### 참고 표준

- **FORCE11 FAIR Principles** (2016)
- **GO FAIR Initiative**: https://www.go-fair.org
- **Research Data Alliance (RDA)**: FAIR 데이터 공유

---

## 📌 관련 개념 맵

- [공공 빅데이터](./public_bigdata.md) - FAIR 적용 분야
- [데이터 거버넌스](../09_governance/data_governance.md) - 데이터 관리 체계
- [메타데이터 관리](../09_governance/metadata_management.md) - FAIR 메타데이터
- [데이터 카탈로그](../09_governance/data_catalog.md) - 검색 가능성 확보

---

## 👶 어린이를 위한 3줄 비유

**1단계 (무엇인가요?)**: FAIR는 데이터가 "찾기 쉽고, 가져오기 쉽고, 같이 쓰기 쉽고, 다시 쓰기 쉬워야 한다"는 규칙이에요. 도서관 책처럼 정리되어 있어야 한다는 뜻이에요.

**2단계 (어떤 게 중요한가요?)**: F는 찾기 쉽게, A는 누구나 볼 수 있게, I는 다른 데이터랑 섞기 쉽게, R은 다시 쓸 수 있게 만드는 거예요. 이렇게 하면 데이터가 쓰레기가 안 돼요!

**3단계 (왜 필요한가요?)**: FAIR하지 않으면 좋은 데이터도 아무도 못 써요. 서랍 깊숙이 숨겨진 보물 같아요. FAIR하게 만들면 많은 사람이 데이터를 쓰고, 더 좋은 연구를 할 수 있어요!
