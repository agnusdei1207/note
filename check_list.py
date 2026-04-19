import os
import re

def check_numbering(filepath):
    nums = []
    with open(filepath, "r") as f:
        for line in f:
            match = re.match(r'^(\d+)\.\s+', line.strip())
            if match:
                nums.append(int(match.group(1)))
    
    if not nums:
        return
    
    # check if it restarts
    restarts = sum(1 for i in range(1, len(nums)) if nums[i] <= nums[i-1])
    print(f"{filepath}: total {len(nums)} items, restarts {restarts} times.")
    if restarts > 0:
        print("  Sample:", nums[:20])

base_dir = "content/studynote"
subjects = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and re.match(r'^\d{2}_', d)])

for subject in subjects:
    kw_file = os.path.join(base_dir, subject, "_keyword_list.md")
    if os.path.exists(kw_file):
        check_numbering(kw_file)
