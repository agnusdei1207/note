import os
import re

base_dir = "content/studynote"
HEADING_RE = re.compile(r"^##\s+(\d+)\.\s+(.*)$")
KEYWORD_RE = re.compile(r"^(\d+)\.\s+(.*)$")
FILE_NUM_RE = re.compile(r"^(\d+)")

missing_info = {}

for subject_dir in os.listdir(base_dir):
    subj_path = os.path.join(base_dir, subject_dir)
    if not (os.path.isdir(subj_path) and subject_dir[0].isdigit()):
        continue

    kw_path = os.path.join(subj_path, "_keyword_list.md")
    if not os.path.exists(kw_path):
        continue

    # Get expected numbers
    expected_nums = []
    with open(kw_path, "r", encoding="utf-8") as f:
        for line in f:
            match = KEYWORD_RE.match(line.strip())
            if match:
                expected_nums.append(int(match.group(1)))

    # Get actual numbers
    actual_nums = set()
    for root, dirs, files in os.walk(subj_path):
        for file in files:
            if file.endswith(".md") and not file.startswith("_"):
                match = FILE_NUM_RE.match(file)
                if match:
                    actual_nums.add(int(match.group(1)))

    missing = sorted(list(set(expected_nums) - actual_nums))
    if missing:
        missing_info[subject_dir] = missing[:5]

for k in sorted(missing_info.keys(), key=lambda x: int(x.split('_')[0])):
    print(f"{k}: {missing_info[k]}")
