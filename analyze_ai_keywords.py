import os
import re

keyword_list_path = 'content/studynote/10_ai/_keyword_list.md'
base_dir = 'content/studynote/10_ai/'

# Mapping based on user request
def get_target_folder(num):
    if 1 <= num <= 100:
        return '01_ai_basics'
    elif 101 <= num <= 200:
        return '02_dl_architecture'
    elif 201 <= num <= 282:
        return '03_llm_nlp'
    elif 283 <= num <= 340:
        return '04_ai_ops_ethics'
    elif 341 <= num <= 420:
        return '05_data_science_ml'
    return 'unknown'

# Parse keywords
keywords = {}
with open(keyword_list_path, 'r', encoding='utf-8') as f:
    for line in f:
        match = re.match(r'^(\d+)\.\s+(.*)', line.strip())
        if match:
            num = int(match.group(1))
            name = match.group(2).strip()
            keywords[num] = name

# Scan existing files
existing_files = []
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.md') and file != '_index.md' and file != '_keyword_list.md':
            full_path = os.path.join(root, file)
            match = re.match(r'^(\d+)_', file)
            if match:
                num = int(match.group(1))
                existing_files.append({
                    'num': num,
                    'path': full_path,
                    'filename': file
                })

# Analysis
keyword_to_files = {}
for i in range(1, 421):
    keyword_to_files[i] = []

for f in existing_files:
    if f['num'] in keyword_to_files:
        keyword_to_files[f['num']].append(f)
    else:
        # Number not in 1-420 range, but maybe relevant?
        print(f"File with out-of-range number: {f['filename']} ({f['num']})")

missing = []
duplicates = []
correct_location = []
wrong_location = []

for i in range(1, 421):
    files = keyword_to_files[i]
    if not files:
        missing.append(i)
    else:
        if len(files) > 1:
            duplicates.append(i)
        
        target_folder = get_target_folder(i)
        for f in files:
            current_folder = os.path.basename(os.path.dirname(f['path']))
            if current_folder != target_folder:
                wrong_location.append(f)
            else:
                correct_location.append(f)

print(f"Total Keywords: 420")
print(f"Missing Keywords: {len(missing)}")
print(f"Keywords with Multiple Files (Duplicates): {len(duplicates)}")
print(f"Files in Wrong Location: {len(wrong_location)}")
print(f"Files in Correct Location: {len(correct_location)}")

print("\nMissing Keywords List (first 50):")
print(missing[:50])

print("\nWrong Location Examples (first 10):")
for f in wrong_location[:10]:
    num = f['num']
    print(f"{f['path']} -> should be in {get_target_folder(num)}")

# Save detailed report for my own use
with open('ai_keywords_report.txt', 'w', encoding='utf-8') as f:
    f.write(f"Missing: {missing}\n")
    f.write("Duplicates:\n")
    for d in duplicates:
        f.write(f"{d}: {[x['path'] for x in keyword_to_files[d]]}\n")
    f.write("Wrong Locations:\n")
    for w in wrong_location:
        f.write(f"{w['path']} -> {get_target_folder(w['num'])}\n")
