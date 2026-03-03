+++
title = "5. 데이터베이스"
description = "관계형 DB, NoSQL, 트랜잭션, 정규화, 분산 DB, 데이터 웨어하우스, NewSQL"
sort_by = "title"
weight = 5
+++

# 제5과목: 데이터베이스

데이터베이스 설계, 관리, 최적화의 핵심 개념을 다룹니다.

## 핵심 키워드

### DBMS 기초
- [DBMS](dbms.md) - 데이터베이스 관리 시스템, 장점(공유/무결성/보안/일관성), DDL/DML/DCL 제공
  - **DBMS 유형**: RDBMS(Oracle, MySQL, PostgreSQL, SQL Server), NoSQL(MongoDB, Redis), NewSQL(TiDB, CockroachDB)
  - **핵심 기능**: 데이터 정의·조작·제어, 동시성 제어, 회복, 보안, 무결성 유지
- [ANSI/SPARC 3단계 스키마 구조](dbms.md) - 외부(External)/개념(Conceptual)/내부(Internal) 스키마
  - **외부 스키마**: 사용자 뷰(View), 각 사용자 그룹별 데이터 표현, 서브스키마
  - **개념 스키마**: 전체 논리 구조, 통합 뷰, 무결성 제약조건, 하나만 존재
  - **내부 스키마**: 물리적 저장 구조, 인덱스/해시/B+Tree, 저장 레코드 형식
  - **사상(Mapping)**: 외부/개념 사상(논리적 독립성), 개념/내부 사상(물리적 독립성)
- [데이터 독립성](dbms.md) - 논리적/물리적 독립성, 스키마 변경 영향 최소화
  - **논리적 독립성**: 개념 스키마 변경→외부 스키마 영향 없음 (응용 프로그램 수정 불필요)
  - **물리적 독립성**: 내부 스키마 변경→개념/외부 스키마 영향 없음 (인덱스 추가, 저장구조 변경)
- [데이터 모델](data_modeling.md) - 계층형/네트워크형/관계형/객체관계형/NoSQL
  - **개념적 모델**: E-R 모델 (개체-관계 모델, Chen/IE/Crow's Foot 표기법)
  - **논리적 모델**: 관계형(릴레이션), 계층형(트리 구조, 1:N만 가능), 네트워크형(그래프 구조, M:N 가능)
  - **물리적 모델**: 레코드 저장 방식, 인덱스 구조, 파티셔닝 전략
- [ERD (개체-관계 다이어그램)](data_modeling.md) - 개체(Entity)/속성(Attribute)/관계(Relationship)
  - **개체(Entity)**: 독립적으로 존재하는 객체, 사각형 표기, 강한개체/약한개체(이중 사각형)
  - **속성(Attribute)**: 타원형 표기, 단일/다중값(이중 타원), 유도/저장, 복합/단순, 키 속성(밑줄)
  - **관계(Relationship)**: 마름모 표기, 차수(Degree): 단항/이항/삼항, 재귀 관계
  - **카디날리티(Cardinality)**: 1:1(혼인), 1:N(부서-사원), M:N(학생-과목), 최소/최대값 표기 (min,max)
  - **참여도(Participation)**: 전체(이중선, 필수)/부분(단일선, 선택), 전체 참여 = 존재 종속
  - **식별 관계 vs 비식별 관계**: 약한개체 식별(이중 마름모), 강한개체 FK NULL 허용 여부
- [논리적 데이터 모델링](data_modeling.md) - ERD→릴레이션 변환, 정규화 적용
  - **개체→릴레이션 변환**: 각 개체는 테이블로, 속성은 컬럼으로
  - **1:1 관계 변환**: 어느 쪽에나 FK 삽입, 또는 병합
  - **1:N 관계 변환**: N측에 FK 삽입 (자식 테이블)
  - **M:N 관계 변환**: 연결 테이블(교차 엔티티) 생성, 두 FK 복합키
  - **다중값 속성 변환**: 별도 테이블로 분리 (1NF 위반 해결)
- [물리적 데이터 모델링](data_modeling.md) - 인덱스/파티션/클러스터/테이블스페이스 설계
  - **테이블스페이스**: 논리적 저장 공간, 데이터파일과 매핑, SYSTEM/USERS/TEMP/UNDO
  - **세그먼트**: 테이블/인덱스/롤백/임시 세그먼트, 익스텐트 집합
  - **익스텐트**: 연속된 블록 집합, 공간 할당 단위
  - **블록(페이지)**: I/O 최소 단위, 헤더+가용공간+행 데이터, Oracle 8KB/16KB, PostgreSQL 8KB
  - **클러스터링**: 자주 조인되는 테이블 물리적으로 인접 저장, 클러스터 키

### 관계 대수 / SQL
- [관계형 DB 기초](relational/relational_db.md) - 릴레이션(테이블), 튜플(행), 속성(열), 도메인, 스키마
  - **릴레이션 특성**: 순서 없음(집합), 중복 튜플 없음, 원자값(Atomic Value)
  - **카디날리티**: 튜플의 수 (행 개수), **디그리(Degree)**: 속성의 수 (열 개수)
  - **스키마 vs 인스턴스**: 스키마(정적 구조, 메타데이터) / 인스턴스(동적 데이터, 특정 시점)
- [키(Key) 종류](relational/relational_db.md) - 슈퍼키/후보키/기본키/대체키/외래키, 유일성/최소성
  - **슈퍼키(Super Key)**: 유일성 O, 최소성 X (학번+이름도 슈퍼키)
  - **후보키(Candidate Key)**: 유일성 O, 최소성 O (학번, 주민번호 등)
  - **기본키(Primary Key)**: 후보키 중 선택, NOT NULL, 불변, 단일 식별자
  - **대체키(Alternate Key)**: 후보키 중 기본키로 선택되지 않은 것
  - **외래키(Foreign Key)**: 참조 무결성, NULL 가능(약한 참조), 부모 테이블 존재 필요
  - **복합키(Composite Key)**: 두 개 이상 속성으로 구성된 기본키
- [무결성 제약](relational/relational_db.md) - 개체 무결성(PK NOT NULL), 참조 무결성(FK), 도메인 무결성, 사용자 정의
  - **개체 무결성(Entity Integrity)**: PK는 NULL 불가, 중복 불가
  - **참조 무결성(Referential Integrity)**: FK는 부모 PK 값이거나 NULL, CASCADE 옵션
  - **도메인 무결성(Domain Integrity)**: 데이터 타입, 범위, 형식, DEFAULT, CHECK 제약
  - **참조 무결성 옵션**: CASCADE(연삭제), SET NULL, SET DEFAULT, RESTRICT, NO ACTION
- [관계 대수](relational/relational_db.md) - 선택(σ)/투영(π)/합집합(∪)/교집합(∩)/차집합(-)/카테시안곱(×)/조인(⋈)/나누기(÷)
  - **순수 관계 연산**: 선택(Selection, σ), 투영(Projection, π), 조인(Join, ⋈), 나누기(Division, ÷)
  - **집합 연산**: 합집합(∪), 교집합(∩), 차집합(-), 카테시안 곱(×) - 교환/결합 법칙 성립
  - **일반 집합 연산 조건**: 합병 호환성(Union Compatibility) - 동일 속성 수, 대응 도메인 호환
  - **선택(σ)**: σ_조건(R) → 조건 만족 튜플 추출, WHERE 절 대응, 카디날리티 감소
  - **투영(π)**: π_속성(R) → 지정 속성만 추출, 중복 제거, SELECT 절 대응
  - **조인(⋈)**: R ⋈_조건 S → 카테시안 곱 + 선택, 동등조인(Equi)/자연조인(Natural)/외부조인
  - **나누기(÷)**: R ÷ S → S의 모든 속성과 매칭되는 R 튜플, "모든...을 만족하는" 질의
  - **관계 대수 vs 관계 해석**: 절차적(어떻게) vs 비절차적(무엇을), 동등 표현력
- [SQL DDL](relational/sql.md) - CREATE/ALTER/DROP/TRUNCATE, 제약조건(NOT NULL/UNIQUE/CHECK/PK/FK)
  - **CREATE**: 스키마 정의, 컬럼 정의, 제약조건 정의, 테이블스페이스 지정
  - **ALTER**: ADD(컬럼/제약), MODIFY(타입/크기), DROP(컬럼/제약), RENAME
  - **DROP vs TRUNCATE vs DELETE**: DDL(구조삭제, 롤백불가)/DDL(전체삭제, 롤백불가)/DML(선택삭제, 롤백가능)
  - **CASCADE**: DROP시 참조 객체 함께 삭제 (DROP TABLE t CASCADE)
  - **제약조건 명명**: CONSTRAINT pk_student PRIMARY KEY(id), 제약조건 관리 용이
- [SQL DML](relational/sql.md) - SELECT/INSERT/UPDATE/DELETE, MERGE(UPSERT)
  - **INSERT**: VALUES(단일), SELECT(벌크), INSERT INTO ... SELECT ... FROM ...
  - **UPDATE**: SET 절, WHERE 생략 시 전체 수정, 서브쿼리 사용 가능
  - **DELETE**: WHERE 생략 시 전체 삭제, TRUNCATE보다 느리지만 로깅, 롤백 가능
  - **MERGE(UPSERT)**: ON 조건 → MATCHED(UPDATE)/NOT MATCHED(INSERT), 동기화 작업
- [SQL DCL/TCL](relational/sql.md) - GRANT/REVOKE, COMMIT/ROLLBACK/SAVEPOINT
  - **GRANT**: 권한 부여, GRANT SELECT, INSERT ON table TO user WITH GRANT OPTION
  - **REVOKE**: 권한 회수, REVOKE SELECT ON table FROM user CASCADE
  - **WITH GRANT OPTION**: 받은 권한을 다른 사용자에게 부여 가능
  - **권한 종류**: SELECT/INSERT/UPDATE/DELETE(객체), CREATE/ALTER/DROP(시스템)
  - **COMMIT**: 트랜잭션 확정, 변경사항 영구 저장, 락 해제
  - **ROLLBACK**: 트랜잭션 취소, 마지막 COMMIT 지점으로 복구
  - **SAVEPOINT**: 부분 롤백 지점, ROLLBACK TO savepoint_name
- [고급 SQL](relational/sql.md) - 서브쿼리(상관/비상관), JOIN(INNER/OUTER/CROSS/SELF), 집계함수, GROUP BY/HAVING
  - **스칼라 서브쿼리**: 단일 값 반환, SELECT 절/HAVING 절 사용
  - **인라인 뷰**: FROM 절 서브쿼리, 동적 뷰, 임시 결과셋
  - **상관 서브쿼리(Correlated)**: 외부 쿼리 컬럼 참조, 행별 실행, EXISTS/NOT EXISTS
  - **비상관 서브쿼리**: 독립 실행, 한 번만 수행, IN/ANY/ALL
  - **JOIN 종류**: INNER(교집합), LEFT/RIGHT/FULL OUTER, CROSS(카테시안), SELF(자기참조)
  - **집계함수**: COUNT(*)/COUNT(col)/SUM/AVG/MAX/MIN, NULL 제외(COUNT(*) 제외)
  - **GROUP BY**: 그룹화, 집계함수와 함께 사용, SELECT 절 집계함수/GROUP BY 컬럼만 허용
  - **HAVING vs WHERE**: 그룹 필터링(집계함수 가능) vs 행 필터링(집계함수 불가)
  - **WITH(CTE)**: 공통 테이블 식, 복잡 쿼리 모듈화, 재귀 CTE(계층형 데이터)
- [윈도우 함수](relational/sql.md) - OVER(), PARTITION BY, RANK/ROW_NUMBER/LAG/LEAD, 분석 함수
  - **기본 구문**: 함수명() OVER([PARTITION BY ...] [ORDER BY ...] [frame_clause])
  - **순위 함수**: RANK(동순위-건너뜀), DENSE_RANK(동순위-건너뜀X), ROW_NUMBER(고유번호)
  - **집계 윈도우**: SUM/AVG/COUNT/MAX/MIN OVER(), 누적/이동 집계
  - **LAG(col, n)/LEAD(col, n)**: 이전/이후 행 값 참조, 시계열 분석
  - **FIRST_VALUE/LAST_VALUE**: 파티션 내 첫/마지막 값
  - **NTILE(n)**: n개 그룹으로 분할, 백분위 계산
  - **프레임 절**: ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW (누적)
- [정적 SQL vs 동적 SQL](relational/sql.md) - 컴파일 타임 vs 런타임 SQL, 커서(DECLARE/OPEN/FETCH/CLOSE)
  - **정적 SQL(Static SQL)**: 컴파일 시 쿼리 확정, 실행계획 고정, 성능 예측 가능
  - **동적 SQL(Dynamic SQL)**: 런타임 쿼리 생성, EXECUTE IMMEDIATE, 유연성↑/성능↓
  - **SQL Injection 위험**: 동적 SQL 사용 시 파라미터화 필수
  - **커서(Cursor)**: 결과셋 순차 접속, DECLARE→OPEN→FETCH→CLOSE
  - **커서 종류**: 암시적(Implicit, 자동)/명시적(Explicit, 수동), FORWARD_ONLY/SCROLL
  - **REF CURSOR**: 포인터 기반 커서, 동적 쿼리 결과 전달
- [뷰(View)](relational/sql.md) - 가상 테이블, 보안/단순화, 구체화 뷰(Materialized View), 뷰 갱신 제약
  - **뷰 특성**: 실제 데이터 저장X, 정의만 저장(메타데이터), 사용 시 쿼리 변환
  - **뷰 장점**: 보안(컬럼/행 숨김), 단순화(복잡 쿼리 캡슐화), 독립성(스키마 변경 영향 최소)
  - **뷰 갱신 조건**: 단일 테이블, 집계함수X, DISTINCTX, GROUP BYX, UNIONX
  - **INSTEAD OF 트리거**: 뷰 갱신 불가 시 대체 동작 정의
  - **구체화 뷰(Materialized View)**: 실제 데이터 저장, 주기적 갱신, 성능 향상, Oracle/PostgreSQL
  - **WITH CHECK OPTION**: 뷰 정의 조건 위반하는 INSERT/UPDATE 차단
- [저장 프로시저](relational/sql.md) - PL/SQL, 비즈니스 로직 DB 내장, 성능/보안 이점
  - **PL/SQL 구조**: DECLARE(선언부)→BEGIN(실행부)→EXCEPTION(예외처리)→END
  - **장점**: 네트워크 트래픽 감소(쿼리 일괄 전송), SQL 주입 방지, 캡슐화, 권한 분리
  - **단점**: DB 의존성, 디버깅 어려움, 확장성 제한, DB 서버 부하
  - **IN/OUT/INOUT 파라미터**: 입력/출력/양방향 파라미터
  - **프로시저 vs 함수**: 반환값X/여러 SQL 실행(Call)/트랜잭션 가능 vs 반환값O/단일 값(SELECT)/트랜잭션 제한
- [트리거(Trigger)](relational/sql.md) - BEFORE/AFTER, INSERT/UPDATE/DELETE 이벤트, FOR EACH ROW
  - **트리거 구성**: 이벤트(INSERT/UPDATE/DELETE) + 시점(BEFORE/AFTER) + 동작(SQL 블록)
  - **행 레벨 트리거**: FOR EACH ROW, :OLD/:NEW 의사레코드 접근
  - **문장 레벨 트리거**: FOR EACH STATEMENT, 행별 한 번만 실행
  - **CASCADE 트리거**: 트리거가 다른 트리거 유발, 순환 주의
  - **트리거 용도**: 무결성 검사, 감사 로그(Audit), 파생 컬럼 자동 계산, 복제
- [함수(Function)](relational/sql.md) - 스칼라/집계/테이블 값 함수, 사용자 정의 함수(UDF)
  - **스칼라 함수**: 단일 값 반환, UPPER/LOWER/LENGTH/SUBSTR/COALESCE/NVL
  - **집계 함수**: 그룹당 단일 값, COUNT/SUM/AVG/MAX/MIN
  - **테이블 값 함수(TVF)**: 테이블 반환, FROM 절 사용, 인라인/다중문
  - **내장 함수**: 문자열(CONCAT/TRIM/REPLACE), 날짜(DATEADD/DATEDIFF/EXTRACT), NULL(COALESCE/NULLIF)
  - **UDF 주의**: SELECT 절 UDF는 행별 실행→성능 저하, 집계 대신 윈도우 함수 권장

### 정규화
- [정규화 목적](normalization.md) - 이상 현상(삽입/삭제/갱신 이상) 제거, 데이터 중복 최소화
  - **삽입 이상(Insertion Anomaly)**: 불필요한 데이터를 함께 삽입해야 함 (학생 정보 없이 과목만 등록 불가)
  - **삭제 이상(Deletion Anomaly)**: 한 튜플 삭제로 원치 않는 정보까지 손실 (학생 삭제→과목 정보 손실)
  - **갱신 이상(Update Anomaly)**: 중복 데이터 일부만 갱신→일관성 위반 (주소 변경 시 일부만 반영)
- [함수적 종속성(Functional Dependency)](normalization.md) - X→Y (X가 Y를 결정), 결정자(Determinant)/종속자(Dependent)
  - **완전 함수 종속(FFD)**: Y가 X 전체에 종속, X의 진부분집합에는 종속하지 않음
  - **부분 함수 종속(PFD)**: Y가 X의 진부분집합에 종속 (복합키의 일부에만 의존)
  - **이행 함수 종속(TFD)**: X→Y, Y→Z 이면 X→Z (간접 종속)
  - **다치 종속(MVD)**: X↠Y (X값이 Y의 다중 값 집합 결정), 4NF 위반 원인
  - **조인 종속(JD)**: 릴레이션을 무손실 분해 후 재조인 가능, 5NF 관련
- [1NF (제1정규형)](normalization.md) - 모든 속성의 원자성(Atomicity) 보장
  - **조건**: 릴레이션 모든 속성이 원자값, 반복 그룹(Repeating Group) 제거
  - **위반 예**: 한 셀에 "수학,영어,과학" (다중값), 복수 행 반복 패턴
  - **해결**: 반복 그룹→별도 테이블 분리, 다중값 속성→행 분리 또는 별도 테이블
- [2NF (제2정규형)](normalization.md) - 1NF + 부분 함수 종속 제거 (복합키에서만 해당)
  - **조건**: 모든 비주요 속성이 기본키에 완전 함수 종속
  - **위반 예**: (학번,과목코드)→성적, 학번→학과 (학과는 학번에만 종속→부분 종속)
  - **해결**: 부분 종속 속성을 별도 테이블로 분리 (학생(학번,학과), 성적(학번,과목,점수))
  - **판단 기준**: 단일 컬럼 PK면 자동 2NF 만족
- [3NF (제3정규형)](normalization.md) - 2NF + 이행 함수 종속 제거
  - **조건**: 비주요 속성이 기본키에만 직접 종속 (다른 비주요 속성 통한 간접 종속 제거)
  - **위반 예**: 학번→학과코드→학과명 (학과명이 학과코드를 통해 이행 종속)
  - **해결**: 이행 종속 제거 위해 분해 (학생(학번,학과코드), 학과(학과코드,학과명))
  - **정리**: 비PK→비PK 종속 제거
- [BCNF (Boyce-Codd 정규형)](normalization.md) - 3NF의 강화 형태, 모든 결정자가 후보키
  - **조건**: X→Y일 때 X가 반드시 후보키여야 함
  - **3NF vs BCNF 차이**: 3NF는 비주요 속성의 결정자만 제거, BCNF는 모든 결정자 검사
  - **위반 예**: (학생,과목)→교수, 교수→과목 (교수가 결정자지만 후보키 아님)
  - **해결**: 교수 테이블 분리, 무손실 분해 보장
  - **주의**: BCNF 분해 시 종속성 보존 안 될 수 있음
- [4NF (제4정규형)](normalization.md) - BCNF + 다치 종속(MVD) 제거
  - **다치 종속**: X↠Y|Z (X값이 Y집합과 Z집합을 독립적으로 결정)
  - **위반 예**: 학생→→과목, 학생→→동아리 (한 학생이 여러 과목, 여러 동아리 독립적 다중값)
  - **문제점**: 카테시안 곱 발생 (과목×동아리 조합만큼 행 증가)
  - **해결**: 다치 속성별 별도 테이블 분리 (수강(학생,과목), 동아리가입(학생,동아리))
- [5NF (제5정규형/PJNF)](normalization.md) - 4NF + 조인 종속(Join Dependency) 제거
  - **조인 종속**: R = R1 ⋈ R2 ⋈ ... ⋈ Rn (무손실 다중 분해 가능)
  - **위반 예**: 공급자-부품-프로젝트 (SPJ), 순환 제약 발생 시
  - **판단**: 모든 조인 종속이 후보키에 의한 것일 때 5NF
  - **실무**: 5NF까지 정규화 드묾, 복잡한 비즈니스 제약 표현 시 고려
- [DK/NF (도메인-키 정규형)](normalization.md) - 모든 제약조건이 도메인과 키로 표현
  - **이론적 최종 단계**: 5NF보다 강력한 조건
  - **실제**: 달성 불가능한 경우 많음
- [반정규화(Denormalization)](normalization.md) - 성능 최적화를 위한 의도적 정규화 역행
  - **목적**: 조인 감소→읽기 성능 향상, 테이블 수 감소
  - **기법**: 테이블 합병(Merge), 파생 컬럼 추가(합계, 평균), 중복 컬럼 허용
  - **트레이드오프**: 읽기 성능↑ vs 쓰기 성능↓, 중복↑→일관성 유지 비용↑
  - **적용 시점**: 읽기 빈도 높음, 실시간 분석, 대용량 데이터 웨어하우스
  - **주의**: 트리거/애플리케이션으로 일관성 유지 필요

### 인덱스 / 쿼리 최적화
- [인덱스 기본 원리](db_index.md) - 탐색 속도 향상, B+Tree 기본 구조
  - **검색 복잡도**: O(log n) (인덱스) vs O(n) (풀스캔)
  - **트레이드오프**: SELECT 성능↑ vs INSERT/UPDATE/DELETE 성능↓ (인덱스 갱신 비용)
  - **선택도(Selectivity)** = (고유 값 수) / (전체 행 수) → 높을수록 인덱스 효율↑
  - **카디날리티(Cardinality)**: 컬럼의 고유 값 개수, 높을수록 인덱스 유리
  - **밀도(Density)** = 1 / 카디날리티, 낮을수록 선택적↑ → 인덱스 효율↑
  - **비용 공식**: 인덱스 사용 비용 = 트리 높이(=log n) + 리프 블록 I/O + 테이블 액세스
- [B-Tree 인덱스](db_index.md) - 균형 트리, 분기 계수(Degree) m
  - **구조**: 루트→내부노드→리프, 모든 리프 노드 동일 깊이
  - **노드 구조**: 키(정렬) + 포인터, 최소 ⌈m/2⌉~m-1개 키
  - **검색**: 루트→리프 경로 탐색, O(log n)
  - **삽입**: 리프에 키 추가→오버플로우 시 분할(Split)→부모로 전파
  - **삭제**: 키 제거→언더플로우 시 형제에서 차용 또는 병합
- [B+Tree 인덱스](db_index.md) - DB 인덱스 표준, B-Tree 확장
  - **B-Tree vs B+Tree 차이점**:
    | 특성 | B-Tree | B+Tree |
    |------|--------|--------|
    | 내부노드 데이터 | O (키+데이터) | X (키만) |
    | 리프노드 연결 | X | O (순차 포인터) |
    | 데이터 중복 | X | O (내부+리프) |
    | 범위 검색 | 비효율 | 효율적 (순차 접근) |
  - **리프 노드 구조**: (키, 데이터 포인터/ROWID) + 순차 링크
  - **장점**: 범위 스캔 효율, 더 많은 키 저장(내부노드), 순차 접근 최적
  - **높이 계산**: h ≈ log_f(n), f=팬아웃(한 노드 자식 수), n=레코드 수
- [해시 인덱스](db_index.md) - 등치 탐색 전용, O(1)
  - **해시 함수**: h(key) → 버킷 주소, 충돌 해결(체이닝/개방주소법)
  - **장점**: 등치 검색(=) 최고 성능, 단일 레코드 조회
  - **단점**: 범위 검색(>, <, BETWEEN) 불가, 정렬 불가, LIKE 불가
  - **적용**: 메모리 DB(Redis), HashMap, 제한적 RDBMS(MySQL MEMORY 엔진)
- [비트맵 인덱스](db_index.md) - 각 값별 비트맵 생성
  - **구조**: 값→비트맵(각 행 1비트), 예: 성별(남:1010, 여:0101)
  - **적합 조건**: 낮은 카디날리티(성별, 상태코드, 지역), 읽기 위주
  - **장점**: 복합 조건 비트 연산(AND/OR/NOT) → 고속, 저장 공간 작음
  - **단점**: 동시 쓰기 시 락 경합 심각, OLTP 부적합
  - **활용**: OLAP, 데이터 웨어하우스, Oracle/PostgreSQL
- [클러스터드/논클러스터드 인덱스](db_index.md) - 물리적 정렬 여부
  - **클러스터드(Clustered)**: 테이블 데이터 자체가 인덱스 순서로 정렬 저장
    - 테이블당 1개만 가능 (PK 또는 지정), 리프=실제 데이터
    - 장점: 범위 스캔 빠름, PK 검색 최고, 정렬된 데이터
    - 단점: INSERT 시 페이지 분할(Page Split), UPDATE 시 행 이동
  - **논클러스터드(Non-clustered)**: 별도 인덱스 구조, 리프=ROWID/포인터
    - 테이블당 다수 가능, 원본 데이터 순서 유지
    - 조회 시: 인덱스 탐색→ROWID로 테이블 액세스 (키 룩업)
  - **커버링 인덱스(Covering Index)**: 쿼리 필요 컬럼 모두 인덱스 포함→테이블 액세스 불필요
    - 예: `SELECT name FROM users WHERE id = 1` + 인덱스(id, name)
- [복합 인덱스(Composite Index)](db_index.md) - 다중 컬럼 인덱스
  - **왼쪽 접두어 규칙(Leftmost Prefix Rule)**: 인덱스(col1, col2, col3)
    - WHERE col1='a' → 인덱스 사용 O
    - WHERE col1='a' AND col2='b' → 인덱스 사용 O
    - WHERE col2='b' → 인덱스 사용 X (col1 누락)
  - **컬럼 순서 원칙**: 선택도 높은 컬럼 우선, WHERE 조건 빈도, 정렬/그룹화 고려
  - **스킵 스캔(Skip Scan)**: MySQL 8.0+, Oracle→선행 컬럼 조건 없어도 사용 가능 (성능 저하)
- [함수 기반 인덱스(Function-Based Index)](db_index.md) - 표현식 기반 인덱스
  - **용도**: `WHERE UPPER(name) = 'KIM'` → 인덱스(UPPER(name))
  - **계산 컬럼 인덱스**: `(salary * 12)` 연봉 계산식 인덱싱
  - **부분 인덱스(Partial Index)**: 조건부 인덱스, `WHERE status = 'active'` 행만
  - **주의**: 함수 사용 시 데이터 변경 시마다 재계산→쓰기 비용↑
- [인덱스 스캔 방식](db_index.md) - 옵티마이저 선택
  - **Index Unique Scan**: 유니크 인덱스 등치 검색, 최대 1건
  - **Index Range Scan**: 범위 검색, 시작점~끝점 스캔
  - **Index Full Scan**: 인덱스 전체 스캔 (테이블 풀스캔보다 나은 경우)
  - **Index Fast Full Scan**: 물리적 순서로 읽기 (순서 보장X, 속도↑)
  - **Index Skip Scan**: 선행 컬럼 건너뛰고 후행 컬럼으로 검색
- [실행 계획(Execution Plan)](db_index.md) - EXPLAIN/EXPLAIN ANALYZE
  - **연산자 종류**: Seq Scan(풀스캔), Index Scan, Bitmap Index Scan, Hash Join, Nested Loop, Merge Join
  - **비용(Cost)**: 상대적 수치, 시작 비용 + 총 비용
  - **행 수(Rows)**: 예측 행 수, 통계 정보 기반
  - **실제 실행 시간**: EXPLAIN ANALYZE로 실제 측정 (PostgreSQL)
- [쿼리 옵티마이저](db_index.md) - 최적 실행 계획 수립
  - **RBO(Rule-Based Optimizer)**: 규칙 기반, 인덱스 존재→사용 (레거시)
  - **CBO(Cost-Based Optimizer)**: 비용 기반, 통계 정보로 비용 계산→최소 비용 선택
  - **통계 정보**: 테이블 행 수, 컬럼 카디날리티, 값 분포(Histogram), 인덱스 깊이
  - **힌트(Hint)**: 옵티마이저 강제 지정 (USE INDEX, FORCE INDEX, INDEX_JOIN)
  - **파라미터 스니핑(Parameter Sniffing)**: 첫 실행 시 파라미터 기준 계획→후속 실행 재사용→비효율
- [쿼리 튜닝 기법](db_index.md) - 성능 최적화
  - **인덱스 추가/변경**: WHERE, JOIN, ORDER BY, GROUP BY 대상
  - **서브쿼리→JOIN 변환**: 상관 서브쿼리→LEFT JOIN (성능 향상)
  - **커버링 인덱스 활용**: SELECT 컬럼 모두 인덱스에 포함
  - **LIKE 최적화**: 'A%'(인덱스 O), '%A'(인덱스 X)
  - **OR→UNION ALL**: OR 조건 분리→각각 인덱스 활용
  - **페이징 최적화**: OFFSET 대신 커서 기반 (WHERE id > last_id)
- [파티셔닝(Partitioning)](db_index.md) - 대용량 테이블 분할
  - **수평 분할(Horizontal)**: 행 단위 분할 (샤딩과 유사, 단일 DB 내)
  - **수직 분할(Vertical)**: 컬럼 단위 분할 (자주 사용 컬럼 분리)
  - **분할 기준**:
    - RANGE: 날짜(2024-01, 2024-02...), 숫자 범위
    - LIST: 지역, 카테고리 등 이산값
    - HASH: 해시 함수 % 파티션 수
    - COMPOSITE: RANGE+HASH 복합
  - **파티션 프루닝(Pruning)**: 조건에 맞는 파티션만 스캔 (불필요 파티션 제외)
  - **장점**: 관리 용이(파티션별 백업/삭제), 병렬 처리, 인덱스 크기 감소
  - **주의**: 파티션 키 선택 중요, 전역 인덱스 vs 지역 인덱스

### 트랜잭션 / 동시성
- [트랜잭션(Transaction)](transaction.md) - 논리적 작업 단위, ACID 특성
  - **정의**: 하나의 논리적 기능 수행 위한 작업 집합, 전부 성공(COMMIT) 또는 전부 실패(ROLLBACK)
  - **상태 전이**: 활성(Active)→부분커밋(Partial Commit)→커밋(Committed) / 실패(Failed)→철회(Aborted)
  - **트랜잭션 경계**: BEGIN TRANSACTION → SQL문들 → COMMIT/ROLLBACK
- [ACID 속성](transaction.md) - 트랜잭션 4대 특성
  - **A(원자성, Atomicity)**: All or Nothing, 실행 완료되거나 전혀 실행되지 않음
    - 구현: WAL(Write-Ahead Logging), Undo Log
  - **C(일관성, Consistency)**: 트랜잭션 전후 데이터 무결성 유지 (제약조건, 트리거)
    - 구현: 선언적 무결성 제약(CHECK, FK), 애플리케이션 로직
  - **I(격리성, Isolation)**: 동시 실행 트랜잭션 간 간섭 없음, 독립 실행 효과
    - 구현: Lock, MVCC, 격리 수준 설정
  - **D(지속성, Durability)**: 커밋된 트랜잭션 결과는 영구 저장 (시스템 장애에도)
    - 구현: WAL, Redo Log, 체크포인트, 미러링
- [트랜잭션 격리 수준(Isolation Level)](concurrency_control.md) - 동시성 제어 강도
  - **Read Uncommitted**: 더티 읽기 허용, 격리 최소, 동시성 최대
  - **Read Committed**: 커밋된 데이터만 읽기, Non-Repeatable Read 발생 가능
  - **Repeatable Read**: 동일 쿼리 동일 결과 보장, Phantom Read 발생 가능 (MySQL InnoDB: Gap Lock으로 방지)
  - **Serializable**: 완전 직렬화, 동시성 최소, 격리 최대
  - **격리 수준별 현상**:
    | 격리 수준 | Dirty Read | Non-Repeatable | Phantom |
    |----------|------------|----------------|---------|
    | Read Uncommitted | O | O | O |
    | Read Committed | X | O | O |
    | Repeatable Read | X | X | O* |
    | Serializable | X | X | X |
    *MySQL InnoDB는 넥스트 키 락으로 Phantom Read 방지
- [동시성 문제(Concurrency Problems)](concurrency_control.md)
  - **Dirty Read**: 커밋되지 않은 데이터 읽기, 롤백 시 문제
    - T1이 값 변경(미커밋)→T2가 읽음→T1 롤백→T2가 읽은 값 무효
  - **Non-Repeatable Read**: 같은 행 두 번 읽기→다른 값
    - T1이 행 읽음→T2가 수정+커밋→T1이 다시 읽음→값 변경
  - **Phantom Read**: 같은 조건 쿼리→행 수 변화
    - T1이 WHERE 조건 조회→T2가 새 행 삽입→T1 재조회→새 행 출현
  - **Lost Update**: T1 수정→T2 수정→T1 수정 사항 덮어쓰기 손실
  - **Write Skew**: 두 트랜잭션이 각자 조건 충족→동시 수정→전체 조건 위반 (Serializable 필요)
- [잠금(Lock)](concurrency_control.md) - 동시 접근 제어 메커니즘
  - **공유 잠금(Shared Lock, S-Lock)**: 읽기 전용, 여러 트랜잭션 동시 획득 가능
  - **배타 잠금(Exclusive Lock, X-Lock)**: 읽기+쓰기, 단독만 가능
  - **잠금 호환성 행렬**:
    | | S-Lock | X-Lock |
    |--|--------|--------|
    | S-Lock | O | X |
    | X-Lock | X | X |
  - **잠금 세분도(Granularity)**: DB→테이블→페이지→행→컬럼
    - 세분화↑: 동시성↑, 오버헤드↑
    - 대형화↓: 동시성↓, 오버헤드↓
  - **의도 잠금(Intent Lock)**: 상위 계층 잠금 의도 표시 (IS, IX, SIX)
  - **자동 증가 잠금(Auto-Inc Lock)**: AUTO_INCREMENT 동시성 제어
- [2단계 잠금 프로토콜(2PL, Two-Phase Locking)](concurrency_control.md) - 직렬 가능성 보장
  - **확장 단계(Growing Phase)**: 잠금 획득만 가능, 해제 불가
  - **수축 단계(Shrinking Phase)**: 잠금 해제만 가능, 획득 불가
  - **Lock Point**: 확장→수축 전환점
  - **보장**: 직렬 가능성(Serializability) 보장, 교착상태 발생 가능
  - **변형**:
    - Basic 2PL: 교착상태 가능
    - Strict 2PL: X-Lock은 트랜잭션 종료까지 유지 (연쇄 롤백 방지)
    - Rigorous 2PL: 모든 Lock 종료까지 유지
- [교착상태(Deadlock)](concurrency_control.md) - 순환 대기 상태
  - **발생 조건 (4가지 모두 충족)**:
    1. 상호 배제(Mutual Exclusion): 자원 독점
    2. 점유 대기(Hold and Wait): 자원 보유+다른 자원 대기
    3. 비선점(No Preemption): 강제 회수 불가
    4. 순환 대기(Circular Wait): T1→T2→T3→T1
  - **해결 방안**:
    - **예방(Prevention)**: 자원 순서 부여 (모든 트랜잭션이 같은 순서로 잠금)
    - **회피(Avoidance)**: Wait-Die(오래된 것이 대기)/Wound-Wait(오래된 것이 선점)
    - **탐지(Detection)**: 대기 그래프(Wait-For Graph) 분석, 주기적 탐지
    - **복구(Recovery)**: 피해자(Victim) 선택→롤백, 타임아웃 강제 롤백
- [MVCC (Multi-Version Concurrency Control)](concurrency_control.md) - 다중 버전 동시성 제어
  - **원리**: 갱신 시 기존 버전 유지, 새 버전 생성→읽기와 쓰기 비차단
  - **구조**: 버전 체인(Version Chain), Undo Log 활용, Read View
  - **장점**: 읽기 작업이 쓰기 작업 블로킹X, 높은 동시성, 일관된 스냅샷 읽기
  - **단점**: 버전 관리 오버헤드, 주기적 가비지 컬렉션(Vacuum) 필요
  - **구현 예**:
    - MySQL InnoDB: Undo Log로 이전 버전, Read View로 가시성 판단
    - PostgreSQL: xmin/xmax 시스템 컬럼, MVCC 스냅샷, VACUUM
    - Oracle: Undo Segment, SC(System Change) 번호
- [낙관적/비관적 동시성 제어](concurrency_control.md) - 충돌 처리 전략
  - **비관적(Pessimistic)**: 충돌 자주 발생 가정, 잠금으로 미리 방지
    - 읽기 시에도 잠금, 충돌 시 대기
    - 장점: 충돌 빈번 시 효율, 일관성 보장
    - 단점: 동시성 저하, 교착상태 가능
  - **낙관적(Optimistic)**: 충돌 드물다고 가정, 커밋 시 충돌 검사
    - 읽기: 버전 번호/타임스탬프 확인, 쓰기: 커밋 시점 검증(Validation)
    - 3단계: 읽기→검증→쓰기
    - 장점: 높은 동시성, 잠금 오버헤드 없음
    - 단점: 충돌 시 재시도 비용, 롤백 빈번 시 비효율
  - **선택 기준**: 충돌 빈도 낮음→낙관적, 충돌 빈도 높음→비관적
- [타임스탬프 기반 순서화](concurrency_control.md) - 트랜잭션 순서 부여
  - **W-TS(R)**: R 항목에 기록한 최대 타임스탬프, **R-TS(R)**: R 항목을 읽은 최대 타임스탬프
  - **규칙**: T가 R 읽기→TS(T) ≥ W-TS(R), T가 R 쓰기→TS(T) ≥ R-TS(R) ∧ TS(T) ≥ W-TS(R)
  - **위반 시**: 트랜잭션 롤백, 새 타임스탬프로 재시작
- [WAL (Write-Ahead Logging)](recovery.md) - 선로그 기록 원칙
  - **원칙**: 데이터 변경 전 반드시 로그 먼저 기록
  - **목적**: 원자성(롤백 시 UNDO), 지속성(장애 복구 시 REDO)
  - **로그 구조**: LSN(Log Sequence Number), 트랜잭션ID, 타입(BEGIN/INSERT/UPDATE/DELETE/COMMIT), 전후 이미지(Before/After Image)
  - **체크포인트(Checkpoint)**: 주기적 일관성 지점 생성, 복구 시간 단축
- [회복(Recovery)](recovery.md) - 장애 후 일관성 복원
  - **장애 유형**: 트랜잭션(논리오류), 시스템(전원, SW), 미디어(디스크)
  - **회복 기법**:
    - **UNDO**: 미완료 트랜잭션 변경 사항 취소 (이전 값으로 복원)
    - **REDO**: 완료된 트랜잭션 재실행 (로그→데이터 적용)
    - **ARIES(Algorithm for Recovery and Isolation Exploiting Semantics)**:
      1. Analysis: 로그 분석→복구 대상 식별
      2. Redo: 모든 변경 재실행 (커밋 여부 무관)
      3. Undo: 미완료 트랜잭션 취소
  - **즉시 갱신(Immediate Update)**: 로그 기록 후 즉시 디스크 반영 (UNDO/REDO 모두 필요)
  - **지연 갱신(Deferred Update)**: 커밋 시점에만 디스크 반영 (UNDO 불필요)
- [Savepoint & 중첩 트랜잭션](transaction.md) - 부분 롤백
  - **SAVEPOINT**: 트랜잭션 내 롤백 지점 설정, `ROLLBACK TO savepoint_name`
  - **중첩 트랜잭션(Nested Transaction)**: 트랜잭션 내 하위 트랜잭션, 독립적 커밋/롤백
  - **Saga 패턴**: 분산 트랜잭션, 연속적 로컬 트랜잭션+보상 트랜잭션(Compensating)

### 분산 / 고급 DB
- [분산 데이터베이스(Distributed Database)](distributed_database.md) - 다수 노드에 분산 저장·처리
  - **분산 투명성(Transparency) 4종류**:
    - 위치 투명성(Location): 데이터 물리적 위치 모름
    - 복제 투명성(Replication): 복제본 존재 모름
    - 분할 투명성(Fragmentation): 데이터 분할 여부 모름
    - 장애 투명성(Failure): 부분 장애에도 서비스 지속
  - **동종(Homogeneous) vs 이종(Heterogeneous)**: DBMS 동일 vs DBMS 상이
  - **장점**: 가용성↑, 확장성↑, 성능↑, 지역성
  - **단점**: 복잡성↑, 분산 트랜잭션 오버헤드, 일관성 유지 어려움
- [복제(Replication)](distributed_database.md) - 데이터 다중 복사본 유지
  - **마스터-슬레이브(Primary-Replica)**: 쓰기→마스터, 읽기→슬레이브 분산
    - 장점: 읽기 확장, 단순 구조
    - 단점: 쓰기 단일 병목, 마스터 장애 시 페일오버 필요
  - **마스터-마스터(Multi-Master)**: 모든 노드 쓰기 가능
    - 장점: 쓰기 확장, 고가용성
    - 단점: 충돌 해결 복잡 (Last-Write-Wins, CRDT)
  - **동기(Sync) vs 비동기(Async)**:
    - 동기: 일관성 보장, 지연↑ (모든 복제본 확인 후 응답)
    - 비동기: 지연↓, 일관성↓ (복제 지연 Replication Lag 발생 가능)
  - **읽기 일관성 레벨**: Strong(동기), Eventual(비동기), Quorum(과반수)
- [샤딩(Sharding)](distributed_database.md) - 수평 분할 기법
  - **샤드 키(Shard Key)**: 데이터 분배 기준 컬럼 (해시, 범위)
  - **샤딩 전략**:
    - **Range Sharding**: 키 범위별 분할 (1-1000→S1, 1001-2000→S2)
      - 장점: 범위 쿼리 효율
      - 단점: 핫스팟(Hotspot) 가능 (최신 데이터 몰림)
    - **Hash Sharding**: `shard = hash(key) % num_shards`
      - 장점: 균등 분배
      - 단점: 범위 쿼리 비효율, 리샤딩 어려움
    - **Directory Sharding**: 룩업 테이블로 매핑
      - 장점: 유연성
      - 단점: 룩업 오버헤드, 단일 실패점
  - **핫스팟 문제**: 특정 샤드에 부하 집중→해결: Consistent Hashing, Composite Key
  - **리샤딩(Resharding)**: 샤드 추가 시 재분배→데이터 마이그레이션 필요
- [2PC (Two-Phase Commit)](distributed_database.md) - 분산 트랜잭션 원자성 보장
  - **참여자**: Coordinator(코디네이터), Participants(참여 노드들)
  - **Phase 1 - Prepare**:
    1. Coordinator: 모든 참여자에게 PREPARE 전송
    2. Participants: 트랜잭션 실행, 잠금 획득, 로그 기록
    3. Participants: 준비 완료 시 VOTE_COMMIT, 실패 시 VOTE_ABORT 응답
  - **Phase 2 - Commit/Abort**:
    - 모든 VOTE_COMMIT→GLOBAL_COMMIT 전송→참여자 커밋
    - 하나라도 VOTE_ABORT→GLOBAL_ABORT 전송→참여자 롤백
  - **장점**: 원자성 보장
  - **단점**:
    - 블로킹: 코디네이터 장애 시 참여자 대기
    - 성능: 2번의 왕복, 동기화 오버헤드
    -단일 실패점: 코디네이터
  - **개선**: 3PC(3단계 커밋), Paxos, Raft
- [CAP 정리(Theorem)](distributed_database.md) - 분산 시스템 트레이드오프
  - **C(Consistency)**: 모든 노드 동일 데이터 (강한 일관성)
  - **A(Availability)**: 모든 요청 응답 보장 (장애 노드 있어도)
  - **P(Partition Tolerance)**: 네트워크 분할 시에도 동작
  - **조합**:
    - **CP**: 일관성 우선, 가용성 희생 (MongoDB, HBase, Redis)
    - **AP**: 가용성 우선, 일관성 희생 (Cassandra, DynamoDB, CouchDB)
    - **CA**: 분할 없는 환경에서만 가능 (단일 노드 RDBMS)
  - **실제**: P는 선택 불가(네트워크 장애 필연), C vs A 선택
  - **Eric Brewer(2000)** 제안
- [PACELC 이론](distributed_database.md) - CAP 확장
  - **P(Partition)**: 분할 발생 시 A(Availability) vs C(Consistency) 선택
  - **E(Else)**: 정상 상태 시 L(Latency) vs C(Consistency) 선택
  - **분류**:
    - PC/EC: 항상 일관성 우선 (MySQL, PostgreSQL)
    - PC/EL: 분할 시 일관성, 정상 시 지연 우선 (MongoDB)
    - PA/EL: 항상 가용성/지연 우선 (Cassandra)
    - PA/EC: 분할 시 가용성, 정상 시 일관성 (DynamoDB)
- [BASE 속성](distributed_database.md) - NoSQL 트랜잭션 모델
  - **BA(Basically Available)**: 기본적 가용성, 부분 장애에도 서비스
  - **S(Soft State)**: 상태가 시간에 따라 변할 수 있음 (일시적 불일치 허용)
  - **E(Eventually Consistent)**: 최종적 일관성, 시간 경과 시 모든 노드 동일 상태
  - **vs ACID**: 강한 일관성(ACID) vs 높은 가용성(BASE)
- [합의 알고리즘(Consensus)](distributed_database.md) - 분산 시스템 합의
  - **Paxos**: Leslie Lamport, Prepare-Promise, Accept-Accepted, 복잡
  - **Raft**: Leader Election + Log Replication, 이해 쉬움, etcd/Consul
  - **ZAB(Zookeeper Atomic Broadcast)**: Leader-Follower, Zookeeper
  - **PBFT(Practical Byzantine Fault Tolerance)**: 악의적 노드 허용, 블록체인

### NoSQL / 신기술 DB
- [NoSQL 유형](nosql/nosql_overview.md) - 비관계형 DB 분류
  | 유형 | 데이터 모델 | 대표 제품 | 적합 용도 |
  |------|------------|----------|----------|
  | 키-값 | Key→Value | Redis, Memcached, DynamoDB | 캐시, 세션, 단순 조회 |
  | 도큐먼트 | JSON/BSON 문서 | MongoDB, CouchDB, DocumentDB | 콘텐츠, 계층적 데이터 |
  | 칼럼패밀리 | 행키→컬럼족→컬럼 | Cassandra, HBase, Bigtable | 시계열, 대용량 쓰기 |
  | 그래프 | 노드-간선-속성 | Neo4j, JanusGraph, Amazon Neptune | 관계 중심, 소셜, 추천 |
- [MongoDB](nosql/mongodb.md) - 도큐먼트 데이터베이스
  - **BSON(Binary JSON)**: JSON 확장, 이진 인코딩, 추가 타입(Date, ObjectId, Binary)
  - **컬렉션(Collection)**: 테이블 대응, 스키마리스(Schemaless), 도큐먼트 집합
  - **CRUD**: db.collection.insertOne/find/updateMany/deleteOne
  - **집계 파이프라인(Aggregation Pipeline)**: $match→$group→$project→$sort
    - 예: `db.orders.aggregate([{$match: {status: "A"}}, {$group: {_id: "$cust_id", total: {$sum: "$amount"}}}])`
  - **인덱스**: 단일, 복합, 텍스트, 지리공간(Geospatial), TTL
  - **샤딩**: Config Server + mongos(라우터) + Shard(데이터 노드)
  - **레플리카셋(Replica Set)**: Primary(쓰기) + Secondary(읽기 복제) + Arbiter(투표만)
  - **트랜잭션**: 4.0+ 다중 도큐먼트 ACID 트랜잭션 지원
  - **Atlas**: MongoDB 클라우드 서비스, 관리형
- [Redis](nosql/redis.md) - 인메모리 키-값 데이터 스토어
  - **자료구조 5종**: String(문자열), List(양방향 연결리스트), Hash(해시테이블), Set(집합), Sorted Set(ZSet, 스코어 순서)
  - **고급 기능**:
    - Pub/Sub: 발행-구독 메시징
    - Streams: 로그 구조 메시지 스트림
    - Geo: 지리적 위치 명령
    - HyperLogLog: 카디날리티 추정 (근사)
    - Bitmap/Bitfield: 비트 수준 연산
  - **영속성**:
    - RDB(스냅샷): 주기적 전체 덤프, 빠른 복구, 데이터 손실 가능
    - AOF(Append Only File): 모든 쓰기 명령 로그, 데이터 안전, 파일 크기↑
    - 하이브리드: RDB+AOF 조합
  - **복제**: Master-Replica, 읽기 분산
  - **클러스터**: 16384슬롯 분산, 샤딩, 고가용성
  - **Lua 스크립팅**: 원자적 실행, 복잡한 연산
  - **사례**: 세션 저장소, 캐시, 리더보드, Rate Limiter, 메시지 큐
- [Cassandra](nosql/nosql_overview.md) - 분산 칼럼패밀리 DB
  - **링 아키텍처(Ring)**: P2P, 모든 노드 동등, 마스터 없음
  - **파티셔닝**: `partition_key = hash(key) % num_tokens`
  - **복제 팩터(Replication Factor)**: RF=N→N개 노드에 복제
  - **일관성 레벨(Consistency Level)**: ONE, QUORUM, ALL
    - 읽기/쓰기마다 선택: `CL=QUORUM` → 과반수 노드 확인
  - **CQL(Cassandra Query Language)**: SQL 유사 쿼리 언어
  - **특징**: 최종 일관성, 쓰기 최적화, 선형 확장, SPOF 없음
  - **제약**: 조인 미지원, 파티션 키 설계 중요
- [HBase](nosql/nosql_overview.md) - Hadoop 기반 칼럼 스토어
  - **HDFS 위 구동**: Hadoop 분산 파일 시스템 활용
  - **데이터 모델**: RowKey→Column Family→Column→Timestamp→Value
  - **영역(Region)**: 테이블 수평 분할 단위, RegionServer 관리
  - **일관성**: 행 수준 강한 일관성
  - **용도**: 대용량 실시간 읽기/쓰기, 시계열 데이터, 로그 분석
- [Neo4j](nosql/nosql_overview.md) - 그래프 데이터베이스
  - **요소**: 노드(Node)→엔티티, 관계(Relationship)→간선, 속성(Property)→키-값
  - **라벨(Label)**: 노드 그룹화, 인덱싱
  - **Cypher 쿼리**: `MATCH (p:Person)-[:KNOWS]->(f) WHERE p.name = 'Kim' RETURN f`
  - **패턴 매칭**: 그래프 순회, 경로 탐색, 최단 경로
  - **인덱스**: 라벨+속성 조합, 제약조건(UNIQUE, EXISTS)
  - **장점**: 관계 쿼리 O(1)~O(depth), 조인 없이 깊은 탐색
  - **용도**: 소셜 네트워크, 추천, 사기 탐지, 지식 그래프
- [Elasticsearch](nosql/nosql_overview.md) - 분산 검색/분석 엔진
  - **역색인(Inverted Index)**: 토큰→문서ID 리스트 매핑, 전문 검색
  - **인덱스(Index)**: 문서 컬렉션, 샤드로 분할
  - **매핑(Mapping)**: 스키마 정의, 필드 타입(text, keyword, date, geo_point)
  - **분석기(Analyzer)**: Character Filter→Tokenizer→Token Filter
  - **쿼리 DSL**: match, term, bool, range, agg(집계)
  - **집계(Aggregation)**: 버킷(terms, histogram), 메트릭(avg, sum, cardinality)
  - **ELK Stack**: Elasticsearch + Logstash(수집) + Kibana(시각화)
  - **용도**: 로그 분석, 전문 검색, 모니터링, 보안 분석
- [NewSQL](newsql_architecture.md) - RDBMS 일관성 + NoSQL 확장성
  - **HTAP(Hybrid Transactional/Analytical Processing)**: OLTP+OLAP 통합
  - **특징**: ACID 트랜잭션, 수평 확장, 분산 쿼리, SQL 지원
  - **제품**:
    - **Google Spanner**: TrueTime API(GPS+원자시계), 외부 일관성, 글로벌 분산
    - **TiDB**: MySQL 호환, Raft 합의, TiKV(스토리지), HTAP(TiFlash)
    - **CockroachDB**: PostgreSQL 호환, Raft, 강한 일관성, 자동 복구
    - **YugabyteDB**: PostgreSQL/Cassandra 호환, 분산 ACID
  - **아키텍처**: SQL Layer + Distributed Storage Layer
- [데이터 웨어하우스(Data Warehouse)](data_warehouse.md) - 분석 중앙 저장소
  - **특성(4가지)**: 주제지향(Subject-Oriented), 통합(Integrated), 시계열(Time-Variant), 비휘발성(Non-Volatile)
  - **스키마**:
    - **Star Schema**: 팩트(측정값) + 차원(속성), 단순 조인, 쿼리 빠름
    - **Snowflake Schema**: 차원 정규화, 저장 공간↓, 조인 복잡
    - **Fact Constellation**: 다수 팩트 테이블 공유 차원
  - **용어**:
    - 팩트(Fact): 측정값(매출, 수량), 수치
    - 차원(Dimension): 분석 기준(시간, 지역, 제품), 속성
    - 계층(Hierarchy): 차원 내 계층 구조 (년→분기→월→일)
  - **제품**: Snowflake, Amazon Redshift, Google BigQuery, Azure Synapse
- [OLAP 연산](data_warehouse.md) - 다차원 분석
  - **Drill-Down**: 상세 데이터 탐색 (년→월→일)
  - **Roll-Up**: 요약 데이터 집계 (일→월→년)
  - **Slice**: 한 차원 값 고정 (2024년만)
  - **Dice**: 다차원 부분집합 (2024년, 서울, 제품A)
  - **Pivot(rotate)**: 차원 축 회전, 관점 변경
- [ETL/ELT](data_warehouse.md) - 데이터 적재 방식
  - **ETL**: 추출(Extract)→변환(Transform)→적재(Load), 전통적, DW 적재 전 변환
  - **ELT**: 추출→적재→변환, 클라우드 DW(Snowflake, BigQuery), 적재 후 DW 내 변환
  - **도구**: Informatica, Talend, Apache Airflow, dbt, Fivetran
- [데이터 마이닝(Data Mining)](data_mining.md) - 패턴 발견 기법
  - **분류(Classification)**: 의사결정트리, 나이브 베이즈, SVM, 신경망 → 라벨 예측
  - **회귀(Regression)**: 선형/로지스틱/다항 → 수치 예측
  - **군집(Clustering)**: K-Means, DBSCAN, 계층적 → 그룹화
  - **연관 규칙(Association Rule)**: Apriori, FP-Growth → X→Y (지지도, 신뢰도, 향상도)
    - **지지도(Support)**: P(X∩Y) = (X∩Y 발생 수) / 전체
    - **신뢰도(Confidence)**: P(Y|X) = P(X∩Y) / P(X)
    - **향상도(Lift)**: P(Y|X) / P(Y) > 1이면 연관 있음
  - **이상 탐지(Anomaly Detection)**: Isolation Forest, One-Class SVM, LOF
- [레이크하우스(Lakehouse)](data_mesh_lakehouse.md) - 레이크+웨어하우스 융합
  - **데이터 레이크**: 원시 데이터 저장, 스키마 온 리드, 비정형, 저비용 (S3, ADLS)
  - **웨어하우스**: 정형 데이터, 스키마 온 라이트, 고비용, 고성능 SQL
  - **레이크하우스**: 레이크 위 메타데이터 레이어 + 트랜잭션 지원
  - **기술**:
    - **Delta Lake**: ACID 트랜잭션, 스키마 강제, 시간 여행, Databricks
    - **Apache Iceberg**: 오픈 테이블 포맷, 스키마 진화, 파티션 진화, Netflix
    - **Apache Hudi**: 증분 처리, Upsert, CDC(Change Data Capture), Uber
- [데이터 메시(Data Mesh)](data_mesh_lakehouse.md) - 탈중앙화 데이터 아키텍처
  - **4원칙 (Zhamak Dehghani)**:
    1. 도메인 지향 소유권(Domain Ownership): 데이터는 비즈니스 도메인이 소유
    2. 데이터 제품(Data as a Product): 데이터를 제품처럼 관리 (품질, 문서, SLA)
    3. 셀프서비스 데이터 플랫폼(Self-Service Platform): 인프라 자동화
    4. 연합 거버넌스(Federated Governance): 표준화+자율성 균형
  - **vs 중앙 집중형**: 단일 DW 팀 병목 → 도메인별 데이터 팀
- [벡터 데이터베이스](nosql/nosql_overview.md) - AI 임베딩 저장·검색
  - **용도**: RAG, 시맨틱 검색, 추천, 유사 이미지 검색
  - **임베딩(Embedding)**: 텍스트/이미지→고차원 벡터 (768~1536차원)
  - **유사도 측정**: 코사인 유사도, 유클리드 거리, 내적
  - **ANN(Approximate Nearest Neighbor)**: 근사 최근접 이웃, 정확도 일부 희생→속도↑
    - HNSW(Hierarchical Navigable Small World): 그래프 기반, 빠른 검색
    - IVF(Inverted File Index): 클러스터링 후 검색
    - PQ(Product Quantization): 벡터 양자화, 압축
  - **제품**: Pinecone, Weaviate, ChromaDB, Milvus, Qdrant, pgvector(PostgreSQL)
- [시계열 데이터베이스(TSDB)](nosql/nosql_overview.md) - 시계열 데이터 최적화
  - **특성**: 높은 쓰기 처리량, 시간 기반 쿼리, 다운샘플링, 리텐션
  - **압축**: 시간 근접성 활용, Delta-of-Delta, XOR 압축 (Gorilla)
  - **제품**:
    - **InfluxDB**: Flux 쿼리 언어, TSM(저장 포맷), Telegraf(수집)
    - **TimescaleDB**: PostgreSQL 확장, 하이퍼테이블, SQL 호환
    - **Prometheus**: Pull 기반 메트릭 수집, PromQL, Alertmanager
  - **용도**: IoT 센서, 모니터링, 금융 데이터, 로그
- [인메모리 DB](nosql/nosql_overview.md) - 메모리 상주 데이터베이스
  - **특징**: 디스크 I/O 없음, 마이크로초 지연, 휘발성(영속성 옵션)
  - **제품**: SAP HANA(HTAP), VoltDB(OLTP, ACID), Redis, Memcached
  - **용도**: 실시간 분석, 고빈도 거래(HFT), 캐싱, 세션

### 데이터 품질 / 거버넌스
- [데이터 품질](data_warehouse.md) - 정확성/완전성/일관성/최신성/유일성, 데이터 프로파일링
- [마스터 데이터 관리(MDM)](data_warehouse.md) - 단일 진실 소스(Single Source of Truth)
- [데이터 카탈로그](data_warehouse.md) - 메타데이터 관리, 데이터 계보(Lineage), 데이터 탐색
- [데이터 보안](dbms.md) - TDE(투명한 데이터 암호화), 컬럼 암호화, 데이터 마스킹
- [개인정보 DB 처리](dbms.md) - 익명화/가명화, GDPR/개인정보 보호법 준수, 동의 관리

### 최신 DB 트렌드
- [Serverless DB](newsql_architecture.md) - Aurora Serverless, DynamoDB On-Demand, 자동 스케일링, 사용량 기반 과금
- [Multi-Model DB](nosql/nosql_overview.md) - ArangoDB(문서+그래프), Cosmos DB(다중 API), 단일 DB로 다중 데이터 모델
- [Graph RAG](nosql/nosql_overview.md) - 그래프 DB + LLM, 구조화 지식 활용, Neo4j + GPT
- [Real-time Analytics](data_warehouse.md) - Apache Druid, ClickHouse, OLAP+OLTP 융합, 서브초 쿼리
- [Data Virtualization](data_mesh_lakehouse.md) - Denodo, Dremio, 물리적 이동 없는 논리적 통합, 데이터 페브릭
