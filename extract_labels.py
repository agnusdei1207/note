import os
import re
import json

dirs = [
    "content/studynote/1_computer_architecture",
    "content/studynote/2_operating_system",
    "content/studynote/3_network",
    "content/studynote/4_software_engineering"
]

def contains_korean(text):
    return bool(re.search(r'[가-힣]', text))

def is_ascii_diagram(text):
    return bool(re.search(r'[-+|<>^v]{2,}', text))

labels = set()

for d in dirs:
    if not os.path.exists(d): continue
    for root, _, files in os.walk(d):
        for f in files:
            if f.endswith('.md'):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                    
                    blocks = re.findall(r'(```text\n.*?```)', content, re.DOTALL)
                    for block in blocks:
                        inner_text = block[7:-3]
                        if is_ascii_diagram(inner_text) and not contains_korean(inner_text):
                            # Find all [ ... ] or ( ... )
                            found = re.findall(r'\[(.*?)\]|\((.*?)\)', inner_text)
                            for match in found:
                                m = match[0] if match[0] else match[1]
                                m = m.strip()
                                # if it has alphabet characters and no drawing characters
                                if re.search(r'[a-zA-Z]', m) and not re.search(r'[-+|<>^v]{2,}', m):
                                    labels.add(m)
                except Exception as e:
                    pass

with open('labels.json', 'w', encoding='utf-8') as f:
    json.dump(list(labels), f, indent=2)
print(f"Extracted {len(labels)} labels.")
