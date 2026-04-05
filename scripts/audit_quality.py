import os
import glob
import json

def audit():
    files = glob.glob('content/studynote/**/*.md', recursive=True)
    defective = []
    
    total_checked = 0
    for f in files:
        if '_index.md' in f or '_keyword_list.md' in f:
            continue
            
        total_checked += 1
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
            
        if issues:
            defective.append({'file': f, 'issues': issues})
            
    with open('quality_audit_results.json', 'w', encoding='utf-8') as out:
        json.dump(defective, out, indent=2, ensure_ascii=False)
        
    print(f"Total files checked: {total_checked}")
    print(f"Files needing improvement: {len(defective)}")

if __name__ == '__main__':
    audit()