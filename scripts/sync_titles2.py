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
not_in_keyword_list_count = 0

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
                
                tm = re.search(r'title\s*=\s*"([^"]+)"', content)
                if not tm:
                    tm = re.search(r'title:\s*(.*)', content)
                
                if not tm: continue
                
                old_title = tm.group(1).strip()
                
                if re.match(rf'^{file_num}\.\s', old_title):
                    continue
                
                new_title = ""
                if file_num in keywords:
                    new_title = f"{file_num}. {keywords[file_num]}"
                else:
                    not_in_keyword_list_count += 1
                    clean_old_title = re.sub(r'^\d+\.\s*', '', old_title)
                    new_title = f"{file_num}. {clean_old_title}"
                
                # Double escape quotes inside the title if any, but properly
                new_title = new_title.replace('"', '\\"')
                
                if 'title =' in content:
                    new_content = re.sub(r'title\s*=\s*"[^"]+"', lambda _: f'title = "{new_title}"', content, count=1)
                else:
                    new_content = re.sub(r'title:\s*.*', lambda _: f'title: "{new_title}"', content, count=1)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1

print(f"Updated {updated_count} files' titles to sync with numbers and keyword list.")
print(f"Files not found in keyword list but prepended anyway: {not_in_keyword_list_count}")
