import os
import re

base_dir = 'content/studynote/06_ict_convergence'
folders = [
    '01_blockchain',
    '02_iot_mobility',
    '03_cloud_infrastructure',
    '04_ai_llm',
    '05_data_science',
    'uncategorized'
]

existing_files = {} # num -> path

for folder in folders:
    folder_path = os.path.join(base_dir, folder)
    if not os.path.exists(folder_path):
        continue
    for filename in os.listdir(folder_path):
        if filename.endswith('.md') and filename != '_index.md' and filename != '_keyword_list.md':
            match = re.match(r'^(\d+)_', filename)
            if match:
                num = int(match.group(1))
                if num not in existing_files:
                    existing_files[num] = []
                existing_files[num].append(os.path.join(folder, filename))

# Read keyword list
keyword_list_path = os.path.join(base_dir, '_keyword_list.md')
keywords = {}
with open(keyword_list_path, 'r', encoding='utf-8') as f:
    for line in f:
        match = re.match(r'^(\d+)\.\s+(.*)', line.strip())
        if match:
            num = int(match.group(1))
            name = match.group(2).strip()
            keywords[num] = name

# Audit
missing = []
for i in range(1, 553):
    if i not in existing_files:
        missing.append(i)

duplicates = {num: paths for num, paths in existing_files.items() if len(paths) > 1}

print(f"Total keywords in list: {len(keywords)}")
print(f"Total existing files found: {len(existing_files)}")
print(f"Missing keywords (1-552): {missing}")
print(f"Duplicates: {duplicates}")

# Check misplaced files
# 01_blockchain: 1-100, 473-485, 542-545
# 02_iot_mobility: 101-180, 486-498, 260
# 03_cloud_infrastructure: 181-259, 499-509, 526, 531, 539-541
# 04_ai_llm: 261-320, 464-472, 527-530, 532-538, 547-549
# 05_data_science: 321-432 (actually user said 321-432), 466-468, 510-520, 546
# uncategorized: 521-525, 550-552

def get_target_folder(num):
    if 1 <= num <= 100 or 473 <= num <= 485 or 542 <= num <= 545:
        return '01_blockchain'
    if 101 <= num <= 180 or 486 <= num <= 498 or num == 260:
        return '02_iot_mobility'
    if 181 <= num <= 259 or 499 <= num <= 509 or num in [526, 531, 539, 540, 541]:
        return '03_cloud_infrastructure'
    if 261 <= num <= 320 or 464 <= num <= 472 or 527 <= num <= 530 or 532 <= num <= 538 or 547 <= num <= 549:
        return '04_ai_llm'
    if 321 <= num <= 432 or 466 <= num <= 468 or 510 <= num <= 520 or num == 546:
        return '05_data_science'
    if 521 <= num <= 525 or 550 <= num <= 552:
        return 'uncategorized'
    return None

misplaced = []
for num, paths in existing_files.items():
    target = get_target_folder(num)
    for path in paths:
        folder = path.split('/')[0]
        if target and folder != target:
            misplaced.append((path, target))

print(f"Misplaced files: {misplaced}")
