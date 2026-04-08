import os
import glob
import re

def get_max_num(subject_dir):
    files = glob.glob(f'{subject_dir}/[0-9]*.md')
    nums = []
    for f in files:
        basename = os.path.basename(f)
        match = re.match(r'^0*([0-9]+)_', basename)
        if match:
            nums.append(int(match.group(1)))
        elif re.match(r'^0*([0-9]+)\.md$', basename):
            nums.append(int(re.match(r'^0*([0-9]+)\.md$', basename).group(1)))
    return max(nums) if nums else 0

dirs = {
    "ICT": "content/studynote/6_ict_convergence",
    "Algorithm": "content/studynote/8_algorithm_stats",
    "BigData": "content/studynote/16_bigdata"
}

for name, d in dirs.items():
    print(f"{name}: Max={get_max_num(d)}")
