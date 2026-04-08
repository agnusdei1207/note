import os
import re

dir_path = "content/studynote"
mismatched = []

for root, _, files in os.walk(dir_path):
    if "_trash" in root: continue
    for file in files:
        if file.endswith(".md") and not file.startswith("_"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find title
            tm = re.search(r'title\s*=\s*"([^"]+)"', content)
            if not tm:
                tm = re.search(r'title:\s*(.*)', content)
                
            if tm:
                title = tm.group(1).strip()
                # Check if title starts with digits followed by dot
                if not re.match(r'^\d+\.', title):
                    mismatched.append((filepath, title))

print(f"Found {len(mismatched)} files with title missing numbering:")
for fp, t in mismatched[:20]:
    print(f"{fp} -> {t}")
