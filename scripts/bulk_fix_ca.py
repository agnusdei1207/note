import os
import re

dir_path = "content/studynote/1_computer_architecture/15_advanced_topics"
files = [f for f in os.listdir(dir_path) if f.endswith(".md") and not f.startswith("_")]

def get_num(filename):
    match = re.match(r"(\d+)_", filename)
    return int(match.group(1)) if match else 999

files.sort(key=get_num)

for filename in files:
    num = get_num(filename)
    if num < 790: continue
    
    file_path = os.path.join(dir_path, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if lines[0].strip() == "+++":
        # Already has front matter, but let's check category
        has_correct_cat = False
        for line in lines:
            if 'categories = "studynote-computer-architecture"' in line:
                has_correct_cat = True
                break
        if has_correct_cat:
            continue
    
    # Standardize
    title = ""
    start_idx = 0
    if lines[0].strip() == "+++":
        for i in range(1, len(lines)):
            if lines[i].startswith('title ='):
                title = lines[i].split('=')[1].strip().strip('"').strip("'")
            if lines[i].strip() == "+++":
                start_idx = i + 1
                break
    
    if not title:
        for i in range(start_idx, len(lines)):
            if lines[i].startswith("# "):
                title = lines[i].strip("# ").strip()
                start_idx = i + 1
                break

    if not title:
        title = filename.replace(".md", "").replace("_", " ")

    content_start = start_idx
    while content_start < len(lines) and not lines[content_start].strip():
        content_start += 1
            
    front_matter = [
        "+++\n",
        f'title = "{title}"\n',
        'date = "2026-03-21"\n',
        "[extra]\n",
        'categories = "studynote-computer-architecture"\n',
        "+++\n\n"
    ]
    
    new_content = "".join(front_matter + lines[content_start:])
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("CA files 790-802 standardized.")
