import os
import re
import shutil

base_dir = 'content/studynote/10_ai/'
target_mapping = {
    '01_ai_basics': (1, 100),
    '02_dl_architecture': (101, 200),
    '03_llm_nlp': (201, 282),
    '04_ai_ops_ethics': (283, 340),
    '05_data_science_ml': (341, 420)
}

def get_target_folder(num):
    for folder, (start, end) in target_mapping.items():
        if start <= num <= end:
            if folder == '02_dl_architecture':
                return '02_dl_architecture_new'
            return folder
    return None

# List all md files except _index.md and _keyword_list.md
files_to_move = []
for root, dirs, files in os.walk(base_dir):
    # Skip newly created folders to avoid moving them into themselves if they were already there
    if any(x in root for x in ['01_ai_basics', '02_dl_architecture_new', '03_llm_nlp', '04_ai_ops_ethics', '05_data_science_ml']):
        if root != base_dir: # allow files at root to be moved
            continue

    for file in files:
        if file.endswith('.md') and file != '_index.md' and file != '_keyword_list.md':
            match = re.match(r'^(\d+)_', file)
            if match:
                num = int(match.group(1))
                files_to_move.append((os.path.join(root, file), num, file))

# Perform move
for src_path, num, filename in files_to_move:
    target_folder = get_target_folder(num)
    if target_folder:
        dest_dir = os.path.join(base_dir, target_folder)
        dest_path = os.path.join(dest_dir, filename)
        
        # Ensure dest dir exists (already created but safe)
        os.makedirs(dest_dir, exist_ok=True)
        
        print(f"Moving {src_path} to {dest_path}")
        shutil.move(src_path, dest_path)
    else:
        print(f"No target folder for {filename} ({num})")
