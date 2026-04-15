import os
import re

ROOT_DIR = "/mnt/c/workspace/brainscience/content/studynote/"

def get_leading_number(name):
    match = re.match(r"^(\d+)", name)
    if match:
        return int(match.group(1))
    return None

def extract_weight_from_content(content):
    match = re.search(r"weight\s*=\s*(\d+)", content)
    if match:
        return int(match.group(1))
    return None

def update_file(path, new_weight, is_index):
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="latin-1") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return False

    new_content = content
    # Find weight in front matter
    # We use a more specific regex to only target weight in the front matter
    weight_pattern = re.compile(r"^(weight\s*=\s*)(\d+)", re.MULTILINE)
    
    if weight_pattern.search(content):
        new_content = weight_pattern.sub(fr"\g<1>{new_weight}", content)
    else:
        # Insert weight if missing
        if content.startswith("+++"):
            new_content = content.replace("+++", f"+++\nweight = {new_weight}", 1)
        elif content.startswith("---"):
            new_content = content.replace("---", f"---\nweight = {new_weight}", 1)

    if is_index:
        # Ensure sort_by = "weight"
        if 'sort_by = "weight"' not in new_content:
            if '+++' in new_content:
                new_content = new_content.replace("+++", '+++\nsort_by = "weight"', 1)
            elif '---' in new_content:
                new_content = new_content.replace("---", '---\nsort_by = "weight"', 1)
        
    if new_content != content:
        try:
            with open(path, "w", encoding="latin-1") as f:
                f.write(new_content)
            return True
        except Exception as e:
            print(f"Error writing to {path}: {e}")
            return False
    return False

print("Starting weight correction...")
updated_count = 0

for root, dirs, files in os.walk(ROOT_DIR):
    children = []
    
    # Process files in this directory
    for f in files:
        if f.endswith(".md") and f != "_index.md":
            path = os.path.join(root, f)
            base_weight = get_leading_number(f)
            if base_weight is None:
                try:
                    with open(path, "r", encoding="latin-1") as fp:
                        head = fp.read(1000)
                        base_weight = extract_weight_from_content(head) or 999
                except:
                    base_weight = 999
            children.append({
                "name": f,
                "path": path,
                "is_index": False,
                "base_weight": base_weight
            })
            
    # Process subdirectories in this directory (if they have _index.md)
    for d in dirs:
        index_path = os.path.join(root, d, "_index.md")
        if os.path.exists(index_path):
            base_weight = get_leading_number(d)
            if base_weight is None:
                try:
                    with open(index_path, "r", encoding="latin-1") as fp:
                        head = fp.read(1000)
                        base_weight = extract_weight_from_content(head) or 999
                except:
                    base_weight = 999
            children.append({
                "name": d,
                "path": index_path,
                "is_index": True,
                "base_weight": base_weight
            })
            
    # Sort all siblings (files and subdirs) and assign unique weights
    if children:
        children.sort(key=lambda x: (x["base_weight"], x["name"]))
        
        current_weight = -1
        for child in children:
            new_weight = max(child["base_weight"], current_weight + 1)
            if update_file(child["path"], new_weight, child["is_index"]):
                updated_count += 1
            current_weight = new_weight

    # Ensure root _index.md of current root has sort_by = "weight"
    root_index = os.path.join(root, "_index.md")
    if os.path.exists(root_index):
        try:
            with open(root_index, "r", encoding="latin-1") as f:
                content = f.read()
            if 'sort_by = "weight"' not in content:
                new_content = content
                if '+++' in content:
                    new_content = content.replace("+++", '+++\nsort_by = "weight"', 1)
                elif '---' in content:
                    new_content = content.replace("---", '---\nsort_by = "weight"', 1)
                if new_content != content:
                    with open(root_index, "w", encoding="latin-1") as f:
                        f.write(new_content)
                    updated_count += 1
        except Exception as e:
            print(f"Error checking root index {root_index}: {e}")

print(f"Weight correction complete. Total files updated: {updated_count}")
