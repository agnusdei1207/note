+++
weight = 138
title = "로그 (Logs)"
date = "2026-03-04"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
- 로그는 애플리케이션이나 시스템에서 발생하는 이벤트를 시간 순서대로 기록한 상세한 텍스트 데이터로, 옵저버빌리티의 가장 기초적이고 구체적인 기둥이다.
- 메트릭이 "어디가 아픈가"를 알려준다면, 로그는 "왜 아픈가"에 대한 근본 원인(Root Cause)을 파악하기 위한 디버깅의 핵심 근거를 제공한다.
- 현대의 분산 시스템에서는 파편화된 로그를 통합 수집하여 검색 가능하게 만드는 **중앙 집중식 로깅(Centralized Logging)** 체계 구축이 필수적이다.

### Ⅰ. 개요 (Context & Background)
초기 운영은 서버에 직접 접속하여 `tail -f` 명령어로 로그 파일을 확인하는 방식이었으나, MSA 환경에서 수백 개의 컨테이너가 생성되고 사라지면서 이 방식은 불가능해졌다. 로그는 파일이 아닌 **이벤트 스트림(Event Stream)**으로 취급되어야 하며, 인프라의 휘발성에 대비해 외부 저장소로 즉시 전송되어야 한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
효율적인 로그 관리를 위해 **수집(Ship) -> 버퍼(Buffer) -> 저장(Store) -> 시각화(Visualize)** 파이프라인이 구성된다.

```text
[ Centralized Logging Pipeline / 중앙 집중식 로깅 파이프라인 ]

  [ Application ] -> (Stdout) -> [ Logging Agent ] -> [ Message Queue ]
                                 (Fluentd/Logstash)    (Kafka/Redis)
                                        |                    |
                                        v                    v
  [ Visualization ] <--- (Query) --- [ Storage ] <--- [ Indexer/Processor ]
      (Kibana)                    (Elasticsearch)

1. Generation: Apps emit logs to stdout/stderr (12-Factor style).
2. Collection: Agents scrape and transform unstructured logs into JSON.
3. Buffering: Message queues prevent data loss during traffic spikes.
4. Indexing: Search engines index text for fast full-text search.
```

- **구조화된 로깅 (Structured Logging):** 단순 텍스트가 아닌 JSON 포맷으로 로그를 생성하여, 추후 필터링과 분석(예: `level="ERROR"`, `user_id="123"`)이 용이하도록 한다.
- **로그 레벨 (Log Levels):** DEBUG, INFO, WARN, ERROR, FATAL 단계를 구분하여 필터링 효율을 높인다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 분석 항목 | 메트릭 (Metrics) | 로그 (Logs) | 분산 추적 (Traces) |
| :--- | :--- | :--- | :--- |
| **특징** | 압축된 수치 데이터 | 상세 이벤트 기록 | 요청의 전체 경로 흐름 |
| **용량** | 작음 (저렴) | 매우 큼 (비쌈) | 중간 |
| **주 용도** | 모니터링, 알람 | 디버깅, 근본 원인 분석 | 병목 지점 파악 |
| **데이터 형태** | 시계열 (TSDB) | 비정형/반정형 (Search Engine) | 스팬(Span) 기반 트리 구조 |
| **상호 보완** | 메트릭으로 이상 감지 -> 추적으로 구간 확인 -> 로그로 최종 원인 파악 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **샘플링 및 보관 정책:** 모든 로그를 무기한 저장하는 것은 비용 측면에서 불가능하다. 운영 로그는 7~14일, 감사/보안 로그는 법적 근거에 따라 장기 보관하는 티어링(Tiering) 전략이 필요하다.
- **민감 정보 마스킹:** 로그에 개인정보(Pii), 비밀번호 등이 찍히지 않도록 수집 단계에서 반드시 마스킹 처리를 수행해야 한다. 이는 기술사로서 보안 컴플라이언스 준수를 위한 필수 판단 사항이다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
로그는 단순한 텍스트 뭉치에서 데이터 분석의 원천으로 진화하고 있다. 최근에는 AI를 이용해 수백만 건의 로그 중 이상 패턴을 자동으로 탐지하는 로그 아노말리 탐지(Log Anomaly Detection)가 주목받고 있다. 잘 관리된 로그는 시스템의 과거를 기록하는 일기이자, 미래의 문제를 예방하는 지식 베이스가 된다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 옵저버빌리티 (Observability)
- **주요 도구:** ELK Stack (Elasticsearch, Logstash, Kibana), Grafana Loki, Fluentd
- **핵심 기술:** 구조화된 로깅, 로그 파이프라인, 마스킹

### 👶 어린이를 위한 3줄 비유 설명
- 컴퓨터가 일을 하면서 쓰는 **일기장**과 같아요. 몇 시에 무슨 일을 했고, 어디가 아팠는지 자세히 적어두는 거예요.
- 나중에 컴퓨터가 고장 나면 의사 선생님(엔지니어)이 이 일기장을 읽고 원인을 찾아내요.
- 일기장이 너무 많아지면 찾기 힘드니까, 커다란 도서관(중앙 저장소)에 모아서 정리해두는 거랍니다!
