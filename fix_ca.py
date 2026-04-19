import os
import re

base_dir = "content/studynote/01_computer_architecture"

# 1. Extract keyword list
keywords = {}
with open(os.path.join(base_dir, "_keyword_list.md"), "r") as f:
    for line in f:
        match = re.match(r'^(\d+)\.\s+(.*)$', line.strip())
        if match:
            num = int(match.group(1))
            keywords[num] = match.group(2)

# 2. Check and rename files
for root, dirs, files in os.walk(base_dir):
    for filename in files:
        if filename.endswith(".md") and filename not in ["_index.md", "_keyword_list.md"]:
            # extract number from file, e.g. 021_digital_vs_analog.md or 21_digital_vs_analog.md
            match = re.match(r'^0*(\d+)_.*\.md$', filename)
            if match:
                num = int(match.group(1))
                rest = filename[match.end(1):] # the part after the digits
                
                # new name: zero pad to 3 digits
                new_filename = f"{num:03d}{rest}"
                
                if filename != new_filename:
                    old_path = os.path.join(root, filename)
                    new_path = os.path.join(root, new_filename)
                    print(f"Renaming {old_path} -> {new_path}")
                    os.rename(old_path, new_path)
            else:
                print(f"Unmatched filename: {os.path.join(root, filename)}")

