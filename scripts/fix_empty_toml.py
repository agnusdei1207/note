import glob
import re

md_files = glob.glob('content/**/*.md', recursive=True)
count = 0
for f in md_files:
    if "keyword_list" in f or "_index.md" in f: continue
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if content.startswith('+++\n'):
            parts = content.split('+++\n', 2)
            if len(parts) == 3:
                toml_content = parts[1]
                lines = toml_content.split('\n')
                new_lines = []
                changed = False
                for line in lines:
                    if line.strip().endswith('='):
                        new_lines.append(line + ' ""')
                        changed = True
                    else:
                        new_lines.append(line)
                
                if changed:
                    new_content = '+++\n' + '\n'.join(new_lines) + '+++\n' + parts[2]
                    with open(f, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    count += 1
    except Exception as e:
        print(f"Error {f}: {e}")

print(f"Fixed {count} empty TOML values.")
