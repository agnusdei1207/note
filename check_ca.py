import os
import re
from collections import defaultdict

base_dir = "content/studynote/01_computer_architecture"

# 1. Extract keyword list
expected_keys = {}
with open(os.path.join(base_dir, "_keyword_list.md"), "r") as f:
    for line in f:
        match = re.match(r'^(\d+)\.\s+(.*)$', line.strip())
        if match:
            num = int(match.group(1))
            expected_keys[num] = match.group(2)

# 2. Extract numbers from files
found_files = defaultdict(list)
unmatched_files = []

for root, dirs, files in os.walk(base_dir):
    for filename in files:
        if filename.endswith(".md") and filename not in ["_index.md", "_keyword_list.md"]:
            match = re.match(r'^0*(\d+)_.*\.md$', filename)
            if match:
                num = int(match.group(1))
                found_files[num].append(os.path.join(root, filename))
            else:
                unmatched_files.append(os.path.join(root, filename))

# 3. Report
print(f"Total expected keywords: {len(expected_keys)}")
print(f"Total numbered files found: {sum(len(v) for v in found_files.values())}")
print(f"Unmatched files: {len(unmatched_files)}")
for f in unmatched_files:
    print(f" - {f}")

duplicates = {k: v for k, v in found_files.items() if len(v) > 1}
print(f"\nDuplicates ({len(duplicates)}):")
for k, v in duplicates.items():
    print(f" {k}: {v}")

missing = set(expected_keys.keys()) - set(found_files.keys())
print(f"\nMissing ({len(missing)}):")
for k in sorted(missing):
    print(f" {k}: {expected_keys[k]}")

extra = set(found_files.keys()) - set(expected_keys.keys())
print(f"\nExtra ({len(extra)}):")
for k in sorted(extra):
    print(f" {k}: {found_files[k]}")

