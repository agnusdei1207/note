import os
import re

dir_path = "content/studynote"
updated = 0

for root, _, files in os.walk(dir_path):
    if "_trash" in root: continue
    for file in files:
        if file.endswith(".md") and not file.startswith("_"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find broken title: title = "..."..."
            tm = re.search(r'title\s*=\s*"([^"]*\\"?[^"]*)"(.*)"', content)
            if tm:
                # If there's a trailing quote part due to bad replace
                # Let's just fix it manually by re-reading the correct title from the first part
                # Actually, simpler: find lines starting with title =
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('title = "'):
                        # If there are multiple unescaped quotes or trailing garbage
                        # Let's extract the part after 'title = "' and before the last '"'
                        match = re.match(r'title = "(.*)"', line)
                        if match:
                            val = match.group(1)
                            # If it looks like: "46. ... \"Never Trust...\""Never Trust..."
                            if val.endswith('"') or '\\"' in val:
                                # Just clean it up: remove trailing garbage
                                # We can just parse the file number and fetch from keyword_list
                                pass

# Actually, the easiest way to fix TOML parse error is to rewrite the script to properly set title line.
# Let's just use Python's regex to replace the entire line starting with `title = ` or `title: `
EOF
