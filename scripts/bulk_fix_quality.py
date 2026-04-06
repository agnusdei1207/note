import os
import glob
import subprocess
import time
import sys

def get_defective_files():
    # Only process security files right now to be safe
    files = glob.glob('content/studynote/9_security/**/*.md', recursive=True)
    defective = []
    
    for f in files:
        if '_index.md' in f or '_keyword_list.md' in f:
            continue
            
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        issues = []
        if '## 핵심 인사이트' not in content:
            issues.append('missing_insight')
        if '📢 섹션 요약 비유' not in content:
            issues.append('missing_section_analogy')
        if '👶 어린이를 위한' not in content:
            issues.append('missing_child_analogy')
        if '```text' not in content or ('┌' not in content and '─' not in content):
            issues.append('missing_ascii_diagram')
        if 'Ⅰ.' not in content:
            issues.append('missing_roman_numerals')
            
        # If it misses ANY of the formatting requirements, rewrite it
        if len(issues) > 0:
            defective.append(f)
            
    return defective

def main():
    defective_files = get_defective_files()
    print(f"Found {len(defective_files)} defective files in 9_security to rewrite.")
    
    # Just output the list so the LLM can use `generalist` tool on them
    for df in defective_files[:20]: # Let's output up to 20 for the LLM to process in parallel
        print(df)

if __name__ == '__main__':
    main()
