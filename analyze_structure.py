import os
import re
from collections import defaultdict

base_dir = "content/studynote"
subjects = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and re.match(r'^\d{2}_', d)])

for subject in subjects:
    subj_dir = os.path.join(base_dir, subject)
    kw_file = os.path.join(subj_dir, "_keyword_list.md")
    
    if not os.path.exists(kw_file):
        print(f"[{subject}] No _keyword_list.md found!")
        continue
        
    expected_keys = {}
    with open(kw_file, "r") as f:
        for line in f:
            match = re.match(r'^(\d+)\.\s+(.*)$', line.strip())
            if match:
                num = int(match.group(1))
                expected_keys[num] = match.group(2)
                
    found_files = defaultdict(list)
    unmatched_files = []
    
    for root, dirs, files in os.walk(subj_dir):
        for filename in files:
            if filename.endswith(".md") and filename not in ["_index.md", "_keyword_list.md"]:
                # Try to extract a leading number
                match = re.match(r'^(?:#)?0*(\d+)[_\-\s]+(.*)\.md$', filename)
                if match:
                    num = int(match.group(1))
                    found_files[num].append(os.path.join(root, filename))
                else:
                    # Also try to match files that might just be a number or have different formats
                    match_alt = re.search(r'0*(\d+)', filename)
                    if match_alt and filename.startswith(match_alt.group(0)):
                        num = int(match_alt.group(1))
                        found_files[num].append(os.path.join(root, filename))
                    else:
                        unmatched_files.append(os.path.join(root, filename))
                        
    duplicates = {k: v for k, v in found_files.items() if len(v) > 1}
    missing = set(expected_keys.keys()) - set(found_files.keys())
    
    print(f"\n{'='*50}\n[{subject}]")
    print(f"Expected: {len(expected_keys)}, Found Mapped: {sum(len(v) for v in found_files.values())}")
    print(f"Unmatched (Odd structure): {len(unmatched_files)}")
    if unmatched_files:
        for f in unmatched_files[:5]:
            print(f"  - {f}")
        if len(unmatched_files) > 5:
            print(f"  ... and {len(unmatched_files)-5} more")
            
    print(f"Duplicates: {len(duplicates)} numbers have multiple files")
    if duplicates:
        for k, v in list(duplicates.items())[:3]:
            print(f"  {k}: {v}")
        if len(duplicates) > 3:
            print(f"  ... and {len(duplicates)-3} more")

