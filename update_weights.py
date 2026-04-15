import os
import re

def update_files(root_dir):
    updated_count = 0
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if not file.endswith('.md'):
                continue
            
            file_path = os.path.join(root, file)
            content = None
            for encoding in ['utf-8', 'cp949', 'euc-kr', 'latin-1']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                print(f"Could not read file: {file_path}")
                continue
            
            # Extract front matter
            fm_match = re.match(r'^\+\+\+\n(.*?)\n\+\+\+', content, re.DOTALL)
            if not fm_match:
                continue
            
            fm_content = fm_match.group(1)
            original_fm = fm_content
            
            new_weight = None
            if file == '_index.md':
                # Use parent directory name
                dir_name = os.path.basename(root)
                match = re.match(r'^(\d+)_', dir_name)
                if match:
                    new_weight = int(match.group(1))
            else:
                # Use filename
                match = re.match(r'^(\d+)_', file)
                if match:
                    new_weight = int(match.group(1))
            
            # Update weight in front matter
            if new_weight is not None:
                if 'weight =' in fm_content:
                    fm_content = re.sub(r'weight\s*=\s*\d+', f'weight = {new_weight}', fm_content)
                else:
                    # Insert weight at the beginning
                    fm_content = f'weight = {new_weight}\n' + fm_content
            
            # Update sort_by for _index.md
            if file == '_index.md':
                if 'sort_by =' in fm_content:
                    fm_content = re.sub(r'sort_by\s*=\s*".*?"', 'sort_by = "weight"', fm_content)
                else:
                    fm_content += '\nsort_by = "weight"'
            
            if fm_content != original_fm:
                new_content = content[:fm_match.start(1)] + fm_content + content[fm_match.end(1):]
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1
                
    return updated_count

if __name__ == "__main__":
    count = update_files('/mnt/c/workspace/brainscience/content/studynote/')
    print(f"Total files updated: {count}")
