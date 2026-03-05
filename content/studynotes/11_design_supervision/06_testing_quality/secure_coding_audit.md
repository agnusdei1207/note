+++
title = "시큐어 코딩 진단 (Secure Coding Audit)"
categories = ["studynotes-11_design_supervision"]
+++

# 시큐어 코딩 진단 (Secure Coding Audit)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시큐어 코딩 진단은 KISA 47개 보안 약점 기준에 따라 소스코드의 **보안 취약점을 정적 분석(SAST)**하여, 해킹, 데이터 유출, 서비스 장애 등을 예방하는 감리 핵심 활동입니다.
> 2. **가치**: 개발 단계에서 보안 약점을 조기 발견하여 수정 비용을 최소화하고, 개인정보보호법, 정보통신망법 등 법적 요건을 준수합니다.
> 3. **융합**: DevSecOps의 핵심 구성요소로 CI/CD 파이프라인에 통합되며, OWASP Top 10, CWE/SANS Top 25 등 국제 기준과 연계됩니다.

---

## Ⅰ. 개요

### 1. 정의
시큐어 코딩 진단은 **소스코드 수준에서 보안 취약점을 탐지**하는 활동입니다. KISA(한국인터넷진흥원)에서 정의한 47개 보안 약점을 기준으로 정적 분석 도구(SAST)와 수동 검토를 통해 취약점을 식별합니다.

### 2. KISA 47개 보안 약점 카테고리

| 카테고리 | 주요 항목 | 개수 |
|:---:|:---|:---:|
| **입력 데이터 검증** | SQL Injection, XSS, 파일 업로드 | 18 |
| **보안 기능** | 인증, 인가, 암호화, 세션 | 14 |
| **시간 및 상태** | 경쟁 조건, Deadlock | 2 |
| **에러 처리** | 예외 처리, 정보 노출 | 3 |
| **코드 품질** | 메모리 누수, null 포인터 | 7 |
| **캡슐화** | 정보 은닉, 접근 제어 | 3 |

---

## Ⅱ. 핵심 원리

### 1. 주요 취약점 상세

#### SQL Injection
```kotlin
// Bad: 취약한 코드
val query = "SELECT * FROM users WHERE id = '" + userId + "'"

// Good: Prepared Statement
val query = "SELECT * FROM users WHERE id = ?"
pstmt.setString(1, userId)
```

#### XSS (Cross-Site Scripting)
```kotlin
// Bad: 사용자 입력 그대로 출력
println("<div>${userInput}</div>")

// Good: HTML 이스케이프
println("<div>${escapeHtml(userInput)}</div>")
```

#### 경로 조작
```kotlin
// Bad: 사용자 입력을 경로로 사용
val file = File("/uploads/" + userInput)

// Good: 경로 검증
val sanitized = userInput.replace("../", "")
val file = File("/uploads/${sanitized}")
```

### 2. 정적 분석 도구

| 도구 | 언어 | 특징 |
|:---:|:---|:---|
| **SonarQube** | 다양 | 오픈소스, 품질 지표 |
| **Checkmarx** | 다양 | 기업용, 정밀 분석 |
| **Fortify** | 다양 | 마이크로포커스 |
| **FindSecBugs** | Java | 오픈소스, 보안 특화 |

---

## Ⅲ. 비교 분석

### 1. SAST vs DAST

| 구분 | SAST (정적) | DAST (동적) |
|:---:|:---|:---|
| **시점** | 개발 중 | 운영/테스트 |
| **대상** | 소스코드 | 실행 중인 앱 |
| **장점** | 조기 발견 | 실제 공격 시뮬레이션 |
| **단점** | 오탐 가능 | 늦은 발견 |

---

## Ⅳ. 실무 적용

### 감리 체크리스트
- [ ] SQL Injection 방지 (PreparedStatement 사용)
- [ ] XSS 방지 (출력 이스케이프)
- [ ] 파일 업로드 검증 (확장자, 크기)
- [ ] 암호화 적용 (비밀번호, 민감 정보)
- [ ] 세션 관리 (타임아웃, 재생성)
- [ ] 에러 메시지 정보 노출 방지
- [ ] 로그에 민감 정보 미포함

---

## Ⅴ. 기대효과

| 효과 | 설명 |
|:---:|:---|
| **보안 사고 예방** | 취약점 사전 차단 |
| **법적 컴플라이언스** | 개인정보보호법 준수 |
| **비용 절감** | 조기 수정으로 비용 절감 |

---

## 📌 관련 개념
- [OWASP Top 10](./owasp_top10.md): 웹 보안 취약점
- [SAST/DAST](./sast_dast.md): 정적/동적 분석
- [DevSecOps](./devsecops.md): 보안 내재화

---

## 👶 어린이를 위한 비유
시큐어 코딩 진단은 **집에 도둑이 들어오지 못하게 미리 검사하는 것**과 같아요. 문이 튼튼한지, 창문에 자물쇠가 있는지 확인해요!
