+++
title = "2. 운영체제"
description = "프로세스 관리, 메모리 관리, 파일 시스템, 동기화, 가상화"
sort_by = "title"
weight = 2
+++

# 제2과목: 운영체제

운영체제의 핵심 개념과 자원 관리 기법을 다룹니다.

## 핵심 키워드

### OS 기초 / 구조
- [운영체제 개요](process.md) - OS 정의, 역할(자원관리/인터페이스), 발전 과정
- [운영체제 구조](process.md) - 모놀리식/마이크로커널/하이브리드/엑소커널, 계층 구조
- [시스템 콜](process.md) - 사용자→커널 전환(Trap), fork/exec/wait, 시스템 콜 인터페이스
- [커널 모드/사용자 모드](process.md) - 이중 동작 모드, 특권 명령어, 모드 전환
- [POSIX](file_system.md) - 표준 OS 인터페이스, 이식성 보장
- [리눅스 커널](process.md) - 커널 모듈, proc 파일시스템, init/systemd

### 프로세스 관리
- [프로세스](process.md) - 상태 전이(New/Ready/Running/Waiting/Terminated), PCB (프로세스 제어 블록)
- [프로세스 생성/종료](process.md) - fork(), exec(), exit(), wait(), 좀비/고아 프로세스
- [스레드](thread.md) - 사용자/커널 스레드, 다대일/일대일/다대다 매핑 모델
- [멀티스레딩](thread.md) - 경량 프로세스, POSIX 스레드(Pthreads)
- [컨텍스트 스위칭](process.md) - 오버헤드, PCB 저장/복원, 문맥 교환 비용
- [코루틴/파이버](thread.md) - 협력적 멀티태스킹, 비선점적 스케줄링

### CPU 스케줄링
- [CPU 스케줄링 기본](cpu_scheduling.md) - 선점형(Preemptive, 시간 할당량, 인터럽트)/비선점형(Non-preemptive, 자발적 양보)
- [스케줄링 큐](cpu_scheduling.md) - Job Queue(전체)/Ready Queue(CPU 대기)/Wait Queue(I/O 대기), 다단계 큐
- [디스패처(Dispatcher)](cpu_scheduling.md) - 스케줄러 선택→실제 문맥 교환, 모드 전환, 디스패치 지연(Dispatch Latency)
- [스케줄링 기준](cpu_scheduling.md) - CPU 이용률/처리량(Throughput)/반환시간(Turnaround)/대기시간(Waiting)/응답시간(Response)
- [스케줄링 목표](cpu_scheduling.md) - 공정성(Fairness)/효율성(Efficiency)/응답성(Response)/처리량(Throughput) 최적화
- [FCFS(First-Come First-Served)](cpu_scheduling.md) - 비선점, 도착 순서, 호위 효과(Convoy Effect, 긴 작업 뒤 대기)
- [SJF(Shortest Job First)](cpu_scheduling.md) - 비선점, 최단 작업 우선, 평균 대기시간 최소, 실행 시간 예측 문제
- [SRTF(Shortest Remaining Time First)](cpu_scheduling.md) - SJF 선점형, 남은 시간 최소 우선, 잦은 문맥 교환
- [Round Robin(RR)](cpu_scheduling.md) - 선점, 시간 할당량(Time Quantum, 10~100ms), 돌아가며 실행, 시분할(Time-Sharing)
- [RR 타임 퀀텀](cpu_scheduling.md) - 너무 작음(문맥 교환 오버헤드↑)/너무 큼(FCFS처럼 동작), 응답성 vs 오버헤드
- [우선순위 스케줄링(Priority)](cpu_scheduling.md) - 정적(고정)/동적(에이징 Aging) 우선순위, 기아(Starvation)/에이징 해결
- [다단계 큐(MLQ)](cpu_scheduling.md) - 우선순위별 큐 분리(Foreground/Background), 각 큐별 스케줄링 알고리즘, 큐 간 이동 없음
- [다단계 피드백 큐(MLFQ)](cpu_scheduling.md) - MLQ + 큐 간 이동, 오래 실행→낮은 우선순위, I/O 중심→높은 우선순위, 동적 조정
- [MLFQ 파라미터](cpu_scheduling.md) - 큐 수/우선순위/타임 퀀텀(높은 큐일수록 작게), 에이징/강등/승격 규칙
- [HRN(Highest Response Ratio Next)](cpu_scheduling.md) - (대기시간+실행시간)/실행시간, SJF 기아 해결, 비선점
- [실시간 스케줄링](cpu_scheduling.md) - 경성(Hard, 데드라인 필수)/연성(Soft, 데드라인 권장), EDF/RMS
- [EDF(Earliest Deadline First)](cpu_scheduling.md) - 동적, 데드라인 임박 순서, 최적(단일 CPU), 과부하 시 예측 불가
- [RMS(Rate Monotonic Scheduling)](cpu_scheduling.md) - 정적, 주기 짧을수록 높은 우선순위, 주기적 태스크, 이론적 한계(69% 활용률)
- [CFS(Completely Fair Scheduler)](cpu_scheduling.md) - 리눅스 기본, vruntime(가상 실행시간) 기반, Red-Black Tree, 완전 공정성
- [CFS 동작](cpu_scheduling.md) - vruntime 작은 태스크 우선, min_vruntime, 타임슬라이스 동적 할당, nice 값
- [Linux 스케줄러](cpu_scheduling.md) - CFS(SCHED_NORMAL)/RT(SCHED_FIFO, SCHED_RR)/Deadline, cgroups
- [CPU-bound vs I/O-bound](cpu_scheduling.md) - CPU 집중(긴 버스트, I/O 드묾)/I/O 집중(짧은 버스트, I/O 빈번), 스케줄링 전략

### 동기화 / 상호배제
- [동기화 문제](synchronization.md) - 임계 구역(Critical Section, 경쟁 조건(Race Condition), 데이터 일관성 깨짐
- [상호배제(Mutual Exclusion)](synchronization.md) - 한 순간에 하나의 프로세스만 임계 구역 진입
- [진행(Progress)](synchronization.md) - 임계 구역 밖 대기 중인 프로세스가 진입 가능
- [한정 대기(Bounded Waiting)](synchronization.md) - 기아(Starvation) 방지, 진입 보장
- [피터슨 알고리즘](synchronization.md) - 2개 프로세스 상호배제, turn/plag 변수, 하드웨어 없이 구현
- [데커 알고리즘](synchronization.md) - 2개 프로세스, 3-state 플래그(turn/wait), 바쁜 응답
- [뮤텍스(Mutex)](synchronization.md) - 이진 세마포어, 잠금(Lock)/해제(Unlock), 소유권(Ownership), 재진입 불가
- [뮤텍스 vs 세마포어](synchronization.md) - 뮤텍스(소유권, 재진입 X)/세마포어(소유권 X, 카운팅, 시그널 방식)
- [세마포어](synchronization.md) - 이진(Binary, 0/1)/카운팅(Counting, 0~N), P(wait/down)/V(signal/up) 연산
- [P/V 연산](synchronization.md) - P: 값>0이면 대기, 아니면 값 감소/V: 값<최대이면 증가, 아니면 wakeup 대기 프로세스
- [세마포어 구현](synchronization.md) - 정수 변수 + P/V 함수 + 원자성 보장, busy-wait(스핀락) 또는 block(블로킹)
- [모니터(Monitor)](synchronization.md) - 추상화된 동기화, 조건 변수(Condition Variable), wait/signal/broadcast
- [모니터 구조](synchronization.md) - 공유 데이터 + 연산(프로시저) + 조건 변수 큐 + 진입/출구 큐
- [모니터 vs 세마포어](synchronization.md) - 모니터(캡슐화, 조건 변수)/세마포어(저수준, busy-wait 가능)
- [스핀락(Spinlock)](synchronization.md) - Busy-Waiting, 락 획득 시까지 루프, 멀티프로세서/실시간에 적합
- [스핀락 변형](synchronization.md) - Ticket Lock(순서 부여)/MCS Lock(다중 코어)/RTM(Read-Copy-Update)
- [Lock-free 자료구조](synchronization.md) - CAS(Compare-And-Swap)/LL/SC(Linked List), 원자적 연산
- [생산자-소비자 문제](synchronization.md) - 유한 버퍼, 생산자(데이터 생성)/소비자(데이터 사용), Empty/Full 동기화
- [생산자-소비자 해법](synchronization.md) - 3개 세마포어(mutex/empty/full) 또는 2개(binary mutex + counting), N缓冲 크기
- [판독자-기록자 문제](synchronization.md) - Readers(동시 읽기)/Writers(배타적 쓰기), Read-priority/Write-priority
- [판독자-기록자 해법](synchronization.md) - read-count/write-count 세마포어, 기록자 굶주
- [식사하는 철학자 문제](synchronization.md) - 5명 철학자, 5개 포크, 교착상태(Deadlock) 발생 가능
- [식사 철학자 해법](synchronization.md) - 자원 계층(순서 부여)/포크 짝수/시도-실패 후 해제/중앙 코디네이터
- [Dining Philosophers 교착상태](synchronization.md) - 각 철학자가 왼쪽 포크 획득 후 오른쪽 포크 대기 → 전원 대기

### 교착상태 (Deadlock)
- [교착상태(Deadlock)](deadlock.md) - 두 프로세스 이상이 서로의 자원을 대기하며 무한 대기, 진전(Progress) 불가
- [시스템 모델](deadlock.md) - 자원(Resource) 타입(가변/고정 수량), 할당 그래프, 자원 인스턴스
- [교착상태 4조건(Coffman)](deadlock.md) - 상호배제/점유대기/비선점/순환대기, 4가지 동시 성립 필수
- [상호배제(Mutual Exclusion)](deadlock.md) - 자원은 한 번에 한 프로세스만 사용
- [점유대기(Hold and Wait)](deadlock.md) - 자원 보유 + 다른 자원 대기
- [비선점(No Preemption)](deadlock.md) - 자원 강제 회수 불가
- [순환대기(Circular Wait)](deadlock.md) - 대기 사이클 P1→P2→...→Pn→P1
- [자원 할당 그래프(RAG)](deadlock.md) - 프로세스(원)/자원(사각형), 요청/할당 간선, 사이클=교착상태
- [교착상태 처리 전략](deadlock.md) - 예방(Prevention)/회피(Avoidance)/탐지(Detection)/복구(Recovery)
- [교착상태 예방(Prevention)](deadlock.md) - 4조건 중 하나 부정, 순환대기→자원 순서 부여
- [교착상태 회피(Avoidance)](deadlock.md) - 안전 상태(Safe State)/불안전 상태, 은행원 알고리즘(Banker's Algorithm)
- [은행원 알고리즘](deadlock.md) - 가용 자원(Available)/최대需求(Max)/할당(Allocation)/필요(Need), 안전 순서(Safe Sequence)
- [교착상태 탐지(Detection)](deadlock.md) - 대기 그래프(Wait-For Graph), 주기적 검사, 오버헤드
- [교착상태 복구(Recovery)](deadlock.md) - 프로세스 종료(희생자 선택)/자원 선점/롤백(Checkpoint-Restart)
- [기아(Starvation)](deadlock.md) - 특정 프로세스가 무한 대기, 에이징(Aging)으로 해결
- [라이브락(Livelock)](deadlock.md) - 프로세스가 상태 변경하지만 진전 없음, 서로 양보 반복
- [Deadlock vs Starvation vs Livelock](deadlock.md) - Deadlock(블록됨)/Starvation(일부만 굶주림)/Livelock(바쁜 대기)

- [현대 OS 교착상태](deadlock.md) - 탐지/복구보다 예방/회피 거의 안 함, 재부팅/OOM Killer가 사실상 복구

### 메모리 관리
- [주소 바인딩](memory.md) - 논리 주소(가상, 0부터 시작)→물리 주소(실제, 프레임 번호+오프셋) 변환
- [바인딩 시점](memory.md) - 컴파일(Compile, 절대 코드)/적재(Load, 재배치 로더)/실행(Execution, MMU)
- [MMU(Memory Management Unit)](memory.md) - 재배치 레지스터(Base/Limit)/TLB/페이지 테이블, 하드웨어 주소 변환
- [메모리 할당 전략](memory.md) - First Fit(최초, 빠름)/Best Fit(최적, 단편화↓)/Worst Fit(최악, 큰 공간 활용)
- [단편화(Fragmentation)](memory.md) - 외부(External, 할당 안 됨)/내부(Internal, 할당 내 남음)
- [외부 단편화 해결](memory.md) - 컴팩션(Compaction, 메모리 압축)/페이징(Paging)/세그멘테이션(Segmentation)
- [내부 단편화 해결](memory.md) - 슬랩 할당(Slab Allocator)/페이지 크기 최적화/Huge Pages
- [페이징(Paging)](memory.md) - 고정 크기 페이지(Page, 4KB~2MB)/프레임(Frame), 내부 단편화만 존재
- [페이지 테이블(Page Table)](memory.md) - PTE(Page Table Entry), Valid/Dirty/Reference/Access 비트, 주소 변환
- [다단계 페이지 테이블](memory.md) - 2-level/3-level, 페이지 테이블 공간 절약, 메모리 접근 ↑
- [역페이지 테이블(Inverted)](memory.md) - 물리 프레임당 1 엔트리, 시스템 전체 1개, PID+페이지 번호로 검색
- [해시 페이지 테이블](memory.md) - 해시 함수로 PTE 위치, 역페이지 테이블 검색 가속
- [TLB(Translation Lookaside Buffer)](memory.md) - 최근 주소 변환 캐시, 64~128 엔트리, 99%+ 히트율
- [페이지 크기](memory.md) - 4KB(기본)/2MB/1GB(Huge Pages), 크기↑=내부 단편화↑/테이블 크기↓/TLB 효율↑
- [세그멘테이션(Segmentation)](memory.md) - 논리 단위 분할(Code/Data/Stack/Heap), 가변 길이, 외부 단편화
- [세그먼트-페이지 혼합](memory.md) - 세그먼트 내 페이징, 외부 단편화 해결 + 논리적 구조 유지
- [페이지 교체(Page Replacement)](page_replacement.md) - 페이지 부재(Page Fault) 시 희생 프레임 선택
- [FIFO(First-In-First-Out)](page_replacement.md) - 들어온 순서대로 교체, Belady's Anomaly(프레임↑=부재↑ 가능)
- [LRU(Least Recently Used)](page_replacement.md) - 최근 사용 시간 기반, 근사, Belady's Anomaly 없음
- [LFU(Least Frequently Used)](page_replacement.md) - 사용 빈도 기반, 새 페이지 불리
- [Clock(NRU/Second Chance)](page_replacement.md) - Reference 비트 활용, FIFO+참조 비트, 순환 큐
- [SCR(Second Chance Replacement)](page_replacement.md) - Reference=1이면 0으로, 다음 검사/Reference=0이면 교체
- [Optimal(OPT/MIN)](page_replacement.md) - 앞으로 가장 오랫동안 안 쓸 페이지 교체, 이론적 최적, 구현 불가
- [Working Set Model](memory.md) - 시간 윈도우 내 접근한 페이지 집합, 지역성(Locality) 기반
- [PFF(Page Fault Frequency)](memory.md) - 페이지 부재율 기반 프레임 할당, 부재율↑=프레임↑/부재율↓=프레임↓
- [스래싱(Thrashing)](memory.md) - 과도한 페이지 교환, CPU 이용률 급락, 디스크 I/O 급증
- [스래싱 원인/해결](memory.md) - 프레임 부족/원인, 워킹셋 모델/PFF/지역 교체/프로세스 일시 중지
- [Copy-on-Write(COW)](memory.md) - 페이지 공유, 쓰기 시 복사, fork() 최적화
- [메모리 오버커밋(Overcommit)](memory.md) - 물리 메모리 초과 할당, 페이지 공유/지연 할당, OOM Killer
- [OOM(Out of Memory) Killer](memory.md) - 메모리 부족 시 프로세스 종료, badness 젞수, 희생자 선택

### 파일 시스템
- [파일 시스템 구조](file_system.md) - 부트 블록/슈퍼블록/아이노드 블록/데이터 블록, 블록 크기(4KB/8KB/64KB)
- [inode(Inode)](file_descriptor.md) - 파일 메타데이터(크기/권한/타임스탬프/블록 포인터), 하드링크/식볼릭 링크, inode 번호
- [inode 구조](file_descriptor.md) - 128B~256B, 직접 블록(12개)/간접 블록(1단계/2단계/3단계), inode 테이블
- [디렉터리 구조](file_system.md) - 단일/이중/트리(Absolute Path)/비순환 그래프(심볼릭 링크)/일반 그래프(순환, 허용/미허용)
- [디렉터리 엔트리](file_system.md) - 파일명+inode 번호(dentry), 경로 해석(Path Resolution), dcache
- [파일 할당 방법](file_system.md) - 연속(순차, 빠름/외부 단편화)/연결(Linked, 비순차/포인터 오버헤드)/색인(Indexed, inode 기반, ext4)
- [Ext4 할당](file_system.md) - extent tree(블록 그룹), 딜레이 할당/사전 할당, 단편화 최소화
- [파일 시스템 비교](file_system.md) - FAT32(단순, 4GB)/NTFS(저널, ACL)/EXT4(extent, 저널)/APFS(Apple SSD)/ZFS(COW, RAID)/XFS(고성능)
- [저널링 파일 시스템](file_system.md) - 메타데이터 저널/전체 데이터 저널, Ordered Mode/Writeback Mode
- [저널링 동작](file_system.md) - 트랜잭션 시작→메타데이터 기록→데이터 기록→커밋, 크래시 복구
- [Copy-on-Write(COW)](file_system.md) - 쓰기 시 새 블록 할당, 원본 유지, 스냅샷, ZFS/Btrfs
- [파일 시스템 일관성](file_system.md) - fsck(검사/복구)/Journal Replay/Soft/Hard Link
- [파일 보호](file_system.md) - 접근 행렬(Access Matrix)/ACL(POSIX)/DAC/MAC(SELinux)/Capability
- [파일 권한](file_system.md) - rwx(읽기/쓰기/실행)/소유자(Owner)/그룹(Group)/기타(Others)/SetUID/SetGID/Sticky Bit
- [특수 권한 비트](file_system.md) - SetUID(실행 시 소유자 권한)/SetGID(실행 시 그룹 권한)/Sticky(삭제 제한, /tmp)
- [마운트(Mount)](file_system.md) - 파일 시스템 트리에 연결, bind mount/overlayfs/unionfs/fuse
- [파티션(Partition)](file_system.md) - MBR(4 partition, 2TB 제한)/GPT(128 partition, 9.4ZB)/LVM(논리 볼륨, 동적 확장)
- [LVM(Logical Volume Manager)](file_system.md) - PV(물리 볼륨)/VG(볼륨 그룹)/LV(논리 볼륨), 스냅샷, 리사이징
- [RAID 파일 시스템](file_system.md) - mdadm(소프트웨어 RAID)/ZFS(RAID-Z)/Btrfs(프로파일)/LVM-RAID

### 입출력 관리
- [I/O 서브시스템 계층](buffer.md) - 사용자 영역(시스템 콜)→커널(VFS/파일 시스템)→블록 계층→드라이버→장치
- [장치 드라이버](buffer.md) - 블록 장치(랜덤 접근, 디스크)/문자 장치(순차 접근, 터미널), 인터럽트/Polling
- [장치 파일](buffer.md) - /dev/sda(블록)/dev/tty(문자), Major/Minor 번호, udev
- [버퍼링](buffer.md) - 단일 버퍼/이중 버퍼/순환 버퍼(Circular), 사용자↔커널 버퍼
- [스풀링(Spooling)](buffer.md) - 디스크를 이용한 버퍼링, 프린터 큐, 디스크 공유
- [동기/비동기 I/O](process.md) - Blocking(대기)/Non-Blocking(즉시 반환)/Asynchronous(완료 시 알림)
- [I/O 멀티플렉싱](process.md) - select(비트마스크, FD_SETSIZE)/poll(구조체)/epoll(이벤트, Edge/Level)/kqueue(BSD)
- [epoll 동작](process.md) - epoll_create/epoll_ctl/epoll_wait, LT(Level Triggered)/ET(Edge Triggered)
- [Zero-Copy I/O](buffer.md) - sendfile(커널→커널 직접)/splice/mmap(DMA), CPU 개입 최소화
- [디스크 I/O 스케줄러](buffer.md) - CFQ(공정)/BFQ(저지연)/deadline(실시간)/mq-deadline/none(NVMe)
- [디스크 캐시](buffer.md) - Page Cache(파일)/Buffer Cache(블록), Read-ahead, Dirty Write-back
- [Direct I/O](buffer.md) - 캐시 우회, O_DIRECT, 데이터베이스/자체 캐시

### 가상화 / 컨테이너
- [가상화 유형](virtualization.md) - 전가상화(Full, HVM)/반가상화(Para, 커널 수정)/하드웨어 지원(AMD-V/Intel VT-x)
- [하이퍼바이저](virtualization.md) - Type 1(Bare-metal, ESXi/Hyper-V)/Type 2(Hosted, VirtualBox/VMware Workstation)
- [가상화 기술](virtualization.md) - EPT/NPT(Extended/Nested Page Table)/VPID/TLB, IOMMU/SR-IOV
- [KVM(Kernel-based Virtual Machine)](virtualization.md) - 리눅스 커널 모듈, /dev/kvm, QEMU(사용자 공간 에뮬레이션)
- [Xen](virtualization.md) - Dom0(특권)/DomU(게스트), PV/HVM/PVHVM, Paravirtualized I/O
- [컨테이너(Container)](virtualization.md) - OS 수준 가상화, 공유 커널, 리소스 격리, Docker/Podman/LXC
- [컨테이너 격리](virtualization.md) - Namespaces(PID/NET/MNT/IPC/UTS/USER/Cgroup)/Capabilities/Seccomp
- [Namespace 종류](virtualization.md) - PID(프로세스)/NET(네트워크)/MNT(마운트)/IPC(System V IPC)/UTS(호스트명)/USER(UID/GID)/TIME/CGROUP
- [cgroup(Control Group)](virtualization.md) - 자원 제한(CPU/메모리/IO)/우선순위/모니터링, cgroup v1/v2
- [cgroup 컨트롤러](virtualization.md) - cpu/cpuacct/cpuset/memory/blkio/pids/hugetlb, 계층적 그룹
- [컨테이너 런타임](virtualization.md) - OCI(Open Container Initiative)/runc(containerd)/CRI-O(Kubernetes)/Podman(daemonless)
- [컨테이너 vs VM](virtualization.md) - 컨테이너(초기화 빠름, 밀도 높음, 격리 약함)/VM(완전 격리, 무겁, 독립 커널)
- [WASM(Wasmtime/Wasmer)](virtualization.md) - WebAssembly System Interface(WASI), 샌드박스, 이식성, 경량
- [Unikernel](virtualization.md) - 단일 주소 공간, 라이브러리 OS, 특화 VM, MirageOS/IncludeOS

### 보안 / 보호
- [보호 링(Protection Ring)](process.md) - Ring 0(커널)/Ring 1/2(드라이버)/Ring 3(사용자), CPL(Current Privilege Level)
- [사용자/커널 경계](process.md) - 시스템 콜(Trap)/인터럽트/예외, 모드 전환, Kernel Mode/User Mode
- [ASLR(Address Space Layout Randomization)](synchronization.md) - 주소 난수화, 스택/힙/라이브러리 위치, RTL(Return-Oriented Programming) 방어
- [DEP/NX(Data Execution Prevention)](synchronization.md) - 데이터 실행 방지  W^X(Write XOR eXecute), NX 비트
- [Stack Canary](synchronization.md) - 스택 버퍼 오버플로우 탐지, __stack_chk_fail, 임의 값, Return 주소 보호
- [SELinux/AppArmor](synchronization.md) - MAC(Mandatory Access Control)/Domain/Type Enforcement/Profile 기반
- [접근 제어 모델](file_system.md) - DAC(임의)/MAC(강제)/RBAC(역할)/ABAC(속성)/Capability
- [RBAC(Role-Based Access Control)](file_system.md) - Role/Permission/Operation/Object, 최소 권한 원칙

### 실시간 / 분산 / 최신 OS
- [실시간 운영체제 (RTOS)](process.md) - 경성/연성 실시간, 태스크 스케줄링, VxWorks, FreeRTOS
- [분산 운영체제](process.md) - 투명성(접근/위치/이주/복제), 분산 파일 시스템(NFS, GFS)
- [IPC (프로세스 간 통신)](ipc.md) - 공유메모리, 메시지 큐, 파이프(익명/이름있는), 소켓, 시그널
- [eBPF](ebpf_runtime.md) - 커널 수준 프로그래밍, 추적/보안/네트워킹/관찰성
- [프로그램 카운터](program_counter.md) - PC 레지스터 역할, 명령어 흐름 제어
- [서버리스 실행 환경](virtualization.md) - FaaS 기반, Cold Start 최소화
