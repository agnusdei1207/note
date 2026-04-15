import os
import re

dirs = [
    "content/studynote/5_database",
    "content/studynote/6_ict_convergence",
    "content/studynote/7_enterprise_systems",
    "content/studynote/8_algorithm_stats"
]

def contains_korean(text):
    return bool(re.search(r'[가-힣]', text))

def is_ascii_diagram(text):
    # check if it has drawing characters
    return bool(re.search(r'[-+|<>^v]{2,}', text))

for d in dirs:
    for root, _, files in os.walk(d):
        for f in files:
            if f.endswith('.md'):
                filepath = os.path.join(root, f)
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                blocks = re.findall(r'```text\n(.*?)```', content, re.DOTALL)
                for i, block in enumerate(blocks):
                    if is_ascii_diagram(block) and not contains_korean(block):
                        print(f"--- MATCH IN {filepath} ---")
                        print(block.strip())
                        print("-----------------------------")
