+++
title = "1. 컴퓨터 구조"
description = "컴퓨터 구조, CPU, 메모리, 입출력, 디지털 논리 회로"
sort_by = "title"
weight = 1
+++

# 제1과목: 컴퓨터 구조

컴퓨터 시스템의 구성요소와 동작 원리를 다룹니다.

## 핵심 키워드

### CPU / 처리장치
- [CPU 구조](cpu_architecture.md) - ALU(산술논리장치, 가산기/곱셈기)/제어장치(Control Unit)/레지스터(범용/특수)/데이터 경로(Data Path)
- [CPU 내부 버스](cpu_architecture.md) - 데이터 버스(32/64비트)/주소 버스(주소 공간)/제어 버스(Read/Write)
- [CPU 성능 공식](cpu.md) - 실행시간 = (명령어 수 × CPI) / 클럭속도, MIPS = (명령어 수 / 실행시간) / 10⁶, MFLOPS = (부동소수점 연산 수 / 실행시간) / 10⁶
- [암달의 법칙](cpu.md) - 전체 개선 후 속도 = 1 / ((1-병렬화율) + 병렬화율/프로세서 수), 이론적 한계
- [구스타프손 법칙](cpu.md) - 실제 확장성: 확장 속도 = 병렬화율 + (1-병렬화율)/프로세서 수, 워크로드 증가 고려
- [명령어 사이클](instruction_cycle.md) - Fetch(인출)→Decode(해석)→Execute(실행)→Memory(메모리 접근)→Writeback(결과 저장), 마이크로 사이클
- [인터럽트 사이클](instruction_cycle.md) - 명령어 완료 후 인터럽트 확인, PC 저장, ISR(인터럽트 서비스 루틴) 점프
- [명령어 형식](instruction_cycle.md) - 0주소(스택), 1주소(누산기), 2주소(ACC+레지스터), 3주소(연산+저장), Opcode(4~8비트)+Operand
- [명령어 집합 구조(ISA)](instruction_cycle.md) - CISC(x86)/RISC(ARM/RISC-V)/VLIW/EPIC(Itanium), 레지스터 수, 주소 지정 방식
- [파이프라이닝](instruction_pipeline.md) - 5단계(IF/ID/EX/MEM/WB), 처리량(Throughput) 증가, CPI 이상적=1
- [파이프라인 성능](instruction_pipeline.md) - 스피드업 = 순차시간 / 파이프라인시간, 효율 = 이상적 시간 / 실제 시간
- [파이프라인 해저드](stall.md) - 구조적(자원 충돌)/데이터(의존성)/제어(분기) 해저드, RAW(Read After Write)/WAR/WAW
- [해저드 해결 기법](stall.md) - Stall(버블), 포워딩(Bypassing/Forwarding), 분기 예측, 지연 슬롯(Delay Slot), 코드 재배치
- [데이터 해저드](stall.md) - RAW(진성 의존)/WAR(반의존)/WAW(출력 의존), 레지스터 리네이밍, 스코어보딩
- [제어 해저드](stall.md) - 분기 지연, 분기 예측(정적/동적), 분기 타겟 버퍼(BTB), 반환 주소 스택(RAS)
- [슈퍼스칼라](pipeline.md) - 복수 파이프라인(2~8-way), 동시 다중 명령어 발행(Issue), 디스패치, 완료(Commit)
- [비순서 실행(OoO)](pipeline.md) - 명령어 레벨 병렬성(ILP) 활용, 스코어보드, 토마줄로 알고리즘(레지스터 리네이밍)
- [투기적 실행](pipeline.md) - Speculative Execution, 분기 결과 확정 전 실행, Spectre/Meltdown 취약점
- [분기 예측](pipeline.md) - 정적(Not-Taken/Taken/프로필 기반)/동적(1비트/2비트/BHT/BTB), 예측 정확도 영향
- [분기 예측기](pipeline.md) - BHT(Branch History Table, 1비트/2비트), BTB(Branch Target Buffer), RAS(Return Address Stack)
- [분기 예측 정확도](pipeline.md) - 예측 성공률, 미예측 페널티(Misprediction Penalty), 파이프라인 플러시 비용
- [CISC vs RISC](cisc.md) - CISC(복잡, 가변 길이, 마이크로코드, 메모리→레지스터)/RISC(단순, 고정 길이, 하드와이어드, 레지스터→메모리)
- [RISC 설계 원칙](risc.md) - 단순 명령어, 고정 길이, Load/Store 구조, 대형 레지스터 파일, 레지스터 윈도우, 지연 분기
- [ARM 아키텍처](risc.md) - ARMv7(32비트)/ARMv8(64비트), Thumb-2(16/32비트 혼합), 빅.LITTLE(이종 코어)
- [RISC-V](risc.md) - 오픈 소스 ISA, 확장 모듈형(IMAFDQ), 표준 확장(S/D/V), 특허 무료
- [VLIW/EPIC](vliw.md) - 초장 명령어(128~256비트), 컴파일러 기반 병렬성 추출, 정적 스케줄링, Itanium
- [EISC](eisc.md) - 임베디드 RISC, Low Power, Thumb-2 유사, IoT/임베디드
- [마이크로 오퍼레이션](microinstruction.md) - 제어 신호 단위 동작, 수평형(병렬 제어)/수직형(인코딩), 마이크로프로그래밍
- [제어 장치 구현](microinstruction.md) - 하드와이어드(고정 로직, 빠름)/마이크로프로그램(ROM, 유연), 제어 메모리
- [멀티코어 프로세서](multiprocessor.md) - 다중 코어 구조(2~64코어), 공유 캐시(L2/L3)/전용 캐시(L1), 코어 간 인터커넥트
- [HW 스레드 / SMT](multiprocessor.md) - Hyper-Threading(Intel)/SMT(POWER), 물리 코어당 2~8 스레드, 리소스 공유
- [동시 멀티스레딩(SMT)](multiprocessor.md) - 1사이클에 여러 스레드 명령어 실행, ALU/캐시 공유, 레지스터 분리

### 메모리 계층
- [메모리 계층 구조](memory_hierarchy.md) - 레지스터(CPU, ns)→L1 캐시→L2/L3→DRAM(ns)→SSD(μs)→HDD(ms), 위로 갈수록 빠르고 작고 비쌈
- [메모리 계층 목적](memory_hierarchy.md) - 속도(CPU)/비용(저장장치) 트레이드오프, 지역성(Locality) 활용, 평균 접근 시간 최소화
- [지역성(Locality)](memory_hierarchy.md) - 시간 지역성(반복 접근)/공간 지역성(인근 접근), 순차 지역성(배열 순회), 분기 지역성
- [캐시 메모리](cache_memory.md) - SRAM 기반, L1(Instruction/Data, 32~64KB)/L2(256KB~1MB)/L3(공유, 8~64MB), 계층적 구조
- [캐시 성능 지표](cache_memory.md) - 히트율(Hit Rate)/미스율(Miss Rate), AMAT(평균 메모리 접근 시간) = Hit Time + Miss Rate × Miss Penalty
- [캐시 매핑 방식](cache_memory.md) - 직접 사상(Direct, 1-way)/완전 연관(Fully, N-way)/집합 연관(Set-Associative, n-way)
- [캐시 구조](cache_memory.md) - 태그(Tag)/인덱스(Index)/오프셋(Offset), 블록 크기(Block Size, 32~128B), 라인(Line)/셋(Set)
- [집합 연관 캐시](cache_memory.md) - 2-way/4-way/8-way, Higher Associativity=낮은 충돌/높은 복잡도
- [캐시 쓰기 정책](cache_memory.md) - Write-Through(즉시 기록)/Write-Back(지연, Dirty Bit), Write-Allocate(미스 시 적재)/No-Write-Allocate(미스 시 직접 기록)
- [캐시 미스 분류 (3C)](cache_memory.md) - Compulsory(첫 접근, Cold Miss)/Capacity(용량 부족)/Conflict(충돌)
- [캐시 최적화](cache_memory.md) - 프리페칭(Prefetching)/스트라이드(Stride)/비트래킹/분리 캐시(Split I/D)
- [캐시 일관성(Cache Coherence)](cache_memory.md) - 멀티코어 캐시 동기화, Write Invalidate/Write Update, MESI(Modified/Exclusive/Shared/Invalid)
- [MESI 프로토콜](cache_memory.md) - Modified(수정됨)/Exclusive(단독)/Shared(공유)/Invalid(무효), 상태 전이, Bus Snooping
- [MOESI](cache_memory.md) - MESI + Owner(소유자), Forwarding(전달), snoop 필터링
- [가상 메모리](virtual_memory.md) - 주소 변환(VA→PA), 페이지(4KB~2MB)/프레임, TLB(Translation Lookaside Buffer)
- [페이지 테이블](virtual_memory.md) - PTE(Page Table Entry), Valid/Dirty/Reference/Access 비트, 다단계(L2/L3)/역(Inverted) 페이지 테이블
- [TLB](virtual_memory.md) - 주소 변환 캐시, 64~128 엔트리, TLB 미스(Page Walk), ASID(주소 공간 ID)
- [페이지 부재](virtual_memory.md) - Page Fault(Valid=0), 디맨드 페이징(Demand Paging), 페이지 교체, 스왑 영역(Swap Space)
- [페이지 교체 알고리즘](virtual_memory.md) - FIFO(First-In)/LRU(Least Recently Used)/LFU(Least Frequently Used)/Optimal(Belady's)/Clock(NRU)/WSClock
- [페이지 교체 평가](virtual_memory.md) - LRU(근사, 구현 복잡)/Clock(간단, 하드웨어 지원)/Aging(비트 시프트)
- [스래싱(Thrashing)](virtual_memory.md) - 과도한 페이지 교체, 워킹셋(Working Set) 모델, PFF(Page Fault Frequency), 지역성 교체
- [워킹셋](virtual_memory.md) - 시간 윈도우 내 접근 페이지 집합, 동적 크기 조정, 스래싱 방지
- [세그멘테이션](virtual_memory.md) - 논리 단위 분할(Code/Data/Stack/Heap), 가변 길이, 외부 단편화
- [페이징 vs 세그멘테이션](virtual_memory.md) - 고정 길이/가변 길이, 내부 단편화/외부 단편화, 주소 변환 구조
- [RAM 유형](ram.md) - SRAM(정적, 캐시, 6T)/DRAM(동적, 주기억, 1T1C, 리프레시), SDRAM(동기), DDR(더블 데이터 레이트)
- [DRAM 구조](ram.md) - 행/열 주소, RAS/CAS, 리프레시(Refresh, 64ms), 프리차지(Precharge)
- [DDR 진화](ram.md) - DDR4(3200MT/s)/DDR5(5600MT/s), 뱅크 그룹, 온다이 ECC, 전압 하락(1.2V→1.1V)
- [ROM 계열](rom.md) - Mask ROM(공장)/PROM(1회)/EPROM(UV 소거)/EEPROM(전기 소거)/Flash(NAND/NOR)
- [플래시 메모리](flash_memory.md) - NAND(대용량, SSD)/NOR(읽기 빠름, 펌웨어), SLC/MLC/TLC/QLC(셀당 비트), Wear Leveling
- [SSD 내부](flash_memory.md) - 컨트롤러, 채널(다중), FTL(Flash Translation Layer), 가비지 컬렉션, TRIM
- [NVMe](flash_memory.md) - PCIe 기반 SSD, 높은 큐 깊이(Queue Depth, 64), MSI-X, 4KB/8KB LBA
- [메모리 인터리빙](memory_hierarchy.md) - 상위(High-Order)/하위(Low-Order)/블록 인터리빙, 병렬 접근, 대역폭 향상
- [인터리빙 효과](memory_hierarchy.md) - 메모리 뱅크 활용, 버스트 모드, 지연 회피
- [CXL 인터페이스](cxl_interface.md) - PCIe 5.0/6.0 기반, 메모리 확장, CXL.mem/CXL.cache/CXL.io, Type-1/2/3 장치
- [CXL 유스케이스](cxl_interface.md) - 메모리 풀링(Shared Memory)/계층형 메모리(HBM+DDR)/가속기 간 공유
- [HBM (고대역폭 메모리)](ram.md) - 3D 적층(TSV), HBM2/2E/3/3e, 8~12층, AI 가속기용, 256~1024GB/s
- [HBM vs GDDR](ram.md) - HBM(3D 적층, 저전력)/GDDR6X(2D, 고속), GPU/HBM, GPU/GDDR
- [Optane/SCM](flash_memory.md) - 3D XPoint(인텔/마이크론), Storage Class Memory, 지속형 메모리(Persistent Memory), PMEM

### 입출력 / 버스
- [I/O 방식 비교](dma.md) - 프로그램 I/O(Polling, CPU 대기)/인터럽트 I/O(이벤트 기반)/DMA(CPU 개입 최소)
- [DMA(Direct Memory Access)](dma.md) - 장치→메모리 직접 전송, CPU 버스트 해제, DMA 컨트롤러(DMAC), 버스 마스터
- [DMA 전송 모드](dma.md) - Cycle Stealing(한 사이클씩)/Burst Mode(연속)/Interleaved(교차), Fly-by 전송
- [DMA 컨트롤러](dma.md) - 주소 레지스터/카운트/제어 레지스터, 초기화→전송→완료 인터럽트
- [IOP/채널](dma.md) - 입출력 프로세서, 셀렉터(Selector)/멀티플렉서(Multiplexer)/블록 멀티플렉서 채널
- [인터럽트](interrupt.md) - HW(장치, 타이머, 예외)/SW(SVC, Trap) 인터럽트, 동기/비동기
- [인터럽트 처리 과정](interrupt.md) - 요청→우선순위 판별→현재 PC 저장→ISR 점프→처리→복귀
- [인터럽트 벡터 테이블](interrupt.md) - 인터럽트 번호→ISR 주소 매핑, IDT(x86), IVT(ARM), 벡터 번호
- [인터럽트 우선순위](interrupt.md) - 데이지 체인(Daisy Chain)/폴링(Polling)/우선순위 인코더/PIC(Programmable Interrupt Controller)
- [마스크/비마스크 인터럽트](interrupt.md) - Maskable(프로그램 제어 가능)/Non-Maskable(NMI, 하드웨어 오류), IF 플래그
- [인터럽트 중첩](interrupt.md) - 인터럽트 처리 중 더 높은 우선순위 인터럽트, 스택 활용, 재진입
- [버스](bus.md) - 시스템 버스(데이터/주소/제어), Front-Side Bus(FSB)/DMI/QPI/UPI(Intel), HyperTransport/Infinity Fabric(AMD)
- [버스 대역폭](bus.md) - 대역폭 = 버스 폭(비트) × 클럭(MHz) × 전송당 데이터(바이트), MB/s, GB/s
- [버스 중재(Arbitration)](bus.md) - 데이지 체인(순차)/중앙집중식(Centralized)/분산식(Distributed), 고정/가변 우선순위, 공정성
- [버스 중재 알고리즘](bus.md) - 고정 우선순위/Time-Sliced/Lottery/First-Come-First-Serve
- [핸드쉐이킹](handshaking.md) - 동기(클럭 기반, STROBE/ACK)/비동기(요청-응답, 2-way/3-way), 전송 동기화
- [동기/비동기 전송](handshaking.md) - 동기(클럭 공유)/비동기(Start/Stop 비트, UART), 전송 효율 vs 신뢰성
- [PCI/PCIe](bus.md) - PCI(병렬, 32/64비트, 133MB/s)/PCIe(직렬, 레인×N, x1/x4/x8/x16, 1~32GB/s)
- [PCIe 구조](bus.md) - Root Complex/Endpoint/Switch, TLP(Transaction Layer Packet), DLLP, LTSSM
- [디스크 스케줄링](disk_scheduling.md) - FCFS(순차)/SSTF(최단 탐색 우선)/SCAN(엘리베이터)/C-SCAN/LOOK/C-LOOK/SLTF
- [디스크 성능](disk_scheduling.md) - 회전 지연(Rotational Latency, 평균 반 회전)/탐색 시간(Seek Time)/전송 시간
- [RAID](raid.md) - Redundant Array of Independent Disks, 스트라이핑(Striping)/미러링(Mirroring)/패리티(Parity)
- [RAID 레벨](raid.md) - RAID 0(스트라이프, 성능↑, 신뢰성↓)/RAID 1(미러, 50% 공간)/RAID 5(블록+패리티, N+1)/RAID 6(이중 패리티)/RAID 10(0+1)
- [RAID 계산](raid.md) - 패리티 계산(XOR), 리빌드(Rebuild) 시간, 체크섬, Hot Spare
- [NVMe RAID](raid.md) - 소프트웨어 RAID(mdadm)/하드웨어 RAID(컨트롤러), 성능, 신뢰성, 비용

### 병렬 처리
- [Flynn 분류](simd_mimd.md) - SISD(단일 명령/단일 데이터)/SIMD(단일/다중, 벡터)/MISD(다중/단일, 거의 없음)/MIMD(다중/다중, 멀티코어)
- [SIMD 응용](simd_mimd.md) - GPU(Graphics, CUDA/OpenCL)/벡터 프로세서(AVX-512/SVE)/AI 추론(배치 처리)
- [MIMD 분류](simd_mimd.md) - SPMD(단일 프로그램/다중 데이터, MPI)/MPMD(다중 프로그램, 클러스터)
- [다중 처리기](multiprocessor.md) - SMP(대칭형, 공유 메모리)/ASMP(비대칭형, 마스터-슬레이브)/AMP(비대칭, I/O 전담)
- [SMP vs ASMP](multiprocessor.md) - SMP(모든 CPU 동등, OS 스케줄링)/ASMP(마스터 CPU만 OS, 분담)
- [UMA/NUMA](multiprocessor.md) - UMA(균등 메모리 접근, 버스)/NUMA(비균등, 코어별 메모리), ccNUMA(Cache Coherent)
- [NUMA 최적화](multiprocessor.md) - 메모리 지역성(Affinity), 페이지 마이그레이션, 인터리브 메모리
- [파이프라인](pipeline.md) - 산술 파이프라인(부동소수점)/명령어 파이프라인(IF/ID/EX/MEM/WB), 처리 단계 중첩
- [상호연결망(Interconnection Network)](hypercube.md) - 크로스바(Crossbar, O(N²))/오메가(Omega)/메시(Mesh)/토러스(Torus)/하이퍼큐브(Hypercube)
- [네트워크 토폴로지](hypercube.md) - 차수(Degree)/지름(Diameter)/대역폭/비용, 확장성
- [NoC(Network-on-Chip)](hypercube.md) - 칩 내부 네트워크, 라우터/링크/버퍼, 라우팅 알고리즘(XY/West-First)
- [GPU 아키텍처](ai_accelerator.md) - SM(Streaming Multiprocessor)/CUDA Core(실행 유닛)/Warp(32 스레드 그룹)/L1/L2 캐시
- [GPU 병렬성](ai_accelerator.md) - SIMT(Single Instruction Multiple Threads), 워프 스케줄링, 분기 발산(Divergence)
- [GPU 메모리](ai_accelerator.md) - 글로벌/공유(Shared, 블록 내)/상수(Constant)/텍스처/레지스터, HBM
- [GPGPU](ai_accelerator.md) - 범용 GPU 컴퓨팅, CUDA/NVIDIA, OpenCL(표준), ROCm/AMD, oneAPI/Intel
- [AI 가속기](ai_accelerator.md) - NPU(신경망 전용, Apple Neural Engine)/TPU(Tensor Processing Unit, Google, TPU v4/v5)/PIM(Processing-In-Memory)
- [TPU 구조](ai_accelerator.md) - MXU(Matrix Multiply Unit, 128×128)/벡터 유닛/하이브리드 메모리, Systolic Array
- [벡터 프로세서](simd_mimd.md) - 벡터 연산(VADD/VMUL), 파이프라인 체이닝, 마스킹, AVX-512(Intel)/SVE(ARM)/RISC-V V-extension
- [SoC(System-on-Chip)](mcu_mpu.md) - CPU+GPU+NPU+IO+메모리 컨트롤러 통합, 전력 효율, 모바일/임베디드
- [NoC(Network-on-Chip)](mcu_mpu.md) - SoC 내부 통신, 버스 대체, 라우터 기반, 대역폭/지연 최적화

### 디지털 논리 회로
- [불 대수(Boolean Algebra)](boolean_algebra.md) - 논리 연산(AND·OR·NOT·XOR), 드모르간 법칙, 논리식 간소화, Canonical Form
- [불 대수 공식](boolean_algebra.md) - 항등원/역원/지배원/보등원, 흡수/결합/분배 법칙, Consensus 정리
- [카르노맵(Karnaugh Map)](boolean_algebra.md) - Min-term(SOP)/Max-term(POS), 2/3/4/5변수 맵, Don't Care(X), 인접 그룹화
- [카르노맵 간소화](boolean_algebra.md) - 1/2/4/8셀 그룹, 순환 그룹, Essential Prime Implicant
- [퀸-맥클러스키](boolean_algebra.md) - 다변수 간소화, 표 형식, Prime Implicant, 정형화된 방법
- [논리 게이트](and_gate.md) - AND(A·B)/OR(A+B)/NOT(Ā)/NAND(NAND=NAND-NOT, NOT-AND)/NOR/XOR(⊕)/XNOR(⊙)
- [범용 게이트](and_gate.md) - NAND만으로 모든 논리 구현/NOT(NAND 단독)/AND(NAND-NAND)/OR(NOT-NAND-NOT)
- [NAND vs NOR](and_gate.md) - NAND(CMOS 4T, 빠름)/NOR(CMOS 4T, 느림), CMOS 게이트 설계
- [조합 논리 회로](boolean_algebra.md) - 출력이 현재 입력에만 의존, 상태 없음, 게이트 조합
- [반가산기(Half Adder)](alu.md) - 1비트 덧셈, S=A⊕B, C=A·B, 입력 2개(1비트)
- [전가산기(Full Adder)](alu.md) - 1비트 덧셈+올림수 입력, S=A⊕B⊕Cin, Cout=AB+BCin+ACin, 2 Half Adder+OR
- [병렬 가산기(Ripple Carry Adder)](alu.md) - N개 전가산기 직렬 연결, 올림수 전파(Ripple), 지연 누적
- [올림수 예측 가산기(CLA)](alu.md) - Carry Look-Ahead, P(전파)=A+B, G(생성)=AB, 병렬 올림수 계산, 2-level 게이트
- [감산기(Subtractor)](alu.md) - 반감산기/전감산기, 2의 보수 활용 덧셈으로 뺄셈
- [비교기(Comparator)](alu.md) - A>B/A<B/A=B, 가산기 변형, MSB 비교→LSB 전파
- [멀티플렉서(MUX)](boolean_algebra.md) - 2ⁿ:1 선택, 데이터 선택기, 주소 입력(S), 출력 1개, 스위치 네트워크
- [디멀티플렉서(DEMUX)](boolean_algebra.md) - 1:2ⁿ 분배, 데이터 분배기, MUX 역방향, 출력 2ⁿ개 중 1개만 활성
- [디코더(Decoder)](boolean_algebra.md) - n:2ⁿ, 이진→1-hot, 입력 조합별 고유 출력, 인에이블(Enable)
- [인코더(Encoder)](boolean_algebra.md) - 2ⁿ:n, 1-hot→이진, 우선순위 인코더(Priority Encoder), 유효 비트
- [순서 논리 회로](flip_flop.md) - 출력이 현재 입력+이전 상태에 의존, 상태(메모리) 존재, 클럭 동기화
- [래치(Latch)](flip_flop.md) - 레벨 트리거, SR 래치(Set-Reset, 무효 상태 S=R=1)/D 래치(투명, Q추적)
- [플립플롭(Flip-Flop)](flip_flop.md) - 엣지 트리거, 클럱 상승/하강 에지에서만 상태 변경
- [플립플롭 종류](flip_flop.md) - RS JK(무효 상태 해결, J=K=1 토글)/D(데이터 저장)/T(토글, T 입력)
- [플립플롭 특성표](flip_flop.md) - 진리표/상태 전이표/상태 전이 다이어그램/여기 표/다음 상태 논리
- [레지스터](register.md) - N비트 데이터 저장, D 플립플롭 N개 병렬, 병렬 로드/스토어
- [시프트 레지스터](register.md) - 직렬 입력/병렬 출력(SISO)/병렬 입력/직렬 출력(PISO)/양방향(PIPO, Bidirectional)
- [카운터(Counter)](register.md) - 비동기(리플, Asynchronous)/동기(Synchronous)/링(Ring)/존슨(Johnson)/업-다운(Up-Down)
- [비동기 카운터](register.md) - 리플 카운터, 플립플롭 출력→다음 클럭, 전파 지연
- [동기 카운터](register.md) - 공통 클럭, 병렬 올림수, 빠름, 복잡한 게이트
- [ALU(Arithmetic Logic Unit)](alu.md) - 산술(ADD/SUB/MUL/DIV)/논리(AND/OR/XOR/NOT)/시프트/비교 연산, 연산 선택
- [ALU 구조](alu.md) - 피연산자 입력(A/B)/제어 입력(Operation Select)/결과 출력(Status Flags: Z/C/N/V)
- [PLA/FPGA](boolean_algebra.md) - PLA(AND-OR 고정)/FPGA(LUT 기반, 재구성 가능), 프로그래머블 논리
- [FPGA 구조](boolean_algebra.md) - CLB(Configurable Logic Block, LUT+플립플롭)/IOB/BRAM/DSP Block/인터커넥트
- [LUT(Look-Up Table)](boolean_algebra.md) - 진리표 메모리화, 입력→출력 매핑, N입력 LUT=2^N 비트

### 마이크로 구조
- [주소 지정 방식(Addressing Mode)](addressing_mode.md) - 오퍼랜드 위치 결정, 명령어 길이 vs 실행 시간 트레이드오프
- [즉시 주소 지정(Immediate)](addressing_mode.md) - 오퍼랜드=상수, 메모리 접근 없음, 빠름, 값 범위 제한
- [직접 주소 지정(Direct)](addressing_mode.md) - 오퍼랜드=유효 주소, 메모리 1회 접근, 주소 범위 제한(짧은 주소)
- [간접 주소 지정(Indirect)](addressing_mode.md) - 오퍼랜드→유효 주소→데이터, 메모리 2회 접근, 넓은 주소 범위
- [레지스터 주소 지정(Register)](addressing_mode.md) - 오퍼랜드=레지스터 번호, 메모리 접근 없음, 매우 빠름
- [레지스터 간접(Register Indirect)](addressing_mode.md) - 레지스터→유효 주소→데이터, 포인터, 배열 순회
- [변위 주소 지정(Displacement)](addressing_mode.md) - 레지스터+변위(Offset), 상대(PC+Offset)/베이스(Base+Offset)/인덱스(Index+Offset)
- [상대 주소 지정(Relative)](addressing_mode.md) - PC+Offset, 분기 명령어, 위치 독립 코드(Position Independent)
- [인덱스 주소 지정(Indexed)](addressing_mode.md) - 베이스+인덱스 레지스터, 배열 접근, 자동 증가/감소
- [레지스터 종류](register.md) - PC(프로그램 카운터, 다음 명령어 주소)/IR(명령어 레지스터, 현재 명령어)/MAR(메모리 주소)/MDR(메모리 데이터)
- [특수 레지스터](register.md) - SP(스택 포인터)/FP(프레임 포인터)/PSW(상태 워드, Z/N/C/V)/MAR/MBR
- [범용 레지스터](register.md) - R0~R31(RISC-V)/EAX/EBX/ECX/EDX(x86), 호출자/피호출자 저장, 윈도우
- [부동 소수점(Floating Point)](floating_point.md) - IEEE 754 표준, 단정밀도(32비트, 7+8+23)/배정밀도(64비트, 1+11+52), 반정밀도(16비트)
- [IEEE 754 구조](floating_point.md) - 부호(S, 1비트)/지수(E, 8비트, Bias=127)/가수(M, 23비트, Hidden 1), 정규화
- [부동 소수점 특수값](floating_point.md) - ±0/±∞(지수 전부 0/1)/NaN(Not a Number, 가수≠0)/비정규화(지수=0, 가수≠0)
- [반올림 모드](floating_point.md) - Round to Nearest(기본)/Toward Zero/Toward +∞/Toward -∞, Banker's Rounding
- [부동 소수점 예외](floating_point.md) - 오버플로우(Overflow)/언더플로우(Underflow)/부정확(Inexact)/무효 연산(Invalid)
- [고정 소수점(Fixed Point)](floating_point.md) - 부호-크기/1의 보수/2의 보수, 정수 범위 내 소수 표현, 정밀도 제한
- [2의 보수 연산](floating_point.md) - 음수 표현, 뺄셈=덧셈, 오버플로우(Carry Out) 무시
- [데이터 표현](floating_point.md) - BCD(10진, 4비트)/그레이 코드(1비트 변화)/ASCII(7비트)/유니코드(UTF-8/16/32)
- [엔디안(Endianness)](floating_point.md) - 빅 엔디안(MSB 우선, 네트워크)/리틀 엔디안(LSB 우선, x86), 바이트 순서

### 컴퓨터 유형 / 특수 프로세서
- [폰 노이만 vs 하버드 구조](von_neumann_harvard.md) - 통합 메모리(폰노이만 병목)/분리 메모리(명령어·데이터), 현대는 하버드+캐시
- [Modified Harvard](von_neumann_harvard.md) - L1 분리(I/D)/L2/L3 통합, 메모리 계층에서 결합
- [양자 컴퓨터](quantum_computer.md) - 큐비트(Qubit, 0과 1 동시), 중첩(Superposition)/얽힘(Entanglement)/간섭(Interference)
- [양자 게이트](quantum_computer.md) - Hadamard(중첩)/CNOT(얽힘)/Pauli-X/Y/Z/Phase/Toffoli, 양자 회로
- [양자 오류 수정](quantum_computer.md) - 표면 코드(Surface Code)/논리 큐비트, 오류 임계값, QEC
- [양자 우위(Quantum Supremacy)](quantum_computer.md) - Sycamore(Google, 2019)/Zuchongzhi(중국), 난수 생성
- [양자 알고리즘](quantum_computer.md) - Shor(소인수분해, 위협)/Grover(검색, √N)/QAOA(최적화)
- [뉴로모픽 칩](ai_accelerator.md) - 스파이킹 신경망(SNN), 이벤트 기반, 초저전력, Intel Loihi/IBM TrueNorth
- [하이브리드 컴퓨터](hybrid_computer.md) - 아날로그(연속)+디지털(이산), 시뮬레이션, 제어 시스템
- [ENIAC](eniac.md) - 최초 전자식 컴퓨터(1946), 10진수, 플러그보드 프로그래밍, 진공관 17,468개
- [컴퓨터 세대](eniac.md) - 1세대(진공관)/2세대(트랜지스터)/3세대(IC)/4세대(VLSI)/5세대(초LSI, AI)
- [DSP(Digital Signal Processor)](dsp.md) - 실시간 신호 처리, MAC(Multiply-Accumulate) 연산 최적화, 하버드 구조
- [DSP 응용](dsp.md) - 오디오/영상/통신(OFDM)/레이더, FFT/FIR/IIR 필터
- [MCU vs MPU](mcu_mpu.md) - MCU(마이크로컨트롤러, SoC, 임베디드)/MPU(마이크로프로세서, 범용, 외부 메모리)
- [MCU 구조](mcu_mpu.md) - CPU+Flash+SRAM+GPIO+ADC+UART+SPI+I2C+타이머, 저전력, 실시간
- [임베디드 시스템](mcu_mpu.md) - 특수 목적, RTOS(실시간 OS), 펌웨어, 크로스 컴파일, 제약(전력/메모리/비용)
- [엣지 AI 칩](ai_accelerator.md) - 온디바이스 추론, 저전력 NPU, TinyML, 모바일/임베디드
- [ASIC vs FPGA](boolean_algebra.md) - ASIC(주문형, 고성능, 고비용, 변경 불가)/FPGA(재구성, 유연, 개발 비용↓)
- [칩렛 아키텍처](multiprocessor.md) - 이종 다이(Chiplet) 통합, UCIe(Universal Chiplet Interconnect), 2.5D/3D 패키징
- [칩렛 장점](multiprocessor.md) - 수율 향상/유연한 구성/비용 절감, 다양한 공정 혼합, EMIB/CoWoSE/TSV
