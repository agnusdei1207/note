import os
import re

def parse_keyword_list(file_path):
    keywords = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'^\s*([0-9]+)\.\s*(.*)', line)
            if match:
                num = int(match.group(1))
                topic = match.group(2).strip()
                keywords[num] = topic
    return keywords

def audit_subject(subject_dir, keyword_file):
    print(f"Auditing {subject_dir}...")
    keywords = parse_keyword_list(keyword_file)
    
    files_to_delete = []
    found_numbers = {} # num -> list of file paths
    missing_keywords = set(keywords.keys())

    for root, dirs, files in os.walk(subject_dir):
        # Skip directories that contain their own keyword list (if they are separate subjects)
        # But for CA, all subfolders belong to the same keyword list
        
        for file in files:
            if not file.endswith('.md') or file.startswith('_'):
                continue
            
            match = re.match(r'^([0-9]+)_(.*)\.md$', file)
            if match:
                num = int(match.group(1))
                full_path = os.path.join(root, file)
                
                if num not in found_numbers:
                    found_numbers[num] = []
                found_numbers[num].append(full_path)
                
                if num in missing_keywords:
                    missing_keywords.remove(num)

    for num, paths in found_numbers.items():
        if num not in keywords:
            print(f"  [DELETE EXTRA NUM] {num}: {paths}")
            for p in paths:
                os.remove(p)
        elif len(paths) > 1:
            print(f"  [CLEANING DUPLICATE] {num}: {paths}")
            target_topic = keywords[num].lower()
            # Find which file matches the target_topic better
            to_keep = None
            for p in paths:
                filename = os.path.basename(p).lower()
                # Remove number prefix for comparison
                name_part = re.sub(r'^[0-9]+_', '', filename).replace('.md', '').replace('_', ' ')
                # Very simple match: is the name_part in the topic or vice-versa?
                # Or use the one created/modified most recently if sizes are similar?
                # Actually, the 'Correct' ones usually have names that are translations or transliterations
                # Let's check size. The high-quality rewrites I just did are likely the ones I want to keep
                # UNLESS they were for the wrong topic!
                
                # RE-EVALUATION:
                # The 'Correct' topic for 605 is "High-Level Synthesis".
                # My file list had "605_high_level_synthesis.md" (5KB) and "605_security_by_design.md" (17KB).
                # Even though "security_by_design" is higher quality (17KB), it is the WRONG TOPIC for 605.
                # So I must keep the 5KB one and then REWRITE it correctly later.
                
                if any(word in name_part for word in target_topic.split()):
                    to_keep = p
                    break
            
            if to_keep:
                print(f"    Keeping: {to_keep}")
                for p in paths:
                    if p != to_keep:
                        os.remove(p)
            else:
                print(f"    [WARNING] No clear winner for {num}. Manual check needed.")

    print(f"Summary for {subject_dir}:")
    print(f"  Missing Keywords: {len(missing_keywords)}")
    print(f"  Total Distinct Numbers Found: {len(found_numbers)}")
    
    return files_to_delete, missing_keywords

if __name__ == "__main__":
    extra_files, missing = audit_subject("content/studynote/01_computer_architecture", "content/studynote/01_computer_architecture/_keyword_list.md")
    
    # Save extra files to a temporary file for deletion
    with open("extra_files_ca.txt", "w") as f:
        for file in extra_files:
            f.write(file + "\n")
