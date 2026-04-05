import re
import sys

file_path = 'content/studynote/9_security/_keyword_list.md'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
current_num = 1

for line in lines:
    match = re.match(r'^(\d+)\.\s*(.*)', line)
    if match:
        new_lines.append(f"{current_num}. {match.group(2)}\n")
        current_num += 1
    else:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Renumbered {current_num - 1} keywords.")