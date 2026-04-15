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
            "I": False,
            "II": False,
            "III": False,
            "IV": False,
            "V": False
        },
        "section_summaries": {
            "I": False,
            "II": False,
            "III": False,
            "IV": False,
            "V": False
        },
        "concept_map": False,
        "children_explanation": False
    }

    # 6. Front matter TOML check
    if content.startswith('+++'):
        second_pos = content.find('+++', 3)
        if second_pos != -1:
            results["toml_front_matter"] = True

    # 1. 핵심 인사이트 section and 3 points
    insight_match = re.search(r'#{2,4}\s*핵심 인사이트.*?\n((?:>.*\n?)+)', content)
    if insight_match:
        results["insight_section"] = True
        insight_content = insight_match.group(1)
        points = re.findall(r'>\s*\d+\.', insight_content)
        results["insight_points_count"] = len(points)

    # 2. Roman numeral sections
    # Support both Unicode (Ⅰ, Ⅱ, ...) and ASCII (I, II, ...) and different header levels
    roman_map = {
        "I": [r'#{2,4}\s*[ⅠI]\.'],
        "II": [r'#{2,4}\s*Ⅱ\.', r'#{2,4}\s*II\.'],
        "III": [r'#{2,4}\s*Ⅲ\.', r'#{2,4}\s*III\.'],
        "IV": [r'#{2,4}\s*Ⅳ\.', r'#{2,4}\s*IV\.'],
        "V": [r'#{2,4}\s*Ⅴ\.', r'#{2,4}\s*V\.']
    }

    section_positions = {}
    for key, patterns in roman_map.items():
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                results["roman_sections"][key] = True
                section_positions[key] = match.start()
                break

    # 3. Section summaries 📢 섹션 요약 비유
    sorted_keys = sorted(section_positions.keys(), key=lambda k: section_positions[k])
    for i, key in enumerate(sorted_keys):
        start = section_positions[key]
        if i + 1 < len(sorted_keys):
            end = section_positions[sorted_keys[i+1]]
        else:
            # Look until the end of the main content
            end = len(content)
            next_markers = [re.search(r'📌 관련 개념 맵', content), re.search(r'👶 어린이를 위한 3줄 비유 설명', content)]
            for m in next_markers:
                if m and m.start() > start:
                    end = min(end, m.start())
        
        section_text = content[start:end]
        if '📢 섹션 요약 비유' in section_text:
            results["section_summaries"][key] = True

    # 4. 관련 개념 맵
    if '📌 관련 개념 맵' in content:
        results["concept_map"] = True

    # 5. 어린이를 위한 3줄 비유 설명
    if '👶 어린이를 위한 3줄 비유 설명' in content:
        results["children_explanation"] = True

    return results

def main():
    base_dir = '/mnt/c/workspace/brainscience/content/studynote/'
    all_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md') and file != '_index.md':
                all_files.append(os.path.join(root, file))

    total_files = len(all_files)
    passed_all = 0
    failures = []

    stats = {
        "toml_front_matter": 0,
        "insight_section": 0,
        "insight_3_points": 0,
        "all_roman_sections": 0,
        "all_section_summaries": 0,
        "concept_map": 0,
        "children_explanation": 0
    }

    print(f"Auditing {total_files} files...")

    for i, file_path in enumerate(all_files):
        if i % 500 == 0 and i > 0:
            print(f"Processed {i}/{total_files} files...")
            
        res = audit_file(file_path)
        
        if "error" in res:
            failures.append({
                "file": os.path.relpath(file_path, base_dir),
                "reasons": [f"Read error: {res['error']}"]
            })
            continue
        
        file_passed = True
        file_failures = []

        if res["toml_front_matter"]: stats["toml_front_matter"] += 1
        else: 
            file_passed = False
            file_failures.append("Missing/Invalid TOML Front Matter")

        if res["insight_section"]:
            stats["insight_section"] += 1
            if res["insight_points_count"] == 3:
                stats["insight_3_points"] += 1
            else:
                file_passed = False
                file_failures.append(f"Insight points count: {res['insight_points_count']} (Expected 3)")
        else:
            file_passed = False
            file_failures.append("Missing 핵심 인사이트 section")

        if all(res["roman_sections"].values()):
            stats["all_roman_sections"] += 1
        else:
            file_passed = False
            missing = [k for k, v in res["roman_sections"].items() if not v]
            file_failures.append(f"Missing Roman sections: {', '.join(missing)}")

        if all(res["section_summaries"].values()):
            stats["all_section_summaries"] += 1
        else:
            file_passed = False
            missing = [k for k, v in res["section_summaries"].items() if not v]
            file_failures.append(f"Missing section summaries in: {', '.join(missing)}")

        if res["concept_map"]: stats["concept_map"] += 1
        else:
            file_passed = False
            file_failures.append("Missing 📌 관련 개념 맵")

        if res["children_explanation"]: stats["children_explanation"] += 1
        else:
            file_passed = False
            file_failures.append("Missing 👶 어린이를 위한 3줄 비유 설명")

        if file_passed:
            passed_all += 1
        else:
            failures.append({
                "file": os.path.relpath(file_path, base_dir),
                "reasons": file_failures
            })

    print("\n=== Audit Summary ===")
    print(f"Total files audited: {total_files}")
    print(f"Files following all guidelines: {passed_all} ({passed_all/total_files*100:.2f}%)")
    
    print("\n--- Detailed Statistics ---")
    print(f"TOML Front Matter: {stats['toml_front_matter']/total_files*100:.2f}%")
    print(f"핵심 인사이트 Section: {stats['insight_section']/total_files*100:.2f}%")
    print(f"Exactly 3 Insight Points: {stats['insight_3_points']/total_files*100:.2f}%")
    print(f"All 5 Roman Sections (I-V): {stats['all_roman_sections']/total_files*100:.2f}%")
    print(f"All 5 Section Summaries: {stats['all_section_summaries']/total_files*100:.2f}%")
    print(f"📌 관련 개념 맵: {stats['concept_map']/total_files*100:.2f}%")
    print(f"👶 어린이를 위한 3줄 비유 설명: {stats['children_explanation']/total_files*100:.2f}%")

    if failures:
        print("\n--- Sample Failures (First 10) ---")
        for f in failures[:10]:
            print(f"- {f['file']}: {', '.join(f['reasons'])}")

if __name__ == "__main__":
    main()
