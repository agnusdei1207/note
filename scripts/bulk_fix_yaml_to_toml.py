import os
import glob
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Case 1: Missing frontmatter entirely (starts with #)
    if content.startswith('# '):
        lines = content.split('\n')
        title_line = lines[0]
        title = title_line.replace('# ', '').strip()
        new_content = f"+++\ntitle = \"{title}\"\n+++\n\n" + content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    # Case 2: YAML frontmatter (---)
    if content.startswith('---\n'):
        # Extract YAML block
        parts = content.split('---\n', 2)
        if len(parts) == 3:
            yaml_content = parts[1]
            rest_content = parts[2]
            
            # Convert YAML to TOML (naive conversion for title, weight, etc)
            toml_lines = []
            for line in yaml_content.split('\n'):
                if not line.strip(): continue
                if ':' in line:
                    k, v = line.split(':', 1)
                    k = k.strip()
                    v = v.strip()
                    # if v is unquoted string, quote it if it's title
                    if k == 'title':
                        if not v.startswith('"'):
                            v = v.replace('"', '\\"')
                            v = f'"{v}"'
                    toml_lines.append(f"{k} = {v}")
            
            toml_content = "+++\n" + "\n".join(toml_lines) + "\n+++\n"
            new_content = toml_content + rest_content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
            
    return False

# Find all markdown files
md_files = glob.glob('content/**/*.md', recursive=True)
fixed_count = 0
for f in md_files:
    if "keyword_list" in f or "_index.md" in f: continue
    try:
        if process_file(f):
            fixed_count += 1
    except Exception as e:
        print(f"Error processing {f}: {e}")

print(f"Fixed {fixed_count} files.")
