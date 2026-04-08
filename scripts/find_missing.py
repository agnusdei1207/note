import os
import glob
import re

def find_missing(subject_dir, max_val):
    files = glob.glob(f'{subject_dir}/[0-9]*.md')
    nums = set()
    for f in files:
        basename = os.path.basename(f)
        match = re.match(r'^0*([0-9]+)', basename)
        if match:
            nums.add(int(match.group(1)))
    
    missing = [i for i in range(1, max_val + 1) if i not in nums]
    return missing[:5]

print("ICT:", find_missing("content/studynote/6_ict_convergence", 1050))
print("Algorithm:", find_missing("content/studynote/8_algorithm_stats", 115))
print("BigData:", find_missing("content/studynote/16_bigdata", 100))
