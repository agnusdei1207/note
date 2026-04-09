import re
import shutil
from pathlib import Path

base_dir = Path("content/studynote")
HEADING_RE = re.compile(r"^##\s+(\d+)\.\s+(.*)$")
KEYWORD_RE = re.compile(r"^(\d+)\.\s+(.*)$")
FILE_NUM_RE = re.compile(r"^(\d+)")

# 1. Load all keyword mappings across all subjects
subject_sections = {}
for subject_dir in base_dir.iterdir():
    if not (subject_dir.is_dir() and subject_dir.name[0].isdigit()):
        continue
    
    keyword_path = subject_dir / "_keyword_list.md"
    if not keyword_path.exists():
        continue

    lines = keyword_path.read_text(encoding="utf-8").splitlines()
    sections = []
    current_section = None
    
    # build folder map for this subject
    folder_map = {}
    for p in subject_dir.iterdir():
        if p.is_dir() and not p.name.startswith("."):
            match = FILE_NUM_RE.match(p.name)
            if match:
                folder_map[int(match.group(1))] = p

    for line in lines:
        heading = HEADING_RE.match(line.strip())
        if heading:
            if current_section:
                sections.append(current_section)
            current_section = {
                "index": int(heading.group(1)),
                "title": heading.group(2).strip(),
                "numbers": []
            }
            continue

        item = KEYWORD_RE.match(line.strip())
        if item and current_section:
            current_section["numbers"].append(int(item.group(1)))

    if current_section:
        sections.append(current_section)
        
    subject_sections[subject_dir] = {"sections": sections, "folder_map": folder_map}

# 2. Find all loose files
loose_files = []
for subject_dir in base_dir.iterdir():
    if not (subject_dir.is_dir() and subject_dir.name[0].isdigit()):
        continue
    uncat = subject_dir / "uncategorized"
    if uncat.exists():
        for path in uncat.glob("*.md"):
            match = FILE_NUM_RE.match(path.name)
            if match:
                loose_files.append((int(match.group(1)), path, subject_dir))

# 3. Match and move
for file_num, path, current_subject_dir in loose_files:
    moved = False
    
    # Search all subjects for this number
    for subj_dir, data in subject_sections.items():
        sections = data["sections"]
        folder_map = data["folder_map"]
        
        target_section = None
        for sec in sections:
            if sec["numbers"] and sec["numbers"][0] <= file_num <= sec["numbers"][-1]:
                target_section = sec
                break
                
        if target_section:
            target_folder = folder_map.get(target_section["index"])
            if target_folder:
                dest = target_folder / path.name
                shutil.move(str(path), str(dest))
                print(f"Moved {path.name} to {dest}")
                moved = True
                break
