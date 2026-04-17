import os
import re
import subprocess

def pad_directory_names(base_dir):
    for root, dirs, files in os.walk(base_dir, topdown=False):
        for dir_name in dirs:
            match = re.match(r'^(\d+)_+(.*)$', dir_name)
            if match:
                num = int(match.group(1))
                rest = match.group(2)
                padded_name = f"{num:02d}_{rest}"
                if padded_name != dir_name:
                    old_path = os.path.join(root, dir_name)
                    new_path = os.path.join(root, padded_name)
                    print(f"Renaming {old_path} to {new_path}")
                    subprocess.run(["git", "mv", old_path, new_path])

pad_directory_names("content/studynote")
