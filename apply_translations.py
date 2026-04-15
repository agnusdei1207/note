import os
import re

dirs = [
    "content/studynote/1_computer_architecture",
    "content/studynote/2_operating_system",
    "content/studynote/3_network",
    "content/studynote/4_software_engineering"
]

# Provide a comprehensive translation dictionary for technical terms
translations = {
    "Biometric Sensor": "생체 센서",
    "Encrypted Secure Path": "암호화된 보안 경로",
    "SEP Crypto Engine": "SEP 암호 엔진",
    "Reference Template": "참조 템플릿",
    "Matching Algorithm": "매칭 알고리즘",
    "SEP Microprocessor": "SEP 마이크로프로세서",
    "Score Calculation": "점수 계산",
    "Rich OS (AP)": "리치 OS (AP)",
    "Decision Logic": "결정 로직",
    "Power On": "전원 켜기",
    "Hardware ROM Boot": "하드웨어 ROM 부팅",
    "Secure Enclave Firmware": "Secure Enclave 펌웨어",
    "Initialize Crypto Engine": "암호 엔진 초기화",
    "Main OS Bootloader": "메인 OS 부트로더",
    "Verify Signature": "서명 확인",
    "Verify Kernel": "커널 확인",
    "Secure Enclave OS": "Secure Enclave OS",
    "Rich OS Running": "리치 OS 실행 중",
    "Complex Equation": "복잡한 방정식",
    "Karnaugh Map": "카르노 맵",
    "Minimized": "최소화됨",
    "Benefits": "이점",
    "Fewer Gates -> Lower Chip Area (Cost ↓)": "더 적은 게이트 -> 칩 면적 감소 (비용 ↓)",
    "Shorter Paths -> Higher Speed (Frequency ↑)": "더 짧은 경로 -> 속도 증가 (주파수 ↑)",
    "Less Switching -> Lower Power Consumption (Battery ↑)": "스위칭 감소 -> 전력 소비 감소 (배터리 ↑)",
    "MSB": "최상위 비트",
    "LSB": "최하위 비트",
    "Sign": "부호",
    "Sign (+)": "부호 (+)",
    "7-bit Integer": "7비트 정수",
    "8-bit Fraction": "8비트 소수",
    "Fixed-Point Multiplication (Q8.8 * Q8.8)": "고정 소수점 곱셈",
    "Floating-Point Multiplication (IEEE 754)": "부동 소수점 곱셈",
    "Payload (4 bits): 1 0 1 1": "페이로드 (4비트): 1 0 1 1",
    "The Intersecting Radar Logic (Even Parity Coverage)": "교차 레이더 로직 (짝수 패리티 커버리지)",
    "Receiver Error Checker (Syndrome Calculus)": "수신기 오류 검사기 (신드롬 계산)",
    "Setup for CRC": "CRC 설정",
    "Hardware Polynomial Division (Modulo-2 / XOR)": "하드웨어 다항식 나눗셈",
    "The Perfect Transmission": "완벽한 전송",
    "Receiver Validation": "수신기 검증",
    "A 3-Bit Data World (Cube coordinates x, y, z)": "3비트 데이터 세계",
    "Scenario: Cosmic Ray flips ONE bit of 000": "시나리오: 우주선이 000의 한 비트를 뒤집음",
    "The Receiver's Geometry Brain (Correction Logic)": "수신기의 기하학적 뇌 (수정 로직)",
    "Formula: Error Capability": "공식: 오류 기능",
    "Programmed I/O Sequential Execution Step": "프로그램된 I/O 순차 실행 단계",
    "S/W App": "소프트웨어 앱",
    "OS Kernel": "OS 커널",
    "Device Driver": "디바이스 드라이버",
    "MMIO Access": "MMIO 접근",
    "Check Status Reg": "상태 레지스터 확인",
    "Write Data Reg": "데이터 레지스터 쓰기",
    "Parallel Bus": "병렬 버스",
    "Serial PCIe": "직렬 PCIe",
    "Unified CXL Fabric": "통합 CXL 패브릭",
    "Low Speed": "저속",
    "High Throughput": "고처리량",
    "Memory & Cache Coherent": "메모리 및 캐시 일관성",
    "Optimal Point": "최적 지점",
    "User Application": "사용자 애플리케이션",
    "System Call Interface": "시스템 호출 인터페이스",
    "Kernel Mode": "커널 모드",
    "Resource Protection": "리소스 보호",
    "Task Execution": "작업 실행",
    "Source Code": "소스 코드",
    "Executable File": "실행 파일",
    "Memory Space": "메모리 공간",
    "Code": "코드",
    "Data": "데이터",
    "Heap": "힙",
    "Stack": "스택",
    "Physical Memory": "물리 메모리",
    "Process Address Space": "프로세스 주소 공간",
    "Memory Pages": "메모리 페이지",
    "Argv / Env": "인수 / 환경변수",
    "Start Execution": "실행 시작",
    "fork+exec": "fork+exec",
    "fork+COW": "fork+COW",
    "posix_spawn": "posix_spawn",
    "clone3+NS": "clone3+NS",
    "Write Data": "데이터 쓰기",
    "ECC Encoder": "ECC 인코더",
    "Storage": "스토리지",
    "Read Data": "데이터 읽기",
    "ECC Decoder": "ECC 디코더",
    "Syndrome Calc": "신드롬 계산",
    "No Error": "오류 없음",
    "1-bit Error": "1비트 오류",
    "2-bit Error": "2비트 오류",
    "Master A": "마스터 A",
    "Master B": "마스터 B",
    "Master C": "마스터 C",
    "Request A": "요청 A",
    "Request B": "요청 B",
    "Request C": "요청 C",
    "Error Detected": "오류 감지됨",
    "Is it User-space?": "유저 공간인가?",
    "Restart Application / Process": "애플리케이션/프로세스 재시작",
    "Is it Fatal (Panic)?": "치명적인가(패닉)?",
    "Log Oops & Monitor closely": "Oops 로그 및 면밀한 모니터링",
    "User App Event": "사용자 앱 이벤트",
    "CPU Detection": "CPU 감지",
    "Kernel Handler": "커널 핸들러",
    "Is System Critical?": "시스템에 치명적인가?",
    "Terminate Only Process": "프로세스만 종료",
    "Next Proc": "다음 프로세스",
    "Kernel Panic / Halt": "커널 패닉 / 정지",
    "Ready Queue": "준비 큐",
    "CPU Running P1": "P1을 실행하는 CPU",
    "Timer Interrupt": "타이머 인터럽트",
    "Context Switch": "문맥 교환",
    "Save P1, Load P2": "P1 저장, P2 로드",
    "Next Target": "다음 대상",
    "Admin Command": "관리자 명령",
    "Unit File Parsing": "유닛 파일 구문 분석",
    "Dependency Check": "의존성 검사",
    "ExecStart": "ExecStart",
    "Success?": "성공?",
    "Condition Check": "조건 검사",
    "Crash!": "충돌!",
    "Restart Policy?": "재시작 정책?",
    "Stop Command": "정지 명령",
    "SIGTERM": "SIGTERM",
    "SIGKILL": "SIGKILL",
    "Dead": "종료됨",
    "Memory Management Service": "메모리 관리 서비스",
    "Scheduler Service": "스케줄러 서비스",
    "User Session": "사용자 세션",
    "System Session": "시스템 세션",
    "Foreground": "포어그라운드",
    "Background": "백그라운드",
    "Parent: Shell": "부모: 쉘",
    "Parent: PID 1 / init": "부모: PID 1 / init",
    "Process Exit": "프로세스 종료",
    "Infinite Loop": "무한 루프",
    "Start": "시작",
    "Background Job": "백그라운드 작업",
    "Independent": "독립적",
    "New Session": "새 세션",
    "Daemon Ready!": "데몬 준비 완료!",
    "Running State": "실행 상태",
    "HW Auto Save (PC, SP, Flags)": "HW 자동 저장 (PC, SP, 플래그)",
    "User Mode": "사용자 모드",
    "Kernel Mode Transition": "커널 모드 전환",
    "Update PCB with General Regs": "일반 레지스터로 PCB 업데이트",
    "Context Save Routine": "문맥 저장 루틴",
    "Scheduler Selects Next Process": "스케줄러가 다음 프로세스 선택",
    "Context Restore from New PCB": "새 PCB에서 문맥 복원",
    "User Mode Return": "사용자 모드 복귀",
    "iret Instruction": "iret 명령어",
    "HW Auto Restore": "HW 자동 복원",
    "Event: Interrupt / Trap": "이벤트: 인터럽트 / 트랩",
    "Is Scheduler Action Required?": "스케줄러 동작이 필요한가?",
    "Return to Current Process": "현재 프로세스로 복귀",
    "Select Next Process (Policy)": "다음 프로세스 선택 (정책)",
    "Is Address Space Different?": "주소 공간이 다른가?",
    "Heavy": "무거움",
    "Light: Thread Switch": "가벼움: 스레드 전환",
    "Switch Page": "페이지 전환",
    "Maintain MMU": "MMU 유지",
    "Flush TLB*": "TLB 플러시*",
    "Save/Restore Regs": "레지스터 저장/복원",
    "Execute Dispatcher": "디스패처 실행",
    "Resume Execution": "실행 재개",
    "Level 0": "레벨 0",
    "Level 1": "레벨 1",
    "Maintenance": "유지보수",
    "Release": "릴리스",
    "Testing": "테스팅",
    "Code": "코드",
    "Read MMIO": "MMIO 읽기",
    "Write MMIO": "MMIO 쓰기",
    "Disk": "디스크",
    "Fraction": "소수",
    "Exponent - 127": "지수 - 127",
    "Exponent - 1023": "지수 - 1023",
    "Normal": "정상",
    "Denormalized": "비정규화됨",
    "Zero": "0",
    "Not a Number": "숫자가 아님(NaN)",
    "Quiet NaN": "Quiet NaN",
    "Signaling NaN": "Signaling NaN",
    "Loss of Hidden 1": "숨겨진 1 손실",
    "Catastrophe Zone": "재앙 구역",
    "Hardware Interpretation": "하드웨어 해석",
    "Hardware Win": "하드웨어의 승리",
    "Arithmetic Danger": "산술적 위험",
    "Result is not zero": "결과가 0이 아님",
    "Catastrophic Loss of Data": "치명적인 데이터 손실",
    "Loss Scaling": "손실 스케일링",
    "Safe Zone": "안전 구역",
    "1's place": "1의 자리",
    "Fractional Digits": "소수 자릿수",
    "Target Value to Store: Exponent -2": "저장할 대상 값: 지수 -2",
    "Big Endian Layout": "빅 엔디안 레이아웃",
    "Little Endian Layout": "리틀 엔디안 레이아웃",
    "Checksum Sum = 30": "체크섬 합 = 30",
    "Total Mess = 7 and D in Hex": "총 난장판 = 16진수 7과 D",
    "Outputs 0": "0 출력",
    "Outputs 1": "1 출력",
    "Safe!": "안전!",
    "Data mathematically preserved!": "데이터 수학적으로 보존됨!",
    "The Curse of the Word Width": "워드 너비의 저주",
    "Data chunks A and B": "데이터 청크 A와 B",
    "Transmission Phase": "전송 단계",
    "Receiver Side: A 1-Bit Error Occurs": "수신기 측: 1비트 오류 발생",
    "Logical Lesson": "논리적 교훈",
    "Even Parity": "짝수 패리티",
    "Odd Parity": "홀수 패리티",
    "Even": "짝수",
    "Odd": "홀수",
    "Test with Even Parity Protocol": "짝수 패리티 프로토콜로 테스트",
    "Test with Odd Parity Protocol": "홀수 패리티 프로토콜로 테스트",
    "1's Complement": "1의 보수",
    "2's Complement": "2의 보수",
    "Signed": "부호 있음",
    "Unsigned": "부호 없음",
    "Overflow Carry": "오버플로우 캐리",
    "Target Value: +85": "대상 값: +85",
    "Value to Translate: 25": "변환할 값: 25",
    "Value to store: +32": "저장할 값: +32",
    "Value -2": "값 -2",
    "Addition Operation": "덧셈 연산",
    "Correct Answer Achieved": "정확한 답 도출",
    "Overflow Flag": "오버플로우 플래그",
    "Carry Flag": "캐리 플래그",
    "Status Flags Generation (Crucial for IF statements)": "상태 플래그 생성 (IF 문에 중요)",
    "Destination Register": "대상 레지스터",
    "Register A": "레지스터 A",
    "Register B": "레지스터 B",
    "Logical NOT gate": "논리 NOT 게이트",
    "XOR Gate": "XOR 게이트",
    "Final XOR": "최종 XOR",
    "Output Stage": "출력 단계",
    "Control Stage": "제어 단계",
    "Input Stage": "입력 단계",
    "Internal ROM Firmware": "내부 ROM 펌웨어"
}

def contains_korean(text):
    return bool(re.search(r'[가-힣]', text))

def is_ascii_diagram(text):
    return bool(re.search(r'[-+|<>^v]{2,}', text))

def translate_labels_in_text(inner_text):
    # Regex to find [ label ] or ( label )
    # We will replace them sequentially if they match the dictionary
    
    # Process brackets [ ... ]
    def repl_bracket(match):
        content = match.group(1)
        clean_content = content.strip()
        if clean_content in translations:
            # Reconstruct with the translation appended
            # Use original spacing to minimize disruption
            return f"[{content} / {translations[clean_content]}]"
        return match.group(0)
    
    # Process parentheses ( ... )
    def repl_paren(match):
        content = match.group(1)
        clean_content = content.strip()
        if clean_content in translations:
            return f"({content} / {translations[clean_content]})"
        return match.group(0)
        
    modified = re.sub(r'\[(.*?)\]', repl_bracket, inner_text)
    modified = re.sub(r'\((.*?)\)', repl_paren, modified)
    
    return modified

count = 0
for d in dirs:
    if not os.path.exists(d): continue
    for root, _, files in os.walk(d):
        for f in files:
            if f.endswith('.md'):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                    
                    blocks = re.findall(r'(```text\n.*?```)', content, re.DOTALL)
                    modified_content = content
                    changed = False
                    for block in blocks:
                        inner_text = block[7:-3]
                        if is_ascii_diagram(inner_text) and not contains_korean(inner_text):
                            translated_inner = translate_labels_in_text(inner_text)
                            if translated_inner != inner_text:
                                new_block = f"```text\n{translated_inner}```"
                                modified_content = modified_content.replace(block, new_block)
                                changed = True
                    
                    if changed:
                        with open(filepath, 'w', encoding='utf-8') as file:
                            file.write(modified_content)
                        count += 1
                        print(f"Updated {filepath}")
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

print(f"Successfully processed {count} files.")
