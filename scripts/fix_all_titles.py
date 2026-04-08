import os
import re

subjects = [
    "1_computer_architecture",
    "2_operating_system",
    "3_network",
    "4_software_engineering",
    "5_database",
    "6_ict_convergence",
    "7_enterprise_systems",
    "8_algorithm_stats",
    "9_security",
    "10_ai",
    "11_design_supervision",
    "12_it_management",
    "13_cloud_architecture",
    "14_data_engineering",
    "15_devops_sre",
    "16_bigdata"
]

updated_count = 0

for subject in subjects:
    dir_path = os.path.join("content/studynote", subject)
    kw_path = os.path.join(dir_path, "_keyword_list.md")
    
    keywords = {}
    if os.path.exists(kw_path):
        nums = []
        with open(kw_path, 'r', encoding='utf-8') as f:
            for line in f:
                m = re.match(r'^(\d+)\.\s+', line)
                if m: nums.append(int(m.group(1)))
        
        has_duplicates = len(nums) != len(set(nums))
        
        with open(kw_path, 'r', encoding='utf-8') as f:
            idx = 1
            for line in f:
                m = re.match(r'^(\d+)\.\s+(.*)', line)
                if m:
                    file_k = idx if has_duplicates else int(m.group(1))
                    keywords[file_k] = m.group(2).strip()
                    idx += 1

    for root, _, files in os.walk(dir_path):
        if "_trash" in root: continue
        for file in files:
            if file.endswith('.md') and not file.startswith('_'):
                filepath = os.path.join(root, file)
                m = re.match(r'^0*(\d+)[_\.]', file)
                if not m: continue
                
                file_num = int(m.group(1))
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract the old title text (just roughly to keep if not in keywords)
                tm = re.search(r'^title\s*[=:]\s*"(.*)"\s*$', content, flags=re.MULTILINE)
                if not tm:
                    # Could be unquoted or trailing garbage
                    tm = re.search(r'^title\s*[=:]\s*(.*)$', content, flags=re.MULTILINE)
                
                if not tm: continue
                
                old_title_raw = tm.group(1).strip()
                # Clean up any trailing quotes or backslashes from previous bad replace
                old_title_raw = old_title_raw.strip('"').replace('\\"', '"')
                # Remove starting number if any
                clean_old_title = re.sub(r'^\d+\.\s*', '', old_title_raw)
                
                new_title = ""
                if file_num in keywords:
                    new_title = f"{file_num}. {keywords[file_num]}"
                else:
                    new_title = f"{file_num}. {clean_old_title}"
                
                # Escape quotes properly for TOML
                new_title = new_title.replace('"', '\\"')
                
                # Replace the entire line starting with title = or title:
                new_content = re.sub(r'^title\s*[=:]\s*.*$', lambda _: f'title = "{new_title}"', content, flags=re.MULTILINE)
                
                if content != new_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    updated_count += 1

print(f"Successfully fixed and updated {updated_count} files' titles.")
