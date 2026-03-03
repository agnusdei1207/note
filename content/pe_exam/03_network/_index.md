+++
title = "3. 데이터통신/네트워크"
description = "OSI 7계층, TCP/IP, 무선통신, 네트워크 장비, 프로토콜, 네트워크 보안"
sort_by = "title"
weight = 3
+++

# 제3과목: 데이터통신 / 네트워크

데이터 통신의 원리와 네트워크 기술을 다룹니다.

## 핵심 키워드

### 데이터 통신 기초
- [데이터 통신 기본](protocol.md) - 통신 요소(전송로/신호/장비), 반이중/전이중, 직렬/병렬 전송
- [신호](modulation.md) - 아날로그/디지털 신호, 주파수/진폭/위상, 대역폭, SNR
- [전송 매체](antenna.md) - UTP/STP 케이블, 동축케이블, 광섬유, 무선 전파, 위성
- [데이터 통신 속도](modulation.md) - 보(Baud) vs bps, 나이퀴스트/샤논 정리, 채널 용량
- [캡슐화/역캡슐화](protocol.md) - 각 계층별 PDU(비트/프레임/패킷/세그먼트/데이터)
- [프로토콜](protocol.md) - 통신 규약, 구문(Syntax)/의미(Semantics)/타이밍(Timing)

### 프로토콜 / 계층 구조
- [OSI 7계층](osi_7_layer.md) - L1(물리)/L2(데이터링크)/L3(네트워크)/L4(전송)/L5(세션)/L6(표현)/L7(응용), PDU/SDU 캡슐화
- [OSI 계층별 장비](osi_7_layer.md) - L1:리피터/허브, L2:브리지/스위치, L3:라우터/L3스위치, L4:L4스위치, L7:ADC/프록시
- [TCP/IP 4계층](tcp_udp.md) - 네트워크 액세스/인터넷/전송/응용, OSI 7계층 매핑
- [TCP/IP 프로토콜 스택](tcp_udp.md) - ARP/RARP/IP/ICMP/IGMP/TCP/UDP/DNS/HTTP/SMTP

### TCP 심화
- [TCP 헤더](tcp_udp.md) - Src/Dst Port(16bit), Seq/Ack Number(32bit), Flags(SYN/ACK/FIN/RST/PSH/URG), Window(16bit)
- [TCP 상태 전이](tcp_udp.md) - LISTEN/SYN-SENT/SYN-RECEIVED/ESTABLISHED/FIN-WAIT-1/FIN-WAIT-2/TIME-WAIT/CLOSE-WAIT/LAST-ACK/CLOSED
- [TCP 3-way Handshake](tcp_udp.md) - SYN(ISN)→SYN-ACK(ISN+1)→ACK, 연결 수립, ISN(초기 순서번호) 난수화
- [TCP 4-way Handshake](tcp_udp.md) - FIN→ACK→FIN→ACK, 연결 해제, TIME-WAIT(2MSL) 이유(지연 패킷/연결 종료 확인)
- [TCP 흐름제어](tcp_udp.md) - 슬라이딩 윈도우, 수신 윈도우(rwnd), Zero Window Probe, Silly Window Syndrome 방지
- [TCP 혼잡제어](tcp_udp.md) - cwnd(혼잡 윈도우), ssthresh(임계값), Slow Start(지수)/Congestion Avoidance(선형)/Fast Retransmit/Fast Recovery
- [TCP 혼잡제어 알고리즘](tcp_udp.md) - Tahoe/Reno/NewReno/Vegas/Cubic(리눅스 기본)/BBR(Bottleneck Bandwidth and RTT)
- [TCP 타이머](tcp_udp.md) - 재전송 타이머(RTO), Persist 타이머, Keepalive 타이머, TIME-WAIT 타이머, 2MSL
- [TCP 신뢰성 메커니즘](tcp_udp.md) - 순차적 전달, ACK 지연(Delayed ACK), Nagle 알고리즘, 선택적 ACK(SACK)
- [TCP vs UDP](tcp_udp.md) - 연결형/비연결형, 신뢰성/최선형, 흐름/혼잡제어 유무, 헤더 크기(20B vs 8B), 사용 사례

### 응용 계층 프로토콜
- [HTTP/1.1](dns_http.md) - 지속 연결(Persistent Connection), 파이프라이닝, 청크 분할 전송, Host 헤더 필수
- [HTTP 메서드](dns_http.md) - GET/POST/PUT/DELETE/PATCH/HEAD/OPTIONS/CONNECT/TRACE, 멱등성(Idempotent)
- [HTTP 상태 코드](dns_http.md) - 1xx(정보)/2xx(성공)/3xx(리다이렉션)/4xx(클라이언트 오류)/5xx(서버 오류)
- [HTTP 헤더](dns_http.md) - General/Request/Response/Entity 헤더, Content-Type/Content-Length/Authorization
- [쿠키/세션](dns_http.md) - Set-Cookie/Cookie, 세션 ID, 세션 하이재킹 방지(HttpOnly/Secure/SameSite)
- [HTTPS/TLS](dns_http.md) - TLS 1.3 핸드쉐이크, 인증서 검증, 세션 키 교환, Perfect Forward Secrecy
- [HTTP/2](dns_http.md) - 멀티플렉싱(스트림/프레임), 헤더 압축(HPACK), 서버 푸시, 스트림 우선순위
- [HTTP/3 & QUIC](http3_quic.md) - UDP 기반, 0-RTT 연결, QPACK, 연결 마이그레이션(Connection ID), HOL 블로킹 해결
- [DNS](dns_http.md) - 계층 구조(루트/TLD/SLD/서브도메인), A/AAAA/PTR/CNAME/MX/TXT/SRV/NS 레코드
- [DNS 질의](dns_http.md) - 재귀(Recursive)/반복(Iterative) 질의, DNS 캐싱, TTL
- [DNS 보안](dns_http.md) - DNSSEC(RRSIG/DS/ DNSKEY), DNS over HTTPS(DoH)/DNS over TLS(DoT), DNS 필터링
- [DHCP](ip_addressing.md) - DORA(Discover/Offer/Request/Ack), DHCP Relay, IP 풀/리스, 옵션(게이트웨이/DNS)
- [SMTP/POP3/IMAP](dns_http.md) - SMTP(포트 25/587, 메일 전송), POP3(다운로드 후 삭제), IMAP(동기화, 폴더)
- [FTP/SFTP](dns_http.md) - 제어 채널(21)/데이터 채널(20/패시브), Active/Passive 모드, SFTP(SSH 기반)
- [SSH](dns_http.md) - 포트 22, 공개키 인증, 키 교환(DH/ECDH), 에이전트 포워딩, SCP/SFTP
- [SNMP](protocol.md) - v1/v2c/v3, Manager/Agent, MIB(Management Information Base), OID, Get/Set/Trap

### 데이터 전송 / 변조 / 부호화
- [회선/패킷/메시지 교환](circuit_packet_switching.md) - 회선(연결 후 독점), 패킷(저장-전달), 메시지(비연결형), 가상회선(SVC)/데이터그램
- [가상회선 vs 데이터그램](circuit_packet_switching.md) - 연결 설정 유무, 순서 보장, 신뢰성, 오버헤드 비교, ATM/MPLS
- [오류 제어](error_control.md) - ARQ(Stop-and-Wait/Go-Back-N/Selective Repeat), FEC(전진 오류 수정: Reed-Solomon/LDPC/Turbo Code)
- [ARQ 방식 비교](error_control.md) - Stop-and-Wait(1:1), Go-Back-N(윈도우 크기 N, 재전송 N), Selective Repeat(버퍼링, 선택적 재전송)
- [오류 검출 코드](error_detection_correction_codes.md) - 패리티(1비트), 해밍코드(7비트, 1비트 오류 수정), CRC-16/32/64(Cyclic Redundancy Check), 체크섬(Checksum)
- [CRC 원리](error_detection_correction_codes.md) - 다항식 연산, 생성 다항식(G(x)), 나머지 연산, 프레임 체크 시퀀스(FCS)
- [패리티 비트](parity_bit.md) - 1차원 패리티(홀수/짝수), 2차원 패리티(행+열), 블록 인터리빙 패리티(RAID)
- [흐름 제어](error_control.md) - 정지-대기(Stop-and-Wait), 슬라이딩 윈도우, XON/XOFF(소프트웨어), RTS/CTS(하드웨어)
- [다중화](multiplexing.md) - FDM(주파수 분할)/TDM(시간 분할)/WDM(파장 분할)/CDM(코드 분할)/OFDM(직교 주파수 분할)
- [다중화 비교](multiplexing.md) - FDM(주파수 영역), TDM(시간 영역), CDM(코드 영역), OFDM(직교성 활용)
- [OFDM/OFDMA](multiplexing.md) - IFFT(역 고속 푸리에 변환), CP(순환 접두사), GI(보호 구간), 주파수 효율, LTE/5G/WiFi 핵심
- [변조](modulation.md) - 아날로그(AM/FM/PM), 디지털(ASK/FSK/PSK/QAM), BPSK(2상)/QPSK(4상)/8PSK/16QAM/64QAM/256QAM
- [QAM 변조](modulation.md) - 진폭+위상 변조, 심볼 레이트(심볼/초당), BER(비트 오류율) vs SNR
- [나이퀴스트 정리](modulation.md) - 이상적 무잡음 채널: C = 2B·log₂(M) bps, 대역폭 효율
- [샤논 정리](modulation.md) - 잡음 채널 용량: C = B·log₂(1 + S/N) bps, S/N(dB) = 10·log₁₀(S/N)
- [양자화/표본화](quantization.md) - 표본화(Sampling, fs≥2fmax), 양자화(Quantization, 비트 깊이), 부호화(Encoding), PCM(Pulse Code Modulation)
- [A/D 변환기](quantization.md) - Sample and Hold, ADC(Analog-to-Digital), DAC(Digital-to-Analog), 해상도(Resolution)/속도(Sampling Rate)
- [부호화/복호화](encoder_decoder.md) - 라인 코드(NRZ/NRZI/RZ/Manchester/AMI/4B/5B/8B/MLT-3), 스크램블링, 비트 스터핑
- [맨체스터 코드](encoder_decoder.md) - 자체 클럭 복원(전이 횟수), 위상 인코딩, 10Base-T, 100Base-TX
- [채널 코딩](encoder_decoder.md) - 블록 코드(해밍/Reed-Solomon), 컨볼루션 코드(Viterbi/Turbo), LDPC(5G/WiFi 6)
- [데이터 압축](encoder_decoder.md) - 무손실(Huffman/LZ77/LZ78/LZW/DEFLATE), 손실(JPEG/MP3/H.264/AV1)
- [Base64 인코딩](base64_encoding.md) - 64문자(A-Z, a-z, 0-9, +, /), 3바이트→4문자 변환, 패딩(=), MIME/이메일 첨부

### IP 주소 / 라우팅
- [IP 주소 체계](ip_addressing.md) - IPv4 클래스 A/B/C/D/E, 사설/공인 IP, 특수 주소
- [서브네팅](ip_addressing.md) - CIDR, FLSM/VLSM, 서브넷 마스크 계산, 호스트 수 산출
- [IPv6](ip_addressing.md) - 128비트, 주소 표기, 유니캐스트/멀티캐스트/애니캐스트, ICMPv6, NDP
- [IPv6 전환 기법](ip_addressing.md) - 듀얼스택, 터널링(6to4/Teredo), NAT64/DNS64
- [NAT/PAT](ip_addressing.md) - 사설IP↔공인IP 변환, 포트 매핑(NAPT), STUN/TURN
- [ARP/RARP](ip_addressing.md) - IP↔MAC 주소 변환, ARP 캐시, Gratuitous ARP
- [ICMP](ip_addressing.md) - 제어 메시지 프로토콜, ping/traceroute, Type/Code
- [라우팅](routing.md) - 정적/동적 라우팅, 라우팅 테이블, 포워딩 테이블
- [거리벡터 vs 링크상태](routing.md) - 벨만-포드 vs 다익스트라, 수렴 속도, 루팅 루프
- [RIP v1/v2](routing.md) - 거리벡터, 홉 카운트, 수평 분할
- [OSPF](routing.md) - 링크상태, Area 구조, LSA 홍수, SPF 계산, DR/BDR 선출
- [BGP (외부 게이트웨이)](routing.md) - 경로벡터, AS 간 라우팅, 인터넷 백본, 정책 라우팅
- [EIGRP](routing.md) - 하이브리드 라우팅, 처리량/지연 고려, DUAL 알고리즘
- [IGP vs EGP](routing.md) - 내부/외부 게이트웨이 프로토콜 비교

### 네트워크 장비 / 구성
- [네트워크 장비](network_equipment.md) - L1:리피터/허브, L2:브리지/L2/L3 스위치, L3:라우터, L7:ADC/WAF/프록시/게이트웨이
- [스위치 동작](ethernet.md) - MAC 주소 학습(Adaptive Learning), 플러딩/포워딩/필터링/에이징
- [포트 미러링](ethernet.md) - SPAN/TPID/RSPAN/Mirrored Port, 링크 집합(LAG)
- [포트 보안](ethernet.md) - 802.1X(Port-Based NAC), Sticky MAC, DHCP Snooping/ARP Inspection
- [이더넷](ethernet.md) - CSMA/CD, 충돌 도메인(Collision Domain), 브로드캐스트 도메인, Jumbo Frame(9000바이트)
- [MAC 주소](ethernet.md) - 48비트, OUI(24비트, 제조사)+NIC(24비트, 일련번호), I/G/비트로 유니캐스트/멀티캐스트/브로드캐스트 구분
- [VLAN](ethernet.md) - 포트 기반/태그 기반(802.1Q), Native VLAN, 트렁크(Trunk)/액세스(Access), VTP(VLAN Trunking Protocol)
- [VLAN 간 라우팅](ethernet.md) - Router-on-a-Stick, SVI(Switch Virtual Interface), L3 스위치 라우팅
- [STP/RSTP/MSTP](ethernet.md) - 스패닝 트리 프로토콜, Root Bridge/Designated Bridge 선출, BPDU(Bridge PDU), 포트 역할(Root/Designated/Non-designated)
- [루프 방지](ethernet.md) - STP, Loop Guard, BPDU 가드, UDLD(UniDirectional Link Detection)
- [링크 어그리게이션](ethernet.md) - LACP(802.3ad)/PAgP, 액티브/수동 모드, MLAG(Multi-Chassis LAG), MC-LAG
- [이더넷 채널](ethernet.md) - 채널 복구, 1588av/10GBASE-KR/40GBASE-KR2/25GBASE-KR/100GBASE-KR2(100G)
- [오토 협상](ethernet.md) - 802.3ad(Auto-Negotiation), Flow Control, Priority-based Flow Control
- [SDN (소프트웨어 정의 네트워킹)](sdn_nfv.md) - 제어평면/데이터평면 분리, OpenFlow(1.0~1.5), 중앙화 제어, OVSDB/ODP/OF-Config
- [SDN 컨트롤러](sdn_nfv.md) - 중앙 제어기, NOS(네트워크 운영체제), Northbound/Southbound API
- [OpenFlow 매치](sdn_nfv.md) - Exact Match(1:1)/Prefix Match(1:N)/Wildcard Match(0:N), Flow Table(우선순위)
- [NFV (네트워크 기능 가상화)](sdn_nfv.md) - VNF(Virtual Network Function), NFVI(인프라), VNFM/VIM/MANO(관리/오케스트레이션)
- [SD-WAN](sdn_nfv.md) - 소프트웨어 정의 광역망, AMP(Application-Aware Routing), 다중 링크(MPLS/인터넷/4G/LTE) 활용, QoS 보장
- [IBN (의도 기반 네트워킹)](sdn_nfv.md) - 비즈니스 의도→자동 네트워크 정책, GUI/AI 기반 구성, 검증/롤백
- [네트워크 자동화](sdn_nfv.md) - Ansible/NSO/Terraform, NETCONF/YANG, gNMI/gRPC, Event-Driven Automation
- [IoT 네트워크](iot.md) - LPWAN(LoRaWAN/NB-IoT/Sigfox/LTE-M), Zigbee(2.4GHz)/Z-Wave(Sub-GHz)/Thread/6LoWPAN/BLE Mesh

### 무선/이동통신 기초
- [무선 LAN](wireless_communication.md) - IEEE 802.11(WiFi 4/5/6/6E/7), CSMA/CA, RTS/CTS, 은닉/노출 단말 문제
- [WiFi 표준 진화](wireless_communication.md) - 802.11a/b/g/n/ac/ax/be, OFDMA(MU-MIMO), BSS Coloring, TWT(Target Wake Time)
- [블루투스](wireless_communication.md) - BR/EDR/BLE 4.0/5.0/5.3, 주파수 호핑(FHSS), 피코넷/스캐터넷, BLE Mesh
- [UWB](wireless_communication.md) - 초광대역, IEEE 802.15.4a, cm급 정밀 측위, Apple U1/U2 칩
- [NFC/RFID](wireless_communication.md) - NFC-A/B/F(Type 1~4), RFID(125kHz/13.56MHz/900MHz), 비접촉 결제/물류 추적
- [무선 채널 특성](fading_diversity.md) - 경로 손실(Path Loss), 그림자 효과(Shadowing), 다중 경로(Multipath)
- [페이딩](fading_diversity.md) - 대규모/소규모 페이딩, 레일리(무가우시안)/라이시안(LOS) 페이딩, 플랫/주파수 선택성 페이딩
- [다이버시티](fading_diversity.md) - 공간/주파수/시간/편파 다이버시티, 선택/최대비/등이득 합성, MRC(Maximal Ratio Combining)
- [MIMO](antenna.md) - SU-MIMO/MU-MIMO, 공간 다중화(SM), 공간 블록 부호(SFBC/STBC), 채널 상태 정보(CSI)
- [빔포밍](antenna.md) - 디지털/아날로그/하이브리드 빔포밍, 안테나 어레이, Massively Parallel Processing

### 셀룰러 / 이동통신
- [셀룰러 구조](mobile_communication.md) - 셀 분할(Femto/Pico/Micro/Macro), 주파수 재사용, 클러스터(N=3/4/7)
- [핸드오버](mobile_communication.md) - Hard/Soft Handover, 인트라-인터 빈도 핸드오버, MOB/MT 핸드오버, 핸드오버 실패율(HOF)
- [간섭 관리](mobile_communication.md) - 동채널 간섭(CCI), 인접 채널 간섭(ACI), 간섭 조정(ICIC)
- [전력 제어](mobile_communication.md) - 개방루프/폐루프, 내부/외부 전력 제어, UPC(역링크 전력제어)

### LTE / 4G
- [LTE 구조](mobile_communication.md) - EPC(Evolved Packet Core), eNodeB, MME(모빌리티), SGW/PGW(게이트웨이), HSS(가입자), PCRF(정책)
- [LTE 무선 접속](mobile_communication.md) - OFDMA(하향), SC-FDMA(상향), 20MHz 대역폭, 150Mbps~1Gbps
- [LTE 프로토콜](mobile_communication.md) - RRC/PDCP/RLC/MAC/PHY, 무선 베어러(RB), QoS 클래스 식별자(QCI)
- [LTE-A (Advanced)](mobile_communication.md) - CA(캐리어 어그리게이션: intra/inter-band), CoMP(협력 통신), HetNet(이종망), eICIC
- [VoLTE](mobile_communication.md) - IMS 기반 음성, SRVCC(Handover to 3G), RTP/RTCP, QCI=1
- [eMBMS](mobile_communication.md) - 멀티미디어 브로드캐스트 멀티캐스트 서비스, eBM-SC

### 5G / NR
- [5G NR(New Radio)](mobile_communication.md) - Sub-6GHz(FR1)/mmWave(FR2: 24~100GHz), 100MHz~1GHz 대역폭
- [5G 핵심 기술](mobile_communication.md) - Massive MIMO(64~256 안테나), 3D 빔포밍, Full-Dimension MIMO
- [5G 코어망(5GC)](mobile_communication.md) - SBA(서비스 기반 아키텍처), AMF/SMF/UPF, NSSF/PCF/UDM/AUSF
- [네트워크 슬라이싱](mobile_communication.md) - eMBB(고속)/URLLC(초저지연)/mMTC(대규모연결), NSSAI, Slice Profile
- [5G RAN](mobile_communication.md) - gNB, CU/DU 분리, F1/WDM-CPRI/eCPRI 프론트홀, O-RAN
- [5G 특화망(Private 5G)](mobile_communication.md) - SA/NSA 구성, MEC(Multi-access Edge Computing), NPN(Non-Public Network)
- [5G-Advanced](mobile_communication.md) - 3GPP Rel-18/19, XR 지원, RedCap(Reduced Capability), AI/ML 기반 최적화

### 6G / 미래 통신
- [6G 비전](mobile_communication.md) - 2030년 상용화, 1Tbps, 0.1ms 지연, 100km² 당 10M 디바이스
- [6G 핵심 기술](mobile_communication.md) - 테라헤르츠(100GHz~10THz), 지능형 반사면(RIS/IRS), 통합 공중 인터페이스(AI-Native)
- [탈지구 통신](mobile_communication.md) - NTN(Non-Terrestrial Network), 위성-지상 통합, HAPS(고고도 플랫폼)
- [NOMA](mobile_communication.md) - 비직교 다중접속, SIC(Successive Interference Cancellation), 전력 도메인 다중화

### 위성통신 / 광통신
- [위성통신](antenna.md) - LEO(Starlink/OneWeb: 300~2000km)/MEO(GPS: 20000km)/GEO(36000km), 지연/커버리지 트레이드오프
- [위성 인터넷](antenna.md) - Starlink(4200위성), Ka/Ku 밴드, Phased Array 안테나, 레이저 ISL(위성간 링크)
- [광통신](optical_communication.md) - SMF(단일모드: 1310/1550nm)/MMF(다중모드: 850nm), G.652/G.655 표준
- [광 증폭](optical_communication.md) - EDFA(어비움 첨가), Raman 증폭, 중계기(Repeater)
- [WDM/DWDM](optical_communication.md) - 파장 분할 다중화, CWDM(18파장)/DWDM(40~160파장), OADM/ROADM
- [FTTH/PON](optical_communication.md) - GPON(2.5G/1.25G), XGS-PON(10G), NG-PON2, OLT/ONT/ODN
- [OTN](optical_communication.md) - 광 전송 네트워크, G.709, ODUk/OTUk 계층, FEC(전방 오류 정정)

### 네트워크 보안
- [VPN](vpn_network_security.md) - IPsec(AH/ESP, 터널/전송 모드), SSL/TLS VPN(OpenVPN/Clientless), L2TP over IPsec, PPTP(취약)
- [IPsec 프로토콜](vpn_network_security.md) - IKEv1/v2(키 교환), SA(Security Association), ESP(Encapsulating Security Payload), AH(Authentication Header)
- [IPsec 모드](vpn_network_security.md) - 터널 모드(원본 패킷 캡슐화)/전송 모드(페이로드만 암호화)
- [방화벽](vpn_network_security.md) - 패킷 필터링/상태추적(Stateful Inspection)/애플리케이션 프록시(Proxy), NGFW(차세대 방화벽)
- [NGFW](vpn_network_security.md) - DPI(심도 패킷 검사), 앱 인식, IPS 통합, SSL/TLS 복호화, 위협 인텔리전스
- [IDS/IPS](vpn_network_security.md) - 침입 탐지/방지, 시그니처 기반(패턴 매칭)/이상 탐지(행위 분석), 인라인(IPS)/패시브(IDS) 배치
- [WAF (웹 방화벽)](vpn_network_security.md) - OWASP Top 10 방어, SQL Injection/XSS 방지, 가상 패치
- [제로 트러스트 아키텍처](zero_trust_architecture.md) - "Never Trust, Always Verify", ZTNA(Zero Trust Network Access), SDP(Software Defined Perimeter)
- [ZTNA vs VPN](zero_trust_architecture.md) - VPN(경계 기반)/ZTNA(에이전트 기반, 지속 검증, 세분화 접근), BeyondCorp(Google)
- [DDoS 공격](vpn_network_security.md) - 볼류메트릭(Volumetric)/프로토콜(Protocol)/애플리케이션(Application) 레이어 공격
- [DDoS 방어](vpn_network_security.md) - CDN/Anycast/블랙홀 라우팅/트래픽 스크러빙/WAF/레이트 리미팅
- [Syn Flood/UDP Flood](vpn_network_security.md) - SYN Cookie, TCP Intercept, UDP 포트 차단, Amplification 방지
- [네트워크 포렌식](vpn_network_security.md) - 패킷 캡처(Wireshark/tcpdump), PCAP 분석, 타임라인 재구성, IOC(Indicators of Compromise) 추출
- [NAC (네트워크 접근 제어)](vpn_network_security.md) - 802.1X(EAP-TLS/EAP-PEAP), RADIUS, 포스처(Posture) 검사, 게스트 VLAN 분리
- [포트 시큐리티](vpn_network_security.md) - 포트 스캔 탐지, 서비스 필터링, 불필요한 서비스 비활성화

### 서비스 품질 / 관리
- [QoS](routing.md) - DiffServ(DSCP: EF/AF/BE), IntServ(RSVP), 트래픽 셰이핑(Shaping)/폴리싱(Policing)
- [QoS 메커니즘](routing.md) - 분류(Classification)/마킹(Marking)/폴리싱(Policing)/큐잉(Queuing)/스케줄링(Scheduling)
- [큐잉 알고리즘](routing.md) - FIFO/PQ(Priority Queuing)/WFQ(Weighted Fair Queuing)/CBWFQ(Class-Based WFQ)/LLQ(Low Latency Queuing)
- [MPLS](routing.md) - 레이블 스위칭(2.5계층), LER(Label Edge Router)/LSR(Label Switching Router), LSP(Label Switched Path)
- [MPLS 서비스](routing.md) - L2VPN(VPLS/E-Line)/L3VPN(VPRN)/TE(Traffic Engineering)/Fast Reroute
- [MPLS 레이블](routing.md) - 레이블(20비트), EXP(실험용)/S(서비스)/BOS(스택 하단), TTL, PHP(Penultimate Hop Popping)
- [네트워크 관리](protocol.md) - FCAPS(장애/구성/회계/성능/보안), NMS(네트워크 관리 시스템), SNMP v1/v2c/v3
- [SNMP](protocol.md) - Manager/Agent, Get/GetNext/Set/Trap/Inform, MIB(Management Information Base), OID(Object Identifier)
- [RMON](protocol.md) - 원격 모니터링, RMON v1/v2, 프로브(Probe), 이력(History)
- [NetFlow/IPFIX](protocol.md) - 플로우 수집, 익스포트(Exporter)/콜렉터(Collector), AS 정보, 샘플링
- [클라우드 네이티브 네트워킹](sdn_nfv.md) - CNI(Flannel/Calico/Cilium/Weave), 서비스 메시(Istio/Linkerd/Consul Connect), eBPF/XDP
- [CNI 플러그인](sdn_nfv.md) - Overlay(VXLAN/IPIP)/Underlay(BGP), 라우팅 모드(VXLAN/HostGW), 네트워크 정책(NetworkPolicy)
- [서비스 메시](sdn_nfv.md) - 사이드카 프록시(Envoy), mTLS, 트래픽 관리(VirtualService/DestinationRule), 카나리/서킷브레이커
- [eBPF 네트워킹](sdn_nfv.md) - 커널 우회 없는 패킷 처리, XDP(eXpress Data Path), tc(traffic control), 맵/스키비/튜플 업데이트
- [역색인 (Inverted Index)](inverted_index.md) - 문서→단어 매핑, 포스팅 리스트, TF-IDF, Elasticsearch/Lucene/Solr
