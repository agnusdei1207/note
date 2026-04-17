import os
import re

def find_missing(subject_dir):
    keyword_file = os.path.join(subject_dir, "_keyword_list.md")
    if not os.path.exists(keyword_file):
        return
    
    with open(keyword_file, "r") as f:
        content = f.read()
    
    # Extract keywords
    # 1. Web 1.0 (Read-only) / Web 2.0 (Read-Write, 플랫폼 중심)
    pattern = re.compile(r'^(\d+)\.\s+(.*)$', re.MULTILINE)
    keywords = pattern.findall(content)
    
    existing_files = []
    for root, dirs, files in os.walk(subject_dir):
        for file in files:
            if file.endswith(".md") and file != "_index.md" and file != "_keyword_list.md":
                match = re.match(r'^(\d+)_', file)
                if match:
                    existing_files.append(int(match.group(1)))
                else:
                    # check for #123_concept.md format or similar
                    match2 = re.search(r'#?(\d+)_', file)
                    if match2:
                        existing_files.append(int(match2.group(1)))
    
    existing_set = set(existing_files)
    missing = []
    for num_str, name in keywords:
        num = int(num_str)
        if num not in existing_set:
            missing.append((num, name))
            
    print(f"Missing in {subject_dir}: {len(missing)} files")
    for m in missing[:5]:
        print(f" - {m[0]}: {m[1]}")

find_missing("content/studynote/06_ict_convergence")
find_missing("content/studynote/07_enterprise_systems")
find_missing("content/studynote/08_algorithm_stats")
find_missing("content/studynote/09_security")
find_missing("content/studynote/10_ai")
find_missing("content/studynote/11_design_supervision")
