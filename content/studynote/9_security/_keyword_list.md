+++
title = "09. 정보보안 키워드 목록"
date = "2026-03-03"
[extra]
categories = "studynote-security"
+++

# 정보보안 (Information Security) 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 보안 전 영역 기술사 수준 핵심 키워드
> ⚡ 기술사 보안 문제는 단순 지식이 아닌 **위협 모델링 → 아키텍처 설계 → 법적·제도적 대응**까지 통합 서술을 요구함

+++

## 1. 정보보안 개론 / 원칙 — 24개

1. 정보보안 3요소 — CIA (기밀성·무결성·가용성) + 인증성·부인방지·책임추적성
2. 기밀성 (Confidentiality) — 암호화, 접근 제어, DRM
3. 무결성 (Integrity) — 해시, 전자서명, MAC, HMAC
4. 가용성 (Availability) — HA 설계, DDoS 방어, SLA
5. 인증성 (Authenticity) — 신원 확인, PKI, 디지털 서명
6. 부인방지 (Non-repudiation) — 전자서명, 타임스탬프, 로그
7. 책임추적성 (Accountability) — 감사 로그, 사용자 행동 기록
8. 보안 원칙 — 최소 권한 / 직무 분리 / 알 필요성 / 심층 방어
9. 심층 방어 (Defense in Depth) — 다층 보안 아키텍처
10. 보안 정책 — 조직 보안 정책, 표준·지침·절차 수립
11. 위험 관리 (Risk Management) — 위험 식별/분석/평가/대응/모니터링
12. 위험 분석 방법 — 정량적 (ALE=ARO×SLE) / 정성적
13. ALE / ARO / SLE — Annual Loss Expectancy 계산
14. 잔여 위험 (Residual Risk) — 대응 후 남은 위험
15. 위험 대응 전략 — 회피 / 전가 / 완화 / 수용
16. 보안 아키텍처 — Zachman / SABSA / OSA
17. SABSA (Sherwood Applied Business Security Architecture)
18. 제로 트러스트 (Zero Trust) — "절대 신뢰하지 말고 항상 검증하라", NIST SP 800-207
19. 마이크로 세그멘테이션 (Micro-segmentation) — 측면 이동 차단
20. 보안 통제 유형 — 예방/탐지/교정/복구/억제
21. 관리적/기술적/물리적 보안 통제
22. 게이트웨이 모델 vs 제로 트러스트 모델 비교
23. 내재적 보안 (Security by Design) vs 사후 보안 (Bolt-on Security)
24. 개인정보 중심 설계 (Privacy by Design) — ISO 31700

+++

## 2. 암호학 심화 — 32개

25. 대칭키 암호 (Symmetric Encryption) — 기밀성, 빠름, 키 배분 문제
26. AES (Advanced Encryption Standard) — 128/192/256비트, Rijndael, SPN 구조
27. AES 운영 모드 — ECB / CBC / CFB / OFB / CTR / GCM
28. GCM (Galois/Counter Mode) — 인증 암호화 (AEAD)
29. DES (Data Encryption Standard) — 56비트, 취약, 구식
30. 3DES (Triple DES) — 112/168비트, 레거시 시스템
31. ChaCha20-Poly1305 — AEAD, TLS 1.3 대안 스위트
32. 비대칭키 암호 (Asymmetric Encryption) — 키 배분 해결, 느림
33. RSA — 소인수분해 어려움, PKCS#1 v2.2, OAEP
34. ECC (Elliptic Curve Cryptography) — 더 짧은 키, 동등 강도
35. ECDSA (Elliptic Curve Digital Signature Algorithm) — secp256k1, P-256
36. EdDSA / Ed25519 — 빠른 서명, 결정론적
37. DH (Diffie-Hellman) — 키 교환, 이산 로그 기반
38. ECDH (Elliptic Curve DH) — 효율적 키 교환
39. 해시 함수 (Hash Function) — 단방향, 충돌 저항성
40. SHA-2 (SHA-256/384/512)
41. SHA-3 (Keccak) — NIST 2015 표준
42. BLAKE2 / BLAKE3 — 빠른 해시
43. MD5 / SHA-1 — 취약, 사용 금지
44. MAC (Message Authentication Code) — 무결성+인증
45. HMAC (Hash-based MAC) — HMAC-SHA256
46. CMAC (Cipher-based MAC)
47. 디지털 서명 (Digital Signature) — 인증+무결성+부인방지
48. RSA-PSS — 확률적 서명, 안전한 RSA 서명
49. 키 유도 함수 (KDF) — PBKDF2 / bcrypt / scrypt / Argon2
50. 패스워드 해싱 — Argon2id (NIST 권장), bcrypt
51. 키 관리 (Key Management) — 생성/배포/갱신/폐기
52. HSM (Hardware Security Module) — 키 하드웨어 보호
53. 전방 비밀성 (PFS, Perfect Forward Secrecy) — DHE/ECDHE
54. 양자 내성 암호 (PQC, Post-Quantum Cryptography) — NIST PQC 표준화
55. CRYSTALS-Kyber — NIST PQC 선택 (KEM)
56. CRYSTALS-Dilithium / FALCON / SPHINCS+ — NIST PQC 서명

+++

## 3. 네트워크 보안 심화 — 28개

57. 방화벽 (Firewall) — 패킷 필터 / Stateful Inspection / Proxy / NGFW
58. NGFW (Next-Generation Firewall) — DPI, 앱 인식, 사용자 인식, IPS 통합
59. IDS (Intrusion Detection System) — 오용 탐지 / 이상 탐지
60. IPS (Intrusion Prevention System) — 인라인 차단, 서명 기반/행위 기반
61. WAF (Web Application Firewall) — OWASP Core Rule Set, 가상 패치
62. DDoS 공격 유형 — 볼류메트릭 / 프로토콜 / 애플리케이션 계층
63. DDoS 방어 — Anycast, Scrubbing Center, Rate Limiting, BGP Blackhole
64. DNS 기반 공격 — DNS Spoofing / Cache Poisoning / DNS Amplification / DNSsec
65. ARP 기반 공격 — ARP Spoofing / Gratuitous ARP Poisoning
66. IP 스푸핑 (IP Spoofing) — BCP38, uRPF
67. 세션 하이재킹 (Session Hijacking) — TCP Sequence Number 예측
68. 중간자 공격 (MITM) — SSL Stripping, 공개 WiFi 위협
69. 패킷 스니핑 (Packet Sniffing) — 프로미스큐어스 모드
70. VPN (Virtual Private Network) 기술 비교 — IPsec / SSL / WireGuard / OpenVPN / ZeroTier
71. IPsec 프로토콜 — AH (인증만) / ESP (암호화+인증), IKEv1 vs IKEv2
72. SSL/TLS 취약점 — POODLE / BEAST / CRIME / HEARTBLEED / DROWN
73. TLS 1.3 — 핸드쉐이크 1-RTT, 0-RTT, PFS 필수, 약한 알고리즘 제거
74. 인증서 투명성 (CT, Certificate Transparency) — 감사 로그
75. HSTS (HTTP Strict Transport Security) — 강제 HTTPS
76. CAA (Certification Authority Authorization) DNS 레코드
77. SASE (Secure Access Service Edge) — Gartner, 클라우드 통합 보안
78. ZTNA (Zero Trust Network Access) — SDP, 앱별 터널
79. SD-WAN 보안 — 암호화된 WAN, 중앙 정책 관리
80. 네트워크 접근 제어 (NAC) — IEEE 802.1X, EAP, 포스처 검사
81. DMZ (Demilitarized Zone) 설계 패턴 — 3계층 방화벽
82. 내부 세그멘테이션 방화벽 (ISFW) — East-West 트래픽 통제
83. 네트워크 가시성 — NetFlow / sFlow / IPFIX
84. 딥 패킷 인스펙션 (DPI, Deep Packet Inspection) — 페이로드 분석

+++

## 4. 시스템 / 엔드포인트 보안 — 24개

85. 엔드포인트 보안 — AV / EPP / EDR / XDR
86. EDR (Endpoint Detection and Response) — 행위 기반 탐지, Crowdstrike, SentinelOne
87. XDR (Extended Detection and Response) — 교차 계층 상관 분석
88. 취약점 (Vulnerability) 유형 — 버퍼 오버플로우 / Use-After-Free / Format String
89. 버퍼 오버플로우 방어 — ASLR / NX / Stack Canary / RELRO / PIE
90. ASLR (Address Space Layout Randomization) — 주소 난수화
91. DEP/NX (Data Execution Prevention / No-Execute) — W^X 정책
92. Stack Canary / SSP — 스택 보호 쿠키
93. RELRO (Relocation Read-Only) — GOT/PLT 쓰기 보호
94. PIE (Position-Independent Executable) — ASLR 연동
95. ROP (Return-Oriented Programming) — 가젯 체인, 셸코드 우회
96. CFI (Control Flow Integrity) — 제어 흐름 무결성 검사
97. Heap Spray / Heap Grooming — heap 취약점 공격 기법
98. Use-After-Free (UAF) — 해제 후 재사용 취약점
99. Race Condition — TOCTOU (Time-of-Check-Time-of-Use)
100. 권한 상승 (Privilege Escalation) — 로컬 / 원격, 커널 취약점
101. 루트킷 (Rootkit) — 커널/부트킷/파일시스템, 탐지 회피
102. 부트킷 (Bootkit) — MBR/UEFI 감염, Secure Boot 우회
103. 펌웨어 보안 — UEFI Secure Boot, Measured Boot, TPM 2.0
104. TPM (Trusted Platform Module) — 키 저장, 원격 증명
105. Intel SGX (Software Guard Extensions) — 하드웨어 enclave
106. AMD SEV (Secure Encrypted Virtualization) — 가상머신 메모리 암호화
107. 패치 관리 (Patch Management) — CVSS 점수 기반 우선순위
108. 취약점 관리 프로세스 — 식별/우선순위/패치/검증/보고

+++

## 5. 웹 / 애플리케이션 보안 — 30개

109. OWASP Top 10 (2021) — A01~A10
110. A01. 취약한 접근 제어 (Broken Access Control) — IDOR, 경로 순회
111. A02. 암호화 실패 (Cryptographic Failures) — 하드코딩 키, 약한 TLS
112. A03. 인젝션 (Injection) — SQL / OS Command / LDAP / XPath Injection
113. A04. 안전하지 않은 설계 (Insecure Design) — 위협 모델링 부재
114. A05. 보안 설정 오류 (Security Misconfiguration) — 기본 계정, 불필요 서비스
115. A06. 취약하고 오래된 컴포넌트 (Vulnerable Components) — Log4Shell 사례
116. A07. 식별 및 인증 실패 (Identification/Authentication Failures) — Credential Stuffing
117. A08. 소프트웨어 무결성 실패 (Software Data Integrity Failures) — CI/CD 보안
118. A09. 로깅/모니터링 실패 (Logging/Monitoring Failures)
119. A10. SSRF (Server-Side Request Forgery) — 내부망 프록시 악용
120. SQL 인젝션 — 파라미터화 쿼리, ORM, 입력 검증
121. XSS (Cross-Site Scripting) — 반사형/저장형/DOM 기반, CSP
122. CSRF (Cross-Site Request Forgery) — SameSite 쿠키, CSRF 토큰
123. 클릭재킹 (Clickjacking) — X-Frame-Options, frame-ancestors
124. XXE (XML External Entity) — XML 파서 취약점
125. SSTI (Server-Side Template Injection) — Jinja2, Twig 취약점
126. 경로 순회 (Path Traversal) — ../../etc/passwd
127. 보안 쿠키 — HttpOnly / Secure / SameSite / Expires
128. JWT (JSON Web Token) — alg:none 취약점, 서명 검증 필수
129. OAuth 2.0 취약점 — 오픈 리다이렉트, PKCE 부재
130. API 보안 — OWASP API Security Top 10
131. 인증 방식 비교 — 세션 쿠키 / JWT / API Key / OAuth 2.0 / mTLS
132. GraphQL 보안 — 인트로스펙션, DoS (depth/alias 제한)
133. 컨텐츠 보안 정책 (CSP, Content Security Policy) — XSS 완화
134. 보안 헤더 — X-Content-Type-Options / X-Frame-Options / HSTS / Referrer-Policy
135. CORS (Cross-Origin Resource Sharing) 오설정 — 와일드카드 위험
136. 파일 업로드 보안 — MIME 검증, 이름 변경, 격리 스토리지
137. 역직렬화 취약점 (Insecure Deserialization) — Java/Python/PHP 객체
138. SSRF 심화 — 클라우드 메타데이터 서버 악용 (169.254.169.254)

+++

## 6. 클라우드 보안 — 22개

139. 클라우드 보안 공동 책임 모델 (Shared Responsibility)
140. CSPM (Cloud Security Posture Management) — 잘못된 설정 탐지
141. CWPP (Cloud Workload Protection Platform) — 컨테이너/VM/서버리스
142. CNAPP (Cloud-Native Application Protection Platform) — CSPM+CWPP 통합
143. CIEM (Cloud Infrastructure Entitlement Management) — 최소 권한
144. IAM (Identity and Access Management) — 정책/역할/그룹/조건
145. IAM 취약점 — 과도한 권한, 공개 S3 버킷, 공개 스냅샷
146. 클라우드 스토리지 보안 — 버킷 정책, 암호화 (SSE-S3/SSE-KMS), 버전 관리
147. KMS (Key Management Service) — AWS KMS, Azure Key Vault, GCP Cloud KMS
148. 시크릿 관리 — HashiCorp Vault, AWS Secrets Manager
149. 컨테이너 이미지 보안 — CVE 스캔 (Trivy, Snyk), 최소 베이스 이미지
150. Kubernetes 보안 — RBAC, PodSecurityContext, NetworkPolicy, OPA Gatekeeper
151. 서비스 메시 보안 — mTLS (Istio), 인증서 자동 순환
152. 서버리스 보안 — 함수별 최소 권한, 콜드 스타트 악용
153. 클라우드 로깅 — CloudTrail / Cloud Audit Logs / Activity Log
154. 클라우드 위협 모델링 — STRIDE, LINDDUN
155. CSA STAR 인증 — 클라우드 보안 인증
156. FedRAMP — 미국 정부 클라우드 보안
157. CASB (Cloud Access Security Broker) — 사용자↔클라우드 가시성/제어
158. SWG (Secure Web Gateway) — 웹 트래픽 프록시 필터링
159. 데이터 손실 방지 (DLP) — 클라우드 파일 유출 차단
160. 클라우드 컴플라이언스 — PCI DSS Level 1 / ISO 27017 / SOC 2

+++

## 7. 신원 관리 / 접근 제어 — 20개

161. 신원 관리 (Identity Management) — 라이프사이클 (생성/수정/비활성/삭제)
162. IAM (Identity and Access Management) — 인증·인가·감사
163. SSO (Single Sign-On) — SAML 2.0 / OAuth 2.0 / OpenID Connect
164. SAML 2.0 — XML 기반, IDP-SP 연동, Assertion
165. OpenID Connect (OIDC) — OAuth 2.0 위에 ID 레이어, JWT ID Token
166. MFA (Multi-Factor Authentication) — 지식/소유/특징 + 위치/행동
167. FIDO2 / WebAuthn — 암호 없는 인증, 피싱 저항
168. Passkey — FIDO2 기반, Apple/Google/MS 지원
169. PAM (Privileged Access Management) — 특권 계정 관리, 세션 레코딩
170. Privileged Account — 관리자/서비스/공유 계정 위험
171. RBAC (Role-Based Access Control) — 역할 계층, 최소 권한
172. ABAC (Attribute-Based Access Control) — 속성 기반, XACML
173. ReBAC (Relationship-Based AC) — Zanzibar (Google), 객체 관계
174. 최소 권한 원칙 (PoLP) — 실행 시점에 필요한 권한만
175. 직무 분리 (SoD, Segregation of Duties) — 4-eyes 원칙
176. 디렉터리 서비스 — LDAP / Active Directory / Azure AD / Okta
177. Federation (연합 ID) — 신뢰 도메인 간 ID 공유
178. SCIM (System for Cross-domain Identity Management) — 사용자 프로비저닝 자동화
179. JIT (Just-In-Time) 권한 — 필요 시점에만 권한 부여, PAM
180. 행동 분석 (UEBA) — User/Entity Behavior Analytics, 이상 행동 탐지

+++

## 8. 보안 운영 (SecOps/SOC) — 22개

181. SOC (Security Operations Center) — 보안 관제, 티어 1/2/3
182. SIEM (Security Information and Event Management) — 로그 수집, 상관 분석, 알림
183. SOAR (Security Orchestration, Automation and Response) — 플레이북, 자동화
184. Threat Intelligence (위협 정보) — 전략적/전술적/운영적/기술적 TI
185. MITRE ATT&CK — 전술(Tactics) / 기법(Techniques) / 절차(Procedures)
186. Cyber Kill Chain (Lockheed Martin) — 정찰/무기화/배달/악용/설치/C2/실행
187. MITRE D3FEND — 방어 기법 온톨로지
188. 인시던트 대응 (IR, Incident Response) — 준비/식별/억제/근절/복구/교훈
189. DFIR (Digital Forensics and Incident Response)
190. 포렌식 (Digital Forensics) — 증거 보전, 연속 보관, 법적 증거 요건
191. 메모리 포렌식 — Volatility, 프로세스 덤프, 아티팩트 분석
192. 네트워크 포렌식 — PCAP 분석, DNS 로그, 프록시 로그
193. 타임라인 분석 — 이벤트 재구성, $MFT, 레지스트리 분석
194. 취약점 스캐닝 — Nessus / OpenVAS / Qualys VMDR
195. 침투 테스트 (Penetration Testing) — 블랙박스/회색박스/화이트박스
196. 레드팀 (Red Team) vs 블루팀 (Blue Team) vs 퍼플팀
197. BAS (Breach and Attack Simulation) — Cymulate, SafeBreach
198. 위협 헌팅 (Threat Hunting) — 가설 기반 선제 탐사
199. Honey Pot / Honey Net — 공격자 유인 및 분석
200. 카나리 토큰 (Canary Token) — 조기 침해 탐지
201. EPP (Endpoint Protection Platform) — AV + 행위 차단 + 인터넷 필터링
202. 사이버 레질리언스 (Cyber Resilience) — 저항성+흡수력+복구력+적응력

+++

## 9. 악성코드 / 공격 기법 — 24개

203. 악성코드 (Malware) 분류 — 바이러스/웜/트로이목마/랜섬웨어/스파이웨어/애드웨어/루트킷/봇
204. 랜섬웨어 (Ransomware) — 이중 갈취, RaaS (서비스형 랜섬웨어)
205. APT (Advanced Persistent Threat) — 표적/지속/은밀 공격
206. APT 공격 단계 — 정찰→침투→내부 이동→기반 구축→데이터 유출
207. 피싱 (Phishing) / 스피어 피싱 (Spear Phishing) / 웨일링 (Whaling)
208. 스미싱 (Smishing) / 비싱 (Vishing)
209. BEC (Business Email Compromise) — 임원 사칭 금융 사기
210. 소셜 엔지니어링 (Social Engineering) — 프리텍스팅, 테일게이팅
211. 제로데이 공격 (Zero-Day Attack) — 패치 전 취약점 악용
212. 워터링홀 (Watering Hole) — 자주 방문 사이트 감염
213. 드라이브-바이 다운로드 (Drive-By Download)
214. 공급망 공격 (Supply Chain Attack) — SolarWinds, 3CX, XZ Utils
215. 다형성 악성코드 (Polymorphic Malware) — 서명 회피
216. 메타모픽 악성코드 (Metamorphic Malware) — 코드 구조 변환
217. 파일리스 악성코드 (Fileless Malware) — 메모리 상주, LOLBins
218. LOLBins (Living Off the Land Binaries) — 정상 계통 도구 악용
219. C2 (Command & Control) — 봇넷, Cobalt Strike, Sliver, Havoc
220. DNS 터널링 (DNS Tunneling) — C2 통신 은닉
221. 스테가노그래피 (Steganography) — 이미지에 데이터 은닉
222. 반사 공격 (Reflection Attack) / 증폭 공격 (Amplification) — DNS/NTP/memcached
223. 크리덴셜 스터핑 (Credential Stuffing) — 유출 계정 목록 자동 대입
224. 패스워드 스프레이 (Password Spraying) — 잠금 회피 분산 시도
225. 측면 이동 (Lateral Movement) — Pass-the-Hash, Pass-the-Ticket, Golden Ticket
226. 지속성 (Persistence) 기법 — 레지스트리 런키, 예약 작업, 서비스 설치

+++

## 10. 암호 프로토콜 / PKI 심화 — 18개

227. PKI (Public Key Infrastructure) 구성 — CA / RA / VA / OCSP / CRL
228. 루트 CA / 중간 CA / 사용자 인증서 — 신뢰 체인
229. X.509 v3 인증서 — 확장 필드 (SAN, keyUsage, CRL/OCSP 포인터)
230. CT (Certificate Transparency) — 인증서 발급 감사 로그, SCT
231. OCSP 스테이플링 (OCSP Stapling) — 클라이언트 부하↓, 신선도 보장
232. CRL (Certificate Revocation List) vs OCSP — 크기/실시간성 트레이드오프
233. 인증서 핀닝 (Certificate Pinning) — HPKP (deprecated) → 동적 핀닝
234. 코드 서명 (Code Signing) — 소프트웨어 무결성, 타임스탬핑
235. 이메일 보안 — S/MIME, PGP, DKIM / SPF / DMARC
236. DKIM (DomainKeys Identified Mail) — 이메일 위조 방지
237. SPF (Sender Policy Framework) — 발송 서버 IP 검증
238. DMARC (Domain-based Message Auth Reporting) — SPF+DKIM 정책
239. DANE (DNS-Based Authentication of Named Entities) — TLSA 레코드
240. SSH 프로토콜 심화 — 키 기반 인증, ForwardAgent 위험, SSH 옵션 강화
241. Kerberos (v5) — KDC (AS+TGS), TGT, ST, 상호 인증
242. NTLM vs Kerberos — 안전성 비교, Pass-the-Hash 공격
243. 영지식 증명 (Zero-Knowledge Proof) — 암호 없이 지식 증명
244. 동형 암호 (Homomorphic Encryption) — 암호화된 채로 연산

+++

## 11. 데이터·개인정보 보호 — 18개

245. 개인정보 (Personal Data) 정의 — 식별가능성
246. 개인정보보호법 (한국) — 수집/처리/제공/파기 원칙, DPO
247. GDPR (EU) — 6가지 처리 근거, 정보 주체 권리, DPO, DPIA
248. CCPA (California Consumer Privacy Act)
249. 정보보호 관리 체계 인증 (ISMS-P) — 한국 통합 인증
250. DLP (Data Loss Prevention) — 콘텐츠 검사, 정책 기반 차단
251. 데이터 마스킹 (Data Masking) — 정적/동적 마스킹
252. 데이터 토큰화 (Tokenization) — 원본↔토큰, PCI DSS
253. 익명화 (Anonymization) vs 가명화 (Pseudonymization)
254. 데이터 분류 (Data Classification) — 공개/내부/기밀/극비
255. 데이터 라이프사이클 보안 — 생성/저장/활용/공유/폐기
256. 전송 암호화 — TLS 1.3, DTLS, WireGuard
257. 저장 암호화 — 전체 디스크 (FDE), 파일 수준, 필드 수준
258. TDE (Transparent Data Encryption) — DB 레벨 암호화
259. 클라우드 데이터 보안 — CSKM (Customer Supplied Key Management)
260. 개인정보 영향 평가 (PIA/DPIA) — 고위험 처리 전 필수
261. 잊혀질 권리 (Right to Erasure) — GDPR Article 17
262. 데이터 이동권 (Data Portability) — GDPR Article 20

+++

## 12. 보안 프레임워크 / 컴플라이언스 — 20개

263. ISO/IEC 27001 — ISMS (정보보안 관리 시스템), PDCA
264. ISO/IEC 27002 — 보안 통제 지침 (93개 통제)
265. ISO/IEC 27005 — 정보보안 위험 관리
266. ISO/IEC 27017 — 클라우드 서비스 보안
267. ISO/IEC 27018 — 클라우드 개인정보 보호
268. NIST Cybersecurity Framework (CSF) 2.0 — 식별/보호/탐지/대응/복구 + 거버넌스
269. NIST SP 800-53 — 연방 정보 시스템 보안 통제
270. NIST SP 800-171 — CUI (Controlled Unclassified Information) 보호
271. NIST SP 800-207 — 제로 트러스트 아키텍처
272. SOC 2 (Type I / Type II) — AICPA, 신뢰 서비스 기준
273. PCI DSS v4.0 — 카드 결제 보안, 12개 요구사항
274. HIPAA — 미국 의료정보 보안
275. CMMC (Cybersecurity Maturity Model Certification) — 미국 국방 공급망
276. CIS Controls v8 — 18개 핵심 보안 통제
277. OWASP ASVS (Application Security Verification Standard)
278. CC (Common Criteria) / ISO 15408 — 제품 보안 인증
279. K-ISMS / ISMS-P — 한국 정보보호 관리체계 인증
280. 전자금융감독규정 — 금융 전산 보안 기준
281. 국가 사이버 안보 전략 — 관제체계, 정보공유, CERT/CSIRT
282. SBOM (Software Bill of Materials) — 공급망 취약점 가시성, EO 14028

+++

## 13. IoT / OT / ICS 보안 — 14개

283. OT (Operational Technology) 보안 — SCADA, ICS, PLC
284. ICS (Industrial Control System) 보안 — IT-OT 경계
285. SCADA 보안 — 취약한 레거시 프로토콜 (Modbus/DNP3 암호화 없음)
286. Purdue 모델 — OT 네트워크 계층 분리 (0~5레벨)
287. IEC 62443 — 산업 자동화 보안 표준
288. ISA/IEC 62443 보안 레벨 (SL 0~4)
289. OWASP IoT Top 10 — 취약한 펌웨어, 기본 계정, 안전하지 않은 업데이트
290. IoT 디바이스 보안 — Secure Boot, 코드 서명, TPM, 격리
291. 펌웨어 분석 — binwalk, Ghidra, 하드코딩 시크릿
292. 물리적 보안 (Physical Security) — CCTV, 생체 인식, 잠금 장치, 환경 통제
293. 차량 보안 (Automotive Security) — UNECE WP.29, ISO/SAE 21434
294. 의료기기 보안 — FDA 지침, SBOM, Cybersecurity Risk Management
295. 스마트 그리드 보안 — AMI 보안, NERC CIP
296. 위성 통신 보안 — 재밍/스푸핑 방지, 암호화

+++

## 14. AI 보안 / 신기술 보안 — 14개

297. AI 보안 위협 — 적대적 예제 (Adversarial Examples), 모델 역전 공격
298. 적대적 공격 (Adversarial Attack) — FGSM, PGD, 물리 세계 공격
299. 데이터 포이즈닝 (Data Poisoning) — 훈련 데이터 오염
300. 모델 추출 (Model Extraction) — 쿼리로 모델 복제
301. 모델 반전 (Model Inversion) — 훈련 데이터 재구성
302. 할루시네이션 보안 위협 — 잘못된 법률/의료 정보, 프롬프트 인젝션
303. 프롬프트 인젝션 (Prompt Injection) — LLM 탈옥, 지시어 오버라이드
304. AI TRiSM (Trust, Risk, Security Management) — Gartner
305. LLM 가드레일 (Guardrails) — 출력 필터링, 안전 레이어
306. 딥페이크 (Deepfake) 탐지 — C2PA 프레임워크, 디지털 워터마킹
307. 컨피덴셜 컴퓨팅 (Confidential Computing) — TEE 기반 AI 학습 보호
308. 양자 컴퓨팅 위협 — "Harvest Now, Decrypt Later" 전략
309. 크립토 민첩성 (Crypto Agility) — 알고리즘 교체 능력
310. 블록체인 보안 — 51% 공격, 스마트 컨트랙트 취약점, Reentrancy

+++

**총 키워드 수: 270개**
