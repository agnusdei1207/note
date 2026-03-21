import os
import re

dir_path = "content/studynote/2_operating_system/1_overview_architecture"
files = [f for f in os.listdir(dir_path) if f.endswith(".md") and not f.startswith("_")]

def get_num(filename):
    match = re.match(r"(\d+)_", filename)
    return int(match.group(1)) if match else 999

files.sort(key=get_num)

for filename in files:
    num = get_num(filename)
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
            
    if end_fm_idx == -1:
        continue

    # Extract real title from content headers if front matter title is "---" or we want to re-standardize
    real_title = ""
    for i in range(end_fm_idx + 1, len(lines)):
        line = lines[i].strip()
        if line.startswith("# ") and "핵심 인사이트" not in line:
            real_title = line.replace("# ", "").strip()
            # If the header already has a number like "1. ", strip it so we can format it cleanly
            real_title = re.sub(r'^\d+\.\s*', '', real_title)
            break
    
    # If no header found, fallback to filename
    if not real_title or real_title == "---":
        # Extract from filename
        name_part = filename.replace(".md", "")
        name_part = re.sub(r'^\d+_', '', name_part)
        real_title = name_part.replace("_", " ").title()

    # Format the new title with numbering: "1. 운영체제..."
    new_title = f"{num}. {real_title}"

    # Update front matter
    new_lines = []
    for i in range(len(lines)):
        if i > 0 and i < end_fm_idx and lines[i].startswith("title ="):
            new_lines.append(f'title = "{new_title}"\n')
        else:
            new_lines.append(lines[i])
            
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

print("Titles fixed and numbered.")
