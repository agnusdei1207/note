import os
import re

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
                            print(f"--- MATCH IN {filepath} ---")
                            print(block)
                            print("-----------------------------")
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
