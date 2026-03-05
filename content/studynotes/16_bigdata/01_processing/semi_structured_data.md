+++
title = "반정형 데이터 (JSON/XML)"
categories = ["studynotes-16_bigdata"]
+++

# 반정형 데이터 (JSON/XML)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 반정형 데이터는 고정된 스키마 없이 데이터 내부에 구조 정보를 포함하는 형태로, JSON, XML, YAML 등이 대표적이며 웹 API, 로그, 설정 파일에 광범위하게 활용된다.
> 2. **가치**: Schema-on-Read 방식으로 유연한 데이터 통합이 가능하며, 마이크로서비스 간 데이터 교환, IoT 센서 데이터, 로그 분석의 핵심 포맷이다.
> 3. **융합**: NoSQL 문서형 DB(MongoDB), 검색 엔진(Elasticsearch), 스트리밍 플랫폼(Kafka)과 결합하여 실시간 데이터 파이프라인의 표준 포맷으로 자리 잡았다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

반정형 데이터(Semi-structured Data)는 정형 데이터의 엄격한 스키마 제약과 비정형 데이터의 형식 자유 사이의 중간 지점에 위치한다. 데이터 자체가 구조 정보(메타데이터)를 포함하고 있어, 외부 스키마 정의 없이도 자체적으로 구조를 기술한다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                  데이터 구조화 스펙트럼                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  정형 (Structured)        반정형 (Semi-structured)     비정형       │
│  ◄─────────────────────────────────────────────────────────────►   │
│                                                                     │
│  ┌─────────────┐    ┌─────────────────────────────┐  ┌──────────┐  │
│  │ RDBMS Table │    │ JSON │ XML │ YAML │ CSV    │  │ Image    │  │
│  │             │    │      │     │      │        │  │ Audio    │  │
│  │ 고정 스키마 │    │ 자체 기술형 스키마          │  │ Video    │  │
│  │ Schema-on-  │    │ Schema-on-Read              │  │ Raw Text │  │
│  │ Write       │    │                             │  │          │  │
│  └─────────────┘    └─────────────────────────────┘  └──────────┘  │
│                                                                     │
│  엄격한 구조 ◄───────────────────────────────────────► 자유로운 형태 │
│  높은 일관성                                         높은 유연성     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 💡 비유

반정형 데이터는 "라벨이 붙은 서류 봉투"에 비유할 수 있다. 정형 데이터가 모든 칸이 정해진 신청서라면, 반정형 데이터는 각 문서에 "이름", "주소", "전화번호" 같은 라벨(태그)이 붙어 있어 내용을 바로 파악할 수 있는 서류 봉투다. 봉투마다 들어있는 문서가 다를 수 있지만, 라벨 덕분에 무엇인지 알 수 있다.

### 등장 배경 및 발전 과정

1. **SGML/XML의 등장 (1986~1998)**: SGML이 문서 마크업 표준으로 시작, 이를 간소화한 XML이 1998년 W3C 표준으로 채택되어 기업 간 데이터 교환(EDI)의 핵심 포맷이 되었다.

2. **JSON의 부상 (2001~2006)**: Douglas Crockford가 JSON을 정의하고, AJAX의 대중화와 함께 웹 API의 사실상 표준으로 자리 잡았다. XML 대비 30% 작은 payload와 파싱 속도 2~3배 향상이 강점이다.

3. **NoSQL과의 결합 (2009~)**: MongoDB, CouchDB 등 문서형 DB가 JSON을 네이티브 포맷으로 채택하면서 반정형 데이터의 저장 및 쿼리가 대중화되었다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### JSON vs XML 상세 비교

| 구분 | JSON | XML |
|------|------|-----|
| **전체 이름** | JavaScript Object Notation | Extensible Markup Language |
| **태생** | 2001, Douglas Crockford | 1998, W3C |
| **데이터 모델** | Key-Value, Array, 중첩 객체 | Element, Attribute, Text, 중첩 Element |
| **데이터 타입** | String, Number, Boolean, null, Array, Object | String only (스키마로 타입 정의) |
| **파일 크기** | 작음 (태그 없음) | 큼 (닫는 태그 필요) |
| **파싱 속도** | 빠름 (네이티브 JS 지원) | 느림 (DOM 파싱 필요) |
| **스키마** | JSON Schema (선택적) | XSD, DTD (강력한 지원) |
| **주 용도** | API, 설정, 로그 | 문서, EDI, SOAP |
| **가독성** | 중간 | 높음 (태그로 명확) |
| **표준화** | ECMA-404, RFC 8259 | W3C XML 1.0 |

### JSON 구조 심층 분석

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       JSON 데이터 모델 구조                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  JSON Value Types (6가지 기본 타입)                             │   │
│  │                                                                 │   │
│  │  1. String: "Hello World"                                      │   │
│  │  2. Number: 42, 3.14, -100, 1.5e10                             │   │
│  │  3. Boolean: true, false                                       │   │
│  │  4. null: null                                                 │   │
│  │  5. Array: [1, 2, 3] 또는 [{"a":1}, {"b":2}]                  │   │
│  │  6. Object: {"key": "value", "nested": {"x": 1}}              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  실제 JSON 예시: 이커머스 주문 데이터                           │   │
│  │                                                                 │   │
│  │  {                                                              │   │
│  │    "orderId": "ORD-2024-001",         // String                │   │
│  │    "customerId": 12345,               // Number                │   │
│  │    "orderDate": "2024-03-15T10:30:00Z", // String (ISO 8601)  │   │
│  │    "isPriority": true,                // Boolean               │   │
│  │    "discount": null,                  // null                  │   │
│  │    "items": [                         // Array                 │   │
│  │      {                                                        │   │
│  │        "productId": "P001",                                   │   │
│  │        "productName": "Laptop",                               │   │
│  │        "quantity": 1,                                         │   │
│  │        "unitPrice": 1299.99,                                  │   │
│  │        "options": {                    // Nested Object        │   │
│  │          "color": "Space Gray",                               │   │
│  │          "storage": "512GB"                                   │   │
│  │        }                                                      │   │
│  │      },                                                       │   │
│  │      {                                                        │   │
│  │        "productId": "P002",                                   │   │
│  │        "productName": "Mouse",                                │   │
│  │        "quantity": 2,                                         │   │
│  │        "unitPrice": 79.99                                     │   │
│  │      }                                                        │   │
│  │    ],                                                         │   │
│  │    "shipping": {                       // Object               │   │
│  │      "method": "Express",                                     │   │
│  │      "address": {                                             │   │
│  │        "street": "123 Main St",                               │   │
│  │        "city": "Seoul",                                       │   │
│  │        "zipCode": "04538"                                     │   │
│  │      }                                                        │   │
│  │    }                                                          │   │
│  │  }                                                            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### XML 구조 심층 분석

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       XML 데이터 모델 구조                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  XML 구성 요소 (5가지 핵심 개념)                                 │   │
│  │                                                                 │   │
│  │  1. Element: <name>John</name>                                 │   │
│  │  2. Attribute: <person age="30">                               │   │
│  │  3. Text Content: Element 내부의 텍스트                         │   │
│  │  4. Namespace: xmlns:ns="http://example.com"                   │   │
│  │  5. CDATA: <![CDATA[<script>alert('xss')</script>]]>         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  실제 XML 예시: 이커머스 주문 데이터 (JSON과 동일 내용)         │   │
│  │                                                                 │   │
│  │  <?xml version="1.0" encoding="UTF-8"?>                        │   │
│  │  <order xmlns="http://example.com/order"                       │   │
│  │        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">  │   │
│  │    <orderId>ORD-2024-001</orderId>                             │   │
│  │    <customerId>12345</customerId>                              │   │
│  │    <orderDate>2024-03-15T10:30:00Z</orderDate>                 │   │
│  │    <isPriority>true</isPriority>                               │   │
│  │    <discount xsi:nil="true"/>                                  │   │
│  │    <items>                                                     │   │
│  │      <item>                                                    │   │
│  │        <productId>P001</productId>                             │   │
│  │        <productName>Laptop</productName>                       │   │
│  │        <quantity>1</quantity>                                  │   │
│  │        <unitPrice currency="USD">1299.99</unitPrice>           │   │
│  │        <options>                                               │   │
│  │          <color>Space Gray</color>                             │   │
│  │          <storage>512GB</storage>                              │   │
│  │        </options>                                              │   │
│  │      </item>                                                   │   │
│  │      <item>                                                    │   │
│  │        <productId>P002</productId>                             │   │
│  │        <productName>Mouse</productName>                        │   │
│  │        <quantity>2</quantity>                                  │   │
│  │        <unitPrice currency="USD">79.99</unitPrice>             │   │
│  │      </item>                                                   │   │
│  │    </items>                                                    │   │
│  │    <shipping method="Express">                                 │   │
│  │      <address>                                                 │   │
│  │        <street>123 Main St</street>                            │   │
│  │        <city>Seoul</city>                                      │   │
│  │        <zipCode>04538</zipCode>                                │   │
│  │      </address>                                                │   │
│  │    </shipping>                                                 │   │
│  │  </order>                                                      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: JSON 처리 파이프라인

```python
import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import ijson  # 스트리밍 JSON 파서

@dataclass
class Order:
    """주문 데이터 클래스"""
    orderId: str
    customerId: int
    orderDate: str
    isPriority: bool
    discount: Optional[float]
    items: List[Dict]
    shipping: Dict

class JSONProcessor:
    """JSON 데이터 처리기"""

    def __init__(self):
        self.encoding = 'utf-8'

    # ============== 기본 JSON 처리 ==============

    def parse_string(self, json_str: str) -> Dict:
        """문자열 JSON 파싱"""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 파싱 오류: {e}")

    def parse_file(self, filepath: str) -> Dict:
        """파일 JSON 파싱"""
        with open(filepath, 'r', encoding=self.encoding) as f:
            return json.load(f)

    def to_json(self, data: Any, pretty: bool = False) -> str:
        """객체를 JSON 문자열로 변환"""
        indent = 2 if pretty else None
        return json.dumps(
            data,
            indent=indent,
            ensure_ascii=False,  # 한글 지원
            default=self._json_serializer
        )

    def _json_serializer(self, obj):
        """커스텀 타입 직렬화"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        raise TypeError(f"Type {type(obj)} not serializable")

    # ============== 대용량 JSON 스트리밍 처리 ==============

    def stream_large_json(self, filepath: str, array_key: str):
        """대용량 JSON 스트리밍 처리 (메모리 효율적)"""
        with open(filepath, 'rb') as f:
            # ijson을 사용하여 배열 요소를 하나씩 스트리밍
            parser = ijson.items(f, f'{array_key}.item')

            for item in parser:
                yield self._process_item(item)

    def _process_item(self, item: Dict) -> Dict:
        """개별 아이템 처리"""
        # 비즈니스 로직 적용
        if 'unitPrice' in item:
            item['unitPriceWithTax'] = item['unitPrice'] * 1.1
        return item

    # ============== JSON Schema 검증 ==============

    def validate_schema(self, data: Dict, schema: Dict) -> bool:
        """JSON Schema 검증"""
        try:
            import jsonschema
            jsonschema.validate(instance=data, schema=schema)
            return True
        except jsonschema.ValidationError as e:
            print(f"검증 실패: {e.message}")
            return False

    # ============== JSON Path 쿼리 ==============

    def query_jsonpath(self, data: Dict, path: str) -> List:
        """JSONPath 쿼리 수행"""
        from jsonpath_ng import parse
        jsonpath_expr = parse(path)
        return [match.value for match in jsonpath_expr.find(data)]


# 사용 예시
if __name__ == "__main__":
    processor = JSONProcessor()

    # JSON 생성 예시
    order = Order(
        orderId="ORD-2024-001",
        customerId=12345,
        orderDate="2024-03-15T10:30:00Z",
        isPriority=True,
        discount=None,
        items=[
            {"productId": "P001", "productName": "Laptop", "quantity": 1}
        ],
        shipping={"method": "Express", "city": "Seoul"}
    )

    # 객체 → JSON
    json_str = processor.to_json(asdict(order), pretty=True)
    print("JSON 출력:")
    print(json_str)

    # JSON → 객체
    parsed = processor.parse_string(json_str)
    print(f"\n파싱된 orderId: {parsed['orderId']}")

    # JSONPath 쿼리 예시
    # 결과: ["P001"]
```

### 심층 동작 원리: XML 처리 파이프라인

```python
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, Any, List
import defusedxml.ElementTree as safe_ET  # XXE 공격 방지

class XMLProcessor:
    """XML 데이터 처리기"""

    # ============== XML 파싱 ==============

    def parse_string(self, xml_str: str) -> ET.Element:
        """문자열 XML 파싱"""
        # XXE 공격 방지를 위해 defusedxml 사용
        return safe_ET.fromstring(xml_str)

    def parse_file(self, filepath: str) -> ET.ElementTree:
        """파일 XML 파싱"""
        tree = safe_ET.parse(filepath)
        return tree

    # ============== XML → Dict 변환 ==============

    def to_dict(self, element: ET.Element) -> Dict:
        """XML Element를 Dict로 변환"""
        result = {}

        # 속성 추가
        if element.attrib:
            result['@attributes'] = element.attrib

        # 자식 요소 처리
        children = list(element)
        if children:
            child_dict = {}
            for child in children:
                child_data = self.to_dict(child)
                if child.tag in child_dict:
                    # 동일 태그가 여러 개면 리스트로 변환
                    if not isinstance(child_dict[child.tag], list):
                        child_dict[child.tag] = [child_dict[child.tag]]
                    child_dict[child.tag].append(child_data)
                else:
                    child_dict[child.tag] = child_data
            result.update(child_dict)
        elif element.text and element.text.strip():
            # 텍스트 내용
            text = element.text.strip()
            if result:  # 속성이 있으면 #text 키 사용
                result['#text'] = text
            else:
                return text

        return result if result else None

    # ============== Dict → XML 변환 ==============

    def from_dict(self, data: Dict, root_tag: str = 'root') -> ET.Element:
        """Dict를 XML Element로 변환"""
        root = ET.Element(root_tag)
        self._dict_to_element(data, root)
        return root

    def _dict_to_element(self, data: Dict, parent: ET.Element):
        """재귀적으로 Dict를 XML로 변환"""
        for key, value in data.items():
            if key == '@attributes':
                parent.attrib.update(value)
            elif key == '#text':
                parent.text = str(value)
            elif isinstance(value, list):
                for item in value:
                    child = ET.SubElement(parent, key)
                    if isinstance(item, dict):
                        self._dict_to_element(item, child)
                    else:
                        child.text = str(item)
            elif isinstance(value, dict):
                child = ET.SubElement(parent, key)
                self._dict_to_element(value, child)
            else:
                child = ET.SubElement(parent, key)
                child.text = str(value)

    # ============== XML 포맷팅 ==============

    def prettify(self, element: ET.Element) -> str:
        """XML 보기 좋게 포맷팅"""
        rough_string = ET.tostring(element, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    # ============== XPath 쿼리 ==============

    def xpath_query(self, element: ET.Element, xpath: str) -> List:
        """XPath 쿼리 수행"""
        return element.findall(xpath)

    # ============== XML Schema (XSD) 검증 ==============

    def validate_xsd(self, xml_path: str, xsd_path: str) -> bool:
        """XSD 스키마 검증"""
        from lxml import etree

        xmlschema = etree.XMLSchema(etree.parse(xsd_path))
        xml_doc = etree.parse(xml_path)

        if xmlschema.validate(xml_doc):
            return True
        else:
            print("검증 실패:")
            for error in xmlschema.error_log:
                print(f"  Line {error.line}: {error.message}")
            return False


# 사용 예시
if __name__ == "__main__":
    processor = XMLProcessor()

    xml_str = '''<?xml version="1.0" encoding="UTF-8"?>
    <order>
        <orderId>ORD-2024-001</orderId>
        <customerId>12345</customerId>
        <items>
            <item>
                <productId>P001</productId>
                <quantity>1</quantity>
            </item>
        </items>
    </order>'''

    # XML 파싱 및 Dict 변환
    root = processor.parse_string(xml_str)
    order_dict = processor.to_dict(root)
    print("XML → Dict:")
    print(order_dict)

    # XPath 쿼리
    order_id = processor.xpath_query(root, './/orderId')
    print(f"\nXPath 쿼리 결과: {order_id[0].text if order_id else 'Not found'}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### JSON vs XML vs YAML 비교

| 구분 | JSON | XML | YAML |
|------|------|-----|------|
| **가독성** | 중간 | 중간 | 높음 |
| **파일 크기** | 작음 | 큼 | 중간 |
| **파싱 속도** | 빠름 | 느림 | 중간 |
| **주석 지원** | 없음 | 있음 | 있음 |
| **데이터 타입** | 6개 | 1개(String) | 다양함 |
| **스키마** | JSON Schema | XSD/DT | 없음 |
| **주 용도** | API, 로그 | 문서, EDI | 설정 파일 |
| **인기도 (2024)** | ★★★★★ | ★★★☆☆ | ★★★★☆ |

### 반정형 데이터 처리 기술 스택

| 처리 단계 | JSON | XML |
|-----------|------|-----|
| **파싱** | orjson, ujson, simdjson | lxml, xml.etree |
| **쿼리** | JSONPath, jq | XPath, XQuery |
| **검증** | JSON Schema, AJV | XSD, DTD, Schematron |
| **변환** | json-logic, JOLT | XSLT |
| **저장** | MongoDB, Elasticsearch | MarkLogic, eXist-db |
| **분석** | Spark SQL (JSON) | Spark SQL (XML) |

### 과목 융합: 데이터베이스 관점

반정형 데이터는 RDBMS와 NoSQL에서 다르게 처리된다:

1. **RDBMS (PostgreSQL/MySQL)**: JSONB, JSON 컬럼 타입으로 저장, JSON 함수로 쿼리
2. **NoSQL (MongoDB)**: BSON (Binary JSON)으로 네이티브 저장, 인덱싱 지원
3. **검색엔진 (Elasticsearch)**: JSON 문서 역색인, 전문 검색 최적화

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 마이크로서비스 API 응답 설계

```
┌─────────────────────────────────────────────────────────────────────────┐
│  시나리오: 이커머스 주문 조회 API 응답 포맷 설계                         │
├─────────────────────────────────────────────────────────────────────────┤
│  요구사항:                                                              │
│  - 모바일 앱과 웹에서 공통 사용                                         │
│  - 다국어 지원 (한국어, 영어, 일본어)                                   │
│  - 버전 관리 (v1, v2 호환성)                                           │
│  - 확장성 (새 필드 추가 가능)                                          │
│                                                                         │
│  설계 결정:                                                             │
│  1. 포맷: JSON (XML 대비 40% 작은 payload)                             │
│  2. 구조: HAL (Hypertext Application Language) 적용                    │
│  3. 버전: URL Path (/api/v1/orders vs /api/v2/orders)                  │
│  4. 에러: RFC 7807 Problem Details 포맷                                │
│                                                                         │
│  JSON 응답 예시:                                                        │
│  {                                                                      │
│    "_links": {                                                          │
│      "self": {"href": "/api/v2/orders/ORD-001"},                       │
│      "customer": {"href": "/api/v2/customers/12345"}                   │
│    },                                                                   │
│    "orderId": "ORD-001",                                               │
│    "status": "SHIPPED",                                                │
│    "items": [...],                                                     │
│    "metadata": {                                                        │
│      "apiVersion": "2.0",                                              │
│      "timestamp": "2024-03-15T10:30:00Z"                               │
│    }                                                                    │
│  }                                                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

### 도입 체크리스트

**기술적 고려사항**
- [ ] JSON vs XML 선택 근거 문서화
- [ ] JSON Schema / XSD 정의
- [ ] API 버전 관리 전략
- [ ] 대용량 파일 스트리밍 처리 (ijson, SAX)
- [ ] 보안: XXE 방지, JSON Injection 방지

**운영적 고려사항**
- [ ] 압축 (gzip, brotli) 적용
- [ ] 캐싱 전략 (ETag, Last-Modified)
- [ ] 모니터링 (파싱 시간, payload 크기)

### 안티패턴 (Anti-patterns)

1. **Deeply Nested JSON**: 5단계 이상 중첩은 가독성 저하 및 파싱 비용 증가
2. **Mixed Content in XML**: Element와 Text가 섞이면 처리 복잡도 급증
3. **Giant JSON Files**: 100MB+ JSON은 스트리밍 파서 사용 권장
4. **Schema Drift**: 스키마 변경을 추적하지 않아 호환성 깨짐

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 정형 (RDBMS) | 반정형 (JSON) | 개선 효과 |
|------|--------------|---------------|-----------|
| 스키마 변경 비용 | 높음 (마이그레이션) | 낮음 (유연) | -90% |
| API 개발 속도 | 느림 | 빠름 | +200% |
| 데이터 통합 난이도 | 높음 | 낮음 | -70% |
| 쿼리 성능 | 빠름 | 중간 | -30% |

### 미래 전망

1. **JSON Schema 강화**: OpenAPI 3.1의 JSON Schema 완전 호환
2. **JSONata**: JSON용 쿼리 언어로 복잡한 변환 지원
3. **Protocol Buffers vs JSON**: gRPC에서는 Protobuf, REST에서는 JSON
4. **JSONC (JSON with Comments)**: 설정 파일에서 주석 허용

### 참고 표준/가이드

- **RFC 8259**: The JSON Data Interchange Format
- **W3C XML 1.0**: Extensible Markup Language
- **JSON Schema Draft 2020-12**: JSON Schema Validation
- **OpenAPI 3.1**: API Specification with JSON Schema

---

## 📌 관련 개념 맵

- [비정형 데이터](./unstructured_data_types.md) - 고정 스키마가 없는 데이터
- [MongoDB](../05_nosql/mongodb.md) - JSON 기반 문서형 NoSQL
- [Elasticsearch](../05_nosql/elasticsearch.md) - JSON 기반 검색 엔진
- [REST API](../08_platform/rest_api_design.md) - JSON 기반 웹 API
- [Kafka 메시지 포맷](../03_streaming/apache_kafka.md) - JSON/Avro 직렬화
- [ETL vs ELT](../06_data_lake/elt_vs_etl.md) - 반정형 데이터 처리 방식

---

## 👶 어린이를 위한 3줄 비유

**1단계 (무엇인가요?)**: 반정형 데이터는 이름표가 붙은 물건들이에요. "이름: 철수", "나이: 10살", "좋아하는 것: 사과"처럼 각 정보에 이름표가 붙어 있어서 무엇인지 바로 알 수 있어요.

**2단계 (어떻게 쓰나요?)**: 컴퓨터는 이름표를 보고 정보를 찾아요. "철수의 나이가 뭐야?"라고 물으면 "나이"라는 이름표를 찾아서 "10살"이라고 대답해요. JSON은 {이름: "철수"}처럼 중괄호로, XML은 <이름>철수</이름>처럼 꺾쇠로 이름표를 만들어요.

**3단계 (왜 중요한가요?)**: 반정형 데이터는 유연해서 새로운 정보를 쉽게 추가할 수 있어요. "취미: 축구"를 나중에 추가해도 문제없어요. 그래서 스마트폰 앱이나 웹사이트에서 데이터를 주고받을 때 가장 많이 쓰여요!
