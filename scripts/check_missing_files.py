import os
import re

subjects = {
    "4_software_engineering": "SE",
    "5_database": "DB",
    "6_ict_convergence": "ICT",
    "7_enterprise_systems": "Enterprise",
    "8_algorithm_stats": "Algorithm",
    "9_security": "Security",
    "10_ai": "AI",
    "11_design_supervision": "Design",
    "12_it_management": "IT_Mgmt",
    "13_cloud_architecture": "Cloud",
    "14_data_engineering": "DataEng",
    "15_devops_sre": "DevOps",
    "16_bigdata": "BigData"
}

missing_list = {}

for folder, name in subjects.items():
    dir_path = os.path.join("content/studynote", folder)
    keyword_file = os.path.join(dir_path, "_keyword_list.md")
    
    keywords = []
    if os.path.exists(keyword_file):
        with open(keyword_file, "r", encoding="utf-8") as f:
            global_idx = 1
            for line in f:
                match = re.match(r'^(\d+)\.\s+(.*)', line)
                if match:
                    keywords.append((global_idx, match.group(2).strip()))
                    global_idx += 1
    
    existing_nums = set()
    for root, _, files in os.walk(dir_path):
        for file in files:
            m = re.match(r'^0*(\d+)[_\.]', file)
            if m:
                existing_nums.add(int(m.group(1)))
    
    max_existing = max(existing_nums) if existing_nums else 0
    missing = []
    for idx, title in keywords:
        if idx <= max_existing and idx not in existing_nums:
            missing.append((idx, title))
            
    missing_list[name] = {"missing": missing, "next": max_existing + 1, "keywords": keywords}

for name, info in missing_list.items():
    print(f"[{name}] Max Existing: {info['next'] - 1}")
    if info['missing']:
        print("Missing files found!")
        for idx, title in info['missing'][:5]:
            print(f"  {idx}. {title}")
    else:
        print("No missing files up to max.")
    
    # What's the very next one?
    next_idx = info['next']
    if next_idx <= len(info['keywords']):
        print(f"Next to create: {next_idx}. {info['keywords'][next_idx-1][1]}")
    print()
