import os
import re

base_dir = "content/studynote"
subjects = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and re.match(r'^\d{2}_', d)])

def get_section_id(dirname):
    match = re.match(r'^0*(\d+)_', dirname)
    if match:
        return int(match.group(1))
    return None

def process_subject(subject_path):
    kw_file = os.path.join(subject_path, "_keyword_list.md")
    if not os.path.exists(kw_file):
        print(f"Skipping {subject_path}, no _keyword_list.md")
        return

    # Check if this subject is globally numbered or restarting
    nums_in_list = []
    with open(kw_file, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r'^(\d+)\.\s+', line.strip())
            if match:
                nums_in_list.append(int(match.group(1)))
    
    if not nums_in_list:
        return
    
    restarts = sum(1 for i in range(1, len(nums_in_list)) if nums_in_list[i] <= nums_in_list[i-1])
    is_restarting = restarts > 0

    expected_keys = set()
    current_section_id = -1
    
    # Parse the keyword list properly
    with open(kw_file, "r", encoding="utf-8") as f:
        for line in f:
            # check section header
            sec_match = re.match(r'^##\s+(\d+)\.\s+', line.strip())
            if sec_match:
                current_section_id = int(sec_match.group(1))
            
            kw_match = re.match(r'^(\d+)\.\s+', line.strip())
            if kw_match:
                num = int(kw_match.group(1))
                if is_restarting:
                    if current_section_id != -1:
                        expected_keys.add((current_section_id, num))
                else:
                    expected_keys.add(num)

    found_files = {} # key -> list of file paths
    unmatched_files = []

    for root, dirs, files in os.walk(subject_path):
        sec_id = get_section_id(os.path.basename(root))
        for filename in files:
            if filename.endswith(".md") and filename not in ["_index.md", "_keyword_list.md"]:
                filepath = os.path.join(root, filename)
                match = re.match(r'^(?:#)?0*(\d+)[_\-\s]+(.*)\.md$', filename)
                if not match:
                    match_alt = re.search(r'0*(\d+)', filename)
                    if match_alt and filename.startswith(match_alt.group(0)):
                        num = int(match_alt.group(1))
                    else:
                        unmatched_files.append(filepath)
                        continue
                else:
                    num = int(match.group(1))

                if is_restarting:
                    if sec_id is not None and (sec_id, num) in expected_keys:
                        found_files.setdefault((sec_id, num), []).append(filepath)
                    else:
                        unmatched_files.append(filepath)
                else:
                    if num in expected_keys:
                        found_files.setdefault(num, []).append(filepath)
                    else:
                        unmatched_files.append(filepath)

    to_delete = unmatched_files[:]
    to_rename = []

    # Process duplicates: keep largest, delete rest
    for key, filepaths in found_files.items():
        if len(filepaths) > 1:
            # Sort by file size descending
            filepaths.sort(key=lambda p: os.path.getsize(p), reverse=True)
            to_delete.extend(filepaths[1:])
        
        # the kept file is filepaths[0]
        kept_file = filepaths[0]
        
        # Determine new zero-padded name
        num = key[1] if is_restarting else key
        filename = os.path.basename(kept_file)
        match = re.match(r'^(?:#)?0*\d+([_\-\s]+.*\.md)$', filename)
        if match:
            rest = match.group(1)
            new_filename = f"{num:03d}{rest}"
        else:
            # fallback if it was just a number
            new_filename = f"{num:03d}_{filename}"
            # cleanup double underscore
            new_filename = new_filename.replace(f"{num:03d}_{num}", f"{num:03d}")
        
        if filename != new_filename:
            new_filepath = os.path.join(os.path.dirname(kept_file), new_filename)
            to_rename.append((kept_file, new_filepath))

    print(f"[{os.path.basename(subject_path)}] Expected: {len(expected_keys)}, Found Unique: {len(found_files)}, Deleting: {len(to_delete)}, Renaming: {len(to_rename)}")

    # Execute deletions
    for f in to_delete:
        os.remove(f)
    
    # Execute renames
    for old_path, new_path in to_rename:
        if os.path.exists(old_path) and not os.path.exists(new_path):
            os.rename(old_path, new_path)

for subject in subjects:
    process_subject(os.path.join(base_dir, subject))

# Clean up empty directories
for subject in subjects:
    subj_dir = os.path.join(base_dir, subject)
    for root, dirs, files in os.walk(subj_dir, topdown=False):
        for dirname in dirs:
            dir_path = os.path.join(root, dirname)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"Removed empty directory: {dir_path}")
