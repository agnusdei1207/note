+++
title = "96. K8s Sealed Secrets - GitOps 시크릿 암호화 관리"
date = "2026-03-04"
weight = 96
[extra]
categories = ["studynote-devops-sre", "cicd-gitops"]
+++

## 핵심 인사이트 (3줄 요약)
- **GitOps 보안 딜레마 해결**: GitOps 환경에서는 모든 선언적 YAML을 Git에 올려야 하나, DB 비밀번호 등 민감한 K8s Secret은 평문으로 커밋할 수 없는 취약점을 단방향 비대칭키 암호화로 타파하는 솔루션입니다.
- **Sealed Secrets 원리**: 개발자는 로컬에서 `kubeseal` CLI로 퍼블릭 키를 이용해 평문을 암호화(Sealed)하여 Git에 푸시하고, 쿠버네티스 클러스터 내부의 컨트롤러만 프라이빗 키로 이를 복호화합니다.
- **보안 중심의 파이프라인**: 인프라 코드와 시크릿 코드를 동일한 Git 저장소에서 중앙 집중식 버전으로 관리하면서도 자격 증명 유출 리스크를 완전히 차단하는 DevSecOps의 핵심 요소입니다.

### Ⅰ. 개요 (Context & Background)
현대의 지속적 배포 아키텍처는 ArgoCD나 Flux와 같은 풀 기반(Pull-based)의 GitOps 방식을 채택하고 있습니다. 그러나 GitOps 원칙에 따르면 쿠버네티스의 모든 상태 정보가 Git 레포지토리에 선언되어야 하는데, Kubernetes의 기본 `Secret` 리소스는 단순 Base64 인코딩일 뿐 암호화되지 않습니다.
비밀번호나 API 키를 Git에 올리는 것은 치명적 보안 위반입니다. Bitnami에서 개발한 **Sealed Secrets**은 비대칭 암호화 기술을 이용해 누구나 암호화할 수 있지만 오직 클러스터만이 해독할 수 있는 K8s 커스텀 리소스(CRD)를 제공하여 이 모순을 완벽하게 해결했습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

Sealed Secrets는 클러스터 내부에 상주하는 컨트롤러와 로컬 클라이언트 유틸리티(`kubeseal`)로 구성됩니다.

```text
+-------------------+        +-------------------+        +-------------------+
| Developer         | -----> | Git Repository    | -----> | Kubernetes Cluster|
| (개발자)          | kubeseal (Git 저장소)      | ArgoCD | (쿠버네티스)      |
| Cleartext Secret  | Encrypt| SealedSecret      | Sync   | SealedSecret      |
| (평문 시크릿)     | -----> | (암호화된 시크릿) | -----> | Controller        |
+-------------------+        +-------------------+        | Decrypts to Secret|
                                                          | (시크릿으로 복호화)|
                                                          +-------------------+
```

1. **비대칭 키 생성**: Sealed Secrets Controller가 클러스터 내에 배포될 때 RSA 퍼블릭 키와 프라이빗 키 쌍을 자동 생성합니다.
2. **암호화 (Encryption)**: 개발자는 `kubeseal` 툴을 사용해 K8s 클러스터에서 퍼블릭 키를 가져오고, 로컬의 평문 Secret YAML 파일을 `SealedSecret` 커스텀 리소스로 단방향 암호화합니다.
3. **배포 및 복호화 (Decryption)**: 암호화된 코드를 Git에 푸시하면, ArgoCD가 K8s에 반영합니다. K8s 내부의 Controller는 자신이 보유한 프라이빗 키를 사용해 이를 원본 `Secret` 리소스로 복호화하여 K8s에 생성합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구분 | K8s Sealed Secrets | HashiCorp Vault (External) | AWS Secrets Manager (CSI) |
| :--- | :--- | :--- | :--- |
| **아키텍처 개념** | 암호화된 시크릿 자체를 Git에 보관 (GitOps 친화적) | 중앙 집중형 전용 외부 시크릿 보관 서버 운영 | 클라우드 벤더 종속적 KMS 보관 서비스 연동 |
| **운영 오버헤드** | K8s 컨트롤러 하나만 띄우면 되어 매우 낮음 | 별도의 고가용성 Vault 서버 운영 및 관리 부하 큼 | AWS IAM OIDC (IRSA) 권한 연동 및 정책 관리 필요 |
| **보안 동적 제어** | 정적인 시크릿 암호화에 특화 (동적 갱신 한계) | TTL 기반 동적 시크릿 발급, 일회용 자격증명 우수 | 비밀번호 자동 로테이션(Rotation) 기능 강력 지원 |
| **적용 권장 환경** | 소/중규모 클러스터 및 완전한 GitOps 추구 조직 | 엔터프라이즈 대규모 멀티 클러스터 공통 관리 환경 | AWS 네이티브 인프라 100% 종속 및 통제 환경 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **재해 복구(DR) 리스크**: Sealed Secrets의 치명적 리스크는 컨트롤러가 가진 '프라이빗 키(마스터 키)' 자체를 백업하지 않으면, 클러스터 파괴 시 Git에 있는 모든 시크릿 코드가 영구적 쓰레기 데이터가 된다는 점입니다. 따라서 초기 프라이빗 키 도출 후 오프라인 금고 등에 안전하게 백업(Disaster Recovery)하는 정책 수립이 선행되어야 합니다.
- **아키텍트 전략**: 서비스 규모가 커져 토큰의 실시간 동적 발급이나 멀티 클라우드 간 시크릿 공유가 필요해지면 Vault + External Secrets Operator 패턴으로 고도화 마이그레이션하는 하이브리드 전략을 취해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
Sealed Secrets는 인프라스트럭처 애즈 코드(IaC)의 완전성을 보장하며 개발자가 로컬 비밀번호를 안전하게 취급할 수 있는 심리적 안전감을 부여합니다. GitOps가 쿠버네티스 생태계의 절대적 배포 표준으로 굳건해짐에 따라, 시크릿 매니지먼트의 가장 접근성 높고 직관적인 데브섹옵스(DevSecOps) 베스트 프랙티스로 자리잡고 있습니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **선행 개념**: 쿠버네티스 Secret, 공개키 암호화(RSA), GitOps
- **핵심 기술**: Sealed Secrets, kubeseal, ArgoCD
- **확장 및 응용**: HashiCorp Vault, External Secrets Operator, DevSecOps

### 👶 어린이를 위한 3줄 비유 설명
1. 여러분의 비밀 일기장을 누구나 볼 수 있는 칠판(Git)에 붙여놔야 하는 규칙이 생겼어요.
2. 하지만 여러분은 '특수 자물쇠 상자(Sealed Secrets)' 안에 일기를 넣고 잠가서 칠판에 붙인답니다.
3. 이 상자는 오직 교장 선생님(쿠버네티스)이 가진 단 하나의 마법 열쇠로만 열 수 있어서 해커들이 절대 볼 수 없어요!