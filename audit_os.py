import re
import os
import glob

def get_os_topics():
    topics = {}
    with open('content/studynote/2_operating_system/_keyword_list.md', 'r', encoding='utf-8') as f:
        content = f.read()
        # Match "Number. Title - Description" or "Number. Title"
        matches = re.findall(r'^(\d+)\.\s+(.*?)(?:\s+-\s+.*)?$', content, re.MULTILINE)
        for num, title in matches:
            topics[int(num)] = title.strip()
    return topics

def get_existing_os_files():
    files = glob.glob('content/studynote/2_operating_system/**/*.md', recursive=True)
    existing_nums = set()
    for f in files:
        basename = os.path.basename(f)
        if basename.startswith('_'): continue
        match = re.match(r'^(\d+)_', basename)
        if match:
            existing_nums.add(int(match.group(1)))
    return existing_nums

def audit_os():
    topics = get_os_topics()
    existing = get_existing_os_files()
    missing = []
    for num in range(1, 801):
        if num not in existing:
            if num in topics:
                missing.append((num, topics[num]))
            else:
                missing.append((num, "Unknown Topic"))
    return missing

if __name__ == "__main__":
    missing = audit_os()
    print(f"Total missing: {len(missing)}")
    for num, title in missing:
        print(f"{num}: {title}")
