import os
import re

def audit_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return {"error": str(e)}

    results = {
        "toml_front_matter": False,
        "insight_section": False,
        "insight_points_count": 0,
        "roman_sections": {
            "I": False, "II": False, "III": False, "IV": False, "V": False
        },
        "section_summaries": {
            "I": False, "II": False, "III": False, "IV": False, "V": False
        },
        "concept_map": False,
        "children_explanation": False
    }

    if content.startswith('+++'):
        second_pos = content.find('+++', 3)
        if second_pos != -1:
            results["toml_front_matter"] = True

    # Debugging 핵심 인사이트
    insight_match = re.search(r'#### 핵심 인사이트.*?\n(>.*?(?:\n>.*)*)', content, re.DOTALL)
    if insight_match:
        results["insight_section"] = True
        insight_content = insight_match.group(1)
        print(f"DEBUG: Found insight content:\n{insight_content}")
        points = re.findall(r'>\s*\d+\.', insight_content)
        print(f"DEBUG: Points found: {points}")
        results["insight_points_count"] = len(points)
    else:
        print("DEBUG: 핵심 인사이트 section NOT found with the regex.")
        # Try a simpler regex to see what's happening
        simple_match = re.search(r'#### 핵심 인사이트', content)
        if simple_match:
            print("DEBUG: '#### 핵심 인사이트' header exists, but the following blockquote didn't match.")
            # Print next few lines
            start = simple_match.end()
            print(f"DEBUG: Next 100 chars: {repr(content[start:start+100])}")

    # Roman sections
    roman_map = {
        "I": [r'### Ⅰ\.', r'### I\.'],
        "II": [r'### Ⅱ\.', r'### II\.'],
        "III": [r'### Ⅲ\.', r'### III\.'],
        "IV": [r'### Ⅳ\.', r'### IV\.'],
        "V": [r'### Ⅴ\.', r'### V\.']
    }
    section_positions = {}
    for key, patterns in roman_map.items():
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                results["roman_sections"][key] = True
                section_positions[key] = match.start()
                break

    # Section summaries
    sorted_keys = sorted(section_positions.keys(), key=lambda k: section_positions[k])
    for i, key in enumerate(sorted_keys):
        start = section_positions[key]
        if i + 1 < len(sorted_keys):
            end = section_positions[sorted_keys[i+1]]
        else:
            end = len(content)
            next_markers = [re.search(r'### 📌 관련 개념 맵', content), re.search(r'### 👶 어린이를 위한 3줄 비유 설명', content)]
            for m in next_markers:
                if m and m.start() > start:
                    end = min(end, m.start())
        section_text = content[start:end]
        if '📢 섹션 요약 비유' in section_text:
            results["section_summaries"][key] = True

    if '### 📌 관련 개념 맵' in content: results["concept_map"] = True
    if '### 👶 어린이를 위한 3줄 비유 설명' in content: results["children_explanation"] = True

    return results

file_path = '/mnt/c/workspace/brainscience/content/studynote/7_enterprise_systems/uncategorized/216_liss_logic.md'
print(f"Auditing {file_path}")
res = audit_file(file_path)
print(f"Results: {res}")
