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
        with open(kw_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Capture the number and the rest of the line (excluding newline)
                m = re.match(r'^(\d+)\.\s+(.*)', line)
                if m:
                    keywords[int(m.group(1))] = m.group(2).strip()
    
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
                
                # Find current title
                tm = re.search(r'title\s*=\s*"([^"]+)"', content)
                if not tm:
                    tm = re.search(r'title:\s*(.*)', content)
                
                if not tm: continue # No title found
                
                old_title = tm.group(1).strip()
                
                # Check if title already starts with the correct number
                # "119. 시프트 연산"
                if re.match(rf'^{file_num}\.', old_title):
                    continue # already has the number, skip to avoid touching 3000 files needlessly
                
                # We need to update the title.
                new_title = ""
                if file_num in keywords:
                    # Sync completely with keyword list
                    # But wait, some keyword list entries are very long or have weird formats.
                    # It's safer to just prepend the number to the existing title if the user just complained about missing numbers.
                    # But the user said: "키워드 리스트에 맞게 싱크 맞추세요" -> "Sync with keyword list"
                    new_title = f"{file_num}. {keywords[file_num]}"
                else:
                    # Not in keyword list, just prepend number
                    not_in_keyword_list_count += 1
                    # Remove any existing wrong numbers
                    clean_old_title = re.sub(r'^\d+\.\s*', '', old_title)
                    new_title = f"{file_num}. {clean_old_title}"
                
                # Escape quotes
                new_title = new_title.replace('"', '\\"')
                
                # Replace in content
                new_content = content
                if 'title =' in content:
                    new_content = re.sub(r'title\s*=\s*"[^"]+"', f'title = "{new_title}"', content, count=1)
                else:
                    new_content = re.sub(r'title:\s*.*', f'title: "{new_title}"', content, count=1)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1

print(f"Updated {updated_count} files' titles to sync with numbers and keyword list.")
print(f"Files not found in keyword list but prepended anyway: {not_in_keyword_list_count}")
