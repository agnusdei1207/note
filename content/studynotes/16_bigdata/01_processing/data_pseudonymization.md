+++
title = "개인정보 비식별화 (k-익명성/l-다양성/t-근접성)"
categories = ["studynotes-16_bigdata"]
+++

# 개인정보 비식별화 (k-익명성/l-다양성/t-근접성)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 개인정보 비식별화는 데이터에서 개인을 식별할 수 있는 정보를 제거하거나 변환하여, 분석 가치는 유지하면서 개인 프라이버시를 보호하는 기술이다.
> 2. **가치**: k-익명성, l-다양성, t-근접성은 비식별화의 강도를 수학적으로 보장하는 모델로, 데이터 활용과 프라이버시 보호의 균형을 제공한다.
> 3. **융합**: 데이터 3법의 가명정보, AI 학습 데이터, 의료 데이터 공유와 결합하여 안전한 데이터 활용의 핵심 기술로 활용된다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

개인정보 비식별화(De-identification)는 개인을 식별할 수 있는 정보를 제거하거나 변환하여, 데이터 내의 개인을 알아볼 수 없게 만드는 과정이다. 주요 기법으로는 마스킹, 일반화, 교란, 가명처리 등이 있으며, k-익명성, l-다양성, t-근접성은 비식별화의 수학적 보장 모델이다.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    비식별화 기법 분류                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  원본 데이터                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  이름   │ 나이 │ 성별 │ 우편번호 │ 질병코드 │ 소득             │   │
│  │  홍길동 │ 35  │ 남   │ 04538   │ A01     │ 5000만원         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                        │
│                              ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    비식별화 기법                                 │   │
│  │                                                                  │   │
│  │  1. 마스킹 (Masking)                                             │   │
│  │     홍**    35   남   04538   A01     5000만원                  │   │
│  │                                                                  │   │
│  │  2. 일반화 (Generalization)                                      │   │
│  │     [삭제]  30-40 남   045**   A0*    4000-6000만원             │   │
│  │                                                                  │   │
│  │  3. 교란 (Perturbation)                                          │   │
│  │     [삭제]  37   남   04512   A01     5200만원 (노이즈 추가)    │   │
│  │                                                                  │   │
│  │  4. 가명처리 (Pseudonymization)                                  │   │
│  │     USER001 35   남   04538   A01     5000만원                  │   │
│  │                                                                  │   │
│  │  5. 데이터 교환 (Data Swapping)                                  │   │
│  │     [삭제]  35   여   04538   B02     5000만원 (값 교환)        │   │
│  │                                                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                        │
│                              ▼                                        │
│  비식별화 데이터                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  ID     │ 연령대│ 성별 │ 지역    │ 질병군 │ 소득구간          │   │
│  │  U001   │ 30-40│ 남   │ 강남구  │ A그룹  │ 4-6천만원         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 💡 비유

비식별화는 "모자이크 처리"에 비유할 수 있다. 뉴스에서 용의자 얼굴을 모자이크 처리하면 누구인지 알 수 없지만, 여전히 사람이라는 정보는 유지된다. k-익명성은 "최소 k명이 같은 모자이크 패턴을 가져야 한다"는 규칙과 같다.

### 등장 배경

1. **1998년**: Latanya Sweeney, k-익명성 제안
2. **2002년**: Massachusetts 주지사 의료기록 재식별 사건 (우편번호+생일+성별로 87% 식별)
3. **2007년**: Machanavajjhala et al., l-다양성 제안
4. **2007년**: Ninghui Li et al., t-근접성 제안
5. **2020년**: 한국 데이터 3법으로 가명정보 활용 법적 근거 마련

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### k-익명성 (k-Anonymity)

k-익명성은 각 레코드가 최소 k-1개의 다른 레코드와 동일한 준식별자(Quasi-Identifier) 조합을 가져야 한다는 원칙이다.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    k-익명성 예시 (k=3)                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  [원본 데이터]                                                          │
│  ┌──────────┬───────┬────────┬─────────┬─────────┐                    │
│  │ 이름     │ 나이  │ 성별   │ 우편번호 │ 질병    │                    │
│  ├──────────┼───────┼────────┼─────────┼─────────┤                    │
│  │ 홍길동   │ 25    │ 남     │ 04538   │ 감기    │                    │
│  │ 김철수   │ 27    │ 남     │ 04537   │ 독감    │                    │
│  │ 이영희   │ 35    │ 여     │ 04538   │ 천식    │                    │
│  │ 박민수   │ 38    │ 남     │ 04539   │ 감기    │                    │
│  │ 최수진   │ 32    │ 여     │ 04537   │ 독감    │                    │
│  └──────────┴───────┴────────┴─────────┴─────────┘                    │
│                                                                         │
│  [3-익명화 적용]                                                        │
│  ┌──────────┬───────┬────────┬─────────┬─────────┐                    │
│  │ [삭제]   │ 나이  │ 성별   │ 우편번호 │ 질병    │                    │
│  ├──────────┼───────┼────────┼─────────┼─────────┤                    │
│  │ *        │ 20-30 │ 남     │ 045**   │ *       │ ← 그룹 A (3명)     │
│  │ *        │ 20-30 │ 남     │ 045**   │ *       │                    │
│  │ *        │ 30-40 │ 여     │ 045**   │ *       │ ← 그룹 B (2명) ✗   │
│  │ *        │ 30-40 │ 남     │ 045**   │ *       │ ← 그룹 C (1명) ✗   │
│  │ *        │ 30-40 │ 여     │ 045**   │ *       │                    │
│  └──────────┴───────┴────────┴─────────┴─────────┘                    │
│                                                                         │
│  문제: 그룹 B, C는 각각 2명, 1명으로 3-익명성 미달                      │
│                                                                         │
│  [추가 일반화로 3-익명성 달성]                                          │
│  ┌──────────┬───────┬────────┬─────────┬─────────┐                    │
│  │ [삭제]   │ 나이  │ 성별   │ 우편번호 │ 질병    │                    │
│  ├──────────┼───────┼────────┼─────────┼─────────┤                    │
│  │ *        │ 20-40 │ 남     │ 045**   │ *       │ ← 그룹 A (3명) ✓   │
│  │ *        │ 20-40 │ 남     │ 045**   │ *       │                    │
│  │ *        │ 20-40 │ *      │ 045**   │ *       │ ← 그룹 B (3명) ✓   │
│  │ *        │ 20-40 │ 남     │ 045**   │ *       │                    │
│  │ *        │ 20-40 │ *      │ 045**   │ *       │                    │
│  └──────────┴───────┴────────┴─────────┴─────────┘                    │
│                                                                         │
│  모든 그룹이 최소 3명 → 3-익명성 달성                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### l-다양성 (l-Diversity)

k-익명성의 약점(동질성 공격)을 보완하여, 각 동등 클래스 내의 민감 속성이 최소 l개의 서로 다른 값을 가져야 한다는 원칙이다.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    l-다양성 예시 (l=3)                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  [k-익명성만 적용 - 동질성 공격 취약]                                   │
│  ┌──────────┬───────┬────────┬─────────┬─────────┐                    │
│  │ 나이     │ 성별  │ 지역   │ 질병    │         │                    │
│  ├──────────┼───────┼────────┼─────────┼─────────┤                    │
│  │ 20-30    │ 남    │ 강남   │ 감기    │ ← 모두 감기!              │
│  │ 20-30    │ 남    │ 강남   │ 감기    │   공격자가 25세 남성임을   │
│  │ 20-30    │ 남    │ 강남   │ 감기    │   알면 감기 환자임을 확정  │
│  └──────────┴───────┴────────┴─────────┴─────────┘                    │
│                                                                         │
│  → 3-익명성이지만 동질성 공격에 취약                                    │
│                                                                         │
│  [3-다양성 적용]                                                        │
│  ┌──────────┬───────┬────────┬─────────┬─────────┐                    │
│  │ 나이     │ 성별  │ 지역   │ 질병    │         │                    │
│  ├──────────┼───────┼────────┼─────────┼─────────┤                    │
│  │ 20-30    │ 남    │ 강남   │ 감기    │ ← 3가지 다른 질병         │
│  │ 20-30    │ 남    │ 강남   │ 독감    │   (감기, 독감, 천식)       │
│  │ 20-30    │ 남    │ 강남   │ 천식    │   어떤 질병인지 확정 불가  │
│  └──────────┴───────┴────────┴─────────┴─────────┘                    │
│                                                                         │
│  → 3-익명성 + 3-다양성 달성                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### t-근접성 (t-Closeness)

l-다양성의 약점(배경 지식 공격)을 보완하여, 각 동등 클래스 내의 민감 속성 분포가 전체 데이터셋의 분포와 t 이내로 유사해야 한다는 원칙이다.

```python
from dataclasses import dataclass
from typing import List, Dict, Tuple
import numpy as np
from collections import Counter

@dataclass
class AnonymizationResult:
    """비식별화 결과"""
    data: List[Dict]
    k_anonymity: int
    l_diversity: int
    t_closeness: float
    information_loss: float

class KAnonymityProcessor:
    """k-익명성 처리기"""

    def __init__(self, quasi_identifiers: List[str], sensitive_attr: str):
        self.quasi_identifiers = quasi_identifiers
        self.sensitive_attr = sensitive_attr

    def apply_k_anonymity(
        self,
        data: List[Dict],
        k: int,
        generalization_rules: Dict
    ) -> AnonymizationResult:
        """k-익명성 적용"""

        # 1단계: 일반화 적용
        generalized_data = self._generalize(data, generalization_rules)

        # 2단계: 동등 클래스 형성
        equivalence_classes = self._form_equivalence_classes(generalized_data)

        # 3단계: k-익명성 검증
        k_value = self._verify_k_anonymity(equivalence_classes)

        # 4단계: l-다양성 계산
        l_value = self._calculate_l_diversity(equivalence_classes)

        # 5단계: t-근접성 계산
        t_value = self._calculate_t_closeness(equivalence_classes, data)

        # 6단계: 정보 손실 계산
        info_loss = self._calculate_information_loss(data, generalized_data)

        return AnonymizationResult(
            data=generalized_data,
            k_anonymity=k_value,
            l_diversity=l_value,
            t_closeness=t_value,
            information_loss=info_loss
        )

    def _generalize(self, data: List[Dict], rules: Dict) -> List[Dict]:
        """일반화 적용"""
        result = []
        for record in data:
            new_record = {}
            for key, value in record.items():
                if key in rules:
                    new_record[key] = self._apply_rule(value, rules[key])
                else:
                    new_record[key] = value
            result.append(new_record)
        return result

    def _apply_rule(self, value, rule):
        """일반화 규칙 적용"""
        if rule["type"] == "range":
            for range_spec, replacement in rule["mappings"].items():
                min_val, max_val = map(int, range_spec.split("-"))
                if min_val <= value <= max_val:
                    return replacement
        elif rule["type"] == "prefix":
            return value[:rule["keep_chars"]] + "*"
        elif rule["type"] == "suppress":
            return "*"
        return value

    def _form_equivalence_classes(self, data: List[Dict]) -> Dict:
        """동등 클래스 형성"""
        classes = {}
        for record in data:
            key = tuple(record[q] for q in self.quasi_identifiers)
            if key not in classes:
                classes[key] = []
            classes[key].append(record)
        return classes

    def _verify_k_anonymity(self, classes: Dict) -> int:
        """k-익명성 검증"""
        if not classes:
            return 0
        return min(len(records) for records in classes.values())

    def _calculate_l_diversity(self, classes: Dict) -> int:
        """l-다양성 계산 (최소 다양성)"""
        diversities = []
        for records in classes.values():
            sensitive_values = [r[self.sensitive_attr] for r in records]
            diversities.append(len(set(sensitive_values)))
        return min(diversities) if diversities else 0

    def _calculate_t_closeness(self, classes: Dict, original_data: List[Dict]) -> float:
        """t-근접성 계산 (EMD 기반)"""
        # 전체 분포
        global_dist = Counter(r[self.sensitive_attr] for r in original_data)
        total = sum(global_dist.values())
        global_prob = {k: v/total for k, v in global_dist.items()}

        max_emd = 0
        for records in classes.values():
            # 클래스 내 분포
            class_dist = Counter(r[self.sensitive_attr] for r in records)
            class_total = sum(class_dist.values())
            class_prob = {k: v/class_total for k, v in class_dist.items()}

            # EMD (Earth Mover's Distance) 계산 (간소화)
            emd = sum(abs(global_prob.get(k, 0) - class_prob.get(k, 0))
                     for k in set(global_prob.keys()) | set(class_prob.keys()))
            emd /= 2  # 정규화

            max_emd = max(max_emd, emd)

        return max_emd

    def _calculate_information_loss(self, original: List[Dict], anonymized: List[Dict]) -> float:
        """정보 손실 계산"""
        # 간소화된 계산: 일반화된 필드 비율
        total_fields = len(original) * len(self.quasi_identifiers)
        generalized_fields = 0

        for orig, anon in zip(original, anonymized):
            for qi in self.quasi_identifiers:
                if orig[qi] != anon[qi]:
                    generalized_fields += 1

        return generalized_fields / total_fields if total_fields > 0 else 0


# 사용 예시
if __name__ == "__main__":
    # 테스트 데이터
    data = [
        {"name": "홍길동", "age": 25, "gender": "M", "zipcode": "04538", "disease": "감기"},
        {"name": "김철수", "age": 27, "gender": "M", "zipcode": "04537", "disease": "독감"},
        {"name": "이영희", "age": 35, "gender": "F", "zipcode": "04538", "disease": "천식"},
        {"name": "박민수", "age": 38, "gender": "M", "zipcode": "04539", "disease": "감기"},
        {"name": "최수진", "age": 32, "gender": "F", "zipcode": "04537", "disease": "독감"},
    ]

    # 일반화 규칙
    generalization_rules = {
        "name": {"type": "suppress"},
        "age": {"type": "range", "mappings": {"20-30": "20-30", "30-40": "30-40"}},
        "zipcode": {"type": "prefix", "keep_chars": 3}
    }

    processor = KAnonymityProcessor(
        quasi_identifiers=["age", "gender", "zipcode"],
        sensitive_attr="disease"
    )

    result = processor.apply_k_anonymity(data, k=2, generalization_rules=generalization_rules)

    print(f"k-익명성: {result.k_anonymity}")
    print(f"l-다양성: {result.l_diversity}")
    print(f"t-근접성: {result.t_closeness:.3f}")
    print(f"정보 손실: {result.information_loss:.2%}")
