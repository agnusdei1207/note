+++
weight = 670
title = "670. 컨테이너 보안 (Container Security)"
date = "2026-03-16"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "컨테이너 보안", "Container Security", "Docker 보안", "Kubernetes 보안", "Rootless"]
+++

# 컨테이너 보안 (Container Security)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 컨테이너 보안은 **"VM보다 격리가 약하다"**는 점을 보완하기 위해 **최소 권한, 이미지 스캔, 런타임 보안**을 제공하는 분야다.
> 2. **가치**: "컨테이너는 같은 커널 공유 → 보다 취약"하므로, **Root 사용 방지, 불필요한 능력 제거, Seccomp/AppArmor** 등 다층 방어가 필요하다.
> 3. **융합**:**CIS Benchmarks**, **Pod Security Policy(K8s)**, **Rootless Containers**, **Confidential Containers(암호화된 Pod)**가 표준 보안 기술이다.

---

## Ⅰ. 컨테이너 보안의 개요

### 1. 정의
- 컨테이너 보안은 **Docker, Kubernetes 등 컨테이너 환경**의 보안 위협을 완화하는 기술이다.

### 2. 등장 배경
- 컨테이너 널리 보급 → 새로운 공격 표면

### 3. 💡 비유: '아파트 복도'
- 컨테이너는 **"아파트 복도에 있는 세대"**와 같다.
- 내벽은 얇지만(프로세스 격리), 보안 경비(보안 기술)가 필요하다.

---

## Ⅱ. 컨테이너 보안 위협 (Deep Dive)

### 1. 주요 위협
| 위협 | 설명 |
|:---|:---|
| **Container Escape** | 컨테이너에서 호스트로 탈출 |
| **Image Vulnerabilities** | 취약한 베이스 이미지 |
| **Secrets Leakage** | 환경 변수, Dockerfile에 비밀 |
| **Supply Chain** | 악성 이미지 공급 |
| **Runtime Attack** | 실행 중 공격 |

### 2. Kernel 공유
- 모든 컨테이너가 **동일 커널** 사용 → 커널 취약점 공유

---

## Ⅲ. 보안 강화 기법

### 1. 이미지 보안
```dockerfile
# Base 이미지 최소화
FROM alpine:3.18

# 비root 사용자
RUN adduser -D appuser
USER appuser

# 취약 패키지 제거
RUN apk del --purge build-dependencies

# 스캔
# trivy image myapp:latest
```

### 2. 런타임 보안
```yaml
# Kubernetes Pod Security Context
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
    add:
      - NET_BIND_SERVICE
  seccompProfile:
    type: RuntimeDefault
```

### 3. Rootless 컨테이너
```bash
# Rootless Docker
dockerd-rootless-setuptool install
```

---

## Ⅳ. 네트워크 보안

### 1. Network Policy
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

---

## Ⅴ. 실무 적용

### 1. CIS Benchmark
- Kubernetes/Docker 보안 체크리스트

### 2. 도구
- **Trivy**: 이미지 스캔
- **Falco**: 런타임 보안
- **Kube-bench**: K8s 설정 검사
- **OPA Gatekeeper**: 정책 강제

---

## Ⅵ. 기대효과 및 결론

### 1. 정량/정성 기대효과
- **공격 표면 감소**

---

## Ⅶ. 미래 전망

### 1. Confidential Containers
- AMD SEV, Intel TDX로 암호화된 컨테이너

---

## 📌 관련 개념 맵
- **[컨테이너](./642_container.md)**: 기반 기술
- **[Kubernetes](./645_kubernetes.md)**: 보안 정책
- **[SELinux](./651_selinux.md)**: MAC

---

## 👶 어린이를 위한 3줄 비유 설명
1. 컨테이너 보안은 **"얇은 벽을 가진 방을 보호하는 장치"** 같아요.
2. 벽이 얇으니까(CPU 공유), 경비원을 여러 명 세워두죠.
3. CCTV(모니터링), 문단속(네트워크 정책), 금고(암호화)를 해서 안전하게 지켜요!
