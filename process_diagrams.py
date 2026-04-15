import os
import glob
import re
import unicodedata

def get_display_width(s):
    width = 0
    for char in s:
        if unicodedata.east_asian_width(char) in ('W', 'F'):
            width += 2
        else:
            width += 1
    return width

translations = {
    "AI Inference": "AI 추론",
    "API Gateway": "API 게이트웨이",
    "App 1": "앱 1",
    "App 2": "앱 2",
    "App 3": "앱 3",
    "App Instance A": "앱 인스턴스 A",
    "App Instance B": "앱 인스턴스 B",
    "Autonomous Car": "자율주행차",
    "BaaS Cloud Platform": "BaaS 플랫폼",
    "BaaS Security Rules Engine": "보안 룰 엔진",
    "Buildpack": "빌드팩",
    "CPU Pool": "CPU 풀",
    "CSP Central Control Plane": "CSP 중앙 제어 평면",
    "Canary Deployment via Ingress": "인그레스 카나리 배포",
    "Central Cloud Platform": "중앙 클라우드",
    "Central Cloud Storage": "중앙 스토리지",
    "Client": "클라이언트",
    "Client A": "클라이언트 A",
    "Client Request": "클라이언트 요청",
    "Cloud Control Plane": "클라우드 제어 평면",
    "Cloud DB": "클라우드 DB",
    "Container Registry": "컨테이너 레지스트리",
    "Customer A": "고객 A",
    "Customer B": "고객 B",
    "Customer C": "고객 C",
    "Customer On-Premise": "온프레미스",
    "DB Master VM": "DB 마스터 VM",
    "DB Replica VM": "DB 레플리카",
    "DB VM": "DB VM",
    "Database A": "DB A",
    "Database B": "DB B",
    "Developer Workspace": "개발자 공간",
    "Edge Gateway": "엣지 게이트웨이",
    "External Load Balancer": "외부 로드밸런서",
    "Factory IoT Data": "공장 IoT 데이터",
    "Frankfurt": "프랑크푸르트",
    "Guest OS 1": "게스트 OS 1",
    "Host-Only": "호스트 전용",
    "IaaS": "IaaS",
    "IaaS Control Plane": "IaaS 제어 평면",
    "Ingestion Buffer": "수집 버퍼",
    "Ingress Controller": "인그레스 컨트롤러",
    "Internet": "인터넷",
    "IoT Devices": "IoT 기기",
    "Kernel Space": "커널 공간",
    "LA": "LA",
    "Local Actuator": "로컬 액추에이터",
    "London": "런던",
    "Managed DB": "관리형 DB",
    "Managed NoSQL DB": "관리형 NoSQL DB",
    "Memory Pool": "메모리 풀",
    "NY": "뉴욕",
    "No": "아니오",
    "Node 1": "노드 1",
    "Node 2": "노드 2",
    "Node 3": "노드 3",
    "Node 4": "노드 4",
    "OS": "운영체제",
    "On-Premise": "온프레미스",
    "PaaS": "PaaS",
    "PaaS Control Engine": "PaaS 엔진",
    "PaaS Instance A": "인스턴스 A",
    "PaaS Instance B": "인스턴스 B",
    "PaaS Load Balancer": "PaaS 로드밸런서",
    "PaaS Runtime Cluster": "런타임 클러스터",
    "Pod": "파드",
    "Protocol Translator": "프로토콜 변환기",
    "Public Cloud": "퍼블릭 클라우드",
    "Public Region": "퍼블릭 리전",
    "QEMU Userspace Emulator": "QEMU 에뮬레이터",
    "RDBMS": "RDBMS",
    "Redis": "Redis",
    "ReplicaSet Controller": "레플리카셋",
    "Resource Scheduler": "스케줄러",
    "S3 Object": "S3 객체",
    "SSO Endpoint": "SSO 엔드포인트",
    "SaaS": "SaaS",
    "SaaS Application Instance": "SaaS 인스턴스",
    "Scale-In": "스케일 인",
    "Scale-Out": "스케일 아웃",
    "Scheduler": "스케줄러",
    "Sensor A": "센서 A",
    "Sensor B": "센서 B",
    "Sensor C": "센서 C",
    "Sensor Data Stream": "데이터 스트림",
    "Seoul": "서울",
    "Server 1": "서버 1",
    "Server 2": "서버 2",
    "Server 3": "서버 3",
    "Shared App Instance": "공유 앱 인스턴스",
    "Shared DB": "공유 DB",
    "Storage Pool": "스토리지 풀",
    "Stream Processing Engine": "스트림 처리 엔진",
    "Telco 5G Edge": "통신사 5G 엣지",
    "Transient Cache Buffer": "임시 캐시",
    "User Applications": "사용자 앱",
    "User Space": "유저 공간",
    "VM 1": "VM 1",
    "VM 2": "VM 2",
    "VM 3": "VM 3",
    "VM 4": "VM 4",
    "Web VM": "웹 VM",
    "Yes": "예",
    "kube-proxy": "kube-proxy",
    "kubelet": "kubelet",
    "App": "앱",
    "Database": "데이터베이스",
    "User": "사용자"
}

def replace_labels(match):
    block = match.group(1)
    lines = block.split('\n')
    new_lines = []
    
    for line in lines:
        new_line = line
        
        # Find all [ Label ] matches
        matches = list(re.finditer(r"\[\s*([a-zA-Z0-9\s_\-]+)\s*\]", new_line))
        # We need to replace from right to left so indices don't change
        for m in reversed(matches):
            label = m.group(1).strip()
            
            # Check if this label needs translation
            trans = translations.get(label)
            if trans and label != trans:
                old_text = f"[{m.group(1)}]"
                new_text = f"[{m.group(1).strip()} / {trans}]"
                
                # Calculate widths
                old_w = get_display_width(old_text)
                new_w = get_display_width(new_text)
                diff = new_w - old_w
                
                # Find spaces after the bracket to consume, to keep alignment
                # We look at the substring after the bracket
                after_bracket_idx = m.end()
                after_str = new_line[after_bracket_idx:]
                
                # How many consecutive spaces?
                space_match = re.match(r"^ +", after_str)
                if space_match:
                    spaces = space_match.group(0)
                    if len(spaces) >= diff:
                        # Consume spaces
                        new_after_str = spaces[diff:] + after_str[len(spaces):]
                        new_line = new_line[:m.start()] + new_text + new_after_str
                    else:
                        # Not enough spaces to consume, just replace and hope it doesn't break too badly
                        new_line = new_line[:m.start()] + new_text + after_str
                else:
                    new_line = new_line[:m.start()] + new_text + after_str
                    
        new_lines.append(new_line)
        
    return "```text\n" + '\n'.join(new_lines) + "\n```"

def process_files():
    files = glob.glob("content/studynote/13_cloud_architecture/1_virtualization/**/*.md", recursive=True)
    changed_count = 0
    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Replace only in text blocks
        new_content, num_subs = re.subn(r"```text\n(.*?)\n```", replace_labels, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(f, "w", encoding="utf-8") as file:
                file.write(new_content)
            changed_count += 1
            print(f"Updated {f}")
            
    print(f"Total files updated: {changed_count}")

if __name__ == '__main__':
    process_files()
