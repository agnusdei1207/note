import os
import glob
import re

directory = "content/studynote/9_security/2_crypto"
files = glob.glob(os.path.join(directory, "*.md"))

for file in files:
    if "index" in file:
        continue
        
    filename = os.path.basename(file)
    match = re.match(r"^0(\d\d)_(.*)", filename)
    if match:
        old_num = int(match.group(1))
        new_num = old_num - 3
        new_filename = f"0{new_num}_{match.group(2)}"
        
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Update weight in frontmatter
        content = re.sub(r'weight\s*=\s*' + str(old_num), f'weight = {new_num}', content)
        # Update title numbering in frontmatter if any
        content = re.sub(r'title\s*=\s*"0' + str(old_num) + r'\.', f'title = "0{new_num}.', content)
        # Update markdown H1 title if any
        content = re.sub(r'#\s*0' + str(old_num) + r'\.', f'# 0{new_num}.', content)
        
        new_filepath = os.path.join(directory, new_filename)
        with open(new_filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        os.remove(file)
        print(f"Renamed {filename} to {new_filename} and updated content.")
