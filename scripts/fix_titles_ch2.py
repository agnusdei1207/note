import os
import re

# 1. Parse keyword list to get exact titles
keyword_file = "content/studynote/2_operating_system/_keyword_list.md"
titles = {}
with open(keyword_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        match = re.match(r"^(\d+)\.\s+(.*)$", line)
        if match:
            num = int(match.group(1))
            title = match.group(2)
            titles[num] = f"{num}. {title}"

# 2. Update files in 2_process_thread
dir_path = "content/studynote/2_operating_system/2_process_thread"
files = [f for f in os.listdir(dir_path) if f.endswith(".md") and not f.startswith("_")]

count = 0
for filename in files:
    match = re.match(r"(\d+)_", filename)
    if not match: continue
    num = int(match.group(1))
    
    if num not in titles: continue
    
    correct_title = titles[num]
    file_path = os.path.join(dir_path, filename)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    if not lines or lines[0].strip() != "+++":
        continue
        
    end_fm_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "+++":
            end_fm_idx = i
            break
            
    if end_fm_idx == -1: continue
    
    new_lines = []
    for i in range(len(lines)):
        if 0 < i < end_fm_idx and lines[i].startswith("title ="):
            safe_title = correct_title.replace('"', '\\"')
            new_lines.append(f'title = "{safe_title}"\n')
        else:
            new_lines.append(lines[i])
            
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    count += 1

print(f"Fixed {count} titles in Chapter 2.")
