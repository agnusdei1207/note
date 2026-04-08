+++
title = "Nginx + Let's Encrypt 환경에서 TLS 설정 삽질 정리"
+++

# Nginx + Let's Encrypt 환경에서 TLS 설정 삽질 정리

> **tl;dr** — TLS 에러의 90%는 인증서 문제가 아니라, Nginx가 어떤 server block을 먼저 선택하느냐의 문제다.

---

## 배경: 서비스 구조

```
인터넷 → [4번 서버: Nginx Gateway] → [5번 서버: Nginx + Container]
```

관리해야 할 도메인:

| 도메인 | 용도 |
|---|---|
| example.kr | 메인 |
| example.com | 메인 |
| admin.example.kr | 관리자 |
| admin.example.com | 관리자 |

외부 트래픽은 4번 서버에서 수신하고, 5번 서버의 컨테이너가 실제 서비스를 처리하는 구조다. 이 상태에서 Let's Encrypt 인증서를 발급받고 적용했더니 — **일부 도메인에서 TLS가 깨진다.**

---

## 문제 현상

- 특정 도메인 접속 시 브라우저 경고
- 다른 도메인의 인증서가 내려오는 상황 발생
- certbot 로그에는 이상 없음

---

## 핵심 원인 3가지

### 1. `server_name`과 `ssl_certificate` 매칭 오류

Nginx는 HTTP 요청의 `Host` 헤더를 기반으로 server block을 선택한다. 문제는 설정 파일 안에서 **인증서와 server_name이 1:1로 묶여야 한다는 사실을 놓치는 것**이다.

**잘못된 설정:**

```nginx
server {
    server_name admin.example.kr admin.example.com;
    ssl_certificate /etc/letsencrypt/kr_fullchain.pem;  # kr 인증서
}
```

.COM 도메인으로 요청이 들어와도, 이 server block이 잡히면 **.kr 인증서가 내려간다.** 브라우저에 따라 경고가 뜨거나, 일부 브라우저는 무시해버린다.

### 2. 인증서 SAN 범위 이해 부족

Let's Encrypt 멀티도메인 인증서 내부에는 Subject Alternative Name(SAN)이 있다.

```
DNS: admin.example.kr
DNS: example.kr
```

이 인증서로 가능한 것:

| 도메인 | 가능 여부 |
|---|---|
| example.kr | ✅ |
| admin.example.kr | ✅ |
| example.com | ❌ |
| admin.example.com | ❌ |

**SAN에 없으면, 해당 도메인에서는 인증서가 절대 동작하지 않는다.** 인증서 파일 명목상으로 여러 도메인을 커버할 수 있다고 생각하기 쉬운데, 실제로는 반드시 SAN에 포함되어 있어야 한다.

### 3. Reverse Proxy 환경에서의 certbot 동작

Let's Encrypt 인증 방식 비교:

| 방식 | 요구 조건 |
|---|---|
| HTTP-01 | 외부 80포트 → 해당 서버 직접 접근 가능 |
| DNS-01 | DNS TXT 레코드 설정 |

현재 구조(`인터넷 → 4번 → 5번`)에서는 5번 서버에서 직접 80포트에 응답할 수 없으므로, HTTP-01 방식으로 `--nginx` 플러그인을 실행하면 **실패할 가능성이 높다.**

---

## 해결 전략

### 전략 1. DNS-01 방식으로 인증서 발급 (권장)

```bash
certbot certonly --manual --preferred-challenges dns \
  -d example.kr -d admin.example.kr
```

> **오타 주의:** `--preferred-challenges`를 `--preferred-challenages`(eccc 누락)로 잘못 쓰는 경우가 많다. 옵션 이름은 반드시 `challenges`로 올바로 써야 한다.

**각 옵션의 의미:**

| 옵션 | 의미 |
|---|---|
| `certbot` | Let's Encrypt CA와 통신해 인증서를 발급·갱신하는 클라이언트 |
| `certonly` | 인증서 파일만 발급, 웹서버 설정은 자동 수정하지 않음 (`--nginx`, `--apache`와 대비) |
| `--manual` | 수동 플러그인 사용 — 챌린지 응답을 사용자가 직접 수행 |
| `--preferred-challenges dns` | DNS-01 챌린지를 우선 사용 (http와 dns를 동시에 지정하면 `http,dns`처럼 쉼표로 연결) |
| `-d <도메인>` | 인증서에 포함할 도메인, 여러 번 지정 가능 |

**DNS-01 챌린지 동작 흐름:**

```
1. Certbot이 example.kr 인증서 요청
2. Let's Encrypt가 도메인 소유권 검증값을 회신
3. Certbot이 다음과 같이 안내:
   "Please deploy a DNS TXT record under the name:
    _acme-challenge.example.kr
    with the following value:
    [랜덤값]"
4. 사용자가 DNS 콘솔에서 TXT 레코드 추가
5. 전파 완료 후 Enter를 눌러 Let's Encrypt가 TXT 레코드 조회
6. 검증 완료 → 인증서 발급
```

**TXT 레코드 등록 예시 (DNS 관리 콘솔):**

```
类型: TXT
名称: _acme-challenge
内容: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TTL:  300
```

**왜 이 방식이 유용한가:**
- 포트 80이 열려 있지 않아도 OK
- 게이트웨이 서버가 앞에 있어도 OK — 서버 경로가 아니라 DNS 제어권으로 검증하기 때문
- 와일드카드 인증서 발급에 필수 (Let's Encrypt FAQ에서 명시)

**단점 — 자동 갱신 불가:**
`--manual` 방식은 `--manual-auth-hook` 스크립트를 함께 쓰지 않으면 자동 갱신을 지원하지 않는다. Let's Encrypt 인증서 만료는 90일이므로, 만기 전 동일한 명령을 수동으로 재실행해야 한다. **장기 운영용이 아니다.**

**자동화 가능한 구조 (훅 스크립트 사용):**

```bash
certbot certonly --manual --preferred-challenges dns \
  --manual-auth-hook /path/to/auth.sh \
  --manual-cleanup-hook /path/to/cleanup.sh \
  -d example.kr -d admin.example.kr
```

| 옵션 | 의미 |
|---|---|
| `--manual-auth-hook` | 챌린지 직전에 실행할 스크립트 (TXT 레코드 생성·삽입 자동화) |
| `--manual-cleanup-hook` | 챌린지 종료 후 실행할 스크립트 (TXT 레코드 정리 자동화) |

DNS 제공자가 API를 제공하면 이 두 훅을 통해 TXT 레코드 생성과 정리를 자동화할 수 있어, 자동 갱신까지 연결 가능하다. DNS API 플러그인이 있다면 그것을 쓰는 쪽이 더 깔끔하다.

**한 줄 요약:**

```
"웹서버 설정은 건드리지 말고, 내가 DNS TXT 레코드를 직접 추가할 테니,
 DNS 방식으로 도메인 소유권을 검증해서 인증서만 발급해줘."
```

**도메인 그룹 주의:** `-d`로 여러 도메인을 나열하면 모든 도메인이 **하나의 SAN 인증서**에 포함된다. kr 도메인과 com 도메인을 한 번에 지정하면 두 TLD가 섞인 인증서가 발급되어 이후 매칭 문제를 야기할 수 있다. **도메인 그룹(TLD)별로 각각 발급하는 것을 권장한다.**

---

### 전략 2. server block을 도메인마다 분리

**잘못된 구조:**

```nginx
server {
    server_name admin.example.kr admin.example.com;
    ssl_certificate kr_fullchain.pem;  # 둘 다 kr 인증서 사용
}
```

**올바른 구조:**

```nginx
server {
    server_name admin.example.kr;
    ssl_certificate /etc/letsencrypt/kr_fullchain.pem;
}

server {
    server_name admin.example.com;
    ssl_certificate /etc/letsencrypt/com_fullchain.pem;
}
```

**핵심 원칙:** 하나의 `server` 블록에는 하나의 `ssl_certificate`만 둔다.

### 전략 3. 도메인과 인증서 1:1 매핑

| 도메인 | 인증서 |
|---|---|
| example.kr | kr 인증서 |
| admin.example.kr | kr 인증서 |
| example.com | com 인증서 |
| admin.example.com | com 인증서 |

같은 TLD의 도메인끼리(kr ↔ kr)라면 하나의 인증서를 공유해도 된다. 단, 반드시 **해당 도메인들이 SAN에 모두 포함되어 있어야 한다.**

---

## 디버깅 방법

### 1. 인증서 내부 SAN 확인

```bash
openssl x509 -in fullchain.pem -noout -text | grep -A1 "Subject Alternative Name"
```

**명령어 분해:**

| 명령어 부분 | 역할 |
|---|---|
| `openssl x509` | X.509 인증서(.pem)를 다루는 도구 |
| `-in fullchain.pem` | 입력 파일 지정 (인증서 경로) |
| `-noout` | 출력에서 불필요部分(certificate 자체)을 제거 |
| `-text` | 인증서 내용을 사람이 읽을 수 있는 텍스트로 출력 |
| `\| grep -A1 "Subject Alternative Name"` | 출력 중 SAN section 1줄 포함해서 표시 |

**실제 출력 예시:**

```
Subject Alternative Name:
    DNS:example.kr, DNS:admin.example.kr
```

이 출력은 **이 인증서가 어떤 도메인들에 대해 유효한지를** 보여준다. 이 목록에 없는 도메인에 이 인증서를 적용하면 TLS mismatch가 발생한다.

---

### 2. 실제로 서비스되는 인증서 확인 (가장 중요)

```bash
openssl s_client -connect domain:443 -servername domain \
  | openssl x509 -noout -issuer -dates -ext subjectAltName
```

**명령어 분해:**

`openssl s_client` 부분:

| 옵션 | 의미 |
|---|---|
| `-connect domain:443` | 대상 서버의 443포트에 TCP 연결 |
| `-servername domain` | TLS SNI(Server Name Indication)에 도메인을 명시 — **이 값이 Nginx server_name 매칭의 기준** |

`openssl x509` 부분:

| 옵션 | 의미 |
|---|---|
| `-noout` | 인증서 본문 출력 방지 |
| `-issuer` | 인증서 발급자 (Let's Encrypt 등) 출력 |
| `-dates` | 인증서 유효 기간(notBefore, notAfter) 출력 |
| `-ext subjectAltName` | SAN 확장 영역만 추출 |

**SNI가关键的인 이유:**

`-servername`을 지정하지 않으면, Nginx는 Host 헤더 기반 fallbacks server block을 선택할 수 있다. **브라우저가 보는 인증서를 정확히 재현하려면 반드시 `-servername`을 지정해야 한다.**

**실제 출력 예시:**

```
issuer=Let's Encrypt
notBefore=Apr  1 00:00:00 2026 GMT
notAfter=Jun 30 23:59:59 2026 GMT
subjectAltName= DNS:example.kr, DNS:admin.example.kr
```

이 명령어로 보는 인증서가 **실제로 Nginx가 해당 도메인 요청에 대해 내보내는 인증서**다. certbot이 발급한 파일과 다를 수 있다 — 이 지점이 삽질의 핵심이다.

**추가 확인 팁:** 인증서 체인 전체를 보려면:

```bash
openssl s_client -connect domain:443 -servername domain -showcerts
```

---

### 3. Nginx server_name 매칭 확인

```bash
grep -R "server_name" /etc/nginx
```

**명령어 분해:**

| 옵션 | 의미 |
|---|---|
| `grep` | 패턴 매칭 검색 |
| `-R` (recursive) | 디렉토리 전체 재귀 탐색 |
| `"server_name"` | 찾을 패턴 |
| `/etc/nginx` | 검색 대상 디렉토리 |

**동작 방식:**

`/etc/nginx` 아래 모든 파일에서 `server_name` 문자열이 포함된 줄을 출력한다. Nginx 설정이 여러 파일로 분할되어 있는 경우(e.g. `/etc/nginx/conf.d/`, `/etc/nginx/sites-enabled/`) 전체에서 한 번에 찾을 수 있다.

**출력 예시:**

```
/etc/nginx/conf.d/example.kr.conf:    server_name example.kr;
/etc/nginx/conf.d/admin.kr.conf:    server_name admin.example.kr;
/etc/nginx/conf.d/example.com.conf:    server_name example.com;
/etc/nginx/conf.d/admin.com.conf:    server_name admin.example.com;
```

**Nginx server block 선택 규칙 (알아두면 좋은 배경):**

1. **exact match** — 정확히 일치하는 server_name 우선
2. **longest prefix match** — 가장 긴 패턴 매칭
3. **default server** — 매칭되는 게 없으면 첫 번째 server block (설정 파일 순서依存)

즉, `server_name admin.example.kr admin.example.com;`이 있는 server block이 파일에서 먼저 등장하면, `admin.example.com` 요청도 이 블록이 먼저 잡힌다. 이게 매칭 오류의 실체다.

---

## 핵심 인사이트

**1. TLS 문제의 90%는 "nginx 매칭 문제"**
인증서가 틀린 게 아니라, Nginx가 잘못된 server block을 먼저 선택하는 경우가 대부분이다.

**2. 인증서는 "파일" 문제가 아니라 "매칭" 문제다**

| 착각 | 실제 |
|---|---|
| "인증서 파일이 잘못됨" | "Nginx가 잘못된 인증서를 선택함" |

**3. SAN에 없는 도메인은 무조건 깨진다**
인증서 하나로 여러 도메인을 커버할 수 있지만, 반드시 SAN에 포함되어야 한다.

**4. Reverse Proxy 환경에서는 DNS 방식이 가장 확실하다**
HTTP 방식은 경로 전달까지 신경 써야 하고, DNS 방식은 서버 구조와 무관하게 동작한다.

**5. manual 방식은 운영용이 아니다**
Let's Encrypt 인증서 만료는 90일. 자동 갱신 없이 manual 방식으로 운영하면 인증서 관리가 곧 병원이 된다.

---

## 올바른 설정 구조 (정리)

```nginx
# === KR 도메인 ===
server {
    listen 80;
    server_name example.kr;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name example.kr;
    ssl_certificate /etc/letsencrypt/live/example.kr/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.kr/privkey.pem;
    proxy_pass http://backend;
}

# === COM 도메인 ===
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name example.com;
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    proxy_pass http://backend;
}

# === Admin KR ===
server {
    listen 80;
    server_name admin.example.kr;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name admin.example.kr;
    ssl_certificate /etc/letsencrypt/live/example.kr/fullchain.pem;  # kr 인증서 공유
    ssl_certificate_key /etc/letsencrypt/live/example.kr/privkey.pem;
    proxy_pass http://backend;
}

# === Admin COM ===
server {
    listen 80;
    server_name admin.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name admin.example.com;
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    proxy_pass http://backend;
}
```

**원칙:**
- 도메인마다 server block 분리
- ssl_certificate는 해당 server_name의 SAN 범위 내 인증서만 지정
- Reverse Proxy 구조라면 **DNS-01 방식으로 발급**

---

## 한 줄 결론

> TLS 문제는 **인증서 문제가 아니라**, **Nginx가 어떤 server block을 선택하느냐**의 문제다.
